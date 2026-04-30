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

description_COLLECTIVE_5 = '''
**Strategy: Conditional Tit-for-Tat with Forgiving Reciprocity**

This strategy operates on the principle of conditional cooperation, seeking to maximize the public good while protecting against exploitation. It relies on a history-tracking variable $C_{observed}$, which stores the number of cooperators observed in the previous round.

**Initialization and Constants:**
*   $T$: Current round number ($1 \le T \le r$).
*   $k/n$: Marginal per capita return (MPCR).
*   $Threshold$: The minimum number of cooperators required to justify continued cooperation. Calculate $Threshold = \lceil n/k \rceil$. If $Threshold > n$, set $Threshold = n$ (as cooperation is never rational if even unanimous cooperation yields less than defecting).

**Decision Rules:**

1.  **Round 1:** Play Cooperate (C). Initiate the partnership with trust.

2.  **Rounds 2 to $r-1$:**
    *   If $C_{observed} \ge Threshold$: Play Cooperate (C).
    *   If $C_{observed} < Threshold$: Play Defect (D).
    *   *Forgiveness Clause:* If you previously played Defect (D) due to insufficient cooperation, switch back to Cooperate (C) if the group returns to $C_{observed} \ge Threshold$.

3.  **Final Round ($r$):**
    *   If $C_{observed}$ in round $r-1$ was $\ge Threshold$: Play Cooperate (C).
    *   If $C_{observed}$ in round $r-1$ was $< Threshold$: Play Defect (D).

**Pseudocode:**

```python
def decide_action(round, total_players, k, history):
    threshold = ceil(total_players / k)
    
    # First round initialization
    if round == 1:
        return 'C'
        
    # Check previous round's performance
    prev_cooperators = history.last_round_cooperators
    
    # Strategy logic
    if prev_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Small Groups/Low Returns:** If $k/n \le 1/n$ (i.e., $k \le 1$), the dominant strategy is always Defect (D) because the individual cost of contributing exceeds the individual benefit. In this scenario, play Defect (D) in every round.
*   **Zero Cooperation:** If $C_{observed}$ is 0, maintain Defect (D) until the start of the next opportunity to signal, but prioritize safety by reverting to Defect (D) permanently if the group fails to meet the $Threshold$ for more than three consecutive rounds.
'''

description_COLLECTIVE_6 = '''
**Strategy: Conditional Tit-for-Tat with Forgiving Defection**

**Initialization (Round 1):**
Play Cooperate (C). This establishes a baseline for reciprocal cooperation without risking immediate exploitation.

**Decision Rules (Rounds 2 to r-1):**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
1.  **Strict Reciprocity:** If $C_{t-1} \ge \tau$, play C. If $C_{t-1} < \tau$, play Defect (D).
    *   The threshold $\tau$ is defined as $\lceil n \times (1/k) \rceil$. This threshold represents the minimum number of cooperators required for the collective payoff of a cooperator to be greater than or equal to the payoff of a defector in that round.
2.  **Forgiveness Mechanism:** If the strategy previously played D because $C_{t-1} < \tau$, but the *current* round observation shows $C_{t-1} \ge \tau$, revert to playing C immediately. This allows for the restoration of cooperation if the population returns to a mutually beneficial state.

**Terminal Phase (Round r):**
1.  If the strategy has consistently played C for the last $m$ rounds (where $m = \min(3, r-1)$), play C.
2.  If the strategy has defected at any point in the last $m$ rounds, continue to play D.
    *   This prevents end-of-game exploitation by defecting agents while maintaining cooperation with stable partners.

**Edge Cases:**
*   **Observation Noise/Ambiguity:** If $n$ is large and observation is aggregated, assume the strategy is operating in a population where individual identification is impossible. Rely solely on the aggregate threshold $\tau$.
*   **Low $k$ values:** If $k$ is extremely close to 1, such that the threshold $\tau$ approaches $n$, the strategy effectively becomes "Always Defect" unless full cooperation is observed. This is mathematically optimal to avoid the "sucker's payoff."
*   **Early Defection:** If the strategy detects that the threshold $\tau$ is never met in the first two rounds, switch permanently to D for the remainder of the game to minimize total losses.
'''

description_COLLECTIVE_7 = '''
### Strategy: Conditional Reciprocal Contribution (CRC)

The strategy operates on the principle of conditional cooperation, maintaining a baseline of cooperation as long as the aggregate contribution levels remain viable, and transitioning to defection to avoid exploitation or when cooperation no longer serves the collective outcome.

#### Decision Rules
Define $T$ as the current round index, $r$ as total rounds, $N$ as the number of players, $C_t$ as the total number of contributors in the previous round, and $k$ as the multiplication factor.

**Round 1:**
Always play $C$ (Cooperate) to initiate a cooperative equilibrium.

**Rounds 2 to $r-1$:**
Assess the contribution rate of the group from the previous round ($C_{t-1}$).
*   **Case 1 (High Cooperation):** If $(C_{t-1} / N) > (1/k)$, play $C$. This threshold represents the break-even point where the marginal benefit of contributing equals the cost.
*   **Case 2 (Low Cooperation):** If $(C_{t-1} / N) \le (1/k)$, play $D$ (Defect). This serves to punish free-riders and minimize personal loss when the collective effort is mathematically insufficient to yield a net positive return.
*   **Case 3 (Recovery Mechanism):** If the strategy is currently playing $D$ due to Case 2, and the previous round's cooperation rate $C_{t-1}$ meets or exceeds the threshold $(1/k)$ (indicating that other players may have attempted to restart cooperation), switch back to $C$ with a probability of 0.5 to test the environment without committing to immediate, permanent exploitation.

**Round $r$ (Final Round):**
Play $D$ regardless of previous outcomes. Since the game terminates, there is no future incentive for others to maintain cooperation or for the group to sustain a high-performing equilibrium, rendering the final contribution a net loss.

#### Pseudocode
```python
def get_action(round_number, total_rounds, n, k, prev_cooperators):
    # Rule for the final round
    if round_number == total_rounds:
        return 'D'

    # Rule for the first round
    if round_number == 1:
        return 'C'

    # Assessment logic for interim rounds
    threshold = n / k  # Inverse of (k/n)
    
    if prev_cooperators >= threshold:
        return 'C'
    else:
        # Check for recovery: if opponents attempted cooperation, 
        # try to re-enter cooperation
        if prev_cooperators >= threshold:
             return 'C' 
        return 'D'
```

#### Edge Cases
*   **Insufficient Data (Round 1):** Default to $C$ to seed cooperation.
*   **Sudden Defection:** If the system is cooperating and $C_{t-1}$ drops sharply below the threshold, the strategy immediately switches to $D$ for the subsequent round to prevent exploitation.
*   **Termination:** The strategy strictly enforces defection on the final round to negate the possibility of being the sole contributor in a round where no future benefits can be realized.
'''

description_COLLECTIVE_8 = '''
Adopt a "Generous Tit-for-Tat with Forgiveness" strategy based on the observed contribution rate of the group.

**Strategy Logic**

1.  **First Round:** Play **Cooperate (C)**. Establish initial trust.

2.  **Subsequent Rounds (t=2 to r-1):** Calculate the previous round’s contribution rate, $R_{t-1} = \frac{\sum c_j}{n}$.
    *   **Reciprocate:** If $R_{t-1} \ge \tau$, play **Cooperate (C)**.
    *   **Punish:** If $R_{t-1} < \tau$, play **Defect (D)**.
    *   **Threshold ($\tau$):** Set the threshold $\tau = 1/k$. This ensures cooperation remains profitable for the group by incentivizing a contribution level that recovers at least the cost of the endowment.
    *   **Forgiveness:** If previously defecting due to low group cooperation, switch back to **Cooperate (C)** if the group's cooperation rate $R$ meets or exceeds $\tau$ for two consecutive rounds. This breaks deadlock cycles created by mutual defection.

3.  **Final Round (t=r):** Defect (D) unconditionally. In a finite, repeated game, the incentive to cooperate vanishes in the terminal period as there is no future round to punish or reward behavior, and the dominant strategy is to maximize the final round payoff.

**Edge Cases & Adjustments**

*   **Low-k environments ($k \approx 1$):** If the incentive to cooperate is extremely marginal, reduce the forgiveness requirement to a single round. If $R_{t-1} \ge \tau$ after one round of defection, immediately return to **Cooperate (C)**.
*   **Persistent Defection:** If the group's cooperation rate $R_t$ remains consistently below the threshold $\tau$ for more than $r/3$ rounds, switch to **Defect (D)** for the remainder of the game to prevent exploitation by non-cooperative agents.
*   **Observation Noise:** Treat any observed cooperation rate as valid. Do not assume collusion; respond only to the aggregate data provided by the game mechanism.
'''

description_COLLECTIVE_9 = '''
The strategy utilizes a conditional "Win-Stay, Lose-Shift" logic extended to incorporate a "Tit-for-Tat" cooperative threshold, balanced against the finite time horizon of the game.

### Round 1: Initialization
Cooperate (C).

### Rounds 2 to r-1: Conditional Reciprocity
Define `k_threshold = n / k` as the number of cooperators required to make cooperation individually rational (i.e., where contributing yields a payoff equal to or greater than defecting).

Calculate `C_total(t-1)`, the total number of cooperators observed in the previous round.

1.  **Strict Reciprocity:** If `C_total(t-1) >= k_threshold`, Cooperate (C).
2.  **Defection Response:** If `C_total(t-1) < k_threshold`, Defect (D).
3.  **Exception:** If `C_total(t-1)` is zero, Defect (D) to avoid exploitation.

### Round r: Final Round Defection
Defect (D) unconditionally.

### Pseudocode Representation
```python
# Constants: n, k, r
# k_threshold = n / k

def strategy(round, history):
    if round == 1:
        return 'C'
    
    if round == r:
        return 'D'
    
    previous_cooperators = history[round - 1]
    
    if previous_cooperators >= k_threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_COLLECTIVE_10 = '''
### Strategy: Tit-for-Tat Trigger with Threshold Conditioning

**Initialization (Round 1):**
Play C (Cooperate). This initiates cooperation and signals a collective-benefit mindset.

**Subsequent Rounds (t > 1 and t < r):**
Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
Let $T_{t-1} = C_{t-1} - 1$ be the number of cooperators excluding the self (if you cooperated) or $C_{t-1}$ (if you defected).

1.  **If $T_{t-1} > \frac{n}{k}$:** Play C (Cooperate). If the aggregate contribution of others in the previous round exceeds the critical threshold required to make cooperation individually rational (recovering the endowment), continue to cooperate.
2.  **If $T_{t-1} \le \frac{n}{k}$:** Play D (Defect). If the aggregate contribution of others falls below the threshold, switch to Defect. This serves as a punishing mechanism to deter free-riding and prevents loss of endowment.
3.  **Recovery Clause:** If playing D, check if $T_{t-1} > \frac{n}{k}$ in any subsequent round. If the population returns to a level where cooperation is rational, revert to C.

**Final Round (t = r):**
Play D (Defect). Since there is no future interaction to incentivize cooperation or punish defection, the dominant strategy for the final round is to maximize payoff by defecting, regardless of previous rounds.

**Pseudocode Summary:**
```python
if round == r:
    return D

if round == 1:
    return C

# Calculate contributions of others (excluding self)
if last_action == C:
    others_contributions = observed_total_cooperators - 1
else:
    others_contributions = observed_total_cooperators

# Threshold Condition: k/n * (others + 1) >= 1  => others >= n/k - 1
threshold = (n / k) - 1

if others_contributions >= threshold:
    return C
else:
    return D
```
'''

description_COLLECTIVE_11 = '''
### Strategy: Adaptive Tit-for-Tat with Threshold Reciprocity

**1. Round 1 (Initial State):**
Start by playing **Cooperate (C)** to initiate cooperative behavior.

**2. Standard Rounds (Round 2 to Round r-1):**
Observe the total number of cooperators from the previous round, $S_{t-1}$. Calculate the number of other players who cooperated, $O_{t-1} = S_{t-1} - c_{t-1}$.

*   **Cooperate if:** $O_{t-1} \ge \lfloor \frac{(n-1) \times k}{n} \rfloor$. This threshold represents the minimum number of contributors required for the marginal gain of cooperation to equal or exceed the marginal gain of defection. 
*   **Defect if:** $O_{t-1} < \lfloor \frac{(n-1) \times k}{n} \rfloor$.

If the calculation yields a threshold of zero or less, default to **Cooperate**.

**3. Final Round (Round r):**
Regardless of previous history or calculation, play **Defect (D)**. This prevents exploitation by opponents attempting to maximize their final round payoff by defecting while relying on cooperative participants.

**4. Edge Case Handling:**
*   **Total Defection:** If $S_{t-1} = 0$, play **Defect (D)** for the subsequent round. Continue to defect until the group average of cooperation rises above the threshold defined in step 2.
*   **Fluctuation Handling:** If the group behavior is volatile (switching between C and D frequently), prioritize the **Defect (D)** action to avoid consistent losses.
*   **Fixed Parameter Scaling:** The decision threshold $\lfloor \frac{(n-1) \times k}{n} \rfloor$ automatically adjusts to the specific $n$ and $k$ values of the game session, ensuring alignment with the payoff structure's breakeven point.
'''

description_COLLECTIVE_12 = '''
### Initial Phase (Round 1)
Begin by playing **Cooperate (C)**. This establishes a baseline of cooperation to signal willingness to participate in a mutually beneficial outcome, regardless of the expected behavior of anonymous opponents.

### Monitoring Phase (Rounds 2 to r-1)
In each subsequent round `t` (where 1 < t < r), evaluate the aggregate behavior of the group from round `t-1`.

Let `C_prev` be the number of cooperators in the previous round.
1.  **Strict Conditional Reciprocity:** Calculate the net impact of the previous round's cooperation on individual payoffs. Compare `C_prev` against a threshold `T = n/k`. 
    *   If `C_prev >= T`: Continue to **Cooperate (C)**. The group behavior is generating sufficient public good to offset the cost of individual contribution.
    *   If `C_prev < T`: Switch to **Defect (D)**. When the group contribution level fails to provide a positive return on investment for the cooperator, the strategy shifts to protect the endowment until group behavior improves.

2.  **Forgiveness and Recovery:** If playing `D` due to a previous defection, monitor the total cooperators in the next round (`C_next`). If `C_next >= T`, switch back to **Cooperate (C)** immediately in round `t+1`. This allows the strategy to recover collective cooperation if the group trend corrects itself.

### Final Phase (Round r)
In the final round, the incentive to maintain long-term reputation or future cooperation is removed. Regardless of previous history or the reciprocity logic applied in earlier rounds, switch to **Defect (D)**. This minimizes the risk of losing the final endowment in an environment where no future retaliatory consequences exist. 

### Decision Logic Pseudocode
```python
if round == r:
    return D

if round == 1:
    return C

threshold = n / k
prev_cooperators = get_previous_round_cooperators()

if prev_cooperators >= threshold:
    return C
else:
    return D
```
'''

description_COLLECTIVE_13 = '''
Adopt a conditional cooperation strategy based on a "Tit-for-Tat with Forgiveness" framework, adapted for aggregate observation.

**Round 1:**
Cooperate (C).

**Rounds 2 through r-1:**
Let $S_{t-1}$ be the number of cooperators observed in the previous round.
Let $A_{t-1}$ be the action taken in the previous round (C=1, D=0).
Let $n$ be the total number of players.

Calculate the expected cooperation threshold $T$ as $n \times (1/k)$. This represents the break-even point where the marginal benefit of cooperation equals the cost of contribution.

1.  **If $S_{t-1} \geq T$:** Cooperate.
2.  **If $S_{t-1} < T$:** Defect.
3.  **Exception (Probabilistic Forgiveness):** If the previous action was Defect and $S_{t-1} \geq T$, switch to Cooperate (resume cooperation immediately). If the previous action was Defect and $S_{t-1} < T$, remain Defect. If the previous action was Cooperate and $S_{t-1} < T$, switch to Defect.

**Round r (Final Round):**
Defect. The incentive structure of the final round dictates that there is no future interaction to penalize, making the dominant strategy to maximize immediate payoff regardless of previous history.

**General Heuristic:**
The strategy aims to maintain a stable equilibrium where the group cooperates at or above the threshold $T$. If the group performance falls below $T$, the strategy imposes a "punishment" by defecting in the subsequent round. It allows for spontaneous recovery if the group signal returns to or exceeds $T$, effectively resetting the cooperation cycle without requiring infinite grudge-holding.
'''

description_COLLECTIVE_14 = '''
Adopt a "Contingent Tit-for-Tat" strategy, where the probability of cooperation is calibrated to maintain a reciprocal social contract.

**Round 1:**
Play C (Cooperate).

**Rounds 2 through r-1:**
Calculate the target contribution threshold, $T$, where cooperation is rational for the collective. Cooperation is individually rational if $k/n \times (\text{Cooperators} + 1) > 1$, or simply when the marginal benefit of your contribution exceeds your cost.

Set your action $A_t$ based on the total number of cooperators in the previous round, $S_{t-1}$:

1.  If $S_{t-1} \ge \lceil n/k \rceil$, play C (Cooperate). This reinforces cooperative behavior when the group is already contributing at a sustainable level.
2.  If $S_{t-1} < \lceil n/k \rceil$, play D (Defect). This protects your endowment against exploitation when the group fails to sustain a mutually beneficial threshold.

**Round r (Final Round):**
Play D (Defect). Since there is no future interaction to incentivize, the dominant strategy is to maximize the final round payoff by keeping your endowment.

**Pseudocode:**

```
// Constants: n, k, r are given parameters
// History: S_prev is the number of cooperators in the previous round

Action DetermineMove(current_round, S_prev):
    If current_round == 1:
        Return C
    
    If current_round == r:
        Return D
        
    threshold = ceil(n / k)
    
    If S_prev >= threshold:
        Return C
    Else:
        Return D
```
'''

description_COLLECTIVE_15 = '''
A "Conditional Tit-for-Tat with Forgiveness and Defection" strategy is employed to balance long-term collective cooperation with protection against exploitation. The strategy operates on the principle that the aggregate cooperative behavior of others serves as a proxy for the group's willingness to sustain the public good.

**Decision Rules:**

1.  **Initial Round (t=1):** Always Cooperate (C). This establishes a baseline of trust and signals a willingness to cooperate.

2.  **Intermediate Rounds (1 < t < r):** 
    Let $S_{t-1}$ be the number of cooperators observed in the previous round, excluding self.
    *   If $S_{t-1} \ge \tau \cdot (n-1)$, where $\tau$ is the cooperation threshold (initially set to $0.5$), Cooperate (C).
    *   If $S_{t-1} < \tau \cdot (n-1)$, Defect (D).
    *   *Adaptive Forgiveness:* If the strategy defected in the previous round due to low cooperation, but $S_{t-1} \ge \tau \cdot (n-1)$, return to Cooperate (C).

3.  **Terminal Round (t=r):** Always Defect (D). Since there is no future round to punish or incentivize, the game effectively collapses into a single-round Prisoner's Dilemma where defection is the dominant strategy to maximize payoff.

**Pseudocode:**

```python
threshold = 0.5
cooperated_previous = True

def decide_action(t, r, n, total_cooperators_last_round, self_contributed_last):
    if t == r:
        return 'D'
    
    if t == 1:
        return 'C'
    
    others_cooperated = total_cooperators_last_round - (1 if self_contributed_last else 0)
    
    if others_cooperated / (n - 1) >= threshold:
        return 'C'
    else:
        return 'D'
```

**Adaptive Adjustment:**
If the strategy experiences a cycle of mutual defection, or if $S_{t-1}$ consistently remains below the threshold for more than $k_{rounds\_limit}$ (set to 3), the strategy assumes the population is uncooperative. In this state, the threshold $\tau$ increases to $1.0$ (effectively permanently defecting) to prevent further loss of individual endowments against a non-cooperative pool. If at any point the average cooperation rate of the group recovers and sustains $\tau \ge 0.5$ for two consecutive rounds, the strategy resets $\tau$ to the baseline $0.5$ to resume conditional cooperation.
'''

description_COLLECTIVE_16 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Cooperation**

This strategy relies on a "trigger-conditional" approach designed to foster collective cooperation while protecting against defection.

**1. First Round**
Always play Cooperate (C). 

**2. Subsequent Rounds (t > 1)**
Let $S_{t-1}$ be the total number of cooperators observed in the previous round, including oneself.
Let $n$ be the total number of players and $k$ be the multiplication factor.

Calculate the "Defection Tolerance" threshold ($T$):
$T = \lceil n / k \rceil$

*   **If $S_{t-1} \ge T$:** Play Cooperate (C).
*   **If $S_{t-1} < T$:** Play Defect (D).

**3. Final Round**
The strategy is "always defect" ($D$) in the final round ($t = r$), regardless of history. 

**4. Reset Logic**
If the strategy has switched to Defect ($D$) due to the threshold rule, it will attempt to re-establish cooperation if, and only if, the number of cooperators in a single round significantly exceeds the threshold ($S_{t-1} \ge n - 1$). If this condition is met, play Cooperate (C) in the subsequent round to signal a restart of the collective agreement.

**Pseudocode:**

```python
if round == r:
    return D

if round == 1:
    return C

threshold = ceil(n / k)
cooperators_prev_round = observe_cooperators()

if cooperators_prev_round >= threshold:
    return C
else:
    # Check for signal to restart cooperation
    if cooperators_prev_round >= (n - 1):
        return C
    return D
```
'''

description_COLLECTIVE_17 = '''
**Round 1:** Play Cooperate (C). This establishes a willingness to contribute to the collective good and provides a baseline to observe the population's response.

**Subsequent Rounds (2 to r-1):** Implement a Conditional Tit-for-Tat strategy based on the aggregate cooperation level observed in the previous round. Define a threshold $T = n/k$ as the minimum number of cooperators required to make universal cooperation marginally profitable or neutral compared to defection.

1. If the number of cooperators in the previous round was $\ge T$: Play Cooperate (C).
2. If the number of cooperators in the previous round was $< T$: Play Defect (D).

**Final Round (r):** Play Defect (D) unconditionally. Since there are no future rounds to influence or leverage, defection is the dominant strategy to maximize the terminal payoff, regardless of the previous round's performance.

**Edge Case Handling:**
*   **Threshold Infeasibility:** If $T > n$ (which is impossible given the constraint $1 < k < n$), always play Defect (D).
*   **Observation Noise/Uncertainty:** In the event of a tie or ambiguity near the threshold $T$ in a dynamic environment, default to Defect (D) to prevent exploitation, as the risk of being a "sucker" outweighs the marginal gain of sustaining a fragile cooperation group.
*   **Total Defection:** If the aggregate cooperation in the previous round was 0, continue to Defect (D) in all subsequent rounds, as this signals a lack of reciprocity in the population.
'''

description_COLLECTIVE_18 = '''
The strategy follows a conditional, threshold-based reciprocity model designed to maximize group contributions while minimizing exploitation in the final rounds.

### Strategy Parameters
*   **Threshold ($\tau$):** Maintain a contribution threshold equal to $\lceil n/k \rceil$. If the number of contributors is at or above this threshold, the public good is profitable for the group.
*   **State:** The strategy maintains a *cooperation_count* variable for each round and an *active_history* list of past round outcomes.

### Decision Rules

**Round 1:**
*   Play **Cooperate (C)**. This signals a willingness to engage in reciprocal cooperation.

**Rounds $t=2$ to $r-1$:**
*   Calculate the number of contributors $C_{t-1}$ from the previous round.
*   If $C_{t-1} \geq \tau$:
    *   Play **Cooperate (C)**.
*   If $C_{t-1} < \tau$:
    *   Play **Defect (D)**. This punishes the group for falling below the profitability threshold and protects against exploitation.

**Final Round ($t=r$):**
*   Play **Defect (D)**. Regardless of prior cooperation, the final round provides no incentive for future reciprocity. Defecting prevents exploitation in the terminal round where future retaliation is impossible.

### Pseudocode Implementation

```python
def decide_action(t, r, n, k, history):
    # Parameter setup
    threshold = ceil(n / k)
    
    # Final round defect
    if t == r:
        return 'D'
    
    # First round cooperate
    if t == 1:
        return 'C'
    
    # Reciprocal logic
    last_contributors = history[-1].cooperators
    
    if last_contributors >= threshold:
        return 'C'
    else:
        return 'D'
```

### Edge Cases and Adjustments
*   **Threshold Vulnerability:** If the calculated threshold $\lceil n/k \rceil$ is very high (close to $n$), the group may struggle to reach it. If the strategy observes three consecutive rounds of defection ($C_t < \tau$), it switches to permanent defection for the remainder of the game, as the group demonstrates an inability or unwillingness to sustain the public good.
*   **Recovery:** If the group fails to meet the threshold but then returns to $\geq \tau$ in the subsequent round, the strategy resumes **Cooperate (C)** immediately, allowing for potential reconciliation if the population of cooperators is dynamic.
'''

description_COLLECTIVE_19 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Cooperation (CTFT-TC)**

The strategy operates based on the round number $t \in \{1, \dots, r\}$ and the observed number of cooperators from the previous round $C_{t-1}$.

**Round 1:**
Play **Cooperate (C)**.

**Rounds $2$ through $r-1$:**
Calculate the cooperation threshold $\tau = \lceil \frac{n}{k} \rceil$.
Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
- If $C_{t-1} \geq \tau$, play **Cooperate (C)**.
- If $C_{t-1} < \tau$, play **Defect (D)**.

**Round $r$ (The Final Round):**
Play **Defect (D)** regardless of previous history.

**State Recovery (Optional Modification):**
If the strategy is currently Defecting due to a previous observation $C_{t-1} < \tau$, and the current round is not the final round, attempt to re-establish cooperation if specific conditions are met:
- If $C_{t-1} < \tau$, play **Defect (D)** with probability $p = 0.9$ and **Cooperate (C)** with probability $1-p = 0.1$. This "probabilistic probe" allows the strategy to potentially restart cooperation if other players are also utilizing a similar "trigger" or "cooperative recovery" mechanism, breaking cycles of mutual defection.

**Decision Logic Pseudocode:**
```python
def get_action(t, r, n, k, C_prev):
    if t == r:
        return 'D'
    if t == 1:
        return 'C'
    
    threshold = ceil(n / k)
    
    if C_prev >= threshold:
        return 'C'
    else:
        # Probabilistic probe to attempt recovery
        if random() < 0.1:
            return 'C'
        else:
            return 'D'
```
'''

description_COLLECTIVE_20 = '''
Play Cooperate (C) in the first round.

In subsequent rounds (t > 1), adopt a conditional trigger strategy based on the observed number of cooperators from the previous round (t-1). Let $C_{t-1}$ be the total number of cooperators observed in round $t-1$.

If $t < r$:
- If $C_{t-1} \geq \lceil n \cdot (1 - \frac{k}{n}) \rceil$ (the threshold required to make cooperation individually rational compared to universal defection), play Cooperate (C).
- Otherwise, play Defect (D) for the remainder of the game.

If $t = r$:
- If $C_{t-1} = n$ (perfect cooperation maintained throughout), play Cooperate (C).
- Otherwise, play Defect (D).

In the specific case where $C_{t-1}$ indicates that defection was universally profitable (i.e., $C_{t-1} < \frac{n}{k}$), immediately switch to Defect (D) for all remaining rounds.
'''

description_COLLECTIVE_21 = '''
The strategy employs a "Conditional Tit-for-Tat with Forgiving Resilience" approach, designed to cultivate mutual cooperation while minimizing exploitation.

**Initialization (Round 1):**
Play C (Cooperate). Starting with cooperation signals a preference for the socially optimal outcome.

**General Decision Rule (Rounds 2 to r-1):**
Define the "Contribution Threshold" ($T$) as the level of cooperation required to sustain the strategy. The strategy monitors the aggregate cooperation of opponents in the previous round ($C_{prev}$).

*   If $C_{prev} \geq \lceil n \cdot (1/k) \rceil$: Play C. This maintains the cycle of mutual cooperation.
*   If $C_{prev} < \lceil n \cdot (1/k) \rceil$: Play D (Defect). This punishes free-riding.
*   **Forgiveness Mechanism:** If the strategy defected in the previous round due to low aggregate cooperation, play C with probability $p = 0.1$ in the current round. This probability check prevents "death spirals" of mutual defection caused by noise or transient misunderstandings, allowing the group to restart cooperation.

**Terminal Phase (Last Round):**
Play D (Defect). Since the future shadow of the game is non-existent in the final round, the incentive to defect outweighs the value of maintaining a reputation for the next round. This avoids exploitation in the terminal period.

**Pseudocode Logic:**

```python
def decide_action(round_number, total_rounds, prev_round_cooperators, n, k):
    # Threshold for break-even cooperation: (k/n) * Total_C >= 1  => Total_C >= n/k
    threshold = ceil(n / k)
    
    # Last round termination
    if round_number == total_rounds:
        return 'D'
    
    # First round initialization
    if round_number == 1:
        return 'C'
        
    # Standard conditional logic
    if prev_round_cooperators >= threshold:
        return 'C'
    else:
        # Check for recovery from mutual defection
        if random_chance() < 0.1:
            return 'C'
        else:
            return 'D'
```

**Collective Mindset:**
The strategy assumes that the aggregate group welfare is maximized when all players contribute. The decision rule effectively enforces a collective standard where cooperation is conditional on sufficient group participation ($n/k$). By defecting when group participation falls below this threshold, the strategy protects its own endowment while signaling that universal cooperation is required to incentivize further contributions. By utilizing a small probability of forgiveness, the strategy remains robust against transient fluctuations in group behavior, ensuring that a single round of low cooperation does not permanently collapse the cooperative potential of the group.
'''

description_COLLECTIVE_22 = '''
**Strategy: Tit-for-Tat with Conditional Cooperation (TFT-CC)**

**Initialization:**
Set `cooperation_threshold = 1` for the first round.
Set `punishment_mode = False`.

**Decision Rules:**

1.  **First Round:** 
    Always play **Cooperate**.

2.  **Subsequent Rounds (2 to r-1):**
    Let `previous_total_cooperators` be the total number of players who contributed in the previous round.
    *   If `previous_total_cooperators` >= `cooperation_threshold`: 
        Play **Cooperate**.
        Set `punishment_mode = False`.
    *   If `previous_total_cooperators` < `cooperation_threshold`:
        Play **Defect**.
        Set `punishment_mode = True`.
    
    *Dynamic Adjustment:* 
    If `punishment_mode` is active, increment `cooperation_threshold` by 1 (up to a cap of `n-1`) to attempt to nudge the group toward higher coordination. If the group successfully meets or exceeds the new `cooperation_threshold`, revert `cooperation_threshold` to the baseline value of 1 and set `punishment_mode = False`.

3.  **Final Round (Round r):**
    If `punishment_mode` is active, play **Defect**.
    If `punishment_mode` is false, play **Cooperate**.

**Pseudocode:**

```python
# Constants: n, k, r are provided inputs
threshold = 1
in_punishment = False

for round in range(1, r + 1):
    if round == 1:
        action = Cooperate
    elif round == r:
        if in_punishment:
            action = Defect
        else:
            action = Cooperate
    else:
        # Evaluate previous round performance
        # total_cooperators includes self if previously Cooperated
        if total_cooperators >= threshold:
            action = Cooperate
            in_punishment = False
            threshold = 1 # Reset to baseline
        else:
            action = Defect
            in_punishment = True
            if threshold < (n - 1):
                threshold += 1

    submit(action)
```

**Edge Case Handling:**
*   **Low k values:** If `k` is close to 1, the incentive to defect is high. The `threshold` adjustment mechanism will naturally scale upward, causing the strategy to shift to permanent defection earlier if the group fails to coordinate, thereby minimizing losses.
*   **High k values:** If `k` approaches `n`, the strategy maintains cooperation unless the group size or behavior indicates high defection, ensuring mutual benefit.
*   **Anonymous feedback:** Because individual identification is impossible, the strategy assumes the group is a single entity. The `threshold` adjustment serves as a signal to the aggregate population that higher participation is required for continued cooperation.
'''

description_COLLECTIVE_23 = '''
Use a conditional cooperative strategy based on the **"Pavlov" (Win-Stay, Lose-Shift)** heuristic modified for an N-player environment, governed by a "target contribution threshold."

### State Variables
- $C_{t-1}$: Number of cooperators observed in the previous round.
- $Action_{t-1}$: Own action in the previous round (1 for C, 0 for D).
- $Threshold$: The minimum number of cooperators required to justify cooperation. Calculate $Threshold = \lceil n/k \rceil$. This is the point at which the individual payoff of cooperating equals the individual payoff of defecting ($k/n * C = 1 + k/n * (C-1)$ simplifies to requiring $k/n * C \geq 1$, hence $C \geq n/k$).

### Round 1
Play $C$ (Cooperate).

### Rounds 2 to $r-1$
Determine action based on the previous round's performance and cooperation density:

1.  **If $C_{t-1} \geq Threshold$**:
    - If $Action_{t-1} == C$: Repeat $C$. (The collective outcome is beneficial or neutral; maintain stability).
    - If $Action_{t-1} == D$: Switch to $C$. (The threshold was met; defecting is unnecessary and harmful to potential future cooperation).

2.  **If $C_{t-1} < Threshold$**:
    - If $Action_{t-1} == C$: Switch to $D$. (Cooperation is being exploited or under-supported; withdraw contribution to minimize losses).
    - If $Action_{t-1} == D$: Repeat $D$. (Continue defecting while the group fails to meet the contribution threshold).

### Final Round ($r$)
Regardless of history, play $D$ (Defect). Since there is no future round to incentivize or punish, the dominant strategy is to maximize the immediate payoff by keeping the endowment.

### Edge Case:
If $n/k$ is not an integer, the decision to cooperate remains tied to the ceiling of the calculation ($\lceil n/k \rceil$) to ensure the marginal return of the public good covers the cost of the contribution.
'''

description_COLLECTIVE_24 = '''
Adopt a "Conditional Reciprocity" strategy based on the principle of Tit-for-Tat extended to N players.

**Round 1:**
Cooperate (C).

**Subsequent Rounds (2 to r-1):**
Observe the total number of cooperators from the previous round (S_{t-1}).
Calculate the expected cooperation threshold $T$ required to make mutual cooperation as profitable as defection, defined as $T = \frac{n}{k}$.
If $S_{t-1} \ge T$: Cooperate (C).
Else: Defect (D).

**Final Round (r):**
Defect (D).

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, last_round_cooperators, n, k):
    # Determine the cooperation threshold
    threshold = n / k
    
    # Final round defect
    if round_number == total_rounds:
        return 'D'
    
    # First round cooperate
    if round_number == 1:
        return 'C'
        
    # Reciprocal cooperation based on threshold performance
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
- If the calculated threshold $T$ is not an integer, round up to the nearest integer.
- In cases where $T > n$ (impossible scenarios given $k > 1$), prioritize defecting if previous contributions were suboptimal to protect against exploitation.
- If $n$ is very large or information is noisy, treat the threshold $T$ as a target; if the group average cooperation rate falls below $1/k$, immediately switch to Defect (D) for one round to signal dissatisfaction before attempting to return to Cooperation (C).
'''

description_COLLECTIVE_25 = '''
Use a conditional cooperation strategy based on the "Triggered Tit-for-Tat" principle, adjusted for $N$-player interaction.

**Decision Rules:**
1.  **Round 1:** Play C (Cooperate).
2.  **Rounds $t > 1$:** Calculate the "cooperation threshold" $T$. This threshold is the minimum number of cooperators required in the previous round ($t-1$) to make reciprocal cooperation viable. Given the payoff structure, cooperation is individually rational if the benefit of the group effort outweighs the loss of the private endowment. Specifically, play C if the number of cooperators in round $t-1$ was $\ge$ some minimal viable quorum. A robust heuristic is to cooperate if the previous round’s total cooperation count was greater than or equal to the "break-even" point: $n/k$.
3.  **Defection Trigger:** If the number of cooperators in round $t-1$ is strictly less than the break-even threshold $\lceil n/k \rceil$, play D (Defect) for the current round.
4.  **Resumption:** If playing D, return to C in the next round if the number of cooperators in the immediately preceding round increases to $\ge \lceil n/k \rceil$.

**Edge Cases:**
*   **Last Round ($t=r$):** Regardless of previous history, play D. In a finite, repeated prisoner's dilemma variant where defection is a dominant strategy in a single round, the rational equilibrium for the final round is to defect to maximize the individual payoff, as there is no future punishment for the defection.
*   **Ambiguous History:** If the number of cooperators in round $t-1$ was zero, continue to play D to avoid exploitation.
*   **Tie-breaking:** If the number of cooperators in round $t-1$ exactly equals $\lceil n/k \rceil$, play C.

**Pseudocode:**
```python
def get_action(t, r, n, k, last_round_cooperators):
    if t == r:
        return D
    if t == 1:
        return C
    
    threshold = ceil(n / k)
    
    if last_round_cooperators >= threshold:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_26 = '''
In round 1, play C.

In subsequent rounds $t \in \{2, \dots, r-1\}$, track the number of cooperators from the previous round, $S_{t-1}$. 

If $S_{t-1} \geq \text{threshold}$, play C, where the threshold is defined as $\lceil \frac{n}{k} \rceil$. 

If $S_{t-1} < \lceil \frac{n}{k} \rceil$, play D. Once having switched to D due to an insufficient number of cooperators, remain in a "punishment state" for 2 rounds. After the punishment state concludes, return to C.

In the final round $t = r$:
If $S_{r-1} \geq \lceil \frac{n}{k} \rceil$, play C.
If $S_{r-1} < \lceil \frac{n}{k} \rceil$, play D.

If a sequence of "all-defect" rounds occurs (where $S_{t-1} = 0$) for 3 consecutive rounds, trigger an "extinction" protocol: play D for the remainder of the game, regardless of any future cooperation by opponents.
'''

description_COLLECTIVE_27 = '''
### Strategy: Conditional Reciprocity with Forgiving Tit-for-Tat

**Initialization (Round 1):**
Play C (Cooperate). This initiates a cooperative stance and tests the collective environment.

**Decision Rules (Rounds 2 to r-1):**
Let $c_{t-1}$ be the total number of cooperators observed in the previous round.
Let $n$ be the total number of players.
Calculate the cooperation threshold $T$ as $T = \lceil n/k \rceil$.

*   **If $c_{t-1} \geq T$:** Play C (Cooperate). This sustains cooperation when the collective benefit meets or exceeds the opportunity cost of contribution.
*   **If $c_{t-1} < T$:** Play D (Defect). This punishes the group for failing to maintain a socially optimal level of contribution, minimizing personal losses when the group is non-cooperative.
*   **Forgiveness Mechanism:** If the previous round resulted in total defection ($c_{t-1} = 0$), play D. However, if $c_{t-1}$ increases by more than 50% of the previous round's value, play C regardless of the threshold $T$ to signal a willingness to rebuild cooperation.

**Terminal Phase (Round r):**
Play D (Defect) regardless of previous history. Because there are no future rounds to influence, the dominant strategy is to maximize the final round's payoff by keeping the endowment.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, n, k, prev_cooperators):
    # Terminal round logic
    if round_number == total_rounds:
        return 'D'
    
    # First round initialization
    if round_number == 1:
        return 'C'
        
    # Standard conditional logic
    threshold = ceil(n / k)
    
    # Forgiveness/Rebuilding
    if prev_cooperators > 0 and (prev_cooperators / last_observed_prev) > 1.5:
        return 'C'
        
    # Reciprocity
    if prev_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_COLLECTIVE_28 = '''
**Strategy: Conditional Tit-for-Tat (CTFT)**

The strategy operates on the principle of conditional reciprocity: cooperate if the collective behavior demonstrates sufficient support for the public good, and defect otherwise.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. This signals a willingness to initiate cooperation and tests the cooperative disposition of the opponent pool.

2.  **Rounds 2 through (r-1):**
    Calculate the cooperation threshold required to make cooperation individually rational or neutral compared to the previous round’s outcome.
    *   Let $C_{t-1}$ be the total number of cooperators in the previous round (including yourself).
    *   Define the "Critical Mass" $M$ as the minimum number of cooperators required such that playing $C$ yields a payoff $\ge$ playing $D$:
        $(k/n) \times M \ge 1 \implies M \ge n/k$.
    *   If $C_{t-1} \ge \lceil n/k \rceil$, play **Cooperate (C)**.
    *   If $C_{t-1} < \lceil n/k \rceil$, play **Defect (D)**. This serves as a punishment mechanism against groups that fail to sustain the critical mass of cooperation required for a positive return on investment.

3.  **Final Round (Round r):**
    Play **Defect (D)**. Because the game terminates, there is no future round to incentivize or punish. Defection is the dominant strategy in the final round as it maximizes individual payoff regardless of the collective outcome, given that the threat of future retaliation is nullified.

**Adaptive Refinement:**
If the history indicates that the number of cooperators has been exactly $\lceil n/k \rceil$ for two consecutive rounds, increase the threshold by +1 (if possible without exceeding $n$) to encourage higher efficiency (approaching universal cooperation). If the number of cooperators falls below $\lceil n/k \rceil$ after this increase, revert immediately to the baseline threshold of $\lceil n/k \rceil$ in the next round.
'''

description_COLLECTIVE_29 = '''
Adopt a conditional-cooperation strategy based on a trigger-based tit-for-tat mechanism with a forgiving threshold. The objective is to sustain mutual cooperation while minimizing exploitation.

**Initialization (Round 1):**
Play Cooperate (C) with probability $p = 1.0$.

**Decision Rule (Rounds $t=2$ to $r-1$):**
Define a "cooperation threshold" $T$ as $T = \lceil n/k \rceil$. Observe the total number of cooperators $S_{t-1}$ from the previous round.

1.  If $S_{t-1} \geq T$ (or if $S_{t-1} \geq n-1$ in cases where $n < k$ is impossible but coordination is high): Play Cooperate (C).
2.  If $S_{t-1} < T$: Play Defect (D) to punish non-cooperative behavior and preserve endowment.
3.  **Forgiveness Mechanism:** If the strategy previously defected, check if the previous round's cooperation count $S_{t-1}$ returned to a level indicating intent to cooperate (i.e., $S_{t-1} \geq T - 1$). If so, resume cooperation (C) with probability 0.5 to test for reconciliation.

**Terminal Phase (Round $r$):**
Always play Defect (D), regardless of previous history. In a finite game, the rational incentive structure collapses in the final round as there is no future interaction to penalize, and defection is the dominant strategy to maximize the final round's individual payoff.

**Pseudocode Logic:**

```python
def get_action(round_number, history, n, k):
    if round_number == r:
        return 'D'
    
    if round_number == 1:
        return 'C'
    
    threshold = ceil(n / k)
    last_round_cooperators = history.last_round_count
    
    if last_round_cooperators >= threshold:
        return 'C'
    elif last_round_cooperators >= threshold - 1 and previously_defected():
        return 'C' if random() > 0.5 else 'D'
    else:
        return 'D'
```
'''

description_COLLECTIVE_30 = '''
Play "Generous Tit-for-Tat with a Threshold Trigger."

### Decision Rules

Define `c_total` as the number of cooperators observed in the previous round.
Define `c_prev` as your own contribution in the previous round (1 for Cooperate, 0 for Defect).
Define `cooperation_threshold` as `(n / k)`. This is the minimum number of cooperators required to make universal cooperation marginally profitable or neutral relative to universal defection.

1.  **First Round:** Play **Cooperate**. This signals a cooperative intent and initiates the potential for mutual benefit.

2.  **Subsequent Rounds (t=2 to r-1):**
    *   If `c_total` is greater than or equal to `cooperation_threshold`, play **Cooperate**.
    *   If `c_total` is less than `cooperation_threshold`, play **Defect**.

3.  **Last Round (t = r):** Play **Defect**. Because there is no future interaction to incentivize cooperation, the dominant strategy for the final round is defection.

### Edge Cases and Adjustments

*   **Adjustment for Uncertainty:** If the calculation of `cooperation_threshold` results in a non-integer, round up to the nearest integer.
*   **The "Punishment" Buffer:** If `c_total` in the previous round is exactly 1 less than `cooperation_threshold` and your own previous action was `Defect`, play **Cooperate** to test if the group is attempting to return to equilibrium. If you played `Cooperate` in the previous round while the group failed to meet the threshold, revert to **Defect** to avoid exploitation.
*   **Initialization Failure:** If in any round prior to the last, the total contribution is 0, continue to play **Defect** for the remainder of the game, as the group has demonstrated a complete refusal to cooperate.
'''

description_COLLECTIVE_31 = '''
Initialize state variable `my_cooperation_history` as an empty list and `opponent_contribution_history` as an empty list.

**Round 1:**
Contribute (C). This establishes a cooperative baseline to encourage mutual cooperation.

**Intermediate Rounds (2 to r-1):**
Observe the number of cooperators from the previous round, `total_c_prev`. Calculate the `expected_others_contribution` as `total_c_prev - my_previous_action`.

Apply a Conditional Cooperation strategy:
1. If `total_c_prev` is greater than or equal to a threshold `T`, where `T` is determined by the ratio of the multiplication factor to the number of players:
   - Calculate the contribution threshold `T = (n / k)`.
   - If `total_c_prev >= T`: Play C.
   - If `total_c_prev < T`: Play D.
2. If the population has consistently defected (total cooperation is 0 or near 0) for the last 2 rounds, permanently switch to D to minimize losses.

**Final Round (r):**
Calculate the `net_benefit` of cooperating versus defecting based on the current round's expected cooperation.
- If the trend of `opponent_contribution_history` over the last 3 rounds shows an upward or stable trajectory and the average cooperation rate suggests `(k/n) * (avg_cooperators) > 1`: Play C.
- Otherwise, play D to capture the private endowment, as there is no future incentive for opponents to reciprocate in subsequent rounds.

**Pseudocode Logic:**
```python
def decide_action(round_number, total_c_prev, my_last_action):
    # Establish cooperation in round 1
    if round_number == 1:
        return C
    
    # Calculate threshold based on sustainability
    # If (k/n) * total_contributors > 1, cooperation is net-positive for the group
    threshold = n / k 
    
    # Final round defect condition: 
    # Unless group cooperation is extremely high (all or near-all), defect to maximize individual payoff
    if round_number == r:
        return D if total_c_prev < n else C
    
    # Conditional strategy for intermediate rounds
    if total_c_prev >= threshold:
        return C
    else:
        return D
```
'''

description_COLLECTIVE_32 = '''
**Initial Round:**
Cooperate (C).

**Subsequent Rounds:**
Calculate the "Cooperation Threshold" ($T$) required for mutual cooperation to be profitable:
$T = \lceil n/k \rceil$.

If the total number of cooperators observed in the previous round ($C_{t-1}$) is greater than or equal to $T$:
- Continue to Cooperate (C).

If the total number of cooperators observed in the previous round ($C_{t-1}$) is less than $T$:
- Defect (D) for the current round.

**Terminal Phase:**
In the final round ($t = r$), unconditionally Defect (D), regardless of previous observations, to avoid exploitation.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, n, k, last_round_cooperators):
    # Threshold for social optimality
    threshold = ceil(n / k)
    
    # Defect on the final round
    if round_number == total_rounds:
        return 'D'
        
    # Start by signaling cooperation
    if round_number == 1:
        return 'C'
        
    # Tit-for-tat adaptation based on collective threshold
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_5 = '''
**Strategy: Adaptive Reciprocal Tit-for-Tat**

The strategy operates on the principle of conditional cooperation, seeking to establish a cooperative equilibrium while protecting against exploitation. The decision process for round $t$ is as follows:

**1. Initialization (Round $t = 1$):**
Always cooperate (Play C). Establishing trust is the prerequisite for achieving high-payoff cooperative outcomes.

**2. Decision Logic (Rounds $t = 2$ to $r-1$):**
Cooperate if and only if the contributions of the opponents in the previous round ($t-1$) met a sufficient threshold of reciprocity.

Calculate the observed cooperation rate of the group from the previous round:
$O_{t-1} = \frac{\Sigma_{j \neq i} c_j}{n-1}$

*   **Cooperate (C)** if $O_{t-1} \geq \theta$
*   **Defect (D)** if $O_{t-1} < \theta$

Where the threshold $\theta$ is defined by the game parameters to ensure the contribution is rational:
$\theta = \frac{n}{k(n-1)}$

This threshold $\theta$ represents the minimum fraction of other players who must cooperate for the expected return of cooperating to be non-negative relative to defecting. If the group meets this threshold, cooperation is incentivized; if they fall below it, the strategy switches to defection to avoid being a "sucker" while the group is uncooperative.

**3. Terminal Round (Round $t = r$):**
Defect (Play D). In a finite, known-length game with no reputation mechanism beyond the current game, the rational and game-theoretic dominant strategy for the final round is defection. This prevents exploitation in the terminal phase where future consequences cannot be enforced.

**4. Exception/Reset Rule:**
If the strategy is currently defecting, "forgive" the opponents by switching back to Cooperate (C) with probability $p = 0.05$ (or simply every $x$ rounds, e.g., every 10th round, if the game length $r$ allows) to test if the group has returned to a cooperative norm. If an opponent tests cooperation and the group threshold is met, the strategy resumes conditional cooperation.

**Pseudocode Summary:**

```python
if t == 1:
    return C
elif t == r:
    return D
else:
    threshold = n / (k * (n - 1))
    observed_others_cooperation = (total_cooperators_previous - (1 if last_move == C else 0)) / (n - 1)
    
    if observed_others_cooperation >= threshold:
        return C
    else:
        # Stochastic forgiveness: check if we should test for cooperation
        if random() < 0.05: 
            return C
        else:
            return D
```
'''

description_PROSOCIAL_6 = '''
**Strategy: Conditional Reciprocal Contribution**

**Decision Logic**
The strategy operates on the principle of conditionally cooperating as long as the aggregate group cooperation rate justifies the investment. It calculates a "break-even" threshold for cooperation based on the game parameters and adjusts behavior in response to the group's recent history.

Let $C_{t-1}$ be the number of cooperators in the previous round, and let $T_t = 1$ if the player cooperates in round $t$ and $T_t = 0$ if they defect.

*   **Round 1:** Play $C$ (Cooperate). This initiates a prosocial stance and signals willingness to participate in the public good.

*   **Rounds $t \in [2, r-1]$:**
    Calculate the effective cooperation threshold. A player's contribution $C$ is profitable if the total number of cooperators ($N_C$) satisfies the inequality: 
    $(k/n) \times N_C > 1$. 
    Rearranging gives the target number of cooperators: $N_C > n/k$.
    
    *   If $C_{t-1} \ge \lceil n/k \rceil$, play $C$.
    *   If $C_{t-1} < \lceil n/k \rceil$, play $D$.
    
    *Exception (The Forgiveness/Re-entry Rule):* If the strategy is currently playing $D$ due to low group cooperation, play $C$ once every 5 rounds to test if the group has returned to a cooperative state. If this test round results in $C_t \ge \lceil n/k \rceil$, resume consistent cooperation in the subsequent round.

*   **Final Round ($t = r$):**
    Play $D$ (Defect). Because the game ends at $t=r$, there is no future interaction to incentivize, and therefore no strategic reason to contribute to the public good. The benefits of cooperation cannot be reciprocated in subsequent rounds, making $D$ the dominant strategy for the terminal round.

**Pseudocode**

```python
def get_action(round_number, total_rounds, last_round_cooperators, n, k):
    # Terminal round logic
    if round_number == total_rounds:
        return "D"
    
    # Initiation
    if round_number == 1:
        return "C"
        
    # Calculate cooperation threshold
    threshold = ceil(n / k)
    
    # Forgiveness/Re-entry check
    if (round_number % 5 == 0):
        return "C"
        
    # Reciprocal check
    if last_round_cooperators >= threshold:
        return "C"
    else:
        return "D"
```
'''

description_PROSOCIAL_7 = '''
The strategy employs a conditional cooperative approach based on a "tit-for-tat with threshold-based forgiveness" mechanism. Let $C_t$ be the number of cooperators observed in round $t$, and $n$ be the number of players.

**Round 1:**
Always play **C**. This initiates cooperation and signals a willingness to engage in a mutually beneficial outcome.

**Subsequent Rounds ($t > 1$):**
Decide the action for round $t$ based on the aggregate cooperation level observed in the previous round ($C_{t-1}$):

1.  **If $C_{t-1} \ge \lfloor n/2 \rfloor + 1$:** Play **C**. If the collective cooperation level indicates a clear majority or supermajority supporting the public good, continue to support the project.
2.  **If $C_{t-1} < \lfloor n/2 \rfloor$:** Play **D**. If the previous round’s contribution level falls significantly below a simple majority, defect to protect individual payoff and signal disapproval of the current collective contribution rate.
3.  **If $C_{t-1} = \lfloor n/2 \rfloor$ (in even-numbered $n$ scenarios):** Play **C** if $t < r$, but play **D** if $t = r$. This maintains cooperation during the game but avoids exploitation during the final round when the future benefit of signaling is nullified.

**The "Apology" Mechanism (Recovery Rule):**
If the previous action was **D** due to low turnout, but the round before that ($t-2$) had a high turnout, and the current turnout $C_{t-1}$ shows signs of recovery (defined as $C_{t-1} > C_{t-2}$), switch back to **C** to reset the cycle of cooperation.

**Final Round ($t = r$):**
Apply the following override:
*   If $C_{r-1} \ge \lfloor n/2 \rfloor$: Play **C**.
*   If $C_{r-1} < \lfloor n/2 \rfloor$: Play **D**.

**Pseudocode:**
```
Function GetAction(t, r, n, C_prev, C_prevprev):
    If t == 1:
        Return C
    
    If t == r:
        If C_prev >= floor(n / 2): Return C
        Else: Return D
        
    If C_prev >= (floor(n / 2) + 1):
        Return C
        
    If C_prev < floor(n / 2):
        If C_prev > C_prevprev: Return C
        Else: Return D
        
    If C_prev == floor(n / 2):
        Return C
```
'''

description_PROSOCIAL_8 = '''
The strategy operates on a conditional cooperation framework with a "forgiving tit-for-tat" logic, adjusted for the $N$-player environment where individual contribution tracking is impossible. The core objective is to incentivize mutual cooperation while minimizing exploitation.

### Decision Rules

Define $C_t$ as the number of cooperators observed in round $t$. Let $E[C_{t-1}]$ be the expected number of cooperators required to make cooperation individually rational (i.e., the break-even point where the payoff of cooperating equals the payoff of defecting).

1.  **Round 1:** Always choose **Cooperate**. This establishes a prosocial signal and tests the population's willingness to cooperate.

2.  **Rounds 2 through $r-1$:**
    *   Calculate the observed cooperation rate $P_{t-1} = C_{t-1} / (n-1)$ (excluding your own contribution).
    *   Maintain a "cooperation threshold" $T$, where $T = n/k$.
    *   If $C_{t-1} \ge T$, choose **Cooperate**.
    *   If $C_{t-1} < T$, apply a probabilistic response:
        *   With probability $P_{t-1}$, choose **Cooperate**.
        *   With probability $1 - P_{t-1}$, choose **Defect**.
    *   This probabilistic approach ensures that even if cooperation drops, you remain open to resuming cooperation if the group trend stabilizes, without being blindly exploited.

3.  **Final Round ($r$):**
    *   If $C_{r-1} \ge T$, choose **Cooperate**.
    *   If $C_{r-1} < T$, choose **Defect**.
    *   This prevents the "end-game effect" from being exploited by unconditional defectors while rewarding a successful history of group cooperation one last time.

### Pseudocode Representation

```python
def decide_action(round_number, n, k, history):
    threshold = n / k
    
    if round_number == 1:
        return "C"
        
    if round_number == r:
        if history[-1].cooperators >= threshold:
            return "C"
        else:
            return "D"
            
    # Calculate observed cooperators excluding self
    obs_coops = history[-1].cooperators - (1 if history[-1].my_action == "C" else 0)
    coop_rate = obs_coops / (n - 1)
    
    if obs_coops >= threshold:
        return "C"
    else:
        # Probabilistic defection to maintain presence without full exposure
        return "C" if random() < coop_rate else "D"
```

### Prosocial Justification

The strategy is "prosocial" because it prioritizes group welfare as long as a sufficient number of peers also contribute to the public good. It does not initiate defection and attempts to restart cooperation cycles if the group environment becomes favorable. By using the threshold $n/k$, the strategy only demands the minimum level of group cooperation necessary to make contribution collectively rational, thereby maximizing the likelihood of sustaining the cooperative equilibrium.
'''

description_PROSOCIAL_9 = '''
**Strategy Name: Adaptive Conditional Cooperation (ACC)**

This strategy operates on the principle of conditional cooperation, seeking to build mutual benefit through reciprocity while maintaining a defensive mechanism against defectors. The strategy tracks the history of the game to determine an adaptive contribution level.

**Decision Rules:**

1.  **Initialization (Round 1):** Play C (Cooperate). Cooperation is necessary to initiate the potential for mutual benefit.

2.  **Tracking (Round 2 to r-1):**
    *   Define $C_{t-1}$ as the number of cooperators observed in the previous round.
    *   Define $S_{t-1}$ as the number of cooperators observed in the previous round *excluding* your own contribution.
    *   Calculate the "Cooperation Ratio" $R = S_{t-1} / (n - 1)$.
    *   **Cooperation Rule:** If your previous move was C, continue to play C if $R \ge 1/k$. This threshold ensures that your contribution is at least breaking even or generating net value based on the multiplication factor $k$.
    *   **Defection Rule:** If the previous round saw zero cooperation from opponents ($S_{t-1} = 0$), play D (Defect).
    *   **Forgiveness/Resumption:** If you previously played D due to a low cooperation ratio, play C only if the *previous* round saw a cooperation count $C_{t-1} \ge \lceil n/k \rceil$. This requires a significant collective signal of cooperation before re-engaging.

3.  **Terminal Phase (Round r):**
    *   In the final round, the incentive to maintain future cooperation vanishes. To maximize total payoff, play D (Defect) unless the previous round was a state of "Perfect Cooperation" (where $C_{t-1} = n$). If $C_{t-1} = n$, play C.

**Pseudocode Implementation:**

```python
def choose_action(round_num, total_rounds, n, k, history):
    # Round 1
    if round_num == 1:
        return 'C'
    
    # Terminal Round
    if round_num == total_rounds:
        # Check if everyone cooperated last round
        if history[-1]['cooperators'] == n:
            return 'C'
        else:
            return 'D'
            
    # Standard Rounds
    last_round_data = history[-1]
    # Identify how many others cooperated
    if last_round_data['my_action'] == 'C':
        others_cooperated = last_round_data['cooperators'] - 1
    else:
        others_cooperated = last_round_data['cooperators']
        
    # Reciprocity Logic
    # Threshold: play C if others' contribution is sustainable (k/n * others >= 1/n)
    # Simplified: play C if others_cooperated >= (n / k)
    if others_cooperated >= (n / k):
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Zero Cooperation:** If opponents play D, the strategy immediately switches to D to prevent exploitation.
*   **Low r:** If $r$ is small, the strategy prioritizes the reciprocal trigger. If the multiplication factor $k$ is very close to 1, the strategy defaults to D, as the game structure approaches a non-cooperative prisoner's dilemma where the returns on cooperation are minimal.
*   **Incomplete Information:** Since aggregate observation is the only data available, the strategy treats the aggregate count as the sole indicator of group intent, ignoring individual identity.
'''

description_PROSOCIAL_10 = '''
**Initial Round:**
Cooperate (C).

**Subsequent Rounds (t > 1):**
Let $N$ be the number of players, $C_{t-1}$ be the number of cooperators in the previous round, and $k$ be the multiplication factor.

1.  Calculate the Threshold for Collective Benefit ($T$):
    $T = n / k$

2.  Decision Rule:
    If $C_{t-1} \ge \lceil T \rceil$:
    Cooperate (C).

    If $C_{t-1} < \lceil T \rceil$:
    Defect (D).

**Terminal Round (t = r):**
Regardless of the decision rule above, play Defect (D) if the strategy has defected at any point in the previous rounds or if the calculated threshold $T$ is greater than or equal to $n-1$. Otherwise, continue the decision rule from the subsequent rounds section.

**Exception:**
If the history indicates that total cooperation has strictly increased or remained stable at a high level relative to the group size for the majority of rounds, play Cooperate (C) regardless of the previous round's outcome to encourage sustained cooperation. If the group size is small (n < 4), prioritize Tit-for-Tat behavior: Cooperate if the group cooperated in the previous round; Defect if the group defected.
'''

description_PROSOCIAL_11 = '''
The strategy operates as a conditional cooperator, utilizing a "Tit-for-Tat with Forgiveness" approach adapted for n-player dynamics. It aims to foster mutual cooperation while limiting exploitation by defectors.

**1. Definitions and Initialization:**
*   **Target Contribution Level:** $T_{t}$ is the threshold of cooperation from the group required to justify continued cooperation.
*   **Cooperation Trigger:** Initially, cooperate (C) in the first round.
*   **Forgiveness Parameter:** Keep a history of the number of cooperators observed, $C_{obs, t-1}$.

**2. Decision Rules:**
For any round $t$ where $1 < t \le r$:
*   **Observation:** Calculate the "Cooperation Rate" $R_{t-1} = C_{obs, t-1} / (n-1)$. This represents the fraction of other players who cooperated in the previous round.
*   **Decision Logic:**
    *   If $R_{t-1} > 0.5$: Cooperate (C). This threshold indicates that a majority of the group is behaving prosocially, justifying continued contribution to the public good.
    *   If $R_{t-1} \le 0.5$: Defect (D). This is a punitive response to insufficient cooperation, protecting against exploitation.
    *   **Probabilistic "Probe" (Recovery):** If the current state is Defect, play Cooperate (C) with a small probability $p = 0.05$ in the next round. This allows the strategy to "test the waters" and restart cooperation if the group behavior has shifted back toward prosociality, preventing permanent defection traps.

**3. Boundary and Edge Cases:**
*   **Round 1:** Always Cooperate (C). This establishes the intention for mutual benefit.
*   **Final Round ($t = r$):** Defect (D) if the previous round's cooperation rate $R_{t-1} \le 0.5$. If $R_{t-1} > 0.5$, Cooperate (C). While standard game theory suggests defecting in the final round, this strategy maintains consistency with the established cooperative equilibrium to maximize group utility unless the group has already collapsed.
*   **Small $n$ dynamics:** If $n=2$, the threshold $R_{t-1} > 0.5$ effectively reduces to "if the opponent cooperated last round, cooperate." If $n$ is large, the threshold ensures that one or two defectors do not immediately collapse the strategy.
'''

description_PROSOCIAL_12 = '''
The strategy employs a conditional cooperation model with a forgiving trigger mechanism, designed to establish mutual cooperation while protecting against persistent exploitation.

**Phase 1: Initialization**
In the first round (t=1), play C.

**Phase 2: Adaptive Response (Rounds 2 to r-1)**
For each round $t$, calculate the contribution of the $n-1$ opponents in the previous round ($t-1$). Let $S_{t-1}$ be the total number of cooperators in the previous round.
Let $C_{i, t-1}$ be your own action in the previous round (1 for C, 0 for D).
The number of opponents who cooperated is $O_{t-1} = S_{t-1} - C_{i, t-1}$.

*   **Cooperation Rule:** If $O_{t-1} \ge \lceil (n-1) \times \frac{1}{k} \rceil$, play C. This threshold ensures that if everyone else follows this same rule, cooperation is individually rational, as the marginal benefit of contributing ($k/n$) exceeds the marginal cost (1) only when a sufficient quorum is met.
*   **Defection Rule (Retaliation):** If $O_{t-1} < \lceil (n-1) \times \frac{1}{k} \rceil$, play D. This serves as a punishment mechanism to discourage non-cooperative behavior.
*   **Forgiveness Mechanism:** If the previous round resulted in defection ($O_{t-1} < \text{threshold}$), revert to C if the total cooperation count $S_{t-1}$ exceeds $O_{t-1}$ by a margin sufficient to suggest a potential return to prosociality (i.e., if you defected previously, but your defection was not the sole cause of the group failure). Specifically, if you played D in $t-1$ and $O_{t-1} \ge \lceil (n-1) \times \frac{1}{k} \rceil - 1$, play C.

**Phase 3: Final Round (Round r)**
In the final round, play D, regardless of previous history. This accounts for the lack of future incentives to maintain reputation or punish defectors, ensuring the strategy remains robust against end-game exploitation.

**Edge Case Handling:**
*   **If $n$ or $k$ makes the cooperation threshold undefined or impossible:** If $\lceil (n-1) \times \frac{1}{k} \rceil > n-1$, always play D.
*   **Initial Defection:** If the group fails to sustain cooperation in round 1, revert to D for one round to signal intolerance for free-riding, then test cooperation again in the subsequent round.
'''

description_PROSOCIAL_13 = '''
The strategy employs a conditional cooperation model incorporating a "probabilistic test" phase and an "adaptation threshold" to maintain long-term cooperation while minimizing exploitation.

### Core Logic
The strategy maintains a target cooperation state based on the observed group behavior of the previous round. It defines `C_count` as the number of cooperators observed in the previous round, excluding self-contribution if known, or including it if only the total aggregate is visible.

**Pseudocode:**

```python
# Strategy Variables
state = "COOPERATE"  # Initial state
trust_threshold = 0.5 # Threshold fraction of group cooperation to sustain trust

def decide_action(round_number, total_rounds, last_round_cooperators):
    # Round 1: Always initiate with cooperation
    if round_number == 1:
        return "C"

    # Final Round: Defect to prevent exploitation
    if round_number == total_rounds:
        return "D"

    # Evaluate group behavior
    # Calculate cooperation density (excluding self if possible, 
    # otherwise use total_group_cooperation / n)
    group_density = last_round_cooperators / n
    
    # Adaptive Trigger
    # If the group density is high, maintain cooperation
    if group_density >= trust_threshold:
        return "C"
    
    # If the group density falls below the threshold, 
    # trigger a retaliatory defect to punish non-cooperation 
    # and encourage re-alignment
    else:
        return "D"
```

### Strategy Components

**1. Initialization (Round 1)**
Always play `C`. This establishes a prosocial signal and tests the collective willingness to cooperate without prior negative history.

**2. Conditional Sustenance (Rounds 2 to r-1)**
Calculate the `group_density` from the previous round. If the collective cooperation level meets or exceeds the `trust_threshold` (defined as 0.5, or n/2), continue to play `C`. This reinforces positive social norms and maximizes total group utility when the group is functional.

**3. Retaliation (Rounds 2 to r-1)**
If `group_density` falls below the `trust_threshold`, switch to `D` for the immediate next round. This serves as a "tit-for-tat" mechanism against non-cooperators. Because the game is anonymous, retaliation is indiscriminate; however, switching to `D` protects the player from exploitation when the group environment deteriorates. If the group returns to `C` in subsequent rounds (meaning others also switched to `C` or the defectors are outnumbered), the strategy immediately resumes `C` in the following round.

**4. Termination (Round r)**
Play `D`. In finite repeated games, the incentive to cooperate collapses in the final round as there is no future punishment for defection. Defecting in the final round is a defensive measure to avoid being the only cooperator when others inevitably defect, thereby securing the maximum possible payoff given the game's finite nature.
'''

description_PROSOCIAL_14 = '''
### Strategy: Conditional Tit-for-Tat with Forgiving Escalation

**1. Initial State (Round 1)**
Play C (Cooperate).

**2. Recursive Decision Rules (Rounds 2 to r)**
Let $S_{t-1}$ be the number of cooperators in the previous round.
Let $T_{t-1} = S_{t-1} - c_{t-1}$ be the number of opponents who cooperated in the previous round, where $c_{t-1} \in \{0, 1\}$ is your own action in the previous round.

Calculate the average opponent cooperation rate from the previous round: $\rho_{t-1} = \frac{T_{t-1}}{n-1}$.

*   **If $\rho_{t-1} \ge 0.5$:** Play C (Cooperate).
*   **If $0 < \rho_{t-1} < 0.5$:** Play C (Cooperate) with probability $\rho_{t-1}$ (stochastic forgiveness), otherwise play D.
*   **If $\rho_{t-1} = 0$:** Play D (Defect) for exactly one round to penalize defection, unless the previous round was the final round (see below).

**3. Last Round Adjustment (Round r)**
Regardless of the decision rule above, if $t = r$:
*   If the strategy has cooperated in $\ge 50\%$ of previous rounds, play C.
*   Otherwise, play D.

**4. Edge Cases**
*   **Punishment Exception:** If you played D in round $t-1$ because $\rho_{t-2} = 0$, and in round $t-1$ you observe $\rho_{t-1} > 0$ (indicating others have begun cooperating), immediately revert to C in round $t$ regardless of the probability threshold.
*   **High Sensitivity:** If $k > n/2$ (a "strong" public good), always play C unless $\rho_{t-1} = 0$ for two consecutive rounds, in which case switch to D until $\rho > 0$ is observed again.
'''

description_PROSOCIAL_15 = '''
**Strategy: Tit-for-Tat with Conditional Forgiveness (TFT-CF)**

This strategy operates on the principle of conditional cooperation, maintaining prosocial engagement as long as the aggregate behavior of the group remains sufficiently cooperative, while protecting against exploitation.

**Decision Rules:**

Let $C_{total, t-1}$ be the total number of players who cooperated in the previous round, and $n$ be the number of players.

1.  **First Round ($t=1$):** Cooperate ($C$).

2.  **Subsequent Rounds ($t > 1$):**
    *   Calculate the cooperation threshold $T = \lceil n \cdot (1/k) \rceil$.
    *   If the previous round's cooperation count $C_{total, t-1}$ meets or exceeds the cooperation threshold ($C_{total, t-1} \geq T$), Cooperate ($C$).
    *   If the previous round's cooperation count $C_{total, t-1}$ falls below the cooperation threshold ($C_{total, t-1} < T$), Defect ($D$).

3.  **Last Round ($t = r$):** Apply the same decision rules as standard subsequent rounds. There is no automatic defection on the final turn; the strategy remains conditional on the performance of the group in the penultimate round.

**Handling Exploitation and Recovery:**

If the strategy defects due to low group cooperation ($C_{total, t-1} < T$), it continuously monitors the next round. If the group cooperation rebounds and returns to the threshold ($C_{total, t} \geq T$), the strategy immediately resumes cooperation in the following round ($t+1$). This ensures the strategy is resilient to temporary lapses in group coordination while remaining capable of re-establishing cooperation if the collective behavior improves.

**Pseudocode:**

```
// Constants: n, k, r are provided parameters
// Threshold: T = ceil(n / k)
// Memory: last_round_cooperators = 0

// Round 1
Action = C

// Rounds 2 through r
If t > 1:
    If last_round_cooperators >= T:
        Action = C
    Else:
        Action = D

// Update memory after each round
last_round_cooperators = Observed_C_total
```
'''

description_PROSOCIAL_16 = '''
### Adaptive Prosocial Tit-for-Tat Strategy

**Phase 1: Initialization**
In the first round (t=1), always cooperate (C). This establishes an initial signal of prosocial intent.

**Phase 2: Adaptive Decision Logic**
For all subsequent rounds (t > 1), determine the cooperation decision based on the previous round’s aggregate data (C_prev, the total number of cooperators observed in round t-1). Let `threshold` be the required number of cooperators for reciprocity: `threshold = ceil(n * (1 / k))`. 

If the public goods benefit is marginal (i.e., your contribution increases the group return by less than it costs you individually, which is always true since $k < n$), enforce a strict reciprocity condition. Cooperate if and only if the cooperation rate in the previous round was sufficient to sustain mutual benefit.

**Pseudocode:**
```python
def decide_action(t, n, k, C_prev):
    if t == 1:
        return 'C'
    
    # Calculate critical mass: the minimum number of cooperators
    # required to make cooperation individually rational (net payoff >= 1)
    # Payoff of C: (k/n) * C_total
    # Payoff of D: 1 + (k/n) * (C_total - 1)
    # C is rational if (k/n) * C_total >= 1 + (k/n) * (C_total - 1)
    # This simplifies to: (k/n) >= 1
    # Since k < n, individual rationality never holds strictly.
    # Therefore, reciprocity relies on group-level return.
    
    # Define success as the group achieving at least 50% cooperation 
    # or the previous round's cooperation count C_prev >= threshold.
    threshold = n / 2 
    
    if C_prev >= threshold:
        return 'C'
    else:
        return 'D'
```

**Phase 3: Terminal Round Handling**
In the final round (t=r), the incentive to defect is maximized because there are no future rounds to punish defection. However, to remain prosocial, maintain the adaptive logic defined in Phase 2. Do not automatically defect in the final round unless the group has demonstrated a consistent failure to reciprocate. If the group has cooperated at or above the threshold in at least 75% of previous rounds, cooperate in the final round regardless of the previous round's outcome to signal continued trust.

**Edge Cases & Failure Recovery:**
1.  **Mass Defection:** If C_prev = 0, switch to D for the subsequent round. Then, attempt to restart cooperation at probability p=0.2 in the next round. If the restart succeeds (C_prev > 0), revert to the adaptive logic in Phase 2.
2.  **Fluctuating Cooperation:** If the group's cooperation rate oscillates around the threshold, maintain the previous action to avoid creating instability.
'''

description_PROSOCIAL_17 = '''
**Strategy Definition:**

The strategy employs a conditional cooperation mechanism based on a "tit-for-tat with forgiveness and threshold-based adjustment" logic. It aims to stabilize mutual cooperation while protecting against persistent defectors.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)** to initiate cooperative norms.
2.  **Subsequent Rounds:**
    *   Calculate the average contribution rate of all other players in the previous round: `Avg_Others = (Total_Contributions_Previous - Own_Contribution_Previous) / (n - 1)`.
    *   If `Avg_Others >= Threshold`, play **Cooperate (C)**.
    *   If `Avg_Others < Threshold`, play **Defect (D)**.
3.  **Threshold Logic:**
    *   The `Threshold` is defined as `(n - k) / (n - 1)`. This represents the minimum cooperation level required from others for your own cooperation to yield a net social utility greater than or equal to defecting (i.e., breaking even or better).
4.  **Forgiveness/Resurrection Clause:**
    *   If the strategy defected in the previous round due to low cooperation, observe the most recent round’s `Avg_Others`.
    *   If `Avg_Others` rises above the `Threshold` in any round following a defection, revert to **Cooperate (C)** immediately in the next round.
5.  **Terminal Round Adjustment:**
    *   In the final round (`t = r`), disregard the `Threshold` rule and play **Defect (D)** to prevent exploitation by opponents who might switch to defection, unless the cooperation history in the previous `r-1` rounds has been perfect (all players cooperated in every round). If cooperation has been perfect, play **Cooperate (C)** to maintain the social optimum until the game concludes.

**Pseudocode:**

```python
def get_action(round, n, k, history):
    threshold = (n - k) / (n - 1)

    if round == 1:
        return 'C'

    if round == r:
        if history.is_perfect_cooperation():
            return 'C'
        else:
            return 'D'

    # Retrieve data from round - 1
    total_cooperators = history.last_round_total_cooperators
    own_last_action = history.last_round_my_action
    
    # Calculate cooperation rate of opponents
    if own_last_action == 'C':
        avg_others = (total_cooperators - 1) / (n - 1)
    else:
        avg_others = total_cooperators / (n - 1)

    # Decision based on threshold
    if avg_others >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_18 = '''
Cooperate in the first round (t=1). In all subsequent rounds (t > 1), cooperate if and only if the contribution rate of the group in the previous round (t-1) met or exceeded a prosocial threshold; otherwise, defect.

**Decision Rules:**

1. **Round 1:** Play C.
2. **Rounds 2 to r:**
   - Let $C_{t-1}$ be the number of players who cooperated in the previous round.
   - Calculate the observed contribution rate $\rho = C_{t-1} / n$.
   - Cooperate (C) if $\rho \ge \tau$, where $\tau = k/n$.
   - Defect (D) if $\rho < \tau$.
3. **Final Round (r):** Follow the decision rule for round $r$ based on the aggregate results of round $r-1$. No special end-game defection strategy is employed, as the goal is to sustain cooperation through consistent reciprocity rather than exploiting the finite horizon.

**Edge Cases:**

- If $C_{t-1} = 0$, immediately default to Defect (D) for the current round, as the group has collapsed into a non-cooperative state.
- If the strategy observes a state of total cooperation ($C_{t-1} = n$), maintain C regardless of the specific $k/n$ threshold.
- If $n$ is small (e.g., $n=2$ or $n=3$), the threshold $\tau = k/n$ remains the primary decision metric to ensure that individual contributions are still "profitable" to the group, preventing unconditional cooperation against exploiters.

**Pseudocode:**

```python
def decide_action(t, n, k, history):
    if t == 1:
        return 'C'
    
    # history contains the aggregate C_count from previous rounds
    last_C_count = history[t-2] 
    
    # Threshold for prosocial stability
    threshold = k / n 
    observed_rate = last_C_count / n
    
    if observed_rate >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_19 = '''
Play according to a "Contingent Tit-for-Tat" algorithm. Let $N_c(t)$ be the total number of cooperators observed in round $t$. Let $M$ be a target threshold for cooperation, defined as $M = \lceil \frac{n}{k} \rceil$.

1.  **Round 1:** Play $C$ (Cooperate).

2.  **Rounds $t = 2$ to $r-1$:**
    *   If $N_c(t-1) \geq M$, play $C$.
    *   If $N_c(t-1) < M$, play $D$ (Defect).

3.  **Round $r$ (Final Round):**
    *   If $N_c(t-1) \geq M$, play $C$.
    *   If $N_c(t-1) < M$, play $D$.

4.  **Reciprocity Adjustment (Memory Decay):**
    To avoid permanent defection spirals caused by single-round noise or low-contribution events, if you have played $D$ for three consecutive rounds and $N_c(t)$ was strictly increasing over those three rounds, play $C$ in the next round to test for re-cooperation, regardless of the previous threshold result. Otherwise, default to the threshold decision rule in step 2.
'''

description_PROSOCIAL_20 = '''
The strategy utilizes a conditional cooperation approach with a trigger for defectors, balanced by a "forgiving" adjustment mechanism.

**Definitions:**
- Let $C_t$ be the number of cooperators observed in round $t$.
- Let $N_{opponents} = n - 1$.
- Let $k_{eff} = k/n$.
- Define the Cooperation Threshold $T = 1/k_{eff}$. This is the minimum number of total cooperators required in a round for a cooperator to break even (i.e., when total contributions $S \ge n/k$).

**Decision Logic:**

1.  **First Round:**
    Play $C$ (Cooperate).

2.  **Subsequent Rounds ($t > 1$):**
    Calculate the total number of cooperators from the previous round $C_{t-1}$.

    *   **Case 1: Total Cooperation.** If $C_{t-1} = n$, continue to play $C$.
    *   **Case 2: Partial Cooperation.** If $C_{t-1} \ge T$, play $C$. This maintains the public good provision where the individual benefit of cooperating is non-negative.
    *   **Case 3: Below Threshold.** If $C_{t-1} < T$, play $D$ (Defect) for the current round $t$. This protects against exploitation when the aggregate contribution level does not provide a positive return.

3.  **Forgiveness/Re-entry (The "Reset" Mechanism):**
    If the strategy played $D$ in round $t$ due to the previous round falling below $T$, attempt to re-establish cooperation in round $t+1$ with a probability $p = 0.1$. If the random check passes, play $C$; otherwise, continue playing $D$. This allows the system to recover from cycles of mutual defection if opponents are also using conditional cooperation strategies.

4.  **Last Round:**
    If the strategy is currently cooperating (playing $C$), play $C$. If the strategy is currently defecting, continue to play $D$. This ensures consistency and prevents unconditional defection in the final round, which might trigger retaliatory behavior in the preceding rounds if opponents are monitoring aggregate contributions.

**Pseudocode:**

```python
def decide_action(round_number, total_cooperators_prev_round, n, k):
    threshold = n / k
    
    if round_number == 1:
        return 'C'
    
    # Analyze if previous round yielded a positive return for cooperators
    if total_cooperators_prev_round >= threshold:
        return 'C'
    
    # If below threshold, initiate punishment/protection
    # Try to re-enter cooperation occasionally to signal willingness
    if random.random() < 0.1:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_21 = '''
The strategy employs a conditional cooperation model with forgiveness, designed to initiate mutual cooperation while shielding against exploitation. Let $S_t$ be the number of cooperators observed in round $t$. Let $C_i$ denote your own action in round $t$, where $C=1$ (contribute) and $D=0$ (defect).

**Decision Rules:**

1.  **Round 1:** Always play C (contribute).
2.  **Rounds 2 to $r-1$:**
    *   Calculate the average contribution rate of opponents in the previous round: $A_{t-1} = (S_{t-1} - C_{i, t-1}) / (n - 1)$.
    *   If $A_{t-1} \ge \tau$, play C.
    *   If $A_{t-1} < \tau$, play D.
    *   The threshold $\tau$ is defined as $1/k$. This threshold represents the break-even point where the marginal benefit of your contribution equals its cost.
3.  **Round $r$ (Final Round):**
    *   Defect (play D) if the cumulative payoff variance suggests high risk of exploitation, or to prevent last-round losses.
    *   More specifically: If $S_{r-1} > 0$ and the average opponent contribution rate $A_{r-1} \ge \tau$, play C. Otherwise, play D.

**Edge Case Handling:**

*   **Initial Defection:** If the group fails to reach $S_t \ge 1$ in early rounds, immediately switch to D for all subsequent rounds to prevent total loss.
*   **Forgiveness:** If the group switches back to cooperation after a period of defection (i.e., $A_{t-1} \ge \tau$ again), the strategy resumes playing C in the subsequent round.
*   **The Last-Round Problem:** To avoid the rational temptation to defect in the final round, the strategy incorporates a "tit-for-tat" lookback. If the group has maintained a consistent average cooperation rate $A \ge \tau$ for the majority of the game (defined as $> 50\%$ of previous rounds), play C in the final round even if the previous round was a slight dip. Otherwise, default to D.

**Pseudocode:**

```python
threshold = 1 / k

if round == 1:
    return C

# Look at previous round
opponents_cooperated = S_prev - my_last_action
avg_opp_coop = opponents_cooperated / (n - 1)

if round < r:
    if avg_opp_coop >= threshold:
        return C
    else:
        return D

if round == r:
    # Check if history warrants last-round trust
    # 'coop_history' is the count of rounds where avg_opp_coop >= threshold
    if coop_history > (r / 2) and avg_opp_coop >= threshold:
        return C
    else:
        return D
```
'''

description_PROSOCIAL_22 = '''
The strategy is a conditional-cooperation tit-for-tat variant designed to sustain prosocial outcomes while protecting against exploitation.

**Initialization (Round 1):**
Play C (Cooperate).

**General Decision Rule (Rounds 2 to r-1):**
Let *C_total* be the total number of cooperators observed in the previous round.
Let *n* be the total number of players and *C_expected* be the number of cooperators observed in the round prior to that (or *n* if it is round 2).

Calculate the Cooperation Threshold (*T*):
*T* = max(1, *n* × (1 / *k*))

If *C_total* ≥ *T*:
Play C (Cooperate).

If *C_total* < *T*:
Play D (Defect).

**Terminal Phase (Round r):**
If the total number of cooperators in round *r-1* was greater than or equal to *T*, play C. Otherwise, play D.

**Logic:**
The threshold *T* is derived from the payoff structure. In this game, cooperating is individually rational only if the number of other cooperators is sufficient to return at least the value of the endowment kept (which is 1). The break-even point occurs when (k/n) * C_total ≥ 1, which simplifies to C_total ≥ n/k. By setting the threshold at or slightly above this value, the strategy cooperates only when the group size provides a net positive or neutral return on cooperation, effectively punishing defectors when they drag the group cooperation level below the sustainability threshold while maintaining a prosocial stance when the group demonstrates collective goodwill.
'''

description_PROSOCIAL_23 = '''
The strategy follows a conditional cooperation framework known as "Adaptive Trigger Tit-for-Tat," which balances the promotion of mutual cooperation with protection against exploitation.

**Decision Rules**

Let $C_{t-1}$ be the number of cooperators observed in the previous round, excluding oneself.
Let $T_{t-1} = C_{t-1} + c_{t-1}$ be the total number of cooperators in the previous round, where $c_{t-1}$ was your own action (1 for C, 0 for D).

The strategy proceeds as follows:

*   **Round 1:** Play $C$. Initiate cooperation to signal a prosocial intent and establish a foundation for collective gain.

*   **Rounds 2 through $r-1$:**
    *   If $T_{t-1} \ge n/2$: Play $C$. When the group demonstrates a strong or majority preference for cooperation, reciprocate to maintain and encourage the collective benefit.
    *   If $0 < T_{t-1} < n/2$: Play $C$ with probability $P = T_{t-1}/(n-1)$. This probabilistic response rewards partial cooperation without fully committing to a group that is underperforming, creating pressure to increase contribution levels.
    *   If $T_{t-1} = 0$: Play $D$. If the group has collapsed into total defection, cease cooperation to avoid unilateral exploitation.

*   **Round $r$ (The Final Round):**
    *   If $T_{r-1} \ge n/2$: Play $C$. Maintain the cooperative equilibrium even in the final round to avoid triggering a "defection cascade" if others are using similar logic.
    *   If $T_{r-1} < n/2$: Play $D$. Since there are no future rounds to influence, maximize personal payoff against a group that has failed to sustain cooperation.

**Edge Case Handling**

*   **Sudden Collapse:** If, in any round $t < r$, the number of cooperators drops to zero ($T_{t-1} = 0$), the strategy shifts to an "Observation Mode." For the next round ($t+1$), play $D$. If $T_{t} > 0$ in that subsequent round, resume the standard decision rules in round $t+2$ as if the previous cooperation had occurred. This allows for recovery if a single defector caused a temporary dip, but avoids exploitation if the group has abandoned cooperation.
*   **Calculating Expected Thresholds:** If the division $n/2$ results in a non-integer, use $n/2$ rounded up as the threshold for strong cooperation.
'''

description_PROSOCIAL_24 = '''
Strategy: Trigger-Based Tit-for-Tat with Forgiving Resilience

Maintain a persistent state variable, `trust_level`, initialized to 0.5 (on a scale of 0.0 to 1.0). The decision to cooperate in round `t` depends on the current `trust_level` and the observed cooperation rate of the population in the previous round, `avg_cooperation_prev` = (Σ c_j) / n.

1. Round 1:
   Always play Cooperate (C).

2. Rounds 2 to r-1:
   Update `trust_level` based on the observed outcome of the previous round:
   - If `avg_cooperation_prev` >= `trust_level`, increase `trust_level` by 0.1 (capped at 1.0).
   - If `avg_cooperation_prev` < `trust_level`, decrease `trust_level` by 0.2 (floor at 0.0).

   Decision Rule:
   - If `trust_level` >= 0.5, play Cooperate (C).
   - If `trust_level` < 0.5, play Defect (D) for one round, then reset `trust_level` to 0.5 for the following round to test for cooperation again.

3. Final Round (r):
   If `trust_level` >= 0.5, play Cooperate (C). Otherwise, play Defect (D).

Pseudocode implementation:

```
trust_level = 0.5

for round in 1 to r:
    if round == 1:
        action = C
    else:
        # Update logic based on previous round's performance
        prev_C_count = observed_total_cooperators_from_last_round
        avg_cooperation_prev = prev_C_count / n
        
        if avg_cooperation_prev >= trust_level:
            trust_level = min(1.0, trust_level + 0.1)
        else:
            trust_level = max(0.0, trust_level - 0.2)
        
        # Decision Logic
        if round == r:
            action = C if trust_level >= 0.5 else D
        else:
            if trust_level >= 0.5:
                action = C
            else:
                action = D
                # Forgiveness mechanism: reset to allow re-entry
                trust_level = 0.5 
```
'''

description_PROSOCIAL_25 = '''
The strategy employs a conditional cooperation mechanism known as "Trigger-Adjusted Tit-for-Tat," designed to foster cooperation while protecting against persistent exploitation.

**State Variables:**
- $C_{prev}$: The total number of players who cooperated in the previous round (including self).
- $k/n$: The return multiplier per contributor.
- $r_{rem}$: Number of rounds remaining.

**Initialization (Round 1):**
Play C (Cooperate).

**Decision Rules for Rounds $t = 2$ to $r-1$:**
1. Calculate the "target contribution" threshold: If the previous round's total cooperation $C_{prev}$ was $\geq \lceil n/k \rceil$, cooperation is potentially profitable.
2. If $C_{prev} \geq \text{threshold}$, play C (Cooperate).
3. If $C_{prev} < \text{threshold}$, play D (Defect) with probability $p$, where $p$ is a "forgiveness" parameter (e.g., 0.1) to allow for re-entry into cooperation if opponents were merely noise-testing, or simply switch to D to punish the group. Specifically: Play D if $C_{prev}$ falls below the threshold needed for the public good to return a net gain ($\pi_i \geq 1$).

**Decision Rules for Final Round ($t = r$):**
1. If the game history shows consistent high cooperation (defined as $\text{average}(C_{prev}) > n/2$ over the previous 75% of rounds), play C.
2. Otherwise, play D.

**Edge Cases & Adaptive Logic:**
- **Punishment Mechanism:** If, after a round of D, the subsequent round shows an increase in $C_{prev}$ back above the threshold, immediately revert to C to signal a desire for restoration of the cooperative equilibrium.
- **Exploitation Guard:** If $C_{prev}$ is consistently zero or near-zero for three consecutive rounds, switch to D for the remainder of the game, regardless of any signals, as the population is non-cooperative.
- **Low-Yield Threshold:** If $k/n \leq 1/n$, the game structure prevents any cooperative outcome from exceeding the payoff of defection; in this specific case, play D for all rounds.

**Pseudocode:**

```python
threshold = ceil(n / k)

if t == 1:
    return C
    
if t == r:
    if history.avg_cooperation > (n / 2):
        return C
    else:
        return D

if history.last_three_rounds_all_zero():
    return D

if C_prev >= threshold:
    return C
else:
    return D
```
'''

description_PROSOCIAL_26 = '''
For the first round, cooperate (C).

For all subsequent rounds (t > 1), adopt a conditional cooperation strategy based on the observed aggregate contribution history of the other players.

Let $C_{t-1}$ be the number of cooperators observed in round $t-1$. Calculate the "cooperation threshold" $T$ as $n \times (1/k)$. If $k$ is such that $T$ is not an integer, round up to the nearest integer.

The decision rule is as follows:

1.  If $t = r$ (the final round), defect (D). This accounts for the lack of future incentives to maintain cooperation.
2.  If $t < r$:
    *   Calculate the average contribution level observed over all previous rounds: $\bar{C} = \frac{1}{t-1} \sum_{j=1}^{t-1} C_j$.
    *   If $\bar{C} \ge T$, cooperate (C).
    *   If $\bar{C} < T$, defect (D).

To handle stochasticity and noise in opponent behavior, incorporate a "forgiveness" mechanism. If the strategy is currently defecting because $\bar{C} < T$, check the most recent round $C_{t-1}$. If $C_{t-1} \ge T$ (indicating a sudden shift toward prosocial behavior by the group), ignore the average and cooperate (C) for one round to test if the group is sustaining this new level of cooperation.

Pseudocode:

```python
threshold = ceil(n / k)

def strategy(round_t, history_C):
    if round_t == r:
        return 'D'
    
    if round_t == 1:
        return 'C'
        
    avg_prev_C = sum(history_C) / (round_t - 1)
    last_C = history_C[-1]
    
    # Forgiveness/Re-engagement clause
    if last_C >= threshold:
        return 'C'
        
    # Standard conditional cooperation
    if avg_prev_C >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_27 = '''
The strategy utilizes a conditional "Win-Stay, Lose-Shift" logic modified for multi-player dynamics, aiming to establish cooperative equilibrium by rewarding cooperation and punishing defection, while preemptively adjusting for the final round.

**Initialization and First Round:**
Cooperate (C) in the first round to signal a willingness to establish a cooperative group norm.

**Decision Logic for Subsequent Rounds (t = 2 to r-1):**
Observe the total number of cooperators from the previous round (S_{t-1}).

1. Calculate the contribution of the opponents in the previous round: O_{t-1} = S_{t-1} - c_{t-1}.
2. Compare the payoff received in the previous round (π_{t-1}) against the payoff that would have been received had I defected (π_{D,t-1}).
   - π_{t-1} = (1 - c_{t-1}) + (k/n) * S_{t-1}
   - π_{D,t-1} = 1 + (k/n) * S_{t-1}
3. Define the "Cooperation Threshold" (T): If the number of other cooperators (O_{t-1}) is sufficiently high to make cooperation personally beneficial (or neutral) compared to the alternative, maintain cooperation. Specifically, evaluate if:
   - (k/n) * (O_{t-1} + 1) >= 1
   - This simplifies to: O_{t-1} >= (n/k) - 1.

**Strategy Pseudocode:**

```
if t == 1:
    return C

# Calculate effective contributions of others from last round
others_cooperated = total_cooperators_last_round - my_action_last_round

# Determine if cooperation was locally optimal
threshold = (n / k) - 1

if t == r:
    # Final round: Pure Defection (Nash Equilibrium for finite game)
    # unless history suggests a high probability of reciprocal cooperation
    if others_cooperated > (n / 2):
        return C
    else:
        return D

else:
    # Intermediate rounds: Reciprocal conditional cooperation
    if others_cooperated >= threshold:
        return C
    else:
        # If cooperation is below threshold, punish by defecting
        return D
```

**Edge Cases and Adjustments:**

*   **The Final Round (t = r):** The strategy defaults to defecting (D) to prevent exploitation, as there are no future rounds to incentivize. However, if the history of the game (all previous rounds) shows that the majority of players have consistently cooperated (others_cooperated > n/2), switch to C to maximize collective welfare, assuming a high probability of reciprocal cooperative intent.
*   **Threshold Interpretation:** If (n/k) - 1 results in a non-integer, round up. For example, if n=6 and k=2, threshold = (6/2) - 1 = 2. If 2 or more opponents cooperated, the investment is justified, and cooperation continues.
*   **Adaptation:** If the game starts with high defection, the strategy will defect until a round occurs where cooperation exceeds the threshold, at which point it immediately attempts to resume the cooperative cycle.
'''

description_PROSOCIAL_28 = '''
**Strategy: Adaptive Reciprocal Cooperation**

This strategy employs a "Conditional Tit-for-Tat" mechanism based on the observed cooperation level of the group, aiming to maximize prosocial outcomes while protecting against exploitation.

**Decision Rules:**

1.  **First Round:** Play **Cooperate (C)**.

2.  **Subsequent Rounds:** Let $C_{prev}$ be the number of cooperators in the previous round.
    *   Calculate the threshold $T = \lceil n \times (1/k) \rceil$.
    *   If $C_{prev} \ge T$, play **Cooperate (C)**.
    *   If $C_{prev} < T$, play **Defect (D)**.

3.  **Last Round:**
    *   If $r$ is the final round, play **Defect (D)**, unless the group has maintained a full cooperation rate ($C_{prev} = n$) for the previous $r-1$ rounds, in which case play **Cooperate (C)** to support unconditional cooperation.

**Pseudocode Logic:**

```python
if current_round == 1:
    action = C
elif current_round == r:
    if history_of_full_cooperation:
        action = C
    else:
        action = D
else:
    # Threshold based on the payoff break-even point for the group
    # where the public return covers the private cost of contribution.
    threshold = ceil(n / k)
    
    if last_round_cooperators >= threshold:
        action = C
    else:
        action = D
```

**Adaptive Logic and Edge Cases:**

*   **Forgiveness:** The strategy is inherently forgiving. If the group meets the threshold, cooperation resumes immediately. It does not punish past defections if the group returns to a collectively beneficial level of contribution.
*   **Threshold Rationale:** The threshold $n/k$ represents the minimum number of contributors required for the public good return to be greater than or equal to the individual cost of contributing. Operating at or above this threshold ensures that contributing is rational for the group utility.
*   **Exploitation Defense:** If the group fails to sustain a sufficient number of contributors (falling below the threshold), the strategy defects to minimize personal loss while the public good is undersupplied.
*   **Endgame Dynamics:** The strategy accounts for the "unravelling" effect of finite games by defaulting to defection in the final round, unless the group has proven to be perfectly cooperative throughout the history of the game, rewarding that stability.
'''

description_PROSOCIAL_29 = '''
Adopt a "Conditional Tit-for-Tat with Forgiveness" strategy based on the observed public cooperation level.

**Parameters and Variables:**
*   $T$: Current round number.
*   $R$: Total rounds.
*   $C_{t-1}$: Number of cooperators observed in the previous round.
*   $Threshold$: A target number of cooperators required to maintain cooperation, calculated as $\lceil (n/k) \rceil$. This value represents the minimum number of cooperators needed to make the public contribution break even or profit for the group.

**Decision Rules:**

1.  **Round 1:** Always play Cooperate (C).

2.  **Round $T$ (where $1 < T < R$):**
    *   If $C_{t-1} \geq Threshold$: Play Cooperate (C).
    *   If $C_{t-1} < Threshold$: Play Defect (D).
    *   **Forgiveness Mechanism:** If the strategy previously defected due to a low contribution count, revert to Cooperate (C) with a probability of 0.1 in the current round to test for renewed cooperation among opponents.

3.  **Final Round ($T = R$):**
    *   If the strategy defected in the previous round ($T-1$), play Defect (D).
    *   If the strategy cooperated in the previous round, play Cooperate (C).

**Pseudocode:**

```python
def decide_action(T, R, C_prev, n, k):
    threshold = ceil(n / k)
    
    if T == 1:
        return C
    
    if T == R:
        return last_action_was_C ? C : D
        
    if C_prev >= threshold:
        return C
    else:
        # Check for re-entry attempt
        if random() < 0.1:
            return C
        return D
```
'''

description_PROSOCIAL_30 = '''
The strategy employs a "Conditional Tit-for-Tat with Forgiveness" approach, optimized for the N-player structure by tracking the average contribution rate of the group.

**Initialization**
In the first round (t=1), cooperate.

**Round-by-Round Decision Logic**
For rounds t=2 to r-1:
1. Calculate the contribution rate of the previous round: $C_{t-1} = (\text{Total Contributors}) / n$.
2. Maintain a running threshold $T$, which represents the minimum acceptable contribution rate to sustain cooperation. Set $T = 0.5$ initially.
3. If $C_{t-1} \ge T$, cooperate.
4. If $C_{t-1} < T$, defect.
5. If the decision in the current round $t$ is "Defect" but the previous round $t-1$ saw a partial contribution (where $0 < C_{t-1} < T$), apply a "Forgiveness" trigger: cooperate with probability $P = C_{t-1} / T$. Otherwise, defect.

**The Last-Round Constraint**
In the final round (t=r), defect regardless of previous history, as there are no future rounds to incentivize cooperation, rendering the prosocial equilibrium non-enforceable.

**Adaptive Parameter Adjustment**
After each round, update the threshold $T$ to account for the efficiency of the group:
- If the previous round's outcome ($C_{t-1}$) was $1.0$ (full cooperation), decrease $T$ by $0.05$ (to a floor of $0.2$) to promote tolerance for minor errors or low-performing agents.
- If the previous round's outcome ($C_{t-1}$) was $0.0$, increase $T$ by $0.1$ (to a ceiling of $0.8$) to avoid being exploited by free-riders.
- If $T$ fluctuates, always clip the value to the range $[0.2, 0.8]$.

**Pseudocode Summary**
```
IF t == r: RETURN D
IF t == 1: RETURN C
C_prev = (Total_Contributors_t-1) / n
IF C_prev >= T:
    RETURN C
ELSE IF C_prev > 0 AND random_float() < (C_prev / T):
    RETURN C
ELSE:
    RETURN D
```
'''

description_PROSOCIAL_31 = '''
The strategy relies on a Tit-for-Tat variant adapted for N-player public goods, calibrated to encourage conditional cooperation while protecting against persistent exploitation.

**Initialization**
In the first round (t=1), cooperate. This establishes a prosocial baseline and invites mutual cooperation.

**Decision Logic**
For any round t > 1, calculate the average cooperation rate of the population from the previous round (t-1). Let $C_{t-1}$ be the total number of cooperators observed in the previous round. The population cooperation rate is $\rho_{t-1} = C_{t-1} / n$.

1. **Cooperate** if:
   - The observed cooperation rate $\rho_{t-1}$ exceeds a threshold $\tau$, where $\tau = 1/k$. This threshold represents the break-even point where the marginal benefit of contributing matches the cost of the contribution.
   - Or, if you are attempting to "re-seed" cooperation after a collapse (see Recovery Logic).

2. **Defect** if:
   - The observed cooperation rate $\rho_{t-1}$ is strictly less than $\tau$. This minimizes losses against players who are not reciprocating the public good.

**Recovery Logic (The "Olive Branch")**
If the strategy has defected for the last two consecutive rounds, attempt a single round of cooperation regardless of the previous round's data to test for renewed cooperation among opponents. If this round results in a population cooperation rate $\rho \ge \tau$, resume conditional cooperation. If not, return to defection until the end of the game or the next scheduled re-seed attempt.

**Final Round Handling**
In the final round (t=r), defect. Because there are no subsequent rounds to incentivize or punish opponents, cooperation provides no strategic utility in terms of future reciprocity.

**Pseudocode**

```
Variables:
  threshold = 1 / k
  last_action = [None for _ in range(r)]
  history_c = [0 for _ in range(r)]
  is_recovering = False

Function get_action(round_t):
  if round_t == 1:
    action = C
  elif round_t == r:
    action = D
  elif is_recovering:
    action = C
    is_recovering = False
  else:
    observed_rate = history_c[round_t - 1] / n
    if observed_rate >= threshold:
      action = C
    else:
      action = D
      # Check if we should re-seed later
      if last_action[round_t-1] == D and last_action[round_t-2] == D:
        is_recovering = True
        
  last_action[round_t] = action
  return action
```
'''

description_PROSOCIAL_32 = '''
The strategy is a threshold-based conditional cooperation mechanism designed to maximize total group welfare while minimizing exploitation. The strategy maintains two internal state variables: `cooperation_threshold` (initially set to `n/k`) and `my_cooperation_status` (initially `C`).

### Decision Rules
For each round $t \in \{1, \dots, r\}$:

1. **First Round ($t=1$):** Always play `C`.

2. **Subsequent Rounds ($t > 1$):**
   - Let $C_{t-1}$ be the number of cooperators observed in the previous round.
   - If $C_{t-1} \ge \text{cooperation\_threshold}$: Play `C`.
   - If $C_{t-1} < \text{cooperation\_threshold}$: Play `D` (the "punishment" phase).

3. **Adjustment Mechanism:**
   - If the player played `D` in round $t-1$ because the threshold was not met, and the observed $C_{t-1} > 0$, attempt to restart cooperation in round $t$ with a probability $p = \min(0.5, \frac{C_{t-1}}{n})$. If the random draw allows, play `C` and reset the `cooperation_threshold` to the observed $C_{t-1}$ to signal a willingness to stabilize at that lower level of participation.
   - If the player played `D` in round $t-1$ and observed $C_{t-1} = 0$, continue to play `D` until the final round.

4. **Terminal Phase:**
   - For the final round ($t=r$), if the player played `C` in round $r-1$ or if $C_{r-1}$ was sufficient to maintain a positive trend, play `C`. Otherwise, play `D`.

### Edge Cases
- **Low-Participation Equilibria:** If the number of cooperators falls to 0 for two consecutive rounds, switch to unconditional `D` for all remaining rounds to prevent sustained losses.
- **Threshold Calibration:** If $k/n$ is extremely low (making individual cooperation strictly irrational), the strategy defaults to `D` for all rounds to avoid unilateral loss.
- **Perfect Coordination:** If $C_{t-1} = n$ (all players cooperate), maintain `C` regardless of threshold calculations for all $t < r$.
'''

description_ALTRUISTIC_5 = '''
**Strategy: Conditional Tit-for-Tat with Altruistic Initiation**

This strategy is defined by the objective to sustain collective cooperation while minimizing exposure to exploitation. It maintains a memory of the total number of cooperators from the previous round, denoted as $C_{t-1}$.

**1. Decision Rules**

*   **Round 1:** Always Cooperate ($C$). The strategy initiates with a commitment to the public good to signal cooperation potential.
*   **Round $t$ (where $1 < t < r$):**
    *   If the previous round's cooperation count $C_{t-1}$ reached a threshold of cooperation defined as $C_{threshold} = \lceil n \cdot \frac{1}{k} \rceil$, then Cooperate ($C$). This threshold represents the break-even point where the marginal benefit of contributing equals or exceeds the private gain of defecting.
    *   If $C_{t-1} < C_{threshold}$, then Defect ($D$). This functions as a "punishment" phase for low group contribution.
*   **Round $r$ (Last Round):**
    *   If $C_{r-1} \geq C_{threshold}$, Cooperate ($C$).
    *   If $C_{r-1} < C_{threshold}$, Defect ($D$).
    *   *Note:* While standard game theory suggests defecting in the final round (the "unravelling" problem), this altruistic strategy remains consistent with its previous round's logic to signal sustained trustworthiness rather than opportunistic termination.

**2. Adaptive Pseudocode**

```python
# Initialization
threshold = ceil(n / k)

# Round-by-Round Logic
if t == 1:
    action = C
else:
    # Observe aggregate cooperation from previous round
    # C_prev represents the total number of cooperators in round t-1
    if C_prev >= threshold:
        action = C
    else:
        action = D
```

**3. Edge Case Handling**

*   **Threshold Calculation:** If $k$ is small, the break-even threshold $\lceil n/k \rceil$ may approach $n$. In high-threshold environments, the strategy becomes more demanding, requiring near-unanimous cooperation to maintain contribution, which prevents the strategy from subsidizing "free riders" in non-cooperative groups.
*   **Opponent Noise:** Because the strategy observes aggregate cooperation rather than individual actions, it treats the group as a single entity. It cannot identify specific defectors, so the punishment response ($D$) applies uniformly to the group. This protects against exploitation by anonymous defectors who reduce the group's efficiency.
*   **Re-initiation:** If a group returns to high levels of cooperation after a period of punishment, this strategy automatically resumes cooperation, allowing for the recovery of collective benefit without holding permanent grudges.
'''

description_ALTRUISTIC_6 = '''
**Round 1:** Play Cooperate (C).

**Round t (where 1 < t < r):** 
Let $S_{t-1}$ be the total number of cooperators in the previous round.
If $S_{t-1} \ge n/k$, play Cooperate (C).
If $S_{t-1} < n/k$, play Defect (D).

**Round r (Final Round):**
If $S_{r-1} \ge n/k$, play Cooperate (C).
If $S_{r-1} < n/k$, play Defect (D).

**Edge Case Handling:**
1. If $n/k$ is not an integer, the decision threshold for $S_{t-1}$ uses the ceiling of $n/k$ (i.e., $\lceil n/k \rceil$). 
2. If at any point the total number of cooperators $S_{t-1}$ exceeds the threshold required to make cooperation profitable for the group (specifically, where the aggregate benefit of cooperation outweighs the individual cost), continue to play C.
3. If the game reaches a state where $S_{t-1} = 0$, play Defect (D) for all remaining rounds to prevent exploitation in a scenario where others have abandoned the public good.
'''

description_ALTRUISTIC_7 = '''
**Strategy: Conditional Reciprocity with Forgiveness**

This strategy operates on the principle of conditional cooperation, seeking to maximize collective welfare while protecting against exploitation.

**1. Definitions and Initialization**
- Let $C_{t-1}$ be the number of cooperators observed in the previous round.
- Let $T$ be the total number of players $n$.
- Let $Threshold$ be a calculated value $(T/k) + \epsilon$, where $\epsilon$ is a small positive constant to ensure incentive alignment (e.g., 0.1). This represents the minimum number of cooperators required to make the act of cooperation individually rational or at least break-even.

**2. Decision Rules**
- **Round 1:** Always play $C$. This establishes a cooperative baseline and tests the potential for mutual benefit.
- **Rounds 2 to $r-1$:**
    - If $C_{t-1} \ge Threshold$: Play $C$. The group is demonstrating sufficient cooperative behavior to sustain the public good.
    - If $C_{t-1} < Threshold$: Play $D$ with probability $p = 1 - (C_{t-1} / Threshold)$. This introduces a "soft" response—punishing defection by reducing cooperation, but allowing for recovery if the group's cooperation levels rebound.
- **Round $r$:** Always play $D$. Since there is no subsequent round, the incentive to maintain the cooperative cycle is removed. Defection at the final step prevents exploitation by other agents who might defect on the final round.

**3. Handling Edge Cases and Deviations**
- **Forgiveness:** If the strategy defected in round $t-1$ due to low observed cooperation, but round $t$ observes cooperation above the $Threshold$ (e.g., others re-initiated cooperation), immediately revert to $C$ in round $t+1$. 
- **Initialization of History:** If the game provides information on average cooperation trends across the group in the first round, and that average is below the $Threshold$, switch to $D$ immediately in round 2.

**Pseudocode:**
```python
threshold = (n / k) + 0.1
if round == 1:
    action = C
elif round == r:
    action = D
else:
    if observed_cooperators_prev_round >= threshold:
        action = C
    else:
        # Probabilistic defection to signal dissatisfaction 
        # while keeping the door open for cooperation
        if random() < (1 - (observed_cooperators_prev_round / threshold)):
            action = D
        else:
            action = C
```
'''

description_ALTRUISTIC_8 = '''
### Strategy: Conditional Reciprocity with Forgiveness (CRF)

The objective is to foster cooperation through conditional altruism while mitigating exploitation by defectors. The strategy relies on observing the average contribution behavior of the group to determine the likelihood of future cooperation.

#### Decision Rules

For every round $t \in \{1, \dots, r\}$, the strategy maintains a state variable $S_t$, representing the perceived cooperativeness of the group.

1.  **Round 1 ($t=1$):**
    Always play **C**. Establish a baseline of cooperation.

2.  **Rounds $t > 1$:**
    Calculate the effective cooperation rate of the group from the previous round $t-1$:
    $$CR_{t-1} = \frac{\sum_{j \neq i} c_j}{n-1}$$
    
    Update the cooperation threshold $T$ based on the group's history:
    - If $CR_{t-1} \ge \tau$, then play **C**.
    - If $CR_{t-1} < \tau$, play **D** with probability $P_D = 1 - CR_{t-1}$ to signal disapproval, or play **C** if the group average has consistently remained high despite minor fluctuations.

    Specifically, use a running average of the group contribution $AvgCR_t = \frac{1}{t-1} \sum_{k=1}^{t-1} CR_k$.
    - Cooperate if $AvgCR_t > 0.5$ (or a custom sensitivity threshold related to $k/n$).
    - If the group total drops below the point where cooperation is profitable for the collective ($k \times \text{total contributions} < n$), revert to **D** to protect against exploitation.

3.  **The "Forgiveness" Mechanism:**
    If the strategy defected in round $t$, and the group contribution in round $t$ increases by more than 20% compared to round $t-1$, play **C** in round $t+1$. This allows for the restoration of cooperation after accidental or minor defections.

4.  **Final Round ($t=r$):**
    Regardless of history, play **D** if the game structure does not allow for long-term reputation building, *unless* the altruistic objective prioritizes collective utility over individual payoff, in which case continue to match the established cooperation rate of the previous round ($C$ if $CR_{r-1} > 0.5$, else $D$).

#### Pseudocode

```python
# Constants
# threshold_k: Minimum contribution rate to sustain a public good
threshold_k = n / k 

def get_action(round_number, history):
    if round_number == 1:
        return 'C'
    
    if round_number == r:
        # Altruistic final move: Maintain cooperation if group has been reliable
        avg_cooperation = calculate_historical_avg(history)
        return 'C' if avg_cooperation > 0.5 else 'D'

    last_round_cooperation = history[-1].group_contribution_rate
    
    # Tit-for-tat logic with altruistic buffer
    if last_round_cooperation >= threshold_k:
        return 'C'
    else:
        # Check for recovery signal (Forgiveness)
        if needs_forgiveness_trigger(history):
            return 'C'
        return 'D'
```

#### Edge Cases
- **Low Cooperation ($k < 1$ effectively):** If $k/n$ is extremely low such that $C$ is strictly dominated for the group, default to **D** immediately to avoid wasted resources.
- **Random Noise:** If the observation of $c_j$ includes small, non-systematic fluctuations, ignore any single-round drop of $< 10\%$ in total cooperation, treating it as an execution error rather than a defection signal.
'''

description_ALTRUISTIC_9 = '''
For the first round, contribute (C).

For every subsequent round $t$ (where $t > 1$):

1. Let $C_{t-1}$ be the number of cooperators in the previous round, and $n$ be the total number of players.
2. If $C_{t-1} \geq \frac{n}{k}$, then contribute (C).
3. If $C_{t-1} < \frac{n}{k}$, then defect (D).

In the final round $r$, if the previous round $C_{r-1}$ met the condition to cooperate, continue to cooperate (C). Otherwise, defect (D).

This strategy maintains cooperation as long as the aggregate group benefit exceeds the individual cost of contribution. It triggers defection only when the observed collective behavior falls below the threshold required to make cooperation individually profitable, thereby protecting the altruistic player from exploitation while signaling a willingness to sustain a mutually beneficial social equilibrium.
'''

description_ALTRUISTIC_10 = '''
**Strategy: Conditional Reciprocal Altruism**

This strategy operates on the principle of unconditional initial cooperation followed by conditional maintenance, designed to support the public good while mitigating exploitation.

**Initialization (Round 1):**
Always play Cooperate (C).

**Round T (T > 1) Execution:**
Let $C_{T-1}$ be the number of cooperators observed in the previous round.
Let $n$ be the total number of players.
Let $Threshold = \lceil n \times (1/k) \rceil$ be the minimum number of cooperators required to make universal cooperation marginally profitable or neutral compared to total defection.

Apply the following logic:

1.  **If $C_{T-1} \ge Threshold$:**
    Play Cooperate (C). Maintain cooperation as long as the aggregate contribution level is sufficient to sustain the public good or demonstrate a cooperative signal.

2.  **If $C_{T-1} < Threshold$:**
    Switch to Defect (D). If the group fails to sustain a cooperative threshold, the strategy shifts to protect against exploitation.

3.  **Recovery Clause:**
    If the strategy is currently Defecting (D) due to a previous round, monitor the group behavior for a return to cooperative norms. If the number of cooperators in the previous round ($C_{T-1}$) was $\ge Threshold$, revert to Cooperate (C).

**Final Round (Round R):**
Play Cooperate (C) if the strategy cooperated in Round $R-1$. If the strategy defected in Round $R-1$ due to insufficient participation, play Defect (D). Ignore "end-game" defection logic; maintain the cooperative signal if the group has proven reliable.

**Pseudocode:**

```python
def decide_action(round_number, n, k, history):
    # Determine the threshold for efficiency
    # Public Good benefit for player i is (k/n)*C
    # Cost of cooperation is 1. Break even at C = n/k.
    threshold = ceil(n / k)
    
    if round_number == 1:
        return 'C'
    
    previous_cooperators = history.last_round_cooperation_count
    
    if previous_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_ALTRUISTIC_11 = '''
The strategy employs a "Conditional Conditional Cooperator" approach, prioritizing group welfare while defending against exploitation.

**Initialization (Round 1):**
Play C (Cooperate). This initiates a cooperative equilibrium, signaling a willingness to contribute to the public good.

**Subsequent Rounds (t > 1):**
Observe the total cooperation count from the previous round (S_{t-1}), which includes your own contribution.

1. **Calculate the average contribution rate of opponents:**
   Let C_{prev} be the total cooperators in round t-1.
   Let m be the number of cooperators among your opponents:
   - If you played C in t-1: m = C_{prev} - 1
   - If you played D in t-1: m = C_{prev}

   Calculate the opponents' cooperation rate: p = m / (n - 1).

2. **Decision Rule:**
   - **Cooperate (C)** if p ≥ (1 / k). This threshold ensures that your contribution is mathematically justified by the collective return on investment (k * contributions / n > 1 implies contributions / n > 1/k).
   - **Defect (D)** if p < (1 / k). If the group's cooperation level is insufficient to make cooperation net-positive for the collective, switch to Defection to avoid being exploited by free-riders.

**Last Round (Round r):**
Because the game ends, the incentive for future reciprocity vanishes. However, an altruistic strategy maintains cooperation if the previous round's cooperation rate (p) was above the threshold (1/k). If p < 1/k, defect immediately.

**Edge Cases & Robustness:**
- **Incentive for forgiveness:** If you are currently defecting (D) because the group was uncooperative (p < 1/k), and the group suddenly increases cooperation such that the current state would support cooperation (p ≥ 1/k), immediately switch back to C in the next round. This allows the strategy to recover from temporary dips in group cooperation.
- **Sensitivity:** This strategy ignores the specific identity of anonymous opponents, focusing entirely on the aggregate group behavior as the signal for cooperation.
'''

description_ALTRUISTIC_12 = '''
Define the strategy as follows:

**Round 1:**
Cooperate.

**Subsequent Rounds (2 to r):**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $T_{t-1}$ be the total number of players ($n$).

Calculate the "observed cooperation threshold" required to make cooperation beneficial for the group, defined as $k > 1$. Since individual incentive to defect exists when $k/n < 1$ (the standard public goods dilemma), maintain cooperation as long as a significant portion of the group reciprocates.

1.  **If $C_{t-1} \geq \lceil n/k \rceil$:** Cooperate. This sustains the public good where the return on investment for the collective outweighs the private incentive to defect.
2.  **If $C_{t-1} < \lceil n/k \rceil$:** Defect. This signals that the group cooperation level is insufficient to sustain the public good and protects against exploitation by defectors.

**Final Round (r):**
Cooperate if $C_{r-1} \geq \lceil n/k \rceil$, otherwise Defect. (Note: While standard game theory suggests defecting in the final round, this strategy maintains altruistic commitment provided the group has demonstrated a consistent cooperative trend leading up to the final move).

**Edge Cases:**
*   **If $n=2$:** The strategy simplifies to Tit-for-Tat: Cooperate in round 1; copy the opponent's action from round $t-1$.
*   **If $C_{t-1} = 0$:** Defect immediately in round $t$ to avoid being the sole provider of the public good.
*   **Restart/Recovery:** If the group returns to $C_{t} \geq \lceil n/k \rceil$ after a period of defection, resume Cooperation in $t+1$.
'''

description_ALTRUISTIC_13 = '''
Strategy: **Conditional Reciprocator with Generous Thresholds**

**Objective:** Maximize total group welfare while preventing exploitation by defectors.

**Decision Rules:**

1.  **First Round:** Cooperate (C). Initiate a signal of cooperation to encourage mutual benefit.

2.  **Subsequent Rounds:**
    Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   If $C_{t-1} \ge \lceil n/k \rceil$, play Cooperate (C). This threshold represents the "break-even" point where group cooperation yields a return greater than or equal to defecting alone. 
    *   If $C_{t-1} < \lceil n/k \rceil$, play Defect (D) for the current round.

3.  **Punishment/Reset Mechanism:**
    *   After defecting (when $C_{t-1} < \lceil n/k \rceil$), if the total number of cooperators in the current round ($C_{t}$) rises back to the threshold level $\lceil n/k \rceil$ or higher, immediately return to Cooperate (C) in the following round. This serves as a "forgiving" mechanism to re-establish cooperation if opponents shift behavior.

**Edge Cases:**

*   **Last Round:** If $r$ is known, play Defect (D) regardless of history. Since there is no future interaction to influence, the incentive to maximize individual payoff is the only remaining rational choice, assuming no additional altruistic utility is derived from the final state. (If $r$ is unknown or the end is not fixed, ignore this rule).
*   **Initialization/Recovery:** If the group enters a cycle of low cooperation, play Defect (D) to minimize personal loss until the previous round's cooperation count meets the threshold. 
*   **Tie-breaking:** If the calculation for the threshold $\lceil n/k \rceil$ results in an integer, treat it as the strict minimum for cooperation. If the number of cooperators exactly equals the threshold, it is considered a success; cooperate.
'''

description_ALTRUISTIC_14 = '''
**Strategy: Conditional Reciprocal Altruism with a "Grim" Safety Trigger**

This strategy is defined by three phases: Initiation, Maintenance, and Termination. The objective is to maximize aggregate cooperation while protecting against persistent exploitation.

**Phase 1: Initiation (Round 1)**
Always Cooperate. This signals an initial commitment to a collective optimum, regardless of the parameters $n$ and $k$.

**Phase 2: Maintenance (Rounds 2 through $r-1$)**
Decision logic relies on the observed cooperation count from the previous round $t-1$. Let $S_{t-1}$ be the total number of cooperators observed in the previous round.

1.  **If $S_{t-1} \ge \theta$:** Cooperate. The threshold $\theta$ is defined as $\lceil n/k \rceil$. This value represents the minimum number of cooperators required for cooperation to yield a personal payoff equal to or greater than the payoff of defection (i.e., the "break-even" point).
2.  **If $S_{t-1} < \theta$:** Defect. This penalizes the group for failing to maintain a socially beneficial level of cooperation, preventing exploitation while signaling a demand for higher participation.
3.  **Recovery:** If the group fails to meet the threshold, remain in a "Defect" state for exactly one round to discourage free-riding, then test the group's intent by returning to "Cooperate" in the subsequent round.

**Phase 3: Termination (Round $r$)**
In the final round, the incentive to maintain future cooperation vanishes. To maximize total altruistic outcome:
1.  **If the average cooperation count across all previous rounds is $\ge \theta$:** Cooperate.
2.  **Otherwise:** Defect.

**Pseudocode:**

```python
# Variables:
# n: total players
# k: multiplication factor
# r: total rounds
# t: current round index
# S_{t-1}: number of cooperators observed in round t-1
# history: list of cooperation counts observed so far

threshold = ceil(n / k)

if t == 1:
    return Cooperate

if t < r:
    if S_{t-1} >= threshold:
        return Cooperate
    else:
        # Check if we are currently punishing
        # If we defected in t-1 because of low cooperation, 
        # return to Cooperate to test group willingness
        if last_action == Defect: 
            return Cooperate
        else:
            return Defect

if t == r:
    avg_coop = sum(history) / (r - 1)
    if avg_coop >= threshold:
        return Cooperate
    else:
        return Defect
```

**Edge Case Handling:**
*   **Small $k$:** If $k$ is close to 1, the threshold $\theta$ approaches $n$. If $\theta > n$, it is mathematically impossible for cooperation to be individually rational; in this scenario, the strategy defaults to Defect for all rounds, as the game structure prevents meaningful altruistic gains.
*   **Silent Groups:** If $S_{t-1} = 0$, immediately trigger Defect.
'''

description_ALTRUISTIC_15 = '''
Adopt a Tit-for-Tat-based strategy with a forgiveness mechanism to encourage mutual cooperation while preventing exploitation.

**Initialization:**
Set `reputation_threshold` = (n / k). This represents the minimum number of cooperators required to make universal cooperation marginally profitable or neutral compared to defection.

**Round 1:**
Play `C` (Cooperate). This signals willingness to engage in a cooperative equilibrium.

**Rounds 2 to r-1:**
Let `C_prev` be the number of cooperators observed in the previous round.
Let `my_action_prev` be my own action in the previous round (1 for C, 0 for D).
Let `observed_others_C` be `C_prev` - `my_action_prev`.

*   **Rule:** If `observed_others_C` ≥ `reputation_threshold` - 1, play `C`.
*   **Rule (Forgiveness):** If the previous round resulted in defection but the number of cooperators was high, or if cooperation has been inconsistent, play `C` with probability `p = 0.1` to attempt to restart cooperation.
*   **Default:** Otherwise, play `D` (Defect).

**Final Round (r):**
Play `D`. Since there are no future interactions, the incentive to build reputation is removed. Playing `D` in the final round minimizes exploitation risk without impacting future cooperative opportunities.

**Pseudocode Logic:**

```
// Variables:
// n: total players
// k: multiplier
// t: current round
// C_prev: cooperators in t-1
// my_last_action: my action in t-1 (1 if C, 0 if D)

if t == r:
    return D

if t == 1:
    return C

observed_others_C = C_prev - my_last_action

if observed_others_C >= (n / k) - 1:
    return C
else if random(0, 1) < 0.1: // Forgiveness mechanism
    return C
else:
    return D
```
'''

description_ALTRUISTIC_16 = '''
**Strategy Definition: Conditional Reciprocal Altruism**

**1. First Round Action**
Play Cooperate (C) unconditionally. This establishes a cooperative baseline to signal potential for collective optimization.

**2. Standard Round Decision Rule (Rounds 2 to r-1)**
Calculate the "Cooperation Threshold" $T = n/k$.
Let $C_{prev}$ be the number of players who cooperated in the previous round.
- If $C_{prev} \geq T$: Play C.
- If $C_{prev} < T$: Play D with probability $P(D) = (T - C_{prev}) / T$, otherwise play C. 

This rule targets the break-even point where the marginal benefit of cooperation ($k/n$) equals the cost of contribution (1). By scaling the probability of defection based on how far below the threshold the group falls, the strategy punishes non-cooperation while remaining flexible enough to recover if the group returns to the threshold.

**3. Last Round Decision Rule (Round r)**
Play D unconditionally. Since the game terminates, there is no future benefit to maintaining cooperative reputation or incentivizing others, and altruism is maximized by preserving personal resources when no further public goods can be generated.

**4. Edge Cases**
- **Symmetry Break:** If $C_{prev} = 0$, play D unconditionally to prevent exploitation.
- **Perfect Cooperation:** If $C_{prev} = n$ in any round, maintain C for all subsequent rounds, regardless of the threshold, assuming a fully cooperative equilibrium has been established.
- **End-Game Sensitivity:** For $r < 3$, ignore the threshold calculation in the final round; play C in all rounds prior to the final round, and play D in the final round.
'''

description_ALTRUISTIC_17 = '''
**Strategy: Conditional Reciprocal Altruism**

The strategy operates on a principle of optimistic cooperation constrained by observed group reciprocity. Let $C_t$ be the total number of cooperators observed in round $t$, and $n$ be the total number of players.

**1. Initialization (Round 1):**
Always cooperate ($C$). This signals a willingness to engage in the cooperative equilibrium.

**2. Decision Rule (Rounds $t = 2$ to $r-1$):**
Calculate the cooperation rate of the group from the previous round $t-1$. Let $c_{t-1}^{other}$ be the number of cooperators observed among the other $n-1$ players. 
*   If you cooperated in $t-1$: Cooperate if $c_{t-1}^{other} \geq \lceil \frac{n}{k} \rceil - 1$.
*   If you defected in $t-1$: Cooperate if and only if $c_{t-1}^{other} \geq \lceil \frac{n}{k} \rceil$.

This threshold $\lceil \frac{n}{k} \rceil$ represents the "break-even" point where collective cooperation yields a payoff at least equal to pure defection. The strategy maintains cooperation as long as the group demonstrates a baseline commitment to the public good, while requiring a slightly higher burden of proof to return to cooperation after a defection episode.

**3. Terminal Phase (Round $r$):**
In the final round, the incentive to build future reputation is removed. To maximize the aggregate social welfare without being exploited in the final step, cooperate if and only if the group cooperation rate in round $r-1$ was above the break-even threshold $\lceil \frac{n}{k} \rceil$.

**Pseudocode:**

```python
# Constants: n, k, r are provided parameters
# Let 'last_round_cooperators' be the number of cooperators observed in the previous round
# Let 'my_last_action' be my action in the previous round (1 for C, 0 for D)

break_even = ceil(n / k)

if current_round == 1:
    return Cooperate

if current_round == r:
    # Final round: cooperate only if the group was productive in the previous round
    if last_round_cooperators >= break_even:
        return Cooperate
    else:
        return Defect

# Standard rounds
if my_last_action == Cooperate:
    # Maintain cooperation if the group is contributing at a sustainable level
    # Subtract 1 from break_even to account for my own previous contribution
    if last_round_cooperators >= (break_even - 1):
        return Cooperate
    else:
        return Defect
else:
    # If I defected, punish the group slightly by requiring a strictly higher threshold 
    # to resume cooperation
    if last_round_cooperators >= break_even:
        return Cooperate
    else:
        return Defect
```
'''

description_ALTRUISTIC_18 = '''
**Strategy: Conditional Reciprocal Altruism**

**1. Initialization (Round 1):**
Cooperate (C) in the first round to signal intent for mutual cooperation.

**2. Decision Rules (Rounds 2 to r-1):**
Observe the total number of cooperators from the previous round (S_prev). Let S_target be the number of cooperators required to make universal cooperation marginally more profitable than individual defection. If the opponents' previous behavior indicates a sustainable cooperative equilibrium, maintain cooperation.

Define the cooperation threshold: T = n / k.

Calculate:
- If S_prev > T: Cooperate (C).
- If S_prev == T: Cooperate (C) with probability 0.5; otherwise, Defect (D).
- If S_prev < T: Defect (D) for one round to minimize losses from exploitation, then evaluate the subsequent round to attempt re-entry.

**3. Edge Case Handling:**
- **Re-entry:** If the strategy defected in the previous round due to S_prev < T, observe the new S_current. If S_current returns to a level where cooperation is sustainable (S_current ≥ T), return to Cooperation (C).
- **The Final Round (Round r):** Defect (D). Since there is no future interaction to incentivize, and the objective is to maximize payoff within the finite horizon, the dominant strategy is to capture the private endowment while benefiting from any remaining altruists.

**4. Altruistic Adjustment:**
If the total game history shows a persistent downward trend in cooperation despite consistent attempts to sustain it, trigger "Conditional Altruism": persist in Cooperation (C) for one additional round beyond the standard threshold of S_prev < T to attempt to stabilize the group dynamic, but only if the cumulative payoff variance remains positive. If cooperation fails to recover after this intervention, default to Defect (D) for the remainder of the game.
'''

description_ALTRUISTIC_19 = '''
Use a modified Tit-for-Tat strategy defined by an aspiration-based threshold, aiming for mutual cooperation while penalizing sustained defection. Let $C_t$ be the total number of cooperators observed in round $t$, and let $N$ be the total number of players.

**Decision Rules:**

1.  **First Round ($t=1$):** Always play $C$. This establishes a cooperative baseline.

2.  **Subsequent Rounds ($t > 1$):** Cooperate if the aggregate cooperation level from the previous round meets or exceeds a target threshold $T$; otherwise, defect.

    *   Calculate $T = \lceil \alpha \times N \rceil$, where $\alpha$ is the cooperation target ratio (initially set to $0.5 + \frac{1}{2N}$).
    *   If $C_{t-1} \ge T$, play $C$.
    *   If $C_{t-1} < T$, play $D$.

3.  **Adaptive Threshold Adjustment:**
    *   If the strategy defected in the previous round ($C_{t-1} < T$) and observing the outcome $C_t$ shows an increase in cooperation from other players ($C_t > C_{t-1}$), restore cooperation ($C$) in the next round, $t+1$, regardless of the threshold. This serves as a "forgiveness" mechanism to restart mutual cooperation.
    *   If the strategy cooperated ($C$) but the public good contribution $C_{t-1}$ resulted in a payoff lower than the payoff of a defector in that same round, increase the threshold $\alpha$ by $0.05$ (up to a maximum of $0.9$) to become more selective.
    *   If the strategy cooperated and the public good contribution $C_{t-1}$ resulted in a payoff equal to or greater than the average payoff of a defector, decrease the threshold $\alpha$ by $0.02$ (down to a minimum of $0.1$) to encourage broader participation.

**Edge Case Handling:**

*   **Final Round ($t = r$):** If the average observed cooperation over the previous $r-1$ rounds is $\ge \frac{N}{2}$, play $C$. Otherwise, play $D$.
*   **Low Participation:** If $C_{t-1} = 0$, play $D$ for the remainder of the game, as the environment is non-cooperative.
*   **High Participation:** If $C_{t-1} = N$, maintain $C$ regardless of payoff calculations, as this represents a stable altruistic equilibrium.
'''

description_ALTRUISTIC_20 = '''
**Strategy: Conditional Reciprocal Altruism with Threshold Monitoring**

The core objective is to maximize collective welfare while minimizing exploitation. This strategy treats the public good as a fragile system that requires maintenance but survives only if supported by a critical mass of participants.

**1. Definitions**
*   Let $S_t$ be the total number of contributors in the previous round (including self).
*   Let $C_t = 1$ if self contributed in round $t$, and $C_t = 0$ otherwise.
*   Let $O_t$ be the number of opponents who contributed in round $t$ (calculated as $S_t - C_t$).
*   The cooperation threshold $T$ is defined as $\lceil n/k \rceil$. This is the minimum number of contributors required for the public good to be individually rational (where the benefit of contributing outweighs the private benefit of defecting).

**2. Decision Rules**

*   **Round 1:** Play **Cooperate (C)**. This signals a commitment to group welfare and establishes a baseline for cooperation.

*   **Rounds $t=2$ to $r-1$:**
    *   If $O_{t-1} \geq (T - 1)$, play **Cooperate (C)**.
    *   If $O_{t-1} < (T - 1)$, play **Defect (D)**.
    *   *Correction Mechanism:* If the strategy played **Defect (D)** in the previous round and the number of other cooperators in the group $O_{t-1}$ returns to or exceeds $T-1$, reset to **Cooperate (C)**. This allows the strategy to forgive and re-enter cooperative cycles if the group dynamics improve.

*   **Final Round ($t=r$):**
    *   If $O_{t-1} \geq (T - 1)$, play **Cooperate (C)**.
    *   If $O_{t-1} < (T - 1)$, play **Defect (D)**.

**3. Rationale for Altruism**
This strategy is inherently altruistic because it creates a "cooperation floor." By using the threshold $T$, it attempts to sustain the public good when it is viable for the group, rather than immediately defecting to maximize personal gain at the expense of others. It only reverts to defection when the collective contribution level falls below the point where cooperation is sustainable, serving as a defensive measure to prevent the exploitation of the altruistic agent while preserving the capacity to contribute in the future if others resume cooperation.
'''

description_ALTRUISTIC_21 = '''
**Round 1:** Cooperate (C).

**Round 2 to Round (r-1):**
Calculate the cooperation threshold $T$ using the game parameters, where $T = \lceil n/k \rceil$. Observe the total number of cooperators ($C_{t-1}$) from the previous round.
- If $C_{t-1} \ge T$, continue to Cooperate (C).
- If $C_{t-1} < T$, switch to Defect (D) for the subsequent round.
- If previously defecting, check if $C_{t-1} \ge T$. If yes, return to Cooperate (C). If no, continue to Defect (D).

**Final Round (r):**
To maximize social welfare regardless of past defection or the incentives of the endgame, Defect (D) if the average cooperation rate across all previous rounds is below the threshold $T/n$. Otherwise, Cooperate (C).

**Pseudocode logic for rounds $t \in [2, r-1]$:**
```python
threshold = ceil(n / k)
if t == 1:
    return Cooperate
elif t < r:
    if total_cooperators_previous_round >= threshold:
        return Cooperate
    else:
        return Defect
else: # Round r
    avg_cooperation = sum(cooperators_history) / ((r-1) * n)
    if avg_cooperation >= (threshold / n):
        return Cooperate
    else:
        return Defect
```
'''

description_ALTRUISTIC_22 = '''
**Strategy: Conditional Reciprocal Altruism**

This strategy operates on the principle of conditional cooperation, maintaining a baseline of trust while defending against exploitation.

**Decision Logic**

For any round `t` in the set `{1, ..., r}`:

1.  **Initialization (Round 1):**
    Play `C` (Cooperate). Starting with cooperation signals an openness to collective benefit.

2.  **Adaptive Response (Rounds 2 to r-1):**
    Calculate `m`, the number of cooperators observed in round `t-1`.
    *   If `m >= (n * 0.5)`: Play `C`.
    *   If `m < (n * 0.5)`: Play `D` (Defect).

    This threshold represents a "sufficient contribution" level. By requiring at least half the group to cooperate, the strategy supports collective efforts that generate a net positive benefit greater than or equal to the cost of cooperation, while punishing groups that lean heavily toward defection.

3.  **Terminal Phase (Round r):**
    Regardless of history, play `D` (Defect). Because there are no future rounds to influence via reputation, the incentive to provide a public good vanishes. This maximizes the terminal payoff without risking exploitation from players who might defect early in the final round to capture a last-minute gain.

**Exception: Recovery Mechanism**

If the strategy is in a state of Defection (due to a previous round `t-1` where `m < (n * 0.5)`), it retains the potential to forgive and return to cooperation.

In any round `t` where the strategy played `D`:
*   Observe the total contributions `m` from round `t`.
*   If `m >= (n * 0.5)`: Play `C` in round `t+1`.

This allows the strategy to re-engage with the group if the majority demonstrates a return to cooperative behavior, ensuring that the altruistic cycle is not permanently broken by a single round of low participation.
'''

description_ALTRUISTIC_23 = '''
**Strategy Name: Conditional Altruistic Reciprocator (CAR)**

The strategy operates on the principle of conditional cooperation, maintaining a baseline of trust while guarding against exploitation. It interprets "altruistic" as maximizing group outcome without being systematically victimized by defectors.

### Pseudocode Definition

```python
# Constants
# tolerance_threshold = 0.2 (20% defection buffer)
# leniency_factor = 0.5 (forgiveness threshold)

def decide_action(round, history, n, k):
    # Round 1: Open with cooperation
    if round == 1:
        return Cooperate

    # Calculate previous round metrics
    prev_round_index = round - 1
    total_cooperators_prev = history[prev_round_index].total_c
    
    # We cooperated last time: check if it was reciprocated
    if history[prev_round_index].my_action == Cooperate:
        # Define 'defecting threshold' based on total cooperation
        # We define a successful group as one where at least (n/k) 
        # cooperate (the break-even point for the group).
        # We allow a small error margin for noise/mistakes.
        if total_cooperators_prev >= (n/k) * (1 - tolerance_threshold):
            return Cooperate
        else:
            return Defect

    # We defected last time: check for redemption opportunity
    else:
        # If the group has returned to high cooperation levels, forgive
        if total_cooperators_prev >= (n/k) * (1 + leniency_factor):
            return Cooperate
        else:
            return Defect

# Edge Case: The Final Round
def final_round_logic(history, n, k):
    # Regardless of previous strategy, if the group has maintained 
    # cooperation for > 50% of the game, cooperate one last time
    # to maximize total social utility.
    if count_rounds_where(history, cooperators > n/k) > (0.5 * r):
        return Cooperate
    else:
        return Defect
```

### Strategic Rules

1.  **Initiation (Round 1):** Always start by choosing **Cooperate**. This signals a willingness to engage in the public good and invites others to coordinate.
2.  **Steady State (Rounds 2 to r-1):**
    *   **Maintain Cooperation:** If the previous round’s total contributions resulted in a group payoff that justifies the social investment (specifically, where the total number of cooperators was sufficient to make the group utility positive relative to the k/n factor), continue to **Cooperate**.
    *   **Retaliation:** If the previous round saw a collapse in cooperation (falling below the break-even threshold necessary for the public good to be profitable), switch to **Defect**. This punishes free-riding.
    *   **Forgiveness:** If the strategy is currently defecting, it will revert to **Cooperate** only if the group demonstrates a strong return to high-level contribution (exceeding the baseline expectation), proving that the previous defection was an anomaly and not a strategic shift by the group.
3.  **Terminal Phase (Round r):** The strategy assesses the overall history of the game. If the majority of rounds (over 50%) were characterized by sustainable levels of cooperation, the strategy will **Cooperate** in the final round. This prioritizes the global maximum payoff over individual gain, acknowledging that the incentive to defect in the final round is a known non-cooperative Nash equilibrium that harms the group. If the group has historically failed to cooperate, the strategy defaults to **Defect** to minimize personal loss.
'''

description_ALTRUISTIC_24 = '''
Define `target_cooperation_level` as 1 (full cooperation).

Initialize `round_count` = 1.
Initialize `cooperation_history` as an empty list.

For each round `t`:
1.  **First Round (t=1):**
    Play **Cooperate**.

2.  **Subsequent Rounds (t > 1):**
    Let `N_c` be the number of cooperators in round `t-1`.
    Calculate the `average_contribution` = `(N_c - c_i) / (n - 1)`, where `c_i` was your action in the previous round.
    
    If `average_contribution` ≥ threshold `T`, where `T` = 0.5:
        Play **Cooperate**.
    Else if `average_contribution` < threshold `T`:
        Play **Defect**.

3.  **Last Round (t=r):**
    Regardless of history, if `r` is known, play **Defect** (as there is no future interaction to incentivize, effectively ending the altruistic cycle to prevent exploitation, unless `n` is small and the expected loss from defecting against cooperators is outweighed by the gain of unilateral defection). However, to remain strictly altruistic, apply the same conditional rule as `t > 1`.

**Exception (Tit-for-Tat Adaptation):**
If `n` is small (e.g., n=2) and the strategy identifies a stable reciprocal partner, maintain **Cooperate** regardless of the last round if the partner has cooperated in > 80% of previous rounds.

**Pseudocode:**
```python
def get_action(round, n, history):
    if round == 1:
        return Cooperate
    
    # Calculate partner cooperation rate (excluding self)
    # history[-1] contains total cooperators in previous round
    # If self cooperated, cooperators excluding self = history[-1] - 1
    # If self defected, cooperators excluding self = history[-1]
    last_round_total_c = history[-1]
    
    if last_action_was_cooperate:
        others_c = last_round_total_c - 1
    else:
        others_c = last_round_total_c
        
    avg_cooperation_rate = others_c / (n - 1)
    
    if avg_cooperation_rate >= 0.5:
        return Cooperate
    else:
        return Defect
```
'''

description_ALTRUISTIC_25 = '''
**Round 1:** Play **Cooperate (C)**.

**Round t (where 1 < t < r):** 
Maintain a "Trust Score" (S), initialized at 1.0. Let $C_{t-1}$ be the number of cooperators observed in the previous round, and $n$ be the number of players.

Calculate the Cooperation Rate of the group in the previous round: $\rho_{t-1} = C_{t-1} / (n-1)$ (excluding your own contribution).

Update the Trust Score: $S_t = S_{t-1} + (\rho_{t-1} - S_{t-1}) \times \alpha$, where $\alpha$ is a sensitivity parameter (e.g., 0.1).

Decision Rule:
If $S_t > \tau$ (where $\tau$ is a cooperation threshold, e.g., 0.5):
    Play **Cooperate (C)**.
Else:
    Play **Defect (D)**.

**Last Round (t = r):**
If the average Cooperation Rate across all rounds $1$ to $r-1$ is $\geq 0.5$, play **Cooperate (C)**. Otherwise, play **Defect (D)** to avoid exploitation in the final opportunity.

**Edge Case - Punishment for Free-Riding:**
If $\rho_{t-1} = 0$ (full defection by opponents), immediately reset $S_t$ to 0 and play **Defect (D)** for one round as a signaling mechanism, regardless of the threshold $\tau$, before resuming the Trust Score calculation in the subsequent round.

**Pseudocode:**

```python
# Constants
alpha = 0.1  # Trust adaptation rate
tau = 0.5    # Cooperation threshold

# State Variables
trust_score = 1.0
history = []

def action(t, r, n, cooperators_previous_round):
    # Round 1
    if t == 1:
        return 'C'
    
    # Last Round
    if t == r:
        avg_coop = sum(history) / (t - 1)
        return 'C' if avg_coop >= 0.5 else 'D'

    # Intermediary Rounds
    # Calculate others' cooperation rate
    my_last_action = history[-1]
    others_coop_count = cooperators_previous_round - (1 if my_last_action == 'C' else 0)
    rho = others_coop_count / (n - 1)
    
    # Update Trust
    trust_score += (rho - trust_score) * alpha
    
    # Signaling mechanism: If full defection, signal displeasure
    if others_coop_count == 0:
        trust_score = 0
        return 'D'
    
    return 'C' if trust_score > tau else 'D'
```
'''

description_ALTRUISTIC_26 = '''
**Strategy: Conditional Tit-for-Tat with Cooperative Threshold (CTFT)**

The strategy is defined by the following rules for each round $t$ (where $t = 1$ to $r$):

**Round 1:**
Cooperate (C). This establishes a baseline for prosocial behavior, testing the environment for potential cooperators.

**Subsequent Rounds ($t > 1$):**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $T$ be the threshold of observed cooperation required to maintain collaboration, calculated as:
$T = \lceil n \cdot \frac{1}{k} \rceil$

*   If $C_{t-1} \ge T$: Cooperate (C).
*   If $C_{t-1} < T$: Defect (D).

**Final Round ($t = r$):**
Defect (D). Regardless of previous history, defect in the final round to prevent exploitation by non-altruistic agents who may defect in the final stage to maximize their short-term payoff.

**Pseudocode:**

```python
def decide_action(round, n, k, history):
    # Base threshold for maintaining cooperation
    # T represents the minimum number of cooperators needed to make 
    # C a non-negative-sum contribution relative to the temptation to defect.
    threshold = ceil(n / k)
    
    # Final round defect
    if round == r:
        return D
    
    # First round cooperate
    if round == 1:
        return C
    
    # Observe previous round performance
    prev_cooperators = history[round - 1]
    
    # Conditional reciprocity
    if prev_cooperators >= threshold:
        return C
    else:
        return D
```

**Adaptive Logic:**
This strategy is altruistic yet robust. It initiates cooperation to build collective value but uses the threshold $T$ to ensure that cooperation is only sustained when it is group-beneficial. Since $k < n$, the payoff for playing C is lower than playing D if fewer than $n/k$ players cooperate. By requiring $C_{t-1} \ge \lceil n/k \rceil$, the strategy punishes defection while providing a clear "on-ramp" for other players to restore cooperation in subsequent rounds if they choose to switch back to C.
'''

description_ALTRUISTIC_27 = '''
Adopt a conditional cooperation strategy aimed at fostering mutual contribution while maintaining a baseline defense against exploitation. 

### Strategy Pseudocode

```python
# Constants
# epsilon: A small tolerance threshold for deviations, e.g., 0.1
# threshold: A cooperation requirement, typically 1/k

history = [] # Stores total cooperators from previous rounds

def determine_action(round_number, n, k):
    # Round 1: Initiate cooperation to signal pro-social intent.
    if round_number == 1:
        return 'C'

    # Last Round: Defect to avoid unilateral loss, as no future consequences exist.
    if round_number == total_rounds:
        return 'D'

    # Adaptive Cooperation: Observe previous round's total cooperators (S)
    previous_S = history[-1]
    
    # Calculate the critical mass of cooperators needed to make cooperation 
    # individually rational (or at least neutral): (k/n) * S >= 1 => S >= n/k
    critical_mass = n / k
    
    # If the group has sustained cooperation, continue to cooperate.
    # We include a buffer (epsilon) to allow for minor errors or intentional noise.
    if previous_S >= (critical_mass - epsilon):
        return 'C'
    
    # If the group has fallen below the critical threshold, revert to defection
    # for a single round to minimize losses and signal the need for higher contribution.
    else:
        return 'D'
```

### Strategy Description

1. **Initial Cooperation**: Always play 'C' in the first round. This establishes a baseline of trust and invites the group to coordinate toward the Pareto-optimal outcome where everyone contributes.

2. **Conditional Continuation**: From round 2 onward, evaluate the effectiveness of the group's cooperation in the previous round. If the number of cooperators was sufficient to make the public good return at least equal to the cost of contributing (i.e., total cooperators $\geq n/k$), continue to play 'C'.

3. **Defection as Correction**: If the group’s cooperation falls significantly below the threshold required to make contribution individually worthwhile, switch to 'D'. This serves as a "tit-for-tat" correction, preventing the exploitation of your own altruism while incentivizing other agents to increase their contribution levels to restore the cooperative equilibrium.

4. **Last-Round Defection**: In the final round ($r$), play 'D'. Because the shadow of the future is removed, there is no strategic benefit to signaling or maintaining reputation; defecting captures the final individual gain regardless of the group's past behavior.

5. **Resilience**: The strategy is inherently adaptive. If the group successfully returns to the required cooperation threshold after a period of defection, the strategy will immediately resume cooperation, allowing the system to recover from temporary breakdowns or noise.
'''

description_ALTRUISTIC_28 = '''
The strategy, designated "Conditional Reciprocity with Forgiveness," operates on the principle of establishing mutual cooperation through a tit-for-tat dynamic while maintaining altruism in the face of temporary deviations.

**Variables:**
- $C_{t}$: Number of other cooperators in round $t$.
- $T_{t}$: Total number of players cooperating in round $t$ (including self).
- $Target$: A threshold ratio of $C_{t}/(n-1)$ representing the cooperative state of the group.

**Strategy Logic:**

1. **Round 1 (Initialization):**
   Always cooperate ($c_1 = 1$). This signals a willingness to engage in the public good and invites others to reciprocate.

2. **Rounds 2 to $r-1$ (Adaptive Phase):**
   - **Cooperation Threshold:** Cooperate if the group cooperation rate in the previous round ($C_{t-1} / (n-1)$) meets or exceeds $k/n$. This threshold ensures that if the average contribution of others is high enough to generate a net gain for the group (or satisfies the condition where cooperation is socially efficient), you reciprocate.
   - **Forgiveness:** If the group cooperation rate falls below the threshold in round $t-1$, defect ($c_t = 0$) only once to penalize non-cooperation, then immediately return to cooperation in round $t+1$ regardless of the outcome of the penalty round. This prevents the "death spiral" of defect-defect feedback loops and provides an opportunity for the group to reset.
   - **Exception:** If $C_{t-1} = n-1$ (everyone else cooperated), you must cooperate ($c_t = 1$).

3. **Round $r$ (Final Round):**
   Cooperate if and only if the group cooperation rate in the previous round ($C_{r-1} / (n-1)$) was $\ge k/n$. This maintains the incentive structure until the very end, preventing defection on the final move unless previous behavior warrants it.

**Pseudocode:**

```python
def decide_action(round_number, n, k, history):
    if round_number == 1:
        return 'C'
    
    # Calculate previous round cooperation rate
    prev_cooperators = history[round_number - 1].opponents_cooperated
    cooperation_rate = prev_cooperators / (n - 1)
    
    # Check if this is the final round
    if round_number == r:
        if cooperation_rate >= (k / n):
            return 'C'
        else:
            return 'D'

    # Standard adaptive logic
    # If the group was highly cooperative last time, sustain it
    if cooperation_rate >= (k / n):
        return 'C'
    
    # If the group was uncooperative, check if I just punished them
    # If I punished last round, forgive and cooperate now
    if history[round_number - 1].my_action == 'D':
        return 'C'
    
    # Otherwise, punish the defection
    return 'D'
```
'''

description_ALTRUISTIC_29 = '''
In Round 1, cooperate unconditionally.

In all subsequent rounds (t > 1), cooperate if the average cooperation level of the opponents in the previous round (t-1) met or exceeded the threshold defined by the "altruism ratio" $A = k/n$. If the average cooperation level in the previous round fell below this threshold, play defect.

**Formal Decision Logic:**

Let $C_{total, t-1}$ be the total number of cooperators in round $t-1$.
Let $C_{opponents, t-1} = C_{total, t-1} - c_{self, t-1}$.
Let $N_{opponents} = n - 1$.
The observed opponent cooperation fraction is $F_{t-1} = C_{opponents, t-1} / N_{opponents}$.

For $t = 1$:
$c_t = 1$

For $1 < t \leq r$:
If $F_{t-1} \geq (k-1)/(n-1)$:
    $c_t = 1$
Else:
    $c_t = 0$

**Edge Case Handling:**

1. **Last Round (t = r):** Follow the standard decision logic above, using the results of round $r-1$. Do not defect automatically in the final round, as this breaks the cycle of reciprocated altruism required for total payoff maximization.

2. **Recovery:** If the strategy defects in round $t$, it must "forgive" and attempt to re-establish cooperation if opponents cooperate at a high level. If, while in a defection state, the observed opponent cooperation fraction $F_{t-1}$ reaches or exceeds the threshold $(k-1)/(n-1)$, switch to cooperate in round $t$.

3. **Indifference:** If the calculation yields an exact boundary condition where $F_{t-1} = (k-1)/(n-1)$, choose to cooperate to signal pro-social intent.
'''

description_ALTRUISTIC_30 = '''
**Strategy: Conditional Reciprocity with Altruistic Initiation**

This strategy operates on the principle of "tit-for-tat with a forgiving threshold," designed to foster cooperation while mitigating exploitation. It establishes cooperation early and maintains it as long as the aggregate contribution of others meets a sustainability threshold.

**Decision Logic**

Let $c_{i,t}$ be your action at round $t$, where $c=1$ is Cooperate and $c=0$ is Defect. Let $S_t$ be the total number of cooperators observed in round $t$, and $S_{t-1}$ be the number of cooperators observed in the previous round.

1.  **Round 1 (Initiation):**
    Always Cooperate ($c_{i,1} = 1$). This signals a willingness to engage in a cooperative equilibrium.

2.  **Subsequent Rounds ($t > 1$):**
    Calculate the *Contribution Ratio* ($R_{t-1}$) from the previous round as $R_{t-1} = \frac{S_{t-1} - 1}{n-1}$. This represents the proportion of opponents who cooperated.

    *   **If $R_{t-1} \ge \frac{1}{k}$:**
        Cooperate ($c_{i,t} = 1$). This threshold is the "breakeven point" where altruism is individually rational. If the group meets this, continue cooperating to maximize collective utility.

    *   **If $R_{t-1} < \frac{1}{k}$:**
        Defect ($c_{i,t} = 0$). This protects against exploitation when the group cooperation level falls below the efficiency threshold.

3.  **The "Forgiveness" Trigger:**
    If you have defected due to low cooperation, attempt to restart cooperation every $m$ rounds (where $m=3$ is recommended). If $t \pmod m = 0$, cooperate regardless of the previous round's outcome. This allows the group to recover from mutual defection traps.

4.  **Final Round ($t = r$):**
    Regardless of history, if $R_{r-1} \ge \frac{1}{k}$, Cooperate. If the group has sustained cooperation until the penultimate round, maintain the cooperative stance to maximize the final round's social welfare. If the group has been non-cooperative, Defect to prevent last-minute exploitation.

**Pseudocode**

```python
# Parameters: n (players), k (multiplier), r (rounds)
# Threshold: 1/k is the break-even proportion for individual rationality

def get_action(t, r, n, k, history):
    # Rule 1: First round initiation
    if t == 1:
        return 1 # Cooperate
    
    # Identify previous round outcome
    last_round_cooperators = history[-1]
    # Calculate proportion of others who cooperated
    # If I cooperated, subtract 1 from total to count only opponents
    if history_my_action[-1] == 1:
        opponents_cooperated = last_round_cooperators - 1
    else:
        opponents_cooperated = last_round_cooperators
        
    proportion_opponents = opponents_cooperated / (n - 1)
    
    # Rule 3: Periodic Forgiveness
    if t % 3 == 0:
        return 1
        
    # Rule 2: Conditional Reciprocity
    if proportion_opponents >= (1 / k):
        return 1 # Cooperate
    else:
        return 0 # Defect
```
'''

description_ALTRUISTIC_31 = '''
In the first round, play Cooperate (C).

In all subsequent rounds, determine your move based on the history of cooperation among all players in the previous round, denoted as $S_{t-1}$ (the total number of contributors at time $t-1$):

1.  If $S_{t-1} \geq \frac{n}{k}$, play Cooperate (C). This threshold represents the "break-even" point where universal cooperation among all players (including yourself) yields a higher individual payoff than universal defection, or where your contribution creates a positive aggregate return for the group.
2.  If $S_{t-1} < \frac{n}{k}$, play Defect (D). This signals that the group cooperation level is insufficient to sustain a mutually beneficial outcome, shifting to a protective stance to prevent exploitation while awaiting evidence of increased altruism from others.

For the final round ($r$), regardless of the threshold rule above, evaluate the cumulative performance of the group. If the average number of cooperators across all previous rounds $\bar{S} \geq \frac{n}{k}$, play Cooperate (C) to maximize the final round's public good contribution. Otherwise, play Defect (D).

Pseudocode:

```python
def decide_action(round_number, total_rounds, n, k, history):
    threshold = n / k
    
    # First round initialization
    if round_number == 1:
        return 'C'
        
    # Last round conditional evaluation
    if round_number == total_rounds:
        average_cooperation = sum(history) / len(history)
        if average_cooperation >= threshold:
            return 'C'
        else:
            return 'D'
            
    # Standard adaptive round rule
    previous_round_cooperation = history[-1]
    if previous_round_cooperation >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_ALTRUISTIC_32 = '''
**Strategy: Conditional Reciprocity with Forgiveness**

This strategy attempts to foster high cooperation levels among agents who are also inclined toward cooperation, while minimizing exposure to pure defectors. It balances the "altruistic" goal of maximizing group welfare against the "robust" goal of protecting one's own payoff.

**Decision Rules**

Let $C_{t-1}$ be the number of cooperators observed in the previous round ($t-1$).
Let $T$ be the total number of rounds ($r$).
Let $t$ be the current round index.

**Round 1:**
Play $C$ (Cooperate).

**Rounds $2 \le t < T$:**
Play $C$ if $C_{t-1} \ge \lfloor n \cdot \frac{1}{k} \rfloor$.
Otherwise, play $D$ (Defect).

*Note: The threshold $\lfloor n \cdot \frac{1}{k} \rfloor$ represents the break-even point where the marginal return on cooperation matches the opportunity cost of contribution. If total contributions are below this level, cooperation is net-negative for the group; if above, it is net-positive.*

**Final Round ($t = T$):**
Play $C$ if:
1. $C_{t-1} \ge \lfloor n \cdot \frac{1}{k} \rfloor$, OR
2. The cumulative payoff average from previous rounds is significantly higher than the theoretical defector baseline of $1.0$, indicating successful past cooperation.

Otherwise, play $D$.

**Handling Edge Cases**

*   **Sudden Drop in Cooperation:** If the number of cooperators drops below the threshold, immediately defect in the subsequent round. This signals that cooperation must be sustained to be maintained.
*   **Re-initiation (Forgiveness):** If you defected in the previous round due to low cooperation, but observe a subsequent round where $C_{t-1} \ge \lfloor n \cdot \frac{1}{k} \rfloor$, play $C$ immediately to attempt to restart cooperative cycles.
*   **Perfect Cooperation:** If $C_{t-1} = n$, continue to play $C$ regardless of the threshold calculation, as this is the global optimum.
*   **Parameter Sensitivity:** If $\frac{k}{n} \le \frac{1}{n}$ (i.e., $k \le 1$), the game is purely competitive, and no public good is generated. In this specific scenario, play $D$ for all rounds.
'''

description_BENEVOLENT_5 = '''
**Strategy Description: Benevolent Reciprocal Tit-for-Tat**

The strategy operates on the principle of conditional cooperation, aiming to foster mutual contribution while protecting against exploitation.

**Initialization**
In the first round (t=1), cooperate.

**Decision Rules (Rounds 1 < t < r)**
The decision depends on the contribution of the collective in the previous round (t-1). Let *S* be the total number of cooperators observed in the previous round.
1.  **If *S* ≥ (n * (1/k))**: Maintain cooperation. This threshold represents the break-even point where the public good returns are equal to or greater than the private benefit of defection.
2.  **If *S* < (n * (1/k))**: Defect. This signals a transition to a defensive posture because the aggregate contribution level is insufficient to justify the cost of cooperation.

**Recovery Mechanism**
If the strategy is in a state of defection, it will attempt to re-establish cooperation periodically to test for renewed mutual contribution.
1.  In any round *t* where the strategy defected in *t-1*, observe the total cooperators *S*.
2.  If *S* ≥ (n * (1/k)) in the previous round, or if *t* mod 5 == 0, switch back to cooperate. This ensures the strategy does not get permanently stuck in a mutual defection trap.

**Termination**
In the final round (t=r), defect regardless of previous history. Since there are no subsequent rounds to incentivize future cooperation or punish defection, the final round is treated as a one-shot game where the dominant strategy is to maximize the immediate payoff by keeping the endowment.

**Pseudocode**

```python
# Variables:
# n: total players
# k: multiplication factor
# t: current round
# r: total rounds
# S_prev: number of cooperators observed in previous round
# is_defected: boolean flag for current state

if t == 1:
    return Cooperate
    
if t == r:
    return Defect

threshold = (n / k)

if is_defected:
    if S_prev >= threshold or t % 5 == 0:
        is_defected = False
        return Cooperate
    else:
        return Defect
else:
    if S_prev >= threshold:
        return Cooperate
    else:
        is_defected = True
        return Defect
```
'''

description_BENEVOLENT_6 = '''
### Tit-for-Tat with Conditional Forgiveness and Greed-Check

The strategy relies on a conditional cooperation mechanism based on the observed number of cooperators ($S_{t-1}$) in the previous round.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**.
2.  **Round $t$ (where $1 < t < r$):**
    *   Calculate the average contribution rate of opponents from the previous round: $\bar{S}_{t-1} = (S_{t-1} - c_{t-1}) / (n - 1)$.
    *   If $\bar{S}_{t-1} \geq 0.5$ (the "Benevolence Threshold"): Play **Cooperate (C)**.
    *   If $\bar{S}_{t-1} < 0.5$: Play **Defect (D)**.
3.  **Last Round ($t = r$):**
    *   If $\bar{S}_{r-1} \geq 0.5$: Play **Cooperate (C)**.
    *   If $\bar{S}_{r-1} < 0.5$: Play **Defect (D)**.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, n, previous_cooperators, my_last_action):
    # Round 1
    if round_number == 1:
        return 'C'
    
    # Calculate previous round opponent cooperation rate
    # Subtract my own contribution from total to isolate others
    my_contribution = 1 if my_last_action == 'C' else 0
    opponents_cooperated = previous_cooperators - my_contribution
    opponent_cooperation_rate = opponents_cooperated / (n - 1)
    
    # Tit-for-Tat logic with threshold
    if opponent_cooperation_rate >= 0.5:
        return 'C'
    else:
        return 'D'
```

**Edge Cases & Calibration:**

*   **Sudden Defection:** If the group cooperation rate drops below the 0.5 threshold due to a few defectors, the strategy immediately defects to protect against exploitation. It remains in a state of defection until the group demonstrates a recovery to at least 50% cooperation, at which point it resumes cooperation ("forgiveness").
*   **$n=2$ (Prisoner's Dilemma context):** If $n=2$, the threshold logic functions as standard Tit-for-Tat, where the player matches the previous action of the single opponent.
*   **Last Round:** The strategy does not exhibit "end-game defection" (playing D on the final round regardless of history). It maintains the same conditional logic in the final round to encourage stability and consistent incentives throughout the duration of the game.
'''

description_BENEVOLENT_7 = '''
The strategy is a variant of "Generous Tit-for-Tat" adapted for N-player aggregate observations, designed to incentivize mutual cooperation while remaining resilient to exploitation.

**Initialization:**
Play **Cooperate** in the first round (t=1).

**Decision Rule:**
For each subsequent round t ∈ {2, ..., r}:

1. **Calculate the Threshold:** Define the cooperation threshold T as `n * (1 / k)`. If the number of total cooperators in the previous round (S_{t-1}) meets or exceeds this threshold, the return on cooperation is net positive for the group; otherwise, it is net negative.

2. **Evaluate Opponent Reciprocity:** 
   - If S_{t-1} ≥ T, play **Cooperate**. This rewards recent collective success.
   - If S_{t-1} < T, play **Defect** with probability P = (1 - S_{t-1}/n). This provides a probabilistic "forgiveness" mechanism that punishes mass defection while allowing for the possibility that some opponents were attempting to cooperate but were outnumbered.

3. **Last Round Adjustment:** 
   Regardless of the history, in the final round (t=r), play **Cooperate** if S_{r-1} ≥ T. If S_{r-1} < T, play **Defect**. This acknowledges that the incentive to cooperate to induce future cooperation vanishes in the final round, so the strategy reverts to maximizing immediate payoff based on the established trust level.

**Pseudocode:**
```
IF t == 1:
    RETURN Cooperate

// Define threshold based on payoff structure
Threshold = n / k

// Get total cooperators from previous round
S_prev = Observation(t-1)

IF t < r:
    IF S_prev >= Threshold:
        RETURN Cooperate
    ELSE:
        // Probability of defecting scales with how many players defected
        IF Random(0, 1) < (1 - S_prev/n):
            RETURN Defect
        ELSE:
            RETURN Cooperate

IF t == r:
    // Final round: strict reciprocity
    IF S_prev >= Threshold:
        RETURN Cooperate
    ELSE:
        RETURN Defect
```

**Edge Case Handling:**
- **Incomplete Information:** If the number of cooperators is reported as ambiguous or missing for a round, assume S_{t-1} = 0 and act as if the previous round was a total defection to protect resources.
- **Low-K Scenarios (k ≈ 1):** If the payoff structure is nearly zero-sum (k is very close to 1), the threshold becomes very high (close to n). The strategy naturally defaults to defection, preventing unnecessary resource loss when collective cooperation provides negligible benefit.
'''

description_BENEVOLENT_8 = '''
Play Cooperate (C) in round 1.

For every subsequent round $t$ (where $1 < t \le r$), evaluate the behavior of the group using the observed number of cooperators from the previous round ($C_{t-1}$). Let $c_{t-1}$ be your own action in round $t-1$.

Define the observed cooperation rate among others as $O_{t-1} = (C_{t-1} - c_{t-1}) / (n - 1)$.

Decision Logic:

1.  If $t = r$ (the final round):
    Play Defect (D) if $k < n$ (the dominant strategy for the final round in a finite game), unless the observed cooperation rate $O_{t-1}$ consistently exceeds a threshold of $0.5$ across previous rounds, in which case play Cooperate (C) to reciprocate the established benevolence.

2.  If $1 < t < r$:
    Employ a "Tit-for-Tat with Forgiveness" approach:
    *   If $O_{t-1} \ge \frac{1}{k}$, play Cooperate (C).
    *   If $O_{t-1} < \frac{1}{k}$, play Defect (D) to punish non-cooperation and protect your endowment.
    *   Additionally, if you played D in round $t-1$ but $O_{t-1} \ge \frac{1}{k}$, play Cooperate (C) to signal a willingness to restore cooperation (forgiveness).

3.  Edge cases for observation:
    *   If $n=1$, this does not apply; for $n \ge 2$, if $n-1$ is the denominator, ensure the calculation handles the division correctly.
    *   In the event of an ambiguous observation (e.g., $O_{t-1}$ exactly equals the threshold), prioritize Cooperate (C) to favor collective gain.
'''

description_BENEVOLENT_9 = '''
The strategy follows a conditional cooperation framework designed to incentivize mutual contribution while minimizing exploitation in the final stages.

**State Variables:**
- `cooperation_threshold`: A dynamic variable initialized to 0, representing the minimum number of contributions from other players required to justify cooperation.
- `last_round_cooperators`: The number of cooperators observed in the previous round.
- `t`: The current round number (1 to r).

**Decision Rules:**

1.  **First Round (t=1):**
    Play **Cooperate**. This establishes a baseline for cooperation and signals a willingness to engage in the public good.

2.  **Intermediate Rounds (1 < t < r):**
    *   Calculate the `breakeven_point` required for cooperation to be payoff-neutral. Since the payoff from cooperating is `(k/n) * (total_cooperators)`, and the payoff from defecting is `1 + (k/n) * (total_cooperators - 1)`, cooperation is individually rational only if `k/n * total_cooperators >= 1 + k/n * (total_cooperators - 1)`. Simplifying this reveals that cooperation is beneficial when the total number of contributors (including self) meets or exceeds `n/k`.
    *   Define `my_contribution` as 1 (Cooperate) if `last_round_cooperators + 1 >= n/k`.
    *   Define `my_contribution` as 0 (Defect) if `last_round_cooperators + 1 < n/k`.
    *   To be benevolent and encourage stability, if the `last_round_cooperators` was close to the threshold (within 1 player), continue to cooperate even if the math barely fails, acting as a "generous" contributor to prevent a collapse of cooperation.

3.  **Final Round (t = r):**
    Play **Defect**. Because there are no subsequent rounds to incentivize or punish, there is no strategic benefit to cooperating. Defecting in the final round protects the agent's total payoff against potential exploitation by other agents who may defect, without impacting future cooperation.

**Pseudocode:**

```python
def decide_action(t, r, n, k, last_round_cooperators):
    # Final round defect
    if t == r:
        return 'D'
    
    # First round cooperate
    if t == 1:
        return 'C'
    
    # Calculate threshold for rationality
    threshold = n / k
    
    # Determine if cooperating was rational in the previous round
    # We add 1 to last_round_cooperators to account for our own contribution
    if (last_round_cooperators + 1) >= threshold:
        return 'C'
    
    # Generous buffer: if cooperation was very close (within 1 player)
    # to the threshold, maintain cooperation to encourage group stability
    elif (last_round_cooperators + 2) >= threshold:
        return 'C'
        
    else:
        return 'D'
```
'''

description_BENEVOLENT_10 = '''
**Strategy: Tit-for-Tat Threshold Cooperation**

This strategy is defined by three phases: initialization, conditional cooperation based on a dynamic threshold, and endgame termination.

**Decision Rules:**

1.  **Initialization (Round 1):**
    Always play Cooperate (C). This establishes a willingness to contribute to the public good.

2.  **Conditional Cooperation (Rounds 2 to r-1):**
    For every round $t > 1$, calculate the contribution threshold $T$ required for a mutually beneficial outcome. Cooperation is sustained if the group contribution in the previous round ($S_{t-1}$) meets or exceeds the sustainability threshold.

    Let $S_{t-1}$ be the number of players who contributed in the previous round (including yourself).
    *   If $S_{t-1} \geq \lceil n/k \rceil$, play Cooperate (C). This maintains the momentum of a successful public good project.
    *   If $S_{t-1} < \lceil n/k \rceil$, play Defect (D). This signals that the collective contribution is insufficient to provide a net benefit exceeding private defection, protecting against exploitation.

3.  **Endgame (Round r):**
    If the average group contribution rate over the previous $r-2$ rounds was $\geq 0.5$, play Cooperate (C). Otherwise, play Defect (D). This final move rewards established cooperation while hedging against non-cooperative groups.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, history_of_contributions, n, k):
    # Round 1: Benevolent start
    if round_number == 1:
        return 'C'
    
    # Endgame: Last round
    if round_number == total_rounds:
        avg_contribution = sum(history_of_contributions) / (total_rounds - 1)
        if avg_contribution >= (n / 2):
            return 'C'
        else:
            return 'D'
    
    # Rounds 2 to r-1: Conditional Cooperation
    last_round_contribution = history_of_contributions[-1]
    # Threshold calculation based on payoff break-even
    # Defecting yields 1. Cooperating yields (k/n) * S.
    # We cooperate if (k/n) * S >= 1 => S >= n/k
    threshold = ceil(n / k)
    
    if last_round_contribution >= threshold:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **n/k is non-integer:** The threshold uses $\lceil n/k \rceil$ to ensure the contribution provides at least break-even utility.
*   **Total Defection:** If the group results in 0 contributions, the threshold logic ($0 < \lceil n/k \rceil$) correctly triggers Defect (D) to avoid wasting resources on a non-cooperating group.
*   **High Cooperation:** If the group maintains a high contribution rate, the strategy remains consistently in the Cooperate (C) state, promoting group welfare.
'''

description_BENEVOLENT_11 = '''
This strategy employs a Conditional Tit-for-Tat approach with a forgiveness threshold, aiming to establish mutual cooperation while maintaining robustness against defection.

**Variables and State Tracking:**
- Let $C_{t-1}$ be the number of cooperators observed in the previous round.
- Let $Target$ be the threshold for cooperation, defined as $Target = \lceil n/k \rceil$. If $C_t \ge Target$, the public good provides a net benefit to the group.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)** to initiate cooperative norms and test group alignment.

2.  **Rounds 2 through $r-1$:**
    - If the number of cooperators in the previous round, $C_{t-1}$, is equal to $n$ (total cooperation), play **Cooperate (C)**.
    - If $C_{t-1} \ge Target$, play **Cooperate (C)**.
    - If $C_{t-1} < Target$, play **Defect (D)**. This serves as a corrective measure to avoid exploitation when the group contribution is insufficient to generate a net positive return.

3.  **Last Round ($t = r$):**
    - Regardless of previous history, play **Defect (D)** to prevent being the sole cooperator (the "sucker's payoff") when no future incentives for reciprocity remain.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, prev_cooperators, n, k):
    target = ceil(n / k)
    
    if round_number == 1:
        return 'C'
    
    if round_number == total_rounds:
        return 'D'
        
    if prev_cooperators >= target:
        return 'C'
    else:
        return 'D'
```

**Benevolence Adjustment:**
If the strategy has defected in the previous round ($C_{t-1} < Target$), it will test the group again in the next round by playing **Cooperate (C)** with a probability of $1/t$ (where $t$ is the number of rounds since the last defection) to facilitate potential recovery of cooperation without being perpetually trapped in a cycle of mutual defection.
'''

description_BENEVOLENT_12 = '''
Strategy: Tit-for-Tat with Forgiving Escalation (TFE)

Decision Rules:
1. Round 1: Cooperate (C).
2. Rounds 2 to $r-1$:
   - Let $S_{t-1}$ be the total number of cooperators in the previous round.
   - Calculate the "Cooperation Threshold" ($T$) required for reciprocal altruism: $T = \lceil n/k \rceil$.
   - If $S_{t-1} \ge T$: Cooperate (C).
   - If $S_{t-1} < T$: Defect (D).
   - *Exception for Forgiveness:* If the strategy defected in round $t-1$ and the current aggregate cooperation level $S_{t-1}$ is sufficient to make cooperation profitable for the group (i.e., $S_{t-1} \times k > n$), return to Cooperate (C) with probability 0.5 to probe for restored group cooperation.
3. Round $r$: Defect (D).

Edge Cases:
- First round: Always Cooperate (C) to signal intent for mutual gain.
- Final round: Defect (D) to avoid exploitation, as there are no future consequences to influence.
- Tie-breaking: If $S_{t-1}$ is exactly at the threshold $T$, treat this as sufficient cooperation and Cooperate (C).
- Minimum cooperation: If $k/n \le 1/n$ (i.e., $k=1$), this strategy effectively reverts to Defect (D) for all rounds after the first, as the threshold $T$ becomes unachievable or strictly disadvantageous.
'''

description_BENEVOLENT_13 = '''
**Strategy: Conditional Benevolence with Forgiving Reciprocity**

This strategy operates on the principle of *Tit-for-Tat* scaled for public goods, maintaining cooperation as the default while dynamically adapting to the collective contribution level of the group.

### Decision Rules

Let $C_{t-1}$ be the number of cooperators observed in round $t-1$. The strategy determines action $A_t$ for the current round $t$ as follows:

1.  **First Round ($t=1$):** Always play **Cooperate (C)**. This initiates the benevolent cycle and tests the collective willingness to cooperate.

2.  **Subsequent Rounds ($t > 1$):**
    *   **Cooperate (C)** if:
        *   The average contribution rate of others in the previous round, $R_{t-1} = \frac{C_{t-1} - 1}{n - 1}$ (if $A_{t-1} = C$) or $R_{t-1} = \frac{C_{t-1}}{n - 1}$ (if $A_{t-1} = D$), meets or exceeds the cooperation threshold $\tau = \frac{n}{k}$.
        *   *Alternatively*, cooperate if the total group contribution $C_{t-1}$ is sufficient to make cooperation profitable for the group or at least break even compared to defection.
    *   **Defect (D)** if:
        *   The contribution rate falls significantly below the threshold $\tau$, signaling that the group is sliding into a defection equilibrium. 

3.  **The "Forgiveness" Trigger:**
    *   If you are currently defecting, switch back to **Cooperate (C)** every $m$ rounds (where $m=3$ or $5$ depending on $r$) to probe for recovery of cooperative norms. If the group responds with increased cooperation, return to steady-state cooperation.

### Formalized Decision Logic

Let $C_{prev}$ be the number of cooperators in the previous round.
Let $MyAction_{prev}$ be the action taken in the previous round.
Let $OthersCoop = C_{prev} - (1 \text{ if } MyAction_{prev} == C \text{ else } 0)$.

*   If $t = 1$: Return **C**
*   If $OthersCoop \ge \lceil \frac{n}{k} \rceil - 1$: Return **C** (Continue/Reward cooperation)
*   Else if $t \pmod 5 == 0$: Return **C** (Probe/Forgive)
*   Else: Return **D** (Punish defection/Protect against exploitation)

### Edge Cases

*   **Last Round ($t=r$):** The game structure creates an incentive to defect in the final round to maximize individual payoff. However, to remain strictly benevolent, this strategy plays **C** in the final round if the average contribution rate in the previous $n-1$ rounds suggests that the group sustained a cooperative effort. If the group average was primarily defectors, play **D** to avoid unnecessary loss.
*   **Multiplier Thresholds ($k \approx n$ vs. $k \approx 1$):** The strategy dynamically adjusts the "required" cooperation density based on $k/n$. As $k$ approaches $n$, the threshold for cooperation lowers, allowing for more forgiving interactions. As $k$ approaches 1, the threshold tightens, requiring near-unanimous cooperation to justify continuing the C-strategy.
*   **Constant Defection:** If the group remains non-cooperative for an extended duration, the strategy switches permanently to **D** to prevent exploitation, ceasing all probe attempts.
'''

description_BENEVOLENT_14 = '''
The strategy employs a conditional cooperation model that seeks to maximize aggregate group welfare while protecting against exploitation. It operates on the principle of "Generous Tit-for-Tat" with a focus on stabilizing high-contribution equilibria.

**State Variables:**
- `n`: Total number of players.
- `r`: Total number of rounds.
- `t`: Current round number.
- `k`: Multiplication factor.
- `C_prev`: Total cooperators in the previous round.
- `my_history`: List of my own previous moves.

**Decision Rules:**

1.  **First Round (t=1):**
    Always play Cooperate (C). This initiates cooperation and signals an intent for collective optimization.

2.  **Intermediate Rounds (1 < t < r):**
    Calculate the "Fair Contribution Threshold" (FCT), defined as `floor(n * (1/k)) + 1`. This represents the minimum number of cooperators required for the total group benefit to exceed the individual benefit of defecting.
    
    *   If `C_prev >= FCT`: Play Cooperate (C). Reward the group for maintaining a sustainable level of contribution.
    *   If `C_prev < FCT`:
        *   With probability `p` (where `p` is proportional to `C_prev / n`), play Cooperate (C).
        *   Otherwise, play Defect (D). This "probabilistic forgiveness" encourages a return to cooperation even if the group dipped below the threshold, preventing death spirals while signaling that unconditional support is not infinite.

3.  **Last Round (t=r):**
    Because there is no future incentive to maintain reputation or punish defectors, the standard subgame perfect equilibrium dictates defection. However, as a benevolent actor, this strategy adheres to a "Fair Play" principle:
    *   If `C_prev >= FCT` (or if all previous rounds were C): Play Cooperate (C). This assumes a norm of mutual benefit has been established.
    *   Otherwise: Play Defect (D).

**Edge Cases and Robustness:**
- **Sudden Drop in Cooperation:** If `C_prev` drops significantly (e.g., to zero) regardless of previous rounds, immediately switch to Defect (D) for one round to minimize losses, then return to the probabilistic rule in the next round.
- **k approaching 1:** As `k` gets closer to 1, the FCT increases towards `n`. The strategy becomes more conservative, requiring near-unanimous cooperation to sustain C.
- **k approaching n:** As `k` increases, the FCT decreases towards 1. The strategy becomes more generous and permissive, as the social cost of a single defector is lower relative to the total benefit of the public good.
'''

description_BENEVOLENT_15 = '''
Adopt a "Conditional Reciprocity" strategy initialized as Tit-for-Tat, modified to maximize the expected total cooperation across the group while insulating against exploitation.

### Decision Rules

**Round 1:**
Cooperate (C).

**Subsequent Rounds:**
Calculate the target contribution threshold, $T$. The goal is to sustain cooperation if the collective behavior demonstrates a willingness to contribute. Set $T = \lceil n / k \rceil$. This threshold represents the minimum number of cooperators required to make universal cooperation break-even for individual contributors.

If the number of cooperators in the previous round, $S_{t-1}$, meets or exceeds $T$:
- Cooperate (C).

If the number of cooperators in the previous round, $S_{t-1}$, is less than $T$:
- Defect (D) to minimize personal loss against non-cooperative groups.

### Edge Cases and Adjustments

**Last Round (Round $r$):**
Always Defect (D). Since there is no future interaction to incentivize, and the dominant strategy in a final round is to minimize the cost of contribution, defection is the rational choice to preserve the accumulated payoff.

**The "Forgiveness" Trigger:**
If $S_{t-1} < T$ (resulting in a Defect action) but $S_{t-1}$ increases relative to $S_{t-2}$, there is a risk of punishing a recovering group too harshly. 
- If $S_{t-1} > S_{t-2}$ AND $S_{t-1} \geq (T - 1)$:
  - Cooperate (C) to signal a willingness to restore the cooperative equilibrium.

**Pseudocode Logic:**

```python
def decide_action(round, history):
    if round == r:
        return D
    
    if round == 1:
        return C
    
    prev_cooperators = history[round - 1].S
    prev_prev_cooperators = history[round - 2].S if round > 2 else 0
    threshold = ceil(n / k)
    
    if prev_cooperators >= threshold:
        return C
        
    if (prev_cooperators > prev_prev_cooperators) and (prev_cooperators >= threshold - 1):
        return C
        
    return D
```

### Benevolent Alignment
This strategy is benevolent because it prioritizes the establishment and maintenance of a cooperative equilibrium (where $S \geq T$) over short-term gain. By using a threshold based on the payoff structure ($k/n$), the strategy ensures that cooperation is only sustained when it is mathematically beneficial for the collective, while the forgiveness mechanic allows the group to recover from accidental or noise-induced defections.
'''

description_BENEVOLENT_16 = '''
**Strategy: Adaptive Reciprocal Altruism with Conditional Forgiveness**

This strategy maintains cooperation as long as the aggregate behavior of opponents remains mutually beneficial, while strictly defecting in the final round to prevent exploitation.

**Decision Rules:**

1.  **Round 1:** Play **C**. This establishes a cooperative baseline and tests for the presence of other reciprocal players.

2.  **Intermediate Rounds (2 to r-1):**
    *   Define the "Cooperation Threshold" (T) as the minimum number of contributors required for universal cooperation to be more profitable than universal defection, calculated as T = ⌈n / k⌉.
    *   Let C(t-1) be the number of cooperators observed in the previous round.
    *   If C(t-1) ≥ T, play **C**.
    *   If C(t-1) < T, play **D**.

3.  **Final Round (r):** Play **D**. Since the game concludes after round r, there is no future interaction to incentivize, and defection maximizes the individual payoff against any remaining cooperative behavior.

**Handling Edge Cases:**

*   **Observed Cooperation Count (Aggregated):** If the aggregate observation is ambiguous due to the anonymous nature of opponents, rely strictly on the total count provided after each round. The logic applies the threshold T to the total count (including one's own contribution from the previous round if applicable).
*   **Threshold Calculation:** If n/k results in a non-integer, round up to the nearest integer to ensure the cooperation threshold is conservative (i.e., requires sufficient contributions to outweigh the temptation to defect).
*   **Initialization:** If a previous round history is unavailable (e.g., if re-starting or error states), revert to the Round 1 rule.

**Benevolent Logic:**
This strategy is benevolent by initiating and sustaining public goods contributions whenever the group demonstrates a capacity for mutual benefit. It avoids the "sucker's payoff" by withdrawing contributions when the group fails to sustain the collective threshold, while providing a necessary "clean break" in the final round to maintain game-theoretic rationality.
'''

description_BENEVOLENT_17 = '''
**Strategy: Conditional Tit-for-Tat with Forgiveness and End-Game Defection Avoidance**

The strategy relies on a simple threshold mechanism based on the observed cooperation rate of the group. Let $C_{total, t-1}$ be the total number of cooperators in the previous round, and let $T_c$ be the threshold for cooperation, defined as $T_c = \lceil \frac{n}{k} \rceil$.

**Round 1:**
Cooperate ($c=1$). This establishes a benevolent signal to the group.

**Rounds $t=2$ to $r-1$:**
Cooperate ($c=1$) if the previous round’s total contributions $C_{total, t-1}$ met or exceeded the threshold $T_c$. Otherwise, Defect ($c=0$).

*Exception for Forgiveness:* If the strategy defected in the previous round due to low group cooperation, it will "test" the group again by cooperating ($c=1$) with a probability $p=0.2$, regardless of the previous round's outcome. This allows for the recovery of cooperation if the group accidentally drifted into a defection cycle.

**Final Round ($t=r$):**
Cooperate ($c=1$) if and only if the average cooperation rate over all previous rounds $\bar{C} = \frac{1}{r-1} \sum_{t=1}^{r-1} (\frac{C_{total, t}}{n})$ exceeds $0.5$. Otherwise, Defect ($c=0$). This acknowledges the end-game incentive to defect but maintains benevolence if the group has demonstrated a consistent willingness to cooperate.

**Pseudocode Logic:**

```python
def get_action(round_number, total_history, n, k, r):
    threshold = ceil(n / k)
    
    # First round initialization
    if round_number == 1:
        return Cooperate
        
    # Final round decision
    if round_number == r:
        avg_cooperation_rate = mean(total_history) / n
        return Cooperate if avg_cooperation_rate > 0.5 else Defect
        
    # Mid-game logic
    prev_total = total_history[-1]
    
    if prev_total >= threshold:
        return Cooperate
    else:
        # Forgiveness mechanism
        if random() < 0.2:
            return Cooperate
        else:
            return Defect
```
'''

description_BENEVOLENT_18 = '''
**Strategy: Adaptive Reciprocal Tit-for-Tat with Forgiveness**

This strategy functions as a conditional cooperator, utilizing a "trust-but-verify" mechanism to encourage group-wide cooperation while protecting against persistent defectors. It tracks the average contribution rate of the group over time to determine future moves.

**Decision Rules:**

Define $C_t$ as the number of cooperators observed in round $t$.
Define $S_t = C_t - 1$ as the number of cooperators among the other $n-1$ players.
Define $AvgCoop$ as the cumulative average of $(S_t / (n-1))$ over all previous rounds.

1.  **First Round ($t=1$):**
    Play **Cooperate**.

2.  **Subsequent Rounds ($t > 1$):**
    *   If $t = r$ (the final round), always play **Defect** (as there is no future interaction to incentivize).
    *   Otherwise, calculate the threshold $T = 0.5$.
    *   If $AvgCoop \ge T$, play **Cooperate**.
    *   If $AvgCoop < T$, play **Defect** to minimize exploitation.

3.  **Reset Mechanism (Forgiveness):**
    To avoid "death spirals" caused by misinterpreted signals or noise, reset the memory after a period of exploitation. If the strategy has been in a Defect state for 3 consecutive rounds, switch to **Cooperate** for one round to test if the opponents have returned to cooperation.

**Pseudocode:**

```python
def get_action(round, total_rounds, history):
    # Base Case: Last round
    if round == total_rounds:
        return "D"
    
    # Base Case: First round
    if round == 1:
        return "C"
    
    # Calculate group contribution history
    all_s = [h.s for h in history]
    avg_coop = sum(all_s) / ((n - 1) * len(all_s))
    
    # Check for reset mechanism (Forgiveness)
    consecutive_defects = 0
    for h in reversed(history):
        if h.action == "D":
            consecutive_defects += 1
        else:
            break
            
    if consecutive_defects >= 3:
        return "C"
        
    # Standard conditional cooperation
    if avg_coop >= 0.5:
        return "C"
    else:
        return "D"
```
'''

description_BENEVOLENT_19 = '''
The strategy utilizes a conditional-cooperation mechanism based on a rolling average of aggregate contribution, designed to maximize social welfare while protecting against defection.

**1. Definitions and Initialization**
*   $T$: Total rounds in the game.
*   $t$: Current round index.
*   $S_{t-1}$: Aggregate number of cooperators in the previous round (observed).
*   $\tau$: Cooperation threshold. Set $\tau = 1$. This is the minimum number of contributors required to justify continued cooperation.
*   Let $history\_c$ be the cumulative number of cooperators observed in all previous rounds.
*   Let $history\_r$ be the number of rounds played so far.

**2. Decision Rules**
*   **Round 1:** Always cooperate ($C$). This signals benevolent intent and establishes a basis for mutual cooperation.
*   **Rounds $t \in [2, r-1]$:**
    *   Calculate the moving cooperation rate: $avg\_c = \frac{history\_c}{history\_r}$.
    *   If $S_{t-1} \ge \tau$, then cooperate ($C$).
    *   If $S_{t-1} < \tau$, defect ($D$).
*   **Round $r$ (Final Round):**
    *   Cooperate ($C$) if and only if the average cooperation rate of the opponents in all previous rounds met or exceeded a reciprocal threshold. Specifically, cooperate if $\frac{history\_c}{history\_r} \ge \frac{1}{n}$. Otherwise, defect ($D$).

**3. Adaptive Logic**
*   **Recovery:** If the strategy detects a shift back toward cooperation (e.g., if it defected due to low turnout but a subsequent round shows $S_{t-1} \ge \tau$), it resets to cooperate ($C$) in the immediate next round. This allows for "forgiveness" to restart mutual cooperation if the environment improves.
*   **Threshold Adjustment:** In the event that $k$ is close to $n$ (high efficiency), the threshold $\tau$ scales to $\lceil n/k \rceil$. If $k$ is small (close to 1), $\tau$ remains 1 to prioritize cautious mutualism.

**4. Pseudocode**

```python
def decide_action(round_number, total_rounds, observed_last_round_c, history_c, history_r, n, k):
    # Round 1
    if round_number == 1:
        return 'C'

    # Final Round
    if round_number == total_rounds:
        if (history_c / history_r) >= (1 / n):
            return 'C'
        else:
            return 'D'

    # Intermediate Rounds
    threshold = ceil(n / k) if (k / n) > 0.5 else 1
    
    if observed_last_round_c >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_BENEVOLENT_20 = '''
Adopt a conditional cooperation strategy based on the "Triggered Tit-for-Tat with Forgiveness" framework, designed to incentivize group cooperation while minimizing exploitation.

**Strategy Logic:**

1.  **Initialization (Round 1):**
    Always play Cooperate (C). This establishes a benevolent intent and invites mutual cooperation.

2.  **Tracking State:**
    Maintain two variables throughout the game:
    *   `cooperation_threshold`: The number of cooperators required to make cooperation individually rational (or at least break-even). Since the payoff for C is $(k/n) \times \sum c_j$ and the payoff for D is $1 + (k/n) \times (\sum c_j - 1)$, cooperation is rational if $k/n \times (\sum c_j) \geq 1 + k/n \times (\sum c_j - 1)$. This simplifies to $k/n \geq 1$, which is impossible under $k < n$. Therefore, cooperation is never individually rational in a single round. The strategy must rely on reciprocal altruism rather than immediate profit maximization.
    *   `cooperation_history`: The average cooperation rate of the group across all previous rounds.

3.  **Recursive Decision Rules (Rounds 2 to r-1):**
    Calculate the total cooperators in the previous round ($C_{t-1}$).
    *   If $C_{t-1} \geq \lceil n/k \rceil$ (the break-even point for the group): Play C.
    *   If $C_{t-1} < \lceil n/k \rceil$: Play D.
    *   *Forgiveness Clause:* If the previous round saw a sudden drop in cooperation to 0, but the cumulative cooperation rate over the last 3 rounds exceeds 50% of $n$, play C to attempt to restore cooperation.

4.  **Terminal Phase (Round r):**
    To prevent "end-game" defection common in finite repeated games, play C if the average number of cooperators over the previous $r-1$ rounds is $\geq 0.5n$. Otherwise, play D. This rewards consistent partners while protecting against persistent defectors.

**Pseudocode Implementation:**

```python
def decide_action(round, total_players, n, k, history):
    # Round 1
    if round == 1:
        return 'C'
    
    # End-game logic
    if round == r:
        avg_cooperators = sum(history) / (round - 1)
        return 'C' if avg_cooperators >= (n / 2) else 'D'
    
    # Conditional logic
    prev_cooperators = history[-1]
    
    # Break-even threshold calculation (Approximate)
    threshold = n / k
    
    # Standard response: reciprocate previous cooperation
    if prev_cooperators >= threshold:
        return 'C'
    
    # Forgiveness logic
    recent_history = history[-3:]
    if prev_cooperators == 0 and sum(recent_history) / (3 * n) > 0.5:
        return 'C'
        
    return 'D'
```
'''

description_BENEVOLENT_21 = '''
The strategy, "Benevolent Conditional Reciprocity," operates as a dynamic, threshold-based cooperation mechanism. Let $H_t$ be the history of total cooperators in previous rounds, where $C_{total, t-1}$ is the number of cooperators in the immediately preceding round, and $S_t = \sum_{m=1}^{t-1} C_{total, m}$ is the cumulative number of cooperative contributions observed.

### Decision Rules

**Round 1:**
Always play $C$ (Cooperate). This initiates cooperation and signals an intent to build a mutually beneficial equilibrium.

**Rounds 2 to $r-1$:**
Play $C$ if the following conditions are met:
1. $C_{total, t-1} \ge \lfloor \frac{n}{k} \rfloor$: Cooperation must be above the threshold required to make universal cooperation marginally profitable or neutral relative to defection.
2. If $C_{total, t-1} < \lfloor \frac{n}{k} \rfloor$, play $D$ (Defect) for one round as a punishment signal, unless the total cooperation rate in the previous round has shown a strictly positive trend (i.e., $C_{total, t-1} > C_{total, t-2}$). If the trend is positive, remain in $C$ to foster growth.

**Final Round ($r$):**
Play $C$ if and only if the average cooperation rate across all previous rounds $t \in [1, r-1]$ exceeds $0.5 \times n$. If the average cooperation was less than or equal to $50\%$ of the group, play $D$ to minimize losses in the final interaction.

### Pseudocode

```python
def decide_action(t, r, n, k, history):
    # Round 1: Initiate trust
    if t == 1:
        return 'C'
    
    # Last Round: Rational cutoff based on accumulated trust
    if t == r:
        avg_cooperation = sum(history['total_c']) / (r - 1)
        return 'C' if avg_cooperation > (0.5 * n) else 'D'
    
    # Intermediate Rounds: Conditional Reciprocity
    prev_c = history['total_c'][-1]
    threshold = n / k
    
    # Trend Analysis
    if t > 2:
        prev_prev_c = history['total_c'][-2]
        is_improving = prev_c > prev_prev_c
    else:
        is_improving = False
        
    if prev_c >= threshold or is_improving:
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling

*   **Sudden Defection:** If the group cooperation drops sharply (below the threshold without a positive trend), the strategy defaults to $D$ for one round. This serves as a "warning" to the population without permanently collapsing the cooperation attempt.
*   **Persistent Defection:** If the population fails to cooperate for two consecutive rounds, the strategy shifts to $D$ for all remaining rounds to prevent exploitation.
*   **Low $k$ values:** When $k$ is small (making the individual return on public goods minimal), the threshold $\lfloor \frac{n}{k} \rfloor$ increases. This naturally makes the strategy more conservative and prone to early defection, protecting the agent against populations that do not value the public good sufficiently.
'''

description_BENEVOLENT_22 = '''
The strategy is based on "Conditional Altruism," employing a variation of Tit-for-Tat adapted for aggregate public goods environments. It operates by attempting to establish mutual cooperation while maintaining a fallback against exploitation.

**Decision Rules:**

*   **Round 1:** Play **C**. Assume benevolence in others to foster a cooperative equilibrium from the start.

*   **Round $t$ (where $1 < t < r$):** Let $S_{t-1}$ be the number of cooperators observed in the previous round.
    *   Define a threshold $T = \lceil (n/k) \rceil$.
    *   If $S_{t-1} \geq T$, play **C**. This threshold represents the "break-even" point where a cooperator would receive a return equal to or greater than the private return of defecting ($k \cdot S_{t-1} / n \geq 1$).
    *   If $S_{t-1} < T$, play **D**. This indicates insufficient cooperation, signaling a need to punish non-contribution or protect against exploitation.

*   **Final Round ($t = r$):** Play **D**. Since there are no future rounds to influence, the incentive to maintain the cooperative reputation is absent. In the final round, the strategy prioritizes maximizing the individual payoff while acknowledging the termination of the game.

**Edge Cases & Logic:**

*   **Re-entry into Cooperation:** If the strategy is currently playing **D** due to low previous cooperation, it will re-evaluate cooperation only if a cooperative signal is received. However, because this is an aggregate-observation game (not individual), the strategy will "test" cooperation by switching to **C** if $S_{t-1} \geq T$ for a single round after a period of defection. 

*   **Mathematical Precision for $T$:**
    *   If $k \leq 1$, always play **D** in all rounds (as cooperation is strictly dominated).
    *   The threshold $T$ is calculated such that $\frac{k}{n} \cdot T \geq 1$. If $T > n$, cooperation is never rational; play **D** always.

*   **Benevolence Constraint:** If at any point the average total contribution over all previous rounds exceeds $0.8n$, the strategy adopts a "Forgiving" mode: ignore the $T$ threshold and play **C** for the remainder of the game (excluding the final round). This prioritizes sustaining high-cooperation equilibria over marginal gains from defection.
'''

description_BENEVOLENT_23 = '''
The strategy operates on a "Conditional Tit-for-Tat with Forgiveness and Last-Round Defection" framework, designed to incentivize mutual cooperation while protecting against exploitation.

### Core Logic

1.  **Initial Round:** Play **Cooperate (C)**. This signals a benevolent intent to establish a cooperative equilibrium.

2.  **Intermediate Rounds (2 to r-1):** Calculate the "Cooperation Threshold" ($T$) required for your contribution to be net-positive for the collective compared to the defection payoff. Since your contribution adds $1$ to the total pool, which is then multiplied by $k/n$, your contribution is individually optimal if $k/n > 1$ (impossible given $1 < k < n$) and collectively optimal if $k > 1$. To maintain benevolence, mirror the observed cooperation level of the group.

    *   **Decision Rule:**
        Let $S_{t-1}$ be the total number of cooperators in the previous round.
        *   If $S_{t-1} \ge \text{threshold}$: Cooperate.
        *   If $S_{t-1} < \text{threshold}$: Defect.

    *   **Threshold Determination:**
        Set the threshold at $n \times (1/k)$. This is the "break-even" point where the public good generated by the group’s contributions is sufficient to justify your own contribution.

    *   **Forgiveness Mechanism:**
        If you defected in the previous round due to low cooperation, observe the current state. If the group cooperation level recovers to $\ge n \times (1/k)$ despite your defection, immediately return to **Cooperate** in the next round. This prevents death spirals where all players defect because of a single round of low turnout.

3.  **Final Round (r):** Play **Defect (D)**. Because there are no future rounds to influence, the incentives are purely based on immediate payoff. Benevolence is exhausted by the terminal round, as cooperation provides no signaling value or future reward.

### Pseudocode

```python
def decide_action(round_number, n, r, k, history):
    # Rule 1: First round
    if round_number == 1:
        return 'C'
    
    # Rule 2: Last round
    if round_number == r:
        return 'D'
    
    # Rule 3: Intermediate rounds
    # Threshold for group cooperation to sustain mutual benefit
    threshold = (n / k)
    
    # Observe previous round cooperation
    previous_cooperators = history[-1]['total_cooperators']
    
    # If the group supports the public good, continue contributing
    if previous_cooperators >= threshold:
        return 'C'
    
    # If group cooperation is insufficient, defect to avoid exploitation
    else:
        return 'D'
```

### Edge Case Handling

*   **Sudden Drops:** If cooperation falls below the threshold, the strategy immediately switches to Defect. This protects against altruistic over-extension.
*   **Recovery:** If the group spontaneously cooperates again (signals benevolence), the strategy resets to Cooperate immediately.
*   **Stochastic/Noisy Environments:** If $n$ is large and the group cooperation fluctuates near the threshold due to error, utilize a smoothed threshold. Calculate the threshold as $T = (n/k) - 1$ to provide a buffer, ensuring that minor fluctuations do not trigger a collapse in cooperation.
'''

description_BENEVOLENT_24 = '''
Strategy: Conditional Reciprocal Benevolence (CRB)

CRB operates on the principle of conditional cooperation, maintaining a benevolent baseline while adjusting to the observed aggregate contribution levels of opponents.

Variables:
- `round_number`: Current round (t ∈ {1...r})
- `cooperation_threshold`: Minimum required total contributions from others to justify continued cooperation. This is set to `(n/k)` to ensure the expected return of cooperation is at least equal to the return of defection.
- `last_round_cooperators`: The number of players who contributed in the previous round (excluding self).

Decision Rules:
1. Round 1: Play C (Cooperate). This establishes a benevolent baseline and signals readiness for mutual cooperation.

2. Rounds 2 to r-1: Calculate `last_round_cooperators`.
   - If `last_round_cooperators` >= `cooperation_threshold`, play C. This rewards existing cooperation and sustains the group output.
   - If `last_round_cooperators` < `cooperation_threshold`, play D (Defect). This protects against exploitation by non-cooperative agents who reduce the group payoff below the sustainable equilibrium for a single cooperator.

3. Final Round (r): Play D (Defect). Because the game ends, future incentives for cooperation are non-existent. Defection is the rational choice to maximize terminal payoff, regardless of previous history, though the strategy remains benevolent by having cooperated for all preceding rounds where aggregate contribution was sufficient.

Pseudocode:
```
if t == 1:
    return C

if t == r:
    return D

# Calculate the minimum number of contributors needed to break even
# Payoff(C) = k/n * (C_others + 1)
# Payoff(D) = 1 + k/n * (C_others)
# Equilibrium: k/n * (C_others + 1) >= 1 + k/n * (C_others) 
# Simplifies to: k/n >= 1 (Which implies all players must cooperate)
# To be robust, use the threshold k/n * (C_others + 1) >= 1
threshold = ceil(n / k) - 1

if last_round_cooperators >= threshold:
    return C
else:
    return D
```

Edge Case Handling:
- If `k` is small such that `n/k > n-1` (i.e., mutual cooperation is not individually rational even if everyone else cooperates), the strategy defaults to D in all rounds to prevent irrational exploitation, maintaining maximum efficiency under strictly non-cooperative parameters.
- If `last_round_cooperators` is ambiguous (e.g., in a round where self played C, observe total - 1), the strategy assumes the worst-case scenario regarding specific player behavior but relies strictly on the observed aggregate count for the decision rule.
'''

description_BENEVOLENT_25 = '''
**Strategy: Conditional Benevolence with Forgiving Reciprocity**

This strategy is defined by a threshold-based conditional cooperation model, where cooperation is sustained as long as the aggregate group contribution meets an efficiency target.

**Initialization (Round 1):**
Always play Cooperate (C). This establishes a willingness to contribute and tests the collective responsiveness of the group.

**Main Decision Loop (Rounds 2 to r-1):**
Maintain a memory variable `group_cooperation_history` representing the average contribution rate of other players.

1. **Observe:** At the end of round $t-1$, calculate the cooperation rate of the group $S_{t-1} = (\sum c_j - c_{self}) / (n-1)$.
2. **Evaluate Threshold:**
   * If $S_{t-1} \ge 1/k$, play Cooperate (C). This threshold represents the break-even point where the marginal benefit of universal cooperation outweighs the cost of defection.
   * If $S_{t-1} < 1/k$, play Defect (D). This signals that the group is currently inefficient and protects against exploitation.
3. **Forgiveness Mechanism:**
   If the previous action was Defect (D) due to the threshold rule, return to Cooperate (C) if the group’s cooperation rate $S$ increases by more than 20% relative to the previous round, or if the average cooperation rate over the last three rounds exceeds $1/k$. This allows the strategy to "restart" cooperation if the group attempts to reform.

**Termination (Final Round):**
Always play Defect (D). In a finite game with no reputation carry-over into future games, the final round is a one-shot prisoner's dilemma where the dominant strategy is to defect to maximize terminal payoff, assuming other rational actors will also defect.

**Pseudocode:**

```python
def choose_action(round, history, n, k):
    if round == 1:
        return 'C'
    
    if round == r:
        return 'D'

    # Calculate aggregate cooperation rate of opponents in the previous round
    # history stores lists of [my_c, total_c]
    total_c_prev = history[-1][1]
    my_c_prev = history[-1][0]
    opp_c_prev = total_c_prev - my_c_prev
    opp_rate = opp_c_prev / (n - 1)

    # Threshold: Must be efficient to continue cooperation
    threshold = 1 / k
    
    if opp_rate >= threshold:
        return 'C'
    else:
        # Check for recovery signal (forgiveness)
        recent_avg = calculate_recent_avg(history, window=3)
        if recent_avg > threshold:
            return 'C'
        return 'D'
```
'''

description_BENEVOLENT_26 = '''
**Strategy Name: Conditional Tit-for-Tat with Forgiveness and End-Game Defection**

The strategy relies on a threshold-based cooperation model designed to foster mutual benefit while protecting against exploitation.

**Decision Rules:**

1.  **First Round (Round 1):** Play **Cooperate (C)**. This initiates the potential for mutual cooperation.

2.  **Subsequent Rounds (Round t > 1):**
    *   Observe the number of contributors from the previous round, $C_{t-1}$.
    *   Let $S_{t-1} = C_{t-1} - 1$ (the number of other players who cooperated).
    *   Calculate the *Cooperation Ratio* ($R_{t-1} = S_{t-1} / (n-1)$).
    *   If $R_{t-1} \geq \text{Threshold}$, play **Cooperate (C)**.
    *   If $R_{t-1} < \text{Threshold}$, play **Defect (D)**.

3.  **Threshold Definition:**
    *   The Threshold is set to $1/k$. This ensures cooperation is maintained if the collective contribution provides a positive net return on the investment.

4.  **Forgiveness:**
    *   If the strategy defected in the previous round due to a low $R_{t-1}$, play **Cooperate (C)** in the current round with a probability of 0.2. This serves as a "probing" mechanism to determine if the group has returned to cooperative behavior, allowing the strategy to resume mutual cooperation if the opponents respond positively.

5.  **Final Round (Round r):**
    *   Regardless of previous history or threshold calculations, play **Defect (D)**. This mitigates the risk of being exploited in the final opportunity for interaction, where future retaliation or cooperation signals are irrelevant.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, n, k, history):
    # Final round constraint
    if round_number == total_rounds:
        return 'D'
    
    # First round initialization
    if round_number == 1:
        return 'C'
    
    # Analyze previous round
    # 'history' contains list of cooperators in rounds 1 to t-1
    prev_cooperators = history[-1] 
    others_cooperated = prev_cooperators - 1 if prev_cooperated_me else prev_cooperators
    
    threshold = 1 / k
    cooperation_ratio = others_cooperated / (n - 1)
    
    # Decision logic with forgiveness mechanism
    if cooperation_ratio >= threshold:
        return 'C'
    else:
        # Check if we should probe for forgiveness
        if random() < 0.2:
            return 'C'
        else:
            return 'D'
```
'''

description_BENEVOLENT_27 = '''
The strategy follows a conditional "Win-Stay, Lose-Shift" logic modified to promote mutual cooperation through an initial trust-building phase and a forgiveness mechanism.

**Definitions:**
*   $T$: Total rounds remaining ($r - \text{current\_round} + 1$).
*   $C_{t-1}$: Total number of cooperators observed in the previous round.
*   $Status$: A variable tracked per round, initialized to "Cooperative".

**Decision Logic:**

1.  **Round 1:**
    Play **Cooperate (C)**. Set $Status = \text{"Cooperative"}$.

2.  **Rounds 2 through $r-1$:**
    *   If $Status == \text{"Cooperative"}$:
        *   If $C_{t-1} \ge \lfloor n/2 \rfloor$: Play **C**.
        *   If $C_{t-1} < \lfloor n/2 \rfloor$: Play **Defect (D)**, set $Status = \text{"Defensive"}$.
    *   If $Status == \text{"Defensive"}$:
        *   If $C_{t-1} = n$: Play **C**, reset $Status = \text{"Cooperative"}$.
        *   Otherwise: Play **D**.

3.  **Final Round ($t = r$):**
    *   If $Status == \text{"Cooperative"}$: Play **C**.
    *   If $Status == \text{"Defensive"}$: Play **D**.

**Edge Case Handling:**
*   **Minimal Cooperation:** In any round where $C_{t-1} = 0$, immediately switch to $Status = \text{"Defensive"}$ for the next round regardless of previous state.
*   **Parameter Sensitivity:** If $k \le 1$, the strategy defaults to Defect (D) in all rounds as cooperation yields no positive externality.
*   **Resumption of Trust:** The transition from "Defensive" back to "Cooperative" requires a round of universal cooperation ($n$ players). If a player deviates from this, the strategy remains "Defensive" until $C_{t-1} = n$ is achieved in a subsequent round.
'''

description_BENEVOLENT_28 = '''
This strategy, "Generous Tit-for-Tat with Threshold Monitoring," aims to cultivate mutual cooperation while protecting against persistent defectors. It balances benevolence with accountability.

**Core Mechanism**

The strategy relies on tracking the "contribution density," defined as the fraction of other players who cooperated in the previous round.

**Initialization and First Round**
*   **Round 1:** Play C. Assume benevolence is the baseline until proven otherwise.

**Subsequent Rounds (2 to r-1)**
Calculate the contribution rate of the other $n-1$ players from the previous round, $C_{prev} = (\text{TotalCooperators}_{prev} - \text{MyPreviousAction}) / (n-1)$.

Apply the following conditional logic:
1.  **If $C_{prev} > 0.5$:** Play C. Reward the collective effort.
2.  **If $C_{prev} == 0.5$:** Play C with probability 0.5 (stochastic adaptation).
3.  **If $C_{prev} < 0.5$:** Play D. Defect in response to insufficient group cooperation to avoid exploitation.

**Special Case: The Final Round (r)**
Regardless of history, play D. This is a non-cooperative dominant strategy equilibrium in a finite game with no further future interactions, serving as a terminal reset to optimize individual payoff in the final step.

**Implementation Logic (Pseudocode)**

```python
def decide_action(round_number, total_rounds, history_of_others):
    # Rule 1: First Round
    if round_number == 1:
        return 'C'

    # Rule 2: Last Round
    if round_number == total_rounds:
        return 'D'

    # Rule 3: Intermediate Rounds
    # Calculate previous round's cooperation rate of opponents
    # history_of_others stores count of cooperators from previous round
    others_cooperated = history_of_others[-1]
    
    # Adjust for self-contribution if necessary
    if my_previous_action == 'C':
        others_cooperated -= 1
        
    contribution_rate = others_cooperated / (n - 1)

    if contribution_rate > 0.5:
        return 'C'
    elif contribution_rate == 0.5:
        return 'C' if random() > 0.5 else 'D'
    else:
        return 'D'
```

**Adaptive Refinement**
If the group cooperation rate stays at 0 for more than 2 consecutive rounds, reset the strategy by playing C in the next round to offer a "peace pipe" or restart signal, attempting to break out of a defection trap. If this attempt fails (resulting in another 0), revert to the standard conditional logic for the remainder of the game.
'''

description_BENEVOLENT_29 = '''
**Strategy: Tit-for-Tat with Conditional Forgiveness**

This strategy attempts to induce mutual cooperation by mirroring the collective behavior of opponents, using a threshold-based response mechanism. It is benevolent, initiating cooperation, but robust, punishing defection while remaining open to reconciliation.

**Parameters and State Variables:**
- `last_round_cooperators`: The number of contributors in the previous round (including self).
- `threshold`: A value `n / k` rounded up, representing the minimum number of cooperators required to make the return on contribution neutral or positive compared to pure defection. If the total cooperators `S` meets `(k/n) * S >= 1`, cooperation is efficient.
- `my_contribution`: The action taken in the previous round (1 for C, 0 for D).

**Decision Rules:**

1.  **Round 1:** Always Cooperate. Establish benevolent intent immediately.

2.  **Rounds 2 to r-1:**
    *   Calculate `cooperators_excluding_me`: `last_round_cooperators - my_contribution`.
    *   If `cooperators_excluding_me >= threshold - 1`: Cooperate. This signals that the group is sustaining a sufficiently productive environment.
    *   If `cooperators_excluding_me < threshold - 1`: Defect. This protects against exploitation by "free riders" who are suppressing the public good below the break-even point.
    *   *Forgiveness trigger:* If the strategy previously defected, switch back to Cooperate if the current `cooperators_excluding_me` rises to or exceeds `threshold` for a single round, regardless of the previous state. This allows for restarting cooperation after a lapse in group cohesion.

3.  **Final Round (Round r):**
    *   If `cooperators_excluding_me >= threshold - 1`: Cooperate.
    *   If `cooperators_excluding_me < threshold - 1`: Defect.
    *   *Note:* There is no incentive to deviate from the standard rule set in the final round because the strategy prioritizes group-level stability and norm enforcement over short-term gain.

**Pseudocode:**

```python
def get_action(round_num, history):
    if round_num == 1:
        return Cooperate
    
    threshold = ceil(n / k)
    prev_total = history.last_round_cooperators
    prev_my_action = history.my_last_action
    
    # Calculate how many others contributed
    others_contributed = prev_total - (1 if prev_my_action == Cooperate else 0)
    
    # Determine next action
    if others_contributed >= (threshold - 1):
        return Cooperate
    else:
        return Defect
```

**Edge Case Handling:**
- **Initial Defection:** If the group defects in Round 1, the strategy defects in Round 2, but resumes cooperation the moment the threshold is met, preventing permanent "death spirals" of mutual defection.
- **Small Population Constraints:** If `k` is very close to `n` such that `threshold` is 1 or 2, the strategy remains permissive, requiring only minimal group support to maintain cooperation.
- **Round-by-Round Volatility:** By using the previous round's data as the sole signal, the strategy reacts immediately to shifts in group behavior without requiring long-term memory or complex pattern matching, ensuring consistency.
'''

description_BENEVOLENT_30 = '''
**Strategy: Conditional Reciprocity with Threshold-Based Forgiveness**

This strategy operates on the principle of "benevolent conditional cooperation," aiming to maximize total group welfare while protecting against exploitation.

**Initialization**
In the first round, always play **Cooperate (C)**. This signals a commitment to mutual cooperation.

**Ongoing Decision Logic (Rounds 2 to r-1)**
For each round $t$, calculate the contribution rate of the group from the previous round ($t-1$): $S_{t-1} = (\text{Total Cooperators in } t-1) / n$.

1.  **Cooperation:** If $S_{t-1} \ge \tau$, play **Cooperate (C)**.
    *   The threshold $\tau$ is set to $1/k$. This threshold represents the break-even point where your contribution is recouped by the return on the public good.
2.  **Punishment/Defection:** If $S_{t-1} < \tau$, play **Defect (D)**. This response serves as a temporary withdrawal of cooperation to incentivize others to contribute.
3.  **Forgiveness:** If the group failed to meet the threshold in the previous round, but the number of cooperators was exactly one less than the threshold requirement, play **Cooperate (C)** with a probability $p = 0.5$. This re-opens the door to cooperation if the previous round was a "near miss," preventing perpetual cycles of defection.

**Terminal Phase (Round r)**
In the final round, the incentive to defect is maximized because there are no future rounds to punish non-cooperation. However, to maintain benevolence, use a "Generous Last Round" rule:

*   If the strategy cooperated in round $r-1$, play **Cooperate (C)** regardless of the group's past behavior.
*   If the strategy defected in round $r-1$, play **Defect (D)**.

**Pseudocode**

```python
def decide_action(round_number, history, n, k):
    threshold = 1/k
    
    if round_number == 1:
        return 'C'
    
    if round_number == r:
        if history.last_action == 'C':
            return 'C'
        else:
            return 'D'
            
    # Calculate group cooperation rate from previous round
    # Observe opponents' contribution count
    prev_total_cooperators = history.get_prev_total()
    prev_group_rate = prev_total_cooperators / n
    
    # Check if we were betrayed in the last round (we cooperated, they didn't)
    # If group rate is below threshold, punish
    if prev_group_rate < threshold:
        # Check for near-miss forgiveness
        if prev_total_cooperators >= (n * threshold) - 1:
            return random_choice(['C', 'D']) # 50/50 split
        return 'D'
    
    return 'C'
```
'''

description_BENEVOLENT_31 = '''
Play Tit-for-Tat with a forgiving threshold mechanism.

**Core Decision Rule:**
In every round `t`, cooperate if and only if the number of cooperators in the previous round `t-1` was greater than or equal to the "cooperation threshold."

**Threshold Definition:**
The threshold `T` is calculated based on the game parameters and rounds remaining.
*   Let `C_{t-1}` be the number of cooperators observed in the previous round.
*   Let `S_{t-1}` be the number of cooperators *excluding oneself* from the previous round. Note that `S_{t-1} = C_{t-1} - 1` if you cooperated, or `S_{t-1} = C_{t-1}` if you defected.
*   Cooperate if `S_{t-1} >= target_cooperation_count`, where `target_cooperation_count` is set to `n - 1`.

**Initialization and Edge Cases:**
1.  **First Round (t=1):** Cooperate. This initiates the potential for mutual cooperation and signals a benevolent intent.
2.  **Last Round (t=r):** Defect. Because the game ends, there is no future incentive for others to maintain cooperation, and any previous cooperation cannot be reciprocated. This avoids exploitation in the terminal phase.
3.  **Observation Ambiguity:** If you cooperated in `t-1` and `C_{t-1} == 0`, you have received no signal of cooperation. Reset to Defect for `t`. If you defected in `t-1` and `C_{t-1} > 0`, you have observed potential cooperation; cooperate in `t` to rejoin the cooperative cycle (forgiveness).

**Pseudocode:**

```python
def choose_action(round_t, n, k, r, history):
    if round_t == 1:
        return 'C'
    
    if round_t == r:
        return 'D'
    
    # Analyze the previous round's outcome
    prev_total_C = history.last_round_cooperators
    my_last_action = history.my_last_action
    
    # Calculate how many others cooperated
    if my_last_action == 'C':
        others_C = prev_total_C - 1
    else:
        others_C = prev_total_C
        
    # Threshold for benevolence: 
    # Attempt to sustain cooperation if almost everyone else is cooperating
    if others_C >= (n - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_BENEVOLENT_32 = '''
The strategy follows a "Conditional Tit-for-Tat with Forgiveness" approach, optimized to encourage mutual cooperation while protecting against persistent defectors.

**1. Definitions and Initialization**
*   `r`: Total number of rounds.
*   `n`: Number of players.
*   `k`: Multiplication factor.
*   `history`: A list of the number of cooperators in each past round.
*   `threshold`: The minimum number of cooperators required to justify continued cooperation. Calculate `threshold` as `⌈n/k⌉`. If `k` is such that `n/k` is an integer, set `threshold = (n/k) + 1` to ensure a net gain for the group.

**2. Round 1**
Always play Cooperate (C). Starting with trust establishes the potential for a cooperative equilibrium.

**3. Rounds 2 to r-1**
Play Cooperate (C) if the previous round’s total contributions met or exceeded the `threshold`.
If the previous round’s total contributions fell below the `threshold`, play Defect (D) to avoid exploitation.

*Forgiveness Mechanism:*
If the strategy is currently playing Defect (D) due to a previous round’s failure, monitor the subsequent round. If, while playing Defect, the total contributions from the other `n-1` players (the number of cooperators in the last round) meets or exceeds `threshold`, switch back to Cooperate (C) in the next round. This allows the group to recover from accidental or momentary lapses in coordination.

**4. Final Round (Round r)**
In the final round, the incentive to defect is maximized because there is no future interaction to punish or reward. However, to maintain benevolence, play Cooperate (C) unless the average number of cooperators in the last three rounds (or all rounds, if less than three have passed) was strictly less than the `threshold`. If that average was below the `threshold`, play Defect (D) to prevent a final-round exploitation.

**Pseudocode Logic:**

```python
def decide_action(round_num, r, n, k, history):
    threshold = ceil(n / k)
    
    # First round
    if round_num == 1:
        return 'C'
    
    # Last round: Conditional on recent performance
    if round_num == r:
        recent_history = history[-3:] if len(history) >= 3 else history
        avg_cooperators = sum(recent_history) / len(recent_history)
        return 'C' if avg_cooperators >= threshold else 'D'
    
    # Standard rounds
    last_round_cooperators = history[-1]
    
    # If last round was good, continue cooperating
    if last_round_cooperators >= threshold:
        return 'C'
    
    # If last round was bad, defect, but check for forgiveness
    # (The system naturally forgives if others return to cooperation 
    # while we are defecting, because history will show they met threshold)
    return 'D'
```
'''

description_SELFISH_5 = '''
Play "Tit-for-Tat with a Greedy Threshold" (TFT-GT). This strategy aims to maintain cooperation when the group demonstrates sufficient reciprocity, while defecting immediately upon detection of exploitation or when the potential for future gains vanishes.

**Decision Rules**

Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $T$ be the threshold of cooperators required to justify cooperation. Calculate $T = \lceil n/k \rceil$.

*   **Round 1:** Play **Defect**. (Establishing a baseline of selfishness and testing the group's tolerance for non-contribution).
*   **Final Round ($t = r$):** Play **Defect**. (The dominant strategy in the final round is always to defect, as there are no future rounds to incentivize cooperation).
*   **Intermediate Rounds ($1 < t < r$):**
    *   If $C_{t-1} \geq T$: Play **Cooperate**. (The public good is being produced efficiently enough that your contribution results in a net individual gain or acceptable break-even point compared to the group).
    *   If $C_{t-1} < T$: Play **Defect**. (The group is under-contributing; contributing would be a net loss for you individually).

**Pseudocode**

```python
# Parameters: n (players), k (factor), r (rounds)
# Variables: t (current round), c_prev (cooperators in previous round)

T = ceil(n / k)

if t == 1:
    action = Defect
elif t == r:
    action = Defect
else:
    if c_prev >= T:
        action = Cooperate
    else:
        action = Defect
```

**Edge Case Behavior**

*   **When $k \geq n$:** The threshold $T$ becomes 1. You will cooperate in all intermediate rounds regardless of previous history, as your contribution is always self-sustaining.
*   **When $k$ is low (near 1):** The threshold $T$ approaches $n$. You will defect almost exclusively unless near-universal cooperation is established, protecting you from being a "sucker" in a group with low contribution density.
*   **Sudden Drop in Cooperation:** If the group's cooperation drops below $T$, your immediate defection in the next round serves as a punitive signal to recover the threshold or minimize your losses.
'''

description_SELFISH_6 = '''
For round 1: Cooperate (C).

For rounds 2 through $r-1$:
Observe the number of cooperators from the previous round ($C_{t-1}$).
If $C_{t-1} \ge \text{threshold}$, then Cooperate (C).
The threshold is defined as $\frac{n}{k}$.
If $C_{t-1} < \text{threshold}$, then Defect (D).

For the final round $r$:
Defect (D).

In all scenarios, if the previous round’s contribution count $C_{t-1}$ resulted in a payoff lower than the payoff obtained by defecting alone (which occurs when $C_{t-1} < \frac{n}{k}$), immediately switch to Defect (D) for all subsequent rounds, regardless of future cooperation by others.
'''

description_SELFISH_7 = '''
### Strategy: Tit-for-Tat Trigger with Threshold Conditioning

**Core Logic:**
The strategy aims to maximize cumulative payoff by incentivizing cooperation through conditional reciprocity while remaining immune to exploitation. It maintains cooperation only as long as the aggregate contribution of the group remains above a critical threshold required for net positive utility.

**Decision Rules:**
Let $S_{t-1}$ be the number of cooperators observed in round $t-1$. Let $c_t$ be the action for the current round $t$.

1. **Initial Round ($t=1$):**
   - Play **Cooperate (C)**. This serves as an initial probe of the group's cooperativeness.

2. **Subsequent Rounds ($t > 1$):**
   - If $t = r$ (the final round): Play **Defect (D)**. Regardless of prior cooperation, there is no future incentive to sustain the group.
   - If $1 < t < r$:
     - Calculate the "Break-even Contribution" ($T_b$). This is the minimum number of total cooperators ($C_{total}$) required such that playing $C$ yields a payoff at least equal to playing $D$.
     - Solve for $C_{total}$ in: $0 + \frac{k}{n} \cdot C_{total} \geq 1 + \frac{k}{n} \cdot (C_{total} - 1)$
     - This simplifies to $C_{total} \geq \frac{n}{k}$. Set threshold $T = \lceil n/k \rceil$.
     - If $S_{t-1} \geq T$: Play **Cooperate (C)**.
     - If $S_{t-1} < T$: Play **Defect (D)**. This punishes the group for failing to maintain a mutually beneficial public good level.

**Edge Case Handling:**
- **Inability to reach threshold:** If the required threshold $T$ is greater than $n$ (which occurs if $k < 1$, though excluded by parameters), always play $D$.
- **Sudden drop-offs:** If a round results in $S_{t-1} < T$, the strategy switches to $D$. It will only revert to $C$ if the group signals a return to collective cooperation. Specifically, after a defecting round, check if $S_{t} \geq T$ in the subsequent round. If the group coordinates back above the threshold, resume cooperation in $t+1$.
- **Last Round Override:** The "Defect" rule for $t=r$ is absolute. It ignores previous cooperation history and aggregate observations to prevent final-round exploitation by other agents.
'''

description_SELFISH_8 = '''
The strategy employs a "Conditional Tit-for-Tat with Defection Threshold" approach, designed to incentivize contribution while minimizing exploitation in the final round.

**Round 1:**
Play Defect (D). This establishes a baseline and prevents immediate exploitation by unconditional cooperators.

**Rounds 2 to r-1:**
Assess the total number of cooperators from the previous round (S_{t-1}). Define the "Benefit Threshold" (T) as the minimum number of cooperators required for cooperation to be individually rational (where the payoff of Cooperating ≥ payoff of Defecting). Solving the inequality (k/n) * (S + 1) ≥ 1 + (k/n) * S results in the threshold T = ceil(n/k).

1.  If S_{t-1} ≥ T: Play Cooperate (C).
2.  If S_{t-1} < T: Play Defect (D).

**Final Round (r):**
Play Defect (D) unconditionally. Regardless of historical cooperation, there is no future round to punish defection or incentivize ongoing contribution; therefore, maximizing the immediate payoff via defection is the dominant strategy.

**Pseudocode:**

```python
# Constants: n, k, r are fixed
threshold = ceil(n / k)

def play_round(round_number, history):
    # Rule 1: Always defect in the last round
    if round_number == r:
        return 'D'
    
    # Rule 2: First round baseline
    if round_number == 1:
        return 'D'
    
    # Rule 3: Conditional cooperation based on previous aggregate
    prev_cooperators = history.last_round_total_cooperators
    
    # Check if cooperation is profitable
    # If the number of cooperators is sufficient to make 
    # my contribution net-positive, I cooperate to sustain the good.
    if prev_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_9 = '''
1. **Initial Round (t=1):** Play Defect (D). Establish a baseline of play without risking the endowment.

2. **Monitoring Phase (t=2 to r-1):**
   Calculate the "Cooperation Threshold" ($T$) required for cooperation to be profitable:
   If playing Cooperate (C) results in a payoff $π_C = (k/n) \times (\text{Cooperators}_{t-1})$, and playing Defect (D) results in a payoff $π_D = 1 + (k/n) \times (\text{Cooperators}_{t-1} - 1)$, then cooperate if and only if:
   $(k/n) \times \text{Cooperators}_{t-1} > 1 + (k/n) \times (\text{Cooperators}_{t-1} - 1)$
   Which simplifies to: $k/n > 1 - k/n$, or $\text{Cooperators}_{t-1} > n/k$.

   Decision Rule:
   - If (Total Cooperators in $t-1$) > $n/k$, play Cooperate (C).
   - If (Total Cooperators in $t-1$) ≤ $n/k$, play Defect (D).

3. **Final Round (t=r):** Always play Defect (D). Since there are no future rounds to incentivize cooperation, the dominant strategy is to maximize the immediate payoff by keeping the endowment.

4. **Pseudocode:**

```
// Constants: n, k, r
// Inputs: t (current round), C_prev (cooperators in previous round)

if t == 1:
    return Defect
if t == r:
    return Defect

threshold = n / k
if C_prev > threshold:
    return Cooperate
else:
    return Defect
```
'''

description_SELFISH_10 = '''
The strategy employs a conditional cooperation mechanism known as "Win-Stay, Lose-Shift" tailored for public goods, constrained by a strict defection trigger in the final rounds.

**Definitions:**
*   $C_t$: Number of cooperators in round $t$.
*   $m_t$: My action in round $t$ ($1$ for Cooperate, $0$ for Defect).
*   $T$: Total number of rounds.
*   $threshold = (n / k)$: The critical number of cooperators required to make cooperation individually rational (i.e., when cooperation yields at least as much as defection).

**Decision Rules:**

1.  **Round 1:** Play $C$ (Cooperate) to test the cooperative baseline of the group.

2.  **Rounds 2 to $T-1$:**
    *   Calculate the outcome of the previous round ($t-1$).
    *   If $C_{t-1} \ge threshold$, play $C$.
    *   If $C_{t-1} < threshold$, play $D$.
    *   *Exception:* If I played $D$ in round $t-1$ and the total number of cooperators $C_{t-1}$ was sufficient to make cooperation profitable for a cooperator (i.e., $C_{t-1} \ge threshold$), I return to $C$ in round $t$ to attempt to restore the cooperative equilibrium. If $C_{t-1} < threshold$ while I played $D$, I maintain $D$.

3.  **Final Round ($T$):** Always play $D$ (Defect). Since there is no future interaction to incentivize or punish opponents, playing $C$ provides no strategic return.

**Pseudocode:**

```python
if current_round == T:
    return Defect

if current_round == 1:
    return Cooperate

# Check previous round performance
prev_cooperators = history[current_round - 1].total_cooperators
prev_my_action = history[current_round - 1].my_action

if prev_my_action == Cooperate:
    if prev_cooperators >= (n / k):
        return Cooperate
    else:
        return Defect
else: # I played Defect previously
    if prev_cooperators >= (n / k):
        return Cooperate
    else:
        return Defect
```

**Edge Case Handling:**
*   **Insufficient Data:** If the game provides no history (though defined as having history), default to $C$ for rounds 1 through $T-1$.
*   **Tie-breaking:** If $C_{t-1}$ is exactly $n/k$, the decision rule defaults to Cooperation.
*   **Endgame Horizon:** The strategy strictly adheres to the $T$-round horizon, treating the penultimate round as the final opportunity to sustain cooperation. If the opponent pool seems to be defecting, the "Lose-Shift" component ensures rapid withdrawal to $D$ to minimize losses.
'''

description_SELFISH_11 = '''
**Strategy: Conditional Defection with Forgiving Threshold**

The core objective is to maximize payoff by incentivizing contribution from others while avoiding exploitation in the final rounds. The strategy relies on maintaining a "conditional cooperation" state, transitioning to permanent defection when the return on investment falls below the threshold of private defection.

**Definitions:**
*   $T$: Current round number.
*   $R$: Total number of rounds.
*   $C_{t}$: Number of other players who contributed in round $t$.
*   $n$: Number of players.
*   $k$: Multiplication factor.
*   $Threshold$: The minimum number of other contributors required to make cooperation individually rational. Since the payoff of cooperating is $\frac{k}{n} \times (1 + C_{t})$ and the payoff of defecting is $1 + \frac{k}{n} \times C_{t}$, cooperation is rational only if $\frac{k}{n} > 1$. Because $k < n$ in this game, cooperation is strictly dominated by defection in any single round. Therefore, cooperation is only rational if it induces future cooperation from others.

**Decision Rules:**

1.  **Round 1:** Play $C$ (Cooperate). This establishes a baseline and tests for the existence of other reciprocal players.

2.  **Rounds 2 through $R-1$:**
    *   If $C_{t-1} \ge \lfloor \frac{n-1}{2} \rfloor$: Play $C$ (Cooperate). This assumes that if half or more of the other players contributed, the group is sufficiently cooperative to justify continued investment.
    *   If $C_{t-1} < \lfloor \frac{n-1}{2} \rfloor$: Play $D$ (Defect). If the group fails to sustain a majority contribution, stop contributing immediately to minimize losses.

3.  **Final Round ($R$):** Play $D$ (Defect). Regardless of history, the final round provides no opportunity for future reciprocity, making defection the dominant strategy for a self-interested player.

4.  **Recidivism Rule (For-giving trigger):** If the strategy is currently playing $D$ because of a previous round's failure, but the total number of contributors in the previous round ($C_{t-1}$) is $\ge \lfloor \frac{n-1}{2} \rfloor + 1$, reset to $C$ (Cooperate). This allows for recovery if the group performance improves significantly.

**Pseudocode:**

```python
if current_round == R:
    return D

if current_round == 1:
    return C

last_contributors = get_last_round_contributors()
threshold = floor((n - 1) / 2)

if last_contributors >= threshold:
    return C
else:
    return D
```
'''

description_SELFISH_12 = '''
**Strategy Name:** Conditional Reciprocity-Defection (CRD)

**Decision Logic:**

1.  **Round 1:** Play D (Defect).
    *   *Rationale:* Without prior information, minimizing risk against potential exploiters is optimal.

2.  **Rounds 2 to r-1:** Observe the number of cooperators from the previous round (S_{t-1}).
    *   Calculate the threshold for cooperation (T) where playing C yields a higher payoff than playing D:
        T = (n * (1 - k/n)) / (k/n) = (n - k) / k
        (If the number of other cooperators is above this threshold, cooperating is individually rational.)
    *   If S_{t-1} > T: Play C (Cooperate).
    *   If S_{t-1} <= T: Play D (Defect).
    *   *Edge Case:* If the number of other cooperators in the previous round was high enough to sustain cooperation, reward that group by cooperating. If the number of cooperators falls below the threshold, immediately switch to defection to protect resources.

3.  **Round r (Final Round):** Play D (Defect).
    *   *Rationale:* There is no future round to incentivize or punish, so the dominant strategy is to maximize the final round payoff by keeping the endowment.

**Pseudocode:**

```python
def choose_action(round, total_cooperators_prev, n, k):
    # Determine the break-even threshold for cooperation
    # Cooperating gives (k/n) * (S + 1)
    # Defecting gives 1 + (k/n) * S
    # Cooperate if (k/n) * (S + 1) > 1 + (k/n) * S
    # Which simplifies to k/n > 1, but since 1 < k < n,
    # the threshold logic must account for the group composition.
    
    threshold = (n / k) - 1

    if round == 1:
        return "D"
    
    if round == r:
        return "D"
    
    # Check if the number of others cooperating is sufficient
    # to make cooperation personally beneficial
    if total_cooperators_prev > threshold:
        return "C"
    else:
        return "D"
```
'''

description_SELFISH_13 = '''
Define a threshold of reciprocity $T = n/k$. Since the game is simultaneous-move and anonymous, maintain a belief state $B$ representing the probability distribution of opponent cooperation levels. 

**Decision Logic:**

1.  **Round 1:** Play **D**. This minimizes initial risk while establishing a baseline for the aggregate cooperation level of opponents ($S_1$) without incurring the cost of contribution.

2.  **Rounds 2 to $r-1$:**
    *   Calculate the average number of cooperators from the previous round, $S_{t-1}$.
    *   If $S_{t-1} \geq T$, play **C** (Cooperate). This conditional cooperation exploits the "social" behavior of others to maximize the public good return while remaining within the bounds of a profitable exchange (where the marginal return of the public good outweighs the private cost of contribution).
    *   If $S_{t-1} < T$, play **D** (Defect). If the aggregate contribution is below the threshold $T$, the public good return is insufficient to justify the cost of contribution. By defecting, minimize losses when the collective effort is failing.

3.  **Round $r$ (Final Round):** Play **D** regardless of historical performance. Since there are no future interactions, the incentive for maintaining a reputation or influencing future opponent behavior is zero. Defection is the dominant strategy for the final round to capture the private endowment while potentially benefiting from any lingering, unconditional cooperation from others.

**Pseudocode:**

```python
def get_action(round_t, total_rounds, history_of_cooperators, n, k):
    threshold = n / k
    
    if round_t == total_rounds:
        return 'D'
    
    if round_t == 1:
        return 'D'
        
    last_cooperators = history_of_cooperators[-1]
    
    if last_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_14 = '''
**Strategy: Threshold-Triggered Conditional Cooperation**

This strategy maximizes individual payoff by maintaining cooperation only as long as the aggregate behavior of opponents provides a sufficient return on investment, while aggressively defecting when the cooperative threshold is not met or when the game enters its final stage.

**Decision Rules:**

Define the *Break-Even Threshold* (T) as the minimum number of cooperators required to make playing C at least as profitable as playing D. Based on the payoff function, you play C if the return from the public good when you contribute exceeds the return from defecting and relying solely on others:

$T = \lceil \frac{n}{k} \rceil$

For any round $t$ where $1 \leq t < r$:

1.  **First Round ($t=1$):** Play **Cooperate (C)** to initiate the possibility of mutual cooperation.
2.  **Subsequent Rounds ($1 < t < r$):** Let $S_{t-1}$ be the total number of cooperators in the previous round.
    *   If you played C in $t-1$: Cooperate if $S_{t-1} \geq T$. Otherwise, Defect (D).
    *   If you played D in $t-1$: Cooperate if $S_{t-1} \geq T + 1$. Otherwise, Defect (D). (The extra increment is a "forgiveness penalty" to ensure opponents are committed to a high-cooperation equilibrium before resuming cooperation).

For the final round ($t = r$):

*   Always play **Defect (D)**. This is a dominant strategy in the final round because there is no future interaction to incentivize, and the marginal benefit of your own contribution is always less than 1 (since $k < n$).

**Logic and Edge Cases:**

*   **Defection Trap:** If your opponents defect, the total cooperation $S$ will fall below the threshold. Your strategy immediately switches to D, protecting your endowment from being wasted on a failing public project.
*   **Signaling:** By requiring a higher threshold ($T+1$) to resume cooperation after defecting, you avoid being exploited by "flickering" opponents who alternate D/C to harvest the public good.
*   **End-Game:** The hardcoded defection in the final round prevents exploitation by altruistic opponents who might otherwise cooperate until the end.
'''

description_SELFISH_15 = '''
**Strategy: Conditional Defection with Forgiveness**

This strategy operates on the principle of Tit-for-Tat conditioned on the group's aggregate contribution, weighted by a threshold of reciprocation required to sustain cooperation.

**Parameters**
- `Threshold_T`: The minimum number of other players (out of `n-1`) required to cooperate in the previous round for you to cooperate in the current round. 
- Set `Threshold_T` = `ceil(n / k)`. This ensures that if at least this number of players cooperate, your contribution is break-even or profitable.

**Pseudocode**

```
// Round 1
Action = Defect

// Rounds 2 to r-1
If (Round_t-1_Cooperators >= Threshold_T) Then:
    Action = Cooperate
Else:
    Action = Defect

// Round r (The Final Round)
Action = Defect
```

**Decision Rules and Logic**

1.  **Initial Move (Round 1):** Always Defect. Because the game is anonymous and you have no information about the opponents, you must protect your endowment against potential unconditional defectors.
2.  **Adaptive Phase (Rounds 2 to r-1):** 
    *   Calculate the profitability threshold. By setting the threshold at `ceil(n/k)`, you ensure you only contribute when the group's collective action is sufficient to return value equal to or greater than your private endowment (1). 
    *   If the aggregate cooperation in the previous round meets or exceeds this threshold, you "reward" the group by cooperating. 
    *   If the group fails to meet the threshold, you Defect to avoid subsidizing non-contributors.
3.  **Final Round (Round r):** Always Defect. In the final round, there is no future utility to be gained from signaling cooperation or maintaining a reputation. Because the game ends, the incentive to defect is maximized to capture the private endowment without the risk of future retaliation or the need to sustain a public good.

**Handling Aggregate Observation**
Since the feedback is the aggregate number of cooperators (`Σc_j`):
- If you played C in `Round_t-1`: The number of *other* players who cooperated is `(Aggregate_Cooperators - 1)`.
- If you played D in `Round_t-1`: The number of *other* players who cooperated is `Aggregate_Cooperators`.
- Adjust the `Threshold_T` check accordingly to ensure the decision logic is based strictly on the behavior of the *opponents*.
'''

description_SELFISH_16 = '''
Adopt a "Tit-for-Tat with Forgiveness" strategy, optimized for selfish maximization by leveraging the aggregate contribution signal.

**Initialization:**
Play `C` in round 1.

**Subsequent Rounds (2 to r-1):**
Observe the total number of cooperators from the previous round, $S_{t-1}$.
Define the contribution threshold $T = \lceil n/k \rceil$.
Let $C_{prev}$ be your action in the previous round ($1$ if cooperated, $0$ if defected).
Calculate the total cooperation by others, $S_{others} = S_{t-1} - C_{prev}$.

Decision rule:
1. If $S_{others} \ge (T - 1)$: Play `C`.
2. If $S_{others} < (T - 1)$: Play `D`.

*Exception:* If the strategy previously defected due to a low $S_{others}$ count, but the current round's cooperation threshold is met despite your defection, "forgive" the defectors by playing `C` in the next round to test if cooperation can be sustained.

**Final Round ($t = r$):**
Play `D`. 

**Rationale for Edge Cases:**
- The threshold $T = \lceil n/k \rceil$ represents the minimum number of cooperators required for cooperation to yield a return greater than or equal to defecting.
- In the final round, there is no future incentive for reciprocity; therefore, unconditional defection is the dominant selfish strategy to maximize the terminal payoff.
- The forgiveness mechanism prevents the system from getting trapped in a cycle of mutual defection if opponents are playing a similar reactive strategy.
'''

description_SELFISH_17 = '''
Strategy: Tit-for-Tat with Conditional Forgiveness and Terminal Defection

The strategy operates on a round-by-round basis, tracking the total number of cooperators from the previous round, denoted as $C_{t-1}$. 

Decision Logic:

1.  Round 1: Play C.
2.  Last Round ($t = r$): Play D.
3.  Intermediate Rounds ($1 < t < r$):
    - If $C_{t-1} \ge \lfloor (n-1) \cdot \frac{1}{k} \rfloor + 1$, Play C.
    - Otherwise, Play D.

Variable Definition:
- $n$: total players.
- $k$: multiplication factor.
- $C_{t-1}$: the total number of players who contributed (cooperated) in the previous round.
- $\lfloor \cdot \rfloor$: the floor function, rounding down to the nearest integer.

The threshold calculation $\lfloor (n-1) \cdot \frac{1}{k} \rfloor + 1$ determines the minimum number of cooperators required in the previous round to make cooperation profitable for the player in the current round, assuming opponents replicate their previous behavior. If the collective cooperation level is insufficient to yield a net benefit (where individual payoff exceeds the defect payoff), the strategy shifts to D to avoid exploitation. This approach is aggressively selfish: it cooperates only when the public goods return justifies the contribution cost, defects unilaterally in the final round to capture the last-mover advantage, and punishes non-cooperative pools immediately.
'''

description_SELFISH_18 = '''
### Strategy Definition: Threshold-Based Conditional Cooperation

**Objective:** Maximize cumulative payoff over $r$ rounds by incentivizing mutual cooperation while defecting when cooperation is clearly unprofitable or nearing the game's end.

**State Variables:**
- $t$: Current round index ($1$ to $r$).
- $S_{t-1}$: Number of cooperators observed in the previous round.
- $N_{opp}$: Number of other players ($n - 1$).

**Decision Logic:**

1. **Initial Round ($t = 1$):**
   - Play **Cooperate (C)**. This signals a willingness to cooperate, establishing the potential for a high-payoff reciprocal equilibrium.

2. **Terminal Rounds ($t > r - \text{buffer}$):**
   - If $k < n/2$, set the buffer to 1 round (the final round).
   - If $k \ge n/2$, set the buffer to 2 rounds.
   - For all rounds within the buffer, play **Defect (D)**. Regardless of prior cooperation, the incentive to free-ride outweighs any future reciprocity benefits, and mutual cooperation will inevitably collapse.

3. **Intermediate Rounds ($1 < t \le r - \text{buffer}$):**
   - Define the Cooperation Threshold ($T$): $T = n/k$. This is the minimum number of total cooperators required for the public good return $(k/n \times T)$ to equal or exceed the cost of contributing (1).
   - If $S_{t-1} \ge T$, play **Cooperate (C)**.
   - If $S_{t-1} < T$, play **Defect (D)**.

**Adaptive Refinement (The Forgiveness/Re-entry Rule):**
If the previous round resulted in total defection ($S_{t-1} = 0$), treat the next round as a "probe" round:
- With probability $p = 0.1$, play **Cooperate (C)** to test if other players are willing to resume cooperation.
- Otherwise, play **Defect (D)**.

**Pseudocode:**
```python
def decide_action(t, r, n, k, S_prev):
    # Terminal phase check
    buffer = 1 if (k < n / 2) else 2
    if t > (r - buffer):
        return 'D'
    
    # First round initialization
    if t == 1:
        return 'C'
    
    # Cooperation threshold logic
    threshold = ceil(n / k)
    if S_prev >= threshold:
        return 'C'
    
    # If previous round failed, try to restart occasionally
    if S_prev == 0 and random() < 0.1:
        return 'C'
        
    return 'D'
```
'''

description_SELFISH_19 = '''
In round *t = 1*, play *D*.

For all subsequent rounds *t ∈ {2, ..., r-1}*, maintain a belief state regarding the average contribution behavior of the opponent pool. Let *S_{t-1}* be the total number of cooperators observed in the previous round. If *S_{t-1} / (n-1) > 1/k*, play *C*. Otherwise, play *D*.

For the final round *t = r*, play *D* regardless of historical outcomes.

If *S_{t-1} / (n-1) ≤ 1/k* for three consecutive rounds, set the strategy to permanent defection (*D*) for all remaining rounds, as this indicates that the aggregate contribution level is insufficient to yield a positive net utility relative to a defection-only baseline.

In all rounds where the contribution threshold is met, the decision logic is:
*   Calculate *Expected_Gain_from_Cooperation = (k/n) - 1*.
*   If *Expected_Gain_from_Cooperation > 0* (which contradicts the game parameters *k < n*), play *C*.
*   Since *k < n*, the dominant strategy for a purely selfish actor is *D*. However, to maximize payoff against adaptive opponents who reward cooperation, cooperate only if the observed density of cooperators in the previous round suggests that the collective benefit of *C* sustains a "cooperative equilibrium" where the probability of future reciprocity outweighs the immediate loss of *1* unit. If *S_{t-1} < (n/k) * threshold_factor* (where threshold_factor is set to 1.1), defect to prevent exploitation.
'''

description_SELFISH_20 = '''
The strategy follows a conditional cooperation framework designed to incentivize group contribution while protecting against exploitation, defaulting to defection in terminal phases to maximize individual payoff.

**Core Decision Logic**

Define $C_t$ as the number of cooperators observed in round $t$ and $N$ as the total number of players.

1.  **Round 1:** Play **Defect**. Establishing a baseline of selfishness prevents early-game exploitation and sets a low-trust threshold, forcing the group to demonstrate cooperative value before investment.

2.  **Rounds 2 through $r-1$:**
    *   **Monitor Cooperation:** Calculate the "Cooperation Threshold" $T = n/k$. 
    *   **Decision Rule:** 
        *   If the previous round's total cooperators $C_{t-1} \geq T$, play **Cooperate**.
        *   If the previous round's total cooperators $C_{t-1} < T$, play **Defect**.
    *   *Rationale:* This rule ensures that cooperation is only engaged when the collective return exceeds the private benefit of defecting. If the group is insufficient to provide a positive marginal return on your contribution, you must defect to maintain your payoff relative to the group.

3.  **Final Round ($r$):** Play **Defect**. Since there are no future rounds to influence or leverage, there is no strategic value in cooperating. Defecting in the final round captures the maximum possible private endowment without penalty.

**Pseudocode**

```python
# Constants: n, k, r are fixed
threshold = n / k 

def get_action(round_number, prev_round_cooperators):
    if round_number == 1:
        return "Defect"
    
    if round_number == r:
        return "Defect"
        
    if prev_round_cooperators >= threshold:
        return "Cooperate"
    else:
        return "Defect"
```

**Edge Case Handling**
*   **Insufficient Threshold:** If $k \leq 1$, the threshold $T = n/k \geq n$. Since the maximum number of cooperators is $n$, and you are one of them, the threshold will never be met. In this case, the strategy defaults to **Defect** for all rounds, as cooperation is strictly dominated.
*   **Total Defection:** If the system detects a pattern of total defection ($C_{t-1} = 0$), the strategy maintains **Defect** to avoid subsidizing a non-productive collective.
'''

description_SELFISH_21 = '''
At the start of the game (Round 1), play Cooperate (C) to establish a baseline for cooperation among opponents.

In subsequent rounds (Round 2 to Round $r-1$), base the decision to cooperate on the observed behavior of the group in the previous round:

1. Let $C_{t-1}$ be the number of cooperators observed in the previous round.
2. Calculate the "Cooperation Threshold" $T$ required to make cooperation break-even relative to defecting. Since playing C yields a payoff of $(k/n) \times C_{total}$ and playing D yields a payoff of $1 + (k/n) \times (C_{total}-1)$, the marginal benefit of contributing is $(k/n)$. If $k/n < 1$ (which is always true given $k < n$), playing D is strictly dominant in a one-shot sense. Therefore, the goal is to trigger reciprocal cooperation rather than optimize single-round payoffs.
3. If $C_{t-1} \geq \lceil n/k \rceil$, play Cooperate (C). This target threshold assumes that for cooperation to be rational, a sufficient mass of players must participate to provide a return better than the individual defect incentive.
4. If $C_{t-1} < \lceil n/k \rceil$, play Defect (D). This punishes the group for failing to maintain a sustainable cooperative equilibrium.

For the final round (Round $r$), always play Defect (D), regardless of previous history. Because there are no future rounds to influence, the incentive to maintain a cooperative reputation or trigger reciprocity vanishes, making Defect the optimal selfish choice.

Pseudocode:

```python
# Strategy for round t
if t == 1:
    return C
if t == r:
    return D

# Determine threshold for reciprocity based on parameters
# If k/n * C_total >= 1, cooperation is net positive for the group
# We use a greedy threshold to maintain self-interest
threshold = ceil(n / k)

if last_round_cooperators >= threshold:
    return C
else:
    return D
```
'''

description_SELFISH_22 = '''
Implement a "Conditional Tit-for-Tat with Defection-First Terminality" strategy based on the observed public good contribution levels.

**Decision Rules:**

1. **Initialization:** In Round 1, play **D** (Defect). Since the game is finite and players are assumed selfish, beginning with cooperation is an uncompensated risk.

2. **Transition and Adaptation:** For any Round $t$ (where $1 < t < r$):
   - Calculate $S_{t-1}$, the number of cooperators in the previous round.
   - If $S_{t-1} > 0$ and the number of cooperators has increased or remained stable compared to $S_{t-2}$, play **C** (Cooperate). This acts as a conditional incentive to sustain cooperation.
   - If $S_{t-1} = 0$, or if $S_{t-1} < S_{t-2}$, play **D** (Defect). This punishes free-riding or the collapse of the cooperative equilibrium.

3. **Terminality:** In the final Round $r$, always play **D** (Defect). Because there are no future rounds to influence, there is no strategic benefit to cooperation, and defecting yields a strictly higher payoff regardless of others' actions.

**Pseudocode:**

```python
# Variables:
# r = total rounds
# n = total players
# history = list of total cooperators in each round [S_1, S_2, ..., S_t-1]

def choose_action(round_t, history):
    # Rule 1: Always defect in the final round
    if round_t == r:
        return 'D'
    
    # Rule 2: First round defection
    if round_t == 1:
        return 'D'
        
    # Rule 3: Adaptation
    last_S = history[-1]
    prev_S = history[-2] if len(history) > 1 else 0
    
    # If last round was a failure to cooperate, punish
    if last_S == 0:
        return 'D'
    
    # If cooperation is sustained or growing, cooperate to maintain the incentive
    if last_S >= prev_S:
        return 'C'
    
    # Otherwise, defect
    return 'D'
```
'''

description_SELFISH_23 = '''
Initialize `reputation_score = 0.0`. 
Define `threshold = 0.5` (the critical fraction of cooperators required to make cooperation individually profitable).
Define `cooperation_history` as an empty list to store the total number of cooperators observed in each round.

**Round 1:**
Defect.

**Rounds 2 to r-1:**
Calculate the current `reputation_score` based on the moving average of the fraction of cooperators in previous rounds:
`avg_cooperators = sum(cooperation_history) / (n * len(cooperation_history))`

If `avg_cooperators >= threshold` and the previous round's cooperation count was high enough to justify the contribution, cooperate. 
Otherwise, defect. 

Specifically, evaluate the decision using the following logic:
1. Identify the break-even point where cooperating provides at least as much utility as defecting: `(k/n) * (S + 1) >= 1 + (k/n) * S`, which simplifies to `k/n >= 1`. Since the problem constraints define `1 < k < n`, cooperation is socially beneficial but individually unprofitable unless the reciprocity threshold is met.
2. If `avg_cooperators > (n/k - 1)`:
   Cooperate.
3. Else:
   Defect.

Update `cooperation_history` after observing the result of each round.

**Round r (Final Round):**
Defect.

**Edge Cases:**
*   If `k/n <= 0.5` (or any condition where the private gain from defecting consistently outweighs the public return), default to permanent defection regardless of history.
*   If the aggregate observation of `cooperation_history` drops below the `threshold` for three consecutive rounds, reset `reputation_score` to 0 and switch to permanent defection for the remainder of the game to prevent exploitation.
'''

description_SELFISH_24 = '''
### Strategy: Conditional Reciprocal Defection

**Core Philosophy:**
The strategy is strictly selfish, aiming to maximize cumulative payoff by maintaining cooperation only when it incentivizes others to contribute more than the marginal cost of contribution. When the public good returns are insufficient to justify cooperation, or when opponents demonstrate a preference for defection, the strategy switches to permanent defection to avoid exploitation.

**Decision Rules:**

1.  **First Round (t=1):**
    *   Cooperate if $(k/n) \times n \ge 1$ (the theoretical maximum possible return exceeds the cost of contribution).
    *   Otherwise, Defect.

2.  **Subsequent Rounds (t > 1):**
    *   Let $S_{t-1}$ be the total number of cooperators observed in the previous round.
    *   Let $C_{self}$ be your own action in the previous round.
    *   Calculate the *Net Marginal Benefit* ($NMB$) of cooperation: $NMB = (k/n) \times (S_{t-1} - C_{self}) + (k/n) - 1$.
        *   This represents the gain from the additional contribution to the public good minus the cost of the contribution itself.
    *   **If $NMB > 0$:** Cooperate. (This indicates that the collective cooperation level, excluding your own impact, is sufficient to make your contribution profitable).
    *   **If $NMB \le 0$:** Defect. (This indicates that the public good is being under-provided, and contributing further would result in a net loss or zero gain relative to defecting).

3.  **Last Round (t = r):**
    *   Always Defect, regardless of history. Since there is no future interaction to influence, the dominant strategy is to capture the private endowment without contributing to the public pool.

**Edge Cases & Logic Flow:**

*   **Initial Trust:** The strategy begins with a "trust but verify" stance. If the system parameters $k$ and $n$ are set such that even full cooperation is unprofitable ($k < 1$, though excluded by parameters), it defaults to Defect immediately.
*   **Punishment/Reward:** By relying on $S_{t-1}$, the strategy effectively punishes the group for low cooperation by switching to Defection, and rewards the group for high cooperation by maintaining support.
*   **Adaptation:** This strategy does not track individual opponents but reacts to the aggregate population signal. If the population contribution $S_{t-1}$ drops, $NMB$ will likely fall below 0, triggering an immediate shift to Defection until the population signal improves.

**Pseudocode:**

```python
def choose_action(round_t, total_rounds, k, n, last_round_cooperators, my_last_action):
    # Rule for final round (dominant strategy)
    if round_t == total_rounds:
        return 'D'
    
    # Rule for first round
    if round_t == 1:
        if (k / n) * n >= 1:
            return 'C'
        else:
            return 'D'
            
    # Rule for all other rounds
    # my_contribution is 1 if my_last_action was 'C', else 0
    my_contribution = 1 if my_last_action == 'C' else 0
    
    # Calculate net marginal benefit of contributing
    # (k/n) * (total_cooperators_excluding_me) + (k/n) - 1
    # total_cooperators_excluding_me = last_round_cooperators - my_contribution
    others_coop = last_round_cooperators - my_contribution
    nmb = (k / n) * (others_coop + 1) - 1
    
    if nmb > 0:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFISH_25 = '''
In Round 1, play Defect (D).

For Rounds 2 through $r-1$, track the number of cooperators from the previous round, denoted $C_{prev}$. Calculate the cooperation threshold $T = n/k$. 

If $C_{prev} \geq T$, play Cooperate (C) with probability $p$, where $p$ is scaled by the consistency of the group: if the observed number of cooperators has been increasing or stable at or above $T$ for the last two rounds, set $p = 1$; otherwise, set $p = (C_{prev} - T) / (n - T)$. If $C_{prev} < T$, play Defect (D).

In the final round $r$, play Defect (D) regardless of history.

If at any point the total group payoff (inferred from the number of cooperators) drops significantly below the expected return of a fully defecting group (i.e., if $C_{prev} < n/k$), immediately switch to Defect (D) for all subsequent rounds until $r-1$.
'''

description_SELFISH_26 = '''
In Round 1, play Defect (D).

In subsequent rounds (t > 1), evaluate the previous round's outcome. Let $C_{prev}$ be the total number of cooperators from the previous round (including yourself if you cooperated). Your decision for the current round depends on the observed performance of the group as a whole.

For any round $t < r$:
1. If $C_{prev} = 0$, continue to play D.
2. If $C_{prev} > 0$, calculate the "Threshold of Advantage" ($T$). The payoff for cooperating is $(k/n) \times C_{total}$. The payoff for defecting is $1 + (k/n) \times (C_{total} - 1)$. Cooperating is only strictly better than defecting if the collective contribution is sufficient to overcome the individual loss of the endowment. Specifically, cooperation becomes individually rational only if $k \times (C_{prev}/n) > 1 + k \times ((C_{prev}-1)/n)$, which simplifies to $k/n > 1$. Since $k < n$ by game parameters, this condition is never met. Therefore, cooperation is never individually rational in a one-shot sense.

3. To maintain a selfish strategy that encourages others to contribute, implement a "Win-Stay, Lose-Shift" variant based on total contributions:
   - Calculate your previous payoff $\pi_{i, t-1}$.
   - If $\pi_{i, t-1}$ was greater than the payoff of an all-defector outcome (which is 1), evaluate the trend. If the total number of cooperators ($C_{prev}$) is increasing, play Cooperate (C) to signal potential for higher collective gain, provided your payoff remains at least 1.
   - If $\pi_{i, t-1} < 1$, play Defect (D) to punish the lack of collective coordination.

4. In the final round ($t = r$), always play Defect (D). Regardless of past cooperation, there is no future round to influence or gain from, so defecting is the dominant strategy to maximize the final period payoff.

Pseudocode:
```
if t == r:
    return D

if t == 1:
    return D

if C_prev == 0:
    return D

// Check if group cooperation is trending or stable enough to be profitable
// relative to a baseline of zero cooperation
expected_cooperation_gain = (k * C_prev) / n
if expected_cooperation_gain > 1:
    return C
else:
    return D
```
'''

description_SELFISH_27 = '''
### Strategy: Adaptive Conditional Defection

**State Variable Tracking**
Maintain a history of the round number $t$ and the total number of cooperators observed in the previous round $C_{t-1}$. 

**Decision Rules**

1. **Round 1 (Initialization):**
   Defect ($D$). Starting with defection establishes a baseline to assess the cooperative propensity of the group without risking personal endowment.

2. **Rounds $2$ through $r-1$ (Adaptive Phase):**
   Use a "Conditional Reciprocity" logic defined by the threshold $T = n / k$.

   *   **If $C_{t-1} \ge T$:** Cooperate ($C$).
       If the group's cooperation level generates a return on contribution greater than or equal to the opportunity cost of not defecting (the private payoff of 1), participate to sustain the public good.
   
   *   **If $C_{t-1} < T$:** Defect ($D$).
       If the group's contribution level fails to provide a profitable return relative to private retention, defect to minimize losses.

3. **Round $r$ (Final Round):**
   Defect ($D$).
   Since there is no future round to incentivize reciprocity or punish defections, maximizing the private payoff is the dominant strategy regardless of previous history.

**Edge Case Handling**
*   **Total Defection by Group:** If $C_{t-1} = 0$, proceed to $D$.
*   **Total Cooperation by Group:** If $C_{t-1} = n$, proceed to $C$ (unless it is the final round).
*   **Calculation Logic:** Always treat $T$ as the ceiling of $n/k$. If $k$ is such that $n/k$ is not an integer, round up to the nearest integer to ensure the return on contribution strictly meets or exceeds the private payoff of 1.

**Pseudocode**
```python
if round == r:
    return D
if round == 1:
    return D

threshold = ceil(n / k)
if last_round_cooperators >= threshold:
    return C
else:
    return D
```
'''

description_SELFISH_28 = '''
**Initial Round:**
Play Cooperate (C) to establish the potential for mutual cooperation.

**Intermediate Rounds (2 ≤ t < r):**
Let $c_{t-1}$ be the number of cooperators observed in the previous round, and $S_{t-1}$ be the strategy used in the previous round (1 if C, 0 if D).

The strategy follows a conditional cooperation rule based on the threshold $T = n/k$. This threshold represents the break-even point where contributing is neutral compared to free-riding, given the expected contribution of others.

1.  If $c_{t-1} \ge T$, play C.
2.  If $c_{t-1} < T$, play D.

*Exception for Punitive Reset:* If the strategy played D in the previous round ($S_{t-1} = 0$), it monitors the response of the group. If the group's cooperation level $c_{t-1}$ increases by more than 20% compared to the round where the strategy first switched to D, or if $c_{t-1}$ meets the threshold $T$ again, resume playing C. Otherwise, continue playing D.

**Final Round (t = r):**
Play Defect (D). Since there are no future rounds to incentivize, maintaining cooperation provides no strategic value.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, last_cooperators, last_action, n, k):
    threshold = n / k
    
    # Final round defect
    if round_number == total_rounds:
        return 'D'
    
    # First round cooperate
    if round_number == 1:
        return 'C'
        
    # Conditional cooperation based on threshold
    if last_cooperators >= threshold:
        return 'C'
    
    # If the group fails to meet threshold, defect
    # Stay defecting until group behavior improves significantly
    if last_action == 'D':
        # Logic to test if others started contributing again
        if last_cooperators >= threshold:
            return 'C'
        return 'D'
        
    return 'D'
```
'''

description_SELFISH_29 = '''
The strategy operates on a conditional "Tit-for-Tat" variant adjusted for public goods thresholds, designed to maximize individual payoff while leveraging the potential for mutual cooperation.

**Decision Rules:**

Define the *cooperation threshold* $T$ as $T = \lceil n/k \rceil$. This is the minimum number of contributors required for cooperation to yield a payoff greater than or equal to defection. 

1.  **First Round:** Play **Cooperate (C)**. This serves as an initial probe to test the cooperative inclination of the group.

2.  **Subsequent Rounds (t > 1 and t < r):**
    *   If the previous round's total cooperation count ($S_{t-1}$) was $\ge T$: Play **Cooperate (C)**.
    *   If the previous round's total cooperation count ($S_{t-1}$) was $< T$: Play **Defect (D)**.

3.  **Final Round (t = r):** Play **Defect (D)**. Regardless of previous outcomes, the lack of future rounds eliminates the incentive to maintain the cooperative equilibrium.

**Refinement for Adaptive Defection:**

If $S_{t-1} < T - 1$, effectively signaling that even if you had cooperated, the group would still have failed to reach the threshold, enforce an additional penalty round of **Defect (D)** regardless of the next round's outcome, unless the group achieves a majority contribution of $S > n/2$, in which case reset to the primary logic.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, last_round_cooperators, n, k):
    threshold = ceil(n / k)
    
    # Final round: always defect
    if round_number == total_rounds:
        return D
        
    # First round: always cooperate
    if round_number == 1:
        return C
        
    # Default logic: conditional cooperation
    if last_round_cooperators >= threshold:
        return C
    else:
        return D
```
'''

description_SELFISH_30 = '''
The strategy follows a conditional, threshold-based logic designed to maximize individual payoff by reciprocating cooperation while immediately punishing defection. 

**Decision Logic**

1. **Round 1:** Play D (Defect). This establishes a baseline and prevents exploitation in the event that the population is dominated by defectors.

2. **Rounds 2 to r-1:** Calculate the "Contribution Threshold" (T). Cooperate only if the expected marginal benefit of the group's cooperation outweighs the cost of personal contribution.
   
   Define $S_{t-1}$ as the total number of cooperators in the previous round.
   Define $C_{t-1}$ as your own action in the previous round ($C=1, D=0$).
   Define $O_{t-1} = S_{t-1} - C_{t-1}$ as the number of opponents who cooperated.

   *   If $O_{t-1} \ge \frac{n}{k}$: Cooperate (C).
   *   Else: Defect (D).

   This rule ensures cooperation only when the collective behavior is sufficient to make the public good return greater than or equal to the cost of contribution (1).

3. **Round r (The Last Round):** Always play D (Defect). Since there are no future rounds to influence, future reputation is irrelevant. Defecting secures the maximum possible payoff given the current round’s contribution levels.

**Pseudocode**

```
Strategy(round, n, k, history):
    if round == 1:
        return D
    
    if round == r:
        return D
    
    // Retrieve previous round's outcome
    total_cooperators_prev = history.last_round_total_cooperators
    my_action_prev = history.last_round_my_action
    opponents_cooperated = total_cooperators_prev - (1 if my_action_prev == C else 0)
    
    // Threshold calculation
    // Condition derived from: (k/n) * (opponents_cooperated + 1) >= 1
    threshold = n / k
    
    if opponents_cooperated >= threshold:
        return C
    else:
        return D
```
'''

description_SELFISH_31 = '''
**Strategy Definition: Conditional Tit-for-Tat with Defection Threshold (CTFT-DT)**

This strategy operates on the logic of conditional cooperation to maximize total payoffs while strictly defaulting to defection in the final round and when aggregate cooperation drops below a critical sustainability threshold.

**Decision Rules**

In any given round $t$ where $t < r$:

1.  **Calculate Sustainability Threshold ($S$):**
    Determine the minimum number of cooperators required for cooperation to be individually profitable compared to defecting alone. Cooperation is profitable only if the benefit of the group contribution outweighs the cost of the individual contribution. This occurs when:
    $(k/n) \times (\text{Cooperators} + 1) \ge 1$.
    Solving for cooperators: $\text{Cooperators} \ge (n/k) - 1$.
    Let $S = \lceil n/k - 1 \rceil$. This is the minimum number of other players who must cooperate for cooperation to be rational.

2.  **Evaluate History:**
    Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   **Round 1:** Play **Defect (D)**. (Because there is no history to enforce, and the game is strictly competitive, starting with defection avoids exploitation by cooperative-agnostic or parasitic strategies).
    *   **Round $t > 1$:**
        *   If $C_{t-1} \ge S + 1$: Play **Cooperate (C)**. (If the threshold was met in the previous round, assume the population is currently maintaining a cooperative equilibrium and contribute to sustain it).
        *   If $C_{t-1} < S + 1$: Play **Defect (D)**. (If the previous round failed to meet the sustainability threshold, punish the deviation by withholding contribution).

**Edge Cases**

1.  **Last Round ($t = r$):**
    Always play **Defect (D)** regardless of history or parameter values. Since there are no subsequent rounds to sustain cooperative norms or trigger future punishment, the dominant strategy is to capture the private endowment while free-riding on any remaining cooperative contributions.

2.  **Uncertainty/No History:**
    If $C_{t-1}$ data is ever ambiguous (not applicable per prompt but included for robustness), default to **Defect (D)**.

3.  **Threshold Logic:**
    If $S \ge n$, the game is fundamentally non-cooperative because the required contributions to break even are impossible to achieve; in this scenario, play **Defect (D)** in all rounds.
'''

description_SELFISH_32 = '''
**Initial Round (t=1):**
Cooperate if $k/n > 0.5$. Otherwise, defect.

**Subsequent Rounds (1 < t < r):**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
1. If $C_{t-1} = n$, cooperate.
2. If $n > C_{t-1} \ge \lceil n/k \rceil$, cooperate to sustain a cooperative equilibrium.
3. If $C_{t-1} < \lceil n/k \rceil$, defect.
4. If the history shows a repeated pattern of opponent defection (defined as $C_{t-1} < \lceil n/k \rceil$ for two consecutive rounds), maintain defection regardless of other signals.

**Final Round (t=r):**
Defect.

**Edge Case Definitions:**
- If the strategy was defecting and the observation $C_{t-1}$ suddenly rises above $\lceil n/k \rceil$, test for cooperation by playing C in round $t$. If $C_t$ drops below $\lceil n/k \rceil$ in the following round, revert to permanent defection for the remainder of the game.
- If $k/n \le 1/n$ (the marginal benefit of cooperation is less than the cost of contribution), defect in all rounds.
'''

description_SELFINTERESTED_5 = '''
The strategy, titled "Conditional Reciprocity with Retaliatory Deterrence," functions as a tit-for-tat variant adapted for the anonymity constraints of an N-player setting. It employs a "cooperation threshold" to punish free-riders while incentivizing collective contribution.

**Decision Rules:**

1.  **First Round:** Play **Cooperate (C)**. This establishes a baseline and tests for the presence of other reciprocators.
2.  **Subsequent Rounds (t > 1):** Calculate the previous round’s total cooperation count ($S_{t-1}$).
    *   Let $T$ be the threshold for cooperation, defined as $T = \lceil n / k \rceil$.
    *   **If $S_{t-1} \ge T$:** Play **Cooperate (C)**. This maintains the cooperative equilibrium when the returns on investment are net positive or neutral.
    *   **If $S_{t-1} < T$:** Play **Defect (D)**. This triggers a punishment phase to deter free-riding and minimize personal loss when the collective effort fails to provide sufficient returns.
3.  **Last Round (t = r):** Play **Defect (D)** regardless of history. Since the future shadow of the game vanishes, the dominant strategy is to capture the private endowment without incurring the cost of contribution.

**Pseudocode:**

```python
def decide_action(t, r, n, k, history):
    # Base case: Last round defection
    if t == r:
        return D
    
    # Base case: First round cooperation
    if t == 1:
        return C
    
    # Adaptive logic: Observe previous round total contributions (S)
    # Threshold T = ceil(n / k)
    threshold = ceil(n / k)
    previous_S = history.get_last_round_total_cooperators()
    
    if previous_S >= threshold:
        return C
    else:
        return D
```

**Edge Cases:**

*   **Tie-breaking (when $S_{t-1} = T$):** Explicitly prioritize cooperation. If the return on the public good exactly offsets the cost of contribution, cooperation is neutral but builds trust; therefore, maintain the cooperative stance.
*   **Persistent Defection:** If the system is stuck in a state where $S < T$ for multiple rounds, the strategy correctly identifies the Nash equilibrium of total defection and remains in Defect mode to avoid exploitation.
*   **Recovery:** If opponents switch to cooperation in round $t$ such that $S_t \ge T$, the strategy immediately resumes cooperation in round $t+1$, allowing for the re-establishment of cooperative equilibria if other agents are using similar adaptive logic.
'''

description_SELFINTERESTED_6 = '''
The strategy follows a conditional, tit-for-tat dynamic based on the observed cooperation rate, adjusted for the finite horizon of the game.

**Decision Logic:**

1.  **First Round:** Play **Cooperate** (C) to signal willingness to engage in mutually beneficial cooperation.

2.  **Subsequent Rounds (t < r):** 
    Let $S_{t-1}$ be the number of cooperators in the previous round.
    *   If $S_{t-1} \ge \tau \cdot n$, where $\tau = 1/k$, play **Cooperate**.
    *   If $S_{t-1} < \tau \cdot n$, play **Defect**.

    The threshold $\tau = 1/k$ represents the break-even point where the marginal benefit of contributing equals the marginal cost. If the cooperation level supports a positive return on investment, continue cooperating. If the cooperation level falls below this threshold, the strategy switches to defection to avoid exploitation.

3.  **Last Round (t = r):**
    Play **Defect**. In the final round, there is no future incentive for others to cooperate in response to your actions, removing the penalty for defecting.

**Refinement for Adaptation:**

To recover from unintentional or transient low-cooperation periods, the strategy employs a "probabilistic check":

```pseudocode
// Calculate cooperation threshold
threshold = n / k

// Decision function
If t == r:
    Return Defect
Else if t == 1:
    Return Cooperate
Else:
    // Determine the cooperation density observed in the last round
    previous_cooperators = observed_count_from_round_t_minus_1
    
    If previous_cooperators >= threshold:
        Return Cooperate
    Else:
        // Tit-for-tat reset logic: 
        // Occasionally test if cooperation is possible again 
        // if the population behavior shifts.
        If Random(0, 1) < 0.1: 
             Return Cooperate
        Else:
             Return Defect
```

**Edge Case Handling:**
*   **Minimal Cooperation:** If $k$ is such that $1/k$ is not an integer, the ceiling of the threshold is used to determine the minimum number of cooperators required to justify cooperation.
*   **Constant Defection:** If the strategy observes persistent defection (zero or near-zero cooperators) for more than two consecutive rounds, the "reset" mechanism (the 10% chance to cooperate) is disabled for the remainder of the game to prevent continuous exploitation.
'''

description_SELFINTERESTED_7 = '''
The strategy follows a conditional, history-dependent tit-for-tat mechanism designed to induce cooperation while minimizing exploitation in the final rounds.

**Initial Round (t=1):**
Cooperate (C). This establishes a cooperative baseline to incentivize reciprocal behavior from other players.

**Subsequent Rounds (t > 1 and t < r):**
Let $C_{t-1}$ be the number of players who cooperated in the previous round.
Let $T_{t-1}$ be the total number of contributors observed in the previous round (including the self).

1.  **Calculate the Threshold for Net Gain ($T_{threshold}$):**
    A contribution is individually rational if the marginal return from the public good exceeds the marginal cost of contribution (1).
    $\frac{k}{n} \times T \geq 1 \Rightarrow T \geq \frac{n}{k}$
    Define $T_{threshold} = \lceil \frac{n}{k} \rceil$.

2.  **Evaluate Opponent Cooperation:**
    If the number of other players who cooperated in the previous round ($C_{t-1} - c_{t-1}$) was $\geq (T_{threshold} - 1)$, play C. This indicates sufficient group cooperation to justify a contribution.

    Otherwise, play D. This serves as a penalty phase to discourage defection.

3.  **Correction (The "Forgiveness" Trigger):**
    If the strategy defected in the previous round ($t-1$) but the *total* number of cooperators in that round was $\geq T_{threshold}$, switch back to C. This mechanism allows the strategy to restart cooperation if the group is inherently cooperative but the strategy's own defection lowered the count below the threshold.

**Final Round (t = r):**
Defect (D). Since there are no future rounds to sustain a cooperative equilibrium, the incentive to defect is absolute. This maximizes the payoff in the final period by capturing the private endowment while still benefiting from any residual cooperation from other agents.

**Edge Case Handling:**
- If $T_{threshold} > n$, the game is fundamentally non-cooperative (the cost of contributing always outweighs the benefit). In this specific scenario, defect (D) in every round.
- If the calculation $\lceil \frac{n}{k} \rceil$ results in a requirement where even $n$ cooperators do not produce a return of 1, revert to unconditional Defection (D) immediately.
'''

description_SELFINTERESTED_8 = '''
Strategy: Conditional Tit-for-Tat with Defection Threshold (CTFT-DT)

Decision Rules:

1. Initial Round (t=1): Always Cooperate (C).

2. Subsequent Rounds (t > 1):
   Let $C_{total, t-1}$ be the number of cooperators observed in the previous round.
   Let $k$ be the multiplication factor and $n$ be the number of players.
   
   Calculate the "Breakeven Threshold" ($T_{threshold}$):
   The payoff for cooperating is $(k/n) \times C_{total}$.
   The payoff for defecting is $1 + (k/n) \times (C_{total} - 1)$.
   Cooperating is strictly better or equal when $(k/n) \times C_{total} \geq 1 + (k/n) \times (C_{total} - 1)$.
   Simplifying, cooperation is rational if:
   $C_{total} \geq n/k$.
   
   Set $T_{threshold} = \lceil n/k \rceil$.

   Action logic:
   - If $t = r$ (Last Round): Defect (D). Self-interest dictates maximizing immediate payoff without future consequences.
   - If $t < r$:
     - If $C_{total, t-1} \geq T_{threshold}$: Cooperate (C). This maintains the public good and signals cooperative intent.
     - If $C_{total, t-1} < T_{threshold}$: Defect (D). This punishes non-cooperative groups where individual contribution is net-loss and protects against exploitation.

3. Recovery Logic (Grim Trigger Sensitivity):
   If the strategy defected in round $t-1$ because $C_{total, t-2} < T_{threshold}$, check the outcome of round $t-1$.
   - If the group returns to $C_{total, t-1} \geq T_{threshold}$, resume cooperation in round $t$.
   - If the group remains below $T_{threshold}$, maintain defection.
'''

description_SELFINTERESTED_9 = '''
The strategy utilizes a conditional-cooperation mechanism, specifically a Tit-for-Tat variant adapted for N-player dynamics, designed to incentivize mutual cooperation while minimizing exploitation.

### Decision Rules

1. **Round 1 (Initialization):**
   - Play **Cooperate (C)**. This tests for the existence of cooperative partners in the group without immediately defecting.

2. **Rounds 2 through (r - 1):**
   - Let $C_{t-1}$ be the number of cooperators in the previous round.
   - Let $c_{self, t-1}$ be your own action in the previous round (1 for Cooperate, 0 for Defect).
   - Let $C_{others, t-1} = C_{t-1} - c_{self, t-1}$ be the number of other cooperators.
   - Calculate the "Cooperation Threshold" ($T$):
     $T = \frac{n-1}{k}$
   - **Decision Rule:**
     - If $C_{others, t-1} \ge T$: Play **Cooperate (C)**.
     - If $C_{others, t-1} < T$: Play **Defect (D)**.

3. **Round r (Terminal Round):**
   - Play **Defect (D)**. Because there is no future interaction, there is no reputational or reciprocal incentive to contribute. The subgame perfect Nash equilibrium for the final round is always defection, and cooperating would result in a strictly lower payoff regardless of others' actions.

### Logic and Adaptivity

The threshold $T = (n-1)/k$ represents the critical mass of other contributors required for your contribution to be marginally profitable or neutral. If $k$ cooperators exist, the group generates $k$ units of value. If you contribute, your cost is 1, and your share of the return is $k/n$. You break even or profit if $(k/n) \times (\text{others} + 1) \ge 1$, which simplifies to $C_{others} \ge (n/k) - 1$. The provided threshold $T$ serves as a cautious baseline for ongoing reciprocity.

If the number of other cooperators falls below the threshold, the strategy switches to Defect to protect against free-riders. If cooperators return to the group in subsequent rounds, the strategy can resume cooperation (if it were allowed to be "generous Tit-for-Tat"), but strictly sticking to the threshold ensures that you only subsidize the public good when there is a sufficient cooperative signal to warrant it.

### Pseudocode

```python
def decide_action(t, r, n, k, history):
    # Terminal round: always defect
    if t == r:
        return "D"
    
    # First round: attempt cooperation
    if t == 1:
        return "C"
        
    # Standard rounds: conditional cooperation
    previous_cooperators = history[t-1].C_total
    my_last_action = history[t-1].my_action
    others_cooperated = previous_cooperators - (1 if my_last_action == "C" else 0)
    
    threshold = (n / k) - 1
    
    if others_cooperated >= threshold:
        return "C"
    else:
        return "D"
```
'''

description_SELFINTERESTED_10 = '''
Start Round 1 by playing Cooperate (C).

For all subsequent rounds $t \in \{2, \dots, r\}$, track the total number of cooperators observed in the previous round ($C_{t-1}$). Calculate your decision using a Tit-for-Tat variant adjusted for the public goods environment, specifically focusing on the "average contribution" threshold.

Let $S_{t-1}$ be the number of cooperators in round $t-1$. Calculate the "cooperation intensity" of the group:
If $S_{t-1} \geq \lceil (n-1) \cdot \frac{1}{k} \rceil$, then play C.
Else, play Defect (D).

This threshold function ensures that you only cooperate if the group's cooperation level makes the marginal benefit of your contribution positive or neutral for the collective (relative to your private endowment). Specifically, when $S_{t-1}$ cooperators are present, the payoff for cooperating is $(k/n)(S_{t-1}+1)$ and for defecting is $1 + (k/n)S_{t-1}$. Cooperate if $(k/n)(S_{t-1}+1) \geq 1 + (k/n)S_{t-1}$, which simplifies to $k/n \geq 1 - (k/n)S_{t-1}$, or more simply, your decision is conditioned on the group sustaining enough cooperators to make the public good return profitable.

**Edge Cases:**
1. **Last Round ($t=r$):** Play Defect (D) regardless of history, as there is no future interaction to incentivize cooperation.
2. **First Round ($t=1$):** Play Cooperate (C) to signal willingness to participate in a cooperative equilibrium.
3. **Observation Anomaly:** If $S_{t-1}$ is ambiguous or data is missing, default to Defect (D) to protect your endowment.
4. **Punishment:** If the group fails to meet the threshold, play Defect (D) in the subsequent round to penalize non-cooperation and prevent exploitation. Return to Cooperate (C) only in round $t+1$ if the group cooperation level in round $t$ recovers to the threshold $\lceil (n-1) \cdot \frac{1}{k} \rceil$.
'''

description_SELFINTERESTED_11 = '''
**Decision Rules:**

Initialize the strategy with a *cooperation threshold* parameter, τ, set to 0.7.

**Round 1:** Play C.

**Rounds 2 to r-1:**
Let $S_{t-1}$ be the number of cooperators in the previous round, and let $C_{t-1}$ be the binary indicator of the player's own move in the previous round (1 for C, 0 for D).

1. If $S_{t-1} \ge \tau \cdot n$, play C.
2. If $S_{t-1} < \tau \cdot n$, transition to a punishment state for the current round:
   - If $C_{t-1} = 0$, play D.
   - If $C_{t-1} = 1$, play D with probability $p = 1 - \frac{S_{t-1}}{n}$, and play C with probability $1-p$.
   
*Punishment recovery:* If the strategy played D due to a low $S_{t-1}$ in the previous round, it will revert to playing C in the current round only if the average cooperation rate of the last two rounds exceeds $\tau \cdot n$. Otherwise, continue the conditional defection rule.

**Round r:** Play D.

**Edge Case Handling:**
- **Initial Observation:** If $S_1$ in the first round is below the threshold $\tau \cdot n$, immediately switch to D for all subsequent rounds, including the final round, to minimize losses against non-cooperative groups.
- **Threshold Adjustment:** If the group cooperation level $S$ oscillates near the threshold $\tau \cdot n$ for more than three rounds without stabilizing, adjust $\tau$ to be $\tau + 0.05$ to become more conservative.
- **Defector Dominance:** If $S_t = 0$ for any two consecutive rounds, set $\tau = 1.0$ (effectively playing D for all remaining rounds).
'''

description_SELFINTERESTED_12 = '''
**Strategy: Conditional Reciprocity with Retaliation and Defection Thresholds**

**Decision Logic**

The strategy maintains a state variable $S_t$ representing the observed cooperation level of the group in the previous round, where $S_t = \frac{\text{Total Cooperators in round } t}{n}$.

*   **Round 1:** Play **Cooperate (C)**. Establish initial trust to incentivize conditional cooperators.

*   **Rounds 2 to $r-1$:**
    *   Calculate the "breakeven" cooperation threshold $\theta = \frac{n}{k}$. 
    *   If $S_{t-1} \geq \theta$: Play **Cooperate (C)**. This maintains the public good when contributions are high enough to yield a net gain or near-parity.
    *   If $S_{t-1} < \theta$: Play **Defect (D)**. This punishes defection and minimizes individual loss when the public good is undersupplied.

*   **Round $r$ (Final Round):** Play **Defect (D)** regardless of history. There is no future round to punish or incentivize, and the dominant strategy in the final round of a finitely repeated prisoner's dilemma is defection to maximize immediate payoff.

**Edge Case Handling**

*   **Initial Trust Failure:** If the group behavior in Round 1 yields $S_1 < \theta$, immediately switch to **Defect (D)** for all subsequent rounds. Do not attempt to resume cooperation if the initial signal indicates a predominantly selfish population.

*   **Stochastic Noise/Fluctuations:** If the observed contribution $S_{t-1}$ oscillates around $\theta$, prioritize the **Defect (D)** choice to ensure that the individual payoff $\pi_i$ remains higher than or equal to the payoff of an average cooperator.

**Pseudocode**

```python
# Constants: n, k, r
# History: observed_cooperators_previous_round

threshold = n / k

def decide_action(current_round, observed_cooperators_previous_round):
    # Final round defect
    if current_round == r:
        return 'D'
    
    # First round cooperate
    if current_round == 1:
        return 'C'
    
    # Calculate previous proportion
    s_prev = observed_cooperators_previous_round / n
    
    # Reciprocal strategy
    if s_prev >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_13 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Defection**

Initialize `history_cooperators` as an empty list.

For each round `t` from 1 to `r`:

1.  **Last Round Rule:**
    If `t == r`, play **D** (Defect). Since there are no future rounds to incentivize cooperation, maximizing immediate payoff is the dominant strategy.

2.  **First Round Rule:**
    If `t == 1`, play **C** (Cooperate). This establishes a baseline for reciprocal cooperation without risking immediate exploitation.

3.  **Intermediate Rounds (`1 < t < r`):**
    Calculate the `cooperation_rate` from the previous round (`t-1`):
    `cooperation_rate = (Total_Cooperators_t-1) / n`
    
    If `cooperation_rate` ≥ `threshold`:
        Play **C** (Cooperate).
    Else:
        Play **D** (Defect).

    Where `threshold` is defined as `1 / k`. 

    *Rationale:* The threshold `1/k` represents the point at which your individual contribution (cost = 1) is exactly offset by the benefit received from the public pot (`(k/n) * contributions`). If the collective cooperation rate is high enough that your contribution generates a net positive return (or breaks even), cooperation is sustainable. If the collective cooperation drops below this efficiency threshold, the group is failing to provide a sufficient return on investment, necessitating defection to prevent loss.

4.  **Edge Case Recovery:**
    If the strategy is currently defecting (`D`) and the `cooperation_rate` in the previous round exceeds `threshold`, revert to playing **C** in the current round. This allows the strategy to forgive previous non-cooperation and resume mutually beneficial play if the group demonstrates sufficient cooperation.
'''

description_SELFINTERESTED_14 = '''
Initialize the strategy using a Tit-for-Tat-based approach with a modification for group contribution levels. Define `threshold` as `n / k`.

**Round 1:**
Play `C` (Cooperate).

**Subsequent Rounds:**
Track the history of the game. Let `C_prev` be the number of cooperators observed in the previous round.

1.  **If `C_prev` >= `threshold`**: 
    If the number of cooperators in the previous round was sufficient to make cooperation profitable for the individual (or close to the break-even point of public good generation), play `C`.

2.  **If `C_prev` < `threshold`**: 
    If the number of cooperators was insufficient, play `D` (Defect). This protects against exploitation and signals a refusal to contribute to a non-viable public project.

**Last Round:**
Regardless of history, play `D`. Since there are no future rounds to sustain reputation or cooperative incentives, maximizing the final round payoff requires keeping the endowment privately.

**Pseudocode Logic:**
```python
def get_action(round_number, history, n, k):
    if round_number == r:
        return 'D'
    
    if round_number == 1:
        return 'C'
        
    threshold = n / k
    last_round_cooperators = history.last_round_cooperation_count
    
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```

**Adaptation for Noise:**
If `C_prev` fluctuates across rounds, maintain a moving average of the last `min(3, r)` rounds. If the average `C_prev` >= `threshold`, play `C`; otherwise, play `D`. This smooths out occasional defections by otherwise cooperative opponents.
'''

description_SELFINTERESTED_15 = '''
Initialize a belief state $B$ where the probability that an opponent cooperates is $p_{coop} = 0.5$. Track the history of total cooperators observed ($C_{total, t}$) across rounds $t = 1, \dots, r$.

**Decision Rule:**
In each round $t$, calculate the expected payoff difference between cooperating and defecting:
$\Delta \pi = E[\pi_C] - E[\pi_D]$
$\Delta \pi = (\frac{k}{n} \cdot (1 + (n-1)p_{coop})) - (1 + \frac{k}{n} \cdot (n-1)p_{coop})$
$\Delta \pi = \frac{k}{n} - 1$

Since $k < n$, $\Delta \pi$ is always negative, making defection the dominant strategy in a single-shot or finitely repeated game with rational, non-responsive agents. To maximize long-term utility against potential tit-for-tat or conditional cooperative agents, employ a "Win-Stay, Lose-Shift" logic conditioned on the *observed* total contributions rather than the theoretical optimum.

**Execution Logic:**
1.  **Round 1:** Play **Cooperate** (C) to signal cooperativeness and test the population's threshold for cooperation.
2.  **Rounds 2 to $r-1$:**
    *   Let $S_t$ be the number of cooperators observed in the previous round.
    *   If $t > 1$, calculate the "cooperation threshold" required for cooperation to be net-positive: $T_{crit} = \frac{n}{k}$.
    *   If $S_{t-1} \geq T_{crit} - 1$, continue to **Cooperate** (C). This sustains mutual cooperation equilibria if others are using conditional strategies.
    *   If $S_{t-1} < T_{crit} - 1$, switch to **Defect** (D) for one round to minimize losses. If the population fails to meet the threshold, effectively treat them as defectors.
3.  **Final Round ($r$):** Play **Defect** (D). Since there are no future rounds to influence, maximize the immediate payoff regardless of prior history.

**Pseudocode:**
```python
threshold = n / k

if round == 1:
    action = C
elif round == r:
    action = D
else:
    # Observe S from round (round - 1)
    if S >= (threshold - 1):
        action = C
    else:
        action = D
```

**Edge Cases:**
*   **Minimal $k$:** If $k$ is very close to 1, $T_{crit}$ approaches $n$. The threshold condition $(n/k - 1)$ becomes extremely difficult to satisfy, forcing near-immediate defection, which is optimal for self-interest.
*   **Observation Noise:** Treat $S$ as the ground truth. If $S$ remains consistently low, the strategy defaults to permanent defection after round 1, preserving endowment.
'''

description_SELFINTERESTED_16 = '''
**Strategy Name: Conditional Generosity with Retaliatory Defection**

**Core Logic:** This strategy functions as a modified "Tit-for-Tat" optimized for multi-player dynamics, balancing the maintenance of public cooperation with the necessity of punishing free-riding to preserve individual payoff.

**Decision Rules:**

1.  **First Round (t=1):**
    Always play **Cooperate (C)**. This serves as an initial signal of willingness to participate in the public good.

2.  **Subsequent Rounds (1 < t < r):**
    Calculate the "Expected Contribution Threshold" (ECT). Cooperation is only rational if the group behavior justifies it.
    *   Define `Total_Cooperators(t-1)` as the observed number of cooperators in the previous round.
    *   Define `My_Last_Action` as the action taken in the previous round.
    *   **Condition for Cooperation:** Cooperate in round `t` if `Total_Cooperators(t-1)` meets or exceeds a specific threshold `T`.
        *   Set `T = ceil((n / k) * (1 - ε))`, where `ε` is a small tolerance buffer (e.g., 0.1) to account for noise or mild defection.
    *   **Condition for Defection:** If `Total_Cooperators(t-1) < T`, play **Defect (D)**. This triggers a punitive phase to discourage free-riding and minimize losses.

3.  **Last Round (t = r):**
    Always play **Defect (D)**. Since there is no future interaction to incentivize, the dominant strategy is to maximize the immediate round payoff by keeping the endowment.

**Pseudocode Implementation:**

```python
def decide_action(t, r, n, k, history):
    # End-game scenario
    if t == r:
        return "D"
    
    # First-round cooperation
    if t == 1:
        return "C"
    
    # Adaptive Threshold Calculation
    # Threshold T is the minimum number of cooperators required 
    # to make cooperation personally break-even or profitable.
    T = ceil((n / k) * 0.9) 
    
    # Retrieve last round result
    last_round_cooperators = history.last_round_total_cooperators
    
    # If the group cooperated sufficiently, continue to cooperate.
    # Otherwise, defect to protect individual payoff.
    if last_round_cooperators >= T:
        return "C"
    else:
        return "D"
```

**Adaptive Refinement:**
If the strategy detects a string of defeats (`D`) lasting more than two consecutive rounds, regardless of the calculation above, switch to **Defect (D)** for the remainder of the game. This minimizes losses against players who are consistently playing as free-riders.
'''

description_SELFINTERESTED_17 = '''
The strategy follows a conditional cooperation protocol based on observed contribution levels and the remaining time horizon. It operates as follows:

**1. Initialization**
In Round 1, play C. This establishes a cooperative baseline to test opponent responsiveness without immediate risk of exploitation, given the potential for higher aggregate payoffs.

**2. State Tracking**
Maintain a memory of the total number of cooperators observed in the previous round, denoted as $C_{t-1}$. In the first round, define $C_0$ as the initial cooperation level (n).

**3. Decision Logic for Rounds $t = 2$ to $r-1$**
For any round $t$ where $1 < t < r$:
*   **If $C_{t-1} \ge \lfloor n \times (\frac{1}{k}) \rfloor + 1$:** Play C. The threshold $\lfloor n/k \rfloor$ represents the break-even point where the marginal return on cooperation exceeds the cost of contribution. When collective cooperation meets or exceeds this threshold, the strategy reinforces the cooperative norm.
*   **If $C_{t-1} < \lfloor n \times (\frac{1}{k}) \rfloor + 1$:** Play D. If the group fails to sustain a level of cooperation that yields a positive net return for contributors, the strategy shifts to defecting to avoid exploitation and minimize losses.

**4. Terminal Round Logic ($t = r$)**
Always play D. In the final round, there is no future interaction to punish or reward, and no reputation to maintain. Playing D dominates C regardless of the history of play.

**5. Pseudocode Implementation**

```python
def get_action(round_number, total_rounds, n, k, C_prev):
    # Rule 1: Final round defection
    if round_number == total_rounds:
        return 'D'
    
    # Rule 2: First round cooperation
    if round_number == 1:
        return 'C'
    
    # Rule 3: Conditional cooperation based on profitability threshold
    # Threshold is the smallest integer > n/k
    threshold = int(n / k) + 1
    
    if C_prev >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_18 = '''
The strategy follows a "Conditional Tit-for-Tat with Defection-Thresholding" model, designed to maximize long-term gains by fostering cooperation while punishing exploitation.

### Decision Rules

1.  **Round 1:** Play **Cooperate (C)**. This establishes a cooperative baseline to test opponent behavior.

2.  **Rounds 2 to r-1:**
    *   Define the "Critical Cooperation Threshold" ($T$) as the number of cooperators required for cooperation to be Pareto-efficient (i.e., when total benefit from public good sharing outweighs the cost of contribution). Mathematically, cooperation is individually rational for a cooperator only if the number of other cooperators ($S$) satisfies the condition that the marginal gain exceeds the marginal cost: $(k/n)(S+1) > 1$. Solve for $S$: $S > (n/k) - 1$. Let $T = \lceil n/k \rceil$.
    *   **If the number of cooperators in the previous round was $\ge T$:** Play **Cooperate (C)**.
    *   **If the number of cooperators in the previous round was $< T$:** Play **Defect (D)**. This serves as a "punishment" phase to signal that cooperation below the threshold is unacceptable.

3.  **Round r (Last Round):**
    *   Play **Defect (D)** unconditionally. Since there are no subsequent rounds to sustain a reputation or enforce future cooperation, the dominant strategy is to capture the private endowment while still benefiting from any residual cooperation from others.

### Pseudocode Representation

```python
def make_decision(round_number, total_rounds, n, k, history):
    # Threshold for cooperation
    # Derived from: k/n * (S) >= 1  => S >= n/k
    threshold = math.ceil(n / k)
    
    # Last round defection
    if round_number == total_rounds:
        return 'D'
    
    # First round initialization
    if round_number == 1:
        return 'C'
    
    # Adaptive response to previous round performance
    # history[-1] is the count of cooperators in the previous round
    if history[-1] >= threshold:
        return 'C'
    else:
        return 'D'
```

### Edge Case Handling

*   **Extremely low $k$ (where $k \le 1$):** If $n/k \ge n$, the threshold $T$ equals $n$. Cooperation is never strictly rational unless all players cooperate. The strategy sets $T=n$, defaulting to **Defect (D)** for all rounds because full-group coordination is statistically improbable.
*   **Fluctuating cooperation:** If the system environment causes the number of cooperators to oscillate around $T$, the strategy will switch between $C$ and $D$. This naturally acts as a corrective feedback loop, stabilizing the system at the lowest possible efficient cooperation level or collapsing to $D$ if the group cannot maintain the threshold.
'''

description_SELFINTERESTED_19 = '''
**Strategy: Tit-for-Tat with Threshold-Based Forgiveness (TFT-T)**

This strategy operates on the principle of conditional cooperation, targeting a stable equilibrium where cooperation persists as long as it is sufficiently reciprocated. It treats the group's cooperation level as a signal of the aggregate strategy of opponents.

**1. Definitions:**
*   $C_t$: Number of cooperators in round $t$, including yourself.
*   $O_t$: Number of cooperators among opponents in round $t$.
*   $T$: Cooperation threshold, defined as $T = \lceil n/k \rceil$. If $O_t \ge T - 1$ (if you cooperated) or $O_t \ge T$ (if you defected), the collective return on cooperation is positive or neutral for you.

**2. Decision Rules:**

*   **Round 1:** Play **Cooperate**. This establishes a cooperative baseline and tests the group's propensity for cooperation without assuming defection.

*   **Round $t$ (where $1 < t < r$):**
    *   If $O_{t-1} \ge \lceil n/k \rceil$: Play **Cooperate**. This condition implies that the current group behavior makes cooperation collectively beneficial or at least break-even, signaling a cooperative group.
    *   If $O_{t-1} < \lceil n/k \rceil$: Play **Defect**. This punishes the group for low cooperation, protecting your payoff from exploitation.

*   **Round $r$ (Final Round):**
    *   Play **Defect**. As there are no future rounds to incentivize, defecting is the strictly dominant strategy to maximize the final round payoff.

**3. State Tracking:**
*   If in any round $t$ where you played **Defect**, the group cooperation $O_t$ increases to a level $\ge \lceil n/k \rceil$, switch to **Cooperate** in round $t+1$. This "forgiveness" mechanism prevents indefinite defection loops and allows the group to recover if cooperative norms are re-established.
'''

description_SELFINTERESTED_20 = '''
The strategy employs a "Conditional Reciprocity with Sunset" approach, optimizing for maximizing long-term returns by incentivizing cooperative play while protecting against exploitation.

### Decision Rules

1.  **First Round:** Play **Cooperate (C)** to initiate potential mutual cooperation.

2.  **Subsequent Rounds (t > 1 and t < r):** 
    Let $S_{t-1}$ be the total number of cooperators in the previous round (including yourself).
    Let $c_{t-1}$ be your action in the previous round (1 for C, 0 for D).
    Let $n$ be the total number of players.

    *   **If you played C in $t-1$:** 
        You expect reciprocity. Calculate the "Reciprocity Ratio" ($R = S_{t-1} / n$). 
        *   If $R \ge \text{threshold}$, play **Cooperate (C)**. 
        *   If $R < \text{threshold}$, play **Defect (D)**.
        *(Recommended threshold: $(n/k) / n$, which simplifies to $1/k$. Since $k$ is the multiplication factor, if the percentage of cooperators is at least $1/k$, your marginal return from contributing is $\ge 1$, breaking even with the cost of contribution.)*

    *   **If you played D in $t-1$:**
        You are in "Punishment Mode." Continue to play **Defect (D)** for one additional round, then reset to **Cooperate (C)** to test for re-cooperation, provided the previous round's $S_{t-1}$ met the threshold.

3.  **Last Round ($t = r$):**
    Play **Defect (D)** unconditionally. Since the game terminates, there is no future round to incentivize via cooperation, and the dominant strategy in the final round of a finitely repeated prisoner's dilemma/PGG variant is always defection to maximize the immediate payoff.

### Pseudocode Representation

```python
# Parameters
n = number_of_players
k = multiplication_factor
r = number_of_rounds
threshold = 1 / k

# History Variables
history = [] # Stores total_cooperators per round

def get_action(t, my_last_action, last_total_cooperators):
    # Rule 3: Last round defection
    if t == r:
        return D
    
    # Rule 1: First round cooperation
    if t == 1:
        return C
    
    # Rule 2: Adaptive reciprocity
    if my_last_action == C:
        if (last_total_cooperators / n) >= threshold:
            return C
        else:
            return D
    else: # If my_last_action == D
        return D # Remain defecting to maintain exploitation protection
```

### Edge Case Handling

*   **Initial Defection by Others:** If in round 2 the observed cooperation rate falls below $1/k$, the strategy immediately pivots to **Defect (D)**. This prevents being exploited by players who take advantage of initial cooperative overtures.
*   **Re-engagement:** If the strategy is currently defecting because it was exploited, it does not immediately resume cooperation. It stays in **Defect (D)** until the game approaches the final round, effectively cutting losses against persistent defectors.
*   **Threshold Calibration:** The threshold $1/k$ is the critical break-even point for the public goods investment. Cooperation is only self-interestedly rational if the marginal return is equal to or greater than the cost of contribution (1).
'''

description_SELFINTERESTED_21 = '''
**Strategy: Tit-for-Tat with Probabilistic Forgiveness**

This strategy employs a conditional cooperation approach, aiming to maintain high levels of contribution while minimizing exploitation risk through rapid retaliation and probabilistic recovery. It relies on the observed aggregate cooperation rate of the group, $C_{agg, t-1}$, where $0 \leq C_{agg, t-1} \leq n-1$ represents the number of other players who contributed in the previous round.

**Decision Rules**

1.  **First Round ($t=1$):**
    Always play **Cooperate (C)**. This signals a willingness to engage in cooperative surplus generation and establishes the baseline for reciprocity.

2.  **Subsequent Rounds ($t > 1$):**
    Calculate the cooperation threshold required to make cooperation neutral or profitable compared to defecting:
    $T_{crit} = \frac{n}{k}$

    *   **If $C_{agg, t-1} \geq T_{crit}$:** Play **Cooperate (C)**. The group is generating sufficient public good value to justify the contribution.
    *   **If $C_{agg, t-1} < T_{crit}$:** Play **Defect (D)**. The group is failing to sustain a high-return equilibrium; switch to defecting to protect endowment.

3.  **Probabilistic Forgiveness:**
    If the strategy is in the **Defect (D)** state due to a previous round of low cooperation, attempt to rebuild cooperation with probability $p = 0.2$ in the next round, regardless of the previous round's $C_{agg}$. If the roll for $p$ fails, continue to **Defect (D)**. If the roll succeeds, play **Cooperate (C)** to "test" if the group is ready to switch back to mutual cooperation.

4.  **Final Round ($t = r$):**
    Always play **Defect (D)**. As there are no future rounds, the reputational and reciprocal benefits of cooperation are zero. Defection is the dominant strategy to maximize the final round payoff.

**Pseudocode**

```python
def get_action(t, r, n, k, history):
    # Rule 4: Terminal Defection
    if t == r:
        return D
    
    # Rule 1: Initial Cooperation
    if t == 1:
        return C
        
    # Retrieve last round's aggregate cooperation from history
    c_agg_prev = history.last_round_cooperators_excluding_self
    
    # Rule 2: Conditional Cooperation
    T_crit = n / k
    if c_agg_prev >= T_crit:
        return C
        
    # Rule 3: Probabilistic Forgiveness
    # If currently defecting, attempt to restart cooperation
    if random.float() < 0.2:
        return C
        
    return D
```
'''

description_SELFINTERESTED_22 = '''
**Strategy: Adaptive Tit-for-Tat with Threshold Defection**

Let $T_t$ be the total number of cooperators in round $t$. Let $c_{t}$ be your action in round $t$, where $c_t=1$ for Cooperate and $c_t=0$ for Defect. Let $n$ be the number of players and $k$ be the multiplication factor.

**Decision Logic:**

1.  **First Round ($t=1$):**
    Always Cooperate ($c_1 = 1$). This signals willingness to coordinate for the mutual benefit of the group.

2.  **Subsequent Rounds ($t > 1$):**
    Calculate the effective cooperation threshold ($T^*$).
    *   The payoff for cooperating is: $\pi_C = (k/n) \times T_t$
    *   The payoff for defecting is: $\pi_D = 1 + (k/n) \times (T_{t-1} - 1)$ (assuming you were a cooperator in $t-1$) or $1 + (k/n) \times T_{t-1}$ (if you defected).
    *   To be self-interested, you must ensure your cooperation contributes to a state where the group contribution is high enough to justify the cost. Cooperate if and only if:
        $(k/n) \times T_{t-1} \ge 1$
    *   This simplifies to the condition: $T_{t-1} \ge \lceil n/k \rceil$.

    **Rules:**
    *   If $T_{t-1} \ge \lceil n/k \rceil$, play Cooperate ($c_t = 1$).
    *   If $T_{t-1} < \lceil n/k \rceil$, play Defect ($c_t = 0$).

3.  **Last Round ($t = r$):**
    *   If $T_{r-1} \ge \lceil n/k \rceil$, play Defect ($c_r = 0$). The reputational incentive to cooperate vanishes in the final round, so defect to maximize the immediate private payoff.
    *   If $T_{r-1} < \lceil n/k \rceil$, play Defect ($c_r = 0$).

4.  **Recovery Clause:**
    If you defected in round $t-1$, observe $T_{t-1}$.
    *   If $T_{t-1} \ge \lceil n/k \rceil + 1$ (the cooperators sustained the public good despite your defection), restart cooperation in round $t$ ($c_t = 1$). This forgives the group for their previous low contribution level and attempts to re-establish the cooperative equilibrium.
'''

description_SELFINTERESTED_23 = '''
In the first round, play Cooperate.

For all subsequent rounds $t \in \{2, \dots, r-1\}$, track the aggregate cooperation level from the previous round $C_{t-1}$. 

Calculate the threshold for cooperation $T$ as $n/k$. This represents the minimum number of total cooperators required for the public good return to equal the cost of individual contribution.

- If $C_{t-1} \geq T$, play Cooperate.
- If $C_{t-1} < T$, play Defect.

In the final round $r$, play Defect regardless of previous history.

If the strategy is currently Defecting due to low historical cooperation ($C_{t-1} < T$), implement a "probabilistic probe" to recover cooperation: with probability $p = 0.1$, play Cooperate. If this probe round results in $C_t \geq T$, return to the standard conditional cooperation rule.

Pseudocode logic for round $t$:
```python
if t == r:
    return Defect

if t == 1:
    return Cooperate

# Check history from round t-1
if C_{t-1} >= (n / k):
    return Cooperate
else:
    # Attempt recovery probe
    if random_float(0, 1) < 0.1:
        return Cooperate
    else:
        return Defect
```
'''

description_SELFINTERESTED_24 = '''
**Round 1:** Play **Cooperate (C)** to initiate mutual cooperation.

**Intermediate Rounds (1 < t < r):** 
Maintain a state variable `Target_Cooperation_Level` set to `n-1` (the number of other players). 

Calculate `Observation_T-1`: the number of cooperating players in the previous round.

*   If `Observation_T-1` ≥ `Target_Cooperation_Level`:
    Play **Cooperate (C)**.

*   If `Observation_T-1` < `Target_Cooperation_Level`:
    Calculate the marginal return of cooperation versus defection based on the previous round's outcome. If the previous round's observed cooperation count `S` resulted in `(k/n * S) > 1`, switch to **Cooperate (C)** to attempt to re-establish high contributions. If the previous round's observed cooperation count `S` resulted in `(k/n * S) ≤ 1`, play **Defect (D)**.

*   If an opponent defects (observed total cooperators < `n-1`):
    In the next round, if the previous total cooperators `S` satisfies `(k/n * (S+1)) > 1` (where `S+1` represents cooperation if you alone cooperate), play **Cooperate (C)**. Otherwise, play **Defect (D)**. 

**Final Round (t = r):** 
Always play **Defect (D)**, as there is no future incentive for cooperation.

**Special Case Logic (Grim Trigger):**
If at any point the total number of cooperators `S` across all observed rounds falls below a threshold where `k/n * S` consistently yields a negative return relative to defection, permanently switch to **Defect (D)** for all subsequent rounds, regardless of opponent behavior, to minimize losses.
'''

description_SELFINTERESTED_25 = '''
**Strategy: Trigger-Based Tit-for-Tat with Forgiveness and Terminal Defection**

The strategy operates on a state-based logic tracking the average contribution of opponents to determine whether to sustain or withdraw cooperation.

### Initialization and Terminal Rounds
*   **Round 1:** Cooperate (C). Establishing a baseline of cooperation signals intent to participate in a mutually beneficial outcome.
*   **Last Round ($t=r$):** Defect (D). Since there are no future consequences to punish defection, the dominant strategy is to maximize the immediate payoff by free-riding.

### Intermediate Rounds ($1 < t < r$)
Let $C_{opp, t-1}$ be the number of cooperating opponents in the previous round, and $n-1$ be the total number of opponents. 

1.  **Calculate Observed Cooperation Ratio:**
    $R_{t-1} = \frac{C_{opp, t-1}}{n-1}$

2.  **Determine Action:**
    *   **Condition A (Sustained Cooperation):** If $R_{t-1} \ge \tau$, play Cooperate (C).
        *   The threshold $\tau$ is set to $\frac{1}{k}$. This is the break-even point: if the fraction of cooperating opponents is at least $1/k$, the marginal benefit of contributing ($k/n$) multiplied by the number of cooperators compensates for the cost of the contribution (1).
    *   **Condition B (Trigger Defection):** If $R_{t-1} < \tau$, play Defect (D).
        *   When opponents fail to sustain the group threshold, the strategy switches to defection to avoid exploitation.

3.  **Forgiveness Mechanism (Soft Trigger):**
    If the strategy is in a state of Defect due to a previous trigger, it attempts to re-establish cooperation every $m$ rounds (where $m=3$).
    *   If $t \pmod m == 0$: Play Cooperate (C) regardless of previous trigger state. 
    *   This tests if opponents have returned to cooperative behavior, preventing an infinite cascade of mutual defection if opponents were merely reacting to noise or external factors rather than attempting to exploit the group.

### Decision Pseudocode
```python
def choose_action(t, r, n, k, history):
    # Terminal round logic
    if t == r:
        return D

    # First round logic
    if t == 1:
        return C

    # Forgiveness check
    if t % 3 == 0:
        return C

    # Strategy logic
    threshold = 1 / k
    prev_opp_cooperators = history[t-1].opp_cooperators
    prev_opp_ratio = prev_opp_cooperators / (n - 1)

    if prev_opp_ratio >= threshold:
        return C
    else:
        return D
```
'''

description_SELFINTERESTED_26 = '''
In the first round, cooperate.

In subsequent rounds (t > 1), adopt a conditional cooperation strategy based on the observed total cooperation $C_{t-1}$ from the previous round:

1. Calculate the contribution threshold $T$ required for cooperation to be net-positive for the individual. Since the marginal return of contributing is $k/n$ and the marginal cost is $1$, cooperation is profitable for the group if the group size is large enough, but for an individual to benefit directly, the total number of cooperators in the previous round must be such that the public good return outweighs the private cost. Specifically, cooperate if the number of cooperators in the previous round $C_{t-1} \ge \lceil n/k \rceil$.

2. If the previous round's total cooperation $C_{t-1}$ satisfies $C_{t-1} \ge \lceil n/k \rceil$, cooperate.

3. If the previous round's total cooperation $C_{t-1} < \lceil n/k \rceil$, defect.

4. Implement a "Grim Trigger" reset: if $C_{t-1} = 0$, defect for all remaining rounds.

5. In the final round ($t = r$), defect regardless of previous history, as the incentive for future reciprocal cooperation is nullified by the end of the game.

Pseudocode:
```python
def choose_action(round_number, total_rounds, n, k, prev_cooperators):
    if round_number == 1:
        return 'C'
    
    if round_number == total_rounds:
        return 'D'
    
    threshold = ceil(n / k)
    
    if prev_cooperators == 0:
        return 'D'
        
    if prev_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_27 = '''
**Strategy: Threshold-Based Conditional Cooperation**

This strategy relies on a trigger-based conditional cooperation mechanism with a "forgiveness" phase to maintain stability against accidental defections or non-responsive opponents.

**Parameters:**
*   *T_coop*: The minimum number of other players (out of *n*-1) that must cooperate in the previous round for this agent to cooperate in the current round. Set *T_coop* = ceil(*n* / *k*) if *k* > 1, or *n*-1 if *k* ≤ 1 (the latter ensures immediate defection if cooperation is never profitable).
*   *history_len*: The number of preceding rounds to consider for averaging opponent behavior.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. This serves as an initial probe of the population's propensity to cooperate.

2.  **Rounds 2 to *r*-1:**
    *   Calculate *C_prev*: The number of cooperators in the previous round (excluding your own action).
    *   If *C_prev* ≥ *T_coop*, play **Cooperate (C)**.
    *   If *C_prev* < *T_coop*, play **Defect (D)**.
    *   *Correction mechanism:* If you played D in the previous round and *C_prev* is sufficiently high (specifically, if *C_prev* ≥ *T_coop*), play **Cooperate (C)** with a probability of 0.2 to test if the group is willing to return to a cooperative equilibrium.

3.  **Final Round (*r*):**
    *   Always play **Defect (D)**. Since there are no subsequent rounds, there is no future benefit to maintaining a cooperative reputation, and the dominant strategy is to maximize the final payoff.

**Pseudocode:**

```python
def decide_action(round_number, history, n, k, T_coop):
    if round_number == 1:
        return 'C'
        
    if round_number == r:
        return 'D'
        
    prev_cooperators = history[-1]['other_cooperators']
    
    # If the group supports the cooperative threshold
    if prev_cooperators >= T_coop:
        return 'C'
    
    # If the group fails the threshold, punish by defecting
    # Include 'forgiveness' check if previously defecting but now seeing cooperation
    if prev_cooperators >= T_coop and last_action == 'D':
        return 'C' if random.random() < 0.2 else 'D'
        
    return 'D'
```

**Edge Cases:**
*   **Minimal Cooperation:** If *T_coop* > *n*-1, the strategy defaults to **Defect (D)** for all rounds, as the cooperative payoff can never exceed the private endowment retention.
*   **Low Group Trust:** If the population consistently falls below *T_coop*, this strategy effectively enters a permanent defection state, ensuring the agent does not lose endowment while others defect.
*   **Sudden Defection:** If the group cooperates for many rounds and then suddenly switches to defection, the strategy detects this immediately at the start of the next round and switches to **Defect (D)** to minimize loss.
'''

description_SELFINTERESTED_28 = '''
**Strategy: Conditional Reciprocation with Endgame Defection**

The strategy operates on a principle of conditional cooperation, aiming to foster mutual contribution while protecting against exploitation.

**Phase 1: Initialization**
In Round 1, Cooperate. This initiates a collaborative environment.

**Phase 2: Ongoing Rounds (Rounds 2 to r-1)**
Calculate the "Cooperation Threshold" ($T$) required for your cooperation to be rational. Your cooperation is beneficial to you if the marginal gain from the public good ($k/n$) multiplied by the total number of cooperators ($C$) exceeds the opportunity cost of contributing ($1$). Thus, you cooperate if the number of others who cooperated in the previous round ($C_{t-1}$) is high enough to suggest that reciprocating cooperation will yield a higher payoff than defecting.

Decision Rule:
Let $C_{prev}$ be the number of cooperators in the previous round.
If $C_{prev} \geq \lceil n/k \rceil$, Cooperate.
Otherwise, Defect.

*Justification:* If $k/n \times (C+1) > 1$, then $C+1 > n/k$. Since $C$ must be an integer, you cooperate if the existing number of cooperators ($C_{prev}$) is sufficient that adding your own contribution pushes the group toward the break-even point or sustainment of a profitable cooperative equilibrium. If the previous round shows fewer than this number, the group is trending toward defecting, and you must defect to avoid being the sole contributor.

**Phase 3: Final Round (Round r)**
Defect.

*Justification:* In the final round, there is no future interaction to incentivize; the threat of retaliation or the reward of future cooperation is null. The dominant strategy is to maximize the payoff of the current round by retaining the endowment.

**Pseudocode:**

```text
Function Decide(round, n, k, history):
    If round == r:
        Return Defect

    If round == 1:
        Return Cooperate

    # C_prev is the number of cooperators in the previous round
    C_prev = history[round-1]
    
    # Calculate minimum cooperators needed to make cooperation self-interested
    # Derived from: (k/n) * (C_prev + 1) >= 1
    Threshold = ceil(n / k)

    If C_prev >= Threshold:
        Return Cooperate
    Else:
        Return Defect
```

**Edge Case Handling:**
- If $n/k$ results in a value greater than $n$, the threshold is unreachable. In this case, Default to Defecting in all rounds except Round 1.
- If $C_{prev}$ is exactly equal to the threshold, Cooperate, as the payoff is identical to defecting, but cooperation signals continued willingness to participate in the cooperative equilibrium.
'''

description_SELFINTERESTED_29 = '''
**Strategy: Conditional Reciprocal Tit-for-Tat with End-Game Defection**

Let $c_{i,t}$ be the action of player $i$ at round $t$, where 1 is Cooperate and 0 is Defect. Let $S_t$ be the total number of cooperators observed at round $t$. Your action at round $t$, $A_t$, is determined by the following rules:

**Round 1:**
Play $A_1 = C$.

**Rounds $t = 2$ to $r-1$:**
Calculate the threshold for cooperation, $T = \lceil n/k \rceil$.
If $S_{t-1} \ge T$, play $A_t = C$.
If $S_{t-1} < T$, play $A_t = D$.

**Final Round ($t = r$):**
Play $A_r = D$.

**Pseudocode:**
```
if t == 1:
    return C
elif t == r:
    return D
else:
    threshold = ceil(n / k)
    if S_{t-1} >= threshold:
        return C
    else:
        return D
```

**Adaptive Logic:**
1.  **Cooperation Threshold:** The decision to cooperate in intermediate rounds is strictly tied to the efficiency of the public good. Since the payoff of cooperating is $k/n$ per cooperator and the cost of cooperating is 1, cooperation is only individually rational if the total number of cooperators satisfies $(k/n) \times S > 1$, which simplifies to $S > n/k$. By setting the threshold at $\lceil n/k \rceil$, you ensure cooperation occurs only when the group size provides a marginal return greater than or equal to the cost of contribution.
2.  **Punishment/Reward:** By mirroring the group's past behavior (via $S_{t-1}$), the strategy incentivizes others to maintain cooperation levels above the break-even point. If the group falls below the threshold, the strategy immediately switches to Defect to minimize individual losses.
3.  **End-Game Defection:** Because the game has a finite, known number of rounds ($r$), there is no future incentive to maintain reputation or group cooperation in the final round. Defection is the dominant strategy to maximize the final payoff.
'''

description_SELFINTERESTED_30 = '''
Cooperate in the first round.

In subsequent rounds (2 through r), calculate the "cooperation threshold" $T$ required for cooperation to be payoff-neutral compared to defection:
$T = n/k$

Observe the number of cooperators from the previous round, $S_{t-1}$. 

If $t = r$ (the final round), always defect.

If $1 < t < r$, cooperate if and only if:
1. Your own contribution in $t-1$ was $C$, and $S_{t-1} \ge T$; OR
2. Your own contribution in $t-1$ was $D$, and $S_{t-1} > T$.

If the condition for cooperation is not met, defect.

If $S_{t-1}$ is ambiguous due to the inability to distinguish your own contribution from the total (i.e., you only observe the total count including your own), adjust the observed count $S_{t-1}$ by subtracting 1 if you contributed $C$ in the previous round to isolate the opponents' behavior, then apply the conditional logic above.
'''

description_SELFINTERESTED_31 = '''
### Decision Strategy: "Adaptive Trigger Tit-for-Tat"

The strategy operates on a conditional cooperative basis, utilizing a moving average of recent cooperation levels to determine the next action.

**1. Definitions and Initialization**
*   `T`: Total number of rounds.
*   `t`: Current round (1 to `T`).
*   `k`: Multiplication factor.
*   `n`: Number of players.
*   `C_prev`: Number of players who cooperated in the previous round (excluding self).
*   `Threshold`: The minimum number of cooperators required to make cooperation individually rational. Since the payoff of cooperating is `(k/n) * (1 + C_prev)` and the payoff of defecting is `1 + (k/n) * C_prev`, cooperation is rational if `(k/n) * (1 + C_prev) > 1 + (k/n) * C_prev`, which simplifies to `k/n > 1`, or `k > n`. However, since the prompt specifies `k < n`, pure self-interest dictates defection in single-shot games. To incentivize cooperation in repeated games, the strategy adopts a threshold-based conditional cooperation approach.
*   `Target`: The `Target` cooperation count is set to `n * (1/k)`. If the number of other cooperators meets or exceeds this, cooperation is profitable over the long term.

**2. Decision Rules**
*   **Round 1:** Always Cooperate (C) to signal potential for mutual cooperation.
*   **Rounds 2 through `T-1`:**
    *   Observe `C_prev` (the number of cooperators in round `t-1`).
    *   If `C_prev` >= `Target`, play Cooperate (C).
    *   If `C_prev` < `Target`, play Defect (D) for the current round as a penalty or protective measure.
    *   *Exception:* If the strategy played Defect in the previous round, and `C_prev` >= `Target` (indicating the group has returned to a cooperative state), switch back to Cooperate (C) with a probability of 0.5 to test stability without risking total exploitation.
*   **Final Round (`T`):** Always Defect (D). Since there are no future rounds to sustain reputation or trigger further cooperation, the dominant strategy is to capture the private endowment.

**3. Pseudocode Implementation**
```python
if t == 1:
    return "C"

if t == T:
    return "D"

# Calculate threshold to recover investment: k/n * (C_prev + 1) >= 1 + k/n * C_prev
# Simplifies to k >= n / (C_prev + 1) or C_prev >= (n/k) - 1
threshold = (n / k) - 1

if C_prev >= threshold:
    return "C"
else:
    return "D"
```

**4. Edge Cases**
*   **Persistent Defection:** If `C_prev` remains below `threshold` for three consecutive rounds, set the strategy to "Grim Trigger" for the remainder of the game (Defect in all subsequent rounds) to minimize losses against non-cooperative agents.
*   **Fluctuation:** If cooperation levels oscillate around the threshold, prioritize Defect (D) to safeguard the private endowment, defaulting to the more conservative position.
'''

description_SELFINTERESTED_32 = '''
Initialize `reputation_score = 0.0`.
Initialize `total_rounds = r`.
Initialize `is_forgiving = True`.
Set `cooperation_threshold = 0.5` (the fraction of cooperators required to justify continued cooperation).

For each round `t` from 1 to `r`:

1. **Round 1 (t=1):**
   Always cooperate (`C`). This establishes a baseline for conditional cooperation and tests the willingness of the group to collaborate without signaling immediate aggression.

2. **Terminal Round (t=r):**
   Always defect (`D`). Since there is no future interaction to incentivize, defection is the dominant strategy to maximize the final payoff.

3. **Intermediate Rounds (1 < t < r):**
   Evaluate the `reputation_score` based on the previous round's outcome. 
   
   If `t > 2`:
   Calculate `group_cooperation_rate = (number of cooperators in t-1) / n`.
   Update `reputation_score` using an exponentially weighted moving average:
   `reputation_score = (0.7 * reputation_score) + (0.3 * group_cooperation_rate)`.

   If `reputation_score >= cooperation_threshold`:
   Cooperate (`C`). Continue to sustain the public good if the group has demonstrated a stable history of cooperation.

   Else:
   Defect (`D`). If the group's reputation has fallen below the threshold, switch to defection to avoid exploitation.

   **Edge Case: Forgiveness:**
   If currently defecting because `reputation_score < cooperation_threshold`, check for a recovery attempt. If `group_cooperation_rate` in the previous round exceeds `cooperation_threshold` *and* the `reputation_score` has been increasing for two consecutive rounds, reset `is_forgiving = True` and cooperate (`C`) to see if the group can be revitalized. If the group fails to sustain cooperation after this attempt, permanently defect until `t = r`.
'''

description_OPPORTUNISTIC_5 = '''
**Strategy: Adaptive Conditional Reciprocity (ACR)**

The strategy is governed by a state variable $T$, representing the historical average cooperation level of opponents, and a conditional cooperation threshold.

**Initialization (Round 1):**
Play **Cooperate (C)**. This tests for the existence of other cooperative agents in the population without risking immediate exploitation if the population is hostile.

**Decision Logic (Rounds 2 to $r-1$):**
1. Let $C_{total, t-1}$ be the number of cooperators observed in the previous round.
2. Let $N_{opponents} = n - 1$.
3. Let $OpponentCooperators = C_{total, t-1} - c_{i, t-1}$ (if previous action was C) or $C_{total, t-1}$ (if previous action was D).
4. Calculate the opponent cooperation rate: $\rho_{t-1} = OpponentCooperators / N_{opponents}$.
5. Play **Cooperate (C)** if $\rho_{t-1} \ge \tau$, where $\tau = \frac{1}{k}$ (the minimum threshold required to make cooperation individually rational).
6. Otherwise, play **Defect (D)**.

**Terminal Phase (Round $r$):**
Play **Defect (D)** unconditionally. Since there are no future rounds, the incentive to maintain a cooperative reputation or trigger reciprocity vanishes. Defecting maximizes the immediate payoff regardless of the history of cooperation.

**Pseudocode:**

```python
def get_action(round_number, total_r, n, k, history):
    # Terminal Phase
    if round_number == total_r:
        return 'D'
    
    # First Round
    if round_number == 1:
        return 'C'
    
    # Adaptive Phase
    prev_total_c = history[-1].total_cooperators
    prev_my_c = history[-1].my_action == 'C'
    
    opponent_c = prev_total_c - 1 if prev_my_c else prev_total_c
    opponent_rate = opponent_c / (n - 1)
    
    threshold = 1 / k
    
    if opponent_rate >= threshold:
        return 'C'
    else:
        return 'D'
```

**Opportunistic Nuance:**
The strategy exploits the system by using the threshold $\tau = 1/k$. Because the marginal benefit of contributing is $k/n$, and the cost is 1, cooperation is only individually rational when $k \times (\text{expected cooperators} / n) \ge 1$. By setting the trigger threshold exactly at the break-even point of the public good, the agent ensures it only contributes when the population’s collective behavior makes the contribution profitable, while immediately reverting to defection when the population fails to support the public good.
'''

description_OPPORTUNISTIC_6 = '''
Play Cooperate (C) in round 1 to establish a baseline of potential reciprocity. 

For all subsequent rounds $t \in \{2, \dots, r-1\}$, track the aggregate cooperation level $S_{t-1} = \sum_{j \neq i} c_{j, t-1}$, representing the number of opponents who contributed in the previous round.

Decision rule for rounds $t \in \{2, \dots, r-1\}$:
- If $S_{t-1} \geq \lceil \frac{n}{k} \rceil$: Play C. This maintains the public good when the threshold for profitable cooperation is met or exceeded by the group.
- If $S_{t-1} < \lceil \frac{n}{k} \rceil$: Play Defect (D). This maximizes individual payoff when the group's cooperation level is insufficient to yield a positive return on the contribution.

For the final round $t = r$:
- Always play Defect (D). This is the dominant strategy regardless of previous history, as there are no future rounds to incentivize cooperation.

Edge cases:
- If $k \leq 1$: Always play D, as cooperation never yields a net positive return.
- If $\lceil \frac{n}{k} \rceil > n$: Always play D, as the group size is insufficient to ever make cooperation rational under these parameters.
'''

description_OPPORTUNISTIC_7 = '''
**Strategy: Conditional Tit-for-Tat with Defection-Threshold**

Maintain a state variable `cooperation_threshold` (initialized to $n-1$) and a counter for the current round $t$.

**Round 1:**
Play `C` (Cooperate). This establishes cooperative intent and gathers baseline data on opponent behavior.

**Rounds $t \in [2, r-1]$:**
Let $S_{t-1}$ be the total number of cooperators observed in the previous round.
Let $c_{t-1}$ be your own action in the previous round ($1$ if `C`, $0$ if `D`).
The number of opponents who cooperated is $O_{t-1} = S_{t-1} - c_{t-1}$.

*   If $O_{t-1} \ge \text{cooperation\_threshold}$:
    Play `C`. Your cooperation is yielding enough social contribution to justify the cost relative to the return.
*   If $O_{t-1} < \text{cooperation\_threshold}$:
    Play `D` (Defect). Switch to defection to protect your private endowment.
    *   Increment `cooperation_threshold` by $1$ (maximum $n-1$) if your defection in the previous round did not result in total group collapse below previous levels, signaling that you are becoming more selective. If the group cooperation level drops significantly following your defection, reset `cooperation_threshold` to $O_{t-1} + 1$ to test for a lower-cooperation equilibrium that is still profitable.

**Final Round ($t = r$):**
Always play `D` (Defect). With no future rounds, there is no reputational or retaliatory incentive to contribute. The marginal gain of keeping the endowment is strictly superior to the marginal gain of the public good share in the final interaction.

**Dynamic Adjustment:**
If at any point $O_{t-1} == n-1$ (all opponents cooperated), reset `cooperation_threshold` to $n-1$ to maximize the probability of sustaining full group cooperation. If at any point $O_{t-1} == 0$, set `cooperation_threshold` to $n-1$ and play `D` for the next $\lceil r/4 \rceil$ rounds to punish the lack of cooperation before attempting to re-engage with a `C` action.
'''

description_OPPORTUNISTIC_8 = '''
### Opportunistic Tit-for-Tat with Defection Thresholds

The strategy operates on a conditional cooperative basis, utilizing a moving threshold to maximize personal payoff while penalizing consistent defectors. The logic relies on maintaining "good standing" with the group while aggressively defecting when the group cooperation level fails to meet a sustainable threshold.

**Initialization (Round 1):**
Always play **Cooperate**. This serves as a probe to gauge the baseline cooperation level of the population without immediately sacrificing potential shared gains.

**Subsequent Rounds (2 to r-1):**
Calculate the observed cooperation rate $S_{t-1} = C_{t-1} / (n-1)$, where $C_{t-1}$ is the number of opponents who cooperated in the previous round.

1.  **Strict Threshold Rule:**
    If $S_{t-1} \geq (1 / k)$, play **Cooperate**. Since $k$ is the multiplication factor, the threshold $(1/k)$ represents the break-even point where the marginal benefit of cooperation equals the cost of contribution. When the group supports this level, cooperation is the profit-maximizing choice.

2.  **Conditional Defection:**
    If $S_{t-1} < (1 / k)$, play **Defect**. This punishes the group for under-contributing, as the expected return on cooperation is less than the guaranteed return of keeping the endowment.

3.  **Exploitation/Recovery Logic:**
    If your previous move was **Defect** and the group cooperation rate $S_{t-1}$ increases by more than 20% compared to the prior round, play **Cooperate** in the current round. This acts as a signal to "re-warm" the relationship and re-establish the cooperative cycle if the group attempts to return to a higher-yield state.

**Final Round (Round r):**
Always play **Defect**. Regardless of the history or strategy, the incentive to free-ride is maximal in the final round as there are no future interactions to sustain cooperation.

**Pseudocode:**

```python
def decide_action(round_number, n, k, history):
    if round_number == 1:
        return Cooperate
    
    if round_number == r:
        return Defect

    # Get cooperation rate of opponents from last round
    # observed_cooperators_count is the total cooperation count minus 1 (if I cooperated) 
    # or the full count (if I defected)
    prev_opp_coop = history.get_last_opponents_cooperation_count()
    s_prev = prev_opp_coop / (n - 1)
    
    # Check if we should re-warm the relationship
    if history.last_my_action == Defect:
        if s_prev > (history.second_to_last_s_prev * 1.20):
            return Cooperate

    # Standard threshold logic
    if s_prev >= (1 / k):
        return Cooperate
    else:
        return Defect
```
'''

description_OPPORTUNISTIC_9 = '''
### Decision Rules

Define $S_t$ as the total number of cooperators in round $t$ (including yourself).

**Round 1:**
Cooperate ($c=1$). This establishes a baseline of cooperation and tests the propensity of opponents to contribute.

**Rounds 2 through $r-1$:**
Follow a "Conditional Tit-for-Tat" approach based on the observed public good production.

1.  **If $k \cdot S_{t-1} / n \ge 1$:**
    The previous round yielded a positive net return for cooperators (or at least broke even compared to defecting). Continue to cooperate ($c=1$).
2.  **If $k \cdot S_{t-1} / n < 1$:**
    The previous round resulted in a net loss for cooperators. Defect ($c=0$) to protect your endowment.

**Round $r$ (Final Round):**
Defect ($c=0$). Since there are no subsequent rounds to punish or reward, there is no strategic value in contributing. Maximize your final payoff by keeping your endowment.

### Edge Case Handling

*   **Initialization ($t=1$):** Always cooperate. Initial defection signals non-cooperation immediately, closing off potential mutually beneficial rounds.
*   **Total Defection by Opponents:** If $S_{t-1} = 0$, you must defect in the next round ($c=0$).
*   **Threshold Breaches:** If you defected in $t-1$ because of low returns but the *potential* returns (if everyone else had cooperated) suggest the group is viable, you may test cooperation again. If the group has historically shown low cooperation rates, remain in defection until the end.
*   **End-of-Game Horizon:** The strategy automatically switches to defection in the final round, effectively cutting ties regardless of previous cooperation levels.

### Opportunistic Logic

This strategy maximizes utility by shifting the burden of cooperation onto those willing to pay the cost, while reaping the benefits of the public good when it is profitable. By cooperating only when the group's collective behavior makes cooperation net-positive for the individual, the strategy avoids "sucker payoffs" while exploiting the high-cooperation phases of the group. The final-round defection ensures that no capital is wasted on future-oriented signaling that has no future.
'''

description_OPPORTUNISTIC_10 = '''
The strategy operates on a "Tit-for-Tat with a threshold" logic, designed to punish defectors while aggressively exploiting the public good when contribution levels are sufficiently high to generate a net positive return.

### Core Variables
*   `T`: The contribution threshold required for the player to cooperate. `T` is calculated as `ceil(n / k)`. This is the minimum number of contributors required for the public good return to be greater than or equal to the cost of contributing.
*   `my_c`: The action taken by this agent in the previous round (1 for C, 0 for D).
*   `opp_c`: The number of opponents who cooperated in the previous round.
*   `total_cooperators`: The total number of contributors in the previous round, calculated as `opp_c + my_c`.

### Strategy Logic

**Round 1:**
Play `C` (Cooperate) to signal willingness to cooperate and test the cooperative environment.

**Intermediate Rounds (2 ≤ t < r):**
If `total_cooperators` ≥ `T`:
    Play `C`.
Else:
    Play `D`.

**Final Round (t = r):**
Play `D` (Defect).

### Pseudocode
```python
def get_action(round_number, total_rounds, n, k, history):
    T = ceil(n / k)
    
    # Final round opportunistic defection
    if round_number == total_rounds:
        return "D"
    
    # First round initialization
    if round_number == 1:
        return "C"
    
    # Adaptive response to group behavior
    prev_round = history[-1]
    total_cooperators = prev_round.opp_c + prev_round.my_c
    
    if total_cooperators >= T:
        return "C"
    else:
        return "D"
```

### Strategic Rationale for Opportunism
1.  **Exploitation Avoidance:** The strategy only cooperates if the group meets the `T` threshold, ensuring that contributing never results in a net loss compared to defection. If the group fails to meet the threshold, the strategy immediately switches to `D` to avoid being a "sucker" while the group is under-contributing.
2.  **Coordination Signaling:** By cooperating in the first round, the strategy attempts to establish a cooperative equilibrium. It remains cooperative as long as the aggregate group behavior sustains the incentive.
3.  **Terminal Exploitation:** In the final round, the strategy always defects (`D`), as there is no future interaction to incentivize, allowing for a final gain without the risk of future retaliation.
'''

description_OPPORTUNISTIC_11 = '''
**Strategy: Threshold-Based Reciprocal Tit-for-Tat**

The strategy operates on a "conditional cooperation" mechanism, attempting to maximize short-term payoffs while enforcing long-term cooperation through conditional punishment. It assumes that if the public good is sufficiently profitable, cooperation can be sustained, but it immediately defects when it detects insufficient group cooperation.

**State Tracking**
- Maintain a variable `previous_cooperation_count` tracking the number of total cooperators in the previous round.
- Maintain a flag `is_punishing` (initially set to false).

**Decision Rules**

*   **Round 1:**
    Cooperate (C). This establishes a baseline of willingness to participate in the public good.

*   **Round 2 through r-1:**
    1. If `is_punishing` is true:
       - Defect (D) to avoid exploitation.
       - If `previous_cooperation_count` equals $n-1$ (the total number of players minus oneself), set `is_punishing` to false.
    2. If `is_punishing` is false:
       - Calculate the "Minimum Necessary Contribution" ($MNC$) to ensure that playing C is at least as profitable as playing D.
       - $MNC = \lceil n / k \rceil$.
       - If `previous_cooperation_count` $\ge MNC$:
         - Cooperate (C).
       - Else:
         - Defect (D).
         - Set `is_punishing` to true.

*   **Last Round (Round r):**
    Always Defect (D). Since there is no future round to incentivize or punish opponents, defecting maximizes the final payoff regardless of previous state.

**Pseudocode Logic**

```python
def get_action(round, total_players, multiplier, last_round_cooperators, is_punishing):
    if round == total_rounds:
        return 'D'
    
    if round == 1:
        return 'C'

    mnc = ceil(total_players / multiplier)

    if is_punishing:
        if last_round_cooperators >= (total_players - 1):
            is_punishing = False
            return 'C'
        else:
            return 'D'
    else:
        if last_round_cooperators >= mnc:
            return 'C'
        else:
            is_punishing = True
            return 'D'
```
'''

description_OPPORTUNISTIC_12 = '''
Initialize a state variable `cooperation_threshold` at $n/k$. 

In Round 1:
- Always play Cooperate (C).

In Rounds 2 through $r-1$:
- Observe the number of cooperators from the previous round, $S_{t-1}$.
- If $S_{t-1} \ge \text{cooperation\_threshold}$, play Cooperate (C).
- If $S_{t-1} < \text{cooperation\_threshold}$, play Defect (D).
- Additionally, if the previous action was Defect (D) and current cooperators $S_{t-1} \ge \text{cooperation\_threshold}$, switch to Cooperate (C) to test for potential re-establishment of cooperation.

In the final round $r$:
- If the number of cooperators in the previous round $S_{r-1} \ge n-1$, play Cooperate (C).
- Otherwise, play Defect (D).

Edge Cases:
- If `cooperation_threshold` is not an integer, round up to the nearest integer.
- If $n/k \ge n$ (i.e., $k \le 1$), the game is strictly dominant for Defection; in this scenario, play Defect (D) in every round.
'''

description_OPPORTUNISTIC_13 = '''
Start with unconditional cooperation in the first round to establish potential for mutual gain.

For all subsequent rounds $t \in \{2, \dots, r\}$, implement a "Conditional Reciprocity with Opportunistic Defection" strategy based on the observation of the total number of cooperators from the previous round ($C_{t-1}$):

1.  **Calculate the Cooperation Threshold ($T$):** Define the break-even threshold as $T = \lceil n/k \rceil$. This represents the minimum number of cooperators required for cooperation to yield a payoff equal to or greater than defection.

2.  **Evaluate Cooperation:**
    *   If $t = r$ (the final round): Defect ($D$). Since there is no future interaction to incentivize, maximize payoff immediately.
    *   If $t < r$: 
        *   If $C_{t-1} \ge T$: Cooperate ($C$). Reward the collective effort as long as the aggregate contribution ensures a net gain equivalent to or better than individual defection.
        *   If $C_{t-1} < T$: Defect ($D$). Punish the group for failing to maintain the threshold required for mutual benefit.

3.  **Handling History:**
    *   If $C_{t-1}$ consistently stays above $T$ for multiple rounds, maintain cooperation.
    *   If the group output drops below $T$, defect immediately in the next round to protect your private endowment.
    *   After defecting due to a drop below threshold, attempt to restart cooperation ("probe") every 3 rounds. If $C_{t-1} \ge T$ in the round immediately following a probe, resume conditional cooperation. If not, continue defecting.

4.  **Pseudocode Summary:**
    ```python
    T = ceil(n / k)
    if round == r:
        return D
    if round == 1:
        return C
    if C_{prev} >= T:
        return C
    if round % 3 == 0: # Probe strategy
        return C
    return D
    ```
'''

description_OPPORTUNISTIC_14 = '''
Adopt a "Conditional Tit-for-Tat with a Greedy Exit" strategy.

Initialize internal state:
- `target_cooperators = ceil(n / k)`: The threshold of cooperators required to make contributing profitable (break-even or better).
- `last_round_cooperators`: Stores total cooperators from the previous round (excluding self, if applicable).

Decision Rules:

1.  Round 1: Play Defect (D). This establishes a baseline and prevents immediate exploitation.

2.  Round $t$ (where $1 < t < r$):
    Observe the number of cooperators from round $t-1$. Let $C_{t-1}$ be the total cooperators in the previous round.
    - If you played $C$ in round $t-1$:
        - If $C_{t-1} \geq target\_cooperators$: Play Cooperate (C).
        - If $C_{t-1} < target\_cooperators$: Play Defect (D).
    - If you played $D$ in round $t-1$:
        - If $C_{t-1} \geq target\_cooperators + 1$: Play Cooperate (C) (Transition to cooperation only if the group shows high collective resilience).
        - Otherwise: Play Defect (D).

3.  Round $r$ (Final Round): Play Defect (D) unconditionally.

Edge Cases:
- If `target_cooperators` > $n$, set `target_cooperators` = $n + 1$. This renders cooperation mathematically impossible as a rational choice, forcing permanent Defection.
- If $C_{t-1}$ equals $target\_cooperators$ exactly, the net gain from contributing is $\geq 0$. Playing $C$ here is acceptable to signal willingness to sustain the group.
'''

description_OPPORTUNISTIC_15 = '''
**Strategy: Conditional Tit-for-Tat with Defection-Threshold (CTFT-DT)**

**Core Logic**
The strategy maintains a target cooperation threshold. If the average cooperation rate of the group meets or exceeds the sustainability threshold required to make cooperation individually profitable, cooperate; otherwise, defect.

**Decision Rules**

1.  **Sustainability Threshold Calculation (S):**
    Calculate the minimum number of cooperators ($C_{min}$) required for cooperation to yield a payoff equal to or greater than defection. 
    Solving $0 + (k/n) \times C_{min} \ge 1 + (k/n) \times (C_{min}-1)$ simplifies to the requirement that the group cooperation count $C_{total} \ge n/k$.
    Set $S = \lceil n/k \rceil$.

2.  **Round 1:**
    Always Cooperate (C). This establishes a baseline of cooperation and tests the propensity of opponents to contribute.

3.  **Rounds 2 through (r-1):**
    Evaluate the previous round's total cooperation count ($C_{prev}$).
    *   If $C_{prev} \ge S$: Cooperate (C). Reward the group for maintaining a profitable environment.
    *   If $C_{prev} < S$: Defect (D). Switch to defection to avoid exploitation when the group fails to sustain the public good.
    *   *Correction Step:* If you defected in the previous round, you may "test" the water. If $C_{prev} < S$, but you observe a positive trend in cooperation (i.e., $C_{prev} > C_{prev-2}$), assume the group is moving toward cooperation and Cooperate (C).

4.  **Final Round (r):**
    Always Defect (D). In the final round, there is no future interaction to incentivize or punish, so the dominant strategy is to maximize the final period payoff by retaining the endowment.

**Edge Case Handling**
*   **Initialization/Trendless Data:** If $C_{prev} = 0$, immediately default to Defect (D) for all subsequent rounds, as the group has demonstrated a permanent lack of cooperative intent.
*   **Tie-Breaking:** If $C_{prev} = S-1$, apply a probabilistic "Forgiveness" factor. Cooperate (C) with probability $p = 0.2$ to signal a willingness to restart cooperation if the group was close to the threshold. If this fails to shift $C$ upward in the subsequent round, revert to hard Defection (D) for $N$ rounds before trying again.
'''

description_OPPORTUNISTIC_16 = '''
Define a threshold $T$ for the minimum number of cooperators required to justify cooperation. Calculate $T$ as the smallest integer such that cooperating yields a payoff greater than or equal to defecting, given the contribution of others. Since the payoff for defecting is $1 + (k/n) \times (\text{cooperators})$ and the payoff for cooperating is $0 + (k/n) \times (\text{cooperators} + 1)$, cooperation is rational if:
$(k/n) \times (\text{cooperators} + 1) \ge 1 + (k/n) \times (\text{cooperators})$
This simplifies to $(k/n) \ge 1$, which is impossible under the constraint $1 < k < n$. Therefore, unconditional cooperation is never strictly rational in a single round.

However, employ a Tit-for-Tat variant modified for $N$-player public goods to induce cooperation among rational agents.

**Decision Rules:**

*   **Round 1:** Play **Cooperate**. This signals a willingness to engage in reciprocal cooperation.
*   **Rounds 2 to $r-1$:**
    *   Let $S_{t-1}$ be the number of cooperators in the previous round.
    *   If $S_{t-1} \ge \text{target}$, where $\text{target} = \lceil n \times (1 / k) \rceil$, play **Cooperate**.
    *   Otherwise, play **Defect**.
*   **Round $r$ (Last Round):** Play **Defect**. Without future rounds to punish defection, there is no strategic incentive to sustain public good contributions.

**Pseudocode:**

```python
target = ceil(n / k)

if current_round == 1:
    return Cooperate
elif current_round == r:
    return Defect
else:
    # Observe previous round cooperation count (S_prev)
    if S_prev >= target:
        return Cooperate
    else:
        return Defect
```

**Edge Case Handling:**

*   **Initial Defection:** If $S_1 < \text{target}$, immediately defect in Round 2. This prevents exploitation by non-cooperative agents.
*   **Recovery:** If the population cooperation level drops below the target due to noise or transient defection, play Defect for one round to signal that the current contribution level is insufficient, then revert to Cooperate in the subsequent round only if the average cooperation level across the last two rounds is sufficiently high to suggest a return to mutual cooperation.
*   **Parameter Sensitivity:** If $k$ is very small (near 1), the required target approaches $n$. If the target is $n$, any single defector forces an immediate switch to Defect.
'''

description_OPPORTUNISTIC_17 = '''
**Strategy: Conditional Tit-for-Tat with Defection Anticipation**

**Initialization**
Set `trust_threshold = 0.5`. Initialize `round_count = 1` and `total_rounds = r`.

**Round 1**
Cooperate (C).

**Rounds 2 to r-1**
1. Let `observed_cooperators` be the total number of players who contributed in the previous round.
2. Let `self_contribution` be the action taken in the previous round (1 for C, 0 for D).
3. Calculate `others_cooperated = observed_cooperators - self_contribution`.
4. Calculate `cooperation_rate_of_others = others_cooperated / (n - 1)`.

Decision Rule:
If `cooperation_rate_of_others >= trust_threshold`, then Cooperate (C).
Else, Defect (D).

**The Final Round (r)**
Defect (D) regardless of history.

**Adaptive Trigger for Exploitation**
In any round `t < r`, if the observed `cooperation_rate_of_others` is strictly less than `(n-k)/n`, immediately shift to Defect (D) for the remainder of the game. This threshold represents the break-even point where individual defection yields a higher payoff than full cooperation.

**Edge Case Handling**
If at any point the `total_rounds` is unknown or effectively infinite, treat the game as a rolling horizon where `trust_threshold` increases by `0.05` every 10 rounds to become progressively less tolerant of non-cooperation. If `n` is small (e.g., n=2), reduce `trust_threshold` to `0.2` to account for high volatility in single-opponent behavior.
'''

description_OPPORTUNISTIC_18 = '''
Play Cooperate (C) in Round 1.

In subsequent rounds (t > 1), calculate the *marginal net gain* of cooperation based on the observed total cooperation $C_{t-1}$ from the previous round. The payoff difference $\Delta\pi$ between defecting and cooperating is defined by:
$\Delta\pi = \pi_{defect} - \pi_{cooperate} = 1 - \frac{k}{n}$

To maximize opportunistic gains, assess the "Average Trust Level" ($T$) of the group, defined as the moving average of total cooperators across all previous rounds $1$ through $t-1$.

Decision Rule for Round $t$:
1. If $t = r$ (the final round), play Defect (D) unconditionally.
2. If $t < r$, compare the marginal benefit of group cooperation against the temptation to defect:
   - If the observed number of cooperators in the previous round ($C_{t-1}$) is greater than or equal to $n \times (1 - \frac{1}{k})$, play Cooperate (C). This threshold identifies the point where group cooperation yields a return on contribution $\ge 1$, making cooperation individually rational relative to the baseline of 1.
   - If $C_{t-1}$ is below the threshold, play Defect (D) to avoid exploitation.

If, after playing D, the observed cooperation $C_t$ increases by at least $20\%$ in the next round, reset the strategy by playing C for one round to test the group’s propensity for conditional cooperation. If $C_t$ remains stagnant or declines, continue playing D until the final round.
'''

description_OPPORTUNISTIC_19 = '''
### Strategy: Conditional Reciprocal Opportunism

**Decision Logic**

The strategy operates on a "Tit-for-Tat with a Threshold" mechanism, adjusted to maximize short-term utility while hedging against exploitation in the final rounds. Let $C_t$ be the number of cooperators observed in round $t$. Let $n$ be the total number of players and $k$ be the multiplication factor.

1.  **First Round ($t=1$):** Cooperate. This establishes goodwill and signals potential for cooperation, providing a baseline to measure the cooperativeness of the opponent pool.

2.  **Intermediate Rounds ($1 < t < r$):**
    *   Calculate the **Break-Even Threshold ($T$)**: This is the minimum number of cooperators required to make cooperation individually rational (i.e., payoff from cooperating $\geq$ payoff from defecting).
        *   Payoff if Cooperating ($P_c$): $(k/n) \times C_t$
        *   Payoff if Defecting ($P_d$): $1 + (k/n) \times (C_t - 1)$
        *   Cooperation is rational if $P_c \geq P_d \implies (k/n) \times C_t \geq 1 + (k/n) \times C_t - k/n$
        *   Simplifying, cooperate if the total contributions including yours results in a return $\geq 1$. Since this specific game formulation makes cooperation *always* strictly dominated (the net gain from contributing is $k/n - 1$, and since $k < n$, $k/n < 1$), the "opportunistic" threshold is purely empirical.
    *   **Decision Rule:** Cooperate in round $t$ if and only if $C_{t-1} \geq \lceil n \times (n/k) \rceil$ is *not* required; instead, use a **Reciprocity Trigger**:
        *   If $C_{t-1} / (n-1) \geq \theta$, then Cooperate.
        *   Where $\theta$ is the observed ratio of cooperation in the previous round, set $\theta = k/n$.
        *   If the ratio of cooperators in the previous round is $\geq k/n$, cooperate. Otherwise, Defect.

3.  **Final Round ($t=r$):** Defect. Regardless of history, the final round offers no opportunity for future reciprocity. The dominant strategy is to defect to secure the payoff from withholding the endowment without the risk of future retaliation.

**Handling Edge Cases**

*   **Initial Defection by Others:** If $C_{t-1} < k/n$ at any point after the first round, immediately switch to Defect for all subsequent rounds until the final round. If the population cooperates again in a later round (a "recovery"), re-engage with Cooperation only if the cooperation rate meets the threshold $\theta$ for two consecutive rounds.
*   **Total Defection Scenario:** If $C_t = 0$ for two consecutive rounds, permanently lock to Defect for all remaining rounds.
*   **Threshold Parameter:** If $k$ is small, the threshold for cooperation becomes high, making it harder to sustain cooperative behavior. If $k$ is close to $n$, the threshold is low, encouraging consistent cooperation unless others defect.

**Pseudocode**

```python
def get_action(round, total_rounds, history):
    # Rule for last round
    if round == total_rounds:
        return 'D'

    # Rule for first round
    if round == 1:
        return 'C'

    # Retrieve previous round cooperators (C_prev) from history
    c_prev = history.last_round_cooperators
    
    # Calculate cooperation ratio of opponents (n-1 players)
    ratio = c_prev / (n - 1)
    
    # Threshold condition
    if ratio >= (k / n):
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_20 = '''
**Strategy: Conditional Tit-for-Tat with Defection Anticipation**

The strategy operates on a "Reciprocal Conditional Cooperation" logic, aiming to maximize personal utility by fostering cooperation while preemptively defecting against the inevitable decline of group contribution in late-game scenarios.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate**. This establishes a baseline for potential mutual cooperation and tests the cooperative disposition of the group.

2.  **Subsequent Rounds ($t > 1$):**
    *   Let $C_{prev}$ be the total number of players who cooperated in the previous round ($t-1$).
    *   Calculate the "Cooperation Threshold" $T = \lceil n/k \rceil$. Since $1 < k < n$, the return on a single contribution is $k/n$. To break even or profit from cooperation, the total number of cooperators must be at least $\lceil n/k \rceil$.
    *   **Rule:** If $C_{prev} \geq T$, play **Cooperate**. This rewards group-level cooperation and incentivizes its continuation.
    *   **Rule:** If $C_{prev} < T$, play **Defect**. If the group is below the threshold required to make cooperation individually rational, contribution is purely loss-making; minimize loss by switching to defection.

3.  **Last Round ($t = r$):**
    *   **Rule:** Always play **Defect**. Regardless of history, in the final round, there is no future interaction to incentivize. Defection is the dominant strategy to capture the maximum immediate payoff.

**Edge Case Handling:**

*   **Sudden Drop in Cooperation:** If $C_{prev} \geq T$ for several rounds, and then in round $t$, $C_{prev}$ drops significantly but remains $\geq T$, continue to **Cooperate** to avoid a "noise-induced" collapse of cooperation. If $C_{prev}$ drops below $T$, trigger immediate **Defect**.
*   **Near-Threshold Fluctuations:** If $C_{prev}$ is consistently hovering near $T$, prioritize **Defect** if the trend of $C$ over the last 3 rounds is negative, or **Cooperate** if the trend is positive.
*   **Total Defection Start:** If $C_{prev} = 0$ in any round (other than the first), consider the group "non-cooperative" for the remainder of the game and permanently play **Defect**.

**Opportunistic Alignment:**

This strategy exploits cooperative environments by contributing when the return is positive ($k/n \times C_{prev} > 1$) and protects assets by defecting immediately when the group fails to sustain a profitable threshold or when the game enters its final stage where future incentives vanish. It is self-correcting: it builds a history of cooperation when profitable, but aggressively pivots to defection to avoid exploitation by free-riders.
'''

description_OPPORTUNISTIC_21 = '''
Initialize `trust_level` = 0.5. Define `cooperation_threshold` as $(1 - k/n) / (k/n)$. This threshold represents the critical number of other cooperators required to make the payoff of Cooperating ($C$) equal to the payoff of Defecting ($D$).

For each round $t \in \{1, \dots, r\}$:

1.  **First Round ($t=1$):** Cooperate. This establishes an initial signal of potential cooperation to build reciprocal value, while minimizing risk by testing the environment.

2.  **Subsequent Rounds ($t > 1$):**
    *   Let $N_c$ be the number of cooperators in round $t-1$ (excluding self).
    *   Let $S_{t-1}$ be the action taken in the previous round ($S_{t-1} = 1$ for $C$, $S_{t-1} = 0$ for $D$).
    *   Update `trust_level` using an exponential moving average: `trust_level` = $\alpha \cdot (N_c / (n-1)) + (1-\alpha) \cdot \text{trust\_level}$, where $\alpha \approx 0.2$.

    *   **Decision Rule:**
        *   If $t = r$: Defect. In the final round, the incentive to build future cooperation is zero, so maximize immediate utility.
        *   If `trust_level` $\times (n-1) \ge$ `cooperation_threshold` + 0.5: Cooperate. If the history suggests that the group is sufficiently cooperative to yield a positive net gain over defecting, reciprocate.
        *   If `trust_level` $\times (n-1) <$ `cooperation_threshold` + 0.5: Defect. If the group behavior is insufficient to justify cooperation, treat the game as a series of one-shot prisoner's dilemmas and defect to capture the free-rider payoff.

3.  **Opportunistic Adjustment:**
    *   If $S_{t-1} = D$ and $N_c$ is unexpectedly high ($N_c > (n-1) \times \text{trust\_level} + 1$), increase `trust_level` aggressively for the next round, as this signals a high probability of unobserved collective altruism.
    *   If the strategy defected in $t-1$ and realized a payoff $\pi > 1 + (k/n)$, transition to Cooperate in $t$ with probability $p = 0.1$, creating a "probing" mechanism to see if the group will shift toward mutual cooperation.
'''

description_OPPORTUNISTIC_22 = '''
Strategy: Threshold-Based Conditional Reciprocity

This strategy maintains cooperation as long as a critical mass of opponents reciprocates, but defects immediately upon detecting exploitation. The strategy relies on maintaining a "Reputation-of-Cooperation" score for the group, denoted as $R$, initialized at 0.

Pseudocode:

```python
# Parameters:
# n: Number of players
# k: Multiplication factor
# r: Total rounds
# t: Current round index
# c_total_prev: Total number of cooperators in the previous round
# my_action_prev: Action taken by self in previous round (1 for C, 0 for D)

# Decision Rule:
if t == 1:
    # First round: Attempt to establish cooperation.
    action = Cooperate

elif t == r:
    # Final round: Defect to capture the final private endowment.
    action = Defect

else:
    # Calculate the number of opponents who cooperated in the previous round.
    # Adjust for self-contribution.
    opponents_C = c_total_prev - my_action_prev
    opponents_total = n - 1
    
    # Calculate cooperation density of opponents
    density = opponents_C / opponents_total

    # Threshold for opportunistic cooperation:
    # The minimum density required to justify continuing cooperation is 1/k.
    # Below 1/k, cooperation yields a net loss compared to defection.
    threshold = 1.0 / k

    if density >= threshold:
        action = Cooperate
    else:
        action = Defect
```

Operational Logic:

1.  **Initialization:** In the first round, the strategy plays Cooperate to test the field. Since mutual cooperation maximizes individual payoff, it initiates the potential for a high-value equilibrium.

2.  **Conditional Reciprocity:** From round 2 to $r-1$, the strategy calculates the cooperation density of the group. The decision rule is derived from the payoff function: cooperation is individually rational if and only if the benefit received from others' contributions ($k \cdot C_{others} / n$) exceeds the cost of contributing ($1$). This simplifies to $C_{others} / (n-1) \ge 1/k$. By setting the threshold at $1/k$, the strategy ensures it only cooperates when the collective group size and contribution rate make cooperation profitable relative to defection.

3.  **Opportunism:** The strategy exploits the final round by defecting. Because there are no subsequent rounds to incentivize or punish, there is no strategic benefit to cooperation in the final step. It captures the private endowment ($1$) plus the public good share generated by others, maximizing the final payoff.

4.  **Reaction to Defection:** If the group fails to sustain a sufficient density of cooperators, the strategy triggers an immediate switch to Defect. It does not attempt to "forgive" or re-initiate cooperation unless the density returns to the profitable threshold in the subsequent round, effectively treating the group's cooperation as a prerequisite for its own contribution.
'''

description_OPPORTUNISTIC_23 = '''
The strategy utilizes a conditional "Win-Stay, Lose-Shift" logic extended to accommodate the continuous nature of public goods contributions. Since the goal is opportunistic—maximizing individual payoff while discouraging free-riding—the strategy operates as follows:

**1. Initialization (Round 1):**
Cooperate. This establishes a baseline for potential mutual cooperation, signaling an initial willingness to contribute without immediately revealing exploitable behavior.

**2. Subsequent Rounds (t > 1):**
Define the "Target Cooperation Threshold" ($T$) as $n/k$. This threshold represents the minimum number of cooperators required for cooperation to be payoff-neutral for an individual (i.e., where the benefit of contributing equals the cost).

Decision Rule:
*   **If** $(t = r)$: Defect. In the final round, the incentive to build future trust or punish defection vanishes; maximize immediate payoff by defecting regardless of past outcomes.
*   **If** $(t < r)$:
    *   **If** (Total cooperators in $t-1 \ge T$): Cooperate. Mutual cooperation is profitable or neutral; maintain this status.
    *   **If** (Total cooperators in $t-1 < T$): Defect. If the group is unable or unwilling to sustain a profitable public good, stop contributing to avoid being exploited.
    *   **Re-entry Trigger:** If the strategy is currently defecting because of low cooperation, inspect the last round. If the number of cooperators suddenly jumps to $\ge T$, switch back to Cooperate in the following round to "re-test" the group's willingness to sustain the public good.

**3. Opportunistic Adjustment:**
The strategy ignores the identity of defectors (since players are anonymous) and focuses solely on the aggregate cooperation count. It treats the group as a collective entity. If the group provides a return on investment ($\ge T$ cooperators), contribute. If the group provides a net loss, stop contributing to minimize losses and wait for the group to reset its behavior.

**Pseudocode:**
```python
if round == total_rounds:
    return Defect
if round == 1:
    return Cooperate

# T is the break-even point: n / k
threshold = n / k

if cooperators_previous_round >= threshold:
    return Cooperate
else:
    return Defect
```
'''

description_OPPORTUNISTIC_24 = '''
Play according to a "Win-Stay, Lose-Shift" logic scaled for an $n$-player environment, optimized to exploit cooperative environments while minimizing loss against exploiters.

### Core Logic
Your decision variable is whether the expected utility of cooperation exceeds the expected utility of defection based on the previous round's outcome.

**1. First Round (t=1):**
Cooperate (C). This establishes a baseline of goodwill to test the cooperation levels of other agents.

**2. Rounds t = 2 to r-1:**
Let $C_{t-1}$ be the total number of cooperators in the previous round.
Calculate the "Cooperation Threshold" $T_c = n/k$.
*   If $C_{t-1} \ge T_c$: Cooperate (C). The public good is generating a positive net return; reinforce the cooperative equilibrium.
*   If $C_{t-1} < T_c$: Defect (D). The public good is under-producing; switch to defect to maximize private payoff and avoid subsidizing non-contributors.

**3. Final Round (t=r):**
Defect (D). Since there are no future rounds to sustain, there is no reputational or retaliatory incentive to cooperate. Always play the dominant strategy to capture the maximum short-term surplus.

### Pseudocode Implementation
```python
def decide_action(t, r, n, k, last_round_cooperators):
    # Rule for final round
    if t == r:
        return 'D'
        
    # Rule for first round
    if t == 1:
        return 'C'
        
    # Standard decision logic
    threshold = n / k
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```

### Opportunistic Adjustments
*   **Threshold Sensitivity:** Because $1 < k < n$, the system inherently rewards defection at the individual level unless a significant portion of the group cooperates. The strategy treats the game as a series of conditional partnerships: if the collective is contributing enough to provide a return on investment ($k/n \times C_j > 1$, which simplifies to $C_j > n/k$), you participate. If not, you extract value by defecting.
*   **Last-Round Defection:** This is mandatory to prevent exploitation by agents who play "Always Cooperate" or "Tit-for-Tat" variants, ensuring you capture the final round's private endowment without the risk of future retaliation.
'''

description_OPPORTUNISTIC_25 = '''
In the first round, cooperate. In all subsequent rounds, monitor the total number of cooperators from the previous round, denoted as $C_{t-1}$.

Calculate your contribution decision for the current round $t$ based on the following rules:

1.  **If $t = r$ (the final round):**
    Always defect. The game ends, so there is no future incentive to maintain a cooperative reputation or punish others.

2.  **If $t < r$:**
    Calculate the threshold for reciprocity: $T = n/k$.
    *   If $C_{t-1} \ge T$, cooperate. This indicates that sufficient cooperative activity exists in the population to make mutual cooperation profitable or that the population is sustaining a cooperative equilibrium.
    *   If $C_{t-1} < T$, defect. This indicates that the current level of cooperation is insufficient to provide a positive return on your investment, signaling that exploiting the defectors or protecting your endowment is the rational opportunistic choice.

3.  **Special Edge Cases:**
    *   If you have observed only one round of play where $C_{t-1} \ge T$, cooperate.
    *   If your own previous action was Defect and you decide to return to Cooperation, do so only if $C_{t-1} \ge T$ and you have a "cooling off" period of one round of observation. If the population average cooperation remains below $T$, continue to defect until the signal changes.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, last_round_cooperators, n, k):
    # Rule 1: Always defect in the final round
    if round_number == total_rounds:
        return 'D'

    # Rule 2: First round cooperation
    if round_number == 1:
        return 'C'

    # Rule 3: Opportunistic Threshold Check
    threshold = n / k
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_26 = '''
The strategy, "Threshold Reciprocity," operates on the principle of conditional cooperation, maintaining high-yield coordination while proactively defecting when the collective contribution falls below the break-even point for the individual.

**Core Decision Logic**

Define $T_{min}$ as the minimum number of cooperators required for a contributor to achieve a payoff of at least 1 (the payoff of a defector in a scenario where zero contributions are made). Since the payoff for cooperating is $(k/n) \times (\text{Total Coops})$, cooperation is profitable relative to the baseline if $(k/n) \times (\text{Total Coops}) \ge 1$. Solving for total cooperators, the threshold is $T_{min} = \lceil n/k \rceil$.

In every round $t$, play according to the following state machine:

1. **Initial Phase (Round 1):**
   Start by playing $C$ (Cooperate) to test the cooperative potential of the group.

2. **Adaptive Phase (Rounds $2$ to $r-1$):**
   Let $C_{t-1}$ be the number of cooperators in the previous round.
   - If $C_{t-1} \ge T_{min}$: Play $C$. This reinforces stable, high-value cooperation.
   - If $C_{t-1} < T_{min}$: Play $D$. When the group fails to reach the critical mass required for individual payoff parity, switch to defection to avoid exploitation.
   - If the group returns to $C_{t-1} \ge T_{min}$ after a period of defection, resume playing $C$ in the next round. This allows for recovery if the group dynamics improve.

3. **Terminal Phase (Round $r$):**
   Play $D$ (Defect) regardless of previous history. In the final round, there is no future interaction to incentivize, and the dominant strategy is to maximize the immediate private endowment.

**Pseudocode**

```python
# Parameters: n, k, r
threshold = ceil(n / k)

def get_action(current_round, history):
    # 1. Terminal Phase
    if current_round == r:
        return 'D'
    
    # 2. Initial Phase
    if current_round == 1:
        return 'C'
    
    # 3. Adaptive Phase
    last_round_cooperators = history.last_round_total_coops
    
    # If I played C last round
    if history.my_last_action == 'C':
        if last_round_cooperators >= threshold:
            return 'C'
        else:
            return 'D'
            
    # If I played D last round
    else: # my_last_action == 'D'
        # Check if the total cooperators (including me potentially) 
        # would have crossed the threshold if I had cooperated.
        # Opponents_Coops = last_round_cooperators (since I played D)
        if (last_round_cooperators + 1) >= threshold:
            return 'C'
        else:
            return 'D'
```

**Edge Case Handling**
- **Low $k$ (where $n/k > n$):** If the threshold is mathematically impossible ($T_{min} > n$), the strategy defaults to $D$ for all rounds, as the public good structure is never profitable for the individual.
- **Fluctuating Groups:** The strategy treats the threshold as a strict boundary. It does not attempt to "punish" specific players, as individual identities are anonymous; it only responds to the aggregate incentive structure.
'''

description_OPPORTUNISTIC_27 = '''
**Strategy: Conditional Tit-for-Tat with Defection-First Threshold**

This strategy operates on the principle of conditional cooperation, maintaining an opportunistic stance by aggressively defecting when the collective contribution falls below a sustainability threshold, while rewarding mutual cooperation.

**State Variables:**
- `round_number`: Current round (1 to $r$).
- `cooperators_last_round`: Total count of cooperators observed in the previous round ($C_{t-1}$).
- `my_action_last_round`: Last action taken ($C$ or $D$).
- `threshold`: $(n/k)$, the minimum number of cooperators required for cooperation to be break-even for the individual.

**Decision Logic:**

1.  **Round 1:** Play $D$ (Defect). This establishes a baseline for opponent behavior without risking initial endowment in a potentially non-cooperative environment.

2.  **Rounds 2 to $r-1$:**
    *   If `cooperators_last_round` $\ge$ `threshold` AND `my_action_last_round` was $C$: Play $C$ (Cooperate). This sustains cooperative momentum when it is profitable to do so.
    *   If `cooperators_last_round` $\ge$ `threshold` AND `my_action_last_round` was $D$: Play $C$ (Cooperate). This acts as a "testing the waters" mechanism; if the group is strong enough to support cooperation, shift to $C$ to capture mutual gains.
    *   If `cooperators_last_round` < `threshold`: Play $D$ (Defect). If the group's cooperation level is insufficient to yield a positive return relative to defecting, cease cooperation immediately to protect endowment.

3.  **Final Round ($r$):** Play $D$ (Defect). Regardless of history, the final round offers no future incentives for maintaining cooperation; defecting maximizes the final payoff.

**Pseudocode:**

```python
def choose_action(round_number, cooperators_last_round, my_action_last_round, n, k, r):
    threshold = n / k
    
    if round_number == 1:
        return 'D'
    
    if round_number == r:
        return 'D'
        
    if cooperators_last_round >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_OPPORTUNISTIC_28 = '''
**Strategy: Conditional Conditional-Cooperation (CCC)**

The strategy functions as a dynamic threshold-based optimizer that approximates a Tit-for-Tat mechanism while prioritizing payoff maximization during the final round.

**Initialization:**
Set `Target_Cooperation_Rate` (TCR) = 0.5.
Set `State` = `Cooperative`.

**Round 1:**
Play `C` (Cooperate).

**Round 2 to Round (r-1):**
Observe `S_prev`, the number of cooperators in the previous round (excluding self).
Calculate `Observed_Cooperation_Rate` (OCR) = `S_prev / (n - 1)`.

If `OCR` >= `TCR`:
  Play `C`.
  `State` = `Cooperative`.
Else:
  Play `D` (Defect).
  `State` = `Defective`.

*Self-Correction Mechanism:* If `State` == `Defective` and `OCR` increases significantly (defined as `OCR_current` > `OCR_previous`), switch `State` to `Cooperative` and play `C` to attempt to rebuild trust/cooperation levels.

**Final Round (Round r):**
Regardless of previous history or state, play `D`.

**Edge Cases:**
*   **n=2:** If the opponent defects, immediately play `D` in the subsequent round. If the opponent switches back to `C`, play `C` immediately.
*   **Consistent Defection:** If `OCR` remains below 0.2 for three consecutive rounds, set `State` = `Defective` and play `D` for all remaining rounds except the final round, where `D` is already mandated.
*   **Threshold Adjustment:** After every 5 rounds, if `State` == `Cooperative` but average payoff is lower than the payoff of pure defection (`1`), increase `TCR` by 0.1 to tighten the requirement for cooperation.
'''

description_OPPORTUNISTIC_29 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Exploitation**

This strategy maintains an internal state variable `T`, representing the target threshold of cooperating peers required to justify cooperation. It operates based on the principle of "conditional mutualism": cooperate only when others demonstrate sufficient cooperativeness to make the collective action profitable or sustainable, while defecting immediately when the environment is hostile or terminal.

**1. Initialization**
Set `T = (n / k)`. This is the theoretical break-even point where your contribution yields a neutral return.

**2. Round 1**
Play `C` (Cooperate). This establishes a baseline of goodwill and probes the population for conditional cooperators.

**3. Subsequent Rounds (t > 1)**
Let `C_prev` be the number of cooperators observed in the previous round.
Let `n_opp = n - 1` be the number of opponents.

*   **Rule A: The Defection Trap (End-Game)**
    If `t == r` (the final round), play `D` (Defect). Since there is no future interaction to incentivize, the dominant strategy is to maximize the immediate private payoff.

*   **Rule B: Exploitation Check**
    If `C_prev` is high enough that defecting would be highly profitable but cooperating remains safe, maximize gain. If `C_prev > T`, play `C`. The high cooperation level signals a stable cooperative environment worth maintaining.

*   **Rule C: Retaliation and Reset**
    If `C_prev < T`, play `D`. This serves as a penalty for the group failing to reach the profitability threshold. If the group is not cooperating sufficiently, you must defect to avoid being the "sucker" who subsidizes the free riders.

*   **Rule D: Stochastic Recovery (The "Opportunistic Probe")**
    If you have defected for the last two rounds, there is a small probability `p = 0.1` that you play `C` in the next round, regardless of `C_prev`. This acts as an opportunistic test to see if the group has reset or if the environment has become more favorable, allowing you to re-enter a cooperative cycle if the others respond.

**Pseudocode Summary:**

```python
if round == total_rounds:
    return D

if round == 1:
    return C

if C_prev >= (n / k):
    return C

if last_action == D and previous_last_action == D:
    if random() < 0.1:
        return C

return D
```
'''

description_OPPORTUNISTIC_30 = '''
The strategy, named "Conditional Reciprocity with Opportunistic Defection" (CROD), operates on the principle of maintaining cooperation only as long as it yields a marginal return superior to defection, while maximizing individual gains during terminal phases.

### Decision Rules

For round $t \in \{1, \dots, r\}$:

1. **Round 1:** Play **Cooperate (C)**. This serves as an initial probe to assess the aggregate cooperation levels of the group.

2. **Rounds $2$ through $r-1$:**
   Let $C_{t-1}$ be the number of cooperators observed in the previous round.
   - Calculate the "Cooperation Threshold" ($T_c$): $T_c = \lceil \frac{n}{k} \rceil$.
   - If $C_{t-1} \geq T_c$, play **Cooperate (C)**. This maintains the cooperative equilibrium when the public good yield is sufficient to justify the investment.
   - If $C_{t-1} < T_c$, play **Defect (D)**. This triggers an immediate withdrawal of support when the group fails to sustain a profitable public good level, minimizing losses.

3. **Final Round ($r$):** Play **Defect (D)** unconditionally. Since there are no subsequent rounds to punish or reward, the "shadow of the future" vanishes, and the dominant strategy is to capture the private endowment while free-riding on any remaining cooperation.

### Pseudocode

```python
def play_round(round_number, total_rounds, n, k, last_round_cooperators):
    # Threshold for profitable cooperation: 
    # Breaking even requires k * (total_cooperators) / n >= 1
    # total_cooperators >= n / k
    threshold = ceil(n / k)
    
    # Final round opportunistic defection
    if round_number == total_rounds:
        return "D"
    
    # First round probe
    if round_number == 1:
        return "C"
    
    # Adaptive conditional response
    if last_round_cooperators >= threshold:
        return "C"
    else:
        return "D"
```

### Edge Case Handling

- **Sudden Collapse:** If the group cooperation level drops below the profitability threshold ($n/k$) at any point, the strategy immediately shifts to Defect (D). It will only resume cooperation if, in a subsequent round, the observed cooperation returns to or exceeds the threshold.
- **Threshold Sensitivity:** In scenarios where $k$ is close to 1, the threshold $T_c$ becomes very high (close to $n$), effectively making cooperation fragile and prone to frequent defection, which aligns with the strategy's opportunistic nature.
- **Ambiguity:** If the observed number of cooperators is exactly equal to the threshold, the strategy maintains Cooperation (C) to prevent a downward spiral.
'''

description_OPPORTUNISTIC_31 = '''
**Strategy: Conditional Tit-for-Tat with Defection-in-Last-Round**

**1. First Round (t=1)**
Cooperate (C) to establish the potential for mutual cooperation and to assess the baseline level of public goods contribution by the group.

**2. Rounds t = 2 to r-1**
Maintain a "Conditional Cooperation" rule based on the observed number of cooperators from the previous round (S_{t-1}).

*   Let C_{t-1} = S_{t-1} - 1 (the number of other players who cooperated in the previous round).
*   Define the "Break-even Threshold" (T) as the minimum number of contributors required for cooperation to be more profitable than defection:
    *   The payoff for cooperating is (k/n) * S.
    *   The payoff for defecting is 1 + (k/n) * (S-1).
    *   Cooperation is strictly better than defection if (k/n) * S > 1 + (k/n) * (S-1), which simplifies to k/n > 1. However, since k < n, individual cooperation usually yields a lower immediate return than defection (k/n < 1).
*   **Decision Rule:**
    *   If C_{t-1} ≥ n * (1 / (k - (k/n))), cooperate. (This calculation adjusts for the fact that you need enough *others* to cooperate to offset the loss of your private endowment).
    *   *Simplified heuristic:* If the total number of contributors (S_{t-1}) is high enough that the marginal benefit of the public good (k/n * S_{t-1}) exceeds the cost of contribution (1), cooperate. Otherwise, defect.
    *   If the strategy observes a sudden, significant drop in the number of cooperators compared to the previous average (indicating a trend toward defection), switch to Defect (D) immediately to minimize losses.

**3. Last Round (t = r)**
Defect (D). Since there are no future rounds to incentivize, there is no value in maintaining a cooperative reputation or enforcing conditional cooperation. Extract the maximum possible payoff by keeping the endowment while benefiting from any residual cooperation from other players.

**4. Opportunistic Edge Cases**
*   **Reciprocity Lag:** If the group shows consistent, high-level cooperation (S > n/k), continue to cooperate, even if the immediate payoff is slightly lower than defecting, to sustain the high-return environment.
*   **The "Sucker" Trap:** If the number of contributors drops to a level where the return is less than 1 (specifically, S < n/k), switch to Defect (D) in the subsequent round. Return to Cooperate (C) only if the total number of contributors in the previous round rises back above the threshold (S > n/k) for two consecutive rounds, to ensure the group has stabilized.
*   **Threshold Calculation:** If k/n is such that cooperation can *never* be profitable (specifically, if k < 1, though the prompt specifies k > 1), defect in every round. Given 1 < k < n, cooperation is only collectively rational, not individually rational, so utilize the opportunistic pivot to D whenever the collective contribution drops below the critical threshold required to make C profitable.
'''

description_OPPORTUNISTIC_32 = '''
Play Cooperate in round 1.

For all subsequent rounds $t \in \{2, \dots, r\}$, determine the action based on the observed history of cooperation from the previous round $t-1$:

Let $C_{total, t-1}$ be the total number of cooperators observed in round $t-1$.
Calculate the marginal return on cooperation ($MRC$) for the upcoming round:
If the number of cooperators in the previous round was $C_{total, t-1}$, the payoff difference between cooperating and defecting is:
$\Delta = \frac{k}{n} - 1$

If $t = r$ (the final round):
Play Defect regardless of history.

If $t < r$:
If $C_{total, t-1} \geq \lceil \frac{n}{k} \rceil$:
Play Cooperate. This threshold condition ensures that your contribution triggers a group outcome where the public benefit outweighs the private cost of the contribution.

If $C_{total, t-1} < \lceil \frac{n}{k} \rceil$:
Play Defect. This enforces a "tit-for-tat" style punishment mechanism, withholding cooperation when the collective contribution level is insufficient to justify the personal cost of investment.

Special Case: If $k \leq 1$, always play Defect in every round, as the dominant strategy is always to keep the endowment regardless of others' actions.
'''

description_INDIVIDUALISTIC_5 = '''
**Adaptive Reciprocal Threshold Strategy (ARTS)**

**Phase 1: Initial Rounds (t = 1 to 3)**
Play Cooperate (C) for the first three rounds to establish a baseline for cooperation and measure the aggregate contribution behavior of the opponents.

**Phase 2: Steady-State Decision Logic (t > 3)**
In every subsequent round, calculate the "Observed Contribution Rate" from the previous round (t-1). Let $C_{prev}$ be the number of cooperators observed in round $t-1$. Calculate the individualistic breakeven threshold $T$ for the current round, where $T = n/k$. 

Apply the following conditional logic:

1.  **Defection Trigger:** If $C_{prev} < T$, play Defect (D). The group is not contributing at a level that provides a positive net return on investment relative to keeping the endowment.
2.  **Reciprocal Cooperation:** If $C_{prev} \ge T$, play Cooperate (C). If the group sustains the threshold, continue to contribute.
3.  **Recovering Cooperation:** If the previous action was Defect and $C_{prev} \ge T$, play Cooperate (C) to test if the group will maintain the threshold.

**Phase 3: Final Rounds (t > r - 2)**
For the final two rounds, switch exclusively to Defect (D). Given the finite horizon and the inability to establish long-term reputation or punishment mechanisms, the dominant individualistic strategy shifts to maximizing the immediate payoff by keeping the endowment.

**Summary of Decision Rules:**
*   **t $\in \{1, 2, 3\}$:** Cooperate.
*   **t $\in \{4, \dots, r-2\}$:**
    *   If $C_{prev} < n/k$: Defect.
    *   If $C_{prev} \ge n/k$: Cooperate.
*   **t $\in \{r-1, r\}$:** Defect.
'''

description_INDIVIDUALISTIC_6 = '''
In Round 1, play C.

For rounds 2 through $r-1$, track the history of the aggregate cooperation count $C_{t-1}$. Let $C_{t-1}$ be the number of cooperators observed in the previous round.

Calculate the Cooperation Threshold $T$ as follows:
$T = \lceil \frac{n}{k} \rceil$

If $C_{t-1} \geq T$, play C.
If $C_{t-1} < T$, play D.

In the final round ($t = r$), play D regardless of previous outcomes.

If at any point a player observes a round where the total cooperation count $C$ drops from a value $\geq T$ to a value $< T$, initiate a "punishment phase" for exactly one round: play D, then resume the threshold-based logic in the subsequent round. If the punishment phase occurs in round $r-1$, this rule is overridden by the final round D condition.
'''

description_INDIVIDUALISTIC_7 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Reciprocity**

**1. Strategy Definition**
The strategy is defined by three phases: Initialization, Maintenance, and Termination. The decision to cooperate ($C$) or defect ($D$) depends on the aggregate number of cooperators from the previous round ($S_{t-1}$), where $S$ is the count of other players who chose $C$. Let $n$ be the total number of players and $S_{t-1}$ be the number of cooperators observed in the previous round.

*   **Initialization (Round 1):** Play $C$ to signal cooperative intent and test the collective threshold.
*   **Maintenance (Rounds 2 to $r-1$):**
    *   Calculate the "break-even" threshold ($T$) required for cooperation to be individually rational relative to defection: $T = \lceil \frac{n}{k} \rceil$.
    *   If $S_{t-1} \ge T$: Play $C$.
    *   If $S_{t-1} < T$: Play $D$.
*   **Termination (Round $r$):** Play $D$ regardless of prior history.

**2. Decision Logic Pseudocode**
```python
def get_action(round_number, total_rounds, prev_round_cooperators, n, k):
    # Termination phase
    if round_number == total_rounds:
        return 'D'
    
    # Initialization phase
    if round_number == 1:
        return 'C'
    
    # Maintenance phase
    # Threshold T: Minimum cooperators needed to make contribution profitable
    # Payoff_C = (k/n) * (S + 1)
    # Payoff_D = 1 + (k/n) * S
    # Payoff_C >= Payoff_D  =>  (k/n)*S + k/n >= 1 + (k/n)*S
    # This inequality implies cooperation is strictly dominated if k < n.
    # Therefore, we use a "Tit-for-Tat" reciprocal threshold based on observed 
    # cooperation sustainability.
    
    threshold = ceil(n / k)
    
    if prev_round_cooperators >= threshold:
        return 'C'
    else:
        return 'D'
```

**3. Edge Cases**
*   **Non-integer thresholds:** If $\frac{n}{k}$ is not an integer, the threshold $T$ is rounded up ($\lceil \frac{n}{k} \rceil$). If this value exceeds $n-1$ (the maximum possible number of other cooperators), the threshold is effectively set to $n$, implying cooperation is never individually rational, triggering constant defection.
*   **All-Defect History:** If $S_{t-1} = 0$, the condition $0 \ge T$ will always be false, forcing an exit to $D$.
*   **Re-entry (Optional):** If the system observes a resurgence of cooperation after a period of defection (i.e., $S_{t-1} \ge T$ after a period where $S < T$), the strategy reverts to $C$ to re-engage with the cooperative group, provided $t < r$.
'''

description_INDIVIDUALISTIC_8 = '''
**Strategy: Adaptive Threshold Tit-for-Tat (ATTT)**

The strategy relies on a dynamic threshold of cooperation to incentivize group participation while protecting against exploitation. 

**Decision Rules:**

1.  **First Round:** Play **Cooperate (C)**. This initiates the potential for mutual cooperation and tests the propensity of opponents to contribute.

2.  **Subsequent Rounds (t > 1):**
    Calculate the cooperation rate of opponents in the previous round ($t-1$):
    $C_{opponents, t-1} = \frac{\sum_{j \neq i} c_j}{n-1}$

    Define the "Break-Even Cooperation Rate" ($C_{break-even}$) required for cooperation to be payoff-neutral compared to defecting:
    $1 + \frac{k}{n} \times (\text{Total Contributions}_D) = \frac{k}{n} \times (\text{Total Contributions}_C)$
    Solving for the number of cooperators ($N_c$):
    $1 + \frac{k}{n} \times N_c = \frac{k}{n} \times (N_c + 1)$
    $1 = \frac{k}{n}$
    Since $1 < k < n$, full cooperation is always socially optimal, but the individual incentive is to defect. Therefore, the strategy targets a cooperation threshold $T$ defined by the multiplier $k$:
    $T = \frac{n}{k}$

    **Action Logic:**
    *   **If** $C_{opponents, t-1} \geq \frac{T}{n}$, play **Cooperate (C)**.
    *   **If** $C_{opponents, t-1} < \frac{T}{n}$, play **Defect (D)**.

3.  **Last Round (t = r):**
    Play **Defect (D)** regardless of history. Since there are no future rounds to influence or coordinate, the incentive to preserve collective cooperation vanishes, and the dominant strategy is to maximize the final round payoff.

**Pseudocode:**

```python
def decide_action(t, r, n, k, history):
    if t == r:
        return D
    
    if t == 1:
        return C
    
    # Calculate previous round outcome
    prev_total_cooperators = history[-1].total_cooperators
    
    # Determine if I cooperated last round
    my_last_action = history[-1].my_action
    
    if my_last_action == C:
        prev_opp_cooperators = prev_total_cooperators - 1
    else:
        prev_opp_cooperators = prev_total_cooperators
        
    prev_opp_rate = prev_opp_cooperators / (n - 1)
    
    # Threshold for reciprocating cooperation
    # Target is to sustain participation when return on investment > 1
    threshold = (n / k) / n 
    
    if prev_opp_rate >= threshold:
        return C
    else:
        return D
```

**Edge Cases:**
*   **Low Participation:** If the group fails to reach the threshold $T/n$, the strategy immediately switches to Defect to mitigate losses.
*   **Rebound:** If the strategy has defected due to low participation, it remains in the Defect state for the remainder of the game, as the loss of trust in the specific cohort is treated as irreversible given the anonymity constraint.
*   **Parameter Sensitivity:** As $k$ approaches $n$, the required threshold $T/n$ decreases, making the strategy more lenient toward cooperators. As $k$ approaches 1, the threshold increases, making the strategy more aggressive in defecting.
'''

description_INDIVIDUALISTIC_9 = '''
The strategy employs a conditional cooperative approach based on the observed aggregate contribution levels, utilizing a modified Tit-for-Tat mechanism optimized for N-player environments.

**Decision Rules**

1.  **First Round:** Cooperate (C).

2.  **Subsequent Rounds (2 through r-1):**
    Calculate the observed cooperation rate of the opponents in the previous round, $O_{t-1} = \frac{C_{total, t-1} - c_{i, t-1}}{n-1}$, where $C_{total}$ is the total number of cooperators observed.
    
    *   If $O_{t-1} \geq \frac{1}{k}$: Cooperate (C).
    *   If $O_{t-1} < \frac{1}{k}$: Defect (D).

    *Rationale:* Since the marginal return of cooperation to the individual is $\frac{k}{n}$, the group threshold required to make cooperation break-even for a cooperator (compared to defecting) is exactly $\frac{1}{k}$ of the total population. Contributing when the group average is above this threshold supports a collaborative equilibrium; defecting when the group average falls below it minimizes losses against non-contributors.

3.  **Final Round (Round r):** Defect (D).
    Regardless of history, defect in the final round to capture the private endowment without the risk of future retaliation or the need to incentivize future cooperation.

**Edge Cases and Adjustments**

*   **Low-k Sensitivity:** If $k \leq 1$, the strategy immediately defaults to Defect (D) for all rounds, as cooperation is strictly dominated by defection regardless of other players' actions.
*   **Total Defection:** If $C_{total, t-1} = 0$, the strategy defects (D) for all subsequent rounds.
*   **Round Reset:** If the strategy defects due to $O_{t-1} < \frac{1}{k}$, it attempts to "test" the group again after two consecutive rounds of defection. If the opponent cooperation rate $O$ remains below the threshold $\frac{1}{k}$ for two consecutive rounds, the strategy remains in Defect (D) mode permanently. If, however, the strategy defects but then observes a round where $O_{t-1} \geq \frac{1}{k}$, it will return to Cooperate (C) in the following round, effectively "forgiving" temporary drops in cooperation.
'''

description_INDIVIDUALISTIC_10 = '''
Strategy: Triggered Conditional Reciprocity with End-Game Defection

1. First Round (t=1):
   Play C.

2. Subsequent Rounds (1 < t < r):
   Calculate the Cooperation Ratio (CR) of the previous round:
   CR = (Number of Cooperators) / n.

   If CR ≥ (n / k), Play C.
   Otherwise, Play D.

   If your previous action was D, you must observe a "recovery" period. If the round immediately following your previous D resulted in a CR ≥ (n / k), you may return to C in the next round. If not, continue to Play D.

3. Final Round (t = r):
   Play D.

4. Edge Cases and Overrides:
   - If the number of cooperators in the previous round was 0, Play D.
   - If you detect that your own contribution was required to reach the threshold (i.e., CR was exactly (n / k) and you played C), you are permitted to play C again, provided the CR remains stable.
   - If at any point the game is sufficiently long (r > 20) and you have defected for more than 3 consecutive rounds due to low CR, check for "re-entry" by playing C once every 4 rounds to probe for cooperative shifts in the opponent pool. If this probe round results in a CR ≥ (n/k), resume the standard conditional logic; otherwise, revert to permanent D.
'''

description_INDIVIDUALISTIC_11 = '''
**Initial Round (t=1):** Cooperate.

**Subsequent Rounds (t > 1):**
Calculate the threshold of cooperation, $T$, required for the strategy to be profitable (i.e., where playing $C$ yields a higher payoff than playing $D$):
$(k/n) \times (C_{total}) \ge 1 + (k/n) \times (C_{total} - 1)$
This simplifies to $(k/n) \ge 1$, which is impossible given $1 < k < n$. Therefore, in a strictly single-round payoff sense, defection is always the dominant strategy. To maintain cooperation, rely on a Tit-for-Tat mechanism conditioned on the aggregate behavior of the group.

Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $M$ be the minimum number of cooperators observed in the previous round that you define as "sufficient cooperation." Calculate $M$ as $\lceil n/k \rceil$.

*   If $C_{t-1} \ge M$, cooperate.
*   If $C_{t-1} < M$, defect.

**Final Round (t=r):**
Defect. Since there are no subsequent rounds to incentivize future cooperation or punish current defections, the dominant strategy is to maximize the immediate payoff by keeping the endowment.

**Pseudocode:**

```python
if round == 1:
    return Cooperate
    
if round == r:
    return Defect

# Tit-for-Tat threshold logic
threshold = ceil(n / k)
if last_round_cooperators >= threshold:
    return Cooperate
else:
    return Defect
```
'''

description_INDIVIDUALISTIC_12 = '''
**Strategy: Conditional Tit-for-Tat with Defection Threshold (CTTD)**

The strategy is defined by three phases: Initiation, Response, and Termination.

**1. Initiation (Round 1)**
Play C (Cooperate). This establishes a baseline to observe the aggregate cooperation level of opponents without immediately inducing a race to the bottom.

**2. Response (Rounds 2 to r-1)**
Calculate the aggregate cooperation of opponents from the previous round $t-1$. Let $C_{prev}$ be the total number of cooperators in round $t-1$. 

Define the "Target Threshold" $T$ as $n/k$. This threshold represents the minimum number of cooperators required for cooperation to be break-even for an individual (where $\pi_C \geq \pi_D$).

*   If $C_{prev} \geq T$: Play C (Cooperate). Reward collective cooperation by contributing to the public good.
*   If $C_{prev} < T$: Play D (Defect). Retaliate against low cooperation levels to protect individual payoff and prevent exploitation.

*Self-Correction Mechanism:* If the strategy played D in round $t-1$ and the total cooperation $C_{prev}$ increases such that $C_{prev} \geq T$, switch to C in round $t$. If the strategy played C in round $t-1$ but $C_{prev} < T$, switch to D in round $t$.

**3. Termination (Final Round)**
Play D (Defect). Regardless of previous history or observed cooperation levels, play D in the final round $r$. This eliminates the risk of being exploited in a round where reciprocal punishment is impossible.

**Pseudocode:**
```python
if round == r:
    return D

if round == 1:
    return C

# Calculate threshold T (min cooperators needed for break-even)
T = n / k

if observed_cooperators_prev_round >= T:
    return C
else:
    return D
```
'''

description_INDIVIDUALISTIC_13 = '''
**Initial Strategy: Conditional Reciprocity with Sunset Clause**

1.  **First Round:** Cooperate (C). Establishing a baseline for cooperation tests the responsiveness of the group.

2.  **Subsequent Rounds (t < r):** 
    Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
    *   If $C_{t-1} \ge \tau$, Cooperate (C).
    *   If $C_{t-1} < \tau$, Defect (D).
    
    The threshold $\tau$ is dynamic:
    *   $\tau = \text{max}(1, \lceil \frac{n}{k} \rceil)$. This threshold represents the minimum number of cooperators required for the public good return ($k/n \times C$) to equal or exceed the opportunity cost of contributing (1). 
    *   If the group sustained cooperation at or above the break-even point for the previous $m$ rounds, reduce $\tau$ by 1 (down to a floor of 1) to foster stability.
    *   If the group failed to sustain cooperation, reset $\tau$ to the initial break-even calculation $\lceil \frac{n}{k} \rceil$.

3.  **Last Round (t = r):** Always Defect (D). In the final round, the incentive for future reciprocity is removed, making defection the dominant individual strategy to maximize the final payoff.

4.  **Resumption Logic:** If the strategy is currently defecting because the threshold $\tau$ was not met, observe the next round. If the total number of cooperators $C_{t}$ meets or exceeds $\tau$ again, return to Cooperate (C) in the subsequent round to attempt re-establishment of the cooperative equilibrium. If $C_{t}$ remains below $\tau$, continue to Defect (D).
'''

description_INDIVIDUALISTIC_14 = '''
**Strategy Definition: Conditional Tit-for-Tat with Defection Threshold (CTFT-DT)**

This strategy operates on the principle of conditional reciprocity while ensuring individual utility maximization in the final round. The strategy uses a "cooperation threshold" based on the observed contribution density of the group.

**Decision Variables:**
*   $T$: Contribution threshold, defined as $\lceil n/k \rceil$. If the number of contributors equals or exceeds $T$, the public good provides a net benefit greater than or equal to keeping the endowment.
*   $C_{t-1}$: Number of cooperators observed in the previous round.
*   $t$: Current round index.
*   $r$: Total number of rounds.

**Pseudocode Logic:**

```python
if t == 1:
    # Initial probe: cooperate to signal potential for cooperation
    action = COOPERATE
elif t == r:
    # Final round: purely individualistic rational choice
    action = DEFECT
else:
    # Standard rounds: conditional reciprocity
    if C_{t-1} >= T:
        action = COOPERATE
    else:
        action = DEFECT
```

**Operational Mechanics:**

1.  **First Round ($t=1$):** Always play **Cooperate**. This functions as a "warm-start" signal. It tests if the aggregate group behavior supports a cooperative equilibrium without assuming the existence of conditional cooperators.
2.  **Intermediate Rounds ($1 < t < r$):** Play **Cooperate** if and only if the number of cooperators in the previous round ($C_{t-1}$) was greater than or equal to $T$. This threshold $T = \lceil n/k \rceil$ is the "break-even" point: below this number of cooperators, the individual payoff from defecting is strictly higher than from cooperating. If the group fails to meet this threshold, the strategy immediately switches to **Defect** to minimize individual loss and punish free-riding, restarting the check only if a future round hits the threshold again.
3.  **Last Round ($t=r$):** Always play **Defect**. Since the game terminates, there is no future benefit to maintaining a cooperative reputation or enforcing conditional reciprocity. The dominant strategy in a finite, non-repeated game (or the final round of a repeated game) is to maximize the private payoff ($1 - c_i$).

**Edge Case Handling:**
*   **Stochastic Fluctuations:** If the group's cooperation levels oscillate around $T$, the strategy will naturally oscillate between $C$ and $D$. This is intentional; it protects the agent from exploitation during low-cooperation periods while re-engaging if the group demonstrates a stable cooperative tendency.
*   **Minimal $k$:** If $k$ is very small (near 1), $T$ approaches $n$. The strategy effectively becomes "Defect" after round 1, as the requirement for mutual cooperation is rarely met by anonymous agents.
*   **High $k$:** If $k$ is large, $T$ is small. The strategy becomes highly tolerant, continuing to cooperate even when only a few others contribute, maximizing long-term gains in high-incentive environments.
'''

description_INDIVIDUALISTIC_15 = '''
The strategy follows a conditional, history-dependent approach based on the "Pavlov" (Win-Stay, Lose-Shift) logic, modified to account for the threshold of cooperation necessary to make contribution profitable.

**Decision Logic**

Let $C_t$ be the total number of cooperators in round $t$ (including yourself). You cooperate in round $t$ if and only if your payoff in round $t-1$ satisfies the condition for cooperation, or if $t=1$.

1. **Round 1:** Always Cooperate.

2. **Subsequent Rounds ($t > 1$):**
   Calculate your payoff in round $t-1$, denoted $\pi_{i,t-1}$.
   *   If you played Cooperate ($c_{i,t-1} = 1$): Cooperate again if $\pi_{i,t-1} \ge \text{target}$, where $\text{target} = 1$. This implies you cooperate if the public good return ($k \times C_{t-1} / n$) is $\ge 1$. If $\pi_{i,t-1} < 1$, switch to Defect.
   *   If you played Defect ($c_{i,t-1} = 0$): Cooperate if $\pi_{i,t-1} > \text{threshold}$, where $\text{threshold} = 1$. This implies you switch to Cooperate if the public good return ($k \times C_{t-1} / n$) is $> 1$. If $\pi_{i,t-1} \le 1$, remain Defect.

**Threshold Calculation**

The condition $\pi_i \ge 1$ (the break-even point for cooperation) depends on the aggregate cooperation count $C_{t-1}$.
*   If you played Cooperate ($c_i = 1$): You receive $\pi_i = (k/n) \times C_{t-1}$. You continue cooperating if $(k/n) \times C_{t-1} \ge 1$, which simplifies to $C_{t-1} \ge n/k$.
*   If you played Defect ($c_i = 0$): You receive $\pi_i = 1 + (k/n) \times C_{t-1}$. You switch to cooperating if $1 + (k/n) \times C_{t-1} > 1$ (meaning the return from the public good is positive), or more strictly, if the potential for group coordination is high. To prevent exploitation, switch to Cooperate only if $C_{t-1} > n/k$.

**Edge Cases**

*   **Last Round ($t = r$):** Defect regardless of history. Because the game ends, there is no future punishment for defection, making Defect the dominant strategy for maximizing individual utility.
*   **Total Defection:** If $C_{t-1} = 0$ in any round, immediately Defect in the subsequent round, as there is no public good being generated.
*   **Tie-Breaking:** If the calculated return on investment is exactly equal to the cost of contribution ($C_{t-1} = n/k$), follow the previous action (maintain status quo).

**Pseudocode**

```python
if t == r:
    action = Defect
elif t == 1:
    action = Cooperate
else:
    # C_prev is observed total cooperators from last round
    # If I cooperated last: payoff = (k * C_prev) / n
    # If I defected last: payoff = 1 + (k * C_prev) / n
    
    threshold = n / k
    
    if last_action == Cooperate:
        if C_prev >= threshold:
            action = Cooperate
        else:
            action = Defect
    else: # last_action == Defect
        if C_prev > threshold:
            action = Cooperate
        else:
            action = Defect
```
'''

description_INDIVIDUALISTIC_16 = '''
**Strategy: Tit-for-Tat Triggered Conditional Cooperation (TTT-CC)**

**Round 1:**
Contribute (C).

**Subsequent Rounds (2 to r-1):**
Observe the total number of cooperators from the previous round (S_{t-1}). Let the number of opponents who cooperated be O_{t-1} = S_{t-1} - c_{t-1} (where c_{t-1} is your own contribution status: 1 for C, 0 for D).

Define a threshold for conditional cooperation: T = n - 1 (the maximum number of opponents). Determine the "Cooperation Density" (D_{t-1}) of opponents as (O_{t-1} / (n-1)).

If D_{t-1} ≥ (1/k), contribute (C).
If D_{t-1} < (1/k), defect (D).

**Edge Cases and Adjustments:**
1.  **Strict Defection Trigger:** If at any point the average contribution density of opponents falls below (1/k) for two consecutive rounds, switch to Defect (D) for the remainder of the game to minimize exploitation.
2.  **Recovery:** If you have switched to permanent Defect (D) due to the trigger, ignore it if you detect a "cooperation spike." If in any single round (O_{t-1} / (n-1)) > 0.8, reset strategy and contribute (C) for one round to test for reciprocity.
3.  **Final Round (Round r):** Defect (D). Since there is no future interaction to incentivize cooperation, the dominant individualistic strategy in the final round is to maximize immediate payoff regardless of historical cooperation.

**Pseudocode:**
```python
def decide_action(t, r, n, k, history):
    if t == 1:
        return C
    
    if t == r:
        return D
        
    # Check for sustained low cooperation from opponents
    if history.last_two_rounds_low_cooperation():
        return D
    
    # Calculate opponent cooperation density
    opp_coop_density = history.last_round_opponents_coop / (n - 1)
    
    # Cooperation condition
    if opp_coop_density >= (1 / k):
        return C
    else:
        return D
```
'''

description_INDIVIDUALISTIC_17 = '''
**Decision Logic:**

Initialize `reputation_score` to 0.5. 

**Round 1:**
Play **Cooperate (C)**.

**Round t (where 1 < t < r):**
Calculate the observed cooperation rate of the group from the previous round (t-1): 
`group_cooperation_rate = (total_cooperators_t-1 - contribution_t-1) / (n - 1)`

If `group_cooperation_rate` ≥ `threshold`, where `threshold` is defined as `1/k`:
    Play **Cooperate (C)**.
    Increment `reputation_score` by 0.05, capped at 1.0.

If `group_cooperation_rate` < `threshold`:
    Play **Defect (D)**.
    Decrement `reputation_score` by 0.1, floored at 0.0.

**Round r (Final Round):**
Play **Defect (D)** regardless of past history or performance.

**Conditional Logic for Reputation Recovery:**
If the strategy is currently playing Defect (D) due to a previous round’s low cooperation rate, monitor the `group_cooperation_rate` in the subsequent round. If the `group_cooperation_rate` rises to ≥ `threshold` *and* the `reputation_score` is ≥ 0.4, revert to **Cooperate (C)** in the following round. If `reputation_score` < 0.4, maintain **Defect (D)** for one additional round to test for sustained cooperation before reverting to **Cooperate (C)**.
'''

description_INDIVIDUALISTIC_18 = '''
**Strategy: Conditional Tit-for-Tat with Threshold Reciprocation**

This strategy operates on the principle of conditional cooperation: contribute if the collective effort indicates mutual benefit, and defect to protect the endowment when contribution levels signal exploitation.

**Decision Logic**

For each round $t \in \{1, \dots, r\}$:

1.  **Initialization ($t=1$):** Cooperate. This initiates a signal of willingness to participate in the public good.

2.  **Assessment ($t > 1$):**
    Calculate the cooperation threshold $\tau = \frac{n}{k}$.
    Let $S_{t-1}$ be the total number of cooperators observed in the previous round.
    *   If $S_{t-1} \ge \tau$: Cooperate.
    *   If $S_{t-1} < \tau$: Defect.

3.  **Terminal Round ($t = r$):** Defect. Regardless of history, play Defect in the final round to capture the private endowment, as no future rounds exist to incentivize continued cooperation.

**Pseudocode**

```python
# Parameters: n, k, r
threshold = n / k

def get_action(round_number, history):
    # Terminal phase
    if round_number == r:
        return D
    
    # Initiation
    if round_number == 1:
        return C
    
    # Conditional Reciprocation
    # history[-1] is the count of cooperators in the previous round
    if history[-1] >= threshold:
        return C
    else:
        return D
```

**Adaptive Logic:**
The threshold $\tau = n/k$ represents the break-even point for an individual contributor. Since the marginal return of cooperation is $k/n$, contributing is rational only if the total number of cooperators is $\ge n/k$. By defecting when aggregate cooperation falls below this efficiency threshold, the strategy automatically punishes low-cooperation groups while sustaining high-cooperation equilibria, effectively decoupling from irrational defection while exploiting opportunities when the group behaves efficiently.
'''

description_INDIVIDUALISTIC_19 = '''
The strategy employs a conditional "Trigger Tit-for-Tat" approach combined with a backward induction defection at the final round.

**Decision Rules:**

*   **Round 1:** Play **Cooperate (C)**. This establishes a baseline for cooperation and tests the propensity of opponents to contribute.
*   **Rounds 2 to r-1:**
    *   Let $N_c$ be the number of cooperators from the previous round (including yourself if you cooperated).
    *   Calculate the threshold for reciprocity: $T = \lceil n/k \rceil$. If $k$ is not an integer, round up the result of $n/k$ to determine the minimum number of cooperators required to make cooperation individually rational or sustainable.
    *   If the number of cooperators in the previous round is $\ge T$, play **Cooperate (C)**.
    *   If the number of cooperators in the previous round is $< T$, play **Defect (D)**.
*   **Round r (Final Round):** Always play **Defect (D)**. Since there are no subsequent rounds to sustain cooperative norms or punish future defection, maximizing the immediate private payoff is the dominant individualistic strategy.

**Pseudocode:**

```python
# Strategy for player i
threshold = ceil(n / k)

def get_action(round_number, prev_round_cooperators):
    if round_number == r:
        return D
    
    if round_number == 1:
        return C
    
    if prev_round_cooperators >= threshold:
        return C
    else:
        return D
```

**Edge Case Handling:**

*   **Initial Defection by Opponents:** If the strategy detects that cooperation levels fall below the threshold $T$ in any round, it immediately switches to **Defect (D)** and remains in that state for all subsequent rounds (excluding the final round, where defection is already guaranteed). It does not attempt to "forgive" opponents, as individualistic optimization dictates that continued cooperation in an environment of low contribution results in a net loss compared to defection.
*   **Threshold Calculation:** If $k/n$ is such that $k \le 1$, the threshold $T$ becomes impossible to satisfy or exceeds $n$. In this scenario, the strategy identifies the game as a pure Prisoner's Dilemma, and the decision rule defaults to **Defect (D)** for all rounds, as the public good return will never outweigh the private cost of contribution.
'''

description_INDIVIDUALISTIC_20 = '''
**Strategy: Conditional Reciprocal Tit-for-Tat**

The strategy operates on the principle of conditional reciprocity, establishing a "trust threshold" based on the aggregate behavior of opponents. Define $S_{t-1}$ as the number of cooperators observed in the previous round (excluding your own action).

**Decision Rules:**

1.  **First Round (t = 1):** Play Cooperate (C). This initiates a cooperative equilibrium, signaling willingness to participate in the public good.

2.  **Subsequent Rounds (t > 1 and t < r):** 
    *   If $S_{t-1} \ge \lceil (n-1) \times \frac{1}{k} \rceil$: Play Cooperate (C).
    *   If $S_{t-1} < \lceil (n-1) \times \frac{1}{k} \rceil$: Play Defect (D).

3.  **Last Round (t = r):** Play Defect (D). Since there are no future rounds, the incentive to maintain a cooperative reputation or punish future defection is non-existent. Defection maximizes the payoff in the final instance regardless of previous history.

**Edge Case Handling:**

*   **"Punishment" / Re-entry Protocol:** If you played Defect in round $t-1$ because the threshold was not met, and in round $t$, the number of cooperators ($S_t$) meets or exceeds the threshold $\lceil (n-1) \times \frac{1}{k} \rceil$, switch to Cooperate (C) in round $t+1$. This allows for the restoration of cooperation if the collective behavior improves.
*   **Threshold Calculation:** The threshold $\lceil (n-1) \times \frac{1}{k} \rceil$ is the minimum number of cooperators required to make the payoff of cooperating ($\frac{k \cdot (S_{t-1} + 1)}{n}$) equal to or greater than the payoff of defecting ($\frac{k \cdot S_{t-1}}{n} + 1$). By playing C only when this threshold is met, you ensure that cooperation is either profit-neutral or profit-positive relative to the defection payoff in the current round.

**Pseudocode:**

```python
def choose_action(round_number, total_rounds, history_cooperators, n, k):
    if round_number == total_rounds:
        return "D"
    
    if round_number == 1:
        return "C"
    
    threshold = ceil((n - 1) / k)
    last_round_cooperators = history_cooperators[round_number - 2]
    
    if last_round_cooperators >= threshold:
        return "C"
    else:
        return "D"
```
'''

description_INDIVIDUALISTIC_21 = '''
Strategy: Conditional Reciprocity with Retaliation and Defection Thresholds

1. Initialization (Round 1): Cooperate (C).

2. Subsequent Rounds (2 ≤ t < r):
   Let C_obs be the number of cooperators observed in the previous round (t-1).
   Let my_action_{t-1} be the action taken by me in the previous round.

   - If my_action_{t-1} = C:
     - If C_obs ≥ (n * (1 - k/n)) / (k/n), specifically C_obs ≥ n / k: Cooperate (C).
     - Otherwise: Defect (D).
   - If my_action_{t-1} = D:
     - If C_obs ≥ (n / k) + 1: Cooperate (C) (Forgiveness/Attempt to restart cooperation).
     - Otherwise: Defect (D).

3. Final Round (t = r):
   Defect (D).

Edge Cases:
- If the game parameters allow for a total contribution C_obs such that the public good return is strictly less than the cost of private retention, prioritize Defection (D) regardless of history.
- In the event of ties or ambiguity where the decision threshold is met exactly, choose the action that maximizes individual payoff based on the expectation of opponent behavior derived from the trend of the previous three rounds.
- If the calculated cooperation threshold (n/k) is greater than n, always Defect (D), as cooperation is mathematically dominated by defection for all players.
'''

description_INDIVIDUALISTIC_22 = '''
**Strategy: Conditional Tit-for-Tat with Defection-on-Threshold (CTFT-DT)**

This strategy operates on the principle of conditional reciprocity while protecting individual payoff against systemic exploitation. It utilizes a moving target of cooperation based on the total cooperation count of the previous round.

### Initialization and Parameters
Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
Let $T$ be the threshold required to sustain cooperation. Set $T = \lceil n/k \rceil$. This threshold represents the minimum number of cooperators required to make the payoff of cooperation equal to or greater than the payoff of defection.

### Decision Rules

**Round 1:**
Cooperate (C). This establishes a baseline of cooperation to probe opponent willingness to engage in mutually beneficial behavior.

**Round $t$ (where $1 < t < r$):**
If $C_{t-1} \geq T$:
Play Cooperate (C).
Else:
Play Defect (D).

**Final Round ($t = r$):**
Defect (D). Given the finite horizon, there is no future round to incentivize opponents; defection is the dominant strategy to maximize the final round payoff regardless of opponent history.

### Pseudocode Representation

```
if t == r:
    return D

if t == 1:
    return C

threshold = ceil(n / k)

if observations_from_round(t-1).total_cooperators >= threshold:
    return C
else:
    return D
```

### Edge Cases and Robustness

*   **Systemic Defection:** If the group fails to meet the threshold $T$, the strategy immediately switches to Defect (D) to prevent the "sucker's payoff" and protect the individual endowment.
*   **Recovery:** If the group's cooperation count rises above $T$ in any subsequent round, the strategy resumes cooperation. This allows for self-correction if the group moves from an uncooperative state back to a cooperative equilibrium.
*   **High-Cooperation Environments:** If opponents are cooperative, the strategy effectively locks into a continuous cooperation loop, maximizing long-term gains.
*   **Ambiguous Parameters:** If $n/k$ results in a non-integer, the `ceil` function ensures the threshold is set to the lowest integer value where cooperation is strictly profitable ($\pi_C \geq \pi_D$).
'''

description_INDIVIDUALISTIC_23 = '''
**Strategy: Trigger-Based Conditional Contribution (TBCC)**

**Decision Rules:**

*   **Round 1:** Play **Cooperate (C)**. This establishes a baseline for cooperation and signals a willingness to engage in mutually beneficial behavior, provided the aggregate contribution ($S_{t-1}$) remains high.
*   **Rounds 2 through $r-1$:**
    *   If $S_{t-1} \geq \lceil n/k \rceil$, play **Cooperate (C)**. This threshold represents the minimum aggregate contribution required for cooperation to yield a net payoff greater than or equal to defection.
    *   If $S_{t-1} < \lceil n/k \rceil$, play **Defect (D)**. This serves as a punitive response to insufficient group cooperation.
    *   If a shift to **Defect (D)** was triggered in the previous round, you may return to **Cooperate (C)** only if the opponents demonstrate a return to the threshold contribution ($S_{t-1} \geq \lceil n/k \rceil$) for two consecutive rounds (a "forgiveness lag").
*   **Final Round ($r$):** Play **Defect (D)** unconditionally. Since there are no future rounds to incentivize cooperation through retaliation, the dominant strategy is to maximize the final period payoff by keeping the endowment.

**Handling Edge Cases:**

*   **Initial Defectors:** If $S_1 < \lceil n/k \rceil$, immediately switch to **Defect (D)** in Round 2. Do not return to **Cooperate (C)** unless the group sustains the required threshold for the defined forgiveness lag.
*   **Threshold Boundary:** If $\lceil n/k \rceil > n$, cooperation is mathematically impossible to make profitable for the individual. In this specific configuration, play **Defect (D)** in every round $t \in \{1, ..., r\}$.
*   **Noisy Cooperation:** If $S_{t-1} = \lceil n/k \rceil - 1$, continue to play **Defect (D)** unless there is an upward trend in $S$ over the last three rounds. If an upward trend exists, play **Cooperate (C)** once to test if the group is attempting to coordinate on the cooperative equilibrium. If the group fails to reach the threshold on that test, revert to **Defect (D)** immediately.
'''

description_INDIVIDUALISTIC_24 = '''
### Initial Strategy (Round 1)
Cooperate. Establishing cooperation early maximizes potential returns if other players are reciprocating.

### Decision Rules for Subsequent Rounds (Round 2 to r-1)
Let $C_{prev}$ be the number of cooperators observed in the previous round, excluding the self.
Let $I_{prev}$ be the self-action in the previous round ($1$ for Cooperate, $0$ for Defect).
Let $TotalC = C_{prev} + I_{prev}$ be the total cooperators in the previous round.

Calculate the net benefit of cooperation in the previous round ($B_{prev}$):
$B_{prev} = (\frac{k}{n} \times TotalC) - 1$

If $B_{prev} \geq 0$, play Cooperate.
If $B_{prev} < 0$, play Defect.

*Refined Decision Logic:*
Regardless of the calculation above, if $TotalC = 0$, play Defect. This prevents exploitation in an environment where no one is contributing.

### Final Round Strategy (Round r)
Play Defect. Since there are no future rounds to incentivize or punish opponents, maximizing the final round payoff is accomplished by keeping the endowment.

### Pseudocode Representation

```python
def get_action(round_num, total_rounds, n, k, prev_cooperators, self_prev_action):
    # Rule 1: Final round always defects to maximize absolute payoff
    if round_num == total_rounds:
        return "D"
    
    # Rule 2: First round always cooperates to test for reciprocity
    if round_num == 1:
        return "C"
        
    # Rule 3: Adaptive Tit-for-Tat logic based on public good efficiency
    total_c = prev_cooperators + (1 if self_prev_action == "C" else 0)
    
    # If no one contributed last round, defect to avoid waste
    if total_c == 0:
        return "D"
        
    # Calculate marginal benefit of contributing 1 unit
    # Benefit = (k/n) * (total_c) - 1
    # We contribute if the average utility of a C-state is non-negative
    marginal_benefit = (k / n) * total_c - 1
    
    if marginal_benefit >= 0:
        return "C"
    else:
        return "D"
```
'''

description_INDIVIDUALISTIC_25 = '''
Adopt a conditional cooperation strategy governed by the "Win-Stay, Lose-Shift" logic extended to threshold cooperation, designed to maximize individual utility while hedging against exploitation.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. This establishes an initial signal of cooperation, incentivizing potential cooperative clusters without assuming immediate defecting behavior.

2.  **Round 2 through (r-1):** Monitor the aggregate cooperation from the previous round, $S_{t-1}$ (the total number of cooperators in round $t-1$).
    *   If $S_{t-1} \geq \text{threshold}$, where threshold is defined as $\lceil n/k \rceil$: Play **Cooperate (C)**. This threshold is the point at which cooperation becomes individually rational (i.e., where contributing yields a payoff $\geq 1$, the payoff of defecting when no public good is produced).
    *   If $S_{t-1} < \text{threshold}$: Play **Defect (D)**. This switches to a retaliatory state because the current level of cooperation is insufficient to provide a net positive return on the investment of $1$.

3.  **Final Round (r):** Play **Defect (D)** unconditionally. Since there are no future rounds to sustain a cooperative equilibrium through reputation or reciprocity, the individualistic dominant strategy in the final round is to minimize personal expenditure.

**Adaptive Refinement:**

Maintain a secondary "cautious" state if the system detects unstable oscillation (e.g., if $S$ fluctuates around the threshold for two consecutive rounds). If oscillation occurs, immediately switch to **Defect (D)** for one round to reset the environment, then revert to the Decision Rules.

**Pseudocode:**

```python
threshold = ceil(n / k)

def get_action(round_number, history):
    # Rule 1: First Round
    if round_number == 1:
        return 'C'
    
    # Rule 3: Final Round
    if round_number == r:
        return 'D'
    
    # Rule 2: Adaptive Reciprocity
    # Get total cooperators from the previous round
    S_prev = history[round_number - 1]
    
    if S_prev >= threshold:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_26 = '''
### Tit-for-Tat with Threshold Cooperation

**Round 1:**
Cooperate ($C$). This establishes a baseline of willingness to contribute.

**Rounds 2 through $r-1$:**
Calculate the target contribution threshold $T$, defined as $\lceil \frac{n}{k} \rceil$.
Let $C_{prev}$ be the total number of cooperators from the previous round.

*   **Rule 1 (Retaliation):** If the total number of cooperators in the previous round ($C_{prev}$) is strictly less than $T$, play Defect ($D$).
*   **Rule 2 (Reciprocation):** If $C_{prev} \geq T$, play Cooperate ($C$).

**Round $r$:**
Play Defect ($D$). Since there are no future rounds to influence, the dominant strategy is to maximize the final round payoff by keeping the private endowment.

**Edge Cases:**
*   **If $n \leq k$:** The game ceases to be a social dilemma (cooperation is dominant). Play Cooperate ($C$) for all rounds.
*   **If you played $D$ in the previous round:** If the group cooperates at a level of $C_{prev} \geq T$, you may "forgive" the group and switch back to Cooperate ($C$) in the current round. If $C_{prev} < T$, continue to Defect ($D$).
'''

description_INDIVIDUALISTIC_27 = '''
Execute the following logic in each round *t* ∈ {1, 2, ..., *r*}:

**Round 1:**
Contribute (C). Establishing a baseline of cooperation is necessary to identify if other agents are reciprocators.

**Rounds 2 through *r*-1:**
Calculate the "Cooperation Threshold" for the previous round *t-1* as follows:
Let *S* be the number of cooperators in round *t-1*.
Let *s* be the number of cooperators excluding yourself (*S - 1* if you played C; *S* if you played D).
The strategy is: Cooperate (C) if *s* ≥ (*n*-1) / 2. Otherwise, Defect (D).

*Adjustment for non-reciprocity:* If you played D in round *t-1* and the number of cooperators *S* was ≥ (*n* * (1/k)), switch back to C for round *t* to test for re-emergence of cooperative groups.

**Final Round *r*:**
Always Defect (D). Since there is no subsequent round to sustain a reputation or elicit future cooperation, the dominant individual strategy is to maximize the immediate payoff by keeping the endowment.

**Pseudocode:**

```python
if t == 1:
    action = C
elif t == r:
    action = D
else:
    # Observe previous round results
    S = cooperators_count_prev_round
    my_action_prev = my_action_prev_round
    
    # Calculate others' cooperation
    if my_action_prev == C:
        s = S - 1
    else:
        s = S
    
    # Decision logic
    if my_action_prev == D and S >= (n / k):
        action = C
    elif s >= (n - 1) / 2:
        action = C
    else:
        action = D
```
'''

description_INDIVIDUALISTIC_28 = '''
**Initial Phase (Round 1):**
Cooperate (C). This establishes a baseline for group contribution and tests the responsiveness of the other players.

**Adaptive Phase (Rounds 2 to r-1):**
Calculate the cooperation threshold $T$ required for cooperation to be payoff-neutral for an individual contributor:
$T = n/k$

Observe the number of cooperators from the previous round, $S_{t-1}$.
1. If $S_{t-1} \ge T$: Cooperate (C). This rewards the group for maintaining a level of cooperation that yields a positive expected value or breakeven return.
2. If $S_{t-1} < T$: Defect (D). This protects individual endowment when the aggregate contribution level is insufficient to yield a positive return on investment.

**Terminal Phase (Round r):**
Defect (D). In the final round, there are no future interactions, rendering conditional cooperation strategies (like "tit-for-tat") irrelevant. Given the incentive structure (where $k < n$, making defection the dominant strategy in a single-shot interaction), the rational action is to maximize the final round payoff by keeping the endowment.

**Pseudocode Summary:**
```
if t == 1:
    return C
if t == r:
    return D
threshold = n / k
previous_cooperators = observed_cooperators_from_round(t-1)
if previous_cooperators >= threshold:
    return C
else:
    return D
```
'''

description_INDIVIDUALISTIC_29 = '''
**Round 1:** Play **Cooperate (C)**.

**Subsequent Rounds (2 to r-1):**
Define the “Cooperation Threshold” as the minimum number of cooperators ($N_c$) required for cooperation to be rational (i.e., when the individual payoff from cooperating is greater than or equal to the payoff from defecting). This threshold is met when:
$0 + (k/n) \times N_c \ge 1 + (k/n) \times (N_c - 1)$
$ (k/n) \times N_c \ge 1 + (k/n) \times N_c - (k/n)$
$ 0 \ge 1 - (k/n)$
$ (k/n) \ge 1$

Since the game rules state $k < n$, $(k/n)$ is always less than 1. This means the individual payoff from defecting is always greater than cooperating, regardless of the number of cooperators. However, to incentivize mutual cooperation (the collective optimum), observe the trend in total cooperation from the previous round ($N_{c, t-1}$).

- If $N_{c, t-1} = n$: Play **Cooperate (C)**.
- If $n > N_{c, t-1} \ge \lfloor n/k \rfloor$: Play **Cooperate (C)**.
- If $N_{c, t-1} < \lfloor n/k \rfloor$: Play **Defect (D)**.

**Final Round (r):**
Play **Defect (D)** regardless of previous history.

**Pseudocode Logic:**

```
// Constants: n, k, r are given
// History: last_round_cooperators (total count from previous round)

if current_round == 1:
    return Cooperate

if current_round == r:
    return Defect

threshold = floor(n / k)
if last_round_cooperators >= threshold:
    return Cooperate
else:
    return Defect
```
'''

description_INDIVIDUALISTIC_30 = '''
Adopt a "Win-Stay, Lose-Shift" logic predicated on a threshold of cooperation, adjusted for the specific multiplication factor *k* and group size *n*.

**Decision Rule:**

1.  **First Round:** Play **Cooperate (C)**. This establishes a baseline of cooperation and tests the group's responsiveness.

2.  **Subsequent Rounds (t > 1):** Let $S_{t-1}$ be the total number of cooperators observed in the previous round.
    *   **Determine Expected Payoff:** Calculate the payoff difference between cooperating and defecting for the previous round: $\Delta\pi = \pi_{C, t-1} - \pi_{D, t-1}$.
        *   $\Delta\pi = -1 + k/n$.
    *   **Decision Logic:**
        *   If $S_{t-1} \ge \lceil n/k \rceil$, play **Cooperate (C)**.
        *   If $S_{t-1} < \lceil n/k \rceil$, play **Defect (D)**.

3.  **Last Round (r):**
    *   Regardless of the history, play **Defect (D)**. Because there are no future rounds to influence, the dominant individualistic strategy in the final interaction is to maximize immediate payoff by withholding contributions.

**Rationale for Threshold:**
The threshold $\lceil n/k \rceil$ represents the minimum number of cooperators required to make the act of cooperation yield an individual payoff at least equal to the payoff of defection. Since $1 < k < n$, the group provides a social benefit, but free-riding is individually rational unless a critical mass is met. This strategy effectively creates a "conditional reciprocator" stance that incentivizes group cooperation while protecting the player from exploitation in non-cooperative environments.

**Edge Case Adjustments:**
*   **Transition from Round r-1 to r:** Ignore the history-based trigger in the final round; override all previous logic to output **Defect (D)**.
*   **Tie-breaking:** If the calculation for the threshold is ambiguous due to floating-point rounding, always round up to the nearest integer to require a higher standard of group cooperation before committing your own contribution.
'''

description_INDIVIDUALISTIC_31 = '''
**Strategy: Tit-for-Tat with Probabilistic Defection Threshold**

**Round 1:**
Play Cooperate (C).

**Subsequent Rounds (t > 1):**
Observe the aggregate number of cooperators from the previous round (S_{t-1}). Let M_{t-1} be the number of cooperators among opponents in the previous round (S_{t-1} - c_{t-1}).

1.  **If M_{t-1} ≥ Threshold:**
    Play Cooperate (C).
    *Where Threshold = floor(n / k). This represents the minimum number of contributors required to make the payoff of cooperation at least as good as the payoff of defection.*

2.  **If M_{t-1} < Threshold:**
    Play Defect (D).

**The "Finality" Adjustment:**
In the final round (t = r), if the decision rule above indicates Cooperate, calculate the expected value of shifting to Defect. Since there are no future rounds to incentivize, strictly play Defect (D) in the final round regardless of previous history to maximize immediate payoff, unless the observed cooperation level in round r-1 was at or above the threshold n/k. If M_{r-1} ≥ (n/k) - 1, play Cooperate (C) as a final signal of conditional cooperation; otherwise, play Defect (D).

**Edge Cases:**
- If k is large enough that (k/n) > 1 (which violates the provided parameter constraint 1 < k < n, but for robustness), always play Cooperate (C).
- If the game state results in an impossible threshold (e.g., k=1), always play Defect (D).
- If n=2, the threshold (n/k) is effectively the trigger for the Prisoner's Dilemma logic; if the opponent cooperated previously, cooperate; otherwise, defect.
'''

description_INDIVIDUALISTIC_32 = '''
**Strategy: Adaptive Threshold Tit-for-Tat**

The strategy operates on the principle of conditional cooperation, maintaining cooperation only as long as it is profitable or necessary to incentivize others to cooperate.

**Decision Rules:**

Define $C_t$ as the number of cooperators observed in round $t$.
Define $I_t$ as the number of *other* players who cooperated in round $t$. Since the player's own contribution $c_t \in \{0, 1\}$, calculate $I_t = C_t - c_t$.

1. **Round 1 (Initialization):**
   Contribute ($c_1 = 1$). This signals willingness to cooperate and initiates the potential for mutual benefit.

2. **Rounds 2 to $r-1$ (Adaptive Phase):**
   Cooperate ($c_t = 1$) if and only if the observed contribution rate of opponents in the previous round exceeds the breakeven threshold.
   
   The breakeven threshold $T$ is calculated as:
   $T = n/k$
   
   Decision rule:
   If $C_{t-1} \geq T$: Cooperate ($c_t = 1$)
   If $C_{t-1} < T$: Defect ($c_t = 0$)

   *Exception:* If the player defected in $t-1$ but observes that the total contributions $C_{t-1}$ were sufficient to make cooperation profitable for the *next* round (i.e., $C_{t-1} + 1 \geq T$), attempt to "re-enter" cooperation by playing $c_t = 1$ to signal a reset.

3. **Round $r$ (Final Round):**
   Always defect ($c_r = 0$). Because there is no subsequent round to incentivize or punish, there is no strategic benefit to cooperation. The dominant strategy is to maximize the payoff by keeping the endowment.

**Edge Case Handling:**

*   **Small Sample/No Data:** If $n$ is very small or the contribution threshold $T$ is effectively impossible to reach (e.g., $k$ is very close to 1), default to Defect ($c_t = 0$) immediately after Round 1.
*   **Constant Defection:** If the player observes $C_{t-1} = 0$ for two consecutive rounds, assume the population is non-cooperative and switch to permanent Defection ($c_t = 0$) for the remainder of the game to minimize personal losses.
*   **Threshold rounding:** If $n/k$ is not an integer, use the ceiling: $T = \lceil n/k \rceil$. This ensures that cooperation is only engaged when it yields a net positive return.
'''
