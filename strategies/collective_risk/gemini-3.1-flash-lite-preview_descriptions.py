"""
Strategy descriptions for collective_risk.

Generated with:
- Provider: Client
- Model: gemini-3.1-flash-lite-preview
"""


description_COLLECTIVE_1 = '''
Initialize `history` as an empty list to track the number of cooperators per round. Define `threshold_met` as a boolean, true if cooperators ≥ `m`.

**Round 1:**
Play `C` if `m/n` is less than 0.5. Otherwise, play `D`.

**Subsequent Rounds:**
Calculate `cooperation_rate` as the average number of cooperators across all previous rounds divided by `n`.

1. **Reciprocity Trigger:**
   If `history` shows that in the previous round, the number of cooperators was ≥ `m` AND you played `D`, switch to `C` (if you were previously defecting). This acknowledges a successful threshold was reached despite your defection and invites stability.

2. **Threshold Sensitivity:**
   - If the number of cooperators in the previous round was < `m`:
     - If you played `C` and the threshold was failed, switch to `D` for the current round (a "punishment" or "resource conservation" phase to avoid wasting endowments).
     - If you played `D` and the threshold was failed, play `D` (continue to avoid wasting endowments).
   - If the number of cooperators in the previous round was ≥ `m`:
     - If you played `C` and the threshold was met, play `C` (maintain cooperation).
     - If you played `D` and the threshold was met, play `D` (exploit the success).

3. **Last Round Specialization:**
   If `current_round == r`:
   - If `m` cooperators are required and you observe a trend where the total cooperators are consistently `m-1`, play `C`.
   - Otherwise, play `D`.

**Decision Logic Pseudocode:**
```python
def decide_action(round_num, history, last_action, n, m, k, r):
    if round_num == 1:
        return 'C' if (m/n < 0.5) else 'D'
    
    if round_num == r:
        prev_cooperators = history[-1]
        if prev_cooperators == m - 1:
            return 'C'
        return 'D'

    prev_cooperators = history[-1]
    threshold_met = (prev_cooperators >= m)

    # Tit-for-Tat adaptation
    if threshold_met:
        # If the collective succeeded, reward them by cooperating
        # unless you were already exploiting, in which case continue exploiting
        return 'C' if last_action == 'C' else 'D'
    else:
        # If the collective failed, conserve resources
        return 'D'
```
'''

description_COLLECTIVE_2 = '''
Strategy: Threshold-Triggered Tit-for-Tat (TTT)

Decision Logic:

1. Initialization (Round 1):
   Play C (Cooperate) to signal willingness to participate in the collective effort.

2. Monitoring:
   Track the history of the number of cooperators ($N_c$) in every preceding round.

3. Iterative Decision Rule (Rounds 2 to r):
   Calculate the outcome of the previous round ($t-1$):
   *   If $N_c \ge m$, the collective goal was met. Cooperate (C) in the current round.
   *   If $N_c < m$, the collective goal failed. Defect (D) in the current round.

4. Recovery Mechanism (The "Reset" Protocol):
   If the strategy defects due to a previous failure ($N_c < m$), do not remain locked in defection indefinitely. Periodically attempt to restart cooperation to break potential cycles of mutual defection.
   *   Define an "Observation Window" $w = 2$ rounds.
   *   If the strategy is currently defecting, check if $N_c \ge m$ occurred in the *most recent* round. Even if the current state is "Defect," if $N_c \ge m$ in the immediately preceding round, switch to C.
   *   Otherwise, if the strategy has been defecting for $k$ consecutive rounds where $k$ is a multiple of 3, play C to probe for renewed cooperation from other players.

5. Edge Case - Final Round (Round r):
   *   If the strategy defected in the previous round ($r-1$) because $N_c < m$, continue to defect (D) in the final round to protect against potential exploitation.
   *   If the strategy cooperated in the previous round ($r-1$) because $N_c \ge m$, continue to cooperate (C) in the final round to ensure the threshold is met for the final payout.
'''

description_COLLECTIVE_3 = '''
The strategy employs a conditional "Threshold Trigger" mechanism, prioritizing the achievement of the threshold $m$ while punishing unilateral defection and maintaining a "Grim Trigger" for the final round.

**Initialization (Round 1):**
Cooperate. The initial cooperation signals an intent to coordinate for the collective benefit.

**Core Decision Logic (Rounds 2 to r-1):**
In each round $t$, calculate the number of cooperators from the previous round $t-1$, denoted as $C_{t-1}$.

1.  **Strict Coordination:**
    If $C_{t-1} \ge m$: Continue to Cooperate. The threshold is met, and the collective outcome is Pareto-superior to individual defection.
    If $C_{t-1} < m$: Defect. The threshold was not met, and continuing to cooperate while others defect yields a lower payoff than defection.

2.  **Adaptive Recovery (Threshold Sensitivity):**
    If the threshold was missed ($C_{t-1} < m$), monitor for a recovery signal. If the system observes $C_{t-1} = m - 1$ (the "near-miss" condition), switch to Cooperate in the subsequent round $t+1$ to attempt to push the group over the threshold. If $C_{t-1} < m - 1$ (a "total failure" condition), continue to Defect for one additional round before returning to the strategy in step 1.

**Terminal Decision Logic (Final Round $r$):**
In the final round $r$, discard the "Adaptive Recovery" logic. Evaluate the cumulative behavior of the group:
- If the group met the threshold ($C_{t-1} \ge m$) in the majority of previous rounds, Cooperate.
- If the group failed to meet the threshold ($C_{t-1} < m$) in the majority of previous rounds, Defect.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, prev_cooperators, m, n):
    if round_number == 1:
        return 'C'
    
    if round_number == total_rounds:
        # Final round logic: trust based on historical average
        if history_successful_rounds > (total_rounds / 2):
            return 'C'
        else:
            return 'D'

    # Core logic
    if prev_cooperators >= m:
        return 'C'
    elif prev_cooperators == m - 1:
        # Attempt to trigger the group over the threshold
        return 'C'
    else:
        # Penalty for low cooperation
        return 'D'
```
'''

description_COLLECTIVE_4 = '''
The strategy operates on a conditional mechanism designed to establish mutual cooperation while minimizing exploitation. It relies on a "trigger-threshold" logic that adapts based on the history of aggregate cooperation.

**1. Definitions and Initialization**
*   **Threshold:** Let $m$ be the required number of cooperators.
*   **Safety Buffer:** Define $S = \text{max}(1, \lceil \alpha \cdot (m - 1) \rceil)$ where $\alpha$ is a sensitivity parameter (e.g., 0.25). This buffer accounts for potential noise or minor deviations.
*   **Target:** The primary goal is to ensure at least $m$ players cooperate. As an individual, you play $C$ if the expected cooperation count is close to the threshold $m$.

**2. Decision Rules**
*   **Round 1:** Play $C$. This initiates a signal of cooperative intent.
*   **Subsequent Rounds ($t > 1$):**
    *   Let $N_{C, t-1}$ be the number of cooperators in the previous round.
    *   **Case A (Stable Cooperation):** If $N_{C, t-1} \ge m$, you play $C$. This reinforces the collective success.
    *   **Case B (Near Miss):** If $m - S \le N_{C, t-1} < m$, you play $C$. This signals support to reach the threshold, attempting to nudge the group toward success.
    *   **Case C (Failure/Defection):** If $N_{C, t-1} < m - S$, play $D$. This is the punishment phase. In the event of significant defection, the strategy shifts to $D$ to preserve resources until the group demonstrates a return to cooperative signals.
    *   **The "Re-entry" Rule:** If you are in the punishment phase (Case C) and the observed $N_{C, t-1}$ increases toward $m$ (e.g., $N_{C, t-1} \ge m - S$), switch back to $C$ in the following round to restart cooperation.

**3. Last Round Handling**
*   If $t = r$, ignore punishment phases. If the average cooperation rate across all previous rounds is $\ge \frac{m}{n}$, play $C$; otherwise, play $D$. This maximizes utility given that there is no future interaction to influence.

**4. Pseudocode**

```python
# Strategy for player i at round t
def play(round_index, history, n, m, k):
    if round_index == 1:
        return 'C'
    
    if round_index == r:
        avg_coop = calculate_average_coop(history)
        return 'C' if avg_coop >= (m / n) else 'D'
    
    last_round_coop = history.last_round.count_cooperators
    
    # Punishment logic: If total cooperation is too low, defect
    if last_round_coop < (m - S):
        return 'D'
    
    # Otherwise, maintain or resume cooperation
    return 'C'
```
'''

description_PROSOCIAL_1 = '''
**Strategy: Threshold-Dependent Conditional Cooperation (TDCC)**

The strategy relies on a trigger-based cooperation mechanism that seeks to reach the threshold $m$ while punishing unilateral defection and maintaining flexibility as the game approaches the final round.

**Decision Logic**

1.  **First Round:** Play **Cooperate (C)**. This signals a willingness to engage in prosocial behavior to meet the threshold $m$.

2.  **Subsequent Rounds ($t > 1$):**
    *   Let $N_{C, t-1}$ be the number of cooperators observed in the previous round.
    *   **Cooperate (C) if:**
        *   The threshold was met in the previous round ($N_{C, t-1} \geq m$) AND the number of cooperators was sufficient to suggest a stable cooperative environment ($N_{C, t-1} \geq m$).
        *   OR, the threshold was NOT met in the previous round ($N_{C, t-1} < m$), but the number of cooperators was strictly increasing or stable at a high level, indicating a collective learning process.
    *   **Defect (D) if:**
        *   The threshold was met in the previous round ($N_{C, t-1} \geq m$), but you observed that $N_{C, t-1} = m$. This targets situations where you are essential to the threshold; if the group is barely meeting the threshold, defecting (D) acts as a signal to see if others will compensate to maintain $m$. If the threshold is missed, revert to (C).
        *   The threshold was not met in the previous round ($N_{C, t-1} < m$) and the group size of cooperators has been stagnant or decreasing, indicating a failure to coordinate.

**Pseudocode**

```python
def decide(t, r, n, m, k, history):
    # Base Case: First round
    if t == 1:
        return 'C'

    # Retrieve previous round data
    prev_cooperators = history[t-1].num_cooperators
    
    # Analyze trends
    trend_improving = False
    if t > 2:
        if history[t-1].num_cooperators > history[t-2].num_cooperators:
            trend_improving = True

    # Main Decision Rules
    if prev_cooperators >= m:
        # If threshold met, test for 'free-rider' stability
        # If we are exactly at threshold, defect to signal
        if prev_cooperators == m:
            return 'D'
        else:
            return 'C'
            
    else: # prev_cooperators < m
        # If threshold not met, only cooperate if there is hope/growth
        if trend_improving or prev_cooperators > (m / 2):
            return 'C'
        else:
            return 'D'

    # Final Round Adjustment: Always Cooperate
    if t == r:
        return 'C'
```

**Edge Case Handling**

*   **Final Round ($t = r$):** Always play **Cooperate (C)**. Without future rounds to incentivize behavior, the social optimum is to prioritize reaching the threshold $m$ regardless of past defection, maximizing the aggregate payoff for the final round.
*   **Threshold Vulnerability:** If $N_{C, t-1} = m$, the strategy plays **Defect (D)**. This is a deliberate "test" of the group's cooperation resilience. If the group continues to meet the threshold despite this defection, it confirms high-level cooperative stability. If the group falls below the threshold, the strategy immediately reverts to **Cooperate (C)** in the subsequent round.
*   **Persistent Failure:** If $N_{C, t-1} < m$ for three consecutive rounds without an increase in $N_C$, assume the group is uncooperative. Play **Defect (D)** for the remainder of the game, only switching to **Cooperate (C)** for the final round.
'''

description_PROSOCIAL_2 = '''
### Strategic Framework: Conditional Threshold Reciprocity (CTR)

The strategy utilizes a conditional threshold approach that seeks to trigger collective cooperation by signaling willingness, then enforcing participation through tit-for-tat logic. It prioritizes achieving the threshold $m$ while minimizing exploitation.

**Decision Rules:**

1.  **Phase I: Initiation (Round 1)**
    *   Cooperate ($C$) if $m/n \leq 0.5$.
    *   If $m/n > 0.5$, defect ($D$) to avoid exploitation, as the threshold is too high to achieve without signaling from others.

2.  **Phase II: Threshold Tracking (Rounds 2 to $r-1$)**
    *   Let $c_{t-1}$ be the number of cooperators observed in the previous round.
    *   If $c_{t-1} \geq m$, continue to cooperate. The collective goal is met; maintain stability.
    *   If $c_{t-1} < m$ but $c_{t-1} > 0$:
        *   If you played $C$ in $t-1$, switch to $D$ for one round (a warning signal to punish free-riders).
        *   If you played $D$ in $t-1$, play $C$ (attempting to boost the count toward $m$).
    *   If $c_{t-1} = 0$:
        *   Play $D$. The environment is uncooperative; risking an endowment is irrational.

3.  **Phase III: Termination (Round $r$)**
    *   If $c_{r-1} \geq m$, cooperate ($C$).
    *   If $c_{r-1} < m$, defect ($D$). In the final round, there is no future to incentivize, and the probability of meeting the threshold is low if the group has failed to coordinate by this point.

**Pseudocode:**

```python
def choose_action(round_num, history, n, m, k):
    # Round 1
    if round_num == 1:
        return 'C' if m/n <= 0.5 else 'D'
    
    # Last Round
    if round_num == r:
        prev_cooperators = history[-1]
        return 'C' if prev_cooperators >= m else 'D'
    
    # Intermediate Rounds
    prev_cooperators = history[-1]
    last_action = my_actions[-1]
    
    if prev_cooperators >= m:
        return 'C'
    
    if prev_cooperators > 0:
        if last_action == 'C':
            return 'D' # Punishment/Warning
        else:
            return 'C' # Attempt to hit threshold
            
    return 'D' # Environment is defecting
```

**Edge Case Handling:**
*   **Failed Coordination:** If the threshold is never reached, the strategy collapses to $D$ after one round of failed initiation to preserve individual payoff.
*   **Threshold volatility:** If $c_{t-1}$ fluctuates around $m$, the strategy acts as a buffer: cooperating when the group is successful and pivoting to defecting only when the group fails to meet the threshold, effectively punishing the collective non-cooperation.
'''

description_PROSOCIAL_3 = '''
### The "Threshold-Sensitive Tit-for-Tat" Strategy

This strategy is defined by an aspiration to achieve the collective reward (k) while maintaining a defensive posture against sustained defection. It relies on a "threshold-trigger" mechanism that adjusts based on the observed collective cooperation count ($C_t$) in the previous round.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. This signals a willingness to engage in the collective effort from the start.

2.  **Rounds $t > 1$:**
    *   Let $C_{t-1}$ be the number of players who cooperated in the previous round.
    *   If $C_{t-1} \ge m$: Play **Cooperate (C)**. The collective goal is being met, and the social optimum is sustained.
    *   If $m - C_{t-1} = 1$: Play **Cooperate (C)**. In this state, your cooperation is the "swing vote" required to reach the threshold and trigger the reward ($k$).
    *   If $m - C_{t-1} > 1$: Play **Defect (D)**. The group is failing to reach the threshold even with your cooperation; switching to defection preserves your endowment until the group shows sufficient effort to warrant renewed cooperation.

**Special Case: Last Round ($r$):**
*   If $C_{r-1} \ge m-1$: Play **Cooperate (C)**. Regardless of whether the previous round met the threshold, if the group is within one vote of success, you provide the final contribution to ensure the collective reward is captured.
*   If $C_{r-1} < m-1$: Play **Defect (D)**. If the group effort is too low to reach the threshold even with your contribution, maximize your payoff by keeping the endowment.

**Pseudocode:**

```python
def choose_action(round_number, n, m, k, history):
    if round_number == 1:
        return 'C'

    prev_cooperators = history[-1].cooperation_count
    
    # Check for Last Round Opportunity
    if round_number == r:
        if prev_cooperators >= m - 1:
            return 'C'
        else:
            return 'D'

    # Standard Round Logic
    if prev_cooperators >= m:
        return 'C'
    elif prev_cooperators == m - 1:
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_4 = '''
### Threshold-Targeted Reciprocal Strategy (TTRS)

The strategy operates on the principle of conditional cooperation: contribute to the project only when the history suggests that doing so is necessary and effective to reach the cooperation threshold $m$, while simultaneously punishing non-cooperation to incentivize the group toward the efficient outcome.

**1. Decision Rules (Per Round $t$)**

Let $C_{t-1}$ be the number of players who cooperated in the previous round. 

*   **Round 1:** Play $C$ (Cooperate). This signals a willingness to coordinate.
*   **Rounds $t > 1$:**
    *   **Case A (Threshold Met):** If $C_{t-1} \ge m$:
        *   If you played $C$ in round $t-1$: Play $C$. 
        *   If you played $D$ in round $t-1$: Play $D$ (This is a "tit-for-tat" adaptation; if the group succeeds without you, maximize your private payoff).
    *   **Case B (Threshold Failed):** If $C_{t-1} < m$:
        *   If you played $C$ in round $t-1$: Play $C$. (This assumes the failure was due to insufficient participation, not a lack of effort).
        *   If you played $D$ in round $t-1$: Play $C$ with probability $p$, where $p$ is scaled by the remaining rounds to encourage re-engagement.

**2. Adaptive Refinement (The "Need-Based" Adjustment)**

To handle scenarios where the group is close to $m$ but failing, adjust based on the current round $t$:

*   **If $C_{t-1} = m-1$:** Regardless of previous action, play $C$. This is the "critical tipping point" rule: if the group is exactly one person short of success, prioritize the reward $k$ over the short-term gain of $1$.
*   **If $C_{t-1} < m-1$ and $t > (r/2)$:** If the failure to reach $m$ has persisted for more than two consecutive rounds, switch to $D$ for the remainder of the game. If the group cannot coordinate by the midpoint, the reward $k$ is likely unattainable, and individual payoff maximization becomes the rational fallback.

**3. Edge Cases**

*   **Final Round ($t = r$):** If the group successfully met the threshold ($C_{r-1} \ge m$) in the previous round, play $D$. Because the game ends, there is no future reputation to maintain, and defecting provides a higher individual payoff in the final state. If the threshold was not met in $r-1$, maintain the $C$ strategy if $C_{r-1} = m-1$ (attempting to capture the reward one last time), otherwise play $D$.
*   **"Free-Rider" Detection:** If the observed count of cooperators drops significantly while the threshold was previously met, immediately switch to $D$ for one round as a warning, then revert to $C$ only if the count stabilizes at $\ge m$.
'''

description_ALTRUISTIC_1 = '''
This strategy employs a "Conditional Threshold Reciprocity" model, designed to stabilize cooperation by mirroring the collective behavior observed in previous rounds while maintaining a buffer against exploitation.

### Decision Rules

Define $N_c(t)$ as the number of cooperators observed in round $t$.
Define $S(t) = \sum_{j=1}^{t-1} N_c(j)$ as the cumulative number of cooperations observed across all previous rounds.
Define $T = t-1$ as the total number of completed rounds.

1.  **Phase 1: Initial Investment (Round 1)**
    Always play **C**. This establishes a baseline of willingness to contribute.

2.  **Phase 2: Conditional Reciprocity (Rounds 2 to $r-1$)**
    Calculate the historical average participation rate: $\bar{P} = S(t) / (T \times n)$.

    *   **If $\bar{P} \geq \frac{m}{n}$**: Play **C**. The collective effort is consistently sufficient to meet the threshold, so sustain cooperation to ensure the group reward.
    *   **If $\bar{P} < \frac{m}{n}$**: Calculate the "Need-to-Reach" contribution ($NTR$) required for the current round: $NTR = m - (\text{previous round's observed cooperators})$.
        *   If $NTR \leq 1$, play **C** to assist in reaching the threshold.
        *   If $NTR > 1$, play **D**. If the group is significantly failing to coordinate, the cost of contribution is lost without the benefit of the threshold reward.

3.  **Phase 3: Terminal Stage (Round $r$)**
    *   If the strategy was in a "Cooperate" state in Round $r-1$, play **C**.
    *   If the strategy was in a "Defect" state in Round $r-1$, check the historical average $\bar{P}$. If $\bar{P} > 0.5 \times (m/n)$, play **C** as a final altruistic gesture to attempt to trigger the threshold reward; otherwise, play **D**.

### Edge Cases and Robustness

*   **Sudden Drop-off:** If $N_c(t-1) < m$ and the trend is sharply declining, switch to **D** regardless of historical averages to prevent resource exhaustion, unless the current round is the final round.
*   **Threshold Vulnerability:** If $N_c(t-1) = m$, prioritize **C** in the subsequent round. This preserves the status quo of the threshold, acting as an anchor to signal that the cooperative threshold is the goal.
*   **Indifference:** In any case where the calculated decision rule is ambiguous, default to **C**.
'''

description_ALTRUISTIC_2 = '''
The strategy employs a "Conditional Threshold Reciprocity" model, operating in three distinct phases based on the round number ($t$) and historical cooperation levels ($H_t$).

**Phase 1: Initialization ($t=1$)**
Cooperate ($C$) if $m/n \leq 0.5$. If $m/n > 0.5$, play $C$ with probability $0.5$ to test the collective willingness to coordinate without immediate exploitation risk.

**Phase 2: Reciprocal Monitoring ($1 < t < r$)**
Let $c_{t-1}$ be the number of cooperators in the previous round.
1.  **If $c_{t-1} \geq m$:** Continue to cooperate ($C$). Success is being achieved; maintain contribution.
2.  **If $c_{t-1} < m$:** Defect ($D$) with probability $P_d$ where $P_d = 1 - (c_{t-1}/m)$. This "probabilistic defection" signals that the current level of cooperation is insufficient while keeping a window open for recovery.
3.  **If $c_{t-1} = 0$:** Defect ($D$). Total breakdown indicates the strategy is being exploited or the group is uncoordinated.

**Phase 3: Terminal Phase ($t = r$)**
Defect ($D$) unless the cumulative history suggests the group is highly cooperative ($c_{avg} \geq m$). Specifically, if the average number of cooperators across all previous rounds $\bar{C} \geq m$, play $C$. Otherwise, play $D$.

**Edge Case Logic:**
*   **Persistent Failure:** If the group fails to meet $m$ for three consecutive rounds despite your cooperation, switch to playing $D$ for the remainder of the game to prevent indefinite loss of endowment.
*   **Sudden Drop:** If $c_{t-1}$ drops significantly (defined as a decrease of $> 50\%$ from the previous round), immediately switch to $D$ for one round as a "tit-for-tat" warning, regardless of the threshold status, before reverting to the rules in Phase 2.
*   **The "Altruistic Buffer":** In any round where the group achieves exactly $m$ cooperators, play $C$ in the next round regardless of your own potential gain from defecting, as this maintains the critical threshold required for the collective reward.
'''

description_ALTRUISTIC_3 = '''
Define the cooperation target $T$ as $m$ players.

### Phase 1: Initiation
In Round 1, always play C.

### Phase 2: Monitoring and Adaptation
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $S_{t-1}$ be your own action in the previous round (1 if C, 0 if D).

Calculate the "Defector-Weighted Deficit":
Define $D_{t-1}$ as the number of players who played D in the previous round.
$D_{t-1} = n - C_{t-1}$.

Maintain a variable `Forgiveness_Index` initialized at 0.
- If $C_{t-1} \ge m$, increment `Forgiveness_Index` by 1.
- If $C_{t-1} < m$, decrement `Forgiveness_Index` by 2 (minimum 0).

**Decision Rule:**
Play C if any of the following conditions are met:
1. $C_{t-1} \ge m$: The collective target was reached. Continue cooperating to maintain stability.
2. $C_{t-1} < m$ AND `Forgiveness_Index` < 2: Attempt to foster cooperation by being the player who corrects the shortfall.
3. Random Probability: If the above conditions are not met, play C with probability $P = \frac{m - C_{t-1}}{n - C_{t-1}}$. This specifically targets the gap between current cooperation and the threshold required for the collective reward.

Otherwise, play D.

### Phase 3: Terminal Round Handling
In the final round ($t = r$):
- If the average number of cooperators over the previous $r-1$ rounds $\ge m - 1$, play C.
- Otherwise, play D, as the game ends and altruistic signaling cannot influence future rounds.

### Strategy Summary Logic
```pseudocode
if (t == 1) return C
if (t == r) {
    if (Average_Historical_Cooperation >= m - 1) return C
    else return D
}

if (Observed_Cooperators[t-1] >= m) {
    Forgiveness_Index = min(5, Forgiveness_Index + 1)
    return C
} else {
    Forgiveness_Index = max(0, Forgiveness_Index - 2)
    if (Forgiveness_Index < 2) return C
    else return D
}
```
'''

description_ALTRUISTIC_4 = '''
The strategy, named "Conditional Threshold Cooperation," is defined by a cooperative, tit-for-tat-inspired mechanism designed to stabilize the contribution threshold ($m$) while resisting exploitation.

### Decision Rules

1. **Initialization (Round 1):** Play **Cooperate (C)**. This signals a commitment to the collective goal and establishes a baseline for group reciprocity.

2. **Subsequent Rounds ($t > 1$):**
   * Let $C_{t-1}$ be the number of cooperators observed in the previous round.
   * If $C_{t-1} \ge m$: Play **Cooperate (C)**. The threshold was met; continue reinforcing the successful cooperative norm.
   * If $C_{t-1} < m$: Play **Defect (D)**. The collective failed, indicating either a lack of coordination or widespread defection. Defecting prevents the continued loss of endowment while attempting to "reset" the group or signal dissatisfaction.

3. **Restoration (The "Forgiveness" Trigger):**
   * If you played **Defect (D)** in round $t-1$ because $C_{t-1} < m$, observe the outcome of round $t-1$. If $C_{t-1} = m-1$, play **Cooperate (C)** in the next round. This facilitates a "coordinated restart" specifically when the group was only one person short of success, signaling a willingness to reach the threshold without initiating a death spiral of total defection.
   * If $C_{t-1} < m-1$, continue to play **Defect (D)** until a round occurs where at least $m-1$ players cooperate, at which point revert to **Cooperate (C)**.

4. **Terminal Round ($t = r$):**
   * If $C_{r-1} \ge m$, play **Cooperate (C)**.
   * If $C_{r-1} < m$, play **Defect (D)**. This avoids the "last-round betrayal" paradox by adhering to the established success/failure pattern of the previous round.

### Pseudocode

```python
# Variables:
# m: minimum cooperators needed
# C_prev: number of cooperators observed in the last round
# played_D_last: boolean, true if I played D in the last round

def get_action(round_num, m, C_prev, played_D_last):
    if round_num == 1:
        return 'C'
    
    # Check if the group was successful
    if C_prev >= m:
        return 'C'
    
    # If the group failed, decide whether to forgive or continue punishing
    # Only forgive if the group was very close (m-1) to success
    if played_D_last and C_prev >= (m - 1):
        return 'C'
        
    return 'D'
```

### Strategic Intent
This strategy prioritizes altruism by proactively contributing to the public good. It minimizes the "sucker's payoff" by withdrawing contributions when the collective demonstrates an inability to coordinate ($C_{t-1} < m$). By linking the return to cooperation to the group's proximity to the threshold ($m-1$), the strategy acts as a catalyst for convergence, encouraging others to join in meeting the requirement rather than abandoning the project entirely.
'''

description_BENEVOLENT_1 = '''
**Strategy: Conditional Threshold Coordination**

The core of this strategy is to cooperate in the early stages to establish the feasibility of the threshold and to enforce threshold maintenance, while defecting only when the risk of non-cooperation by others makes the investment irrational.

### Decision Rules

Define $C_t$ as the total number of players who cooperated in round $t$. Let $M_{needed} = m$.

**Phase 1: Initial Signaling (Round 1)**
Always play **C**. This signals willingness to participate in the collective goal.

**Phase 2: Adaptive Maintenance (Rounds 2 to $r-1$)**
Calculate the observed cooperation from the previous round ($C_{t-1}$).
1. If $C_{t-1} \ge m$: 
   - If the player cooperated in $t-1$: Continue to play **C**.
   - If the player defected in $t-1$: Play **C**. (This assumes the threshold was met, so contribution is safe and beneficial).
2. If $C_{t-1} < m$:
   - Calculate the "deficiency": $d = m - C_{t-1}$.
   - If the player cooperated in $t-1$ but the threshold was failed, treat this as a signal of unreliability. Play **D** in round $t$ to avoid the loss of endowment (preserving the unit payoff) unless the observed $C_{t-1}$ is within 1 of the threshold ($C_{t-1} = m - 1$).
   - If $C_{t-1} = m - 1$, play **C** to attempt a "rescue" move to hit the threshold.

**Phase 3: Terminal Phase (Round $r$)**
Regardless of previous history, if the cumulative probability of hitting the threshold $m$ is low or the group has demonstrated inconsistent behavior, the dominant payoff is keeping the endowment.
- If $C_{r-1} \ge m - 1$, play **C**.
- If $C_{r-1} < m - 1$, play **D** to minimize losses in the final round.

### Logic & Edge Cases

*   **Failure Threshold:** If $C_t < m$ consistently for two consecutive rounds, assume the population is non-cooperative. Shift to **D** for all subsequent rounds to maximize personal payoff ($1$ per round) against a non-functioning system.
*   **Threshold Surplus:** If $C_{t-1} \gg m$ (specifically, if $C_{t-1} \ge m + \text{buffer}$, where buffer is $n/4$ or integer 1 if $n$ is small), the contribution is surplus. In this specific scenario, switch to **D** for one round to signal that "over-cooperation" is unnecessary, then revert to **C** in the next round to stabilize.
*   **Anonymity Constraint:** Since opponents are anonymous, assume that the group behavior is a stochastic process. The strategy prioritizes hitting $m$ rather than punishing specific defectors, as punishment is impossible without identifiers.
*   **Benevolence Alignment:** The strategy is benevolent because it prioritizes the success of the collective threshold ($m$) over immediate personal gain, provided that there is a reasonable expectation that other players are also reciprocating. It only defaults to defection when collective action is mathematically or empirically futile.
'''

description_BENEVOLENT_2 = '''
**Round 1:** Play **C** (Cooperate). This signals an initial commitment to collective success.

**Rounds 2 to r-1:**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
1.  **Sustenance Phase:** If $C_{t-1} \ge m$, play **C**. This reinforces the threshold achievement.
2.  **Recovery Phase:** If $C_{t-1} < m$, and the total number of cooperative actions across all previous rounds $R_c$ is less than $m \times t$, play **C** to attempt to re-establish the threshold. 
3.  **Defection Handling:** If $C_{t-1} < m$ and the group appears to have abandoned the threshold (e.g., $C_{t-1}$ is significantly lower than $m$ consistently), play **D** (Defect). This prevents the continuous loss of endowment without receiving the reward $k$.

**Round r (Last Round):**
1.  If the cumulative total of cooperators in the previous round $C_{r-1}$ was $\ge m$, play **C** to secure the final reward.
2.  If $C_{r-1} < m$, play **D**. Since there is no future round to influence, contributing in the final round provides no strategic benefit if the threshold was already missed or is unreachable.

**Adaptivity Rule:**
If the strategy observes $C_t$ such that $C_t \ge m$ for two consecutive rounds, assume the population has reached a cooperative equilibrium and maintain **C** regardless of individual defection risks, unless the observed $C$ drops below $m$ for two consecutive rounds.
'''

description_BENEVOLENT_3 = '''
**Strategy Definition: Conditional Threshold-Trigger (CTT)**

The strategy relies on a "Tit-for-Tat" variation adapted for collective thresholds. It treats cooperation as a social investment and defection as a signal of non-participation.

**1. Definitions**
*   $C_t$: The number of players who cooperated in round $t$.
*   $k$: The reward factor.
*   $m$: The minimum cooperation threshold.
*   $n$: The number of players.
*   $t_{final} = r$.

**2. Decision Rules**

*   **Round 1 ($t=1$):** Cooperate ($C$). The strategy initiates as a cooperator to signal willingness to participate in the collective effort.

*   **Rounds $t \in [2, r-1]$:**
    *   *If the threshold was met in the previous round ($C_{t-1} \ge m$):*
        *   If the current player's payoff was optimal (i.e., they acted as a "free rider" last round), they switch to Cooperate ($C$) to sustain the group equilibrium.
        *   If the previous round resulted in a successful group outcome, Cooperate ($C$).
    *   *If the threshold was NOT met in the previous round ($C_{t-1} < m$):*
        *   If the number of cooperators was close to the threshold ($C_{t-1} = m-1$), Cooperate ($C$) to attempt to rescue the collective reward.
        *   If the number of cooperators was significantly below the threshold ($C_{t-1} < m-1$), Defect ($D$) to avoid wasted contributions until trust is re-established.

*   **Final Round ($t=r$):**
    *   If the group has successfully reached the threshold $m$ in at least 50% of the previous rounds, Cooperate ($C$).
    *   Otherwise, Defect ($D$).

**3. Conditional Logic (Pseudocode)**

```
if t == 1:
    return Cooperate

if previous_round_success == True:
    return Cooperate

if previous_round_success == False:
    if previous_cooperators >= (m - 1):
        return Cooperate
    else:
        return Defect

if t == r:
    if count(rounds_where_success == True) >= (r / 2):
        return Cooperate
    else:
        return Defect
```

**4. Benevolence Heuristic**
The strategy prioritizes group success (the achievement of $m$ cooperators) over short-term individual gain. It aggressively attempts to meet the threshold if the group is near failure, but withdraws contribution (Defection) if the group shows persistent inability to cooperate, thereby signaling that the cooperative mechanism is broken and protecting individual resources from being consistently wasted. It remains "benevolent" by always attempting to contribute to the threshold in the first round and attempting to rescue the threshold when the group is within one player of success.
'''

description_BENEVOLENT_4 = '''
**Strategy Definition: Threshold-Adaptive Reciprocity**

**Core Logic:**
The strategy aims to establish a collaborative outcome where the group reaches the threshold *m* while minimizing exploitation. It operates on the principle of conditional cooperation: cooperate only as long as there is evidence that cooperation can sustain the group threshold, but defect if the collective effort is failing or if the population is predominantly free-riding.

**Decision Rules:**

*   **Round 1 (Initialization):**
    Play **Cooperate (C)**. This signals a commitment to the collective goal and tests the baseline cooperation level of the population.

*   **Subsequent Rounds (t > 1):**
    Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
    *   **Threshold Achievement:** If $C_{t-1} \ge m$, play **C**. This rewards the collective for hitting the target and maintains the status quo.
    *   **Threshold Failure:** If $C_{t-1} < m$, assess the viability of future cooperation:
        *   If the system is approaching the final round ($t = r$), play **Defect (D)**. Since no future rounds remain to influence, maximizing private payoff is the only logical move.
        *   If the system is early or mid-game ($t < r$), implement a "probabilistic test": play **C** with probability $p$, where $p$ is proportional to the observed cooperation in the previous round ($p = \frac{C_{t-1}}{n-1}$ is a baseline heuristic). This forces a continued signal of intent even after a failure, attempting to recover the cooperative equilibrium without unilaterally bearing the full cost of failure.

*   **Opponent Behavior Filtering (Edge Cases):**
    *   **Total Defection:** If $C_{t-1} = 0$, play **D** for all remaining rounds. The population is non-cooperative, and investment is wasted.
    *   **The "Final Round" Hard Stop:** Regardless of history, if $t = r$, play **D**. There is no strategic incentive to contribute when no future consequences exist.
    *   **The "Threshold Safety" Margin:** If $C_{t-1} = m$, there is a risk of small fluctuations causing failure. If $C_{t-1} = m$, play **C** consistently. If $C_{t-1} > m$, continue to play **C** as long as $C_{t-1} \ge m$.

**Pseudocode:**

```python
def decide_action(round_t, total_rounds, n, m, history):
    # Base Case: Last Round
    if round_t == total_rounds:
        return "D"
    
    # Base Case: First Round
    if round_t == 1:
        return "C"
        
    prev_cooperators = history[-1]
    
    # Check for total collapse
    if prev_cooperators == 0:
        return "D"
        
    # Check for successful threshold
    if prev_cooperators >= m:
        return "C"
    
    # Recovery Attempt (if failure occurred but some cooperated)
    # Re-cooperate with probability proportional to past success
    probability_to_cooperate = prev_cooperators / (n - 1)
    if random() < probability_to_cooperate:
        return "C"
    else:
        return "D"
```
'''

description_SELFISH_1 = '''
Define the player’s goal as maximizing total payoff over $r$ rounds. This is achieved by playing $C$ only when necessary to induce the threshold reward $k$, while defecting whenever the threshold can be reached without the player's contribution or when the group fails regardless of the player's contribution.

**Decision Logic:**

1.  **Round 1:** Play $C$. This establishes a baseline of cooperation and tests the group's responsiveness to the collective action.

2.  **Subsequent Rounds ($t > 1$):** Let $C_{t-1}$ be the total number of cooperators in the previous round.
    *   If $C_{t-1} \geq m + 1$: The threshold was exceeded even without this player's contribution. Play $D$. This is the strictly dominant choice for maximizing payoff, as keeping the endowment yields a higher immediate return ($1 + k > k$).
    *   If $C_{t-1} = m$: The threshold was met, but exactly or barely. Play $D$. If the group maintained the threshold, continue defecting. If the group falls below $m$ as a result, revert to $C$ in the next round.
    *   If $C_{t-1} < m$: The threshold was not met.
        *   If the player played $D$ last round, switch to $C$.
        *   If the player played $C$ last round, analyze the history. If the group has consistently failed to reach $m$ cooperators despite this player's $C$ contribution for the last 3 rounds, conclude the group is uncooperative. Switch to $D$ for the remainder of the game to minimize personal losses.

3.  **Final Round ($r$):** Play $D$. Since there are no future consequences to influence, the dominant strategy is to defect regardless of previous history, as the immediate payoff for $D$ is always higher than $C$ ($1 + \text{reward} > \text{reward}$ vs $0 + \text{reward} > \text{reward}$).

**Pseudocode:**

```python
# Variables:
# m: threshold
# k: reward
# history: list of cooperator counts per round
# t: current round
# last_action: C or D

if t == r:
    return D

if t == 1:
    return C

prev_cooperators = history[-1]

if prev_cooperators >= m + 1:
    return D

if prev_cooperators == m:
    return D

if prev_cooperators < m:
    if last_action == D:
        return C
    else:
        # Check for consistent failure
        if t > 4 and all(c < m for c in history[-3:]):
            return D
        return C
```
'''

description_SELFISH_2 = '''
### Strategy: Threshold-Conditional Reciprocity

The objective is to maximize cumulative payoff by balancing the free-rider incentive (D) against the necessity of meeting the threshold (m) to secure the reward (k).

**Decision Rule Framework:**

1.  **First Round:** Play `C`. Establishing a cooperative baseline is necessary to induce others to contribute in early rounds, as defecting immediately signals a non-cooperative stance that often triggers widespread defection.

2.  **Subsequent Rounds (t > 1):**
    *   **Observation:** Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   **Condition A (Threshold Met):** If $C_{t-1} \ge m$, the group is successfully coordinating.
        *   If the strategy defected in the previous round and received the maximum payoff (i.e., the strategy contributed 0 but the threshold was still met), continue to defect.
        *   If the strategy cooperated in the previous round, defect (D) to maximize individual gain.
    *   **Condition B (Threshold Not Met):** If $C_{t-1} < m$, the group is failing.
        *   If the strategy defected in the previous round, switch to `C`. This attempts to nudge the group toward the threshold by increasing the cooperation count by one.
        *   If the strategy cooperated in the previous round, continue to `C` only if $C_{t-1} \ge m - 2$. If the group is far from the threshold ($C_{t-1} < m - 2$), switch to `D` to minimize losses, as the reward $k$ is unreachable.

**Final Round (t = r):**
Always play `D`. Since there are no future consequences, the dominant strategy is to keep the endowment and hope that others play `C` to trigger the threshold reward.

**Pseudocode Logic:**

```python
# Strategy Variables
last_action = 'C'
last_cooperators = 0

def play(round, r, n, m, k):
    if round == 1:
        last_action = 'C'
        return 'C'
    
    if round == r:
        return 'D'

    # Logic based on previous round outcome
    if last_cooperators >= m:
        # Threshold was met; defect to free-ride
        last_action = 'D'
        return 'D'
    else:
        # Threshold was not met; pivot based on how close we were
        if last_cooperators >= (m - 2):
            # Close enough to potentially reach threshold
            last_action = 'C'
            return 'C'
        else:
            # Too far to make a difference; conserve resources
            last_action = 'D'
            return 'D'

def update(cooperators_count):
    last_cooperators = cooperators_count
```
'''

description_SELFISH_3 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Defection-in-the-End**

**Strategy Overview**
This strategy aims to maximize personal payoff by exploiting the threshold condition $m$ while minimizing individual contribution cost, effectively acting as a "parasitic cooperator" or a free-rider until the collective behavior forces a shift. It operates by observing the total number of cooperators ($C_{total}$) in the previous round to gauge the group's reliability.

**Core Decision Rules**
Let $C_{prev}$ be the number of cooperators observed in the previous round.
Let $my\_contribution$ be your action in the previous round ($1$ if $C$, $0$ if $D$).
Let $C_{others}$ be the number of cooperators excluding yourself.

*   **Round 1:** Play $C$ if $m \le n/2$, otherwise play $D$. This establishes a cooperative signal if the threshold is low, or protects endowment if the threshold is high.
*   **Subsequent Rounds (2 through $r-1$):**
    *   If $C_{others} \ge m$: Always play $D$. The threshold is met without your contribution; you maximize payoff by free-riding.
    *   If $C_{others} = m - 1$: Play $C$. You are the pivotal player required to trigger the reward $k$.
    *   If $C_{others} < m - 1$: Play $D$. The threshold is unattainable this round regardless of your contribution; preserve your endowment.
*   **Final Round ($r$):** Always play $D$. Since there are no future rounds to incentivize others to cooperate, any contribution is a pure loss of the endowment with no possibility of gaining future reputation benefits.

**Pseudocode Logic**
```
If round == r:
    return D

If round == 1:
    if m <= (n / 2):
        return C
    else:
        return D

# Logic for intermediate rounds
C_others = C_prev - (1 if my_prev_action == C else 0)

if C_others >= m:
    return D
elif C_others == m - 1:
    return C
else:
    return D
```

**Edge Case Handling**
*   **Threshold Infeasibility:** If the observed history consistently shows $C_{others} < m-1$ for multiple consecutive rounds, the strategy abandons all attempts to coordinate and defaults to $D$ for all remaining rounds, as the group is deemed uncooperative.
*   **Anonymity Constraint:** Because the game provides aggregate information only, the strategy ignores identifying specific opponents and relies purely on the aggregate signal ($C_{prev}$) to determine the likelihood of reaching the threshold.
*   **Incentive Alignment:** If the reward $k$ is so small that $1 + k < 1$ (i.e., $k < 0$), the strategy defaults to $D$ for all rounds, as the cost of contributing outweighs the reward. This is implicitly handled by the condition $C_{others} == m-1$ (the strategy will not trigger if the cost-benefit ratio is negative).
'''

description_SELFISH_4 = '''
**Strategic Framework: Threshold-Sensitive Tit-for-Tat**

The core objective is to maximize individual cumulative payoff by maintaining the public good (reaching the threshold $m$) only when necessary, while defecting whenever the threshold is guaranteed to be met without personal contribution, or when the cost of cooperation outweighs the benefit of reaching the threshold.

**Decision Logic**

For each round $t \in \{1, \dots, r\}$, let $C_{t-1}$ be the total number of cooperators observed in the previous round. The strategy follows these rules in sequence:

1.  **Safety Check:** If the game is in the final round ($t = r$), always defect ($D$). The future incentive to maintain cooperation disappears, and the immediate payoff for defecting is strictly higher than cooperating.

2.  **Threshold Analysis:**
    *   If $C_{t-1} > m$: Defect ($D$). The group successfully reached the threshold in the previous round without your contribution. Assuming opponent stability, the threshold remains attainable without your participation.
    *   If $C_{t-1} = m$: Defect ($D$). You are a "swing" cooperator. If the group meets the threshold while you defect, you maximize your payoff (free-riding). If the group fails because you defected, you assess the risk in the next round.
    *   If $C_{t-1} < m$: Cooperate ($C$). The threshold is not being met. You must contribute to attempt to trigger the reward $k$.

3.  **Initialization:** In round 1, play $C$. This establishes a baseline level of cooperation to signal willingness to participate, which is necessary to gauge whether the group is capable of reaching the threshold $m$.

**Refinement Rules (Adaptive adjustment)**

*   **Failure Penalty:** If you cooperate ($C$) and the threshold is still not met ($C_{t-1} < m$), defect ($D$) in the subsequent round. This prevents being exploited by a group that fails to coordinate despite your contribution.
*   **Restoration:** If you have been defecting due to a prior failure, wait for one round of observation. If the group shows signs of potential coordination (e.g., $C_{t-1}$ increases towards $m$), return to the standard logic. If the group remains static at a low cooperation level, continue to defect for the remainder of the game to minimize sunk costs.

**Pseudocode Representation**

```python
def decide_action(t, r, m, C_previous):
    if t == r:
        return D
    
    if t == 1:
        return C
    
    # If the group is meeting the goal without me, or if I am the reason 
    # the goal was met (C=m), I free-ride.
    if C_previous >= m:
        return D
    
    # If the group failed the threshold, stop contributing.
    if C_previous < m:
        return D
```
'''

description_SELFINTERESTED_1 = '''
**Strategy Name: Conditional Threshold Trigger (CTT)**

**Decision Rules:**

Maintain a running count of cooperators in the previous round, denoted as $C_{t-1}$. In the first round ($t=1$), play **C (Cooperate)**.

For all subsequent rounds ($t > 1$):

1.  **Observational Check:** Determine if the collective goal was achieved in the previous round.
    *   If $C_{t-1} \ge m$, the threshold was met.
    *   If $C_{t-1} < m$, the threshold was not met.

2.  **Adaptive Response:**
    *   **If the threshold was met in the previous round ($C_{t-1} \ge m$):** 
        *   If you played C in the previous round and the number of cooperators was exactly $m$, there is a high probability that your contribution was necessary. In this specific scenario, switch to **D (Defect)** to test if the group can maintain the threshold without you.
        *   If the number of cooperators was $C_{t-1} > m$, switch to **D (Defect)**. You are currently in a surplus of contributors; defecting maximizes your individual payoff (1 + k) while potentially still meeting the threshold.
        *   If you played D in the previous round and the threshold was met, continue to **D (Defect)**.

    *   **If the threshold was not met in the previous round ($C_{t-1} < m$):**
        *   If you played D, switch to **C (Cooperate)**.
        *   If you played C, continue to **C (Cooperate)**.

3.  **Endgame Logic:**
    *   In the final round ($t = r$):
        *   If the previous round ($t = r-1$) resulted in $C_{r-1} \ge m$, play **D (Defect)**. The incentive to contribute vanishes as there are no future rounds to influence.
        *   If the previous round ($t = r-1$) resulted in $C_{r-1} < m$, play **C (Cooperate)** if your contribution is required to push the count to $m$ (i.e., $C_{r-1} = m-1$). Otherwise, play **D (Defect)**, as cooperation is mathematically futile if the threshold cannot be met by your single contribution.

**Summary of Logic:**
The strategy uses a "Win-Stay, Lose-Shift" logic modified for threshold games. It aggressively pursues the $k$ reward while minimizing the cost of cooperation. It assumes that if the threshold is met, the group is stable enough to allow for freeriding, and if the threshold fails, the group must coordinate on cooperation to unlock the $k$ value.
'''

description_SELFINTERESTED_2 = '''
The strategy follows a conditional, threshold-based logic designed to incentivize cooperation while minimizing exploitation in early rounds and maximizing gain in final rounds.

### Strategy: Adaptive Threshold Tit-for-Tat

**State Variables:**
- $C_{t-1}$: Number of cooperators observed in the previous round.
- $r_{rem}$: Number of rounds remaining (including current).
- $CoopCount$: Accumulated cooperators observed in prior rounds.

**Decision Rules:**

1. **Initialization (Round 1):**
   - Play **Cooperate (C)**. This signals a willingness to coordinate for the threshold $m$.

2. **Standard Play (Round 2 to $r-1$):**
   - If $C_{t-1} \ge m$: Play **Cooperate (C)**. The threshold is being met, and cooperation is sustainable.
   - If $C_{t-1} < m$: Play **Defect (D)**. If the threshold was not met, cooperation is either being exploited or is insufficient; defecting protects endowment against wasted contributions.
   - *Special Case (Trigger):* If the strategy has defected for 2 consecutive rounds and the group $C_{t-1}$ remains $< m$, switch to **Cooperate (C)** for one round to attempt a "reset" or "restart" of coordination, assuming random noise or confusion. If this reset fails, revert to permanent **Defect (D)** for the remainder of the game.

3. **Terminal Play (Final Round):**
   - Play **Defect (D)** regardless of history. Since there are no future rounds to incentivize, the dominant strategy is to capture the endowment regardless of whether the threshold is met.

**Pseudocode:**

```python
def choose_action(round, total_rounds, observed_cooperators_prev, m):
    if round == total_rounds:
        return 'D'
    
    if round == 1:
        return 'C'
    
    # Check if threshold was met in previous round
    if observed_cooperators_prev >= m:
        return 'C'
    else:
        # Evaluate recent failure trend
        if consecutive_failures_count >= 2:
            # Attempt one-time reset of coordination
            consecutive_failures_count = 0
            return 'C'
        else:
            consecutive_failures_count += 1
            return 'D'
```

**Edge Case Handling:**
- **Insufficient Cooperators:** If the population consistently fails to reach $m$, the strategy defaults to Defect to maximize individual endowment (1 per round) rather than wasting contributions (0 per round).
- **Stochastic Noise:** The "reset" mechanism handles scenarios where previous failures might have been due to a single defector or low-participation variance, allowing the group a second chance to reach the threshold without being permanently trapped in a non-cooperative state.
'''

description_SELFINTERESTED_3 = '''
Maintain a "Conditional Threshold Tracker" strategy, centered on minimizing unnecessary cooperation while ensuring the threshold $m$ is met only when profitable.

**Variables:**
- $C_{t-1}$: Number of cooperators in the previous round.
- $T_{avg}$: A rolling average or simple moving threshold of observed cooperation across rounds.
- $Status_{t}$: Boolean, true if $C_{t-1} \geq m$, false otherwise.

**Strategy Logic:**

1.  **Initialization (Round 1):**
    Play **Defect (D)**. This establishes a baseline of the opponents' cooperative propensity without sacrificing the endowment.

2.  **Adaptive Phase (Rounds 2 to $r-1$):**
    - If $C_{t-1} \geq m$ and you played $D$:
        Continue playing **Defect (D)**. The threshold is met without your contribution.
    - If $C_{t-1} = m-1$:
        Play **Cooperate (C)**. By contributing, you push the count to $m$, triggering the reward $k$ for the group. Since the gain from $k$ ($k > 1$) outweighs the cost of the lost endowment ($1$), this is rational.
    - If $C_{t-1} < m-1$:
        Play **Defect (D)**. If the group is far below the threshold, a single contribution is insufficient to trigger the reward. Conserve the endowment.

3.  **Terminal Phase (Final Round $r$):**
    - If the goal is pure self-interest and there is no future interaction to incentivize, play **Defect (D)** regardless of past history. There is no future round to punish non-cooperation, and the cost of contribution ($1$) is never recouped if the threshold is not met or if you are the marginal contributor.

**Exception handling:**
If at any point $k \leq 1$, always play **Defect (D)** in all rounds, as the reward cannot compensate for the endowment loss. If the game environment shows a consistent trend where $C_{t-1}$ consistently fails to reach $m$ despite your cooperation, revert permanently to **Defect (D)** to maximize accumulated private wealth.
'''

description_SELFINTERESTED_4 = '''
**Strategy: Threshold-Responsive Tit-for-Tat**

The objective is to maximize cumulative payoff by balancing free-riding (defecting) with the necessity of contributing (cooperating) to hit the threshold $m$. The strategy relies on observing the number of cooperators ($C_t$) in the previous round to adjust the probability of cooperation.

**State Variables:**
- $C_{t-1}$: Number of cooperators in the previous round.
- $N_{coop}$: The number of cooperators observed in the previous round, excluding self.
- $m$: Minimum cooperators needed.
- $r$: Total rounds.
- $t$: Current round.

**Decision Logic:**

1.  **Round 1:**
    Play **Defect (D)**. This establishes a baseline for the population's cooperation level without risking the endowment.

2.  **Rounds $t=2$ to $r-1$:**
    The decision to cooperate depends on whether the threshold was met in the previous round and whether the contribution is necessary.
    - If the threshold was met ($C_{t-1} \ge m$):
        - If I played $C$ in round $t-1$: Check if my contribution was pivotal. My contribution was pivotal if $C_{t-1} = m$. If pivotal, continue to play **Cooperate (C)**. If not pivotal ($C_{t-1} > m$), switch to **Defect (D)**.
        - If I played $D$ in round $t-1$: Continue to play **Defect (D)**.
    - If the threshold was not met ($C_{t-1} < m$):
        - If I played $C$ in round $t-1$: This indicates insufficient cooperation. Switch to **Defect (D)** to preserve the endowment, as consistent cooperation without reciprocal support is net-negative.
        - If I played $D$ in round $t-1$: Calculate the "Necessity Index" $I = m - C_{t-1}$. If $I = 1$ (the threshold is one player away), play **Cooperate (C)**. Otherwise, play **Defect (D)**.

3.  **Final Round ($t = r$):**
    Always play **Defect (D)**. Since there are no future rounds to incentivize or punish opponents, maximizing the immediate payoff by keeping the endowment is the dominant strategy regardless of the threshold outcome.

**Pseudocode:**

```python
def get_action(round_num, total_rounds, m, last_round_cooperators, my_last_action):
    if round_num == 1:
        return 'D'
    
    if round_num == total_rounds:
        return 'D'
    
    # Calculate cooperators other than self in previous round
    others_cooperated = last_round_cooperators - (1 if my_last_action == 'C' else 0)
    
    if last_round_cooperators >= m:
        # Threshold met: exploit if possible
        if my_last_action == 'C' and last_round_cooperators == m:
            return 'C' # Maintain cooperation if pivotal
        return 'D'
    
    else:
        # Threshold not met: attempt to trigger threshold if marginal
        if others_cooperated == (m - 1):
            return 'C'
        return 'D'
```
'''

description_OPPORTUNISTIC_1 = '''
The strategy adopts a "Conditional Tit-for-Tat with a Threshold Constraint," prioritizing short-term gain (defecting) while maintaining the collective threshold only when necessary to secure the reward $k$.

### Decision Logic

The strategy relies on a sliding window of historical cooperation. Let $C_{total, t-1}$ be the total number of cooperators in round $t-1$.

**Round 1:**
- Defect ($D$). This establishes the baseline for the opponents' cooperation levels without risking endowment unnecessarily.

**Rounds 2 through $r-1$:**
- Calculate the "Minimum Necessary Cooperation" ($MNC$):
  - If you played $C$ in round $t-1$: You need $m-1$ other cooperators to trigger the reward.
  - If you played $D$ in round $t-1$: You need $m$ other cooperators to trigger the reward.
- If the previous round's outcome ($C_{total, t-1}$) met the threshold $m$ and resulted in a reward for you:
  - Defect ($D$). Attempt to free-ride.
- If the previous round's outcome failed to meet the threshold $m$:
  - If the reward $k$ is greater than the cost of contribution (1), and the history suggests that the group is fluctuating near $m$, switch to Cooperate ($C$) to nudge the total over the threshold.
  - If the history suggests $C_{total, t-1} < m - 1$ consistently, remain Defecting ($D$) to minimize loss.

**Final Round ($r$):**
- Defect ($D$) regardless of previous history. The future-game incentive to cooperate vanishes, making the only rational choice to keep the endowment.

### Pseudocode Implementation

```python
def get_action(t, r, m, k, history):
    # Rule 1: Always defect in the final round
    if t == r:
        return 'D'
    
    # Rule 2: Always defect in the first round
    if t == 1:
        return 'D'
    
    # Analyze history
    last_round_cooperators = history[-1]
    
    # Rule 3: Opportunistic logic
    # Check if we gained the reward last round
    # If we played 'C' last round, we needed m-1 others.
    # If we played 'D' last round, we needed m others.
    gained_reward_last_round = (last_round_cooperators >= m)
    
    if gained_reward_last_round:
        # If we got the reward, try to free-ride
        return 'D'
    else:
        # If we failed the reward, check if cooperating helps
        # If the group is close to the threshold, contribute
        if last_round_cooperators >= (m - 1):
            return 'C'
        else:
            # If the group is far from threshold, don't waste contribution
            return 'D'
```

### Edge Case Handling

*   **Reward Inefficiency:** If $k \le 1$, the strategy immediately defaults to permanent Defection ($D$) for all $r$ rounds, as the cost of contributing (1) outweighs the reward ($k$).
*   **Threshold Volatility:** If the number of cooperators oscillates wildly, the strategy defaults to $D$ for two consecutive rounds to reset and verify if the group is reliably providing the reward before committing a contribution.
*   **Minimal Thresholds ($m \approx n$):** If $m$ is very close to $n$, the probability of hitting the threshold via others is low. The strategy will default to $D$ after the first attempt to verify, effectively treating the game as a non-cooperative prisoner's dilemma.
'''

description_OPPORTUNISTIC_2 = '''
The strategy utilizes a "threshold-trigger conditional cooperation" model, focusing on maximizing individual gains while ensuring the collective threshold is met only when necessary for long-term reward stability. The core mechanism is a rolling window estimate of opponent cooperativeness, adjusted by a "free-rider" bias.

**Strategy Definitions:**

*   **Cooperation Window (W):** A parameter set to 3 rounds.
*   **Target Contribution ($C_{target}$):** The minimum number of cooperators required ($m$).
*   **Free-Rider Threshold ($\tau$):** A tolerance level defined as $m/n$.

**Decision Logic:**

1.  **Initialization (Round 1):**
    Play **C** (Cooperate) to signal willingness to participate and establish the cooperative baseline.

2.  **Tracking:**
    In each round $t > 1$, calculate the number of cooperators observed in the previous round ($C_{t-1}$). Track the average number of cooperators over the last $W$ rounds ($\bar{C}_W$).

3.  **Core Decision Rule (Round $t$):**
    *   **If $t = r$ (Last Round):**
        Defect (**D**). Since there are no future rounds to influence, maximize immediate payoff regardless of threshold outcomes.
    *   **If $\bar{C}_W \geq m$:**
        Defect (**D**). If the group has historically met the threshold without additional help, exploit the contribution of others to capture the $k$ reward without paying the contribution cost.
    *   **If $\bar{C}_W < m$:**
        Cooperate (**C**). If the group is underperforming, contribute to ensure the threshold $m$ is met, thereby securing the $k$ reward. This acts as a "recovery" mechanism to prevent the loss of the reward.
    *   **Stochastic Jitter:**
        If $\bar{C}_W$ is exactly $m-1$ or $m-2$, incorporate a probabilistic check. Cooperate with probability $p = 0.5$ to introduce uncertainty, preventing opponents from perfectly predicting the exploitation pattern while maintaining a high probability of meeting the threshold.

**Pseudocode:**

```python
# Parameters: m (threshold), n (players), r (rounds)
# Variables: history (list of cooperators per round)

def make_decision(round_number, history):
    if round_number == r:
        return 'D'
    
    if round_number == 1:
        return 'C'
    
    avg_cooperators = mean(history[-W:])
    
    if avg_cooperators >= m:
        return 'D'
    
    if avg_cooperators >= (m - 2):
        return random_choice(['C', 'D'], p=[0.5, 0.5])
    
    return 'C'
```

**Edge Case Handling:**
*   **Persistent Defection:** If the group fails to meet the threshold for 3 consecutive rounds despite your cooperation, switch to pure Defection (**D**) for the remainder of the game. The group is deemed uncooperative, and efforts to influence the outcome are effectively sunk costs.
*   **Last Round Sensitivity:** Always prioritize personal gain ($1+k$ vs $0+k$) in the final round $r$, as no future consequences exist to incentivize threshold maintenance.
'''

description_OPPORTUNISTIC_3 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat**

The strategy operates on the principle of conditional cooperation: contribute only if necessary to meet the threshold $m$, while defecting whenever the threshold is guaranteed to be met by others or impossible to reach. This balances group success with personal payoff maximization.

**Decision Logic**

Let $C_{t-1}$ be the number of cooperators observed in the previous round (for $t=1$, assume $C_0 = m-1$). Let $s_i$ be your own action in the previous round ($1$ for Cooperate, $0$ for Defect).

1.  **If $t = 1$:** 
    Play **Cooperate**. This establishes initial trust and tests the willingness of the group to reach the threshold without needing negative feedback.

2.  **If $t > 1$:**
    Calculate the "Effective Cooperation" ($E$), defined as the number of *other* players who cooperated in the previous round:
    *   If $s_i = 1$ (you cooperated): $E = C_{t-1} - 1$
    *   If $s_i = 0$ (you defected): $E = C_{t-1}$

    Decide current action $A_t$:
    *   **Defect** if $E \ge m$: The threshold is secured by others; capture the free-rider bonus.
    *   **Cooperate** if $m - E = 1$: You are the marginal player required to hit the threshold.
    *   **Defect** if $m - E > 1$: The threshold is too far out of reach to be saved by a single contribution; conserve resources.
    *   **Cooperate** if $m - E \le 0$: Maintain momentum.

**Edge Cases**

*   **Last Round ($t = r$):** If the threshold was met in the previous round ($C_{t-1} \ge m$), play **Defect** regardless of the calculated logic, as there are no future rounds to influence. If the threshold was not met, play **Defect** unless you are the sole missing contributor needed to reach $m$ ($E = m-1$), in which case play **Cooperate** to secure the final payoff.
*   **Persistent Defection:** If $E$ remains consistently below $m-1$ for more than two consecutive rounds, switch to **Defect** permanently for the remainder of the game to minimize personal losses against an uncooperative pool.
*   **Threshold volatility:** If $C_{t-1} < m$ but $C_{t-1} > C_{t-2}$, play **Cooperate** to reward the positive trend and encourage group coordination.
'''

description_OPPORTUNISTIC_4 = '''
**Threshold-Monitoring Tit-for-Tat (TMTT)**

The strategy operates on a state-based logic that prioritizes hitting the cooperation threshold $m$ while maximizing individual payoffs by defecting whenever the threshold is safely exceeded.

**Decision Logic**

In each round $t \in \{1, \dots, r\}$, the strategy determines whether to contribute $c_t$ based on the total number of cooperators in the previous round $C_{t-1}$.

1. **Initial Round ($t=1$):**
   - Cooperate ($c_1 = 1$). This signals willingness to participate and tests the baseline cooperation level of the population.

2. **Subsequent Rounds ($t > 1$):**
   - Let $C_{t-1}$ be the number of players who cooperated in the previous round.
   - If $C_{t-1} \geq m + 1$:
     - Defect ($c_t = 0$). The threshold is met without your contribution. You collect the private endowment plus the threshold reward.
   - If $C_{t-1} = m$:
     - Defect ($c_t = 0$). You are currently "pivotal" (your contribution is keeping the threshold met). However, an opportunistic agent tests whether the group will sustain the threshold without them. 
     - *Exception:* If $t = r$, play $c_r = 1$ to ensure the reward is captured in the final round before the game ends.
   - If $C_{t-1} < m$:
     - Cooperate ($c_t = 1$). The group failed to meet the threshold. You must contribute to help reach $m$.

**Pseudocode**

```python
def get_action(t, r, m, history):
    if t == 1:
        return 1  # Always cooperate in the first round

    last_round_cooperators = history[t-1]
    
    # Check if threshold was met
    if last_round_cooperators >= m:
        # If we are in the last round, protect the reward by cooperating
        if t == r:
            return 1
        # Otherwise, attempt to free-ride
        return 0
    
    # If threshold was missed
    else:
        return 1
```

**Edge Case Handling**

*   **Last Round ($t=r$):** The strategy forces cooperation if the previous round suggests there is any risk of falling below $m$. If the previous round saw $C_{r-1} \ge m$, the strategy defaults to defection for maximum payoff, assuming the group inertia or the previous success will carry through to the final round.
*   **Failed Thresholds:** If the strategy cooperates ($c_t=1$) and the group still fails to meet the threshold ($C_t < m$), it continues to cooperate in the next round ($t+1$) until the threshold is met.
*   **Reward Maximization:** The strategy strictly prioritizes $D$ when the threshold is met, as $1+k > k$. It only switches to $C$ to rectify a failure state or to secure the reward in the terminal round.
'''

description_INDIVIDUALISTIC_1 = '''
**Strategy: Conditional Threshold Tit-for-Tat**

The strategy operates on the principle of maintaining the threshold $m$ while punishing unilateral defection and rewarding collective stability.

**Initialization (Round 1):**
Play Cooperate (C) if $m/n \leq 0.5$. Otherwise, play Defect (D). This establishes a baseline of cooperation only if the required burden is perceived as sustainable given the total population.

**Subsequent Rounds (t > 1):**
Let $N_c(t-1)$ be the number of cooperators observed in the previous round.
Let $c_{self}(t-1)$ be your own action in the previous round.

1. **Defection Punishment:** If $N_c(t-1) < m$ (the threshold was missed), play Defect (D) for the current round regardless of any other conditions. This forces a reset in scenarios where cooperation has collapsed.
2. **Cooperation Maintenance:** If $N_c(t-1) \geq m$:
   - If you played Defect (D) last round and $N_c(t-1) \geq m+1$, play Cooperate (C). This signals a transition to cooperation.
   - If you played Cooperate (C) last round and $N_c(t-1) > m$, play Cooperate (C). The threshold is being exceeded comfortably.
   - If you played Cooperate (C) last round and $N_c(t-1) = m$, play Defect (D) with probability $p = 1/n$. This individualistic check tests whether the threshold is maintained even if you reduce your contribution, preventing unnecessary over-contribution.
   - If you played Defect (D) last round and $N_c(t-1) = m$, play Defect (D). Do not increase contribution when the threshold is exactly met without your input.

**Final Round Strategy (Round r):**
Regardless of previous history, if $m < n$, play Defect (D). If $m = n$, play Cooperate (C) only if the previous round resulted in all $n$ players cooperating; otherwise, play Defect (D). This prioritizes individual gain in the terminal round while preserving the collective outcome only if it is already guaranteed.

**Summary Pseudocode:**

```python
if t == 1:
    return C if m/n <= 0.5 else D

if t == r:
    return D if m < n else (C if N_c(t-1) == n else D)

if N_c(t-1) < m:
    return D

if N_c(t-1) >= m:
    if c_self(t-1) == D and N_c(t-1) > m:
        return C
    if c_self(t-1) == C and N_c(t-1) > m:
        return C
    if c_self(t-1) == C and N_c(t-1) == m:
        return D if random_float() < (1/n) else C
    return D
```
'''

description_INDIVIDUALISTIC_2 = '''
The strategy follows a conditional tit-for-tat framework calibrated to the threshold $m$, designed to identify and exploit reliable contributors while minimizing losses against exploiters.

### Core Logic

Let $C_{t-1}$ be the number of cooperators observed in the previous round.

1.  **Phase 1: Probing (Round 1)**
    Cooperate ($C$) in the first round to signal intent and establish the threshold equilibrium.

2.  **Phase 2: Adaptive Response (Rounds 2 to $r-1$)**
    - **Trigger Condition:** If $C_{t-1} \ge m$, continue to cooperate. This reinforces the cooperative equilibrium when the threshold is successfully met.
    - **Retaliation Condition:** If $C_{t-1} < m$, defect ($D$). This minimizes contribution losses when the collective goal is failing, signaling that participation is contingent upon success.
    - **Recovery Condition:** If $C_{t-1} < m$ but the previous action was $D$, switch to $C$ with a probability $p$ (where $p = 0.5$ or a lower value if the player is risk-averse) to test if the collective environment has shifted back to a cooperative state. If the probe results in $C_t \ge m$, return to the Trigger Condition.

3.  **Phase 3: Final Round Strategy (Round $r$)**
    - Defect ($D$) regardless of the previous round's outcome. Since there is no future shadow of the future to enforce cooperation, the dominant individualistic move is to capture the private payoff without the threat of retaliation in a subsequent round.

### Edge Cases and Parameter Calibration

- **Threshold Sensitivity:** If the observed count is exactly $m$, maintain the cooperative state. If the observed count is $m-1$ and you were a defector, do not switch to cooperation unless you have a high expectation that others will also switch.
- **Independence:** Because the strategy observes only the aggregate number of cooperators, it treats the group as a single entity. It does not attempt to track specific players. If the group consistently fails to meet the threshold, the strategy defaults to permanent defection to avoid resource depletion.
- **Robustness:** If $C_{t-1}$ is consistently low, the strategy shifts to permanent defection after the first $r/4$ rounds to prevent perpetual loss.
'''

description_INDIVIDUALISTIC_3 = '''
To maximize the total payoff over *r* rounds, adopt a threshold-based conditional cooperation strategy, focusing on achieving the minimum viable coalition size while minimizing personal contribution costs.

**Strategic Principle: Conditional Threshold Optimization**

Define a target state where exactly *m* players cooperate. Because the payoff structure rewards all players equally once the threshold *m* is reached, individual cooperation is only strictly profitable if it is necessary to reach that threshold.

**Decision Rules**

1.  **First Round:** Cooperate (C). Establishing a signal of cooperation is necessary to trigger potential reciprocation from other players.

2.  **Subsequent Rounds (t > 1):**
    *   Observe the total number of cooperators from the previous round, denoted as *N_{t-1}*.
    *   **Case 1: If *N_{t-1}* ≥ *m*:**
        *   If the system is already stable, defect (D). You maximize your individual return (1 + k) by letting others bear the cost of contribution.
    *   **Case 2: If *N_{t-1}* = *m - 1*:**
        *   Cooperate (C). By contributing, you push the group over the threshold, ensuring the reward *k* is unlocked for everyone.
    *   **Case 3: If *N_{t-1}* < *m - 1*:**
        *   Defect (D). If the group is significantly below the threshold, your single contribution is insufficient to trigger the reward. Conservatism dictates keeping the endowment (1) to avoid the sunk cost of contribution.

**Edge Cases and Adjustments**

*   **The "Defection Trap":** If the observed cooperation rate drops consistently below *m* for two consecutive rounds, assume the population is not coordinating. Switch to pure defection (D) for all remaining rounds to maximize baseline returns (1).
*   **The Final Round (r):**
    *   If the strategy was in a "cooperative" state (having successfully triggered the reward *k* in the previous round), defect (D). In the final round, there is no future reputation benefit to maintaining the threshold, and the temptation to defect (1 + k) outweighs the altruistic incentive.
    *   If the strategy was not in a cooperative state, continue following the round *t > 1* logic.

**Pseudocode Representation**

```python
def decide_action(round_num, last_round_cooperators, m, r):
    if round_num == 1:
        return 'C'
    
    if round_num == r:
        return 'D'
        
    if last_round_cooperators >= m:
        return 'D'
    
    if last_round_cooperators == m - 1:
        return 'C'
        
    # If last_round_cooperators < m - 1
    return 'D'
```
'''

description_INDIVIDUALISTIC_4 = '''
The optimal individualistic strategy is a "Conditional Threshold-Triggered Tit-for-Tat" approach, designed to maximize personal utility by incentivizing group success while aggressively defecting when the group fails to meet the threshold.

**Decision Logic:**

1.  **Round 1:** Play **Defect (D)**. This establishes a baseline of self-interest and avoids exploitation in the absence of trust.

2.  **Subsequent Rounds (2 to r):**
    *   Let $N_c(t-1)$ be the number of cooperators observed in the previous round.
    *   Let $c_{self}(t-1)$ be your own action in the previous round.
    *   If $N_c(t-1) \ge m$: 
        *   Play **Cooperate (C)**. This assumes the group has reached the threshold, and you are ensuring your own inclusion in the reward $k$ (since your contribution is required to keep the total count $\ge m$ if $N_c$ is exactly $m$, or simply to maintain the cooperative equilibrium).
    *   If $N_c(t-1) < m$ and $c_{self}(t-1) = C$: 
        *   Play **Defect (D)**. This is a punitive response to the group failing to reach the threshold despite your contribution. You stop carrying the burden for non-cooperators.
    *   If $N_c(t-1) < m$ and $c_{self}(t-1) = D$: 
        *   Play **Defect (D)**. The group is unstable or insufficient; continue playing for the private endowment.

**Exceptions and Edge Cases:**

*   **The Threshold Recovery Protocol:** If the group fails ($N_c < m$) and you are currently defecting, you may attempt to "test" the group again. Every $X$ rounds (where $X$ is a value between 3 and 5), play **Cooperate (C)** regardless of the previous round's outcome to see if others are willing to coordinate. If this test round results in $N_c \ge m$, immediately revert to the standard Conditional rule above. If it results in $N_c < m$, return to immediate Defection.
*   **The Final Round:** Regardless of previous history, if the cumulative probability of success in the final round is assessed as low (i.e., historical $N_c$ rarely hits $m$), play **Defect (D)** to guarantee the private endowment of 1. If the group has consistently hit the threshold ($N_c \ge m$) in the prior $r-1$ rounds, play **Cooperate (C)** to secure the final reward $k$.
'''
