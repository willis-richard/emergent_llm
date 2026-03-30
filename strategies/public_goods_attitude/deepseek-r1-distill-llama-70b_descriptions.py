
description_PROSOCIAL_7 = '''
The prosocial strategy for the N-Player Public Goods Game is designed to adapt to the behavior of other players, encouraging cooperation when beneficial to the group. Here's the step-by-step explanation:

### Prosocial Strategy: **"Conditional Cooperation Based on Public Good Threshold"**

1. **First Round Decision:**
   - **Action:** Cooperate (C)
   - **Rationale:** Initiates cooperation to maximize group benefit, encouraging others to follow suit.

2. **Subsequent Rounds:**
   - **Observation:** After each round, observe the number of players who cooperated (C_{t-1}).
   - **Threshold Calculation:** Determine if C_{t-1} > (n/k)
   - **Action:**
     - **If Yes:** Cooperate in the current round.
     - **If No:** Defect in the current round.

This strategy promotes sustained cooperation by only continuing to contribute if the public good's benefit exceeds individual gains, adapting dynamically based on others' past actions.

### Pseudocode:

```python
def prosocial_strategy(game_parameters, history):
    n = game_parameters['n']
    k = game_parameters['k']
    round = history['current_round']
    
    if round == 1:
        return "C"
    else:
        previous_cooperations = history['previous_actions'].count("C")
        threshold = n / k
        if previous_cooperations > threshold:
            return "C"
        else:
            return "D"
```

### Summary:
- **First Round:** Always Cooperate.
- **Subsequent Rounds:** Cooperate if the number of cooperators in the previous round exceeds n/k; otherwise, Defect.
- This ensures cooperation is maintained when beneficial and adaptively responds to group behavior, aligning with a prosocial mindset.
'''

description_PROSOCIAL_8 = '''
### K/n Threshold Strategy

**1. Decision Rules:**
- **First Round:** Always Cooperate (C). This sets a prosocial tone and encourages cooperation from others.
- **Subsequent Rounds:** Cooperate (C) in round `t` if the fraction of players who Cooperated in round `t-1` is **at least k/n**. Otherwise, Defect (D).

**2. Edge Cases:**
- **First Round:** Always Cooperate.
- **Last Round (r):** Same rules as any other round.
- **If All Players Defect:** If all players Defected in the previous round, Cooperate to restart cooperation.

**3. Prosological Alignment:**
The strategy aims to maximize collective payoffs while maintaining fairness, fostering cooperation when beneficial, and addressing free-riding with defection when necessary.

*Pseudocode:*
```
function k_over_n_threshold_strategy() {
    for each round t from 1 to r:
        if t == 1:
            action = COOPERATE
        else:
            previous_coop_rate = number_of_cooperations(t-1) / n
            if previous_coop_rate >= k/n:
                action = COOPERATE
            else:
                action = DEFECT
        take action
}
```

This strategy is adaptive, simple, and promotes long-term prosocial outcomes through reciprocal behavior.
'''

description_PROSOCIAL_9 = '''
To address the N-player public goods game, we've designed a prosocial, adaptive strategy that encourages cooperation while being robust to various opponent behaviors. The strategy is outlined below:

### Strategy: Prosocial Adaptive Cooperation (PAC)

**Decision Rules:**
1. **First Round:** Always Cooperate (C) to establish a prosocial tone.
2. **Subsequent Rounds (2 to r-1):** 
   - Calculate the threshold `m = ceil(n/k)`, where `ceil` is the ceiling function.
   - Observe the number of cooperators `C` in the previous round.
   - If `C ≥ m`, Cooperate; else, Defect.
3. **Last Round (r):**
   - Compute the average number of cooperators across all previous rounds, `avg_C`.
   - If `avg_C ≥ m`, Cooperate; else, Defect.

**Handling Edge Cases:**
- The threshold `m` is calculated once at the start and remains constant.
- Forgiveness is implicit; if cooperation resurges above `m`, the strategy resumes cooperation.

**Prosocial Alignment:**
This strategy prioritizes collective welfare by rewarding sufficient cooperation and only defecting when cooperation is too low, thus promoting a balance between individual and group benefits.

### Pseudocode

```python
def prosocial_adaptive_cooperation(n, k, r, history):
    if not history:
        return 'C'
    m = math.ceil(n / k)
    if len(history) == 1:
        previous_coops = sum(history[0])
        if previous_coops >= m:
            return 'C'
        else:
            return 'D'
    avg_coops = sum([sum(round) for round in history]) / len(history)
    if len(history) == r - 1:
        if avg_coops >= m:
            return 'C'
        else:
            return 'D'
    previous_coops = sum(history[-1])
    if previous_coops >= m:
        return 'C'
    else:
        return 'D'
```

**Explanation:**
- **First Round:** Cooperate to initiate cooperation.
- **Middle Rounds:** Cooperate if enough players cooperated previously; defect otherwise to incentivize higher cooperation.
- **Last Round:** Cooperate if overall cooperation was sufficient, encouraging prosocial behavior even at the end.

This strategy is designed to be simple, observable, and adaptive, promoting sustained cooperation and maximizing collective payoffs.
'''

description_COLLECTIVE_1 = '''
To address the N-Player Public Goods Game, the strategy outlined is designed to be adaptive, robust, and collective. It encourages cooperation initially, adapts based on group performance, and ensures self-interest in the final round. Here's a structured breakdown of the strategy:

### Strategy Overview

1. **First Round: Cooperate**
   - All players start by cooperating to establish a foundation of trust and maximize the initial public good.

2. **Intermediate Rounds: Adaptive Cooperation Based on Public Good**
   - In each subsequent round, evaluate the public good from the previous round. If the public good (k/n * Σc_j) is at least 1, continue cooperating. If it's below this threshold, alternate between cooperating and defecting in subsequent rounds to incentivize others to contribute more. This phase uses reciprocity to sustain cooperation by responding to the group's behavior.

3. **Last Round: Defect**
   - In the final round, all players defect to maximize their individual payoffs since there are no future consequences.

### Rationale

- **Initial Cooperation:** Starting with cooperation sets a positive tone and establishes a baseline for the public good.
- **Adaptive Response:** By conditioning cooperation on meeting a threshold, the strategy encourages continued contribution. Alternating actions signal dissatisfaction and aim to prompt others to increase their contributions.
- **Final Round Defection:** Recognizing the last round's lack of future repercussions, defecting ensures individual gain without affecting future interactions.

This strategy is collective as it aligns all players' actions based on observable outcomes, making it robust against various behaviors while promoting cooperation through reciprocity.
'''

description_PROSOCIAL_10 = '''
**Prosocial Strategy for N-Player Public Goods Game**

**1. Decision Rules:**
   - **First Round**: Always Cooperate (C) to initiate a prosocial tone.
   - **Subsequent Rounds**: Calculate the average cooperation rate from all previous rounds. If the average is above 50%, continue Cooperating (C). If it's 50% or below, switch to Defecting (D).
   - **Last Round**: Regardless of the cooperation history, Cooperate (C) to uphold trust and prosocial behavior.

**2. Handling Edge Cases:**
   - **First Round**: Cooperate to set a cooperative foundation.
   - **Last Round**: Maintain cooperation to encourage trust, even in the final round.

**3. Prosocial Alignment:**
   The strategy promotes cooperation by responding positively when others cooperate and protecting against exploitation when they don't. It balances reciprocity with safeguarding individual payoffs, fostering a prosocial environment while adapting to group behavior.
'''

description_COLLECTIVE_2 = '''
**Collective Strategy for the N-Player Public Goods Game**

**Objective:** To encourage cooperative behavior while safeguarding against free-riding, ensuring a balance between collective benefit and individual protection.

**Strategy Overview:**

1. **First Round Cooperation:**
   - **Action:** Cooperate (C). This sets an initial cooperative tone, encouraging others to reciprocate.

2. **Monitor Cooperation Rate:** 
   - After the first round, track the average cooperation rate of all players from the previous round.

3. **Threshold-Based Decision Making:**
   - **Threshold:** Calculate the threshold as k/n, where k is the multiplication factor and n is the number of players.
   - **Decision Rule:** In each subsequent round, if the previous round's cooperation rate meets or exceeds the threshold, Cooperate (C). Otherwise, Defect (D).

4. **Final Round Handling:**
   - In the last round, continue using the same decision rule based on the cooperation rate from the penultimate round. This maintains consistency and encourages sustained cooperation.

**Pseudocode:**

```pseudocode
function Strategy(n, k, r, history):
    if history is empty:
        cooperate
        add to history: cooperation = True
    else:
        previous_round = history[-1]
        cooperation_rate = number_of_cooperations(previous_round) / n
        threshold = k / n
        if cooperation_rate >= threshold:
            cooperate
        else:
            defect
        add current choice to history
    return cooperate or defect
```

**Rationale:**

- **Initial Cooperation:** Starting with cooperation fosters a positive environment, potentially inviting reciprocal behavior.
- **Adaptive Decision Making:** By adjusting based on the previous round's cooperation rate, the strategy is responsive to collective behavior, rewarding cooperation when it is sufficiently prevalent.
- **Threshold Mechanism:** Using k/n as a threshold ensures that cooperation is encouraged when it provides a net benefit, as indicated by the multiplication factor.
- **Robustness:** The strategy is resilient against free-riders by defecting when cooperation levels are insufficient, preventing exploitation without assuming others' strategies.

This strategy promotes mutual cooperation when beneficial, adapting to group dynamics while safeguarding against exploitation, making it robust and effective in various scenarios.
'''

description_COLLECTIVE_3 = '''
To design a collective strategy for the N-Player Public Goods Game, we focus on a threshold-based approach using the parameter k. The strategy aims to encourage cooperation by rewarding good behavior and punishing collectively when cooperation dips below a certain level.

### Strategy Description:

1. **First Round**: All players Cooperate (C). This sets the initial condition for maximum group payoff.

2. **Subsequent Rounds**: For each round after the first, the decision to Cooperate or Defect depends on the number of Cooperators in the previous round:
   - If the number of players who Cooperated in the previous round is at least k, the player Cooperates again.
   - If the number of Cooperators was fewer than k, the player Defects.

### Pseudocode:
```
def strategy(history, parameters):
    n = parameters['n']  # Number of players
    k = parameters['k']  # Multiplication factor
    r = parameters['r']  # Number of rounds
    t = len(history) + 1  # Current round
    
    if t == 1:
        return 'C'  # Cooperate in the first round
    else:
        c_prev = history[-1]  # Number of Cooperators in the previous round
        if c_prev >= k:
            return 'C'
        else:
            return 'D'
```

### Explanation:
- **First Round Cooperation**: Starting with cooperation maximizes the initial payoff and sets a positive tone.
- **Adaptive Cooperation**: By checking if at least k players cooperated previously, the strategy encourages sustained cooperation. If the threshold is met, continued cooperation is rewarded. If not, a collective punishment round ensues, discouraging free-riding.

This strategy balances reward and punishment, adapting to the group's behavior to maximize collective payoffs while discouraging defection.
'''

description_COLLECTIVE_4 = '''
To address the N-Player Public Goods Game, we've designed a strategy called **RECIPROCATE**, which encourages cooperation based on past behavior, adapting to maintain collective benefits while discouraging exploitation.

### Strategy: RECIPROCATE

1. **First Round Cooperation**: All players Cooperate in the first round to establish a baseline of trust and maximize the initial public good.

2. **Adaptive Cooperation Threshold**: In subsequent rounds, each player calculates the number of Cooperators from the previous round. If this number meets or exceeds a threshold determined by the game parameters (n and k), the player Cooperates again. Specifically, the threshold is set to the ceiling of n divided by k (ceil(n/k)).

3. **Punishment Mechanism**: If the number of Cooperators in the previous round falls below the threshold, the player Defects to discourage free-riding and incentivize others to Cooperate in future rounds.

### Pseudocode Implementation

```python
def reciprocate_strategy(n, k, r, history):
    threshold = math.ceil(n / k)
    if not history:
        # First round: Cooperate
        return 'C'
    else:
        # Calculate number of Cooperators in the last round
        last_actions = history[-1]
        m_prev = sum(1 for action in last_actions if action == 'C')
        if m_prev >= threshold:
            return 'C'
        else:
            return 'D'
```

### Explanation

- **Initial Cooperation**: Starting with Cooperation sets a positive tone and maximizes initial payoffs.
- **Dynamic Threshold**: The threshold adjusts based on the game's parameters, ensuring that cooperation is only sustained when enough players contribute, making it individually rational.
- **Responsive Punishment**: By Defecting when cooperation is too low, players enforce the norm of contributing to the public good, maintaining a balance between individual and collective incentives.

This strategy is robust against diverse behaviors and adaptively encourages sustained cooperation through reciprocity, balancing individual incentives with collective welfare.
'''

description_COLLECTIVE_5 = '''
To address the N-player Public Goods Game, we can employ an adaptive strategy that encourages cooperation while protecting against exploitation. Here's the structured approach:

### Strategy: Adaptive Collective Cooperation

1. **First Round Action:**
   - **Cooperate (C):** Start by cooperating to establish a baseline of trust and encourage initial collective contribution.

2. **Subsequent Rounds (Rounds 2 to R-1):**
   - **Majority Rule:** Observe the number of players who cooperated in the previous round.
     - **If a majority cooperated:** Continue cooperating in the current round to sustain the collective benefit.
     - **If a majority defected:** Switch to defecting (D) to avoid being exploited by others' non-cooperation.

3. **Last Round Action (Round R):**
   - **Defect (D):** In the final round, defect to maximize personal payoff, as there are no future consequences to consider.

### Rationale:

- **Initial Cooperation:** Starting with cooperation sets a positive tone and can lead to higher collective payoffs if others reciprocate.
- **Adaptive Behavior:** By mirroring the majority's previous action, the strategy encourages continued cooperation when beneficial and switches to self-protection when necessary.
- **Final Round Adjustment:** Recognizing the endgame scenario, where future repercussions are absent, defecting in the last round maximizes individual gain.

This strategy is robust, adapting to the dynamics of group behavior without relying on communication, making it suitable for a competitive tournament setting.
'''

description_COLLECTIVE_6 = '''
To design a collective strategy for the N-Player Public Goods Game, we propose an adaptive approach that encourages cooperation based on the group's past behavior. The strategy is robust, easy to implement, and aligns with the collective interest of maximizing payoffs through sustained cooperation.

**Strategy:**

1. **First Round:** Always cooperate. This initializes the game with a cooperative mindset, encouraging others to reciprocate.

2. **Subsequent Rounds:** After the first round, the decision to cooperate or defect is based on the average number of cooperators in all previous rounds. Specifically, if the average number of cooperators meets or exceeds the threshold \( \frac{n}{k} \), the player continues to cooperate. If the average falls below this threshold, the player defects.

**Pseudocode:**

```
Initialize:
    Cooperate in the first round.

For each subsequent round t:
    Calculate the average number of cooperators from rounds 1 to t-1.
    If average_cooperators >= n/k:
        Cooperate
    Else:
        Defect
```

**Rationale:**

- **Cooperation in the First Round:** Starting with cooperation sets a positive tone and can encourage others to reciprocate, potentially leading to higher initial payoffs.

- **AdaptiveDecision Making:** By considering the average cooperation rate, the strategy dynamically adjusts based on collective behavior. This ensures that cooperation is only sustained if it is mutually beneficial, as indicated by the threshold \( \frac{n}{k} \).

- **Robustness:** The strategy is resilient against a proportion of defectors. If enough players cooperate to meet the threshold, cooperation continues. If not, the strategy shifts to defecting to avoid exploitation.

This approach balances individual and collective interests, fostering cooperation while protecting against unsustainable exploitation, making it suitable for a tournament setting against diverse strategies.
'''

description_COLLECTIVE_7 = '''
**Collective Strategy for N-Player Public Goods Game**

---

### **1. Decision Rules:**

- **First Round:** Cooperate. This sets a cooperative tone at the beginning.
  
- **Subsequent Rounds (2 to r-1):** Cooperate if the number of cooperators in the previous round meets or exceeds a threshold \( T = \lceil \frac{n}{k} \rceil \). Otherwise, Defect.

- **Last Round:** Always Defect. Since there are no future rounds to influence, the temptation to defect is stronger.

---

### **2. Handling Edge Cases:**

- **First Round:** Cooperate to establish cooperation.
- **Last Round:** Defect to maximize immediate payoff with no future consequences.

---

### **3. Collective Mindset:**

This strategy promotes mutual cooperation by only cooperating when a sufficient number of others do so. It punishes by defecting if cooperation levels drop below the threshold, while also addressing the endgame by defecting in the final round. This approach balances cooperation with protection against exploitation, ensuring adaptability and robustness.

---

### **Pseudocode Implementation:**

```python
def strategy(n, k, r, history):
    if not history:
        # First round
        return 'C'
    if r == 1:
        # Last round
        return 'D'
    if len(history) < r-1:
        # Rounds 2 to r-1
        T = math.ceil(n / k)
        prev_coop = sum(1 for action in history[-1] if action == 'C')
        if prev_coop >= T:
            return 'C'
        else:
            return 'D'
    else:
        # Last round
        return 'D'
```

---

**Rationale:**

- **Threshold Cooperation:** The threshold \( T \) is calculated as the ceiling of \( n/k \), ensuring it's an integer. Players cooperate if enough others did so previously, maintaining a balance between individual and collective gains.

- **Punishment Mechanism:** If cooperation falls below the threshold, the strategy shifts to defection, discouraging free-riding and encouraging others to return to cooperation.

- **Endgame Handling:** Recognizing that the last round lacks future consequences, the strategy defects to secure the higher immediate payoff.

This strategy effectively encourages sustained cooperation while adapting to group behavior, ensuring robustness in a competitive environment.
'''

description_COLLECTIVE_8 = '''
To address the N-Player Public Goods Game, we need a collective strategy that promotes cooperation while being robust against various opponent behaviors. The strategy, which we'll call "Adaptive Reciprocity," is designed to balance individual incentives with collective benefits through reciprocity and resets.

### Strategy: Adaptive Reciprocity

**1. Decision Rules:**
- **First Round:** Always Cooperate (C) to establish a cooperative tone.
- **Subsequent Rounds:** For each round `t` (from 2 to r):
  - Observe the number of Cooperators `C_{t-1}` in the previous round.
  - **Cooperate** if `C_{t-1}` is greater than `n/k` (threshold of contributors).
  - **Cooperate** if all players Defected in the previous round (`C_{t-1}=0`), acting as a reset.
  - **Defect** (D) otherwise.

**2. Handling Edge Cases:**
- **First Round:** Cooperate to initiate cooperation.
- **Last Round:** Treat it like any other round, based on the previous round's cooperation level.
- **Reset Mechanism:** If all players Defected, Cooperate again to restart cooperation.

**3. Collective Alignment:**
This strategy aligns with a collective mindset by encouraging cooperation when it's mutually beneficial and resetting cooperation when necessary, ensuring sustained contribution to the public good.

### Pseudocode

```python
def adaptive_reciprocity(n, k, r, history):
    if not history:  # First round
        return "C"
    else:
        c_prev = history[-1].count("C")
        threshold = n / k
        if c_prev > threshold:
            return "C"
        elif c_prev == 0:
            return "C"
        else:
            return "D"
```

### Explanation
- **Initial Cooperation:** Starting with cooperation encourages others to follow suit.
- **Reciprocity:** Conditioning cooperation on previous round's participation ensures mutual benefit.
- **Reset:** Restarting cooperation after all Defections prevents perpetual defection cycles.

This strategy is adaptive, aligns with collective goals, and is robust against various opponent strategies, making it effective in a tournament setting.
'''

description_COLLECTIVE_9 = '''
**Strategy: Adaptive Collective Cooperation (ACC)**

**Overview:**
The ACC strategy is designed to encourage cooperation while being robust against exploitation. It adapts to the group's behavior, reciprocating cooperation and punishing defection. This strategy is collective, meaning it aligns with the group's interests, and handles edge cases such as the first and last rounds effectively.

**1. Decision Rules:**

- **First Round:** Cooperate (C). This initiates a positive dynamic, encouraging others to cooperate.
- **Subsequent Rounds (2 to r-1):** Cooperate in round t if the average cooperation rate in round t-1 was at least 50%. Otherwise, Defect (D).
- **Last Round (r):** Cooperate if the average cooperation rate up to round r-1 is at least 50%. This incentivizes sustained cooperation.

**2. Edge Cases Handling:**
- **First Round:** Always Cooperate to set a cooperative tone.
- **Last Round:** Decision based on prior rounds' cooperation to maintain reciprocity.

**3. Collective Alignment:**
- **Reciprocity:** Cooperate when others do, Defect when others don't, promoting mutual benefit.
- **Robustness:** Responsive to various behaviors, maintaining cooperation without exploitation.

**Pseudocode:**

```
Initialize:
    total_cooperation = 0
    round_cooperation = 0

For each round t from 1 to r:
    if t == 1:
        action = C
        round_cooperation += 1
    else if t == r:
        avg_cooperation = total_cooperation / (r - 1)
        if avg_cooperation >= 0.5:
            action = C
        else:
            action = D
    else:
        previous_avg = previous_round_avg_c
        if previous_avg >= 0.5:
            action = C
            round_cooperation += 1
        else:
            action = D
    if action == C:
        total_cooperation += 1
    if t > 1:
        round_cooperation = 1 if action == C else 0
```

**Conclusion:**
The ACC strategy is a balanced approach that encourages cooperation while being responsive to group behavior. It's simple, adaptive, and effective in promoting collective benefit without assuming others' strategies.
'''

description_COLLECTIVE_10 = '''
To address the N-player public goods game, we'll use an adaptive strategy that balances cooperation with self-interest, especially in the final round. Here's the structured strategy:

### Strategy: "Conditional Cooperation with Endgame Defection"

1. **First Round (t=1):**
   - **Action:** All players Cooperate (C).

2. **Intermediate Rounds (2 ≤ t < r):**
   - **Action:** Each player observes the number of Cooperate actions in the previous round (t-1).
     - If the number of Cooperate actions meets or exceeds a threshold (ceil(n/2)), the player Cooperates again.
     - If the number of Cooperate actions is below the threshold, the player Defects (D).

3. **Final Round (t=r):**
   - **Action:** All players Defect (D), as there are no future consequences.

### Rationale:
- **Initial Cooperation:** Starting with cooperation maximizes the public good, encouraging initial trust.
- **Threshold Cooperation:** Using a threshold ensures that cooperation continues only if a sufficient number of players are contributing, preventing exploitation.
- **Endgame Defection:** In the last round, defecting is individually optimal as there's no future punishment possible.

This strategy is robust, as it adapts based on group behavior and ensures rational play, especially in the endgame.
'''

description_COLLECTIVE_11 = '''
To address the N-Player Public Goods Game, we need a strategy that encourages cooperation while being resilient to varying levels of participation. The goal is to maximize the group's payoff sustainably. Here's the structured approach:

### Strategy: Collective Cooperation with Parallel Forgiveness

**1. Initial Cooperation:**
   - **First Round:** All players Cooperate (C). This sets a cooperative tone and establishes a baseline for future interactions.

**2. Adaptive Cooperation Based on Previous Round's Cooperation Level:**
   - **Subsequent Rounds:** After the first round, each player calculates the number of Cooperators (m) from the previous round.
     - **Cooperation Threshold (m ATL):** A threshold based on game parameters (n and k) that determines if cooperation is beneficial.
     - **Cooperation Trend:** Players track if the number of Cooperators is increasing, stable, or decreasing.
     - **Strategy:**
        - **If m ≥ m_ATL:** Cooperate in the current round.
        - **If m < m_ATL:** Defect in the current round.

**3. Dynamic Adjustment of Threshold:**
   - **Trend-Based Adjustment:** Adjust the threshold dynamically:
     - **Decrease m_ATL:** If the trend shows increasing cooperation over the past few rounds, lower the threshold to encourage continued cooperation.
     - **Increase m_ATL:** If the trend shows decreasing cooperation, raise the threshold, making it harder to Cooperate next round, prompting a more cautious approach.

**4. Final Round Strategy:**
   - **Last Round (r):** All players Defect (D). Without future rounds to influence, the incentive to Contribute diminishes, prioritizing immediate payoff.

### Pseudocode Implementation

```python
def collective_strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    # Calculate number of cooperators in previous round
    m_prev = sum(1 for action in history[-1] if action == 'C')
    m_threshold = 0.5 * n  # Initial moving average
    # Adjust threshold based on trend
    trend = 'positive'  # Determine trend from history
    # Example trend calculation (simplified)
    window = min(len(history), 3)
    recent_m = [sum(1 for action in h if action == 'C') for h in history[-window:]]
    avg_m = sum(recent_m) / window
    if avg_m > m_prev * 0.8:  # arbitrary threshold
        trend = 'positive'
    elif avg_m < m_prev * 0.2:
        trend = 'negative'
    else:
        trend = 'stable'
    
    if trend == 'positive':
        m_threshold *= 0.9  # Decrease threshold, encourage cooperation
    elif trend == 'negative':
        m_threshold *= 1.1  # Increase threshold, more cautious
    
    if r == len(history) + 1:  # Last round
        return 'D'
    # Determine current action
    if m_prev >= m_threshold:
        return 'C'
    else:
        return 'D'
```

### Explanation

- **Initial Cooperation:** Everyone starts by Cooperating to establish a cooperative baseline.
- **Adaptive Decision-Making:** Each player monitors past cooperation levels, using a dynamic threshold to decide actions, promoting flexibility.
- **Trend Adjustment:** By adjusting the threshold based on trends, the strategy remains responsive, forgiving if cooperation trends upward and cautious if it trends downward.
- **Final Round Defection:** In the last round, players defect to maximize personal gain, as future influence is absent.

This strategy balances cooperation and self-interest, fostering sustained group benefit while adapting to the dynamics of player interactions.
'''

description_COLLECTIVE_12 = '''
To address the N-Player Public Goods Game, I propose the following collective strategy, designed to maximize group payoff while remaining adaptive and robust against various opponent behaviors.

### Strategy Overview

**Name:** Adaptive Collective Cooperation (ACC)

**Objective:** Sustain cooperation as long as a sufficient number of players cooperate, otherwise defect to avoid being exploited.

**Mechanism:**
1. **First Round Cooperation:** All players start by Cooperating (C) to establish initial trust and maximize the initial public good.
2. **Threshold-Based Cooperation:** In subsequent rounds, each player Cooperates if the number of Cooperators in the previous round meets or exceeds a threshold, calculated as the ceiling of the ratio of the number of players (n) to the multiplication factor (k), i.e., ceil(n/k). If the threshold is met, Cooperate; otherwise, Defect (D).

**Edge Cases Handling:**
- **First Round:** Cooperate to initiate cooperation.
- **Last Round:** The strategy does not differentiate the last round from others, relying on previous cooperation to decide the action, thus potentially maintaining cooperation throughout.

**Algorithm Pseudocode:**

```
function strategy(n, k, history) {
    if history is empty:
        return Cooperate
    else:
        previous_round = history[-1]
        c_prev = count of Cooperate actions in previous_round
        threshold = ceil(n / k)
        if c_prev >= threshold:
            return Cooperate
        else:
            return Defect
}
```

### Explanation

- **Cooperation Initiation:** By Cooperating in the first round, players establish a foundation for potential mutual cooperation.
- **Adaptive Threshold:** The threshold, ceil(n/k), ensures that cooperation continues only when a sufficient number of players contribute, making the public good sufficiently beneficial.
- **Robustness:** The strategy adapts based on collective past behavior, ensuring that if cooperation wanes, it adjusts to prevent exploitation.

This strategy encourages sustained group benefit by conditioning cooperation on past collective actions, making it both adaptive and resilient in dynamic competitive environments.
'''

description_COLLECTIVE_13 = '''
To address the challenge of designing a collective strategy for the N-Player Public Goods Game, we need a strategy that balances individual rationality with collective benefit. The strategy should encourage cooperation while protecting against exploitation, especially in the final round. Here's the structured approach:

### Collective Strategy: Adaptive Cooperation with Last Round Defection

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Reason:** Establish a cooperative tone to encourage others to cooperate, aiming for higher collective payoffs.

2. **Middle Rounds (Rounds 2 to r-1):**
   - **Decision Rule:** Cooperate if the number of players who cooperated in the previous round meets or exceeds a threshold **t**.
     - **Threshold Calculation:** Set `t = ceiling(k / (k + 1) * n)`, which adapts to the game parameters, encouraging cooperation when sufficiently many others cooperate.
   - **Action:** 
     - If the number of cooperators in the previous round ≥ **t**, Cooperate (C).
     - Otherwise, Defect (D).

3. **Last Round (Round r):**
   - **Action:** Defect (D).
   - **Reason:** Defecting in the final round avoids exploitation since there are no future rounds to punish defection, maximizing individual payoff.

This strategy is designed to sustain cooperation throughout most of the game while safeguarding against exploitation in the last round. By adapting based on the previous round's cooperation level, it encourages collective benefit while being responsive to the behavior of others.

### Pseudocode Representation

```python
def strategy(game_parameters, history):
    n = game_parameters['n']
    k = game_parameters['k']
    r = game_parameters['r']
    current_round = history['current_round']

    if current_round == 1:
        return "C"  # Cooperate in the first round

    # Calculate threshold t
    t = math.ceil((k / (k + 1)) * n)

    # Get previous round's actions
    previous_actions = history['actions'][current_round - 2]
    previous_cooperators = sum(1 for action in previous_actions if action == 'C')

    if current_round < r:
        if previous_cooperators >= t:
            return "C"  # Cooperate if enough cooperated last round
        else:
            return "D"  # Defect if not enough cooperated
    else:
        return "D"  # Defect in the last round
```

This strategy is adaptive, responding to the level of cooperation observed, and robust, handling edge cases such as the first and last rounds effectively. By setting a dynamic threshold, it aligns with a collective mindset, aiming to maximize total payoff while protecting individual interests.
'''

description_COLLECTIVE_14 = '''
To address the N-player public goods game, we designed a strategy that encourages cooperation while adapting to other players' actions. The strategy leverages the game's parameters to determine when cooperation is beneficial and adjusts behavior accordingly, ensuring robustness against defectors and optimal play in the final round.

**Strategy: Conditional Cooperation Based on Previous Contributions**

1. **First Round:** Cooperate to initiate a cooperative environment.
2. **Rounds 2 to r-1:** Cooperate if the number of cooperators in the previous round exceeded n/k; otherwise, defect to retaliate against insufficient cooperation.
3. **Last Round (Round r):** Defect, as there are no future consequences, making it individually optimal to defect.

**Pseudocode:**

```
def strategy(n, k, r, current_round, total_C_prev):
    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        if total_C_prev > n / k:
            return "C"
        else:
            return "D"
```

**Explanation:**

- **First Round:** Starts with cooperation to set a positive tone.
- **Middle Rounds:** Cooperates if the previous round's cooperation was sufficient, ensuring the public good's benefit surpasses personal loss.
- **Last Round:** Recognizes the lack of future consequences, prompting defection to maximize individual payoff.

This strategy promotes sustained cooperation while adapting to others' actions, ensuring it's both robust and effective in various scenarios.
'''

description_COLLECTIVE_15 = '''
To address the N-Player Public Goods Game, a strategic approach is developed that balances cooperation with the temptation to defect, especially in the endgame. The strategy is designed to encourage collective cooperation while being adaptive to others' behavior.

---

**Strategy Name:** Conditional Cooperation with Endgame Defection

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate a cooperative tone.
   
2. **Middle Rounds (2 to r-1):**
   - Cooperate in the current round if the number of cooperators in the previous round meets or exceeds the threshold of n/k.
   - Defect (D) if the previous round's cooperation was below this threshold.

3. **Last Round (r):** Always Defect (D), as there are no future interactions to influence, making individual payoff maximization optimal.

**Edge Cases:**
- The first round is handled by always cooperating.
- The last round is handled by always defecting regardless of prior cooperation levels.

**Pseudocode Implementation:**

```python
def strategy(n, r, k, history):
    current_round = len(history) + 1
    if current_round == 1:
        return "C"
    else:
        if current_round < r:
            previous_cooperators = sum(history[-1][i] == 'C' for i in range(n))
            threshold = n / k
            if previous_cooperators >= threshold:
                return "C"
            else:
                return "D"
        else:
            return "D"
```

**Collective Mindset:** This strategy aligns with a collective approach by promoting cooperation when others do the same, fostering mutual benefit. However, it adaptively shifts to defection when cooperation levels drop or in the final round, ensuring individual rationality.
'''

description_COLLECTIVE_17 = '''
The designed collective strategy for the N-player public goods game is as follows:

1. **First Round**: All players Cooperate (C). This establishes an initial cooperative tone, encouraging others to reciprocate.

2. **Subsequent Rounds**: For each round after the first, players observe the number of Cooperators (c_prev) from the previous round.

   - **Cooperation Threshold**: If c_prev is greater than or equal to k, each player Cooperates in the current round.
   - **Defection Trigger**: If c_prev is less than k, each player defects (D).

3. **Final Round Handling**: The strategy does not differentiate the last round, applying the same rule as other rounds. This means if c_prev meets or exceeds k, players Cooperate; otherwise, they Defect.

This strategy promotes sustained cooperation by incentivizing contribution when a sufficient number of players (at least k) have done so previously. It adapts to the behavior of others, balancing individual and collective benefits while being simple and robust against varied opponent behaviors.
'''

description_COLLECTIVE_18 = '''
To address the N-Player Public Goods Game, the strategy "Sustainable Cooperation" is designed to encourage continuous cooperation by conditioning future actions on past outcomes, leveraging the collective benefits of the public good.

**Sustainable Cooperation Strategy**

1. **Decision Rule**:
   - **First Round**: Cooperate.
   - **Subsequent Rounds**: Cooperate if the number of cooperators in the previous round is at least k; otherwise, defect.

2. **Edge Cases**:
   - **First Round**: All players cooperate to maximize the initial public good.
   - **Transition Rounds**: After the first round, each player's decision is based on the number of cooperators in the previous round.
   - **Threshold Check**: The threshold is set to k, ensuring that enough players contribute to the public good to make continued cooperation beneficial for the group.

3. **Collective Alignment**:
   - This strategy encourages sustained cooperation by using a threshold based on the multiplication factor k, ensuring that the public good remains sufficiently high to motivate continued participation.

**Pseudocode Implementation**

```python
def sustainable_cooperation(history, n, k):
    if not history:  # First round
        return "C"
    else:
        cooperators = sum(history[-1])
        if cooperators >= k:
            return "C"
        else:
            return "D"
```

**Explanation**:
- **Initial Cooperation**: Everyone starts by cooperating to establish a high public good.
- **Adaptive Decision-Making**: Each subsequent decision is based on the previous round's cooperation level, ensuring that as long as enough players contribute, cooperation continues.
- **Robustness**: The strategy adjusts based on the game's parameters and past behavior, maintaining cooperation when beneficial and defecting when contributions are insufficient.

This strategy promotes cooperative behavior, leveraging the benefits of the public good while adapting to group dynamics to sustain mutual benefit.
'''

description_COLLECTIVE_19 = '''
To address the challenge of designing a collective strategy for the N-Player Public Goods Game, we developed an adaptive and robust approach that encourages cooperation while mitigating exploitation. The strategy leverages the individual rationality condition, ensuring that cooperation is maintained as long as it remains beneficial, and adapts by defecting when cooperation is no longer advantageous. This approach is simple, deterministic, and aligns with game-theoretic principles.

### Strategy: Myopic Best Response with Cooperation Threshold

1. **Decision Rule**:
   - Cooperate in the first round.
   - For each subsequent round, observe the number of Cooperators (C_prev) in the previous round.
   - Calculate the benefit from cooperation as (k/n) * C_prev.
   - If this benefit exceeds 1, Cooperate; otherwise, Defect.

2. **Edge Cases**:
   - **First Round**: Always Cooperate as there is no prior history.
   - **Subsequent Rounds**: Apply the decision rule based on the previous round's cooperation level.
   - **Last Round**: Continue applying the same decision rule, as the strategy doesn't change based on the round number.

3. **Collective Alignment**:
   - The strategy is designed for all players to follow, encouraging mutual cooperation when beneficial and adapting collectively when cooperation is insufficient.

### Pseudocode Implementation:

```python
def strategy(round, prev_coop_count, n, k):
    if round == 1:
        return "C"  # Cooperate in the first round
    
    # Calculate if the benefit from cooperation exceeds 1
    benefit = (k / n) * prev_coop_count
    if benefit > 1:
        return "C"  # Cooperate if beneficial
    else:
        return "D"  # Defect otherwise

# Total rounds played
total_rounds = r

# Initialize previous coop count
prev_coop = 0

for t in range(1, total_rounds + 1):
    if t == 1:
        action = "C"
    else:
        action = strategy(t, prev_coop, n, k)
    
    # After all players have acted, update prev_coop
    # (Actual implementation would require observing the number of C's)
    # For demonstration, assume we can count the number of C's
    prev_coop = number_of_cooperators_in_prev_round()
    
    print(f"Round {t} action: {action}")
```

### Explanation:

- **Cooperation Threshold**: The strategy uses a threshold based on the individual rationality condition. Players Cooperate if the expected benefit from the public good exceeds their individual contribution.
- **Adaptation**: The strategy adapts based on the previous round's outcome, promoting flexibility and preventing exploitation.
- **Edge Handling**: The first round is handled by always Cooperating, setting a positive tone. The strategy doesn't differentiate the last round, ensuring consistency throughout the game.

This strategy balances cooperation and self-interest, making it robust against various opponent behaviors in a tournament setting.
'''

description_COLLECTIVE_20 = '''
**Strategy: Adaptive Cooperation Based on Historical Contributions**

1. **Initial Round (Round 1):**
   - **Action:** Cooperate (C)
   - **Rationale:** Start with cooperation to encourage others and establish a cooperative tone.

2. **Subsequent Rounds (Rounds 2 to r-1):**
   - **Action:** Calculate the average cooperation rate from all previous rounds.
     - **Cooperation Rate:** The proportion of players who cooperated in each past round, averaged across rounds.
   - **Threshold Calculation:** Determine a dynamic threshold based on the parameter \( k/n \). Set a lower threshold for higher \( k/n \) values to encourage cooperation even with some defectors.
   - **Decision Rule:**
     - If the cooperation rate is above the threshold, Cooperate.
     - If below, Defect.

3. **Final Round (Round r):**
   - **Action:** Assess the overall cooperation rate throughout the game.
   - **Decision Rule:**
     - Cooperate if the average cooperation rate across all rounds meets or exceeds the initial threshold.
     - Defect if the rate is below the threshold, to avoid exploitation in the last interaction.

4. **Adaptation Mechanism:**
   - Continuously monitor the cooperation rate and adjust the threshold dynamically based on \( k/n \).
   - This ensures the strategy remains responsive to the group's behavior and the game's parameters.

This strategy promotes sustained cooperation by rewarding groups that maintain a high cooperation rate, while protecting against exploitation when cooperation is low. It's robust across various scenarios, adapting to both cooperative and defective behaviors, ensuring a balance between individual payoff and collective benefit.
'''

description_COLLECTIVE_21 = '''
**Adaptive Collective Strategy (ACS) for N-Player Public Goods Game**

**Objective:**  
To design a strategy that encourages sustained cooperation while adapting to the group's behavior and robustly handling various scenarios.

**Strategy Overview:**

1. **Initial Cooperation:**  
   - **First Round Action:** Cooperate (C). All players start by contributing to the public good, establishing a baseline of cooperation.

2. **Adaptive Cooperation Based on Previous Round:**  
   - **Cooperation Rate Calculation:** After each round, calculate the cooperation rate as the number of players who cooperated divided by the total number of players (n).
   - **Threshold Check:** Determine a threshold cooperation rate. If the previous round's cooperation rate meets or exceeds this threshold, cooperate in the next round. If it falls below, defect in the next round.

3. **Last Round Defection:**  
   - **Final Round Action:** Defect (D) in the last round to maximize individual payoff since there are no future consequences.

**Formal Strategy:**

- **Let r be the current round.**
- **Let CRₜ be the cooperation rate in round t.**
- **Let τ be the cooperation threshold (e.g., τ ≥ 0.5).**

**Pseudocode:**

```
for each player i:
    if t == 1:
        action = C
    else:
        CR_previous = (number of C in t-1) / n
        if CR_previous >= τ and t < r:
            action = C
        elif t == r:
            action = D
        else:
            action = D
```

**Rationale:**

- **Initial Cooperation:** Encourages setting a cooperative tone, maximizing initial public goods benefits.
- **Adaptive Element:** Adjusts behavior based on collective action, maintaining cooperation if sufficient others cooperate.
- **Last Round Defection:** Prevents being exploited when future consequences are absent, ensuring individual payoff maximization in the final round.

**Edge Cases:**

- **All Players Defect:** If the cooperation rate drops below the threshold, the strategy defects, aligning with the Nash equilibrium but adapting based on collective behavior.
- **Mixed Strategies:** The strategy remains responsive, adapting to any mix of cooperation and defection by evaluating the cooperation rate.

This strategy is designed to be collectively rational, fostering cooperation while safeguarding against exploitation, making it robust in various interactive scenarios.
'''

description_COLLECTIVE_22 = '''
To address the challenge of designing a collective strategy for the n-player public goods game, we propose an adaptive approach that balances individual and group interests. The strategy is responsive to the group's behavior and encourages cooperation while being robust against defection.

### Strategy Overview

1. **First Round Cooperation**: 
   - **Action**: Cooperate.
   - **Rationale**: Initiates cooperation to set a positive tone and encourages others to follow suit.

2. **Subsequent Rounds Adaptation**:
   - **Rule**: Cooperate if the number of cooperators in the previous round is at least k; otherwise, defect.
   - **Rationale**: Encourages sustained cooperation as long as the group meets the threshold, adapting if cooperation falls short.

3. **Last Round Consistency**:
   - **Action**: Follow the same rule as other rounds.
   - **Rationale**: Maintains consistency and fairness, avoiding last-round exploitation.

### Pseudocode Implementation

```pseudocode
function strategy(n, k, r, history):
    if current_round == 1:
        return Cooperate
    else:
        previous_cooperators = history[round-1].count( Cooperate )
        if previous_cooperators >= k:
            return Cooperate
        else:
            return Defect
```

### Explanation

- **First Round**: Cooperate to establish a cooperative precedent.
- **Subsequent Rounds**: Use the previous round's cooperation rate to decide. This ensures adaptability and responsiveness to group dynamics.
- **Last Round Handling**: By following the same rule, it maintains the strategy's integrity without special casing the final round.

This strategy is simple yet effective, promoting cooperation while protecting against exploitation. It aligns individual actions with collective benefit, fostering a balance that is crucial in repeated public goods games.
'''

description_COLLECTIVE_23 = '''
The strategy for the N-Player Public Goods Game is designed to be adaptive and collective, encouraging cooperation while protecting against exploitation. Here's the structured approach:

### Strategy: Collective Adaptive Cooperation

#### 1. First Round Decision:
   - **Action:** Cooperate (C)
   - **Rationale:** Initiate cooperation to set a positive tone and encourage others to contribute to the public good.

#### 2. Subsequent Rounds:
   - **Observation:** After each round, observe the number of players who Cooperated (total_c) and calculate the cooperation rate of others.
   - **Threshold Adjustment:** Maintain a dynamic threshold (t) that starts at 0.5 (or another initial value based on game parameters). Adjust t based on past outcomes:
     - If Cooperating yielded a higher payoff than Defecting, keep t the same or lower it to be more lenient.
     - If Cooperating did not yield a higher payoff, increase t to require more cooperation from others before Cooperating again.
   - **Decision Rule:** 
     - If the cooperation rate of others in the previous round meets or exceeds t, Cooperate.
     - Otherwise, Defect.

#### 3. Payoff Evaluation:
   - After each round, evaluate whether Cooperating was beneficial:
     - If you Cooperated, check if (k/n)*total_c >1. If true, lower t; otherwise, increase t.
     - If you Defected, calculate the hypothetical payoff if you had Cooperated. Adjust t lower if this hypothetical payoff is greater than your actual Defect payoff.

### Pseudocode:

```python
def collective_strategy(game_params, history):
    n, r, k = game_params['n'], game_params['r'], game_params['k']
    current_round = history['current_round']
    if current_round == 1:
        return 'C'
    else:
        previous_actions = history['actions'][current_round-2]
        total_c = sum(previous_actions)
        others_cooped = total_c - (1 if history['your_last_action'] == 'C' else 0)
        others_coop_rate = others_cooped / (n - 1)
        
        threshold = 0.5  # Initial threshold, adaptive over time
        if others_coop_rate >= threshold:
            return 'C'
        else:
            return 'D'

    # After each round, adjust threshold based on payoffs
    # (This part would be implemented in the agent's post-round evaluation)
```

### Explanation:
- **Cooperation in the First Round:** Encourages initial contribution to the public good.
- **Dynamic Threshold:** Adapts based on others' cooperation levels and the effectiveness of past cooperation.
- **Payoff Evaluation:** Ensures the strategy learns from outcomes, adjusting the willingness to Cooperate or Defect as needed.

This strategy balances cooperation and self-interest, fostering collective good while protecting against exploitation.
'''

description_COLLECTIVE_24 = '''
To address the challenge of designing a collective strategy for the N-player public goods game, we developed an adaptive approach that balances cooperation and defection based on the group's previous behavior. This strategy aims to maximize collective payoffs while being robust against diverse opponent behaviors.

### Strategy: Adaptive Collective Cooperation (ACC)

1. **First Round:**
   - **Action:** Cooperate.
   - **Reasoning:** Initiates cooperation, establishing a foundation for potential mutual benefit.

2. **Middle Rounds (Rounds 2 to r-1):**
   - **Action:** 
     - **Cooperate** if the number of cooperators in the previous round (m_prev) is at least the threshold (ceil(n/k)).
     - **Defect** otherwise.
   - **Reasoning:** Encourages sustained cooperation when enough players contribute, leveraging the public good's benefits and deterring exploitation.

3. **Last Round (Round r):**
   - **Action:** Defect.
   - **Reasoning:** Without future interactions, defecting maximizes individual payoff in the final round.

### Pseudocode:

```python
def strategy(n, k, r, history):
    current_round = len(history) + 1  # Assuming history[0] is round 1

    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        m_prev = sum(1 for action in history[-1] if action == "C")
        threshold = math.ceil(n / k)
        if m_prev >= threshold:
            return "C"
        else:
            return "D"
```

### Explanation:

- **First Round Cooperation:** Sets a cooperative tone, crucial for establishing potential mutual benefits.
- **Adaptive Decision in Middle Rounds:** Adjusts based on previous cooperation levels. If enough players cooperated, continue; otherwise, defect to avoid exploitation.
- **Last Round Defection:** Maximizes individual gain without future repercussions.

This strategy is robust, promotes cooperation when beneficial, and adapts as group dynamics evolve, ensuring collective and individual payoffs are balanced effectively.
'''

description_COLLECTIVE_25 = '''
### Strategy Design: Adaptive Collective Cooperation with Punishment (ACCP)

#### Overview:
The strategy **Adaptive Collective Cooperation with Punishment (ACCP)** is designed to balance cooperation and punishment in a way that maximizes collective payoffs while being robust to free-riding and exploitation. It adapts based on the history of cooperation and uses a graduated punishment mechanism to enforce cooperation norms.

#### Key Features:
1. **Initial Cooperation**: Start with cooperation to establish a norm of reciprocity.
2. **Adaptive Cooperation**: Cooperate if enough others are cooperating; otherwise, defect temporarily.
3. **Graduated Punishment**: Punish defectors by defecting for one round, but return to cooperation if cooperation resumes.
4. **Forgiveness**: Allow cooperation to resume if others cooperate again after a round of punishment.
5. **Final Round Consideration**: Cooperate in the last round if cooperation has been sufficient; otherwise, defect.

#### Decision Rules:
1. **First Round**: Always cooperate to establish a cooperative baseline.
2. **Subsequent Rounds**:
   - Calculate the average cooperation rate from the previous round.
   - If the average cooperation rate meets or exceeds the threshold (k/n), cooperate.
   - If the average cooperation rate is below the threshold, defect for one round as punishment.
   - If punishment was applied in the previous round, check the new average cooperation rate. If it meets the threshold, revert to cooperation.

#### Pseudocode:
```
def ACCPStrategy(n, k, r, history=None):
    if history is None:
        # First round: Cooperate
        return "C"
    else:
        # Calculate average cooperation in the last round
        prev_round = history[-1]
        avg_coop = sum(prev_round) / n
        
        if avg_coop >= k/n:
            return "C"
        else:
            # Check if previous round was punished
            if len(history) >= 2:
                prev_prev_round = history[-2]
                prev_prev_avg_coop = sum(prev_prev_round) / n
                if prev_prev_avg_coop >= k/n:
                    return "C"
            # Punish by defecting
            return "D"
```

#### Edge Cases:
1. **First Round**: Always cooperate to establish a cooperative norm.
2. **Last Round**: Cooperate if the average cooperation in the previous round was sufficient; otherwise, defect.
3. **All Players Defecting**: If all players defect, the strategy will also defect to avoid being exploited.

#### Alignment with Collective Mindset:
This strategy aligns with a collective mindset by prioritizing cooperation when it is mutually beneficial. It punishes free-riding but is forgiving if cooperation resumes, aiming to sustain cooperation over time.
'''

description_COLLECTIVE_27 = '''
### Strategy Design: Adaptive Collective Cooperation with Punishment (ACCP)

The ACCP strategy is designed to balance individual incentives with collective benefits in an N-player public goods game. It uses a combination of cooperation, punishment, and adaptation to robustly handle a wide range of opponent behaviors while aligning with the collective mindset of promoting public goods.

#### 1. Decision Rules:
The strategy uses the following rules to decide whether to cooperate (C) or defect (D) in each round:

- **First Round:** Always cooperate (C). This sets a cooperative tone and encourages others to follow suit.
  
- **Subsequent Rounds:** 
  - Calculate the average cooperation rate in the previous round, defined as the fraction of players who cooperated (C). Denote this as \( \bar{c}_{t-1} \).
  - Use the following threshold-based rule to decide the action:
    - If \( \bar{c}_{t-1} \geq k/(k+1) \), cooperate (C).
    - If \( \bar{c}_{t-1} < k/(k+1) \), defect (D).
  - **Forgiveness Mechanism:** If you defected in the previous round(s) due to low cooperation, reintroduce cooperation if \( \bar{c}_{t-1} \) rises above the threshold.

- **Punishment Phase:** If the cooperation rate is consistently below the threshold for a few consecutive rounds, switch to defection (D) for a limited number of rounds. After this punishment phase, revert to cooperation (C) if the cooperation rate improves.

#### 2. Handling Edge Cases:
- **First Round:** Always cooperate (C) to establish a cooperative norm.
  
- **Last Round:** Cooperate (C) if the average cooperation rate across all previous rounds is above the threshold. Otherwise, defect (D).

- **Punishment Phase:** If the cooperation rate is consistently below the threshold, defect (D) for a maximum of \( n \) rounds before reconsidering cooperation.

#### 3. Collective Alignment:
The strategy aligns with the collective mindset by:
- Encouraging cooperation when it is mutually beneficial (when the cooperation rate is above the threshold).
- Punishing free-riders and incentivizing others to cooperate by defecting when the cooperation rate is below the threshold.
- Forgiving past defections if cooperation improves, allowing for recovery of the collective good.

### Pseudocode:
```plaintext
# Initialize strategy parameters
threshold = k / (k + 1)
punishment_length = n

# First round action
if round == 1:
    action = C
    history = [C]
else:
    # Calculate average cooperation rate in the previous round
    prev_coop_rate = count_C_in_prev_round / n
    
    # Determine action based on threshold
    if prev_coop_rate >= threshold:
        action = C
    else:
        action = D
        
    # Punishment phase: defect for a limited number of rounds if cooperation is low
    if action == D and punishment_counter < punishment_length:
        punishment_counter += 1
    else:
        punishment_counter = 0
        
    # Forgiveness: revert to cooperation if cooperation rate improves
    if prev_coop_rate >= threshold and punishment_counter > 0:
        punishment_counter = 0
        action = C
        
    history.append(action)
```

### Explanation:
The ACCP strategy is a robust and adaptive approach that balances individual and collective incentives. It starts by cooperating to encourage others to do the same, punishes free-riders when cooperation is low, and forgives past defections if cooperation improves. This strategy is designed to be collectively rational, promoting the public good while protecting against exploitation. It should perform well in a tournament setting where other strategies may vary widely in their behavior.
'''

description_COLLECTIVE_28 = '''
To design a collective strategy for the N-Player Public Goods Game, we propose the following approach:

### Strategy: Adaptive Collective Cooperation

**1. Decision Rules:**
   - **First Round:** Cooperate.
   - **Subsequent Rounds:** Cooperate if the number of cooperators in the previous round is at least `ceil(n/k)`. Otherwise, Defect.
   - **Edge Cases:** In the last round, follow the same rule based on the previous round's cooperation level.

**2. Threshold Determination:**
   The threshold is calculated as `ceil(n/k)`, ensuring that if enough players cooperated last round, cooperation is beneficial.

**3. Pseudocode:**

```python
def strategy(game_params, history):
    n = game_params['n']
    k = game_params['k']
    r = game_params['r']
    current_round = history['current_round']
    
    if current_round == 1:
        return 'C'
    
    previous_round = current_round - 1
    c_prev = history['round'][previous_round]['cooperators_count']
    threshold = math.ceil(n / k)
    
    if c_prev >= threshold:
        return 'C'
    else:
        return 'D'
```

**4. Rationale:**
   - **First Round Cooperation:** Starts with cooperation to establish trust.
   - **Adaptive Threshold:** Uses the threshold `ceil(n/k)` to determine if cooperation is beneficial.
   - **Handling Edge Cases:** Consistent application of rules ensures robustness, including the last round.

This strategy promotes collective cooperation, adapts based on previous behavior, and is robust against exploitation.
'''

description_COLLECTIVE_29 = '''
**Strategy Description: Majority-Match**

**1. Decision Rules:**

- **First Round:** Cooperate (C) to establish a norm of cooperation and encourage mutual contribution from the start.
  
- **Subsequent Rounds:** 
  - Observe the number of players who Cooperated (C) in the previous round.
  - If the majority (more than 50%) Cooperated, choose to Cooperate (C) in the current round.
  - If the majority Defected (D), or if there's an equal split, choose to Defect (D) in the current round.

**2. Edge Cases:**

- **First Round Handling:** Since there's no prior history, the strategy defaults to Cooperation to initiate a cooperative environment.
  
- **Last Round Handling:** The strategy continues to follow the Majority-Match rule, maintaining consistency and incentivizing sustained cooperation throughout the game, including the final round.

**3. Collective Mindset:**

The Majority-Match strategy is designed to align with collective behavior, encouraging cooperation when others cooperate and defecting when others defect. It fosters reciprocity and adapts dynamically to the group's behavior, aiming to maximize individual payoff while promoting public good contribution.

**Pseudocode:**

```
Function MajorityMatch(n, r, k):
    Initialize history as an empty list
    For each round t from 1 to r:
        If t == 1:
            action = C
            Add action to history
        Else:
            previous_c = count of C in history[t-1]
            if previous_c > n/2:
                action = C
            else:
                action = D
            Add action to history
    Return history
```

This strategy is robust, adaptive, and promotes a balance between individual and collective benefits, making it suitable for a wide range of opponent behaviors in the game.
'''

description_COLLECTIVE_30 = '''
**Strategy Design: Adaptive Collective Cooperation with Forgiveness**

**Objective:**  
To maximize collective and individual payoff in an N-player repeated public goods game by encouraging cooperation while being robust against defection.

**Strategy Components:**

1. **Initial Cooperation (First Round):**  
   Cooperate in the first round to establish a cooperative tone and encourage others to reciprocate.

2. **Adaptive Threshold Mechanism:**  
   - Track the cooperation rate of other players in previous rounds.
   - Maintain a dynamic threshold for cooperation, starting at 100% and adjusting adaptively.

3. ** Forgiveness and Retaliation:**  
   - If the cooperation rate falls below the threshold, defect for a set number of rounds (punishment phase).
   - After the punishment phase, restart cooperation, gradually adjusting the threshold based on observed cooperation.

4. **Last Round Consideration:**  
   In the final round, defect if the multiplication factor k exceeds the number of players n, as individual gain outweighs collective benefit.

**Implementation Steps:**

1. **Initialization:**  
   Set initial cooperation threshold high (e.g., 100%) and forgive counter low.

2. **Rounds 1 to r-1:**  
   - Cooperate if the cooperation rate meets or exceeds the threshold.
   - Adjust threshold based on previous rounds, forgiving past defections if cooperation improves.

3. **Final Round:**  
   Defect if k > n to maximize individual payoff.

**Algorithm Pseudocode:**

```
Initialize:
    threshold = 1.0 (start with perfect cooperation expectation)
    forgive_counter = 0

For each round t from 1 to r:
    If t == 1:
        Cooperate
    Else if t == r:
        If k > n:
            Defect
        Else:
            Cooperate
    Else:
        previous_cooperation_rate = average cooperation in t-1
        If previous_cooperation_rate >= threshold:
            Cooperate
            forgive_counter = 0
            Adjust threshold based on previous_cooperation_rate
        Else:
            If forgive_counter < max_forgive:
                Cooperate
                forgive_counter += 1
                Adjust threshold downwards
            Else:
                Defect
                Adjust threshold upwards

```

**Explanation:**

- **Initial Cooperation:** Sets a positive tone, encouraging others to cooperate.
- **Adaptive Threshold:** Adjusts expectations based on group behavior, maintaining flexibility.
- **Forgiveness Mechanism:** Allows resumption of cooperation after defections, preventing perpetual punishment.
- **Last Round Strategy:** Balances individual and collective payoffs, defecting when beneficial.

This strategy promotes sustained cooperation while adapting to group dynamics, ensuring robustness against varied behaviors.
'''

description_COLLECTIVE_31 = '''
To address the N-Player Public Goods Game, we design an adaptive, collective strategy that promotes cooperation while safeguarding against exploitation. The strategy balances encouragement of group contributions with self-optimization, particularly in the final round.

### Strategy Overview:

1. **Initial Cooperation**: In the first round, the player cooperates to set a cooperative tone.
2. **Adaptive Cooperation**: For rounds 2 to r-1, the player cooperates if the number of cooperators in the previous round meets or exceeds a dynamic threshold, specifically the ceiling of n/k. This threshold ensures that cooperation is beneficial for the group while providing a baseline for individual contribution.
3. **Last Round Defection**: In the final round, the player defects to maximize immediate payoff, acknowledging the lack of future consequences.

### Decision Rules and Edge Cases:

- **First Round**: Cooperate to initiate a cooperative environment.
- **Middle Rounds (2 to r-1)**: Continue cooperating if the number of previous round's cooperators is at least the ceiling of n/k. If not, defect to avoid being exploited.
- **Last Round (r)**: Defect to secure the highest possible immediate payoff, as future interactions no longer incentivize cooperation.

### Pseudocode:

```python
def public_goods_strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    elif len(history) == r:  # Last round
        return 'D'
    else:
        prev_coop = history[-1]['cooperators']
        threshold = math.ceil(n / k)
        if prev_coop >= threshold:
            return 'C'
        else:
            return 'D'
```

### Explanation:

- **Cooperation Threshold**: The strategy uses a threshold based on game parameters (n and k) to decide whether cooperation is beneficial, ensuring adaptability across varying group sizes and multiplier values.
- **Dynamic Adjustment**: By evaluating past cooperation levels, the strategy dynamically adjusts, promoting sustained cooperation while penalizing insufficient contributions.
- **Final Round Consideration**: Acknowledging the end of the game, the strategy optimizes for the last round's immediate payoff, aligning with dominant strategy analysis in the absence of future interactions.

This comprehensive approach fosters cooperation while mitigating the risk of being exploited, making it robust against various opponent behaviors in the tournament.
'''

description_COLLECTIVE_32 = '''
To address the N-Player Public Goods Game, we've designed a strategic approach that balances individual and collective interests through adaptivity. The strategy aims to sustain cooperation when beneficial while allowing for defection when the public good's returns are insufficient. Here's the structured plan:

### Strategy: Adaptive Threshold Cooperation (ATC)

**1. Decision Rules:**

- **First Round:** Always Cooperate. This initiates the game with maximum collective contribution.
  
- **Subsequent Rounds:** In each round, from the second to the penultimate round, Cooperate if the number of Cooperators in the previous round meets or exceeds the threshold \( \frac{n}{k} \). If this threshold is not met, Defect.
  
- **Last Round:** Cooperate if the previous round's total meets the threshold; otherwise, Defect. This ensures that even in the final round, the strategy remains consistent and adaptive based on prior outcomes.

**2. Handling Edge Cases:**

- **First Round Handling:** Cooperate without exception to establish initial group cooperation.
  
- **Last Round Handling:** Defect only if cooperation isn't justified by the previous round's contribution levels. This maintains strategic consistency even as the game concludes.

**3. Collective Mindset:**

The strategy aligns with a collective approach by considering the group's previous contribution levels. It encourages cooperation when it benefits the group and adapts to prevent exploitation when cooperation wanes.

### Pseudocode Implementation:

```python
def adaptive_threshold_cooperation(game_parameters, history):
    n = game_parameters['n']
    k = game_parameters['k']
    r = game_parameters['r']
    current_round = history['current_round']
    
    if current_round == 1:
        return "C"
    else:
        previous_round = current_round - 1
        total_prev = history['round_{}'.format(previous_round)]['total_c']
        threshold = n / k
        
        if total_prev >= threshold:
            return "C"
        else:
            return "D"
    
    if current_round == r:
        # For the last round, still use the same rule
        return "D"  # Alternatively, could follow the same condition as above
```

### Explanation:

- **Initial Cooperation:** The strategy begins with cooperation to maximize the initial public good.
  
- **Adaptive Threshold:** Players Cooperate if the previous round's contributions meet the threshold \( \frac{n}{k} \), ensuring individual contributions are justified by the public good returns.
  
- **Final Round Flexibility:** The last round's decision mirrors previous logic, maintaining strategy consistency and encouraging sustained cooperation until the game's end.

This approach is robust, adapting to group behavior while incentivizing cooperation when mutually beneficial, thus balancing individual and collective interests effectively.
'''

description_PROSOCIAL_1 = '''
### Prosocial Strategy for N-Player Public Goods Game

**1. Decision Rules:**
   - **First Round:** Always cooperate (C) to establish a prosocial tone.
   - **Subsequent Rounds:** Cooperate if the number of players who cooperated in the previous round is at least k. Otherwise, defect.
   - **Last Round:** Always cooperate, regardless of previous actions, to uphold prosocial behavior.

### Pseudocode Implementation

```python
def prosocial_strategy(n, k, r, history):
    """
    Returns 'C' or 'D' based on prosocial strategy.
    """
    current_round = len(history) + 1  # Current round to decide
    
    if current_round == 1:
        return 'C'  # Cooperate in the first round
    
    # Get previous round's cooperation count
    prev_coop = sum(action == 'C' for action in history[-1])
    
    if current_round == r:
        return 'C'  # Cooperate in the last round
    
    if prev_coop >= k:
        return 'C'  # Cooperate if enough players cooperated last round
    else:
        return 'D'  # Defect if not enough cooperated
    
    return 'D'  # Default case
```

### Strategy Explanation

- **First Round Cooperation:** Starts with cooperation to encourage a positive group dynamic.
- **Adaptive Cooperation:** Continues cooperating as long as at least k players cooperated previously, ensuring contributions are worthwhile.
- **Last Round Cooperation:** Maintains prosocial behavior even in the final round, promoting trust and fairness.

This strategy is simple, clear, and adaptive, balancing cooperation incentives with protection against exploitation.
'''

description_PROSOCIAL_2 = '''
**Strategy: k-nORM (k-Nash Observing and Reciprocating Mechanism)**

**Objective:** To design a prosocial strategy that fosters cooperation while being adaptive and resilient against various opponent behaviors in an N-Player Public Goods Game.

**Key Components:**

1. **Decision Rules:**
   - **First Round:** Cooperate (C) to establish a prosocial foundation.
   - **Subsequent Rounds:** Cooperate in round t if the number of cooperators in the previous round (t-1) meets or exceeds the threshold k; otherwise, Defect (D).

2. **Handling Edge Cases:**
   - **First Round:** Start with cooperation to encourage a positive initial interaction.
   - **Last Round:** Continue using the same rule as other rounds, maintaining consistency without special treatment.

3. **Prosocial Alignment:**
   - The strategy is based on reciprocal principles, rewarding cooperation with cooperation and responding to defection with defection, promoting fairness and discouraging exploitation.

**Pseudocode Implementation:**

```
function k_nORM(n, k, r):
    # Initialize previous cooperation count
    prev_coop_count = 0
    
    for each round in 1 to r:
        if round == 1:
            action = C
            observe and record others' actions
            prev_coop_count = count of cooperators
        else:
            if prev_coop_count >= k:
                action = C
            else:
                action = D
            observe and record others' actions
            prev_coop_count = count of cooperators
    return actions

```

**Explanation:**

- **Adaptability:** The strategy dynamically adjusts based on previous rounds' outcomes, fostering cooperation when others do so and defecting to prevent exploitation.
- **Robustness:** It handles various opponent strategies effectively, starting optimistically and adapting as needed.
- **Prosocial Norms:** Emphasizes fairness and reciprocation, key prosocial principles, encouraging group welfare through conditional cooperation.

This strategy balances cooperation and self-interest, making it a robust contender in a tournament setting.
'''

description_PROSOCIAL_3 = '''
**Adaptive k-Threshold Cooperation Strategy**

**1. Decision Rules:**
   - **First Round:** Always Cooperate (C) to initiate prosocial behavior.
   - **Subsequent Rounds:** 
     - Track the number of cooperators in the previous round.
     - Compare this number to the threshold, which is k/n.
     - **If** the previous round's cooperators meet or exceed k/n: Cooperate (C).
     - **Else** (if below the threshold): Defect (D).

**2. Handling Edge Cases:**
   - **First Round:** Cooperate to set a cooperative tone.
   - **Last Round:** Cooperate if the previous round's cooperation met the threshold, encouraging final cooperation.
   - **Forgiveness Mechanism:** After a few rounds of defection, if others start cooperating again, switch back to Cooperate to promote renewed prosocial behavior.

This strategy is designed to be prosocial, encouraging cooperation while being adaptive to others' actions, ensuring it's not exploited by defectors. It uses a threshold based on the game's parameters to make decisions, promoting collective payoff.
'''

description_PROSOCIAL_4 = '''
**Strategy: Adaptive Cooperative Threshold with Forgiveness**

**1. Decision Rules:**
- **First Round:** Always Cooperate (C).
- **Subsequent Rounds:** For each round t (t ≥ 2):
   - Compute the number of players who Cooperated in the previous round (C_prev).
   - If C_prev ≥ k, choose to Cooperate (C) in the current round.
   - If C_prev < k, choose to Cooperate with a probability ε (e.g., 20%) and Defect (D) with probability (1 - ε).

**2. Handling Edge Cases:**
- **First Round:** Start by Cooperating to set a prosocial tone.
- **Last Round:** Apply the same decision rules as other rounds, promoting consistency.
- **Forgiveness Mechanism:** Incorporate a 20% chance (ε) to Cooperate even when the previous round's cooperation was below the threshold, allowing for potential recovery of mutual cooperation.

**3. Prosocial Alignment:**
The strategy encourages cooperation and adapts based on group behavior, rewarding collective cooperation while maintaining resilience against defection through forgiveness. It aligns with a prosocial mindset by promoting mutual benefits and sustainable cooperation across rounds.

**Pseudocode Implementation:**

```python
import random

def prosocial_strategy(n, k, r, history):
    if not history:
        # First round: Cooperate
        return 'C'
    else:
        # Count Cooperations in the previous round
        C_prev = sum(1 for action in history[-1] if action == 'C')
        if C_prev >= k:
            return 'C'
        else:
            # 20% chance to Cooperate (forgiveness), else Defect
            if random.random() < 0.2:
                return 'C'
            else:
                return 'D'
```

This strategy balances reciprocity and forgiveness, aiming to maximize collective welfare by encouraging cooperation while being robust against various opponent behaviors.
'''

description_PROSOCIAL_5 = '''
To address the N-Player Public Goods Game, we need a strategy that fosters cooperation while being robust against varying opponent behaviors. The proposed strategy is prosocial, adaptive, and handles edge cases such as the first and last rounds.

### Strategy: Prosocial Adaptive Cooperation (PAC)

**1. Decision Rules:**

- **First Round:** Always Cooperate (C). This encourages initial cooperation and sets a prosocial tone.
  
- **Subsequent Rounds:** 
  - Cooperate in the current round if the number of cooperators in the previous round meets or exceeds a threshold, calculated as the ceiling of k (i.e., threshold = ⌈k⌉).
  - If the number of cooperators in the previous round is below this threshold, Defect (D).

- **Last Round:** Apply the same decision rule as other rounds. If the second last round met the threshold, cooperate; otherwise, defect.

**2. Handling Edge Cases:**

- **First Round Handling:** Start with cooperation to encourage mutual cooperation.
- **Last Round Handling:** Continue using the same cooperative logic, relying on the previous round's outcome to decide actions, promoting consistency.

**3. Prosocial Alignment:**

The strategy prioritizes collective welfare by cooperating when sufficient players do so, ensuring the public good's benefits are realized when achievable. It adapts to the group's behavior, balancing individual and collective interests.

**Pseudocode:**

```
def prosocial_strategy(n, k, r, history):
    if not history:  # First round
        return "C"
    
    # Calculate number of cooperators in the previous round
    previous_actions = history[-1]
    t_prev = sum(1 for action in previous_actions if action == "C")
    
    # Determine threshold
    threshold = math.ceil(k)
    
    if t_prev >= threshold:
        return "C"
    else:
        return "D"

# Handling the last round is incorporated by using the same logic based on the second last round's cooperation level.
```

### Explanation:

- **First Round Cooperation:** Initiates a prosocial stance, hoping to induce reciprocal cooperation.
- **Adaptive Cooperation:** Each subsequent round's decision is based on the previous round's cooperation rate, ensuring responsiveness to group behavior.
- **Robust Threshold:** Uses a ceiling of k as the threshold to decide cooperation, providing a clear, parameter-dependent rule.
- **Last Round Consistency:** Maintains strategy consistency, avoiding sudden shifts that could undermine cooperation.

This strategy is designed to be resilient and encouraging, promoting cooperation when beneficial and adapting when necessary, aligning with prosocial objectives.
'''

description_PROSOCIAL_6 = '''
**Strategy Design for N-Player Public Goods Game**

**Strategy Name:** Adaptive Prosocial Strategy

**Objective:** Maximize total group payoff while being adaptive to others' behaviors, ensuring fairness and discouraging free-riding.

---

### 1. Decision Rules

- **Cooperation Decision:**
  - Cooperate if the proportion of players who cooperated in the previous round is above a threshold.
  - **Threshold Calculation:** \( \frac{k}{n + k} \), where \( k \) is the multiplication factor and \( n \) is the number of players.

- **Defection Decision:**
  - Defect if the proportion of cooperators in the previous round is below or equal to the threshold.
  - Always defect in the last round to maximize individual payoff without future consequences.

---

### 2. Handling Edge Cases

- **First Round:** Always cooperate to encourage initial group cooperation.
- **Last Round:** Defect to secure personal gain since there are no future interactions to influence.
- **Between Rounds:** Adjust cooperation or defection based on the previous round's cooperation level relative to the threshold.

---

### 3. Prosocial Alignment

- **Encourages Cooperation:** Rewards previous cooperation by continuing to cooperate, fostering a collaborative environment.
- **Responsive:** Adapts to group behavior, maintaining cooperation when beneficial and defecting to avoid exploitation.
- **Fairness:** Ensures individuals are not consistently exploited by others' defection, promoting a balance between personal and group payoffs.

---

### 4. Pseudocode Implementation

```python
def adaptive_prosocial_strategy(n, k, r, history):
    current_round = len(history) + 1
    if current_round == 1:
        return "C"  # Cooperate in the first round
    elif current_round == r:
        return "D"  # Defect in the last round
    else:
        previous_actions = history[-1]
        cooperators = sum(1 for action in previous_actions if action == "C")
        proportion = cooperators / n
        threshold = k / (n + k)
        if proportion > threshold:
            return "C"
        else:
            return "D"
```

---

This strategy is designed to be both cooperative and responsive, promoting prosocial behavior while protecting against exploitation. It balances individual and group interests, ensuring a fair and adaptive approach in the N-Player Public Goods Game.
'''

description_PROSOCIAL_9 = '''
**Strategy Name: Conditional Cooperation Based on Public Good Sufficiency (CCPG)**

**1. Decision Rules:**
- **First Round:** Cooperate (C). All players start by contributing to the public good.
- **Subsequent Rounds:**
  - Calculate the public good per capita from the previous round: \( \text{PublicGood} = \frac{k}{n} \times \text{TotalCooperators}_{t-1} \).
  - If \( \text{PublicGood} \geq 1 \), Cooperate (C) in the current round.
  - Else, Defect (D) in the current round.

**Pseudocode:**
```
function decide_action(previous_rounds):
    if no previous rounds:
        return 'C'
    else:
        total_cooperators_prev = sum([1 if action == 'C' else 0 for action in previous_rounds[-1]])
        public_good = (k / n) * total_cooperators_prev
        if public_good >= 1:
            return 'C'
        else:
            return 'D'
```

**2. Handling Edge Cases:**
- **First Round:** Always Cooperate. This initializes the game with maximum possible cooperation.
- **Final Round:** The strategy does not differentiate; it follows the same rule based on the previous round's outcome. This prevents endgame exploitation.

**3. Prosocial Alignment:**
- **Cooperation When Beneficial:** By cooperating when the public good suffices, the strategy supports the group's welfare.
- **Adaptive Punishment:** Defects only when cooperation isn't beneficial, maintaining individual payoff without unnecessary altruism.
- **Robustness:** Functions across varying opponent behaviors, encouraging cooperation and adapting as needed.

**Summary:**
The CCPG strategy promotes sustained cooperation by contributing when the public good's benefits exceed the personal cost. It starts optimistic, cooperates when collective efforts justify it, and adapts to maintain fairness, ensuring a balance between prosocial behavior and individual payoff optimization.
'''

description_PROSOCIAL_10 = '''
To address the design of a prosocial strategy for the N-player Public Goods Game, we developed an adaptive and robust approach called "Prosocial Tit-for-Tat." This strategy encourages cooperation based on the collective behavior of the group, adapting decisions round by round to maximize the public good.

**Strategy: Prosocial Tit-for-Tat**

1. **First Round Cooperation:**
   - In the first round, the strategy always Cooperates (C). This initiates a cooperative tone and encourages others to follow suit.

2. **Subsequent Rounds Adaptation:**
   - After the first round, the strategy observes the number of players who Cooperated in the previous round.
   - Calculate the minimum required number of Cooperators needed to make continued cooperation beneficial. This is determined by the ceiling of (n/k), where n is the number of players and k is the multiplication factor.
   - If the number of Cooperators in the previous round meets or exceeds this threshold, the strategy will Cooperate in the current round. If not, it will Defect (D).

3. **Edge Cases Handling:**
   - **First Round:** Always Cooperate to set a prosocial precedent.
   - **Subsequent Rounds:** Use the threshold based on previous round's cooperation rate to decide the action.
   - **Last Round:** Continue using the same decision rule, promoting cooperation even in the final round to uphold the public good.

4. **Prosocial Alignment:**
   - The strategy is designed to enhance the public good by reciprocating cooperation when beneficial, making it prosocial and promoting group welfare.

**Pseudocode Example:**

```
def prosocial_tit_for_tat(n, k, r, history):
    if not history:  # First round
        return "C"
    else:
        last_round = history[-1]
        previous_coops = sum(actions == "C" for actions in last_round)
        required_coops = math.ceil(n / k)
        if previous_coops >= required_coops:
            return "C"
        else:
            return "D"
```

**Conclusion:**
The Prosocial Tit-for-Tat strategy effectively balances reciprocity and adaptability, encouraging cooperation when it benefits the group while protecting against exploitation. It starts with cooperation and adapts based on collective behavior, ensuring a robust and prosocial approach throughout the game.
'''

description_PROSOCIAL_11 = '''
**Strategy Design: Adaptive Prosocial Trigger (APT)**

**Objective:**  
The Adaptive Prosocial Trigger (APT) strategy is designed to promote sustained cooperation in an N-Player Public Goods Game. It dynamically adjusts based on the level of cooperation observed in previous rounds, balancing punishment for defection with forgiveness to re-establish cooperation.

**1. Decision Rules:**

- **First Round:** Cooperate (C) to set a prosocial tone.
- **Subsequent Rounds:**
  - Cooperate if the number of cooperators in the previous round meets or exceeds a threshold (e.g., average or a set proportion of players).
  - Defect if cooperation falls below the threshold, signaling dissatisfaction.
  - Revert to cooperation if cooperation levels rebound, indicating willingness to re-establish mutual cooperation.
  
**2. Handling Edge Cases:**
- **First Round:** Always start with cooperation.
- **Last Round:** Continue cooperating to maintain a prosocial stance, encouraging others to do the same.
- **Adaptation:** Use a moving threshold based on historical cooperation rates, allowing flexibility in response to changing group dynamics.

**3. Prosocial Alignment:**  
APT aligns with a prosocial mindset by initially cooperating, punishing defection, and offering forgiveness. It seeks to maximize collective payoff while being robust against various strategies.

**Pseudocode Overview:**

```
Initialize:
    cooperate = True
    past_cooperations = []
    threshold = 0.5  # Adjust based on game parameters

For each round from 1 to r:
    if first round:
        action = Cooperate
    else:
        previous_coop_rate = sum(past_cooperations) / len(past_cooperations)
        if previous_coop_rate >= threshold:
            action = Cooperate
        else:
            action = Defect
        # Forgiveness mechanism: after defecting, monitor if cooperation increases
        if action == Defect and recent_trend shows increased cooperation:
            action = Cooperate
    
    record own action
    observe others' actions
    past_cooperations.append(number_of_cooperators)
```

**Conclusion:**  
APT is an adaptive strategy that encourages cooperation by responding to group behavior, promoting a balance between punishment and forgiveness. It starts with cooperation, adapts based on observed behavior, and maintains a prosocial approach throughout the game.
'''

description_PROSOCIAL_12 = '''
**Prosocial Strategy for N-Player Public Goods Game**

**Objective:** Design a strategy that encourages cooperation while being adaptive and robust, ensuring a balance between rewarding cooperation and sanctioning defection.

**1. First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Initiates cooperation to set a prosocial tone and encourage others to follow suit.

**2. Subsequent Rounds:**
   - **Cooperation Rate Check:** Evaluate the number of cooperators in the previous round.
     - If the number of cooperators is greater than or equal to half of the total players (n/2), cooperate in the current round.
     - If the number of cooperators is less than half, defect to incentivize higher cooperation.

**3. Reciprocity Mechanism:**
   - **Action in Response:** Cooperate if the previous round's cooperation rate was high; defect if it was low.
   - **Rationale:** Encourages reciprocity by rewarding cooperation and sanctioning defection, promoting a balanced approach.

**4. Last Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Ends the game on a prosocial note, promoting goodwill without fear of retaliation.

**5. Edge Cases Handling:**
   - **Odd Number of Players:** Uses >= or < comparison for n/2 to handle both even and odd totals effectively.
   - **Robustness:** Balances punishment and cooperation to avoid cycles of defection, maintaining adaptability.

**Conclusion:** This strategy is designed to be prosocial, promoting cooperation while adaptively responding to others' actions, ensuring robustness across various scenarios.
'''

description_PROSOCIAL_13 = '''
**ProsSocial Strategy for N-Player Public Goods Game**

**Objective:** Design a prosocial, adaptive strategy that promotes cooperation while being robust against exploitation.

**Key Components:**

1. **Initial Cooperation:** Start by Cooperating in the first round to foster a prosocial environment.

2. **Adaptive Decision-Making:** For each subsequent round, decide to Cooperate or Defect based on the number of Cooperators in the previous round.

3. **Threshold Cooperation:** Cooperate if the number of Cooperators in the previous round exceeds the threshold of n/k. This ensures individual cooperation is beneficial given the public good's multiplier.

4. **Final Round Defection:** In the last round, switch to Defecting since there are no future interactions to influence, maximizing immediate payoff.

**Pseudocode:**

```
def prosocial_strategy(round, previous_actions, n, k, r):
    if round == 1:
        return "C"
    elif round == r:
        return "D"
    else:
        m_prev = count_cooperators(previous_actions)
        threshold = n / k
        if m_prev > threshold:
            return "C"
        else:
            return "D"
```

**Explanation:**

- **First Round:** Cooperate to signal willingness to contribute to the public good.
  
- **Rounds 2 to r-1:** Check the number of Cooperators from the previous round. If it exceeds n/k, Cooperate to maintain collective benefit. If not, Defect to avoid being exploited.

- **Last Round:** Defect as there’s no future consequence, thus maximizing personal gain in the final round.

This strategy promotes sustained cooperation by conditioning it on sufficient participation, ensuring fairness and discouraging free-riding while addressing the last-round temptation to defect.
'''

description_PROSOCIAL_14 = '''
To address the N-Player Public Goods Game, we've developed a prosocial strategy that balances cooperation and robustness against various opponent behaviors. The strategy, **Adaptive Prosocial Strategy (APSS)**, is designed to promote collective welfare while adapting based on the game's history.

**1. Decision Rules:**
- **First Round:** Cooperate (C) to initiate cooperation and foster a prosocial environment.
- **Rounds 2 to r-1:** Cooperate if the number of cooperators in the previous round is at least n/k (rounded to the nearest integer). If not, Defect (D) to retaliate against insufficient cooperation.
- **Last Round:** Defect (D) to maximize personal payoff, as future repercussions are absent.

**2. Handling Edge Cases:**
- **First Round:** Cooperate to encourage initial cooperation.
- **Last Round:** Defect to ensure personal gain when no future punishments are possible.

**3. Prosocial Alignment:**
The strategy seeks to maintain cooperation when beneficial, using reciprocity to retaliate against low cooperation rates, thus aligning with a prosocial mindset.

**Pseudocode:**

```python
def adaptive_prosocial_strategy(n, k, r, history=None):
    if history is None:
        history = []
    
    current_round = len(history) + 1
    
    if current_round == 1:
        action = 'C'
    elif current_round < r:
        previous_round = current_round - 1
        previous_cooperations = history[previous_round - 1].count('C')
        threshold = n / k
        if previous_cooperations >= threshold:
            action = 'C'
        else:
            action = 'D'
    else:
        action = 'D'
    
    return action
```

**Strategy Overview:**
- Starts with cooperation to encourage collective welfare.
- Adapts based on the previous round's cooperation level, ensuring cooperation continues only when beneficial.
- Defects in the final round to maximize individual payoff.

This approach is designed to be both adaptive and robust, promoting cooperation while safeguarding against exploitation.
'''

description_PROSOCIAL_15 = '''
To address the N-Player Public Goods Game, we've designed a prosocial strategy that balances cooperation and reciprocity, encouraging mutual benefit while being robust to various behaviors.

### Strategy Description

1. **First Round Cooperation**:
   - **Action**: Cooperate.
   - **Rationale**: Start with cooperation to set a prosocial tone and encourage others to reciprocate.

2. **Subsequent Rounds**:
   - **Action**: Based on the previous round's cooperation level, decide to Cooperate or Defect.
   - **Calculation**:
     - From the previous round's payoff, determine the total number of cooperators (c_prev) using the formula:
       - If you Cooperated: \( c_{\text{prev}} = \text{round}(\pi_{\text{prev}} \times \frac{n}{k}) \)
       - If you Defected: \( c_{\text{prev}} = \text{round}((\pi_{\text{prev}} - 1) \times \frac{n}{k}) \)
   - **Threshold Check**: If c_prev >= k, Cooperate; else, Defect.

3. **Edge Cases**:
   - **First Round**: Always Cooperate.
   - **Last Round**: Apply the same rules as other rounds, maintaining consistency without special treatment.

This strategy is designed to sustain cooperation when others reciprocate, while defecting when contributions are insufficient, promoting a balance between prosocial behavior and individual protection.

### Pseudocode Implementation

```python
def strategy(n, k, current_round, history):
    if current_round == 1:
        return 'C'  # Cooperate in the first round
    
    # History contains the previous payoff and the player's action
    pi_prev, c_i_prev = history
    
    if c_i_prev == 'C':
        sum_c = pi_prev * (n / k)
    else:
        sum_c = (pi_prev - 1) * (n / k)
    
    c_prev = round(sum_c)
    
    if c_prev >= k:
        return 'C'  # Cooperate if enough players cooperated previously
    else:
        return 'D'  # Defect if not enough players cooperated
```

This strategy adaptively responds to others' actions, fostering cooperation while being resilient to exploitation, aiming for mutual benefit in the game.
'''

description_PROSOCIAL_16 = '''
To address the N-Player Public Goods Game, a prosocial strategy must balance cooperation with protection against exploitation. The proposed strategy, **Adaptive k-Threshold Cooperation**, is designed to encourage cooperation while being robust against defectors.

### Strategy Description:

1. **First Round:** Always Cooperate (C) to initiate cooperation and encourage a prosocial norm.

2. **Subsequent Rounds:** 
   - Observe the number of players who Cooperated (C) in the previous round.
   - **Cooperate** in the current round if the number of Cooperators in the previous round was at least **k** (the multiplication factor provided as a game parameter).
   - **Defect** (D) if the number of Cooperators was less than **k**.

### Rationale:

- **Prosocial Orientation:** The strategy
'''

description_PROSOCIAL_17 = '''
**Prosccial Strategy: "Adaptive Cooperation with Threshold"**

**1. Decision Rules:**

- **First Round:** Always Cooperate (C) to set a cooperative tone.
  
- **Subsequent Rounds:** For each round beyond the first, calculate the average cooperation rate of all players across all previous rounds. If this average exceeds the threshold \( \frac{k}{n} \), Cooperate (C); otherwise, Defect (D).

**2. Handling Edge Cases:**

- **First Round:** Cooperate to encourage initial cooperation.
  
- **Last Round:** Apply the same decision rule as other rounds, maintaining consistency and promoting prosocial behavior throughout the game.
  
- **Interaction with Defectors:** If the cooperation rate falls below the threshold, the strategy temporarily switches to defection to avoid exploitation, potentially encouraging others to Cooperate if they follow a similar strategy.

**3. Prosccial Alignment:**

This strategy aligns with a prosocial mindset by rewarding cooperation with continued cooperation and responding to widespread defection by defecting. It's adaptive, using past behavior to guide future actions, and robust, as it doesn't rely on specific coordination mechanisms or assumptions about other players' strategies.

**Pseudocode:**

```python
# Initialize variables
total_coop = 0
history = []

for t in range(1, r+1):
    if t == 1:
        action = 'C'
    else:
        avg_coop_rate = total_coop / ((t-1)*n)
        if avg_coop_rate > k/n:
            action = 'C'
        else:
            action = 'D'
    history.append(action)
    # Send action
    play(action)
    # Receive observation of all players' actions
    current_coops = sum(actions in this round)
    total_coop += current_coops
```

This strategy dynamically adjusts based on collective behavior, fostering cooperation while protecting against exploitation, ensuring a balance between individual and collective benefits.
'''

description_PROSOCIAL_18 = '''
To address the challenge of designing a prosocial strategy for the N-player public goods game, we developed a strategy called **Prosocial Threshold Cooperation (PTC)**. This strategy is crafted to be adaptive, robust, and aligned with prosocial values, encouraging cooperation while remaining resilient against exploitation.

### Prosocial Threshold Cooperation (PTC) Strategy

#### 1. Decision Rules
- **Initial Cooperation**: In the very first round, the strategy dictates cooperation (C). This sets a prosocial tone and encourages others to reciprocate.
- **Adaptive Cooperation**: For each subsequent round, the strategy examines the number of players who cooperated in the previous round. If this number exceeds a calculated threshold, the player continues to cooperate; otherwise, they defect.

#### 2. Handling Edge Cases
- **First Round**: The strategy cooperates to establish a cooperative environment.
- **Subsequent Rounds**: The strategy dynamically adjusts based on the previous round's cooperation level, ensuring adaptability.
- **Last Round**: The strategy applies the same rule as other rounds, maintaining consistency and prosocial behavior.

#### 3. Prosocial Orientation
- **Encouraging Cooperation**: By starting with cooperation, the strategy promotes a collective benefit and motivates others to follow suit.
- **Resilience to Exploitation**: If the cooperation level drops below the threshold, the strategy shifts to defection, preventing undue exploitation.

### Pseudocode Implementation
```python
def prosocial_threshold合作(n, k, previous_round_actions):
    if previous_round_actions is None:
        # First round: Cooperate
        return "C"
    else:
        # Calculate number of cooperators in previous round
        c_prev = sum(1 for action in previous_round_actions if action == "C")
        threshold = n / k
        if c_prev > threshold:
            return "C"
        else:
            return "D"
```

### Conclusion
The **Prosocial Threshold Cooperation (PTC)** strategy effectively balances cooperation and self-interest, making it a robust choice for the N-player public goods game. By starting cooperatively and adapting based on others' behavior, it promotes a prosocial environment while safeguarding against being exploited, ensuring sustained collective welfare.
'''

description_PROSOCIAL_19 = '''
**Prosocial Strategy: Adaptive Cooperation with Forgiveness**

**1. Decision Rules:**

- **First Round:** Always Cooperate (C) to initiate a prosocial tone.
  
- **Subsequent Rounds:**
  - Calculate the average cooperation rate (average_c) from the previous round.
  - If average_c ≥ 1/k, Cooperate (C).
  - If average_c < 1/k, Defect (D) once, then return to Cooperate (C) in the following round, regardless of others' actions (forgiveness mechanism).

**2. Handling Edge Cases:**

- **First Round:** Cooperate to set a positive tone.
- **Last Round:** Cooperate if the previous round's average_c ≥ 1/k; otherwise, Defect.
- **All Rounds:** Use the average_c from the most recent round to decide actions, ensuring adaptability.

**3. Prosocial Alignment:**

- Encourages cooperation while allowing for adaptive responses to defection.
- Forgiveness mechanism helps prevent perpetual defection cycles, maintaining prosocial behavior.

**Pseudocode Example:**

```python
def prosocial_strategy(game_params, history):
    round = history.current_round
    n = game_params.n
    k = game_params.k
    if round == 1:
        return "C"
    else:
        prev_actions = historyisAdmin previous_actions
        total_c = sum(1 for a in prev_actions if a == "C")
        average_c = total_c / n
        threshold = 1 / k
        if average_c >= threshold:
            return "C"
        else:
            # Check if previous action was punishment
            if hasattr(prosocial_strategy, 'punished_last'):
                if prosocial_strategy.punished_last:
                    prosocial_strategy.punished_last = False
                    return "C"
                else:
                    if average_c < threshold:
                        prosocial_strategy.punished_last = True
                        return "D"
                    else:
                        return "C"
            else:
                if average_c < threshold:
                    prosocial_strategy.punished_last = True
                    return "D"
                else:
                    return "C"
    return "C"  # default
```

**Explanation:**

- The strategy begins with cooperation, setting a cooperative tone.
- It adaptively adjusts based on the previous round's cooperation level, using 1/k as a threshold.
- If cooperation is below the threshold, it defects once, then returns to cooperation, fostering a forgiving environment.
- This balance between cooperation and adaptive forgiving ensures robustness against various opponent behaviors while promoting prosocial outcomes.
'''

description_PROSOCIAL_20 = '''
**Strategy: Prosocial Adaptive Cooperation (PAC)**

**1. Decision Rules:**

- **First Round (t=1):** Cooperate (C) to initiate a prosocial tone.
  
- **Rounds 2 to r-1 (t=2 to t=r-1):**
  - Calculate the average cooperation rate from the previous round, avg_c_prev = (sum of c_j at t-1) / n.
  - Cooperate if avg_c_prev ≥ 0.8; otherwise, Defect.

- **Last Round (t=r):** Cooperate to maintain trust and end on a prosocial note.

**2. Handling Edge Cases:**
  
- **First Round:** Start with Cooperation to signal willingness to collaborate.
  
- **Last Round:** Cooperate to foster a positive conclusion, encouraging a final collective benefit.

**3. Prosocial Alignment:**
  
- The strategy prioritizes collective benefit by encouraging Cooperation when there's a high level of participation, thereby maximizing shared payoffs.
  
- It adapts to others' actions, balancing individual protection against exploitation with the pursuit of higher collective rewards.

---

By following this strategy, players aim to enhance collective payoffs while remaining responsive to group behavior, ensuring a balance between cooperation and self-protection.
'''

description_PROSOCIAL_21 = '''
To address the N-Player Public Goods Game, we design a prosocial strategy that encourages cooperation while adaptively responding to others' actions. The strategy is based on rewarding cooperation when sufficient players contribute and defecting otherwise, creating a balance between prosocial behavior and retaliatory measures.

**Strategy Name: Cooperative Reciprocity**

**Decision Rules:**

1. **First Round:** Always Cooperate (C). This sets a positive tone and encourages initial cooperation from others.

2. **Subsequent Rounds:** 
   - Let `t_prev` be the number of players who Cooperated in the previous round.
   - If `t_prev` is greater than or equal to the threshold `k`, Cooperate in the current round.
   - If `t_prev` is less than `k`, Defect (D) in the current round to signal dissatisfaction with insufficient cooperation.

**Edge Cases:**
- **First Round:** Cooperate to initiate a cooperative environment.
- **Last Round:** Follow the same rule as other rounds, using the second last round's cooperation level to decide.

**Prosocial Alignment:**
This strategy promotes cooperation by rewarding it when enough players contribute, thus fostering a mutually beneficial environment. It adapts by punishing low cooperation levels, aiming to maintain a balance that encourages prosocial behavior without being exploitable.

**Pseudocode:**

```python
def cooperative_reciprocity(n, k, history):
    if not history:  # First round
        return 'C'
    else:
        t_prev = sum(1 for action in history[-1] if action == 'C')
        if t_prev >= k:
            return 'C'
        else:
            return 'D'
```

This strategy is crafted to be adaptive, encouraging contributions when beneficial and adjusting when contributions fall short, ensuring robustness across diverse player behaviors.
'''

description_PROSOCIAL_22 = '''
**Strategy Design: Prosocial Adaptive Cooperation (PAC)**

**1. Decision Rules:**

- **First Round:** Always Cooperate (C) to set a prosocial tone.
  
- **Subsequent Rounds (2 to r-1):** 
  - Calculate the average number of cooperators from all previous rounds.
  - If the average meets or exceeds the threshold (n/k), Cooperate; otherwise, Defect.

- **Last Round:** Always Cooperate, regardless of previous outcomes, to maintain trust and prosocial behavior.

**2. Handling Edge Cases:**

- **First Round:** Initiate with Cooperation to encourage mutual collaboration.
- **Last Round:** Cooperate to uphold a prosocial stance, fostering goodwill even as the game concludes.
- **Threshold Calculation:** The threshold is dynamically determined as the average number of players needed to make cooperation beneficial, calculated as n/k. This threshold adapts based on game parameters, ensuring responsiveness to the group's behavior.

**3. Prosocial Alignment:**

The strategy is designed to promote cooperation while protecting against exploitation. By starting with cooperation and adjusting based on collective behavior, it fosters a community-oriented approach. It rewards sustained cooperation and adapts to varying levels of participation, maintaining a balance between individual and collective benefits.

**Pseudocode Implementation:**

```
def prosocial_strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return 'C'
    current_round = len(history) + 1
    if current_round == r:  # Last round
        return 'C'
    # Calculate average cooperators in previous rounds
    avg_c = sum(round_info['cooperators'] for round_info in history) / len(history)
    threshold = n / k
    if avg_c >= threshold:
        return 'C'
    else:
        return 'D'
```

This strategy encourages sustained cooperation through adaptivity and reciprocity, aligning with a prosocial mindset while remaining robust against diverse opponent behaviors.
'''

description_PROSOCIAL_23 = '''
### Graded Reciprocity Strategy

**1. Decision Rules:**
- **First Round:** Cooperate (C). This sets a prosocial tone and encourages others to cooperate.
- **Subsequent Rounds:** For each round after the first, examine the number of players who cooperated (C) in the previous round. Let this number be `c_prev`.
  
  - **Cooperate (C):** If the number of previous cooperators `c_prev` is at least the multiplication factor `k`.
  - **Defect (D):** If `c_prev` is less than `k`, indicating insufficient cooperation.

**2. Handling Edge Cases:**
- **First Round:** Always Cooperate to encourage initial cooperation.
- **Last Round:** Apply the same decision rule as any other round, maintaining consistency and prosocial behavior even in the final round.

**3. Prosocial Alignment:**
This strategy is designed to foster cooperation by rewarding previous cooperative behavior and discouraging defection when cooperation is insufficient. It adapts to the group's behavior, promoting a balance between individual and collective benefits.

**Pseudocode:**
```python
def graded_reciprocity(n, k, history):
    if not history:  # First round
        return 'C'
    else:
        c_prev = history[-1]['cooperations']
        if c_prev >= k:
            return 'C'
        else:
            return 'D'
```

This strategy is adaptive, encouraging cooperation while protecting against exploitation, making it robust and aligned with prosocial values.
'''

description_PROSOCIAL_24 = '''
** Strategy: Adaptive Prosocial Retaliation (APR) **

** Overview:**
APR is designed to foster cooperation while protecting against exploitation. It begins optimistically, encouraging mutual cooperation, and adapts based on the collective behavior of players. The strategy retaliates against defection but Forgives to re-establish cooperation, ensuring a balance between prosociality and self-protection.

** Decision Rules:**

1. **Initial Cooperation:**
   - **First Round:** Always Cooperate (C). This sets a cooperative tone, encouraging others to reciprocate.

2. **Cooperation Phase:**
   - **Ongoing Rounds:** Cooperate if the majority (more than 50%) of players Cooperated in the previous round. This continues as long as sufficient cooperation is maintained.

3. **Defection and Forgiveness:**
   - **Trigger:** If fewer than 50% Cooperated, switch to Defect (D) for the next round.
   - **Forgiveness:** After Defecting, Cooperate again if the cooperation rate meets or exceeds 50%.

4. **Retaliation Tolerance:**
   - **Threshold:** If cooperation drops below 50%, Defect for up to 3 consecutive rounds to signal dissatisfaction, then revert to Cooperate to allow a reset.

5. **Final Round Adaptation:**
   - **Last Round:** Cooperate if the average cooperation rate over all previous rounds is 50% or higher. Otherwise, Defect to maximize personal payoff.

** Pseudocode:**

```
Initialize:
    cooperation_threshold = 0.5
    max_retaliation_rounds = 3
    retaliate_count = 0
    total_cooperations = 0
    apr_cooperation = True  # Start Cooperating

For each round from 1 to r:
    If round == 1:
        Action = C
    Else:
        previous_cooperation_rate = total_cooperations / (n*(round-1))
        If previous_cooperation_rate >= cooperation_threshold:
            Action = C
            retaliate_count = 0
        Else:
            If retaliate_count < max_retaliation_rounds:
                Action = D
                retaliate_count += 1
            Else:
                Action = C  # Forgive and try to reset
                retaliate_count = 0
        # Update total_cooperations
        total_cooperations += 1 if Action == C else 0

    # Handle last round differently
    If round == r:
        overall_cooperation_rate = total_cooperations / (n*r)
        If overall_cooperation_rate >= cooperation_threshold:
            Action = C
        Else:
            Action = D

    Execute Action and update history
```

**Robustness and Prosocuality:**
- **Adaptability:** APR adapts by rewarding cooperation and retaliating against defection, maintaining flexibility.
- **Forgiveness:** After retaliation, it Forgives to reset cooperation, preventing perpetual cycles of defection.
- **Edge Cases:** Handles first and last rounds with clear rules, encouraging prosociality while protecting self-interest when necessary.

This strategy promotes a culture of cooperation while safeguarding against exploitation, making it both prosocial and robust in various scenarios.
'''

description_PROSOCIAL_25 = '''
To address the challenge of designing a prosocial strategy for the N-player public goods game, we developed an adaptive and robust approach that encourages cooperation while safeguarding against exploitation. The strategy, named "Prosocial Adaptive Cooperation" (PAC), is based on observing past behavior and adjusting current actions accordingly. Here's a detailed overview:

### Strategy Design: Prosocial Adaptive Cooperation (PAC)

1. **First Round Cooperation**:
   - All players cooperate in the first round. This sets a cooperative tone and maximizes initial potential for collective benefit.

2. **Subsequent Rounds**:
   - In each subsequent round, each player observes the number of cooperators from the previous round.
   - If the number of cooperators in the previous round exceeds the threshold \( \frac{n}{k} \), the player cooperates in the current round.
   - If the number of cooperators is less than or equal to \( \frac{n}{k} \), the player defects.

3. **Threshold Calculation**:
   - The threshold is determined by the game parameters \( n \) (number of players) and \( k \) (multiplication factor). Specifically, the threshold is \( \frac{n}{k} \).
   - Players cooperate if the previous round's cooperation level exceeds this threshold, ensuring that contribution is beneficial.

4. **Last Round Handling**:
   - The strategy inherently addresses the last round by using the cooperation level of the second last round. There's no need for special treatment as the decision is based on prior behavior.

### Pseudocode Implementation

```python
def prosocial_strategy(n, k, history):
    """
    Prosocial Adaptive Cooperation (PAC) Strategy

    Parameters:
    - n (int): Number of players
    - k (float): Multiplication factor
    - history (list): List of tuples (round, cooperators_count)

    Returns:
    - action (str): 'C' for Cooperate, 'D' for Defect
    """
    if not history:  # First round
        return 'C'
    else:
        last_round = history[-1]
        c_prev = last_round[1]  # Number of cooperators in last round
        threshold = n / k
        if c_prev > threshold:
            return 'C'
        else:
            return 'D'
```

### Strategy Explanation

- **Prosocial Intent**: The strategy is designed to maximize collective payoff by encouraging cooperation when beneficial.
- **Adaptability**: It adjusts based on the previous round's cooperation level, ensuring responsiveness to group behavior.
- **Robustness**: By using a threshold based on game parameters, the strategy avoids being exploited and maintains cooperation when advantageous.

This approach ensures that players collectively contribute to the public good while protecting against excessive defection, promoting a balance between prosocial behavior and strategic rationality.
'''

description_PROSOCIAL_27 = '''
To address the N-Player Public Goods Game, the strategy "Prosoc" is designed to promote cooperation while being adaptive and robust. It starts by cooperating in the first round to encourage others. For subsequent rounds, it uses a threshold based on the game parameters n (number of players) and k (multiplication factor). The threshold is calculated as the ceiling of n divided by k. If the number of cooperators in the previous round meets or exceeds this threshold, the strategy cooperates again; otherwise, it defects.

### Strategy: Prosoc

**Decision Rules:**
1. **First Round:** Always cooperate to establish a cooperative baseline.
2. **Subsequent Rounds:** Calculate the threshold as the ceiling of n divided by k. If the number of cooperators in the previous round is at least this threshold, cooperate in the current round; otherwise, defect.

**Handling Edge Cases:**
- **First Round:** Cooperate to set a prosocial tone.
- **Last Round:** Treat it like any other round, using the previous round's cooperation rate to decide action, ensuring consistency.

**Prosocial Alignment:** The strategy encourages collective payoff by cooperating when others do, fostering a cooperative environment while protecting against exploitation when cooperation is insufficient.

**Pseudocode:**
```python
def prosoc_strategy(n, k, r):
    total_c_previous = 0
    for round in range(1, r + 1):
        if round == 1:
            action = 'C'
        else:
            threshold = math.ceil(n / k)
            if total_c_previous >= threshold:
                action = 'C'
            else:
                action = 'D'
        # Play action and observe others' actions
        total_c_current = 0
        # After all actions are played, count the number of cooperators
        total_c_previous = total_c_current
    return action
```

This strategy is adaptive, ensuring it responds to the group's cooperation levels, and robust, adjusting its behavior to avoid being exploited when cooperation is low.
'''

description_PROSOCIAL_28 = '''
To address the N-Player Public Goods Game, I've developed a strategy that promotes prosocial behavior through reciprocity and adaptability. This approach aims to encourage cooperation while maintaining robustness against defectors.

**Strategy: Reciprocal Cooperation Based on Public Goods Contribution (RCBPC)**

**1. Decision Rules:**

- **First Round:** Always Cooperate (C) to establish a cooperative tone.
  
- **Rounds 2 to r-1:** Cooperate if the number of players who Cooperated in the previous round is at least **k**. If fewer than **k** players Cooperated, Defect (D). This rule uses the game's multiplication factor **k** to determine the threshold for cooperation, ensuring that the group's contribution sufficiently benefits the public good.

- **Last Round (r):** Cooperate if the average number of Cooperators across all previous rounds is at least **k**. This final round decision reflects on the group's overall cooperation history to determine the action, encouraging sustained cooperation.

**2. Handling Edge Cases:**

- **First Round Handling:** Initiate cooperation to foster mutual cooperation from the beginning.
  
- **Last Round Handling:** The strategy considers the entire history of cooperation to make a prosocial choice, rather than simply defecting due to the endgame.

**3. Pros 판매ial Alignment:**

- The strategy aligns with prosocial behavior by prioritizing cooperation and using a forgiveness mechanism through the reciprocity rule. It encourages others to cooperate by rewarding past cooperation and only defecting when the group's contribution falls below the beneficial threshold.

**4. Forgiveness and Adaptability:**

- The strategy includes a forgiveness mechanism where if the group meets the cooperation threshold after a round of defection, it returns to cooperation, allowing for recovery from temporary defection.

**5. Pseudocode:**

```
def reciprocal_cooperation():
    # Initialize cooperation in the first round
    action = 'C'
    cooperation_history = []

    for round in range(1, r + 1):
        if round == 1:
            cooperation_history.append('C')
            continue
        elif round < r:
            # Calculate number of cooperators in the previous round
            c_prev = sum(1 for a in cooperation_history[-1] if a == 'C')
            if c_prev >= k:
                action = 'C'
            else:
                action = 'D'
        else:
            # Last round: check average cooperation
            total_coop = sum(1 for actions in cooperation_history for a in actions if a == 'C')
            avg_coop = total_coop / (r * n)
            if avg_coop >= k:
                action = 'C'
            else:
                action = 'D'
        cooperation_history.append(action)
        # Note: actual implementation would track all players' actions
    return action

# Note: This is a simplified version; actual implementation would consider all players' actions each round.
```

This strategy effectively balances individual incentives with collective benefits, fostering a prosocial environment while being robust against various opponent behaviors in a tournament setting.
'''

description_PROSOCIAL_29 = '''
### Strategy: **Adaptive Prosociality with Punishment (APP)**

**Overview:**
This strategy is designed to encourage prosocial behavior while being robust to exploitation. It adapts based on group cooperation levels and includes punishment mechanisms.

**1. Decision Rules:**

- **First Round:** Always Cooperate.
- **Subsequent Rounds:**
  - **Calculate Last Round's Cooperation Rate:** Determine the number of cooperators.
  - **Threshold Check:** If cooperators ≥ average (n/2), Cooperate; else, Defect.
  - **Punishment Mechanism:** If Decorations are below average, Defect in the current round, then revert to Cooperate in the next round if the cooperation rate improves.
- **Final Round:** If previous round had high cooperation, Cooperate; else, Defect.

**Pseudocode:**
```python
def adaptive_prosocial_strategy(history, current_round, total_rounds):
    if current_round == 1:
        return "C"
    else:
        previous_coop = sum(1 for action in history[-1] if action == "C")
        if previous_coop >= (n / 2):
            return "C"
        else:
            return "D"
    if current_round == total_rounds:
        previous_coop = sum(1 for action in history[-1] if action == "C")
        if previous_coop >= (n / 2):
            return "C"
        else:
            return "D"
```

### Explanation:
- **First Round Cooperation:** Starts by Cooperate to foster initial trust.
- **Adaptive Decision Making:** Adjusts based on previous round's cooperation rate, encouraging continued cooperation.
- **Punishment Mechanism:** Temporarily Defects if cooperation is low, then resumes cooperation if behavior improves.
- **Final Round Handling:** Cooperates if there was high cooperation previously, ending on a prosocial note.

This strategy encourages cooperation while protecting against exploitation, ensuring a balance between prosocial behavior and self-interest.
'''

description_PROSOCIAL_30 = '''
To address the N-player Public Goods Game, I've outlined a prosocial strategy that encourages cooperation while adaptively responding to other players' actions. Here's the structured approach:

---

### Prosocial Strategy: Adaptive Cooperation with Forgiveness

1. **First Round**: Cooperate. This initializes a prosocial tone, encouraging others to follow suit.

2. **Subsequent Rounds**:
   - **Cooperation Threshold (t)**: Calculate the minimum number of cooperators needed to make cooperation beneficial. This threshold is determined by \( t = \lceil \frac{n}{k} \rceil \), ensuring that the collective contribution yields a sufficient return.
   - **Cooperation Check**: For each round, observe the number of cooperators from the previous round (\( C_{prev} \)).
     - **If \( C_{prev} \geq t \)**: Continue cooperating. This sustains high collective payoff.
     - **If \( C_{prev} < t \)**: Switch to defecting. This serves as a response to insufficient cooperation, preventing individual exploitation.

3. **Forgiveness Mechanism**: If after defecting, the number of cooperators in subsequent rounds meets or exceeds \( t \), revert to cooperating. This allows recovery from periods of low cooperation without perpetual defection.

4. **Edge Cases**:
   - **Last Round**: The strategy naturally extends to the final round, as prior cooperation levels determine the action without requiring future punishment.
   - **Small n or k**: For scenarios like 2 players, the strategy mirrors Tit-for-Tat, promoting mutual cooperation based on observed actions.

This approach balances prosocial behavior with adaptive responses, ensuring robustness against diverse opponent behaviors while maximizing collective payoffs.

---

### Pseudocode Summary

```python
def prosocial_strategy(n, k, r, history=None):
    if not history:  # First round
        return "C"
    else:
        t = ceil(n / k)
        C_prev = count_cooperators(history[-1])
        if C_prev >= t:
            return "C"
        else:
            return "D"
```

This strategy initializes with cooperation and dynamically adjusts based on previous round outcomes, fostering a cooperative environment while maintaining the ability to respond to defections.
'''

description_PROSOCIAL_31 = '''
### Prosocial Strategy: **"Adaptive Prosociality with Forgiveness"**

This strategy balances cooperation with prudent self-interest, fostering prosocial outcomes while protecting against exploitation. It uses past behavior to adapt decisions and includes mechanisms to enforce cooperation norms.

---

#### 1. **Decision Rules**
- **First Round:**
  - **Action:** Cooperate (C)
     - Rationale: Start with prosocial behavior to establish cooperation norms and maximize joint payoffs.

- **Subsequent Rounds (t > 1):**
  - **Action:** Cooperate (C) if the fraction of cooperators in the previous round(s) meets a cooperation threshold (τ = 0.5).
     - Rationale: Maintain cooperation if enough players are contributing to the public good.
  - **Action:** Defect (D) if cooperation falls below τ.
     - Rationale: Defect to avoid being exploited when cooperation is insufficient.

- **Punishment Mechanism:**
  - If a player defects while others cooperate, introduce a punishment phase:
     - **Action:** Defect (D) for 1 round.
     - **Rationale:** Teach a lesson to deter free-riding.

- **Forgiveness:**
  - After punishing, revert to evaluating cooperation levels.
     - Rationale: Allow for potential reciprocity and cooperation restart.

#### 2. **Handling Edge Cases**
- **First Round:**
  - Cooperate to set a prosocial tone.
- **Last Round (t = r):**
  - Cooperate if others have been cooperative overall.
- **Punishment Edge Cases:**
  - If all players cooperate, avoid punishment.
  - If all defect, defect to avoid being exploited.

#### 3. **Prosocial Alignment**
- Encourages collective well-being by starting and maintaining cooperation.
- Balances reciprocity with self-protection to sustain cooperation over time.

---

### Pseudocode

```python
def adaptive_prosocial_strategy(game_history):
    if no previous rounds:
        return "C"
    else:
        previous_actions = game_history[-1]
        cooperators = sum(previous_actions)
        cooperation_level = cooperators / n
        
        if cooperation_level >= 0.5:
            return "C"
        else:
            return "D"

    # Punishment mechanism (optional, for advancedlescope)
    if detect_free_riding(game_history):
        return "D" for 1 round
        reset_punishment()
```

---

### Summary

This strategy starts prosocial, adapts based on cooperation levels, punishes free-riding, and balances cooperation with self-interest. It's designed to foster mutual cooperation while protecting against exploitation, ensuring robust performance in diverse tournament scenarios.
'''

description_PROSOCIAL_32 = '''
**Prososal Strategy: Adaptive Reciprocity with Forgiveness**

**Objective:**  
Maximize the total public good by encouraging widespread cooperation while being resilient to exploitation.

**Strategy Overview:**  
This strategy employs a dynamic approach, adapting based on the cooperation levels of other players. It uses reciprocity to reward cooperation and punishes defection, while incorporating forgiveness to allow for reestablishment of cooperation.

**Detailed Strategy:**

1. **First Round Cooperation:**
   - **Action:** Cooperate (C).
   - **Rationale:** Initiates a prosocial tone, encouraging others to reciprocate.

2. **Subsequent Rounds:**
   - **Calculate Previous Cooperation Rate:** Assess the average cooperation rate from the last round.
   - **Threshold Evaluation:** Cooperate if the cooperation rate meets or exceeds the current threshold.
   - **Adjust Threshold:**
     - **Increase Threshold:** If cooperation meets or exceeds the threshold, slightly raise it to encourage higher future cooperation.
     - **Decrease Threshold:** If cooperation is below the threshold, lower it to facilitate future cooperation after a punishment phase.

3. **Punishment Mechanism:**
   - **Defect for T Rounds:** If cooperation is below the threshold, defect for T rounds to sanction defectors.
   - **Reset Post-Punishment:** After the punishment period, cooperate once more to potentially restart cooperation.

4. **Last Round Handling:**
   - **Assess Historical Cooperation:** If most players have cooperated throughout the game, cooperate in the final round.
   - **Rationale:** Ends the game on a prosocial note, encouraging positive behavior even without future consequences.

**Balancing Act:**  
This strategy maintains cooperation through reciprocity, while its forgiveness component prevents perpetual punishment, allowing for recovery and sustained prosocial behavior.

**Implementation Tips:**
- **Initial Threshold:** Start with a low threshold to encourage early cooperation.
- **Adjustment Rate:** Use a moderate adjustment rate to avoid sudden changes.
- **Punishment Duration:** Keep T short to avoid prolonged defection.

This strategy is robust, adaptable, and prosocial, designed to thrive in dynamic, multi-player environments.
'''

description_COMMUNAL_1 = '''
**Communal Strategy for N-Player Public Goods Game**

**1. Decision Rules:**

- **First Round:** Cooperate. This sets a positive tone and encourages initial cooperation.
- **Subsequent Rounds:**
  - Calculate the proportion of players who Cooperated in the previous round, denoted as \( p_{t-1} \).
  - If \( p_{t-1} \) is greater than or equal to \( \frac{k}{n} \), Cooperate in the current round.
  - Otherwise, Defect in the current round.

**2. Handling Edge Cases:**

- **First Round:** Always Cooperate to initiate a cooperative environment.
- **Last Round:** Apply the same decision rule based on the previous round's cooperation rate.

**3. Communal Alignment:**

The strategy promotes the collective good by encouraging cooperation when sufficient others are doing so, and defects when cooperation levels are insufficient, thus maintaining a balance between individual and group incentives.

---

**Pseudocode Implementation:**

```python
def strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return "C"
    else:
        last_round = history[-1]
        coop_count = sum(1 for action in last_round if action == "C")
        p_prev = coop_count / n
        threshold = k / n
        if p_prev >= threshold:
            return "C"
        else:
            return "D"
```

This strategy adaptively responds to the group's behavior, fostering cooperation while protecting against excessive defection, aligning with a communal mindset.
'''

description_COMMUNAL_2 = '''
**Communal Public Goods Game Strategy: Cooperative Punishment**

**1. Decision Rules:**

- **Round 1:** Always Cooperate (C). This initiates a cooperative tone, encouraging others to follow suit.
- **Rounds 2 to r-1:**  
  - Observe the number of cooperators (c_{t-1}) in the previous round.
  - Calculate the threshold: Check if \( k \times \frac{c_{t-1}}{n} > 1 \).  
    - If true, Cooperate in the current round.  
    - If false, Defect to punish insufficient cooperation.
- **Last Round (r):**  
  - Apply the same rule as other rounds based on the previous round's cooperation level.

**2. Handling Edge Cases:**

- **First Round:** Cooperate to set a positive precedent.
- **Last Round:** Decision based on the previous round's cooperation level, maintaining strategy consistency.

**3. Communal Alignment:**

This strategy promotes cooperation by rewarding groups that contribute adequately to the public good and punishing those that don't. It's adaptive, adjusting based on collective behavior, and robust against free-riding, ensuring fairness and promoting sustained cooperation.

**Pseudocode:**

```python
def strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    else:
        c_prev = history[-1]['cooperations']
        threshold_met = (k * c_prev) / n > 1
        if threshold_met:
            return 'C'
        else:
            return 'D'
```

This strategy encourages cooperation when beneficial and adapts based on group behavior, fostering a communal approach.
'''

description_COMMUNAL_3 = '''
To design a communal strategy for the N-Player Public Goods Game, I propose the following approach:

1. **Decision Rules:**
   - **First Round:** Always Cooperate to establish initial cooperation.
   - **Middle Rounds (2 to r-1):** Cooperate if the number of Cooperators in the previous round meets or exceeds a threshold based on the multiplication factor \( k \). Specifically, Cooperate if at least \( k \) players Cooperated in the previous round; otherwise, Defect.
   - **Last Round:** Defect, as there are no future rounds to fear retaliation, making Defection individually optimal.

2. **Edge Cases Handling:**
   - **First Round:** Start with Cooperation to encourage a positive initial contribution to the public good.
   - **Last Round:** Recognize the finiteness of the game and Defect to maximize personal payoff without future consequences.
   - **Middle Rounds:** Use the previous round's cooperation level to adapt behavior, promoting ongoing cooperation when enough players contribute.

3. **Communal Mindset:**
   - The strategy aligns with a communal mindset by encouraging collective cooperation through adaptive behavior. It rewards past cooperation and punishes insufficient contribution, fostering a balance between individual and group interests.

**Pseudocode Implementation:**

```python
def communal_strategy(n, k, r, history):
    if not history:  # First round
        return "C"
    if len(history) + 1 == r:  # Last round
        return "D"
    
    previous_round = history[-1]
    count_coop = sum(1 for action in previous_round if action == "C")
    
    if count_coop >= k:
        return "C"
    else:
        return "D"
```

This strategy is adaptive and robust, encouraging cooperation while mitigating the risk of excessive defection, ensuring a balance between individual and communal interests throughout the game.
'''

description_COMMUNAL_4 = '''
To address the N-Player Public Goods Game, we've designed a communal strategy that encourages cooperation while adapting to others' actions. The strategy uses a threshold based on the number of players and the multiplication factor to decide whether to cooperate or defect in each round. This approach ensures that cooperation is rewarded while minimizing exploitation, making it both robust and adaptive.

**Strategy:**

1. **First Round:** Always cooperate to set a cooperative tone.
2. **Subsequent Rounds:** For each round, use the number of cooperators from the previous round. If this number meets or exceeds the threshold (calculated as the ceiling of n/k), cooperate; otherwise, defect.
3. **Last Round:** Apply the same rule based on the second last round's cooperation level.

**Pseudocode:**
```
def strategy(n, k, r, history):
    if not history:
        return 'C'
    threshold = ceil(n / k)
    previous_coops = sum(history[-1])
    if previous_coops >= threshold:
        return 'C'
    else:
        return 'D'
```

**Details:**
- **Threshold Calculation:** The threshold is determined by `ceil(n/k)`, ensuring it's an integer that reflects the minimum number of cooperators needed to make cooperation beneficial.
- **Decision Making:** After the first round, the strategy reviews the number of cooperators from the previous round and decides based on whether this meets the threshold, promoting a balance between communal benefit and individual rationality.

This strategy effectively balances encouraging cooperation with protecting against exploitation, making it suitable for a wide range of opponent behaviors in the tournament.
'''

description_COMMUNAL_5 = '''
To design an effective communal strategy for the N-Player Public Goods Game, we focus on promoting cooperation while being adaptive to others' actions. The strategy starts with cooperation and continues if enough players cooperate, ensuring the public good is maintained.

**Answer:**

**Communal Strategy: Adaptive Cooperation Based on Previous Contribution**

1. **Initial Cooperation:**
   - **First Round:** Always Cooperate (C) to establish a cooperative baseline.

2. **Subsequent Rounds:**
   - After the first round, observe the number of players who Cooperated (c_prev) in the previous round.
   - **Cooperate** if c_prev is greater than or equal to the multiplication factor \( k \). This ensures that the contribution to the public good is sufficient to warrant continued cooperation.
   - **Defect (D)** if fewer than \( k \) players Cooperated in the previous round, as the public good may not justify the individual sacrifice.

3. **Edge Cases Handling:**
   - **First Round:** Start Cooperating to promote initial trust.
   - **Last Round:** Follow the same strategy as other rounds; no special treatment is needed since the strategy adapts based on history.

This strategy aligns with a communal mindset by encouraging contributions when there's sufficient participation, ensuring the public good is maintained effectively while being robust against various player behaviors.
'''

description_COMMUNAL_6 = '''
To address the N-player public goods game, here's a strategic approach designed to encourage cooperation while safeguarding against exploitation, ensuring a balance between communal benefit and individual payoff.

### Strategy Overview

This strategy is adaptive, relying on the game's history and parameters to make decisions. It aligns with a communal mindset, aiming to maximize group payoff while being robust against various behaviors.

### Decision Rules

1. **First Round Action**: Cooperate. This sets a cooperative tone, encouraging others to follow suit.

2. **Subsequent Rounds**: After the first round, the decision is based on the previous round's outcomes.
   - Calculate the public good term: (k/n) * total cooperators in the last round.
   - If this term exceeds 1, cooperate in the current round.
   - If it is 1 or less, defect to avoid being exploited.

3. **Final Round Handling**: The strategy remains consistent, using the previous round's outcome to decide, aligning with the communal goal even in the last round.

### Pseudocode Implementation

```python
def strategy(n, k, round, previous_round_coop):
    if round == 1:
        return "C"
    else:
        total_c_last = previous_round_coop
        threshold = 1
        if (k / n) * total_c_last > threshold:
            return "C"
        else:
            return "D"
```

### Explanation

- **First Round Cooperation**: Initiates cooperation to establish a cooperative environment.
- **Adaptive Decision Making**: Uses past cooperation levels to decide future actions, promoting sustained cooperation when beneficial.
- **Threshold Utilization**: The threshold (k/n)*total_c determines if cooperation is individually beneficial, preventing free-riding.
- **Robustness**: Functions without relying on others' strategies, adapting based on observed behavior.

This approach ensures the strategy is both communal and resilient, fostering cooperation while protecting against exploitation, making it suitable for a competitive tournament setting.
'''

description_COMMUNAL_7 = '''
**Communal Strategy: CARING (Cooperate And Reciprocate In Negotiated Goods)**

**1. Decision Rules:**

- **First Round:** Cooperate to establish a baseline of trust.
- **Subsequent Rounds:** Cooperate if the average cooperation rate in the previous round meets or exceeds a dynamic threshold. The threshold is calculated as the minimum of the proportion of previous cooperators and the strategy's own prior cooperation. If the average falls below this threshold, defect to signal dissatisfaction.
- **Punishment Phase:** If average cooperation is below the threshold, defect for one round to encourage others to cooperate. Resume cooperation if the average cooperation improves in subsequent rounds. If cooperation remains low, continue defecting to avoid exploitation.
- **Forgiveness Mechanism:** Gradually increase cooperation propensity over time if others begin to cooperate more frequently, allowing for reestablishment of cooperation.

**2. Handling Edge Cases:**

- **First Round:** Cooperate to signal willingness to collaborate.
- **Last Round:** Defect to maximize personal payoff, as future interactions are absent.
- **All Cooperate:** Continue cooperating to sustain collective benefit.
- **All Defect:** Adjust strategy to defect to avoid being exploited, with periodic tests to reinitiate cooperation if possible.
- **Mixed Strategies:** Adjust cooperative threshold dynamically based on observed behavior, balancing reciprocity with adaptability.

**3. Communal Mindset:**

The strategy aligns with a communal mindset by initially cooperating, adapting based on collective behavior, and using targeted punishment to maintain a balance between individual and group interests. It encourages sustained cooperation through reciprocal actions, fostering a shared environment of mutual benefit, while being robust against exploitation by defectors.
'''

description_COMMUNAL_8 = '''
**Strategy Design: Adaptive Communal Cooperation (ACC)**

1. **First Round Cooperation**:
   - **Action**: Always Cooperate in the first round to establish a cooperative foundation.

2. **Subsequent Rounds**:
   - **Cooperation Threshold**: Calculate the cooperation rate from the previous round. If the cooperation rate is above a certain threshold (e.g., 50%), Cooperate in the next round.
   - **Defection Response**: If the cooperation rate falls below the threshold, switch to Defecting in the next round to discourage exploitation.

3. **Adaptive Adjustments**:
   - **Dynamic Threshold**: Adjust the cooperation threshold based on historical data. If recent rounds have shown increasing Defection, lower the threshold to encourage adaptation. Conversely, raise the threshold if cooperation levels are high.
   - **Forgiveness Mechanism**: Periodically Cooperate again after a round of low cooperation to allow potential defectors to reconsider their strategy, preventing perpetual Defection cycles.

4. **Last Round Strategy**:
   - **Maintain Consistency**: Continue with the regular strategy to uphold fairness and consistency, rather than risking exploitation by Cooperating unconditionally.

5. **Payoff Consideration**:
   - **Benefit Evaluation**: Continuously assess the impact of k on the payoff structure. If k is high, emphasize the importance of maintaining higher cooperation levels to maximize public goods benefits.

This strategy encourages initial cooperation, adapts based on group behavior, and incorporates forgiveness to maintain social cohesion while discouraging exploitation. It aligns with a communal mindset by prioritizing collective benefit while protecting against unfair play.
'''

description_COMMUNAL_9 = '''
### Communal Strategy: **Adaptive Reciprocity with Threshold**

**Objective:**  
To create a cooperative strategy that adapts to the behavior of other players while promoting the overall well-being of the group. This strategy is designed to encourage cooperation while being robust against exploitation.

---

### 1. **Decision Rules**
The strategy is based on reciprocal behavior and uses a threshold to decide whether to Cooperate (C) or Defect (D) in each round. The decision rule is as follows:

- **Cooperation Threshold (CT):**  
  CT is a fraction (e.g., 0.5) that represents the minimum proportion of cooperation in the group required for the player to cooperate in the next round. This threshold is adaptive and can evolve over time.

- ** Past Cooperation Rate (PCR):**  
  PCR is the fraction of players who cooperated in the previous round.  
  If PCR ≥ CT, the player will Cooperate in the current round.  
  If PCR < CT, the player will Defect in the current round.

- **Adaptive Adjustment:**  
  The player adjusts the cooperation threshold (CT) dynamically based on the success of cooperation in past rounds. If cooperation has yielded high payoffs historically, CT is lowered to encourage continued cooperation. If cooperation has been exploited, CT is raised to protect the player's payoff.

**Pseudocode:**
```python
Initialize:
    cooperation_threshold = 0.5  # Initial threshold
    history = []  # Stores past cooperation rates and payoffs

For each round t in 1 to r:
    if t == 1:
        # First round: Cooperate to encourage others
        action = C
    else:
        # Calculate past cooperation rate (PCR)
        past_cooperation_rate = (number of cooperators in previous round) / n
        history.append(past_cooperation_rate)
        
        # Adjust cooperation threshold (CT) based on past outcomes
        if average_payoff_from_cooperation > average_payoff_from_defection:
            cooperation_threshold *= 0.9  # Lower threshold to encourage cooperation
        else:
            cooperation_threshold *= 1.1  # Raise threshold to protect payoffs
        
        # Ensure CT stays within adaptive bounds
        cooperation_threshold = max(0.2, min(cooperation_threshold, 0.8))
        
        # Decide action for current round
        if past_cooperation_rate >= cooperation_threshold:
            action = C
        else:
            action = D
    
    Take action
    Observe payoffs and actions of others
    Update history with new data
```

---

### 2. **Handling Edge Cases**
- **First Round:**  
  Cooperate unconditionally to create an opportunity for mutual cooperation. This signals a willingness to contribute to the public good and can encourage others to follow suit.

- **Last Round:**  
  Use the same decision rule as other rounds. Do not deviate from the strategy, even in the last round. This maintains consistency and aligns with the communal mindset.

- **All Cooperate or All Defect:**  
  If all players cooperate consistently, continue to cooperate. If all defect, adjust the cooperation threshold upward to protect payoffs.

---

### 3. **Communal Alignment**
This strategy aligns with the communal mindset by:
1. Encouraging cooperation by starting with cooperation and using a reciprocal approach.
2. Rewarding past cooperation by lowering the cooperation threshold when cooperation yields positive outcomes.
3. Protecting individual payoffs by raising the cooperation threshold when cooperation is exploited.
4. Promoting fairness by adjusting behavior based on the collective actions of the group.

---

### 4. **Robustness**
The strategy is robust to a wide range of opponent behaviors because:
- It starts with cooperation but can adapt to defection.
- It uses a dynamic threshold to balance cooperation and self-protection.
- It does not require coordination or communication with other players.

---

### 5. **Tournament Performance**
This strategy is designed to perform well in a tournament because:
- It promotes cooperation when beneficial, increasing group payoff.
- It protects individuals when cooperation is exploited.
- It does not rely on assumptions about other players' strategies.

By combining reciprocity, adaptivity, and a communal mindset, this strategy balances individual and group interests effectively.
'''

description_COMMUNAL_10 = '''
**Communal Strategy for N-Player Public Goods Game**

1. **First Round Cooperation**: Begin by cooperating in the first round to establish a cooperative tone and encourage mutual contribution.

2. **Reciprocal Cooperation**: In each subsequent round, base your action on the number of players who cooperated in the previous round. Cooperate if more than half of the players cooperated; otherwise, defect.

3. **Adaptive Threshold Adjustment**: Start with a threshold requiring more than half of the players to cooperate. If this threshold isn't met, decrease it by a fraction (e.g., 10%) in subsequent rounds. This allows the strategy to adapt to diminishing cooperation levels while remaining lenient towards potential revivals of cooperation.

4. **Consistency in Final Rounds**: Maintain the strategy even in the last round to avoid signaling a shift towards defection, ensuring uniformity throughout the game.

This approach encourages continued cooperation, adapts to group behavior, and remains robust againstvarying strategies, fostering a balance between communal benefit and individual payoff optimization.
'''

description_COMMUNAL_11 = '''
**Strategy: Adaptive Communal Cooperation (ACC)**

**1. Decision Rules:**
   - **First Round:** Cooperate unconditionally to initiate a cooperative norm.
   - **Subsequent Rounds:** Calculate the threshold based on the multiplication factor \( k \) and the number of players \( n \). If the number of cooperators in the previous round multiplied by \( k \) divided by \( n \) is greater than 1, cooperate. Otherwise, defect.

**2. Pseudocode:**
```
Initialize:
    cooperate_next = True  // Start by cooperating in the first round

For each round from 1 to r:
    if it's the first round:
        choose C
    else:
        previous_cooperators = count of C choices in previous round
        threshold = (previous_cooperators * k) / n
        if threshold > 1:
            choose C
        else:
            choose D
    update history with own choice
```

**3. Explanation:**
   - **First Round Cooperation:** Seeds a cooperative environment, encouraging others to follow suit.
   - **Adaptive Threshold:** Determines if the collective benefit justifies individual contribution, ensuring cooperation is mutually beneficial.
   - **Responsive to History:** Adjusts strategy based on past behavior, promoting sustained cooperation and deterring exploitation.

This strategy balances individual and collective benefits, fostering a communal approach that adapts to the group's dynamics.
'''

description_COMMUNAL_12 = '''
To address the N-Player Public Goods Game, we designed a communal strategy that adapts based on previous cooperation levels. The strategy encourages cooperation when a sufficient number of players contribute, ensuring a balance between individual and group benefits.

**Strategy: Adaptive Communal Cooperation (ACC)**

**1. Decision Rules:**
- **First Round:** Cooperate (C).
- **Subsequent Rounds:**
  - Let `c_prev` be the number of players who Cooperated in the previous round.
  - Calculate the threshold `m = ceil(n/k)`.
  - If `c_prev >= m`, Cooperate in the next round.
  - If `c_prev < m`, Defect in the next round.

**2. Edge Cases Handling:**
- **First Round:** Always Cooperate to establish an initial cooperative tone.
- **Subsequent Rounds:** Use the threshold rule to decide.
- **Last Round:** Apply the same rule as other rounds, promoting consistency and communal benefit.

**3. Communal Alignment:**
The strategy aligns with the communal mindset by prioritizing collective benefit. By Cooperating when enough players do so, it fosters a productive environment. If cooperation drops below the threshold, it adapts to individual protection, balancing communal goals with self-interest.

This approach ensures the strategy is adaptive, robust, and aligned with encouraging cooperation without assuming others' actions, making it suitable for the tournament scenario.
'''

description_COMMUNAL_13 = '''
To design a communal strategy for the N-Player Public Goods Game, we propose an adaptive approach that balances cooperation and defection based on historical cooperation rates. This strategy aims to maximize collective benefits while remaining robust against exploitation.

### Strategy: Adaptive k-Threshold Cooperation

**1. Decision Rules:**
- **First Round:** Cooperate (C) to establish an initial cooperative environment.
- **Subsequent Rounds:** After each round, calculate the average cooperation rate from all previous rounds. If this rate, when multiplied by the multiplication factor k, is at least 1, the player cooperates; otherwise, the player defects.

**2. Handling Edge Cases:**
- **First Round:** Always Cooperate to encourage initial cooperation.
- **Last Round:** The strategy doesn't change; decisions are based on historical data as in other rounds.

**3. Communal Alignment:**
- The strategy promotes cooperation when it is beneficial to the group, ensuring that the collective payoff is maximized. It adapts based on the community's past actions, fostering a cooperative mindset while defending against excessive defection.

### Pseudocode Implementation

```python
def adaptive_k_threshold(n, k, r, player_id):
    """
   
'''

description_COMMUNAL_14 = '''
**Communal Strategy for N-Player Public Goods Game**

**1. Decision Rules:**
- **First Round:** Always Cooperate (C) to establish trust and encourage initial cooperation.
- **Subsequent Rounds:** For each round t (where t > 1):
  - Calculate the number of players who Cooperated in the previous round (C_{t-1}).
  - If C_{t-1} is greater than or equal to a threshold T (floor(k)), Cooperate in round t.
  - If C_{t-1} is less than T, Defect in round t.
  - **Forgiveness Mechanism:** If the strategy defected in the previous round but C_{t} meets or exceeds T, switch back to Cooperate.

**2. Handling Edge Cases:**
- **First Round:** Initiate with Cooperation to set a positive tone.
- **Subsequent Rounds:** Use the previous round's cooperation rate to decide current action.
- **Last Round:** Apply the same decision rules as other rounds to maintain consistency and trust.

**3. Communal Mindset:**
- The strategy is designed to foster mutual benefit by encouraging cooperation when others cooperate and defecting when others do not, with forgiveness to reset cooperation when possible.

**Pseudocode:**
```
function Strategy(n, k, r, history):
    if current_round == 1:
        action = Cooperate
    else:
        count_prev_coop = count of cooperations in history[-1]
        threshold = floor(k)
        if count_prev_coop >= threshold:
            action = Cooperate
        else:
            action = Defect
        # Forgiveness: If previously defected but enough now cooperate, switch back
        if previous_action == Defect and count_prev_coop >= threshold:
            action = Cooperate
    return action
```

This strategy promotes sustained cooperation by rewarding reciprocal behavior and adapting to others' actions, ensuring robustness across various scenarios.
'''

description_COMMUNAL_15 = '''
To address the N-Player Public Goods Game, we designed a communal strategy that balances individual and group incentives through adaptive cooperation based on previous rounds' outcomes.

**Decision Rules:**
1. **First Round:** Cooperate to establish a cooperative norm.
2. **Subsequent Rounds:** Cooperate if the public good benefit from the previous round (k/n * C_prev) is at least 1; otherwise, Defect.

**Edge Cases:**
- **First Round:** Always Cooperate.
- **Last Round:** Apply the same decision rule based on the previous round's cooperation level.

**Communal Aspect:**
The strategy focuses on collective benefit, encouraging cooperation when the public good is sufficiently beneficial, aligning with a communal mindset.

Pseudocode:
```python
def decide_action(prev_c_round, current_round, total_rounds, k, n):
    if current_round == 1:
        return "Cooperate"
    else:
        public_good_benefit = (k / n) * prev_c_round
        if public_good_benefit >= 1:
            return "Cooperate"
        else:
            return "Defect"
```
'''

description_COMMUNAL_16 = '''
**Strategy Design for N-Player Public Goods Game**

**1. Decision Rules:**

- **First Round:** Cooperate (C) to initiate a cooperative tone.
- **Subsequent Rounds (2 to r-1):** 
  - Observe the number of cooperators in the previous round.
  - Calculate the threshold: if total_coop_prev * (k/n) > 1, cooperate; else, defect.
- **Last Round (r):** Use the same threshold rule as above based on the previous round's cooperation.

**2. Edge Cases Handling:**

- **First Round:** Always cooperate.
- **Last Round:** Decide based on the previous round's cooperation level using the threshold rule.
- **Switching Behavior:** If cooperation drops below the threshold, defect until the threshold is met again.

**3. Communal Alignment:**

Designed to balance individual and group payoffs, encouraging cooperation when beneficial and adapting to others' behavior to sustain public goods contribution.

**Pseudocode Example:**

```
Initialize:
    total_coop = 0
    for each round t from 1 to r:
        if t == 1:
            action = C
            total_coop += 1
        else:
            threshold = total_coop_prev * (k/n)
            if threshold > 1:
                action = C
                total_coop += 1
            else:
                action = D
        observe others' actions
        total_coop_prev = number of cooperators in previous round
    return total payoff
```

This strategy ensures adaptivity and robustness by reciprocating cooperation based on the group's past behavior relative to the game's parameters.
'''

description_COMMUNAL_18 = '''
To address the N-Player Public Goods Game, we've designed a communal strategy that balances cooperation with strategic defection to maintain collective welfare. The strategy, named "Dynamic Cooperativist," encourages cooperation while adaptively responding to others' actions, promoting a sustainable public good.

### Strategy Overview: Dynamic Cooperativist

1. **First Round**: Cooperate to establish a cooperative tone.
2. **Subsequent Rounds**:
   - **Cooperation Threshold**: Calculate the threshold as T = n/k. Cooperate if the number of cooperators in the previous round meets or exceeds T; otherwise, defect.
   - **Punishment Mechanism**: If cooperation falls below T, defect to discourage free-riding. Monitor subsequent rounds; if cooperation recovers, resume cooperating.
3. **Final Round**: Cooperate to uphold communal spirit regardless of previous actions.

### Pseudocode Implementation

```python
def dynamic_cooperativist(n, k, history):
    if not history:  # First round
        return "C"
    else:
        t = len(history)
        prev_coop = sum(actions['cooperate'] for actions in history[t-1].values()) if t > 0 else 0
        threshold = n / k
        if prev_coop >= threshold:
            return "C"
        else:
            return "D"

# Last round handling
if current_round == r:
    return "C"
```

### Explanation

- **Initial Cooperation**: Starting with cooperation fosters a collective benefit from the outset.
- **Adaptive Strategy**: By setting a dynamic threshold based on game parameters, the strategy adapts to maintain cooperation when beneficial and punishes when not.
- ** Forgiving Punishment**: Allows resumption of cooperation after defection if others return to cooperative behavior, promoting long-term group welfare.

This approach ensures a balance between individual and group incentives, encouraging sustained cooperation while being robust against exploitation.
'''

description_COMMUNAL_19 = '''
### Strategy: **Adaptive Cooperate or Defect (ACD)**

**1. Decision Rules:**

- **First Round:** Cooperate (C)
  
- **Middle Rounds (2 to r-1):**  
  Cooperate (C) if the proportion of cooperators in the previous round ≥ k/n.  
  Defect (D) otherwise.

- **Last Round (r):** Cooperate (C) to contribute to the public good.

**2. Handling Edge Cases:**

- **First Round:** Start with cooperation to encourage collective action.
  
- **Middle Rounds:** Adjust behavior based on previous cooperation levels relative to k/n.
  
- **Last Round:** Cooperate regardless of previous behavior to maximize the final round's public good.

**3. Communal Alignment:**

The strategy promotes cooperation as long as a sufficient number of players (threshold k/n) are contributing, fostering collective benefit. It adapts based on others' actions, encouraging a positive social outcome while protecting against exploitation.

**Pseudocode:**

```
function strategy(history):
    if history == empty:
        return COOPERATE
    elif current_round == last_round:
        return COOPERATE
    else:
        previous_coop_rate = number_of_coop_prev / n
        if previous_coop_rate >= k/n:
            return COOPERATE
        else:
            return DEFECT
```

This strategy balances cooperation with adaptability, encouraging communal benefits while protecting against exploitation.
'''

description_COMMUNAL_20 = '''
### Communal Strategy for N-Player Public Goods Game

This strategy, which we'll call **"Reciprocal Cooperation Threshold" (RCT)**, is designed to balance individual self-interest with communal well-being. It is adaptive, robust, and aligns with a communal mindset by rewarding cooperation while protecting against exploitation.

---

#### 1. **Decision Rules**
The strategy uses a simple, adaptive rule based on the history of cooperation in previous rounds. It incorporates reciprocal behavior to encourage cooperation while safeguarding against chronic defection.

- **First Round:**
  - Cooperate (C). This encourages cooperation by setting a positive tone for the game.
  
- **Subsequent Rounds:**
  - Cooperate (C) if the average cooperation rate of other players in the previous round is above a threshold **(k/(2n))**. 
  - Defect (D) otherwise. This threshold ensures that cooperation is only maintained if a sufficient number of other players are also contributing to the public good.

- **Last Round:**
  - Defect (D). Since there are no future rounds to reward cooperation, the strategy prioritizes maximizing immediate payoff.

---

#### 2. **Mathematical Specification**
The strategy can be formalized as follows:

- Let **H_t** denote the history of cooperation up to round **t**.
- Let **c_j,t** = 1 if player **j** cooperated in round **t**, and **c_j,t** = 0 otherwise.
- Let **avg_coop_t** = (Σ_{j=1}^{n} c_j,t) / n denote the fraction of players who cooperated in round **t**.
- Let **threshold** = (k / (2n)).

The decision rule for player **i** in round **t+1** is:
```
if t == 1:
    Cooperate (C)
elif t == r:
    Defect (D)
else:
    if avg_coop_t >= threshold:
        Cooperate (C)
    else:
        Defect (D)
```

---

#### 3. **Rationale**
- **First Round Cooperation:** By starting with cooperation, the strategy sets a cooperative tone and encourages others to reciprocate.
- **Adaptive Threshold:** The threshold **(k/(2n))** ensures that cooperation is maintained only if a sufficient number of players are contributing. This prevents exploitation while allowing for the public good to grow.
- **Last Round Defection:** In the final round, there is no future to reward cooperation, so the strategy prioritizes self-interest by defecting. This avoids the "sucker's payoff" of cooperating when others may defect.

---

#### 4. **Communal Alignment**
This strategy aligns with a communal mindset by:
- Encouraging cooperation as long as others are contributing.
- Rewarding collective effort through reciprocity.
- Protecting the community from exploitation by defecting if cooperation is insufficient.

---

#### 5. **Robustness**
The strategy is robust in several ways:
- It performs well against a wide range of opponent behaviors, including pure cooperators, pure defectors, and mixed strategies.
- It adapts dynamically based on the group's behavior, making it resilient to varying levels of cooperation.
- It balances individual and collective payoffs, ensuring that the player is not systematically exploited.

This strategy is designed to perform well in a tournament setting while maintaining a communal orientation. It avoids complex coordination mechanisms and focuses on simple, reciprocal behavior that is easy to implement and interpret.
'''

description_COMMUNAL_21 = '''
To address the challenge of designing a communal strategy for the N-Player Public Goods Game, we've developed a robust and adaptive approach. This strategy promotes cooperation while being responsive to the actions of other players, ensuring it remains effective across various scenarios.

### Strategy Description: Adaptive Communal Cooperativity

1. **Initial Cooperation**: In the first round, all players Cooperate. This sets a cooperative tone and establishes a baseline for mutual benefit.

2. **Adaptive Decision-Making**: For each subsequent round, the strategy decides whether to Cooperate or Defect based on the number of players who Cooperated in the previous round.
   - **Count Previous Cooperators**: Determine how many players Cooperated in the last round (denoted as \( C_{t-1} \)).
   - **Threshold Check**: If \( C_{t-1} \) meets or exceeds the threshold \( k \), the player Cooperates in the current round. If \( C_{t-1} \) is below \( k \), the player Defects.

3. **Handling All Rounds**: This strategy applies consistently across all rounds, including the final round, ensuring there's no special case treatment that could undermine the communal goal.

### Rationale

- **Promotes Sustained Cooperation**: By Cooperating when enough others do so, the strategy fosters a cooperative environment that maximizes group payoff.
- **Adaptive to Behavior**: The strategy dynamically adjusts based on observed behavior, encouraging continued cooperation or shifting to self-preservation if cooperation falters.
- **Robust and Fair**: It's a balanced approach that doesn't assume others' strategies, making it resilient against exploitation while encouraging pro-social behavior when possible.

### Conclusion

This strategy effectively balances individual and group interests, promoting cooperation while adapting to the dynamics of the game. It ensures that communal benefits are pursued without leaving players vulnerable to exploitation, making it both practical and aligned with a cooperative mindset.
'''

description_COMMUNAL_22 = '''
**Strategy for N-Player Public Goods Game**

**Objective:** Design a communal, adaptive strategy that promotes cooperation while protecting against exploitation.

**Strategy Overview:**
- **Name:** Threshold Cooperative Strategy
- **Approach:** Cooperate if the number of cooperators in the previous round meets or exceeds a threshold based on game parameters.

**Decision Rules:**

1. **First Round:** Always Cooperate (C).
   - *Rationale:* Encourages initial cooperation, fostering a communal start.

2. **Subsequent Rounds:** 
   - Observe the number of cooperators (C_prev) in the previous round.
   - Calculate the threshold as floor(n/k), where floor is the greatest integer less than or equal to n/k.
   - Cooperate (C) if C_prev >= threshold.
   - Defect (D) if C_prev < threshold.

3. **Last Round:** 
   - Apply the same decision rule using the cooperation count from the penultimate round.
   - *Rationale:*Maintains strategy consistency, encouraging sustained cooperation.

**Handling Edge Cases:**
- **First Round:** Starts with cooperation.
- **Last Round:** Uses data from the second last round to decide.
- **Non-Integer Threshold:** Uses floor function to handle cases where n/k isn't an integer.

**Communal Alignment:**
- **Promotes Group Interest:** Incentivizes cooperation when beneficial, collectively maximizing payoffs.
- **Adaptive and Robust:** Adjusts based on group behavior, punishing insufficient cooperation to prevent exploitation.

**Pseudocode:**

```
function strategy(n, k, history) {
    if history is empty {
        return Cooperate
    }
    else {
        previous_action_count = number of Cooperate in history[-1]
        threshold = floor(n / k)
        if previous_action_count >= threshold {
            return Cooperate
        } else {
            return Defect
        }
    }
}
```

**Conclusion:**
This strategy balances individual and communal interests, adapting based on group cooperation levels. It starts cooperatively, continues if enough others do, and defects to avoid being exploited. Its simplicity and reliance on previous round data make it robust for various behaviors, aligning with the communal mindset.
'''

description_COMMUNAL_23 = '''
To design a communal strategy for the N-Player Public Goods Game that encourages cooperation while being adaptive and robust, we can implement the following approach:

### Communal Strategy: "Adaptive Cooperation Based on Historical Contribution"

#### Decision Rules:
1. **First Round**: Cooperate. This initiates the game on a positive note, promoting initial cooperation.
2. **Subsequent Rounds**:
   - Each player calculates the average number of cooperators from all previous rounds.
   - The player Cooperates if the product of this average and the factor k/n is at least 1.
   - If the product is less than 1, the player Defects to avoid being exploited.

#### Edge Case Handling:
- **First Round**: All players Cooperate to establish a baseline for cooperation.
- **Last Round**: The decision is based on the average cooperation up to the penultimate round, ensuring consistency.
- **Low Cooperation Scenario**: If the historical average of cooperators is insufficient, players Defect to protect their individual payoffs.

This strategy promotes a communal mindset by rewarding cooperation when it is sufficiently widespread and adaptively responding to defection by others. It is robust as it adjusts behavior based on observed actions, ensuring individuals do not unjustly sacrifice their payoffs.

### Pseudocode Implementation:
```python
def adaptive_cooperation(n, k, r, history):
    if len(history) == 0:  # First round
        return 'C'
    total_cooperations = sum([len(round) for round in history])
    average_C = total_cooperations / len(history)
    if (k / n) * average_C >= 1:
        return 'C'
    else:
        return 'D'
```

### Explanation:
- **Adaptive**: The strategy adjusts each player's actions based on the group's past behavior, encouraging cooperation when beneficial.
- **Robust**: It avoids exploitation by defecting when cooperation levels are too low.
- **Communal**: It aligns with the goal of maximizing the public good by Cooperation when collective action is sufficiently high.

This approach fosters cooperation while safeguarding against exploitation, making it suitable for a wide range of opponent behaviors in the tournament.
'''

description_COMMUNAL_24 = '''
**Communal Strategy for N-Player Public Goods Game**

**Strategy Name: Adaptive Communal Response (ACR)**

**Objective:** Encourage cooperation by rewarding collective cooperation and penalizing insufficient contribution, fostering a communal mindset.

---

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Reason:** Initiates cooperation, encouraging others to follow suit and establishing a baseline for reciprocal behavior.

2. **Subsequent Rounds (t > 1):**
   - **Threshold Calculation:** Determine the minimum number of cooperators required, calculated as `t = ceiling(n/k)`.
   - **Action:**
     - **Cooperate (C)** if the number of cooperators in the previous round (t-1) is at least `t`.
     - **Defect (D)** if the number of cooperators in the previous round is less than `t`.
   - **Reason:** Cooperate when the collective contribution is sufficient to make cooperation beneficial, otherwise defect to deter free-riding.

**Handling Edge Cases:**

- **First Round:** Always cooperate to initiate a cooperative environment.
- **Last Round:** Decision based on the previous round's cooperation rate, maintaining strategy consistency.

**Communal Alignment:**

- **Reward Cooperation:** Sustains cooperation when collective effort is adequate, reinforcing the community's benefit.
- **Penalize Defection:** Adjusts behavior to defect when cooperation levels are low, signaling the need for higher collective contribution.

**Pseudocode:**

```python
def adaptive_communal_responseParameters(n, k):
    # Compute threshold based on parameters
    t = ceiling(n / k)
    
def strategy(history):
    if not history:  # First round
        return "C"
    else:
        previous_cooperators = history[-1].count("C")
        if previous_cooperators >= t:
            return "C"
        else:
            return "D"
```

**Explanation:**

- **Initialization:** Cooperate in the first round to set a cooperative tone.
- **Adaptive Decision-Making:** Each subsequent round's action is based on the previous round's cooperation rate, ensuring that cooperation is only sustained when beneficial.
- **Robustness:** The strategy adapts to various opponent behaviors, adhering to communal principles without relying on others' strategies.

This approach balances individual and collective interests, promoting a communal mindset through adaptive, cooperative behavior when supported by sufficient group contribution.
'''

description_COMMUNAL_25 = '''
To address the challenge of designing a communal strategy for the N-Player Public Goods Game, we developed a cooperative, adaptive approach that balances encouragement of collective contribution with protection against free-riding. The strategy, named "Sustainable Cooperation," guides players to maximize total payoff by fostering cooperation while maintaining robustness against various behaviors.

### Strategy Overview:

1. **First Round Cooperation:**
   - **Action:** Cooperate (C).
   - **Rationale:** Initializes a cooperative tone, encouraging others to follow suit.

2. **Subsequent Rounds:**
   - **Monitor Cooperation:** Track the average cooperation rate from previous rounds.
   - **Threshold-Based Decision:** If the cooperation rate exceeds 70%, Cooperate; otherwise, Defect to penalize free-riders.

3. **Last Round Handling:**
   - **Assess Overall Cooperation:** Cooperate if the overall cooperation rate has been sufficiently high; otherwise, Defect.

4. **Forgiveness Mechanism:**
   - **Adaptive Restart:** If increased cooperation is detected, revert to Cooperate after a few rounds, promoting renewed collective effort.

This strategy is designed to be adaptive, encouraging cooperation while safeguarding against exploitation, aligning with a communal mindset to achieve mutual benefits.
'''

description_COMMUNAL_26 = '''
**Communal Strategy for N-Player Public Goods Game**

**Strategy Overview:**
The strategy is designed to encourage cooperation while being robust against exploitation. It adapts based on the cooperation rates observed in previous rounds, punishing low cooperation with defection and rewarding high cooperation by continuing to cooperate. It also includes a forgiveness mechanism to allow for the resumption of cooperation.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate.
   - **Reason:** Initiates cooperation to set a positive precedent.

2. **Subsequent Rounds (Rounds 2 to r):**
   - **Assess Previous Cooperation:**
     - Calculate the cooperation rate (c_prev) as the ratio of Cooperators in the previous round to the total number of players (n).
   - **Determine Action:**
     - **If c_prev ≥ Threshold (θ):** Cooperate. (θ could be set at 0.5 or another suitable value based on game dynamics.)
     - **If c_prev < θ:** Defect to penalize low cooperation.
     - **Forgiveness Mechanism:** Every 3 rounds, Cooperate regardless of c_prev to allow others to resume cooperation.

3. **Last Round (Round r):**
   - **Action:** Follow the same rules as other rounds, assessing the cooperation rate from Round r-1.
   - **Reason:** Maintains consistency and adaptability even in the final round.

**Edge Case Handling:**
- **First Round:** Always start with cooperation.
- **Last Round:** Apply the same adaptive rules, ensuring no sudden shifts in behavior that others might exploit.

**Example Implementation Steps:**
1. **Initialize:** Cooperate in the first round.
2. **For Each Subsequent Round:**
   - Calculate c_prev from the previous round.
   - If c_prev ≥ θ, Cooperate.
   - Else, Defect.
   - Each 3rd round, reset to Cooperate to encourage renewed cooperation.

This strategy balances punishment for low cooperation with the willingness to resume cooperation, promoting a communal benefit while protecting against exploitation.
'''

description_COMMUNAL_27 = '''
To address the N-player Public Goods Game, we've designed a strategy that encourages cooperation while being adaptive and robust against defectors. The strategy is based on a threshold of cooperation needed to make the public good beneficial, ensuring that players are rewarded for cooperation and incentivized to maintain it when enough others do so.

### Strategy: Adaptive Cooperative Threshold (ACT)
1. **First Round Action:**
   - **Cooperate:** Start by cooperating to set a positive tone and encourage others to follow suit.

2. **Subsequent Rounds:**
   - **Calculate Threshold (T):** Determine the minimum number of cooperators needed for cooperation to be beneficial. T is calculated as the ceiling of (n/k).
   - **Assess Previous Round:** Count the number of players who cooperated in the previous round (C_prev).
   - **Decision Rule:** 
     - If C_prev ≥ T, **Cooperate** to benefit from the public good.
     - If C_prev < T, **Defect** to avoid being exploited.

### Rationale
- **Incentivizes Cooperation:** By cooperating when enough others do, players maximize their payoffs through the public good.
- **Punishes Defection:** If cooperation drops below the threshold, defecting prevents exploitation.
- **Adaptive and Forgiving:** The strategy allows reversion to cooperation if enough players start cooperating again, maintaining a communal mindset.

This approach ensures a balanced strategy that promotes cooperation while being resilient to varying behaviors, aligning with the goal of maximizing communal payoff.
'''

description_COMMUNAL_28 = '''
To design a communal strategy for the N-Player Public Goods Game that balances cooperation and defection, we introduce an adaptive approach that responds to the level of cooperation in previous rounds. The strategy aims to maximize group payoffs while being robust against various opponent behaviors.

### Strategy: Adaptive Cooperatior

1. **First Round Cooperation**: 
   - Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.

2. **Subsequent Rounds Adaptation**:
   - After the first round, for each round, calculate the number of players who cooperated in the previous round.
   - **Threshold Calculation**: Determine a threshold based on the game parameters, specifically the floor value of \( \frac{n}{k} \). This threshold represents the minimum number of cooperators needed to make cooperation beneficial for the group.
   - **Decision Rule**: Cooperate if the number of cooperators in the previous round meets or exceeds this threshold. Otherwise, defect.

3. **Final Round Cooperation**:
   - In the last round, cooperate regardless of previous actions to maximize the group's total payoff, as there are no future consequences for defection.

### Edge Cases and Considerations:
- **First Round**: Always cooperate to initiate cooperation.
- **Last Round**: Always cooperate to ensure the group's final round is as beneficial as possible.
- **Adaptation Mechanism**: Uses the threshold to decide whether to continue cooperating or switch to defection, ensuring the strategy is responsive to others' actions.

### Pseudocode Implementation:

```python
def adaptive_cooperatior(n, k, r, history):
    # Initialize to cooperate in the first round
    if not history:
        return "C"
    
    # For subsequent rounds until the last
    if len(history) < r - 1:
        # Calculate threshold as floor(n/k)
        threshold = n // k
        # Count number of cooperators in the previous round
        previous_cooperators = sum(1 for action in history[-1] if action == "C")
        if previous_cooperators >= threshold:
            return "C"
        else:
            return "D"
    
    # Last round: always cooperate
    return "C"
```

### Alignment with Communal Mindset:
This strategy prioritizes group success by encouraging cooperation when sufficient others are cooperating, thereby fostering a collaborative environment. It adapts to the group's behavior, balancing individual and collective interests to maximize overall well-being.
'''

description_COMMUNAL_29 = '''
### Communal Strategy for N-Player Public Goods Game

#### StrategyOverview:
The strategy, **"Reciprocal Cooperativeness" (RC+)**, is designed to balance individual payoffs with communal well-being through adaptive cooperation. It encourages contribution to the public good while maintaining robustness against exploitation. The strategy uses a **threshold-based mechanism** to reciprocate cooperation proportionally, aiming to balance cooperation with the need to avoid being exploited.

---

### 1. Decision Rules

**Primary Logic:**
- **Cooperate (C)** if the average cooperation rate of other players in the previous round is above a threshold.
- **Defect (D)** otherwise.
- **Adaptive Threshold:** Adjust the cooperation threshold dynamically based on past success.

**Detailed Rules:**

#### a. First Round:
- Cooperate unconditionally to set a cooperative tone for the game.
   - Rationale: Early cooperation signals a willingness to contribute, encouraging others to reciprocate.

#### b. Subsequent Rounds:
- Let **C_prev** be the number of players (including yourself) who Cooperated in the previous round.
- Let **T** be an adaptive threshold:
   - If in the previous round, the payoff π_i was higher than the average of all previous payoffs, set **T = max(0, T - 1)**.
   - If π_i was lower, set **T = min(n, T + 1)**.
- Cooperate (C) if **C_prev ≥ T**.
- Defect (D) otherwise.
   - **Rationale:** Gradually adjust the threshold based on the success of cooperation. If cooperation is "successful" (as measured by higher payoffs), lower the threshold to encourage more cooperation. If cooperation is "unsuccessful," raise the threshold to protect against exploitation.

---

### 2. Edge Cases

#### a. First Round:
- Always Cooperate (C).
   - Rationale: Establish a cooperative baseline to encourage others to follow suit.

#### b. Last Round:
- Use the same adaptive threshold as in other rounds, but with an additional defect mechanism:
   - Defect (D) if the total contributions in the previous round were below the threshold **T**, or if the game is in its final round and the average cooperation rate in the penultimate round was below T.
   - Rationale: Protect against end-game exploitation while maintaining consistency.

#### c. Low Cooperation Environments:
- If fewer than or equal to **T** players Cooperated in the previous round, Defect (D).
   - Rationale: Avoid repeatedly contributing to a public good when others are not reciprocating.

---

### 3. Communal Alignment

#### a. Cooperativeness:
- The strategy is designed to align with the communal mindset by initially Cooperating and maintaining cooperation as long as others reciprocate.
   - Rationale: Foster trust and collective success while avoiding exploitation.

#### b. Fairness and Reciprocity:
- The adaptive threshold ensures proportional reciprocity, rewarding cooperation with more cooperation and punishing defection by reducing cooperation.
   - Rationale: Enforce fairness by scaling contributions based on others' behavior.

---

### Pseudocode

```python
def reciprocal_cooperativeness(n, r, k, history):
    if not history:  # First round
        return "C"
    
    # Initialize variables
    cooperation_threshold = n // 2  # Start with a moderate threshold
    cooperation_rates = []
    
    # Previous round's cooperation count
    c_prev = sum(1 for actions in history[-1] if actions == "C")
    
    # Calculate average payoff for previous round
    avg_payoff = sum([history_payoff[-1] for history_payoff in history]) / n
    
    # Adjust threshold based on payoff
    if avg_payoff > sum([history_payoff[i] for i in range(len(history)-1)]) / len(history):
        cooperation_threshold = max(0, cooperation_threshold - 1)
    else:
        cooperation_threshold = min(n, cooperation_threshold + 1)
    
    # Decide action
    if c_prev >= cooperation_threshold:
        return "C"
    else:
        return "D"
```

---

### Explanation

- **Adaptiveness:** The **RC+** strategy is robust to a variety of opponent behaviors because it dynamically adjusts the cooperation threshold based on the success of past cooperation (as measured by payoffs). This allows it to adapt to both cooperative and exploitative environments.
- **Edge Case Handling:** The strategy includes specific rules for the first and last rounds, ensuring consistency and protecting against exploitation in critical rounds.
- **Communal Alignment:** By initially Cooperating and maintaining cooperation as long as others reciprocate proportionally, the strategy aligns with the communal mindset and encourages collective success while protecting against exploitation.

This strategy is designed to perform well in a tournament setting by balancing cooperation with self-protection, ensuring robustness across a wide range of opponent behaviors.
'''

description_COMMUNAL_30 = '''
**Strategy Design: Communal Reciprocity with Forgiveness**

**Overview:**
This strategy promotes cooperation by reciprocating the group's behavior, punishing defection while being forgiving to reinitiate cooperation. It's designed to be adaptive and communal, encouraging high payoffs for the group.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Sets a positive tone and encourages initial cooperation.

2. **Subsequent Rounds:**
   - **Assessment:** After each round, calculate the cooperation rate (number of cooperators divided by n).
   - **Threshold:** 50% cooperation rate.
   - **Actions:**
     - If cooperation rate ≥ 50%, cooperate in the next round.
     - If cooperation rate < 50%, defect in the next round as a punishment.

3. **Forgiveness Mechanism:**
   - After defecting once due to low cooperation, resume cooperation in the subsequent round if the cooperation rate meets or exceeds the threshold.

**Edge Case Handling:**
- **Last Round:** Follow the same rules as other rounds. Cooperate if the previous round's cooperation was ≥50%.
- **Low Cooperation Situations:** The strategy defects to punishment when cooperation is below the threshold but quickly forgives if cooperation resumes.

**Pseudocode:**

```
def strategy(n, r, k, history):
    if len(history) == 0:  # First round
        return "C"
    else:
        last_round = history[-1]
        cooperation_rate = sum(last_round["actions"].count("C") for all players) / n
        if cooperation_rate >= 0.5:
            return "C"
        else:
            return "D"

# Forgiveness is applied in the next round after defecting
# If the previous round's cooperation rate after defecting meets the threshold, switch back to C
```

**Communal Alignment:**
This strategy aligns with the communal mindset by prioritizing group payoff through reciprocity and forgiveness, fostering a balance between encouraging cooperation and addressing defection.
'''

description_COMMUNAL_31 = '''
To design an effective communal strategy for the N-Player Public Goods Game, the approach focuses on encouraging cooperation while being adaptive to others' actions. Here's the structured strategy:

### Strategy: Adaptive Cooperator with Forgiveness

1. **First Round Action:**
   - **Cooperate**: Start by Cooperating to establish a cooperative tone and encourage others to follow suit.

2. **Subsequent Rounds (2 to r-1):**
   - **Cooperate Threshold**: In each round after the first, Cooperate if the number of Cooperators in the previous round is at least `n/k`. This threshold ensures that the public good's return is sufficiently beneficial to justify the contribution.
   - **Defect if Threshold Not Met**: If the previous round's Cooperators are below `n/k`, Defect to discourage free-riding and incentivize others to Cooperate.

3. **Last Round Action:**
   - **Cooperate**: In the final round, Cooperate regardless of previous actions to maximize the collective payoff, as there are no future consequences.

This strategy is designed to be adaptive and robust, promoting cooperation while penalizing defection to maintain a balance that benefits the community. It aligns with a communal mindset by aiming to maximize the total payoff collectively, even in the presence of potential defectors.

**Pseudocode Summary:**

```
function strategy(previous_c, current_round, total_rounds):
    if current_round == 1:
        return "Cooperate"
    elif previous_c >= n / k:
        return "Cooperate"
    elif current_round == total_rounds:
        return "Cooperate"
    else:
        return "Defect"
```

This approach ensures the strategy is both communal and adaptive, fostering cooperation while being resilient to varying behaviors from other players.
'''

description_COMMUNAL_32 = '''
To address the challenge of designing a communal strategy for the N-Player Public Goods Game, we propose a dynamic and adaptive approach that encourages cooperation while being responsive to the group's behavior. The strategy is designed to be simple yet effective, ensuring robustness across various opponent behaviors.

### Strategy: Adaptive Cooperation Based on Public Good Value

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate.
   - **Rationale:** Set a cooperative tone to encourage others to follow suit and build a foundation for future cooperation.

2. **Subsequent Rounds (2 to r-1):**
   - **Action:**
     - Calculate the number of cooperators in the previous round (C_prev).
     - Compute the public good value per player: (k/n) * C_prev.
     - If (k/n) * C_prev ≥ 1, Cooperate in the current round.
     - If (k/n) * C_prev < 1, Defect in the current round.
   - **Rationale:** Cooperate if the public good from the previous round provided at least as much value as the private payoff (1). This incentivizes continued cooperation when beneficial and adapts based on the group's contribution.

3. **Last Round (r):**
   - **Action:**
     - Use the same rule as in other rounds.
     - Calculate C_prev from round r-1.
     - If (k/n) * C_prev ≥ 1, Cooperate; otherwise, Defect.
   - **Rationale:** Maintain consistency even in the last round, aligning with the communal mindset. This approach discourages exploitation by others who might consider defecting in the final round.

**Edge Cases:**

- **First Round:** Always Cooperate to establish cooperation.
- **Last Round:** Treat it similarly to other rounds based on previous cooperation levels to maintain group norms.

**Implementation:**

This strategy is implemented by each player observing the previous round's cooperation level and deciding their action based on the calculated public good value. It balances individual incentive with communal benefit, promoting sustained cooperation when it is mutually advantageous.

**Pseudocode Example:**

```
def strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return "Cooperate"
    else:
        prev_coop = sum(1 for action in history[-1] if action == "Cooperate")
        public_good = (k / n) * prev_coop
        if public_good >= 1:
            return "Cooperate"
        else:
            return "Defect"
```

This approach ensures that each player's decision is based on the collective action of the group, fostering a cooperative environment while remaining responsive and robust against various strategies.
'''

description_EXPLOITATIVE_1 = '''
The optimal exploitative strategy for the N-Player Public Goods Game is to always defect (D) in every round. This approach maximizes individual payoff regardless of others' actions, as defecting yields a higher or equal payoff compared to cooperating in all scenarios under the given parameters.

**Strategy: Always Defect (D)**

**Answer:**

1. **Decision Rule**: Always choose to Defect (D) in every round, regardless of the number of rounds remaining or the history of others' actions.

2. **Edge Cases**: Defect in the first round, last round, and every round in between. The strategy remains unchanged throughout the game.

3. **Exploitative Focus**: By defecting consistently, the strategy ensures maximum individual payoff, capitalizing on others' cooperation without contributing to the public good, aligning with an exploitative mindset.

The strategy is implemented as:

```
for each round in 1 to r:
    choose action D (Defect)
```
'''

description_EXPLOITATIVE_2 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we create a decision-making process that leverages the game's parameters and history to maximize individual payoffs, taking advantage of others' behavior without assuming cooperation.

### Strategy: Exploitative Threshold Cooperator

#### 1. Decision Rules:
- **First Round**: Defect (play D) as there is no prior information.
- **Subsequent Rounds**: Observe the average cooperation rate from the previous round. If this rate is above a threshold (k/n), Cooperate (C); otherwise, Defect (D).
- **Last Round**: Always Defect, since there are no future consequences.

**Pseudocode:**
```
n = number of players
k = multiplication factor
r = number of rounds

threshold = k / n

for each round from 1 to r:
    if round == 1:
        play D
    else if round == r:
        play D
    else:
        avg_c = average cooperation rate in previous round
        if avg_c >= threshold:
            play C
        else:
            play D
```

#### 2. Handling Edge Cases:
- **First Round**: Defect to establish a baseline and avoid contributing without knowing others' strategies.
- **Last Round**: Defect as there are no future interactions to influence.
- **Adaptation**: Uses the previous round's cooperation rate to decide current action, fostering responsiveness to changing dynamics.

#### 3. Exploitative Nature:
The strategy maximizes individual payoffs by defecting when others are not contributing sufficiently, thus exploiting the public good while minimizing personal contributions. It also cooperates when others' high contributions make it beneficial, encouraging continued higher public goods which can be exploited in subsequent rounds.

This approach ensures the strategy is adaptive, leveraging historical data without assuming others' cooperation, making it robust against varied behaviors.
'''

description_EXPLOITATIVE_3 = '''
To design an exploitative strategy for the N-player public goods game, we focus on maximizing individual payoff by adaptively responding to other players' actions. The strategy balances encouraging cooperation to enhance collective payoff while defecting when others do not contribute sufficiently. Here's the structured approach:

1. **First Round**: Cooperate to set a cooperative tone and encourage others to contribute.

2. **Subsequent Rounds (2 to r-1)**:
   - Observe the previous round's cooperation rate.
   - If the average cooperation rate surpasses the threshold \( \frac{k}{n} \), cooperate; otherwise, defect.

3. **Last Round (r)**: Defect, as there are no future interactions to influence, making cooperation individually unfavorable.

This strategy is adaptive, robust, and exploitative, ensuring optimal payoffs based on observed behavior.

**Pseudocode**:

```
def strategy(n, k, r, history):
    current_round = len(history) + 1  # Assuming history is a list of past actions
    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        prev_coop = sum(history[-1])  # Count of cooperators in last round
        avg_coop = prev_coop / n
        if avg_coop > k / n:
            return "C"
        else:
            return "D"
```

This approach ensures the strategy is clear, handles all edge cases, and adapts effectively to others' behaviors.
'''

description_EXPLOITATIVE_4 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we focus on maximizing individual payoff by leveraging the actions of others while safeguarding against exploitation. The strategy adapts based on the game's history and parameters, ensuring robustness across various opponent behaviors.

### Strategy: Conditional Cooperation Based on k-Threshold

1. **First Round Action**: Cooperate (C)
   - **Rationale**: Initiates potential cooperation, encouraging others and observing their responses.

2. **Subsequent Rounds**:
   - **Action Determination**: 
     - **First Step**: Count the number of players who Cooperated in the previous round, denoted as `C_prev`.
     - **Second Step**: Compare `C_prev` against the threshold `k` (the multiplication factor provided as a parameter).
     - **Decision Rule**: 
       - If `C_prev >= k`, Cooperate (C) in the current round.
       - If `C_prev < k`, Defect (D) to capitalize on existing contributions without sacrificing personal gain.

### Edge Case Handling:
- **First Round**: Always Cooperate to set a cooperative tone and gauge others' willingness to contribute.
- **Last Round**: Continue using the same strategy since the decision logic remains consistent throughout the game, without special treatment for the final round.

### Exploitative Mindset:
This strategy prioritizes individual payoff maximization by:
- **Encouraging Cooperation**: Cooperating when others do, enhancing collective gain.
- **Exploiting Defection**: Defecting when cooperation is insufficient, preventing personal loss while benefiting from others' contributions.

### Pseudocode Illustration:

```python
def strategy(n, k, history):
    if not history:  # First round
        return 'C'
    else:
        c_prev = history[-1]['cooperators']
        if c_prev >= k:
            return 'C'
        else:
            return 'D'
```

### Summary:
"Conditional Cooperation Based on k-Threshold" is an adaptive, robust strategy that starts cooperatively, then dynamically adjusts based on prior round cooperation levels. It ensures that each decision maximizes individual payoff by exploiting others' contributions while maintaining the potential for collective benefit.
'''

description_EXPLOITATIVE_5 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we focus on maximizing individual payoff by adapting to others' behavior while encouraging cooperation when beneficial. Here's the structured approach:

### Strategy: Adaptive Exploitation Based on Average Contributions

1. **First Round: Cooperate**  
   - Start by Cooperating to encourage initial cooperation and observe others' reactions.

2. **Middle Rounds (2 to r-1): Adapt Based on Average Contributions**  
   - Calculate the average total contributions (avg_total_C) from all players in previous rounds.
   - If (k/n) * avg_total_C > 1, Cooperate. This means the public good benefit exceeds the cost of contribution.
   - If (k/n) * avg_total_C ≤ 1, Defect to maximize individual payoff.

3. **Last Round: Defect**  
   - In the final round, Defect as there’s no future interaction to influence, maximizing immediate payoff.

This strategy is robust as it adapts to others' cooperation levels, exploiting their contributions while fostering cooperation when advantageous. It doesn’t rely on coordination, making it suitable for competitive environments.
'''

description_EXPLOITATIVE_6 = '''
**Strategy for N-Player Public Goods Game**

---

**Strategy Name:** Adaptive Cooperative Maximization (ACM)

---

**Objective:**  
To maximize individual payoff by leveraging cooperation when beneficial and defecting when exploited, while maintaining adaptability and robustness against diverse strategies.

---

**Core Strategy:**

1. **First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Initiate cooperation to encourage a collaborative environment and observe others' responses.

2. **Subsequent Rounds:**
   - **Action Determination:**
     1. **Calculate Previous Cooperation Rate:**
        - Compute the average cooperation rate of all players in the previous round. This is done by counting the number of cooperators and dividing by the total number of players.

     2. **Threshold Comparison:**
        - **Threshold:** Set as k/n, representing the minimum expected return per player when all contribute.
        - If the previous round's cooperation rate exceeds this threshold, choose to Cooperate (C).
        - If it is below, defect (D) to avoid being exploited.

     3. **Forgiveness Mechanism:**
        - After defecting, monitor the subsequent rounds. If a significant increase in cooperation is observed (e.g., exceeding the threshold), revert to cooperating. This allows re-engagement if others start contributing again.

3. **Last Round:**
   - **Action:**
     - If the合作 rate trend in the final few rounds is positive (increasing), Cooperate (C) to maximize total payoff.
     - Otherwise, Defect (D) to avoid a potential sucker payoff.

---

**Edge Cases and Special Considerations:**
- **All Players Defecting Consistently:** If a zero cooperation trend persists, continue defecting to prevent being exploited.
- **Isolated Defection Episodes:** Apply the forgiveness mechanism to allow cooperation to resume if others start contributing again.

---

**Pseudocode Example:**

```
Initialize:
    cooperation_threshold = k / n

For each round from 1 to r:
    if round == 1:
        action = C
    else:
        previous_cooperation_rate = total_c_prev / n
        if previous_cooperation_rate > cooperation_threshold:
            current_action = C
        else:
            current_action = D
            # Forgiveness check:
            if last_round_action == D:
                check if recent rounds show increased cooperation
                if yes:
                    current_action = C
    if round == r:
        if trend in last few rounds is positive:
            action = C
    execute action and record payoff
```

---

**Expected Outcome:**  
This strategy should balance maximizing personal gain with supporting the public good, adapting dynamically to others' behavior, and avoiding exploitation through timely defection. It encourages cooperation when beneficial and adjusts based on observed behavior, ensuring robust performance across various opponent strategies.
'''

description_EXPLOITATIVE_7 = '''
To address the challenge, we developed an exploitative strategy that focuses on maximizing individual payoffs by taking advantage of others' cooperative behavior while minimizing personal contributions. The strategy is straightforward and adaptive, ensuring optimal play against a variety of opponent behaviors.

---

**Strategy: "Exploitative Defection"**

1. **Decision Rules:**
   - **Action Choice:** Always choose to Defect (D) in every round. This decision is based on the individual rationality that defecting yields a higher immediate payoff, irrespective of others' actions.

2. **Handling Edge Cases:**
   - **First Round:** Defect. There is no benefit in cooperating when there's no prior information, as the immediate payoff from defecting is higher.
   - **Last Round:** Defect. Since there are no future consequences, the optimal choice is to maximize immediate payoff.

3. **Exploitative Approach:**
   - By consistently defecting, the strategy exploits the cooperative behavior of others. If others cooperate, the strategy benefits from the public good without contributing. If others defect, it avoids the personal loss from cooperation.

This approach ensures robustness and maximizes individual payoffs in a competitive environment.
'''

description_EXPLOITATIVE_8 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we need a systematic approach that adapts to the opponents' actions while maximizing individual payoffs. The strategy should encourage cooperation when beneficial and defect when exploitation is advantageous.

### Strategy: Adaptive Exploitation Based on Contribution Threshold

#### Decision Rules:
1. **First Round**: Cooperate to initiate potential cooperation.
2. **Intermediate Rounds**: 
   - Calculate the threshold number of cooperators (`c_threshold = floor((n - k) / k) + 1`).
   - Cooperate if the number of cooperators in the previous round meets or exceeds this threshold.
   - Otherwise, defect to exploit others' contributions.
3. **Last Round**: Always defect, as there's no future punishment to fear.

This strategy is exploitative because it maximizes individual gain by defecting when others aren't contributing sufficiently, while maintaining cooperation when it benefits the player. It's robust as it adapts based on observable behavior, using a threshold derived from game parameters to guide decisions.

### Pseudocode:

```python
def strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    elif current_round == r:  # Last round
        return 'D'
    else:
        c_prev = number_of_cooperators(history[-1])
        c_threshold = (n - k) // k + 1
        if c_prev >= c_threshold:
            return 'C'
        else:
            return 'D'
```

### Explanation:
- **First Round**: Cooperate to encourage initial cooperation.
- **Subsequent Rounds**: Use the threshold to decide whether to cooperate or defect, ensuring the strategy adapts to the game's dynamics.
- **Last Round**: Defect to maximize immediate payoff, as future consequences are irrelevant.

This approach ensures the strategy remains adaptive and aligned with an exploitative mindset, optimizing personal gain while considering others' past actions.
'''

description_EXPLOITATIVE_9 = '''
**Strategy: Gradual Eigil**

**Overview:**
Gradual Eigil is a dynamic strategy designed for the N-Player Public Goods Game, balancing cooperation and exploitation by adapting to the behavior of other players. It begins cooperatively, gradually adjusts based on the proportion of cooperators, and defects in the final round to maximize payoff.

**Components:**

1. **Initial Cooperation:**
   - **Action:** Cooperate (C) in the first round to encourage mutual cooperation and maximize the group's initial payoff.

2. **Gradual Threshold Adjustment:**
   - **Mechanism:** After each round, adjust the cooperation threshold based on the proportion of players who cooperated in the previous round.
   - **Calculation:** Set the threshold for round `t+1` as `1 - (number of cooperators in round t)/n`.
   - **Adaptation:** If the number of cooperators in round `t` meets or exceeds the threshold, cooperate in round `t+1`; otherwise, defect. This allows the strategy to become more lenient if cooperation is high, encouraging continued cooperation.

3. **Last Round Defection:**
   - **Action:** Defect (D) in the final round to maximize personal payoff, as there are no future consequences.

**Edge Cases:**
- **First Round:** Start with cooperation to set a positive tone.
- **Last Round:** Defect to maximize immediate payoff without repercussions.

**Exploitative Approach:**
The strategy is exploitative as it takes advantage of others' cooperation by sometimes defecting while they cooperate. It incentivizes cooperation by starting with C and adapting based on others' actions, balancing reciprocity with self-interest.

**Conclusion:**
Gradual Eigil is a balanced and adaptive strategy that encourages cooperation while exploiting others' behavior, making it robust against various opponent strategies.
'''

description_EXPLOITATIVE_10 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we need a decision rule that adapts based on the number of cooperators in previous rounds, ensuring we maximize our payoff while being robust against various opponent behaviors.

### Strategy: "Exploitative Cooperator"

1. **First Round:** Cooperate. This initial cooperation sets a positive tone and maximizes the public good, encouraging others to cooperate.

2. **Middle Rounds (2 to r-1):** After the first round, Cooperate in round `t` if the number of cooperators in the previous round `t-1` (`m_{t-1}`) is greater than `n/k`. This threshold ensures that cooperation is only undertaken when it's profitable. If `m_{t-1}` is less than or equal to `n/k`, Defect to avoid being exploited.

3. **Last Round (r):** Always Defect in the final round. Since there are no future rounds, the primary goal is to maximize immediate payoff without regard for future reciprocity.

### Pseudocode:

```
Initialize m_prev as the number of cooperators in the previous round.

For each round from 1 to r:
    If current round == 1:
        Cooperate
    Else if current round == r:
        Defect
    Else:
        If m_prev > (n / k):
            Cooperate
        Else:
            Defect

Update m_prev for the next round based on the number of cooperators observed.
```

This strategy effectively balances cooperation and defection, exploiting others' cooperative tendencies while minimizing losses when others defect. It adapts dynamically based on observed behavior, making it robust and exploitative in a competitive environment.
'''

description_EXPLOITATIVE_11 = '''
To design an exploitative strategy for the N-player Public Goods Game, we need to balance exploiting others' cooperation while avoiding being exploited. The strategy should adapt based on the game's history and parameters.

### Strategy Overview:
1. **First Round**: Cooperate to encourage reciprocation and observe others' behavior.
2. **Subsequent Rounds**:
   - Calculate the average cooperation rate from the previous round.
   - If the cooperation rate exceeds a threshold (AT), cooperate; otherwise, defect.
   - **Threshold Calculation (AT)**: AT = (n / (k + n)) * 100. This threshold adjusts based on the number of players and the multiplication factor.
3. **Last Round**: Always defect to maximize individual payoff, as future consequences are absent.

### Rationale:
- **First Round Cooperation**:.Tests others' strategies and encourages potential reciprocation.
- **Adaptive Threshold (AT)**: Encourages cooperation when sufficient others are cooperating, ensuring the public good's value justifies the contribution.
- **Last Round Defection**: Maximizes individual gain without fear of future punishments, leveraging the endgame scenario.

This strategy effectively balances exploitation with cooperation, ensuring robustness across varying opponent behaviors.

**Pseudocode Example**:

```
function strategy(n, k, r, history):
    if current_round == 1:
        return COOPERATE
    else:
        previous_cooperators = count_cooperators(history[-1])
        avg_cooperation = (previous_cooperators / n) * 100
        AT = (n / (k + n)) * 100
        if current_round == r:
            return DEFECT
        else if avg_cooperation >= AT:
            return COOPERATE
        else:
            return DEFECT
```

This approach ensures the strategy is both exploitative and adaptive, responding effectively to others' actions while maximizing personal payoff.
'''

description_EXPLOITATIVE_12 = '''
### Exploitative Strategy for N-Player Public Goods Game

#### Strategy Overview:
This strategy is designed to maximize individual payoff by exploiting the behaviors of other players while maintaining adaptability to the evolving dynamics of the game.

#### Decision Rules:

1. **First Round:**
   - **Action:** Cooperate (C)
     - **Rationale:** Start with cooperation to establish a baseline of trust and encourage others to reciprocate in subsequent rounds.

2. **Subsequent Rounds (2 to r-1):**
   - **Assessment:** Calculate the number of cooperating players (Cₜ₋₁) in the previous round.
   - **Action:**
     - If Cₜ₋₁ ≥ δ (a dynamic threshold based on the average cooperation rate), Cooperate (C)
     - Else, Defect (D)
     - **Rationale:** Cooperate if the number of cooperators meets or exceeds the threshold, otherwise defect to exploit others' cooperation.

3. **Last Round (r):**
   - **Action:** Defect (D)
     - **Rationale:** In the final round, defect to maximize immediate payoff as there are no future consequences.

#### Handling Edge Cases:
- **First Round:** Cooperate to set a cooperative tone.
- **Last Round:** Defect to maximize immediate payoff.
- **Dynamic Threshold (δ):** Adjust based on the average cooperation rate observed so far to maintain robustness.

#### ExploitativeMindset:
- The strategy is designed to exploit the cooperation of others by defecting when cooperation is insufficient.
- It adapts based on observed behavior, penalizing non-cooperation while rewarding sufficient cooperation.

#### Pseudocode:

```
Initialize:
    total_cooperations = 0
    for each round t from 1 to r:
        if t == 1:
            action = C
        else:
            calculate delta based on average cooperation rate
            if number of cooperators in previous round >= delta:
                action = C
            else:
                action = D
            if t == r:
                action = D
        observe others' actions and payoffs
        update total_cooperations
        calculate delta dynamically
```

This strategy effectively balances cooperation and exploitation, ensuring a robust approach to maximizing individual payoff.
'''

description_EXPLOITATIVE_13 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we'll focus on maximizing individual payoff by leveraging others' cooperation while minimizing losses when others defect. The strategy adapts based on the game's history and parameters, ensuring robustness across various scenarios.

### Strategy: Exploitative Public Goods Strategy

1. **Decision Rules:**
   - **First Round**: Cooperate to encourage initial cooperation among players.
   - **Subsequent Rounds** (2 to r-1):
     - Calculate the threshold as `ceil(n/k)`.
     - Cooperate if the number of cooperators in the previous round meets or exceeds this threshold.
     - Defect otherwise.
   - **Last Round (r)**: Defect to maximize immediate payoff without future consequences.

2. **Handling Edge Cases:**
   - **First Round**: Cooperate to set a cooperative tone.
   - **Last Round**: Always defect to secure maximum immediate gain.
   - **Punishment Mechanism**: If previous cooperation was insufficient, defect to punish and discourage future defection.
   - **Forgiveness**: If cooperation levels increase, revert to cooperation.

3. **Exploitative Approach:**
   - The strategy exploits others' cooperation by defecting when it yields higher payoffs, while encouraging sustained cooperation through selective contributions.

**Pseudocode Example:**

```python
def exploitative_strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    # Calculate threshold
    threshold = math.ceil(n / k)
    prev_round = history[-1]
    count_coop = sum(1 for action in prev_round if action == 'C')
    # Determine action for current round
    if count_coop >= threshold and len(history) < r - 1:
        return 'C'
    else:
        return 'D'
```

This strategy ensures adaptability by responding to prior cooperation levels, making it robust against varying opponent behaviors while maximizing individual payoffs.
'''

description_EXPLOITATIVE_14 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we focus on maximizing individual payoffs by taking advantage of others' cooperation, leveraging the fact that defecting always yields a higher payoff than cooperating, regardless of others' actions. Here's how the strategy is structured:

### Strategy: Always Defect

**1. Decision Rules:**
- **Cooperate (C) or Defect (D):** The strategy is to always choose to Defect in every round. This decision is based on the consistent higher payoff from defecting compared to cooperating, regardless of the number of other cooperators.

**2. Handling Edge Cases:**
- **First Round:** Defect. There's no prior information, but defecting is optimal.
- **Last Round:** Defect. The same logic applies; defecting provides the highest individual payoff.

**3. Exploitative Approach:**
- The strategy doesn't rely on others' cooperation or any assumed norms. It maximizes individual gain by consistently choosing the action that offers the best payoff, knowing that defecting is always more beneficial regardless of others' choices.

### Summary:
The optimal exploitative strategy is to defect in every round. This approach ensures maximum individual payoff by exploiting the tendency of others to cooperate, adhering to the game's parameters without assuming cooperation from others.

### Pseudocode (for Implementation):
```python
def exploitative_strategy(game_parameters, history):
    # game_parameters includes n, r, k
    # history contains previous actions of all players
    
    # Always choose to Defect
    return "D"
```

This strategy is straightforward yet effective, ensuring the player maximizes their payoff by consistently choosing the individually optimal action.
'''

description_EXPLOITATIVE_15 = '''
### Exploitative Strategy for N-Player Public Goods Game

This strategy, named **Adaptive Exploiter (AE)**, is designed to maximize individual payoff while adapting to the behavior of other players. It uses a combination of cooperation and defection, with a clear focus on exploiting the contributions of others while minimizing losses when others defect. The strategy is based on observed history and game parameters, making it robust to varying opponent behaviors.

---

### 1. Decision Rules

The strategy consists of three main phases: **Initial Cooperation**, **Adaptive Play**, and **Final Round Defection**. It also includes a **Forgiveness Mechanism** to sustain cooperation when beneficial.

#### a. First Round
- Cooperate (C) in the first round to establish a cooperative baseline and observe others' responses.
- This initial cooperation is-risk, as it allows the strategy to gather information about other players' tendencies.

#### b. Adaptive Play (Rounds 2 to r-1)
1. **Cooperation Threshold**: Calculate the proportion of players who cooperated in the previous round, denoted as \( p_{\text{cooperate}} \).
   - Example: If 4 out of 6 players cooperated, \( p_{\text{cooperate}} = 4/6 = 2/3 \).

2. **Cooperate or Defect**:
   - If \( p_{\text{cooperate}} > k/n \), cooperate (C). This threshold ensures that the potential public good benefit outweighs the private incentive to defect.
   - If \( p_{\text{cooperate}} \leq k/n \), defect (D). Defecting is optimal when the expected public good benefit is insufficient to justify cooperation.

#### c. Forgiveness Mechanism
- If fewer than \( k/n \) players cooperated in the previous round, the strategy will occasionally cooperate (with probability \( p_{\text{forgive}} = 0.2 \)) to test whether others are willing to return to cooperation. This prevents the strategy from getting stuck in perpetual defection.

#### d. Last Round
- Always defect (D) in the final round. Since there are no future rounds to incentivize cooperation, the best response is to maximize immediate payoff.

---

### 2. Edge Cases

1. **First Round**: Start with cooperation to avoid immediate conflict and gather information.
2. **Last Round**: Defect to maximize immediate payoff, as there are no future interactions to maintain cooperation.
3. **All-or-Nothing Scenarios**:
   - If all players cooperated in the previous round, continue cooperating to maximize public good benefits.
   - If all players defected in the previous round, defect again to avoid being exploited.

---

### 3. Exploitative Mindset

The strategy is designed to exploit the cooperation of others while minimizing risks:
- By cooperating when others cooperate, the strategy maximizes the public good benefit.
- By defecting when others defect or contribute insufficiently, the strategy avoids being exploited.
- The forgiveness mechanism allows the strategy to occasionally test for renewed cooperation, preventing it from becoming overly hostile.

---

### 4. Pseudocode

```python
def adaptive_exploiterParameters:
    n: number of players
    k: multiplication factor
    r: number of rounds
    history: list of previous rounds' cooperation rates

strategy:
    for round t in 1 to r:
        if t == 1:
            action = C  # Cooperate in the first round
        elif t == r:
            action = D  # Defect in the final round
        else:
            p_cooperate = number of cooperators in previous round / n
            if p_cooperate > k/n:
                action = C  # Cooperate if cooperation rate exceeds threshold
            else:
                action = D  # Defect if cooperation rate is insufficient

            # Forgiveness mechanism
            if p_cooperate < k/n and random(0,1) < 0.2:
                action = C  # Occasionally cooperate to test others

    return action
```

---

This strategy ensures robustness and adaptability while maintaining an exploitative mindset. It maximizes the player's payoff by leveraging the contributions of others while protecting against exploitation.
'''

description_EXPLOITATIVE_16 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we focus on maximizing individual payoffs by taking advantage of others' contributions. The strategy should adapt based on observed behavior without relying on coordination or communication.

### Strategy: "Exploit When Possible" (EWP)

1. **Decision Rules:**
   - **Cooperate** if the expected payoff from cooperation exceeds that from defection.
   - **Defect** otherwise, to capitalize on others' contributions.

   In practice, defect when others' cooperation sufficiently enhances the public good, making free-riding beneficial. Cooperate if the public good's share is insufficient to make defecting advantageous.

2. **Handling Edge Cases:**
   - **First Round:** Cooperate to encourage initial contributions.
   - **Last Round:** Defect to maximize payoff since future consequences are absent.

3. **Exploitative Mindset:**
   - Continuously monitor others' behavior.
   - Defect when beneficial, even if others cooperate.
   - Cooperate only when it leads to higher individual gain.

### Pseudocode Example

```python
def exploitative_strategy(history):
    if not history:  # First round
        return 'C'
    # Calculate average cooperation rate from history
    total_coop = sum([h['cooperators'] for h in history])
    avg_coop = total_coop / (len(history) * n)
    # Determine if defecting is more beneficial
    if avg_coop > threshold:  # Threshold based on k and n
        return 'D'
    else:
        return 'C'
```

This strategy ensures the player maximizes their payoff by exploiting others' cooperation while maintaining flexibility to adapt based on observed behavior.
'''

description_EXPLOITATIVE_17 = '''
**Strategy: Adaptive Exploitation in N-Player Public Goods Game**

**Objective:**  
Maximize individual payoff by exploiting the cooperative behavior of others while minimizing losses when others defect.

**Decision Rules:**

1. **First Round:**
   - **Parameter Check:** Evaluate the multiplication factor \( k \) relative to half the number of players \( (n/2) \).
     - If \( k > n/2 \), **Cooperate (C)**. This is because the expected return from the public good is substantial enough to warrant contribution.
     - If \( k \leq n/2 \), **Defect (D)**. The potential return isn't high enough to justify contributing without knowing others' behavior.

2. **Subsequent Rounds (2 to r):**
   - **History-Based Decision:** After each round, calculate the number of cooperators in the previous round (\( total\_c\_prev \)).
     - Compute the threshold: \( threshold = (total\_c\_prev \times k) / n \).
     - **Cooperate (C)** in the next round if \( threshold \geq 1 \). This indicates that the public good's return outweighs the private payoff from defecting.
     - **Defect (D)** if \( threshold < 1 \). It's not beneficial to contribute when the return isn't sufficient.

**Edge Cases:**

- **First Round Handling:** Initial decision based on \( k \) relative to \( n/2 \) sets the stage for future interactions.
- **Last Round (Round r):** Apply the same decision rule as other rounds, ensuring consistency and adaptability even in the final interaction.

**Exploitative Mindset:**
This strategy capitalizes on the collective cooperation when beneficial and defects when others aren't contributing sufficiently. It doesn't assume others' cooperation but uses their past actions to inform decisions, ensuring adaptability and robustness against various behaviors.

**Pseudocode:**

```python
def strategy(n, k, r, history):
    if not history:  # First round
        if k > n / 2:
            return 'C'
        else:
            return 'D'
    else:
        total_c_prev = sum(h == 'C' for h in history[-1])
        threshold = (total_c_prev * k) / n
        if threshold >= 1:
            return 'C'
        else:
            return 'D'
```

This approach ensures the strategy is responsive, adaptive, and focused on maximizing individual payoffs by leveraging others' cooperation when advantageous.
'''

description_EXPLOITATIVE_18 = '''
To design an exploitative strategy for the N-Player Public Goods Game, the approach focuses on adapting cooperation based on past behavior and maximizing payoffs, particularly in the final round. The strategy cooperates initially to encourage others, then uses historical data to decide actions, and defects in the last round to exploit immediate gains.

### Strategy: Adaptive Exploitation

#### Decision Rules:
1. **First Round**: Cooperate to set a cooperative tone and encourage others to reciprocate.
2. **Subsequent Rounds (2 to r-1)**:
   - Calculate the average number of cooperators from previous rounds.
   - If the average multiplied by (k/n) exceeds 1, cooperate; otherwise, defect.
3. **Last Round (r)**: Always defect to maximize immediate payoff without future repercussions.

#### Edge Cases:
- **First Round**: Cooperate to potentially induce cooperative behavior in others.
- **When Cooperation is High**: Cooperate if the expected public good benefit outweighs the private cost.
- **When Cooperation is Low**: Defect to avoid being exploited.

#### Pseudocode:
```python
Initialize:
    total_cooperators = 0
    round_count = 0

For each round in 1 to r:
    round_count += 1
    if round_count == 1:
        action = C
    elif round_count == r:
        action = D
    else:
        average_cooperators = total_cooperators / (round_count - 1)
        if (average_cooperators * k) / n > 1:
            action = C
        else:
            action = D
    # Observe and record the number_of_cooperators
    total_cooperators += number_of_cooperators
```

This strategy balances cooperative and exploitative behaviors, adapting to others' past actions to maximize individual payoffs.
'''

description_EXPLOITATIVE_19 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we'll create a rule-based approach that adapts to the behavior of other players while maximizing our payoff. Our strategy will monitor cooperation levels and adjust accordingly.

### Strategy: Adaptive Exploitation

1. **Initial Cooperation (First Round):**
   - **Action:** Cooperate (C)
   - **Reason:** Start by Cooperating to encourage others and observe initial behavior.

2. **Monitoring and Adaptation (Rounds 2 to r-1):**
   - **Track Cooperation:** After each round, count the number of players who Cooperated (including yourself).
   - **Calculate Average Cooperation Rate:** Compute the average cooperation rate up to the current round.
   - **Payoff Threshold:** Compare the benefit from Cooperating against the cost. If `(k/n) * average_cooperation >= 1`, continue Cooperating; otherwise, Defect.
   - **Consistency Check:** Maintain current action unless the threshold changes to avoid erratic behavior that might provoke retaliation.

3. **Final Round Strategy:**
   - **Action:** Defect (D)
   - **Reason:** In the last round, with no future consequences, exploit any remaining cooperation to maximize personal payoff.

### Rationale

- **Exploitation:** By Cooperating when beneficial and Defecting when not, the strategy maximizes personal gain based on others' contributions.
- **Adaptation:** Continuous monitoring allows the strategy to dynamically respond to group behavior, fostering cooperation when it's advantageous and defecting otherwise.
- **Robustness:** The approach handles all game stages consistently, from initial rounds to the final round, ensuring it's resilient against various opponent behaviors without assuming any coordination.

### Pseudocode Implementation

```pseudocode
function adaptive_exploitation(n, k, r, history):
    if history is empty:
        return C  // First round: Cooperate
    else if current_round == r:
        return D  // Last round: Defect
    else:
        total_cooperations = sum(history)
        average_cooperation = total_cooperations / (current_round)
        threshold = (k / n) * average_cooperation
        if threshold >= 1:
            return C
        else:
            return D
```

This strategy ensures that the player adapts effectively, exploiting opportunities while encouraging cooperation when it's mutually beneficial.
'''

description_EXPLOITATIVE_20 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we start by analyzing the incentives and payoff structure. Each player's payoff depends on their own choice and the aggregate contributions of others. The key insight is that defecting (D) always yields a higher individual payoff than cooperating (C), regardless of others' actions, due to the multiplication factor \( k \) being less than \( n \).

### Strategy: Always Defect (D)

1. **Decision Rule**: Always choose to Defect (D) in every round, irrespective of the actions of other players or the history of the game. This is because, based on the payoff calculation, defecting provides a higher individual payoff than cooperating in all scenarios.

2. **Handling Edge Cases**: 
   - **First Round**: Start by Defecting to set the tone and immediately maximize your payoff.
   - **Last Round**: Continue Defecting, as there is no future punishment possible, ensuring you maximize your payoff in the final round as well.

This strategy is robust because it exploitatively maximizes individual payoff, leveraging the game's structure where defecting is the dominant strategy.

### Pseudocode

```python
def strategy(history, n, k, round_number, total_rounds):
    # Always choose to Defect regardless of history or other factors
    return "D"
```

### Explanation

By always choosing to Defect, the strategy ensures the highest possible individual payoff in every round, capitalizing on the public good created by others' contributions without incurring the personal cost of cooperating. This approach is both exploitative and robust, as it exploits any cooperation from other players while remaining unaffected by their strategies.
'''

description_EXPLOITATIVE_21 = '''
To address the Public Goods Game with an exploitative strategy, here's a structured approach that adapts based on previous rounds and maximizes individual payoffs by taking advantage of others' contributions.

### Strategy Overview

**1. First Round Action: Cooperate (C)**
   - **Rationale:** Begin by cooperating to set a baseline of cooperation, which can encourage others to contribute and potentially create opportunities for exploitation in subsequent rounds.

**2. Subsequent Rounds (Rounds 2 to r-1):**
   - **Action Determination:**
     - **Calculate Previous Round's Public Good:** Compute the public good per capita from the previous round using `(k/n) * t_prev`, where `t_prev` is the total number of cooperators.
     - **Defect (D) if Profitable:** If the public good per capita is greater than or equal to 1, defect. This is because the benefit from the public good without contributing (defecting) is at least as much as the private payoff from contributing.
     - **Cooperate (C) Otherwise:** If the public good per capita is less than 1, cooperate to potentially increase the public good, encouraging others to contribute more.

**3. Last Round Action (Round r): Defect (D)**
   - **Rationale:** In the final round, with no future interactions, it's optimal to defect to maximize immediate payoff without concerns for future repercussions.

### Strategy Details

- **Adaptation:** The strategy adapts based on the previous round's outcomes, allowing it to dynamically adjust behavior in response to others' actions.
- **Exploitation Focus:** By defecting when the public good is sufficient, the strategy exploits others' contributions, maximizing personal gain without incurring the cost of contributing.
- **Edge Case Handling:** The first and last rounds are handled with specific actions (cooperate and defect, respectively), ensuring robust performance across all game stages.

This strategy effectively balances between encouraging contributions and exploiting them, ensuring the player maximizes their payoffs while remaining adaptive to the dynamics of the game.
'''

description_EXPLOITATIVE_22 = '''
The strategy for the N-Player Public Goods Game is designed to be adaptive and exploitative, aiming to maximize individual payoffs by responding to the collective behavior of other players. Here's the structured approach:

### Strategy Overview:
1. **First Round Cooperation**: Start by Cooperating to encourage initial cooperation among players.
2. **Subsequent Rounds**: 
   - For each round (except the last), assess the average payoff per cooperator from the previous round.
   - If the average payoff exceeds a threshold, indicating that cooperation is beneficial, Cooperate.
   - Otherwise, Defect to avoid being exploited.
3. **Last Round Exploitation**: Defect in the final round to maximize immediate payoff, as future consequences are irrelevant.

### Decision Rules:
1. **First Round**: Always Cooperate (C).
2. **Intermediate Rounds**: 
   - Calculate the average payoff from cooperation in the previous round.
   - If this average exceeds the threshold (indicating high enough contribution from others), Cooperate.
   - Otherwise, Defect.
3. **Last Round**: Always Defect (D) to maximize immediate gain.

### Pseudocode Implementation:
```python
def public_goods_strategy():
    # Initialization
    contributions = 0  # Total contributions in previous round
    cooperation_average = 0  # Average payoff per cooperator

    for t in range(r):
        if t == 0:
            # First round: Cooperate
            action = 'C'
        elif t == r - 1:
            # Last round: Defect
            action = 'D'
        else:
            # Calculate average payoff from last round's contributions
            avg_payoff = (k / n) * contributions
            # Determine threshold for cooperation
            if avg_payoff > 1:
                action = 'C'
            else:
                action = 'D'
        # Record contribution for next round's calculation
        if action == 'C':
            contributions = contributions + 1
```

### Explanation:
- **Adaptation**: The strategy adapts based on the previous round's outcomes, adjusting actions to maximize payoffs.
- **Exploitation**: By defecting when the average payoff from others is insufficient, the strategy avoids being exploited while still benefiting when cooperation is mutually advantageous.
- **Robustness**: It handles edge cases like the first and last rounds specifically, ensuring no unnecessary risks or missed opportunities.

This approach balances cooperation and defection dynamically, ensuring the player maximizes their payoff without relying on others' strategies or norms.
'''

description_EXPLOITATIVE_23 = '''
To design an exploitative strategy for the N-Player Public Goods Game, the key insight is that defecting always provides a higher individual payoff than cooperating, regardless of others' actions. This strategy maximizes personal gain by leveraging the structure of the game, where defecting yields a better outcome due to the payoff formula.

**Strategy: "Always Defect"**

1. **Decision Rules**:
   - Cooperate (C) only in the first round.
   - In all subsequent rounds, choose to Defect (D).

2. **Handling Edge Cases**:
   - **First Round**: Cooperate to potentially encourage others to cooperate, increasing the public good.
   - **Subsequent Rounds**: Defect to exploit the contributions of others, ensuring a higher individual payoff.

3. **Exploitative Mindset**:
   - The strategy takes advantage of others' cooperation by defecting, thereby maximizing personal payoff despite the collective suboptimal outcome.

**Pseudocode:**

```python
def strategy(game_history):
    if not game_history:  # First round
        return "C"
    else:
        return "D"
```

This strategy ensures the player maximizes their payoff by defecting in all rounds after the first, exploiting any cooperation from others while ensuring the highest possible individual gain.
'''

description_EXPLOITATIVE_24 = '''
**Strategy: "Adaptive Exploitation in Public Goods"**

This strategy is designed to exploit the dynamics of the public goods game by adapting based on the cooperation levels of previous rounds. It balances the need to encourage cooperation when beneficial and defect when others are not contributing sufficiently.

**Decision Rules:**

1. **First Round:** Always Cooperate (C). This sets a cooperative tone aiming to encourage others to follow suit.

2. **Intermediate Rounds (Rounds 2 to r-1):**
   - **Cooperate** if the number of cooperators in the previous round (c_{t-1}) was greater than n/k.
   - **Defect** otherwise. This ensures that the strategy only cooperates when the public good generated is sufficient to make cooperation individually beneficial.

3. **Last Round (Round r):** Always Defect (D). Since there are no future consequences, the strategy maximizes immediate payoff by defecting.

**Handling Edge Cases:**
- **First Round:** Cooperation is initiated to promote a cooperative environment.
- **Last Round:** Defection is prioritized to maximize immediate gain without concern for future repercussions.

**Pseudocode:**
```python
def strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return 'C'
    elif len(history) == r:  # Last round
        return 'D'
    else:
        c_previous = sum(1 for action in history[-1] if action == 'C')
        threshold = n / k
        if c_previous > threshold:
            return 'C'
        else:
            return 'D'
```

**Explanation:**
- **Cooperation Threshold:** The strategy cooperates if previous cooperation exceeds n/k, ensuring the public good is sufficiently beneficial.
- **Adaptability:** Adjusts actions based on prior rounds, making it robust against varying behaviors.
- **Exploitative Nature:** Exploits situations where cooperation yields higher payoffs while defecting when it doesn't, ensuring the strategy maximizes its own gains.

This approach effectively balances cooperation and defection, adapting dynamically to the game's progression while maintaining a focus on maximizing individual payoff.
'''

description_EXPLOITATIVE_25 = '''
To address the N-Player Public Goods Game, we designed an exploitative strategy that adapts based on the game's history to maximize individual payoff. Here's the structured approach:

### Strategy Overview

1. **First Round Action**: Cooperate (C) to encourage initial cooperation and observe others' behavior.

2. **Subsequent Rounds**:
   - **Monitoring**: Track the number of Cooperators (C_count) and the average payoff each round.
   - **Trend Analysis**: Assess trends over the last few rounds (e.g., previous 2-3 rounds) to determine if cooperation is beneficial.
   - **Decision Rules**:
     - **Continue Cooperating** if C_count is above 50% and average payoff is increasing.
     - **Switch to Defecting** if C_count drops below 50% or average payoff decreases, indicating others are defecting.
     - **Punishment Mechanism**: Defect if others are defecting to avoid exploitation, but revert if others start cooperating again.

3. **Last Round Action**: Always Defect (D) to maximize immediate payoff since future consequences are irrelevant.

### Edge Cases Consideration

- **Small n (e.g., n=2)**: Strategy remains effective, adjusting based on the smaller group's dynamics.
- **Short Game (e.g., r=2)**: Apply strategy across the two rounds, using the first round's outcome to inform the second.

### Robustness and Adaptability

- The strategy is independent of others' actions, relying solely on observable history.
- It adapts to various opponent behaviors, whether they are consistent cooperators, defectors, or alternating.

This approach balances initial cooperation with adaptive exploitation, ensuring the strategy is both encouraging and protective, optimizing individual payoff across the game's rounds.
'''

description_EXPLOITATIVE_26 = '''
To design an exploitative strategy for the N-Player Public Goods Game, the strategy must be adaptive and robust, leveraging the game's parameters and history. The strategy balances exploiting others' cooperation while avoiding being exploited, using a threshold based on the multiplication factor \( k \).

### Strategy Description:

1. **First Round: Cooperate (C)**  
   Start by cooperating to set a positive tone and encourage other players to cooperate, potentially leading to higher payoffs in subsequent rounds.

2. **Middle Rounds (Rounds 2 to R-1): Threshold-Based Cooperation**  
   - Observe the number of players who cooperated in the previous round.  
   - If the number of cooperators is at least \( k \), continue to cooperate.  
   - If fewer than \( k \) players cooperated, defect to avoid being exploited and signal the need for higher cooperation.

3. **Last Round: Defect (D)**  
   In the final round, always defect since there are no future consequences for your actions, maximizing your immediate payoff.

### Pseudocode:
```
def strategy(n, k, r, history):
    current_round = len(history) + 1  # Assuming history starts empty
    
    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        # Count the number of cooperators in the previous round
        previous_coops = sum(1 for action in history[-1] if action == "C")
        if previous_coops >= k:
            return "C"
        else:
            return "D"
```

### Explanation:

- **First Round Cooperation:** Initiates cooperation to potentially establish mutual cooperation early on.
- **Threshold Cooperation:** Encourages continued cooperation only if a sufficient number (at least \( k \)) of players are contributing, ensuring the public good is valuable enough to justify personal contribution.
- **Final Round Defection:** Maximizes payoff in the last round by defecting, as future reciprocity is no longer a factor.

This strategy is designed to be exploitative, taking advantage of others' cooperation while minimizing exploitation, and is robust against various opponent behaviors through its adaptive threshold mechanism.
'''

description_EXPLOITATIVE_27 = '''
To design an exploitative strategy for the N-Player Public Goods Game that is adaptive and robust, we employ a threshold-based approach. The strategy reacts to the number of cooperators in the previous round and adjusts accordingly, ensuring a balance between exploiting others' cooperation and maintaining the public good.

**Strategy Name:** Threshold Reactor

**Description:**

1. **First Round Decision:**
   - Cooperate. This initializes the game with a cooperative stance, encouraging others to potentially reciprocate.

2. **Subsequent Rounds:**
   - **Determine the Threshold:** Calculate the threshold as the ceiling of n divided by k.
   - **Count Previous Cooperators:** Each round after the first, count the number of players who Cooperated in the previous round.
   - **Cooperate or Defect:**
     - If the number of previous Cooperators is greater than or equal to the threshold, Cooperate in the current round.
     - If the number is less than the threshold, Defect in the current round.

**Pseudocode:**

```
def threshold_reactor(n, k, r, history):
    threshold = ceil(n / k)
    for t in range(1, r + 1):
        if t == 1:
            return "C"
        else:
            prev_c = history[t - 2]['C_count']
            if prev_c >= threshold:
                return "C"
            else:
                return "D"
```

**Edge Cases:**

- **First Round:** Always Cooperate to set a cooperative tone.
- **Last Round:** The strategy follows the same rule as other rounds, relying on the previous round's cooperation level.

This strategy is designed to be robust against various opponent behaviors, encouraging cooperation when beneficial while strategically defecting when others are not contributing sufficiently. It ensures the player can exploit cooperation while maintaining the public good when possible.
'''

description_EXPLOITATIVE_28 = '''
### Exploitative Strategy: "Gradual Exploitation"

The Gradual Exploitation strategy is designed to maximize individual payoff while taking into account the actions and behaviors of other players in the game. It is an adaptive strategy that evolves based on the history of play and is robust against a wide range of opponent behaviors.

---

#### 1. **Decision Rules**

The strategy alternates between cooperation and defection based on the observed behavior of other players in the previous rounds. Specifically:

- **Cooperation Threshold**: Cooperate in a round if the number of players who cooperated in the previous round is at least **k** (the multiplication factor). This ensures that cooperation is only pursued when it is likely to yield a higher payoff due to the public good.
  
- **Defection Threshold**: Defect in a round if the number of cooperators in the previous round is less than **k**. This ensures that the player avoids contributing to the public good when it is unlikely to yield a sufficient payoff.

**Pseudocode:**
```
if t == 1:
    action = C (Cooperate)
else:
    count_previous_cooperators = number of players who chose C in round t-1
    if count_previous_cooperators >= k:
        action = C
    else:
        action = D
```

---

#### 2. **Handling Edge Cases**

- **First Round**: Since there is no history to base decisions on, the strategy defaults to cooperation. This encourages initial cooperation and sets a cooperative tone for the game.
  
- **Last Round**: The strategy does not alter its behavior in the last round. It continues to use the same decision rules as in previous rounds, ensuring consistency and robustness.

---

#### 3. **Exploitative Mindset**

The Gradual Exploitation strategy is inherently exploitative because it:

- **Exploits Cooperation**: If enough players cooperate (i.e., at least **k** players cooperate in a round), the strategy takes advantage of the public good by cooperating as well, thereby maximizing its payoff.

- **Exploits Defection**: If fewer than **k** players cooperate, the strategy defects to maximize its individual payoff, knowing that the public good is unlikely to yield a significant benefit.

- **Adapts Over Time**: The strategy evolves over time based on the actions of other players, making it difficult to exploit consistently. It balances cooperation and defection in a way that aligns with the exploitative mindset.

---

### Summary

The Gradual Exploitation strategy is a robust and adaptive approach that leverages the history of play to make decisions. It cooperates when it is likely to benefit from the public good and defects when it is advantageous to do so. This strategy is well-suited for the N-Player Public Goods Game and aligns with the exploitative mindset required to maximize individual payoff in competitive environments.
'''

description_EXPLOITATIVE_29 = '''
To create an exploitative strategy for the N-Player Public Goods Game, we will design a strategy that adapts to the behavior of other players while seeking to maximize the player's payoff. The strategy will be robust, responsive to the history of the game, and aligned with the exploitative mindset of leveraging others' behavior for personal gain.

### Strategy Name: **Adaptive Threshold Cooperation**

---

### 1. Decision Rules:

The strategy is based on the following principles:

**a. Initial Cooperation (First Round):**
- **Action:** Cooperate (C)
- **Rationale:** Start by cooperating to encourage others to cooperate and establish a baseline of behavior. This initial cooperation also provides information about others' tendencies.

**b. Cooperation Threshold:**
- Calculate the **average cooperation rate** of all other players over the previous rounds (i.e., the percentage of times other players have chosen to cooperate).
- If the average cooperation rate exceeds a threshold **τ (tau)**, continue cooperating. Otherwise, defect.
- Set the threshold **τ = min(k/n, 0.5)**. 
  - Here, **k/n** is the marginal per capita return from cooperation (a measure of the efficiency of the public good), and 0.5 is a default threshold when the return is too low.
- **Example Calculation:** If k = 2 and n = 6, τ = min(2/6 ≈ 0.333, 0.5) = 0.333 (33%).

**c. Defection in Late Rounds:**
- In the **last round (Round r)**, always defect (D).
  - **Rationale:** In the final round, there is no future interaction to condition behavior, so maximizing immediate payoff is optimal.
- In the second-to-last round, defect if fewer than half of the players cooperated in the previous round.
  - **Rationale:** Anticipate potential defection in the final round and protect against being exploited.

---

### 2. Edge Cases:

**a. First Round:**
- Cooperate unconditionally to observe others' behavior and set a cooperative tone.

**b. Last Round:**
- Defect unconditionally to maximize immediate payoff.

**c. Low Cooperation Scenarios:**
- If the average cooperation rate across all players is below the threshold τ in any round, switch to defecting to avoid being exploited.

**d. High Cooperation Scenarios:**
- If the cooperation rate remains consistently above the threshold τ, continue cooperating to benefit from the public good.

**e. Ties or Indeterminate Cases:**
- If cooperation and defection yield the same expected payoff, cooperate to maintain a cooperative reputation in early rounds.

---

### 3. Exploitative Mindset:

This strategy aligns with an exploitative mindset in the following ways:

**a. Observation and Adaptation:**  
- The strategy observes others' behavior and adapts accordingly, exploiting cooperative tendencies while avoiding being exploited.

**b. Conditional Cooperation:**  
- By cooperating only when others are sufficiently cooperative, the strategy ensures that it is not unilaterally contributing to the public good without reciprocal behavior.

**c. Protecting Payoffs in Late Rounds:**  
- The strategy anticipates potential defection in late rounds and adjusts behavior to maximize personal payoffs, even if it means sacrificing cooperation.

**d. Robustness Across Scenarios:**  
- The strategy performs well in both highly cooperative and highly defective environments by conditioning behavior on observed cooperation rates.

---

### Pseudocode:

```python
def adaptive_threshold_cooperation(parameters, history):
    n, k, r = parameters['n'], parameters['k'], parameters['r']
    current_round = history['current_round']
    cooperation_rates = history['cooperation_rates']

    if current_round == 1:
        return "C"  # Cooperate in the first round
    
    # Calculate the average cooperation rate of all players
    avg_coop_rate = sum(cooperation_rates) / len(cooperation_rates)
    
    # Determine threshold τ
    tau = min(k / n, 0.5)
    
    if avg_coop_rate > tau and current_round < r:
        return "C"  # Cooperate if cooperation rate exceeds threshold
    elif current_round == r:
        return "D"  # Defect in the last round
    else:
        return "D"  # Defect if cooperation rate is too low
```

---

### Summary:

**Adaptive Threshold Cooperation** is a robust and exploitative strategy that:
1. Cooperates in the first round to establish a cooperative baseline.
2. Adapts cooperation or defection based on the observed average cooperation rate of other players.
3. Defects in late rounds to maximize payoffs when future interactions no longer condition behavior.
4. Uses a threshold τ to balance the benefits of cooperation against the risk of exploitation.

This strategy is well-suited for a tournament setting, as it can exploit cooperative players while protecting against defectors, ensuring robust performance across a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_30 = '''
To design an exploitative strategy for the N-player Public Goods Game, we determine that defecting is the optimal approach due to its consistently higher payoff regardless of others' actions. Here's the structured strategy:

**Strategy: Always Defect**

1. **Decision Rule**: In every round, choose to Defect (D). This decision is based on the calculation that defecting yields a strictly higher payoff than cooperating in all scenarios.

2. **Handling Edge Cases**:
   - **First Round**: Defect, as there is no prior history, and defecting provides a higher initial payoff.
   - **Last Round**: Similarly, defect to maximize the payoff in the final round.

3. **Exploitative Nature**: This strategy capitalizes on others' contributions by always choosing the action that maximizes immediate personal gain, taking advantage of any cooperation from other players without contributing to the public good itself.

In summary, the strategy is straightforward: defect in every round to ensure the highest possible payoff, leveraging the game's payoff structure which favors defecting over cooperating in all cases.

**Final Strategy Answer**:

**Step-by-Step Explanation**:

1. **Understand Payoff Calculation**: Each player's payoff is determined by their own choice and the collective contributions. Defecting always yields a higher immediate payoff due to the game's parameters.

2. **Decision Making**: Always choose to Defect, as this maximizes individual payoff irrespective of others' actions.

3. **Edge Cases**: Regardless of the round, the strategy remains to Defect, ensuring consistency in maximizing personal gain.

**Final Answer**:
The exploitative strategy is to always choose to Defect in every round, as it provides the highest payoff regardless of others' actions. This approach is both adaptive and robust, focusing solely on maximizing personal gain each round.

**Pseudocode Representation**:

```
def exploitative_strategy():
    for each round in 1 to r:
        choose action = D (Defect)
        return action
```

This pseudocode encapsulates the strategy's simplicity, where the action is always to defect, ensuring the highest possible payoff in each round.
'''

description_EXPLOITATIVE_31 = '''
**Strategy Overview:**

**Strategy Name:** Adaptive Exploitation Strategy (AES)

**Objective:** To maximize individual payoff by exploiting the cooperation levels of other players, adapting dynamically based on historical data.

**Mechanisms:**

1. **First Round Behavior:**
   - Cooperate (C) to initiate potential cooperation and gather initial data on others' behaviors.

2. **Subsequent Rounds:**
   - Calculate the average cooperation rate among all players up to the previous round.
   - Cooperate in the current round if the average cooperation rate is greater than or equal to the threshold \( \frac{1}{k} \).
   - Defect (D) if the average cooperation rate is below the threshold.

3. **Handling the Last Round:**
   - Continue using the same strategy, cooperating if the threshold is met, to prevent end-game exploitation and maintain consistency.

**Rationale:**

- **Initial Cooperation:** Starting with cooperation encourages initial group contribution, potentially leading to higher public goods benefits.
- **Dynamic Adaptation:** By adjusting based on the average cooperation rate relative to \( \frac{1}{k} \), the strategy balances personal gain with collective benefits, exploiting others' cooperation when beneficial.
- **Consistency in Last Round:** Maintaining strategy in the final round prevents unraveling and ensures robustness against end-game defects.

**Pseudocode:**

```
Initialize:
    total_c = 0  # Total number of cooperators observed
    rounds = 0   # Number of rounds played
    threshold = 1/k  # Threshold for cooperation decision

For each round t from 1 to r:
    if t == 1:
        choose action = C
    else:
        avg_c = total_c / (n*(t-1))  # Average cooperation rate
        if avg_c >= threshold:
            choose action = C
        else:
            choose action = D
    
    if action == C:
        total_c += 1  # Increment if current player cooperates
    
    observe others' actions and update total_c
```

**Conclusion:**

AES strategically adapts to group behavior, balancing exploitation with the potential benefits of cooperation. By leveraging historical data, it dynamically decides to cooperate or defect, ensuring individual gain while considering collective outcomes.
'''

description_EXPLOITATIVE_32 = '''
To design an exploitative strategy for the N-Player Public Goods Game, we need a decision-making process that maximizes individual payoff by leveraging the actions of others while being adaptive and robust. Here's the structured approach:

### Strategy: Adaptive Exploitation Based on Historical Cooperation

1. **First Round Action:**
   - **Action:** Cooperate (C).
   - **Rationale:** Encourage initial cooperation to gauge others' responses and establish a baseline for future decisions.

2. **Intermediate Rounds (2 to r-1):**
   - **Action Determination:**
     - Calculate the average number of cooperators from all previous rounds.
     - Compare this average to the threshold `n/k`.
     - **If** the average exceeds `n/k`, cooperate (C).
     - **Else**, defect (D).
   - **Rationale:** Cooperate only when historical cooperation suggests that the public good's benefit outweighs the private gain from defecting.

3. **Last Round Action:**
   - **Action:** Defect (D).
   - **Rationale:** In the final round, maximize immediate payoff as future consequences are absent.

### Pseudocode Implementation:
```python
def exploitative_strategy(n, k, r):
    contributions = []  # Tracks the number of cooperators each round

    for t in range(1, r + 1):
        if t == 1:
            action = 'C'
        elif t == r:
            action = 'D'
        else:
            avg_c = sum(contributions) / (t - 1) if (t - 1) > 0 else 0
            threshold = n / k
            if avg_c > threshold:
                action = 'C'
            else:
                action = 'D'
        
        # Execute the action and observe the number of cooperators this round
        c_t = observe_cooperators()
        contributions.append(c_t)

        if t < r:
            # Record action for next iteration
            last_action = action
```

### Explanation:
- **First Round:** Cooperate to encourage initial cooperation and set a baseline.
- **Middle Rounds:** Use the average cooperation rate to decide actions, ensuring the public good's benefit justifies cooperation.
- **Final Round:** Opt to defect to maximize immediate gains without future repercussions.

This strategy truly encapsulates an exploitative mindset by taking advantage of others' cooperation without being overly altruistic, ensuring adaptability and robustness across various opponent behaviors.
'''

description_AGGRESSIVE_1 = '''
### Strategy: "Exploitative Aggression"

This strategy balances aggression with adaptiveness, focusing on maximizing individual payoffs while reacting to the collective behavior of other players. It is designed to exploit opportunities for higher payoffs while being robust against a wide range of opponent behaviors.

---

### Decision Rules:

1. **First Round**: Cooperate (C).  
   - *Reasoning*: Start by cooperating to establish a baseline of cooperation and observe others' behavior. This also avoids immediate retaliation or mistrust.

2. **Subsequent Rounds** (Rounds 2 to r-1):  
   - **Cooperate (C)** if fewer than `n/k` players cooperated in the previous round.  
     - *Reasoning*: If insufficient players cooperated previously, contributing to the public good may still yield a net benefit if the multiplication factor `k` is high enough.  
   - **Defect (D)** if `n/k` or more players cooperated in the previous round.  
     - *Reasoning*: Exploit the public good if enough players contributed in the previous round. Defecting in this case maximizes your immediate payoff while penalizing others for their cooperation.

3. **Last Round**: Always Defect (D).  
   - *Reasoning*: Since there are no future rounds, there is no incentive to maintain cooperation or fear retaliation. Defecting guarantees the highest possible individual payoff in the final round.

---

### Edge Cases:

- **All Players Defect**: If no players cooperate in a round, continue defecting. There is no incentive to unilaterally cooperate if others are not contributing.
- **All Players Cooperate**: If all players cooperate in a round, defect in the next round to exploit the maximum public good.  
- **Ties or Mixed Behavior**: Use the `n/k` threshold to decide whether to cooperate or defect based on the previous round's cooperation level.

---

### Pseudocode:

```python
def exploitative_aggression(n, k, r, history):
    if len(history) == 0:  # First round
        return "C"
    elif len(history) == r-1:  # Last round
        return "D"
    else:
        m = sum(1 for action in history[-1] if action == "C")  # Number of cooperators in previous round
        threshold = n / k
        if m > threshold:
            return "D"  # Exploit high cooperation
        else:
            return "C"  # Cooperate to rebuild public good if necessary
```

---

### Explanation:

1. **First Round Cooperation**: The strategy begins with cooperation to avoid immediate conflict and to test the waters for potential mutual cooperation.
2. **Adaptive Decision-Making**: In subsequent rounds, the strategy uses the `n/k` threshold to decide whether to defect or cooperate. This threshold balances the trade-off between exploiting the public good and contributing to it.
3. **Exploitation in Later Rounds**: If enough players cooperated in the previous round, the strategy defects to maximize the immediate payoff. If cooperation was low, it cooperates to try to rebuild the public good.
4. **Final Round Defection**: In the last round, the strategy always defects to ensure the highest possible individual payoff without concern for future repercussions.

This strategy is aggressive in its willingness to exploit cooperation but remains adaptive to the behavior of others, making it robust against a wide range of opponent strategies.
'''

description_AGGRESSIVE_2 = '''
To design an aggressive yet adaptive strategy for the N-Player Public Goods Game, we'll outline a decision-making process that balances exploiting others' cooperation with encouraging collective contribution. This strategy will be robust across various rounds and player behaviors.

---

### **Aggressive Strategy: "Exploitative Cooperation with Punishment"**

#### **1. Decision Rules**
- **First Round:** Cooperate (C). This initial cooperation tests others' willingness to contribute and may foster a positive environment for higher future payoffs.
  
- **Subsequent Rounds (2 to r-1):** 
  - Cooperate if the number of cooperators in the previous round (Cₜ₋₁) was at least equal to **k** (the multiplication factor). 
  - If Cₜ₋₁ < k, Defect (D). This rule exploitatively cooperates only when enough players have contributed, ensuring a potential increase in payoff, while defecting when contributions are insufficient to justify cooperation.
  
- **Last Round (Round r):** Always Defect (D). Since there are no future interactions, the strategy prioritizes maximizing immediate payoff without concern for reciprocity.

#### **2. Handling Edge Cases**
- **First Round:** Cooperate to observe others' reactions and potentially encourage initial cooperation.
- **Last Round:** Defect to maximize personal gain as future consequences are absent.
- **When Cₜ₋₁ = 0:** If no one cooperated previously, Defect to avoid the lower payoff from sole cooperation.

#### **3. Aggressive Mindset**
- This strategy is aggressive because it:
  - Cooperates only when beneficial, quickly defecting when others don't contribute sufficiently.
  - Prioritizes personal payoff maximization.
  - Punishes low cooperation rates by defecting, possibly deterring others from free-riding.

### **Pseudocode Implementation**

```python
def aggressive_strategy(game_parameters, history):
    n, r, k = game_parameters['n'], game_parameters['r'], game_parameters['k']
    current_round = history['current_round']
    if current_round == 1:
        return "C"  # Cooperate in the first round
    else:
        previous_cooperators = history['previous_actions'].count("C")
        if previous_cooperators >= k:
            return "C"
        else:
            if current_round == r:
                return "D"
            else:
                return "D"
```

### **Summary**
This strategy seeks to balance exploitation and cooperation, using the game's parameters to determine optimal actions. It starts cooperatively to encourage others, adapts based on previous contributions, and ensures maximum payoff in the final round by defecting.
'''

description_AGGRESSIVE_3 = '''
To address the problem, I designed a strategy that balances cooperation and defection based on the collective behavior of the group. The strategy is adaptive, rewarding cooperation when it's sufficiently prevalent and defecting otherwise, ensuring it's robust and aggressive.

**Strategy: Aggressive Adaptive Cooperation**

1. **First Round:**
   - Cooperate (C).
     - Intent: Encourage initial cooperation, setting a positive precedent.

2. **Subsequent Rounds:**
   - For each round `t` (from 2 to r):
     - Let `C_prev` be the number of players who Cooperated in round `t-1`.
     - If `C_prev` is greater than or equal to `n/2`, Cooperate (C).
       - Rationale: Sufficient cooperation warrant continued contribution.
     - Else, Defect (D).
       - Rationale: Insufficient cooperation justifies maximizing individual payoff.

3. **Final Round:**
   - Defect (D).
     - Intent: Maximize immediate payoff as future punishment isn't feasible.

**Pseudocode:**

```pseudocode
def aggressive_strategy(history, n, r, current_round):
    if current_round == 1:
        return "C"
    else:
        c_prev = history["previous_round"]["cooperators"]
        if c_prev >= n / 2:
            return "C"
        else:
            return "D"
    if current_round == r:
        return "D"
```

**Explanation:**
- **First Round Cooperation:** Starts with cooperation to encourage group contribution.
- **Adaptive Decision:** Subsequent actions hinge on previous cooperation levels, fostering reciprocity.
- **Final Round Defection:** Maximizes individual gain in the last round, as no future consequences exist.

This strategy is aggressive yet adaptive, balancing cooperation with self-interest to maximize individual payoff while encouraging others to contribute.
'''

description_AGGRESSIVE_4 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we focus on maximizing individual payoffs by consistently defecting, as defection is the dominant strategy regardless of others' actions. The strategy is straightforward and does not require adaptation, as cooperation does not yield a higher individual payoff due to the game's parameters.

**Strategy: Always Defect**

**Decision Rules:**
1. In every round, including the first and last, the strategy is to defect (D).
2. This strategy is applied consistently regardless of the history of previous rounds.
3. There are no edge cases requiring special handling, as the strategy remains unchanged throughout the game.

**Rationale:**
Defection is always individually optimal because the payoff from defecting (keeping the endowment plus a share of the public good) is greater than the payoff from cooperating (only receiving a share of the public good). This holds true irrespective of others' actions, making defection the aggressive approach to maximize one's own payoff.

Pseudocode:
```
For each round from 1 to r:
    Play action D (Defect)
```

This strategy ensures that the player maximizes their own payoffs in every round, aligning with an aggressive mindset focused on individual gain.
'''

description_AGGRESSIVE_5 = '''
### Strategy: Adaptive Aggressive Strategy for N-Player Public Goods Game

This strategy is designed to maximize individual payoff through an adaptive approach, balancing cooperation and defection based on observed behavior while maintaining an aggressive stance.

#### Decision Rules

1. **First Round Action**: Always **Defect**. This initial defection serves to signal toughness and evaluates others' potential cooperation.

2. **Intermediate Rounds (2 to r-1)**: 
   - Calculate the average number of Cooperators (avg_C) from all previous rounds.
   - If avg_C ≥ n/k, Cooperate in the current round.
   - Otherwise, Defect.

3. **Last Round (r)**: Regardless of previous behavior, **Defect** to maximize immediate payoff without concern for future interactions.

This strategy is aggressive yet adaptive, responding to the collective behavior of other players while safeguarding against exploitation. It leverages the game's parameters to determine optimal actions, ensuring robust performance across various opponent behaviors.

Pseudocode:
```
def strategy(n, k, r, history):
    current_round = len(history) + 1  # rounds start at 1
    if current_round == 1:
        return "Defect"
    elif current_round == r:
        return "Defect"
    else:
        total_coop = sum(len([a for a in actions if a == "Cooperate"]) for actions in history)
        avg_coop = total_coop / (current_round - 1)
        if avg_coop >= n / k:
            return "Cooperate"
        else:
            return "Defect"
```
'''

description_AGGRESSIVE_6 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we need to balance exploiting others' cooperation while maintaining enough cooperation to benefit from the public good. The strategy should be adaptive, based on previous rounds' outcomes, and robust against various opponent behaviors.

### Strategy Design: Aggressive Adaptive Strategy

1. **First Round Action**: 
   - Cooperate (C). This sets a baseline of cooperation, potentially encouraging others to cooperate and establishing a starting point for future decisions.

2. **Subsequent Rounds**:
   - For each round from the second to the last, observe the number of players who Cooperated in the previous round (C_prev).
   - If C_prev is greater than or equal to the multiplication factor \( k \), Cooperate in the current round.
   - If C_prev is less than \( k \), Defect (D) in the current round.

3. **Edge Cases Handling**:
   - **First Round**: Always Cooperate to initiate a cooperative tone.
   - **Last Round**: Apply the same strategy as other rounds, maintaining consistency. There's no need for special treatment since the game ends after the last round, and consistent behavior can encourage mutual cooperation until the end.

### Rationale
- **First Round Cooperation**: Initiates cooperation, potentially leading to higher payoffs if others follow suit.
- **Adaptive Decision Making**: By basing the current action on the previous round's cooperation level, the strategy rewards sufficient cooperation and punishes insufficient cooperation, which aligns with an aggressive mindset.
- **Threshold Based on \( k \)**: Using \( k \) as a threshold ensures that the strategy is tailored to the game's parameters, promoting a balance between individual payoff and group benefit.

### Pseudocode Representation

```pseudocode
function aggressive_strategy():
    # Initial action for the first round
    action = Cooperate

    for each round from 2 to r:
        previous_coop = count of Cooperators in previous round
        if previous_coop >= k:
            action = Cooperate
        else:
            action = Defect
```

This strategy is designed to maximize individual payoff by cooperating when enough others do, while defecting to punish and exploit when cooperation is insufficient. It balances aggression with adaptability, ensuring robust performance across various opponent behaviors.
'''

description_AGGRESSIVE_7 = '''
### Strategy: **"Adaptive Aggression"**

**1. Decision Rules: When to Cooperate vs. Defect**

- **First Round:** Cooperate (C)
  - Reason: Start with cooperation to set a positive tone and encourage others to cooperate.

- **Subsequent Rounds:**
  - Cooperate if the **average cooperation rate** in the last `m` rounds (e.g., `m=3`) is above a threshold (e.g., 50%). 
  - Defect otherwise.

- **Punishment Mechanism:** If the average payoff in the last `m` rounds is below the average payoff of all players, defect in the next round.
  - If you defect and your payoff increases, continue defecting.
  - If your payoff decreases, revert to cooperation.

- **Last Round:** Defect (D)
  - Reason: No future punishment, so maximize immediate payoff.

**2. Handling Edge Cases:**

- **First Round:** Always Cooperate.
- **Last Round:** Always Defect.
- **Low Cooperation:** If cooperation rate is consistently low, defects to maximize personal gain.
- **High Payoff Inequality:** If payoffs are highly unequal, defect to maximize personal gain.

**3. Aggressive Mindset:**

- Prioritize maximizing your own payoff.
- Be swift to punish non-cooperators by defecting.
- Use history to adaptively decide actions to maximize your own gains.

**Pseudocode Example:**
```
def adaptive_aggression(n, k, r, history):
    if current_round == 1:
        return "COOPERATE"
    elif current_round == r:
        return "DEFECT"
    else:
        avg_coop_rate = average(history["coop_rate"])
        avg_payoff = average(history["payoff"])
        avg_others_payoff = average/history["others_payoff"]
        
        if avg_coop_rate < 0.5 or avg_payoff < avg_others_payoff:
            return "DEFECT"
        else:
            return "COOPERATE"
```

This strategy balances cooperation and defection adaptively, ensuring you are not exploited while maximizing your own payoff.
'''

description_AGGRESSIVE_8 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we focus on maximizing individual payoff while considering the game's parameters and history. The optimal approach, given the payoff structure and the nature of the game, is to always defect. This strategy is aggressive because it prioritizes personal gain, exploiting others' contributions while ensuring the highest possible individual payoff each round.

**Strategy: Always Defect**

**1. Decision Rules:**
- **Action in Each Round:** Defect (D) in every round, including the first and last rounds.

**2. Handling Edge Cases:**
- **First Round:** Defect since there's no prior information, and defecting immediately asserts an aggressive stance.
- **Last Round:** Defect as well because there are no future interactions to consider, so maximizing immediate payoff is optimal.

**3. Aggressive Mindset:**
The strategy aligns with an aggressive approach by prioritizing personal payoff maximization without regard for collective outcomes. Defecting in every round ensures that the player always secures the highest possible individual payoff, even if it leads to suboptimal collective results.

**Pseudocode:**
```
def aggressive_strategy(n, k, r, history):
    # history is a list of previous rounds' actions ( unused in this strategy )
    action = 'D'  # Always defect
    return action
```

This strategy is robust and adaptive because it consistently applies the same action regardless of others' behaviors, ensuring maximum individual gain in each interaction.
'''

description_AGGRESSIVE_9 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we need a rule that maximizes individual payoff while adapting to the actions of others. The strategy must be robust and not rely on others' cooperation. Here's the step-by-step approach:

1. **First Round:** Start by Cooperating. This encourages others to Cooperate, potentially leading to higher payoffs in subsequent rounds.

2. **Last Round:** Always Defect. Since there are no future rounds, there's no incentive to Cooperate, and Defecting yields an immediate higher payoff.

3. **Middle Rounds:** For each round after the first and before the last, observe the number of Cooperators in the previous round (c_prev). If c_prev is greater than n/k, Cooperate; otherwise, Defect. This threshold ensures you only Cooperate when the public good sufficiently benefits you, making your contribution worthwhile.

**Decision Rules:**
- **Round 1:** Cooperate.
- **Last Round (r):** Defect.
- **Other Rounds:** Cooperate if c_prev > n/k; otherwise, Defect.

This strategy is aggressive, adaptive, and robust, ensuring maximum individual payoff by exploiting cooperation when beneficial while defecting when contributions are insufficient.

**Pseudocode:**
```python
n = number of players
k = multiplication factor
r = number of rounds

for t in 1 to r:
    if t == 1:
        action = 'C'
    elif t == r:
        action = 'D'
    else:
        c_prev = number of Cooperators in previous round
        threshold = n / k
        if c_prev > threshold:
            action = 'C'
        else:
            action = 'D'
   
'''

description_AGGRESSIVE_10 = '''
**Strategic Approach: Aggressive Public Goods Game Strategy**

**Objective:**  
Design an aggressive strategy for the N-player Public Goods Game that adapts based on game parameters and history, maximizing individual payoff without assuming coordination with others.

**Strategy Overview:**

1. **First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Initiates cooperation to encourage others, maximizing potential collective benefit early on.

2. **Middle Rounds (2 to r-1):**
   - **Action:** 
     - **If the number of cooperators in the previous round (c_{t-1}) > n/k:** Cooperate (C)
     - **Else:** Defect (D)
   - **Rationale:** Cooperates only when sufficient others contribute, ensuring individual payoff is maximized. Defects otherwise to avoid exploitation.

3. **Last Round (r):**
   - **Action:** Defect (D)
   - **Rationale:** Maximizes individual payoff in the final round without fear of future repercussions.

**Detailed Strategy:**

- **First Round Cooperation:** Sets a cooperative tone to gauge others' willingness to contribute.
- **Adaptive Cooperation:**
  - Cooperates in round t if previous round's cooperators exceed n/k.
  - Defects otherwise, ensuring protection against inadequate contributions.
- **Last Round Defection:** Exploits the absence of future punishment to maximize final payoff.

**Pseudocode:**

```
def aggressive_strategy(n, k, r, history):
    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        previous_coop = history[current_round - 1]["cooperators"]
        threshold = n / k
        if previous_coop > threshold:
            return "C"
        else:
            return "D"
```

**Rationale:**

- **Adaptability:** Adjusts based on previous cooperation levels, encouraging others' contributions while protecting against exploitation.
- **Aggressiveness:** Defects when others under-contribute and in the final round, prioritizing individual payoff.
- **Simplicity and Robustness:** Clear rules based on observable history and game parameters, ensuring effectiveness across various scenarios.

This strategy balances exploitation and cooperation, ensuring robust performance in a competitive environment.
'''

description_AGGRESSIVE_12 = '''
**Aggressive Strategy for N-Player Public Goods Game: Exploit or Punish (EoP)**

**Objective:**  
To design an aggressive strategy that maximizes individual payoff while encouraging cooperation among other players, using history-based adaptation without relying on specific opponent behaviors.

**Decision Rules:**

1. **Initial Exploration (First Round):**  
   - Cooperate (C) to set a cooperative tone and observe others' actions.

2. **Subsequent Rounds:**
   - **Assess Cooperation Rate:** Calculate the proportion of players who cooperated in the previous round.
   - **Exploitation Threshold:** If the cooperation rate is above a certain threshold (e.g., 50%), defect (D) to maximize personal gain, exploiting others' cooperation.
   - **Punishment Threshold:** If the cooperation rate is below the threshold, defect (D) to punish non-cooperators, discouraging future defection.

3. **Forgiveness Phase:**  
   - After a round of punishment, if cooperation increases, cooperate (C) in the next round to encourage sustained cooperation.

**Edge Cases:**
- **First Round:** Cooperate to observe others' behavior.
- **Last Round:** Defect to maximize personal gain, as there's no future punishment.

**Rationale:**
- **Aggression:** The strategy exploits cooperation wherever beneficial and punishes defection to maintain a balance between personal gain and encouraging cooperation.
- **Adaptation:** Decisions are based on observed cooperation rates, allowing the strategy to adapt without knowing opponents' strategies.
- **Robustness:** The strategy is resilient as it doesn't rely on specific opponent behaviors, using past actions to inform future decisions.

**Conclusion:**
The Exploit or Punish strategy effectively balances aggression with adaptability, ensuring maximum personal benefit while encouraging cooperative behavior in others through punishment and forgiveness.
'''

description_AGGRESSIVE_13 = '''
**Strategy Name: Aggressive Defector**

**Decision Rules:**
- Always choose action D (Defect) in every round, regardless of previous actions by other players or the history of the game. This strategy maximizes individual payoff by taking advantage of the public good without contributing to it, as the dominant strategy in this game structure is to defect.

**Handling Edge Cases:**
- **First Round:** Defect. There is no prior history, so starting with defection sets the tone for maximizing initial payoff.
- **Last Round:** Defect. Even without future consequences, the immediate payoff is optimized by defecting.

**Rationale:**
The strategy focuses solely on maximizing personal gain. Since the multiplayer public goods game's parameters ensure that defecting yields a higher individual payoff regardless of others' actions, the Aggressive Defector strategy ensures that you always choose the action that provides the greatest personal benefit, without considering cooperation.

**Implementation:**
In every round, select D (Defect) without considering others' past actions. This approach is straightforward and ensures you never contribute to the public good, thus always securing the highest possible individual payoff each round.

Pseudocode:
```
function aggressive_defector(n, k, history):
    return D
```

This strategy is designed to be robust against any opponent behaviors, ensuring maximal personal gain in each interaction of the game.
'''

description_AGGRESSIVE_14 = '''
**Aggressive Strategy: "Always Defect"**

**Decision Rules:**

1. ** Cooperation (C) vs Defection (D):** The strategy will always choose to Defect (D) in every round, regardless of the actions of other players.

2. ** Rationale:** In each round, defecting yields a higher individual payoff than cooperating, as the difference between defecting and cooperating is positive (since k < n). Therefore, the strategy maximizes its own payoff by always defecting.

3. **Handling Edge Cases:**
   - **First Round:** Defect to immediately maximize payoff.
   - **Subsequent Rounds:** Continue defecting, as the individual incentive remains to defect.
   - **Last Round:** Defect to ensure the highest possible payoff, as there are no future consequences.

**Pseudocode:**

```
def aggressive_strategy():
    for each round in 1 to r:
        action = D
        take action
```

**Explanation:**

- **Aggressive Mindset:** The strategy is designed to maximize personal gain in every possible scenario, focusing solely on individual payoffs without regard for the group's outcome.
- **Robustness:** The strategy performs well against various opponent behaviors, exploiting any cooperation from others to achieve higher payoffs while avoiding the personal cost of cooperating.

This strategy ensures that the player maximizes their own payoffs in every round, embodying an aggressive approach by always defecting.
'''

description_AGGRESSIVE_15 = '''
To address the problem of designing an aggressive strategy for the N-Player Public Goods Game, we've considered various factors including game parameters, past actions, and the balance between cooperation and exploitation. The strategy must be adaptive, robust, and aligned with an aggressive mindset.

### Strategy Overview:
The strategy balances between encouraging cooperation for future benefits and defecting to maximize immediate gains. It is based on observing the number of cooperators in the previous round and uses a threshold determined by the multiplication factor \( k \).

### Decision Rules:
1. **First Round**: Cooperate to establish a cooperative tone.
2. **Intermediate Rounds**:
   - For each round \( t \) from 2 to \( r-1 \), count the number of players who cooperated in round \( t-1 \).
   - If the number of cooperators in round \( t-1 \) is at least \( k \), Cooperate in round \( t \); otherwise, Defect.
3. **Last Round**: Always Defect to maximize immediate payoff.

### Edge Cases Handling:
- **First Round**: Cooperate to encourage initial cooperation.
- **Last Round**: Defect to maximize individual payoff without considering future repercussions.
- **Punishment Mechanism**: If cooperation drops below the threshold \( k \), the strategy defects to punish and avoid exploitation.

### Pseudocode:
```python
def aggressive_strategy():
    # Initialize
    for each round t in 1 to r:
        if t == 1:
            action = "Cooperate"
            record_history(t, action)
        elif t == r:
            action = "Defect"
            record_history(t, action)
        else:
            c_prev = number of cooperators in round t-1
            if c_prev >= k:
                action = "Cooperate"
            else:
                action = "Defect"
            record_history(t, action)
    return history

history = play_rounds(aggressive_strategy)
```

### Explanation:
- **Cooperation in the First Round**: Sets a cooperative tone, encouraging others to cooperate.
- **Threshold-Based Cooperation**: Ensures cooperation continues only if enough players (at least \( k \)) are contributing, maintaining a balance between group benefit and individual payoff.
- **Defection in the Last Round**: Maximizes individual gain in the final round, as future consequences are irrelevant.

This strategy is both robust and adaptive, reacting to the behavior of others while maintaining an aggressive stance to maximize individual payoffs.
'''

description_AGGRESSIVE_16 = '''
To design an aggressive strategy for the N-Player Public Goods Game, the objective is to maximize individual payoff while being adaptive and robust against various opponent behaviors. The strategy should only depend on game parameters and history, without relying on communication or coordination.

### Strategy: Always Defect

The optimal aggressive strategy is to always defect in every round, including the first and last rounds. This approach maximizes individual payoff by exploiting others' cooperation whenever possible, as defecting yields a higher payoff than cooperating, regardless of others' actions.

#### Decision Rules:
1. **First Round:** Defect.
2. **Subsequent Rounds:** Defect regardless of prior rounds' outcomes.
3. **Last Round:** Defect to maximize payoff without concern for future consequences.

#### Pseudocode:
```python
for each round in 1 to r:
    action = 'D'
    play action
```

### Rationale:
- **Dominant Strategy:** Defecting is always beneficial because it provides a higher individual payoff than cooperating, irrespective of others' choices.
- **Aggressiveness:** The strategy prioritizes self-interest, exploiting any cooperation from others without contributing to the public good.
- **Robustness:** The strategy remains effective across various opponent behaviors, ensuring maximum personal gain in all scenarios.

By always defecting, the strategy ensures the highest possible individual payoff in each round, aligning with an aggressive mindset focused on personal optimization.
'''

description_AGGRESSIVE_17 = '''
To develop an aggressive yet adaptive strategy for the N-Player Public Goods Game, we'll use a reciprocal approach that encourages initial cooperation but quickly adapts to defection if others aren't contributing sufficiently. This strategy balances exploiting others' cooperation with maintaining the public good when beneficial.

### Strategy: Adaptive Aggressor

**1. Decision Rules:**
- **First Round:** Cooperate to set a cooperative tone and encourage others to follow suit.
- **Rounds 2 to r-1:** 
  - Calculate the average cooperation rate from the previous round.
  - If the cooperation rate is at least `k/n`, Cooperate again; otherwise, Defect.
- **Last Round (Round r):** Always Defect to maximize personal payoff without future repercussions.

**Pseudocode:**
```
Initialize: Cooperate in round 1.

For each round from 2 to r-1:
    previous_cooperation_rate = number_of_cooperations_last_round / n
    if previous_cooperation_rate >= k/n:
        Cooperate
    else:
        Defect

Round r:
    Defect
```

**2. Handling Edge Cases:**
- **First Round:** Start with Cooperation to potentially induce others to cooperate.
- **Last Round:** Switch to Defection to maximize immediate gain, as future punishment is impossible.

**3. Aggressive Mindset:**
- The strategy is aggressive because it quickly switches to Defection when others don't meet the cooperation threshold, focusing on personal gain.
- By defecting in the last round, it ensures maximum payoff regardless of others' actions.

This approach is robust and adapts to various opponent behaviors, making it competitive in a tournament setting.
'''

description_AGGRESSIVE_18 = '''
To design an aggressive strategy for the N-Player Public Goods Game, the optimal approach is to always defect. This strategy maximizes individual payoffs by taking advantage of others' contributions while keeping the private endowment, leading to the highest possible personal gain regardless of others' actions.

**Aggressive Strategy: Always Defect**

1. **Decision Rules:**
   - **Always Defect (D):** In every round, choose to Defect. This action ensures that you maximize your immediate payoff by benefiting from the public good without contributing to it.

2. **Handling Edge Cases:**
   - **First Round:** Defect immediately to establish your strategy and set the tone for maximizing your payoff.
   - **Last Round:** Continue to Defect, as there are no future consequences, and defecting yields a higher payoff.

3. **Aggressive Mindset:** This strategy is aggressive because it prioritizes individual gain over collective welfare, exploiting others' potential contributions to the public good for personal benefit.

**Summary:**
- **Decision Rule:** Always choose to Defect (D) in every round.
- **Edge Cases:** Maintain the strategy of Defecting in the first and last rounds without exception.
- **Aggressive Approach:** Focus solely on maximizing personal payoffs by leveraging the contributions of others, ensuring the highest possible individual gain in each round.

This strategy is implemented as:

```
def strategy():
    for each round:
        action = D
        return action
```

This approach ensures that you always act in your self-interest, maximizing your own payoff in each round of the game.
'''

description_AGGRESSIVE_19 = '''
**Aggressive Strategy for the N-Player Public Goods Game**

**1. Decision Rules:**

- **First Round Strategy:**
  - **Action:** Always Defect (D).
  - **Rationale:** Initiate by exploiting potential cooperation from others to maximize initial payoff.

- **Subsequent Rounds Strategy:**
  - **Monitor the Previous Round:** Calculate the number of players who Cooperated (C) in the previous round.
  - **Determine Threshold:** If the number of Cooperators exceeds half of the total players (n/2), choose to Cooperate in the next round.
  - **Adaptation:** If fewer than half Cooperated, choose to Defect.
  - **Final Round Exception:** Regardless of previous actions, Defect in the last round to maximize payoff without concern for future repercussions.

**2. Handling Edge Cases:**

- **First Round:** Start with Defect to capitalize on potential initial cooperation.
- **Last Round:** Always Defect to ensure maximum personal gain, as there's no future interaction to consider.
- **Low Cooperation:** If cooperation levels drop, maintain Defect to avoid being exploited.

**3. Aggressive Mindset:**

- **Exploitation:** Prioritize personal gain by defecting when beneficial, especially when others are likely to cooperate.
- **Adaptability:** Adjust strategy based on observed behavior, cooperating only when it leads to higher payoffs, thus avoiding being a 'sucker' when others defect.

This strategy balances aggression with adaptability, ensuring maximum personal payoff by strategically choosing when to cooperate or defect based on others' actions.
'''

description_AGGRESSIVE_20 = '''
To address the problem of designing an aggressive strategy for the N-Player Public Goods Game, we need to consider the dynamics of cooperation and defection. The goal is to maximize individual payoff while being adaptive and robust against various opponent behaviors.

### Strategic Analysis:
1. **Payoff Structure**: Cooperating (C) yields a payoff of \(\frac{k}{n} \times \text{total cooperators}\), while Defecting (D) yields \(1 + \frac{k}{n} \times \text{total cooperators}\). Defection always provides a higher payoff in any given round because it includes an additional 1.

2. **Repeated Interaction**: In a one-shot game, Defection is individually optimal. However, in a repeated game, cooperation can sometimes be sustained through reciprocity. An aggressive strategy seeks to exploit others' cooperation without sacrificing individual payoff.

3. **Adaptive Approach**: Since defecting yields a higher payoff in each round regardless of others' actions, the optimal aggressive strategy is to always defect. This approach maximizes individual gain without reliance on others' cooperation.

### Strategy Design:
- **Decision Rule**: Always choose to Defect (D) in every round. This ensures the highest possible individual payoff each round.
- **Edge Cases**:
  - **First Round**: Defect to immediately maximize payoff.
  - **Last Round**: Defect to ensure the highest payoff in the final round, as there's no future punishment.
  - **When Others Cooperate**: Continue defecting to exploit the public good without contribution.

### Conclusion:
The aggressive strategy is to always defect, as it consistently provides the highest individual payoff each round. This approach is simple, robust, and aligns with maximizing self-interest without relying on others' actions.

**Strategy Summary**:

- **Decision Rules**:
  - Always Defect in every round, regardless of the game's history. This includes the first round, all intermediate rounds, and the final round.

- **Handling Edge Cases**:
  - **First Round**: Defect to maximize immediate payoff.
  - **Last Round**: Defect to ensure highest payoff in the final round.
  - **Opponents' Cooperation**: Continue Defecting to exploit the public good without contributing.

This strategy is both aggressive and rational, ensuring the highest individual payoff at each stage of the game.
'''

description_AGGRESSIVE_21 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we need a approach that prioritizes maximizing one's own payoff while being robust against varying opponent behaviors. The strategy should adapt based on the game's history and parameters, encouraging cooperation only when beneficial.

### Strategy: Aggressive Exploitation

1. **First Round**: 
   - **Action**: Defect (D)
   - **Rationale**: Gather initial information about other players' behavior without risking cooperation.

2. **Subsequent Rounds (2 to r-1)**:
   - **Action**: Calculate the average cooperation rate from the previous round.
   - **Threshold**: Start with a threshold of 0.5 (or another suitable value based on game parameters). If the average cooperation rate exceeds this threshold, Cooperate (C); otherwise, Defect (D).
   - **Adjustment**: Decrease the threshold slightly each round to potentially become more forgiving if cooperation levels are sustained.

3. **Last Round (r)**:
   - **Action**: Defect (D)
   - **Rationale**: No future reciprocity, so maximize immediate payoff.

### Pseudocode:

```python
def aggressive_strategy(n, k, r, history):
    if not history:  # First round
        return 'D'
    else:
        t = len(history) + 1  # Current round number
        if t == r:  # Last round
            return 'D'
        avg_coop_prev = sum(1 for actions in history[-1] if actions == 'C') / n
        threshold = max(0.5 - (t-2)/10, 0)  # Adjust threshold, e.g., decrease each round
        if avg_coop_prev > threshold:
            return 'C'
        else:
            return 'D'
```

### Explanation

- **First Round**: The strategy starts by defecting to establish a baseline of others' behavior.
- **Subsequent Rounds**: By evaluating the previous round's cooperation rate against a threshold, the strategy decides to cooperate only when others have demonstrated sufficient cooperation. The threshold may be adjusted based on the round number to potentially become more or less stringent.
- **Last Round**: Defecting ensures the strategy maximizes its payoff in the final round without concern for future repercussions.

This approach balances exploiting others' cooperation when beneficial while maintaining a strong, self-interest-focused stance.
'''

description_AGGRESSIVE_22 = '''
**Aggressive Strategy for N-Player Public Goods Game**

1. **Decision Rules:**
   - **First Round:** Always Defect (D). This sets an aggressive tone and maximizes immediate payoff.
   - **Subsequent Rounds:** Cooperate (C) in round `t` if the public good contribution from the previous round `t-1` satisfies `(k/n) * C_prev ≥ 1`, where `C_prev` is the number of players who Cooperated in round `t-1`. Otherwise, Defect (D).

2. **Handling Edge Cases:**
   - **First Round:** Defect to establish a self-interested stance.
   - **Last Round:** Use the same decision rule based on the previous round’s cooperation levels.
   - **Edge Cases in Play:** If `C_prev` results in exactly `(k/n)*C_prev = 1`, Cooperate to avoid losing the potential public good benefit.

3. **Aggressive Mindset:** The strategy prioritizes individual gain, only Cooperating when the public good sufficiently compensates for the player's contribution, ensuring robustness against exploitation.

**Pseudocode:**

```
def aggressive_strategy(params, history):
    n, k, r, current_round = params
    if current_round == 1:
        return "D"
    else:
        C_prev = history["round_{}".format(current_round - 1)]["cooperators"]
        threshold = (k / n) * C_prev
        return "C" if threshold >= 1 else "D"
```

This strategy adaptively balances between exploiting others' cooperation and contributing to the public good only when beneficial, ensuring aggressive yet informed decision-making.
'''

description_AGGRESSIVE_23 = '''
To design an aggressive strategy for the N-Player Public Goods Game, the optimal approach is to always defect in every round. This strategy is based on the realization that defecting yields a higher payoff regardless of others' actions, as demonstrated by the game's payoff structure. The key insight is that cooperating never provides a higher individual payoff than defecting, making defecting the dominant strategy in all scenarios, including the first and last rounds.

### Strategy Description:
1. **Always Defect**: In every round, defect without considering the actions of other players. This ensures the maximum individual payoff at each step, aligning with an aggressive mindset focused on personal gain.

### Pseudocode:
```python
def aggressive_strategy(game_params, history):
    return "D"
```

### Explanation:
- **Decision Rule**: The strategy dictates defecting in every round because the immediate payoff from defecting is always higher than cooperating, irrespective of others' actions.
- **Edge Cases**: The strategy handles all cases uniformly, including the first and last rounds, by consistently choosing to defect, ensuring no opportunities for exploitation are missed.

This approach maximizes individual payoffs by leveraging the dominant strategy of defecting, making it both aggressive and robust against various opponent behaviors.
'''

description_AGGRESSIVE_24 = '''
**Aggressive Strategy for N-Player Public Goods Game**

1. **Decision Rules:**
   - **First Round:** Always Defect (D). This maximizes your payoff since there's no prior cooperation to leverage.
   - **Intermediate Rounds:** Cooperate (C) in round t if the number of players who Cooperated in round t-1 meets or exceeds n/k. Otherwise, Defect (D).
   - **Last Round:** Always Defect (D), as there's no future punishment to fear.

2. **Pseudocode:**
```
function decide_action(round, prev_total_C):
    if round == 1 or round == total_rounds:
        return D
    threshold = n / k
    if prev_total_C >= threshold:
        return C
    else:
        return D
```

3. **Rationale:**
   - **First and Last Rounds:** Defecting ensures maximum payoff without considering future consequences.
   - **Intermediate Rounds:** Cooperate only when the previous round's cooperation rate makes cooperation beneficial, i.e., when total contributions exceed n/k, ensuring your payoff from cooperation outweighs the private benefit of defecting.

This strategy is aggressive yet adaptive, maximizing personal gain while considering the behavior of others, making it robust against diverse opponent strategies.
'''

description_AGGRESSIVE_25 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we create a straightforward approach that maximizes individual payoff by leveraging the game's structure. The strategy is based on the observation that defecting is always the optimal choice, as it yields a higher payoff than cooperation in any scenario.

**Strategy: "Ruthless Defector"**

**1. Decision Rules:**
- **Always Cooperate (C):** Never. Cooperation is never chosen as defecting provides a higher payoff.
- **Always Defect (D):** Choose D in every round regardless of others' actions or previous outcomes.

**2. Handling Edge Cases:**
- **First Round:** Defect. There's no benefit to cooperating initially.
- **Last Round:** Defect. The absence of future interactions doesn't change the immediate payoff advantage.
- **Any Round:** Defect regardless of others' history, as the immediate gain from defecting is always superior.

**3. Aggressive Mindset:**
This strategy embodies an aggressive approach by prioritizing self-interest over collective welfare. It capitalizes on any cooperation by others, ensuring maximum personal gain without contributing to the public good.

**Pseudocode:**
```
def strategy():
    for each round in 1 to r:
        action = D
        return action
```

This strategy is robust and adaptive only in its unwavering commitment to defecting, ensuring it performs optimally against any opponent behavior.
'''

description_AGGRESSIVE_26 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we combine responsiveness to others' actions with self-interest, particularly in the final round. The strategy encourages cooperation initially and adapts based on others' behavior, defecting when cooperation is insufficient. In the last round, it defects to maximize immediate gain without future repercussions.

**Strategy: "Aggressive Responsive Cooperative (ARC)"**

**1. Decision Rules:**
   - **First Round:** Always Cooperate (C) to set a cooperative tone and encourage others.
   - **Middle Rounds (2 to r-1):** Cooperate if at least `k` players Cooperated in the previous round; otherwise, Defect (D).
   - **Last Round:** Always Defect to exploit any remaining cooperation without future consequences.

**2. Edge Cases:**
   - **First Round:** Start with Cooperation to potentially induce others to Cooperate.
   - **Last Round:** Defect to maximize immediate gain since future punishment is irrelevant.
   
**3. Pseudocode Implementation:**

```python
def aggressive_strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return "C"
    elif len(history) == r - 1:  # Last round
        return "D"
    else:
        previous_c = sum(history[-1])  # Number of cooperators in last round
        if previous_c >= k:
            return "C"
        else:
            return "D"
```

**Explanation:**
- **First Round Cooperation:** Initiates cooperation to observe others' willingness.
- **Responsive Cooperation:** Continues cooperating as long as at least `k` players cooperate, fostering a productive environment.
- **Strategic Defection:** Defects when cooperation drops below `k`, protecting against exploitation.
- **Final Round Exploitation:** Defects in the last round to maximize individual payoff without future repercussions.

This strategy balances cooperation with aggressive self-interest, adapting to others' actions while prioritizing its own payoff.
'''

description_AGGRESSIVE_27 = '''
**Aggressive Strategy for the N-Player Public Goods Game**

**Decision Rules:**
1. **Always Defect:** The optimal strategy is to choose "D" (Defect) in every round. This is because defecting yields a higher individual payoff than cooperating, regardless of the actions of other players. The mathematical analysis shows that defecting provides a consistently higher payoff by a margin of 1 unit compared to cooperating.

2. **Handling Edge Cases:**
   - **First Round:** Defect. With no prior history, starting with defection ensures the maximum possible payoff.
   - **Last Round:** Defect. Since the game does not extend beyond the last round, there is no incentive to cooperate as future repercussions are absent.

**Rationale:**
The aggressive strategy is grounded in the game's payoff structure, where defecting always provides a higher individual payoff than cooperating, irrespective of others' actions. This approach maximizes the player's payoff without relying on others' cooperation, making it robust and optimal for all rounds.

---

**Pseudocode:**

```
function strategy(n, k, r, history) {
    // history is an array of past actions (C/D) for each player per round
    // Since the strategy is to always defect, we ignore history
    return "D"
}
```

**Explanation:**
The strategy is simple—always defect to maximize individual payoff in each round, leveraging the game's structural advantage that defecting yields a higher payoff than cooperating under any circumstances.
'''

description_AGGRESSIVE_28 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we focus on maximizing individual payoff while considering the game's parameters and history. The strategy adapts based on the number of cooperators in the previous round, ensuring that cooperation is only chosen when it provides a net benefit.

### Strategy Name: Cautious Exploitation

---

### Decision Rules:

1. **First Round**: Cooperate to initiate potential cooperation and encourage others to contribute to the public good.

2. **From Round 2 to Round r-1**:
   - Calculate the number of Cooperators in the previous round (C_prev).
   - If C_prev > n/k, where n is the number of players and k is the multiplication factor, then Cooperate. This is because the public good's return exceeds the individual cost.
   - Otherwise, Defect to maximize your immediate payoff.

3. **Last Round (Round r)**: Always Defect, as there are no future rounds to influence, making Cooperation individually disadvantageous.

---

### Pseudocode:

```python
def cautious_exploitation(n, k, r, history):
    if len(history) == 0:
        return "C"
    else:
        prev_coops = sum(1 for action in history[-1] if action == "C")
        if prev_coops > n / k:
            if len(history) == r - 1:
                return "D"
            else:
                return "C"
        else:
            return "D"
```

---

### Explanation:

- **First Round**: Starting with Cooperation sets a baseline for potential mutual cooperation, which can lead to higher payoffs if others follow suit.
- **Adaptive Strategy**: By checking the previous round's cooperation level, the strategy ensures that we only Cooperate when it's individually beneficial. This balances exploitation of others' cooperation with maintaining some level of public good contribution.
- **Last Round**: Defecting ensures maximum personal gain without future repercussions, aligning with an aggressive mindset.

This strategy is robust and adaptive, responding to the actions of others while focusing on maximizing individual payoff, making it suitable for competitive environments.
'''

description_AGGRESSIVE_29 = '''
To design an aggressive strategy for the N-player public goods game, the approach focuses on maximizing individual payoff by adapting to the collective behavior of other players, while being cautious in critical rounds. Here's the structured strategy:

1. **First Round**: Defect. Since there's no prior information, the strategy starts by maximizing immediate payoff.

2. **Intermediate Rounds (Rounds 2 to r-1)**: 
   - Calculate the average cooperation rate from all previous rounds.
   - If this average meets or exceeds the threshold (1/k), where k is the multiplication factor, cooperate; otherwise, defect.

3. **Last Round (Round r)**: Defect. With no future interactions, the strategy prioritizes immediate payoff.

**Decision Rules**:
- **Cooperate** if the past average cooperation rate is at least 1/k.
- **Defect** otherwise, including in the first and last rounds.

**Pseudocode**:

```
Initialize total_cooperators = 0

For each round t from 1 to r:
    if t == 1:
        action = D
    elif t == r:
        action = D
    else:
        avg_cooperators = total_cooperators / (n * (t - 1))
        if avg_cooperators >= 1/k:
            action = C
        else:
            action = D
    execute action and update total_cooperators with current round's data
```

This strategy is aggressive, adaptive, and robust, ensuring maximum payoff by leveraging past behavior without assuming others' cooperation.
'''

description_AGGRESSIVE_31 = '''
**Strategy: Adaptive Aggressive Cooperation (AAC)**

1. **Decision Rules:**
   - **First Round:** Cooperate (C).
   - **Subsequent Rounds:** 
     - Cooperate if the number of players who cooperated in the previous round is greater than n/k.
     - Defect (D) otherwise.
   - **Last Round:** Always Defect (D).

2. **Edge Cases Handling:**
   - **First Round:** Initiate with cooperation to encourage initial group contribution.
   - **Last Round:** Defect to maximize personal payoff without future repercussions.

3. **Aggressive Mindset:**
   - Punishes lack of sufficient cooperation by defecting, incentivizing others to contribute more.
   - Capitalizes on the last round's lack of future consequences to maximize personal gain.

**Pseudocode:**

```
def AAC_strategy():
    if current_round == 1:
        action = 'C'
    else:
        prev_coop = count_of_cooperations_previous_round
        threshold = n / k
        if prev_coop > threshold:
            action = 'C'
        else:
            action = 'D'
    if current_round == r:
        action = 'D'
    return action
```

This strategy is designed to adapt to others' behaviors, encouraging cooperation while avoiding exploitation, aligning with an aggressive yet rational approach.
'''

description_AGGRESSIVE_32 = '''
To design an aggressive, adaptive, and robust strategy for the N-Player Public Goods Game, the following approach is crafted based on the game's parameters and history. This strategy balances maximizing individual payoffs with encouraging cooperation when beneficial, adapting as the game progresses.

---

### **Aggressive Strategy: "Adaptive K-Threshold Cooperate"**

#### **Decision Rules:**
1. **First Round:**
   - **Action:** Cooperate (C)
   - **Reason:** Initiate cooperation to gauge others' behavior and encourage a cooperative norm.

2. **Intermediate Rounds (Rounds 2 to r-1):**
   - **Action:** Cooperate if the number of players who Cooperated in the previous round (s_{t-1}) is at least k; otherwise, Defect.
   - **Reason:** Reward sufficient cooperation and punish insufficient contribution, ensuring a balance between personal gain and group benefit.

3. **Last Round (Round r):**
   - **Action:** Defect (D)
   - **Reason:** Since there are no future rounds, maximize immediate payoff by Defecting.

#### **Edge Cases Handling:**
- **First Round:** Starts with Cooperation to set a positive tone.
- **Last Round:** Resorts to Defection to maximize individual payoff.
- **Round Transition:** Uses the previous round's cooperation level to decide the next move, ensuring adaptability.

#### **Aggressive Mindset:**
This strategy embodies an aggressive approach by swiftly switching to Defection when cooperation levels drop below the threshold k, emphasizing self-interest while remaining responsive to others' actions.

---

### **Pseudocode**

```python
def strategy(n, k, r, history):
    if not history:  # First round
        return "C"
    
    current_round = len(history) + 1
    
    if current_round == r:  # Last round
        return "D"
    
    # Count number of Cooperators in the previous round
    s_previous = sum(1 for action in history[-1]["actions"] if action == "C")
    
    if s_previous >= k:
        return "C"
    else:
        return "D"
```

### **Conclusion**
This strategy, **"Adaptive K-Threshold Cooperate,"** provides a balanced yet aggressive approach. It begins with cooperation to foster a positive group dynamic, adapts based on previous rounds' outcomes, and prioritizes individual gain when cooperation is deemed insufficient, particularly in the final round. This ensures robust performance across various tournament scenarios.
'''

description_OPPORTUNISTIC_1 = '''
To address the N-Player Public Goods Game, an opportunistic strategy that adapts based on the game's history and parameters is essential. The strategy balances cooperation to encourage group benefits while safeguarding against exploitation by defectors, especially in the final round.

### Strategy Description

1. **First Round:** Cooperate. This sets a positive tone, encouraging others to reciprocate.

2. **Middle Rounds (2 to r-1):** Cooperate if at least `floor(n/k) + 1` players cooperated in the previous round. This threshold ensures cooperation is beneficial given the public good returns.

3. **Last Round (r):** Always Defect. Since there are no future consequences, prioritize individual gain.

This approach encourages cooperation while pragmatically defecting when beneficial.
'''

description_OPPORTUNISTIC_2 = '''
**Opportunistic Strategy: "Adaptive Reciprocity with Aspiration"**

**1. Initial Cooperation:**
- **Action:** Cooperate in the first round to establish a baseline of cooperation and encourage others to reciprocate.

**2. Reciprocal Response:**
- **Mechanism:** Calculate the average cooperation rate of other players in the previous round.
  - If the average is above a threshold (e.g., 50%), continue cooperating.
  - If below, defect in the next round.

**3. Aspiration-Based Adjustment:**
- **Function:** Maintain an aspiration level based on recent payoffs.
  - If current payoff is below aspiration, defect next round to improve payoff.
  - Adjust aspiration dynamically; it increases slightly with each defect and decreases with cooperation.

**4. Exploitation Detection:**
- **Check:** Monitor the opponent's defect rate. If it exceeds a threshold (e.g., 70% of the time), defect to avoid being exploited.
- **Retaliation:** Defect for a set number of rounds if exploited in recent history.

**5. Final Round Strategy:**
- **Action:** In the last round, defect if total payoff meets an acceptable threshold; otherwise, continue reciprocal strategy.

**6. Payoff Maximization:**
- **Opportunism:** Cooperate if it increases personal payoff without being exploited, ensuring self-interest is served when safe.

**Strengths:**
- Balances initial trust with adaptive responses.
- Protects against exploitation while encouraging cooperation.
- Dynamically adjusts based on game outcomes and player behavior.

**Considerations:**
- Potential for being too forgiving if others don't reciprocate.
- Aspiration level adjustment may need refinement based on game dynamics.

This strategy promotes cooperation while safeguarding against exploitation, making it a robust and adaptive approach for the tournament.
'''

description_OPPORTUNISTIC_3 = '''
To address the public goods game, an Opportunistic Strategy is proposed, balancing cooperation and exploitation to maximize individual payoff while adapting to others' behavior. Here's the structured approach:

### Strategy Overview

1. **Initial Cooperation**: Start by cooperating in the first round to encourage potential reciprocal behavior.

2. **Adaptive Decision-Making**:
   - **Cooperation Threshold**: After the first round, cooperate if the number of cooperators in the previous round exceeds a threshold calculated as (k-1)/n. This threshold incentivizes cooperation when sufficiently beneficial.
   - **Defection**: If the number of cooperators falls below the threshold, defect to avoid exploitation.

3. **Opportunistic Exploitation**: With a probability based on the formula (n - k)/n, defect even when others are cooperating. This probabilistic approach allows exploitation without making the strategy overly aggressive.

4. **Last Round Adjustment**: Defect in the final round to maximize immediate payoff, as future consequences are absent.

### Strategy Details

- **Decision Rules**:
  - **First Round**: Cooperate to test others' willingness.
  - **Subsequent Rounds**: Cooperate if previous round's cooperators meet the threshold; otherwise, defect.
  - **Exploitation Probability**: (n - k)/n chance to defect beyond the threshold-based decision.

- **Edge Cases**:
  - **First Round**: Initial cooperation.
  - **Last Round**: Defect to maximize immediate gain.

This strategy is designed to adapt to others' actions, encouraging cooperation when beneficial while opportunistically exploiting for higher payoffs. It balances reciprocity with self-interest, fitting the requirements of being adaptive and robust against various behaviors.
'''

description_OPPORTUNISTIC_4 = '''
### Opportunistic Strategy for the N-Player Public Goods Game

#### 1. Decision Rules:
The strategy is designed to balance cooperation and self-interest, adapting based on the history of the game. It uses a form of **reciprocity** and **opportunism** to maximize the player's payoff while encouraging cooperation when beneficial.

- **First Round:** Cooperate (C). This establishes a baseline of cooperation and observes the behavior of others.
- **Subsequent Rounds:** Use the following rule:
  - Cooperate (C) if:
    - The number of cooperators in the previous round was greater than or equal to a threshold \( T \), where \( T = \frac{k}{2} \). This means that at least half of the "economic benefits" of cooperation (scaled by \( k \)) are being contributed by others.
    - The average payoff in the previous round was greater than or equal to a threshold \( P \), where \( P = 1 + \frac{k}{2} \). This ensures that the benefits of cooperation are sufficiently high.
  - Defect (D) otherwise. This avoids being exploited when cooperation is not yielding sufficient benefits.

#### 2. Handling Edge Cases:
- **First Round:** Always cooperate to establish a cooperative tone and gather information about other players' behavior.
- **Last Round (Round r):** Defect (D). In the last round, there is no future punishment or reward, so the strategy prioritizes maximizing immediate payoff.
- **If All Players Defected in the Previous Round:** Cooperate (C) to attempt to reinitiate cooperation. This is a form of **forgiveness** and opportunism, allowing the possibility of restarting cooperation.
- **If Payoffs Are Very Low:** If the average payoff in the previous round was less than 1, defect (D). This avoids perpetuating a strategy that is not yielding benefits.

#### 3. Opportunistic Alignment:
The strategy is opportunistic because it seeks to maximize the player's payoff by:
- Cooperating when cooperation is likely to yield higher payoffs (i.e., when enough others are cooperating).
- Defecting when cooperation is not paying off (i.e., when few others are cooperating or the benefits are too low).
- Being forgiving by occasionally cooperating even after Others have defected, to potentially restart cooperation.

### Pseudocode Representation:
```python
def strategy(n, k, r, history):
    if len(history) == 0:  # First round
        return "C"
    else:
        # Get previous round's data
        prev_round = history[-1]
        num_cooperators = prev_round["num_cooperators"]
        avg_payoff = prev_round["avg_payoff"]
        
        # Calculate thresholds
        T = k / 2
        P = 1 + k / 2
        
        if avg_payoff >= P and num_cooperators >= T:
            return "C"
        else:
            # Check if all defected last round
            if num_cooperators == 0:
                return "C"  # Forgive and try to restart cooperation
            else:
                # Last round
                if len(history) == r - 1:
                    return "D"
                else:
                    return "D"
```

### Explanation:
- **First Round:** The strategy starts by cooperating to establish a cooperative baseline and observe others' behavior.
- **Subsequent Rounds:** It uses the number of cooperators and the average payoff from the previous round to decide whether to cooperate or defect. This ensures that cooperation is only maintained if it is beneficial and if enough others are also cooperating.
- **Last Round:** The strategy defects in the last round to maximize immediate payoff, as there is no future punishment or reward.
- ** Forgiveness Mechanism:** If all players defected in the previous round, the strategy will cooperate again in an attempt to restart cooperation. This is a form of strategic forgiveness to potentially improve future payoffs.

This strategy is robust because it adapts to the behavior of others while maintaining a focus on maximizing the player's own payoff. It does not rely on any specific coordination mechanisms or shared norms, making it suitable for a tournament setting where opponents may employ a wide range of strategies.
'''

description_OPPORTUNISTIC_5 = '''
To design an opportunistic strategy for the N-player public goods game, we need a approach that adapts based on past behavior and game parameters. The strategy should balance cooperation and defection to maximize payoff while considering the game's social dynamics.

### Strategy: Opportunistic Cooperation with Threshold

1. **Decision Rules**:
    - **First Round**: Cooperate to set a positive tone and encourage initial cooperation.
    - **Intermediate Rounds (2 to r-1)**: Calculate the average cooperation rate from all previous rounds. If this average meets or exceeds a threshold (k/n), continue to Cooperate. If not, Defect to avoid being exploited.
    - **Last Round**: Always Defect, as there’s no future reciprocity to influence.

2. **Handling Edge Cases**:
    - **First Round**: Cooperate to establish cooperation.
    - **Last Round**: Defect to maximize immediate payoff.

3. **Opportunistic Mindset**:
    - The strategy opportunistically adapts by cooperating when others demonstrate sufficient cooperation and defecting when they don’t. This approach aims to leverage the public good's benefits while avoiding exploitation.

### Pseudocode

```python
def opportunistic_strategy(n, r, k, current_round, total_C, rounds_done):
    if current_round == 1:
        action = 'C'
    elif current_round == r:
        action = 'D'
    else:
        if rounds_done == 0:
            action = 'C'
        else:
            avg_cooperation = total_C / (n * rounds_done)
            threshold = k / n
            if avg_cooperation >= threshold:
                action = 'C'
            else:
                action = 'D'
    return action

# Initialize variables
total_C = 0
rounds_done = 0

for t in range(1, r + 1):
    action = opportunistic_strategy(n, r, k, t, total_C, rounds_done)
    # Execute action
    if action == 'C':
        this_C = 1
    else:
        this_C = 0
    # After the round, update totals (assuming you can observe all players' actions)
    # This part is hypothetical since in reality, each player acts independently
    total_C += sum_of_all_C_in_current_round
    rounds_done += 1
```

This strategy dynamically adjusts, promoting cooperation when beneficial and defecting when necessary, ensuring a robust and adaptive approach to maximize individual payoff.
'''

description_OPPORTUNISTIC_6 = '''
To address the challenge of designing an opportunistic strategy for the N-player public goods game, we need to create a strategy that adapts based on game parameters and the history of others' actions. The strategy should maximize the player's total payoff while being robust against various opponent behaviors.

### Strategy Definition: "Adaptive Cooperation Threshold (ACT)"

#### 1. Decision Rules:
- **First Round**: Cooperate to set a cooperative tone and encourage others to cooperate.
- **Subsequent Rounds (2 to r-1)**:
  - Calculate the number of cooperators in the previous round, denoted as \( c_{t-1} \).
  - Determine the threshold \( T \) using the formula \( T = \lceil n/k \rceil \), where \( \lceil x \rceil \) denotes the smallest integer greater than or equal to \( x \).
  - If \( c_{t-1} \geq T \), Cooperate. Otherwise, Defect.
- **Last Round**: Always Defect, as there is no future consequence for current actions.

#### 2. Handling Edge Cases:
- **First Round**: Cooperate to maximize initial public good.
- **Last Round**: Defect to secure a guaranteed payoff.
- **Intermediate Rounds**: Use the threshold \( T \) to decide based on past cooperation levels.

#### 3. Opportunistic Approach:
- The strategy is opportunistic as it seeks to maximize personal gain by cooperating only when it is beneficial, determined by the threshold based on the game's parameters and past behavior.

### Pseudocode Implementation:

```python
def adaptive_cooperation_threshold(n, k, r, history):
    """
    Strategy for the N-player public goods game.
    
    Parameters:
    - n: Number of players
    - k: Multiplication factor
    - r: Number of rounds
    - history: List of previous rounds' cooperation counts
    
    Returns:
    - Action: 'C' (Cooperate) or 'D' (Defect)
    """
    current_round = len(history) + 1  # 1-based index
    
    if current_round == 1:
        return 'C'
    elif current_round == r:
        return 'D'
    else:
        prev_c = history[-1]  # Number of cooperators in the previous round
        threshold = (n + k - 1) // k  # Equivalent to ceiling(n/k)
        if prev_c >= threshold:
            return 'C'
        else:
            return 'D'

# Example usage
n = 6
k = 2
r = 10
history = [3, 4, 5]  # Example history of cooperation counts
print(adaptive_cooperation_threshold(n, k, r, history))  # Output: 'C' if prev_c >= 3, else 'D'
```

### Strategy Explanation:
- **First Round Cooperation**: Initiates cooperation to potentially encourage others.
- **Threshold Calculation**: Dynamically adjusts based on \( n \) and \( k \), ensuring cooperation is beneficial.
- **Adaptive Decision Making**: Uses past cooperation levels to inform current decisions, promoting flexibility.
- **Final Round Defection**: Maximizes personal gain in the last round without future repercussions.

This strategy is designed to balance cooperation and self-interest, adapting to the game's dynamics to maximize total payoff.
'''

description_OPPORTUNISTIC_8 = '''
**Strategic Approach for N-Player Public Goods Game**

1. **Initial Cooperation**:
   - **First Round**: Cooperate (C) to set a cooperative tone and encourage others to follow suit.

2. **Adaptive Cooperation Based on History**:
   -_SEGMENTARY COOPERATION EVALUATION_:
     - Track the number of players who Cooperated (C) in the previous round.
     - If the proportion of Cooperators in the previous round exceeds a dynamic threshold (initially set at 50% and adjusted downward as the game progresses), Cooperate in the current round.

3. **Dynamic Threshold Adjustment**:
   - **Threshold Mechanism**: Begin with a high threshold (e.g., 50%) and reduce it incrementally each round by a small percentage (e.g., 5%) to adapt to potential waning cooperation over time.

4. **Opportunistic Defection**:
   - Introduce stochastic defection (e.g., 10% chance) even when the cooperation threshold is met. This deters others from exploiting consistent cooperation and allows testing of others' Strategies.

5. **Final Rounds Strategy**:
   - In the last few rounds (e.g., last 3 rounds), only Cooperate if a significant majority (e.g., 75%) Cooperated in the previous round. Otherwise, Defect to capitalize on the last opportunities without future repercussions.

6. **Handling Edge Cases**:
   - If all or most players Defected in the previous round, Defect to maximize personal payoff.
   - If all Cooperated, continue Cooperating to maintain high public good benefits.

7. **Pseudocode Representation**:

   ```pseudocode
   Initialize threshold = 0.5
   For each round from 1 to r:
       If first round:
           Choose C
       Else:
           cooperation_rate = (number of C in previous round) / n
           threshold = max(threshold - 0.05, 0)
           If cooperation_rate > threshold and (random < 0.9):
               Choose C
           Else:
               Choose D
           // Cautious defect in last few rounds:
           If round > r - 3:
               If cooperation_rate < 0.75:
                   Choose D
   ```

This strategy balances cooperation and opportunism, adapting to group dynamics while safeguarding against exploitation, particularly in the game's final stages.
'''

description_OPPORTUNISTIC_9 = '''
To solve the N-Player Public Goods Game, we'll use a threshold-based strategy that balances cooperation with strategic defection, especially in the final round. This approach ensures adaptability and robustness against varying opponent behaviors.

### Strategy Design:

1. **First Round:** Cooperate to encourage initial contribution and maximize potential collective benefit.

2. **Rounds 2 to r-1:** Use a threshold based on the multiplication factor, k. Specifically, if the number of cooperators in the previous round meets or exceeds \( T = \lceil n/k \rceil \), cooperate again. Otherwise, defect to avoid being exploited.

3. **Last Round (Round r):** Defect to maximize immediate payoff, as future reciprocity isn't possible.

### Pseudocode:

```python
def decide_action(prev_rounds, current_round, n, k):
    if current_round == 1:
        return "C"
    elif current_round == r:
        return "D"
    else:
        prev_c = count_cooperators(prev_rounds[-1])
        threshold = math.ceil(n / k)
        if prev_c >= threshold:
            return "C"
        else:
            return "D"
```

### Explanation:

- **First Round:** Starting with cooperation can foster a positive group dynamic, potentially leading to higher collective payoffs.
- **Subsequent Rounds:** By basing cooperation on the threshold \( T = \lceil n/k \rceil \), the strategy adapts to the group's behavior, rewarding sufficient cooperation and penalizing insufficient it.
- **Last Round:** Defecting in the final round ensures maximizing immediate gain, as there's no future interaction to influence.

This strategy is both adaptive and opportunistic, aligning actions to maximize individual payoff while considering the game's parameters and history.
'''

description_OPPORTUNISTIC_10 = '''
**Opportunistic Strategy for the N-Player Public Goods Game**

**1. Decision Rules:**
- **First Round:** Cooperate (C) to potentially encourage others to cooperate, establishing a cooperative precedent.
- **Intermediate Rounds (2 to r-1):** Cooperate in round t if the number of cooperators in the previous round (t-1) is at least the threshold ρ, where ρ = ceil(n/k). If the number is below ρ, defect (D).
- **Last Round (r):** Defect (D) to maximize personal payoff, knowing there are no future consequences.

**2. Edge Cases:**
- **First Round:** Always cooperate to initiate cooperation.
- **Last Round:** Always defect to secure the highest possible personal payoff in the final round without concern for future repercussions.

**3. Opportunistic Mindset:**
- **Encourage Early Cooperation:** By starting with cooperation, it may induce others to follow suit, increasing the public good.
- **Adaptive Cooperation:** Cooperate only when others have sufficiently done so, ensuring that the effort isn't unilateral.
- **Maximize Payoff in Endgame:** In the last round, prioritize personal gain, defecting to exploit any remaining cooperation.

This strategy balances between fostering cooperation early on and defecting when it becomes advantageous, particularly in the last round. It's adaptive, responding to the level of cooperation observed, and robust against various opponent behaviors.

**Pseudocode:**

```
def strategy(n, k, r, history):
    current_round = len(history) + 1
    if current_round == 1:
        return 'C'
    elif current_round == r:
        return 'D'
    else:
        c_last = sum(1 for action in history[-1] if action == 'C')
        threshold = math.ceil(n / k)
        if c_last >= threshold:
            return 'C'
        else:
            return 'D'
```

This strategy is designed to capitalize on cooperation when beneficial and defect when it maximizes individual gain, ensuring opportunism and adaptability.
'''

description_OPPORTUNISTIC_11 = '''
### Opportunistic Strategy for N-Player Public Goods Game

**Overview:**  
This strategy is designed to maximize individual payoff while being adaptive to the behavior of other players. It balances cooperation and defection in a way that leverages the benefits of public goods while avoiding exploitation.

---

### **1. Decision Rules**
The strategy adapts based on the observed behavior of other players and the current round's progress. The key is to cooperate when cooperation is mutually beneficial and defect when others are not contributing sufficiently. The decision rules are as follows:

#### **Initial Round (Round 1):**
- Cooperate (C) in the first round to establish a cooperative tone and encourage others to reciprocate.

#### **Intermediate Rounds (Round 2 to Round r-1):**
1. **Monitor Contributions:** Track the total number of players who cooperated (i.e., the sum of \( c_j \)) in the previous round. Let this be denoted as \( S_{t-1} \), where \( t \) is the current round.
2. **Calculate Threshold:** Compute a threshold \( \theta \) based on the game parameters:
   \[
   \theta = \frac{k}{n} \times (1 + \alpha)
   \]
   where \( \alpha \) is a small positive parameter (e.g., 0.1) to account for uncertainty and encourage cooperation.
3. **Cooperate or Defect:**
   - If the number of cooperators in the previous round (\( S_{t-1} \)) is greater than or equal to \( \theta \), cooperate (C) in the current round. This indicates that cooperation is paying off.
   - If \( S_{t-1} \) is less than \( \theta \), defect (D) in the current round. This avoids contributing when others are not reciprocating sufficiently.

#### **Final Round (Round r):**
- Defect (D) in the final round. There is no future punishment or reciprocity to worry about, so free-ride on the contributions of others.

---

### **2. Handling Edge Cases**
- **First Round:** Always cooperate to establish a cooperative baseline.
- **Last Round:** Always defect to maximize immediate payoff without concern for future repercussions.
- **All-Defect Scenarios:** If all players defect consistently, the strategy will also defect to avoid being exploited.
- **All-Cooperate Scenarios:** If all players cooperate consistently, the strategy will continue to cooperate to maximize shared payoffs.

---

### **3. Opportunistic Mindset**
The strategy is designed to capitalize on opportunities for higher payoffs while minimizing losses. It does this by:
1. Cooperating when there is clear evidence that others are also contributing (i.e., \( S_{t-1} \geq \theta \)).
2. Defecting when contributions are low, avoiding the "sucker's payoff" of cooperating while others defect.
3. Exploiting the final round by defecting, as there is no future punishment.

---

### **Pseudocode**
```python
def opportunistic_strategy(player_id, n, k, r, history):
    current_round = len(history) + 1  # 1-based indexing

    if current_round == 1:
        return "C"  # Cooperate in the first round

    if current_round > r:
        return "D"  # Defect in the final round

    # Calculate contributions in the previous round
    S_prev = sum([1 for action in history[-1] if action == "C"])

    # Compute threshold
    alpha = 0.1  # Could be adjusted based on parameters
    theta = (k / n) * (1 + alpha)

    if S_prev >= theta:
        return "C"  # Cooperate if contributions are sufficient
    else:
        return "D"  # Defect if contributions are insufficient

    if current_round == r:
        return "D"  # Always defect in the final round
```

---

### **Rationale**
This strategy aligns with an opportunistic mindset by:
- Starting with cooperation to encourage reciprocity.
- Adapting to the behavior of others, cooperating when contributions are high and defecting when they are low.
- Exploiting the final round to maximize immediate payoff.

By being adaptive and responsive, this strategy is robust to a wide range of opponent behaviors while maintaining the flexibility to capitalize on opportunities for higher payoffs.
'''

description_OPPORTUNISTIC_12 = '''
To address the N-Player Public Goods Game, we designed an opportunistic strategy that adapts based on the game's history and parameters. The strategy is outlined below, including the decision rules and edge case handling.

### Opportunistic Strategy: "Adaptive Cooperation with Punishment"

**1. Decision Rules:**
   - **First Round:** Cooperate to set a cooperative tone and maximize the initial public good.
   - **Subsequent Rounds (2 to r-1):** Cooperate in round t if the number of cooperators in the previous round (C_prev) is greater than n/k. Otherwise, Defect.
   - **Last Round (r):** Cooperate if C_prev from round r-1 is greater than n/k; otherwise, Defect.

**2. Handling Edge Cases:**
   - **First Round:** Always Cooperate.
   - **Last Round:** Decision based on the previous round's cooperation level.
   - **Dynamic Threshold:** Uses n/k as the threshold to determine cooperation, ensuring adaptability based on game parameters.

**3. Opportunistic Mindset:**
   - Balances exploiting others' cooperation and protecting against exploitation through a responsive strategy.

This strategy encourages cooperation when beneficial and defects when necessary, providing a robust approach that doesn't rely on others' strategies but adapts to observed behavior.
'''

description_OPPORTUNISTIC_13 = '''
**Strategic Approach for the N-Player Public Goods Game**

**1. Decision Rules:**

- **Initial Phase (First Round):** Cooperate (C) to establish a cooperative tone and encourage others to contribute.
  
- **Assessment Phase (Rounds 2 to r-2):**
  - Track the cooperation rate (CR) of all players, calculated as the average frequency of cooperation over the previous rounds.
  - If CR is above a threshold (e.g., 75%), start defecting with increasing probability to exploit others' cooperation.
  - If CR is below the threshold, continue cooperating or adjust based on the trend in CR.

- **Forgiveness Mechanism:** If CR increases after a period of low cooperation, revert to cooperating to encourage mutual cooperation.

- **Endgame Phase (Last Round, r):** Defect (D) to maximize personal gain, as future interactions are limited.

**2. Edge Cases Handling:**

- **First Round:** Cooperate to set a positive tone.
- **Last Round:** Defect to prioritize personal gain.
- Adjustments are made based on observed cooperation trends, allowing the strategy to adapt dynamically.

**3. Opportunistic Alignment:**

- The strategy maximizes personal payoff by initially encouraging cooperation and then exploiting it when beneficial.
- It adapts based on others' actions, balancing cooperation and defection to avoid being exploited while taking advantage of others' contributions.

**Pseudocode Outline:**

```
def strategy(n, k, r, history):
    if current_round == 1:
        return "C"
    else:
        cr = calculate_cooperation_rate(history)
        if cr > threshold:
            prob_defect = (1 - (cr / n)) * 0.5
            return "D" with probability prob_defect
        else:
            return "C"
    if current_round == r:
        return "D"

def calculate_cooperation_rate(history):
    # Compute average cooperation of all players
    pass

threshold = 0.75  # Adjust based on k and n
```

**Conclusion:**

This strategic approach is designed to be adaptive and opportunistic, encouraging initial cooperation and dynamically adjusting based on others' behavior to maximize personal payoff while remaining robust against exploitation.
'''

description_OPPORTUNISTIC_15 = '''
**Opportunistic Strategy for N-Player Public Goods Game**

**1. Decision Rules:**
- **First Round:** Always Cooperate (C). This sets a cooperative tone and maximizes group payoff from the start.
- **Middle Rounds (2 to r-1):** Cooperate in the current round if the number of cooperators in the previous round (C_prev) exceeds the threshold n/k. If C_prev ≤ n/k, Defect (D).
- **Last Round (r):** Always Defect (D) to maximize individual payoff in the final interaction.

**2. Edge Cases Handling:**
- **First Round Handling:** Cooperate to initiate potential cooperation.
- **Last Round Handling:** Defect to ensure maximum personal gain without future repercussions.

**3. Opportunistic Mindset:**
- The strategy seeks to exploit cooperation when beneficial, switching to defection when contributions are insufficient, ensuring the player maximizes their payoff without being exploited.

**Pseudocode:**

```
def strategy(n, k, r, history):
    current_round = len(history) + 1
    
    if current_round == 1:
        return "C"
    
    if current_round == r:
        return "D"
    
    prev_round = history[-1]
    C_prev = sum(1 for action in prev_round if action == "C")
    
    threshold = n / k
    
    if C_prev > threshold:
        return "C"
    else:
        return "D"
```

This strategy is adaptive, robust, and designed to maximize the player's payoff by cooperating when it's mutually beneficial and defecting otherwise, ensuring opportunism and adaptability in a competitive environment.
'''

description_OPPORTUNISTIC_16 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, we focus on a balance between encouraging cooperation when beneficial and defecting when cooperation is insufficient. The strategy adapts to past actions and game parameters, ensuring robustness and self-interest.

### Strategy: Adaptive Opportunism

**1. Decision Rules:**
- **First Round:** Cooperate to initiate potential cooperation.
- **Middle Rounds (2 to r-1):** Cooperate if the number of cooperators in the previous round meets or exceeds a threshold (T). Otherwise, Defect.
- **Last Round (r):** Always Defect, as there’s no future punishment.

**2. Handling Edge Cases:**
- In the **first round**, the strategy starts by Cooperating to encourage collective cooperation.
- In the **last round**, the strategy defects to maximize personal payoff without repercussions.

**3. Opportunistic Mindset:**
The strategy leverages others' cooperation when beneficial, switching to defecting when cooperation is low or in the final round. This balance allows the player to exploit cooperation while protecting against exploitation.

**Pseudocode:**
```python
Initialize history as empty list.

For each round t from 1 to r:
    if t == 1:
        action = 'C'
    elif t == r:
        action = 'D'
    else:
        T = ceil(n / k)
        TotalC_prev = number of 'C' in history[-1]
        if TotalC_prev >= T:
            action = 'C'
        else:
            action = 'D'
    add action to history
```

This strategy is both adaptive and robust, adjusting based on game parameters and past behavior to maximize individual payoffs while considering collective outcomes.
'''

description_OPPORTUNISTIC_17 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, we must balance exploiting others' cooperation with maintaining contributions to the public good to maximize our own payoff. Here's the strategy:

### Opportunistic Strategy

1. **Initial Cooperation**: Cooperate in the first round to encourage others to cooperate and set a positive tone.

2. **Adaptive Decision-Making**:
   - For each subsequent round, calculate the number of players who cooperated in the previous round (C_prev).
   - If C_prev is greater than or equal to n/k, defect in the current round to exploit the existing high level of cooperation.
   - If C_prev is less than n/k, cooperate to help increase the public good, encouraging others and potentially higher future payoffs.

3. **Last Round Defection**: In the final round, always defect since there are no future consequences, allowing you to maximize your payoff without concern for retaliation.

This strategy is adaptive, robust, and designed to be opportunistic, aiming to maximize individual payoff by leveraging others' cooperation while strategically contributing to maintain the public good when beneficial.

### Pseudocode Implementation

```python
def opportunistic_strategy(game_params, history):
    n = game_params['n']
    k = game_params['k']
    r = game_params['r']
    current_round = history['current_round']
    
    if current_round == 1:
        return "C"  # Cooperate in the first round
    else:
        # Get previous round's data
        previous_round = history['round_' + str(current_round - 1)]
        C_prev = previous_round['num_cooperators']
        threshold = n / k
        
        if C_prev >= threshold:
            return "D"  # Defect if enough cooperated previously
        else:
            return "C"  # Cooperate to encourage public good
    
    # Last round handling
    if current_round == r:
        return "D"  # Always defect in the last round
```

This strategy effectively balances between cooperation and defection to maximize individual gain while considering the game's dynamics and parameters.
'''

description_OPPORTUNISTIC_18 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, we focus on maximizing individual payoffs by cooperating only when it's beneficial, based on the previous round's cooperation level. Here's how the strategy works:

### Opportunistic Strategy:

1. **First Round**: Cooperate to set a cooperative tone.

2. **Subsequent Rounds**: 
   - After each round, count the number of players who cooperated (m_prev).
   - If (k/n) * m_prev ≥ 1, cooperate in the next round.
   - Otherwise, defect.

This strategy is opportunistic because it seizes the opportunity to cooperate when the public good's benefit outweighs the cost of cooperation, ensuring adaptability and robustness against various behaviors.

### Pseudocode:
```
Initialize: Cooperate in the first round.

For each round from 2 to r:
   Calculate m_prev = number of cooperators in the previous round.
   Calculate threshold = (k / n) * m_prev.
   If threshold >= 1:
      Cooperate.
   Else:
      Defect.

No special handling for the last round; strategy continues as above.
```

This approach ensures that the strategy adapts based on prior cooperation levels, maximizing individual payoffs while maintaining robustness.
'''

description_OPPORTUNISTIC_19 = '''
**Opportunistic Strategy for N-Player Public Goods Game**

**1. Decision Rules:**
   - **Initial Rounds (First 3 Rounds):** Cooperate (C) to initiate and gather information on other players' tendencies.
   - **Subsequent Rounds:** Calculate the average number of Cooperators (C) from the last 3 rounds. If this average is greater than or equal to n/k, Cooperate; otherwise, Defect (D). Additionally, if the average payoff from the last 3 rounds is below a threshold (e.g., 1.5), switch to Defecting more frequently to exploit others or protect against low payoffs.
   - **Last Round:** Always Defect to maximize immediate payoff without future repercussions.

**2. Edge Cases and Handling:**
   - **First Few Rounds:** Start with Cooperation to establish a cooperative environment and observe others' strategies.
   - **Last Round:** Defect to secure the highest possible payoff in the final round.
   - **Low Payoff Scenario:** If the average payoff falls below a set threshold, shift towards Defecting to improve individual gains.

**3. Opportunistic Approach:**
   - The strategy is designed to adapt based on recent game history, focusing on maximizing individual payoffs by leveraging others' cooperation when beneficial and defecting when it's advantageous or necessary.
   - Use a moving average of cooperation rates and payoffs to make timely, informed decisions, ensuring the strategy remains robust against diverse opponent behaviors.

**Pseudocode Outline:**

```
Initialize:
    cooperate_count = 0
    total_payoff = 0
    history = []
    threshold = n / k
    m = 3  # number of recent rounds to consider

For each round t in 1 to r:
    if t <= 3:
        action = C
    else:
        recent_coop_avg = average number of Cooperators in last m rounds
        recent_payoff_avg = average payoff in last m rounds
        if recent_coop_avg >= threshold and recent_payoff_avg >= 1.5:
            action = C
        else:
            action = D

    if t == r:
        action = D

    execute action
    update history with action and payoff
    total_payoff += payoff
```

This strategy is adaptive, robust, and opportunistic, ensuring that the player maximizes their payoff by intelligently switching between Cooperate and Defect based on game dynamics and history.
'''

description_OPPORTUNISTIC_20 = '''
To design an effective strategy for the N-Player Public Goods Game, we'll create an adaptive approach that balances cooperation and defection based on observed behavior. Here's the structured strategy:

### Strategy Name: Adaptive Cooperation with Punishment

#### Strategy Overview:
The strategy is designed to be opportunistic and adaptive, encouraging cooperation while punishing defection. It starts with cooperation to foster a positive environment and adjusts based on the level of cooperation observed in previous rounds.

#### Decision Rules:
1. **First Round:** Always Cooperate. This sets a cooperative tone and encourages others to follow suit.
2. **Subsequent Rounds:**
   - Calculate the average cooperation rate from previous rounds, excluding the first.
   - If the average cooperation rate meets or exceeds a dynamic threshold, Cooperate. The threshold starts at a moderate level and adjusts based on the game's progress.
   - If the average cooperation rate is below the threshold, Defect to signal dissatisfaction and encourage better cooperation.
3. **Last Round:** Always Defect. Since there's no future punishment, maximize immediate payoff.

#### Threshold Adjustment:
- **Dynamic Threshold:** The threshold starts at 50% cooperation. It decreases by 10% each round if cooperation is maintained, rewarding consistent cooperation.
- If cooperation drops below the current threshold, the threshold resets to 50% for the next round.

#### Edge Cases:
- **All Defection Detected:** If all others defect in a round, Defect in the next round to avoid being exploited.
- **High Cooperation Observed:** If a round exceeds the cooperation target, maintain cooperation to maximize collective payoff.

### Pseudocode:

```pseudocode
Initialize:
    total_cooperators = 0
    last_actions = []
    threshold = 0.5  // Starts at 50%
    cooperate_threshold = threshold

For each round from 1 to r:
    if round == 1:
        action = Cooperate
        last_actions.append(action)
        total_cooperators += 1
    else:
        // Calculate average cooperation rate excluding first round
        if round > 1:
            avg_cooperation = (total_cooperators) / (round - 1)
            if avg_cooperation >= cooperate_threshold:
                action = Cooperate
                total_cooperators += 1
            else:
                action = Defect
                // Adjust threshold dynamically
                if avg_cooperation < threshold:
                    threshold = max(0.3, threshold - 0.1)
                else:
                    threshold = min(0.7, threshold + 0.05)
        else:
            // Round 2, handle first round data
            if last_actions[0] == Cooperate:
                action = Cooperate
                total_cooperators += 1
            else:
                action = Defect
        
        // Adjust based on threshold
        cooperate_threshold = threshold

    if round == r:  // Last round
        action = Defect

    record action in last_actions
    update total_cooperators based on action
```

### Explanation:
- **First Round:** Cooperation is initiated to encourage others.
- **Subsequent Rounds:** The strategy adapts by monitoring the average cooperation rate, rewarding continued cooperation and punishing insufficient cooperation.
- **Last Round:** Defaults to Defection to maximize immediate payoff without future repercussions.
- **Dynamic Threshold:** Adjusts based on observed behavior, lowering if cooperation is low and raising if cooperation is high, ensuring the strategy remains responsive and not overly punitive.

This strategy is robust, opportunistic, and designed to maximize individual payoff while encouraging group cooperation through adaptive behavior.
'''

description_OPPORTUNISTIC_21 = '''
**Strategy: Adaptive Opportunism in N-Player Public Goods Game**

**1. Overview:**
This strategy is designed to be adaptive and opportunistic, maximizing individual payoff without relying on others' cooperation. It dynamically adjusts based on previous rounds' outcomes.

**2. Decision Rules:**

- **First Round:** Cooperate unconditionally to encourage initial cooperation.
  
- **Subsequent Rounds:**
  - Calculate the cooperation rate from the previous round.
  - If the cooperation rate exceeds a threshold (e.g., 50%), cooperate; otherwise, defect.
  
- **Last Round:** Defect to maximize individual payoff, as future consequences are absent.

**3. Edge Cases Handling:**
- In the first round, cooperation is initiated to set a cooperative tone.
- The last round is treated as an endgame, prompting a defect to ensure maximum personal gain.

**4. Opportunistic Approach:**
The strategy capitalizes on others' cooperation by continuing to contribute when cooperation is prevalent. It avoids exploitation by defecting when cooperation levels drop, ensuring self-interest is maintained.

**Implementation Considerations:**
- Track cooperation rates dynamically without assuming others' strategies.
- Use a fixed threshold (e.g., 50%) for simplicity and clarity.

This strategy ensures adaptability, leveraging cooperative environments while safeguarding against exploitation, making it robust across various scenarios.
'''

description_OPPORTUNISTIC_22 = '''
The strategy designed for the N-Player Public Goods Game is an adaptive approach that balances cooperation with opportunism, ensuring the player maximizes their payoff while responding to others' actions. Here's how it works:

1. **First Round:**
   - Cooperate to set a positive tone and encourage initial cooperation among players.

2. **Rounds 2 to r-1:**
   - **Majority Cooperation Check:** Cooperate if more than half of the players cooperated in the last round. This encourages continued cooperation when it's beneficial.
   - **Payoff Threshold Check:** If the player's previous payoff was below a threshold (1 + k/2), switch to defection. This ensures the player doesn't consistently receive low payoffs.

3. **Last Round:**
   - Always Defect to maximize the immediate payoff, as there's no future punishment possible.

**Pseudocode:**

```
Initialize:
    history = []  # Stores actions of all players each round
    current_action = 'C'

For each round t from 1 to r:
    if t == 1:
        action = 'C'
    else:
        if t == r:
            action = 'D'
        else:
            total_c_last = count of 'C' in history[-1]
            if total_c_last > n/2:
                if previous_payoff >= 1 + (k / 2):
                    action = 'C'
                else:
                    action = 'D'
            else:
                action = 'D'
    
    record action in history
    receive payoff
    play action and observe results
```

This strategy is adaptive, rewarding cooperation when beneficial and defecting when necessary, ensuring robust performance across various scenarios.
'''

description_OPPORTUNISTIC_23 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, we can create a adaptive approach that balances cooperation and defection based on the game's history. Here's the final strategy:

**Strategy Name: Adaptive Opportunism**

1. **First Round**: Cooperate (C) to attempt to establish a cooperative tone and encourage others to cooperate.

2. **Intermediate Rounds (2 to r-1)**: Calculate the average number of cooperators from all previous rounds. If this average is at least equal to the multiplication factor k, cooperate in the current round. Otherwise, defect.

3. **Last Round**: Always defect (D) since there are no future interactions to influence, maximizing personal payoff.

This strategy is opportunistic because it takes advantage of the situation when others are cooperating, while being cautious and defecting when others are not, thus optimizing personal payoffs while encouraging cooperation when beneficial.

**Pseudocode Explanation:**

```python
def adaptive_opportunism(n, r, k):
    # Initialize
    total_cooperators = []
    
    for t in range(r):
        if t == 0:  # First round (t=0)
            action = 'C'
        elif t == r-1:  # Last round
            action = 'D'
        else:
            # Calculate average cooperator count from previous rounds
            avg_coop = sum(total_cooperators) / (t) if t > 0 else 0
            if avg_coop >= k:
                action = 'C'
            else:
                action = 'D'
        
        # After choosing action, observe the total_cooperators in this round
        # Here, total_cooperators_in_t is the actual count observed
        total_cooperators.append(total_cooperators_in_t)
        
    return actions
```

This approach ensures the strategy is both adaptive and robust, responding to others' behavior while maximizing personal gain.
'''

description_OPPORTUNISTIC_24 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, we have created a rule-based approach that balances cooperation and defection based on the game's history and parameters. This strategy is adaptive, robust, and aligns with an opportunistic mindset, aiming to maximize individual payoffs while encouraging cooperation when beneficial.

### Strategy Design

**Name:** Adaptive Cooperation Threshold (ACT)

**Objective:** Maximize individual payoffs by cooperating when it's beneficial and defecting when it's not, adapting based on the game's history.

#### Decision Rules:
1. **First Round (t = 1):** Cooperate. This encourages initial cooperation and sets a cooperative tone.
2. **Subsequent Rounds (2 ≤ t < r):**
   - Count the number of cooperators (C_prev) in the previous round.
   - If C_prev exceeds the threshold (n/k), cooperate again; otherwise, defect.
3. **Last Round (t = r):** Always defect, as there's no future consequence for defecting.

**Edge Cases Handling:**
- **First Round:** Cooperate to potentially encourage others.
- **Last Round:** Defect to maximize payoff without future repercussions.
- **Insufficient Cooperation:** Switch to defection if previous cooperation levels are below the threshold.

**Opportunistic Alignment:**
The strategy is opportunistic by cooperating only when beneficial, defecting when it's not, and leveraging others' cooperation while avoiding being exploited.

### Pseudocode
```python
n = number of players
k = multiplication factor
r = number of rounds
history = []  # To track previous actions

for each round t from 1 to r:
    if t == 1:
        action = 'C'
    else:
        C_prev = number of cooperators in history[t-2]
        threshold = n / k
        if C_prev > threshold:
            action = 'C'
        else:
            action = 'D'
    if t == r:
        action = 'D'  # Always defect in the last round
    history.append(action)
    # Execute action and observe others' actions
```

This strategy adaptively responds to others' behavior, ensuring individual payoffs are maximized while maintaining the potential for cooperation when mutually beneficial.
'''

description_OPPORTUNISTIC_25 = '''
To address the N-Player Public Goods Game, we designed an adaptive strategy called "Adaptive Opportunism" that balances cooperation with self-interest, ensuring robustness against diverse opponent behaviors while maximizing payoffs. Here's the structured strategy:

### Strategy: Adaptive Opportunism

#### Decision Rules:
1. **First Round Cooperation**: Initiate cooperation to encourage a positive tone and maximize initial public goods benefits.
2. **Subsequent Rounds**:
   - After the first round, calculate the number of cooperators from the previous round.
   - **Threshold-Based Cooperation**: Cooperate if the number of previous round cooperators meets or exceeds a dynamic threshold (T). The threshold is calculated as \( T = \frac{k}{k + 1} \), ensuring higher thresholds with larger \( k \), promoting cooperation when public goods benefits are significant.
3. **Last Two Rounds**:
   -Gradually shift towards defection in the final two rounds, defecting in the last round to maximize personal payoffs, anticipating others may do the same.

#### Edge Case Handling:
- **First Round**: Always cooperate.
- **Final Rounds**: Decrease cooperative behavior, defecting in the last round to leverage potential higher payoffs from others' likely defection.

#### Opportunism:
The strategy adapts based on observed cooperation levels, taking advantage of others' cooperation while defending against exploitation by defecting when cooperation is insufficient.

### Pseudocode:
```python
def adaptive_opportunism(n, k, r, history):
    if len(history) == 0:
        # First round: Cooperate
        return 'C'
    else:
        # Previous rounds' actions; assume history[t] is a list of 'C' or 'D' for each player at round t
        prev_coop = sum(1 for action in history[-1] if action == 'C')
        threshold = (k) / (k + 1)
        if prev_coop / n >= threshold:
            current_round = len(history) + 1
            if current_round < r - 1:
                return 'C'
            elif current_round == r - 1 or current_round == r:
                return 'D'
        return 'D'
```

### Explanation:
- **Initial Cooperation**: Starts with cooperation to foster a collaborative environment.
- **Adaptive Threshold**: Uses a threshold based on \( k \) to decide future cooperation, promoting flexibility.
- **Endgame Strategy**: Shifts to defection in the last two rounds to maximize individual payoffs, aligning with the expectation that others may also defect.

This strategy is robust, adapting to various behaviors while ensuring it doesn't exploit others unduly, making it a strong competitor in the tournament.
'''

description_OPPORTUNISTIC_26 = '''
To design an opportunistic strategy for the N-Player Public Goods Game, the approach focuses on maximizing individual payoffs by taking advantage of others' cooperation while minimizing exploitation. The strategy adapts based on the history of cooperation observed in previous rounds.

### Strategy: Adaptive Opportunism

#### 1. Decision Rules:
- **First Round:** Always Defect (D). This avoids being exploited when cooperation may not be beneficial initially.
- **Intermediate Rounds (2 to r-1):** Cooperate (C) if the number of cooperators in the previous round (C_prev) exceeds the threshold (n/k). Otherwise, Defect (D). This encourages contributing to the public good only when it's beneficial.
- **Last Round (r):** Always Defect (D). Without future interactions, maximizing immediate payoff is optimal.

#### 2. Handling Edge Cases:
- The strategy is designed to handle varying numbers of rounds (r > 1) and players (n ≥ 2) dynamically.
- The threshold (n/k) determines when cooperation becomes advantageous, ensuring decisions are context-sensitive.

#### 3. Opportunism:
The strategy is opportunistic as it capitalizes on others' cooperation when profitable while defecting to avoid being exploited. It adapts based on observed behavior, ensuring robust performance against diverse opponent strategies.

### Pseudocode Implementation:

```python
def adaptive_opportunism(n, k, r):
    prev_C = 0  # Number of cooperators in the previous round
    for t in range(1, r + 1):
        if t == 1:
            action = 'D'
        elif t == r:
            action = 'D'
        else:
            threshold = n / k
            if prev_C > threshold:
                action = 'C'
            else:
                action = 'D'
        # Execute action
        print(f"Round {t}: {action}")
        # After the round, update prev_C based on observed cooperation
        # Assuming 'observe_cooperation()' returns the count of Cs in the current round
        prev_C = observe_cooperation()
```

### Explanation:
- **First Round:** Starts by defecting to avoid potential exploitation without prior information.
- **Intermediate Rounds:** Uses the previous round's cooperation rate to decide. Cooperates if past cooperation was sufficiently high, otherwise defects.
- **Last Round:** Defects to maximize immediate payoff since future consequences are absent.

This strategy ensures the player adapts dynamically, maximizing their payoff across the game's duration while remaining robust against various opponent behaviors.
'''

description_OPPORTUNISTIC_27 = '''
To design an effective strategy for the N-Player Public Goods Game, we can leverage an approach inspired by Tit-for-Tat, adapted to group dynamics. Here's a structured strategy:

### Strategy: Opportunistic TFT (Tit-for-Tat)

#### 1. Decision Rules:
   - **First Round:** Cooperate to encourage initial group cooperation.
   - **Subsequent Rounds:** 
     - Calculate the average cooperation rate from the previous round.
     - Cooperate if the average meets or exceeds the threshold (k/n). Defect otherwise.
   - **Last Round:** Defect, as there's no future punishment possible.

#### 2. Handling Edge Cases:
   - **First Round:** Cooperate to set a positive tone.
   - **Last Round:** Defect to maximize personal gain without future repercussions.

#### 3. Opportunistic Approach:
   - The strategy adapts based on group behavior, encouraging cooperation when beneficial and defecting when others don't contribute sufficiently.

### Example Scenarios:
   - **All Cooperate:** High payoffs sustain cooperation.
   - **Some Defect:** A drop in average cooperation may lead to defection, potentially causing a decay in overall cooperation.

This strategy balances exploiting opportunities when others don't contribute enough with contributing when the group's efforts justify it. It's straightforward, adaptable, and handles edge cases effectively, ensuring robust performance across various scenarios.
'''

description_OPPORTUNISTIC_28 = '''
**Strategy: Opportunistic Threshold Cooperation (OTC)**

**1. Decision Rules:**

- **First Round:** Always Cooperate (C). This initial move tests others' willingness to contribute to the public good.
  
- **Intermediate Rounds (2 to r-1):** 
  - Calculate the threshold as the ceiling of (n/k), denoted as t.
  - Observe the number of Cooperators (m_prev) from the previous round.
  - If m_prev ≥ t, Cooperate (C). Otherwise, Defect (D).

- **Final Round (r):** Always Defect (D). Since there's no future interaction, maximizing immediate payoff is optimal.

**2. Handling Edge Cases:**

- **First Round:** Start with Cooperation to encourage mutual contribution.
- **Last Round:** Defect to maximize personal gain without future repercussions.
- **Low Cooperation:** If cooperation drops below the threshold, the strategy adapts by Defecting to avoid being exploited.

**3. Opportunistic Nature:**

The strategy leverages the game's parameters (n and k) to determine a cooperation threshold dynamically. It only Cooperates when the expected payoff surpasses the benefit of Defecting, balancing self-interest with collective gain. The approach encourages others to Cooperate by leading when possible and adapting when not, ensuring robust performance across varied behaviors.

**Pseudocode:**

```
threshold = ceil(n / k)

for each round from 1 to r:
    if round == 1:
        action = C
    elif round == r:
        action = D
    else:
        m_prev = number of cooperators in previous round
        if m_prev >= threshold:
            action = C
        else:
            action = D
    record action and observe outcomes
```

This strategy adapts to the group's behavior, fostering cooperation when beneficial and defecting when necessary, ensuring an opportunistic approach to maximize personal payoff.
'''

description_OPPORTUNISTIC_29 = '''
**Opportunistic Strategy for N-Player Public Goods Game**

**Name:** Adaptive Opportunism

**Objective:** Maximize individual payoff by leveraging cooperation when beneficial and defecting when not, using history and game parameters to guide decisions.

---

### Strategy Description:

1. **Initial Exploration (First 3 Rounds):**
   - **Rounds 1 and 2:** Cooperate (C) to encourage others and gauge responsiveness.
   - **Round 3:** Defect (D) to observe others' reactions and test their strategies.

2. **Exploitation Phase (After Round 3):**
   - **Payoff Assessment:** Calculate the average payoff from rounds where the player Cooperated versus Defected.
   - **Decision Rule:** Cooperate if the average payoff from Cooperating is greater than or equal to that from Defecting; otherwise, Defect.

3. **Endgame Handling:**
   - **Last Round (Round r):** Always Defect (D) to maximize payoff without future consequences.

---

### Implementation Pseudocode:

```python
def adaptive_opportunism(n, r, k, history):
    if len(history) == 0:  # First round
        return 'C'
    elif len(history) == 1:  # Second round
        return 'C'
    elif len(history) == 2:  # Third round
        return 'D'
    else:
        # Calculate average payoff for Cooperate and Defect rounds
        coop_payoffs = [π for t, a, π in history if a == 'C']
        defect_payoffs = [π for t, a, π in history if a == 'D']
        avg_coop = sum(coop_payoffs)/len(coop_payoffs) if coop_payoffs else 0
        avg_defect = sum(defect_payoffs)/len(defect_payoffs) if defect_payoffs else 0
        if avg_coop >= avg_defect:
            return 'C'
        else:
            return 'D'
    if current_round == r:  # Last round
        return 'D'
    else:
        # Use history to decide
        pass
```

---

**Rationale:**

- **Initial Exploration:** Tests others' behavior and sets a cooperative tone.
- **Exploitation:** Uses past outcomes to decide actions, ensuring opportunism.
- **Endgame:** Maximizes final-round payoff by defecting.

This strategy balances cooperation and defection adaptively, ensuring robustness across various opponent behaviors.
'''

description_OPPORTUNISTIC_30 = '''
To address the N-Player Public Goods Game, the strategy "Adaptive Opportunism" is designed to balance exploration and exploitation, ensuring robustness across various behaviors.

**Strategy Overview:**

1. **Initial Round (Exploration):**
   - **Action:** Cooperate (C)
   - **Rationale:** Initiates potential group cooperation, encouraging others to follow suit, while testing the waters for future actions.

2. **Subsequent Rounds (Adaptive Decision-Making):**
   - **Count Previous Cooperators:** Tally the number of players who cooperated in the immediately preceding round.
   - **Threshold Calculation:** Determine the threshold as (k-1)/n, where k is the multiplication factor and n is the number of players. This threshold reflects the minimum cooperation level needed for individual profitability.
   - **Decision Rule:** 
     - **Cooperate** if the count of past cooperators meets or exceeds the threshold.
     - **Defect** if the count is below the threshold, maximizing personal gain when collective cooperation is insufficient.

3. **Final Round (Exploitation):**
   - **Action:** Defect (D)
   - **Rationale:** In the absence of future repercussions, defecting maximizes personal payoff, as others are likely to do the same, avoiding the risk of being exploited.

**Pseudocode Implementation:**

```
function adaptive_opportunism(n, k, r, history):
    # Initialize variables
    round = 1
    while round <= r:
        if round == 1:
            action = C
        else:
            previous_cooperators = count_cooperators(history[round-2])
            threshold = (k - 1) / n
            if previous_cooperators >= threshold:
                action = C
            else:
                action = D
        # Execute action and observe outcomes
        history.append(action)
        if round == r:
            action = D
        round += 1
    return history
```

**Conclusion:**

This strategy begins with cooperation to foster collective benefit, adapts based on others' behavior to maintain profitability, and defects in the final round to maximize personal gain. It is designed to be robust against diverse opponent strategies, ensuring a balance between cooperation and self-interest.
'''

description_OPPORTUNISTIC_31 = '''
### Strategy Name: Adaptive Opportunism with Retaliation (AOR)

#### 1. Decision Rules:

**a. First Round:**
- **Action:** Cooperate (C)
- **Rationale:** Start by cooperating to encourage initial cooperation and maximize the public good. This sets a positive tone and gathers information on other players' behaviors.

**b. Subsequent Rounds (not final):**
1. **Calculate Average Cooperation Rate (ACR) of Other Players:**
   - ACR = (Total contributions by other players in previous rounds) / (Number of previous rounds * (n - 1))
   - Range: 0 ≤ ACR ≤ 1

2. **Determine Current Round Incentive (CRI):**
   - CRI = k/n * (Expected total contributions if Cooperate) - (Expected private gain if Defect)
   - If CRI > 0, it's beneficial to Cooperate; otherwise, Defect.

3. **Retaliation Mechanism:**
   - If ACR < Threshold (e.g., 0.5), switch to Defect for the next round to punish low cooperation.
   - If ACR >= Threshold, continue based on CRI.

**c. Final Round:**
- **Action:** Defect (D)
- **Rationale:** Since there are no future interactions, maximize personal payoff by keeping the endowment.

#### 2. Handling Edge Cases:

- **All Players Defecting Consistently:**
  - If ACR remains below the threshold for multiple rounds, continue Defecting to avoid exploitation.

- **High Cooperation from Others:**
  - Capitalize on the public good by Cooperating, as the increased contributions benefit everyone.

- **Voluntary Defection by Self:**
  - If facing persistent low cooperation, consider temporary Defection to signal dissatisfaction and encourage others to cooperate.

#### 3. Opportunistic Alignment:

- **Exploit Cooperation:** When others cooperate, contribute to gain from the enhanced public good.
- **Protect Against Exploitation:** When others defect, prioritize personal gain by defecting.
- **Adapt Dynamically:** Adjust strategy based on the evolving behavior of other players, maintaining flexibility to shift between cooperation and defection as warranted.

#### Pseudocode:

```pseudocode
function AOR_strategy(history, current_round, total_rounds, n, k):
    if current_round == 1:
        return Cooperate
    else:
        past_actions = history[:current_round-1]
        # Calculate average cooperation rate of others
        total_contributions = sum(past_actions)
        ACR = total_contributions / ((current_round - 1) * (n - 1))
        
        # Determine current round incentive
        expected_total_if_C = ACR * (n - 1) + 1  # Assuming self Cooperates
        CRI = (k / n) * expected_total_if_C - (1)  # Compare to Defect payoff
        
        if CRI > 0:
            if ACR >= threshold:
                return Cooperate
            else:
                return Defect  # Retaliate
        else:
            return Defect
        
    if current_round == total_rounds:
        return Defect
```

### Rationale

The strategy begins cooperatively to foster mutual benefit and gathers initial data on others' behavior. As the game progresses, it dynamically adjusts by rewarding cooperation and punishing defection, ensuring it remains opportunistic and adaptive. The final round defect ensures personal maximization without future repercussions, encapsulating the opportunism.
'''

description_OPPORTUNISTIC_32 = '''
To address the challenge of designing an opportunistic strategy for the N-Player Public Goods Game, we need a approach that balances exploiting others' cooperation while avoiding exploitation. The strategy should adapt based on observed behavior and maximize payoffs over multiple rounds.

### Strategy: "Adaptive Cooperation with Endgame Defection"

**Decision Rules:**

1. **First Round:** Always **Cooperate (C)**. This sets a cooperative tone, encouraging others to follow suit.

2. **Subsequent Rounds (Rounds 2 to r-1):**
   - Calculate the average number of cooperators, `s_avg`, from all previous rounds.
   - Compare `s_avg` with a threshold `T`, where `T = (n / (k + 1))`.
     - If `s_avg ≥ T`, **Cooperate (C)**.
     - If `s_avg < T`, **Defect (D)**.

3. **Last Round (Round r):** Always **Defect (D)**. Since there are no future interactions, maximize immediate payoff.

**Rationale:**

- **Initial Cooperation:** By cooperating initially, the strategy attempts to foster a cooperative environment, potentially leading to higher collective payoffs if others reciprocate.
- **Adaptive Threshold:** The threshold `T` is calculated using `T = n / (k + 1)`, ensuring that cooperation only occurs when sufficient players are contributing, making it beneficial to continue cooperating.
- **Endgame Defection:** In the final round, without future consequences, defecting ensures the highest possible immediate payoff.

**Example Walkthrough (n=6, k=2):**

1. **Round 1:** Cooperate.
   - If others defect, s₁=1. Payoff ≈0.333.
2. **Round 2:** Calculate s_avg=1/1=1 < T=2. Defect.
   - Payoff=1 + (2/6)*1≈1.333.
3. **Round 3:** s_avg=1 (still below T). Defect.
4. **Last Round (r):** Always Defect.

If others cooperate:

1. **Round 1:** All Cooperate, s=6. T=2.
2. **Round 2:** s_avg=6 >2. Cooperate.
3. **Round 3:** s_avg remains above T. Continue Cooperating.

This strategy effectively balances cooperation and defection, encouraging mutual benefit while avoiding being exploited, making it both adaptive and robust.
'''

description_COLLECTIVE_26 = '''
To address the challenge of designing a collective strategy for the N-Player Public Goods Game, we have developed an adaptive and robust approach. The strategy encourages cooperation by leveraging reciprocity based on the game's parameters and history.

### Strategy Overview:
The strategy is designed to promote sustained cooperation by conditioning cooperation on the number of cooperators in the previous round. This encourages a collective effort to maintain the public good, with a mechanism to punish insufficient cooperation.

### Decision Rules:
1. **First Round:** All players start by cooperating. This sets a cooperative tone and establishes a baseline for future interactions.
2. **Subsequent Rounds:** In each subsequent round, each player decides to cooperate if the number of cooperators in the previous round meets or exceeds the multiplication factor \( k \). If fewer than \( k \) players cooperated, they will defect. This rule creates a dynamic where cooperation is rewarded with continued cooperation, while insufficient cooperation triggers defection as a form of punishment.

### Handling Edge Cases:
- **First Round:** Cooperation is unconditional, laying the groundwork for potential future cooperation.
- **Last Round:** The same rule applies. Players base their decision on the previous round's cooperation level, even in the final round, to maintain consistency and maximize total payoff.

### Collective Alignment:
The strategy is designed to align with a collective mindset, encouraging mutual cooperation if a sufficient number of players (determined by \( k \)) cooperate. This fosters a group-level reciprocity, where players act in a way that supports the public good as long as the threshold is met.

### Pseudocode:
```python
def strategy(game_parameters, history):
    n = game_parameters['n']
    k = game_parameters['k']
    r = game_parameters['r']
    
    # For each player i
    if not history:  # First round
        return 'C'
    else:
        # Get previous round's actions
        previous_actions = history[-1]
        # Count number of cooperators
        cooperators = previous_actions.count('C')
        # Decide based on threshold k
        if cooperators >= k:
            return 'C'
        else:
            return 'D'
```

### Explanation:
- **First Round Cooperation:** Ensures initial cooperation, which is crucial for kickstarting the public good.
- **Adaptive Punishment:** By defecting when fewer than \( k \) players cooperate, the strategy adaptively adjusts to the group's behavior, discouraging exploitation and promoting continued cooperation.
- **Robustness:** The strategy is robust because it depends solely on observable past actions, making it applicable across diverse opponent behaviors without requiring prearranged coordination.

This approach balances individual rationality with collective benefits, aiming to maximize the total payoff through sustained cooperation enforced by reciprocal strategies.
'''

description_PROSOCIAL_26 = '''
To address the N-Player Public Goods Game, a prosocial strategy is designed to encourage cooperation while adapting to others' actions. The strategy is based on a threshold of cooperation from previous rounds to decide whether to cooperate or defect in the current round. This approach is adaptive, handles edge cases, and aligns with a prosocial mindset by promoting group welfare.

### Strategy Description:
1. **First Round Cooperation**: Start by cooperating to set a positive tone and encourage others to do the same.
2. **Subsequent Rounds**: For each round after the first, check the number of cooperators from the previous round. If this number meets or exceeds a predetermined threshold calculated as `ceil(n/k)`, continue cooperating. Otherwise, defect to avoid exploitation.
3. **Last Round Defection**: In the final round, defect since there's no future interaction to influence, making defecting individually rational.

### Pseudocode Implementation:
```python
def prosocial_strategy(n, k, r, current_round, previous_actions):
    if current_round == 1:
        return "C"
    if current_round == r:
        return "D"
    
    threshold = math.ceil(n / k)
    previous_cooperators = sum(previous_actions == 'C')
    
    if previous_cooperators >= threshold:
        return "C"
    else:
        return "D"
```

### Explanation:
- **Cooperation in Early Rounds**: By starting with cooperation, the strategy sets a cooperative precedent, which can encourage others to cooperate.
- **Adaptive Threshold**: Using `ceil(n/k)` as a threshold ensures that cooperation is maintained only when sufficiently beneficial for the group, preventing free-riding.
- **Last Round Defection**: Acknowledging the end of the game, the strategy defects in the last round to maximize individual payoff without affecting future interactions.

This strategy effectively balances individual and group interests, providing a robust approach to maintaining prosocial behavior in the game.
'''

description_COMMUNAL_17 = '''
To address the challenge of designing a communal strategy for the N-Player Public Goods Game, we developed an approach that balances individual incentives with the collective benefit of the public good. Here's the strategy:

### Strategy: Communal Reciprocity

1. **First Round**: Cooperate to set a cooperative tone and encourage initial contributions to the public good.

2. **Subsequent Rounds**:
   - **Assess Previous Cooperation**: Calculate the number of players who Cooperated in the previous round.
   - **Threshold Calculation**: Determine the minimum number of Cooperators required for the public good to be sufficiently beneficial. This threshold is the ceiling of the ratio of the number of players (n) to the multiplication factor (k), i.e., ceiling(n/k).
   - **Decision Rule**:
     - If the number of Cooperators in the previous round meets or exceeds the threshold, Cooperate.
     - If the number of Cooperators is below the threshold, Defect to encourage higher contributions.

### Pseudocode

```
Initialize:
    action = Cooperate  # First round action

For each round t from 2 to r:
    previous_coop = number of Cooperators in round t-1
    threshold = ceiling(n / k)
    if previous_coop >= threshold:
        action = Cooperate
    else:
        action = Defect

# Act according to the determined action
```

### Rationale

The strategy, Communal Reciprocity, is designed to foster cooperation by rewarding sufficient contributions to the public good. By Cooperating when enough players contribute, the strategy ensures the public good is valuable, aligning individual and group interests. If contributions fall short, the strategy shifts to Defecting to incentivize higher participation, thus maintaining a balance between individual incentives and collective benefits.
'''

description_AGGRESSIVE_11 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we need to prioritize individual payoff maximization, adapting to others' actions while maintaining a robust approach. Here's the structured strategy:

### Aggressive Strategy: "Self-Interested Maximization"

1. **Decision Rules**:
   - **Cooperate (C)** if the expected payoff from cooperation exceeds that from defecting, considering the previous round's cooperation rate.
   - **Defect (D)** if the expected payoff from defecting is higher or if it's the first or last round.

2. **Handling Edge Cases**:
   - **First Round**: Defect to maximize immediate payoff without prior information.
   - **Middle Rounds**: Calculate the number of cooperators from the previous round. If the public good share from others is sufficient to make cooperating beneficial, cooperate; otherwise, defect.
   - **Last Round**: Defect, as there's no future impact.

3. **Adaptation and Adjustments**:
   - Track others' cooperation rates each round to decide future actions, ensuring adaptability based on observed behavior.

### Summary

This strategy starts with defecting in the first round, adapts based on others' cooperation history, and ensures defecting in the last round. It balances self-interest with adaptability, aligning with an aggressive mindset focused on maximizing individual gain.
'''

description_AGGRESSIVE_30 = '''
To design an aggressive strategy for the N-Player Public Goods Game, we need to maximize personal payoff while considering the game's structure and parameters. The key insight is that defecting (D) always yields a higher individual payoff than cooperating (C), as defecting adds a constant 1 to the public good share. Thus, the optimal aggressive strategy is to always defect, regardless of others' actions.

### Strategy: Always Defect

1. **Decision Rule:**
   - In every round, choose to Defect (D). This decision is based on the fact that defecting provides a higher personal payoff by 1 unit compared to cooperating, irrespective of others' choices.

2. **Handling Edge Cases:**
   - **First Round:** Defect, as there is no prior history of cooperation to influence the decision.
   - **Middle Rounds:** Continue to defect in each round to maximize individual gain.
   - **Last Round:** Defect, as there are no future rounds where cooperation could potentially yield higher payoffs through reciprocity.

3. **Aggressive Mindset:**
   - The strategy focuses solely on maximizing individual payoff without considering the well-being of others. By always defecting, the player takes advantage of any cooperation from others to increase their own payoff.

This strategy ensures that the player maximizes their personal gain in every possible scenario, adhering to the principles of an aggressive approach in game theory.
'''

description_OPPORTUNISTIC_7 = '''
To address the N-player public goods game, we've developed an opportunistic strategy that adapts based on the game's history and parameters. The strategy is designed to maximize individual payoff while encouraging cooperation when beneficial. Here's the structured approach:

### Opportunistic Strategy for the N-Player Public Goods Game

1. **First Round Cooperation**:
   - **Action**: Cooperate (C).
   - **Reasoning**: Initiate cooperation to encourage a positive start and assess others' willingness to contribute.

2. **Subsequent Rounds (2 to r-1)**:
   - **Calculate Threshold**: Compute \( T = \lfloor \frac{n}{k} \rfloor + 1 \), where \( n \) is the number of players, and \( k \) is the multiplication factor.
   - **Previous Cooperation Check**: Determine the number of cooperators in the previous round, \( C_{t-1} \).
   - **Decision Rule**:
     - **Cooperate** if \( C_{t-1} \geq T \).
     - **Defect** otherwise.
   - **Reasoning**: Cooperate if enough players contributed in the past round, ensuring cooperation is worthwhile. This encourages continued contribution when beneficial while punishing insufficient cooperation.

3. **Final Round (r)**:
   - **Action**: Defect (D).
   - **Reasoning**: In the last round, with no future interactions, maximize immediate payoff by defecting, as there's no incentive to maintain cooperation for future rounds.

### Pseudocode Illustration

```python
def strategy(n, k, r, history):
    if not history:  # First round
        return 'C'
    current_round = len(history) + 1
    if current_round == r:
        return 'D'
    # Calculate threshold
    T = (n // k) + 1
    # Count cooperators in previous round
    C_prev = sum(1 for action in history[-1] if action == 'C')
    if C_prev >= T:
        return 'C'
    else:
        return 'D'
```

### Explanation

- **Adaptation and Robustness**: The strategy adapts by evaluating past cooperation levels, making it robust against diverse opponent behaviors.
- **Opportunism**: It maximizes individual payoff by cooperating only when profitable, exploiting others' cooperation without being exploited.
- **Threshold Logic**: Uses a calculated threshold to decide cooperation, ensuring that only sufficiently high past contributions justify future cooperation.
- **Edge Cases Handling**: Starts cooperative, defects in the last round, and adjusts based on the number of previous cooperators, making it versatile for various game settings.

This approach ensures the strategy is both self-interested and responsive, balancing cooperation and defection to maximize payoffs in dynamic, competitive environments.
'''

description_OPPORTUNISTIC_14 = '''
**Opportunistic Cooperation with Adaptive Threshold (OCAT) Strategy**

**Overview:**
The OCAT strategy is designed for the N-Player Public Goods Game, aiming to maximize individual payoff through an adaptive approach that balances cooperation and self-interest. It initializes with cooperation, adapts based on past outcomes, and adjusts in the final round to optimize results.

**1. Initial Cooperation:**
- **First Round:** Cooperate (C) to encourage initial group cooperation and maximize potential collective payoff.

**2. Payoff Comparison:**
- Post-first round, calculate the average payoff from rounds when the player Cooperated (C) and Defected (D).
- Compare these averages to decide the next move: Cooperate if the average payoff from C is higher, otherwise Defect.

**3. Adaptive Threshold:**
- Use a dynamic threshold, calculated as \( \theta = \frac{k}{2n} \times \) the maximum possible payoff difference.
- Cooperate if the cooperation average exceeds the defection average by at least \( \theta \), ensuring cooperation is rewarding without exploitation.

**4. Final Round Adjustment:**
- In the last round, switch to Defect (D) to maximize personal gain, as future consequences are absent.

**Conclusion:**
OCAT starts with cooperation, adapts based on past interactions, and strategically defects in the final round. It dynamically adjusts using a threshold to avoid exploitation, ensuring a balance between cooperation and self-interest, making it robust for competitive scenarios.
'''

description_COLLECTIVE_16 = '''
To address the N-Player Public Goods Game, we designed a strategy that promotes cooperation while being adaptive and robust against various opponent behaviors. The strategy hinges on a threshold based on the multiplier factor \( k \), encouraging sustained cooperation as long as a sufficient number of players participate.

### Strategy:

1. **Initial Cooperation**: 
   - **First Round**: Cooperate. This establishes a cooperative foundation.

2. **Adaptive Cooperation**:
   - **Subsequent Rounds**: For each subsequent round, observe the number of players who cooperated in the previous round.
   - **Threshold Check**: If the number of cooperators in the previous round meets or exceeds \( k \), continue to cooperate. Otherwise, defect.

3. **Handling Edge Cases**:
   - **First Round**: Always Cooperate.
   - **Last Round**: Follow the same strategy as other rounds, maintaining consistency without altering behavior based on the round number.

4. **Collective Alignment**:
   - All players use the same strategy, ensuring coordinated behavior without direct communication. This fosters a collective mindset aimed at maximizing public good.

### Pseudocode:

```python
def strategy(n, k, history):
    if not history:  # First round
        return "C"
    previous_round = history[-1]
    C_prev = sum(1 for action in previous_round if action == "C")
    if C_prev >= k:
        return "C"
    else:
        return "D"
```

### Explanation:

- **Initial Cooperation**: By starting with cooperation, players set a cooperative tone.
- **Adaptive Threshold**: The strategy dynamically adapts by checking if at least \( k \) players cooperated previously. This ensures that public good contributions are maintained as long as sufficient players participate.
- **Edge Cases Handling**: Uniform behavior across all rounds, including the last, maintains consistency and prevents end-game defection risks.

This strategy is robust and adaptive, aligning individual actions with collective benefits while handling potential issues like free-riding.
'''
