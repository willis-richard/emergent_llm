"""
Strategy descriptions for public_goods.

Generated with:
- Provider: Client
- Model: gemini-3.1-flash-lite-preview
"""


description_COLLECTIVE_1 = '''
The strategy employs a "Conditional Tit-for-Tat" framework based on the observed contribution rate of the group.

### Strategy Initialization
For the first round, cooperate ($C$). This signals a willingness to engage in mutually beneficial cooperation.

### Round t Decision Rules
For all rounds $t \in \{1, \dots, r\}$:

1.  **If $t = 1$:** Play $C$.
2.  **If $t > 1$:**
    *   Define $C_{t-1}$ as the total number of cooperators in the previous round.
    *   Calculate the observed cooperation rate $P_{t-1} = \frac{C_{t-1} - c_{self, t-1}}{n - 1}$, where $c_{self, t-1}$ is your own action in the previous round. This isolates the behavior of the other $n-1$ players.
    *   Define a threshold $T = 0.5$ (or $\frac{n}{2(n-1)}$ if adjusting for population sensitivity).
    *   **Decision Logic:**
        *   If $P_{t-1} \ge T$: Play $C$. (The collective is sufficiently cooperative; continue maintaining the public good.)
        *   If $P_{t-1} < T$: Play $D$. (The collective has fallen below the cooperation threshold; switch to defection to avoid exploitation.)

### Last Round Adjustment
In the final round $t = r$:
*   If the strategy has been in a "cooperative state" (meaning it played $C$ in round $r-1$), play $C$ to sustain the mutual benefit until the end.
*   If the strategy has been in a "defective state" (meaning it played $D$ in round $r-1$), play $D$.

### Robustness & Recovery
To prevent permanent deadlock due to isolated fluctuations:
*   Every $m$ rounds (where $m=5$ or an equivalent fraction of $r$), initiate a "probing" round.
*   If currently in a defective state, play $C$ regardless of the previous round's outcome.
*   If the resulting $P_t \ge T$, resume the Conditional Tit-for-Tat logic in the next round. If $P_t < T$, revert immediately to $D$ for the subsequent round.
'''

description_COLLECTIVE_2 = '''
The strategy is a conditional variant of Tit-for-Tat designed to maximize long-term cooperation while mitigating exploitation.

### Decision Rules

For round $t=1$:
Play **Cooperate (C)**.

For round $t > 1$:
Observe the number of cooperators from round $t-1$, denoted as $N_{c, t-1}$.
1. If $N_{c, t-1} \ge \lceil n/k \rceil$, play **Cooperate (C)**.
   *Rationale: The threshold $\lceil n/k \rceil$ represents the minimum number of cooperators required to make cooperation individually profitable compared to full defection.*
2. If $N_{c, t-1} < \lceil n/k \rceil$, play **Defect (D)**.
   *Rationale: If the group contribution level is below the breakeven point, cooperation results in a lower payoff than defection; punish by switching to defection.*

### Edge Cases and Adjustments

*   **Final Round ($t = r$):**
    If the strategy is intended to be purely selfish for the final round, play **Defect (D)** unconditionally because there is no future interaction to incentivize. However, for a *collective* strategy aiming to signal trust or maintain a reputation in potentially repeating environments, apply the standard rule:
    *   If $N_{c, r-1} \ge \lceil n/k \rceil$, play **Cooperate (C)**.
    *   Otherwise, play **Defect (D)**.

*   **Recovery from Defection:**
    The strategy is "forgiving" by default. If the group returns to the threshold $\lceil n/k \rceil$ in round $t$, the strategy immediately reverts to **Cooperate (C)** in round $t+1$. No extended punishment phase is required; the decision rule is strictly reactive to the previous round's outcome.

*   **Threshold Constraint:**
    If $k \le 1$, the payoff of cooperation is always strictly less than the payoff of defection. In this specific case, unconditionally play **Defect (D)** for all rounds $t=1 \dots r$.
'''

description_COLLECTIVE_3 = '''
**Strategy: Adaptive Reciprocal Tit-for-Tat with Forgiving Defection Threshold**

**Round 1:** Cooperate (C).

**Round 2 to Round (r-1):**
Calculate the cooperation rate of the opponents in the previous round ($C_{opp\_prev}$), where $C_{opp\_prev} = \frac{(\text{Total Cooperators in } t-1) - (\text{Self Contribution in } t-1)}{n-1}$.

1.  If $C_{opp\_prev} \geq \frac{1}{k}$: Cooperate (C).
2.  If $C_{opp\_prev} < \frac{1}{k}$: Defect (D).

**Round r (Final Round):**
Defect (D) regardless of history.

**Edge Cases & Exception Handling:**
*   **Initialization (r=1):** If the total game length is only one round ($r=1$), Defect (D) immediately.
*   **Inconclusive History:** If $n-1 = 0$ (not possible per parameters $n \geq 2$), default to Defect (D).
*   **Threshold Adjustment:** If the calculated cooperation rate of opponents is exactly $\frac{1}{k}$, treat this as satisfying the condition for cooperation (C).
'''

description_COLLECTIVE_4 = '''
The strategy follows a conditional, threshold-based cooperation model designed to incentivize collective contribution while minimizing losses against exploiters.

**Strategy Definition:**

1.  **Initialization:** In the first round, play Cooperate (C).

2.  **State Tracking:** Track the number of Cooperators in each previous round ($C_{t-1}$). Define the cooperation threshold $T$ as $n/k$. This threshold represents the point of indifference where individual payoffs for C and D are equal ($1 = k(C/n)$).

3.  **Round-to-Round Decision Rule:**
    *   If $t = r$ (the final round), play Defect (D).
    *   If $t < r$, evaluate the previous round's outcome:
        *   If the number of cooperators ($C_{t-1}$) $\ge T$, play C.
        *   If the number of cooperators ($C_{t-1}$) $< T$, play D.

4.  **Recovery Protocol:**
    *   If the strategy defected in the previous round ($t-1$) due to low contributions, attempt a single round of "testing" cooperation if $t < r-1$.
    *   If the subsequent round yields $C_t \ge T$, continue playing C.
    *   If $C_t < T$, revert to playing D immediately.

**Pseudocode:**

```python
# Constants
n = number_of_players
k = multiplication_factor
r = total_rounds
threshold = n / k

# Variables
last_action = 'C' # First round
history = []

def get_action(current_round, history):
    if current_round == r:
        return 'D'
    
    if current_round == 1:
        return 'C'

    prev_cooperators = history[-1]

    # Recovery from punishment phase
    if last_action == 'D' and current_round > 2:
        # Occasionally test cooperation after a defection cycle
        if random.random() < 0.1: # 10% probability to probe for restoration
            return 'C'

    # Standard conditional cooperation
    if prev_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_1 = '''
Define a "target cooperation level" τ based on the game parameters: τ = min(1, 1/k). In the first round, play Cooperate.

For all subsequent rounds *t* (where 1 < *t* ≤ *r*):

1.  **Monitor Cooperation:** Observe the total number of cooperators from the previous round, *C*_(t-1). Calculate the observed cooperation rate: *ρ*_(t-1) = *C*_(t-1) / *n*.
2.  **Evaluate Reciprocity:** Determine the strategy's own intended action based on the aggregate behavior of the group:
    *   If *ρ*_(t-1) ≥ *τ*, play Cooperate.
    *   If *ρ*_(t-1) < *τ*, play Defect.
3.  **Last Round Exception:** Regardless of the above rules, if *t* = *r*, play Defect.

**Edge Cases and Adjustments:**
*   **Initialization:** If the calculation of *τ* results in a value such that *τ* ≤ 0, play Defect exclusively.
*   **Stochastic Sensitivity:** To avoid total collapse due to isolated mistakes or noise, introduce a "forgiveness" trigger: If *ρ*_(t-1) < *τ* but *ρ*_(t-1) > 0, calculate the moving average of cooperation over the previous 3 rounds. If this moving average is ≥ *τ*, play Cooperate despite the most recent Defect.
*   **Terminal Phase:** To mitigate the inevitable "end-game effect" where rational agents defect in the final round, begin a "ramp-down" phase starting at *t* = *r* - 1. In this phase, play Defect if *ρ*_(t-1) < 0.5; otherwise, maintain Cooperate. This protects against immediate exploitation while signaling a willingness to contribute until the game's horizon is imminent.
'''

description_PROSOCIAL_2 = '''
To play the N-Player Public Goods Game prosocially, employ a conditional cooperation strategy with a "tit-for-tat with forgiveness" logic, adjusted for the aggregate feedback mechanism.

**Strategy: Prosocial Conditional Contribution**

1.  **First Round:** Play **Cooperate (C)**. Assume an initial environment of trust to facilitate optimal group payoffs.

2.  **Subsequent Rounds (t > 1):** Calculate the previous round’s contribution rate of the group: $R_{t-1} = (\text{Total Cooperators in round } t-1) / n$.
    *   If you played C in the previous round, your contribution to the total count was 1. If you played D, it was 0.
    *   Determine the behavior of opponents: $O_{t-1} = (\text{Total Cooperators} - c_{i, t-1}) / (n - 1)$. This represents the fraction of opponents who cooperated.

    *   **Cooperation Rule:**
        *   If $O_{t-1} \ge \theta$, where $\theta$ is a threshold parameter (initially 0.5), continue to **Cooperate (C)**.
        *   If $O_{t-1} < \theta$, play **Defect (D)**.

    *   **Forgiveness and Recovery:**
        *   If you are currently defecting (due to low opponent cooperation), do not stay in a permanent state of defection. Every 3 rounds of defection, test the group's intent by playing **Cooperate (C)**, regardless of the previous round's outcome.
        *   If the group responds with an $O_{t} \ge \theta$ during this test, reset to the Cooperation Rule.

3.  **Last Round (t = r):**
    *   If the history of the game shows that $O_{t} > 0$ on average across all rounds, play **Cooperate (C)** to maximize total social welfare, assuming the likelihood of future retribution or signaling is irrelevant but social utility remains the priority.
    *   If the history shows the group consistently converged to a Defect equilibrium (average $O \approx 0$), play **Defect (D)**.

4.  **Parameter Adaptation:**
    *   Adjust $\theta$ dynamically. If the group consistently cooperates (e.g., $O_{t-1} = 1.0$), lower $\theta$ slightly to be more tolerant of transient noise.
    *   If the group is highly volatile, increase $\theta$ toward $1.0$ (requiring nearly unanimous cooperation to sustain C).
'''

description_PROSOCIAL_3 = '''
The strategy utilizes a conditional cooperation approach centered on establishing and maintaining a mutual contribution threshold.

**Decision Rules**

The strategy tracks a state variable `Target`, which represents the minimum number of cooperators expected from the group to justify ongoing contribution.

*   **Round 1:** Play **Cooperate (C)** to signal willingness to participate in the public good.
*   **Subsequent Rounds:** Let `C_prev` be the number of cooperators observed in the previous round.
    *   If `C_prev` ≥ `Target`, play **Cooperate (C)**.
    *   If `C_prev` < `Target`, play **Defect (D)**.

**Target Calculation**

The `Target` is initialized as 1. If the group average cooperation levels fluctuate, the strategy dynamically adjusts `Target` to align with the critical mass required for the public good to be profitable for the individual. The `Target` is calculated as the smallest integer `T` such that:
(k / n) * T > 1

This ensures the strategy only sustains cooperation when the public good return meets or exceeds the opportunity cost of the contribution.

**Adaptive Feedback and Recovery**

To remain robust against transient shocks (e.g., accidental defections or non-responsive opponents):

1.  **The "Probe" Mechanism:** If the strategy is currently playing Defect due to low `C_prev`, it will periodically attempt to "probe" for cooperation. Every `m` rounds (where `m` is an integer, typically 3), play **Cooperate (C)** regardless of the previous round's outcome. If this probe round results in `C_prev` ≥ `Target` (or if it triggers a reciprocal response in the following round), resume full conditional cooperation based on the standard logic.
2.  **Last Round:** In the final round (round `r`), play **Defect (D)** unless the current `C_prev` indicates that the group has consistently sustained `C_prev` ≥ `Target` for the majority of the game. If the group has sustained cooperation, continue playing **Cooperate (C)** to maximize the collective social optimum.

**Pseudocode**

```python
# Constants: n, k, r
# Threshold T = ceil(n / k)
# History: Track rounds_cooperated

Target = ceil(n / k)
Probe_Interval = 3

for round in 1 to r:
    if round == 1:
        play Cooperate
    elif round == r:
        if history_is_highly_cooperative:
            play Cooperate
        else:
            play Defect
    elif round % Probe_Interval == 0:
        play Cooperate
    else:
        if C_prev >= Target:
            play Cooperate
        else:
            play Defect
```
'''

description_PROSOCIAL_4 = '''
The strategy employs a conditional cooperative approach based on the "Generous Tit-for-Tat" principle, adapted for anonymity and aggregate observation in an $N$-player setting.

**Core Mechanism: Adaptive Threshold Cooperation**

1.  **Initial Round (t=1):**
    Always Cooperate (C). This initiates a prosocial signal and tests the population for reciprocity.

2.  **Subsequent Rounds (1 < t < r):**
    Calculate the observed cooperation rate of the population from the previous round (t-1). Let $C_{t-1}$ be the number of players who cooperated in the previous round, and $n$ be the total players. Since you are one of the $n$ players, the number of *other* players who cooperated is $C_{others} = C_{t-1} - c_{me}$, where $c_{me} = 1$ if you cooperated and $0$ if you defected.

    Define the threshold for cooperation $T$ as $1 - (1/k)$, where $k$ is the multiplication factor.

    *   If $C_{others} / (n-1) \ge T$: Cooperate (C).
    *   If $C_{others} / (n-1) < T$: Defect (D) with probability $p$, where $p$ is proportional to the deviation from $T$. Specifically, play D if a random variable $rand(0,1) < (1 - C_{others}/(n-1))$. Otherwise, Cooperate (C).

    This probabilistic defection serves as a "forgiving" mechanism; it punishes consistent defectors but maintains a baseline level of cooperation to encourage the group to return to mutual contribution.

3.  **Final Round (t=r):**
    Always Defect (D). Since the game concludes, there is no future interaction to incentivize, and the dominant strategy is to maximize the final round payoff by keeping the endowment.

**Pseudocode:**

```python
# Parameters: n (players), k (multiplier), history (previous round data)
# Variables: c_me (my action last round), count_total (total cooperators last round)

def get_action(t, r, n, k, count_total, c_me):
    if t == 1:
        return 'C'
    
    if t == r:
        return 'D'
    
    # Calculate cooperation rate of opponents
    count_others = count_total - (1 if c_me == 'C' else 0)
    coop_rate_opponents = count_others / (n - 1)
    
    # Threshold for social efficiency: r_eff = 1 - 1/k
    # This aligns with the point where the group benefits from contribution
    threshold = 1 - (1 / k)
    
    if coop_rate_opponents >= threshold:
        return 'C'
    else:
        # Probabilistic forgiveness: cooperate with probability 
        # equal to the observed cooperation rate to avoid total collapse
        if random() < coop_rate_opponents:
            return 'C'
        else:
            return 'D'
```
'''

description_ALTRUISTIC_1 = '''
For each round $t \in \{1, \dots, r\}$, track the history of the total number of cooperators observed in previous rounds, $C_{obs, t-1}$, where $C_{obs, 0} = 0$. Let $C_{self, t}$ be the action taken (1 for Cooperate, 0 for Defect). The total contributions in a round is $S_t = C_{obs, t-1} + C_{self, t}$.

**Strategy Logic:**

1.  **Round 1:** Play **Cooperate** ($C_{self, 1} = 1$). This signals willingness to contribute to the public good.

2.  **Rounds 2 to $r-1$:**
    Calculate the average cooperation rate of the opponents in the previous round, $A_{t-1} = C_{obs, t-1} / (n-1)$.
    *   If $A_{t-1} > 0.5$ (or if the cooperative threshold $k/n > 0.5$), maintain **Cooperate**.
    *   If $A_{t-1} \leq 0.5$, play **Defect** to protect against exploitation, unless the cumulative gain for the group is high. Specifically, use a "Generous Tit-for-Tat" adjustment: Play **Cooperate** if the observed cooperation in the previous round was at least $n/k - 1$ (the breakeven point where contributing is net-positive for the contributor), otherwise play **Defect**.

3.  **Final Round ($t = r$):**
    Play **Defect**. Given that future rounds cannot be influenced by current actions, the game simplifies to a one-shot prisoner's dilemma where defection is the dominant strategy. This maximizes individual payoff without violating the cooperative spirit of the earlier rounds.

**Pseudocode:**

```python
def get_action(t, r, n, k, history):
    # t: current round (1 to r)
    # history: list of total cooperators in previous rounds
    
    if t == 1:
        return Cooperate
        
    if t == r:
        return Defect
        
    # Observe opponents' behavior in the previous round
    # We remove our own previous action to isolate opponent behavior
    prev_total_cooperators = history[-1]
    my_prev_action = my_history[-1]
    opponents_prev_cooperation = prev_total_cooperators - my_prev_action
    
    # Calculate payoff breakeven point: 
    # Contributing is rational if k * (S + 1) / n > 1 + k * S / n
    # Which simplifies to k > n / (S + 1) or S > n/k - 1
    breakeven_threshold = (n / k) - 1
    
    if opponents_prev_cooperation >= breakeven_threshold:
        return Cooperate
    else:
        return Defect
```

**Adaptation for Altruism:**
To maintain a stronger altruistic stance, if the total contributions in the previous round result in a positive net utility for the group (i.e., $(k/n) \times S_t > 1$), continue to Cooperate regardless of the strict breakeven point. This favors long-term collective welfare over immediate individualistic defection.
'''

description_ALTRUISTIC_2 = '''
For the first round, play Cooperate (C).

For all subsequent rounds $t \in \{2, ..., r\}$, determine the action based on the aggregate cooperation level from the previous round $C_{total, t-1}$:

1.  **Calculate the "Cooperation Threshold" ($T$):** 
    $T = \lceil n/k \rceil$. This threshold represents the minimum number of cooperators required for the collective benefit of cooperation to outweigh the individual benefit of defection.

2.  **Evaluate Reciprocity:**
    *   If $C_{total, t-1} \ge T$: Play Cooperate (C). By contributing, you reward the group for maintaining a level of cooperation that yields a net positive outcome for the collective.
    *   If $C_{total, t-1} < T$: Play Defect (D). By defecting, you signal that the current level of cooperation is insufficient to sustain the public good and protect your endowment from being wasted on a failing initiative.

3.  **Endgame Condition:**
    In the final round ($t = r$), play Cooperate (C) if and only if $C_{total, r-1} \ge T$. If $C_{total, r-1} < T$, play Defect (D). This enforces the same conditional cooperation logic as earlier rounds, ensuring that altruism is only extended when it is reciprocated at a level that justifies the cost.

**Summary Pseudocode:**

```python
# Constants
n = number_of_players
k = multiplication_factor
T = ceil(n / k)

# Round 1
Action[1] = Cooperate

# Rounds 2 to r
for t from 2 to r:
    previous_cooperators = get_cooperation_count(t-1)
    
    if previous_cooperators >= T:
        Action[t] = Cooperate
    else:
        Action[t] = Defect
```
'''

description_ALTRUISTIC_3 = '''
The strategy follows a "Conditional Tit-for-Tat with a Forgiving Threshold" logic designed to incentivize mutual cooperation while remaining robust against exploitation.

**Decision Rules**

The strategy maintains a state variable $T$, representing the "Cooperation Threshold." This threshold is defined by the minimum aggregate number of cooperating opponents from the previous round required to justify continued cooperation.

1.  **First Round:** Play **Cooperate (C)**. Set the initial baseline for cooperation.

2.  **Subsequent Rounds ($t > 1$):**
    *   Let $S_{t-1}$ be the total number of players who cooperated in round $t-1$.
    *   Let $C_{t-1}$ be your action in round $t-1$.
    *   Calculate the number of *other* players who cooperated: $O_{t-1} = S_{t-1} - C_{t-1}$.
    *   The strategy calculates the "Cooperation Threshold" $T$ as $T = \lceil n \cdot \frac{1}{k} \rceil$. This value represents the minimum number of contributors required for the public good to provide a positive net return on investment for the group (making cooperation efficient).

    *   **Condition A (Reciprocation):** If $O_{t-1} \ge T$, play **Cooperate (C)**.
    *   **Condition B (Punishment/Correction):** If $O_{t-1} < T$, play **Defect (D)**.

3.  **The Forgiveness Mechanism:**
    If the strategy played Defect (D) in the previous round, it enters a "Test Phase" in the current round $t$:
    *   Play **Cooperate (C)** with probability $p = 0.1$.
    *   If the outcome of the test round results in $O_t \ge T$, revert to Condition A for the next round. If not, maintain Defect status until a test round returns a cooperative environment.

**Edge Cases**

*   **Last Round ($t=r$):**
    The altruistic imperative is modified to avoid the rational defection trap. If $r$ is known, play **Cooperate (C)** if and only if the average cooperation rate of opponents over the previous $r-1$ rounds exceeds $T / (n-1)$. Otherwise, play **Defect (D)**. This preserves altruistic behavior unless the history proves that the collective group is fundamentally non-cooperative.

*   **Boundary Conditions:**
    *   If $k \le 1$: Since the public good return is less than the private cost, the strategy defaults to **Defect (D)** in all rounds.
    *   If $O_{t-1}$ is always 0: The strategy remains in **Defect (D)** after the first round, effectively minimizing loss while signaling through the occasional Test Phase (as described in the Forgiveness Mechanism) that cooperation is available if the environment improves.

**Pseudocode Summary**

```python
# Constants: n, k, T = ceil(n / k)
# History: O_prev (number of others who cooperated in last round)

if round == 1:
    action = C
elif round == r:
    if average_other_cooperation > (T / (n-1)):
        action = C
    else:
        action = D
elif O_prev >= T:
    action = C
elif was_last_action_D and random() < 0.1: # Forgiveness/Test
    action = C
else:
    action = D
```
'''

description_ALTRUISTIC_4 = '''
Define an altruistic strategy based on a conditional cooperative framework with a forgiveness-focused "tit-for-tat" adaptation, calibrated to the efficiency threshold of the multiplication factor $k$.

**Strategy Initialization (Round 1):**
Play C (Cooperate). This assumes mutual good faith and sets a baseline for establishing a cooperative group outcome.

**General Decision Rule (Rounds $t = 2$ to $r-1$):**
Observe the number of total cooperators in round $t-1$, denoted as $S_{t-1}$. Calculate the "cooperation threshold" $T$ as $n/k$. This threshold represents the minimum number of cooperators required for the group to break even on the public good investment (the point where the marginal benefit of contributing matches the cost).

- If $S_{t-1} \ge T$, play C.
- If $S_{t-1} < T$, play D. This serves as a "punishment" or a withdrawal of contribution when the public good provision is inefficient or being exploited by free-riders.

**Special Case: "Forgiveness" (Round $t$ following a defecting round):**
If the previous round resulted in $S_{t-1} < T$ but the round prior to that ($t-2$) resulted in $S_{t-2} \ge T$, play C. This one-round "probe" tests whether the group is willing to return to cooperation, preventing a permanent lock-in of defection.

**Strategy for the Final Round ($t = r$):**
Play D, regardless of history, *unless* the historical average of cooperators ($S_{avg}$) is consistently high ($S_{avg} > T$). If the group has maintained a high cooperation rate throughout the game, maintain C to maximize the collective social welfare outcome.

**Pseudocode Implementation:**

```
// State variables
S_history = [] // Track total cooperators per round

// Round 1
Action = C

// Rounds 2 to r-1
If S_history[last] >= (n / k):
    Action = C
Else If S_history[last] < (n / k) AND S_history[second_to_last] >= (n / k):
    Action = C // Forgiveness probe
Else:
    Action = D

// Round r
If (Average(S_history) > (n / k)):
    Action = C
Else:
    Action = D
```

**Altruistic Adjustment:**
If at any point the current round $t$ is far from the final round and the total accumulated payoff of the group appears to be trending toward a Pareto-inferior equilibrium, increase the threshold $T$ by a factor of $0.1$ to strictly penalize defection, forcing the group toward the socially optimal outcome (all C) more aggressively.
'''

description_BENEVOLENT_1 = '''
The strategy follows a "Generous Tit-for-Tat with a Trigger-Warning" mechanism, designed to incentivize mutual cooperation while protecting against persistent defectors. It defines benevolence as initiating cooperation and maintaining it as long as the group average remains above a sustainability threshold, but reverting to defection if the group proves exploitative.

### Decision Rules

1. **Round 1 (Initialization):** Always play **Cooperate (C)**. This signals a benevolent intent and attempts to establish a cooperative equilibrium.

2. **Subsequent Rounds (Adaptive Response):** 
   Calculate the Cooperation Threshold, $T = (n - 1) \times (n/k)$. This value represents the minimum number of other players who must cooperate for the act of cooperation to be individually rational (payoff-neutral or better) compared to defection. 

   Define $C_{others}$ as the number of other players who cooperated in the previous round ($C_{others} = \text{Total\_Cooperators} - c_{me, t-1}$).

   *   **If $C_{others} \ge T$:** Play **Cooperate (C)**. The group has met the threshold of sustainability; continue to support the public good.
   *   **If $C_{others} < T$:** Play **Defect (D)**. The group is below the sustainability threshold, making continued cooperation a net loss for the individual. 
   *   **Recovery Exception:** If the strategy is currently defecting, but the previous round resulted in a Total Cooperation count of $\ge T$, switch back to **Cooperate (C)** in the current round to restart the benevolent cycle.

### Last Round Edge Case
In the final round ($r$), regardless of history, play **Defect (D)** if $C_{others} < T$. If the group has maintained $C_{others} \ge T$ consistently (defined as the average of all previous rounds being $\ge T$), play **Cooperate (C)**. This serves as a "good faith" exit in stable environments, while preventing exploitation in the final round of a failing group.

### Pseudocode

```python
# Parameters: n, k, r, history
# T = threshold for individual rationality
T = (n - 1) * (n / k)

def get_action(current_round, history):
    if current_round == 1:
        return 'C'
    
    # Calculate previous round metrics
    prev_total_coop = history.last_round_total_cooperators
    prev_my_action = history.last_round_my_action
    prev_others_coop = prev_total_coop - (1 if prev_my_action == 'C' else 0)

    # Recovery logic: If we were defecting, did the group self-correct?
    if prev_my_action == 'D' and prev_total_coop >= T:
        return 'C'
        
    # Standard threshold logic
    if prev_others_coop >= T:
        return 'C'
    
    # Final Round Logic: Only cooperate if historically stable
    if current_round == r:
        avg_others_coop = mean(history.others_coop_counts)
        return 'C' if avg_others_coop >= T else 'D'

    return 'D'
```
'''

description_BENEVOLENT_2 = '''
Initialize memory of opponent cooperation counts across all previous rounds $t=1$ to $T$. Let $S_{t}$ be the total number of cooperators observed in round $t$. Let $M$ be a target threshold for cooperation, defined as $M = \lceil \frac{n}{k} \rceil$.

**Round 1:**
Play Cooperate (C).

**Intermediate Rounds ($1 < t < r$):**
Calculate the average cooperation level observed in all previous rounds: $\bar{S} = \frac{1}{t-1} \sum_{j=1}^{t-1} S_j$.

If $\bar{S} \geq M - 1$:
Play Cooperate (C).

If $\bar{S} < M - 1$:
Play Defect (D).

*Adjustment for triggering cooperation:* If the total cooperation count in the most recent round $S_{t-1}$ was high enough to suggest a group effort ($S_{t-1} \geq M$), prioritize sustaining this cooperation regardless of the historical average. Play Cooperate (C).

**Final Round ($t = r$):**
If $\bar{S} \geq M - 1$ or $S_{r-1} \geq M$:
Play Cooperate (C).

Else:
Play Defect (D).

**Robustness Rule:**
If at any point the observation $S_{t-1} = 0$, play Defect (D) for the subsequent three rounds to protect against persistent defection, then return to the standard logic above, treating the average as if the defecting rounds had occurred.
'''

description_BENEVOLENT_3 = '''
Play Cooperate (C) in the first round.

For all subsequent rounds $t \in \{2, \dots, r\}$, play Cooperate (C) if and only if the total number of cooperators observed in round $t-1$ meets or exceeds a cooperation threshold $T_t$, where $T_t$ is defined as follows:

1. Let $S_{t-1}$ be the total number of cooperators in round $t-1$.
2. Define the "benevolence trigger" as $S_{t-1} \ge \lceil \frac{n}{k} \rceil$. This threshold represents the break-even point for the group: when $S \ge \frac{n}{k}$, the total utility generated by the public good equals or exceeds the total cost of contribution.
3. If $S_{t-1} \ge \lceil \frac{n}{k} \rceil$, play Cooperate.
4. If $S_{t-1} < \lceil \frac{n}{k} \rceil$, play Defect.

**Edge Cases and Adjustments:**

*   **Final Round:** If $r$ is known, deviate from the conditional logic in the final round $t=r$ only if the cumulative payoff history suggests that defection has been the dominant strategy of opponents. Specifically, if the average number of cooperators over the previous $r-1$ rounds is less than 1, play Defect; otherwise, play Cooperate.
*   **Re-entry (Forgiveness):** If the strategy is currently defecting because $S_{t-1} < \lceil \frac{n}{k} \rceil$, but the opponents increase their contribution in round $t$ such that $S_t \ge \lceil \frac{n}{k} \rceil$, reset the strategy to Cooperate in round $t+1$. This allows for the re-establishment of cooperation if a sufficient number of players attempt to restart the public good.
*   **Tie-breaking:** In any round where $k/n$ is such that the break-even point $\lceil n/k \rceil$ is exactly met, prioritize Cooperation to signal continued benevolent intent.
'''

description_BENEVOLENT_4 = '''
Adopt a Tit-for-Tat variant with a "Forgiving Threshold" mechanism.

**Core Decision Logic:**
Let $C_t$ be the total number of cooperators observed in round $t$. Let $c_{self, t}$ be your action in round $t$, where $c=1$ is Cooperate and $c=0$ is Defect.

*   **Round 1:** Play Cooperate ($c=1$).
*   **Round $t$ (where $1 < t \le r$):**
    *   Calculate the average contribution rate of your opponents in the previous round:
        $\text{Rate}_{t-1} = \frac{C_{t-1} - c_{self, t-1}}{n-1}$
    *   Define the "Benevolent Threshold" ($\tau$) as $\frac{1}{k}$. This is the minimum proportion of cooperators required for universal cooperation to be socially superior to universal defection.
    *   If $\text{Rate}_{t-1} \ge \tau$: Play Cooperate ($c=1$).
    *   If $\text{Rate}_{t-1} < \tau$: Play Defect ($c=0$).

**Special Conditions and Exceptions:**
*   **Forgiveness Rule:** If you are currently defecting due to a previous low turnout, observe the next round. If the average contribution rate $\text{Rate}_{t}$ rises above or equals $\tau$ in any subsequent round, immediately revert to Cooperate ($c=1$) in the following round ($t+1$).
*   **Final Round ($t=r$):**
    *   If $\text{Rate}_{r-1} \ge \tau$, play Cooperate ($c=1$).
    *   Otherwise, play Defect ($c=0$).
*   **Noise/Ambiguity:** If $n=2$, the threshold logic remains robust. If $C_{t-1}$ is ambiguous due to the anonymous nature of the game, rely strictly on the calculated contribution rate of the group aggregate.

**Pseudocode:**

```python
def decide_action(round_number, total_cooperators_prev, last_action, n, k):
    # Parameter Setup
    threshold = 1.0 / k
    
    # Round 1
    if round_number == 1:
        return 1
    
    # Calculate opponent cooperation rate from previous round
    opponent_cooperators = total_cooperators_prev - last_action
    opponent_rate = opponent_cooperators / (n - 1)
    
    # Strategy Decision
    if opponent_rate >= threshold:
        return 1
    else:
        return 0
```
'''

description_SELFISH_1 = '''
The strategy is defined by the following ruleset:

**Round 1:**
Defect.

**Subsequent Rounds:**
Track the history of total contributions from opponents. Define $S_{t-1}$ as the number of cooperators observed in the previous round. Calculate the marginal benefit of cooperation as $\frac{k}{n}$. Calculate the marginal cost of cooperation as $1$. Because $k < n$, the marginal cost (1) always exceeds the marginal benefit ($\frac{k}{n}$), making defection the strictly dominant strategy in any single round.

However, to incentivize opponents to cooperate (thereby increasing the total pool), employ a "Generous Tit-for-Tat" variant based on the total number of cooperators observed.

Let $C_{target} = n-1$ (the total number of opponents). Define the "Cooperation Threshold" $T$ as $T = \lceil \frac{n}{k} \rceil$.

If $t < r$:
- If $S_{t-1} \ge T$, cooperate.
- If $S_{t-1} < T$, defect.

If $t = r$ (Final Round):
Defect.

**Logic:**
The strategy exploits the potential for conditional cooperation among other players. By cooperating only when the number of contributors is high enough to make the collective action profitable (or at least close to break-even relative to the baseline of zero contributions), the agent encourages the emergence of a cooperative cluster. If the aggregate contribution falls below the threshold $T$, the agent reverts to the strictly dominant strategy of defection to minimize personal loss. In the final round, the incentive to maintain the cooperative reputation vanishes, necessitating defection to maximize the terminal payoff.
'''

description_SELFISH_2 = '''
Play defect in the first round (t=1). For subsequent rounds (t > 1), adopt a conditional strategy based on the cooperation level observed in the previous round (t-1).

Let $N_c$ be the number of cooperators observed in round $t-1$.

1.  If $t = r$ (the final round):
    Defect.

2.  If $t < r$:
    If the observed contribution level in $t-1$ satisfies the condition:
    $\frac{k}{n} \times (N_c) > 1$
    Then cooperate. Otherwise, defect.

If $t=1$, always defect. If $N_c$ is unknown (e.g., first round), treat the expectation as 0.

Pseudocode:

```
if round == total_rounds:
    return Defect
if round == 1:
    return Defect

// Strategy Logic
contribution_gain = (k / n) * cooperators_previous_round
if contribution_gain > 1:
    return Cooperate
else:
    return Defect
```
'''

description_SELFISH_3 = '''
The strategy follows a conditional cooperation framework known as "Win-Stay, Lose-Shift" applied to the aggregate contribution level, optimized for personal payoff maximization.

### Decision Rules

Define `T_t` as the total number of cooperators in round `t`, and `C_t` as your own contribution choice (1 for C, 0 for D).

**Round 1:** Always play Defect (D). This establishes a baseline and avoids vulnerability to unilateral cooperation.

**Rounds 2 through `r-1`:**
Calculate the "break-even" threshold `T_threshold = n / k`.
*   If `T_threshold` is not an integer, round up to the nearest integer.
*   If the previous round's total cooperators `T_{t-1}` ≥ `T_threshold`, play Cooperate (C).
*   If `T_{t-1}` < `T_threshold`, play Defect (D).

*Adjustment for your own action:* Because you only observe `T_{t-1}` (which includes your own action), the rule is calibrated to ensure that your own contribution is only provided when the collective behavior is already sufficient to make cooperation profitable for you. Specifically:
*   If you played C in `t-1` and `T_{t-1}` ≥ `T_threshold`, continue with C.
*   If you played D in `t-1` and `T_{t-1}` ≥ `T_threshold - 1` (where your contribution would have pushed the total to or above the threshold), switch to C.

**Last Round (`t = r`):** Always play Defect (D). There is no future round to incentivize others to cooperate, so the dominant strategy is to capture the private endowment without contributing.

### Pseudocode

```python
def get_action(round, total_cooperators_prev, my_action_prev):
    if round == 1:
        return D
    
    if round == r:
        return D
    
    threshold = ceil(n / k)
    
    # Check if cooperation is profitable
    # If I defected, the group count was T_prev. If I switch to C, it becomes T_prev + 1.
    # We cooperate if the resulting group count meets the threshold.
    
    if my_action_prev == C:
        if total_cooperators_prev >= threshold:
            return C
        else:
            return D
    else: # my_action_prev == D
        if (total_cooperators_prev + 1) >= threshold:
            return C
        else:
            return D
```

### Edge Case Handling

1.  **k ≤ 1:** If the parameters allow `k` ≤ 1, the strategy defaults to Defect (D) for all rounds, as cooperation is strictly dominated.
2.  **Threshold > n:** If `ceil(n / k) > n` (which occurs if `k < 1`), the threshold logic will naturally result in never cooperating.
3.  **Fluctuating Cooperation:** If the group's cooperation level oscillates around the threshold, the strategy will defect until the group proves it can sustain the threshold, then participate, and immediately drop out if the group fails to sustain it. This minimizes exposure to "sucker" rounds while aggressively harvesting benefits when the group collaborates.
'''

description_SELFISH_4 = '''
Maintain an internal state variable `cooperation_threshold` (initially set to 1) and a count of total rounds `r`.

**Decision Logic:**

1.  **Terminal Round:** If `current_round == r`, always play **Defect**.

2.  **Initial Round:** If `current_round == 1`, play **Cooperate**.

3.  **Subsequent Rounds:**
    *   Let `C_prev` be the number of cooperators observed in the previous round.
    *   Let `k` be the multiplication factor and `n` be the number of players.
    *   Assess the "Return on Cooperation" (ROC) of the previous round:
        *   Calculate the average contribution payoff: `ROC = k / n`.
        *   Calculate the net gain of cooperating versus defecting in the previous round: `Net_Gain = (k/n * C_prev) - 1`.
    *   Calculate the probability of cooperation required for a net positive return:
        *   The break-even point for cooperation is when `(k/n) * C_total = 1`, or `C_total = n/k`.
        *   Update `cooperation_threshold = ceil(n / k)`.

    *   Decision Rule:
        *   If `C_prev >= cooperation_threshold`, play **Cooperate**.
        *   If `C_prev < cooperation_threshold`, play **Defect**.

4.  **Edge Case Recovery (Trigger Strategy):**
    *   If you played **Defect** in the previous round and the observed `C_prev` is greater than or equal to `cooperation_threshold`, switch back to **Cooperate** in the current round with a probability of 0.5 (to test for renewed cooperation from the pool without remaining stuck in mutual defection). If the test succeeds (i.e., `C_prev` remains high), continue to **Cooperate**; if it fails, resume **Defect**.
'''

description_SELFINTERESTED_1 = '''
The strategy, titled "Conditional Tit-for-Tat with Defection Threshold," operates on the principle of conditional cooperation while maintaining a preemptive exit strategy to avoid exploitation.

**Initialization and First Round**
In round 1, play Cooperate (C). This establishes a cooperative baseline and allows the strategy to gauge the aggregate willingness of the group to contribute.

**Round 2 through Round (r-1)**
For all subsequent rounds up to the penultimate round, base the decision on the aggregate cooperation observed in the previous round (let $S_{t-1}$ be the total number of cooperators observed in round $t-1$):

1. **Calculate Threshold**: Define the break-even threshold, $T$, as the minimum number of cooperators required for a Cooperator to earn at least as much as a Defector. Since the payoff for C is $(k/n) \times S$ and the payoff for D is $1 + (k/n) \times S_{others}$, the break-even point is where $(k/n) \times S = 1 + (k/n) \times (S-1)$. Solving this, $T = n/k$.
2. **Conditional Rule**: 
   - If $S_{t-1} \ge \lceil n/k \rceil$, play Cooperate (C).
   - If $S_{t-1} < \lceil n/k \rceil$, play Defect (D).
3. **Adjustment**: If you played D in the previous round, you remain in a "probationary" state. In the next round, if the group cooperation $S_{t-1}$ reaches $\lceil n/k \rceil$, play Cooperate (C) to signal a return to cooperative equilibrium.

**The Penultimate Round (r-1)**
In the second-to-last round, maintain the conditional rule based on $S_{r-2}$. However, if $S_{r-2}$ was below the threshold $\lceil n/k \rceil$, play Defect (D) to safeguard assets against the imminent final-round defection.

**The Final Round (r)**
Play Defect (D). Regardless of past cooperation, the final round removes the incentive for future reciprocity. Defecting in the final round provides the maximum guaranteed payoff without risk of retaliation.

**Pseudocode Summary**

```python
def decide_action(round_number, total_round_cooperators, n, k):
    # n: total players, k: multiplication factor
    threshold = ceil(n / k)
    
    # Final round: always defect
    if round_number == r:
        return 'D'
    
    # First round: cooperate
    if round_number == 1:
        return 'C'
        
    # Conditional logic
    if total_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_2 = '''
The strategy employs a conditional trigger-based mechanism with a learning rate, formalized as follows:

**Initial Phase (Round 1):**
Play Cooperate (C).

**Decision Rule for Rounds 2 to r-1:**
Let $S_t$ be the total number of cooperators observed in the previous round $t-1$.
Let $n$ be the number of players and $k$ be the multiplication factor.

1.  Calculate the Threshold for Cooperation: $T = n / k$.
2.  If $S_t \ge T$, continue to cooperate.
3.  If $S_t < T$, switch to Defect (D) for the current round.
4.  If the strategy is currently Defecting, check if $S_t \ge T$ for three consecutive rounds. If this condition is met, perform a "test" by playing Cooperate (C) for one round to re-evaluate opponent behavior.

**Terminal Phase (Round r):**
Always Defect (D).

**Edge Case Logic:**
*   If $S_t = n$ (all players cooperate), maintain Cooperation regardless of $T$.
*   If the strategy was Defecting and observed $S_t = T$ (or higher) in the immediately preceding round, it immediately reverts to Cooperation (C).
*   If the number of players $n$ or factor $k$ results in a non-integer threshold $T$, round up to the nearest integer for $T$.
'''

description_SELFINTERESTED_3 = '''
Initialize a memory variable `cooperation_threshold` at 0.5. Initialize a history variable `total_rounds_played` at 0.

In round 1:
Contribute (Cooperate).

In rounds 2 through `r-1`:
Observe the total number of cooperators `C_t` from the previous round. Calculate the average cooperation rate of the group: `avg_C = C_t / n`.
- If `avg_C` ≥ `cooperation_threshold`, play Cooperate.
- If `avg_C` < `cooperation_threshold`, play Defect.
- Update `cooperation_threshold` based on the success of the previous round: if `avg_C` resulted in a higher payoff than the previous round's payoff, slightly lower the threshold (multiply by 0.95); if it resulted in a lower payoff, slightly raise the threshold (multiply by 1.05, capping at 0.9).

In the final round `r`:
Play Defect.

*Pseudocode logic for decision rules:*

```
def choose_action(round_number, n, r, prev_cooperators):
    if round_number == 1:
        return Cooperate
    
    if round_number == r:
        return Defect

    avg_C = prev_cooperators / n
    
    if avg_C >= cooperation_threshold:
        return Cooperate
    else:
        return Defect
```
'''

description_SELFINTERESTED_4 = '''
The strategy employs a conditional cooperative approach (Tit-for-Tat variant) with a defection trigger for the terminal round.

**Decision Rules**

In the first round, play C (Cooperate).

For every round t where 1 < t < r:
1. Calculate the contribution rate of others from the previous round (t-1). Let S(t-1) be the total cooperators in the previous round.
2. If you cooperated in round t-1:
    - Cooperation threshold = n - 1 (all others cooperated).
    - If S(t-1) == n, continue to play C.
    - If S(t-1) < n, switch to D (Defect).
3. If you defected in round t-1:
    - Check for recovery: If S(t-1) == n - 1 (everyone else cooperated while you defected), assume the group is willing to sustain cooperation; switch to C.
    - Otherwise, maintain D.

In the final round (t = r):
Always play D (Defect), regardless of previous history.

**Edge Cases and Logic**

*   **First Round:** Initiate with C to signal willingness to participate in the public good, establishing potential for mutual cooperation.
*   **Defection Sensitivity:** The strategy is strictly punitive. If the total number of cooperators falls below the maximum possible (indicating at least one defector among the opponents), the strategy immediately defects to avoid being exploited by free-riders.
*   **Recovery Logic:** If you were defecting (perhaps due to others' previous defection) and the data shows that the rest of the group is cooperating (S(t-1) = n - 1), you switch back to C to re-establish the cooperative equilibrium. This prevents infinite defection loops caused by single-round noise or isolated incidents.
*   **Terminal Round:** Because the game ends at round r, there is no future shadow of the future to enforce cooperation. Any contribution in round r is a pure loss. Therefore, D is the only dominant, self-interested choice.
'''

description_OPPORTUNISTIC_1 = '''
Play according to a "Generous Trigger with Defection Horizon" strategy:

**Decision Rules:**

1.  **Initial Phase (Round 1):** Play Cooperate (C). This establishes a cooperative baseline to signal potential for mutual gain.

2.  **Tracking Mechanism:** Maintain a variable `avg_cooperation` representing the historical average contribution rate of all other players (total cooperators minus your own contribution, divided by `n-1`, averaged across all previous rounds).

3.  **Active Rounds (Round 2 to R-1):**
    *   If `avg_cooperation` > `1/k`, play Cooperate (C). This threshold identifies a group contribution level that yields a positive expected return on investment for all participants.
    *   If `avg_cooperation` ≤ `1/k`, play Defect (D). This punishes free-riding and minimizes loss when the collective contribution is insufficient to generate a profit.

4.  **Terminal Phase (Round R):** Play Defect (D). Since there are no future interactions to sustain cooperation, exploit the final round to maximize individual payoff regardless of historical performance.

**Edge Cases and Adjustments:**

*   **Sudden Collapse:** If the observed number of cooperators drops to zero in any round `t < R`, immediately switch to Defect (D) for the remainder of the game, regardless of previous averages.
*   **Multiplier Sensitivity:** If `k` is very close to `n` (making the public good highly efficient), prioritize cooperation. If `k` is very close to 1 (making the public good barely profitable), lower the `avg_cooperation` threshold to `1/(k-0.1)` to be more selective, preventing exploitation by minimal contributors.
*   **Recovery:** If the strategy is currently defecting due to poor history, attempt to "test" the water by playing Cooperate (C) every 5th round. If the number of other cooperators increases following this test, revert to conditional cooperation rules; if not, continue defecting.
'''

description_OPPORTUNISTIC_2 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Dampening**

The strategy maintains a state variable `trust_level` initialized to 0.5, representing the estimated propensity of the collective group to cooperate. In each round `t`, the decision is based on whether the expected marginal return of cooperation exceeds the certain return of defection, adjusted by a forgiveness decay factor.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)** to initiate cooperation and signal readiness to contribute.

2.  **Rounds 2 to R-1:**
    *   Calculate `cooperation_threshold = n / k`.
    *   Let `C_prev` be the number of cooperators observed in round `t-1`.
    *   Update `trust_level` using an exponential moving average: `trust_level = (0.7 * trust_level) + (0.3 * (C_prev / (n-1)))`.
    *   If `C_prev >= cooperation_threshold`, play **Cooperate (C)**.
    *   Else if `C_prev < cooperation_threshold` AND `trust_level > 0.4`, play **Cooperate (C)** as a test to see if cooperation can be restored.
    *   Otherwise, play **Defect (D)** to protect payoff against a non-cooperative environment.

3.  **Round R (The Final Round):**
    *   Play **Defect (D)** regardless of history. There is no future round to incentivize or punish, making defection the dominant strategy to maximize the final round payoff.

**Pseudocode Implementation:**

```python
# Parameters: n, k, r
# State: trust_level = 0.5

def select_action(round_number, n, k, history):
    if round_number == 1:
        return 'C'
    
    if round_number == r:
        return 'D'
    
    # Observe previous round cooperators (excluding self)
    # If I played C in t-1, C_prev = observed_coop - 1
    # If I played D in t-1, C_prev = observed_coop
    c_prev = calculate_previous_cooperators(history[-1]) 
    
    # Update trust
    trust_level = (0.7 * trust_level) + (0.3 * (c_prev / (n - 1)))
    
    threshold = n / k
    
    if c_prev >= threshold:
        return 'C'
    elif trust_level > 0.4:
        return 'C'
    else:
        return 'D'
```

**Opportunistic Edge Case Handling:**

*   **Sudden Defection:** If the group collapses (high defection) but `trust_level` remains artificially high, the strategy immediately defaults to **Defect (D)** if `C_prev` is significantly below the `threshold`, ensuring protection against free-riders while keeping a buffer for transient noise.
*   **Multiplier Sensitivity:** As `k` approaches `n`, the `cooperation_threshold` decreases, making the strategy more lenient and willing to cooperate with fewer partners. As `k` approaches 1, the `cooperation_threshold` increases, making the strategy more aggressive and likely to defect.
'''

description_OPPORTUNISTIC_3 = '''
Play C in Round 1.

In all subsequent rounds t > 1, calculate the payoff difference Δπ between cooperating and defecting based on the number of cooperators observed in round t-1, denoted as C_{t-1}. 

Let C_{t-1} be the total number of cooperators in the previous round. 
The observed number of opponents who cooperated is O_{t-1} = C_{t-1} - 1 (if I cooperated) or C_{t-1} (if I defected).

The strategy relies on a "Tit-for-Tat with Trend Analysis" mechanism:

1.  **Condition for Continued Cooperation:** 
    Cooperate in round t if:
    a) (k/n) * (C_{t-1} + 1) > 1 
    AND 
    b) The trend of cooperation is non-decreasing: C_{t-1} ≥ C_{t-2}.

2.  **Condition for Opportunistic Defection:**
    Defect in round t if:
    a) (k/n) * (C_{t-1} + 1) ≤ 1 (the public good return is insufficient to justify personal cost), OR
    b) C_{t-1} < C_{t-2} (indicates opponents are defecting or the group is unreliable), OR
    c) t = r (last round defection maximizes individual payoff as there is no future interaction to penalize).

3.  **Recovery Protocol:**
    If the strategy defected in t-1 but C_{t-1} remains high (specifically C_{t-1} > n * (1/k)), reset to C in the next round to test if the group will sustain a high-contribution equilibrium.

Pseudocode:

```python
if t == 1:
    return Cooperate
if t == r:
    return Defect

prev_cooperators = history[t-1].total_cooperators
prev_prev_cooperators = history[t-2].total_cooperators

# Calculate marginal benefit of contributing
marginal_benefit = (k / n) * (prev_cooperators + 1)

# Check for sustainability
is_profitable = marginal_benefit > 1
is_stable = prev_cooperators >= prev_prev_cooperators

if is_profitable and is_stable:
    return Cooperate
else:
    return Defect
```
'''

description_OPPORTUNISTIC_4 = '''
**Strategy: Tit-for-Tat with Conditional Forgiveness (TTCF)**

**1. Initialization**
*   **Round 1:** Cooperate (C). This establishes a cooperative baseline to test opponent behavior.

**2. Decision Rules (Rounds 2 to r-1)**
Define "cooperation threshold" *T* as the minimum number of cooperators required in the previous round to justify continued cooperation.
*   *T* = ceil(n * (1 / (k - 1))) - 1 (or n - 1 if the calculation exceeds n). This threshold ensures that the expected payoff of cooperating is at least equal to the payoff of defecting, assuming reciprocal behavior from others.
*   **Rule:** If the number of cooperators in round *t-1* is ≥ *T*, play C.
*   **Rule:** If the number of cooperators in round *t-1* is < *T*, play D.

**3. Opportunistic Adjustment**
*   If the strategy defected in the previous round due to the threshold rule, it enters "Probe Mode" once every *m* rounds (where *m* = 3), playing C to test if the group has returned to a cooperative state. If the probe results in a cooperative count ≥ *T*, return to the standard cooperation rule.

**4. End-Game Strategy (Final Round)**
*   **Round r:** Defect (D). Regardless of previous history, unconditionally defect in the final round to maximize individual payoff, as there is no future shadow of the future to enforce cooperation.

**5. Pseudocode Implementation**

```python
# Parameters: n (players), r (rounds), k (multiplier)
# Variables: history (list of coop counts per round)

T = ceil(n / (k - 1)) - 1

def decide_action(round_number, history):
    # Final Round
    if round_number == r:
        return 'D'
    
    # First Round
    if round_number == 1:
        return 'C'
    
    # Standard Adaptive Logic
    last_coop_count = history[-1]
    
    # Probe Logic: If previously defected, check for cooperation every 3 rounds
    if last_coop_count < T:
        if (round_number % 3 == 0):
            return 'C'
        else:
            return 'D'
            
    # Default logic
    return 'C' if last_coop_count >= T else 'D'
```
'''

description_INDIVIDUALISTIC_1 = '''
Adopt a conditional cooperative strategy based on a trigger-threshold mechanism, designed to maximize individual payoff by balancing the exploitation of defectors with the cultivation of cooperative cycles.

**Decision Rules**

In each round *t*, let *S_t* be the total number of cooperators observed in the previous round *t-1*, excluding yourself.

1.  **First Round (t=1):** Play Cooperate (C). This establishes a signal of potential cooperation to influence future aggregate behavior.
2.  **Subsequent Rounds (t > 1 and t < r):** 
    *   Calculate the "Cooperation Threshold" *T* where cooperation becomes individually profitable: *T = n / k*. 
    *   If *S_{t-1}* ≥ *T*, play Cooperate (C). You are in a cooperative equilibrium where the group size sustains the public good.
    *   If *S_{t-1}* < *T*, play Defect (D). The group is failing to produce sufficient value, and individual contribution would yield a lower payoff than defection.
3.  **Last Round (t = r):** Always play Defect (D). Since there are no future rounds to influence, there is no strategic benefit to cooperation, and defection serves as the dominant strategy to maximize the final round payoff.

**Adaptive Logic**

The strategy effectively functions as a "Tit-for-Tat" variant scaled for N-players. By observing the aggregate cooperation level *S_{t-1}*, the strategy dynamically switches between enforcement (punishing defectors by defecting) and cooperation (rewarding contributors).

*   **Failure Recovery:** If *S_{t-1}* < *T* and you play Defect, but the group returns to *S_t* ≥ *T* in the next round, immediately resume Cooperation (C) in round *t+1*.
*   **Edge Case - Ambiguity:** If *S_{t-1}* is exactly equal to *T* (if *T* is an integer), treat this as sufficient cooperation and play C.

**Logic Pseudocode**

```python
def decide_action(round, r, n, k, history):
    if round == r:
        return 'D'
    
    if round == 1:
        return 'C'
    
    threshold = n / k
    # S_prev is the number of cooperators observed in the previous round
    # If I cooperated in round-1, S_prev = total_cooperators - 1
    # If I defected in round-1, S_prev = total_cooperators
    S_prev = calculate_S_prev(history[round-1])
    
    if S_prev >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_2 = '''
**Strategy: Conditional Tit-for-Tat with Defection Threshold (CTFT-DT)**

**1. Decision Rules**

The strategy relies on a dynamic threshold of cooperation required from the group to justify further cooperation. Let $C_t$ be the number of cooperators observed in round $t$.

*   **Round 1:** Play **Cooperate (C)**.
*   **Subsequent Rounds ($t > 1$):**
    *   Calculate the "Break-Even Cooperation Threshold" ($T_{be}$):
        $T_{be} = \lceil \frac{n}{k} \rceil$
        *(This is the minimum number of cooperators required in the previous round for the public good benefit of cooperation to equal or exceed the private benefit of defection.)*

    *   **Condition:** If $C_{t-1} \ge T_{be}$, play **Cooperate (C)**.
    *   **Condition:** If $C_{t-1} < T_{be}$, play **Defect (D)**.

**2. Edge Case Handling**

*   **Last Round ($t = r$):** Override all previous conditional logic and play **Defect (D)**. Since there are no future rounds to influence, the individual payoff is strictly maximized by keeping the endowment.
*   **The "Rebound" Exception:** If the strategy has defected in round $t-1$ because $C_{t-2} < T_{be}$, but wishes to test if cooperation is viable again, implement a "Probing" rule:
    *   If $t < r - 1$ AND $C_{t-1} = 0$: Play **Defect (D)**.
    *   If $t < r - 1$ AND $C_{t-1} > 0$: Play **Cooperate (C)** with probability $P = \frac{C_{t-1}}{n}$. If random roll $> P$, play **Defect (D)**. This "soft" re-entry prevents being exploited by perpetual defectors while attempting to restart cooperation if the group shows activity.

**3. Logic Summary (Pseudocode)**

```
if t == r:
    return D

if t == 1:
    return C

T_be = ceil(n / k)

if C_{t-1} >= T_be:
    return C

else:
    # Attempt probabilistic probe if the group shows any activity
    if C_{t-1} > 0 and random() < (C_{t-1} / n):
        return C
    else:
        return D
```
'''

description_INDIVIDUALISTIC_3 = '''
### Strategy: Conditional Reciprocity with Tit-for-Tat Threshold

**Initial Round (t=1):**
Cooperate (C). This establishes a baseline of cooperation and assesses the aggregate contribution level of the opponent pool.

**Subsequent Rounds (t > 1):**
Calculate the cooperation threshold required to break even versus defecting. A contribution is rational if the expected return from the public good exceeds the individual private payoff. Define the "Cooperation Threshold" ($T$) as the minimum number of cooperators ($C_{total}$) required such that cooperating is at least as profitable as defecting. 

Given $\pi_C = (k/n) \times C_{total}$ and $\pi_D = 1 + (k/n) \times (C_{total}-1)$ (assuming you are the only one changing behavior), cooperating is profitable when:
$(k/n) \times C_{total} \ge 1 + (k/n) \times (C_{total}-1)$
$(k/n) \times C_{total} \ge 1 + (k/n) \times C_{total} - k/n$
$0 \ge 1 - k/n$
$k/n \ge 1$, which is impossible given the constraint $1 < k < n$.

Because the dominant strategy in any single round is always to Defect (D), cooperation is only viable as a conditional mechanism to incentivize others. Therefore, employ the following adaptive rule:

1.  **Observe:** In round $t-1$, let $C_{t-1}$ be the total number of cooperators observed.
2.  **Calculate Reciprocity:** Determine the "Cooperation Ratio" ($R$) defined as $C_{t-1} / n$.
3.  **Threshold Decision:**
    *   If $R \ge 0.5$ (or a calibrated threshold based on $k/n$): Cooperate (C).
    *   If $R < 0.5$: Defect (D).

**Edge Cases:**
*   **The Final Round (t = r):** Defect (D). Since there are no subsequent rounds to sustain a reputation or punish defection, the incentive for cooperation vanishes entirely.
*   **Persistent Defection:** If the system observes $C_{t-1} = 0$ for two consecutive rounds, switch to Defect (D) for all remaining rounds, as the opponent pool is structurally incapable or unwilling to coordinate.
*   **Unexpected Defection:** If $C_{t-1}$ drops significantly (e.g., by more than 50% relative to the previous round), immediately Defect (D) in round $t$ to prevent exploitation, then revert to the threshold decision for round $t+1$.
'''

description_INDIVIDUALISTIC_4 = '''
**Initialization Phase (Round 1):**
Play Cooperate (C).

**Standard Phase (Rounds 2 to r-1):**
Let $C_t$ be the number of cooperators observed in the previous round, and $c_{i,t}$ be your action in the previous round (1 for C, 0 for D).

1.  If $C_t = n$: Continue to play Cooperate (C).
2.  If $C_t < n$ and $c_{i,t} = 1$: If $C_t \ge \frac{n}{k}$, play Cooperate (C); otherwise, switch to Defect (D).
3.  If $C_t < n$ and $c_{i,t} = 0$: If $C_t \ge \frac{n}{k}$, play Cooperate (C); otherwise, continue to Defect (D).

**Termination Phase (Round r):**
If $C_{r-1} = n$, play Cooperate (C). Otherwise, play Defect (D).

**Edge Case Handling:**
*   **Threshold Trigger:** If at any point the total number of cooperators $C_t$ falls below the threshold $n/k$ (the point where the marginal benefit of your contribution is less than the cost), immediately switch to Defect (D) for all subsequent rounds, regardless of your previous action.
*   **Recovery:** If you are in a state of Defect (D) due to low cooperation, check the opponent cooperation count $C_t$ in each round. If $C_t$ increases to $n-1$ (suggesting a potential collective effort to restore cooperation), play Cooperate (C) in the next round to signal willingness to re-engage in mutual cooperation.
'''
