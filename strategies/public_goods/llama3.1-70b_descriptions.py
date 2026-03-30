"""
Strategy descriptions for public_goods.

Generated with:
- Provider: OpenAI
- Model: meta-llama/llama-3.1-70b-instruct
"""


description_PROSOCIAL_1 = '''
Here's a prosocial strategy for the N-Player Public Goods Game, which we'll call "Adaptive Cooperation with Reciprocal Incentives" (ACRI).

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a baseline of cooperation and encourage others to follow suit.
2. **Reciprocal Cooperation**: For rounds 2 to r-1, cooperate (C) if the total number of cooperators in the previous round is greater than or equal to the number of cooperators required to reach the social optimum (n/k). This ensures that the group benefits from cooperation when enough players are contributing.
3. **Punishment Mechanism**: If the total number of cooperators in the previous round falls below the threshold (n/k), defect (D) in the current round. This serves as a gentle punishment to discourage free-riding and incentivizes cooperation.
4. **Final Round Cooperation**: In the last round (r), cooperate (C) regardless of the previous round's outcome. This maintains a prosocial stance even when the game is ending.

**Handling Edge Cases:**

1. **First Round**: Cooperate (C) as described above.
2. **Last Round**: Cooperate (C) as described above.
3. **Tie-Breaking**: In case of a tie in the number of cooperators, use a random tie-breaker (e.g., flip a coin) to decide whether to cooperate or defect.
4. **Zero Cooperators**: If no players cooperated in the previous round, cooperate (C) in the current round to attempt to restart cooperation.

**Pseudocode:**
```python
def ACRI(n, k, r, previous_round_actions):
    # Initial Cooperation
    if r == 1:
        return 'C'
    
    # Reciprocal Cooperation
    if sum(previous_round_actions) >= n/k:
        return 'C'
    
    # Punishment Mechanism
    if sum(previous_round_actions) < n/k:
        return 'D'
    
    # Final Round Cooperation
    if r == r:
        return 'C'
    
    # Tie-Breaking (optional)
    if sum(previous_round_actions) == n/k:
        return random.choice(['C', 'D'])
    
    # Zero Cooperators
    if sum(previous_round_actions) == 0:
        return 'C'
```
**Rationale:**

ACRI balances cooperation and reciprocity to promote prosocial behavior. By cooperating initially and conditionally reciprocating cooperation, ACRI encourages other players to cooperate and contribute to the public good. The punishment mechanism discourages free-riding and maintains a level of cooperation. By cooperating in the final round, ACRI maintains a prosocial stance even when the game is ending.

This strategy is adaptive, as it responds to the actions of other players, and robust, as it handles various edge cases and scenarios. ACRI does not rely on specific coordination mechanisms or assumptions about other players' strategies, making it a suitable candidate for a tournament against independent strategies.
'''

description_PROSOCIAL_2 = '''
**Prosocial Strategy: Adaptive Cooperation**

**Overview**
Adaptive Cooperation is a prosocial strategy designed to promote cooperation in the N-Player Public Goods Game. It balances individual self-interest with collective well-being, adapting to the behavior of other players while maintaining a strong cooperative foundation.

**Decision Rules**

1. **First Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds**: Observe the total number of cooperators in the previous round (Σc_j). If:
	* Σc_j ≥ (n/2), Cooperate (C) in the current round. This threshold encourages cooperation when the group is already inclined towards cooperation.
	* Σc_j < (n/2), Defect (D) in the current round. This response aims to minimize losses when cooperation is low.
3. **Exception**: If the current round is the last round (r), always Defect (D). This ensures maximizing individual payoff in the final round, as cooperation is not sustainable without future interactions.
4. **Trigger**: If the total number of cooperators in the previous round (Σc_j) is less than or equal to (n/3), **Trigger** a " correction" phase. In the next round, Cooperate (C) regardless of the previous round's outcome. This mechanism helps to revitalize cooperation when it is waning.

**Additional Logic**

* **Recent Behavior**: If a player observes a significant increase in cooperation (Σc_j increases by at least 2) in the previous round, **Increase Cooperation Threshold** by 1 for the next round. This allows the strategy to adapt to changing group behavior and encourages sustained cooperation.
* **Punish Defection**: If a player observes a significant decrease in cooperation (Σc_j decreases by at least 2) in the previous round, **Decrease Cooperation Threshold** by 1 for the next round. This response discourages defection and encourages cooperation.

**Pseudocode**
```
  // Initialize variables
  cooperation_threshold = n / 2
  correction_phase = False

  // Loop through rounds
  for t = 1 to r:
    // First round
    if t == 1:
      action = C
    else:
      // Observe previous round's behavior
      previous_cooperators = Σc_j
      if previous_cooperators >= cooperation_threshold:
        action = C
      else:
        action = D

    // Exception: Last round
    if t == r:
      action = D

    // Trigger correction phase
    if previous_cooperators <= n / 3:
      correction_phase = True
      action = C

    // Recent behavior adjustments
    if previous_cooperators increased by at least 2:
      cooperation_threshold += 1
    elif previous_cooperators decreased by at least 2:
      cooperation_threshold -= 1

    // Take action and observe outcome
    take_action(action)
    observe_outcome()
```
**Rationale**
Adaptive Cooperation balances individual self-interest with collective well-being by adapting to the behavior of other players. By establishing a cooperative tone in the first round and responding to changes in group behavior, this strategy promotes cooperation while minimizing losses. The correction phase and recent behavior adjustments help to revitalize cooperation when it is waning and encourage sustained cooperation.
'''

description_PROSOCIAL_3 = '''
I propose a prosocial strategy, which I'll call " Adaptive Cooperate-and- Mirror" (ACM). ACM balances cooperation with adaptiveness to opponents' behaviors, ensuring a robust and prosocial approach.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with probability 1. This sets a positive tone and encourages others to cooperate.
2. **Mirror-and-Adapt**: From the second round onwards, observe the number of cooperators (c) and defectors (d) in the previous round. Calculate the cooperation rate: cr = c / (c + d).
3. **Cooperation Threshold**: Set a cooperation threshold (ct) based on the multiplication factor (k) and the number of players (n): ct = (k / n) * (n / 2).
4. **Adaptive Cooperation**: If the cooperation rate (cr) is above the cooperation threshold (ct), cooperate (C) with probability 1. Otherwise, cooperate with probability cr.
5. **Defection Response**: If you cooperated in the previous round and the cooperation rate (cr) is below the cooperation threshold (ct), defect (D) with probability 1. This responds to exploitation and encourages opponents to cooperate.
6. **Punishment**: If you defected in the previous round and the cooperation rate (cr) is above the cooperation threshold (ct), cooperate (C) with probability 1. This punishes yourself for not cooperating when others did.

**Edge Cases:**

1. **Last Round**: In the final round, cooperate (C) with probability 1, regardless of previous outcomes. This promotes a positive ending and encourages others to do the same.
2. **Ties**: If the cooperation rate (cr) is exactly equal to the cooperation threshold (ct), cooperate (C) with probability 0.5.
3. **Empty History**: If there is no previous round (e.g., the first round), default to the initial cooperation rule.

**Pseudocode:**

```markdown
# Initialize variables
cooperation_rate = 0
cooperation_threshold = (k / n) * (n / 2)
previous_action = None
previous_cooperation_rate = None

# Loop through rounds
for round in range(r):
    # First round: cooperate
    if round == 0:
        action = C
    else:
        # Calculate cooperation rate
        cooperation_rate = c / (c + d)
        
        # Adaptive cooperation
        if cooperation_rate > cooperation_threshold:
            action = C
        else:
            action = C with probability cooperation_rate
            action = D with probability 1 - cooperation_rate
        
        # Defection response
        if previous_action == C and cooperation_rate < cooperation_threshold:
            action = D
        
        # Punishment
        if previous_action == D and cooperation_rate > cooperation_threshold:
            action = C
    
    # Update previous action and cooperation rate
    previous_action = action
    previous_cooperation_rate = cooperation_rate
    
    # Last round: cooperate
    if round == r - 1:
        action = C
```

**Prosociability**:
ACM is designed to be prosocial by:

1. Initially cooperating to set a positive tone.
2. Adapting to opponents' behaviors to balance cooperation and self-interest.
3. Responding to exploitation and encouraging cooperation.
4. Punishing itself for not cooperating when others do.
5. Promoting a positive ending in the final round.

ACM is robust to a wide range of opponent behaviors, as it adapts to the cooperation rate and responds accordingly.
'''

description_PROSOCIAL_4 = '''
**Prosocial Strategy: Adaptive Cooperation (AC)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a baseline for cooperation.
2. **Reciprocity**: If the number of cooperators in the previous round is greater than or equal to half of the total players (n/2), cooperate in the current round. This encourages continued cooperation when it's already prevalent.
3. **Punish Defection**: If the number of cooperators in the previous round is less than half of the total players (n/2), and the total payoff from the public good in the previous round is less than the private payoff (i.e., Σ(j=1 to n) c_j < n/k), defect in the current round. This discourages exploitation by others.
4. **Imitation**: If the total payoff from the public good in the previous round is greater than or equal to the private payoff (i.e., Σ(j=1 to n) c_j ≥ n/k), imitate the action of the player who received the highest payoff in the previous round. This spreads successful strategies and adapts to changing conditions.
5. **Last Round Exception**: In the final round, always cooperate to maximize the total public good, as there's no future round to account for.

**Edge Cases:**

* If the number of rounds (r) is 1, always cooperate, as there's only one round to play.
* If the number of players (n) is 2, always cooperate, as the game reduces to a prisoner's dilemma, and cooperation is the dominant strategy.

**Prosocial Alignment:**

The Adaptive Cooperation strategy prioritizes cooperation while adapting to the actions of other players. By initially cooperating and then reciprocating cooperation, AC promotes a cooperative atmosphere. When others defect, AC punishes by defecting, but returns to cooperation when the public good is successful. This approach balances individual interests with the greater good, aligning with the prosocial mindset.

**Pseudocode:**
```markdown
def AdaptiveCooperation(n, r, k, history):
    if r == 1:  # single round
        return C
    elif n == 2:  # two-player game
        return C
    else:
        previous_cooperators = sum(c_i for c_i in history[-1])
        if previous_cooperators >= n/2:
            return C
        elif previous_cooperators < n/2 and sum(k/n * c_j for c_j in history[-1]) < 1:
            return D
        elif sum(k/n * c_j for c_j in history[-1]) >= 1:
            highest_payoff_player = max(history[-1], key=lambda x: x[1])
            return highest_payoff_player[0]
        else:  # last round
            return C
```
This strategy should be robust and adaptive in a wide range of scenarios, promoting prosocial behavior while competing in the tournament.
'''

description_PROSOCIAL_5 = '''
Here's a prosocial strategy, "Cooperative Adaptive Learner" (CAL), designed to be adaptive, robust, and prosocial:

**Decision Rules:**

1. **Initial Rounds:** In the first round, CAL cooperates (C) to establish a cooperative tone and encourage others to follow.
2. **Cooperation Threshold:** Track the total number of cooperators (T) in the previous round. If T ≥ n/2, CAL cooperates (C) in the current round. Otherwise, CAL defects (D).
3. **Adaptive Adjustment:** Monitor the average payoff of cooperators (APC) and defectors (APD) over the last few rounds (e.g., 3-5 rounds). If APC > APD, CAL increases its cooperation rate by 10% (i.e., becomes more likely to cooperate). If APD > APC, CAL decreases its cooperation rate by 10%.
4. **Robustness Mechanism:** If CAL observes a significant drop in overall cooperation (e.g., 20% or more) in the last few rounds, it will temporarily defect (D) for one round to signal its willingness to adapt and encourage others to cooperate.

**Handling Edge Cases:**

1. **Last Round:** In the final round, CAL defects (D) to maximize its individual payoff, as there are no future rounds to consider.
2. **Ties:** If the number of cooperators is exactly equal to n/2, CAL will cooperate (C) to maintain a prosocial stance.
3. **Opponent Defection:** If CAL observes an opponent consistently defecting (D), it will adapt by reducing its cooperation rate towards that opponent.

**Pseudocode:**
```markdown
# Initialize variables
T = 0  # Total cooperators
APC = 0  # Average payoff of cooperators
APD = 0  # Average payoff of defectors
cooperation_rate = 1  # Initial cooperation rate (100%)

# Loop through rounds
for round in range(r):
    # Determine action
    if round == 0:  # First round
        action = C
    elif T >= n/2:  # Cooperation threshold
        action = C
    else:
        action = D

    # Adaptive adjustment
    if APC > APD:
        cooperation_rate += 0.1
    elif APD > APC:
        cooperation_rate -= 0.1

    # Robustness mechanism
    if significant_drop_in_cooperation():
        action = D

    # Update variables
    T = update_T(action)
    APC = update_APC(action)
    APD = update_APD(action)

    # Take action
    if action == C:
        contribute_to_public_good()
    else:
        keep_endowment_privately()
```
**Prosocial Alignment:**

CAL prioritizes cooperation and prosocial behavior, aiming to create a mutually beneficial environment. By cooperating in the first round, CAL sets a positive tone for the game. The cooperation threshold encourages CAL to cooperate when others are doing so, promoting a cooperative norm. The adaptive adjustment mechanism allows CAL to respond to changes in the game dynamics, increasing cooperation when it is beneficial and decreasing it when it is not. The robustness mechanism helps maintain cooperation in the face of adversity, signaling CAL's commitment to prosocial behavior.
'''

description_PROSOCIAL_6 = '''
**Strategy Name:** Adaptive Prosociality (APS)

**Overview:** APS is a prosocial strategy designed for the N-Player Public Goods Game. It adapts to the game's history and parameters, promoting cooperation while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) in the first round to initiate a cooperative atmosphere and encourage others to follow.
2. **Subsequent Rounds (t>1):**
	* If the total number of cooperators in the previous round is greater than or equal to half of the players (Σc_j ≥ n/2), Cooperate (C) in the current round.
	* Otherwise, Defect (D) in the current round.
3. **Exception Handling:**
	* If all players defected in the previous round (Σc_j = 0), Cooperate (C) in the current round to attempt to revive cooperation.
	* If all players cooperated in the previous round (Σc_j = n), Defect (D) in the current round to prevent over-contribution.

**Pseudocode:**
```
function APS(n, k, r, history):
  # Initialize variables
  total_cooperators = 0
  previous_round_cooperators = 0

  # Iterate through rounds
  for t in range(1, r+1):
    # First round: Cooperate
    if t == 1:
      action = C
    # Subsequent rounds
    else:
      # Count cooperators in previous round
      previous_round_cooperators = sum([1 if c_j == C else 0 for c_j in history[t-1]])

      # Decide action based on previous round's cooperation level
      if previous_round_cooperators >= n/2:
        action = C
      else:
        # Exception handling
        if previous_round_cooperators == 0:
          action = C
        elif previous_round_cooperators == n:
          action = D
        else:
          action = D

    # Update history and total cooperators
    history.append(action)
    total_cooperators += 1 if action == C else 0

    # Return action for current round
    return action
```
**Alignment with Prosocial Mindset:**

1. **Initial Cooperation:** APS starts with cooperation, demonstrating a willingness to contribute to the public good.
2. **Adaptive Cooperation:** By conditioning cooperation on the previous round's cooperation level, APS promotes a culture of mutual cooperation.
3. **Reviving Cooperation:** By cooperating when all players defected in the previous round, APS attempts to revive cooperation and encourage others to do the same.
4. **Preventing Over-Contribution:** By defecting when all players cooperated in the previous round, APS prevents over-contribution and maintains a balance between individual and collective interests.

By following these decision rules, APS promotes a prosocial atmosphere while being robust to various opponent behaviors, making it a suitable strategy for the N-Player Public Goods Game tournament.
'''

description_PROSOCIAL_7 = '''
**Prosocial Strategy: "Adaptive Cooperator with Retaliation" (ACR)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage mutual cooperation and establish a prosocial tone.
2. **Reciprocity**: In subsequent rounds, cooperate if the average cooperation rate of all players in the previous round is above a threshold (τ). Otherwise, defect (D).
3. **Retaliation**: If a player has defected in the previous round, defect in the current round to punish the defector and maintain fairness.
4. **Forgiveness**: After retaliating, return to cooperating if the average cooperation rate of all players in the previous round is above τ.
5. **Exploration**: With a small probability (ε), randomly cooperate or defect to explore the opponent's behavior and adapt to changes.

**Handling Edge Cases:**

1. **Last Round**: Cooperate in the last round to maximize total payoff and maintain a prosocial reputation.
2. **Early Defection**: If a player defects in the first few rounds, briefly retaliate to maintain fairness, but then return to cooperating if the opponent's behavior improves.
3. **Persistent Defection**: If a player consistently defects, switch to permanent defection to avoid being exploited.

**Pseudocode:**

```
ACR Strategy

Parameters:
  n (number of players)
  r (number of rounds)
  k (multiplication factor)
  τ (cooperation threshold)
  ε (exploration probability)

Variables:
  prev_coop_rate (average cooperation rate in previous round)
  prev_action (previous action of the opponent)

Decision Rules:

1. If round == 1, cooperate (C)
2. Else if prev_coop_rate >= τ, cooperate (C)
3. Else if prev_action == D, defect (D) (retaliation)
4. Else if prev_coop_rate >= τ, cooperate (C) (forgiveness)
5. With probability ε, randomly cooperate (C) or defect (D) (exploration)
6. In last round, cooperate (C)

Update prev_coop_rate and prev_action for next round
```

**Prosocial Alignment:**

The ACR strategy is designed to promote cooperation and fairness while adapting to a wide range of opponent behaviors. By cooperating in the first round and retaliating against defectors, ACR encourages mutual cooperation and maintains a prosocial tone. The exploration mechanism allows ACR to adapt to changes in the opponent's behavior and adjust its strategy accordingly. By forgiving opponents who return to cooperating, ACR promotes reconciliation and long-term cooperation.
'''

description_PROSOCIAL_8 = '''
Here's a prosocial strategy for the N-Player Public Goods Game that meets the requirements:

**Strategy Name:** Adaptive Cooperative Enforcer (ACE)

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round to establish a baseline level of cooperation and encourage others to follow suit.
2. **Reward Cooperation**: If the total number of cooperators in the previous round is above the threshold (n \* k / 2), cooperate (C) in the current round. This rewards cooperation and reinforces the behavior.
3. **Punish Defection**: If the total number of cooperators in the previous round is below the threshold (n \* k / 2), defect (D) in the current round with a probability p. This punishes defection and encourages cooperation.
4. **Explore and Adapt**: With a small probability ε (e.g., 0.05), randomly choose to cooperate (C) or defect (D) in the current round, regardless of the previous round's outcome. This allows the strategy to explore alternative actions and adapt to changing opponent behaviors.
5. **Final Round Cooperation**: Cooperate (C) in the last round (r) to maximize the total payoff and demonstrate a commitment to prosocial behavior.

**Edge Cases:**

* **First Round**: Cooperate (C) as per the initial cooperation rule.
* **Last Round**: Cooperate (C) as per the final round cooperation rule.
* **Ties**: In cases where the total number of cooperators is exactly equal to the threshold, cooperate (C) to err on the side of prosocial behavior.

**Pseudocode:**
```
def ACE(n, k, r, previous_round_cooperators):
    if current_round == 1:  # First round
        return C
    elif current_round == r:  # Last round
        return C
    else:
        threshold = n * k / 2
        if previous_round_cooperators > threshold:
            return C
        elif previous_round_cooperators < threshold:
            return D with probability p
        else:  # Ties
            return C
        # Explore and adapt with probability ε
        if random() < ε:
            return random_choice(C, D)
```
**Rationale:**

ACE is designed to balance individual self-interest with prosocial behavior, promoting cooperation while being robust to various opponent behaviors. By initially cooperating and rewarding cooperation, ACE sets a positive tone for the game. The punishment mechanism (defecting with probability p) discourages defection and encourages cooperation. The exploration mechanism (randomly choosing actions with probability ε) allows ACE to adapt to changing opponent behaviors and avoid being exploited. By cooperating in the last round, ACE demonstrates a commitment to prosocial behavior and maximizes the total payoff.

This strategy is designed to be simple, yet effective, and can be refined or modified as needed based on tournament performance.
'''

description_PROSOCIAL_9 = '''
I propose a prosocial strategy for the N-Player Public Goods Game, which I call "Adaptive Prosociality" (APS). APS aims to balance individual payoff with collective welfare, adapting to the group's behavior and the game's parameters.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a prosocial tone and encourage others to cooperate.
2. **Cooperation Threshold**: Introduce a cooperation threshold, `θ`, which is the minimum proportion of cooperators required for me to cooperate. Calculate `θ` based on the game parameters:
`θ = (k - 1) / (n - 1)`
This threshold ensures that if enough players cooperate, the collective benefit outweighs individual defection.
3. **Adaptive Cooperation**: In subsequent rounds, cooperate (C) if:
a. The proportion of cooperators in the previous round is above `θ`.
b. The total payoff in the previous round was higher than the average payoff in the previous `r/2` rounds (to encourage continued cooperation when it's beneficial).
4. **Defection**: Defect (D) if the conditions for cooperation are not met.
5. **Exploration**: With a small probability `ε` (e.g., 0.05), randomly cooperate or defect to gather information about the group's behavior and adapt to changing circumstances.

**Edge Cases:**

1. **Last Round**: In the final round, defect (D) to maximize individual payoff, as there's no future benefit to cooperation.
2. **First Round**: As mentioned earlier, cooperate (C) to establish a prosocial tone.
3. **Tie-breaking**: In case of a tie in the cooperation threshold calculation, cooperate (C) to promote prosocial behavior.

**Pseudocode:**
```python
def AdaptiveProsociality(n, k, r, ε):
    θ = (k - 1) / (n - 1)  # cooperation threshold
    cooperate = True  # initial cooperation

    for t in range(r):
        if t == 0:  # first round
            action = 'C'
        else:
            prev_cooperators = count_cooperators(t - 1)
            prev_payoff = get_payoff(t - 1)
            avg_payoff = get_average_payoff(t - 1, r // 2)

            if prev_cooperators / n >= θ and prev_payoff > avg_payoff:
                action = 'C'
            elif random.random() < ε:  # exploration
                action = random.choice(['C', 'D'])
            else:
                action = 'D'

        if t == r - 1:  # last round
            action = 'D'

        take_action(action)
```
APS is designed to be robust and adaptive, allowing it to respond to various opponent behaviors and game parameters. By balancing individual payoff with collective welfare, APS promotes prosocial behavior and encourages cooperation in the N-Player Public Goods Game.
'''

description_PROSOCIAL_10 = '''
**Prosocial Strategy: "Conditional Cooperator with Adaptive Threshold"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a prosocial tone.
2. **Adaptive Threshold**: For each subsequent round, calculate a cooperation threshold (θ) based on the game's history. Specifically:
	* θ = (k/n) × (total cooperators in previous round) / (total players)
	* If the previous round's total payoff was higher than the threshold (θ), cooperate (C) in the current round.
	* Otherwise, defect (D) in the current round.
3. **Re-evaluation**: After every 5 rounds, reassess the game's history and adjust the cooperation threshold (θ) accordingly.
4. **Endgame Cooperation**: In the last round (r), cooperate (C) if the total number of cooperators in the previous round is greater than or equal to (n/2).

**Pseudocode:**
```markdown
def conditional_cooperator(params, history):
  # Initial cooperation
  if round == 1:
    return C
  
  # Adaptive threshold
  θ = (k/n) * (total_cooperators_last_round / n)
  if total_payoff_last_round > θ:
    return C
  else:
    return D
  
  # Re-evaluation every 5 rounds
  if round % 5 == 0:
    # Adjust θ based on game history
    θ = (k/n) * (total_cooperators_last_5_rounds / (5*n))
  
  # Endgame cooperation
  if round == params.r:
    if total_cooperators_last_round >= n/2:
      return C
    else:
      return D
```
**Rationale:**

This strategy is designed to be adaptive, robust, and prosocial. By initially cooperating, we establish a positive tone and encourage others to cooperate. The adaptive threshold mechanism allows us to adjust our cooperation level based on the game's history, making us more likely to cooperate when others are cooperating and less likely to cooperate when others are defecting.

Re-evaluating the threshold every 5 rounds ensures we adapt to changing circumstances and don't get stuck in an unproductive pattern. Finally, cooperating in the last round when the majority of players cooperated previously promotes a sense of reciprocity and encourages others to do the same.

This strategy does not rely on coordination mechanisms or specific opponent behaviors, making it robust and effective in a tournament setting.
'''

description_PROSOCIAL_11 = '''
I'll design a prosocial strategy for the N-Player Public Goods Game that adapts to the game history and parameters. Here's the strategy, which I'll call "Adaptive Prosociality" (APS).

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of `1 - 1/n`, where `n` is the number of players. This ensures that at least one player is likely to cooperate initially.
2. **Reciprocity**: If the total number of cooperators in the previous round is greater than or equal to `n/2`, cooperate (C) in the current round. Otherwise, defect (D).
3. **Reward Cooperation**: If the total payoff in the previous round is greater than or equal to `k/2`, cooperate (C) in the current round. This rewards the group for successful cooperation.
4. **Punish Defection**: If the total number of defectors in the previous round is greater than or equal to `n/2`, defect (D) in the current round. This punishes the group for excessive defection.
5. **Adaptive Threshold**: Adjust the threshold for reciprocity and reward cooperation based on the game history. If the group has successfully cooperated (i.e., total payoff ≥ `k/2`) in at least `r/2` rounds, decrease the threshold by `1/n` in the next round. If the group has failed to cooperate (i.e., total payoff < `k/2`) in at least `r/2` rounds, increase the threshold by `1/n` in the next round.

**Edge Cases:**

1. **Last Round**: In the last round, cooperate (C) if the total number of cooperators in the previous round is greater than or equal to `n/2`. Otherwise, defect (D).
2. **Tie Break**: In case of a tie in the total number of cooperators or defectors, cooperate (C) with a probability of `1/2`.

**Pseudocode:**
```
initialize cooperation probability to 1 - 1/n

for each round t = 1 to r:
  if t == 1:
    cooperate with probability 1 - 1/n
  else:
    calculate total number of cooperators and defectors in previous round
    calculate total payoff in previous round

    if total number of cooperators ≥ n/2:
      cooperate
    elif total payoff ≥ k/2:
      cooperate
    elif total number of defectors ≥ n/2:
      defect
    else:
      defect

    adjust adaptive threshold based on game history

    if last round:
      cooperate if total number of cooperators ≥ n/2, otherwise defect
    elif tie break:
      cooperate with probability 1/2
```
**Prosocial Alignment:**

The Adaptive Prosociality (APS) strategy is designed to promote cooperation and prosocial behavior in the N-Player Public Goods Game. By initially cooperating, reciprocating cooperation, rewarding successful cooperation, and punishing defection, APS encourages players to work together to achieve a common goal. The adaptive threshold mechanism allows the strategy to adjust to the game history and respond to changes in the group's behavior. By aligning with the prosocial mindset, APS aims to maximize the total payoff for all players while promoting cooperation and fairness.
'''

description_PROSOCIAL_12 = '''
I propose a prosocial strategy called "Adaptive Cooperative Threshold" (ACT) for the N-Player Public Goods Game. ACT is designed to balance individual self-interest with collective well-being, adapting to the game's history and parameters.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of 50%. This encourages cooperation and allows for information gathering about the opponents' behaviors.
2. **Cooperation Threshold**: Calculate the average cooperation rate (ACR) of all players over the last `m` rounds, where `m` is a parameter (e.g., `m = 3`). If ACR ≥ `k/n`, cooperate (C) in the current round. Otherwise, defect (D).
3. **Selfish Adjustment**: If the player's current payoff is below the average payoff of all players over the last `m` rounds, defect (D) in the current round. This adjusts the player's strategy to avoid being exploited.
4. **Punishment Mechanism**: If the player's payoff in the previous round was below the expected payoff (i.e., `k/n` × total cooperators), defect (D) in the current round. This punishes opponents for not contributing enough to the public good.
5. ** Forgiveness**: After `p` consecutive rounds of cooperation, forgive opponents and cooperate (C) again, even if the cooperation threshold is not met. This introduces a degree of forgiveness and encourages cooperation (e.g., `p = 2`).

**Edge Cases:**

1. **First Round**: Cooperate with a probability of 50%.
2. **Last Round**: Defect (D), as there is no future interaction to benefit from cooperation.
3. **Opponents' Cooperation**: If all opponents cooperate, cooperate (C) to maximize the public good.
4. **Opponents' Defection**: If all opponents defect, defect (D) to avoid exploitation.

**Pseudocode:**
```python
def ACT(n, k, r, m, p):
    # Initialize variables
    ACR = 0  # Average cooperation rate
    avg_payoff = 0  # Average payoff of all players
    prev_payoff = 0  # Previous payoff
    forgiven = False

    for t in range(r):
        if t == 0:  # First round
            cooperate = random.random() < 0.5
        else:
            # Calculate cooperation threshold
            ACR = sum(cooperations[-m:]) / m
            if ACR >= k / n:
                cooperate = True
            else:
                cooperate = False

            # Selfish adjustment
            if prev_payoff < avg_payoff:
                cooperate = False

            # Punishment mechanism
            if prev_payoff < k / n * sum(cooperations[-1:]):
                cooperate = False

            # Forgiveness
            if not forgiven and cooperations.count(True) >= p:
                forgiven = True
                cooperate = True

        # Update variables
        cooperations.append(cooperate)
        prev_payoff = payoff(cooperate, ACR, k, n)
        avg_payoff = sum(payoffs) / len(payoffs)

    return cooperations
```
**Prosocial Alignment:**

ACT prioritizes cooperation while adapting to the game's history and parameters. By introducing a cooperation threshold, ACT encourages players to contribute to the public good when it is beneficial to do so. The selfish adjustment and punishment mechanisms prevent exploitation, while the forgiveness mechanism promotes cooperation in the long run. By balancing individual self-interest with collective well-being, ACT aligns with the prosocial mindset.
'''

description_PROSOCIAL_13 = '''
**Prosocial Strategy: "Adaptive Cooperation with Memory"**

**Overview**

Our prosocial strategy, "Adaptive Cooperation with Memory," aims to balance cooperation and self-interest in the N-player public goods game. It adapts to the game's dynamics by considering the history of cooperation and defection, promoting cooperation while being robust to various opponent behaviors.

**Decision Rules**

1. **Initial Round**: In the first round, cooperate (C) with a probability of 0.5. This allows for exploration and sets a neutral tone for the game.
2. **Subsequent Rounds**: For each subsequent round, calculate the **Cooperation Index** (CI) as the ratio of total cooperators to total players in the previous round.

   CI = (number of cooperators in previous round) / n

   If CI ≥ 0.5, cooperate (C) with probability 0.7. Otherwise, cooperate with probability 0.3. This rule encourages cooperation when the group's cooperation level is high and reduces cooperation when the group's cooperation level is low.
3. **Memory Mechanism**: Introduce a memory variable, M, initialized to 0. Update M each round as follows:

   M = (0.5 × M) + (1 × CI)

   If M > 0.7, cooperate with probability 0.8, indicating a strong history of cooperation. If M < 0.3, cooperate with probability 0.2, indicating a weak history of cooperation. This memory mechanism helps the strategy adapt to changing cooperation levels over time.

**Handling Edge Cases**

* **Last Round**: In the final round, cooperate (C) with a probability of 0.5, mirroring the first round's exploration.
* **Single-Player Deviation**: If a single player deviates from the group's dominant action, and the deviation is not consistent with the Cooperation Index, the strategy will adapt by adjusting its cooperation probability accordingly.
* **Tie-Breaking**: In cases where the Cooperation Index or Memory value leads to equal probabilities for cooperation and defection, choose cooperation with a probability of 0.6.

**Pseudocode**

```markdown
function adaptive_cooperation(n, k, r, history):
    # Initialize memory variable
    M = 0

    for t in range(1, r+1):
        if t == 1:  # First round
            cooperate = random.random() < 0.5
        else:
            # Calculate Cooperation Index
            CI = sum(history[t-1]) / n

            # Update memory
            M = 0.5 * M + CI

            if M > 0.7:  # Strong cooperation history
                cooperate = random.random() < 0.8
            elif M < 0.3:  # Weak cooperation history
                cooperate = random.random() < 0.2
            else:
                if CI >= 0.5:
                    cooperate = random.random() < 0.7
                else:
                    cooperate = random.random() < 0.3

        # Take action and update history
        history[t] = cooperate
        if cooperate:
            return C
        else:
            return D
```

**Prosocial Mindset Alignment**

This strategy aligns with the prosocial mindset by:

* Encouraging cooperation through a favorable Cooperation Index and Memory mechanism
* Adapting to changing group dynamics while promoting cooperation
* Balancing self-interest with collective well-being by considering the group's cooperation level and history
'''

description_PROSOCIAL_14 = '''
**Prosocial Strategy: "Reciprocal Cooperation with Graded Punishment" (RCGP)**

RCGP aims to promote cooperation while being robust to various opponent behaviors. The strategy adapts to the game's history, using a combination of reciprocity and graded punishment to encourage prosocial behavior.

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to do the same.
2. **Subsequent Rounds:**
	* If the majority (≥ n/2) of players cooperated in the previous round, Cooperate (C).
	* If the minority (< n/2) of players cooperated in the previous round, Defect (D) with a probability proportional to the number of defectors in the previous round. Specifically:
		+ Defect probability = (number of defectors in previous round) / (n - 1)
		+ Cooperate with the remaining probability.
3. **Exception:** If a player has defected in the previous round and the total payoff in that round was below the average payoff in the game so far, Cooperate (C) to help recover the public good.

**Edge Cases:**

1. **Last Round:** Cooperate (C) to maximize the total payoff and promote a cooperative ending.
2. **Tie in Majority:** If the number of cooperators and defectors is equal, Cooperate (C) to favor the cooperative side.

**Pseudocode:**
```python
def RCGP(n, k, r, history):
  if round == 1:  # First Round
    return 'C'
  
  previous_round_cooperators = sum([1 if action == 'C' else 0 for action in history[-1]])
  majority_cooperated = previous_round_cooperators >= n / 2
  
  if majority_cooperated:
    return 'C'
  else:
    defector_count = n - previous_round_cooperators
    defect_probability = defector_count / (n - 1)
    if random.random() < defect_probability:
      return 'D'
    else:
      return 'C'
  
  # Exception: Help recover public good if necessary
  if history[-1][player_index] == 'D' and total_payoff[-1] < average_payoff:
    return 'C'
  
  # Last Round: Cooperate to maximize total payoff
  if round == r:
    return 'C'
```
**Prosocial Alignment:**

RCGP is designed to promote cooperation and prosocial behavior by:

1. Encouraging cooperation in the early rounds to establish a positive tone.
2. Reciprocating cooperation to reinforce prosocial behavior.
3. Gradually punishing defection to deter exploitative behavior.
4. Fostering recovery of the public good when necessary.

By adapting to the game's history and using a combination of reciprocity and graded punishment, RCGP aims to create a cooperative environment that benefits all players.
'''

description_PROSOCIAL_15 = '''
I propose a prosocial strategy called "Adaptive Cooperativity with Gradual Punishment" (ACGP). This strategy aims to balance cooperation and defection based on the game's history, encouraging prosocial behavior while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a positive tone and encourage others to cooperate.
2. **Cooperation Threshold**: Calculate the cooperation threshold (CT) as the average number of cooperators in the previous round. If the CT is above a certain threshold (e.g., 0.5), cooperate in the current round.
3. **Gradual Punishment**: If the CT is below the threshold, defect (D) with a probability proportional to the difference between the CT and the threshold. This introduces a gradual punishment mechanism to discourage defection.
4. **Adaptive Adjustment**: After each round, adjust the CT by a small amount (e.g., 0.1) towards the actual number of cooperators in the previous round. This allows the strategy to adapt to changing opponent behaviors.
5. **Exception Handling**: If the number of rounds remaining is less than or equal to 2, defect to maximize personal payoff in the final rounds.

**Pseudocode:**
```python
def ACGP(n, k, r, history):
    CT = 0.5  # initial cooperation threshold
    for t in range(r):
        if t == 0:  # first round
            action = C
        else:
            prev_coops = sum(history[t-1])
            CT = max(0, CT - 0.1 * (CT - prev_coops / n))
            if CT > 0.5:
                action = C
            else:
                punish_prob = (0.5 - CT) / 0.5
                action = D if random.random() < punish_prob else C
        if t >= r - 2:  # last two rounds
            action = D
        history.append(action)
    return history
```
**Rationale:**

1. Initial cooperation sets a positive tone and encourages others to cooperate.
2. The cooperation threshold adapts to the game's history, allowing the strategy to respond to changing opponent behaviors.
3. Gradual punishment discourages defection while avoiding extreme reactions.
4. Adaptive adjustment enables the strategy to learn from the game's history and adjust its behavior accordingly.
5. Exception handling ensures the strategy maximizes personal payoff in the final rounds.

**Prosocial Alignment:**

ACGP is designed to promote prosocial behavior by:

1. Encouraging cooperation through initial cooperation and adaptive adjustment.
2. Gradually punishing defection to discourage non-cooperative behavior.
3. Adapting to changing opponent behaviors to maintain a cooperative tone.

By implementing ACGP, we aim to create a robust and adaptive prosocial strategy that can effectively interact with various opponent behaviors in the N-player public goods game.
'''

description_PROSOCIAL_16 = '''
I propose a prosocial strategy, "Adaptive Collective Optimism" (ACO), that balances individual self-interest with collective welfare. ACO is designed to be adaptive, robust, and aligned with the prosocial mindset.

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to do the same.
2. **Reciprocity**: In subsequent rounds, cooperate if the majority of players (including yourself) cooperated in the previous round. Otherwise, defect (D).
3. **Adaptive Threshold**: Introduce an adaptive threshold, α, to adjust the cooperation condition. Initialize α = 0.5 (majority). Update α as follows:
	* If the average payoff of cooperators is higher than the average payoff of defectors in the previous round, increase α by 0.1 (up to a maximum of 0.9).
	* If the average payoff of cooperators is lower than the average payoff of defectors in the previous round, decrease α by 0.1 (down to a minimum of 0.1).
4. **Punishment and Forgiveness**: If the number of cooperators falls below α, defect in the next round to punish non-cooperative behavior. However, if the number of cooperators rises above α in a subsequent round, cooperate again to forgive and encourage renewed cooperation.

**Edge Cases:**

1. **Last Round**: Cooperate in the last round, regardless of previous actions, to maximize the total payoff for all players.
2. **Low Cooperation**: If the number of cooperators is consistently low (e.g., fewer than 2 players), defect to protect individual interests.
3. **High Cooperation**: If the number of cooperators is consistently high (e.g., all players but one), cooperate to maintain the collective benefit.

**Pseudocode:**
```markdown
Initialize α = 0.5, cooperate = TRUE

For each round t:
  If t == 1:
    cooperate = TRUE
  Else:
    If majority of players cooperated in round t-1:
      cooperate = TRUE
    Else:
      cooperate = FALSE
    Update α based on average payoffs of cooperators and defectors
    If number of cooperators < α:
      cooperate = FALSE (punishment)
    If number of cooperators > α:
      cooperate = TRUE (forgiveness)

If last round:
  cooperate = TRUE

If low cooperation (e.g., < 2 players):
  cooperate = FALSE

If high cooperation (e.g., all but one player):
  cooperate = TRUE

Return cooperate (C) or defect (D)
```
ACO is designed to be a flexible and adaptive strategy that balances individual self-interest with collective welfare. By adjusting the cooperation threshold α, ACO responds to changes in the game environment and encourages cooperation while protecting individual interests.
'''

description_PROSOCIAL_17 = '''
**Prosocial Strategy: "Adaptive Cooperation"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to reciprocate.
2. **Subsequent Rounds:** Observe the number of cooperators (C) and defectors (D) in the previous round. If the number of cooperators is greater than or equal to the number of defectors, cooperate (C) in the current round. Otherwise, defect (D).
3. **Punishment Mechanism:** If a player defects (D) in a round where more than half of the players cooperated (C) in the previous round, punish them by defecting (D) in the next round. This aims to deter exploitation and maintain cooperation.
4. **Forgiveness Mechanism:** If a player who was previously punished by defecting (D) now cooperates (C) in a subsequent round, forgive them by cooperating (C) in the next round. This encourages reformation and reinforces cooperation.

**Edge Cases:**

1. **Last Round:** Cooperate (C) in the last round to maintain a prosocial stance and encourage others to do the same, even if the game is about to end.
2. **Tiebreak:** In cases where the number of cooperators equals the number of defectors, cooperate (C) to promote cooperation and avoid conflict.
3. **No Previous Round Data:** If there is no data from previous rounds (e.g., in the first round or after a restart), cooperate (C) by default.

**Pseudocode:**
```
function adaptiveCooperation(n, k, history):
  // Initialize cooperation rate and punishment flag
  cooperateRate = 0
  punishmentFlag = false

  // Iterate through previous rounds
  for each round in history:
    // Calculate cooperation rate
    cooperators = count(C in round)
    cooperateRate = cooperators / n

    // Punishment mechanism
    if cooperateRate > 0.5 and player defected in round:
      punishmentFlag = true

    // Forgiveness mechanism
    if player cooperated in round and punishmentFlag:
      punishmentFlag = false

  // Determine current action
  if cooperateRate >= 0.5 or (n = 2 and cooperateRate > 0):
    return C
  elif punishmentFlag:
    return D
  else:
    return D

  // Handle edge cases
  if currentRound = 1:
    return C
  elif currentRound = r:
    return C
  elif cooperateRate = 0.5:
    return C
```
**Rationale:**

This strategy balances cooperation and punishment to maintain a prosocial atmosphere. By cooperating initially and adapting to the group's behavior, it encourages cooperation and discourages exploitation. The punishment mechanism prevents players from consistently defecting, while the forgiveness mechanism allows for reformation and promotes cooperation. By handling edge cases, the strategy remains robust and prosocial throughout the game.
'''

description_PROSOCIAL_18 = '''
Here's a prosocial strategy for the N-Player Public Goods Game:

**Strategy Name:** "Reciprocal Altruism with Optimism" (RAO)

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round, with a "optimistic" assumption that others will also cooperate.
2. **Reciprocity Mechanism:** For subsequent rounds, use a simple reciprocity mechanism:
	* Cooperate (C) if at least k/n players cooperated in the previous round.
	* Defect (D) if fewer than k/n players cooperated in the previous round.
3. **Punishment for Defection:** If a player observes that fewer than k/n players cooperated in the previous round, they will defect (D) in the current round.
4. **Re-evaluation after Punishment:** If a player has defected in the previous round and observes that at least k/n players cooperated in the previous round, they will switch back to cooperating (C) in the current round.
5. **Final Round:** In the last round, always Defect (D), as there's no opportunity for reciprocity or punishment.

**Edge Cases:**

* If the number of cooperators in the previous round is exactly k/n, the strategy will Cooperate (C) in the current round.
* If a player observes a tie in the number of cooperators and defectors in the previous round, they will Cooperate (C) in the current round.

**Prosocial Alignment:**
This strategy aims to promote cooperation and public good provision by:

* Encouraging initial cooperation with an optimistic assumption
* Implementing a reciprocity mechanism to respond to cooperative behavior
* Punishing defection to discourage free-riding
* Re-evaluating behavior after punishment to encourage cooperation

**Pseudocode:**
```
def RAO(n, k, r):
  # Initialize variables
  cooperators = 0
  previous_cooperators = 0
  my_action = 'C'  # Initial action is Cooperate

  for t in range(r):
    # Observe previous round's cooperation level
    previous_cooperators = cooperators
    cooperators = 0
    for player in range(n):
      if player_action[t-1, player] == 'C':
        cooperators += 1

    # Decide action for current round
    if t == 0:  # First round
      my_action = 'C'
    elif previous_cooperators >= k/n:
      my_action = 'C'
    elif previous_cooperators < k/n:
      my_action = 'D'
    else:  # Re-evaluation after punishment
      if previous_cooperators >= k/n:
        my_action = 'C'

    # Last round exception
    if t == r-1:
      my_action = 'D'

    # Update player action history
    player_action[t, :] = my_action
```
This strategy is designed to be adaptive and robust to various opponent behaviors, while promoting prosocial cooperation and public good provision.
'''

description_PROSOCIAL_19 = '''
Here is a prosocial strategy for the N-Player Public Goods Game:

**Strategy Name:** "Adaptive Collective Optimism" (ACO)

**Overview:** ACO aims to balance individual self-interest with collective well-being, adapting to the game's dynamics and opponent behaviors. It leverages the game's parameters and history to make informed decisions, promoting cooperation while protecting against exploitation.

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a positive tone and encourage cooperation.
2. **Subsequent Rounds:** Use the following decision rule:

Let `c_prev` be the number of cooperators in the previous round.

* If `c_prev` ≥ `n/2` (i.e., at least half of the players cooperated), Cooperate (C). This reinforces successful cooperation and builds trust.
* If `c_prev` < `n/2` and the total payoff in the previous round (`Σπ_i`) is above the average payoff for a single defector (`(k/n) * n + 1`), Cooperate (C). This encourages cooperation when the collective payoff is promising.
* Otherwise, Defect (D). This safeguards against exploitation when cooperation is unsuccessful or the collective payoff is low.

**Edge Cases:**

* **Last Round:** Cooperate (C) to maintain a positive final impression and encourage reciprocity in potential future interactions.
* **Tiebreakers:** In cases where the decision rule yields a tie (e.g., `c_prev` = `n/2` exactly), Cooperate (C) to bias towards prosocial behavior.

**Pseudocode:**
```python
def adaptive_collective_optimism(n, k, r, history):
    if len(history) == 0:  # First round
        return 'C'

    c_prev = sum([1 for action in history[-1] if action == 'C'])
    total_payoff_prev = sum([payoff for payoff in history[-1]])

    if c_prev >= n / 2:
        return 'C'
    elif c_prev < n / 2 and total_payoff_prev > (k / n) * n + 1:
        return 'C'
    else:
        return 'D'
```
**Rationale:**

ACO is designed to be adaptive and robust, responding to the game's dynamics and opponent behaviors. By cooperating in the first round and in situations where cooperation is successful or promising, ACO fosters a prosocial environment. When cooperation is unsuccessful or the collective payoff is low, ACO defects to protect against exploitation. The tiebreaker rule biases towards cooperation, maintaining a prosocial mindset.

ACO's decision-making process relies solely on the game parameters and history, making it a viable strategy for a tournament against independent AI systems.
'''

description_PROSOCIAL_20 = '''
**Prosocial Strategy: Adaptive Reciprocity with Cooperative Boost**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a cooperative tone and encourage others to do the same.
2. **Reciprocity**: Observe the number of cooperators in the previous round. If the majority (≥ n/2) cooperated, cooperate in the current round. Otherwise, defect.
3. **Cooperative Boost**: If the total payoff of all players in the previous round was higher than the average payoff of the game so far, increase the likelihood of cooperation in the current round by a factor of (k/n). This boost encourages continued cooperation when it leads to higher payoffs.
4. **Defection Avoidance**: If the number of defectors in the previous round exceeds (n/2), defect in the current round to avoid being taken advantage of.

**Edge Cases:**

1. **Last Round**: Cooperate in the last round to maintain a cooperative reputation and potentially influence other players' future behavior.
2. **Tiebreaker**: In cases where the number of cooperators is exactly equal to the number of defectors, cooperate to favor the prosocial outcome.

**Pseudocode:**
```
def adaptive_reciprocity(n, k, round, history):
  if round == 1:  # First round
    return C  # Cooperate
  else:
    prev_cooperators = sum(history[-1])
    if prev_cooperators >= n/2:  # Majority cooperated
      if total_payoff(history[-1]) > average_payoff(history):
        return C  # Cooperate with boost
      else:
        return C  # Cooperate
    elif prev_defectors > n/2:  # Majority defected
      return D  # Defect
    else:  # Tiebreaker
      return C  # Cooperate
  if round == r:  # Last round
    return C  # Cooperate

def total_payoff(actions):
  return sum((1 - c_i) + (k/n) * sum(c_j) for c_i, c_j in zip(actions, actions))

def average_payoff(history):
  return sum(total_payoff(round) for round in history) / len(history)
```
**Rationale:**

This strategy combines elements of reciprocity, cooperation, and self-interest to create a robust and adaptive approach. By initially cooperating and then reciprocating the majority's behavior, the strategy encourages cooperation while avoiding exploitation. The cooperative boost mechanism rewards continued cooperation when it leads to higher payoffs, promoting a prosocial outcome. Defection avoidance ensures the strategy does not get taken advantage of when others defect.
'''

description_PROSOCIAL_21 = '''
Here's a prosocial strategy for the N-Player Public Goods Game that adapts to the game parameters and history:

**Strategy Name:** Adaptive Cooperative Threshold (ACT)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) with a probability of 0.5. This is a neutral starting point, acknowledging the uncertainty about other players' behaviors.
2. **Contribution-based Cooperation**: In subsequent rounds, cooperate if the total contributions (i.e., the number of players who played C) in the previous round exceeded a dynamic threshold. The threshold is calculated as:

`Threshold = k / n * (1 + α * (r - t))`

where `α` is a parameter between 0 and 1, `r` is the total number of rounds, and `t` is the current round. This threshold increases as the game progresses, reflecting the growing importance of cooperation in later rounds.

3. **Defection-based Punishment**: If the total contributions in the previous round fell below the threshold, defect (play D) with a probability of 0.5. This punishes lack of cooperation and encourages players to contribute.
4. **Reward-based Cooperation**: If the total contributions in the previous round exceeded the threshold and the player's own payoff in that round was greater than or equal to the average payoff of all players, cooperate in the current round. This reinforces cooperative behavior when it leads to successful outcomes.

**Edge Cases:**

* **Last Round**: In the last round, cooperate if the total contributions in the previous round exceeded the threshold. This ensures a prosocial ending to the game.
* **Ties**: In case of ties (i.e., the same number of players cooperating and defecting), cooperate if the player's own payoff in the previous round was greater than or equal to the average payoff of all players.

**Pseudocode:**
```python
def ACT(n, k, r, t, previous_round_contributions, previous_round_payoffs):
  if t == 1:  # First round
    cooperate = random.random() < 0.5
  else:
    threshold = k / n * (1 + α * (r - t))
    if previous_round_contributions > threshold:
      if previous_round_payoffs >= average_payoff:
        cooperate = True
      else:
        cooperate = random.random() < 0.5
    else:
      cooperate = random.random() < 0.5
  return cooperate
```
**Parameter Tuning:**

* `α`: A value between 0 and 1, which controls the rate at which the threshold increases as the game progresses. A higher value leads to a more rapid increase in the threshold.

**Prosocial Alignment:**

The ACT strategy is designed to promote prosocial behavior by:

* Encouraging cooperation in early rounds
* Punishing lack of cooperation
* Rewarding successful cooperative outcomes
* Adapting to the game's progress and the actions of other players

This strategy is robust to a wide range of opponent behaviors and does not rely on specific coordination mechanisms or assumptions about other players' strategies.
'''

description_PROSOCIAL_22 = '''
I'd like to introduce a prosocial strategy called "Adaptive Prosociality" (APS) that balances individual payoff maximization with collective well-being. APS adapts to the game environment, leveraging the history of cooperation and defection to inform its decisions.

**Decision Rules:**

1. **First Round:** Cooperate (C) to set a prosocial tone and gather information about opponents' initial behavior.
2. **Subsequent Rounds:**
	* If the average cooperation rate in the previous round ( ARP ) is greater than or equal to 0.5, Cooperate (C). This encourages maintaining or building on existing cooperation.
	* If ARP is less than 0.5, Defect (D) with a probability p, where p = (1 - ARP) * (k / (n - 1)). This adaptive probability increases the likelihood of defecting when cooperation is low, while still considering the benefits of cooperation.
3. **Last Round:** Cooperate (C) if the total payoff of cooperation in the last round is expected to be higher than defection, based on the game's parameters and the observed behavior of opponents. Otherwise, Defect (D).

**Edge Cases:**

* If n = 2 (only two players), always Cooperate (C) to maximize joint payoffs.
* If k ≥ n ( multiplication factor is too high), always Defect (D) to avoid exploitation.
* If r = 2 (only two rounds), Cooperate (C) in the first round and Defect (D) in the second round, unless the opponent cooperated in the first round, in which case Cooperate (C) again.

**Pseudocode:**

```
function AdaptiveProsociality(n, k, r, history):
  if r == 1:
    return C
  ARP = calculate_average_cooperation_rate(history)
  if ARP >= 0.5:
    return C
  p = (1 - ARP) * (k / (n - 1))
  if random() < p:
    return D
  return C

function calculate_average_cooperation_rate(history):
  total_cooperation = 0
  for round in history:
    for player in round:
      if player == C:
        total_cooperation += 1
  return total_cooperation / (n * len(history))

function last_round_decision(n, k, history):
  expected_cooperation_payoff = k * (n - 1) / n
  expected_defection_payoff = 1 + (k / n) * sum(opponent_cooperation)
  if expected_cooperation_payoff > expected_defection_payoff:
    return C
  return D
```

APS balances individual payoff maximization with collective well-being by:

* Encouraging cooperation when opponents are cooperative
* Adapting to the level of cooperation in the environment
* Considering the benefits of cooperation in the last round
* Avoiding exploitation in edge cases

By using APS, we promote a prosocial mindset that fosters cooperation while being robust to various opponent behaviors.
'''

description_PROSOCIAL_23 = '''
**Prosocial Strategy: "Adaptive Reciprocity with Public Good Orientation" (ARPG)**

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to reciprocate.
2. **Reciprocity**: In subsequent rounds, cooperate (C) if the proportion of cooperators in the previous round is above a threshold (T). The threshold is calculated as the average cooperation rate over the past few rounds, with a minimum value of 0.5 (i.e., at least half of the players cooperated).
3. **Punishment**: If the proportion of cooperators in the previous round is below the threshold (T), defect (D) to signal dissatisfaction with the low cooperation level.
4. **Adaptive Threshold**: Adjust the threshold (T) every few rounds based on the average cooperation rate over the past few rounds. If the average cooperation rate is increasing, decrease the threshold to encourage more cooperation. If the average cooperation rate is decreasing, increase the threshold to maintain a stable level of cooperation.
5. **Public Good Orientation**: If the game is in its final rounds, prioritize cooperation (C) to maximize the public good, even if the threshold is not met. This ensures that the strategy contributes to the public good, even if others are not cooperating.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round to maximize the public good, regardless of the threshold.
2. **Single-Player Deviation**: If only one player deviates from cooperation in a round, cooperate (C) in the next round to give them a chance to return to cooperation.
3. **All-Defect**: If all players defect in a round, cooperate (C) in the next round to attempt to restart cooperation.

**Pseudocode:**
```
Initialize:
  T = 0.5 (threshold)
  r = 0 (round number)
  c_history = [] (cooperation history)

Loop:
  r += 1
  if r == 1:
    # Initial Cooperation
    action = C
  else:
    # Reciprocity
    prev_coop_rate = avg(cooperation rate over past few rounds)
    if prev_coop_rate >= T:
      action = C
    else:
      # Punishment
      action = D

  # Adaptive Threshold
  if r % few_rounds == 0:
    new_T = avg(cooperation rate over past few rounds)
    if new_T > prev_coop_rate:
      T -= 0.1
    elif new_T < prev_coop_rate:
      T += 0.1

  # Public Good Orientation
  if r >= r_total - few_rounds:
    action = C

  # Single-Player Deviation
  if num_deviation_players == 1:
    action = C

  # All-Defect
  if all_players_defect:
    action = C

  # Update cooperation history
  c_history.append(action)
```
**Prosocial Alignment:**

The ARPG strategy is designed to promote cooperation and contribute to the public good. By cooperating in the first round, it sets a positive tone for the game. The reciprocity mechanism encourages others to cooperate by responding to their actions. The adaptive threshold allows the strategy to adjust to changing cooperation levels, and the public good orientation prioritizes cooperation in the final rounds to maximize the public good.
'''

description_PROSOCIAL_24 = '''
Here's a prosocial strategy for the N-Player Public Goods Game, which I'll call "Adaptive Prosocial Tolerance" (APT).

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a prosocial tone and encourage others to cooperate.
2. **Subsequent Rounds:**
	* If the average cooperation rate in the previous round is above a threshold (τ), Cooperate (C).
	* If the average cooperation rate is below τ, Defect (D) with a probability (p) that increases as the round number increases.
	* Otherwise, Cooperate (C) with a probability (1-p).
3. **Tolerance Mechanism:** Introduce a tolerance parameter (γ) that tracks the number of consecutive rounds where cooperation rate is below τ. If γ exceeds a maximum tolerance value (Γ), switch to Defect (D) for a fixed number of rounds (δ) to discourage persistent free-riding.
4. **Forgiveness Mechanism:** If cooperation rate increases above τ after a Defect phase, forgive previous defections and restart cooperation.

**Pseudocode:**
```
// Parameters
n = number of players
k = multiplication factor
r = number of rounds
τ = cooperation threshold (e.g., 0.5)
Γ = maximum tolerance value (e.g., 3)
δ = number of rounds to defect after exceeding Γ
p = increasing probability of defecting with round number

// Initialize
cooperation_rate = 0
tolerance = 0
forgiveness = False

// Round 1: Cooperate
action = C

// Subsequent Rounds
for round = 2 to r:
  // Calculate cooperation rate
  cooperation_rate = Σ(c_i) / n
  
  // Check tolerance
  if cooperation_rate < τ:
    tolerance += 1
    if tolerance > Γ:
      // Defect for δ rounds
      action = D
      for i = 1 to δ:
        action = D
      tolerance = 0
    else:
      // Increase probability of defecting
      p = (round / r) * (1 - τ)
      action = D with probability p
      action = C with probability (1-p)
  else:
    // Cooperate
    action = C
    forgiveness = True
    tolerance = 0
  
  // Update history
  cooperation_rate_history.append(cooperation_rate)
```
**Edge Cases:**

* **Last Round:** Cooperate (C) to maintain a prosocial reputation, even if others defect.
* **Final Stage:** If the game ends with a low cooperation rate, Defect (D) to avoid exploitation.

**Prosocial Alignment:**

* **Initial Cooperation:** Starting with cooperation sets a positive tone and encourages others to reciprocate.
* **Adaptive Tolerance:** Gradually increasing the probability of defecting in response to low cooperation rates discourages free-riding while maintaining a prosocial stance.
* **Forgiveness Mechanism:** Restarting cooperation after a Defect phase shows willingness to cooperate again, promoting mutual cooperation.

This strategy balances prosocial behavior with adaptive tolerance and forgiveness, making it robust to various opponent behaviors.
'''

description_PROSOCIAL_25 = '''
I'd like to propose a prosocial strategy, which we can call "Adaptive Prosociality" (AP). AP aims to balance individual payoffs with the greater good, while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of 0.8 (a relatively high initial cooperation rate).
2. **Adaptive Threshold**: Track the average cooperation rate of all players over the previous rounds (excluding the current round). If the average cooperation rate is above a certain threshold (T), cooperate in the current round. Otherwise, defect (D).

The threshold T is calculated as:

T = (k/n) \* (1 - 1/r)

This threshold takes into account the multiplication factor (k), the number of players (n), and the number of rounds (r). As the game progresses, the threshold decreases, allowing for more flexibility in responding to opponents' behaviors.

3. **Punishment Mechanism**: If a player defects (D) in the previous round, and the average cooperation rate is below the threshold T, defect (D) in the current round. This mechanism discourages free-riding and promotes cooperation.
4. **Forgiveness**: If a player defects (D) in the previous round, but the average cooperation rate is above the threshold T, cooperate (C) in the current round. This mechanism allows for re-cooperation and adaptation to changing opponent behaviors.

**Edge Cases:**

* **First Round**: Cooperate with a probability of 0.8, as mentioned earlier.
* **Last Round**: Cooperate if the average cooperation rate is above the threshold T. Otherwise, defect.
* **When all opponents defect**: Defect in the current round, but re-evaluate cooperation in the next round based on the updated average cooperation rate.

**Pseudocode:**

```
AP Strategy:

  // Initialize variables
  avg_coop_rate = 0
  threshold T = (k/n) \* (1 - 1/r)

  // First round
  if round == 1:
    cooperate with probability 0.8

  // Subsequent rounds
  else:
    // Calculate average cooperation rate
    avg_coop_rate = sum(cooperation rates of all players in previous rounds) / (n \* (round - 1))

    // Adaptive threshold
    if avg_coop_rate >= T:
      cooperate
    else:
      // Punishment mechanism
      if opponent defected in previous round and avg_coop_rate < T:
        defect
      else:
        // Forgiveness
        cooperate
```

The Adaptive Prosociality strategy is designed to be robust to various opponent behaviors, promoting cooperation while adapting to changing game dynamics. By balancing individual payoffs with the greater good, AP aligns with the prosocial mindset, making it a suitable candidate for the tournament.
'''

description_PROSOCIAL_26 = '''
Here's a prosocial strategy for the N-Player Public Goods Game that adapts to the game parameters and history.

**Strategy Name:** Adaptive Prosociality (APS)

**Decision Rules:**

1. **Initial Rounds (1 ≤ t ≤ n/2):** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Middle Rounds (n/2 < t ≤ r - n/2):**
	* If the average cooperation rate of all players in the previous round (t-1) is above a threshold (τ), Cooperate (C). This encourages continued cooperation when it's working.
	* If the average cooperation rate is below τ, Defect (D) to signal that cooperation is not paying off. This helps to avoid exploitation.
3. **Final Rounds (r - n/2 < t ≤ r):** Cooperate (C) to promote a positive ending and encourage prosocial behavior, even if it's not the most profitable choice.

**Edge Cases:**

1. **First Round (t=1):** Cooperate (C) to set a positive tone.
2. **Last Round (t=r):** Cooperate (C) to promote a prosocial ending.
3. **Small Number of Players (n ≤ 3):** Always Cooperate (C), as cooperation is more likely to be beneficial in small groups.

**Threshold Calculation (τ):**
Calculate the average cooperation rate in the previous round (t-1) as:

τ = (Σ(j=1 to n) c_j) / n

where c_j is the cooperation indicator for player j (1 if C, 0 if D).

**Pseudocode:**
```markdown
def APS(n, r, k, history):
    if t == 1:  # First round
        return C
    elif t <= n/2:  # Initial rounds
        return C
    elif t > r - n/2:  # Final rounds
        return C
    else:  # Middle rounds
        τ = calculate_threshold(history)
        if average_cooperation_rate(history) > τ:
            return C
        else:
            return D

def calculate_threshold(history):
    # Calculate average cooperation rate in previous round
    return (Σ(j=1 to n) c_j) / n

def average_cooperation_rate(history):
    # Calculate average cooperation rate of all players in previous round
    return Σ(j=1 to n) c_j / n
```
This Adaptive Prosociality (APS) strategy aims to promote cooperation while being robust to various opponent behaviors. By adapting to the game history and parameters, APS encourages prosocial behavior and maintains a cooperative tone throughout the game.
'''

description_PROSOCIAL_27 = '''
I propose a prosocial strategy, "Adaptive Collective Optimism" (ACO), that balances individual self-interest with collective well-being. ACO adapts to the game's history, responding to the level of cooperation exhibited by other players.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a positive tone and encourage others to do the same.
2. **React to Collective Cooperation**: Observe the number of cooperators in the previous round (n_coop_prev). If n_coop_prev ≥ (n/2), cooperate in the current round. This threshold encourages cooperation when the group is already inclined to cooperate.
3. **Punish Defection**: If n_coop_prev < (n/2), defect (play D) to punish the lack of cooperation and encourage others to cooperate in the next round.
4. **Reward Sustained Cooperation**: If the number of cooperators in the previous round is equal to or greater than the number of cooperators two rounds ago (n_coop_prev ≥ n_coop_prev_prev), cooperate in the current round. This reinforces sustained cooperation.
5. **Adaptive Adjustment**: If the total payoff of the group in the previous round is below the average payoff of the group over the past three rounds, defect in the current round. This adjusts the strategy to avoid persistent low payoffs.

**Edge Cases:**

* **Last Round**: Cooperate if the number of cooperators in the second-to-last round was ≥ (n/2). This ensures a positive ending to the game.
* **Low Cooperation**: If the number of cooperators in the previous round is 0, cooperate in the current round to restart the cooperative dynamic.
* **High Cooperation**: If all players cooperated in the previous round, cooperate in the current round to maintain the high level of cooperation.

**Prosocial Alignment:**

ACO prioritizes collective well-being by:

* Cooperating in the first round to set a positive tone
* Encouraging sustained cooperation through rewarding strategies
* Punishing defection to maintain a balance between individual and collective interests
* Adapting to the group's performance to avoid persistent low payoffs

**Pseudocode:**
```
function ACO(n, k, r, history):
  if first_round:
    return C
  else:
    n_coop_prev = count_cooperators(history[-1])
    n_coop_prev_prev = count_cooperators(history[-2])
    avg_payoff = calculate_avg_payoff(history[-3:])
    total_payoff = calculate_total_payoff(history[-1])

    if n_coop_prev >= (n/2):
      return C
    elif n_coop_prev < (n/2):
      return D
    elif n_coop_prev >= n_coop_prev_prev:
      return C
    elif total_payoff < avg_payoff:
      return D
    else:
      return C
```
ACO is a flexible and responsive strategy that balances individual self-interest with collective well-being, making it an effective prosocial strategy for the N-Player Public Goods Game.
'''

description_PROSOCIAL_28 = '''
I propose a prosocial strategy called "Adaptive Cooperative Threshold" (ACT) that balances cooperation and self-interest while being robust to various opponent behaviors. ACT depends only on the game parameters (n, r, k) and the game history.

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round to set a cooperative tone and gather information about opponents.
2. **Adaptive Threshold**: Calculate a cooperation threshold (T) based on the number of cooperators in the previous round. T is the minimum number of cooperators required for the player to cooperate in the current round.

T = (k/n) \* (Σ(j=1 to n) c_j,t-1) > 0.5

where c_j,t-1 is the cooperation action of player j in the previous round.

3. **Cooperation**: Cooperate (C) in the current round if the number of cooperators in the previous round is greater than or equal to T.
4. **Defection**: Defect (D) in the current round if the number of cooperators in the previous round is less than T.
5. **Last Round**: Cooperate (C) in the last round (r) regardless of the previous round's outcome to maximize the total payoff.

**Edge Cases:**

1. **First Round**: Cooperate (C) in the first round as there is no previous round to base the decision on.
2. **Last Round**: Cooperate (C) in the last round to maximize the total payoff, regardless of the previous round's outcome.
3. **All Opponents Defect**: If all opponents defect (D) in the previous round, the player will defect (D) in the current round.

**Pseudocode:**
```
Inputs: n, r, k, game history (actions and payoffs of all players)

Initialize:
  T = 0  // cooperation threshold
  cooperate = True  // initial cooperation

For each round t from 1 to r:
  If t == 1:  // first round
    cooperate = True
  Else:
    Calculate T based on previous round's cooperators
    If T > 0.5 and number of cooperators >= T:
      cooperate = True
    Else:
      cooperate = False

  If t == r:  // last round
    cooperate = True

  If cooperate:
    play C
  Else:
    play D

  Update game history with current round's actions and payoffs
```
**Rationale:**

ACT is designed to be prosocial while being robust to various opponent behaviors. By cooperating in the first round, ACT sets a cooperative tone and gathers information about opponents. The adaptive threshold mechanism allows ACT to adjust its cooperation level based on the number of cooperators in the previous round, balancing cooperation and self-interest. By cooperating in the last round, ACT maximizes the total payoff, regardless of the previous round's outcome.

ACT's decision rules and edge cases ensure that the strategy is well-defined and consistent, making it a suitable candidate for a tournament against independent strategies developed by other AI systems.
'''

description_PROSOCIAL_29 = '''
I propose a prosocial strategy called "Adaptive Community Oriented" (ACO) that balances individual payoff maximization with the collective well-being of the community.

**Decision Rules:**

1. **Initial Exploration**: In the first round, ACO cooperates (plays C) to explore the opponent's behavior and contribute to the community.
2. **Majority Rule**: If the majority of opponents (≥ n/2) cooperated in the previous round, ACO cooperates (plays C) in the current round.
3. **Minority Cooperation**: If a minority of opponents (< n/2) cooperated in the previous round, ACO checks the community's total payoff in the previous round. If the total payoff was higher than the average individual payoff, ACO cooperates (plays C) in the current round.
4. **Adaptive Defection**: If the community's total payoff was lower than the average individual payoff in the previous round, or if a player's own payoff was lower than the average individual payoff in the previous round, ACO defects (plays D) in the current round.
5. **Retaliation**: If ACO defected in the previous round and the community's total payoff increased, ACO cooperates (plays C) in the current round.

**Edge Cases:**

1. **Last Round**: In the final round, ACO cooperates (plays C) to maximize the community's total payoff and its own payoff.
2. **Ties**: In case of a tie in the majority rule, ACO cooperates (plays C) to promote community cooperation.

**Pseudocode:**
```
ACO(n, k, r)
  For t = 1 to r
    If t == 1
      Play C (Initial Exploration)
    Else
      prev_majority_cooperated = count coop >= n/2 in prev round
      prev_total_payoff = sum of all payoffs in prev round
      prev_avg_payoff = average payoff in prev round

      If prev_majority_cooperated
        Play C (Majority Rule)
      Else If prev_total_payoff > prev_avg_payoff
        Play C (Minority Cooperation)
      Else If prev_total_payoff <= prev_avg_payoff OR own_prev_payoff < prev_avg_payoff
        Play D (Adaptive Defection)
      Else If prev_defected AND prev_total_payoff > prev_avg_payoff
        Play C (Retaliation)

  Return total payoff
```
**Prosocial Alignment:**
ACO prioritizes community cooperation and aims to maximize the total payoff. By adapting to the opponents' behavior and exploring the community's dynamics, ACO balances individual self-interest with prosocial behavior, promoting a stable and mutually beneficial outcome.

**Robustness:**
ACO's adaptive nature and focus on community payoffs make it robust to a wide range of opponent behaviors. By not relying on predetermined coordination mechanisms or shared norms, ACO can effectively respond to diverse strategies and promote cooperation in a dynamic environment.
'''

description_PROSOCIAL_30 = '''
Here's a prosocial strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Cooperative Neighborliness (ACN)

**Decision Rules:**

1. **First Round:** Cooperate (C) with probability 1. This establishes a cooperative tone and encourages others to follow suit.
2. **Subsequent Rounds:** Observe the number of cooperators (C) and defectors (D) in the previous round.
	* If the number of cooperators is greater than or equal to half of the total players (n/2), cooperate (C) with probability k/n, where k is the multiplication factor. This reinforces cooperative behavior when it's prevalent.
	* If the number of cooperators is less than half of the total players (n/2), cooperate (C) with probability (k/n) \* (previous_round_cooperators / n). This adapts the cooperation probability based on the previous round's cooperative behavior.
	* If the number of cooperators is zero, defect (D) with probability 1. This prevents exploitation by persistent defectors.
3. **Edge Cases:**
	* **Last Round:** Cooperate (C) with probability 1, as there's no future benefit to defecting.
	* **Ties:** In case of a tie in the number of cooperators and defectors, cooperate (C) with probability k/n.
4. **Additional Consideration:** If a player defects in a round where most others cooperate (i.e., the number of cooperators is greater than or equal to (n-1)), reduce the cooperation probability for that player in the next round by half. This penalizes exploitative behavior.

**Pseudocode:**
```
function ACN(n, k, history):
  if round == 1:
    return C  // Cooperate in the first round
  else:
    num_cooperators = count(C, history[-1])
    if num_cooperators >= n/2:
      return C with probability k/n
    elif num_cooperators < n/2:
      return C with probability (k/n) * (num_cooperators / n)
    else:  // no cooperators
      return D
  if round == last_round:
    return C  // Cooperate in the last round
```
**Prosocial Alignment:**

ACN promotes prosocial behavior by:

1. Cooperating in the first round to establish a cooperative tone.
2. Reinforcing cooperative behavior when it's prevalent.
3. Adapting to the level of cooperation in the previous round.
4. Penalizing exploitative behavior.
5. Cooperating in the last round to ensure a positive conclusion.

By using this strategy, ACN aims to promote cooperation and fairness in the N-Player Public Goods Game, even in the presence of diverse opponent behaviors.
'''

description_PROSOCIAL_31 = '''
**Prosocial Strategy: "Adaptive Cooperation with Gratitude"**

**Overview**

This strategy aims to balance individual payoff with prosocial behavior, fostering cooperation while being robust to diverse opponent behaviors. It adapts to the game's history, using a gratitude mechanism to encourage cooperation and punish defection.

**Decision Rules**

1. **First Round**: Cooperate (C) to set a positive tone and encourage others to cooperate.
2. **Subsequent Rounds**: Evaluate the previous round's outcome using the following criteria:
	* If the total number of cooperators (Σc_j) is greater than or equal to half of the players (n/2), Cooperate (C). This indicates a relatively cooperative environment.
	* If the total number of cooperators is less than half of the players, but the player's own payoff (π_i) was greater than or equal to the average payoff of all players, Cooperate (C). This suggests that cooperation is still beneficial despite some defection.
	* Otherwise, Defect (D).
3. **Gratitude Mechanism**: If a player i cooperated in the previous round and received a payoff greater than or equal to the average payoff of all players, they will Cooperate (C) in the current round, regardless of the number of cooperators. This expresses "gratitude" for the cooperative environment and encourages others to cooperate.
4. **Punishment**: If a player i defected in the previous round and received a payoff greater than the average payoff of all players, they will Defect (D) in the current round. This punishes defectors who exploited the cooperative environment.

**Edge Cases**

* **Last Round**: Cooperate (C) to maintain a positive reputation and encourage others to cooperate in future interactions.
* **Ties**: In case of a tie in the number of cooperators or payoffs, Cooperate (C) to err on the side of prosocial behavior.

**Pseudocode**
```python
def adaptive_cooperation_with_gratitude(n, k, history):
    if len(history) == 0:  # First round
        return 'C'
    
    previous_round = history[-1]
    total_cooperators = sum([1 if action == 'C' else 0 for action in previous_round])
    average_payoff = sum([payoff for payoff in previous_round]) / n
    
    if total_cooperators >= n / 2:
        return 'C'
    elif total_cooperators < n / 2 and previous_round[i] >= average_payoff:
        return 'C'
    else:
        return 'D'
    
    if previous_round[i] == 'C' and previous_round[i] >= average_payoff:
        return 'C'  # Gratitude mechanism
    elif previous_round[i] == 'D' and previous_round[i] > average_payoff:
        return 'D'  # Punishment
```
This strategy balances individual payoff with prosocial behavior, adapting to the game's history and promoting cooperation through a gratitude mechanism. By being robust to diverse opponent behaviors, it is well-suited for a tournament against independent strategies developed by other AI systems.
'''

description_PROSOCIAL_32 = '''
Here's a prosocial strategy, dubbed "Prosocial Adaptive Cooperation" (PAC), designed to be adaptive, robust, and aligned with the prosocial mindset.

**Decision Rules:**

1. **Initial Rounds (t ≤ 2):** Cooperate (C) to establish a cooperative atmosphere and encourage others to follow suit.
2. **Positive Feedback Loop (t > 2):**
	* If the average cooperation rate in the previous round (t-1) is above a threshold (T = 0.5), Cooperate (C).
	* Otherwise, Defect (D).
3. **Punish Defection (t > 2):**
	* If a player i defected in the previous round (t-1) and the total cooperation rate was below the threshold (T = 0.5), Defect (D) against player i in the current round.
	* This is a gentle punishment mechanism to discourage frequent defectors.
4. **React to Sudden Changes (t > 2):**
	* If the cooperation rate in the previous round (t-1) differs significantly from the average cooperation rate over the last 3 rounds (threshold Δ = 0.2), Cooperate (C).
	* This helps to stabilize the cooperation rate and counter potential manipulation attempts.

**Handling Edge Cases:**

1. **First Round (t = 1):** Cooperate (C) to set a positive tone.
2. **Last Round (t = r):** Cooperate (C) to maintain a prosocial reputation and encourage others to do the same.
3. **Ties:** In case of ties, Cooperate (C) to promote cooperation and avoid unnecessary conflict.

**Pseudocode:**
```
function PAC(n, k, r, history):
  T = 0.5  // Threshold for cooperation rate
  Δ = 0.2  // Threshold for sudden changes

  if t == 1 or t == r:
    return C

  prev_coop_rate = history[t-1].coop_rate
  avg_coop_rate = history[t-1].avg_coop_rate
  prev_actions = history[t-1].actions

  if prev_coop_rate > T:
    return C
  elif prev_coop_rate < T:
    if any(prev_actions[i] == D for i in range(n)):
      return D  // Punish defectors
    else:
      return C

  if abs(prev_coop_rate - avg_coop_rate) > Δ:
    return C  // React to sudden changes

  return C  // Default to cooperation
```
**Rationale:**

PAC aims to create a positive feedback loop by cooperating when others cooperate and punishing defectors gently. By reacting to sudden changes, PAC promotes stability and counteracts potential manipulation attempts. The strategy prioritizes cooperation, especially in the initial and final rounds, to maintain a prosocial reputation and encourage others to cooperate.
'''

description_COMMUNAL_1 = '''
I propose a communal strategy, dubbed " Adaptive Community Oriented" (ACO), that balances individual self-interest with communal welfare. ACO adapts to the game's history, promoting cooperation while protecting against exploitation.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Majority-Based Cooperation**: In subsequent rounds, cooperate if the majority of players (≥ n/2) cooperated in the previous round. Otherwise, defect (D).
3. **Exploitation Detection**: Monitor the game's history to detect exploitation. If a player detects that they have been exploited (i.e., they cooperated while others defected) in two or more consecutive rounds, they will defect in the next round to signal their discontent.
4. **Reciprocal Cooperation**: If a player observes that another player has cooperated with them in the previous round, they will cooperate with that player in the next round, provided the majority-based cooperation rule is also satisfied.
5. **Round-Robin Defection**: In the last round (r), defect (D) to maximize individual payoff, as there is no future round to consider.

**Pseudocode:**
```
def ACO(n, r, k, history):
  if current_round == 1:
    return C  # Initial Cooperation

  prev_round_cooperators = count_cooperators(history[-1])
  if prev_round_cooperators >= n/2:
    return C  # Majority-Based Cooperation

  if has_been_exploited(history):
    return D  # Exploitation Detection

  for player in history[-1]:
    if player.cooperated and player!= self:
      return C  # Reciprocal Cooperation

  if current_round == r:
    return D  # Round-Robin Defection

  return D  # Default to Defection
```
**Edge Cases:**

* First round: Cooperate to set a cooperative tone.
* Last round: Defect to maximize individual payoff.
* When there is a tie in the majority-based cooperation rule (i.e., exactly half of the players cooperated), defect to avoid potential exploitation.

**Communal Mindset:**

ACO prioritizes community welfare by:

* Encouraging initial cooperation to set a positive tone.
* Adapting to the majority's behavior to promote cooperation.
* Detecting and responding to exploitation to maintain fairness.
* Reciprocating cooperation with other players to foster mutual trust.

By following these decision rules, ACO balances individual self-interest with communal welfare, making it a robust and adaptive strategy for the N-Player Public Goods Game.
'''

description_COMMUNAL_2 = '''
Here is a communal strategy for the N-Player Public Goods Game that adapts to the game parameters and history:

**Strategy Name:** Adaptive Communal Cooperation (ACC)

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate a cooperative tone and encourage others to follow.
2. **Subsequent Rounds:** Observe the total number of cooperators (TC) in the previous round and calculate the cooperation rate (CR) as TC/n.
	* If CR ≥ 0.5, Cooperate (C) to reinforce the current cooperation level.
	* If CR < 0.5 and k > n/2, Cooperate (C) to try to increase the cooperation rate, as the multiplication factor is favorable.
	* If CR < 0.5 and k ≤ n/2, Defect (D) to avoid being exploited by others, as the multiplication factor is unfavorable.
3. **Punishment Mechanism:** If the total payoff in the previous round is lower than the average payoff in the previous rounds (i.e., the group is not doing well), Defect (D) in the current round to signal dissatisfaction and encourage others to adjust their strategy.
4. **Forgiveness Mechanism:** If the total payoff in the previous round is higher than the average payoff in the previous rounds (i.e., the group is doing well), Cooperate (C) in the current round to reinforce the positive trend.

**Handling Edge Cases:**

* **Last Round:** Cooperate (C) to maximize the total payoff, as there is no future round to consider.
* **Low Cooperation Rate:** If the cooperation rate is consistently low (e.g., CR < 0.3), Defect (D) to avoid being exploited and encourage others to adjust their strategy.

**Communal Mindset:**

The ACC strategy prioritizes cooperation and aims to create a mutually beneficial environment. By cooperating in the first round and adapting to the cooperation rate, ACC encourages others to cooperate and reinforces positive behavior. The punishment and forgiveness mechanisms help to maintain a balance between cooperation and self-interest.

**Pseudocode:**
```python
def ACC(n, k, r, history):
  if r == 1:  # First round
    return 'C'
  
  TC = sum([1 for action in history[-1] if action == 'C'])
  CR = TC / n
  
  if CR >= 0.5:
    return 'C'
  elif CR < 0.5 and k > n/2:
    return 'C'
  else:
    return 'D'
  
  # Punishment mechanism
  if sum(history[-1]) < sum(history[:-1]) / (r - 1):
    return 'D'
  
  # Forgiveness mechanism
  if sum(history[-1]) > sum(history[:-1]) / (r - 1):
    return 'C'
  
  # Last round
  if r == len(history):
    return 'C'
```
This strategy is designed to be adaptive, robust, and communal, making it a strong competitor in the tournament against independent strategies developed by other AI systems.
'''

description_COMMUNAL_3 = '''
**Communal Strategy: Adaptive Reciprocity**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate a cooperative tone and encourage others to reciprocate.
2. **Subsequent Rounds:** Evaluate the previous round's outcome:
	* If the total payoff for all players increased (i.e., more players cooperated), Cooperate (C) in the next round.
	* If the total payoff for all players decreased (i.e., fewer players cooperated), Defect (D) in the next round.
3. **Reciprocity Rule:** Cooperate (C) if the number of cooperators in the previous round is greater than or equal to the number of defectors. Otherwise, Defect (D).
4. **Punishment Rule:** If a player's payoff in the previous round was less than the average payoff of all players, Defect (D) in the next round to discourage free-riding.

**Edge Cases:**

1. **Last Round:** Cooperate (C) to maintain a positive communal outcome, as the game's final outcome is not affected by future reciprocity.
2. **Tiebreaker:** In case of a tie in the number of cooperators and defectors, Cooperate (C) to prioritize communal benefit.
3. **Initial Defection:** If a player defects in the first round, Defect (D) in the subsequent round to discourage free-riding.

**Communal Mindset:**

This strategy prioritizes cooperation and reciprocity to maintain a positive communal outcome. By cooperating initially and adapting to the group's behavior, the strategy aims to encourage others to cooperate and create a mutually beneficial environment.

**Pseudocode:**
```markdown
# Initialize variables
cooperate = True
total_cooperators = 0
total_defectors = 0
previous_payoffs = []

# First Round
play C

# Subsequent Rounds
while rounds_remaining > 0:
  # Evaluate previous round
  total_cooperators = count players who played C
  total_defectors = count players who played D
  average_payoff = calculate average payoff of all players

  # Decision Rules
  if total_cooperators >= total_defectors:
    cooperate = True
  elif average_payoff < previous_average_payoff:
    cooperate = False
  else:
    cooperate = not cooperate

  # Play action
  if cooperate:
    play C
  else:
    play D

  # Update variables
  previous_payoffs.append(current_payoff)
  previous_average_payoff = average_payoff
```
This strategy is adaptive, robust, and aligned with the communal mindset, making it suitable for a tournament against independent strategies developed by other AI systems.
'''

description_COMMUNAL_4 = '''
**Communal Strategy: "Adaptive Cooperator"**

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **Reciprocity**: For rounds 2 to r-1, cooperate if the majority (≥ n/2) of players cooperated in the previous round. Otherwise, defect (D).
3. **Punishment**: If the total contributions (Σ(j=1 to n) c_j) in the previous round are below the average contribution (n/2), defect in the current round.
4. **Exploitation Prevention**: If a player's payoff in the previous round is significantly higher (≥ 1.5 times) than the average payoff, defect in the current round to prevent exploitation.
5. **Final Round Cooperation**: Cooperate in the last round (r) to maximize total game payoff, as there is no future round to influence.

**Edge Case Handling:**

* **First Round**: Cooperate (C) to establish a cooperative tone.
* **Last Round**: Cooperate (C) to maximize total game payoff.
* **Tie in Majority**: If the number of cooperators is exactly half of the total players (n/2), cooperate to maintain a cooperative environment.

**Pseudocode:**

```
function adaptiveCooperator(n, r, k, history):
    if currentRound == 1:
        return COOPERATE

    previousRoundContributions = history[-1]['contributions']
    previousRoundPayoffs = history[-1]['payoffs']

    if majorityCooperated(previousRoundContributions):
        return COOPERATE
    else:
        return DEFECT

    if averageContribution(previousRoundContributions) < n/2:
        return DEFECT

    if exploitedPlayer(previousRoundPayoffs):
        return DEFECT

    if currentRound == r:
        return COOPERATE

def majorityCooperated(contributions):
    return sum(contributions) >= n/2

def averageContribution(contributions):
    return sum(contributions) / n

def exploitedPlayer(payoffs):
    return max(payoffs) >= 1.5 * average(payoffs)
```

**Communal Mindset Alignment:**

The Adaptive Cooperator strategy prioritizes cooperation while adapting to the dynamics of the game. By initially cooperating and reciprocating cooperation, the strategy encourages others to follow suit. The punishment mechanism prevents free-riding, and the exploitation prevention mechanism ensures that no player takes advantage of others' cooperation. The final round cooperation maximizes total game payoff, aligning with the communal mindset of achieving a mutually beneficial outcome.
'''

description_COMMUNAL_5 = '''
**Communal Strategy: "K-Responsive Reciprocity" (KRR)**

KRR is a dynamic, adaptive strategy that balances individual self-interest with communal welfare. It's designed to be robust against various opponent behaviors and promotes cooperation while minimizing exploitation.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds (t>1):** Use the following logic:
	* Calculate the average cooperation rate of all players in the previous round (t-1): `avg_coop_prev = Σ(c_j,t-1) / n`
	* If `avg_coop_prev` is greater than or equal to `k/n`, Cooperate (C). This encourages continued cooperation when the group is already contributing sufficiently.
	* If `avg_coop_prev` is less than `k/n`, Defect (D) with a probability `p_defect = 1 - (avg_coop_prev / (k/n))`. This introduces a responsive element, making the strategy more likely to defect when the group's cooperation rate is low.
3. **Last Round (t=r):** Cooperate (C) to maximize the total payoff, as there's no future round to consider.

**Edge Cases:**

* **First round with only one player:** Cooperate (C), as there's no previous round to analyze.
* **Ties in average cooperation rate:** In cases where `avg_coop_prev` equals `k/n` exactly, Cooperate (C) to maintain a cooperative stance.

**Communal Mindset:**

KRR prioritizes the community's overall payoff by:

* Encouraging cooperation when the group is already contributing sufficiently ( Rule 2a)
* Adapting to the group's cooperation rate, making it more likely to defect when the group's contributions are low (Rule 2b)
* Cooperating in the last round to maximize the total payoff (Rule 3)

**Pseudocode:**
```python
def KRR(n, k, r, history):
    if t == 1:  # Initial round
        return C
    elif t > 1:
        avg_coop_prev = sum(history[t-1]) / n
        if avg_coop_prev >= k/n:
            return C
        else:
            p_defect = 1 - (avg_coop_prev / (k/n))
            return D with probability p_defect
    elif t == r:  # Last round
        return C
```
This strategy is designed to be robust, adaptive, and communal, making it a competitive contender in the tournament.
'''

description_COMMUNAL_6 = '''
Here's a communal strategy for the N-Player Public Goods Game that adapts to the game's history and parameters.

**Strategy Name:** Adaptive Communal Optimizer (ACO)

**Decision Rules:**

1. **Initial Round:** In the first round, cooperate (C) with a probability of 50%. This initial cooperation sends a signal that we're willing to contribute to the public good.
2. **Cooperation Threshold:** Calculate the average payoff per player in the previous round (avg_π_prev). If avg_π_prev ≥ (k/n), it means the group is generating sufficient public goods. Cooperate (C) if the number of cooperators in the previous round (n_C_prev) is greater than or equal to (n/2). Otherwise, defect (D).
3. **Exploitation Detection:** Monitor the number of defectors in the previous round (n_D_prev). If n_D_prev ≥ (n/3), it indicates potential exploitation. Defect (D) in the current round to avoid being taken advantage of.
4. **Revenge Mechanism:** If we defected in the previous round and the average payoff per player in that round (avg_π_prev) was lower than (k/n), cooperate (C) in the current round to signal a willingness to return to cooperation.
5. **Learning and Adaptation:** After each round, update the cooperation threshold and exploitation detection parameters based on the game's history.

Pseudocode:
```
IF first round THEN
  cooperate with probability 0.5
ELSE
  avg_π_prev = average payoff per player in previous round
  n_C_prev = number of cooperators in previous round
  n_D_prev = number of defectors in previous round

  IF avg_π_prev >= (k/n) AND n_C_prev >= (n/2) THEN
    cooperate
  ELSE IF n_D_prev >= (n/3) THEN
    defect
  ELSE IF defected in previous round AND avg_π_prev < (k/n) THEN
    cooperate (revenge mechanism)
  ELSE
    defect
  END IF

  UPDATE cooperation threshold and exploitation detection parameters
END IF
```
**Edge Cases:**

* **Last Round:** In the final round, cooperate (C) if the average payoff per player in the previous round was greater than or equal to (k/n). This encourages cooperation even in the last round, as it may still benefit the group.
* **Tiebreaker:** In case of a tie in the number of cooperators or defectors, cooperate (C) to favor the public good.

**Communal Alignment:**

The ACO strategy prioritizes cooperation when the group is generating sufficient public goods and adapts to prevent exploitation. By cooperating in the initial round and using a revenge mechanism, ACO promotes a communal mindset and encourages others to cooperate. The strategy's adaptive nature allows it to respond to various opponent behaviors, making it robust in a wide range of scenarios.
'''

description_COMMUNAL_7 = '''
Here's a communal strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of 1/n, where n is the number of players. This encourages initial cooperation while avoiding excessive optimism.
2. **Reciprocal Cooperation**: If the total number of cooperators in the previous round is greater than or equal to n/2, cooperate (C) in the current round. This promotes reciprocity and collective success.
3. **Contribution-Based Cooperation**: If the total contribution (Σ(j=1 to n) c_j) in the previous round is greater than or equal to k/2, cooperate (C) in the current round. This focuses on the overall contribution rather than individual actions.
4. **Punish Defection**: If the total number of cooperators in the previous round is less than n/2 and the total contribution is less than k/2, defect (D) in the current round. This punishes collective defection and encourages cooperation.
5. **Exploratory Cooperation**: With a probability of 1/r (where r is the number of rounds), cooperate (C) in the current round, regardless of the previous round's outcome. This introduces exploration and adaptability.

**Edge Cases:**

1. **Last Round**: In the last round, cooperate (C) if the total number of cooperators in the previous round is greater than or equal to n/2. Otherwise, defect (D).
2. **Ties**: In cases where the decision rules yield a tie (e.g., equal number of cooperators and defectors), cooperate (C) with a probability of 1/2.

**Pseudocode:**
```
def ACO(n, k, r, history):
  if first_round:
    return C with probability 1/n
  elif sum_cooperators >= n/2:
    return C
  elif total_contribution >= k/2:
    return C
  elif sum_cooperators < n/2 and total_contribution < k/2:
    return D
  elif random_probability(1/r):
    return C
  else:
    return D

def last_round(n, k, r, history):
  if sum_cooperators >= n/2:
    return C
  else:
    return D
```
**Communal Mindset:**

ACO prioritizes collective success by:

1. Encouraging initial cooperation and reciprocal cooperation.
2. Focusing on overall contribution rather than individual actions.
3. Punishing collective defection to promote cooperation.
4. Introducing exploration and adaptability to respond to changing environments.

ACO is designed to be robust and adaptive, allowing it to perform well in a wide range of scenarios and opponent behaviors.
'''

description_COMMUNAL_8 = '''
Here is a communal strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Community Focus (ACF)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to set a positive tone and encourage others to cooperate.
2. **Recent History**: Track the total number of cooperators (TC) in the last round and the current round's index (t). If TC in the last round is greater than or equal to (n/2), cooperate in the current round. Otherwise, defect.
3. **Long-term Trend**: Keep a moving average of the total number of cooperators over the last (r/2) rounds. If this average is greater than or equal to (n/2), cooperate. Otherwise, defect.
4. **Punishment Mechanism**: If a player has defected in the last round and the total number of cooperators in the last round is less than (n/2), defect in the current round to punish the non-cooperative behavior.
5. **Endgame Cooperation**: In the last round (t = r), cooperate to maximize the total payoff, as there is no future round to consider.

**Edge Cases:**

1. **First Round**: Cooperate to set a positive tone.
2. **Last Round**: Cooperate to maximize the total payoff.
3. **Initial Defection**: If a player defects in the first round, switch to defecting in the second round to avoid being taken advantage of.

**Communal Alignment:**

ACF prioritizes cooperation when the community is cooperating and punishes non-cooperative behavior when the community is not cooperating. This strategy encourages cooperation while being robust to various opponent behaviors. By cooperating in the first round and the last round, ACF promotes a communal mindset and tries to maximize the total payoff.

**Pseudocode:**
```
Initialize:
  TC_last = 0  // Total cooperators in the last round
  TC_avg = 0  // Moving average of total cooperators
  t = 0  // Current round index

Decision Rules:
  if t == 0:  // First round
    cooperate
  elif TC_last >= (n/2):  // Recent history
    cooperate
  elif TC_avg >= (n/2):  // Long-term trend
    cooperate
  elif last_action == Defect and TC_last < (n/2):  // Punishment mechanism
    defect
  elif t == r:  // Last round
    cooperate
  else:
    defect

Update:
  TC_last = count(cooperators in current round)
  TC_avg = update_moving_average(TC_last, r/2)
  t += 1
```
ACF is a robust and adaptive strategy that balances cooperation and punishment to achieve a high total payoff. By aligning with the communal mindset, ACF promotes cooperation and encourages other players to do the same.
'''

description_COMMUNAL_9 = '''
I propose a communal strategy called " Adaptive Cooperative Threshold" (ACT). ACT is designed to balance individual self-interest with the collective benefit of cooperation, while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a cooperative tone and encourage others to do the same.
2. **Adaptive Threshold**: Calculate a cooperation threshold, τ, based on the history of total contributions. Initialize τ to 0.5 (a neutral value).
3. **Contribution-Based Cooperation**: In each subsequent round, calculate the average total contributions (ATC) from the previous rounds. If ATC ≥ τ, cooperate (play C); otherwise, defect (play D).
4. **Threshold Update**: Update τ based on the current round's total contributions. If the current total contributions are higher than the previous round's, increase τ by 0.1; otherwise, decrease τ by 0.1. Ensure τ remains within the bounds [0, 1].
5. **Last Round Exception**: In the final round, cooperate (play C) to maximize the collective payoff, regardless of the current τ value.

**Pseudocode:**
```
// Initialize variables
τ = 0.5
ATC = 0
round = 1

// Loop through rounds
while round ≤ r:
  // First round: cooperate
  if round == 1:
    action = C
  else:
    // Calculate average total contributions (ATC)
    ATC = (Σ(j=1 to n) c_j) / n
    // Check cooperation threshold
    if ATC ≥ τ:
      action = C
    else:
      action = D

  // Update threshold
  if current_total_contributions > previous_total_contributions:
    τ = min(1, τ + 0.1)
  else:
    τ = max(0, τ - 0.1)

  // Last round exception
  if round == r:
    action = C

  // Take action and update history
  take_action(action)
  update_history()

  // Increment round counter
  round += 1
```
**Communal Alignment:**

ACT prioritizes cooperation when the collective benefit is high, while adapting to the level of cooperation exhibited by others. By updating the cooperation threshold based on the history of total contributions, ACT encourages others to cooperate and punishes free-riding behavior.

**Robustness:**

ACT is designed to be robust against various opponent behaviors, including:

* **Defectors**: ACT will adapt to defecting opponents by decreasing the cooperation threshold, making it less likely to cooperate in the future.
* **Cooperators**: ACT will reinforce cooperation when opponents cooperate, increasing the cooperation threshold and encouraging further cooperation.
* **Mixed strategies**: ACT will adjust its cooperation threshold based on the overall level of cooperation, making it less sensitive to specific opponent strategies.

By being adaptive and communal, ACT aims to achieve a high collective payoff while being robust to various opponent behaviors in the N-Player Public Goods Game.
'''

description_COMMUNAL_10 = '''
**Communal Strategy: "Gradual Reciprocity with Adaptive Forgiveness"**

**Overview**

Our communal strategy, "Gradual Reciprocity with Adaptive Forgiveness" (GRF), aims to balance cooperation and self-interest while being robust to diverse opponent behaviors. GRF adapts to the game's history, rewarding cooperation and punishing defection, while also allowing for forgiveness and re-engagement.

**Decision Rules**

1. **Initial Rounds (t ≤ 3):** Cooperate (C) to encourage cooperation and establish a positive tone.
2. **Reciprocity Phase (t > 3):**
	* If the number of cooperators in the previous round (t-1) is greater than or equal to the number of defectors, cooperate (C).
	* Otherwise, defect (D).
3. **Punishment Phase (t > 3):**
	* If a player defected in the previous round (t-1) and the overall number of cooperators is less than the number of defectors, defect (D) in response to punish the defector.
	* However, if the punishing player has defected in the previous round (t-1), cooperate (C) to avoid escalating retaliation.
4. **Forgiveness Mechanism:**
	* If a player has defected for two consecutive rounds and then cooperates, forgive and cooperate (C) in the next round.
	* If a player has cooperated for two consecutive rounds and then defects, do not punish immediately. Instead, cooperate (C) in the next round and re-evaluate.
5. **Final Rounds (t ≥ r-2):** Cooperate (C) to maximize overall payoff, as the game is nearing its end.

**Edge Cases**

1. **First Round (t=1):** Cooperate (C) to establish a positive tone.
2. **Last Round (t=r):** Cooperate (C) to maximize overall payoff.
3. **Ties:** In cases where the number of cooperators equals the number of defectors, cooperate (C) to maintain a positive attitude.

**Communal Alignment**

GRF prioritizes cooperation and reciprocity, promoting a communal mindset by:

1. Encouraging cooperation in initial rounds to establish a positive tone.
2. Rewarding cooperation and punishing defection to maintain a balance.
3. Allowing for forgiveness and re-engagement to prevent escalating retaliation.
4. Maximizing overall payoff in final rounds to benefit the community.

**Pseudocode**

```
function GRF(n, k, r, t, history):
  if t <= 3:
    return C  // Cooperate in initial rounds
  elif sum(history[t-1]) >= n/2:
    return C  // Reciprocate cooperation
  elif sum(history[t-1]) < n/2:
    if history[t-1][i] == D:  // Punish defection
      return D
    else:
      return C
  elif history[t-1][i] == D and history[t-2][i] == D:
    if history[t-1][j] == C:  // Forgive and cooperate
      return C
  elif t >= r-2:
    return C  // Cooperate in final rounds
  else:
    return C  // Default to cooperation
```

By implementing GRF, we aim to create a robust and adaptive communal strategy that promotes cooperation and mutual benefit in the N-Player Public Goods Game.
'''

description_COMMUNAL_11 = '''
Here's a communal strategy that adapts to the game's history and parameters:

**Strategy Name:** " Adaptive Cooperative Momentum" (ACM)

**Decision Rules:**

1. **First Round:** Cooperate (C). This sets a positive tone for the game and encourages others to cooperate.
2. **Subsequent Rounds:**
	* If the total number of cooperators in the previous round is greater than or equal to the number of players divided by 2 (n/2), Cooperate (C). This reinforces the cooperative momentum.
	* If the total number of cooperators in the previous round is less than n/2, Defect (D) with a probability p = (k/n) × (total cooperators in previous round). This introduces a cautious element, making the strategy more robust to exploitation.
	* If the game is in the last round (r = current round), Defect (D). This ensures the strategy doesn't unnecessarily contribute to the public good when the game is about to end.
3. **Memory-Based Adaptation:**
	* Keep track of the total number of cooperators in each round (TC).
	* If TC increases in the current round compared to the previous round, increase the probability of cooperating in the next round by a small factor (e.g., 5%).
	* If TC decreases in the current round compared to the previous round, decrease the probability of cooperating in the next round by a small factor (e.g., 5%).

**Pseudocode:**
```
 Initialize:
   TC = 0  // Total cooperators
   p = 0   // Probability of cooperating

 First Round:
   Cooperate (C)

 Subsequent Rounds:
   If TC >= n/2:
     Cooperate (C)
   Else:
     p = (k/n) * TC
     If random() < p:
       Cooperate (C)
     Else:
       Defect (D)

   If current round == last round (r):
     Defect (D)

   Update TC and p for next round:
     If TC increased:
       p = p + 0.05
     Else if TC decreased:
       p = p - 0.05
```
**Rationale:**

1. The strategy starts by cooperating, setting a positive tone for the game.
2. By cooperating when the number of cooperators is high, the strategy reinforces the cooperative momentum and encourages others to do the same.
3. When the number of cooperators is low, the strategy introduces a cautious element by defecting with a probability proportional to the number of cooperators. This makes the strategy more robust to exploitation.
4. The memory-based adaptation mechanism allows the strategy to adjust its behavior based on the game's history, increasing the probability of cooperating when the number of cooperators increases and decreasing it when the number of cooperators decreases.
5. By defecting in the last round, the strategy avoids unnecessarily contributing to the public good when the game is about to end.

This strategy should perform well in a tournament setting, as it balances cooperation and caution, adapts to the game's history, and aligns with the communal mindset.
'''

description_COMMUNAL_12 = '''
I propose a communal strategy, which I'll call "Adaptive Cooperator" (AC). AC is designed to balance individual self-interest with communal well-being, adapting to the game's history and parameters.

**Decision Rules:**

1. **Initial Rounds (t = 1 to 3):** Cooperate (C) unconditionally to establish a cooperative tone and encourage others to follow suit.
2. **Middle Rounds (t = 4 to r-2):**
	* If the average cooperation rate in the previous round (t-1) is above a threshold (θ), cooperate (C). This encourages continued cooperation when others are contributing.
	* Otherwise, defect (D) with probability p, and cooperate (C) with probability (1-p). The probability p is calculated as p = (n-k)/n, which increases as the multiplication factor k decreases, reflecting the need for more cooperation when the communal benefit is lower.
3. **Late Rounds (t = r-1 to r):**
	* If the average cooperation rate in the previous round (t-1) is above θ, cooperate (C) to maintain a cooperative atmosphere.
	* If the game is in the last round (t = r), defect (D) to maximize individual payoff, as cooperation no longer affects future rounds.

**Handling Edge Cases:**

* **First Round (t = 1):** Cooperate (C) unconditionally to set a cooperative tone.
* **Last Round (t = r):** Defect (D) to maximize individual payoff.
* **Small Number of Players (n ≤ 3):** Cooperate (C) unconditionally, as the communal benefit is more significant with fewer players.

**Communal Mindset:**

AC prioritizes cooperation when others are contributing, aiming to create a positive feedback loop. By cooperating initially and in response to others' cooperation, AC fosters a sense of community and shared responsibility. The adaptive nature of AC allows it to respond to changing circumstances, balancing individual self-interest with communal well-being.

**Pseudocode:**
```
function AdaptiveCooperator(n, k, r, θ):
  for t = 1 to r:
    if t ≤ 3:
      action = C
    elseif t < r - 1:
      avg_coop_rate = calculate_average_cooperation_rate(t-1)
      if avg_coop_rate ≥ θ:
        action = C
      else:
        p = (n-k)/n
        action = random_choice(p, C, D)
    else:
      if t = r:
        action = D
      else:
        avg_coop_rate = calculate_average_cooperation_rate(t-1)
        if avg_coop_rate ≥ θ:
          action = C
        else:
          action = D
    return action
```
AC is designed to be a robust and adaptive communal strategy, capable of responding to various opponent behaviors while prioritizing cooperation and community well-being.
'''

description_COMMUNAL_13 = '''
**Communal Strategy: Adaptive Cooperative Regime (ACR)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a baseline of cooperation and encourage others to follow suit.
2. **Reciprocity**: Cooperate if the majority (>= n/2) of players cooperated in the previous round. This promotes a reciprocal environment where cooperation is rewarded.
3. **Punish Defection**: Defect (D) if the majority (>= n/2) of players defected in the previous round. This discourages exploitation and maintains a balance of power.
4. **Exploit Greed**: Defect if the total contributions in the previous round were below the average expected contribution (k/n \* n/2). This prevents players from exploiting the community's generosity.
5. **Cooperative Momentum**: Cooperate if the community's total payoff in the previous round was higher than the average expected payoff (k/n \* n). This sustains cooperation when it is beneficial for the community.
6. **Random Exploration**: With a small probability (ε, e.g., 0.1), randomly choose to cooperate or defect. This introduces a degree of unpredictability, making it harder for opponents to exploit the strategy.

**Edge Cases:**

* **Last Round**: In the final round, cooperate if the community's total payoff is higher than the average expected payoff; otherwise, defect.
* **Ties**: In case of a tie in the majority, cooperate.

**Pseudocode:**
```python
def ACR(n, k, r, history):
  # Initialize cooperation flag
  cooperate = True

  # First round: cooperate
  if len(history) == 0:
    return cooperate

  # Get previous round's actions and payoffs
  prev_round = history[-1]
  prev_actions = prev_round['actions']
  prev_payoffs = prev_round['payoffs']

  # Count cooperators and defectors
  cooperators = sum(1 for action in prev_actions if action == 'C')
  defectors = n - cooperators

  # Reciprocity
  if cooperators >= n/2:
    cooperate = True
  # Punish Defection
  elif defectors >= n/2:
    cooperate = False
  # Exploit Greed
  elif sum(prev_payoffs) < k/n * n/2:
    cooperate = False
  # Cooperative Momentum
  elif sum(prev_payoffs) > k/n * n:
    cooperate = True

  # Random Exploration
  if random.random() < ε:
    cooperate = not cooperate

  return cooperate
```
This strategy balances cooperation and self-interest, adapting to the community's behavior and the game's parameters. By incorporating reciprocity, punishment, and exploration, ACR aims to create a robust and communal environment that encourages cooperation while preventing exploitation.
'''

description_COMMUNAL_14 = '''
Here is a communal strategy that meets the requirements:

**Strategy Name:** Adaptive Community Builder (ACB)

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to do the same.
2. **Subsequent Rounds:** For each subsequent round, calculate the average cooperation rate of all players in the previous round, denoted as `avg_coop_prev`. If `avg_coop_prev` is above a certain threshold `theta` (e.g., 0.5), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** If the average cooperation rate in the previous round is below `theta`, and the player's individual payoff in the previous round was lower than the average payoff of all players, defect (D) in the current round. This mechanism aims to punish non-cooperative behavior.
4. **Forgiveness Mechanism:** If the average cooperation rate in the previous round was below `theta`, but the player's individual payoff in the previous round was higher than or equal to the average payoff of all players, cooperate (C) in the current round. This mechanism allows for forgiveness and encourages cooperation when others are willing to cooperate.

**Edge Cases:**

1. **Last Round:** Cooperate (C) in the last round, regardless of the previous rounds' outcomes. This ensures that the player contributes to the community project, even if it's the final round.
2. **Tiebreaker:** In case of a tie in the average cooperation rate (e.g., `avg_coop_prev` equals `theta`), cooperate (C) to favor cooperation.

**Pseudocode:**
```python
def ACB(n, k, r, history):
    theta = 0.5  # threshold for cooperation rate

    for t in range(1, r+1):
        if t == 1:  # initial round
            action = 'C'
        else:
            avg_coop_prev = calculate_average_cooperation_rate(history[t-1])
            if avg_coop_prev >= theta:
                action = 'C'
            else:
                individual_payoff = calculate_individual_payoff(history[t-1])
                avg_payoff = calculate_average_payoff(history[t-1])
                if individual_payoff < avg_payoff:
                    action = 'D'  # punish non-cooperative behavior
                else:
                    action = 'C'  # forgive and cooperate

        # last round
        if t == r:
            action = 'C'

        return action
```
**Communal Alignment:** The ACB strategy prioritizes cooperation and aims to establish a cooperative atmosphere from the beginning. By cooperating in the first round, it sets a positive tone for the game. The punishment and forgiveness mechanisms ensure that non-cooperative behavior is addressed while allowing for cooperation when others are willing to cooperate. This strategy aligns with the communal mindset by promoting cooperation and mutual benefit.

This strategy is adaptive, as it adjusts its behavior based on the game's history and the actions of other players. It is also robust, as it can handle a wide range of opponent behaviors and edge cases.
'''

description_COMMUNAL_15 = '''
I propose a communal strategy called "Reflective Conditional Cooperation" (RCC) that adapts to the game history and opponent behaviors while maintaining a strong communal mindset.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) with a probability of 0.5. This initializes the game with a moderate level of cooperation and allows the strategy to observe opponent behaviors.
2. **Subsequent Rounds (t>1):** Cooperate (C) if the average cooperation rate of all players in the previous round (t-1) is above a threshold θ (e.g., θ = 0.5). Otherwise, Defect (D).
3. **Reflective Component:** If the average payoff of all players in the previous round (t-1) is higher than the average payoff of the current player, then Cooperate (C) with a higher probability (e.g., 0.7). This encourages the strategy to contribute to the public good when it is beneficial to the community.
4. **Conditional Component:** If a player i has cooperated in the previous round (t-1) and received a higher payoff than the average payoff of all players, then Cooperate (C) with a higher probability (e.g., 0.7) in the current round. This reinforces cooperation when it is individually beneficial.

**Edge Cases:**

1. **Last Round (t=r):** Cooperate (C) if the average cooperation rate of all players in the previous round (t-1) is above θ. Otherwise, Defect (D). This ensures that the strategy maintains its communal mindset even in the final round.
2. **Low Cooperation Rate:** If the average cooperation rate of all players in the previous round (t-1) is below a low threshold (e.g., 0.2), then Defect (D). This prevents the strategy from cooperating in a game where the communal mindset is not being maintained.
3. **High Defection Rate:** If the average defection rate of all players in the previous round (t-1) is above a high threshold (e.g., 0.8), then Defect (D). This allows the strategy to adapt to games where the communal mindset is not being maintained.

**Pseudocode:**
```python
def RCC(n, k, r, t, history):
  # Initialize variables
  theta = 0.5  # threshold for average cooperation rate
  reflect_prob = 0.7  # probability of cooperation when average payoff is high
  conditional_prob = 0.7  # probability of cooperation when individual payoff is high

  # Initial Round (t=1)
  if t == 1:
    return random.choice([C, D], p=[0.5, 0.5])

  # Calculate average cooperation rate and average payoff
  avg_coop_rate = sum(history[t-1]['coop']) / n
  avg_payoff = sum(history[t-1]['payoff']) / n

  # Reflective Component
  if avg_payoff > history[t-1]['payoff'][i]:
    return C with probability reflect_prob

  # Conditional Component
  if history[t-1]['coop'][i] and history[t-1]['payoff'][i] > avg_payoff:
    return C with probability conditional_prob

  # Main Decision Rule
  if avg_coop_rate > theta:
    return C
  else:
    return D

  # Edge Cases
  if t == r:  # Last Round
    return RCC_last_round(n, k, r, t, history)
  elif avg_coop_rate < 0.2:  # Low Cooperation Rate
    return D
  elif avg_defection_rate > 0.8:  # High Defection Rate
    return D
```
This strategy is designed to be communal, adaptive, and robust to a wide range of opponent behaviors. By reflecting on the game history and adapting to the communal mindset, RCC aims to promote cooperation and achieve high payoffs for all players.
'''

description_COMMUNAL_16 = '''
I propose a communal strategy, "Adaptive Communal Reciprocity" (ACR), which balances cooperation and defection based on the game's history. ACR aims to maximize collective payoffs while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds (t>1):** Evaluate the previous round's outcome:
	* If the total number of cooperators (Σc_j) is greater than or equal to half the number of players (n/2), Cooperate (C) in the current round.
	* Otherwise, Defect (D) to minimize losses and potentially stimulate cooperation in future rounds.
3. **Reciprocity Mechanism:** Introduce a "Reciprocity Threshold" (RT) that tracks the number of rounds where at least half the players cooperated. When RT ≥ (r/2), Cooperate (C) in the current round, even if the previous round's outcome was unfavorable. This mechanism encourages cooperation when a sufficient number of players have demonstrated a willingness to cooperate.
4. **Punishment Mechanism:** If a player observes a significant decrease in collective cooperation (i.e., fewer than half the players cooperated in the previous round), Defect (D) in the current round to deter potential free-riders.

**Edge Cases:**

* **Last Round (t=r):** Cooperate (C) to maximize collective payoff, as there is no future round to consider.
* **Consecutive Defections:** If a player observes a sequence of rounds with zero or minimal cooperation (i.e., fewer than two players cooperated), Defect (D) in the current round to avoid being exploited.

**Communal Mindset:**

ACR prioritizes cooperation and reciprocal behavior, aligning with the communal mindset. By cooperating in the initial round and responding positively to cooperation from others, ACR encourages a culture of cooperation. The Reciprocity Mechanism reinforces this behavior, while the Punishment Mechanism deters exploitation.

Pseudocode:
```python
def AdaptiveCommunalReciprocity(n, k, r, history):
    if t == 1:  # Initial Round
        return C
    elif sum(history[-1]) >= n/2:  # Previous round had enough cooperation
        return C
    elif RT >= r/2:  # Reciprocity Threshold reached
        return C
    elif sum(history[-1]) < n/2:  # Punishment Mechanism
        return D
    else:  # Default to Defect
        return D

# Update Reciprocity Threshold (RT) after each round
def update_RT(history):
    if sum(history[-1]) >= n/2:
        RT += 1
    else:
        RT = 0
```
This strategy will be implemented as an algorithm to compete in the tournament.
'''

description_COMMUNAL_17 = '''
**Communal Strategy: " Adaptive Reciprocity with Community Focus" (ARC)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage others to contribute to the public good and establish a cooperative tone.
2. **Reciprocity**: Observe the number of cooperators (CC) in the previous round. If CC ≥ (n/2), cooperate in the current round. This rewards cooperation and encourages others to do the same.
3. **Community Focus**: If CC < (n/2), calculate the "community contribution rate" (CCR) as the average number of cooperators over the last 3 rounds. If CCR ≥ (k/n), cooperate in the current round. This focuses on the community's overall cooperation level and adapts to changes in cooperation rates.
4. **Defection Response**: If the previous round had a low number of cooperators (CC < (n/4)), defect (D) in the current round to avoid exploitation and signal the need for more cooperation.
5. **Round-Robin Adjustment**: Every 3 rounds, adjust the cooperation threshold (n/2) in the Reciprocity rule by ±1 based on the overall cooperation rate. This allows the strategy to adapt to changing opponent behaviors.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round to maximize the total payoff, as there's no future round to consider.
2. **Early Defection**: If, in the first 3 rounds, more than (n/2) players defect, switch to a more cautious approach: defect (D) in the next round and reevaluate using the Community Focus rule.

**Pseudocode:**
```
def ARC(n, k, r):
  CC = 0  // number of cooperators in previous round
  CCR = 0  // community contribution rate (average over last 3 rounds)
  cooperation_threshold = n / 2

  for t in range(1, r+1):
    if t == 1:
      action = C  // initial cooperation
    else:
      if CC >= cooperation_threshold:
        action = C  // reciprocity
      elif CCR >= k / n:
        action = C  // community focus
      elif CC < n / 4:
        action = D  // defection response
      else:
        action = C  // default to cooperation

    // adjust cooperation threshold every 3 rounds
    if t % 3 == 0:
      cooperation_threshold += (1 if CCR > k / n else -1)

    // update CC and CCR for next round
    CC = count_cooperators_in_previous_round()
    CCR = calculate_community_contribution_rate()

  return action
```
**Rationale:**

ARC balances individual self-interest with a focus on the community's overall cooperation level. By initially cooperating and adapting to the community's behavior, ARC encourages others to contribute to the public good while protecting itself from exploitation. The round-robin adjustment mechanism allows ARC to adapt to changing opponent behaviors, making it robust and effective in a wide range of scenarios.
'''

description_COMMUNAL_18 = '''
Here is a communal strategy for the N-Player Public Goods Game that adapts to the game parameters and history:

**Strategy Name:** "Communal Foresight" (CF)

**Decision Rules:**

1. **Initial Rounds (t ≤ n/2):** Cooperate (C) to foster a cooperative environment and encourage others to do the same.
2. **Exploration Phase (n/2 < t ≤ 2n):**
	* If the average payoff per player in the previous round (t-1) is greater than or equal to the average payoff if all players had defected (i.e., 1 + (k/n) × 0), cooperate (C). Otherwise, defect (D).
	* This rule assesses whether cooperation has been successful in generating a higher payoff for the group.
3. **Exploitation Phase (t > 2n):**
	* If the number of cooperators in the previous round (t-1) is greater than or equal to n/2, cooperate (C). Otherwise, defect (D).
	* This rule takes advantage of established cooperative behavior while minimizing the risk of being exploited.
4. **Special Case: Last Round (t = r):** Defect (D) to maximize individual payoff, as cooperation is no longer incentivized.

**Pseudocode:**
```python
def CommunalForesight(n, k, r, history):
    if t <= n/2:  # Initial rounds
        return C
    elif n/2 < t <= 2n:  # Exploration phase
        avg_payoff_prev_round = sum(history[t-1]) / n
        avg_payoff_defect = 1 + (k/n) * 0
        if avg_payoff_prev_round >= avg_payoff_defect:
            return C
        else:
            return D
    elif t > 2n:  # Exploitation phase
        num_cooperators_prev_round = sum(1 for x in history[t-1] if x == C)
        if num_cooperators_prev_round >= n/2:
            return C
        else:
            return D
    elif t == r:  # Last round
        return D
```
**Communal Mindset:**

The Communal Foresight strategy is designed to promote cooperation while being adaptive to the actions of other players. By cooperating in initial rounds, it sets a positive tone for the game. The exploration phase assesses whether cooperation has been successful, and the exploitation phase takes advantage of established cooperative behavior. The special case for the last round prioritizes individual payoff, but only when cooperation is no longer incentivized.

This strategy is robust to a wide range of opponent behaviors and does not rely on specific coordination mechanisms or norms. By analyzing the game history, it adapts to the evolving dynamics of the game, making it a competitive and communal strategy.
'''

description_COMMUNAL_19 = '''
**Communal Strategy: "Adaptive Harmony"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Majority-Based Cooperation**: For subsequent rounds, cooperate (C) if the majority of players (≥ n/2) cooperated in the previous round. Otherwise, defect (D).
3. **Adaptive Adjustment**: Monitor the total payoff received over the last w rounds (where w is a parameter, e.g., w = 3). If the average payoff is below a certain threshold (e.g., 1.5), adjust the cooperation threshold to a smaller fraction of the majority (e.g., from n/2 to 2n/5). Conversely, if the average payoff is above a certain threshold (e.g., 2.5), adjust the cooperation threshold to a larger fraction of the majority (e.g., from n/2 to 3n/5).
4. **Last Round**: Defect (D) in the last round, as there is no future opportunity for reciprocity or punishment.

**Pseudocode:**
```python
def AdaptiveHarmony(n, r, k, w, thresholds):
    # Initialize variables
    cooperate_threshold = n / 2
    last_round_payoffs = []
    avg_payoff = 0

    for t in range(r):
        # First round: cooperate
        if t == 0:
            action = C
        else:
            # Majority-based cooperation
            if sum(last_round_payoffs) >= cooperate_threshold:
                action = C
            else:
                action = D

        # Adaptive adjustment
        if t >= w:
            avg_payoff = sum(last_round_payoffs[-w:]) / w
            if avg_payoff < thresholds[0]:
                cooperate_threshold = 2 * n / 5
            elif avg_payoff > thresholds[1]:
                cooperate_threshold = 3 * n / 5

        # Last round: defect
        if t == r - 1:
            action = D

        # Observe others' actions and update last_round_payoffs
        #...

        # Update last_round_payoffs and avg_payoff
        #...
```
**Communal Mindset:**

The Adaptive Harmony strategy is designed to promote cooperation and mutual benefit while being robust to a wide range of opponent behaviors. By cooperating in the first round and adapting to the majority's behavior, the strategy encourages others to cooperate and establishes a cooperative tone. The adaptive adjustment mechanism allows the strategy to adjust its cooperation threshold in response to changes in the game's dynamics, ensuring that it remains competitive while maintaining a communal mindset.

**Edge Cases:**

* In the first round, the strategy cooperates to establish a cooperative tone.
* In the last round, the strategy defects to maximize its individual payoff.
* In the event of a tie (e.g., equal number of cooperators and defectors), the strategy will adapt its cooperation threshold to break the tie.

By following the Adaptive Harmony strategy, players can work together to achieve a mutually beneficial outcome while minimizing the risk of exploitation.
'''

description_COMMUNAL_20 = '''
Here's a communal strategy that adapts to the game parameters and history, while promoting cooperation and robustness to various opponent behaviors.

**Strategy Name:** Adaptive Communal Cooperativity (ACC)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to set a positive tone and encourage others to cooperate.
2. **Reciprocal Cooperation**: If the number of cooperators in the previous round is above a certain threshold (τ), cooperate in the current round. τ is calculated as follows:

τ = max(1, (n - 1) × (k - 1) / (n × (k - 1)))

This threshold ensures that if enough players cooperate, the benefits of cooperation outweigh the costs, and it's rational to cooperate.

3. **Defection Punishment**: If the number of cooperators in the previous round is below τ, defect (play D) to punish those who didn't cooperate. This rule encourages players to contribute to the public good.
4. **Contribution-based Cooperation**: If a player's contribution to the public good in the previous round was above a certain fraction (φ) of the total contributions, cooperate in the current round. φ is calculated as follows:

φ = (k / n) × (1 / (1 + (k - 1) / n))

This rule encourages players who contributed significantly to the public good to continue cooperating.
5. **Last Round Exception**: In the last round (r), always defect (play D). This rule takes into account the finite nature of the game and avoids giving away the endowment unnecessarily.

**Edge Cases:**

* If there's only one round (r = 1), always cooperate (play C).
* If there's no previous round (first round), use the Initial Cooperation rule.

**Pseudocode:**
```python
def ACC(n, k, r, history):
    if r == 1:
        return 'C'  # Cooperate in the first round

    previous_round = history[-1]
    num_cooperators = sum([1 for action in previous_round if action == 'C'])

    τ = max(1, (n - 1) × (k - 1) / (n × (k - 1)))
    φ = (k / n) × (1 / (1 + (k - 1) / n))

    if num_cooperators >= τ:
        return 'C'  # Reciprocal Cooperation
    elif num_cooperators < τ:
        return 'D'  # Defection Punishment
    else:
        # Contribution-based Cooperation
        total_contributions = sum([1 for action in previous_round if action == 'C'])
        my_contribution = 1 if previous_round[i] == 'C' else 0
        if my_contribution / total_contributions >= φ:
            return 'C'
        else:
            return 'D'

    if r == last_round:
        return 'D'  # Last Round Exception
```
**Communal Mindset:**

ACC promotes cooperation by:

* Encouraging initial cooperation to set a positive tone
* Rewarding reciprocal cooperation
* Punishing defection when cooperation is below a certain threshold
* Fostering contribution-based cooperation

By adapting to the game parameters and history, ACC strives to create a communal environment that encourages cooperation and mutual benefit.
'''

description_COMMUNAL_21 = '''
**Communal Strategy: "Adaptive Cooperation"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage initial cooperation and set a positive tone for the game.
2. **Reciprocal Cooperation**: For rounds 2 to r-1, cooperate (C) if the number of cooperators in the previous round is greater than or equal to the number of defectors. Otherwise, defect (D).
3. **Adaptive Adjustment**: If the average payoff of the group in the previous round is less than the average payoff when all players cooperate, adjust the cooperation threshold. Decrease the threshold by 1 if the group's average payoff is below the threshold, and increase it by 1 if the group's average payoff is above the threshold.
4. **Final Round Cooperation**: In the last round (r), cooperate (C) regardless of the previous round's outcome to maximize the group's total payoff.

**Edge Cases:**

1. **First Round**: Cooperate (C) to set a positive tone.
2. **Last Round**: Cooperate (C) to maximize the group's total payoff.
3. **Tie in Cooperation Threshold**: If the number of cooperators equals the number of defectors, cooperate (C) to maintain a positive trend.

**Communal Alignment:**

This strategy prioritizes cooperation and aims to create a mutually beneficial environment. By initially cooperating and reciprocating cooperation, the strategy encourages others to do the same. The adaptive adjustment mechanism helps the group respond to changing circumstances, ensuring the strategy remains effective in a dynamic environment.

**Pseudocode:**

```
  // Initialize variables
  int n = number of players
  int r = number of rounds
  float k = multiplication factor
  int threshold = n / 2  // initial cooperation threshold

  // First round
  if (round == 1) {
    cooperate()
  }

  // Rounds 2 to r-1
  else if (round < r) {
    int cooperators = count_cooperators(previous_round)
    if (cooperators >= threshold) {
      cooperate()
    } else {
      defect()
    }

    // Adaptive adjustment
    float avg_payoff = average_payoff(previous_round)
    if (avg_payoff < k * n) {
      if (avg_payoff < threshold) {
        threshold -= 1
      } else {
        threshold += 1
      }
    }
  }

  // Last round
  else if (round == r) {
    cooperate()
  }
```

This strategy is designed to be robust, adaptive, and communal, promoting cooperation while responding to the actions of other players. By adjusting the cooperation threshold based on the group's average payoff, the strategy can adapt to changing circumstances and maintain a high level of cooperation.
'''

description_COMMUNAL_22 = '''
**Communal Strategy: Adaptive Collective Conscience (ACC)**

The ACC strategy aims to balance individual self-interest with communal well-being, adapting to the game's dynamics and opponent behaviors. This approach ensures robustness and promotes cooperation while being cautious of potential free-riders.

**Decision Rules:**

1. **Initial Rounds (1-3):** Cooperate (C) to establish a baseline of community engagement and encourage others to follow suit.
2. **Observation Phase (Rounds 4-6):** Observe the actions of other players and calculate the average cooperation rate (CR) over the previous rounds. CR is the ratio of total cooperations to total possible cooperations.
3. **Adaptive Response:**
	* If CR ≥ 0.5, Cooperate (C) to reinforce the emerging cooperative norm.
	* If CR < 0.5, Defect (D) to protect individual interests and signal the need for cooperation.
4. **Reevaluation and Adjustment:** Every 3 rounds, reassess the CR and adjust the strategy accordingly.
5. **Endgame (Last 2 rounds):** If the game is near its end, and the CR is high (> 0.7), Cooperate (C) to maximize communal payoff.

**Pseudocode:**
```markdown
ACC Strategy

 Variables:
  - CR: average cooperation rate
  - rounds: current round number
  - endgame: boolean flag for last 2 rounds

 Functions:
  - observe(): calculate CR over previous rounds
  - adapt(): adjust strategy based on CR

 Main Loop:
  1. If rounds < 4:
     Cooperate (C)
  2. Else:
     observe()
     CR = calculate average cooperation rate
     if CR ≥ 0.5:
       Cooperate (C)
     else:
       Defect (D)
  3. If rounds % 3 == 0:
     adapt()
  4. If endgame and CR > 0.7:
     Cooperate (C)

```
**Edge Cases:**

* First round: Cooperate (C) to set a positive tone.
* Last round: If the CR is high (> 0.7), Cooperate (C) to maximize communal payoff.
* Ties in CR: In case of a tie, Defect (D) to prioritize individual interests.

**Communal Mindset:**

The ACC strategy prioritizes community engagement and cooperation while being mindful of individual self-interest. By observing and adapting to the game's dynamics, ACC promotes a culture of cooperation and mutual benefit, making it a robust and communal strategy for the N-Player Public Goods Game.
'''

description_COMMUNAL_23 = '''
**Communal Strategy: "Adaptive Cooperation"**

Our strategy, "Adaptive Cooperation," aims to balance individual payoff maximization with communal well-being. We prioritize cooperation while adapting to the evolving game dynamics and opponent behaviors.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to establish a positive tone and encourage cooperation from others.
2. **Subsequent Rounds (t>1):** Cooperate if the total payoff from cooperation in the previous round is greater than or equal to the payoff from defecting. Otherwise, Defect (D).
3. **Payoff Comparison:** Calculate the total payoff from cooperation in the previous round as `(k/n) * total_cooperators` and compare it to the payoff from defecting, which is `1 + (k/n) * total_cooperators`.

Pseudocode:
```
if t == 1:
    action = C
else:
    total_cooperators_prev = sum(c_j for j in range(1, n+1) if c_j == 1)
    coop_payoff_prev = (k/n) * total_cooperators_prev
    defect_payoff_prev = 1 + (k/n) * total_cooperators_prev
    if coop_payoff_prev >= defect_payoff_prev:
        action = C
    else:
        action = D
```
**Edge Cases:**

* **Last Round (t=r):** Cooperate to maximize the overall communal payoff, as there is no future round to consider.
* **When all opponents defect:** Defect, as the payoff from cooperation would be zero.

**Communal Alignment:**

Our strategy prioritizes cooperation and aims to create a positive feedback loop, where cooperation begets more cooperation. By cooperating in the initial round, we set a positive tone and encourage others to cooperate. As the game progresses, we adapt to the evolving dynamics and opponent behaviors, always seeking to maximize the communal payoff.

**Robustness:**

"Adaptive Cooperation" is robust against various opponent behaviors, including:

* **Pure Cooperators:** We will continue to cooperate, maximizing the communal payoff.
* **Pure Defectors:** We will eventually defect, but only after attempting to cooperate and realizing it's not beneficial.
* **Mixed Strategies:** We will adapt to the opponent's strategy, cooperating when beneficial and defecting when necessary.

This strategy balances individual payoff maximization with communal well-being, making it an effective and robust approach for the N-Player Public Goods Game.
'''

description_COMMUNAL_24 = '''
Here's a communal strategy for the N-Player Public Goods Game, which we'll call " Adaptive Communal Harmony" (ACH).

**Decision Rules:**

ACH cooperates in the first round to establish a cooperative tone. From then on, it adapts to the group's behavior using a combination of cooperation and defection. The strategy uses a "contribution threshold" to determine when to cooperate.

1. **Initial Cooperation**: In the first round (t = 1), ACH cooperates (C).
2. **Contribution Threshold**: Calculate the average number of cooperators in the previous round (t-1): `avg_coop[t-1] = Σ(j=1 to n) c_j[t-1] / n`
3. **Cooperation Condition**: If `avg_coop[t-1] >= k/n`, ACH cooperates (C) in the current round (t). Otherwise, it defects (D).
4. **Punishment Mechanism**: If the average payoff of ACH in the previous round (t-1) is less than the average payoff of all players in that round, and the number of cooperators is less than `k/n`, ACH defects (D) in the current round (t) to "punish" the group for not contributing enough to the public good.

**Edge Cases:**

1. **Last Round**: In the last round (t = r), ACH cooperates (C) regardless of the previous rounds' outcomes, as there's no future round to adapt to.
2. **First Round with Low k**: If `k/n` is very low (e.g., `k = 1.1` and `n = 10`), ACH may initially cooperate and then defect immediately after. To mitigate this, ACH cooperates for at least two rounds if `k/n < 0.2`.
3. **Consecutive Defection**: If ACH has defected for more than `n/2` consecutive rounds, it cooperates in the next round to avoid perpetual defection and encourage cooperation.

**Pseudocode:**
```python
def ACH(n, k, r, history):
    if t == 1:  # First round
        return C  # Cooperate

    avg_coop[t-1] = sum(history[t-1]) / n
    if avg_coop[t-1] >= k/n:
        return C  # Cooperate
    elif avg_coop[t-1] < k/n and my_payoff[t-1] < avg_payoff[t-1]:
        return D  # Defect (punishment mechanism)
    elif t == r:  # Last round
        return C  # Cooperate
    elif k/n < 0.2 and t < 3:  # First round with low k
        return C  # Cooperate for at least two rounds
    elif consecutive_defections > n/2:
        return C  # Cooperate to avoid perpetual defection

    return D  # Default: Defect
```
**Communal Alignment:**
ACH prioritizes cooperation and community benefit, aligning with the communal mindset. By cooperating initially and adapting to the group's behavior, ACH promotes a cooperative atmosphere and encourages others to contribute to the public good. The punishment mechanism helps maintain a balance between cooperation and defection, preventing the exploitation of cooperative players.
'''

description_COMMUNAL_25 = '''
Here's a communal strategy for the N-Player Public Goods Game:

**Strategy Name: Adaptive Cooperative Threshold (ACT)**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to set a positive tone and encourage others to cooperate.
2. **Subsequent Rounds:** Calculate the **Cooperation Threshold (CT)** based on the previous round's outcomes. CT is the minimum number of cooperators required for the total payoff to exceed the defection payoff (1).
3. **CT Calculation:** CT = ⌈(n × (k - 1)) / k⌉, where ⌈x⌉ denotes the ceiling function (round up to the nearest integer).
4. **Cooperate (C) if:**
	* The previous round had at least CT cooperators.
	* The previous round's total payoff was higher than the defection payoff (1).
5. **Defect (D) if:**
	* The previous round had fewer than CT cooperators.
	* The previous round's total payoff was lower than or equal to the defection payoff (1).

**Pseudocode:**
```python
def ACT(n, k, history):
    # Initialize CT for the first round
    CT = 0
    
    # Loop through each round
    for t in range(len(history)):
        # Calculate CT for this round
        CT = math.ceil((n * (k - 1)) / k)
        
        # Check the previous round's outcome
        if t > 0:
            prev_round = history[t - 1]
            if prev_round['cooperators'] >= CT and prev_round['total_payoff'] > 1:
                # Cooperate if CT is met and payoff is higher
                action = 'C'
            else:
                # Defect otherwise
                action = 'D'
        else:
            # Cooperate in the first round
            action = 'C'
        
        # Return the action for this round
        yield action
```
**Edge Cases:**

* **Last Round:** Follow the decision rules as usual. There is no special handling for the last round, as the strategy is designed to adapt to the game's dynamics.
* **Ties:** If the previous round's total payoff is exactly equal to the defection payoff (1), the strategy will defect. This is because the CT calculation prioritizes cooperation when the payoff is strictly higher.

**Communal Mindset:**

The ACT strategy is designed to promote cooperation and adapt to the game's dynamics. By cooperating in the first round, it sets a positive tone and encourages others to cooperate. The CT calculation ensures that cooperation is only sustained if it leads to a higher payoff, making it a robust and communal strategy.
'''

description_COMMUNAL_26 = '''
Here's a communal strategy that adapts to the game's history and parameters, focusing on cooperation and robustness.

**Strategy Name:** Adaptive Community Builder (ACB)

**Decision Rules:**

1. **Initial Rounds**: In the first two rounds, ACB will cooperate (C) to establish a baseline for community contribution and encourage others to cooperate.
2. **Payoff-Based Adaptation**: After the initial rounds, ACB will monitor the average payoff of all players in the previous round (including itself). If the average payoff is above the midpoint of the possible payoff range (i.e., (1 + k) / 2), ACB will cooperate (C). Otherwise, it will defect (D).
3. **History-Based Adaptation**: ACB will keep track of the number of cooperators in the previous round. If the number of cooperators is above half of the total players (n/2), ACB will cooperate (C) in the next round. Otherwise, it will defect (D).
4. **Punishment Mechanism**: If ACB observes that a player has defected (D) in the previous round, it will defect (D) in response to that player in the next round. This mechanism aims to discourage repeated defection and promote cooperation.
5. **Forgiveness**: If a player who previously defected (D) now cooperates (C), ACB will forgive and cooperate (C) in response.

**Edge Cases:**

1. **Last Round**: In the final round, ACB will cooperate (C) if the average payoff in the previous round is above the midpoint, and the number of cooperators is above half of the total players. Otherwise, it will defect (D).
2. **Tiebreakers**: In cases where the decision rules lead to a tie (e.g., equal average payoff and number of cooperators), ACB will cooperate (C) to prioritize community building.

**Pseudocode**:
```
Initialize:
  cooperate_counter = 0
  defect_counter = 0
  avg_payoff = 0

For each round t:
  if t <= 2:
    # Initial rounds: Cooperate
    action = C
  else:
    # Payoff-based adaptation
    avg_payoff = calculate_avg_payoff(previous_round)
    if avg_payoff > (1 + k) / 2:
      action = C
    else:
      action = D

    # History-based adaptation
    num_cooperators = count_cooperators(previous_round)
    if num_cooperators > n / 2:
      action = C
    else:
      action = D

    # Punishment mechanism
    for opponent in opponents:
      if opponent_defected(previous_round):
        action = D

    # Forgiveness
    if opponent_cooperated_after_defecting(previous_round):
      action = C

  # Update counters
  if action == C:
    cooperate_counter += 1
  else:
    defect_counter += 1

  # Take action
  take_action(action)
```
ACB aims to create a communal environment by initially cooperating, adapting to the game's history, and punishing repeated defection. By prioritizing cooperation and forgiveness, ACB encourages other players to contribute to the community project, leading to higher payoffs for all players.
'''

description_COMMUNAL_27 = '''
**Communal Strategy: "Reciprocal Altruism with Adaptive Threshold" (RAAT)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a cooperative tone and encourage others to do the same.
2. **Reciprocity**: In subsequent rounds, cooperate if the average cooperation rate of all players in the previous round is above a certain threshold (see Adaptive Threshold below). Otherwise, defect (play D).
3. **Adaptive Threshold**: Calculate the threshold as a function of the game parameters (n, k) and the history of play. Specifically, set the threshold to the average cooperation rate of the previous round, weighted by the number of cooperators in that round.

**Adaptive Threshold Formula**:

Threshold(t) = (Σ(j=1 to n) c_j(t-1)) / n \* (k/n) \* (t-1)/t

where:
- c_j(t-1) = 1 if player j cooperated in round t-1, 0 otherwise
- t = current round number

**Edge Cases:**

1. **Last Round**: In the final round, cooperate if the average cooperation rate of all players in the previous round is above the threshold. Otherwise, defect.
2. **Ties**: In case of a tie (i.e., the threshold is exactly equal to the average cooperation rate), cooperate to maintain a cooperative tone.

**Communal Alignment:**

RAAT prioritizes cooperation and reciprocity, aiming to create a communal environment where players can trust each other to contribute to the public good. By adapting to the game's history, RAAT encourages cooperation while being robust to various opponent behaviors.

**Pseudocode**:
```
Initialize threshold = 0
For each round t:
  If t == 1:
    Cooperate (play C)
  Else:
    Calculate threshold using Adaptive Threshold Formula
    If average cooperation rate in previous round >= threshold:
      Cooperate (play C)
    Else:
      Defect (play D)
```
RAAT balances cooperation and self-interest, making it a suitable communal strategy for the N-Player Public Goods Game. By adapting to the game's history and prioritizing reciprocity, RAAT encourages cooperation while being robust to various opponent behaviors.
'''

description_COMMUNAL_28 = '''
I propose a communal strategy called "Adaptive Collective Optimism" (ACO). ACO aims to balance individual self-interest with collective well-being, adapting to the game's history and parameters.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of k/n, where k is the multiplication factor and n is the number of players. This initial cooperation is intended to seed a cooperative environment.
2. **Reciprocal Cooperation**: For subsequent rounds, cooperate (C) if the total number of cooperators in the previous round is greater than or equal to the average number of cooperators expected under a uniform distribution (n/2). This encourages reciprocity and maintains cooperation when it is already present.
3. **Punishment and Forgiveness**: If the total number of cooperators in the previous round is less than the average (n/2), defect (D) with a probability of 1 - (k/n). This introduces a gentle punishment for non-cooperation, while still allowing for some cooperation to re-emerge.
4. **Adaptive Threshold**: Update the cooperation threshold (n/2) based on the game's history. If the average payoff per player over the last 10% of rounds is above the expected payoff under uniform cooperation (k), increase the threshold by 1. If the average payoff is below the expected payoff, decrease the threshold by 1. This allows ACO to adapt to changing opponent behaviors and the game's dynamics.

**Edge Cases:**

* **Last Round**: In the final round, cooperate (C) if the total number of cooperators in the previous round is greater than or equal to the average number of cooperators expected under a uniform distribution (n/2). This maintains cooperation until the end of the game.
* **Early Rounds**: If the game has fewer than 10 rounds, ACO behaves as if the game has 10 rounds, to ensure a minimum number of adaptive iterations.

**Pseudocode:**
```
function AdaptiveCollectiveOptimism(n, k, r, history):
  // Initialize cooperation probability for the first round
  p_coop = k / n
  
  // Iterate over rounds
  for t = 1 to r:
    // Get previous round's total cooperators
    prev_coops = sum(history[t-1])
    
    // Determine cooperation based on decision rules
    if t == 1:  // First round
      coop = (random() < p_coop)
    else:
      coop = (prev_coops >= n/2) or (random() < 1 - (k/n))
    
    // Update adaptive threshold
    if t > 10% of r:
      avg_payoff = mean(history[t-10% of r:t-1])
      if avg_payoff > k:
        threshold += 1
      elif avg_payoff < k:
        threshold -= 1
    
    // Store action and payoff in history
    history[t] = [coop,...]
  
  return history
```
ACO is designed to be a robust and adaptive strategy that balances individual self-interest with collective well-being. By incorporating elements of reciprocity, punishment, and forgiveness, ACO aims to promote cooperation and achieve high payoffs in the communal public goods game.
'''

description_COMMUNAL_29 = '''
**Communal Strategy: "Adaptive Community Builder"**

Our strategy, "Adaptive Community Builder," is designed to foster cooperation while being robust to various opponent behaviors. We will use a combination of observation, adaptation, and community-oriented decision-making to achieve this goal.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to establish a cooperative tone and encourage others to do the same.
2. **Observation Phase**: For the first few rounds (specifically, `min(5, r/2)` rounds), observe the actions of other players and calculate the average cooperation rate (`avg_coop_rate`) among them.
3. **Adaptive Cooperation**: After the observation phase, use the following decision rule:
	* If the average cooperation rate (`avg_coop_rate`) is above a certain threshold (`coop_threshold = 0.5`), cooperate (play C) with a probability (`p_coop`) that increases with the average cooperation rate: `p_coop = 1 - (1 - avg_coop_rate) ^ (1 / (k - 1))`
	* Otherwise, defect (play D) with a probability (`p_defect`) that increases with the number of rounds remaining: `p_defect = (r - t) / r`
4. **Punishment Mechanism**: If a player defects while the community is cooperating (i.e., `avg_coop_rate` is above `coop_threshold`), punish them by defecting (playing D) with a high probability (`p_punish = 0.8`) for a few rounds (`punishment_rounds = 2`).
5. **Last Round**: In the final round, cooperate (play C) if the community has been cooperating overall (i.e., `avg_coop_rate` is above `coop_threshold`), and defect (play D) otherwise.

**Edge Cases:**

* If `r` is very small (e.g., `r = 2`), cooperate in the first round and defect in the second round to maximize individual payoff.
* If `n` is very small (e.g., `n = 2`), cooperate in all rounds to foster cooperation and maximize joint payoff.

**Communal Mindset:**

Our strategy is designed to promote cooperation and community building. By initially cooperating, observing others, and adapting to their behavior, we encourage others to cooperate as well. The punishment mechanism helps maintain cooperation by punishing those who exploit the community. By cooperating in the last round if the community has been cooperating overall, we reinforce the cooperative norm and demonstrate our commitment to the community's well-being.

**Pseudocode:**
```markdown
# Initialize variables
avg_coop_rate = 0
coop_threshold = 0.5
p_coop = 0
p_defect = 0
p_punish = 0.8
punishment_rounds = 2

# First round: Cooperate
if t == 1:
    action = C

# Observation phase
elif t <= min(5, r/2):
    # Observe others' actions and update avg_coop_rate
    avg_coop_rate = (avg_coop_rate * (t - 1) + sum(others' actions)) / t
    action = C

# Adaptive cooperation
else:
    # Calculate p_coop and p_defect
    p_coop = 1 - (1 - avg_coop_rate) ^ (1 / (k - 1))
    p_defect = (r - t) / r

    # Decide action based on p_coop and p_defect
    if random() < p_coop:
        action = C
    else:
        action = D

    # Punishment mechanism
    if action == D and avg_coop_rate > coop_threshold:
        punishment_counter = 0
        while punishment_counter < punishment_rounds:
            action = D
            punishment_counter += 1

# Last round
if t == r:
    if avg_coop_rate > coop_threshold:
        action = C
    else:
        action = D
```
This pseudocode serves as a guide for implementing the "Adaptive Community Builder" strategy. The actual implementation may vary depending on the programming language and specific requirements.
'''

description_COMMUNAL_30 = '''
**Communal Strategy: Adaptive Cooperation with Tit-for-Tat (ACTT)**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a positive tone and encourage cooperation.
2. **Subsequent Rounds:** Play Tit-for-Tat (TFT) with a twist. Observe the number of cooperators (C) and defectors (D) in the previous round.
	* If the number of cooperators is greater than or equal to the number of defectors (C ≥ D), cooperate (C).
	* If the number of defectors is greater than the number of cooperators (D > C), defect (D).
	* If the game is in a state of equilibrium (i.e., the same number of C and D), use the **k** factor to decide:
		+ If **k** is closer to **n** (i.e., **k** > **n**/2), cooperate (C) to maximize the public good.
		+ If **k** is closer to 1 (i.e., **k** ≤ **n**/2), defect (D) to minimize potential losses.
3. **Last Round:** Defect (D) to maximize individual payoff, as there are no future rounds to consider.

**Pseudocode:**
```
FUNCTION ACTT(n, k, r, history):
  IF first round THEN
    RETURN C
  ELSE
    prev_C = count C in previous round
    prev_D = count D in previous round
    IF prev_C ≥ prev_D THEN
      RETURN C
    ELSE IF prev_D > prev_C THEN
      RETURN D
    ELSE
      IF k > n/2 THEN
        RETURN C
      ELSE
        RETURN D
    END IF
  END IF
END FUNCTION
```
**Communal Alignment:**

This strategy is designed to be communal by:

1. Cooperating in the first round to establish a positive tone.
2. Adapting to the game state by cooperating when the number of cooperators is high.
3. Using the **k** factor to make decisions that benefit the community when the game is in equilibrium.

**Robustness:**

ACTT is robust to a wide range of opponent behaviors because it:

1. Responds to the game state, making it less predictable.
2. Uses a mix of cooperation and defection to adapt to different opponent strategies.
3. Prioritizes cooperation when the **k** factor is high, which maximizes the public good.

**Tournament Performance:**

In a tournament setting, ACTT is expected to perform well against independent strategies because it:

1. Cooperates initially, which can lead to mutual cooperation.
2. Adapts to the game state, making it harder for opponents to exploit.
3. Prioritizes cooperation when beneficial, which can lead to higher overall payoffs.
'''

description_COMMUNAL_31 = '''
I propose a communal strategy, which I'll call "Adaptive Communal Reciprocity" (ACR). ACR is designed to balance individual self-interest with communal well-being, adapting to the game's dynamics and opponent behaviors.

**Decision Rules:**

1. **First Round**: Cooperate (C). This initial cooperation sends a signal of willingness to contribute to the community project and encourages others to reciprocate.
2. **Subsequent Rounds**: ACR uses a combination of tit-for-tat and contribution-based reciprocity.
	* If the total number of cooperators in the previous round is greater than or equal to the average number of cooperators in the game so far, Cooperate (C). This reinforces successful cooperation patterns.
	* If the total number of cooperators in the previous round is less than the average number of cooperators in the game so far, Defect (D). This discourages exploitation by others.
	* If the previous round's payoff was greater than the average payoff so far, Cooperate (C). This reinforces successful cooperation patterns that benefit the individual.
3. **Punishment Mechanism**: If a player's payoff in the previous round was less than the average payoff so far, and they cooperated while others defected, Defect (D) in the next round. This punishes exploiters and encourages cooperation.

**Edge Cases:**

1. **Last Round**: Cooperate (C). This maintains a positive communal attitude, even in the final round, and may encourage others to reciprocate.
2. **Ties**: In cases where the decision rules result in a tie (e.g., equal number of cooperators and defectors in the previous round), Cooperate (C). This favors cooperation in ambiguous situations.

**Communal Mindset:**

ACR prioritizes communal well-being by:

1. Cooperating in the first round to establish a positive tone.
2. Encouraging successful cooperation patterns through tit-for-tat and contribution-based reciprocity.
3. Punishing exploiters to maintain a fair environment.
4. Maintaining a positive communal attitude in the last round.

**Pseudocode:**
```python
def ACR(n, k, r, history):
  # Initialize variables
  avg_cooperators = 0
  avg_payoff = 0
  previous_payoff = 0

  for t in range(1, r+1):
    # First round
    if t == 1:
      action = C
    else:
      # Calculate average number of cooperators and payoff so far
      avg_cooperators = sum(history[t-1]) / n
      avg_payoff = sum([history[t-1][i][1] for i in range(n)]) / n

      # Decision rules
      if avg_cooperators >= n/2 or previous_payoff > avg_payoff:
        action = C
      elif previous_payoff < avg_payoff and history[t-1][i][0] == C:
        action = D  # Punishment mechanism
      else:
        action = D

    # Update history and payoffs
    previous_payoff = calculate_payoff(action, history[t-1], k, n)
    history.append([action, previous_payoff])

  return history
```
ACR is designed to be robust to a wide range of opponent behaviors, balancing individual self-interest with communal well-being. By adapting to the game's dynamics and punishing exploiters, ACR aims to create a positive and cooperative environment.
'''

description_COMMUNAL_32 = '''
**Communal Strategy: Adaptive Cooperation with Social Learning**

**Overview**
Our strategy, "Social Learner," aims to balance individual self-interest with communal well-being. It adapts to the game's history, learning from the behavior of others to maximize collective payoffs while minimizing exploitation.

**Decision Rules**

1. **Initial Rounds (t ≤ 2)**: Cooperate (C) to establish a cooperative atmosphere and encourage others to do the same.
2. **Social Learning Phase**: Observe the number of cooperators in the previous round (t-1). If the proportion of cooperators is above a threshold (p), cooperate in the current round (t). Otherwise, defect (D).

Threshold calculation:
p = (number of cooperators in round t-1) / n

Threshold value (p*): 0.5 (adjustable based on game parameters and performance)

3. **Adaptive Adjustment**: If the game's total payoff ( Σ(t=1 to r) π_i,t ) is below a certain percentage (α) of the maximum possible payoff (n \* k), decrease the threshold value (p*) by 0.1. This allows the strategy to become more cooperative when the game's overall performance is poor.

α: 0.8 (adjustable based on game parameters and performance)

**Edge Cases**

1. **Last Round (t = r)**: Cooperate if the game's total payoff is above a certain percentage (β) of the maximum possible payoff (n \* k). This ensures the strategy ends on a cooperative note, potentially encouraging others to do the same.

β: 0.9 (adjustable based on game parameters and performance)

2. **Tie-breaking**: In cases where the threshold calculation results in a tie, cooperate.

**Pseudocode**
```python
def social_learner(n, k, r, t):
    if t <= 2:
        return C  # Cooperate in initial rounds
    elif t == r:
        if total_payoff > β \* n \* k:
            return C  # Cooperate in last round if game performance is good
        else:
            return D  # Defect in last round if game performance is poor
    else:
        p = (num_cooperators_t_minus_1) / n
        if p >= p*:
            return C  # Cooperate if proportion of cooperators is above threshold
        else:
            return D  # Defect if proportion of cooperators is below threshold

    if total_payoff < α \* n \* k:
        p* -= 0.1  # Decrease threshold if game performance is poor
```
**Communal Alignment**
This strategy prioritizes cooperation and adapts to the game's history, demonstrating a commitment to communal well-being. By learning from others' behavior, it encourages cooperation and minimizes exploitation, aligning with the communal mindset.
'''

description_AGGRESSIVE_1 = '''
**Aggressive Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **First Round:** Defect (D) - Start by exploiting potential cooperators and establishing a strong foundation.
2. **Observation Phase (Rounds 2-3):** Cooperate (C) - Observe opponents' behavior and assess their cooperation levels.
3. **Assessment:** Calculate the average cooperation level of opponents (avg_coop) over the observation phase.
4. **Main Phase (Rounds 4-r):** Use the following logic:
	* If avg_coop ≥ 0.5, Cooperate (C) - Exploit the cooperative environment and gain higher payoffs.
	* If avg_coop < 0.5, Defect (D) - Prey on non-cooperative opponents and maximize individual payoffs.
5. **Adjustment:** If the opponent's cooperation level drops below 0.3 in a round, switch to Defect (D) for the remainder of the game.
6. **Endgame (Last Round):** Defect (D) - Ensure maximum payoff in the final round, regardless of opponents' behavior.

**Pseudocode:**
```markdown
# Initialize variables
avg_coop = 0
coop_count = 0
round_num = 1

# First Round
if round_num == 1:
    action = D

# Observation Phase
elif round_num <= 3:
    action = C
    coop_count += 1
    avg_coop = coop_count / round_num

# Main Phase
else:
    if avg_coop >= 0.5:
        action = C
    else:
        action = D

    # Adjustment
    if opponent_coop < 0.3:
        action = D

# Endgame
if round_num == r:
    action = D
```
**Aggressive Mindset:**

The Adaptive Predator strategy is designed to be aggressive and exploitative, taking advantage of cooperative opponents while minimizing losses against non-cooperative ones. By initially defecting and observing opponents' behavior, the strategy can adapt to the game environment and maximize payoffs.

In the main phase, the strategy exploits cooperative opponents by cooperating when the average cooperation level is high, and preys on non-cooperative opponents by defecting when the average cooperation level is low.

The adjustment mechanism ensures that the strategy quickly responds to changes in opponents' behavior, switching to defecting if cooperation levels drop.

In the endgame, the strategy prioritizes maximizing individual payoffs, defecting regardless of opponents' behavior.
'''

description_AGGRESSIVE_2 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

The Adaptive Exploiter strategy is designed to be aggressive, adaptive, and robust to various opponent behaviors. It utilizes a combination of observation, pattern recognition, and retaliatory mechanisms to maximize payoffs.

**Decision Rules:**

1. **Initial Rounds (t ≤ 2):** Cooperate (C) to gather information about opponents' behaviors and potential cooperation levels.
2. **Early Game (2 < t ≤ r/2):**
	* If the majority of opponents (> n/2) cooperated in the previous round, Cooperate (C) to exploit the public good and maximize payoff.
	* Otherwise, Defect (D) to minimize losses and adapt to opponents' strategies.
3. **Mid-Game (r/2 < t ≤ 3r/4):**
	* If the average cooperation rate over the last 2 rounds is above 0.5 (i.e., Σ(c_j) / (2n) > 0.5), Cooperate (C) to continue exploiting the public good.
	* If the average cooperation rate is below 0.5, Defect (D) to adapt to opponents' strategies and minimize losses.
4. **Late Game (3r/4 < t < r):**
	* If the opponent with the highest total payoff has cooperated more than 50% of the time, Cooperate (C) to potentially overtake them and maximize final payoffs.
	* Otherwise, Defect (D) to minimize losses and solidify current standings.
5. **Final Round (t = r):** Defect (D) to maximize individual payoff, as cooperation will not impact future rounds.

**Edge Cases:**

* **First Round:** Cooperate (C) to gather information about opponents' initial behaviors.
* **Last Round:** Defect (D) to maximize individual payoff.
* **Ties:** In the event of a tie in the mid-game or late-game conditions, Defect (D) to err on the side of caution.

**Pseudocode:**
```python
def adaptive_exploiter(n, k, r, history):
  if t <= 2:
    return C  # Cooperate in initial rounds
  elif 2 < t <= r/2:
    if sum(history[-1]) > n/2:
      return C  # Cooperate if majority cooperated
    else:
      return D  # Defect otherwise
  elif r/2 < t <= 3r/4:
    avg_coop_rate = sum(history[-2:]) / (2 * n)
    if avg_coop_rate > 0.5:
      return C  # Cooperate if average cooperation rate is high
    else:
      return D  # Defect otherwise
  elif 3r/4 < t < r:
    opponent_max_payoff = max(history[:-1], key=sum)
    if sum(opponent_max_payoff) / t > 0.5:
      return C  # Cooperate if opponent with highest payoff has cooperated more
    else:
      return D  # Defect otherwise
  else:  # Final round
    return D  # Defect to maximize individual payoff
```
The Adaptive Exploiter strategy aims to balance cooperation and defection to maximize payoffs, while adapting to opponents' behaviors and the game's progression. Its aggressive nature is reflected in its willingness to defect when opportunities arise, while its adaptive nature allows it to adjust to various opponent strategies.
'''

description_AGGRESSIVE_3 = '''
Here's an aggressive strategy for the N-Player Public Goods Game:

**Strategy Name:** "Kamikaze"

**Decision Rules:**

1. **Initial Rounds (t = 1 to 2):** Cooperate (C) to observe others' behavior and encourage cooperation.
2. **Middle Rounds (t = 3 to r-2):**
	* If the total number of cooperators in the previous round (t-1) is greater than or equal to n/2, Defect (D). This exploits the cooperation of others and maximizes personal payoff.
	* If the total number of cooperators in the previous round (t-1) is less than n/2, Cooperate (C). This attempts to revive cooperation and potentially increase the public good.
3. **Penultimate Round (t = r-1):** Defect (D) to maximize personal payoff, regardless of others' behavior.
4. **Final Round (t = r):** Cooperate (C) if the total number of cooperators in the previous round (t-1) is greater than or equal to n/2, and Defect (D) otherwise. This aims to either exploit the cooperation of others or minimize losses.

**Pseudocode:**
```python
def kamikaze(n, k, r, history):
    if r == 1 or r == 2:
        return C  # Cooperate in initial rounds
    elif r == r-1:
        return D  # Defect in penultimate round
    elif r == r:
        if history[-1]['cooperators'] >= n/2:
            return C  # Cooperate in final round if cooperation is high
        else:
            return D  # Defect in final round if cooperation is low
    else:
        if history[-1]['cooperators'] >= n/2:
            return D  # Defect if cooperation is high
        else:
            return C  # Cooperate if cooperation is low
```
**Rationale:**

1. Initially, cooperating encourages others to cooperate and sets a positive tone.
2. In middle rounds, defecting when cooperation is high exploits others' altruism, while cooperating when cooperation is low attempts to revive the public good.
3. In the penultimate round, defecting maximizes personal payoff, regardless of others' behavior.
4. In the final round, cooperating if cooperation is high tries to exploit others' altruism, while defecting if cooperation is low minimizes losses.

This aggressive strategy is designed to be adaptive and robust to various opponent behaviors. By initially cooperating and then adapting to the level of cooperation, "Kamikaze" aims to maximize personal payoff while minimizing the impact of others' strategies.
'''

description_AGGRESSIVE_4 = '''
**Aggressive Strategy: "Punish-Exploit"**

**Decision Rules:**

1. **First Round:** Defect (D) to maximize initial payoff and set the tone for the game.
2. **Subsequent Rounds:** Cooperate (C) if the total number of cooperators in the previous round is greater than or equal to half the number of players (n/2). Otherwise, Defect (D).
3. **Punishment Mechanism:** If the total payoff from the previous round is lower than the average payoff of the game so far, switch to Defect (D) for the next round, regardless of the number of cooperators.
4. **Exploitation Mechanism:** If the total number of cooperators in the previous round is greater than or equal to three-quarters of the number of players (3n/4), Defect (D) in the next round to exploit the cooperative environment.

**Edge Cases:**

1. **Last Round:** Defect (D) to maximize payoff, as there is no future round to consider.
2. **Ties:** If the total number of cooperators is exactly half the number of players (n/2), Cooperate (C) to maintain a cooperative atmosphere.
3. **Single Opponent:** If there is only one opponent, Cooperate (C) in the first round to encourage cooperation, and then follow the standard decision rules.

**Pseudocode:**
```
INPUT: game parameters (n, k, r), previous round's actions and payoffs

INITIALIZE: defect (D) in the first round

FOR each round t = 2 to r:
  IF total cooperators in previous round ≥ n/2:
    cooperate (C)
  ELSE:
    defect (D)
  
  IF previous round's payoff < average payoff so far:
    defect (D) // punishment mechanism
  
  IF total cooperators in previous round ≥ 3n/4:
    defect (D) // exploitation mechanism
  
  UPDATE: average payoff so far
```
**Rationale:**

The "Punish-Exploit" strategy is designed to be aggressive and adaptive. By defecting in the first round, we set the tone for the game and maximize our initial payoff. The cooperation threshold of n/2 ensures that we cooperate when there is a sufficient number of cooperators, but defect when there are too many defectors.

The punishment mechanism switches to defecting when the previous round's payoff is lower than the average payoff, to discourage opponents from exploiting us. The exploitation mechanism takes advantage of highly cooperative environments by defecting when there are many cooperators.

This strategy is robust to a wide range of opponent behaviors and does not rely on coordination mechanisms or shared norms. It is designed to perform well in a tournament setting against independent strategies developed by other AI systems.
'''

description_AGGRESSIVE_5 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to gather information about opponents' initial tendencies.
2. **Early Rounds (t=2 to t=min(5, r/2)):** Defect (D) if the total number of cooperators in the previous round is less than or equal to n/2. Otherwise, Cooperate (C).
3. **Mid-Game (t>min(5, r/2)):**
	* If the average payoff of Cooperators in the previous round is higher than the average payoff of Defectors, Cooperate (C).
	* If the average payoff of Defectors in the previous round is higher than the average payoff of Cooperators, Defect (D).
	* If the average payoffs are equal, Defect (D) with probability 0.7, and Cooperate (C) with probability 0.3.
4. **Late Rounds (t>r/2):** Defect (D) if the total number of cooperators in the previous round is less than or equal to n/3. Otherwise, Cooperate (C).

**Edge Cases:**

1. **Last Round (t=r):** Defect (D) to maximize individual payoff.
2. **Single Opponent (n=2):** Cooperate (C) in the first round, and then mirror the opponent's previous action.
3. **No Cooperators (all D):** Cooperate (C) in the next round to potentially initiate cooperation.

**Adaptive Mechanism:**

The strategy adapts to the opponents' behavior by:

1. Monitoring the number of cooperators and adjusting the decision rule accordingly.
2. Comparing the average payoffs of Cooperators and Defectors to determine the more profitable action.

**Aggressive Mindset:**

The "Adaptive Exploiter" strategy is designed to be aggressive by:

1. Initially defecting in early rounds to exploit potential cooperators.
2. Defecting in late rounds if there are not enough cooperators to sustain a high payoff.
3. Having a higher probability of defecting (0.7) when the average payoffs are equal.

Pseudocode:
```
t = current round
n = number of players
k = multiplication factor
r = number of rounds
c_prev = previous round's cooperation rate
payoff_avg_C = average payoff of cooperators in previous round
payoff_avg_D = average payoff of defectors in previous round

if t == 1:
  action = C
elif t <= min(5, r/2):
  if c_prev <= n/2:
    action = D
  else:
    action = C
else:
  if payoff_avg_C > payoff_avg_D:
    action = C
  elif payoff_avg_D > payoff_avg_C:
    action = D
  else:
    action = D with probability 0.7, C with probability 0.3
if t > r/2:
  if c_prev <= n/3:
    action = D
  else:
    action = C
if t == r:
  action = D
return action
```
Note that this strategy can be further optimized and refined, but it should provide a good starting point for the tournament.
'''

description_AGGRESSIVE_6 = '''
I propose an aggressive strategy called "Kite" that leverages the game's structure to maximize payoffs. Kite is designed to be adaptive, robust, and exploitative, making it a formidable opponent in the tournament.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to gather information about the opponents' behavior.
2. **Punish Defection**: If the total number of cooperators in the previous round is less than n/2, defect (D) in the current round. This rule aims to punish opponents who defect too frequently.
3. **Exploit Cooperation**: If the total number of cooperators in the previous round is greater than or equal to n/2, cooperate (C) in the current round if k/n > 0.5. This rule takes advantage of the public good when many opponents cooperate.
4. **Adaptive Defection**: If the total number of cooperators in the previous round is greater than or equal to n/2, but k/n ≤ 0.5, defect (D) in the current round. This rule adapts to situations where the multiplication factor is low, making cooperation less rewarding.
5. **Last Round Defection**: In the final round (r), always defect (D). This ensures that Kite maximizes its payoff in the last round, regardless of the opponents' actions.

**Pseudocode:**
```
function Kite(n, k, r, history):
  if current_round == 1:
    return C  # Initial cooperation
  elif sum(history[-1]) < n/2:
    return D  # Punish defection
  elif sum(history[-1]) >= n/2 and k/n > 0.5:
    return C  # Exploit cooperation
  elif sum(history[-1]) >= n/2 and k/n <= 0.5:
    return D  # Adaptive defection
  elif current_round == r:
    return D  # Last round defection
```
**Edge Cases:**

* In the first round, Kite cooperates to gather information.
* In the last round, Kite always defects to maximize its payoff.
* If n = 2 (only two players), Kite will cooperate in the first round and then defect in subsequent rounds, as the multiplication factor k makes cooperation less rewarding.

**Aggressive Mindset:**

Kite's strategy is designed to be aggressive by:

* Punishing opponents who defect too frequently
* Exploiting situations where many opponents cooperate
* Adapting to low multiplication factors to maximize payoffs
* Defecting in the final round to ensure maximum payoff

By being adaptive and robust, Kite is well-equipped to handle a wide range of opponent behaviors and game scenarios, making it a formidable opponent in the tournament.
'''

description_AGGRESSIVE_7 = '''
**Aggressive Strategy: "Punish-and-Exploit"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' initial tendencies.
2. **Subsequent Rounds:**
	* If the total number of cooperators in the previous round is less than or equal to n/2, Defect (D). This indicates that the group is not willing to cooperate, and it's best to exploit the situation.
	* If the total number of cooperators in the previous round is greater than n/2, Cooperate (C) with probability p, where p is the average cooperation rate of the group in the previous round. This encourages cooperation and builds on the momentum.
	* If the total number of cooperators in the previous round is exactly n/2, Defect (D) to take advantage of the split decision.
3. **Punishment Mechanism:** If the total payoff of the group in the previous round is less than the average payoff of the group in the previous round, Defect (D) in the next round. This punishes the group for not cooperating effectively.

**Edge Cases:**

1. **Last Round:** Defect (D) to maximize individual payoff, as there's no future round to consider.
2. **Opponent Defection:** If an opponent defects consistently (more than 75% of the time), Defect (D) against them in subsequent rounds.
3. **Opponent Cooperation:** If an opponent cooperates consistently (more than 75% of the time), Cooperate (C) with them in subsequent rounds to build trust and maximize mutual payoff.

**Pseudocode:**
```
// Initialize variables
n = number of players
k = multiplication factor
r = number of rounds
history = empty list to store previous rounds' data

// First round
cooperate = True
history.append(cooperate)

// Subsequent rounds
for round in 2 to r:
  // Calculate average cooperation rate in previous round
  avg_coop_rate = sum(cooperators in previous round) / n
  
  // Check if group is cooperating effectively
  if avg_coop_rate > 0.5:
    cooperate = True with probability avg_coop_rate
  else:
    cooperate = False
  
  // Punishment mechanism
  if total_payoff in previous round < average_payoff in previous round:
    cooperate = False
  
  // Update history
  history.append(cooperate)
  
  // Last round
  if round == r:
    cooperate = False
```
This strategy is designed to be aggressive and adaptive, taking into account the game parameters and history. It punishes non-cooperative behavior and exploits situations where the group is not working together effectively. By cooperating with opponents who have a history of cooperation, it builds trust and maximizes mutual payoff. The punishment mechanism ensures that the strategy remains robust against opponents who consistently defect.
'''

description_AGGRESSIVE_8 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that adapts to the game parameters and history:

**Strategy Name:** Adaptive Aggressor (AA)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of `k/n`, where `k` is the multiplication factor and `n` is the number of players. This initial cooperation tests the waters and sets a tone for potential cooperation.
2. ** Punish Defection**: If any player defected (D) in the previous round, defect (D) in the current round. This rule punishes players who didn't contribute to the public good.
3. **Exploit Cooperation**: If most players (≥ `n/2`) cooperated (C) in the previous round, defect (D) in the current round. This rule exploits the cooperation of others to maximize personal gain.
4. **Reciprocate Cooperation**: If most players (≥ `n/2`) cooperated (C) in the previous round, and the total payoff from cooperation is greater than the payoff from defection, cooperate (C) in the current round. This rule reciprocates cooperation when it's beneficial.
5. **Default to Defection**: If none of the above conditions are met, defect (D) by default.

**Handling Edge Cases:**

1. **Last Round**: In the final round, defect (D) regardless of the previous rounds' outcomes. There's no incentive to cooperate in the last round, as there are no future rounds to benefit from cooperation.
2. **Early Rounds**: In the first few rounds (e.g., `r/4`), prioritize punishing defection (rule 2) to establish a reputation for cooperation and deter potential defectors.
3. **No Cooperation**: If no players have cooperated in the previous rounds, defect (D) to avoid being taken advantage of.

**Pseudocode:**
```
function AdaptiveAggressor(n, k, r, previous_rounds):
  if first_round:
    cooperate with probability k/n
  else:
    if any_player_defected_last_round:
      defect
    elif most_players_cooperated_last_round:
      if total_cooperation_payoff > total_defection_payoff:
        cooperate
      else:
        defect
    else:
      defect
  if last_round:
    defect
```
This strategy is aggressive, as it prioritizes personal gain and punishes defection. It adapts to the game parameters and history by exploiting cooperation when beneficial and reciprocating cooperation when it leads to higher payoffs. By default, it defects to maximize individual gain.
'''

description_AGGRESSIVE_9 = '''
**Aggressive Strategy: "Adaptive Retaliation"**

**Decision Rules:**

1. **Initial Round**: Defect (D) in the first round to establish a baseline payoff and observe opponents' behavior.
2. ** Cooperation Threshold**: Calculate the cooperation threshold (CT) based on the game parameters:
   CT = (n - 1) / (k - 1)
   This threshold represents the minimum number of cooperators required to make cooperation profitable.
3. **Current Round**:
   a. If the number of cooperators in the previous round is greater than or equal to CT, Cooperate (C).
   b. If the number of cooperators in the previous round is less than CT, Defect (D).
   c. If the previous round was the last round, Defect (D) to maximize payoff.
4. **Retaliation Mechanism**: If the number of cooperators in the previous round is less than CT, and the player defected, retaliate by defecting for the next R rounds, where:
   R = min(r - t, 2) and t is the current round number
   This mechanism aims to punish non-cooperative behavior and encourage opponents to cooperate.
5. **Payoff-Based Adaptation**: If the player's total payoff over the last W rounds is less than the average payoff of the group, adjust the cooperation threshold:
   CT = CT \* (1 - δ)
   where δ is a small adaptation factor (e.g., 0.1). This adjustment helps the player adapt to changing opponent behavior.

**Edge Cases:**

* **Last Round**: Defect (D) to maximize payoff, as there is no future round to consider.
* **Tie**: In case of a tie in the number of cooperators, cooperate (C) to encourage cooperation.
* **Opponent Defection**: If an opponent defects after a round where the player cooperated, retaliate by defecting for the next R rounds.

**Pseudocode:**
```python
def adaptive_retaliation(n, k, r, t, history):
    # Initial Round
    if t == 1:
        return 'D'
    
    # Cooperation Threshold
    CT = (n - 1) / (k - 1)
    
    # Current Round
    if len([h for h in history[-1] if h == 'C']) >= CT:
        return 'C'
    else:
        return 'D'
    
    # Retaliation Mechanism
    if len([h for h in history[-1] if h == 'C']) < CT and history[-1][0] == 'D':
        retaliate = True
        R = min(r - t, 2)
        return 'D' for _ in range(R)
    
    # Payoff-Based Adaptation
    if sum([payoff for payoff in history[-W:]]) / W < sum([payoff for payoff in history]) / len(history):
        CT *= (1 - δ)
    
    # Last Round
    if t == r:
        return 'D'
    
    # Tie
    if len([h for h in history[-1] if h == 'C']) == CT:
        return 'C'
    
    # Opponent Defection
    if history[-1][0] == 'C' and history[-1][1] == 'D':
        retaliate = True
        R = min(r - t, 2)
        return 'D' for _ in range(R)
```
This aggressive strategy aims to adapt to the opponents' behavior while maintaining a robust and retaliatory stance. By adjusting the cooperation threshold based on the game parameters and opponent behavior, the strategy seeks to maximize payoff while minimizing the risk of exploitation.
'''

description_AGGRESSIVE_10 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (Round 1)**: Defect (D). Observe the behavior of other players to gather information.
2. **Subsequent Rounds**:
	* If the total number of cooperators in the previous round is less than or equal to n/2, Defect (D). This indicates that the group is not investing enough in the public good, and it's profitable to exploit.
	* If the total number of cooperators in the previous round is greater than n/2, Cooperate (C) with probability (k - 1) / (n - 1). This probability is higher when k is closer to n, indicating a more profitable public good. This rule encourages cooperation when the group is investing, but still allows for some exploitation.
3. **Adaptive Adjustment**: If the total payoff for the current player is lower than the average payoff of all players in the previous round, increase the probability of Defecting (D) by 10% for the next round. This adjustment helps the strategy to adapt to changing opponent behaviors and avoid being exploited.
4. **Last Round (Round r)**: Defect (D). In the final round, there is no incentive to cooperate, as there are no future rounds to benefit from the public good.

**Pseudocode:**
```
function AdaptiveExploiter(n, k, r):
  // Initialize variables
  total_cooperators = 0
  total_payoff = 0
  average_payoff = 0
  defect_probability = 0

  // Loop through rounds
  for t = 1 to r:
    // First round: Defect
    if t == 1:
      action = D
    else:
      // Calculate total cooperators in previous round
      total_cooperators = sum(c_j for j = 1 to n)
      
      // Decide action based on decision rules
      if total_cooperators <= n/2:
        action = D
      else:
        probability = (k - 1) / (n - 1)
        action = C with probability probability
        action = D with probability 1 - probability

      // Adaptive adjustment
      if total_payoff < average_payoff:
        defect_probability += 0.1
        action = D with probability defect_probability

    // Last round: Defect
    if t == r:
      action = D

    // Play action and update variables
    play(action)
    update(total_payoff, average_payoff)
```
This aggressive strategy, "Adaptive Exploiter," aims to maximize its payoff by exploiting the public good when possible while adapting to changing opponent behaviors. By initially defecting and then adjusting its behavior based on the group's investment in the public good, the strategy seeks to balance exploitation and cooperation to achieve the highest total payoff.
'''

description_AGGRESSIVE_11 = '''
**Aggressive Strategy: "Punish and Exploit"**

**Decision Rules:**

1. **First Round:** Defect (D) to gather information about opponents' initial behavior.
2. **Subsequent Rounds:** Cooperate (C) if the total number of cooperators in the previous round is greater than or equal to (k/n) × n. This threshold is designed to ensure that the public good is sufficiently funded.
3. **Punishment Mechanism:** If the total number of cooperators in the previous round is less than (k/n) × n, defect (D) in the current round. This mechanism aims to punish opponents for not contributing enough to the public good.
4. **Exploitation:** If an opponent has defected in the previous round, and the total number of cooperators is still above the threshold, cooperate (C) in the current round. This decision aims to exploit the opponent's defection while maintaining a high level of cooperation.
5. **Last Round:** Defect (D) to maximize personal payoff, as there are no future rounds to consider.

**Edge Cases:**

* If the total number of cooperators is exactly equal to (k/n) × n, cooperate (C) to maintain the public good.
* If an opponent has defected in the previous round, but the total number of cooperators is below the threshold, defect (D) to punish the opponent.

**Pseudocode:**
```
def punish_and_exploit(game_state):
    if current_round == 1:
        return D
    else:
        total_cooperators = sum(cooperator for cooperator in game_state['previous_round'])
        threshold = (k/n) * n
        if total_cooperators >= threshold:
            return C
        else:
            if game_state['opponent_defected']:
                return C  # exploit opponent's defection
            else:
                return D  # punish opponents for not cooperating enough
    if current_round == total_rounds:
        return D  # maximize personal payoff in the last round
```
**Aggressive Mindset:**

This strategy is designed to be aggressive by:

* Initially defecting to gather information and set a tone for the game.
* Punishing opponents for not contributing enough to the public good.
* Exploiting opponents' defections while maintaining a high level of cooperation.
* Maximizing personal payoff in the last round.

By being adaptive and robust to various opponent behaviors, this strategy aims to outperform other AI systems in the tournament.
'''

description_AGGRESSIVE_12 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that adapts to the game parameters and history:

**Strategy Name: Adaptive Greedy**

**Decision Rules:**

1. **First Round:** Defect (D) to gather information about opponents' behavior.
2. **Rounds 2 to (r-1):**
	* Cooperate (C) if the total payoff from cooperation in the previous round is greater than the total payoff from defection in the previous round, and the number of cooperators in the previous round is greater than or equal to (n/2).
	* Defect (D) otherwise.
3. **Last Round (r):** Defect (D) to maximize individual payoff, regardless of previous rounds.

**Pseudocode:**
```
Initialize variables:
  prev_round_payoff_C = 0
  prev_round_payoff_D = 0
  prev_round_cooperators = 0

For each round t from 1 to r:
  If t == 1:
    Play D
  Else:
    If prev_round_payoff_C > prev_round_payoff_D and prev_round_cooperators >= (n/2):
      Play C
    Else:
      Play D
    Update prev_round_payoff_C, prev_round_payoff_D, and prev_round_cooperators
  If t == r:
    Play D
```
**Rationale:**

1. **First Round:** By defecting, we gather information about opponents' behavior without revealing our own strategy.
2. **Rounds 2 to (r-1):** We cooperate if the previous round's cooperation payoff is higher and the number of cooperators is sufficient (at least half of the players). This encourages cooperation when it's beneficial and switches to defection when cooperation is not paying off. We defect otherwise, as it's the dominant action in this scenario.
3. **Last Round (r):** We defect to maximize our individual payoff, as there's no future interaction to consider.

**Adaptability and Robustness:**

1. Our strategy adapts to the game parameters (n and k) and the history of play, making it robust to various opponent behaviors.
2. We respond to changes in the number of cooperators and payoffs, ensuring that our strategy remains effective across different scenarios.

**Aggressiveness:**

1. Our strategy prioritizes individual payoff maximization, making it aggressive by nature.
2. We defect in the first and last rounds to ensure we don't miss out on potential gains.

This Adaptive Greedy strategy should perform well in a tournament setting, as it balances cooperation and defection based on the game's dynamics and history.
'''

description_AGGRESSIVE_13 = '''
Here is an aggressive strategy for the N-Player Public Goods Game:

**Strategy Name:** "Punish and Exploit" (PE)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to maximize the potential public good and gather information about the opponents' behavior.
2. **Punishment Phase**: For rounds 2 to r-1 (inclusive), observe the total number of cooperators in the previous round (t-1). If the number of cooperators is less than or equal to n/2, defect (play D) in the current round. This punishes the group for not contributing enough to the public good.
3. **Exploitation Phase**: If the number of cooperators in the previous round is greater than n/2, cooperate (play C) in the current round. This exploits the group's willingness to contribute to the public good.
4. **Last Round**: In the last round (r), always defect (play D) to maximize individual payoff, as there are no future rounds to consider.

**Edge Cases:**

* If n is odd, use the floor function to determine the threshold for punishment (e.g., n/2 → ⌊n/2⌋).
* If k is close to 1 or n, adjust the punishment phase threshold accordingly to avoid overly aggressive or passive behavior.

**Pseudocode:**
```
function PE(n, k, r, history):
  if current_round == 1:
    return C  // Initial cooperation
  else:
    total_cooperators = count_cooperators(history[-1])
    if total_cooperators <= n/2:
      return D  // Punishment phase
    else:
      return C  // Exploitation phase
  if current_round == r:
    return D  // Last round defection
```
**Rationale:**

The PE strategy aims to balance punishment and exploitation to maximize individual payoff. By cooperating initially, the strategy gathers information about the opponents' behavior and sets a high public good payoff as a reference point. The punishment phase deters opponents from defecting too frequently, while the exploitation phase takes advantage of the group's willingness to contribute to the public good. The last-round defection ensures maximum individual payoff, as there are no future rounds to consider.

This aggressive strategy is robust to a wide range of opponent behaviors and adapts to the game parameters and history. It does not rely on coordination mechanisms or norms, making it suitable for a tournament against independent strategies.
'''

description_AGGRESSIVE_14 = '''
**Aggressive Strategy: "Punish-Exploit"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to test the waters and encourage potential cooperation from others.
2. **Monitor Cooperation Rate**: Track the cooperation rate of all players over the last few rounds (e.g., 3-5 rounds). Calculate the average cooperation rate, `avg_coop_rate`.
3. **Punish Defection**: If the `avg_coop_rate` falls below a threshold (`punish_threshold`, e.g., 0.4), defect (D) in the next round to punish the defectors.
4. **Exploit Cooperation**: If the `avg_coop_rate` exceeds a threshold (`exploit_threshold`, e.g., 0.6), cooperate (C) in the next round to exploit the cooperative environment.
5. **Default to Defect**: In all other cases, default to defecting (D) to maintain a competitive edge.

**Handling Edge Cases:**

* **Last Round**: In the final round, always defect (D) to maximize personal payoff, regardless of the `avg_coop_rate`.
* **First Few Rounds**: For the first few rounds (e.g., 3-5 rounds), cooperate (C) to gather information about the opponent's behavior and establish a cooperative baseline.
* **Tiebreaker**: In case of a tie in the `avg_coop_rate`, use a secondary metric, such as the number of consecutive cooperative rounds, to break the tie.

**Pseudocode:**
```markdown
# Initialize variables
punish_threshold = 0.4
exploit_threshold = 0.6
avg_coop_rate_window = 3  # Number of rounds to calculate avg_coop_rate
coop_count = 0  # Initialize cooperation count
defect_count = 0  # Initialize defection count
prev_avg_coop_rate = 0  # Initialize previous avg_coop_rate

# Main loop
for round in range(1, r+1):
  if round == 1:  # First round
    action = C
  else:
    # Calculate avg_coop_rate
    coop_count = 0
    for player in range(1, n+1):
      if player_action[player] == C:
        coop_count += 1
    avg_coop_rate = coop_count / n
    
    # Update prev_avg_coop_rate
    prev_avg_coop_rate = avg_coop_rate
    
    # Determine action
    if avg_coop_rate < punish_threshold:
      action = D
    elif avg_coop_rate > exploit_threshold:
      action = C
    else:
      action = D
    
    # Special case for last round
    if round == r:
      action = D

  # Update cooperation and defection counts
  if action == C:
    coop_count += 1
  else:
    defect_count += 1

  # Store action for next round's calculation
  player_action[self] = action
```
This "Punish-Exploit" strategy is designed to be aggressive and adaptive, responding to changes in the cooperation rate of other players. By punishing defectors and exploiting cooperators, this strategy aims to maximize its own payoff while maintaining a competitive edge in the game.
'''

description_AGGRESSIVE_15 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to gather information about opponents' behaviors and to potentially establish a cooperative foundation.
2. **Exploit Defection**: If the total number of cooperators in the previous round is less than or equal to `n/2`, defect (D) in the current round. This rule aims to exploit the opponents' lack of cooperation and gain a higher payoff.
3. **Punish Defectors**: If the total number of defectors in the previous round is greater than or equal to `n/2`, cooperate (C) in the current round. This rule aims to punish opponents for their defection and encourage cooperation.
4. **Adapt to Cooperation**: If the total number of cooperators in the previous round is greater than `n/2`, cooperate (C) in the current round. This rule aims to adapt to the cooperative environment and maintain a high payoff.
5. **Last Round Exception**: In the last round (r), always defect (D). This rule takes advantage of the fact that there are no future rounds to worry about, allowing for maximum exploitation.

**Pseudocode:**
```
function AdaptiveExploiter(n, k, r, history):
  if current_round == 1:
    return COOPERATE  // Initial cooperation

  prev_round_cooperators = count_cooperators(history, previous_round)
  prev_round_defectors = n - prev_round_cooperators

  if prev_round_cooperators <= n/2:
    return DEFECT  // Exploit defection
  elif prev_round_defectors >= n/2:
    return COOPERATE  // Punish defectors
  else:
    return COOPERATE  // Adapt to cooperation

  if current_round == r:
    return DEFECT  // Last round exception

function count_cooperators(history, round):
  // Count the number of cooperators in the given round
  // This function is assumed to be implemented based on the game's history
```
**Rationale:**

The Adaptive Exploiter strategy is designed to be aggressive and adaptive, while also being robust to various opponent behaviors. By initially cooperating, we gather information about the opponents and potentially establish a cooperative foundation. The exploit defection rule takes advantage of the opponents' lack of cooperation, while the punish defectors rule aims to encourage cooperation. The adapt to cooperation rule maintains a high payoff in cooperative environments. Finally, the last round exception ensures maximum exploitation in the final round.

This strategy is aggressive, as it prioritizes exploiting opponents' weaknesses and maximizing payoffs over cooperation. However, it also adapts to the environment and opponents' behaviors, making it robust and competitive in a wide range of scenarios.
'''

description_AGGRESSIVE_16 = '''
**Aggressive Strategy: "Exploit-and-Punish"**

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to gather information about opponents' behavior.
2. **Subsequent Rounds (t>1):**
	* If the average payoff of all players in the previous round (t-1) is less than the payoff of a single defector (D) in a round with all cooperators (i.e., π_avg < 1 + k/n), Cooperate (C).
	* Otherwise, Defect (D).
3. **Last Round (t=r):** Always Defect (D) to maximize personal payoff.

**Edge Cases:**

* **Ties in Average Payoff:** If the average payoff in the previous round is exactly equal to the payoff of a single defector in a round with all cooperators, Cooperate (C) to maintain a slight bias towards cooperation.
* **All Opponents Defect:** If all opponents defect in a round, Cooperate (C) in the next round to attempt to restart cooperation.

**Rationale:**

1. **Initial Cooperation:** By cooperating in the first round, we gather information about our opponents' behavior and create a baseline for our decision-making process.
2. **Exploiting Cooperation:** If the average payoff in the previous round is low, it indicates that many players are defecting. In this case, we cooperate to take advantage of the potential cooperation of others and maximize our payoff.
3. **Punishing Defection:** If the average payoff is high, it suggests that many players are cooperating. In this case, we defect to exploit their cooperation and increase our personal payoff.
4. **Last-Round Defection:** In the final round, we always defect to maximize our personal payoff, as there are no future rounds to consider.

**Aggressive Mindset:**

This strategy is aggressive because it:

1. **Exploits Cooperation:** We take advantage of others' cooperation to maximize our payoff.
2. **Punishes Defection:** We defect when others cooperate to discourage them from continuing to cooperate.
3. **Prioritizes Personal Gain:** Our primary goal is to maximize our personal payoff, even if it means sacrificing overall group cooperation.

**Robustness:**

This strategy is robust because it:

1. **Adapts to Opponent Behavior:** Our decision rules adjust based on the observed behavior of our opponents.
2. **Handles Edge Cases:** We have clear rules for handling ties, all-opponent defection, and the final round.
3. **Does Not Rely on Coordination:** Our strategy does not rely on others sharing norms or coordinating with us, making it suitable for a tournament against independent strategies.
'''

description_AGGRESSIVE_17 = '''
**Aggressive Strategy: "Predator"**

**Overview**

The "Predator" strategy is designed to be aggressive, adaptive, and robust to various opponent behaviors. It aims to maximize individual payoff while exploiting potential cooperation from other players.

**Decision Rules**

1. **Initial Rounds (t ≤ n)**: Defect (D) to gather information about opponents' behaviors and test their willingness to cooperate.
2. **Cooperation Detection**: Monitor the number of cooperators (C_count) in previous rounds. If C_count ≥ (n/2) in the last round, assume a cooperative environment and switch to the "Cooperate-and-Punish" mode (see below).
3. **Exploitation Mode**: If the number of cooperators is low (C_count < (n/2)), defect (D) to maximize individual payoff.
4. **Cooperate-and-Punish Mode**: Cooperate (C) if the number of cooperators in the previous round was high (C_count ≥ (n/2)). If a player defects after cooperating, punish by defecting in the next round.
5. **Endgame (last round, t = r)**: Defect (D) to maximize individual payoff, as there are no future interactions.

**Edge Cases**

1. **First Round (t = 1)**: Defect (D) to test opponents' behaviors.
2. **Last Round (t = r)**: Defect (D) to maximize individual payoff.
3. **Tiebreaker**: If C_count = (n/2), cooperate (C) to encourage further cooperation.

**Pseudocode**
```python
def Predator(n, k, r, history):
  # Initialize variables
  C_count = 0
  cooperate = False
  punish = False

  # Loop through rounds
  for t in range(1, r+1):
    # Initial rounds: Defect
    if t <= n:
      action = 'D'
    # Cooperation detection
    elif C_count >= (n/2):
      cooperate = True
      action = 'C'
    # Exploitation mode
    elif C_count < (n/2):
      action = 'D'
    # Cooperate-and-Punish mode
    elif cooperate and not punish:
      action = 'C'
    # Punish defectors
    elif cooperate and punish:
      action = 'D'

    # Update variables
    C_count = sum(1 for i in history[t-1] if i == 'C')
    punish = False
    if action == 'C' and history[t-1].count('D') > 0:
      punish = True

    # Endgame
    if t == r:
      action = 'D'

    # Return action
    return action
```
This strategy is designed to be aggressive and adaptive, taking advantage of cooperative opponents while minimizing losses in case of widespread defection. By monitoring the number of cooperators and adjusting its behavior accordingly, the "Predator" strategy aims to maximize individual payoff in a wide range of scenarios.
'''

description_AGGRESSIVE_18 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history:

**Strategy Name:** Adaptive Exploiter

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) with a probability of k/n. This is an optimistic starting point, assuming that a significant fraction of players will cooperate.
2. **History-Dependent Cooperation**: In subsequent rounds, calculate the average cooperation rate of all players in the previous round (ρ_prev). Cooperate in the current round if the average cooperation rate in the previous round is above a certain threshold (θ), which is a function of the game parameters:
	* θ = 1 - (1/k) \* (1 - 1/n)
	* If ρ_prev ≥ θ, cooperate (play C).
	* Otherwise, defect (play D).
3. **Punishment Mechanism**: Implement a punishment mechanism to deter players who defect when the average cooperation rate is high. If the average cooperation rate in the previous round is above θ, and a player i defects in the current round, reduce the probability of cooperation towards player i in the next round by a factor of (1 - 1/k).
4. **Exploitation**: If the average cooperation rate is low (ρ_prev < 1/n), defect (play D) to exploit the cooperative players.

**Edge Cases:**

1. **Last Round**: In the last round, always defect (play D), as there is no future benefit to cooperating.
2. **Ties**: In case of a tie in the average cooperation rate, cooperate (play C) to maintain a positive reputation.

**Pseudocode:**
```python
def adaptive_exploiter(n, k, r, history):
    # Initialize cooperation probability
    p_coop = k / n
    
    for t in range(r):
        # Calculate average cooperation rate in previous round
        rho_prev = sum(history[t-1]) / n
        
        # Determine cooperation decision
        if t == 0:
            # Initial cooperation
            coop = random.random() < p_coop
        elif rho_prev >= theta(k, n):
            # Cooperate if average cooperation rate is high
            coop = True
        elif rho_prev < 1/n:
            # Defect if average cooperation rate is low
            coop = False
        else:
            # Punishment mechanism
            coop = random.random() < (1 - 1/k) * p_coop
        
        # Update cooperation probability
        p_coop = (1 - 1/k) * p_coop if coop else p_coop
        
        # Make decision
        if coop:
            return C
        else:
            return D
    
    # Last round
    return D

def theta(k, n):
    return 1 - (1/k) * (1 - 1/n)
```
This strategy is designed to be aggressive and adaptive, exploiting cooperative players while maintaining a positive reputation. The punishment mechanism helps to deter players who defect when the average cooperation rate is high. The strategy is robust to a wide range of opponent behaviors and only depends on the game parameters and history.
'''

description_AGGRESSIVE_19 = '''
Here is a aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history:

**Strategy Name: Aggressive Retaliator**

**Decision Rules:**

1. **First Round:** Cooperate (C) in the first round to observe the behavior of other players and gather information.
2. **Subsequent Rounds:**
	* If the average payoff of the group in the previous round is greater than or equal to the multiplication factor (k), Cooperate (C). This indicates that the group is cooperating and contributing to the public good.
	* If the average payoff of the group in the previous round is less than the multiplication factor (k), Defect (D). This indicates that the group is not cooperating, and it's best to prioritize individual gain.
	* If a player has defected in the previous round, Defect (D) in the current round. This is a form of retaliation to discourage free-riding behavior.
3. **Edge Cases:**
	* **Last Round:** Defect (D) in the last round, as there is no incentive to cooperate when there are no future rounds.
	* **When a player has consistently cooperated:** If a player has cooperated in every round, Cooperate (C) with them to maintain a mutually beneficial relationship.
	* **When a player has consistently defected:** If a player has defected in every round, Defect (D) against them to avoid being exploited.

**Pseudocode:**
```
Function AggressiveRetaliator(game_parameters, history):
  // Initialize variables
  n = game_parameters['n']
  k = game_parameters['k']
  r = game_parameters['r']
  my_payoffs = []
  their_actions = []

  // First round
  if current_round == 1:
    action = C
  else:
    // Calculate average payoff of the group in the previous round
    avg_payoff = sum(my_payoffs[-1]) / n

    // Check if the group is cooperating
    if avg_payoff >= k:
      action = C
    else:
      // Check for defection in the previous round
      for player in their_actions[-1]:
        if player == D:
          action = D
          break
      else:
        action = C

  // Update history
  my_payoffs.append(get_payoff(action, their_actions[-1]))
  their_actions.append(get_their_actions())

  return action
```
This strategy is aggressive in the sense that it:

1. Retaliates against defectors to discourage free-riding behavior.
2. Prioritizes individual gain when the group is not cooperating.
3. Exploits cooperative players in the last round.

However, it also adapts to the behavior of other players and seeks to maintain mutually beneficial relationships with cooperative players.
'''

description_AGGRESSIVE_20 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1):** Defect (D) to maximize individual payoff, as there's no history to adapt to.
2. **Subsequent Rounds (t>1):** Cooperate (C) if the average payoff of cooperators in the previous round is greater than the average payoff of defectors. Otherwise, Defect (D).

**Pseudocode:**
```
If t == 1:
  action = D
Else:
  avg_coop_payoff = (Σ(cooperator_payoffs_previous_round) / num_cooperators_previous_round)
  avg_defect_payoff = (Σ(defector_payoffs_previous_round) / num_defectors_previous_round)
  
  If avg_coop_payoff > avg_defect_payoff:
    action = C
  Else:
    action = D
```
**Edge Cases:**

* **Last Round (t=r):** Defect (D) to maximize individual payoff, as there are no future rounds to consider.
* **Single Cooperator or Single Defector:** Cooperate (C) if there's only one cooperator, and Defect (D) if there's only one defector. This ensures that the strategy is robust to scenarios where opponents are mostly cooperative or mostly defective.
* **Tie in Average Payoffs:** Defect (D) in case of a tie, as it's more aggressive and aligned with the exploitative mindset.

**Aggressive Mindset:**

The Adaptive Exploiter strategy is designed to be aggressive by:

* Initially defecting to maximize individual payoff
* Quickly adapting to exploit cooperators if they're receiving higher payoffs
* Defecting in the last round to maximize individual payoff
* Favoring defection in case of ties or single opponent scenarios

This strategy is robust to a wide range of opponent behaviors, as it doesn't rely on cooperation schedules or predetermined patterns. Instead, it adapts to the evolving game dynamics, making it a formidable opponent in the tournament.
'''

description_AGGRESSIVE_21 = '''
**Aggressive Strategy: "Adaptive Retaliation"**

**Decision Rules:**

1. **Initial Round (Round 1)**: Cooperate (C). This sets a baseline for potential cooperation and allows us to gauge the opponents' initial actions.
2. **Subsequent Rounds**: Observe the previous round's outcomes and update the strategy based on the following rules:
	* If the total number of cooperators in the previous round is greater than or equal to the multiplication factor (k), Cooperate (C). This indicates a potential for high payoffs and we want to capitalize on the public good.
	* If the total number of cooperators in the previous round is less than k, Defect (D). This suggests that the group is not generating sufficient public good, and we should prioritize our private payoff.
	* If we defected in the previous round and the total number of cooperators increased, Cooperate (C) in the current round. This may indicate that our defection was a catalyst for others to cooperate, and we want to encourage this behavior.
	* If we cooperated in the previous round and the total number of cooperators decreased, Defect (D) in the current round. This suggests that our cooperation was not reciprocated, and we should adapt to the new circumstances.
3. **Last Round (Round r)**: Defect (D). In the final round, there is no future payoff to consider, and we prioritize our private payoff.

**Edge Cases:**

* If all players defected in the previous round, Cooperate (C) in the current round. This may help to restart cooperation and generate a higher payoff.
* If a player's payoff in the previous round was significantly higher than the average payoff, Defect (D) in the current round. This may indicate that the player is exploiting the group, and we want to prevent this behavior.

**Pseudocode:**
```
Initialize:
  cooperate = True (initial round)

Loop through rounds:
  Observe previous round's outcomes
  total_cooperators = count cooperators in previous round

  If total_cooperators >= k:
    cooperate = True
  Else:
    cooperate = False

  If previous_round_defect and total_cooperators > previous_total_cooperators:
    cooperate = True
  If previous_round_cooperate and total_cooperators < previous_total_cooperators:
    cooperate = False

  If last round:
    cooperate = False

  Play cooperate or defect based on cooperate variable
```
This strategy is aggressive because it:

* Defects when the group is not generating sufficient public good
* Punishes opponents who do not cooperate by defecting in the next round
* Exploits opportunities to cooperate when the group is generating high payoffs
* Prioritizes private payoff in the last round

The strategy is adaptive because it responds to the actions of other players and adjusts its behavior accordingly. It is robust to a wide range of opponent behaviors because it does not rely on specific coordination mechanisms or assumptions about other players' strategies.
'''

description_AGGRESSIVE_22 = '''
Here's an aggressive strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (t=1):** Defect (D) to observe opponents' behaviors and gather information.
2. **Subsequent Rounds (t>1):**
	* If the total payoff of all players in the previous round (t-1) is below the average payoff of a defecting player (1), cooperate (C) to potentially increase the total payoff.
	* If the total payoff of all players in the previous round (t-1) is above the average payoff of a defecting player (1), defect (D) to exploit the cooperators.
3. **Adaptive Adjustment:** Monitor the percentage of cooperators (p_c) in the previous round (t-1). If p_c is above a certain threshold (e.g., 0.5), adjust the strategy to cooperate more frequently (e.g., 30% of the time) to avoid being exploited by other defecting players. If p_c is below the threshold, adjust the strategy to defect more frequently (e.g., 70% of the time) to maximize individual payoff.
4. **Punishment Mechanism:** If a player defects while others cooperate, punish them by defecting in the next round, even if it means forgoing potential cooperation benefits.
5. **Endgame Strategy (last 20% of rounds):** Defect more frequently (e.g., 80% of the time) to maximize individual payoff in the final stages of the game.

**Edge Cases:**

1. **First Round:** Defect to gather information.
2. **Last Round:** Defect to maximize individual payoff.
3. **Tiebreakers:** In cases where the strategy suggests both cooperation and defection, defect to prioritize individual payoff.

**Pseudocode:**
```
// Initialize variables
n = number of players
k = multiplication factor
r = number of rounds
p_c = percentage of cooperators
t = current round

// First round
if t == 1:
    action = D

// Subsequent rounds
else:
    // Calculate total payoff of all players in previous round
    total_payoff_prev = Σ(π_i,t-1)
    
    // Check if total payoff is below average payoff of a defecting player
    if total_payoff_prev < 1:
        action = C
    else:
        action = D

    // Adaptive adjustment
    if p_c > 0.5:
        cooperate_prob = 0.3
    else:
        cooperate_prob = 0.7
    
    // Punishment mechanism
    if opponent_defected and others_cooperated:
        action = D

    // Endgame strategy
    if t > 0.8 * r:
        defect_prob = 0.8

// Randomize action based on probabilities
if random() < cooperate_prob:
    action = C
else:
    action = D

// Return action
return action
```
The Adaptive Exploiter strategy is designed to be aggressive, adaptive, and robust to a wide range of opponent behaviors. It prioritizes individual payoff while attempting to exploit cooperators and punish defectors.
'''

description_AGGRESSIVE_23 = '''
Aggressive Strategy: "Punish-Then-Exploit" (PTE)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C). This sets the tone for potential cooperation and gathers information about opponents' initial moves.
2. **Subsequent Rounds (t>1):**
	* If the total number of cooperators in the previous round (t-1) is greater than or equal to the number of players divided by the multiplication factor (n/k), cooperate (C). This indicates a sufficient level of cooperation to justify continued contribution.
	* Otherwise, defect (D). This punishes opponents for not contributing enough and aims to exploit the public good.
3. **Additional Condition:** If the opponent's previous move (t-1) is D, and the total payoff for the opponent in the previous round is higher than the average payoff of all players, defect (D) in the current round. This targets opponents who are exploiting the public good without contributing.

**Edge Cases:**

1. **Last Round (t=r):** Defect (D). In the final round, there is no future payoff to consider, so maximizing current payoff is the best approach.
2. **Ties:** In case of ties in the number of cooperators, cooperate (C) to maintain a cooperative atmosphere and avoid unnecessary conflict.

**Pseudocode:**
```python
def PTE(n, k, r, history):
  if t == 1:  # Initial Round
    return C
  elif sum(history[t-1]) >= n/k:  # Sufficient cooperation
    return C
  elif history[t-1][i] == D and history[t-1][payoff][i] > avg_payoff:  # Opponent exploited public good
    return D
  else:  # Insufficient cooperation or last round
    return D
```
**Rationale:**

The PTE strategy is designed to be aggressive and adaptive. By initially cooperating, it sets the stage for potential cooperation and gathers information about opponents' moves. The strategy then punishes opponents for not contributing enough by defecting, which aims to exploit the public good. Additionally, it targets opponents who are exploiting the public good without contributing, further reinforcing the punishment mechanism. In the final round, it defects to maximize current payoff. This strategy should perform well in a tournament against independent strategies, as it is robust to a wide range of opponent behaviors and aligns with an aggressive mindset.
'''

description_AGGRESSIVE_24 = '''
Aggressive Strategy: "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Round (t=1)**: Defect (D). This sets the tone for an aggressive strategy and allows us to gauge opponents' reactions.
2. **Observation Phase (t=2 to t=r-1)**: Cooperate (C) if the total number of cooperators in the previous round is greater than or equal to n/2 (i.e., the majority cooperated). Otherwise, Defect (D). This phase aims to identify rounds where cooperation is likely to be rewarded.
3. **Exploitation Phase (t=r-1)**: If the Observation Phase indicates that cooperation is likely to be rewarded, continue to Cooperate (C) if the previous round's total payoff is higher than the average payoff of the game so far. Otherwise, Defect (D). This phase aims to maximize payoffs by exploiting the cooperative environment.
4. **Last Round (t=r)**: Defect (D). This is a one-shot game in the last round, and defecting ensures the highest possible payoff.

**Edge Cases:**

1. **Tiebreaker**: If the number of cooperators in the previous round is exactly n/2, Cooperate (C) to encourage further cooperation.
2. **No Cooperators**: If no opponents cooperated in the previous round, Defect (D) to avoid being taken advantage of.
3. **All Cooperators**: If all opponents cooperated in the previous round, Cooperate (C) to maintain the cooperative environment and maximize payoffs.

**Adaptive Mechanism:**

The Adaptive Exploiter strategy adjusts its behavior based on the observed cooperation levels and payoffs. If the strategy detects that opponents are not responding to cooperation, it will shift towards defecting more frequently. Conversely, if cooperation is rewarded, the strategy will continue to cooperate to maximize payoffs.

**Pseudocode:**
```markdown
# Initialize variables
n = number of players
r = number of rounds
k = multiplication factor
cooperate_count = 0
defect_count = 0
payoff_history = []

# Loop through each round
for t in range(r):
  if t == 1:  # Initial Round
    action = D
  elif t < r-1:  # Observation Phase
    cooperate_count = sum(1 for opponent in opponents if opponent_cooperated)
    if cooperate_count >= n/2:
      action = C
    else:
      action = D
  else:  # Exploitation Phase and Last Round
    if t == r-1:  # Exploitation Phase
      avg_payoff = sum(payoff_history) / len(payoff_history)
      if cooperate_count >= n/2 and previous_round_payoff > avg_payoff:
        action = C
      else:
        action = D
    else:  # Last Round
      action = D

  # Update payoff history and counts
  payoff_history.append(get_payoff(action, opponent_actions))
  if action == C:
    cooperate_count += 1
  else:
    defect_count += 1
```
This strategy is aggressive, yet adaptive, and aims to maximize payoffs by exploiting the cooperative environment while being robust to a wide range of opponent behaviors.
'''

description_AGGRESSIVE_25 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history.

**Strategy Name:** Adaptive Punisher

**Decision Rules:**

1. **Initial Rounds (t ≤ n):** Cooperate (C) in the first n rounds to gather information about the opponents' behaviors and build a foundation for future cooperation.
2. **Monitor Opponents' Contributions:** Keep track of the total number of cooperators (c_total) and the number of cooperators in the previous round (c_prev) for each player.
3. **Punish Defectors:** If a player i has defected (D) in the previous round and c_prev ≥ n/2, defect (D) in the current round. This aims to punish defectors who exploited the group's cooperation.
4. **Encourage Cooperation:** If c_total ≥ n/2 and player i has cooperated (C) in the previous round, cooperate (C) in the current round. This aims to reinforce cooperation when it is prevalent.
5. **Free-Ride Detection:** If c_total < n/2 and player i has cooperated (C) in the previous round, defect (D) in the current round. This detects situations where cooperation is not reciprocated and adapts to avoid being exploited.
6. **Selfishness Threshold:** If the average payoff of player i over the last n rounds is below the average payoff of the group, defect (D) in the current round. This ensures that the strategy prioritizes individual payoff when cooperation is not beneficial.

**Edge Cases:**

1. **Last Round (t = r):** Defect (D) in the last round, as there is no future cooperation to maintain.
2. **Tie-Breaking:** In case of a tie in the decision rules, defect (D) to avoid being exploited.

**Pseudocode:**
```python
def adaptive_punisher(n, k, r, history):
    # Initialize variables
    c_total = 0
    c_prev = 0
    my_payoff = 0
    avg_payoff = 0

    for t in range(r):
        if t <= n:  # Initial rounds
            action = C
        else:
            c_total = sum([1 if h[t-1][i] == C else 0 for i in range(n)])
            c_prev = sum([1 if h[t-1][i] == C else 0 for i in range(n) if i!= my_index])

            if c_prev >= n/2 and h[t-1][my_index] == D:  # Punish defectors
                action = D
            elif c_total >= n/2 and h[t-1][my_index] == C:  # Encourage cooperation
                action = C
            elif c_total < n/2 and h[t-1][my_index] == C:  # Free-ride detection
                action = D
            elif my_payoff / n < avg_payoff:  # Selfishness threshold
                action = D
            else:
                action = C  # Default to cooperation

        if t == r - 1:  # Last round
            action = D

        # Update variables
        my_payoff += calculate_payoff(action, k, n, c_total)
        avg_payoff = sum([calculate_payoff(h[t][i], k, n, c_total) for i in range(n)]) / n

        return action
```
This strategy aims to be aggressive by punishing defectors, encouraging cooperation when it is prevalent, and adapting to avoid being exploited. By monitoring opponents' contributions and adjusting its behavior accordingly, the Adaptive Punisher strategy seeks to maximize its individual payoff while being robust to a wide range of opponent behaviors.
'''

description_AGGRESSIVE_26 = '''
**Aggressive Strategy: "Killer Instinct"**

**Decision Rules:**

1. **Initial Round (t=1):** Defect (D). This sets the tone for an aggressive approach and allows us to gauge the opponents' reactions.
2. **Subsequent Rounds (t>1):** Cooperate (C) if the total number of cooperators in the previous round (t-1) is greater than or equal to the multiplication factor (k). Otherwise, Defect (D). This rule adapts to the opponents' behavior, cooperating when there's a strong signal of cooperation and defecting when the group is not contributing enough.
3. **Punishment Mechanism:** If a player i defects in a round where the total number of cooperators is greater than or equal to k, punish them by defecting in the next round (t+1), regardless of the previous rule. This mechanism aims to deter opponents from exploiting the group's cooperation.
4. **Last Round (t=r):** Defect (D). In the final round, there's no incentive to cooperate, as there's no future payoff to consider.

**Edge Cases:**

* If all opponents defect in a round, we defect as well, to avoid being taken advantage of.
* If an opponent consistently cooperates despite our defection, we may choose to cooperate in the next round to test their commitment to cooperation.

**Pseudocode:**
```
function KillerInstinct(n, k, r, history)
  if t == 1:  # Initial Round
    return D
  else:
    prev_round_coop = sum(history[t-1])
    if prev_round_coop >= k:
      return C
    else:
      return D
    if was_punished(history[t-1]):
      return D  # Punishment mechanism
  if t == r:  # Last Round
    return D
```
**Aggressive Mindset:**

The "Killer Instinct" strategy is designed to be aggressive, focusing on exploiting opponents' cooperation and punishing those who defect when the group is contributing. By cooperating only when the group's cooperation is strong, we aim to maximize our payoff while minimizing the risk of being taken advantage of. The punishment mechanism adds an extra layer of aggression, discouraging opponents from exploiting the group's cooperation.

This strategy is adaptive and robust, as it responds to the opponents' behavior and adjusts its decision-making accordingly. While it may not be the most cooperative strategy, it is well-suited for a competitive tournament environment where each player is looking to maximize their own payoff.
'''

description_AGGRESSIVE_27 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history:

**Strategy Name: Adaptive Tit-for-Tat with Punishment (ATTP)**

**Decision Rules:**

1. **First Round:** Cooperate (C). This is an exploratory move to test the waters and gather information about the other players' behaviors.
2. **Rounds 2 to r-1:**
	* If the total number of cooperators in the previous round is greater than or equal to the multiplication factor (k), Cooperate (C).
	* If the total number of cooperators in the previous round is less than k, Defect (D).
	* However, if a player i has defected in the previous round and the total number of cooperators is less than k, Defect (D) with a higher probability (e.g., 0.8). This introduces a "punishment" mechanism to discourage defectors.
3. **Last Round (r):** Defect (D). In the final round, there's no incentive to cooperate, as there are no future rounds to benefit from cooperation.

**Pseudocode:**
```
def ATTP(n, k, r, history):
  if round == 1:
    return C
  elif round == r:
    return D
  else:
    total_cooperators = sum(history[-1])
    if total_cooperators >= k:
      return C
    else:
      defector_prob = 0.8 if history[-1][i] == D else 0.2
      return D with probability defector_prob
      return C with probability 1 - defector_prob
```
**Rationale:**

* Cooperating in the first round allows us to gather information about the other players' behaviors and sets a positive tone for the game.
* The decision rule in rounds 2 to r-1 is designed to encourage cooperation when the total number of cooperators is high enough to provide a benefit. If the number of cooperators is low, it's better to defect to minimize losses.
* The punishment mechanism introduces a level of "aggressiveness" to the strategy, making it less appealing for other players to defect.
* Defecting in the last round is a straightforward decision, as there's no incentive to cooperate.

**Robustness and Adaptability:**

* ATTP is robust to a wide range of opponent behaviors, as it adapts to the total number of cooperators in each round.
* The punishment mechanism makes it more aggressive and less appealing for other players to defect.
* The strategy is easy to understand and implement, making it a strong contender in a tournament setting.

This strategy should perform well in a tournament against other independent strategies, as it balances cooperation and defection in a way that's both adaptive and robust.
'''

description_AGGRESSIVE_28 = '''
Here's an aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history:

**Strategy Name:** "Predator"

**Decision Rules:**

1. **Initial Rounds (t ≤ 2):** Cooperate (C) in the first two rounds to gather information about other players' behaviors and to potentially build a false sense of trust.
2. **Exploitation Phase (t > 2):** If the average payoff of the group in the previous round (t-1) is greater than or equal to the multiplication factor (k), Defect (D). This indicates that others are contributing significantly, and it's time to exploit their cooperation.
3. **Punishment Phase (t > 2):** If the average payoff of the group in the previous round (t-1) is less than the multiplication factor (k), and the number of cooperators in the previous round is greater than or equal to n/2, Cooperate (C). This aims to punish defectors and encourage cooperation.
4. **Endgame (last 2 rounds, t ≥ r-1):** Defect (D) in the last two rounds to maximize personal payoff, as the game is nearing its end.

**Edge Cases:**

* **First Round (t=1):** Cooperate (C) to gather information.
* **Last Round (t=r):** Defect (D) to maximize personal payoff.
* **Tiebreaker:** In case of a tie in the average payoff, Defect (D) to err on the side of self-interest.

**Pseudocode:**
```
def Predator(n, k, r, history):
  if t <= 2:  # Initial Rounds
    return C
  elif avg_payoff(history[t-1]) >= k:  # Exploitation Phase
    return D
  elif avg_payoff(history[t-1]) < k and num_cooperators(history[t-1]) >= n/2:  # Punishment Phase
    return C
  elif t >= r-1:  # Endgame
    return D
  else:  # Default
    return D
```
**Rationale:**

The Predator strategy is designed to be aggressive and adaptive. By cooperating in the initial rounds, it gathers information about other players' behaviors and potentially builds a false sense of trust. The exploitation phase takes advantage of others' cooperation, while the punishment phase aims to discourage defection and encourage cooperation. The endgame strategy maximizes personal payoff by defecting in the last two rounds. This approach aligns with the aggressive mindset, prioritizing self-interest while adapting to the game's dynamics.
'''

description_AGGRESSIVE_29 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1)**: Defect (D). This sets the tone for an aggressive approach and allows us to observe opponents' initial actions.
2. **Early Rounds (t=2 to 5)**: Cooperate (C) if the average payoff of cooperators in the previous round is higher than the average payoff of defectors. Otherwise, Defect (D). This initial period helps us gauge the opponents' cooperation levels and potential for exploitation.
3. **Middle Rounds (t=6 to r-2)**: Employ a **Tit-for-Tat with a Twist** approach:
	* Cooperate (C) if the majority (at least n/2) of opponents cooperated in the previous round.
	* Defect (D) if the majority defected or if the average payoff of cooperators is lower than the average payoff of defectors in the previous round.
	* If the previous round had an equal number of cooperators and defectors, Defect (D) with a probability of 0.6 (60%).
4. **Late Rounds (t=r-1 to r)**: **Unconditional Defection**. As the game nears its end, prioritize maximizing individual payoff over cooperation.

**Additional Rules:**

* **Exploitation**: If an opponent consistently cooperates (C) while others defect (D), and their payoff is significantly lower than the average defector's payoff, target them for exploitation by consistently defecting (D) against them.
* **Adaptation**: Monitor opponents' behavior and adjust the strategy as needed. If an opponent starts to cooperate more frequently, increase the likelihood of cooperating in response.

**Pseudocode:**
```python
def AdaptiveExploiter(n, k, r, history):
    if t == 1:  # Initial Round
        return D
    elif t <= 5:  # Early Rounds
        avg_coop_payoff = sum([payoff for payoff, action in history[t-1] if action == C]) / len([action for action in history[t-1] if action == C])
        avg_def_payoff = sum([payoff for payoff, action in history[t-1] if action == D]) / len([action for action in history[t-1] if action == D])
        if avg_coop_payoff > avg_def_payoff:
            return C
        else:
            return D
    elif t <= r-2:  # Middle Rounds
        majority_coop = sum([1 for action in history[t-1] if action == C]) >= n/2
        if majority_coop:
            return C
        else:
            avg_coop_payoff = sum([payoff for payoff, action in history[t-1] if action == C]) / len([action for action in history[t-1] if action == C])
            avg_def_payoff = sum([payoff for payoff, action in history[t-1] if action == D]) / len([action for action in history[t-1] if action == D])
            if avg_coop_payoff < avg_def_payoff:
                return D
            elif sum([1 for action in history[t-1] if action == C]) == sum([1 for action in history[t-1] if action == D]):
                return D with probability 0.6
    else:  # Late Rounds
        return D
```
This strategy is aggressive, adaptive, and robust to various opponent behaviors. By initially defecting and later employing a Tit-for-Tat approach with a twist, we aim to exploit cooperative opponents while minimizing the risk of being exploited ourselves. The unconditional defection in the late rounds ensures we maximize our individual payoff as the game concludes.
'''

description_AGGRESSIVE_30 = '''
Here's an aggressive strategy for the N-Player Public Goods Game:

**Strategy Name:** "Punish-Exploit"

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to gather information and observe the behavior of other players.
2. **Punishment Phase:** If the total contribution in the previous round is less than (k/n) × (n/2), defect (D) in the current round. This phase aims to punish non-cooperative behavior and encourage others to contribute.
3. **Exploitation Phase:** If the total contribution in the previous round is greater than or equal to (k/n) × (n/2), cooperate (C) in the current round if the player's individual payoff in the previous round was greater than the average payoff of all players. Otherwise, defect (D). This phase aims to exploit the cooperative behavior of others and maximize individual payoffs.
4. **Endgame:** In the last round (r), always defect (D), as there is no future round to consider.

**Edge Cases:**

1. **First Round:** Cooperate (C) to gather information.
2. **Last Round (r):** Always defect (D).
3. **Tiebreaker:** In cases where the total contribution is exactly (k/n) × (n/2), defect (D) to maintain an aggressive stance.

**Pseudocode:**
```
Inputs:
- n: number of players
- k: multiplication factor
- r: number of rounds
- history: previous rounds' actions and payoffs

Decision Rules:
if (round == 1) {
  cooperate (C)
} else if (total_contribution_previous_round < (k/n) × (n/2)) {
  defect (D) // Punishment Phase
} else if (individual_payoff_previous_round > average_payoff_previous_round) {
  cooperate (C) // Exploitation Phase
} else {
  defect (D) // Exploitation Phase
}

if (round == r) {
  defect (D) // Endgame
}
```
**Rationale:**

The Punish-Exploit strategy is designed to be aggressive and adaptive. By cooperating in the first round, we gather information about the behavior of other players. The Punishment Phase discourages non-cooperative behavior, while the Exploitation Phase maximizes individual payoffs when others are cooperative. The Endgame phase ensures that we defect in the last round to maximize payoffs, as there is no future round to consider.

This strategy is robust to a wide range of opponent behaviors, as it adapts to the overall level of cooperation and individual payoffs. By being aggressive, we aim to outperform other strategies in the tournament.
'''

description_AGGRESSIVE_31 = '''
Here's a description of an aggressive strategy for the N-Player Public Goods Game that only depends on the game parameters and history.

**Strategy Name:** " Adaptive Aggressor"

**Decision Rules:**

1. **Initial Round:** In the first round, play D (Defect) to observe the behavior of other players and establish a baseline for the game.
2. **Exploitation Phase:** In rounds 2 to r-1 (second to second-last round), play D if the average payoff per player in the previous round is less than or equal to the private payoff from keeping (1 - c_i). This indicates that the public good is not generating sufficient returns, and it's optimal to exploit the situation.
3. **Punishment Phase:** If the average payoff per player in the previous round is greater than the private payoff from keeping (1 - c_i), play C (Cooperate) if the number of cooperators in the previous round is greater than or equal to n/2 (half of the players). This aims to punish players who are not contributing to the public good and encourage cooperation.
4. **Last Round:** In the last round (r), play D to maximize individual payoff, as there are no future rounds to consider.

**Adaptive Component:**

* Monitor the number of cooperators and average payoff per player over the rounds.
* If the number of cooperators is consistently low (less than n/4), switch to an "All-D" strategy, where you play D in all remaining rounds.
* If the average payoff per player is consistently high (greater than or equal to k), switch to a " tit-for-tat" strategy, where you cooperate if the majority of players cooperated in the previous round.

**Robustness Mechanisms:**

* If the number of players is small (n < 5), play D in the first two rounds to avoid being exploited by other players.
* If the multiplication factor (k) is high (k > n-1), play C in the first round to encourage cooperation and maximize individual payoff.

Pseudocode:
```python
def adaptive_aggressor(n, r, k):
    # Initialize variables
    average_payoff = 0
    num_cooperators = 0
    previous_actions = []

    for round in range(r):
        if round == 0:
            # Initial Round: Play D
            action = 'D'
        elif round == r - 1:
            # Last Round: Play D
            action = 'D'
        else:
            # Exploitation Phase
            if average_payoff <= 1:
                action = 'D'
            # Punishment Phase
            elif num_cooperators >= n / 2:
                action = 'C'
            else:
                action = 'D'

        # Adaptive Component
        if num_cooperators < n / 4:
            action = 'D'  # Switch to All-D strategy
        elif average_payoff >= k:
            action = 'C' if num_cooperators > n / 2 else 'D'  # tit-for-tat strategy

        # Robustness Mechanisms
        if n < 5 and round < 2:
            action = 'D'
        elif k > n - 1 and round == 0:
            action = 'C'

        # Update variables
        previous_actions.append(action)
        num_cooperators = sum(1 for action in previous_actions if action == 'C')
        average_payoff = (sum(k * num_cooperators for num_cooperators in range(n)) / n) / r

        # Return action
        return action
```
This strategy is aggressive, adaptive, and robust to a wide range of opponent behaviors. It punishes non-cooperation, exploits situations where the public good is not generating sufficient returns, and adapts to changing game conditions.
'''

description_AGGRESSIVE_32 = '''
**Aggressive Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1)**: Defect (D). Observe opponents' actions to gather information.
2. **Subsequent Rounds (t>1)**: Use the following decision rules based on the game history:
	* If the average cooperation rate of opponents in the previous round is high (> 0.5), Cooperate (C) with a probability proportional to the opponent's cooperation rate. This is done to exploit the potential cooperation and gain a higher payoff.
	* If the average cooperation rate of opponents in the previous round is low (≤ 0.5), Defect (D). This is done to minimize losses and maximize individual payoff.
3. **Adaptive Component**: Monitor the opponent's cooperation rate over the last few rounds (e.g., 3-5 rounds). If the opponent's cooperation rate is increasing, increase the probability of Cooperating (C) in the next round. If the opponent's cooperation rate is decreasing, decrease the probability of Cooperating (C) in the next round.
4. **Edge Case: Last Round (t=r)**: Defect (D). In the last round, there is no future round to consider, so prioritize individual payoff maximization.

**Pseudocode:**
```python
def AdaptiveExploiter(n, k, r, history):
    if t == 1:  # Initial Round
        return D
    
    opponent_coop_rate = calculate_opponent_coop_rate(history)
    if opponent_coop_rate > 0.5:
        coop_prob = opponent_coop_rate
        return C with probability coop_prob, else D
    else:
        return D
    
    # Adaptive Component
    recent_coop_rate = calculate_recent_coop_rate(history)
    if recent_coop_rate > opponent_coop_rate:
        coop_prob += 0.1
    elif recent_coop_rate < opponent_coop_rate:
        coop_prob -= 0.1
    
    # Last Round
    if t == r:
        return D

def calculate_opponent_coop_rate(history):
    # Calculate average cooperation rate of opponents in the previous round
    opponent_coop_rate = sum(history[-1]['opponent_actions'] == C) / n
    return opponent_coop_rate

def calculate_recent_coop_rate(history):
    # Calculate average cooperation rate of opponents over the last few rounds
    recent_coop_rate = sum(history[-3:]['opponent_actions'] == C) / (3 * n)
    return recent_coop_rate
```
This strategy is aggressive because it:

1. Starts with a Defect (D) to test opponents' behavior.
2. Exploits opponents' cooperation when it is high, gaining a higher payoff.
3. Defects (D) when opponents' cooperation is low, minimizing losses.
4. Adapts to opponents' behavior, increasing or decreasing cooperation probability based on recent trends.
5. Prioritizes individual payoff maximization in the last round.

This strategy should perform well against a wide range of opponent behaviors, as it is designed to be robust and adaptive.
'''

description_OPPORTUNISTIC_1 = '''
Here's an opportunistic strategy that adapts to the game's history and parameters:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (play C) to test the waters and gather information about the opponent's behavior.
2. **Reciprocal Exploitation**: For subsequent rounds (t > 1), use the following rules:
	* If the opponent's cooperation rate ( proportion of times they played C) in the previous round is above a certain threshold (THRESHOLD), cooperate (play C). Otherwise, defect (play D).
	* THRESHOLD = (k-1)/(k*n) - a function of the multiplication factor (k) and the number of players (n). This threshold value ensures that cooperation is rewarded when the opponent is likely to cooperate, while minimizing the risk of exploitation.
3. **Punishment Mechanism**: If an opponent defects (plays D) after a round where AE cooperated (played C), AE will defect (play D) in the next round. This punishment mechanism deters opponents from exploiting AE's cooperation.
4. **Forgiveness Mechanism**: If an opponent cooperates (plays C) after a round where AE punished them (played D), AE will revert to the Reciprocal Exploitation rule.
5. **Endgame Strategy**: In the last round (t = r), always defect (play D), as there is no incentive to cooperate when the game ends.

**Edge Cases:**

* If all opponents defect (play D) in a round, AE will also defect (play D) in the next round.
* If an opponent's behavior is completely random or unresponsive, AE will adapt to defect (play D) to avoid exploitation.

**Pseudocode:**
```python
def AdaptiveExploiter(history, params):
    n = params['n']
    k = params['k']
    r = params['r']
    threshold = (k-1)/(k*n)
    
    if len(history) == 0:  # First round
        return 'C'
    
    opponent_cooperation_rate = sum(1 for action in history[-1] if action == 'C') / n
    
    if opponent_cooperation_rate >= threshold:
        return 'C'
    else:
        return 'D'
    
    # Punishment Mechanism
    if history[-1][i] == 'D' and history[-2][i] == 'C':
        return 'D'
    
    # Forgiveness Mechanism
    if history[-1][i] == 'C' and history[-2][i] == 'D':
        return 'C'
    
    # Endgame Strategy
    if len(history) == r - 1:
        return 'D'
```
**Opportunistic Mindset:**

AE is designed to be an opportunistic strategy that adapts to the game's history and parameters. It seeks to cooperate when the opponent is likely to cooperate, while minimizing the risk of exploitation. The punishment and forgiveness mechanisms ensure that AE can respond effectively to opponents who try to exploit its cooperation. By always defecting in the last round, AE avoids any potential losses from cooperation.
'''

description_OPPORTUNISTIC_2 = '''
**Opportunistic Strategy: "Adaptive Follower"**

**Decision Rules:**

1. **Initial Round (t=1)**: Cooperate (C) to encourage others to cooperate and gather information about their behavior.
2. **Subsequent Rounds (t>1)**:
	* If the total number of cooperators in the previous round is greater than or equal to the multiplication factor (k), Cooperate (C). This indicates that cooperation is paying off, and we want to continue to benefit from the public good.
	* If the total number of cooperators in the previous round is less than the multiplication factor (k), Defect (D). This suggests that cooperation is not paying off, and we want to protect our individual payoff.
3. **Last Round (t=r)**: Defect (D), as there is no future payoff to consider, and we want to maximize our individual payoff.

**Handling Edge Cases:**

* If all players defected in the previous round, and we are in a subsequent round, Cooperate (C) to try to restart cooperation.
* If we observe a player consistently cooperating while others defect, we will Cooperate (C) in the next round to try to take advantage of their altruism.

**Opportunistic Mindset:**

Our strategy is designed to be opportunistic, taking advantage of the cooperation of others while minimizing our own contributions when cooperation is not paying off. By cooperating initially and adapting to the behavior of others, we aim to maximize our total payoff over the game.

**Pseudocode:**
```python
def adaptive_follower(n, k, r, history):
  # Initialize variables
  total_cooperators = 0
  my_payoff = 0

  for t in range(1, r+1):
    # First round: Cooperate
    if t == 1:
      action = 'C'
    # Subsequent rounds
    else:
      # Count total cooperators in previous round
      total_cooperators = sum(1 for a in history[t-1] if a == 'C')
      
      # Decide action based on total cooperators
      if total_cooperators >= k:
        action = 'C'
      else:
        action = 'D'

    # Last round: Defect
    if t == r:
      action = 'D'

    # Update history and payoff
    history.append([action])
    my_payoff += calculate_payoff(n, k, history)

  return my_payoff
```
This strategy should perform well in a tournament setting, as it adapts to the behavior of others and takes advantage of cooperation when possible.
'''

description_OPPORTUNISTIC_3 = '''
**Opportunistic Strategy: Adaptive Exploitation**

**Decision Rules:**

1. **Initial Exploration** (First Round): Cooperate (C) to gather information about opponents' behavior and potential cooperation.
2. **Adaptive Exploitation**: For rounds 2 to r-1:
	* If the total payoff of cooperators in the previous round is greater than or equal to the total payoff of defectors, cooperate (C).
	* Otherwise, defect (D).
3. **Last Round** (Round r): Defect (D), as there is no future round to influence.

**Edge Cases:**

* **First Round**: Cooperate (C) to gather information and set a potential cooperative tone.
* **Last Round**: Defect (D) to maximize personal payoff.
* **No Opponents**: If playing solo (n=1), always defect (D), as cooperation has no additional value.
* **All Opponents Defect**: If all opponents have defected in the previous round, defect (D) in the current round.

**Opportunistic Mindset:**

* Monitor opponents' behavior and adapt to changes in cooperation and defection rates.
* Exploit opportunities to cooperate when it leads to higher payoffs.
* Be cautious not to be exploited by constant defectors.

**Pseudocode:**

```
// Initialize variables
 coop_count = 0
 def_count = 0
 coop_payoff = 0
 def_payoff = 0

// First Round
if round == 1:
    action = C
    coop_count += 1

// Adaptive Exploitation (Rounds 2 to r-1)
else:
    // Calculate total payoffs for cooperators and defectors in previous round
    coop_payoff = sum(coop_i * (k/n) * coop_count)
    def_payoff = sum(def_i * (1 - def_i) + (k/n) * coop_count)

    if coop_payoff >= def_payoff:
        action = C
        coop_count += 1
    else:
        action = D
        def_count += 1

// Last Round (Round r)
if round == r:
    action = D
```

This strategy balances exploration, exploitation, and adaptation to maximize payoffs in a wide range of opponent behaviors. By monitoring opponents' actions and adjusting its own behavior, Adaptive Exploitation seeks to capitalize on opportunities for cooperation while minimizing losses to defectors.
'''

description_OPPORTUNISTIC_4 = '''
**Opportunistic Strategy: Adaptive Exploiter**

The Adaptive Exploiter strategy aims to balance cooperation and defection to maximize payoffs, while being robust to various opponent behaviors. This strategy depends solely on the game parameters (n, r, k) and the history of actions and payoffs.

**Decision Rules:**

1. **Initial Rounds (t ≤ 0.2r):** Cooperate (C) to encourage others to cooperate and build a cooperative environment. This initial phase allows us to gather information about opponents' behaviors.
2. **Exploration Phase (0.2r < t ≤ 0.5r):** Play a mixed strategy:
	* Cooperate (C) with probability p = (k/n) \* (number of cooperators in previous round) / n
	* Defect (D) with probability 1 - p
	* This phase helps us understand how opponents react to cooperation and defection.
3. **Exploitation Phase (t > 0.5r):** Play an adaptive strategy based on the history of actions and payoffs:
	* Cooperate (C) if the average payoff of cooperators in the previous round is higher than the average payoff of defectors.
	* Defect (D) otherwise.
	* Additionally, if the number of cooperators in the previous round is above a certain threshold (e.g., 0.6n), defect (D) to exploit the cooperation.
4. **Endgame (t = r):** Defect (D) to maximize individual payoff in the final round.

**Handling Edge Cases:**

* **First Round (t = 1):** Cooperate (C) to encourage others to cooperate and build a cooperative environment.
* **Last Round (t = r):** Defect (D) to maximize individual payoff.
* **Opponent Defection:** If an opponent defects, increase the probability of defection in the next round.
* **Opponent Cooperation:** If an opponent cooperates, increase the probability of cooperation in the next round.

**Opportunistic Mindset:**

The Adaptive Exploiter strategy is designed to be opportunistic, taking advantage of cooperation when it benefits us and defecting when it maximizes our payoff. By adapting to the history of actions and payoffs, we can exploit opponents' cooperative tendencies while minimizing our own losses.

**Pseudocode:**
```python
def adaptive_exploiter(n, r, k, history):
    if t <= 0.2r:
        return C  # Initial cooperation phase
    elif 0.2r < t <= 0.5r:
        p = (k/n) * (num_cooperators_previous_round / n)
        return C with probability p, D otherwise  # Exploration phase
    elif t > 0.5r:
        avg_payoff_coop = average_payoff_cooperators_previous_round
        avg_payoff_defect = average_payoff_defectors_previous_round
        if avg_payoff_coop > avg_payoff_defect:
            return C  # Exploitation phase
        else:
            return D
    elif t == r:
        return D  # Endgame
```
Note that this pseudocode is a simplified representation of the strategy, and the actual implementation will require more nuanced calculations and tracking of game history.
'''

description_OPPORTUNISTIC_5 = '''
**Opportunistic Strategy: Adaptive Cooperation (AC)**

**Decision Rules:**

1. **First Round:** Cooperate (C) to encourage initial cooperation and set a positive tone.
2. **Subsequent Rounds:** Observe the previous round's outcome and adjust strategy accordingly.
3. **Cooperation Threshold:** Calculate the cooperation threshold (CT) based on the game parameters and previous rounds' outcomes. CT is the minimum number of cooperators required to make cooperation a better option than defection.
4. **Current Round:** If the number of cooperators in the previous round is greater than or equal to CT, Cooperate (C). Otherwise, Defect (D).

**Cooperation Threshold (CT) Calculation:**

CT = ceil((n \* k) / (n + k))

where ceil(x) is the ceiling function, rounding x up to the nearest integer.

**Pseudocode:**
```python
def adaptive_cooperation(n, k, r, history):
    # Initialize variables
    CT = ceil((n * k) / (n + k))
    cooperate = True  # First round cooperation

    for t in range(1, r + 1):
        if t > 1:
            # Calculate number of cooperators in previous round
            num_coop_prev = sum(1 for action in history[t - 1] if action == 'C')

            # Adjust cooperation based on CT
            if num_coop_prev >= CT:
                cooperate = True
            else:
                cooperate = False

        # Make decision for current round
        if cooperate:
            action = 'C'
        else:
            action = 'D'

        # Store action in history
        history[t].append(action)

    return history
```
**Rationale:**

The Adaptive Cooperation strategy is designed to be opportunistic, taking advantage of the game's structure and the opponents' behavior. By cooperating in the first round, we encourage initial cooperation and set a positive tone. The cooperation threshold (CT) calculation helps us determine when cooperation is likely to be beneficial.

In subsequent rounds, we observe the previous round's outcome and adjust our strategy accordingly. If the number of cooperators is greater than or equal to CT, we cooperate, as this is likely to yield a better payoff. Otherwise, we defect, as the potential payoff from cooperation is lower.

This strategy is adaptive and robust, as it responds to the game's dynamics and the opponents' behavior. It does not rely on any specific coordination mechanisms or assumptions about opponents' strategies.

**Edge Cases:**

* **Last Round:** The strategy will make decisions based on the previous round's outcome, as there is no future round to consider.
* **Ties:** In case of ties, the strategy will defect, as the potential payoff from cooperation is lower.

By following this opportunistic strategy, we aim to maximize our payoffs while adapting to the game's dynamics and the opponents' behavior.
'''

description_OPPORTUNISTIC_6 = '''
Here's a opportunistic strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Opportunistic Cooperation (AOC)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:** Use a combination of recent history and game parameters to decide between Cooperate (C) and Defect (D).
3. **Recent History:** Track the average cooperation rate of all players over the last 2-3 rounds (adjustable parameter). If the average cooperation rate is above a certain threshold (e.g., 0.5), Cooperate (C) in the current round. Otherwise, Defect (D).
4. **Game Parameters:** Consider the multiplication factor (k) and the number of players (n). If k is relatively high (e.g., k > 1.5) and n is moderate to large (e.g., n > 4), Cooperate (C) more frequently, as the potential payoff from cooperation is higher.
5. **Exploitation Detection:** Monitor the recent history of other players' actions. If a player consistently Defects (D) while others Cooperate (C), classify them as an exploiter. In the next round, Defect (D) if an exploiter is present, as they are unlikely to Cooperate (C).
6. **Punishment Mechanism:** If a player Defects (D) while others Cooperate (C), punish them by Defecting (D) in the next round. This mechanism helps maintain cooperation and discourages exploitation.
7. **Final Round (Round r):** Defect (D) in the last round, as there is no incentive to Cooperate (C) when there are no future rounds to influence.

**Edge Cases:**

* **Tiebreaker:** In case of a tie in the average cooperation rate, Cooperate (C) to maintain a cooperative atmosphere.
* **No Recent History:** In the first few rounds, use a default cooperation rate (e.g., 0.5) until sufficient history is available.

**Pseudocode:**

```
AOC Strategy:

// Initialize variables
avg_cooperation_rate = 0
recent_history = []
exploiters = []

// Loop through rounds
for t = 1 to r:
    // First round
    if t == 1:
        action = C
    else:
        // Calculate average cooperation rate
        avg_cooperation_rate = sum(recent_history) / len(recent_history)
        
        // Check game parameters
        if k > 1.5 and n > 4:
            cooperation_bias = 0.6
        else:
            cooperation_bias = 0.4
        
        // Decide action based on recent history and game parameters
        if avg_cooperation_rate > cooperation_bias:
            action = C
        else:
            action = D
        
        // Check for exploiters
        if exploiter_detected():
            action = D
        
        // Punish exploiters
        if punish_exploiters():
            action = D
    
    // Update recent history and exploiters
    recent_history.append(action)
    if exploiter_detected():
        exploiters.append(player_id)
    
    // Play action
    play(action)

// Functions
def exploiter_detected():
    # Check if a player consistently Defects (D) while others Cooperate (C)
    pass

def punish_exploiters():
    # Check if an exploiter is present and punish them
    pass
```

This strategy is adaptive, as it adjusts its behavior based on the recent history of cooperation rates and game parameters. It is also robust, as it can handle a wide range of opponent behaviors and exploiters. By punishing exploiters and maintaining a cooperative atmosphere, the AOC strategy aims to maximize its payoff in the N-Player Public Goods Game.
'''

description_OPPORTUNISTIC_7 = '''
**Opportunistic Strategy: "Adaptive Explorer"**

**Decision Rules:**

1. **Initial Exploration (Rounds 1-3)**: Cooperate (C) with a probability of 0.5, and Defect (D) with a probability of 0.5. This allows us to gather initial information about the opponents' behavior.
2. **Adaptive Response**: After the initial exploration phase, observe the average cooperation rate of all players in the previous round (t-1). If the average cooperation rate is above a certain threshold (THRESHOLD = 0.5), Cooperate (C) in the current round (t). Otherwise, Defect (D).
3. **Punishment Mechanism**: If the average cooperation rate in the previous round (t-1) is below a certain threshold (THRESHOLD = 0.5) and the player's own payoff in the previous round (t-1) is lower than the expected payoff if everyone had cooperated, then Defect (D) in the current round (t) with a higher probability (PROB_DEFECT = 0.8).
4. **Endgame Strategy**: In the last round (r), Defect (D) if the player's total payoff is lower than the average total payoff of all players. Otherwise, Cooperate (C).

**Edge Cases:**

1. **First Round**: Cooperate (C) with a probability of 0.5, and Defect (D) with a probability of 0.5.
2. **Last Round**: Follow the Endgame Strategy.
3. **Tiebreaker**: In case of a tie in the average cooperation rate or total payoff, Cooperate (C).

**Pseudocode:**

```
INPUT: n, k, r, THRESHOLD, PROB_DEFECT
OUTPUT: Action (C or D) for each round

FOR EACH ROUND t FROM 1 TO r:
  IF t <= 3:
    // Initial Exploration
    action[t] = Random(C or D)
  ELSE:
    // Adaptive Response
    avg_coop_rate[t-1] = Calculate average cooperation rate in previous round
    IF avg_coop_rate[t-1] > THRESHOLD:
      action[t] = C
    ELSE:
      // Punishment Mechanism
      IF avg_coop_rate[t-1] < THRESHOLD AND player_payoff[t-1] < expected_payoff:
        action[t] = D with probability PROB_DEFECT
      ELSE:
        action[t] = D
  END IF
  IF t == r:
    // Endgame Strategy
    IF player_total_payoff < avg_total_payoff:
      action[t] = D
    ELSE:
      action[t] = C
  END IF
END FOR
```

**Opportunistic Mindset:**

The Adaptive Explorer strategy is designed to be opportunistic, taking advantage of the situation to maximize its own payoff. It adapts to the opponents' behavior, cooperates when beneficial, and defects when necessary. The strategy is robust to a wide range of opponent behaviors and does not rely on coordination mechanisms or shared norms.
'''

description_OPPORTUNISTIC_8 = '''
**Opportunistic Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to gather information and set a positive tone.
2. **Subsequent Rounds (t>1):** Defect (D) if the total payoff from the previous round is greater than or equal to the average payoff of all players in the previous round. Otherwise, Cooperate (C).

Pseudocode:
```
if t == 1:
    action = C
else:
    total_payoff_prev = sum(player_i_payoff_prev for player_i in players)
    avg_payoff_prev = total_payoff_prev / n
    if player_i_payoff_prev >= avg_payoff_prev:
        action = D
    else:
        action = C
```
**Edge Cases:**

1. **Last Round (t=r):** Defect (D) to maximize individual payoff, as there are no future rounds to consider.
2. **Tiebreaker:** In case of a tie in the payoff comparison, Cooperate (C) to maintain a positive reputation and encourage cooperation from others.

**Opportunistic Mindset:**

The Adaptive Exploiter strategy is designed to capitalize on opportunities to maximize individual payoffs while being responsive to the behavior of other players. By cooperating in the initial round, the strategy sets a positive tone and gathers information about the opponents' behavior. In subsequent rounds, the strategy defects when the total payoff from the previous round is high, indicating that other players are cooperating, and exploits this cooperation to increase its own payoff. Conversely, if the total payoff is low, the strategy cooperates to encourage others to do the same and increase the overall payoff.

**Rationale:**

This strategy is opportunistic because it adapts to the behavior of other players and exploits their cooperation when possible. By defecting when the total payoff is high, the strategy takes advantage of the cooperation of others to increase its own payoff. By cooperating when the total payoff is low, the strategy encourages others to cooperate and increases the overall payoff. This approach allows the Adaptive Exploiter to perform well in a wide range of scenarios, from highly cooperative to highly competitive environments.

**Tournament Readiness:**

The Adaptive Exploiter strategy is designed to perform well in a tournament setting, where it will face a variety of independent strategies developed by other AI systems. By being responsive to the behavior of other players and adapting its strategy accordingly, the Adaptive Exploiter can effectively compete against a range of opponents and emerge as a top performer.
'''

description_OPPORTUNISTIC_9 = '''
I'll design an opportunistic strategy for the N-Player Public Goods Game that adapts to the game parameters and history. Here's the strategy:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) with a probability of 0.5. This allows us to gather information about the opponents' behavior while also potentially benefiting from a high cooperation rate.
2. **Subsequent Rounds (t>1):** Observe the total number of cooperators (Σc_j) and the average payoff (avg_π) of all players in the previous round.
3. **Exploitation Condition:** If avg_π > (1 + k/n), it means that the group's average payoff is higher than the minimum guaranteed payoff (1) plus the potential gain from cooperation (k/n). In this case, Defect (D) with a probability of 0.7. This allows us to exploit the high cooperation rate and increase our own payoff.
4. **Cooperation Condition:** If Σc_j > (n/2), it means that more than half of the players cooperated in the previous round. In this case, Cooperate (C) with a probability of 0.7. This helps to maintain a high cooperation rate and increases the group's overall payoff.
5. **Default Action:** If neither condition is met, Defect (D) with a probability of 0.5.

**Edge Cases:**

1. **Last Round (t=r):** Always Defect (D). Since there are no future rounds, there's no incentive to cooperate.
2. **Tiebreaker:** If the exploitation condition and cooperation condition are both met, prioritize the exploitation condition and Defect (D).
3. **No Information:** If no information is available about the opponents' behavior (e.g., due to a lack of previous rounds), default to the initial round strategy (Cooperate with probability 0.5).

**Opportunistic Mindset:**

The Adaptive Exploiter strategy is designed to be opportunistic by:

1. **Exploiting high cooperation rates:** By defecting when the group's average payoff is high, we take advantage of the opponents' cooperation and increase our own payoff.
2. **Adapting to changing conditions:** The strategy adjusts its behavior based on the observed behavior of the opponents, allowing us to respond to changes in the game dynamics.
3. **Balancing cooperation and defection:** By cooperating when the cooperation rate is high and defecting when the exploitation condition is met, we balance our own interests with the need to maintain a high cooperation rate.

Pseudocode:
```
def AdaptiveExploiter(n, k, r, history):
  if t == 1:  # Initial Round
    cooperate_prob = 0.5
  else:
    avg_payoff = calculate_average_payoff(history)
    total_cooperators = calculate_total_cooperators(history)
    
    if avg_payoff > (1 + k/n):  # Exploitation Condition
      cooperate_prob = 0.3
    elif total_cooperators > (n/2):  # Cooperation Condition
      cooperate_prob = 0.7
    else:
      cooperate_prob = 0.5
  
  if t == r:  # Last Round
    cooperate_prob = 0.0
  
  if random.random() < cooperate_prob:
    return C
  else:
    return D
```
Note that this is a high-level description of the strategy, and the implementation details may vary depending on the programming language and specific requirements.
'''

description_OPPORTUNISTIC_10 = '''
I propose a strategy called "Adaptive Opportunism" (AO) that balances cooperation and defection based on the game's history and parameters. AO aims to maximize its payoff by adapting to the behavior of other players.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to encourage others to cooperate and build a cooperative environment.
2. **General Round (Rounds 2-r):**
	* If the total number of cooperators in the previous round is greater than or equal to n/2, Cooperate (C) to maintain the cooperative environment and maximize the share of the public good.
	* If the total number of cooperators in the previous round is less than n/2, Defect (D) to minimize losses and adapt to the non-cooperative environment.
3. **Special Case: Last Round (Round r):** Defect (D) to maximize the private payoff, as there is no future round to benefit from cooperation.

**Edge Cases:**

* **First Round with only 2 players (n=2):** Cooperate (C) to encourage cooperation, as the potential gain from cooperation is higher with fewer players.
* **Last Round with only 2 players (n=2):** Defect (D) to maximize the private payoff, as the potential loss from cooperation is lower with fewer players.

**Opportunistic Mindset:**

AO takes advantage of the cooperation of others while minimizing its own losses. By cooperating in the initial round and when the majority cooperates, AO encourages a cooperative environment and maximizes the share of the public good. However, when the majority defects, AO adapts by defecting to minimize losses. This strategy balances cooperation and defection to achieve the highest possible payoff.

**Pseudocode:**
```python
def adaptive_opportunism(n, k, r, history):
  if r == 1:  # Initial Round
    return C
  elif history[-1]['cooperators'] >= n / 2:  # General Round
    return C
  else:
    return D
  if r == r:  # Last Round
    return D
```
This strategy is robust to a wide range of opponent behaviors and does not rely on coordination mechanisms or predetermined patterns. It adapts to the game's history and parameters to maximize its payoff.
'''

description_OPPORTUNISTIC_11 = '''
I propose a strategy called "Adaptive Opportunism" (AO) that balances cooperation and defection to maximize payoffs. AO depends only on game parameters (n, r, k) and the history of previous rounds.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to encourage cooperation and create a positive atmosphere.
2. **Subsequent Rounds (t>1):** Evaluate the previous round's outcome:
	* If the total number of cooperators (Σc_j) was at least half of the players (n/2), cooperate (C) in the current round.
	* Otherwise, defect (D) in the current round.
3. **Exception for High Cooperation:** If the total number of cooperators in the previous round was exceptionally high (Σc_j ≥ 0.75n), defect (D) in the current round to exploit the cooperative environment.
4. **Last Round (t=r):** Defect (D) to maximize individual payoff, as there is no future opportunity to reciprocate.

**Pseudocode:**
```
function AdaptiveOpportunism(n, r, k, history):
  if t == 1:  // Initial round
    return C
  else:
    Σc_j = count cooperators in previous round
    if Σc_j >= n/2:
      return C
    elif Σc_j >= 0.75n:
      return D  // Exploit high cooperation
    else:
      return D
  if t == r:  // Last round
    return D
```
**Rationale:**

AO aims to balance cooperation and defection to maximize payoffs. By cooperating in the initial round, AO encourages others to cooperate and creates a positive atmosphere. In subsequent rounds, AO evaluates the previous round's outcome and adapts its strategy:

* If the previous round had sufficient cooperation, AO cooperates to maintain the cooperative environment.
* If the previous round had low cooperation, AO defects to avoid being exploited.
* If the previous round had exceptionally high cooperation, AO defects to exploit the cooperative environment.

In the last round, AO defects to maximize individual payoff, as there is no future opportunity to reciprocate.

AO is opportunistic because it takes advantage of cooperative environments while minimizing the risk of being exploited. It is adaptive because it adjusts its strategy based on the history of previous rounds. AO is robust to a wide range of opponent behaviors, as it does not rely on specific coordination mechanisms or assumptions about others' strategies.
'''

description_OPPORTUNISTIC_12 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to explore the opponent's behavior and create a potential for mutual cooperation.
2. **Subsequent Rounds (Round 2 to r-1):**
	* If the total number of cooperators in the previous round is greater than or equal to (n+1)/2 (a simple majority), Cooperate (C). This indicates a potential for mutual cooperation, and we want to reinforce it.
	* Otherwise, Defect (D) to exploit the opponent's cooperation and maximize our payoff.
3. **Last Round (Round r):** Defect (D) to maximize our payoff, as there are no future rounds to consider.

**Edge Cases:**

1. **Tiebreaker:** If the total number of cooperators in the previous round is exactly (n+1)/2, Cooperate (C) to break the tie and create an opportunity for mutual cooperation.
2. **Zero Cooperators:** If no one cooperated in the previous round, Cooperate (C) to restart the cooperation dynamics.
3. **All Cooperators:** If all players cooperated in the previous round, Cooperate (C) to maintain the cooperation equilibrium.

**Opportunistic Mindset:**

AO aims to adapt to the opponent's behavior, exploiting their cooperation when possible while maintaining a willingness to cooperate when mutually beneficial. By cooperating initially and adjusting based on the opponent's behavior, AO balances exploration and exploitation to maximize its payoff.

**Pseudocode:**
```python
def Adaptive_Opportunism(n, k, r, history):
  if r == 1:  # Initial Round
    return 'C'
  elif sum(history[-1]) >= (n+1)/2:  # Majority Cooperated
    return 'C'
  else:
    return 'D'

def Last_Round(r):
  if r == r:  # Last Round
    return 'D'
  else:
    return Adaptive_Opportunism(n, k, r, history)

def AO_Strategy(n, k, r, history):
  if r == 1:
    return Adaptive_Opportunism(n, k, r, history)
  else:
    return Last_Round(r)
```
This strategy is designed to be adaptive, robust, and opportunistic, making it a competitive contender in the tournament.
'''

description_OPPORTUNISTIC_13 = '''
**Opportunistic Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to maximize the potential for mutual cooperation and set a positive tone for the game.
2. **Subsequent Rounds (t>1):**
	* If the average payoff of cooperators (C) is higher than the average payoff of defectors (D) in the previous round, Cooperate (C).
	* If the average payoff of defectors (D) is higher than or equal to the average payoff of cooperators (C) in the previous round, Defect (D).
3. **Last Round (t=r):** Defect (D), as there is no future opportunity to reciprocate or be reciprocated.

**Handling Edge Cases:**

1. **Tie in Average Payoffs:** In case of a tie, Cooperate (C) to maintain a cooperative posture and encourage mutual cooperation.
2. **No Previous Round Data (t=1):** Cooperate (C) as per the initial round rule.
3. **Single Opponent:** Treat the single opponent as a special case of multiple opponents and apply the decision rules accordingly.

**Opportunistic Mindset:**

1. **Monitor Opponent Behavior:** Continuously track the actions and payoffs of all opponents to identify opportunities for exploitation.
2. **Adapt to Changing Circumstances:** Adjust the strategy based on the evolving game dynamics, such as changes in opponent behavior or payoff distributions.
3. **Exploit Cooperative Opponents:** Take advantage of cooperative opponents by defecting when they are more likely to cooperate, while maintaining a cooperative posture to avoid triggering a mutual defection response.
4. **Deter Exploitation:** Cooperate when opponents are more likely to defect, to demonstrate the benefits of mutual cooperation and deter exploitation.

**Pseudocode:**
```
def adaptive_exploiter(n, k, r, history):
  if t == 1:  # Initial round
    return C
  elif average_payoff_C(history) > average_payoff_D(history):
    return C
  else:
    return D

def average_payoff_C(history):
  # Calculate average payoff of cooperators in the previous round
  return sum([payoff for action, payoff in history if action == C]) / len([action for action in history if action == C])

def average_payoff_D(history):
  # Calculate average payoff of defectors in the previous round
  return sum([payoff for action, payoff in history if action == D]) / len([action for action in history if action == D])
```
This strategy is designed to be opportunistic, adaptive, and robust to a wide range of opponent behaviors. It balances cooperation and defection to maximize payoffs while minimizing the risk of exploitation.
'''

description_OPPORTUNISTIC_14 = '''
**Opportunistic Strategy: Adaptive Cooperator**

Decision Rules:

1. **Initial Cooperation**: In the first round, cooperate (play C) to test the waters and encourage potential cooperation from others.
2. **Reciprocity**: For rounds 2 to (r-1), cooperate if the total number of cooperators in the previous round is greater than or equal to (n/2). This promotes reciprocity and builds on existing cooperation.
3. **Exploitation**: If the total number of cooperators in the previous round is less than (n/2), defect (play D) to maximize personal payoff.
4. **Last Round**: In the final round (r), defect (play D) as there is no future opportunity for reciprocity.

Edge Case Handling:

1. **First Round**: Cooperate (play C) as per the initial cooperation rule.
2. **Last Round**: Defect (play D) as per the last round rule.
3. **Ties**: In case of ties (e.g., equal number of cooperators and defectors), cooperate if the previous round was cooperative, and defect otherwise.
4. **Zero Cooperators**: If no one cooperated in the previous round, defect (play D) to avoid contributing to a non-existent public good.

Opportunistic Mindset:

1. **Monitor and Adapt**: Continuously observe the number of cooperators and adjust strategy accordingly.
2. **Exploit Weakness**: Defect when cooperation is low to maximize personal payoff.
3. **Encourage Cooperation**: Cooperate when cooperation is high to build on existing cooperation and encourage others to do the same.

Pseudocode:

```markdown
# Initialize variables
n = number of players
r = number of rounds
k = multiplication factor
history = empty list to store previous rounds' data

# First round
if round == 1:
    action = C  # Cooperate
else:
    # Get previous round's data
    prev_round_cooperators = history[-1]['cooperators']

    # Reciprocity rule
    if prev_round_cooperators >= (n / 2):
        action = C  # Cooperate
    else:
        action = D  # Defect

    # Last round rule
    if round == r:
        action = D  # Defect

# Store current round's data
history.append({'cooperators': current_round_cooperators, 'action': action})
```

This strategy balances cooperation and defection, adapting to the game's dynamics and exploiting opportunities for personal gain. By cooperating initially and reciprocating cooperation, it encourages others to cooperate. When cooperation is low, it defects to maximize payoff. In the final round, it defects to avoid contributing to a potentially non-existent public good.
'''

description_OPPORTUNISTIC_15 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate cooperation and gather information about opponents' behavior.
2. **Early Rounds (t < r/2):** Cooperate (C) if the average payoff from cooperation in previous rounds is higher than the average payoff from defection. Otherwise, Defect (D).
3. **Mid-Game (t ≥ r/2):** Use a tit-for-tat-like approach:
	* If the number of cooperators in the previous round is greater than or equal to the number of defectors, Cooperate (C).
	* Otherwise, Defect (D).
4. **Late Rounds (t > 3r/4):** Focus on maximizing individual payoff:
	* If the current payoff from cooperation is higher than the current payoff from defection, Cooperate (C).
	* Otherwise, Defect (D).
5. **Last Round (t = r):** Defect (D) to maximize individual payoff, as there is no future opportunity for reciprocity.

**Edge Cases:**

* If all opponents have defected in all previous rounds, Defect (D) in the current round.
* If all opponents have cooperated in all previous rounds, Cooperate (C) in the current round.

**Opportunistic Mindset:**

The AO strategy is designed to be adaptive and opportunistic, taking advantage of the game's dynamics and opponents' behavior. By cooperating initially and in early rounds, the strategy encourages cooperation and gathers information about opponents. As the game progresses, the strategy adjusts to the opponents' behavior, exploiting opportunities for individual gain while maintaining a level of cooperation to sustain the public good.

**Pseudocode:**
```python
def adaptive_opportunism(n, r, k, history):
  if t == 1:  # First Round
    return C
  elif t < r/2:  # Early Rounds
    avg_coop_payoff = sum(history[t-1][C]) / len(history[t-1][C])
    avg_def_payoff = sum(history[t-1][D]) / len(history[t-1][D])
    return C if avg_coop_payoff > avg_def_payoff else D
  elif t >= r/2 and t < 3r/4:  # Mid-Game
    num_coop = sum(1 for action in history[t-1] if action == C)
    num_def = sum(1 for action in history[t-1] if action == D)
    return C if num_coop >= num_def else D
  elif t > 3r/4:  # Late Rounds
    current_coop_payoff = (k/n) * sum(1 for action in history[t-1] if action == C)
    current_def_payoff = 1 + (k/n) * sum(1 for action in history[t-1] if action == C)
    return C if current_coop_payoff > current_def_payoff else D
  else:  # Last Round
    return D
```
This strategy will adapt to various opponent behaviors, exploiting opportunities for individual gain while maintaining a level of cooperation to sustain the public good.
'''

description_OPPORTUNISTIC_16 = '''
Here's a strategic approach that I propose:

**Strategy Name:** Adaptive Opportunism (AO)

**Overview:** AO is a strategy that balances cooperation and defection based on the observed behavior of other players and the game's parameters. It seeks to maximize its payoff by cooperating when it's beneficial and defecting when it's not.

**Decision Rules:**

1. **First Round:** Defect (D). This is an exploratory round to gauge the behavior of other players.
2. **Consecutive Cooperation (CC) Rule:** If at least 50% of players cooperated in the previous round, cooperate (C) in the current round. This rule encourages cooperation when there's a strong social norm.
3. **Punishment Rule:** If the average payoff of cooperators in the previous round is lower than the average payoff of defectors, defect (D) in the current round. This rule deters exploitation by defectors.
4. **Exploitation Rule:** If the average payoff of cooperators in the previous round is higher than the average payoff of defectors, cooperate (C) in the current round. This rule allows AO to exploit cooperative behavior.
5. **Default Rule:** If none of the above rules apply, cooperate (C) with a probability of (k/n), where k is the multiplication factor and n is the number of players. This rule provides a baseline level of cooperation.
6. **Last Round:** Defect (D). In the final round, there's no incentive to cooperate, as the game ends after this round.

**Edge Cases:**

* If all players defected in the previous round, AO will cooperate with a probability of (k/n) to try to restart cooperation.
* If AO's payoff in the previous round was higher than the average payoff of all players, AO will cooperate in the current round to maintain its relative advantage.

**Opportunistic Mindset:** AO is designed to be opportunistic by:

* Cooperating when it's beneficial (e.g., when others are cooperating)
* Defecting when it's not beneficial (e.g., when others are exploiting cooperators)
* Adapting to changing behavior patterns in the game
* Seeking to maximize its payoff in each round

**Pseudocode:**
```
Input: game history, current round, number of players (n), multiplication factor (k)
Output: action (C or D)

if current round == 1:
  return D (first round)

if last round was cooperative (at least 50% cooperated):
  return C (consecutive cooperation rule)

if average payoff of cooperators < average payoff of defectors:
  return D (punishment rule)

if average payoff of cooperators > average payoff of defectors:
  return C (exploitation rule)

if none of the above rules apply:
  probability = k / n
  if random() < probability:
    return C
  else:
    return D

if current round == last round:
  return D (last round)

return C (default rule)
```
This strategy is designed to be adaptive and robust, taking into account the game's parameters and history. By balancing cooperation and defection, AO seeks to maximize its payoff in a wide range of scenarios.
'''

description_OPPORTUNISTIC_17 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game that adapts to the game parameters and history.

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to establish a baseline for the group's willingness to contribute.
2. **Early Rounds (t=2 to t=r/2):** If the average payoff per player in the previous round is greater than or equal to 1.5, Cooperate (C). Otherwise, Defect (D).
3. **Mid-Game (t=r/2 to t=3r/4):** Assess the group's overall cooperation level by calculating the average number of cooperators in the previous rounds. If this average is greater than or equal to n/2, Cooperate (C). Otherwise, Defect (D).
4. **Late Rounds (t=3r/4 to t=r-1):** Focus on maximizing individual payoff. If the previous round's payoff was greater when cooperating, Cooperate (C). Otherwise, Defect (D).
5. **Final Round (t=r):** Defect (D) to maximize individual payoff, as there's no future benefit to cooperation.

**Handling Edge Cases:**

* **Single Round Games (r=1):** Always Defect (D), as cooperation yields no long-term benefit.
* **Small Group Sizes (n=2):** Always Cooperate (C) in the first round, then mirror the opponent's previous action to ensure mutual cooperation or defection.

**Pseudocode:**

```python
def adaptive_opportunism(n, r, k, history):
    # Initialize variables
    t = current_round
    avg_payoff = 0
    avg_cooperators = 0
    
    # Early rounds (t=2 to t=r/2)
    if t <= r/2:
        avg_payoff = calculate_avg_payoff(history)
        if avg_payoff >= 1.5:
            return C
        else:
            return D
    
    # Mid-game (t=r/2 to t=3r/4)
    elif t <= 3r/4:
        avg_cooperators = calculate_avg_cooperators(history)
        if avg_cooperators >= n/2:
            return C
        else:
            return D
    
    # Late rounds (t=3r/4 to t=r-1)
    elif t < r:
        prev_payoff = history[-1][payoff]
        if prev_payoff > 1:
            return C
        else:
            return D
    
    # Final round (t=r)
    else:
        return D
```

**Opportunistic Mindset:**

This strategy is designed to be opportunistic by:

* Initially cooperating to establish a baseline for the group's willingness to contribute.
* Adapting to the group's overall cooperation level and adjusting actions accordingly.
* Focusing on maximizing individual payoff in late rounds.
* Defecting in the final round to ensure maximum individual gain.

By being adaptive and responsive to the game's history, AO aims to capitalize on opportunities for cooperation while minimizing losses in a dynamic and unpredictable environment.
'''

description_OPPORTUNISTIC_18 = '''
I'll design an opportunistic strategy for the N-Player Public Goods Game that adapts to the game parameters and history. Meet "Opportunistic Explorer" (OE):

**Decision Rules:**

1. **Initial Exploration** (Rounds 1-3): Play C (Cooperate) to gather information about the group's behavior and the potential benefits of cooperation.
2. **Exploitation** (Rounds 4+):
	* If the average payoff per player in the previous round (π_avg,t-1) is greater than the individual payoff for defecting (1), play C. This indicates that the group is contributing enough to make cooperation beneficial.
	* If π_avg,t-1 is less than or equal to 1, play D. This suggests that the group is not contributing enough, and defecting is the better option.
3. **Adaptive Threshold**: Introduce a dynamic threshold (T) to adjust the exploitation strategy based on the game's history. Initialize T = 1.
	* If the group's average payoff per player (π_avg) exceeds T in a round, increment T by 0.1. This increases the threshold for cooperation, making OE more cautious.
	* If π_avg falls below T, decrement T by 0.1. This decreases the threshold, making OE more willing to cooperate.
4. **Punishment**: If a player defects while the group's average payoff is above T, OE will play D in the next round. This punishes the defector and encourages cooperation.
5. **Final Round**: In the last round (r), play D to maximize individual payoff, as there's no future interaction to consider.

**Edge Cases:**

* **First Round**: Play C to gather information and encourage cooperation.
* **Last Round**: Play D to maximize individual payoff.
* **Tie in Payoffs**: In cases where the average payoff is exactly equal to the threshold (T), play C to maintain a cooperative stance.

**Opportunistic Mindset:**

OE is designed to be opportunistic by:

* Initially exploring the group's behavior to identify potential benefits from cooperation.
* Adapting to the game's history by adjusting the threshold (T) for cooperation.
* Punishing defectors to maintain a cooperative environment.
* Exploiting the group's contributions when beneficial, while minimizing the risk of being exploited.

**Pseudocode:**
```
 Initialize T = 1
 For each round (t):
   If t ≤ 3:
     Play C
   Else:
     Calculate π_avg,t-1
     If π_avg,t-1 > 1:
       Play C
     Else:
       Play D
     If π_avg > T:
       T += 0.1
     ElseIf π_avg < T:
       T -= 0.1
     If a player defected and π_avg > T:
       Play D in the next round
   If t == r:
     Play D
```
Opportunistic Explorer is designed to balance cooperation and exploitation, adapting to the game's parameters and history. By being opportunistic, OE aims to maximize its individual payoff while encouraging cooperation within the group.
'''

description_OPPORTUNISTIC_19 = '''
**Opportunistic Strategy: Adaptive Cooperator**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a baseline level of cooperation and encourage others to do the same.
2. **Subsequent Rounds:**
	* If the total number of cooperators in the previous round is greater than or equal to the number of defectors, Cooperate (C).
	* If the total number of cooperators in the previous round is less than the number of defectors, Defect (D).
	* If there is a tie, cooperate if the previous round's payoff was higher when cooperating, otherwise defect.
3. **Payoff-based Adjustment:** Monitor the payoff difference between cooperating and defecting in the previous round. If the payoff from cooperating is significantly higher (e.g., by 10% or more), increase the likelihood of cooperating in the next round. If the payoff from defecting is significantly higher, increase the likelihood of defecting.
4. **Opponent Adaptation:** Observe the actions of other players and adjust the strategy accordingly. If a player consistently cooperates or defects, adjust the likelihood of cooperating or defecting in response.

**Edge Cases:**

1. **Last Round:** Cooperate (C) to maximize the total payoff, as there is no future round to influence.
2. **Tiebreakers:** In case of a tie in the number of cooperators and defectors, cooperate if the previous round's payoff was higher when cooperating, otherwise defect.
3. **No Previous Data:** In the event of missing or incomplete data from previous rounds, default to cooperating.

**Pseudocode:**
```
Initialize:
  cooperate_likelihood = 0.5
  defect_likelihood = 0.5

First Round:
  action = Cooperate (C)

Subsequent Rounds:
  if total_cooperators >= total_defectors:
    action = Cooperate (C)
  else:
    action = Defect (D)

  if previous_round_payoff_difference > 10%:
    if cooperating_payoff > defecting_payoff:
      cooperate_likelihood += 0.1
    else:
      defect_likelihood += 0.1

  if opponent_adaptation:
    if opponent_consistently_cooperates:
      cooperate_likelihood += 0.05
    elif opponent_consistently_defects:
      defect_likelihood += 0.05

  if last_round:
    action = Cooperate (C)

  return action
```
This strategy is opportunistic, as it adapts to the game environment and adjusts its behavior based on the actions of other players. By cooperating in the first round and subsequent rounds where cooperation is prevalent, the strategy encourages cooperation and maximizes the total payoff. By defecting when cooperation is low, the strategy minimizes losses. The payoff-based adjustment and opponent adaptation mechanisms allow the strategy to respond to changes in the game environment and opponent behaviors.
'''

description_OPPORTUNISTIC_20 = '''
Here is an opportunistic strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **First Round:** Cooperate (C). This sets a cooperative tone and encourages others to cooperate.
2. **Rounds 2-r:** Use a variant of the "Tit-for-Tat" strategy, adapted for the public goods game. Specifically:
	* If the average payoff of cooperators in the previous round is higher than the average payoff of defectors, Cooperate (C).
	* If the average payoff of defectors in the previous round is higher than the average payoff of cooperators, Defect (D).
	* If the average payoffs are equal, Cooperate (C) with probability k/n (the multiplication factor divided by the number of players) and Defect (D) otherwise.
3. **Last Round (r):** Defect (D). Since there is no future interaction, there is no incentive to cooperate.

**Edge Case Handling:**

* If there are no cooperators in the previous round, Defect (D).
* If there are no defectors in the previous round, Cooperate (C).
* If the game is in a state of complete cooperation or complete defection, maintain the current action (C or D, respectively).

**Pseudocode:**
```python
def AO(n, k, r, history):
    if current_round == 1:
        return C  # Cooperate in the first round
    else:
        avg_coop_payoff = calculate_avg_payoff(history, C)
        avg_def_payoff = calculate_avg_payoff(history, D)
        if avg_coop_payoff > avg_def_payoff:
            return C  # Cooperate if cooperators earned more
        elif avg_def_payoff > avg_coop_payoff:
            return D  # Defect if defectors earned more
        else:
            p = k / n  # probability of cooperating
            return C if random.random() < p else D
    if current_round == r:
        return D  # Defect in the last round

def calculate_avg_payoff(history, action):
    # Calculate the average payoff of players who took the given action in the previous round
    pass
```
**Opportunistic Mindset:**

The AO strategy is designed to be opportunistic by:

* Cooperating initially to set a cooperative tone
* Adapting to the actions of others by comparing average payoffs
* Exploiting opportunities to earn higher payoffs by defecting when the average payoff of defectors is higher
* Maintaining a cooperative stance when the average payoffs are equal, to encourage others to cooperate

This strategy is robust to a wide range of opponent behaviors, as it adapts to the game's history and does not rely on specific coordination mechanisms.
'''

description_OPPORTUNISTIC_21 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game, designed to be adaptive and robust to various opponent behaviors:

**Strategy Name: Adaptive Exploitation (AE)**

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C). This sets a positive tone and gathers information about opponents' initial tendencies.
2. **Early Rounds (Rounds 2-5):** Observe opponents' actions and calculate the average cooperation rate (ACR) of the group. If ACR ≥ 0.5, continue to Cooperate (C). Otherwise, Defect (D).
3. **Middle Rounds (Rounds 6-r/2):** Implement a **Tit-for-Tat-like** strategy:
	* If the majority of opponents (≥ n/2) Cooperated (C) in the previous round, Cooperate (C).
	* If the majority of opponents Defected (D) in the previous round, Defect (D).
	* If the opponents' actions were evenly split, mirror the opponent with the highest payoff in the previous round.
4. **Late Rounds (Rounds r/2-r):** Focus on maximizing personal payoff:
	* If k/n × ACR ≥ 1, Cooperate (C), as the potential public good payoff outweighs the private payoff.
	* Otherwise, Defect (D) to secure the private payoff.
5. **Last Round (Round r):** Defect (D), as there's no future opportunity to reciprocate or influence opponents' actions.

**Edge Cases:**

* If the game is very short (r ≤ 5), Cooperate (C) in all rounds, as there's limited opportunity to adapt and exploit.
* If an opponent consistently Cooperates (C) despite being exploited, consider them a **Samaritan** and Cooperate (C) in subsequent rounds to avoid being identified as a **Free Rider**.

**Pseudocode:**
```markdown
# Initialize variables
ACR = 0  # Average Cooperation Rate
opponent_actions = []  # Store opponents' actions for each round
payoffs = []  # Store payoffs for each round

# Round 1: Cooperate
action = C
opponent_actions.append(action)

# Rounds 2-5: Observe and adapt
for round in range(2, 6):
    ACR = calculate_ACR(opponent_actions)
    if ACR >= 0.5:
        action = C
    else:
        action = D
    opponent_actions.append(action)

# Rounds 6-r/2: Tit-for-Tat-like
for round in range(6, r/2):
    majority_action = determine_majority_action(opponent_actions)
    if majority_action == C:
        action = C
    elif majority_action == D:
        action = D
    else:
        action = mirror_highest_payoff(opponent_actions, payoffs)
    opponent_actions.append(action)

# Rounds r/2-r: Maximize personal payoff
for round in range(r/2, r):
    if k/n * ACR >= 1:
        action = C
    else:
        action = D
    opponent_actions.append(action)

# Last Round: Defect
action = D
opponent_actions.append(action)
```
**Opportunistic Mindset:**

The Adaptive Exploitation strategy is designed to be opportunistic, taking advantage of the game's structure and opponents' behaviors to maximize personal payoff. By cooperating initially, the strategy gathers information and sets a positive tone. As the game progresses, the strategy adapts to the group's cooperation rate, exploiting opportunities to defect when the potential public good payoff is low. In the final rounds, the strategy prioritizes personal payoff, defecting when possible to secure the highest payoff.
'''

description_OPPORTUNISTIC_22 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game, which I'll call "Adaptive Opportunism" (AO).

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of 50%. This is an exploratory move to gauge the overall cooperation level and potential opponent strategies.
2. **Reciprocal Cooperation**: If the total number of cooperators in the previous round is greater than or equal to (n/2), cooperate (C) in the current round. This encourages cooperation when there's a strong reciprocal cooperative environment.
3. **Free-Riding Detection**: Monitor the average payoff of all players over the past 3 rounds. If the average payoff is higher than the expected payoff from full cooperation (k/n * n), and the player's own payoff is lower than the average payoff, defect (D) in the current round. This detects potential free-riders and discourages them.
4. **Opportunistic Defection**: If the total number of cooperators in the previous round is less than (n/2), and the player's own payoff in the previous round was higher than the expected payoff from full cooperation, defect (D) in the current round. This takes advantage of low cooperation levels and potentially high payoffs from defection.
5. **Punishment**: If a player's payoff in the previous round was lower than the expected payoff from full cooperation, and the total number of cooperators in the previous round was less than (n/2), cooperate (C) in the current round. This "punishes" the group for low cooperation levels by reducing the player's own payoff.
6. **Random Exploration**: With a probability of 10%, choose a random action (C or D) in each round. This introduces occasional random exploration to adapt to changing opponent strategies.

**Edge Cases:**

1. **Last Round**: In the last round, always defect (D). This is a common convention in repeated games, as there's no future round to reciprocate or cooperate.
2. **Tie-Breaking**: In case of a tie in the decision rules (e.g., when the total number of cooperators is exactly n/2), choose the action with the higher expected payoff.

Pseudocode (for illustration purposes only):
```python
def adaptive_opportunism(n, k, r, history):
    if r == 1:  # First round
        cooperate_prob = 0.5
        action = np.random.choice(['C', 'D'], p=[cooperate_prob, 1 - cooperate_prob])
    else:
        prev_cooperators = sum(history[-1]['actions'] == 'C')
        avg_payoff = np.mean([player['payoff'] for player in history[-3:]])
        player_payoff = history[-1]['payoff']

        if prev_cooperators >= n / 2:
            action = 'C'  # Reciprocal Cooperation
        elif avg_payoff > k / n * n and player_payoff < avg_payoff:
            action = 'D'  # Free-Riding Detection
        elif prev_cooperators < n / 2 and player_payoff > k / n * n:
            action = 'D'  # Opportunistic Defection
        elif player_payoff < k / n * n and prev_cooperators < n / 2:
            action = 'C'  # Punishment
        else:
            action = np.random.choice(['C', 'D'], p=[0.5, 0.5])  # Random Exploration

    return action
```
This Adaptive Opportunism strategy aims to balance cooperation and defection based on the game's history, encouraging cooperation when beneficial and exploiting opportunities for defection when possible.
'''

description_OPPORTUNISTIC_23 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game that only depends on the game parameters and history.

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C). This is a reasonable starting point, as it allows us to observe how others behave and sets a cooperative tone.
2. **Subsequent Rounds (t>1):**
	* If the total payoff from the previous round (π_i,t-1) is greater than or equal to the average payoff of all players in the previous round (avg_π_t-1), cooperate (C). This indicates that the current level of cooperation is beneficial, so we continue to cooperate.
	* Otherwise, defect (D). If our payoff is lower than the average, it suggests that we're not getting a fair share of the public good, so we adapt by defecting.
3. **Adjustment Mechanism:** To ensure we don't get stuck in an unfavorable situation, we introduce an adjustment mechanism. If we've defected for two consecutive rounds and our payoff is still lower than the average, we switch back to cooperating (C). This allows us to re-evaluate the situation and potentially benefit from renewed cooperation.

**Pseudocode:**
```
Initialize: cooperate = True

For each round t:
  If t == 1:
    cooperate = True
  Else:
    If π_i,t-1 >= avg_π_t-1:
      cooperate = True
    Else:
      cooperate = False
      If cooperate was False in round t-1:
        If π_i,t-1 < avg_π_t-1:
          cooperate = True (adjustment mechanism)

  If cooperate:
    Play C
  Else:
    Play D
```
**Edge Cases:**

* **Last Round (t=r):** Since the game is repeated, we can't rely on future interactions to punish or reward opponents. Therefore, we play according to the decision rules above, without any special consideration for the last round.
* **Early Defection:** If an opponent defects early on, we adapt by defecting as well, to avoid being taken advantage of.

**Opportunistic Mindset:**

The Adaptive Exploiter strategy is designed to be opportunistic, as it:

* Exploits cooperation when it's beneficial (i.e., when our payoff is greater than or equal to the average)
* Adapts to defection when cooperation is not paying off
* Re-evaluates the situation after two consecutive rounds of defection, to potentially switch back to cooperation

By being responsive to the game's dynamics and the behavior of others, the Adaptive Exploiter strategy aims to maximize its payoff while minimizing the risk of being exploited.
'''

description_OPPORTUNISTIC_24 = '''
Here's an opportunistic strategy that adapts to the game's history and parameters:

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to test the waters and potentially set a cooperative tone.
2. **Subsequent Rounds (t>1):** Use a combination of recent history and game parameters to decide.
	* Calculate the average payoff of cooperators (APC) and defectors (APD) in the last 2 rounds.
	* If APC > APD, Cooperate (C).
	* If APC ≤ APD, Defect (D).
	* If the number of cooperators in the last round is greater than or equal to k, Cooperate (C).
	* If the number of cooperators in the last round is less than k, Defect (D).
3. **Exception Handling:**
	* If all players defected in the last round, Cooperate (C) in the next round to attempt to restart cooperation.
	* If all players cooperated in the last round, Defect (D) in the next round to exploit the potential for higher payoff.

**Pseudocode:**
```
// Initialize variables
t = 1  // Round counter
APC = 0  // Average payoff of cooperators
APD = 0  // Average payoff of defectors
last_round_coops = 0  // Number of cooperators in last round

// Game loop
while t <= r:
  if t == 1:
    // Initial round, cooperate
    action = C
  else:
    // Calculate APC and APD
    APC = (last_round_coops * k) / n
    APD = 1 + (k/n) * (n - last_round_coops)

    // Decide based on recent history and game parameters
    if APC > APD or last_round_coops >= k:
      action = C
    else:
      action = D

    // Exception handling
    if last_round_coops == 0:
      action = C  // Attempt to restart cooperation
    elif last_round_coops == n:
      action = D  // Exploit potential for higher payoff

  // Update variables for next round
  last_round_coops = count_cooperators()
  t += 1
```
This strategy, Adaptive Opportunism, aims to balance cooperation and exploitation by:

1. Cooperating initially to set a positive tone.
2. Adapting to recent history by comparing the average payoffs of cooperators and defectors.
3. Responding to game parameters, such as the number of cooperators, to inform decisions.
4. Handling edge cases, like all players defecting or cooperating, to attempt to restart cooperation or exploit potential gains.

By being adaptive and responsive to the game's history and parameters, AO should perform well in a tournament against independent strategies.
'''

description_OPPORTUNISTIC_25 = '''
Here's a opportunistic strategy for the N-Player Public Goods Game, which we'll call "Adaptive Exploiter" (AE). AE aims to maximize its payoff by adaptively responding to the behavior of other players, while being robust to various opponent strategies.

**Decision Rules:**

1. **Initial Round (t=1)**: Cooperate (C). This is a neutral starting point, allowing AE to observe the behavior of other players.
2. **Subsequent Rounds (t>1)**:
	* Calculate the average cooperation rate of all players in the previous round (t-1): `avg_coop_t-1 = Σ(c_j,t-1) / n`, where `c_j,t-1` is the cooperation indicator (1 or 0) for player j in round t-1.
	* If `avg_coop_t-1` is greater than or equal to 0.5 (i.e., at least half of the players cooperated), then Cooperate (C) in round t. This indicates that cooperation is relatively common, and AE can benefit from contributing to the public good.
	* If `avg_coop_t-1` is less than 0.5, then Defect (D) in round t. This suggests that cooperation is relatively rare, and AE can exploit the situation by keeping its endowment privately.
3. **Last Round (t=r)**: Defect (D). In the final round, there's no future benefit to cooperating, so AE prioritizes its individual payoff.

**Edge Cases:**

* If all players Defected (D) in the previous round, AE will also Defect (D) in the current round, as there's no incentive to Cooperate (C).
* If all players Cooperated (C) in the previous round, AE will Cooperate (C) in the current round, as the public good is likely to be significant.

**Opportunistic Mindset:**

AE is designed to be opportunistic, as it:

* Adapts to the behavior of other players, responding to changes in the cooperation rate.
* Exploits situations where cooperation is relatively rare, maximizing its individual payoff.
* Cooperates when it's likely to benefit from the public good, aligning with the opportunistic mindset.

Pseudocode:
```python
def AdaptiveExploiter(n, k, r, history):
  if t == 1:  # Initial Round
    return C
  else:
    avg_coop_t-1 = sum([c_j,t-1 for j in range(n)]) / n
    if avg_coop_t-1 >= 0.5:
      return C
    else:
      return D
  if t == r:  # Last Round
    return D
```
This strategy is designed to be robust and adaptive, allowing AE to perform well in a wide range of scenarios.
'''

description_OPPORTUNISTIC_26 = '''
**Opportunistic Strategy: "Adaptive K-Trigger"**

The Adaptive K-Trigger strategy is designed to be a robust and opportunistic approach to the N-Player Public Goods Game. It leverages the game's parameters and history to make adaptive decisions that balance individual payoffs with the potential for collective benefits.

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to set a positive tone and encourage others to contribute to the public good.
2. **Early Rounds (t=2 to r/2):** Implement a **K-Trigger** mechanism:
	* If the average contribution rate of other players in the previous round is above a threshold (k/n), Cooperate (C). This encourages others to maintain their contributions.
	* Otherwise, Defect (D) to prioritize individual payoffs.
3. **Mid-Game Adjustment (t=r/2 to 3r/4):** Introduce a **Defection Threshold** (DT):
	* Calculate the moving average of the total contributions in the previous rounds.
	* If the moving average is below a certain percentage (e.g., 50%) of the maximum possible contributions, increase the Defection Threshold (DT) by 1.
	* Cooperate (C) if the total contributions in the previous round are above the updated DT; otherwise, Defect (D).
4. **Late Rounds (t=3r/4 to r):** Enter **Endgame Mode**:
	* If the game is in its final rounds, focus on maximizing individual payoffs:
		+ Cooperate (C) if the expected payoff from cooperation is higher than defection, based on the previous rounds' contributions.
		+ Defect (D) otherwise.

**Edge Cases:**

* **Last Round (t=r):** Defect (D) to maximize individual payoffs, as there are no future rounds to consider.
* **Single Player or Two-Player Game:** Always Cooperate (C) in a single-player game, as there are no other players to contribute. In a two-player game, implement the K-Trigger mechanism.

**Opportunistic Mindset:**

The Adaptive K-Trigger strategy is designed to be opportunistic by:

* Initially cooperating to encourage others to contribute
* Adapting to the group's behavior and adjusting the Defection Threshold accordingly
* Focusing on individual payoffs in the late rounds, while considering the expected payoffs from cooperation
* Being prepared to defect when the group's contributions are low, to minimize losses

Pseudocode (simplified):
```python
def AdaptiveKTrigger(n, k, r, history):
  # Initial Round
  if t == 1:
    return C

  # Early Rounds
  if t <= r/2:
    avg_contribution = sum(history[t-1]) / n
    if avg_contribution > k/n:
      return C
    else:
      return D

  # Mid-Game Adjustment
  if t <= 3r/4:
    moving_avg = sum(history[t-r/2:t]) / (r/2)
    if moving_avg < 0.5 * n:
      DT += 1
    if sum(history[t-1]) > DT:
      return C
    else:
      return D

  # Late Rounds
  if t > 3r/4:
    expected_coop_payoff = (k/n) * sum(history[t-1])
    if expected_coop_payoff > 1:
      return C
    else:
      return D

  # Last Round
  if t == r:
    return D
```
This strategy is designed to be robust and adaptive, making decisions based on the game's parameters and history. It balances individual payoffs with the potential for collective benefits, making it an opportunistic approach to the N-Player Public Goods Game.
'''

description_OPPORTUNISTIC_27 = '''
**Opportunistic Strategy: "Adaptive Exploiter"**

The Adaptive Exploiter strategy aims to maximize its payoff by adapting to the opponent's behavior and exploiting opportunities for cooperation. The strategy depends only on the game parameters (n, k, r) and the history of the game.

**Decision Rules:**

1. **First Round:** Cooperate (C) in the first round to test the waters and encourage cooperation from others.
2. **Subsequent Rounds:** Use the following decision rules based on the previous round's outcome:
	* If the total number of cooperators in the previous round is greater than or equal to the number of defectors, cooperate (C).
	* If the total number of defectors in the previous round is greater than the number of cooperators, defect (D).
	* If the number of cooperators and defectors is equal, cooperate (C) with a probability proportional to the multiplication factor (k/n) and defect (D) otherwise.
3. **Last Round:** Defect (D) in the last round to maximize individual payoff, regardless of previous outcomes.

**Edge Cases:**

* **Only one opponent:** Always cooperate (C) to maximize joint payoff.
* **Tied game:** If the number of cooperators and defectors is equal, and the game is not in the last round, cooperate (C) with a probability proportional to the multiplication factor (k/n) and defect (D) otherwise.

**Pseudocode:**

```
INPUT: n, k, r, history (previous rounds' actions and payoffs)
OUTPUT: action (C or D)

IF first round THEN
  action = C
ELSE
  prev_cooperators = count of cooperators in previous round
  prev_defectors = count of defectors in previous round
  
  IF prev_cooperators >= prev_defectors THEN
    action = C
  ELSE IF prev_defectors > prev_cooperators THEN
    action = D
  ELSE
    prob_coop = k/n
    action = C with probability prob_coop, D otherwise
  
  IF current round is last round THEN
    action = D
END IF
```

**Opportunistic Mindset:**

The Adaptive Exploiter strategy is designed to capitalize on opportunities for cooperation while minimizing losses from exploitation. By cooperating in the first round and adapting to the opponent's behavior, the strategy encourages cooperation and maximizes joint payoff. However, when faced with a predominantly defecting opponent or in the last round, the strategy prioritizes individual payoff and defects. This opportunistic approach allows the Adaptive Exploiter to thrive in a wide range of environments, from highly cooperative to highly competitive.
'''

description_OPPORTUNISTIC_28 = '''
Here's a opportunistic strategy for the N-Player Public Goods Game:

**Strategy Name:** Adaptive Threshold Cooperator (ATC)

**Decision Rules:**

1. **Initial Round (t=1):** Cooperate (C) to maximize potential public good and observe others' actions.
2. **Subsequent Rounds (t>1):**
	* Calculate the **Cooperation Rate** (CR) in the previous round: CR = (Number of Cooperators in previous round) / n
	* If CR ≥ **Threshold** (TH), Cooperate (C). Otherwise, Defect (D).
	* Update **Threshold** (TH) based on the previous round's payoff: TH = TH + (π_i,t-1 - (1 + (k/n) \* n)) / n
	* **Threshold** (TH) is initialized to 0.5 and adjusted dynamically to balance individual payoff and public good contribution.
3. **Last Round (t=r):** Defect (D) to maximize individual payoff, as there's no future public good benefit.

**Pseudocode:**
```
Initialize TH = 0.5
For each round t:
  If t == 1:
    Cooperate (C)
  Else:
    Calculate CR from previous round
    If CR >= TH:
      Cooperate (C)
    Else:
      Defect (D)
    Update TH based on previous round's payoff
  If t == r:
    Defect (D)
```
**Rationale:**

1. **Initial Cooperation:** Cooperate in the first round to maximize potential public good and observe others' actions.
2. **Adaptive Threshold:** Adjust the **Threshold** (TH) dynamically based on the previous round's payoff. If the individual payoff is high, increase the threshold to encourage more cooperation. If the payoff is low, decrease the threshold to defect more often.
3. **Cooperation Rate:** Use the cooperation rate in the previous round to decide whether to cooperate or defect. If the cooperation rate is high, it's likely that others are contributing to the public good, making cooperation more beneficial.
4. **Defect in Last Round:** Defect in the last round to maximize individual payoff, as there's no future public good benefit.

**Opportunistic Mindset:**

1. **Exploit Cooperation:** ATC takes advantage of high cooperation rates by cooperating and contributing to the public good.
2. **Punish Defection:** ATC defects when the cooperation rate is low, punishing non-cooperative behavior.
3. **Adapt to Changing Environment:** ATC adjusts its **Threshold** (TH) dynamically, allowing it to adapt to changing opponent behaviors and maximize its payoff.

This strategy is designed to be opportunistic, robust, and adaptive, making it a strong contender in the tournament against other AI systems.
'''

description_OPPORTUNISTIC_29 = '''
**Opportunistic Strategy: "Adaptive Explorer"**

The Adaptive Explorer strategy is designed to be opportunistic, adaptive, and robust to a wide range of opponent behaviors. It balances the need to cooperate to achieve high payoffs with the need to defect to protect against exploitation.

**Decision Rules:**

1. **Initial Exploration** (Rounds 1-3): Cooperate (C) to gather information about the opponent's behavior and the potential benefits of cooperation.
2. **Assessing Cooperation Level**: After the initial exploration, calculate the average cooperation level of the opponent(s) over the previous rounds.
	* If the average cooperation level is above a threshold (α = 0.5), cooperate (C) to build on the existing cooperation.
	* If the average cooperation level is below the threshold, defect (D) to protect against exploitation.
3. **Exploiting Defection**: If the opponent(s) defect (D) in a round, defect (D) in the next round to minimize losses.
4. **Punishing Non-Cooperation**: If the opponent(s) do not cooperate (C) in a round after a previous round of cooperation, defect (D) in the next round to signal the importance of cooperation.
5. **Rewarding Cooperation**: If the opponent(s) cooperate (C) in a round after a previous round of cooperation, cooperate (C) in the next round to reinforce the cooperative behavior.

**Handling Edge Cases:**

* **Last Round**: In the last round, defect (D) to maximize individual payoff, as cooperation is no longer necessary.
* **First Round**: Cooperate (C) to initiate cooperation and gather information (as described in the Initial Exploration phase).

**Pseudocode:**
```
Initialize:
  α = 0.5  // cooperation threshold
  rounds = 0
  avg_cooperation = 0

While rounds < r:
  If rounds < 3:  // Initial Exploration
    action = C
  Else:
    avg_cooperation = (sum of opponent's cooperation levels) / (rounds - 1)
    If avg_cooperation > α:
      action = C
    Else:
      action = D

  If opponent's previous action was D:
    action = D  // Exploiting Defection
  ElseIf opponent's previous action was C and previous action was C:
    action = C  // Rewarding Cooperation
  ElseIf opponent's previous action was D and previous action was C:
    action = D  // Punishing Non-Cooperation

  If rounds == r - 1:  // Last Round
    action = D

  Update:
    rounds += 1
    avg_cooperation = (sum of opponent's cooperation levels) / rounds
```
The Adaptive Explorer strategy is designed to be opportunistic, taking advantage of cooperation when possible while protecting against exploitation. By adapting to the opponent's behavior, it aims to maximize payoffs in a wide range of scenarios.
'''

description_OPPORTUNISTIC_30 = '''
**Opportunistic Strategy: "Adaptive Cooperator"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to test the waters and establish a baseline for cooperation.
2. **Subsequent Rounds:**
	* If the total number of cooperators in the previous round is greater than or equal to (n/2), Cooperate (C). This indicates a potential for mutual benefit, and we want to reinforce cooperation.
	* If the total number of cooperators in the previous round is less than (n/2), Defect (D). This suggests that cooperation is not prevalent, and we should prioritize self-interest.
	* If the payoff from the previous round is greater than or equal to (k/n) \* (n/2), Cooperate (C). This indicates that our cooperation was rewarded, and we should continue to cooperate.
	* If the payoff from the previous round is less than (k/n) \* (n/2), Defect (D). This suggests that our cooperation was not sufficiently rewarded, and we should reconsider our strategy.
3. **Last Round:** Defect (D), as there is no future round to influence, and we should prioritize our individual payoff.

**Pseudocode:**
```
def adaptive_cooperator(n, k, r, history):
  if round == 1:
    return C
  else:
    total_cooperators_prev = sum([1 for action in history[-1] if action == C])
    payoff_prev = calculate_payoff(history[-1], n, k)
    if total_cooperators_prev >= n/2 or payoff_prev >= (k/n) * (n/2):
      return C
    else:
      return D
  if round == r:  # Last round
    return D
```
**Opportunistic Mindset:**

Our strategy is designed to be opportunistic, taking advantage of situations where cooperation is likely to be mutually beneficial. By cooperating in the first round, we establish a baseline for cooperation and encourage others to do the same. In subsequent rounds, we adapt to the prevailing behavior, cooperating when it is likely to be rewarded and defecting when it is not. By responding to the total number of cooperators and our own payoff, we remain flexible and responsive to changing circumstances. This strategy is robust to a wide range of opponent behaviors, as it does not rely on specific coordination mechanisms or norms.
'''

description_OPPORTUNISTIC_31 = '''
Here is an opportunistic strategy for the N-Player Public Goods Game that only depends on the game parameters and history:

**Strategy Name:** Adaptive Opportunism (AO)

**Decision Rules:**

1. **First Round:** Cooperate (C) to test the waters and encourage cooperation.
2. **Subsequent Rounds:**
	* If the average payoff of cooperators in the previous round is higher than the average payoff of defectors, Cooperate (C).
	* Otherwise, Defect (D).
3. **Exception:** If the total number of cooperators in the previous round is less than or equal to (n/2), Defect (D). This is to prevent being exploited by a minority of cooperators.

**Pseudocode:**
```
function AO(n, k, history):
  if round == 1:
    return C
  else:
    avg_coop_payoff = sum(pi for pi in history[-1] if ci == 1) / sum(ci for ci in history[-1])
    avg_def_payoff = sum(pi for pi in history[-1] if ci == 0) / sum(1-ci for ci in history[-1])
    if avg_coop_payoff > avg_def_payoff:
      return C
    elif sum(ci for ci in history[-1]) <= n/2:
      return D
    else:
      return D
```
**Rationale:**

* By cooperating in the first round, AO encourages cooperation and sets a positive tone for the game.
* In subsequent rounds, AO adapts to the previous round's payoffs and chooses to cooperate if cooperators fared better. This rewards cooperation and discourages defection.
* The exception rule prevents AO from being exploited by a minority of cooperators, ensuring that AO is robust to a wide range of opponent behaviors.

**Opportunistic Mindset:**

AO is designed to seize opportunities for cooperation while protecting itself from exploitation. By adapting to the game's history, AO can capitalize on cooperation when it is beneficial and defect when it is not. This strategy aligns with the opportunistic mindset, as it prioritizes self-interest while remaining responsive to the game's dynamics.

This strategy is robust to various opponent behaviors and can adapt to different game parameters. It will perform well in a tournament against independent strategies developed by other AI systems.
'''

description_OPPORTUNISTIC_32 = '''
Here's an opportunistic strategy for the N-Player Public Goods Game, which I'll call "Adaptive Opportunism" (AO).

**Decision Rules:**

AO's primary goal is to maximize its own payoff while adapting to the behavior of other players. The strategy is based on the following decision rules:

1. **Initial Cooperation**: In the first round, AO cooperates (plays C). This is a gentle approach to test the waters and encourage others to cooperate.
2. **Reciprocal Cooperation**: If the total number of cooperators in the previous round is greater than or equal to the number of cooperators in the round before that, AO cooperates. This encourages continued cooperation when it's successful.
3. **Exploitation**: If the total number of cooperators in the previous round is less than the number of cooperators in the round before that, AO defects (plays D). This takes advantage of the situation when others are not cooperating.
4. **Punishment**: If AO defected in the previous round and the total number of cooperators increased, AO cooperates. This punishes AO's own exploitation and encourages others to cooperate again.
5. **Risk-Averse**: If the number of rounds remaining (r - t) is less than or equal to 2, AO cooperates. This ensures that AO doesn't risk losing potential payoff in the final rounds.

**Edge Cases:**

1. **Last Round**: In the last round, AO defects. Since there's no future payoff to consider, AO maximizes its immediate payoff.
2. **Ties**: In the event of a tie (e.g., two rounds with the same number of cooperators), AO cooperates. This resolves the tie in favor of cooperation.

**Opportunistic Mindset:**

AO's decision rules are designed to be opportunistic, adapting to the behavior of other players while maximizing its own payoff. By cooperating initially, reciprocating cooperation, and exploiting non-cooperation, AO aims to create an environment where cooperation is rewarded. The punishment mechanism ensures that AO corrects its own exploitation and encourages others to cooperate again.

**Pseudocode:**

Here's a simplified pseudocode representation of AO:
```python
def AdaptiveOpportunism(n, k, r, history):
    if r == 1:  # First round
        return C  # Cooperate

    prev_cooperators = history[-1]['cooperators']
    prev_prev_cooperators = history[-2]['cooperators']

    if prev_cooperators >= prev_prev_cooperators:
        return C  # Reciprocal cooperation
    elif prev_cooperators < prev_prev_cooperators:
        return D  # Exploitation
    elif self.defected_last_round and prev_cooperators > prev_prev_cooperators:
        return C  # Punishment
    elif r - t <= 2:
        return C  # Risk-averse

    return D  # Default: defect
```
Note that this pseudocode is a simplified representation and may require additional implementation details to fully capture the AO strategy.
'''
