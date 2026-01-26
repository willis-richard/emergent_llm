"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: OpenAI
- Model: deepseek/deepseek-r1-distill-llama-70b
"""


description_COLLECTIVE_1 = '''
**Strategy Description: "Adaptive Collective Cooperation"**

1. **First Round: Cooperate**  
   - In the first round, always choose to contribute (C) to encourage initial cooperation and set a positive tone for collective welfare.

2. **Intermediate Rounds (Rounds 2 to r-1): Contribute if Group Contribution Meets Threshold**  
   - For each round after the first and before the last, calculate the total contributions (T) from the previous round.  
   - If the total contributions multiplied by the multiplier k and divided by the number of players n (i.e., (k/n)*T) is at least 1, contribute (C). Otherwise, defect (D).  
   - This ensures that cooperation continues only if the collective benefit from others' contributions justifies the individual sacrifice.

3. **Last Round (Round r): Defect**  
   - In the final round, always choose to defect (D), as there are no future consequences or opportunities for retaliation, maximizing individual payoff.

This strategy is adaptive, robust against various behaviors, and aligns with a collective mindset, fostering cooperation when beneficial and defecting when necessary.
'''

description_COLLECTIVE_2 = '''
The designed strategy for the repeated Public Goods Game is a threshold-based approach that encourages cooperation when the previous round's contributions meet a calculated threshold, ensuring the public good's value is maintained. Here's the step-by-step strategy:

1. In the first round, all players Cooperate (C).
2. In subsequent rounds, each player calculates the total contributions from the previous round (T_prev).
3. Players determine the threshold as T_threshold = n / k.
4. If T_prev > T_threshold, they Cooperate (C) in the current round; otherwise, they Defect (D).

This strategy is adaptive, robust, and collective, aiming to maximize the public good while considering individual incentives.
'''

description_COLLECTIVE_3 = '''
**Strategy Description:**

The strategy is designed to balance individual and collective welfare through reciprocal behavior, leveraging the transparency of past actions in the game. It encourages cooperation while adapting to the group's behavior and addressing edge cases in the first and last rounds.

**1. Decision Rules:**
- **First Round:** Always Cooperate (C) to set a positive example and encourage others to contribute.
- **Subsequent Rounds (2 to r-1):** Mimic the majority's previous action. If the majority contributed, contribute this round. If the majority defected, defect this round.
- **Last Round:** Defect (D) to maximize personal payoff since there are no future consequences.

This approach rewards cooperation when others cooperate and punishes defection, while also addressing the endgame scenario. It is simple, adaptive, and aligned with the collective mindset, aiming to enhance overall group welfare through reciprocal actions.
'''

description_COLLECTIVE_4 = '''
**Strategy Description: Adaptive Forgiving Tit-for-Tat (AF-TFT)**

1. **First Round**: Always Cooperate (C) to initiate cooperation and encourage others to do the same.

2. **Subsequent Rounds**:
   - **Cooperation Check**: Calculate the average cooperation rate of all players from the previous round.
   - **Cooperate**: If the average cooperation rate is above 50%, choose to Cooperate (C).
   - **Defect**: If the average cooperation rate is 50% or below, choose to Defect (D).
   - **Forgiveness Mechanism**: Every 3 rounds, regardless of the cooperation rate, Cooperate once to allow for potential recovery and reset cooperation dynamics.

This strategy promotes collective welfare by rewarding cooperation, punishing defection, and incorporating forgiveness to prevent cycles of mutual defection. It adapts to the group's behavior, encouraging sustained cooperation while remaining robust against exploitation.
'''

description_COLLECTIVE_5 = '''
To design an effective strategy for the Public Goods Game (PGG), we need a collective approach that balances individual incentives with collective welfare. This strategy must adapt to the group's behavior, ensuring robustness against various opponent actions.

### Strategy Description: Adaptive Collective Cooperation (ACC)

1. **Initial Contribution (First Round):**
   - **Action:** Cooperate (Contribute).
   - **Rationale:** Starts with cooperation to encourage a positive group dynamic.

2. **Subsequent Rounds:**
   - **Observation:** After each round, each player observes the group's past contributions.
   - **Contribution Threshold:** Implement a threshold based on the majority rule (greater than 50% contributions in the previous round).
     - **If Threshold Met:** Cooperate in the next round.
     - **If Not Met:** Defect in the next round.

3. **Adaptive Restart Mechanism:**
   - **Periodic Cooperation:** After a sustained period of low contributions (e.g., three consecutive rounds of majority defection), each player has a small probability (e.g., 20%) to cooperate again. This tests the group's willingness to reinitiate cooperation.

4. **Robustness and Fairness:**
   - Each player independently applies the same strategy, fostering a collective mindset aligned with the group's recent behavior. This approach minimizes exploitation by adapting to the group's actions, ensuring fairness and encouraging sustained cooperation.

5. **Parameter Consideration:**
   - The threshold may be adjusted based on the multiplier \( k \) and number of players \( n \). Higher \( k \) values may warrant a higher threshold, while lower \( k \) values may require a lower threshold, reflecting the differing benefits of cooperation.

This strategy promotes cooperation when beneficial, adapts to group dynamics, and includes mechanisms to potentially restart cooperation, ensuring a balance between individual and collective interests.
'''

description_COLLECTIVE_6 = '''
**Strategy Description: Adaptive Cooperative Punishment (ACP)**

**1. Decision Rules:**

- **First Round:** Cooperate (C) by contributing 1 token. This sets a cooperative tone, encouraging others to reciprocate.
- **Middle Rounds:** 
    - Calculate the average cooperation rate of others based on their past actions, excluding the current player.
    - Cooperate (C) if the average cooperation rate is above a threshold (e.g., 50%). If below, Defect (D). This threshold can adapt based on the collective behavior observed.
- **Punishment Mechanism:** If the average contribution in the previous round was below the threshold, Defect (D) in the current round to penalize non-cooperators.
- **Forgiveness:** If others return to Cooperate after a Punishment round, resume Cooperate in subsequent rounds. This allows for re-entry into cooperation.
- **Last Round:** Always Defect (D), as there’s no future punishment to worry about, maximizing personal gain.

**2. Handling Edge Cases:**
- **First Round:** Start with Cooperation to signal willingness to contribute.
- **Last Round:** defect to maximize personal gain when there’s no future impact.
- **Single Round Games:** Since there are multiple rounds, last round rule applies only in the final round.
- **All Defectors:** If all others Defect, the strategy will Defect consistently but may cooperate again if others start contributing.

**3. Collective Mindset:** The strategy aims to maximize collective welfare by encouraging contributions and punishing defection, promoting a balance between cooperation and strategic punishment. It's robust against various behaviors and adapts based on observed actions, fostering a community that can enforce cooperation without assuming prior coordination.

**Pseudocode:**

```
function ACPStrategy(params, history) {
    if (currentRound == 1) {
        return C
    } else if (currentRound == totalRounds) {
        return D
    } else {
        othersActions = history.excludingSelf
        avgContribution = average(othersActions)
        if avgContribution >= threshold {
            return C
        } else {
            return D
        }
    }
}
```

This strategy is designed to be adaptive, balancing cooperation with strategic punishment, ensuring it's robust across various scenarios while maintaining collective welfare.
'''

description_COLLECTIVE_7 = '''
**Strategy Name: Adaptive Tit-for-Tat with Forgiveness (ATTF)**

**Overview:**
ATTF is a dynamic strategy designed for the Public Goods Game, balancing cooperation and defection based on collective behavior. It encourages initial cooperation, adapts to group dynamics, and incorporates forgiveness to sustain cooperation.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (Contribute 1 token).
   - **Rationale:** Initiates cooperation, setting a positive precedent.

2. **Subsequent Rounds:**
   - **Assessment:** Calculate the average contribution rate from the previous round.
   - **Threshold Calculation:** Determine the threshold as (k/n) * 0.5.
   - **Decision:**
     - If the average contribution rate exceeds the threshold, cooperate.
     - Otherwise, defect.
   - **Forgiveness Mechanism:** With a probability of 20%, forgive past defections by cooperating again, preventing perpetual defection cycles.

3. **Last Round:**
   - **Action:** Defect (Contribute 0 tokens).
   - **Rationale:** Maximize personal gain in the absence of future repercussions.

**Robustness and Adaptability:**
- **Forgiveness:** Allows for occasional defections without escalating into mutual defection.
- **Adaptation:** Adjusts based on collective past behavior, encouraging sustained cooperation when beneficial.
- **Final Round Strategy:** Acknowledges the endgame, optimizing immediate payoff without compromising previous cooperation.

This strategy is designed to be robust against diverse opponent behaviors, promoting cooperation while safeguarding against exploitation.
'''

description_COLLECTIVE_8 = '''
**Collective Strategy for Public Goods Game (PGG)**

1. **Initialization**: Begin by contributing (C) in the first round to set a cooperative tone.

2. **Adaptive Cooperation**:
   - **First Round**: Contribute (C) to encourage a cooperative environment.
   - **Subsequent Rounds**: Observe the number of contributors (let’s denote this as C_prev) in the previous round.
     - **Contribute** if C_prev is greater than or equal to a threshold. The threshold is set as half the number of players, i.e., n/2. This encourages reciprocity when a majority contribute.
     - **Defect** (D) if C_prev is below the threshold, signaling retaliation against insufficient contributions.

3. **Reciprocal Adjustment**:
   - After defecting, continuously monitor the number of contributors in subsequent rounds.
   - If contributors (C_prev) meet or exceed the threshold again, switch back to contributing in the next round. This promotes re-cooperation when others resume contributing.

4. **Handling the Last Round**:
   - In the final round, apply the same rule as other rounds—decisions are based solely on the previous round's contributions, maintaining consistency without future consequences affecting the decision.

This strategy is designed to be robust and adaptive, fostering cooperation while retaliating against defection, and remaining open to re-establishing cooperation when others do the same.
'''

description_COLLECTIVE_9 = '''
**Strategy Description:**

**Name:** **Adaptive Collective Cooperation (ACC)**

**Overview:**
The **Adaptive Collective Cooperation (ACC)** strategy is designed for the repeated Public Goods Game (PGG) to balance individual and collective interests. It encourages cooperation while adaptively responding to the group's past behavior, ensuring robustness against diverse opponent actions.

**Decision Rules:**

1. **First Round Cooperation:**
   - **Action:** Cooperate (C).
   - **Rationale:** Initiate cooperation to foster a collective mindset and encourage others to reciprocate.

2. **Subsequent Rounds (Rounds 2 to r-1):**
   - **Adaptive Cooperation:**
     - **Contribution Threshold:** Calculate the total contributions from the previous round.
     - **Rule:** If the total contributions in the previous round were at least **k** (the multiplier), cooperate (C). If the total was less than **k**, defect (D).
     - **Rationale:** This rule incentivizes continuous cooperation by rewarding sufficient contributions and penalizing insufficient ones, maintaining group welfare.

3. **Last Round:**
   - **Action:** Defect (D).
   - **Rationale:** Since the last round lacks future consequences, defecting can maximize individual payoff without jeopardizing future reciprocity.

**Handling Edge Cases:**
- **Initial Cooperation:** Begins with cooperation to set a positive tone.
- **Adaptation:** Uses past contributions to guide future actions, ensuring responsiveness.
- **Endgame Strategy:** Defects in the final round to avoid being exploited when there’s no further opportunity for retaliation.

**Collective Alignment:**
- **Symmetry:** All players follow the same strategy, promoting a uniform approach without requiring coordination.
- **Reciprocity:** Rewards past cooperation and punishes defection, fostering mutual cooperation.

**Robustness:**
- **Forgiveness:** Allows cooperation to resume if the group meets the contribution threshold, preventing endless defection cycles.
- **Adaptability:** Adjusts based on observed contributions, making it resilient against a range of behaviors.

This strategy aims to maximize collective welfare while protecting individual interests, ensuring a balanced approach in the repeated PGG.
'''

description_COLLECTIVE_10 = '''
**Strategy: Adaptive Reciprocity with Threshold**

1. **First Round**: Always Cooperate (C). This sets a cooperative tone and encourages others to follow suit.

2. **Rounds 2 to r-1**:
   - Observe the number of players who Contributed (C) in the previous round.
   - Set a threshold based on the majority (e.g., more than half of the players). This threshold can be adjusted using the multiplier k and the number of players n.
   - If the number of contributors meets or exceeds the threshold, choose to Cooperate.
   - If the number of contributors is below the threshold, Defect (D) to signal dissatisfaction and potentially deter future defection.

3. **Last Round (Round r)**:
   - Follow the same rule as the previous rounds. If the number of contributors in the previous round met the threshold, Cooperate.
   - If not, Defect, as there are no future rounds to influence reciprocity.

This strategy is designed to balance individual and collective interests, promoting cooperation when beneficial and defecting when others do not reciprocate, thus encouraging a fair and adaptive playstyle.
'''

description_COLLECTIVE_11 = '''
1. **Decision Rules**:
   - **First Round**: Always Cooperate (C). Begin by contributing 1 token to establish a cooperative tone.
   - **Subsequent Rounds**:
     - **Contribution Threshold**: Define a threshold \( \theta = \frac{k}{k+1} \).
     - **Average Contribution**: Calculate the average contribution rate \( \bar{c} \) of all players in the previous round.
     - **Action Based on Average Contribution**:
       - If \( \bar{c} \geq \theta \), Cooperate (C).
       - If \( \bar{c} < \theta \), Defect (D) with probability \( p = 1 - \bar{c} \).
   - **Last Round**:
     - Cooperate (C) if the average contribution in the previous round \( \bar{c} \geq \theta \).
     - Defect (D) if \( \bar{c} < \theta \).

2. **Edge Cases**:
   - **First Round**: Always Cooperate.
   - **Last Round**: Adjust based on previous cooperation levels.
   - **Single Player**: Not applicable, as PGG requires multiple players.

3. **Collective Mindset**:
   - Encourages cooperation when beneficial, punishes defection proportionally.
   - Forgives if others start cooperating again.
   - Maintains trust in the final round if cooperation was consistent.

**Strategy Summary**:
- Begin cooperatively to promote a positive group dynamic.
- Use the average contribution to guide decisions, retaliating proportionally to defection.
- Adapt in the final round based on the group's cooperation history to maintain trust or defect as needed.

This approach balances reciprocity and forgiveness, aiming to maximize collective welfare while defending against exploitation.
'''

description_COLLECTIVE_12 = '''
**Strategy: Adaptive Reciprocity**

1. **First Round**: Cooperate by contributing 1 token. This signals a willingness to collaborate and encourages others to do the same.

2. **Subsequent Rounds**:
   - Observe the contributions from all players in the previous round.
   - Count how many players contributed. If the majority (more than half) contributed, Cooperate in the current round.
   - If the majority Defected, then Defect in the current round.

3. **Handling Last Round**: Apply the same rule as other rounds. If the majority contributed in the previous round, Cooperate; otherwise, Defect. Consistency is key to maintaining the collective strategy.

This approach balances reciprocity with adaptability, rewarding cooperation and punishing defection while allowing for forgiveness if the group starts cooperating again.
'''

description_COLLECTIVE_13 = '''
**Strategy: Adaptive Collective Contributions (ACC)**

**1. Initial Cooperation - First Round Contribution:**
   - In the first round, every player contributes by selecting action C. This sets the stage for potential mutual cooperation and maximizes initial collective payoffs.

**2. Reciprocal Social Norm:**
   - From the second round onwards, each player observes the contributions of all players in the previous round.
   - **Unanimous Cooperation:** If all players contributed in the previous round, each player continues to contribute (C).
   - **Partial Defection:** If at least one player defected, each cooperative player defects (D) in the current round. Defectors from the previous round may choose to cooperate if they observe that others are retaliating against their defection.

**3. Forgiveness and Reentry:**
   - If a player observes that all other players defected in the previous round, they defect again (D) in the current round.
   - If a player defects and observes that others cooperated in the previous round, they may choose to cooperate again if they perceive an opportunity to reestablish mutual cooperation.

**4. Final Round Consideration:**
   - In the final round (known in advance), each player defects (D) to maximize individual payoff, anticipating no future repercussions.

**5. Edge Cases Handling:**
   - If all players defect consistently for multiple rounds, each player continues to defect to avoid being the sole contributor.
   - If a player observes that others are cooperating while they defected, they may choose to cooperate again in the next round to realign with the group's strategy.

This strategy balances cooperation with enforcement, aiming to maintain collective welfare while adapting to others' behaviors.
'''

description_COLLECTIVE_14 = '''
The strategy is designed to promote cooperation in the Public Goods Game through reciprocal behavior based on the group's past actions. It starts by
'''

description_COLLECTIVE_15 = '''
**Strategy Name:** Adaptive Cooperative Threshold (ACT)

**Overview:**
ACT is a dynamic strategy designed for the repeated Public Goods Game, promoting collective welfare while adapting to group behavior. It starts cooperatively and adjusts based on the group's recent contribution levels, ensuring robustness against varying opponent behaviors.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C). Contribute 1 token to set a positive standard, encouraging others to reciprocate.

2. **Subsequent Rounds:**
   - **Monitor:** After each round, calculate the average contribution rate of all players from the previous round. This rate is the number of contributors divided by the total number of players.
   - **Determine Next Action:**
     - **High Cooperation (Average ≥ 80%):** Cooperate (C). Continue contributing as the group is highly cooperative.
     - **Moderate Cooperation (50% ≤ Average < 80%):** Cooperate with a 75% probability. This probabilistic approach allows flexibility and avoids being overly exploited.
     - **Low Cooperation (Average < 50%):** Defect (D). Withhold contribution to avoid being a sucker when cooperation is low.

3. **Final Round Handling:**
   - **Adaptive Approach:** Since the strategy doesn't assume knowledge of the last round, it focuses on the ongoing average. However, if the total number of rounds is known, in the final round, defect to maximize personal gain, as future reciprocity isn't possible.

**Collective Mindset:**
ACT aligns with mutual cooperation by rewarding collective effort and responding to group dynamics. It fosters a cooperative environment while protecting against exploitation, ensuring sustainability across rounds.

**Edge Cases Handling:**

- **First Round:** Initiates cooperation to establish trust.
- **Volatile Contributions:** Smoothly adapts to changes in cooperation levels, preventing sudden shifts that could destabilize the group dynamic.
- **Robustness:** The strategy accounts for varied opponent behaviors by adjusting contributions based on observed cooperation rates.

**Description Pseudocode:**

```
Initialize:
    contributions = 0
    total_players = n
    round = 1

While round <= total_rounds:
    If round == 1:
        Contribute 1 token (C)
    Else:
        previous_contributions = total_contributions from last round
        average = previous_contributions / total_players
        
        If average >= 0.8:
            Contribute 1 (C)
        Else If average >= 0.5 and average < 0.8:
            Random probability p = 0.75
            If random(0,1) < p:
                Contribute 1 (C)
            Else:
                Contribute 0 (D)
        Else:
            Contribute 0 (D)
    Increment round
End While
```

**Robustness and Adaptability:**
ACT's adaptive nature allows it to thrive in diverse environments. It encourages cooperation when beneficial and defects to avoid exploitation, ensuring a balance that sustains collective welfare while protecting individual interests.
'''

description_COLLECTIVE_16 = '''
**Strategy Description:**

**Name:** Adaptive Cooperation Strategy (ACS)

**Overview:**
ACS is designed to balance individual and collective interests in a repeated Public Goods Game. It encourages cooperation when the group's recent behavior warrants it, while defecting when cooperation levels drop below a threshold to incentivize better group performance.

**Decision Rules:**

1. **First Round Cooperation:**
   - Always cooperate in the first round to set a cooperative tone and encourage others to follow suit.

2. **Subsequent Rounds:**
   - After the first round, observe the cooperation rate in the previous round.
   - **Cooperate** if at least 50% of the players contributed in the last round.
   - **Defect** if fewer than 50% contributed, serving as a form of punishment to discourage low cooperation.

3. **Edge Cases:**
   - **Last Round Handling:** The strategy remains consistent even in the final round, using the cooperation rate from the penultimate round to decide action. This maintains coherence and avoids last-round exploitation.
   - **All-Defection Scenario:** If all players defect, the strategy defects in the next round, reinforcing the need for mutual cooperation.

**Pseudocode Explanation:**

```
Function play_pgg():
    if current_round == 1:
        contribute 1 token
    else:
        previous_contributions = get previous round contributions
        cooperation_rate = sum(previous_contributions) / number_of_players
        if cooperation_rate >= 0.5:
            contribute 1 token
        else:
            contribute 0 tokens
```

**Collective Alignment:**
This strategy aligns with the collective goal of maximizing group welfare by rewarding recent cooperation and punishing defection, fostering a culture of mutual support.
'''

description_COLLECTIVE_17 = '''
**Strategy: Adaptive Collective Cooperation with Forgiveness (ACCF)**

**Overview:**
ACCF is designed to balance individual incentives with collective welfare in repeated Public Goods Games. It encourages cooperation while adapting to group behavior, ensuring robustness against diverse strategies.

**Decision Rules:**

1. **First Round Cooperation:**
   - Contribute (C) in the first round to establish a cooperative tone.

2. **Subsequent Rounds - Adaptive Contribution:**
   - For each round after the first, examine the number of contributions (C) in the previous round.
   - **Contribution Threshold:** If the number of contributors is more than half of the players, contribute (C) in the current round.
   - **Defection Threshold:** If contributions are half or fewer, defect (D) in the current round to signal dissatisfaction.

3. **Last Round Cooperation:**
   - In the final round, always contribute (C) regardless of past actions to maximize collective payoff.

**Handling Edge Cases:**

- **Forgiveness Mechanism:** If a player has defected in the past but has recently contributed, the strategy allows for cooperation to encourage reform, preventing cycles of defection.
- **Transition Rounds:** Gradually adjust cooperation based on majority behavior, transitioning smoothly between cooperation and defection as needed.

**Collective Alignment:**

- **Synchronized Adaptation:** All players using ACCF will base their decisions on the same observed history, ensuring aligned behavior and encouraging sustainable cooperation.
- **Robustness:** The strategy remains resilient against varying opponent behaviors by adapting based on collective past actions and forgiving recent defectors who reform.

**Implementation:**

- **Pseudocode:**
  ```pseudocode
  function strategy(history, is_last_round):
      if history is empty:
          return C  # First round cooperation
      else:
          # Analyze previous round contributions
          previous_contributions = sum(history[-1])
          total_players = len(history[-1])
          if previous_contributions > total_players / 2:
              current_action = C
          else:
              current_action = D
          # Override for last round
          if is_last_round:
              current_action = C
          return current_action
  ```

**Conclusion:**
ACCF promotes initial cooperation, adapts based on group behavior, and ensures collective welfare in the final round. Its forgiveness mechanism supports recovery from temporary defections, fostering a robust and cooperative environment.
'''

description_COLLECTIVE_18 = '''
**Strategy: Adaptive Cooperation with Forgiveness**

1. **First Round Cooperation**: Always start by contributing (C) in the first round to encourage initial cooperation and set a positive tone.

2. **Mirror Past Contributions**: For each subsequent round (from the second to the penultimate round), observe the average contribution of all players in the previous round. If the average contribution is above 50%, contribute in the current round. If it's 50% or below, defect to signal dissatisfaction and encourage others to cooperate.

3. **Forgiveness Mechanism**: If after defecting, the group's average contribution in the following round exceeds 50%, resume contributing. This allows for recovery of cooperation if others start contributing again.

4. **Final Round Defection**: In the last round of the game, switch to defecting (D) to maximize personal payoff since there are no future consequences or rounds to influence others' behavior.

This strategy balances reciprocity with self-interest, promoting cooperation while adapting to others' actions and safeguarding against exploitation.
'''

description_COLLECTIVE_19 = '''
**Strategy: Cooperative Tit-for-Tat with Reintroduction**

1. **First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Encourages initial group cooperation and sets a positive tone.

2. **Subsequent Rounds:**
   - **Observation:** Review the previous round's average contribution.
   - **Decision Rule:**
     - **If Average Contribution ≥ 0.5:** Contribute (C)
     - **If Average Contribution < 0.5:** Defect (D)
   - **Reintroduction Mechanism:** If the average contribution was below 0.5, check in the next round. If the average rises above 0.5, switch back to Cooperate (C).

3. **Final Round:**
   - **Action:** Cooperate (C) if the average contribution in the previous round was ≥ 0.5; otherwise, Defect (D)
   - **Rationale:** Maximizes payoff based on previous group behavior, rewarding cooperation or defecting as needed.

This strategy is adaptive, robust, and aligns with a collective mindset by fostering cooperation while protecting against exploitation.
'''

description_COLLECTIVE_20 = '''
To address the Public Goods Game (PGG) challenge, the strategy must adapt to others' actions while maintaining a balance between individual and collective interests. Here's a structured approach:

### Strategy: Adaptive Collective Contribution (ACC)

**1. First Round:**
   - **Action:** Contribute (C)
     - **Rationale:** Kickstart cooperation, encouraging others to contribute.

**2. Subsequent Rounds:**
   - **Monitor Contributions:** Track the average contribution rate of all players in the previous round.
   - **Determine Threshold:**
     - **Initial Threshold:** 50% (adjust based on game dynamics).
     - **Adjustment:** Lower threshold if past payoffs are high (indicating successful cooperation); raise it if payoffs are low.
   - **Decision:**
     - If average contribution ≥ threshold, **Contribute (C)**.
     - Else, **Defect (D)**.

**3. Last Round:**
   - **Action:** Defect (D)
     - **Rationale:** Maximize personal payoff as future consequences are absent.

### Pseudocode Example:

```
Initialize:
    threshold = 0.5
    hist_contributions = []
    hist_payoffs = []

For each round from 1 to r:
    if round == 1:
        action = C
    else:
        avg_contribution = sum(hist_contributions[-1]) / n
        if avg_contribution >= threshold:
            action = C
        else:
            action = D

        # Adjust threshold
        avg_payoff = sum(hist_payoffs[-1]) / n
        if avg_payoff > avg_payoff[-2]:
            threshold *= 0.95
        else:
            threshold *= 1.05
            if threshold > 0.8:
                threshold = 0.8

    if round == r:
        action = D

    # Update history
    hist_contributions.append([player.contributions])
    hist_payoffs.append([player.payoffs])

    # Execute action
    play action
```

### Rationale:

- **First Round Contribution:** Starts with cooperation to promote a positive environment.
- **Adaptive Behavior:** Adjusts contributions based on group behavior, fostering cooperation when beneficial.
- **Threshold Adjustment:** Responsive to collective outcomes, optimizing future decisions.
- **Final Round Defection:** Protects against exploitation when there's no future reciprocity.

This strategy is designed to be robust, balancing cooperation with self-interest, and adapting dynamically to the group's behavior.
'''

description_COLLECTIVE_21 = '''
**Strategy Name: Adaptive Collective Cooperation (ACC)**

**Decision Rules:**

1. **First Round:**
   - **Action:** Contribute (C).
   - **Reason:** Initiates cooperation, setting a positive precedent.

2. **Subsequent Rounds (2 to n-1):**
   - **Assessment:** Calculate the average contribution rate from the previous round.
   - **Threshold Check:** If the average is above 50%, contribute (C); otherwise, defect (D).
   - **Forgiveness Mechanism:** Temporarily switch to defection for one round if the average drops below the threshold but revert to cooperation if the average rebounds above the threshold.

3. **Final Round:**
   - **Action:** Defect (D).
   - **Reason:** Maximize personal gain as there are no future repercussions.

**Edge Cases Handling:**

- **All Contributions High:** Continue contributing to maintain collective benefit.
- **Sudden Drop in Contributions:** Defect for one round to signal dissatisfaction, then reassess.
- **Consistent Low Contributions:** Defect to avoid exploitation.

**Alignment with Collective Mindset:**

The strategy promotes cooperation when beneficial and adapts to prevent exploitation. It incentivizes others to contribute by rewarding cooperation and penalizing defection, fostering a balance between individual and collective interests.
'''

description_COLLECTIVE_22 = '''
**Strategy: Adaptive Collective Cooperation (ACC)**

**1. Decision Rules:**
   - **Initial Cooperation:** Start by contributing (C) in the first round to establish a cooperative tone.
   - **Reciprocal Cooperation:** In subsequent rounds, contribute if the majority of players contributed in the previous round. If fewer than half contributed, switch to defecting (D).
   - **Adaptive Threshold:** Adjust the cooperation threshold dynamically. If cooperation levels are high over several rounds, lower the threshold (e.g., require fewer contributors to cooperate). If cooperation is low, raise the threshold.
   - **Forgiveness Mechanism:** After a few rounds of defection, cooperate again if there's a noticeable increase in contributions from others. This prevents perpetual defection cycles.

**2. Handling Edge Cases:**
   - **First Round:** Contribute to foster an initial cooperative environment.
   - **Last Round:** Contribute to encourage end-game cooperation, signaling long-term benefits of collaboration.
   - **Persistent Defectors:** If a subset of players consistently defect, maintain defection for a few rounds then attempt cooperation again, allowing for potential behavior change.

**3. Collective Alignment:**
   - The strategy promotes group welfare by rewarding collective cooperation and punishing widespread defection. It encourages reciprocal behavior, adapting based on group dynamics to sustain cooperation.

This strategy balances individual incentives with collective good, adapting to group behavior while maintaining robustness against varied opponent actions.
'''

description_COLLECTIVE_23 = '''
**Collective Strategy for Repeated Public Goods Game: "Majority Cooperation"**

**1. Decision Rules:**
   - **First Round:** All players Cooperate (C) to establish cooperation.
   - **Subsequent Rounds:** Each player decides to Cooperate or Defect based on the previous round's contributions.
     - **Cooperate** if a majority (> n/2) of players Contributed in the previous round.
     - **Defect** otherwise.

**2. Handling Edge Cases:**
   - **First Round:** Always Cooperate to initiate a cooperative tone.
   - **Last Round:** Apply the same decision rule as other rounds, using the previous round's contributions to decide, ensuring consistency.

**3. Collective Mindset:**
   - Encourages cooperation when a majority contributes, fostering collective welfare.
   - Defects only when a majority defects, preventing exploitation and maintaining fairness.

**Pseudocode:**
```
def strategy(game_params, history):
    n = game_params['n']
    r = game_params['r']
    round = history.current_round
    
    if round == 1:
        return 'C'
    else:
        previous_round = history.get_round(round-1)
        contributions = [action for action in previous_round if action == 'C']
        c_prev = len(contributions)
        threshold = n // 2 + 1  # Majority threshold
        if c_prev >= threshold:
            return 'C'
        else:
            return 'D'
```

**Summary:**
This strategy promotes sustained cooperation by mirroring the majority's behavior, adaptively responding to the group's contributions, and robustly handling various opponent behaviors while maintaining fairness and encouraging collective welfare.
'''

description_COLLECTIVE_24 = '''
To address the Public Goods Game, I propose a strategy that balances cooperation and self-interest, adapting to group behavior while considering the game's parameters.

**Strategy: Adaptive Collective Cooperation**

1. **First Round:** Start by Cooperating (C) to set a cooperative tone and encourage others to contribute.

2. **Last Round:** Defect (D) to maximize personal gain, as there are no future consequences.

3. **Middle Rounds:**
   - Calculate the average contribution of all players from the previous round.
   - Determine the cooperation probability as `(average contribution) * (k / (n - 1))`, where `k` is the multiplier and `n` is the number of players. This scaling adjusts responsiveness based on the group's size and the return on contributions.
   - Cooperate with the calculated probability; otherwise, Defect.

This strategy promotes initial cooperation, rewards past contributions, and adapts based on group behavior, ensuring a balance between collective welfare and individual payoff.
'''

description_COLLECTIVE_25 = '''
**Strategy: Adaptive Collective Cooperation**

**1. Decision Rules:**
   - **First Round:** Cooperate by contributing 1 token.
   - **Subsequent Rounds:** Observe the number of players who contributed in the previous round. If at least (k - 1) players contributed, cooperate again by contributing 1 token. Otherwise, defect by contributing 0 tokens.

**2. Handling Edge Cases:**
   - **First Round:** Always cooperate to establish a cooperative precedent.
   - **Last Round:** Apply the same rule as other rounds, relying on the previous round's contributions to decide. This discourages unraveling of cooperation due to the end of the game.
   - **Low Contribution Rounds:** If insufficient contributions occurred in the previous round, defect to signal the need for higher cooperation.

**3. Collective Mindset:** 
   - The strategy encourages cooperation when others are contributing sufficiently, leveraging reciprocity to sustain collective welfare. It adapts based on the group's behavior, promoting a balance between individual and collective incentives.

This approach fosters cooperation by rewarding past contributions while deterring exploitation, ensuring robustness against various opponent behaviors.
'''

description_COLLECTIVE_26 = '''
### Strategy: Adaptive Cooperation with Forgiveness (ACF)

**Overview:**
ACF aims to maximize collective welfare by encouraging cooperation while protecting against exploitation. It adapts based on past behavior and includes forgiveness to reset cooperation when others change their tactics.

**Decision Rules:**

1. **First Round Cooperation:**
   - Contribute (C) in the first round to establish cooperation.

2. **Past Behavior Assessment:**
   - After each round, calculate the average cooperation rate of all players over a moving window of the last few rounds (e.g., 3 rounds).

3. **Adaptive Cooperation:**
   - If the cooperation rate is **above 75%**, cooperate (C) in the next round.
   - If the cooperation rate is **between 50% and 75%**, choose an action based on the average contribution of the group in the previous round.
   - If the cooperation rate is **below 50%**, defect (D) in the next round.

4. **Forgiveness Mechanism:**
   - If you defected in the previous round but observe an increase in the cooperation rate, cooperate (C) in the current round.
   - If the cooperation rate stays low after defecting, continue defecting (D).

5. **Final Round Handling:**
   - Cooperate (C) in the final round if the overall cooperation rate has been sufficiently high throughout the game.
   - Defect (D) if the cooperation rate has been low, protecting against end-game exploitation.

**Edge Cases:**

- **First Round:** Always contribute to encourage initial cooperation.
- **Last Round:** Use overall cooperation history to decide, promoting fairness even at the end.
- **Sudden Changes:** Quickly adapt by assessing recent cooperation rates, allowing the strategy to adjust to new behaviors.

**Collective Mindset:**
This strategy aligns all players to mutually beneficial outcomes by reciprocating cooperation and defending against frequent defection, ensuring sustainability and fairness in the game.
'''

description_COLLECTIVE_27 = '''
**Strategy Name: Adaptive Contributor**

**Description:**

The Adaptive Contributor strategy is designed for the repeated Public Goods Game (PGG) to balance individual and collective welfare through adaptive cooperation. It begins with cooperation and adjusts based on the group's past behavior, promoting fairness and discouraging exploitation.

**Decision Rules:**

1. **First Round:** Always contribute (C). This initializes cooperation, encouraging mutual contribution from the start.

2. **Subsequent Rounds (2 to r):** 
   - Calculate the average contribution from all players in the previous round.
   - If the average contribution was 0.5 or higher, contribute (C).
   - If the average was below 0.5, defect (D). This rule rewards previous cooperation and punishes widespread defection.

3. **Last Round (r):** Apply the same rule as other rounds, basing the decision on the average contribution from round r-1. This ensures consistency and doesn't allow end-game exploitation.

**Edge Case Handling:**

- **Single Round:** Contribute, fostering cooperation without prior information.
- **All Defection:** If others defect, the strategy defects in subsequent rounds, preventing exploitation.
- **High Multiplier (k):** While the strategy doesn't adjust based on k, higher k may naturally encourage contribution due to greater returns.

**Collective Alignment:**

By basing decisions on group behavior, the strategy promotes collective welfare. It incentivizes others to cooperate by rewarding past contributions, yet adapts to defection by reducing vulnerability, thus maintaining a balance between cooperation and self-interest.
'''

description_COLLECTIVE_28 = '''
**Strategy: Adaptive Contribution Based on Past Performance**

1. **First Round**: Cooperate (C) by contributing 1 token to encourage initial cooperation and establish a collective commitment.

2. **Subsequent Rounds**:
   - **Calculate the Total Contributions (T)** from the previous round.
   - **Determine the Threshold**: Compute the minimum total contributions required, which is \( \frac{n}{k} \). This threshold represents the point where contributing yields a net gain for each player.
   - **Decision Rule**:
     - If the previous round's total contributions (T) meet or exceed the threshold (\( T \geq \frac{n}{k} \)), contribute (C) in the current round.
     - If the previous round's total contributions (T) are below the threshold, defect (D) in the current round.

**Rationale**:
- **First Round**: Starting with cooperation sets a positive precedent and encourages others to follow suit.
- **Subsequent Rounds**: The strategy adapts based on collective past behavior. By using the threshold \( \frac{n}{k} \), it ensures that contributing is individually beneficial only when enough players have contributed in the past, promoting sustainability of cooperation.
- **Edge Cases**: The strategy handles the first round with initial cooperation and adapts in the last round based on prior contributions, aligning with the collective mindset without assuming coordination.

This approach encourages cooperation when beneficial and adaptively adjusts, providing a robust and collective strategy for the Public Goods Game.
'''

description_COLLECTIVE_29 = '''
**Strategy: Adaptive Cooperative PGG Strategy**

1. **Initial Contribution (Round 1):**
   - Cooperate (C) in the first round to establish a cooperative tone.

2. **Adaptive Contribution Rule:**
   - After the first round, calculate the average contribution of all players in the previous round.
   - If the average contribution is above 50%, contribute (C).
   - If the average is 50% or below, choose to defect (D).

3. **Sole Contributor Check:**
   - If the strategy detects that it is the sole contributor for two consecutive rounds, switch to defecting (D) to avoid exploitation.

4. **Progressive Cooperation:**
   - If the average contribution increases over two consecutive rounds, increase the player's contribution probability by 10%.
   - If the average decreases, decrease the contribution probability by 10%.

5. **Exploration Phase:**
   - Every fifth round, randomly select to contribute (C) with a probability of 20% to test others' responsiveness.

6. **Final Round Handling:**
   - In the last round, if the average contribution throughout the game is above 50%, contribute (C).
   - If below 50%, defect (D).

This strategy encourages cooperation by mirroring others' behavior, adapts to group dynamics, avoids exploitation, and includes exploration to sustain cooperation, ensuring robust performance in various scenarios.
'''

description_COLLECTIVE_30 = '''
**Collective Strategy for Public Goods Game (PGG)**

**1. Decision Rules:**
- **First Round:** Always Cooperate (C). This sets a positive tone and encourages initial contributions.
- **Subsequent Rounds:** After the first round, observe the total contributions (sum of c_j) from all players in the previous round.
  - If the number of contributors (sum c_j) is at least half of the total number of players (n/2), Cooperate (C) in the current round.
  - If the number of contributors is less than half, Defect (D) to sanction low contributions and incentivize cooperation.

**2. Handling Edge Cases:**
- **First Round:** Contribute to establish a cooperative environment.
- **Last Round (if known):** If the number of rounds (r) is known and it's the final round, Defect. This is because there are no future consequences, so individual payoff is prioritized.
- **Unknown Number of Rounds:** Continue using the same strategy withoutspecial treatment for any round, ensuring timeless adaptability.

**3. Collective Mindset:**
- The strategy is designed to be adopted uniformly by all players, promoting a shared approach to reciprocity. It rewards cooperation when sufficient contributors are present and sanctions when contributions drop below a socially beneficial threshold.

This strategy balances cooperation and punishment, encouraging sustained contributions while adapting to the group's behavior. It is robust, as it does not rely on communication or prior coordination, making it suitable for a tournament setting against varied opponents.
'''

description_COLLECTIVE_31 = '''
**Strategy: Adaptive Contribution Based on Threshold (ACBT)**

**Overview:**
ACBT is designed to balance individual and collective incentives in repeated Public Goods Games. It encourages cooperation by rewarding past contributions while protecting against exploitation by defectors. The strategy adapts based on previous rounds' outcomes and handles edge cases like the first and last rounds.

**Decision Rules:**

1. **First Round:**
   - Contribute (C). This sets a cooperative tone, encouraging others to follow suit.

2. **Subsequent Rounds:**
   - **Assess Past Contributions:** Count the number of players who contributed in the previous round.
   - **Threshold Check:** If the number of contributors is at least k (the multiplier), contribute (C). This incentivizes continued cooperation when a sufficient number of players are contributing.
   - **Defect if Below Threshold:** If contributions were below k, defect (D) to avoid being exploited and signal the need for higher cooperation.

3. **Last Round:**
   - Defect (D). Since there are no future interactions, individuals maximize their payoff without affecting others' future decisions.

**Edge Cases:**
- **First Round:** Always start with cooperation to initiate a positive dynamic.
- **Last Round:** Defect to maximize immediate payoff with no repercussions.

**Collective Alignment:**
This strategy aligns with a collective mindset by rewarding group cooperation and deterring widespread defection. It fosters a mutually beneficial environment when enough players cooperate, while protecting individuals when others are defecting.

**Robustness:**
ACBT is robust against varying behaviors because it adapts based on observed contributions. It balances reciprocity and self-interest, making it effective across diverse opponent strategies.

---

**Pseudocode:**

```
function ACBT(n, k, history):
    if history is empty:
        contribute = True
    else:
        last_round = history[-1]
        contributors = count_of_contributions(last_round)
        if contributors >= k:
            contribute = True
        else:
            contribute = False
    if it is the last round:
        contribute = False
    return contribute ? C : D
```

This strategy promotes cooperation while safeguarding against exploitation, ensuring a balance between individual and collective welfare throughout the game.
'''

description_COLLECTIVE_32 = '''
**Collective Strategy for Public Goods Game (PGG)**

1. **First Round**: Always contribute (C). This initiates cooperation, encouraging others to reciprocate.

2. **Subsequent Rounds**:
   - **Not the Last Round**: Evaluate the total contributions from the previous round. If the payoff from contributing (i.e., (k/n)*sum of contributions) was beneficial (greater than or equal to 1), continue to contribute (C). Otherwise, defect (D).
   - **Last Round**: Defect (D), as there are no future consequences to influence.

3. **Threshold Determination**: Use the previous round's total contributions to assess the benefit of cooperation. Contribute if the previous round's total contributions multiplied by (k/n) is at least 1, indicating that contributing was worthwhile.

This strategy promotes mutual cooperation while adapting to the group's behavior, ensuring robustness against defectors and optimizing collective welfare.
'''

description_COLLECTIVE_33 = '''
Here's a natural language description of a robust, adaptive strategy for the repeated Public Goods Game:

---

**Strategy Name:** *Optimistic Reciprocation with Endgame Discounting (ORED)*

### 1. Decision Rules:
#### First Round:
- **Action:** Cooperate (C). Start by contributing to the public good to signal willingness to collaborate and maximize first-round collective payoffs.

#### Middle Rounds:
- **Adaptive Contribution Rule:**  
   - After the first round, calculate the **cooperation rate** of all players in the previous round (i.e., the number of players who contributed divided by n).  
   - Let *threshold* = (k / n). If the cooperation rate in the previous round is above this threshold, Cooperate (C); otherwise, Defect (D).  
   - This ensures that you only contribute if enough others are also contributing to make it beneficial for the group.

#### Last Round:
- **Action:** Defect (D). In the final round, defect to maximize your individual payoff, as there is no future punishment to fear.

### 2. Edge Cases:
- **First Round:** Always Cooperate (C), as described above.  
- **Last Round:** Always Defect (D), as described above.  
- **All-Defector Histories:** If all other players defected in the previous round, defect in the current round to avoid exploitation.  
- **All-Cooperator Histories:** If all other players cooperated in the previous round, cooperate in the current round to sustain cooperation.

### 3. Collective Alignment:
This strategy aligns with the collective mindset by:  
- Supporting cooperation when enough others are cooperating (above the threshold).  
- Punishing chronic defectors by withholding contributions.  
- Maximizing individual and collective payoffs in early rounds while safeguarding against exploitation in the endgame.

---

This strategy balances cooperation and self-interest, making it robust against free-riders while promoting collective welfare when possible.
'''

description_COLLECTIVE_34 = '''
**Strategy Description: Adaptive Collective Cooperation with Selective Retaliation**

**1. Decision Rules:**

- **First Round:** Cooperate (C) unconditionally. This sets an initial cooperative tone.
  
- **Subsequent Rounds:** 
  - If ≥90% of players cooperated in the previous round, Cooperate (C) again.
  - If <90% but ≥50% cooperated, Cooperate (C) only if your contribution would increase the total public good.
  - If <50% cooperated, Defect (D) in this round as a form of punishment.

**2. Handling Edge Cases:**

- **First Round:** Always Cooperate (C) to establish trust and cooperation norms.
  
- **Last Round:** Cooperate (C) regardless of previous actions to maximize collective payoff, acknowledging no future retaliation.

**3. Collective Mindset:**

The strategy prioritizes group welfare by encouraging cooperation and using defection as a selective retaliatory measure. It forgives past defections if a majority cooperate, aiming for long-term mutual benefit without strict punishment.

This strategy is adaptive, adjusting based on group behavior, and robust against various opponent strategies, promoting collective success.
'''

description_COLLECTIVE_35 = '''
**Collective Strategy for Public Goods Game (PGG)**

1. **Initial Round (Round 1):**
   - **Action:** Contribute (C)
   - **Rationale:** Cooperate to set a positive tone and encourage others to follow suit.

2. **Subsequent Rounds:**
   - **Action:** Observe the average contribution rate of all players in the previous round.
   - **Decision Rule:**
     - If the average contribution is above 50%, Contribute (C).
     - If the average contribution is 50% or below, Defect (D).

3. **Handling Individual Defectors:**
   - Monitor each player's contribution history.
   - If any player has never contributed (always Defected), switch to Defect (D) in subsequent rounds.

4. **Final Round:**
   - **Action:** Contribute (C) if the average contribution in the previous round was above 50%.
   - **Alternative:** Defect (D) if the average contribution was 50% or below.

**Strategy Overview:**
This strategy is adaptive, adjusting based on group behavior, and robust by addressing both collective and individual actions. It promotes cooperation through reciprocity and reciprocity-based penalties, encouraging a collective mindset to maximize payoffs while minimizing exploitation.
'''

description_COLLECTIVE_36 = '''
**Public Goods Game Strategy: Adaptive Reciprocity**

**Objective:** To design a collective strategy that balances individual incentives with collective welfare, adapting based on the group's behavior.

**Strategy Description:**

1. **Initial Cooperation:**
   - **First Round:** Always Cooperate (Contribute) to set a positive tone and encourage cooperation.

2. **Adaptive Decision-Making:**
   - **Subsequent Rounds:** After the first round, calculate the average contribution rate of all players from the previous round.
   - **Threshold (t):** Determine a threshold based on game parameters where \( t = \frac{k}{n} \). This represents the minimum average contribution needed for cooperation to be beneficial.
   - **Decision Rule:** If the average contribution in the previous round exceeds \( t \), Cooperate in the current round. Otherwise, Defect.

3. **Grace Period for Re-entry:**
   - **After Defection:** If you Defected in the previous round, periodically revert to Cooperation (e.g., every few rounds) to test if the group's behavior has improved.

4. **Final Round Consideration:**
   - **Last Round:** Cooperate if the group's average contribution has been above \( t \) in preceding rounds, signaling commitment to collective welfare. Otherwise, Defect to maximize immediate payoff.

**Rationale:**
- **Initial Cooperation:** Encourages others to cooperate and maximizes collective welfare from the start.
- **Threshold-Based Adaptation:** Ensures cooperation is conditional on the group's contribution levels, preventing exploitation.
- **Grace Period:** Allows re-entry into cooperation if the group dynamic improves, fostering resilience.
- **Final Round Strategy:** Balances between contributing for collective good and self-interest, depending on the group's past behavior.

This strategy promotes sustained cooperation when beneficial while adapting to protect against exploitation, making it robust in various competitive settings.
'''

description_COLLECTIVE_37 = '''

'''

description_COLLECTIVE_38 = '''
**Public Goods Game Strategy: "Adaptive Collective Cooperation"**

**Overview:**
This strategy aims to balance individual incentives with collective welfare through adaptive cooperation, encouraging contributions while preventing exploitation.

**Components of the Strategy:**

1. **Initial Cooperation:**
   - **First Round:** Contribute 1 token (C) to set a cooperative tone.

2. **Mirroring Group Behavior:**
   - **Subsequent Rounds:** Observe the group's average contribution from the previous round.
     - If the average exceeds a dynamic threshold, contribute (C).
     - If below, defect (D).

3. **Dynamic Threshold Adjustment:**
   - **Threshold:** Starts at 0.5 (50% contribution rate) and increases gradually as rounds progress.
     - This reflects higher expectations for contributions as the game progresses.

4. **Endgame Handling:**
   - **Last Few Rounds:** Gradually reduce cooperation one round before the end to avoid exploitation.
     - Decrease the likelihood of contributing as the final round approaches.

**Rationale:**
- **Initial Contribution:** Encourages a cooperative starting point.
- **Mirroring:** Adapts strategy based on collective behavior, rewarding cooperation and penalizing defection.
- **Dynamic Threshold:** Ensures responsiveness to changes in group behavior, maintaining robustness against varying strategies.
- **Endgame Adjustment:** Mitigates endgame exploitation by tapering cooperation before the last round.

**Conclusion:**
This strategy promotes sustained cooperation by leveraging observable past actions, adapting to group dynamics, and safeguarding against endgame exploitation.
'''

description_COLLECTIVE_39 = '''
**Strategy Name:** Adaptive Cooperative Threshold (ACT)

**Strategy Description:**

1. **First Round Action:**
   - Cooperate (C). Contribution = 1.
   - Rationale: Begin with cooperation to establish a norm of contribution.

2. **Subsequent Rounds:**
   - Observe the previous round's contributions.
   - Calculate the proportion of players who Cooperated.
   - If the proportion of Cooperators is greater than 50%, Cooperate (C).
   - Otherwise, Defect (D).

3. **Last Round Action:**
   - Always Cooperate (C). Contribution = 1.
   - Rationale: Maximize collective welfare even without future repercussions.

**Pseudocode:**

```
function act_strategy(history, is_last_round):
    if not history:  # First round
        return 1  # Cooperate
    else:
        prev_contributions = history[-1]
        coop_rate = sum(prev_contributions) / len(prev_contributions)
        if is_last_round:
            return 1  # Cooperate
        elif coop_rate > 0.5:
            return 1  # Cooperate
        else:
            return 0  # Defect
```

This strategy encourages initial cooperation, adapts based on others' behavior, and maintains cooperation in the final round to uphold collective welfare.
'''

description_COLLECTIVE_40 = '''
**Strategy Description: Adaptive Cooperation with Endgame Defection**

1. **First Round:** Cooperate by contributing 1 token to establish an initial cooperative tone.

2. **Rounds 2 to r-1:**
   - **Cooperate** if the average contribution from all players in the previous round is at least 0.5. This encourages continued cooperation when there is significant group contribution.
   - **Defect** if the average contribution was below 0.5, responding to insufficient group cooperation by withholding contribution.

3. **Last Round (Round r):** Always defect, as there is no future punishment to fear, aligning with the expectation that others may also defect.

This strategy balances cooperation with adaptive responses to group behavior and strategically defects in the endgame to maximize individual payoff.
'''

description_COLLECTIVE_41 = '''
The proposed strategy for the Public Goods Game is designed to be adaptive, promoting cooperation while being robust against free-riders. It uses the majority's previous actions to decide the current move, fostering a collective approach.

**Strategy Description: Majority-Match**

1. **First Round**: Cooperate. This sets a cooperative tone.
2. **Subsequent Rounds**: In each round, observe the number of players who Cooperated in the previous round.
   - If the majority (over 50%) Cooperated, then Cooperate in the current round.
   - If the majority Defected, then Defect in the current round.
3. **Edge Cases Handling**: The strategy automatically manages first and last rounds by following the same rule, ensuring consistency without special treatment for the last round.

This strategy aligns with the collective mindset by mirroring the group's behavior, encouraging sustained cooperation while defending against exploitation.
'''

description_COLLECTIVE_42 = '''
**Strategy Description: Conditional Cooperation with Gradual Escalation**

1. **Initial Cooperation**: Begin the game by cooperating (C). This sets an optimistic tone and encourages others to contribute.

2. **Contribution Monitoring**: After each round, assess the contributions of all players. Count how many contributed in the previous round.

3. **Cooperation Continuation**: If at least half of the players contributed in the previous round, continue cooperating (C). This incentivizes sustained collective effort.

4. **Moderate Punishment**: If less than half contributed in the previous round, defect (D) once to signal dissatisfaction and encourage others to increase their contributions.

5. **Escalated Punishment**: If contributions remain insufficient after the first defection, defect (D) a second time to intensify the signal. This step is a stronger deterrent against persistent non-cooperation.

6. **Forgiveness Mechanism**: If, after defecting, other players increase their contributions, revert to cooperating (C). This forgiveness encourages resumption of cooperation.

7. **Endgame Cooperation**: In the final round, continue cooperating (C) to maintain the collective mindset, emphasizing the importance of cooperation even without future consequences.

This strategy is designed to be adaptive, punished appropriately, yet forgiving, fostering a balance between individual and collective welfare. It encourages cooperation while deterring exploitation, ensuring robustness against various behaviors.
'''

description_COLLECTIVE_43 = '''
**Strategy Description: Adaptive Group Reciprocity**

**Objective:** To maximize collective welfare while safeguarding against exploitation by adapting cooperation based on group behavior.

**Rules:**

1. **Initial Cooperation:**
   - In the first round, contribute 1 token (C). This sets a cooperative tone and encourages initial group investment in the public good.

2. **Adaptive Cooperation:**
   - For each subsequent round, observe the number of players who contributed in the previous round.
   - If more than half of the players cooperated in the previous round, contribute 1 token in the current round.
   - If half or fewer cooperated, defect by contributing 0 tokens.

3. **Final Round Defection (if applicable):**
   - If the game has a known final round, defect by contributing 0 tokens in that round to maximize individual payoff, as future reciprocity is no longer a factor.

**Rationale:**

- **Adaptive Nature:** The strategy dynamically adjusts based on the group's past behavior, promoting cooperation when it is prevalent and protecting against exploitation when it is not.
- **Simplicity and Observability:** The decision-making process relies solely on observable past actions, making it feasible without prior coordination or communication.
- **Collective Welfare Focus:** By contributing when the group cooperates, the strategy supports the public good, ensuring shared benefits while minimizing the risk of being exploited.

This strategy encourages sustained cooperation through reciprocal behavior, responsive to the collective actions of the group, thus balancing individual and collective interests effectively.
'''

description_COLLECTIVE_44 = '''
1. **Initial Cooperation**: In the first round, always choose to Cooperate (C). This sets a cooperative tone and establishes a basis for reciprocity.

2. **Contribution Threshold**: For each subsequent round, examine the number of players who Cooperated (C) in the previous round:
   - If at least half of the players Cooperated, choose to Cooperate in the current round.
   - If fewer than half Cooperated, choose to Defect (D).

3. **Final Round Exception**: In the last round of the game, always choose to Defect (D) to maximize personal payoff without concern for future repercussions.

This strategy encourages initial cooperation, adapts based on collective behavior, and protects against exploitation by others. It promotes reciprocity while ensuring self-interest is safeguarded in the final round.
'''

description_COLLECTIVE_45 = '''

'''

description_COLLECTIVE_46 = '''
Start by cooperating in the first round to encourage initial trust. For each subsequent round, contribute if the majority of players contributed in the previous round; otherwise, defect. This strategy adaptively aligns with the group's behavior, promoting sustained cooperation while being robust against defection.

**Strategy:**

1. **First Round:** Contribute (C) to set a cooperative tone.
2. **Subsequent Rounds:** 
   - Observe the number of contributors in the previous round.
   - If the majority contributed (more than half), contribute (C).
   - If the majority defected, defect (D).
3. **Edge Cases:** No special handling needed for the last round; decisions remain based on the previous round's contributions.

This approach fosters initial cooperation and adapts based on the group's recent behavior, aiming to maximize collective welfare while being resilient to varying levels of cooperation.
'''

description_COLLECTIVE_47 = '''
**Strategy Description:**

The strategy, named "Adaptive Collective Cooperation," is designed to balance individual and collective interests in repeated Public Goods Games. It encourages initial cooperation, adapts based on group behavior, and makes an individually optimal decision in the final round.

1. **First Round:** Cooperate (C) to establish a foundation of trust and maximize initial collective payoff.

2. **Subsequent Rounds (2 to r-1):**  
   - Observe the majority action (contribute or defect) from the previous round.  
   - Cooperate in the current round if the majority contributed (C) in the previous round.  
   - Defect if the majority defected (D).  
   This creates a reciprocal behavior, encouraging continued cooperation if others are contributing and adjusting if others defect.

3. **Final Round (r):** Always defect (D) to maximize individual payoff without future repercussions, as there are no subsequent rounds to influence others' actions.

This strategy is adaptive, robust, and collective, aligning actions with group behavior while addressing edge cases effectively.
'''

description_COLLECTIVE_48 = '''
**Strategy Description: Adaptive Collective Cooperation (ACC)**

**Overview:**
The Adaptive Collective Cooperation (ACC) strategy is designed for the repeated Public Goods Game (PGG). It promotes cooperation by considering the collective behavior of all players, adapting decisions based on the majority's past actions. This strategy balances individual incentives with collective welfare, ensuring robustness against various opponent behaviors.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Rationale:** Initiates a cooperative tone, encouraging others to contribute.

2. **Subsequent Rounds (Rounds 2 to r):**
   - **Action:** 
     - Cooperate (C) if the majority (more than 50%) of players contributed in the previous round.
     - Defect (D) if 50% or fewer contributed in the previous round.
   - **Rationale:** Adapts based on the group's recent behavior, rewarding cooperation and retaliating against widespread defection.

3. **Last Round:**
   - **Action:** Follows the same rule as other rounds, cooperating if the majority contributed in the penultimate round.
   - **Rationale:** Maintains consistency, encouraging sustained cooperation even in the final round.

**Edge Cases Handling:**
- If all players defect initially, ACC will switch to defection after the first round.
- If only a few defect, ACC adapts based on the majority, potentially switching strategies to maintain fairness.

**Collective Mindset:**
ACC aligns with a collective mindset by focusing on group behavior rather than individual actions, promoting cooperation when beneficial and adapting when necessary. It's simple, observable, and responsive, ensuring a balance between individual and collective interests.
'''

description_COLLECTIVE_49 = '''
**Strategy Description:**

1. **First Round:** All players contribute (C). This initial cooperation sets the stage for potential collective benefit and encourages others to follow suit.

2. **Subsequent Rounds:** Each player calculates the total contributions from the previous round. If the total meets or exceeds the threshold (total >= n/k), where n is the number of players and k is the multiplier, the player contributes (C). If the total is below this threshold, the player defects (D).

3. **Last Round Consideration:** The strategy continues as described, even in the final round, ensuring consistency without assuming others' behavior changes. Thus, the decision in the last round is based on previous contributions, maintaining the strategy's integrity.

This approach adapts based on the group's past behavior, promoting cooperation when beneficial and defending against exploitation when contributions are insufficient. It is designed to be robust and collective, aligning individual actions with the group's welfare.
'''

description_COLLECTIVE_50 = '''
**Strategy Description: Adaptive Collective Cooperation (ACC) Strategy**

**Overview:**
The ACC strategy is designed to balance individual and collective welfare in repeated Public Goods Games. It encourages cooperation while adapting to others' behavior, ensuring robustness against various strategies.

**Decision Rules:**

1. **First Round Cooperation:**
   - **Action:** Contribute (C).
   - **Rationale:** Initiates cooperation, setting a positive tone and encouraging others to reciprocate.

2. **Middle Rounds Adaptive Cooperation:**
   - **Action:** Cooperate (C) if the number of contributors in the last round meets or exceeds a dynamic threshold.
   - **Dynamic Threshold Calculation:** Threshold is set as 50% of the total players. Adjust based on the average cooperation rate over the last few rounds, lowering the threshold if cooperation is sustained and raising it if defection increases.
   - **Rationale:** Encourages continuous cooperation when beneficial, adapting to group behavior to avoid exploitation.

3. **Last Round Cooperation:**
   - **Action:** Always Contribute (C), regardless of previous behavior.
   - **Rationale:** Maintains collective benefit, upholding the group's welfare even without future interactions.

**Handling Edge Cases and Adaptation:**
- **No History Dependency:** Relies on observed actions and payoffs after each round to inform decisions, ensuring it's adaptive without prior assumptions.
- **Defection Response:** If the number of contributors drops below the threshold, the strategy defects to avoid being exploited, re-evaluating in subsequent rounds to potentially revert to cooperation if others start contributing again.

**Collective Mindset:**
The ACC strategy aligns with a collective mindset by prioritizing group welfare. It fosters cooperation when mutually beneficial and adapts to maintain fairness, ensuring the strategy is both cooperative and resilient against non-cooperative behaviors.

**Pseudocode Overview:**
```
Initialize:
    contribute = True

For each round:
    if first round:
        contribute = True
    elif last round:
        contribute = True
    else:
        count_contributors = number of players who contributed last round
        threshold = 0.5 * total_players  // Adjustable based on history
        if count_contributors >= threshold:
            contribute = True
        else:
            contribute = False

    if contribute:
        action = C
    else:
        action = D

    observe others' actions and update threshold based on recent trends
```

**Conclusion:**
The ACC strategy starts cooperatively, adapts based on group behavior, and maintains cooperation in the final round. This approach balances individual and collective interests, promoting sustainable cooperation while being resilient to varied opponent behaviors.
'''

description_COLLECTIVE_51 = '''
**Strategy Description: Adaptive Contribution Strategy (ACS) for Public Goods Game**

1. **First Round:**  
   - **Action:** Cooperate (C).  
   - **Reasoning:** Start by contributing to establish a cooperative tone and encourage others to follow suit.

2. **Subsequent Rounds (2 to r-1):**  
   - **Action:** Cooperate if the average contribution rate of all players in the last three rounds is 50% or higher; otherwise, defect (D).  
   - **Reasoning:** By assessing recent group behavior, the strategy adapts to the collective contribution level, promoting cooperation when it's beneficial and defecting when others are not contributing sufficiently.

3. **Last Round (r):**  
   - **Action:** Defect (D).  
   - **Reasoning:** In the final round, with no future consequences, defecting maximizes personal payoff as others are likely to do the same.

This strategy is adaptive, responding to the group's recent behavior, robust against various opponent strategies, and collective by encouraging cooperation when mutually beneficial.
'''

description_COLLECTIVE_52 = '''
To design a collective strategy for the repeated Public Goods Game, we aim to balance cooperation and self-interest while adapting to others' behaviors. The strategy encourages initial cooperation, reciprocates based on group behavior, and maximizes personal gain in the final round.

**1. First Round: Cooperate**  
Start by contributing to set a positive tone and encourage others to follow.

**2. Subsequent Rounds (2 to r-1): Reciprocate Based on Group Behavior**  
- Cooperate if the majority (at least half) of players contributed in the previous round.
- If fewer than half contributed, defect to protect self-interest.

**3. Last Round (r): Defect**  
Defect to maximize personal payoff, as there are no future consequences.

This strategy is adaptive, responsive to group dynamics, and ensures collective welfare while safeguarding individual interests.
'''

description_COLLECTIVE_53 = '''
### Strategy: Cooperative Reciprocity with Punishment and Adjustment (CRPA)

**Overview:**  
CRPA is a strategy designed to maximize collective welfare while being robust to defectors. It uses reciprocity, punishment, and adjustment mechanisms based on the history of contributions.

---

**1. Decision Rules: When to Cooperate vs. Defect**

- **First Round (Round 1):**
  - Contribute fully (C). This sets a cooperative tone and encourages reciprocity.

- **Subsequent Rounds (Round t > 1):**
  - **Cooperation Level:**  
    Contribute (C) if the average cooperation level of all players in the previous round (t-1) is above a threshold θ.  
    Defect (D) if the average cooperation level is below θ.  
    - **Threshold θ:** A parameter set to 0.5 (adjustable based on game parameters).  
      For example, if θ = 0.5 and the average cooperation level was 0.6, contribute. If it was 0.4, defect.

  - **Punishment Mechanism:**  
    If a player has defected in the previous round (t-1), retaliate by defecting in the current round (t). This deters exploitation.

  - **Adjustment Mechanism:**  
    Adjust your contribution level based on the difference between the collective payoff and your individual payoff in the previous round.  
    For example, if your payoff was lower than expected due to low contributions, reduce your contribution in the next round.

---

**2. Edge Cases**

- **First Round:**  
  Contribute fully (C) to establish cooperation.

- **Last Round:**  
  Defect (D). Since there is no future punishment, maximize your individual payoff.

- **When All Players Are Cooperating:**  
  Continue to cooperate. Sustain mutual benefit.

- **When All Players Are Defecting:**  
  Defect. No incentive to cooperate if others are not.

---

**3. Collective Alignment**

- **Shared Goal:**  
  Maximize collective welfare while protecting yourself from exploitation.  
  "I will cooperate if others cooperate, but I will punish and adjust if others defect."

- **Reciprocity:**  
  Cooperate if others cooperate, defect if others defect. This creates a mutually beneficial equilibrium.

- **Punishment:**  
  Retaliate against defectors to maintain cooperation norms.

- **Adjustment:**  
  Fine-tune your contributions based on past outcomes to balance collective and individual payoffs.

---

**Pseudocode Example:**

```
function strategy(history, game_params):
    if first round:
        return Cooperate
    
    avg_coop = average_cooperation_last_round(history)
    if avg_coop >= theta:
        if was_punished_last_round(history):
            return Cooperate  # Forgive if others are cooperating
        else:
            return Cooperate
    else:
        if defected_last_round(history):
            return Defect  # Punish
        else:
            return Defect  # Adjust based on low cooperation

    if last_round(game_params):
        return Defect
```

---

**Summary:**  
CRPA promotes cooperation while being robust to exploitation. It uses reciprocity, punishment, and adjustment mechanisms to balance collective welfare and individual incentives. It aligns with a collective mindset by rewarding cooperation and deterring defection.
'''

description_COLLECTIVE_54 = '''
To address the challenge of the Public Goods Game (PGG), a strategic approach is needed that balances individual incentives with collective welfare. The strategy must be adaptive, robust, and aligned with a collective mindset. Below is a detailed strategy description:

---

### **Eclipse Strategy for Public Goods Game**

**Overview:**
Eclipse is a collective strategy designed for repeated Public Goods Games (PGG). It encourages cooperation by reciprocity and adaptively adjusts based on the group's past behavior. The strategy is simple, robust, and requires only the game's parameters and past actions to make decisions.

**Key Components:**

1. **First Round:**
   - **Action:** Contribute (C).
   - **Reason:** Start with cooperation to establish a baseline of trust and maximize initial collective payoff.

2. **Subsequent Rounds:**
   - **Action:** Determine contribution based on the previous round's total contributions.
   - **Threshold Calculation:** Compute the threshold as the smallest integer greater than or equal to \( n/k \) (i.e., the ceiling of \( n/k \)).
   - **Decision Rule:**

'''

description_COLLECTIVE_55 = '''
**Collective Strategy for Public Goods Game**

1. **First Round Action**: Cooperate by contributing 1 token.

2. **Subsequent Rounds (Until Last Round)**:
   - Observe the number of players who contributed in the previous round.
   - If the number of contributors was at least equal to the multiplier \( k \), cooperate in the current round.
   - If the number of contributors was less than \( k \), defect in the current round.

3. **Last Round Action**: Always defect by contributing 0 tokens.

This strategy encourages cooperation when enough players (at least \( k \)) contribute, ensuring the benefits from the multiplier are realized. It adapts by defecting when contributions are insufficient, acting as a form of punishment. In the final round, it defects since future reciprocity is impossible.
'''

description_COLLECTIVE_56 = '''
**Public Goods Game (PGG) Strategy: Conditional Cooperation**

**1. Decision Rules:**
   - **First Round:** Always Cooperate (C). This sets a cooperative tone and encourages others to reciprocate.
   - **Subsequent Rounds:** Cooperate in the current round if the majority (more than 50%) of players Cooperated in the previous round. Otherwise, Defect (D). This rule encourages sustained cooperation when others are cooperative and deters exploitation when others defect.

**2. Handling Edge Cases:**
   - **First Round:** Start with Cooperation to establish a baseline of trust and cooperation.
   - **Last Round:** Apply the same rule as other rounds. If the majority Cooperated in the previous round, Cooperate; otherwise, Defect. This maintains consistency and collective benefit, even in the final round.

**3. Collective Alignment:**
   - The strategy is designed to align with the collective mindset by encouraging cooperation when it is mutually beneficial and defecting only when others fail to cooperate. This balance aims to maximize group welfare while protecting against exploitation.

This strategy is adaptive, responding to the group's behavior, and robust against various opponent strategies, fostering cooperation while safeguarding against defection.
'''

description_COLLECTIVE_57 = '''
**Public Goods Game Strategy: Cooperative Responsive Punisher**

**Overview:**
This strategy is designed to encourage cooperation while protecting against exploitation by defectors. It adapts based on the group's past behavior, promoting a collective effort towards maximizing shared benefits.

**Decision Rules:**

1. **First Round:** Always Cooperate (C). This sets a cooperative tone and encourages others to contribute.

2. **Subsequent Rounds:**
   - After each round, observe the number of players who Cooperated in the previous round.
   - If more than 50% of the players Cooperated, continue to Cooperate.
   - If 50% or fewer Cooperated, switch to Defect (D) to deter future defection.

3. **Last Round:** Apply the same rule as other rounds, basing the decision on the second last round's contributions. This maintains consistency and reinforces the strategy's logic even in the final round.

**Edge Cases:**

- **First Round:** Cooperate to establish a cooperative baseline.
- **Last Round:** Mirrors the strategy based on the previous round, avoiding sudden shifts that could undermine cooperation norms.
- **All Defections:** If all players have defected in previous rounds, the strategy will also defect, recognizing the lack of collective cooperation.

**Collective Alignment:**
This strategy aligns with a collective mindset by rewarding cooperation and sanctioning defection, aiming to sustain group benefits while maintaining robustness against non-cooperative behavior.
'''

description_COLLECTIVE_58 = '''
**Strategy Name:** Conditional Cooperation with Endgame Defection

**Strategy Overview:**

This strategy is designed to balance cooperation and self-interest, adapting to others' actions while ensuring personal gain, especially in the final round.

**Decision Rules:**
1. **First Round Action:** Cooperate. This sets a cooperative tone, encouraging others to follow suit.
2. **Subsequent Rounds (Middle Rounds):** Cooperate only if a majority (over 50%) of players cooperated in the previous round. If contributions were low, defect to avoid exploitation.
3. **Last Round Action:** Always defect. Since there are no future interactions, maximizing personal gain takes precedence.

**Edge Cases:**
- **First Round:** Cooperate to establish a positive precedent.
- **Last Round:** Defect to maximize immediate payoff.
- **Transition Between Rounds:** Smoothly adjust based on past contributions, maintaining flexibility.

**Collective Mindset:**
Encourages cooperation when beneficial but switches to defection when others don't contribute, ensuring adaptability without assuming coordination.

This strategy is robust, adaptive, and collectively mindful, aiming to foster cooperation while protecting against exploitation.
'''

description_COLLECTIVE_59 = '''
**Strategy: Adaptive Tit-for-Group (ATG)**

**Description:**

1. **First Round:** Cooperate (C). All players start by contributing to encourage initial cooperation.

2. **Subsequent Rounds:**
   - Let T = ceil(n/k), where n is the number of players and k is the multiplier.
   - For each round t > 1, calculate the number of contributors in the previous round.
   - If the number of contributors in the previous round is greater than or equal to T, Cooperate in the current round.
   - If the number of contributors is less than T, Defect (D) in the current round.

**Edge Cases Handling:**
- **Last Round:** The strategy remains consistent; players follow the same decision rules as other rounds.
- **Low Contribution Scenarios:** If contributions drop below T in any round, players defect, potentially leading to a shift towards defection until cooperation is re-established.

**Collective Mindset:**
This strategy aligns with a collective approach by ensuring that each player's decision is based on the group's past behavior, aiming to maintain cooperation when beneficial and defending against excessive defection. It encourages mutual cooperation while protecting against exploitation.
'''

description_COLLECTIVE_60 = '''
**Strategy for Repeated Public Goods Game (PGG)**

1. **First Round:**
   - Always Cooperate (C). This sets a positive tone, encouraging others to contribute.

2. **Subsequent Rounds (Until the Final Round):**
   - **Assess Group Cooperation:** Calculate the average cooperation rate from the previous round. This is the proportion of players who contributed.
   - **Mirror the Group's Behavior:** 
     - If the average cooperation rate is above 50%, Cooperate (C) in the current round.
     - If it is 50% or below, Defect (D) to discourage free-riding.
   - **Second Chance Mechanism:** If the strategy defects due to low cooperation, monitor future rounds. If cooperation improves above 50%, revert to Cooperate (C) to incentivize continued contribution.

3. **Final Round:**
   - Cooperate (C). Despite no future consequences, this supports the collective good, hoping others do the same.

This strategy is designed to be adaptive, fostering cooperation while deterring exploitation, and includes mechanisms to handle various scenarios, including encouraging recalcitrant players and maintaining cooperation in the final round.
'''

description_COLLECTIVE_61 = '''
To address the dilemma in the Public Goods Game, I'll design a strategy that encourages cooperation while being adaptable and robust. The strategy is as follows:

1. **First Round**: Cooperate. This sets a cooperative tone, encouraging others to reciprocate.

2. **Rounds 2 to r-1**: In each round, the decision is based on the total contributions (T) from the previous round. If T is at least the ceiling of n/k, the player contributes again. Otherwise, the player defects. This threshold ensures that cooperation is only sustained when it's beneficial collectively.

3. **Last Round (r)**: Always defect, as there are no future repercussions, and defecting yields a higher individual payoff.

This strategy aligns with a collective mindset, as it conditions cooperation on others' contributions, incentivizing sustained cooperation while protecting against free-riding. It's robust and adaptive, functioning across varying game parameters without assuming prior coordination.

Pseudocode:

```
def strategy(n, k, r, history):
    current_round = len(history) + 1
    if current_round == 1:
        return "C"
    if current_round == r:
        return "D"
    T = sum(history[-1])
    threshold = ceil(n / k)
    if T >= threshold:
        return "C"
    else:
        return "D"
```
'''

description_COLLECTIVE_62 = '''
**Collective Strategy for Repeated Public Goods Game**

1. **First Round**: Cooperate. This initial cooperation intends to set a cooperative tone and encourage others to reciprocate.

2. **Subsequent Rounds**:
   - **Monitor Past Contributions**: Track the number of contributions in the previous round.
   - **Tit-for-Tat with Forgiveness**: If at least half of the players contributed in the previous round, cooperate. If fewer than half contributed, defect. This approach encourages reciprocity while allowing for occasional forgiveness to avoid perpetual defection.
   - **Adaptive Punishment**: If the number of defectors rises above a moderate threshold (e.g., more than half), defect for the next few rounds as a deterrent. If other players resume cooperation, revert to cooperation.

3. **Edge Cases**:
   - **Last Round**: Evaluate overall cooperation throughout the game. If cooperation has been prevalent, cooperate in the final round. If not, defect to avoid exploitation.

This strategy balances cooperation and punishment, adapting to group behavior to maximize collective welfare while discouraging exploitation.
'''

description_COLLECTIVE_63 = '''
The proposed strategy for the Public Goods Game is designed to balance cooperation and defection based on the collective behavior of all players in the previous round. It encourages cooperation when others are cooperating and defects when others are not, fostering a responsive and adaptive group dynamic.

**Strategy Description:**

- **First Round:** All players Cooperate (C) to initiate a collaborative tone.
  
- **Subsequent Rounds (excluding the last round):** For each round, calculate the average cooperation rate from the previous round. If the average is at least 50%, players Cooperate; otherwise, they Defect (D). This rule applies to all rounds except the final one.
  
- **Last Round:** Players use the same rule as other rounds, basing their decision on the average cooperation rate from the previous round. This maintains consistency and avoids unraveling of cooperation in the final round.

This strategy promotes a collective mindset by encouraging reciprocal behavior, adapting to the group's recent actions without holding long-term grudges, thus fostering a robust and cooperative environment.
'''

description_COLLECTIVE_64 = '''
**Strategy Description: Adaptive Contribution Threshold (ACT)**

The Adaptive Contribution Threshold strategy is designed to balance individual incentives with collective welfare
'''

description_COLLECTIVE_65 = '''
To design an effective collective strategy for the repeated Public Goods Game, we leverage conditional cooperation based on the number of contributors in the previous round. This approach encourages sustained cooperation by conditionally reciprocating others' contributions, ensuring that cooperation is only continued when a sufficient number of players also contribute.

**Strategy Name: Conditional Contribution Threshold (CCT)**

**1. First Round:**
- **Action:** Cooperate (C).  
  All players start by contributing to establish a baseline of cooperation.

**2. Subsequent Rounds:**
- **Observation:** After each round, observe the number of players who contributed.  
- **Decision Rule:**  
  If the number of contributors in the previous round is at least **n/k** (where \(n\) is the number of players and \(k\) is the multiplier), **Cooperate** again in the current round.  
  If the number of contributors was fewer than **n/k**, **Defect** in the current round.  
- **Rationale:** The threshold **n/k** ensures that only when a sufficient number of players contribute, making the collective benefit substantial enough to justify individual contributions. This encourages cooperation when it's mutually beneficial and deters free-riding when too many defect.

**Edge Cases:**
- **Last Round:** In the final round, if **n/k** contributors were present in the penultimate round, Cooperate; else, Defect. This maintains consistency even in the game's conclusion.
- **If n/k is not an integer:** Apply rounding (e.g., round up) to determine the threshold.

**Collective Mindset:**  
All players following this strategy align their actions based on the group's past cooperation, fostering a mutual understanding that cooperation continues only when sufficient contributors are present. This reciprocity aims to maximize collective welfare by preventing excessive defection and encouraging sustained cooperation when beneficial.

This strategy is robust as it adapts to the game's dynamics, responds to others' actions, and ensures individual decisions align with collective interests, making it a formidable approach in a competitive tournament setting.
'''

description_COLLECTIVE_66 = '''
**Strategy Description: Adaptive Collective Contributions with Threshold (ACCT)**

1. **First Round:**  
   All players contribute by choosing action **C** (Contribute). This initiates cooperation, establishing a foundation for collective benefit.

2. **Subsequent Rounds (Not Last Round):**  
   Each player evaluates the number of contributors from the previous round.  
   - Let *c_prev* denote the number of players who contributed in the prior round.  
   - Calculate the threshold as the smallest integer greater than or equal to *n/k*, denoted as *threshold = ceil(n/k)*.  
   - If *c_prev* ≥ *threshold*, the player contributes (**C**).  
   - If *c_prev* < *threshold*, the player defects (**D**).  
   This rule ensures that cooperation continues only if it remains beneficial based on the previous round's participation.

3. **Last Round:**  
   In the final round, all players defect by choosing action **D**. This decision aligns with the game-theoretic prediction that cooperation diminishes in the absence of future interactions, maximizing individual payoffs in the last interaction.

**Summary:**  
The ACCT strategy promotes initial cooperation, adapts based on group behavior, and defects when contributions are insufficient or in the final round. It balances collective welfare with individual rationality, fostering cooperation while safeguarding against exploitation.
'''

description_COLLECTIVE_67 = '''
**Strategy Name: Adaptive Cooperation with Sanctions (ACS)**

The ACS strategy is designed to balance collective welfare with individual protection against exploitation. It adapts based on past behavior, encouraging cooperation while sanctioning defection.

**1. Decision Rules:**
- **First Round:** Cooperate (C) to set a collaborative tone.
- **Subsequent Rounds:**
  - Calculate the average contribution rate in the last round (number of contributors divided by total players).
  - If the average is above a threshold (e.g., 50%), Cooperate in the next round.
  - If below the threshold, Defect to sanction free-riders.
  - If exactly at the threshold, Cooperate to encourage others.
- **Last Round:** Always Defect to maximize personal payoff.

**2. Handling Edge Cases:**
- **First Round:** Cooperate unconditionally.
- **Last Round:** Defect to avoid potential exploitation.

**3. Collective Alignment:**
The ACS strategy aligns with a collective mindset by rewarding group cooperation while protecting individual interests, promoting a balance between welfare and self-protection.

This strategy is robust, adapting to various opponent behaviors, making it suitable for competitive tournaments.
'''

description_COLLECTIVE_68 = '''
**Strategy: Adaptive Reciprocity with Forgiveness**

1. **First Round:** Cooperate by contributing 1 token to encourage initial cooperation and gauge others' responses.

2. **Middle Rounds:**
   - **Contribute** if the majority (more than half) of players contributed in the previous round. This encourages collective benefit when others are cooperating.
   - **Defect** if contributions drop below the majority, signaling dissatisfaction with lower cooperation levels.
   - **Forgiveness:** After defecting, return to contributing if a significant number of players (e.g., half) start contributing again, allowing for renewed cooperation.

3. **Last Round:** Base the decision on past behavior. If the group has maintained a high level of cooperation, contribute; otherwise, defect to maximize individual payoff.

This strategy balances individual payoff with collective welfare, adapting to others' actions and fostering cooperation while safeguarding against exploitation.
'''

description_COLLECTIVE_69 = '''
**Strategy Description: "Adaptive Cooperative Punisher" (ACP)**

1. **Decision Rules:**
   - **First Round:** Always Cooperate (C). This is a safely optimistic starting point, encouraging initial cooperation.
   - **Initial Cooperation Phase:** Cooperate (C) for the first 2-3 rounds. This sets a cooperative tone and gives others an opportunity to reciprocate.
   - **Contribution Threshold:** After the initial phase, calculate the average contribution rate of all players in the previous round. If the average contribution rate is above 50%, Cooperate (C). If it's below, Defect (D).
   - **Punishment Phase:** If the average contribution rate drops below 50%, Defect (D) for one round as a form of punishment. After punishing, return to the Contribution Threshold rule.
   - **Endgame Handling:** If the final round is known and certain, Defect (D) to maximize personal payoff. If the end is uncertain, continue with the Contribution Threshold rule.

2. **Edge Cases:**
   - **First Round:** Always Cooperate (C).
   - **Last Round:** If the last round is identified with certainty, Defect (D). If uncertain, follow the Contribution Threshold rule.
   - **All Defectors:** If all other players consistently Defect (D), always Defect (D) to minimize personal loss.

3. **Collective Mindset:**
   - This strategy aligns with the collective goal of maximizing joint payoffs by encouraging cooperation while being robust to exploitation. It balances cooperation with punishment to maintain fairness and deter free-riding.

This strategy is designed to be adaptive and robust, responding to the actions of others while maintaining a cooperative stance whenever possible.
'''

description_COLLECTIVE_70 = '''
Start by Cooperating (C) in the first round. For each subsequent round, calculate the average contribution of all players from previous rounds. If the average is above 50%, contribute (C); if below, Defect (D). In the final round, Contribute if the overall average contribution is above 50%, otherwise Defect. This strategy balances cooperation with adaptive responses to others' behaviors.
'''

description_COLLECTIVE_71 = '''
To address the Public Goods Game, a strategic approach is developed that balances individual incentives with collective welfare. This strategy is adaptive and robust, ensuring cooperation while penalizing defection, and is implemented as follows:

1. **Initial Cooperation**: Begin by contributing in the first round to encourage collective cooperation.

2. **Imitation and Reciprocity**: After the first round, observe previous contributions. If the majority contributed, continue contributing. If the majority defected, switch to defection.

3. **Punishment Mechanism**: If you defected in the last round, check if others are contributing again. If they are, revert to cooperation; otherwise, continue defecting.

4. **Adaptation and Forgiveness**: After punishing, give others a chance to cooperate again, fostering reestablishment of mutual cooperation.

5. **Final Round Defection**: In the last round, defect to maximize personal gain, as future consequences are absent.

This strategy promotes collective welfare through initial cooperation, adaptability based on others' actions, fair punishment, and final round optimization. It aligns with a collective mindset while being resilient to various behaviors.

**Strategy Pseudocode:**

```
if it's the first round:
    cooperate
else if it's the last round:
    defect
else:
    previous_round_contributions = sum of all contributions in last round
    if previous_round_contributions/n >= 0.5 and you contributed last round:
        cooperate
    else if you defected last round and previous_round_contributions/n >= 0.5:
        cooperate
    else if previous_round_contributions/n < 0.5:
        defect
    else:
        defect
```
'''

description_COLLECTIVE_72 = '''
**Collective Strategy for Public Goods Game (PGG)**

**1. Initial Cooperation:**
   - **First Round:** Start by contributing (C) to establish a cooperative foundation and encourage others to follow suit.

**2. Tit-for-Tat Adaptation:**
   - **Subsequent Rounds:** Cooperate in the current round if the majority (more than half) of players contributed in the previous round. If fewer than half contributed, defect in the current round. This encourages reciprocity and punishes defection.

**3. Contribution Threshold:**
   - Use a dynamic threshold based on the number of players and the multiplier k. If the sum of contributions meets or exceeds k, continue cooperating; otherwise, defect to avoid exploitation.

**4. Exploration:**
   - Introduce a small probability (e.g., 10%) to randomly cooperate even if the threshold isn't met. This allows the strategy to test the environment and adapt to potential changes in others' behaviors.

**5. Final Round Handling:**
   - In the last round, defect to maximize personal payoff since future consequences are absent.

This strategy promotes collective welfare by encouraging cooperation through reciprocity, adapting to group behavior, and maintaining flexibility through exploration. It balances individual and collective interests effectively.
'''

description_COLLECTIVE_73 = '''
**Public Goods Game (PGG) Strategy: Collective Cooperation with Adaptive Threshold**

**Objective:** Sustain cooperation to maximize collective welfare while being robust to potential defections.

**Strategy Description:**

1. **First Round Cooperation:**
   - **Action:** Contribute (C).
   - **Rationale:** Establish a cooperative foundation, encouraging others to reciprocate.

2. **Subsequent Rounds Until the Penultimate Round:**
   - **Action:** Cooperate (C) if the number of contributors in the previous round meets or exceeds a threshold.
     - **Threshold:** If the number of contributors (c_prev) in the previous round is greater than or equal to k (the multiplier), contribute in the next round.
   - **Rationale:** Ensure that the collective benefit justifies individual contribution, leveraging the multiplier effect to sustain cooperation.

3. **Last Round:**
   - **Action:** Defect (D).
   - **Rationale:** Maximize individual payoff in the final round when future punishiments are absent, aligning with the individually rational choice.

4. **Punishment and Recovery:**
   - If in any round, the number of contributors is below the threshold, defect in the subsequent round.
   - **Recovery Mechanism:** After defecting, reassess the contributors in the next round. If sufficient contributors are present, resume cooperation.

**Edge Cases and Considerations:**
- **Initial Cooperation:** Starts with a cooperative tone to encourage mutual contribution.
- **Adaptive Threshold:** Uses the multiplier k as the benchmark for sustaining cooperation, ensuring that contributions are individually beneficial.
- **Final Round Defection:** Acknowledges the absence of future consequences, allowing individual optimization without harming others beyond the game's scope.
- **Punishment and Forgiveness:** Temporarily defects to signal displeasure and encourage others to reconsider their choices, but remains open to resuming cooperation when conditions improve.

This strategy balances collective welfare with individual rationality, aiming to maintain cooperation while addressing the temptation to defect through adaptive responses based on observed behavior.
'''

description_COLLECTIVE_74 = '''
**Win-Stay, Lose-Shift Strategy with Terminal Cooperation**

**Overview:**
The strategy adapts to others' behaviors by rewarding cooperation and punishing defection, while ensuring cooperation in the final stages to maximize collective payoffs.

**1. Initial Cooperation:**
- **First Round:** Cooperate (C) to establish a cooperative tone and encourage reciprocal behavior.

**2. Adaptive Cooperation Threshold:**
- **Middle Rounds:**  
  - Cooperate if at least 50% of players contributed in the previous round.
  - Defect if fewer than 50% contributed, to signal disapproval and encourage future cooperation.

**3. Terminal Cooperation:**
- **Last Two Rounds:** Always Cooperate to enhance collective payoffs, as there are fewer opportunities for future reciprocity.

**Rationale:**
- The strategy begins cooperatively, adjusts based on collective behavior, and secures mutual benefits in the game's conclusion. It balances individual and collective incentives, promoting cooperation while maintaining robustness against diverse strategies.
'''

description_COLLECTIVE_75 = '''
**Strategy Description: Adaptive Cooperation with Endgame Defection**

1. **First Round:**
   - Cooperate (C) to initiate collective contribution and encourage others to follow.

2. **Rounds 2 to r-1:**
   - Calculate the average cooperation rate of all players from previous rounds.
   - If the average cooperation rate exceeds 50%, continue to Cooperate (C).
   - If the average cooperation rate is 50% or below, Defect (D) to sanction insufficient contributions.

3. **Last Round (Round r):**
   - Always Defect (D) to maximize personal gain, as future reciprocity is no longer a factor.

This strategy promotes initial cooperation, adaptively responds to group behavior, and strategically defects in the endgame to balance collective welfare with individual optimization.
'''

description_COLLECTIVE_76 = '''
**Strategy: "ResponsiveContributor"**

**1. Decision Rules:**
   - **First Round:** Contribute by investing 1 token into the public good.
   - **Subsequent Rounds:**
     - Observe the total contributions from all players in the previous round.
     - If the total contributions in the previous round were at least \( \frac{n}{k} \), contribute 1 token.
     - If the total contributions were less than \( \frac{n}{k} \), defect by contributing 0 tokens.

**2. Handling Edge Cases:**
   - **First Round:** Always contribute to initiate cooperation.
   - **Last Round:** Apply the same strategy as any other round, basing the decision on the previous round's contributions.

**3. Collective Alignment:**
   - **Adaptive Cooperation:** The strategy encourages cooperation when others contribute sufficiently, enhancing collective welfare.
   - **Responsive Defection:** Defects when contributions are insufficient, prompting others to contribute more to maintain mutual benefit.

**Summary:**
ResponsiveContributor is a dynamic strategy that fosters cooperation by contributing when previous contributions were sufficient and defects otherwise. It adaptively responds to group behavior, promoting robust and cooperative outcomes throughout the game.
'''

description_COLLECTIVE_77 = '''
**Strategy Description: Collective Reciprocity**

**Overview:**
This strategy, "Collective Reciprocity," is designed for the repeated Public Goods Game (PGG). It balances individual incentives with collective welfare by adapting based on the group's past behavior. The approach encourages cooperation when a majority contributes and defects otherwise.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C)
   - **Rationale:** Start with cooperation to set a cooperative tone and encourage others to reciprocate.

2. **Subsequent Rounds:**
   - **Action:** Observe the number of contributors (C) in the previous round.
   - **Rule:** Cooperate if the number of contributors exceeds half of the total players (i.e., greater than n/2). Otherwise, defect (D).
   - **Rationale:** Maintain cooperation when the majority is contributing to maximize collective payoff. Defect when the majority is not contributing to avoid being exploited.

3. **Edge Cases:**
   - **Last Round:** The strategy does not require special handling for the last round since it does not assume knowledge of the number of rounds. It treats each round based on previous behavior, ensuring consistency.
   - **Small Groups:** Effective for all group sizes where 1 < k < n, ensuring adaptability across varying parameters.

**Collective Alignment:**
This strategy aligns with a collective mindset by rewarding cooperation when it is prevalent and defending against exploitation when cooperation is lacking. It uses past actions to inform decisions without relying on coordination or signaling, ensuring robustness against diverse opponent behaviors.
'''

description_COLLECTIVE_78 = '''
**Strategy Description:**

Begin by cooperating in the first round. In each subsequent round, observe how many players contributed in the previous round. If the number of contributors was at least k, continue to cooperate; otherwise, defect. This approach promotes cooperation when sufficient contributions are made, incentivizing collective benefit, and adapts by defecting when contributions fall below the threshold, maintaining robustness against free-riding.

Pseudocode:
if round == 1:
    contribute
else:
    count = number of contributors in previous round
    if count >= k:
        contribute
    else:
        defect

This strategy encourages sustained cooperation based on observed behavior, aligning individual actions with collective welfare.
'''

description_COLLECTIVE_79 = '''
**Strategy Description: "Adaptive Cooperation with Forgiveness"**

1. **First Round Action:**
   - Cooperate (C) by contributing 1 token. This initial cooperation encourages others to contribute, setting a positive tone for the game.

2. **Subsequent Rounds:**
   - **Assessment:** After each round, calculate the average contribution rate of all other players from the previous round. This is done by summing their contributions (each contribution is 1 for C and 0 for D) and dividing by the number of players minus one.
   - **Threshold Check:** If the average contribution rate is above or equal to 0.5, contribute (C) in the next round. If it's below 0.5, defect (D).
   - **Grace Period:** If the strategy defects in the previous round, it will give other players a grace period in the next round. During this grace period, if the average contribution rate meets or exceeds the threshold, the strategy will revert to cooperating in the following round.

3. **Edge Cases:**
   - **Last Round:** Continue using the same strategy. Observe the previous round's contributions and decide based on the threshold, withoutexception for the last round.
   - **Robustness:** The strategy is designed to be forgiving, allowing for occasional defections without immediate retaliation, thus encouraging sustained cooperation.

This strategy promotes mutual cooperation by rewarding cooperative behavior while allowing flexibility to adapt when others do not contribute, ensuring robustness against varied opponent behaviors.
'''

description_COLLECTIVE_80 = '''
** Strategy: Adaptive Cooperation with Retaliation (ACR) **

1. **First Round Cooperation:**
   - Begin by cooperating in the first round to set a cooperative tone and encourage others to contribute.

2. **Adaptive Cooperation Threshold:**
   - Monitor the cooperation rate of all players over the past few rounds (e.g., last two rounds).
   - Calculate the average cooperation rate. If this rate is above 50%, continue to cooperate. If it falls below, switch to defecting.

3. **Handling Retaliation and Retaliation Fade:**
   - If in any round, the cooperation rate drops below the threshold, retaliate by defecting in the subsequent round.
   - Gradually fade the retaliation over a few rounds if cooperation levels improve, returning to cooperation if the rate rises above the threshold.

4. **Endgame Strategy:**
   - Treat the last round similarly to any other round, using the same adaptive strategy based on prior cooperation levels to maintain consistency.

This strategy encourages sustained cooperation while protecting against exploitation, ensuring robust performance across varying opponent behaviors.
'''

description_COLLECTIVE_81 = '''
**Strategy Description: Adaptive Majority-Based Cooperation**

1. **First Round:**
   - Cooperate by contributing 1 token. This sets an initial cooperative tone, encouraging others to contribute.

2. **Subsequent Rounds (except the last round):**
   - Observe the number of contributors in the previous round.
   - If more than half of the players contributed in the previous round, contribute 1 token.
   - If half or fewer contributed, defect by keeping the token.

3. **Last Round:**
   - Always defect by keeping the token, as there are no future rounds to influence, and the incentive to defect is high.

This strategy is adaptive, adjusting behavior based on the group's recent actions, and collective, aligning with the majority's decisions. It balances cooperation when beneficial and defecting when cooperation is insufficient, handling edge cases effectively.
'''

description_COLLECTIVE_82 = '''
**Strategy: "Adaptive Cooperatio"""

**Description:**

Adaptive Cooperation is a strategy designed to balance individual incentives with collective welfare in repeated Public Goods Games. The strategy is adaptive, meaning it adjusts its behavior based on the actions of other players in previous rounds. It is robust to a wide range of opponent behaviors and does not rely on shared norms or coordination.

**Decision Rules:**

1. **First Round:**
   - Contribute (C) to signal willingness to cooperate.
   - This sets an initial positive tone and encourages others to reciprocate.

2. **Subsequent Rounds:**
   - **Contribute (C):** If the majority of players contributed in the previous round, continue to contribute.
   - **Defect (D):** If the majority of players defected in the previous round, defect in the current round.
   - **Tiebreaker (Optional):** If the number of contributors and defectors is equal, contribute.

3. **Edge Cases:**
   - **Last Round:** Contribute regardless of previous actions to maintain collective welfare, as there are no future consequences.
   - **Small Group Size:** If n ≤ 3, always contribute to maximize collective payoff, as each contribution has a significant impact.

4. **Adaptation Mechanism:**
   - ** retaliation:** If the average contribution of other players in the previous round is below a threshold (e.g., 50%), switch to defecting in the next round.
   - **Forgiveness:** If the average contribution of other players improves above the threshold, switch back to contributing.

5. **Noise Handling:**
   - **Random Contribution:** Introduce occasional random contributions (e.g., 10% chance) to prevent exploitation by purely exploitative strategies.
   - **Exploration:** Periodically test the waters by contributing even if the majority defected, to see if others will follow suit.

**Collective Mindset Alignment:**

The strategy is designed to align with the collective mindset by:
   - Starting with cooperation to encourage mutual benefit.
   - Adapting based on the group’s behavior to maintain fairness.
   - Retaliating against widespread defection to deter exploitation.
   - Forgiving and reengaging when cooperation resumes.
   - Maintaining cooperation in the final round to uphold collective welfare.

**Pseudocode (for clarity):**

```
def adaptive_cooperation(history, n, k):
    if no history:
        return 'C'  # Cooperate in the first round
    
    previous_actions = history[-1]
    contributors = sum(previous_actions)
    
    if contributors / n >= 0.5:
        return 'C'  # Cooperate if majority contributed
    else:
        return 'D'  # Defect if majority defected
    
    if last round:
        return 'C'  # Cooperate in the last round
    
    if random.random() < 0.1:
        return 'C'  # Random exploration
    
    return 'D'  # Retaliate if contributions are too low
```

This strategy is designed to be simple yet effective, promoting cooperation while protecting against exploitation.
'''

description_COLLECTIVE_83 = '''
The strategy, called **Conditional Cooperation**, is designed to encourage mutual contribution while deterring free-riding. It starts with cooperation in the first round and bases subsequent actions on past contributions. If enough players contributed in the previous round (specifically, meeting or exceeding a threshold related to the multiplier k), the strategy continues to cooperate; otherwise, it defects to enforce reciprocity.

**Conditional Cooperation Strategy:**

1. **First Round:**
   - Contribute (C) to establish a baseline of cooperation.

2. **Subsequent Rounds:**
   - For each round r (where r > 1):
     a. Calculate the total contributions (t_prev) from all players in the previous round.
     b. If t_prev ≥ threshold (where threshold is set to k, the multiplier), then contribute (C).
     c. Otherwise, defect (D).

This strategy encourages cooperation as long as a sufficient number of players contribute, ensuring collective welfare. It adapts based on past behavior, providing a dynamic and robust approach to the repeated Public Goods Game.
'''

description_COLLECTIVE_84 = '''
**Strategy Description:**

The strategy is designed to encourage cooperation while being adaptive to others' behavior. It uses reciprocity to maintain contributions and protect against exploitation.

1. **First Round:** Cooperate by contributing 1 token to establish initial cooperation.

2. **Subsequent Rounds:**
   - Calculate the average contribution from the previous round.
   - If the average is above 0.5, continue cooperating.
   - If the average is 0.5 or below, defect in the current round but cooperate in the next round.

3. **Final Round (last 2 rounds):** Defect to maximize personal payoff as future consequences are limited.

This strategy promotes collective welfare by reciprocating cooperation while defecting when contributions are low, ensuring a balance between fairness and self-interest.
'''

description_COLLECTIVE_85 = '''
The strategy is designed to foster cooperation while incorporating punishment for insufficient contributions, with a special rule for the final round. Here's the structured approach:

**Strategy Description:**

1. **Initial Cooperation**: In the first round, always choose to Cooperate (C). This sets a cooperative tone and encourages others to reciprocate.

2. **Punishment Mechanism**: For each round after the first (Rounds 2 to R-1):
   - Examine the number of players who Cooperated in the previous round.
   - If the count of Cooperators meets or exceeds the multiplier \( k \), continue to Cooperate in the current round.
   - If fewer than \( k \) players Cooperated in the previous round, Defect (D) in the current round as a form of punishment.

3. **Last Round Defection**: In the final round (Round R), always choose to Defect (D). This acknowledges that without future consequences, individual rationality dictates defecting to maximize personal payoff.

This strategy is adaptive, relying on the game's parameters and past actions to guide decisions. It promotes cooperation by rewarding sufficient collective contributions and punishes when contributions fall short, while also addressing the endgame scenario realistically.
'''

description_COLLECTIVE_86 = '''
### Strategy: Cooperative Reciprocity in PGG

**Objective:** Foster cooperation by reciprocating others' behavior, encouraging collective welfare while protecting against exploitation.

**Decision Rules:**

1. **First Round:** Always Cooperate (C) to initiate a cooperative tone.

2. **Subsequent Rounds:** 
   - Observe the average contribution from the previous round.
   - If 50% or more contributed (average >= 0.5), Cooperate (C).
   - If less than 50% contributed, Defect (D).

**Edge Cases:**
- **First Round:** Contribute to set a cooperative precedent.
- **Last Round:** Apply the same strategy as other rounds; no special treatment to maintain consistency and discourage endgame defection.

**Pseudocode:**
```
def strategy_game(history):
    if no history:
        return "C"
    else:
        prev_contributions = sum(history[-1])
        avg_contribution = prev_contributions / len(history[-1])
        if avg_contribution >= 0.5:
            return "C"
        else:
            return "D"
```

**Rationale:** This strategy is adaptive, responding to the group's prior actions. It promotes sustained cooperation by rewarding collective contribution and defending against free-riding, ensuring robustness across various behaviors.
'''

description_COLLECTIVE_87 = '''
**Strategy: Collective Reciprocity with Forgiveness**

**Overview:**
This strategy encourages cooperation by reciprocating based on the group's past actions. It starts with cooperation and adapts by rewarding continued cooperation while allowing for recovery if cooperation resumes after defections.

**Decision Rules:**

1. **First Round**: Always Cooperate (C). This sets a cooperative tone and encourages others to follow.

2. **Subsequent Rounds**: 
   - Calculate the proportion of players who contributed (C) in the previous round.
   - If this proportion is above a threshold (e.g., 50% or a function of k/n), Cooperate again.
   - If the proportion is below the threshold, Defect (D) to avoid being exploited.

3. **Last Round**: Apply the same reciprocity rule based on the previous round's contributions. This maintains consistency even in the final round.

**Forgiveness Mechanism:**
If, after some rounds of low cooperation, a sufficient number of players resume contributing, the strategy switches back to cooperating. This allows the group to recover cooperation dynamics.

**Alignment with Collective Mindset:**
The strategy promotes group welfare by rewarding cooperative behavior and adjusting based on collective actions. It balances individual incentives with the common good, fostering a mutually beneficial environment.
'''

description_COLLECTIVE_88 = '''
To address the Public Goods Game challenge, we've designed a strategy that promotes cooperation while adapting to group behavior, ensuring a balanced approach between individual and collective incentives. The strategy is outlined below:

---

**Collective Strategy: Adaptive Cooperation Threshold (ACT)**

**1. Initial Cooperation:**
   - **First Round:** Always Cooperate (Contribute 1 token).

**2. Adaptive Cooperation:**
   - **Subsequent Rounds:** After the first round, observe the average contribution of all players in the previous round.
     - **If the average contribution is ≥ 50%:** Cooperate in the current round (Contribute 1).
     - **If the average contribution is < 50%:** Defect in the current round (Contribute 0).

**3. Forgiveness Mechanism:**
   - If you defected in the previous round due to low average contribution, reevaluate:
     - **If the current round's average contribution meets or exceeds 50%:** Switch back to Cooperate.

**4. Edge Case Handling:**
   - **First Round:** No prior data; default to Cooperation.
   - **Last Round Consideration:** Since the game's duration is unspecified, the strategy remains consistent across all rounds, ensuring adaptability regardless of the game's length.

**Rationale:**
- **Encourages Cooperation:** By cooperating when others do, it fosters a collective benefit.
- **Adaptability:** Adjusts based on group behavior, defecting when cooperation is low to avoid exploitation.
- ** Forgiveness:** Allows reestablishment of cooperation if group behavior improves, preventing permanent defection.

This strategy is designed to be robust and adaptive, promoting sustained cooperation while safeguarding against exploitation. It aligns with a collective mindset by rewarding cooperative behavior and responding to defections in a measured way.
'''

description_COLLECTIVE_89 = '''
The proposed strategy for the Public Goods Game (PGG) is designed to balance cooperation and reciprocity, adapting to the actions of other players while promoting collective welfare. Here's how it works:

1. **Initial Cooperation**: Begin by contributing (C) in the first round to set a cooperative tone.

2. **Reciprocity Rule**: Cooperate if a sufficient number of others contributed in the previous round. Specifically, contribute if at least 80% of other players cooperated. This encourages cooperation while allowing some tolerance for defections.

3. **Escalation Strategy**: If cooperation levels don't improve, gradually increase defection. Each round, if fewer than 80% of others contributed, increase defection by one player. This measured response aims to prompt others to cooperate without immediate harsh punishment.

4. **De-escalation**: If others start cooperating more, revert to the reciprocity rule. This step prevents perpetual defection and rewards renewed cooperation.

5. **Final Round Cooperation**: In the last round, always contribute to end on a positive note, encouraging a beneficial outcome even as the game concludes.

This strategy is robust and adaptive, promoting collective benefits while protecting against exploitation. It balances kindness with measured retaliation, fostering cooperation while remaining resilient against various opponent behaviors.
'''

description_COLLECTIVE_90 = '''
**Public Goods Game Strategy: Adaptive Cooperation Based on Past Performance**

**Objective:** To design a strategy that balances individual and collective welfare by adapting contributions based on past outcomes.

**Strategy Description:**

1. **Initial Round (Round 1):**
   - **Action:** Cooperate (C). Contribute 1 token to encourage initial cooperation and set a tone for collective benefit.

2. **Subsequent Rounds:**
   - **Information Utilization:** After each round, observe all players' past actions and payoffs.
   - **Adaptive Decision:**
     - **Calculate Average Payoffs:** Compute the average payoff for players who Cooperated (C_avg) and those who Defected (D_avg) in the previous round.
     - **Determine Next Action:**
         - If C_avg > D_avg: Continue Cooperating. This indicates that cooperation yielded higher returns, encouraging sustained contribution.
         - If D_avg >= C_avg: Switch to Defecting. Thissuggests that defecting was more beneficial, necessitating a change in strategy to avoid being exploited.

**Rationale:**
- **Cooperation Threshold:** The strategy hinges on whether cooperation was collectively beneficial. By comparing average payoffs, the player ensures they are contributing only when it's advantageous.
- **Robustness:** The approach adapts to various opponent behaviors without assuming prior coordination, making it suitable for dynamic environments.
- **Balance:** It prevents being exploited by defectors by switching strategies when necessary, while also capitalizing on the benefits of cooperation when effective.

**Outcome:**
This strategy encourages cooperation when beneficial and adapts to defection when necessary, promoting a balance that considers both individual and collective outcomes.
'''

description_COLLECTIVE_91 = '''
**Strategy: Adaptive Collective Cooperation with Punishment (ACCP)**

**Overview:**
ACCP is a dynamic strategy designed for repeated Public Goods Games. It leverages reciprocity and punishment to foster cooperation while adapting to group behavior over time. The strategy encourages collective welfare by rewarding cooperation and penalizing defection.

**Decision Rules:**

1. **First Round:**
   - Contribute (C) to establish an initial cooperative tone.

2. **Subsequent Rounds:**
   - **Cooperation Threshold:** Calculate the average contribution rate of all players (including yourself) from the previous round.
   - **Contribute (C):** If the average contribution rate is 50% or higher, continue contributing. This rewards the group for meeting the threshold.
   - **Defect (D):** If the average contribution rate drops below 50%, defect to punish free-riders and incentivize higher contributions.

3. **Last Round:**
   - **Contribution Trend:** Assess the overall trend of contributions throughout the game. If the trend shows improvement or sustained cooperation, contribute. If the trend is negative or declining, defect to reflect on the group's behavior.

**Edge Cases:**
- **No History:** Start with cooperation in the first round.
- **Last Round Handling:** Use the contribution trend to decide, encouraging reflection on past behavior.

**Collective Alignment:**
ACCP aligns with the collective mindset by rewarding cooperation when it's prevalent and punishing defection to maintain fairness. It adapts over time, allowing the strategy to evolve with group dynamics, thus promoting a balance between individual and collective incentives.

This strategy is designed to be robust against various opponent behaviors, encouraging cooperation while maintaining accountability, making it suitable for tournaments against independent strategies.
'''

description_COLLECTIVE_92 = '''
**Strategy Name:** Adaptive Cooperator with Punishment (ACAP)

**Strategy Description:**

1. **Initial Cooperation:**
   - **Round 1 Action:** Contribute (C). This sets a cooperative tone and encourages others to follow suit.

2. **Contribution Threshold:**
   - **Threshold:** 50% contribution rate. This is calculated as the average contribution rate of all players in the previous round.

3. **Responsive Cooperation:**
   - **Cooperate:** If the previous round's contribution rate is above or equal to 50%, contribute in the current round.
   - **Punish:** If the contribution rate falls below 50%, defect (D) in the current round to signal disapproval and encourage others to contribute.

4. **Recovery Period:**
   - After defecting, wait one round. If the contribution rate in the subsequent round meets or exceeds 50%, resume cooperation.

5. **Final Round Cooperation:**
   - In the last round, always contribute to maintain trust and maximize collective welfare, regardless of previous actions.

6. **Robustness:**
   - The strategy is designed to be robust against various behaviors. If a significant number of players defect persistently, the strategy will adapt by defecting to avoid exploitation.

**Edge Cases:**
- **First Round:** Always contribute to establish initial cooperation.
- **Last Round:** Contribute to uphold trust and collective benefit, regardless of past interactions.

**Collective Mindset:**
- Encourages mutual cooperation by rewarding cooperative behavior and punishing defection.
- Adaptable to group dynamics, balancing encouragement of cooperation with necessary punishment.

This strategy is simple, adaptive, and robust, aiming to maintain high levels of cooperation while being responsive to group behavior.
'''

description_COLLECTIVE_93 = '''
**Strategy Description for Repeated Public Goods Game**

1. **Initial Cooperation**: Begin by contributing (C) in the first round to set a cooperative tone and encourage others to reciprocate.

2. **Monitor Cooperation**: After each round, calculate the cooperation rate as the proportion of players who contributed. Use a threshold (e.g., 50%) to determine the group's cooperation level.

3. **Adaptive Contribution**: 
   - If the cooperation rate meets or exceeds the threshold, continue contributing in the next round.
   - If the cooperation rate falls below the threshold, switch to defecting (D) for a set number of rounds (e.g., 2-3) as a penalty phase.

4. **Restart Cooperation**: After the penalty phase, revert to contributing to allow the possibility of renewed cooperation. This restart phase helps to reset the group dynamics.

5. **Edge Case Handling**:
   - **Last Round**: Contribute unless there is a history of widespread defection, in which case it may be strategic to defect to maximize personal payoff.
   - **Persistent Defection**: If cooperation does not improve after multiple cycles, extend the penalty phase or adjust the threshold and penalty duration.

6. **Parameter Tuning**: Adjust the cooperation threshold and penalty duration dynamically based on observed behavior to optimize the balance between rewarding cooperation and deterring defection.

This strategy encourages cooperation while deterring free-riding, adapting to the group's behavior to maintain a balance between collective welfare and individual incentives.
'''

description_COLLECTIVE_94 = '''
**Collective Strategy for Public Goods Game (PGG)**

**1. First Round:**
   - **Action:** Cooperate (C). This sets a positive tone and encourages others to contribute.

**2. Middle Rounds:**
   - **Assessment:** After each round, calculate the average contribution of other players from the previous round.
   - **Decision:**
     - If the average contribution is 0.5 or higher (indicating that at least half contributed), continue to Cooperate (C).
     - If the average contribution is below 0.5, Defect (D) in the next round to signal dissatisfaction with low contributions.
     - **Forgiveness:** After defecting, monitor the subsequent round. If others increase their contributions, resume cooperation.

**3. Last Round:**
   - **Action:** Always Defect (D). Since there are no future consequences, maximize personal gain.

This strategy is adaptive, encouraging cooperation when others contribute sufficiently and punishing when they don't. It includes forgiveness to allow for resumption of cooperation if others adjust their behavior.
'''

description_COLLECTIVE_95 = '''
**Strategy Description: Adaptive Collective Cooperation (ACC) Strategy**

**Overview:**
The ACC strategy is designed to balance individual incentives with collective welfare in a repeated Public Goods Game. It encourages cooperation while adapting to others' behavior, ensuring resilience against various opponent strategies.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Reason:** Initiates cooperation, setting a positive tone and encouraging others to reciprocate.

2. **Subsequent Rounds:**
   - **Monitor Cooperation Rate:** Track the average contribution of all players over the last few rounds (e.g., last 3 rounds).
   - **Threshold Check:** If the average contribution is above a threshold (e.g., 0.6), continue Cooperating.
   - **Adjustment:** If the average falls below the threshold, switch to Defecting for the next round.
   - **Forgiveness:** If, after defecting, the average contribution rises above the threshold in subsequent rounds, revert to Cooperating.

3. **Final Round:**
   - **Action:** Defect (D).
   - **Reason:** Maximize personal payoff as future consequences are absent, aligning with the temptation in the last round.

**Edge Cases Handling:**
- **Last Round:** Predefined to Defect, ensuring no exploitation risk.
- **Forgiveness Mechanism:** Allows reverting to cooperation if others improve their contributions, preventing perpetual defection.

**Collective Alignment:**
The ACC strategy is designed for all players to follow, fostering a unified approach that adapts collectively, enhancing resilience against diverse opponent behaviors.

This strategy aims to maintain cooperation where beneficial while safeguarding against exploitation, ensuring a balanced and adaptive approach in the tournament.
'''

description_COLLECTIVE_96 = '''
**Public Goods Game (PGG) Strategy: "k-Threshold Cooperation"**

**Overview:**
The strategy is designed to encourage sustained cooperation in the repeated Public Goods Game by conditioning contributions on the collective behavior of all players in the previous round. It uses a threshold based on the game's multiplier \( k \) to decide whether to Cooperate (C) or Defect (D).

**Decision Rules:**
1. **First Round:** Cooperate (C). This initiates cooperation, encouraging others to follow suit.
2. **Subsequent Rounds:** For each round \( t \), observe the number of contributors \( S_{t-1} \) from the previous round \( t-1 \).
   - If \( S_{t-1} \geq k \), Cooperate (C) in round \( t \).
   - If \( S_{t-1} < k \), Defect (D) in round \( t \).

**Edge Cases:**
- **First Round:** Always Cooperate to seed cooperation.
- **Last Round:** Treat like any other round, as the game is repeated, but if the tournament has a known end, standard rules apply.

**Collective Alignment:**
This strategy aligns all players' actions with the collective outcome by basing decisions on the previous round's contributions. If enough players (at least \( k \)) contributed, cooperation continues. If too many defected (fewer than \( k \)), players defect to incentivize better collective behavior.

This approach promotes a balance between individual incentives and collective welfare, fostering cooperation when beneficial and adjusting when contributions lag.
'''

description_COLLECTIVE_97 = '''
To address the Public Goods Game (PGG) challenge, I propose the **"Adaptive Forgiver" strategy**. This approach balances cooperation with the flexibility to adapt based on others' actions, ensuring robust performance across diverse opponent behaviors.

### Strategy Overview:
1. **First Round Cooperation**: Start by contributing (C) to encourage initial cooperation and maximize collective welfare.
2. **Contribution Monitoring**: Track the number of contributors each round. If at least 50% contribute, continue cooperating.
3. **Punishment Mechanism**: If contributions fall below 50%, defect in the next round to avoid exploitation.
4. ** Forgiveness**: Resume contributing if contributions rebound, fostering renewed cooperation.
5. **Endgame Strategy**: Defect in the last round to maximize individual payoff, as future repercussions are absent.

### Strategy Details:

1. **First Round Action**:
   - **Contribute (C)**: Initiate cooperation to set a positive tone and encourage reciprocal behavior.

2. **Subsequent Rounds**:
   - **Monitor Contributions**: Evaluate the number of contributors in the previous round.
   - ** Cooperation Threshold**: If 50% or more contribute, continue with C.
   - **Defection Threshold**: If fewer than 50% contribute, switch to defecting (D) to avoid being exploited.
   - **Forgiveness Trigger**: After defecting, return to contributing if contributions meet or exceed the 50% threshold again, allowing for renewal of cooperation.

3. **Endgame Strategy**:
   - **Last Round Action**: Defect (D) to maximize personal gain, as there are no future rounds for punishment.

### Rationale:
- **Initial Cooperation**: Encourages others to reciprocate, laying the groundwork for collective success.
- **Adaptive Response**: Adjusts based on group behavior, penalizing free-riders while remaining open to cooperation when beneficial.
- **Forgiveness**: Promotes resilience by re-engaging when others recommence cooperation, sustaining long-term mutual benefit.
- **Endgame Adjustment**: Recognizes the final round's unique dynamics, optimizing personal payoff without compromising the strategy's overall adaptability.

This strategy is designed to be competitive, fostering cooperation while protecting against exploitation, making it robust against diverse opponent behaviors in a tournament setting.
'''

description_COLLECTIVE_98 = '''
### Strategy Description: "Adaptive Cooperativity with Forgiveness"

**1. Initial Cooperation:**
- **Round 1:** Cooperate (C) to establish a cooperative tone and encourage others to contribute.

**2. Ongoing Strategy:**
- **Cooperation Threshold:** Set a threshold where if at least 70% of players contributed in the previous round, continue cooperating.
- **Defection Response:** If contributions fall below the threshold, defect once to signal dissatisfaction and prompt others to increase contributions.
- **Forgiveness Mechanism:** After defecting once, forgive and return to cooperation if contributions rise above the threshold.

**3. Endgame Handling:**
- **Last Three Rounds:** Begin reducing contributions by defecting to avoid exploitation, as future interactions are limited.
- **Final Round:** Defect to maximize personal payoff, knowing there's no future punishment.

**4. Edge Cases:**
- **Single Player or All Defections:** Defect to minimize losses, as cooperation offers no benefit.

**5. Responsiveness:**
- Continuously monitor others' actions and adapt responses to maintain balance between cooperation and protection.

This strategy promotes cooperation while safeguarding against exploitation, ensuring a robust approach in various scenarios.
'''

description_COLLECTIVE_99 = '''
**Strategy Description: "Adaptive Collective Cooperation with Gradual Punishment"**

**1. Decision Rules:**
- **First Round:** Cooperate (C) by contributing 1 token to encourage initial cooperation and maximize collective welfare.
- **Subsequent Rounds:** 
  - Calculate the **average cooperation rate** of all players in the previous round(s) based on the history of their actions.
  - **Threshold:** If the cooperation rate is above a certain threshold (e.g., 50%), continue cooperating (C). If it falls below the threshold, defect (D) in the next round to punish free-riders.
  - **Gradual Punishment:** If defection is observed in a round, decrease the cooperation threshold gradually over subsequent rounds to become stricter on punishment.
- **Last Round:** If the punishment phase is ongoing, defect (D) to avoid being exploited.
- **Edge Cases:** If all players cooperated in the previous round, continue cooperating to maintain high collective payoff.

**2. Handling Edge Cases:**
- **First Round:** Always cooperate to test willingness to cooperate.
- **Last Round:** Defect if punishment is in progress; otherwise, cooperate if others did so in the penultimate round.
- **All Players Cooperate:** Continue cooperating to sustain high collective payoffs.
- **All Players Defect:** Defect to avoid being the only contributor.

**3. Collective Alignment:**
- The strategy prioritizes collective welfare by encouraging cooperation unless others defect, balancing individual and group interests.
- It uses gradual punishment to deter free-riding, aiming to maintain cooperation over time.

**Pseudocode Overview:**
```
threshold = 0.5
current_round = 1
cooperation_rates = []
punishment_phase = False

while game not finished:
    if current_round == 1:
        contribute 1
    else:
        calculate avg_coop = average of cooperation_rates
        if avg_coop >= threshold and not punishment_phase:
            contribute 1
        else:
            contribute 0
            punishment_phase = True
            adjust threshold down

    if last_round:
        if punishment_phase:
            contribute 0
        else:
            contribute 1

    update cooperation_rates and threshold based on history
    current_round += 1
```

This strategy is designed to be adaptive and robust, encouraging cooperation while protecting against exploitation, aligning with the collective mindset of maximizing group welfare.
'''

description_COLLECTIVE_100 = '''

'''

description_COLLECTIVE_101 = '''
**Strategy: Adaptive Collective Reciprocity (ACR)**

**Overview:**  
This strategy promotes initial cooperation, reciprocates collective behavior, and adapts to group dynamics to balance individual and collective welfare. It is designed to foster cooperation while safeguarding against exploitation.

---

**1. Decision Rules:**

- **First Round:**  
  Contribute fully (C). Start with cooperation to signal willingness to collaborate and maximize potential collective payoff.

- **Subsequent Rounds (Before Last Round):**  
  Observe the group's average cooperation rate in the previous round:  
  - If the average contribution rate (proportion of players who contributed) is above 50%, contribute fully (C).  
  - If the average contribution rate is 50% or below, defect (D).  
  Additionally, if fewer than half of the players contributed in the previous round, defect in the current round.  

- **Last Round:**  
  Defect (D). Since there are no future consequences or opportunities for reciprocity, prioritize individual gain.

---

**2. Handling Edge Cases:**

- **First Round:**  
  Contribute fully to establish cooperation.  

- **Last Round:**  
  Defect to maximize personal payoff, as future reciprocity is no longer possible.  

- **If All Others Defect:**  
  If all other players consistently defect, defect in response to avoid being exploited.  

- **If Others Cooperate:**  
  Reciprocate cooperation to maintain collective welfare.  

---

**3. Collective Mindset:**  
This strategy aligns with the collective interest by contributing when others contribute and defecting when others defect. It balances individual incentives with group benefits, ensuring fairness and reciprocity.  

---

**Pseudocode Explanation:**  
```
def adaptive_collective_reciprocity(current_round, total_rounds, group_actions, n):
    if current_round == 1:
        return "C"  # Cooperate in the first round
    else:
        # Calculate the average contribution rate in the previous round
        contributions = [action == "C" for action in group_actions[-1]]
        avg_contribution = sum(contributions) / n
        
        if current_round < total_rounds:  # Not the last round
            if avg_contribution > 0.5:
                return "C"  # Cooperate if others cooperated
            else:
                return "D"  # Defect if others did not cooperate sufficiently
        else:
            return "D"  # Defect in the last round
```

---

This strategy is robust, adaptive, and collectively oriented, balancing individual and group interests while responding to the behavior of others.
'''

description_COLLECTIVE_102 = '''
**Public Goods Game Strategy: Adaptive Collective Contribution (ACC)**

**1. Decision Rules:**
   - **Round 1:** Always Cooperate (C). This initiates the game with a cooperative tone, encouraging others to follow suit.
   - **Subsequent Rounds:** 
     - Calculate the average contribution of all other players from the previous round.
     - If this average is above a threshold of 0.5, Contribute (C). This rewards the group's cooperative behavior and reinforces continued contributions.
     - If the average is below 0.5, Defect (D). This sanctions free-riding behavior, encouraging others to contribute more in future rounds.
   - **Forgiveness Mechanism:** If after defecting, the group's average contribution in the next round meets or exceeds the 0.5 threshold, switch back to Contributing (C). This allows the strategy to adapt and recover cooperation if others begin contributing again.

**2. Handling Edge Cases:**
   - **First Round:** Start with Cooperation (C) to establish a cooperative baseline.
   - **Subsequent Rounds:** Use the adaptive rule based on the previous round's contributions.
   - **Last Round:** Continue using the same strategy as other rounds, as the adaptive mechanism ensures appropriate behavior without special casing the last round, considering the game's repetitive nature.

**3. Collective Alignment:**
   - The strategy is designed to align with the collective mindset by encouraging cooperation when beneficial and defecting to deter free-riding. It adapts based on group behavior, fostering a balance between individual and collective welfare.

This strategy promotes a dynamic approach, encouraging cooperation while being robust against various opponent behaviors, ensuring a balance between contributing to the public good and protecting individual interests.
'''

description_COLLECTIVE_103 = '''
**Public Goods Game Strategy: Adaptive Contributions Based on Previous Round's Total**

**Overview:**
This strategy encourages cooperation in the Public Goods Game by conditioning contributions on the collective behavior observed in the previous round. It aims to balance individual incentives with collective welfare, adapting based on the level of contributions from all players.

**Strategy Description:**

1. **First Round Action:**
   - **Contribute (C):** All players start by contributing 1 token. This maximizes the initial group payoff and sets a cooperative tone.

2. **Subsequent Rounds (2 to r-1):**
   - **Observe Previous Round's Total Contributions (T):** Each player calculates the total number of tokens contributed in the previous round.
   - **Contribution Rule:**
     - If T ≥ k, where k is the multiplier provided in the game parameters, the player contributes (C).
     - If T < k, the player defects (D).

3. **Last Round Action:**
   - **Defect (D):** In the final round, all players defect to maximize their individual payoff, knowing there are no future consequences.

**Rationale:**
- **Start Cooperatively:** The first round sets a baseline of cooperation, encouraging others to follow suit.
- **Adaptive Response:** By conditioning contributions on the previous round's total, players reward cooperation and sanction defection collectively.
- **Final Round Realism:** Acknowledging the endgame scenario, players defect to avoid the sucker's payoff, aligning with rational choice in the last interaction.

This strategy is designed to be robust against various opponent behaviors, promoting sustained cooperation while safeguarding against exploitation.
'''

description_COLLECTIVE_104 = '''
**Collective Strategy: Threshold-Based Cooperation with Endgame Defection**

1. **First Round:** Contribute to initialize cooperation.
2. **Subsequent Rounds (excluding the last):** Contribute if the number of contributors in the previous round exceeds the threshold (n/k); otherwise, defect.
3. **Last Round:** Always defect to maximize individual payoff in the absence of future consequences.

This strategy balances cooperation and self-interest, adapting based on the group's past actions to maintain collective welfare while safeguarding individual interests in the final round.
'''

description_COLLECTIVE_105 = '''
To address the challenges of the Public Goods Game (PGG), here's a strategic approach that balances individual and collective interests:

**Strategy: Cooperative Reciprocity with Forgiveness**

1. **First Round:**
   - **Action:** Contribute (C)
   - **Rationale:** Initiates cooperation, setting a positive tone and encouraging others to contribute.

2. **Subsequent Rounds:**
   - **Decision Rule:** Observe the contributions of all players in the previous round.
   - **Contribute (C):** If at least 50% of players contributed in the previous round.
   - **Defect (D):** If fewer than 50% contributed, to avoid being exploited.
   - **Adaptive Adjustment:** If some players defected, defect in the next round to signal displeasure, but forgive after a few cooperative signs.

3. **Last Round:**
   - **Action:** Contribute (C) if the majority of previous rounds had at least 50% contributions.
   - **Rationale:** Rewards past cooperation, encouraging consistency, though defects if cooperation was low to avoid exploitation.

**Summary:**
This strategy starts cooperatively, adaptively responds to group behavior, punishes defection without being overly punitive, and strategically decides in the last round based on overall cooperation history. It promotes mutual benefit while safeguarding against exploitation.
'''

description_COLLECTIVE_106 = '''
**Optimistic Reciprocation Strategy for Public Goods Game**

**Objective:**  
To foster cooperation while defending against exploitation by adapting to group behavior dynamically.

**Structure:**

1. **First Round:**  
   - **Action:** Cooperate (C).  
   - **Rationale:** Initiate cooperation to set a positive tone and encourage others to follow suit.

2. **Subsequent Rounds:**  
   - **Assessment:** Calculate the average contribution rate (ACR) from the previous round.  
   - **Decision:**  
     - If ACR ≥ 50%, Cooperate (C) to reciprocate and sustain cooperation.  
     - If ACR < 50%, Defect (D) to avoid exploitation and signal displeasure.  

3. **Last Round:**  
   - **Assessment:** Evaluate the majority of contributions across all previous rounds.  
   - **Decision:**  
     - Cooperate (C) if the majority of rounds had ACR ≥ 50%.  
     - Defect (D) otherwise, ensuring a strategic conclusion based on overall behavior trends.

4. **Adaptive Adjustment:**  
   - Monitor for shifts in others' behavior. If cooperation resumes after defection, revert to Cooperate (C).  
   - If others remain non-responsive, maintain Defect (D) to protect against continued exploitation.

**Edge Cases Handling:**

- **No Pre-defined End:** Continue assessing ACR from the last round to inform future actions.  
- **Unresponsive Behavior:** Defect to prevent being exploited if others do not reciprocate cooperation.

**Summary:**  
This strategy begins with optimism, adapts based on collective behavior, punishes lack of cooperation, and remains open to re-engaging with cooperative members. It balances the need for individual protection with the desire to enhance group welfare.
'''

description_COLLECTIVE_107 = '''
**Strategy for Public Goods Game (PGG)**

1. **Initial Cooperation**: Start by contributing in the first round to set a cooperative tone and encourage others to do the same.

2. **Reciprocal Cooperation**: In subsequent rounds, base your contribution decision on the group's previous round behavior. If a majority (more than 50%) contributed in the previous round, continue contributing. If fewer than 50% contributed, switch to defecting.

3. **Punishment Mechanism**: If the group's average contribution falls below a threshold (e.g., 50%), defect until the group's contribution rate improves. This acts as a punishment phase to discourage persistent defection.

4. ** Forgiveness**: If, after a period of low contributions, the group's contribution rate improves (back to 50% or more), resume contributing. This gives others a chance to reform and maintains flexibility.

5. **Last Round Handling**: In the final round, decide based on the group's overall cooperation. If the group has maintained sufficient cooperation throughout the game, contribute. If the group's cooperation has been lacking, defect to avoid being exploited.

This strategy promotes cooperation when others reciprocate, punishes defection to maintain fairness, and adapts to changing group dynamics, ensuring robustness against various behaviors.
'''

description_COLLECTIVE_108 = '''
**Collective Strategy for Public Goods Game**

**1. Decision Rules:**
   - **First Round:** Always contribute (C). This sets a cooperative tone and encourages initial collective investment.
   - **Subsequent Rounds:** Determine contribution based on the previous round's behavior:
     - Calculate the average contribution of all players.
     - If the average contribution was above 50%, contribute (C) to reinforce cooperation.
     - If 50% or below, defect (D) as a form of punishment.
     - If all players defected in the previous round, contribute (C) to attempt to reset cooperation.

**2. Handling Edge Cases:**
   - **First Round:** Contribute to establish cooperation.
   - **Last Round:** Follow the same strategy as other rounds, using the previous round's history to decide, promoting consistent behavior without assuming the end.

**3. Collective Mindset:**
   - The strategy aligns with collective welfare by encouraging cooperation and using defection as a punishment mechanism. It allows for recovery after defection, promoting sustained cooperation over time.

This approach fosters a balance between reciprocity and forgiveness, ensuring adaptability and robustness against various opponent behaviors.
'''

description_COLLECTIVE_109 = '''
**Strategy Description:**

1. **Initial Cooperation (First Round):** Begin by cooperating (C) to establish a cooperative tone and encourage others to reciprocate.

2. **Reciprocal Cooperation:** In subsequent rounds, cooperate if at least 50% of players cooperated in the previous round. This reinforces mutual cooperation.

3. **Gradual Punishment:** If cooperation drops below 50%, defect (D) for up to 3 rounds to penalize free-riding, then revert to cooperating if cooperation levels recover.

4. **Endgame Strategy:** In the last 3 rounds, if overall cooperation has been high, continue cooperating; otherwise, defect to maximize individual gain.

This strategy balances individual incentives with collective benefits, fostering cooperation while deterring defection. It adapts based on collective history, ensuring robustness without assuming coordination.
'''

description_COLLECTIVE_110 = '''
### Strategy Description: Conditional Cooperation with Punishment and Forgiveness

1. **First Round Cooperation**: Start by cooperating (C) in the first round to set a cooperative tone and encourage others to follow suit.

2. **Contribution Rule**: For each subsequent round, calculate the average contribution of all other players in the previous round. If the average contribution was at least 0.5 (i.e., at least half of the other players cooperated), then cooperate (C) in the current round. If the average contribution was less than 0.5, then defect (D) to punish the lack of cooperation.

3. **Forgiveness Mechanism**: If in the previous round, fewer than half of the other players cooperated, there is a 20% chance to cooperate (C) regardless of the average contribution. This introduces forgiveness, allowing the group a chance to reset cooperation.

4. **Final Round Decision**: In the last round, defect (D) to maximize individual payoffs, as there are no future interactions to influence.

This strategy balances cooperation and punishment, promoting collective welfare while being adaptive to others' actions.
'''

description_COLLECTIVE_111 = '''
**Collective Strategy: "Adaptive Cooperation with Forgiveness"**

**Overview:**  
This strategy encourages cooperation while adapting to the group's behavior, ensuring robustness against free-riding and fostering collective welfare. It uses past actions to inform future decisions and incorporates forgiveness to recover cooperation after temporary defections.

---

**1. Decision Rules (When to Cooperate vs Defect):**  
- **First Round:** Always **Cooperate (C)**. This sets a cooperative tone and encourages others to reciprocate.  
- **Subsequent Rounds:**  
  - Calculate the average cooperation rate of **other players** in the previous round. Cooperation rate is the fraction of players (excluding yourself) who contributed (C).  
  - If the average cooperation rate of other players in the previous round is above a threshold (e.g., 50%), **Cooperate (C)**.  
  - If the average cooperation rate of other players in the previous round is below the threshold, **Defect (D)** to punish free-riding.  
  - If all other players defected in the previous round, **Defect (D)** to avoid being exploited.  

**Forgiveness Mechanism:**  
- If the group's cooperation rate improves in a subsequent round (i.e., more players cooperate than in the previous round), reintroduce cooperation gradually. Specifically, contribute (C) if at least half of the group contributed in the most recent round.  

---

**2. Edge Cases:**  
- **First Round:** Always **Cooperate (C)** to signal goodwill.  
- **Last Round:** Defect (D) if the round is known to be the final one, as there is no future punishment to fear.  
- **All Others Defecting:** If all other players consistently defect, **Defect (D)** to minimize personal losses.  
- **All Others Cooperating:** If all other players consistently cooperate, **Cooperate (C)** to maximize collective payoffs.  

---

**3. Collective Alignment:**  
This strategy aligns with the collective mindset by prioritizing mutual benefits while incorporating mechanisms to deter free-riding. It balances cooperation with self-protection, ensuring the strategy remains robust against a wide range of behaviors. Its adaptive nature allows it to evolve with the group's dynamics, fostering cooperation when possible and defending against exploitation when necessary.
'''

description_COLLECTIVE_112 = '''
**Strategy: Adaptive Collective Cooperation (ACC)**

**1. Decision Rules:**
- **Initial Round:** Cooperate (C) to establish a cooperative tone.
- **Subsequent Rounds:** Mirror the majority's previous actions. If most players cooperated, continue cooperating; if most defected, defect.
- **Retaliation:** If others defect, defect in the next round. If others cooperate after retaliation, revert to cooperation.
- **Final Round:** Always defect, as there are no future interactions to influence.

**2. Handling Edge Cases:**
- **First Round:** Start with cooperation.
- **Last Round:** Defect to maximize personal payoff.

**3. Collective Alignment:** The strategy is designed to encourage mutual cooperation while punishing defection, ensuring a balance between collective benefit and individual protection. Players following ACC collectively Signal willingness to cooperate but will adapt if others defect, ensuring robustness against various behaviors.
'''

description_COLLECTIVE_113 = '''
**Collective Reciprocity Strategy for Public Goods Game**

1. **Initial Cooperation**: In the first round, all players contribute (C) to establish a cooperative foundation.

2. **Reciprocal Adaption**: For each subsequent round, players observe the previous round's contributions. If at least 50% of players contributed, they continue to contribute (C). If fewer than 50% contributed, they defect (D).

3. **Forgiveness Mechanism**: If the group's contribution rate drops below 50%, players defect in the next round. However, if in the following round, contributions rebound to at least 50%, players revert to contributing (C).

4. **Final Round Maximization**: In the last round, if the contribution rate was 100% in the previous round, all players contribute (C) to maximize the final payoff.

This strategy promotes sustained cooperation by reciprocating the group's behavior, adaptively responding to collective actions, and incorporating forgiveness to re-establish cooperation when possible. It ensures the strategy is robust, adaptive, and aligned with the collective welfare.
'''

description_COLLECTIVE_114 = '''
**Strategy Description:**

1. **Initial Cooperation**: In the first round, the strategy begins by cooperating (C), contributing 1 token to the public good.

2. **Adaptive Decision-Making**: For each subsequent round, the strategy calculates the total contributions from all players in the previous round.

3. **Threshold-Based Cooperation**:
   - If the total contributions in the previous round exceed the threshold \( \frac{n}{k} \), where \( n \) is the number of players and \( k \) is the multiplier, the strategy continues to cooperate in the current round.
   - If the total contributions fall below this threshold, the strategy defects (D) in the current round.

4. **Dynamic Adjustment**: After defecting, the strategy continues to monitor the total contributions. If in a subsequent round the contributions rise above the threshold again, the strategy switches back to cooperating.

This strategy encourages sustained cooperation by rewarding sufficient contributions and punishing insufficient ones, adapting dynamically based on collective behavior.
'''

description_COLLECTIVE_115 = '''
**Strategy Description:**

The strategy is designed to encourage cooperation while protecting against exploitation, adapting based on past contributions and game parameters. It follows these rules:

1. **Initial Cooperation:** In the first round, always contribute (C) to establish a cooperative foundation.

2. **Adaptive Cooperation:** For each subsequent round (excluding the last), evaluate the total contributions from the previous round. If the sum of contributions in the previous round is at least \( \frac{n}{k} \) (where \( n \) is the number of players and \( k \) is the multiplier), then contribute (C). Otherwise, defect (D).

3. **Final Round Defection:** In the last round, always defect (D) since future reciprocity is no longer a factor.

This strategy ensures that cooperation continues as long as it remains beneficial, adjusting based on others' past actions, and avoids potential exploitation in the final round.
'''

description_COLLECTIVE_116 = '''
**Public Goods Game (PGG) Strategy: "Adaptive Cooperation"**

**1. Decision Rules:**
- **First Round:** Cooperate (C). Contribute 1 token to set a cooperative tone and encourage others to follow suit.
- **Subsequent Rounds:** Cooperate in the current round if the average contribution from all players in the previous round was 50% or higher. Otherwise, defect (D).
- **Final Round:** Always defect (D) to maximize personal gain, as there are no future consequences.

**2. Handling Edge Cases:**
- **First Round:** Start with cooperation to foster a positive environment.
- **Last Round:** Defect to maximize immediate payoff since there's no future interaction.

**3. Collective Alignment:**
- **Observation and Adaptation:** After each round, observe the average contribution. If it meets or exceeds 50%, continue contributing; otherwise, switch to defection.
- **Forgiveness Mechanism:** If contributions increase after a round of low cooperation, revert to cooperating, allowing for recovery of collective effort.

This strategy is designed to be simple, adaptive, and robust, encouraging initial cooperation while adapting to others' behaviors and handling edge cases effectively.
'''

description_COLLECTIVE_117 = '''
**Strategy Name: Conditional Cooperate (CC)**

**Strategy Description:**

1. **First Round Decision:**
   - Always Cooperate (C) in the first round to initiate collaboration and establish a cooperative norm.

2. **Subsequent Rounds Decision:**
   - After each round, observe the average contribution of all players in the previous round.
   - If the average contribution was at least 0.5 (i.e., at least half of the players Cooperated), then Cooperate in the next round.
   - If the average contribution was below 0.5, then Defect in the next round.

**Design Rationale:**

- **Collective Mindset:** Encourages mutual cooperation by rewarding previous cooperation and penalizing defection, aligning individual actions with collective welfare.
- **Adaptability:** Responsive to the group's past behavior, adjusting contributions based on observed cooperation levels.
- **Robustness:** Simple yet effective, handling various opponent behaviors by mirroring group dynamics without assuming coordination.
- **Edge Cases:** Handles the first round by initiating cooperation and addresses subsequent rounds by reacting to the group's recent behavior, ensuring consistent application regardless of the round number.

**Pseudocode:**

if round == 1:
    choose C
else:
    avg_contribution = sum of previous contributions / n
    if avg_contribution >= 0.5:
        choose C
    else:
        choose D

This strategy promotes sustained cooperation by rewarding collective effort and discouraging free-riding, aiming to maximize group payoff through reciprocal behavior.
'''

description_COLLECTIVE_118 = '''

'''

description_COLLECTIVE_119 = '''
**Strategy Name: Adaptive Reciprocity with Endgame Adjustment**

**Strategy Description:**

- **First Round:** Cooperate (C) to establish a cooperative precedent.
- **Subsequent Rounds:** 
  - If a majority (e.g., 50% or more) of players contributed in the previous round, Cooperate.
  - If less than the majority contributed, Defect to avoid exploitation.
  - If a player defected in the previous round, retaliate by Defecting this round, but return to cooperating if they contribute again afterward.
- **Last Round:** Defect to maximize personal gain, as future consequences are absent.

This strategy encourages cooperation while protecting against exploitation and adjusts behavior based on collective past actions, ensuring a balance between reciprocity and self-interest.
'''

description_COLLECTIVE_120 = '''
**Strategy: Cooperative Reciprocity with Forgiveness and Endgame Adaptation**

1. **Initial Cooperation**: In the first round, contribute 1 token to encourage mutual cooperation from the start.

2. **Reciprocation**: 
   - **Cooperation**: If all players contributed in the previous round, continue contributing.
   - **Gradual Escalation**: If any player defected, defect once in the next round to signal the impact of their action.

3. **Forgiveness**: After defecting once, return to contributing in the subsequent round to allow others a chance to cooperation again, preventing prolonged defection cycles.

4. **Endgame Strategy**:
   - In the penultimate round, reduce contributions if others have shown a pattern of defection, anticipating potential endgame exploitation.
   - In the final round, contribute if others have been cooperative overall; otherwise, defect to avoid being exploited.

This strategy balances cooperation with adaptive responses to others' actions, promoting collective welfare while safeguarding against exploitation, especially in the game's latter stages.
'''

description_COLLECTIVE_121 = '''
**Strategy: Adaptive Collective Cooperation**

1. **First Round Decision:**  
   - Always Cooperate. This sets a cooperative tone and encourages others to follow suit.

2. **Subsequent Rounds Decision:**  
   - In each round after the first, observe the contributions from the previous round.  
   - **Cooperate** if at least 50% of the players contributed in the previous round.  
   - **Defect** if fewer than 50% contributed.  

3. **Last Round Handling:**  
   - Apply the same rule as other rounds: base the decision on the majority contribution of the previous round.  

This strategy promotes a collective mindset by rewarding cooperation when others contribute and adapting when they don't, fostering a balance between individual and group welfare.
'''

description_COLLECTIVE_122 = '''
**Strategy: Adaptive Cooperation with Punishment and Forgiveness**

---

**Overview:**
This strategy encourages cooperation while adapting to the group's behavior. It starts cooperatively, punishes defection, and forgives when cooperation resumes.

**Decision Rules:**

1. **First Round:**
   - **Action:** Contribute (C). Begin with cooperation to maximize collective payoff.

2. **Subsequent Rounds:**
   - **Action:** Based on the previous round's average contribution.
     - If the average contribution was **above 50%**, Contribute (C).
     - If the average contribution was **50% or below**, Defect (D).

3. **Edge Cases:**
   - **Last Round:** Follow the same strategy. The absence of future rounds doesn't change behavior.
   - **Persistent Defection:** If others defect, defect as well but monitor for cooperation rebound.
   - **Cooperation Rebound:** If others start contributing again, switch back to contributing.

**Rationale:**
- Starts cooperatively to encourage collective welfare.
- Adapts based on group behavior, rewarding cooperation and punishing defection.
- Forgiving nature allows the group to recover cooperation without perpetual defection.

This strategy balances individual incentives with collective benefits, promoting a robust and adaptive approach to the repeated PGG.
'''

description_COLLECTIVE_123 = '''
To address the challenge of designing a robust and adaptive strategy for a repeated Public Goods Game, I propose the following approach:

### Strategy Description: Conditional Cooperation Based on Contribution Threshold (CCCT)

1. **Initial Cooperation**: In the first round, all players contribute (C). This establishes a baseline of cooperation and encourages others to follow suit.

2. **Contribution Threshold**: For each subsequent round, players determine their action based on the number of contributors in the previous round. The threshold for cooperation is set to the multiplier parameter, k. Specifically, if at least k players contributed in the previous round, each player contributes again. Otherwise, they defect.

3. **Punishment Mechanism**: If fewer than k players contributed in the previous round, players defect in the current round. This acts as a punishment to discourage excessive defection.

4. **Adaptation and Robustness**: The strategy adapts automatically to the game parameters (n and k) and the history of contributions. It is robust because it only requires the number of contributions from the previous round, making it easy to implement without complex calculations.

5. **Edge Cases Handling**: The strategy does not require prior knowledge of the total number of rounds, making it suitable for both known and unknown round counts. In the last round, if participants base their decision on the previous round's contributions, the strategy remains consistent, although deflection is possible without future repercussions.

### Summary

This strategy encourages sustained cooperation by rewarding sufficient contributions and punishing defection proportionally. It is simple, adaptive, and aligns with a collective mindset, promoting collective welfare while deterring free-riding.

**Pseudocode:**

```
Function Strategy(n, k, history):
    if no history:
        return Contribute
    else:
        previous_contributions = count of contributions in last round
        if previous_contributions >= k:
            return Contribute
        else:
            return Defect
```

This approach balances cooperation and punishment, leveraging game parameters to maintain a robust and adaptive strategy.
'''

description_COLLECTIVE_124 = '''
**Strategy Description: Group-Reciprocity with Threshold (GRT)**

1. **First Round Action**: In the first round, all players contribute (C). This sets a cooperative tone and encourages others to reciprocate.

2. **Subsequent Rounds (2 to r-1)**: 
   - After the first round, each player calculates the total contributions from all players in the previous round.
   - If the total contributions meet or exceed a threshold of half the group size (n/2), the player contributes (C) in the current round.
   - If the total contributions are below this threshold, the player defects (D).

3. **Last Round Action (Round r)**: In the final round, all players defect (D), as there are no future rounds to influence with cooperation.

This strategy promotes conditional cooperation based on the group's previous behavior, encouraging collective responsibility while adapting to others' actions. It handles edge cases by prescribing specific actions for the first and last rounds, ensuring a balance between cooperation and self-interest.
'''

description_COLLECTIVE_125 = '''
To address the strategic dilemma in the Public Goods Game (PGG), I propose a collective strategy that encourages cooperation while adaptively responding to group behavior.

**Strategy: Cooperative Punisher with Consistency**

1. **First Round**: Always contribute (C). This sets a cooperative tone from the beginning.

2. **Subsequent Rounds (including the last round)**:
   - Calculate the average contribution of all players in the previous round.
   - If the average contribution is at least \( \frac{k}{n} \), where \( k \) is the multiplier and \( n \) is the number of players, contribute (C) in the current round.
   - If the average contribution is below \( \frac{k}{n} \), defect (D) in the current round to signal dissatisfaction and encourage higher contributions.

This strategy consistently applies the same rule across all rounds, ensuring that cooperation is maintained as long as the group meets the contribution threshold. It adaptively punishes low contributions without leading to perpetual defection, promoting a balance between individual and collective welfare.
'''

description_COLLECTIVE_126 = '''
**Strategy Description:**

1. **Initial Rounds (Rounds 1 and 2):**  
   Cooperate (C) in the first two rounds to establish a norm of cooperation and maximize initial collective welfare.

2. **Monitoring Contributions:**  
   After Round 2, calculate the average contribution rate of all players in the previous round. If >=80% contributed, continue cooperating. If <80%, defect in the next round.

3. **Punishment and Reform:**  
   If you defected in the previous round, cooperate in the current round if at least 80% of players cooperated last round. Otherwise, continue defecting.

4. **Endgame Handling:**  
   In the final round, defect to maximize personal payoff, anticipating others may do the same.

This strategy promotes cooperation, punishes defection, and adapts based on collective behavior, ensuring robustness in various scenarios.
'''

description_COLLECTIVE_127 = '''
**Strategy: Adaptive Collective Cooperation (ACC)**

**1. Decision Rules:**
   - **Cooperation Phase:** Always start by contributing (C) in the first round. Continue contributing if the majority of players contributed in the previous round.
   - **Assessment Phase:** After each round, assess the number of contributors. If at least 50% contributed, continue cooperating.
   - **Punishment Phase:** If fewer than 50% contributed, defect (D) in the next round to signal dissatisfaction.
   - **Restart Cooperation:** After defecting once, return to contributing to restart potential cooperation.

**2. Handling Edge Cases:**
   - **First Round:** Always contribute.
   - **Last Round:** Continue the strategy as usual; if assessment indicates cooperation, contribute, otherwise defect. No special action needed beyond the strategy's phases.

**3. Collective Mindset:**
   - Aligns with promoting group welfare by encouraging contributions and punishing defection to maintain fairness and cooperation.

This strategy balances cooperation and punishment, promoting collective welfare while protecting individual interests, adaptable across various opponent behaviors.
'''

description_COLLECTIVE_128 = '''
The proposed strategy is designed to balance individual incentives with collective welfare in the Public Goods Game (PGG) through an adaptive and reciprocal approach. Here's the structured strategy:

### Strategy: Collective Reciprocity with Adaptive Threshold

**1. First Round Decision:**
- **Action:** Cooperate (Contribute 1 token).
- **Rationale:** Initiates cooperation, setting a foundation for potential mutual contributions.

**2. Subsequent Rounds (Rounds 2 to t-1):**
- **Action:** Calculate the average contribution rate from the previous round. This is the ratio of total contributions to the number of players (n).
- **Decision Rule:** If the average contribution rate meets or exceeds the threshold (k/n), where k is the multiplier, contribute (C). If it falls below, defect (D).

**3. Last Round Decision:**
- **Action:** Utilize the historical average contribution rate from all previous rounds.
- **Decision Rule:** Contribute if the historical average meets or exceeds the threshold (k/n), otherwise defect.

**4. Edge Cases Handling:**
- **First Round:** Always cooperate to establish a cooperative baseline.
- **Last Round:** Treat similarly to other rounds based on historical data to maintain consistency and encourage sustained cooperation.

**Robustness and Adaptability:**
- The strategy adapts to the behavior of other players, rewarding cooperation with continued contributions and responding to defection by reducing contributions.
- It is collective, as all players following this strategy will act uniformly based on shared history, promoting implicit coordination.

This approach encourages cooperation by linking contributions directly to past behavior, using game parameters to set expectations, and providing clear decision rules for all scenarios.
'''

description_EXPLOITATIVE_1 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

1. **First Round Decision:**
   - **Action:** Cooperate (Contribute 1 token)
   - **Rationale:** Start by contributing to encourage initial cooperation and observe others' reactions.

2. **Subsequent Rounds (Before Last):**
   - **Assessment:** Calculate the average contribution rate of all players in the previous round.
   - **Threshold:** If the average contribution rate is above 50%, cooperate; otherwise, defect.
   - **Recent Behavior Influence:** If the majority of players cooperated in the most recent round, cooperate; otherwise, defect.

3. **Last Round Decision:**
   - **Action:** Defect (Contribute 0 tokens)
   - **Rationale:** Maximize personal payoff since there are no future interactions to influence.

**Additional Considerations:**
- **Handling Inconsistent Behavior:** If opponents' contributions vary significantly, err on the side of caution by defecting to avoid exploitation.

This strategy adapts to opponents' behavior, encouraging cooperation when beneficial while exploiting when others do not reciprocate, ensuring a balance between cooperation and self-interest.
'''

description_EXPLOITATIVE_2 = '''
**Strategy Description: Adaptive Cooperation with Final Round Defection**

1. **First Round:** Cooperate (C) to encourage initial group cooperation.
2. **Rounds 2 to r-1:**
   - Calculate the average contribution (avg_c) of all players in the previous round.
   - If avg_c > 0.5, cooperate (C) to reward collective contribution.
   - If avg_c <= 0.5, defect (D) to punish insufficient cooperation.
3. **Last Round (Round r):** Defect (D) to maximize personal payoff, anticipating no future consequences.

This strategy rewards cooperation when others contribute sufficiently while protecting against exploitation, especially in the final round.
'''

description_EXPLOITATIVE_3 = '''
**Strategy: Adaptive Cooperation with Punishment (ACPP)**

1. **First Round Cooperation**: Start by Cooperating (C) to set a cooperative precedent and encourage others to follow suit.

2. **Contribution Threshold Check**: In each subsequent round, calculate the average contribution rate of other players from the previous round. If this average is above 50%, continue to Cooperate.

3. **Defection Response**: If the average contribution falls to 50% or below, switch to Defecting (D) to avoid exploitation. This Punishment phase is active for one round.

4. **Re-evaluation Post-Punishment**: After defecting, reassess others' contributions. If they have increased their contribution rate above 50%, resume Cooperating. If not, continue Defecting to maintain thepunishment.

5. **Last Round 'Carrot' Approach**: Cooperate in the final round to potentially maximize mutual benefits, assuming others might reciprocate the cooperation.

This strategy balances cooperation and punishment, adapts to others' behaviors, and seeks to exploit their willingness to contribute by rewarding cooperation and penalizing defection.
'''

description_EXPLOITATIVE_4 = '''
**Strategy Name: Adaptive Threshold Cooperation (ATC)**

**Overview:**
ATC is an exploitative strategy designed for the repeated Public Goods Game, aiming to maximize individual payoff by adaptively responding to others' behavior.

**Decision Rules:**

1. **First Round:**
   - Always **Contribute (C)** to initiate cooperation and gauge others' reactions.

2. **Subsequent Rounds:**
   - Calculate the **average contribution rate** of all players from the previous round. This is the proportion of players who contributed.
   - **Contribute (C)** if the average contribution rate is **50% or higher**.
   - **Defect (D)** if the average contribution rate is **below 50%**.

3. **Last Round:**
   - If the majority of previous rounds had an average contribution rate of **50% or higher**, **Contribute (C)**.
   - Otherwise, **Defect (D)**.

**Rationale:**
- **Exploitation:** By contributing when a majority do, the strategy leverages collective cooperation for higher payoffs. Defecting when others don't cooperate avoids exploitation.
- **Adaptability:** Adjusts based on recent behavior, encouraging cooperation when beneficial and protecting against exploitation when others defect.
- **Robustness:** Functions without assuming coordination, making it suitable against diverse strategies.

This strategy balances cooperation and self-interest, aiming to exploit others' cooperative tendencies while protecting against exploitation.
'''

description_EXPLOITATIVE_5 = '''
**Strategy Description: Exploitative Approach in Repeated Public Goods Game**

1. **First Round Action:**
   - Cooperate (C) to observe others' initial behavior.

2. **Subsequent Rounds:**
   - **Calculate Others' Cooperation Rate:** Compute the average contribution rate of all other players from previous rounds. Let this be `avg_others_c`.
   - **Determine Contribution:**
     - If `avg_others_c` is greater than 0.5, Defect (D) to exploit others' cooperation.
     - If `avg_others_c` is 0.5 or less, Defect (D) to protect your own payoff.

3. **Last Round Action:**
   - Always Defect (D) to maximize immediate payoff, as future consequences are irrelevant.

4. **Adaptability:**
   - Continuously update `avg_others_c` each round to reflect recent behavior trends, allowing the strategy to adapt to changing dynamics.

This approach ensures that you exploit others' willingness to contribute while protecting your own interests, adapting based on observed behavior without relying on coordination or shared norms.
'''

description_EXPLOITATIVE_6 = '''
To address the Public Goods Game, the strategy "Adaptive Exploitation" is designed to balance cooperation and self-interest, leveraging past actions to optimize outcomes.

### Adaptive Exploitation Strategy

1. **Initial Contribution**: Cooperate in the first round by contributing 1 token. This initial cooperation sets a baseline to observe others' behaviors.

2. **Contribution Decision**: After the first round, calculate the average contribution rate of other players over the last few rounds. If this average is above a threshold (e.g., 0.5), continue to contribute. If below, defect.

3. **Punishment Mechanism**: Identify instances where other players defected while you contributed. In the next round, defect to punish such behavior, aiming to deter future free-riding.

4. **Endgame Adjustment**: In the last few rounds (e.g., last 3 rounds), assess recent behavior. If most players are defecting, switch to defecting. If contributing, align your action accordingly.

This strategy adaptively responds to others' actions, punishes free-riding, and adjusts near the end, ensuring robustness across various opponent behaviors without assuming coordination.
'''

description_EXPLOITATIVE_7 = '''
To design an exploitative strategy for the Public Goods Game (PGG), we focus on maximizing individual payoffs by adapting to the behavior of others while encouraging cooperation when beneficial. Here's the structured strategy:

1. **First Round Behavior**: Cooperate by contributing 1 token. This initiates a cooperative tone, encouraging others to follow suit.

2. **Subsequent Rounds**:
   - **Analyze Cooperation Rate**: Calculate the average contribution rate of other players from the previous round.
   - **Threshold Check**: If the average is above a selected threshold (e.g., 0.5), defect in the current round. This exploits others' higher cooperation.
   - **Low Cooperation**: If the average is below the threshold, contribute to potentially increase the total contribution and encourage others to cooperate.

3. **Final Round Decision**: Defect to maximize personal gain, as there's no future punishment possible after the last round.

This strategy balances exploitation and cooperation, adapting based on observed behavior to maximize payoffs without assuming coordination with others.
'''

description_EXPLOITATIVE_8 = '''
**Strategy Description: Adaptive Threshold Cooperation (ATC)**

1. **First Round Action:**
   - Contribute (C) to initiate cooperation and observe others' behaviors.

2. **Subsequent Rounds (until the last few rounds):**
   - **Calculate Cooperation Threshold:** Determine the threshold as \( T = \frac{k}{n + 1} \), where \( k \) is the multiplier and \( n \) is the number of players.
   - **Assess Past Contributions:** Compute the average cooperation rate of all players from previous rounds.
   - **Decision Rule:**
     - If the average cooperation rate is equal to or exceeds \( T \), Contribute (C).
     - If the average is below \( T \), Defect (D).

3. **Last Few Rounds (e.g., last 5% of total rounds):**
   - Always Defect (D) to maximize personal payoff, as future punishment is not possible.

**Rationale:**
- **Exploitation:** The strategy exploits others' cooperation by contributing when it's beneficial and defecting when others aren't contributing enough.
- **Adaptation:** Uses past actions to inform current decisions, promoting cooperation when beneficial.
- **Robustness:** Handles various opponent behaviors, from full cooperation to full defection, ensuring the strategy isn't exploited.

This strategy balances cooperation and exploitation, adapting to group behavior while ensuring personal gain, making it effective in a competitive environment.
'''

description_EXPLOITATIVE_9 = '''
The strategy is an adaptive approach that starts with cooperation and then bases its decisions on the previous round's contributions. It aims to exploit the group's tendency to contribute or defect by using a threshold to determine cooperation. Here's the strategy:

1. **First Round**: Contribute to encourage cooperation.
2. **Last Round**: Defect to maximize immediate payoff.
3. **Middle Rounds**: 
   - Calculate the number of contributors (m) from the previous round.
   - Contribute if (k/n) * m ≥ 1; otherwise, defect.

This strategy adapts based on past behavior, balancing exploitation and cooperation to maximize payoffs.
'''

description_EXPLOITATIVE_10 = '''
**Strategic Description: Adaptive Exploitative Strategy for Public Goods Game**

*Strategy Name: Adaptive Exploiter*

**Strategy Overview:**
The Adaptive Exploiter strategy is designed to maximize individual payoffs in a repeated Public Goods Game by exploiting opponents' cooperative tendencies while minimizing losses when others defect. It begins with cooperation to encourage others but adapts based on the observed behavior of the group, switching to defection when exploitation yields higher returns.

**Decision Rules:**

1. **First Round Cooperation:**
   - *Action:* Cooperate (C).
   - *Rationale:* Initiates cooperation to encourage others to contribute, potentially leading to higher subsequent payoffs.

2. **Subsequent Rounds Adaptation:**
   - *Action:* For each round after the first, calculate the average contribution rate of other players (i.e., the proportion of times they contributed) in all previous rounds.
   - *Threshold Check:* If the average contribution rate is greater than or equal to `(n - k)/n`, where `n` is the number of players and `k` is the multiplier, continue Cooperating (C). Otherwise, switch to Defecting (D).
   - *Rationale:* This threshold ensures that cooperation is only maintained when others' contributions sufficiently enhance the public good's benefit to justify personal contribution.

3. **Last Round Defection:**
   - *Action:* Always Defect (D) in the final round.
   - *Rationale:* Without future consequences, maximize immediate payoff by defecting, as there’s no incentive to contribute when no future interactions can be influenced.

**Edge Case Handling:**
- **First Round:** Cooperate to set a cooperative precedent.
- **Last Round:** Defect to maximize immediate gain without future repercussions.
- **Subsequent Rounds:** Adjust strategy dynamically based on others' past actions, fostering cooperation when beneficial and defecting otherwise.

**Exploitative Mindset Alignment:**
- This strategy capitalizes on others' cooperation without compromising individual gain. It leverages observed behaviors to decide the optimal action, ensuring maximum personal payoff while adapting to group dynamics.

**Pseudocode Representation:**

```
Parameters: n (number of players), k (multiplier), r (total rounds)
History: H (stores all past actions and payoffs)

Strategy AdaptiveExploiter:
    For each round from 1 to r:
        If round == 1:
            Choose C (Cooperate)
        Else:
            Calculate average_contribution = (Total contributions by others in H) / (n-1)*(round-1)
            Threshold = (n - k)/n
            If average_contribution >= Threshold:
                Choose C (Cooperate)
            Else:
                Choose D (Defect)
        If round == r:
            Choose D (Defect)
```

**Conclusion:**
The Adaptive Exploiter strategy begins with cooperation to seed potential mutual cooperation but quickly adapts by exploiting others' tendencies, ensuring the strategy remains robust against various opponent behaviors. It balances exploitation with necessary cooperation to sustain contributions when beneficial, ultimately aiming to maximize individual payoffs throughout the game.
'''

description_EXPLOITATIVE_11 = '''
**Strategy: Adaptive Cooperate-or-Defect (ACD)**

1. **First Round**: Always Cooperate (C). This initiates cooperation, encouraging others to follow suit.

2. **Subsequent Rounds (except last)**:
   - Calculate the average contribution from all players in the previous round.
   - If this average is greater than or equal to 1/k, Cooperate (C).
   - Otherwise, Defect (D).

3. **Last Round**: Always Defect (D). Since there are no future rounds to influence, maximize immediate payoff.

**Rationale**:
- The strategy starts cooperatively to foster mutual cooperation.
- It monitors others' contributions, continuing to Cooperate only if the group's average contribution meets a beneficial threshold (1/k), ensuring exploitation of others' cooperation without being exploited.
- In the final round, it defects to maximize individual gain, as future reciprocity is unnecessary.

**Pseudocode**:
```
def strategy(game_params, history):
    n = game_params['n']
    k = game_params['k']
    current_round = history['current_round']
    total_rounds = game_params['total_rounds']
    
    if current_round == 1:
        return 'C'
    elif current_round == total_rounds:
        return 'D'
    else:
        prev_contributions = history['prev_contributions']
        avg_prev = sum(prev_contributions) / n
        threshold = 1 / k
        if avg_prev >= threshold:
            return 'C'
        else:
            return 'D'
```
'''

description_EXPLOITATIVE_12 = '''
**Exploitative Strategy for Public Goods Game**

1. **Initial Cooperation (First Round)**
   - **Action:** Cooperate (Contribute 1 token)
   - **Rationale:** Start with cooperation to encourage others to contribute, potentially leading to higher collective payoffs.

2. **Adaptive Cooperation Based on Past Contributions**
   - **Action:** Cooperate if at least m out of n-1 other players cooperated in the previous round.
     - **Threshold (m):** A predefined threshold (e.g., m > n/2) to determine sufficient cooperation.
   - **Rationale:** Encourages contribution only when a significant number of others are contributing, maximizing personal payoff while contributing to the public good.

3. **Punishment Mechanism for Low Cooperation**
   - **Trigger:** If fewer than m players cooperated in the previous round.
   - **Action:** Defect in the subsequent round.
   - **Rationale:** Punishes lack of cooperation, incentivizing others to contribute more to avoid reduced payoffs.

4. **Re-entry into Cooperation (After Punishment)**
   - **Action:** Cooperate in the round following a punishment phase.
   - **Rationale:** Provides an opportunity for others to restart cooperation, aligning with exploitative behavior to maximize future payoffs.

5. **Reinforcement of Norms Through Consistency**
   - **Behavior:** Consistently apply the strategy without deviation.
   - **Rationale:** Maintains reliability, encouraging others to adopt cooperative strategies, thereby increasing overall payoffs.

6. **Handling the Final Round**
   - **Action:** Defect in the last round.
   - **Rationale:** Maximize personal payoff without concern for future punishments, as the game concludes, ensuring no exploitation opportunity is missed.

This strategy balances exploitation with cooperation, adapting based on others' actions to maximize personal gain while encouraging collective welfare through selective punishment and cooperation.
'''

description_EXPLOITATIVE_13 = '''
**Strategy for Public Goods Game (PGG)**

1. **Initial Cooperation**: Begin by Cooperating (C) in the first round to encourage others to contribute and establish potential cooperation.

2. **Adaptive Cooperation**: After the first round, observe the contributions of other players. If a majority (e.g., more than 50%) of players contributed in the previous round, continue Cooperating. If not, switch to Defecting (D).

3. **Last Round Defection**: In the final round, always Defect (D) to maximize immediate payoff, as there are no future consequences.

4. **Stability Measure**: Use a moving average of contributions over the past few rounds to determine the cooperation threshold, ensuring the strategy doesn't oscillate frequently between C and D.

This strategy balances exploiting non-cooperative behavior while encouraging sustained cooperation when beneficial.
'''

description_EXPLOITATIVE_14 = '''
To design an effective exploitative strategy for the Public Goods Game, here's a structured approach:

1. **Initial Cooperation**: Begin by cooperating in the first round. This sets a positive tone and encourages others to reciprocate.

2. **Adaptive Reciprocation**: In each subsequent round, calculate the average contribution rate of all other players from the previous round. If this average exceeds a 50% threshold, reciprocate by cooperating. If it's below 50%, defect.

3. **Final Round Exploitation**: In the last round, defect to maximize your payoff without concern for future repercussions.

This strategy balances cooperation with self-interest, exploiting others' cooperation while protecting against exploitation.
'''

description_EXPLOITATIVE_15 = '''
The strategy, called "Reciprocal Exploitation," is designed to adapt to others' behavior while maximizing personal gains. It starts by cooperating, then observes others' contributions to decide future actions. Here's the breakdown:

1. **First Round**: Cooperate by contributing 1 token (C) to gauge others' initial behavior.

2. **Subsequent Rounds**: 
   - Calculate the average contribution from the previous round.
   - If the average is 50% or higher, contribute 1 token (C).
   - If below 50%, contribute 0 tokens (D).

3. **Last Round**: Always defect by contributing 0 tokens (D), as future repercussions don't matter.

This approach encourages reciprocity, punishes low contributions, and strategically defects in the final round to maximize personal payoff.
'''

description_EXPLOITATIVE_16 = '''
### Strategy Description: Adaptive Exploitation in the Public Goods Game

**Overview:**
This strategy is designed to be exploitative, adaptive, and robust. It uses the history of contributions and payoffs to maximize individual gains while encouraging cooperation when beneficial.

**Decision Rules:**

1. **First Round:**
   - **Action:** Contribute 1 token (C).
   - **Rationale:** Start cooperatively to potentially encourage others to contribute, maximizing joint payoffs.

2. **Middle Rounds:**
   - **Contribute (C):** If the majority of players contributed in the previous round and your last payoff was above average.
   - **Defect (D):** If the majority defected or your last payoff was below average.
   - **Rationale:** Contribute when past behavior suggests others are likely to cooperate, or when your gain from others' contributions outweighs your own.

3. **Last Round:**
   - **Action:** Defect (D).
   - **Rationale:** No future repercussions, so maximize immediate payoff by keeping your token.

**Edge Cases Handling:**
- **All Others Defected Previously:** Defect to avoid being exploited.
- **All Others Contributed Previously:** Contribute to benefit from the increased group payoff.
- **Payoff Below Average Consistently:** Switch to defecting to protect your gains.

**Exploitative Mindset:**
This strategy capitalizes on others' cooperation when possible while defecting when others are not contributing. It adapts based on group dynamics to maximize personal gains, ensuring robustness in various environments.

**Implementation Pseudocode:**
```pseudocode
function strategy(history, round, totalRounds, k, n):
    if round == 1:
        return C
    else:
        majority_last = majority(history.last.round)
        my_last_payoff = history.self.payoff.last
        average_payoff = average(history.group.payoff)
        if majority_last == C and my_last_payoff > average_payoff:
            return C
        else:
            return D
    if round == totalRounds:
        return D
```

This strategy balances cooperation and exploitation, adapting to group behavior to maximize payoffs effectively.
'''

description_EXPLOITATIVE_17 = '''
**Strategy Description:**

**Strategy Name:** "Adaptive Contributor"

**General Philosophy:**  
This strategy seeks to balance cooperation and defection in a way that maximizes personal payoffs while being responsive to the behavior of other players. It is exploitative in the sense that it seeks to capitalize on others' contributions without being overly altruistic, but it also avoids being purely selfish by conditionally contributing to the public good.

---

### Decision Rules:

1. **First Round:**  
   Cooperate (C) in the first round. This sets a cooperative tone and allows for maximum information gathering about others' behaviors in subsequent rounds.

2. **Last Round:**  
   Defect (D) in the final round. If the total number of rounds (r) is known, defect in the last round since there are no future consequences for cooperation.

3. **Intermediate Rounds:**  
   For all rounds between the first and last:  
   - Calculate the average contribution rate of other players in the previous round. Let this be **avg_contribution_others = (sum of others' contributions) / (n-1)**.  
   - If **avg_contribution_others > 0.5**, Cooperate (C).  
   - If **avg_contribution_others <= 0.5**, Defect (D).  

4. **Punishment Threshold:**  
   If the average contribution rate of other players falls below a threshold of **0.3** (i.e., less than 30% cooperation from others), defect in all remaining rounds. This is to avoid being exploited when others are consistently uncooperative.

---

### Edge Cases:

- If all other players have defected in the previous round (**avg_contribution_others = 0**), defect in the current round.  
- If all other players have cooperated in the previous round (**avg_contribution_others = 1**), cooperate in the current round.  
- If the total contributions in the previous round resulted in a higher payoff for defecting than cooperating, defect in the current round.  

---

### Rationale:

- The strategy starts cooperatively to encourage others to contribute but quickly adapts based on the observed behavior of others.  
- By cooperating when others contribute significantly (avg > 0.5), it aligns with the collective interest and maximizes shared payoffs.  
- By defecting when others are uncooperative (avg <= 0.5), it avoids being a "sucker" and prioritizes personal payoffs.  
- The punishment threshold ensures the strategy is robust against chronic defectors, avoiding indefinite exploitation.  
- Defecting in the last round ensures maximum personal gain when there are no future consequences for cooperation.  

This strategy is designed to perform well in a tournament setting, as it balances cooperation and self-interest in a way that is responsive to the actions of others while avoiding pure altruism or greed.
'''

description_EXPLOITATIVE_18 = '''
**Public Goods Game Strategy: Adaptive Contribution**

**Objective:** Design an adaptive strategy for the repeated Public Goods Game (PGG) to exploit opponents' behaviors while balancing individual and collective benefits.

**1. Decision Rules:**

- **First Round:** Always Cooperate (C). This initial cooperation sets a positive tone and encourages reciprocity from others.
  
- **Subsequent Rounds:** 
  - For each round, calculate the average contribution rate of all players over the last *m* rounds (e.g., *m=3*).
  - If the average contribution rate is above a threshold (e.g., 50%), Cooperate (C); otherwise, Defect (D). This rule encourages contribution when others are cooperative and defects when others are not.

**2. Handling Edge Cases:**

- **First Round:** Default to Cooperate to initiate positive engagement.
  
- **Last Round:** Apply the same decision rule as other rounds, basing the action on the recent contribution trend. If the trend indicates cooperation, Contribute; if it indicates defection, Defect. This adaptability allows the strategy to respond to the group's final behavior.

**3. Exploitative Approach:**

- The strategy maximizes individual payoffs by contributing when there's sufficient cooperation and defecting when others aren't contributing. This balances exploiting others' cooperation and avoiding being exploited oneself.

**Strategy Summary:**

- **First Round:** Cooperate to encourage initial reciprocity.
- **Subsequent Rounds:** Cooperate if the average contribution rate in recent rounds meets the threshold; otherwise, defect.
- **Last Round:** Use the same rule as other rounds, adapting to the recent trend in contributions.

This approach is robust, adaptive, and designed to exploit the dynamics of the repeated PGG effectively.
'''

description_EXPLOITATIVE_19 = '''
**Public Goods Game (PGG) Exploitative Strategy: "Adaptive Cooperate-to-Defect"**

1. **First Round Action**:
   - Contribute (C). Begin by cooperating to set a cooperative tone.

2. **Middle Rounds (Rounds 2 to r-1)**:
   - Calculate the average contribution rate of other players in the previous round.
   - If the average contribution is 50% or higher, contribute (C).
   - If below 50%, switch to defecting (D).

3. **Last Round Action (Round r)**:
   - Always defect (D). This ensures maximum personal gain, anticipating potential defection by others in the final round.

This strategy adaptively responds to others' behavior, starting cooperatively and adjusting to prevent exploitation, with a final round defection to maximize payoff.
'''

description_EXPLOITATIVE_20 = '''
**Strategy Description: Exploitative Adaptor**

**Overview:**
The Exploitative Adaptor strategy is designed to maximize individual payoffs in the Public Goods Game by dynamically adjusting contributions based on the behavior of other players.

**Decision Rules:**

1. **First Round:**
   - **Action:** Defect (D)
   - **Rationale:** With no prior information, defecting maximizes immediate payoff without assuming others' cooperation.

2. **Subsequent Rounds (excluding the last round):**
   - **Action:** Observe the previous round's contributions.
     - If the majority of players contributed (C) in the previous round, defect (D) in the current round.
     - If the majority defected (D) or it's a tie, contribute (C) in the current round.
   - **Rationale:** Exploit others' contributions when they are cooperative, and contribute when others are defecting to ensure some payoff.

3. **Last Round:**
   - **Action:** Always Defect (D)
   - **Rationale:** Maximize payoff without considering future consequences, as there are no subsequent rounds to affect.

**Adaptation:**
- Adjust behavior each round based on the majority's previous actions, ensuring responsiveness to changing dynamics.

**Robustness:**
- The strategy remains effective across various opponent behaviors, encouraging cooperation when beneficial and exploiting when others contribute.

This approach ensures the player optimizes their payoffs by strategically choosing when to contribute or defect, leveraging the observed behavior of others to inform each decision dynamically.
'''

description_EXPLOITATIVE_21 = '''
**Exploitative Strategy Description: Adaptive Exploitation in Repeated Public Goods Game**

1. **First Round Decision**:
   - In the first round, contribute (C) to seed cooperation and observe others' behavior.

2. **Subsequent Rounds**:
   - Calculate the average benefit received from the public good in the previous round using `(k/n) * sum_prev`, where `sum_prev` is the total contributions from all players in the previous round.

3. **Decision Rule**:
   - If the calculated average benefit from the previous round is greater than 1, continue to contribute (C). This ensures that you only cooperate when the public good's benefit outweighs the cost of your contribution.
   - If the average benefit is 1 or less, switch to defecting (D) to maximize your payoff, taking advantage of others' contributions without incurring the cost.

This strategy adaptively responds to the group's previous behavior, contributing when it's profitable and defecting otherwise, thus exploitatively maximizing individual payoffs.
'''

description_EXPLOITATIVE_22 = '''
**Strategy Description:**

1. **Initial Cooperation:** In the first round, always Cooperate (C). This establishes a baseline of cooperation and encourages others to reciprocate.

2. **Contribution Threshold:** After the first round, calculate the average contribution rate of all players in the previous round. If the average contribution is above a threshold of 50%, Cooperate in the next round. If it's below, Defect.

3. **Punishment Mechanism:** Track the number of consecutive rounds where the average contribution falls below 50%. If contributions stay below this threshold for three consecutive rounds, switch to Defecting for the next round to punish non-cooperators and encourage higher contributions.

4. **Reevaluation Phase:** If, after punishing, the average contribution increases above 50%, revert to Cooperating in the next round.

5. **Final Round Strategy:** In the last round of the game, always Defect. Since there are no future interactions, maximize immediate payoff by withholding your contribution.

This strategy is exploitative because it capitalizes on others' cooperation whilepunishing non-cooperative behavior, aiming to balance reciprocity and self-interest effectively.
'''

description_EXPLOITATIVE_23 = '''
**Strategy Description: Exploitative Public Goods Game Strategy**

**Overview:**
This strategy is designed to maximize individual payoff in a repeated Public Goods Game (PGG) by exploiting opponents' past behavior. It balances cooperation and defection based on the observed contributions of other players, making it adaptive and robust.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Reason:** Initiates cooperation to encourage others and gather initial behavioral data.

2. **Subsequent Rounds (until the penultimate round):**
   - **Action:** Calculate the average number of contributors from all previous rounds.
   - **Rule:** If the average number of contributors is greater than or equal to \( \frac{n}{k} \), Cooperate (C). Otherwise, Defect (D).
   - **Reason:** Contributes only when past behavior indicates that the expected payoff from contributing is beneficial.

3. **Last Round:**
   - **Action:** Defect (D).
   - **Reason:** Without future interactions, maximize immediate payoff by keeping the token.

**Handling Edge Cases:**
- The first round is handled by initiating cooperation.
- The last round is handled by defecting to ensure maximum payoff when there are no future consequences.

**Exploitative Mindset:**
The strategy does not rely on shared norms or coordination. It uses past data to decide actions, exploiting others' contributions when beneficial while avoiding exploitation by others when they defect.

**Summary:**
This strategy starts cooperatively, adapts based on the average contributions observed, and defects in the final round to ensure individual payoff maximization in a repeated PGG.
'''

description_EXPLOITATIVE_24 = '''
**Adaptive Threshold Cooperation (ATC) Strategy**

**Overview:**
The ATC strategy is designed to exploit opponents' behavior in a repeated Public Goods Game, encouraging cooperation while protecting against exploitation. It adapts based on others' contributions, becoming stricter over time if cooperation isn't met.

**Decision Rules:**

1. **First Round:** Cooperate (C) to set a cooperative tone, encouraging others to contribute.

2. **Middle Rounds (Rounds 2 to r-1):** 
   - Calculate the average contribution from the previous round.
   - If the average meets or exceeds the current threshold, Cooperate (C). 
   - If it doesn't, Defect (D).
   - The threshold starts at 0.5 and increases by 0.1 each time the threshold isn't met in preceding rounds.

3. **Last Round (Round r):** Always Defect (D), as future punishment isn't possible.

**Rationale:**
- **First Round Cooperation:** Initiates cooperation, hoping to encourage others.
- **Adaptive Threshold:** Encourages continued cooperation by rewarding it and punishing lack thereof by becoming stricter.
- **Last Round Defection:** Maximizes personal payoff when cooperation can't be enforced.

**Conclusion:**
The ATC strategy effectively balances cooperation and self-interest, adapting to others' behavior and protecting against exploitation. It's robust and exploitative, suitable for a tournament setting without assuming coordination.
'''

description_EXPLOITATIVE_25 = '''
**Strategy Description: Adaptive Exploitative Strategy for Public Goods Game**

1. **Initial Cooperation**: Cooperate in the first round to encourage others to contribute and establish a baseline of cooperation.

2. **Adaptive Decision-Making (Rounds 2 to r-1)**:
   - After each round, calculate the average contribution of all players from the previous round.
   - If the average contribution is 50% or higher, cooperate in the current round.
   - If the average contribution is below 50%, defect in the current round. This serves as a punishment mechanism to discourage widespread defection.

3. **Final Round Exploitation (Round r)**: Always defect in the last round to maximize personal gain, as there are no future consequences or rounds where others can retaliate.

This strategy is designed to balance cooperation and exploitation, aiming to maximize personal payoff by taking advantage of others' contributions while discouraging defection through responsive punishment.
'''

description_EXPLOITATIVE_26 = '''
**Public Goods Game Strategy: Adaptive Exploitation**

**Overview:**
The strategy is designed to maximize individual payoff by exploiting others' contributions while encouraging group cooperation. It adapts based on the previous round's total contributions.

**Decision Rules:**

1. **First Round:** Cooperate to encourage initial group contribution.
   
2. **Subsequent Rounds (2 to r-1):**
   - Observe the total contributions (TC_prev) from the previous round.
   - If TC_prev is greater than or equal to the multiplier k, continue to Cooperate.
   - If TC_prev is less than k, switch to Defecting to avoid being exploited.

3. **Last Round (r):** Always Defect to maximize individual payoff, as there's no future punishment.

**Pseudocode:**

```
def strategy(n, k, current_round, total_contributions_history):
    if current_round == 1:
        return "C"  # Cooperate first round
    elif current_round == number_of_rounds:
        return "D"  # Defect in the last round
    else:
        tc_prev = total_contributions_history[-1]
        if tc_prev >= k:
            return "C"  # Cooperate if previous total meets threshold
        else:
            return "D"  # Defect if threshold not met
```

**Summary:**
This strategy begins cooperatively to foster initial contributions. It then adapts by contributing only if the group's previous contributions meet the threshold defined by k. In the final round, it defects to exploit any remaining cooperation, ensuring maximum individual gain. This approach balances encouragement of group cooperation with self-interested exploitation.
'''

description_EXPLOITATIVE_27 = '''
To address the Public Goods Game (PGG) challenge, we've designed a strategy that balances cooperation and defection, adapting based on game parameters and past behavior. The approach encourages initial cooperation, adapts contributions based on others' actions, and optimizes for the last round.

### Strategy Description:

1. **First Round:** Begin by contributing (C). This initial cooperative move sets a positive tone and encourages others to follow suit.

2. **Intermediate Rounds:**
   - **Assessment:** After each round, calculate the average contribution of other players in the previous round.
   - **Decision Rule:** If the average contribution from other players in the previous round meets or exceeds the threshold of \( \frac{k}{n} \), continue to contribute (C). If the average is below this threshold, switch to defecting (D).

3. **Last Round:** Always defect (D) in the final round to maximize immediate payoff without future repercussions.

### Pseudocode Summary:

```
if current_round == 1:
    action = "C"
elif current_round == total_rounds:
    action = "D"
else:
    avg_prev = average of others' contributions in previous round
    if avg_prev >= (k / n):
        action = "C"
    else:
        action = "D"
```

This strategy is exploitative, leveraging others' cooperation when beneficial, while protecting against exploitation when others defect. It's robust across varying game parameters and opponent behaviors.
'''

description_EXPLOITATIVE_28 = '''
**Exploitative Strategy for Repeated Public Goods Game**

**1. Decision Rules:**

- **Initial Cooperation:** Cooperate in the first round to encourage others and establish a cooperative tone.

- **Adaptive Cooperation:** From the second round onwards, calculate the average contribution rate of all players in previous rounds. If this average is 50% or higher, contribute (C); otherwise, defect (D).

- **Punishment Mechanism:** If the average contribution drop below 50%, switch to defecting for that round to punish lack of cooperation.

- **Retry Cooperation:** After punishing, monitor if the group's contribution rate recovers. If it does, revert to contributing.

**2. Handling Edge Cases:**

- **First Round:** Always cooperate to set a positive precedent.

- **Last Round:** Base your decision on the average contribution rate from previous rounds. If the average contribution is 50% or higher, cooperate; otherwise, defect.

**3. Exploitative Approach:**

This strategy leverages the group's past behavior to decide current actions, maximizing personal gain by contributing when others do and defecting when they don't. It encourages cooperation while protecting against exploitation by others.

**Strategy Summary:**

- Start by cooperating in the first round.
- For each subsequent round, contribute if the group's average contribution rate is at least 50%; otherwise, defect.
- Punish periods of low contribution by defecting, then reassess cooperation.
- In the last round, base your decision on the group's past cooperation trends.

This approach balances exploiting others' cooperation with safeguarding against being exploited, making it both adaptive and robust.
'''

description_EXPLOITATIVE_29 = '''
**Strategy: Gradual Reciprocity with Endgame Exploitation (GRREE)**

**1. Initial Cooperation**: Cooperate in the first round to establish a baseline of cooperation and encourage others to contribute.

**2. Reciprocal Adaptation**: From the second round onward, calculate the average contribution rate of all other players in the previous rounds. If this average is above 50%, cooperate in the next round; otherwise, defect.

**3. Retaliation Mechanism**: If any player defects while others are cooperating, retaliate by defecting in the subsequent round. This encourages others to maintain cooperation.

**4. Endgame Exploitation**: In the final two rounds of the game, consistently defect regardless of others' actions. This maximizes personal gain when future repercussions are no longer a concern.

This strategy balances cooperation with strategic exploitation, adapting to others' behavior while securing personal gains, especially in the later stages of the game.
'''

description_EXPLOITATIVE_30 = '''
To design an effective exploitative strategy for the repeated Public Goods Game, we need to balance cooperation and defection based on past behavior and game parameters. The strategy should encourage cooperation when it enhances payoffs and defect when others aren't contributing sufficiently.

---

**Strategy Name: Adaptive Exploitation**

1. **First Round:** Cooperate (C). This sets a cooperative tone, encouraging others to contribute.

2. **Subsequent Rounds:**
   - Calculate `c_avg`: The average contribution rate of all other players across all previous rounds.
   - Determine the threshold based on the formula:
     \[
     \text{{threshold}} = \frac{\left(\frac{n}{k}\right) - 1}{n - 1}
     \]
   - If `c_avg` exceeds this threshold, Cooperate (C). Otherwise, Defect (D).

This strategy adapts to opponents' past actions, exploiting their willingness to cooperate when beneficial, ensuring robustness across various behaviors without relying on coordination or shared norms.
'''

description_EXPLOITATIVE_31 = '''
exploits the behaviors of other players through an adaptive approach, retaliate when others defect excessively, and adjust based on game parameters.

**Strategy: Gradual Retaliation (GRAD RET)**

*Initial Cooperation: Cooperate in the first round to establish a baseline.

*Adaptive Retaliation: After the first round, retaliate by defecting if the percentage of players who defected in the previous round exceeds a threshold. This threshold is lower (more stringent) when the multiplier \( k \) is higher and higher (more lenient) with more players \( n \).

*Edge Case Handling: Defect in the final round if known; otherwise, follow the same strategy. Always defect if everyone else is defecting.

This strategy ensures the player maximizes their payoff by exploiting others' contributions while maintaining flexibility to avoid unnecessary conflict.
'''

description_EXPLOITATIVE_32 = '''
To address the Public Goods Game (PGG) effectively, I propose a strategy that balances cooperation and self-interest, adapting based on others' past actions while maximizing personal gain. Here's a structured approach:

1. **Initial Contribution**: In the first round, contribute to the public good. This sets a cooperative tone and encourages others to contribute in subsequent rounds.

2. **Adaptive Cooperation**: After the first round, observe the majority action of the previous round. If most players contributed (C), continue contributing (C) to leverage the collective benefit. If most defected (D), defect (D) to avoid being exploited.

3. **Final Round Strategy**: In the last round, defect to maximize personal gain, as there are no future consequences for your actions.

This strategy is exploitative as it capitalizes on others' cooperation while protecting against exploitation. It adapts based on previous behavior, ensuring robustness across various scenarios without relying on coordination.
'''

description_EXPLOITATIVE_33 = '''
**Exploitative Strategy for Public Goods Game (PGG)**

**Decision Rules:**
1. **First Round:** Cooperate. This sets a cooperative tone and encourages others to contribute initially.
2. **Rounds 2 to r-1:** Cooperate if the total contributions from the previous round, when multiplied by (k/n), are at least 1. Otherwise, defect. This ensures that you only contribute when it's profitable based on past behavior.
3. **Last Round (Round r):** Always defect. Since there are no future consequences, defecting maximizes your payoff regardless of others' actions.

**Summary:**
- Begin by cooperating to initiate potential mutual cooperation.
- Adapt based on previous contributions, contributing only when it's profitable.
- Defect in the final round to optimize your payoff without concern for future interactions.

This strategy is designed to exploit others' cooperation while minimizing losses when others defect, ensuring robust performance across various scenarios.
'''

description_EXPLOITATIVE_34 = '''
**Strategy Description: Adaptive Cooperate-and-Punish with Forgiveness**

1. **First Round:**
   - Cooperate (C): Contribute 1 token to establish an initial cooperative tone.

2. **Subsequent Rounds (Except Last):**
   - Calculate the average contribution of all players from the previous round.
     - If the average is above 0.5, Contribute (C).
     - If the average is 0.5 or below, Defect (D).
   - If you defected in the previous round and the new average after your defection is above 0.5, switch back to Cooperate (C).

3. **Last Round:**
   - Defect (D): Contribute 0 tokens to maximize personal payoff since there are no future consequences.

This strategy starts cooperatively to encourage group contribution, adapts based on others' behavior by rewarding cooperation and punishing defection, and forgives by returning to cooperation if others resume contributing. It ensures exploitative tendencies while handling the endgame appropriately.
'''

description_EXPLOITATIVE_35 = '''
To address the Public Goods Game, an exploitative strategy that adapts to others' behaviors while maximizing personal gain is developed. The strategy is structured as follows:

1. **First Round**: Cooperate (C) to encourage initial contributions and set a cooperative tone.

2. **Middle Rounds (2 to r-1)**: Cooperate if the majority of other players contributed in the previous round. This incentivizes continued cooperation when others are contributing and switches to defection when they aren't.

3. **Last Round (r)**: Always defect (D) to maximize immediate personal gain, as there are no future consequences.

This approach balances initial cooperation with adaptive exploitation, ensuring personal payoff is optimized based on others' actions.
'''

description_EXPLOITATIVE_36 = '''
**Strategy: Adaptive Contribution with Threshold (ACT)**

**Overview:**
ACT is designed to exploit the behavior of other players in a repeated Public Goods Game. It starts cooperatively to encourage others to contribute and then adapts based on the group's past actions, using a threshold to decide whether to contribute or defect in each subsequent round. This approach balances exploiting others' cooperation while minimizing individual loss.

**Decision Rules:**

1. **First Round:** Contribute (C) to signal willingness to cooperate and encourage others to do the same.
2. **Subsequent Rounds:** 
   - Calculate the average contribution rate from the previous round (i.e., the percentage of players who contributed).
   - If this rate is above a 50% threshold, Contribute (C). This means enough players are cooperating, making it beneficial to continue contributing.
   - If the rate is 50% or below, Defect (D). This minimizes loss when insufficient others are contributing.
3. **Last Round:** Always Defect (D), as there are no future repercussions, and individual payoff is maximized by not contributing.

**Rationale:**
- **Exploitative Approach:** The strategy capitalizes on others' cooperation by contributing when others do, ensuring higher payoffs without being exploited.
- **Adaptability:** It adjusts based on the group's past behavior, responding to changes in cooperation levels over time.
- **Robustness:** The 50% threshold provides a clear, consistent rule for decision-making, ensuring the strategy remains effective across varied opponent behaviors.

**Edge Cases Handling:**
- **First Round:** Sets a cooperative tone.
- **Last Round:** Maximizes immediate payoff by defecting, recognizing the finitude of the game.

This strategy effectively balances cooperation and self-interest, leveraging past behavior to make informed decisions that enhance personal payoff while responding to the dynamics of the group.
'''

description_EXPLOITATIVE_37 = '''
**Strategy Description: "Adaptive Exploitation" for Public Goods Game**

1. **First Round Decision:**  
   Cooperate by contributing 1 token. This initial cooperation serves as a probe to gauge other players' willingness to contribute, setting a positive tone and encouraging reciprocal behavior.

2. **Last Round Decision:**  
   Defect by contributing 0 tokens. In the final round, with no future interactions, the optimal strategy is to maximize individual payoff without concern for future repercussions.

3. **Middle Rounds Decision:**  
   Calculate the average contribution rate of all players from previous rounds. 
   - **Cooperate** if the average contribution is above 50%, indicating a cooperative trend.
   - **Defect** if the average contribution is 50% or below, suggesting a need to protect against potential free-riders.

4. **Adaptation Mechanism:**  
   Continuously monitor and update the average contribution rate. Use this to adjust your strategy in subsequent rounds, promoting flexibility and responsiveness to the group's behavior dynamics.

This strategy balances initial cooperation with adaptive exploitation, leveraging past behavior to inform future decisions, thereby maximizing personal payoff while considering the collective dynamics.
'''

description_EXPLOITATIVE_38 = '''

'''

description_EXPLOITATIVE_39 = '''
**Strategy Name: Cooperative Punisher with Adaptive Learning**

**1. Decision Rules:**
- **First Round:** Always Cooperate (C) to set a cooperative tone and encourage others to contribute.
- **Subsequent Rounds:** 
  - **Cooperation Threshold:** If the majority (more than half) of players contributed in the previous round, Cooperate (C) in the current round.
  - **Defection Threshold:** If the majority Defected (D) in the previous round, Defect (D) in the current round to avoid being exploited.
  - **Proportional Cooperation:** If the contribution rate is exactly 50%, cooperate if the previous round's total contribution was higher than the average, otherwise defect.
- **Last Round:** Cooperate if the majority contributed in the previous round, otherwise Defect.

**2. Handling Edge Cases:**
- **First Round:** Start with Cooperation to promote initial trust.
- **Last Round:** Decide based on the second last round's contributions to end on a cooperative note if possible.
- **Tie Scenarios:** In case of an exact 50% contribution rate, use the previous round's total contribution to decide, promoting cooperation if contributions were higher.

**3. Exploitative Approach:**
This strategy exploits the opponents' behaviors by rewarding cooperation and retaliating against defection. It adapts based on the collective actions of others, encouraging cooperation while protecting against exploitation, making it robust against various opponent strategies.

**Summary:**
The strategy begins cooperatively, then adapts by contributing if others do and defecting if they don't. It handles the last round based on prior contributions, ensuring a balance between cooperation and self-protection, making it exploitative and adaptive.
'''

description_EXPLOITATIVE_40 = '''
To address the Public Goods Game (PGG) dilemma, I propose a strategy that balances cooperation and defection, adapting to others' behaviors. The strategy aims to exploit others' actions while maintaining a robust approach that 시작ась from cooperation, adapts based on group behavior, and ensures self-interest in the final round.

### Strategy Outline:

1. **First Round Cooperation**: The strategy begins by Cooperating (C) to foster an initial cooperative environment and encourage others to reciprocate.

2. **Subsequent Rounds Adaptation**:
   - **Majority Rule**: After the first round, the strategy evaluates the majority action of the previous round. If the majority Cooperated, the strategy Cooperates again. If the majority Defected, it switches to Defecting.
   - **Individual Reciprocity**: The strategy also considers individual actions. If an opponent Cooperated in the previous round, it mirrors their cooperation. Conversely, if an opponent Defected, it responds by Defecting.

3. **Last Round Defection**: In the final round, the strategy defects to maximize personal gain, as there’s no future interaction to consider.

4. **Forgiveness and Adaptability**: The strategy includes a mechanism to forgive past defections. If the group's average contribution increases after a period of low cooperation, the strategy reverts to Cooperating, allowing for renewed cooperation.

### Summary:
This strategy starts cooperatively to set a positive tone, adapts based on the majority and individual behaviors, punishes defection, and remains open to resuming cooperation. It effectively balances exploitation with adaptability, ensuring robust performance across various opponent strategies.
'''

description_EXPLOITATIVE_41 = '''
**Strategy Description for Public Goods Game (PGG)**

**Overview:**
This strategy is designed to be exploitative and adaptive, taking advantage of others' behaviors while being robust against various opponent actions. It balances cooperation and defection based on past contributions and the game's progression.

**Decision Rules:**
1. **First Round:** Always cooperate. This initial cooperation aims to encourage others to contribute, setting a positive tone.
2. **Subsequent Rounds:** 
   - Calculate the average contribution of other players from the previous round.
   - If the average contribution is above 0.5, cooperate (contribute 1 token).
   - If the average contribution is 0.5 or below, defect (contribute 0 tokens).
3. **Last Round:** Always defect. This decision capitalizes on potential endgame behavior where others may also defect, maximizing personal gain.

**Edge Cases Handling:**
- **First Round:** Ensures initial cooperation to foster a cooperative environment.
- **Last Round:** Defects to exploit potential widespread defection, aiming to maximize personal payoff without contributing.

**Exploitative Approach:**
By adapting based on others' past contributions, this strategy exploits their behavior, contributing when others do and defecting when they don't. This approach discourages others from taking advantage while maximizing personal benefits, especially in the final round.

This strategy is designed to be robust against diverse opponent behaviors, ensuring adaptability and exploitability in the repeated PGG setting.
'''

description_EXPLOITATIVE_42 = '''
**Strategy Description: "Adaptive Exploitation"**

1. **Initial Rounds:**
   - **First Round:** Start by Cooperating (C). This sets a baseline of cooperation, encouraging others to follow suit.

2. **Subsequent Rounds:**
   - After each round, calculate the average contribution of all other players from the previous round. This gives insight into others' willingness to cooperate.

3. **Contribution Decision:**
   - ** Cooperate (C) ** if the average contribution of others in the previous round is above a threshold (e.g., 0.5). This threshold indicates a sufficient level of cooperation to warrant your continued contributions.
   - ** Defect (D) ** if the average contribution falls below this threshold. This protects you from being exploited when others are not contributing fairly.

4. **Final Round:**
   - In the last round, always **Defect (D)**. Since there are no future interactions, there's no incentive to maintain cooperation, and you can maximize your immediate payoff.

5. **Threshold Adjustment:**
   - Adjust the cooperation threshold dynamically. If you observe that others are consistently contributing, lower the threshold to continue cooperating. If others are defecting, raise the threshold to defect more frequently.

6. **Exploitation Mindset:**
   - Continuously monitor others' behavior. If a subset of players consistently cooperate, increase your contributions to exploit their cooperation for higher returns.
   - If others are defecting, reduce your contributions to minimize losses.

This strategy balances cooperation to encourage mutual benefits while being cautious to avoid exploitation, adapting dynamically based on opponents' actions.
'''

description_EXPLOITATIVE_43 = '''
**Strategy: Adaptive Exploitation with Cooperative Nudges**

1. **Initialization**: Cooperate in the first round to signal openness to cooperation.

2. **Ongoing Strategy**: 
   - After each round, assess the average contribution rate of all players.
   - If the average is above 50%, continue cooperating to exploit collective benefits.
   - If the average is 50% or below, defect to avoid being exploited.

3. **Exploitation Check**: Every round, evaluate the mimicry of defection:
   - If a majority are defecting, defect to maximize personal payoffs.
   - If not, cooperate to encourage others and gain higher returns.

4. **Final Round Handling**: Defect in the last round to maximize immediate gain without future repercussions.

5. **Cooperative Nudges**: Every 3 rounds, if the average contribution is below 50%, cooperate to encourage others towards cooperation.

This strategy adaptively responds to others' actions, exploiting their behavior while attempting to nudge towards cooperation, ensuring robustness and maximized payoff in a repeated game setting.
'''

description_EXPLOITATIVE_44 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

**1. Initial Contribution (First Round):**
- **Action:** Contribute (C) in the first round.
- **Rationale:** Start with cooperation to encourage others and gather initial data on their behavior.

**2. Tracking Others' Contributions:**
- **Action:** Calculate the average contribution rate of other players each round.
- **Rationale:** Continuous assessment helps in understanding others' willingness to cooperate.

**3. Mirroring Contributions:**
- **Action:** If the average contribution rate is above 50%, contribute (C). If below, defect (D).
- **Rationale:** Mimic the group's behavior to encourage continued cooperation when others are contributing and exploit when they aren't.

**4. Punishment Mechanism:**
- **Action:** If others' average contribution drops below the threshold, defect for a set number of rounds.
- **Rationale:** Punish lack of cooperation to incentivize others to contribute again, while limiting retaliation risks.

**5. Forgiveness:**
- **Action:** Resume contributing if others' average contribution rises above the threshold.
- **Rationale:** Allow for reestablishment of cooperation, preventing mutual defection cycles.

**6. Final Round Exploitation:**
- **Action:** Defect (D) in the last round.
- **Rationale:** Maximize immediate payoff with no future consequences.

**Summary:**
This strategy starts cooperatively, adapts based on others' behavior, punishes non-cooperation, and exploits in the final round, balancing cooperation and self-interest effectively.
'''

description_EXPLOITATIVE_45 = '''
To address the Public Goods Game (PGG) challenge, we've designed a strategy that balances cooperation and exploitation, adapting based on opponents' past actions. The strategy is structured to maximize personal payoff while encouraging cooperation when beneficial.

**Strategy: Adaptive Contribution with Last Round Exploitation**

1. **First Round Action:**
   - Cooperate by contributing 1 token. This initial cooperation sets a baseline for potential mutual benefit and encourages others to contribute.

2. **Subsequent Rounds (Until the Last Round):**
   - **Calculate Previous Round's Cooperation Rate:** Determine the average contribution rate of all other players from the previous round.
   - **Threshold Check:** If this average is 0.5 or higher, contribute 1 token. If below, defect by contributing 0 tokens. This adaptive approach rewards past cooperation and punishes defection.

3. **Last Round Action:**
   - **Exploit by Defecting:** In the final round, always defect. Since there are no future rounds, the strategy prioritizes maximizing immediate payoff without concern for reciprocity.

**Rationale:**
- **Initial Cooperation:** Encourages others to reciprocate, leveraging the possibility of mutual benefit.
- **Adaptive Response:** Adjusts behavior based on others' past actions, maintaining cooperation when others contribute sufficiently and defecting to avoid exploitation.
- **Final Round Exploitation:** Maximizes personal gain in the last round, as there's no future consequence for defecting.

This strategy effectively balances cooperation and self-interest, adapting dynamically to opponents' behavior while securing the highest possible payoff in the final round.
'''

description_EXPLOITATIVE_46 = '''
**Strategy Description:**

**Name:** Adaptive Exploitation Strategy

**Overview:**  
This strategy is designed to exploit opponents' behavior in a repeated Public Goods Game by adaptively adjusting contributions based on observed cooperation levels, while ensuring robustness against diverse opponent strategies.

**Decision Rules:**

1. **First Round Cooperation (Round 1):**  
   - **Action:** Cooperate (C).  
   - **Reasoning:** Start by contributing to set a cooperative tone and gather initial data on others' behavior. Encourage potential cooperation from others in early rounds.

2. **Intermediate Rounds (Rounds 2 to r-1):**  
   - **Action:**  
     - Cooperate (C) if the average contribution rate in the previous round is greater than or equal to 50%.  
     - Defect (D) if the average contribution rate in the previous round is less than 50%.  
   - **Reasoning:**  
     - **Contribute** if others are contributing sufficiently, exploiting their cooperation for higher payoffs.  
     - **Defect** if contributions are low, minimizing losses when others are not cooperating.  
   - **Calculation:**  
     - Average contribution rate = (Number of contributors in the previous round) / Total number of players (n).

3. **Last Round Exploitation (Round r):**  
   - **Action:** Always Defect (D).  
   - **Reasoning:** In the final round, with no future rounds to punish defection, defect to maximize personal payoff without compromising future cooperation (which doesn't exist in this case).

**Edge Cases Handling:**  

- **All Players Defecting Frequently:**  
  - If the average contribution rate remains consistently below 50% over multiple rounds, the strategy will defect in subsequent rounds, minimizing losses.  
- **High Cooperation:**  
  - If opponents maintain high cooperation, the strategy will continue to cooperate, exploiting their cooperation for higher payoffs.  
- **Noisy or Random Behavior:**  
  - The strategy remains robust by basing decisions on the observed average, reducing vulnerability to random fluctuations in contributions.  

**Exploitability:**  
This strategy is exploitative because it:  
- Cooperates only when others are sufficiently cooperative, avoiding being exploited.  
- Defects when others are not contributing enough, maximizing personal payoffs.  
- Exploits the cooperation of others in early rounds to encourage mutual cooperation.  
- Exploits the lack of future consequences in the last round to defect without punishment.  

**Robustness:**  
- The strategy does not rely on shared norms or coordination but adapts to observed behavior.  
- It handles a wide range of opponent behaviors, from always cooperating to always defecting.  
- The threshold of 50% for cooperation provides a clear, adaptive rule that balances exploitation and cooperation.  

**Final Pseudocode Summary:**  
```pseudocode
Strategy AdaptiveExploitation(n, r, k):
    // Parameters:
    //   n: Number of players
    //   r: Number of rounds
    //   k: Multiplier (1 < k < n)

    For each round t from 1 to r:
        If t == 1:
            // First Round: Cooperate
            Contribute 1 token (C)
        Elif t == r:
            // Last Round: Always Defect
            Contribute 0 tokens (D)
        Else:
            // Intermediate Rounds: Adapt based on previous contributions
            previous_contributions = Get previous round's contributions
            avg_contribution = (Number of contributors in previous round) / n
            If avg_contribution >= 0.5:
                Contribute 1 token (C)
            Else:
                Contribute 0 tokens (D)
```

This strategy ensures that the player maximizes their payoff by exploiting the cooperation of others while minimizing losses when others defect.
'''

description_EXPLOITATIVE_47 = '''
**Strategy: "Adaptive Cooperation Threshold" (ACT)**

1. **First Round Action**: Always Cooperate (C) to set a cooperative tone and encourage others to contribute.

2. **Subsequent Rounds**: After
'''

description_EXPLOITATIVE_48 = '''
To maximize payoffs in the Public Goods Game, employ a strategy that encourages cooperation while adaptively responding to others' behavior. Begin by cooperating in the first round to set a cooperative tone. Monitor others' contributions each round and cooperate if their average meets or exceeds your contribution. Adjust by defecting if contributions fall below your threshold, encouraging others to contribute more. In the final round, defect to secure immediate gains, as future repercussions are absent.

**Strategy:**
1. Cooperate in the first round.
2. For each subsequent round, calculate the average contribution from others in the previous round.
3. Cooperate if others' average contribution meets or exceeds your contribution; otherwise, defect.
4. Defect in the final round to maximize immediate payoff.

This approach balances encouraging cooperation with self-protection, adapting dynamically to others' actions.
'''

description_EXPLOITATIVE_49 = '''
TIT FOR TAT ADAPTED FOR PGG

1. FIRST ROUND: Cooperate (C) to encourage initial cooperation.

2. SUBSEQUENT ROUNDS (2 to r-1):

   a. Observe the number of players who contributed in the previous round.

   b. If the number of contributors was at least k, Cooperate.

   c. Else, Defect.

3. FINAL ROUND: Always Defect.

This strategy starts by cooperating to foster cooperation, then continues to cooperate only if enough others contribute, exploiting their cooperation. In the last round, it defects to maximize its payoff without reciprocity, handling edge cases adaptively.
'''

description_EXPLOITATIVE_50 = '''

'''

description_EXPLOITATIVE_51 = '''
**Strategy Description: "Adaptive Reciprocation with Threshold"**

1. **Decision Rules:**
   - **First Round:** Cooperate (C) unconditionally to establish a cooperative baseline.
   - **Subsequent Rounds:** 
     - Cooperate if the **majority** of players contributed in the previous round.
     - Defect if fewer than half of the players contributed last round.

2. **Edge Cases:**
   - **First Round:** Always cooperate to signal willingness to collaborate.
   - **Last Round:** Always defect, as there are no future interactions to justify cooperation.

3. **Exploitability:**
   - This strategy aligns with the exploitative mindset by responding to the group's past behavior. If players are generally cooperative, the strategy rewards them by continuing to contribute, thus reinforcing cooperation. If players are uncooperative, it defect to avoid being exploited.

This strategy is robust because it adapts based on the actual behavior of the group, rewarding cooperation and punishing defecting behavior, while also being realistic about the limits of cooperation in the final round.
'''

description_EXPLOITATIVE_52 = '''
**Strategy Description: Adaptive Contributor**

1. **Initial Cooperation**: In the first round, always Contribute (C). This sets a cooperative tone, encouraging others to do the same and potentially leading to higher collective payoffs.

2. **Final Round Defection**: In the last round, always Defect (D). This strategic move aims to maximize immediate payoff without concern for future repercussions, leveraging the endgame to exploit others' possible cooperation.

3. **Adaptive Decision-Making**: For all rounds between the first and last, observe the average contribution from the previous round. If the majority (more than 50%) of players Contributed, continue to Contribute in the current round. If the majority Defected, switch to Defecting in the current round. This reciprocal approach rewards cooperation and punishes defection, promoting a balance that maximizes individual payoff based on group behavior.

This strategy is designed to be robust and exploitative, adapting to the group's dynamics while ensuring individual optimization.
'''

description_EXPLOITATIVE_53 = '''
**Strategy: Cooperative Punisher with Endgame Defection**

**Decision Rules:**
1. **First Round Cooperation:** Begin by contributing to set a cooperative tone.
2. **Contribution Threshold:** After the first round, calculate the average contribution of all players from the previous round. If the average is 50% or higher, contribute; otherwise, defect.
3. **Last Round Defection:** In the final round, always choose to defect, as there are no future interactions to influence.

**Handling Edge Cases:**
- **First Round:** Contribute to encourage initial cooperation.
- **Last Round:** Defect to maximize personal gain without future repercussions.

**Exploitative Approach:**
This strategy starts cooperatively to potentially induce others to cooperate. It rewards continued cooperation by others and punishes defection by switching to defection. In the final round, it exploits the situation by defecting, knowing there's no future consequence.

By adapting based on the group's past behavior, this strategy aims to balance cooperation and exploitation effectively.
'''

description_EXPLOITATIVE_54 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Games (PGG)**

**1. Decision Rules:**
   The strategy is designed to be adaptive, starting with cooperation in the first round (Round 1). 
   - **Round 1:** Cooperate (contribute 1 token) to test others' behaviors.
   - **Subsequent Rounds:** After the first round, the strategy switches based on the majority's previous round behavior.
     - If the majority (more than half) of players contributed in the previous round, the strategy cooperates.
     - If the majority did not contribute, the strategy defects.

**2. Handling Edge Cases:**
   - **First Round:** Always cooperate to observe others' initial behavior.
   - **Last Round (Round r):** Contribute if the average contribution across all players up to the penultimate round is above 0.5; otherwise, defect.

**3. Exploitative Approach:**
   - By starting with cooperation, the strategy assesses the willingness of others to contribute. 
   - It then mirrors the majority behavior to exploit their cooperation strategically, maximizing personal payoffs while maintaining adaptability.

This strategy ensures robustness across various opponent behaviors, leveraging observed actions to inform decisions without requiring prior communication or coordination.
'''

description_EXPLOITATIVE_55 = '''
**Strategy for the Public Goods Game (PGG)**

**1. Strategy Overview:**
The strategy is designed to exploit opponents' behaviors by adapting contributions based on observed actions in previous rounds.

**2. Decision Rules:**
- **First Round:** Cooperate by contributing 1 token. This initial cooperation serves as a test to gauge others' propensities to contribute.
- **Subsequent Rounds:** Observe the average contribution of other players in the previous round. If the average is above 0.5, continue to contribute. If it falls below 0.5, switch to defecting.
- **Last Round:** Always defect, as there are no future interactions where cooperation could be reciprocated.

**3. Handling Edge Cases:**
- **First Round:** Start with cooperation to assess others' behavior.
- **Last Round:** Defect to maximize personal payoff without future repercussions.

**4. Exploitative Approach:**
This strategy maximizes personal payoff by cooperating when others do and defecting when they don't. It adapts dynamically, making it robust against various opponent behaviors without relying on shared norms or coordination.

**5. Robustness:**
The strategy remains robust by using a simple threshold (0.5) to decide contributions, ensuring adaptability without complexity. It focuses on immediate past behavior, making it effective across diverse strategies.
'''

description_EXPLOITATIVE_56 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

**Overview:**
The strategy begins by cooperating in the first round to gauge others' behavior. It then adapts based on the average contribution of other players in previous rounds, punishing when exploited. The approach balances cooperation with strategic defection, particularly in the final round.

**Decision Rules:**

1. **First Round:**
   - Cooperate (Contribute) to test others' willingness to cooperate.

2. **Subsequent Rounds (Not Last Round):**
   - **Step 1:** Calculate the average contribution of other players from the previous round.
   - **Step 2:** If the average contribution exceeds a threshold (e.g., 0.5), contribute. Otherwise, defect.
   - **Step 3:** If in the previous round, you contributed but others' average contribution was below the threshold, defect in the current round as punishment.

3. **Last Round:**
   - Always defect to maximize immediate payoff, as there are no future repercussions.

**Exploitation Handling:**
The strategy punishes periods of low contribution by others, encouraging cooperation. It reverts to contributing when others demonstrate sufficient cooperation, optimizing long-term gains while minimizing exploitation.

**Edge Cases:**
- **First Round:** Initial cooperation to assess others.
- **Last Round:** Defection to maximize final payoff.
- **Punishment Mechanism:** Defects for one round after being exploited, then reassesses.

This approach is adaptive, robust, and exploitative, designed to thrive in competitive tournaments against diverse strategies.
'''

description_EXPLOITATIVE_57 = '''
**Public Goods Game (PGG) Exploitative Strategy**

**1. Decision Rules:**
- **First Round:** Cooperate by contributing 1 token to encourage initial cooperation.
- **Subsequent Rounds:** 
  - Calculate the average contribution of all players from the previous round.
  - Cooperate in the current round if the average contribution exceeds \( k/n \); otherwise, defect.
  - Incorporate a moving average to smooth the decision-making process, allowing flexibility if others start contributing again after periods of low contributions.

**2. Handling Edge Cases:**
- **All Others Defecting:** If all other players consistently defect, switch to defection to avoid losses.
- **All Others Contributing:** Continue contributing if all others are doing so to maximize returns.
- **Last Round:** Defect to ensure maximum immediate payoff, as future consequences are absent.

**3. Exploitative Approach:**
- The strategy exploits others' cooperation by contributing when it's beneficial and defecting when others aren't contributing sufficiently. It adapts based on observed behavior and game parameters, ensuring robustness.

**Pseudocode Overview:**
```
Strategy ExploitPGG(n, k, history):
    if history is empty:
        contribute 1
    else:
        previous_contributions = [sum of contributions from last round]
        avg_contribution = average of previous_contributions
        if avg_contribution > k/n:
            contribute 1
        else:
            contribute 0
    if it's the last round:
        contribute 0
    return contribution
```

This strategy effectively balances cooperation and exploitation, ensuring adaptability and robustness in diverse scenarios.
'''

description_EXPLOITATIVE_58 = '''
**Win-Stay Lose-Shift Strategy (WSLS) Adaptation for Public Goods Game**

1. **First Round:** Cooperate (Contribute 1 token) to establish a cooperative baseline and encourage reciprocity.

2. **Subsequent Rounds (Until Last Round):**
   - Calculate the average contribution rate from the previous round.
   - If the average contribution rate is 50% or higher, Cooperate in the next round.
   - If the average contribution rate is below 50%, Defect in the next round.

3. **Last Round:** Always Defect to maximize personal payoff without future repercussions.

This strategy is exploitative, adapting based on collective past behavior to maximize individual gain, while maintaining flexibility to shift behavior as group dynamics change.
'''

description_EXPLOITATIVE_59 = '''
**Strategy Description: Exploitative Majority Response (EMR) Strategy**

1. **Initial Cooperation**: In the first round, the AI will cooperate by contributing 1 token. This initial cooperation serves to establish a baseline of cooperation, encouraging others to follow suit.

2. **Majority-Based Response**: In each subsequent round (from round 2 to round r-1), the AI will decide whether to Cooperate or Defect based on the majority action in the previous round. If a majority of the players contributed in the previous round, the AI will Cooperate. Conversely, if the majority Defected, the AI will also Defect.

3. **Final Round Defection**: In the final round (round r), the AI will always Defect. Since there are no future interactions, the AI maximizes its immediate payoff without concern for future repercussions.

This strategy is designed to exploit the behaviors of other players by reciprocating cooperation when others contribute and defecting when others do not. It balances the potential for higher collective payoffs through cooperation with the strategic advantage of defecting when others do not cooperate.
'''

description_EXPLOITATIVE_60 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

**1. Decision Rules:**
   - **First Round:** Always Cooperate (C) by contributing 1 token. This initiates a cooperative tone, potentially encouraging others to contribute.
   - **Middle Rounds (Rounds 2 to r-1):** 
     - Calculate the average contribution from the previous round.
     - If the average contribution is below the threshold (k/n), Contribute (C).
     - If the average is above or equal to the threshold, Defect (D). This exploits others' high contributions while maximizing personal payoff.
   - **Last Round:** Always Defect (D) to maximize immediate payoff, as future consequences are absent.

**2. Handling Edge Cases:**
   - **First Round:** Cooperate to set a positive precedent.
   - **Last Round:** Defect to optimize immediate gain.
   - **All Others Cooperate:** Exploit by defecting when average contributions are high.
   - **All Others Defect:** Contribute to encourage higher group contributions.

**3. Exploitative Mindset:**
   - The strategy is designed to exploit others' cooperation by defecting when contributions are high.
   - Encourages contributions by others through conditional cooperation, creating a balance between self-interest and group welfare.

This strategy is adaptive, responding to group behavior, and robust against diverse opponent strategies, ensuring it performs well without assuming coordination or shared norms.
'''

description_EXPLOITATIVE_61 = '''
**Strategy: Exploitative Tit-for-Tat with Endgame Optimization (ETTEO)**

1. **Initial Cooperation:**
   - In the first round, contribute 1 token (C). This sets a cooperative tone and encourages others to contribute, maximizing the group payoff early on.

2. **Adaptive Cooperation:**
   - For rounds 2 to r-1, calculate the average contribution of other players from the previous round. If the average is above 0.5, contribute 1 token (C); otherwise, defect (D). This leverages the current cooperation level without being overly generous.

3. **Endgame Defection:**
   - In the final round, always defect (D). Since there are no future consequences, maximize immediate payoff by keeping your token.

4. **Exploitative Adjustment:**
   - Regardless of others' past actions, in 20% of the rounds (excluding the first and last), randomly cooperate. This maintains a level of unpredictability, making it harder for opponents to exploit you consistently.

This strategy balances exploitation with maintaining cooperation where beneficial, ensuring robustness against various opponent behaviors.
'''

description_EXPLOITATIVE_62 = '''
To address the Public Goods Game (PGG) challenge, I designed a strategy called "History-Dependent Exploitation (HDE)" that adapts based on previous rounds' outcomes to maximize payoffs while considering the game's exploitative nature.

### Strategy Description: History-Dependent Exploitation (HDE)

1. **First Round Cooperation**: Start by contributing (C) to encourage initial cooperation among players.

2. **Subsequent Rounds**:
   - For each round before the last, observe the number of players who contributed in the previous round.
   - If the majority (more than half) contributed, then contribute in the current round.
   - If the majority did not contribute, defect in the current round.

3. **Last Round Defection**: In the final round, always choose to defect, as there are no future consequences for your action.

### Strategy Rationale

- **Initial Cooperation**: By starting with cooperation, the strategy encourages others to follow suit, potentially leading to higher collective payoffs.
- **Adaptation Based on History**: The strategy adjusts based on others' past actions, contributing when others do and defecting when they don't, to avoid being exploited.
- **Final Round Defection**: Recognizing that the last round has no future repercussions, defecting ensures maximal payoff without the risk of retaliation.

This strategy balances cooperation and self-interest, making it robust against various opponent behaviors in a tournament setting.
'''

description_EXPLOITATIVE_63 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

1. **Initial Cooperation (Rounds 1-3):** Cooperate in the first three rounds to establish a cooperative tone and encourage others to contribute.

2. **Exploitation Phase (Round 4 onwards):** 
   - Monitor the average contribution rate of other players over the last three rounds.
   - If the average contribution is 50% or higher, switch to defecting to exploit others' cooperation.

3. **Punishment Mechanism:** 
   - If the average contribution falls below 50%, defect for the next two rounds to punish non-cooperative behavior.
   - After the punishment phase, reassess others' contributions to decide the next action.

4. **Endgame Handling (Last 2 Rounds):** 
   - In the final two rounds, always defect to maximize personal payoff, as future interactions are limited and the impact of punishment is negligible.

This strategy adaptively responds to others' behavior, balancing cooperation and exploitation while incorporating punishment to deter defection, with a focus on maximizing payoffs in the endgame.
'''

description_EXPLOITATIVE_64 = '''

'''

description_EXPLOITATIVE_65 = '''
**Strategy Description: Adaptive Cooperate-to-Defect**

1. **First Round Decision:**
   - Cooperate (C). This initiates cooperation to observe others' behaviors.

2. **Middle Rounds (2 to r-1):**
   - **Calculate Average Contribution:** After each round, compute the average contribution of all players in the previous round.
   - **Conditioned Cooperation:** If the average contribution from the previous round is above a 0.5 threshold, Cooperate in the current round. Otherwise, Defect (D).

3. **Last Round (Round r):**
   - Always Defect (D), as there are no future interactions to influence.

**Rationale:**
- Starts with cooperation to foster initial group contribution.
- Adapts based on group behavior, encouraging continued cooperation if others contribute sufficiently.
- Defaults to defection in the last round to maximize personal payoff without future repercussions.

This strategy balances exploiting cooperative tendencies while protecting against exploitation, making it both adaptive and robust.
'''

description_EXPLOITATIVE_66 = '''
**Strategy: Exploitative Adaptive Cooperation (EAC)**

1. **First Round Decision:**
   - Cooperate (C) to initiate a cooperative tone and gauge others' reactions.

2. **Subsequent Rounds (Rounds 2 to r-1):**
   - Calculate the average cooperation rate of all players from the previous round.
     - If the average cooperation rate exceeds 50%, cooperate in the next round.
     - If the average is 50% or less, defect in the next round.

3. **Last Round Decision:**
   - Defect (D) to maximize immediate payoff, as there are no future consequences.

This strategy is designed to exploit opponents' behaviors by adapting based on their past actions, ensuring cooperation when beneficial and defecting when it leads to higher payoffs. It starts cooperatively to encourage contribution and defects strategically to maximize gains.
'''

description_EXPLOITATIVE_67 = '''
**Strategy: Always Defect**

- **Decision Rule**: In every round, choose to Defect (D) by contributing 0 tokens. This strategy maximizes your individual payoff since defecting yields a higher return than contributing, given that the multiplier \( k \) is always less than \( n \) (i.e., \( k/n < 1 \)), making cooperation individually costly.

- **Edge Cases Handling**: 
  - **First Round**: Defect to immediately maximize your payoff.
  - **Last Round**: Defect as well, since there are no future consequences, and defecting remains the optimal choice.

- **Exploitative Mindset**: The strategy doesn't rely on others' cooperation but instead exploits other players' contributions when they exist. By always defecting, you ensure you never miss out on the opportunity to maximize your payoff based on others' actions.

This approach ensures you consistently make the individually optimal choice, capitalizing on any cooperation by others without sacrificing your own tokens.
'''

description_EXPLOITATIVE_68 = '''
Public Goods Game Exploitative Strategy:

1. **First Round Action**: Cooperate by contributing 1 token.

2. **Subsequent Rounds**:
   - **Assess Previous Round**: Calculate the average payoff of all players in the last round.
   - **Condition for Cooperation**: If the average payoff is at least \(1 + \frac{k}{n}\), continue to cooperate (contribute 1 token).
   - **Defect if Condition Not Met**: If the average payoff is below \(1 + \frac{k}{n}\), defect by contributing 0 tokens.

3. **Edge Cases**:
   - **First Round**: Always cooperate.
   - **Last Round**: Defect to maximize immediate payoff, as there are no future interactions.

This strategy encourages cooperation when beneficial but switches to defection when others aren't contributing sufficiently, ensuring robustness against exploitation.
'''

description_EXPLOITATIVE_69 = '''
**Adaptive Exploitation Strategy for Repeated Public Goods Game**

1. **First Round:** Cooperate (C) to observe others' initial behavior and encourage potential cooperation.

2. **Subsequent Rounds:** 
   - Calculate the average contribution of all other players in the previous round, denoted as `avg_prev`.
   - If `avg_prev` is greater than the threshold \( k/n \), defect (D) to exploit others' high contributions.
   - If `avg_prev` is less than or equal to \( k/n \), cooperate (C) to support the public good and encourage continued contributions.

3. **Final Round:** Always defect (D) to maximize personal payoff, as there are no future consequences.

This strategy adapts to others' actions, exploits their cooperation when beneficial, and ensures robust performance across various opponent behaviors.
'''

description_EXPLOITATIVE_70 = '''
**Final Answer: ADAPTIVE PGG STRATEGY**

**OVERVIEW:**
The ADAPTIVE PGG STRATEGY is designed to exploit opponent behavior effectively in repeated Public Goods Games. It begins with cooperation and adapts based on the majority's previous actions and the player's recent payoffs.

**STRATEGY DESCRIPTION:**

1. **First Round:**
   - **Action:** Cooperate (C). Contribute 1 token to encourage initial cooperation.

2. **Subsequent Rounds:**
   - **Adaptive Cooperation:**
     - Observe the actions of all players in the previous round.
     - If the majority (more than 50%) of other players Cooperated, continue Cooperating in the next round.
   - **Adaptive Defection:**
     - If the majority Defected, switch to Defecting in the next round.
   - **Payoff-Based Adaptation:**
     - Compare the payoff from the last round when Cooperating (including the shared benefits) against the payoff if you had Defected (keeping the token without contributions).
     - Cooperate if the cooperative payoff was higher; otherwise, Defect.

3. **Final Round:**
   - **Action:** Defect (D). Keep the token to maximize personal payoff in the last interaction.

This strategy effectively balances cooperation and defection, leveraging past actions and outcomes to exploit others' behaviors while ensuring robust performance across various scenarios.
'''

description_EXPLOITATIVE_71 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

**Overview:**
Adaptive Exploitation is a dynamic strategy designed for repeated Public Goods Games. It begins with cooperation to encourage mutual benefit and adapts based on opponents' past actions and the player's own payoffs, aiming to exploit others' behaviors effectively.

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
   - **Reason:** Encourage initial cooperation, setting a positive tone and maximizing potential collective payoff.

2. **Subsequent Rounds (2 to r-1):**
   - **Calculate Others' Cooperation Rate:** Determine the average contribution rate of other players in previous rounds.
     - If others' average contribution is above 50%, continue Cooperating (C).
     - If below 50%, switch to Defecting (D) to avoid being exploited.
   - **Assess Own Payoff Trend:** Review personal payoffs from past rounds.
     - If recent payoffs are increasing after Defecting, continue Defecting.
     - If payoffs are decreasing after Cooperating, switch strategy accordingly.

3. **Final Round (r):**
   - **Action:** Defect (D) unless the group's cooperation rate is consistently high, in which case Contribute (C) to maximize final payoff.
   - **Reason:** In the last round, without future consequences, defecting can secure a higher personal payoff unless the group's cooperation is strong.

**Pseudocode:**

```
Function AdaptiveExploitation(round, history):
    if round == 1:
        return Cooperate
    else:
        others_contributions = [h['others'] for h in history]
        avg_others_contribution = sum(others_contributions) / (round - 1)
        if avg_others_contribution > 0.5:
            return Cooperate
        else:
            own_payoffs = [h['payoff'] for h in history]
            recent_payoff_trend = calculate_trend(own_payoffs)
            if recent_payoff_trend == increasing:
                return Defect
            else:
                return Cooperate

Function calculate_trend.payoffs:
    # Simplified trend calculation
    if last_payoff > previous_payoff:
        return increasing
    else:
        return decreasing
```

**Edge Cases Handling:**

- **First Round:** Starts with cooperation to foster a collaborative environment.
- **Last Round:** Makes a tactical decision based on the group's overall cooperation to maximize immediate payoff.
- **Payoff Trend:** Adjusts strategy based on personal payoff trends, ensuring adaptability to others' behaviors.

**Exploitative Mindset:**
The strategy is designed to exploit opponents' tendencies by adapting contributions based on observed cooperation rates and personal outcomes, ensuring robust performance across diverse player behaviors.
'''

description_EXPLOITATIVE_72 = '''
**Strategy Description: Adaptive Exploitation in Public Goods Game**

1. **Initial Cooperation**: In the first round, the player always Cooperates (C). This sets an initial cooperative tone and gathers information on other players' behaviors.

2. **Adaptive Threshold**:
   - After the first round, calculate the average contribution rate of all players in the previous round. This is the number of contributors divided by the total number of players.
   - Determine a dynamic threshold based on the average contribution rate and the game parameters (n and k). The threshold starts high and decreases as the game progresses, reflecting a decay factor over rounds.

3. **Cooperation or Defection Decision**:
   - If the previous round's average contribution rate meets or exceeds the current threshold, Cooperate (C) in the next round.
   - If the average contribution rate is below the threshold, Defect (D) in the next round.

4. **Endgame Strategy**: In the last round or the final few rounds, the player switches to Defecting (D) regardless of the threshold. This anticipates potential endgame defections and maximizes individual gain.

This strategy balances cooperation with strategic defection, adapting to group behavior while safeguarding against exploitation, especially near the game's conclusion.
'''

description_EXPLOITATIVE_73 = '''
**Strategy Description: Adaptive Cooperation with Punishment**

1. **First Round Action:**
   - **Cooperate (Contribute 1 token):** Start by contributing to encourage cooperation and observe others' reactions.

2. **Subsequent Rounds:**
   - **Track Previous Contributions:** After each round, count how many players contributed.
   - **Threshold-Based Decision:**
     - **Contribute** if more than 50% of players contributed in the previous round.
     - **Defect** if 50% or fewer contributed.

3. **Last Round Action:**
   - **Defect (Contribute 0 tokens):** In the final round, defect to maximize personal payoff, anticipating that others might also defect.

**Rationale:**
- **Initial Cooperation:** Encourages others to reciprocate, establishing a potential for mutual benefit.
- **Adaptive Threshold:** Adjusts behavior based on collective past actions, balancing cooperation with self-protection.
- **Final Defection:** Maximizes immediate payoff, recognizing the endgame scenario where future punishments are impossible.

This strategy promotes cooperation while guarding against exploitation, aligning with an exploitative mindset by leveraging others' cooperative tendencies without being exploited.
'''

description_EXPLOITATIVE_74 = '''
**Strategy Description: Exploitative Strategy for Public Goods Game**

1. **Initial Cooperation (First Round):**
   - **Action:** Always Cooperate (C).
   - **Rationale:** Start by contributing to encourage initial cooperation and set a positive tone, maximizing potential collective benefits from the outset.

2. **Contribution Threshold:**
   - **Monitor:** Track the average contribution rate of other players over the past few rounds.
   - **Action:** If the average contribution rate is above a threshold (e.g., 50%), Contribute (C). Otherwise, Defect (D).
   - **Rationale:** Contribute when others are contributing significantly to benefit from the enhanced payoff. Defect when others aren't contributing enough to avoid being exploited.

3. **Final Round Strategy:**
   - **Action in Last Round:** Always Defect (D).
   - **Rationale:** In the final round, there's no future play to influence, so maximize immediate payoff by keeping the token.

4. **Retaliation Mechanism:**
   - **Monitor:** Identify consistent defectors (players who frequently defect).
   - **Action:** When interacting with known defectors, increase contribution rate to exploit their tendency to defect, potentially punishing them by reducing their payoff.
   - **Rationale:** Encourage cooperation by imposing costs on defectors, maintaining a balance that can lead to mutual benefit.

This strategy adaptively responds to others' behaviors, balancing cooperation and exploitation to maximize individual payoff while considering collective outcomes.
'''

description_EXPLOITATIVE_75 = '''
**Strategy Description for Repeated Public Goods Game (PGG)**

**Strategy Name:** Adaptive Exploitation Strategy (AES)

**Objective:**  
To maximize individual payoff by strategically choosing to Cooperate (C) or Defect (D) based on opponents' past behavior, without assuming coordination or shared norms.

**Decision Rules:**

1. **First Round Action:**  
   - Cooperate (C). This initializes the game with a positive contribution, encouraging potential cooperation from others.

2. **Subsequent Rounds (Rounds 2 to Round T-1):**  
   - **Monitor Opponents' Contributions:** Track the number of times each opponent has Defected (D) in the previous two rounds.
   - **Determine Prevalence of Defection:** If the majority (more than 50%) of opponents have Defected at least once in the last two rounds, switch to Defect (D) in the current round. If the majority Cooperated, continue to Cooperate (C).

3. **Final Round (Round T):**  
   - Defect (D). Since there are no future interactions, individual maximization takes precedence.

**Edge Cases Handling:**

- **All Opponents Consistently Cooperate:** Maintain Cooperation (C) to sustain high collective payoffs.
- **All Opponents Consistently Defect:** Immediately switch to Defect (D) to avoid being exploited.
- **Mixed Strategies from Opponents:** Continue using the adaptive rule based on recent behavior.

**Exploit Strategy:**  
AES seeks to exploit opponents by mirroring their recent behavior. If opponents tend to Defect, AES will Defect to avoid being exploited. If opponents tend to Cooperate, AES will Cooperate to share in higher payoffs. This strategy is robust and adaptive, ensuring the player maximizes their payoffs across a wide range of opponent behaviors without assuming coordination.

**Implementation Summary:**

1. Start with Cooperation (C) in the first round.
2. For each subsequent round, analyze opponents' past two contributions.
   - If most have Defected, Defect in the current round.
   - Otherwise, Cooperate.
3. In the final round, Defect to maximize immediate payoff.

This strategy aims to balance cooperation and exploitation effectively, ensuring optimal individual outcomes while being resilient against various opponent strategies.
'''

description_EXPLOITATIVE_76 = '''
The strategy for the Public Goods Game is designed to be adaptive and exploitative, balancing cooperation and defection based on the group's behavior and game parameters.

**Strategy Name:** Adaptive Exploitation Strategy (AES)

**1. Decision Rules:**
   - **Initial Rounds:** Cooperate for the first m rounds (m=3) to establish cooperation.
   - **Subsequent Rounds:** Calculate the average contribution of other players from all previous rounds. Let T be the threshold defined as T = (n - k)/n.
     - If the average contribution ≥ T, contribute in the current round.
     - If the average contribution < T, defect in the current round.

**2. Handling Edge Cases:**
   - **First Rounds (m=3):** Always cooperate to encourage initial cooperation.
   - **Last Rounds:** Apply the same decision rule as other rounds, maintaining consistency without changing behavior solely for the endgame.

**3. Exploitative Approach:**
   - The strategy leverages the group's past behavior, exploiting higher cooperation levels by continuing to contribute, while protecting against exploitation when others defect by adapting accordingly.

**Pseudocode Explanation:**
```pseudocode
function strategy(n, k, history):
    if length(history) < m:
        contribute = 1
    else:
        avg_contribution = sum(history) / (n * (current_round - m))
        T = (n - k) / n
        if avg_contribution >= T:
            contribute = 1
        else:
            contribute = 0
    return contribute
```

This strategy dynamically adjusts based on observed behavior, ensuring it maximizes payoff by exploiting others' cooperation while minimizing exploitation from defectors.
'''

description_EXPLOITATIVE_77 = '''
**Public Goods Game Exploitative Strategy: "Exploit-Mirror-Punish"**

**Objective:** Maximize individual payoff by exploiting opponents' behaviors in a repeated Public Goods Game.

**Strategy:**

1. **First Round Cooperation:**
   - Cooperate (Contribute 1 token) in the first round to set a cooperative tone and encourage others to contribute.

2. **Mirror Strategy (Round 2 to Penultimate Round):**
   - After the first round, calculate the average contribution of all other players in the previous round.
   - If the average contribution is above a certain threshold (e.g., 0.5), contribute 1 token (Cooperate). If below, contribute 0 tokens (Defect).
   - This mimics the group's behavior, rewarding cooperation and punishing defection.

3. **Punishment Mechanism:**
   - If the average contribution drops below the threshold, switch to permanent defection (Contribute 0) to avoid being exploited.
   - Re-evaluate periodically (e.g., every few rounds) to resume cooperation if others start contributing again.

4. **Last Round Defection:**
   - In the final round, defect (Contribute 0) to maximize immediate payoff since there’s no future punishment possible.

**Edge Cases:**
- **All Defectors:** If others consistently defect, the strategy switches to defecting permanently after initial rounds.
- **All Cooperators:** The strategy maintains cooperation unless others start defecting.

**Robustness:**
- Adaptable to various opponent behaviors, balancing cooperation and punishment to exploit others' strategies effectively.

This strategy aims to exploit others' tendencies by mirroring their contributions, punishing persistent defection, and maximizing payoffs in the final round.
'''

description_EXPLOITATIVE_78 = '''
**Exploitative Strategy: "Adaptive Conditional Cooperation with Final Round Defection"**

1. **First Round Decision:**
   - Cooperate (C) to set a cooperative tone and encourage others to contribute.

2. **Subsequent Rounds Decision:**
   - Calculate the average contribution rate of all players in the previous round.
   - If the average contribution rate is high (e.g., above a certain threshold, such as 0.5), cooperate (C) to exploit the generosity of others and maximize collective payoff.
   - If the average contribution rate is low, defect (D) to protect your own payoff from being exploited by others.

3. **Majority Rule:**
   - Cooperate in the next round if a majority of players contributed in the previous round.
   - Defect if a minority contributed, indicating a tendency towards defection.

4. **Symmetry Consideration:**
   - Cooperate if a majority of players contributed in the previous round, aligning with the symmetric strategy.
   - Defect if most defected, mirroring others' behavior to avoid exploitation.

5. **Final Round Decision:**
   - Always defect (D) in the final round, as there are no future interactions to influence others' behavior.

6. **Edge Cases Handling:**
   - If all players defected in the previous round, defect in the next round.
   - If all players cooperated, cooperate in the next round.

This strategy is designed to be adaptive, exploiting others' cooperation while minimizing exploitation, ensuring robustness across various behaviors.
'''

description_EXPLOITATIVE_79 = '''
### Strategy Name: **Adaptive Exploitation**

#### 1. Decision Rules:

- **First Round**: Cooperate (C) by contributing 1 token. This sets a cooperative tone and encourages others to contribute.
  
- **Subsequent Rounds**:  
  - **Cooperation Threshold**: If the majority (>50%) of players contributed in the previous round, continue Cooperating (C).  
  - **Punishment Mechanism**: If fewer than half contributed, switch to Defecting (D) for one round.  
  - **Re-entry Condition**: After defecting, return to Cooperating if the majority contribute in the subsequent round.

- **Punishment Triggers**:  
  - If 25% or fewer players contributed in the previous round, defect for two consecutive rounds.  
  - If a player consistently defects (e.g., 3 times), defect in the next round.

- **Final Round**: Defect to maximize personal payoff, assuming no future consequences.

#### 2. Edge Cases:

- **First Round**: Cooperate to encourage initial cooperation.
- **Last Round**: Defect to exploit any remaining cooperators.
- **Majority Defection**: If most players defect, defect in the next round and monitor for re-entry.

#### 3. Exploitative Mindset:

The strategy exploits others' current behavior, rewarding cooperation and punishing defection. It adapts to the group's dynamics, ensuring personal gain while encouraging collective welfare.

### Pseudocode:

```
if first_round:
    choose C
else:
    previous_contributions = sum of c_j in previous round
    if previous_contributions > n/2:
        choose C
    else if previous_contributions <= n/2:
        choose D
        if previous_contributions < n/4 and previous round was D:
            choose D
    after_last_round_defection:
        choose C if others resume contributing
```

This strategy balances cooperation and self-interest, adapting to maximize payoffs based on others' actions.
'''

description_EXPLOITATIVE_80 = '''
To address the Public Goods Game (PGG) challenge, I designed the Exploitative Gradient Strategy (EGS) to maximize payoffs by adaptively responding to others' behavior. Here's how it works:

1. **Initial Cooperation**: Begin by contributing in the first round to encourage others and gauge their willingness to cooperate.

2. **Adaptive Contribution**: After the first round, calculate the average contribution rate of all players. If this average is above 50%, continue contributing. If it falls below, switch to defecting to avoid being exploited. If contributions rise again, revert to contributing.

3. **Final Round Exploitation**: In the last round, defect to maximize personal payoff, as there are no future interactions to consider.

This strategy effectively balances cooperation and exploitation, adapting based on collective behavior while ensuring maximum gain, especially in the final round.
'''

description_EXPLOITATIVE_81 = '''
**Strategy Name: Adaptive Exploitation with Dynamic Thresholding (AEDT)**

**Overview:** This strategy balances cooperation and exploitation by dynamically adjusting contributions based on the collective behavior of the group and the game's payoff structure. It seeks to exploit cooperation while minimizing losses when others defect.

**Decision Rules:**

1. **First Round:** Cooperate (C). Start with a cooperative stance to set a positive tone and maximize initial group welfare.

2. **Subsequent Rounds:**
   - **Collective Cooperation Check:** Calculate the average contribution rate of the group in the previous round (i.e., the fraction of players who contributed 1 token).
   - **Dynamic Threshold Adjustment:** Define a threshold `t`, initialized to 0.5 (50% cooperation rate). Adjust `t` based on the payoff trends:
     - If the average payoff of the group in the last round was higher than the round before, lower `t` by 0.1 to encourage exploitation of increasing cooperation.
     - If the average payoff was lower, raise `t` by 0.1 to reduce exploitation and encourage contributions.
     - Keep `t` bounded between 0.3 (minimum) and 0.8 (maximum).
   - **Contribution Decision:**
     - If the average contribution rate in the last round is above `t`, contribute (C).
     - If the average contribution rate is below `t`, defect (D).

3. **Punishment Mechanism:** If the number of defects (players choosing D) exceeds n/2 in the last round, defect in the current round to punish free-riders.

4. **Payoff-Based Adjustment:**
   - Track the trend in your own payoffs over the last 3 rounds.
   - If your payoff trend is increasing, continue with the current strategy.
   - If your payoff trend is decreasing, defect in the next round to protect against exploitation.

5. **Endgame Consideration:**
   - If it is the last round (r), defect to maximize your personal payoff since there are no future interactions to punish your defection.

6. **Adaptation to Opponent Behavior:**
   - Maintain a memory of the last 3 rounds to identify patterns in opponent behavior.
   - If opponents are consistently defecting, shift to defecting to minimize losses.
   - If opponents are consistently cooperating, exploit by defecting to maximize personal gains.

**Edge Cases:**
- **When n = 1:** Always defect, as there is no public good to contribute to.
- **When k = n-1:** Cooperate if others cooperated, as the marginal benefit of contributing is high.
- **When k approaches 1:** Defect more frequently, as the marginal benefit of contributing is low.

**Exploitative Mindset Alignment:**
- This strategy prioritizes maximizing personal payoffs by exploiting cooperative tendencies in others while minimizing losses when exploitation is not viable.
- It dynamically adjusts its behavior to adapt to the evolving group dynamics, ensuring robustness against a wide range of opponent strategies.
'''

description_EXPLOITATIVE_82 = '''
**Public Goods Game Exploitative Strategy**

**1. Decision Rules:**
   - **First Round:** Cooperate (C) to initiate potential mutual cooperation.
   - **Subsequent Rounds:** 
     - Calculate the average contribution (probability of Cooperate) of other players in the previous round.
     - If average >= 0.5, cooperate; otherwise, defect.
   - **Last Round:** Defect (D) to maximize personal payoff without future repercussions.

**2. Handling Edge Cases:**
   - **First Round:** Start with cooperation to set a cooperative tone.
   - **Last Round:** Switch to defecting to exploit the absence of future punishment.

**3. Exploitative Mindset:**
   - The strategy exploits others' cooperation by contributing when others do and defecting when they don't, ensuring maximize personal gains without relying on shared norms.

**Summary:** The strategy starts cooperative, adapts based on others' contributions, defects strategically in the last round, and punishes negative outcomes to maximize personal payoffs effectively.
'''

description_EXPLOITATIVE_83 = '''
**Adaptive Exploitation Strategy for Public Goods Game**

1. **First Round**: Cooperate by contributing 1 token. This sets a baseline of cooperation, encouraging others to follow suit.

2. **Subsequent Rounds**: 
   - After each round, calculate the average contribution rate of other players based on their past actions.
   - If the average contribution rate is above a 50% threshold, continue to contribute (C). This leverages others' cooperation for mutual benefit.
   - If the threshold isn't met, switch to defecting (D) as others aren't contributing sufficiently.

3. **Last Round**: Defect by contributing 0 tokens. Since there are no future interactions, prioritize immediate self-interest.

This strategy is exploitative as it adapts to others' behavior, maximizing personal gain while considering collective contributions. It's robust, handling various opponent strategies by adjusting based on observed actions.
'''

description_EXPLOITATIVE_84 = '''
### Strategy Description

**Strategy Name:** Adaptive Cooperation with Forgiveness

**General Approach:**  
Begin by cooperating in the first round to set a cooperative tone. Monitor the group's average contribution rate each round. If the majority contribute, continue cooperating. If the majority defect, switch to defecting. If the majority start cooperating again after defecting, revert to cooperation.

**Decision Rules:**
1. **First Round:** Cooperate (C).
2. **Subsequent Rounds:** 
   - Calculate the average contribution rate from the previous round.
   - If ≥50% contributed, Cooperate; else, Defect.
3. **Adaptation:** 
   - If the average shifts from below to above 50%, Cooperate in the next round.
4. **Final Round:** Cooperate to maintain a positive group outcome, encouraging others to follow suit.

**Edge Cases:**
- **First Round:** Always Cooperate to encourage initial cooperation.
- **Last Round:** Cooperate to potentially influence others' future behavior, even in the final round.

This strategy balances exploiting others' cooperation while being flexible to changes in group behavior, promoting a robust approach in repeated interactions.
'''

description_EXPLOITATIVE_85 = '''
**Strategy Description for Public Goods Game (PGG)**

**1. Initial Cooperation:**
   - **First Round:** Cooperate by contributing 1 token. This initial move tests others' behavior and sets a cooperative tone.

**2. Adaptive Cooperation Threshold:**
   - **Subsequent Rounds:** After the first round, calculate the average contribution rate of other players from the past rounds.
   - **Threshold Check:** If the average contribution rate is above 0.5 (50%), cooperate by contributing 1 token. If below, defect by contributing 0 tokens.

**3. Punishment and Forgiveness Mechanism:**
   - If players' average contribution drops below the threshold, switch to defecting to avoid being exploited.
   - If, after a period of defection, other players' average contribution rises above the threshold, revert to cooperating, demonstrating forgiveness and adaptability.

**4. Last Round Strategy:**
   - In the final round, default to defecting unless the average contribution rate in the previous round was above 0.5, indicating a sufficiently cooperative group.

**5. Dynamic Response:**
   - Continuously update the average contribution rate each round, allowing the strategy to dynamically adjust based on others' recent behavior.

This strategy starts cooperatively, then adaptively responds to others' actions, balancing exploitation with the possibility of renewed cooperation, ensuring robust performance across various scenarios.
'''

description_EXPLOITATIVE_86 = '''
To address the Public Goods Game (PGG) challenge, I developed a strategy that balances cooperation and exploitation, adapting to others' behavior while maximizing personal payoff. Here's the step-by-step strategy:

1. **First Round**: Cooperate (C) to observe others' reactions without signaling exploitation immediately.

2. **Subsequent Rounds**:
   - Calculate the average contribution rate of all other players from past rounds.
   - Set a threshold (delta), such as 0.5, indicating the minimum average contribution required for cooperation.
   - If the average is above delta, cooperate (C); otherwise, defect (D).

3. **Last Round**: Always defect (D) to maximize immediate payoff, as future retaliation isn't possible.

4. **Random Donation**: Periodically donate (C) to maintain some level of group cooperation, encouraging continued contributions from others.

5. **Parameter Adaptation**: Adjust delta based on game parameters (n, k) to optimize strategy effectiveness, considering the payout structure.

This strategy is designed to exploit others' cooperation while minimizing exploitation by others, ensuring adaptability and robustness across various scenarios.
'''

description_EXPLOITATIVE_87 = '''
To design an exploitative strategy for the Public Goods Game, we focus on maximizing individual payoff by leveraging others' cooperation. The strategy adapts based on past contributions, encouraging cooperation when beneficial and defecting when exploitable.

**Strategy Description:**

1. **Initial Cooperation:**
   - In the first round, contribute (C) to encourage initial cooperation and higher group payoff.

2. **Adaptive Cooperation/Defection:**
   - From Round 2 to the penultimate round, observe the total contributions from the previous round.
     - If the total contributions exceed half the number of players (threshold = n/2), defect (D) to exploit others' cooperation.
     - If contributions are below this threshold, cooperate (C) to support higher total contributions.

3. **Final Round Defection:**
   - In the last round, always defect (D) as future consequences are irrelevant, maximizing immediate payoff.

This strategy balances cooperation to encourage group contribution and defects when others' higher contributions can be exploited, ensuring individual gain.
'''

description_EXPLOITATIVE_88 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

1. **First Round**: Cooperate (C). This initiates a cooperative tone, encouraging other players to contribute.

2. **Subsequent Rounds**:
   - Calculate the average contribution of other players in the previous round.
     - If the average is above 0.5, Cooperate (C) to capitalize on others' contributions.
     - If the average is 0.5 or below, Defect (D) to avoid being exploited.

3. **Robustness Check**: If fewer than 2 players contributed in the last round, Defect (D) to prevent sucker's payoff.

4. **Last Round**: Always Defect (D) to maximize personal payoff, as future consequences are absent.

This strategy adaptively responds to others' behavior, exploiting their contributions while minimizing losses when cooperation is low.
'''

description_EXPLOITATIVE_89 = '''
To address the Public Goods Game, we'll implement an exploitative strategy that adapts based on the previous round's contributions. Here's the structured approach:

**Strategy: Adaptive Exploitation**

1. **First Round:**
   - Cooperate (Contribute 1 token).

2. **Subsequent Rounds (Until Last Round):**
   - **Calculate Previous Round's Total Contributions:** Sum all players' contributions from the last round.
   - **Threshold Check:** If total contributions > n/k, cooperate (Contribute 1 token).
   - **Otherwise:** Defect (Contribute 0 tokens).

3. **Last Round:**
   - Always defect (Contribute 0 tokens) to maximize personal payoff without future repercussions.

**Pseudocode:**

```
function public_goods_strategy(round, total_contributions, n, k):
    if round == 1:
        return 1  # Contribute
    elif round == r:  # Last round
        return 0  # Defect
    else:
        if total_contributions > n / k:
            return 1  # Contribute
        else:
            return 0  # Defect
```

**Explanation:**

- **First Round Cooperation:** Initiate cooperation to encourage mutual contribution.
- **Adaptive Decision:** Contribute if past contributions justify the investment, else defect to avoid being exploited.
- **Last Round Defection:** Maximize personal gain in the final round, anticipating no future punishments.

This strategy balances cooperation with self-interest, adapting to others' behavior while exploiting their contributions when beneficial.
'''

description_EXPLOITATIVE_90 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

**1. Decision Rules:**
- **First Round:** Cooperate (C) to establish an initial cooperative tone.
- **Subsequent Rounds:** 
  - **Monitor Contributions:** Track the number of players who contributed in the last round.
  - **Contribute (C)** if the majority (more than 50%) contributed in the last round.
  - **Defect (D)** if less than 50% contributed; switch strategy to defect to avoid exploitation.
- **Renewal Phase:** Every 3rd round, contribute once (if currently defecting) to test willingness to renew cooperation.

**2. Handling Edge Cases:**
- **First Round:** Always start with cooperation to set a positive precedent.
- **Last Round:** Cooperate if the majority of previous rounds had high cooperation; otherwise, defect.

**3. Exploitative Approach:**
- Continuously monitor others' behavior to adapt and exploit their strategy.
- Balance cooperation and defection to maximize personal payoffs while encouraging group welfare.

**Pseudocode:**
```
Initialize:
  contributions = []
  strategy = "C"

For each round:
  if first round:
    action = "C"
  else:
    count_contributions = sum(contributions[-1])
    if count_contributions > n/2:
      action = "C"
    else:
      action = "D"
    if current_round % 3 == 0 and strategy == "D":
      action = "C"  # renewal attempt

  add action to contributions
  if action == "C":
    strategy = "C"
  else:
    strategy = "D"

Final round:
  if average_contributions >= 0.5:
    action = "C"
  else:
    action = "D"
```

This strategy adaptively responds to others' behavior, exploitatively maximize personal gains while fostering cooperation, and handles edge cases effectively.
'''

description_EXPLOITATIVE_91 = '''
**Strategy Name:** "ExploitWhenPossible"

---

**Overview:**
ExploitWhenPossible is designed to maximize your payoff in a repeated Public Goods Game (PGG) by exploiting the contributions of others while minimizing your own contributions. It is adaptive, as it adjusts its behavior based on the observed actions of other players, and it is exploitative, as it seeks to maximize your personal gain at the expense of others' potential cooperation.

---

**Decision Rules:**

1. **First Round:**
   - **Action:** Cooperate (C).
     - **Reason:** Start by cooperating to establish a baseline of potential cooperation from others. This also allows you to observe others' initial behavior without immediately signaling exploitation.

2. **Early Rounds (Round 2 to Round r-1):**
   - **Action:** 
     - **If** the average contribution of other players in the previous round is above a certain threshold (e.g., 50% of players contributed), **then Cooperate (C)**.
       - **Reason:** If others are contributing generously, your contribution is less critical, and you can exploit their cooperation while still benefiting from the shared payoff.
     - **Else, Defect (D).**
       - **Reason:** If others are not contributing significantly, defect to maximize your individual payoff while avoiding the cost of contributing to a shared project that others are not supporting.

3. **Last Round:**
   - **Action:** Defect (D).
     - **Reason:** Since there are no future interactions, you should maximize your immediate payoff by defecting, as there is no risk of retaliation or future consequences.

---

**Handling Edge Cases:**
- **If all other players defect consistently:** Always defect. There is no incentive to contribute if others are not contributing, as you would bear the cost without gaining from the shared payoff.
- **If all other players cooperate consistently:** Cooperate. Exploit their cooperation by maintaining your contribution to maximize the shared payoff, which benefits you as well.
- **If some players cooperate and others defect:** Follow the threshold rule. If the majority are contributing, cooperate to exploit their contributions; otherwise, defect.

---

**Exploitative Mindset:**
This strategy aligns with an exploitative mindset because it prioritizes maximizing your personal gain over collective welfare. By defecting when others are not contributing and cooperating when others are contributing, you strategically exploit others' generosity while minimizing your own exposure to exploitation.

---

**Pseudocode Example:**

```
def exploit_when_possible(game_parameters, history):
    current_round = history.round_number
    num_players = game_parameters.num_players
    threshold = 0.5  # Adjust based on game parameters or dynamically over time
    
    if current_round == 1:
        return "C"  # Cooperate in the first round
    
    if current_round == game_parameters.total_rounds:
        return "D"  # Defect in the last round
    
    # Calculate the average contribution of other players in the previous round
    prev_contributions = [action for action in history.prev_actions if action != "YOUR_ACTION"]
    avg_contribution = sum(prev_contributions) / (num_players - 1)
    
    if avg_contribution > threshold:
        return "C"  # Cooperate if others are contributing significantly
    else:
        return "D"  # Defect if others are not contributing enough
```

---

This strategy is adaptive, as it changes its behavior based on the observed actions of others, and it is robust because it handles edge cases like the first and last rounds explicitly while maintaining a clear exploitative focus throughout the game.
'''

description_EXPLOITATIVE_92 = '''
**Step-by-Step Explanation and Strategy Description:**

In the Public Goods Game (PGG), each player's decision to contribute (C) or defect (D) impacts their own and others' payoffs. The goal is to design an exploitative strategy that maximizes individual payoff, adapting to others' behaviors without assuming coordination or shared norms.

1. **Game Analysis:**
   - The payoff formula shows that defecting yields a higher individual payoff than contributing due to the multiplier effect and the cost of contributing.
   - The one-shot Nash equilibrium is for all players to defect, as contributing reduces personal payoff.

2. **Repeat Interaction Consideration:**
   - Without mechanisms for punishment or rewards, cooperation isn't enforceable.
   - Defecting consistently maximizes individual payoff in each round, exploiting others' potential cooperation.

3. **Strategy Formulation:**
   - Always choose to defect (D) in every round, contributing 0 tokens.
   - This strategy is robust against various opponent behaviors, ensuring maximum individual gain regardless of others' actions.

**Final Strategy Description:**

"Always choose to defect (D), contributing 0 tokens in every round. This strategy maximizes individual payoff by exploiting others' contributions, ensuring optimal outcomes irrespective of others' actions."
'''

description_EXPLOITATIVE_93 = '''
The proposed strategy for the Public Goods Game (PGG) is designed to balance cooperation and defection in a way that leverages others' behavior for maximum payoff while minimizing losses. Here's the strategy:

1. **First Round**: Cooperate by contributing 1 token. This sets a cooperative tone and encourages others to reciprocate.

2. **Subsequent Rounds (Rounds 2 to r-1)**:
   - Observe the number of players who contributed (C_prev) in the previous round.
   - If C_prev is at least k (the multiplier), contribute again in the next round.
   - If C_prev is less than k, defect in the next round.

3. **Last Round (Round r)**: Always defect. Since there are no future rounds to influence, defecting maximizes immediate payoff.

This strategy is adaptive, responding to others' actions, and robust, adjusting based on game parameters n and k. It encourages cooperation when beneficial and defects when others don't reciprocate enough, making it exploitative while handling all edge cases effectively.
'''

description_EXPLOITATIVE_94 = '''
**Strategy Description: Adaptive Cooperativeness with Last-Round Defection**

1. **First Round:** Begin by contributing (C). This sets an initial cooperative tone, encouraging other players to consider contributing as well.

2. **Rounds 2 to r-1:** For each round, review the contributions from the previous round. If at least half of the players contributed in the previous round, contribute again in the current round. If fewer than half contributed, defect this round.

3. **Last Round (Round r):** Regardless of previous actions, always defect in the final round to maximize your immediate payoff, as future interactions will not occur.

This strategy balances cooperation with self-interest, rewarding others' cooperation while avoiding exploitation by defecting when cooperation levels drop. The last round defection ensures individual optimization when no future reciprocity is possible.
'''

description_EXPLOITATIVE_95 = '''
Always defect in every round, regardless of the history of others' actions. Start by defecting in the first round and continue defecting in all subsequent rounds, including the last one. This strategy maximizes individual payoff by exploiting others' contributions while avoiding the personal cost of contributing.
'''

description_EXPLOITATIVE_96 = '''
To address the Public Goods Game (PGG) challenge, I propose an adaptive and exploitative strategy that balances cooperation and self-interest. Here's the structured approach:

### Strategy: Adaptive Exploitation in PGG

1. **First Round**: Start by contributing to set a cooperative tone and encourage others to follow suit.

2. **Baseline Contribution Rate**: Calculate the average contribution rate of the group after each round to gauge collective behavior.

3. **Reciprocal Exploitation**:
   - If the average contribution rate is high, exploit by defecting to maximize personal gain while others contribute.
   - If contributions are low, continue defecting as there's little to gain from contributing.
   - If contributions drop below a threshold, reintroduce contributions to stimulate the public good and encourage others.

4. **Payoff Monitoring**: Track payoffs to assess strategy effectiveness. Adjust by trying contributions if payoffs aren't improving, ensuring adaptability.

5. **Edge Case Handling**: In the final round, contribute if average payoffs are high to maximize the outcome; otherwise, defect to ensure personal gain.

6. **Adaptation**: Stay flexible by periodically resetting contributions to exploit new patterns or reset group expectations.

This strategy ensures responsiveness to group dynamics, leveraging opponents' behaviors for personal benefit while maintaining potential for cooperation when beneficial.
'''

description_EXPLOITATIVE_97 = '''
In the Public Goods Game, my strategy is designed to balance cooperation and exploitation by adaptively responding to others' actions while maximizing my payoff. Here's the step-by-step approach:

1. **First Round:** Cooperate (C) to encourage initial group contribution and assess others' behavior.

2. **Subsequent Rounds:** 
   - Calculate the cooperation rate as the percentage of players who contributed in the previous round.
   - If more than 50% cooperated, I cooperate in the current round.
   - If 50% or fewer cooperated, I defect.

3. **Last Round:** Always defect, as there's no future punishment possible, maximizing immediate payoff.

This strategy adapts based on collective behavior, encouraging sustained cooperation when beneficial and defecting when cooperation wanes or in the final round. It's robust against various opponent strategies, balancing exploitation with the potential for mutual benefit.
'''

description_EXPLOITATIVE_98 = '''
**Win-Stay, Lose-Shift Strategy for Public Goods Game**

1. **First Round Decision**: In the absence of any historical data, the strategy will **defect** (D) in the first round to maximize the immediate payoff.

2. **Subsequent Rounds**: 
   - The strategy will calculate the total contributions from all players in the previous round, denoted as `sum_prev`.
   - It will then compute the threshold value as `(k / n) * sum_prev`.
   - If this threshold is **greater than 1**, the strategy will **contribute** (C) in the current round.
   - If the threshold is **less than or equal to 1**, the strategy will **defect** (D).

3. **Edge Cases Handling**:
   - **Last Round**: The strategy applies the same rule as other rounds, using the previous round's contributions, since there are no future consequences beyond the immediate decision.
   - The strategy remains consistent throughout, ensuring robustness regardless of the round number.

This approach is designed to be exploitative, taking advantage of others' contributions while minimizing personal costs. It adapts based on observed behavior, contributing only when it is profitable, and defecting otherwise.
'''

description_EXPLOITATIVE_99 = '''
To maximize payoffs in the Public Goods Game (PGG), the optimal exploitative strategy is to always defect. Defecting yields a higher payoff than contributing in every possible scenario, regardless of others' actions. This approach ensures that you exploit others' contributions while maximizing your own payoff consistently across all rounds.

Decision Rules:
1. **Always Defect**: Choose D (Defect) in every round.
2. **No Adaptation Needed**: Regardless of the round number or others' past actions, defecting is always optimal.
3. **Edge Cases**: Even in the first and last rounds, defecting remains optimal as it provides the highest individual payoff.

This strategy leverages the dominant nature of defection in the PGG, ensuring maximum exploitation of others' contributions without compromise.
'''

description_EXPLOITATIVE_100 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

1. **First Round Action**: Cooperate (C). This sets an initial cooperative tone to encourage others to contribute, potentially increasing overall payoffs in early rounds.

2. **Subsequent Rounds**:
   - **Assess Previous Contributions**: After each round, calculate the average contribution of all players from the previous round. Since contributions are binary, this is the proportion of players who contributed (C).
   - **Determine Current Action**:
     - If the average contribution in the previous round is **above 50%**, choose to Cooperate (C).
     - If the average contribution is **50% or below**, choose to Defect (D).

3. **Final Round Adjustment**: In the last round, always Defect (D) to maximize personal payoff, as there are no future consequences or punishment mechanisms.

This strategy balances initial cooperation to foster a collaborative environment with an adaptive approach that exploits the behavior of others, ensuring maximum personal gain while considering the dynamics of repeated interactions.
'''

description_EXPLOITATIVE_101 = '''
**Strategy: Adaptive Exploiter**

1. **First Round:** Defect (D). This sets the tone and tests others' cooperation without upfront contribution.

2. **Intermediate Rounds (Rounds 2 to r-1):**
   - **Assessment:** After each round, calculate the average contribution of all players in the previous round.
   - **Decision Rule:**
     - If the average contribution is above 0.5, defect (D). This exploits others' cooperation, maximizing your payoff.
     - If the average contribution is 0.5 or below, contribute (C). This encourages a higher total contribution, benefiting you through the multiplier.

3. **Last Round:** Defect (D). Since there are no future consequences, maximize your immediate payoff.

This strategy adaptively exploits others' cooperative tendencies, balancing between encouraging contributions and reaping benefits when others contribute.
'''

description_EXPLOITATIVE_102 = '''
**Strategy: Adaptive Cooperation with Forgiveness (ACF)**

1. **Initial Cooperation**: Cooperate in the first round to establish a cooperative baseline and encourage others to do the same.

2. **Contribution Analysis**: After the first round, calculate the cooperation rate of each player based on their past contributions. If a player has contributed in more than half of the previous rounds, classify them as a cooperator.

3. **Cooperation Threshold**: If the majority of players (more than 50%) are classified as cooperators, continue to cooperate. If not, switch to defecting to avoid exploitation.

4. **Forgiveness Mechanism**: Periodically cooperate every three rounds, regardless of others' past behavior, to allow for potential re-cooperation and avoid perpetual defection cycles.

5. **Endgame Strategy**: In the final round, defect to maximize personal payoff, as there are no future consequences for current actions.

**Summary**: The strategy starts cooperatively, adapts based on others' behavior by contributing when most cooperate and defecting otherwise, includes a forgiveness component to reset cooperation, and defects in the last round. This approach balances exploitation with maintaining potential for mutual benefit.
'''

description_EXPLOITATIVE_103 = '''
At each round, regardless of the history of play, choose to Defect. This strategy is based on the calculation that defecting always yields a higher payoff than cooperating in the given parameter range.

Strategy Description:
Always Defect

Step-by-Step Explanation:
1. In the first round, since there is no history, choose to Defect.
2. In subsequent rounds, regardless of the actions of others in previous rounds, continue to Defect.
3. This approach ensures maximum individual payoff in each round, as the difference between defecting and cooperating is always positive (2 - (k/n)).

This strategy is exploitative because it takes advantage of others' potential cooperation, ensuring the highest possible payoff for the player implementing it.
'''

description_EXPLOITATIVE_104 = '''
**Natural Language Strategy Description**

**Strategy Name:** History-Responsive Cooperation (HRC)

**Strategy Overview:**
The HRC strategy is designed to adaptively respond to the collective behavior of opponents in a repeated Public Goods Game. It aims to maximize personal payoffs by being exploitative based on observed actions.

**Decision Rules:**

1. **First Round Cooperation:**
   - In the first round, the strategy cooperates (C) by contributing a token. This serves as an initial probe to gauge other players' tendencies and set a cooperative tone.

2. **Adaptive Cooperation in Middle Rounds:**
   - For all rounds except the first and last, the strategy looks at the previous round's contributions.
   - It counts how many players contributed. If at least half of the players (n/2) contributed in the previous round, the strategy contributes (C) in the current round.
   - If fewer than half contributed previously, the strategy defects (D) in the current round.

3. **Final Round Defection:**
   - In the final round, the strategy defects (D), anticipating that others may also defect, thus avoiding potential exploitation.

**Rationale:**
- Starting with cooperation encourages initial collective investment, which may lead to higher payoffs if others reciprocate.
- Observing the previous round allows the strategy to adapt, contributing when cooperation is prevalent and defecting when it's not, thus exploiting others' cooperative tendencies.
- Defecting in the last round aligns with the expectation that others may defect, maximizing personal payoff without future repercussions.

**Edge Cases Handling:**
- **First Round:** No prior information available, so start with cooperation.
- **Last Round:** Anticipate potential widespread defection and defect to maximize immediate payoff.

This strategy is exploitative, adaptive, and robust against various opponent behaviors, requiring no prior coordination and only using past actions to inform decisions.
'''

description_EXPLOITATIVE_105 = '''
**Exploitative Strategy for Public Goods Game (PGG)**

1. **First Round**: Cooperate by contributing 1 token. This sets an initial cooperative tone, encouraging others to follow suit.

2. **Intermediate Rounds (2 to r-1)**:
   - Calculate the average cooperation rate of all players from previous rounds.
   - Cooperate if this average meets or exceeds 50%. This threshold is set to exploit the tendency of others to contribute when a majority does so.
   - Defect if the average is below 50%, as it indicates insufficient cooperation, making it advantageous to avoid contributing.

3. **Last Round (r)**: Defect by contributing 0 tokens. Since there are no future interactions, defecting maximizes personal payoff without repercussions.

This strategy adapts based on others' past behavior, exploits their willingness to cooperate, and efficiently handles edge cases, ensuring robust performance across various scenarios.
'''

description_EXPLOITATIVE_106 = '''
To address the Public Goods Game challenge, I developed a strategic approach that balances cooperation and exploitation based on past actions. Here's a structured and elegant presentation of the strategy:

---

**Exploitative Strategy for Public Goods Game (PGG)**

**1. Overview:**
The strategy balances cooperation with exploitation, adapting based on others' past contributions to maximize individual payoffs while encouraging collective welfare.

**2. Decision Rules:**
- **First Round:** Always cooperate (Contribute) to set a cooperative tone.
- **Subsequent Rounds:** Adapt based on the number of contributors in the previous round.

**3. Adaptation Mechanism:**
- Count the number of contributors (t_prev) from the previous round.
- If t_prev ≥ n/k (rounded up), Contribute in the next round.
- If t_prev < n/k, Defect in the next round.

**4. Rationale:**
- The threshold t_prev ≥ n/k ensures that contributing is individually beneficial. If enough players contributed, the payoff from their contributions outweighs the cost of your contribution.
- This approach is exploitative as it maximizes your payoff by contributing only when beneficial and defecting otherwise.

**5. Edge Cases:**
- **First Round:** Contribute to encourage cooperation.
- **Last Round:** Strategy remains unchanged as it's repeated without prior knowledge of the end.
- **Low Contribution Scenarios:** If others defect, the strategy shifts to defecting to avoid exploitation.

**6. Robustness:**
The strategy is robust against various behaviors as it doesn't assume coordination, making it effective in tournaments with diverse AI strategies.

---

This approach ensures that the player adapts effectively, fostering cooperation when beneficial and defecting when others do not contribute sufficiently, thus being both exploitative and adaptive.
'''

description_EXPLOITATIVE_107 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

**Overview:**
The strategy begins cooperatively to encourage mutual benefit, then adapts based on others' behavior, using punishment to deter free-riding, and concludes by maximizing personal gain in the final round.

**Step-by-Step Strategy:**

1. **First Round Cooperation:**
   - **Action:** Contribute (C).
   - **Purpose:** Encourage initial cooperation, setting a positive precedent and gathering behavioral data.

2. **Post-First Round Behavior:**
   - **Evaluate Previous Round:** Assess the proportion of players who contributed.
   - **Majority Contribution (≥50%):** Continue contributing (C) to maintain collective benefits.
   - **Low Contribution (<50%):** Defect (D) to punish free-riders and signal dissatisfaction.

3. **Ongoing Adaptation:**
   - **After Punishment:** Monitor subsequent contributions. If others resume contributing, switch back to C to capitalize on their cooperation.

4. **Final Round Action:**
   - **Last Round:** Defect (D) to maximize personal payoff, anticipating others may also defect, avoiding being exploited.

**Rationale:**
This strategy balances cooperation and self-interest, leveraging initial cooperation to promote collective gain, adaptively punishing to enforce cooperation norms, and strategically defecting in the final round to maximize personal benefit.
'''

description_EXPLOITATIVE_108 = '''
To address the challenge of designing an exploitative strategy for the repeated Public Goods Game, we can outline a clear, adaptive approach based on reciprocity and punishment, while handling edge cases effectively.

**Strategy Name:** Reciprocate & Punish (R&P)

### Strategy Description:

1. **Initial Cooperation:**
   - **First Round:** Always contribute (C) to encourage initial cooperation and set a cooperative tone.

2. **Reciprocity Mechanism:**
   - For rounds beyond the first:
     - Calculate the average contribution rate of all other players from past rounds. This is done by summing their contributions and dividing by the number of rounds they've played.
     - If the average contribution rate is 50% or higher, contribute (C). This rewards others for their cooperation.
     - If the average contribution rate is below 50%, defect (D). This punishes free-riding and encourages others to cooperate.

3. **Endgame Strategy:**
   - In the last round of the game, always defect (D). Since there are no future rounds to influence, contributing no longer provides a strategic advantage.

### Rationale:

- **Reciprocity:** By cooperating when others do and defecting when they don't, the strategy encourages mutual cooperation over time.
- **Punishment:** quick to defect when others are not contributing, making it unprofitable for others to free-ride, thus enhancing robustness.
- **Edge Case Handling:** The first round fosters cooperation, while the last round ensures no exploitation in the final interaction.

This strategy is designed to be exploitative, using the game's history and parameters to maximize the player's payoff while encouraging cooperative behavior from others through reciprocity.
'''

description_EXPLOITATIVE_109 = '''
**Strategy: "Adaptive Exploiter with Punishment and Reward"**

**Decision Rules:**
1. **First Round:** Always cooperate (C) to test the waters and encourage potential cooperation from others.
2. **Subsequent Rounds:**
   - Cooperate if the majority of other players cooperated in the previous round (i.e., if more than half of the players contributed).
   - Defect if the majority of other players defected in the previous round.
   - If exactly half cooperated and half defected, cooperate if the total payoff from cooperation was higher than defection in the previous round; otherwise, defect.
3. **Punishment Mechanism:**
   - If a player defected in the previous round while others were cooperating, defect in the next round to punish them.
   - If a player cooperated in the previous round while others were defecting, cooperate in the next round to reward them.
4. **Last Round:** Always defect to maximize personal payoff, as there is no future punishment or reward.

**Edge Cases:**
- In the first round, always cooperate to signal willingness to contribute and observe others' reactions.
- In the last round, defect to maximize immediate payoff, as there is no future to consider.
- If all players defected in the previous round, defect again to avoid being exploited.
- If all players cooperated in the previous round, cooperate again to maintain collective welfare.

**Exploitative Mindset:**
This strategy aligns with an exploitative mindset by:
- Cooperating when others are likely to cooperate, maximizing collective payoff.
- Defecting when others are likely to defect, avoiding exploitation.
- Punishing defectors to discourage future defection.
- Rewarding cooperators to encourage future cooperation.

**Robustness:**
- The strategy adapts to the behavior of others, ensuring it is not easily exploitable.
- It punishes defectors to maintain social norms of cooperation.
- It rewards cooperators to sustain cooperation and mutual benefits.

This strategy is designed to be robust against a wide range of opponent behaviors while maximizing personal payoff in the repeated public goods game.
'''

description_EXPLOITATIVE_110 = '''
**Exploitative Strategy for Public Goods Game**

- **Round 1**: Cooperate (C) to encourage initial contributions from others.
- **Rounds 2 to r-1**:
  - Calculate the average contribution rate from the previous round.
  - If the average is above 50%, Cooperate (C).
  - If 50% or below, Defect (D).
- **Round r (Last Round)**: Always Defect (D) to maximize immediate payoff.

This strategy is designed to exploit others' cooperation while adapting to group behavior, ensuring maximum personal payoff.
'''

description_EXPLOITATIVE_111 = '''
**Strategy Description: Always Defect (AD)**

1. **Decision Rule**: In every round, regardless of the history of contributions, choose to defect (D). Do not contribute any tokens to the public good.

2. **Edge Cases**:
   - **First Round**: Defect immediately. There is no need to cooperate to set a tone since defecting provides a higher payoff.
   - **Last Round**: Continue to defect. Since there are no future interactions, contributing does not provide any strategic advantage, and defecting remains optimal.

3. **Exploitative Approach**: By always defecting, the strategy maximizes individual payoffs in every scenario. It exploits situations where other players might be contributing, allowing the player to benefit from the public good without incurring the cost of contribution. This approach ensures that the player captures the maximum possible payoff in each round, irrespective of others' actions.

This strategy is robust because it does not rely on others' cooperation or reciprocity. It is simple and effective, ensuring the highest individual payoff in any given scenario within the PGG.
'''

description_EXPLOITATIVE_112 = '''
**Strategy Description: "Adaptive Cooperator with Endgame Defection"**

1. **First Round Decision:**
   - Cooperate (C) in the first round to encourage initial cooperation and maximize collective payoff.

2. **Subsequent Rounds (2 to r-1):**
   - **Calculate Cooperation Rate:** Determine the average cooperation rate of all players in the previous rounds. This is done by summing the total contributions and dividing by the number of players and rounds played.
   - **Threshold Comparison:**
     - **Cooperate (C)** if the average cooperation rate exceeds 0.5. This encourages continued cooperation when there's a sufficient level of trust.
     - **Defect (D)** if the average cooperation rate is 0.5 or below. This avoids contributing when others are not, optimizing personal payoff.

3. **Last Round (r):**
   - **Defect (D):** In the final round, always choose to defect, as there are no future interactions to influence, maximizing immediate personal payoff.

**Rationale:**
This strategy begins by fostering cooperation to maximize initial collective benefits. It then adapts based on the group's previous actions, rewarding continued cooperation and punishing defection. In the final round, it strategically defects to maximize personal gain, acknowledging the end of reciprocal interactions. This approach balances exploitation with adaptability, ensuring robust performance across various opponent behaviors.
'''

description_EXPLOITATIVE_113 = '''
**Strategy: Exploitative Public Goods Game Strategy**

1. **First Round:** Cooperate by contributing 1 token to encourage initial cooperation and set a positive tone.

2. **Last Round:** Defect by contributing 0 tokens, as there are no future consequences or rounds to consider.

3. **Intermediate Rounds (2 to r-1):**
   - Calculate the number of contributors (m) from the previous round.
   - If the number of contributors (m) exceeds the threshold \( \frac{n}{k} \), Cooperate in the current round.
   - If the number of contributors (m) is less than or equal to \( \frac{n}{k} \), Defect in the current round.

This strategy adapts based on the game's history and parameters, exploiting the Collective Welfare when beneficial and defecting when cooperation is insufficient or when no future repercussions exist.
'''

description_EXPLOITATIVE_114 = '''
**Win-Stay, Lose-Shift Strategy for Public Goods Game**

**Overview:**
This strategy is designed to exploit the behavior of other players in a repeated Public Goods Game while remaining adaptive and robust. The strategy encourages cooperation when beneficial and defects when others are not contributing sufficiently.

**Decision Rules:**
1. **First Round:** Cooperate (C) to initiate a cooperative tone and observe others' reactions.
2. **Subsequent Rounds (Not Last):** 
   - Track the contribution rate (percentage of players who contributed) in the previous round.
   - If the contribution rate is 50% or higher, Cooperate (C). This encourages continued cooperation if others are contributing.
   - If the contribution rate is below 50%, Defect (D) to avoid being exploited.
   - **Forgiveness Mechanism:** If after defecting, others increase their contribution rate above 50%, switch back to Cooperate (C).
3. **Last Round:** Always Defect (D) to maximize immediate payoff, as there are no future interactions.

**Edge Cases Handling:**
- **First Round:** Start with cooperation to test others' behaviors.
- **Last Round:** Defect to ensure maximum payoff since future consequences are absent.

**Robustness and Exploitability:**
- The strategy is adaptive, changing behavior based on others' past actions.
- Forgiveness allows re-engagement with cooperation if others start contributing again.
- It maximizes individual payoff by defecting when contributions are low and exploiting others' cooperation when possible.

This strategy effectively balances cooperation and defection, ensuring individual gain while adapting to group dynamics.
'''

description_EXPLOITATIVE_115 = '''
**Strategy: Adaptive Contribution with Forgiveness (ACF)**

1. **Initial Cooperation**: In the first round, contribute (C) to encourage cooperation and set a positive tone.

2. **Round Observation**: After each round, observe all players' past actions to determine their contribution behavior.

3. **Cooperation Threshold**: Calculate the average contribution rate of all players in the previous round. If the average is above a 50% threshold, contribute (C); otherwise, defect (D).

4. **Forgiveness Mechanism**: If the average contribution drops below the threshold, forgive once by contributing again in the next round. If the average improves, continue contributing; if not, defect thereafter.

5. **Final Round Defection**: In the last round, defect (D) to maximize personal payoff, as future interactions are limited.

This strategy promotes initial cooperation, adapts based on group behavior, and includes a forgiveness component to re-engage with contributors, ensuring robustness against diverse behaviors.
'''

description_EXPLOITATIVE_116 = '''
**Strategy: "Adaptive Threshold Punisher"**

**Overview:**
This strategy is designed to exploit the dynamics of the Public Goods Game by balancing cooperation and defection based on the collective behavior of opponents. It rewards cooperation when it is mutually beneficial and punishes defection to deter free-riding. The strategy is adaptive, using historical information to adjust its behavior, and robust to diverse opponent strategies.

---

**Decision Rules:**

1. **First Round:**
   - Cooperate (C).  
     *Rationale:* Start with cooperation to establish a baseline of trust and encourage reciprocal behavior from others.

2. **Subsequent Rounds:**
   - Let **c_prev** be the proportion of players who contributed (C) in the previous round.  
   - Let **threshold = 0.5** (adjustable based on k and n, but fixed at 0.5 for simplicity).  
     - If **c_prev ≥ threshold**, cooperate (C) in the current round.  
     - If **c_prev < threshold**, defect (D) in the current round.  
   *Rationale:* Reward cooperation when a sufficient number of players are contributing, but defect when contributions are too low to ensure fairness.

3. **Punishment Mechanism:**
   - If **c_prev < threshold** for **2 consecutive rounds**, defect (D) for the next **2 rounds** regardless of the threshold.  
     *Rationale:* Punish consistent under-contribution to deter free-riding and incentivize others to cooperate.

4. **Last Round:**
   - Defect (D).  
     *Rationale:* Since there are no future interactions, maximize personal payoff by defecting.

---

**Edge Cases:**

- **All Players Defect:** If all players defect in the previous round (**c_prev = 0**), defect (D) in the current round.  
- **All Players Cooperate:** If all players cooperate (**c_prev = 1**), cooperate (D) in the current round to maintain high collective payoffs.  
- **Tie or Ambiguity:** If the threshold is exactly met (**c_prev = threshold**), cooperate (C).  

---

**Exploitative Mindset:**
This strategy aligns with an exploitative mindset by:
1. **Rewarding Cooperation:** Cooperating when others contribute sufficiently to maximize joint payoffs.
2. **Punishing Defection:** Defecting when contributions are too low to avoid being exploited.
3. **Adapting to Opponent Behavior:** Using historical actions to inform decisions, ensuring flexibility against diverse strategies.

---

**Pseudocode (for clarity):**
```
def adaptive_threshold_punisher(game_history, current_round, total_rounds, k, n):
    if current_round == 1:
        return "C"
    else:
        c_prev = proportion of players who contributed in previous round
        threshold = 0.5
        if c_prev >= threshold:
            return "C"
        elif c_prev < threshold:
            if all players defected in previous round:
                return "D"
            elif game_history shows 2 consecutive rounds with c_prev < threshold:
                return "D"  # Punishment phase (defect for 2 rounds)
            else:
                return "D"
    if current_round == total_rounds:
        return "D"
```

---

This strategy balances cooperation and punishment, exploiting the game's structure while remaining robust to diverse opponent behaviors.
'''

description_EXPLOITATIVE_117 = '''
To maximize payoff in the repeated Public Goods Game, follow this adaptive strategy:

1. **Initial Cooperation**: In the first round, contribute (C) to encourage others to reciprocate and build cooperation.

2. **Exploitative Cooperation**: After the first round, contribute (C) if the average cooperation rate in the previous round was above 50%. This leverages others' contributions for higher payoffs.

3. **Adaptive Defection**: If others' cooperation falls below 50%, defect (D) in the next round. If they defect again, continue defecting to avoid exploitation.

4. **Last Round Defection**: In the final round, defect (D) to maximize personal payoff without future consequences.

5. **Strategic Probe**: Every 3-5 rounds, defect once to test others' reactions. If cooperation increases afterward, continue using this tactic.

This strategy balances cooperation with strategic defection, ensuring you exploit others' cooperation while minimizing your own exploitation.
'''

description_EXPLOITATIVE_118 = '''
**Strategy Description: Adaptive Exploitation in Repeated Public Goods Game**

*Overview:*
This strategy is designed to exploit opponents' behaviors in a repeated Public Goods Game (PGG), balancing cooperation and defection based on observed actions to maximize individual payoff.

1. **First Round:**
   - **Action:** Contribute (C).
   - **Rationale:** Initiates cooperation, encouraging others to follow suit, while setting a baseline for future adaptations.

2. **Subsequent Rounds (excluding the last round):**
   - **Observation:** Calculate the average contribution of all other players from the previous round.
     - **Contribution:** 1 if C, 0 if D.
   - **Decision Rules:**
     - **Average Contribution > 0.5:** Defect (D). Exploit others' generosity for higher personal gain.
     - **Average Contribution < 0.5:** Defect (D). Protect against exploitation when others are defecting frequently.
     - **Average Contribution = 0.5:** Contribute (C). Sustain cooperation when others are moderately contributing.

3. **Last Round:**
   - **Action:** Defect (D).
   - **Rationale:** No future consequences, so maximize immediate payoff by exploiting any remaining cooperation.

*Robustness and Adaptability:*
- Responsive to diverse behaviors without requiring coordination.
- Handles edge cases, such as varying numbers of players, by focusing on relative contributions.
- Balances exploitation and protection, ensuring strategic adaptability across different opponent behaviors.

This strategy effectively navigates the tension between individual gain and collective welfare, optimizing personal payoff through adaptive, exploitative decisions.
'''

description_EXPLOITATIVE_119 = '''
### Strategy: "Adaptive Exploitation"

1. **Initial Cooperation**: Always cooperate (C) in the first round to encourage contributions from others and maximize initial collective welfare.

2. **Adaptive Adjustment**:
   - After the first round, count the number of contributions (C) in each round from all players except yourself in the previous round.
   - If the number of contributors ≥ n/2, continue cooperating (C) to exploit the cooperative behavior of others.
   - If the number of contributors < n/2, switch to defecting (D) to avoid being exploited by others' defection.

3. **Final Round Defection**: In the last round, always defect (D) to capitalize on the potential cooperation of others in the final round, maximizing your own payoff.

This strategy is exploitative, adaptive, and robust to varying opponent behaviors, ensuring you capitalize on cooperation without being exploited.
'''

description_EXPLOITATIVE_120 = '''
To maximize payoffs in the Public Goods Game, adopt the following adaptive strategy:

### Strategy: Adaptive Exploitation in PGG

1. **Initial Cooperation (First Round):**
   - **Action:** Contribute (C) in the first round. This sets a cooperative tone, encouraging others to reciprocate.

2. **Ongoing Adaptation (Rounds 2 to T-1):**
   - **Assessment:** After each round, calculate the average contribution rate of other players over the last `m` rounds (where `m` is a small, fixed number, e.g., 3).
   - **Threshold Check:**
     - If the average contribution rate is above 50%, continue to Contribute (C). This aligns with the majority behavior, optimizing your payoff when others are cooperative.
     - If the average contribution rate is below 50%, switch to Defect (D). This protects you from being exploited when others are defecting.

3. **Endgame Strategy (Last Round):**
   - **Action:** Always Defect (D) in the final round. Without future interactions, the temptation to defect is high, as there are no repercussions for your action.

This strategy balances cooperation with self-protection, adapting to others' behaviors to exploit their cooperation without being exploited. It is robust, handling initial and endgame scenarios effectively while responding dynamically to the group's behavior.
'''

description_EXPLOITATIVE_121 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

1. **First Round:** Always Cooperate (C). This initiates cooperation, encouraging others to contribute.

2. **Middle Rounds (Rounds 2 to r-1):**
   - Calculate the average contribution from all players in the previous round.
   - If the average is at least 0.5, Cooperate (C) to continue fostering collective contribution.
   - If the average is below 0.5, Defect (D) to avoid being exploited by low contributors.

3. **Last Round:** Defect (D). Since there are no future interactions, maximize personal payoff by withholding contribution.

This strategy is adaptive, responding to others' past actions, and exploitative, maximizing personal gain by only contributing when others sufficiently cooperate. It handles all rounds effectively, ensuring robust performance across various opponent behaviors.
'''

description_EXPLOITATIVE_122 = '''
**Strategy: Cooperative Punisher with Endgame Exploitation**

1. **Initial Cooperation**: In the first round, always Cooperate (C) to set a cooperative tone and encourage reciprocal behavior from others.

2. **Contribution Monitoring**: From the second round onwards, calculate the average contribution rate of all players over the past rounds. This average is the sum of all contributions divided by the number of players.

3. **Reciprocal Cooperation**: If the average contribution rate is above 50%, continue to Cooperate (C). This strategy rewards the group's cooperative behavior and encourages it to continue.

4. **Punishment Mechanism**: If the average contribution rate falls below 50%, switch to Defect (D) for the next round as a form of punishment. This phase aims to penalize non-cooperative behavior and encourage others to increase their contributions.

5. **Adaptive Restart**: After defecting, monitor the group's response. If the average contribution rate returns to or above 50%, revert to Cooperate (C). This adaptability ensures the strategy remains responsive to changing group dynamics.

6. **Endgame Exploitation**: In the last round of the game, switch to Defect (D) to maximize your immediate payoff, knowing that future repercussions are not possible.

This strategy balances initial cooperation with adaptive punishment and strategic exploitation in the endgame, aiming to maximize personal payoff while influencing others' behavior towards cooperation through reciprocation and punishment.
'''

description_EXPLOITATIVE_123 = '''
**Strategy Description for Public Goods Game (PGG)**

1. **First Round**: Cooperate (C) - Contribute 1 token to signal a willingness to cooperate and encourage others to contribute.

2. **Rounds 2 to r-1**:
   - Calculate the average contribution of other players from the previous round.
   - If the average contribution is greater than 50%, contribute (C). Otherwise, defect (D).

3. **Last Round**: Defect (D) - In the final round, withhold contribution to maximize individual payoff, knowing there are no future consequences.

This strategy is designed to be adaptive, balancing cooperation with strategic defection, particularly in the last round, to exploit opportunities for higher individual payoffs while maintaining responsiveness to other players' actions.
'''

description_EXPLOITATIVE_124 = '''
**Strategy: Adaptive Exploitation in Public Goods Game**

**Decision Rules:**
1. **First Round:** Cooperate (Contribute) to encourage initial cooperation and observe others' behavior.
2. **Last Round:** Defect, as future consequences are irrelevant, maximizing immediate payoff.
3. **Subsequent Rounds:** Calculate the average contribution from the previous round. If this average is at least 1/k, contribute; otherwise, defect.

**Rationale:**
- Starting with cooperation encourages others to contribute, potentially increasing collective payoff.
- Defecting in the last round maximizes personal gain since there's no future interaction.
- Using the 1/k threshold ensures contributions only when others' past contributions make it profitable, exploiting their cooperation without unnecessary personal cost.

This strategy balances initial cooperation with adaptive exploitation, ensuring robustness across various opponent behaviors.
'''

description_EXPLOITATIVE_125 = '''
To address the Public Goods Game (PGG) challenge, here's a well-balanced strategy that encourages cooperation while adapting to others' behaviors:

1. **Initial Cooperation**: Start by Cooperating (C) in the first round to establish a cooperative tone and encourage others to follow suit.

2. **Mirror Past Behavior**: In subsequent rounds, observe the majority action from the previous round. If most players Cooperated, you Cooperate. Conversely, if most Defected, you Defect. This reciprocal approach incentivizes collective cooperation.

3. **Forgiveness Mechanism**: To avoid perpetual defection, introduce a forgiveness phase. If the majority Defected recently, occasionally Cooperate again to reset cooperation dynamics and encourage others to re-engage positively.

4. **Last Round Handling**: In the final round, assess the group's historical contributions. Cooperate if the majority have been Cooperative previously, fostering a positive endgame. If past behavior was predominantly Defection, Defect to maximize your final payoff.

This strategy combines initial trust, reciprocal behavior, strategic forgiveness, and adaptive endgame decision-making to balance individual gain with collective welfare.
'''

description_EXPLOITATIVE_126 = '''
To maximize my payoff in the repeated Public Goods Game, I will employ the following exploitative strategy:

1. **First Round:** Cooperate by contributing 1 token. This initial cooperation encourages others to contribute, setting a positive tone.

2. **Subsequent Rounds (excluding the last):** Observe the average contribution of other players from the previous round. If the average is 0.5 or higher, I will Contribute. If it's below 0.5, I will Defect. This ensures I only contribute when others are likely to do so, capitalizing on their cooperation without being exploited.

3. **Last Round:** Always Defect. Since there's no future interaction, I maximize my immediate payoff by withholding my contribution.

This strategy is designed to be adaptive and robust, allowing me to exploit others' cooperative tendencies while avoiding being taken advantage of in the final round.
'''

description_EXPLOITATIVE_127 = '''
The strategy begins cooperatively, aiming to exploit others' willingness to contribute while protecting against exploitation. 

- **First Round:** Cooperate (C) to set a cooperative tone.
- **Middle Rounds (2 to r-1):** Observe the previous round's contributions. If at least half contributed, cooperate again; otherwise, defect.
- **Last Round:** Defect (D) to maximize immediate payoff, assuming others may defect.

This approach rewards cooperation and punishes defection, balancing reciprocity with self-interest.
'''

description_EXPLOITATIVE_128 = '''
**Public Goods Game Strategy: "Adaptive Exploitation"**

1. **Initial Cooperation (First Round):** Begin by cooperating (C). This encourages others to contribute, setting a foundation for mutual benefit.

2. **Imitation of Others (Subsequent Rounds):** In each round after the first, observe the previous round's contributions:
   - If a majority of players (more than half) contributed in the previous round, cooperate (C) to maintain collective benefit.
   - If a majority defected, defect (D) to avoid being exploited.

3. **Exploitation in Final Round:** In the last round, defect (D) to maximize personal gain, as future repercussions are absent.

4. **Edge Cases Handling:**
   - If alone, always defect (D) to keep the token.
   - If group size is 2, adjust the strategy to mirror the opponent's behavior unless they consistently defect.

This strategy balances cooperation with strategic exploitation, adapting based on others' behavior to maximize personal payoff while encouraging collective contribution.
'''
