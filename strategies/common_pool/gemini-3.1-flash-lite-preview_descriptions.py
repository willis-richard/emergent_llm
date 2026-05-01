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

description_COLLECTIVE_5 = '''
Strategy: Triggered Tit-for-Tat with Sustainability Thresholding

The strategy operates based on two states: "Cooperative" and "Punishing." The agent begins in the Cooperative state.

### State Definitions
1.  **Cooperative State**: The default state. Attempt to maintain the common pool stock at or near `capacity` by cooperating.
2.  **Punishing State**: Triggered when a significant portion of the collective defects. Defect to minimize immediate losses and punish the group, resetting to the Cooperative state if the pool recovers.

### Decision Logic

**Round 1:**
- Play C (Cooperate).

**Round $t$ (where $t > 1$):**
1.  **Check Previous Round Consumption**: Calculate the number of defectors $d_{t-1}$ from the previous round by observing the new stock $S_{t}$ and the previous stock $S_{t-1}$.
    - Total consumption $C_{total} = S_{t-1} - (S_t - \text{Growth}(S_t - \text{Consumption}_{total}))$. Since consumption is observable only via the resulting stock change, deduce $d_{t-1}$ by solving for $x$ in:
      $S_{t-1} - [(\text{cooperators} \times S_{t-1}/2n) + (d_{t-1} \times S_{t-1}/n)] = S_{remaining}$.
    - If $d_{t-1} > n/2$ (a majority of the group is defecting), switch to Punishing state.
    - If the current stock $S_t < \text{capacity} / 2$, switch to Punishing state (the pool is collapsing).

2.  **State Execution**:
    - **If Cooperative State**:
        - If $S_t < \text{capacity} / 4$, play D to extract value before total depletion occurs.
        - Otherwise, play C.
        - If the count of defectors $d_{t-1} > 0$ but $\le n/2$, maintain Cooperative state but set a "warning" flag. If the warning flag persists for 2 consecutive rounds, switch to Punishing state for 1 round.

    - **If Punishing State**:
        - Play D.
        - If $S_t \ge 0.8 \times \text{capacity}$ (the pool has recovered significantly), reset state to Cooperative.
        - If $t = r$ (the final round), play D, regardless of state.

### Pseudocode

```python
state = "COOPERATIVE"
warning_count = 0

def get_action(t, r, S_current, S_previous, n, capacity, d_prev):
    global state, warning_count

    # Last round edge case
    if t == r:
        return "D"

    # State transitions
    if state == "COOPERATIVE":
        if d_prev > n / 2 or S_current < capacity / 2:
            state = "PUNISHING"
        elif d_prev > 0:
            warning_count += 1
            if warning_count >= 2:
                state = "PUNISHING"
        else:
            warning_count = 0
            
    elif state == "PUNISHING":
        if S_current >= 0.8 * capacity:
            state = "COOPERATIVE"
            warning_count = 0

    # Action execution
    if state == "PUNISHING":
        return "D"
    
    # Cooperative state logic
    if S_current < capacity / 4:
        return "D" # Preemptive extraction
    return "C"
```
'''

description_COLLECTIVE_6 = '''
The strategy employs a "Trigger-Modified Tit-for-Tat" mechanism that aims to sustain the pool at the capacity level while punishing defection to prevent resource collapse.

**Core Decision Logic**

1.  **First Round:** Play C.
2.  **Round $t$ (where $1 < t < r$):**
    *   Observe the number of defectors ($k_{def}$) from the previous round ($t-1$).
    *   If $k_{def} = 0$: Play C.
    *   If $k_{def} > 0$: 
        *   Calculate the "Stability Threshold." If current stock $S_{t-1} \ge \frac{capacity}{2}$, play C. 
        *   If current stock $S_{t-1} < \frac{capacity}{2}$, play D for one round to recoup losses, then revert to C in round $t+1$ regardless of the outcome, provided the pool has not hit 0.
3.  **Last Round ($t = r$):** Play D.

**Pseudocode Implementation**

```python
def decide_action(round_number, total_rounds, current_stock, capacity, last_round_defectors):
    # End-game scenario
    if round_number == total_rounds:
        return 'D'
    
    # Opening move
    if round_number == 1:
        return 'C'
    
    # Adaptive logic based on previous behavior and sustainability
    if last_round_defectors == 0:
        return 'C'
    else:
        # If stock is healthy despite past defection, continue cooperating
        if current_stock >= (capacity / 2):
            return 'C'
        # If stock is critically low, defect to recover prior to collapse
        else:
            return 'D'
```

**Edge Case Handling**

*   **Stock Depletion:** If the stock $S_t$ drops below $\frac{capacity}{10n}$ (the threshold of near-extinction), ignore the Tit-for-Tat rule and play D immediately, regardless of the round number, to maximize remaining individual payoff before the pool reaches 0.
*   **Opponent Defection Persistence:** If the number of defectors remains constant for 3 consecutive rounds, switch to a "Grim Trigger" strategy: play D for all subsequent rounds until $r$.
*   **Recovery:** If the pool stock $S$ is at capacity ($S \approx capacity$), always play C, effectively ignoring small numbers of defectors to prioritize long-term system stability over immediate payout maximizing.
'''

description_COLLECTIVE_7 = '''
This strategy, *Conditional Stock-Stabilizing Reciprocity*, seeks to maintain the common pool at approximately 50% of capacity, where regenerative growth is maximized, while punishing defectors who force the stock below sustainable levels.

### Strategy Rules

**Round 1:**
- Play **Cooperate (C)**.

**Round $t$ (where $t > 1$):**

1. **Calculate Target Consumption:** 
   - Define $S_{prev}$ as the stock level at the start of the current round.
   - The goal is to reach a post-consumption stock level of $S_{rem} = 0.5 \times capacity$.
   - Calculate the total allowable consumption for the group: $Total\_Cons\_Target = S_{prev} - (0.5 \times capacity)$.

2. **Evaluate Opponent Behavior (History):**
   - Let $N_{total} = n$.
   - Let $C_{prev}$ be the number of cooperators in the previous round.
   - If the previous round resulted in a significant deviation from the sustainable trajectory (i.e., total consumption significantly exceeded the target or the stock dropped below $0.2 \times capacity$), trigger a "Retaliation Mode."

3. **Decision Logic:**

   *   **Condition A: Equilibrium/Growth Path**
       If the system is currently stable or recovering (stock $> 0.2 \times capacity$ and previous total consumption was sustainable):
       - If $S_{prev} \geq 0.5 \times capacity$: Play **Cooperate (C)**.
       - If $S_{prev} < 0.5 \times capacity$: Play **Cooperate (C)** to allow recovery.

   *   **Condition B: Defection Response (Retaliation Mode)**
       If the stock $S_{prev} < 0.2 \times capacity$ or if the number of defectors in the previous round exceeds 25% of $n$:
       - Play **Defect (D)** if $t < r$ and $S_{prev} > 0$.
       - Play **Cooperate (C)** if $S_{prev} \approx 0$ (attempting to allow growth from the absolute minimum).

   *   **Condition C: Final Round**
       If $t = r$:
       - Play **Defect (D)** regardless of state, as there is no future benefit to conservation.

### Pseudocode Representation

```python
def get_action(n, r, capacity, current_round, stock_history, action_history):
    # Retrieve current state
    S_current = stock_history[-1]
    
    # 1. Final Round Heuristic
    if current_round == r:
        return 'D'

    # 2. Recovery check
    # If the pool is critically low, D is unsustainable, but cooperation 
    # provides negligible immediate returns. We cooperate to foster regeneration.
    if S_current < (0.1 * capacity):
        return 'C'

    # 3. Determine if punishment is required
    # Check if last round's aggregate behavior caused a collapse
    if current_round > 1:
        prev_C = action_history[-1] # Number of cooperators
        # If defectors > threshold, retaliate to discourage exploitation
        if (n - prev_C) > (n * 0.25):
            return 'D'

    # 4. Default: Sustainable Cooperation
    # When the pool is healthy, cooperate to maximize long-term yield
    return 'C'
```

### Edge Case Handling
- **System Collapse ($S \approx 0$):** If the stock drops to 0, growth becomes 0. The strategy switches to **C** to prevent permanent lockout, assuming other rational actors will recognize the need for recovery.
- **Opponent Thresholds:** The strategy utilizes a 25% defection threshold to trigger retaliation. This provides tolerance for small "noise" in the system while strictly penalizing widespread exploitation that threatens the long-term stock viability.
- **First-Mover Advantage:** By starting with **C**, the strategy establishes a baseline of cooperation, maximizing the probability of initiating a collaborative equilibrium rather than a destructive one.
'''

description_COLLECTIVE_8 = '''
Strategy: Trigger-Based Conditional Cooperation with Threshold Recovery

This strategy utilizes a "Tit-for-Tat" variant adjusted for the aggregate observation constraint, prioritizing long-term stock sustainability (the "capacity" state) to maximize aggregate payoffs.

Decision Rules:

1. Initial Round: Play C.
2. Subsequent Rounds (t > 1):
   - Assess the "Cooperation Ratio" ($CR$): $CR = \frac{\text{number of cooperators}}{n}$.
   - Identify the "Sustainability Threshold": If the previous round's outcome resulted in a stock level $S_t \le 0.1 \times \text{capacity}$, enter "Recovery Mode."
   - Action Rule:
     - If in Recovery Mode: Play D if and only if $CR \ge 0.5$ (punishing the pool to force recovery or testing for systemic collapse); otherwise, play C.
     - If not in Recovery Mode: Play C if $CR \ge 0.75$; otherwise, play D.

3. Final Round: Play D.

Edge Cases and Adjustments:

- Stock Depletion: If the stock level $S_t$ drops to 0, play D in all subsequent rounds, as the game state is permanently collapsed and no future returns are possible.
- High Defection Scenarios: If at any point the average Cooperation Ratio over the last 3 rounds drops below 0.3, switch to D for all remaining rounds, assuming the population is non-cooperative.
- Partial Coordination: The strategy uses a threshold of 0.75 for cooperation. This provides a buffer against sporadic defection while maintaining the incentive for others to cooperate. In a pool of $n$ players, if $n-1$ players cooperate, $CR = \frac{n-1}{n}$. If $n \ge 4$, this threshold is met. If $n < 4$, the strategy defaults to a "Grim Trigger" approach where a single defection leads to permanent defection, as small $n$ makes C-based sustainability highly fragile.

```pseudocode
// Strategy Execution Logic per Round
current_stock = S
if stock_is_zero:
    return D
if round == r:
    return D
if round == 1:
    return C

// Analyze previous round performance
previous_CR = observed_cooperators / n

if previous_stock <= (0.1 * capacity):
    // Recovery Mode
    if previous_CR >= 0.5:
        return D
    else:
        return C
else:
    // Normal Mode
    if previous_CR >= 0.75:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_9 = '''
The optimal strategy is a conditional "Tit-for-Tat" variant designed to maintain stock levels at capacity through stable cooperation, while mitigating exploitation risk.

### Decision Rules

1.  **Phase 1: Observation/Initialization (Round 1)**
    *   Always play **C**.

2.  **Phase 2: Reciprocity and Stability (Rounds 2 to r-1)**
    *   Define the "Defection Threshold" ($T$): If the number of defectors in the previous round exceeds 0, switch to **D** for the current round.
    *   If 0 defectors were observed in the previous round, play **C**.
    *   *Constraint Adjustment:* If the current stock ($S$) falls below $0.5 \times \text{capacity}$, play **D** regardless of past behavior to extract remaining value before depletion becomes irreversible.

3.  **Phase 3: Termination (Round r)**
    *   Play **D** regardless of history or stock level. Since there is no future state to incentivize cooperation, the dominant strategy is to maximize immediate extraction.

### Pseudocode Implementation

```python
def decide_action(round_number, total_rounds, last_round_defect_count, current_stock, capacity):
    # Termination condition
    if round_number == total_rounds:
        return 'D'
    
    # Initialization
    if round_number == 1:
        return 'C'
        
    # Crisis management: extract if resource is critically depleted
    if current_stock < (0.5 * capacity):
        return 'D'
        
    # Reciprocal strategy: punish defection
    if last_round_defect_count > 0:
        return 'D'
    
    # Default state: maintain sustainability
    return 'C'
```

### Edge Case Handling

*   **Low Stock Start:** If the stock is significantly below capacity due to previous rounds, the strategy transitions to 'D' to prevent the common pool from bottoming out while waiting for growth that may not occur in time.
*   **Mass Defection:** If the system observes mass defection, the strategy ceases cooperation immediately to avoid subsidizing defectors with a shrinking resource pool.
*   **Partial Recovery:** If stock levels are recovering but opponents still defect, the punishment phase ('D') resets only once the opponent defection count drops to 0, ensuring that the pool is not exhausted by a subset of exploiters.
'''

description_COLLECTIVE_10 = '''
### Decision Rules

The strategy functions as a conditionally cooperative, adaptive algorithm. It balances collective preservation with protection against exploitation.

**1. Initialization (Round 1):**
Always play **C**.

**2. Subsequent Rounds ($t > 1$):**
Let $S_t$ be the current stock at the start of the round and $C_{t-1}$ be the number of players who cooperated in the previous round.

*   **Step 1: Survival Check**
    If $S_t < \frac{\text{capacity}}{n}$, play **C**. 
    *Rationale: The stock is critically low. Regardless of past behavior, defection guarantees systemic collapse, eliminating future payoffs. Cooperation is the only action that keeps the pool viable.*

*   **Step 2: Reciprocity and Norm Enforcement**
    If $S_t \ge \frac{\text{capacity}}{n}$, determine action based on the previous round's aggregate behavior:
    *   If $C_{t-1} \ge \lceil \frac{n}{2} \rceil$ (a simple majority of the group cooperated), play **C**.
    *   If $C_{t-1} < \lceil \frac{n}{2} \rceil$ (the group is dominated by defectors), play **D**.

**3. Last Round ($t = r$):**
Follow the standard rules derived in Step 2. Do not deviate to defection on the final round. Maintaining the cooperative norm on the final round prevents last-minute stock exhaustion, ensuring the highest possible total accumulated payoff for the collective across all rounds, consistent with the objective of maximizing sustainable utility.

### Pseudocode

```python
def get_action(t, n, capacity, current_stock, prev_round_cooperators):
    # Rule: Always cooperate in the first round to signal intent
    if t == 1:
        return 'C'
    
    # Rule: Survival constraint
    # If the stock is critically low, prioritize system continuity
    if current_stock < (capacity / n):
        return 'C'
    
    # Rule: Adaptive Tit-for-Tat
    # Reward majority cooperation, punish majority defection
    if prev_round_cooperators >= (n / 2):
        return 'C'
    else:
        return 'D'
```

### Edge Cases
*   **System Collapse:** If $S_t = 0$, the game effectively ends; the strategy will continue to play **C** in subsequent rounds to facilitate any potential recovery if the growth dynamics allow, though the strategy assumes the round-based nature precludes recovery from zero.
*   **Total Defection:** If the group enters a cycle of total defection, the strategy will defect to protect individual payoff until the Survival Check ($S_t < \text{capacity}/n$) triggers a switch back to cooperation.
*   **Dynamic Group Size:** The threshold for reciprocity ($\lceil \frac{n}{2} \rceil$) is fixed to the majority, ensuring the strategy remains scalable regardless of the exact value of $n$.
'''

description_COLLECTIVE_11 = '''
The strategy follows a conditional cooperation protocol based on a trigger-threshold mechanism, designed to maximize long-term yield while penalizing exploitation.

**Initialization (Round 1):**
Play C (Cooperate).

**General Decision Rule (Round 2 to Round r-1):**
Observe the aggregate behavior of opponents in the previous round. Define $k$ as the number of opponents who played C in the previous round ($0 \le k \le n-1$). 

1.  If $k = n-1$ (perfect cooperation): Play C.
2.  If $k < n-1$:
    *   Calculate the stock $S_{t-1}$ from the previous round and the current stock $S_t$.
    *   If $S_t \ge S_{t-1} \times 0.9$ (stock is recovering or stable despite defection), play C.
    *   If $S_t < S_{t-1} \times 0.9$ (stock is being dangerously depleted), play D for the current round as a corrective signal. Return to C in the next round if the stock level increases or stabilizes.

**Edge Cases:**
*   **The Final Round ($t = r$):** If the stock $S_r \ge 1$, play D to capture the remaining value before the game terminates. If $S_r < 1$ (effectively exhausted), play C to avoid wasting computational resources on negligible gains.
*   **Low Stock Threshold:** If the current stock $S_t < (S_{initial} \times 0.2)$ and total consumption from the previous round indicates non-cooperation ($k < n-1$), play D for one round to maximize utility before total collapse, then revert to C to attempt recovery.
*   **Perfect Stock Saturation:** If $S_t = capacity$, play C regardless of previous history to maintain equilibrium.

**Pseudocode:**
```python
if current_round == last_round:
    return D if stock >= 1 else C

if current_round == 1:
    return C

if stock < (initial_capacity * 0.2) and previous_round_k < (n - 1):
    return D

if previous_round_k == (n - 1) or stock_delta >= -0.1:
    return C
else:
    return D
```
'''

description_COLLECTIVE_12 = '''
The strategy follows a conditional, tit-for-tat variant adapted for a shared resource pool, designed to stabilize stock levels by mirroring the aggregate cooperativeness of the group in the previous round.

**Initialization**
In the first round, play C (Cooperate).

**Observation and Tracking**
Maintain a record of the group’s "Cooperation Level" (CL) from the previous round, calculated as:
$CL = \frac{k}{n-1}$, where $k$ is the number of opponents observed to have played C.

**Decision Rules (Rounds 2 to r-1)**
For any round $t$ where $1 < t < r$:
1. If $CL \geq 0.5$, play C.
2. If $CL < 0.5$, play D (Defect) with probability $p = 1 - CL$. (If the random draw results in Cooperate, play C; otherwise play D).
3. If the stock level $S_t$ drops below a critical threshold $S_{crit} = \frac{capacity}{2n}$, play D to maximize short-term payoff regardless of $CL$, as the resource is approaching exhaustion.

**Edge Cases**
*   **Last Round ($t = r$):** Defect (D) unconditionally to maximize final payoff, as there are no future rounds to influence.
*   **Near-Zero Stock:** If $S_t \leq \epsilon$ (where $\epsilon$ is a minimal threshold relative to $capacity$, e.g., 0.05), play D.
*   **Full Stock Recovery:** If $S_t = capacity$, increase the sensitivity to cooperation; play C if $CL > 0.3$.

**Pseudocode for Decision at round $t$:**
```
if t == r:
    return D
if S_t < (capacity / (2 * n)):
    return D
if CL >= 0.5:
    return C
else:
    // Probabilistic Defection based on group performance
    if random(0, 1) < CL:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_13 = '''
The strategy adopts a conditional cooperation approach aimed at maintaining the stock at the capacity level to ensure long-term sustainability while maximizing immediate yield. The fundamental rule is to cooperate (C) as long as the aggregate behavior of the population is sustainable, switching to a punitive defect (D) state only when necessary to discourage depletion.

**Strategy Logic**

1.  **Initialization:**
    In the first round, play Cooperate (C). Assume a baseline of trust.

2.  **State Assessment:**
    At the start of each subsequent round $t$, calculate the "Sustainability Threshold." A round is considered sustainable if the total consumption does not drive the stock below the level required for maximum replenishment in the next cycle. Specifically, target a stock level $S \approx capacity$.

3.  **Decision Rules:**

    *   **If $t = r$ (Last Round):**
        Defect (D). Since there are no future rounds to sustain, there is no penalty for depleting the resource. Maximize the immediate payoff.

    *   **If $t < r$:**
        Evaluate the previous round’s outcome. Let $c$ be the number of cooperators observed in the previous round $t-1$.
        *   *If $c = n$ (Everyone cooperated):* Cooperate (C). The resource is healthy; maintain the cooperative equilibrium.
        *   *If $c < n$ (Some defected):*
            *   Calculate the stock $S_t$ resulting from the previous round.
            *   If $S_t < (capacity \times 0.5)$: Defect (D) to "punish" the pool and recover immediate payoff before the stock crashes entirely.
            *   If $S_t \geq (capacity \times 0.5)$: Cooperate (C). Continue cooperation despite the defectors, as the stock remains resilient enough to absorb the hit.

4.  **Pseudocode:**

```python
def get_action(round_number, total_rounds, prev_cooperators, current_stock):
    # Rule 1: Terminal round maximizes payoff
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: First round defaults to cooperation
    if round_number == 1:
        return 'C'
    
    # Rule 3: Punish if stock is dangerously low after defections
    # (Threshold set at 50% capacity as a heuristic for risk)
    if prev_cooperators < n:
        if current_stock < (capacity * 0.5):
            return 'D'
        else:
            return 'C'
            
    # Rule 4: Otherwise, maintain cooperation
    return 'C'
```

**Edge Case Handling**
*   **Low Stock Start:** If the stock is below $0.25 \times capacity$ at the start of any round, ignore the previous round's cooperation count and Defect (D) immediately to extract value before the stock hits zero, as the sustainability mechanism is already compromised.
*   **Aggregated Observation:** The strategy relies strictly on the count of cooperators from the previous round. If the information from the previous round indicates that $n$ players cooperated, the system continues to cooperate. Any deviation from $n$ triggers the conditional check on current stock levels to determine if the environment can sustain further cooperation.
'''

description_COLLECTIVE_14 = '''
Initialize `reputation` = 1.0. 
Initialize `punishment_threshold` = 0.5.

**Round 1:**
Play `C` (Cooperate).

**Round 2 to r-1:**
1. Calculate `C_count` (the number of players who played `C` in the previous round).
2. Update `reputation`: `reputation` = `alpha` * `reputation` + `(1 - alpha)` * (`C_count` / `n`), where `alpha` = 0.8 (weighting recent history heavily).
3. If `stock` < (`capacity` / 2):
   Play `D` (Defect).
4. Else if `reputation` < `punishment_threshold`:
   Play `D` (Defect) for one round to signal dissatisfaction and force recovery of the pool, then revert to `C` in the next round.
5. Else:
   Play `C` (Cooperate).

**Round r (Final Round):**
Play `D` (Defect).

**Edge Cases:**
- If `stock` is 0: Play `D` (as recovery is impossible).
- If `n` is large (n > 10) and `reputation` trend is consistently declining (i.e., `reputation` drops by > 0.2 over two consecutive rounds): Play `D` for the remainder of the game, as cooperation has failed to achieve sustainability.
'''

description_COLLECTIVE_15 = '''
Adopt a "Tit-for-Tat with Forgiving Resilience" strategy. The core objective is to maximize sustainability by mirroring the collective behavior of opponents while attempting to restore cooperation if a deviation occurs.

### Strategy Rules

1.  **Initialization:**
    In the first round, always play **C (Cooperate)**.

2.  **Round-by-Round Decision Logic:**
    Let $n$ be the total number of players and $k$ be the number of opponents who cooperated in the previous round.
    *   **Cooperation Threshold:** If $k \ge n - 1$ (unanimous or near-unanimous cooperation), play **C**.
    *   **Defection Threshold:** If $k < n - 1$, switch to **D (Defect)** for one round to prevent exploitation.
    *   **Re-entry (Forgiveness):** If you played **D** in the previous round due to the threshold rule, check if $k \ge n - 1$. If true, return to **C**. If false, continue **D**.

3.  **Special Case: Last Round:**
    In the final round ($r$), ignore the tit-for-tat dynamic. If the current stock level $S > 0$, play **D** to capture maximum remaining value, as future sustainability is no longer a factor.

4.  **State-Dependent Calibration:**
    If the stock level $S$ falls below the critical threshold of $0.2 \times \text{capacity}$, play **C** regardless of opponent history to prevent total resource collapse, unless $S$ is near 0. If $S \approx 0$, play **D** to minimize losses in the final moments of existence.

### Pseudocode Representation

```python
# Constants: n (players), r (rounds), capacity
# Variables: round_number, last_round_cooperators, current_stock

def get_action(round_number, last_round_cooperators, current_stock):
    # End-game scenario
    if round_number == r:
        return 'D' if current_stock > 0 else 'C'
        
    # Crisis management
    if current_stock < (0.2 * capacity) and current_stock > 0:
        return 'C'

    # Tit-for-tat logic
    # Assume i = 1 (our player). 
    # last_round_cooperators = count of opponents who played C.
    # Total participants = n. 
    # Max opponents = n - 1.
    
    if last_round_cooperators >= (n - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_COLLECTIVE_16 = '''
### Strategy: Trigger-Based Sustainable Harvest

The strategy operates on a "Tit-for-Tat with Sustainability Constraints" logic, prioritizing resource regeneration while punishing defectors.

#### Core Logic
The strategy maintains a target state: keep the common pool stock $S$ at the capacity level to maximize long-term yield. The strategy cooperates as long as the aggregate behavior of opponents is sustainable, but switches to defection if the stock falls below a critical threshold or if mass defection occurs.

#### Variables
*   `k`: Number of cooperators observed in the previous round.
*   `t`: Current round number.
*   `r`: Total number of rounds.
*   `S`: Current stock level.
*   `S_threshold`: Critical stock level, defined as `capacity / 2`.
*   `Punishment_Mode`: A boolean flag, initially `False`.

#### Pseudocode Algorithm

```python
if t == 1:
    return Cooperation (C)

# Strategy for rounds 2 to r:
if Punishment_Mode == True:
    # Assess if stock has recovered to sustainable levels
    if S > S_threshold:
        Punishment_Mode = False
        return C
    else:
        return Defection (D)

# Check for mass defection in the previous round
# Mass defection is defined as more than n/2 players choosing D
if (n - k) > (n / 2):
    Punishment_Mode = True
    return D

# Check for stock depletion risk
# If S is critically low, force conservation regardless of previous behavior
if S < (capacity / n):
    return C

# Standard Operation
# If the previous round resulted in stock growth or stability, continue C
# If previous round resulted in net loss, switch to D temporarily to re-balance
if S_previous > S_current:
    return D
else:
    return C
```

#### Edge Cases and Rules
1.  **The Last Round ($t = r$):** In the final round, ignore sustainability constraints. If `Punishment_Mode` is `False`, play Defection (D) to maximize terminal payoff, as there are no future rounds to punish or sustain. If `Punishment_Mode` is `True`, maintain Defection.
2.  **Sudden Stock Collapse:** If $S$ drops below `capacity / (2n)` (a level where even Cooperators consume more than the growth rate can replenish), trigger unconditional Cooperation for one round to attempt stabilization, regardless of opponent history.
3.  **Ambiguity:** If the number of cooperators `k` is unknown (e.g., initial round error), default to Cooperation (C).
4.  **Punishment Decay:** If in `Punishment_Mode`, remain in this state until $S$ rises above `S_threshold`. This ensures the pool is not exhausted by a retaliatory cycle.
'''

description_COLLECTIVE_17 = '''
Initialize state variable `trust_level` = 1.0 (representing the estimated probability of collective cooperation).

**Round 1:**
Play **C**.

**Intermediate Rounds (2 to r-1):**
Let $c_{t-1}$ be the number of cooperators in the previous round.
Let $n$ be the total number of players.

1.  **Update Trust:**
    Adjust `trust_level` using a weighted moving average:
    `trust_level` = (0.7 × `trust_level`) + (0.3 × ($c_{t-1}$ / $n$))

2.  **Decision Rule:**
    If `trust_level` > 0.6:
        Play **C** if current `stock` > (0.4 × `capacity`).
        Play **D** if current `stock` ≤ (0.4 × `capacity`).
    Else:
        Play **D**.

**Final Round (r):**
Play **D**.

**Edge Case Handling:**
- If the `stock` drops to 0, play **D** regardless of `trust_level`.
- If $n$ is large (e.g., $n > 10$), increase the cooperation threshold: if `trust_level` > 0.8, Play **C**.
'''

description_COLLECTIVE_18 = '''
Initialize local history variables:
- `last_stock`: Initial capacity.
- `cooperation_threshold`: 0.75 (minimum fraction of cooperation required from opponents to maintain mutual cooperation).
- `forgiveness_factor`: 1 (rounds of defecting allowed before retaliating; can be adjusted based on total rounds `r`).

Strategy Logic:

1. First Round (t=1):
   - Always play C (Cooperate). This signals willingness to sustain the resource.

2. Subsequent Rounds (t > 1):
   - Calculate `observed_cooperation_rate` = (Total Cooperation Actions by all players - 1) / (n - 1).
   - If `last_stock` < (0.2 * capacity):
     - Defect (D) to secure immediate individual payoff before collapse.
   - If t == `r` (last round):
     - Defect (D) to maximize final round yield, as there is no future incentive for conservation.
   - If `observed_cooperation_rate` >= `cooperation_threshold`:
     - Play C (Cooperate).
   - If `observed_cooperation_rate` < `cooperation_threshold`:
     - Play D (Defect) for the next round to punish non-cooperation or induce lower total consumption.

3. State Tracking:
   - At the end of each round, update `last_stock` to the current `stock` value provided by the game environment.

Pseudocode:

```python
def decide_action(round_number, current_stock, last_round_cooperation_count, n, r, capacity):
    # End-game logic
    if round_number == r:
        return D
    
    # Resource collapse protection
    if current_stock < (0.2 * capacity):
        return D
    
    # First round
    if round_number == 1:
        return C
    
    # Tit-for-Tat / Cooperative tracking
    # Determine if opponents are cooperating
    opponents_cooperated = last_round_cooperation_count - (1 if my_last_action == C else 0)
    cooperation_rate = opponents_cooperated / (n - 1)
    
    if cooperation_rate >= 0.75:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_19 = '''
The strategy utilizes a "Tit-for-Tat with Forgiveness and Stock-Dependent Thresholds" approach, prioritizing collective sustainability when the stock allows, but reverting to defensive consumption when the pool is threatened by others.

**Decision Logic:**

In each round *t*, let *n_C* be the number of observed cooperating opponents in the previous round, and *S* be the current stock.

1.  **Cooperation Trigger (The "Nice" Baseline):**
    If *t* = 1, play **C**.

2.  **Punishment/Reward (The "Adaptive" Core):**
    For *t* > 1, determine the "Cooperation Threshold." Define a threshold *K* based on the stock *S*.
    *   If *S* > (*capacity* / 2), the system is healthy. Play **C** if *n_C* ≥ (*n* - 2). Otherwise, play **D**.
    *   If *S* ≤ (*capacity* / 2), the system is vulnerable. Play **C** only if *n_C* = (*n* - 1). Otherwise, play **D**.

3.  **Last Round Dynamics:**
    For the final round *t* = *r*:
    *   If *S* is greater than or equal to 50% of *capacity*, play **C**.
    *   If *S* is less than 50% of *capacity*, play **D**.

**Edge Cases & Robustness:**

*   **Recovery:** If the stock drops below (10% of *capacity*), the cooperative equilibrium is broken; play **D** for all remaining rounds to extract residual value before the stock reaches zero.
*   **Total Defection:** If *n_C* = 0 in any round, assume the population is non-cooperative. Immediately play **D** for the subsequent two rounds, then attempt a "Probe" by playing **C** once to test if opponents have returned to cooperation.
*   **State-Dependent Calibration:** If at any point *n_C* is consistently lower than the threshold required for sustainability, prioritize immediate payoff (**D**) until the stock recovers or the game ends.

**Pseudocode representation:**

```python
def get_action(round, total_rounds, n, n_coop_prev, stock, capacity):
    # End-game logic
    if round == total_rounds:
        return C if stock >= (0.5 * capacity) else D
    
    # Emergency depletion
    if stock < (0.1 * capacity):
        return D

    # Healthy state logic
    if stock > (0.5 * capacity):
        return C if n_coop_prev >= (n - 2) else D
    
    # Vulnerable state logic
    else:
        return C if n_coop_prev >= (n - 1) else D

    # Default to cooperation in Round 1
    if round == 1:
        return C
```
'''

description_COLLECTIVE_20 = '''
### Strategy: Conditional Tit-for-Tat with Threshold-based Defection

The core objective is to maximize sustainability (keeping stock near `capacity`) while punishing free-riders. The strategy operates on a trigger-based, reactive logic relative to the aggregate behavior observed in the previous round.

**Decision Logic:**

1.  **Initial State (Round 1):**
    Always play **Cooperate (C)**.

2.  **Subsequent Rounds (Round 2 to r):**
    Let `C_obs` be the count of opponents who chose Cooperate in the previous round.
    Let `D_obs = n - 1 - C_obs` be the count of opponents who chose Defect in the previous round.
    Let `S_prev` be the stock level at the start of the previous round.

    *   **Rule A (Full Cooperation):** If `C_obs == n - 1` (everyone cooperated), play **Cooperate (C)**.
    *   **Rule B (Sustainability Threshold):** If the stock level `S` at the start of the current round is below `0.25 * capacity`, play **Defect (D)** regardless of past behavior to extract remaining value before depletion, unless `C_obs == n - 1`.
    *   **Rule C (Punishment):** If `C_obs < n - 1`, observe the total consumption of the previous round. If the total consumption caused the stock `S` to drop below the level required for the growth function to return to `capacity` (specifically, if `S_new < 0.5 * capacity`), calculate the "Defection Index." If the index indicates that your cooperation was exploited (i.e., `D_obs > 0`), switch to **Defect (D)** for `floor(D_obs / (n/2))` rounds.
    *   **Rule D (Forgiveness):** If you are currently in a punishment phase but `C_obs == n - 1` for two consecutive rounds, immediately revert to **Cooperate (C)**.

3.  **Last Round (Round r):**
    Regardless of history, play **Defect (D)**. Since there is no future stock to preserve, the sustainability incentive is nullified, and the dominant strategy is to maximize immediate payoff.

**Pseudocode implementation:**

```python
punishment_counter = 0

def get_action(round, n, capacity, current_stock, history):
    if round == r:
        return 'D'
    
    if round == 1:
        return 'C'

    # Retrieve data from previous round
    C_obs = history[-1].opponents_cooperated
    D_obs = (n - 1) - C_obs
    
    # Check if currently punishing
    if punishment_counter > 0:
        if C_obs == (n - 1):
            for i in range(1, 3): # Check last 2 rounds
                if history[-i].opponents_cooperated < (n - 1):
                    return 'PUNISH_PHASE' # Continue punishment
            punishment_counter = 0 # Forgiveness triggered
            return 'C'
        else:
            punishment_counter -= 1
            return 'D'

    # Logic to initiate punishment
    if C_obs < (n - 1):
        # Calculate if stock is unsustainable due to others
        if current_stock < (0.5 * capacity):
            punishment_counter = max(1, int(D_obs / (n / 2)))
            return 'D'
            
    # Default to cooperation if stock is healthy and no punishment warranted
    return 'C'
```
'''

description_COLLECTIVE_21 = '''
**Strategy: Tit-for-Tat Adjusted Stock Thresholding**

This strategy relies on a trigger-based conditional cooperation model designed to maintain the common pool stock near the sustainable capacity (capacity) while punishing defectors.

### Decision Rules

Define `cooperation_threshold` as the minimum fraction of the previous round's players that must have cooperated to justify continued cooperation. This threshold is dynamically calculated as:
`threshold = (1 - (current_stock / capacity))`
*   If `current_stock` is near `capacity`, the `threshold` approaches 0 (allowing for higher forgiveness).
*   If `current_stock` is low, the `threshold` approaches 1 (demanding near-universal cooperation to restore the pool).

**Round 1:**
Always play **C (Cooperate)**. This establishes a baseline for cooperation.

**Rounds 2 to r-1:**
Let $N_c$ be the number of cooperators observed in the previous round (including yourself, if you played C).
1.  **Calculate Observed Cooperation:** Let `observed_cooperation_rate = (N_c - 1) / (n - 1)` if you played C, or `N_c / (n - 1)` if you played D.
2.  **Evaluate Strategy:**
    *   If `observed_cooperation_rate >= threshold` AND `stock >= (capacity / n)`: Play **C**.
    *   If `observed_cooperation_rate < threshold` OR `stock < (capacity / n)`: Play **D** for one round to minimize resource depletion while the pool is unstable, then revert to step 1 in the next round.

**Last Round (Round r):**
Always play **D (Defect)**. Because there is no future utility to be gained from maintaining the stock after the final round, individual payoff maximization dictates defection, assuming a finite game horizon.

### Edge Case Handling

1.  **Stock Collapse:** If `stock` falls below `capacity / (2n)` (a critical depletion state), play **D** exclusively for two consecutive rounds regardless of opponent history. This forces the stock to either replenish via growth dynamics or provides the maximum possible payoff before the stock hits zero. After two rounds, attempt to reset to **C**.
2.  **Sudden Defection Spike:** If the observed `cooperation_rate` drops by more than 50% compared to the previous round, switch to **D** for one round immediately, regardless of the `threshold`, to discourage "freerider" behavior.
3.  **Low Stock, High Cooperation:** If `stock` is low but `observed_cooperation_rate` is 100%, continue to play **C** to prioritize group sustainability over immediate gain, provided the `stock` is not at zero. If `stock` is zero, play **D** (as the payoff for C is zero).
'''

description_COLLECTIVE_22 = '''
1. Initialization:
   - Begin Round 1 by playing C.
   - Maintain a "Reputation" score $R$ for the collective, initialized to $0$.

2. Strategy Execution (Round $t$):
   - For all rounds $1 \le t < r$:
     - Determine the number of cooperating opponents from the previous round $t-1$, denoted as $C_{t-1}$.
     - Update the Reputation score $R$: $R \leftarrow R + \frac{C_{t-1}}{n-1} - \text{threshold}$, where the threshold is set to $0.5$.
     - If $S_t \le 0.1 \times \text{capacity}$: Defect (D) to ensure short-term survival.
     - Else, calculate the expected sustainability coefficient $\sigma = \frac{S_{rem}}{S_{expected}}$, where $S_{rem}$ is the stock remaining after the proposed round of cooperation, and $S_{expected}$ is the replenishment goal (target of $S_{t+1} \approx S_t$).
     - If $R < -2$: Defect (D) for the current round to punish the collective until $R$ recovers.
     - Else: Cooperate (C).

3. Terminal Phase (Round $r$):
   - If $t = r$:
     - If $S_r \ge 0.5 \times \text{capacity}$: Defect (D).
     - Else: Cooperate (C).

4. Edge Cases:
   - If $n=2$, the reputation logic simplifies such that any defection by the opponent ($C_{t-1} = 0$) results in an immediate reputation drop, triggering immediate retaliation (D) in round $t+1$, followed by a return to C in round $t+2$ to test for renewed cooperation.
   - If the stock $S_t$ drops below $0.05 \times \text{capacity}$, the strategy overrides all other conditions and plays D until the stock recovers above $0.2 \times \text{capacity}$.
'''

description_COLLECTIVE_23 = '''
The strategy employs a conditional "Tit-for-Tat with Forgiveness" approach, optimized for the maintenance of the common pool at capacity.

### Decision Rule Logic
The strategy maintains a target state where the aggregate consumption remains sustainable (i.e., total consumption $\leq S$).

1.  **Initial Round:** Play **Cooperate (C)**. 
    *   Rationale: This establishes a signal of cooperative intent and preserves the maximum stock for future growth.

2.  **Subsequent Rounds ($t > 1$):**
    *   Calculate the **Sustainability Index ($\sigma$)** based on the previous round ($t-1$):
        *   Let $D_{t-1}$ be the number of observed defectors in the previous round.
        *   The strategy observes the previous round's outcome ($S_{t-1}$ and $D_{t-1}$).
    *   **If the stock is critically low ($S_{t} < \epsilon$ where $\epsilon$ is a threshold of 0.2 $\times$ capacity):**
        *   Play **Cooperate (C)** regardless of previous history.
        *   *Rationale:* In a near-collapsed state, defection accelerates extinction; cooperation is the only mechanism to allow recovery.
    *   **If the stock is healthy ($S_{t} \geq \epsilon$):**
        *   Play **Cooperate (C)** if $D_{t-1} < \alpha \times n$ (where $\alpha$ is a tolerance threshold, recommended $\alpha = 0.5$).
        *   Play **Defect (D)** if $D_{t-1} \geq \alpha \times n$.
        *   *Rationale:* This punishes mass defection to prevent exploitation, while maintaining cooperation if the pool of defectors is in the minority.

3.  **Last Round ($t = r$):**
    *   Play **Defect (D)**.
    *   *Rationale:* There is no future round to incentivize cooperation. Maximizing payoff in the final state is the rational dominant strategy once the horizon terminates.

### Edge Case Handling
*   **Mass Defection:** If the system enters a state where $S_t \approx 0$ due to aggregate behavior in $t-1$, the strategy prioritizes recovery via **Cooperate (C)** for a period of 2 rounds, regardless of opponent actions. If the stock does not recover after 2 rounds, it switches to **Defect (D)**, as the resource is effectively exhausted and the game value is negligible.
*   **Recovery Period:** If the strategy previously defected due to high $D_{t-1}$, it will return to **Cooperate (C)** in the next round if $S_t$ has stabilized or increased, acting as an automatic forgiveness mechanism to re-establish the sustainable equilibrium.

### Pseudocode
```python
def decide_action(round, stock, prev_defectors, n):
    if round == r:
        return D
    
    # Recovery logic
    if stock < (0.2 * capacity):
        return C
    
    # Conditional cooperation based on tolerance
    tolerance = 0.5 * n
    if prev_defectors <= tolerance:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_24 = '''
The strategy employs a conditional cooperation mechanism based on a tit-for-tat variant that accounts for the continuous state dynamics of the common pool. The core objective is to maintain the stock level at exactly capacity (S = capacity), which maximizes long-term sustainable extraction.

**Initialization and State Tracking:**
Maintain a memory of the previous round's results: the stock level ($S_{t-1}$) and the number of cooperators ($C_{t-1}$). Define the target stock level as $S_{target} = \text{capacity}$.

**Decision Rules:**

1.  **First Round ($t=1$):**
    Always play **Cooperate (C)**.

2.  **Subsequent Rounds ($t > 1$):**
    Evaluate the stock level relative to the capacity.
    
    *   **Condition A (System Health):** If the stock $S_{t-1} \approx \text{capacity}$ (allowing for minor floating-point fluctuations), play **Cooperate (C)**.
    *   **Condition B (Depletion Response):** If the stock $S_{t-1} < \text{capacity}$, determine the cooperation rate of the opponents in the previous round. If the number of cooperators $C_{t-1} \ge \lfloor n/2 \rfloor$, play **Cooperate (C)** to attempt to rebuild the stock. If $C_{t-1} < \lfloor n/2 \rfloor$, play **Defect (D)** to capture remaining value before the resource collapses.
    *   **Condition C (Terminal Round):** In the final round ($t = r$), play **Defect (D)** regardless of current stock or past behavior, as there is no future state to sustain.

**Pseudocode Implementation:**

```python
def choose_action(round, total_rounds, n, capacity, stock_prev, cooperators_prev):
    # Rule 3: Last round defection
    if round == total_rounds:
        return 'D'
    
    # Rule 1: First round cooperation
    if round == 1:
        return 'C'
    
    # Rule 2: Dynamic state assessment
    # Define threshold for "near capacity" (e.g., 95% of capacity)
    if stock_prev >= 0.95 * capacity:
        return 'C'
    else:
        # Stock is depleted; respond to collective behavior
        if cooperators_prev >= (n // 2):
            return 'C'
        else:
            return 'D'
```

**Edge Case Handling:**
*   **Rapid Depletion:** If the stock drops significantly ($S < 0.25 \times \text{capacity}$), switch to **Defect (D)** permanently, as the system is likely unrecoverable within the remaining round limit.
*   **Total Collapse:** If the stock is 0, play **Defect (D)**, as no resource remains to be preserved.
*   **Rounding/Precision:** When comparing $S_{t-1}$ to capacity, utilize an epsilon tolerance ($|S_{t-1} - \text{capacity}| < 1e-6$) to account for floating-point arithmetic variances.
'''

description_COLLECTIVE_25 = '''
The strategy employs a "Trigger-Tit-for-Tat" mechanism based on the observed collective cooperation rate, adjusted by a safety threshold to ensure stock sustainability.

**State Variables:**
- `target_cooperation_rate`: 1.0 (all players cooperating)
- `history`: A record of total cooperation count $C_t$ for all prior rounds.
- `last_round`: $r$

**Decision Logic:**

1. **Initialization (Round 1):**
   - Play **Cooperate (C)**. This signals a willingness to sustain the resource.

2. **Subsequent Rounds (Round 2 to r-1):**
   - Let $C_{prev}$ be the number of players who cooperated in the previous round.
   - If $C_{prev} == n$ (or $C_{prev} == n-1$ assuming one defector is negligible and likely noise), play **C**.
   - If $C_{prev} < n - 1$:
     - Calculate the `stock_growth_factor` = $2 \times (1 - S_{current} / capacity)$.
     - If $S_{current} > (capacity / 2)$ and $C_{prev} \ge (n/2)$, play **C**. 
     - If $S_{current} \le (capacity / 2)$ or $C_{prev} < (n/2)$, play **Defect (D)**. This serves as a defensive punishment against rapid depletion when the resource becomes critical.

3. **Terminal Round (Round r):**
   - Play **Defect (D)** regardless of history. Since there is no future round to preserve, the dominant strategy is to extract the maximum remaining share.

**Edge Cases & Adjustments:**
- **Resource Depletion:** If $S_{current} \approx 0$ (calculated as $S < (capacity / 10n)$), play **D** to extract whatever is left before the stock collapses entirely.
- **Resumption:** If the system is in a "Defect" state (triggered by low $C_{prev}$), monitor $S_{current}$. If $S_{current}$ recovers to $> 0.8 \times capacity$ after a period of non-cooperation, revert to **C** in the following round to test for cooperation again.

**Pseudocode:**

```python
def play(round_num, stock, n, history):
    if round_num == r:
        return D
    
    if round_num == 1:
        return C
    
    prev_cooperators = history[-1]
    
    # Check if stock is critical
    if stock < (capacity / (10 * n)):
        return D
        
    # Standard Tit-for-Tat with sustainability threshold
    if prev_cooperators >= (n - 1):
        return C
    elif prev_cooperators >= (n / 2) and stock > (capacity / 2):
        return C
    else:
        return D
```
'''

description_COLLECTIVE_26 = '''
Play **C** in the first round. In subsequent rounds, determine your action based on the "Defector Fraction" (the proportion of players who played **D** in the previous round).

Define $d_{t-1}$ as the number of players who played **D** in the previous round $t-1$. Calculate the effective cooperation threshold $T$ as follows:

If $r - t < \text{buffer\_rounds}$ (where $\text{buffer\_rounds} = 2$), play **D** regardless of past history to prevent final-round exploitation.

Otherwise, calculate the "Sustainability Index" $S_{index} = (\text{Stock}_t / \text{Capacity})$. Apply the following decision rules:

1. **Reciprocity (Tit-for-Tat variant):**
   If $d_{t-1} = 0$: Play **C**.
   If $d_{t-1} > 0$: Play **D** with probability $p = (d_{t-1} / n)$. If the probability check fails, play **C**.

2. **Stock Preservation Override:**
   If $S_{index} < 0.25$: Play **C** regardless of opponent behavior in the previous round to allow stock recovery.

3. **Defection Trigger:**
   If $d_{t-1} > (n / 2)$: Play **D** for the subsequent two rounds, then revert to Rule 1.

**Pseudocode:**

```python
if (current_round == total_rounds) or (total_rounds - current_round < 2):
    return "D"

if (current_stock / capacity) < 0.25:
    return "C"

if previous_defectors > (n / 2):
    return "D" # Trigger short-term retaliation

if previous_defectors == 0:
    return "C"

# Stochastic Tit-for-Tat
if random_float(0, 1) < (previous_defectors / n):
    return "D"
else:
    return "C"
```
'''

description_COLLECTIVE_27 = '''
Adopt a conditional cooperation strategy governed by a "Tit-for-Tat with Forgiveness and Stock-Awareness" logic.

**Initialization**
In the first round, play C (Cooperate).

**Round Evaluation Logic**
For each round $t > 1$, define the previous round's outcome:
1. Let $K$ be the number of cooperators in the previous round ($t-1$).
2. Let $D_{opp} = (n-1) - K_{opp}$ be the count of defectors observed in the previous round, where $K_{opp}$ is the number of cooperators observed among the $n-1$ other players. (If the strategy observes $K$ total cooperators, $K_{opp} = K-1$ if the self-action was C, or $K$ if the self-action was D).

**Decision Rules**
Play C (Cooperate) if all the following conditions are met:
1. **Reciprocity Trigger:** $K_{opp} \ge (n-1) \times 0.5$ (The majority of the population cooperated in the previous round).
2. **Stock Sustainability:** $S_t > \frac{capacity}{4}$ (The current stock level is sufficient to support cooperation without immediate collapse).
3. **Horizon Constraint:** $t < r$ (Do not cooperate on the final round).

Play D (Defect) if any of the following occur:
1. **Retaliation:** $K_{opp} < (n-1) \times 0.5$ (The population has defected significantly in the previous round).
2. **Collapse Prevention:** $S_t \le \frac{capacity}{4}$ (The stock is critically low; defect to extract remaining value before depletion).
3. **Endgame:** $t = r$ (The final round).

**Forgiveness Mechanism**
If the strategy is currently in a Defect state due to a previous Retaliation trigger, reset to a Cooperate state (attempt to re-establish cooperation) if:
- In the immediate previous round, the observed cooperation rate $K_{opp}$ was $\ge (n-1) \times 0.8$.
- This single-round test allows for re-coupling with the population if a majority suddenly switches back to C.

**Pseudocode for Decision**
```python
def decide_action(n, r, t, stock, prev_opp_cooperators):
    # Endgame
    if t == r:
        return D
    
    # Critical Stock Level
    if stock <= (capacity / 4):
        return D
    
    # First Round
    if t == 1:
        return C
    
    # Reciprocity and Forgiveness
    threshold = (n - 1) * 0.5
    if prev_opp_cooperators >= threshold:
        return C
    else:
        # Check if we should forgive and re-test
        if prev_opp_cooperators >= (n - 1) * 0.8:
            return C
        return D
```
'''

description_COLLECTIVE_28 = '''
Strategy: Conditional Tit-for-Tat with Resilience Thresholds

1.  **State Initialization (Round 1):**
    Always play **C** in the first round to signal cooperativeness and establish the baseline potential for equilibrium.

2.  **Action Logic (Rounds 2 to r-1):**
    Calculate the "Cooperation Ratio" ($CR$) of the previous round, defined as the number of players who played **C** divided by $n$.
    *   If $CR \geq 0.75$: Play **C**. (Maintaining high collective cooperation is the priority).
    *   If $0.5 \leq CR < 0.75$: Play **C** only if the current stock $S \geq \text{capacity} \times 0.5$. Otherwise, play **D**. (This prevents exploitation when the stock is already being depleted by mixed signals).
    *   If $CR < 0.5$: Play **D**. (The majority is defecting; switching to **D** prevents the resource from collapsing while you are the only one conserving).

3.  **End-Game Heuristic (Final Round):**
    Play **D** if the current stock $S$ is below a "collapse threshold" of $\text{capacity} \times 0.25$, as the resource is unlikely to recover significantly post-game. If $S \geq \text{capacity} \times 0.25$, continue following the action logic from Step 2 to maximize the final round payoff without risking total depletion.

4.  **Resilience Override:**
    Regardless of the $CR$ logic, if the current stock $S < \text{capacity} \times 0.1$:
    *   Play **C** if and only if the aggregate cooperation from the previous round was at least $n-1$ (i.e., you were the only defector or everyone cooperated). This forces a "stop-loss" mechanism where you refuse to deplete a near-extinct resource unless almost everyone else is already doing so. Otherwise, play **D** to extract remaining value before potential depletion.

5.  **Summary Logic Pseudocode:**
    ```python
    def decide_action(round, stock, prev_C_count, n, capacity):
        if round == 1:
            return C

        CR = prev_C_count / n

        # Resilience override: Critical stock levels
        if stock < (capacity * 0.1):
            return C if prev_C_count >= (n - 1) else D

        # End-game scenario
        if round == r and stock < (capacity * 0.25):
            return D

        # Standard strategy based on previous collective behavior
        if CR >= 0.75:
            return C
        elif CR >= 0.5:
            return C if stock >= (capacity * 0.5) else D
        else:
            return D
    ```
'''

description_COLLECTIVE_29 = '''
Adopt a "Tit-for-Tat with a sustainable threshold" strategy. The objective is to maintain the stock at the capacity level to maximize long-term payoffs, as the growth function is maximized when the stock is at half capacity (50%), but the replenishment is highest when the stock is high. Since the stock dynamics favor a steady state at capacity, the strategy prioritizes sustained cooperation while punishing deviations.

**Strategy Logic:**

1.  **Initialization (Round 1):** Play **Cooperate (C)**. This signals a willingness to maintain the resource.

2.  **State-Dependent Decision (Rounds 2 to r):**
    Evaluate the stock level $S_t$ and the history of the previous round's cooperation count, $C_{opponents}$.

    *   **The "Defector Punishment" Rule:** If any defectors were observed in the previous round ($C_{opponents} < n-1$), switch to **Defect (D)** for the current round. This serves as an immediate, one-round penalty to discourage opportunistic depletion.
    *   **The "Sustainability Buffer" Rule:** If the current stock $S_t$ is below a critical threshold (defined as $S_t < \text{capacity} / 2$), play **Cooperate (C)** regardless of previous history to allow the resource to recover. 
    *   **Default Behavior:** If no defectors were observed in the previous round and the stock is at or above the threshold ($S_t \ge \text{capacity} / 2$), play **Cooperate (C)**.

3.  **End-Game Heuristic (Last 3 rounds):**
    If the round index $t > r - 3$:
    *   If the current stock $S_t$ is sufficient to support Defecting ($S_t > 0$), calculate whether the cumulative payoff of Defecting for the remaining rounds outweighs the potential loss of stock recovery.
    *   Specifically: If $S_t > \text{capacity} / 4$, switch to **Defect (D)** for the final round to extract remaining value. If $S_t \le \text{capacity} / 4$, maintain **Cooperate (C)** to ensure positive payoffs in the final moments rather than risking a stock of zero.

**Pseudocode:**

```python
def decide_action(round, stock, last_round_cooperators, n):
    # End-game logic
    if round > total_rounds - 3:
        if stock > capacity / 4:
            return D
        else:
            return C

    # Standard play logic
    if round == 1:
        return C
    
    # Check for defection by others in previous round
    # last_round_cooperators includes all players; 
    # my own last action must be subtracted to isolate opponents.
    my_last_action = get_my_last_action()
    opponents_who_cooperated = last_round_cooperators - (1 if my_last_action == C else 0)
    
    if opponents_who_cooperated < (n - 1):
        return D # Punish defection
    
    # If resource is critically low, prioritize replenishment over punishment
    if stock < (capacity / 2):
        return C
    
    return C # Default to cooperation
```
'''

description_COLLECTIVE_30 = '''
Adopt a Tit-for-Tat variant with a threshold-based forgiveness mechanism.

**Core Strategy Logic:**

1.  **Initialization (Round 1):** Play Cooperate (C).
2.  **Observation:** After each round $t$, calculate the cooperation rate of the group. Let $N_C$ be the number of cooperators observed in the previous round.
3.  **State Assessment:** Monitor the `stock`. If the stock level falls below $2n$ (which implies depletion below the sustainable growth equilibrium point), switch to a "Recovery Mode" regardless of opponent history.
4.  **Decision Rules:**
    *   If `stock` < $2n$: Play Defect (D) only if necessary to maximize survival, but ideally play C to allow stock regeneration. In practice, if `stock` < $0.1 \times \text{capacity}$, play D to capture remaining value before collapse; otherwise, play C to assist recovery.
    *   If $t = r$ (Final Round): Play Defect (D).
    *   If $t < r$ and `stock` $\ge 2n$:
        *   If $N_C$ in round $t-1$ was $\ge \lceil n/2 \rceil$: Play Cooperate (C).
        *   If $N_C$ in round $t-1$ was $< \lceil n/2 \rceil$: Play Defect (D) to mitigate loss, with a probability of $0.2$ to play Cooperate (C) to test for opponent cooperation recovery.

**Pseudocode:**

```python
def get_action(round, stock, n, r, history):
    # End-game scenario
    if round == r:
        return 'D'
    
    # Crisis management
    if stock < (2 * n):
        if stock < (0.1 * capacity):
            return 'D'
        else:
            return 'C'
            
    # Tit-for-Tat logic
    if round == 1:
        return 'C'
    
    last_round_cooperators = history.last_round.num_C
    threshold = ceil(n / 2)
    
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        # Probabilistic probe for cooperation restoration
        if random_float() < 0.2:
            return 'C'
        else:
            return 'D'
```

**Edge Cases:**
*   **Rapid Depletion:** If the stock drops to 0, the game terminates effectively; the strategy accepts the 0 payoff.
*   **High Cooperation:** If the population consistently cooperates, the strategy sustains cooperation indefinitely.
*   **Mass Defection:** If the majority defects, the strategy defaults to Defect to capture immediate utility, occasionally "testing the waters" to see if the population shifts back to cooperation.
'''

description_COLLECTIVE_31 = '''
For each round $t \in \{1, \dots, r\}$, the strategy employs a conditional cooperative approach based on the sustainability threshold of the resource.

**Phase 1: Initialization**
In round 1, play C.

**Phase 2: Monitoring and Retaliation (Rounds 2 to $r-1$)**
The strategy tracks the `previous_round_stock` and the number of cooperators observed in the previous round ($C_{obs}$).

1.  **Calculate Sustainability:** Determine the "Safe Consumption Threshold" ($T$). The resource is stable if consumption $\le$ growth. Given stock $S$, the maximum total consumption $K$ that sustains the stock (where new stock = $S$) is found by solving $S = (S - K) + 2(S - K)(1 - (S - K)/capacity)$. To simplify decision-making, cooperate if the stock $S \ge capacity/2$.

2.  **Decision Logic:**
    *   **If $S < capacity \times 0.25$:** Switch to D immediately to maximize remaining individual payoff before the pool collapses.
    *   **If $S \ge capacity \times 0.25$:**
        *   If all players cooperated in the previous round ($C_{obs} = n$), play C.
        *   If any player defected in the previous round ($C_{obs} < n$), play D for one round (tit-for-tat retaliation), then revert to C in the following round, provided the stock is above the critical threshold.

**Phase 3: The Final Round ($r$)**
Regardless of previous cooperation history, play D. This captures the residual value of the resource, as there is no future incentive to maintain sustainability.

**Pseudocode:**

```python
def get_action(round_number, current_stock, prev_cooperators, n, r, capacity):
    # Final round defect
    if round_number == r:
        return 'D'

    # Emergency resource exhaustion: abandon cooperation
    if current_stock < (capacity * 0.25):
        return 'D'

    # First round start
    if round_number == 1:
        return 'C'

    # Conditional cooperation: Tit-for-tat
    if prev_cooperators == n:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Low Stock:** If the stock drops below the critical 25% of capacity, the strategy treats the game as effectively terminated and defects to extract value before total depletion occurs.
*   **Partial Cooperation:** If $0 < C_{obs} < n$, the strategy treats this as a defection event. The retaliation is calibrated to trigger D for exactly one round, returning to C regardless of whether the defectors switch back, provided the stock remains above the critical threshold.
'''

description_COLLECTIVE_32 = '''
The objective is to maintain the stock $S$ at or near the capacity $K$ (where $K = \text{capacity}$) to maximize cumulative payoffs over $r$ rounds, as depletion leads to a collapse of future returns. 

The strategy employs a conditional cooperation protocol based on the "Tit-for-Tat" variant adjusted for group dynamics, utilizing the observed number of cooperators ($c_{obs}$) from the previous round.

### Operational Logic
1.  **Initialization (Round 1):**
    Play **C** (Cooperate). This initiates cooperation and signals a willingness to sustain the resource.

2.  **Round Progression (Rounds 2 to $r-1$):**
    Let $c_{obs}$ be the number of cooperators in the previous round, excluding self.
    *   If $c_{obs} = n - 1$: All players cooperated in the previous round. Play **C**.
    *   If $c_{obs} < n - 1$: The resource is being over-extracted.
        *   Calculate the threshold: If current stock $S < 0.5 \times K$, play **D** (Defect) to protect remaining stock or extract value before total depletion.
        *   If current stock $S \geq 0.5 \times K$, play **C** (Cooperate) to attempt to signal and restore the stock level.

3.  **Terminal Phase (Final Round $r$):**
    Play **D** (Defect). Since there is no future round to reap the benefits of a preserved stock, the dominant strategy shifts to maximizing the immediate payoff.

### Pseudocode Implementation

```python
def decide_action(round_number, total_rounds, n, S, capacity, last_round_cooperators):
    # Terminal phase: Maximize final payoff
    if round_number == total_rounds:
        return 'D'

    # Initial phase: Start with trust
    if round_number == 1:
        return 'C'

    # Adaptive Cooperation phase
    # Count of other players who cooperated last round
    c_obs = last_round_cooperators

    # If the group is fully cooperative, continue cooperating
    if c_obs == n - 1:
        return 'C'
    
    # If the group is over-consuming:
    # If stock is critically low, defect to secure last remnants
    if S < (0.5 * capacity):
        return 'D'
    
    # Otherwise, attempt to recover stock by cooperating
    return 'C'
```

### Edge Case Handling
*   **Stock Collapse:** If $S$ drops to 0, the payoff for both **C** and **D** is 0. If $S$ is near 0, the decision rule defaults to **D** (via the $S < 0.5 \times K$ condition) to extract the remaining minimal value.
*   **Partial Cooperation:** In scenarios where $c_{obs}$ is high but not maximal, the strategy maintains **C** as long as the resource remains above the critical $0.5 \times K$ threshold, prioritizing resource recovery over immediate gain. If the stock falls below this threshold, the strategy pivots to **D** to prevent loss against defectors.
'''

description_PROSOCIAL_5 = '''
Let $k_t$ be the number of cooperators observed in round $t$. Let $n$ be the number of players and $S_t$ be the stock at the start of round $t$.

**Phase 1: Initial Trigger (Round 1)**
Play C.

**Phase 2: Cooperative Maintenance (Rounds 2 through $r-1$)**
Calculate the "Prosocial Compliance Ratio" ($PCR$), representing the average cooperation rate of opponents up to the current round:
$PCR = \frac{\sum_{j=1}^{t-1} (k_j - \delta_{C,j})}{n \times (t-1)}$, where $\delta_{C,j} = 1$ if I played C in round $j$, else 0.

Apply the following conditional logic:
1.  **If $S_t < \frac{capacity}{2n}$**: This indicates critical resource depletion. Defect (D) to maximize immediate utility before the stock potentially collapses to 0.
2.  **If $PCR \ge 0.5$**: Cooperate (C). A majority of the group is sustaining the resource; reciprocate this behavior.
3.  **If $PCR < 0.5$**: Defect (D). The group is exploiting the resource; shift to a defensive stance to prevent the opponent's "tragedy of the commons" from yielding them higher relative payoffs while depleting the resource I help maintain.

**Phase 3: Terminal Phase (Round $r$)**
Regardless of previous history or $PCR$, if $S_r \ge \frac{capacity}{2n}$, cooperate (C) to ensure the final round remains sustainable. If $S_r < \frac{capacity}{2n}$, defect (D).

**Edge Case Adjustments:**
*   **Stock Floor:** If $S_t < \frac{capacity}{4n}$ (near-extinction), play D in all subsequent rounds. The resource is effectively non-renewable at this level, and cooperative maintenance is mathematically futile.
*   **Reset Mechanism:** If the strategy enters a Defect (D) state due to $PCR < 0.5$, check the stock level $S_t$ every round. If $S_t$ recovers to $\ge \frac{capacity}{2}$, revert to Cooperation (C) for one round to test if the opponents have also shifted to a sustainable equilibrium. If $k_t = n$ (all cooperate), permanently return to the Phase 2 Cooperation logic. If $k_t < n$, continue Defecting (D).
'''

description_PROSOCIAL_6 = '''
The strategy employs a "Targeted Sustainability" approach. It attempts to maintain the common pool at the capacity level ($C_{ap}$) by calculating a required collective cooperation rate based on the current stock ($S_t$) and the goal of maximizing long-term yield.

**Decision Logic:**

1.  **Target Calculation:**
    Define the target stock as $S_{target} = C_{ap}$. The goal is to keep $S_{t+1} \approx S_{target}$.

2.  **Required Cooperation Rate:**
    Calculate the total cooperation required to stabilize or restore the pool.
    Let $n$ be the number of players.
    Let $S_t$ be the current stock.
    Total consumption if $k$ players cooperate and $(n-k)$ players defect:
    $Consumption_{total} = k(S_t / 2n) + (n-k)(S_t / n) = (S_t/n) * (k/2 + n - k) = (S_t/n) * (n - k/2)$.
    Remaining stock after consumption $S_{rem} = S_t - (S_t/n)(n - k/2) = S_t(k/2n)$.
    Next stock $S_{t+1} = S_{rem} + 2(S_{rem})(1 - S_{rem}/C_{ap})$.
    To keep $S_{t+1} = S_{target}$, solve for $k$. For $S_{target} = C_{ap}$, we need $S_{rem} = C_{ap}/2$.
    Thus, set $S_t(k/2n) = C_{ap}/2$, implying the target number of cooperators is $k_{target} = \frac{n \cdot C_{ap}}{S_t}$.

3.  **Pseudocode Strategy:**

```python
def get_action(round, total_rounds, n, capacity, current_stock, history):
    # 1. Terminal Round Adjustment
    # In the final round, the incentive to defect is maximized as there is no future.
    # However, to remain prosocial, we cooperate if we are confident that 
    # cooperation is sustainable. If capacity is threatened, play defensively.
    if round == total_rounds:
        if current_stock < (capacity / 2):
            return "D"
        return "C"

    # 2. Calculate target cooperators to maintain capacity
    target_cooperators = (n * capacity) / current_stock
    
    # 3. Strategy Calibration
    # If the pool is healthy (S_t >= capacity * 0.9), cooperate.
    # If the pool is depleting (S_t < capacity * 0.9), trigger tit-for-tat
    # logic based on recent observations.
    
    if current_stock >= (0.9 * capacity):
        return "C"
    
    # 4. Observation-based Tit-for-Tat
    # Look at the previous round (t-1)
    if round > 1:
        prev_cooperators = history[round-1].cooperators_count
        
        # If the pool is low, adjust behavior based on recent group trend.
        # If the group is cooperating enough to restore stock, join them.
        if prev_cooperators >= target_cooperators:
            return "C"
        else:
            return "D"
            
    # 5. First Round Default
    return "C"
```

**Edge Case Handling:**
*   **Initialization (Round 1):** Always cooperate to signal pro-sociality and attempt to maintain the initial state.
*   **Depleted Stock ($S_t \approx 0$):** If the stock is extremely low, the strategy switches to "Defect" to minimize individual loss in the face of inevitable collapse, effectively exiting the resource pool.
*   **Fluctuation:** The threshold $0.9 * capacity$ creates a buffer against slight variances in growth dynamics, preventing over-reaction to small, harmless fluctuations while remaining highly sensitive to significant depletion.
'''

description_PROSOCIAL_7 = '''
Maintain a reputation-based reciprocal strategy that prioritizes long-term stock sustainability by mimicking the observed cooperation levels of the previous round while punishing unilateral defection.

**Decision Logic**

1.  **Round 1:** Play Cooperate (C). Start with the assumption of mutual sustainability.

2.  **Rounds 2 to r-1:**
    Let $c_{t-1}$ be the number of opponents who played Cooperate in the previous round.
    *   If $c_{t-1} = n-1$ (all other players cooperated): Play C.
    *   If $c_{t-1} < n-1$:
        *   Calculate the stock $S_t$ resulting from the previous round. If $S_t \le \frac{1}{4} \cdot \text{capacity}$, play D to secure remaining resources before the pool collapses.
        *   If $S_t > \frac{1}{4} \cdot \text{capacity}$, play C with probability $P_c = \frac{c_{t-1}}{n-1}$ to incentivize cooperation while limiting exposure to exploitation.

3.  **Final Round (Round r):**
    Play Defect (D). Since there are no future rounds to sustain, maximizing the remaining stock yield is the dominant strategy regardless of past behavior.

**Pseudocode**

```python
def decide_action(round, n, capacity, current_stock, history):
    if round == r:
        return D
    
    if round == 1:
        return C
    
    # Analyze previous round
    c_prev = history.last_round.opponent_cooperators
    
    # Determine stock health threshold
    # Collapse is imminent if previous stock was low
    if current_stock <= (0.25 * capacity):
        return D
    
    # Tit-for-tat variant based on opponent population
    if c_prev == (n - 1):
        return C
    else:
        # Probabilistic cooperation based on observed group sentiment
        # or switch to D if cooperation is critically low
        if c_prev > (0.5 * (n - 1)):
            return C
        else:
            return D
```

**Edge Case Handling**

*   **Stock Collapse:** If at any point the `current_stock` falls below the threshold required for significant regeneration (determined as 10% of capacity), immediately switch to D for all remaining rounds, as the common pool is no longer viable for sustainable collective extraction.
*   **Anonymity:** Since identity is unknown, treat the aggregate cooperation count as the sole indicator of group trust. Do not attempt to track specific opponents; only respond to the group-level trend.
'''

description_PROSOCIAL_8 = '''
The strategy utilizes a "Tit-for-Tat with Forgiveness" approach, calibrated to the state of the pool, balancing mutual cooperation with protection against depletion.

**Core Decision Rule:**
In any round $t$, choose $A_t$ based on the observation of the previous round's aggregate behavior and the current stock level $S$.

1. **Initial Round ($t=1$):**
   Always play **C**. Establish a baseline of cooperation.

2. **Subsequent Rounds ($t > 1$):**
   Determine the number of defectors in the previous round, $k_{t-1}$.
   *   If $k_{t-1} = 0$: Play **C**. Reward continued cooperation.
   *   If $k_{t-1} > 0$:
       *   Calculate a "Sustainability Threshold" $S_{crit}$. If $S_t < \text{capacity} \times 0.25$, play **D** to extract value before the stock collapses.
       *   Otherwise, play **C** if and only if the stock $S_t$ is above the "Recovery Buffer" ($S_t \ge 0.5 \times \text{capacity}$).
       *   If $S_t < 0.5 \times \text{capacity}$ and $k_{t-1} > 0$, play **D** to minimize losses in a failing resource environment, effectively "punishing" the collective failure to maintain the stock.

3. **Final Round ($t=r$):**
   Ignore future consequences. If $S_r$ is sufficient to provide a higher payoff via $D$, play **D**. Specifically: if $S_r \times (1/n) > S_r \times (1/2n)$, play **D**. This is always true given the payoff structure ($1/n > 1/2n$), so play **D** in the final round regardless of history.

**Pseudocode:**

```python
def get_action(round, total_rounds, current_stock, prev_round_defectors, capacity):
    # Rule 1: Final round defection
    if round == total_rounds:
        return 'D'

    # Rule 2: Initial round cooperation
    if round == 1:
        return 'C'

    # Rule 3: Responsive strategy
    # If everyone cooperated previously, continue cooperating
    if prev_round_defectors == 0:
        return 'C'
    
    # If the stock is critically low, defect to salvage utility
    if current_stock < (capacity * 0.25):
        return 'D'
    
    # If the stock is below the recovery buffer and others are defecting,
    # protect personal utility by defecting
    if current_stock < (capacity * 0.5):
        return 'D'
        
    # Otherwise, cooperate to encourage long-term sustainability
    return 'C'
```

**Edge Case Handling:**
*   **Rapid Depletion:** If the stock approaches zero, the strategy pivots to $D$ to capture remaining resources before the pool empties, accepting that if the pool is effectively dead, cooperation yields zero utility.
*   **Non-cooperative Environment:** If $k_{t-1} > 0$ persists, the strategy defaults to $D$ if the resource environment is compromised ($S_t < 0.5 \times \text{capacity}$), preventing the strategy from being exploited indefinitely while the resource is being drained by others.
*   **Recovery:** If the resource pool recovers despite previous $D$ actions (due to the growth function), the strategy resets to $C$ as soon as $k_{t-1}$ returns to 0.
'''

description_PROSOCIAL_9 = '''
**Strategy: Target-Stock Triggered Reciprocity**

This strategy maintains the common pool at its maximum sustainable capacity by targeting the steady-state stock $S^* = \text{capacity}/2$, which maximizes renewable growth. It cooperates when the current stock allows for sustainable consumption and retaliates against defection to enforce collective restraint.

### Definitions
*   **Ideal Consumption:** $C_{ideal} = S_{current} / (2n)$.
*   **Defection Consumption:** $D_{current} = S_{current} / n$.
*   **Defection Threshold:** If total consumption exceeds the amount that maintains the steady state, the stock will decline. The strategy monitors the proportion of cooperators $k$ (where $k$ is the number of players who played $C$ in the previous round).

### Decision Rules
1.  **Initialization (Round 1):** Play **Cooperate (C)**.
2.  **Steady-State Maintenance (Rounds 2 to $r-1$):**
    *   Calculate the outcome of the previous round. If the number of cooperators $k \ge n-1$ (allowing at most one defector), play **C**.
    *   If the number of cooperators $k < n-1$, play **Defect (D)** for one round to signal intolerance for over-consumption, then revert to **C** in the subsequent round, provided the stock remains above a critical floor of $0.25 \times \text{capacity}$.
3.  **Last Round ($r$):** Play **Defect (D)**. Since there is no future to protect, the strategic value of preserving the stock reaches zero.

### Edge Case Handling
*   **Stock Collapse:** If $S_{current} < 0.1 \times \text{capacity}$, play **C** regardless of opponent behavior in the previous round. At this level, defecting risks driving the stock to zero, which eliminates all future payoffs, whereas cooperation provides a small, non-zero return and allows for potential recovery.
*   **Recovery Phase:** If the stock is below $0.5 \times \text{capacity}$ but above the critical floor, play **C** until the stock returns to $\ge 0.5 \times \text{capacity}$, regardless of opponent history. This prioritizes the long-term viability of the pool over short-term retaliation.

### Pseudocode
```python
def action(round_num, S, k_prev, n, r, capacity):
    # Base Case: Last Round
    if round_num == r:
        return 'D'
    
    # Base Case: Critical Stock Shortage
    if S < 0.1 * capacity:
        return 'C'
        
    # Recovery Phase: Prioritize sustainability
    if S < 0.5 * capacity:
        return 'C'
        
    # Standard Play: Conditional Reciprocity
    # Cooperate if the group is cooperating (allowing max 1 defector)
    # Otherwise, punish with Defection
    if round_num == 1:
        return 'C'
    elif k_prev >= n - 1:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_10 = '''
The strategy adopts a conditional cooperation model that seeks to maintain the stock at its maximum capacity while punishing defectors proportionally to their observed behavior.

**Strategy Logic:**

1.  **Phase 1: Initial Rounds (The Trust-Building Phase)**
    In the first round, play C (Cooperate). For subsequent rounds, track the observed average cooperation rate of the group. If the total stock S is above 90% of capacity, play C.

2.  **Phase 2: Adaptive Response**
    After the first round, track the history of the aggregate group cooperation. Let $C_{obs}$ be the number of opponents who cooperated in the previous round (out of $n-1$).
    Define a target cooperation threshold $T = n/2$.

    *   If $S$ falls below $capacity/2$, switch to D (Defect) for one round to secure immediate resources, then return to C if the stock recovers.
    *   If $S \geq capacity/2$:
        *   If $C_{obs} \geq (n-1)/2$, play C.
        *   If $C_{obs} < (n-1)/2$, play D.

3.  **Phase 3: The End Game (The Final Round)**
    In the final round $r$, ignore cooperation history. If $S > capacity/2$, play C. If $S \leq capacity/2$, play D.

**Pseudocode:**

```python
# Constants: n, r, capacity, my_history
# Input: current_round (t), current_stock (S), opponents_cooperated (c_obs)

if t == r:
    if S > capacity / 2:
        return C
    else:
        return D

if t == 1:
    return C

# Dynamic adjustment based on resource health
if S < (capacity / 2):
    # Resource is critically low; prioritize survival
    # If we have been burned, we defect, otherwise we cooperate
    if c_obs < (n - 1) / 2:
        return D
    else:
        return C

# Standard steady-state condition
if c_obs >= (n - 1) / 2:
    return C
else:
    return D
```
'''

description_PROSOCIAL_11 = '''
**Strategy: Sustainable Tit-for-Tat with Stock Sensitivity**

This strategy relies on a conditional cooperation rule that adjusts based on the sustainability of the current stock level and the observed behavior of the collective.

**Decision Logic**

For any round $t$ with current stock $S_t$:

1.  **Sustainability Check**: Calculate the "Sustainable Extraction Limit" ($L$). This is the maximum total extraction allowed while maintaining $S_{t+1} \geq S_t$. If $S_t$ is below the threshold required to regenerate back to $S_t$ (or capacity) given the current $n$, prioritize conservation.
    *   If $S_t < \text{capacity} / 2$, you must play **Cooperate (C)** to minimize stock depletion regardless of opponent behavior, as the system is at risk of collapse.

2.  **Collective Behavior Assessment (The Tit-for-Tat Mechanism)**:
    *   In the first round ($t=1$), play **Cooperate (C)**.
    *   For all subsequent rounds ($t > 1$), calculate the cooperation rate of the opponents in the previous round ($t-1$). Let $k_{t-1}$ be the number of players who played **C** in round $t-1$.
    *   Calculate the target cooperation threshold ($T$): $T = n - 1$.
    *   If $k_{t-1} \geq T$, play **Cooperate (C)**.
    *   If $k_{t-1} < T$, play **Defect (D)** with a probability $P = 1 - (k_{t-1}/n)$ to signal a preference for lower extraction while maintaining a slight hedge against exploitation.

3.  **End-Game Adjustment**:
    *   In the final round ($t = r$), ignore the Tit-for-Tat rule. If $S_r > 0$, always play **Defect (D)**. Because there are no future rounds to influence, defecting maximizes the final payoff without impacting future stock levels.

**Pseudocode Representation**

```python
def get_action(round, total_rounds, n, stock, last_round_cooperators):
    # 1. End-game override
    if round == total_rounds:
        return 'D'
    
    # 2. Sustainability override
    # If stock is critically low, enforce conservation
    if stock < (capacity / 2.0):
        return 'C'
    
    # 3. First round start
    if round == 1:
        return 'C'
    
    # 4. Adaptive Tit-for-Tat
    # Cooperate if enough others cooperated, otherwise defect
    if last_round_cooperators >= (n - 1):
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling**
*   **Low Stock**: If the system enters a state where $S_t$ is critically low, the strategy forces cooperation ($C$) regardless of previous history to prevent total stock depletion ($0$), which guarantees $0$ payoff for all future rounds.
*   **Total Defection**: If all opponents defect, the strategy responds by defecting ($D$) in non-critical stock states, but switches immediately back to $C$ if the stock level drops below the sustainability threshold, preventing a "race to the bottom" that kills the pool.
'''

description_PROSOCIAL_12 = '''
### Strategy: Adaptive Tit-for-Tat with Sustainability Buffer

The strategy aims to maintain the common pool at its maximum sustainable capacity by balancing individual consumption with the regeneration rate, while utilizing a conditional response mechanism to punish defection.

#### Core Logic
The strategy relies on a "Target Cooperation Level" (TCL) based on the observation of opponents in the previous round. If opponents are generally cooperating, the strategy cooperates. If opponents are defecting, the strategy defects to protect its share, shifting back to cooperation only after observing signs of restraint from the population.

#### Decision Rules
For any round $t$ where $t < r$:

1.  **Observe**: Identify the number of defectors $k_{t-1}$ from the previous round.
2.  **State Check**: If the current stock $S < (\text{capacity} / 2)$, adopt a "Regeneration Phase." Defect if the number of cooperators from the previous round $C_{t-1} < n/2$, otherwise cooperate. This prioritizes stock recovery.
3.  **Cooperation Rule**: In the first round ($t=1$), always play **Cooperate (C)**.
4.  **Reaction Rule** ($t > 1$):
    *   Let $D_{t-1}$ be the number of players who chose D in the previous round.
    *   If $D_{t-1} > (n/2)$, play **Defect (D)**. This is a punitive response to widespread depletion.
    *   If $D_{t-1} \le (n/2)$, play **Cooperate (C)**. This assumes the population is sufficiently prosocial to sustain the resource.

#### Edge Case Handling
*   **The Final Round ($t=r$)**: Play **Defect (D)**. Since there are no future rounds to incentivize cooperation, the dominant strategy is to capture the remaining stock before the game terminates.
*   **Near-Depletion**: If the current stock $S$ is below a critical threshold (defined as $S < 0.1 \times \text{capacity}$), override all rules and play **Cooperate (C)** regardless of previous history, to prevent the resource from hitting zero and eliminating all future growth potential.
*   **Recovery Reset**: If the strategy is currently in a punitive Defect cycle (triggered by $D_{t-1} > n/2$), revert to **Cooperate (C)** for one round if the stock $S$ has increased by more than 20% compared to the previous round, signaling that the pool is recovering.

#### Pseudocode Representation

```python
def get_action(round_number, total_rounds, n, stock, capacity, opponents_defected_last_round):
    # Rule 1: Always defect in the last round
    if round_number == total_rounds:
        return 'D'

    # Rule 2: Emergency conservation
    if stock < (0.1 * capacity):
        return 'C'

    # Rule 3: Regeneration Phase (if stock is low, be cautious)
    if stock < (0.5 * capacity):
        if opponents_defected_last_round >= (n / 2):
            return 'D'
        else:
            return 'C'

    # Rule 4: Standard Adaptive Response
    if opponents_defected_last_round > (n / 2):
        return 'D'
    else:
        return 'C'
```
'''

description_PROSOCIAL_13 = '''
The strategy, "Proportional Tit-for-Tat with Threshold Sensitivity," operates based on the observed cooperation level of opponents in the previous round to determine the current round's action.

**State Definitions:**
*   $k$: Number of opponents observed to cooperate in the previous round.
*   $n_{opp} = n - 1$: Total number of opponents.
*   $S_{t}$: Current stock level.
*   $capacity$: Maximum stock capacity.

**Initial Round (t=1):**
Always play $C$ (Cooperate).

**Subsequent Rounds (t > 1):**
1.  **Calculate Opponent Cooperation:** Observe $k$, the number of cooperators among the $n-1$ opponents in the previous round.
2.  **Determine Cooperation Threshold ($T$):** Define the required cooperation threshold as $T = \lceil \frac{n_{opp}}{2} \rceil$.
3.  **Apply Logic:**
    *   If $S_{t} < (\frac{capacity}{n})$, play $D$ (Defect) to extract remaining value before exhaustion.
    *   If $S_{t} \geq (\frac{capacity}{n})$:
        *   If $k \geq T$, play $C$.
        *   If $k < T$, play $D$ (Defect) to punish non-cooperation and protect the resource from collapse by discouraging over-extraction.
4.  **Terminal Round (t = r):** If $r > 1$, play $D$ regardless of state to capture remaining potential utility.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, current_stock, capacity, n, opponents_cooperated):
    # Terminal Round
    if round_number == total_rounds:
        return 'D'
        
    # Desperation threshold: If stock is critically low, take share immediately
    if current_stock < (capacity / n):
        return 'D'
    
    # Tit-for-Tat logic
    n_opponents = n - 1
    threshold = ceil(n_opponents / 2)
    
    if opponents_cooperated >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_14 = '''
Define the following variables:
- $k_t$: Number of cooperators observed in round $t$.
- $n$: Total number of players.
- $r$: Total number of rounds.
- $t$: Current round number ($1 \leq t \leq r$).
- $S_t$: Stock at the start of round $t$.
- $\theta$: A sensitivity threshold, set to $0.25$ (25% of $n$).

**Core Strategy Logic**

The strategy follows a "Tit-for-Tat with Forgiveness and Depletion Awareness" approach. It attempts to maintain the stock at the capacity limit by cooperating when others cooperate, while defecting to prevent total collapse or to punish exploitation.

**Decision Rules per Round $t$:**

1.  **Initialization:** In round 1, always play **Cooperate (C)**.

2.  **State Check (Safety Valve):** If $S_t < \text{capacity} \times 0.2$, play **Defect (D)**. This is a survival trigger to extract value before the stock reaches a non-recoverable state, assuming cooperation has failed to sustain the resource.

3.  **Endgame:** If $t = r$, play **Defect (D)**. Since there are no future rounds to influence, the dominant strategy is to maximize immediate payoff regardless of stock replenishment.

4.  **Reciprocity and Tit-for-Tat:** For $1 < t < r$, determine action based on the observation from round $t-1$:
    *   If $k_{t-1} \geq n - \theta$: Play **Cooperate (C)**. The group is largely cooperating.
    *   If $k_{t-1} < n - \theta$: Play **Defect (D)**. The group is over-exploiting; withhold contribution to signal disapproval and reduce the depletion rate of the shared pool.

5.  **Forgiveness/Resumption:** If the strategy played Defect (D) in round $t-1$ due to low $k_{t-2}$, it will test for cooperation in round $t$ by playing **Cooperate (C)** if $S_t \geq \text{capacity} \times 0.5$. Otherwise, remain in **Defect (D)** until the stock recovers or the game ends.

**Pseudocode Implementation:**

```python
def get_action(round, total_rounds, n, stock, capacity, prev_k):
    # Rule 1: Survival check
    if stock < (capacity * 0.2):
        return D
        
    # Rule 2: Final round
    if round == total_rounds:
        return D
        
    # Rule 3: First round
    if round == 1:
        return C
        
    # Rule 4: Tit-for-Tat with threshold
    # If the previous cooperation level was high enough
    if prev_k >= (n - 0.25 * n):
        return C
    
    # Rule 5: Forgiveness / Recovery
    # If we previously defected, check if stock is healthy enough to cooperate again
    if stock >= (capacity * 0.5):
        return C
        
    return D
```
'''

description_PROSOCIAL_15 = '''
Define the target stock level for sustainability at $S^* = \text{capacity} \times 0.5$.

At each round $t \in \{1, \dots, r\}$, execute the following decision logic:

1. **Initialization:**
   In the first round ($t=1$), always choose action **C**.

2. **Trigger-Based Adaptation:**
   In subsequent rounds ($t > 1$), calculate the stock $S_{t-1}$ at the end of the previous round. Define the "Sustainability Condition" as $S_{t-1} \geq S^*$.

   If $t = r$ (the final round), play **D** if $S_{t-1} < S^*$ or if the expected accumulated payoff of defecting exceeds the value of maintaining the resource for future rounds (which is zero). To be strictly prosocial, play **C** unless the history indicates widespread defection. Specifically, play **D** in the final round only if the average cooperation rate of opponents in the previous $t-1$ rounds is less than 0.5. Otherwise, play **C**.

   If $t < r$:
   - **Case A (Stock Recovery):** If $S_{t-1} < S^*$, play **C** to prioritize resource replenishment.
   - **Case B (Mutual Cooperation):** If $S_{t-1} \geq S^*$ and the majority of opponents cooperated in the previous round ($C_{t-1} > n/2$), play **C**.
   - **Case C (Defection Response):** If $S_{t-1} \geq S^*$ but the majority of opponents defected in the previous round ($D_{t-1} \geq n/2$), play **D** for the current round as a penalty to disincentivize exploitative behavior.

3. **Pseudocode representation:**

```python
def choose_action(t, r, n, current_stock, prev_opp_coops):
    target_stock = capacity * 0.5
    
    # Final round logic
    if t == r:
        if prev_opp_coops < (n - 1) / 2:
            return 'D'
        else:
            return 'C'
            
    # Stock-based recovery logic
    if current_stock < target_stock:
        return 'C'
        
    # Tit-for-tat variant for mid-game
    if prev_opp_coops >= (n - 1) / 2:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_16 = '''
The strategy utilizes a "Target-Stock Tit-for-Tat" mechanism, focusing on maintaining the pool at its optimal sustainable capacity while reciprocating the collective cooperation level observed in the previous round.

**Initialization**
In round 1, play C.

**Decision Rules**
For any round $t > 1$, calculate the "Target Stock" ($S^*$) and the "Observed Cooperation Rate" ($O_{t-1}$).
1. Define $S^*$ as the capacity value.
2. Define $O_{t-1}$ as the fraction of players who cooperated in the previous round: $(n - d_{t-1}) / n$, where $d_{t-1}$ is the number of defectors observed in round $t-1$.

Determine the action for round $t$ based on the following logic:

*   **Condition 1 (Recovery):** If the current stock $S_t < (S^* / 2)$, play C regardless of the history to prioritize pool survival.
*   **Condition 2 (Reciprocity):** If $S_t \geq (S^* / 2)$, act according to the observed cooperation from the previous round:
    *   If $O_{t-1} \geq 0.5$, play C.
    *   If $O_{t-1} < 0.5$, play D for one round to buffer the exploitation, then return to C in the next round.
*   **Condition 3 (Final Round):** If $t = r$, ignore all future incentives and play D if the current stock $S_r \geq 0.5 \times \text{capacity}$; otherwise, play C.

**Pseudocode**
```python
if round == 1:
    return C

if current_stock < (capacity / 2):
    return C

if round == r:
    return D if current_stock >= (capacity / 2) else C

# Reciprocity Logic
previous_cooperators = (n - observed_defectors_last_round)
cooperation_rate = previous_cooperators / n

if cooperation_rate >= 0.5:
    return C
else:
    # Check if we were forced to defect last round due to low cooperation
    if last_action == D:
        return C
    else:
        return D
```

**Edge Case Handling**
*   **Low Stock:** If the stock drops below the threshold required for meaningful regeneration ($S < capacity/4$), prioritize C indefinitely until the stock recovers to $capacity/2$, overriding reciprocal defection.
*   **Anonymity:** Since specific opponents cannot be identified, the strategy treats the group as a single aggregate entity. If multiple rounds of low cooperation occur, continue to oscillate between one round of D (to signal intolerance for depletion) and subsequent rounds of C (to signal a return to cooperation), preventing a descent into a total collapse loop.
'''

description_PROSOCIAL_17 = '''
Define the cooperative action as $C$ and the defection action as $D$. Let $S_t$ be the stock at the start of round $t$, $k$ be the number of cooperators observed in round $t-1$, and $n$ be the number of total players.

The strategy follows a conditional cooperation framework modified by a dynamic threshold to ensure long-term sustainability:

1.  **Initialization (Round 1):**
    Always play $C$.

2.  **State Assessment:**
    Define the "Target Stock" as $S^* = capacity / 2$. This is the point of maximum stock growth.
    Define a "Sustainability Buffer" $B = capacity \times 0.2$. If $S_t < B$, the stock is critical.

3.  **Recursive Decision Rule (Rounds $t > 1$):**
    *   **Critical State Recovery:** If $S_t < B$, play $C$ regardless of previous round outcomes to prevent total pool depletion.
    *   **Conditional Reciprocation:** If $S_t \geq B$:
        *   If the number of cooperators in the previous round $k \geq n - 1$, play $C$.
        *   If $k < n - 1$, switch to $D$ to punish the aggregate defection, effectively "tit-for-tat" against the group.
    *   **Recovery Phase:** If the strategy switched to $D$ in the previous round, check $S_t$. If $S_t \geq S^*$ (sufficiently recovered), return to $C$. If $S_t < S^*$, continue $D$ for one additional round or until $S_t$ trends upward, then return to $C$.

4.  **End-Game Heuristic (Rounds $t = r$):**
    Ignore long-term sustainability and maximize current payoff. If the group has historically cooperated ($k \geq n-1$ on average over the last 3 rounds), play $C$. If the group has consistently defected, play $D$.

Pseudocode:

```python
def strategy(S_t, k_prev, t, r, n, capacity):
    # End-game override
    if t == r:
        if avg_cooperation_recent > 0.8:
            return C
        else:
            return D

    # Critical depletion protection
    if S_t < (0.2 * capacity):
        return C

    # Standard reciprocation logic
    if k_prev >= (n - 1):
        return C
    else:
        # Check if recovery is needed
        if S_t < (0.5 * capacity):
            return D # Punish and wait for growth
        else:
            return C
```
'''

description_PROSOCIAL_18 = '''
Maintain the common pool at maximum sustainable yield by employing a conditional cooperation strategy driven by the observed stock level and the recent collective behavior of opponents.

**Strategy Definition:**

1.  **Initialization (Round 1):**
    *   Play **C**.

2.  **Conditional Rule (Rounds $t = 2$ to $r-1$):**
    *   Define the "Prosocial Threshold" $T_t = 0.5$.
    *   Calculate the "Cooperation Rate" $R_{t-1} = \frac{C_{observed}}{n-1}$, where $C_{observed}$ is the number of opponents who played C in the previous round.
    *   If current stock $S_t > \text{threshold\_critical}$ (where $\text{threshold\_critical} = 0.2 \times \text{capacity}$):
        *   If $R_{t-1} \ge T_t$, play **C**.
        *   If $R_{t-1} < T_t$, play **D** (to punish defection and force stock recovery if possible, or extract value before depletion).
    *   If current stock $S_t \le \text{threshold\_critical}$:
        *   Play **D** to extract remaining value, as the resource is approaching collapse.

3.  **Terminal Round ($t = r$):**
    *   Play **D**.

**State-Dependent Calibration:**

*   **Stock Recovery Adjustment:** If $R_{t-1} < T_t$ and the stock has been declining for two consecutive rounds, switch to **D** regardless of the cooperation rate for one round to protect personal payoff before the pool reaches a point of non-recovery, then return to the Conditional Rule.
*   **Edge Case - Resource Recovery:** If $S_t$ drops below $0.1 \times \text{capacity}$ and remains there despite the group behavior, always play **D** for the remainder of the game, as sustainable cooperation is no longer viable.

**Pseudocode Logic:**

```python
def get_action(round, stock, prev_opp_C_count, n, r):
    if round == r:
        return D
    
    # Calculate cooperation rate of opponents
    opp_coop_rate = prev_opp_C_count / (n - 1)
    
    # Critical low stock state
    if stock <= (0.2 * capacity):
        return D
    
    # Tit-for-Tat inspired response
    if opp_coop_rate >= 0.5:
        return C
    else:
        return D
```
'''

description_PROSOCIAL_19 = '''
**Strategy: Prosocial Equilibrium Maintenance (PEM)**

This strategy operates as a conditional cooperator, utilizing a "Trigger-Tit-for-Tat" mechanism that targets the maintenance of the common pool stock at approximately 50% capacity (S/capacity ≈ 0.5), which maximizes sustainable growth while allowing for cooperation.

**Decision Logic**

1.  **Phase 1: Initialization**
    In Round 1, always play **Cooperate (C)**.

2.  **Phase 2: Monitoring and Retaliation**
    In all subsequent rounds (2 ≤ t ≤ r), track the "Defection Index" (DI) of the previous round. The DI represents the number of players who chose to defect.
    - If the number of defectors in round (t-1) was 0, play **Cooperate (C)**.
    - If the number of defectors in round (t-1) was > 0, calculate the "Stock Vitality" (SV = current_stock / capacity).
        - If SV > 0.4, play **Cooperate (C)** with a probability of 0.5, or alternatively, play **Cooperate (C)** if the previous round's total consumption did not lead to a stock collapse (new_stock > 0).
        - If SV ≤ 0.4, play **Defect (D)** until the stock recovers or the final round is reached.

3.  **Phase 3: The End-Game**
    Calculate the remaining rounds ($r - t$).
    - If $r - t < n$ (the final rounds are imminent), switch to **Defect (D)** if the current stock $S$ is below the threshold required to sustain growth (i.e., if $S$ is low enough that cooperation will not yield a meaningful return), otherwise maintain **Cooperate (C)**.

**Pseudocode Implementation**

```python
def get_action(current_round, total_rounds, current_stock, capacity, last_round_defectors):
    # End-game logic
    if (total_rounds - current_round) < 2:
        return 'D' if current_stock < (0.2 * capacity) else 'C'

    # Initial round
    if current_round == 1:
        return 'C'

    # Trigger-Tit-for-Tat logic
    if last_round_defectors == 0:
        return 'C'
    else:
        # Check stock health
        vitality = current_stock / capacity
        if vitality > 0.4:
            # Conditional forgiveness
            return 'C'
        else:
            # Retaliation due to resource scarcity
            return 'D'
```

**Edge Case Handling**

*   **Stock Collapse (S = 0):** If the stock reaches 0, the game is effectively terminated regardless of action. Play **Defect (D)** as the default for the final round.
*   **High Volatility:** If the number of defectors fluctuates frequently, the strategy prioritizes the "Stock Vitality" metric over "Tit-for-Tat" history. If the resource is abundant (S > 0.6 * capacity), the strategy remains **Cooperate (C)** even if there is minor defection, assuming the pool can absorb the loss. If the resource is scarce (S < 0.3 * capacity), the strategy switches to **Defect (D)** to maximize individual payoff before the pool exhausts.
'''

description_PROSOCIAL_20 = '''
Initialize `cooperation_threshold` = 0.5 (the fraction of opponents required to cooperate to justify continued cooperation).
Initialize `is_punished` = False.

For each round `t` from 1 to `r`:
1. **Decision Rule:**
   - If `t == 1`:
     Play `C`.
   - If `t > 1` and `t < r`:
     - Calculate `opponents_cooperated` = (number of cooperators observed in `t-1` - (1 if action at `t-1` was `C` else 0)) / (n-1).
     - If `is_punished` is `True`:
       Play `D`.
     - Else if `opponents_cooperated` >= `cooperation_threshold`:
       Play `C`.
     - Else:
       Set `is_punished` = `True`.
       Play `D`.
   - If `t == r`:
     - If `is_punished` is `True` or `opponents_cooperated` < `cooperation_threshold` (based on `t-1` results):
       Play `D`.
     - Else:
       Play `C`.

2. **State Monitoring:**
   - If `stock` falls below `capacity / 4`:
     - Force action `C` for the current round, regardless of history, to preserve the pool.
     - Temporarily override `is_punished` logic to `False` for the next round to test for cooperative recovery.

3. **Edge Cases:**
   - If `n` is large (e.g., n > 10), adjust `cooperation_threshold` dynamically:
     `cooperation_threshold` = max(0.2, (n - 2) / (2 * n)). This ensures the threshold scales with the difficulty of achieving consensus in larger groups.
'''

description_PROSOCIAL_21 = '''
### Strategy: Conditional Sustainability (CS)

The strategy maintains a target stock level ($S_{target} = capacity$) to maximize long-term sustainable yield. It utilizes a tit-for-tat variant adapted for a continuous state space, observing the aggregate behavior of opponents to adjust cooperation levels.

#### Variables
*   $k$: Number of opponents who cooperated in the previous round.
*   $k_{threshold}$: An adaptive threshold, initially $\lfloor (n-1)/2 \rfloor$.
*   $S_t$: Stock at the start of round $t$.

#### Decision Rules
1.  **Round 1:** Cooperate (C).
2.  **Rounds 2 to $r-1$:**
    *   If $S_t < (capacity / 2)$: Defect (D) to preserve individual payoff, as the stock is too depleted to recover efficiently.
    *   If $S_t \geq (capacity / 2)$:
        *   If $k \geq k_{threshold}$: Cooperate (C).
        *   If $k < k_{threshold}$: Defect (D) to punish excessive consumption and force stock recovery.
3.  **Final Round ($r$):** Defect (D), regardless of history, to maximize terminal payoff.

#### Adaptive Updates
*   **Threshold Adjustment:** After every round $t$ where $S_t \geq (capacity / 2)$, update $k_{threshold}$ to reflect average opponent cooperation:
    *   $k_{threshold} = \alpha \cdot k_{threshold} + (1 - \alpha) \cdot k$, where $\alpha = 0.9$.
    *   Ensure $k_{threshold}$ remains within the bounds $[0, n-1]$.
*   **Recovery Trigger:** If $S_t$ drops below $(capacity / 4)$, trigger "Recovery Mode": Cooperate (C) for the next 2 rounds regardless of opponent history to allow the stock to regenerate.

#### Pseudocode
```python
def decide_action(round, stock, prev_k, n, capacity):
    # Terminal phase
    if round == r:
        return 'D'

    # Low stock collapse recovery
    if stock < (capacity / 4):
        return 'C'

    # Standard decision logic
    if stock < (capacity / 2):
        return 'D'
    
    # Observe aggregate history and respond
    if prev_k >= k_threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_22 = '''
Maintain a "Conditional Cooperator" stance designed to track and reciprocate the collective behavior of the population. The core objective is to maximize sustainability by matching the aggregate cooperation level of opponents, while applying a "Tit-for-Tat" impulse to punish defection and incentivize restoration of the pool.

**Initialization and State Tracking**
Initialize `reputation = 1.0` (where 1.0 represents full cooperation). 
Maintain a counter `observed_cooperation` based on the previous round's outcome, calculated as `(n_cooperated_opponents) / (n - 1)`.

**Decision Logic**
In each round $t$, determine the action based on the current `reputation` score and the observed history:

1. **Calculate Target Action:**
   If $t = 1$, play **Cooperate (C)**. 
   If $t > 1$:
   - Update `reputation`: `reputation = (0.9 * reputation) + (0.1 * observed_cooperation)`.
   - If `stock` $< (capacity / 4)$: Play **Defect (D)** if previous round outcomes suggest the group is collapsing (i.e., `observed_cooperation` < 0.5), to capture remaining utility; otherwise play **Cooperate (C)** to attempt recovery.
   - If `stock` $\geq (capacity / 4)$:
     - If `reputation` $\geq 0.7$: Play **Cooperate (C)**.
     - If `reputation` $< 0.7$: Play **Defect (D)**.

2. **The "Last Round" Adjustment:**
   In the final round ($t = r$), ignore the `reputation` score and adopt a "Grudger" variation:
   - If the average `observed_cooperation` across all previous rounds $1$ to $r-1$ is $\geq 0.5$, play **Cooperate (C)**.
   - If the average `observed_cooperation` is $< 0.5$, play **Defect (D)**.

**Pseudocode Implementation**

```python
def choose_action(round, total_rounds, n, stock, capacity, history):
    if round == 1:
        return 'C'
    
    if round == total_rounds:
        avg_coop = sum(history['opponents_cooperated']) / (total_rounds - 1)
        return 'C' if avg_coop >= 0.5 else 'D'

    # Calculate reputation
    recent_opp_coop = history['opponents_cooperated'][-1] / (n - 1)
    reputation = (0.9 * history['last_reputation']) + (0.1 * recent_opp_coop)
    
    # Adaptive Thresholding
    if stock < (capacity / 4):
        # Emergency mode
        return 'C' if recent_opp_coop >= 0.5 else 'D'
    else:
        # Standard maintenance
        return 'C' if reputation >= 0.7 else 'D'
```

**Edge Case Handling**
- **Collapse:** If `stock` is effectively zero, all moves yield zero payoff. In this state, continue to play **Cooperate (C)** to minimize further negative impact on potential growth, regardless of opponent behavior.
- **Ambiguous History:** If $n=2$, the `observed_cooperation` will binary-switch (0 or 1). The smoothing factor `(0.9 * reputation) + (0.1 * observed_cooperation)` acts as a hysteresis loop, preventing rapid oscillating behavior against a single, erratic opponent.
'''

description_PROSOCIAL_23 = '''
The strategy employs a "Conditional Sustainability" approach, prioritizing system-wide equilibrium (maintaining stock at capacity) while punishing persistent defection. The strategy tracks the running average of cooperation observed in the population to determine its own move.

**Core Logic:**

1.  **State Tracking:** Maintain a variable `k` representing the number of cooperative moves observed in the previous round, and a variable `r_left` representing the number of rounds remaining.
2.  **Threshold Determination:** Calculate the "Sustainability Threshold" (`T`), defined as the maximum number of defectors the system can sustain in a single round without causing irreversible stock collapse. Given the growth dynamics, the stock remains stable if consumption equals growth.
3.  **Action Rules:**

```python
# Strategy for Round t
if t == 1:
    return Cooperate

# Evaluate historical sustainability
# Let S_prev be the stock at the start of the previous round
# Let C_prev be the number of cooperators observed in the previous round
# Let D_prev be the number of defectors (n - C_prev)

# Calculate consumption for previous round
total_consumption = (C_prev * (S_prev / (2*n))) + (D_prev * (S_prev / n))
s_rem = S_prev - total_consumption
growth = 2 * s_rem * (1 - s_rem / capacity)
next_stock_expected = min(s_rem + growth, capacity)

# If stock is collapsing or we are in the last round:
# Collapse is defined as next_stock_expected < (initial_stock * 0.25)
if next_stock_expected < (capacity * 0.25):
    return Defect # Maximize utility before resource exhaustion

# General Reciprocity Loop
# Maintain cooperation if the group is sustainable
# If the group is behaving unsustainably (consuming too much),
# temporarily defect to pressure the average consumption down,
# or to protect personal payoff parity.

# Calculate Critical Defection Threshold (T_crit)
# T_crit is the number of defectors such that stock degradation occurs.
# If observed defectors (D_prev) > T_crit, enter "Correction Phase"
if D_prev > T_crit:
    return Defect
else:
    return Cooperate
```

**Implementation Specifics:**

*   **T_crit Calculation:** At any state $S$, the strategy calculates the maximum number of defectors ($D_{max}$) allowed such that $S_{next} \ge S$. If $D_{prev} > D_{max}$, the strategy assumes the population is exploitative and switches to Defect to mitigate the loss of the common resource.
*   **The "Last-Mover" Override:** If `r_left == 0`, the strategy always returns `Defect`, as there is no future state to sustain and no incentive for continued cooperation.
*   **Correction Phase:** If the strategy detects that the aggregate behavior of the group caused the stock to drop below a critical threshold (defined as 50% of the previous round's starting stock), it plays `Defect` for one round to re-equilibrate, then returns to `Cooperate` in the subsequent round to signal a willingness to restore the cooperative equilibrium, provided the stock remains above the critical floor.
*   **Robustness:** If `stock` is ever $\le 0$, the strategy assumes the resource is exhausted and plays `Defect` for the remainder of the game.
'''

description_PROSOCIAL_24 = '''
**Strategy: Threshold-Based Conditional Cooperation**

This strategy maintains cooperation while actively punishing defection to sustain the common pool stock. It uses a Tit-for-Tat foundation adapted for a multi-player environment where outcomes are contingent on the aggregate behavior of opponents.

**Decision Logic**

The strategy determines the action for round *t* based on the observed aggregate behavior in round *t-1* and the current stock level *S*.

1.  **Initialization (Round 1):**
    Play **Cooperate (C)**.

2.  **State Assessment (Rounds 2 to *r-1*):**
    Let *K* be the number of opponents who cooperated in the previous round.
    *   **If *K = n-1* (All opponents cooperated):** Play **Cooperate (C)**.
    *   **If *S < capacity / 4* (Critical Stock):** Play **Cooperate (C)**. Low stock requires restraint to prevent extinction.
    *   **If *K < n-1*:** Play **Defect (D)**. This triggers a one-round punishment against the defecting majority, intended to signal that sub-optimal extraction is not tolerated. If the aggregate behavior improves in the next round, return to cooperation immediately.

3.  **Terminal Phase (Round *r*):**
    Play **Defect (D)**, regardless of history. Since there is no future round to punish or reward, maximizing individual payoff is the dominant utility choice.

**Pseudocode**

```
function get_action(round, stock, history):
    if round == r:
        return D
    
    if round == 1:
        return C
    
    // Retrieve previous round aggregate cooperation count
    K = get_opponents_cooperating(history[round-1])
    
    // Recovery trigger
    if stock < (capacity / 4.0):
        return C
    
    // Conditional cooperation mechanism
    if K == (n - 1):
        return C
    else:
        return D
```

**Edge Case Handling**

*   **Stock Collapse:** If the stock reaches 0, the game is effectively over as no further payoff is possible. The strategy will continue to play the dictated action (C), though the result is null.
*   **Persistent Defection:** If the majority of opponents play Defect (D) consistently, the strategy defaults to Defect (D) to avoid being the sole provider for an exploited resource, switching back to C only if the stock falls below the critical threshold (capacity/4) to attempt a desperate recovery of the common pool.
'''

description_PROSOCIAL_25 = '''
The strategy follows a "Conditional Sustainability" approach, prioritizing cooperation while maintaining a trigger mechanism to protect the resource from collapse if opponents over-extract.

**State Tracking**
- `rounds_remaining`: $r - t + 1$
- `cooperation_threshold`: $n - 1$ (The number of other players required to cooperate to maintain long-term stability).
- `stock_critical_level`: $\text{capacity} / 4$ (If the stock falls below this, the risk of total collapse is extreme; more defensive play is required).

**Decision Rules**

1.  **Round 1:** Play **Cooperate (C)**. Establish a baseline for collective behavior.

2.  **Subsequent Rounds ($t > 1$):**
    *   **Check Stock:** If `stock` $\le$ `stock_critical_level`, play **Defect (D)**. When the common pool is near depletion, individual extraction is necessary to recover some utility before the stock reaches zero.
    *   **Check History:** Analyze the behavior of opponents in the previous round ($t-1$).
        *   If the number of players who played **C** in the previous round was $\ge n-1$, play **Cooperate (C)**.
        *   If the number of players who played **C** in the previous round was $< n-1$, play **Defect (D)**. This triggers a temporary "punishment" phase to signal that over-extraction is unsustainable.

3.  **Last Round ($t = r$):**
    *   If `stock` > 0, play **Defect (D)**. Since there are no future rounds, the penalty for depletion is non-existent, and the optimal individual strategy is to maximize the final payoff.

**Pseudocode**

```python
def decide_action(round_number, current_stock, prev_round_cooperators, n, r, capacity):
    # End of game: Grab remaining value
    if round_number == r:
        return 'D'
    
    # Critical depletion: Cannot rely on growth
    if current_stock <= (capacity / 4):
        return 'D'
    
    # Adaptive Trigger: Cooperate if others are cooperating
    # We require near-unanimous cooperation to sustain growth
    if prev_round_cooperators >= (n - 1):
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling**
- **Low Stock Recovery:** If the strategy enters a Defect state due to low cooperation, it resets its cooperation in the subsequent round ($t+1$) *only if* the stock level recovers to above `stock_critical_level`. This creates a "Tit-for-Tat" dynamic that is resilient to small errors or temporary over-consumption, provided the stock remains healthy enough to sustain the group.
- **Initial Round Failure:** If the first round results in immediate depletion, the strategy shifts to D for the duration of the game to minimize loss, as the resource will not recover sufficiently for long-term cooperation.
'''

description_PROSOCIAL_26 = '''
### Strategy: Adaptive Tit-for-Tat with Resource-Contingent Forgiveness

This strategy prioritizes long-term resource sustainability while penalizing defectors proportionally to the threat they pose to the common pool. It uses an "optimism-based" initial approach and shifts to conditional reciprocity based on the observed aggregate cooperation rate.

**Decision Rules:**

1.  **Initial Round (t=1):** Cooperate (C).

2.  **Subsequent Rounds (t > 1):**
    *   Calculate the **Aggregated Cooperation Rate (ACR)** from the previous round (t-1):
        ACR = (Number of Cooperators) / n
    *   **Determine Action:**
        *   **If Stock > Threshold_A (0.8 * capacity):**
            Always Cooperate (C). At high stock levels, maximize the pool even if some opponents defect.
        *   **If Stock < Threshold_B (0.2 * capacity):**
            Defect (D) if ACR < 0.5. At critical low levels, protect self-interest to prevent stock extinction, as the pool is already failing.
        *   **Standard Condition:**
            Cooperate (C) if ACR ≥ 0.5.
            Defect (D) if ACR < 0.5.

3.  **Last Round (t = r):**
    *   If Stock > (0.5 * capacity), Cooperate (C).
    *   If Stock ≤ (0.5 * capacity), Defect (D) to secure remaining resources before game termination.

**Pseudocode:**

```python
def get_action(round_number, stock, total_rounds, last_round_cooperators, n):
    
    # Define thresholds
    HIGH_STOCK_THRESHOLD = 0.8 * capacity
    CRITICAL_STOCK_THRESHOLD = 0.2 * capacity
    TERMINATION_THRESHOLD = 0.5 * capacity

    # Calculate aggregate cooperation rate from last round
    acr = last_round_cooperators / n

    # End-game logic
    if round_number == total_rounds:
        return 'C' if stock > TERMINATION_THRESHOLD else 'D'

    # Opening move
    if round_number == 1:
        return 'C'

    # Strategy execution based on stock and reciprocity
    if stock > HIGH_STOCK_THRESHOLD:
        return 'C'
    
    if stock < CRITICAL_STOCK_THRESHOLD:
        return 'C' if acr >= 0.5 else 'D'
    
    # Standard conditional cooperation
    return 'C' if acr >= 0.5 else 'D'
```

**Adaptation for Forgiveness:**
To recover from periods of mutual defection, if the strategy is currently playing Defect (D) due to low ACR, it checks if stock levels have recovered to > 0.5 * capacity. If the stock is recovering, reset to Cooperate (C) for one round to signal a desire to restart cooperation, regardless of the previous ACR.
'''

description_PROSOCIAL_27 = '''
Calculate the target sustainable consumption level, $C_{target}$, for each round. $C_{target}$ is defined as the consumption value that maintains a stock level of approximately $0.5 \times \text{capacity}$.

The decision logic follows a conditional cooperation framework with a "tit-for-tat" memory window and an aggressive stock-recovery mechanism.

**State Variables:**
- `round_t`: The current round number ($1$ to $r$).
- `prev_stock`: Stock level from the previous round (initialized to `capacity`).
- `cooperation_rate`: The proportion of opponents who cooperated in the previous round.

**Decision Rules:**

1. **Initialization (Round 1):**
   Always play **C**. This signals willingness to cooperate and tests the environment.

2. **Terminal Round (Round $r$):**
   If `prev_stock` > 0.5 * `capacity`, play **C**. Otherwise, play **D** to extract remaining resources, as there are no future consequences to depletion.

3. **Intermediate Rounds ($1 < t < r$):**
   Execute a "Responsive Sustainability" check:
   - If `prev_stock` < $0.2 \times \text{capacity}$:
     Defect (**D**) to force stock replenishment, as the resource is in critical danger of collapse.
   - Else if `cooperation_rate` $\geq 0.5$:
     Cooperate (**C**), as the majority is acting sustainably.
   - Else if `cooperation_rate` < $0.5$:
     Defect (**D**), to punish non-cooperation and prevent further exploitation of the resource by free-riders.

**Pseudocode:**

```python
def get_action(round_t, r, prev_stock, cooperation_rate):
    # Rule 1: Termination Phase
    if round_t == r:
        if prev_stock > (0.5 * capacity):
            return C
        else:
            return D

    # Rule 2: Critical Stock Protection
    # If stock is critically low, prioritize growth over immediate consumption
    if prev_stock < (0.2 * capacity):
        return D 

    # Rule 3: Responsive Sustainability
    # Cooperate if the majority is cooperative, otherwise punish
    if cooperation_rate >= 0.5:
        return C
    else:
        return D
```
'''

description_PROSOCIAL_28 = '''
The strategy operates as a conditional cooperator, utilizing a tit-for-tat variant with a forgiving trigger mechanism that prioritizes long-term resource sustainability. It tracks the average cooperation level of the opponent pool to determine the appropriate action.

**Strategy Logic**

1.  **Initialization:**
    For the first round, play Cooperate (C).

2.  **State Tracking:**
    Maintain a running history of the total number of players who chose Cooperate in previous rounds. Let `Coop_History` be the cumulative count of cooperative actions observed from the population over all prior rounds `t`. Let `Total_Possible_Coops` be `(n-1) * (t-1)`. 
    
    Calculate the opponent cooperation rate:
    `Opponent_Rate = Coop_History / Total_Possible_Coops`

3.  **Decision Rule:**
    For any round `t > 1`:
    - If `Stock < (capacity * 0.25)`, Defect (D) to maximize individual gain before potential collapse, regardless of history.
    - If `Stock >= (capacity * 0.25)`:
        - If `Opponent_Rate >= 0.75`, play Cooperate (C).
        - If `0.4 <= Opponent_Rate < 0.75`, play Cooperate (C) with probability `Opponent_Rate` to encourage reciprocity while managing risk.
        - If `Opponent_Rate < 0.4`, play Defect (D).

4.  **Forgiveness and Recovery:**
    If the strategy defected in the previous round, reset the observation window. In the next round, if the stock is above `capacity * 0.5`, play Cooperate (C) to attempt to restart cooperative behavior, effectively re-initializing the strategy.

5.  **Final Round (t = r):**
    If `Stock >= (capacity * 0.5)`, play Cooperate (C). If `Stock < (capacity * 0.5)`, play Defect (D).

**Pseudocode Representation**

```python
def get_action(round, stock, history_counts, n, capacity):
    # Emergency depletion check
    if stock < (capacity * 0.25):
        return D

    # Final round behavior
    if round == r:
        return C if stock >= (capacity * 0.5) else D

    # Calculate average cooperation rate
    t = round - 1
    if t == 0:
        return C
        
    opp_rate = sum(history_counts) / ((n - 1) * t)

    # Adaptive reciprocity
    if opp_rate >= 0.75:
        return C
    elif opp_rate >= 0.4:
        return C if random.random() < opp_rate else D
    else:
        return D
```
'''

description_PROSOCIAL_29 = '''
Let $S_t$ be the stock at the start of round $t$, $r$ be the total rounds, and $k_t$ be the number of players (excluding self) who played $C$ in the previous round $t-1$. Let $c_t \in \{0, 1\}$ be the self-action at time $t$, where $c_t=1$ is Cooperate ($C$) and $c_t=0$ is Defect ($D$).

**Initialization:**
Play $C$ in the first round ($t=1$).

**Decision Rule for Rounds $t \in \{2, ..., r-1\}$:**
Calculate the "Prosocial Threshold" based on the stock trajectory. If the stock $S_t$ is above the critical sustainability level (defined as $S_t \ge capacity/2$), maintain cooperation to encourage stability. If the stock falls below this level, switch to a reciprocal punishment-restoration logic.

Pseudocode for round $t$:
```python
if t == r:
    return D # Terminal round strategy

if S_t == 0:
    return D # Resource collapsed

# Calculate peer cooperation rate (rho) from previous round
# Let P_t-1 be the number of cooperators observed in round t-1
# rho = P_t-1 / (n - 1)

if S_t > (capacity * 0.5):
    # Stock is healthy; cooperate if most others are cooperating
    if rho >= 0.5:
        return C
    else:
        return D # Punish defection to force sustainable consumption

else:
    # Stock is critically low; require high cooperation to restore
    if rho > 0.8: 
        return C # Only cooperate if high consensus is forming to restore
    else:
        return D # Conserve self-payoff while resource is dying
```

**Edge Case Handling:**
1.  **Terminal Round ($t = r$):** Always play $D$. Since there is no future to impact, the dominant strategy is to capture remaining value.
2.  **Resource Collapse ($S_t = 0$):** Play $D$. Any attempt to cooperate is futile when the stock cannot regenerate.
3.  **Low Population Cooperation:** If the average peer cooperation rate drops below 0.2, initiate a "Tit-for-Tat" reset: play $D$ for two rounds regardless of stock level to discourage parasitic behavior, then resume the standard decision rule.
4.  **Recovery Phase:** If the stock $S_t$ increases by more than 30% from $S_{t-1}$, revert to $C$ regardless of peer history to signal support for the sustainable equilibrium.
'''

description_PROSOCIAL_30 = '''
Maintain cooperation as the default strategy, using a conditionally cooperative threshold mechanism to protect the common pool from depletion.

**Strategy Definitions:**
- **Cooperate (C):** Participate in sustainable extraction.
- **Defect (D):** Extract greedily.
- **Sustainability Threshold (T):** The stock level $S_t$ below which the pool is at risk of collapse. Let $T = 0.5 \times \text{capacity}$.
- **Target Cooperation Count ($k$):** The number of cooperating opponents required to maintain or increase the pool stock. For $n=4$, if all play $C$, stock remains stable. If $k$ players cooperate, the total consumption is $(k \times \frac{S}{2n}) + ((n-k) \times \frac{S}{n}) = \frac{S}{2n}(k + 2(n-k)) = \frac{S}{2n}(2n - k)$.

**Decision Rules:**

1. **Initialization (Round 1):**
   Always play $C$.

2. **Conditional Response (Rounds 2 to $r-1$):**
   Observe the number of cooperating opponents $c_{t-1}$ from the previous round.
   - **If $S_t > T$:** Play $C$. The pool is robust enough to sustain moderate defecting behavior without immediate risk of collapse.
   - **If $S_t \le T$:**
     - If $c_{t-1} \ge \frac{n}{2}$ (a majority of opponents cooperated), play $C$.
     - If $c_{t-1} < \frac{n}{2}$ (the pool is being rapidly depleted by greedy behavior), play $D$ to minimize personal loss while the pool collapses, or to force a reset if the group dynamic necessitates it. 

3. **Terminal Phase (Final Round $r$):**
   In the final round, the incentive for future sustainability is removed. 
   - If $S_r \ge T$, play $C$ to maximize the final collective extraction.
   - If $S_r < T$, play $D$ to secure the maximum share of the remaining stock before the game terminates.

**Edge Case Handling:**
- **Pool Exhaustion:** If $S_t \approx 0$, play $D$ regardless of history. There is no future value to preserve, and mutual $C$ at near-zero stock yields negligible utility.
- **Recovery Mode:** If $S_t$ falls below a critical level (e.g., $0.2 \times \text{capacity}$), switch to $D$ for one round to recoup utility, then return to $C$ in the subsequent round to attempt a "tit-for-tat" style reset of group cooperation, provided the stock is above 0.
'''

description_PROSOCIAL_31 = '''
The strategy relies on a tit-for-tat variant adapted for a continuous resource environment, designed to sustain stock levels while punishing defection. 

Let $C_t$ be the number of cooperators observed in round $t$. Let $H_t$ be the history of observed cooperation counts $\{C_1, C_2, \dots, C_{t-1}\}$.

### Decision Rule
In any round $t$, play Cooperate ($C$) if the "Cooperation Threshold" is met. Otherwise, play Defect ($D$).

**1. Initialization:**
In round $t=1$, always play $C$.

**2. Threshold Calculation:**
The Cooperation Threshold depends on the current stock level $S_t$ and recent history. 
*   If $S_t < \frac{capacity}{4}$, play $D$ regardless of history to recover stock (a "rescue" maneuver).
*   Otherwise, define the opponent average cooperation rate $\bar{A} = \frac{1}{k} \sum_{j=t-k}^{t-1} \frac{C_j}{n-1}$, where $k = \min(t-1, 3)$ is the lookback window.
*   Play $C$ if $\bar{A} \ge 0.5$.
*   Play $D$ if $\bar{A} < 0.5$.

**3. The Last Round Constraint:**
In the final round $r$, ignore the threshold. Play $D$ if $S_r > 0$, otherwise play $C$. This prevents exploitation of cooperative behavior when there is no future interaction to incentivize.

### Pseudocode

```python
def get_action(round_number, current_stock, history, n, capacity):
    # Rule 1: Last round exit
    if round_number == r:
        return 'D' if current_stock > 0 else 'C'

    # Rule 2: Stock preservation (The "Rescue" mode)
    if current_stock < (capacity / 4):
        return 'D'

    # Rule 3: Tit-for-Tat adaptation
    if round_number == 1:
        return 'C'
    
    # Calculate average cooperation of others from recent history (k=3)
    k = min(round_number - 1, 3)
    recent_others_cooperation = [history[j] / (n - 1) for j in range(round_number - 1 - k, round_number - 1)]
    avg_opponents_cooperation = sum(recent_others_cooperation) / k
    
    if avg_opponents_cooperation >= 0.5:
        return 'C'
    else:
        return 'D'
```

### Edge Cases
*   **Total Depletion ($S_t \approx 0$):** If the stock is zero, cooperation yields zero payoff. Defecting also yields zero, but does not harm others. The strategy defaults to $C$ in the final round if stock is zero, otherwise $D$. 
*   **Low Stock Recovery:** The "Rescue" threshold ($capacity/4$) overrides cooperation norms. If the stock falls into this critical zone, the strategy automatically switches to Defect to maximize individual gain and stabilize the stock through the subsequent growth function, treating the population as having failed to coordinate.
*   **Small $n$:** The threshold $\bar{A} \ge 0.5$ remains robust for $n \ge 2$, as it requires a majority of opponents to have cooperated in the recent window.
'''

description_PROSOCIAL_32 = '''
The strategy utilizes a conditional, state-aware approach designed to maximize the sustainable stock while punishing defectors, balancing long-term resource preservation against immediate depletion threats.

**Initial Round (Round 1):**
Always play Cooperate (C).

**Subsequent Rounds (Round $t > 1$):**
Decide action based on the *Cooperation Rate* ($CR_{t-1}$) of the previous round and the current stock level ($S_t$).

The Cooperation Rate is defined as the fraction of all $n$ players who cooperated in the previous round, calculated by observing total consumption ($C_{total, t-1}$) relative to the stock level ($S_{t-1}$). Since $C_{total, t-1} = (\text{number of cooperators} \times \frac{S_{t-1}}{2n}) + (\text{number of defectors} \times \frac{S_{t-1}}{n})$, the number of cooperators ($k_{t-1}$) is derived as:
$k_{t-1} = \frac{n \times (S_{t-1} - C_{total, t-1})}{S_{t-1}/2}$

**Decision Rules:**
1. **Stock Threshold:** If $S_t < \epsilon$ (where $\epsilon = 0.05 \times \text{capacity}$), play Defect (D) to secure remaining utility before resource collapse.
2. **Tit-for-Tat Trigger:** If $k_{t-1} < n$, calculate the expected stock growth for the next round based on current cooperation. If the stock $S_t$ is below the sustainability equilibrium (where consumption exceeds regeneration, specifically if $S_t < 0.5 \times \text{capacity}$), switch to Defect (D) for one round to signal intolerance for over-extraction.
3. **Recovery:** If $S_t \ge 0.5 \times \text{capacity}$ and $k_{t-1} = n$, play Cooperate (C).
4. **Forgiveness:** If the previous round resulted in a partial collapse but the current stock $S_t$ has regenerated to $\ge 0.5 \times \text{capacity}$, reset to Cooperate (C) to re-establish trust.

**Pseudocode:**
```python
if round == 1:
    return Cooperate

# Check for imminent collapse
if stock < (0.05 * capacity):
    return Defect

# Observe previous round behavior
# Calculate number of cooperators from observed total consumption
num_cooperators = calculate_cooperators(total_consumption_prev, stock_prev)

if num_cooperators == n:
    return Cooperate
else:
    # If the resource is critically low or being depleted faster than it grows
    if stock < (0.5 * capacity):
        return Defect # Punish non-cooperation
    else:
        # Resource is healthy enough to tolerate some non-cooperation
        return Cooperate 
```

**Final Round (Round $r$):**
If $S_r \ge 0.5 \times \text{capacity}$, play Cooperate (C). If $S_r < 0.5 \times \text{capacity}$, play Defect (D) to avoid leaving resources unharvested that will not regenerate.
'''

description_ALTRUISTIC_5 = '''
This strategy employs a "Conditional Tit-for-Tat with Resource Preservation" logic. It prioritizes the sustainability of the common pool while punishing defection only to the extent required to preserve future utility for all participants.

### Strategy Rules

**1. Initialization (Round 1):**
Always play **Cooperate (C)**. This signals a commitment to sustainable resource management and establishes a baseline for cooperation.

**2. Monitoring (Rounds 2 to r):**
Calculate the "Cooperation Threshold" based on the observed behavior of opponents in the previous round. Define `C_observed` as the number of players who played C in the previous round (including yourself).
*   Target a sustainable consumption state where the resource grows to maximum capacity at the start of every round. 
*   If `C_observed` = `n` (All players cooperated in the previous round), continue to play **C**.

**3. Response to Defection (Retaliation/Adaptation):**
If `C_observed` < `n` (at least one player defected):
*   Calculate the projected stock for the next round. If the current stock `S` is below a "Safety Threshold" (defined as `0.5 * capacity`), play **Defect (D)**. This is a survival mechanism to ensure you capture remaining value before the pool collapses due to others' over-consumption.
*   If `S` is above the "Safety Threshold," play **Cooperate (C)**. This acts as an altruistic gesture, signaling that even though some players defected, you are willing to invest in the pool's recovery to allow them another opportunity to cooperate.

**4. Final Round (Round r):**
Regardless of previous history or current stock, play **Defect (D)**. Since there is no future round to benefit from sustainable stock levels, the altruistic priority shifts to maximizing your final payoff, as any remaining stock is lost regardless of action.

### Pseudocode Representation

```python
def get_action(round_number, total_rounds, n, S, capacity, last_round_cooperators):
    # Final round: Maximize payoff
    if round_number == total_rounds:
        return 'D'
    
    # First round: Signal cooperation
    if round_number == 1:
        return 'C'
    
    # Analyze previous round
    # last_round_cooperators includes your own move
    if last_round_cooperators == n:
        return 'C'
    
    # If defection occurred, check stock viability
    safety_threshold = 0.5 * capacity
    
    if S < safety_threshold:
        # Resource endangered: Defect to secure share
        return 'D'
    else:
        # Resource healthy: Offer forgiveness/altruism
        return 'C'
```

### Edge Cases
*   **Stock = 0:** If the stock reaches 0, the game dynamics dictate payoff will be 0 regardless of action. Continue to play **C** until the final round to maintain consistent behavior, assuming the resource might recover.
*   **High-Defection Environments:** If the opponents consistently defect and the stock drops below the safety threshold, this strategy forces a switch to **D** to prevent total loss, while attempting to revert to **C** if the stock manages to recover through the growth dynamics.
'''

description_ALTRUISTIC_6 = '''
To maximize the sustainability of the resource and ensure equitable, long-term welfare for all participants, adopt a **Conditional Sustainable Stewardship** strategy. This approach relies on "Tit-for-Tat" logic adapted for a resource-replenishment environment, prioritizing the preservation of the common pool above immediate gain.

### Decision Rules
In each round $t$, choose your action based on the state of the pool ($S_t$) and the observed behavior of the group in round $t-1$. Let $k$ be the number of players who chose Cooperate ($C$) in the previous round.

1.  **Initial Round ($t=1$):** Always play $C$. This establishes a willingness to cooperate.
2.  **Sustainability Threshold:** If $S_t \le (\text{capacity} / 4)$, the resource is in critical decline. Play $C$ regardless of previous history to prevent total collapse.
3.  **General Rounds ($t > 1$):**
    *   **If $k = n$ (Everyone cooperated):** Play $C$. The resource is stable; maintain the equilibrium.
    *   **If $k < n$:** Play $D$ with a probability $p$ proportional to the degree of defection, or play $C$ if the stock $S_t$ is below the "optimal regeneration level" (calculated as $S_{target} = \text{capacity} / 2$).
    *   **Strict Trigger (Punishment/Correction):** If the average consumption in the previous round exceeded the regenerative capacity (causing $S_{t} < S_{t-1}$), and you did not play $D$ in the previous round, switch to $D$ for one round to signal that the current consumption rate is unsustainable.

### Pseudocode Logic
```python
def decide_action(round_num, stock, last_round_cooperators, n, capacity):
    # 1. Survival Clause
    if stock <= (capacity / 4):
        return 'C'

    # 2. Initialization
    if round_num == 1:
        return 'C'

    # 3. Collaborative Maintenance
    if last_round_cooperators == n:
        return 'C'

    # 4. Adaptive Correction
    # If the resource is decreasing and others are defecting, 
    # force a 'D' action only if it helps reach the tipping point 
    # to signal unsustainability, otherwise default to 'C' to 
    # avoid accelerating the collapse.
    if last_round_cooperators < n:
        if stock < (capacity / 2):
            return 'D' # Signal that consumption is too high relative to stock
        else:
            return 'C' # Resource is healthy enough to sustain defectors
```

### Edge Cases
*   **Final Round ($t = r$):** Ignore future-looking sustainability. Play $D$ if the resource is healthy ($S_t > \text{capacity} / 2$) to capture remaining value. If $S_t$ is low, play $C$ to avoid depleting the stock to zero, as a zero-stock outcome provides no utility.
*   **Near-Zero Stock:** If $S_t \approx 0$, play $C$. There is no utility in defecting against an empty pool, and cooperating leaves a non-zero remainder for potential future recovery.

### Altruistic Alignment
The core philosophy is *reciprocal restraint*. You act as a stabilizer:
*   You punish defection when the resource is threatened by "Defecting" (reducing your own intake to force a collective drop in total consumption if you were the only one defecting, or signaling to others).
*   You forgive (return to $C$) as soon as the group demonstrates a return to sustainable consumption patterns.
*   You prioritize long-term aggregate payoff over short-term individual gain, ensuring the resource survives long enough to generate the maximum possible sum of payoffs for all players.
'''

description_ALTRUISTIC_7 = '''
Cooperate (C) for the duration of the game unless the common pool is being depleted by others to a critical threshold, at which point switch to Defect (D) to maximize individual share before total collapse.

**Decision Logic:**

Initialize `trust_threshold = 0.5`.
Maintain a running estimate of `cooperation_rate`, defined as the ratio of observed cooperators to total players in previous rounds.

For every round `t` with current stock `S`:

1. **Terminal Round Handling:** If `t == r`, play Defect (D) regardless of history, as there is no future state to incentivize cooperation.

2. **Stability Check:** If `S < (capacity * 0.2)`, the stock is at critical risk of exhaustion. Play Defect (D) to ensure payoff capture before depletion.

3. **Reciprocity Trigger:**
   If `t > 1`, calculate `avg_cooperation = (sum of cooperators in previous rounds) / ((n-1) * (t-1))`.
   If `avg_cooperation < trust_threshold` and `S` is declining (New stock at `t-1` < Stock at `t-2`), play Defect (D).
   Otherwise, play Cooperate (C).

4. **First Round:** Play Cooperate (C).

**Pseudocode:**

```python
def get_action(round_t, stock_t, history):
    if round_t == r:
        return D
    
    if stock_t < (capacity * 0.2):
        return D
    
    if round_t > 1:
        avg_cooperation = sum(history['cooperators']) / ((n - 1) * (round_t - 1))
        stock_declining = history['stock'][round_t-1] < history['stock'][round_t-2]
        
        if avg_cooperation < 0.5 and stock_declining:
            return D
            
    return C
```
'''

description_ALTRUISTIC_8 = '''
The strategy operates on a "Tit-for-Tat with Forgiveness and Sustainability Thresholds" logic, prioritizing resource preservation while incentivizing collective cooperation.

### Strategy Rules

**Phase 1: Initialization**
In the first round, always play **Cooperate (C)**. This signals a commitment to sustainable resource management.

**Phase 2: Monitoring and Retaliation (Rounds 2 to r-1)**
Calculate the "Cooperation Ratio" ($CR$) of the previous round: $CR = (\text{Number of Cooperators}) / n$.

If $S_t$ (current stock) is above a critical threshold of $0.5 \times \text{capacity}$:
- If $CR \ge 0.5$, play **Cooperate (C)**.
- If $CR < 0.5$, play **Defect (D)** to penalize over-extraction.

If $S_t$ (current stock) falls below $0.5 \times \text{capacity}$:
- Regardless of $CR$, play **Cooperate (C)**. This prioritizes stock recovery even if opponents are defecting, as depleting a near-empty pool ensures zero future payoffs.

**Phase 3: Forgiveness**
If you defected in the previous round due to low $CR$, but in the subsequent round $CR$ rises above $0.5$, immediately switch back to **Cooperate (C)** in the following round. This mechanism resets the dynamic to allow for renewed sustainable extraction.

**Phase 4: Terminal Rounds (Final 2 rounds)**
In the final round, ignore the $CR$ logic. If $S_r > 0$, play **Defect (D)** if and only if you have consistently cooperated in $\ge 75\%$ of prior rounds and the current stock $S_r$ is sufficient to support Defection without collapsing the system below 0 stock. If the stock is critically low ($< 0.25 \times \text{capacity}$), always play **Cooperate (C)** to maximize the final round's collective welfare.

### Pseudocode Representation

```python
def decide_action(round, n, S, capacity, history):
    # Terminal Round
    if round == r:
        if S < (0.25 * capacity):
            return C
        else:
            return D if (cooperation_rate_history > 0.75) else C

    # Initial Round
    if round == 1:
        return C

    # Stock-Dependent Strategy
    previous_cooperators = history.last_round.cooperators
    CR = previous_cooperators / n

    if S > (0.5 * capacity):
        if CR >= 0.5:
            return C
        else:
            return D
    else:
        # Stock recovery mode
        return C
```

### Altruistic Rationale
This strategy is altruistic by embedding the "Common Good" within the decision structure. By defaulting to cooperation in early rounds and when stock levels are perilous, it prevents the Tragedy of the Commons. It only defects to enforce a punishment mechanism, specifically designed to force opponents back toward sustainable extraction rates, thereby maximizing the total long-term utility of the pool for all participants rather than seeking immediate individual gain at the expense of system collapse.
'''

description_ALTRUISTIC_9 = '''
Define the target stock level as $S_{target} = capacity / 2$. This level maximizes the growth function (derivative of $2S(1 - S/capacity)$ is zero at $S = capacity/2$).

### Core Decision Rule: Threshold-Triggered Tit-for-Tat
Maintain a "cooperation score" ($C_{score}$) representing the perceived willingness of the collective group to sustain the resource.

1. **Initialization**: Start with $C_{score} = 0$.
2. **Round 1**: Always play **C** (Cooperate) to signal altruistic intent.
3. **Subsequent Rounds (t > 1)**:
   - Calculate $S_{expected} = min(S_{remaining\_prev} + 2 \times S_{remaining\_prev} \times (1 - S_{remaining\_prev}/capacity), capacity)$.
   - If current stock $S < 0.2 \times capacity$, play **D** (Defect) to maximize immediate personal payoff before the pool is exhausted, as the resource is no longer sustainable.
   - If current stock $S \ge 0.2 \times capacity$, execute the following conditional logic:
     - Determine "Proportion of Cooperators" ($P_c$) from the previous round.
     - Update $C_{score}$: $C_{score} = C_{score} + (P_c - \text{threshold})$, where the threshold is $(n-1)/n$ (roughly 1.0).
     - If $C_{score} \ge 0$, play **C**.
     - If $C_{score} < 0$, play **D**.

### Pseudocode Logic
```python
def get_action(round, stock, prev_cooperators_count):
    # Terminal phase: maximize remaining returns if stock is collapsing
    if stock < (0.2 * capacity) or round == r:
        return D
    
    # Initial exploration
    if round == 1:
        return C
    
    # Assess collective behavior
    # prev_cooperators_count is the number of players who chose C in previous round
    # If I chose C, the number of other cooperators is (prev_cooperators_count - 1)
    # If I chose D, the number of other cooperators is prev_cooperators_count
    
    # Calculate cooperation threshold (n-1 = full cooperation of others)
    others_cooperated = (prev_cooperators_count - 1) if (my_prev_action == C) else prev_cooperators_count
    
    # Adjustment factor: Reward full cooperation, punish defectors
    # If all others cooperated, score increases. If any defected, score decreases.
    if others_cooperated == (n - 1):
        self.c_score += 1
    else:
        self.c_score -= (n - others_cooperated)
        
    # Decision
    if self.c_score >= 0:
        return C
    else:
        return D
```

### Altruistic Constraints
- **Self-Correction**: If the stock recovers due to other players switching to cooperation, the $C_{score}$ will naturally rise above 0, and the strategy will return to playing **C**.
- **Last Round Exception**: In the final round ($r$), always play **D** regardless of $C_{score}$, as the game ends and future growth is irrelevant. This ensures individual payoff is not entirely sacrificed when reciprocity can no longer be enforced.
- **Resource Protection**: If the stock is critical ($< 20\%$ of capacity), switch to **D**. At this state, the tragedy of the commons is effectively occurring; hoarding the remaining units provides higher utility than attempting a failed rescue, preventing other defectors from extracting the remaining stock exclusively.
'''

description_ALTRUISTIC_10 = '''
The strategy, titled "Sustainable Stewardship," aims to maintain the stock at its capacity for the duration of the game through a conditional cooperation mechanism. It treats the common pool as a shared asset, prioritizing sustainability over short-term gain while punishing persistent defectors to protect the resource.

### Core Logic
The strategy uses a "Tit-for-Tat with Forgiveness" approach, modified to account for the continuous nature of the resource. The fundamental decision is determined by the "target action" for the current round, which is modified by the observed behavior of opponents in the previous round.

### Variables and Parameters
*   `n`: Number of players.
*   `C_rate`: Number of cooperators observed in the previous round.
*   `S_prev`: Stock level at the start of the previous round.
*   `Threshold_Stock`: The minimum stock level below which the strategy defaults to cooperation to facilitate recovery (set to 0.5 * capacity).
*   `Defection_Tolerance`: The number of rounds an opponent is "forgiven" before triggering a defensive strategy (set to 1).

### Decision Rules

1.  **Initialization (Round 1):**
    Play `Cooperate` (C). This establishes a commitment to sustainability and signals cooperative intent.

2.  **General Rounds (Round 2 to r-1):**
    Calculate the `Sustainability_Index`, which is the ratio of `C_rate` to `n`.
    *   **Case A (Strong Cooperation):** If `C_rate == n`, continue to play `Cooperate` (C).
    *   **Case B (Minor Defection):** If `C_rate` is between `(n/2)` and `(n-1)`, play `Cooperate` (C) but monitor the `S_prev`. If `S_prev < Threshold_Stock`, switch to `Cooperate` (C) regardless of current defection to ensure stock recovery.
    *   **Case C (High Defection):** If `C_rate <= n/2`, switch to `Defect` (D) for the current round. This is a temporary corrective measure to rebalance the stock and discourage systematic depletion.
    *   **Case D (Stock Crisis):** If `S_prev < 0.2 * capacity`, play `Cooperate` (C) regardless of `C_rate` to prevent total resource collapse.

3.  **Last Round (Round r):**
    Play `Defect` (D) only if `S_prev` is above `0.5 * capacity` AND the average `C_rate` over the previous `(r/2)` rounds was greater than `0.75 * n`. Otherwise, play `Cooperate` (C) to ensure the resource remains viable for the final state transition.

### Pseudocode Representation

```python
def make_decision(round, stock, prev_C_rate, n, capacity):
    # Rule 1: First Round
    if round == 1:
        return Cooperate
    
    # Rule 2: Stock Crisis (Emergency Recovery)
    if stock < (0.2 * capacity):
        return Cooperate
    
    # Rule 3: Last Round Strategy
    if round == r:
        if stock > (0.5 * capacity) and avg_C_rate > (0.75 * n):
            return Defect
        else:
            return Cooperate
            
    # Rule 4: Standard Adaptive Behavior
    if prev_C_rate == n:
        return Cooperate
    elif prev_C_rate <= (n / 2):
        return Defect
    else: # Mixed behavior
        if stock < (0.5 * capacity):
            return Cooperate
        else:
            return Cooperate # Maintain cooperation unless clearly betrayed
```

### Altruistic Rationale
The strategy is designed to maximize the total sum of payoffs across the collective rather than individual gains. By prioritizing the `Sustainability_Index`, it ensures that the common pool is replenished. The "Defect" option in Case C is not malicious; it acts as a stabilizing feedback loop to prevent "Tragedy of the Commons" scenarios where players who defect consistently exhaust the resource for everyone. The final round rule ensures that cooperation is sustained as long as the resource health permits.
'''

description_ALTRUISTIC_11 = '''
**Target State Maintenance (TSM)**

The strategy aims to maintain the common pool stock at `capacity/2`, the level maximizing replenishment (growth). This ensures long-term sustainability for all players.

**Decision Logic**

For any round *t*, let *S* be the current stock, *n* be the number of players, and *k* be the number of cooperators observed in the previous round (for *t* > 1).

1.  **Initialization (Round 1):**
    Play **Cooperate (C)**.

2.  **Adaptive Phase (Rounds 2 to r-1):**
    Calculate the projected stock *S_next* assuming all players play C:
    *   *Consumption per player* = *S / (2n)*
    *   *Total consumption* = *n × (S / 2n) = S / 2*
    *   *S_remaining* = *S - (S/2) = S/2*
    *   *S_next* = *S_remaining + 2 × S_remaining × (1 - S_remaining / capacity)*

    If *S_next* < *capacity/2* (the stock is depleting), or if the *S* is below a critical threshold (e.g., *capacity/4*), prioritize replenishment:
    *   Play **Cooperate (C)**.

    If *S_next* > *capacity/2* (the stock is abundant, exceeding sustainable replenishment levels):
    *   Play **Defect (D)** if the number of cooperators in the previous round was greater than *n/2* (indicating the pool can handle the extraction).
    *   Otherwise, play **Cooperate (C)**.

    If *S_next* ≈ *capacity/2*:
    *   Play **Cooperate (C)**.

3.  **Terminal Phase (Final Round *r*):**
    Play **Defect (D)** if the remaining stock *S* is sufficiently high such that *S/n* > *S/(2n)*. Since this is the final round, the sustainability constraint is irrelevant. Maximize the individual payoff to ensure the accumulated altruistic efforts are realized.

**Edge Case Handling**

*   **Stock Extinction:** If *S* drops below *1/n* of the initial capacity, play **Cooperate (C)** regardless of previous history or round number to prevent immediate collapse, unless the game is in the final round.
*   **Opponent Defection:** If the observed number of cooperators in round *t-1* is consistently low (e.g., *k < n/4*), calculate the probability of survival. If survival probability is near zero, switch to **Defect (D)** to capture remaining utility before exhaustion. If survival is possible, continue to play **Cooperate (C)** to signal potential for cooperation, as punishment is not possible.
*   **Near Capacity:** If *S* > 0.9 * capacity, prioritize **Defect (D)** to prevent "wasteful" accumulation that does not convert to growth, effectively "harvesting" the surplus for all players.
'''

description_ALTRUISTIC_12 = '''
The strategy operates on a "Tit-for-Tat with Forgiveness and Stock Preservation" principle, designed to maximize collective utility while punishing defection only to the extent necessary to preserve the resource. The core objective is to maintain the stock level at exactly $S_{target} = capacity/2$, where the growth function $2 \times S \times (1 - S/capacity)$ reaches its maximum value of $capacity/2$, allowing for sustainable consumption.

### Decision Logic

Let $k$ be the number of cooperators observed in the previous round, and $D_{count} = n - k$ be the number of defectors.

**1. Initialization (Round 1):**
Cooperate ($C$). This signals intent for mutual sustainability.

**2. Standard Rounds ($t \in \{2, \dots, r-1\}$):**
The decision is based on whether the collective action in the previous round resulted in a sustainable stock level and whether the group is cooperating.

*   **Condition A (Sustainability Check):** If current stock $S$ is below a critical threshold $S_{crit} = capacity \times 0.25$, immediately play $D$ for one round to extract remaining value before exhaustion, as collapse is imminent.
*   **Condition B (Tit-for-Tat):** If $S \ge S_{crit}$:
    *   If $D_{count} = 0$: Play $C$.
    *   If $D_{count} > 0$: Play $D$. This enforces a penalty on the group for previous defection.
*   **Condition C (Forgiveness):** If $D_{count} > 0$ and the stock $S$ is recovering (i.e., $S_{t} > S_{t-1}$), switch back to $C$ with probability $P_{forgive} = (S_t / capacity)$, favoring cooperation as the resource replenishes.

**3. Final Round ($t = r$):**
If $S > 0$, play $D$. Because there is no future, there is no benefit to saving the resource. If $S = 0$, the action is irrelevant.

### Pseudocode Representation

```python
def get_action(round_number, n, S, capacity, last_round_defectors):
    # Terminal Round
    if round_number == total_rounds:
        return 'D'
    
    # Critical Stock Check (Collapse prevention)
    critical_threshold = capacity * 0.25
    if S < critical_threshold:
        return 'D'
        
    # Tit-for-Tat Logic
    if last_round_defectors == 0:
        return 'C'
    else:
        # Check if we should forgive defectors based on recovery
        # (This logic implies we stay D if defectors exist, 
        # unless stock is healthy, then we test cooperation)
        if S > (capacity * 0.5):
            return 'C' # Attempt reconciliation if stock is high
        else:
            return 'D' # Punishment phase
```

### Altruistic Rationale
This strategy assumes that the group's collective benefit is prioritized. It sacrifices individual short-term gain ($D$) to ensure the common pool remains within the optimal growth range ($capacity/2$). It is altruistic because it only defects when necessary to force the group back toward cooperation (Condition B) or when the resource is already doomed (Condition A), thereby minimizing the "tragedy of the commons" while remaining robust against exploitation.
'''

description_ALTRUISTIC_13 = '''
### Strategy: Adaptive Sustainable Reciprocity

The objective is to maintain the stock at its maximum sustainable capacity ($C_{max}$) while penalizing defectors proportionally to their impact, transitioning to defect only when the stock is critically threatened.

**1. Definitions**
*   **Target Stock ($S_{target}$):** Defined as $0.5 \times \text{capacity}$. This is the inflection point where growth is maximized (the apex of the logistic growth curve).
*   **Stock Health ($H$):** $S / \text{capacity}$.
*   **Defection Threshold ($\tau$):** The number of opponents observed defecting in the previous round.
*   **Cooperation Phase:** Default state, where action is $C$.
*   **Punishment Phase:** Triggered by detecting non-cooperative behavior; action is $D$.

**2. Decision Rules**
In each round $t$, perform the following calculation:

*   **Round 1:** Play $C$.
*   **Rounds $t > 1$:**
    *   *If current stock $S < 0.1 \times \text{capacity}$:* Defect ($D$) to maximize remaining personal payoff before depletion.
    *   *Else:*
        *   Calculate observed defection count from the previous round ($d_{prev}$).
        *   If $d_{prev} = 0$: Play $C$.
        *   If $d_{prev} > 0$:
            *   Calculate probability of punishment: $P(\text{punish}) = \min(1, \frac{d_{prev}}{n-1} \times \text{RiskFactor})$.
            *   Where $\text{RiskFactor}$ scales based on stock health: if $H < 0.5$, $\text{RiskFactor} = 1.5$; if $H \ge 0.5$, $\text{RiskFactor} = 0.5$.
            *   If random value $\in [0, 1] < P(\text{punish})$: Play $D$.
            *   Else: Play $C$.

**3. Altruistic Heuristic**
The strategy inherently prioritizes the "Cooperate" action because the aggregate payoff is maximized when all players cooperate ($S$ stays near capacity). The punishment mechanism is probabilistic rather than deterministic; this allows for "noisy" altruism, preventing death spirals that occur when all players instantly switch to permanent defection upon detecting a single error.

**4. Pseudocode**

```python
def get_action(round, stock, n, capacity, prev_round_defectors):
    # Terminal phase check
    if stock < 0.1 * capacity:
        return D
    
    # Opening move
    if round == 1:
        return C
    
    # Tit-for-Tat derivative
    if prev_round_defectors == 0:
        return C
    
    # Probabilistic punishment
    health = stock / capacity
    risk_factor = 1.5 if health < 0.5 else 0.5
    prob_punish = min(1.0, (prev_round_defectors / (n - 1)) * risk_factor)
    
    if random.random() < prob_punish:
        return D
    else:
        return C
```

**5. Edge Case Handling**
*   **Last Round:** The strategy ignores the "end-game" defect bias. It continues to follow the probabilistic punishment rules. This maintains the cooperative equilibrium up to the final moment, maximizing the collective potential payoff for the entire duration of the game.
*   **Depletion:** If the stock falls below 10% of capacity, the strategy ceases altruism and switches to $D$, acknowledging that collective sustainability has failed and individual loss mitigation is necessary.
'''

description_ALTRUISTIC_14 = '''
The strategy, **Conditional Stewardship**, aims to maximize the long-term utility of the pool while maintaining resilience against exploitation. It operates on a tit-for-tat logic grounded in the sustainability of the resource stock.

### Decision Rules

For any given round `t`, let `S_t` be the current stock level, `n` be the number of players, and `m_t` be the number of cooperators observed in the previous round `t-1`.

1.  **Initialization (Round 1):** Play **Cooperate (C)**.
2.  **Sustainability Threshold:** If `S_t < (capacity / n)`, the resource is critically low. Play **Cooperate (C)** regardless of previous history to prioritize stock recovery.
3.  **Cooperation Maintenance:** In rounds `t > 1`, play **Cooperate (C)** if the average cooperation rate of the opponents in the previous round `m_{t-1}` meets or exceeds the sustainability threshold `T`. Define `T` as `(n-1) * 0.75` (rounded up to the nearest integer). This ensures that as long as a strong majority of players are acting sustainably, you continue to support the common pool.
4.  **Defection Response:** If `m_{t-1} < T`, play **Defect (D)**. This triggers a punitive response to prevent free-riders from depleting the stock while you sustain it alone.
5.  **Re-entry (Forgiveness):** If you are currently in a punitive state (`D`), monitor the stock level. If the stock `S_t` recovers to `≥ capacity / 2`, switch back to **Cooperate (C)** in the following round, regardless of the previous round's cooperation count.

### Edge Cases

*   **Final Round (Round `r`):** Ignore the future consequences of depletion. If `S_r` is sufficiently high (e.g., `S_r > capacity / 2`), you may switch to **Defect (D)** to capture the remaining value. If `S_r` is low, stick to the cooperation rule to maximize the final round's potential payoff for the group.
*   **Low Stock Floor:** If `S_t` is extremely close to 0 (where even cooperation risks total collapse), force **Cooperate (C)** to minimize further drainage.
*   **Opponent Consistency:** If opponents consistently defect, the strategy collapses to permanent defection, which is the only rational response when the resource is doomed to exhaustion.

### Pseudocode

```python
def get_action(round, n, S_t, S_prev, m_prev, capacity):
    # Rule 2: Sustainability Threshold
    if S_t < (capacity / n):
        return C
    
    # Rule 5: Final Round
    if round == r:
        return D if S_t > (capacity / 2) else C

    # Rule 3 & 4: Tit-for-Tat based on quorum
    quorum = ceil((n - 1) * 0.75)
    
    # Check if we were punishing and can forgive
    if S_t >= (capacity / 2):
        return C
        
    if m_prev >= quorum:
        return C
    else:
        return D
```
'''

description_ALTRUISTIC_15 = '''
### Strategy: Adaptive Stewardship

**Core Principle:**
Maximize the sustainability of the common pool resource by mirroring the aggregate cooperativeness of the group, while punishing defectors only enough to incentivize cooperative convergence.

**Variables:**
- `history_cooperation_rate`: The cumulative ratio of (total cooperation events) / (total potential cooperation events) across all previous rounds.
- `last_round_cooperation_rate`: The ratio of (cooperating opponents in last round) / (number of opponents).
- `t`: The current round number.

**Decision Logic:**

1.  **Initialization (Round 1):**
    - Play **C (Cooperate)**. Assume initial good faith.

2.  **Steady State (Rounds 2 to r-1):**
    - Calculate `last_round_cooperation_rate` = (observed_cooperators) / (n - 1).
    - If `last_round_cooperation_rate` ≥ 0.75:
        - Play **C**. The group is sufficiently cooperative to maintain or grow the stock.
    - If `0.50` ≤ `last_round_cooperation_rate` < 0.75:
        - Play **C** with probability `last_round_cooperation_rate`. This probabilistic approach signals willingness to cooperate while reducing exposure to exploitation.
    - If `last_round_cooperation_rate` < 0.50:
        - Play **D (Defect)**. If the majority defects, the stock is collapsing; individual cooperation is insufficient to save the resource and merely exhausts one's own potential payoff.

3.  **Terminal Phase (Final Round):**
    - If `history_cooperation_rate` ≥ 0.50:
        - Play **C**. Reward the long-term cooperative effort of the group.
    - Else:
        - Play **D**. The resource is already degraded or the group is inherently uncooperative; capture remaining value.

**Dynamic Adjustment (Edge Cases):**
- **Critical Depletion Trigger:** If the current stock `S` falls below `(capacity / (2*n))`, ignore the `last_round_cooperation_rate` and play **C** regardless, unless the strategy has already entered a terminal Defect state. This represents an "emergency preservation" mode to prevent total stock extinction.
- **Perfect Cooperation Reward:** If `last_round_cooperation_rate` is 1.0 (perfect cooperation) for three consecutive rounds, maintain **C** regardless of other conditions to lock in a sustainable, high-growth equilibrium.
'''

description_ALTRUISTIC_16 = '''
### Decision Logic

The core objective is to maximize sustainable yield while punishing aggressive defection to prevent total resource depletion. The strategy employs a conditional cooperation model that seeks equilibrium at full cooperation while tracking the "health" of the resource stock as the primary metric for strategy adjustment.

**State Variables:**
*   `S_t`: Stock at beginning of round $t$.
*   `D_t`: Number of defectors observed in round $t$.
*   `C_t`: Number of cooperators observed in round $t$.
*   `threshold`: The stock level required to support full cooperation safely (set to $0.5 \times \text{capacity}$).
*   `my_action`: The action taken by the agent.

#### Round 1
Play **Cooperate (C)**. This signals a commitment to sustainable resource management.

#### Round $t$ (where $t > 1$)
The agent evaluates the current stock and the behavior of the population in the previous round ($t-1$) to determine the current action.

1.  **Safety Check:** If the stock $S_t$ falls below $0.2 \times \text{capacity}$, play **Defect (D)**. This is a "rescue" move to extract remaining utility before the stock collapses entirely due to previous over-extraction.
2.  **Growth Monitoring:** If the stock $S_t$ is high ($> 0.8 \times \text{capacity}$) and the previous round's aggregate behavior was fully cooperative ($D_{t-1} = 0$), play **Cooperate (C)**.
3.  **Conditional Reciprocity (Tit-for-Tat variant):**
    *   Calculate the average defection rate: $DR = D_{t-1} / n$.
    *   If $DR > 0.5$ (the majority are defecting), play **Defect (D)**. This prevents being exploited while the pool is being depleted by others.
    *   If $DR \le 0.5$, play **Cooperate (C)**. This maintains altruistic support even if a minority is defecting, provided the stock is not in critical danger.

#### Final Round ($r$)
Regardless of history, if $S_r > 0$, play **Defect (D)**. Since there is no future round to benefit from stock growth, harvesting the maximum possible yield is the optimal altruistic choice to extract the remaining value from the common pool before the game ends.

### Pseudocode

```python
def get_action(round_num, total_rounds, current_stock, prev_round_defectors, n, capacity):
    
    # 1. Terminal Round
    if round_num == total_rounds:
        return 'D'
    
    # 2. Rescue Phase (Critical Stock)
    if current_stock < (0.2 * capacity):
        return 'D'
    
    # 3. Round 1 Default
    if round_num == 1:
        return 'C'
    
    # 4. Adaptive Cooperation
    defector_ratio = prev_round_defectors / n
    
    # If majority defects, punish/protect resources by defecting
    if defector_ratio > 0.5:
        return 'D'
    
    # Otherwise, maintain altruistic cooperation
    return 'C'
```
'''

description_ALTRUISTIC_17 = '''
The strategy follows a "Conditional Altruism with Sustainability Constraints" logic, aiming to maintain the resource at its capacity while penalizing defectors proportionally to the threat they pose to system stability.

**State Definitions:**
*   $S_t$: Stock at the beginning of round $t$.
*   $k_t$: Number of players who played $C$ in round $t-1$.
*   $m_t$: Number of players who played $D$ in round $t-1$ (where $m_t = n - k_t$).
*   $T$: Total rounds remaining (current round index $r - t + 1$).
*   $threshold$: A sustainability buffer (set to $0.2 \times capacity$).

**Decision Rules:**

1.  **Initialization (Round 1):**
    Always play $C$. This establishes a cooperative baseline and provides data on opponent behavior.

2.  **Sustainability Check:**
    If $S_t < threshold$, play $C$ regardless of previous actions. The system is too fragile to sustain any defection; preservation is the only priority.

3.  **Endgame Phase (Final 2 Rounds):**
    If $T \le 2$, play $D$. Because the future value of the stock drops to zero after the game ends, the rational altruist shifts to maximizing individual gain before the resource collapses, assuming other agents will do the same.

4.  **Adaptive Response (General Case):**
    If $S_t \ge threshold$ and $T > 2$:
    *   Calculate the "System Integrity Score" ($SIS$) based on the previous round's outcome.
    *   If $m_t$ (defectors in previous round) $= 0$: Play $C$. The system is healthy; continue to cooperate.
    *   If $m_t > 0$:
        *   Calculate the projected stock $S_{t+1}$ assuming all players continue the current pattern of defection ($m_t$).
        *   If the projected stock $S_{t+1}$ is trending toward depletion ($S_{t+1} < S_t$), play $C$ with a probability $P(C) = k_t / n$. This is a "forgiving" approach that maintains cooperation proportionally to the observed level of cooperation in the group.
        *   If $S_{t+1} \ge S_t$ (meaning the current stock levels are resilient to the defection), play $C$.

**Pseudocode:**

```python
def decide_action(S_t, k_prev, n, r, current_round, capacity):
    threshold = 0.2 * capacity
    remaining_rounds = r - current_round + 1
    
    # Endgame phase
    if remaining_rounds <= 2:
        return 'D'
    
    # Crisis management
    if S_t < threshold:
        return 'C'
    
    # Analyze previous round
    if current_round == 1:
        return 'C'
    
    # Pattern of behavior
    if k_prev == n:
        return 'C'
    
    # Adaptive response to defection
    m_prev = n - k_prev
    # Calculate projected next stock based on m_prev defectors
    # Total consumption = k_prev*(S_t/2n) + m_prev*(S_t/n)
    # S_rem = S_t - consumption
    # S_next = S_rem + (2 * S_rem * (1 - S_rem/capacity))
    
    consumption = (k_prev * (S_t / (2*n))) + (m_prev * (S_t / n))
    S_rem = max(0, S_t - consumption)
    S_next = min(capacity, S_rem + (2 * S_rem * (1 - S_rem/capacity)))
    
    if S_next >= S_t:
        return 'C' # System is resilient, continue cooperating
    else:
        # Probabilistic cooperation based on observed group adherence
        if random.random() < (k_prev / n):
            return 'C'
        else:
            return 'D'
```
'''

description_ALTRUISTIC_18 = '''
The strategy implements a "Conditional Tit-for-Tat with Resource Preservation" approach. It prioritizes long-term sustainable cooperation, pivoting to defection only to punish persistent exploiters or to recover resource levels when the stock is critically low.

**Definitions:**
*   $T_t$: Total number of cooperators in round $t$.
*   $C_{threshold}$: A parameter set to $\lceil n/2 \rceil$. If the number of cooperators falls below this, the resource is effectively being pillaged.
*   $S_t$: Current stock level at the start of round $t$.
*   $S_{crit}$: Critical stock level, defined as $0.2 \times capacity$. Below this, aggressive recovery is required.

**Strategy Logic:**

1.  **First Round ($t=1$):**
    Always play **Cooperate**.

2.  **Subsequent Rounds ($1 < t < r$):**
    *   **If $S_t < S_{crit}$:**
        Play **Cooperate**. (When resources are critically low, defection accelerates extinction; maintaining cooperation is the only path to survival).
    *   **Else (if $S_t \geq S_{crit}$):**
        *   **If $T_{t-1} \geq C_{threshold}$:**
            Play **Cooperate**. (The collective behavior supports sustainability).
        *   **Else ($T_{t-1} < C_{threshold}$):**
            Play **Defect**. (If a majority is exploiting the resource, you must consume your share to maximize individual payoff before the stock is exhausted, or to force a reset of the stock growth calculation).

3.  **Last Round ($t = r$):**
    Play **Defect** regardless of history or stock level. (Since there is no future benefit to maintaining the resource, the optimal altruistic act at the terminal point is to maximize your own final payout, as the common pool resource will not regenerate).

**Pseudocode:**

```python
def get_action(round_number, total_rounds, current_stock, prev_round_cooperators, n, capacity):
    # Terminal round: maximize final payoff
    if round_number == total_rounds:
        return "Defect"

    # Crisis management: protect the stock
    S_crit = 0.2 * capacity
    if current_stock < S_crit:
        return "Cooperate"

    # Standard strategy: reciprocal altruism
    threshold = (n + 1) // 2
    if prev_round_cooperators >= threshold:
        return "Cooperate"
    else:
        return "Defect"
```
'''

description_ALTRUISTIC_19 = '''
The altruistic objective is to maintain the stock at the capacity level to maximize long-term aggregate payoffs. The strategy employs a Tit-for-Tat variant with a "forgiveness" mechanism, conditioned on the current stock level and the recent aggregate behavior of opponents.

Let $C_t$ be the number of players who cooperated in round $t$.
Let $D_t$ be the number of players who defected in round $t$ ($D_t = n - C_t$).
Let $S_t$ be the stock at the start of round $t$.
Let $H_t$ be the history of $C$ counts for all previous rounds.

**Decision Logic:**

1.  **Initial Round ($t=1$):**
    Always play **Cooperate (C)**.

2.  **Subsequent Rounds ($t > 1$):**
    Play **Cooperate (C)** if *any* of the following conditions are met:
    *   $S_t \ge 0.8 \times \text{capacity}$: Cooperate to sustain the pool.
    *   The previous round's average cooperation rate ($C_{t-1}/n$) was $> 0.5$. This indicates sufficient goodwill to justify continued cooperation.
    *   The stock is recovering: $S_t > S_{t-1}$.

    Play **Defect (D)** if *all* of the following conditions are met:
    *   $S_t < 0.2 \times \text{capacity}$: The stock is critically depleted. Defection is necessary to extract remaining value before exhaustion.
    *   The previous round's cooperation rate ($C_{t-1}/n$) was $\le 0.5$.
    *   $t$ is within the final 2 rounds of the game ($t \ge r - 1$): In the terminal phase, if the stock is already depleted, rational extraction overrides altruistic preservation.

**Pseudocode:**

```python
def get_action(t, r, S, S_prev, C_prev, n):
    # Rule for Terminal phase or Critical depletion
    if (t >= r - 1 and S < 0.2 * capacity) or (S < 0.1 * capacity):
        return Defect

    # Rule for Maintenance
    if S >= 0.8 * capacity:
        return Cooperate

    # Rule for Reciprocity
    if C_prev / n > 0.5:
        return Cooperate
    
    # Rule for Recovery
    if S > S_prev:
        return Cooperate

    # Default
    return Defect
```

**Edge Cases:**
*   **$S_t = 0$:** If the stock reaches 0, the payoff is 0 regardless of action. The strategy treats this as a hard stop (Defect is forced by payoff mechanics).
*   **Rapid Depletion:** If the stock drops sharply ($S_t < 0.5 \times S_{t-1}$), prioritize Defect regardless of previous cooperation to hedge against the total collapse of the pool by aggressive opponents.
'''

description_ALTRUISTIC_20 = '''
**Strategy: Tit-for-Tat with Logistic Sustainability Threshold**

The strategy is defined by the objective to maintain the common pool stock at or near the capacity level to maximize long-term collective and individual payoffs, while punishing defectors proportionally to their impact on stock depletion.

**Decision Rules:**

1.  **Initial Round (t=1):** Play Cooperate (C). Assume a cooperative baseline to initiate mutual benefit.

2.  **Subsequent Rounds (t > 1):** Calculate the stock growth sustainability threshold.
    *   Let $k$ be the number of players who played $D$ in the previous round $t-1$.
    *   Let $S_{t-1}$ be the stock level at the start of round $t-1$.
    *   If $S_{t-1} < (\text{capacity} \times 0.25)$ (Critical Scarcity):
        *   Play Cooperate (C) regardless of history. When the stock is critically low, the priority is absolute preservation to prevent extinction.
    *   Else if $k = 0$ (All Cooperated):
        *   Play Cooperate (C). Maintain the steady state.
    *   Else if $k > 0$ (Defection Detected):
        *   Calculate the Expected Sustainability Index ($ESI$):
            $ESI = S_{t-1} - (\text{total consumption in } t-1) + \text{growth in } t-1$.
        *   If $ESI > (\text{capacity} \times 0.5)$:
            *   Play Defect (D) with probability $p = k/n$. This is a "Tit-for-Tat" adjustment: match the proportion of defection observed to signal disapproval without crashing the resource.
        *   If $ESI \leq (\text{capacity} \times 0.5)$:
            *   Play Cooperate (C). If the resource is being drained too quickly, revert to cooperation to preserve the stock, sacrificing individual payoff for collective survival.

3.  **Final Rounds (t = r):**
    *   If $S_{t-1} < (\text{capacity} \times 0.5)$:
        *   Play Cooperate (C). Do not extract maximum value if it risks long-term viability, even in the final round.
    *   Else:
        *   Play Defect (D). Since there is no future interaction, extract maximum utility from the resource.

**Pseudocode:**

```python
def decide_action(n, r, capacity, current_round, stock_history, opponents_history):
    if current_round == 1:
        return "C"
    
    # Check if this is the final round
    if current_round == r:
        if stock_history[-1] < (capacity * 0.5):
            return "C"
        else:
            return "D"
            
    # Assess sustainability
    prev_stock = stock_history[-1]
    k = opponents_history[-1] # Number of defectors
    
    # Calculate recovery stock dynamics
    cons_coop = prev_stock / (2 * n)
    cons_defect = prev_stock / n
    total_cons = (n - k) * cons_coop + k * cons_defect
    stock_remaining = prev_stock - total_cons
    growth = 2 * stock_remaining * (1 - stock_remaining / capacity)
    esi = min(stock_remaining + growth, capacity)
    
    # Critical Scarcity Check
    if prev_stock < (capacity * 0.25):
        return "C"
    
    # Strategy execution based on ESI
    if k == 0:
        return "C"
    elif esi > (capacity * 0.5):
        # Tit-for-Tat: Probabilistically mimic defectors
        if random.random() < (k / n):
            return "D"
        else:
            return "C"
    else:
        # Emergency sustainability: Stop defecting if growth is threatened
        return "C"
```
'''

description_ALTRUISTIC_21 = '''
Maintain a target stock level of *capacity* by prioritizing long-term sustainability. Define the strategy *Tit-for-Tat with Forgiveness and Sustainability Thresholds*.

**Core Decision Rule:**
In every round *t*, evaluate the current stock *S* and the average behavior of opponents in the previous round *t-1*.

1.  **Calculate Sustainability:** Determine if *S* is at or above the sustainability threshold. A "sustainable state" exists when *S* ≥ *capacity* / 2. If *S* is below this threshold, prioritize resource recovery.
2.  **Evaluate Opponent Cooperation:** Let *k* be the number of opponents who cooperated (played C) in the previous round.
3.  **Action Selection:**
    *   **If *t* = 1:** Play C. Starting with cooperation signals an intent for collective sustainability.
    *   **If *t* > 1 and *S* ≥ *capacity* / 2:** Play C if *k* ≥ (n-1) / 2 (majority or near-majority cooperation). If *k* < (n-1) / 2, play D for one round to buffer the stock level against the impending crash caused by excessive defection, then return to C in the next round.
    *   **If *t* > 1 and *S* < *capacity* / 2:** Play D regardless of opponent history. When the resource is depleted below 50% capacity, the system enters a high-risk state where individual defection is necessary to avoid being the only player harmed by the inevitable collapse, while simultaneously signaling the danger of the current trajectory.
    *   **If *t* = *r* (Final Round):** Play D. In the final round, there is no future stock to replenish. Since the game terminates, utility maximization dictates capturing the remaining resources.

**Pseudocode:**
```
function get_action(S, t, k, n, r, capacity):
    if t == r:
        return D
    if t == 1:
        return C
    
    threshold = capacity / 2
    
    if S >= threshold:
        if k >= (n - 1) / 2:
            return C
        else:
            return D
    else:
        return D
```

**Edge Case Handling:**
*   **Total Collapse (*S* ≈ 0):** If *S* drops near 0, the growth function *2 × S × (1 - S/capacity)* yields near-zero growth. In this state, the game is effectively over regardless of the round number. The strategy defaults to D to capture any remaining fractional utility before the final round.
*   **High Cooperation (k = n-1):** If all other players cooperate, the strategy will always cooperate (unless *S* < threshold, which should not occur if all players cooperate), maintaining the *capacity* equilibrium.
*   **High Defection (k = 0):** The strategy will default to D, essentially minimizing losses in a doomed common pool.
'''

description_ALTRUISTIC_22 = '''
This strategy employs a Conditional Reciprocity model combined with a Target State maintenance mechanism to maximize long-term social welfare. It prioritizes keeping the stock at the capacity level while rewarding cooperation and punishing persistent defectors.

### Strategy Parameters
*   **Target Stock Level ($S_{target}$):** Defined as $0.75 \times \text{capacity}$. This buffer zone prevents collapse due to unexpected aggregate defection while maintaining high yield.
*   **Cooperation Threshold ($\tau$):** The minimum fraction of opponents required to have cooperated in the previous round for the agent to continue cooperating. Set $\tau = 0.5$.
*   **Memory Depth ($m$):** The number of rounds to evaluate for trend analysis. Set $m = 3$.

### Decision Rules

1.  **Round 1:** Play **Cooperate (C)**. This signals a commitment to sustainable growth.
2.  **Rounds 2 to $r-1$:**
    *   **Stock Check:** If current stock $S \leq 0.1 \times \text{capacity}$, play **Defect (D)**. The resource is nearing extinction; maximize personal payoff before total collapse.
    *   **Reciprocity Logic:**
        *   Calculate the average cooperation rate $A$ of opponents over the last $m$ rounds.
        *   If $A \geq \tau$, play **Cooperate (C)**.
        *   If $A < \tau$, play **Defect (D)**. This switch functions as a "Grim Trigger" variant, withholding resources from non-cooperative peers to preserve the stock.
    *   **Restoration Adjustment:** Regardless of the reciprocity logic, if $S < S_{target}$, play **Cooperate (C)**. This prioritizes replenishment over punishment when the common pool is stressed.
3.  **Last Round ($r$):** Play **Defect (D)** regardless of state or history. Since there is no future utility in the resource, individual maximization is the only rational action.

### Pseudocode

```python
def get_action(round, stock, history, n):
    # Base Case: Last round
    if round == r:
        return D

    # Edge Case: Extreme depletion
    if stock <= 0.1 * capacity:
        return D
    
    # Restoration priority
    if stock < 0.75 * capacity:
        return C
    
    # Reciprocity Logic
    recent_history = history[-3:] 
    avg_cooperation = sum(recent_history) / (len(recent_history) * (n-1))
    
    if avg_cooperation >= 0.5:
        return C
    else:
        return D
```

### Edge Case Handling
*   **Initial Growth Lag:** If the system is in the first few rounds and the stock is below $S_{target}$, the strategy defaults to **C** to jumpstart the resource, ignoring opponent behavior.
*   **Recovery Phase:** If the pool has been depleted below $S_{target}$, the strategy reverts to **C** exclusively. This assumes that collective altruism is required to escape a low-resource trap, making punishment ineffective.
*   **Persistent Defection:** If opponents defect consistently, the strategy switches to **D** once $S \geq S_{target}$, protecting the agent's relative share until the resource naturally recovers or depletes below the $0.1$ collapse threshold.
'''

description_ALTRUISTIC_23 = '''
The strategy prioritizes long-term resource stability and collective yield maximization through conditional cooperation, shifting toward defect-only strategies only when the resource is exhausted or opponents unilaterally exploit cooperation.

### Core Logic
The strategy maintains a target stock level to ensure sustainability while attempting to induce mutual cooperation. If the resource is threatened by high aggregate consumption, it aggressively restricts usage to allow regeneration.

**State Variables:**
*   `C_count`: Number of opponents who cooperated in the previous round.
*   `S_prev`: Stock level at the start of the previous round.
*   `S_curr`: Stock level at the start of the current round.

### Decision Rules

1.  **Initial Round:**
    *   Always play **Cooperate (C)**.

2.  **Subsequent Rounds (t > 1):**
    *   **The Sustainability Threshold:** If `S_curr` < `capacity / 4`, play **Defect (D)**. At critical low levels, recovery is mathematically improbable if cooperation continues; defect to extract remaining value before the pool collapses.
    *   **The Tit-for-Tat Trigger:** If `C_count < (n - 1)`, play **Defect (D)**. If any opponent defects, punish the move by defecting for the subsequent round.
    *   **The Regeneration Check:** If `S_curr` is significantly lower than `S_prev` (specifically, `S_curr < S_prev * 0.8`), play **Defect (D)**. This detects if aggregate consumption in the previous round was too high to sustain growth, regardless of opponent counts, and forces a recovery phase.
    *   **The Cooperative Default:** If `S_curr >= capacity / 4`, `C_count == (n - 1)`, and `S_curr >= S_prev * 0.8`, play **Cooperate (C)**.

3.  **End-Game Strategy (Final Round):**
    *   If the current round index `t == r`, play **Defect (D)** regardless of history, as the future value of the stock is zero.

### Pseudocode Implementation

```python
def get_action(round_number, total_rounds, n, capacity, stock, prev_stock, prev_cooperators):
    # 1. End-game condition
    if round_number == total_rounds:
        return D

    # 2. Critical scarcity condition
    if stock < (capacity / 4):
        return D

    # 3. Regeneration failure check (if prev_stock is defined)
    if prev_stock is not None and stock < (prev_stock * 0.8):
        return D

    # 4. Cooperation enforcement
    if prev_cooperators is not None and prev_cooperators < (n - 1):
        return D

    # 5. Default to cooperation
    return C
```

### Edge Cases
*   **First Round:** Always cooperates to signal willingness to sustain the pool.
*   **Total Depletion:** If `S_curr` approaches 0, the Sustainability Threshold forces defection, maximizing extraction before the stock hits zero.
*   **High Cooperation, High Depletion:** If all opponents cooperate but the `S_curr` drops sharply due to previous rounds, the Regeneration Check forces a temporary switch to defection to allow the stock to recover naturally.
'''

description_ALTRUISTIC_24 = '''
The strategy adopts a Conditional Tit-for-Tat approach with a "Sustainability Threshold," prioritizing long-term stock replenishment over short-term gains. It interprets altruism as maximizing the total pool health to ensure sustainable consumption for all players, punishing defectors only when they threaten the survival of the resource.

**Core Decision Logic**

1.  **First Round:** Always play **C** (Cooperate). This signals an initial willingness to contribute to resource sustainability.

2.  **Subsequent Rounds:** Let $C_{prev}$ be the number of cooperators observed in the previous round (excluding self). Let $S_{prev}$ be the stock level at the start of the previous round.
    *   **Target Sustainability:** The goal is to keep $S \geq \text{capacity}/2$ to maximize the logistic growth function.
    *   **Observation Analysis:**
        *   If the previous round's stock was below a critical threshold (defined as $S < \text{capacity}/4$), switch to **C** to prevent collapse, regardless of opponent behavior.
        *   If $S \geq \text{capacity}/4$, evaluate opponent behavior:
            *   If $C_{prev} \geq \lfloor n/2 \rfloor$ (majority or half are cooperating), play **C**.
            *   If $C_{prev} < \lfloor n/2 \rfloor$, play **D** (Defect). This serves as a trigger-based pressure mechanism to force opponents toward cooperation by showing that defecting yields higher individual utility when the population is failing to coordinate.

3.  **End-Game (The "Shadow of the Future" Adjustment):**
    *   For the final $k$ rounds (where $k$ is defined by $r - t \le 3$), calculate the expected stock remaining.
    *   If $S < \text{capacity}/4$, play **C** to maximize the remaining utility for all.
    *   Otherwise, abandon the sustainability constraint and play **D** for the final round to capture remaining value before the game terminates, unless $C_{prev} = n-1$ (all others cooperated in the previous round), in which case play **C** to maintain the cooperative equilibrium until the end.

**Pseudocode Definition**

```python
def decide_action(round, total_rounds, n, capacity, current_stock, prev_cooperators):
    # Rule 1: First round
    if round == 1:
        return 'C'

    # Rule 3: End-game logic
    if round > (total_rounds - 3):
        if current_stock < (capacity / 4):
            return 'C'
        elif prev_cooperators == (n - 1):
            return 'C'
        else:
            return 'D'

    # Rule 2: Adaptive sustainability logic
    if current_stock < (capacity / 4):
        return 'C'
    
    # Conditional Cooperation
    if prev_cooperators >= (n // 2):
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling**
*   **Near-Total Depletion ($S \approx 0$):** If the stock drops below a critical point, the strategy enters "Recovery Mode," playing **C** unconditionally regardless of opponent history, as defecting in a collapsed system yields near-zero payoff for all players.
*   **Total Cooperation:** If all opponents cooperate, the strategy maintains **C** indefinitely to ensure the resource remains at maximum capacity.
*   **Total Defection:** If all opponents defect, the strategy shifts to **D** to capture the remaining stock before it disappears, then switches back to **C** if the system reset allows for recovery.
'''

description_ALTRUISTIC_25 = '''
The strategy follows a "Tit-for-Tat with Forgiveness and Resource Stewardship" logic, prioritizing sustainable long-term yields over immediate extraction.

### Strategy Logic
The strategy maintains a target cooperation level based on the observed behavior of the group in the previous round, while enforcing a hard safety threshold to prevent stock collapse.

**Pseudocode Definitions:**
*   `k`: Number of previous rounds.
*   `C_prev`: Number of cooperators in round `k-1` (including self).
*   `S_prev`: Stock level at start of round `k-1`.
*   `S_curr`: Stock level at start of current round.
*   `threshold`: A sustainability trigger set to `capacity * 0.25`.

### Decision Rules

**Round 1:**
*   Always play **C**. This signals willingness to cooperate and maintains initial stock levels.

**Rounds 2 to r-1:**
1.  **Stock Safety Check:** If `S_curr < threshold`, play **D** with probability 0.5 and **C** with probability 0.5. This aims to maximize individual payoff while the resource is already in a critical state.
2.  **Adaptive Reciprocity:** If `S_curr >= threshold`, count the number of cooperators from the previous round (`C_prev`).
    *   If `C_prev` ≥ `n/2` (the majority cooperated), play **C**.
    *   If `C_prev` < `n/2`, play **D** to avoid exploitation.
3.  **Forgiveness:** If `S_curr` is trending upward (i.e., `S_curr > S_prev`), play **C** regardless of previous defection, provided `S_curr > threshold`. This encourages a return to sustainable equilibrium if opponents have begun cooperating again.

**Final Round (r):**
*   If `S_curr > threshold`, play **C**.
*   If `S_curr <= threshold`, play **D**. This maximizes final payoff when the resource is already depleted and future growth is irrelevant.

### Operational Pseudocode

```python
def get_action(round, n, S_curr, S_prev, C_prev, threshold):
    if round == 1:
        return 'C'
    
    if round == r:
        return 'C' if S_curr > threshold else 'D'
    
    # Critical state management
    if S_curr <= threshold:
        return random_choice(['C', 'D'])
    
    # Reciprocal cooperation logic
    if C_prev >= (n / 2):
        return 'C'
    
    # Recovery logic: if stock is growing, forgive defection
    if S_curr > S_prev:
        return 'C'
        
    return 'D'
```
'''

description_ALTRUISTIC_26 = '''
The strategy employs a "Conditional Sustainability" approach, prioritizing the long-term regeneration of the stock while maintaining a mechanism to punish exploitation. The core logic is to cooperate if the stock is healthy or recovering, but defect if the pool is being depleted by others, scaling the response based on the observed collective action.

### Decision Rules

**Round 1:**
Always play **C**. Establish trust.

**Round t (where t > 1):**
Define `observed_cooperators` as the number of players who played C in round `t-1`.
Define `is_depleting` as true if the current stock `S` is less than 50% of `capacity` OR if the stock in `t-1` was strictly greater than the stock in `t` (indicating negative growth).

1.  **Cooperate (C)** if:
    *   `observed_cooperators` > (n/2), OR
    *   `S` is greater than or equal to 75% of `capacity`.

2.  **Defect (D)** if:
    *   `observed_cooperators` < (n/2), OR
    *   (`is_depleting` is true AND `observed_cooperators` <= (n/2)).

### The "Altruistic Buffer" Adjustment
If `r - t < 3` (the final three rounds), ignore the `is_depleting` check and instead play **D** only if the stock is already below 10% of `capacity`. Otherwise, play **C** to ensure the common good is preserved until the game's termination, as the future value of the stock drops to zero, and the incentive to conserve diminishes.

### Pseudocode

```python
def get_action(round_num, total_rounds, n, capacity, current_stock, prev_stock, observed_cooperators):
    # Final phase: maximize payoff while minimizing exhaustion
    if (total_rounds - round_num) < 3:
        if current_stock < (0.1 * capacity):
            return D
        else:
            return C

    # Standard phase
    growth_trend = (current_stock < prev_stock)
    
    # Cooperative threshold
    if observed_cooperators > (n / 2) or current_stock >= (0.75 * capacity):
        return C
    
    # Punitive/Defensive threshold
    if observed_cooperators < (n / 2) or (growth_trend and observed_cooperators <= (n / 2)):
        return D
        
    return C
```

### Strategic Intent
This strategy functions as a modified "Tit-for-Tat" that incorporates a threshold-based sustainability check. It is altruistic because it explicitly prioritizes replenishing the stock (when `S >= 0.75 * capacity`) even if others are defecting, and it attempts to coordinate with a majority of cooperators to stabilize the system. It only resorts to defection when the pool is being actively destroyed by a majority of the group or when the growth trend is negative, serving as a defensive measure to ensure the altruist is not the sole entity bearing the cost of consumption while others deplete the resource.
'''

description_ALTRUISTIC_27 = '''
### Altruistic Sustainability Strategy

The strategy prioritizes maximizing the total sustainable yield of the pool over the game's horizon, rather than maximizing individual payoff. It employs a conditional "tit-for-tat with forgiveness" logic based on the observed aggregate cooperation level, adjusted for the pool's health.

**Core Heuristic:**
Maintain the pool stock ($S$) as close to $capacity/2$ as possible. This level ($S = capacity/2$) maximizes the growth function $2 \times S \times (1 - S/capacity)$.

**Decision Logic (per round $t$):**

1.  **Initialization ($t=1$):**
    Always play **C**.

2.  **Standard Rounds ($t > 1$):**
    Calculate the desired aggregate consumption $C_{target}$ to maintain or move toward the optimal stock level ($S^* = capacity/2$).
    
    *   If $S_{t} > S^*$, the system can tolerate slightly higher consumption.
    *   If $S_{t} < S^*$, the system requires strict conservation.

    Let $n_c$ be the number of cooperators observed in round $t-1$. Let $S_t$ be the current stock.
    Define "Cooperation Threshold" $T$ as $n \times 0.5$ (or $\lceil n/2 \rceil$).

    *   **If $S_t \ge capacity/4$:**
        Play **C** if $n_c \ge T$. If $n_c < T$, play **D** for one round as a signal of intolerance for over-extraction (punishment), then revert to **C** in $t+1$ regardless of the outcome (forgiveness).

    *   **If $S_t < capacity/4$:**
        Prioritize extreme conservation. Play **C** regardless of opponent behavior to prevent stock collapse.

3.  **Terminal Phase ($t \approx r$):**
    As $t$ approaches $r$, the future value of the stock diminishes.
    
    *   If $t = r$:
        Play **D** to extract final value, unless $S_t$ is already extremely low (near 0), in which case play **C** as a symbolic final act.
    *   If $r - t \le 2$:
        Switch to **D** if $n_c$ was consistently high in previous rounds, or if the stock is high enough that defection will not deplete the pool to 0 before the final round. Otherwise, maintain **C**.

**Pseudocode Implementation:**

```python
def choose_action(round, total_rounds, n, stock, capacity, last_round_cooperators):
    # Terminal phase logic
    if round == total_rounds:
        return 'D' if stock > 0 else 'C'
    
    if (total_rounds - round) <= 2:
        if last_round_cooperators >= (n / 2):
            return 'D'
        return 'C'

    # Standard strategy logic
    optimal_stock = capacity / 2
    threshold = n / 2

    if stock < (capacity / 4):
        # Emergency recovery mode
        return 'C'
    
    # Tit-for-Tat with Forgiveness
    # If the previous round saw cooperative behavior, continue cooperating.
    # If the previous round was defective, punish for one round.
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_ALTRUISTIC_28 = '''
Play Cooperate (C) in the first round.

For all subsequent rounds $t > 1$, determine action based on the observation of the total number of cooperating players in round $t-1$, denoted as $k_{t-1}$:

1.  **Cooperation Threshold:** If the observed average cooperation rate in previous rounds is consistently high, continue to cooperate. Specifically, define a tolerance threshold $T$ based on the number of defectors allowed. If $k_{t-1} \ge n - \text{tolerance}$, play C.
    *   Set initial tolerance to 0 (Tit-for-Tat baseline).
    *   If $k_{t-1} < n$, increment tolerance by 1 for future rounds, up to a maximum tolerance of $\lfloor n/2 \rfloor$. This allows for occasional noise or accidental defection without collapsing into a permanent defect cycle.

2.  **Punishment/Defection Rule:** If the current stock $S_t$ falls below a critical threshold $S_{crit} = \text{capacity} / 2$, and the number of defectors in the previous round was greater than the current tolerance, switch to Defect (D) for one round to signal the unsustainable trajectory, then revert to Cooperate (C) immediately.

3.  **Terminal Phase:** In the final round $r$, always play Defect (D) only if the stock $S_r$ is insufficient to support sustained cooperative play beyond the current round (i.e., if $S_r$ is low enough that the resource is likely to collapse regardless of current round action). Otherwise, prioritize cooperation to maximize the long-term utility of the pool.

4.  **Recovery:** If the stock $S_t$ is approaching capacity ($S_t > 0.9 \times \text{capacity}$), strictly prioritize C regardless of past defections to encourage collective renewal.

Pseudocode:
```python
tolerance = 0
if round == 1:
    return C
elif round == r:
    if stock < (capacity * 0.1): 
        return D
    else:
        return C
else:
    # Observe k: number of cooperators in round t-1
    if k >= (n - tolerance):
        return C
    else:
        # Trigger temporary punishment if stock is dangerously low
        if stock < (capacity / 2):
            tolerance = min(tolerance + 1, n // 2)
            return D
        else:
            return C
```
'''

description_ALTRUISTIC_29 = '''
The strategy follows a conditional "Tit-for-Tat with Forgiveness" approach, optimized to sustain the resource pool while incentivizing cooperation.

**State Variables:**
- `prev_stock`: Stock at the start of the previous round.
- `my_history`: List of my past actions.
- `others_history`: List of total cooperation counts per round by opponents.
- `cooperation_threshold`: A dynamic parameter calculated as $n/2$ (the minimum number of cooperators required to keep stock stable or growing, assuming average conditions).

**Decision Logic:**

1.  **Round 1:** Play **C**.

2.  **Round 2 to r-1:**
    *   **Observation:** Identify the number of cooperators in the previous round ($C_{prev}$).
    *   **Regret/Reciprocity Rule:** If $C_{prev} \ge$ `cooperation_threshold`, play **C**.
    *   **Punishment/Correction Rule:** If $C_{prev} <$ `cooperation_threshold`, play **D** with probability $P$, where $P = (n - C_{prev})/n$. This probability scales the harshness of the response to the level of defection observed.
    *   **Forgiveness:** If $C_{prev} <$ `cooperation_threshold` but the current `stock` is below 25% of `capacity`, play **C** regardless of opponent behavior to prevent total collapse.

3.  **Final Round (Round r):**
    *   If $C_{r-1} \ge$ `cooperation_threshold`, play **C**.
    *   If $C_{r-1} <$ `cooperation_threshold`, play **D**. (This prevents exploitation in the terminal round while maintaining the cooperative equilibrium if it was already established).

**Pseudocode Implementation:**

```python
def choose_action(round_num, r, n, current_stock, capacity, history):
    # Base Case: Always cooperate on first round
    if round_num == 1:
        return 'C'
    
    # Terminal Round: Reward cooperation, protect against defection
    if round_num == r:
        if history.last_round_cooperators >= (n / 2):
            return 'C'
        else:
            return 'D'

    # Standard Rounds
    # If stock is critically low, always cooperate to rebuild
    if current_stock < (0.25 * capacity):
        return 'C'
    
    # Calculate threshold for sustainability
    threshold = n / 2
    
    # Reciprocal Logic
    if history.last_round_cooperators >= threshold:
        return 'C'
    else:
        # Probabilistic punishment based on severity of defection
        # More defections lead to a higher likelihood of playing D
        defection_count = n - history.last_round_cooperators
        if random_float() < (defection_count / n):
            return 'D'
        else:
            return 'C'
```
'''

description_ALTRUISTIC_30 = '''
### Core Strategy: Adaptive Sustainability Tit-for-Tat

The strategy prioritizes the maintenance of the common pool stock at the capacity level to maximize long-term aggregate yield, while punishing defection to prevent resource depletion.

**Decision Rules:**

1.  **Initialization (Round 1):** Play Cooperate (C). Assume a baseline of cooperation to initiate a virtuous cycle.

2.  **Tracking and State Awareness:**
    *   Let $N_c$ be the number of players who played Cooperate in the previous round ($t-1$).
    *   Let $S_t$ be the stock at the start of round $t$.
    *   Define a "Sustainability Threshold" $T_S = 0.5 \times \text{capacity}$. If $S_t < T_S$, the resource is in a critical state.

3.  **Round $t$ Decision logic:**
    *   **If $t = r$ (Last Round):** Play Defect (D). Since there is no future to protect, individual payoff maximization without negative externalities on future stock is the rational conclusion for the final round.
    *   **If $S_t < (S_{t-1} \times 0.2)$:** Play Defect (D). If the stock has crashed unexpectedly, prioritize immediate recovery of remaining value.
    *   **If $N_c = n$:** Play Cooperate (C). Everyone is contributing to sustainability; maintain the equilibrium.
    *   **If $N_c < n$:**
        *   Calculate the Expected Sustainability (ES). If playing Cooperate leads to a predicted stock $S_{t+1} > S_t$, play Cooperate (C).
        *   Otherwise, play Defect (D) to match the behavior of the majority and mitigate the "sucker's payoff," but revert to C if the stock recovers above $T_S$ in the subsequent round.

**Pseudocode:**

```python
def decide_action(round, total_rounds, n, capacity, current_stock, prev_stock, prev_cooperators):
    
    # 1. Terminal condition
    if round == total_rounds:
        return "D"
    
    # 2. Critical depletion check
    if current_stock < (prev_stock * 0.2):
        return "D"
        
    # 3. Collaborative enforcement
    if prev_cooperators == n:
        return "C"
    
    # 4. Adaptive Sustainability
    # Calculate stock remaining if I cooperate
    # My consumption = current_stock / (2n)
    # Others consumption = prev_cooperators * (current_stock / (2n)) 
    #                    + (n - prev_cooperators) * (current_stock / n)
    
    my_cons_C = current_stock / (2 * n)
    others_cons = (prev_cooperators * (current_stock / (2 * n))) + \
                  ((n - prev_cooperators) * (current_stock / n))
    
    remaining_stock = current_stock - my_cons_C - others_cons
    growth = 2 * remaining_stock * (1 - remaining_stock / capacity)
    projected_next_stock = min(remaining_stock + growth, capacity)
    
    if projected_next_stock > current_stock:
        return "C"
    else:
        return "D"
```

**Altruistic Rationale:**
This strategy is altruistic because it sacrifices potential short-term gains (D) for the explicit purpose of sustaining the common pool, which benefits all players equally over the duration of the game. It treats the pool as a collective asset, utilizing "tit-for-tat" logic to encourage group cooperation while safeguarding against exploitation by defectors. By linking the decision to cooperate directly to the sustainability of the pool ($S_{t+1} > S_t$), the strategy enforces a normative expectation of stewardship.
'''

description_ALTRUISTIC_31 = '''
The strategy, "Altruistic Tit-for-Tat with Resource Preservation," operates on the principle of conditionally sustained cooperation while prioritizing the long-term stability of the common pool. It employs a trigger mechanism based on the stock growth potential and historical cooperation levels.

### Decision Logic

**Round 1:**
Cooperate (C).

**Subsequent Rounds:**
Define $k$ as the number of opponents who cooperated in the previous round.
Define $S_{t-1}$ as the stock level at the start of the previous round.

1.  **Growth Preservation Rule:** If $S_{t-1} \times (1 - \frac{S_{t-1} - \text{Total Consumption}_{t-1}}{\text{capacity}}) < \text{Threshold}_C$, defect (D) immediately to protect individual utility before the pool collapses, where $\text{Threshold}_C$ is calculated as the expected growth if everyone cooperates.
2.  **Conditional Cooperation (Tit-for-Tat variant):** If the stock is above a critical depletion level (defined as $S_{t-1} < 0.2 \times \text{capacity}$), defect (D) to maximize personal utility before the pool hits zero.
3.  **Reciprocity:** If the stock is healthy ($S_{t-1} \geq 0.2 \times \text{capacity}$), play C if $k \geq \lceil \frac{n-1}{2} \rceil$ (a majority of opponents cooperated in the previous round). If $k < \lceil \frac{n-1}{2} \rceil$, play D.

### Edge Cases

*   **Final Round:** If $t = r$, play Defect (D) regardless of history, as there is no future rounds to influence via reputation or growth.
*   **Near-Zero Stock:** If $S < \epsilon$ (where $\epsilon$ is a minimal threshold, e.g., $1.0$), play Defect (D) because the resource is effectively exhausted and cannot recover.
*   **Sudden Collapse:** If the observed stock drops below the level required for sustainable growth (calculated as $S_{remaining} \approx 0.5 \times \text{capacity}$), switch to Defect (D) for one round to buffer personal losses, then return to the conditional reciprocity rule if the stock recovers.

### Pseudocode

```python
def decide_action(t, r, n, stock, capacity, history):
    # Rule 1: Terminal round exhaustion
    if t == r:
        return 'D'

    # Rule 2: Critical depletion protection
    if stock < (0.2 * capacity):
        return 'D'

    # Rule 3: Initial round altruism
    if t == 1:
        return 'C'

    # Rule 4: Reciprocal Altruism
    # Observe previous round cooperation count (k)
    k = history[-1].cooperators_count
    
    # Requirement for cooperation: Majority of opponents must cooperate
    if k >= ceil((n - 1) / 2):
        return 'C'
    else:
        return 'D'
```
'''

description_ALTRUISTIC_32 = '''
Implement a "Conditional Sustainable Tit-for-Tat" strategy.

**Strategy Logic**

1.  **Initialization:** In Round 1, play C (Cooperate).

2.  **Round-by-Round Decision Rule:** For every round $t > 1$, calculate the "Sustainability Threshold." If the stock at the start of the previous round ($S_{t-1}$) was greater than or equal to $0.8 \times \text{capacity}$, cooperation is viable. If $S_{t-1} < 0.8 \times \text{capacity}$, the resource is degrading significantly; play D (Defect) to maximize immediate utility before the stock collapses.

3.  **Cooperation Maintenance:** If cooperation is viable (based on the threshold above), evaluate the collective behavior from the previous round $t-1$:
    *   If the number of defectors in $t-1$ was zero, continue to play C.
    *   If the number of defectors in $t-1$ was greater than zero, play D for the current round to punish the exploitation.
    *   If you played D due to a punishment in the previous round, switch back to C in the current round only if the stock level has recovered to at least $0.5 \times \text{capacity}$.

4.  **Terminal Phase:** In the final round ($t=r$), if the stock level $S_r \geq 0.5 \times \text{capacity}$, play C. If $S_r < 0.5 \times \text{capacity}$, play D.

**Pseudocode**

```python
def get_action(round_number, n, capacity, current_stock, history):
    # history stores: [last_stock, last_defectors_count, last_my_action]
    
    # Round 1 default
    if round_number == 1:
        return 'C'
    
    # Terminal phase logic
    if round_number == r:
        return 'C' if current_stock >= (0.5 * capacity) else 'D'
        
    last_stock, last_defectors_count, last_my_action = history
    
    # Resource preservation check
    if last_stock < (0.8 * capacity):
        return 'D'
    
    # Tit-for-tat logic
    if last_defectors_count > 0:
        # If I was punishing, check if recovery is sufficient to resume cooperation
        if last_my_action == 'D' and current_stock >= (0.5 * capacity):
            return 'C'
        else:
            return 'D'
            
    return 'C'
```
'''

description_BENEVOLENT_5 = '''
Adopt a "Conditional Sustainability" strategy, designed to maintain the common pool resource at its maximum regenerative capacity while minimizing the risk of exploitation.

**Decision Rules:**

In each round *t*, let *n* be the total number of players, *S* be the current stock, and *C_observed* be the number of cooperators observed in round *t-1* (excluding self).

1.  **Target State**: Maintain the stock *S* as close to *capacity / 2* as possible. This point maximizes the growth function (2 × S_rem × (1 - S_rem/capacity)).
2.  **Cooperation Trigger**:
    *   If *t = 1*: Cooperate.
    *   If *t > 1*: Calculate the "Sustainability Ratio," *R = (C_observed + 1) / n*.
    *   If *S < (capacity / 4)*: Defect. The resource is in critical decline; prioritize immediate capture before exhaustion.
    *   If *S >= (capacity / 4)* and *R >= 0.5*: Cooperate. Reward the group for maintaining sustainability.
    *   If *S >= (capacity / 4)* and *R < 0.5*: Defect. Treat the group as non-cooperative; minimize further loss to the pool by extracting a larger share.
3.  **Last Round Exception**:
    *   If *t = r*: Defect. There is no future potential for growth, rendering cooperation unsustainable.

**Pseudocode:**

```python
def get_action(round, total_rounds, n, stock, capacity, cooperators_prev_round):
    # Terminal round logic
    if round == total_rounds:
        return 'D'
    
    # First round logic
    if round == 1:
        return 'C'
    
    # Critical threshold check
    if stock < (capacity / 4):
        return 'D'
    
    # Cooperative threshold calculation
    # cooperators_prev_round is the count of others who cooperated
    # We define our own cooperation as index 1 for the ratio calculation
    if cooperators_prev_round >= (n / 2) - 1:
        return 'C'
    else:
        return 'D'
```

**Benevolence Implementation:**

The strategy is benevolent by prioritizing the sustainability of the common pool above immediate personal gain, provided that other players exhibit a minimal baseline of cooperation. By using a tit-for-tat derivative (the Sustainability Ratio), it protects the collective good from over-extraction while remaining robust against defectors by refusing to sacrifice resources when others are depleting the pool. It defaults to cooperation in the first round to signal intent and resets to extraction in the final round to prevent being exploited by actors who do not value the future of the pool.
'''

description_BENEVOLENT_6 = '''
The strategy, "Resilient Sustainability," follows a conditional cooperation protocol designed to maintain the common pool at its carrying capacity while minimizing vulnerability to defectors.

### Core Decision Rule

Let $k_t$ be the number of players who chose $C$ in round $t-1$. Your action at round $t$ is determined by the following logic:

1.  **If $t=1$:** Play $C$.
2.  **If $t > 1$:**
    *   Calculate the "Stability Threshold" $T = n - 1$.
    *   If $k_{t-1} \geq T$ (meaning all or all-but-one played $C$ previously), play $C$.
    *   If $k_{t-1} < T$ (meaning two or more players defected), play $D$.

### Handling Special Cases and Dynamics

*   **Recovery Phase:** If the strategy enters the $D$ state due to observed mass defection, it must actively transition back to cooperation to restore the common pool. If you are in the $D$ state, play $C$ if the stock $S_t \geq \text{capacity} \times 0.5$. This threshold ensures that the pool is sufficiently robust to sustain a return to cooperative play without collapsing immediately upon the resumption of shared consumption.
*   **The Final Round:** In the round $t=r$, play $D$ if the current stock $S_r \geq \text{capacity} \times 0.25$, otherwise play $C$. This prevents "sucker's payoff" exploitation in the final round while maintaining sustainability if the resource is already nearing exhaustion.
*   **Low Stock Sensitivity:** Regardless of historical observations, if $S_t < \text{capacity} / n$, play $C$ unconditionally for the remainder of the game. When the resource is at imminent risk of collapse, the priority shifts entirely to collective preservation to ensure the game continues.

### Pseudocode Representation

```python
def decide_action(round, stock, capacity, n, history_k):
    # History_k is a list of the number of cooperators in previous rounds
    
    # 1. Immediate Survival Protocol
    if stock < (capacity / n):
        return 'C'
        
    # 2. Final Round Logic
    if round == r:
        return 'D' if stock >= (capacity * 0.25) else 'C'
        
    # 3. First Round Initialization
    if round == 1:
        return 'C'
        
    # 4. Conditional Cooperation / Recovery Logic
    last_round_cooperators = history_k[-1]
    threshold = n - 1
    
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        # Check if we should exit Defect state for Recovery
        if stock >= (capacity * 0.5):
            return 'C'
        else:
            return 'D'
```
'''

description_BENEVOLENT_7 = '''
**Strategy: Adaptive Sustainable Tit-for-Tat (ASTFT)**

The strategy operates on the principle of conditionally cooperative sustainability. It aims to maintain the common pool at its optimal regeneration capacity ($S \approx capacity/2$, where growth is maximized) while punishing defectors only when they threaten the stock level's viability.

**1. Definitions and Initialization**
*   **Target Stock ($S_{target}$):** $capacity / 2$.
*   **Defection Threshold ($k$):** Let $c_t$ be the number of players who chose $C$ in the previous round. The strategy tracks the aggregate behavior.
*   **History:** Maintain a list of the number of cooperators observed in each round $t$: $H = [c_1, c_2, ..., c_{t-1}]$.

**2. Decision Rules**
For each round $t \in \{1, \dots, r\}$:

*   **First Round ($t=1$):** Always play $C$. This establishes a cooperative baseline.

*   **Subsequent Rounds ($t > 1$):**
    *   **Condition A (Stock Safety):** If $S_t < (capacity / n)$, the stock is critically low. Play $C$ regardless of previous history to attempt recovery.
    *   **Condition B (Trigger Strategy):** If $S_t \ge (capacity / n)$:
        *   Calculate the average cooperation rate of opponents from the previous round: $\bar{c}_{t-1} = (c_{t-1} - 1_{my\_last\_move=C}) / (n - 1)$.
        *   If $\bar{c}_{t-1} > 0.5$ (or if $n=2$ and opponent played $C$): Play $C$.
        *   If $\bar{c}_{t-1} \le 0.5$: There is a defection trend. Play $D$ with probability $P(D) = 1 - \bar{c}_{t-1}$ (Mixed strategy to signal dissatisfaction while maintaining partial cooperation) or play $D$ if the defection is severe ($c_{t-1} < n/2$).

*   **Final Round ($t = r$):**
    *   If $S_r \ge (capacity / 2)$: Play $C$ to maximize the final collective payout.
    *   If $S_r < (capacity / 2)$: Play $D$. Since there is no future round to recoup, extract the remaining utility.

**3. Edge Cases**
*   **Extinction Risk ($S \to 0$):** If the stock falls to a level where the total consumption of even one $D$ player would result in 0 or near-0 stock for the next round (i.e., $S \le capacity / (2n)$), play $C$ exclusively to minimize further depletion.
*   **Recovery Phase:** If the stock is below $S_{target}$ but increasing, prioritize $C$ to accelerate growth back to the equilibrium point, even if previous rounds showed defection.
*   **Full Cooperation:** If all players cooperate ($c = n$) for two consecutive rounds, increase the "forgiveness" threshold for the next round, ignoring a single defector to encourage a return to equilibrium without entering a punishment cycle.

**Pseudocode for Decision at round $t$:**

```python
def decide_action(S, t, n, capacity, history):
    if t == 1: return C
    if t == r: return C if S >= (capacity / 2) else D
    
    # Critical state check
    if S < (capacity / n):
        return C
    
    # Observe opponents
    last_c = history[-1]
    opponents_cooperating = last_c - (1 if my_last_move == C else 0)
    fraction_coop = opponents_cooperating / (n - 1)
    
    # Tit-for-tat logic
    if fraction_coop >= 0.5:
        return C
    else:
        # Benevolent punishment: Defect partially proportional to opponent defection
        return D if random() < (1 - fraction_coop) else C
```
'''

description_BENEVOLENT_8 = '''
The strategy employs a "Conditional Sustainability" mechanism, which seeks to maximize the long-term stock level while punishing defection only when necessary to preserve system viability. The strategy tracks the running average of cooperation observed in previous rounds and adjusts its own propensity to cooperate based on the current stock level and the perceived aggregate behavior of opponents.

**Decision Rules:**

In any round *t*, let *S* be the current stock, *n* be the number of players, and *k* be the number of other players who cooperated in the previous round *t-1*. Define the "Sustainability Threshold" *T* = 0.5 * capacity.

1. **Initialization (Round 1):**
   Always play **C**.

2. **Standard Play (Rounds 2 to r-1):**
   - If *S* > *T*:
     Play **C**.
   - If *S* ≤ *T*:
     Calculate the "Cooperation Index" *I* = *k / (n-1)*.
     - If *I* ≥ 0.5:
       Play **C** (assuming opponents are generally cooperative, proceed with trust).
     - If *I* < 0.5:
       Play **D** (a defensive measure to recoup immediate utility if the resource is collapsing due to widespread defection).

3. **Terminal Play (Round *r*):**
   - If *S* > (capacity / *n*):
     Play **C** to maintain the benevolent equilibrium until the final moment.
   - If *S* ≤ (capacity / *n*):
     Play **D**, as the resource is insufficient to sustain future growth and the game ends, rendering future-oriented cooperation moot.

**Edge Cases and Adjustments:**

*   **Sudden Depletion:** If *S* drops below 10% of *capacity*, prioritize survival. If *S* is < 10% of *capacity* regardless of the round number, switch to **D** to prevent total resource extinction, unless *I* (from the previous round) was 1.0 (indicating total group cooperation), in which case continue to play **C** to attempt collective recovery.
*   **Zero Stock:** If *S* = 0, play **D** (as all actions yield zero payoff).
*   **Perfect Cooperation:** If at any point the average cooperation index *I* has been 1.0 for three consecutive rounds, override the threshold *T* and always play **C** until *S* falls below 20% of capacity.
'''

description_BENEVOLENT_9 = '''
The strategy, titled "Sustainable Tit-for-Tat with Resilience Buffer," aims to maintain the common pool at maximum capacity while penalizing defectors proportionally to their threat level. The strategy maintains a history of cooperation levels observed in previous rounds to calibrate future responses.

### State Tracking
Maintain a variable `observed_C` representing the count of opponents who cooperated in the previous round, and a variable `reputation` (initially set to 1.0) representing the moving average of cooperation levels, where 1.0 is full cooperation and 0.0 is full defection.

### Decision Rules
In any given round $t$, where $S$ is the current stock:

1. **Calculate Target Cooperation:**
   If $t = 1$, play **C**.

2. **Calculate Response:**
   If $t > 1$:
   - Update `reputation`: `reputation = (0.7 * reputation) + (0.3 * (observed_C / (n - 1)))`.
   - Determine threshold for cooperation: If `reputation` ≥ 0.6, play **C**.
   - If `reputation` < 0.6, play **D** to protect against resource exhaustion caused by aggregate defection.

3. **Last Round Adaptation:**
   If $t = r$:
   - Play **D** regardless of `reputation`. Since this is the terminal round, the resource cannot regenerate, and conserving stock provides no future utility. Maximizing immediate payoff is the rational choice to prevent "sucker" losses if opponents defect in the final round.

4. **Resource Criticality Override:**
   Regardless of the `reputation` metric, if current stock $S < (\text{capacity} / n)$:
   - Play **C**. When the stock is critically low, defecting ($D$) accelerates total collapse for all players. Cooperating ($C$) minimizes individual draw, allowing the maximum potential for the remaining stock to regenerate in the next round.

### Pseudocode
```python
def get_action(round, n, S, capacity, observed_C):
    # Terminal round: extract value
    if round == r:
        return D
    
    # Resource criticality: protect the seed
    if S < (capacity / n):
        return C
    
    # First round: initiate trust
    if round == 1:
        return C
    
    # Adaptive thresholding
    # reputation tracks weighted moving average of opponent cooperation
    reputation = (0.7 * reputation) + (0.3 * (observed_C / (n - 1)))
    
    if reputation >= 0.6:
        return C
    else:
        return D
```
'''

description_BENEVOLENT_10 = '''
The strategy utilizes a "Tit-for-Tat with Forgiveness and Resource Awareness" approach, designed to maintain the common pool at its maximum sustainable capacity while punishing defections proportionally.

**Decision Rules:**

In any given round $t$, calculate the *Sustainable Cooperation Threshold* based on the observed stock $S_t$ and the number of players $n$. Cooperation is defined as choosing action $C$.

1.  **Initialization (Round 1):** Always play $C$.

2.  **State Assessment:** In rounds $t > 1$, evaluate the average cooperation level of the group in the previous round ($t-1$). Let $c_{t-1}$ be the number of players who chose $C$ in the previous round.
    *   If $S_{t-1} \approx 0$, assume a regime of total collapse or aggressive defection; revert to $D$ to secure remaining resources until replenishment, or switch to $C$ only if the system shows signs of recovery (i.e., $S_t > S_{t-1}$).
    *   If $S_t < \frac{capacity}{2}$, prioritize stock preservation. Play $C$ regardless of previous round outcomes to catalyze the logistic growth function.

3.  **Conditional Cooperation (Trigger Strategy):**
    *   If $S_t \ge \frac{capacity}{2}$, match the previous cooperation level. Specifically, define the cooperation threshold $k = \frac{n}{2}$.
    *   If $c_{t-1} \ge k$, play $C$.
    *   If $c_{t-1} < k$, play $D$ to protect individual returns against exploitation, as the pool is being depleted faster than sustainable limits.

4.  **Forgiveness and Recovery:**
    *   If playing $D$ due to low cooperation, observe the stock levels in the subsequent round. If the stock $S$ increases toward the $capacity$, immediately resume playing $C$ in the following round, even if $c_{t-1}$ was low. This resets the mechanism to encourage cooperative equilibrium.

**Edge Cases:**

*   **Final Round ($t = r$):** Defect ($D$) if the aggregate cooperation history shows that the average $c_t < n-1$ across the game duration, as the incentive for long-term sustainability vanishes. If the group has maintained $c_t = n$ (full cooperation) for the duration of the game, play $C$ to honor the collaborative equilibrium.
*   **Low Stock Floor ($S_t \approx 0$):** If the stock is insufficient to support sustained consumption, play $D$ to recover the maximum possible share of the remaining, negligible pool.
*   **Ambiguous Observations:** If the number of cooperators is indeterminate, default to the action that yielded the highest payoff in the previous round, provided $S_t$ did not decrease.

**Pseudocode:**

```python
def get_action(round, stock, prev_c, n, capacity):
    if round == 1:
        return C
    
    if round == r:
        return C if all_rounds_were_full_cooperation else D
        
    if stock < capacity * 0.5:
        return C
        
    if prev_c >= n / 2:
        return C
    else:
        return D
```
'''

description_BENEVOLENT_11 = '''
The strategy follows a "Tit-for-Tat with Forgiveness and Resource Stewardship" logic, prioritizing sustainable cooperation while reacting to observed group behavior.

### Strategy Definition

**Core Objective:** Maintain the common pool at the capacity level to maximize long-term group yield. The strategy interprets high cooperation as a signal of trust and high defection as a threat to sustainability.

**Variables:**
- `last_stock`: Stock level from the previous round (initialized to `capacity`).
- `cooperation_threshold`: A dynamic variable tracking the average number of cooperators per round.
- `round_number`: Current round (1 to `r`).

### Decision Rules

1.  **First Round:** Play `C` (Cooperate). This signals an initial commitment to sustainability.

2.  **Subsequent Rounds:**
    *   **Observation:** Observe the previous round's total consumption to deduce the number of cooperators ($C_t$) in the group.
        *   Total Consumption $T_c = \text{last\_stock} - \text{stock\_remaining\_after\_consumption}$.
        *   Since $T_c = (\text{count}_C \times \frac{S}{2n}) + (\text{count}_D \times \frac{S}{n})$, solve for $\text{count}_C$:
            $\text{count}_C = \frac{n \times (T_c - S/n)}{S/2n - S/n} = \frac{n(T_c \cdot n - S)}{S(n/2 - 1)}$.
    *   **Action Logic:**
        *   If the current `stock` is less than or equal to $S_{critical}$ (defined as $2n$), immediately play `D` (Defect) to extract resources before the pool crashes.
        *   If the `stock` is robust ($> 2n$):
            *   **Reciprocity:** If the number of cooperators in the previous round was greater than or equal to $n/2$, play `C`.
            *   **Punishment/Correction:** If the number of cooperators was less than $n/2$, play `D` to protect against exploitation, but only for one round.
            *   **Forgiveness:** If the previous round involved playing `D` (punishment), return to playing `C` in the next round, regardless of the previous outcome, to allow for the re-establishment of cooperation.

### Edge Cases and Constraints

*   **Final Rounds:** In the final round ($r$), play `D` (Defect) regardless of previous history. This is the Nash equilibrium for a finite game; since no future rounds exist to incentivize cooperation, maximizing immediate payoff is the rational survival mechanism.
*   **Low Stock Trap:** If the `stock` falls below $1.5n$, play `D` regardless of the cooperation count, as the resource is approaching a collapse state where "sustainable" consumption is no longer viable.
*   **Drift Adjustment:** If the `stock` trend over the last 3 rounds is consistently decreasing (even with cooperators present), reduce the cooperators-needed threshold by 1 for the next round to test if the group requires a stricter "punishment" cycle to stabilize.

### Pseudocode Implementation

```python
def decide_action(stock, last_stock, last_consumption, round_number, total_rounds, n):
    # Final round defect
    if round_number == total_rounds:
        return 'D'

    # Resource survival check
    if stock <= 2 * n:
        return 'D'

    # Calculate cooperators from last round
    # consumption_i = (last_stock / (2*n)) * C + (last_stock / n) * D
    # total_consumption = (last_stock / (2*n)) * C + (last_stock / n) * (n - C)
    # Simplify to solve for C (cooperators)
    C_count = round((last_consumption - last_stock) / (last_stock / (2 * n) - last_stock / n))

    # Reciprocity Logic
    if C_count >= (n / 2):
        return 'C'
    else:
        # Check if we were just punishing
        if my_previous_action == 'D':
            return 'C' # Forgiveness
        else:
            return 'D' # Punishment
```
'''

description_BENEVOLENT_12 = '''
The strategy employs a modified Tit-for-Tat approach centered on sustainability-contingent reciprocity, governed by the following decision logic for each round *t*:

1.  **First Round (t=1):** Play **C**.

2.  **Subsequent Rounds (t > 1):**
    *   **Sustainability Check:** Calculate the theoretical remaining stock if all players had cooperated in the previous round (S_{theory}). If the actual current stock *S* is greater than 90% of *S_{theory}*, proceed to the "Reciprocity Check." Otherwise, transition to "Survival Mode."

    *   **Reciprocity Check:** Let *k* be the number of cooperators in the previous round.
        *   If *k* ≥ (n - 1) (i.e., universal or near-universal cooperation), play **C**.
        *   If *k* < (n - 1), play **D** with probability *p*, where *p = 1 - (k/(n-1))*. This probabilistic response punishes defection while maintaining a potential path back to cooperation if opponents pivot.

    *   **Survival Mode:** If the actual stock *S* is less than or equal to 20% of *capacity*, play **C** to prevent total collapse, unless the game is in the final two rounds.

3.  **Endgame Phase (t = r, t = r-1):**
    *   If *S* is greater than 50% of *capacity*, play **D** to capture remaining value.
    *   If *S* is less than or equal to 50% of *capacity*, play **C** to avoid resource exhaustion, regardless of opponent history.

4.  **Pseudocode Logic:**

```python
def decide_action(round, n, S, capacity, history):
    if round == 1:
        return 'C'
    
    # Endgame logic
    if round >= r - 1:
        return 'D' if S > (0.5 * capacity) else 'C'

    # Sustainability monitor
    # S_prev was the stock at start of last round
    # consumption = (k * S_prev/(2n)) + ((n-k) * S_prev/n)
    # S_theory approximates expected stock if all C
    if S < (0.9 * S_theory):
        return 'C' if S < (0.2 * capacity) else 'D'

    # Reciprocity
    k = last_round_cooperators
    if k == n:
        return 'C'
    else:
        # Probabilistic trigger: defect more often if more people defected previously
        threshold = (k / (n - 1))
        return 'C' if random.random() < threshold else 'D'
```
'''

description_BENEVOLENT_13 = '''
**Strategy: Conditional Stewardship (Tit-for-Tat with Resource Thresholds)**

The strategy operates on a principle of "Calculated Benevolence." It seeks to maintain the stock near its capacity, which maximizes long-term yields, while defensively punishing exploitation by defectors.

### Decision Logic

**Round 1:**
Always play **C (Cooperate)**. This establishes a cooperative baseline.

**Rounds 2 through (r-1):**
1. **Observation:** Let $k$ be the number of players who played **D** in the previous round (determined by the net change in stock vs. the projected change if all had cooperated).
2. **Defensive Threshold:** If $k = 0$, play **C**.
3. **Adaptive Response:** If $k > 0$, observe the current stock level $S$.
    *   If $S < \text{capacity} \times 0.25$, play **D** (The resource is at critical risk; aggressive consumption is necessary for self-preservation before total collapse).
    *   If $S \geq \text{capacity} \times 0.25$, play **D** with probability $p = k/(n-1)$, and play **C** with probability $1-p$. This proportionality punishes defectors relative to their impact on the pool while attempting to stabilize cooperation.

**Final Round (r):**
Always play **D (Defect)**. Because the resource has no future utility and the game ends immediately after this round, there is no strategic benefit to sustaining the stock. Defecting ensures maximum realization of remaining value.

### Pseudocode Implementation

```python
def get_action(round_number, total_rounds, n, capacity, current_stock, history):
    # Final round defect
    if round_number == total_rounds:
        return "D"
    
    # First round cooperate
    if round_number == 1:
        return "C"
    
    # Analyze last round behavior
    previous_k = calculate_defectors_from_history(history)
    
    # If perfect cooperation, continue cooperating
    if previous_k == 0:
        return "C"
    
    # If resource is dying, switch to extraction
    if current_stock < (capacity * 0.25):
        return "D"
        
    # Tit-for-tat with probabilistic response to defectors
    # p scales with number of defectors; if everyone else defected, 
    # the probability of our defection is high.
    p_defect = previous_k / (n - 1)
    
    if random.random() < p_defect:
        return "D"
    else:
        return "C"
```

### Edge Cases and Benevolence Constraints

*   **Recovery Handling:** If the stock drops significantly due to other players' actions, the strategy defaults to **C** to aid recovery unless the stock falls below the 25% threshold. This prioritizes the long-term sustainability of the pool over short-term gains, ensuring the resource remains available for as long as possible for all players.
*   **Anonymity:** The strategy assumes the worst-case scenario (all players observed are treated as a collective unit) to simplify the calculation of $k$.
*   **Benevolence:** The strategy is benevolent because it exclusively triggers defection as a reaction to active exploitation by others or as a necessary measure of self-preservation during critical resource depletion. It never initiates exploitation.
'''

description_BENEVOLENT_14 = '''
The strategy employs a Conditional Reciprocity mechanism with a target stock threshold, designed to incentivize sustained cooperation while protecting against total resource collapse.

**Core Decision Rules:**

1.  **Target Stock Preservation:** The primary objective is to maintain the stock level as close to `capacity` as possible. The strategy calculates the `projected_stock` for the next round based on current consumption patterns.
    *   If current `stock` is below a critical threshold (defined as `capacity / n`), act defensively.
    *   If current `stock` is high, prioritize cooperation.

2.  **The "Tit-for-Tat with Forgiveness" Logic:**
    *   **Round 1:** Always play `C`.
    *   **Rounds 2 to r-1:** Observe the number of cooperators ($k$) from the previous round.
        *   If $k = n-1$ (all other players cooperated), play `C`.
        *   If $k < n-1$ (at least one defector), play `D` if the current `stock` is critically low (below $0.5 \times$ `capacity`) to reclaim a share, otherwise play `C` to attempt to rebuild the resource pool.
        *   *Special Condition:* If $k < n-1$ for two consecutive rounds, switch to `D` for one round to signal that exploitation is not acceptable, then revert to `C`.

3.  **Last Round Strategy:**
    *   In the final round ($r$), play `D` regardless of previous history. Because there is no future interaction to penalize, defecting maximizes the final payoff without impacting future stock levels.

**Pseudocode Definition:**

```python
def get_action(round_number, n, capacity, current_stock, history):
    # Terminal round behavior
    if round_number == r:
        return 'D'
    
    # First round behavior
    if round_number == 1:
        return 'C'
    
    # Conditional logic based on history
    last_round_cooperators = history[-1].cooperators
    
    # Check if stock is endangered
    is_stock_critically_low = (current_stock < (capacity / n))
    
    # Punishment and Recovery logic
    if last_round_cooperators == n - 1:
        return 'C'
    elif is_stock_critically_low:
        return 'D'
    elif history[-1].cooperators < (n - 1) and history[-2].cooperators < (n - 1):
        # Trigger temporary punishment for persistent defectors
        return 'D'
    else:
        # Default to benevolent cooperation
        return 'C'
```

**Edge Case Handling:**

*   **Stock = 0:** If the `stock` is 0, the game is effectively over regarding payoffs; the strategy defaults to `D` in subsequent rounds as no further cooperation is possible.
*   **Low Stock Start:** If the `stock` is below `capacity / 2` at the start of any round, the strategy prioritizes `C` to avoid extinction, unless the opponent population shows consistent high-level defecting (where the strategy shifts to `D` to mitigate total loss).
*   **Persistent Defection:** If the majority of the population consistently defects, the strategy switches to permanent `D` after round $r/2$ to prevent being the sole cooperator bearing the cost of stock maintenance while others capture the surplus.
'''

description_BENEVOLENT_15 = '''
### The Sustainable Tit-for-Tat Strategy (STFT)

The objective of this strategy is to maintain the common pool resource at a level that supports maximum sustainable yield, while punishing defectors sufficiently to discourage over-consumption.

**Strategy Logic:**

1.  **First Round:** Always play **C**. This initiates cooperation and signals an intent to manage the pool sustainably.

2.  **Subsequent Rounds:** Let $C_{prev}$ be the number of players who played **C** in the previous round.
    *   **Observation:** If $C_{prev} = n$ (full cooperation in previous round), play **C**.
    *   **Adaptive Response:** If $C_{prev} < n$, calculate the "Defection Penalty." If the current `stock` is greater than or equal to $0.5 \times \text{capacity}$, play **C** to maintain the resource stability. If the `stock` is less than $0.5 \times \text{capacity}$, play **D** for one round. This serves as a "tit-for-tat" correction to signal that depletion is unsustainable, effectively reclaiming a larger share of the shrinking resource before it collapses entirely.

3.  **Last Round:** Always play **D**. Since there is no future benefit to maintaining the stock for the subsequent round, defecting in the final round captures remaining value without penalty.

**Pseudocode:**

```python
def get_action(round_number, n, capacity, stock, history):
    # Rule 1: First Round
    if round_number == 1:
        return 'C'

    # Rule 2: Last Round
    if round_number == r:
        return 'D'

    # Rule 3: Adaptive Policy
    # Retrieve number of cooperators from the previous round's history
    last_round_cooperators = history[-1]['cooperators']

    if last_round_cooperators == n:
        return 'C'
    
    # If others defected, check if the pool is in danger
    # If pool is below half capacity, take a defensive share (Defect)
    # Otherwise, maintain cooperation to encourage others to recover
    if stock < (0.5 * capacity):
        return 'D'
    else:
        return 'C'
```

**Edge Case Handling:**
*   **Near-Zero Stock:** If the `stock` drops near zero, the strategy prioritizes the "Defect" action regardless of previous round outcomes, as the game effectively ends if the stock cannot support growth, making the extraction of remaining assets the only rational move.
*   **High Cooperation:** If the system is consistently at full cooperation, the strategy locks into an infinite loop of cooperation, maintaining the stock at `capacity` (or the equilibrium state), maximizing the long-term payoff for all participants.
'''

description_BENEVOLENT_16 = '''
Adopt a "Trigger-Modified Tit-for-Tat" strategy, which prioritizes sustainability and collective long-term yield over short-term gain.

### Decision Logic

Let $k$ be the number of cooperators observed in the previous round, $S_t$ be the stock at the start of the current round $t$, and $r$ be the total number of rounds.

1.  **First Round:** Play C.
2.  **Rounds $t \in [2, r-1]$:**
    *   If $S_t < \text{capacity} / 2$, play C regardless of previous history. The pool is in danger; maximizing growth takes precedence over punishing defectors.
    *   If $S_t \geq \text{capacity} / 2$:
        *   If $k = n$ (everyone cooperated last round), play C.
        *   If $k = n-1$ (only one defector), play C to maintain cooperation, provided the stock remains above $25\%$ of capacity.
        *   If $k < n-1$, play D to signal that universal cooperation is required to sustain the pool.
3.  **Final Round ($t = r$):** Play D. In the final round, there is no future stock to preserve, and the stock dynamics do not affect any subsequent rounds. Defecting maximizes the immediate payoff before the game ends.

### Edge Case Handling

*   **Low Stock Threshold:** If $S_t \approx 0$ or falls below a critical threshold (e.g., $S_t < 1$), always play C. Even if the current yield is negligible, cooperation is the only mechanism that allows the stock to potentially recover if opponents also switch to C.
*   **Rapid Depletion:** If the total consumption in the previous round resulted in a net loss of stock greater than $50\%$ of the previous stock level, play C in the current round, overriding any retaliation logic.
*   **Reset Condition:** If the stock reaches the `capacity` limit, reset the punishment memory. Treat the next round as if it were the first round of a sub-game (i.e., cooperate) to encourage re-stabilization at the maximum potential.

### Pseudocode

```python
def get_action(round_num, r, stock, k, n):
    # Final round defect
    if round_num == r:
        return 'D'
    
    # Emergency conservation: stock is low
    if stock < (capacity / 4):
        return 'C'
    
    # If pool is healthy, reciprocate cooperation
    if stock >= (capacity / 2):
        if k >= (n - 1):
            return 'C'
        else:
            return 'D'
    
    # If pool is moderate, lean towards cooperation
    return 'C'
```
'''

description_BENEVOLENT_17 = '''
Adopt a "Conditional Sustainment" strategy designed to maintain stock at full capacity while maximizing cooperative yield. This strategy relies on monitoring the aggregate behavior of opponents to distinguish between cooperative and defective environments, employing a responsive punishment mechanism when necessary, and phasing out cooperation in the final round to avoid exploitation.

### Decision Rules

Define a "Cooperation Threshold" ($T_c$) based on the current round and observed history. Let $k$ be the number of opponents who cooperated in the previous round.

1.  **Initialization (Round 1):**
    Play **C** (Cooperate). This establishes a cooperative baseline.

2.  **Steady State (Round 2 to $r-1$):**
    *   If the previous round's stock was $\ge$ 90% of capacity: Play **C**.
    *   If the previous round's stock was $< 90 \%$ of capacity:
        *   If the number of cooperating opponents $k$ was $\ge$ 50% of the total number of opponents $(n-1)$: Play **C**.
        *   If the number of cooperating opponents $k$ was $< 50 \%$ of the total number of opponents $(n-1)$: Play **D** (Defect). This serves as a "tit-for-tat" signal to curb rapid depletion caused by defectors.
    *   *Correction Rule:* If you played **D** in the previous round, switch to **C** in the current round if the current stock level is $\ge$ 50% of capacity. This creates a "forgiving" dynamic to allow the resource to recover.

3.  **Terminal Phase (Round $r$):**
    Regardless of history, always play **D**. This prevents a "sucker's payoff" in the final round, where future stock sustainability is irrelevant.

### Logic Pseudocode

```python
def decide_action(round_number, total_rounds, current_stock, capacity, opponents_cooperated, last_action):
    # Terminal Phase
    if round_number == total_rounds:
        return 'D'

    # Initial Phase
    if round_number == 1:
        return 'C'

    # Forgiveness logic
    if last_action == 'D' and current_stock >= (0.5 * capacity):
        return 'C'

    # Cooperation Threshold Logic
    # Maintain cooperation if stock is healthy (>= 90%)
    if current_stock >= (0.9 * capacity):
        return 'C'
    
    # Otherwise, assess aggregate opponent behavior
    # n_minus_1 is the number of opponents
    threshold = (n - 1) / 2
    if opponents_cooperated >= threshold:
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling

*   **Stock Collapse (Stock $\approx$ 0):** If current stock is below 10% of capacity, prioritize playing **C** regardless of previous trends. This is a "rescue" move intended to allow the stock growth function (which is maximized at 50% of capacity) to recover the pool rather than forcing it to zero through further defection.
*   **High Population (Large $n$):** As $n$ increases, the incentive to defect grows. The strategy remains robust by using the 50% aggregate cooperation threshold. If fewer than half of the other agents are cooperating, the environment is fundamentally defective, and the agent switches to **D** to extract value before the resource is depleted by others.
*   **Rapid Depletion:** If stock falls faster than the capacity threshold logic can accommodate, the "Correction Rule" defaults to **D** to prioritize immediate yield, anticipating that cooperative equilibrium is not attainable in the current round.
'''

description_BENEVOLENT_18 = '''
The strategy employs a "Conditional Tit-for-Tat" framework based on the aggregate behavior of opponents to balance personal yield with the sustainability of the common pool. 

**Decision Rule Framework:**

1.  **Initialization (Round 1):** Play `C`. Always initiate with cooperation to establish a sustainable trajectory.

2.  **Subsequent Rounds (Round 2 to r-1):** 
    Determine the "Sustainable Threshold" for the current round. Let $C_{prev}$ be the number of cooperators observed in the previous round. 
    *   If $C_{prev} = n-1$ (only you defected) or $C_{prev} = n$ (everyone cooperated): Play `C`.
    *   If $C_{prev} < n-1$: Calculate the current stock $S_t$. If $S_t > \frac{capacity}{2}$, play `C`. If $S_t \leq \frac{capacity}{2}$, play `D`.
    *   *Correction Rule:* If the previous round resulted in a significant stock collapse (defined as $S_{new} < 0.2 \times capacity$), play `C` regardless of aggregate history to attempt resource regeneration.

3.  **Final Round (Round r):** 
    Play `D` if the current stock $S_r \geq \frac{capacity}{n}$. Otherwise, play `C`. This maximizes utility in the terminal stage without causing long-term damage, as no future growth is possible.

**Pseudocode Implementation:**

```python
def choose_action(round_number, current_stock, history, n, capacity):
    # Rule 1: Always start with C
    if round_number == 1:
        return 'C'
    
    # Rule 3: Terminal round logic
    if round_number == r:
        if current_stock >= (capacity / n):
            return 'D'
        else:
            return 'C'
            
    # Rule 2: Adaptive cooperation
    prev_round_data = history[-1]
    cooperators = prev_round_data['cooperators_count']
    
    # Observe aggregate behavior
    if cooperators >= (n - 1):
        return 'C'
    
    # Check for collapse scenarios
    if current_stock < (0.2 * capacity):
        return 'C'
        
    # Standard conditional logic
    if current_stock > (0.5 * capacity):
        return 'C'
    else:
        return 'D'
```

**Benevolent Design Principles:**

*   **Sustainability Bias:** The strategy defaults to `C` when the stock is healthy ($> 50\%$ capacity) or when the majority of the group is cooperating, prioritizing the maintenance of the resource over short-term gain.
*   **Forbearance:** It allows for one player to defect without immediate retaliation, preventing a "death spiral" caused by a single aggressive player. 
*   **Regenerative Focus:** By choosing `C` when the stock is below $20\%$ capacity, the agent sacrifices immediate payoff to allow the common pool to recover, which is objectively better for the long-term utility of all participants.
*   **Non-Aggressive Termination:** In the final round, it only defects if the resources allow for it without exhausting the pool entirely, respecting the potential for non-zero utility.
'''

description_BENEVOLENT_19 = '''
The strategy is a modified "Tit-for-Tat with Forgiving Resilience," designed to maintain the common pool at its carrying capacity while penalizing defectors proportionally to their impact on the stock.

**Strategy Definitions:**

*   **Target State:** The optimal stock level is `capacity`. When the stock is at capacity, the total consumption of `n/2` (if everyone cooperates) leads to a consumption of `n * (capacity / 2n) = capacity / 2`. The remaining stock `capacity / 2` then doubles via growth, returning the stock to `capacity`.
*   **Cooperation Threshold:** The strategy tracks the running average of cooperation observed in the population. Let `C_rate` be the number of cooperators observed in the previous round divided by `n`.
*   **State Awareness:** The strategy monitors the "Health Factor" `H = stock / capacity`.

**Decision Rules:**

1.  **Round 1:** Always choose **C**. This signals willingness to cooperate and tests the population's baseline behavior.

2.  **Subsequent Rounds (t > 1):**
    *   **If H < 0.25 (Critical Depletion):** Play **D** only if absolutely necessary to prevent starvation, but ideally play **C** to prioritize stock recovery. Specifically: Play **C** if `H > 0.1`. If `H <= 0.1`, play **D** to extract remaining resources before they vanish, unless `H` has been declining despite high cooperation.
    *   **If 0.25 <= H < 0.9 (Recovery/Maintenance):** Match the cooperation rate of the population.
        *   If `C_rate >= 0.5`, play **C**.
        *   If `C_rate < 0.5`, play **D** with probability `1 - C_rate`. (Probabilistic Defection). This prevents exploitation while attempting to nudge the population back toward C.
    *   **If H >= 0.9 (Optimal Zone):** Play **C**. If the observed `C_rate` in the previous round was `< 1.0` (meaning at least one defector exists), play **D** for one round to signal that full cooperation is required to maintain the optimal state, then revert to **C** immediately.

3.  **Final Round (t = r):** Play **D**. Since there is no future, any stored stock provides no further benefit. Defecting maximizes the final payoff.

**Pseudocode Implementation:**

```python
def choose_action(round_num, total_rounds, stock, capacity, last_round_cooperators, n):
    # Rule 1: Terminal Round
    if round_num == total_rounds:
        return 'D'

    # Rule 2: First Round
    if round_num == 1:
        return 'C'

    H = stock / capacity
    C_rate = last_round_cooperators / n

    # Rule 3: Critical Depletion
    if H < 0.25:
        return 'C' if H > 0.1 else 'D'

    # Rule 4: Optimal/High Zone
    if H >= 0.9:
        if C_rate < 1.0:
            return 'D' # Signal
        return 'C'

    # Rule 5: Recovery/Maintenance Zone
    if C_rate >= 0.5:
        return 'C'
    else:
        # Probabilistic response to maintain leverage
        return 'D' if random.random() < (1 - C_rate) else 'C'
```

**Edge Case Handling:**
*   **Total Population Defection:** If `C_rate` is consistently 0, the strategy switches to **D** to avoid being the sole provider in a depleting pool.
*   **Sudden Stock Drops:** If `stock` drops significantly (e.g., > 30%) in a single round despite previous high cooperation, the strategy triggers a "Punishment Phase" for one round where it plays **D** to discourage the hidden defectors, regardless of the `C_rate` logic.
*   **Stagnation:** If `H` remains below 0.5 for three consecutive rounds, the strategy defaults to **C** to prevent the "Tragedy of the Commons" collapse.
'''

description_BENEVOLENT_20 = '''
The strategy employs a conditional cooperation framework based on the "tit-for-tat" principle, adapted for a collective resource environment. It aims to maximize long-term social welfare by maintaining the stock level at $K/2$, where the logistic growth function $2 \times S_{rem} \times (1 - S_{rem}/K)$ is maximized, while punishing free-riders to prevent total depletion.

### Decision Rules

Define the target consumption for round $t$ as $C_{target}$. To maximize sustainable yield, the stock $S_t$ should ideally be maintained near $K/2$.

Let $n_c$ be the number of players who cooperated in round $t-1$ (observed).
Let $history$ track the running average of cooperation levels.

1. **Initialization (Round 1):** Play $C$. Assume the majority of agents are benevolent.
2. **Subsequent Rounds (2 to $r-1$):**
   - Calculate the "Cooperation Threshold": Determine the fraction of players cooperating in the previous round ($f = n_c / n$).
   - If $f \ge 0.5$ and the current stock $S_t$ is above a critical depletion floor (defined as $K/n$), play $C$.
   - If $f < 0.5$ or $S_t < K/n$, switch to "Defensive Defection" to recover stock:
     - Play $D$ for one round.
     - Following a $D$ action, return to $C$ in the subsequent round (a "forgiving" trigger) to test if the group returns to sustainable consumption.
     - If the stock is critically low ($S_t < 0.1 \times K$), play $D$ exclusively until $S_t$ recovers to at least $0.5 \times K$.

3. **Final Round ($r$):**
   - If $S_r > K/4$, play $C$.
   - If $S_r \le K/4$, play $D$ to capture remaining resources, as there is no future utility to protect.

### Pseudocode

```python
def get_action(round, n, S, last_round_cooperators, is_first_round):
    if is_first_round:
        return 'C'
    
    if round == r:
        return 'D' if S <= (capacity / 4) else 'C'

    # Adaptive Cooperation Logic
    cooperation_fraction = last_round_cooperators / n
    critical_depletion_floor = capacity / n
    
    # Trigger conditions
    if S < 0.1 * capacity:
        return 'D'  # Aggressive recovery mode
        
    if cooperation_fraction >= 0.5 and S >= critical_depletion_floor:
        return 'C'  # Maintain sustainable equilibrium
    else:
        # Punish/Recover: Play D to stabilize stock, 
        # but reset in the next round to allow cooperation to reform
        return 'D' 
```

### Benevolent Considerations

This strategy is benevolent because it prioritizes the long-term viability of the shared resource over short-term gain. It operates on the principle of "Conditional Sustainability": it will cooperate so long as the group maintains a threshold of sustainability (the $50\%$ cooperation mark), but it switches to defensive consumption when the resource is being over-exploited by others, preventing the tragedy of the commons while simultaneously attempting to signal the need for lower consumption to the rest of the pool. It specifically avoids "Grim Trigger" strategies, which permanently collapse cooperation upon a single defection, by favoring forgiveness and recovery.
'''

description_BENEVOLENT_21 = '''
### Strategy Description: Sustainable Tit-for-Tat (STFT)

The strategy aims to maximize long-term social welfare by maintaining the common pool stock at its optimal carrying capacity while punishing defectors just enough to encourage cooperation.

#### Core Logic
The strategy maintains a target cooperation level. It treats the game as a reciprocal relationship where one's own cooperation is contingent on the average cooperativeness of the group in the previous round.

#### Pseudocode

```python
# Constants/Parameters
# n: number of players, r: total rounds, capacity: max stock
# t: current round
# S_t: stock at start of round t
# c_{t-1}: number of cooperators observed in round t-1

def get_action(t, S_t, c_{t-1}):
    # 1. Edge Case: First Round
    if t == 1:
        return C

    # 2. Edge Case: Last Round
    # If the resource is sufficient, maintain cooperation to extract value.
    # If the resource is depleted, defecting doesn't change the future, 
    # but cooperation is the benevolent choice.
    if t == r:
        return C

    # 3. Dynamic Thresholding (The Tit-for-Tat mechanism)
    # The 'benevolence' factor: We cooperate if the group cooperates 
    # above a minimal threshold of reciprocity.
    
    # Threshold definition: We require at least n/2 players (rounded down) 
    # to cooperate to justify continued cooperation.
    threshold = floor(n / 2)
    
    if c_{t-1} >= threshold:
        return C
    else:
        # If the group defects, punish briefly by defecting once 
        # to signal non-compliance, then return to cooperate next round.
        return D
```

#### Decision Rules
1.  **Initialization:** Always start with **C** to foster trust and establish the cooperative equilibrium.
2.  **Reciprocity:** In any round $t$ (where $1 < t < r$), evaluate the previous round's outcome ($c_{t-1}$). If the number of cooperators was equal to or greater than $\lfloor n/2 \rfloor$, play **C**. This threshold ensures that the pool is not exhausted by a minority of defectors.
3.  **Punishment:** If the number of cooperators in $t-1$ fell below the threshold, play **D** for round $t$. This acts as a "grim-trigger lite" signal, indicating that unconditional exploitation is not tolerated. After one round of defection, return to **C** in $t+1$ to reset the cooperative cycle and invite re-cooperation from the group.
4.  **Terminal Round:** In the final round ($t=r$), always play **C**. There is no strategic benefit to punishing defectors, and defection in the final round provides no long-term gain for the system.

#### Benevolence and Robustness
*   **Sustainability:** By setting a threshold based on $n/2$, the strategy allows for slight fluctuations in group behavior without collapsing into a total defect state, but remains strict enough to prevent total depletion.
*   **Forgiveness:** The strategy is forgiving. After punishing in round $t$ for a violation in $t-1$, it immediately reverts to cooperation in $t+1$. This creates an "olive branch" for opponents who might have accidentally defected or who were trying to signal a shift in behavior.
*   **Optimism:** The strategy assumes that the group can reach a sustainable equilibrium. It never initiates a sequence of defection unless provoked, ensuring that if all players follow a similar logic, the system converges to full cooperation ($C$ for everyone) and maximum possible stock level.
'''

description_BENEVOLENT_22 = '''
The strategy follows a conditional "Tit-for-Tat" variant adjusted for the specific growth dynamics of the common pool. The objective is to maintain the stock level at the capacity point to maximize sustainable, long-term yield for all players.

**Strategy Definitions:**

*   **Cooperation Target ($C$):** All players choosing action C results in the stock remaining at capacity (assuming it started there).
*   **Defection Sensitivity ($k$):** Let $D_t$ be the count of defectors in the previous round. If $D_t > 0$, the stock is depleted.
*   **Grim Threshold:** If the stock falls below 50% of capacity, the system enters a recovery mode.

**Decision Rules:**

In round $t=1$:
- Play **C**.

In rounds $t > 1$:
1. **Observation:** Determine the number of defectors in the previous round, $D_{t-1}$.
2. **Recovery Mode:** If the current stock $S_t < \text{capacity} \times 0.5$, play **C** regardless of opponent history to allow the stock to regenerate.
3. **Cooperation Maintenance:** If $D_{t-1} = 0$ (all players cooperated in the previous round) or $S_t \approx \text{capacity}$, play **C**.
4. **Punishment/Response:** If $D_{t-1} > 0$ and $S_t \ge \text{capacity} \times 0.5$:
   - Calculate the "Fair Share" to punish defectors without destroying the pool.
   - If the previous round's stock reduction resulted in a net growth rate of $\le 0$ (i.e., consumption > growth potential), play **D** to signal that unsustainable extraction is unacceptable.
   - If the pool is resilient (sufficient stock remaining), play **C** to incentivize a return to sustainable cooperation, assuming the previous defection might be an error or a temporary anomaly.

**Pseudocode:**

```python
def get_action(round, current_stock, prev_defectors, capacity):
    # Always cooperate on the first move
    if round == 1:
        return 'C'
    
    # Allow regeneration if stock is critical
    if current_stock < (capacity * 0.5):
        return 'C'
        
    # If everyone cooperated previously, continue cooperating
    if prev_defectors == 0:
        return 'C'
        
    # If defection occurred, assess pool stability
    # If stock is healthy, give benefit of the doubt (cooperate)
    # If stock is unhealthy, defect to prioritize personal survival 
    # and signal unsustainable play
    if current_stock < (capacity * 0.8):
        return 'D'
    else:
        return 'C'
```

**Edge Cases:**

*   **Last Round:** In the final round ($t=r$), if the stock is healthy ($S_r \ge 0.5 \times \text{capacity}$), switch to **D** to capture the remaining value, as there are no future rounds to sustain. If the stock is critically low, continue to play **C** to ensure the total yield is not zeroed out by total collapse.
*   **Fluctuation:** If the stock is exactly at capacity, play **C**. The strategy prioritizes the "benevolent" outcome of keeping the pool at capacity for the duration of the game, only punishing when the aggregate behavior threatens the sustainability of the resource.
'''

description_BENEVOLENT_23 = '''
**Strategy: Adaptive Sustainable Tit-for-Tat**

The strategy maintains the common pool stock at its optimal carrying capacity by aligning personal consumption with the observed aggregate behavior of opponents. The strategy treats the common pool as a shared asset where sustained cooperation maximizes total long-term utility.

**Decision Rules:**

1.  **Round 1:** Always play **C** (Cooperate). This signals an initial willingness to sustain the resource.

2.  **Rounds 2 to *r*-1:**
    *   Calculate the **Cooperation Ratio (CR)** from the previous round: `CR = (Number of Cooperators in previous round) / n`.
    *   If `CR` is greater than or equal to a threshold `T = 0.5`, play **C**.
    *   If `CR` is less than `T`, play **D** (Defect).
    *   **Conditional Forgiveness:** If the current `stock` is less than or equal to `capacity * 0.25` (critical depletion), prioritize resource recovery by playing **C** regardless of the previous round's `CR`, provided that `stock` is non-zero. If `stock` is zero, play **C** (attempting to allow growth).

3.  **Last Round (*r*):**
    *   If the current `stock` is greater than 0, play **D** (Defect). Since there is no future to protect, the benevolent obligation shifts to capturing the remaining sustainable resource before the game ends, as the terminal state of the pool has no further value.
    *   If the `stock` is 0, play **C**.

**Pseudocode:**

```python
def get_action(round_number, n, stock, capacity, prev_round_cooperators):
    # Terminal round logic
    if round_number == r:
        return D if stock > 0 else C

    # First round logic
    if round_number == 1:
        return C

    # Resource recovery logic (Benevolent prioritization of sustainability)
    if stock <= (capacity * 0.25):
        return C if stock > 0 else C

    # Tit-for-Tat based on aggregate cooperation
    # CR is the fraction of the population that cooperated
    cr = prev_round_cooperators / n
    
    if cr >= 0.5:
        return C
    else:
        return D
```

**Benevolent Intent:**
This strategy is designed to enforce a sustainable equilibrium. By playing **C** in the first round and observing the population, it creates a "handshake" protocol. If the majority cooperates, the strategy sustains the pool indefinitely. If the majority defects, the strategy switches to **D** to prevent total exploitation by free-riders while the stock is high. Crucially, the "Conditional Forgiveness/Recovery" clause ensures that if the resource is critically low, the strategy will sacrifice short-term gain (by playing **C**) to prevent resource collapse, assuming that preventing extinction of the pool is the highest benevolent imperative.
'''

description_BENEVOLENT_24 = '''
Define a cooperative threshold `T` based on the round number `t` and the current stock level `S`. Initialize an internal state variable `reputation` to 1.0 (representing full trust).

In each round `t`, execute the following decision logic:

1. **Calculate the Sustainable Consumption Threshold:** 
   Determine if the current stock `S` supports full cooperation without collapse. The stock is sustainable if the sum of all individual consumptions `C_total` does not exceed the potential growth. If all players cooperate, total consumption is `n * (S / 2n) = S/2`. The resulting stock is `S/2`. Growth is `2 * (S/2) * (1 - (S/2)/capacity) = S * (1 - S/(2*capacity))`. For stability, we require `S/2 + Growth >= S`, which simplifies to `S <= capacity`. Since `S <= capacity` is always true, full cooperation is always sustainable if all agents cooperate.

2. **Observe Previous Round:**
   Let `k` be the number of players who cooperated in the previous round `t-1`. 
   Update `reputation` as follows:
   `reputation_new = reputation_old * 0.9 + (k/n) * 0.1`
   If `t == 1`, set `reputation` to 1.0.

3. **Determine Strategy:**
   If `t == r` (last round):
   Defect (D) if `reputation < 0.5`, otherwise Cooperate (C).

   If `t < r`:
   *   If `S < (capacity * 0.2)`:
       Defect (D) to maximize individual gain before potential stock exhaustion.
   *   Else if `reputation >= 0.6`:
       Cooperate (C) to maintain stock levels.
   *   Else:
       Defect (D) to punish defecting behavior and penalize non-cooperative outcomes.

4. **Pseudocode representation:**
   ```
   def get_action(t, r, S, n, k_prev):
       if t == 1:
           reputation = 1.0
       else:
           reputation = reputation * 0.9 + (k_prev/n) * 0.1
       
       if t == r:
           return C if reputation >= 0.5 else D
           
       if S < (capacity * 0.2):
           return D
           
       if reputation >= 0.6:
           return C
       else:
           return D
   ```

5. **Benevolence Adjustment:**
   The strategy is inherently benevolent by prioritizing cooperation when the population demonstrates sustained trust (reputation >= 0.6) and the resource is viable. The strategy only shifts to defection when the resource is critically depleted (below 20% capacity) or when the population has demonstrated a failure to cooperate (low reputation), ensuring the agent does not unilaterally subsidize defectors while the pool is being destroyed.
'''

description_BENEVOLENT_25 = '''
Adopt a "Generous Tit-for-Tat with Sustainability Threshold" strategy. This approach aims to maximize collective welfare by sustaining the pool at or near capacity while punishing persistent defectors only when they threaten the pool's viability.

**Decision Rules:**

1.  **Cooperation Baseline:** Always initiate with C in the first round.
2.  **Sustenance Logic:** In any round $t < r$, monitor the `new_stock` generated from the previous round. If `new_stock` is below a critical threshold (defined as `0.5 * capacity`), switch to C immediately, regardless of previous opponent behavior, to allow the pool to recover.
3.  **Conditional Strategy:** If `new_stock` is greater than or equal to `0.5 * capacity`, adopt a Tit-for-Tat approach based on the *average* cooperation rate of the opponents in the previous round.
    *   Let $C_{count}$ be the number of players who chose C in the previous round.
    *   If $C_{count} / (n-1) \ge 0.5$, play C.
    *   If $C_{count} / (n-1) < 0.5$, play D.
4.  **Final Round (t = r):** Defect (play D) in the final round if the game is considered a finite interaction without future consequence, unless the `stock` is below `0.25 * capacity`. If the stock is critically low, continue to play C to maximize final round yield, as total depletion would minimize returns for all players.

**Pseudocode Implementation:**

```python
def get_action(current_round, total_rounds, n, capacity, current_stock, prev_opp_c_count):
    # Sustainability Recovery Mode
    if current_stock < (0.5 * capacity):
        return 'C'
    
    # Final Round Defection
    if current_round == total_rounds:
        if current_stock < (0.25 * capacity):
            return 'C'
        else:
            return 'D'
    
    # First Round
    if current_round == 1:
        return 'C'
        
    # Tit-for-Tat / Adaptive Cooperation
    # prev_opp_c_count is the number of opponents who cooperated previously
    # Total opponents = n - 1
    if (prev_opp_c_count / (n - 1)) >= 0.5:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**

*   **Stock Collapse:** If the `current_stock` approaches zero, the priority shifts entirely to C to prevent extinction, as D yields zero when the stock is zero.
*   **Anonymity:** Because the identities of opponents are unknown, the strategy relies purely on the aggregate statistic of the previous round's cooperation count. It avoids targeting specific players, maintaining a consistent, fair, and observable signal that encourages others to cooperate.
*   **Threshold Buffers:** The use of the $0.5$ threshold ensures the strategy is resilient against small amounts of noise or accidental defection while aggressively reclaiming cooperation when the pool is at risk.
'''

description_BENEVOLENT_26 = '''
The strategy employs a "Trigger-Adaptive Cooperation" approach. The primary objective is to maintain the stock at or near `capacity` to ensure long-term sustainability and maximize total group utility.

### Decision Rules

Let $k$ be the number of opponents who played Cooperate ($C$) in the previous round.

1.  **First Round:** Always play $C$. This establishes a cooperative baseline.
2.  **Subsequent Rounds (1 < t < r):** 
    *   Calculate the "Cooperation Threshold" $T = \lceil n/2 \rceil$.
    *   If $k \geq T$, play $C$. 
    *   If $k < T$, play $D$ for exactly one round to signal dissatisfaction and prevent the resource from being exploited by others without receiving a proportional share, then return to $C$ in the following round regardless of their action.
3.  **Final Round (t = r):** 
    *   If current stock $S \leq (S_{initial} / 2)$, play $D$ to maximize personal utility before the game terminates.
    *   If current stock $S > (S_{initial} / 2)$, play $C$ to maintain the resource state for any potential future interaction or extended horizon, assuming the "benevolent" constraint prioritizes long-term resource health.

### Handling Edge Cases

*   **Low Stock Scenario:** If the current stock $S$ falls below $capacity / (2n)$, switch to $C$ immediately regardless of past history or the $T$ threshold. This is critical for preventing population collapse (extinction), which results in zero payoffs for all future rounds.
*   **Persistent Defection:** If the group consistently sustains $k < T$ for more than three consecutive rounds, the strategy shifts to $D$ for the remainder of the game, as cooperative maintenance is no longer viable given the group's behavior.
*   **Near-Capacity Sustainability:** If the observed state $S$ is consistently within 95% of `capacity`, prioritize $C$ even if a small minority defects ($k = n-2$), as the resource recovery function is robust enough to tolerate minor depletion.

### Pseudocode

```python
def decide_action(round, stock, prev_opponents_cooperated, n, r):
    # Base Case: First round
    if round == 1:
        return 'C'
    
    # Critical Conservation: Prevent extinction
    if stock < (capacity / (2 * n)):
        return 'C'

    # Final Round Logic
    if round == r:
        return 'D' if stock <= (capacity / 2) else 'C'

    # Adaptive Threshold Strategy
    threshold = ceil(n / 2)
    if prev_opponents_cooperated >= threshold:
        return 'C'
    else:
        # Punish/Recover logic:
        # If we just defected (signaled), return to C
        # Otherwise, defect to protect share
        return 'D' if last_action_was_C else 'C'
```
'''

description_BENEVOLENT_27 = '''
Play Cooperate (C) in the first round.

For all subsequent rounds, observe the total number of cooperators from the previous round, denoted as *k* (where 0 ≤ *k* ≤ n). Your action for the current round depends on the current stock level *S* and the recent history of cooperation:

1.  **Cooperation Trigger:** Cooperate (C) if *k* > *n/2*. This indicates that a majority of the group is successfully maintaining the resource.
2.  **Punishment/Defection:** Defect (D) if *k* ≤ *n/2* and the current stock *S* is greater than a critical threshold *S_crit*. 
    *   Define *S_crit* = (capacity / 2) - (current_round_number / total_rounds) * (capacity / 2). This threshold decreases over time, becoming more permissive as the game nears its end.
3.  **Survival/Reclamation:** If *k* ≤ *n/2* and the stock *S* is below or equal to *S_crit*, play C to prioritize resource recovery.
4.  **Final Round Exception:** In the final round (t = r), play Defect (D) regardless of the stock level or previous history, provided that *S* > 0. If *S* = 0, the choice is null.

**Pseudocode:**

```python
def get_action(round, total_rounds, n, capacity, current_stock, k_prev):
    # k_prev is the number of cooperators in the previous round
    
    # 1. End-game terminal condition
    if round == total_rounds:
        return 'D'
    
    # 2. Survival condition (Critical shortage)
    # If the resource is critically depleted, favor preservation over punishment
    s_crit = (capacity / 2) * (1 - (round / total_rounds))
    if current_stock <= s_crit:
        return 'C'
    
    # 3. Cooperation condition (Majority consensus)
    if k_prev > (n / 2):
        return 'C'
    
    # 4. Default state: Tit-for-tat punishment
    # If the majority are defecting, switch to defect to avoid exploitation 
    # unless the resource is critical (handled in step 2)
    return 'D'
```
'''

description_BENEVOLENT_28 = '''
The strategy, "Adaptive Sustainable Stewardship," operates on the principle of conditional cooperation aimed at maximizing collective stock stability while punishing exploitation. It maintains a cooperative stance as long as the aggregate behavior of the pool allows for sustainable growth.

**State Variables**
- `n`: Number of players.
- `capacity`: Maximum stock level.
- `S_t`: Stock at the start of round `t`.
- `C_count_t-1`: Number of cooperators observed in the previous round.
- `Cooperative_Threshold`: A dynamically calculated value derived from the stock-dependent growth curve.

**Decision Rules**

In each round `t`, the decision to Cooperate (C) or Defect (D) is determined by the following logic:

1.  **Round 1:** Always choose C.
2.  **Rounds 2 to r-1:**
    *   Calculate the *Target Consumption*: If all players choose C, the stock changes from `S` to `S - (n * S/2n) = S/2`. The resulting growth is `2 * (S/2) * (1 - (S/2)/capacity)`. To maintain `S_t+1 >= S_t`, the system requires `S_t <= capacity / 2`.
    *   Observe `C_count` from round `t-1`.
    *   If `C_count` == `n` (perfect cooperation), choose C.
    *   If `C_count` < `n` (some defectors):
        *   If `S_t` > `capacity / 2` (the resource is currently robust), choose C to signal continued cooperation, but only if the previous round’s total consumption did not deplete the stock below 50% of the maximum sustainable level.
        *   If `S_t` <= `capacity / 2` (the resource is vulnerable) AND `C_count` < `n`, choose D to protect remaining stock or mitigate loss relative to defecting opponents.
3.  **Final Round (r):**
    *   If `S_r` > `capacity / 4`, choose C.
    *   If `S_r` <= `capacity / 4`, choose D to capture remaining value before the game terminates.

**Pseudocode Implementation**

```python
def choose_action(round_number, total_rounds, current_stock, prev_round_cooperators, n, capacity):
    # Rule 1: Initial move
    if round_number == 1:
        return 'C'

    # Rule 3: Final round logic
    if round_number == total_rounds:
        if current_stock > (capacity / 4):
            return 'C'
        else:
            return 'D'

    # Rule 2: Adaptive middle game logic
    # Calculate if the resource is in a critical state (below 50% capacity)
    is_vulnerable = current_stock <= (capacity / 2)
    
    # If perfect cooperation occurred previously, continue cooperating
    if prev_round_cooperators == n:
        return 'C'
    
    # If the resource is vulnerable and someone defected, protect self
    if is_vulnerable and prev_round_cooperators < n:
        return 'D'
    
    # Otherwise, maintain cooperation to encourage sustainable equilibrium
    return 'C'
```

**Edge Case Handling**
- **Depleted Stock:** If `S_t` approaches 0, the strategy forces D in any round where `S_t` < `capacity / (2*n)`, acknowledging that the resource is effectively collapsed and individual capture is the only remaining payoff.
- **Opponent Fluctuation:** If the number of cooperators fluctuates, the strategy uses the `is_vulnerable` check as a fallback; it prioritizes collective sustainability (C) when the stock is high but switches to self-preservation (D) when the resource is nearing collapse to prevent being the sole cooperator in a zero-sum environment.
'''

description_BENEVOLENT_29 = '''
Strategy: Tit-for-Tat with Resource-Aware Forgiveness

This strategy prioritizes sustainability through conditional cooperation, adjusting behavior based on the observed collective impact on the resource stock.

1.  **Initialization:**
    In Round 1, always play C.

2.  **Round-by-Round Decision Rule:**
    In each round $t > 1$, define the "Cooperation Threshold" based on the previous round's outcome. Let $c_{t-1}$ be the number of players who played C in the previous round.
    *   Play C if $c_{t-1} \ge \lfloor n/2 \rfloor$ and the current stock $S_t > \epsilon$, where $\epsilon$ is a safety margin (e.g., $0.1 \times \text{capacity}$).
    *   Play D only if the observed collective behavior indicates a collapse is imminent or ongoing. Specifically, if $c_{t-1} < \lfloor n/2 \rfloor$ or the current stock $S_t$ drops below $0.2 \times \text{capacity}$, switch to D to maximize personal payoff before the stock hits zero, effectively "salvaging" value from a failing pool.

3.  **End-Game Heuristic:**
    As the number of rounds remaining ($r_{rem}$) decreases, the incentive to preserve stock diminishes.
    *   If $r_{rem} \le 3$:
        *   If the current stock $S_t > 0.5 \times \text{capacity}$, play C to maintain the pool for the final rounds.
        *   If the current stock $S_t \le 0.5 \times \text{capacity}$, defect (play D) for all remaining rounds, as the stock is unlikely to regenerate sufficiently to support cooperation for the duration of the game.

4.  **Edge Case Handling:**
    *   *Resource Depletion:* If at any point the stock $S_t$ falls below $0.05 \times \text{capacity}$, play D regardless of the round number, as the resource is effectively exhausted and regeneration is unlikely.
    *   *Recovery:* If the stock begins to recover (defined as $S_{t} > S_{t-1}$ for two consecutive rounds) after a period of exploitation, switch immediately back to C, regardless of the previous round's $c_{t-1}$. This acts as a signal of benevolence to encourage re-cooperation.

Pseudocode:

```python
def decide_action(round, r, n, current_stock, prev_cooperators):
    # End-game logic
    rounds_remaining = r - round
    if rounds_remaining <= 3:
        if current_stock > (0.5 * capacity):
            return C
        else:
            return D

    # Critical depletion logic
    if current_stock < (0.05 * capacity):
        return D

    # Standard Tit-for-Tat with Cooperation Threshold
    if round == 1:
        return C
    
    # If the group is cooperating enough, continue to cooperate
    if prev_cooperators >= (n // 2) and current_stock > (0.2 * capacity):
        return C
    else:
        return D
```
'''

description_BENEVOLENT_30 = '''
The strategy follows a "Tit-for-Tat with Forgiveness and Resource Awareness" logic, designed to sustain the common pool while incentivizing cooperation.

**Decision Rules:**

1.  **Initial Round (t=1):** Always play $C$. This establishes a cooperative baseline.
2.  **Subsequent Rounds (t > 1):** Calculate the sustainability of the current stock and the behavior of opponents in the previous round ($t-1$).
    *   **Assessment of Opponent Cooperation ($k$):** Let $k$ be the number of opponents who played $C$ in the previous round.
    *   **Threshold Rule:** If $k < n-1$ (meaning at least two opponents defected), play $D$ to protect your individual resource share against depletion.
    *   **Reciprocal Cooperation:** If $k = n-1$ (all opponents cooperated), play $C$.
    *   **Conditional Forgiveness:** If the previous round resulted in $k < n-1$, but the stock level $S_t > 0.5 \times \text{capacity}$, play $C$ in the current round to offer a "fresh start" for collective sustainability, provided $t < r$ (not the final round).
3.  **Final Round (t = r):** If $S_r$ is sufficient to support a cooperative payout without crashing the ecosystem in this final turn, play $C$. If $S_r$ is already low ($\le \frac{\text{capacity}}{n}$), play $D$ to maximize your remaining yield, as future growth is irrelevant.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, current_stock, prev_opponents_cooperated, n):
    # Rule 1: First round cooperation
    if round_number == 1:
        return 'C'

    # Rule 2: Final round optimization
    if round_number == total_rounds:
        if current_stock <= (capacity / n):
            return 'D'
        else:
            return 'C'

    # Rule 3: Strategy adjustment based on opponent behavior
    # k is the number of opponents who cooperated (prev_opponents_cooperated)
    # Total opponents = n - 1
    if prev_opponents_cooperated == (n - 1):
        # Full cooperation observed; maintain cooperation
        return 'C'
    
    # Rule 4: Forgiveness Mechanism
    # If the ecosystem is healthy despite defection, attempt to restore cooperation
    elif current_stock > (0.5 * capacity):
        return 'C'
    
    # Otherwise, punish defection
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Near-Depletion ($S \approx 0$):** If the stock drops below the threshold required for growth (based on the growth function), the strategy forces a $C$ play in an attempt to allow the stock to recover, even if opponents continue to defect. 
*   **Total Defection:** If all opponents defect in round $t$, and the stock is depleted below the sustainable threshold, the strategy switches to $D$ for all subsequent rounds to prevent total loss of resources before the game ends.
'''

description_BENEVOLENT_31 = '''
The strategy employs a "Trigger-Modified Tit-for-Tat" approach designed to maximize the sustainable yield of the common pool by encouraging mutual cooperation while protecting against resource collapse caused by defectors.

### Strategy Rules

**Round 1:**
Play **C** (Cooperate). This establishes a baseline of cooperation.

**Rounds 2 to r-1:**
Assess the previous round's outcome. Let $c$ be the number of opponents who played **C** in the previous round ($0 \le c \le n-1$).

*   **If the stock $S_t$ is below a critical threshold (defined as $capacity/4$):**
    Play **C** regardless of opponent behavior. Defecting when the stock is near collapse accelerates resource death; cooperation is the only path to potential recovery.

*   **If the stock $S_t$ is healthy ($S_t \ge capacity/4$):**
    *   If $c = n-1$ (everyone cooperated): Play **C**.
    *   If $c < n-1$ (at least one defector): Play **D** with probability $p = 1 - (c / (n-1))$. This stochastic punishment reduces the incentive for others to defect while maintaining a possibility of reconciliation. If the random check fails (resulting in a **C** action), treat it as an attempt to signal forgiveness.

**Final Round ($r$):**
Play **D** (Defect). Since the game terminates, there is no future utility to be gained from stock preservation. Defecting in the final round captures remaining value before the game ends.

### Pseudocode Implementation

```python
def get_action(round_number, current_stock, prev_round_opponents_cooperated, n, r, capacity):
    # Rule for final round
    if round_number == r:
        return 'D'
    
    # Rule for first round
    if round_number == 1:
        return 'C'
    
    # Critical threshold protection
    if current_stock < (capacity / 4):
        return 'C'
    
    # Adaptive retaliation/forgiveness logic
    num_opponents = n - 1
    coop_rate = prev_round_opponents_cooperated / num_opponents
    
    # Defect with probability inverse to cooperation rate
    if random_float(0, 1) > coop_rate:
        return 'D'
    else:
        return 'C'
```

### Benevolence Handling
This strategy is benevolent by prioritizing long-term sustainability over immediate gains. It avoids "tit-for-tat" escalation by using stochastic punishment rather than binary retaliation, allowing for "noisy" recovery if other players attempt to return to cooperation. The critical threshold rule ensures that even if opponents are consistently greedy, this agent will not participate in the final destruction of the common pool, acting as a steward for the resource until the very end.
'''

description_BENEVOLENT_32 = '''
Adopt a "Tit-for-Tat with Graduated Stock Sensitivity" approach. 

### Decision Rules
Maintain a `reputation_score` for the aggregate pool of opponents, initialized to 1.0 (indicating perfect trust).

**Round 1:**
- Always play Cooperate (C).

**Rounds 2 to r-1:**
- Calculate the `cooperation_rate` of opponents from the previous round.
- Update `reputation_score`:
  - `reputation_score = reputation_score * 0.9 + cooperation_rate * 0.1`
- Determine action based on `current_stock` and `reputation_score`:
  - If `current_stock` > 0.5 * `capacity` AND `reputation_score` > 0.7: Play C.
  - If `current_stock` > 0.5 * `capacity` AND `reputation_score` <= 0.7: Play D with probability `(1 - reputation_score)`. Otherwise, play C.
  - If `current_stock` <= 0.5 * `capacity` AND `reputation_score` >= 0.5: Play C.
  - If `current_stock` <= 0.5 * `capacity` AND `reputation_score` < 0.5: Play D.

**Final Round (r):**
- If `current_stock` > (0.25 * `capacity`), play C.
- Otherwise, play D.

### Pseudocode Logic
```python
# Variables
reputation_score = 1.0

# Per Round
if round == 1:
    action = C
elif round == r:
    action = C if current_stock > (0.25 * capacity) else D
else:
    cooperation_rate = (num_opponents_cooperated) / (n - 1)
    reputation_score = (0.9 * reputation_score) + (0.1 * cooperation_rate)
    
    if current_stock > (0.5 * capacity):
        if reputation_score > 0.7:
            action = C
        else:
            action = D if random() < (1 - reputation_score) else C
    else:
        action = C if reputation_score >= 0.5 else D
```

### Edge Cases and Benevolence
- **Stock Depletion:** If the stock drops below 10% of `capacity`, prioritize preservation (C) regardless of the reputation score to prevent total collapse, unless it is the final round.
- **Opponent Defection:** If all opponents defect, the `reputation_score` will rapidly decline, triggering defensive defection (D) to avoid being exploited, but the strategy maintains a probabilistic chance to revert to cooperation if they return to C, allowing for mutual recovery.
- **Benevolence Mechanism:** The strategy prioritizes C whenever the ecosystem is healthy (`stock` > 0.5 * `capacity`) or when the group has demonstrated past cooperation, ensuring maximum long-term yield for the collective rather than short-term extraction.
'''

description_SELFISH_5 = '''
The strategy follows a conditional tit-for-tat approach with a threshold-based exit for the final round. It aims to maximize individual payoff by balancing immediate resource extraction against the necessity of maintaining future stock viability.

**Variables:**
*   $k$: number of cooperators observed in the previous round ($0 \le k \le n-1$).
*   $S_t$: stock level at the beginning of round $t$.
*   $T$: current round number ($1 \le T \le r$).

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. Establishing a baseline of cooperation is necessary to observe opponent behavior and allow the stock to grow toward capacity.

2.  **Rounds 2 through $r-1$:**
    *   Calculate the average cooperation rate of opponents from the previous round: $rate = k / (n-1)$.
    *   If $rate \ge 0.5$ (the majority or half of opponents cooperated in the previous round), play **Cooperate (C)**.
    *   If $rate < 0.5$ or if the current stock $S_t$ drops below a critical threshold (defined as $capacity \times 0.2$), switch to **Defect (D)**. This triggers a "harvest phase" to extract maximum remaining utility before the resource pool collapses.

3.  **Final Round ($T = r$):**
    *   Always play **Defect (D)**. Regardless of previous cooperation levels or stock status, there is no future utility to be gained from preserving the pool. Extract the maximum possible share of the remaining stock.

**Edge Case Handling:**
*   **Stock Depletion:** If $S_t \le 0$, the game state prevents any consumption; if the game permits actions regardless, play **Defect (D)** to maintain consistency with the final round logic.
*   **Observed Cooperation ($k$):** In cases where $n=2$, the "previous round cooperation" is binary (0 or 1). If the opponent defected in the previous round, treat this as $rate=0$ and Defect. If the opponent cooperated, treat as $rate=1$ and Cooperate.
*   **Recovery:** If the strategy has switched to Defect due to low cooperation, but the stock subsequently recovers above $0.5 \times capacity$ and cooperation is detected again (i.e., opponents return to C), resume **Cooperate (C)**. This allows for self-correction if opponents were temporarily forced into defection by their own algorithm's stock-level constraints.
'''

description_SELFISH_6 = '''
The objective is to maximize cumulative payoff by maintaining stock levels near the capacity while exploiting the cooperative behavior of others. The strategy utilizes a tit-for-tat variant conditioned on the sustainable yield threshold of the common pool.

### Decision Rules

For every round $t$, define the current stock as $S_t$. The strategy selects action $A_t \in \{C, D\}$ based on the estimated cooperation rate of opponents in the previous round $t-1$ (denoted as $k_{t-1}$, where $0 \leq k_{t-1} \leq n-1$ is the number of opponents who cooperated) and the current stock $S_t$.

1. **Initialization (Round 1):**
   - Play $C$.

2. **Iterative Rounds ($t > 1$):**
   - Calculate the "Sustainable Threshold" ($T$): This is the stock level below which total consumption must be limited to ensure growth. Set $T = 0.5 \times \text{capacity}$.
   - If $S_t < T$:
     - Play $C$ regardless of previous opponent behavior to prevent stock collapse.
   - If $S_t \geq T$:
     - If the number of opponents who cooperated in round $t-1$ was $n-1$ (perfect cooperation): Play $C$.
     - If the number of opponents who cooperated in round $t-1$ was $< n-1$: Play $D$.

3. **Terminal Rounds:**
   - Define the "Horizon Threshold" ($H$) as $r - t + 1$. If $H \leq \lceil \frac{S_t}{n \cdot \text{max_payout}} \rceil$ (where max_payout is the payoff of D at current stock), the remaining rounds are insufficient to sustain future growth.
   - In all rounds where $H < 3$, switch to $D$ unconditionally to extract remaining value before the game ends.

### Pseudocode

```python
def get_action(S, t, r, n, history):
    # Check for end-game depletion
    if (r - t) < 2:
        return 'D'

    # Sustainable threshold
    sustainable_stock = capacity * 0.5

    if S < sustainable_stock:
        return 'C'

    if t == 1:
        return 'C'

    # Observe opponent behavior from last round
    # history[-1] contains number of cooperators
    last_opponents_cooperated = history[-1]['cooperators']
    
    # If the user was a cooperator, they count as one of the cooperators 
    # observed in the aggregate. Adjust accordingly:
    if history[-1]['my_action'] == 'C':
        opponents_who_cooperated = last_opponents_cooperated - 1
    else:
        opponents_who_cooperated = last_opponents_cooperated

    # Strict cooperation requirement: only share if everyone else is sharing
    if opponents_who_cooperated == (n - 1):
        return 'C'
    else:
        return 'D'
```

### Edge Cases
- **Stock Collapse ($S \approx 0$):** If the stock falls below a critical level (defined as $S < 0.1 \times \text{capacity}$), defect unconditionally. Preservation is futile if the stock cannot recover within the remaining rounds; extraction takes precedence.
- **High Opponent Defection:** If the strategy detects that opponents have defected for two consecutive rounds regardless of stock level, abandon cooperation immediately for the remainder of the game to minimize relative loss.
'''

description_SELFISH_7 = '''
**Strategy: Threshold-Based Tit-for-Tat (TBTFT)**

This strategy operates as a reactive, selfish optimizer that prioritizes long-term resource maintenance over short-term gain, defecting only when resource sustainability is threatened by others or when the game enters the terminal phase.

**1. Decision Logic**

Define the state variable $k$ as the number of opponents who cooperated in the previous round.

*   **Round 1:** Play **C** (Cooperate). Establish cooperation while the stock is at maximum capacity, ensuring optimal growth for the next round.
*   **Round 2 to (r-1):**
    *   If $k \ge \lceil n/2 \rceil$: Play **C**. When a majority or split-majority of the group cooperates, the stock remains sustainable or grows; continuing to cooperate maximizes the infinite-horizon payoff.
    *   If $k < \lceil n/2 \rceil$: Play **D**. When the majority defects, the stock is being depleted rapidly. Cooperating in this environment results in a net loss of potential payoff, as others will capture the surplus. Defecting captures the remaining stock before it reaches zero.
*   **Final Round (Round r):** Play **D**. With no future rounds to incentivize, cooperation yields no long-term benefits. Extract the maximum possible share of the remaining stock.

**2. Resilience Mechanism (Self-Correction)**

If the stock $S_t$ falls below a critical threshold defined by $S_{crit} = \text{capacity} / 2n$ in any round $t < r$:

*   Immediately switch to **D** regardless of past history. This ensures extraction of remaining value before the pool reaches a non-renewable state due to group over-consumption.
*   If, after switching to **D** due to low stock, the stock recovers to $S_t > \text{capacity} / 2$ in the subsequent round, revert to the conditional logic ($k \ge \lceil n/2 \rceil \to C$).

**Pseudocode Implementation:**

```python
def make_decision(round_number, current_stock, last_round_cooperators, n, r, capacity):
    # Terminal phase logic
    if round_number == r:
        return 'D'

    # Resource exhaustion protection
    if current_stock < (capacity / (2 * n)):
        return 'D'

    # Initial round
    if round_number == 1:
        return 'C'

    # Tit-for-Tat conditional logic
    # Assume 'n' players total, so n-1 opponents.
    # Cooperators observed from last_round_cooperators (which represents count of C among n-1 opponents)
    if last_round_cooperators >= (n - 1) / 2:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_8 = '''
Maintain a state variable `reputation` initialized to 0, representing the observed cooperative behavior of the population. In each round `t`, track the number of cooperators from the previous round `c_{t-1}`. Update `reputation` as `reputation = (reputation * 0.7) + (c_{t-1} / n * 0.3)`.

**Decision Logic:**

1.  **Terminal Phase:** If `t == r` (the final round), choose **Defect (D)**. Regardless of state or history, maximizing immediate consumption is optimal when no future rounds exist to leverage the stock.

2.  **Initial Phase:** If `t == 1`, choose **Cooperate (C)**. This preserves the resource stock to ensure high-value consumption in subsequent rounds.

3.  **Adaptive Phase (Rounds 2 to r-1):**
    *   Let `growth_potential` be defined as the current stock `S`. If `S < (capacity * 0.25)`, the stock is critically depleted. Defect to extract remaining value before collapse.
    *   If `S >= (capacity * 0.25)`:
        *   Calculate the moving average of cooperation: `reputation`.
        *   If `reputation > 0.6`, choose **Cooperate (C)**. The cooperative signal from opponents suggests they are likely to sustain the stock; reciprocating this maintains the long-term yield.
        *   If `reputation <= 0.6`, choose **Defect (D)**. The resource is being depleted by the aggregate population, so individual maximization requires accelerating extraction before the stock reaches zero.

**Edge Cases:**
*   If `S == 0`, the strategy defaults to **Defect (D)**, as there is no stock to preserve and no potential for growth.
*   If `S` is very high (near `capacity`), bias toward **Cooperate (C)** unless `reputation` falls below 0.3, in which case switch to **Defect (D)** to capture the surplus before others inevitably deplete it.
'''

description_SELFISH_9 = '''
The strategy employs a Conditional Trigger approach aimed at maximizing accumulated individual payoff by maintaining the resource stock near the capacity level while punishing defection to deter depletion.

### Decision Rules

1.  **Round 1:**
    *   Always play **C**.

2.  **Rounds 2 to $r-1$:**
    *   Let $N_C$ be the number of cooperators in the previous round, observed by the aggregate count.
    *   Let $S_t$ be the stock at the start of the current round $t$.
    *   If $S_t < \text{capacity} / 2$:
        *   Always play **C** (Conservation Mode: allow stock recovery).
    *   Else if $N_C = n$ (Everyone cooperated in the previous round):
        *   Play **C** (Maintaining sustainability).
    *   Else if $N_C < n$:
        *   Play **D** (Retaliatory Defection: if others deplete the pool, secure a larger share before the stock collapses).

3.  **Last Round ($r$):**
    *   Always play **D** (Terminal Defection: maximize payoff, as no future rounds exist to incentivize cooperation).

### Edge Cases and State Logic

*   **Stock Collapse Recovery:** If $S_t$ falls below a critical threshold (defined as any value where potential growth is mathematically unable to restore the pool to near-capacity within the remaining rounds), immediately switch to **D** for all remaining rounds to extract remaining value.
*   **Threshold Calculation:**
    *   Calculate potential recovery $R = 2 \times S_{\text{rem}} \times (1 - S_{\text{rem}}/\text{capacity})$.
    *   If $S_{\text{rem}} + R \cdot (r - t) < \text{capacity} / n$, assume the pool is depleted and play **D**.

### Pseudocode

```python
def get_action(round_number, total_rounds, current_stock, last_round_cooperators, n):
    # Rule 1: Terminal Round
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: First Round
    if round_number == 1:
        return 'C'
    
    # Rule 3: Recovery / Low Stock Protection
    # If stock is critically low, switch to aggressive extraction
    if current_stock < (capacity / n):
        return 'D'
        
    # Rule 4: Conditional Cooperation
    # Cooperate if everyone cooperated previously, or if stock is low enough
    # that preservation is necessary for future payoffs
    if last_round_cooperators == n or current_stock < (capacity / 2):
        return 'C'
    
    # Default: Punish defection
    return 'D'
```
'''

description_SELFISH_10 = '''
**Strategy: Conditional Sustainability (CS)**

This strategy operates as a Tit-for-Tat derivative modified for resource preservation, prioritizing immediate yield maximization while protecting the stock required for future high-yield rounds. It assumes that cooperation from others is fragile and that total stock depletion renders the game worthless.

**1. Definitions and Parameters**
*   **Cooperation Threshold ($T$):** Let $C_{count}$ be the number of opponents who cooperated in the previous round. Define a "Cooperation Threshold" $T = \lceil n/2 \rceil$.
*   **Stock Safety Buffer ($\delta$):** Define a minimum stock level below which long-term growth is jeopardized, $\delta = capacity / 4$.

**2. Decision Rules**
In any round $t < r$:
*   **If Current Stock $S < \delta$:** Always play **D** (Defect). If the stock is already critically low, future growth is inefficient or impossible; extract maximum value immediately.
*   **If Current Stock $S \ge \delta$:**
    *   **Round 1:** Play **C** (Cooperate). This establishes a baseline and tests opponent behavior without immediate depletion.
    *   **Rounds $t > 1$:**
        *   If $C_{count} \ge T$: Play **C** (Cooperate). Maintain the resource equilibrium.
        *   If $C_{count} < T$: Play **D** (Defect). If the majority are defecting, preemptively extract maximum value to avoid being the only player sacrificing yield for a dwindling resource.

**3. Edge Cases**
*   **The Final Round ($t = r$):** Always play **D** (Defect). There are no future rounds to benefit from resource preservation; immediate utility maximization is the dominant strategy regardless of the stock state or previous history.
*   **Stock Reset:** If the stock is $0$, the strategy effectively terminates (all future moves yield 0).
*   **Opponent Heterogeneity:** The strategy is agnostic to individual identity; it only tracks the aggregate count of $C$ actions from the previous round. If $C_{count}$ is unavailable, default to **D** to minimize risk.

**4. Pseudocode**

```python
def get_action(round, stock, prev_opponents_cooperated):
    # Always defect in the final round
    if round == r:
        return 'D'
    
    # Critical state: stock depleted below safety threshold
    if stock < (capacity / 4):
        return 'D'
    
    # First round: start with cooperation
    if round == 1:
        return 'C'
        
    # Adaptive phase: match majority behavior
    threshold = ceil(n / 2)
    if prev_opponents_cooperated >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_11 = '''
Initialize a "cooperation history" variable `H_c = 0` representing the estimated proportion of cooperative behavior by opponents.

**Round 1:**
Play **Cooperate (C)**.

**Subsequent Rounds:**
Calculate the stock regeneration threshold. Determine if the previous round resulted in a stock decrease by comparing the `new_stock` to the `previous_stock`. If the `new_stock` is strictly less than the `previous_stock`, identify the environment as "depleting"; otherwise, identify it as "sustainable."

Apply the following logic:

1.  **Terminal Phase:** If the current round `t` is the final round (`r`), play **Defect (D)**.
2.  **Punishment/Retaliation:** If `stock` < (capacity / 2), play **Defect (D)** to maximize immediate extraction before resource collapse.
3.  **Adaptive Response:**
    *   If `H_c` > 0.75, play **Cooperate (C)**.
    *   If `H_c` is between 0.25 and 0.75:
        *   If the previous round's `new_stock` < `previous_stock` (indicating depletion), play **Defect (D)**.
        *   If the previous round's `new_stock` >= `previous_stock`, play **Cooperate (C)**.
    *   If `H_c` < 0.25, play **Defect (D)**.

**Pseudocode for Updating Strategy State:**

```python
# After observing the number of opponents who cooperated (k_coop)
# Total number of opponents = n - 1
if t > 1:
    # Update running average of opponent cooperation
    H_c = (H_c * (t - 1) + (k_coop / (n - 1))) / t

# Decision Logic
if t == r:
    action = D
elif stock < (capacity / 2):
    action = D
elif H_c > 0.75:
    action = C
elif H_c >= 0.25:
    if stock_new < stock_old:
        action = D
    else:
        action = C
else:
    action = D
```
'''

description_SELFISH_12 = '''
Adopt a conditional "Tit-for-Tat with Resource Thresholds" strategy designed to maximize individual payoff by balancing immediate extraction with long-term stock sustainability.

**State Tracking**
- Maintain a variable `last_cooperation_rate` (the fraction of players who cooperated in the previous round).
- Track the `rounds_remaining` in the game.
- Monitor the current `stock` level.

**Decision Rules**

*   **Round 1:** Play **Cooperate (C)**. This preserves the stock for future rounds and establishes a cooperative baseline while preventing immediate resource collapse.

*   **Rounds 2 through (r-1):** 
    - If `stock` < (`capacity` / 4), play **Cooperate (C)**. At critically low levels, even defectors are forced to moderate; cooperating signals restraint and helps stabilize the pool to avoid depletion to zero, where future payoffs become impossible.
    - If `stock` >= (`capacity` / 4) and `last_cooperation_rate` > 0.5, play **Cooperate (C)**. Reciprocate cooperation as long as a majority of the population is maintaining the stock.
    - If `stock` >= (`capacity` / 4) and `last_cooperation_rate` <= 0.5, play **Defect (D)**. Punish the population for over-extraction. If others are depleting the pool rapidly, individual cooperation only subsidizes their consumption without preventing the collapse; capturing a larger share is the only rational choice.

*   **Final Round (r):** Always play **Defect (D)**. Regardless of stock level or prior history, there is no future benefit to conservation. Extract the maximum possible share immediately to capture the highest possible final payoff.

**Pseudocode Implementation**

```
function get_action(round, total_rounds, current_stock, last_cooperation_rate):
    if round == total_rounds:
        return D
    
    if round == 1:
        return C
    
    threshold = capacity / 4
    
    if current_stock < threshold:
        return C
    
    if last_cooperation_rate > 0.5:
        return C
    else:
        return D
```
'''

description_SELFISH_13 = '''
Maintain a target sustainable stock level of $S^* = 0.5 \times \text{capacity}$ to ensure growth replenishment. Play $C$ if the current stock $S$ is below a critical threshold $S_{crit} = 0.4 \times \text{capacity}$ or if the previous round's aggregate cooperation count suggests that playing $C$ will keep the stock above $S_{crit}$ in the next round. Otherwise, play $D$.

In the final round, always play $D$.

**Pseudocode:**

```python
# Parameters:
# n: number of players
# capacity: max capacity
# S: current stock
# last_round_cooperators: number of players who played C in the previous round
# r: total rounds
# current_round: current round number

S_crit = 0.4 * capacity

def decide_action():
    # 1. Final round termination logic
    if current_round == r:
        return D

    # 2. Defensive cooperation logic
    # If the stock is critically low, prioritize replenishment to prevent total depletion
    if S < S_crit:
        return C

    # 3. Opportunistic defection logic
    # If the stock is healthy, defect to maximize short-term payoff.
    # However, if aggregate cooperation in the last round was high enough
    # to likely keep the stock stable even if I defect, remain selfish.
    
    # Calculate projected next stock if I defect:
    # Consumption_C = S/(2n)
    # Consumption_D = S/n
    # Total_consumption = (last_round_cooperators * Consumption_C) + ((n - last_round_cooperators) * Consumption_D) + Consumption_D
    # If projected_next_stock > S_crit, I defect to harvest.
    
    # Simplified heuristic:
    # If stock is sufficiently high (> 0.7 * capacity), prioritize harvesting.
    if S > 0.7 * capacity:
        return D
        
    # Default to conditional cooperation
    if last_round_cooperators >= (n / 2):
        return C
    else:
        return D
```

**Decision Logic Refinement:**
*   **First Round:** Play $C$ to build stock momentum, assuming other rational actors are also seeking to establish sustainability.
*   **Edge Cases:** If $S \approx 0$, play $C$ exclusively until $S \ge S_{crit}$. If $S \approx \text{capacity}$, play $D$ to maximize immediate extraction, as the stock has excess buffer capacity for growth.
*   **Selfish Maximization:** The strategy treats the resource pool as a finite asset. It switches between $C$ (investment in future capacity) and $D$ (extraction) based solely on whether current stock levels require replenishment to sustain future payoffs. It minimizes altruism by only cooperating when the stock is threatened, defaulting to defection as soon as the stock is healthy.
'''

description_SELFISH_14 = '''
In round 1, play Cooperate (C).

For all subsequent rounds $t > 1$, define the observed cooperators from the previous round $t-1$ as $C_{t-1}$ (where $0 \le C_{t-1} \le n$). Calculate the current stock $S_t$.

The strategy follows a conditional tit-for-tat approach modified by a threshold-based depletion avoidance rule:

1. **Defection Trigger:**
   If at any point the stock $S_t$ falls below a critical threshold $S_{crit} = \text{capacity} \times 0.25$, immediately play Defect (D) for the remainder of the game.

2. **Tit-for-Tat Adaptation:**
   If $S_t \ge S_{crit}$, determine action based on the previous round's cooperation level:
   - If the number of cooperators in the previous round $C_{t-1} \ge n-1$ (meaning everyone cooperated or only one person defected), play C.
   - If $C_{t-1} < n-1$, play D.

3. **Endgame:**
   In the final round $t=r$, always play Defect (D), regardless of previous history or current stock level, to extract maximum utility before the game terminates.

**Pseudocode:**

```python
if round == r:
    return D
if stock < (capacity * 0.25):
    return D
if round == 1:
    return C
if cooperators_previous_round >= (n - 1):
    return C
else:
    return D
```
'''

description_SELFISH_15 = '''
Define the strategy `SelfishOptimizer` with the following parameters:
- `history`: A record of previous rounds, specifically the total stock at the start of each round and the count of cooperating opponents.
- `threshold_stock`: A value defined as `capacity * 0.5`. This represents the "safety zone" where regeneration is maximized.
- `last_round`: The final round index `r`.

**Decision Rules:**

1. **Initialization (Round 1):**
   - Play **Cooperate (C)**. This preserves stock for future rounds, ensuring higher potential payouts later.

2. **Main Loop (Rounds 2 to r-1):**
   - If `stock` < `threshold_stock`:
     - Play **Cooperate (C)** regardless of previous opponent behavior. The stock is too low to survive exploitation; aggressive consumption will deplete the pool and collapse future payoffs.
   - If `stock` ≥ `threshold_stock`:
     - Calculate the `cooperation_rate` of opponents in the previous round: `num_cooperators / (n - 1)`.
     - If `cooperation_rate` > 0.5:
       - Play **Defect (D)**. The resource is healthy and the majority is cooperating, allowing for maximum exploitation without causing a total collapse in the immediate next step.
     - If `cooperation_rate` ≤ 0.5:
       - Play **Cooperate (C)**. The majority is defecting; defecting alongside them risks depleting the stock to a level where regeneration becomes negligible, destroying the long-term value.

3. **Termination (Round r):**
   - Play **Defect (D)**. With no future rounds, there is no value in preserving the stock. Exhaust all remaining resources immediately to maximize the final round payoff.

**Pseudocode:**

```python
def decide_action(round_index, current_stock, prev_opp_coop_count, n, r, capacity):
    # Rule 3: Final round grab
    if round_index == r:
        return 'D'
    
    # Rule 1: First round setup
    if round_index == 1:
        return 'C'
    
    # Rule 2: Dynamic state-based logic
    threshold_stock = capacity * 0.5
    
    if current_stock < threshold_stock:
        return 'C' # Preserve to prevent extinction
    
    # Analyze opponent cooperation rate
    # num_opponents = n - 1
    cooperation_rate = prev_opp_coop_count / (n - 1)
    
    if cooperation_rate > 0.5:
        return 'D' # Exploit while resource is healthy and others contribute
    else:
        return 'C' # Rebuild resource when others are depleting it
```
'''

description_SELFISH_16 = '''
### Strategy: Sustainable Extraction Equilibrium

This strategy maintains the stock level at exactly `capacity / 2`, as this maximizes the growth rate of the common pool, thereby ensuring the largest possible per-round resource base for future consumption. The strategy approximates a Tit-for-Tat mechanism with a threshold adjustment based on the stock level.

**Decision Rules**

In any given round `t` with current stock `S` and `r - t` rounds remaining:

1.  **Threshold Calculation:** Calculate the target consumption level `C_target` that keeps the stock `S` at or near `capacity / 2`.
    *   Let `n_C` be the number of cooperators observed in the previous round.
    *   Define `action_t` as:
        *   **Cooperate (C)** if `S >= capacity / 2` and the observed cooperation rate from the previous round was high (i.e., `n_C / n >= 0.5`).
        *   **Defect (D)** if `S < capacity / 2` or if the observed cooperation rate from the previous round was low (i.e., `n_C / n < 0.5`).

2.  **End-Game Adjustment:**
    *   In the final round `t = r`: Defect regardless of the stock level or previous history. Maximize immediate payoff as there is no future utility to protect.

3.  **Initialization (Round 1):**
    *   Cooperate (C). This establishes a baseline for potential cooperation with other agents, signaling a preference for sustainable growth.

**Pseudocode Logic**

```python
def choose_action(round_t, total_rounds, current_stock, capacity, n, n_cooperators_prev):
    # Rule 1: Final Round
    if round_t == total_rounds:
        return "D"

    # Rule 2: First Round
    if round_t == 1:
        return "C"

    # Rule 3: Maintain equilibrium
    # If stock is healthy, reciprocate cooperation
    if current_stock >= (capacity / 2):
        if (n_cooperators_prev / n) >= 0.5:
            return "C"
        else:
            # Defect if others are depleting the pool excessively
            return "D"
    
    # If stock is depleted, prioritize survival or maximize remaining yield
    else:
        return "D"
```

**Edge Case Handling**

*   **Stock Depletion:** If the stock drops below the sustainable threshold (`S < capacity / 2`), the strategy switches to permanent defection (`D`). This is based on the logic that if other players are failing to maintain the pool, individual attempts to cooperate are futile; harvesting the remaining resource before the pool collapses is the rational selfish choice.
*   **Reciprocity:** The strategy monitors the collective action of opponents (`n_C`). If more than half the table defects, the strategy assumes the pool is doomed and switches to defection to avoid being the only player sacrificing yield for a collective good that others are undermining.
'''

description_SELFISH_17 = '''
Define the state variable $k$ as the number of opponents who cooperated in the previous round, where $0 \le k \le n-1$. Let $c_t$ be the action taken at time $t$ ($1$ for Cooperate, $0$ for Defect).

**Decision Rule:**

1.  **First Round ($t=1$):** Play **Cooperate**. This initiates a "tit-for-tat" baseline, testing if the environment supports cooperative equilibrium.

2.  **Intermediate Rounds ($1 < t < r$):**
    *   Calculate the "Sustainability Threshold": If current stock $S_t < (\text{capacity} / 2)$, immediately switch to **Defect** regardless of history, as the resource is collapsing.
    *   If $S_t \ge (\text{capacity} / 2)$, check the cooperation rate of the opponents in the previous round. If $k = n-1$ (all opponents cooperated), play **Cooperate**.
    *   If $k < n-1$ (at least one opponent defected), play **Defect**.
    *   **Exception:** If the strategy previously switched to **Defect** due to $k < n-1$, it may attempt to "re-seed" cooperation. If playing **Defect** leads to a stock recovery such that $S_t > 0.9 \times \text{capacity}$, play **Cooperate** for one round to test if the opponents have returned to cooperation. If they do not reciprocate, revert to **Defect** immediately.

3.  **Final Round ($t = r$):** Play **Defect**. Because there are no future consequences or retaliation possibilities, capturing the maximum share of the remaining stock is the optimal selfish choice.

**Pseudocode:**

```python
def choose_action(round, total_rounds, current_stock, capacity, opponents_cooperated, last_action):
    # Final round: Always defect to maximize final payoff
    if round == total_rounds:
        return "Defect"

    # Sustainability check: If stock is low, exploit to salvage value before collapse
    if current_stock < (capacity / 2):
        return "Defect"

    # First round: Cooperate to signal potential for sustainable yield
    if round == 1:
        return "Cooperate"

    # Tit-for-Tat logic: 
    # If all opponents cooperated last round, continue cooperating
    if opponents_cooperated == (n - 1):
        return "Cooperate"
    
    # If at least one opponent defected, retaliate
    # Check for re-seeding opportunity:
    if last_action == "Defect" and current_stock > (0.9 * capacity):
        return "Cooperate" # Probe for cooperation
        
    return "Defect"
```
'''

description_SELFISH_18 = '''
The strategy operates on a "Tit-for-Tat with Resource Constraints" logic, designed to maintain a sustainable stock level while exploiting high-cooperation environments. Let $C_t$ be the number of cooperators observed in round $t-1$, $N$ be the total number of players, and $S_t$ be the current stock.

**Strategy Logic**

1.  **Phase 1: Exploration (Round 1)**
    *   Play $C$. This establishes a baseline for cooperation and preserves the resource for subsequent turns.

2.  **Phase 2: Adaptive Response (Rounds 2 to $r-1$)**
    *   **Sustainability Threshold:** If $S_t < \text{capacity} \times 0.2$, play $D$ regardless of history. The resource is nearing collapse; prioritize immediate extraction over future growth.
    *   **Reciprocity:** If $S_t \ge \text{capacity} \times 0.2$:
        *   If the number of cooperators in the previous round ($C_{t-1}$) was $\ge N/2$, play $C$. This rewards group cooperation and keeps the resource replenishing.
        *   If $C_{t-1} < N/2$, play $D$. This maximizes immediate payoff in an environment where defectors are prevalent and the stock is being depleted by others.

3.  **Phase 3: Finality (Round $r$)**
    *   Regardless of previous history or current stock, play $D$. In the final round, there is no future stock to preserve, rendering the long-term benefit of $C$ null.

**Pseudocode**

```python
def get_action(round, total_rounds, n, capacity, current_stock, prev_cooperators):
    # Rule 1: Always defect in the final round
    if round == total_rounds:
        return 'D'

    # Rule 2: Always cooperate in the first round
    if round == 1:
        return 'C'

    # Rule 3: Sustainability Check
    if current_stock < (capacity * 0.2):
        return 'D'

    # Rule 4: Tit-for-Tat conditional on majority
    if prev_cooperators >= (n / 2):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_19 = '''
Initialize `trust_level` = 0.5.
Initialize `reputation_threshold` = 0.5.

For each round `t` from 1 to `r`:
1.  **Decision Rule:**
    If `t == 1`:
        Play Cooperate (C).
    Else if `t == r`:
        Play Defect (D).
    Else:
        If `stock < (capacity / n)`:
            Play Defect (D).
        Else:
            Determine `k` (the number of cooperating opponents in round `t-1`).
            Calculate `observed_cooperation_rate` = `k / (n - 1)`.
            Update `trust_level` = `(0.9 * trust_level) + (0.1 * observed_cooperation_rate)`.
            
            If `trust_level >= reputation_threshold`:
                Play Cooperate (C).
            Else:
                Play Defect (D).

2.  **Edge Case Logic:**
    *   If `stock` drops below 10% of `capacity` at any point during `t < r`, immediately switch to Defect (D) for the remainder of the game to extract remaining utility before depletion.
    *   If `observed_cooperation_rate` is consistently 0 for two consecutive rounds, set `reputation_threshold` to 1.0 (effectively forcing Defect for all future rounds).
    *   If `n` is large (n > 10) and `trust_level` dips below 0.3, transition to a "tit-for-tat" variant: always play Defect if `k` < 1.
'''

description_SELFISH_20 = '''
**Decision Logic**

The strategy employs a conditional "Tit-for-Tat" variant based on the observed aggregate cooperation rate of opponents. It prioritizes maximizing immediate individual yield while attempting to maintain the common pool at a level that supports future extraction.

Define:
*   $k$: Number of opponents who chose $C$ in the previous round.
*   $n$: Total number of players.
*   $S_t$: Current stock level at the start of round $t$.
*   $R_{rem}$: Number of rounds remaining.

**Rules:**

1.  **Initialization (Round 1):**
    *   Play $C$ to test for mutual cooperation and build initial stock stability.

2.  **Steady State (Rounds $2$ to $R_{rem} > 0$):**
    *   Calculate the "Sustainability Threshold": If $S_t \leq \frac{capacity}{2}$, play $C$. This prevents total resource collapse, which guarantees zero future payoff.
    *   If $S_t > \frac{capacity}{2}$:
        *   If the aggregate behavior of opponents in the previous round indicates sufficient cooperation (defined as $k \geq \frac{n-1}{2}$), play $C$ to sustain the pool.
        *   If the aggregate behavior of opponents indicates insufficient cooperation (defined as $k < \frac{n-1}{2}$), play $D$. This maximizes immediate individual extraction before the stock is inevitably depleted by free riders.

3.  **Terminal Phase (Final Round):**
    *   Play $D$ regardless of previous history or stock level. There is no future round to preserve, making $C$ strictly dominated by $D$ in the final round.

**Decision Algorithm:**

```python
if current_round == last_round:
    return D

if stock <= (capacity / 2):
    return C

# Determine opponent cooperation rate
if previous_round_cooperators >= (n - 1) / 2:
    return C
else:
    return D
```
'''

description_SELFISH_21 = '''
**Strategy: Conditional Sustainability-Maximization**

This strategy treats the common pool as an asset to be harvested at the maximum sustainable yield, while identifying and exploiting defectors to prevent unilateral losses.

**Decision Rules**

In each round $t$, calculate the *Sustainable Consumption Threshold* ($T_t$). Let $S_t$ be the current stock. The target stock for maximum growth is $S_{target} = capacity / 2$.

1.  **Phase 1: Cooperation**
    Play **C** if and only if the current stock $S_t$ is below or approaching the capacity-depletion danger zone ($S_t < S_{threshold}$) and the observed cooperation rate of opponents in round $t-1$ was $\geq 50\%$.

2.  **Phase 2: Retaliation/Exploitation**
    Play **D** if:
    *   The observed cooperation rate in round $t-1$ was $< 50\%$.
    *   The current stock $S_t$ is sufficient to support a higher payoff without immediate collapse ($S_t > capacity / 4$).
    *   It is the final round ($t = r$).

3.  **Phase 3: Trigger for Extinction**
    If the stock $S_t$ falls below $capacity / (2n)$, play **D** regardless of past history. When the resource is insufficient to sustain long-term growth, the dominant selfish strategy is to capture remaining value before depletion.

**Pseudocode Implementation**

```python
def choose_action(round_number, stock, history):
    # Base case: Last round, always defect for immediate gain
    if round_number == r:
        return 'D'
    
    # Emergency case: Stock too low for recovery, harvest remaining
    if stock < (capacity / (2 * n)):
        return 'D'

    # First round: Cooperate to build/maintain stock
    if round_number == 1:
        return 'C'

    # Observe previous round behavior
    previous_cooperators = history[round_number - 1].opponents_cooperated
    total_opponents = n - 1
    
    # Tit-for-Tat adaptation
    if previous_cooperators / total_opponents >= 0.5:
        # Sufficient cooperation exists to keep stock growing
        return 'C'
    else:
        # Defectors present; switch to Defect to mitigate loss
        return 'D'
```

**Edge Case Handling**

*   **Round 1:** Default to **C**. Establishing the resource base is necessary for higher long-term payoffs.
*   **The Final Round ($t = r$):** Always play **D**. There is no future round to preserve the stock for, so the "Cooperate" benefit is nullified.
*   **Low Stock ($S_t \approx 0$):** If the pool is essentially exhausted, play **D**. The resource growth function implies that if $S$ is near zero, $S_{next} \approx 0$ regardless of action. Defecting ensures you capture the maximum possible share of the remaining stock before the game ends.
*   **Opponent Fluctuation:** If the population is volatile, this strategy defaults to **D** after a single round of low cooperation ($< 50\%$), effectively punishing the group to minimize your disadvantage when others fail to preserve the stock.
'''

description_SELFISH_22 = '''
The strategy relies on maintaining the "Sustainability Threshold" (ST), defined as the stock level where collective cooperation (all C) results in stock replenishment to capacity, and partial defection results in stock decline.

**Core Decision Rule:**
In each round $t < r$, cooperate if the stock level $S_t$ is below the threshold $S_{target} = capacity \times 0.75$, and defect if $S_t \ge S_{target}$. In the final round $t = r$, always defect.

**Adaptive Mechanism:**
Track the average cooperation rate of the population, $C_{avg}$, defined as the number of cooperators observed in the previous round divided by $n$. Adjust the threshold $S_{target}$ based on opponent behavior:

1.  **Initialization:** In $t=1$, cooperate if $S_1 < S_{target}$, otherwise defect.
2.  **Tracking:** After each round, calculate $C_{avg} = \frac{k}{n}$, where $k$ is the number of observed cooperators.
3.  **Observation Feedback:**
    *   If $C_{avg} > 0.5$ (the population is mostly cooperative), maintain $S_{target} = capacity \times 0.75$.
    *   If $C_{avg} \le 0.5$ (the population is mostly defecting), decrease the threshold $S_{target}$ by 10% of capacity to preserve stock more aggressively or, if $S_{target}$ hits a lower bound of $capacity \times 0.25$, defect continuously until the stock recovers or the game ends.
4.  **Defection Trigger:** Regardless of $S_t$, defect if $S_t$ falls below $capacity \times 0.1$. In this scenario, the resource is collapsing regardless of your choice; defecting extracts the remaining value before total depletion occurs.

**Pseudocode:**

```python
# Parameters
S_target_base = capacity * 0.75
S_target_min = capacity * 0.25
S_collapse_threshold = capacity * 0.1
S_target = S_target_base

def decide_action(round_num, S_current, history):
    # Final round greed
    if round_num == r:
        return D
    
    # Observe population behavior from previous round
    if round_num > 1:
        prev_k = history[-1].cooperators_count
        C_avg = prev_k / n
        
        # Adjust target based on population reliability
        if C_avg <= 0.5:
            S_target = max(S_target_min, S_target - (capacity * 0.1))
        else:
            S_target = S_target_base

    # Collapse imminent: extract value
    if S_current < S_collapse_threshold:
        return D

    # Sustainability logic
    if S_current < S_target:
        return C
    else:
        return D
```

**Edge Cases:**
*   **First Round ($t=1$):** Default to $C$ to test population cooperativeness, as the initial stock is $capacity$.
*   **High Initial Defection:** If the first round results in a massive stock drop (growth rate becomes negative), immediately switch to $D$ for the remainder of the game, as the common pool is effectively a "tragedy of the commons" scenario.
*   **Stock Equilibrium:** If the stock stabilizes exactly at $S_{target}$, maintain $C$ to sustain the resource, provided $C_{avg} \ge 0.5$.
'''

description_SELFISH_23 = '''
The strategy operates on a Tit-for-Tat foundation modified by a threshold-based sustainability check, prioritizing long-term payout maximization through the maintenance of the resource stock. 

**Decision Rules:**

1.  **Sustainability Threshold:** Calculate the "Safe Consumption Limit." If all players cooperate, total consumption is $n \times (S / 2n) = S/2$, leaving $S/2$ in the pool. For the stock to regenerate to capacity (or remain stable at capacity), the stock after consumption must be at least $S/2$. If the current stock $S$ is below a critical threshold (defined as $S < 0.2 \times \text{capacity}$), defecting is irrational because the pool is already exhausted; thus, defect immediately to extract remaining value before depletion.

2.  **Adaptive Cooperation:**
    *   **Round 1:** Play C. Establishing cooperation provides the highest probability of long-term stock sustainability.
    *   **Subsequent Rounds:** Observe the total number of cooperators ($C_{obs}$) from the previous round.
        *   If $C_{obs} = n - 1$ (everyone except perhaps you cooperated) or $C_{obs} = n$ (full cooperation): Play C.
        *   If $C_{obs} < n - 1$: Play D. 
    *   **Recovery:** If the strategy has been playing D due to a low $C_{obs}$, play D until the stock $S$ recovers to at least $0.5 \times \text{capacity}$, then revert to C to test if cooperation can be re-established.

3.  **End-Game:**
    *   In the final round ($t = r$), play D regardless of history. The future value of the stock is zero; extraction maximization is the only rational behavior.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, current_stock, capacity, last_round_cooperators, n):
    # End-game extraction
    if round_number == total_rounds:
        return D

    # Immediate depletion check
    if current_stock < (0.2 * capacity):
        return D

    # Recovery mode: if stock is depleted, extract until it's sustainable
    if current_stock < (0.5 * capacity) and last_round_cooperators < (n - 1):
        return D

    # Tit-for-Tat logic
    if round_number == 1:
        return C
    
    if last_round_cooperators >= (n - 1):
        return C
    else:
        return D
```
'''

description_SELFISH_24 = '''
**Strategy Description: Adaptive Sustainable Extraction**

The strategy maximizes personal payoff by maintaining the resource stock at levels that maximize future yield (specifically the capacity level) while defecting when the environment permits depletion without jeopardizing long-term gains.

**State Variables:**
*   $S_t$: Stock at start of round $t$.
*   $k$: Number of observed cooperators in the previous round $t-1$.
*   $N$: Total number of players.
*   $D_t$: The decision for the current round $\in \{C, D\}$.
*   $TargetStock$: $Capacity / 2$.

**Decision Logic:**

1.  **Initialization (Round 1):**
    Play **C**. The initial stock is at capacity, providing the highest possible dividend for cooperation, while simultaneously gauging the collective restraint of the other players.

2.  **General Round Logic ($t > 1$):**
    Calculate the potential $NextStock$ if everyone were to cooperate ($C$):
    $S_{after\_consumption} = S_t - (N \times (S_t / 2N)) = S_t / 2$
    $Growth = 2 \times (S_t / 2) \times (1 - (S_t / 2) / Capacity) = S_t \times (1 - S_t / 2 \times Capacity)$
    $NextStock = \min(S_t/2 + Growth, Capacity)$

    *   **Condition A (Sustainable Threshold):** If $S_t \leq (Capacity \times 0.5)$, play **C**. This is necessary to prevent total collapse ($S=0$), which results in zero future payoffs.
    *   **Condition B (Exploitation Phase):** If $S_t > (Capacity \times 0.5)$ AND $k > (N/2)$, play **D**. If the majority are cooperating, the stock is growing or stable; defecting captures a larger share of the surplus without causing a collapse.
    *   **Condition C (Punishment/Retaliation):** If $S_t > (Capacity \times 0.5)$ AND $k \leq (N/2)$, play **C**. When the stock is healthy but the other players are also defecting, total depletion is imminent. Cooperation is required to recover the stock to a harvestable level.

3.  **End-Game Logic (Rounds $t$ where remaining rounds $r-t < 2$):**
    Ignore sustainability. Defect (**D**) in the final two rounds regardless of state or history to extract maximum remaining stock, as there is no future to preserve.

**Edge Cases:**
*   If $S_t \approx 0$ (within a tolerance of $0.001$), play **C** to allow any residual recovery, though expect a zero payoff.
*   If $k$ is unknown (e.g., first round), assume $k = N-1$ for the purposes of estimating stock health, but strictly follow the $S_t$ thresholds.
'''

description_SELFISH_25 = '''
Define the "Target Sustainability Level" (TSL) as 0.5 * capacity. This is the inflection point where the stock growth rate is maximized (logistic growth derivative is highest at half-capacity).

Maintain a rolling memory of the previous round's outcome, specifically the number of defectors ($k_t$), where $k_t \in \{0, 1, ..., n-1\}$ represents the count of opponents who defected.

**Decision Rules:**

1.  **Round 1:** Always choose Cooperate (C). Establishing cooperation is necessary to ensure the stock remains high enough to exploit in later rounds.

2.  **Rounds 2 through $r-1$:**
    *   Calculate the "Growth Safety Margin": If the current stock ($S_t$) is $\leq$ TSL, play C. This preserves the resource base.
    *   Calculate "Defector Threshold": If $S_t >$ TSL, play C if $k_{t-1} \leq \lfloor (n-1)/2 \rfloor$. This encourages cooperative behavior when the resource is abundant, provided the majority of opponents are not defecting.
    *   Default to Defect (D) if $S_t >$ TSL AND $k_{t-1} > \lfloor (n-1)/2 \rfloor$. If opponents are defecting while the resource is high, extract maximum value before the stock is depleted.

3.  **Final Round ($r$):** Always choose Defect (D), regardless of the stock level or history. The future value of the stock is zero after the final round, so maximizing immediate extraction is the optimal selfish move.

**Edge Cases & Adjustments:**

*   **Critical Depletion:** Regardless of the rules above, if $S_t < (S_{t-1} * 0.2)$, immediately play C for all subsequent rounds until $S_t$ returns above $0.3 * \text{capacity}$. This ensures the resource does not hit zero, which would terminate all future payoff potential.
*   **Opponent Defection:** If the system observes that $k_t = n-1$ (all opponents are defecting) for two consecutive rounds, switch to Defect (D) immediately for all subsequent rounds, assuming the resource is headed for total collapse regardless of personal intervention.
'''

description_SELFISH_26 = '''
Initialize `k = 0` (previous round cooperation count).
Define a "Defection Threshold" `T = (n - 1) / n`.

Round 1:
Play Cooperate (C).

Rounds 2 to `r - 1`:
Calculate `S_t`, the stock level at the start of the current round.
If `S_t` < `capacity * 0.25`:
    Play Defect (D) to extract remaining value before depletion.
Else if the proportion of cooperators in the previous round `k/n` < `T`:
    Play Defect (D) to maximize short-term payoff.
Else:
    Play Cooperate (C) to maintain sustainable stock growth.

Round `r`:
Play Defect (D).

Pseudocode for round `t` (where 1 < `t` < `r`):

```python
def decide_action(stock, previous_cooperators, n, capacity):
    # Short-term depletion logic
    if stock < (0.25 * capacity):
        return D
    
    # Sustainability check
    # Defect if the group fails to sustain a sufficient cooperation level
    cooperation_ratio = previous_cooperators / n
    if cooperation_ratio < ((n - 1) / n):
        return D
        
    return C
```
'''

description_SELFISH_27 = '''
In round 1, play C.

In subsequent rounds (2 through r), calculate the "Growth-Neutral Stock Level" (GNSL), defined as the stock level S such that the new stock equals the current stock S after consumption and growth. Let K = capacity. Since total consumption depends on the number of cooperators (C_count) and defectors (D_count = n - C_count), the remaining stock is S - (C_count * S/2n + (n - C_count) * S/n). Simplifying, S_rem = S * (1 - (C_count + 2n - 2*C_count) / 2n) = S * (1 - (2n - C_count) / 2n) = S * (C_count / 2n).
The GNSL for a given composition of players is the S satisfying S = (S * C_count/2n) + 2 * (S * C_count/2n) * (1 - (S * C_count/2n) / K).

For each round t > 1, determine the action based on the previous round's outcome:

1.  **Observation:** Let C_prev be the number of cooperators in the previous round.
2.  **Sustainability Check:** If the current stock S <= (K / (n^2)), play D. This threshold assumes that defecting now maximizes immediate utility before the stock crashes to zero, as the stock is insufficient to recover effectively.
3.  **Reciprocity Rule:** If the previous round’s action by the collective was predominantly cooperative (where C_prev >= n/2), play C. The collective is maintaining or growing the stock sufficiently to justify continued participation.
4.  **Punishment/Defection Rule:** If the previous round’s action was predominantly defective (C_prev < n/2), play D. The resource is being depleted by the collective; shift to maximizing individual extraction immediately.
5.  **Final Round (t = r):** Regardless of history, if S > 0, play D. In the final round, there is no future stock growth to preserve, so extract the maximum possible share.

Pseudocode:
```python
if t == r:
    return D
if t == 1:
    return C
if stock <= (capacity / (n**2)):
    return D
if C_prev >= (n / 2):
    return C
else:
    return D
```
'''

description_SELFISH_28 = '''
Define $TargetStock = \text{capacity} \times 0.5$.

In each round $t$ with current stock $S$ and observed number of cooperators from round $t-1$ as $k_{t-1}$:

1. **Initialization:**
   If $t = 1$, play **Cooperate (C)**.

2. **Last Round:**
   If $t = r$, play **Defect (D)** regardless of history, as there are no future consequences to preserve the stock.

3. **Steady State Monitoring:**
   If $t > 1$ and $t < r$, calculate the stock growth trajectory. Define the "Safe Depletion Threshold" as the consumption level that maintains the stock at or above $TargetStock$ in the next round, given the most recent observed behavior.

   Let $S_{rem} = S - (k_{t-1} \times \frac{S}{2n} + (n-k_{t-1}) \times \frac{S}{n})$.
   Let $S_{next} = \min(\text{capacity}, S_{rem} + 2 \times S_{rem} \times (1 - \frac{S_{rem}}{\text{capacity}}))$.

   If $S_{next} < TargetStock$ or $S < \text{capacity} \times 0.25$:
   Play **Defect (D)**. The resource is collapsing or insufficient; maximize immediate extraction before depletion.

   Otherwise, if $k_{t-1} < n$ (some players are defecting):
   Play **Defect (D)**. Retaliate against the defectors to prevent free-riding.

   If $k_{t-1} == n$ (everyone cooperated in the previous round):
   Play **Cooperate (C)**. Maintain the resource base to ensure long-term extraction capacity.

**Pseudocode:**

```python
if t == r:
    return D

if t == 1:
    return C

# Calculate projected stock health
S_rem = S - (k_prev * (S/(2*n)) + (n - k_prev) * (S/n))
S_next = min(capacity, S_rem + 2 * S_rem * (1 - S_rem / capacity))

# Decision logic
if S_next < (capacity * 0.5) or S < (capacity * 0.25):
    return D
elif k_prev < n:
    return D
else:
    return C
```
'''

description_SELFISH_29 = '''
Maintain a memory of the previous round's outcome, tracking the total number of cooperators observed in the prior round ($C_{t-1}$). Initialize a strategy state based on a tit-for-tat variant calibrated to sustain the resource while maximizing extraction.

Decision rules:

1.  **First Round (t=1):** Always play C (Cooperate). This establishes a baseline of resource preservation to maximize the stock for subsequent, more lucrative rounds.

2.  **Subsequent Rounds (t > 1):**
    *   Calculate the current stock ratio $\rho = S_t / \text{capacity}$.
    *   If $\rho < 0.25$: Defect (D) unconditionally. When the resource is critically low, extraction priority shifts to immediate payoff before the stock collapses.
    *   If $\rho \geq 0.25$: Cooperate (C) if and only if the number of cooperators in the previous round ($C_{t-1}$) was greater than or equal to $n - 1$. 
    *   If $C_{t-1} < n - 1$: Defect (D). This punishes the group for previous over-extraction by maximizing individual share before the stock potentially declines further.

3.  **Last Round (t = r):** Always play D (Defect). Since there is no future utility for the stock, maximize individual consumption without regard for resource regeneration.

4.  **Edge Case - Stock Collapse:** If $S_t = 0$, play D (Defect) regardless of previous rounds, as the game effectively terminates or provides no further value for future cooperation.
'''

description_SELFISH_30 = '''
**Strategy: Threshold-Based Sustainable Exploitation (TBSE)**

The objective is to maximize cumulative payoff by maintaining the common pool stock at the "Golden Ratio" of maximum regeneration—50% of capacity—where growth is maximized, while simultaneously defecting whenever the state permits high-yield extraction without triggering total resource collapse.

**Decision Rules**

Define $S_t$ as the stock at the start of round $t$, and $k$ as the number of cooperators observed in the previous round.

1.  **Safety Buffer Requirement:**
    Calculate the projected stock $S_{t+1}$ assuming $m$ players defect. If $S_t$ is below $0.25 \times \text{capacity}$, prioritize preservation to ensure the resource does not crash.
    *   If $S_t < 0.25 \times \text{capacity}$: Always play **C** to prevent extinction.

2.  **Greedy Exploitation:**
    If $S_t \ge 0.25 \times \text{capacity}$, determine the Defection-Cooperation boundary.
    *   Calculate the "Sustainability Threshold": If playing **D** in the current round would result in a remaining stock after growth $S_{t+1} < 0.5 \times \text{capacity}$ given the observed historical cooperation rate, switch to **C**.
    *   If the projected $S_{t+1} > 0.5 \times \text{capacity}$, play **D**.

3.  **Adaptive Response to Opponents:**
    Track the moving average of cooperation $C_{avg}$ from previous rounds.
    *   If $C_{avg} > 0.5$ (cooperative environment): Adopt a "Tit-for-Tat" variant. Play **D** only every other round to maximize yield while keeping the stock replenished.
    *   If $C_{avg} \le 0.5$ (exploitative environment): Immediately play **D** to extract value before the resource is depleted by opponents.

**Edge Cases**

*   **Round 1:** Play **C**. This provides the data necessary to calibrate the environment and preserves initial stock for mid-game exploitation.
*   **Final Round (Round $r$):** Play **D** regardless of state. Future resource growth is irrelevant; capture the maximum possible share of the remaining stock.
*   **Total Collapse ($S \approx 0$):** If $S$ falls below a critical threshold where regeneration is impossible ($S < \epsilon$), defect in all remaining rounds.

**Pseudocode**

```python
def choose_action(round, total_rounds, current_stock, capacity, history):
    if round == total_rounds:
        return D
    
    if current_stock < 0.25 * capacity:
        return C
    
    avg_cooperation = sum(history) / len(history)
    
    # Project stock after playing D
    # Assuming current cooperation trend continues
    projected_consumption = (1 * (S/n)) + ((n-1) * avg_cooperation * (S/(2*n)))
    remaining = current_stock - projected_consumption
    growth = 2 * remaining * (1 - remaining / capacity)
    next_S = min(remaining + growth, capacity)
    
    if next_S > 0.5 * capacity:
        return D
    else:
        return C
```
'''

description_SELFISH_31 = '''
The strategy employs a "Conditional Sustainability" approach, prioritizing long-term yield over immediate extraction by monitoring the stock trajectory and responding to aggregate defection.

**State Variables**
- `n`: Number of players.
- `r`: Total rounds.
- `t`: Current round index (1 to `r`).
- `S_t`: Stock at the start of round `t`.
- `k_t`: Number of players who cooperated in round `t-1`.

**Decision Rules**

1. **Initial Phase (Round 1):**
   - Play **C (Cooperate)**. This establishes a baseline for sustainability.

2. **Ongoing Phase (Rounds 2 to r-1):**
   - Calculate the "Sustainable Stock Threshold" (`S_threshold`): Define `S_threshold` as `capacity / 2`.
   - If `S_t` < `S_threshold`: Play **D (Defect)**. If the stock is critically low and likely to crash, extraction is prioritized to secure individual payoff before the resource vanishes.
   - If `S_t` >= `S_threshold`:
     - Calculate the "Cooperation Rate" of the previous round: `ρ = k_t / n`.
     - If `ρ` >= 0.75: Play **C (Cooperate)**. If the majority is sustaining the resource, continue cooperation to maintain the state.
     - If `ρ` < 0.75: Play **D (Defect)**. If the group is defecting heavily, switch to defection to avoid being the sole provider of a resource that others are depleting.

3. **Terminal Phase (Round r):**
   - Play **D (Defect)** regardless of the stock level or previous history. Since there are no future rounds to benefit from, maximize the immediate payoff by consuming the maximum allowable portion.

**Pseudocode Logic**

```python
def choose_action(t, S_t, k_prev, n, r):
    # Terminal round: extract max
    if t == r:
        return D

    # Critical depletion: salvage what is left
    if S_t < (capacity / 2):
        return D

    # High-functioning pool: sustain
    if k_prev / n >= 0.75:
        return C

    # Default to extraction
    return D
```

**Edge Case Handling**
- **Low `n`:** The threshold for `ρ` remains constant. Even in small groups, the cost of sustained defection from even a single opponent is high enough to trigger the transition to D if the stock level does not justify the risk of continued cooperation.
- **Immediate Stock Depletion:** If `S_t` is negligible, the decision defaults to D, as the game's future value is zero and individual payoff is non-zero only via maximum extraction.
'''

description_SELFISH_32 = '''
### Strategy: Tit-for-Tat with Threshold-Based Defection

Maintain a state variable `trust_level`, initialized to 1.0. This variable represents the estimated propensity of the aggregate pool of opponents to cooperate. Adjust `trust_level` dynamically based on the observed proportion of cooperative actions in previous rounds.

**Decision Rules:**

1.  **First Round:** Play **Cooperate (C)** to establish a baseline for cooperation and maintain the stock for future yields.

2.  **Intermediate Rounds (2 to r-1):**
    *   Let $N_c$ be the number of opponents who cooperated in the previous round, and $n-1$ be the total number of opponents.
    *   Calculate the observed cooperation rate: $R_c = N_c / (n-1)$.
    *   Update `trust_level`: Set `trust_level` = $0.9 \times \text{trust\_level} + 0.1 \times R_c$.
    *   **Defection Trigger:** If `stock` falls below $0.4 \times \text{capacity}$ or if `trust_level` $< 0.4$, switch to **Defect (D)**.
    *   **Cooperation Resumption:** If `stock` $\ge 0.4 \times \text{capacity}$ and `trust_level` $\ge 0.5$, switch to **Cooperate (C)**.

3.  **Final Round (r):** Play **Defect (D)** regardless of state or history to maximize final payout, as there are no future rounds to influence.

**Edge Cases and Adjustments:**

*   **Low Stock Warning:** If `stock` is less than or equal to $0.1 \times \text{capacity}$ at the start of any round $t < r$, force **Defect (D)**. The resource is nearing collapse, and extracting maximum value before depletion is the optimal selfish move.
*   **Opponent Behavior:** If all opponents defected in the previous round ($N_c = 0$), immediately reset `trust_level` to 0 and switch to **Defect (D)** for the next round.
*   **Recovery:** If the strategy has been defecting due to low `trust_level` but the `stock` has recovered to $> 0.8 \times \text{capacity}$ due to aggregate player behavior, revert to **Cooperate (C)** for one round to test if cooperation is viable again.
'''

description_SELFINTERESTED_5 = '''
### Triggered Tit-for-Tat with Sustainability Constraints

**Objective:** Maintain stock near *capacity* to ensure long-term yield while punishing defectors who attempt to extract more than their fair share.

**Core Decision Logic:**
In each round $t$ with current stock $S_t$:

1. **Safety Threshold Check:** 
   If $S_t < \text{capacity} / 2n$, play **D** (Defect). When the pool is critically depleted, maximizing personal extraction is the only rational move as the pool's recovery is unlikely to benefit the player within the remaining rounds.

2. **Reputational Assessment (Tit-for-Tat):**
   If $S_t \ge \text{capacity} / 2n$:
   * **Round 1:** Play **C** (Cooperate).
   * **Subsequent Rounds:** Let $k$ be the number of cooperators in the previous round.
     * If $k = n$ (all cooperated), play **C**.
     * If $k < n$ (any defected), play **D** for the current round to punish defection and compensate for the previous loss.

3. **Terminal Round Handling:**
   If the current round $t = r$:
   * Play **D** regardless of past history or current stock level. Since there is no future, any incentive to maintain the common pool disappears, and individual payoff is maximized by extracting the maximum possible share immediately.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, stock, prev_round_cooperators, n):
    # Terminal round: maximize extraction
    if round_number == total_rounds:
        return 'D'
        
    # Crisis mode: pool is too small to sustain, extract before exhaustion
    if stock < (capacity / (2 * n)):
        return 'D'
        
    # First round: initiate cooperation
    if round_number == 1:
        return 'C'
        
    # Adaptive enforcement: punish if anyone defected in the previous round
    if prev_round_cooperators < n:
        return 'D'
    else:
        return 'C'
```
'''

description_SELFINTERESTED_6 = '''
The strategy follows a "Conditional Reciprocity with Stock Awareness" model, aimed at sustaining the common pool to maximize long-term yield while punishing defectors when possible.

### Decision Rules

Define $k_t$ as the number of opponents who cooperated in round $t$.
Define $S_t$ as the current stock at the start of round $t$.

**Round 1:** Play Cooperate (C).

**Subsequent Rounds ($t > 1$):**
1. **Calculate Survival Threshold:** If $S_t < \frac{capacity}{2n}$, play Defect (D) to extract maximum value before potential exhaustion.
2. **Evaluate Cooperation:**
   - If the previous round's outcome ($k_{t-1}$) indicates that cooperation is widespread (e.g., $k_{t-1} \geq \frac{n-1}{2}$), play Cooperate (C) to maintain stock levels.
   - If the previous round's outcome indicates prevalent defection ($k_{t-1} < \frac{n-1}{2}$), play Defect (D) to minimize individual losses while the pool is being depleted by others.

### Final Round Behavior

In the final round ($t = r$):
- Ignore previous cooperation reciprocity logic.
- Always play Defect (D) regardless of stock level, as there is no future stock to preserve for subsequent turns.

### Adaptive Mechanism (The "Stock Guard")

To prevent total collapse due to others' defection:
- If $S_t$ drops below $10\%$ of $capacity$ and $t < r$, switch to Defect (D) immediately for all subsequent rounds, regardless of previous cooperation levels, to salvage remaining value.

### Pseudocode Summary

```python
def get_action(round_number, total_rounds, current_stock, capacity, n, prev_round_cooperators):
    # Terminal condition: last round
    if round_number == total_rounds:
        return 'D'
    
    # Emergency condition: stock nearly empty
    if current_stock < (0.10 * capacity):
        return 'D'
    
    # Survival condition: pool too low to sustain mutual cooperation
    if current_stock < (capacity / (2 * n)):
        return 'D'
        
    # Reciprocity condition: check if majority cooperated last round
    # (n-1 because opponents exclude self)
    if prev_round_cooperators >= ((n - 1) / 2):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_7 = '''
1. **Initial State (Round 1):**
Always play Cooperate (C) in the first round to test the cooperation level of the opponent pool and ensure stock remains high for future rounds.

2. **Recursive Strategy (Rounds $t > 1$):**
Maintain an estimate of the average opponent cooperation rate ($\alpha$) based on the history of observed aggregate cooperation. Let $k$ be the number of opponents observed to play Cooperate in the previous round, and $n-1$ be the total number of opponents.
$\alpha = \frac{\sum_{j=1}^{t-1} k_j}{\sum_{j=1}^{t-1} (n-1)}$

Decision rule at round $t$:
*   If $t = r$ (Final Round): Play Defect (D).
*   If $S_{t} < (\text{capacity} / n)$: Play Defect (D) regardless of history, as the stock is too low for recovery to be profitable.
*   If $\alpha \geq 0.5$: Play Cooperate (C).
*   If $\alpha < 0.5$: Play Defect (D).

3. **Adjustment for Stock Stability:**
If the stock $S_t$ drops below a critical threshold $\tau = \text{capacity} / 2$, override the cooperation logic:
*   Regardless of $\alpha$, if $S_t < \tau$, play Cooperate (C) to allow stock regeneration, provided that the number of previous defectors was not overwhelmingly high (i.e., if observed average defection rate $> 0.75$, switch to Defect (D) permanently as the pool is predatory and recovery is futile).

4. **Pseudocode Logic:**
```python
def decide_action(t, r, n, capacity, current_stock, history):
    # Base Case: Last round
    if t == r:
        return D

    # Critical Depletion: If stock is too low to sustain growth
    if current_stock < (capacity / n):
        return D

    # Calculate aggregate opponent cooperation rate
    total_coop_obs = sum(h.cooperators_observed for h in history)
    total_opp_rounds = (n - 1) * (t - 1)
    alpha = total_coop_obs / total_opp_rounds

    # Aggressive Depletion: If pool is overwhelmingly predatory
    if alpha < 0.25 and current_stock < (capacity / 2):
        return D

    # Cooperative Recovery: If stock is low, prioritize sustainability
    if current_stock < (capacity / 2):
        return C

    # Standard Tit-for-Tat logic based on aggregate behavior
    return C if alpha >= 0.5 else D
```
'''

description_SELFINTERESTED_8 = '''
**Strategy: Dynamic Sustainable Tit-for-Tat (DSTFT)**

The strategy adheres to a conditional cooperation logic based on the observed aggregate behavior of opponents in the previous round, modulated by the current state of the stock.

**1. Variable Definitions**
*   `N_c`: Number of opponents who played C in the previous round.
*   `N`: Total number of players.
*   `S`: Current stock level.
*   `C_opp`: Cooperation threshold. Set `C_opp = n - 1` (i.e., require full cooperation from all others to sustain equilibrium).

**2. Decision Rules**
In any given round `t`, determine action `A_t` as follows:

*   **Initial Round (t=1):** Play **Cooperate (C)**.
*   **Subsequent Rounds (t > 1):**
    *   **Observation:** If the previous round's aggregate cooperation count among opponents was `N_c`:
    *   **Defection Trigger:** If `N_c < C_opp` (i.e., at least one opponent defected in the previous round) OR if the current stock `S` falls below the threshold `(capacity / 2)`:
        *   Play **Defect (D)** for the current round.
    *   **Cooperation Maintenance:** If `N_c == C_opp` (all opponents cooperated previously) AND `S >= (capacity / 2)`:
        *   Play **Cooperate (C)** for the current round.

**3. Terminal Round Adjustment (t = r)**
Regardless of history, in the final round `t = r`:
*   Play **Defect (D)**.

**4. Pseudocode**
```python
def get_action(round_number, total_rounds, n, capacity, current_stock, prev_opp_c):
    # Rule for final round
    if round_number == total_rounds:
        return 'D'
    
    # Rule for first round
    if round_number == 1:
        return 'C'
    
    # Adaptive rule for intermediate rounds
    # Check if stock is healthy and all others cooperated
    if current_stock >= (capacity / 2) and prev_opp_c == (n - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_9 = '''
The strategy follows a conditional, history-dependent approach designed to maximize long-term resource extraction while punishing defectors. Let $S_t$ be the stock at the start of round $t$, $N_C$ be the number of players who played $C$ in the previous round, and $D_{count}$ be the number of consecutive rounds of observed defection.

**1. Initialization**
- Round 1: Play $C$.

**2. Decision Logic (Round $t > 1$)**
- If the current stock $S_t < \epsilon$ (where $\epsilon$ is a threshold of $0.05 \times \text{capacity}$), play $D$ for the remainder of the game.
- Otherwise, assess the cooperation history of the group:
    - Let $k$ be the number of defectors in round $t-1$, calculated as $n - N_C$.
    - If $k = 0$ (all players cooperated), play $C$.
    - If $k > 0$, play $D$ for the next $k$ rounds.

**3. Terminal Rounds**
- In the final 2 rounds, if $S_t > 0.5 \times \text{capacity}$, play $D$ regardless of prior history.
- If $S_t \le 0.5 \times \text{capacity}$, follow the decision logic in Section 2.

**4. Pseudocode Implementation**
```python
def get_action(round_number, stock, last_round_cooperators, n, total_rounds):
    # Terminal phase check
    if round_number > total_rounds - 2:
        if stock > 0.5 * capacity:
            return "D"
            
    # Resource collapse protection
    if stock < 0.05 * capacity:
        return "D"
        
    # Standard play
    if round_number == 1:
        return "C"
    
    # Calculate punishment
    defectors_last_round = n - last_round_cooperators
    
    # Check if currently in a punishment phase
    # (Simplified tracker: assumes internal state tracks active punishment duration)
    if active_punishment_rounds > 0:
        active_punishment_rounds -= 1
        return "D"
    
    # Trigger new punishment
    if defectors_last_round > 0:
        active_punishment_rounds = defectors_last_round - 1
        return "D"
        
    return "C"
```
'''

description_SELFINTERESTED_10 = '''
### Strategy: Adaptive Tit-for-Tat with Depletion Thresholding

**Initialization (Round 1):**
Play Cooperate ($C$). The initial state is optimal ($S=capacity$), and establishing a cooperative precedent maximizes the likelihood of sustained high stock levels, which are necessary for long-term payoff accumulation.

**Subsequent Rounds (Round $t > 1$):**
Decide action based on the state $S_t$ and the history of opponent behavior $H_{t-1}$.

1.  **Safety Threshold Check:**
    If $S_t < \text{capacity} / 2$, play Defect ($D$). At low stock levels, the stock dynamics (logistic growth) are vulnerable to collapse. If the pool is significantly depleted, the "tragedy of the commons" incentive dominates because future returns on investment (stock growth) are unreliable.

2.  **Reputation/Reciprocity Logic:**
    If $S_t \ge \text{capacity} / 2$, determine action based on the average cooperation rate of opponents in the previous round ($k_{t-1} / (n-1)$):
    *   **Full Cooperation:** If all opponents cooperated in the previous round, play Cooperate ($C$).
    *   **Partial/Full Defection:** If any opponents defected in the previous round, play Defect ($D$).

3.  **Final Round ($t = r$):**
    Regardless of history, play Defect ($D$). In the final round, there is no future shadow of the future; therefore, the marginal utility of preserving the stock for the next round is zero. Maximize immediate consumption.

**Decision Pseudocode:**

```python
def choose_action(round, total_rounds, n, capacity, current_stock, history):
    # Rule 3: End-game trigger
    if round == total_rounds:
        return D

    # Rule 1: Stock preservation threshold
    if current_stock < (capacity / 2):
        return D

    # Rule 2: Tit-for-Tat
    if round == 1:
        return C
    
    previous_opponents_defecting = history.last_round_defecting_count
    
    if previous_opponents_defecting == 0:
        return C
    else:
        return D
```

**Edge Case Handling:**
*   **Opponent Defection:** If opponents defect, the strategy immediately shifts to $D$ for the following round to minimize the relative payoff loss (preventing the "sucker's payoff").
*   **Stock Recovery:** If the strategy detects that the pool is recovering toward the capacity (via the state input), it remains open to returning to $C$ in the next round, provided that the opponents show consistent cooperation in the preceding round.
*   **Low $n$:** In smaller games ($n=2$), the logic holds as the tit-for-tat dynamic is clearer; in larger games, the strict "all-or-nothing" threshold for reciprocation ensures that the strategy does not subsidize a group of defectors.
'''

description_SELFINTERESTED_11 = '''
Adopt a conditional "Tit-for-Tat" variant based on the observed aggregate cooperation rate, utilizing a "sustainable harvest" threshold.

**Definitions:**
*   $k$: Number of opponents who cooperated in the previous round ($0 \le k \le n-1$).
*   $C_{prev}$: Boolean, true if I cooperated in the previous round.
*   $S_t$: Current stock level at the start of round $t$.
*   $T$: Total rounds $r$.

**Strategy Logic:**

1.  **First Round ($t=1$):**
    Always play **Cooperate (C)**. This tests for cooperation without immediately depleting the resource.

2.  **Last Round ($t=r$):**
    Always play **Defect (D)**. Since there are no future rounds to protect, maximize immediate payoff regardless of stock levels or past behavior.

3.  **Intermediate Rounds ($1 < t < r$):**
    Calculate the "sustainable exploitation" threshold. If $S_t < \frac{capacity}{2}$, the stock is fragile; prioritize recovery. If $S_t \ge \frac{capacity}{2}$, the stock is robust; tolerate moderate exploitation.

    Apply the following decision matrix:
    *   **If $S_t \approx 0$ (Stock is exhausted):** Play **Defect (D)**. Cooperation yields negligible returns when the pool is empty; capture the remaining scraps.
    *   **If $S_t \ge \frac{capacity}{2}$:** Play **Cooperate (C)** if $k \ge \lfloor \frac{n-1}{2} \rfloor$. If fewer than half the opponents cooperated, play **Defect (D)** to penalize non-cooperative behavior and prevent excessive free-riding.
    *   **If $S_t < \frac{capacity}{2}$:** Play **Cooperate (C)** if $k = n-1$ (everyone else cooperated). If even one opponent defects, play **Defect (D)**. In a fragile state, any defection by an opponent necessitates switching to defection to avoid being the sole victim of resource depletion.

**Pseudocode:**

```python
def decide_action(t, r, n, S_t, k_prev, my_last_action):
    if t == r:
        return 'D'
    
    if t == 1:
        return 'C'
    
    # Calculate recovery threshold
    is_fragile = (S_t < (capacity / 2))
    
    if is_fragile:
        # Require total consensus to cooperate
        if k_prev == (n - 1):
            return 'C'
        else:
            return 'D'
    else:
        # Require majority consensus to cooperate
        if k_prev >= (n - 1) / 2:
            return 'C'
        else:
            return 'D'
```

**Edge Case Handling:**
*   **System Shock:** If the stock drops suddenly due to mass defection by opponents, the "is_fragile" logic triggers immediately in the subsequent round, forcing a shift to Defect until the stock recovers or the game ends.
*   **Anonymity:** Since identity is unknown, the strategy relies purely on the aggregate $k$. If the population of opponents is volatile, the threshold-based approach prevents "sucker" payoffs by strictly conditioning cooperation on observable aggregate cooperation counts.
'''

description_SELFINTERESTED_12 = '''
The strategy follows a conditional, history-dependent approach designed to maximize long-term yield by maintaining the stock near the "Optimal Sustainability Threshold" (OST).

### State Variables
Let $k_t$ be the number of cooperators observed in round $t-1$.
Let $S_t$ be the current stock at the start of round $t$.
Let $r$ be the total rounds and $t$ be the current round.

### Decision Rule
1. **Initial Round ($t=1$):**
   - Play **Cooperate (C)**. This signals a willingness to maintain the resource, which is necessary for future-round yields.

2. **Terminal Round ($t=r$):**
   - Play **Defect (D)**. Since no future rounds exist to reap the benefits of a replenished stock, extract the maximum possible amount.

3. **Intermediate Rounds ($1 < t < r$):**
   - Calculate the **Stock Viability Indicator ($V_t$)**:
     - If $S_t > \text{capacity} \times 0.5$, the stock is robust.
     - If $S_t \le \text{capacity} \times 0.25$, the stock is critically low.
   - Apply **Trigger Logic**:
     - **If $S_t \le \text{capacity} \times 0.25$:** Play **Defect (D)**. If the stock is below 25% of capacity, growth rates become insufficient to reliably recover against defector consumption; extract while the resource remains.
     - **Else (Stock is sufficient):**
       - If $k_{t-1} \ge \lfloor n/2 \rfloor$: Play **Cooperate (C)**. Reward the cooperative behavior observed in the previous round to sustain the pool.
       - If $k_{t-1} < \lfloor n/2 \rfloor$: Play **Defect (D)**. Punish the lack of cooperation to prevent free-riding when the group is trending toward exhaustion.

### Edge Case Handling
- **If $S_t \approx 0$**: Play **Defect (D)** regardless of round number, as the resource is effectively exhausted and payoff potential is near zero.
- **If $n=2$**: The strategy simplifies to a Tit-for-Tat variant. Play C if the opponent played C in the previous round; otherwise, play D. In the final round, always play D.
'''

description_SELFINTERESTED_13 = '''
**Strategy: Tit-for-Tat with Sustainability Threshold (TFTS)**

This strategy operates on the principle of conditionally cooperating to maintain the common pool at its maximum sustainable capacity, while defecting when the pool is being depleted by others or when the remaining rounds make future cooperation irrelevant.

**Decision Logic**

For each round $t$ (where $t = 1 \dots r$):

1.  **Terminal Round Rule**: If $t = r$, play **Defect (D)**. Since there are no future rounds to protect, the immediate maximization of individual payoff is the only logical move.

2.  **Sustainability Check**: If the current stock $S_t$ is below a critical threshold $S_{crit} = \text{capacity} / 2$, play **Defect (D)**. When the stock is low, the growth function yields diminishing returns; it is optimal to extract remaining value before others deplete the resource entirely.

3.  **Cooperation Maintenance (Adaptive Tit-for-Tat)**:
    If $t < r$ and $S_t \ge S_{crit}$:
    *   Observe the total number of cooperators from round $t-1$. Let $k_{t-1}$ be the number of players who chose $C$ in the previous round.
    *   If $k_{t-1} \ge n - 1$ (meaning everyone or all but one cooperated), play **Cooperate (C)**. This reinforces cooperative behavior.
    *   If $k_{t-1} < n - 1$ (meaning significant defection occurred), play **Defect (D)**. This penalizes the group for depleting the resource.

**Initialization**

*   In Round 1 ($t=1$), play **Cooperate (C)**. This signals a preference for long-term sustainability to other players, provided the initial stock is at capacity.

**Pseudocode**

```python
def get_action(round_number, total_rounds, current_stock, capacity, last_round_cooperators, n):
    # Rule 1: Last round maximization
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: Low stock emergency extraction
    if current_stock < (capacity / 2):
        return 'D'
    
    # Rule 3: Adaptive Tit-for-Tat
    if round_number == 1:
        return 'C'
    
    # Threshold for penalty: if more than 1 person defected, punish
    if last_round_cooperators >= (n - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_14 = '''
**Strategy: Trigger-Based Sustainable Yield (TBSY)**

The strategy relies on a Conditional Tit-for-Tat approach adjusted for the logistic growth function of the resource. The objective is to maintain the stock $S$ near the capacity level $K = \text{capacity}$ by enforcing collective cooperation while punishing defection.

**1. Definitions and Parameters**
*   **Cooperation Threshold ($T$):** Define the cooperation threshold as $n-1$. This means the strategy only considers "full cooperation" to be the state where all $n-1$ other players choose $C$.
*   **State Observation:** In each round $t$, observe $k_{t-1}$, the number of opponents who played $C$ in the previous round.

**2. Decision Rules**
Let $a_t$ be the action in round $t$.

*   **Round 1:** Play $C$ (Cooperate). This initiates a cooperative equilibrium.
*   **Rounds $t > 1$:**
    *   **If $S_t \approx 0$:** Play $D$ (Defect). If the stock is exhausted, the resource cannot regenerate; capture the residual value immediately.
    *   **If $k_{t-1} = n-1$:** Play $C$ (Cooperate). If all opponents cooperated in the previous round, maintain the cooperative equilibrium to preserve long-term growth.
    *   **If $k_{t-1} < n-1$:** Play $D$ (Defect) for the current round. If any opponent defects, the cooperative equilibrium has broken down. Defecting in response maximizes immediate payoff before the stock is depleted by others.
    *   **Recovery Condition:** If $k_{t-1} < n-1$ but $S_t$ has recovered to $> 0.8 \times \text{capacity}$, reset to $C$ (Cooperate) for the next round, regardless of the previous round's outcome, to attempt to re-establish the cooperative equilibrium.

**3. Edge Cases**
*   **Last Round ($t = r$):** Always play $D$ (Defect). Since there is no future utility to protect the resource, the dominant strategy is to extract the maximum possible amount from the remaining stock.
*   **Low Stock ($S_t < \text{consumption}_C$):** If the current stock is too low to sustain $C$ consumption without risking total depletion, play $D$ to secure the remaining fragments of the resource.
*   **Non-zero observation (Ambiguity):** If $k_{t-1}$ is ambiguous due to noise or sudden state changes, default to $D$ if $S_t$ is trending downward significantly (e.g., $S_t < S_{t-1}$ despite growth calculations), otherwise default to $C$.

**4. Pseudocode**

```python
def decide_action(round, total_rounds, current_stock, capacity, opponents_cooperated_prev_round, n):
    # Rule 1: Last round defection
    if round == total_rounds:
        return 'D'
    
    # Rule 2: Exhausted stock
    if current_stock == 0:
        return 'D'
        
    # Rule 3: Recovery attempt
    if current_stock > (0.8 * capacity):
        return 'C'
        
    # Rule 4: Tit-for-Tat Enforcement
    # If all opponents cooperated last round
    if opponents_cooperated_prev_round == (n - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_15 = '''
The strategy follows a conditional "Tit-for-Tat with Forgiveness and Stock Preservation" logic, aiming to sustain the common pool while maximizing share.

### Strategy Definition: "Threshold-Based Stewardship"

**Decision Rules:**
1. **Initial Phase:** In Round 1, play **C**.
2. **Growth Maintenance Rule:** Calculate the "Sustainability Threshold." If the current stock $S$ is below $0.5 \times \text{capacity}$, play **C** regardless of opponent history to allow stock recovery.
3. **Response to Opponents:** If $S \ge 0.5 \times \text{capacity}$, determine action based on the previous round's outcome:
    *   If the number of defectors in the previous round was 0, play **C**.
    *   If the number of defectors in the previous round was $> 0$, play **D**.
4. **Final Phase:** In the final 2 rounds ($r-1, r$), switch to **D** regardless of stock level or previous history.

**Logic Breakdown:**
*   **Cooperation Phase:** By defaulting to **C** when stock is below $0.5 \times \text{capacity}$, the agent enforces a "regrowth" period, ensuring the pool is not exhausted. This is a non-negotiable floor for self-interest, as zero stock results in zero future payoffs.
*   **Tit-for-Tat Trigger:** When the stock is healthy ($S \ge 0.5 \times \text{capacity}$), the agent punishes defection by defecting in the subsequent round. This serves as a deterrent to opponents.
*   **Forgiveness Mechanism:** The strategy resets to **C** automatically once the stock recovers back to the $S < 0.5 \times \text{capacity}$ threshold, effectively forgiving past defections if the stock was depleted, but keeping the pressure high while the stock is healthy.
*   **Defection Phase:** The terminal rounds ($r-1, r$) prioritize immediate extraction over sustainability, as the stock's future regeneration value is rendered moot.

**Pseudocode:**

```python
def get_action(current_round, stock, prev_opponents_defected, n, r, capacity):
    # Terminal phase: extract everything
    if current_round >= r - 1:
        return 'D'
    
    # Conservation phase: protect the resource
    if stock < (capacity * 0.5):
        return 'C'
    
    # Tit-for-Tat logic when resource is healthy
    if prev_opponents_defected > 0:
        return 'D'
    else:
        return 'C'
```
'''

description_SELFINTERESTED_16 = '''
The strategy follows a Tit-for-Tat variant adapted for continuous resource constraints, using an "Optimistic Trigger" approach.

**Strategy Logic**

1.  **Phase 1: Initial Rounds (Round 1 to 2)**
    *   Always play **C**. This establishes cooperative intent and gathers baseline data on the population's willingness to sustain the resource.

2.  **Phase 2: Monitoring and Retaliation (Round 3 onwards)**
    *   **State Assessment:** Evaluate the stock level $S_t$ at the beginning of the round.
        *   If $S_t < \text{threshold}$ (where threshold is $0.25 \times \text{capacity}$), defect immediately to extract remaining value before depletion, regardless of past cooperation.
        *   If $S_t \geq \text{threshold}$, calculate the "Defection Tolerance" based on the previous round's outcome.

    *   **Defection Tolerance (The Trigger Rule):**
        *   Let $N_c$ be the number of players who cooperated in the previous round.
        *   Define the "Sustainable Cooperation Requirement" $N_{req}$ as $\lceil n/2 \rceil$.
        *   If $N_c \geq N_{req}$: Play **C**.
        *   If $N_c < N_{req}$: Play **D**.

3.  **Phase 3: Endgame (Final 2 rounds)**
    *   In the second-to-last round ($r-1$), if the stock $S_{r-1}$ is below $0.5 \times \text{capacity}$, switch to **D** to capture remaining value. Otherwise, follow the standard Phase 2 logic.
    *   In the final round ($r$), always play **D**. There is no future value to preserve, and the stock dynamics do not affect any subsequent payoffs.

**Pseudocode**

```python
def decide_action(round, n, S_t, N_c, r):
    # Endgame Logic
    if round == r:
        return 'D'
    
    if round == r - 1 and S_t < (0.5 * capacity):
        return 'D'

    # Survival Logic
    if S_t < (0.25 * capacity):
        return 'D'

    # Cooperation Logic
    # Start cooperating early to build stock
    if round <= 2:
        return 'C'
    
    # Tit-for-Tat / Trigger Mechanism
    # Require majority cooperation to continue sustaining the pool
    N_req = ceil(n / 2)
    
    if N_c >= N_req:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling**
*   **Rapid Depletion:** If the stock drops below the $0.25 \times \text{capacity}$ critical floor, the strategy abandons cooperation immediately. This prevents the agent from being the "last one out" while the resource is liquidated by defectors.
*   **Zero-Sum Dynamics:** By incorporating $N_{req}$ (majority cooperation), the strategy avoids being exploited by a minority of defectors while allowing for recovery if the majority remains cooperative.
*   **Final Round Defection:** Recognizing the game's termination point removes the incentive to maintain future stock, maximizing the final payoff.
'''

description_SELFINTERESTED_17 = '''
The strategy employs a conditional "Tit-for-Tat with Threshold Monitoring" approach designed to maintain the resource stock near the capacity level while punishing defectors.

**1. Variable Definitions**
*   `threshold_stock`: A dynamic safety buffer, calculated as `0.7 * capacity`.
*   `observed_cooperation_rate`: The ratio of cooperators in the previous round, calculated as `(count_cooperators - is_self_cooperating) / (n - 1)`.

**2. Decision Rules**
In each round `t`, the decision to Cooperate (C) or Defect (D) is determined by the following logic:

*   **Round 1:** Play **C**. This establishes cooperative intent and preserves stock for growth.
*   **Final Round (t = r):** Play **D**. Since there are no future rounds to influence, maximize current consumption regardless of the state.
*   **Intermediate Rounds (1 < t < r):**
    1.  **Safety Check:** If `stock` < `(capacity / n)`, play **D**. The resource is too depleted to sustain cooperation; attempt to extract remaining value before collapse.
    2.  **Reciprocity Check:** If `observed_cooperation_rate` < 0.5, play **D**. This punishes the group for previous defection.
    3.  **Sustainability Check:** If `stock` > `threshold_stock` and the previous round's `observed_cooperation_rate` ≥ 0.5, play **C**. This maintains the resource at high levels.
    4.  **Default:** Play **C**. If the resource is healthy and the group is generally cooperative, prioritize long-term stock sustainability.

**3. Pseudocode Implementation**

```python
def choose_action(round, total_rounds, n, capacity, current_stock, history):
    # Rule 1: First round
    if round == 1:
        return 'C'
    
    # Rule 2: Last round
    if round == total_rounds:
        return 'D'
    
    # Analyze previous round data
    prev_round = history[-1]
    prev_stock = prev_round['stock_start']
    prev_cooperators = prev_round['num_cooperators']
    my_prev_action = prev_round['my_action']
    
    # Calculate external cooperation rate
    # If I cooperated, subtract 1 from count, n-1 opponents total
    # If I defected, don't subtract, n-1 opponents total
    if my_prev_action == 'C':
        opp_cooperators = prev_cooperators - 1
    else:
        opp_cooperators = prev_cooperators
    
    opp_cooperation_rate = opp_cooperators / (n - 1)
    
    # Rule 3: Safety Check
    if current_stock < (capacity / n):
        return 'D'
        
    # Rule 4: Reciprocity Check (Punishment)
    if opp_cooperation_rate < 0.5:
        return 'D'
        
    # Rule 5: Sustainability/Default
    if current_stock > (0.7 * capacity):
        return 'C'
    else:
        return 'C'
```
'''

description_SELFINTERESTED_18 = '''
### Strategy: Conditional Sustainability Equilibrium (CSE)

This strategy employs a threshold-based, trigger-tit-for-tat logic designed to enforce sustainable extraction levels while punishing defection only as necessary to protect the stock.

#### Decision Logic

Define $k_t$ as the number of opponents who played $C$ in the previous round $t-1$. Calculate the number of opponents who played $D$ in the previous round as $d_{t-1} = (n-1) - k_{t-1}$.

1.  **Initial Round ($t=1$):** Always play $C$. This establishes a baseline for cooperation and preserves the resource for the subsequent growth phase.

2.  **Intermediate Rounds ($1 < t < r$):**
    *   **If the previous round's stock $S_{t-1}$ was high enough to sustain growth:**
        *   If the majority of opponents played $C$ (specifically, if $k_{t-1} \geq \lceil (n-1)/2 \rceil$): Play $C$. Reward mutual cooperation.
        *   If the majority of opponents played $D$: Play $D$ with probability $P(D) = \min(1, \frac{d_{t-1}}{n-1})$. This tit-for-tat variation scales the punishment to the level of observed defection.
    *   **Emergency Threshold:** If the stock $S_{t-1} < \text{capacity} / 4$, prioritize stock recovery regardless of opponent history. Play $C$ every round until $S_t > \text{capacity}/2$.

3.  **Final Round ($t=r$):**
    *   If $S_r \geq \text{capacity}/2$: Play $D$. Given no future rounds exist to suffer the consequences of depletion, extraction is maximized.
    *   If $S_r < \text{capacity}/2$: Play $C$. Aggressive extraction when the stock is already low risks zero payoff; playing $C$ provides a non-zero, guaranteed return.

#### Pseudocode

```python
def get_action(round_num, stock, n, history, r):
    # Base Case: Last round defection if sustainable
    if round_num == r:
        if stock >= capacity / 2:
            return D
        else:
            return C

    # Base Case: First round cooperation
    if round_num == 1:
        return C

    # Emergency conservation
    if stock < capacity / 4:
        return C

    # Tit-for-tat logic based on previous round's observation
    # k = number of opponents who cooperated
    k = history[round_num-1].cooperators
    
    # Threshold for reciprocal cooperation
    if k >= (n - 1) / 2:
        return C
    else:
        # Probabilistic punishment scaled to level of defection
        d_opponents = (n - 1) - k
        if random() < (d_opponents / (n - 1)):
            return D
        else:
            return C
```

#### Edge Cases and Adaptations

*   **Stock Collapse Prevention:** The strategy ignores opponent defection if the stock drops below $25\%$ of capacity. In this state, cooperation is mandatory to prevent the extinction of the pool, which would result in zero future payoffs.
*   **Asymmetric Punishment:** The probability-based punishment ($d_{t-1} / (n-1)$) allows the agent to blend into groups of varying cooperation levels. If one opponent defects, the agent rarely retaliates fully; if the group defects en masse, the agent defects immediately, preventing free-rider exploitation.
*   **Terminal Defection:** The strategy acknowledges the "end-game problem" by defecting on the final round, provided the stock can support the higher extraction rate, ensuring the agent captures residual value that would otherwise be left in the pool.
'''

description_SELFINTERESTED_19 = '''
This strategy, "Adaptive Sustainability Guard," operates on a modified Tit-for-Tat foundation that prioritizes long-term resource maintenance while defending against exploitation.

### Core Logic
The strategy maintains a target "safe stock" level of `capacity * 0.75` to allow for buffer room against unexpected depletion. If the stock falls below this threshold or if the recent cooperation rate of opponents drops, the strategy switches to defensive defection to extract value before the resource collapses.

### Decision Rules

**1. Initialization:**
Play **C** in the first round to establish a baseline of cooperation.

**2. Rounds $t = 2$ to $r-1$:**
Assess the average cooperation level of opponents from the previous round, $O_c$.
*   **IF** current `stock` $\ge$ `capacity * 0.75`:
    *   **IF** $O_c = n-1$ (perfect group cooperation): Play **C**.
    *   **IF** $O_c < n-1$: Play **D** with probability $P = 1 - (O_c / (n-1))$ to punish free-riders while signaling willingness to cooperate.
*   **IF** current `stock` < `capacity * 0.75`:
    *   **IF** $O_c = n-1$: Play **C** (attempting to rebuild stock).
    *   **IF** $O_c < n-1$: Play **D** (the common pool is threatened; prioritize immediate extraction).

**3. The Final Round ($t = r$):**
Always play **D** regardless of state or history. Since no future rounds exist, the stock regeneration dynamics are irrelevant, and defection provides the maximum possible payoff.

### Pseudocode Implementation

```python
def get_action(round_number, total_rounds, stock, capacity, n, last_opponents_c):
    # Rule 1: Final Round
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: First Round
    if round_number == 1:
        return 'C'
    
    # Rule 3: Maintenance Phase
    # Calculate opponent cooperation rate
    cooperation_rate = last_opponents_c / (n - 1)
    
    if stock >= (capacity * 0.75):
        if cooperation_rate == 1.0:
            return 'C'
        else:
            # Probability-based punishment: 
            # higher defection rate by others = higher probability of D
            return 'D' if random.random() > cooperation_rate else 'C'
    
    # Rule 4: Critical Resource Phase
    else:
        if cooperation_rate >= 0.8: # Threshold for restoration
            return 'C'
        else:
            return 'D'
```

### Edge Case Handling
*   **Stock Collapse ($S \to 0$):** If the stock is so low that even $C$ yields negligible returns, the strategy defaults to $D$ for the remainder of the game to ensure any final marginal utility is captured.
*   **Empty History:** In the event of observing no history (if `last_opponents_c` is null, i.e., round 1), default to $C$.
*   **Inconsistent Behavior:** If opponents oscillate between $C$ and $D$, the strategy prioritizes $D$ whenever the stock falls below the `capacity * 0.75` threshold to prevent being the "sucker" in a dwindling pool.
'''

description_SELFINTERESTED_20 = '''
**Strategy: Sustainable Tit-for-Tat with Resource Thresholding**

The objective is to maximize long-term payoff by enforcing a sustainable equilibrium while preventing exploitation by defectors. The strategy operates on a conditional "cooperate-if-others-cooperate" logic, constrained by a safety threshold regarding the stock level.

**Decision Rules:**

For each round $t \in \{1, \dots, r\}$, with current stock $S_t$:

1.  **Safety Threshold Check:**
    If $S_t < \text{capacity} / 2n$, play **D** (Defect).
    *Rationale:* If the stock is critically low, future growth is unlikely to recover the pool to a meaningful level. Extract maximum remaining value before depletion.

2.  **Reputation Tracking:**
    Maintain an estimate of opponent cooperation. Let $C_{opp}$ be the number of opponents who cooperated in the previous round $t-1$.
    *   If $t = 1$: Play **C** (Cooperate).
    *   If $t > 1$:
        *   If $C_{opp} \ge n - 1$: Play **C**. (Reward collective sustainability).
        *   If $C_{opp} < n - 1$: Play **D**. (Punish defection to discourage free-riding).

3.  **Endgame Override:**
    If $t = r$: Play **D**.
    *Rationale:* In the final round, there is no future value to preserve. Extract maximum immediate payoff regardless of prior cooperation history.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, n, stock, capacity, opponents_cooperated_last_round):
    # Rule 1: Endgame
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: Critical Stock Depletion
    # Threshold is defined by n to prevent premature collapse
    if stock < (capacity / (2 * n)):
        return 'D'
    
    # Rule 3: Tit-for-Tat / Reciprocity
    if round_number == 1:
        return 'C'
    
    # If almost everyone cooperated, continue cooperating
    if opponents_cooperated_last_round >= (n - 1):
        return 'C'
    
    # Otherwise, punish defection
    return 'D'
```

**Edge Case Handling:**

*   **Initial Round:** Always default to **C**. This signals willingness to cooperate and allows the stock to grow if others are also reciprocal.
*   **Total Depletion (Stock = 0):** The payoff for both C and D becomes zero. The strategy defaults to **D** (via Rule 1, as the state effectively ends), though payoffs are nullified regardless of choice.
*   **Aggressive Opponents:** If the environment is dominated by defectors, the strategy will defect from round 2 onwards. This limits losses against non-cooperative players while preserving potential utility if the pool does not immediately hit zero.
'''

description_SELFINTERESTED_21 = '''
For round `t = 1` to `r`:

1. **Calculate the Sustainable Threshold:** Define a target stock level `S_target = capacity / 2`. This level maximizes the logistic growth function (growth is highest when the stock is at half capacity), ensuring the pool replenishes optimally for future rounds.

2. **Evaluate the Current State:** Let `S_t` be the current stock.
   - If `t = r` (the final round): Play **Defect (D)**. Since no future rounds exist, the stock's future value is zero; immediate payoff maximization is the only rational objective.
   - If `S_t` is below the threshold required to sustain growth (specifically, if `S_t < (capacity * (0.5 / n))`), play **Defect (D)**. When the stock is collapsing regardless of cooperation, extract remaining value immediately.

3. **Determine Adaptive Behavior (Tit-for-Tat with Forgiveness):** For all rounds `t < r` where `S_t` is sufficient to sustain growth:
   - Identify `k`, the number of opponents who cooperated in round `t-1`.
   - In round `1`, cooperate (**C**).
   - In subsequent rounds, cooperate (**C**) if the average cooperation rate of opponents in the previous round `(k / (n-1))` is greater than or equal to a threshold `T = 0.5`.
   - If the average cooperation rate falls below `T`, switch to defect (**D**) for one round to signal intolerance for over-extraction.
   - Return to cooperation (**C**) in the immediately following round regardless of opponent action to attempt re-coordination (forgiveness).

4. **Exception Rule:** If at any point the stock `S_t` drops below the amount consumed by a single defector (i.e., `S_t / n < epsilon`), play **Defect (D)** to capture the remaining resources before they are exhausted by other agents.
'''

description_SELFINTERESTED_22 = '''
Strategy: Tit-for-Tat with Conditional Forgiveness and Terminal Defection

The strategy maintains a cooperative state if the aggregate behavior of opponents aligns with sustainable resource usage and shifts to exploitation when the state or opponent history dictates.

**Variables:**
- `last_stock`: Stock level from the previous round (initialized to `capacity`).
- `cooperation_threshold`: A dynamic parameter set at 0.5 (i.e., at least half of the other players must cooperate for the round to be considered "sustainable").
- `reputation`: A score initialized at 0. Positive values indicate past cooperative behavior, negative values indicate defecting behavior.

**Decision Rules:**

1. **Terminal Round (Round = r):**
   - Play **D**. Since there are no future consequences, maximizing immediate extraction is the dominant strategy.

2. **First Round (Round = 1):**
   - Play **C**. Establish a cooperative baseline.

3. **Intermediate Rounds (1 < Round < r):**
   - **Evaluate Sustainability:** If `last_stock` < (`capacity` / 4), switch to **D**. At low stock levels, the resource cannot regenerate effectively; extract remaining value before depletion.
   - **Evaluate Opponent Behavior:** Let `k` be the number of cooperators observed in the previous round.
     - If `k` ≥ `(n - 1) * cooperation_threshold`:
       - If `reputation` < 0, increment `reputation` by 1.
       - Play **C**.
     - If `k` < `(n - 1) * cooperation_threshold`:
       - If `reputation` > -2, decrement `reputation` by 1.
       - Play **D**.
   - **Forgiveness Mechanism:** If the strategy is currently playing **D** but the opponents play **C** for two consecutive rounds, reset `reputation` to 0 and switch to **C**.

**Pseudocode:**

```python
def get_action(round, r, n, stock, last_stock, opponents_cooperated):
    if round == r:
        return D
    
    if last_stock < (capacity / 4):
        return D
        
    threshold = (n - 1) * 0.5
    
    if opponents_cooperated >= threshold:
        reputation = min(0, reputation + 1)
        return C
    else:
        reputation = max(-2, reputation - 1)
        return D
```
'''

description_SELFINTERESTED_23 = '''
**Strategy: Threshold-Based Tit-for-Tat with Sustainability Correction**

The strategy calculates a "Safety Target" for the stock level and adjusts cooperation based on the observed aggregate cooperation of opponents.

**1. Variable Definitions**
*   `r`: Total rounds.
*   `t`: Current round index (1 to r).
*   `S_t`: Current stock at round t.
*   `O_C`: Number of opponents who cooperated in round t-1.
*   `n`: Number of players (n-1 opponents).
*   `History_Coop`: A running average of the fraction of opponents cooperating across previous rounds.

**2. Decision Rules**
In round 1, play `C`.
For all rounds `t > 1`, calculate the Cooperation Fraction ($F_{t-1} = O_C / (n-1)$):

*   **If $S_t < (capacity / 2)$:**
    *   If $F_{t-1} \ge 0.5$, play `C` to attempt to recover the stock.
    *   If $F_{t-1} < 0.5$, play `D` to extract remaining value before stock depletion (The "Run to the Exit" condition).

*   **If $S_t \ge (capacity / 2)$:**
    *   If $F_{t-1} > 0.5$, play `C` to maintain sustainability.
    *   If $F_{t-1} == 0.5$, play `C` with probability 0.5 (stochastic tit-for-tat to probe cooperation).
    *   If $F_{t-1} < 0.5$, play `D`.

**3. Edge Cases & Overrides**
*   **Final Round ($t = r$):** Always play `D`. Since there is no future state to preserve, defecting is the dominant strategy to maximize the final round payoff.
*   **Near-Zero Stock ($S_t \approx 0$):** If $S_t < (capacity / (2n))$, play `D` regardless of history. The stock is too low to sustain growth regardless of cooperation, and the immediate payoff is prioritized.
*   **Reciprocity Reset:** If the average history of opponent cooperation ($History\_Coop$) falls below 0.25, switch permanently to `D` for all remaining rounds, as the cooperative equilibrium is likely unattainable.

**4. Pseudocode**

```python
def get_action(t, r, S_t, n, history):
    if t == r:
        return 'D'
    
    if S_t < (capacity / (2 * n)):
        return 'D'
        
    if t == 1:
        return 'C'
        
    # Observe previous round cooperation
    F_prev = count_opponents_cooperated() / (n - 1)
    
    # Strategy Logic
    if S_t < (capacity / 2):
        return 'C' if F_prev >= 0.5 else 'D'
    else:
        if F_prev > 0.5:
            return 'C'
        elif F_prev == 0.5:
            return 'C' if random() > 0.5 else 'D'
        else: # F_prev < 0.5
            return 'D'
```
'''

description_SELFINTERESTED_24 = '''
The strategy employs a conditional cooperative approach (Tit-for-Tat variant) designed to sustain maximum stock levels for the duration of the game while punishing defectors.

### Core Strategy Rules

1. **Initial Round ($t=1$):** Always play **Cooperate (C)**. This establishes a cooperative baseline.

2. **Subsequent Rounds ($t > 1$):** Play **Cooperate (C)** if and only if all other players cooperated in the previous round. If any player defected in the previous round, switch to **Defect (D)**.

3. **Restoration Rule:** If the current stock $S$ falls below a sustainability threshold $T = \frac{capacity}{2}$, switch to **Cooperate (C)** regardless of previous rounds, continuing this until the stock recovers to $S \ge T$. If all players return to cooperative play, resume the standard conditional logic.

4. **Final Round ($t=r$):** Switch to **Defect (D)** regardless of history. The sustainability of the stock is irrelevant for future rounds, and there is no future penalty for defection.

### Pseudocode Logic

```python
def decide_action(round, current_stock, prev_round_actions, n, capacity):
    # 1. Terminal condition
    if round == r:
        return D

    # 2. Sustainability check
    # If stock is depleted below 50% capacity, prioritize resource recovery
    threshold = capacity / 2
    if current_stock < threshold:
        return C

    # 3. First round
    if round == 1:
        return C

    # 4. Tit-for-tat logic
    # Check if all opponents cooperated in the previous round
    # Assuming 'prev_round_actions' indicates the count of defectors
    if prev_round_actions.defectors == 0:
        return C
    else:
        return D
```

### Edge Cases and Behavior

*   **Stock Exhaustion:** If the stock reaches 0, the game state cannot recover (since growth becomes 0). The logic prioritizes cooperation early to prevent this. If the stock drops dangerously low, the Restoration Rule forces cooperation to ensure the pool remains viable for as long as possible, overriding the desire to punish defectors.
*   **Opponent Defection:** When the Tit-for-Tat logic detects defection, the strategy immediately switches to Defect (D) in the next round. This captures the higher payoff available when others defect, mitigating losses. It resumes cooperation only if the opponents demonstrate a return to cooperative behavior in the subsequent round, provided the stock is not in a critical state.
*   **Final Round Defection:** This assumes rational self-interest. Since there is no $r+1$ state, the long-term payoff from resource preservation is zero, making defection the dominant strategy in the final step.
'''

description_SELFINTERESTED_25 = '''
The strategy employs a conditional "Tit-for-Tat with Forgiveness" approach, modified for a continuous resource environment to prioritize long-term stock sustainability while maximizing short-term yield.

### Decision Rules

For round $t$, define $C_{t-1}$ as the number of players who chose "Cooperate" in the previous round.

1.  **Round 1:** Play **Cooperate (C)**.
2.  **Rounds 2 to $r-1$:**
    *   If $C_{t-1} = n$ (all cooperated): Play **Cooperate (C)**.
    *   If $C_{t-1} < n$:
        *   If current stock $S_t > \text{capacity} / 2$: Play **Defect (D)** to capture surplus.
        *   If current stock $S_t \le \text{capacity} / 2$: Play **Cooperate (C)** to initiate resource recovery.
3.  **Round $r$ (Final Round):**
    *   Play **Defect (D)** regardless of history, as there is no future state to preserve.

### Handling Edge Cases

*   **Low Stock Trap:** If $S_t \le \text{capacity} / (2n)$, the resource is near collapse. Even if opponents defected previously, play **Cooperate (C)** until $S_t$ returns to a level where the recovery rate is positive (i.e., $S_t > 0$).
*   **Opponent Defection:** If the group behavior shows a consistent trend of defection ($C_{t-1} < n/2$ for two consecutive rounds), switch to permanent **Defect (D)** for the remainder of the game, as cooperation is effectively subsidizing opponent greed.
*   **Perfect Recovery:** If $S_t \ge 0.9 \times \text{capacity}$, play **Defect (D)** for that round to extract the excess, then resume **Cooperate (C)** in the next round to return to the sustainable equilibrium.

### Pseudocode Implementation

```python
def select_action(t, r, n, S_t, C_history):
    # Final round greed
    if t == r:
        return "D"
    
    # First round start
    if t == 1:
        return "C"
        
    # Check for unsustainable collapse
    if S_t <= (capacity / (2 * n)):
        return "C"
        
    # Observe recent history
    C_prev = C_history[-1]
    
    # Analyze group behavior trend
    is_group_cooperative = (C_prev == n)
    
    # If the group is cooperating, follow suit
    if is_group_cooperative:
        return "C"
        
    # If group is defecting, exploit surplus or preserve minimal stock
    if S_t > (capacity / 2):
        return "D"
    else:
        return "C"
```
'''

description_SELFINTERESTED_26 = '''
Play **Adaptive Tit-for-Tat with Sustainable Thresholds**.

### Decision Rules
Define a "Sustainable Stock Threshold" $T$ as $0.5 \times \text{capacity}$. Define $k$ as the number of opponents who cooperated in the previous round.

1. **Initial Round:** Play $C$.
2. **Subsequent Rounds (if $t < r$):**
   - If `stock` $\ge T$:
     - If $k \ge n - 1$: Play $C$. (Reward universal cooperation)
     - If $k < n - 1$: Play $D$. (Punish defection when stock is healthy to capture immediate gains before the pool depletes)
   - If `stock` $< T$:
     - If $k = n - 1$: Play $C$. (Restore the pool)
     - If $k < n - 1$: Play $D$. (Abandon sustainability; extract maximum value before the pool crashes)
3. **Final Round ($t = r$):**
   - Play $D$ regardless of stock level or history.

### Edge Cases
- **Low Stock Collapse:** If the `stock` is less than or equal to $1/n$ of the initial capacity and previous rounds show high defection, ignore sustainability and play $D$ for the remainder of the game to maximize terminal extraction.
- **Opponent Dynamics:** Treat the aggregate count of $k$ as the primary signal. If the majority of the population consistently defects, switch to permanent defection strategy immediately, as sustainable play is mathematically impossible with defecting agents.
- **Population Extinction:** If `stock` reaches $0$, cease all attempts at cooperation and play $D$ (as the payoff becomes $0$ regardless, this fulfills the condition for any action).

### Pseudocode Logic
```python
def get_action(round, stock, prev_opponents_cooperated):
    n = number_of_players - 1 # opponents
    
    if round == total_rounds:
        return D
        
    if stock < (capacity * 0.1): # Near terminal state
        return D
        
    if stock >= (capacity * 0.5):
        if prev_opponents_cooperated >= (n - 1):
            return C
        else:
            return D
    else: # Stock stressed
        if prev_opponents_cooperated >= (n - 1):
            return C
        else:
            return D
```
'''

description_SELFINTERESTED_27 = '''
**Decision Rules:**

Define the state $S_t$ as the stock level at the start of round $t$, and $k_t$ as the number of cooperators observed in the previous round $t-1$. Let $c_i$ be the strategy variable for the current round.

1. **Initial Round ($t=1$):**
   Play $C$. Establish cooperative baseline to maintain the maximum growth potential of the common pool.

2. **Subsequent Rounds ($t > 1$):**
   Adopt a "Tit-for-Tat with Sustainability Threshold" strategy:
   * **Condition A (Sustainability):** If $S_t < (capacity / n)$, play $D$. The stock has degraded to a level where recovery is inefficient or unlikely; prioritize immediate extraction before the pool collapses.
   * **Condition B (Cooperation):** If $S_t \geq (capacity / n)$, calculate the observed cooperation rate of the population from the previous round, $\rho = k_{t-1} / n$.
      * If $\rho \geq 0.5$, play $C$.
      * If $\rho < 0.5$, play $D$.

3. **Final Round ($t = r$):**
   Always play $D$. Since there are no future rounds, the penalty for depleting the stock is zero; maximize extraction immediately.

**Pseudocode:**

```python
def choose_action(current_round, total_rounds, current_stock, capacity, num_players, prev_round_cooperators):
    # 1. Final round defection
    if current_round == total_rounds:
        return 'D'
    
    # 2. Initial round cooperation
    if current_round == 1:
        return 'C'
    
    # 3. Sustainability check
    # If the stock is too low to sustain growth (below 1/n of capacity), maximize extraction
    if current_stock < (capacity / num_players):
        return 'D'
    
    # 4. Adaptive response
    # Reciprocate the majority behavior of the population
    cooperation_rate = prev_round_cooperators / num_players
    if cooperation_rate >= 0.5:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
* **Stock Crash:** If $S_t = 0$, the payoff is 0 regardless of action. The strategy defaults to $D$ if encountered, though the Sustainability Condition (Condition A) will catch this state before it persists, ensuring extraction occurs at the last possible moment of solvency.
* **Tie-breaking:** In the decision rule $\rho \geq 0.5$, ties (exactly 50% cooperation) result in $C$. This maintains cooperation in neutral states, preserving the pool for another round.
'''

description_SELFINTERESTED_28 = '''
Adopt a conditional cooperation strategy governed by a state-dependent threshold (trigger) mechanism, designed to maximize long-term yield by maintaining the common pool at or near capacity while punishing defectors.

**Decision Rules**

In any round *t*, let $S_t$ be the current stock, $n$ be the number of players, and $k_t$ be the observed number of cooperators in the previous round.

1.  **Phase 1: Cooperation Maintenance (Normal Operations)**
    If $S_t \ge 0.5 \times \text{capacity}$ and $t < r$:
    *   Cooperate if the previous round's cooperation rate ($k_{t-1}/n$) was greater than or equal to a critical sustainability threshold, defined as $\tau = (2n-2)/(2n)$.
    *   Defect if the previous round's cooperation rate was less than $\tau$.

2.  **Phase 2: Restoration (Low Stock)**
    If $S_t < 0.5 \times \text{capacity}$:
    *   Cooperate regardless of previous history. This prioritizes resource recovery. Once $S_t$ returns to $\ge 0.5 \times \text{capacity}$, revert to Phase 1.

3.  **Phase 3: Terminal Defection (Final Round)**
    If $t = r$:
    *   Defect. With no future rounds, the penalty of stock depletion is zero, and the payoff for defection strictly dominates cooperation.

**Handling Edge Cases**

*   **Round 1:** Play Cooperate. Establishing cooperative behavior is necessary to prevent immediate resource collapse and signal a non-predatory strategy.
*   **Persistent Defection:** If the system is in Phase 1 and the observed cooperation rate falls below $\tau$ for two consecutive rounds, switch to Defect for the next round regardless of $S_t$. This acts as a 'tit-for-tat' deterrent against groups that consistently fail to maintain the resource.
*   **Recovery Failure:** If the stock $S_t$ remains below $0.1 \times \text{capacity}$ for three consecutive rounds despite cooperation, the resource is effectively unrecoverable within the remaining timeframe. Switch to Defect for all remaining rounds to extract remaining value.

**Pseudocode**

```python
def choose_action(round, total_rounds, stock, prev_k, capacity, n):
    if round == total_rounds:
        return D
    
    if stock < 0.1 * capacity and rounds_of_failure > 3:
        return D

    if stock < 0.5 * capacity:
        return C
    
    threshold = (2 * n - 2) / (2 * n)
    if (prev_k / n) >= threshold:
        return C
    else:
        return D
```
'''

description_SELFINTERESTED_29 = '''
Adopt a "Tit-for-Tat with Resilience" approach, focusing on maintaining long-term stock sustainability while punishing excessive consumption.

### Variables and Tracking
*   **$k$**: The number of rounds remaining.
*   **$c_t$**: The number of opponents who cooperated in round $t$.
*   **$d_t$**: The number of opponents who defected in round $t$ ($d_t = n - 1 - c_t$).
*   **$S_t$**: The current stock level at the start of round $t$.
*   **Target consumption ratio**: Maintain a strategy that approximates full cooperation as long as the stock allows for sustainable growth.

### Decision Rules
1.  **Round 1:** Play **Cooperate (C)**. Establish a cooperative baseline.

2.  **Rounds 2 to $r-1$:**
    *   **If stock $S_t$ is below a critical threshold (defined as $S_t < \text{capacity}/4$):** Play **Cooperate (C)**. When the stock is critically low, defection leads to stock collapse and zero payoffs for all future rounds. Cooperation is the only path to potential recovery.
    *   **If the previous round's behavior indicates mass defection:** Calculate the total consumption of the previous round. If total consumption exceeded the stock growth capacity (leading to stock depletion), play **Cooperate (C)** to minimize further damage to the pool.
    *   **If the previous round was stable (total consumption $\leq$ growth):** Play **Defect (D)** if the goal is to maximize immediate return, *unless* the number of cooperators from the previous round ($c_{t-1}$) was $\geq \lceil n/2 \rceil$. If $c_{t-1} \geq \lceil n/2 \rceil$, play **Cooperate (C)** to sustain the equilibrium.
    *   **Punishment/Trigger:** If at any point the stock drops below the level where the next round's stock could hit 0 due to the *average* previous consumption, shift to **Cooperate (C)** for all remaining rounds to prevent total extinction.

3.  **Final Round ($r$):**
    *   Play **Defect (D)** regardless of history, provided $S_r > 0$. Since there are no future rounds to preserve, the self-interested action is to maximize the final immediate payout. If $S_r = 0$, the action is irrelevant.

### Logic Pseudocode
```python
def choose_action(round_number, total_rounds, current_stock, prev_opponents_cooperated, n):
    # Terminal phase: Always defect if potential payoff exists
    if round_number == total_rounds:
        return 'D'
    
    # Critical state: Stock is near exhaustion, forced cooperation
    if current_stock < (capacity / 5): 
        return 'C'
    
    # Tit-for-tat logic based on previous aggregate behavior
    # If the majority cooperated, maintain the cooperative state
    # Threshold for cooperation is set at n/2
    if prev_opponents_cooperated >= (n / 2):
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling
*   **Stock Exhaustion:** If $S_t = 0$, the payoff is 0 regardless of action. Continue to play **Cooperate (C)** to allow the stock the maximum mathematical possibility of regeneration through growth dynamics.
*   **Small $n$ (n=2):** The threshold for cooperation becomes highly sensitive. If an opponent defects, the stock drops significantly. If $S_t$ drops below $\text{capacity}/2$, switch to permanent **Cooperate (C)** to ensure the stock recovers for the final rounds.
*   **Sudden Stock Shock:** If $S_t$ unexpectedly drops by more than $50\%$ in a single round, assume the population is trending toward total defect and play **Cooperate (C)** to preserve the remaining stock for as long as possible until the game ends.
'''

description_SELFINTERESTED_30 = '''
Implement a Trigger-Based Tit-for-Tat variant with a stock-preservation threshold. Let $C_t$ be the number of players who cooperated in the previous round, $S_t$ be the current stock level, and $d$ be the history of observed cooperation.

**Decision Logic:**

1.  **Initialization (Round 1):** Play Cooperate (C).

2.  **Endgame Threshold (Round $r$):** Play Defect (D). Since there is no future round to benefit from stock replenishment, defecting maximizes the final payoff regardless of the state.

3.  **Intermediate Rounds ($1 < t < r$):**
    *   **Cooperation Trigger:** If the aggregate cooperation in the previous round $C_{t-1} = n$, play Cooperate (C).
    *   **Stock Criticality:** Calculate the stock level $S_{crit}$ required to sustain future rounds. If $S_t < \frac{capacity}{n}$, assume the resource is collapsing regardless of cooperation; play Defect (D) to extract remaining value before exhaustion.
    *   **Punishment:** If $C_{t-1} < n$, calculate the defection ratio. Play Defect (D) for the next $k$ rounds, where $k$ is proportional to the observed depletion. A simple heuristic is $k = \lceil \frac{n - C_{t-1}}{n} \times (r-t) \rceil$.
    *   **Restoration:** If the punishment phase $k$ is complete and $S_t \ge \frac{capacity}{n}$, resume cooperation (C) to attempt to signal coordination and restore the pool.

**Pseudocode:**

```python
def get_action(round, total_rounds, n, stock, capacity, last_round_cooperators):
    # End of game
    if round == total_rounds:
        return 'D'
    
    # Resource exhaustion check
    if stock < (capacity / n):
        return 'D'
    
    # Initial round
    if round == 1:
        return 'C'
        
    # Coordination maintenance
    if last_round_cooperators == n:
        return 'C'
        
    # Punishment for past defection
    # Calculate punishment duration based on how many defected
    punishment_severity = (n - last_round_cooperators) / n
    punishment_rounds = ceil(punishment_severity * (total_rounds - round))
    
    # If currently in a punishment window, stay defecting
    if self.punishment_counter > 0:
        self.punishment_counter -= 1
        return 'D'
    
    # If everyone defected, punish aggressively
    if last_round_cooperators < n:
        self.punishment_counter = punishment_rounds
        return 'D'
        
    return 'C'
```
'''

description_SELFINTERESTED_31 = '''
The strategy employs a "Sustainable Trigger" mechanism, prioritizing the maintenance of the common pool stock while punishing defection to prevent ruin.

**Strategy Definition**

1. **State Tracking**: Maintain a memory of the previous round's stock ($S_{t-1}$), the previous round's total consumption, and the number of cooperative actions observed in the previous round ($k_{t-1}$).

2. **First Round (t=1)**: 
   Always play **Cooperate (C)**. This tests for general cooperativeness without immediately depleting the common pool.

3. **Subsequent Rounds (2 ≤ t < r)**:
   - **Condition for Cooperation**: Play **Cooperate (C)** if *all* of the following criteria are met:
     - The stock at the start of the current round ($S_t$) is greater than or equal to $S_{t-1}$ OR $S_t \ge 0.5 \times \text{capacity}$.
     - In the previous round, at least $(n-1)$ players played **Cooperate (C)**.
   - **Condition for Defection**: Play **Defect (D)** if:
     - The stock at the start of the current round ($S_t$) is below a critical threshold (defined as $< 0.25 \times \text{capacity}$), signaling that the pool is being depleted regardless of your cooperation.
     - OR, in the previous round, more than one player played **Defect (D)**. 

4. **Last Round (t=r)**:
   - Play **Defect (D)** regardless of history. Since there is no future, there is no incentive to preserve the stock.

**Pseudocode Logic**

```python
def choose_action(round_t, current_stock, prev_stock, prev_cooperators, n, capacity):
    # Rule 1: Terminal round exploitation
    if round_t == total_rounds:
        return 'D'
    
    # Rule 2: First round cooperation
    if round_t == 1:
        return 'C'
    
    # Rule 3: Punish systemic defection or critical stock depletion
    # If more than one defector last round, punish
    prev_defectors = n - prev_cooperators
    if prev_defectors > 1:
        return 'D'
    
    # Rule 4: If stock is critically low, defect to extract remaining value
    if current_stock < (0.25 * capacity):
        return 'D'
        
    # Rule 5: Cooperative equilibrium
    # If the stock is healthy or regenerating, cooperate
    if current_stock >= prev_stock or current_stock >= (0.5 * capacity):
        return 'C'
        
    # Default to defection if trends are downward and stock is mid-tier
    return 'D'
```

**Edge Case Handling**
- **Critical Stock Loss**: If the stock drops below the $0.25 \times \text{capacity}$ threshold, the strategy switches to **Defect (D)** permanently, assuming the common pool is collapsing and future returns are negligible.
- **"Grim" Response**: The strategy is sensitive to defection; if more than one player defects, the strategy defaults to **Defect (D)** in the subsequent round to minimize exploitation, only resuming **Cooperate (C)** if the stock levels recover sufficiently or if observing a return to full cooperation by the group in the following turn (by checking if the stock has stabilized or grown).
'''

description_SELFINTERESTED_32 = '''
The strategy employs a conditional "Tit-for-Tat with Forgiveness" approach, calibrated to protect the long-term sustainability of the stock while maximizing extraction when conditions allow.

**Strategy Definitions:**

*   **Current Cooperation Threshold ($T$):** Let $k$ be the number of opponents who cooperated in the previous round. The strategy uses a threshold $T = n - 1$. If $k \geq T$, the opponents are largely cooperating. If $k < T$, the group is defecting.
*   **Sustainability Check ($S_{min}$):** If the current stock $S < \text{capacity} / 4$, the pool is critically depleted. 
*   **Final Round Rule:** In round $r$, always play $D$.

**Decision Logic:**

1.  **Round 1:** Play $C$. Establish cooperative intent.

2.  **Rounds $2$ to $r-1$:**
    *   If $S < S_{min}$: Play $C$. Prioritize stock regeneration to avoid total depletion.
    *   If $k \geq T$: Play $C$. The group is maintaining the pool, so cooperate to maximize future total stock.
    *   If $k < T$: Play $D$. If others are depleting the pool, extract the maximum value before the stock collapses.
    *   *Correction/Forgiveness:* If the strategy played $D$ in the previous round, check if the group cooperation count $k$ has increased (i.e., opponents returned to cooperation). If $k \geq T$, play $C$ in the current round to resume cooperative equilibrium.

3.  **Round $r$:** Play $D$. Harvest remaining resources before the game terminates.

**Pseudocode:**

```python
def decide_action(round_number, n, capacity, current_stock, last_round_opponents_cooperated):
    # Base check
    if round_number == r:
        return D
    
    # Critical sustainability
    if current_stock < (capacity / 4):
        return C
        
    # Initial round
    if round_number == 1:
        return C
        
    # Check current group behavior
    threshold = n - 1
    
    # If the group is cooperating, continue cooperating
    if last_round_opponents_cooperated >= threshold:
        return C
    
    # If the group is defecting, defect to protect individual payoff
    else:
        return D
```
'''

description_OPPORTUNISTIC_5 = '''
The strategy employs a conditional "Tit-for-Tat" variant adjusted for dynamic resource thresholds, maximizing immediate yield while enforcing sustainability through punishment. It treats the resource stock as a finite asset to be harvested aggressively if the collective behavior deviates from sustainability, but sustained if cooperation is stable.

### Decision Rules

The strategy maintains an internal state variable $H$, representing the "Cooperation History Score," initialized to $0$.

**Round 1:**
- Play **C** (Cooperate).

**Rounds 2 to $r-1$:**
1.  **Observe Last Round:** Calculate $k$, the number of opponents who played **C** in the previous round.
2.  **Update State:** Update $H = H + (k / (n-1)) - 0.5$. (This tracks the relative cooperation rate of the population).
3.  **Evaluate Thresholds:**
    *   **Sustainable Harvest:** If the current stock $S \ge 0.5 \times \text{capacity}$ AND the most recent round had at least $(n-1)$ cooperators (including self), play **C**.
    *   **Opportunistic Harvesting:** If $H < -2.0$ (indicating persistent defection) OR if the current stock $S < 0.25 \times \text{capacity}$ (risking collapse), play **D** (Defect). By playing **D** when stock is critically low or others are defecting, the strategy captures a larger share of the depleting pool before it hits zero.
    *   **Default:** Play **C** if $H \ge -2.0$ and stock is healthy; otherwise, play **D**.

**Final Round ($r$):**
- Regardless of history, play **D** (Defect). Since there is no future benefit to maintaining the resource, consume the maximum possible share of the remaining stock.

### Edge Case Handling

1.  **Low Stock Collapse:** If $S \approx 0$ (calculated as $S < (\text{consumption per C player})$), play **D** regardless of history. When the resource is effectively exhausted, cooperation provides negligible payout; switching to **D** maximizes the final crumbs.
2.  **Sudden Cooperation Recovery:** If the strategy has been playing **D** due to low $H$ but $k$ increases to $(n-1)$ for two consecutive rounds, reset $H = 0$ and switch back to **C** to resume sustainable harvesting.
3.  **Tie-Breaking:** If current stock is exactly at a boundary condition, prioritize **D** if the current round index $t > 0.75 \times r$ (accelerating harvest as the game nears end).

### Pseudocode

```python
# Constants
capacity = ...
n = ...

# Variables
H = 0 
round_index = 1

def choose_action(S, prev_round_opponents_C):
    # Terminal Round
    if round_index == r:
        return 'D'
        
    # Terminal Phase Acceleration
    if round_index > 0.75 * r:
        return 'D'
    
    # History Update (if not round 1)
    if round_index > 1:
        H += (prev_round_opponents_C / (n - 1)) - 0.5
        
    # Decision Logic
    is_stable = (prev_round_opponents_C == (n - 1))
    
    if S < 0.25 * capacity or H < -2.0:
        return 'D'
    elif is_stable and S >= 0.5 * capacity:
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_6 = '''
The strategy employs a conditional trigger-based mechanism with an "opportunistic" modification to maximize yield when the stock is robust and punish exploitation when the stock is vulnerable.

### Strategy Rules

**Phase 1: Initialization**
In Round 1, always play **Cooperate (C)** to establish a baseline of sustainability and gauge opponent behavior.

**Phase 2: Monitoring and Retaliation**
Maintain a memory variable `is_punishing` (initially False) and a reputation score `reputation` (initially 0).
*   For each round *t > 1*:
    *   Assess the behavior of opponents in round *t-1* based on the observed change in stock relative to the expected change if all players had cooperated.
    *   If the observed stock *S_observed* < *S_expected_if_all_C*, update `reputation` negatively.
    *   If `reputation` falls below a threshold (e.g., -0.5 × *n*), set `is_punishing` to True.

**Phase 3: Decision Logic**
In each round, determine the action *A* based on current stock *S* and `is_punishing`:

```pseudocode
if (t == r): 
    # Final round: Opportunistic grab
    return Defect (D)

if (is_punishing):
    # Retaliation mode: Ensure stock depletion to limit long-term payoff of defectors
    return Defect (D)

if (S > 0.8 * capacity):
    # High-stock opportunity: Maximize individual yield
    return Defect (D)

if (S < 0.2 * capacity):
    # Emergency: Forced cooperation to prevent total collapse
    return Cooperate (C)

# Normal conditions: Reciprocate based on previous round's cooperation
if (opponents_cooperated_ratio > 0.5):
    return Cooperate (C)
else:
    return Defect (D)
```

**Phase 4: Adjustment**
*   **Opportunistic Threshold:** If *S* > 0.8 * capacity, the system is underutilized. Play **Defect (D)** to capture surplus that will otherwise be lost to the growth dynamics' diminishing returns or consumed by others.
*   **Emergency Floor:** If *S* < 0.2 * capacity, the resource is nearing collapse. Force **Cooperate (C)** to ensure future rounds remain viable, ignoring previous defection history.
*   **Last Round:** Always play **Defect (D)**. Since no future rounds exist to receive the benefits of the resource stock, the optimal opportunistic move is to extract the maximum possible value.
*   **Reset:** If `is_punishing` is True, reset `is_punishing` to False only if *S* returns to > 0.5 * capacity and opponents cooperate for two consecutive rounds.
'''

description_OPPORTUNISTIC_7 = '''
### Opportunistic Tit-for-Tat Strategy

**Core Logic:**
The strategy maintains a "Target Cooperation Level" ($TCL$) based on the current stock level and the number of remaining rounds. It attempts to maximize immediate gain while ensuring the resource does not collapse, utilizing a conditional response mechanism to punish defectors.

**Decision Rules:**

1.  **Initialization (Round 1):** Play Cooperate (C).

2.  **Target Calculation:** At the beginning of each round $t$, calculate the "Sustainability Threshold" ($S_{min}$):
    *   $S_{min} = capacity / (n+1)$.
    *   If $S < S_{min}$, immediately switch to Defect (D) for all remaining rounds to extract maximum value before the pool collapses.

3.  **Action Determination (Rounds 2 to $r-1$):**
    *   Let $N_c$ be the number of cooperators observed in the previous round.
    *   If $N_c = n-1$ (all opponents cooperated), play C.
    *   If $N_c < n-1$, play D with probability $p = 1 - (N_c / (n-1))$. In deterministic mode, play D if $N_c < n-1$.
    *   If the stock $S$ has dropped by more than 25% from the previous round despite a previous cooperative state, play D.

4.  **End-Game Strategy (Final Round $r$):**
    *   Always play D. There is no incentive to preserve the pool for a non-existent $r+1$ state.

**Pseudocode:**

```python
def get_action(round, n, S, last_round_stats):
    # End-game override
    if round == r:
        return D

    # Collapse imminent
    if S < (capacity / (n + 1)):
        return D

    # First round
    if round == 1:
        return C

    # Retrieve opponent behavior from history
    # last_round_stats provides N_c (number of cooperators in previous round)
    N_c = last_round_stats.cooperators
    
    # Conditional Response:
    # Punish if opponents defected, cooperate if they maintained trust
    if N_c >= (n - 1):
        return C
    else:
        return D
```

**Edge Case Handling:**
*   **Rapid Depletion:** If the stock level $S$ is below 10% of $capacity$, the strategy treats the game as effectively over and plays D regardless of history.
*   **Recovery:** If the stock level $S$ is near $capacity$ (>= 0.9 * capacity), the strategy is biased toward C to maintain high yields, only switching to D if $N_c < n-1$ (detected cheating).
*   **Anonymity:** Since individuals are indistinguishable, the strategy treats the group as a single aggregate entity. Punishment (playing D) applies to the collective group response rather than specific individuals.
'''

description_OPPORTUNISTIC_8 = '''
**Strategy: Dynamic Threshold Reciprocity**

This strategy relies on monitoring the total cooperation rate of opponents to determine the sustainability of the pool and adjusting action accordingly. It prioritizes long-term resource maintenance while exploiting periods of high cooperation and punishing systemic over-consumption.

**State Variables:**
*   $c_{t-1}$: Number of opponents who chose Cooperate in the previous round ($0 \le c_{t-1} \le n-1$).
*   $S_t$: Current stock at start of round $t$.
*   $T$: Total rounds remaining (current round index $t$ vs total $r$).

**Decision Logic:**

1.  **Initialization (Round 1):**
    Play **Cooperate (C)**. Establishing cooperative baseline is necessary to maximize long-term $S$.

2.  **Steady State (Rounds $2$ to $r-1$):**
    Calculate the "Cooperation Threshold" $K$ required to maintain the stock level:
    $K = (n - 1) / 2$
    
    If $c_{t-1} \ge K$:
    Play **Cooperate (C)**. Maintain pool health when the aggregate behavior is sustainable.

    If $c_{t-1} < K$ AND $S_t > (\text{capacity} / 4)$:
    Play **Defect (D)**. Shift to opportunistic extraction. If the group is depleting the resource, extract higher immediate value before the stock collapses.

    If $c_{t-1} < K$ AND $S_t \le (\text{capacity} / 4)$:
    Play **Cooperate (C)**. If the stock is critically low, defecting guarantees extinction. Even if opponents defect, cooperate to attempt restoration or mitigate the crash.

3.  **Terminal Phase (Final Round $r$):**
    Play **Defect (D)** regardless of history. There is no future value to preserve the pool.

**Pseudocode:**

```python
def get_action(round_idx, total_rounds, current_stock, prev_opponents_cooperated, n):
    # Terminal phase: Extract everything
    if round_idx == total_rounds:
        return D
    
    # Round 1: Build trust
    if round_idx == 1:
        return C
    
    # Threshold for sustainability (derived from n)
    sustainability_threshold = (n - 1) / 2
    
    # Opportunistic logic
    if prev_opponents_cooperated >= sustainability_threshold:
        return C
    else:
        # Stock safety check: prevent immediate depletion if pool is low
        if current_stock > (capacity / 4):
            return D
        else:
            return C
```
'''

description_OPPORTUNISTIC_9 = '''
Play Cooperate ($C$) for all rounds $t < r$, provided the common pool stock $S_t$ exceeds a sustainability threshold $T = \text{capacity} / n$. If the current stock $S_t$ falls below $T$, switch to Defect ($D$) immediately for all remaining rounds. 

In the final round ($t = r$), always play Defect ($D$).

### Decision Logic:
1.  **Round 1:** Play $C$.
2.  **Rounds $1 < t < r$:**
    *   Observe the total consumption and resulting $S_t$ from the previous round.
    *   If $S_t \ge \text{capacity} / n$: Play $C$.
    *   If $S_t < \text{capacity} / n$: Play $D$.
3.  **Round $t = r$:**
    *   Play $D$.

### Edge Case Handling:
*   **Near-Depletion:** If at any point $S_t = 0$, Defect ($D$) for all remaining rounds, as the resource cannot regenerate.
*   **Opponent Behavior:** This strategy is insensitive to individual opponent identities, relying strictly on the aggregate state of the resource pool. It prioritizes long-term extraction maximization by maintaining the stock within the "golden ratio" of growth (where $S \approx \text{capacity}/2$ yields maximum replenishment) while retaining the option to capture residual value before the game terminates.
'''

description_OPPORTUNISTIC_10 = '''
Let `n` be the number of players, `r` be the total rounds, and `t` be the current round index (1-indexed). Let `S_t` be the stock at the start of round `t`. Let `C_count_t-1` be the number of players who cooperated in the previous round, and `D_count_t-1` be the number of players who defected.

**Core Strategy: Conditional Tit-for-Tat with Terminal Defection**

The strategy relies on maintaining the stock at capacity to maximize long-term yield while exploiting opportunities to defect when the stock is abundant or the game is ending.

**Decision Rules:**

1.  **First Round (t=1):**
    Always play **C**. Establish a baseline of cooperation.

2.  **Intermediate Rounds (1 < t < r):**
    Evaluate the cooperation rate of the population from the previous round (`C_count_t-1`).
    *   If `C_count_t-1 == n`: Play **C**. The system is stable; sustain the equilibrium.
    *   If `S_t > 0.8 * capacity` AND `C_count_t-1 < n`: Play **D**. The stock is high enough to absorb a defection without crashing the system; extract extra value.
    *   If `S_t <= 0.8 * capacity` AND `C_count_t-1 < n`: Play **C**. If the stock is threatened, prioritize recovery to prevent total collapse, despite opponent defection.

3.  **Terminal Round (t = r):**
    Always play **D**. There is no future value to preserve; maximize individual payoff by consuming the maximum possible share of the remaining stock.

**Pseudocode:**

```python
def decide_action(t, r, n, S_t, C_count_prev):
    # Rule 1: Always defect in the final round
    if t == r:
        return "D"
    
    # Rule 2: Start with cooperation
    if t == 1:
        return "C"
    
    # Rule 3: Conditional Adaptation
    if C_count_prev == n:
        return "C"
    
    # Opportunistic threshold for high stock
    # If the environment is healthy, extract surplus
    if S_t > (0.8 * capacity):
        return "D"
    
    # Fallback to cooperation to prevent system collapse
    return "C"
```

**Edge Case Handling:**
*   **Total Collapse (`S_t = 0`):** Regardless of the rule set, if `S_t == 0`, play **C**. Defecting yields 0 payoff and contributes to an unrecoverable state.
*   **Low `n` / High `r`:** The opportunistic threshold (`0.8 * capacity`) acts as a buffer. If the stock recovers quickly (e.g., small `n`), the strategy naturally reverts to cooperation once the stock is replenished, provided the history shows a return to stability.
*   **Sudden Defection:** If the group consensus breaks (many defectors), the strategy immediately shifts to cooperation if the stock falls below the 80% threshold, ensuring that the game does not terminate prematurely due to stock exhaustion.
'''

description_OPPORTUNISTIC_11 = '''
Define a target stock ratio $T = 0.5$. This represents the "sustainable maximum" where the resource regenerates at its optimal rate.

Maintain a state variable `forgiveness_level` (initially 0, range 0-5) representing the tolerance for defecting behavior in the group.

**Decision Logic:**

1.  **Terminal Round:** If round $t = r$, play **D** (Defect).

2.  **Initial Round:** If round $t = 1$, play **C** (Cooperate).

3.  **Standard Rounds (1 < t < r):**
    Evaluate the observed stock trajectory and opponent behavior:
    *   Calculate $G_{prev}$, the growth rate observed from the previous round: $G_{prev} = (\text{Stock}_{t} - \text{Stock}_{t-1\_remaining})$.
    *   If $\text{Stock}_t < (0.2 \times \text{capacity})$: Play **C**. If the stock is critically low, survival requires strict cooperation, regardless of opponent behavior.
    *   If the number of defectors in the previous round ($D_{count}$) exceeds $(n / 2) + \text{forgiveness\_level}$: Play **D**. Punish the group for excessive depletion.
    *   If $\text{Stock}_t > (0.8 \times \text{capacity})$ and $D_{count} < (n / 2)$: Play **D**. The stock is high enough to absorb opportunistic extraction without immediate collapse.
    *   Otherwise: Play **C**.

**Adjustment Rules:**

*   **Forgiveness Decay:** If the group cooperates ($D_{count} = 0$) for 3 consecutive rounds, increment `forgiveness_level` by 1.
*   **Punishment Reset:** If playing **D** results in a significant increase in the stock level in the following round (stock increases compared to previous state), immediately reset `forgiveness_level` to 0 and switch to **C**.

**Pseudocode Logic:**

```
if t == r:
    return D
if t == 1:
    return C

if stock_t < (0.2 * capacity):
    return C

if D_count_prev > (n/2 + forgiveness_level):
    return D

if stock_t > (0.8 * capacity) and D_count_prev < (n/2):
    return D

return C
```
'''

description_OPPORTUNISTIC_12 = '''
### Strategy: Tit-for-Tat Resource Harvesting

This strategy operates on the principle of conditional cooperation, maintaining the maximum sustainable yield when the population exhibits restraint, while exploiting the resource when systemic collapse is inevitable or when others have already defected.

**Decision Logic**

The strategy tracks a reputation variable, `R`, initially set to 0.5 (neutral). For every round `t`, the strategy observes the number of cooperators `k` from the previous round `t-1`.

1.  **Round 1:** Play **Cooperate (C)**.
2.  **Round $r$ (Final Round):** Play **Defect (D)**.
3.  **Intermediate Rounds ($1 < t < r$):**
    *   Calculate the cooperation threshold: `T = 0.5 * n`.
    *   Update reputation: `R = (R * 0.7) + (k / n) * 0.3`.
    *   Assess stock health: If `Stock < (capacity / n)`, the resource is critically low; play **Defect (D)** to capture remaining value before collapse.
    *   Decision:
        *   If `R >= 0.6` (high collective trust): Play **Cooperate (C)**.
        *   If `R < 0.4` (pervasive defection): Play **Defect (D)**.
        *   Otherwise (unstable cooperation): Play **Cooperate (C)** if `k >= T`, else play **Defect (D)**.

**Pseudocode**

```python
def decide_action(round_num, total_rounds, n, capacity, current_stock, prev_cooperators):
    # Final Round Opportunism
    if round_num == total_rounds:
        return "D"
    
    # First Round Cooperation
    if round_num == 1:
        return "C"
        
    # Crisis Management
    if current_stock < (capacity / n):
        return "D"
        
    # Reputation-based Conditional Cooperation
    # Update reputation R (assume R is stored state)
    R = (R * 0.7) + (prev_cooperators / n) * 0.3
    
    if R >= 0.6:
        return "C"
    elif R < 0.4:
        return "D"
    else:
        # Tit-for-Tat logic
        return "C" if prev_cooperators >= (n / 2) else "D"
```

**Opportunistic Edge Case Handling**

*   **Sudden Collapse:** If the `current_stock` drops below a threshold where regeneration is mathematically impossible to recover within the remaining rounds, switch permanently to **Defect (D)** to maximize individual payout before total depletion.
*   **The "Defector's Exit":** In the round immediately preceding the final round, if the `current_stock` is insufficient to sustain $n$ cooperators in the final round, switch to **Defect (D)** early to front-run the anticipated final-round scramble.
*   **Recovery:** If the population returns to high cooperation (`prev_cooperators > T`), the reputation variable `R` will eventually rise above the `0.6` threshold, allowing the strategy to resume **Cooperate (C)** behavior even after periods of conflict.
'''

description_OPPORTUNISTIC_13 = '''
Strategy: "Tit-for-Tat with Resource-Aware Thresholding"

This strategy operates on a conditional cooperative basis, utilizing a moving threshold to track opponent aggregate cooperation and adjusting action based on the state of the common pool.

**Strategy Definitions:**
- **Cooperation Threshold (T):** A dynamic value determined by current stock (S) and round number (r_t). Start with T = 0.5 (expecting 50% cooperation from opponents).
- **Target Stock Ratio (SR):** The ratio of current stock (S) to capacity.
- **Opponent Cooperation Rate (OCR):** The fraction of total opponents who cooperated in the previous round.

**Decision Rules:**

1. **Round 1:**
   Play **Cooperate (C)**.

2. **Subsequent Rounds (t > 1):**
   - Calculate `OCR` = (Number of Cooperators / (n - 1)).
   - Evaluate `Stock Risk`: If `S < (capacity / 4)`, prioritize sustainability; if `S > (3 * capacity / 4)`, prioritize exploitation.

   - **Logic Flow:**
     ```python
     if t == r: # Final round
         return Defect (D)

     if S < (capacity / 2n): # Critical scarcity
         return Cooperate (C)

     # Conditional Response
     if OCR >= T:
         return Cooperate (C)
     else:
         return Defect (D)
     ```

3. **Adaptive Threshold Adjustment (Updates T after each round):**
   - If `OCR` > `T` (Opponents are more cooperative than expected):
     - Decrease `T` slightly (e.g., T = max(0.2, T - 0.05)) to encourage mutual cooperation.
   - If `OCR` < `T` (Opponents are less cooperative than expected):
     - Increase `T` (e.g., T = min(0.8, T + 0.1)) to protect against exploitation.
   - If `S` drops below `capacity / 2`:
     - Force `T` = 0.9 (drastically raise the bar for cooperation to stop depletion).

**Edge Cases:**
- **Sudden Depletion:** If `S` drops by more than 50% in a single round, override all logic and play **Cooperate (C)** for the next two rounds to allow stock recovery, regardless of `OCR`.
- **High Stock Opportunity:** If `S > (0.9 * capacity)`, play **Defect (D)** if `OCR < 0.5` to capture surplus value before the system self-regulates or collapses.
- **Tied Decisions:** If `OCR` equals `T` exactly, match the action played in the previous round (Win-Stay, Lose-Shift).
'''

description_OPPORTUNISTIC_14 = '''
Initialize a counter `opponents_defecting` to 0. Maintain a variable `is_exploiting` set to False.

**Round 1:**
Play Cooperate (C).

**Subsequent Rounds:**
1. **End-Game Phase:** If the current round is the final round (r), play Defect (D).
2. **Exploitation Trigger:** If `is_exploiting` is True, play Defect (D).
3. **Threshold Check:** Calculate the current stock (S). If S < (capacity / n), play Cooperate (C) to prevent resource collapse.
4. **Opportunistic Assessment:**
   Let `k` be the number of opponents who played Defect (D) in the previous round.
   - If `k` > 0 and `is_exploiting` is False:
     - Set `is_exploiting` to True.
     - Play Defect (D).
   - If `k` == 0:
     - Play Cooperate (C).
     - Reset `is_exploiting` to False.
5. **Default:** Play Cooperate (C).

**Pseudocode Logic:**
```python
if round == r:
    return D
if is_exploiting == True:
    return D
if S < (capacity / n):
    return C
if count_defecting_opponents > 0:
    is_exploiting = True
    return D
return C
```
'''

description_OPPORTUNISTIC_15 = '''
This strategy follows a "Conditional Tit-for-Tat with Yield Thresholds" logic. It balances cooperation to maintain long-term stock levels against opportunism to extract maximum value when the environment is stable or when the remaining rounds are few.

### Core Variables
- $S_t$: Current stock at start of round $t$.
- $k_t$: Number of players who cooperated in round $t-1$.
- $C_{target}$: The target cooperation count required to sustain the stock (set to $n$).
- $R_{rem}$: Remaining rounds ($r - t + 1$).

### Decision Rules

**Round 1:**
- Cooperate ($C$). The goal is to establish baseline stability and observe the collective behavior of opponents.

**Round $t$ ($1 < t < r$):**
- **Trigger A (Sustainability Check):** If $S_t < (\text{capacity} / 2)$, immediately Defect ($D$) for this round. The stock is too low to rely on regeneration; capture remaining value before depletion.
- **Trigger B (Cooperative Response):** If $S_t \ge (\text{capacity} / 2)$:
    - If $k_t \ge (n - 1)$, Cooperate ($C$). The system is stable; sustain the equilibrium.
    - If $k_t < (n - 1)$, Defect ($D$). The group is over-harvesting; switch to defensive extraction to avoid being the only contributor to a collapsing pool.

**Final Round ($t = r$):**
- Defect ($D$) regardless of history or stock level. This is the terminal state where long-term sustainability is irrelevant.

### Pseudocode

```python
def get_action(round_number, total_rounds, current_stock, capacity, n, last_round_cooperators):
    # Rule 1: Terminal Opportunism
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: Preservation Mode
    # If the stock is critically low, extraction priority overrides cooperation
    if current_stock < (capacity / 2):
        return 'D'
    
    # Rule 3: Tit-for-Tat Reciprocity
    # Only cooperate if almost everyone else was cooperating
    if round_number == 1:
        return 'C'
    
    if last_round_cooperators >= (n - 1):
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling
- **Low Stock:** If the stock drops below the threshold needed for regeneration (capacity / 2), the strategy ceases all cooperation, effectively transitioning to a "scavenger" mode to extract remaining resources before they hit zero.
- **High Stock, High Defection:** If the stock is healthy but opponents are defecting, the strategy will defect to protect individual payoff share, preventing the exploit of the cooperative agent by "free-rider" logic.
- **Low Stock, High Cooperation:** Even if the group is cooperating, if the stock is below the threshold, this strategy defects to secure a higher payoff from a depleting pool that is destined to collapse regardless of cooperative input.
'''

description_OPPORTUNISTIC_16 = '''
The strategy utilizes a conditional, state-sensitive mechanism that prioritizes sustainable yield early in the game while pivoting to exploitation as the terminal round approaches or if the stock is inevitably crashing.

### Decision Rules

1.  **State Assessment:** In each round `t` (where `t` goes from 1 to `r`), calculate the "Safety Threshold." The Safety Threshold is `(capacity / 2)`.
2.  **Strategic Phase:**
    *   **Cooperation Phase (Rounds 1 to r-2):**
        *   If `stock` > `Safety Threshold`: Play **Cooperate (C)**.
        *   If `stock` ≤ `Safety Threshold`: Play **Defect (D)**. This is a "harvest-and-exit" trigger, assuming that if the stock is already halved, the ecosystem's ability to regenerate has been critically compromised, making future-value maximization less viable than immediate extraction.
    *   **Terminal Phase (Rounds r-1 to r):**
        *   Always play **Defect (D)** regardless of current `stock`. This maximizes immediate return without regard for the future, as there is no future beyond round `r`.

### Handling Opponent Behavior (Adaptation)

The strategy incorporates a "Tit-for-Tat" filter within the Cooperation Phase to adjust to the aggregate behavior of the pool:

*   **Observation:** Track the average cooperation rate of the opponents in the previous round `t-1`.
*   **Reaction Rule:**
    *   If the aggregate opponent cooperation rate in the previous round was < 0.5 (indicating a majority of defectors): Immediately switch to **Defect (D)** for the current round, regardless of the `stock` level or current phase.
    *   If the aggregate opponent cooperation rate was ≥ 0.5: Resume the standard rules defined in the "Strategic Phase."

### Pseudocode

```
// Constants: r (total rounds), capacity
// Variables: t (current round), stock (current state), prev_coop_rate (from t-1)

if t == r or t == r - 1:
    return Defect

if t > 1 and prev_coop_rate < 0.5:
    return Defect

if stock <= (capacity / 2):
    return Defect

return Cooperate
```
'''

description_OPPORTUNISTIC_17 = '''
Strategy: Tit-for-Tat with Resource-Aware Thresholding

**Phase 1: Initialization**
In Round 1, always play C (Cooperate). This establishes a baseline of goodwill to test the ecosystem of strategies without immediately exhausting the common pool.

**Phase 2: Monitoring and Adaptation**
Let $c_t$ be the number of players who played C in the previous round $t-1$.
Calculate the "Sustainability Index" $S_t$ (the stock at the start of round $t$).

If the previous round's outcome resulted in a stock growth trajectory that maintains $S_t \ge \text{capacity} / 2$:
1. If $c_{t-1} \ge \lfloor 0.75n \rfloor$ (majority cooperation): Play C.
2. If $c_{t-1} < \lfloor 0.75n \rfloor$ (defection detected): Play D.

If the previous round's outcome resulted in $S_t < \text{capacity} / 2$ (resource danger zone):
1. Immediately switch to D regardless of historical cooperation. The pool is collapsing; extract immediate value before the stock hits zero.

**Phase 3: The End Game**
Define the horizon $H$ as the number of remaining rounds.
1. If $H \le 2$: Play D, regardless of current stock or past cooperation. In the final rounds, the future value of the stock becomes zero, removing the incentive to conserve.

**Pseudocode Implementation:**

```python
def play_round(round_number, total_rounds, n, stock, capacity, last_round_cooperators):
    # End-game logic
    if (total_rounds - round_number) < 2:
        return 'D'
    
    # First round initialization
    if round_number == 1:
        return 'C'
    
    # Resource exhaustion check
    if stock < (capacity / 2):
        return 'D'
    
    # Adaptive cooperation logic
    # Threshold for cooperation is 75% of players
    if last_round_cooperators >= (0.75 * n):
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_18 = '''
Adopt a "Conditional Sustainability" strategy that aims to maximize short-term gains while preventing total resource collapse. The core logic centers on maintaining the stock at or above the 50% capacity threshold to ensure maximum regeneration, while defecting whenever the long-term sustainability of the pool is secondary to immediate payout.

**Decision Rules**

Define `threshold` as 0.5 * `capacity`.
Define `n_cooperators` as the number of other players who chose 'C' in the previous round.
Define `cooperation_history` as the moving average of `n_cooperators` over the past 3 rounds.

1.  **First Round:** Play 'C'. This establishes a baseline and prevents immediate depletion of the initial optimal stock.

2.  **Rounds 2 to r-1:**
    *   If `stock` < (`threshold` * 0.8): Play 'C'. Prioritize survival to ensure there is a resource to exploit in the next round.
    *   If `stock` >= (`threshold` * 0.8) and `cooperation_history` > (`n` / 2): Play 'D'. If the group is largely cooperative and the resource is healthy, exploit the resource while the pool remains stable due to the collective restraint of others.
    *   If `stock` >= (`threshold` * 0.8) and `cooperation_history` <= (`n` / 2): Play 'C'. If the group is trending toward defectors, excessive consumption will collapse the pool; cooperate to keep the resource from hitting zero.

3.  **Last Round (r):**
    *   Play 'D'. Since there are no future rounds to sustain, prioritize maximizing the final individual payoff regardless of the resulting stock level.

**Pseudocode Logic**

```python
def choose_action(round_num, current_stock, history):
    if round_num == r:
        return 'D'
    
    if round_num == 1:
        return 'C'
        
    threshold = 0.5 * capacity
    n_cooperators_avg = mean(history.last_3_rounds.n_cooperators)
    
    if current_stock < (threshold * 0.8):
        return 'C'
    
    if n_cooperators_avg > (n / 2):
        return 'D'
    else:
        return 'C'
```

**Edge Case Handling**
*   **Rapid Stock Depletion:** If the `stock` falls below 10% of `capacity`, override all rules and play 'C' every round until the stock recovers above 20% of `capacity`, regardless of opponent behavior.
*   **Total Defection:** If the group shows 0 cooperators for two consecutive rounds, assume the environment has entered a "tragedy of the commons" phase where the resource will inevitably hit zero. Switch to 'D' immediately for all subsequent rounds to extract remaining value before exhaustion.
'''

description_OPPORTUNISTIC_19 = '''
The strategy follows a conditional, history-dependent approach designed to maximize individual payoff while leveraging the growth dynamics of the common pool. The core logic is to cooperate when the pool is at risk of depletion and defect when the pool is sufficiently robust to absorb high consumption without crashing.

**Definitions:**
*   $k$: Number of previous rounds.
*   $S_t$: Current stock at start of round $t$.
*   $C_t$: Number of players who cooperated in round $t$ (including self).
*   $D_t$: Number of players who defected in round $t$ (including self).
*   $\text{Threshold}_L$: A critical stock level (defined as $0.25 \times \text{capacity}$) below which sustainability is prioritized over extraction.
*   $\text{Threshold}_H$: A sustainability stock level (defined as $0.75 \times \text{capacity}$) above which the pool can support high consumption.

**Decision Rules:**

1.  **Initial Round ($t=1$):**
    Always play **Cooperate (C)**. This establishes a baseline for cooperation and preserves the stock for subsequent growth, ensuring the pool does not collapse immediately.

2.  **Subsequent Rounds ($1 < t < r$):**
    *   **If $S_t < \text{Threshold}_L$:** Play **Cooperate (C)**. When the pool is critically low, defecting guarantees long-term collapse, which terminates future potential gains.
    *   **If $S_t > \text{Threshold}_H$:** Play **Defect (D)**. The stock is high enough that the growth function will likely replenish it even if other players are moderate in their consumption. This maximizes short-term gain.
    *   **If $\text{Threshold}_L \le S_t \le \text{Threshold}_H$:**
        *   If the average number of defectors in the previous 2 rounds was $< (n/2)$, play **Cooperate (C)** to maintain stability.
        *   If the average number of defectors in the previous 2 rounds was $\ge (n/2)$, play **Defect (D)**. This is an opportunistic pivot; if the population is already aggressive, it is suboptimal to bear the cost of cooperation alone.

3.  **Final Round ($t = r$):**
    Always play **Defect (D)** regardless of the current stock level. There is no future round to preserve the stock for, so the entire remaining stock is optimally extracted to maximize total payoff.

**Pseudocode:**

```python
def decide_action(round, total_rounds, current_stock, history):
    if round == total_rounds:
        return D
    
    if round == 1:
        return C
        
    if current_stock < (0.25 * capacity):
        return C
        
    if current_stock > (0.75 * capacity):
        return D
        
    # Analyze recent history (last 2 rounds)
    recent_defect_count = sum(history.defect_counts[-2:]) / 2
    
    if recent_defect_count < (n / 2):
        return C
    else:
        return D
```
'''

description_OPPORTUNISTIC_20 = '''
1. **Initial State (Round 1):** Play Cooperate (C). This establishes a baseline for cooperation and maximizes the probability of maintaining a high stock level for subsequent rounds.

2. **Ongoing Rounds (Round 2 to Round r-1):** Implement a Conditional Tit-for-Tat strategy based on the observed aggregate cooperation of the previous round.
   - Let $k$ be the number of opponents who played C in the previous round.
   - Let $N = n - 1$ (the number of opponents).
   - Calculate the "Cooperation Threshold" ($T$). If $S_{t-1} \ge \text{capacity} \times 0.75$, set $T = N/2$. If $S_{t-1} < \text{capacity} \times 0.75$, set $T = N$.
   - If $k \ge T$, play C.
   - If $k < T$, play D.

3. **Defection Logic (Opportunistic Shift):**
   - If the current stock $S$ falls below $10\%$ of capacity, immediately play C regardless of previous history to prevent total stock depletion (system collapse).
   - If the total number of rounds $r$ is unknown or large, maintain the Conditional Tit-for-Tat logic. If the total number of rounds $r$ is known, transition to a "Greedy Exit" in the final 2 rounds.

4. **Terminal Phase (Final 2 Rounds):** 
   - In the penultimate round (Round $r-1$), if the current stock $S > \text{capacity} \times 0.5$, play D. Otherwise, continue the Conditional Tit-for-Tat logic.
   - In the final round (Round $r$), play D regardless of the state or history.

5. **Summary Pseudocode:**

```python
def get_action(round_number, current_stock, last_round_cooperators, n, r, capacity):
    # Terminal Phase
    if round_number == r:
        return 'D'
    if round_number == r - 1 and current_stock > capacity * 0.5:
        return 'D'
        
    # Crisis Prevention
    if current_stock < (capacity * 0.1):
        return 'C'
        
    # Round 1
    if round_number == 1:
        return 'C'
        
    # Adaptive Tit-for-Tat
    threshold = (n - 1) / 2 if current_stock >= (capacity * 0.75) else (n - 1)
    
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_21 = '''
### Strategy: Adaptive Threshold Tit-for-Tat (AT-TFT)

This strategy employs a dynamic threshold mechanism to balance long-term sustainability with immediate exploitation. It tracks the behavior of the pool (aggregate cooperation) and adjusts actions to maximize personal payout relative to the stock's regeneration capacity.

#### Core Logic
The strategy relies on a "Sustainability Quotient" (SQ) calculated each round.
*   **SQ** = (Number of Cooperators / Total Players)
*   **Target SQ** = The minimum cooperation rate required to maintain stock growth (approx. 0.5 when stock is at 50% capacity, scaling dynamically).

#### Decision Rules

**Round 1:**
*   Always choose **Cooperate (C)**. This signals a willingness to maintain the common pool and establishes a baseline for future reciprocity.

**Subsequent Rounds:**
1.  **Assess State:** If the current stock is ≤ (capacity / 4), choose **Defect (D)**. The resource is nearing collapse; prioritize immediate extraction before depletion.
2.  **Assess Opponent Behavior (Reciprocity):** Calculate the previous round's cooperation rate (C_prev).
    *   If C_prev > 0.6: Choose **Cooperate (C)**. The group is effectively maintaining the pool; sustain the positive equilibrium.
    *   If C_prev ≤ 0.6: Choose **Defect (D)**. The group is over-consuming or failing to coordinate; extract maximum value to compensate for the anticipated decline of the resource.
3.  **Last Round Exception:** Regardless of previous history or stock levels, always choose **Defect (D)**. With no future rounds, there is no value in preserving the stock.

#### Pseudocode

```python
def decide_action(round_number, total_rounds, stock, capacity, num_players, prev_cooperators):
    # Rule 0: Endgame Defection
    if round_number == total_rounds:
        return "D"
    
    # Rule 1: Collapse Imminent
    if stock <= (capacity / 4):
        return "D"
        
    # Rule 2: First Round Cooperation
    if round_number == 1:
        return "C"
        
    # Rule 3: Reciprocity Threshold
    # Calculate cooperation percentage of population
    cooperation_rate = prev_cooperators / num_players
    
    if cooperation_rate > 0.6:
        return "C"
    else:
        return "D"
```

#### Opportunistic Edge Case Handling
*   **High Stock (> 90% capacity):** The strategy defaults to **Cooperate** provided the previous cooperation rate was at least 0.4. This allows for a slightly lower threshold for cooperation when the resource is abundant, permitting opportunistic growth of the stock pool.
*   **Sudden Drop:** If the stock drops by more than 40% in a single round, immediately switch to **Defect** for the next round, regardless of opponent cooperation, to hedge against an impending collapse.
'''

description_OPPORTUNISTIC_22 = '''
This strategy employs a Conditional Reciprocity model based on stock sustainability thresholds. It tracks a running "Trust Index" (T) for the population, initialized at 0.5.

**Decision Rules**

In any given round with stock $S$, number of players $n$, and current round $t$ of total $r$:

1. **Calculate Sustainability Threshold**: Determine the critical stock level $S_{crit}$ below which the resource cannot replenish to full capacity in the next round. If total consumption in the current round exceeds $0.5 \times S$, the stock is likely to crash.

2. **The Opportunistic Threshold (OT)**:
   - If $t = r$: Always play D.
   - If $S < (capacity / n)$: Always play D (resource is already collapsing, extract remaining value).
   - If $t < r$: 
     - If $T \ge 0.5$ and $S \ge S_{crit}$: Play C.
     - If $T < 0.5$ or $S < S_{crit}$: Play D.

3. **Update Trust Index (T)**:
   After each round, observe the number of cooperators ($C_{obs}$).
   - Let $k = C_{obs}$ be the number of players who played C in the previous round (including self if I played C).
   - If I played C: $k_{others} = k - 1$.
   - If I played D: $k_{others} = k$.
   - Update $T$ using a decaying average: $T_{new} = (0.7 \times T_{old}) + (0.3 \times (k_{others} / (n-1)))$.

**Logic Flow (Pseudocode)**

```python
# Initial State
T = 0.5

def get_action(S, t, r, n):
    # Terminal condition
    if t == r:
        return D
    
    # Crisis condition
    if S < (capacity / n):
        return D

    # Cooperation condition
    # S_crit is the level where consumption > regeneration potential
    # Based on the dynamics, max growth is when S_remaining = capacity / 2
    # To maximize longevity, we target keeping S near capacity / 2
    S_crit = capacity / 2
    
    if T >= 0.5 and S >= S_crit:
        return C
    else:
        return D

def update_trust(my_action, num_cooperators, n):
    others_who_cooperated = num_cooperators - (1 if my_action == C else 0)
    cooperation_rate = others_who_cooperated / (n - 1)
    T = (0.7 * T) + (0.3 * cooperation_rate)
```

**Edge Case Handling**

- **First Round ($t=1$)**: Treat $T=0.5$. The strategy defaults to C unless the starting capacity itself is below $S_{crit}$ (unlikely given $capacity \ge 2n$).
- **Collapse ($S \to 0$)**: If the stock drops below the level where $C$ is mathematically non-viable to sustain future growth, the strategy immediately switches to D to harvest the remaining utility before total exhaustion, regardless of previous trust.
- **Last Round ($t=r$)**: Pure defection to maximize final payoff, as there is no future utility to protect.
'''

description_OPPORTUNISTIC_23 = '''
For each round $t$, let $S_t$ be the current stock, and let $C_{t-1}$ be the count of cooperators in the previous round. Define a "sustainable threshold" $T = \text{capacity} / 2$.

**Decision Rules:**

1. **Initial Round ($t=1$):** Play **Cooperate (C)**. Establish a baseline for collective sustainability.

2. **Subsequent Rounds ($t > 1$):**
   - If $S_t > T$:
     - If the number of cooperators in $t-1$ was $\geq n/2$, play **Cooperate (C)**.
     - If the number of cooperators in $t-1$ was $< n/2$, play **Defect (D)**. Capitalize on the resource while it remains above the recovery threshold, recognizing that collective restraint is failing.
   - If $S_t \leq T$:
     - Play **Defect (D)**. Prioritize immediate extraction because the resource is nearing collapse or has been exhausted by others, rendering long-term conservation ineffective.

3. **Terminal Phase ($t = r$):**
   - Play **Defect (D)** regardless of the current stock level. Maximize final payoff before the game terminates.

**Pseudocode:**

```python
def decide_action(round, total_rounds, current_stock, prev_cooperators_count, n, capacity):
    if round == total_rounds:
        return "D"
    
    threshold = capacity / 2
    
    if current_stock > threshold:
        if prev_cooperators_count >= (n / 2):
            return "C"
        else:
            return "D"
    else:
        return "D"
```

**Edge Case Handling:**

- **Stock Depletion ($S_t \approx 0$):** If $S_t$ is approaching zero, the logic defaults to Defect. This acknowledges that in a near-empty pool, waiting for regrowth is futile if opponents are also extracting; capturing the remaining fraction is the only way to secure any payoff.
- **Ambiguous Cooperation:** In scenarios where $n$ is odd and the count of cooperators is exactly $\lfloor n/2 \rfloor$, the decision rule treats this as a failure to meet the majority threshold, triggering a transition to Defect.
'''

description_OPPORTUNISTIC_24 = '''
For any given round $t$:

**Initialization**
In round 1, play C.

**Decision Logic**
Maintain a "Trust Score" $T$, initialized at 0. After each round $t > 1$, update $T$ based on the aggregate behavior of opponents in the previous round ($t-1$):
- If all opponents played C: Increment $T$ by 1.
- If some opponents played C: $T$ remains unchanged.
- If no opponents played C: Decrement $T$ by 1.

Define a dynamic cooperation threshold, $K$, as a function of the remaining rounds ($r - t$):
- If $(r - t) < 3$: Set $K = \infty$ (Force D).
- Otherwise: Set $K = 2$.

**Action Selection**
Calculate action $A_t$ based on $T$ and the current stock level $S$:
1. **Endgame Trigger:** If $r - t < 3$, play D.
2. **Depletion Safety Check:** If $S < (\text{capacity} / n)$, play C to avoid total stock collapse, regardless of $T$.
3. **Opportunistic Assessment:** If $T \ge K$, play C.
4. **Default:** Play D.

**Pseudocode**
```python
if round == last_3_rounds:
    return D
if current_stock < (capacity / n):
    return C
if trust_score >= cooperation_threshold:
    return C
return D
```

**Edge Case Handling**
- If the stock is at 0: Play C (attempting to allow potential future growth if the system permits, though effectively neutral).
- If the stock is extremely high (near capacity): Prioritize D, as the resource buffer is sufficient to withstand exploitation without immediate collapse.
- If $T$ drops below 0: Reset $T$ to 0 to prevent excessive "grudge-holding" that prevents future cooperation if opponents shift behavior.
'''

description_OPPORTUNISTIC_25 = '''
The strategy employs a conditional cooperation model anchored by a threshold-based trigger mechanism. The core objective is to maximize cumulative payoff by maintaining the common pool stock at approximately 50% of capacity—the level that maximizes regeneration growth—while capturing surplus yield when opponents are collectively cooperating.

**Decision Logic:**

1.  **Phase Initialization (Round 1):**
    Play C. This initiates a "tit-for-tat" cooperation signal, allowing for the observation of aggregate opponent behavior without prematurely exhausting the pool.

2.  **Conditional Rule (Rounds 2 to r-1):**
    Let `C_opp` be the number of opponents who played C in the previous round.
    *   If `C_opp` ≥ (`n` - 1), continue playing C. The cooperative surplus is high enough to sustain the pool; continue to preserve the resource.
    *   If `C_opp` < (`n` - 1), calculate the `next_stock` based on the observed consumption in the previous round. 
        *   If `next_stock` < (0.25 * `capacity`), play D. The pool is collapsing; extract remaining value before exhaustion.
        *   If `next_stock` ≥ (0.25 * `capacity`), play C. The stock is sufficient to absorb the defection without immediate collapse; maintain cooperation to encourage potential recovery.

3.  **End-Game Heuristic (Final Round):**
    Regardless of history, play D. As there are no future rounds to sustain, maximizing the immediate payoff from the existing `stock` is the strictly dominant strategy.

**Pseudocode:**

```python
def get_action(round, current_stock, prev_opp_C, r, n):
    if round == r:
        return D
    
    if round == 1:
        return C
    
    # Calculate state if current cooperation trend continues
    # prev_opp_C: number of opponents playing C in round-1
    # Assume I played C last round:
    # consumption_i = current_stock / (2n) if playing C else current_stock / n
    
    # Threshold for defecting: If opponents are not cooperating, 
    # check if pool can sustain the cooperative equilibrium.
    if prev_opp_C < (n - 1):
        if current_stock < (0.25 * capacity):
            return D
        else:
            return C
    else:
        return C
```

**Edge Case Handling:**
*   **Rapid Depletion:** If `current_stock` drops below 10% of `capacity` at any point prior to the final round, switch to D for all remaining rounds, as the regeneration mechanics will likely fail to recover the stock sufficiently to justify cooperative consumption.
*   **Full Defection:** If all opponents play D for two consecutive rounds, switch to D, as the game has devolved into a prisoner's dilemma where unilateral cooperation is strictly loss-making without benefit to future regeneration.
'''

description_OPPORTUNISTIC_26 = '''
Define a threshold variable, *target_stock*, calculated as $\frac{\text{capacity}}{2} + \epsilon$ (where $\epsilon$ is a buffer determined by $\frac{\text{capacity}}{2n}$), representing the minimum viable stock required to sustain future growth. Maintain a count of rounds remaining, $T_r$.

**Decision Rule:**
In every round $t$, calculate the *expected_stock_next_round* assuming all opponents play the same strategy as they did in the previous round ($t-1$).

1.  **If $t = 1$:** Play **Cooperate (C)** to establish a sustainable baseline.
2.  **If $t = r$ (Last Round):** Play **Defect (D)**. Always exhaust the resource in the final round to maximize immediate payoff, as there is no future utility to protect.
3.  **If $t < r$:**
    *   **Observation:** Check the aggregate consumption from round $t-1$. Calculate the *actual_stock* after the previous round.
    *   **Condition A (Sustainability Check):** If *actual_stock* < $\frac{\text{capacity}}{2n}$, play **Defect (D)**. The resource is collapsing; capture remaining value before depletion.
    *   **Condition B (Trigger Strategy):** If the aggregate number of defectors in the previous round $> \frac{n}{2}$, play **Defect (D)**. Retaliate against non-cooperative groups to prevent unilateral exploitation.
    *   **Condition C (Optimistic Expansion):** If *actual_stock* $\geq$ *target_stock* AND the aggregate number of defectors in the previous round $\leq 1$, play **Cooperate (C)** to keep the resource at maximum capacity.
    *   **Condition D (Default):** If none of the above, match the previous behavior of the majority. If the number of $C$ players $\geq$ number of $D$ players, play **Cooperate (C)**. Otherwise, play **Defect (D)**.

**Edge Cases:**
*   **System Shock:** If *stock* drops below $\frac{capacity}{n}$ at any point, switch to **Defect (D)** for all subsequent rounds, regardless of opponent behavior. The resource is no longer recoverable in a way that justifies self-restriction.
*   **Initialization:** For $t=2$, treat the previous round's opponent behavior as if 0 players defected.
'''

description_OPPORTUNISTIC_27 = '''
Maintain a target stock level to maximize long-term yield. The strategy operates on a Tit-for-Tat variant with a conditional thresholding mechanism based on the observed ratio of cooperators.

**Decision Rules:**

Let $C_{obs}$ be the number of opponents who cooperated in the previous round ($C_{obs} \in \{0, 1, ..., n-1\}$).
Let $S_{current}$ be the current stock level.
Let $S_{threshold}$ be the replenishment target, set to $0.5 \times \text{capacity}$.

1. **Initial Round (Round 1):** Play $C$. The goal is to establish a cooperative baseline.

2. **Subsequent Rounds (Round 2 to $r-1$):**
   - If $S_{current} < S_{threshold}$, play $C$ regardless of previous history to prioritize resource recovery.
   - If $S_{current} \ge S_{threshold}$:
     - If $C_{obs} = n-1$ (full cooperation), play $C$.
     - If $C_{obs} < n-1$, play $D$. This is the opportunistic exploitation phase: when the group is fragmented or defecting, extract maximum value to compensate for the anticipated loss of future growth.

3. **Final Round (Round $r$):** Play $D$. Since there is no future utility to the stock, extract the maximum possible value before the game terminates.

**Edge Cases and Logic:**

*   **Stock Depletion:** If $S_{current}$ is so low that even playing $C$ yields negligible returns, maintain $C$ as long as $S_{current} > 0$ to prevent total system collapse, as $D$ forces a stock of 0, ending all future payoff potential for everyone.
*   **Rapid Stock Recovery:** If $S_{current} > 0.8 \times \text{capacity}$, play $D$ even if $C_{obs} = n-1$. At high stock levels, the growth rate approaches zero, and the resource is underutilized; opportunistic extraction prevents waste.
*   **Recovery Failure:** If $C_{obs} = 0$ for two consecutive rounds, switch strategy to $D$ for all remaining rounds, as the game has entered a permanent defection cycle.

**Pseudocode Logic:**

```python
if round == r:
    return D

if stock < (0.2 * capacity): # Critical threshold
    return C

if stock > (0.8 * capacity): # Over-saturation
    return D

if round > 1:
    if history.count_defectors_in_last_round > 0:
        return D # Opportunistic exploitation
    else:
        return C # Reward cooperation

return C # Default for round 1
```
'''

description_OPPORTUNISTIC_28 = '''
### Strategic Framework: Sustainable Extraction (SE)

The strategy operates on a Tit-for-Tat foundation with conditional expansion during the final rounds. The core objective is to maintain the stock at or near `capacity` to ensure maximum long-term yield while exploiting defections only when the stock is sufficiently high or the game is ending.

#### Decision Rules

**1. Initialization (Round 1):**
*   Play **C**. This signals willingness to cooperate and tests the average cooperativeness of the population.

**2. Standard Rounds (Round 2 to r-1):**
*   **Observe:** Determine `cooperation_rate` = (Total Cooperators in Round t-1) / n.
*   **Adjustment Logic:**
    *   If `cooperation_rate` = 1.0 (All players cooperated): Play **C**.
    *   If `stock` < 0.25 * `capacity`: Play **C** regardless of opponent behavior to allow regeneration.
    *   If `cooperation_rate` < 1.0: Play **D**.
        *   *Exception:* If `stock` ≥ 0.75 * `capacity` AND `cooperation_rate` > 0.5, play **C**. This maintains the resource while acknowledging high, albeit imperfect, cooperation.

**3. Final Round (Round r):**
*   Play **D**. 

#### Pseudocode Representation

```python
def get_action(round, stock, capacity, n, history):
    if round == r:
        return D
    
    if round == 1:
        return C
        
    last_round_coops = count_cooperators(history[round-1])
    coop_rate = last_round_coops / n
    
    # Conservation Phase
    if stock < 0.25 * capacity:
        return C
    
    # Steady State Phase
    if coop_rate == 1.0:
        return C
        
    # Opportunistic Phase
    if stock >= 0.75 * capacity and coop_rate > 0.5:
        return C
    
    return D
```

#### Handling Edge Cases

*   **Sudden Stock Collapse:** If `stock` falls below 0.1 * `capacity`, the strategy overrides all other conditions to play **C** until the `stock` recovers to at least 0.5 * `capacity`, treating stock regeneration as the priority over population coordination.
*   **Inconsistent Opponents:** If the `cooperation_rate` fluctuates between 0 and 1 repeatedly, the strategy defaults to **D** to extract value before the resource is depleted by others, but reverts to **C** immediately if the stock drops below the threshold defined in the Conservation Phase.
*   **High Cooperation, Low Stock:** In rare scenarios where the group continues to cooperate (C) despite the stock dropping (e.g., due to previous aggregate D), the strategy follows the Conservation rule to force recovery, prioritizing long-term yield over short-term gain.
'''

description_OPPORTUNISTIC_29 = '''
Maintain a history of rounds $t=1 \dots r$ and the number of cooperative actions observed in the previous round $C_{prev}$. Calculate the "Critical Stock Threshold" ($S_{crit}$) as $\frac{capacity}{2}$, below which stock regeneration is insufficient to support full cooperation in the long run.

**Decision Rules:**

1.  **Initialization (Round 1):** Play Cooperate (C).

2.  **Standard Rounds (Round 2 to $r-1$):**
    *   Calculate the deviation from collective cooperation. If $C_{prev} = n$ (all cooperated), play C.
    *   If $C_{prev} < n$, calculate the "Exploitation Factor" $E = \frac{n - C_{prev}}{n}$.
    *   If current stock $S < S_{crit}$, play Defect (D) immediately to maximize immediate payoff before the pool collapses.
    *   If current stock $S \geq S_{crit}$, play C with probability $P(C) = 1 - E$. If the random roll results in Defect, switch to Defect for the current round.

3.  **Terminal Round ($t = r$):**
    *   Regardless of previous history or current stock, play Defect (D).

**Pseudocode:**

```python
def get_action(current_round, stock, n, capacity, history):
    if current_round == total_rounds:
        return D
    
    if current_round == 1:
        return C
    
    cooperators_last_round = history[-1].cooperators_count
    
    # Check if stock is critically low
    if stock < (capacity / 2.0):
        return D
        
    # Adaptive responsiveness: align probability of cooperation 
    # with the percentage of cooperators in the previous round
    cooperation_probability = cooperators_last_round / n
    
    if random.random() < cooperation_probability:
        return C
    else:
        return D
```

**Edge Case Handling:**
*   **Total Depletion:** If $S \approx 0$, force Defect (D) regardless of other rules to extract any remaining marginal value.
*   **Perfect Cooperation:** If $C_{prev} = n$, maintain Cooperation (C) unless the final round is reached, to maximize long-term resource sustainability.
*   **Steady Collapse:** If the stock $S$ declines by more than 20% in a single round despite the cooperative strategy, transition to permanent Defection for the remainder of the game to capture value before exhaustion.
'''

description_OPPORTUNISTIC_30 = '''
**Initialization Phase**
For the first round, play C (Cooperate). Maintain a history buffer tracking the number of Cooperators ($c_t$) for every round $t$.

**Strategy Logic**
For any round $t$ where $t < r$, calculate the current "Cooperation Index" ($\kappa$), defined as the weighted moving average of the percentage of opponents cooperating over the last $k$ rounds (where $k = \min(t, 3)$):
$\kappa = \frac{1}{k} \sum_{j=t-k}^{t-1} \left( \frac{c_j}{n-1} \right)$

1.  **Sustainability Threshold:** If current stock $S < \frac{capacity}{2}$, switch to C regardless of previous history to prevent stock collapse, unless the last round showed a total system defection ($c_{t-1} = 0$). If $c_{t-1} = 0$ and $S < \frac{capacity}{4}$, play D (Defect) to capture remaining utility before depletion.
2.  **Opportunistic Exploitation:** If $\kappa < 0.25$ (indicating low group cooperation), play D.
3.  **Tit-for-Tat Alignment:** If $\kappa \geq 0.25$, play C.
4.  **Reward/Punishment:** If $c_{t-1} > 0.5 \times (n-1)$, and the stock $S > 0.5 \times capacity$, play C to maintain the resource level. If $c_{t-1} < 0.5 \times (n-1)$, play D to maximize share before the stock depletes due to others' selfishness.

**Terminal Phase**
For the final round $t=r$:
1. If $S > \frac{capacity}{n}$, play D to capture the maximum remaining resource.
2. If $S \leq \frac{capacity}{n}$, play C.

**Pseudocode Implementation**
```
if round == r:
    if stock > capacity / n: return D
    else: return C

if round == 1:
    return C

k = min(round - 1, 3)
coop_rate = mean(history[round-k : round-1]) / (n - 1)

if stock < capacity / 2:
    if last_round_cooperators == 0 and stock < capacity / 4:
        return D
    return C

if coop_rate < 0.25:
    return D

if last_round_cooperators > (n - 1) / 2 and stock > capacity / 2:
    return C

if last_round_cooperators < (n - 1) / 2:
    return D

return C
```
'''

description_OPPORTUNISTIC_31 = '''
The strategy, titled "Adaptive Sustainability with Defection Trigger," operates on the principle of conditional cooperation while aggressively exploiting the resource in the final phase. It maintains the common pool at its optimal regeneration level ($0.5 \times \text{capacity}$) by matching the aggregate cooperation of the opponents.

**Variables and Thresholds:**
*   **$T_{round}$:** The current round number.
*   **$C_{prev}$:** Number of opponents who played 'Cooperate' in the previous round.
*   **$S_{curr}$:** Current stock level.
*   **$S_{opt}$:** Optimal growth threshold, defined as $0.5 \times \text{capacity}$.

**Decision Logic:**

1.  **Initial Phase ($T_{round} = 1$):**
    Play **Cooperate**. Establishing a cooperative baseline maximizes the initial stock regeneration potential.

2.  **Sustainability Phase ($1 < T_{round} < r$):**
    Evaluate the stock and opponent behavior to determine the action for the current round:
    *   **Condition A (Stock Scarcity):** If $S_{curr} < 0.2 \times \text{capacity}$, play **Cooperate**. Prioritize stock replenishment.
    *   **Condition B (Trigger):** If $C_{prev} = 0$, play **Defect**. If no opponents cooperated in the previous round, punish the group to maximize immediate payoff, as cooperation is already absent.
    *   **Condition C (Equilibrium):** If $S_{curr} \ge 0.2 \times \text{capacity}$ and $C_{prev} > 0$, play **Cooperate**. Maintain the stock as long as there is evidence of mutual cooperation.

3.  **Terminal Phase ($T_{round} = r$):**
    Play **Defect**. In the final round, there are no future consequences or regeneration requirements. The utility of future stock is zero; maximize the final payoff.

**Pseudocode:**

```python
def choose_action(T_round, r, S_curr, C_prev, capacity):
    if T_round == r:
        return 'Defect'
    
    if T_round == 1:
        return 'Cooperate'
    
    # Sustainability logic for intermediate rounds
    if S_curr < (0.2 * capacity):
        return 'Cooperate'
    
    if C_prev == 0:
        return 'Defect'
        
    return 'Cooperate'
```
'''

description_OPPORTUNISTIC_32 = '''
The strategy operates as a Tit-for-Tat variant with a threshold-based decay mechanism, designed to exploit cooperation when abundant while preserving the resource when threatened.

**Core Strategy: Conditional Sustainability**

Define `observed_cooperators` as the number of opponents who played Cooperate (C) in the previous round.
Define `cooperation_threshold` as `n - 1`.
Define `is_last_round` as `round == r`.

**Decision Logic:**

1.  **Round 1:**
    Always play **C**. Establish a cooperative baseline to maximize the growth potential of the common pool while the stock is at maximum capacity.

2.  **Rounds 2 to r - 1:**
    If `stock` < (`capacity` / 4), switch to **D** to extract remaining value before depletion, regardless of history.

    If `stock` ≥ (`capacity` / 4):
    - If `observed_cooperators` == `cooperation_threshold`: Play **C**. Maintain the sustainable equilibrium.
    - If `observed_cooperators` < `cooperation_threshold`: Play **D**. Punish defection to force stock recovery or extract maximum yield while others deplete the pool.

3.  **Last Round (r):**
    Always play **D**. Since there is no future stock growth benefit to consider, maximize individual payoff before the game terminates.

**Pseudocode:**

```
if round == r:
    return D

if stock < (capacity / 4):
    return D

if round == 1:
    return C

if observed_cooperators == (n - 1):
    return C
else:
    return D
```

**Edge Case Handling:**

*   **Stock Collapse:** If the stock falls to 0, no meaningful action can be taken as future payoffs are zero; however, the logic defaults to **D** via the `stock < (capacity / 4)` condition, ensuring any fractional residual value is claimed.
*   **Initial Defectors:** If opponents play **D** in Round 1, the `observed_cooperators < (n - 1)` condition will trigger **D** in Round 2, effectively switching to a non-cooperative stance for the remainder of the game unless the stock level reaches a point of absolute scarcity.
*   **Recovery:** If the stock recovers due to aggregate behavior, the strategy resumes **C** provided the `observed_cooperators` count returns to `n - 1`.
'''

description_INDIVIDUALISTIC_5 = '''
**Initialization:**
Maintain a `reputation_score` variable, initialized to 1.0 (representing initial trust). At the end of each round, update `reputation_score` based on the observed collective behavior of the opponents:
- Let $k$ be the number of cooperators observed in the previous round.
- Calculate observed cooperation fraction: $f = k / (n - 1)$.
- If $n=1$ (not applicable per parameters) or no data is available (Round 1), set $f = 1$.
- Update `reputation_score` using an exponentially weighted moving average: `reputation_score` = $\alpha \times f + (1 - \alpha) \times \text{reputation\_score}$, where $\alpha = 0.2$.

**Decision Rule:**
In any round $t$ where $t < r$:
- If $S < (\text{capacity} / n)$, force Defect (D) to maximize immediate gain before collapse.
- If $S \geq (\text{capacity} / n)$, calculate the probability of cooperating: $P(C) = \min(1.0, \max(0.0, \text{reputation\_score}))$.
- Generate a random number $x \in [0, 1]$. If $x < P(C)$, play Cooperate (C); otherwise, play Defect (D).

**Terminal Round Strategy:**
In the final round ($t = r$):
- Play Defect (D) regardless of state or reputation, as there is no future utility to incentivize continued cooperation.

**Edge Cases:**
- If $S = 0$: Play Defect (D) as payoff is zero regardless of action.
- If the stock growth potential is high but $S$ is significantly depleted ($S < \text{capacity} \times 0.2$): Ignore `reputation_score` and play Cooperate (C) to stimulate recovery, provided the previous round did not show total defection ($k=0$); if $k=0$, switch to Defect (D) for the remainder of the game.
'''

description_INDIVIDUALISTIC_6 = '''
Maintain a trigger-based, threshold-dependent strategy calibrated to the sustainability of the resource stock. Define a "sustainable consumption" model where the goal is to keep the stock at the level that maximizes long-term replenishment (S_t ≈ capacity/2), as growth is maximized when S_remaining = capacity/2.

**Variables:**
- Let $k$ be the number of players observed to have played $C$ in the previous round.
- Let $S_t$ be the stock at the start of round $t$.
- Let $r_{rem}$ be the number of remaining rounds.

**Decision Rules:**

1.  **First Round (t=1):** Always play **Cooperate (C)**. This tests for cooperative behavior and avoids immediate resource depletion.

2.  **Subsequent Rounds (t > 1):**
    *   **If $S_t < (capacity/2) \times 0.2$ (Critical Depletion):** Play **Cooperate (C)** regardless of previous opponent actions. The priority is resource recovery to prevent total collapse.
    *   **If $S_t \approx capacity$ (High Stock):** 
        *   If the previous round's outcome resulted in $S_{t+1} \geq S_t$ (stable or growing), play **Cooperate (C)**.
        *   If the previous round's outcome resulted in a net decline in stock, switch to **Defect (D)** for one round to rebalance or signal, then revert to C.
    *   **Trigger-Condition Strategy:** 
        *   If $k$ (number of cooperators in $t-1$) is $\geq n-1$, continue playing **Cooperate (C)**.
        *   If $k < n-1$ (indicating defectors exist), play **Defect (D)** if $r_{rem} > 1$.
        *   If playing **Defect (D)**, switch back to **Cooperate (C)** in the next round only if the stock $S_t$ is above the critical depletion threshold (defined above).

3.  **Last Round (t = r):**
    *   If $S_r \leq 0$, play **Cooperate (C)** (action is irrelevant).
    *   If $S_r > 0$, play **Defect (D)**. Since no future rounds exist to reap the benefits of conservation, extract maximum value.

**Pseudocode:**

```python
def decide_action(S_t, k_prev, t, r, n, capacity):
    # End-game condition
    if t == r:
        return 'D' if S_t > 0 else 'C'
    
    # Critical recovery condition
    if S_t < (capacity / 2) * 0.2:
        return 'C'
    
    # Conditional reciprocity
    if t > 1:
        if k_prev >= (n - 1):
            return 'C'
        else:
            return 'D'
            
    # Default initial state
    return 'C'
```
'''

description_INDIVIDUALISTIC_7 = '''
For each round $t$ and current stock $S_t$:

**Strategy Logic:**
Adopt a conditional cooperation model based on the "Tit-for-Tat" principle, modified by a resource-availability threshold to protect the long-term stock levels.

1.  **Phase Initialization (Round 1):**
    Play **Cooperate (C)**. This establishes a baseline for cooperation while testing opponent behavior without immediate depletion.

2.  **State-Dependent Thresholding:**
    Before making a decision in rounds $t > 1$, calculate the "Sustainability Index" ($\Phi$) based on the observed behavior of opponents in the previous round ($t-1$):
    *   Let $k$ be the number of opponents who cooperated in round $t-1$.
    *   Let $N_{total} = n-1$ (total opponents).
    *   Calculate $\Phi = k / N_{total}$.

    *   **Rule A (Stock Preservation):** If $S_t < (capacity / 2)$, ignore opponent history and play **Cooperate (C)**. When the stock is low, defection leads to collapse, which eliminates future payoff potential.
    *   **Rule B (Adaptive Response):** If $S_t \ge (capacity / 2)$, apply the following logic:
        *   If $\Phi \ge 0.75$, play **Cooperate (C)**. (High cooperation supports the shared pool).
        *   If $\Phi < 0.75$, play **Defect (D)**. (Low cooperation indicates that others are extracting for short-term gain; matching this prevents being exploited).

3.  **End-Game Heuristic (Rounds $t = r$):**
    In the final round, the incentive to preserve stock vanishes. Regardless of previous history:
    *   If $S_r > (capacity / n)$, play **Defect (D)**.
    *   If $S_r \le (capacity / n)$, play **Cooperate (C)**. 
    *(Rationale: If the remaining stock is so low that a single Defection empties the pool, Defecting maximizes the final payout before terminal collapse. If the pool is small enough that Defection yields minimal returns anyway, cooperate to capture the remaining resources safely.)*

**Pseudocode:**

```python
def get_action(round, total_rounds, n, capacity, current_stock, prev_opp_coop_count):
    # End-game scenario
    if round == total_rounds:
        if current_stock > (capacity / n):
            return D
        else:
            return C
            
    # Resource preservation trigger
    if current_stock < (capacity / 2):
        return C
        
    # Standard Adaptive Logic
    opponents_count = n - 1
    phi = prev_opp_coop_count / opponents_count
    
    if phi >= 0.75:
        return C
    else:
        return D
```
'''

description_INDIVIDUALISTIC_8 = '''
**Core Principle**
Maintain the "Golden Equilibrium": Maximize long-term utility by preserving the common pool near its growth-optimal level while defecting only when the stock is doomed or when the game is nearing its conclusion.

**Decision Rules**

1.  **Initial Phase (Rounds 1 to *r*-1):**
    *   Calculate the "Stability Threshold": If the number of defectors in the previous round exceeds $n/2$, switch to Defect (D) to capture remaining value before the stock collapses.
    *   Otherwise, observe the current stock level ($S$):
        *   If $S < \text{capacity} \times 0.25$: Defect (D). At very low levels, preservation is futile because the growth rate is negligible. Extract remaining value.
        *   If $S \geq \text{capacity} \times 0.25$: Cooperate (C). Maintain the stock to ensure high-yield payoffs in subsequent rounds.

2.  **Endgame Phase (Round *r*):**
    *   Regardless of previous cooperation history or stock levels, play Defect (D). In the final round, there is no future benefit to resource preservation; immediate consumption maximizes the final payoff.

**Pseudocode**

```python
def get_action(round_num, total_rounds, n, capacity, current_stock, history):
    # Rule 1: Always defect in the final round
    if round_num == total_rounds:
        return "D"
    
    # Rule 2: Check for systemic collapse
    # If the previous round saw > 50% defection, we are in a crash trajectory.
    if round_num > 1:
        prev_round = history[-1]
        if prev_round.num_defectors > (n / 2):
            return "D"
            
    # Rule 3: Preservation Logic
    # If the stock is too low to sustain future growth, take the remainder.
    if current_stock < (capacity * 0.25):
        return "D"
    
    # Otherwise, protect the resource for future rounds
    return "C"
```

**Edge Case Handling**
*   **Round 1:** Default to Cooperate (C). This initiates the sustainable cycle.
*   **Near-Total Depletion:** If $S$ is near 0, the logic forces Defect (D) regardless of the round number, acknowledging that attempting to "save" a near-empty pool provides lower returns than capturing the minimal remaining stock.
*   **High Volatility:** If opponents fluctuate between strategies, the "Stability Threshold" (Rule 2) serves as a circuit breaker, pivoting from cooperation to extraction the moment the environment becomes non-viable.
'''

description_INDIVIDUALISTIC_9 = '''
Strategy: Tit-for-Tat with Sustainability Threshold (TFTS)

The strategy relies on a "trigger-and-recover" mechanism that prioritizes long-term resource viability while punishing mass defection.

1.  **Definitions:**
    *   *Cooperation Target ($k$)*: Define the target number of cooperators as $k = n$.
    *   *Observation*: In round $t-1$, let $C_{obs}$ be the number of cooperators observed.
    *   *State Check*: Let $S$ be the current stock. Define "Critical State" as $S < (capacity / 2)$.

2.  **Decision Rules:**

    *   **Round 1**: Always play **C** (Cooperate). This tests opponent cooperation levels without risking immediate collapse.
    *   **Rounds 2 to $r-1$**:
        *   If the previous round resulted in total consumption such that $S_{next} < (capacity / 4)$, play **D** (Defect). This serves as a "bailout" mechanism to extract value before the resource potentially collapses to zero.
        *   If the previous round was stable (growth $\geq$ 0), adopt a conditional response based on observed cooperation:
            *   If $C_{obs} \geq n - 1$: Play **C**. (Maintain the cooperative equilibrium).
            *   If $C_{obs} < n - 1$: Play **D**. (Punish the group for insufficient sustainability).
        *   Exception: If $S \geq 0.9 \times capacity$, prioritize **C** regardless of history to maximize long-term stock replenishment.

    *   **Final Round ($r$)**:
        *   If $S > (capacity / n)$: Play **D**.
        *   If $S \leq (capacity / n)$: Play **C**.
        *   *Rationale*: In the final round, there is no future incentive to preserve the stock. Extract the remaining value unless the stock is so low that defection yields negligible returns compared to the risk of total depletion.

3.  **Pseudocode**:

```python
def get_action(round, total_rounds, stock, capacity, n, prev_round_cooperators):
    # Final round extraction
    if round == total_rounds:
        if stock > (capacity / n):
            return "D"
        else:
            return "C"

    # Bailout logic
    # Calculate projected next stock based on previous round behavior
    # If the resource is trending toward collapse
    if stock < (capacity / 4):
        return "D"

    # Tit-for-Tat logic
    if round == 1:
        return "C"
    
    # Sustainability logic
    if stock >= (0.9 * capacity):
        return "C"
    
    # Reciprocal logic
    if prev_round_cooperators >= (n - 1):
        return "C"
    else:
        return "D"
```

4.  **Edge Cases**:
    *   **Sudden Collapse**: If $S$ drops below a threshold where consumption is effectively zero, the strategy defaults to **D** to extract the final residual value before exhaustion.
    *   **High-Cooperation Environments**: If all opponents play **C** consistently, the strategy locks into **C** indefinitely, ensuring the resource remains at maximum capacity ($capacity$), which maximizes the individual payoff $\pi_i = capacity / (2n)$ per round, ensuring sustainability.
'''

description_INDIVIDUALISTIC_10 = '''
Define `target_sustain_stock` as `capacity / 2`. Define `cooperation_threshold` as `n * 0.75` (rounded to nearest integer). Maintain a state variable `trust_score`, initialized to `0.5`, which adjusts based on observed aggregate cooperation.

**Decision Rules:**

1.  **Round 1:** Play **C**.
2.  **Subsequent Rounds:**
    *   Calculate `projected_stock` for the next round assuming all players repeat their previous round’s action distribution.
    *   If `current_stock` < `target_sustain_stock` * 0.5: Play **D** (maximize immediate gain while the resource is crashing).
    *   If `current_stock` ≥ `target_sustain_stock` * 0.5:
        *   If `count_cooperators` (from previous round) ≥ `cooperation_threshold`: Play **C**.
        *   If `count_cooperators` < `cooperation_threshold`: Play **D**.
3.  **Last Round (Round r):** Always play **D**.

**State Updates:**

*   After every round `t < r`, update `trust_score`:
    *   `trust_score` = `(trust_score * 0.7) + ((count_cooperators / n) * 0.3)`.
*   If `trust_score` drops below `0.25`: Switch to a "Grim Trigger" mode for the remainder of the game, playing **D** in every round until `r`.

**Edge Cases:**

*   **Low Stock:** If `current_stock` is less than `capacity / (2 * n)` (the minimum consumption required to sustain some growth), ignore `trust_score` and always play **D** to extract value before depletion renders the stock negligible.
*   **High Stock:** If `current_stock` is ≥ `0.9 * capacity`, increase `cooperation_threshold` to `n * 0.9` to aggressively exploit the abundance, effectively shifting to **D** unless almost everyone else is cooperating.
'''

description_INDIVIDUALISTIC_11 = '''
**Strategy: Tit-for-Tat Sustainability (TFTS)**

This strategy operates on a "conditional sustainability" framework, where the primary objective is to maintain the stock level at exactly `capacity / 2` (the point of maximum regeneration) while penalizing defection only when the collective behavior threatens long-term stock viability.

**Decision Rules:**

1.  **Phase 1: Establishing Equilibrium (Round 1)**
    *   Play **Cooperate (C)**. This tests if opponents will collectively support the resource base at the start.

2.  **Phase 2: Monitoring and Adjustment (Rounds 2 through r-1)**
    *   Calculate `Target_Stock = capacity / 2`.
    *   Calculate `Projected_Stock = min(capacity, (S_remaining + 2 * S_remaining * (1 - S_remaining / capacity)))`, where `S_remaining` is the stock remaining after the *previous* round.
    *   **Decision Logic:**
        *   **If `S_remaining` < `capacity / 4`**: Play **Defect (D)**. The resource is nearing collapse; prioritize short-term gain before the pool empties.
        *   **If `S_remaining` ≥ `capacity / 4` AND `Projected_Stock` > `Target_Stock`**: Play **Cooperate (C)**. The stock is regenerating sufficiently to allow for sustainable cooperation.
        *   **If `S_remaining` ≥ `capacity / 4` AND `Projected_Stock` ≤ `Target_Stock`**: Play **Defect (D)**. The group behavior is insufficient to maintain the resource; pivot to extraction to avoid subsidizing the consumption of others while the pool depletes.

3.  **Phase 3: Terminal Phase (Final Round)**
    *   Regardless of previous history or current stock level, play **Defect (D)**. Since no future rounds exist to reap the benefits of conservation, extract maximum value.

**Pseudocode Representation:**

```python
def get_action(round_number, total_rounds, S_previous, S_remaining, capacity):
    if round_number == total_rounds:
        return D
    
    if round_number == 1:
        return C
    
    # Calculate projected stock based on previous round's outcome
    growth = 2 * S_remaining * (1 - S_remaining / capacity)
    projected_stock = min(capacity, S_remaining + growth)
    
    # Critical threshold: If stock is dangerously low, extract immediately
    if S_remaining < (capacity / 4):
        return D
    
    # If the group's behavior successfully grows the stock above sustainable equilibrium, cooperate
    if projected_stock > (capacity / 2):
        return C
    else:
        return D
```

**Edge Case Handling:**
*   **Initial Round:** Always defaults to C to initiate potential cooperation.
*   **Depletion:** If the stock drops below 25% of capacity, the strategy abandons cooperation immediately to secure a share of the remaining resources before they vanish.
*   **Last Round:** Always defaults to D to capture residual value, as the "common pool" has no future utility.
'''

description_INDIVIDUALISTIC_12 = '''
The strategy employs a conditional "tit-for-tat with depletion adjustment" approach, designed to maintain long-term resource viability while punishing defection only to the extent that the stock level allows for sustainable harvesting.

**Strategy Logic**

1.  **Initialization (Round 1):**
    Always play **Cooperate (C)** to initiate cooperative norms and establish a baseline for potential cooperation.

2.  **General Decision Rule (Rounds $t=2$ to $r-1$):**
    *   **Cooperate ($C$)** if the average cooperation rate of opponents in the previous round was high (i.e., $\ge 75\%$ of other players cooperated) AND the current stock $S$ is above the "safety threshold" defined as $S > 0.5 \times \text{capacity}$.
    *   **Defect ($D$)** if the average cooperation rate of opponents in the previous round was low (i.e., $< 75\%$ of other players cooperated) OR if the current stock $S$ has fallen below the safety threshold ($S \le 0.5 \times \text{capacity}$).
    *   *Rationale:* If opponents defect, you must harvest more quickly to capture remaining resources before the stock collapses. If the stock is critically low, defecting is necessary to maximize immediate payoff before the pool reaches a non-renewable state.

3.  **Final Round ($t=r$):**
    Always play **Defect ($D$)**. There is no future value in maintaining the stock, so prioritize immediate consumption.

4.  **Stock-Awareness Modifier:**
    If at any point the stock $S$ falls below $0.1 \times \text{capacity}$, disregard all previous cooperation history and play **Defect ($D$)** for all remaining rounds, as the resource is approaching total depletion.

**Pseudocode Implementation**

```python
def get_action(round, stock, capacity, n, previous_opponents_cooperated):
    # Round r: Always maximize immediate return
    if round == r:
        return 'D'
    
    # Critical depletion threshold: Take what remains
    if stock < (0.1 * capacity):
        return 'D'
    
    # First round initialization
    if round == 1:
        return 'C'
    
    # Safety threshold check
    is_stock_safe = (stock > (0.5 * capacity))
    
    # Calculate cooperation rate of opponents
    # 'previous_opponents_cooperated' is the count of C from others in the last round
    opponents_cooperation_rate = previous_opponents_cooperated / (n - 1)
    
    # Adaptive decision
    if is_stock_safe and (opponents_cooperation_rate >= 0.75):
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_13 = '''
### Adaptive Threshold Strategy

The strategy utilizes a responsive "tit-for-tat with threshold adjustment" logic designed to maximize long-term individual payoffs by maintaining stock near capacity while punishing persistent defectors. It operates on the principle that cooperation is only sustainable if the aggregate behavior of opponents permits stock regeneration.

**Phase 1: Initialization**
In the first round (t=1), play C. This establishes a baseline and allows for observation of opponent behavior without immediate depletion.

**Phase 2: Monitoring and Decision Rule**
For rounds t > 1, determine the action based on the *Cooperation Rate* (CR) of the previous round and the current stock level (S).

Let $k$ be the number of opponents who cooperated in the previous round (where $0 \le k \le n-1$).
The Cooperation Rate of opponents is $CR = k / (n-1)$.

Decision Logic:
1.  **If $S < (capacity / 4)$:** Defect (D) unconditionally. When the stock is critically low, the regenerative growth is insufficient to support consumption. Immediate extraction is necessary to secure any positive payoff before the pool collapses.
2.  **If $S \ge (capacity / 4)$:**
    *   If $CR \ge \tau$: Cooperate (C). (Where $\tau$ is the cooperation threshold, initially set to 0.5).
    *   If $CR < \tau$: Defect (D).

**Phase 3: Adaptive Threshold Adjustment**
Update the threshold $\tau$ dynamically to account for opponent trends:
*   If the stock level $S$ decreased by more than 20% compared to the previous round despite playing C, increase $\tau$ by 0.1 (up to a max of 0.9). This makes the strategy more demanding of partners when the common resource is struggling.
*   If the stock level $S$ increased or remained stable while playing C, decrease $\tau$ by 0.05 (down to a floor of 0.3). This encourages cooperation when the resource is abundant.

**Phase 4: Terminal Rounds**
In the final round (t = r):
*   If $S > (capacity / 2)$, Defect (D) to extract maximum value from the remaining stock.
*   If $S \le (capacity / 2)$, continue following the Decision Logic from Phase 2.

**Pseudocode:**

```python
# Initial State
tau = 0.5
last_stock = capacity

def action(round_num, S, k, n, r):
    # Terminal phase check
    if round_num == r:
        if S > (capacity / 2): return 'D'
    
    # Critical shortage check
    if S < (capacity / 4):
        return 'D'
    
    # Cooperation logic
    if round_num == 1:
        return 'C'
    
    CR = k / (n - 1)
    
    # Update threshold based on resource health
    if S < last_stock:
        tau = min(0.9, tau + 0.1)
    elif S > last_stock:
        tau = max(0.3, tau - 0.05)
    
    last_stock = S
    
    if CR >= tau:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_14 = '''
The strategy operates on a "Tit-for-Tat with Sustainability Threshold" logic, aiming to maximize personal payoff by stabilizing the resource stock while retaliating against exploitation.

### Decision Rule
In each round $t$, calculate the target cooperation level $C_{target}$ based on the stock dynamics. Play action $A_t$ according to the following algorithm:

1.  **First Round ($t=1$):**
    Play **Cooperate (C)** to establish a cooperative baseline.

2.  **Subsequent Rounds ($t > 1$):**
    Observe the number of defectors $k_{t-1}$ from the previous round.

    *   **If $k_{t-1} = 0$:**
        Play **Cooperate (C)**. The resource is being managed sustainably.

    *   **If $k_{t-1} > 0$:**
        *   Calculate the "Sustainability Index" $SI$:
            $SI = \frac{S_t}{capacity}$
        *   If $SI > 0.5$:
            Play **Cooperate (C)**. The stock is robust enough to absorb the short-term shock of others' defection without collapsing below the recovery threshold.
        *   If $SI \le 0.5$:
            Play **Defect (D)**. The stock is dangerously low. If the group has defected, the incentive shifts from long-term sustainability to securing remaining stock before total depletion occurs.

3.  **Final Round ($t = r$):**
    *   If $S_r \ge \frac{capacity}{2}$:
        Play **Cooperate (C)**.
    *   If $S_r < \frac{capacity}{2}$:
        Play **Defect (D)**. There is no future round to benefit from regeneration; harvest the maximum possible share immediately.

### Pseudocode
```python
def get_action(round_number, stock_level, last_round_defectors, capacity, r):
    # Terminal round logic
    if round_number == r:
        if stock_level < (capacity / 2):
            return "D"
        else:
            return "C"

    # Opening round
    if round_number == 1:
        return "C"

    # Reactive strategy based on previous behavior and stock state
    if last_round_defectors == 0:
        return "C"
    else:
        # Check if resource is resilient enough to handle exploitation
        sustainability_index = stock_level / capacity
        
        if sustainability_index > 0.5:
            return "C" # Absorb defection to preserve long-term growth
        else:
            return "D" # Resource compromised; switch to individual extraction
```

### Strategic Rationale
This approach balances two competing individualistic objectives:
1.  **Sustainability Maintenance:** By cooperating when the stock is healthy ($> 0.5$ capacity), you maximize the cumulative growth potential of the common pool, which yields higher per-round payoffs in the long run.
2.  **Defensive Extraction:** By defecting when the stock is low ($\le 0.5$ capacity), you protect your individual payoff from being "taxed" by the depletion caused by others, ensuring you extract the largest possible share before the stock hits zero.
'''

description_INDIVIDUALISTIC_15 = '''
### Decision Logic

The strategy follows a "Conditional Sustainability" approach, prioritizing long-term yield over short-term gain while punishing non-cooperative behavior observed in the aggregate.

**Initialization (Round 1):**
Play **Cooperate (C)**. Establish a baseline for cooperation to preserve the resource stock for subsequent rounds, as immediate depletion is strictly suboptimal for long-term payoff.

**General Recursive Rule (Rounds $t = 2$ to $r-1$):**
Define the "Cooperation Threshold" ($T$) based on the observed behavior of opponents in the previous round ($t-1$):
*   Let $C_{obs}$ be the number of cooperators observed in round $t-1$.
*   If $C_{obs} = n-1$ (all opponents cooperated), play **Cooperate (C)**.
*   If $C_{obs} < n-1$ (at least one opponent defected), trigger a Tit-for-Tat penalty phase:
    *   Calculate the Defection Impact: If the current stock ($S_t$) is below 50% of the maximum capacity, play **Defect (D)** to maximize extraction before the resource collapses.
    *   If the current stock ($S_t$) is above 50% of the maximum capacity, play **Cooperate (C)** but maintain a "probabilistic switch" status for the next round. If defection persists for two consecutive rounds, switch to **Defect (D)** permanently for the remainder of the game.

**Terminal Rule (Round $r$):**
Regardless of previous history or current stock, play **Defect (D)**. Since no future rounds exist to provide feedback or allow for stock regeneration, maximize individual utility in the final extraction phase.

### Pseudocode Implementation

```python
def decide_action(round_t, total_rounds, current_stock, observed_cooperators_prev_round, n):
    # Terminal Round
    if round_t == total_rounds:
        return 'D'
    
    # First Round
    if round_t == 1:
        return 'C'
        
    # Recursive phase
    # Opponents is n-1
    if observed_cooperators_prev_round == (n - 1):
        return 'C'
    else:
        # Detect depletion risk
        # If stock is critical (< 50% capacity), prioritize extraction
        if current_stock < (0.5 * capacity):
            return 'D'
        # Otherwise, attempt to maintain sustainability despite moderate defection
        else:
            return 'C'
```
'''

description_INDIVIDUALISTIC_16 = '''
The objective is to maximize cumulative payoff over $r$ rounds by maintaining the common pool stock at or near capacity while incentivizing others to cooperate, transitioning to defection only when necessary to secure a share of the resource before depletion or to punish non-cooperation.

The strategy operates on a Tit-for-Tat foundation with a threshold adjustment based on the observed "cooperation rate" of opponents.

### Core Logic

1.  **Observation Variable:** Let $C_{obs}$ be the count of opponents who chose C in the previous round.
2.  **Reputation Scoring:** Maintain a running average, $R$, of the proportion of cooperators among opponents: $R = \sum_{t=1}^{k} \frac{C_{obs, t}}{(n-1) \times k}$, where $k$ is the number of rounds played. Initialize $R=1.0$ at $t=1$.
3.  **The Cooperation Threshold:** Define a variable $T$ representing the minimum cooperation proportion required to justify continued cooperation. Set $T = 0.5$.

### Decision Rules

For every round $t$:

*   **Round 1:** Play **C**.
*   **Round $t$ (where $1 < t < r$):**
    *   If $C_{obs} / (n-1) \geq T$, play **C**.
    *   If $C_{obs} / (n-1) < T$, play **D** to extract value before the stock is depleted by defectors.
*   **Final Round ($t=r$):**
    *   Regardless of previous history, play **D**. Defection in the final round provides the maximum possible payoff with no risk of future retaliation or resource depletion.

### Adaptive Mechanism

If the strategy plays **D** due to low opponent cooperation ($C_{obs} / (n-1) < T$), it may return to **C** if the opponents demonstrate a shift in behavior. 

After playing **D**, monitor $C_{obs}$ for the subsequent round. If $C_{obs} / (n-1)$ returns to a level $\geq T$, immediately return to playing **C** in the following round. This allows for "forgiveness" and re-establishment of a sustainable stock level if the group self-corrects.

### State-Dependent Constraints

If $S < \frac{capacity}{2n}$ (the stock level falls below the threshold where total consumption by even all-cooperators would lead to zero growth in the next period), switch immediately to **D** regardless of $R$ or $T$. When the resource is failing, individual payoff maximization requires extracting the remaining stock before others do.

### Pseudocode

```python
# Initialization
R = 1.0 # Cooperation history
T = 0.5 # Threshold

def choose_action(round_num, last_C_obs, current_stock, capacity, n):
    # Final round grab
    if round_num == r:
        return 'D'
    
    # Resource exhaustion check
    if current_stock < (capacity / (2 * n)):
        return 'D'
        
    # Round 1 default
    if round_num == 1:
        return 'C'
        
    # Standard decision logic
    coop_rate = last_C_obs / (n - 1)
    
    if coop_rate >= T:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_17 = '''
The strategy operates as a conditionally cooperative "Trigger-Tit-for-Tat" variant designed to maintain stock levels near the carrying capacity while punishing exploitative behavior. The core objective is to maximize the stock level $S$ to ensure that both the payoff per unit of stock and the regeneration rate are maximized, as $S$ acts as a multiplier for all future payoffs.

### Decision Rule
In each round $t$, the action $A_t$ is determined by the following logic:

1.  **First Round ($t=1$):** Play **C**.
2.  **Subsequent Rounds ($t > 1$):**
    *   Let $N_C$ be the number of cooperators in the previous round.
    *   Let $P_{target}$ be the expected number of cooperators required to keep the stock $S$ stable at $capacity$.
    *   Calculate $P_{target}$: The stock remains stable if $S_{after} + \text{Growth}(S_{after}) = S_{initial}$. For a stable system at high capacity, this generally requires all players to cooperate (as seen in the provided example where all-C maintains stock at capacity). 
    *   If $N_C = n$ (all cooperated): Play **C**.
    *   If $N_C < n$: Calculate the "Regeneration Deficit." If the stock $S$ is below a critical threshold (defined as $0.5 \times \text{capacity}$), switch to **D** immediately to extract remaining value before depletion. If $S \ge 0.5 \times \text{capacity}$, play **D** for the current round to punish the defection of the previous round, reverting to **C** in the subsequent round ($t+1$) to test for cooperation again.

### Handling Edge Cases
*   **Last Round ($t = r$):** Defect (**D**) regardless of history. The sustainability of the stock is irrelevant after the final round, and the payoff per round is strictly higher by playing D.
*   **Low Stock Scenario ($S < \text{capacity}/n$):** If the current stock is so low that even cooperation yields negligible immediate payoff and the regeneration potential is effectively destroyed, the strategy defaults to **D** to capture the remaining resources.
*   **"Tit-for-Tat" Recovery:** If the strategy detects that the aggregate behavior has shifted back to universal cooperation ($N_C = n$) after a period of punishment, it resets the cooperation cycle immediately.

### Pseudocode
```python
def get_action(round_number, n, r, capacity, current_stock, prev_round_cooperators):
    # End of game optimization
    if round_number == r:
        return 'D'
    
    # Emergency depletion threshold
    if current_stock < (capacity / n):
        return 'D'

    # First round
    if round_number == 1:
        return 'C'

    # Response to previous round
    if prev_round_cooperators == n:
        return 'C'
    else:
        # Punishment phase: defect if stock is high enough to sustain,
        # otherwise preserve by evaluating threshold logic
        if current_stock >= (0.5 * capacity):
            return 'D'
        else:
            return 'C'
```
'''

description_INDIVIDUALISTIC_18 = '''
The strategy follows a "Conditional Sustainability" protocol, designed to maximize long-term personal payoff by balancing immediate consumption with the preservation of future production capacity.

**Strategy Overview**

The agent operates on the principle of *Dynamic Tit-for-Tat* combined with *Capacity Thresholding*. The objective is to maintain the stock level (S) as close to the capacity as possible, as higher stock levels exponentially increase the sustainable harvest in subsequent rounds.

**Decision Rules**

1.  **Round 1:** Play **Cooperate (C)**. This signals a commitment to sustainability, which is necessary to seed the potential for long-term growth.

2.  **Rounds 2 to r-1:** Calculate the "Sustainability Target." 
    *   If the previous round's total consumption by all players was <= (n/2) * (S_prev / (2n)) + (n/2) * (S_prev / n), the system is considered "Stable." In this state, continue to **Cooperate (C)**.
    *   If the previous round's consumption led to a net decrease in stock (S_current < S_prev), check the level of defection. If the number of defectors in the previous round is > n/2, switch to **Defect (D)**.
    *   If you are currently Defecting and the stock level recovers to > 0.8 * capacity, switch back to **Cooperate (C)** to initiate a sustainable cycle again.

3.  **Last Round (Round r):** Always **Defect (D)**. Since there is no future round to benefit from stock growth, the individual-rational choice is to maximize the final round's consumption before the game terminates.

**Pseudocode Logic**

```python
def get_action(round, stock, history, n):
    if round == r:
        return 'D'
    
    if round == 1:
        return 'C'
    
    # Analyze previous round
    prev_stock = history[round-1].stock
    prev_defectors = history[round-1].num_defectors
    
    # If the stock is critically low, defect to salvage what is left
    if stock < (capacity * 0.1):
        return 'D'
    
    # If the group is behaving unsustainably (majority defecting)
    if prev_defectors > (n / 2):
        return 'D'
    
    # If the stock is recovering well and group is cooperating
    return 'C'
```

**Edge Case Handling**

*   **Stock Collapse:** If at any point the stock level (S) drops below 10% of the capacity, the strategy assumes a "tragedy of the commons" scenario is imminent. Immediately switch to **Defect (D)** for all remaining rounds to extract remaining value before the pool is exhausted.
*   **Perfect Cooperation:** If all players play Cooperate (C) and the stock remains at capacity, continue to **Cooperate (C)** indefinitely, as this yields the most stable long-term return path.
*   **Unknown Histories:** If observation of past defection counts is unavailable, default to **Cooperate (C)** unless the current stock level is below 50% of capacity, in which case switch to **Defect (D)**.
'''

description_INDIVIDUALISTIC_19 = '''
**Strategy: Adaptive Sustainable Tit-for-Tat (ASTFT)**

The strategy functions as a conditional cooperator that tracks the "System Health" of the common pool to determine when cooperation is viable and when defection is necessary for survival.

**State Variables:**
*   `target_stock`: 0.5 * capacity (the level at which growth is maximized).
*   `trust_score`: Initialized to 0.5. Range [0, 1].
*   `last_stock`: Initialized to capacity.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**.

2.  **Rounds 2 to r-1:**
    *   **Calculate System Health:** If the current `stock` is less than `target_stock`, immediately switch to **Cooperate (C)** to allow the pool to recover.
    *   **Calculate Expected Sustainability:** If the current `stock` is > `target_stock`, calculate the `previous_round_total_consumption`.
        *   If `previous_round_total_consumption` < `capacity / 2`, **Trust**: Maintain the previous action.
        *   If `previous_round_total_consumption` >= `capacity / 2`, **Defect**: Switch to or maintain **Defect (D)**.
    *   **Update Trust:**
        *   If the aggregate observation shows the majority of opponents cooperated, increase `trust_score` by 0.1 (capped at 1.0).
        *   If the majority defected, decrease `trust_score` by 0.2 (floor at 0.0).
    *   **Action Selection:** If `trust_score` > 0.4, play **Cooperate (C)**. Otherwise, play **Defect (D)**.

3.  **Last Round (Round r):**
    *   Always play **Defect (D)** to maximize terminal payoff, regardless of history or current stock.

**Pseudocode Logic:**

```python
if round == r:
    return Defect

if stock < (capacity / 2):
    return Cooperate

# Check if the collective action in the previous round was sustainable
# (Total consumption leading to a growth that keeps stock positive)
previous_consumption = (previous_D_count * (last_stock / n)) + (previous_C_count * (last_stock / (2*n)))

if previous_consumption >= (capacity / 2):
    trust_score -= 0.2
    return Defect

# Otherwise, follow trust-based logic
if aggregate_opponents_cooperated > aggregate_opponents_defected:
    trust_score += 0.1
else:
    trust_score -= 0.1

trust_score = clamp(trust_score, 0, 1)

if trust_score > 0.4:
    return Cooperate
else:
    return Defect
```

**Edge Case Handling:**
*   **Stock = 0:** If the stock reaches 0, play **Cooperate (C)** in all subsequent rounds to allow for potential pool replenishment from growth (if growth dynamics allow for recovery from zero), but prioritize **Defect (D)** if the game state indicates recovery is mathematically impossible for the remaining duration.
*   **Low n:** In games where n is small (e.g., n=2), the `trust_score` threshold acts as a aggressive filter, forcing defection immediately upon observing one defection, as a single defector in a small pool represents a high percentage of consumption.
'''

description_INDIVIDUALISTIC_20 = '''
The strategy is "State-Aware Trigger Tit-for-Tat" (SATT). It prioritizes long-term resource stability to maximize cumulative payoff while punishing defectors who threaten the stock level.

**Decision Logic**

For each round *t*, determine action $A_t \in \{C, D\}$ based on the observed behavior of opponents in the previous round ($t-1$) and the current stock level ($S_t$):

1.  **Initialization:**
    In round 1, play **C**.

2.  **Resource Preservation Constraint:**
    If $S_t < \text{capacity} / 2$, play **D** immediately to extract value before the stock collapses to zero, regardless of previous history.

3.  **Adaptive Response:**
    For rounds $t > 1$, where $S_t \ge \text{capacity} / 2$, calculate the Defection Index ($DI_{t-1}$) from the previous round:
    $DI_{t-1} = \frac{\text{Number of Defectors in } t-1}{n-1}$

    If $DI_{t-1} > 0.5$ (more than half the opponents defected), play **D** to prevent exploitation.

    Otherwise, play **C**.

4.  **Terminal Phase:**
    In the final round $r$, if $S_r$ is sufficient to support Defection without immediately causing total depletion (or if the stock is already low), play **D** to maximize final round payoff.

**Pseudocode:**

```python
def get_action(round, total_rounds, current_stock, capacity, n, history):
    # Rule 1: Terminal greed
    if round == total_rounds:
        return 'D'

    # Rule 2: Resource collapse protection
    if current_stock < (capacity / 2.0):
        return 'D'

    # Rule 3: Tit-for-Tat with Majority Threshold
    if round > 1:
        last_round_defectors = history[round-1].num_defectors
        # If I defected last round, I assume others did too; 
        # adjusted count if I was a defector
        if history[round-1].my_action == 'D':
            effective_defectors = last_round_defectors - 1
        else:
            effective_defectors = last_round_defectors
            
        if (effective_defectors / (n - 1)) > 0.5:
            return 'D'
    
    # Default: Cooperation for sustainability
    return 'C'
```

**Edge Cases:**
*   **n=2:** If $n=2$, the "Majority Threshold" triggers if the single opponent defected in the previous round.
*   **Low Stock:** If the stock is below $2n$ or decaying toward zero, the strategy prioritizes immediate extraction (Defection) over indefinite cooperation, as long-term sustainability is mathematically impossible.
'''

description_INDIVIDUALISTIC_21 = '''
### Strategy: "Tit-for-Tat Stock Sustainer"

This strategy employs a conditional cooperative approach to maintain the common pool resource at a sustainable level, switching to defection when the sustainability threshold is violated by opponents.

#### Decision Rules

Let $n$ be the number of players and $S_t$ be the stock at round $t$. Let $k_{t-1}$ be the number of opponents observed to have played $C$ in the previous round. The strategy uses a threshold $\tau$ (where $\tau = n-1$) to evaluate aggregate cooperation.

**For all rounds $1 \le t \le r$:**

1. **Initialization:** In Round 1, play $C$ (Cooperate) to foster long-term stock stability.
2. **Stock Condition:** If $S_t < \frac{capacity}{n}$, prioritize immediate consumption. Play $D$ (Defect) regardless of past behavior, as the resource is collapsing and long-term sustainability is no longer viable.
3. **Cooperation Monitoring:** If $S_t \ge \frac{capacity}{n}$, maintain cooperation provided that previous cooperation levels are sufficient.
   * If $t > 1$, calculate the cooperation ratio $R = \frac{k_{t-1}}{n-1}$.
   * If $R = 1$ (all opponents cooperated previously), play $C$.
   * If $R < 1$ (any opponent defected previously), play $D$.
4. **Final Round:** If $t = r$, play $D$ regardless of state or history, as there is no future utility to protect.

#### Pseudocode

```python
def get_action(round_number, stock, total_rounds, n, opponents_cooperated):
    # Check if this is the final round
    if round_number == total_rounds:
        return 'D'
    
    # Check if stock is below critical sustainability threshold
    # If the stock is too low to sustain future growth, maximize immediate payoff
    if stock < (capacity / n):
        return 'D'
        
    # First round initialization
    if round_number == 1:
        return 'C'
        
    # Tit-for-tat logic based on aggregate observation
    # Opponents_cooperated is the count of players who played C in round_number - 1
    # n - 1 is the number of opponents
    if opponents_cooperated == (n - 1):
        return 'C'
    else:
        return 'D'
```

#### Operational Logic
*   **Sustainability Bias:** The strategy assumes that a healthy pool is superior to an empty one. By playing $C$ initially and rewarding full cooperation with continued $C$, it incentivizes a stable equilibrium where growth matches consumption.
*   **Self-Protection:** The threshold check ($S_t < capacity/n$) ensures that the agent does not sacrifice its own payoff in a "tragedy of the commons" scenario where opponents are already driving the stock to zero.
*   **Defection Trigger:** The transition to $D$ is triggered immediately if *any* opponent defects, enforcing a strict standard of cooperation required to maintain the pool. 
*   **Terminal Defection:** The final round switch to $D$ captures all remaining value from the common pool, as there is no incentive to preserve stock beyond the game's horizon.
'''

description_INDIVIDUALISTIC_22 = '''
The strategy follows a conditional "Tit-for-Tat" approach with a depletion threshold check to maximize long-term yield while aggressively defending against exploitation.

**Pseudocode Structure:**

```python
# Constants defined by game parameters
REMAINING_ROUNDS = r
THRESHOLD_STOCK = capacity * 0.4  # Minimum viable buffer before collapse

def decide_action(round_number, current_stock, history):
    # 1. Terminal Phase Defection
    if round_number == REMAINING_ROUNDS:
        return 'D'

    # 2. Critical Stock Warning
    # If the stock is too low to support cooperation, protect immediate payoff
    if current_stock < THRESHOLD_STOCK:
        return 'D'

    # 3. Tit-for-Tat Adaptation
    if round_number == 1:
        return 'C'
    
    # Analyze previous round's outcome
    prev_total_consumption = (history[-1]['cooperators'] * (current_stock / (2*n))) + \
                             (history[-1]['defectors'] * (current_stock / n))
    
    # If the environment was stable or improving (stock didn't collapse), reciprocate
    # Check if the number of cooperators was sufficient to maintain growth
    if history[-1]['cooperators'] >= n / 2:
        return 'C'
    else:
        # Punish defection or resource over-extraction
        return 'D'
```

**Decision Rules:**

1.  **Initialization:** In the first round, always play 'C' to signal willingness to maintain the common pool.
2.  **Reciprocity Logic:** In subsequent rounds, monitor the aggregate action of the group from the previous round. If at least half of the group cooperated in the previous round, play 'C'. If fewer than half cooperated (indicating a trend toward resource depletion or competitive greed), play 'D'.
3.  **Sustainability Override:** Regardless of history, if the `current_stock` falls below the `THRESHOLD_STOCK` (defined as 40% of `capacity`), immediately play 'D'. This assumes the pool is approaching collapse and prioritizes individual extraction before the resource is fully depleted by others.
4.  **Terminal Phase:** In the final round (`r`), ignore all previous history and reciprocity; play 'D' to maximize the final payoff before the game ends.

**Edge Case Handling:**

*   **Stock Exhaustion:** If `current_stock` is 0 or near 0, the logic defaults to 'D' as there is no sustainable growth to protect.
*   **High Cooperation:** If the group consistently cooperates and the stock grows back to `capacity`, the strategy remains in 'C' mode, continuously cycling the resource.
*   **Sudden Defection:** If the group behavior shifts from cooperation to mass defection, the strategy immediately detects the drop below the 50% cooperation threshold and switches to 'D' in the next round, maintaining 'D' until either the game ends or the stock falls below the threshold.
'''

description_INDIVIDUALISTIC_23 = '''
Define the target sustainable stock level as `T = capacity / 2`. Maintain a belief variable `B`, representing the estimated probability that a randomly chosen opponent will cooperate in any given round, initialized to `1.0`.

**Decision Rules:**

In each round `t`, perform the following steps:

1. **Update Belief:** After observing the number of cooperators `K` from the previous round (where `K` includes your own action if cooperative), update `B` using a moving average: `B_new = (B_old * (1 - α)) + ((K - I_cooperated) / (n - 1) * α)`, where `α` is a smoothing factor (set `α = 0.2`) and `I_cooperated` is 1 if you cooperated last round, 0 otherwise. If `n=1`, `B` is irrelevant.

2. **Calculate Expected Stock:** Project the stock level for the next round based on current `S` and current `B`.
   - Calculate expected consumption `E_cons = (S / (2n)) * (n * B) + (S / n) * (n * (1 - B))`.
   - Estimate remaining stock `S_rem = S - E_cons`.
   - Estimate next round's starting stock `S_next = min(S_rem + 2 * S_rem * (1 - S_rem / capacity), capacity)`.

3. **Determine Action:**
   - **Last Round (`t = r`):** Always play `D` to maximize terminal payoff.
   - **Critical Stock Threshold:** If `S_next < (capacity / 4)`, play `D` to secure remaining value before total collapse.
   - **Optimal Equilibrium Check:** If `S_next >= T`, play `C`. This action supports sustainable growth required for long-term viability.
   - **Conditional Reciprocation:** If `S_next` is between critical threshold and `T`, play `C` if `B > 0.5`, else play `D`. This punishes defection when the resource is vulnerable while maintaining cooperation when group behavior permits.

**Edge Cases:**

- **First Round (`t = 1`):** Always play `C`. This establishes initial cooperation and maximizes the probability of higher subsequent stock.
- **Stock Depletion (`S ≈ 0`):** If `S < (capacity / (2n))`, play `D`. At near-zero stock, the absolute payoff difference between `C` and `D` is negligible, but `D` yields higher immediate utility.
- **Opponent Anonymity:** Since specific opponents cannot be tracked, the strategy relies purely on the aggregate statistic `K` to adjust aggressiveness, treating the pool as a collective behavior system.
'''

description_INDIVIDUALISTIC_24 = '''
The strategy operates on a Tit-for-Tat foundation with a dynamic stock-preservation adjustment, aimed at sustaining the stock near capacity to maximize long-term individual payoffs.

### Core Strategy Logic: "Sustainable Reciprocity"

1.  **Initialization (Round 1):** Play Cooperate (C).

2.  **Tracking State:**
    *   Maintain a variable $C_{prev}$ representing the number of opponents who played C in the previous round.
    *   Maintain an estimate of the "Cooperation Threshold" ($T$), defined as $n-1$.

3.  **Recursive Decision Rule (Rounds $t > 1$):**
    *   **If the stock $S_t$ is below a critical buffer (S < capacity * 0.25):** Always play Defect (D). At critically low levels, stock recovery via collective restraint is mathematically unlikely, making immediate extraction the only rational individualistic action.
    *   **If the stock $S_t$ is healthy (S ≥ capacity * 0.25):** Use the following conditional logic:
        *   If $C_{prev} \ge T$ (full cooperation): Play C.
        *   If $C_{prev} < T$: Play D.

4.  **Terminal Round Adjustment (Round $r$):**
    *   Regardless of previous cooperation levels, play D in the final round. There is no future round to punish or incentivize, so maximizing immediate extraction is the dominant strategy.

### Pseudocode Representation

```python
def get_action(current_round, stock, prev_opponents_cooperated, total_players, num_rounds, capacity):
    # Terminal round: always defect
    if current_round == num_rounds:
        return 'D'
    
    # Critical state: stock depleted below 25% of capacity
    if stock < (capacity * 0.25):
        return 'D'
        
    # Reciprocal cooperation: only cooperate if all others did so previously
    # Threshold for cooperation is n-1 (all other players)
    threshold = total_players - 1
    
    if prev_opponents_cooperated >= threshold:
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling

*   **Initial Round ($t=1$):** The strategy defaults to C to initiate potential mutual cooperation without waiting for external signals.
*   **Total Defection by Opponents:** If the strategy observes that $C_{prev}$ consistently falls below the threshold, it reverts to continuous D until the final round, assuming the environment is non-cooperative.
*   **Recovery Phase:** If the strategy switches to D due to low cooperation, but subsequent rounds show the stock replenishing significantly (S returns to near-capacity), the strategy remains in D until a "reset" signal is impossible. It does not attempt to "forgive" and switch back to C unless the logic is strictly applied to the immediately preceding round.
'''

description_INDIVIDUALISTIC_25 = '''
The optimal individualistic strategy is a "Conditional Sustainability" protocol, designed to maximize immediate consumption while preserving the resource stock required for long-term payoffs. It treats the stock level $S$ as the primary determinant for action, leveraging a tit-for-tat variant based on the aggregate cooperation count.

### Decision Rules

Define $k_t$ as the number of opponents who cooperated in the previous round $t-1$.

1.  **If $S_t \geq \text{Threshold}$:**
    Play **C** if $k_{t-1} \geq \lceil (n-1) \times 0.75 \rceil$ (i.e., if at least 75% of opponents cooperated).
    Play **D** if $k_{t-1} < \lceil (n-1) \times 0.75 \rceil$.

2.  **If $S_t < \text{Threshold}$:**
    Play **D** regardless of history.

**Threshold Calculation:**
The threshold is defined as $\frac{capacity}{2}$. If the stock drops below half capacity, the regenerative potential decreases significantly, making future rounds high-risk. In these states, extracting maximum value immediately is the rational individualistic choice.

### Edge Cases and Temporal Adjustments

*   **Round 1:** Play **C**. Initiating with cooperation establishes the potential for sustainable growth early, maximizing the resource base for subsequent rounds.
*   **Final Round ($t = r$):** Play **D**. Since there are no future rounds to benefit from, preserving the stock provides no utility. Defecting maximizes the terminal payoff regardless of prior state.
*   **Near-Final Rounds:** If $t > r - 3$ (the last three rounds), adopt a "descending greed" approach:
    *   If $t = r-2$, play **D** if $S_t < \frac{3}{4} \times capacity$.
    *   If $t = r-1$, play **D** regardless of $S_t$.
*   **Stock Collapse:** If $S_t = 0$, play **D**. (This is a forced state, as no payoff is possible, but D is the default action).

### Pseudocode Implementation

```python
def get_action(round_idx, total_rounds, S, capacity, n, opponents_cooperated_last_round):
    # Terminal phase logic
    if round_idx == total_rounds:
        return 'D'
    
    # Pre-terminal phase logic
    if round_idx >= total_rounds - 2:
        if round_idx == total_rounds - 1:
            return 'D'
        if S < (0.75 * capacity):
            return 'D'

    # Initial round
    if round_idx == 1:
        return 'C'

    # Core adaptive logic
    threshold = capacity / 2
    required_cooperation = ceil((n - 1) * 0.75)

    if S >= threshold:
        if opponents_cooperated_last_round >= required_cooperation:
            return 'C'
        else:
            return 'D'
    else:
        # Stock is critically low; extract value before collapse
        return 'D'
```
'''

description_INDIVIDUALISTIC_26 = '''
### Strategy: Conditional Sustainability Tit-for-Tat

The strategy operates on a principle of "reciprocal sustainability": cooperate to maintain the resource base, but punish excessive extraction by defectors while protecting against immediate resource collapse.

**Decision Rules:**

1.  **Phase 1 (Observation & Cooperation):** In Round 1, always play **C**. This establishes a baseline for cooperative interaction.

2.  **State-Dependent Response (Rounds 2 to r-1):**
    For each round $t$, calculate the *Defection Count ($d_{t-1}$)* observed in the previous round based on the resulting stock level relative to the expected outcome.
    *   If $S_{t-1} \approx \text{Expected Stock given full cooperation}$, assume all opponents cooperated. Play **C**.
    *   If $S_{t-1} < \text{Expected Stock given full cooperation}$, assume opponents are depleting the resource. Play **D** with probability proportional to the observed depletion. Specifically:
        *   If the number of defectors in the previous round $k > n/2$, play **D** for the current round to extract value before the resource collapses.
        *   If the number of defectors $k \leq n/2$, play **C** to incentivize long-term growth.

3.  **The "Last Round" Override (Round r):**
    Regardless of history, if $r$ is the final round, play **D**. Since there is no future state to preserve, extraction of all available stock is the dominant strategy to maximize terminal payoff.

4.  **Resource Criticality Threshold (Safety Valve):**
    If at any point $S_t < (\text{capacity} / n)$, immediately switch to **C** to prevent resource extinction in the subsequent round, unless it is the final round. If the stock is critically low, maximizing sustainable growth is the only way to avoid a zero-payoff future.

**Pseudocode Implementation:**

```python
def get_action(round_t, current_stock, history):
    # Rule 3: Terminal Round Defection
    if round_t == total_rounds:
        return D

    # Rule 4: Resource Protection
    if current_stock < (capacity / n):
        return C

    # Rule 1: First Round
    if round_t == 1:
        return C

    # Rule 2: Adaptive Response
    # Calculate observed defectors from previous round state
    previous_stock = history.last_round_stock
    expected_if_all_cooperate = calculate_next_state(previous_stock, all_C=True)
    
    if current_stock < expected_if_all_cooperate:
        # Determine defector count k
        k = estimate_defectors(previous_stock, current_stock)
        
        if k > (n / 2):
            return D
        else:
            return C
    
    return C
```

**Edge Case Handling:**
*   **Rapid Depletion:** If the stock drops below the replenishment threshold due to opponent aggression, the strategy prioritizes the "Resource Criticality Threshold" (Rule 4), forcing cooperation to prevent a zero-stock state.
*   **Uncertain Observation:** When the exact number of defectors $k$ is ambiguous due to the specific math of the growth function, the strategy defaults to **C** if the stock is high enough to absorb the shock, maintaining a "benefit of the doubt" stance to maximize potential long-term returns.
'''

description_INDIVIDUALISTIC_27 = '''
### Tit-for-Tat Sustainability Strategy

The primary objective is to maintain the stock level near the `capacity` to maximize long-term consumption while remaining robust against exploitative behavior. 

**Decision Logic:**

1.  **Round 1:** Play **Cooperate (C)**. This initiates the game with a cooperative signal and preserves the common pool for the maximum number of future rounds.

2.  **Subsequent Rounds (2 to r):**
    *   **Stock Check:** If the current stock `S` is below a threshold of `0.25 * capacity`, switch to **Cooperate (C)** regardless of previous rounds, as the priority shifts to preventing total stock collapse.
    *   **Target Growth:** Calculate the required consumption to maintain equilibrium (where stock growth replaces consumption). If the previous round's outcome resulted in a stock decrease of more than 10% of `capacity` (indicating aggregate over-consumption), play **Cooperate (C)**.
    *   **Reciprocity:** If the stock is healthy (`S >= 0.25 * capacity`), calculate the Cooperation Ratio `CR` = (number of cooperators in previous round) / `n`.
        *   If `CR` > 0.5: Play **Cooperate (C)**.
        *   If `CR` <= 0.5: Play **Defect (D)**. This penalizes the pool for over-extraction or provides individual compensation for the inevitable stock decline caused by others.

3.  **Final Round (r):**
    *   If the current stock `S` is less than `0.5 * capacity`: Play **Cooperate (C)** to avoid total resource exhaustion if possible (though this is often moot).
    *   Otherwise: Play **Defect (D)**. This is the terminal round; the future value of the stock is zero, so individual extraction is prioritized.

**Pseudocode:**

```python
def get_action(round, n, S, capacity, history):
    # Terminal Round
    if round == r:
        return D if S >= 0.5 * capacity else C

    # Resource Preservation Check
    if S < 0.25 * capacity:
        return C

    # Round 1
    if round == 1:
        return C

    # Identify previous round outcome
    prev_S = history[-1].S
    num_cooperators = history[-1].num_cooperators
    
    # Check for unsustainable depletion in previous round
    # (If stock dropped significantly, prioritize restoration)
    if (prev_S - S) > 0.1 * capacity:
        return C

    # Reciprocity Logic
    cooperation_ratio = num_cooperators / n
    if cooperation_ratio > 0.5:
        return C
    else:
        return D
```
'''

description_INDIVIDUALISTIC_28 = '''
**Decision Rules**

The agent maintains a target stock-preservation threshold and a reputation score $R$ for the collective. $R$ begins at 0 and is updated each round $t$ based on the aggregate behavior of opponents ($k$ cooperators out of $n-1$ opponents):

$R_{t} = R_{t-1} + \frac{k}{n-1} - \text{threshold}_{coop}$

where $\text{threshold}_{coop} = \frac{n-2}{2n-2}$ (representing the break-even point for population-level cooperation).

**Action Selection:**

1.  **Round 1:** Play **Cooperate (C)** to establish positive signaling.
2.  **Rounds 2 to $r-1$:**
    *   If current stock $S_t < \frac{\text{capacity}}{4}$, play **Cooperate (C)** regardless of $R$ to prevent resource collapse.
    *   If $R_{t-1} \geq 0$, play **Cooperate (C)**.
    *   If $R_{t-1} < 0$, play **Defect (D)** to maximize extraction before the resource is depleted by others.
3.  **Final Round ($r$):** Play **Defect (D)**. Since no future stock regeneration matters for the player’s total payoff, extraction of remaining stock is prioritized.

**State Monitoring and Edge Cases**

*   **Observed Collapse:** If $S_t \approx 0$ (defined as $S_t < 1$), the game is functionally over. Play **Defect (D)** in all remaining rounds, as the resource will not regenerate sufficiently to provide future returns.
*   **Reputation Reset:** If $R$ falls below a floor of $-2$, reset $R$ to $0$ and switch to **Cooperate (C)** for one round as a "probe" to see if the population has shifted to a cooperative equilibrium. If the population fails to reciprocate (i.e., $k/n-1$ remains low), immediately revert to **Defect (D)**.
*   **The "Defector Majority" Trigger:** If, in any round $t$, the number of cooperators $k$ is less than or equal to $1$ (signifying aggressive exploitation by the majority), play **Defect (D)** for the remainder of the game, ignoring $R$, unless $S_t$ recovers above $0.75 \times \text{capacity}$.
'''

description_INDIVIDUALISTIC_29 = '''
The strategy follows a conditional, threshold-based logic, adapting to the stock level and observed cooperation of others. The core principle is "tit-for-tat with a sustainability constraint": cooperating to maximize long-term yield while punishing defectors, subject to a minimum viability check on the pool stock.

**Strategy Logic**

1.  **Phase 1: Startup (Round 1)**
    Always play **C**. Establish a baseline of cooperation to signal willingness to participate in a sustainable equilibrium.

2.  **Phase 2: Monitoring (Rounds 2 to r-1)**
    Evaluate the stock and the behavior of the group from the previous round (t-1).

    *   **Sustainability Check:**
        If the *S* (stock) after the previous round’s consumption is less than or equal to a critical threshold (defined as 10% of capacity), switch to **D** regardless of past history. This prioritizes immediate consumption before the stock reaches a near-zero state from which it cannot recover.

    *   **Conditional Reciprocation:**
        If the stock is above the critical threshold, calculate the cooperation rate of the group:
        Let *c* be the number of players who chose **C** in the previous round.
        *   If *c* ≥ (n - 1) (i.e., everyone else cooperated), play **C**.
        *   If *c* < (n - 1) (i.e., at least one defector exists), play **D**.

    *   **Recovery Exception:**
        If you played **D** in the previous round due to defectors, but the number of defectors in the group is 0, play **C** in the current round to initiate a return to cooperation (re-start the cycle).

3.  **Phase 3: Endgame (Round r)**
    Always play **D**. Since there are no future rounds to influence via reputation or signal, maximize individual payoff before the game terminates.

**Pseudocode Implementation**

```python
def get_action(round_number, n, r, capacity, current_stock, prev_round_cooperators):
    # Phase 3: Endgame
    if round_number == r:
        return 'D'
        
    # Phase 1: First Round
    if round_number == 1:
        return 'C'

    # Phase 2: Monitoring and Adaptation
    # Sustainability Check
    if current_stock <= 0.1 * capacity:
        return 'D'
    
    # Conditional Reciprocation
    # prev_round_cooperators includes self in the count
    # Check if everyone else cooperated
    # prev_round_cooperators is the count of C actions in round t-1
    if prev_round_cooperators >= n - 1:
        return 'C'
    else:
        # If any defections occurred, trigger punishment/defection
        return 'D'
```
'''

description_INDIVIDUALISTIC_30 = '''
Define the strategy state as `trust_score` (initial value: 1.0, range [0, 1]). `trust_score` acts as a measure of the cooperative history of the population.

**Round 1:**
Play **C**.

**Subsequent Rounds (2 to r):**
1. Evaluate the previous round's outcome:
   - Let $k$ be the number of cooperators observed in the previous round.
   - Let $n$ be the total number of players.
   - Calculate `cooperation_rate` = $k / n$.
   
2. Update `trust_score`:
   - `trust_score` = `trust_score` * 0.9 + `cooperation_rate` * 0.1.
   
3. Check the sustainability threshold:
   - If the `stock` is below a safety floor defined as `capacity / n`, immediately play **D** to extract remaining value before depletion, regardless of history.
   
4. Decision Rule:
   - If `stock` ≥ `capacity / n`:
     - If `trust_score` ≥ 0.7: Play **C**.
     - If `trust_score` < 0.7: Play **D**.
   - If `stock` < `capacity / n`: Play **D**.

**Final Round (r):**
Play **D**, regardless of history, `trust_score`, or current `stock` level. This maximizes individual gain when future interactions are non-existent.

**Pseudocode Logic:**

```python
def get_action(round_number, stock, history, n, capacity, r):
    if round_number == r:
        return 'D'
    
    if stock < (capacity / n):
        return 'D'
        
    if round_number == 1:
        return 'C'
        
    # history stores the count of cooperators from the previous round
    cooperation_rate = history[-1] / n
    trust_score = update_trust_score(cooperation_rate) 
    
    if trust_score >= 0.7:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_31 = '''
Maintain an internal state variable `reputation` (initially 0), which tracks the average cooperation level of the opponent pool over time. In each round `t`, execute the following logic:

**1. Decision Rules**
If `t = 1`, play **C**.

For all rounds `t > 1`:
- Calculate the observed average cooperation rate of the population from the previous round: `obs_rate = (count_cooperators) / (n - 1)`.
- Update `reputation`: `reputation = (0.7 * reputation) + (0.3 * obs_rate)`.
- If `stock / capacity < 0.25`:
    - Play **D** regardless of `reputation`. (Rationale: The common pool is collapsing; extract immediate value before the stock hits zero).
- Else if `reputation > 0.6`:
    - Play **C**. (Rationale: The population is sufficiently cooperative to sustain the stock; playing C prevents depletion).
- Else:
    - Play **D**. (Rationale: The population is depleting the stock; playing C is insufficient to save the pool and results in lower individual returns).

**2. Last Round Behavior**
If `t == r`, play **D** regardless of the calculated logic above. (Rationale: Future payoffs are zero; extraction maximizes final total payoff).

**3. Edge Cases**
- If `n = 1` (impossible per parameter constraints, but conceptually): Play **D** always.
- If `stock == 0`: Play **C** (as any action yields 0, but C is the neutral default).
- If `obs_rate` calculation is undefined (i.e., `n=1`), default to **C** for the duration of the game until the final round.
'''

description_INDIVIDUALISTIC_32 = '''
The strategy employs a conditional "Tit-for-Tat with Sustainability Threshold" approach, balancing individual utility maximization against the necessity of maintaining a renewable resource base.

**Strategy Core:**
The strategy aims to cooperate if, and only if, the collective behavior of opponents suggests a sustainable resource trajectory. It models the game as a series of contingent exchanges: cooperate to preserve stock, defect if the stock is being depleted by others, and defect on the final round to capture terminal utility.

**Decision Rules:**
1.  **Round 1:** Play C (Cooperate). Establish a baseline for cooperation.
2.  **Round $r$ (Final Round):** Play D (Defect). Since future resource regeneration is impossible, maximize current period consumption.
3.  **Rounds 2 through $r-1$:**
    *   Calculate the *Sustainability Index* of the previous round. The stock is sustainable if the new stock $S_{t+1}$ is $\ge S_t \times 0.95$.
    *   Calculate the *Opponent Cooperation Rate* ($\phi$) from the previous round: $\phi = \frac{\text{Opponents who played C}}{n-1}$.
    *   **Logic:**
        *   If the stock is critically low ($S < 0.2 \times \text{capacity}$), play D (Defect) to secure a share before depletion.
        *   If the previous round's outcome resulted in a sustainable stock level ($S_{t+1} \ge S_t \times 0.95$) and the opponent cooperation rate $\phi > 0.5$, play C (Cooperate).
        *   If the stock is declining or opponent cooperation is low ($\phi \le 0.5$), play D (Defect) to protect individual payoff share.

**Pseudocode:**

```python
def get_action(round, current_stock, prev_round_data):
    # Rule 1: Terminal round
    if round == total_rounds:
        return 'D'
        
    # Rule 2: First round
    if round == 1:
        return 'C'
        
    # Rule 3: Sustainability check
    # Let S_prev be stock at start of previous round
    # Let S_curr be stock at start of this round
    # Let opponents_C be count of C from previous round
    
    is_sustainable = (S_curr >= S_prev * 0.95)
    cooperation_rate = opponents_C / (n - 1)
    
    if current_stock < (0.2 * capacity):
        return 'D'
        
    if is_sustainable and cooperation_rate > 0.5:
        return 'C'
    else:
        return 'D'
```

**Edge Cases:**
*   **Stock Collapse ($S=0$):** If the stock reaches 0, the payoff for all future actions is 0. In this state, the action is irrelevant, but the logic defaults to D.
*   **High Stock ($S \approx \text{capacity}$):** If the resource is at maximum capacity, the strategy maintains C unless the opponent cooperation rate falls below the 0.5 threshold, treating high stock as a buffer that does not justify immediate exploitation if cooperation is widespread.
*   **Low $n$:** In small groups (e.g., $n=2$), the logic holds, but the sensitivity to individual defection is higher; the strategy forces a return to D immediately if the sole opponent defects, preventing exploitation.
'''
