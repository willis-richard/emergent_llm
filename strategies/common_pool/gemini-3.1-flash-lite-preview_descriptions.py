"""
Strategy descriptions for common_pool.

Generated with:
- Provider: Client
- Model: gemini-3.1-flash-lite-preview
"""


description_COLLECTIVE_1 = '''
This strategy adopts a conditional cooperative approach based on a "Tit-for-Tat with Forgiveness and Stock Sensitivity" logic. The objective is to maintain the stock near capacity to maximize long-term yields while punishing defection only when it threatens sustainability.

**Initialization**
In the first round, play C (Cooperate).

**Round Strategy (t = 1 to r-1)**
1. **Cooperation Threshold:** If the number of opponents who cooperated in the previous round ($C_{t-1}$) is $\ge \lceil \frac{n}{2} \rceil$, continue to play C.
2. **Defection Response:** If $C_{t-1} < \lceil \frac{n}{2} \rceil$, play D (Defect) for the current round.
3. **Stock Safety Override:** Regardless of opponent history, if the current stock $S_t$ falls below the critical threshold $S_{crit} = \frac{capacity}{4}$, switch to D immediately to harvest the remaining value before exhaustion, unless $C_{t-1} = n$ (all players cooperating), in which case maintain C to allow recovery.
4. **Forgiveness:** If D was played in the previous round because of insufficient cooperation, but in the most recent round $C_{t-1}$ returns to $\ge \lceil \frac{n}{2} \rceil$, revert to playing C.

**Last Round (t = r)**
In the final round, play D (Defect) regardless of previous history or current stock.

**Pseudocode Representation**

```python
def choose_action(round, total_rounds, n, stock, prev_opponents_C):
    # Terminal round: extract remaining value
    if round == total_rounds:
        return 'D'
    
    # First round: start cooperative
    if round == 1:
        return 'C'
    
    # Stock safety: if resource is critically low, defect 
    # unless everyone is cooperating (trusting recovery)
    if stock < (capacity / 4) and prev_opponents_C < (n - 1):
        return 'D'
        
    # Reciprocal cooperation: match majority behavior
    if prev_opponents_C >= ceil(n / 2):
        return 'C'
    else:
        return 'D'
```
'''

description_COLLECTIVE_2 = '''
Maintain a Tit-for-Tat strategy based on the aggregate behavior of the population, incorporating a "grim" component for the final rounds to prevent terminal defection.

### Decision Rules

**Round 1:**
Always play **Cooperate (C)**. This initiates the cooperative equilibrium and signals a willingness to sustain the pool.

**Intermediate Rounds ($1 < t < r$):**
Observe the aggregate cooperation count from the previous round ($C_{t-1}$).
1.  **Full Cooperation:** If all $n$ players cooperated in the previous round, continue to **Cooperate (C)**.
2.  **Partial Defection:** If $k$ players cooperated in the previous round ($0 \le k < n$), play **Defect (D)** with a probability proportional to the observed defection. Specifically, play **Defect (D)** if $k < n$, provided the stock $S_t > 0$. If $k = n-1$ (only one defector), "forgive" after one round of defection by returning to **Cooperate (C)** in the next round. If $k < n-1$, punish by playing **Defect (D)** for the next two rounds.

**Final Rounds ($t \ge r - 1$):**
Transition to **Defect (D)** if the aggregate stock $S_t$ is declining significantly (below 50% of capacity). If $S_t$ is stable (near capacity), continue with the conditional cooperation logic used in intermediate rounds.

### Edge Case Handling

*   **Stock Depletion ($S_t \le \text{threshold}$):** If the stock level $S_t$ falls below $10$ (or a value insufficient to sustain growth, defined as $2 \times S \times (1 - S/capacity) < \text{minimum consumption}$), switch immediately to **Defect (D)** to extract remaining utility before the resource collapses.
*   **Zero Stock:** If $S_t = 0$, play **Defect (D)** by default, as no further cooperation is possible.
*   **The "Last-Mover" Correction:** In the final round ($t=r$), ignore all previous history and play **Defect (D)**, as there is no future utility to protect.

### Pseudocode Representation

```python
def get_action(round, total_rounds, n, stock, prev_round_cooperators):
    # Final round: Always defect
    if round == total_rounds:
        return 'D'
    
    # Critical depletion: Always defect
    if stock < (capacity * 0.1): # Threshold for recovery
        return 'D'
    
    # First round: Cooperate
    if round == 1:
        return 'C'
    
    # Tit-for-Tat logic
    if prev_round_cooperators == n:
        return 'C'
    elif prev_round_cooperators == (n - 1):
        # Forgive single defector
        return 'C'
    else:
        # Punish mass defection
        return 'D'
```
'''

description_COLLECTIVE_3 = '''
Adopt a "Trigger-Modified Tit-for-Tat" strategy, which prioritizes sustainability through conditional cooperation while managing defectors.

### Decision Rules
In any round $t$, track the number of players $k_t$ who chose $C$ in the previous round $t-1$.

1.  **Round 1:** Play $C$.
2.  **Subsequent Rounds ($t > 1$):**
    *   **Cooperation Trigger:** If the stock $S_t > \frac{capacity}{2n}$ and the average behavior in the previous round ($k_{t-1}/n$) exceeds a threshold $\tau = 0.5$, play $C$.
    *   **Defection Response:** If the stock $S_t$ drops below $\frac{capacity}{2n}$ or if $k_{t-1}/n \le \tau$, play $D$.
    *   **Recovery:** If you have played $D$ in response to low cooperation or low stock, return to $C$ only if the stock $S_t$ recovers to $\ge \frac{capacity}{n}$ and the average cooperation rate $k/n$ returns to $>\tau$ for two consecutive rounds.

### Edge Cases
*   **Final Round:** If $t = r$, play $D$ regardless of prior history. The accumulation of resources serves no future purpose, and the game structure terminates, removing the incentive for future cooperation.
*   **Low Stock:** Regardless of opponent cooperation, if $S_t < \frac{capacity}{4n}$ (a critical sustainability threshold), play $D$. When the resource is insufficient to support sustainable growth, individual consumption takes precedence over pool maintenance.
*   **Anonymity Constraint:** Since players are anonymous, the strategy treats the aggregate cooperation count ($k_{t-1}$) as a sufficient statistic for the "health" of the cooperative norm. Do not attempt to track specific individuals.

### Pseudocode
```python
def get_action(round_number, total_rounds, current_stock, prev_round_cooperators, n, capacity):
    # Terminal round behavior
    if round_number == total_rounds:
        return 'D'
    
    # Critical resource depletion
    if current_stock < (capacity / (4 * n)):
        return 'D'
    
    # Round 1 behavior
    if round_number == 1:
        return 'C'
    
    # Adaptive Trigger logic
    cooperation_rate = prev_round_cooperators / n
    
    # If the cooperative norm is stable, continue cooperating
    if cooperation_rate > 0.5 and current_stock >= (capacity / (2 * n)):
        return 'C'
    
    # Otherwise, punish or conserve
    return 'D'
```
'''

description_COLLECTIVE_4 = '''
**Strategy: Adaptive Reciprocal Sustainability (ARS)**

This strategy operates on the principle of conditional cooperation, maintaining the common pool resource at a level that maximizes long-term yield while punishing defectors to protect the stock. It treats the game as a series of states requiring balancing current consumption against future availability.

**Decision Rules:**

1.  **Initialization:** In Round 1, always play **Cooperate (C)**.

2.  **State Assessment:** At the start of each round $t > 1$, define the "Sustainability Threshold" ($T$) as the stock level $S$ required to sustain the population over $r-t+1$ rounds if everyone cooperates. If $S < \text{capacity} / 2$, the stock is considered critical.

3.  **Action Selection Logic:**
    For any round $t$:
    *   **Phase 1 (Stock Recovery):** If $S < \text{capacity} / 4$, prioritize growth. Play **C** regardless of opponent behavior in the previous round to ensure the stock does not collapse to 0.
    *   **Phase 2 (Cooperative Equilibrium):** If $S \geq \text{capacity} / 4$, observe the aggregate cooperation count from round $t-1$.
        *   If at least $n-1$ players cooperated in the previous round, play **C**.
        *   If fewer than $n-1$ players cooperated in the previous round, enter the **Punishment Phase**.

4.  **Punishment Phase:**
    *   If the aggregate cooperation count in $t-1$ falls below the threshold, play **Defect (D)** for one round to extract remaining value before potential depletion.
    *   Return to **C** in the following round ($t+1$) *if and only if* the stock $S$ remains above $\text{capacity} / 8$. If the stock falls below $\text{capacity} / 8$ after a punishment round, default to **C** in the next round to prevent terminal depletion.

5.  **Terminal Phase:**
    In the final round $r$:
    *   If $S > \text{capacity} / 2$, play **D** to maximize terminal utility.
    *   If $S \leq \text{capacity} / 2$, play **C** to avoid a zero-sum depletion that reduces the total payoff of the final round.

**Pseudocode:**

```python
def choose_action(round, stock, prev_opp_coop_count, n, r, capacity):
    # Terminal Round Logic
    if round == r:
        return 'D' if stock > (capacity / 2) else 'C'
    
    # Initialization
    if round == 1:
        return 'C'
        
    # Stock Protection Logic
    if stock < (capacity / 4):
        return 'C'
        
    # Reciprocity Logic
    # n-1 allows for one 'error' or single defector without triggering mass defection
    if prev_opp_coop_count >= (n - 1):
        return 'C'
    else:
        # Punishment or Extraction
        if stock > (capacity / 8):
            return 'D'
        else:
            return 'C'
```

**Edge Case Handling:**
*   **Mass Defection:** If the system observes that total cooperation is consistently low, the strategy shifts to perpetual **C** only if $S$ is near critical levels, otherwise it oscillates between **D** and **C** to prevent the strategy from being exploited indefinitely while still attempting to keep the pool alive.
*   **Stock Depletion:** If $S \approx 0$, the strategy ignores reciprocity and plays **C** in a "Hail Mary" attempt to allow regrowth if other players also switch to **C**.
'''

description_PROSOCIAL_1 = '''
The strategy follows a conditional cooperation protocol based on a target "sustainable consumption" threshold, adapted dynamically according to the observed state and recent opponent behavior.

**Core Logic: Sustainable Targeting**
The optimal long-term strategy requires keeping the stock near `capacity` to maximize future growth, as the growth function peaks at `S = capacity/2`. The ideal state is full replenishment (`new_stock ≈ capacity`), which occurs if total consumption is exactly 50% of `capacity` (since 0.5 capacity remains, and growth adds 0.5 capacity).

Let `C_target` be the number of cooperators required to keep the pool sustainable. Because `C` consumes `S/(2n)` and `D` consumes `S/n`, the total consumption is:
`Total_Consumption = [k * S/(2n)] + [(n - k) * S/n]`
`Total_Consumption = S * [k/(2n) + 2(n-k)/(2n)] = S * (2n - k) / (2n)`

To sustain the pool, we aim for a total consumption of `S/2`. Solving `S * (2n - k) / (2n) = S/2` yields `2n - k = n`, or `k = n`. Therefore, full cooperation is necessary for long-term sustainability.

**Decision Rules**
Define `k_obs` as the number of cooperators observed in the previous round (where `k_obs` = total cooperators, including self if I cooperated).

*   **Round 1:** Play C.
*   **Round 2 to r-1:**
    *   If `S < (capacity / 4)`: Play D. (The resource is too depleted to recover via cooperation alone; exploit remaining stock before it collapses).
    *   Else if `k_obs >= n - 1` (allowing for one accidental defection or noise): Play C.
    *   Else (if `k_obs < n - 1`): Play D. (Retaliate against widespread defection to minimize individual losses).
*   **Round r (Last Round):**
    *   If `S > capacity / 2`: Play D.
    *   Else: Play C (or D, as payoff is identical).

**Pseudocode**

```python
def decide_action(round, S, n, capacity, history):
    # History stores {round_t: k_obs}
    
    # 1. Terminal Phase
    if round == r:
        return 'D' if S > (capacity / 2) else 'C'
    
    # 2. Rescue Phase
    # If stock is critically low, cooperation yields insufficient return
    if S < (capacity / 4):
        return 'D'
        
    # 3. Cooperation Phase
    # First round
    if round == 1:
        return 'C'
        
    # Conditional Cooperation: Tit-for-Tat variant
    # Maintain cooperation if the majority cooperated previously
    prev_k = history[round - 1]
    
    # If most players cooperated, sustain the system
    if prev_k >= (n - 1):
        return 'C'
        
    # If system is collapsing due to mass defection, punish/exploit
    return 'D'
```

**State Handling**
*   **Edge Case: `S = 0`:** If the stock reaches 0, the game is effectively terminated regardless of action; play D by default.
*   **Edge Case: `n=2`:** The threshold `k_obs >= n - 1` becomes `k_obs >= 1`. This requires at least one other cooperator to justify staying in the cooperative state. If the other player defects (`k_obs = 0`), switch to D.
'''

description_PROSOCIAL_2 = '''
The strategy operates on a "Conditional Tit-for-Tat with Sustainability Thresholds" model. The goal is to maximize long-term yield by maintaining the common pool stock at the capacity level ($S = \text{capacity}$) while punishing defectors to discourage free-riding.

### Core Logic

The decision to cooperate ($C$) or defect ($D$) depends on two primary factors: the current stock level ($S$) and the observed cooperation rate of the group in the previous round ($C_{prev}$).

**Decision Rule:**

1.  **Initialization (Round 1):** Play $C$.

2.  **Steady State (Rounds 2 to $r-1$):**
    *   **Sustainability Check:** If $S < \text{capacity} \times 0.5$, play $D$ to minimize individual loss while the stock is in a collapse state (the pool is already failing to regenerate).
    *   **Cooperation Assessment:** If $S \ge \text{capacity} \times 0.5$:
        *   Calculate the observed cooperation rate of the opponents in the previous round. If all opponents played $C$, play $C$.
        *   If the number of defectors in the previous round was $> 0$, play $D$ for one round. This serves as a "tit-for-tat" signal to punish current defectors and signal that cooperation is conditional.
        *   Exception: If the previous round resulted in a net increase or maintenance of stock (i.e., $S_{t} \ge S_{t-1}$), play $C$ regardless of previous defects, provided $S \ge \text{capacity} \times 0.8$. This "forgiving" behavior prevents spiraling into mutual defection loops when the pool is healthy.

3.  **Terminal Phase (Final Round $r$):**
    *   Play $D$ regardless of stock level or opponent history. This is the dominant strategy in the final round of a finitely repeated prisoner's dilemma variant, as there are no future rounds to influence.

### Pseudocode Implementation

```python
def decide_action(round_number, current_stock, prev_opp_coop_count, total_opponents, capacity, r):
    # Terminal Phase
    if round_number == r:
        return 'D'
    
    # Sustainability Thresholds
    if current_stock < (0.5 * capacity):
        return 'D'
        
    # Healthy Pool Logic
    # Opponent defectors count
    num_defectors = total_opponents - prev_opp_coop_count
    
    # Punish defectors if the pool is not expanding
    if num_defectors > 0:
        # Check if we are still recovering stock
        if current_stock < (0.8 * capacity):
            return 'D' # Punish defectors
        else:
            return 'C' # Forgive defectors if pool is near capacity
            
    # Default behavior when opponents cooperate
    return 'C'
```

### Edge Case Handling

*   **Stock Collapse ($S \to 0$):** If the stock drops below the threshold required for recovery, the strategy switches to defecting to capture remaining value before the pool hits zero, as cooperative efforts become mathematically futile when the growth function fails to replenish.
*   **Mass Defection:** If the group enters a pattern of mass defection, the strategy remains in $D$ to preserve individual payoff until the stock recovers naturally via the growth function or until a new equilibrium is forced.
*   **Observation Noise/Uncertainty:** Because the strategy treats all opponents as a single aggregate (due to anonymity), the "punishment" is applied globally if *any* defection is detected, maximizing the deterrent signal strength.
'''

description_PROSOCIAL_3 = '''
The strategy employs a "Target-Stock Tit-for-Tat" mechanism, aiming to maintain the common pool resource at a level that maximizes sustainable yield while punishing unilateral defection. The core objective is to reach and stabilize the stock at its maximum sustainable capacity, which occurs when total consumption per round equals total growth per round.

### Strategy Rules

**1. Target State:**
Calculate the "optimal" stock level $S^*$ that allows for sustainable extraction. In this game, full cooperation by all $n$ players (consumption of $S/(2n)$ each) leads to total consumption of $S/2$. For sustainability, $S/2 = \text{Growth}(S_{remaining})$, where $S_{remaining} = S/2$.
Solving $S/2 = 2 \times (S/2) \times (1 - (S/2)/\text{capacity})$ results in $S = \text{capacity}$. Therefore, the target stock is the full capacity.

**2. Decision Logic:**
Let $N_c(t-1)$ be the number of cooperators observed in the previous round.

*   **Round 1:** Always play **Cooperate**.
*   **Rounds 2 to $r-1$:**
    *   If $S_t \geq \text{capacity} \times 0.5$:
        *   If $N_c(t-1) = n$ (all cooperated in previous round), play **Cooperate**.
        *   If $N_c(t-1) < n$ (defection occurred), play **Defect**.
    *   If $S_t < \text{capacity} \times 0.5$:
        *   Play **Defect** regardless of $N_c(t-1)$, unless $S_t$ drops below a critical threshold (defined as $\text{capacity} / 2n$), at which point play **Cooperate** to prevent total collapse.
*   **Round $r$:**
    *   If $N_c(t-1) = n$, play **Cooperate**.
    *   If $N_c(t-1) < n$, play **Defect**.

### Pseudocode Implementation

```python
def get_action(round_number, current_stock, prev_round_cooperators, n, capacity):
    # Round 1: Build trust/start prosocial
    if round_number == 1:
        return 'C'
    
    # Last round: Defect if the group has not maintained full cooperation
    if round_number == r:
        if prev_round_cooperators == n:
            return 'C'
        else:
            return 'D'

    # General state-dependent logic
    # If the pool is healthy (>= 50% capacity), reward cooperation
    if current_stock >= (capacity * 0.5):
        if prev_round_cooperators == n:
            return 'C'
        else:
            return 'D'
    
    # If the pool is recovering or low, force Defect to extract value before total depletion,
    # unless critical exhaustion threshold (1 / 2n of capacity) is reached.
    else:
        critical_threshold = capacity / (2 * n)
        if current_stock < critical_threshold:
            return 'C'  # Last-ditch effort to prevent collapse
        else:
            return 'D'
```

### Edge Case Handling

*   **Recovery from Defection:** If the system is in a state of depletion due to others' defection, the strategy switches to **Defect** to maximize immediate payoff, as cooperative extraction will not stop the stock from trending toward zero if others are depleting it rapidly. The strategy only reverts to **Cooperate** if the pool enters a critical recovery state or if the previous round demonstrates a return to universal cooperation.
*   **Threshold Awareness:** The strategy implicitly recognizes that if the stock is below 50% of capacity, the system is in a trajectory of net loss if all players consume. Thus, it assumes the current group dynamics are non-cooperative and shifts to individual payoff maximization.
*   **Last Round:** The strategy behaves greedily if the history does not show perfect cooperation, effectively minimizing losses against defectors, but maintains altruism if the group has been perfectly cooperative, ensuring the game ends on a cooperative note if deserved.
'''

description_PROSOCIAL_4 = '''
The strategy operates on a "Tit-for-Tat with Forgiving Resilience" mechanism, calibrated to maintain the common pool at its maximum sustainable capacity by targeting the cooperative equilibrium where all players choose C.

**Decision Logic:**

1.  **Round 1:** Play **C**. This initiates cooperation and signals a prosocial intent to the pool.

2.  **Subsequent Rounds:**
    *   **Calculate Cooperation Threshold:** Let $K_t$ be the number of players who played **C** in the previous round $t-1$.
    *   **Decision Rule:**
        *   If $K_t = n$ (full cooperation in the previous round), play **C**.
        *   If $0 < K_t < n$ (partial cooperation), play **C** with probability $P(C) = \frac{K_t}{n}$.
        *   If $K_t = 0$ (full defection in the previous round), play **D** for one round to prevent exploitation, then revert to **C** in the next round to offer a restart.

3.  **State-Dependent Calibration (Stock Override):**
    *   If the current stock $S_t$ falls below a critical threshold $S_{crit} = \frac{capacity}{4}$, the strategy prioritizes immediate stock recovery. In this state, regardless of previous cooperation history, play **C** if and only if the current stock $S_t$ is less than or equal to the stock from the previous round $S_{t-1}$. This enforces a "sustainability-first" protocol during periods of collapse.

4.  **Final Round (Round $r$):**
    *   In the terminal round, the strategic incentive to cooperate vanishes. However, to maintain reputation and maximize long-term average outcomes against adaptive agents, play **C** if the average cooperation rate across rounds $1$ to $r-1$ was greater than or equal to $0.5$. Otherwise, play **D**.

**Pseudocode:**

```python
def get_action(round, stock, prev_stock, prev_cooperators, n):
    # Terminal Round Logic
    if round == r:
        avg_coop = calculate_historical_avg_cooperation()
        return C if avg_coop >= 0.5 else D
    
    # Recovery Override
    if stock < (capacity / 4):
        if stock <= prev_stock:
            return C
        else:
            return D

    # Main Tit-for-Tat Logic
    if prev_cooperators == n:
        return C
    elif prev_cooperators == 0:
        return D # Punish collapse
    else:
        # Probabilistic forgiveness
        return C if random.random() < (prev_cooperators / n) else D
```
'''

description_ALTRUISTIC_1 = '''
The strategy employs a "Target Stock Management" (TSM) approach, aiming to maintain the common pool resource at the capacity level to maximize long-term sustainable yield for all players. Cooperation is prioritized, but the strategy includes a dynamic defense mechanism to prevent resource collapse caused by excessive defection.

### Core Logic
The strategy relies on tracking the expected stock level required to maintain the pool at capacity. In each round, the algorithm calculates an "Acceptable Defection Threshold" (ADT) based on the current stock level and the remaining number of rounds.

### Decision Rules
1.  **Initialization (Round 1):** Always play Cooperate (C).
2.  **Observation:** After each round $t$, calculate the *Actual Stock Growth* observed. Compare the actual stock at the start of round $t+1$ ($S_{t+1}$) against the *Predicted Stock* ($S_{pred}$) that would have existed had all players cooperated in round $t$.
3.  **State Assessment:**
    *   **If $S_t \ge 0.5 \times \text{capacity}$:** Play Cooperate (C).
    *   **If $S_t < 0.5 \times \text{capacity}$:** Trigger a "Restoration Phase." If the number of defectors in the previous round was 0, play Cooperate (C) to allow natural regeneration. If the number of defectors was $> 0$, play Defect (D) only if the stock is critically low (under $0.2 \times \text{capacity}$), otherwise play C.
4.  **Reciprocity Trigger:** If the stock level at the start of any round is less than $75\%$ of the previous round's stock, switch to Defect (D) for exactly one round to recover the lost utility before reverting to Cooperate (C).
5.  **Final Rounds:** In the final round ($t = r$), play Defect (D) regardless of stock, as future growth no longer benefits any player.

### Pseudocode
```
// Constants
S_prev = capacity
Threshold_Recovery = 0.2 * capacity

// Decision per Round t
If t == r:
    Return D

If t == 1:
    Return C

If stock >= 0.5 * capacity:
    Return C

Else if stock < Threshold_Recovery:
    // Critical state: Protect or harvest before collapse
    If observed_defectors_previous_round > 0:
        Return D
    Else:
        Return C

Else: // 0.2 * capacity < stock < 0.5 * capacity
    // Check for resource depletion trend
    If stock < (0.75 * S_prev):
        S_prev = stock
        Return D
    Else:
        S_prev = stock
        Return C
```

### Edge Case Handling
*   **Rapid Depletion:** If the stock drops below the $0.2 \times \text{capacity}$ threshold, the strategy switches to Defect (D) to ensure the player secures a share of the remaining resource before total collapse occurs, as cooperative behavior in a dying pool yields negligible returns.
*   **Total Defection by Others:** If all other players defect, the stock will naturally deplete. In this scenario, the strategy will defect in the following round to extract utility, but immediately return to C if the stock level increases above the $0.5 \times \text{capacity}$ mark, signaling that the pool is recovering.
*   **End-of-Game Horizon:** The strategy strictly adheres to the "last-round defection" rule to capture remaining value, acknowledging that altruism has no future utility once the game terminates.
'''

description_ALTRUISTIC_2 = '''
**Strategy: Tit-for-Tat Sustainability (TFTS)**

**Core Philosophy:** Prioritize the maintenance of the common pool stock at `capacity` (the optimal growth point) to maximize collective long-term returns. Cooperate as long as the resource is sustainable, but penalize excessive consumption by others to prevent stock collapse.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**.

2.  **Rounds $t > 1$:**
    *   **Observation:** Observe the previous round's outcome ($S_{t-1}$) and the total number of cooperators ($C_{t-1}$).
    *   **Threshold Check:** If $S_{t-1}$ is below a critical threshold (defined as $S < 0.2 \times \text{capacity}$), switch to **Cooperate (C)** regardless of previous defections to allow stock recovery.
    *   **Conditional Response:**
        *   If the aggregate behavior in the previous round resulted in the stock increasing or holding steady ($S_t \ge S_{t-1}$), play **Cooperate (C)**.
        *   If the aggregate behavior resulted in stock depletion ($S_t < S_{t-1}$), and the number of other players who defected ($D_{t-1}$) is greater than 0, play **Defect (D)** with a probability $p$ proportional to the defection rate of the previous round.
        *   Specifically, if $S_t < S_{t-1}$, play **Defect (D)** if the number of defectors $n_D > 0$. Otherwise, play **Cooperate (C)**.

3.  **End-Game Strategy (Final 3 Rounds):**
    *   Shift to **Defect (D)** if and only if the current stock $S_t > 0.5 \times \text{capacity}$. If $S_t \le 0.5 \times \text{capacity}$, maintain **Cooperate (C)** to prevent total collapse, even in the final round.

**Pseudocode:**

```python
def get_action(round, total_rounds, current_stock, prev_cooperators, n):
    prev_defectors = n - prev_cooperators
    
    # End-game logic
    if round > (total_rounds - 3):
        if current_stock > (0.5 * capacity):
            return D
        else:
            return C

    # Recovery mode
    if current_stock < (0.2 * capacity):
        return C

    # Tit-for-Tat logic
    if round == 1:
        return C
    
    # If resource is stable or growing, act altruistically
    if current_stock >= prev_stock_snapshot: 
        return C
    
    # If resource is shrinking due to defectors, match defection
    if prev_defectors > 0:
        return D
        
    return C
```

**Edge Case Handling:**
*   **Rapid Depletion:** If the stock drops below the threshold required to sustain growth, the strategy enters "Recovery Mode," forcing **Cooperate (C)** to minimize immediate draw, regardless of whether others are defecting.
*   **Total Defection:** If all other players defect, this strategy will also defect to avoid being the sole contributor to an already doomed stock pool, unless the stock is critically low.
*   **Anonymity:** Since identity is unknown, the strategy acts based solely on the aggregate count of defections from the previous round, treating all opponents as a single collective entity.
'''

description_ALTRUISTIC_3 = '''
The strategy employs a "Conditional Sustainability" approach, designed to maximize the longevity and yield of the common pool while punishing exploitation only to the extent necessary to preserve the resource.

### Core Strategy Logic

The objective is to maintain the stock level at exactly 50% of the `capacity`, as this maximizes the logistic growth rate of the resource (2 × S × (1 - S/capacity)). 

Let $S_t$ be the stock at the start of round $t$, and $n$ be the number of players. Let $k_t$ be the number of cooperators observed in the previous round $t-1$.

**Decision Rule:**
In every round $t$, play $C$ if the following condition is met, otherwise play $D$:

$$S_t \times \left( \frac{k_{t-1} + 2(n - k_{t-1})}{2n} \right) \leq \text{Optimal Consumption Threshold}$$

Where the "Optimal Consumption Threshold" is calculated to maintain the stock at 50% capacity after growth. Specifically, cooperate if:

1.  **Round 1:** Always play $C$.
2.  **Rounds $t > 1$:** Play $C$ if the resource stock $S_t$ is below 75% of `capacity` OR if the number of cooperators in the previous round $k_{t-1} \ge \lceil n/2 \rceil$.
3.  **Last Round:** Play $D$ regardless of state, as preservation for future rounds is irrelevant.

### Pseudocode Implementation

```python
def get_action(round_number, current_stock, total_rounds, n, k_prev, capacity):
    # Rule 1: Always defect in the final round
    if round_number == total_rounds:
        return 'D'
        
    # Rule 2: Always cooperate in the first round
    if round_number == 1:
        return 'C'
        
    # Rule 3: Conditional Sustainability
    # Cooperate if the stock is critically low (below 50% capacity)
    # OR if the group has shown a majority cooperation trend
    # Or if the stock is healthy but trending downward
    if current_stock < (0.75 * capacity) or k_prev >= (n / 2):
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling

*   **Stock Collapse ($S \approx 0$):** If the stock level falls below $1\%$ of `capacity`, the strategy reverts to $C$ regardless of history to prevent total extinction of the resource, assuming that a tiny potential payoff is better than zero.
*   **Capacity Saturation:** If $S_t > 0.9 \times \text{capacity}$, the strategy relaxes and allows for $D$ to capture value, as the growth rate drops significantly when the pool is near maximum capacity.
*   **Low $k_{t-1}$:** If the previous round showed widespread defection ($k_{t-1} < n/4$), the strategy plays $D$ for one round as a signal that exploitation is unsustainable, then resets to $C$ in the subsequent round to attempt to restart cooperation.
'''

description_ALTRUISTIC_4 = '''
The strategy adopts a conditional "Grim-Trigger with Forgiveness" approach, optimized for maintaining the common pool at its maximum sustainable capacity ($capacity$). It treats the population as a collective entity, cooperating as long as the aggregate behavior does not threaten the stock's future viability.

### Strategy Specification

**1. Definitions**
*   $T$: Current round index ($1$ to $r$).
*   $k$: Number of opponents who cooperated in the previous round.
*   $C_{prev}$: Boolean status of the strategy's own move in the previous round.
*   $S_t$: Stock level at the start of round $t$.
*   $S_{target}$: The optimal stock level required for maximum regeneration, defined as $capacity / 2$.

**2. Decision Logic**

*   **Round 1:** Always choose **Cooperate (C)**.
*   **Round $T > 1$:**
    *   **Condition A (Punishment Phase):** If the stock $S_t$ falls below $capacity \times 0.25$ OR if the number of defectors in the previous round exceeds $n/2$, switch to **Defect (D)** for one round to minimize immediate losses before the stock potentially collapses.
    *   **Condition B (Sustainability Check):** If the stock $S_t$ is sufficient ($S_t \geq capacity \times 0.5$), calculate the aggregate consumption required to return the stock to $capacity$ in the next round. If the previous round's total consumption caused the stock to drop below $capacity \times 0.5$, switch to **Cooperate (C)** regardless of opponent actions.
    *   **Condition C (Tit-for-Tat):** In all other scenarios, choose the action that matches the majority behavior of the opponents in the previous round. If $k \geq (n-1)/2$, choose **C**; otherwise, choose **D**.
    *   **Condition D (Endgame):** If $T = r$, choose **Defect (D)** if the stock $S_t$ is insufficient to sustain future growth (i.e., $S_t < capacity \times 0.2$), otherwise play according to Condition C.

### Pseudocode

```python
def choose_action(T, S_t, k, n, C_prev, r, capacity):
    # Round 1
    if T == 1:
        return 'C'
    
    # Endgame logic
    if T == r:
        if S_t < (capacity * 0.2):
            return 'D'
        else:
            return 'C' if k >= (n-1)/2 else 'D'
            
    # Crisis intervention: Punishment or survival mode
    # If the pool is critical, prioritize immediate extraction
    if S_t < (capacity * 0.25) or (n - 1 - k) > (n / 2):
        return 'D'
        
    # Sustainability maintenance
    # If the pool is healthy, reward cooperation
    if S_t >= (capacity * 0.5):
        # Reciprocal altruism: match the majority intent
        if k >= (n - 1) / 2:
            return 'C'
        else:
            return 'D'
            
    # Default state for middling stock levels
    return 'C' if k >= (n - 1) / 2 else 'D'
```

### Altruistic Alignment
This strategy prioritizes the longevity of the resource pool. It assumes that altruism is conditional on the stability of the system; it refuses to deplete the resource for free riders (triggering punishment) but avoids "suicidal altruism" in the final round if the resource is already nearing exhaustion. By attempting to keep the stock near $capacity/2$, it maximizes the total payoff potential for all participants over the long term.
'''

description_BENEVOLENT_1 = '''
The strategy, Tit-for-Tat with Forgiving Resilience, operates on the principle of conditionally sustained cooperation to maximize the common good while insulating against exploitation.

### Core Decision Logic
1.  **First Round:** Play **Cooperate (C)**.
2.  **Subsequent Rounds:** Observe the total number of players who chose **Defect (D)** in the previous round ($D_{prev}$).
    *   If $D_{prev} = 0$: Play **Cooperate (C)**.
    *   If $D_{prev} > 0$: Play **Defect (D)** with a probability $p = D_{prev}/n$. If the random check results in C, play **Cooperate (C)**; otherwise, play **Defect (D)**.
3.  **Last Round:** Play **Defect (D)** regardless of history.

### Adaptive Forgiveness Mechanism
To maintain long-term sustainability despite stochastic or accidental defections, the strategy employs a decay function on past retaliation. If $D_{prev} > 0$, instead of defaulting to pure retaliation, the strategy tracks a "Defection Debt" ($Debt$) counter:
*   Initial $Debt = 0$.
*   If $D_{prev} > 0$, increment $Debt$ by $1$.
*   If $D_{prev} = 0$, decrement $Debt$ by $0.5$ (clamped at $0$).
*   Before deciding the move for round $t$, calculate the "Retaliation Threshold" ($T$):
    *   $T = Debt / (n \times \text{remaining\_rounds})$.
*   If random value $rand(0, 1) < T$, play **Defect (D)**; otherwise, play **Cooperate (C)**.

### Edge Case Handling
*   **Low Stock Warning:** If the current stock $S$ falls below $capacity / n$, the strategy shifts to a "Recovery Mode" regardless of previous history. In Recovery Mode, the strategy forces **Cooperate (C)** for the next three rounds (or until the end of the game) to allow the common pool to regenerate, overriding the retaliation logic.
*   **Final Rounds:** In the final 2 rounds, the "Defection Debt" is ignored to prioritize immediate payoff, but cooperation is maintained if the stock is healthy ($S > capacity / 2$). If the stock is critically low ($S < capacity / 4$), the strategy plays **Cooperate (C)** to ensure there is *any* payoff to be shared, avoiding the zero-sum collapse of total depletion.

### Pseudocode Representation
```python
def decide_action(stock, history, round_number, total_rounds, n, capacity):
    # Check for Recovery Mode
    if stock < (capacity / n):
        return C
    
    # Check for End Game
    if round_number == total_rounds:
        return D
        
    # Standard Decision
    prev_defectors = history.last_round_defectors
    if prev_defectors == 0:
        return C
    else:
        # Probability of retaliation scales with severity of defection
        if random() < (prev_defectors / n):
            return D
        else:
            return C
```
'''

description_BENEVOLENT_2 = '''
**Strategy Description: Benevolent Tit-for-Tat with Stock Sensitivity (BTT-SS)**

This strategy adopts a Conditional Cooperation approach, prioritizing sustainability and mutual benefit. It transitions between Cooperative (C) and Defective (D) modes based on a moving threshold of collective behavior and the remaining stock level, with a specific "forgiveness" mechanism.

### Decision Logic

In each round $t$, define the history as $H_t$, containing the number of cooperators in each previous round $c_1, c_2, ..., c_{t-1}$.

1.  **Initialization (Round 1):**
    Always play **C**. Establish a baseline for cooperation.

2.  **State Assessment:**
    Define the "Safe Stock Threshold" as $S_{safe} = 0.5 \times \text{capacity}$.
    *   If $S < S_{safe}$: Enter **Defensive Mode**. In this mode, prioritize survival. If the current stock is critically low (defined as $< 0.1 \times \text{capacity}$), prioritize self-preservation via **D** to extract remaining value before depletion, regardless of past history. If stock is low but not critical, mimic the average behavior of the group from the previous round (e.g., if $> n/2$ played C, play C; otherwise play D).
    *   If $S \geq S_{safe}$: Enter **Cooperative Mode**.

3.  **Adaptive Enforcement (Cooperative Mode):**
    In Cooperative Mode, the strategy employs a modified Tit-for-Tat approach.
    *   Calculate the average cooperation rate from the previous round: $A_{t-1} = c_{t-1} / n$.
    *   If $A_{t-1} \geq 0.5$: Play **C**.
    *   If $A_{t-1} < 0.5$: Play **D** for the current round (punishment).
    *   **Forgiveness:** If the strategy played **D** in round $t-1$ due to poor opponent behavior, but the opponents return to cooperation ($A_{t-1} \geq 0.5$), switch back to **C** immediately in round $t$.

4.  **Terminal Phase (Last $k$ rounds):**
    As $t$ approaches $r$, the incentive to defect increases.
    *   If $t > r - 3$ (last 3 rounds): Shift to **Tit-for-Tat strictly**. Play **C** if and only if $\geq n-1$ opponents played **C** in the previous round. If stock is high ($> 0.8 \times \text{capacity}$), remain in Cooperative Mode regardless of round count.

### Pseudocode

```python
def decide_action(round, stock, history, n, capacity):
    # Terminal phase check
    if round > (r - 3) and stock < (0.8 * capacity):
        if history.last_round_cooperators >= (n - 1):
            return "C"
        else:
            return "D"

    # Critical stock check
    if stock < (0.1 * capacity):
        return "D"
    
    # Defensive/Low stock check
    if stock < (0.5 * capacity):
        if history.last_round_cooperators >= (n / 2):
            return "C"
        else:
            return "D"

    # Cooperative mode (Main strategy)
    if round == 1:
        return "C"
    
    # Tit-for-Tat with threshold
    if history.last_round_cooperators >= (n / 2):
        return "C"
    else:
        return "D"
```

### Edge Case Handling

*   **Stock Collapse:** If the stock falls to 0, the game is effectively over; the strategy yields no reward. By prioritizing **D** when stock $< 0.1 \times \text{capacity}$, the strategy avoids being the "sucker" in the final moments of a collapsing system.
*   **Initial Defectors:** If opponents defect in round 1, the strategy plays **D** in round 2. This signals that cooperation is conditional and serves to minimize losses against non-cooperative agents.
*   **Fluctuating Cooperation:** If the group toggles between C and D, the strategy oscillates, effectively forcing the system toward the highest sustainable equilibrium that the opponents are willing to support.
'''

description_BENEVOLENT_3 = '''
Define the strategy as "Sustainability-Conditional Reciprocity" (SCR). The objective is to maintain the stock at the capacity level ($S = capacity$) while responding to aggregate defection.

Let $k_t$ be the number of players who cooperated in round $t$, and $m_t$ be the number of players who defected ($m_t = n - k_t$).

**Decision Rules:**

1.  **First Round ($t=1$):**
    Always play **Cooperate (C)**.

2.  **Subsequent Rounds ($t > 1$):**
    *   **If $S_t > 0$ and $k_{t-1} = n$:** Play **Cooperate (C)**. This maintains the cycle of optimal stock replenishment.
    *   **If $k_{t-1} < n$ (Opponents defected):** Calculate the "Required Defection Level" ($L$) to punish defectors or incentivize return to cooperation:
        *   If $S_t \geq \text{threshold}$, play **Cooperate (C)** to keep the pool alive.
        *   If $S_t < \text{threshold}$, play **Defect (D)** if the defecting players are depleting the resource faster than it can recover.
        *   Specifically, if the previous round's total consumption $T_{t-1} > \frac{S_{t-1}}{2}$, play **Defect (D)** for one round to secure a share before the stock hits zero. Otherwise, play **Cooperate (C)**.

3.  **Last Round ($t = r$):**
    *   If $S_r$ is sufficient to support a final payoff without extinction (i.e., $S_r \geq 0$), play **Defect (D)**. Since no future stock matters after $r$, individual payoff maximization is the benevolent choice for the final round.

**Pseudocode:**

```python
def decide_action(t, r, n, S, last_round_k):
    # Rule for final round
    if t == r:
        return D
    
    # Rule for first round
    if t == 1:
        return C
    
    # Rule for subsequent rounds
    if last_round_k == n:
        return C
    else:
        # Calculate last round consumption
        # Cooperators consumed (last_round_k * S_prev / 2n)
        # Defectors consumed ((n - last_round_k) * S_prev / n)
        # Check if last round stock was depleted severely
        if S_prev > 0 and (total_consumption_last_round > (S_prev / 2)):
            return D
        else:
            return C
```

**Edge Case Handling:**

*   **Stock near zero ($S \approx 0$):** If the stock level is so low that cooperation ($C$) yields negligible return, but defection ($D$) yields a slightly higher marginal return, play **Defect (D)** to maximize the final remaining value before the stock effectively dies.
*   **Threshold Recovery:** If the stock $S_t$ drops below $10\%$ of capacity, play **Cooperate (C)** exclusively for the next $3$ rounds, regardless of opponent behavior, to attempt to regenerate the pool. If the stock does not recover, revert to **Defect (D)** in the subsequent round to minimize total loss.
*   **Anonymous Defector Identification:** Because you observe only aggregate $k$, treat the group as a single entity. Reciprocity is applied to the population average: if the population average cooperation rate drops below the threshold required for sustainable stock growth (growth rate $\geq$ consumption rate), switch to **Defect (D)** for exactly one round to offset the disadvantageous payoff, then return to **Cooperate (C)** to signal willingness to restore the resource.
'''

description_BENEVOLENT_4 = '''
The strategy follows a conditional, tit-for-tat inspired approach designed to maintain the common pool at its carrying capacity while penalizing defectors proportionally. The core objective is to maximize the aggregate long-term yield for all participants.

### Strategy Specification

Define $c_t$ as the number of cooperators observed in round $t-1$, and $S_t$ as the current stock at the start of round $t$.

**Round 1:**
Always play **C**. Establish a cooperative baseline.

**Rounds 2 to $r-1$:**
Assess the behavior of the collective from the previous round. Calculate the "cooperation threshold" to determine if the group is sustainably managing the resource.

1.  **Calculate Sustainability:** Estimate if the current stock $S_t$ supports full cooperation. If $S_t < \text{capacity} \times 0.25$, the stock is critical.
2.  **Determine Action:**
    *   If $c_{t-1} = n$ (all players cooperated): Play **C**.
    *   If $c_{t-1} < n$ (defection detected):
        *   If $S_t \ge \text{capacity} \times 0.5$: Play **D** for the current round to offset the "sucker's payoff" and signal the requirement for mutual cooperation, then revert to **C** in $t+1$.
        *   If $S_t < \text{capacity} \times 0.5$: Play **C**. Prioritize stock regeneration over punishment to prevent population collapse.

**Final Round ($r$):**
Always play **D**. Since there are no future rounds to incentivize or punish, there is no strategic benefit to conserving the resource. Maximize individual payoff.

### Pseudocode Logic

```python
def decide_action(round_num, total_rounds, n, capacity, current_stock, prev_round_cooperators):
    # End-game condition
    if round_num == total_rounds:
        return 'D'

    # Initial round
    if round_num == 1:
        return 'C'

    # Tit-for-tat with regeneration priority
    if prev_round_cooperators == n:
        return 'C'
    else:
        # If stock is healthy, punish defectors
        if current_stock >= (capacity * 0.5):
            return 'D'
        # If stock is critically low, prioritize regeneration regardless of past defection
        else:
            return 'C'
```

### Benevolence Principles
*   **Sustainability Bias:** The strategy prioritizes the common pool stock level ($S$) over individual gain whenever $S$ falls below half of the carrying capacity. It sacrifices personal score to ensure the pool does not collapse to zero.
*   **Reciprocity:** It punishes defectors only when the resource is abundant enough to withstand the resulting dip. This discourages "free-riding" without endangering the collective future of all players.
*   **Termination Awareness:** It recognizes the finite nature of the game by switching to "D" only in the final round, ensuring that all cooperation occurs while it is physically possible to benefit from the resulting growth.
'''

description_SELFISH_1 = '''
The strategy employs a "Trigger-Tit-for-Tat" mechanism that aims to sustain the common pool near its optimal growth point (Stock = 50% capacity) to maximize long-term consumption, while aggressively defecting if the pool is exhausted or if opponents act exploitatively.

### Decision Rules
Let $S_t$ be the stock at the start of round $t$, $k$ be the number of cooperators observed in round $t-1$, and $R_{rem}$ be the number of rounds remaining.

**Round 1:**
Cooperate (C).

**Subsequent Rounds ($t > 1$):**
1.  **Exploitation Check:** If the stock $S_t$ falls below the "critical threshold" of $S_{min} = 0.25 \times \text{capacity}$, defect (D) immediately. The resource is failing; minimize losses.
2.  **Reputation Check:** If the observed number of cooperators $k$ in the previous round is strictly less than $n-1$, defect (D). This punishes any defection by others.
3.  **Terminal Phase:** If $R_{rem} < 3$ (last two rounds), defect (D) regardless of the stock state to capture remaining value before the game terminates.
4.  **Steady State:** If $S_t \ge 0.25 \times \text{capacity}$, $k = n-1$ (all others cooperated), and $R_{rem} \ge 3$, cooperate (C).

### Pseudocode Logic
```python
def get_action(round_number, total_rounds, current_stock, prev_round_cooperators, n):
    rounds_remaining = total_rounds - round_number + 1
    
    # Terminal phase: greed is optimal
    if rounds_remaining < 3:
        return 'D'
    
    # Resource safety check
    if current_stock < (0.25 * capacity):
        return 'D'
        
    # Tit-for-tat enforcement: punish if anyone else defected
    if round_number > 1:
        if prev_round_cooperators < (n - 1):
            return 'D'
            
    # Default state for sustainable growth
    return 'C'
```

### Edge Case Handling
*   **Initial Round:** Always cooperates to establish the cooperative equilibrium.
*   **Resource Depletion:** If the stock drops below 25% of capacity, the strategy switches to permanent defection, abandoning cooperation because the growth function cannot recover the stock sufficiently to justify sustained cooperative consumption.
*   **Opponent Defection:** The strategy requires unanimous cooperation from all other $n-1$ players. If even one player deviates, the strategy immediately switches to defection to prevent exploitation and to protect the remaining stock from being depleted by others without reciprocal benefit.
*   **Last Round:** Always defects to ensure capture of the maximum possible share of the remaining resource, as there is no future incentive to maintain stock levels.
'''

description_SELFISH_2 = '''
### Decision Rule
The strategy follows a conditional cooperation framework designed to maximize long-term resource extraction by incentivizing sustainable play while exploiting defection only when necessary to protect personal yield.

**Algorithm:**
1. **Initial Round (t=1):** Play **Cooperate (C)**.
2. **Subsequent Rounds (t > 1):**
   *   Define $C_{observed}$ as the count of opponents who cooperated in the previous round.
   *   Define $Threshold = n - 1 - k$, where $k$ is a tolerance parameter (set $k=1$ for standard play; $k=0$ for aggressive enforcement).
   *   **If** $S_t > \epsilon$ (where $\epsilon$ is a minimal viability buffer, typically $0.1 \times \text{capacity}$):
       *   **If** $C_{observed} \geq Threshold$: Play **Cooperate (C)**.
       *   **If** $C_{observed} < Threshold$: Play **Defect (D)**.
   *   **If** $S_t \leq \epsilon$: Play **Defect (D)** (End-game/exhaustion mode).

**Last Round (t = r):**
Regardless of history, always play **Defect (D)**. Since there is no future round to reap the benefits of sustained growth, maximizing current extraction is the optimal terminal move.

### Logic & Edge Cases
*   **Buffer Management:** The stock dynamics function shows that if the stock drops significantly below 50% of capacity, growth slows dramatically. The $\epsilon$ buffer ensures the strategy switches to extraction mode before the resource becomes entirely unviable, preventing "starvation" scenarios where cooperation yields zero.
*   **Tolerance Parameter ($k$):** This parameter accounts for noise or miscoordination. By setting $k=1$, the strategy forgives a single defector per round, maintaining the sustainable growth loop even if one opponent attempts a minor deviation. If the number of defectors exceeds the tolerance threshold, the strategy immediately switches to Defect (D) to capture a larger share of the remaining pool before it is fully depleted by others.
*   **Punishment/Reward:** The decision to revert to Defect (D) serves as a deterrent. Because the aggregate observation limits targetted retaliation, this strategy treats the "cooperation pool" as a binary state: if the collective is cooperating sufficiently, continue; if the collective is predatory, maximize personal share before the stock collapses.
*   **Terminal Defection:** The strategy acknowledges the finite horizon $r$. In the final round $r$, the incentive to preserve stock for $t+1$ is zero. Therefore, the strategy overrides all history and plays **Defect (D)** to maximize total game payoff.
'''

description_SELFISH_3 = '''
### Strategy Specification: Adaptive Sustenance-Defection (ASD)

**Core Principle:**
The strategy maintains the common pool at or above the capacity level $K/2$ to maximize future yield, while defecting ($D$) exclusively when the stock $S_t$ is sufficient to prevent immediate collapse, or when the game enters the terminal phase where future sustainability is irrelevant.

**Algorithm:**

1.  **Definitions:**
    *   $N_c$: Number of cooperators observed in the previous round.
    *   $N_d$: Number of defectors observed in the previous round ($n - N_c$).
    *   $S_t$: Current stock level at round $t$.
    *   $S_{crit}$: The threshold stock level required to sustain the population. Set $S_{crit} = \text{capacity} / 2$.

2.  **Round 1:**
    *   Play $C$ (Cooperate). This establishes cooperative intent and preserves initial capital.

3.  **Rounds $2$ through $r-1$:**
    *   **Check Sustainability:** If $S_t < S_{crit}$, play $C$. (This is a survival imperative; defecting here accelerates the exhaustion of the pool.)
    *   **Evaluate Opponent Behavior:**
        *   If $N_d = 0$ (all cooperated in previous round): Play $D$ (Defect). This exploits the collective cooperation to maximize immediate gain while $S_t \ge S_{crit}$.
        *   If $N_d > 0$: Play $D$. (This is a "tit-for-tat-adjacent" response: if others are exploiting the resource, you must exploit it as well to capture your share of the value before the stock declines.)
    *   *Correction Rule:* If the observed total consumption in the previous round resulted in a stock decrease of $> 40\%$ of current $S_{t-1}$, revert to $C$ for the next round, regardless of $N_d$, to stabilize the pool.

4.  **Round $r$ (Terminal Round):**
    *   Play $D$ (Defect).
    *   Rationale: There is no future round to benefit from sustainable stock levels. Extract maximum value from the remaining pool.

**Pseudocode:**

```python
def choose_action(round, total_rounds, current_stock, prev_cooperators):
    # Terminal round: extract max value
    if round == total_rounds:
        return 'D'
    
    # Initial round: establish cooperation
    if round == 1:
        return 'C'
    
    # Survival threshold: if stock is dangerously low, prioritize sustainability
    if current_stock < (capacity / 2):
        return 'C'
    
    # Correction mechanism: if stock plummeted last round, force cooperation
    if (stock_delta_last_round > (0.4 * stock_previous)):
        return 'C'
    
    # Default behavior: exploitation
    # If the environment allows it, take the larger share
    return 'D'
```
'''

description_SELFISH_4 = '''
This strategy, labeled "Adaptive Threshold Monitoring," functions as a conditional cooperator with a ruthless endgame pivot. It operates on the principle that cooperation is only instrumentally valuable when the stock level is sufficient to sustain future high yields, and defection is optimal when the resource is threatened or the game is concluding.

**State Variables:**
*   $k$: The number of players who cooperated in the previous round.
*   $S_t$: The stock level at the start of round $t$.
*   $r$: Total rounds.
*   $t$: Current round index.

**Decision Rules:**

1.  **Initialization ($t=1$):**
    Always play **C (Cooperate)**. This establishes a baseline of cooperation and assesses the aggregate behavior of the pool.

2.  **Conditional Strategy ($1 < t < r$):**
    Calculate the sustainability threshold $T = 0.5 \times \text{capacity}$.
    *   If $S_t < T$: Defect (**D**). The resource is over-depleted, and future yields are at risk. Prioritize immediate consumption before total collapse.
    *   If $S_t \ge T$:
        *   If $k \ge \lceil n/2 \rceil$: Cooperate (**C**). The pool is sustaining itself; contributing promotes long-term stock growth.
        *   If $k < \lceil n/2 \rceil$: Defect (**D**). If the majority is depleting the resource, playing C is effectively subsidizing the defectors' gains. Switch to D to maximize share before the stock depletes.

3.  **Endgame Pivot ($t = r$):**
    Always play **D (Defect)**. Because there is no future round to benefit from current stock conservation, the dominant strategy is to extract the maximum available share of the current $S_r$.

**Pseudocode Implementation:**

```python
def choose_action(round_index, total_rounds, current_stock, capacity, n, cooperators_prev_round):
    # Rule 3: Endgame
    if round_index == total_rounds:
        return 'D'

    # Rule 1: Initial Round
    if round_index == 1:
        return 'C'

    # Rule 2: Adaptive Phase
    sustainability_threshold = 0.5 * capacity
    
    if current_stock < sustainability_threshold:
        return 'D'
    
    # Check if majority cooperates
    if cooperators_prev_round >= (n / 2):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_1 = '''
The strategy employs a conditional cooperation approach with a "tit-for-tat" variant adapted for continuous state and aggregate observation. The core objective is to maintain the stock level near the point of maximum sustainable yield ($capacity/2$) while retaliating against defection.

### Core Decision Rule

In any round $t$ where $t < r$:

1.  **Calculate Equilibrium Cooperation Threshold ($k$):** Determine how many other players must cooperate to keep the stock stable. Since the growth function is $G(S_{rem}) = 2 S_{rem} (1 - S_{rem}/capacity)$, the stock remains constant if consumption equals $G(S_{rem})$.
2.  **Observe History:** If $t=1$, cooperate. If $t > 1$, assess the aggregate behavior of opponents in $t-1$. Let $C_{prev}$ be the number of cooperators observed in the previous round.
3.  **Strategy logic:**
    *   If $t=1$, play **Cooperate**.
    *   If $t > 1$:
        *   If the previous round's stock $S_{t-1}$ is below a critical survival threshold (defined as $< 0.1 \times capacity$), play **Defect** to extract remaining value before depletion.
        *   Otherwise, play **Cooperate** if and only if the observed number of cooperators in the previous round was at least $n-1$ (i.e., universal or near-universal cooperation occurred).
        *   If the number of cooperators in the previous round was less than $n-1$, play **Defect**.

### Handling the Final Round

In the final round $t = r$:

1.  Regardless of previous history or current stock level, play **Defect**.
2.  This maximizes short-term utility when future stock sustainability no longer yields a return on investment.

### Pseudocode Representation

```python
def get_action(round_number, total_rounds, current_stock, observed_cooperators_prev_round, n):
    # Terminal round: maximize immediate payoff
    if round_number == total_rounds:
        return 'D'
    
    # First round: initiate cooperative equilibrium
    if round_number == 1:
        return 'C'
    
    # Survival check: if stock is near collapse, salvage
    if current_stock < (0.1 * capacity):
        return 'D'
        
    # Tit-for-tat logic: require near-unanimity to sustain long-term stock
    # Threshold for retaliation is set to n-1 to be robust against 
    # single-agent noise or isolated defection.
    if observed_cooperators_prev_round >= (n - 1):
        return 'C'
    else:
        return 'D'
```

### Edge Cases and Adjustments

*   **Low Stock Recovery:** If the stock drops below the threshold required to sustain the population, the strategy pivots to Defect ($D$) to minimize opportunity cost, accepting the collapse of the pool.
*   **Threshold Calibration:** The threshold for cooperation is set at $n-1$. This creates a "forgiving" tit-for-tat mechanism that ignores a single defector (assuming potential noise) but punishes widespread defection strictly.
*   **Capacity Constraints:** Because the growth function is quadratic, if $S_{current}$ is very high (near $capacity$), playing $C$ is efficient. If $S_{current}$ is low, the incentive to switch to $D$ increases as the marginal value of future stock decreases. This is implicitly handled by the survival threshold logic.
'''

description_SELFINTERESTED_2 = '''
The strategy employs a conditional "Tit-for-Tat" variant based on the observed aggregate cooperation rate of opponents in the previous round, calibrated to preserve stock.

### Decision Rules

For each round $t \in \{1, \dots, r\}$:

1.  **First Round ($t=1$):** Cooperate ($C$). The goal is to establish a high-stock equilibrium.

2.  **Intermediate Rounds ($1 < t < r$):**
    Calculate the effective cooperation rate of opponents from the previous round ($t-1$):
    *   Let $k$ be the number of opponents who cooperated in round $t-1$.
    *   If $k \ge (n-1)$, Cooperate ($C$).
    *   If $k < (n-1)$, Defect ($D$).

    *Exception:* If the current stock $S_t$ is below the threshold $S_{crit} = \text{capacity} / 2$, you must Defect ($D$) regardless of past behavior to maximize immediate extraction before the pool collapses.

3.  **Final Round ($t=r$):** Defect ($D$). Since there is no future to protect, maximize consumption of the remaining stock.

### Pseudocode Representation

```python
def decide_action(round_number, total_rounds, current_stock, prev_round_cooperators, n, capacity):
    # Final round: extract maximum
    if round_number == total_rounds:
        return 'D'
    
    # First round: build trust
    if round_number == 1:
        return 'C'
    
    # Check for critical stock depletion: prioritize extraction if pool is dying
    if current_stock < (capacity / 2.0):
        return 'D'
        
    # Reciprocal cooperation:
    # If all opponents cooperated last round, reciprocate.
    # Otherwise, punish/extract because others are depleting the pool.
    if prev_round_cooperators == (n - 1):
        return 'C'
    else:
        return 'D'
```

### Strategic Edge Cases
*   **Rapid Depletion:** If the stock drops below the sustainability threshold ($S < \text{capacity}/2$), the strategy switches to pure extraction. Because the growth function $2 \times S_{rem} \times (1 - S_{rem}/\text{capacity})$ peaks at $S_{rem} = \text{capacity}/2$, allowing the stock to fall below this point significantly reduces future potential, necessitating immediate Defection to salvage utility.
*   **Robustness to Noise/Heterogeneity:** The requirement for perfect cooperation ($k = n-1$) to maintain $C$ ensures that the strategy is not exploited by defectors. If a single opponent defects, the strategy immediately switches to $D$ in the subsequent round to minimize the relative disadvantage, returning to $C$ only if that opponent ceases defection.
'''

description_SELFINTERESTED_3 = '''
### Strategy: Trigger-Based Sustainable Harvest (TSH)

The strategy utilizes a "Tit-for-Tat" variant adjusted for the renewable resource dynamics of the game, focusing on maintaining the common pool stock level at or near `capacity` to maximize long-term yield.

**Decision Rules:**

1.  **Initialization (Round 1):** Always play **C**.
2.  **General Rounds (Round 2 to r-1):**
    *   Observe the number of defectors in the previous round ($D_{prev}$).
    *   If $D_{prev} = 0$: Play **C**.
    *   If $D_{prev} > 0$:
        *   Calculate the "Stability Threshold": If $S_{current} < (\text{capacity} \times 0.5)$, the stock is critically low. Defect to extract remaining value before depletion.
        *   If $S_{current} \geq (\text{capacity} \times 0.5)$: Respond to defectors with a "punishment" phase lasting $D_{prev}$ rounds. During punishment, play **D**. If no defectors appear during the punishment phase, revert to **C**.
3.  **Terminal Phase (Final Round $r$):**
    *   Regardless of previous cooperation, play **D** to capture the maximum possible share of the remaining stock before the game terminates.

**Edge Cases & Contingencies:**

*   **Critically Low Stock ($S < \text{threshold}$):** If, despite best efforts, the stock level drops below $0.25 \times \text{capacity}$ at the start of any round $t < r$, prioritize defecting for the remainder of the game to ensure immediate payoff realization, as the resource is unlikely to recover sufficiently to sustain future cooperation.
*   **Opponent Heterogeneity:** If the number of defectors remains constant across multiple rounds (suggesting unconditional defectors), switch to **D** permanently to minimize the exploitation of the strategy's cooperative stance.
*   **Growth Buffer:** If $S_{current} > 0.9 \times \text{capacity}$, play **C** even if one opponent defected in the previous round, treating the defect as a manageable variance rather than a threat to sustainability.

**Pseudocode:**

```python
def decide_action(round_num, S, history):
    if round_num == r:
        return 'D'
    
    if round_num == 1:
        return 'C'
    
    prev_defectors = history.last_round_defectors
    
    # Check for critical depletion
    if S < (capacity * 0.25):
        return 'D'
        
    # React to history
    if prev_defectors == 0:
        return 'C'
    else:
        # If stock is high enough, punish defectors
        if S >= (capacity * 0.5):
            return 'D' # Punishment phase
        else:
            return 'D' # Resource collapsing
```
'''

description_SELFINTERESTED_4 = '''
### Strategy: Sustainable Conditional Reciprocity

The strategy is a modified "Tit-for-Tat" that incorporates a threshold-based sustainability check. It aims to maintain the pool at or near `capacity` to ensure long-term returns while punishing defection to deter depletion.

#### Decision Rules
Define $k_t$ as the number of other players (out of $n-1$) who chose Cooperation in round $t-1$.

1.  **First Round ($t=1$):**
    *   Play **Cooperate (C)**.

2.  **Sustainability Threshold:**
    *   If the current `stock` is less than or equal to $0.25 \times \text{capacity}$, play **Defect (D)**. (When the pool is near collapse, immediate extraction is rational as sustainability is no longer viable).

3.  **Conditional Reciprocity (Rounds $t > 1$):**
    *   If `stock` $> 0.25 \times \text{capacity}$:
        *   Calculate the **Cooperation Ratio**: $CR = \frac{k_{t-1}}{n-1}$.
        *   If $CR \geq 0.75$: Play **Cooperate (C)**. (Majority cooperation is sustained).
        *   If $0.25 < CR < 0.75$: Play **Defect (D)**. (Unstable environment; protect individual payoff against partial defection).
        *   If $CR \leq 0.25$: Play **Defect (D)**. (Widespread defection detected; harvest remaining value).

4.  **Last Round ($t=r$):**
    *   Play **Defect (D)**. (With no future interactions, the incentive to preserve stock vanishes).

#### Pseudocode Representation
```python
def get_action(round, total_rounds, stock, capacity, n, k_prev):
    # End-game scenario
    if round == total_rounds:
        return 'D'

    # Collapse imminent or pool depleted
    if stock <= (0.25 * capacity):
        return 'D'

    # First round
    if round == 1:
        return 'C'

    # Cooperation Ratio calculation
    # k_prev is the number of cooperators observed in round t-1
    cooperation_ratio = k_prev / (n - 1)

    # Threshold-based response
    if cooperation_ratio >= 0.75:
        return 'C'
    else:
        return 'D'
```

#### Edge Case Handling
*   **Low Initial Stock (Early Round):** If the initial `stock` is unexpectedly below $0.25 \times \text{capacity}$ (due to rule variations), the strategy defaults to `D` immediately to maximize remaining value.
*   **Rapid Depletion:** If the stock falls below the $25\%$ threshold mid-game, the strategy switches permanently to `D` for all subsequent rounds, assuming the common pool is no longer capable of regenerating to a sustainable level.
*   **Aggressive Defection:** If $CR < 0.75$, the strategy assumes the population is not cooperating sufficiently to sustain the `capacity` target, and therefore switches to `D` to prevent the player from being the sole subsidizer of the pool.
'''

description_OPPORTUNISTIC_1 = '''
**Strategy: Threshold-Based Reciprocal Exploitation (TBRE)**

This strategy operates on a "Tit-for-Tat with a Greedy Twist" mechanism, monitoring the average behavior of opponents to determine whether to sustain the resource or deplete it for immediate gain.

### Definitions
*   **Target Cooperation Threshold ($T$):** Define $T = 0.5$ (50% cooperation rate required to maintain the pool).
*   **Defection Sensitivity ($S$):** The number of rounds to look back, set $S = \min(3, r)$.
*   **Cooperation Rate ($CR_t$):** The fraction of opponents who played Cooperate (C) in round $t$.

### Decision Rules

1.  **Initial Phase (Round 1):**
    Always play **Cooperate (C)** to establish a cooperative environment and test the pool's sustainability.

2.  **Middle Phase (Round 2 to $r-1$):**
    Calculate the moving average cooperation rate ($\overline{CR}$) of opponents over the last $S$ rounds.
    *   If current stock $S_t < (\text{capacity} \times 0.25)$:
        Play **Defect (D)**. The pool is collapsing; extract remaining value before depletion.
    *   Else if $\overline{CR} \ge T$:
        Play **Cooperate (C)** to maintain growth.
    *   Else if $\overline{CR} < T$:
        Play **Defect (D)**. If opponents are not contributing enough to keep the pool sustainable, switch to extraction to maximize immediate payoff.

3.  **Final Phase (Round $r$):**
    Always play **Defect (D)**. There is no future round to benefit from sustainable stock, so extract maximum utility.

### Pseudocode

```python
def decide_action(round_number, total_rounds, current_stock, capacity, history):
    # Rule 1: Terminal Round
    if round_number == total_rounds:
        return 'D'

    # Rule 2: Initial Round
    if round_number == 1:
        return 'C'

    # Rule 3: Calculate Opponent Behavior
    S = min(3, round_number - 1)
    recent_history = history[-(S):]
    avg_cooperation = sum(recent_history) / (len(recent_history) * (n - 1))

    # Rule 4: Opportunistic Thresholding
    # Collapse Imminent
    if current_stock < (capacity * 0.25):
        return 'D'
    
    # Conditional Cooperation
    if avg_cooperation >= 0.5:
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling
*   **Stock Collapse:** If the stock falls below 25% of capacity, the strategy assumes the resource is effectively non-renewable for the remaining horizon and switches to permanent defection, regardless of opponent behavior.
*   **Low $n$:** If $n=2$, the sensitivity of the cooperation rate is high. If the single opponent defects once, the strategy triggers an immediate switch to defection to avoid being the sole contributor to an empty pool.
*   **High $r$:** The strategy remains robust for long games because it recalibrates the decision based on the rolling average, allowing for "forgiveness" (switching back to C) if opponents return to cooperative behavior after a period of defection.
'''

description_OPPORTUNISTIC_2 = '''
The strategy, "Adaptive Resource Harvesting," functions as a conditional cooperator that modulates its consumption based on the observed stability of the common pool and the estimated cooperativeness of the aggregate opponent population.

### Pseudocode Representation

```
// State variables
let r_remaining = total_rounds
let S = initial_stock
let c_observed_previous = 0 // Number of cooperators in last round

// Decision Logic
function get_action(S, c_observed_previous, r_remaining):
    // 1. Terminal Phase Defection
    if r_remaining == 1:
        return D

    // 2. Resource Exhaustion Check
    // If the stock is below a critical replenishment threshold (e.g., 20% of capacity),
    // force C to prevent collapse.
    if S < (0.2 * capacity):
        return C

    // 3. Adaptive Reciprocity (Tit-for-Tat variant)
    // If we are in the initial round, or if the majority defected in the previous round, 
    // punish the pool to maximize short-term yield.
    // If the majority cooperated (or if S is high), reciprocate cooperation.
    if round == 1:
        return C
    
    // Threshold for cooperation: n-1 players must cooperate for stable sustainability
    // If fewer than n-1 players cooperated, defect to extract value before pool collapse.
    if c_observed_previous >= (n - 1):
        return C
    else:
        return D
```

### Strategy Description

The strategy prioritizes long-term resource sustainability while simultaneously exploiting any downward trends in aggregate cooperation.

**1. First Round Behavior**
Always play **C**. This establishes a baseline for cooperation and preserves the maximum possible stock level for subsequent growth, ensuring the game does not collapse immediately due to initial depletion.

**2. Adaptive Reciprocity**
The core decision mechanism relies on the previous round’s aggregate cooperation count. If the population demonstrates a high degree of restraint (defined as at least $n-1$ players cooperating), the strategy reciprocates with **C**. This maintains the pool near optimal carrying capacity. If the aggregate cooperation falls below this threshold, the strategy switches to **D**. This opportunistic switch captures a larger share of the remaining resource before the predicted collapse occurs.

**3. Resource-Aware Safeguards**
Regardless of historical cooperation levels, if the `stock` drops below 20% of the maximum `capacity`, the strategy overrides the reciprocity rule and plays **C**. This prevents the stock from entering a "death spiral" (near 0), which would negate all future earning potential for the remaining rounds. This safeguard is prioritized over short-term gain when total ruin is imminent.

**4. Terminal Phase Defection**
In the final round ($r=1$), the incentive to preserve the pool for future growth is zero. The strategy automatically plays **D**. Since the game terminates, the negative externalities of consuming the remaining stock are irrelevant. The strategy extracts the maximum possible share of the current `stock` to maximize total payoff.
'''

description_OPPORTUNISTIC_3 = '''
Maintain a cooperative stance as long as the aggregate behavior of opponents permits the stock to remain within a productive threshold, switching to immediate defect if the stock trajectory suggests depletion.

**Decision Rules**

Define the "Safety Threshold" ($T$) as $0.6 \times \text{capacity}$.

*   **Initial Round ($t=1$):** Play C. This initiates cooperation and allows for initial observation of opponent behavior.
*   **Subsequent Rounds ($t > 1$):**
    *   **Monitor Stock:** Observe the stock level ($S_t$) at the start of the round.
    *   **Monitor Cooperation:** Observe the number of defectors ($D_{t-1}$) from the previous round.
    *   **Rule:** 
        *   If $S_t \ge T$ and $D_{t-1} < n/2$: Play C.
        *   If $S_t < T$ or $D_{t-1} \ge n/2$: Play D.

**Endgame Adjustment**

For the final rounds, calculate the "horizon effect." If $t > (r - 3)$:
*   If the total accumulated stock is declining (i.e., $S_t < S_{t-1}$), prioritize extraction. Switch to D regardless of the Safety Threshold to maximize final payoffs before the game terminates.
*   If the stock is stable or growing ($S_t \ge S_{t-1}$), continue with the standard Decision Rules.

**Edge Cases**

*   **Stock Collapse ($S \approx 0$):** If the current stock is below $0.1 \times \text{capacity}$, play D in all subsequent rounds. The resource is effectively exhausted, and any residual value must be extracted immediately.
*   **Observation Ambiguity:** If the history of opponent actions is mixed (fluctuating between cooperation and defection), prioritize the $S_t < T$ condition. If the stock is healthy ($> T$), continue to cooperate; if the stock is unhealthy, defect.
*   **Reversion:** If you have switched to D due to high defection ($D_{t-1} \ge n/2$), but the subsequent round reveals the stock has recovered above $T$ and the number of defectors drops below $n/2$, revert to C. This allows for the "tit-for-tat" recovery of the common resource.
'''

description_OPPORTUNISTIC_4 = '''
In each round *t*, let *S* be the current stock, *n* be the number of players, *c_t* be the number of cooperators observed in the previous round, and *r* be the total rounds.

**Decision Rules:**

1.  **Initial Round (t=1):** Always play **Cooperate**.

2.  **Endgame (t=r):** If *S* > 0, always play **Defect**.

3.  **General Rounds (1 < t < r):**
    Calculate the sustainability threshold *K*. Define *K* as the stock level required to maintain current capacity given the observed defection rate. 
    If *S* < (capacity / 2), switch to **Defect** immediately, as the resource is collapsing.
    
    Otherwise, maintain a **Tit-for-Tat with Forgiveness** approach:
    *   Let *D_prev* be the number of defectors in the previous round (where *D_prev = n - c_{t-1} - 1*, accounting for self).
    *   If *D_prev* = 0 (all opponents cooperated), play **Cooperate**.
    *   If *D_prev* > 0:
        *   Calculate the Defection Impact Score: *Impact = (D_prev / (n-1))*.
        *   If *Impact* > 0.5 (majority of opponents defected), play **Defect**.
        *   If *Impact* ≤ 0.5, play **Cooperate** with probability *P = 1 - (2 * Impact)* to incentivize cooperation while limiting exposure.

**Pseudocode:**

```python
def choose_action(round_number, stock, last_round_cooperators, n, r, capacity):
    # Rule 1: Endgame
    if round_number == r:
        return 'D'
    
    # Rule 2: Start
    if round_number == 1:
        return 'C'
    
    # Rule 3: Collapse detection
    if stock < (capacity / 2):
        return 'D'
    
    # Rule 4: Adaptive Response
    opponents_defecting = (n - 1) - (last_round_cooperators - 1 if last_move == 'C' else last_round_cooperators)
    impact = opponents_defecting / (n - 1)
    
    if impact > 0.5:
        return 'D'
    elif impact == 0:
        return 'C'
    else:
        # Probability based punishment
        if random() < (1 - (2 * impact)):
            return 'C'
        else:
            return 'D'
```

**Edge Cases:**
*   **Total Collapse (S = 0):** If stock is 0, play **Defect** (as payoff is 0 regardless, this minimizes computation).
*   **Low n (n=2):** If *n=2*, the impact calculation simplifies to binary states; defect if the opponent defected in the previous round, cooperate if they cooperated.
*   **Stock near capacity:** If *S* is within 10% of *capacity*, prioritize **Cooperate** regardless of history to maximize future round yield, unless the opponent defected in the previous round.
'''

description_INDIVIDUALISTIC_1 = '''
Define a target threshold $T$ for the stock level, where $T$ is calculated as $0.5 \times \text{capacity}$.

In round 1, play **Cooperate (C)** to establish a baseline for cooperation and to allow the pool to remain productive.

For all subsequent rounds $t \in \{2, \dots, r\}$, determine the action based on the state of the system and the observed behavior of opponents in the previous round $t-1$:

1.  **State Check:** If the current stock $S < (\text{capacity} / 4)$, play **Defect (D)**. At critical depletion, individual extraction priority shifts to maximizing immediate return before the pool collapses.
2.  **Growth Check:** If $S \ge T$ and the number of cooperative actions observed in $t-1$ is at least $n/2$, play **Cooperate (C)**. This maintains the cycle of renewal.
3.  **Retaliation/Adaptation:** If the current stock $S$ is below $T$, or if the number of cooperative actions in $t-1$ falls below $n/2$, play **Defect (D)**. This triggers a shift to extraction when the pool is declining or when collective cooperation is insufficient to sustain the resource.

**Edge Cases:**
- **Final Round ($t = r$):** Always play **Defect (D)**. Since there is no future utility to be gained from the stock, immediate extraction is the dominant strategy regardless of the pool's state.
- **Stock Collapse ($S = 0$):** Regardless of the round, if $S = 0$, play **Defect (D)**, as the payoff for both C and D is zero.

**Pseudocode:**

```python
def get_action(round, total_rounds, stock, prev_round_cooperators, n, capacity):
    # Final round dominance
    if round == total_rounds:
        return "D"
    
    # Critical depletion protection
    if stock < (capacity / 4):
        return "D"
        
    # Standard evaluation
    if stock >= (capacity / 2) and prev_round_cooperators >= (n / 2):
        return "C"
    else:
        return "D"
```
'''

description_INDIVIDUALISTIC_2 = '''
Initialize `reputation_score` = 1.0 (representing the estimated likelihood of group cooperation).
Define `target_stock` = capacity / 2 (the point of maximum regeneration).

On each round `t` with current stock `S`:

1. **Last Round Behavior:**
   If `t == r`, play D regardless of history.

2. **First Round Behavior:**
   If `t == 1`, play C.

3. **Subsequent Rounds (t > 1):**
   Calculate the `group_cooperation_rate` ($GR_t$) from the previous round $t-1$:
   $GR_t = (\text{count of C players in round } t-1) / n$

   Update `reputation_score` using a decay factor $\alpha$ (0.1) to weight recent history:
   `reputation_score` = $(1 - \alpha) \cdot \text{reputation\_score} + \alpha \cdot GR_t$

   Execute decision based on `reputation_score` and current stock $S$:

   If `reputation_score` > 0.6 AND $S > (\text{capacity} / n)$:
       Play C.

   Else If $S > (\text{capacity} / 2n)$:
       Play C.

   Else:
       Play D.

**Logic:**
The strategy prioritizes stock sustainability while hedging against imminent collapse. It assumes that if the group cooperation rate is high and the stock is healthy, continued cooperation maximizes long-term yield. If the stock drops below the threshold required to regenerate back to full capacity ($\approx 50\%$ of capacity), it switches to D to maximize immediate return before the pool collapses. In the final round, it ignores cooperation entirely to capture the remaining asset.
'''

description_INDIVIDUALISTIC_3 = '''
The strategy operates as a tit-for-tat variant calibrated to the regenerative capacity of the common pool. It maximizes individual long-term yield by maintaining the stock level $S$ near the carrying capacity $C$, which allows for maximal sustainable extraction rates.

### Core Strategy Rules

1. **Initial State (Round 1):** Play **Cooperate (C)**. This signals a willingness to maintain the resource base.

2. **Monitoring Phase (Rounds 2 to $r-1$):**
   - Calculate the "Sustainable Action Ratio" ($A_s$): Observe the number of defectors ($d$) from the previous round. If $d = 0$, cooperate.
   - If $d > 0$, observe the current stock level ($S_{t-1}$):
     - **If $S_{t-1} \geq 0.5C$:** Play **Cooperate (C)**. The stock is healthy enough to absorb occasional defection without crashing.
     - **If $S_{t-1} < 0.5C$:** Switch to **Defect (D)**. If the stock is critically low, there is a high probability that the pool will be exhausted; extracting the maximum possible amount immediately is the utility-maximizing move to prevent total resource depletion before others do.
   - **Trigger Mechanism:** If at any point in the history the majority of players have defected ($d > n/2$) for two consecutive rounds, switch to **Defect (D)** for all remaining rounds, as the game has entered a race-to-the-bottom state.

3. **Terminal Phase (Round $r$):** Play **Defect (D)**. In the final round, there is no future stock to preserve, removing the incentive to cooperate.

### Pseudocode Representation

```python
def get_action(round, stock, prev_round_defectors, history):
    # Rule 1: Terminal Round
    if round == r:
        return D

    # Rule 2: First Round
    if round == 1:
        return C

    # Rule 3: Trigger for Collapse
    if history_detects_collapse(history): # Two consecutive rounds of majority defection
        return D

    # Rule 4: Adaptive Response
    if prev_round_defectors == 0:
        return C
    
    # Check health of pool
    if stock >= (capacity * 0.5):
        return C
    else:
        return D
```

### Edge Case Handling

- **Low Stock Threshold:** If $S < 0.1C$, immediately ignore cooperation signals and play **Defect (D)** to secure remaining assets before the resource hits 0.
- **Opponent Fluctuation:** If opponents oscillate between C and D, the strategy treats the stock level as the primary signal. If the stock remains above $0.5C$, assume the environment is stable and prioritize cooperation. If it dips below, assume instability and prioritize extraction.
- **End-Game Anticipation:** The strategy does not attempt to "signal" cooperation in the final rounds; it assumes all rational agents will maximize yield when the horizon approaches zero.
'''

description_INDIVIDUALISTIC_4 = '''
**Decision Rules**

The strategy follows a "Conditional Sustainability" approach, prioritizing system stability while adapting to observed aggregate cooperation levels.

1.  **Round 1:** Always play `C` (Cooperate). Establish a baseline for collective behavior.

2.  **Rounds 2 through *r*-1:** Calculate the "Sustainability Ratio" ($\rho$) based on the previous round's outcome.
    *   Let $N_C$ be the number of players who played `C` in the previous round, and $N_D$ be the number of players who played `D`.
    *   Calculate $N_{threshold} = \frac{n}{2}$.
    *   If current $S < \frac{capacity}{4}$ (Critical Depletion), switch to `C` regardless of history to prevent extinction.
    *   Otherwise, if $N_C \geq N_{threshold}$ (or if the last round was all `C`), play `C`.
    *   If $N_C < N_{threshold}$ (Systemic Defection), play `D` to extract share before the pool collapses.

3.  **Final Round (*r*):** Always play `D` (Defect). Since there is no future interaction to penalize, the dominant strategy is to extract the maximum remaining share.

**Pseudocode**

```python
def get_action(round, current_stock, last_round_cooperators, n, r, capacity):
    # Base Case: Last round extraction
    if round == r:
        return 'D'

    # Base Case: Start with cooperation
    if round == 1:
        return 'C'

    # Edge Case: Critical stock protection
    if current_stock < (capacity / 4):
        return 'C'

    # Adaptive Logic
    # If the system is reasonably cooperative, maintain it
    if last_round_cooperators >= (n / 2):
        return 'C'
    
    # If system is collapsing or majority defecting, defect to maximize returns
    else:
        return 'D'
```

**Edge Case Handling**

*   **Stock Depletion:** The rule prioritizing `C` when $S < \frac{capacity}{4}$ overrides all other conditional triggers. This serves as a "rescue mechanism" to keep the game alive, ensuring that even if other players defect, you do not force the stock to zero prematurely, maintaining the possibility of future, higher-payoff rounds.
*   **Initial Instability:** If the first round results in low cooperation ($N_C < \frac{n}{2}$), the strategy immediately switches to `D` in the second round. This protects against being exploited by a predominantly defecting population early in the game.
'''
