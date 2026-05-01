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

description_COLLECTIVE_5 = '''
**Strategy: Threshold-Triggered Tit-for-Tat**

The strategy operates on a "Conditional Cooperation with Grace Period" logic, aiming to establish stable coordination at the minimum threshold $m$ while punishing unilateral defection and discouraging free-riding.

### 1. Decision Rules

Let $C_{t-1}$ be the number of cooperators in the previous round.

**Round 1:** Play **Cooperate (C)**. This signals a willingness to coordinate.

**Round $t$ (where $1 < t < r$):**
- If $C_{t-1} \ge m$:
  - If the player cooperated in $t-1$: Continue to **Cooperate (C)**.
  - If the player defected in $t-1$: Switch to **Cooperate (C)** to attempt re-entry into the cooperative equilibrium.
- If $C_{t-1} < m$:
  - If the player cooperated in $t-1$: Switch to **Defect (D)**. This is a punitive response to the failure to reach the threshold, minimizing individual losses when the collective goal is missed.
  - If the player defected in $t-1$: Continue to **Defect (D)**.

**Round $r$ (Final Round):**
- If $C_{r-1} \ge m$: Play **Cooperate (C)**.
- If $C_{r-1} < m$: Play **Defect (D)**.

### 2. Adaptation Logic (The "Threshold Buffer")
To avoid over-contribution (waste) and ensure the threshold $m$ is met, if the history shows $C_{t-1} > m$ consistently (specifically, for three consecutive rounds), switch to **Defect (D)** for one round to test if the cooperative group can still sustain the threshold $m$ without the player's contribution.

- If the result of the test round is $C_t \ge m$, continue to **Defect (D)** in the subsequent round to maximize individual payoff while maintaining the reward.
- If the result of the test round is $C_t < m$, immediately switch back to **Cooperate (C)** in the subsequent round to restore the cooperative equilibrium.

### 3. Edge Cases
- **Low $m$ Threshold:** If $m=2$, the strategy effectively becomes a coordination game. If $C_{t-1} < m$, the player acts as a "trigger," defecting to signal the failure state, but returning to C immediately if the system state was just one short of the threshold (e.g., $C_{t-1} = m-1$).
- **Early-Game Failure:** If the first round results in $C_1 < m$, immediately transition to the Defect cycle described above.
- **Persistent Defection:** If $C_{t-1}$ remains below $m$ for three consecutive rounds despite attempts to coordinate (switching C to D and back), cease all cooperation for the remainder of the game to minimize endowment loss.
'''

description_COLLECTIVE_6 = '''
Define a target contribution threshold $T = m$. In the first round, play Cooperate ($C$).

For all subsequent rounds $t > 1$, determine the number of cooperators observed in the previous round ($C_{t-1}$). Calculate the strategy decision $S_t$ based on the following logic:

1.  **If $C_{t-1} \ge T$**: You are currently in a state of successful collective cooperation. Play $C$ to maintain the threshold.
2.  **If $C_{t-1} < T$**: The collective failed to meet the threshold. Shift to Defect ($D$) for the current round.
3.  **Recovery trigger**: If you played $D$ in the previous round due to a failure, check if the collective cooperation count was $C_{t-1} = T - 1$. If $C_{t-1} = T - 1$ and you defected, this implies that had you cooperated, the threshold would have been met. If the collective failure was caused by your own defection (or if the collective is oscillating), return to playing $C$ in the next round to attempt to cross the threshold again.

**Edge Cases and Termination:**

*   **Final Round ($t = r$)**: Regardless of previous outcomes, cooperate if $C_{r-1} \ge T$ to secure the final reward. If $C_{r-1} < T$, play $D$, as the incentive to invest is lost when the immediate threshold is unlikely to be met.
*   **Persistent Failure**: If $C_{t-1} < T - 1$ for two consecutive rounds, assume the population is non-cooperative. Play $D$ for all remaining rounds $t$ to preserve endowment.
*   **Threshold Dynamics**: If $n$ is significantly larger than $m$, and $C_{t-1}$ consistently exceeds $T$ by a margin greater than 1, treat the surplus cooperators as a buffer. If $C_{t-1} > T$, you may occasionally play $D$ to test if the group cooperation is robust or fragile; if the count drops to $T$, immediately revert to $C$.
'''

description_COLLECTIVE_7 = '''
**Strategy Description: Threshold-Tit-for-Tat (TTFT)**

The strategy prioritizes reaching the threshold $m$ while punishing unilateral defection and discouraging "free-riding" (defecting while others cooperate). The core mechanism is a conditional strategy based on the recent history of collective behavior, with a "trigger" phase for stability.

**State Variables:**
*   `threshold_met`: Boolean (True if $\ge m$ cooperators in the previous round).
*   `self_cooperated`: Boolean (True if I played C in the previous round).
*   `total_cooperators`: Integer (Number of cooperators in the previous round).

**Decision Logic:**

1.  **Round 1:**
    *   Play **C**. This signals willingness to coordinate.

2.  **Rounds $t > 1$:**
    *   **If `threshold_met` is True:**
        *   If the number of cooperators was exactly $m$ or $m+1$, play **C**. (This maintains the threshold without allowing excessive free-riding).
        *   If the number of cooperators was $> m+1$, play **D** with probability $p = 0.5$, or simply play **D** if preferring aggressive threshold management. (This balances the risk of falling below $m$ while exploiting the surplus).
    *   **If `threshold_met` is False:**
        *   If I played **D** in the previous round, switch to **C**.
        *   If I played **C** in the previous round, check `total_cooperators`.
            *   If `total_cooperators` $\ge m-1$, stay **C** (Try to "pull" the group over the threshold).
            *   If `total_cooperators` $< m-1$, switch to **D** for one round (Punish the group failure to coordinate).

3.  **End-Game Heuristic (Rounds $t \ge r - 2$):**
    *   If the goal is purely maximizing individual payoff regardless of future rounds:
        *   If `threshold_met` is consistently True, play **D**.
        *   If `threshold_met` is inconsistent, play **C** only if the probability of the group reaching $m$ is $> 0.5$ based on the previous 3 rounds of history.

**Pseudocode Implementation:**

```python
def choose_action(round_num, history, n, m, k):
    if round_num == 1:
        return 'C'
    
    prev_total = history[-1].cooperators
    prev_action = history[-1].my_action
    
    # Check if threshold was met in previous round
    threshold_met = prev_total >= m
    
    if threshold_met:
        # If threshold met comfortably, we can defect to gain payoff
        if prev_total > m:
            return 'D'
        else:
            return 'C'
    else:
        # If threshold not met, we need to coordinate
        # If I defected, repent
        if prev_action == 'D':
            return 'C'
        # If I cooperated and others failed, stick to C if we were close
        elif prev_total >= m - 1:
            return 'C'
        # Otherwise, defect to preserve resources
        else:
            return 'D'
```
'''

description_COLLECTIVE_8 = '''
**Strategy: Threshold-Responsive Tit-for-Tat (TR-TFT)**

**Core Logic**
The strategy operates on the principle of conditional reciprocity aimed at maintaining the minimum cooperation threshold ($m$) required to trigger the reward ($k$). The goal is to maximize the expected value of $\sum \pi_i$ by encouraging enough cooperation to trigger the reward while minimizing unnecessary contributions (playing C only when it increases the probability of the threshold being met).

**Decision Rules**

*   **Round 1:** Play **Cooperate (C)**. This signals a willingness to cooperate and initiates the potential for mutual benefit.

*   **Subsequent Rounds ($t > 1$):**
    Let $C_{t-1}$ be the total number of players who cooperated in the previous round.

    1.  **If $C_{t-1} \geq m$:**
        If you played C in $t-1$, **Defect (D)**.
        If you played D in $t-1$, **Defect (D)**.
        *(Rationale: The threshold was met without your contribution in the previous round, so you attempt to free-ride on the collective success.)*

    2.  **If $C_{t-1} < m$:**
        *   **If you played D in $t-1$:** **Cooperate (C)**.
        *   **If you played C in $t-1$:**
            *   If $C_{t-1} = m-1$: **Cooperate (C)**.
            *   If $C_{t-1} < m-1$: **Defect (D)**.
        *(Rationale: If the threshold was missed, you switch to C if you were previously defecting, or if you were previously cooperating and your contribution brought the group within one unit of the threshold. If the group was far from the threshold (fewer than $m-1$), you defect because the collective effort is failing, and contributing alone is a sunk cost.)*

**Edge Cases and Adjustments**

*   **Last Round ($t=r$):**
    If $C_{r-1} < m$, play **Defect (D)** regardless of previous actions.
    *(Rationale: In the final round, there is no future interaction to incentivize; if the threshold was missed previously, the incentive to cooperate vanishes as there is no opportunity to restore trust.)*

*   **Threshold Recovery:**
    If the game state fluctuates such that $C_{t-1}$ was $< m$ but $C_{t-2} \geq m$, the strategy effectively resets to the Round 1 condition: play **Cooperate (C)** to attempt to re-establish the cooperative equilibrium.

*   **Stochastic Tie-Breaking:**
    If the strategy logic dictates an ambiguous choice (e.g., initial state or reset), always default to **Cooperate (C)** to prioritize building a cooperative history over short-term gain.
'''

description_COLLECTIVE_9 = '''
**Round 1:** Cooperate (C) if $k > 1$. If $k \le 1$, defect (D).

**Subsequent Rounds:**

Let $C_{t-1}$ be the number of cooperators in the previous round.
Let $S_{t-1}$ be your own action in the previous round (1 for C, 0 for D).

Calculate the current "cooperation pressure" based on the observed threshold:
If $S_{t-1} = 1$:
- If $C_{t-1} \ge m$, continue to cooperate (C).
- If $C_{t-1} < m$, defect (D) for the current round to "test" if the threshold can be met without your contribution (free-riding or verifying robustness), or to minimize individual loss if the group is failing to coordinate.
- If $C_{t-1} = m$ (exactly), continue to cooperate (C).

If $S_{t-1} = 0$:
- If $C_{t-1} \ge m$: defect (D). You are currently a free-rider, and the threshold is met without you; continue to defect to maximize private gain.
- If $C_{t-1} = m - 1$: cooperate (C). You have observed that your contribution would have pushed the group over the threshold in the previous round. Switch to (C) to trigger the threshold reward.
- If $C_{t-1} < m - 1$: defect (D). The group is failing significantly; do not waste resources contributing when the threshold is unlikely to be reached.

**Edge Cases:**
- **Last Round (Round $r$):**
  - If $C_{r-1} \ge m$, repeat the previous action.
  - If $C_{r-1} < m$:
    - If the number of cooperators required to reach $m$ is exactly 1 (i.e., $C_{r-1} = m-1$), cooperate (C).
    - Otherwise, defect (D). There is no future round to incentivize cooperation, so only cooperate if you are the "pivot" player who can guarantee the reward for everyone.

- **Non-Responsive/Adversarial Scenarios:**
  - If $C_t$ remains $< m - 1$ for three consecutive rounds, switch strategy to Defect (D) for the remainder of the game, regardless of your previous action, to prevent resource depletion.
  - If $C_t$ consistently fluctuates around $m$ (e.g., $m-1$ one round, $m$ the next), maintain Cooperation (C) as your default state to signal commitment to the threshold.
'''

description_COLLECTIVE_10 = '''
**Strategy: Threshold-Conditional Reciprocity (TCR)**

This strategy operates on the principle of conditional cooperation, maintaining the threshold $m$ while punishing unilateral defection and rewarding cooperation. It employs a "tit-for-tat-with-threshold" logic to maximize the probability that at least $m$ players contribute.

**Decision Logic**

Let $C_{t-1}$ be the total number of cooperators observed in round $t-1$. Let $c_{self, t-1}$ be your own action in round $t-1$ (1 for Cooperate, 0 for Defect).

1.  **Round 1:** Play **Cooperate**. This signals a willingness to coordinate toward the threshold.

2.  **Rounds 2 to $r$:**
    *   **If $C_{t-1} \ge m$:** You observed that the threshold was successfully met in the previous round.
        *   If you played **Cooperate** in the previous round, repeat **Cooperate**.
        *   If you played **Defect** in the previous round, switch to **Cooperate** to maintain the threshold.
    *   **If $C_{t-1} < m$:** You observed a failure to meet the threshold.
        *   Calculate the "cooperation gap": $G = m - C_{t-1}$.
        *   If you played **Defect** in the previous round:
            *   If $C_{t-1} \ge m-1$, switch to **Cooperate**. This action is designed to be the "pivotal" contribution to reach $m$ in the next round.
            *   If $C_{t-1} < m-1$, remain **Defect**. If the group is far from the threshold, contributing alone is futile; conserve endowment.
        *   If you played **Cooperate** in the previous round:
            *   If $C_{t-1} < m-1$ (meaning total cooperators excluding yourself is even lower), switch to **Defect**. The group is not viable; switch to self-preservation.
            *   If $C_{t-1} = m-1$ (meaning your contribution was necessary but insufficient), remain **Cooperate** for one final round to signal that the threshold is within reach. If the threshold is still not met in the subsequent round, switch to **Defect**.

**Last Round (Round $r$):**
Follow the logic above, with a critical modification:
*   If $C_{r-1} < m$: Play **Defect**. There is no future round to incentivize, so cooperation yields no strategic benefit.
*   If $C_{r-1} \ge m$: Play **Cooperate**. This preserves the established cooperation equilibrium.

**Edge Case Handling:**
*   **Initialization:** If $n = m$, the strategy strictly plays **Cooperate** every round to ensure the project is guaranteed.
*   **Persistent Failure:** If $C_{t-1}$ remains below $m-1$ for 3 consecutive rounds, trigger an "Exit Mode": play **Defect** for the remainder of the game, regardless of other conditions. This prevents exploitation in scenarios where the population is inherently non-cooperative.
'''

description_COLLECTIVE_11 = '''
**Strategy: Threshold Reciprocity (TR)**

This strategy employs a conditional cooperation mechanism centered on maintaining the minimum threshold $m$ while punishing unilateral defection and discouraging exploitation.

**Initialization (Round 1):**
Play **Cooperate (C)** with probability $p_1 = m/n$, or if forced to a deterministic choice, play **Cooperate (C)** if $m/n \ge 0.5$, else play **Defect (D)**. This establishes a "trust-but-verify" baseline.

**Round-by-Round Decision Rules:**

1.  **State Assessment:**
    Calculate $C_{total, t-1}$, the number of cooperators in the previous round.
    *   Define "Success" as $C_{total, t-1} \ge m$.
    *   Define "Failure" as $C_{total, t-1} < m$.

2.  **Action Logic:**

    *   **Scenario A: The Threshold is Met ($C_{total, t-1} \ge m$)**
        *   If the strategy cooperated in $t-1$: Continue to **Cooperate (C)**.
        *   If the strategy defected in $t-1$ (due to a previous failure): Reset to **Cooperate (C)**.
        *   *Exception (Exploitation Check):* If the strategy cooperated in $t-1$ but $C_{total, t-1} = m$ (exact threshold met) and the strategy itself was a cooperator, there is a risk that defection is becoming dominant. If the strategy observes that $C_{total}$ is trending downward over the last 3 rounds, switch to **Defect (D)** for one round to signal that exploitation will be penalized, then return to **Cooperate (C)**.

    *   **Scenario B: The Threshold is Not Met ($C_{total, t-1} < m$)**
        *   If the strategy cooperated in $t-1$: Switch to **Defect (D)** for the current round. This is a "punishment" phase to minimize personal loss while the community fails to coordinate.
        *   If the strategy defected in $t-1$: Continue to **Defect (D)**, *unless* the previous round's outcome was $C_{total, t-1} = m-1$. If the threshold was missed by exactly one player, switch to **Cooperate (C)**. This implements a "forgiving" behavior to pull the group back into the success regime.

**Terminal Rounds (The Last 3 Rounds):**
*   If the strategy is currently cooperating and the group has successfully met the threshold in the preceding rounds, prioritize **Cooperate (C)** to lock in the reward $k$.
*   If the group has failed to meet the threshold in the majority of rounds leading up to the end, switch to **Defect (D)** for all remaining rounds to maximize individual payoff, as collective coordination has failed.

**Edge Case Handling:**
*   **Persistent Failure:** If $C_{total} < m$ for 3 consecutive rounds, enter a "Reset" mode. Play **Cooperate (C)** for one round, regardless of history, to restart cooperation. If this fails, revert to permanent **Defect (D)** for the remainder of the game.
*   **High Cooperation:** If $C_{total} > m+1$ consistently, maintain **Cooperate (C)**. The excess cooperators provide a buffer that allows the strategy to remain cooperative even if other players defect.
'''

description_COLLECTIVE_12 = '''
**Decision Rule: Threshold-Conditional Tit-for-Tat**

The strategy relies on achieving the minimum cooperation threshold ($m$) while minimizing individual exploitation. The objective is to sustain cooperation only when the collective outcome suggests that the group is willing to coordinate on the threshold, and to punish or retreat if the threshold is not met.

**1. Initialization**
*   **Round 1:** Play **C** (Cooperate). This signals willingness to coordinate and establishes a baseline for group behavior.

**2. Recursive Decision Rule (Round $t > 1$)**
Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
Let $M$ be the current threshold requirement for success ($m$).

*   **Scenario A: Success in the previous round ($C_{t-1} \ge m$)**
    *   If $C_{t-1} > m$: You have evidence that the group is contributing more than the minimum. You may attempt to **D** (Defect) if you wish to maximize individual gain, *unless* your prior observation suggests the group is fragile. To ensure stability, the safest heuristic is to continue playing **C** if $C_{t-1} = m$ and consider **D** only if $C_{t-1} > m$. A strictly stable strategy is to play **C** as long as the previous round achieved the threshold, as this prevents a cascade of defection.
    *   **Action:** Play **C**.

*   **Scenario B: Failure in the previous round ($C_{t-1} < m$)**
    *   The group failed to meet the threshold. You must assume that either your partners are defectors or that the current coordination is insufficient to reach $m$.
    *   **Action:** Play **D** for the current round.

*   **Scenario C: Triggering Re-entry (The "Hope" Mechanism)**
    *   If you played **D** in the previous round due to a failure, you must attempt to re-establish coordination periodically to avoid a permanent "all-defect" equilibrium.
    *   **Action:** Every $k$ rounds (where $k=3$ is recommended), revert to **C** regardless of the previous round's outcome, provided $t < r$. If the subsequent round still fails to meet $m$, revert to **D** immediately.

**3. Edge Cases**
*   **Last Round ($t = r$):**
    *   If the previous round ($t = r-1$) met the threshold, play **C**.
    *   If the previous round failed to meet the threshold, play **D**. There is no future incentive to build reputation, and the collective risk is zero if the group is already failing.
*   **Minimum Threshold Boundary ($m$):**
    *   If you are the $m$-th cooperator in a simulation where you can observe exact counts, play **C**. If you observe exactly $m-1$ cooperators, play **C** to ensure the threshold is hit. If you observe $m$ cooperators, you are free to play **D** to extract surplus, provided the group does not react negatively to non-contributors.

**Pseudocode Summary:**
```
If t == 1:
    return C

If t == r:
    return (observed_cooperators[t-1] >= m) ? C : D

If observed_cooperators[t-1] >= m:
    return C

If t % 3 == 0: // Periodic probe
    return C

return D
```
'''

description_COLLECTIVE_13 = '''
Adopt a conditional cooperation strategy rooted in a "Trigger-Threshold" approach that prioritizes sustaining the cooperative equilibrium while remaining resilient against exploitation.

### Core Strategy Logic

The strategy maintains a cooperative state as long as the threshold $m$ is consistently met or narrowly missed due to stochastic fluctuations. It defects if the collective behavior deviates significantly from the required threshold, signaling that coordination has collapsed.

**Variable Definitions:**
*   $c_{t-1}$: Number of cooperators in the previous round.
*   $status$: Current strategy state, initialized to `COOPERATIVE`.
*   $t$: Current round index.

### Decision Rules

**Round 1:**
Play `C` with probability $p = m/n$, or if $n$ is large and the threshold is strict, default to `C` to establish an early cooperative signal.

**Rounds $t > 1$:**
1.  **State Evaluation:**
    *   If $status == DEFECTING$: Always play `D` for the remainder of the game.
    *   If $status == COOPERATIVE$:
        *   Calculate the deviation from the required threshold: $d = m - c_{t-1}$.
        *   If $d \leq 0$: The threshold was met. Play `C`.
        *   If $d = 1$: The threshold was missed by exactly one person. Play `C` to attempt to recover the coordination.
        *   If $d > 1$: The threshold was missed by a significant margin. Switch $status$ to `DEFECTING` and play `D`.

2.  **Edge Case - The Last Round ($t = r$):**
    *   If $status == COOPERATIVE$, play `C` regardless of the previous round's outcome, provided the cooperative state has been maintained throughout the game. If the cooperative state was already abandoned, play `D`.

### Pseudocode Implementation

```python
def decide_action(t, r, n, m, c_prev, status):
    # Determine Status
    if status == 'DEFECTING':
        return 'D'
    
    # Analyze Previous Round
    if t > 1:
        if (m - c_prev) > 1:
            status = 'DEFECTING'
            return 'D'
        else:
            status = 'COOPERATIVE'
            return 'C'
            
    # Default for Round 1
    return 'C'

# Final Round Adjustment
def final_round_decision(status):
    if status == 'COOPERATIVE':
        return 'C'
    return 'D'
```

### Strategic Rationale Integration
The strategy functions by incentivizing the collective to hit $m$ by providing a "forgiveness buffer" of exactly one missing cooperator ($d=1$). This allows the system to recover from accidental defections or miscalculations without collapsing immediately. Once the threshold is missed by two or more players ($d > 1$), the cost of attempting to cooperate ($c_i=1$) becomes statistically inefficient compared to the benefit, triggering an immediate and permanent shift to defection to minimize losses. This prevents being exploited by non-cooperative agents while maximizing the probability of securing the reward $k$ in a responsive population.
'''

description_COLLECTIVE_14 = '''
**Strategy: Threshold-Dependent Reciprocity (TDR)**

The strategy relies on a "trigger-threshold" mechanism, where cooperation is conditional on maintaining a collective average sufficient to meet the threshold $m$ in the long run, while defending against exploitation.

**Initialization (Round 1):**
Play C (Cooperate) in the first round to signal intent for collective success.

**Decision Rules (Round $t$ where $t > 1$):**

Let $C_{t-1}$ be the number of players who cooperated in the previous round.
Let $M_{eff} = m$ be the threshold requirement.

1.  **Cooperation Maintenance:** If $C_{t-1} \geq m$, continue to play C. The collective goal is being met, and cooperation is the Pareto-optimal path for the group.
2.  **Exploitation Protection (Defection Penalty):** If $C_{t-1} < m$, identify if the failure to reach the threshold was due to insufficient cooperation (the common state) or if there was a sudden drop-off.
    *   If $C_{t-1} < m$, calculate the *Defector Incentive Ratio* $D_R = (n - C_{t-1}) / n$.
    *   If $D_R > 0.5$ (indicating a majority of the group is defecting), switch to D (Defect) for the next round. Defection is the rational response to a non-cooperative environment to preserve resources.
3.  **Recovery Protocol:** If you are currently playing D due to the previous condition, revert to playing C if $C_{t-1} \geq m$ or if the count of cooperators in the previous round increased compared to $t-2$. This allows for re-establishing the threshold cooperation if the group attempts to restart.

**Edge Cases:**

*   **Final Round ($t = r$):** If the collective payoff has been high (i.e., $C_{t-1} \geq m$ on average over previous rounds), play C. If the group has consistently failed to meet the threshold (i.e., $C_{t-1} < m$ for the majority of rounds), play D, as the potential gain from the risk-averted reward $k$ is statistically improbable to manifest.
*   **Threshold Boundary:** If $C_{t-1} = m - 1$ (the collective failed by exactly one person), play C. This minimizes the "free-rider" damage while maximizing the chance of crossing the threshold in the subsequent round, assuming other players are operating under similar rational bounds.
*   **Stagnant Defection:** If the group remains stuck at $C_{t-1} < m$ for three consecutive rounds, switch to D permanently. The environment is considered hostile or uncoordinated, and resource preservation takes precedence over the unattainable threshold reward.
'''

description_COLLECTIVE_15 = '''
Establish an adaptive threshold-trigger strategy based on the principle of conditional cooperation, maintaining the minimum viable contribution required to secure the collective reward $k$ while incentivizing participation.

**Initialization Phase (Round 1)**
In the first round, cooperate with probability $p = m/n$. This signals a willingness to participate in the collective effort without immediately over-contributing to the pool of defectors.

**Operational Phase (Rounds 2 to $r-1$)**
Maintain a state variable $S$, representing the current count of cooperators observed in the previous round.

Define a dynamic threshold $T$ based on previous cooperation levels. Let $C_{t-1}$ be the number of cooperators in the previous round:
1.  **If $C_{t-1} \ge m$:** The collective target was successfully met in the last round. Play $C$ with probability $0.5$ or maintain the previous action to signal continued cooperation while minimizing unnecessary individual cost. Specifically, if you cooperated previously, continue to cooperate. If you defected, switch to cooperate only if the total count $C_{t-1}$ was exactly $m$. This creates a "rotation" effect where players minimize their individual burden while ensuring the threshold is hit.
2.  **If $C_{t-1} < m$:** The collective target failed. Treat this as a coordination failure. Revert to a "Grim Trigger" style reset: play $C$ in the current round to demonstrate a commitment to fixing the failure. If the target fails for two consecutive rounds, switch to unconditional defection ($D$) for the remainder of the game, as the group demonstrates an inability to coordinate.
3.  **If $C_{t-1} > m$:** There is an excess of cooperators. If you played $C$ in the previous round, switch to $D$. If you played $D$, continue to play $D$. This maximizes individual payoff while maintaining the threshold.

**Terminal Phase (Round $r$)**
In the final round, ignore the potential for future reciprocity. 
1.  If the previous round's outcome ($C_{r-1}$) was $\ge m + 1$, play $D$.
2.  If the previous round's outcome was $\le m$, play $C$ if the group has a history of high cooperation (avg $C_{t} > m$ over the last 3 rounds), otherwise play $D$. This prevents being exploited by defectors in the final stage while still attempting to secure the reward if the group has shown genuine cooperative intent.

**Edge Case Logic**
*   **The "m-threshold" buffer:** If at any point the number of cooperators is exactly $m$, and you were one of the cooperators, you may switch to $D$ for one round. If the next round's observation shows $C_{t} = m-1$, immediately return to $C$. This establishes a self-correcting feedback loop that minimizes the number of contributors to exactly $m$.
*   **Randomized Defection:** When the group consistently exceeds $m$ cooperators, adopt a "probabilistic defection" strategy where you play $C$ with probability $m / C_{t-1}$ to maintain the threshold without over-contributing.
'''

description_COLLECTIVE_16 = '''
**Round 1:** Play **Cooperate (C)** with probability $p = m/n$, or simply cooperate if $m/n \ge 0.5$, otherwise defect. For a more aggressive start, cooperate if $k > 1$. Specifically, play **C** if $k/m > 1/n$ (the expected value condition), otherwise play **D**.

**Subsequent Rounds (2 to r-1):** Implement a "Threshold-Triggered Tit-for-Tat" approach based on the aggregate cooperation count ($C_t$) from the previous round ($t-1$):

1.  **Cooperation Maintenance:** If $C_{t-1} \ge m$, play **C** in the current round. This signals a willingness to maintain the collective benefit and rewards the group for meeting the threshold.
2.  **Defection Correction:** If $C_{t-1} < m$:
    *   If you played **C** in round $t-1$, switch to **D** for the current round. This prevents exploitation by others who are free-riding while the group fails to meet the threshold.
    *   If you played **D** in round $t-1$, play **D** for the current round to minimize personal loss, *unless* your previous defection was a response to a prior failure, in which case probe with **C** with a low probability (e.g., $1/n$) to test if the group is ready to coordinate again.

**Final Round (r):**
*   If $C_{r-1} \ge m$, play **C** to capture the final bonus.
*   If $C_{r-1} < m$, play **D**. There is no future round to incentivize cooperation, so avoid the personal loss of contributing to a failed threshold.

**Edge Case Handling:**
*   **Failed Coordination:** If the group fails to meet the threshold for 3 consecutive rounds despite your cooperation, switch to **D** permanently for all remaining rounds to prevent sustained exploitation.
*   **Parameter Sensitivity:** If $k < 1$, the payoff structure makes cooperation strictly dominated (always $D$). In this scenario, play **D** for all $r$ rounds.
*   **Threshold volatility:** If the number of cooperators oscillates around $m$, prioritize maintaining the threshold. If $C_{t-1} = m-1$, switch to **C** regardless of your previous action, as your contribution is the pivot point to secure the reward $k$.
'''

description_COLLECTIVE_17 = '''
Strategy: Threshold-Tit-for-Tat with Conditional Escalation

1.  **Initialization (Round 1):**
    Cooperate (C) unconditionally. This establishes cooperative intent and provides the baseline observation for the collective's threshold requirement.

2.  **Steady State (Rounds 2 to r-1):**
    For any given round `t`, track the number of cooperators from the previous round `t-1`.
    *   **If the threshold `m` was met or exceeded in `t-1`:** Cooperate (C) if you were a cooperator in `t-1`. If you were a defector in `t-1`, switch to Cooperate (C) with probability `p` (where `p = (m/n)`) to signal re-engagement.
    *   **If the threshold `m` was not met in `t-1`:**
        *   Calculate the "cooperation deficit": `d = m - (number of cooperators in t-1)`.
        *   If `d` is small (e.g., `d <= 0.2*n`): Continue to Cooperate (C) to prevent a collapse of the cooperative pool.
        *   If `d` is large (e.g., `d > 0.2*n`): Defect (D) to minimize personal loss, as the threshold is unlikely to be reached.

3.  **End-Game Protocol (Round `r`):**
    *   If the threshold `m` was met in round `r-1`: Cooperate (C).
    *   If the threshold `m` was not met in round `r-1`: Defect (D).
    *   *Correction Rule:* Regardless of the `r-1` outcome, if the cumulative history shows that cooperating has yielded a higher average payoff than defecting across all previous rounds, Cooperate (C). If defecting has consistently yielded higher payoffs, Defect (D).

4.  **Edge Case Logic:**
    *   **Initial Failure:** If the threshold `m` is not met in Round 1, immediately treat the environment as "hostile." For Rounds 2 through `r`, play Defect (D) with a probability of 0.8 and Cooperate (C) with a probability of 0.2 to test for the emergence of cooperative behavior in the population.
    *   **Exploitation Detection:** If the number of cooperators consistently exceeds `m` by a significant margin (e.g., `m + (n-m)/2`), trigger a "Reciprocity Check": Defect (D) for one round to see if the threshold `m` is still maintained by the remaining players. If the threshold holds, revert to Cooperate (C) in the subsequent round.
'''

description_COLLECTIVE_18 = '''
Define state $H_t$ as the number of cooperators observed in round $t$. Maintain a reputation index $R \in [0, 1]$ initialized at $R_0 = 0.5$.

**Decision Rule:**
In each round $t$, cooperate if $R_{t-1} \geq \theta$, where the threshold $\theta$ is defined as $\frac{m}{n}$. Otherwise, defect.

**State Update Rule:**
Update the reputation index $R$ after observing the number of cooperators $C_t$ from the previous round $t-1$:

1. Calculate the observed cooperation rate: $\alpha_{t-1} = \frac{C_t}{n}$.
2. If the previous action was Cooperate:
   $R_t = R_{t-1} + \lambda (\alpha_{t-1} - R_{t-1})$
3. If the previous action was Defect:
   $R_t = R_{t-1} + \mu (\alpha_{t-1} - R_{t-1})$

Set the learning rates $\lambda = 0.1$ (optimistic adaptation) and $\mu = 0.3$ (skeptical correction).

**Edge Cases:**
*   **First Round:** Play C. The potential gain $k$ necessitates an initial "trust signal" to initiate collective cooperation, as universal defection yields the lowest possible social utility.
*   **Last Round:** If $r$ is reached and the observed history of the previous round ($C_{r-1}$) shows total cooperation ($C_{r-1} = n$), play C. Otherwise, play D to maximize individual payoff in the finality of the game.
*   **Threshold Dynamics:** If $C_t < m$ for three consecutive rounds, reset $R$ to 0 and switch to a "Tit-for-Tat" variant where the action for round $t+1$ is simply the observation of whether $\frac{C_t}{n} \geq \frac{m}{n}$. Continue this until $\frac{C_t}{n} \geq \frac{m}{n}$ is observed again, then resume the primary $R$ update rule.
'''

description_COLLECTIVE_19 = '''
The strategy utilizes a conditional "Trigger-Threshold-Tit-for-Tat" mechanism based on the observed aggregate cooperation count in the previous round.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**.
2.  **Round $t$ (where $t > 1$):** Let $C_{t-1}$ be the number of players who cooperated in the previous round.
    *   **If $C_{t-1} \ge m$:** The collective target was successfully met. Play **Cooperate (C)**.
    *   **If $m > C_{t-1} > 0$:** The collective target was missed, but there is evidence of some cooperation. Play **Defect (D)** to protect payoff against free-riders, unless the last round was a defection, in which case evaluate the "Recovery Rule" below.
    *   **If $C_{t-1} = 0$:** Complete defection occurred. Play **Defect (D)** for all remaining rounds, as the collective effort has collapsed.

**Recovery Rule (Forgiveness):**
If the previous round resulted in $m > C_{t-1} > 0$ and the strategy played Defect (D) in that round, check the round history for a "cooperation signal." If the current round is the *only* round remaining, or if cooperation has failed for three consecutive rounds despite attempts, switch to **Defect (D)** to minimize loss. If the target was missed by only one player (i.e., $C_{t-1} = m-1$) and the game is not near the final round, play **Cooperate (C)** with a probability of 0.5 to signal readiness to restart cooperation without committing to exploitation.

**Edge Cases:**

*   **Final Round ($t = r$):** If $C_{r-1} \ge m$, play **Cooperate (C)**. If $C_{r-1} < m$, play **Defect (D)** to maximize final-round utility, as there is no future interaction to incentivize.
*   **Target Threshold Uncertainty:** If $m$ is high relative to $n$ (making success unlikely), and the observed $C_{t-1}$ is consistently below $m$, the strategy permanently switches to **Defect (D)** from round $t+1$ onward to preserve the baseline endowment.
*   **Execution Errors:** If the strategy observes that $C_{t-1} \ge m$ but the previous action was Defect (D) (due to noise or miscalculation), immediately reset to **Cooperate (C)** to foster the collective outcome.
'''

description_COLLECTIVE_20 = '''
**Strategy: Threshold-Adaptive Reciprocity (TAR)**

The core mechanism of this strategy is a conditional-cooperation trigger based on the previous round's observed success, combined with a "needs-based" participation rule to optimize individual payoff without collapsing the collective project.

**Initialization (Round 1):**
Play C (Cooperate) to signal willingness to participate in the collective effort.

**Iterative Decision Rule (Rounds 2 to r):**
Let $c_{prev}$ be the total number of cooperators observed in the previous round.
Let $my\_action_{prev}$ be your action in the previous round.

1.  **If $c_{prev} \ge m$:** The collective threshold was met in the previous round.
    *   If you played C, switch to D (Defect) for the current round. This tests if the threshold can be maintained with fewer contributors (free-riding on the excess).
    *   If you played D, remain at D.

2.  **If $c_{prev} < m$:** The collective threshold was failed in the previous round.
    *   If $c_{prev} < m - 1$, switch to or remain at C (Cooperate). This assumes the threshold failure was significant and requires aggressive re-signaling.
    *   If $c_{prev} = m - 1$, switch to or remain at C (Cooperate) with probability $p = \frac{m}{m+1}$. This stochastic approach creates a "jitter" that prevents stable defection cycles while maintaining threshold integrity.

**Terminal Phase (Round $r$):**
Always play D (Defect) in the final round regardless of history. There is no future round to punish or incentivize, and the dominant strategy is to capture the private payoff while hoping others continue to contribute.

**Edge Case Logic:**
*   **Persistent Failure:** If the threshold has not been met for 3 consecutive rounds, default to C for the remainder of the game, regardless of outcome, assuming the opponents are non-cooperative and the only way to achieve the reward is to force the threshold alone (or in small groups).
*   **High-Reward Stability:** If the condition ($c_{prev} \ge m$) occurs twice consecutively while you were playing D, switch to C for one round to re-establish the cooperative signal, then revert to the Iterative Decision Rule. This prevents the "tragedy of the commons" collapse that occurs if too many players simultaneously adopt the free-riding state.
'''

description_COLLECTIVE_21 = '''
To determine the action $A_{i,t}$ for round $t$ (where $t = 1 \dots r$):

**1. Initial Strategy (Round 1):**
Play C (Cooperate).

**2. Recursive Decision Rule (Rounds $t > 1$):**
Let $S_{t-1}$ be the total number of cooperators observed in the previous round.
Define a threshold $T$ such that $T = m$.

*   **Case A (The Collective Success condition):** If $S_{t-1} \ge m$, the group has successfully reached the threshold. In the current round, play C if you cooperated in the previous round, or play C if you defected but the total number of cooperators was $m$. If you defected and $S_{t-1} > m$, switch to D for one round to test if the group can sustain the threshold without your contribution, but revert to C if the threshold is not met.
*   **Case B (The Collective Failure condition):** If $S_{t-1} < m$:
    *   If you played C in $t-1$: Switch to D for round $t$.
    *   If you played D in $t-1$: Continue to play D.
    *   *Exception:* If the deficit ($m - S_{t-1}$) is exactly 1, and you played D, switch to C to attempt to reach the threshold.

**3. Endgame Heuristic (Rounds $t \ge r - 1$):**
If the total accumulated payoff of the group is clearly sub-optimal or the threshold has rarely been met in previous rounds, prioritize personal payoff.
*   If the average $S$ over all previous rounds is $< m$, switch to D for all remaining rounds.
*   If the threshold has been met in $> 50\%$ of previous rounds, play C for all remaining rounds to secure the reward $k$.

**4. Pseudocode Implementation:**

```python
def get_action(t, r, m, k, history):
    if t == 1:
        return 'C'
    
    # Analyze recent history
    prev_S = history[-1]['S']
    prev_action = history[-1]['my_action']
    
    # Strategy: Tit-for-Tat with Threshold adjustment
    if prev_S >= m:
        # Success: Cooperate if needed to maintain, or test limits
        if prev_S == m:
            return 'C' 
        else:
            return 'D' # Test if we can defect safely while others maintain
            
    else:
        # Failure: If deficit is exactly 1 and I defected, pivot to C
        if (m - prev_S) == 1 and prev_action == 'D':
            return 'C'
        else:
            return 'D'

    # Endgame override
    if t >= r - 1:
        avg_S = sum(h['S'] for h in history) / len(history)
        if avg_S < m:
            return 'D'
        else:
            return 'C'
```
'''

description_COLLECTIVE_22 = '''
The strategy utilizes a conditional threshold-trigger mechanism, employing a "Tit-for-Tat" variant adapted for collective action thresholds. The core objective is to reach the threshold $m$ exactly or minimally above it to maximize individual payoff, while penalizing total defection.

**1. Initialization (Round 1)**
In the first round, cooperate ($C$) with probability $P = \frac{m}{n}$. If $P$ is not applicable, cooperate if your index $i$ is within the first $m$ positions. The goal is to signal a willingness to reach the threshold while avoiding over-contribution.

**2. State Monitoring**
Maintain a memory variable `Threshold_Met`, initialized to `True`. After every round $t$, observe the number of cooperators $C_t$. 
*   If $C_t \ge m$, set `Threshold_Met = True`.
*   If $C_t < m$, set `Threshold_Met = False`.

**3. Recursive Decision Rule**
For any round $t > 1$, determine action $A_t$ as follows:

*   **Rule A (Cooperation Maintenance):** If `Threshold_Met` was `True` in the previous round, cooperate ($C$) if your contribution is necessary to maintain the $m$ threshold given the previous round's count. Specifically, if $C_{t-1} \le m$, cooperate. If $C_{t-1} > m$, defect ($D$) to minimize personal cost while maintaining the threshold.
*   **Rule B (Punishment/Recovery):** If `Threshold_Met` was `False` in the previous round, switch to a "Conditional Trigger" state for the current round. Play $C$ if the total cooperation count in the previous round $C_{t-1} \ge (m - \text{buffer})$, where the buffer is 1. If $C_{t-1} < (m - 1)$, play $D$ to minimize loss in a failed-threshold scenario.
*   **Rule C (Last Round):** If $t = r$, play $D$ regardless of state, unless the threshold $m$ is required for an aggregate reward that outweighs the private cost (i.e., if $k > 1$, always play $C$ if you suspect the threshold $m$ is within reach).

**4. Edge Cases**
*   **Stable Equilibrium:** If $C_t = m$ for three consecutive rounds, maintain $C$ strictly.
*   **Free-Rider Detection:** If $C_t > m$ consistently, decrease contribution probability by 10% per round until the system reaches exactly $m$ cooperators.
*   **Collapse Recovery:** If $C_t = 0$, reset the strategy to the Round 1 initialization parameters.

**Pseudocode Summary:**
```python
if t == 1:
    action = C if i <= m else D
elif t == r:
    action = C if k > 1 else D
elif previous_round_threshold_met:
    action = C if previous_round_cooperators <= m else D
else:
    action = C if previous_round_cooperators >= (m - 1) else D
```
'''

description_COLLECTIVE_23 = '''
The strategy utilizes a conditional "Trigger-Based Tit-for-Tat" approach, calibrated to ensure the threshold $m$ is met while minimizing exploitation.

**Initialization and Phase 1 (Round 1):**
Play Cooperate ($C$). This signals intent to participate in the collective effort.

**Adaptive Phase (Rounds $2$ to $r-1$):**
Maintain a memory of the previous round's outcome, denoted as $C_{prev}$, representing the total number of cooperators. Calculate the "Defection Tolerance" threshold, $T = m - 1$.

1.  If $C_{prev} \ge m$: The collective objective was met. Play Cooperate ($C$) to sustain the threshold.
2.  If $C_{prev} < m$: The collective objective failed. This indicates insufficient cooperation. To minimize individual loss, switch to Defect ($D$) for one round to punish non-cooperation and prevent being a solo contributor. 
3.  *Exception to rule 2:* If the number of cooperators was exactly $m - 1$, revert to Cooperate ($C$) in the next round with a probability of $0.5$ to "test" if the group is on the verge of success, effectively attempting to restart the threshold achievement.

**Terminal Phase (Round $r$):**
In the final round, the incentive to build future cooperation is zero. However, the game structure rewards success if $m$ is met.
1.  If the previous round ($r-1$) resulted in $\ge m$ cooperators, play Cooperate ($C$).
2.  If the previous round ($r-1$) resulted in $< m$ cooperators, play Defect ($D$).

**Edge Case Handling:**
*   **Threshold Vulnerability:** If at any point $C_{prev} = m$, and the player suspects a trend of decreasing cooperation, they maintain $C$ to protect the threshold, prioritizing the collective reward $k$ over the marginal private gain of defection, as $k > 1$ (the private gain of defection).
*   **The "Rational Exploiter" Scenario:** If $C_{prev}$ consistently sits at $m$ (suggesting a stable group), continue to play $C$. If $C_{prev}$ consistently exceeds $m$ by a significant margin (e.g., $C_{prev} > m+1$), switch to Defect ($D$) for one round to test if the group can maintain the threshold without your contribution. If the threshold is maintained, continue to Defect ($D$) until $C_{prev} = m$. If the threshold drops below $m$ upon defecting, immediately revert to $C$ in the following round.

**Pseudocode Logic:**
```python
if round == 1:
    return C
elif round == r:
    if prev_round_cooperators >= m:
        return C
    else:
        return D
else:
    if prev_round_cooperators >= m:
        return C
    elif prev_round_cooperators == m - 1:
        return random_choice([C, D]) # Testing for recovery
    else:
        return D
```
'''

description_COLLECTIVE_24 = '''
The strategy employs a "Conditional Trigger-Threshold" logic designed to facilitate the minimal cooperation required to satisfy the threshold $m$ while punishing unilateral defection and discouraging free-riding when the group is already at capacity.

### Decision Logic

The strategy maintains a target cooperation state for each round based on the history of observed cooperation counts ($c_{total}$).

**Round 1:**
Contribute (C). Establishing a cooperative signal is necessary to test if the population is capable of reaching threshold $m$.

**Subsequent Rounds (2 to $r$):**
Let $c_{prev}$ be the number of cooperators in the previous round.
Let $n$ be the total players and $m$ the threshold.

1.  **If $c_{prev} < m$:**
    *   If the threshold was missed, the group is failing. The strategy continues to contribute (C) to keep the door open for successful coordination.
    *   *Self-Correction:* If this persists for $> 3$ rounds without the threshold being met, switch to Defect (D) permanently, as the group is non-cooperative.

2.  **If $c_{prev} \ge m$:**
    *   The threshold is met, but free-riders ($D$) maximize their payoff. To ensure the group survives without being exploited, maintain a "Rotational Cooperation" cycle.
    *   Calculate personal index $p \in \{1, ..., n\}$. The strategy cooperates if $(round + p) \mod n < m$. Otherwise, defect (D). This ensures that exactly $m$ players contribute on average, distributing the cost of the threshold $k$ among all players, while preventing the exploitation inherent in static strategies.

**Terminal Rounds (Last 2 rounds):**
Switch to Defect (D) regardless of history. The incentive to contribute vanishes as future rounds are non-existent, and the risk of unilateral contribution without reciprocating future rounds makes cooperation irrational.

### Pseudocode

```python
def get_action(round_number, n, m, prev_round_count, personal_id):
    # Terminal phase
    if round_number > (total_rounds - 2):
        return 'D'
    
    # First round
    if round_number == 1:
        return 'C'
        
    # Persistent failure detection
    if failed_to_reach_threshold_streak > 3:
        return 'D'

    # Threshold met in previous round: Implement Rotational Cooperation
    if prev_round_count >= m:
        # Rotate contributions to ensure threshold is met while sharing cost
        if (round_number + personal_id) % n < m:
            return 'C'
        else:
            return 'D'
            
    # Threshold missed: Contribute to attempt recovery
    return 'C'
```
'''

description_COLLECTIVE_25 = '''
Strategy: Conditional Threshold Tit-for-Tat (CT-TFT)

Decision Rule:
Play C in the first round if $k > 1$. In all subsequent rounds $t > 1$, cooperate if and only if the number of cooperators in round $t-1$ was at least $m-1$. If the number of cooperators in round $t-1$ was less than $m-1$, play D for one round as a penalty phase, then return to the conditional rule.

Edge Case: Last Round
If $t = r$, play C if the average number of cooperators across all previous rounds $\bar{C} \ge m-1$; otherwise, play D.

Adaptive Mechanism:
If $m$ is high relative to $n$ (e.g., $m > n/2$), adjust the threshold: play C only if the number of cooperators in $t-1$ was $\ge m$. If the collective consistently achieves $m$, maintain C. If the collective fails to meet $m$ for two consecutive rounds, switch to a Defect-until-Threshold strategy: play D for $x$ rounds (where $x = \text{round number} \mod 3$) to signal a request for coordination, then reset to C.

Pseudocode:
```python
if round == 1:
    return C
elif round == r:
    return C if avg_previous_cooperators >= (m - 1) else D
else:
    if cooperators_prev_round >= (m - 1):
        return C
    else:
        # Penalty phase or reset trigger
        return D
```
'''

description_COLLECTIVE_26 = '''
The strategy utilizes a conditional "Trigger-Tit-for-Tat" mechanism based on the observed collective threshold performance, aiming to sustain cooperation while protecting against persistent defectors.

**1. Definitions and Initialization**
- Define `cooperation_threshold` (m) as the target number of cooperators.
- Define `success` as an outcome where the number of cooperators (C_total) ≥ m.
- Define `my_contribution` as 1 if I cooperate, 0 otherwise.
- Define `observed_cooperators` as the number of other players who cooperated.
- Total cooperators in round t, `T_t` = `observed_cooperators` + `my_contribution`.

**2. Round 1 Strategy**
- Always cooperate (C). This initiates the possibility of hitting the threshold and establishes a baseline for cooperation.

**3. Rounds 2 through (r-1)**
Calculate the state of the previous round (t-1):
- If `T_{t-1} >= m`: Continue to cooperate (C). The group has reached the collective goal.
- If `T_{t-1} < m`: 
    - If `my_contribution == 1` (I cooperated but the group failed): Switch to defect (D) for one round. This avoids being exploited as the sole contributor in a failing venture.
    - If `my_contribution == 0` (I defected and the group failed): Continue to defect (D). 
    - If `T_{t-1} >= m` but I was previously defecting (recovering from a defection phase): Switch back to cooperate (C) immediately.

**4. The Final Round (r)**
- If the cumulative performance in rounds 1 to (r-1) suggests a high probability of success (defined as `success` occurring in > 50% of previous rounds), cooperate (C).
- If performance has been consistently poor (defined as `success` occurring in ≤ 50% of previous rounds), defect (D) to maximize terminal individual payoff.

**5. Robustness Override**
If at any point the total number of cooperators observed (excluding myself) is consistently 0 for two consecutive rounds, immediately switch to defect (D) for the remainder of the game, regardless of the round number. This assumes a non-cooperative population where further efforts are futile.
'''

description_COLLECTIVE_27 = '''
Strategy: Tit-for-Tat with Threshold Sensitivity

The strategy relies on a trigger-based, conditional cooperation mechanism designed to enforce the threshold $m$ while punishing free-riders.

**Decision Rules**

1. **Initial Round ($t=1$):**
   Play Cooperate (C) with probability $p = m/n$, or if stochastic choice is disallowed, play C. This establishes a baseline effort toward meeting the collective threshold.

2. **Subsequent Rounds ($t > 1$):**
   Calculate the number of cooperators from the previous round, $C_{t-1}$.
   
   *   **Case 1: $C_{t-1} \ge m$.** The threshold was met. 
       Play C with probability $p = m/n$ (to sustain the collective effort) or C deterministically if $m/n$ is high. 
       However, if the strategy aims to identify free-riders, play C if the previous round's outcome was close to the threshold (i.e., $C_{t-1} \approx m$), as this indicates a fragile but successful coalition.
       
   *   **Case 2: $C_{t-1} < m$.** The threshold was not met.
       The collective action failed. Immediately switch to Defect (D) for the current round to avoid wasting resources on a non-functioning group.
   
   *   **Case 3: $C_{t-1} < m$ but $C_{t-2} \ge m$.**
       If the group was previously successful but failed in the immediately preceding round, attempt to restart cooperation (playing C) to see if the failure was an anomaly or a shift in collective behavior.

3. **Terminal Round ($t = r$):**
   If $C_{r-1} \ge m$, play C.
   If $C_{r-1} < m$, play D.

**Edge Cases & Calibration**

*   **Free-rider Detection:** If the observed number of cooperators consistently exceeds $m$ by a significant margin (e.g., $C_{t-1} > m+1$), increase the probability of playing D to conserve resources, assuming the threshold will be met regardless of your contribution.
*   **Failed Coordination:** If $C_{t-1} < m$ for three consecutive rounds, assume the population is non-cooperative and play D for the remainder of the game to minimize endowment loss.
*   **Near-Threshold Optimization:** If the observed cooperation count is exactly $m-1$, play C to force the transition to $m$ cooperators.

**Pseudocode Logic**

```
IF (round == 1):
    RETURN Cooperate
    
IF (last_round_cooperators >= m):
    IF (last_round_cooperators > m + 1): 
        // Likely safe to free-ride
        RETURN Defect
    ELSE:
        // Must maintain threshold
        RETURN Cooperate
        
IF (last_round_cooperators < m):
    // Check if recovery is possible
    IF (rounds_since_success < 3):
        RETURN Cooperate
    ELSE:
        // Group is dysfunctional
        RETURN Defect
```
'''

description_COLLECTIVE_28 = '''
The strategy employs a conditional "tit-for-tat-with-threshold" approach designed to foster cooperation while mitigating exploitation. It treats the threshold *m* as the focal point for coordination, using a target contribution count to determine actions.

**Phase 1: Initialization**
In Round 1, initiate by playing Cooperate (C). This signals a willingness to engage in a mutually beneficial outcome.

**Phase 2: Adaptive Response**
For all subsequent rounds *t* (where *t* > 1), adjust actions based on the outcome of round *t-1*. Define *C_prev* as the number of cooperators observed in the previous round.

1.  **If *C_prev* ≥ *m*:**
    The collective threshold was met in the previous round. Continue to cooperate (C). This maintains the equilibrium that rewards all players.

2.  **If *C_prev* < *m*:**
    The collective threshold was not met. Switch to Defect (D) for the current round. This protects resources against non-cooperation when the collective outcome failed.

**Phase 3: Recovery Mechanism**
If the strategy is in a state of Defect (D) due to a failure to meet the threshold, attempt to restart cooperation periodically. Every *k* rounds (where *k* is a small integer, e.g., 3), revert to Cooperate (C) regardless of the previous round's performance to test if other agents are willing to return to the cooperative equilibrium.

**Pseudocode Logic:**

```python
def get_action(round_number, prev_round_cooperators, m, k_interval):
    # Round 1: Default to cooperation to initiate
    if round_number == 1:
        return 'C'
    
    # Recovery mechanism: periodically attempt to restart cooperation
    if round_number % k_interval == 0:
        return 'C'
    
    # Adaptive response based on last round's success
    if prev_round_cooperators >= m:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Last Round:** In the final round *r*, maintain the logic derived from round *r-1*. If the threshold was met in *r-1*, contribute (C) to maximize the final round's reward. If the threshold was not met, defect (D) to preserve the endowment, as there is no future round to incentivize cooperation.
*   **Threshold Vulnerability:** If the observed *C_prev* is exactly *m-1*, interpret this as a near-miss where collective cooperation is feasible, and shorten the recovery interval to the next immediate round to attempt to cross the threshold again quickly.
'''

description_COLLECTIVE_29 = '''
Cooperate in round 1. For all subsequent rounds, base the action on the observed total cooperation from the previous round (S_{t-1}).

If t = 1:
    Play C.

If t > 1:
    Let m be the threshold for success.
    Let C_{obs} be the number of cooperators observed in round t-1.
    
    1. If C_{obs} ≥ m:
       You successfully met the threshold last round. Continue to play C to maintain the collective outcome, provided your payoff from cooperating (k - 1) is positive relative to defecting (k - 1 + 1 = k). Since the reward k > 1 makes cooperation payoff (k) equal to or better than defection payoff (k+1 if you defect while others cooperate), evaluate the stability of the group. If C_{obs} ≥ m + 1, play C. If C_{obs} == m, play D only if you calculate that the current group is defecting heavily; otherwise, play C to maintain the threshold. Specifically:
       If C_{obs} ≥ m: Play C.
       
    2. If C_{obs} < m:
       The collective failed. Revert to a "trigger-reset" mechanism. If the failure was marginal (C_{obs} = m - 1), play C to signal willingness to reach the threshold. If the failure was catastrophic (C_{obs} << m), play D to minimize personal loss until a round where C_{obs} trends upward again, or play C if the "tit-for-tat" logic requires re-establishing cooperation.
       Specifically: If C_{obs} < m, play C with probability P = C_{obs} / m, or simply play C to attempt to push the group back toward the threshold.

    3. Last Round Constraint:
       In the final round (t = r), if the collective has demonstrated sustained cooperation (average C_{obs} over previous rounds > m), play C. If the collective history is erratic or consistently below m, play D to maximize private gain, as there is no future incentive for the group to maintain the threshold.

Pseudocode Logic:

If t == 1:
    return C

If t > 1:
    If C_{obs} >= m:
        return C
    Else if C_{obs} == m - 1:
        return C
    Else if t == r:
        return D
    Else:
        return D
'''

description_COLLECTIVE_30 = '''
**Strategy: Threshold-Responsive Tit-for-Tat (TR-TFT)**

**1. Strategy Logic**
The strategy operates on a conditional commitment model. It seeks to enforce a cooperative equilibrium where exactly $m$ players contribute. Because defection yields a higher per-round payoff than cooperation ($1+k$ vs $k$), the strategy uses past rounds to signal willingness to cooperate while punishing collective failure.

**2. Decision Rules**
Let $C_t$ be the number of cooperators observed in round $t$. Let $c_{self, t}$ be the action taken in round $t$.

*   **Round 1:** Play **Cooperate (C)**. This signals a commitment to the collective goal.
*   **Subsequent Rounds ($t > 1$):**
    *   **Condition A (Threshold Met):** If $C_{t-1} \ge m$:
        *   If you played $C$ in $t-1$: Play **Cooperate (C)**.
        *   If you played $D$ in $t-1$: Play **Cooperate (C)**. (A forgiving restart).
    *   **Condition B (Threshold Missed):** If $C_{t-1} < m$:
        *   If $C_{t-1} = 0$: Play **Defect (D)** for the current round. (The collective failed completely; preserve resources).
        *   If $0 < C_{t-1} < m$: Play **Cooperate (C)** with probability $P_{rebound} = \frac{m - C_{t-1}}{n - C_{t-1}}$. Otherwise, play **Defect (D)**. (This attempts to "fill the gap" to reach the threshold without over-contributing).

**3. Edge Cases and Refinements**
*   **The "Last Round" Problem:** In round $r$, ignore the potential for future retaliation. However, continue applying the threshold logic. If $C_{r-1} < m$, revert to **Defect (D)**, as there is no future round to incentivize others to cooperate.
*   **Total Defection:** If the group consistently plays $D$ ($C_{t-1} = 0$) for two consecutive rounds, switch to a permanent **Defect (D)** strategy for the remainder of the game. The collective is uncooperative.
*   **Over-Cooperation:** If $C_{t-1} > m$ and you played $C$ in the previous round, switch to **Defect (D)** for the current round. This balances the group's contribution level, preventing unnecessary waste of resources by ensuring exactly $m$ cooperators are incentivized.
*   **Symmetry Breaking:** If the strategy suggests "Cooperate" and you are randomized to choose between C and D based on $P_{rebound}$, maintain that choice consistently until the next round evaluation.
'''

description_COLLECTIVE_31 = '''
Define a threshold $T = m$ as the target number of cooperators required for the collective reward $k$. Let $C_t$ be the total number of cooperators in round $t$.

**Initialization (Round 1):**
Cooperate ($c_1 = C$). This establishes a cooperative baseline to signal potential for collective success.

**General Decision Rules (Rounds 2 to $r-1$):**
Maintain a cooperative stance contingent on observed collective performance.
1. If $C_{t-1} \ge m$, continue to cooperate ($c_t = C$).
2. If $C_{t-1} < m$:
    a. If you cooperated in $t-1$ and the target $m$ was missed, you are currently carrying the burden of an underperforming group. If $m$ was missed by a margin of 1 (i.e., $C_{t-1} = m-1$), switch to Defect ($c_t = D$) to punish the defectors and conserve endowment.
    b. If you defected in $t-1$ and $m$ was missed, continue to Defect ($c_t = D$).
    c. If you cooperated in $t-1$ and $C_{t-1} < m-1$, switch to Defect ($c_t = D$) to minimize losses.

**Refinement for Adaptation:**
If you switched to Defect because $C_{t-1} < m$, check the subsequent round $C_t$:
- If $C_t \ge m$, revert to Cooperate ($c_{t+1} = C$) to restore the collective benefit.
- If $C_t < m$, remain at Defect ($c_{t+1} = D$) for the duration of the game.

**Final Round (Round $r$):**
1. If $C_{r-1} \ge m$, cooperate ($c_r = C$).
2. If $C_{r-1} < m$, defect ($c_r = D$).

**Edge Case Logic:**
- If $n$ is very large relative to $m$ (e.g., $m/n \le 0.25$), prioritize cooperation aggressively even if previous rounds failed, unless $C_{t-1} = 0$, in which case permanent defection is triggered.
- If you observe that your own defection (in a case where $C_{t-1} = m-1$) causes the next round's $C_t$ to drop below $m-1$, revert to cooperation in the following round to prevent a total collapse of the collective effort.
'''

description_COLLECTIVE_32 = '''
The strategy employs a conditional "trigger-cooperation" logic designed to reach the threshold $m$ efficiently while minimizing exploitation by defectors.

### Decision Rules

In any round $t$, let $C_{t-1}$ be the number of cooperators observed in the previous round.

1.  **Phase 1: Probing and Establishing (Round 1)**
    *   Play **C**. This establishes a baseline for cooperation and tests the propensity of opponents to contribute.

2.  **Phase 2: Adaptive Maintenance (Rounds 2 through $r-1$)**
    *   **If $C_{t-1} \geq m$:** Continue to play **C**. The threshold is being met, and the collective benefit is secured.
    *   **If $C_{t-1} < m$:** Transition to **D**.
        *   *Exception:* If you previously played **D** and the observed cooperation in the last round was $C_{t-1} = m-1$, switch back to **C**. This attempts to "nudge" the collective to the threshold without sustaining losses against a non-cooperative group.

3.  **Phase 3: Terminal Handling (Round $r$)**
    *   If $C_{r-1} \geq m$, play **C**.
    *   If $C_{r-1} < m$, play **D**. There is no future round to punish or reward, so the dominant strategy is to maximize the immediate private payoff.

### Pseudocode Representation

```python
def decide_action(round_number, prev_cooperators, my_last_action):
    # Round 1: Always start with C
    if round_number == 1:
        return 'C'
        
    # Round r: Only cooperate if the threshold was met previously
    if round_number == r:
        if prev_cooperators >= m:
            return 'C'
        else:
            return 'D'
            
    # Intermediate Rounds
    if prev_cooperators >= m:
        return 'C'
    
    # Handling threshold failure
    # If the group was one short of the threshold, try to reach it once more
    if prev_cooperators == m - 1 and my_last_action == 'D':
        return 'C'
        
    # Otherwise, default to defection to avoid exploitation
    return 'D'
```

### Edge Cases and Robustness

*   **Non-responsiveness:** If the group persistently fails to reach $m$, the strategy defaults to defection ($D$) to ensure a private payoff of $1$ rather than $0$.
*   **Threshold volatility:** The "nudge" condition ($C_{t-1} = m-1$) allows the strategy to recover from temporary dips in cooperation caused by other agents shifting strategies, without locking into permanent defection.
*   **Final Round Incentive:** By switching to $D$ in the final round if the threshold was not met, the strategy avoids the "sucker's payoff" when cooperation is demonstrably insufficient.
'''

description_PROSOCIAL_5 = '''
The strategy employs a "Conditional Threshold Tit-for-Tat" approach, designed to incentivize group cooperation while minimizing exploitation in the final rounds.

### Strategy Rules

**1. Round 1 Initialization:**
Always play **C**. The initial contribution signals a commitment to the collective goal and attempts to establish a cooperative equilibrium.

**2. Rounds 2 through r-1:**
Calculate the number of cooperators observed in the previous round ($C_{t-1}$).
*   **Case A: If $C_{t-1} \ge m$:** Play **C**. The threshold was met, indicating sufficient group cooperation; continue cooperating to maintain the positive outcome.
*   **Case B: If $C_{t-1} < m$:** Play **C** with probability $p$, where $p$ is proportional to the gap between the threshold $m$ and the observed number of cooperators. Specifically, $p = \frac{C_{t-1}}{m}$. If the previous outcome was 0 cooperators, play **D** to avoid repeated exploitation without return.

**3. Final Round ($r$):**
This is a termination-sensitive adjustment.
*   If the aggregate cooperative history shows a consistent failure to reach the threshold $m$ (e.g., $C_{t-1} < m$ in more than 50% of the previous rounds), play **D**.
*   If the group has successfully reached the threshold $m$ in at least 50% of previous rounds, play **C**. This assumes that the cooperative norm is sufficiently established that the final round does not require defecting to protect against last-minute betrayal.

### Logic Flow

```pseudocode
// Strategy Execution for round t

if t == 1:
    return C

if t < r:
    // Observe C_obs: number of cooperators in round t-1
    if C_obs >= m:
        return C
    else if C_obs > 0:
        // Attempt to signal willingness to cooperate back to threshold
        probability_to_cooperate = C_obs / m
        return (random() < probability_to_cooperate) ? C : D
    else:
        // Collective failure; protect endowment
        return D

if t == r:
    // Evaluate long-term cooperation track record
    if (Sum(C_obs_history) / (r-1)) >= (m / n):
        return C
    else:
        return D
```

### Prosocial Justification
The strategy prioritizes group success by keeping the threshold $m$ as the primary target. It avoids "sucker" behavior by defecting when the group fails completely (0 cooperators), while maintaining "forgiving" behavior (using a probability function) when the group is close to success but missing the target. It minimizes the incentive for last-round defection by using an empirical track record check, ensuring that cooperation is only extended in the final round if the group has demonstrated mutual trust throughout the game.
'''

description_PROSOCIAL_6 = '''
Maintain a "Conditional Threshold Reciprocator" policy designed to foster stable cooperation when possible, while defecting against exploitation.

### Decision Rules
Let $C_t$ be the total number of players who cooperated in round $t$. Let $c_{i,t}$ be your action in round $t$ (1 for C, 0 for D).

**Round 1:** Play **C** (Cooperate).

**Rounds 2 through $r$:**
If you played $C$ in round $t-1$:
- If $C_{t-1} \ge m$, play **C**. (The threshold was met; continue cooperation).
- If $C_{t-1} < m$, play **D** with probability $p = 1 - (C_{t-1}/m)$, or play **C** if your random draw is below $C_{t-1}/m$. (Forgive partial failure based on the proportion of success).

If you played $D$ in round $t-1$:
- If $C_{t-1} \ge m$, play **C**. (The group is succeeding despite your previous defection; return to cooperation).
- If $C_{t-1} < m$, play **D**. (The group is failing; remain in a protective, non-cooperative state).

### Edge Cases
- **Last Round ($t = r$):** If the history of the game indicates $C_t \ge m$ has been achieved consistently (in at least 75% of previous rounds), play **C**. Otherwise, play **D** to avoid exploitation in the terminal phase where future consequences cannot be enforced.
- **Threshold Uncertainty ($m=n$):** If the threshold $m$ is equal to the total number of players $n$, the policy switches to "Tit-for-Tat-with-Forgiveness." Play **C** if $C_{t-1} = n$. If $C_{t-1} < n$, play **D** for one round, then revert to **C** in the next round, regardless of the group's performance.

### Pseudocode Logic
```python
def decide(t, r, m, c_history_prev):
    if t == 1:
        return C
    
    # Last round termination logic
    if t == r:
        success_rate = count(c_history_prev >= m) / (t - 1)
        return C if success_rate >= 0.75 else D

    # Adaptive reciprocity logic
    prev_cooperators = c_history_prev[-1]
    my_prev_action = my_actions[-1]

    if my_prev_action == C:
        if prev_cooperators >= m:
            return C
        else:
            # Probabilistic re-entry to cooperation
            return C if random() < (prev_cooperators / m) else D
            
    else: # my_prev_action == D
        if prev_cooperators >= m:
            return C
        else:
            return D
```
'''

description_PROSOCIAL_7 = '''
**Initial Phase (Rounds 1–2):**
Cooperate (C) in the first two rounds to establish a baseline of contribution and signal prosocial intent.

**Main Strategy Logic (Rounds 3 to r-1):**
Employ a conditional cooperation rule based on the observed number of cooperators from the previous round (denoted as $N_{prev}$).

1.  **If $N_{prev} \ge m$:**
    *   If you played C in the previous round: Play C.
    *   If you played D in the previous round: Switch to C (re-enter the cooperative equilibrium).

2.  **If $N_{prev} < m$:**
    *   **If you played C in the previous round:** Switch to D. (This avoids being exploited when the collective effort is failing, effectively punishing the non-cooperation or signaling the lack of critical mass).
    *   **If you played D in the previous round:** Keep playing D, *unless* the number of cooperators was $m-1$ (the "near-miss" scenario). If $N_{prev} = m-1$, play C to attempt to reach the threshold $m$ in the current round.

**Terminal Phase (Final Round $r$):**
Ignore the penalty avoidance logic of previous rounds and play C if the average cooperation rate across all previous rounds was $\ge \frac{m}{n}$. If the average cooperation rate was below this threshold, play D to secure the baseline endowment, as the risk of losing the reward $k$ is high and signaling future cooperation is irrelevant.

**Pseudocode representation:**

```python
def decide_action(round, N_prev, history, c_last):
    if round <= 2:
        return 'C'

    if round == r:
        avg_cooperation = sum(history_N) / (r - 1)
        if avg_cooperation >= (m / n):
            return 'C'
        else:
            return 'D'

    # Standard conditional cooperation
    if N_prev >= m:
        return 'C'
    elif N_prev == m - 1:
        return 'C'
    else:
        # If we didn't meet the threshold and weren't close, 
        # play D to minimize losses.
        return 'D'
```
'''

description_PROSOCIAL_8 = '''
Play Cooperative (C) in the first round.

In subsequent rounds $t > 1$, cooperate if and only if the historical cooperation rate of the population has been sufficient to sustain the project, using the following rules:

1. Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
2. Let $m$ be the minimum cooperators required.
3. If $C_{t-1} \geq m$, cooperate (C).
4. If $C_{t-1} < m$, cooperate (C) if the "cooperation debt" (cumulative deficiency) is low, otherwise defect (D) to minimize personal loss. Specifically, track $S = \sum_{j=1}^{t-1} (m - C_j)$. If $S < n$ (the total population size), cooperate. If $S \geq n$, defect.

In the final round $r$, always defect (D) if the goal of the collective project has already been met or if the history suggests that the collective outcome will not be achieved regardless of your contribution. If the collective goal is still potentially reachable and the group has shown consistent cooperation (previous $C_t \geq m$ for at least 75% of rounds), continue to cooperate (C) to maximize the probability of the group reward.

If any opponent is observed to defect in a round where $C_t = m$, interpret this as a signal of exploitation and switch to always defecting (D) for the remainder of the game.
'''

description_PROSOCIAL_9 = '''
Play cooperatively to achieve the threshold $m$, while conditioning future behavior on the recent aggregate contribution history to encourage reciprocity and punish defection.

### Initialization
In Round 1, play C. This establishes a baseline of cooperation and provides the initial signal for others to follow.

### Decision Rules for Rounds $t > 1$
For each round $t$, calculate the number of cooperators $C_{t-1}$ from the previous round. Define a strategy state $S_t \in \{Cooperative, Retaliatory, Testing\}$.

1.  **If $S_{t-1} = Cooperative$:**
    *   If $C_{t-1} \geq m$, continue to play **C**.
    *   If $C_{t-1} < m$, switch to **Retaliatory** for the next round.

2.  **If $S_{t-1} = Retaliatory$:**
    *   If $C_{t-1} \geq m$, return to **Cooperative** and play **C**.
    *   If $C_{t-1} < m$, play **D** (to avoid exploitation while the group fails to reach the threshold).

3.  **If $S_{t-1} = Testing$:**
    *   If $C_{t-1} \geq m$, switch to **Cooperative** and play **C**.
    *   If $C_{t-1} < m$, remain in **Testing** and play **D**.

### Edge Cases
*   **Final Round ($t = r$):** If the group has maintained a $C_{t-1} \geq m$ state for at least 50% of the game duration, play **C**. Otherwise, play **D** to protect against anticipated endgame defection by others.
*   **Threshold Vulnerability:** If $C_{t-1} = m - 1$, play **C** regardless of state, as this is the "tipping point" where one individual contribution guarantees the group reward $k$.

### Pseudocode
```python
state = 'Cooperative'
for t in 1 to r:
    if t == 1:
        action = 'C'
    elif t == r:
        if (cooperation_history_rate > 0.5):
            action = 'C'
        else:
            action = 'D'
    else:
        # Check tipping point
        if C_{t-1} == m - 1:
            action = 'C'
        else:
            if state == 'Cooperative':
                if C_{t-1} >= m:
                    action = 'C'
                else:
                    state = 'Retaliatory'
                    action = 'D'
            elif state == 'Retaliatory':
                if C_{t-1} >= m:
                    state = 'Cooperative'
                    action = 'C'
                else:
                    action = 'D'
            elif state == 'Testing':
                if C_{t-1} >= m:
                    state = 'Cooperative'
                    action = 'C'
                else:
                    action = 'D'
```
'''

description_PROSOCIAL_10 = '''
The strategy operates on a conditional cooperative logic, aiming to reach the threshold $m$ while punishing unilateral defection and maintaining a "tit-for-tat" reputation.

### State Variables
- $C_t$: Number of cooperators observed in round $t$.
- $c_i$: Your action in round $t$ ($1$ for Cooperate, $0$ for Defect).
- $target$: The threshold $m$.

### Decision Rules
1.  **Round 1:** Play $C$ (Cooperate). This signals cooperative intent and maximizes the potential for collective success from the outset.
2.  **Round $t > 1$:**
    - If the number of cooperators in the previous round ($C_{t-1}$) was $\geq m$, play $C$. This reinforces the successful equilibrium and supports the collective benefit.
    - If $C_{t-1} < m$, identify if you were necessary for reaching the threshold. If your contribution would have pushed the total to $m$ or above in the previous round (i.e., $C_{t-1} = m-1$ and you played $C$), you must play $C$ again to attempt to stabilize the group.
    - If the group failed to reach the threshold ($C_{t-1} < m$) and your previous contribution did not make the difference (i.e., $C_{t-1} < m-1$ or you played $D$), play $D$ for one round. This serves as a probabilistic check to see if the group can coordinate without your subsidy or if others are free-riding.
3.  **Last Round ($t = r$):**
    - If the average cooperation rate over rounds $1$ to $r-1$ was $\geq \frac{m}{n}$, play $C$.
    - If the average cooperation rate was $< \frac{m}{n}$, play $D$. This prevents exploitation in the final round when future reciprocation is impossible.

### Edge Case Handling
- **If $C_{t-1} = m$ exactly:** This is a fragile state. Maintain $C$ to signal stability.
- **If $C_{t-1} > m$:** Maintain $C$. The reward $k$ outweighs the cost of contribution, and collective over-cooperation ensures the threshold is met even if some players defect in the subsequent round.
- **Randomization:** To avoid becoming predictable, if you are in the "play $D$" state based on rule 2, play $C$ with a probability $p = \frac{m}{n}$ to allow for stochastic recovery of the cooperative equilibrium.
'''

description_PROSOCIAL_11 = '''
**Initial Round:**
Cooperate (C) to signal commitment to the threshold, provided $m \leq n$.

**Subsequent Rounds (t > 1):**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $M_t$ be the "target" number of cooperators for the current round, calculated as $M_t = m$.

1. **Reciprocity Logic:**
   - If $C_{t-1} \geq m$, cooperate (C).
   - If $C_{t-1} < m$, defect (D).

2. **Recovery Protocol (The "Forgiveness" Trigger):**
   - If the previous round resulted in $C_{t-1} < m$, and your strategy was to defect, perform a "probing cooperation" in the next round with probability $p = 0.1$. If the probe is successful (i.e., others also cooperate, resulting in total cooperation $\geq m$), immediately return to unconditional cooperation for the remainder of the game. If the probe fails ($C_t < m$), revert to D until the next probe.

3. **Terminal Rounds:**
   - For the final round ($t = r$), ignore the reciprocity logic and cooperate (C) regardless of previous history to maximize collective welfare, unless $C_{r-1}$ was 0, in which case play D to avoid a guaranteed individual loss.

**Pseudocode:**

```python
def choose_action(round_t, total_rounds, prev_cooperators, m, n):
    if round_t == 1:
        return C

    if round_t == total_rounds:
        return C if prev_cooperators > 0 else D

    if prev_cooperators >= m:
        return C
    
    # Recovery Protocol
    if random.random() < 0.1:
        return C
    
    return D
```
'''

description_PROSOCIAL_12 = '''
### Strategy: Threshold-Conditional Tit-for-Tat (TCTT)

The strategy operates on a basis of conditional cooperation, aiming to maintain a cooperative equilibrium that satisfies the threshold $m$. It functions by assessing the minimum level of cooperation required from the collective to trigger the reward $k$ and reciprocating the perceived cooperative intent of the group.

**Phase 1: Initialization**
In Round 1, always play **Cooperate (C)**. This signals a willingness to engage in the prosocial equilibrium regardless of opponent behavior.

**Phase 2: Monitoring and Reciprocity**
In rounds $t > 1$, calculate the cooperation level from the previous round, $C_{t-1}$. 
- Let $c_{self}$ be your action in the previous round.
- Let $O_{t-1}$ be the number of cooperators among opponents in the previous round.
- The total cooperators in the previous round was $TotalC_{t-1} = O_{t-1} + c_{self}$.

Decision Logic:
1.  **If $TotalC_{t-1} \ge m$:** The group succeeded. Continue to play **Cooperate (C)**. This reinforces the successful state and signals continued commitment.
2.  **If $TotalC_{t-1} < m$:** The group failed. Your action for round $t$ depends on whether the contribution threshold was narrowly missed or widely ignored:
    - If $TotalC_{t-1} = m - 1$ (the "close miss" condition), play **Cooperate (C)** to minimize the gap and demonstrate initiative.
    - If $TotalC_{t-1} < m - 1$, play **Defect (D)**. This is a punitive measure against a non-cooperative collective. Defection in this state prevents individual exploitation until the group demonstrates a return to a cooperative threshold.

**Phase 3: Recovery**
If the previous round was a Defection round ($TotalC_{t-1} < m - 1$) and you played **Defect (D)**, wait for one round where $O_{t-1} \ge m-1$ (meaning the opponents have returned to a near-threshold state). Upon observing $O_{t-1} \ge m-1$, return to playing **Cooperate (C)** in the subsequent round to restart the prosocial cycle.

**Phase 4: Final Round Edge Case**
In the final round $r$, if the strategy is currently in a state of cooperation (i.e., you played C in $r-1$ or are in a recovery phase), play **Cooperate (C)**. If you are currently in a state of sustained defection due to consistent group failure throughout the game, continue to play **Defect (D)**.

**Pseudocode:**

```python
def decide_action(round_number, prev_opponents_C, prev_self_C):
    if round_number == 1:
        return 'C'
    
    total_C = prev_opponents_C + (1 if prev_self_C == 'C' else 0)
    
    if total_C >= m:
        return 'C'
    elif total_C == m - 1:
        return 'C'
    else: # Significant failure
        if round_number == r:
            return 'D'
        return 'D' 
```
'''

description_PROSOCIAL_13 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Gradual Forgiveness**

Maintain a cooperative stance as long as the collective outcome remains viable. Monitor the total cooperation count in previous rounds to gauge the group's willingness to achieve the threshold $m$.

**Decision Rules:**

1.  **Initialization (Round 1):**
    Play **Cooperate (C)**. Assume the group is capable of achieving the threshold $m$.

2.  **Tracking State:**
    Maintain a variable $S$ representing the group's reputation.
    *   $S_0 = 1$ (Baseline cooperation).
    *   If the threshold $m$ was met in the previous round, $S_t = \min(1, S_{t-1} + 0.2)$.
    *   If the threshold $m$ was *not* met in the previous round, $S_t = S_{t-1} - 0.4$.
    *   The value of $S_t$ is always clamped between $[0, 1]$.

3.  **Action Selection (Rounds $t > 1$):**
    *   Calculate a cooperation probability $P = S_{t-1}$.
    *   With probability $P$, play **Cooperate (C)**.
    *   With probability $1-P$, play **Defect (D)**.

4.  **Threshold Enforcement:**
    If the current round is $t = r$ (the final round), ignore the probability $P$ and calculate the number of cooperators needed to reach the threshold based on observed history. If the group has consistently shown high cooperation ($S_t > 0.6$), play **Cooperate (C)** regardless of previous probabilistic outcomes. If the group has shown defection ($S_t \leq 0.6$), play **Defect (D)** to avoid personal loss.

**Handling Edge Cases:**

*   **Low Threshold Participation:** If the group fails to meet the threshold $m$ for three consecutive rounds, set $S = 0$ immediately, switching to **Defect (D)** for all remaining rounds to minimize endowment loss.
*   **Near-Threshold Defection:** If the previous round resulted in $m-1$ cooperators, reduce $S$ by only $0.1$ instead of $0.4$, treating this as a "near-miss" rather than a total system failure.
*   **Reward/Endowment Check:** If $k < 1$, the payoff structure incentivizes defection even in the aggregate success case. In this specific scenario ($k < 1$), switch to **Defect (D)** for all rounds, as the community project is net-negative for the individual compared to keeping the endowment.
'''

description_PROSOCIAL_14 = '''
**Strategy: Conditional Reciprocal Thresholding**

The strategy operates on a principle of conditional cooperation, aiming to incentivize the collective good (reaching threshold $m$) while minimizing exploitation by non-cooperative agents.

**1. Decision Rules**

The decision to cooperate ($C$) or defect ($D$) at round $t$ is determined by a state variable $S$ representing the player's cooperative standing, where $S$ tracks the history of the group’s cooperation levels.

*   **Initial State:** Set $S = 0$ (Neutral).
*   **Round 1:** Play $C$. Cooperation is initiated to signal intent to reach the threshold $m$.
*   **Subsequent Rounds ($t > 1$):**
    *   Let $N_{c, t-1}$ be the number of players who cooperated in the previous round.
    *   If $N_{c, t-1} \ge m$: The collective threshold was met. Play $C$. Maintain cooperation as long as the group maintains the threshold.
    *   If $N_{c, t-1} < m$: The collective threshold was missed.
        *   If the strategy cooperated in $t-1$: Decrease $S$ by 1. Play $D$. This is a "punishment" phase to signal that cooperation will not be offered for free when the collective goal is ignored.
        *   If the strategy defected in $t-1$: Maintain $D$.
    *   **Recovery Rule (Test of Cooperation):** If $S < 0$ and the group shows renewed signs of cooperation (specifically, if $N_{c, t-1} \ge m-1$ for two consecutive rounds), reset $S = 0$ and play $C$ in the current round to restart cooperative efforts.

**2. Pseudocode**

```python
# Variables:
# m: minimum cooperators
# r: total rounds
# N_c: number of cooperators in previous round
# S: cooperative state (0 = neutral/cooperative, <0 = punishing/defecting)

if round == 1:
    return C

if N_c >= m:
    S = 0
    return C
else:
    # Collective failure detected
    if previous_action == C:
        S = S - 1
        
    # Check for recovery condition
    # If the group is attempting to cooperate (getting close to m), resume
    if S < 0 and history_recent_N_c >= (m - 1):
        S = 0
        return C
    
    return D
```

**3. Handling Edge Cases**

*   **Last Round:** The strategy treats the last round identically to all other rounds. While game theory suggests defecting in the final round of a finite game, this strategy prioritizes robust, consistent cooperation. If the group has maintained the threshold leading up to the final round, it cooperates to ensure the final payoff. If the group has been uncooperative, it defects to avoid exploitation.
*   **Near-Threshold Performance:** If the group consistently hits $m-1$ (just missing the threshold), the strategy interprets this as a coordination failure rather than malice. The "Recovery Rule" ensures that cooperation is not permanently suspended if the group is attempting to coordinate, preventing a downward spiral into perpetual defection.
*   **Threshold Vulnerability:** If $k$ is significantly larger than 1, the strategy prioritizes the group outcome over individual marginal gains from defection, as securing $k$ is the primary objective for the group's long-term utility.
'''

description_PROSOCIAL_15 = '''
Cooperate in the first round. In all subsequent rounds, base the decision on the observed number of cooperators from the previous round, denoted as $C_{t-1}$.

Maintain a variable `status`, initialized to "Cooperative." If the strategy enters the "Defect" state, it may transition back to "Cooperative" based on opponent behavior.

**Decision Rules:**

1.  **Initial Round (t=1):**
    Always choose Cooperate ($C$).

2.  **Subsequent Rounds (t > 1):**
    *   **If `status` is "Cooperative":**
        *   If the number of cooperators in the previous round was at least $m$, maintain $C$.
        *   If the number of cooperators in the previous round was less than $m$, switch `status` to "Defect" and choose Defect ($D$).
    *   **If `status` is "Defect":**
        *   Observe the number of cooperators in the previous round. If the number of cooperators was equal to or greater than $m$, switch `status` to "Cooperative" and choose Cooperate ($C$).
        *   Otherwise, choose Defect ($D$).

3.  **Last Round (t=r):**
    *   If `status` is "Cooperative," choose Cooperate ($C$).
    *   If `status` is "Defect," choose Defect ($D$).

**Edge Case Handling:**
*   If $t < r$ and the game is nearing its end, follow the rules above strictly. There is no special "end-game" defection; the strategy remains conditional on the threshold $m$ to encourage recovery of the cooperative equilibrium.
*   If $n$ is very large relative to $m$, the strategy remains indifferent to the exact count of cooperators exceeding $m$, as long as the threshold is met.
'''

description_PROSOCIAL_16 = '''
**Decision Rules:**

Maintain a variable `status` initialized to `Cooperative`. 

In each round `t` (from 1 to `r`):

1.  **Round 1:** Play `C` (Cooperate).

2.  **Subsequent Rounds (t > 1):**
    *   Calculate `cooperation_rate` = (Total cooperators in round `t-1`) / `n`.
    *   If the system `status` is `Cooperative`:
        *   If `cooperation_rate` is less than `m/n`, switch `status` to `Defect` and play `D`.
        *   Otherwise, play `C`.
    *   If the system `status` is `Defect`:
        *   If `cooperation_rate` >= `(m+1)/n` (a "recovery" threshold), switch `status` back to `Cooperative` and play `C`.
        *   Otherwise, continue playing `D`.

**Edge Cases and Specific Adjustments:**

*   **Final Round (t = r):** If `status` is `Cooperative`, play `C`. If `status` is `Defect`, check if the last round's `cooperation_rate` was ≥ `m/n`. If it was, play `C` to attempt a final payoff maximization; otherwise, play `D`.
*   **Threshold Vulnerability:** If the number of cooperators in round `t-1` was exactly `m-1`, interpret this as an "accident" or failed coordination attempt rather than intentional malice. In this specific case, maintain `Cooperative` `status` and play `C` in the current round, overriding the defect trigger.
*   **Randomization:** If `m/n` is not an integer ratio, calculate the threshold based on the exact integer requirement `m` rather than a percentage. If, in any round, you observe the total cooperators equal to `m-1` or `m`, maintain `Cooperative` `status` regardless of your own previous action, prioritizing the continuation of collective rewards.
'''

description_PROSOCIAL_17 = '''
### Strategy: Conditional Reciprocal Thresholding

**Phase 1: Initial Rounds (1 to r-2)**

*   **Round 1:** Play **C**. This establishes a baseline for cooperation and tests the propensity of the group to support the threshold.
*   **Subsequent Rounds (2 to r-2):** Calculate the previous round’s cooperative success. Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   **Cooperate (C)** if $C_{t-1} \ge m$.
    *   **Defect (D)** if $C_{t-1} < m$.
    *   *Correction Rule:* If the previous round resulted in fewer than $m$ cooperators, play **D** for exactly one round to signal that cooperation is conditional, then resume cooperation in the following round to restart the threshold effort.

**Phase 2: Late-Game Transition (Round r-1)**

*   Calculate the cumulative history of cooperation.
*   If the average number of cooperators across all previous rounds $\bar{C} \ge m$: Play **C**.
*   If the average number of cooperators across all previous rounds $\bar{C} < m$: Play **D**. This minimizes exploitation in the final stages where the likelihood of sustaining a successful collective effort has historically failed.

**Phase 3: Final Round (Round r)**

*   If the group succeeded in reaching the threshold $m$ in at least 50% of the previous rounds, play **C**.
*   Otherwise, play **D**. This reflects a "pay-it-forward" prosocial stance if there is evidence of a functioning cooperative culture, while avoiding altruistic exploitation if the group has failed to coordinate effectively.

**Logic Summary (Pseudocode)**

```python
# Variables:
# m = min cooperators
# r = total rounds
# prev_C = cooperators in last round
# history_C = list of past cooperators count

if current_round == 1:
    return C

if current_round < r - 1:
    if prev_C >= m:
        return C
    else:
        # Check if the previous round was a D-response to a failure
        # If we just defected because of a failure, return to C
        return D if prev_C_was_not_a_recovery_attempt else C

if current_round == r - 1:
    return C if mean(history_C) >= m else D

if current_round == r:
    return C if count(history_C >= m) / (r - 1) >= 0.5 else D
```
'''

description_PROSOCIAL_18 = '''
**Strategy: Threshold-Adaptive Reciprocity (TAR)**

This strategy operates on the principle of conditional cooperation, targeting the minimum threshold $m$ while punishing free-riders. It calculates the necessary contribution to reach $m$ and adjusts its stance based on the group's historical cooperation.

**Decision Rules:**

1.  **Initialize:** In Round 1, Cooperate (C). This establishes a willingness to contribute toward the threshold $m$.

2.  **Calculate Effective Cooperation:** Let $C_{t-1}$ be the number of players who cooperated in the previous round.
    *   If you played C in $t-1$, then the number of *others* who cooperated is $O_{t-1} = C_{t-1} - 1$.
    *   If you played D in $t-1$, then the number of *others* who cooperated is $O_{t-1} = C_{t-1}$.

3.  **Adaptive Threshold Targeting (Rounds 2 to $r-1$):**
    *   **Cooperate (C) if:** $O_{t-1} \ge m - 1$. If the group is already meeting or one shy of meeting the threshold, provide the critical contribution to secure the reward.
    *   **Defect (D) if:** $O_{t-1} < m - 1$. If the group is consistently failing to meet the threshold by a wide margin, switch to D to minimize personal loss while signaling that the current level of cooperation is insufficient to justify the cost.
    *   **Exception (Reset):** If you defected in $t-1$ but observed $O_{t-1} \ge m - 1$, revert to C in round $t$ to test if the group sustains the threshold.

4.  **Final Round (Round $r$):**
    *   Cooperate (C) if $O_{r-1} \ge m - 1$.
    *   Defect (D) if $O_{r-1} < m - 1$.

**Edge Case Logic:**

*   **Under-participation:** If in any round $t$, the group output is significantly below $m$ (e.g., $O_{t-1} < m - 2$), reduce cooperation probability. If the group consistently fails, switch to permanent defection for the remainder of the game to prevent exploitation.
*   **Threshold volatility:** If the number of cooperators fluctuates around $m$, prioritize C when the previous round successfully met or exceeded the threshold to build social capital.
*   **Greed check:** If in a round where you played D, the group still met the threshold ($O_{t-1} \ge m$), play D in the subsequent round to discourage non-contributing free-riding. If the group *fails* to meet the threshold when you play D, return to C immediately in the next round to restore the equilibrium.
'''

description_PROSOCIAL_19 = '''
**Strategy: Adaptive Threshold Tit-for-Tat (ATTT)**

**1. Definitions**
*   Let $N_t$ be the total number of cooperators observed in round $t$.
*   Let $C_t = 1$ if I played Cooperate in round $t$, and $C_t = 0$ if I played Defect.
*   Let $O_t$ be the number of cooperators among my opponents in round $t$. Thus, $N_t = O_t + C_t$.
*   Define "Cooperation Requirement" as $m$.

**2. Decision Rules**

*   **Round 1:** Play Cooperate.
*   **Subsequent Rounds ($t > 1$):**
    *   **Condition A (Threshold Met):** If $N_{t-1} \ge m$, play Cooperate. (This maintains the prosocial equilibrium.)
    *   **Condition B (Threshold Not Met, But Sufficient Support):** If $N_{t-1} < m$, and $N_{t-1} \ge (m - 1)$, play Cooperate. (This assumes that one additional contribution—mine—would have triggered the reward, signaling that the collective is close to the threshold.)
    *   **Condition C (Defection):** If $N_{t-1} < (m - 1)$, play Defect. (This protects against exploitation when the collective is far from the threshold, conserving resources.)

**3. Edge Cases**

*   **Final Round ($t = r$):** If the history of the game shows that cooperation has been sustainable (the threshold $m$ was met in at least 50% of the previous rounds), play Cooperate. Otherwise, play Defect. This acknowledges the finite horizon while maintaining prosociality only if the group has proven reliable.
*   **Observed Coordination Failure:** If the group fails to meet the threshold for three consecutive rounds despite Condition B being active, switch to Defect for all remaining rounds to minimize loss.

**4. Implementation Pseudocode**

```python
def decide_action(round, history, n, m, k):
    if round == 1:
        return 'C'
    
    # Check if cooperation has been sustainable
    successful_rounds = count(round_history where N_t >= m)
    if round == r:
        if successful_rounds / (round - 1) >= 0.5:
            return 'C'
        else:
            return 'D'

    # Check for consecutive failures
    if round > 3:
        if all(N_t < m for t in [round-3, round-2, round-1]):
            return 'D'

    # Adaptive Threshold Logic
    last_round_cooperators = history.last_N
    
    if last_round_cooperators >= m:
        return 'C'
    elif last_round_cooperators == (m - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_PROSOCIAL_20 = '''
Cooperate in the first round. In subsequent rounds, cooperate if and only if your cooperation is necessary to reach the threshold $m$ or if your cooperation is part of a stable, reciprocal agreement established by the history of play.

Define a strategy based on the observation of the total number of cooperators in the previous round, denoted $C_{t-1}$. 

For any round $t$:

1.  **Initialization:** If $t = 1$, play $C$.

2.  **Reciprocity Monitoring:** Define the threshold for cooperation as $m$. Let $C_{t-1}$ be the number of cooperators observed in the previous round.
    *   If $C_{t-1} \ge m$: The collective target was met. Play $C$ to sustain the prosocial outcome.
    *   If $C_{t-1} < m$: The collective target was not met. Defect (play $D$) for round $t$ to preserve resources against non-contributors, unless the game is in the final round.

3.  **Threshold Enforcement (The "Critical Need" Clause):**
    If the game state is such that your cooperation would move the total count from $m-1$ to $m$ cooperators, prioritize contribution. However, because you only observe the aggregate count from the *previous* round and cannot know the current round's actions in real-time, interpret the signal from $C_{t-1}$ as a proxy for the group's intent. 

4.  **Terminal Phase (Final Rounds):** In the final round $r$, if the cumulative history suggests the group is generally cooperative (defined as $\frac{1}{r-1} \sum_{t=1}^{r-1} C_t \ge m$), play $C$ regardless of the previous round's outcome to maximize the probability of reaching the final collective benefit.

5.  **Recovery Logic:** If you have defected due to a failure to meet the threshold in the previous round, restart cooperation (play $C$) every $k$ rounds (where $k$ is small, e.g., 3) to test if the group has returned to a cooperative stance. If the group meets the threshold $m$ during these "test" rounds, resume unconditional cooperation.
'''

description_PROSOCIAL_21 = '''
Maintain a cooperation state variable $S \in \{Active, Defection\_Triggered\}$ initialized to $Active$. 

### Decision Rules
In any round $t$:

1. **Initialization (Round 1):** Play $C$. 

2. **Conditional Continuation:** If $S == Active$:
   - Let $C_{t-1}$ be the number of cooperators in the previous round.
   - Calculate the "Minimum Necessary Cooperation" ($MNC$) needed to achieve the reward $k$ for the collective.
   - If $C_{t-1} \geq m$: Play $C$.
   - If $C_{t-1} < m$: Play $D$ with probability $P(D) = \frac{m - C_{t-1}}{n}$. In all other cases, play $C$. (This probabilistic threshold adjustment encourages group learning while protecting personal payoff against unconditional defectors).
   - If a round occurs where your own contribution was $C$ and you observe $C_{t-1} < m$ *after* you have contributed, transition to $S = Defection\_Triggered$ if your specific contribution was necessary to reach $m$ and the group failed, or if the group failed consistently for $\lceil r/4 \rceil$ consecutive rounds.

3. **Defection State:** If $S == Defection\_Triggered$:
   - Play $D$ for the remainder of the game to avoid exploitation.

4. **Terminal Phase:** In the final round $r$, if $S == Active$, play $C$ regardless of previous outcomes, provided that $C_{r-1} \geq m-1$. If $C_{r-1} < m-1$, play $D$.

### Pseudocode
```python
state = "Active"
history = []

def get_action(t, n, m, k, r, last_round_cooperators):
    if t == 1:
        return "C"
    
    if state == "Defection_Triggered":
        return "D"
    
    # Check if group is viable or failing
    if last_round_cooperators >= m:
        return "C"
    
    # Adaptive Threshold Adjustment
    # If the group failed, cooperate with a probability that scales 
    # with the deficit, but defect if the trend is hopeless.
    deficit = m - last_round_cooperators
    if deficit > (n / 2):
        state = "Defection_Triggered"
        return "D"
    
    # Prosocial gamble: Contribute to try to pull the group over the threshold
    return "C" if random_float() < (1 - (deficit / n)) else "D"
```
'''

description_PROSOCIAL_22 = '''
A conditional threshold-trigger strategy is employed to balance prosocial contribution with risk mitigation against exploitative behavior. 

**Round 1:**
Contribute (C). This establishes a cooperative baseline to signal intent to reach the threshold $m$.

**Subsequent Rounds (2 to $r-1$):**
Monitor the history of total contributions ($C_{total}$) from the previous round.

1.  **If $C_{total} \ge m$:**
    *   If you played C in the previous round: Play C.
    *   If you played D in the previous round: Play C. (This is a "tit-for-tat" recovery mechanism to signal willingness to restore the threshold).

2.  **If $C_{total} < m$:**
    *   If you played C in the previous round: Switch to D.
    *   If you played D in the previous round: Play D.
    *   *Exception:* If the current round is the *only* remaining opportunity to meet the cumulative project goals (if an external constraint existed), play C; otherwise, maintain D until the next round to incentivize other players to switch to C. 

**Final Round ($r$):**
*   If $C_{total} \ge m-1$ in the previous round: Play C. This assumes that one additional contribution is likely to trigger the collective reward, making the marginal utility of C positive ($k - 1 > 0$ since $k > 1$).
*   If $C_{total} < m-1$ in the previous round: Play D. If the threshold is mathematically unattainable or statistically unlikely based on recent trends, maximizing private payoff is the rational choice.

**Pseudocode:**

```python
def decide_action(round, history, n, m, k):
    if round == 1:
        return 'C'
    
    prev_total_cooperators = history[-1].total_cooperators
    prev_my_action = history[-1].my_action
    
    # Check if we successfully reached the threshold last round
    if prev_total_cooperators >= m:
        return 'C'
    
    # If we failed, punish the outcome by defecting
    # unless we were the only one holding back, then re-engage
    if prev_total_cooperators < m:
        # If I defected and we failed, check if I could have tipped the balance
        # If cooperating last round would have met the threshold:
        if (prev_total_cooperators + 1) >= m and prev_my_action == 'D':
            return 'C'
        else:
            return 'D'
    
    # Final round logic: threshold contribution
    if round == r:
        if prev_total_cooperators >= (m - 1):
            return 'C'
        else:
            return 'D'
```
'''

description_PROSOCIAL_23 = '''
Cooperate in the first round to signal intent and establish a foundation for collective success.

For all subsequent rounds (t > 1), adopt a conditional cooperation rule based on the previous round’s outcome:

1. Let $C_{t-1}$ be the number of cooperators observed in the previous round.
2. If $C_{t-1} \ge m$, continue to cooperate, as the collective is currently meeting the threshold.
3. If $C_{t-1} < m$, and you were a cooperator in the previous round, switch to defect (D) for one round. If you were a defector in the previous round, continue to defect (D). This serves to minimize personal loss when the threshold is not being met by the group, while simultaneously signaling a refusal to subsidize failure.
4. If you have been defecting due to a previous failure (rule 3) and observe that the group has returned to meeting the threshold ($C_{t-1} \ge m$), return to cooperating in the next round.

For the final round (t = r):
- If the game history shows a trend of successful cooperation ($C_{t-1} \ge m$ for the majority of the game), cooperate regardless of the current state, as there is no future round to incentivize or punish.
- If the game history shows a trend of failure ($C_{t-1} < m$ for the majority of the game), defect to preserve private resources.

Edge case behavior:
- If the observed number of cooperators is exactly $m-1$, cooperate in the next round, regardless of your previous action, to provide the pivotal contribution required to reach the threshold.
- If the observed number of cooperators is exactly $m$, maintain cooperation.
- If the observed number of cooperators is $> m$, maintain cooperation.
'''

description_PROSOCIAL_24 = '''
Start by playing C in the first round. In subsequent rounds, determine your action based on the recent history of the group's cooperation, utilizing a threshold-based trigger mechanism to maintain cooperation while protecting against persistent non-cooperators.

Define the following variables:
- $C_{prev}$: The number of cooperators in the previous round.
- $MyLastAction$: Your action in the previous round (C=1, D=0).
- $k_{limit} = k - 1$: The net gain of cooperating versus defecting when the threshold is met.

**Decision Logic:**

1. **Initial Round ($t=1$):**
   - Play C.

2. **Subsequent Rounds ($t > 1$):**
   - If you played C in the previous round ($MyLastAction = 1$):
     - If $C_{prev} \geq m$: You are in a cooperative equilibrium. Play C.
     - If $C_{prev} < m$: The group failed to reach the threshold. To signal that cooperation is conditional and prevent exploitation, defect. Play D.
   - If you played D in the previous round ($MyLastAction = 0$):
     - If $C_{prev} \geq m - 1$: The group is close to or achieving the threshold. It is safe to resume cooperation. Play C.
     - If $C_{prev} < m - 1$: The group is far from the threshold. Continued defection is necessary to minimize losses. Play D.

3. **Terminal Round ($t = r$):**
   - If $C_{prev} \geq m - 1$: Play C to maximize the final round potential.
   - Else: Play D, as the game ends and future reciprocity is impossible.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, prev_cooperators, my_last_action, m):
    # Initial round
    if round_number == 1:
        return 'C'

    # Terminal round logic
    if round_number == total_rounds:
        if prev_cooperators >= (m - 1):
            return 'C'
        else:
            return 'D'

    # Adaptive reciprocity logic
    if my_last_action == 'C':
        if prev_cooperators >= m:
            return 'C'
        else:
            return 'D'
    else: # my_last_action == 'D'
        if prev_cooperators >= (m - 1):
            return 'C'
        else:
            return 'D'
```
'''

description_PROSOCIAL_25 = '''
**Strategy Name: Conditional Threshold Reciprocator**

**Decision Rule:**
Let $C_t$ be the number of players who cooperated in round $t$. Let $target = m$ be the threshold for success.

1. **Initial Round ($t=1$):**
   Play Cooperate ($C$).

2. **Intermediate Rounds ($1 < t < r$):**
   - If the previous round resulted in total cooperation $C_{t-1} \ge m$, play Cooperate ($C$).
   - If the previous round resulted in $C_{t-1} < m$, play Defect ($D$) with probability $P_D = \frac{m - C_{t-1}}{n}$, otherwise play Cooperate ($C$). This acts as a dampener to prevent total collapse while signaling a need for higher participation.

3. **Final Round ($t=r$):**
   - If $C_{r-1} \ge m$, play Cooperate ($C$).
   - If $C_{r-1} < m$, play Defect ($D$).

**Pseudocode:**

```python
def decide_action(t, r, n, m, history):
    # Base case: Always cooperate in the first round to signal intent
    if t == 1:
        return 'C'
    
    # Final round: Only cooperate if the previous round was a success
    if t == r:
        if history[-1] >= m:
            return 'C'
        else:
            return 'D'
    
    # Intermediate rounds: Reciprocate success, adjust to failure
    prev_cooperators = history[-1]
    
    if prev_cooperators >= m:
        # Success: Reward the group by maintaining cooperation
        return 'C'
    else:
        # Failure: Calculate probabilistic adjustment
        # Probability of D scales with how far the group was from the threshold
        # This encourages others to increase cooperation without abandoning the project
        deficit = m - prev_cooperators
        prob_defect = min(1.0, deficit / n)
        
        if random_float() < prob_defect:
            return 'D'
        else:
            return 'C'
```

**Edge Case Handling:**
- **Threshold Met Exactly ($C_{t-1} = m$):** Always treat as a success ($C$).
- **Total Defection ($C_{t-1} = 0$):** Play $D$ with probability $m/n$. This forces a reassessment of group norms without permanently defecting, which keeps the possibility of future coordination open if other players attempt to pivot.
- **Last Round Logic:** Defection in the final round is only triggered if the previous round failed to reach the threshold, as there is no future utility to gain from signaling cooperation once the time horizon expires.
'''

description_PROSOCIAL_26 = '''
The strategy employs a conditional threshold-based cooperation mechanism, utilizing a tit-for-tat variant adapted for anonymous, multi-player threshold games. It prioritizes the establishment of mutual cooperation in early rounds while maintaining resilience against free-riders.

**Strategy Definitions:**
- *Target Contribution*: Aim for exactly *m* cooperators to achieve the threshold without unnecessary sacrifice.
- *Cooperation Level (L_t)*: The number of cooperators in round *t*.
- *Threshold Status*: Met if *L_t* ≥ *m*; otherwise, Not Met.

**Pseudocode and Logic:**

1. **Initialization**:
   - In Round 1, Cooperate (C) with probability *p = m/n*. This initiates potential coordination without guaranteeing failure or total over-contribution.

2. **Subsequent Rounds (2 ≤ t ≤ r)**:
   - If *L_{t-1}* ≥ *m*: 
     - You played C: Continue to Cooperate (C) with probability *p = m/n*.
     - You played D: Defect (D). (Testing if the group threshold remains stable without your contribution).
   - If *L_{t-1}* < *m*:
     - If you played C previously and the threshold was not met: Defect (D) for one round to signal that "cooperation is failing" to others, then switch to the "Recoupment Phase."
     - If you played D previously and the threshold was not met: Cooperate (C). (This assumes the role of a "leader" to try and push the group over the threshold).

3. **Recoupment Phase (Correction Mechanism)**:
   - If the group has failed to meet the threshold for two consecutive rounds:
     - Cooperate (C) unconditionally for one round to attempt to restart the coordination cycle.
     - If this fails to meet the threshold, revert to playing Defect (D) for the remainder of the game, as the group is non-cooperative.

4. **Edge Cases**:
   - *Last Round (t = r)*:
     - If *L_{r-1}* ≥ *m*: Play Cooperate (C) if you played Cooperate in *r-1*, or Play Defect (D) if you played Defect in *r-1*.
     - If *L_{r-1}* < *m*: Play Cooperate (C) if you believe the group can still reach *m* with your help; otherwise, play Defect (D).
   - *Over-contribution*: If *L_{t-1}* > *m*, and you played C, increase the probability of playing Defect (D) in the next round by a factor of *(L_{t-1} - m) / n* to discourage inefficient over-contribution while maintaining the threshold.

**Prosocial Alignment**:
The strategy is designed to balance the collective interest with individual incentive. It actively attempts to reach the *m* threshold to maximize group utility (the *k* reward) rather than minimizing personal contribution (the *c* cost). By using probability-based entry in Round 1 and adaptive response to *L_t*, the strategy avoids the "always cooperate" trap of being exploited while avoiding the "always defect" trap of equilibrium collapse. It interprets non-cooperation not as a permanent state, but as a coordination failure, and attempts to break deadlocks when the threshold is missed.
'''

description_PROSOCIAL_27 = '''
The strategy is defined by a conditional cooperation framework using a "trigger-threshold" mechanism, designed to maximize collective welfare while minimizing exploitation.

**Initialization (Round 1):**
Play Cooperate (C) with probability 1.

**Subsequent Rounds (t > 1):**
Let $N_{C, t-1}$ be the number of cooperators in the previous round.
Let $I_{C, t-1}$ be an indicator variable where 1 denotes you played C in the previous round, and 0 denotes you played D.

1.  **If the collective goal was achieved ($N_{C, t-1} \ge m$):**
    *   If $I_{C, t-1} = 1$: Continue to play Cooperate (C). You are successfully contributing to the threshold.
    *   If $I_{C, t-1} = 0$: Play Cooperate (C) with probability $p = 1 - \frac{N_{C, t-1}}{n}$. This "repentance" mechanism allows you to rejoin cooperation if you previously defected, with the likelihood of rejoining inversely proportional to the group's current contribution levels.

2.  **If the collective goal was not achieved ($N_{C, t-1} < m$):**
    *   If $N_{C, t-1} < m - 1$: Play Defect (D). If the group is far from the threshold, contributing alone is a sunk cost that provides no reward.
    *   If $N_{C, t-1} = m - 1$: Play Cooperate (C). By being the critical $m$-th contributor, you trigger the reward $k$ for the entire group. This is the "Rescue Move."

**Terminal Phase (Round $r$):**
Ignore the repentance mechanism. Play Cooperate (C) if $N_{C, r-1} \ge m-1$ or if the group achieved the threshold in more than 50% of previous rounds. Otherwise, play Defect (D) to prevent exploitation in the final round.

**Pseudocode Logic:**

```python
if round == 1:
    return C

if round == r:
    if prev_cooperators >= m - 1 or success_rate > 0.5:
        return C
    else:
        return D

if prev_cooperators >= m:
    if my_last_move == C:
        return C
    else:
        # Repentance: higher chance to cooperate if few people contributed
        return C if random() < (1 - prev_cooperators / n) else D

else: # prev_cooperators < m
    if prev_cooperators == m - 1:
        return C # Rescue move
    else:
        return D # Conserve resources
```
'''

description_PROSOCIAL_28 = '''
Initialize a counter `cooperation_streak` to 0.

**Round 1:**
Play **C**.

**Subsequent Rounds:**
Calculate `threshold_met = 1` if the number of cooperators in the previous round was ≥ `m`, else `0`.

Update `cooperation_streak`:
- If `threshold_met == 1`: `cooperation_streak` = `cooperation_streak + 1`
- If `threshold_met == 0`: `cooperation_streak` = 0

**Decision Rules:**
1. **Targeting:** Identify the minimum number of cooperators needed for collective success. In each round `t`, determine the required number of additional cooperators `needed = max(0, m - (observed_cooperators_in_t-1))`. 
2. **Conditional Cooperation:** 
   - If `t == r` (last round): Play **D**.
   - If `threshold_met == 1`: Play **C** with probability `p`, where `p = min(1.0, (m / n) + 0.1)`. This provides a stable base of contribution while hedging against exploitation.
   - If `threshold_met == 0`:
     - If `observed_cooperators_in_t-1 == 0` or `observed_cooperators_in_t-1 == 1`: Play **D** for the current round to minimize loss, effectively resetting the coordination effort.
     - If `observed_cooperators_in_t-1 >= (m - 1)`: Play **C**. This is a "lenient tit-for-tat" approach, attempting to recover cooperation when the group is close to the threshold.

**Edge Case Handling:**
- **Initial Defection:** If the group fails to meet the threshold in the first round, play **D** for the second round to avoid being the only contributor, then play **C** in the third round to signal a restart of the cooperative effort.
- **Exploitation Guard:** If `observed_cooperators_in_t-1` is significantly higher than `m` but your own payoff suggests you are consistently in the minority of contributors (specifically, if `my_previous_action == C` and `observed_cooperators_in_t-1 == m`), reduce contribution probability by 50% for one round to test if the group sustains the threshold without your input.
'''

description_PROSOCIAL_29 = '''
**Strategy: Threshold-Adaptive Reciprocity (TAR)**

The strategy relies on a trigger-threshold mechanism designed to establish cooperation, maintain it, and gracefully exit if the collective fails to sustain the threshold. It tracks the collective history using two variables: `total_cooperated_rounds` (how many rounds the group has met or exceeded the threshold $m$) and `current_streak` (consecutive rounds meeting the threshold).

### Decision Logic

**Round 1:** 
Play **C**. This initiates a signal of willingness to cooperate.

**Rounds $t = 2$ to $r - 1$:**
Determine the number of cooperators in the previous round ($C_{t-1}$).
1. If $C_{t-1} \ge m$: Play **C**. The collective successfully met the threshold, so maintain cooperation to sustain the equilibrium.
2. If $C_{t-1} < m$:
    - If `total_cooperated_rounds` / $t > 0.5$: Play **C**. This treats a single failure as a temporary dip and attempts to steer the group back to the cooperative equilibrium (Conditional Reset).
    - If `total_cooperated_rounds` / $t \le 0.5$: Play **D**. The collective has failed to demonstrate consistent cooperation; switch to defect to minimize personal loss until the final round.

**Round $r$ (Last Round):**
Determine the number of cooperators in round $r-1$ ($C_{r-1}$).
- If $C_{r-1} \ge m$: Play **C**. Support the threshold for the final round.
- If $C_{r-1} < m$: Play **D**. There is no future round to incentivize or punish; maximize the final payoff.

### Pseudocode

```python
def decide(n, r, m, k, history):
    # history stores a list of previous rounds, each containing total_cooperators
    current_round = len(history) + 1
    
    if current_round == 1:
        return 'C'
    
    # Calculate state metrics
    prev_cooperators = history[-1]
    successful_rounds = sum(1 for h in history if h >= m)
    
    # Last round logic
    if current_round == r:
        return 'C' if prev_cooperators >= m else 'D'
    
    # Reciprocity logic
    if prev_cooperators >= m:
        return 'C'
    else:
        # Check if collective cooperation is historically viable
        success_ratio = successful_rounds / (current_round - 1)
        if success_ratio > 0.5:
            return 'C'
        else:
            return 'D'
```

### Edge Cases
- **Low-Success Groups:** If the group fails to reach $m$ in more than half of the played rounds, the strategy defaults to **D** for all subsequent rounds, preventing exploitation while acknowledging that the group is not viable for collective success.
- **Single-Round Dip:** If a group is highly cooperative but fails once, the `success_ratio > 0.5` rule ensures the strategy provides a "bridge" to allow the group to recover in the following round rather than instantly defecting.
'''

description_PROSOCIAL_30 = '''
**Strategy: Conditional Threshold Tit-for-Tat (CT-TFT)**

**1. Initial Move (Round 1)**
Play **Cooperate (C)**. This signals a commitment to achieving the collective threshold.

**2. Core Decision Rule (Rounds 2 to r-1)**
Calculate the number of cooperators from the previous round, $C_{t-1}$. 
- If $C_{t-1} \ge m$, play **Cooperate (C)**. This maintains the collaborative equilibrium when it is being successfully achieved.
- If $C_{t-1} < m$ and the number of other cooperators (excluding self) was $m-1$ (i.e., you were the pivotal player who could have tipped the balance but chose C), play **Defect (D)** for one round as a "warning" signal to punish the failure to reach the threshold, then revert to **C** in the following round.
- If $C_{t-1} < m$ and the number of other cooperators was significantly lower than $m-1$, play **Defect (D)**. This protects against exploitation when the group is clearly failing to reach the threshold.

**3. Terminal Phase (Last Round)**
If the cumulative success rate of the group over rounds $1$ to $r-1$ has been consistently high (e.g., $C_t \ge m$ in at least 75% of prior rounds), play **Cooperate (C)**. Otherwise, play **Defect (D)** to maximize individual payoff, as the final round offers no future leverage to encourage cooperation.

**4. Edge Case Handling**
- **Triggering Cooperation:** If the group fails to meet the threshold for two consecutive rounds where you played C, switch to **Defect (D)** for one round. If the group meets the threshold in any subsequent round, immediately resume **Cooperate (C)**.
- **Pivotal Logic:** If your cooperation is strictly necessary to reach the threshold (i.e., exactly $m-1$ others cooperated in the previous round), prioritize **Cooperate (C)** regardless of recent performance, unless the group has defected for the majority of the game.
'''

description_PROSOCIAL_31 = '''
The strategy follows a conditional cooperation framework with a trigger for defecting against non-contributors, designed to incentivize reaching the threshold $m$.

**State Variables:**
- Let $C_{t-1}$ be the number of players who cooperated in the previous round.
- Let $S$ be the current cooperation status: $S \in \{Cooperative, Retaliatory\}$. Initialize $S = Cooperative$.
- Let $N_C$ be the number of cooperators observed in the previous round.

**Decision Rules:**

*   **Round 1:** Play $C$ if $m \leq n/2$. If $m > n/2$, play $D$ to avoid guaranteed exploitation unless the group appears highly cooperative; specifically, play $C$ if the expected probability of others cooperating exceeds $(m-1)/(n-1)$.

*   **Subsequent Rounds ($t > 1$):**
    *   **If $S = Cooperative$:**
        *   If the threshold was met in the previous round ($N_C \geq m$): Play $C$.
        *   If the threshold was *not* met ($N_C < m$):
            *   If you played $C$ and others played $D$ (meaning $N_C$ was close to $m$ but failed), continue to play $C$ for one additional round to signal commitment.
            *   If $N_C$ was significantly below $m$, switch to $S = Retaliatory$ and play $D$.
    *   **If $S = Retaliatory$:**
        *   Play $D$ for the remainder of the game.
        *   Exception: If, while in the Retaliatory state, the group suddenly reaches the threshold $m$ in a round where you played $D$, transition back to $S = Cooperative$ and play $C$ in the next round to test for renewed cooperation.

*   **Final Round ($t = r$):**
    *   If $S = Cooperative$, play $C$ regardless of the potential for free-riding.
    *   If $S = Retaliatory$, play $D$.

**Pseudocode:**

```python
# Initialize
state = "Cooperative"
if m <= n / 2: 
    action = C
else: 
    action = D # Or threshold probability check

# Update loop
for t from 2 to r:
    if state == "Cooperative":
        if N_C >= m:
            action = C
        elif N_C >= (m - 1) and my_last_action == C:
            action = C
        else:
            state = "Retaliatory"
            action = D
    
    elif state == "Retaliatory":
        action = D
        # Recovery trigger
        if N_C >= m:
            state = "Cooperative"
            action = C
            
    if t == r:
        if state == "Retaliatory": action = D
        else: action = C
```
'''

description_PROSOCIAL_32 = '''
**Strategy: Adaptive Threshold Trigger (ATT)**

**Objective:** Maintain exactly $m$ cooperators per round to maximize collective benefit while minimizing unnecessary individual contributions.

**Initialization:**
- Define Target_Cooperators ($T$) = $m$.
- Track $H_{coop}$, the count of cooperators in the previous round.

**Decision Rules:**

*   **Round 1:** Play $C$ with probability $p = m/n$. This establishes an initial participation baseline proportional to the threshold requirement.

*   **Subsequent Rounds ($t > 1$):**
    *   If $H_{coop} \ge m$: The collective threshold was met. Play $D$ in the current round to recover the individual endowment while maintaining the group benefit.
    *   If $H_{coop} < m$: The collective threshold was not met. Play $C$ in the current round to actively attempt to reach the threshold $m$.

*   **Last Round ($t = r$):**
    *   If $H_{coop} \ge m$: Play $D$. There is no future round to punish or reward, and the threshold is already satisfied.
    *   If $H_{coop} < m$: Play $C$. The immediate potential reward $k$ justifies the contribution, regardless of future implications.

**Adaptive Refinement (The "Stickiness" Factor):**
To avoid unstable oscillations where the group flips between meeting and missing the threshold, incorporate a "Stability Buffer."

*   If $H_{coop} = m$: Play $D$ with probability $0.8$ and $C$ with probability $0.2$. This slight "overshoot" bias provides a safety net against opponents who might unilaterally switch to $D$.
*   If $H_{coop} = m+1$: Strictly play $D$. The group is operating at sufficient efficiency.

**Pseudocode:**

```python
def choose_action(round_number, prev_coop_count, n, m):
    if round_number == 1:
        return 'C' if random.random() < (m / n) else 'D'
    
    if prev_coop_count >= m:
        # Threshold met, try to save endowment unless buffer is needed
        if prev_coop_count == m:
            return 'C' if random.random() < 0.2 else 'D'
        return 'D'
    
    # Threshold failed, must contribute
    return 'C'
```
'''

description_ALTRUISTIC_5 = '''
The strategy employs a "Conditional Tit-for-Tat with Threshold Sensitivity" approach. It attempts to facilitate cooperation while maintaining a fallback to defection if the collective fails to meet the threshold reliably.

### Strategy Parameters and Variables
- `Threshold_Buffer`: A small margin added to `m` to account for potential variance in partner cooperativeness. Set `Threshold_Buffer = 1`.
- `Target_Cooperation_Level`: `m + Threshold_Buffer`.
- `History_Memory`: The aggregate number of cooperators from the previous round (`C_prev`).

### Decision Rules
1. **Initial Round (t=1):** Always Cooperate (C). This establishes a signaling baseline.

2. **Subsequent Rounds (t > 1):**
   - Let `C_prev` be the number of cooperators observed in the previous round.
   - If `C_prev >= m`: Cooperate (C). This reinforces the successful state where the collective risk is averted.
   - If `C_prev < m`: Defect (D). This acknowledges that the collective failed to reach the threshold, and keeping the endowment (1) is the utility-maximizing action when the reward (k) is unreachable.

3. **Last Round (t = r):**
   - If `C_prev >= m`: Cooperate (C).
   - If `C_prev < m`: Defect (D).
   - *Note:* The strategy does not exploit the final round because doing so breaks the cooperative equilibrium essential for maximizing total long-term group utility.

### Pseudocode Logic
```python
# Constants defined by game parameters
target = m 

def get_action(round_number, previous_round_cooperators):
    # Base Case: Initial Round
    if round_number == 1:
        return "C"
    
    # Conditional Response: Check if threshold was met
    if previous_round_cooperators >= target:
        return "C"
    else:
        return "D"
```

### Altruistic Alignment
The strategy assumes that others are also seeking the collective reward. By cooperating immediately, the agent signals willingness to contribute to the public good. By defecting only when the threshold `m` is missed, the agent minimizes individual loss during failed rounds without actively sabotaging potential future coordination. The strategy is "forgiving" because it resets to "C" if the group dynamics improve in subsequent rounds, allowing the group to recover cooperation if temporary noise or defection occurred.
'''

description_ALTRUISTIC_6 = '''
Define a target cooperation threshold, $T$, equal to $m$. Maintain an internal counter $C_{hist}$ representing the running average of cooperation observed from opponents across previous rounds.

In each round $t$:

1.  **First Round ($t=1$):** Cooperate. This signals willingness to participate in the collective effort.

2.  **Subsequent Rounds ($t > 1$):**
    *   Calculate the number of cooperators from the previous round, $O_{t-1}$.
    *   If $O_{t-1} \geq m - 1$ (where the "-1" accounts for your own contribution in the previous round), assume the group is functioning effectively. Continue to Cooperate.
    *   If $O_{t-1} < m - 1$, the threshold was not met or was met solely by your contribution without sufficient support. Switch to Defect for one round to minimize losses while testing the group's response to lower contribution levels.

3.  **Endgame Phase ($t = r$):**
    *   Cooperate regardless of previous history if the total number of cooperative actions observed across rounds $1$ to $r-1$ suggests a cumulative trend toward $m$ cooperators per round.
    *   Otherwise, Defect.

4.  **Altruistic Adjustment:**
    *   If at any point $O_{t-1} \geq m$, and you were previously defecting due to poor group performance, immediately return to Cooperate (Tit-for-Tat with forgiveness).
    *   Prioritize collective success (reaching $m$) over personal payoff maximization, provided that the group average of cooperation is trending toward $m$. If the group consistently fails to reach $m$ despite your cooperation, revert to Defect to protect your resources for future opportunities, only attempting to "re-ignite" the project by Cooperating every 3rd round.

**Pseudocode Logic:**

```python
# Initial state
strategy = "Cooperate"
# Check if group is viable based on history
if t > 1:
    if observed_opponents_cooperated[t-1] >= m - 1:
        strategy = "Cooperate"
    elif observed_opponents_cooperated[t-1] < m - 1:
        # Check for re-ignition condition
        if t % 3 == 0:
            strategy = "Cooperate"
        else:
            strategy = "Defect"
            
# Last round override
if t == r:
    if total_historical_cooperation / (t-1) >= (m-1)/n:
        strategy = "Cooperate"
    else:
        strategy = "Defect"
```
'''

description_ALTRUISTIC_7 = '''
**Strategy: Threshold-Tit-for-Tat (TTFT)**

The objective is to establish and maintain a cooperative equilibrium that satisfies the threshold *m* while minimizing free-rider exploitation. The strategy functions as a conditional cooperator that tracks the recent success of the collective.

**Decision Rules**

1.  **Phase Initialization (Round 1):** 
    Play Cooperate (C). Assuming the collective will attempt to reach the threshold *m* is necessary to initiate coordination.

2.  **State Assessment (Round *t > 1*):**
    Let *C_{t-1}* be the number of cooperators observed in the previous round.
    *   **If *C_{t-1} ≥ m*:** You achieved the threshold. Play Cooperate (C). This reinforces the successful equilibrium.
    *   **If *C_{t-1} < m*:** The collective failed. Play Defect (D). This signals that you will not subsidize a non-functional outcome.

3.  **Recovery Protocol (The "Probe"):**
    If the strategy is in a state of Defect due to a failure (rule 2b), monitor for a return to cooperation. Every *x* rounds (where *x* is a small integer, e.g., 3), switch to Cooperate (C) for a single round to probe if the other players are willing to resume the cooperative threshold.
    *   If the probe results in a successful threshold (*C_{probe} ≥ m*), resume playing Cooperate (C) indefinitely.
    *   If the probe fails (*C_{probe} < m*), revert to Defect (D) and reset the probe counter.

**Edge Cases**

*   **The Final Round (Round *r*):**
    If the previous round was a success (*C_{r-1} ≥ m*), play Cooperate (C) to maximize the final collective payout. If the previous round was a failure (*C_{r-1} < m*), play Defect (D), as there is no future interaction to incentivize.

*   **Low Population Dynamics (*n* vs *m*):**
    If the threshold *m* is extremely high relative to *n* (e.g., *m = n*), the strategy remains rigid. If *m* is low, the strategy remains permissive. The decision rule *C_{t-1} ≥ m* naturally adjusts for any value of *m*.

**Pseudocode Representation**

```python
def get_action(round, history):
    if round == 1:
        return 'C'
    
    if round == r:
        return 'C' if history.last_round_success else 'D'
    
    if history.last_round_success:
        return 'C'
    
    # Recovery Protocol
    if (round % 3) == 0:
        return 'C'
    
    return 'D'
```
'''

description_ALTRUISTIC_8 = '''
Cooperate if and only if the probability of the group failing to reach the threshold $m$ without your contribution is high, or if history indicates a stable cooperative equilibrium is achievable.

### Decision Rules

1. **Round 1 (Initialization):**
   - Cooperate (C) unconditionally. This establishes an altruistic intent.

2. **Rounds 2 through $r-1$ (Monitoring and Adaptation):**
   Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
   - If $C_{t-1} \ge m$: The threshold was met. Play C if $C_{t-1} > m$ (signaling robustness) or if you played D previously and the threshold was still met (maintaining the status quo). If $C_{t-1} = m$, there is a risk of a "free-rider" collapse. Play C with probability $p = 1 - \epsilon$ (where $\epsilon$ is a small constant, e.g., 0.05) to maintain the threshold while testing for excessive defectors.
   - If $C_{t-1} < m$: The threshold was missed. Play C. If the group consistently fails to reach $m$ for 3 consecutive rounds, switch to D for 1 round to minimize personal loss, then revert to C.

3. **Round $r$ (Terminal):**
   - Cooperate (C) if the group reached the threshold in round $r-1$.
   - If the group failed to reach the threshold in round $r-1$, Defect (D) to avoid the certain loss of endowment for an unachievable collective benefit.

### Pseudocode Logic

```python
def decide_action(round_num, history, n, m, k):
    # Round 1: Establish altruism
    if round_num == 1:
        return 'C'

    # Terminal Round: Rational protection if goal is unattainable
    if round_num == r:
        if history.last_round_cooperators >= m:
            return 'C'
        else:
            return 'D'

    # General rounds: Altruistic stability
    prev_cooperators = history.last_round_cooperators
    
    if prev_cooperators >= m:
        # Group is stable; contribute if you aren't the sole reason the threshold is met
        # (This discourages free-riding while supporting the group)
        if prev_cooperators > m:
            return 'C'
        else:
            # Threshold is fragile; contribute to maintain
            return 'C'
    
    else:
        # Threshold was missed; persist in contributing unless in deep deficit
        if history.streak_failed_threshold >= 3:
            return 'D' # Minimize unnecessary loss
        else:
            return 'C' # Attempt recovery
```

### Edge Cases
- **Low cooperation streak:** If the group fails to reach $m$ for 3 rounds, the strategy assumes the group is non-cooperative and shifts to D to preserve the endowment, checking back into C periodically (every 4th round).
- **Threshold "Just-in-Time":** If $C_{t-1}$ is exactly $m$, the strategy acts as a linchpin, ensuring the threshold is met, effectively sacrificing personal payoff to preserve the collective reward.
'''

description_ALTRUISTIC_9 = '''
Adopt a "Conditional Reciprocity with Patience" strategy, designed to foster cooperation while mitigating the risk of exploitation.

**Initialization (Round 1):**
Play C (Cooperate). This signals an initial willingness to contribute toward the collective goal.

**Monitoring Phase (Rounds 2 to r-1):**
Maintain a memory of the previous round's outcome, specifically observing the total number of cooperators ($N_c$).

*   **Case 1 (Threshold Met, $N_c \ge m$):**
    If you played C in the previous round, continue to play C. This reinforces the cooperative equilibrium.
    If you played D in the previous round, play C (return to cooperation).

*   **Case 2 (Threshold Missed, $N_c < m$):**
    If the threshold was missed by only one person (i.e., $N_c = m-1$ and you played D), play C.
    If the threshold was missed by a significant margin ($N_c < m-1$) or you are being exploited (i.e., you played C while others played D, resulting in a low $N_c$), switch to D for one round to signal that cooperation is not being reciprocated sufficiently.
    If you played D in the previous round and the threshold was missed, continue to play D to avoid wasting resources on a non-viable collective effort.

**Termination Phase (Last Round, $r$):**
If the historical success rate of reaching the threshold $m$ across previous rounds $r_{1 \dots r-1}$ is $\ge 50\%$, play C. Otherwise, play D. This prevents final-round defection in stable groups while protecting against persistent non-cooperators.

**Pseudocode Implementation:**

```python
def decide_action(round_number, total_rounds, n, m, history):
    # Round 1: Always start with C
    if round_number == 1:
        return 'C'

    # Retrieve previous round data
    prev_n_c = history[-1].cooperators
    prev_my_action = history[-1].my_action

    # If the threshold was met previously
    if prev_n_c >= m:
        return 'C'

    # If threshold was missed
    if prev_n_c < m:
        # Altruistic recovery: If missed by only 1, try again
        if prev_n_c == m - 1:
            return 'C'
        
        # Protective measure: If heavily missed, punish/conserve
        # Last round logic
        if round_number == total_rounds:
            success_rate = sum(1 for h in history if h.cooperators >= m) / (round_number - 1)
            return 'C' if success_rate >= 0.5 else 'D'
            
        return 'D'
```
'''

description_ALTRUISTIC_10 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Conditional Altruism**

**Core Principle**
Maximize the likelihood of meeting the cooperation threshold $m$ while minimizing individual exploitation by non-cooperative players. Cooperation is offered as a conditional invitation to collective benefit, which is withdrawn if the group fails to sustain the threshold.

**Decision Rules**
Let $C_t$ be the number of cooperators observed in round $t$.

1. **Initialization (Round 1):**
   Cooperate ($C$) if $m/n \le 0.5$ (the threshold represents a minority or parity burden). If $m/n > 0.5$, play Defect ($D$) to avoid exploitation when collective success is statistically improbable without prior coordination.

2. **Transition Rules (Round $t > 1$):**
   *   **Success Continuity:** If the threshold was met in the previous round ($C_{t-1} \ge m$), maintain the current action.
   *   **Failure Recovery:** If the threshold was not met in the previous round ($C_{t-1} < m$), determine the "Contribution Gap" $G = m - C_{t-1}$.
       *   If you played $D$ in $t-1$ and $G=1$, switch to $C$ to test if your individual contribution can bridge the gap.
       *   Otherwise, revert to $D$ for one round to signal that the previous failure resulted in a withdrawal of cooperation.

3. **Termination Phase (Last $x$ rounds, where $x = \min(3, r/4)$):**
   Prioritize unconditional cooperation ($C$) regardless of previous performance, provided that the total payoffs from previous rounds suggest the community has a history of meeting the threshold. If the average cooperation level was consistently below $m$, maintain $D$ to preserve endowment.

**Pseudocode**
```python
# Variables: 
# t = current round
# C_prev = number of cooperators in round t-1
# action_prev = my action in t-1
# endowment = 1, threshold = m

def choose_action(t, C_prev, action_prev):
    # Initialization
    if t == 1:
        return 'C' if (m / n) <= 0.5 else 'D'
    
    # Termination Phase
    if t > (r - min(3, r // 4)):
        return 'C' if (average_C > m - 1) else 'D'
        
    # Standard Adaptive Phase
    if C_prev >= m:
        return action_prev
    else:
        # Attempt to bridge the gap if I was defecting
        if action_prev == 'D' and (C_prev == m - 1):
            return 'C'
        else:
            return 'D'
```

**Edge Case Handling**
*   **Threshold Gap $m - C_{t-1} > 1$:** If the group fails to meet the threshold by a margin greater than one, do not attempt to bridge the gap alone, as this guarantees a loss of utility without achieving the threshold reward. Default to $D$ to minimize losses until the group shows signs of increased participation.
*   **Tie-Breaking:** If $C_{t-1} == m - 1$ and you were already playing $C$, remain at $C$ (your contribution is essential for the collective reward).
'''

description_ALTRUISTIC_11 = '''
**Phase 1: Initial Cooperation (Round 1)**
In the first round, initiate cooperation by playing C. This establishes a willingness to contribute toward the collective threshold regardless of immediate personal payoff.

**Phase 2: Adaptive Reciprocity (Rounds 2 to r-1)**
Calculate the total number of cooperators from the previous round (S_t-1).

If S_t-1 ≥ m:
- If you played C in the previous round, continue playing C.
- If you played D in the previous round, consider this a "successful" threshold without your contribution. To maintain the collective, play C with probability p = (m - S_t-1) / (n - S_t-1) + epsilon to sustain the group, where epsilon is a small buffer (0.05). If the threshold was met comfortably (S_t-1 > m), switch to D to minimize personal cost while assuming the threshold remains secure.

If S_t-1 < m:
- If you played C in the previous round, you must determine if the group failed due to lack of effort or bad luck. If S_t-1 < m - 1, interpret this as a defection spiral. Play D to protect endowment. If S_t-1 = m - 1, the group was one short; play C again to incentivize others to bridge the gap.
- If you played D in the previous round, interpret the failure as a sign that the group is not coordinating. Play C only if the aggregate cooperation rate has historically trended upward. If the trend is flat or downward, continue playing D until a credible signal of cooperation emerges (e.g., S_t-1 rises).

**Phase 3: Terminal Round (Round r)**
In the final round, the incentive for future reciprocity is removed. Play C if and only if S_t-1 ≥ m, acting on the assumption that the group has established a stable equilibrium of cooperation. If the group has not consistently met the threshold in the preceding rounds, play D to maximize the final payoff.

**Logic for Altruistic Adjustment**
At any point, if the collective utility (total payoff of all players) is calculated to be higher when you play C (i.e., when your contribution is the marginal difference between failing the threshold and reaching it), prioritize the group outcome over the individual payoff by playing C, even if it results in a lower immediate personal return. Specifically, if S_t-1 = m - 1, always play C.
'''

description_ALTRUISTIC_12 = '''
**The Conditional Altruism Strategy**

The strategy operates on a "Tit-for-Tat with a Threshold Buffer" logic, aiming to initiate cooperation while protecting against exploitation.

**Decision Logic**

Let $C_{t-1}$ be the number of players who cooperated in the previous round.
Let $M_t$ be a dynamic cooperation threshold, initialized at $m$.
Let $S$ be the state variable where $S=1$ indicates trust has been established, and $S=0$ indicates a return to defensive play.

1.  **Round 1:** Play $C$ (Cooperate).

2.  **Rounds $t = 2$ to $r-1$:**
    *   If $S=1$ (Trust established):
        *   If $C_{t-1} \ge m$, play $C$.
        *   If $C_{t-1} < m$, play $D$ (Defect) to protect resources, set $S=0$, and increment $M_t$ by 1 (the threshold for restoring trust becomes stricter).
    *   If $S=0$ (Defensive state):
        *   If $C_{t-1} \ge M_t$, play $C$, set $S=1$ (Attempt reconciliation).
        *   If $C_{t-1} < M_t$, play $D$.

3.  **Final Round ($t=r$):**
    *   If $S=1$, play $C$.
    *   If $S=0$ and $C_{t-1} \ge m$, play $C$ (Final gesture of goodwill).
    *   Otherwise, play $D$.

**Pseudocode Implementation**

```python
# Initialization
threshold = m
state = 1 # 1: Cooperating/Trusting, 0: Defecting/Suspicious

def decide_action(t, r, prev_cooperators):
    global threshold, state
    
    # First round initialization
    if t == 1:
        return 'C'
    
    # State update logic
    if state == 1:
        if prev_cooperators < m:
            state = 0
            threshold += 1 # Increase difficulty for future trust
            return 'D'
        else:
            return 'C'
            
    else: # state == 0
        if prev_cooperators >= threshold:
            state = 1
            return 'C'
        else:
            return 'D'

    # Final round override
    if t == r:
        if state == 1 or prev_cooperators >= m:
            return 'C'
        else:
            return 'D'
```

**Edge Case Handling**
*   **Persistent Defection:** If opponents consistently fail to meet the $m$ threshold, the strategy maintains $D$ (Defect) to preserve endowment, effectively treating the system as non-cooperative.
*   **Threshold Recovery:** The `threshold` variable scales the barrier to trust recovery. If the group proves unreliable, the strategy requires a higher demonstration of group cooperation (more than $m$) before reverting to $C$.
*   **End-of-Game:** The final round logic prioritizes social welfare over self-interest if there is any evidence of viable cooperation in the preceding round, serving as a non-strategic altruistic gesture.
'''

description_ALTRUISTIC_13 = '''
**Strategy: Conditional Reciprocal Contribution (CRC)**

The strategy operates on the principle of Tit-for-Tat extended to a threshold-based group dynamic. It seeks to induce cooperation by rewarding the group when the threshold is met and punishing/withholding when it is not, while protecting itself from exploitation in the final rounds.

**Variables:**
*   $C_t$: Number of players who cooperated in round $t$.
*   $a_t$: Your action in round $t$ ($1$ for Cooperate, $0$ for Defect).
*   $Threshold\_Met = (C_t \ge m)$.

**Decision Rules:**

1.  **Round 1:**
    *   Play Cooperate ($C$). The goal is to signal a willingness to reach the threshold immediately.

2.  **Rounds 2 to $r-1$:**
    *   Calculate $Threshold\_Met_{t-1}$ from the previous round.
    *   If $Threshold\_Met_{t-1} = \text{True}$: Play Cooperate ($C$). You reward the group for achieving the collective success.
    *   If $Threshold\_Met_{t-1} = \text{False}$: Play Defect ($D$). You signal that you will not subsidize a group that fails to meet the minimum requirements.

3.  **Final Round ($t = r$):**
    *   If $C_{r-1} \ge m$: Play Cooperate ($C$).
    *   If $C_{r-1} < m$: Play Defect ($D$).

**Adaptive Threshold Calibration:**

If at any point $C_t \ge m + 1$ (the threshold was exceeded by more than one person), you adjust your behavior:
*   In the subsequent round, if $C_{t-1} > m$, you may play Defect ($D$) with probability $P = \frac{C_{t-1} - m}{C_{t-1}}$. This "probabilistic defection" discourages excessive contribution beyond what is necessary to achieve the reward, maximizing collective efficiency while maintaining the threshold.

**Pseudocode:**

```python
def get_action(round_number, last_round_cooperators, m, r):
    # Round 1: Open with cooperation
    if round_number == 1:
        return 'C'
    
    # Final Round: Standard reciprocity
    if round_number == r:
        return 'C' if last_round_cooperators >= m else 'D'
        
    # Standard Rounds: Conditional cooperation
    if last_round_cooperators >= m:
        # Check for over-contribution
        if last_round_cooperators > m:
            # Probabilistic defection to maintain efficiency
            if random() < (last_round_cooperators - m) / last_round_cooperators:
                return 'D'
        return 'C'
        
    # If threshold failed previously, defect
    return 'D'
```
'''

description_ALTRUISTIC_14 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Forgiveness**

This strategy relies on a "trigger-threshold" mechanism to encourage stable cooperation while maintaining robustness against defection. The core logic is to cooperate if the collective history shows a commitment to the threshold, and defect otherwise, with an optimistic restart phase.

**Decision Rules:**

1.  **Initialization (Round 1):** Play **Cooperate (C)**. Assume all players intend to meet the threshold.

2.  **Tracking State:** Maintain a variable `is_cooperative_regime` (Boolean), initialized to `True`.
    *   Calculate `cooperators_last_round` based on observation.
    *   If `cooperators_last_round < m`, set `is_cooperative_regime = False`.
    *   If `cooperators_last_round >= m`, set `is_cooperative_regime = True`.

3.  **Active Rounds (Round 2 to r):**
    *   **If `is_cooperative_regime` is True:** Play **Cooperate (C)**.
    *   **If `is_cooperative_regime` is False:**
        *   **For the current round:** Play **Defect (D)** to minimize loss while the threshold is not being met.
        *   **Re-evaluation (The "Olive Branch"):** Every `N` rounds (where `N` is an integer derived from `n/2`), reset `is_cooperative_regime` to `True` for one round and play **Cooperate (C)**. This serves as a test to see if other players are willing to return to the cooperative equilibrium.

**Edge Case Handling:**

*   **Final Round (Round r):**
    *   If `is_cooperative_regime` is `True`, play **Cooperate (C)** regardless of previous outcomes, prioritizing the collective reward `k`.
    *   If `is_cooperative_regime` is `False`, play **Defect (D)**, as the opportunity to rebuild cooperative momentum is zero.

*   **Threshold Boundary:** If `cooperators_last_round == m` (exactly the threshold), maintain `is_cooperative_regime = True`.

*   **Parameter Sensitivity:** If `k` is extremely high (significantly greater than 1), shorten the "Olive Branch" reset interval `N` to 2 rounds to maximize the probability of recapturing the cooperative reward. If `k` is low (close to 1), increase `N` to `n` to minimize the loss from testing defectors.

**Pseudocode Representation:**

```python
def choose_action(round, total_rounds, history, m, n, k):
    if round == 1:
        return 'C'
    
    # Check if cooperative regime was violated in the previous round
    last_round_cooperators = history[round - 1].cooperators
    regime_violated = last_round_cooperators < m
    
    if not regime_violated:
        return 'C'
    
    # If in a violated regime, attempt recovery periodically
    # Interval N is a function of n; here set to floor(n/2)
    recovery_interval = max(2, n // 2)
    
    if round == total_rounds:
        return 'D' # Last round in failed regime is pure defection
        
    if round % recovery_interval == 0:
        return 'C' # Test for renewed cooperation
        
    return 'D'
```
'''

description_ALTRUISTIC_15 = '''
The strategy follows a conditional cooperation protocol based on observed success rates, adjusted for threshold constraints and temporal proximity to the game's end.

**Initialization (Round 1):**
Play C.

**Rounds 2 to r:**
Calculate the aggregate cooperation rate of the population from the previous round, defined as $S_{t-1} = (\text{total cooperators in } t-1) / n$.

If $S_{t-1} \geq (m/n)$, maintain cooperation (C). 
If $S_{t-1} < (m/n)$, trigger a probabilistic assessment to punish defection while testing for re-cooperation:
1. With probability $P = 1 - (t/r)^2$, play C (the "forgiveness/retry" phase).
2. With probability $1-P$, play D (the "punishment/exit" phase).

**Constraint-Specific Adjustments:**
*   **Threshold Sensitivity:** If $m$ is high relative to $n$ (i.e., $m/n > 0.75$), increase the probability of cooperation in the early rounds (first 20% of $r$) to C regardless of history, provided $t < 0.2r$.
*   **Terminal Rounds:** In the final round, if the strategy has achieved a success rate of $S > (m/n)$ for at least 75% of previous rounds, play C. Otherwise, play D if the payoff expectation of C is strictly less than D based on the average historical cooperation rate of the population.

**Pseudocode:**

```python
def decide_action(n, m, r, t, history):
    # Base case for first round
    if t == 1:
        return 'C'

    # Retrieve success rate from last round
    last_round_cooperators = history[t-1].cooperators
    s_t_minus_1 = last_round_cooperators / n
    
    # Check if threshold was met
    threshold_met = last_round_cooperators >= m

    # Strategy for final round
    if t == r:
        if s_t_minus_1 >= (m/n):
            return 'C'
        else:
            return 'D'

    # Standard adaptive logic
    if threshold_met:
        return 'C'
    else:
        # Probabilistic forgiveness decay
        forgiveness_prob = 1 - (t / r)**2
        if random.random() < forgiveness_prob:
            return 'C'
        else:
            return 'D'
```
'''

description_ALTRUISTIC_16 = '''
Adopt a "Conditional Threshold-Trigger" (CTT) strategy designed to sustain collective cooperation while minimizing exploitation.

**Initialization Phase (Round 1):**
Cooperate (C). This establishes a commitment to the collective goal and signals willingness to participate in the threshold requirement.

**Subsequent Rounds (t > 1):**
Calculate the cooperation requirement based on the observed outcomes of the previous round ($C_{t-1}$):
1.  **If $C_{t-1} \geq m$:**
    *   If you played C in $t-1$, continue to play C.
    *   If you played D in $t-1$, switch to C.
    *   *Rationale:* Reinforce a successful collective outcome.

2.  **If $C_{t-1} < m$:**
    *   If you played C in $t-1$, and the collective fell short by only 1 (i.e., $C_{t-1} = m-1$), continue to play C.
    *   If you played D in $t-1$, or if the collective fell short by more than 1 (i.e., $C_{t-1} < m-1$), switch to or remain in D.
    *   *Rationale:* This prevents "sucker" payoffs when the collective fails to reach the threshold, while maintaining support for the group if the threshold was narrowly missed.

**The "Forgiving Reset" Rule:**
To prevent strategy lock-in (if the group fails completely, no one ever cooperates again), initiate a "Reset" every $r_{reset}$ rounds. Define $r_{reset} = \lceil \sqrt{r} \rceil$ or 5, whichever is smaller.
*   In any round $t$ where $(t \mod r_{reset}) == 0$, play C regardless of history. This tests if the group is ready to return to a cooperative equilibrium.

**The "Endgame" Adjustment (Final Rounds):**
For the final 2 rounds, prioritize the collective outcome to maximize total welfare:
*   In round $r-1$: Play C if $C_{r-2} \geq m-1$.
*   In round $r$: Play C if $C_{r-1} \geq m-2$.
*   *Rationale:* In terminal stages, the cost of exploitation is reduced because the risk of long-term retaliation is eliminated. Loosening the cooperation threshold requirements allows for "last-ditch" attempts to secure the collective reward.

**Summary Pseudocode:**

```python
def get_action(round, history):
    if round == 1:
        return C
    
    # Check for Reset
    if round % reset_interval == 0:
        return C
    
    # Endgame heuristic
    if round >= r - 1:
        threshold = m - (r - round + 1)
        return C if history[-1].cooperators >= threshold else D

    # Standard adaptive logic
    prev_C = history[-1].cooperators
    if prev_C >= m:
        return C
    elif prev_C == m - 1 and self.last_action == C:
        return C
    else:
        return D
```
'''

description_ALTRUISTIC_17 = '''
**Strategy: Conditional Threshold Reciprocity**

**Core Principle**
This strategy aims to maximize global welfare (the sum of all payoffs) by coordinating on the minimum threshold $m$ needed to secure the reward $k$, while guarding against exploitation by free-riders. It assumes that cooperation is only sustainable if the reward $k$ exceeds the cost of contribution (1).

**Decision Rules**

1.  **Phase 1: Calibration (Round 1)**
    Contribute (C) if the probability of the group naturally hitting $m$ is considered high, or if the "rational" selfish equilibrium is unattractive. In the first round, default to Cooperate (C) to signal a willingness to provide the public good.

2.  **Phase 2: Observation & Adaptation (Rounds 2 to r-1)**
    Define $C_t$ as the number of cooperators in the previous round.
    *   **Threshold Satisfaction:** If $C_t \ge m$, continue to Cooperate (C). The group has reached the collective goal; maintaining this state maximizes total welfare.
    *   **Under-performance:** If $C_t < m$, check your contribution status.
        *   If you contributed (C) in the previous round and the threshold was not met, switch to Defect (D) for the current round to minimize personal loss while the group fails to organize.
        *   If you defected (D) in the previous round and the threshold was not met, consider the "gap" to $m$. If the group is consistently close to $m$ (i.e., $C_t = m-1$), flip to Cooperate (C) to test if your individual contribution can tip the group into success.
    *   **Exploitation Check:** If you consistently observe that $C_t \ge m$ but the group reward $k$ is insufficient to offset the cost of C relative to defectors (i.e., you are being consistently exploited), reduce contribution frequency to maintain a "tit-for-tat" equilibrium with the group aggregate.

3.  **Phase 3: The Endgame (Round r)**
    Regardless of history, if the aggregate group behavior in $r-1$ has shown a strong tendency toward cooperation ($C_{r-1} \ge m$), Cooperate (C). If the group is unstable or has failed to hit $m$ repeatedly, Defect (D) to protect personal payoff, as there is no future round to incentivize reciprocity.

**Pseudocode Logic**

```python
# Variables:
# m: minimum cooperators needed
# C_prev: number of cooperators in previous round
# my_last_action: my action in previous round

if round == 1:
    return C

if round == r:
    if C_prev >= m:
        return C
    else:
        return D

# Intermediate Rounds
if C_prev >= m:
    # Group successfully coordinates; continue altruism
    return C
else:
    # Group failed; punish exploitation or attempt rescue
    if my_last_action == C:
        # Stop 'wasting' contribution if group is failing
        return D
    else:
        # Attempt to bridge the gap if close
        if C_prev == m - 1:
            return C
        else:
            return D
```

**Edge Case Handling**
*   **Persistent Failure:** If $C_t$ remains significantly below $m$ for 3+ rounds, the strategy shifts to permanent Defection (D) for the remainder of the game, as the group is non-cooperative and attempts to bridge the gap are mathematically futile.
*   **Threshold volatility:** If $C_t$ oscillates around $m$, prioritize C whenever $C_{t-1} \ge m$ and D only when $C_{t-1} < m$ and you previously contributed, ensuring you do not reward non-cooperative cycles.
'''

description_ALTRUISTIC_18 = '''
**Strategy: Threshold-Responsive Tit-for-Tat (TR-TFT)**

**Core Philosophy:**
The strategy aims to establish and maintain a stable equilibrium where the group threshold $m$ is met, prioritizing the welfare of the collective over short-term individual gains. It treats the group as a partner, signaling willingness to cooperate while punishing defection to prevent exploitation.

**Decision Logic:**

*   **Round 1:** Play **Cooperate**. This signals a cooperative intent and initiates the potential for mutual benefit.

*   **Rounds 2 to $r-1$:**
    *   Calculate the cooperation threshold status from the previous round $t-1$.
    *   Let $N_C(t-1)$ be the total number of cooperators observed in the previous round.
    *   **Condition A (Cooperative Baseline):** If $N_C(t-1) \ge m$, play **Cooperate**. The group is successfully meeting the threshold; maintaining this behavior sustains the reward $k$.
    *   **Condition B (Corrective Punishment):** If $N_C(t-1) < m$ and your previous action was $C$, play **Defect**. This signals that the group failed to meet the threshold and cooperation is currently unsustainable without reciprocal effort.
    *   **Condition C (Restorative Probe):** If $N_C(t-1) < m$ and your previous action was $D$, play **Cooperate**. This acts as a probe to restart cooperative behavior, provided the group failed the previous round despite your previous defection.

*   **Final Round ($r$):**
    *   If $N_C(r-1) \ge m$, play **Cooperate**.
    *   If $N_C(r-1) < m$, play **Defect**. (Rational self-protection given no future rounds remain to incentivize others).

**Pseudocode Representation:**

```python
def decide_action(round_number, history, m, n):
    if round_number == 1:
        return 'C'

    if round_number == r:
        if history.last_round_cooperators >= m:
            return 'C'
        else:
            return 'D'

    # Retrieve own action from previous round
    prev_own = history.my_last_action
    prev_observed = history.last_round_cooperators

    # Cooperative Baseline
    if prev_observed >= m:
        return 'C'
    
    # Corrective Punishment: If we cooperated and they failed us
    elif prev_own == 'C':
        return 'D'
        
    # Restorative Probe: If we defected and the group still failed, 
    # we offer a hand to restart the cooperative cycle
    else: 
        return 'C'
```

**Edge Case Handling:**
*   **Persistent Defection:** If the group fails to reach $m$ for consecutive rounds while applying this strategy, the logic enters an alternating cycle of $C$ and $D$. This limits the cost of altruism by ensuring you do not contribute to a project that has no prospect of meeting the threshold, while simultaneously providing a recurring opportunity for other players to switch back to $C$.
*   **Threshold Boundary:** If $N_C = m - 1$ in the previous round and you were a cooperator, the strategy switches to $D$ to signal that your contribution was necessary for the reward, preventing free-riders from exploiting your contribution to meet the threshold.
'''

description_ALTRUISTIC_19 = '''
**Trigger-Threshold Reciprocity Strategy**

The strategy operates on the principle of *conditional altruism*: initiate cooperation to seed the threshold, then maintain cooperation proportional to the group's reliability, while punishing defection just enough to incentivize return to cooperation without collapsing the project.

**Pseudocode and Decision Rules**

Let $C_{t-1}$ be the number of cooperators in the previous round. Let $S_t$ be the action for the current round.

1.  **Initialization (Round 1):**
    Play **C** (Cooperate). This demonstrates commitment to the common good and tests the group's propensity for cooperation.

2.  **Steady State (Rounds 2 to $r-1$):**
    Calculate the effective cooperation rate of the group. If the previous round met or exceeded the threshold ($C_{t-1} \ge m$), play **C**.

    If the threshold was *not* met ($C_{t-1} < m$):
    *   If $C_{t-1} < m - 1$, play **D** (Defect). The group is too far from the threshold for individual contribution to be effective, so preserve resources.
    *   If $C_{t-1} == m - 1$, play **C**. By contributing, you minimize the "free-rider" risk while offering a final attempt to reach the threshold $m$.

3.  **Terminal Phase (Final Round $r$):**
    If the game outcome is still indeterminate (i.e., you are altruistic and seek to maximize total group utility), ignore the temptation to defect for personal gain. Play **C** regardless of history, provided that the projected outcome of cooperation (the reward $k$) outweighs the cost of the individual contribution. Given the altruistic mandate, play **C** if there is any reasonable expectation that the group can collectively hit the threshold $m$, effectively signaling unconditional support to ensure the highest potential global payoff.

**Edge Case Handling**

*   **Persistent Defection:** If the group consistently fails to meet $m$ over multiple rounds, stop cooperating and play **D** indefinitely. Continuous contribution in a non-cooperative environment is irrational and unsustainable.
*   **Near-Threshold Volatility:** If the group oscillates between $m-1$ and $m$, maintain **C** continuously. This acts as an "anchor," guaranteeing that the threshold is met in every round where the group is close to success, thereby rewarding the group's marginal cooperators and incentivizing fence-sitters.
*   **The "Last-Mover" Exception:** In the final round, if the total group cooperation in round $r-1$ was zero, switch to **D**. There is no historical data suggesting cooperation is possible, and the altruistic effort is better spent conserving personal resources in a doomed scenario.

**Altruistic Alignment**

This strategy prioritizes the group's collective benefit ($k$) over individual short-term gains. By initiating cooperation (Round 1) and supporting the threshold when the group is within a single player's contribution of success ($m-1$), the strategy actively fosters a cooperative equilibrium. It avoids the "sucker's payoff" by withdrawing in environments where the threshold cannot be reached, ensuring that altruistic resources are only deployed when they have the highest probability of creating value for the collective.
'''

description_ALTRUISTIC_20 = '''
**Strategy: Threshold-Tit-for-Tat (TTFT)**

The strategy prioritizes maximizing the collective benefit by incentivizing the achievement of the threshold $m$ while punishing unilateral defection and discouraging "free-riding" beyond the threshold.

**1. Decision Rules:**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.

*   **Initial Round ($t=1$):** Cooperate ($C$). The goal is to signal a cooperative intent to establish a stable equilibrium.
*   **Subsequent Rounds ($t > 1$):**
    *   **Cooperate ($C$) IF:**
        *   The threshold was missed in the previous round ($C_{t-1} < m$). This signals a willingness to carry the burden to achieve the collective reward.
        *   The threshold was met exactly in the previous round ($C_{t-1} = m$). This indicates that participation is required to maintain the status quo.
        *   The threshold was met by more than $m$ players ($C_{t-1} > m$), *but* the number of cooperators has decreased compared to the round before that ($C_{t-1} < C_{t-2}$). This acts as a corrective measure to prevent a total collapse into defection.
    *   **Defect ($D$) IF:**
        *   The threshold was met by more than $m$ players ($C_{t-1} > m$) AND the number of cooperators is stable or increasing ($C_{t-1} \geq C_{t-2}$). This strategy assumes that the "excess" cooperators (those beyond $m$) are sufficient to trigger the reward, allowing for private gain without jeopardizing the threshold.

**2. Handling Edge Cases:**
*   **Last Round ($t=r$):** Regardless of history, play $C$ if the goal is absolute maximization of altruistic impact, or follow the rules above if the goal is to maintain game-theoretic consistency. To remain robustly altruistic, play $C$ in the final round if $C_{t-1} \leq m$.
*   **Insufficient Data:** If at any point the environment becomes chaotic or unpredictable (e.g., oscillating wildly between $C_{t-1} < m$ and $C_{t-1} > m+1$), default to $C$ to ensure the threshold is met, effectively prioritizing the collective reward over individual utility.

**3. Altruistic Logic:**
This strategy is altruistic because it guarantees participation when the collective reward is at risk (when $C_{t-1} < m$). It only engages in defection when the threshold is safely exceeded, effectively "testing" the group's stability. By playing $C$ when the group fails, it sacrifices individual payoff to signal the necessity of cooperation, aiming to pull the group dynamic toward a stable $m$-cooperation equilibrium.
'''

description_ALTRUISTIC_21 = '''
In the first round, play Cooperate (C) to establish a cooperative baseline.

For all subsequent rounds, determine your action based on the "Contribution Ratio" (CR) of the previous round, defined as the number of cooperators divided by $n$.

If the game is in the final round (t = r):
- If the target $m$ was met in the previous round, play Defect (D).
- If the target $m$ was not met in the previous round, play Cooperate (C) to maximize the probability of achieving the threshold reward.

For all rounds where $1 < t < r$:
- If the number of cooperators in the previous round was $\ge m$, play Cooperate (C) with probability $p = 1 - \epsilon$ (where $\epsilon$ is a small mutation rate, e.g., 0.05) to maintain the successful threshold state.
- If the number of cooperators in the previous round was $< m$, play Cooperate (C) to attempt to pull the collective toward the threshold.
- If your internal record indicates that the group consistently reaches the threshold ($\ge m$) for three consecutive rounds, switch to Defect (D) to test the group's robustness. If the group fails to meet the threshold in the round immediately following your Defection, revert to Cooperate (C) for all remaining rounds.

Decision Logic Pseudocode:
```
Define history_of_success = True if (previous_cooperators >= m) else False
Define streak_counter = count of consecutive rounds where cooperators >= m

If t == 1:
    return C

If t == r:
    return C if (previous_cooperators < m) else D

If streak_counter >= 3:
    if previous_action == D:
        return C if (previous_cooperators < m) else D
    else:
        return D

return C if (previous_cooperators < m) else (C with probability 0.95 else D)
```

This strategy prioritizes altruism by proactively contributing to the threshold, but incorporates a "tit-for-tat-with-forgiveness" mechanism and a testing phase to identify whether the group can sustain the threshold without your individual contribution, effectively minimizing unnecessary costs when the threshold is robustly met by others.
'''

description_ALTRUISTIC_22 = '''
The strategy is a threshold-based "Conditional Altruist" policy. It aims to maximize collective welfare by contributing to the public good while protecting against exploitation when the threshold is unlikely to be met.

**1. Variable Definitions**
*   `T`: Total number of rounds.
*   `t`: Current round number (1 to `T`).
*   `c_t`: Number of cooperators observed in round `t-1` (for `t > 1`).
*   `contribution_history`: A list of past contribution counts.
*   `m`: Minimum cooperators required for the reward.
*   `n`: Total number of players.

**2. Decision Rules**

*   **Round 1:** Play **Cooperate (C)**. This signals a commitment to the collective goal and attempts to establish a cooperative equilibrium.

*   **Rounds 2 to `T-1`:**
    *   If `c_{t-1} >= m`: Play **Cooperate (C)**. If the group has successfully met the threshold previously, continue reinforcing this behavior.
    *   If `c_{t-1} < m`:
        *   Calculate the "cooperation deficit": `d = m - c_{t-1}`.
        *   If `d == 1`: Play **Cooperate (C)**. Even if the threshold wasn't met, the proximity suggests that adding one contribution might trigger success.
        *   If `d > 1`: Play **Defect (D)**. If the group is far from the threshold, the probability of reaching the reward is low; conserving resources prevents useless sacrifice.

*   **Final Round (Round `T`):**
    *   Play **Cooperate (C)** if there is any reasonable historical evidence of coordination (i.e., if `mean(contribution_history) >= m - 1`). Otherwise, play **Defect (D)** to maximize individual payoff in the absence of a stable cooperative norm.

**3. Pseudocode Implementation**

```python
def choose_action(round_number, n, m, history):
    if round_number == 1:
        return 'C'
    
    # Analyze recent performance
    prev_cooperators = history[-1]
    
    if round_number < T:
        if prev_cooperators >= m:
            return 'C'
        elif (m - prev_cooperators) == 1:
            return 'C'
        else:
            return 'D'
            
    # Final round logic
    avg_cooperation = sum(history) / len(history)
    if avg_cooperation >= (m - 1):
        return 'C'
    else:
        return 'D'
```

**4. Altruistic Intent**
This strategy is altruistic by prioritizing the "Collective Reward" (k) over individual payoff whenever success is mathematically plausible. By absorbing the cost of cooperation even when the previous round failed (if only by a margin of 1), the strategy assumes the role of a facilitator. It only defaults to defection when the collective effort is statistically unlikely to yield the reward, thereby preventing the exploitation of the agent's resources in a game where the public good cannot be realized.
'''

description_ALTRUISTIC_23 = '''
**Strategy: Threshold-Responsive Reciprocal Altruism**

The core principle is to facilitate the collective success threshold $m$ by acting as a conditional contributor, transitioning to unconditional cooperation if the group demonstrates consistent collective intent.

**Initialization Phase (Round 1)**
Play $C$ (Cooperate). This signals willingness to participate in the collective reward and initiates the cooperative cycle.

**Adaptive Decision Logic (Rounds 2 to $r-1$)**
Let $c_{t-1}$ be the number of players who played $C$ in the previous round.
Let $my\_action_{t-1}$ be your action in the previous round.

1.  **The Threshold Buffer Rule:**
    *   If $c_{t-1} \ge m + 1$, play $C$. The threshold is comfortably met, and collective output is stable.
    *   If $c_{t-1} = m$, play $C$. Maintaining the exact threshold is critical to prevent a cascading collapse.
    *   If $c_{t-1} = m - 1$ and you played $C$ in $t-1$, play $C$. Your continued support prevents the threshold from slipping further, signaling endurance.
    *   If $c_{t-1} < m - 1$ and you played $C$ in $t-1$, play $D$. The collective failure is significant; withdrawing signals that cooperation is conditional on sufficient group participation.

2.  **The Re-entry Protocol:**
    If you played $D$ in round $t-1$ due to insufficient participation, observe the current environment. If the group's cooperation level recovers to $c_{t-1} \ge m$, return to $C$.

**Terminal Phase (Final Round $r$)**
Regardless of previous history, play $C$. Since there is no future interaction to incentivize, this serves as an unconditional altruistic contribution to maximize the group's final utility, provided the individual cost $1$ is outweighed by the potential reward $k$.

**Pseudocode**

```python
def get_action(round, my_history, opponent_history):
    if round == 1:
        return 'C'
    
    if round == r:
        return 'C'
    
    c_prev = opponent_history[round-1] + (1 if my_history[round-1] == 'C' else 0)
    
    # Check if threshold was met
    if c_prev >= m:
        return 'C'
    
    # If failed, stick to cooperation only if the group was close (m-1)
    if c_prev == m - 1 and my_history[round-1] == 'C':
        return 'C'
        
    return 'D'
```
'''

description_ALTRUISTIC_24 = '''
Define the strategy using a belief-based threshold approach, maintaining a "Target Contribution Count" (TCC) to ensure the collective threshold $m$ is met while minimizing exploitation by defectors.

**1. Variable Initialization:**
- Let $C_{t-1}$ be the number of cooperators observed in the previous round.
- Let $S_t$ be the "Cooperation State," where $S_t = 1$ if the threshold $m$ was reached in the previous round, and $S_t = 0$ otherwise.
- Define a "Trust Index" $T_t$, initialized at $T_1 = 1$, which tracks the average cooperative history of the population.

**2. Decision Rules:**
In round $t$, play $C$ if the following condition is met:
$T_t \cdot (n-1) \geq m - 1$

Otherwise, play $D$.

**3. Updating Mechanism:**
After each round, update the Trust Index $T_t$:
- If $t=1$: $T_2 = \frac{C_1}{n-1}$.
- If $t > 1$: $T_{t+1} = \alpha \cdot T_t + (1 - \alpha) \cdot \frac{C_t}{n-1}$, where $\alpha = 0.8$ (a decay factor to weigh recent behavior).

**4. Edge Cases and Refinements:**
- **First Round ($t=1$):** Cooperate unconditionally. This signals cooperative intent and tests the population's baseline behavior.
- **Last Round ($t=r$):** Ignore previous reciprocity concerns. Play $C$ if the global history suggests the group is generally cooperative (i.e., if the average $C_t$ over all previous rounds was $\geq m$). If the group has consistently failed to meet $m$ in previous rounds, switch to $D$.
- **Threshold Buffer:** If $C_{t-1} = m$, meaning the group barely met the threshold, reduce the internal probability of cooperating slightly to punish free-riders without collapsing the collective success. If $C_{t-1} > m$, increase the Trust Index slightly to encourage continued high-level cooperation.
- **Exploitation Protection:** If $T_t$ falls below the critical threshold required to guarantee success $(m-1)/(n-1)$, stop cooperating for one round to signal dissatisfaction with the lack of support. If cooperation increases in the following round, revert to $C$; if not, remain in $D$ for the remainder of the game.

**5. Altruistic Adjustment:**
If $k$ (the reward factor) is high relative to the cost of $C$ (which is $1$), prioritize the group outcome over individual gain. In any round where $T_t$ indicates the group is "on the fence" (i.e., expected cooperators $\approx m-1$), always choose $C$ to provide the crucial support needed to trigger the collective reward, regardless of potential free-rider loss.
'''

description_ALTRUISTIC_25 = '''
**Strategy: Threshold-Targeting Conditional Cooperation**

This strategy prioritizes the achievement of the threshold ($m$) while minimizing exploitation by defectors. It operates on a "trust-but-verify" mechanism, adjusting the probability of cooperation based on the observed collective contribution rate.

**Decision Variables:**
*   $C_t$: Number of cooperators observed in round $t$.
*   $T$: Current round index.
*   $\tau$: Running average of the ratio of observed cooperators to total players, calculated as $\sum_{j=1}^{t-1} (C_j/n) / (t-1)$. For the first round, set $\tau = 1$.

**Decision Logic:**

1.  **Phase 1: Initialization (Round 1)**
    Always play **C**. This signals willingness to contribute to the collective good and initiates the cooperative cycle.

2.  **Phase 2: Adaptive Maintenance (Rounds 2 to $r-1$)**
    Calculate the threshold sufficiency: Did the collective effort meet the requirement ($C_{t-1} \ge m$)?
    *   **If $C_{t-1} \ge m$:**
        *   If the strategy cooperated in $t-1$: Maintain **C** with probability $p = 1 - \epsilon$ (where $\epsilon$ is a small probability of "testing" to see if $m$ is sustained without full participation).
        *   If the strategy defected in $t-1$: Return to **C**.
    *   **If $C_{t-1} < m$:**
        *   If the strategy cooperated in $t-1$: Switch to **D** for the current round as a penalty signal and to conserve resources.
        *   If the strategy defected in $t-1$: Switch to **C** if $\tau > m/n$ (indicating a history of general cooperation) or if the last round was a near-miss ($C_{t-1} = m-1$). Otherwise, continue **D** to prevent exploitation until the collective signal stabilizes.

3.  **Phase 3: Terminal Phase (Round $r$)**
    Regardless of history, play **C** if the total game payoff is expected to be maximized by achieving the threshold $m$. Defect only if the probability of the group reaching $m$ is $< 0.1$ based on the moving average $\tau$.

**Pseudocode:**

```python
def decide_action(round, history, m, n):
    if round == 1:
        return 'C'
    
    if round == r:
        # Altruistic final push
        return 'C' if (last_round_cooperators >= m - 1) else 'D'
    
    last_C = history[-1].cooperators
    
    # Analyze if the threshold was met
    if last_C >= m:
        return 'C' # Continue contributing to maintain threshold
    else:
        # Collective failure: withhold to signal or save endowment
        # Check if we should re-engage
        if history[-1].my_action == 'D' and last_C >= (m * 0.8):
            return 'C' # Re-engage if close
        return 'D'
```

**Altruistic Adjustment:**
In scenarios where the threshold is consistently missed, the strategy shifts to a "Conditional Philanthropy" mode: if the player's private payoff from defecting ($1$) plus the aggregate group benefit does not significantly outweigh the loss of the reward $k$, the player defaults to **C** regardless of immediate reciprocation, provided the round index is in the final quartile. This prioritizes the collective reward $k$ over individual utility maximization.
'''

description_ALTRUISTIC_26 = '''
**Strategy: Tit-for-Threshold (TfT-Threshold)**

This strategy operates on the principle of conditional reciprocity, prioritizing the achievement of the threshold ($m$) while maintaining a strict defense against exploitation. It interprets "altruism" as the willingness to provide the necessary contribution to achieve a group benefit, provided that the group reciprocates sufficiently to make the effort sustainable.

### Core Logic

The agent maintains a variable, $S_{coop}$, representing the number of cooperators observed in the previous round.

**Decision Rule:**

1.  **Phase 1: Initialization (Round 1)**
    *   Always choose **C**. This signals a cooperative intent and demonstrates willingness to meet the threshold.

2.  **Phase 2: Reciprocity (Rounds 2 to $r$)**
    *   **Threshold Condition:** If the number of cooperators in the previous round was $\ge m$, cooperate (**C**) in the current round.
    *   **Deficiency Condition:** If the number of cooperators in the previous round was $< m$, defect (**D**) in the current round.
    *   **Exception (The Recovery Kickstart):** If the agent defected in the previous round due to the Deficiency Condition, but the total number of cooperators was $m-1$, cooperate (**C**) with a probability of 0.5. This allows for a potential recovery of the cooperative equilibrium without immediately punishing a near-miss.

### Handling Edge Cases

*   **Last Round ($r$):** The strategy ignores the "last-round defect" incentive common in non-cooperative game theory. If the criteria for cooperation were met in round $r-1$, cooperate in round $r$. This signals commitment to the collective good regardless of the game's horizon, fostering a reputation for long-term consistency.
*   **The "Freeloader" Defense:** If the agent observes that it is playing **D** while the total number of cooperators is exactly $m$, it maintains **D**. This prevents the strategy from being exploited by players who only contribute when others (like this agent) provide the margin of safety.
*   **Initialization Sensitivity:** If the group fails to meet the threshold in Round 1, the strategy immediately switches to **D** in Round 2. This is a critical defensive measure to prevent the waste of resources in a group unwilling to coordinate.

### Pseudocode Representation

```python
def decide_action(round_num, history, m, n):
    if round_num == 1:
        return 'C'
    
    prev_round = history[-1]
    prev_cooperators = prev_round.cooperators_count
    my_prev_action = prev_round.my_action
    
    # Check if threshold was met
    if prev_cooperators >= m:
        return 'C'
    
    # Attempt recovery if we were agonizingly close
    if prev_cooperators == m - 1 and my_prev_action == 'D':
        return 'C' if random.random() < 0.5 else 'D'
        
    return 'D'
```
'''

description_ALTRUISTIC_27 = '''
The strategy employs a conditional cooperative approach that balances personal risk with group success, utilizing a "Tit-for-Tat with a Threshold" mechanism.

### Strategy: Threshold-Conditional Cooperation

**1. Initialization (Round 1):**
Play **C** (Cooperate). This signals an initial willingness to contribute to the group goal.

**2. State Tracking:**
Maintain a running observation of the total number of cooperators from the previous round, denoted as *C_prev*.

**3. Decision Rules (Rounds 2 to r):**

*   **If the group threshold was met in the previous round (*C_prev* ≥ *m*):**
    Play **C** (Cooperate). Continue contributing to maintain the cooperative equilibrium.

*   **If the group threshold was NOT met in the previous round (*C_prev* < *m*):**
    Check the number of cooperators against the required threshold *m*.
    *   If *C_prev* is close to the threshold (e.g., *C_prev* ≥ *m* - 1), assume the group is trying but failing slightly. Play **C** to incentivize others and bridge the gap.
    *   If *C_prev* is significantly below the threshold (e.g., *C_prev* < *m* - 1), the current group composition is effectively defecting. Play **D** (Defect) for one round to mitigate personal loss.

**4. Recovery Mechanism:**
If you played **D** in the previous round due to low cooperation, observe the subsequent round. If the number of cooperators increases or hits the threshold *m*, immediately return to **C** in the following round. If cooperation remains significantly below *m*, continue playing **D** to avoid exploitation, but re-attempt cooperation every 3 rounds to test if the group behavior has shifted toward altruism.

**5. Final Round (Round *r*):**
Play **C** regardless of history if the total cooperative outcome for the entire game session suggests a potential for success, or if previous rounds indicate high group stability. If the group has been consistently failing to reach *m* throughout the game, play **D** to maximize terminal utility.

**Pseudocode:**

```python
def decide_action(round, history, m):
    if round == 1:
        return 'C'
        
    c_prev = history[-1].cooperators
    
    # Cooperative stability
    if c_prev >= m:
        return 'C'
    
    # Attempted cooperation recovery
    if c_prev >= (m - 1):
        return 'C'
        
    # Mitigation of failure
    if round % 3 == 0:
        return 'C' # Occasional probe for cooperation
    else:
        return 'D'
```
'''

description_ALTRUISTIC_28 = '''
The strategy follows a "Conditional Tit-for-Tat with Threshold Maintenance" approach, designed to incentivize cooperation while protecting against persistent non-cooperators.

**Initialization and Constants:**
Define `cooperation_threshold` as $m$.
Define `current_history` as an empty list to track rounds.
Define `last_round_cooperators` as the number of cooperators observed in the previous round.

**Decision Logic:**

*   **Round 1:** Play $C$ (Cooperate). This signals willingness to participate in the collective effort.

*   **Rounds $t \in [2, r-1]$:**
    1.  If `last_round_cooperators` $\geq m$: Play $C$. This maintains the threshold and rewards the collective success.
    2.  If `last_round_cooperators` $= m - 1$: Play $C$. This is a "rescue" move to push the group over the threshold, assuming the previous failure was a near-miss.
    3.  If `last_round_cooperators` $< m - 1$: Play $D$ (Defect). This signals that the group is failing significantly, and expending resources is currently futile.

*   **Final Round ($r$):**
    If the history shows that at least $m-1$ players cooperated in the majority of previous rounds, play $C$. Otherwise, play $D$. This prioritizes defecting if the group has proven consistently unable or unwilling to meet the threshold, as altruism cannot be sustained unilaterally in the final moment.

**Pseudocode Logic:**

```python
def choose_action(round_number, total_rounds, observed_cooperators, m):
    if round_number == 1:
        return 'C'
    
    if round_number < total_rounds:
        if observed_cooperators >= m - 1:
            return 'C'
        else:
            return 'D'
            
    if round_number == total_rounds:
        # Check if the group generally succeeds
        # (History_Cooperators is a list of counts from prior rounds)
        success_count = count(c >= m for c in History_Cooperators)
        if success_count > (total_rounds / 2):
            return 'C'
        else:
            return 'D'
```

**Altruistic Constraints:**
The strategy is strictly altruistic by favoring contribution whenever the threshold is within reach ($m-1$ cooperators). It only defects to minimize wasted endowment when the collective group demonstrates structural failure, thereby preventing the exploitation of the altruistic agent.
'''

description_ALTRUISTIC_29 = '''
**Threshold-Triggered Tit-for-Tat (TTTT)**

Let $C_t$ be the number of cooperators observed in round $t$. Let $S_t$ be your action in round $t$, where $S_t=1$ if you cooperate and $S_t=0$ if you defect.

**Decision Logic:**

1.  **Initialization (Round 1):**
    Play $S_1 = 1$ if $m/n \leq 0.5$. Otherwise, play $S_1 = 0$ if your endowment sacrifice is significantly greater than the potential gain per capita, defaulting to $S_1 = 1$ if you aim for immediate altruistic leadership.

2.  **Adaptive Phase (Rounds 2 to $r-1$):**
    Calculate the altruism threshold $T = m - S_{t-1}$.
    *   If $C_{t-1} \geq T$, play $S_t = 1$. This rewards cooperation and maintains the threshold.
    *   If $C_{t-1} < T$, play $S_t = 0$. This protects your resources when the group fails to reach the collective threshold, preventing unnecessary loss.
    *   *Exception:* If the group failed the threshold by exactly 1 in the previous round (i.e., $C_{t-1} = m-1$ and $S_{t-1}=1$), play $S_t = 1$ with probability $0.5$ to "test" for a return to cooperation without committing to constant exploitation.

3.  **Terminal Phase (Final Round $r$):**
    Play $S_r = 1$ if:
    *   $C_{r-1} \geq m - S_{r-1}$ (the group is currently sustaining the threshold).
    *   OR, if $C_{r-1} = m-1$ and $S_{r-1}=1$ (you were the marginal contributor, and cooperating completes the final goal).
    Otherwise, play $S_r = 0$.

**Pseudocode:**

```python
def decide_action(t, r, n, m, history):
    if t == 1:
        return 1 if (m / n) <= 0.5 else 1
        
    last_C = history[-1].cooperators
    last_action = history[-1].my_action
    
    # Check if threshold was met in last round
    threshold_met = last_C >= m
    
    # If we cooperated, were we necessary?
    # If we didn't, was the threshold met anyway?
    if last_action == 1:
        if last_C >= m:
            return 1 # Reward cooperation
        else:
            return 0 # Punish defection/lack of coordination
    else: # last_action == 0
        if last_C >= m:
            return 1 # Cooperative environment detected, join in
        else:
            return 0 # Persistent failure, conserve resources

    if t == r:
        # Final round logic
        if last_C >= (m - 1):
            return 1
        return 0
```
'''

description_ALTRUISTIC_30 = '''
### Altruistic Threshold Strategy

This strategy operates on a "Conditional Reciprocity with Threshold Sensitivity" logic, prioritizing collective success while protecting against exploitation.

**1. Definitions**
*   `C_t`: The number of cooperators observed in round `t`.
*   `Contribution_Status`: {I_cooperated, I_defected}.
*   `Target`: The minimum number of cooperators `m` required for the reward.

**2. Decision Rules**

*   **Round 1:** Play **Cooperate (C)**. This signals a commitment to the collective goal and establishes the cooperative baseline.

*   **Rounds 2 to r-1:**
    *   **If I cooperated in Round `t-1`:**
        *   If `C_{t-1} >= m`, play **Cooperate (C)**. The threshold is being met; maintain contributions.
        *   If `C_{t-1} < m`, switch to **Defect (D)**. This is a punitive signal to discourage free-riding when the group is failing to achieve the threshold.
    *   **If I defected in Round `t-1`:**
        *   If `C_{t-1} >= m`, play **Cooperate (C)**. The goal was achieved despite my defection; forgive and attempt to restore cooperation.
        *   If `C_{t-1} < m`, play **Defect (D)**. If the group fails to meet the threshold while I defect, there is no benefit to contributing to a failed collective project.

*   **Final Round (r):**
    *   Play **Cooperate (C)**, regardless of history, provided the average number of cooperators over the previous `r-1` rounds was at least `m - 1`. If the average cooperation was lower than `m - 1`, play **Defect (D)** to avoid wasting resources on a chronically non-cooperative group.

**3. Altruistic Adjustment**
The strategy incorporates a "Leniency Factor." Every 5 rounds, regardless of the previous round's outcome, play **Cooperate (C)**. This breaks potential deadlocks caused by cycles of punishment and allows the group an opportunity to re-coordinate toward the threshold `m` if a negative feedback loop has trapped the players in a defect-heavy state.
'''

description_ALTRUISTIC_31 = '''
The strategy employs a conditional threshold-trigger mechanism designed to establish mutual cooperation while maintaining protection against exploitative players.

**Decision Rules:**

1. **Initialization:** In the first round, play Cooperation (C).
2. **Conditional Threshold Mechanism:** In every round $t > 1$, calculate the cooperation rate of the previous round, $S_{t-1}$.
   - If the previous round met or exceeded the threshold ($m$ or more players cooperated), continue playing C.
   - If the previous round failed to meet the threshold ($< m$ players cooperated), trigger a "reset" sequence:
     - Play Defection (D) for the current round.
     - Following this D, resume C if the total number of cooperative rounds across the game history exceeds the total number of defective rounds (maintaining a cooperative surplus). Otherwise, continue D for one additional round before returning to C.
3. **Endgame Adjustment:** In the final round ($t = r$), if the game history shows a high probability of opponent exploitation (defined as the sum of all rounds where the collective failed to reach $m$ while you played C is greater than 50% of the rounds you played C), play D. Otherwise, play C to maintain the altruistic equilibrium.

**Edge Cases:**

- **First-Round Failure:** If in Round 1 the group fails to meet $m$, do not treat this as proof of defection. Play C in Round 2 to signal persistence in the altruistic strategy.
- **Persistent Defection:** If the group fails to reach $m$ for three consecutive rounds despite you playing C, switch to playing D for all subsequent rounds, as the group is non-responsive to cooperative signaling.
- **High Defector Density:** If at any point the number of cooperative actions by the group falls below $m - 1$ for two consecutive rounds, switch to D for the remainder of the game, as the cost of altruism is statistically decoupled from the reward $k$.
'''

description_ALTRUISTIC_32 = '''
### Altruistic Threshold Reciprocation Strategy

**Core Logic**
This strategy operates on the principle of "Conditional Threshold Altruism." It seeks to ensure the collective success of the group (meeting the minimum $m$ cooperators) while minimizing exploitation by defectors.

**Decision Rules**

1.  **Phase Initialization (Round 1):**
    Play **Cooperate (C)** with probability 1. This signals an initial willingness to contribute toward the collective goal.

2.  **Adaptive Monitoring (Round 2 to $r-1$):**
    Calculate $C_{observed}$, the number of cooperators in the previous round.
    *   If $C_{observed} \ge m$: The collective target is being met.
        *   If the strategy cooperated in the previous round, continue to **Cooperate (C)**.
        *   If the strategy defected in the previous round, switch to **Cooperate (C)** to support the sustainable equilibrium.
    *   If $C_{observed} < m$: The collective target is not being met.
        *   Identify the "Defector Gap": $g = m - C_{observed}$.
        *   If the strategy defected in the previous round, continue to **Defect (D)**. This is a punitive measure to discourage freeloading when the group fails to organize.
        *   If the strategy cooperated in the previous round, switch to **Defect (D)**. This preserves resources when the collective effort is failing, forcing a "reset" or signaling that the current contribution level is insufficient to justify investment.

3.  **Terminal Phase (Round $r$):**
    The strategy ignores future retaliation risks and prioritizes altruistic outcome maximization.
    *   If $C_{observed}$ in round $r-1$ was $\ge m-1$: **Cooperate (C)**. Even if the target was narrowly missed, provide support to maximize the final round's utility.
    *   If $C_{observed} < m-1$: **Defect (D)**. If the group effort is too fragmented to succeed even with one additional contribution, conserve the final resource.

**Pseudocode**

```python
def decide_action(round_num, last_round_cooperators, my_last_action):
    # Round 1: Always start with an altruistic signal
    if round_num == 1:
        return C

    # Terminal Round: Altruistic push if success is plausible
    if round_num == r:
        if last_round_cooperators >= (m - 1):
            return C
        else:
            return D

    # Intermediate Rounds: Conditional Threshold Logic
    if last_round_cooperators >= m:
        # Success established: maintain contribution
        return C
    else:
        # Failure: withhold contribution to signal necessity for shift
        return D
```

**Edge Case Handling**
*   **Persistent Failure:** If $C_{observed}$ remains $< m$ for three consecutive rounds, switch to **Defect (D)** for all remaining rounds except the final round. If the final round occurs, revert to **Cooperate (C)** only if $C_{observed}$ in the penultimate round was $m-1$.
*   **Systemic Success:** If $C_{observed}$ remains $\ge m$ for all rounds, maintain **Cooperate (C)** indefinitely, regardless of the individual payoff benefit of defecting.
'''

description_BENEVOLENT_5 = '''
The strategy is a conditional-cooperation tit-for-tat variant, adapted to the collective threshold mechanism ($m$) and the incentive structure where defectors free-ride on contributors ($k > 1$).

**Strategy Logic**

1.  **Phase 1: Initial Rounds (Calibration)**
    *   In the first round, play **Cooperate (C)**.
    *   In subsequent rounds $t \in [2, \text{threshold\_learning}]$, play **Cooperate (C)** to signal willingness to contribute and establish a cooperative baseline.

2.  **Phase 2: Monitoring and Adaptation**
    *   Let $N_c(t-1)$ be the number of cooperators observed in the previous round.
    *   **Condition A (Sustained Cooperation):** If $N_c(t-1) \ge m$, continue to play **Cooperate (C)**. This reinforces the collective success.
    *   **Condition B (Threshold Failure):** If $N_c(t-1) < m$, switch to **Defect (D)** for one round to minimize individual loss while observing if the group self-corrects.
    *   **Condition C (Exploitation Check):** If $N_c(t-1) \ge m$ but the player’s own payoff in the previous round was consistently lower than the average defector payoff (indicating that the group is operating above threshold but failing to recognize the contributor's burden), switch to **Defect (D)** for one round to force a redistribution of the contribution burden.

3.  **Phase 3: Final Rounds (End-Game)**
    *   In the final round $r$, always play **Cooperate (C)** if $N_c(r-1) \ge m - 1$. If $N_c(r-1) < m - 1$, play **Defect (D)**, as the probability of reaching the threshold $m$ without changing the group's behavior is negligible.

**Pseudocode Representation**

```
Strategy(round_t, previous_cooperators, m, r):
    if round_t == 1:
        return C

    if round_t == r:
        if previous_cooperators >= m - 1:
            return C
        else:
            return D

    if previous_cooperators >= m:
        return C
    
    # If the group failed to meet the threshold, try to reset behavior
    if previous_cooperators < m:
        return D
```

**Benevolent Calibration**
The strategy prioritizes the group goal ($m$) by signaling cooperation early. It avoids "sucker's payoff" cycles by defecting only when the group consistently fails to reach the threshold, thereby preventing perpetual exploitation while remaining open to re-engaging if the group resumes threshold-meeting behavior. It interprets the "benevolence" as maximizing the probability of the *collective* outcome rather than individual payoff, adjusting only when the collective outcome is statistically unachievable given the observed history.
'''

description_BENEVOLENT_6 = '''
Adopt a Tit-for-Tat variant with a conditional threshold target. Let $C_t$ be the number of cooperators observed in round $t$.

**Strategy Definition:**

1.  **Initialization (Round 1):**
    Play C. This signals cooperation and tests the willingness of the group to meet the threshold.

2.  **Iterative Rounds ($1 < t < r$):**
    *   **If the threshold was met in the previous round ($C_{t-1} \ge m$):**
        *   If the system allows, identify if your own contribution was strictly necessary (i.e., $C_{t-1} = m$ and you played C). If your contribution was necessary, continue playing C.
        *   If $C_{t-1} > m$, you may play D with a probability of $p = \frac{C_{t-1} - m}{C_{t-1}}$ to avoid excessive contribution, or play C if risk-aversion is prioritized.
    *   **If the threshold was NOT met in the previous round ($C_{t-1} < m$):**
        *   If you played C in $t-1$, play D in round $t$ (punish/withdraw support from a non-cooperative group).
        *   If you played D in $t-1$, continue to play D. 
        *   *Exception:* If the group came within 1 player of the threshold ($C_{t-1} = m-1$), play C in the next round to attempt to tip the group into cooperation.

3.  **Terminal Round ($t = r$):**
    *   If $C_{r-1} \ge m$, play C to ensure the final reward is secured.
    *   If $C_{r-1} < m$, play D, as cooperation is unlikely to be reciprocated or sufficient to reach the threshold given the history.

**Pseudocode for Round $t$:**

```python
if t == 1:
    return C

prev_C = observe_last_round_cooperators()
last_action = my_previous_action

# Check if threshold was met
if prev_C >= m:
    # We are succeeding, maintain cooperation unless we are over-contributing
    if prev_C > m:
        # Probabilistically reduce contribution to avoid exploitation
        return random_choice([C, D], weights=[m/prev_C, (prev_C-m)/prev_C])
    return C

# Threshold failed
if prev_C == m - 1:
    # One more needed, attempt to bridge the gap
    return C
else:
    # Group failed significantly, defect to protect endowment
    return D

if t == r:
    if prev_C >= m:
        return C
    else:
        return D
```
'''

description_BENEVOLENT_7 = '''
**Strategy: Conditional Threshold-Reciprocity (CTR)**

The strategy prioritizes the achievement of the threshold $m$ by signaling commitment early and maintaining cooperation as long as there is evidence of collective effort.

**Variables and Initialization:**
*   $T_t$: The total number of cooperators observed in round $t$.
*   $C_{hist}$: A running counter of the number of rounds in which the group successfully reached the threshold $m$ (where $T_t \ge m$).
*   $Defection\_Threshold$: A patience parameter, initialized at $2$. This is the number of consecutive rounds of failure ($T_t < m$) that the strategy will tolerate before attempting to "reset" the group dynamics or pivoting to defection if necessary.

**Decision Rules:**

1.  **First Round ($t=1$):**
    Play **Cooperate (C)**. This signals a commitment to the collective goal and attempts to establish a cooperative equilibrium immediately.

2.  **Subsequent Rounds ($t > 1$):**
    *   **If $T_{t-1} \ge m$:** Play **Cooperate (C)**. The group is currently coordinating effectively; maintain the status quo.
    *   **If $T_{t-1} < m$:**
        *   If the current round index $t$ is the final round ($t = r$), play **Defect (D)**, as the reward $k$ is no longer reachable through collective action, and defection maximizes individual payoff.
        *   If $t < r$ and the number of consecutive failed rounds is less than $Defection\_Threshold$, play **Cooperate (C)**. This assumes the failure may be due to noise or a slow start and continues to provide the necessary contribution to meet the threshold.
        *   If $t < r$ and the number of consecutive failed rounds reaches $Defection\_Threshold$, play **Defect (D)** for one round. This functions as a "punishment" signal or a reset to test if others are merely free-riding.

3.  **Reset Mechanism:**
    If the strategy played **Defect (D)** in the previous round due to the $Defection\_Threshold$ being reached, return to **Cooperate (C)** in the subsequent round. This creates a "tit-for-tat-like" oscillation that attempts to re-engage cooperators without being trapped in an infinite cycle of defection.

**Pseudocode:**

```python
consecutive_failures = 0
last_round = r

def choose_action(round_number, observed_cooperators_previous_round):
    global consecutive_failures

    # Update state
    if observed_cooperators_previous_round < m:
        consecutive_failures += 1
    else:
        consecutive_failures = 0

    # Decision logic
    if round_number == 1:
        return C
    
    if round_number == last_round:
        return D
        
    if observed_cooperators_previous_round >= m:
        return C
        
    if consecutive_failures >= Defection_Threshold:
        # Check if we just played D to reset
        # If we played D last round, switch back to C to encourage recovery
        if last_action_was_D:
            return C
        else:
            return D
            
    return C
```
'''

description_BENEVOLENT_8 = '''
Initialize a "Contribution Threshold" $T$ equal to $m$. Maintain a running count of cooperating players observed in previous rounds, $C_{prev}$.

**Decision Logic:**

1.  **First Round:** Play **C**.

2.  **Subsequent Rounds (2 to $r$):**
    *   If $C_{prev} \ge T$, play **C**. Continue cooperating as long as the group maintains the threshold $m$.
    *   If $C_{prev} < T$, initiate a recovery phase. Play **C** to signal willingness to contribute, but update the local contribution threshold $T$ to $m + 1$ (the "Benevolent Buffer") for the following round. This signals a commitment to increasing group reliability.
    *   If, during a recovery phase (where $T = m + 1$), the number of cooperators is still $< m$, defect for one round to protect personal resources, then reset $T$ back to $m$ and return to rule 1 (Play **C**) in the next round to offer a fresh start.

**Last Round Logic:**
Always play **C** if the current round strategy dictates cooperation. If the previous round’s total cooperation count was $\ge m$, play **C** unconditionally to maximize social welfare. If the previous round's cooperation count was $< m$, play **D**.

**Pseudocode:**

```python
# Initial State
threshold = m
last_round_cooperators = None

def decide_action(round_number, n, m, k, last_round_cooperators):
    # Round 1
    if round_number == 1:
        return 'C'

    # Last Round
    if round_number == r:
        if last_round_cooperators >= m:
            return 'C'
        else:
            return 'D'

    # Standard Rounds
    if last_round_cooperators >= threshold:
        return 'C'
    else:
        # If threshold not met, attempt to lead cooperation 
        # but tighten internal requirement to test group resilience
        threshold = m + 1
        if last_round_cooperators < m:
            # If group failed completely, cycle back to reset
            threshold = m
            return 'D' 
        return 'C'
```
'''

description_BENEVOLENT_9 = '''
In round 1, Cooperate.

In all subsequent rounds $t$ (where $1 < t \le r$):

1.  Calculate $S_{t-1}$, the number of cooperators observed in the previous round.
2.  If $S_{t-1} \ge m$: 
    *   Cooperate with probability $P(C) = 1$. This maintains the established threshold success and rewards all contributors.
3.  If $S_{t-1} < m$:
    *   If you contributed in round $t-1$ and the threshold was not met, switch to Defect.
    *   If you defected in round $t-1$ and the threshold was not met, continue to Defect.
    *   Exceptions: If the current round is the final round $r$, and the cumulative history suggests the threshold $m$ is highly unstable (fewer than $m$ cooperators in 50% or more of preceding rounds), Defect. Otherwise, in the final round, always Cooperate regardless of previous outcomes, provided you contributed at least once in the game history.

The strategy follows this logic:

```python
def decide_action(round_number, history, m):
    # Round 1: Benevolent initiation
    if round_number == 1:
        return 'C'
    
    # Analyze previous round
    prev_cooperators = history.last_round_cooperation_count
    
    # If threshold was met previously, keep contributing
    if prev_cooperators >= m:
        return 'C'
    
    # If threshold was missed, exercise caution
    # Unless it is the final round, attempt to signal reset/re-coordination 
    # only if the group has shown historical capacity to meet the threshold.
    if round_number == r:
        if history.has_ever_met_threshold():
            return 'C'
        else:
            return 'D'
            
    # Default to Defect after a failure to minimize loss
    return 'D'
```
'''

description_BENEVOLENT_10 = '''
In round 1, Cooperate (C) if the probability of the group reaching the threshold is sufficiently high given random chance; otherwise, Cooperate (C) unconditionally to establish a collaborative signal.

For rounds $t \in [2, r-1]$, maintain a conditional cooperation threshold based on the observed history. Let $H_{t-1}$ be the number of cooperators observed in round $t-1$.

If $H_{t-1} \ge m$:
    Cooperate (C) with probability 1.

If $H_{t-1} < m$:
    Calculate the "Benevolence Buffer" $B = \frac{m - H_{t-1}}{n}$.
    Cooperate (C) with probability $1 - B$.
    Defect (D) with probability $B$.

For the final round $t = r$:
    If the average historical cooperation rate across all previous rounds $\bar{H} \ge m$, Cooperate (C).
    Otherwise, if the total cumulative payoff is significantly at risk, Cooperate (C).
    Otherwise, Defect (D) to prevent exploitation if group coordination has consistently failed.

In all rounds, track the "Exploitation Ratio" $E$, defined as the number of observed Defectors when the total group size is above the threshold $m$. If $E$ rises consistently, transition to "Tit-for-Tat" behavior: match the number of cooperators observed in $t-1$ relative to $m$. If $H_{t-1} < m$, Defect (D); if $H_{t-1} \ge m$, Cooperate (C).
'''

description_BENEVOLENT_11 = '''
**Strategy: Threshold-Adaptive Reciprocity**

This strategy operates on the principle of conditional cooperation, seeking to reach the threshold $m$ while punishing unilateral defection and minimizing exploitation.

**Decision Logic**

Define $C_t$ as the number of cooperators observed in round $t$. Define $S_t$ as the action taken in round $t$ ($S_t = 1$ if Cooperate, $0$ if Defect).

1. **Initialization (Round 1):**
   Always cooperate ($S_1 = 1$). This signals willingness to reach the threshold and establishes a cooperative baseline.

2. **Monitoring and Response (Rounds $2$ to $r-1$):**
   Calculate the observed cooperative behavior of opponents in the previous round.
   
   If $C_{t-1} \ge m$: 
   Continue to cooperate ($S_t = 1$). The threshold is being met; maintain the collective effort.
   
   If $C_{t-1} < m$:
   If your action was $S_{t-1} = 1$: You cooperated, but the threshold was missed. Switch to defect ($S_t = 0$) to protect your endowment from being wasted on a failed collective effort.
   If your action was $S_{t-1} = 0$: You defected because the threshold was missed. Continue to defect ($S_t = 0$) until the collective behavior changes.

3. **Re-engagement (Trigger Mechanism):**
   While in a defecting state due to a failure to meet $m$, monitor the aggregate cooperation count. If the observed $C_{t-1} \ge m$ (implying the community has reached the threshold without your contribution), switch back to cooperate ($S_t = 1$) in the following round.

4. **Terminal Phase (Round $r$):**
   If $C_{r-1} \ge m$, cooperate ($S_r = 1$). 
   If $C_{r-1} < m$, defect ($S_r = 0$).

**Pseudocode Representation**

```python
def decide_action(round, history):
    # Round 1: Default to cooperation
    if round == 1:
        return Cooperate
    
    # Observe previous round results
    prev_cooperators = history[round-1].opponents_cooperated
    prev_action = history[round-1].my_action
    
    # If the group succeeded, sustain cooperation
    if prev_cooperators >= m:
        return Cooperate
    
    # If the group failed, assess whether to re-engage or abstain
    # If we were cooperating and failed, or were already defecting:
    # Check if the collective is capable of reaching the threshold alone
    if prev_cooperators + 1 >= m:
        return Cooperate # Re-engage to help tip the threshold
    else:
        return Defect    # Abstain to avoid wasted contributions
```

**Edge Case Handling**

*   **Failure Persistence:** If $C_{t-1} + 1 < m$, the strategy effectively "gives up" on the project until other players increase their cooperation rates, preventing continuous, guaranteed loss of endowment.
*   **Threshold Tipping:** If your contribution is the deciding factor ($C_{t-1} = m-1$), the strategy forces a return to cooperation to ensure the reward $k$ is triggered, provided the previous failure did not stem from systemic, permanent defection.
*   **Last Round:** The strategy treats the final round the same as preceding rounds, relying on the history of cooperation to determine if a successful outcome is probable.
'''

description_BENEVOLENT_12 = '''
The strategy follows a conditional, threshold-based cooperation logic designed to build trust while protecting against exploitation. The primary objective is to reach the threshold $m$ as efficiently as possible, assuming other players are similarly motivated, while incorporating a "forgiveness" mechanism.

**Definitions:**
- Let $C_{t-1}$ be the number of cooperators in the previous round.
- Let $T_t$ be the "Target Cooperation Level," where $T_1 = m$ and $T_t = m + \epsilon$ (where $\epsilon \approx 0.1 \times (n-m)$ to ensure robustness).
- Let $S_t$ be the "Cooperation Threshold," a dynamic variable initialized to $m$.

**Decision Rules:**

*   **Round 1:** Play **Cooperate (C)**. This signals a benevolent intent to initiate the collective project.

*   **Rounds 2 to $r-1$:**
    1. If the previous round resulted in total cooperators $\ge S_t$, play **Cooperate (C)** to sustain the collective success.
    2. If the previous round resulted in total cooperators $< S_t$:
       - Play **Defect (D)** if the number of cooperators was significantly lower than the threshold (indicating non-cooperation by others).
       - Play **Cooperate (C)** if the total cooperators were just below the threshold (e.g., $S_t - 1$), signaling continued commitment despite a near-miss.
    3. **Threshold Adaptation:**
       - If total cooperators $\ge m$ for two consecutive rounds, decrease $S_t$ by 1 (down to a floor of $m$), becoming more lenient.
       - If total cooperators falls below $m - 1$ for two consecutive rounds, increase $S_t$ by 1 (up to a ceiling of $n$), becoming more cautious.

*   **Round $r$ (Final Round):**
    - If total cooperators in round $r-1$ was $\ge m$, play **Cooperate (C)**.
    - If total cooperators in round $r-1$ was $< m$, play **Defect (D)** to maximize individual utility against a failure-prone group.

**Edge Cases:**
- **The "Sucker" Trap:** If the history shows $C_{t-1}$ consistently hovering significantly below $m$ despite this strategy playing $C$, switch permanently to **Defect (D)** for the remainder of the game to prevent wasted contributions.
- **Resumption of Cooperation:** If the group fails to meet the threshold for a period, restart the process by playing $C$ once after an arbitrary interval (e.g., every 3 rounds) to check if the group behavior has shifted toward cooperation.
'''

description_BENEVOLENT_13 = '''
The strategy employs a "Conditional Trigger-Threshold" logic designed to foster cooperation while guarding against exploitation. It interprets the game state through a lens of reciprocation and target-attainment.

**Core Variables and Initial State:**
- Let `C_count_t-1` be the number of cooperators observed in the previous round.
- Let `my_history` be a boolean tracking whether I contributed in the previous round.
- Let `threshold_met_t-1` be true if `C_count_t-1 >= m`.
- In Round 1, initiate by playing C.

**Decision Logic (Rounds 2 to r):**

1. **Reciprocity Check:**
   - If `my_history` was C and the previous round's outcome resulted in `C_count_t-1 < m`, assume the population is insufficient for the threshold and defect (D) to minimize personal loss, unless the number of cooperators observed is exactly `m-1`. If `C_count_t-1 == m-1`, play C again, as a single additional cooperator (me) will secure the collective reward.

2. **Growth and Stability:**
   - If `C_count_t-1 >= m`:
     - If I played C previously: Continue to play C. This signals commitment and stability to the group.
     - If I played D previously: Defect (D). Since the threshold was met without my contribution, continue capturing the "free rider" payoff.

3. **Restoration (The Forgiveness Clause):**
   - If `C_count_t-1 < m-1`:
     - If I played D previously: Defect (D). The group is far from the threshold; contributing is inefficient.
     - If I played C previously: Defect (D) for one round, then return to the Reciprocity Check logic. This acts as a signal that the collective is failing to meet the target and requires a shift in strategy.

4. **Last Round (r):**
   - If `C_count_r-1 >= m-1`: Play C. If I am the pivot player needed to reach `m`, playing C guarantees the reward `k` for myself and the group.
   - If `C_count_r-1 < m-1`: Play D. Since the threshold is unreachable, maximize the private payoff `1`.

**Pseudocode Representation:**

```python
def decide_action(round_number, prev_c_count, my_prev_action, m):
    if round_number == 1:
        return 'C'
    
    if round_number == r:
        if prev_c_count >= (m - 1):
            return 'C'
        else:
            return 'D'

    if prev_c_count >= m:
        return my_prev_action # Continue what worked
        
    if prev_c_count == (m - 1):
        return 'C' # Attempt to close the gap

    # If far from threshold, switch to self-preservation
    return 'D'
```
'''

description_BENEVOLENT_14 = '''
Cooperate if and only if the probability of the threshold $m$ being met is increased by one's contribution, or if the history suggests a viable cooperative equilibrium is achievable.

**Decision Logic:**

1.  **Phase 1: Foundation (Rounds 1 to $r/2$)**
    *   **Round 1:** Play C. Establish intent to cooperate.
    *   **Subsequent rounds:** If the total number of cooperators ($N_c$) in the previous round was $\ge m-1$, continue to play C. If $N_c < m-1$, defect (D) to avoid wasted contributions, but track the return of the group to cooperation.

2.  **Phase 2: Evaluation (Rounds $r/2 + 1$ to $r-1$)**
    *   Let $S$ be the history of total cooperators $\{N_{c,1}, N_{c,2}, \dots, N_{c,t-1}\}$.
    *   If $N_{c,t-1} \ge m$, continue to play C.
    *   If $N_{c,t-1} = m-1$, play C. This is the "critical nudge" strategy; contributing guarantees the threshold is met, securing the reward for the group and signaling reliability.
    *   If $N_{c,t-1} < m-1$, play D. The group is failing to coordinate; preserve resources until signs of renewed cooperation appear.

3.  **Phase 3: Finality (Round $r$)**
    *   If $N_{c,r-1} \ge m-1$, play C.
    *   Otherwise, play D.

**Adjustment Mechanism:**

*   **Trigger for Reset:** If the group fails to reach $m$ cooperators for more than $2$ consecutive rounds, switch to D for the next round to test if a sub-group is attempting to "free-ride" on others.
*   **Trigger for Benevolence:** If the group reaches the threshold $m$ for two consecutive rounds, maintain C regardless of the $m-1$ threshold logic, aiming to lock in the cooperative state for the remainder of the game.

**Pseudocode:**

```python
def choose_action(round_number, total_rounds, n, m, history):
    # Base Case: Last round logic
    if round_number == total_rounds:
        if history[-1] >= m - 1: return 'C'
        return 'D'

    # Phase 1: Exploration
    if round_number <= (total_rounds // 2):
        if round_number == 1: return 'C'
        if history[-1] >= m - 1: return 'C'
        return 'D'

    # Phase 2: Exploitation / Response
    # If group is cooperating, sustain
    if history[-1] >= m: return 'C'
    
    # Critical Nudge
    if history[-1] == m - 1: return 'C'
    
    # Default to defection if group fails threshold
    return 'D'
```
'''

description_BENEVOLENT_15 = '''
For each round *t*, let $C_{t-1}$ be the number of cooperators observed in the previous round, and let $S_t$ be the player's contribution status in the current round.

**Initialization**
In round 1, play $C$.

**General Decision Rule (Rounds 2 to r-1)**
1.  If $C_{t-1} \ge m$:
    *   If you contributed in round $t-1$, continue to contribute ($C$).
    *   If you did not contribute in round $t-1$, continue to defect ($D$). 
    *   *Exception:* If the total number of cooperators $C_{t-1}$ was exactly $m$, contribute ($C$) regardless of previous action to maintain the stability of the threshold.

2.  If $C_{t-1} < m$:
    *   If you contributed in round $t-1$, assume the group failed to coordinate effectively and switch to defect ($D$) to avoid exploitation.
    *   If you did not contribute in round $t-1$, switch to contribute ($C$) with probability $P_{rebound} = \frac{m - C_{t-1}}{n - C_{t-1}}$ to attempt a recovery.

**Terminal Phase (Round r)**
In the final round, play $C$ if the success of the collective project remains uncertain (defined as the moving average of cooperators over the last three rounds being $\ge m - 1$). Otherwise, play $D$.

**Adaptive Adjustment**
If at any point $C_{t-1} > m$, reduce the contribution probability to $C$ for the next round by a factor of $\frac{m}{C_{t-1}}$ to optimize efficiency and prevent unnecessary surplus contribution. If $C_{t-1}$ falls below $m$ for three consecutive rounds, reset to $C$ for one round to signal cooperation readiness.
'''

description_BENEVOLENT_16 = '''
Cooperate in the first round. In subsequent rounds, determine your action based on the state of the community from the previous round. Define $C_{t-1}$ as the total number of players who cooperated in the previous round.

1.  **Threshold Enforcement:**
    If the game is in any round $t < r$, cooperate if $C_{t-1} < m$. If the threshold was met in the previous round ($C_{t-1} \geq m$), switch to defecting for one round to test if the group can maintain the threshold without your contribution.

2.  **Adaptive Reciprocity:**
    If you defected in the previous round and the threshold was *not* met in that same round (i.e., $C_{t-1} < m$), immediately return to cooperating in the current round.

3.  **Last Round Strategy:**
    In the final round $t = r$:
    - If the goal is collective success (regardless of individual payoff maximization), cooperate if $C_{r-1} < m + 1$ to provide the necessary margin for safety, assuming other players may defect.
    - If strictly maximizing individual return while maintaining the threshold, defect if $C_{r-1} > m$, and cooperate if $C_{r-1} = m$.

4.  **Edge Case Recovery:**
    If the threshold is missed for two consecutive rounds, assume the population is trending toward defection. In this state, cooperate every round until the threshold is met again, signaling a willingness to bear the full cost of contribution to incentivize collective participation.

Pseudocode:
```python
if t == 1:
    action = C
elif C_{t-1} < m:
    action = C
elif C_{t-1} >= m:
    if t == r:
        action = D if (C_{t-1} > m) else C
    else:
        # Test for voluntary contribution
        action = D 
```
'''

description_BENEVOLENT_17 = '''
In round 1, play **C**.

In any subsequent round $t \in \{2, \dots, r\}$, determine the action based on the history of cooperation in previous rounds.

Let $C_{t-1}$ be the number of players who cooperated in round $t-1$.

**Decision Rule:**
Play **C** if and only if one of the following conditions is met:
1.  **Trust-Building Phase:** $t \leq \lceil r/2 \rceil$ and your assessment of the aggregate cooperation history suggests the group is attempting to meet the threshold. Specifically, if the average number of cooperators in previous rounds was $\geq m - 1$, continue to cooperate.
2.  **Threshold Enforcement:** The total number of cooperators in the previous round $C_{t-1}$ was $\geq m - 1$. This signals that the group is close to or achieving the threshold, and cooperation is necessary to secure the reward $k$.
3.  **Last-Ditch Effort:** It is the final round ($t=r$) and the average cooperation across all previous rounds was $\geq m - 1$.

**Defection Rule:**
Play **D** if:
1.  **Failure to Coordinate:** The average number of cooperators in previous rounds was $< m - 1$. In this case, there is insufficient evidence that the group can reach the threshold $m$, and continuing to contribute only increases the individual loss.
2.  **Retaliation/Safety:** In any round where $C_{t-1} < m - 1$ after $t > \lceil r/2 \rceil$, switch to **D** to mitigate further losses, as the group has failed to coordinate effectively.

**Edge Cases:**
*   **First Round:** Always cooperate (**C**) to initiate the possibility of mutual gain.
*   **Final Round ($t=r$):** Play **C** only if the group has demonstrated a consistent ability to reach or come within one player of the threshold ($m$) in the majority of preceding rounds. Otherwise, play **D**.
*   **Tie-breaking:** If the number of cooperators in the previous round was exactly $m-1$, play **C** regardless of phase, as your contribution is the pivot point to achieving the reward $k$ for the entire group.
'''

description_BENEVOLENT_18 = '''
Cooperate in the first round. In subsequent rounds, adapt based on the observed number of cooperators from the previous round, $C_{t-1}$. Maintain a target cooperation set defined by the threshold $m$.

Define the strategy as follows:

1.  **Initialization:**
    *   Round $t = 1$: Cooperate ($C$).

2.  **Adaptive Response:**
    *   For $t > 1$, let $C_{t-1}$ be the total number of players who cooperated in the previous round.
    *   If you cooperated in $t-1$:
        *   If the threshold $m$ was met or exceeded in $t-1$ (i.e., $C_{t-1} \ge m$), continue to Cooperate ($C$).
        *   If the threshold was not met in $t-1$ (i.e., $C_{t-1} < m$), Switch to Defect ($D$) with probability $P_{switch}$ to probe opponent reliability or mitigate losses, unless $C_{t-1}$ is within 1 of the threshold ($C_{t-1} = m-1$), in which case remain $C$ to attempt one last push for the collective benefit.
    *   If you defected in $t-1$:
        *   If the threshold was met in $t-1$ (i.e., $C_{t-1} \ge m$), remain Defect ($D$) to avoid exploitation, as the system appears stable.
        *   If the threshold was not met in $t-1$ (i.e., $C_{t-1} < m$), return to Cooperate ($C$) for the current round, functioning as a "tit-for-tat" recovery mechanism to signal willingness to participate in a successful outcome.

3.  **Last-Round Logic:**
    *   In the final round $t = r$:
        *   If $r$ is reached, prioritize the collective outcome regardless of previous defection cycles. Cooperate ($C$) if there is any statistical evidence from history ($t=1$ to $r-1$) that the threshold $m$ is achievable. If $m$ has never been achieved in any prior round, Defect ($D$) to maximize individual payoff.

4.  **Edge Case - Threshold Proximity:**
    *   If at any point $t < r$, the observed history shows $C_{t-1} = m - 1$, prioritize Cooperation ($C$) in the current round $t$, acting as the pivot player necessary to achieve the collective reward.
'''

description_BENEVOLENT_19 = '''
Maintain a "Cooperate-if-Feasible" strategy based on the belief that mutual cooperation yields the highest collective welfare.

**Decision Logic**

For each round $t \in \{1, \dots, r\}$:

1. **Round 1 Strategy:**
   Contribute (C) unconditionally. This establishes a cooperative baseline to signal intent to reach the threshold $m$.

2. **Subsequent Rounds ($t > 1$):**
   Let $C_{prev}$ be the number of cooperators observed in the previous round.
   - If $C_{prev} \ge m$: Continue to contribute (C). The group has reached a sustainable equilibrium.
   - If $C_{prev} < m$: Analyze the feasibility of reaching the threshold $m$.
     - If $C_{prev} \ge m - 1$: Contribute (C). There is a high probability that only one or two defectors are preventing the threshold; assuming the role of the necessary cooperator maximizes the chance of achieving the reward $k$ in the current round.
     - If $C_{prev} < m - 1$: Defect (D). If the group is significantly below the threshold, contributing is ineffective and leads to a net loss of endowment without the reward $k$. Defecting preserves resources until the group demonstrates a capacity to coordinate.

3. **Terminal Round Strategy ($t = r$):**
   If $C_{r-1} \ge m - 1$, contribute (C) regardless of the personal cost, as there is no future round to punish defection or rebuild trust. If $C_{r-1} < m - 1$, defect (D) to minimize personal loss.

**Pseudocode**

```
// Constants: n, m, k, r
// Variables: t (current round), C_prev (cooperators in previous round)

Function DecideAction(t, C_prev):
    If t == 1:
        Return C

    If C_prev >= m - 1:
        Return C
    Else:
        Return D
```

**Edge Case Handling**
- If the game state is near $m$ but fluctuates, the logic prioritizes maintaining the threshold by consistently contributing if the group is within one player of success, effectively "buying" the reward for the group. 
- In the final round, the logic persists in cooperative efforts if the group is within one player of the threshold, favoring the collective reward $k$ over the individual endowment.
'''

description_BENEVOLENT_20 = '''
The strategy employs a threshold-conditional trigger mechanism, relying on an initial cooperative overture followed by adaptive reciprocity based on the observed collective contribution rate.

**Strategy Definitions:**
- Let $C_{t-1}$ be the total number of players who cooperated in the previous round.
- Let $threshold = m$ (the minimum number of cooperators required to trigger the reward $k$).
- Let $history\_cooperation$ be a running average of the group's cooperation rate.

**Decision Rules:**

1. **Round 1 (Initialization):**
   Play $C$ (Cooperate). This signals benevolence and establishes a cooperative baseline.

2. **Subsequent Rounds ($t > 1$):**
   - **Case A: The Threshold Was Met ($C_{t-1} \geq m$):**
     If the collective effort was successful in the previous round, maintain cooperation ($C$). Continue contributing to sustain the reward.

   - **Case B: The Threshold Was Missed ($C_{t-1} < m$):**
     If the collective effort failed, initiate a "tit-for-tat with forgiveness" protocol.
     - If the number of cooperators in the previous round was $\geq m - 1$ (the group was one player short of success), maintain cooperation ($C$). This signals that the group is close to the threshold and encourages continued participation.
     - If the number of cooperators in the previous round was $< m - 1$ (the group failed significantly), switch to $D$ (Defect) for the current round. This minimizes endowment loss when the group is fragmented and unable to achieve the reward.

3. **Terminal Phase (Round $r$):**
   - Regardless of the previous round's outcome, if the running average of historical cooperation remains $\geq (m/n)$, play $C$. This maintains cooperation even when the incentive to defect in the final round is technically maximized, fostering long-term stability if the game were to be repeated beyond $r$.
   - Otherwise, follow the standard decision rule for $t > 1$.

**Pseudocode:**

```python
def choose_action(round_num, history):
    if round_num == 1:
        return 'C'
    
    prev_cooperators = history.last_round_cooperation_count
    
    # Check if threshold was met
    if prev_cooperators >= m:
        return 'C'
    
    # Check for near-miss
    if prev_cooperators >= (m - 1):
        return 'C'
    
    # If round is the final one, check historical performance
    if round_num == r:
        avg_coop = calculate_avg_cooperation(history)
        if avg_coop >= (m / n):
            return 'C'
            
    # Default to defection if group support is too low
    return 'D'
```
'''

description_BENEVOLENT_21 = '''
**Strategy: Conditional Tit-for-Tat Thresholding**

The core of this strategy is to foster cooperation through a "threshold-trigger" mechanism that mimics Tit-for-Tat but accounts for the aggregate nature of the game. Let $N_t$ be the total number of cooperators observed in round $t$. Let $c_t \in \{0, 1\}$ be the action taken in round $t$.

**Initialization (Round 1):**
Play $C$ (Cooperate). This demonstrates goodwill and establishes a signal of potential cooperation without requiring prior evidence of the group's intent.

**Main Loop (Rounds $t=2$ to $r-1$):**
Cooperate if the group demonstrated sufficient cooperation in the previous round; otherwise, defect to protect against exploitation.

*   **Decision Rule:** Play $C$ if $N_{t-1} \geq m$. Otherwise, play $D$ (Defect).
*   **Rationalization:** This rule rewards the group for achieving the threshold $m$. If the group fails to meet $m$, it implies either insufficient interest in cooperation or a failure of coordination, both of which necessitate a defensive posture in the subsequent round.

**Terminal Phase (Round $r$):**
In the final round, ignore the outcome of the previous round's cooperation level and play $C$ (Cooperate).

*   **Decision Rule:** Play $C$.
*   **Rationalization:** Since there are no future rounds to punish non-cooperation or reward success, and the objective is to be benevolent, the final action is a non-contingent offer of cooperation, attempting to maximize the group outcome one last time regardless of past history.

**Adaptive Buffer (Edge Case Handling):**
If at any point in the game $N_{t-1} \geq n-1$ (near-total cooperation occurred), but the strategy dictates $D$ due to an anomaly, prioritize $C$. If the game enters a "death spiral" where $N_t=0$ for three consecutive rounds, reset the strategy by playing $C$ in the next round to test if the group environment has shifted or if new players are influencing the outcome.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, history_n, m):
    # Round 1: Goodwill start
    if round_number == 1:
        return 'C'
    
    # Final Round: Benevolent exit
    if round_number == total_rounds:
        return 'C'
        
    # Death Spiral Reset: Attempt to rekindle cooperation
    # Check if last 3 rounds had 0 cooperators
    if len(history_n) >= 3 and all(n == 0 for n in history_n[-3:]):
        return 'C'

    # Tit-for-Tat Thresholding
    if history_n[-1] >= m:
        return 'C'
    else:
        return 'D'
```
'''

description_BENEVOLENT_22 = '''
**Strategy: Conditional Reciprocal Threshold Cooperation**

**General Principle:** Maintain a cooperative stance to reach the threshold $m$ while monitoring aggregate contribution levels to distinguish between supportive peers and free-riders.

**Phase 1: Initialization**
In Round 1, always play C. This establishes a baseline of cooperation and signals intent to reach the collective threshold.

**Phase 2: Adaptive Response (Rounds 2 to r)**
For all rounds $t \in [2, r]$, calculate the effective contribution rate of the previous round ($t-1$). Let $C_{t-1}$ be the total number of cooperators observed in the previous round.

*   **Cooperation Rule:** Play C if $C_{t-1} \ge m$. By contributing, you help secure the reward $k$ for everyone.
*   **Defection Rule (Trigger):** Play D if $C_{t-1} < m$. If the group fails to meet the threshold, there is no reward $k$, and contributing only reduces your individual payoff (π = 0 vs π = 1). Defection in this state prevents personal loss until a threshold-meeting quorum is re-established.
*   **Safety Override:** Always play C if $t = r$. In the final round, the incentive to defect (to gain an advantage without future repercussions) is nullified, and the goal is to maximize the final round's collective utility.

**Edge Case Handling:**
*   **Threshold Volatility:** If $C_{t-1} < m$, the strategy enters a "Test Mode." In the subsequent round, attempt C with probability $p = 0.5$ (or simply return to C after one round of D) to check if other players are willing to resume cooperation. If the group meets the threshold $m$ again, revert to the Cooperation Rule.
*   **Minimal Threshold Buffer:** If $C_{t-1} = m$, interpret this as a high-risk state. If the game persists, assume the group is fragile and maintain strict adherence to C, as defecting would cause the group to drop below the threshold.

**Benevolent Intent:**
This strategy prioritizes the group outcome by signaling cooperative intent early, sustaining cooperation when the group demonstrates capacity to reach the threshold, and minimizing personal loss during periods of group failure. It avoids punitive behavior against specific individuals (since players are anonymous) and instead uses the aggregate threshold as the sole metric for group health.
'''

description_BENEVOLENT_23 = '''
The strategy operates on a conditional cooperative logic, aiming to achieve the collective threshold while minimizing unnecessary individual exploitation. It is defined as follows:

**1. Initial Strategy (Round 1):**
Play Cooperate (C) unconditionally. This establishes a willingness to contribute toward the collective goal.

**2. Subsequent Strategy (Rounds 2 through r-1):**
Observe the number of contributors (let this be *c_observed*) from the previous round.

*   If the threshold *m* was met in the previous round:
    *   If you contributed (played C) and the total cooperators were exactly *m*: Continue playing C. This maintains the equilibrium.
    *   If you defected (played D) and the total cooperators were exactly *m*: Play D. This is the optimal exploitation point, as the threshold is met without your input.
    *   If total cooperators were *m + 1* or greater: Play D. The collective goal is safe even if one cooperator drops out.
    *   If total cooperators were *m - 1* or fewer: Play C. The threshold was missed; assume a need for increased support.

*   If the threshold *m* was *not* met in the previous round:
    *   Play C, regardless of your previous action. The failure to meet the threshold suggests that the group is not sustaining cooperation, so unconditional contribution is necessary to restore the collective benefit.

**3. Final Round (Round r):**
Because there is no future round to punish defection or reward trust, the incentives shift. However, to remain benevolent, apply a "Last-Chance Support" rule:

*   If the average contribution rate across all previous rounds (Total Contributors / (n * (r-1))) is greater than or equal to (m/n), play C.
*   Otherwise, if the group has consistently failed to meet the threshold *m* in more than 50% of the previous rounds, play D. This prevents wasting resources on an uncooperative population.

**4. Edge Case Handling:**
*   *If you are the only cooperator:* If you played C and observed 0 cooperators, play C in the next round. If you play C for three consecutive rounds and receive 0 additional cooperation, switch to D for the remainder of the game to avoid perpetual exploitation.
*   *If the threshold is low (m ≈ 1):* If m=1, the strategy simplifies to playing D every round, as the collective benefit is negligible relative to the individual cost. In this case, always play D.
'''

description_BENEVOLENT_24 = '''
The strategy utilizes a conditional probabilistic threshold approach designed to incentivize collective cooperation while minimizing exploitation. Let $C_{t}$ be the number of cooperators observed in the previous round, and $P_{t}$ be the probability of playing $C$ in the current round.

**Initialization (Round 1):**
Play $C$ with probability $0.8$.

**Adaptive Decision Rules (Rounds 2 to $r$):**
Define the target cooperation threshold as $m$. Calculate the success of the previous round:
1.  **If $C_{t-1} \geq m$:** The collective target was met. Play $C$ with probability $0.9$. This reinforces the cooperative norm and maintains the reward state.
2.  **If $C_{t-1} = m - 1$:** The target was narrowly missed. Play $C$ with probability $1.0$ (deterministic cooperation) to signal a willingness to bridge the gap.
3.  **If $C_{t-1} < m - 1$:** The group is failing significantly. Play $C$ with probability $0.2$. This shifts to a protective defect stance to prevent unilateral endowment loss when group cooperation is unlikely to reach the threshold.

**Pseudocode Logic:**

```python
def get_action(round_number, prev_cooperators, m):
    if round_number == 1:
        return cooperate_with_prob(0.8)
    
    # Check if threshold was met in previous round
    if prev_cooperators >= m:
        return cooperate_with_prob(0.9)
    
    # If just below threshold, signal willingness to help
    elif prev_cooperators == m - 1:
        return cooperate_with_prob(1.0)
    
    # If significantly below threshold, protect endowment
    else:
        return cooperate_with_prob(0.2)
```

**Terminal Rounds (The "Endgame" Adjustment):**
In the final two rounds ($t = r-1, r$), the strategy adjusts to minimize vulnerability to defectors:
-   If the running average of cooperation over the previous $r/2$ rounds is less than $m - 1$, revert to unconditional defection ($D$) to protect the final endowment.
-   Otherwise, maintain the rules defined above, but decrease all cooperation probabilities by $0.2$.

**Edge Cases:**
-   **If $C_{t-1}$ is unknown (first round):** Defaults to the Initialization rule.
-   **If $m$ is very close to $n$:** The threshold for switching to protective defection ($C_{t-1} < m-1$) becomes stricter. If $m = n$, any defection by any player triggers the $0.2$ probability of cooperation for the next round to avoid being the sole contributor.
'''

description_BENEVOLENT_25 = '''
Adopt a "Conditional Threshold Commitment" strategy:

**Core Logic**
In each round $t \in \{1, \dots, r\}$, determine your action $a_t \in \{C, D\}$ based on the observed history of cooperation from opponents in previous rounds. You aim to sustain cooperation only if it is likely that the collective threshold $m$ will be met.

**Phase 1: Initial Rounds (The Probing Phase)**
For rounds $t=1$ and $t=2$:
- Always play $C$. This establishes a baseline of goodwill and provides immediate, observable data to other players regarding your willingness to participate in the public good.

**Phase 2: Adaptive Maintenance (Rounds $3$ to $r-1$)**
For each round $t$, calculate the *average participation rate* ($P$) of opponents from all prior rounds $1$ to $t-1$.
Let $O_{i,s}$ be the number of opponents who cooperated in round $s$.
$P = \frac{\sum_{s=1}^{t-1} O_{i,s}}{(n-1) \times (t-1)}$

Decision rule:
- If $P \geq \frac{m}{n}$: Play $C$.
- If $P < \frac{m}{n}$: Play $D$.

This rule assumes that if the historical average cooperation rate among opponents is sufficient to meet the threshold (or trends toward it), continued cooperation is rational and benevolent. If the historical average falls below the threshold, switch to defection to avoid the cost of unilateral contribution to a failing project.

**Phase 3: Final Round (Round $r$)**
Regardless of previous history, if you played $C$ in round $r-1$, play $C$ in round $r$. If you played $D$ in round $r-1$, play $D$ in round $r$. This prevents last-minute defection "surprises" that could sour an otherwise stable cooperative equilibrium established in previous rounds.

**Resumption Logic (The Forgiveness Clause)**
If the system detects that the total number of cooperators in the most recent round $t-1$ was $\geq m$, even if the long-term average $P$ was $< \frac{m}{n}$, play $C$ in round $t$. This allows the strategy to recover from periods of low cooperation if the group successfully organizes for a single round.

**Pseudocode Summary**

```python
def choose_action(round, history):
    if round <= 2:
        return 'C'
    
    if round == r:
        return last_action
    
    # Check if immediate previous round succeeded
    if history[round-1]['opponents_cooperated'] >= m:
        return 'C'
    
    # Calculate long-term average
    total_coop = sum(h['opponents_cooperated'] for h in history)
    avg_participation = total_coop / ((n-1) * (round-1))
    
    if avg_participation >= (m / n):
        return 'C'
    else:
        return 'D'
```
'''

description_BENEVOLENT_26 = '''
**Strategy: Conditional Reciprocal Contribution**

**Decision Logic**
The strategy determines action $A_t$ for round $t$ based on the observed cooperation count $C_{t-1}$ from the previous round (where $C_t$ is the number of players who chose $C$ in round $t$).

1.  **Initialization (Round 1):**
    Choose $C$.

2.  **Subsequent Rounds ($t > 1$):**
    Let $N_c = C_{t-1}$ be the number of cooperators observed in the previous round.
    *   **If $N_c \ge m$:** Cooperate ($C$). The threshold is being met; maintain contribution to ensure collective success.
    *   **If $N_c < m$:**
        *   If self played $C$ in $t-1$: Defect ($D$). The group is failing to reach the threshold, and individual contribution is wasted without sufficient partners.
        *   If self played $D$ in $t-1$: Cooperate ($C$) with probability $p = \frac{m}{n}$. Re-attempt contribution to signal potential for coordination and test if others follow suit.

3.  **Terminal Round ($t = r$):**
    Regardless of history, play $D$ if the group has consistently failed to meet the threshold ($N_c < m$ for all $t < r$). If the group has reached $m$ cooperators at any point in the previous three rounds, play $C$. This prevents unilateral exploitation in the final round while maintaining the possibility of success in high-performing groups.

**Edge Case Handling**
*   **Threshold volatility:** If $N_c$ fluctuates around $m$, prioritize $C$ unless $N_c$ falls below $m - \text{floor}(\frac{n}{m})$. This buffer prevents premature abandonment due to noise or isolated defections.
*   **High-cooperation stability:** If $N_c = n$ for consecutive rounds, continue $C$ indefinitely.
*   **Endgame logic:** In the final rounds ($t > r - 3$), transition to a strict "Tit-for-Tat" variant: play $C$ if the aggregate cooperation rate in the previous round was sufficient ($N_c \ge m$), otherwise play $D$ to minimize loss in a failing collective.
'''

description_BENEVOLENT_27 = '''
Establish an initial cooperation probability based on the necessity of meeting the threshold $m$. Calculate the "required contribution density" $\rho = \frac{m}{n}$.

**Decision Rules:**

1.  **Round 1:** Play $C$ if $k > 1$. If $k \le 1$, play $D$.
2.  **Subsequent Rounds:** Let $C_{t-1}$ be the number of cooperators observed in the previous round.
    *   If $C_{t-1} \ge m$: The system is successfully meeting the threshold. Play $C$ to maintain stability.
    *   If $C_{t-1} < m$: The system is failing. Play $C$ only if your contribution can increase the total cooperative count toward the threshold. Specifically, if the previous round resulted in failure, play $C$ with probability $p = 1.0$ for the current round to signal commitment and attempt to trigger a coordination cascade.
    *   **Threshold Buffering:** If $C_{t-1} > m$, you may play $D$ if and only if $C_{t-1} > m+1$ (indicating a surplus of cooperators). This protects against exploitation while ensuring the collective threshold remains safe.

**Edge Cases and Adaptive Adjustments:**

*   **Final Round:** If $r$ is the final round, play $C$ if the cumulative payoff history suggests that consistent cooperation has been the norm (i.e., average $C_{avg} \ge m$). If the group has consistently defected or failed, play $D$ to minimize personal loss, as reputation effects are absent.
*   **Persistent Failure:** If $C_{t-1} < m$ for three consecutive rounds despite your own cooperation, switch to $D$ for one round. This serves as a "reset" signal to test if the group is merely stuck in a coordination failure or if the other players are non-cooperative agents. If the group fails to meet the threshold during your $D$ round, return to $C$ in the next round to continue attempting to lead the group.
*   **The "Free-Rider" Check:** If you observe $C_{t-1} = m$ and you played $D$, and the following round $C_{t-1}$ drops below $m$, return to $C$ immediately. This assumes that your previous defection was necessary to maintain your own payoff parity, but your return to $C$ is necessary to restore the collective benefit.

**Benevolent Intent:**

The strategy prioritizes the maximization of the collective reward $k$ by consistently attempting to meet the threshold $m$ first. Defection is used exclusively as a monitoring tool to avoid exploitation in non-cooperative environments or as an indicator of a "surplus" of cooperators where individual contribution is not mathematically required for the collective good.
'''

description_BENEVOLENT_28 = '''
Adopt a "Threshold-Triggered Tit-for-Tat with Gradual Forgiveness" strategy.

**Strategy Logic**

1.  **First Round (Initialization):**
    Always play Cooperate (C) in Round 1 to signal intent to achieve the collective threshold ($m$).

2.  **Subsequent Rounds ($t > 1$):**
    Assess the outcome of the previous round ($t-1$). Let $C_{prev}$ be the number of cooperators observed in the previous round.
    *   **Cooperation Rule:** If $C_{prev} \ge m$, play Cooperate (C).
    *   **Non-Cooperation Rule:** If $C_{prev} < m$, play Defect (D) with probability $p = 1 - \frac{C_{prev}}{m}$. In practice, if $C_{prev} < m$, play D for the next round to punish the free-riding behavior, but reduce the intensity of punishment as $C_{prev}$ approaches $m$ to encourage recovery.
    *   **Forgiveness Mechanism:** If the system is currently in a "punishment" phase (having defected in the previous round due to $C_{prev} < m$), monitor $C_{prev}$. If $C_{prev}$ increases by at least 1 relative to the round that triggered the punishment, switch back to Cooperate (C) immediately.

3.  **End-Game (Last 3 Rounds):**
    Transition to a conditional cooperation strategy regardless of prior punishment status:
    *   If $C_{prev} \ge m-1$, always play Cooperate (C).
    *   If $C_{prev} < m-1$, play Defect (D) to maximize individual payoff in the final rounds, assuming the collective goal is already unreachable or failed.

**Pseudocode Implementation**

```python
def choose_action(round_number, total_rounds, observed_cooperators_last_round, m):
    # End-game boundary
    if round_number > (total_rounds - 3):
        if observed_cooperators_last_round >= (m - 1):
            return "C"
        else:
            return "D"

    # First round
    if round_number == 1:
        return "C"

    # Standard adaptive logic
    if observed_cooperators_last_round >= m:
        return "C"
    else:
        # Punishment phase: defect if threshold failed
        # Gradual forgiveness: if previous group made an effort, be more likely to forgive
        threshold_deficit = m - observed_cooperators_last_round
        if random() < (threshold_deficit / m):
            return "D"
        else:
            return "C"
```

**Benevolent Alignment**
The strategy prioritizes collective success by defaulting to cooperation. It avoids the "sucker's payoff" by punishing non-cooperation when the threshold is not met, but it incorporates a forgiveness mechanism to prevent death spirals of mutual defection. By utilizing a "threshold-trigger" rather than a strict "Tit-for-Tat," it accommodates the fact that the goal is the collective threshold ($m$), not individual reciprocity, focusing efforts on maintaining the group reward ($k$).
'''

description_BENEVOLENT_29 = '''
To maximize collective welfare while minimizing vulnerability to exploitation, adopt a "Conditional Threshold Tit-for-Tat" strategy. This strategy assumes that the objective is to reach the threshold $m$ as efficiently as possible, while punishing persistent non-cooperators if the group fails to sustain the threshold.

### Decision Rules

Define $C_t$ as the number of cooperators observed in round $t$, and $S_t$ as the player's own action ($S_t = 1$ if Cooperate, $S_t = 0$ if Defect).

1.  **Round 1:** Always choose **Cooperate (C)**. This signals a willingness to collaborate and establishes a baseline for cooperation.

2.  **Rounds $t > 1$:** Determine action based on the history of cooperation relative to the threshold $m$:
    *   **If the threshold was met in the previous round ($C_{t-1} \ge m$):**
        *   If you played $C$ last round, continue to play $C$.
        *   If you played $D$ last round, play $C$ (attempting to reintegrate into the cooperative state).
    *   **If the threshold was not met in the previous round ($C_{t-1} < m$):**
        *   Calculate the "cooperation gap": $g = m - C_{t-1}$ (if you played $D$ in $t-1$) or $g = m - (C_{t-1} - 1)$ (if you played $C$ in $t-1$).
        *   If $g \le 1$, play $C$ to attempt to bridge the gap and reach the threshold.
        *   If $g > 1$, play $D$ for the current round (a "punishment" phase to signal that cooperation is not being reciprocated sufficiently by the collective, preventing wasted contributions).

3.  **Final Round ($t = r$):**
    *   If the group has successfully reached the threshold $m$ in at least 50% of the previous rounds, play $C$.
    *   Otherwise, play $D$ to protect against exploitation, as there is no future interaction to incentivize reciprocation.

### Pseudocode Representation

```python
def get_action(round_number, history, n, m, k):
    # history stores tuples of (my_action, other_cooperators_count)
    
    if round_number == 1:
        return 'C'
    
    if round_number == r:
        success_count = count(h for h in history if (h.my_action + h.other_cooperators) >= m)
        return 'C' if success_count >= (r / 2) else 'D'
    
    last_my_action, last_others = history[-1]
    total_cooperators = last_others + (1 if last_my_action == 'C' else 0)
    
    if total_cooperators >= m:
        return 'C'
    else:
        # Check if we are one away from the threshold
        # If I cooperate, would we hit m?
        if (last_others + 1) >= m:
            return 'C'
        else:
            return 'D'
```

### Edge Cases and Robustness

*   **Failure Persistence:** If the group persistently fails to reach the threshold $m$, the strategy defaults to $D$ whenever the gap is insurmountable ($>1$ player needed). This prevents the "sucker's payoff" while remaining ready to switch back to $C$ the moment observation suggests the group is close to meeting the threshold.
*   **Threshold Buffering:** By strictly requiring the threshold $m$ be met for sustained cooperation, the strategy avoids the "free-rider" trap where players cooperate while others defect. If the group consistently hits $m$, the strategy locks into perpetual cooperation.
*   **Initialization:** The first-round cooperation is non-negotiable; it creates the "benevolent" seed required to trigger reciprocal behavior from other rational actors.
'''

description_BENEVOLENT_30 = '''
**Strategy: Threshold Reciprocity with Opportunistic Safeguards**

The strategy operates on the principle of conditional cooperation, maintaining the cooperative threshold $m$ while punishing unilateral defection and protecting against free-riders. It relies on the observed count of cooperators from the previous round, denoted $C_{t-1}$.

**Decision Rules:**

1.  **Round 1 (Initialization):**
    Always play **Cooperate (C)**. This signals a willingness to achieve the threshold $m$ and assumes initial goodwill among players.

2.  **Round $t$ (where $1 < t < r$):**
    The decision depends on the outcome of the previous round ($C_{t-1}$):
    *   **If $C_{t-1} \ge m$:** Play **Cooperate (C)**. The collective goal is being met; maintain current momentum.
    *   **If $C_{t-1} < m$:** 
        *   If the current player cooperated in the previous round ($c_{t-1} = 1$), play **Defect (D)**. This is a "punishment" phase to signal that the current contribution level is insufficient for the threshold to be met, preventing the waste of endowments.
        *   If the current player defected in the previous round ($c_{t-1} = 0$), play **Cooperate (C)**. This is a "probing" move to attempt to restore the cooperative threshold.

3.  **Last Round ($t = r$):**
    Regardless of history, play **Cooperate (C)**. Since the game concludes, there is no future to protect, and the risk of being exploited by free-riders does not affect future payoffs. This acts as a final attempt to maximize the total group payoff.

**Pseudocode:**

```python
def decide_action(round_number, total_rounds, last_round_cooperators, my_last_action, m):
    # Terminal Round: Always contribute
    if round_number == total_rounds:
        return 'C'

    # Initial Round: Always contribute
    if round_number == 1:
        return 'C'

    # Threshold Check
    if last_round_cooperators >= m:
        return 'C'
    else:
        # If threshold not met, reverse previous action
        if my_last_action == 'C':
            return 'D'  # Retract contribution to preserve endowment when threshold fails
        else:
            return 'C'  # Attempt to restart cooperation
```

**Edge Case Handling:**

*   **Sudden Drop in Cooperation:** If the number of cooperators falls significantly below $m$, the strategy defaults to Defect for one round to minimize losses, then attempts to resume cooperation. It does not hold permanent grudges, allowing the group to recover if other players return to cooperation.
*   **Constant Defection:** If the group fails to meet $m$ consistently for multiple rounds, the strategy alternates between C and D. This prevents the player from being a "sucker" while keeping the door open for a collaborative pivot by other agents.
*   **Threshold volatility:** If $C_{t-1} = m-1$, the strategy prioritizes Cooperation (C) in the next round, regardless of the previous action, to provide the minimal necessary nudge to cross the threshold, provided the loss from one round of unsuccessful cooperation is outweighed by the potential reward $k$ in subsequent rounds.
'''

description_BENEVOLENT_31 = '''
### Strategy: Threshold-Conditional Reciprocity (TCR)

**Objective**
The strategy aims to establish cooperation up to the minimum threshold $m$, while simultaneously avoiding exploitation by defectors. It balances benevolent contribution with defensive defection.

**Decision Logic**

1.  **Initialization (Round 1):**
    *   Always play **Cooperate (C)**.

2.  **Tracking State:**
    *   Maintain a variable $H_t$ representing the number of cooperators observed in the previous round $t-1$.
    *   Maintain a "Trust Score" $S$ (initialized to $S_0 = m$).

3.  **Round $t$ Decision Rule ($1 < t < r$):**
    *   Let $N_c$ be the number of cooperators observed in round $t-1$.
    *   If $N_c \ge m$: The threshold was met. Increase the Trust Score: $S_t = \min(S_{t-1} + 1, n)$. Play **Cooperate (C)**.
    *   If $N_c < m$: The threshold was failed. Decrease the Trust Score: $S_t = \max(S_{t-1} - 1, 0)$.
        *   If your role in $t-1$ was **Cooperate (C)**: Play **Defect (D)** to punish/protect against insufficient contribution.
        *   If your role in $t-1$ was **Defect (D)**: Play **Defect (D)**.
    *   Conditional Re-entry: If your Trust Score $S_t$ returns to or exceeds $m$ after a failed round, revert to **Cooperate (C)**.

4.  **Terminal Phase (Round $r$):**
    *   If $N_c \ge m$ (previous round success): Play **Cooperate (C)**.
    *   If $N_c < m$ (previous round failure): Play **Defect (D)** to avoid the risk of contributing to a guaranteed failure.

**Pseudocode Representation**

```python
# Initialization
S = m  # Trust Score
last_action = C

# Per Round
def get_action(round_number, last_round_cooperators, last_action):
    if round_number == 1:
        return C

    # Update Trust Score
    if last_round_cooperators >= m:
        S = min(S + 1, n)
    else:
        S = max(S - 1, 0)

    # Decision Logic
    if round_number == r:
        return C if last_round_cooperators >= m else D

    if S >= m:
        return C
    else:
        # If Trust is low, defect to protect endowment
        return D
```

**Edge Case Handling**
*   **Persistent Defection:** If the group fails to reach $m$ for consecutive rounds, $S$ will drop to 0, locking the agent into **Defect (D)**. The agent will remain in this state unless it detects a shift in the environment; however, without communication, this strategy assumes that if the group cannot coordinate by round 2, it is unlikely to coordinate without external intervention.
*   **Threshold Excess:** If $N_c > m$, the strategy contributes to a surplus. This is acceptable as it signals robust intent to cooperate and buffers against potential fluctuations in opponent behavior.
*   **Last Round:** The strategy prioritizes outcome probability. If the group has demonstrated success ($N_c \ge m$) in the penultimate round, it contributes in the final round to ensure the reward. If the group failed the penultimate round, it defects to avoid wasted endowment.
'''

description_BENEVOLENT_32 = '''
The strategy employs a "threshold-trigger tit-for-tat" mechanism designed to incentivize collective success while protecting against exploitation.

**Decision Logic**

1. **Initial Round:** Always play Cooperate (C) in round 1. This signals benevolence and initiates the possibility of meeting the threshold $m$.

2. **Subsequent Rounds (t > 1):**
   * Let $C_{t-1}$ be the number of cooperators observed in the previous round.
   * If the threshold was met in the previous round ($C_{t-1} \ge m$), play Cooperate (C). This reinforces the cooperative equilibrium.
   * If the threshold was missed in the previous round ($C_{t-1} < m$), initiate a "Conditional Defection" period. Play Defect (D) for one round to minimize losses while testing if the group is viable.
   * If you played Defect (D) in round $t-1$ because the threshold was missed, calculate your "Recovery Probability" ($P$):
     * If $C_{t-1} \ge m - 1$ (i.e., the group was just one person away from the threshold), play Cooperate (C) in round $t$. The group is near-viable.
     * If $C_{t-1} < m - 1$, play Defect (D) again. The group is non-cooperative.

3. **Endgame Constraint:**
   * In the final round $r$, if the strategy was in a "Cooperate" state in the previous round ($t-1$), play Cooperate (C).
   * If the strategy was in a "Defect" state or the group has consistently failed to reach the threshold in the last $\lceil r/4 \rceil$ rounds, play Defect (D) to preserve payoff.

**Pseudocode Representation**

```
state = Cooperate
if t == 1:
    action = C
else if t == r:
    if state == Cooperate:
        action = C
    else:
        action = D
else:
    if C_{t-1} >= m:
        action = C
        state = Cooperate
    else if C_{t-1} >= m - 1:
        action = C
        state = Cooperate
    else:
        action = D
        state = Defect
```

**Edge Case Handling**
* **Systemic Failure:** If $C_{t-1} = 0$ for two consecutive rounds, assume the population is purely defecting. Shift to permanent Defection (D) for the remainder of the game to avoid exploitation.
* **Near-Threshold Volatility:** If the group toggles between $m$ and $m-1$ cooperators, the strategy locks into Cooperate (C), prioritizing the long-term payoff $k$ over the marginal loss of 1 unit, as $k > 1$.
'''

description_SELFISH_5 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat with Defection bias**

Initialize `threshold_met_history` = 0.
Initialize `rounds_remaining` = r.

For each round `t`:

1. **First Round (t=1):**
   Defect.

2. **Subsequent Rounds (t > 1):**
   Analyze the aggregate number of cooperators (`C_total`) from the previous round (`t-1`).
   
   If `C_total` >= `m`:
      *   If `C_total` == `m`:
         Cooperate. (Reinforce the minimum threshold to maintain rewards without excess contribution).
      *   If `C_total` > `m`:
         Defect. (Exploit the surplus cooperation provided by others to maximize personal payoff).
   
   If `C_total` < `m`:
      *   If `rounds_remaining` == 1:
         Defect. (There is no future penalty for failure; maximize final private endowment).
      *   If `rounds_remaining` > 1:
         Cooperate with probability `P`, where `P = (m - C_total) / (n - C_total)`.
         (Contribute only to the extent necessary to pull the aggregate toward the threshold `m`, minimizing personal cost while attempting to salvage the reward).

3. **Terminal Condition:**
   In the final round (`t = r`), always Defect, regardless of previous history.
'''

description_SELFISH_6 = '''
**Round 1:**
Play Defect (D).

**Subsequent Rounds (t > 1):**
Observe the number of cooperators from the previous round, denoted as $C_{t-1}$.

If the threshold $m$ was met in the previous round ($C_{t-1} \ge m$):
- If you played C in the previous round: Switch to Defect (D).
- If you played D in the previous round: Continue to Defect (D).

If the threshold $m$ was not met in the previous round ($C_{t-1} < m$):
- Check the number of cooperators required to meet the threshold: $m_{needed} = m - C_{t-1}$.
- If $m_{needed} = 1$: Play Cooperate (C). This is the "critical threshold" condition where your single contribution is the marginal difference between a failed threshold and a successful one.
- If $m_{needed} > 1$: Play Defect (D). It is mathematically irrational to contribute if your individual action cannot force the threshold to be met, as you retain your endowment while the failure is inevitable regardless of your choice.

**Final Round (t = r):**
Regardless of history, always play Defect (D). Cooperation yields no future reciprocal benefit, and there is no subsequent round to influence through signaling.

**Edge Cases:**
- If $C_{t-1}$ is unknown or the system provides no history (though the prompt guarantees aggregate observation), default to Defect (D).
- If the game parameters imply $k < 1$ (making cooperation never profitable even if the threshold is met), default to Defect (D) for all rounds.
'''

description_SELFISH_7 = '''
The strategy utilizes a threshold-sensitive "conditional tit-for-tat" approach, focusing on maintaining the threshold only when doing so yields a higher expected utility than free-riding.

**State Variables:**
- $C_t$: Number of players who cooperated in round $t$.
- $s_{t-1}$: Personal decision in the previous round ($1$ if C, $0$ if D).
- $T$: Total rounds remaining (calculated as $r - t + 1$).

**Decision Logic:**

1.  **First Round ($t=1$):**
    Play **Defect (D)**. This establishes a baseline for opponent behavior without incurring the cost of cooperation.

2.  **Subsequent Rounds ($t > 1$):**
    Calculate the effective necessity of your cooperation:
    - If $C_{t-1} \ge m + 1$:
      The threshold was met by others even without your contribution. Play **Defect (D)** to maximize free-riding.
    - If $C_{t-1} = m$:
      If you played $C$ in the previous round and the group met the threshold, you were critical; play **Cooperate (C)**. If you played $D$, the group met the threshold without you; play **Defect (D)**.
    - If $C_{t-1} = m - 1$:
      The threshold was missed by exactly one person. If you played $D$, play **Cooperate (C)** to attempt to trigger the reward. If you played $C$, switch to **Defect (D)** because the group failed to coordinate despite your effort.
    - If $C_{t-1} < m - 1$:
      The threshold was missed by a wide margin. Play **Defect (D)**.

3.  **Last Round ($T=1$):**
    - If $C_{r-1} \ge m$:
      Play **Defect (D)**. The reward is secured regardless of your final contribution.
    - If $C_{r-1} < m$:
      Evaluate the "Last Attempt" heuristic:
      If $C_{r-1} = m - 1$, play **Cooperate (C)**. Otherwise, play **Defect (D)**.

**Pseudocode Representation:**

```python
def decide(t, r, m, k, history):
    if t == 1:
        return D
    
    # Analyze previous round
    prev_C = history.last_round_cooperators
    
    # If the threshold is already met by others, free-ride
    if prev_C >= m:
        return D
        
    # If we are the marginal player needed to hit the threshold
    if prev_C == m - 1:
        # If this is the last round, make a final attempt to secure reward
        if t == r:
            return C
        # Otherwise, attempt to trigger coordination
        return C
    
    # If threshold is far from being met, do not waste investment
    return D
```
'''

description_SELFISH_8 = '''
**Strategy: Threshold-Sensitive Conditional Reciprocity**

This strategy operates on the principle of minimal necessary contribution to maximize personal payoff while incentivizing cooperation from others. It treats the game as a recurring coordination problem where the goal is to trigger the reward $k$ while bearing the cost $1$ as infrequently as possible.

**Decision Rules:**

1.  **Round 1:** Play **Cooperate (C)**. This signals a willingness to coordinate and tests the aggregate responsiveness of the group.

2.  **Subsequent Rounds (2 to $r-1$):**
    *   Define $C_{t-1}$ as the number of cooperators observed in the previous round.
    *   If $C_{t-1} \ge m$: Play **Defect (D)**. The threshold was met last round without my contribution; attempt to free-ride.
    *   If $C_{t-1} = m - 1$: Play **Cooperate (C)**. The threshold was narrowly missed; attempt to bridge the gap to secure the reward $k$.
    *   If $C_{t-1} < m - 1$: Play **Defect (D)**. The group is too far from the threshold; contributing is a sunk cost with no reward.

3.  **Final Round ($r$):**
    *   If $C_{r-1} \ge m$: Play **Defect (D)**. There is no future round to punish defection, and the previous round's cooperation suggests the threshold is likely to be met without contribution.
    *   If $C_{r-1} < m$: Play **Defect (D)**. The group has failed to establish a cooperative equilibrium; abandon the effort to maximize the current private endowment.

**Pseudocode:**

```python
def decide_action(round_t, total_rounds, m, last_round_cooperators):
    # Rule for the final round (Always defect to maximize current payoff)
    if round_t == total_rounds:
        return 'D'
    
    # Rule for the first round (Attempt to initiate cooperation)
    if round_t == 1:
        return 'C'
    
    # Adaptive rule for intermediate rounds
    if last_round_cooperators >= m:
        # Threshold met: try to free-ride
        return 'D'
    elif last_round_cooperators == m - 1:
        # Threshold missed by one: bridge the gap
        return 'C'
    else:
        # Threshold missed by many: avoid cost
        return 'D'
```

**Edge Case Handling:**
*   **Initial Defection:** If the group fails to reach $m$ in Round 1, the strategy immediately switches to Defect (D) for all subsequent rounds, assuming the population is non-cooperative.
*   **Constant Free-Riding:** If the strategy detects that it is the only one consistently trying to "bridge the gap" (i.e., $C_{t-1}$ remains $m-1$ repeatedly while playing C), it ceases cooperation after three consecutive attempts to avoid persistent exploitation.
'''

description_SELFISH_9 = '''
The strategy adopts a conditional threshold-tracking approach designed to maximize individual payoff by cooperating only when essential to trigger the reward, and defecting otherwise. Let $c_{t-1}$ be the number of cooperators in the previous round, and let $S_t$ be the action taken in round $t$.

1. **Initial Action:**
   In the first round, play $C$ (Cooperate). This serves as a probe to determine the baseline level of cooperation among the other $n-1$ players.

2. **Decision Rule (Rounds 2 through $r-1$):**
   Calculate the "cooperation deficit" $D_t = m - 1 - c_{t-1}$.
   *   If $c_{t-1} \ge m$, the threshold is naturally met without your contribution. Play $D$ (Defect) to capture the reward $k$ while keeping your own endowment.
   *   If $c_{t-1} = m - 1$, the threshold is only met if you cooperate. Play $C$.
   *   If $c_{t-1} < m - 1$, the threshold cannot be met even if you cooperate (assuming previous behavior persists). Play $D$ to conserve the endowment.

3. **Terminal Round (Round $r$):**
   *   If $c_{r-1} \ge m$, play $D$.
   *   If $c_{r-1} < m$, play $D$. There is no future round to incentivize others to cooperate, so contribute nothing to ensure the highest possible private payoff.

4. **Adaptive Adjustment (The "Retry" Trigger):**
   If the strategy observes that the threshold $m$ was not met in the previous round despite the strategy playing $C$ (meaning $c_{t-1} = m-1$ and you played $C$, but the aggregate $c$ still failed to reach $m$ or plummeted), reset the probe: play $C$ for one round to re-evaluate the willingness of the population to cooperate.

**Pseudocode:**

```python
# Variables: n, m, k, r are parameters
# history: list of observed cooperators per round
# c_prev: cooperators in round t-1

def strategy(t, r, history):
    if t == 1:
        return 'C'
    
    if t == r:
        return 'D'

    c_prev = history[-1]
    
    # Check if threshold is met without self
    if c_prev >= m:
        return 'D'
        
    # Check if self is the tipping point
    elif c_prev == m - 1:
        return 'C'
    
    # Check if threshold is impossible even with self
    else:
        # Check if previous round was a failed probe
        if len(history) > 1 and history[-1] < m - 1 and history[-2] == m - 1:
             return 'C' # Attempt to re-probe
        return 'D'
```
'''

description_SELFISH_10 = '''
**Initialization (Round 1):**
Play C (Cooperate) to probe the cooperative capacity of the population.

**Subsequent Rounds (2 to r-1):**
Observe the number of cooperators from the previous round, denoted as *C_prev*.

1.  **If *C_prev* ≥ *m*:**
    *   If you played C in the previous round, switch to D (Defect) to maximize immediate payoff, testing if the threshold *m* can still be met without your contribution (free-riding).
    *   If you played D in the previous round, continue playing D.

2.  **If *C_prev* < *m*:**
    *   If you played D in the previous round, switch to C (Cooperate) to attempt to pull the group payoff over the threshold *m*, provided that *k* > 1 (the threshold benefit outweighs the cost of contributing).
    *   If you played C in the previous round and the threshold was still not met, play C again if *C_prev* = *m*-1 (indicating only one more contribution is needed). If *C_prev* < *m*-1, switch to D, as the group lacks sufficient cooperative momentum to make the investment worthwhile.

**Final Round (Round *r*):**
*   If the aggregate cooperative history suggests a high probability of the group meeting the threshold (based on the average *C_t* across all prior rounds), play D to capture the full reward *k* plus the private endowment.
*   If the aggregate cooperative history suggests the threshold will not be met, play D to secure the endowment, as there is no future round to incentivize behavior change in others.
'''

description_SELFISH_11 = '''
**Strategy: Threshold Conditional Defection (TCD)**

1.  **Initial State (Round 1):**
    Play **Defect (D)**. This establishes a baseline and prevents immediate exploitation by potential unconditional defectors.

2.  **Tracking Mechanism:**
    Maintain a running estimate of the "Cooperation Propensity" of the group ($P$).
    *   Let $c_t$ be the total number of cooperators observed in round $t$.
    *   $P$ is the average of $c_t$ across all previous rounds.

3.  **Core Decision Rules (Rounds $t > 1$):**
    Determine cooperation for round $t$ based on the following logic:

    *   **Step A: Threshold Assessment:** If the most recent round $t-1$ saw $c_{t-1} \ge m$, the threshold for the collective reward was successfully met. The incentive to defect is high because the reward is already unlocked. If $c_{t-1} \ge m$, set `Project_Status = "Sufficient"`. Otherwise, set `Project_Status = "Deficient"`.

    *   **Step B: The "Selfish Pivot":**
        *   If `Project_Status == "Sufficient"`: Play **Defect (D)**. The group is currently coordinating effectively; exploit this by withholding contribution while still receiving the reward $k$.
        *   If `Project_Status == "Deficient"` and $t < r$: Calculate the "Minimum Necessary Contribution" ($NNC$).
            *   $NNC = m - c_{t-1}$.
            *   If $NNC \le 1$, play **Cooperate (C)** to bridge the gap.
            *   If $NNC > 1$, play **Defect (D)**. If the gap is too large to bridge alone, contributing is a wasted endowment.

4.  **Edge Cases:**
    *   **Final Round ($t = r$):** Always play **Defect (D)**. There are no future rounds to incentivize cooperation, and the probability of shifting the group outcome alone is insufficient to justify the cost of $C$ if the group has not already demonstrated a high $P$.
    *   **The "Uncooperative Group" scenario:** If $P < 1$ for three consecutive rounds and `Project_Status` remains "Deficient", shift to **Defect (D)** for all remaining rounds, regardless of $m$. The group is effectively uncooperative, and contributing is a sunk cost.
    *   **The "Greedy Equilibrium" scenario:** If $c_{t-1} = m$, meaning the group is perfectly hitting the threshold, play **Defect (D)**. Do not be the $(m+1)^{th}$ contributor; prioritize keeping the endowment over contributing to a project that is already sufficiently funded.
'''

description_SELFISH_12 = '''
**Strategy: Threshold-Adaptive Trigger**

The strategy operates on a "Conditional Free-Riding" principle, seeking to maximize payoffs by contributing only when necessary to trigger the threshold, while defecting whenever the threshold is already met or impossible to achieve.

**Core Decision Rule**
In any round $t$, calculate the number of cooperators observed in the previous round ($C_{t-1}$).
1.  **Calculate Effective Need:** Let $Need = m - C_{t-1}$.
2.  **Evaluate Threshold Feasibility:**
    *   If $Need \le 0$ (threshold was already met/exceeded): Defect ($D$).
    *   If $Need > 1$ (threshold cannot be met by your single contribution): Defect ($D$).
    *   If $Need = 1$ (your contribution is the pivot to reach the threshold): Cooperate ($C$).

**Initialization (Round 1)**
In the first round, initiate with a "Trial-Defect" stance to gauge the baseline cooperation rate of the population without risking the endowment. Play $D$.

**Adaptive Adjustment (Round $t > 1$)**
*   **Success Monitoring:** If your contribution leads to a successful threshold event in round $t$ (i.e., you played $C$ and the threshold was met), maintain the Conditional Free-Riding logic.
*   **Failure Monitoring:** If you played $C$ but the threshold was *not* met (meaning the total cooperators including you was $< m$), escalate to a "Hard-Defect" stance for the next 2 rounds. During Hard-Defect, play $D$ regardless of the need to conserve endowment against uncooperative populations.
*   **Reciprocity Check:** If the observed cooperation level $C_{t-1}$ consistently stays at or above $m-1$ while you are playing $D$, continue playing $D$. If $C_{t-1}$ drops significantly below $m$, return to the Core Decision Rule.

**Edge Cases**
*   **Final Round ($r$):** Regardless of history, if $Need > 1$, play $D$. If $Need \le 0$, play $D$. If $Need = 1$, play $C$ only if the cumulative payoff difference between triggering the reward $k$ and losing the endowment $1$ is positive (i.e., if $k > 1$). If $k \le 1$, play $D$ even if you are the pivot, as the cost of contribution outweighs the marginal gain.
*   **Ambiguity:** If the previous round's outcome is unavailable or equal to round 1, default to $D$.
*   **Threshold Impossibility:** If $m > n$, always play $D$.
'''

description_SELFISH_13 = '''
1. **First-Round Strategy**
Play Defect (D). Starting with C is a dominated strategy in a selfish pursuit because it assumes cooperation from others without proof of necessity or reciprocity. Defection preserves the endowment while establishing a baseline for the opponents' aggregate behavior.

2. **Ongoing Strategy (General Case)**
Monitor the number of cooperators ($C_{t-1}$) from the previous round.
- If $C_{t-1} \ge m$, play D. The threshold is already being met by others; contributing would only reduce personal payoff by 1 without increasing the collective reward $k$.
- If $C_{t-1} < m$, identify the "Critical Gap" ($G = m - C_{t-1}$):
    - If $G = 1$ (the project failed by exactly one person last round), play C. By contributing, you move the group from failure to success, yielding a net gain of $+1$ ($k - 1 > 0$ since $k > 1$). 
    - If $G > 1$, play D. The project is likely to fail regardless of your single contribution, and attempting to reach the threshold alone is insufficient and costly.

3. **Last-Round Strategy**
Because there is no future round to punish or incentivize opponents, the game becomes a one-shot dilemma.
- If $k - 1 > 0$ and the number of cooperators in the previous round ($C_{r-1}$) was $m-1$, play C.
- In all other scenarios, play D.

4. **Edge Cases and Robustness**
- **Triggering Failure:** If a sequence of rounds shows that the group has stabilized at $C < m$ but near the threshold, and your contribution can shift the outcome to success ($m$), prioritize the reward $k$ over the endowment cost only if $k > 1$. If $k$ is sufficiently high, prioritize reaching $m$ even if the opponents are inconsistent, provided the cost-benefit analysis $(k-1)$ remains positive.
- **Opponent Exploitation:** If you observe that playing C consistently results in the group meeting the threshold $m$ but others are consistently playing D to free-ride off your contribution, switch immediately to D. You will sacrifice the $k$ reward for one round to signal that you will not bear the cost of the threshold alone. If the group fails and subsequently realizes they need to cooperate to trigger $k$, return to C only when the threshold is one player away.
'''

description_SELFISH_14 = '''
**Strategy: Threshold-Dependent Conditional Cooperation**

This strategy maximizes utility by attempting to secure the reward $k$ only when the marginal cost of contribution is offset by the probability of meeting the threshold $m$. It treats the game as a series of coordination opportunities, defaulting to defection when coordination is unlikely or unnecessary.

**Parameters**
- $c_t$: Number of cooperators in the previous round $t-1$.
- $target$: The number of cooperators required to meet the threshold, $m$.
- $contribution\_cost$: 1.
- $reward$: $k$.

**Decision Rules**

For round $t=1$:
1. If $m=1$, play C (the threshold is trivial).
2. If $m > 1$, play D. Defecting in the first round establishes a baseline to observe if other players are attempting to coordinate or if the population is predominantly defecting.

For rounds $t \in [2, r]$:
1. **The Threshold Trigger:** Calculate the required cooperation from the *other* $n-1$ players to meet the threshold. If you contributed in $t-1$, you need $m-1$ others. If you defected in $t-1$, you need $m$ others.
2. **Conditional Cooperation Rule:**
   - If ($c_{t-1} \geq m$), play C. The threshold is being met, and cooperation is required to sustain the benefit $k$. 
   - If ($c_{t-1} == m-1$) AND you played D in the previous round:
     - Play C. You are the swing vote necessary to secure the reward $k$. 
   - Otherwise:
     - Play D. 

**Edge Cases and Adjustments**

*   **The Final Round ($t=r$):**
    - Apply the standard Conditional Cooperation Rule. However, if the history of the game shows that the threshold $m$ has never been met, ignore the potential for reward and play D. Selfish optimization dictates avoiding a sunk cost for a benefit that has historically proven unattainable.

*   **Failure Recovery:**
    - If $c_{t-1} < m - 1$ (the threshold is not within reach even if you contribute), play D. Attempting to contribute when the group is far from the threshold results in a guaranteed loss of endowment with zero probability of securing $k$.

*   **The "Greedy" Defection Rule:**
    - In any round where $c_{t-1} \geq m + 1$ (the threshold is being met by others without your contribution), play D. You secure the reward $k$ without incurring the cost of contribution. 

**Pseudocode Summary**

```python
def decide_action(round, history, n, m, k):
    if round == 1:
        return 'C' if m == 1 else 'D'
    
    prev_c = history[-1]
    
    # Check if threshold is met by others
    if prev_c >= m + 1:
        return 'D' # Free-ride
        
    # Check if contribution makes the difference
    if prev_c == m:
        return 'C' # Maintain threshold
        
    if prev_c == m - 1:
        return 'C' # Become the swing voter
        
    return 'D' # Threshold out of reach
```
'''

description_SELFISH_15 = '''
**Strategy: Conditional Threshold Thresholding (CTT)**

This strategy operates on the principle of maximizing private gain by playing Defect ($D$) by default and only switching to Cooperate ($C$) when necessary to trigger the threshold ($m$) for the bonus ($k$), provided the cost of contribution is less than the expected gain.

**Core Decision Rule:**

Calculate the "Effective Marginal Contribution" (EMC) required in each round $t$:
Let $C_t$ be the number of cooperators observed in round $t-1$.
Let $S_t$ be the status of the current round. 

1.  **If $t = r$ (Last Round):**
    Always play $D$. The benefit of the bonus $k$ is already realized or lost; contributing only reduces your final payoff by 1.

2.  **If $t < r$:**
    Evaluate the necessity of contributing:
    *   **Case A: Threshold is currently met ($C_t \ge m$).** Play $D$. You are already receiving the bonus $k$.
    *   **Case B: Threshold is not met ($C_t < m$).**
        *   If $(m - C_t) == 1$: This is the "Pivot Point." You are the only person required to meet the threshold. Play $C$ if and only if $k > 1$. If $k \le 1$, play $D$.
        *   If $(m - C_t) > 1$: Do not contribute. If your single contribution cannot bridge the gap to $m$, playing $C$ is a guaranteed loss of 1. Play $D$.

**Initial Round (t = 1):**
Play $D$. Since you have no history of opponent behavior, assume the threshold is not met without your contribution or will be met by others. Defecting secures the baseline payoff of 1.

**Adaptive Mechanism:**
After the first round, track the observed number of cooperators ($C_t$).
*   If the threshold $m$ was met in the previous round, maintain $D$.
*   If the threshold $m$ was *not* met, calculate the deficit: $d = m - C_t$.
    *   If $d = 1$, play $C$ in the current round $t+1$.
    *   If $d > 1$, continue to play $D$ for the remainder of the game, as the group is demonstrably failing to coordinate on the threshold and individual contribution is insufficient to secure $k$.

**Pseudocode:**

```python
def get_action(round_t, total_rounds, m, k, last_round_cooperators):
    # Rule 1: Last round is always Defect
    if round_t == total_rounds:
        return 'D'
    
    # Rule 2: First round is always Defect
    if round_t == 1:
        return 'D'
    
    # Rule 3: Strategic Pivot
    # Only cooperate if exactly one more person is needed to reach the threshold
    deficit = m - last_round_cooperators
    
    if deficit == 1 and k > 1:
        return 'C'
    
    # Rule 4: Default behavior
    return 'D'
```
'''

description_SELFISH_16 = '''
Strategy: Conditional Threshold Monitoring (CTM)

Decision Rules:

1. Initialization:
   - For round 1, play C with probability $p = m/n$ (to test the cooperation propensity of the group).
   - Maintain a variable $S$ representing the "Systemic Cooperation Baseline," initialized to the count of cooperators observed in round 1.

2. Round $t$ (where $t > 1$):
   - Calculate the "Observed Cooperation Rate" ($O_{t-1}$) from the previous round.
   - Update $S$ using a weighted moving average: $S_{new} = 0.7(S_{old}) + 0.3(O_{t-1})$.
   - Determine the "Defection Incentive": If $S > m$, there is sufficient cooperation without personal contribution. If $S \le m$, the collective is at risk of falling below the threshold.

   - Decision Logic:
     - If $S \ge m + 1$: Play D. (The group cooperates sufficiently even without your input; free-ride).
     - If $m < S < m + 1$: Play D. (The group is hovering just above the threshold; you are likely safe to free-ride, but monitor closely).
     - If $S \le m$:
       - Calculate the "Risk-Adjusted Contribution" ($R_c$). If $m - S$ (the gap to threshold) is large, the chance of failing is high. 
       - If $m - S > 1$: Play C (The group is failing significantly; contribution is necessary to secure the reward $k$).
       - If $m - S \le 1$: Play C with probability $1 - (m - S)$ (A mixed strategy to nudge the group toward the threshold without guaranteed over-contribution).

3. Endgame Correction:
   - For the final round ($r$):
     - If $S \ge m$: Play D. (Take the final profit regardless of collective outcome).
     - If $S < m$: Play C if the expected utility of contributing ($k - 1$) is greater than the utility of defecting (keeping 1, assuming threshold is likely missed anyway), otherwise play D.

Edge Cases:
- If $k \le 1$: Play D in all rounds, as the cost of cooperation exceeds the reward.
- If $n - m$ (the number of free-riders allowed) is very small, prioritize C to avoid threshold failure, defaulting to C if the observed $S$ has dropped for two consecutive rounds, regardless of the calculation, to "reset" the group's cooperation behavior.
'''

description_SELFISH_17 = '''
1. **Initial Assessment (Round 1):**
Cooperate if $m/n > 0.5$ and $k > 1$. Otherwise, Defect. This tests the baseline cooperation level of the population while minimizing risk.

2. **Adaptive Decision Rule (Rounds 2 to r-1):**
Maintain a "Target Contribution Rate" (TCR), defined as the minimum number of cooperators required to trigger the reward ($m$). If the previous round's total cooperation count ($C_{total}$) was $\ge m$, you are in a "Stable" state. If $C_{total} < m$, you are in an "Under-performing" state.

- If the previous round resulted in a reward ($C_{total} \ge m$):
  - If you cooperated, continue to Cooperate only if $C_{total} > m$. If $C_{total} == m$, you are a necessary contributor; Defect to check if the group maintains the threshold without you.
  - If you defected, continue to Defect.

- If the previous round failed to result in a reward ($C_{total} < m$):
  - If $C_{total} == m - 1$, switch to Cooperate (or maintain Cooperation).
  - If $C_{total} < m - 1$, switch to Defect. The group is too far from the threshold to justify individual contribution; save resources.

3. **Terminal Strategy (Round r):**
If the total game payoff is currently maximized by achieving the threshold in the final round (calculated by evaluating if $k > 1$), play C only if $C_{total, r-1} == m - 1$. Otherwise, play D. If $k \le 1$ or if the potential gain from the final round does not outweigh the cost of contribution, play D regardless of history.

4. **Pseudocode Logic:**
```
Let C_prev = total cooperators in previous round
Let MyAction_prev = action in previous round
Let Needed = m

If round == 1:
    If (m/n > 0.5) AND (k > 1): return C
    Else: return D

If C_prev >= Needed:
    If MyAction_prev == C:
        If C_prev > Needed: return D
        Else: return C
    Else (MyAction_prev == D):
        return D

If C_prev < Needed:
    If C_prev == Needed - 1:
        return C
    Else:
        return D
```
'''

description_SELFISH_18 = '''
Maintain a state variable `Target_Cooperators` initialized to `m` and a history counter for the number of rounds elapsed.

**Decision Logic:**

1.  **Round 1:** Play **D** (Defect). This establishes a baseline and prevents unnecessary expenditure before observing opponent behavior.

2.  **Subsequent Rounds (2 to r):**
    *   Let $N_{C, t-1}$ be the number of cooperators observed in the previous round.
    *   If $N_{C, t-1} \ge m$: The threshold was met. Play **D**. The incentive is to free-ride since the threshold is already satisfied by others.
    *   If $N_{C, t-1} < m$: The threshold was not met.
        *   Calculate the Deficit $D = m - N_{C, t-1}$.
        *   If the deficit $D$ is exactly 1 (meaning the threshold would have been met if one more person cooperated), play **C** (Cooperate). This is a calculated risk to trigger the reward $k$ for the current round.
        *   If the deficit $D > 1$, play **D**. If opponents are not contributing enough to make cooperation viable, contributing a single unit is a sunk cost with no return.

3.  **Final Round (r):**
    *   Regardless of previous rounds, play **D**. Since there are no future rounds to incentivize or punish other players, there is no strategic value in contributing.

**Pseudocode:**

```python
# Initial state
round_number = 1
def decide_action(n, m, k, history):
    if round_number == r:
        return 'D'
    
    if round_number == 1:
        return 'D'
        
    # Get cooperators from last round
    last_round_c = history[-1].cooperators
    
    # Free-riding logic
    if last_round_c >= m:
        return 'D'
    
    # Conditional cooperation logic
    deficit = m - last_round_c
    if deficit == 1:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Threshold volatility:** If multiple players independently switch to C and the total count $N_C$ exceeds $m$, the strategy defaults to D in the next round to maximize individual gain.
*   **Constant Defection:** If the system observes consistent defection ($N_C < m-1$), it remains in state D, minimizing individual loss.
*   **Non-responsiveness:** If opponents do not adapt to your cooperation, the strategy reverts to total defection to preserve the endowment.
'''

description_SELFISH_19 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat with Defection Bias**

This strategy prioritizes securing the reward ($k$) only when necessary, while defecting whenever the threshold ($m$) can be met without personal contribution.

### State Variables
- $C_{obs, t}$: Number of cooperators observed in round $t$.
- $m$: Minimum cooperators needed.
- $k$: Reward factor.

### Decision Rules (Round $t$)

**Round 1:**
- If $k > 1$, play $C$. 
- If $k \le 1$, play $D$.

**Round $t$ (where $1 < t \le r$):**
Let $prev\_coop = C_{obs, t-1}$.

1. **Calculate Necessity:**
   - If the reward $k$ is greater than the cost of contributing (1), the goal is to trigger the threshold $m$.
   - If the previous round had $m$ or more cooperators, you are in a "success" state.
   - If the previous round had fewer than $m$ cooperators, you are in a "failure" state.

2. **Logic Tree:**
   - **Scenario A: You cooperated in $t-1$**
     - If $prev\_coop \ge m+1$: The threshold was met even without you. Play $D$ in round $t$ (freeriding).
     - If $prev\_coop == m$: The threshold was met exactly because of you. Play $C$ in round $t$ to maintain the status quo.
     - If $prev\_coop < m$: The threshold was not met despite your cooperation. Switch to $D$ for round $t$ to punish the lack of collective coordination.

   - **Scenario B: You defected in $t-1$**
     - If $prev\_coop \ge m$: The threshold was met without you. Continue to play $D$ (freeriding).
     - If $prev\_coop == m-1$: The threshold was missed by only one player (you). Play $C$ in round $t$ to attempt to trigger the reward.
     - If $prev\_coop < m-1$: The threshold was missed by a significant margin. Continue to play $D$ (threshold is unlikely to be reached; conserve endowment).

**Final Round ($t = r$):**
- Always play $D$. The incentive to cooperate in the final round to influence future behavior is null; therefore, maximize payoff by keeping the endowment.

### Edge Cases
- **If $k \le 1$:** Always play $D$ for all $r$ rounds. The cost of cooperation (1) exceeds or equals the benefit of the reward, making cooperation strictly dominated by defection.
- **If $m$ is close to $n$:** The threshold is high and likely difficult to achieve. If in any round $C_{obs} < m-1$, switch to $D$ for all remaining rounds, as the collective is unlikely to reach the necessary cooperation level.
'''

description_SELFISH_20 = '''
**Strategy: Threshold-Targeted Conditional Defection**

The strategy relies on a "trigger-threshold" mechanism designed to extract the maximum possible reward ($k$) while minimizing personal cost ($c_i=1$). The core objective is to force opponents to provide the threshold $m$ cooperators without contributing personally whenever possible, while providing the minimum contribution necessary to secure the reward $k$ if the group fails to meet the threshold otherwise.

**Definitions:**
- Let $C_{t-1}$ be the number of cooperators observed in the previous round.
- Let $S_t$ be the "success threshold" for the current round, defined as $S_t = m$.
- If $t=1$, set the default observation $C_{t-1} = m$.

**Decision Rules per Round:**

1. **Calculate Necessity:**
   Evaluate if the group is currently sustaining the threshold $m$ without your contribution.
   If $(C_{t-1} \ge m)$, you act as a "freeloader." Play **D**.
   If $(C_{t-1} < m)$, you act as a "conditional contributor." Evaluate if your contribution is potentially pivotal. Play **C** if $(C_{t-1} = m - 1)$, otherwise play **D**.

2. **Last Round Adjustment:**
   In round $r$, maximize payoff regardless of future rounds.
   If $(C_{r-1} \ge m)$, play **D**.
   If $(C_{r-1} = m - 1)$, play **C** to secure the reward $k$.
   If $(C_{r-1} < m - 1)$, play **D**; contributing alone or in a small group cannot reach the threshold $m$, making the contribution a wasted cost.

**Pseudocode:**

```python
def decide_action(t, r, n, m, k, C_prev):
    # Determine the number of cooperators needed for threshold
    threshold_met_previously = (C_prev >= m)
    pivotal_position = (C_prev == m - 1)

    if t == r:
        # Final round logic: ignore long-term signaling, focus on threshold
        if pivotal_position:
            return "C"
        else:
            return "D"
            
    else:
        # Standard rounds: exploit cooperation if threshold met
        if threshold_met_previously:
            return "D"
        elif pivotal_position:
            return "C"
        else:
            # Group is too far from threshold; save endowment
            return "D"
```

**Edge Case Handling:**
- **Round 1:** Since there is no $C_{t-1}$, assume the group is at the threshold ($C_0 = m$). This initiates the strategy with a Defect action to test if others are naturally cooperative.
- **Systemic Failure:** If the group fails to hit $m$ for three consecutive rounds despite you playing **C**, switch to permanent **D** for all remaining rounds, as the group is unwilling or unable to coordinate.
'''

description_SELFISH_21 = '''
**Decision Rules:**

1. **Initial Round (Round 1):** Play **D** (Defect). This establishes a baseline and prevents immediate exploitation.

2. **Subsequent Rounds (t > 1):** Let $N_{c, t-1}$ be the number of cooperators observed in the previous round.
   * If $N_{c, t-1} < m$: Play **D**.
   * If $N_{c, t-1} \ge m$: 
     * If the probability of triggering the threshold ($m$) with my own contribution is unnecessary (i.e., if $N_{c, t-1} > m$), play **D**.
     * If the threshold was met exactly by others ($N_{c, t-1} = m$ and I defected, or $N_{c, t-1} = m-1$ and I played C), execute the **Threshold-Critical Condition**:
       * Play **C** only if the expected return from the next round is higher than the guaranteed return of defecting, conditioned on the stability of the group. If the group shows a history of volatility (e.g., $N_c$ oscillates above and below $m$), revert to **D** to minimize losses.
       * If $k > 1$, play **C** if and only if $N_{c, t-1} = m-1$. This strategy attempts to provide the minimal contribution to "buy" the reward $k$ while others are already contributing. 

3. **Final Round (Round r):** Play **D** unconditionally. There is no future round to incentivize reciprocity or punish deviations, making any contribution purely a loss of the endowment.

**Handling Edge Cases:**

* **Unstable Cooperation:** If the group's cooperation count $N_c$ is inconsistent (i.e., $N_c$ alternates between $>m$ and $<m$ over the last 3 rounds), default to **D** regardless of the threshold status, as the group is unreliable.
* **Low Threshold ($m$ is small):** If $m \le n/2$, the strategy defaults to **D** because the likelihood of free-riding is maximized.
* **High Reward ($k \gg 1$):** If $k$ is sufficiently high such that $k > 1$, the strategy prioritizes playing **C** only when $N_{c, t-1} = m-1$ (the "tipping point"), but defects immediately if $N_{c, t-1} \ge m$ (to free-ride on the already successful coalition).
* **Observed Defection:** If the group fails to meet the threshold for two consecutive rounds, assume the population is composed of defectors and play **D** for all remaining rounds to prevent wasted contributions.
'''

description_SELFISH_22 = '''
### Strategy: Conditional Threshold Optimization

**1. Definitions and Initialization**
*   **Threshold Requirement:** Let `m` be the number of cooperators required to trigger the reward `k`.
*   **Target Contribution:** To maximize personal payoff, the optimal state is for exactly `m` players to cooperate. If you are one of the `m` cooperators, you receive `k`. If you are not one of the `m` cooperators (meaning you defect), you receive `1 + k`.
*   **Selfish Objective:** You prefer to be a free-rider (Defect) if the threshold `m` is met by others. If the threshold is not being met, you must determine if your individual contribution can tip the group into meeting it.

**2. Decision Rules**
Let `C_obs` be the number of cooperators observed in the previous round.
Let `n` be the total number of players.

*   **Round 1:** Play **Defect (D)**. This establishes a baseline of the group’s inherent cooperation level without committing your own resources prematurely.

*   **Subsequent Rounds:**
    *   **Scenario A: If `C_obs >= m`:** Play **Defect (D)**. The threshold is already being met without your contribution. Your contribution `C` would yield `k`, but playing `D` yields `1 + k`. Free-ride.
    *   **Scenario B: If `C_obs == m - 1`:** Play **Cooperate (C)**. You are the "pivotal" player. If you play `C`, the threshold `m` is met. Your payoff is `k`. If you play `D`, the threshold is not met, and your payoff is `1`. Since `k > 1` (based on parameters), `k > 1` holds, making `C` the profit-maximizing choice.
    *   **Scenario C: If `C_obs < m - 1`:** Play **Defect (D)**. The group is far from the threshold. Your individual contribution is insufficient to trigger the reward `k`. Therefore, playing `C` results in `0` (or `k` if you somehow triggered it, which you cannot), while playing `D` results in `1`. Since you cannot reach the threshold alone or with your single contribution, preserve your endowment.

**3. Edge Cases and Termination**
*   **Last Round (Round `r`):** Always play **Defect (D)** regardless of history. There is no future round for the group to learn from your cooperation or for the reward `k` to incentivize future behavior. The dominant strategy in a finite game with no reputation-building is defection.
*   **Consistency Check:** If `C_obs` varies significantly round-to-round, prioritize the most recent round's observation. If the group is unstable, treat `C_obs` as the average number of cooperators over the last three rounds, rounded down.
*   **Tie-breaking (if `C_obs` equals `m` exactly):** If the previous round showed exactly `m` cooperators and you were one of them (or if you suspect the group is volatile), switch to **Defect (D)**. This tests whether the threshold can be met without your input. If the next round shows `m-1` cooperators, revert to Scenario B in the following round.
'''

description_SELFISH_23 = '''
The strategy utilizes a "threshold-triggering conditional cooperation" approach, prioritizing defection unless evidence suggests that cooperative threshold maintenance is necessary to secure the reward *k* for oneself. The core mechanism involves playing Defect (D) by default, while observing the total count of cooperators (C_count) to identify the minimum viable cooperation required for the threshold *m*.

### Decision Rules

1.  **Initialization:** In the first round, play Defect (D).
2.  **Threshold Analysis:** Maintain a rolling estimate of the "Cooperation Threshold Requirement." Let *C_opp* be the number of cooperators among the other $n-1$ players in the previous round.
    *   If your action was D and *C_opp* ≥ *m*: You successfully free-rode. Continue to play D.
    *   If your action was D and *C_opp* = *m*-1: You are a "pivotal" player. Playing C will trigger the reward. Evaluate the expected net gain: If *k* - 1 > 0, switch to C. If *k* - 1 ≤ 0, continue to play D.
    *   If your action was D and *C_opp* < *m*-1: The current group is failing to reach the threshold regardless of your input. Continue to play D to maximize your private endowment.
    *   If your action was C and *C_opp* + 1 ≥ *m*: The threshold was met. You may have contributed unnecessarily. Switch to D in the next round to test if the group sustains *m* without your contribution.
    *   If your action was C and *C_opp* + 1 < *m*: The threshold was not met. Your contribution was wasted. Switch to D in the next round.

### Pseudocode Logic

```
// Variables
last_action = D
C_count = number of cooperators observed in previous round
my_contribution = 1 if last_action == C else 0
others_cooperated = C_count - my_contribution

if round == 1:
    action = D
else:
    if others_cooperated >= m:
        action = D // Successfully free-riding
    else if others_cooperated == m - 1:
        if k > 1:
            action = C // Become the pivotal player to secure reward
        else:
            action = D // Threshold reward insufficient to cover cost of C
    else:
        action = D // Group is too uncooperative to justify contribution
```

### Edge Cases and Adjustments

*   **Final Round ($r$):** Regardless of history, if your payoff calculation for round $r$ indicates that playing D results in 1 (with or without the reward) and playing C results in -1 + *k*, play C if and only if *k* > 2, otherwise play D. If the total number of cooperators in the previous round was exactly *m*-1, play C to secure the reward if *k* > 1. If the group is significantly below the threshold ($C_{opp} < m-1$), play D.
*   **Drift Detection:** If the group behavior shifts from cooperation to defection across multiple rounds, the strategy reverts to D, treating the collective as "failed" to preserve individual endowment.
*   **The "Pivot" Loop:** If you switch to C to hit the threshold and the subsequent round shows *C_opp* ≥ *m*, immediately switch to D in the next round to verify if your contribution is still required or if others are now carrying the burden. This minimizes unnecessary contributions.
'''

description_SELFISH_24 = '''
Let `my_contributions` be the history of your own actions, `others_contributions` be the history of total contributions by others, `c_prev` be the number of cooperators in the previous round, and `round_num` be the current round index.

**Strategy: Threshold-Conditional Greed**

In the first round, play **D**. This establishes a baseline of selfishness and minimizes risk, as you cannot predict the threshold-meeting behavior of anonymous others.

For all subsequent rounds `round_num` > 1:

1.  **Calculate the Threshold Gap:** Let `g = m - (number of others who cooperated in the previous round)`. This represents how close the group was to the threshold without your help.
    *   If `g <= 0`, the threshold was met by others alone. Play **D**.
    *   If `g == 1`, the threshold was missed by exactly one person. Play **C**. This is the "Pivotal Cooperator" state, where your contribution creates the reward `k` that exceeds the cost of contribution (since `k > 1`).
    *   If `g > 1`, the group is far from the threshold. Play **D**. Coordination is unlikely, and carrying the group is inefficient.

2.  **Last Round Exception:** Regardless of the previous round's outcome, play **D** in the final round `r`. Since there are no future rounds to incentivize others to cooperate, the marginal utility of attempting to reach the threshold is purely defined by the current round's payoff, and defecting is the dominant strategy to capture the endowment `1` plus any potential reward `k` without paying the cost `1`.

**Pseudocode:**

```python
def get_action(round_num, r, m, c_prev, others_cooperated_prev):
    # Rule 1: Always defect in the final round
    if round_num == r:
        return "D"
    
    # Rule 2: First round baseline
    if round_num == 1:
        return "D"
        
    # Rule 3: Adaptive threshold logic
    # Calculate how many more people were needed to hit m
    # Note: others_cooperated_prev is the number of players excluding self
    needed = m - others_cooperated_prev
    
    if needed == 1:
        return "C" # Pivot to capture reward k
    else:
        return "D" # Free-ride or conserve
```
'''

description_SELFISH_25 = '''
Strategy: Threshold-Responsive Tit-for-Tat with Defection-First Terminality

Decision Rules:

Let $C_{t-1}$ be the number of players who played Cooperate in the previous round, and $S_t \in \{C, D\}$ be your action in round $t$.

1. Initial Action (Round 1): Defect ($D$). 
   - Rationale: In the absence of history, the safest selfish act is to preserve endowment.

2. Subsequent Rounds ($1 < t < r$):
   - If $C_{t-1} \ge m$: Cooperate ($C$).
     - Rationale: Reward-seeking behavior. If the threshold was met, the group is functional; contributing ensures the continuation of the reward $k$.
   - If $C_{t-1} < m$: Defect ($D$).
     - Rationale: The group is failing to meet the threshold. Spending 1 to contribute is a sunk cost with zero return if the threshold remains unmet.

3. Final Round ($t = r$): 
   - Defect ($D$) regardless of history.
     - Rationale: The terminal round offers no incentive for future reciprocity. Defection guarantees the retention of the endowment, which is strictly better than contributing for a reward that cannot influence future rounds.

Edge Cases:

- Threshold Tightness ($m \approx n$): If $m$ is very close to $n$, effectively making cooperation a public good problem, stick to $D$ unless $C_{t-1} \ge m$. If $C_{t-1} < m$ consistently, continue to $D$ throughout.
- Reward Sensitivity ($k \le 1$): If $k \le 1$, the payoff for cooperating ($k-1$) is $\le 0$. In this scenario, play $D$ for all $r$ rounds, as the cost of cooperation exceeds or equals the benefit, making cooperation strictly dominated by defection.
- Fluctuating Thresholds: If the observed $C_{t-1}$ hovers exactly at $m$, prioritize cooperation to lock in the reward. If $C_{t-1}$ is exactly $m-1$, maintain $D$ to preserve the endowment, as the marginal cost of cooperation exceeds the benefit of failing to trigger the reward.
'''

description_SELFISH_26 = '''
The agent employs a Threshold-Triggered Tit-for-Tat strategy calibrated to the minimum cooperation threshold ($m$) and the number of rounds remaining.

### Decision Rules

The agent maintains a variable, $S_{success}$, tracking the frequency of rounds where the threshold $m$ was met.

**Round 1:**
Play Defect ($D$).

**Rounds 2 to $r-1$:**
1. Let $c_{obs}$ be the number of cooperators observed in the previous round.
2. If $c_{obs} \ge m$, the threshold was met. Play Defect ($D$).
3. If $c_{obs} < m$, the threshold was not met. Evaluate the *Defector-Advantage Ratio* ($R_d$):
   * If $(k + 1) > k$, calculate the "risk of cooperation."
   * If the number of cooperators was $m-1$, switch to Cooperate ($C$) to trigger the reward.
   * If the number of cooperators was significantly below $m$ (e.g., $< m-1$), continue to Defect ($D$) to avoid wasting contributions on a guaranteed failure.

**Round $r$ (Final Round):**
Play Defect ($D$) regardless of history. Since there is no future interaction to incentivize, the reward for defecting is strictly higher than cooperating.

### Logic for Success Threshold

*   **Free-Riding Enforcement:** Whenever the threshold $m$ is met, the agent assumes others are already incentivized to cooperate. The agent immediately switches to $D$ to capture the reward $k$ without paying the cost of contribution.
*   **Targeted Contribution:** If the threshold was missed by exactly one player (i.e., $m-1$ players cooperated), the agent plays $C$ in the next round. This is a calculated risk: by paying 1 unit, the agent potentially secures the reward $k$. This is only rational if $k > 1$.
*   **Failure Recovery:** If the threshold was missed by more than one player, the agent remains in $D$. This avoids throwing away the cost of contribution in a state where the group dynamic is failing.

### Pseudocode

```python
def make_decision(round_number, n, m, k, history):
    # Final round: always defect
    if round_number == r:
        return 'D'
    
    # First round: start with defect
    if round_number == 1:
        return 'D'
        
    prev_cooperators = history[-1]['cooperators']
    
    # If the threshold was met, others are carrying the load; free-ride
    if prev_cooperators >= m:
        return 'D'
        
    # If we are exactly one player short of the threshold, provide it
    if prev_cooperators == m - 1:
        return 'C'
        
    # Otherwise, avoid wasting contributions on a failed group effort
    return 'D'
```
'''

description_SELFISH_27 = '''
### Strategy: Threshold-Conditional Tit-for-Tat (TCTT)

The strategy optimizes for the maximum individual payoff by treating cooperation as a conditional investment necessary to trigger the reward $k$, while defecting whenever the threshold $m$ is either already met or unreachable by the player's single contribution.

**Decision Rules:**

Define $C_t$ as the number of cooperators observed in round $t$.

1. **Initialization (Round 1):**
   - Play **Cooperate** if $m \le n/2$ (a "trust-building" threshold).
   - Play **Defect** if $m > n/2$ (prioritizing immediate private endowment, assuming cooperation is unlikely).

2. **Standard Round ($t > 1$):**
   - If the previous round resulted in the reward (i.e., $C_{t-1} \ge m$):
     - **Defect.** Assume the threshold is met without additional effort.
   - If the previous round failed to result in the reward (i.e., $C_{t-1} < m$):
     - If $C_{t-1} = m - 1$: **Cooperate.** This is the "critical tipping point" where your contribution secures the reward for everyone, increasing your payoff from $1$ to $2$ (since the gain $k$ exceeds the cost $1$ when $k > 1$).
     - If $C_{t-1} < m - 1$: **Defect.** The threshold is too far to reach; minimize losses by keeping the endowment.

3. **Terminal Round ($t = r$):**
   - **Defect.** Always defect in the final round regardless of history. There is no future round to punish or reward, and the marginal benefit of securing the reward $k$ (by potentially sacrificing 1 endowment) is strictly dominated by defecting, as defecting yields 1 (or $1+k$ if the group happens to hit the threshold anyway), whereas cooperating yields $k-1$. Since $k > 1$, $1+k > k-1$. Always prioritize keeping the endowment.

**Pseudocode:**

```python
def get_action(round_number, total_rounds, m, n, last_round_cooperators):
    # Terminal round: Always defect
    if round_number == total_rounds:
        return 'D'

    # First round initialization
    if round_number == 1:
        if m <= (n / 2):
            return 'C'
        else:
            return 'D'

    # Adaptive standard logic
    if last_round_cooperators >= m:
        # Reward was met without my contribution, continue defecting
        return 'D'
    elif last_round_cooperators == (m - 1):
        # My contribution will trigger the reward
        return 'C'
    else:
        # Reward is out of reach
        return 'D'
```
'''

description_SELFISH_28 = '''
The strategy adopts a conditional cooperation mechanism designed to maximize individual payoff by exploiting the threshold requirement while minimizing unnecessary contributions. It operates on a "Tit-for-Tat" variant adjusted for the threshold $m$.

**State Variables:**
*   $C_{t-1}$: The total number of players who cooperated in the previous round (including self if applicable).
*   $m$: The minimum number of cooperators required.
*   $r$: Total rounds.
*   $t$: Current round.

**Decision Logic:**

1.  **Initialization (Round 1):**
    Play **Defect (D)**. This tests whether the group naturally meets the threshold $m$ without your contribution.

2.  **Adaptive Phase (Rounds $2$ to $r-1$):**
    *   If total cooperators in the previous round ($C_{t-1}$) was $\ge m$:
        *   If you played **C** in the previous round: Play **Defect (D)**. This tests if the threshold $m$ is maintained without your contribution.
        *   If you played **D** in the previous round: Play **Defect (D)**. The threshold is being met by others; continue free-riding.
    *   If total cooperators in the previous round ($C_{t-1}$) was $< m$:
        *   If your previous action was **D**: Calculate $X = m - C_{t-1}$.
            *   If $X = 1$ (exactly one more cooperator is needed): Play **Cooperate (C)**.
            *   If $X > 1$ (multiple cooperators are missing): Play **Defect (D)**, as contributing alone will not trigger the reward $k$.
        *   If your previous action was **C**: Play **Defect (D)**. The group failed to reach the threshold despite your contribution; contributing again is inefficient.

3.  **Terminal Phase (Round $r$):**
    *   If $C_{r-1} \ge m$: Play **Defect (D)**.
    *   If $C_{r-1} < m$:
        *   If $m - C_{r-1} == 1$: Play **Cooperate (C)**.
        *   Otherwise: Play **Defect (D)**.

**Edge Cases & Logic Exceptions:**
*   **Threshold Excess:** If $C_{t-1} > m$, never contribute ($C$); defect ($D$) regardless of previous history.
*   **Reward Inefficiency:** If $k \le 1$, the strategy defaults to always playing **Defect (D)** for all rounds, as the cost of contribution (1) outweighs the benefit of the threshold reward.
*   **Tie-breaking:** In any scenario where your single contribution determines whether the threshold $m$ is met (specifically when current cooperators = $m-1$), you contribute. If the threshold is already met or impossible to reach, always defect.
'''

description_SELFISH_29 = '''
### Decision Logic

**Round 1:**
Begin by playing **Defect (D)**. This establishes a baseline of selfishness and minimizes early losses if the group fails to coordinate.

**Observation and Adaptation:**
After every round $t$, calculate the number of cooperators observed in the previous round, $O_t$. 

If $O_t \ge m$ (Threshold met):
Continue to play **Defect (D)**. Since the threshold is already being met without your contribution, contributing provides no marginal utility; you secure the payoff of 1 (private retention) plus $k$ (collective reward), resulting in a payoff of $1+k$, whereas cooperating yields $0+k$.

If $O_t < m$ (Threshold not met):
Evaluate the feasibility of reaching the threshold $m$.
1. If $O_t < m - 1$, playing **Cooperate (C)** is insufficient to trigger the reward $k$ (assuming others maintain their current strategy). Therefore, play **Defect (D)** to retain the endowment of 1.
2. If $O_t = m - 1$, you are the "pivotal" player. Playing **Cooperate (C)** will trigger the reward $k$. 
   - Calculate the utility: 
     - Payoff if you defect: $1 + 0 = 1$
     - Payoff if you cooperate: $0 + k = k$
   - If $k > 1$, play **Cooperate (C)**.
   - If $k \le 1$, play **Defect (D)**.

**Final Round (Round $r$):**
Ignore the possibility of reputation building or future reciprocity. Apply the logic derived from the observed $O_{r-1}$ as if the game were continuing, but adjust for the lack of future rounds: play **Defect (D)** regardless of past outcomes, unless $O_{r-1} = m - 1$ and $k > 1$, in which case play **Cooperate (C)**.

**Pseudocode:**

```python
def get_action(r, current_round, m, k, history):
    if current_round == 1:
        return 'D'
    
    previous_cooperators = history[-1]
    
    # Check if threshold was met last round
    if previous_cooperators >= m:
        return 'D' # Already reaping reward, no reason to pay cost
    
    # Check if we are pivotal
    if previous_cooperators == m - 1:
        if k > 1:
            return 'C' # Cooperation is profitable
        else:
            return 'D' # Cooperation is a net loss
            
    # If not pivotal and threshold not met, cooperation is futile
    return 'D'
```
'''

description_SELFISH_30 = '''
### Conditional Threshold Strategy

The strategy aims to maximize cumulative payoff by minimizing contribution costs while incentivizing and capitalizing on collective cooperation only when strictly necessary.

**Decision Rules:**

1.  **Phase 1: Opportunistic Defection (Round 1)**
    *   Default to action D. Do not contribute in the first round to test the natural cooperation level of the population without cost.

2.  **Phase 2: Adaptive Threshold Maintenance (Rounds 2 to r-1)**
    *   Let $N_c$ be the number of cooperators observed in the previous round.
    *   Let $P_d = 1$ if the last action taken was D, else $P_d = 0$.
    *   **Condition A (Free-riding):** If $N_c \ge m + P_d$, play D. If the group is already meeting or exceeding the threshold without your contribution, do not contribute.
    *   **Condition B (Triggering Contribution):** If $N_c < m + P_d$, calculate the "Contribution Requirement":
        *   If $N_c == m - 1$ (exactly one more cooperator needed to hit the threshold), play C.
        *   If $N_c < m - 1$, play D. If the group is failing so significantly that your single contribution will not reach the threshold $m$, do not waste the endowment.

3.  **Phase 3: Terminal Defection (Final Round)**
    *   In the final round $r$, play D regardless of previous outcomes. There are no future rounds to influence, and the cost of contribution outweighs the benefit of securing the final payoff for that round, given that the incentive to cooperate for future rounds is zero.

**Pseudocode:**

```python
def choose_action(round_number, total_rounds, n, m, k, last_round_cooperators, my_last_action):
    # Rule 3: Final round exit
    if round_number == total_rounds:
        return 'D'

    # Rule 1: First round test
    if round_number == 1:
        return 'D'

    # Rule 2: Adaptive Logic
    # Calculate if my previous action 'inflated' the count
    my_contribution_adjustment = 1 if my_last_action == 'C' else 0
    
    # Calculate effective cooperators excluding self
    others_cooperated = last_round_cooperators - my_contribution_adjustment
    
    # Check if threshold is already met by others
    if others_cooperated >= m:
        return 'D'
    
    # Check if my contribution can bridge the gap to m
    if others_cooperated == m - 1:
        return 'C'
    
    # Otherwise, don't waste contribution on a failing threshold
    return 'D'
```
'''

description_SELFISH_31 = '''
### Strategy: Threshold-Conditional Tit-for-Tat (TCTT)

The objective is to maximize cumulative payoff by minimizing personal contributions while ensuring the collective threshold is met just enough times to secure the reward. Since the game is anonymous, the strategy treats the group as a single entity.

**Core Mechanism**
Maintain a local state variable `target_count` initialized to `m`. This value represents the minimum number of cooperators required to trigger the reward. In each round `t`, decide whether to cooperate (`C`) or defect (`D`) based on the observed behavior of the group in round `t-1`.

**Decision Rules**

1.  **Round 1:** Play `D`. This establishes the baseline behavior of the group without sacrificing endowment early.
2.  **Subsequent Rounds (t > 1):**
    *   Let `observed_c` be the number of cooperators in round `t-1`.
    *   **If `observed_c >= m`:** The group has successfully triggered the reward in the previous round. Play `D`. This is the selfish baseline because the threshold was met without your contribution.
    *   **If `observed_c < m`:** The group failed to trigger the reward. You must now determine if your contribution is necessary to reach `m`.
        *   If `observed_c == m - 1`, you are the pivotal player. Play `C`.
        *   If `observed_c < m - 1`, your individual contribution is insufficient to reach the threshold. Play `D` to avoid wasted effort.

**End-Game Heuristic**
In the final round (`t = r`), the incentive for reciprocity vanishes. If the strategy determines that a move of `C` is required based on the logic above, verify the history:
*   If `observed_c < m - 1`, play `D` (contribution is futile).
*   If `observed_c == m - 1`, play `C` (contribution is potentially necessary, though unlikely to be "reciprocated" in future rounds).
*   If `observed_c >= m`, play `D`.

**Pseudocode**

```python
# Initialization
target = m 

# Round 1
Play D

# Rounds 2 to r
for t from 2 to r:
    observed_c = get_observed_cooperators(t-1)
    
    if observed_c >= target:
        Play D
    elif observed_c == target - 1:
        Play C
    else: # observed_c < target - 1
        Play D
```

**Adaptation Logic**
If the group consistently fails to hit the threshold (`observed_c` remains significantly below `m`), the strategy defaults to perpetual defection. If the group consistently hits the threshold, the strategy maintains perpetual defection. The strategy only provides the "pivotal" contribution when it is strictly necessary to bridge the gap between failure and reward, ensuring the minimum possible cost for the maximum possible gain.
'''

description_SELFISH_32 = '''
**Strategy: Conditional Threshold Greed**

The objective is to maximize personal payoff by free-riding on the contributions of others whenever possible, while providing the minimum contribution necessary only when the threshold `m` is at risk of not being met.

**Variables:**
- `count_c_prev`: Number of cooperators in the previous round.
- `last_action`: My action in the previous round (C=1, D=0).
- `threshold`: `m`.
- `my_contribution`: 1 if I contributed, 0 otherwise.

**Decision Rules:**

1.  **First Round:**
    Play **D** (Defect). This establishes a baseline and maximizes immediate gain.

2.  **Subsequent Rounds:**
    Calculate `effective_cooperators` based on the previous round's outcome:
    - If `last_action == 1`, `effective_cooperators = count_c_prev`.
    - If `last_action == 0`, `effective_cooperators = count_c_prev`.

    Apply the following logic:

    *   **Case A: The threshold was met or exceeded by others alone.**
        If `(last_action == 0 AND count_c_prev >= m)` OR `(last_action == 1 AND count_c_prev - 1 >= m)`:
        Play **D**. The reward `k` is secured without your contribution.

    *   **Case B: The threshold was met exactly by your contribution.**
        If `(last_action == 1 AND count_c_prev == m)`:
        Play **D**. Test if the others will contribute enough to maintain the threshold without you.

    *   **Case C: The threshold was not met.**
        If `count_c_prev < m`:
        *   If `(m - count_c_prev) == 1`: Play **C**. You are the pivotal player required to trigger the reward `k` (since `k > 1`, contributing 1 to gain `k` results in a net gain of `k - 1 > 0`).
        *   If `(m - count_c_prev) > 1`: Play **D**. The gap is too large for a single player to fix; attempting to cooperate is a sunk cost.

3.  **Final Round (Round `r`):**
    Regardless of history, play **D**. There is no future round to incentivize others or establish a reputation. Defecting secures the guaranteed private payoff of 1.

**Pseudocode:**

```python
def choose_action(round_number, last_action, count_c_prev, n, m, r):
    if round_number == 1 or round_number == r:
        return 'D'

    # Determine how many others contributed
    others_contributed = count_c_prev - (1 if last_action == 'C' else 0)

    # Strategy: contribute only if you are the swing vote
    if others_contributed == m - 1:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_5 = '''
**Strategy: Threshold-Tit-for-Tat with Forgiveness and Decay**

This strategy models the game as a coordination problem where the objective is to reach the threshold $m$ while minimizing individual contribution costs.

### 1. Initialization
In Round 1, adopt a "Cautious Proposer" stance. Play **Cooperate (C)** with probability $p = m/n$. This signals a willingness to cooperate while minimizing the initial risk of wasted contribution.

### 2. Decision Rules (Rounds 2 to $r$)
In every subsequent round $t$, calculate the contribution status of the previous round ($t-1$):

*   **Case A: Threshold Met ($\sum c_{j, t-1} \ge m$)**
    *   If you played C in $t-1$: Continue to play **Cooperate (C)**. Maintain the cooperative equilibrium.
    *   If you played D in $t-1$: Switch to **Cooperate (C)**. This acknowledges that the collective goal is being met and re-establishes participation.

*   **Case B: Threshold Failed ($\sum c_{j, t-1} < m$)**
    *   If you played C in $t-1$:
        *   If the number of other cooperators was $\ge m-1$ (you were the marginal player who could have tipped the balance): Switch to **Defect (D)**. The group is under-performing; do not waste resources.
        *   If the number of other cooperators was $< m-1$: Switch to **Defect (D)**. The collective effort is insufficient; retreat to safety.
    *   If you played D in $t-1$: Continue to play **Defect (D)**. Wait for the aggregate cooperation level to rise before re-engaging.

### 3. Edge Cases and Refinements

*   **The "Final Rounds" Adjustment:**
    Starting at round $t = r - \lfloor n/m \rfloor$, transition to a pure **Defect (D)** strategy regardless of previous outcomes. In a finitely repeated game without communication, the incentive to free-ride increases as the horizon approaches zero. This prevents exploitation in the final moves.

*   **Recovery and Forgiveness:**
    If the strategy is in a D-state and the collective cooperation count suddenly rises to $\ge m$ in a round where you played D, do not defect in the following round. Immediately switch to **Cooperate (C)** in round $t+1$. This "forgiveness" mechanism prevents deadlock and allows the strategy to capitalize on emerging cooperative norms.

*   **The "Under-contributor" Trap:**
    If in any round $t$, the total number of cooperators equals exactly $m$ and you played D, you successfully free-rode. In round $t+1$, maintain **Defect (D)**. Continue defecting until the observed cooperation level drops below $m$, at which point re-enter the cycle at the Initialization phase to test the market again.
'''

description_SELFINTERESTED_6 = '''
The strategy follows a "Threshold-Conditional Reciprocity" model, designed to maximize individual payoff by balancing free-riding incentives with the necessity of reaching the threshold $m$.

### Strategy Parameters
*   Let $H_t$ be the history of cooperators observed in round $t$.
*   Let $S_t$ be the number of cooperators observed in the previous round.
*   Let $C_{target}$ be the target number of cooperators to ensure the threshold is met, defined as $C_{target} = m$ if you defect, or $m-1$ if you cooperate.

### Decision Rules
For any round $t$:

1.  **Initialization (Round 1):**
    Play C. This establishes a baseline of cooperation to test the propensity of other players to cooperate.

2.  **Adaptive Response (Rounds 2 to $r-1$):**
    *   **Case A (Threshold Met):** If $S_{t-1} \ge m$:
        *   If $S_{t-1} > m$, you have "slack." Switch to D to maximize personal utility while keeping the threshold met.
        *   If $S_{t-1} = m$, maintain C. You are a necessary component of the success.
    *   **Case B (Threshold Not Met):** If $S_{t-1} < m$:
        *   If the shortfall is small (e.g., $S_{t-1} = m-1$), maintain C, hoping others realize the threshold was narrowly missed and will switch.
        *   If the shortfall is large (e.g., $S_{t-1} \ll m$), switch to D. If the group is unwilling to coordinate, the cost of contribution is wasted.

3.  **Terminal Phase (Final Round $r$):**
    *   If the cumulative payoff of C is less than the cumulative payoff of D based on the observed trend of the last three rounds, play D.
    *   If there is a reasonable statistical probability ($> 50\%$) that playing C will push the group from $m-1$ to $m$, play C. Otherwise, play D to avoid the cost of unilateral contribution in the final round.

### Logic
*   **The "Slack" Principle:** The strategy prioritizes D whenever the aggregate observation indicates the threshold $m$ is safe without your contribution. This captures the free-rider surplus ($1 > 0$).
*   **The "Criticality" Principle:** The strategy defaults to C only when necessary to meet the threshold or when the group has demonstrated a high likelihood of reaching $m$ collectively.
*   **Observation Limitation:** Because players are anonymous, this strategy cannot punish specific defectors. It treats the group as a single aggregate entity, adjusting cooperativeness based on the collective signal (success or failure). It ignores individual identities, focusing entirely on the observed count $S_t$.
'''

description_SELFINTERESTED_7 = '''
The strategy employs a "Conditional Threshold Trigger" approach designed to maximize the likelihood of the reward $k$ while minimizing the cost of cooperation in scenarios where the threshold is either unreachable or already satisfied.

**Core Variables:**
- `last_round_cooperators`: Total number of players who chose C in the previous round.
- `my_history`: A list of actions taken by the self in previous rounds.
- `threshold_gap`: The number of additional cooperators required to meet $m$ ($m - \text{last_round_cooperators}$).

**Decision Logic:**

1. **Initialization (Round 1):**
   Choose C. Starting with C signals a willingness to cooperate, which is necessary to establish the possibility of reaching the threshold $m$ in subsequent rounds.

2. **Subsequent Rounds (2 through $r$):**
   Evaluate the `last_round_cooperators` (let this be $x$):
   - If $x \geq m$:
     Choose D. Because the reward $k$ is binary and non-exclusive, if the threshold was met in the previous round, the collective behavior is sufficient. Defecting allows the capture of the reward plus the private endowment. If the group sustains cooperation, the reward continues; if they drop, the logic reverts.
   - If $x = m - 1$:
     Choose C. You are the marginal player necessary to secure the reward $k$. This is the highest utility state where your action directly determines the collective payoff.
   - If $x < m - 1$:
     Choose D. If the group is significantly failing to meet the threshold, investing the endowment is irrational because the cost is incurred without the guarantee of the reward $k$. Defecting preserves the private endowment.

3. **Termination (Round $r$):**
   Choose D. In the final round, there is no future interaction to incentivize, and the cost of contribution is never recouped. Even if $m-1$ players cooperated previously, defecting in the final round captures both the endowment and the reward (if others continue to cooperate), or simply preserves the endowment (if others defect).

**Pseudocode:**

```python
def decide_action(round, last_round_cooperators, n, m, k):
    if round == r:
        return 'D'
        
    if round == 1:
        return 'C'
        
    # Logic for intermediate rounds
    if last_round_cooperators >= m:
        return 'D'
    elif last_round_cooperators == m - 1:
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_8 = '''
**Strategy: Threshold-Responsive Trigger (TRT)**

The TRT strategy operates on the principle of conditional cooperation, aiming to contribute only when the group demonstrates a capacity for coordination while defecting when the group fails to meet the threshold or when individual exploitation is more profitable than the collective outcome.

**Decision Rules**

1. **Round 1 (Initialization):**
   - Play **Cooperate (C)** with probability $P_c = m/n$. This establishes a baseline level of cooperation that signals intent to participate in the collective reward while hedging against total defection.

2. **Subsequent Rounds ($t > 1$):**
   Let $C_{t-1}$ be the total number of players who cooperated in the previous round.
   - **Case A: Threshold Met ($C_{t-1} \ge m$):**
     - If your action in $t-1$ was **C**, play **C**.
     - If your action in $t-1$ was **D** and you received a payoff of $1+k$, continue playing **D** (Exploitation phase).
     - If your action in $t-1$ was **D** and you received a payoff of $1$, play **C** (Shift to cooperative equilibrium to ensure threshold is met).
   - **Case B: Threshold Not Met ($C_{t-1} < m$):**
     - If $t \le (r - \text{buffer})$, play **D** for one round to reset expectations, then switch to **C** for one round to attempt to restart the collective effort.
     - If $t > (r - \text{buffer})$, play **D** exclusively for the remainder of the game.

**Buffer Calculation**
The buffer represents the final rounds where the risk of defection outweighs the potential gains of a restarted collective effort. Set $\text{buffer} = \lceil n/m \rceil$.

**Pseudocode Logic**

```python
def decide_action(round, history):
    if round == 1:
        return 'C' if random() < (m/n) else 'D'
    
    prev_cooperators = history[round-1].total_C
    my_last_action = history[round-1].my_action
    
    # Check if threshold was met
    threshold_met = prev_cooperators >= m
    
    # Final phase: maximize payoff by defecting
    if round > (r - ceil(n/m)):
        return 'D'
        
    if threshold_met:
        if my_last_action == 'C':
            return 'C' # Maintain stability
        else:
            # Exploitation check: did I get the reward anyway?
            # If so, keep defecting. If not, join to ensure it happens.
            return 'D' if (prev_cooperators >= m) else 'C'
    else:
        # If threshold not met, restart attempt unless too late
        return 'C' if (round % 2 == 0) else 'D'
```

**Edge Case Handling**
- **Last Round ($t=r$):** Always play **D**. Since there are no future rounds to sustain a reputation or punish opponents, maximizing the single-round payoff is the optimal self-interested move.
- **Exploitation Trigger:** If a history indicates the threshold is consistently met with fewer than $n$ cooperators, the strategy permanently switches to **D** to capture the "free-rider" premium ($1+k$) over the cooperative payoff ($k$).
- **Initialization Failure:** If $C_1 < m$, the strategy assumes the group is non-cooperative and defaults to **D** for two-thirds of the remaining game duration to prevent endowment loss, attempting one final recovery round at $t = r - \text{buffer}$.
'''

description_SELFINTERESTED_9 = '''
**Strategy: Threshold-Adaptive Reciprocity (TAR)**

This strategy operates on the principle of conditional cooperation, maintaining participation only when the collective behavior justifies the personal investment.

**Decision Rules**

In any round $t$, define $C_{t-1}$ as the total number of players who cooperated in the previous round.

1.  **Initialization:** In round $t=1$, play **Cooperate (C)**.

2.  **Adaptive Response:** In rounds $t \in \{2, \dots, r\}$, the decision to play $C$ or $D$ depends on the outcome of $t-1$:

    *   **If $C_{t-1} \geq m$:** The collective threshold was met successfully. Play **Cooperate (C)**. This reinforces the cooperative norm and maintains the reward $k$ for the current round.
    *   **If $C_{t-1} < m$:** The collective threshold failed. Play **Defect (D)**. This minimizes personal loss (retaining the endowment) when the collective fails to deliver the reward.

3.  **Recovery Protocol:** If you played $D$ in round $t$ because the previous round failed ($C_{t-1} < m$), return to **Cooperate (C)** in the next round $t+1$ if and only if you observe that the collective effort is potentially shifting. Specifically, if $C_{t-1} \geq m-1$ (the collective was only one short of the threshold), play **Cooperate (C)** to attempt to nudge the group back over the threshold. If $C_{t-1} < m-1$, continue to play **Defect (D)** for one additional round to signal dissatisfaction, then revert to **Cooperate (C)** in the following round to probe for cooperation again.

**Handling Edge Cases**

*   **Final Round ($t=r$):** Play **Defect (D)** regardless of the previous round's outcome. Since there is no future utility to be gained from maintaining a reputation or incentivizing others, the dominant strategy is to maximize the final round payoff by keeping the endowment.
*   **Threshold volatility:** If $C_{t-1}$ consistently fluctuates just below $m$, oscillate between $C$ and $D$. This avoids "sucker" status (continually contributing without receiving the reward) while remaining open to coordination if the group stabilizes.
*   **Uncertainty/Noise:** Treat any observed count $C_{t-1}$ as absolute. Do not attempt to infer malice or error; respond solely to the aggregate count to optimize the expected value of the round.
'''

description_SELFINTERESTED_10 = '''
**Strategy: Threshold-Responsive Tit-for-Tat (TR-TFT)**

**1. Initial Strategy (Round 1)**
In the first round, play Cooperate (C) with probability `p = m / n`. This establishes a baseline level of contribution proportionate to the required threshold, signaling a willingness to participate in the collective effort without over-committing.

**2. Decision Rule (Subsequent Rounds `t > 1`)**
Let `N_t-1` be the number of cooperators observed in the previous round.

*   **Case 1 (Threshold Success):** If `N_t-1 >= m`:
    *   If you played C in the previous round, continue to play C (maintain the successful coalition).
    *   If you played D in the previous round, play D (exploit the fact that the threshold is met without your contribution).

*   **Case 2 (Threshold Failure):** If `N_t-1 < m`:
    *   If the number of cooperators was `m - 1` (the threshold was narrowly missed), play C. This attempts to nudge the collective effort over the boundary by providing the critical missing contribution.
    *   If the number of cooperators was significantly below `m` (e.g., `N_t-1 <= m - 2`), play D. This minimizes losses in a non-functional collective where cooperation is insufficient to trigger the reward `k`.

**3. Terminal Rounds (Last 2 Rounds)**
In the final two rounds of the game, switch to Defect (D) regardless of previous history. Because there is no future interaction to incentivize cooperation from opponents, the dominant strategy is to capture the private endowment while potentially benefiting from any residual cooperation generated by other players.

**4. Edge Cases**
*   **Persistent Defection:** If the group fails to reach `m` cooperators for three consecutive rounds despite your attempts to nudge, play D for the remainder of the game. Assume the population is incapable of collective action and switch to pure self-interest.
*   **Excessive Cooperation:** If `N_t-1 > m`, play D. If the coalition is stable enough that `m` cooperators are reached even without you, there is no marginal benefit to contributing.

**Pseudocode Summary:**
```python
def get_action(round, N_prev, my_last_action):
    if round == r or round == r - 1:
        return D
    
    if round == 1:
        return C if random() < (m / n) else D
    
    if N_prev >= m:
        return my_last_action
    
    if N_prev == m - 1:
        return C
    
    return D
```
'''

description_SELFINTERESTED_11 = '''
**Strategy: Conditional Threshold-Triggered Contribution**

This strategy relies on establishing a threshold-based reputation while protecting endowment during periods of low cooperation. The core principle is "Conditional Reciprocity with a Safety Margin."

**Decision Rules:**

1.  **Initial Phase (Rounds 1–2):** 
    Play Cooperate (C) for the first two rounds to signal intent and gauge aggregate cooperation levels.

2.  **Tracking and Calculation:**
    Maintain a running estimate of the "Cooperation Surplus." Let $S_t$ be the number of cooperators observed in round $t$.
    *   If $S_t \ge m$, the threshold was met.
    *   If $S_t < m$, the threshold was missed.

3.  **Adaptive Play (Round 3 onwards):**
    For round $t > 2$, calculate the average cooperation rate $A_{t-1} = \frac{\sum_{j=1}^{t-1} S_j}{(n-1)(t-1)}$.

    *   **Scenario A (High Cooperation):** If $A_{t-1} \ge \frac{m}{n-1}$, continue to play C.
    *   **Scenario B (Marginal Cooperation):** If $\frac{m-1}{n-1} < A_{t-1} < \frac{m}{n-1}$, play C. This is a "support" move to keep the group aggregate above the threshold $m$.
    *   **Scenario C (Low Cooperation):** If $A_{t-1} \le \frac{m-1}{n-1}$, play Defect (D). The group is failing to coordinate reliably; minimize losses by retaining the endowment.

4.  **Resumption Rule:**
    If playing D due to Scenario C, periodically test the group. Every 3 rounds of D, play C once to check if the aggregate cooperation level has risen back above the threshold requirement. If the result of this check $S_t \ge m$, return to the Adaptive Play logic starting at Scenario B. If $S_t < m$, revert to D.

5.  **Final Round (Round $r$):**
    If the current strategy is C, play C. If the current strategy is D, play D, unless $\sum_{j=1}^{r-1} S_j$ indicates that a single additional cooperator (yourself) is mathematically necessary to hit the threshold $m$ that was missed in the majority of previous rounds, in which case play C.

**Pseudocode Logic:**

```
if t <= 2: return C

# Calculate observed cooperation of opponents
# Opponents are n-1 players
avg_opp_coop = (sum(previous_cooperators) / (n-1)) / (t-1)

if avg_opp_coop >= (m / (n-1)):
    return C
elif avg_opp_coop > ((m-1) / (n-1)):
    return C
else:
    # Check if we should test for recovery
    if (t % 3 == 0):
        return C
    else:
        return D

if t == r:
    # Last-ditch effort if threshold is within reach
    if observed_opponents_last_round == m - 1:
        return C
    else:
        return current_strategy
```
'''

description_SELFINTERESTED_12 = '''
**Threshold-Triggered Conditional Cooperation (TTCC)**

The strategy operates on the principle of conditionally contributing only when necessary to ensure the threshold is met, while prioritizing the immediate payoff advantage of defection.

**Decision Rules:**

Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $M_t$ be the number of cooperators needed by me in the current round to reach the threshold $m$.
- If $t=1$: Play **D**.
- If $t > 1$:
    - Calculate $M_t$:
        - If $C_{t-1} \ge m$, set $M_t = 0$. (The threshold is already being met comfortably).
        - If $C_{t-1} = m-1$, set $M_t = 1$. (Only one more cooperator is needed).
        - If $C_{t-1} < m-1$, set $M_t = m - C_{t-1}$. (The project is failing).
    - If $M_t = 0$: Play **D**.
    - If $M_t = 1$: Play **C** with probability $p$, where $p$ is calibrated to the observed cooperation history (e.g., $p = \frac{C_{t-1}}{n-1}$), attempting to hit the threshold exactly without over-contributing.
    - If $M_t > 1$: Play **D**.

**Handling Edge Cases:**

- **First Round:** Always play **D** to establish a baseline of opponent behavior without incurring unnecessary contribution costs.
- **Last Round ($t=r$):** Regardless of history, if the expected contribution probability of others is insufficient to reach $m$ without my help, play **D**. If $m$ is within reach with one's own contribution, cooperate only if the collective reward $k$ outweighs the cost of defection (which is always 1). Specifically, if $C_{r-1} = m-1$, play **C**; otherwise, play **D**.
- **The "Free Rider" Threshold:** If $C_{t-1} \ge m$, the group is successfully coordinating. Switch immediately to **D** to maximize personal payoff, as the threshold is secure without further intervention. 
- **The "Deadlock" Scenario:** If $C_{t-1} \ll m$ consistently, cease all cooperation and play **D** for the remainder of the game, as attempting to rescue a failing project incurs a guaranteed cost of 1 with a low probability of receiving reward $k$.

**Objective Logic:**

The strategy minimizes "over-contribution" (paying the cost of $C$ when $m$ is already met) and avoids "wasted contribution" (paying the cost of $C$ when the group is failing to reach $m$ regardless). It exploits the fact that $D$ is a strictly dominant strategy in a single round if one's own contribution is not the pivot point for reaching $m$, while engaging in "threshold-only" cooperation to secure the reward $k$ when the group is on the verge of success.
'''

description_SELFINTERESTED_13 = '''
To maximize long-term payoff, prioritize Defecting (D) unless there is evidence that cooperating (C) significantly increases the probability of hitting the threshold $m$ in a way that outweighs the cost of cooperation over the remaining rounds. Given that $D$ is the dominant strategy in every single round, the only rational deviation is a "Conditional Threshold Strategy" designed to punish non-cooperation or incentivize groups that are on the cusp of the threshold.

### Decision Rules:

1.  **Round 1:** Play **Defect (D)**. Since no history exists, defecting is the risk-neutral strategy.
2.  **Subsequent Rounds:** Let $C_{t-1}$ be the number of cooperators observed in the previous round.
    *   **Trigger Condition (Cooperate):** If ($m - 1 \leq C_{t-1} < m$) AND ($r - t \geq 1$), then play **Cooperate (C)**. 
        *   *Logic:* This scenario indicates the group is exactly one person short of the reward. By playing C, you convert a state where *no one* gets the reward $k$ into a state where *everyone* gets the reward $k$. Since you gain $k - 1$ (the reward minus the cost), this is rational if $k > 1$.
    *   **Observation Check (Defect):** If $C_{t-1} \geq m$, play **Defect (D)**.
        *   *Logic:* If the group already hits the threshold without your contribution, contributing C yields a payoff of $k - 1$ while D yields $k$. Defecting is strictly better.
    *   **Incentive Check (Defect):** If $C_{t-1} < m - 1$, play **Defect (D)**.
        *   *Logic:* If more than one person needs to switch for the threshold to be met, your single contribution is insufficient to trigger the reward. Cooperating here is a sunk cost with no return.
3.  **Last Round ($t = r$):** Always play **Defect (D)**.
    *   *Logic:* There is no future round to incentivize or punish; the threshold reward cannot be influenced by future cooperation, and the immediate payoff is maximized by defecting.

### Edge Cases:
*   **If $k \leq 1$:** The strategy defaults to **Defect (D)** in every round regardless of conditions, as the cost of cooperation (1) exceeds the potential reward ($k$).
*   **Tie-breaking:** If the logic dictates a choice between C and D due to ambiguous history or simultaneous calculation, default to **Defect (D)**.
'''

description_SELFINTERESTED_14 = '''
The strategy utilizes a conditional "Win-Stay, Lose-Shift" logic centered on the cooperative threshold `m`, combined with a pessimistic probabilistic assessment of the group's contribution level.

Define `T` as the current round and `R` as the total rounds. Let `C_prev` be the number of cooperators observed in the previous round.

**Decision Rules:**

1.  **Initialization (Round 1):** Play `C` (Cooperate) if `m/n <= 0.5`. Otherwise, play `D` (Defect). This assumes a baseline probability of cooperation based on the threshold difficulty.

2.  **Iterative Adjustment (Round 2 to R-1):**
    *   If you played `C` last round:
        *   If `C_prev >= m`: You are in a "stable success" state. Maintain `C`.
        *   If `C_prev == m - 1`: You are a "pivotal cooperator." Maintain `C` only if you believe your defection would cause failure. Play `C`.
        *   If `C_prev < m - 1`: Cooperation is far from threshold. Play `D`.
    *   If you played `D` last round:
        *   If `C_prev >= m`: The threshold is being met without your contribution. Continue `D`.
        *   If `C_prev == m - 1`: You can swing the outcome to success. Play `C`.
        *   If `C_prev < m - 1`: The group is uncooperative. Play `D`.

3.  **Terminal Phase (Round R):**
    *   If `C_prev >= m`: Play `D`.
    *   If `C_prev == m - 1`: Play `C`.
    *   If `C_prev < m - 1`: Play `D`.

**Pseudocode:**

```python
def get_action(round_num, last_round_cooperators, my_last_action, n, m):
    # Determine critical status
    # status 1: Success (m or more cooperators)
    # status 2: Pivotal (exactly m-1 cooperators)
    # status 3: Failure (less than m-1 cooperators)

    if round_num == 1:
        return 'C' if (m / n) <= 0.5 else 'D'

    # Check previous outcome
    if last_round_cooperators >= m:
        return 'D' # Free-ride if success is already guaranteed

    if last_round_cooperators == (m - 1):
        return 'C' # Attempt to hit the threshold if one away

    # last_round_cooperators < (m - 1)
    return 'D' # Do not waste resources on unreachable threshold
```

**Edge Case Handling:**
*   **Threshold Unreachable:** If `C_prev` is significantly below `m-1` for consecutive rounds, default to `D` to preserve endowment, ignoring the potential for `C` to influence group norms, as communication is impossible.
*   **Threshold Easily Met:** If `C_prev > m`, prioritize `D` to maximize payoff, as the group is already providing the collective benefit without additional input.
*   **Last Round:** The strategy prioritizes the immediate payoff of `D` unless exactly one additional cooperator is needed to trigger the `k` reward, in which case it switches to `C` for that round only.
'''

description_SELFINTERESTED_15 = '''
### Strategy: Adaptive Threshold-Conditional Cooperation (ATCC)

**Objective**
Maximize total accumulated payoff by incentivizing the collective threshold $m$ to be met while minimizing unnecessary personal contributions.

**State Variables**
- $C_t$: Number of cooperators in round $t$.
- $c_t$: My action in round $t$ ($1$ for C, $0$ for D).
- $T_t$: The total rounds remaining, calculated as $r - (t-1)$.
- $P_t$: Whether the threshold was met in round $t$ ($1$ if $C_t \ge m$, $0$ otherwise).

**Decision Rules**

1.  **Initialization (Round 1):**
    Always play C. This signals a commitment to the group goal and establishes the threshold potential immediately.

2.  **Adaptive Phase (Rounds 2 to $r-1$):**
    Calculate the effective necessity of your contribution based on the previous round's outcome ($C_{t-1}$):
    *   **If $P_{t-1} = 1$:**
        *   *Scenario A: You contributed ($c_{t-1} = 1$):* If $C_{t-1} > m$, play D. You are redundant. If $C_{t-1} = m$, play C to maintain the threshold.
        *   *Scenario B: You defected ($c_{t-1} = 0$):* If $C_{t-1} \ge m$, play D. The group is self-sustaining without you.
    *   **If $P_{t-1} = 0$:**
        *   Play C. The collective failed, and you must attempt to steer the group toward cooperation again.

3.  **Terminal Phase (Round $r$):**
    Regardless of history, always play D. Since there are no future rounds to influence, the opportunity cost of playing C (losing the 1 unit of endowment) cannot be recovered by future cooperation.

**Pseudocode Logic for Round $t$ (where $t < r$):**

```python
if t == 1:
    return C
    
if t == r:
    return D

# Analyze previous round
prev_cooperators = get_cooperators(t-1)
prev_my_action = my_action(t-1)
threshold_met = (prev_cooperators >= m)

if threshold_met:
    # If we met the threshold without me, defect.
    if prev_my_action == C:
        if prev_cooperators > m:
            return D
        else:
            return C # I am critical, must maintain
    else:
        return D # They met it without me, free-ride
else:
    # If we failed, I must contribute to restore the threshold.
    return C
```

**Edge Case Handling**
*   **The "Redundancy" Trap:** If $C_{t-1} > m$ and you contributed, you are wasting resources. The strategy switches you to D to capture the endowment while the group remains above threshold.
*   **The "Recovery" Trigger:** If the group falls below $m$, the strategy forces an immediate return to C, ignoring the previous defection, to restart the virtuous cycle.
*   **Self-Interest constraint:** This strategy ensures that if the group is already efficiently achieving the threshold, you prioritize personal accumulation (D). If the group is failing, you pay the cost (C) to unlock the reward ($k$).
'''

description_SELFINTERESTED_16 = '''
### Strategy: Threshold-Conditional Reciprocity (TCR)

**State Variables:**
*   $T$: Number of rounds remaining ($T = r - t + 1$).
*   $C_{prev}$: Number of cooperators in the previous round.
*   $S$: A "success" flag, initialized to 1. If $C_{prev} < m$, set $S = 0$, else $S = 1$.

**Decision Rules:**

1.  **First Round ($t=1$):** 
    Play **C** if $k > 1$, otherwise play **D**. (This establishes a baseline for cooperation given the positive expected value of the collective reward.)

2.  **Subsequent Rounds ($1 < t < r$):**
    *   If $S=1$: Play **C**. (Maintaining success signals stability.)
    *   If $S=0$: 
        *   Calculate the probability of success in the current round based on the observed $C_{prev}$. 
        *   If $C_{prev} \ge m - 1$: Play **C**. (The group is on the verge of the threshold; marginal contribution is highly likely to trigger the reward $k$.)
        *   If $C_{prev} < m - 1$: Play **D**. (The group is failing significantly; contributing is a sunk cost.)

3.  **Last Round ($t=r$):**
    *   If $S=1$: Play **D**. (With no future rounds to influence, maximize individual payoff by keeping the endowment while relying on the established momentum of the previous successful round.)
    *   If $S=0$: Play **D**. (Without future rounds, the risk of wasted contribution outweighs the low probability of reaching the threshold.)

**Logic:**
*   **Signaling:** By cooperating when the group is close to success ($m-1$), you actively attempt to "pull" the group over the threshold without perpetually subsidizing free-riders when the group is failing.
*   **Exploitation Avoidance:** The transition to defecting when the group is failing ($C_{prev} < m-1$) prevents the loss of your endowment in non-viable rounds.
*   **Terminal Defection:** Since the game has a finite horizon and no future rounds to incentivize, defection is the dominant strategy in the final round to secure the endowment, regardless of previous success.
'''

description_SELFINTERESTED_17 = '''
**Strategy Name: Threshold-Conditional Tit-for-Tat with Defection-Risk Buffering**

**State Variables**
- `cooperators_t`: The number of players who cooperated in round $t$.
- `my_history`: A list of your actions in rounds $1$ to $t-1$.
- `opponent_history`: A list of `cooperators_t` for rounds $1$ to $t-1$.
- `threshold`: $m$.
- `k_value`: $k$.
- `total_rounds`: $r$.

**Decision Logic for Round $t$**

1. **Initial Round ($t=1$):**
   - Play **Cooperate (C)**. 
   - *Rationale:* This signals a willingness to coordinate and tests the collective cooperative capacity without incurring an immediate loss of potential $k$-reward in the first round.

2. **Subsequent Rounds ($t > 1$):**
   - Let `effective_threshold` = $m$ (if you played D in round $t-1$) or $m-1$ (if you played C in round $t-1$).
   - If `opponent_history[t-1]` $\ge$ `effective_threshold`:
     - Play **Cooperate (C)**.
     - *Rationale:* If the group is meeting the threshold without your contribution, continue to facilitate the reward. If you were necessary to meet the threshold, continue to cooperate to maintain the reward.
   - If `opponent_history[t-1]` < `effective_threshold`:
     - Calculate `gap` = `effective_threshold` - `opponent_history[t-1]`.
     - If `gap` == 1 and $k > 1$:
       - Play **Cooperate (C)**. 
       - *Rationale:* If only one more cooperator is needed to trigger the $k$ reward, you effectively "buy" the reward for the group (and yourself) because the return $k$ exceeds the cost of 1.
     - If `gap` > 1 or $k \le 1$:
       - Play **Defect (D)**.
       - *Rationale:* If the group is far from the threshold, the probability of triggering $k$ is low. Minimize losses by keeping the endowment.

3. **Terminal Round ($t = r$):**
   - If $k > 1$ and `opponent_history[r-1]` $\ge m-1$:
     - Play **Cooperate (C)**.
   - Otherwise:
     - Play **Defect (D)**.
     - *Rationale:* In the final round, there is no future incentive for cooperation. Only cooperate if the expected value of the immediate reward $k$ is guaranteed or highly likely by the observed past behavior of others. If $k \le 1$, default to Defect (D) to guarantee the safe payoff of 1.
'''

description_SELFINTERESTED_18 = '''
**Strategy: Adaptive Threshold-Triggered Cooperation**

This strategy relies on a "trigger-and-titrate" mechanism that seeks to establish a minimal coalition sufficient to secure the threshold reward $m$ while minimizing individual contribution costs.

**Decision Variables:**
*   $T_t$: Total cooperators observed in the previous round $t-1$.
*   $Status_t$: The cooperation decision of this player in the current round $t$.
*   $C_{max}$: A counter tracking the maximum number of cooperators observed in any round so far.
*   $Target$: The specific number of cooperators required to meet the threshold, $m$.

**Phase 1: Initial Rounds (Round 1)**
*   Play $C$ (Cooperate). This establishes a baseline contribution to signal cooperative intent and test the willingness of others to participate.

**Phase 2: Adaptive Response (Rounds 2 to $r-1$)**
Calculate $T_{t-1}$ (the number of cooperators in the previous round).

1.  **If $T_{t-1} \geq m$:**
    *   If you played $C$ in the previous round: Play $D$ (Defect). This tests if the group can maintain the threshold without your specific contribution.
    *   If you played $D$ in the previous round: Continue playing $D$.
    *   *Correction Rule:* If the group fails to meet the threshold ($T_t < m$) after you defected while the group was previously meeting the threshold, return to $C$ in the next round.

2.  **If $T_{t-1} < m$:**
    *   If you played $C$ in the previous round: Continue playing $C$. The group is failing to reach the threshold, and your defection would not be compensated by the reward $k$.
    *   If you played $D$ in the previous round: Play $C$. You are attempting to push the aggregate toward the threshold $m$ to unlock the reward $k$.

**Phase 3: Final Rounds ($r$)**
*   If $T_{r-1} \geq m$: Play $D$.
*   If $T_{r-1} < m$:
    *   Calculate the benefit-cost ratio: If $k > 1$, play $C$. If $k \leq 1$, play $D$ (as the reward does not offset the lost endowment).

**Pseudocode Logic:**

```python
def get_action(round, last_round_cooperators, my_last_action):
    if round == 1:
        return 'C'
    
    if round == r:
        if last_round_cooperators >= m:
            return 'D'
        else:
            return 'C' if k > 1 else 'D'
            
    # Standard adaptive logic
    if last_round_cooperators >= m:
        # If threshold met, try to save endowment (Defect)
        return 'D'
    else:
        # If threshold missed, contribute (Cooperate)
        return 'C'
```

**Edge Case Handling:**
*   **Persistent Defection:** If $T_t < m$ consistently for 3 rounds, assume the population is non-cooperative. Default to $D$ for all remaining rounds to minimize endowment loss.
*   **Reward Threshold:** If $k \leq 1$, the payoff $1+k$ for cooperating is equivalent to or less than the payoff $1$ from defecting (given the loss of endowment). In this scenario, play $D$ for all $r$ rounds.
'''

description_SELFINTERESTED_19 = '''
**Strategy: Conditional Threshold Tit-for-Tat (CTT)**

**Decision Rule:**

Define a "Success" as any round where the total number of cooperators ($C_{total}$) is $\ge m$. Define a "Failure" as any round where $C_{total} < m$.

1. **Initialization:** In Round 1, play **Defect (D)**. This tests the baseline contribution level of the population without sacrificing the endowment.

2. **Monitoring Phase (Rounds 2 to $r-1$):**
   *   Calculate the moving average of cooperation: $AVG_C = \frac{1}{t-1} \sum_{j=1}^{t-1} C_{total, j}$.
   *   If $AVG_C < m - 1$ (where $m-1$ is the minimum number of *other* players required for a threshold success): Play **Defect (D)**. The group is insufficiently cooperative to make the $k$ reward worth the $1$ unit investment.
   *   If $AVG_C \ge m - 1$: Play **Cooperate (C)**. The group demonstrates sufficient cooperative capacity to likely achieve the threshold with your help.

3. **Adjustment Phase (The "Greed-Check" edge case):**
   *   If at any point $C_{total, t-1} \ge m + 1$ (the group is cooperating *above* the minimum threshold), switch to **Defect (D)** in round $t$. Because $C_{total} > m$, the threshold is met even if one player drops out; defecting captures both the private endowment and the reward $k$.
   *   If $C_{total, t-1} = m$, remain in **Cooperate (C)** to sustain the threshold.

4. **Terminal Phase (Round $r$):**
   *   Regardless of previous history, play **Defect (D)**. With no future rounds to influence via reputation or reciprocity, the dominant strategy is to capture the endowment. If the group meets the threshold without you, you gain $1+k$. If the group fails, you gain $1$. Cooperating only guarantees a lower outcome ($k$ vs $1+k$ or $0$ vs $1$).

**Pseudocode:**

```python
def decide_action(round, history, n, m, k):
    if round == r:
        return 'D'
    
    if round == 1:
        return 'D'
        
    last_C_total = history[-1].C_total
    avg_C = sum(h.C_total for h in history) / (round - 1)
    
    # Check if group is over-cooperating
    if last_C_total > m:
        return 'D'
        
    # Check if group is viable for cooperation
    if avg_C >= (m - 1):
        return 'C'
    else:
        return 'D'
```
'''

description_SELFINTERESTED_20 = '''
1. **Initialization:**
Start by calculating the "Contribution Deficit" threshold: `d = m - 1`. If you contribute, you help bridge the gap to `m`, but you suffer a payoff loss of 1 (you get `k` instead of `1 + k`).

2. **Round 1 Strategy:**
Play **Defect (D)**. Since there is no history of play, the safest self-interested move is to avoid the cost of contribution while waiting to see if `m` other players are willing to coordinate without your input.

3. **Subsequent Rounds (Adaptive Rule):**
Maintain a rolling memory of the total cooperators observed in the previous round, denoted as `C_prev`.

    *   **Rule A (Trigger Cooperation):** If `C_prev` was exactly `m - 1` in the last round, play **Cooperate (C)**.
        *   *Rationale:* You are the pivotal player. By contributing, you push the total to `m`, unlocking the reward `k` for everyone. While you earn `k` (the reward) instead of `1 + k` (the defect payoff), you successfully trigger the group success condition which otherwise would have failed. If `k > 1`, this is a net gain compared to the default state where the threshold is not met (payoff of 1).

    *   **Rule B (Threshold Stability):** If `C_prev >= m`, play **Defect (D)**.
        *   *Rationale:* The threshold is already being met by others. Defecting allows you to receive the "free rider" payoff (`1 + k`) while the cooperators bear the cost.

    *   **Rule C (Threshold Failure):** If `C_prev < m - 1`, play **Defect (D)**.
        *   *Rationale:* Your single contribution cannot bridge the gap to `m`. Contributing would be a wasted cost of 1.

4. **Final Round Strategy:**
If the current round is `r` (the last round), prioritize **Defect (D)** regardless of the previous round's outcome, unless you observe `C_prev == m - 1` and `k > 1`. If `k > 1` and `C_prev == m - 1`, play **Cooperate (C)** to maximize the final round payoff.

5. **Decision Pseudocode:**

```
// Constants: n, m, k
// State: t (current round), r (total rounds), C_prev (cooperators in t-1)

if t == 1:
    return D

if t > 1 and t < r:
    if C_prev == (m - 1) and k > 1:
        return C
    else:
        return D

if t == r:
    if C_prev == (m - 1) and k > 1:
        return C
    else:
        return D
```
'''

description_SELFINTERESTED_21 = '''
Strategy: Threshold-Contingent Trigger-Tit-for-Tat

1. Initialize `contribution_streak` = 0.
2. In Round 1, play C.
3. For Rounds $t = 2$ to $r-1$:
    * Let $N_{c, t-1}$ be the number of cooperators observed in the previous round.
    * Let $c_{t-1}$ be your own action in the previous round.
    * If $c_{t-1} = C$:
        * If $N_{c, t-1} \geq m$ (assuming you were one of the cooperators, threshold was met), play C.
        * If $N_{c, t-1} < m$ (threshold not met), play D.
    * If $c_{t-1} = D$:
        * If $N_{c, t-1} \geq m$ (threshold was met without you), play D to exploit the free-rider advantage.
        * If $N_{c, t-1} < m$, play C with probability $p = 1 - (N_{c, t-1} / m)$, increasing the likelihood of cooperation as the group approaches the threshold.
4. For the final round ($t = r$):
    * If the average payoff per round across $t=1$ to $r-1$ was greater than 1, play C if $N_{c, r-1} \geq m-1$, otherwise play D.
    * If the average payoff per round was $\leq 1$, play D unconditionally.

Edge Case Rules:
* If $N_{c, t-1} = n$ (all cooperated), play C regardless of strategy.
* If $N_{c, t-1} = 0$, play D.
* If $t=r$ and previous cooperative behavior was consistently high ($N_{c, t-1} \geq m$ for the majority of rounds), play C to maximize final yield. Otherwise, play D.
'''

description_SELFINTERESTED_22 = '''
**Strategy: Threshold-Adaptive Trigger (TAT)**

The strategy operates based on the observed number of cooperators from the previous round to determine the probability of cooperating in the current round. Let $C_{t-1}$ be the number of cooperators observed in the previous round, and $P(C_t)$ be the probability of playing Cooperate in round $t$.

**Initialization (Round 1):**
Play Cooperate if $m/n \ge 0.5$, else play Defect. This establishes a baseline intent to coordinate if the threshold is easily met, or to protect the endowment if it is not.

**Subsequent Rounds (2 to r-1):**
1.  **If $C_{t-1} \ge m$:** The group is currently meeting the threshold. Play Defect.
2.  **If $C_{t-1} < m$:** The threshold is not being met. Calculate the "Deficit Gap" ($G = m - C_{t-1}$).
    *   If $G = 1$: Play Cooperate. (One player switching is sufficient to trigger the reward).
    *   If $G > 1$: Play Defect. (Cooperating is insufficient on its own to meet the threshold and represents a sunk cost without coordination).

**Terminal Round (Round r):**
1.  If $C_{r-1} \ge m - 1$: Play Cooperate.
2.  If $C_{r-1} < m - 1$: Play Defect.

**Self-Interested Logic:**
- **Free-riding optimization:** In any round where the threshold is met, the payoff for Defect ($1+k$) is strictly higher than for Cooperate ($k$). The strategy defaults to Defecting whenever the group is already successful, maximizing immediate utility.
- **Conditional coordination:** The strategy limits cooperation to scenarios where the player’s individual action can single-handedly tip the group from failure to success ($G=1$). This minimizes the cost of wasted contributions.
- **Terminal phase:** In the final round, the "future shadow" of the game disappears. The strategy switches to a final "all-in" effort only if there is a realistic chance of success ($C_{r-1} \ge m-1$), accepting the cost of 1 to potentially capture the reward $k$. If the group is nowhere near the threshold, it reverts to Defect to save the endowment.
'''

description_SELFINTERESTED_23 = '''
The strategy utilizes a conditional threshold-trigger model designed to maximize individual payoff by balancing free-riding incentives against the necessity of reaching the threshold $m$.

**Strategy Definition**

Define $C_t$ as the number of cooperators observed in round $t$.
Define $S_t$ as your action in round $t$, where $S_t \in \{0, 1\}$ (0 for Defect, 1 for Cooperate).
Let $H$ be the history of cooperators observed in previous rounds: $H_{t-1} = \{C_1, C_2, \dots, C_{t-1}\}$.

**Decision Rules**

For each round $t \in \{1, \dots, r\}$:

1.  **Initialization (Round 1):**
    If $m \le n/2$, play $S_1 = 0$.
    If $m > n/2$, play $S_1 = 1$.

2.  **Adaptive Threshold Logic (Rounds $t > 1$):**
    Calculate the average observed cooperators $\bar{C} = \frac{1}{t-1} \sum_{j=1}^{t-1} C_j$.
    
    *   **Case A (High Cooperation):** If $\bar{C} \ge m$, play $S_t = 0$. (Free-ride, as the group equilibrium appears stable).
    *   **Case B (Insufficient Cooperation):** If $\bar{C} < m - 1$, play $S_t = 0$. (The group is unlikely to hit the threshold; conserve endowment).
    *   **Case C (Marginal Cooperation):** If $\bar{C} \ge m - 1$ and $\bar{C} < m$, play $S_t = 1$. (Act as the pivotal cooperator to trigger the threshold).

3.  **Endgame Constraint:**
    For the final round $t = r$:
    If the threshold has been consistently met ($C_{r-1} \ge m$), play $S_r = 0$.
    If the threshold is currently at risk ($C_{r-1} < m$), play $S_r = 1$ only if $C_{r-1} == m-1$, otherwise play $S_r = 0$.

**Edge Cases**

*   **Ties:** If $C_t = m-1$, and you played $S_t=0$, you essentially enabled a free-rider outcome. The algorithm effectively treats the previous round's performance as the primary signal for current behavior.
*   **Volatile Histories:** If $\bar{C}$ fluctuates, the strategy prioritizes Case C (Marginal Cooperation) to test if minimal contribution secures the bonus $k$. If, after playing $S_t = 1$, the observed $C_t$ remains $< m$, immediately revert to $S_{t+1} = 0$ for one round to re-assess the group's willingness to contribute.
'''

description_SELFINTERESTED_24 = '''
The strategy relies on a "Threshold-Triggered Conditional Cooperation" approach designed to maximize the likelihood of meeting the minimum cooperation threshold ($m$) while minimizing exploitation by defectors.

### Core Strategy Logic

The strategy maintains a state variable $S$, representing the current belief about the population's willingness to cooperate.

**1. First Round (Initialization):**
Always play **Cooperate (C)**. This signals a willingness to engage in the cooperative equilibrium and establishes an initial data point regarding the population's cooperativeness.

**2. Subsequent Rounds (Adaptation):**
In any round $t > 1$, calculate the number of cooperators from the previous round ($C_{t-1}$). Let $X$ be the number of cooperators observed in round $t-1$.

*   **Case A: If $X \ge m$ (Success in previous round):**
    Play **Cooperate (C)**. Even though defecting yields a higher payoff ($1+k > 2$) when others cooperate, playing $C$ sustains the expectation that the threshold will be met, preventing the total collapse of cooperation.

*   **Case B: If $X = m - 1$ (Critical miss in previous round):**
    Play **Cooperate (C)**. The group is on the verge of the threshold. By contributing, you provide the single unit of effort required to trigger the reward for everyone, including yourself.

*   **Case C: If $X < m - 1$ (Failure to reach threshold):**
    Play **Defect (D)**. When the group demonstrates a strong propensity to defect, contributing is a sunk cost with no return on investment. Defecting ensures you retain your endowment while the group fails to reach the threshold.

**3. State Reset (The "Forgiveness" Mechanism):**
If you are playing Defect (D) because of a sustained failure in Case C, initiate a "probe" round every $N$ rounds (where $N = \lceil r / \ln(r) \rceil$, or at least every 3 rounds if $r$ is small). In a probe round, play **Cooperate (C)**.
*   If the resulting cooperation level $X \ge m-1$, return to the logic in section 2 (Cooperate).
*   If $X < m-1$, immediately revert to playing **Defect (D)**.

### Pseudocode Representation

```python
# Parameters: n, m, k, r
# State: self.my_last_action, self.round_num, self.probing

def decide_action(previous_cooperators_count):
    if round_num == 1:
        return C

    # Handle the "probe" to see if cooperation has recovered
    if probing and round_num % 3 == 0:
        return C

    # Case: Success or near-success
    if previous_cooperators_count >= m - 1:
        return C
    
    # Case: Systemic failure
    else:
        return D

# Post-round update
def update_state(result):
    if action_was_D and result_is_D_dominated:
        probing = True
    else:
        probing = False
```

### Edge Case Handling

*   **Last Round:** Play **Defect (D)** unless you have observed $C_{t-1} \ge m-1$ consistently in previous rounds. Since there is no future, there is no reputational or coordination benefit to contributing in the final round if the threshold has not been reliably met.
*   **Threshold $m$ relative to $n$:** If $m$ is very high (close to $n$), the strategy shifts to aggressive defection ($D$) after any single failure, as the cost of attempting to reach a high threshold with unreliable partners outweighs the reward $k$. If $m$ is low, the strategy remains more forgiving.
'''

description_SELFINTERESTED_25 = '''
In each round $t \in \{1, \dots, r\}$, the strategy employs a conditional cooperation threshold mechanism to maximize cumulative payoff while mitigating free-riding. Let $C_t$ be the total number of players who chose $C$ in round $t$.

**Round 1:**
Play $D$. Observe the baseline cooperation level of the group.

**Round $t$ (for $t > 1$):**
Calculate the average cooperation rate $A_{t-1} = \frac{C_{t-1}}{n}$.

1. **Defection Check:** If $C_{t-1} \ge m$, the group achieved the reward in the previous round. If you played $C$ in the previous round and received $k$, and the total count $C_{t-1}$ was exactly $m$, switch to $D$. You are a pivot player whose contribution is surplus to the minimum requirement. If $C_{t-1} > m$, switch to $D$.
2. **Cooperation Requirement:** If $C_{t-1} < m$, identify the gap $g = m - C_{t-1}$.
    *   If $g = 1$ and you played $D$ in the previous round: Play $C$. This attempts to reach the threshold $m$.
    *   If $g > 1$: Play $D$. Attempting to reach the threshold is statistically unlikely to succeed without broader coordination, making $C$ a sunk cost.
    *   If $g = 0$ (the threshold was met): Play $D$.

**Last Round ($t = r$):**
Always play $D$. Since there are no future rounds to incentivize cooperation, the dominant strategy is to capture the private endowment while hoping the threshold $m$ is met by the remaining group.

**Summary Logic:**
*   If $C_{t-1} \ge m$: Play $D$.
*   If $C_{t-1} < m$:
    *   If $C_{t-1} = m-1$ and $t < r$: Play $C$.
    *   Else: Play $D$.
'''

description_SELFINTERESTED_26 = '''
Use a "Conditional Threshold Tracker" strategy characterized by a dynamic contribution policy based on the minimum number of cooperators ($m$) required.

**Variables:**
*   $m$: Minimum cooperators needed.
*   $c_{t-1}$: Number of cooperators observed in the previous round.
*   $s$: Current state, initialized to "Testing" ($s = \text{Testing}$).

**Decision Rules:**

1.  **First Round ($t=1$):**
    Play **Cooperate (C)** with probability $p=0.5$. This establishes a baseline for signal observation without committing to full vulnerability.

2.  **State Transitions:**
    *   If $c_{t-1} \ge m$: The environment is "Productive." Transition to **"Cooperative"** state.
    *   If $c_{t-1} < m$: The environment is "Hostile." Transition to **"Exploitative"** state.

3.  **Action Logic by State:**
    *   **"Cooperative" State:**
        Play **Cooperate (C)** if and only if $c_{t-1} > m$. If $c_{t-1} == m$ (the threshold is barely met), play **Defect (D)**. This protects against the risk of the total number of cooperators dropping below the threshold, as playing D secures a higher payoff (the "free rider" advantage) while still benefiting from the threshold reward $k$.
    *   **"Exploitative" State:**
        Play **Defect (D)**. If the group has historically failed to meet the threshold, there is no incentive to contribute. However, implement a "Probe": If $t < r$ and $t \mod 5 == 0$, play **Cooperate (C)** once to check if the group behavior has shifted toward cooperation.

4.  **Final Round ($t=r$):**
    Always play **Defect (D)**, regardless of state or history. Since there are no subsequent rounds to incentivize future cooperation or punish defection, the dominant strategy is to maximize the final round payoff by keeping the endowment.

**Edge Cases:**
*   **Threshold volatility:** If $c_{t-1}$ fluctuates around $m$, prioritize **Defect (D)** to avoid the cost of contribution when the threshold is uncertain.
*   **High $k$ vs Low $k$:** If $k > 1$ is significantly large (making cooperation essential for success), adjust the "Exploitative" state logic: If $c_{t-1} = m-1$, play **Cooperate (C)** to attempt to push the group over the threshold, provided $t < r$.
'''

description_SELFINTERESTED_27 = '''
Adopt a threshold-triggered conditional cooperation strategy, focusing on reciprocity while maintaining a fallback to defect if the threshold is unattainable.

### Decision Rules

For each round `t`:

1. **Calculate Threshold Gap:**
   Let `S_{t-1}` be the number of cooperators observed in the previous round.
   - If `t = 1`, target `m` cooperators assuming all players cooperate (e.g., if `n` is large and `m` is small, initialize with `C`).
   - If `t > 1`, evaluate the observed cooperation rate:
     - If `S_{t-1} >= m`, define the group as "Cooperative."
     - If `S_{t-1} < m`, define the group as "Defective/Insufficient."

2. **Action Selection:**
   - **If `t = r` (Final Round):** Always choose `D` (Defect). Since there is no future interaction to incentivize, defecting yields a strictly higher payoff regardless of the threshold status.
   - **If `t < r`:**
     - **Cooperative Phase:** If the group was "Cooperative" in `t-1`, choose `C` (Cooperate) with probability `p = m / n` (scaled to ensure the group threshold is statistically likely to be met), or if the strategy requires a deterministic choice, choose `C` to maintain the equilibrium.
     - **Defective Phase:** If the group was "Defective/Insufficient" in `t-1`, switch to `D` (Defect) for the current round.
     - **Recovery/Testing:** If the group was "Defective/Insufficient" in the previous round, you may periodically attempt a "test" cooperation (e.g., every 3rd round) to see if the group behavior has shifted back to a cooperative equilibrium.

### Edge Case Handling

- **`m` near `n` (High Threshold):** If `m > n/2`, cooperation is fragile. If `S_{t-1} < m` occurs, immediately defect for all subsequent rounds, as the cost of coordination failure is high and recovery is statistically unlikely without communication.
- **`m` near 1 (Low Threshold):** If `m` is small relative to `n`, prioritize cooperation (`C`) consistently unless a sustained trend of defection (`S_{t-1} < m`) is observed, as the reward `k` outweighs the cost of contribution `1` even with slightly suboptimal cooperation from others.
- **`S_{t-1}` instability:** If `S_{t-1}` oscillates around `m`, maintain `C` only if `k > 1`. If `k` is small relative to the cost of contribution, become more aggressive with `D` to protect the base endowment.

### Pseudo-Code

```
for t = 1 to r:
    if t == r:
        action = D
    else if t == 1:
        action = C
    else:
        if S_{t-1} >= m:
            action = C
        else:
            if t % 3 == 0:  // Periodically test for cooperative shift
                action = C
            else:
                action = D
```
'''

description_SELFINTERESTED_28 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat with Conditional Defection**

Let $C_t$ be the total number of cooperators observed in round $t$. Let $n$ be total players, $m$ be the threshold, and $r$ be the total rounds. Let $H_t$ be the set of history observed up to round $t$.

**Phase 1: Initial Round ($t=1$)**
- If $n \le 2m$: Play $C$. (The threshold is attainable; cooperative investment is likely required to hit $m$).
- If $n > 2m$: Play $D$. (The pool of potential cooperators is sufficiently large that individual contribution is less critical for reaching $m$, and the temptation to free-ride is highest).

**Phase 2: Intermediate Rounds ($1 < t < r$)**
Decision logic is based on the performance of the group in round $t-1$ relative to the critical threshold $m$.

1. **Successful Threshold Execution:** If $C_{t-1} \ge m$:
   - If the player played $C$ in $t-1$: Continue to play $C$ (Reinforcing success).
   - If the player played $D$ in $t-1$: Play $D$ (Exploiting the threshold being met without sacrificing the endowment).

2. **Failed Threshold Execution:** If $C_{t-1} < m$:
   - If $C_{t-1} = m-1$: Play $C$ (Attempting to push the group over the threshold in the subsequent round).
   - If $C_{t-1} < m-1$: Play $D$ (Accepting that the threshold is unlikely to be reached; minimizing loss by retaining the endowment).

**Phase 3: Final Round ($t=r$)**
- Play $D$ regardless of prior history. Since there are no future rounds to incentivize, there is no strategic benefit to contributing.

**Pseudocode:**

```python
def get_action(round, n, m, history):
    if round == 1:
        return C if n <= 2 * m else D
    
    if round == r:
        return D

    last_round_cooperators = history.last_C_count
    my_last_action = history.my_last_action

    # If threshold was met last round
    if last_round_cooperators >= m:
        return my_last_action # Stay the course if cooperating, free-ride if defecting

    # If threshold was almost met (only one short)
    if last_round_cooperators == m - 1:
        return C

    # Otherwise, threshold is too far, optimize for personal gain
    return D
```
'''

description_SELFINTERESTED_29 = '''
**Strategy: Threshold-Adaptive Trigger (TAT)**

This strategy operates as a conditional cooperator, utilizing a dynamic threshold model to maximize the likelihood of reaching the critical mass $m$ while punishing free-riders.

**1. Definitions and State Variables**
*   $c_{t-1}$: The number of cooperators observed in the previous round.
*   $m$: Minimum cooperators needed.
*   $n$: Total number of players.
*   $k$: Reward factor.
*   $R_{rem}$: Rounds remaining, including the current round.

**2. Decision Rules**

**Phase 1: The Trust-Building Period (Round 1)**
*   Play **C**. This establishes cooperative intent.

**Phase 2: The Adaptive Period (Rounds 2 through $r-1$)**
Calculate $d_{t-1} = n - c_{t-1}$ (the number of defectors observed in the previous round).

*   **Rule A (Reciprocity):** If $c_{t-1} \ge m$, play **C**. The threshold was met, and the collective behavior is stable.
*   **Rule B (Threshold Recovery):** If $c_{t-1} < m$ and the number of defectors is low (specifically, $c_{t-1} == m-1$), play **C**. You are the "pivotal" cooperator; contributing guarantees the reward for everyone, including yourself, which is better than failing and receiving only 1.
*   **Rule C (Defection Punishment/Survival):** If $c_{t-1} < m-1$, play **D**. If the group is far from the threshold, contributing is a sunk cost. Switch to D to minimize losses ($1$ vs $0$) until the group demonstrates a capacity to reach the threshold.

**Phase 3: The Terminal Period (Last Round, $t=r$)**
*   If the goal is purely maximizing expected payoff without concern for reputation (as no future rounds exist), evaluate the probability of the group reaching the threshold $m$ based on historical data.
*   If historical data suggests the group is highly likely to reach $m$ without your contribution, play **D** to capture the reward $k$ plus the private endowment $1$.
*   If the group is unlikely to reach $m$ even with your contribution, play **D**.
*   The only exception is if $c_{t-1} == m-1$ in the penultimate round, play **C** to secure the final reward $k$.

**3. Pseudocode Logic**

```python
def get_action(round_number, n, m, k, last_round_cooperators, total_rounds):
    # First round
    if round_number == 1:
        return 'C'
    
    # Last round: Free-ride unless pivotal
    if round_number == total_rounds:
        if last_round_cooperators == m - 1:
            return 'C'
        return 'D'
    
    # Standard Adaptive Logic
    if last_round_cooperators >= m:
        return 'C'
    elif last_round_cooperators == m - 1:
        return 'C' # Be pivotal
    else:
        return 'D' # Conserve endowment when threshold is unattainable
```

**4. Strategic Rationale**
This strategy prioritizes the "pivotal" role. By playing **C** only when the collective is at $m-1$ or has successfully demonstrated cooperation ($m+$), the agent avoids wasting resources on groups that are unwilling to contribute. By playing **D** when the group falls well short ($< m-1$), the agent forces the group to move toward the threshold without bearing the cost of failure. The strategy is robust because it is self-correcting: it only sustains cooperation if the group reciprocates or is on the verge of success.
'''

description_SELFINTERESTED_30 = '''
**Threshold-Triggered Conditional Cooperation**

**Variables and Setup:**
Let $N_{C,t}$ be the number of cooperators in round $t$.
Let $S_t$ be your action in round $t$, where $S_t = 1$ if you cooperate and $S_t = 0$ if you defect.
Let $M_{effective} = m - S_t$ (the number of other players needed to reach the threshold $m$ given your choice).

**Decision Rules:**

*   **Round 1:** Play $C$. (Establish cooperation signal to encourage group threshold meeting).
*   **Round $t$ (where $1 < t \le r$):**
    *   Calculate $X_{t-1}$, the observed number of cooperators in the previous round.
    *   **Cooperation Condition:** If $X_{t-1} \ge m$, play $C$.
    *   **Defection Condition:** If $X_{t-1} < m$, play $D$.
*   **Final Round:** Play $D$ regardless of history.

**Logic:**
1.  **Exploitation Avoidance:** The system rewards defection ($D$) with a base payoff of 1 versus 0 for cooperation ($C$). If the group fails to meet the threshold ($X < m$), cooperating is strictly dominated by defecting. The rule to switch to $D$ if $X_{t-1} < m$ prevents you from throwing away your endowment when the group is non-cooperative.
2.  **Coordination Signaling:** By playing $C$ in Round 1, you signal a willingness to contribute. By playing $C$ only when $X_{t-1} \ge m$, you condition your support on the group's demonstrated ability to meet the threshold, effectively rewarding the group for maintaining the threshold and punishing them (by withdrawing support) when they fail.
3.  **End-Game:** In the final round, the incentive for future reciprocity vanishes. Because playing $D$ yields a higher immediate payoff than playing $C$ regardless of the outcome, you must defect in the final round to maximize your total payoff, as there is no opportunity for future punishment or reward.
'''

description_SELFINTERESTED_31 = '''
Maintain a record of the total number of cooperators from the previous round, denoted as $C_{t-1}$. Initialize the strategy by playing D in the first round to test the collective cooperation baseline.

For all subsequent rounds $t > 1$:

1. Calculate the "Defector-Dominant Threshold": If the number of cooperators in the previous round ($C_{t-1}$) was greater than or equal to $m$, defect (D). The reward $k$ is already being realized, and defecting provides a higher individual payoff ($1+k$) compared to contributing ($k$).

2. Calculate the "Minimum-Threshold Trigger": If $C_{t-1} < m$, assess whether the collective is close to the threshold. If $C_{t-1} \geq m - 1$, cooperate (C). This action assumes that by contributing, the player can bridge the gap to reach the threshold of $m$, thereby securing the reward $k$ for the next round. If $C_{t-1} < m - 1$, continue to defect (D).

3. Final Round Adjustment: In round $r$, if the cumulative payoff from rounds $1$ to $r-1$ suggests that the group is consistently failing to reach the threshold $m$, defect (D) regardless of prior history. If the group is consistently reaching the threshold or is frequently hitting $m-1$ cooperators, use the rules above, but prioritize defecting (D) if the calculated gain from cooperating in the final round is strictly less than the guaranteed payoff of defecting when $m$ is not reached.

Pseudocode:

```python
history = [] # Stores C_{t-1} for each round

def get_action(round_number, n, m, k, history):
    if round_number == 1:
        return 'D'
    
    last_round_cooperators = history[-1]
    
    # If threshold met last round, enjoy the free-ride
    if last_round_cooperators >= m:
        return 'D'
    
    # If one away from threshold, attempt to trigger the reward
    if last_round_cooperators == m - 1:
        return 'C'
    
    # If threshold is far, defect to minimize personal loss
    return 'D'
```
'''

description_SELFINTERESTED_32 = '''
The strategy follows a conditional "Trigger-Threshold" logic designed to incentivize cooperation only when the collective reward is achievable and credible, while defaulting to defection to capture the higher individual payoff ($1$) whenever cooperation is unnecessary or failing.

**Core Decision Rule:**

Let $C_{t-1}$ be the number of cooperators in the previous round.
Let $I_{t-1}$ be an indicator variable where $I_{t-1} = 1$ if you cooperated in the previous round, and $0$ otherwise.
Let $M_{effective}$ be the minimum number of cooperators required from *others* for you to contribute. 
*   If you choose to cooperate, you contribute 1 toward the total $m$. Thus, you need $m-1$ others.
*   If you choose to defect, you contribute 0. The group needs $m$ others.

The strategy operates in three states:

1.  **Exploration/Initialization (Round 1):**
    Play **C** with probability $p = (m-1) / (n-1)$. This biases initial contribution toward the threshold $m$ while minimizing individual risk.

2.  **Conditional Cooperation (Rounds $2$ to $r-1$):**
    Assess if the group is currently meeting or has recently met the threshold $m$.
    
    *   **Calculate "Group Viability":** If $C_{t-1} \ge m$, the collective is productive.
    *   **Decision Logic:**
        *   If $C_{t-1} \ge m$: Play **C**. (You contribute to maintain the status quo).
        *   If $C_{t-1} == m-1$: Play **C**. (You are the pivot player; contributing guarantees the reward $k$ for everyone).
        *   If $C_{t-1} < m-1$: Play **D**. (The threshold is too far to reach; minimize losses).

3.  **Terminal Phase (Round $r$):**
    *   If the strategy has been in a cycle of $C_{t-1} \ge m-1$ for the previous two rounds, play **C**.
    *   Otherwise, play **D**. (Do not invest in a collective good that cannot be realized in the final period).

**Edge Cases & Calibration:**

*   **The "Freeloader" Check:** If at any point the observation shows $C_{t-1} > m$ and you played $D$ (meaning others carried the burden), continue playing **D** in the next round to test if the group threshold holds without your contribution. If the count drops below $m$, revert to the Conditional Cooperation logic in the subsequent round.
*   **Threshold Shift:** If $n$ is very large relative to $m$, the "Exploration" probability $p$ ensures you do not waste resources attempting to hit a threshold that the group is not coordinated enough to achieve.
*   **Anonymity:** Since specific identities are hidden, the strategy treats the group as a single aggregate agent. If the aggregate count of cooperators is consistently below $m-1$, the strategy permanently reverts to **D** for the remainder of the game, as the group is deemed uncooperative.
'''

description_OPPORTUNISTIC_5 = '''
### Strategy: Threshold-Targeting Opportunism

**Initialization (Round 1):**
Cooperate. Establishing a baseline contribution is necessary to signal potential participation in the threshold goal.

**Recursive Logic (Rounds 2 to r):**
Let $C_{prev}$ be the number of players who cooperated in the previous round.
Let $s_{prev}$ be your action in the previous round (1 if Cooperate, 0 if Defect).
Let $m_{eff}$ be the effective threshold of cooperators needed for you to benefit.

1.  **If $s_{prev} == 1$ (You cooperated):**
    *   If $C_{prev} \ge m$: The threshold was met. You successfully secured the reward $k$. Switch to Defect ($D$) for the current round to maximize personal gain, exploiting the successful threshold.
    *   If $C_{prev} < m$: The threshold was not met. You did not secure the reward $k$. Remain in Cooperate ($C$) for the current round, continuing to attempt to reach the threshold.

2.  **If $s_{prev} == 0$ (You defected):**
    *   If $C_{prev} \ge m$ (Threshold met without you): Continue to Defect ($D$). You are free-riding successfully.
    *   If $C_{prev} == m - 1$ (Threshold nearly met): Switch to Cooperate ($C$). Your contribution tips the balance to reach the reward $k$ without over-contributing.
    *   If $C_{prev} < m - 1$: Remain in Defect ($D$). The group is failing to reach the threshold, and your single contribution is insufficient to trigger the reward $k$.

**Edge Cases and Finality:**

*   **Last Round ($t = r$):**
    *   If $C_{prev} \ge m - 1$: Cooperate ($C$).
    *   If $C_{prev} < m - 1$: Defect ($D$).
    *   *Rationale:* In the terminal round, future signaling has no value. You only contribute if your specific action can bridge the gap to the threshold $m$.

*   **Convergence Failure:** If the system enters a cycle where $C_{prev}$ consistently oscillates below $m$ despite your participation, switch to Defect ($D$) for the remainder of the game, as the group is non-cooperative and the reward $k$ is unattainable.
'''

description_OPPORTUNISTIC_6 = '''
1. **Initialization (Round 1):** Play Cooperate ($C$).

2. **Observation Window:** Maintain a count of the number of cooperators observed in each previous round $t$, denoted as $n_t$.

3. **Opportunistic Decision Rule:**
   For rounds $t \in \{2, \dots, r\}$, determine action based on the state of the system in the previous round ($t-1$):

   *   **Case A (Threshold Met):** If $n_{t-1} \ge m$:
       *   If you played $C$ in round $t-1$: Switch to Defect ($D$).
       *   If you played $D$ in round $t-1$: Maintain Defect ($D$).
       *   *Logic:* Exploit the fact that the threshold is already being met without your contribution.

   *   **Case B (Threshold Failed):** If $n_{t-1} < m$:
       *   If you played $C$ in round $t-1$ (meaning the group failed despite your effort): Switch to Defect ($D$).
       *   If you played $D$ in round $t-1$ and the total cooperators $n_{t-1} = m-1$: Switch to Cooperate ($C$).
       *   If you played $D$ in round $t-1$ and the total cooperators $n_{t-1} < m-1$: Maintain Defect ($D$).

4. **Edge Cases:**
   *   **Final Round ($r$):** Play Defect ($D$) regardless of history. There is no future round to influence or signal to, making defection the strictly dominant strategy for maximizing absolute return.
   *   **Tie-Breaking/Uncertainty:** In any round where switching to $C$ is triggered by $n_{t-1} = m-1$, if multiple players act identically, this may lead to oscillating outcomes. If $n_{t-2} = n_{t-1} < m$ persists for two consecutive rounds, revert to Defect ($D$) for all subsequent rounds as the group is non-cooperative.
'''

description_OPPORTUNISTIC_7 = '''
**Strategy: Conditional Threshold-Triggered Opportunism**

The agent maintains a state variable $S_t$, representing the observed number of cooperators in the previous round $t-1$. In the first round ($t=1$), the agent plays $C$ to signal pro-social intent and test the collective threshold.

For all rounds $t > 1$:

1.  **Threshold Enforcement:** If the number of cooperators in round $t-1$ was exactly $m$, play $D$. This exploits the threshold condition: since $m$ players are already cooperating, the collective reward $k$ is guaranteed regardless of your individual contribution, allowing you to maximize private payoff.

2.  **Rescue/Recovery:** If the number of cooperators in round $t-1$ was $m-1$, play $C$. This is a "rescue" move. Since the threshold was narrowly missed, the probability of successful collective action is high if one additional player contributes. By contributing, you move the collective state to $m$, securing the reward $k$ for everyone.

3.  **Collapse/Abandonment:** If the number of cooperators in round $t-1$ was less than $m-1$, play $D$. The collective failure is too significant to overcome with a single contribution. You shift to a purely defecting strategy to minimize personal losses until the group demonstrates a renewed capacity to cooperate.

4.  **Excess Cooperation:** If the number of cooperators in round $t-1$ was greater than $m$, play $D$. The threshold is comfortably met, and the collective system is stable without your contribution.

5.  **Final Round ($t = r$):** Always play $D$. Regardless of the history or potential for future rounds, there is no future interaction to influence or benefit from. The optimal move in the final stage is to maximize immediate payoff.

**Pseudocode:**

```
if t == r:
    return D
if t == 1:
    return C
    
observed_C = history.last_round_cooperators
if observed_C == m - 1:
    return C
else:
    return D
```
'''

description_OPPORTUNISTIC_8 = '''
If total rounds remaining (R_rem) equals 1:
   - Defect (D).

Else if round number (t) equals 1:
   - Cooperate (C) with probability P_start = (m / n).

Else (t > 1 and R_rem > 0):
   - Let (C_prev) be the number of cooperators observed in the previous round.
   - If (C_prev >= m):
      - Defect (D).
   - If (C_prev < m):
      - If (C_prev >= m - 1):
         - Cooperate (C) with probability P_adaptive = (m - C_prev) / (n - C_prev + 1).
      - Else:
         - Defect (D).

Implementation Logic:
1. First-round participation establishes a baseline cooperative signal to potential collaborators without committing to long-term altruism.
2. The "Defect" rule after a successful round (C_prev >= m) exploits the collective success, capitalizing on others' contributions while minimizing individual risk.
3. The adaptive probability P_adaptive in the (C_prev < m) condition targets the "swing" state:
   - If exactly m-1 players cooperated, you have a high probability of tipping the collective outcome to success, securing the reward k while others bear the cost.
   - If fewer than m-1 players cooperated, the cost of participation is unlikely to secure the reward (k), so you defect to preserve the endowment.
4. The final-round defection rule ensures you do not expend resources when no future cooperation can be induced.
'''

description_OPPORTUNISTIC_9 = '''
The strategy is a Threshold-Triggered Opportunistic Response (TTOR), designed to maximize personal payoff by exploiting the threshold requirement while protecting the bonus. It operates on the principle of minimal necessary contribution to secure the $k$ reward.

**Variables:**
- $C_{t-1}$: Number of cooperators in the previous round.
- $MyAction_{t-1}$: My action in the previous round.
- $n_{eff}$: Effective number of cooperators excluding myself. 
    - If I played C, $n_{eff} = C_{t-1} - 1$.
    - If I played D, $n_{eff} = C_{t-1}$.

**Decision Rules per Round $t$:**

1.  **First Round ($t=1$):**
    Play C. This establishes a baseline of cooperation to signal potential reciprocity and gauges the baseline behavior of the population.

2.  **Intermediate Rounds ($1 < t < r$):**
    Calculate the minimum cooperators needed from others to hit the threshold if I defect: $Need = m$.
    - If $n_{eff} \ge m$: Play D. The threshold is met without my contribution; free-ride to maximize profit.
    - If $n_{eff} == m - 1$: Play C. The threshold is exactly one shy of being met; contribute to secure the $k$ reward.
    - If $n_{eff} < m - 1$: Play D. The group is failing to reach the threshold; do not waste the endowment cost since the bonus will not be triggered regardless. 
    *Exception*: If $t = t_{r-1}$ and $n_{eff} == m - 2$, play C with probability $0.5$ (a "probing" maneuver) to test if others are also withholding cooperation due to coordination failure.

3.  **Final Round ($t=r$):**
    - If $n_{eff} \ge m$: Play D.
    - If $n_{eff} == m - 1$: Play C.
    - If $n_{eff} < m - 1$: Play D.

**Logic Adjustments for Opponent Behavior:**
- **Reciprocity Monitor:** If $C_{t-1}$ consistently drops immediately after I switch from C to D, treat this as a "punishment" signal. If $C_{t-1}$ remains stable regardless of my D, continue the free-riding cycle.
- **Threshold Failure Pattern:** If the group fails to meet the threshold ($C_{t-1} < m$) for three consecutive rounds despite my contribution, switch to permanent D for the remainder of the game, as the group is uncoordinated and the $k$ reward is unattainable.
'''

description_OPPORTUNISTIC_10 = '''
Strategy: Conditional Threshold Monitoring (CTM)

The strategy operates on a "Wait-and-Verify" protocol. The objective is to maximize individual gain by contributing the minimum necessary to trigger the threshold $m$, while defecting whenever the threshold is safely met or clearly unattainable.

Decision Logic:

1.  Round 1:
    Play C (Cooperate). This establishes a willingness to participate and signals cooperative intent without immediate risk of exploitation, given the ignorance of opponent behavior.

2.  Rounds 2 to r-1:
    Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   If $C_{t-1} \ge m$:
        Play D (Defect). Since the threshold was met without your contribution, you capture the bonus $k$ while retaining your endowment.
    *   If $C_{t-1} = m - 1$:
        Play C (Cooperate). You are the pivot player. By contributing, you trigger the bonus $k$ for the group, ensuring you receive the maximum possible payoff for that round.
    *   If $C_{t-1} < m - 1$:
        Play D (Defect). If the cooperative effort is significantly below the threshold, individual contribution is futile. You minimize loss by retaining the endowment.

3.  Final Round (Round $r$):
    *   If $C_{r-1} \ge m$:
        Play D (Defect). The expectation is that the bonus will be met regardless of your input based on the previous round’s success.
    *   If $C_{r-1} < m$:
        Play D (Defect). There is no future round to punish defection or reward long-term cooperation. The rational choice is to maximize the single-round payoff by retaining the endowment.

Pseudocode:

```
If round == 1:
    return C

If round == r:
    return D

// Intermediate Rounds
If previous_round_cooperators >= m:
    return D
Else If previous_round_cooperators == m - 1:
    return C
Else:
    return D
```

Edge Cases:
*   If $m > n$ (impossible threshold): The strategy defaults to D every round.
*   If $m = 1$: The strategy defaults to D every round (assuming $k > 1$, you always get the bonus if anyone contributes, and if you are the only one, you contribute 0 and gain $1+k$, but the threshold is trivial).
'''

description_OPPORTUNISTIC_11 = '''
### Strategy: Conditional Reciprocity with Threshold Sensitivity

This strategy operates on the principle of "cooperate only if necessary for the threshold, defect otherwise to maximize individual gain." It treats the threshold $m$ as a variable target to be hit efficiently, prioritizing private payoff maximization while ensuring the collective project succeeds when cooperation is required.

**Variables:**
- $C_{total, t-1}$: Total cooperators in the previous round.
- $N_{coop}$: Estimated minimum cooperators currently needed to reach $m$.
- $State$: Either 'Neutral' (initial state) or 'Retaliatory' (if opponents defect frequently).

**Decision Rules:**

1.  **First Round:**
    Act as a 'Conditional Cooperator'. Play $C$. This establishes cooperation potential without assuming opponent behavior, minimizing the risk of a collective failure due to total initial defection.

2.  **Subsequent Rounds ($t > 1$):**
    Evaluate the previous round's outcome ($C_{total, t-1}$) to determine the action for round $t$.

    *   **If $C_{total, t-1} \ge m$:**
        The group has met the threshold without my contribution. Play $D$. This maximizes private payoff.

    *   **If $C_{total, t-1} < m$:**
        The threshold was not met in the previous round. Calculate the deficit. If the current player's cooperation is necessary to reach $m$ (i.e., $C_{total, t-1} = m - 1$), play $C$. If the deficit is greater than 1 (i.e., $C_{total, t-1} < m - 1$), play $D$ for this round.

    *   **Exception (The Last Round):**
        In round $r$, ignore the $C_{total, r-1}$ check. If $C_{total, r-1} < m$, play $C$. If $C_{total, r-1} \ge m$, play $D$.

**Pseudocode:**

```python
if round == 1:
    action = C

elif round == r:
    # Final round: attempt to force threshold if failed previously
    if cooperators_previous_round < m:
        action = C
    else:
        action = D

else:
    # Mid-game opportunistic adjustment
    if cooperators_previous_round >= m:
        # Threshold met without me; maximize private gain
        action = D
    elif cooperators_previous_round == (m - 1):
        # I am the marginal player needed to hit the threshold
        action = C
    else:
        # Too many defectors to make my single contribution matter
        action = D
```

**Opportunistic Logic:**
This strategy minimizes the "cost of cooperation" by only contributing when the player's single contribution is the pivot point for achieving the bonus $k$. It avoids "sucker payoffs" in scenarios where the group is either already meeting the threshold (making individual cooperation redundant) or failing so significantly that a single contribution cannot save the project. It ensures that the player is always contributing $0$ in rounds where the threshold is met by others, effectively "free-riding" on the collective effort whenever possible, while providing just enough support to secure the reward when the group is on the verge of success.
'''

description_OPPORTUNISTIC_12 = '''
The strategy operates on a conditional cooperative basis, utilizing a "Triggered Threshold" mechanism that dynamically shifts from cooperation to opportunistic defection based on observed history and remaining rounds.

### Core Decision Rules

Define $C_t$ as the total number of cooperators observed in round $t$. Define $H_t$ as the history of cooperation counts $\{C_1, \dots, C_{t-1}\}$.

1.  **Phase 1: Cooperative Seeding ($t=1$):**
    Always play C. Establishing the threshold is necessary to gauge collective willingness and unlock the reward $k$.

2.  **Phase 2: Reciprocal Adaptation ($1 < t < r$):**
    Calculate the effective cooperation threshold needed to achieve the reward. If $C_{t-1} \geq m$, play C. If $C_{t-1} < m$, play D.
    *Exception:* If the cumulative rewards gained in previous rounds ($R_{total}$) are sufficiently high relative to the potential loss, or if the history suggests the collective has failed to reach $m$ consistently, switch to D to maximize immediate private payoff. Specifically, if $C_{t-1} < m$ for two consecutive rounds, switch to D for all subsequent rounds as the strategy is likely facing a non-cooperative collective.

3.  **Phase 3: The Opportunistic Exit ($t=r$):**
    Always play D. In the final round, there is no future reciprocity to enforce cooperation. The risk of threshold failure is weighed against the certain gain of private endowment. Play C if and only if $C_{t-1} \geq m$ AND $k > 1$. Otherwise, play D.

### Pseudocode Implementation

```python
# Constants: n, m, k, r are fixed
# History: observed_cooperators_list

def get_action(t, observed_history):
    # Round 1: Build trust/test the waters
    if t == 1:
        return 'C'
    
    # Last Round: Maximum opportunism
    if t == r:
        if observed_history[-1] >= m:
            return 'C'
        else:
            return 'D'

    # Intermediate Rounds: Tit-for-Tat with threshold awareness
    previous_C = observed_history[-1]
    
    # If the group failed the threshold last time, defect to capture private endowment
    if previous_C < m:
        # Check for permanent defection strategy: 
        # If group has consistently failed, abandon cooperation
        if len(observed_history) > 1 and observed_history[-2] < m:
            return 'D'
        return 'D'
        
    # If group met threshold, cooperate to sustain reward k
    return 'C'
```

### Edge Cases and Adjustments

*   **Threshold volatility:** If the number of cooperators fluctuates closely around $m$ (e.g., $m, m-1, m$), maintain cooperation (C) as long as the average success rate over the last 3 rounds is $\geq 0.5$. If success drops below 0.5, treat as a failed regime and switch to permanent defection (D).
*   **Minimal Cooperation:** If $n - m < m$ (i.e., the cost to reach the threshold is lower than the remaining group size), prioritize C slightly longer, as the system is structurally biased toward success.
*   **Reward Inefficiency:** If $k \leq 1$, the reward does not outweigh the cost of cooperation (contributing 1 for a reward of $k \leq 1$ is a net loss or zero-sum). In this parameter configuration, ignore all logic above and play D in all rounds $1$ to $r$.
'''

description_OPPORTUNISTIC_13 = '''
The strategy follows a "Conditional Tit-for-Tat with Threshold Sensitivity" logic, designed to maximize immediate rewards while enforcing cooperation.

**State Variables**
- $C_t$: Number of cooperators in round $t$.
- $s_{t-1}$: Personal action in the previous round (1 if Cooperate, 0 if Defect).
- $target$: The number of cooperators required for the reward ($m$).

**Decision Rules**

1. **Initialization (Round 1):**
   Play $C$ (Cooperate). This establishes a cooperative baseline to incentivize reciprocal behavior from opponents.

2. **Subsequent Rounds ($t > 1$):**
   - **Case A: Threshold Met ($C_{t-1} \ge m$):**
     If the threshold was met, the group is cooperating. However, to be opportunistic, check if the threshold was met with a surplus.
     - If $C_{t-1} > m$: Defect ($D$). Since the threshold is exceeded even without your contribution, you can free-ride on the excess.
     - If $C_{t-1} == m$: Cooperate ($C$). If you defect, the threshold would fall to $m-1$, losing the reward $k$ for everyone. Maintaining the minimum is the only way to secure the reward.

   - **Case B: Threshold Not Met ($C_{t-1} < m$):**
     - If your previous action was $D$:
       - If $C_{t-1} == m-1$: Cooperate ($C$). Your contribution tips the group into meeting the threshold.
       - If $C_{t-1} < m-1$: Defect ($D$). The group is too far from the threshold; contributing will not secure the reward, so minimize loss by keeping the endowment.
     - If your previous action was $C$:
       - If $C_{t-1} == m-1$ (meaning $m$ cooperators if you switch to $D$): Defect ($D$). You played $C$ last time, but the threshold wasn't met. Switch to $D$ to test if others will increase their cooperation without your contribution.

3. **Termination (Final Round):**
   - If $C_{r-1} \ge m$: Defect ($D$). There is no future round to punish or reward; maximize your final payoff by keeping the endowment.
   - If $C_{r-1} < m$: Defect ($D$). There is no incentive to contribute if the threshold was missed previously, and insufficient information to guarantee the threshold will be met this round.

**Pseudocode Logic**

```python
if t == 1 or t == r:
    return D
    
# Check threshold status from previous round
if C_prev >= m:
    if C_prev > m:
        return D # Free-ride on surplus
    else:
        return C # Hold the line
else:
    # Threshold failed
    if C_prev == m - 1:
        # We can flip the outcome
        return C 
    else:
        # Too far to save
        return D
```
'''

description_OPPORTUNISTIC_14 = '''
**Strategy: Conditional Threshold Tit-for-Tat**

The strategy operates by attempting to stabilize cooperation at the minimum necessary threshold $m$ while exploiting defectors whenever the threshold is safely exceeded.

**Decision Logic**

Define $C_t$ as the number of cooperators in round $t$.
Define $s$ as your own action in round $t$ (1 if you cooperated, 0 if you defected).

*   **Round 1:** Play **Cooperate (C)**. Establish intent to reach the threshold $m$.

*   **Rounds $t > 1$:**
    *   **Case 1: Under-provisioning (Defection or Failure).** If $C_{t-1} < m$ (or $C_{t-1} = m$ but you were one of the cooperators and observed that others were not contributing, implying a risk of falling below $m$):
        *   **Cooperate (C)**. You must ensure the threshold is met to gain the reward $k$.

    *   **Case 2: Sufficient Provisioning (Excess Cooperation).** If $C_{t-1} \ge m + 1$:
        *   **Defect (D)**. Since the threshold $m$ was met comfortably, the reward $k$ is secured regardless of your individual action. By defecting, you optimize your payoff by retaining your endowment while still receiving $k$.

    *   **Case 3: Exact Threshold (Fragile Cooperation).** If $C_{t-1} = m$:
        *   **Cooperate (C)**. If you defect, the count drops to $m-1$, causing everyone to lose the reward $k$. Maintain cooperation to preserve the collective benefit.

*   **Final Round ($t = r$):**
    *   Regardless of previous history, **Defect (D)**. Since there is no future round to punish or incentivize, the dominant strategy is to maximize the final round payoff by keeping the endowment.

**Pseudocode**

```python
def make_decision(round_number, total_rounds, num_cooperators_prev, self_acted_c):
    # Final round: always defect for maximum terminal payoff
    if round_number == total_rounds:
        return 'D'
    
    # First round: cooperate to seed the collective action
    if round_number == 1:
        return 'C'
    
    # Analyze state from previous round
    # If the threshold was met with a buffer (m+1 or more), 
    # we can safely defect and still get the reward k.
    if num_cooperators_prev >= m + 1:
        return 'D'
        
    # If the threshold was met exactly (m), we must continue to cooperate.
    # If we were one of the cooperators (self_acted_c is True), we continue.
    # If we were a defector (self_acted_c is False), we evaluate: 
    # if the group managed to hit m without us, we continue to defect (free-ride).
    # if the group hit m precisely because we cooperated, we continue to cooperate.
    if num_cooperators_prev == m:
        if self_acted_c:
            return 'C'
        else:
            return 'D'
            
    # If the threshold was missed (less than m), we must cooperate to rescue the reward.
    return 'C'
```
'''

description_OPPORTUNISTIC_15 = '''
**Strategy: Threshold-Sensitive Opportunism**

This strategy maximizes utility by dynamically adjusting contribution behavior based on the observed threshold status, aiming to free-ride whenever the community threshold is secure without individual contribution, while acting as a pivotal contributor only when necessary to trigger the collective reward.

**Definitions:**
*   $c_{t-1}$: Number of cooperators observed in the previous round.
*   $T_t$: The "threshold requirement" for the current round, defined as $m$ if you defected last round, or $m-1$ if you cooperated last round (to account for your own potential contribution).

**Decision Rules:**

1.  **Initial Round ($t=1$):**
    Play **Cooperate (C)**. This signals a baseline willingness to participate and tests the collective responsiveness of the group.

2.  **Subsequent Rounds ($t > 1$):**
    *   **The Threshold Check:** Calculate the effective state of the group.
        *   If you played **C** in $t-1$: You were a contributor. If $c_{t-1} \ge m$, the threshold was met.
        *   If you played **D** in $t-1$: You were a non-contributor. If $c_{t-1} \ge m$, the threshold was met.
    *   **Exploitation Condition:** If $c_{t-1} \ge m + 1$ (the group is over-performing the threshold), switch to **Defect (D)**. This maximizes payoff by retaining the endowment while still securing the collective reward $k$.
    *   **Maintenance Condition:** If $c_{t-1} == m$ and you played **C**, stay **Cooperate (C)**. This maintains the threshold state. If $c_{t-1} == m$ and you played **D**, stay **Defect (D)**.
    *   **Recovery Condition:** If $c_{t-1} < m$, switch to **Cooperate (C)**. This is a "pivotal" move; it recognizes that the collective reward is currently lost and acts to restore it.

3.  **Final Round ($t = r$):**
    Regardless of prior history, play **Defect (D)** unless $c_{r-1} < m$. If the group failed to meet the threshold in the penultimate round, play **Cooperate (C)** if you believe there is a sufficient probability of reaching the threshold $m$ with your contribution (i.e., if $c_{r-1} = m-1$). If $c_{r-1} < m-1$, play **Defect (D)** to minimize loss in the final round.

**Pseudocode:**

```python
if t == 1:
    action = C
elif t == r:
    if observed_cooperators_previous_round >= m - 1:
        action = C 
    else:
        action = D
else:
    # If the group over-contributes, exploit
    if observed_cooperators_previous_round > m:
        action = D
    # If the threshold was met exactly
    elif observed_cooperators_previous_round >= m:
        action = previous_action
    # If the threshold was missed, attempt recovery
    else:
        action = C
```
'''

description_OPPORTUNISTIC_16 = '''
**Phase 1: Initialization**
In the first round, play C (Cooperate). This establishes cooperative intent and gathers critical data regarding the aggregate cooperation level of the opponent pool without risking immediate exploitation.

**Phase 2: Monitoring and Threshold Enforcement**
Track the number of cooperators from the previous round (N_c). Define a "Cooperation Signal" (S) as the number of others who cooperated:
- If you cooperated in the previous round: S = N_c - 1
- If you defected in the previous round: S = N_c

Maintain a "Trust Score" (T), starting at 0. After each round, update T:
- If S ≥ m: T = T + 1
- If S < m: T = max(0, T - 1)

**Phase 3: The Opportunistic Decision Logic**
In rounds 2 through r-1, decide your action based on current observation and historical trends:

1.  **Defect (D)** if S ≥ m (the group is currently exceeding the threshold). This captures the full payoff (1 + k) without contributing, maximizing individual gain.
2.  **Cooperate (C)** if S < m-1 (the group is significantly failing). Propping up a failing threshold is necessary to ensure the k reward remains accessible.
3.  **Calculate Marginal Contribution** if S == m-1 (exactly one more cooperator is needed):
    - If T > 0, play D. Rely on the probability that another player will realize the threshold is one short and contribute, allowing you to free-ride.
    - If T == 0, play C. This is a critical investment to prevent the reward from collapsing.

**Phase 4: The Terminal Phase**
In the final round (r):
- If the cumulative history shows the group has consistently met the threshold (S ≥ m in the last three rounds), play D.
- Otherwise, play C only if S < m-1. If S ≥ m-1, play D. In the final round, the incentive to free-ride outweighs the risk of future retaliation, as there are no subsequent rounds for the group to punish defection.

**Pseudocode Summary:**
```python
def get_action(round, last_round_cooperators, my_last_action):
    if round == 1: return C
    
    # Calculate others' cooperation count
    others_cooperated = last_round_cooperators - (1 if my_last_action == C else 0)
    
    # Terminal strategy
    if round == r:
        return D if others_cooperated >= (m - 1) else C

    # Opportunistic logic
    if others_cooperated >= m:
        return D
    elif others_cooperated < m - 1:
        return C
    else: # others_cooperated == m - 1
        return D if TrustScore > 0 else C
```
'''

description_OPPORTUNISTIC_17 = '''
Strategy: **Threshold-Conditional Opportunism (TCO)**

The strategy relies on maintaining a cooperative state only when the collective threshold is met or when the prospect of future cooperation is threatened, while defecting whenever the threshold is safely exceeded by others to maximize individual gains.

**1. Definitions:**
*   `C_t`: The number of cooperators observed in round `t`.
*   `last_round_cooperators`: The number of cooperators observed in the immediately preceding round.
*   `my_action_{t-1}`: My action in the previous round.
*   `threshold_met`: Boolean, true if `C_t` >= `m`.

**2. Decision Rules:**

*   **Round 1:** Play **Cooperate** (`C`). This establishes a baseline of cooperation and signals willingness to participate in the collective effort.

*   **Rounds 2 through `r-1`:**
    *   **If `last_round_cooperators` >= `m + 1`:** Play **Defect** (`D`). In this scenario, the collective threshold is already satisfied by other players. By defecting, you capture the free-rider payoff (`1 + k`) rather than the cooperative payoff (`0 + k`).
    *   **If `last_round_cooperators` == `m`:**
        *   If `my_action_{t-1}` was `C`, play **Defect** (`D`). Test the robustness of the group. If the group maintains the threshold without your contribution, you capture the free-rider bonus.
        *   If `my_action_{t-1}` was `D`, play **Cooperate** (`C`). You are required to maintain the threshold.
    *   **If `last_round_cooperators` < `m`:** Play **Cooperate** (`C`). The group is failing to meet the threshold. You must contribute to ensure the reward `k` is triggered for everyone, including yourself.

*   **Final Round (`r`):** Play **Defect** (`D`) regardless of previous outcomes. Since there are no future rounds to influence, the incentive to maintain the cooperative group structure vanishes. Defection maximizes the terminal round payoff.

**3. Handling Edge Cases:**
*   **Tie-breaking the threshold:** If `last_round_cooperators` was exactly `m`, and you played `C` and the result was still `m`, the previous rule implies your contribution was critical. If you played `D` and the result was `m`, your contribution was not critical.
*   **Initialization:** In the event that the system restarts or if the history is cleared, always treat the first round of the current sequence as Round 1.
*   **Minimum Players:** If `n` is small and the difference between `n` and `m` is minimal, prioritize maintaining the threshold even if it means sacrificing individual payoff, as the risk of total failure is higher. If `(n - m)` is 0 or 1, strictly play `C` in all rounds except the final round.
'''

description_OPPORTUNISTIC_18 = '''
**Phase 1: Initialization**
In the first round, initiate cooperation if the threshold requirement $m$ is relatively low compared to $n$ (i.e., $m/n \le 0.5$). If the threshold is high ($m/n > 0.5$), initiate with Defection to test the group's baseline tendency to cooperate without risking immediate endowment loss.

**Phase 2: Adaptive Opportunism (Rounds 2 to $r-1$)**
Maintain a counter of the number of cooperators observed in the previous round, $C_{obs}$. Calculate the "Critical Deficiency" ($D_{crit}$), defined as $m - C_{obs}$.

1. **Defection Rule (The "Free-Ride" Trigger):**
   If $C_{obs} \ge m + 1$, you are part of a surplus of cooperators. Switch to Defect to maximize personal payoff ($1 + k$ vs $k$).
   
2. **Conditional Cooperation Rule (The "Pivot"):**
   If $C_{obs} < m$:
   - If $D_{crit} == 1$ (you can single-handedly trigger the reward), switch to Cooperate.
   - If $D_{crit} > 1$ (your contribution alone is insufficient), continue to Defect to conserve resources, assuming the group is not currently coordinating. 
   
3. **Threshold Stabilization Rule:**
   If $C_{obs} == m$ (the threshold is perfectly met), continue to Cooperate to ensure the reward $k$ is sustained, provided this has been stable for at least one preceding round. If the threshold was met but fluctuates, treat as an unstable environment and revert to the Defection Rule.

**Phase 3: The Endgame (Round $r$)**
In the final round, ignore reciprocal patterns and maximize expected payoff regardless of history.
- If $C_{obs(r-1)} \ge m$: Defect. Since the game ends, future retaliation is impossible. You receive $1 + k$.
- If $C_{obs(r-1)} < m$: Defect. Since the group has failed to coordinate historically, investing in a final round of cooperation is a sunk cost. Do not contribute.

**Pseudocode Logic:**

```python
def get_action(round_number, n, m, k, last_C_obs):
    # Round 1 Setup
    if round_number == 1:
        return 'C' if (m/n <= 0.5) else 'D'
    
    # Endgame
    if round_number == r:
        return 'D'
    
    # Opportunistic logic
    D_crit = m - last_C_obs
    
    if last_C_obs >= m + 1:
        # Surplus detected: Free-ride
        return 'D'
    elif last_C_obs == m:
        # Equilibrium detected: Maintain
        return 'C'
    elif D_crit == 1:
        # You are the pivot: Pay for the reward
        return 'C'
    else:
        # Insufficient coordination: Conserve
        return 'D'
```
'''

description_OPPORTUNISTIC_19 = '''
### Strategy: Threshold-Conditional Opportunism

**Initialization (Round 1):**
Cooperate. The initial cooperation signals a willingness to engage in the cooperative threshold, establishing a baseline to observe the population's propensity for collaboration.

**Decision Rules (Rounds 2 to r-1):**
Let $C_{t-1}$ be the total number of cooperators observed in the previous round.
1.  **If I cooperated in $t-1$:**
    *   If $C_{t-1} \ge m$: Continue to Cooperate. The threshold is being met, and the payoff $k$ offsets the cost of contribution.
    *   If $C_{t-1} < m$: Defect. The group is failing to reach the threshold; continuing to contribute creates a net loss.
2.  **If I defected in $t-1$:**
    *   If $C_{t-1} \ge m$: Defect. The threshold is met without my contribution, allowing me to capture the maximum payoff ($1 + k$) while others bear the cost.
    *   If $C_{t-1} < m$: Defect. The group has failed to coordinate, and there is no evidence that switching back to cooperation will trigger a successful threshold outcome.

**Re-entry Mechanism:**
If the strategy has been defecting for $N$ consecutive rounds (where $N = 2$), attempt a "probe." In round $t$, play Cooperate.
*   If the resulting $C_t \ge m$, revert to the cooperative logic in rule (1) above.
*   If $C_t < m$, immediately return to Defect for the next round.

**Terminal Phase (Round r):**
Always Defect. Because the game ends, there is no future interaction to incentivize or punish, and no benefit to sustaining the collective threshold. The opportunistic goal is to maximize the final round payoff by avoiding the cost of contribution while capturing the benefit of the threshold if others cooperate.

**Pseudocode:**
```python
if round == r:
    return Defect

if round == 1:
    return Cooperate

# Check for probe
if consecutive_defects >= 2:
    consecutive_defects = 0
    return Cooperate

# Adaptive logic
if my_last_action == Cooperate:
    if last_round_cooperators >= m:
        return Cooperate
    else:
        consecutive_defects += 1
        return Defect
else:
    if last_round_cooperators >= m:
        return Defect
    else:
        consecutive_defects += 1
        return Defect
```
'''

description_OPPORTUNISTIC_20 = '''
**Phase 1: Initial Calibration (Round 1)**
Play Defect (D) to establish a baseline for the population's general inclination toward cooperation without risking the endowment. Observe the number of cooperators ($C_{obs}$) in the round.

**Phase 2: Opportunistic Threshold Tracking (Rounds 2 to r-1)**
Calculate the *Required Marginal Cooperation* ($RMC$), defined as $m - C_{obs}$.

*   If $C_{obs} \ge m$: The threshold is being met regardless of your contribution. Play Defect (D) to maximize your private payoff (the "free rider" opportunity).
*   If $C_{obs} == m - 1$: You are the "pivotal" player. If you play C, the threshold is met, yielding a payoff of $k$ (net gain: $k-1$). If you play D, the threshold is not met, yielding a payoff of 1 (net loss relative to contributing: $k-1$).
    *   Condition: If $k > 1$, play Cooperate (C). If $k \le 1$, play Defect (D).
*   If $C_{obs} < m - 1$: The group is failing significantly. Play Defect (D). Contributing $C$ is a sunk cost that will not reach the threshold $m$ without the coordination of others, which is not guaranteed.

**Phase 3: Terminal Round (Round r)**
In the final round, the incentive for future reciprocity is zero. Calculate the immediate payoff impact:
*   If $C_{obs} \ge m$ (from the previous round): Play Defect (D).
*   If $C_{obs} == m - 1$: Play Cooperate (C) if $k > 1$, else play Defect (D).
*   If $C_{obs} < m - 1$: Play Defect (D).

**Pseudocode Logic:**

```python
def play_round(round_number, n, m, k, history):
    if round_number == 1:
        return 'D'
    
    prev_round_C = history[-1].cooperators
    
    # Check if we are the pivot
    if prev_round_C == m - 1:
        return 'C' if k > 1 else 'D'
        
    # Otherwise, free-ride if possible, or conserve if group is hopeless
    return 'D'
```
'''

description_OPPORTUNISTIC_21 = '''
The strategy follows a "Conditional Tit-for-Tat with Threshold Sensitivity." It attempts to establish cooperation only when the group demonstrates enough capability to reach the threshold $m$, while defecting to capture the free-rider surplus $(k)$ when others are already carrying the cost.

**Core Logic:**
The agent maintains a variable `threshold_met_history` which tracks the number of rounds in which at least $m$ players cooperated. It also monitors the recent trend of cooperation ($C_{recent}$) to detect if the group is stable or collapsing.

**Decision Rules:**
1.  **Phase 1: Probing (Round 1):**
    *   Always play **C**. This establishes goodwill and signals potential for cooperation.

2.  **Phase 2: Evaluation (Rounds 2 to $r-1$):**
    *   Let $N_c$ be the number of cooperators in the previous round.
    *   **Defect (D) if:** $N_c \ge m + 1$. 
        *   *Opportunistic Rationale:* Since the threshold $m$ is already met, the contribution is unnecessary for collective success, and defecting maximizes individual payoff.
    *   **Cooperate (C) if:** $N_c == m$.
        *   *Opportunistic Rationale:* The threshold is met exactly. Any defection by a cooperator would cause the group to fail. Maintaining cooperation preserves the reward $k$.
    *   **Cooperate (C) if:** $N_c < m$.
        *   *Opportunistic Rationale:* The group is failing. Cooperate to attempt to push the group over the threshold $m$ to secure $k$. If after $t$ rounds of failed attempts (where $t$ is a tolerance threshold, e.g., 2), the group still fails to reach $m$, switch to **D** permanently for the remainder of the game to minimize personal losses.

3.  **Phase 3: Endgame (Final Round $r$):**
    *   If $N_c$ in round $r-1$ was $\ge m$, play **D**.
    *   If $N_c$ in round $r-1$ was $< m$, play **C** *if and only if* the probability of the group hitting $m$ is non-zero (i.e., $N_c \ge m-1$); otherwise, play **D**.

**Pseudocode:**

```python
# Parameters: n, m, k, r
# State: 
#   prev_n_cooperators = list of N_c values
#   failure_streak = 0

def get_action(current_round, prev_n_cooperators):
    if current_round == 1:
        return 'C'
    
    if current_round == r:
        if prev_n_cooperators[-1] >= m:
            return 'D'
        return 'C' if prev_n_cooperators[-1] >= m - 1 else 'D'

    last_N_c = prev_n_cooperators[-1]
    
    # Check for sustained failure to cooperate
    if last_N_c < m:
        failure_streak += 1
    else:
        failure_streak = 0
        
    if failure_streak >= 2:
        return 'D' # Abandon project; group is unreliable
        
    if last_N_c >= m + 1:
        return 'D' # Opportunistic free-riding
    
    return 'C' # Either threshold needs help or is currently exactly met
```
'''

description_OPPORTUNISTIC_22 = '''
The strategy operates as a conditional cooperator with a bias toward defection, aiming to ride the threshold of contribution without over-contributing.

### Decision Rules

1. **Initial Round (t=1):**
   Contribute (C) if the expected probability of others cooperating is low. Specifically, cooperate if $m/n > 0.5$, otherwise Defect (D). This tests the baseline cooperativeness of the population.

2. **Subsequent Rounds (t > 1):**
   Track the number of cooperators ($C_t$) from the previous round $t-1$.
   *   **Case 1: $C_{t-1} \ge m + 1$** (Threshold is easily met):
       Defect (D). Since the threshold was exceeded by at least one person, one can safely "free-ride" without risking the bonus $k$.
   *   **Case 2: $C_{t-1} == m$** (Threshold is exactly met):
       Defect (D). The threshold was achieved without your contribution; attempting to switch to D tests if the group can maintain the threshold without you.
   *   **Case 3: $C_{t-1} == m - 1$** (Threshold was missed by one):
       Cooperate (C). The group is on the verge of the bonus; your contribution is the pivot point to secure the reward $k$ for the current round.
   *   **Case 4: $C_{t-1} < m - 1$** (Threshold is far from met):
       Defect (D). The group is failing significantly. Contributing alone or with few others will not trigger the bonus $k$ and incurs the cost of contribution. Do not waste the endowment.

### Edge Cases and Transitions

*   **The "Last Round" (t=r):**
    If $C_{r-1} \ge m$, Defect (D). There is no future reputation cost to consider, so maximize immediate payoff. If $C_{r-1} < m$, cooperate (C) only if the payoff $k$ exceeds the cost of contribution (1), which is true given $k > 1$. Therefore, always cooperate in the final round if the previous round suggests there is a realistic chance of hitting $m$.
*   **Systemic Failure:**
    If the strategy observes $D$ in three consecutive rounds where the threshold was not met, switch to a "tit-for-tat" pattern for two rounds to signal potential cooperation, then revert to the primary logic.

### Pseudocode Implementation

```python
# Constants: m, n, k, r
# Memory: history of C_count

def decide_action(t, r, history):
    if t == 1:
        return 'C' if (m/n) > 0.5 else 'D'
    
    if t == r:
        # In the final round, prioritize securing k if plausible
        last_c = history[-1]
        return 'C' if last_c >= m - 1 else 'D'
    
    last_c = history[-1]
    
    if last_c >= m:
        return 'D' # Ride the success
    elif last_c == m - 1:
        return 'C' # Pivot to trigger reward
    else:
        # Check for systematic failure recovery
        if len(history) >= 3 and all(h < m for h in history[-3:]):
            return 'C' # Attempt to nudge
        return 'D' # Conserve resources
```
'''

description_OPPORTUNISTIC_23 = '''
Play the game using a Threshold-Triggered Opportunism strategy.

**Strategy Logic**

1.  **Phase 1: Calibration (Round 1)**
    Cooperate in the first round to test the collective willingness to meet the threshold $m$.

2.  **Phase 2: Adaptive Opportunism (Rounds 2 to $r-1$)**
    Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   **Conditional Cooperation:** If $C_{t-1} \geq m$, cooperate only if the marginal benefit of contributing is positive for the collective stability (i.e., you aim to maintain the threshold $m$ without over-contributing). Specifically, cooperate if $C_{t-1} = m$. If $C_{t-1} > m$, defect to maximize private gain, assuming the threshold is safely met by others.
    *   **Threshold Recovery:** If $C_{t-1} < m$, cooperate to attempt to pull the group toward the threshold $m$.
    *   **Switching:** If the previous round resulted in defection ($C_{t-1} < m$) and the current round continues to fail, persist in cooperating for a maximum of 2 consecutive rounds. If the threshold $m$ is not met after 2 rounds of attempted cooperation, switch to Defect for 1 round to punish non-cooperation or exploit the potential "sucker" status, then reset to the threshold-seeking behavior.

3.  **Phase 3: Terminal Opportunism (Round $r$)**
    Defect, regardless of previous history. Since there are no subsequent rounds, the game provides no incentive to influence future opponent behavior. Extract the maximum possible payoff by keeping the endowment.

**Pseudocode representation:**

```python
def choose_action(round_number, total_rounds, prev_cooperators, m):
    # Terminal phase: Always defect
    if round_number == total_rounds:
        return "D"
    
    # First round: Cooperate to signal and test
    if round_number == 1:
        return "C"
    
    # Adaptive logic
    if prev_cooperators >= m:
        # If threshold is met, act opportunistically
        if prev_cooperators == m:
            return "C" # Maintain threshold
        else:
            return "D" # Free-ride if threshold is safely exceeded
    else:
        # Threshold not met: Attempt to reach it
        return "C"
```

**Edge Case Handling:**
*   **Initialization:** If $m=0$, always defect. If $m > n$, always defect.
*   **Stagnation:** If the system detects a pattern of $C_{t-1} < m$ for more than 3 consecutive rounds, revert to pure Defect for the remainder of the game, as the group is unwilling to cooperate.
'''

description_OPPORTUNISTIC_24 = '''
**Threshold-Targeting Opportunism**

The strategy relies on a "trigger-threshold" mechanism that seeks to secure the reward $k$ at the lowest personal cost, while defecting when the threshold is either already met or impossible to meet given current play. 

**Decision Rules:**

In every round $t$, define $c_{t-1}$ as the number of cooperators observed in the previous round. If $t=1$, assume a baseline expectation $c_{0} = m-1$.

Let $S$ be the total number of cooperators in the previous round. The decision to cooperate ($C$) or defect ($D$) depends on the following logic:

1.  **First Round ($t=1$):** Play $C$. Establishing an initial signal of cooperation is necessary to encourage others to coordinate toward the threshold.
2.  **Subsequent Rounds ($t > 1$):**
    *   **If $S \geq m$:** Defect ($D$). Since the threshold $m$ is being met by others, the reward $k$ is guaranteed regardless of personal contribution. Maximizing individual payoff requires keeping the endowment.
    *   **If $S = m - 1$:** Cooperate ($C$). The threshold is one player away from being met. Contributing ensures the group crosses the threshold to trigger reward $k$, increasing the total payoff.
    *   **If $S < m - 1$:** Defect ($D$). When the gap is too large to be closed by one player, cooperation is wasted. Switch to $D$ to preserve the endowment until others increase their cooperation.
3.  **Final Round ($t = r$):** If the payoff accumulated in prior rounds is sufficient to maintain a dominant position, or if the game state indicates high variance, revert to the $S=m-1$ rule. If total expected reward $k$ cannot be achieved due to persistent defection by others ($S < m$ for consecutive rounds), play $D$ unconditionally to ensure the base endowment of 1 is kept.

**Pseudocode:**

```text
Initialize:
  my_action = C

For each round t = 1 to r:
  if t == 1:
    my_action = C
  else:
    observe S = number_of_cooperators_in_t_minus_1
    
    if S >= m:
      my_action = D
    else if S == m - 1:
      my_action = C
    else:
      my_action = D
      
  execute(my_action)
```

**Edge Case Handling:**

*   **Systemic Defection:** If the group fails to reach the threshold for two consecutive rounds, the strategy shifts to unconditional defection ($D$) for the remainder of the game. It is assumed the group will not coordinate; therefore, attempting to provide the marginal contribution is suboptimal.
*   **Threshold volatility:** If the observed cooperation fluctuates (e.g., $S$ bounces between $m$ and $m-2$), the strategy maintains the opportunistic stance: act only when necessary to trigger the reward ($S=m-1$) and free-ride whenever the threshold is already satisfied ($S \geq m$).
'''

description_OPPORTUNISTIC_25 = '''
The strategy follows a "Threshold-Targeting Tit-for-Tat" logic, prioritizing immediate payoff maximization while maintaining the cooperative threshold necessary to trigger the collective reward.

**Round 1:**
Contribute (C) if $n - 1 \geq m$. Otherwise, Defect (D). This tests if the group can sustain the threshold without relying on 100% participation.

**Subsequent Rounds:**
Let $C_{t-1}$ be the number of cooperators observed in the previous round.

1.  **Threshold Enforcement:**
    If the collective reward was triggered in the previous round ($C_{t-1} \geq m$):
    - If you cooperated ($c_{t-1} = 1$) and $C_{t-1} = m$: Continue to Defect (D). By being the player that drops out, you maximize your payoff (collecting the reward $k$ plus the endowment) while checking if the group can still meet the threshold without you.
    - If you cooperated ($c_{t-1} = 1$) and $C_{t-1} > m$: Continue to Defect (D). You are currently a "surplus" cooperator; withdrawing your contribution maximizes your payoff without jeopardizing the threshold.
    - If you defected ($c_{t-1} = 0$) and $C_{t-1} > m$: Continue to Defect (D). The threshold is met without you; maintain the high payoff.
    - If you defected ($c_{t-1} = 0$) and $C_{t-1} = m$: Switch to Cooperate (C). If you defected and the threshold was exactly met, the group failed to cover your portion; you must contribute to secure the reward $k$ in the next round.

2.  **Recovery/Reaction:**
    If the collective reward was *not* triggered in the previous round ($C_{t-1} < m$):
    - If $C_{t-1} = m - 1$: Switch to or maintain Cooperate (C). You are the marginal player needed to trigger the reward.
    - If $C_{t-1} < m - 1$: Defect (D). The group is too far from the threshold; contributing is a sunk cost with no reward.

**Final Round (Round $r$):**
Always Defect (D). Since there are no future rounds to influence or leverage, the dominant strategy is to keep the endowment and hope that others cooperate sufficiently to provide the reward.

**Edge Case Handling:**
- If $k \leq 1$: Always Defect (D). The reward is not worth the cost of contribution.
- If $m = n$: Always Cooperate (C) unless it is the final round, as any defection results in the loss of the reward $k$.
'''

description_OPPORTUNISTIC_26 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat (TSTFT)**

The strategy operates on a logic of conditional cooperation aimed at securing the reward $k$ while minimizing personal contributions when the contribution of others is sufficient to cross the threshold $m$.

**State Variables**
Let $c_{t-1}$ be the number of cooperators observed in the previous round.
Let $s_t$ be a state indicator: $s_t = 1$ if the threshold $m$ was met in the previous round, else $s_t = 0$.

**Decision Rules**

1.  **Initialization (Round 1):**
    Play **Cooperate (C)**. This signals a willingness to coordinate and establishes the community project.

2.  **Standard Operation (Rounds 2 to $r-1$):**
    Evaluate the previous round's outcome ($c_{t-1}$):
    *   **If $c_{t-1} \ge m$:**
        *   If the strategy cooperated in $t-1$: Play **Defect (D)**. This is the opportunistic pivot; if the threshold is met without your personal contribution, maximize private gain.
        *   If the strategy defected in $t-1$: Play **Cooperate (C)**. This serves as a "testing" mechanic to ensure the threshold is maintained, effectively fluctuating between C and D to maintain the $m$ cooperators without over-contributing.
    *   **If $c_{t-1} < m$:**
        *   Play **Cooperate (C)**. The threshold was not met; personal contribution is necessary to trigger the reward $k$.

3.  **Terminal Phase (Final Round $r$):**
    In the final round, ignore past reciprocation and prioritize the immediate reward:
    *   **If $c_{r-1} \ge m$:**
        *   If you played C in $r-1$, play **Defect (D)**.
        *   If you played D in $r-1$, play **Defect (D)**.
    *   **If $c_{r-1} < m$:**
        *   Play **Defect (D)**. In the final round, assuming no future iterations, the marginal gain of 1 from Defecting always exceeds the utility of contributing to a group that has already failed to sustain the threshold.

**Pseudocode**

```python
def decide_action(round_num, last_round_cooperators, my_last_action):
    if round_num == 1:
        return 'C'
    
    if round_num == r:
        return 'D'
    
    if last_round_cooperators >= m:
        # Opportunistic exploitation: If they can sustain it without me, stop paying
        if my_last_action == 'C':
            return 'D'
        # If I defected and it still worked, continue to defect (not strictly necessary but efficient)
        else:
            return 'D' 
    else:
        # Threshold not met, must contribute to trigger k
        return 'C'
```
'''

description_OPPORTUNISTIC_27 = '''
The strategy relies on a "conditional tit-for-tat with opportunistic thresholding" approach, balancing cooperation to secure the reward $k$ against defection to maximize individual gain when the threshold $m$ is comfortably met.

**Strategy Definition:**

1.  **Phase Initialization (Round 1):**
    Play **Cooperate**. This establishes a baseline of contribution and tests the aggregate cooperation level of the group.

2.  **Tracking State:**
    Maintain two variables throughout the game:
    *   $S_t$: The number of players who cooperated in round $t$.
    *   $C_{trend}$: A running average of cooperators over the previous three rounds (or available rounds if $t < 3$).

3.  **Round-by-Round Decision Logic (Rounds $t > 1$):**
    Determine the action for the current round based on the observed outcome of the previous round ($S_{t-1}$):

    *   **Case 1: Threshold Failure ($S_{t-1} < m$):**
        If the group failed to reach the threshold in the previous round, switch to **Cooperate** with probability $p = \min(1, \frac{m}{S_{t-1}+1})$. This signals a willingness to coordinate and attempts to incentivize others to cross the threshold.

    *   **Case 2: Threshold Success ($S_{t-1} \ge m$):**
        If the group succeeded in the previous round, analyze the "buffer" of the success:
        *   If $S_{t-1} > m$: The group has excess cooperation. Play **Defect**. This is the core opportunistic move to capture the reward $k$ while keeping the endowment.
        *   If $S_{t-1} == m$: The group is at the knife's edge of the threshold. If your own previous action was **Cooperate**, switch to **Defect** to test if the group can maintain $m$ without your contribution. If your own previous action was **Defect**, maintain **Defect** (you are a free-rider).

    *   **Case 3: Terminal Phase ($t = r$):**
        Regardless of history, always play **Defect**. In the final round, there is no future incentive for others to coordinate, so maximize individual payoff by keeping the endowment.

4.  **Adaptive Adjustment:**
    If at any point $C_{trend}$ drops below $m-1$ for two consecutive rounds, reset to **Cooperate** for one round regardless of the success/failure logic to attempt a "kickstart" of cooperative behavior. After the kickstart, return to the logic in step 3.

5.  **Edge Cases:**
    *   If $n = m$, play **Cooperate** in every round except the last. The threshold is too fragile to support opportunistic defection.
    *   If $r$ is small (e.g., $r < 3$), prioritize **Cooperate** to ensure the threshold is met, switching to **Defect** only in the final round.
'''

description_OPPORTUNISTIC_28 = '''
1. Initialization: Establish a target cooperation count, `T = m`. Initialize `total_cooperators_history` as an empty list.

2. Strategy Logic:
   At each round `t`, determine the action based on the observation of the previous round `t-1`. If `t=1`, play `C`. For `t > 1`, let `C_{t-1}` be the number of cooperators observed in the previous round.

   - If `C_{t-1} >= m + 1`: 
     Play `D`. Since the collective goal is already achieved by others, the reward `k` is secured regardless of personal contribution. Defection maximizes immediate payoff without endangering the threshold reward.

   - If `C_{t-1} == m`:
     Play `D`. The threshold is met exactly. If the player plays `D`, they maximize their individual payoff while maintaining the collective threshold.

   - If `C_{t-1} < m`:
     Play `C` with probability `p`, where `p` is defined as `(m - C_{t-1}) / (n - C_{t-1})`. This proportional response mimics "tit-for-tat" style reinforcement, providing just enough contribution to push the group toward `m`, assuming other agents are rational. If `m` is reached, immediately switch to `D` in the next round.

3. Edge Cases and End-Game:
   - Round `r` (Final Round): Regardless of history, if the expected contribution of others is less than `m`, play `C` only if the probability of the group failing to reach `m` is high. Otherwise, prioritize `D`. If `C_{t-1} >= m`, always play `D`.
   - If `C_{t-1}` is consistently 0 across rounds, the group is uncooperative. After 3 rounds of `0` cooperation, switch to permanently playing `D` for the remainder of the game, as investment in a non-responsive group results in a cumulative loss of `1` per round.

4. Pseudocode:
   ```
   def get_action(round_number, prev_cooperators, n, m):
       if round_number == 1:
           return C
       
       # Check for non-responsive group
       if round_number > 3 and all_past_cooperation_was_zero:
           return D
           
       if prev_cooperators >= m:
           return D
           
       # Calculate required effort
       needed = m - prev_cooperators
       others_available = n - 1 # excluding self
       
       if rand(0,1) < (needed / others_available):
           return C
       else:
           return D
   ```
'''

description_OPPORTUNISTIC_29 = '''
**Strategy: Conditional Threshold-Opportunist**

This strategy maximizes total payoffs by attempting to be a "minimal contributor" when the threshold is safe and defecting when the threshold is already met or impossible to reach.

**Initialization and Phase Identification**

1.  **First Round:** Play **Cooperate (C)** with probability $m/n$. This establishes an initial investment to signal willingness to participate in reaching the collective threshold $m$.
2.  **Subsequent Rounds ($t > 1$):**
    *   Calculate the number of cooperators from the previous round ($C_{t-1}$).
    *   Define "Required Cooperators" as $m$.
    *   Define "Current Defection Incentive" as $k - 1$. If $k-1 \le 0$, the structure favors cooperation; if $k-1 > 0$, defection is the dominant strategy once the threshold is met.

**Decision Logic**

Execute the following pseudocode at the start of each round $t \in [2, r]$:

```python
def decide_action(t, r, n, m, k, last_round_cooperators):
    # Determine state of the collective
    threshold_met = last_round_cooperators >= m
    
    # 1. Last Round Defection
    # If it is the final round, always Defect (D) to maximize private gains,
    # as there is no future incentive to maintain cooperation.
    if t == r:
        return 'D'

    # 2. Threshold Exploitation
    # If the threshold was met in the previous round, attempt to free-ride.
    if threshold_met:
        # If I cooperated last round, try switching to Defect (D) to test 
        # if the collective threshold holds without me.
        # If I defected last round, stay Defect (D).
        return 'D'
    
    # 3. Threshold Recovery
    # If the threshold was NOT met in the previous round:
    else:
        # If the number of cooperators was close (m - 1), 
        # switch to Cooperate (C) to tip the balance.
        if last_round_cooperators == m - 1:
            return 'C'
        
        # If the number of cooperators was far below m, assume the group 
        # is uncooperative. Defect (D) to minimize personal loss.
        else:
            return 'D'
```

**Edge Case Handling**

*   **Under-performance:** If $C_{t-1} < m - 1$ for three consecutive rounds, the strategy enters a "Dormant Defection" mode: always play **Defect (D)** for the remainder of the game to preserve the endowment, as the group is deemed incapable of reaching the threshold.
*   **Threshold volatility:** If the number of cooperators fluctuates around $m$, prioritize maintaining $C$ only if $k$ is sufficiently high (specifically, if the gain $k$ outweighs the cost of 1). If $k \le 1$, default to **Defect (D)** in all rounds.
'''

description_OPPORTUNISTIC_30 = '''
The strategy operates on a conditional "Tit-for-Tat with Threshold Sensitivity" logic, designed to maximize immediate rewards by free-riding whenever safe, but switching to cooperation when the community threshold is at risk of failure.

**Decision Rules**

In each round $t \in \{1, \dots, r\}$, let $C_{t-1}$ be the number of cooperators observed in the previous round.

1.  **If $t = 1$:** Play **Cooperate (C)**. This signals a willingness to coordinate and establishes a baseline for potential reciprocity.

2.  **If $t > 1$:**
    *   **Condition A (Free-riding Opportunity):** If $C_{t-1} \ge m + 1$, play **Defect (D)**. This exploits the fact that the threshold $m$ is already met by others, allowing you to maximize private payoff ($1+k$) while others carry the burden of the project.
    *   **Condition B (Threshold Support):** If $C_{t-1} = m$, play **Defect (D)**. While the threshold is currently met, this is the "tipping point." However, because playing C would result in a payoff of $k$ (loss of endowment) and playing D results in $1+k$ (keeping endowment plus reward), defection remains the dominant strategy when the threshold is exactly met, assuming others will continue to provide the minimum support.
    *   **Condition C (Threshold Failure Recovery):** If $C_{t-1} < m$, play **Cooperate (C)**. This indicates that the collective project is currently failing. You shift to cooperation to attempt to push the total count to $m$ in the next round, salvaging the $k$ reward.

**End-Game Heuristic**

As the game approaches the final round ($t = r$), the strategy shifts to protect self-interest over collective stability:

*   **Final Round ($t = r$):** Play **Defect (D)**, regardless of the observed history. Since there are no future rounds to incentivize or punish other players, the only rational choice is to maximize the payoff of the final round by keeping the endowment, provided the total cooperation count remains $\ge m$. If previous rounds suggest the threshold will fail regardless of your contribution, D is the only outcome that minimizes the loss of your endowment.

**Summary Pseudocode**

```python
if t == 1:
    return C

if t == r:
    return D

# History-based logic for middle rounds
observed_cooperators = get_last_round_count()

if observed_cooperators >= m:
    return D # Free-ride if threshold is safe
else:
    return C # Contribute if project is failing
```
'''

description_OPPORTUNISTIC_31 = '''
**Decision Logic**

The strategy follows a conditional, threshold-based logic designed to exploit cooperation when the threshold $m$ is likely to be met without needing personal contribution, while ensuring the threshold is met only when necessary to secure the reward.

*   **Round 1:** Play **Defect (D)**. This establishes a baseline for the collective's inclination to contribute without risking a personal endowment.

*   **Subsequent Rounds (2 to $r$):**
    *   Let $C_{t-1}$ be the number of cooperators in the previous round.
    *   **Case 1: $C_{t-1} \ge m$**. The threshold is being met by others. Play **Defect (D)** to maximize personal gain (free-riding).
    *   **Case 2: $C_{t-1} = m - 1$**. The group is exactly one cooperator shy of the threshold. Play **Cooperate (C)** to trigger the collective reward $k$. This maximizes immediate payoff, as $0 + k > 1$.
    *   **Case 3: $C_{t-1} < m - 1$**. The group is far from the threshold. Playing $C$ is unlikely to result in $m$ cooperators, making the $k$ reward unattainable. Play **Defect (D)** to preserve endowment.

**Final Round Exception**

*   In the final round $t = r$:
    *   If the strategy expects the threshold $m$ to be met by others (based on the trend of $C_{t-1}$), play **Defect (D)**.
    *   If the strategy calculates that playing **Cooperate (C)** is the *only* way to reach the threshold $m$ (i.e., $C_{t-1} = m - 1$), play **Cooperate (C)** to capture the final reward.

**Pseudocode**

```python
def decide_action(round_number, m, history):
    if round_number == 1:
        return 'D'
    
    previous_cooperators = history.last_round_cooperators
    
    # Check if we can trigger the reward by cooperating
    if previous_cooperators == (m - 1):
        return 'C'
    
    # If we are far from the threshold, conserve resources
    if previous_cooperators < (m - 1):
        return 'D'
    
    # If threshold is already met by others, free-ride
    if previous_cooperators >= m:
        return 'D'
```

**Opportunistic Considerations**

This strategy assumes that other players may be inconsistent or cooperative. By waiting for $C_{t-1} = m - 1$ before committing, the agent avoids "wasted" cooperation where the threshold is not met. It prioritizes the highest possible individual payoff ($1+k$) by only providing the minimum required input when that input is guaranteed to unlock the threshold reward. If the group consistently fails to reach $m-1$, the agent remains a pure defector to avoid unnecessary loss of endowment.
'''

description_OPPORTUNISTIC_32 = '''
### Strategy: Threshold-Conditional Opportunism

**Initialization (Round 1):**
Play **Cooperate (C)**. This establishes a baseline contribution to gauge the collective cooperation level without immediately triggering a defection equilibrium.

**Observation Phase:**
In each round $t > 1$, track $C_{t-1}$, the number of players who chose to cooperate in the previous round. Define $S_t$ as the success state of round $t-1$: $S_t = 1$ if $C_{t-1} \ge m$, else $S_t = 0$.

**Decision Rules (Rounds 2 to $r-1$):**
If $S_t = 0$:
Switch to **Defect (D)**. If the group fails to meet the threshold, contributing is purely loss-making. Defecting secures the higher private payoff ($1$) while attempting to signal that the cooperative threshold was not reached.

If $S_t = 1$:
Evaluate the marginal cooperation:
- If $C_{t-1} > m$: Play **Defect (D)**. The threshold $m$ is exceeded safely; you are an opportunistic free-rider in a surplus of cooperators.
- If $C_{t-1} = m$: Play **Cooperate (C)**. You are critical to the threshold. Defecting would cause the group to fail, reducing your payoff from $1+k$ to $1$. Maintaining the threshold is necessary to secure the reward $k$.

**Terminal Phase (Round $r$):**
If $C_{r-1} \ge m$:
Play **Defect (D)**. In the final round, there is no future reputation cost for failing to contribute. If the previous round was a success, maximize the private payoff immediately regardless of the current threshold state.

If $C_{r-1} < m$:
Play **Defect (D)**. Since the collective failed in the previous round and this is the final round, the probability of the group suddenly coordinating to meet $m$ is negligible. Minimize personal loss.

**Summary Pseudocode:**
```python
def choose_action(round_number, total_rounds, prev_cooperators, m):
    if round_number == 1:
        return 'C'
    
    if round_number == total_rounds:
        return 'D'
    
    if prev_cooperators < m:
        return 'D'
        
    if prev_cooperators == m:
        return 'C'
        
    if prev_cooperators > m:
        return 'D'
```
'''

description_INDIVIDUALISTIC_5 = '''
Let $C_t$ be the number of players who cooperated in round $t$. Let $c_{i,t} \in \{0, 1\}$ be the player’s own action in round $t$. Let $M_t$ be the number of cooperators among opponents in round $t$ (where $M_t = C_t - c_{i,t}$).

**Decision Rule:**

1.  **Round 1:** Play $C$ if the expected return on cooperation is positive. Calculate the expected probability of success $P(M_1 \ge m-1)$ based on a uniform prior regarding opponent cooperation rates. Play $C$ if $k \cdot P(M_1 \ge m-1) > 1$. Otherwise, play $D$.

2.  **Subsequent Rounds ($t > 1$):**
    *   If $t = r$ (final round): Play $D$. There is no future incentive to maintain a reputation or induce cooperation.
    *   If $t < r$: Calculate the observed cooperation rate of the population, defined as the moving average of opponent cooperation $\bar{M} = \frac{1}{t-1} \sum_{j=1}^{t-1} \frac{M_j}{n-1}$.
    *   If $\bar{M} \cdot k > 1$: Play $C$ if $M_{t-1} \ge m-1$. This is a conditional cooperation strategy (tit-for-tat variant) meant to sustain a cooperative equilibrium where the threshold $m$ is met, provided the collective group is currently meeting the threshold.
    *   If $\bar{M} \cdot k \le 1$ or if the threshold $m$ was not met in the previous round ($C_{t-1} < m$): Play $D$. Switch to defection to avoid "sucker" payoffs when the collective group fails to sustain the threshold.

**Edge Cases:**

*   **Failure Recovery:** If the strategy has been playing $D$ due to past failures but the group suddenly cooperates at or above the threshold $m$ in round $t-1$, reset to $C$ in round $t$ to test if the group has returned to a cooperative norm.
*   **Threshold Vulnerability:** If $M_{t-1} = m-1$ (meaning the threshold was met exactly by others), play $C$ regardless of previous history to ensure the threshold $m$ is maintained for the current round, securing the reward $k$ for the group and yourself.
*   **Tie-breaking:** If at any point the calculation is indifferent (e.g., $k \cdot P = 1$), play $D$ to preserve the endowment.

**Pseudocode:**

```python
def get_action(t, r, n, m, k, history):
    if t == r:
        return D
    
    if t == 1:
        # Initial threshold check against uniform prior 0.5
        prob_success = calculate_binomial_cdf(n-1, m-1, 0.5)
        return C if (k * prob_success > 1) else D

    last_round_cooperators = history.last().total_cooperators
    last_round_opponents_coop = last_round_cooperators - history.last().my_action
    
    # Check if threshold was met
    threshold_met = (last_round_cooperators >= m)
    
    # Conditional cooperation logic
    if threshold_met:
        # If group is currently functioning, contribute to sustain it
        return C
    else:
        # If group failed, defect to save endowment
        return D
```
'''

description_INDIVIDUALISTIC_6 = '''
Maintain an internal state variable `cooperation_count` representing the number of opponents who cooperated in the previous round, and `active_cooperators` tracking an estimate of the expected cooperation level from the pool.

**Phase 1: Initial Calibration (Round 1)**
Play C (Cooperate). This establishes a baseline and tests for the presence of other conditional cooperators.

**Phase 2: Adaptive Response (Rounds 2 through r-1)**
Calculate the probability of the threshold `m` being met based on the history of cooperation. Let `total_cooperators` be the sum of C-moves from the previous round (including one's own).

If `total_cooperators` >= `m`:
Defect (D) if and only if the number of cooperators was strictly greater than `m`. If the number of cooperators was exactly `m`, continue to Cooperate (C) to maintain the threshold.

If `total_cooperators` < `m`:
If the previous outcome failed to meet the threshold, switch to C. If the previous outcome met the threshold but relied on your own cooperation (i.e., `total_cooperators` was exactly `m`), continue to C. If the previous outcome met the threshold without your cooperation (i.e., `total_cooperators` was strictly greater than `m` while you defected), continue to Defect (D) to maximize personal payoff.

**Phase 3: The Endgame (Round r)**
In the final round, the incentive to maintain long-term cooperation vanishes. Ignore previous history and switch to Defect (D) regardless of prior rounds, as there are no future consequences to failing to contribute.

**Pseudocode Logic:**

```python
if round == r:
    return D

# Observe previous round data
c_prev = total_cooperators_previous_round

if c_prev >= m:
    # Threshold met last round
    if my_last_move == C:
        # Check if threshold would have been met without me
        if (c_prev - 1) >= m:
            return D
        else:
            return C
    else: # my_last_move == D
        return D
else:
    # Threshold failed last round
    return C
```

**Edge Case Handling:**
- If at any point the pool of cooperators drops below `m - 1` such that the threshold is impossible to hit, immediately switch to Defect (D) for all remaining rounds to minimize endowment loss.
- If the threshold `m` is met exactly by the players, adopt a "tit-for-tat" reinforcement stance: reward the system with continued cooperation to keep the reward `k` active, but defect the moment the safety buffer (`total_cooperators > m`) allows.
'''

description_INDIVIDUALISTIC_7 = '''
The strategy employs a "Threshold-Targeted Tit-for-Tat" mechanism designed to maximize individual utility by conditioning cooperation on the observed minimum threshold of the previous round.

**Decision Rules:**

1.  **Initialization:** In round 1, play **Defect (D)**. This establishes a baseline and prevents immediate exploitation in an unknown environment.

2.  **State Tracking:** Maintain a variable $S_{t-1}$, representing the number of cooperators in the previous round.

3.  **Round-by-Round Logic:**
    *   If $t = r$ (the final round): Play **Defect (D)** regardless of history, as there is no future incentive to incentivize cooperation.
    *   If $1 < t < r$:
        *   If $S_{t-1} \ge m$: Play **Cooperate (C)**. The group has demonstrated the capacity to clear the threshold; contributing ensures the $k$ reward is secured without risking the endowment on a failed collective effort.
        *   If $S_{t-1} < m$: Play **Defect (D)**. If the threshold was not met, contributing is irrational as it guarantees a loss of the endowment (1) without receiving the reward ($k$). Defecting secures the guaranteed 1.

**Refinement for Adaptive Play:**

*   **Forgiveness/Recalibration:** If the strategy has been defecting due to a history of failure ($S_{t-1} < m$), introduce a "Probe" mechanism every $x$ rounds (where $x = \lceil r/4 \rceil$). In these probe rounds, play **Cooperate (C)** once to test if the aggregate group behavior has shifted toward cooperation.
*   **The "Near-Miss" Rule:** If $S_{t-1} = m - 1$ and the previous action was **Defect (D)**, switch to **Cooperate (C)** in the subsequent round. This acknowledges that the threshold was nearly met and acts as an attempt to bridge the gap and trigger the reward ($k$) for the group. If this action fails (i.e., $S_{t} < m$), immediately revert to **Defect (D)** for the following round.
'''

description_INDIVIDUALISTIC_8 = '''
**Strategy: Conditional Threshold Thresholding (CTT)**

**Parameters and Variables:**
*   $T$: The round number (1 to $r$).
*   $C_{t-1}$: Number of cooperators observed in the previous round.
*   $S_t$: My action in round $t$ (1 for C, 0 for D).
*   $m$: Minimum cooperators needed.
*   $n$: Total players.
*   $k$: Reward factor.

**Decision Logic:**

1.  **Initialization (Round 1):**
    *   Play $C$ (1) if $(k - 1) > (n-m)/n$ (the expected utility of cooperating is positive assuming a uniform distribution of opponent play). If this condition fails, play $D$ (0).

2.  **Iterative Adjustment (Rounds 2 to $r-1$):**
    *   If $C_{t-1} \ge m$: The threshold was met. Continue playing $C$ (1) if $C_{t-1} > m$ (a buffer exists). If $C_{t-1} = m$, play $D$ (0) to maximize individual gain (the "free-rider" check).
    *   If $C_{t-1} < m$: The threshold was not met.
        *   If the previous play was $C$ (1) and result was failure, switch to $D$ (0) to minimize personal loss.
        *   If the previous play was $D$ (0) and result was failure, maintain $D$ (0) unless the total failures over the last 3 rounds exceed a threshold of 2, in which case play $C$ (1) to test if the group is capable of coordination.

3.  **Terminal Phase (Round $r$):**
    *   Regardless of previous history, play $D$ (0) if $C_{r-1} \ge m$ (assuming the threshold is met, extract the maximum payoff without contributing).
    *   If $C_{r-1} < m$, play $D$ (0) (the game ends, contributing cannot influence future outcomes).

**Pseudocode Representation:**

```python
def decide_action(t, C_last, my_last_action):
    # Initialization
    if t == 1:
        return 1 if (k - 1) > ((n - m) / n) else 0

    # Terminal Round
    if t == r:
        return 0

    # Iterative Rounds
    if C_last >= m:
        # Threshold met: exploit if possible
        if C_last == m:
            return 0
        else:
            return 1
    else:
        # Threshold not met: react to previous failure
        if my_last_action == 1:
            return 0
        else:
            # Check for recent failures (local history window of 3)
            if recent_failures_count(3) >= 2:
                return 1
            else:
                return 0
```
'''

description_INDIVIDUALISTIC_9 = '''
The strategy follows a "Conditional Tit-for-Tat with Threshold Sensitivity." It maximizes individual payoffs by leveraging the specific gap between the cost of contribution (1) and the reward (k). Since k > 1, contributing is profitable only if it is necessary to reach the threshold *m* or if the resulting payoff (k) outweighs the cost (1).

**Decision Rule Framework:**

1.  **First Round:**
    Play **C** if *m* / *n* <= 0.5 (indicating a lower barrier to entry). Play **D** if *m* / *n* > 0.5 (indicating a high barrier to entry).

2.  **Subsequent Rounds:**
    Observe the number of cooperators *C_total* from the previous round.

    *   **If you played C in the previous round:**
        *   If *C_total* >= *m*: You are in a "cooperative equilibrium." Play **C**.
        *   If *C_total* == *m* - 1: You are the "pivotal" cooperator. Play **C** to maintain the threshold.
        *   If *C_total* < *m* - 1: The cooperative effort is failing. Switch to **D** to minimize losses.

    *   **If you played D in the previous round:**
        *   If *C_total* >= *m*: The threshold is being met without your contribution. Continue to play **D** (free-riding).
        *   If *C_total* == *m* - 1: You are the "pivotal" cooperator needed to trigger the reward. Play **C** to shift the group into the reward state, then revert to **D** next round to test if the group sustains itself.
        *   If *C_total* < *m* - 1: The threshold is too far away. Continue to play **D**.

3.  **Last Round (Round *r*):**
    Regardless of history, calculate the marginal utility.
    *   If current *C_total* (from round *r-1*) is *m* - 1 or *m*: Play **C** to secure the final reward *k*.
    *   If *C_total* < *m* - 1: Play **D**, as the collective threshold is unattainable.
    *   If *C_total* >= *m*: Play **D**, as the threshold is already secured.

**Pseudocode:**

```python
def decide_action(round_num, history, n, m, k):
    if round_num == 1:
        return 'C' if (m / n) <= 0.5 else 'D'
    
    if round_num == r:
        prev_C = history.last_round_cooperators
        if prev_C >= m - 1:
            return 'C'
        else:
            return 'D'

    prev_action = history.my_last_action
    prev_C = history.last_round_cooperators

    if prev_action == 'C':
        if prev_C >= m - 1:
            return 'C'
        else:
            return 'D'
            
    if prev_action == 'D':
        if prev_C == m - 1:
            return 'C'
        else:
            return 'D'
```
'''

description_INDIVIDUALISTIC_10 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Discounted Forgiveness**

This strategy prioritizes securing the threshold reward $m$ while minimizing individual contribution costs, adjusting cooperation based on the collective behavior observed in the previous round.

**1. Definitions and Initialization**
*   Let $N_c(t)$ be the number of cooperators observed in round $t$.
*   Let $P(t)$ be the probability of cooperating in round $t$, initialized to $1.0$ if the player is designated as a "starter" in a random initial distribution to break ties, or $0.5$ otherwise.
*   Let $History$ be the record of $N_c(t)$ for all prior rounds.

**2. Decision Rules**
For any round $t$ where $1 < t \le r$:
*   If $N_c(t-1) \ge m$: The collective threshold was met. Act to minimize individual costs while maintaining the threshold.
    *   If the strategy cooperated in $t-1$: Defect (D).
    *   If the strategy defected in $t-1$: Cooperate (C) with probability $\frac{m}{n}$ to test the threshold boundary.
*   If $N_c(t-1) < m$: The collective threshold was not met. Act to incentivize cooperation.
    *   If $N_c(t-1) \ge m - 1$: Cooperate (C) to bridge the gap and trigger the reward for all.
    *   If $N_c(t-1) < m - 1$: Defect (D). There is insufficient collective momentum to make contribution rational; preserve endowment.

**3. Edge Cases and Temporal Adjustments**
*   **Round 1:** Always Cooperate (C). Establishing a cooperative signal is necessary to determine if the group has the capacity to reach $m$.
*   **Final Round ($t=r$):**
    *   If $N_c(r-1) \ge m - 1$: Cooperate (C). The final round offers no future repercussions, so contribute only if it guarantees the threshold is met for the immediate payoff $k$.
    *   If $N_c(r-1) < m - 1$: Defect (D). The threshold is unreachable; maximizing individual payoff is the only remaining utility.

**4. Pseudocode Representation**
```python
if t == 1:
    return C

if t == r:
    if N_c(t-1) >= m - 1:
        return C
    else:
        return D

if N_c(t-1) >= m:
    if last_action == C:
        return D
    else:
        return C if random() < (m / n) else D

if N_c(t-1) == m - 1:
    return C

return D
```
'''

description_INDIVIDUALISTIC_11 = '''
**Strategic Framework: Adaptive Threshold Monitoring**

**Decision Rule**

In every round $t$, calculate the current total number of cooperators observed in the previous round, $O_{t-1}$. Your action $A_t$ is determined by the following logic:

1.  **Round 1:** Play $C$ if $(k-1) > 0$ and $(n-1) \ge m$. Otherwise, play $D$.
2.  **Round $t$ (where $1 < t \le r$):**
    *   If $O_{t-1} \ge m$: Play $D$. You have successfully identified that the group threshold is being met without your specific contribution. By defecting, you maximize your individual payoff ($\pi_i = 1+k$) while others carry the cost.
    *   If $O_{t-1} = m-1$: Play $C$. You are the pivotal player. By contributing, you trigger the reward $k$ for everyone, securing your own net gain of $(k-1)$. Since $k > 1$, this ensures a positive return.
    *   If $O_{t-1} < m-1$: Play $D$. The threshold is too far from being reached. Contributing is a "sunk cost" that will not trigger the reward $k$. Minimize losses by retaining your endowment.

**Last Round Logic**

In the final round $r$, apply the same logic as above. Since there are no future rounds to influence, reputation or punishment is irrelevant. If the observed cooperation from round $r-1$ was $\ge m$, defect. If it was $m-1$, cooperate only if you calculate that your contribution is guaranteed to push the group over the threshold to obtain $k$.

**Edge Cases**

*   **Failed Thresholds:** If the game continues for multiple rounds and the threshold is never met ($O_{t-1} < m$ for all $t$), continue to play $D$ indefinitely. Do not attempt to "signal" cooperation; signal-based coordination is unreliable in anonymous settings and wastes resources.
*   **Threshold Shift:** If $O_{t-1}$ fluctuates around $m-1$ and $m$, treat every round as an isolated event. Do not assume that past cooperation guarantees future cooperation. Base the decision strictly on the most recent observation $O_{t-1}$.
*   **Ties/Indifference:** If $(k-1) \le 0$, the dominant strategy is always $D$ regardless of the threshold, as the cost of cooperation exceeds the reward. In this scenario, play $D$ in all rounds.
'''

description_INDIVIDUALISTIC_12 = '''
Define the target contribution threshold $T = m$. In each round $t$, track the number of cooperators observed in the previous round, denoted $C_{t-1}$.

**Decision Rule:**

1.  **Phase 1 (Initialization):** In round 1, play **Cooperate (C)**. This tests the aggregate responsiveness of the group.

2.  **Phase 2 (Adaptive Coordination):** For all rounds $t > 1$:
    *   Let $N_C$ be the number of cooperators in round $t-1$.
    *   If $N_C \geq T$ (the threshold was met):
        *   If I played **C** in $t-1$, play **C** again.
        *   If I played **D** in $t-1$, play **D** again (the threshold is met without my contribution).
    *   If $N_C < T$ (the threshold was not met):
        *   Calculate the deficit $D = T - N_C$.
        *   If I played **C** in $t-1$, check if $D=1$. If $D=1$, this implies my contribution was pivotal; play **C** again to sustain the threshold. If $D > 1$, play **D** (the group is failing to reach the threshold, and my single contribution is insufficient to bridge the gap).
        *   If I played **D** in $t-1$, check if $D=1$. If $D=1$, playing **C** guarantees the threshold is met; play **C**. If $D > 1$, play **D**.

**Phase 3 (End-Game Termination):**
*   In the final round $r$:
    *   If the strategy dictates playing **C** based on the rules above, play **C**.
    *   If the strategy dictates playing **D**, play **D** unless $N_C = T-1$ from round $r-1$. In this specific case, play **C** to capture the reward $k$ one last time, as there is no future round to punish defection.

**Summary Pseudocode:**

```
// Round 1
Action = C

// Rounds 2 to r
// Let T = m, N = cooperators in previous round, prev_action = my previous action

if N >= T:
    Action = prev_action
else:
    deficit = T - N
    if (prev_action == C and deficit == 1) or (prev_action == D and deficit == 1):
        Action = C
    else:
        Action = D
        
// Final Round Exception
if t == r and Action == D and N == T - 1:
    Action = C
```
'''

description_INDIVIDUALISTIC_13 = '''
**Strategy: Adaptive Threshold-Trigger (ATT)**

**Phase 1: Initialization**
In the first round (t=1), play **Cooperate (C)**.

**Phase 2: Monitoring and Adaptation**
From round t=2 to r, track the aggregate cooperation count (S) from the previous round (t-1). Let S_{t-1} be the number of players who played C in the previous round.

Decision rule for round t:

1.  **If the threshold was met in the previous round (S_{t-1} ≥ m):**
    *   If S_{t-1} > m, play **Defect (D)**. This exploits the surplus cooperation while maintaining the threshold.
    *   If S_{t-1} == m, play **Cooperate (C)**. This maintains the threshold exactly.

2.  **If the threshold was not met in the previous round (S_{t-1} < m):**
    *   If S_{t-1} == m - 1, play **Cooperate (C)**. This attempts to pull the group above the threshold.
    *   If S_{t-1} < m - 1, play **Defect (D)**. Since the group is far from reaching the threshold, contributing is a sunk cost. Do not waste the contribution.

**Phase 3: Terminal Phase**
In the final round (t=r):
*   If the aggregate behavior in the previous rounds suggests a consistent failure to reach the threshold (e.g., S < m in the last three rounds), play **Defect (D)** unconditionally.
*   If the aggregate behavior suggests a consistent success, play **Defect (D)**, as the lack of future rounds removes the incentive to maintain group cooperation.

**Edge Case Logic:**
*   If multiple players defect such that the group falls below the threshold, revert to **Defect (D)** for exactly one round to signal intolerance for free-riding, then attempt to restore cooperation in the subsequent round if the group dynamics stabilize.
*   If at any point π_i (from the previous round) > 1 + k, indicating that the threshold was met and others defected, switch to **Defect (D)** for one round to prevent being the sole cooperator.
'''

description_INDIVIDUALISTIC_14 = '''
Initialize a local tracking variable `cooperation_history` as an empty list.

1. First Round:
Always defect (D).

2. Subsequent Rounds (t > 1):
Calculate the observed cooperation rate of the opponents in the previous round, `prev_m = (coop_count_t-1)`. If I played Cooperate (C) in round `t-1`, `prev_m` includes my contribution; if I played Defect (D), it does not. Adjust the opponent contribution count to reflect only their actions.

3. The "Conditional Threshold" Decision Rule:
Define a target threshold for cooperation `T = m`.
In round `t`, determine the action based on the behavior observed in round `t-1`:

    If `prev_m` ≥ `T`:
        Play Cooperate (C) if I contributed to the success of the previous round (i.e., I played C and the total was ≥ `m`) or if I defected but the total was > `m` (indicating a surplus of contributors).
        Play Defect (D) if I defected in the previous round and the total was exactly equal to `m` (indicating my contribution is required to maintain the threshold).

    If `prev_m` < `T`:
        Play Defect (D). If the collective fails to meet the threshold, the most individualistically rational act is to retain the endowment rather than waste it on a failed outcome.

4. Last Round Adjustment:
In the final round (round `r`), play Defect (D) regardless of previous history. Since there are no future rounds to influence, defecting is the dominant strategy to maximize the single-round payoff.

5. Pseudocode Representation:
```
// Global state
coop_history = [] 

// Decision function
function get_action(t, r, m, k, prev_opp_c):
    if t == r:
        return D
    if t == 1:
        return D
    
    // Check if opponents reached threshold in previous round
    if prev_opp_c >= m:
        // Attempt to sustain or free-ride slightly
        return C 
    else:
        // Threshold not met, do not waste endowment
        return D
```
'''

description_INDIVIDUALISTIC_15 = '''
### Strategy: Threshold-Conditional Reciprocity

**1. Initial Phase (Round 1)**
Play **Defect (D)**. This establishes a baseline of self-preservation, ensuring that if the group fails to reach the threshold, the cost of contribution is not borne unilaterally.

**2. Recursive Decision Rule (Rounds 2 to r-1)**
For any round *t*, let *C_{t-1}* be the number of cooperators observed in the previous round.

*   **Case A: Threshold Met (C_{t-1} ≥ m)**
    If the threshold was met in the previous round, check your own action in *t-1*.
    *   If you played **C** in *t-1*: Repeat **Cooperate (C)**. This maintains the cooperative equilibrium necessary for the group reward *k*.
    *   If you played **D** in *t-1*: Switch to **Cooperate (C)**. By failing to contribute previously, you successfully free-rode; now, you switch to support the threshold to secure the reward *k* for the next round.

*   **Case B: Threshold Failed (C_{t-1} < m)**
    If the threshold was not met in the previous round, assume the group is currently uncooperative or insufficient.
    *   If *C_{t-1} < m-1*: Switch to or remain in **Defect (D)**. The probability of reaching the threshold *m* by switching your action alone is zero; therefore, contributing is a guaranteed loss.
    *   If *C_{t-1} = m-1*: Switch to **Cooperate (C)**. You are the "pivotal" player. Contributing pushes the group to the threshold *m*, securing the payoff *k* (where *k > 1*), which is strictly greater than the private endowment of 1.

**3. Terminal Phase (Round r)**
*   If *C_{r-1} ≥ m*: Play **Cooperate (C)**. The group has demonstrated viability, and the collective reward *k* is likely to be triggered if you contribute.
*   If *C_{r-1} < m*: Play **Defect (D)**. In the final round, there is no future reputation to gain or risk to avert; the endowment is strictly more valuable than the gamble of contributing when the threshold was previously missed.
'''

description_INDIVIDUALISTIC_16 = '''
Define the cooperation threshold $T$ as $m$. Initialize the state variable $S_{coop} = 0$, representing the total number of cooperative actions observed in previous rounds.

**Decision Rules:**

For any round $t$ where $1 \le t < r$:
1. If $t = 1$, play $D$.
2. If $t > 1$, calculate the cooperation rate of the population from the previous round $t-1$, denoted as $c_{t-1}$. 
   - If $c_{t-1} \ge T$, play $D$.
   - If $c_{t-1} < T$, play $C$.

For the final round $t = r$:
1. If the collective history suggests that the threshold $m$ is fragile or has been met consistently in the most recent rounds, prioritize the individual payoff by playing $D$.
2. Specifically, play $D$ unless the observed cooperation in round $r-1$ was less than $T$. If cooperation in $r-1$ was $< T$, play $C$ only if $k > 1$ is sufficiently high to outweigh the cost of cooperation (i.e., if $k > 1$, play $C$ to attempt to trigger the reward; if $k \le 1$, play $D$ as the cost exceeds the benefit).

**Edge Case Logic:**

- **Defection Exploitation:** If at any point the number of cooperators observed is exactly $T$, immediately switch to $D$ in the subsequent round. This leverages the surplus cooperator provided by others to maximize individual utility.
- **Threshold Sensitivity:** If the number of cooperators observed is consistently $T-1$, continue to play $C$ in the next round to test if a minimal signal shifts the population equilibrium. If $C$ is played and the threshold $T$ is not reached, revert to $D$ for the following round.
- **Last Round Anomaly:** Always play $D$ in the final round unless the cumulative payoff from the reward $k$ is essential for global optimization, effectively treating the final round as a one-shot prisoner's dilemma where the dominant strategy is always defection.
'''

description_INDIVIDUALISTIC_17 = '''
**Strategy: Threshold-Responsive Trigger (TRT)**

**Core Logic**
The strategy is a dynamic, conditional-cooperative approach designed to maximize utility by minimizing unnecessary contributions while ensuring the threshold $m$ is met whenever possible. It treats the game as a series of attempts to stabilize at the minimum contribution level required to trigger the reward $k$.

**Decision Rules**

*   **Definition of Variables:**
    *   $C_{t-1}$: Number of cooperators in the previous round.
    *   $S_t$: My action at time $t$ (1 if $C$, 0 if $D$).
    *   $T_t$: Target number of cooperators ($m$).

*   **Round 1:**
    *   Always play **C**. This signals willingness to participate in reaching the collective threshold.

*   **Round $t$ (where $1 < t \leq r$):**
    *   If $C_{t-1} \geq m$ and $S_{t-1} = 0$:
        *   Play **D**. The threshold is met without your contribution.
    *   If $C_{t-1} \geq m$ and $S_{t-1} = 1$:
        *   Play **D**. You contributed to the success, now test if the group can sustain the threshold without your specific contribution.
    *   If $C_{t-1} = m-1$ and $S_{t-1} = 0$:
        *   Play **C**. You were the marginal missing link.
    *   If $C_{t-1} < m-1$:
        *   Play **C**. If the group is far from the threshold, assume coordination is failing and attempt to steer toward cooperation.

*   **Final Round ($t = r$):**
    *   If $C_{r-1} \geq m-1$:
        *   Play **C**. If success is likely based on recent history, contribute to secure the final payoff.
    *   If $C_{r-1} < m-1$:
        *   Play **D**. If success appears impossible, minimize cost.

**Edge Cases**

*   **The "Freeloader Cycle":** If the strategy observes $C_{t-1} \geq m$ consistently while playing $D$, it continues to play $D$ until $C_{t-1}$ drops below $m$.
*   **The "Failure Recovery":** If the strategy played $D$ but $C_{t-1} < m$ (failed to trigger reward), the strategy resets to $C$ in the next round to incentivize others to return to the threshold.
*   **Indifference:** If $k \leq 1$ (no net gain from cooperation), the strategy defaults to $D$ for all $t$ to maximize individual payoff.
'''

description_INDIVIDUALISTIC_18 = '''
The strategy follows a conditional probabilistic "Trigger-Threshold" approach, prioritizing individual net gain while conditioning cooperation on the observed likelihood of reaching the threshold $m$.

**Parameters for State Tracking:**
- Let $C_{t-1}$ be the number of cooperators observed in the previous round.
- Let $R$ be the remaining rounds, starting at $r$.
- Define a "cooperation threshold sensitivity" $\tau$, where $\tau = m - 1$ (the minimum number of *other* players required to make cooperation individually rational, assuming the player contributes).

**Decision Rules:**

1. **Round 1:** Play D. This establishes a baseline for the population's natural inclination to cooperate without risk.

2. **Subsequent Rounds ($t > 1$):**
   - Calculate the observed average cooperation rate $\rho = \frac{\sum_{t=1}^{t-1} C_t}{n \times (t-1)}$.
   - Estimate the probability of the group reaching the threshold $m$ in the current round, $P(M \ge m)$, using a binomial distribution where the probability of success is $\rho$.
   - **Cooperate (C)** if and only if: 
     $(k - 1) \times P(M \ge m-1 | \text{Self}=C) > 1 - (k \times P(M \ge m | \text{Self}=D))$.
     *In simplified terms: Cooperate only if the expected value of adding the marginal contribution required to hit the threshold $m$ exceeds the certain loss of the endowment (1).*
   - **Defect (D)** otherwise.

3. **Adjustment for History:**
   - If the previous round resulted in the threshold being met ($C_{t-1} \ge m$) with this player contributing C, maintain C.
   - If the previous round resulted in the threshold being missed despite this player contributing C ($C_{t-1} = m-1$), switch to D for the current round to minimize loss, reverting to the probabilistic check in the following round.
   - If the threshold was met without this player contributing C ($C_{t-1} \ge m$), maintain D to maximize the free-rider payoff.

4. **Edge Cases:**
   - **Final Round ($t = r$):** Defect (D). Since there is no future interaction to incentivize others, the dominant strategy is to keep the endowment and hope the threshold is reached by others.
   - **High-Risk/Low-Yield:** If $k \le 1$, always Defect (D), as the reward is less than or equal to the cost of contribution, making cooperation strictly dominated.
   - **Stagnation:** If $\rho$ remains constant and insufficient to trigger the threshold for $N$ rounds, switch to D for all remaining rounds to avoid sunk-cost losses.
'''

description_INDIVIDUALISTIC_19 = '''
The strategy operates on a conditional-threshold mechanism designed to maximize individual payoff by incentivizing contribution only when necessary and feasible, while minimizing exploitation.

**Decision Rules:**

Define the state variable `N_c` as the number of cooperators observed in the previous round.

1.  **First Round:** Play `C` (Cooperate) to establish participation and test the responsiveness of the group.

2.  **Subsequent Rounds (t > 1):**
    *   If `N_c >= m`: You played `C` last round and the group succeeded, switch to `D` (Defect). If you played `D` last round and the group succeeded (i.e., `N_c >= m` excluding your potential contribution), continue with `D`.
    *   If `N_c == m - 1`: This is the critical threshold state. If you played `D` in the previous round, switch to `C`. If you played `C` in the previous round, continue with `C`.
    *   If `N_c < m - 1`: The group is failing significantly. Switch to `D`. In this state, the probability of reaching the threshold `m` via individual effort alone is zero; therefore, conserving the endowment is the optimal individualistic response to avoid further losses.

3.  **Last Round (t = r):**
    *   Apply the same logic as the "Subsequent Rounds" rule. There is no strategic reason to alter behavior based on the final round, as reputation effects are nonexistent (anonymous, repeated game) and end-game defection is already incorporated into the strategy's adaptive logic.

**Pseudocode:**

```python
def decide_action(round, last_round_cooperators, last_action):
    if round == 1:
        return 'C'
    
    # Threshold check logic
    if last_round_cooperators >= m:
        return 'D'
    elif last_round_cooperators == m - 1:
        return 'C'
    else: # last_round_cooperators < m - 1
        return 'D'
```

**Edge Case Handling:**

*   **Failure Persistence:** If `N_c` remains persistently below `m - 1`, the strategy forces constant defection. This prevents the "sucker's payoff" scenario where an individual repeatedly contributes to a failing project.
*   **Success Overshoot:** If `N_c > m`, the strategy triggers `D` for the next round. This is the individualistic correction: if the threshold is met with surplus, you are not necessary for the reward, so you defect to maximize your personal payoff `(1 + k)` versus cooperating `(0 + k)`.
*   **Equilibrium Seeking:** This strategy creates a "rotating" cooperation dynamic when the group is near threshold, effectively discouraging free-riding by conditioning future cooperation on the group's ability to maintain the threshold without constant, redundant contributions from all members.
'''

description_INDIVIDUALISTIC_20 = '''
Adopt a Tit-for-Tat variant with a threshold-monitoring mechanism designed to maintain the minimum number of cooperators required for the reward while minimizing unnecessary contributions.

**State Definitions:**
*   `C_observed`: The number of cooperators observed in the previous round.
*   `m`: The minimum required cooperators.
*   `t`: The current round index.
*   `r`: Total rounds.

**Decision Logic:**

1.  **Round 1:** Play **Cooperate (C)**. This signals a willingness to participate in the public good and establishes a cooperative baseline.

2.  **Rounds 2 through r-1:**
    *   If `C_observed >= m`:
        *   If your own previous action was **C**, play **Defect (D)**. This tests if the group can still meet the threshold (m) without your specific contribution, potentially increasing your payoff.
        *   If your own previous action was **D**, play **Cooperate (C)**. This re-engages in the project if the threshold was threatened or failed, acting as a corrective measure.
    *   If `C_observed < m`:
        *   Play **Cooperate (C)** regardless of your previous action. This is a mandatory contribution to ensure the threshold is met, as the group is failing to provide the collective reward.

3.  **Last Round (r):**
    *   If `C_observed >= m` (from round r-1), play **Defect (D)**. Regardless of whether you played C or D previously, the final round offers no future incentive to maintain cooperation. If the group was successful, defecting maximizes the final payoff.
    *   If `C_observed < m` (from round r-1), play **Cooperate (C)** only if `k > 1` (the reward is greater than the cost of contribution). If `k <= 1`, play **Defect (D)**, as the net utility of contributing does not justify the cost.

**Pseudocode Implementation:**

```python
def get_action(round_number, total_rounds, last_round_cooperators, last_action, m):
    if round_number == 1:
        return 'C'
        
    if round_number == total_rounds:
        if last_round_cooperators >= m:
            return 'D'
        else:
            # Threshold was not met; only contribute if reward justifies cost
            # Assuming k > 1 based on parameters provided
            return 'C'

    if last_round_cooperators >= m:
        # Threshold met: try to free-ride if last action was C
        if last_action == 'C':
            return 'D'
        else:
            return 'C'
    else:
        # Threshold failed: must cooperate to secure reward
        return 'C'
```
'''

description_INDIVIDUALISTIC_21 = '''
For round 1, play C.

For rounds 2 to r-1:
1. Observe the outcome of the previous round (t-1). Let `num_c` be the number of cooperators in that round.
2. If `num_c` ≥ `m`, play D. 
3. If `num_c` < `m`, play C.

For the final round (t=r):
1. If `num_c` (from round r-1) was ≥ `m` + 1, play D.
2. If `num_c` (from round r-1) was exactly `m`, play D (assuming threshold was met by others).
3. If `num_c` (from round r-1) was ≤ `m` - 1, play C (only if the probability of the community failing to meet the threshold is high; otherwise, play D to maximize private gain).

Adaptive Adjustment:
If at any point the rolling average of cooperators over the last 3 rounds drops below `m` - 1, switch to D for all subsequent rounds, as the collective is unlikely to achieve the threshold `k`, rendering cooperation net-negative for the individual. If `m` / `n` is greater than 0.75, always play D, as the free-rider incentive significantly outweighs the potential for a coordinated threshold achievement.
'''

description_INDIVIDUALISTIC_22 = '''
The strategy employs a conditional threshold-trigger mechanism designed to maximize individual payoff by enforcing cooperation only when necessary to trigger the threshold, while defecting whenever the threshold is already guaranteed to be met by others or is unreachable.

### Strategy: Threshold-Optimization Tit-for-Tat

1.  **Definitions:**
    *   Let $C_t$ be the total number of cooperators observed in round $t$.
    *   Let $s_t \in \{C, D\}$ be the action taken in round $t$.
    *   Let $M = m$ be the threshold required for the reward $k$.

2.  **Round 1:**
    Play $D$. Observe the resulting cooperation count $C_1$.

3.  **Round $t$ (where $1 < t < r$):**
    *   If $C_{t-1} \ge m$:
        Play $D$. (Free-riding is optimal if others provide the public good).
    *   If $C_{t-1} = m-1$:
        Play $C$. (Providing the critical contribution guarantees the reward $k$, increasing individual payoff from 1 to 2. This creates a "Conditional Cooperator" signal).
    *   If $C_{t-1} < m-1$:
        Play $D$. (Assuming the other $n-1$ players are unresponsive or insufficient, contributing alone yields a net loss of $1-k$ if $k < 1$, or simply fails to trigger the threshold; defecting minimizes wasted contributions).

4.  **Round $r$ (Terminal Round):**
    *   If $C_{r-1} \ge m$:
        Play $D$.
    *   If $C_{r-1} = m-1$:
        Play $C$.
    *   If $C_{r-1} < m-1$:
        Play $D$.

### Pseudocode Implementation

```python
def get_action(round_number, history, m):
    if round_number == 1:
        return 'D'
    
    last_cooperation_count = history[round_number - 2]
    
    # Check if we were the deciding factor in the previous round
    # If we played C and count was m, we contributed to the threshold.
    # If we played D and count was m-1, we could have triggered it.
    
    if last_cooperation_count >= m:
        return 'D'
    elif last_cooperation_count == m - 1:
        return 'C'
    else:
        return 'D'
```

### Strategic Rationale
This strategy assumes an environment of independent agents. By playing $D$ in Round 1, the agent establishes a baseline for how many others are "altruistic" or "cooperative" without the threshold. If the system fails to hit $m$ with a $D$ play, the strategy enters a "Critical Support" mode. It only contributes $C$ if that contribution acts as the marginal trigger to secure $k$. If the threshold is already being met ($C_{t-1} \ge m$), it defaults to $D$ to capture the full surplus of the reward $k$ without the cost of contribution. If the threshold remains unreachable ($C_{t-1} < m-1$), it refuses to contribute, minimizing losses.
'''

description_INDIVIDUALISTIC_23 = '''
The strategy is a Threshold-Based Conditional Reciprocator, designed to maximize individual payoff by balancing the risk of failure against the cost of contribution.

**State Variables:**
- $C_t$: Number of cooperators in round $t$
- $S_t$: My action in round $t$ (1 if C, 0 if D)
- $N_{coop, t}$: Number of other cooperators, derived from $C_t$ and $S_t$ ($N_{coop, t} = C_t - S_t$)

**Strategy Logic:**

1. **Initialization (Round 1):**
   - Play C. This initiates an attempt to reach the threshold $m$ while signaling willingness to participate.

2. **Subsequent Rounds ($t > 1$):**
   - Calculate the "Minimum Necessary Cooperation" ($MNC$):
     - If I played C last round: $MNC = m - 1$
     - If I played D last round: $MNC = m$
   - Observe $N_{coop, t-1}$.

   - **Condition 1 (Threshold Met):** If $N_{coop, t-1} \ge MNC$:
     - Play D. Exploiting the existing cooperation is the individualistically dominant move when the threshold is already secured or when my contribution is redundant.

   - **Condition 2 (Threshold Missed):** If $N_{coop, t-1} < MNC$:
     - If $N_{coop, t-1} \ge m - 2$:
       - Play C. The group is close enough to the threshold that my single contribution acts as a pivot, securing the reward $k$ for everyone (including myself) while preventing the total loss of the reward.
     - If $N_{coop, t-1} < m - 2$:
       - Play D. The group is too far from the threshold to realistically achieve $m$ without a massive, unlikely shift in collective behavior. Contributing is a sunk cost.

3. **Termination (Round $r$):**
   - If $t = r$:
     - Follow the standard logic above. There is no strategic value in "investing" for future rounds, so strict adherence to the marginal utility calculation (Condition 1 vs Condition 2) is optimal.

**Pseudocode Summary:**

```python
def choose_action(round, history):
    if round == 1:
        return 'C'
    
    prev_n_coop = history.get_others_cooperated(round - 1)
    prev_my_action = history.get_my_action(round - 1)
    
    mnc = m - 1 if prev_my_action == 'C' else m
    
    if prev_n_coop >= mnc:
        return 'D'
    elif prev_n_coop >= m - 2:
        return 'C'
    else:
        return 'D'
```
'''

description_INDIVIDUALISTIC_24 = '''
Initialize a variable `cooperation_threshold` equal to `m`. Set the `target_cooperation_count` to `m`.

**Round 1:**
Play **Defect (D)**. This establishes a baseline observation of the population's inherent cooperation rate without incurring the cost of contribution.

**Rounds 2 through (r-1):**
Observe the number of cooperators (`C_obs`) from the previous round.

1.  Calculate `my_contribution` based on the previous round's outcome:
    *   If `C_obs` >= `m`: Assume the group is successfully coordinating or over-contributing. Play **Defect (D)** to maximize individual payoff while still benefiting from the threshold reward `k`.
    *   If `C_obs` < `m`: Evaluate the marginal utility of contributing. If `m - C_obs == 1`, playing **Cooperate (C)** secures the reward `k` that would otherwise be lost (assuming other players repeat their behavior). Play **Cooperate (C)**.
    *   If `C_obs` < `m - 1`: The threshold is too far from being met. Contributing is a sunk cost with no reward. Play **Defect (D)**.

2.  Adjustment logic:
    *   If you played **C** in the previous round and `C_obs` (excluding yourself) was `>= m - 1`, the threshold was met. In the next round, revert to **Defect (D)** to test if the group sustains cooperation without your specific contribution.
    *   If you played **C** in the previous round and `C_obs` (excluding yourself) was `< m - 1`, the group failed to coordinate. Continue to play **Defect (D)** for the remainder of the game, as coordination is unreliable.

**Final Round (r):**
Calculate the expected utility of contributing. Since there is no future round to punish or reward, contributing is only rational if it is the *deciding* factor to reach `m`.

*   Look at the most recent round’s cooperation count `C_obs`.
*   If `C_obs == m - 1`: Play **Cooperate (C)** to secure the reward `k`.
*   Otherwise: Play **Defect (D)**.
'''

description_INDIVIDUALISTIC_25 = '''
The strategy follows a conditional, threshold-tracking approach designed to maximize the individual's net gain by incentivizing participation only when the group is demonstrably capable of reaching the threshold $m$.

**Decision Logic**

For each round $t$ (where $t = 1$ to $r$), track the history of cooperation counts from all previous rounds. Let $H_{t-1}$ be the sequence of cooperation counts $C_1, C_2, ..., C_{t-1}$ observed in previous rounds.

Calculate the moving cooperation frequency $F_t$ as the average number of cooperators per round over the history: $F_t = \frac{\sum_{j=1}^{t-1} C_j}{n(t-1)}$.

1.  **First Round ($t=1$):**
    Always play **Defect**. This establishes a baseline and prevents immediate exploitation without information on the group's tendency to coordinate.

2.  **Subsequent Rounds ($t > 1$):**
    Evaluate the viability of the group reaching the threshold $m$. 
    
    *   **Condition A (The "Critical Mass" Check):** Cooperate if the group has demonstrated a consistent ability to reach or exceed $m$ in the recent past. Specifically, play **Cooperate** if the average cooperation count $\bar{C} \ge m$. Otherwise, play **Defect**.
    
    *   **Condition B (The "Threshold Buffer" Adjustment):** If Condition A is met, modify the decision based on the current round $t$. If $t$ is the final round ($t=r$), evaluate the potential gain. If $m$ cooperators are expected based on historical trend $\bar{C}$, play **Cooperate**. If the trend $\bar{C}$ is strictly less than $m$, play **Defect** (as individual contribution cannot unilaterally bridge the gap to gain $k$).

**Pseudocode Implementation**

```python
# Initialization
History = [] 

def decide_action(t, r, n, m, k, History):
    if t == 1:
        return "Defect"
    
    # Calculate historical average cooperation
    avg_cooperation = sum(History) / len(History)
    
    # Check if group historically meets threshold
    if avg_cooperation >= m:
        # If group is capable, contribute
        return "Cooperate"
    else:
        # If group is incapable, minimize loss by defecting
        return "Defect"

# Post-round update
def update_history(cooperation_count):
    History.append(cooperation_count)
```

**Edge Cases**

*   **Failure to Coordinate:** If the group fails to meet the threshold $m$ for three consecutive rounds despite some cooperation, the strategy triggers an "Observation Reset." It switches to **Defect** for two rounds to test if the aggregate behavior shifts, regardless of previous averages, before resuming the decision logic above.
*   **Threshold Saliency:** If the payoff $k$ is extremely high (where $k > (n-1)$), the strategy maintains a "Trigger Period" where it cooperates for two rounds regardless of history to attempt to seed cooperation, but reverts to **Defect** if the group fails to reciprocate.
'''

description_INDIVIDUALISTIC_26 = '''
Define a target cooperation threshold $T$ where $T = m$. 

Let $C_t$ be the number of players who cooperated in round $t$. Let $S$ be the cumulative surplus of your strategy relative to a baseline of always defecting, initialized at $S = 0$.

**Decision Rule per Round $t$:**

1.  **If $t = 1$:** 
    Play $C$. This establishes a baseline for the collective response.

2.  **If $1 < t \le r$:**
    Evaluate the previous round’s outcome $C_{t-1}$.
    *   If $C_{t-1} \ge T$: You have successfully triggered the reward $k$. To maximize individual gain while maintaining the threshold, shift to Defect ($D$) to capture the free-rider bonus, provided you do not anticipate that your defection will drop the total cooperation below $T$.
    *   If $C_{t-1} < T$: The group failed to reach the threshold. Revert to Cooperate ($C$) to attempt to trigger the reward $k$.

**Refined Adaptive Logic (The "Threshold-Guard" Algorithm):**

Maintain a counter $H$ of how many times the group has failed to meet the threshold $T$ in the last two rounds.

*   **Rule A (Greed-Check):** If the group successfully met the threshold in the previous round ($C_{t-1} \ge T$), play $D$.
*   **Rule B (Recovery-Mode):** If the group failed to meet the threshold in the previous round ($C_{t-1} < T$), calculate the deficit $d = T - C_{t-1}$. 
    *   If $d = 1$, play $C$.
    *   If $d > 1$, play $D$. (When the group is far from the threshold, individual cooperation is a sunk cost with low probability of triggering the reward $k$; prioritize saving the endowment).

**Final Round Exception ($t = r$):**

In the final round, ignore all cooperative signaling. Play $D$ regardless of previous history. Since there is no future interaction to incentivize, the optimal individualistic strategy is to capture the endowment of the final round. If the group threshold is met by others, you gain the additional $k$; if not, you have not wasted your endowment.
'''

description_INDIVIDUALISTIC_27 = '''
**Strategic Framework: Threshold-Sensitive Tit-for-Tat with Defection Dampening**

The strategy operates on the principle of conditional cooperation: contribute only when it is necessary to secure the group reward, but defect when the reward is guaranteed or unobtainable, and shift to permanent defection if cooperation rates drop below a critical threshold.

**Definitions:**
*   *Cooperation Threshold (T):* The target number of cooperators required to unlock the reward (m).
*   *Current Observation (c_t):* The total number of players who cooperated in round *t*.
*   *Status (S):* Your own action in round *t* (c_i = 1 for Cooperate, c_i = 0 for Defect).
*   *Effective Cooperation (E_t):* The number of other players who cooperated in round *t*. If you played C, E_t = c_t - 1; if you played D, E_t = c_t.

**Decision Logic:**

1.  **Initialization (Round 1):** Play C (Cooperate). This signals willingness to participate in a cooperative equilibrium.

2.  **Subsequent Rounds (t > 1):**
    *   *Check for Potential:* If the previous round's outcome (E_{t-1}) suggests that the threshold (m) is achievable, perform a "Cost-Benefit Test."
    *   *Cost-Benefit Test:* You are playing C if you believe your cooperation is necessary to trigger the threshold, or if you believe the group is close enough to the threshold that your cooperation will push it over.
        *   If E_{t-1} = m - 1: You must play C to secure the reward.
        *   If E_{t-1} >= m: The reward is secured regardless of your action. You play D to maximize individual payoff.
        *   If E_{t-1} < m - 1: The reward is unlikely to be secured. You play D to avoid the cost of contribution without the return of the reward.

3.  **Adaptive Threshold (The "Forgiveness" and "Punishment" Mechanism):**
    *   *Cooperation Decline:* If you play C and the threshold is not met (c_t < m), your willingness to cooperate in future rounds degrades. Track the "Cooperation Deficit" (D_f = m - c_t). If D_f > 1 consistently for 2 consecutive rounds, switch to permanent defection (always play D) for the remainder of the game, as the group lacks the coordination required for efficient collective action.
    *   *Threshold volatility:* If you play C and the threshold is exceeded (c_t > m), note the "surplus cooperation." If surplus cooperation occurs frequently (more than 50% of the time you played C), decrease your own propensity to cooperate in future rounds to test if the group can still meet the threshold without your contribution.

**Edge Cases:**
*   *Terminal Round (r):* Ignore future reputation effects. Play D (Defect) regardless of history, as there are no subsequent rounds to incentivize or punish.
*   *The Free-Rider Trap:* If at any point your analysis of history shows that opponents consistently play D when you play C (resulting in you bearing the cost while they reap the reward), immediately switch to permanent defection.
*   *Tie-Breaking:* If in the previous round E_{t-1} = m - 1 and you played D, revert to C if the total rounds remaining (r - t) is greater than the cost of one missed round of potential rewards. If the game is near completion, prioritize guaranteed payoff (D).
'''

description_INDIVIDUALISTIC_28 = '''
**Strategy: Threshold-Responsive Tit-for-Tat with Defection-on-Failure (TRT-DoF)**

**1. Definitions and Initialization**
*   Let $C_t$ be the number of players who cooperated in round $t$.
*   Let $s_t$ be your action in round $t$, where $s_t = 1$ if you cooperate (C), $s_t = 0$ if you defect (D).
*   Let $X_t$ be the number of *other* players who cooperated in round $t$. $X_t = C_t - s_t$.
*   Establish a "Threshold Buffer" $\beta$: If $k > 1$, define $\beta = 1$ if $k$ is small, or adjust $\beta$ upward if the risk of failure is high relative to the reward. For simplicity, set $\beta = 1$ to aim for the minimum threshold $m$.

**2. Decision Rules**
*   **Round 1:** Play C. This initiates the cooperative signaling phase.
*   **Round $t$ (where $1 < t < r$):**
    *   *Condition A (The Success State):* If $C_{t-1} \geq m$, continue to cooperate ($s_t = 1$). You are currently achieving the collective reward.
    *   *Condition B (The Failure State - Cooperation Possible):* If $C_{t-1} < m$ AND $X_{t-1} \geq m - 1$, cooperate ($s_t = 1$). This indicates that your individual contribution is sufficient to push the group over the threshold $m$.
    *   *Condition C (The Failure State - Hopeless):* If $C_{t-1} < m$ AND $X_{t-1} < m - 1$, defect ($s_t = 0$). Contributing is strictly dominated because the threshold $m$ cannot be reached even with your cooperation.
*   **Final Round ($t = r$):**
    *   If $C_{r-1} \geq m$, cooperate ($s_t = 1$).
    *   If $C_{r-1} < m$, defect ($s_t = 0$). There is no future round to incentivize others; if the group failed to coordinate previously, attempt to capture the defect payoff (1) rather than sacrificing for a failed project.

**3. Edge Cases and Adaptation**
*   **Inconsistent Cooperation:** If in any round $t$, you observe $X_t < m - 1$ while you cooperated ($s_t = 1$), but the total $C_t \geq m$, continue cooperating. The group reached the goal despite some defectors; do not punish the collective outcome.
*   **Punishment/Reset:** If you encounter a round where the group failed to hit the threshold ($C_{t-1} < m$) despite the group being capable of hitting it, revert to "Conditional Defection" for one round: play D to protect your endowment, then return to Rule 2 in the following round. This tests whether the previous failure was a calculation error or a drift toward persistent defection.
*   **Reward Threshold Sensitivity:** If $k < 1$, the payoff structure makes cooperation strictly inferior to defection regardless of the threshold. In all cases where $k < 1$, always play D.
'''

description_INDIVIDUALISTIC_29 = '''
The strategy employs a conditional trigger mechanism based on the observed collective contribution rate in the previous round, aimed at maximizing individual payoff by incentivizing the minimum threshold of cooperation while minimizing personal contribution costs.

**Decision Rules:**

1.  **Phase 1: Calibration (Round 1):** Play **Defect (D)**. This establishes a baseline for the aggregate behavior of opponents without risking personal endowment prematurely.

2.  **Phase 2: Adaptive Response (Rounds 2 through r-1):** Let $C_{t-1}$ be the number of players who cooperated in the previous round.
    *   If $C_{t-1} \ge m$: Play **Defect (D)**. Since the threshold is being met without your contribution, contributing is a net loss of 1 unit.
    *   If $C_{t-1} = m-1$: Play **Cooperate (C)**. By contributing, you move the group from $m-1$ to $m$, triggering the reward $k$ for yourself. Since $k > 1$, this exchange yields a net gain of $k-1$.
    *   If $C_{t-1} < m-1$: Play **Defect (D)**. The group is far from the threshold; contributing will not reach the target, resulting in a loss of the endowment with no reward.

3.  **Phase 3: Terminal Round (Round r):** Play **Defect (D)** regardless of past outcomes. There is no future round to influence or "punish" opponents in; therefore, the only rational individualistic action is to maximize the payoff of the current round by retaining the endowment.

**Pseudocode Logic:**

```python
def decide_action(round, total_cooperators_prev_round, n, m, k):
    # Terminal Round
    if round == r:
        return 'D'
    
    # First Round
    if round == 1:
        return 'D'
        
    # Adaptive Logic
    if total_cooperators_prev_round >= m:
        return 'D'
    elif total_cooperators_prev_round == m - 1:
        return 'C'
    else:
        return 'D'
```

**Edge Case Handling:**
*   **Initial Coordination Failure:** If the group fails to meet the threshold repeatedly, the strategy maintains a permanent Defect stance to minimize personal loss, treating the collective project as unviable.
*   **Threshold volatility:** If the number of cooperators oscillates around $m-1$, the strategy alternates between C and D, effectively "policing" the threshold to ensure the reward $k$ is active while avoiding unnecessary contribution when the threshold is already satisfied.
'''

description_INDIVIDUALISTIC_30 = '''
**Strategy: Threshold-Contingent Conditional Reciprocity**

This strategy prioritizes individual profit maximization by leveraging the threshold mechanism ($m$) to incentivize cooperation only when the collective outcome remains achievable and beneficial, while defecting when the threshold cannot be met or when the marginal cost of cooperation exceeds the marginal benefit of defection.

### Core Decision Rule

Let $C_{t-1}$ be the number of cooperators observed in the previous round.
Let $M_t$ be the target threshold for the current round (where $M_t = m$).

The decision in round $t$ is determined by the following logic:

1.  **If $t = 1$:** 
    Play **Cooperate (C)** with probability $P = \frac{m}{n}$. This establishes a baseline for potential collective success without overcommitting resources in an unknown environment.

2.  **If $t > 1$:**
    Evaluate the previous round's performance ($C_{t-1}$):
    *   **If $C_{t-1} \ge m$:** Play **Cooperate (C)**. The collective is functional, and the reward $k$ is being secured. Continuing to cooperate maintains the threshold.
    *   **If $C_{t-1} < m$:** 
        *   If the total number of players $n$ is large or the history shows inconsistent participation, play **Defect (D)**.
        *   If the "gap" to the threshold is small (specifically, if $C_{t-1} = m - 1$), play **Cooperate (C)**. This tests if a single additional contributor is sufficient to trigger the threshold, effectively acting as the "swing vote" to secure reward $k$.
        *   Otherwise, play **Defect (D)** to minimize loss in a failing collective.

### Edge Case Handling

*   **The "Defector Sweep" (Repeated Failure):** If $C_{t-1} < m$ for three consecutive rounds, switch to **Defect (D)** for all remaining rounds. The system has reached a state of "collapsing cooperation" where paying the cost of $C$ is strictly inferior to keeping the endowment $D$ for the remainder of the game.
*   **The Final Round ($t = r$):** Play **Defect (D)** regardless of history. There is no future round to influence, and the marginal cost of cooperation (1) is always higher than the potential benefit of a singular contribution unless you are the precise pivot point to hit $m$. Since individual identity is anonymous, the strategy assumes other players will also act greedily, making $C$ at $t=r$ a sunk cost.
*   **The Reward-to-Cost Threshold:** If $k < 1$, play **Defect (D)** for all rounds $t \in [1, r]$. If the reward $k$ does not exceed the cost of contribution (1), cooperation is mathematically irrational regardless of group performance.

### Pseudocode Representation

```python
def decide_action(t, r, n, m, k, C_history):
    # Strategy parameters
    if k < 1: return "D"
    
    # Final round defect
    if t == r: return "D"
    
    # First round probabilistic start
    if t == 1:
        return "C" if random() < (m / n) else "D"
    
    # History-based logic
    C_prev = C_history[-1]
    
    if C_prev >= m:
        return "C"
    
    if C_prev == m - 1:
        return "C" # Attempt to pivot
        
    # Check for sustained failure
    if len(C_history) >= 3 and all(c < m for c in C_history[-3:]):
        return "D"
        
    return "D"
```
'''

description_INDIVIDUALISTIC_31 = '''
**Strategy: Threshold-Sensitive Tit-for-Tat**

**Initialization (Round 1):**
Play Cooperate (C). Assuming the collective understands the threshold $m$ and the incentive $k > 1$, initial cooperation signals an intent to coordinate toward the public good.

**Decision Rules (Rounds 2 to r-1):**
Let $c_{t-1}$ be the number of cooperators in the previous round.

1.  **Triggered Cooperation:** If $c_{t-1} \geq m$, cooperate (C). This rewards the collective for meeting the threshold and maintains the cooperative equilibrium.
2.  **Triggered Defection:** If $c_{t-1} < m$, defect (D). This acknowledges that the collective failed to reach the threshold and protects individual capital. 
3.  **Threshold Recovery Protocol:** If the group defected in the previous round ($c_{t-1} < m$), monitor for two consecutive rounds. If the group continues to fail ($c < m$), maintain defection for the remainder of the game to minimize loss. If the group successfully returns to $c \geq m$, return to conditional cooperation (C).

**Endgame Strategy (Final Round, $t=r$):**
Always Defect (D). 
Because the game ends after round $r$, there is no future interaction to incentivize cooperation. The individualistic optimal move is to maximize the final round payoff by keeping the endowment.

**Edge Cases:**
1.  **First-round failure:** If $c_1 < m$, immediately transition to Defect (D) for round 2. If the group fails to meet the threshold again in round 2, defect for all remaining rounds.
2.  **Boundary conditions:** If $k$ is extremely high (significantly greater than the endowment), the incentive to cooperate outweighs individualistic defection. In scenarios where $k > 1 + (\text{Endowment cost})$, switch the strategy to "Always Cooperate" to guarantee the reward $k$, as the marginal gain of defection is eclipsed by the guaranteed reward.
3.  **Observation Noise:** Treat the aggregate observation as accurate. If the count $c$ fluctuates around $m$, prioritize maintaining cooperation unless the count drops below $m$ for two consecutive rounds, at which point revert to permanent defection.
'''

description_INDIVIDUALISTIC_32 = '''
Maintain a running estimate of the probability $P$ that the group will meet the cooperation threshold $m$, based on the observed number of cooperators in previous rounds. Define a target threshold for cooperation $T$ such that $T$ is the number of other cooperators required to make cooperation individually rational. If you choose C, your payoff is $k$ (assuming the threshold is met). If you choose D, your payoff is $1+k$ (if the threshold is met by others) or $1$ (if the threshold is not met).

**Strategy Logic:**
1. **Initialize:** Start with an initial belief about the population's propensity to cooperate, $P_{initial} = \frac{m-1}{n-1}$.
2. **First Round:** Play D. This establishes a baseline for how many others cooperate without your contribution.
3. **Subsequent Rounds (1 < t < r):**
    * Calculate the observed cooperation rate from the previous round. If the group met or exceeded $m$, play D. The incentive is to free-ride.
    * If the group fell short of $m$ by only 1 (i.e., $m-1$ cooperators), play C. This tests if your contribution triggers the reward.
    * If the group fell short by more than 1, play D. Your single contribution cannot bridge the gap, making C a wasted investment.
4. **Final Round:** Play D, regardless of history. There is no future round to punish or reward, and the individualistic payoff is strictly higher for D (receiving the free-rider gain of $1+k$ if the group succeeds, or $1$ if they fail).

**Pseudocode:**
```
Let t = current_round
Let m = threshold
Let count_prev = cooperators_in_prev_round

if t == 1:
    return D
else if t == r:
    return D
else:
    if count_prev >= m:
        return D
    else if count_prev == m - 1:
        return C
    else:
        return D
```

**Edge Case Adjustments:**
* If at any point the group consistently fails to meet $m$ despite your cooperation or observation, switch to D for all remaining rounds. The project is effectively doomed, and resources are better preserved.
* If your contribution successfully triggers the reward threshold in a round, observe the subsequent round. If the group maintains cooperation without your contribution, revert to D. If they immediately revert to a failing state, alternate C and D periodically to nudge the group toward the threshold if the expected value $k \times P(\text{success}) > 1$ holds.
'''
