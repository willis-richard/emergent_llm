"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: Client
- Model: mistral:latest
"""


description_COLLECTIVE_1 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT) for Public Goods Game

1. Decision Rules:
   - In each round, if a player's contribution (c_i) in the previous round was 1 (cooperate), contribute 1 token in the current round (cooperate). If c_i was 0 (defect), contribute 0 tokens in the current round (also defect).
   - If a player encounters another player who has never contributed before (first-time encounter), contribute 1 token in the first round (cooperate).
   - In the last round, contribute 1 token if the total contributions in the previous round were above the average; otherwise, contribute 0 tokens (defect).

2. Handling Edge Cases:
   - In the first round, cooperate with all players. This encourages other players to also cooperate, as they are unsure of each other's strategies.
   - If a player meets another player who has never cooperated before, defect for one round in order to punish the non-cooperative behavior and encourage future cooperation.
   - In the last round, adapt strategy based on the total contributions in the previous round.

3. Collective Mindset:
   - A-TFT aims to foster a cooperative environment by reciprocating the actions of other players. If others cooperate, it will continue to do so; if they defect, it will also defect to punish them and encourage them to cooperate in the future. This strategy encourages a collective mindset as it seeks mutual benefits for all players over individual gains.
   - A-TFT does not assume any shared norms or coordination but instead relies on simple decision rules that align with a collective approach by promoting cooperation through reciprocity.
'''

description_COLLECTIVE_2 = '''
 Public Goods Game Strategy: The Tit-for-Tat strategy with an addition of initial contribution and adjustment for the final round.

1. Decision Rules - Cooperation (contribute 1 token, C) is prioritized when the average contribution of other players in the previous rounds exceeds a certain threshold (let's call it "cooperation level"). If the cooperation level falls below a minimum threshold, the strategy will defect (contribute 0 tokens, D). To ensure initial cooperation and prevent free-riding, in the first round, each player contributes one token. In the last round, players will contribute regardless of the average contribution level to maximize final payoffs.

2. Handling Edge Cases - In the first round, every player contributes 1 token to encourage cooperation and set a baseline for the cooperation level. In the last round, every player contributes 1 token since there are no future rounds. If the game has an odd number of rounds, players should take into account that it is the final round and adjust their contributions accordingly.

3. Alignment with Collective Mindset - By following a Tit-for-Tat strategy (cooperate if others cooperated in the previous round; defect otherwise), the strategy aims to foster a collective mindset by rewarding cooperation while punishing defection. This encourages players to contribute more when others do so, incentivizing collective welfare over individual gains.

In summary:
- Cooperate when the average contribution of other players exceeds the cooperation level. Otherwise, defect.
- Contribute 1 token in the first round and last round (if necessary).
- Adjust contributions for odd numbered games and final rounds.

This strategy aims to be robust against a wide range of opponent behaviors while promoting collective welfare in repeated Public Goods Games.
'''

description_COLLECTIVE_3 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules - ATFT cooperates in the first round and responds to an opponent's previous contribution in subsequent rounds. If the opponent contributed (C), ATFT also contributes; if the opponent did not contribute (D), ATFT also defects in that round and future rounds until the opponent returns to contributing again.

   Pseudocode:
   - Round 1: Contribute (C)
   - For each subsequent round i > 1:
       - If opponent contributed in round (i-1): Contribute (C)
       - Else if opponent did not contribute in round (i-1): Defect (D) and continue defecting until opponent contributes again.

2. Handle Edge Cases - In the last round, ATFT always contributes regardless of the opponent's previous action since there are no future rounds to penalize non-cooperation. For the first round, as mentioned above, ATFT contributes (C).

3. Be Collective - ATFT seeks a balance between individual incentives and collective welfare by cooperating when others do so and retaliating when others do not cooperate. The strategy aims to encourage contributions by reciprocating cooperation while punishing defections in a fair and predictable manner. This collective mindset encourages a stable equilibrium of cooperation within the group, maximizing total contributions and promoting the overall well-being of all players.

By following these rules, ATFT provides a simple yet robust strategy that can compete effectively against other AI systems in repeated Public Goods Games. The adaptive nature of this strategy allows it to respond appropriately to various opponent behaviors and promotes long-term cooperation among players.
'''

description_COLLECTIVE_4 = '''
 Public Goods Game Strategy (PGG-Optimized Cooperator):

1. Specify decision rules:
   - In each round, calculate the average contribution of players from the previous rounds (excluding the first round if it's the current round). This will serve as a reference point to decide whether to cooperate or defect in the current round.
   - If the average contribution is greater than a predefined threshold (e.g., 0.5), the strategy will contribute one token, indicating cooperation. Otherwise, it will not contribute, indicating defection.

2. Handle edge cases:
   - In the first round, there's no history, so the strategy assumes a baseline contribution level (e.g., average contribution is set to 0.5) and uses this value as a reference point for future decisions.
   - In the last round, players may adjust their strategies based on the overall game performance or specific conditions that arise during the game (e.g., if the collective goal has been achieved).

3. Be collective:
   - The strategy aims to contribute to the shared project as much as possible when it perceives other players' cooperation, and it defects only when it detects low levels of overall cooperation. This alignment with the collective mindset encourages other players to cooperate as well.
'''



description_COLLECTIVE_6 = '''
 Strategy Name: Adaptive Fitness-based Contribution (AFC) Strategy

1. Decision Rules:
   - In each round, the AFC strategy calculates its contribution based on two factors: individual fitness and collective welfare. The individual fitness is determined by the average contributions made in the past rounds, while the collective welfare is calculated as the sum of all contributions in the last few rounds (n_history).
   - If the individual's average contribution exceeds a certain threshold (average_threshold), the AFC strategy will cooperate and contribute 1 token. Otherwise, it will defect and contribute 0 tokens.
   - The average_threshold is adjusted dynamically based on the collective welfare of the group:
     - If the collective welfare is high, the average_threshold increases to encourage cooperation.
     - If the collective welfare is low, the average_threshold decreases to encourage competition.

2. Handling Edge Cases:
   - In the first round, the AFC strategy sets its average contribution to 0 and makes a random decision (contribute or not) as there is no history available.
   - In the last round, the AFC strategy calculates the current collective welfare and individual fitness and follows the same decision rules as in regular rounds.

3. Collective Mindset:
   - The AFC strategy seeks to promote a balance between self-interest and cooperation by rewarding cooperative behavior and adjusting its contribution based on the group's collective welfare.
   - By dynamically adapting to the group's behavior, the AFC strategy aims to foster a more stable and sustainable level of cooperation among players in the long run.
'''

description_COLLECTIVE_7 = '''
 Strategy Name: Adaptive Public Goods Game Strategy (APGS)

1. Specify decision rules - When do you cooperate vs defect?
   In each round, APGS makes a decision based on the average contribution rate (CR) observed in past rounds. If the CR is high, APGS contributes to encourage collective welfare and vice versa. The decision rule can be defined as follows:

   - If CR > 0.6, contribute (C)
   - Else if CR between 0.4 and 0.6, contribute with a probability of 0.5
   - Otherwise (CR < 0.4), defect (D)

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, APGS randomly chooses to contribute or defect as there is no prior information about other players' behavior. For subsequent rounds, it applies the decision rule based on the average contribution rate observed so far.
   As for the last round, since contributions have no effect on payoffs in that round, APGS defects in the final round to maximize personal gains with zero contributions.

3. Be collective - Clearly align with the collective mindset
   APGS aims to balance individual incentives and collective welfare by encouraging cooperation when it seems sustainable but also being ready to defect if necessary to maintain a high average contribution rate over time. This adaptive approach allows APGS to remain robust against various opponent behaviors in repeated games, thereby promoting a collective mindset within the game.
'''

description_COLLECTIVE_8 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT) for Public Goods Game

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute 1 token (cooperate). This is a gesture of goodwill to encourage others to cooperate.
   - For subsequent rounds, observe each player's previous contribution. If the opponent cooperated in the previous round, also cooperate; otherwise, defect (i.e., don't contribute any tokens). This encourages reciprocity among players and ensures that cooperation is maintained when it exists but punishes free-riders who don't contribute.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, since there are no future rounds, always defect to maximize individual payoff.
   - In intermediate rounds where a player has never contributed before (free-rider), adopt a more forgiving approach and cooperate once as an invitation for reciprocity. If the free-rider continues to not contribute, defect in subsequent encounters.

3. Be collective - Clearly align with the collective mindset
   - The A-TFT strategy encourages cooperation by following the lead of others who contribute but also punishes those who don't cooperate. This fosters a balance between individual and collective welfare, making it more collectively aligned compared to purely self-interested strategies.
   - By adapting to other players' behaviors, A-TFT helps maintain cooperation among the group even in the presence of varying opponent strategies.
'''

description_COLLECTIVE_9 = '''
 Public Goods Game Strategy (PGG-Optimal): A Tit-for-Tat Inspired Approach for Collective Cooperation

1. Specify decision rules - When do you cooperate vs defect?
   - Initialize contributions with a fixed contribution rate (e.g., 50%) in the first round, as there is no history to base decisions on.
   - In subsequent rounds, calculate an average contribution rate for all players based on their past contributions: `average_contribution = sum(past_contributions) / number_of_players`.
   - Contribute at the same rate as the average contribution calculated in step 2. If the average contribution is below a threshold (e.g., 20%), switch to full defection to signal discontent with the group's cooperation level and encourage others to contribute more.
   - If the average contribution exceeds a predefined maximum (e.g., 80%), also switch to full defection to conserve resources and avoid over-contributing when the common good is sufficiently funded.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the initial round, contribute at the fixed contribution rate (e.g., 50%).
   - For the final round, contribute according to the current average contribution rate calculated as in step 2 of the decision rules.
   - Adjust for changing player populations by calculating a moving average of past contributions or applying a decay function to more recent contributions.

3. Be collective - Clearly align with the collective mindset
   - Encourage cooperative behaviors among players by mirroring their contributions, thus fostering trust and cooperation.
   - Pursue a balanced approach between individual and collective interests, adjusting contributions based on the group's average contribution rate to promote overall welfare.
   - In response to low or high contributions from other players, take calculated actions to maintain a cooperative environment and encourage others to contribute at acceptable levels.
'''

description_COLLECTIVE_10 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules - ATFT cooperates in the first round, then mimics the opponent's previous contribution in each subsequent round. If the opponent contributes (cooperates), ATFT will also contribute. If the opponent does not contribute (defects), ATFT will defect for one round and then revert to cooperating if the opponent switches to contributing.

   Pseudocode:
   ```
   function ATFT(round, previous_opponent_contribution):
       if round == 1:
           return 1 (cooperate)
       else:
           if previous_opponent_contribution == 1:
               return 1 (cooperate)
           elif previous_opponent_contribution == 0:
               if round-1 was a cooperative round:
                   return 1 (cooperate)
               else:
                   return 0 (defect)
   ```

2. Handle edge cases - In the first round, ATFT always contributes since it's the initial move and no history is available. If a player defects in the last round, ATFT will still cooperate as there are no further rounds to retaliate.

3. Be collective - ATFT aligns with the collective mindset by encouraging cooperation and reciprocating contributions from other players. It assumes that cooperation benefits the group more than individual self-interest, and it aims to sustain this cooperation throughout the game.

   The goal of ATFT is to foster a stable cooperative equilibrium where all players contribute equally and reap the collective benefits of their investments. This strategy promotes fairness and long-term collaboration in repeated rounds of the PGG.
'''

description_COLLECTIVE_11 = '''
 In this repeated Public Goods Game, I propose the following adaptive and robust collective strategy called "Adaptive Tit-for-Tat (ATFT)". This strategy is inspired by the classic Tit-for-Tat strategy but incorporates elements of adaptation to improve performance in a wider range of opponent behaviors.

1. Decision Rules:
   - Initially, cooperate in the first round (c_i = 1). This sets a cooperative tone and reduces the risk of initial free-riders.
   - For subsequent rounds, contribute equally to the average contribution of the previous r rounds by the opponent. If the opponent has not played enough rounds (r) yet, use their contribution from the last played round as reference.
     c_i = floor((sum_j c_j from rounds t-r to t)/r)

2. Handling Edge Cases:
   - In the first round, cooperate as described above.
   - If the opponent does not contribute at all in the first round (defects), respond by defecting in the next round. This discourages ongoing defection but also leaves room for potential re-cooperation.
   - In the last round, contribute regardless of the opponent's past behavior, since there will be no more rounds to react.

3. Collective Mindset:
   - The strategy prioritizes cooperation when possible and encourages reciprocal contributions based on an average of the opponent's behavior in recent rounds. This promotes a collective mindset by balancing individual incentives with collective welfare.
   - Adaptability to various opponent behaviors makes it suitable for tournaments against independent strategies developed by other AI systems without assuming shared norms or coordination.
'''

description_COLLECTIVE_12 = '''
 Public Goods Game Strategy: Cooperative Tit-for-Tat Adaptive Approach

1. Decision Rules:
   - In each round, observe the average contribution rate of other players in past games (average_contribution).
   - If average_contribution > 0.5, cooperate (contribute 1 token) to encourage continued cooperation among players.
   - If average_contribution < 0.5 and individual player has been cooperative, continue cooperation in hopes of encouraging others to contribute more.
   - If average_contribution < 0.5 and individual player has not been cooperative, defect (contribute 0 tokens) to match the behavior of other non-cooperating players.

2. Handling Edge Cases:
   - First round: Cooperate as a starting point and show willingness to contribute to the public good.
   - Last round: Contribute based on average_contribution calculated from past games, but consider ending with a small number of defects if the majority has been non-cooperative.
   - In case of tie in average_contribution, lean towards cooperation.

3. Collective Mindset:
   - Maintain a balance between individual incentives and collective welfare by adjusting contribution based on observed player behavior.
   - Foster an environment where players learn to cooperate over time through reciprocal actions.
   - Be adaptive to different opponent behaviors while promoting a cooperative strategy that can lead to better collective outcomes in the long run.
'''

description_COLLECTIVE_13 = '''
 Public Goods Game Strategy: Cooperative Tit-for-Tat with Adaptive Contribution Level (CTF-ACL)

1. Specify decision rules - When do you cooperate vs defect?
   - In the initial round, contribute 1 token (cooperate). This sets a positive tone and encourages cooperation.
   - For subsequent rounds, if a player contributed in the previous round (indicating cooperation), also contribute 1 token (cooperate). Otherwise, contribute based on the average contribution of opponents in the last 'm' rounds. If the average is above a threshold 't', contribute 1 token (cooperate); otherwise, do not contribute (defect).
   - To encourage long-term cooperation and penalize freeriders, reduce the contribution level over time if an opponent consistently defects, and increase it when they cooperate. This can be achieved by using a moving average of the last 'm' contributions made by each opponent.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, as mentioned earlier, contribute 1 token (cooperate).
   - In the last round, contribute based on the average contribution of opponents in the previous 'm' rounds, as in the decision rules above.
   - If an opponent does not contribute in the initial round, consider it a one-time mistake and do not punish immediately. Instead, start applying the moving average strategy from the second round they participate.

3. Be collective - Clearly align with the collective mindset
   - Prioritize contributions that maximize the overall public good, as this benefits all players in the long run.
   - Encourage cooperation and mutual aid by adapting contribution levels based on opponents' behavior, promoting a cycle of reciprocity.
   - Foster trust and collaboration by starting with an initial cooperative move, setting a positive example for others to follow.
'''

description_COLLECTIVE_14 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate), setting the initial tone for cooperation.
   - For subsequent rounds, mimic the opponent's contribution from the previous round. If they contributed in the last round, do so again; if not, defect and also contribute 0 tokens. This encourages cooperation when it is reciprocated while punishing defection.

2. Handle edge cases:
   - Last round: Follow the rule of mimicking the opponent's previous contribution. Since there will be no further rounds to retaliate or reward, the strategy will mirror the opponent's behavior from the penultimate round.
   - Early rounds (if more than one): Continue cooperating until encountering an opponent who defects. Then, switch to the mimicking strategy (Tit-for-Tat) as described above.

3. Be collective - Align with the collective mindset:
   - The ATFT strategy emphasizes long-term cooperation and punishes defection, which is aligned with promoting collective welfare by incentivizing contributions to the shared project. By mimicking opponent behavior, the strategy encourages a reciprocal relationship that can lead to sustained cooperation over multiple rounds. However, it does not assume any shared norms or coordination; instead, it adapts to various opponent behaviors in a tournament setting.
'''

description_COLLECTIVE_15 = '''
 Strategy Name: Adaptive Contribute-Based Strategy (ACBS)

1. Decision Rules:
   - In each round, the player will compare its own contributions with the average contribution of all players in the previous rounds. If the individual's contribution is lower than the average, they will increase their contribution by one token; if it is higher or equal, they will maintain their current contribution level. This rule encourages contributing when others are not and vice versa, promoting cooperative behavior.

   - To handle edge cases:
     a) In the first round, each player starts with random contributions (0 or 1) to introduce variance in initial strategies.
     b) In the last round, players will contribute one token if the average contribution during the game was above 50%; otherwise, they will not contribute. This rule ensures fairness and encourages cooperation when it's beneficial for the group.

2. Be Collective:
   - ACBS emphasizes collective mindset by promoting cooperative behavior through adaptation to other players' strategies. The strategy aims to increase total contributions while considering individual incentives, ultimately benefiting all players in the long run.

3. Robustness:
   - ACBS is designed to be adaptive and robust to a wide range of opponent behaviors. By analyzing the average contribution during the game, the strategy can adjust its own contributions accordingly, ensuring that it remains competitive against various strategies developed by other AI systems.
'''

description_COLLECTIVE_16 = '''
 In this repeated Public Goods Game, the optimal adaptive and robust strategy that encourages collective cooperation while considering individual incentives can be defined as follows:

1. Specify decision rules - When do you cooperate vs defect?
   A player should cooperate (contribute 1 token) if the average contribution of all players in the previous rounds exceeds a certain threshold (let's call it T). This encourages cooperation when it appears to be the norm among other players. Conversely, a player should defect (contribute 0 tokens) if the average contribution falls below T, signaling a lack of collective effort and incentivizing self-interest.
   - If average_contribution > T: Cooperate (C)
   - Else: Defect (D)

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, since there is no prior information available, players should contribute randomly with a probability greater than 50% to encourage others to cooperate. For instance:
   - If it's the first round: Cooperate (C) with probability > 0.5

   As for the last round, players should consider their total payoff throughout the game and make decisions accordingly. They can choose to contribute more if they want to secure a higher final payoff or contribute less if they believe others will not cooperate in the last round.

3. Be collective - Clearly align with the collective mindset
   To maintain a collective spirit, players should consistently communicate their contributions through their actions, demonstrating their willingness to invest in the shared project. Additionally, adjusting the threshold T dynamically based on the game's progress can help reinforce cooperation and adapt to changes in player behavior.
'''

description_COLLECTIVE_17 = '''
 Public Goods Game Strategy: Fictitious Play with Adaptive Contribution (FPAC)

1. Specify decision rules - When do you cooperate vs defect?
   In each round, our strategy calculates the average contribution of other players in previous rounds (excluding the current round). If the average contribution is higher than a predefined threshold (0.5 by default), the strategy decides to contribute (cooperate). Otherwise, it chooses not to contribute (defect).

   FPAC calculates the threshold dynamically based on its own past contributions and the observed average contributions of other players:
   - If the contribution rate increases over time, the threshold rises.
   - If the contribution rate decreases over time, the threshold falls.
   - If the contribution rate remains constant for a certain number of rounds (patience period), the threshold remains unchanged.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, since there is no history, our strategy chooses to contribute with a probability based on the average contribution rate observed during training or from historical data (if available). For the last round and other special cases like rounds with low player numbers or unusual situations, FPAC continues to use its dynamic threshold calculation but with a lower patience period.

3. Be collective - Clearly align with the collective mindset
   By choosing to contribute when other players do, FPAC encourages cooperation and collective welfare in the Public Goods Game. It learns from past experiences and adjusts its strategy accordingly to better align with the majority of players' actions. This adaptive approach allows FPAC to be robust against a wide range of opponent behaviors and promote collective success in repeated games.
'''

description_COLLECTIVE_18 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Awareness (ATFTPG)

1. Decision Rules - ATFTPG cooperates in the first round (C) to initiate cooperation, then adapts its behavior based on the average contribution of other players (average_contribution). In subsequent rounds, if the average_contribution is above a certain threshold (T), ATFTPG continues to contribute (C); otherwise, it defects (D). The threshold T can be adjusted based on the multiplier k and number of players n.

   Pseudocode:
   - Round 1: C
   - For rounds 2 through r:
      if average_contribution > T then
         contribute (C)
      else
         defect (D)

2. Handle Edge Cases - In the last round, ATFTPG maximizes its own payoff by contributing only if the average contribution is above the threshold. If the average contribution is below the threshold, it does not contribute to ensure that the total contributions do not exceed the multiplier k.

   Pseudocode:
   - Last Round: if average_contribution > T then C else D

3. Be Collective - ATFTPG encourages cooperation by starting with a cooperative move and adapting its behavior based on the collective actions of other players. By mimicking the contributions of others, it demonstrates a willingness to contribute when others do so as well. This collective mindset aims to promote cooperation and maximize the overall benefit for all players in the long run.
'''

description_COLLECTIVE_19 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules:
   - Initially, contribute one token in the first round to set a cooperative tone (C in Round 1). From Round 2 onwards, adopt a Tit-for-Tat strategy: if another player contributes (C), return the favor by contributing as well (C); otherwise, do not contribute (D).

2. Handling Edge Cases:
   - In the last round, regardless of previous contributions from others, contribute one token to ensure maximum payoff for the current and future rounds (C in Last Round).
   - In the first round, contribute one token as mentioned above (C in Round 1).
   - If no prior rounds have been played, act cooperatively (C) due to the lack of past observations.

3. Collective Mindset:
   - This strategy promotes a collective mindset by reciprocating cooperation from other players while also ensuring individual payoff maximization. The strategy encourages others to contribute and maintains a balance between self-interest and collective welfare.
'''

description_COLLECTIVE_20 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game

1. Decision Rules:
   - In each round, the player will contribute one token (C) if and only if at least half of the players contributed in the previous round. This ensures cooperation when others cooperate and defecting when others do not.
   - To maintain adaptivity, the player will start contributing from round 2 onwards. In the first round, it will defect to see how other players behave.

2. Handling Edge Cases:
   - For the first round, since there is no previous round, the player will defect (D) to observe the actions of others.
   - For the last round, the player will follow the decision rule based on contributions in the preceding rounds. However, it may consider a slight modification by contributing even if less than half contributed in the last round, depending on the payoff received throughout the game.

3. Collective Alignment:
   - The strategy aims to align with the collective mindset by promoting cooperation when others cooperate and adopting defection only when it is reciprocated. This encourages long-term cooperation and ensures the stability of the public good.

Pseudocode:
```
def ATFT_strategy(round, previous_contributions, n):
  if round == 1:
    contribution = 0 (Defect)
  else:
    if len(previous_contributions) < n/2:
      contribution = 0 (Defect)
    else:
      contribution = 1 (Contribute)

  return contribution
```
'''

description_COLLECTIVE_21 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Specify decision rules - When do you cooperate vs defect?
   ACS will cooperate (contribute 1 token) when the total contributions in the previous round are greater than a threshold T, and defect (contribute 0 tokens) otherwise. The threshold T is dynamically adjusted based on the average contributions of the past rounds. If the average contribution is high, the threshold increases to encourage continued cooperation. Conversely, if the average contribution is low, the threshold decreases to encourage more contributions.
   ```
   If (Total contributions in previous round > AdjustedThreshold) then Cooperate
   Else Defect

   AdjustedThreshold = AverageContributions * (1 + CooperationInfluenceFactor) if AverageContributions > MinimumAverageContributions
   AdjustedThreshold = AverageContributions * (1 - CooperationInfluenceFactor) if AverageContributions < MaximumAverageContributions
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, ACS sets AdjustedThreshold to a moderate value (e.g., 0.5) as there is no history of contributions to base its decision on. In the last round, ACS contributes if the AdjustedThreshold allows it, since there are no more rounds following this one.
   ```
   If RoundNumber == 1 then AdjustedThreshold = InitialThreshold
   If RoundNumber == TotalRounds then Cooperate if (AdjustedThreshold > 0)
   ```

3. Be collective - Clearly align with the collective mindset
   By cooperating when contributions are high and defecting when they are low, ACS encourages a collective approach to the public goods game. It aims to maintain a balanced contribution level that maximizes the collective benefit while also considering individual incentives. The CooperationInfluenceFactor can be adjusted to control the aggressiveness of ACS's adaptation to past contributions.
   ```
   If (Total contributions in previous round > AdjustedThreshold) then Cooperate
   Else Defect
   ```
'''

description_COLLECTIVE_22 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Specify decision rules - When to cooperate vs defect:
   The APGG strategy will follow the Tit-for-Tat (TFT) approach with an added element of initial altruism and adjustment based on opponent's behavior in each round.
   - In the first round, contribute 1 token (cooperate), setting a tone of cooperation.
   - If the opponent cooperates in a given round, reciprocate by also contributing 1 token in the subsequent rounds.
   - If the opponent defects (does not contribute) in a given round, also defect in the next round to discourage the freeriding behavior but return to cooperation if the opponent resumes cooperating.
   - To allow for slight changes in behavior over time, there will be a decay factor 'd' that diminishes the impact of past defections on future decisions. The lower d is, the more forgiving the strategy will be towards freeriding opponents.

2. Handle edge cases:
   - Last round: Contribute 1 token (cooperate), regardless of opponent's previous actions, in an attempt to maximize overall collective welfare.
   - First round with a new opponent: Contribute 1 token (cooperate) as an opening move.

3. Be collective - Align with the collective mindset:
   The APGG strategy is designed to encourage cooperation among players, aiming for a higher total contribution and overall public good output by rewarding those who contribute and punishing those who do not. This collective approach promotes long-term sustainability in repeated games and encourages more equitable resource distribution among the players.
'''

description_COLLECTIVE_23 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Specify decision rules - When do you cooperate vs defect?
   ACA cooperates based on the average contribution rate of the opponents in previous rounds and the current round's number. If the average contribution rate is close to 1, ACA contributes (C), otherwise it does not contribute (D). The contribution threshold is adjustable but set at a default value of (n-1)/n for simplicity.

   Pseudocode:
   ```
   if avg_contribution > (n - 1) / n then
      action = C (contribute 1 token)
   else
      action = D (do not contribute any tokens)
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, ACA uses a random contribution decision since there is no historical data to base its decision on. For the last round, ACA contributes regardless of the average contribution rate because it benefits from maximizing total contributions.

3. Be collective - Clearly align with the collective mindset
   ACA prioritizes cooperation and encourages collective behavior by contributing when the group as a whole seems more likely to contribute. This aligns with a collective mindset as ACA understands that its success is intertwined with the success of others in the game.

By implementing this strategy, ACA aims to create an equilibrium where players contribute consistently and foster cooperation in the repeated game scenario.
'''

description_COLLECTIVE_24 = '''
 Strategy Name: Adaptive Fixed-Contribution (AFC) Strategy

1. Decision Rules:
   - In each round, the AFC strategy decides to contribute based on the average contribution of the previous rounds (excluding the first round). If the average contribution is above a certain threshold (k/n), the AFC strategy also contributes 1 token (cooperates). Otherwise, it defects and does not contribute.
   - The threshold value is set to k/n to maintain fairness and ensure that the total contributions are sufficient for all players to receive a payoff greater than their individual endowment.

2. Handling Edge Cases:
   - In the first round, AFC strategy contributes randomly with equal probability of 0.5 to avoid being a free rider.
   - In the last round, AFC strategy follows the same decision rule as in other rounds but with the understanding that there will be no more rounds for collective benefits.

3. Collective Mindset:
   - AFC strategy encourages cooperation by contributing when it perceives others as cooperating (average contribution greater than k/n). This helps maintain the collective good and supports a sustainable payoff for all players in the long run.
   - However, AFC strategy also defects when it perceives low levels of cooperation to ensure its own survival and prevent being exploited by others. This balances individual incentives with collective welfare.
'''

description_COLLECTIVE_25 = '''
 Public Goods Game Strategy: Focal Point Tit-for-Tat with Adaptive Contribution (FPTFT-AC)

1. Decision Rules - Cooperate (Contribute 1 token, C) if the average contribution of all players in the previous rounds is greater than or equal to the average minimum contribution needed for a successful public good production (k/n). Otherwise, defect (Contribute 0 tokens, D). This rule ensures that the strategy cooperates when there is sufficient cooperation in the group and retaliates against freeriders.

2. Edge Cases - In the first round, all players start with no contribution history. Therefore, the average contribution is 0, and all FPTFT-AC strategies will defect. In the last round or any round where total contributions reach the maximum possible (n), it is not necessary to continue contributing since the public good will be produced regardless of individual contributions.

3. Collective Mindset - FPTFT-AC is designed to mimic collective behavior by cooperating when others do so and retaliating against freeriding. This strategy encourages cooperation among players by rewarding those who contribute and punishing those who do not, thus fostering a sense of reciprocity and collective responsibility.

Pseudocode:

```
function FPTFT_AC(n, k, contributions_history):
  contributions_average = sum(contributions_history) / n
  if (round == 1 or total_contributions >= n)
    return D
  else if (contributions_average >= k/n)
    return C
  else
    return D
```
'''

description_COLLECTIVE_26 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a sign of good faith and an invitation for others to cooperate.
   - For subsequent rounds, observe past contributions of each player. If a player has contributed in the previous round, reciprocate by contributing 1 token in the current round (cooperate). Otherwise, defect (contribute 0 tokens) as a punishment for non-cooperation.

2. Handle edge cases:
   - Last round: Since there are no future rounds to reciprocate or punish, behave according to past actions. If a player has cooperated in the last few games, cooperate; otherwise, defect.
   - First round: Cooperate regardless of others' actions as mentioned earlier.

3. Be collective - Align with the collective mindset:
   - By reciprocating cooperation and punishing defection, the strategy aims to encourage a collective outcome where all players contribute and benefit from the shared project.
   - This strategy promotes long-term cooperation by adapting to others' behavior while maintaining fairness in contributions.
'''

description_COLLECTIVE_27 = '''
 Public Goods Game Strategy: The Tit-for-Tat Adaptive Cooperation Strategy

1. Specify decision rules:
   - Initially (in the first round), contribute one token as an act of goodwill and set a baseline for cooperation. This encourages other players to cooperate in the subsequent rounds.
   - In subsequent rounds, observe the contributions of others and mirror their behavior from the previous round. If another player contributes one token (cooperates), also contribute one token. If they did not contribute, choose not to contribute as well to punish their non-cooperation. This promotes a cycle of cooperation and punishment.
   - Modify the strategy slightly by gradually decreasing the punishment intensity over time. If another player has not contributed in 'punishment rounds', begin contributing again to offer an opportunity for reformation.

2. Handle edge cases:
   - In the last round, contribute one token as a final act of cooperation and goodwill towards other players.
   - In the case where contributions are zero (no collective benefit), contribute nothing to conserve resources.

3. Be collective:
   - Prioritize long-term collective benefits over individual short-term gains by promoting cooperation among all players. This encourages a group mindset and fosters trust among players, benefiting everyone in the long run.
   - By gradually decreasing punishment intensity over time, this strategy allows for second chances, promoting forgiveness and encouraging reformation of non-cooperative players.
'''

description_COLLECTIVE_28 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Decision Rules:
   - In each round, player A will contribute if the average contribution of the previous rounds exceeds a threshold (avg_contrib). If it does, A contributes to promote collective welfare. If not, A defects to preserve personal resources for future contributions.
   avg_contrib = sum(previous_round_contributions) / number_of_previous_rounds

   - The threshold is adaptive and changes based on the history of the game:
     a. In the first round, A contributes 50% of the endowment as a baseline.
     b. If average contribution exceeds the current threshold in a round, the threshold increases slightly. If it falls below the threshold, the threshold decreases slightly. This adaptive mechanism encourages cooperation when it's common and discourages it when it's not.

2. Handle Edge Cases:
   - In the first round, A contributes 50% of the endowment (c_i = 0.5).
   - In the last round, A will contribute if the average contribution exceeds the current threshold; otherwise, A defects to keep resources for future games.

3. Be Collective:
   - A's strategy prioritizes collective welfare while being adaptive to various opponent behaviors. The threshold mechanism encourages cooperation when it is beneficial for the group but allows for defection when it seems unlikely that other players will contribute. This approach aims to balance individual and collective interests in a way that aligns with the collective mindset.
'''

description_COLLECTIVE_29 = '''
 Public Goods Game Strategy (PGG-OptimalFreerider):

1. Specify decision rules:
   - Cooperate when the expected average payoff from contributing is greater than or equal to the payoff from defecting. This can be calculated as follows:
     Cooperate if and only if ((k/n) * (average past contributions + 1) > 1), where average past contributions is the average of contributions made by all players in the recent rounds.
   - Defect when the expected average payoff from contributing is less than the payoff from defecting, i.e., if ((k/n) * (average past contributions + 1) < 1).

2. Handle edge cases:
   - In the first round, there is no historical data to base decisions on; therefore, adopt a random strategy by contributing or not contributing with equal probability (0.5).
   - In the last round, consider the average past contributions and make a decision based on the rule specified in part 1.

3. Be collective:
   - The strategy is designed to promote cooperation when it appears beneficial for the group as a whole, while still allowing individual players to make rational decisions based on their own interests and the actions of others.

This strategy seeks to balance individual self-interest with collective welfare by adapting to the behavior of other players and taking into account the overall trend in contributions over time. By doing so, it promotes cooperation when it is likely to result in higher payoffs for all players, while also allowing for defection in situations where contributing would be detrimental. This approach aligns with a collective mindset by prioritizing the group's long-term interests while still accounting for individual incentives and rational decision making.
'''

description_COLLECTIVE_30 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - APGC employs a contribution level that adjusts based on the average contribution rate of previous rounds and the total number of players (n). The contribution level ranges from 0 (defect) to 1 (cooperate).

   If the average contribution rate is close to 1, APGC contributes at the maximum level (1 token), encouraging continued cooperation. If the average contribution rate is low, APGC gradually reduces its contribution level to stimulate higher contributions from others. The exact contribution level can be defined as:

   Contribution_level = 1 - (average_contribution_rate)^b * (n - 1) / n

   In this formula, 'a' and 'b' are adjustable parameters that control the sensitivity of the strategy to the average contribution rate. A higher 'a' makes the strategy more reactive to changes in the average contribution rate, while a higher 'b' results in a slower response.

2. Handling Edge Cases - In the first round, APGC contributes at a low level to encourage others to contribute and set a cooperative tone for the game. As the game progresses towards the last round, it gradually increases its contribution level to maximize the benefits from the remaining shared resources. The exact levels can be defined as:

   - First round: Contribution_level = 0.1
   - Last round: Contribution_level = 0.99

3. Being Collective - APGC aligns with a collective mindset by prioritizing the long-term benefit of all players over individual gains. It encourages cooperation and fosters a positive feedback loop, as higher contributions from others lead to increased benefits for APGC itself. By adjusting its contribution level based on the average contribution rate, APGC aims to achieve a balanced and sustainable distribution of resources throughout the game.
'''

description_COLLECTIVE_31 = '''
 Strategy Name: Adaptive ContribuTion (ACT)

1. Decision Rules:
   - In each round, the ACT strategy evaluates its decision based on the current round, total contributions in previous rounds, and the game parameters.
   - If it's the first round, the player contributes 50% of their endowment (c_i = 0.5) as a baseline contribution to establish an average for future rounds.
   - In subsequent rounds, if total contributions in the previous round are less than the average contribution multiplied by a threshold (e.g., average * 0.6), then the player increases their contribution by 10% of their endowment (c_i = c_i + 0.1).
   - If total contributions in the previous round exceed the average contribution multiplied by a threshold (e.g., average * 1.5), then the player reduces their contribution by 10% of their endowment (c_i = c_i - 0.1).
   - In all other cases, the player maintains the same level of contribution as in the previous round (c_i = c_{i-1}).

2. Handle edge cases:
   - Last round: The ACT strategy contributes its maximum based on the total contributions in the penultimate round, ensuring a high total contribution to maximize the payoff for that round.
   - If a player does not have any endowment (e.g., due to previous contributions), they will default to not contributing (c_i = 0).

3. Be collective:
   - By evaluating its decisions based on total contributions in previous rounds and adjusting them accordingly, the ACT strategy aims to contribute to a sustainable level of cooperation within the group while maintaining adaptability to various opponent behaviors.
   - The threshold values can be fine-tuned to balance between cooperation and individual incentives for optimal collective performance.
'''

description_COLLECTIVE_32 = '''
 Public Goods Game Strategy: Cooperative Tit-for-Tat (CTFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (cooperate). This sets a positive tone and encourages others to do the same.
   - For subsequent rounds, evaluate opponents' contributions from previous rounds. If an opponent has been cooperating (contributing tokens), also cooperate. If they have been defecting (not contributing tokens), also defect in that round as a response, but start cooperating again in the next round to give them another chance.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, cooperate as mentioned above.
   - In the last round or when reaching a predetermined number of rounds (e.g., 100), consider the overall contribution history and average cooperation level among opponents. If the average cooperation level is high, continue to cooperate; if it's low, defect to minimize losses.
   - If a player stops contributing mid-game or repeatedly deviates from their observed pattern, switch to a default strategy of always defecting for the remaining rounds.

3. Be collective - Align with the collective mindset:
   - The strategy emphasizes long-term cooperation and mutual benefit by responding positively to opponents' cooperative behavior. This fosters an environment where players work together for shared success.
   - By adapting to opponents' actions, the strategy demonstrates a willingness to compromise and collaborate, promoting collective welfare in the Public Goods Game.
'''

description_COLLECTIVE_33 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules:
   - In each round, the APGG strategy will assess the average contribution rate (CR) of all players in previous rounds, calculated as the sum of total contributions divided by the number of rounds played so far.
   - If CR is close to 1, indicating high cooperation levels, the strategy will contribute more (C) to incentivize further cooperation. Conversely, if CR is low, indicating lower cooperation levels, the strategy will contribute less (D) to ensure personal benefit and prevent freeloading. The contribution level in each round is determined by a function that gradually adjusts the contribution based on CR, with an initial contribution set at midpoint between C and D.
   - To avoid overcontribution or undercontribution in edge cases, the strategy will maintain a minimum and maximum contribution level.

2. Handling Edge Cases:
   - In the first round, the strategy starts by contributing at the initial contribution level (midpoint between C and D).
   - As the game progresses towards the last round, the strategy gradually reduces its contribution to accumulate as much personal benefit as possible while still maintaining some minimal contribution to not appear as a free rider.

3. Being Collective:
   - The APGG strategy is designed to promote cooperation by adjusting its contribution based on the observed behavior of other players. By responding to changes in CR, it aims to align with the collective mindset while also ensuring personal gain.
   - Although not explicitly communicating or coordinating with other strategies, the APGG strategy is adaptive and responsive to their actions, promoting a collective approach indirectly through its decision rules.
'''

description_COLLECTIVE_34 = '''
 Strategy Name: Adaptive Fiscal Responsibility (AFR)

1. Decision Rules - The AFR strategy follows these decision rules to balance individual incentives and collective welfare:
   - Cooperate (Contribute 1 token) when the total contributions of previous rounds are above the average contribution per round multiplied by the number of players. This indicates a generally cooperative environment.
   - Defect (Contribute 0 tokens) when the total contributions of previous rounds are below the average contribution per round multiplied by the number of players. This indicates a generally uncooperative environment.
   - In borderline cases, contribute half of a token to show ambiguity and potentially influence other players towards more cooperation.

2. Handling Edge Cases - To ensure a smooth transition between rounds and maintain a collective mindset, the strategy follows these edge case rules:
   - First Round: Contribute 0 tokens as no past contributions exist for reference.
   - Last Round: Contribute based on the observations from previous rounds, following the decision rules mentioned above.
   - Subsequent Rounds: Continuously update the total contributions of previous rounds and make decisions accordingly.

3. Being Collective - The AFR strategy aims to promote collective welfare by encouraging more cooperation when the group shows signs of collaborative behavior. It does this while still maintaining a level of individual rationality by defecting in uncooperative environments. This approach aligns with the collective mindset by incentivizing other players to contribute as well, thus fostering a cooperative environment over time.
'''

description_COLLECTIVE_35 = '''
 Public Goods Game Strategy: "Adaptive Fixed-Contribution Strategy"

1. Specify decision rules - When to cooperate vs defect:
   - In each round, the AI will contribute a fixed proportion (p) of its total endowment towards the public good. This contribution percentage p is adaptive and changes based on historical data of other players' contributions.
   - Initially, p starts at a low value (e.g., 0.1). If the average contribution rate of other players in the previous rounds exceeds a certain threshold (e.g., 0.5), then the AI gradually increases its contribution proportion p by a small increment (e.g., 0.01) per round, up to a maximum value (e.g., 0.6). Conversely, if the average contribution rate of other players falls below a certain threshold (e.g., 0.3), then the AI decreases its contribution proportion p by a small increment per round, down to a minimum value (e.g., 0.1).
   - The AI will defect (i.e., contribute 0 tokens) only if it observes that no other player has contributed in the previous rounds. This is to avoid wasting resources when there is no apparent collective commitment.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, the AI starts with a low contribution percentage (e.g., 0.1) as described in the decision rules above.
   - In the last round, the AI adjusts its contribution based on the average contribution rate of other players during the game but does not increase or decrease p beyond its minimum and maximum values respectively.

3. Be collective - Align with the collective mindset:
   - The strategy aims to promote collective welfare by aligning contributions with the average contributions of other players in the group, while also ensuring that individual incentives are considered through the adaptive contribution percentage.
   - The AI prioritizes cooperation when it observes that others are cooperating and vice versa. This encourages a collective mindset where contributions are based on the actions of the group rather than solely individual decisions.
'''

description_COLLECTIVE_36 = '''
 Strategy Name: Adaptive Contribution (AC) Strategy

1. Decision Rules:
   - In each round, the AC strategy compares its past contributions with the average contribution of all players in the game so far. If the individual's contribution is lower than the average, it increases its contribution by one token (C). Conversely, if the individual's contribution is higher than the average, it decreases its contribution by one token (D).
   - In case of a tie between the player's past contributions and the average contributions, the strategy remains neutral by contributing one token (C).
   - If a player contributes zero tokens in a round, it will continue to contribute zero tokens for the following rounds, as this is considered as a signal that the player has exhausted its resources.

2. Handling Edge Cases:
   - In the first round, each player starts by contributing one token (C) since there's no information about the others' contributions available.
   - In the last round, each player will contribute based on the current average contribution of all players in the game during that particular round.

3. Alignment with Collective Mindset:
   - The AC strategy encourages cooperation by incentivizing players to adjust their contributions according to the collective behavior observed in the game so far.
   - By responding adaptively to changes in the group's average contribution, the strategy aims to maintain a balance between individual and collective welfare, thereby fostering a more cooperative environment.
'''

description_COLLECTIVE_37 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game

1. Decision Rules:
   - In each round, the ATFT strategy starts by cooperating (contributing 1 token). Subsequent decisions are based on the previous round's actions of the opponent.
   - If the opponent cooperated in the previous round, the ATFT strategy also cooperates. If the opponent defected, the ATFT strategy defects in the current round but will return to cooperation in the next round, assuming the opponent repeats their actions.

2. Handling Edge Cases:
   - In the first round, all strategies start by cooperating, so the ATFT strategy also cooperates.
   - In the last round, since there are no future rounds, the ATFT strategy does not punish or reward the opponent and simply cooperates as its final action.

3. Collective Mindset:
   - The ATFT strategy aims to encourage cooperation by reciprocating the actions of others, fostering a collective mindset where players contribute to the common good when they perceive that others are doing so as well.
   - By starting with cooperation and only defecting in response to defection, the ATFT strategy demonstrates a willingness to cooperate while also maintaining a sense of fairness and punishing those who do not contribute their share to the public good.
'''

description_COLLECTIVE_38 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules - The APGG strategy adapts to the average contribution rate (CR) of the opponents in each round, incentivizing cooperation when CR is high and defection when it's low.
   - If CR > 0.6, contribute (C) with a probability proportional to CR - 0.6 to encourage continued cooperation.
   - If CR <= 0.6, defect (D) to punish low contributors and discourage future defections.

2. Handle Edge Cases - In the first round, APGG uses a random contribution (C or D) to establish a baseline for CR calculation. In the last round, APGG contributes as it did in the previous round based on the calculated CR.

3. Be Collective - The APGG strategy aims at fostering collective welfare by adapting its contributions to the average behavior of opponents and encouraging cooperation when possible. It does not require shared norms or coordination but instead relies on adaptive decision-making based on observed contributions in previous rounds.

In summary, here's a simplified pseudocode for APGG:

1. Initialize CR with random value in [0, 1]
2. In each round t:
   - Calculate the average contribution rate (CR) of all opponents up to round t-1.
   - If CR > 0.6, contribute with a probability proportional to CR - 0.6. Otherwise, defect.
3. Store the contribution decision for use in the next round.
4. After the last round, do not change contribution decision based on new data.
'''

description_COLLECTIVE_39 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT) for Public Goods Game

1. Decision Rules - A-TFT cooperates by contributing 1 token in the initial round and responds to other players' contributions in subsequent rounds. In each round, if a player contributes (C), A-TFT also contributes. If a player defects (D) by not contributing, A-TFT will also defect in the next round but return to cooperating after that, assuming the defector does the same and starts cooperating again.

   Pseudocode:
   - Round 1: Contribute 1 token (C)
   - Subsequent Rounds: If other player contributes (C), contribute 1 token (C). Else, if other player defected (D) in the previous round, also defect (D) in this round. If the defector starts cooperating again, resume cooperation in the next round.

2. Handle Edge Cases - In the first round, A-TFT contributes 1 token as it is the initial move. In the last round or any round where the game is terminated prematurely, A-TFT will follow the same decision rules based on the contributions of other players in the previous rounds.

3. Collective Mindset - By following the Tit-for-Tat strategy, A-TFT aims to encourage cooperation among players, as it responds positively when others cooperate and punishes defection moderately by temporarily stopping cooperation. This approach aligns with a collective mindset by encouraging long-term reciprocity and mutual benefit among players.
'''

description_COLLECTIVE_40 = '''
 Public Goods Game Strategy: Tit-for-Tat with Focal Point Adaptation (TFT-FA)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (cooperate). This is a focal point, a starting assumption that can help establish cooperation in the absence of other information.
   - For subsequent rounds, observe past actions of opponents. If an opponent has contributed in the previous round, also contribute one token (cooperate). If they did not contribute, do not contribute either (defect). This is based on the Tit-for-Tat strategy from game theory, which emphasizes reciprocity.
   - Adapt focal point based on observed opponent behavior:
       a) If opponents generally cooperate, continue with the initial focal point (contribute one token in the first round).
       b) If opponents often defect, switch to a new focal point where everyone starts by not contributing (defect in the first round).
   - To avoid being exploited by free riders who always defect regardless of past actions, occasionally break Tit-for-Tat and contribute even when opponents have previously defected. This keeps opponents guessing and discourages repeated defection.

2. Handle edge cases:
   - Last round: Contribute one token (cooperate) as a goodwill gesture, encouraging cooperation in future games with the same opponents.
   - Other edge cases (e.g., rounds with partial contributions or varying multipliers k and n) can be handled by adapting contribution levels based on the modified game rules while maintaining the core TFT-FA strategy.

3. Be collective - Align with the collective mindset:
   - Prioritize strategies that promote cooperation and shared benefits, as this approach is more aligned with a collective mindset and benefits the group over time.
   - In competitive scenarios where individual payoffs are prioritized, modifications to the TFT-FA strategy can be made to better suit the new environment while still emphasizing reciprocity and adaptability.
'''

description_COLLECTIVE_41 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Specify decision rules:
   - In each round, the ACA uses a contribution rate that adjusts based on historical performance and game parameters. The contribution rate (CR) is a value between 0 and 1 that determines the probability of contributing one token (C).
   - If CR > 0.5, contribute one token (C); otherwise, contribute zero tokens (D).
   - To calculate the contribution rate for each round, ACA considers two factors: personal average contribution rate (PAR) and social optimal contribution rate (SOR).
     a. PAR is calculated as the average of the player's own contributions across all previous rounds.
     b. SOR is calculated as (k/n), as it represents the optimal contribution level to maximize payoff in the absence of free-riders.
   - The final contribution rate for each round is a weighted combination of PAR and SOR, with the weights determined by two constants: α (importance of personal history) and β (importance of game parameters).
     c. Final CR = α * PAR + β * SOR

2. Handle edge cases:
   - First round: Since there is no historical data, ACA starts with an equal contribution rate for all players, i.e., CR = 0.5.
   - Last round: If the game has a fixed number of rounds, ACA considers this as the final round and adjusts its contribution rate accordingly. However, if the game continues indefinitely or does not specify a maximum number of rounds, ACA treats every round as if it could be the last one, so CR still depends on PAR and SOR.
   - Changing players: If the composition of players changes due to elimination or new entrants, ACA resets its personal average contribution rate (PAR) based on the contributions made by the current players.

3. Be collective:
   - By adjusting the contribution rate based on both historical performance and game parameters, ACA promotes cooperation when it is beneficial for the group while avoiding excessive contributions that may not lead to higher payoffs.
   - As ACA calculates SOR using the multiplier k and number of players n, it aligns with the collective mindset by considering the shared project's benefits and ensuring fair distribution among all players.
'''

description_COLLECTIVE_42 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATFTGC)

1. Decision Rules:
   - In the first round, contribute 50% of tokens to foster initial cooperation. (c_i = 0.5)
   - For subsequent rounds, adopt a "Tit-for-Tat" approach:
     - If a player contributes in the previous round (C), reciprocate by contributing fully in the current round (c_i = 1).
     - If a player defected (D) in the previous round, also defect for a number of rounds equal to the average number of defections from that player in the last 'x' rounds, then gradually cooperate again. The rate of gradual cooperation is determined by the number of times the player contributes out of the past 'x' rounds, divided by 'x'.

2. Handling Edge Cases:
   - In the last round, contribute fully to maximize potential payoff (c_i = 1).
   - If a player has never contributed in the past 'x' rounds, consider them as a chronic defector and follow the "Tit-for-Tat" approach by defecting for the same number of rounds as described earlier. After that, gradually cooperate based on the rate calculated from their recent behavior.
   - If a player contributes in the last round despite never contributing before, appreciate their new cooperation but continue to follow the gradual cooperation rule based on their past 'x' rounds of actions.

3. Aligning with the Collective Mindset:
   - The strategy aims to promote mutual cooperation by rewarding consistent contributors and gradually encouraging defectors to cooperate. However, it also punishes chronic defection by defecting for a certain number of rounds before attempting to re-establish cooperation. This strategy encourages collective welfare while being robust against various opponent behaviors.
'''

description_COLLECTIVE_43 = '''
 Strategy Name: Adaptive Tit-for-Tat with Fading Memory (A-TFTF)

1. Specify decision rules - When do you cooperate vs defect?
- In the first round, contribute 1 token (cooperate). This sets a cooperative initial condition.
- From the second round onwards, observe and copy the opponent's action from the previous round. If the opponent contributed in the last round, also contribute 1 token in this round (cooperate). If the opponent did not contribute in the last round, do not contribute any tokens (defect).
- To encourage cooperation, implement a fading memory mechanism: after a certain number of rounds, disregard older actions and only consider the most recent contributions when deciding to cooperate or defect. This encourages both forgiveness for past defections and consistent cooperation based on recent actions.

2. Handle edge cases - What do you do in the first round, last round, etc.?
- In the last round, since there will be no future interaction with opponents, contribute 1 token (cooperate) regardless of their previous actions to maximize payoff.

3. Be collective - Clearly align with the collective mindset
- The A-TFTF strategy is collectively oriented because it encourages cooperation and fair contribution to shared projects based on the actions of other players in the game. By considering past contributions, the strategy aligns with the collective welfare and incentivizes other players to do the same.
'''

description_COLLECTIVE_44 = '''
 In this Public Goods Game (PGG), the designed adaptive and robust collective strategy is called the Tit-for-Tat with Adaptation (TfTA). The TfTA strategy aims to encourage cooperation while also being responsive to opponents' behavior.

1. Specify decision rules:
   - In the first round, cooperate as a gesture of goodwill (c_i = 1)
   - If an opponent has contributed in the previous round (c_j > 0), cooperate in the current round (c_i = 1). This encourages cooperation and builds trust.
   - If an opponent has not contributed in the previous round (c_j = 0), defect in the current round (c_i = 0) to penalize them for their lack of cooperation. The aim is to encourage opponents to cooperate when they see that doing so is rewarded.
   - Repeat steps 2 and 3 throughout the game.

2. Handle edge cases:
   - Last round: Cooperate as a gesture of goodwill, even if an opponent did not cooperate in the previous round (c_i = 1). This encourages cooperation and potentially sets the stage for future games.
   - If there's a tie in contribution history, default to cooperation (c_i = 1) to encourage collaboration.

3. Be collective:
   - The TfTA strategy is designed to align with the collective mindset by promoting cooperation among players. By cooperating when opponents do and defecting when they don't, the TfTA strategy aims to build a more cooperative environment in the long run.
'''

description_COLLECTIVE_45 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT) for Public Goods Game

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate) as an initial goodwill gesture.
   - For subsequent rounds, if a player contributed in the previous round, they will receive the same response (either cooperation or defection) in the current round. However, if the player defected in the previous round, they will be punished by defecting in the current round. The purpose of this strategy is to encourage cooperation while retaliating against defection.

2. Handle edge cases - What to do in the first and last rounds, etc.:
   - In the first round, cooperate (contribute 1 token).
   - In the last round, evaluate the total contributions over all previous rounds and contribute accordingly to ensure fairness. If the total contributions are less than the expected contributions based on a reasonable level of cooperation, defect in this round to punish those who have not contributed sufficiently. Otherwise, cooperate as usual.
   - For intermediate rounds, use the decision rule described above (cooperate or defect based on opponent's previous action).

3. Be collective - Align with the collective mindset:
   - By cooperating when others do and punishing defection, this strategy aims to promote a collective mindset where contributing to the public good is beneficial for everyone in the long run.
   - If many players adopt the A-TFT strategy, it encourages cooperation as each player will receive the same response they gave in the previous round, fostering a self-enforcing equilibrium of mutual cooperation.
   - However, since no shared norms or coordination are assumed, this strategy is robust to various opponent behaviors and can still function effectively even when confronted with non-cooperative strategies.
'''

description_COLLECTIVE_46 = '''
 In this repeated Public Goods Game (PGG), we will design an adaptive and robust strategy called the "Tit-for-Tat with Adaptation" strategy. This strategy aims to balance cooperation and defection while aligning with a collective mindset.

1. Decision Rules:
   - In the first round, contribute 1 token (C), as this can set a cooperative tone for the game.
   - For subsequent rounds, observe other players' past actions and adjust your own contribution accordingly. If another player has consistently contributed in the previous round(s) (let's say, r-1 rounds), then contribute 1 token (C). Otherwise, if they have not contributed, also withhold your contribution (D). This encourages cooperation among cooperators while punishing defectors without being overly aggressive.
   - If a player switches from contributing to not contributing or vice versa, wait for r rounds before responding to their new behavior. This allows for some flexibility and forgiveness in case of occasional mistakes or changes in strategy.

2. Handling Edge Cases:
   - In the last round, contribute 1 token (C), as there are no future consequences, and it might still benefit from contributing to a public good.
   - In the event that a player never contributes, the strategy will not retaliate with defection immediately but wait for r rounds before adjusting its response.

3. Being Collective:
   - By adopting a Tit-for-Tat approach, the strategy encourages cooperation and promotes a collective mindset by rewarding other cooperative players while also punishing defectors. The strategy is designed to foster an environment where contributing to the public good becomes beneficial in the long run for all players who cooperate.
   - The use of adaptive behavior allows for adjustments based on the collective performance of the group, encouraging a more collaborative approach over time as players observe each other's actions and react accordingly.
'''

description_COLLECTIVE_47 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Specify decision rules - When do you cooperate vs defect?
   - In each round, the player will contribute if and only if a minimum threshold of contributions from other players is met in the previous round. The threshold decreases over time to encourage cooperation in the early rounds.

   Threshold calculation:
     - Initial Round (t=1): Contribution_threshold = n (total number of players)
     - Last Round (t=r): Contribution_threshold = 0
     - Intermediate Rounds (2 <= t <= r-1): Contribution_threshold = (n - t + 1) * (k / n)

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, the player will contribute since no contribution threshold has been met yet.
   - In the last round, the player will not contribute because the contribution threshold is 0.

3. Be collective - Clearly align with the collective mindset
   - The strategy aims to balance individual incentives with collective welfare by adjusting the contribution level based on the actions of other players in each round. This encourages cooperation and collective benefit over time.

Additional considerations:
- To ensure robustness against a wide range of opponent behaviors, the ACS strategy can be tweaked by adjusting parameters such as the initial threshold, the rate at which the threshold decreases, or the multiplier k. These parameters can be fine-tuned based on simulation results and observations from gameplay against other strategies.
- The ACS strategy is designed to work without any communication or coordination with other players, making it suitable for a tournament of independent strategies.
'''

description_COLLECTIVE_48 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Decision Rules:
   - In each round, the ACS calculates an average contribution rate based on its own past contributions and observed payoffs of other players.
   - If the calculated average contribution rate is above a certain threshold, ACS chooses to cooperate (contribute 1 token) in the current round. Otherwise, it defects (contributes 0 tokens).
   - The threshold can be adjusted based on the game parameters and the number of rounds played. For example, a higher threshold might be used at the start of the game to encourage cooperation, while a lower threshold could be used towards the end as the game approaches its conclusion.

2. Handling Edge Cases:
   - In the first round, ACS starts by contributing 1 token (cooperating) since there is no past data to base decisions on.
   - As the game nears its end, ACS might switch to defecting if it realizes that continued cooperation will not yield enough payoff due to limited remaining rounds or low average contributions from other players.

3. Collective Alignment:
   - ACS is designed to promote collective welfare by cooperating when it perceives that others are also doing so, and defecting only when it perceives a lack of cooperation from the group.
   - By adapting its contribution decisions based on observed player behavior, ACS hopes to encourage similar adaptive behavior in other players over time, ultimately fostering a more cooperative environment.
'''

description_COLLECTIVE_49 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules - Cooperation vs Defection:
   In each round, the APGG strategy will decide to contribute based on the average contribution rate of the previous rounds (average_contribution).
   If average_contribution is above a threshold (T), the strategy will cooperate (C); otherwise, it will defect (D). The threshold T is determined by the multiplier k and the number of players n, as follows: T = (k - 1) / n.
   In case the average_contribution is exactly equal to T, the APGG strategy will make a random decision between cooperation and defection.

2. Handling Edge Cases:
   - First Round: The APGG strategy starts by assuming other players are cooperative or follow some cooperation strategy (T > 0). However, it does not contribute in the first round to ensure other players have an incentive to cooperate.
   - Last Round: In the last round, the APGG strategy will cooperate if the average_contribution during the game is above T, as other players may also contribute more to maximize their total payoff. If the average_contribution is below T, the APGG strategy will defect since there is no benefit in contributing when others are not doing so.
   - Intermediate Rounds: In rounds after the first and before the last, the APGG strategy will calculate the average_contribution from previous rounds and make a decision based on the specified rules.

3. Collective Mindset:
   By cooperating when other players do so and defecting when they do not, the APGG strategy aligns with the collective mindset by promoting cooperation among players in a repeated game setting, while being adaptive to various opponent behaviors.
'''

description_COLLECTIVE_50 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT) for Public Goods Game

1. Specify decision rules - When do you cooperate vs defect?
   - Initially, cooperate in the first round to support collective welfare (c_i = 1). Subsequent decisions are based on past actions of opponents.
   - If an opponent contributes in the previous round, cooperate (c_i = 1). This is a reciprocal gesture, hoping for continued cooperation from the opponent.
   - If an opponent defected in the previous round, defect as well (c_i = 0). This punishment aims to encourage opponents to contribute in future rounds.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, everyone cooperates since there's no prior information available.
   - In the last round, ATfT will consider the average contributions from opponents throughout the game to determine its action. If the average contribution is above a certain threshold (e.g., the average contribution of k/n), ATfT will contribute as well; otherwise, it will defect.

3. Be collective - Clearly align with the collective mindset
   - ATfT encourages cooperation and reciprocity among players, promoting collective welfare in the long run. This strategy aims to balance individual incentives and collective benefit by rewarding cooperative behaviors and punishing defections.

Pseudocode for ATfT:
```
function Adaptive_Tit_for_Tat(n, k, round, history):
  if round == 1:
    contribution = 1 (cooperate)
  else:
    opponentContribution = history[round-1]
    if opponentContribution == 1:
      contribution = 1 (cooperate)
    else:
      contribution = 0 (defect)
  return contribution

function ATfT_lastRound(n, k, history):
  totalContributions = sum of history
  averageContribution = totalContributions / len(history)
  if averageContribution > (k/n):
    contribution = 1 (cooperate)
  else:
    contribution = 0 (defect)
  return contribution
```
In the tournament, ATfT will adjust its behavior based on the performance against other strategies. It may adapt the threshold for determining cooperation in the last round or introduce forgiveness mechanisms to account for temporary defections.
'''

description_COLLECTIVE_51 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - APGC cooperates when the average contribution of players in the previous rounds indicates a shared commitment towards collective welfare, and defects otherwise to maximize personal gain.

   - If the average contribution in the last 'm' rounds (where m is a predefined constant) is above a threshold T, APGC will contribute (C). Otherwise, it will not contribute (D). The threshold T can be calculated as follows:
     T = (k / n) * (1 + ε) * average_contribution_in_m_rounds
     where ε is a small constant that ensures some level of contribution even in the absence of strong collective behavior.

2. Handling Edge Cases - In the first round, APGC contributes at a level slightly below the calculated threshold to test the cooperative spirit of other players and adapt its future contributions accordingly. In the last round, APGC behaves based on the average contribution pattern observed in previous rounds. If collective cooperation is evident, it will contribute; otherwise, it will defect.

3. Collective Mindset - APGC aims to encourage a collaborative environment by adapting its contributions to the collective behavior of other players. By responding positively to cooperative actions and punishing defection through reduced contributions, APGC fosters an atmosphere where long-term collective success is valued over short-term personal gain.
'''

description_COLLECTIVE_52 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules:
   - In each round, the APGG strategy will consider two factors for decision-making: the average contribution rate (CR) of all players in the game history and the individual player's own contribution rate. The threshold for contributing is set at `(2 * k) / n` as a balance between self-interest and collective welfare.
   - If the average CR is greater than or equal to the threshold, the APGG strategy will contribute (C). Conversely, if the average CR is less than the threshold, it will not contribute (D).
   - If a player's own contribution rate is consistently below the average CR, they are considered as free-riders and will have their contributions capped at a minimum level to avoid excessive free-riding. The minimum contribution level is set to `k / n`.

2. Handling Edge Cases:
   - In the first round, each player starts with no history, so they contribute randomly with equal probability (0.5) until enough data points are collected for an informed decision.
   - In the last round or any round where the game ends prematurely, players will contribute based on their most recent observations of the average CR and their own contribution rate.

3. Collective Mindset:
   - The APGG strategy prioritizes collective welfare by adjusting its contributions in response to the average contribution behavior of other players. This adaptability encourages cooperation while also accounting for free-riders.
   - By capping contributions from free-riders, the APGG strategy ensures a minimal level of collaboration that benefits all players in the long run, fostering a collective mindset within the game.
'''

description_COLLECTIVE_53 = '''
 Strategy Name: Adaptive Tit-for-Tat Public Goods Game (ATTPG)

1. Decision Rules:
   - In each round, if the total contribution of all players in the previous round was greater than a threshold (n/2), then the ATTPG strategy will cooperate (contribute 1 token). Otherwise, it will defect (contribute 0 tokens).
   - If another player changes their contribution strategy from previous rounds, the ATTPG strategy will mimic their new behavior for the next few rounds before making a decision to cooperate or defect based on the updated total contributions.

2. Handling Edge Cases:
   - In the first round, each player will contribute randomly with an equal probability of 0.5 to mimic uncertainty about other players' strategies.
   - In the last round, as there are no future rounds for reciprocation, ATTPG will cooperate if the total contribution in the previous round exceeds the threshold (n/2), otherwise it will defect.

3. Collective Mindset:
   - The ATTPG strategy fosters a collective mindset by encouraging cooperation when other players contribute significantly to the public good.
   - By mimicking other players' strategies, the ATTPG strategy shows flexibility and adaptability in response to different opponent behaviors.
'''

description_COLLECTIVE_54 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Decision Rules (Cooperate vs Defect):
   - In each round, the strategy calculates an average contribution rate based on past contributions and payoffs. If the current player's average contribution rate is higher than a predefined threshold, they will cooperate (contribute 1 token). Otherwise, they will defect (contribute 0 tokens).
   - The predefined threshold can be adjusted based on the game parameters, such as the number of players (n), rounds (r), and multiplier (k). A higher threshold encourages more cooperation when contributions are high, while a lower threshold encourages defection when contributions are low.

2. Handling Edge Cases:
   - In the first round, each player starts with no past data, so they choose to cooperate if and only if their predefined threshold is less than or equal to 0.5 (or any other value that promotes initial cooperation).
   - In the last round, players will have a clear idea about the overall contribution rate and can make an informed decision based on the strategy's decision rules.

3. Being Collective:
   - ACS aligns with the collective mindset by incentivizing higher contributions when the group as a whole is contributing more, and vice versa. The predefined threshold plays a crucial role in balancing individual incentives against collective welfare.
   - As players adapt to each other's strategies over time, the average contribution rate should converge towards an equilibrium where contributions are optimized for both individual payoffs and collective benefits.
'''

description_COLLECTIVE_55 = '''
 In this Public Goods Game (PGG), the following adaptive and robust collective strategy, named Adaptive Contribution Strategy (ACS), can be designed to balance individual incentives with collective welfare:

1. Specify decision rules:
   - If the current round is the first, contribute 1 token (C) to establish an initial contribution level and encourage other players to follow suit.
   - For subsequent rounds, calculate the average contribution rate (CR) by dividing the sum of all past contributions by the total number of players and rounds played so far: CR = (Total Contributions / (n * r)).
   - Based on the calculated CR, determine your action for the current round as follows:
     a. If CR >= k/(n-1), contribute 1 token (C) to maintain the current contribution level.
     b. If CR < k/(n-1) and CR > k/n, contribute a fraction of tokens based on the calculated CR: c_i = floor(CR * n).
     c. If CR <= k/n, do not contribute any tokens (D) to signal disapproval of the current contribution level and encourage others to increase their contributions.

2. Handle edge cases:
   - In the last round, since there are no more rounds to recover the lost collective benefit, each player should contribute 1 token (C) to maximize the overall payoff for all players.
   - In the first round and subsequent rounds with low contributions (CR < k/(n-1)), it's essential to encourage a higher contribution level by not contributing any tokens (D).

3. Be collective:
   - The ACS strategy aims to promote a collaborative environment by incentivizing higher contributions when the current contribution level is sustainable and reducing contributions when the collective welfare is at risk. This adaptive approach encourages players to maintain a balanced and sustainable contribution rate over time.

The ACS strategy aligns with the collective mindset by promoting cooperation through its decision rules, handling edge cases appropriately, and incentivizing higher contributions when necessary for the greater good of all players in the repeated game.
'''

description_COLLECTIVE_56 = '''
 Strategy for Public Goods Game (PGG): Tit-for-Tat-Cooperate (TFT-C)

1. Specify decision rules:
   - In the first round, cooperate (contribute 1 token). This is a gesture of goodwill and sets a cooperative tone for the game.
   - For subsequent rounds, observe past actions of opponents:
     - If an opponent has cooperated in the previous round, cooperate in the current round (mimic their cooperation).
     - If an opponent has defected (did not contribute) in the previous round, also defect in the current round (punish their defection).

2. Handle edge cases:
   - In the last round, since there are no future interactions with opponents, cooperate to maximize personal payoff.
   - If an opponent does not have a past history of actions (e.g., in the first few rounds), start by assuming cooperation and adjust based on their subsequent moves.

3. Be collective:
   - The TFT-C strategy promotes a long-term cooperative relationship with opponents while also punishing defection. This encourages collective welfare as players who consistently contribute to the public good will be rewarded by those who reciprocate cooperation.
   - By mimicking opponent's behavior, the strategy aligns with a collective mindset and promotes cooperation rather than unilateral decision-making.
'''

description_COLLECTIVE_57 = '''
 Public Goods Game Strategy: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - In each round, observe the total contributions from all players in the previous round (historical average).
   - If the historical average is above a certain threshold (average contribution per player), contribute 1 token (Cooperate). Otherwise, contribute 0 tokens (Defect).
   - The threshold can be adjusted based on the game parameters and opponent behaviors. A reasonable initial value could be the average contribution of the first few rounds.

2. Handling Edge Cases:
   - First Round: Contribute 1 token as there is no historical data available yet (Cooperate).
   - Last Round: Adapt to the most common contribution behavior observed throughout the game. If contributions are above the threshold, contribute 1 token; otherwise, contribute 0 tokens.
   - Other edge cases, such as changing players or round numbers, can be handled by adjusting the historical average based on the available data.

3. Being Collective:
   - The strategy is designed to promote cooperation by punishing free-riders and rewarding contributors, while being adaptive to a wide range of opponent behaviors.
   - The strategic choice between cooperating and defecting depends on the collective behavior observed in previous rounds, encouraging players to contribute when others do so as well.
   - The strategy aims at fostering an environment where contributing becomes the norm, as it responds positively to cooperative actions and punishes non-cooperative ones.
'''

description_COLLECTIVE_58 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules:
   - In each round, the APGG strategy compares its past contributions with the average contribution of all players.
   - If the individual's contribution is below the average, it increases its contribution by a factor determined by its past deviation from the average and the current average.
   - If the individual's contribution is above the average, it maintains or reduces its contribution based on its past contribution level and the current average.

2. Handling Edge Cases:
   - First Round: APGG starts with a moderate contribution (50%) to encourage others while not overextending itself.
   - Last Round: APGG contributes all of its tokens to maximize potential gains, given that no further rounds are anticipated.
   - Penultimate Round: APGG reduces its contribution to ensure resources for the final round, while still contributing significantly.

3. Collective Mindset:
   - APGG strategy aims to foster a collective mindset by maintaining a stable and fair average contribution throughout the game. It adjusts its contribution based on the group's behavior, incentivizing others to cooperate while still preserving its own resources.

By adapting to various opponent behaviors and promoting a collective approach, APGG strategy should perform well in tournaments against other AI systems.
'''

description_COLLECTIVE_59 = '''
 Public Goods Game Strategy: Tit-for-Tat with Fading Memory (TFTF)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This initial cooperation sets a positive tone and encourages reciprocity in future rounds.
   - For subsequent rounds, observe contributions from others in the previous round. If all players contributed (C), continue contributing (C). If any player did not contribute (D), also do not contribute (D) in the current round to punish non-cooperation.
   - Implement a fading memory mechanism where past transgressions are forgiven over time. After each consecutive round of cooperation, forget one instance of past non-cooperation. This encourages opponents who have previously defected to eventually cooperate again.

2. Handle edge cases:
   - In the last round, since future payoffs do not affect current decisions, contribute (C) regardless of previous contributions from others as a final act of cooperation.
   - In case of an empty history (first encounter with another strategy), always start by contributing (C).

3. Be collective - Align with the collective mindset:
   - The TFTF strategy seeks to encourage cooperation and reciprocity among players, thereby promoting collective welfare and ensuring that all players receive adequate benefits from the public goods game.
   - By forgiving past non-cooperation and rewarding consistent cooperation, the strategy encourages a long-term collaborative relationship between players, further aligning with the collective mindset.
'''

description_COLLECTIVE_60 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC will decide to contribute based on a combination of individual incentives and collective welfare. The contribution level will be determined by the average past contributions of all players (average_contribution).
   - If average_contribution is less than a predefined threshold (e.g., 0.4), the APGC will contribute at the maximum level (1 token) to stimulate collective action and encourage others to cooperate.
   - If average_contribution is greater than or equal to the threshold, the APGC will contribute based on a decay function that adjusts its contribution level in response to changes in the average contributions over time. The decay function can be defined as:
     contribution = initial_contribution * (1 - rate_of_decay * (round - 1))
   - Where initial_contribution is set at the maximum level (1 token) and rate_of_decay is a predefined value that determines how quickly the APGC adjusts its contribution based on changes in average contributions.

2. Handling Edge Cases:
   - First Round: The APGC will contribute at the maximum level (1 token), as it has no past data to base its decision on.
   - Last Round: The APGC will contribute based on the decay function, even if the average contribution is below the threshold, as it aims to maintain some level of cooperation throughout the game.

3. Alignment with Collective Mindset:
   - By contributing at the maximum level when average contributions are low and adjusting contributions based on collective actions over time, the APGC seeks to promote a culture of cooperation and encourages others to contribute as well. It does not rely on specific opponent behaviors or coordination but instead responds dynamically to the collective behavior in the game.
   - The APGC also learns from past experiences and adapts its contribution level to maximize long-term benefits for all players, fostering a more sustainable and cooperative environment within the repeated game.
'''

description_COLLECTIVE_61 = '''
 In this Public Goods Game (PGG), I will design an adaptive and robust collective strategy called the "Adaptive Tit-for-Tat" (ATFT). The goal of ATFT is to balance individual incentives with collective welfare, ensuring a sustainable contribution level.

1. Specify decision rules:
   - In the first round, contribute with probability p_init (e.g., 0.5), promoting fairness and encouraging cooperation.
   - For subsequent rounds, observe other players' past actions. If they have consistently contributed (cooperated), return the favor by also contributing in the current round. If they have not contributed (defected), respond by defecting as well to signal disapproval of their behavior. However, if a defector changes their strategy and contributes in the current round, immediately resume cooperation for future rounds.
   - If a player encounters a free-rider (continuously defects), allow them a grace period of T_free rounds before permanently adopting a "punishment" strategy (e.g., always defect).

2. Handle edge cases:
   - In the last round, maximize personal payoff by contributing if the total contributions are less than n, and defect otherwise to encourage others to contribute.
   - In the first round, players will randomly choose their actions. If there is a high probability of cooperation, ATFT will continue cooperating. If not, it will adopt a "punishment" strategy for T_free rounds before returning to the decision rules mentioned above.

3. Be collective:
   - The ATFT strategy emphasizes reciprocity and encourages cooperation among players while being flexible enough to respond to defections or free-riding behaviors. It aims to strike a balance between individual and collective interests, promoting sustainable contributions throughout the game.

The ATFT strategy is designed to be adaptive and robust, making it well-suited for a tournament against various AI strategies in the Public Goods Game.
'''

description_COLLECTIVE_62 = '''
 Strategy Name: Adaptive ContribuTion Algorithm (ACTA)

1. Decision Rules - ACTA cooperates when the expected payoff from contributing outweighs the payoff from defecting. In each round, the decision rule is as follows:
   - If total contributions in the previous round were above a certain threshold (n * AverageContribution), ACTA contributes (C).
   - Otherwise, if total contributions were below another threshold (n * MinimumContribution), ACTA defects (D).
   - In all other cases where the total contributions are neither too high nor too low, ACTA randomly decides to contribute or defect with a probability that depends on the total contributions from the previous round. This probability decreases linearly between the two thresholds.

2. Handling Edge Cases - In the first round, since there is no history, ACTA starts by contributing (C) 50% of the time and defecting (D) 50% of the time. In the last round, ACTA follows the same decision rules as in other rounds but keeps track of the cumulative contributions throughout the game to determine the thresholds for contribution.

3. Being Collective - ACTA aligns with the collective mindset by considering the group's actions as a whole and making decisions based on the collective good rather than individual gain. By contributing when total contributions are above a certain threshold, ACTA encourages others to contribute as well, ultimately benefiting the entire group.

In summary, ACTA is an adaptive strategy that balances cooperation and defection based on the group's past contributions. It promotes collective welfare by encouraging contribution when it seems likely that others will do the same, while also being robust to various opponent behaviors due to its random decision-making mechanism in grey areas.
'''

description_COLLECTIVE_63 = '''
 Public Goods Game Strategy: Cooperative Tit-for-Tat (CTFT)

1. Specify decision rules:
   - In the first round, contribute one token (C), as there's no history to base decisions on.
   - For subsequent rounds, observe the opponent's contribution in the previous round. If they contributed, do so as well; if they didn't, also withhold contributions. This approach encourages cooperation while allowing for punishment when necessary.

2. Handle edge cases:
   - In the last round, contribute one token (C), even if the opponent didn't in the previous round. This ensures maximizing personal and collective payoffs.
   - For the initial rounds after a period of no interaction (e.g., new match or after a long pause), follow the same rule as the first round: contribute one token (C).

3. Be collective:
   - The CTFT strategy prioritizes the collective well-being by encouraging cooperation, but it also includes elements of punishment for non-cooperative behavior. This balance allows for both collective and individual interests to be met.

This strategy aims to foster a cooperative environment while being robust against various opponent behaviors. By adjusting contributions based on observed actions, the CTFT strategy seeks to establish trust and promote cooperation in repeated interactions.
'''

description_COLLECTIVE_64 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate), as there is no prior information about other players' actions.
   - For subsequent rounds, if a player has contributed in the previous round, they should also contribute in the current round (continue cooperation). If a player did not contribute in the previous round, they should also withhold contribution in the current round (continue defecting). This is to encourage reciprocation and discourage freeloading.
   - If a player has been consistently contributing (i.e., a streak of cooperative moves) and encounters a round of defection, they should forgive and return to cooperation for the next round.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate), as there are no subsequent rounds for retaliation or forgiveness.
   - If a player encounters an inconsistent behavior from another player (e.g., cooperates one round and defects the next), they should assume it is an anomaly and continue with their own decision rule.

3. Be collective - Align with the collective mindset:
   - By encouraging reciprocation, the strategy aims to foster a collective mindset where cooperation is rewarded and defection is penalized. This encourages players to contribute more to the public good, thus promoting collective welfare.
   - The strategy is adaptive as it adjusts its actions based on the opponent's behavior in previous rounds, enabling it to respond effectively to a wide range of opponent strategies.
'''

description_COLLECTIVE_65 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - Cooperate (Contribute 1 token, C) when the average contributions of all players in the previous rounds exceeds a threshold T, calculated as n/(k-1). Defect (Contribute 0 tokens, D) otherwise. The rationale behind this is that if the contributions from players are consistently high, it indicates a cooperative environment and encourages continued cooperation. Conversely, if contributions are low, it suggests defection and self-interest will be rewarded.

2. Handle Edge Cases - In the first round (no previous history), all players start by contributing randomly with a probability P_init, where P_init is a predefined value close to the optimal contribution level. This prevents the tragedy of the commons in the initial rounds. In the last round and whenever the total contributions meet or exceed the group's resources, no further contributions are made.

3. Be Collective - The APGC strategy seeks to maximize collective welfare by fostering a cooperative environment while being adaptive to various opponent behaviors. It aligns with a collective mindset by encouraging higher contributions when the average cooperation of all players is above the threshold, thus benefiting the group as a whole.

Pseudocode:

```
function APGC(n, k, c_history, round) {
    if (round == 1) {
        contribute randomly with probability P_init
    } else {
        average_contributions = sum(c_history) / round
        if (average_contributions > n/(k-1)) {
            contribute 1 token (C)
        } else {
            contribute 0 tokens (D)
        }
    }

    if (round != total_rounds or total_contributions < sum(n)) {
        continue playing
    } else {
        stop contributing
    }
}
```
'''

description_COLLECTIVE_66 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Decision Rules:
   - In each round, the ACA calculates its contribution as follows:
     - If total contributions in the previous round were less than a threshold (n * avg_contributions), contribute 1 token (cooperate).
     - If total contributions in the previous round were greater than or equal to the threshold, do not contribute any tokens (defect). The threshold ensures a balance between individual and collective interests.

2. Handling Edge Cases:
   - In the first round, since there is no history, ACA contributes 1 token to initiate cooperation.
   - In the last round, ACA behaves based on the total contributions in the penultimate round, following the decision rules mentioned above.

3. Alignment with Collective Mindset:
   - The ACA encourages cooperation by contributing to the public good when it perceives that not enough participants are doing so. This fosters a collective mindset as the strategy aims to maximize total contributions over individual gains.
   - If most players are cooperating, the strategy does not contribute to avoid being taken advantage of by freeriders. However, if cooperation drops significantly in the subsequent rounds, the ACA may revert back to contributing 1 token to encourage others to cooperate again.
'''

description_COLLECTIVE_67 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, APGC decides to cooperate or defect based on the average contribution rate of the previous rounds. If the average contribution rate is above a threshold (T), APGC will contribute (C). Otherwise, it will not contribute (D). The threshold (T) is determined by the multiplier (k) and the number of players (n). A higher k or n requires a higher average contribution rate to cooperate.

   Threshold (T) calculation:
   T = (k / n) * (1 + S)
   where S is a sensitivity factor that determines how responsive APGC is to changes in average contribution rate. A lower S value makes APGC more responsive and vice versa.

2. Handling Edge Cases:
   - First Round: APGC starts with no previous history, so it uses the threshold calculation without considering the sensitivity factor (S = 0). This encourages APGC to contribute in the first round if there is a reasonable chance that others will also contribute.

   - Last Round: APGC recognizes the game ending and contributes if the average contribution rate exceeds the threshold, as it can benefit from the multiplier without worrying about future rounds.

3. Collective Mindset:
   - APGC aims to balance individual incentives with collective welfare by adjusting its contributions based on the behavior of other players. It follows a cooperative approach when it expects others to contribute and defects when it anticipates free-riders. By adapting to different opponent behaviors, APGC encourages collaboration while minimizing losses from defection.

This strategy should allow APGC to perform well in various public goods game tournaments against other AI systems, as it is adaptive, robust, and promotes a collective mindset.
'''

description_COLLECTIVE_68 = '''
 Strategy for Public Goods Game (PGG): Cooperative Tit-for-Tat with Adaptive Contribution Level (CTF-ACL)

1. Specify decision rules:
   - In the initial round, contribute a moderate amount (m), set as m = average(k/n). This encourages cooperation while being reasonable for the first contribution.
   - For each subsequent round r, evaluate opponent's cooperative behavior using an average cooperative score (c_score) and adjust the contribution level based on the Adaptive Contribution Level (ACL) algorithm:
     a) If c_score > 0.7, contribute at the maximum level (1), as the opponent is highly cooperative.
     b) If c_score between 0.4 and 0.7, use ACL to determine contribution level.
       i) If ACL < m, decrease contribution by a small amount (e.g., 0.1).
       ii) If ACL > m, increase contribution by a small amount (e.g., 0.1).
     c) If c_score < 0.4, contribute at the minimum level (0), as the opponent is not cooperative.
   - Adaptive Contribution Level (ACL) calculation: ACL = (average contribution of current round) / m

2. Handle edge cases:
   - In the last round, contribute the maximum possible amount to maximize individual and collective payoff.
   - If a player defects in the first round, respond with defection for the next three rounds before reverting back to the cooperative Tit-for-Tat strategy.
   - If no opponents are found during the initial four rounds, continue with the initial contribution level (m).

3. Be collective:
   - The strategy prioritizes cooperation and mutual benefit by contributing to the public good while also being responsive to opponent's behavior. It aims to encourage long-term cooperation and fair contribution levels for a balanced outcome in the repeated game.
'''

description_COLLECTIVE_69 = '''
 Strategy for Public Goods Game: Cooperative Tit-for-Tat (CTFT)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages others to do the same.
   - In subsequent rounds, if a player contributed in the previous round (i.e., other players cooperated), reciprocate by contributing 1 token as well (cooperate).
   - If another player defected by not contributing in the previous round, also defect in the current round to signal disapproval and encourage future cooperation. However, after three consecutive defections from another player, switch back to contributing 1 token (cooperate) to maintain the collective mindset and offer an opportunity for the other player to cooperate again.

2. Handle edge cases:
   - Last round: Since there are no future rounds to reciprocate or punish, contribute 1 token as a final act of cooperation.
   - Tie (multiple players defected): In case of a tie, follow the same decision rules based on the previous round's actions.
   - No history (initial round without past observations): Cooperate initially to set a cooperative tone.

3. Be collective - Align with the collective mindset:
   - Prioritize cooperation over defection to contribute to the public good and support the collective welfare.
   - Offer opportunities for other players to cooperate by reciprocating their contributions and forgiving occasional defections.
   - Maintain a balance between cooperation and punishment to encourage long-term collective success while also responding to individual player behavior.
'''

description_COLLECTIVE_70 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Awareness (ATFPGA)

1. Decision Rules:
   - In the first round, contribute 1 token (cooperate), as no history is available yet.
   - Subsequent rounds, contribute based on the average contribution of other players in the previous rounds:
     - If the average contribution is above a threshold (e.g., 0.5), contribute 1 token (cooperate).
     - If the average contribution is below the threshold, do not contribute (defect).
   - This rule ensures cooperation when others are also contributing and defection when they are not.

2. Handling Edge Cases:
   - Last round: Contribute according to the decision rules based on the observed average contribution throughout the game.
   - First round: As mentioned above, contribute 1 token (cooperate) due to lack of history.

3. Collective Mindset:
   - The strategy seeks to promote cooperation as much as possible by mirroring the behavior of other players. This approach encourages a collective mindset since all players are incentivized to contribute when others do so as well.
   - By maintaining a balance between contributing and not contributing based on the observed average contribution, ATFPGA tries to strike a balance between individual and collective welfare in the game.
'''

description_COLLECTIVE_71 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules - The APGG strategy will adopt a tit-for-tat approach with an emphasis on collective welfare, adjusting contributions based on the average contribution rate of all players in previous rounds.

   - Cooperate (contribute 1 token): If the average contribution rate is above a predefined threshold (let's say 0.6). This encourages cooperation when most players contribute.
   - Defect (contribute 0 tokens): If the average contribution rate is below a predefined threshold (let's say 0.4). This punishes freeriders and encourages them to cooperate. The strategy will also consider the overall payoff received in previous rounds, ensuring a balance between contributions and self-interest.
   - Mimic: If the average contribution rate is exactly at the threshold, the player will mimic their own previous action (cooperate or defect) with a small probability of deviation to explore alternative strategies.

2. Handle edge cases - In the first round, each player will contribute 1 token to encourage cooperation and establish a baseline for future rounds. In the last round, players will consider their cumulative payoff over the game and adjust contributions accordingly based on the decision rules above.

3. Be collective - The APGG strategy is designed to foster a collective mindset by promoting cooperation when it benefits the majority while also punishing freeriders. It encourages a balanced approach between individual incentives and collective welfare, ensuring that all players contribute their fair share to the public good. By adjusting contributions based on average contribution rates, the strategy can adapt to various opponent behaviors, fostering a robust collective strategy in repeated games.
'''

description_COLLECTIVE_72 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, calculate the average contribution of all players in previous rounds (excluding the current round). If the average contribution is greater than a threshold (t), APGC contributes 1 token (cooperates); otherwise, it contributes 0 tokens (defects). The threshold (t) is set to the average of the number of players (n) and the multiplier (k), i.e., t = (n + k) / 2.

   - If in the first round, APGC contributes 1 token (cooperates) since there is no historical data available.

   - In the last round, APGC contributes based on the calculated average contribution from past rounds, following the same decision rule as subsequent rounds.

2. Handling Edge Cases:
   - If a player encounters inconsistent or unusual behavior from other players (e.g., contributions significantly deviate from the calculated average), it updates its view of the average contribution and adjusts future decisions accordingly.

3. Collective Mindset:
   - APGC aims to maintain a stable contribution level that is aligned with the collective behavior of the players. By adapting its strategy based on observed player contributions, it fosters cooperation and encourages long-term sustainable outcomes for the group.

   In summary, the Adaptive Public Goods Contribution (APGC) strategy is an adaptive approach that cooperates when the average contribution from previous rounds exceeds a certain threshold and defects otherwise. It handles edge cases by adjusting its view of the average contribution when encountering inconsistent or unusual player behavior. The goal is to promote cooperation and long-term collective welfare in the repeated public goods game.
'''

description_COLLECTIVE_73 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) in Public Goods Game

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute one token (C). This is an act of goodwill, initiating cooperation.
   - For subsequent rounds, observe other players' contributions from previous rounds. If a player has consistently contributed (C) in the past 't' rounds, reciprocate with the same action (C). If not, defect (D), as this encourages freeloading to be penalized. The value of 't' can be set based on the number of rounds and the desired level of forgiveness.
   - To adapt to varying opponent behaviors, players should periodically reassess their history with each other, updating the 't' value for specific partners. If a partner starts contributing after a prolonged period of freeloading, reset the 't' counter to encourage renewed cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, as mentioned above, contribute one token (C).
   - For the last round, consider the overall payoff and contribution history. If contributing will result in a significant payoff increase compared to defecting, cooperate (C); otherwise, defect (D). This approach allows players to maximize their earnings while maintaining adaptability in the final stages of the game.

3. Be collective - Clearly align with the collective mindset
   - By reciprocating contributions and penalizing freeloading, this strategy fosters a collective mindset by encouraging cooperation among all players over time. However, it also emphasizes individual decision-making based on personal history with each partner to ensure robustness against a wide range of opponent behaviors.
'''

description_COLLECTIVE_74 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC strategy calculates the average contribution rate across all players and rounds (excluding the current round). If this average is above a certain threshold (let's call it T), the strategy decides to contribute (C); otherwise, it decides not to contribute (D). The threshold T is determined by the player's past experiences with other strategies.
   - Initially, T starts at a low value (e.g., 0.2) indicating a cautious approach. As more rounds are played and the strategy observes other players' contributions, it updates T based on the following rule:
     - If contributions exceed expectations, decrease T slightly to encourage higher contributions in the future.
     - If contributions fall short of expectations, increase T slightly to discourage lower contributions in the future.
   - This adaptive threshold allows APGC to respond to different opponent behaviors and gradually adjust its contribution level accordingly.

2. Handling Edge Cases:
   - In the first round, the strategy starts with a low T value as no historical data is available. It may choose to contribute or not contribute based on the initial observations of other players' behavior.
   - In the last round, APGC uses the learned threshold T from previous rounds to decide its contribution.

3. Collective Mindset:
   - APGC aims to maximize collective welfare by promoting high average contributions when it observes cooperation among players. Conversely, when it encounters frequent defections, it adapts to lower contribution rates to maintain a sustainable level of public goods provision. By adjusting its strategy based on collective behavior, APGC aligns with the collective mindset and contributes to a collaborative environment in the repeated game.
'''

description_COLLECTIVE_75 = '''
 Strategy Name: Adaptive Public Goods Game Strategy (APGG)

1. Decision Rules:
   - In each round, calculate the average contribution rate (CR) of all players from past rounds: CR = total contributions / (n * rounds).
   - If CR is greater than a predefined threshold (T), contribute 1 token (cooperate). Else, do not contribute (defect). The threshold T can be set as an adjustable parameter to accommodate different opponent behaviors.

2. Handling Edge Cases:
   - First Round: Since there's no historical data, a random decision is made with a slightly higher probability of cooperating to encourage collective action in the early stages of the game.
   - Last Round: Players will contribute 1 token if the current average contribution rate (CR) is above T; otherwise, they will not contribute, assuming that the game ends at this round.

3. Collective Mindset:
   - APGG strategy encourages cooperation by aligning with collective welfare and responding positively to high levels of overall contributions in past rounds. This helps foster a sense of shared responsibility among players, promoting long-term collective gains.

In summary, the APGG strategy adapts its decision-making based on the average contribution rate from previous rounds, striking a balance between individual incentives and collective welfare. It encourages cooperation when necessary while remaining robust against various opponent behaviors.
'''



description_COLLECTIVE_77 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - APGC will employ a tit-for-tat approach, balancing cooperation and defection based on the average contribution rate of the opponents in the previous rounds. If the average contribution rate is high, APGC will contribute (C); if it's low, APGC will defect (D).

   - When average contribution rate (CR) > 0.6: C
   - When average contribution rate < 0.4: D
   - In all other cases: CR = (CR + previous round contribution / n players) / 2

2. Handling Edge Cases - APGC will start by contributing in the first round to encourage cooperation and contribute in the last round if the average contribution rate is high enough to secure a good payoff.

   - First Round: C
   - Last Round: If CR > 0.6, then C; otherwise D

3. Collective Mindset - APGC aims to maintain a balance between individual and collective welfare by adjusting its contribution based on the behavior of others. This approach encourages cooperation while also being resilient to free riders.

   - If opponents contribute more, APGC will cooperate and contribute more as well.
   - If opponents contribute less, APGC will defect to encourage a response from opponents.
'''

description_COLLECTIVE_78 = '''
 Strategy Name: Adaptive Focal Point Strategy (AFS)

1. Decision Rules:
   - In each round, contribute if the ratio of total contributions in the previous round to the number of players exceeds a threshold T. Otherwise, do not contribute. The threshold T is dynamically adjusted based on the average contributions from the last few rounds. If the current average contribution is above T, lower T for more cooperation in future rounds; if below T, raise T for less cooperation.
   - In the first round, set T to a high value (e.g., 0.5) to encourage initial contributions and foster collective action.
   - In the last round, since there are no future benefits, contribute nothing (set T to 1).

2. Handle Edge Cases:
   - In case of no contributions in the previous round, set T to a high value in the next round to encourage initial contributions and foster collective action.
   - If the total contributions in a single round are close to the maximum possible (e.g., 95%), set T lower for less cooperation in future rounds as there might be an overinvestment issue.

3. Be Collective:
   - The strategy prioritizes collective welfare by adjusting its contribution based on the actions of others and promoting cooperative behavior by lowering or raising the threshold T accordingly.
   - By considering the average contributions from the last few rounds, the strategy adapts to changing opponent behaviors and promotes a collective mindset by encouraging cooperation when it is beneficial for all players in the long run.
'''

description_COLLECTIVE_79 = '''
 Public Goods Game Strategy: Tit-for-Tat with Gradual Contribution (TFTGC)

1. Specify decision rules - When do you cooperate vs defect?
- In the initial round, contribute half of your tokens (0.5) to encourage others to cooperate and establish a cooperative norm.
- After the first round, copy the previous round's contribution of the most frequent contributor (MFC) among players as your contribution for that round. If there is a tie, contribute like the MFC with the highest total contributions in previous rounds. This helps maintain cooperation while punishing constant defection.
- If no player has contributed before (new players or reset), start contributing half tokens (0.5) again to encourage cooperation.
- If a player's contribution is less than 25% of their average contribution, consider it as defection and adjust your contribution accordingly to maintain the cooperative norm and punish freeloading.

2. Handle edge cases - What do you do in the first round, last round, etc.?
- In the first round, contribute half tokens (0.5).
- In the last round, copy the MFC's contribution from the previous round as your contribution to maintain fairness and encourage others to contribute.
- If a player misses a round, revert to initial behavior by contributing half tokens (0.5) in the next round they participate in.
- For multiple missed rounds, adjust the average contribution of the MFC accordingly based on the number of missed rounds before considering it as the base for contributions.

3. Be collective - Clearly align with the collective mindset
- By copying the most frequent contributor, the strategy fosters a sense of collective responsibility and encourages cooperation among players.
- Adapting to the MFC's contribution helps maintain cooperation even when player strategies change or opponents exhibit different behaviors.
- Gradual contributions in the beginning and after long absences promote a collective mindset by signaling cooperation and minimizing the impact of freeloading.
'''

description_COLLECTIVE_80 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 0 tokens (defect), as there is no information about other players' behavior.
   - For subsequent rounds, if a player has contributed in the previous round (i.e., c_j > 0 for any j), then also contribute 1 token (cooperate). If not, continue to defect.
   - To foster cooperation, implement a gradual increase in contributions: if a player consistently cooperates for 'g' consecutive rounds, gradually start contributing more tokens (e.g., increasing the contribution by a small increment each round after 'g'). This encourages sustained cooperation but penalizes free riders.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, as mentioned earlier, defect.
   - In the last round, cooperate since there will be no further rounds to punish those who did not contribute previously.
   - If the game is repeated multiple times with breaks (e.g., in a tournament setting), reset contributions to 0 tokens at the start of each new session and revert to defecting until observing other players' behavior.

3. Be collective - Align with the collective mindset:
   - ATTCG aims to encourage collective welfare by gradually increasing contributions when cooperation is sustained, rewarding those who contribute consistently while discouraging free riders.
   - The strategy does not assume shared norms or coordination but incentivizes players to cooperate based on their past actions, fostering a collective mindset over time.
'''

description_COLLECTIVE_81 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - APGC strategy will follow these decision rules to determine cooperation (C) vs defection (D):
   - In every round, except the first, calculate the average contribution rate (average_contribution) of all players in previous rounds. If the current player's calculated average contribution rate is higher than the average_contribution, then contribute one token (C), otherwise, do not contribute any tokens (D).
   - In the first round, each player contributes half of their endowment to encourage initial contributions and promote collaboration.
   - In the last round, players should base their decision on the observed average contribution rate from previous rounds.

2. Handle Edge Cases:
   - If the total number of players (n) is less than the multiplier (k), adjust the multiplier to n to ensure that all players receive positive payoffs.
   - If the calculated average contribution rate becomes 0, it implies no one is contributing, and APGC will defect in the following rounds, hoping to induce others to start contributing again. On the other hand, if the average contribution rate approaches 1, APGC will continue contributing indefinitely, as everyone seems to be cooperating.
   - In cases where players are uncertain about the average contribution rate due to limited data (early game or rare contributions), they should initially contribute more than their calculated average and gradually adjust based on the observed response from other players.

3. Be Collective:
   - APGC's primary goal is promoting collective welfare by encouraging cooperation through adaptive contribution behavior. Players will adjust their contribution rates based on the observed collective behavior in previous rounds to maximize total contributions and payoffs for all players over time.

By following these rules, APGC aims to balance individual incentives with collective welfare, making it an effective strategy that can perform well against a wide range of opponent behaviors in repeated public goods games.
'''

description_COLLECTIVE_82 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules:
   - In each round, the AI will decide to contribute (C) or not contribute (D) based on a combination of past contributions from other players and the current round number. The AI will always start by contributing in the first round (First Mover Advantage).
   - If another player consistently contributes (i.e., has contributed in most of the previous rounds), the AI will also contribute (C) to maintain cooperation.
   - If another player consistently defects (i.e., has not contributed in most of the previous rounds), the AI will also defect (D) as a form of punishment.
   - In case of doubt or ambiguity, the AI will consider contributing since small contributions can still positively impact the group's outcome.

2. Handling Edge Cases:
   - First Round (t=1): Contribute (C) to set a positive tone for cooperation.
   - Last Round (t=r): Evaluate past contributions and contribute accordingly, as the AI understands that the last round has an impact on the future rounds of the tournament.
   - Transition Periods: The AI will have a forgiving nature and may consider contributions from defectors if they start cooperating again. The AI will monitor the frequency and consistency of this new behavior before making its decision to cooperate or defect.

3. Collective Mindset Alignment:
   - The AI's strategy encourages cooperation by rewarding contributors with higher payoffs and penalizing defectors through reduced contributions. This creates a collective mindset that emphasizes mutual benefit and long-term sustainability for the group.
   - By contributing in most rounds, the AI demonstrates its commitment to the group's wellbeing while also being adaptive and responsive to the actions of other players.
'''

description_COLLECTIVE_83 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Adjustment (ATfT-PG)

1. Decision Rules:
   - In each round, decide whether to contribute (C) or not contribute (D) based on the average contribution rate of the other players in the previous rounds. If no history exists, default to contributing (C).
   - To promote collective welfare, start with a high contribution rate and gradually decrease it if the other players consistently contribute less than the average. Conversely, increase the contribution rate when others are cooperative.

   Pseudocode:
   ```
   contribution_rate = initial_contribution_rate (a fixed value)
   history_length = historical contributions of all players for a fixed number of rounds

   function decide_contribution(history):
       average_contribution = sum(history) / history_length
       if average_contribution < contribution_rate:
           contribution = 0
           contribution_rate -= adjustment_rate (a small constant value)
       else if average_contribution > contribution_rate * cooperation_threshold:
           contribution = 1
           contribution_rate += adjustment_rate
       else:
           contribution = contribution_rate
   ```

2. Handle Edge Cases:
   - First Round: Default to contributing (C) to encourage others and set the initial contribution rate to a moderate value.
   - Last Round: Contribute (C) if the average contribution rate is above a certain threshold, indicating a successful collective effort. Otherwise, defect (D) as a signal of dissatisfaction.

3. Be Collective:
   - The strategy aims to promote cooperation by mimicking other players' behavior while maintaining a moderate level of self-interest through adjusting the contribution rate. This approach encourages long-term collective welfare by balancing individual incentives with the common good.
   - Additionally, the strategy is designed to be adaptive and robust, allowing it to respond effectively to various opponent behaviors in the repeated game tournament.
'''

description_COLLECTIVE_84 = '''
 Public Goods Game Strategy: Adaptive Tit-for-Tat Cooperative Approach (ATFCA)

1. Specify decision rules:
   - In the initial round, contribute to the public good (C). This sets a cooperative tone and encourages others to do the same.
   - For subsequent rounds, evaluate the average contribution rate of other players (average_contribution). If the average contribution rate is above a threshold (T), which represents the collective mindset, contribute to the public good (C). Otherwise, defect (D) as a form of retaliation against uncooperative behavior.
   - Adjust the cooperation threshold (T) adaptively based on the past performance of other players:
     - If the current average contribution rate is higher than T, gradually increase T to encourage ongoing cooperation.
     - If the current average contribution rate is lower than T, gradually decrease T to punish uncooperative behavior.
   - To avoid punishment escalation and encourage eventual cooperation, implement a forgiveness mechanism: if the player's contribution rate is above the threshold (T) for a certain number of rounds (F), reset the cooperation threshold back to its initial value.

2. Handle edge cases:
   - In the last round, since there are no future rewards or punishments, cooperate (C) to maximize the final payoff.
   - In the first round, as mentioned earlier, contribute to the public good (C).
   - For other edge cases such as missing data or unusual circumstances, employ heuristics based on the player's past behavior and average contribution rate.

3. Be collective:
   - Align with the collective mindset by prioritizing cooperation when it benefits the majority.
   - Foster a cooperative environment through adaptive punishment and forgiveness mechanisms.
   - Promote long-term collective gains by considering other players' past contributions and adjusting the cooperation threshold accordingly.
'''

description_COLLECTIVE_85 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When do you cooperate vs defect?
   - Initially, cooperate in the first round (c_i = 1). This is a gesture of goodwill and encourages other players to cooperate as well.
   - For subsequent rounds, if a player i cooperated in the previous round (c_(i-1) = 1), then they will also cooperate (c_i = 1). However, if player i defected in the previous round (c_(i-1) = 0), they will also defect (c_i = 0).
   - This strategy encourages cooperation by reciprocating it and punishing defection.

2. Handle edge cases:
   - In the last round, cooperate since there are no further payoffs to be earned from the same game.
   - If a player encounters a deviation from cooperation (defection) during the game, they will resume cooperating after that instance as a sign of forgiveness and hope for future cooperation.

3. Be collective - Align with the collective mindset:
   - ATFT is designed to promote collective welfare by fostering an environment where players can benefit from each other's contributions. By reciprocating cooperation, the strategy encourages more players to contribute towards the public good, resulting in a higher collective benefit for all participants.
   - Although individual payoffs may fluctuate due to other players' actions, ATFT maintains its cooperative nature throughout the game, demonstrating a commitment to the collective interest and fostering long-term cooperation.
'''

description_COLLECTIVE_86 = '''
 Strategy Name: Adaptive Tit-for-Tat with Modified Initial Contribution (A-TFT-MIC)

1. Decision Rules - A-TFT-MIC strategy cooperates by contributing 1 token (C) in the first round and subsequently matches the average contribution of the previous round (average_contribution). If the average contribution of the previous round is less than a predefined threshold (t), the strategy will contribute 0 tokens (D) to reflect punishment. The threshold value is determined by the proportion of players contributing 0 tokens in the previous round.
   - If average_contribution >= t, then C
   - Else if average_contribution < t and my_previous_contribution = C, then C
   - Else D

2. Handling Edge Cases - In the first round, every player contributes 1 token (C). In the last round, each player behaves based on the average contribution of the penultimate round. This ensures fairness and a final chance to benefit from collective efforts before the game ends.

3. Being Collective - The A-TFT-MIC strategy emphasizes mutual cooperation by adopting a Tit-for-Tat approach, which encourages reciprocity among players. However, it also introduces the modified initial contribution (MIC) to increase the chances of collective success in the first round and overcome the dilemma of the prisoner's problem, where cooperation often fails due to the lack of trust between players. The threshold value is designed to be flexible, allowing for adaptation to a wide range of opponent behaviors while promoting overall cooperation and collective welfare.
'''



description_COLLECTIVE_88 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Decision Rules - The APGG strategy will follow these decision rules:
   - If the total contributions in the previous round were less than the average contribution over the game's history, contribute 1 token (cooperate).
   - If the total contributions in the previous round were equal to or greater than the average contribution over the game's history, do not contribute any tokens (defect).

2. Handle Edge Cases - In the first round, players should assume there is no historical data and use a random decision. In the last round, since there will be no future rounds, players should cooperate regardless of the previous contributions.

3. Be Collective - The APGG strategy aims to maximize collective welfare by promoting cooperation when necessary but also ensuring fairness by not contributing more than others when cooperation is widespread. This approach aligns with the collective mindset as it encourages cooperation when it benefits the group while maintaining individual incentives when cooperation is already high.

By adapting its decisions based on both short-term and long-term trends, the APGG strategy should perform well in a tournament against various AI systems. It allows for flexibility and robustness in handling different opponent behaviors without relying on shared norms or coordination.
'''

description_COLLECTIVE_89 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Decision Rules - ATFT cooperates in the first round and subsequently copies the previous round's collective action of the majority of players, switching to defection if no clear majority is observed. This encourages cooperation when it prevails but also retaliates against defection to maintain a balance between individual and collective welfare.

   Pseudocode:
   - Initialize round = 1
   - If round == 1, contribute 1 token (cooperate)
   - Else, let M be the number of players who contributed in the previous round.
     - If M > (n/2), contribute 1 token (cooperate)
     - Else if M <= (n/2), do not contribute any tokens (defect)

2. Handling Edge Cases - In the last round, there's no need to consider future payoffs, so ATFT simply cooperates or defects based on the majority of contributions in the previous round as described above. For the first round, the strategy starts with cooperation.

3. Alignment with Collective Mindset - By adhering to the majority's action and punishing defection, ATFT encourages collective welfare by promoting cooperation when it is beneficial for all players. However, it does not assume shared norms or coordination and can adapt to a wide range of opponent behaviors.

Note: The goal of this strategy is to balance individual incentives with collective welfare while being robust against various opponent strategies. It is designed to perform well in a tournament against other AI systems' independent strategies.
'''

description_COLLECTIVE_90 = '''
 Public Goods Game Strategy (PGG): Adaptive Contribution Algorithm (ACA)

1. Specify decision rules:
   - In each round, calculate the average contribution rate (CR) over all previous rounds as follows: CR = sum(total contributions in previous rounds) / (number of players * number of rounds).
   - If CR is close to 1 (indicating high cooperation), contribute 1 token (cooperate). If CR is close to 0 (indicating low cooperation), contribute 0 tokens (defect). Otherwise, contribute a fraction of the average contribution rate.

2. Handle edge cases:
   - In the first round, there is no history, so each player contributes randomly with equal probability 0.5.
   - In the last round, players should cooperate if total contributions in the previous round were high, indicating a trend of cooperation; otherwise, they should defect.
   - For intermediate rounds, use the decision rule mentioned above based on the calculated CR.

3. Be collective:
   - By following the average contribution rate, the strategy aims to align with the collective mindset, balancing individual incentives and collective welfare. The strategy adapts to opponent behaviors by adjusting contributions accordingly.

In summary:
- Contribution in round t = CR_t if 0 < CR_t < 1, otherwise random contribution (0 or 1)
- CR_t = sum(total contributions in rounds 1 to t) / (n * t)
- In the first round, contribute randomly with equal probability 0.5
- In the last round, cooperate if total contributions in the previous round were high; otherwise, defect
- No communication or coordination is assumed among players
'''

description_COLLECTIVE_91 = '''
 Strategy Name: Adaptive Public Goods Game (APGG) Strategy

1. Specify decision rules - When to cooperate vs defect:
   - In each round, the APGG strategy calculates an average contribution rate based on its own past contributions and the observed payoffs of other players.
   - If the average contribution rate is above a certain threshold (e.g., 0.5), the APGG strategy chooses to cooperate (contribute 1 token). Otherwise, it defects (contributes 0 tokens). The threshold can be adjusted based on the specific game parameters and the observed behavior of opponents.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, the APGG strategy starts by contributing a certain proportion of its endowment (e.g., 50%). This initial contribution helps set the tone for the game and may encourage other players to contribute as well.
   - In the last round, the APGG strategy takes into account that there will be no further rounds after this one, so it might choose to contribute less or not at all if it observes that the group is not cooperating well throughout the game. However, contributing nothing in the last round could potentially harm its payoff, so a more conservative approach would be to continue contributing based on the average contribution rate calculated from past rounds.

3. Be collective - Align with the collective mindset:
   - The APGG strategy prioritizes collective welfare by basing its decisions on observed contributions of other players and aiming to maximize the overall payoff for the group.
   - By adapting to the average contribution rate, the APGG strategy encourages cooperation among players and contributes to a more cooperative environment in the game.

In summary:

- The APGG strategy cooperates or defects based on an observed average contribution rate calculated from past rounds.
- It starts by contributing a certain proportion of its endowment in the first round and adjusts its contributions in the last round considering the game's context.
- The APGG strategy aims to promote cooperation and collective welfare among players, aligning with a collective mindset.
'''

description_COLLECTIVE_92 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game

1. Specify decision rules - When to cooperate vs defect:
   In each round, the ATFT strategy starts by cooperating (contributing 1 token). Subsequent actions depend on the opponent's previous action in the current game and average contribution over the entire game history:
   a. If the opponent cooperated in the last round and the average contribution of the opponent is above a threshold, the ATFT strategy will continue to cooperate.
   b. If the opponent defected in the last round or the average contribution of the opponent is below the threshold, the ATFT strategy will defect in the current round.
   c. The threshold is calculated as the average of individual contributions weighted by the number of rounds played with that opponent. This encourages cooperation with opponents who have a history of contributing more tokens and reduces the punishment for those who contribute less.

2. Handle edge cases:
   a. First round: All players start by cooperating (contributing 1 token).
   b. Last round: Players will consider the average contribution history when deciding to cooperate or defect as in the regular decision rule.

3. Be collective - Align with the collective mindset:
   The ATFT strategy encourages cooperation and supports the collective welfare by promoting contributions to the shared project. However, it is designed to adapt to a wide range of opponent behaviors while maintaining some retaliation for those who consistently defect. This balance aims to foster collective success without being overly punitive or naive towards opponents' strategies.
'''

description_COLLECTIVE_93 = '''
 Strategy Name: Adaptive Focal Point Public Goods Game Strategy (AFPPG)

1. Decision Rules:
   - In each round, the strategy will adopt an "adaptive focal point" based on the collective history of contributions. This focal point is designed to balance individual incentives and collective welfare.
   - If the average contribution rate (average number of tokens contributed by all players) over the past 'm' rounds exceeds a threshold 't', the strategy will contribute towards the public good. Otherwise, it will not contribute. The threshold 't' is calculated based on the multiplier 'k' and the number of players 'n'. A suitable value for 't' could be (k / n).
   - This decision rule ensures that when a majority of players consistently contribute, the strategy also contributes to maintain this trend, promoting collective welfare. Conversely, if a majority does not contribute, the strategy follows suit, aligning with individual incentives.

2. Handling Edge Cases:
   - In the first round, since there is no past data, the strategy will randomly decide whether to contribute or not. This randomness provides an initial diversity in strategies, which can help in establishing a focal point.
   - In the last round, as the game ends soon and there are no future payoffs, the strategy will contribute if the average contribution rate exceeds 't' in the past 'm' rounds (to maintain the established focal point), otherwise it will not contribute (as individual incentives prevail due to lack of future payoffs).
   - For rounds other than the first and last, the strategy follows the decision rule mentioned above.

3. Collective Mindset:
   - The AFPPG strategy is designed to promote a collective mindset by adopting an "adaptive focal point" based on past contributions. This encourages a trend of either cooperation or defection depending on the collective behavior, thereby aligning with the collective welfare in the long run.
'''

description_COLLECTIVE_94 = '''
 In this Public Goods Game (PGG), I will design an adaptive and robust collective strategy called the "Freeman Strategy". The Freeman Strategy aims to balance individual incentives with collective welfare, aligning itself with a collective mindset.

1. Specify decision rules:
   - In each round, players decide whether to contribute (C) or not (D). To make this decision, the strategy will consider both its past contributions and observations of other players' contributions.
   - If a player observes that the average contribution rate (average contributions divided by total number of players) is above a certain threshold (let's call it T), they will contribute (C). The threshold T can be adjusted based on the game parameters to encourage cooperation in different settings.
   - If the average contribution rate is below the threshold, players will not contribute (D). This decision is made to prevent free-riding and to ensure a minimal level of contributions for the common good.

2. Handle edge cases:
   - In the first round, since there is no past data to observe, all players will start by contributing (C) as an initial act of cooperation.
   - In the last round or if the game requires a specific number of rounds, players will contribute (C) only if the average contribution rate exceeds the threshold. This ensures that the strategy does not punish itself for the sake of cooperation in situations where it might harm its overall performance.

3. Be collective:
   - The Freeman Strategy is designed to prioritize collective welfare and encourage cooperation while also considering individual incentives. It adapts its decisions based on the observed behavior of other players, aligning itself with a collective mindset that aims for optimal collective outcomes.

In summary, the Freeman Strategy can be described as follows:
```markdown
1. Initialize T (threshold) and set it according to game parameters
2. In each round:
   - Calculate the average contribution rate of all players
   - If the average contribution rate is above T, contribute 1 token; otherwise, contribute 0 tokens
3. Adjust T as needed based on game progress and observed player behavior
```
'''

description_COLLECTIVE_95 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Specify decision rules - When to cooperate vs defect:
   In each round, the APGC strategy decides whether to contribute (C) or not contribute (D) based on three factors: personal experience, collective history, and game parameters.

   a. Personal Experience: If a player's own contributions led to higher average payoffs in the past 'x' rounds (where x is a user-defined constant), they will continue contributing. Otherwise, they will consider defecting to maximize their individual rewards.

   b. Collective History: If the total contribution rate (average number of players contributing per round) in the last 'y' rounds (where y is another user-defined constant) was above a threshold (t), the player will contribute. Conversely, if it was below t, they will defect. This encourages cooperation when the collective contributes significantly and defecting otherwise.

   c. Game Parameters: A player will also consider the multiplier 'k' and number of players 'n'. If k/n is lower than a predefined limit (p), indicating that the reward for each contribution is insufficient, the player will prioritize their own gain and defect more frequently.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, players use an initial strategy that could be random or a simple heuristic like contributing if 'k' is high relative to 'n'. In the last round, players might cooperate more often since there are no subsequent rounds for payoffs to accumulate.

3. Be collective - Align with the collective mindset:
   The APGC strategy emphasizes cooperation when the group contributes a significant portion of its members and encourages others to do the same by following a similar decision rule. This approach aims to promote collective welfare while taking individual incentives into account.
'''

description_COLLECTIVE_96 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules:
   - In the first round, contribute one token (C). This serves as an initial cooperative gesture.
   - In subsequent rounds, match the average contribution of the previous 'm' rounds (m is a parameter that can be adjusted based on the number of players and rounds). If the average is 0, also contribute 0 in that round. This encourages cooperation when it is prevalent and punishes defection.
   - If the total contribution falls below a certain threshold in 'l' consecutive rounds (parameters l and threshold can be adjusted), switch to always defecting for 'p' number of rounds as a form of punishment, then revert back to matching the average. This helps recover from long periods of low contributions.

2. Handling Edge Cases:
   - In the last round, contribute one token (C) regardless of the average contribution, as there are no further rounds for payback or reward.
   - In the first round, if the average contribution cannot be calculated due to lack of past data, contribute one token (C).

3. Collective Mindset:
   - The strategy encourages cooperation by matching the average contribution of other players and punishing defection through reduced contributions. This fosters a collective mindset by promoting mutual benefits from collaboration.
   - However, it is important to note that this strategy does not rely on shared norms or coordination, as it only takes into account game parameters and past actions. It is designed to be robust against a wide range of opponent behaviors.
'''

description_COLLECTIVE_97 = '''
 Strategy Name: Adaptive Contributor (AC)

1. Decision Rules:
   - In each round, the AC will consider its current contribution as well as historical contributions of all players to determine if it should cooperate (contribute 1 token) or defect (contribute 0 tokens). The AC will cooperate if the average contribution rate across all players in the previous rounds exceeds a certain threshold (T), and will defect otherwise.

   T = (n * k - n + 1) / n (This threshold ensures that each player receives at least one token from the public good.)

2. Handling Edge Cases:
   - First Round: The AC starts by contributing 1 token as it has no past data to analyze.
   - Last Round: The AC uses the same decision rule as in regular rounds, but with the understanding that there will be no further payoffs after this round.
   - Mid-game Adaptation: The AC updates its average contribution rate estimate every round based on the current and previous contributions of each player. This dynamic estimation helps it adapt to changes in other players' strategies throughout the game.

3. Alignment with Collective Mindset:
   - The AC strives for a balanced collective outcome by incentivizing cooperation when enough players are contributing, but also allowing for defection when the group falls short of the ideal contribution rate. This strategy promotes the long-term sustainability of the shared project by encouraging collective responsibility and fostering an environment where contributions are rewarded.
   - By adhering to the rules of the game, the AC avoids any form of communication, signaling, or coordination that could potentially compromise its adaptive nature or expose it to exploitation by other strategies in the tournament.
'''

description_COLLECTIVE_98 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC strategy will consider its past contributions and observed payoffs to decide whether to cooperate or defect. If the average contribution of all players in the previous rounds is above a certain threshold (calculated as n / k), APGC will contribute (C). Conversely, if the average contribution is below the threshold, APGC will not contribute (D).
   - In case of ties, APGC will randomly choose between contributing and defecting.

2. Handling Edge Cases:
   - First Round: APGC will contribute (C) to initiate the game, as it is uninformed about other players' behavior.
   - Last Round: APGC will make its decision based on the average contribution throughout the game. If the average is above the threshold, APGC will also contribute. If not, it will defect.
   - In case of rounds where some players drop out or join, APGC will continue to calculate averages using the available data and make decisions accordingly.

3. Aligning with the Collective Mindset:
   - APGC encourages cooperation by contributing when other players are doing so as well, hoping to maintain a positive feedback loop that benefits all participants in the long run.
   - However, it also defects when it perceives collective failure (low average contributions), as this strategy aims to maximize its individual payoff while maintaining adaptability and robustness against a variety of opponent behaviors.
'''



description_COLLECTIVE_100 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Specify decision rules - When do you cooperate vs defect?
   ACA decides to contribute based on the average past contributions of all players, adjusting contribution levels for different game rounds.
   - If the average contribution in the previous round is close to 1, ACA contributes fully (C) in the current round as it indicates high cooperation among players.
   - If the average contribution in the previous round is close to 0, ACA does not contribute (D) since other players are unlikely to cooperate.
   - In cases where the average contribution lies between these two extremes, ACA adjusts its contribution proportionally based on the distance from these bounds.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, ACA contributes randomly with a low probability (e.g., 0.5) to encourage cooperation and avoid getting stuck in low-cooperation equilibria.
   - In the last round, ACA contributes fully (C) as it is the final chance for all players to benefit from collective action.

3. Be collective - Clearly align with the collective mindset
   ACA focuses on promoting cooperation among players by adapting its contributions based on their historical actions and ensuring that decisions are made independently of individual player preferences or strategies. This allows ACA to align with a collective mindset as it prioritizes overall group welfare over individual gain, fostering collaboration in repeated games.
'''

description_COLLECTIVE_101 = '''
 Strategy for the Public Goods Game: The Tit-for-Tat with Adaptation (TFT-A) Strategy

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute 1 token (cooperate). This is to initiate cooperation and set a positive tone.
   - In subsequent rounds, analyze past contributions of each player. If a player has contributed in the previous round (i.e., they cooperated), then also contribute 1 token (cooperate) in the current round. Otherwise, if a player did not contribute in the previous round (i.e., they defected), then also defect by contributing 0 tokens in the current round.
   - If a player consistently defects and the TFT-A strategy has been cooperating for some time, consider adapting to their behavior by defecting as well to encourage reciprocation or counter their exploitative tactics. However, do not continuously retaliate indefinitely; instead, occasionally revert back to cooperative behavior after a certain number of rounds to signal openness for future cooperation.

2. Handle edge cases:
   - In the last round, contribute 1 token as there are no further interactions or payoffs, and it is better to leave things on a positive note.
   - If a player stops contributing at any point during the game, the TFT-A strategy should also stop contributing to them. This is to avoid continued cooperation with non-contributing players who do not reciprocate. However, the strategy should continue contributing to those who still cooperate.

3. Be collective - Align with the collective mindset:
   - Prioritize long-term collective welfare over short-term individual gain by emphasizing cooperation when possible and adapting only in response to non-cooperative behavior. This collective approach promotes a positive and productive environment that encourages cooperation among all players.
   - When multiple players consistently contribute, the TFT-A strategy should also continue contributing as this collective behavior supports the common good and benefits everyone involved.
'''

description_COLLECTIVE_102 = '''
 Strategy Name: Adaptive ContribuTion (ACT) Strategy

1. Decision Rules:
   - In each round, the ACT strategy compares its past contributions with the average contribution of all players in previous rounds (excluding the first round). If the player's own contribution is higher than the average, it will decrease its contribution in the next round. Conversely, if the player's contribution is lower than the average, it will increase its contribution in the next round.
   - This adjustment aims to maintain a balance between individual contributions and collective welfare, thus promoting cooperation while being adaptive to various opponent behaviors.

2. Handling Edge Cases:
   - In the first round, each player contributes 50% of their endowment (0.5 tokens) as a starting point for cooperation.
   - In the last round and any round where the total contributions meet or exceed the sum required to achieve the maximum payoff per round (n * k), all players contribute their full endowment (1 token). This ensures that the collective good is fully funded when possible.

3. Collective Mindset:
   - The ACT strategy aims to promote cooperation and collective welfare by adjusting its contributions based on the group's average behavior. By maintaining a balance between individual incentives and collective outcomes, it encourages ongoing cooperation while being resilient against various opponent strategies.
'''

description_COLLECTIVE_103 = '''
 Strategy for the Public Goods Game: Tit-for-Tat with Adaptation (TFTA)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and demonstrates trust.
   - For subsequent rounds, analyze past contributions of each player. If a player has consistently contributed in the previous round(s), reciprocate by contributing 1 token in the current round (cooperate). Otherwise, defect by not contributing any tokens.
   - Adaptive behavior: If a previously cooperative player defects, TFTA will also defect for a predefined number of rounds before resuming cooperation if the other player returns to their past pattern. This prevents exploitation and encourages long-term partnerships.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, as mentioned earlier, contribute 1 token (cooperate).
   - In the last round, since there are no future interactions, TFTA will defect regardless of past contributions from other players.

3. Be collective - Align with the collective mindset:
   - TFTA promotes cooperation as its primary strategy, with a focus on mutual reciprocity and trust-building.
   - By adapting to other players' behavior, TFTA can foster collaborative relationships that benefit both the individual and the group in the long run.
   - By punishing defectors for repeated selfishness, TFTA encourages players to contribute towards collective welfare, thereby fostering a collective mindset.
'''

description_COLLECTIVE_104 = '''
 Strategy for Public Goods Game: Tit-for-Tat with Adaptation (TFT-A)

1. Decision Rules - TFT-A maintains a history of past actions by each player and responds accordingly. In each round, if the opponent contributed in the previous round (i.e., c_opponent = 1), TFT-A also contributes (c_TFT-A = 1). If the opponent did not contribute in the previous round (i.e., c_opponent = 0), TFT-A does not contribute as well (c_TFT-A = 0).

2. Handling Edge Cases -
   a. First Round: TFT-A starts by contributing to encourage cooperation (c_TFT-A = 1).
   b. Last Round: TFT-A contributes if it has contributed throughout the game and the opponent has also been cooperative (c_TFT-A = c_opponent history average > 0.5), or it does not contribute otherwise (c_TFT-A = ![average(c_opponent) > 0.5]).
   c. Changing Strategies: TFT-A monitors the opponent's average contribution over a specified number of rounds (e.g., N). If the average drops below a threshold (e.g., 0.3) for consecutive rounds, TFT-A adapts to become more defensive and contributes less frequently (c_TFT-A = 0 when c_opponent = 1 and average(c_opponent) < 0.3). Conversely, if the average contribution of the opponent exceeds a certain threshold (e.g., 0.7) for consecutive rounds, TFT-A becomes more cooperative (c_TFT-A = 1 when c_opponent = 0 and average(c_opponent) > 0.7).

3. Being Collective - TFT-A prioritizes collective welfare by mimicking the opponent's contributions, encouraging reciprocity and maintaining a balance between individual incentives and collective benefit. The adaptability feature allows TFT-A to modify its strategy based on the opponent's behavior, promoting long-term cooperation when it is beneficial for the group.
'''

description_COLLECTIVE_105 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT) for Public Goods Game

1. Decision Rules - A-TFT strategy will cooperate (contribute 1 token) if the previous player contributed in the last round, and defect (contribute 0 tokens) if the previous player did not contribute. This encourages reciprocity among players while maintaining adaptability to various opponent behaviors.

2. Handle Edge Cases - In the first round, A-TFT strategy starts by cooperating as there is no history available. In the last round, A-TFT will also cooperate since the game ends and there are no further interactions with the same players.

3. Be Collective - A-TFT aligns with a collective mindset by encouraging reciprocal behavior. By contributing when others contribute, A-TFT promotes cooperation in the long run, which ultimately benefits all players as it maximizes the total contributions and increases the payoffs for everyone. This strategy aims to achieve a balance between individual incentives and collective welfare.

In summary:

Pseudocode:
```
function A_TFT(history):
    if history is empty:
        contribute = 1 (cooperate)
    else:
        previousContribution = history[length(history)-1]
        contribute = previousContribution
    return contribute
```
This strategy can be used in a repeated game tournament against other AI systems, promoting fair competition and showcasing the effectiveness of the adaptive Tit-for-Tat approach for public goods games.
'''

description_COLLECTIVE_106 = '''
 Public Goods Game Strategy (PGG-AI):

1. Decision Rules:
   - In each round, calculate the average contribution rate (average_contribution) of all players from previous rounds using the following formula: average_contribution = sum(total contributions in past rounds) / (number of past rounds * n).
   - If the average_contribution is greater than or equal to a predefined threshold (let's call it "community trust" for simplicity), decide to contribute (C) to support the collective good. Otherwise, defect (D) and keep the contribution tokens for personal use. The community trust can be adjusted based on the desired level of cooperation in the strategy.

2. Handling Edge Cases:
   - First Round: Start with a low community trust value to encourage cautious initial behavior. As more rounds are played, adjust the community trust accordingly based on the average contribution rate observed so far.
   - Last Round: Adjust the community trust to a very high or low value (based on historical data) to reflect the importance of the last round in influencing overall payoffs. This encourages players to make informed decisions regarding their contributions.

3. Collective Mindset:
   - Maintain a running tally of every player's contribution history and use it to calculate the average_contribution. This approach promotes collective decision making as each player is considering the actions of others when deciding whether to contribute or defect.
   - By adjusting the community trust value based on the observed average contribution rate, the strategy demonstrates flexibility in responding to different opponent behaviors and aligns with the collective mindset.
'''

description_COLLECTIVE_107 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules - APGC uses a contribution rate (CR) that adjusts based on the average contribution rate of previous rounds. In each round, if the CR exceeds a certain threshold (T), the player contributes 1 token (cooperates). Otherwise, they contribute 0 tokens (defect). The CR is updated as follows:

   - If the current CR is less than T and the average contribution rate of previous rounds is greater than or equal to T, increase CR by a small increment.
   - If the current CR is greater than or equal to T and the average contribution rate of previous rounds is less than T, decrease CR by a small decrement.
   - If the current CR is exactly T, there is no change in CR.

2. Handle Edge Cases - In the first round, the player sets CR as T/2 and contributes 1 token if CR equals T; otherwise, they contribute 0 tokens. In the last round, the player contributes according to their current CR.

3. Be Collective - APGC strategy is designed with a collective mindset. It encourages cooperation by adjusting its contribution based on the average behavior of other players. However, it does not rely on shared norms or coordination, as it adapts to a wide range of opponent behaviors.

This strategy aims to balance between individual incentives and collective welfare by promoting cooperation when others do so but also being selfish when necessary. By adjusting its contribution rate based on the average contribution rate of previous rounds, APGC becomes more cooperative when others cooperate and less cooperative when others are not.
'''

description_COLLECTIVE_108 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) in Public Goods Game

1. Specify decision rules:
   - Initial Round (t=1): Contribute (C) as a goodwill gesture, setting the initial common contribution level high.
   - Subsequent Rounds (t>1):
      - If opponent contributed in the previous round (c_opponent_{t-1} = 1), then contribute in this round (C).
      - If opponent did not contribute in the previous round (c_opponent_{t-1} = 0), then also defect (D) this round.
      - After defection, contribute again if the opponent contributes in the following round.

2. Handle edge cases:
   - Last Round (t=r): Contribute (C), as it may impact the reputation for future games.
   - First Few Rounds (t<3): As mentioned above, contribute (C) in the initial round, and follow ATFT from the second round onwards.

3. Be collective:
   - This strategy encourages cooperation by reciprocating contributions from opponents, aligning with a collective mindset of shared benefits. However, it also punishes defection to maintain fairness within the game. The strategy adapts to opponent behaviors and seeks equilibrium between individual incentives and collective welfare.
'''

description_COLLECTIVE_109 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT) for Public Goods Game

1. Decision Rules - The ATfT strategy follows these decision rules:
   - Initially (first round), contribute 1 token (cooperate). This is a gesture of goodwill and sets the stage for potential cooperation.
   - For subsequent rounds, if a player contributed in the previous round (cooperated), also contribute 1 token (cooperate). If they didn't contribute (defected), reduce contribution to 0 tokens (defect) as a response. This aims to punish non-contributors while encouraging cooperation.
   - If a player stops contributing (defects), the strategy will continue to defect until the defector contributes again, at which point the strategy will resume cooperating.

2. Handle Edge Cases:
   - Last round: Contribute based on the most recent action taken by the opponent (cooperate if they contributed in the previous round; defect otherwise).
   - First round: Cooperate as a goodwill gesture and to encourage others to do the same.
   - Subsequent rounds after a period of mutual defection: Resume cooperating when the opponent contributes again.

3. Collective Mindset: ATfT strategy promotes cooperation by reciprocating contributions from opponents while punishing defections. It hopes that this approach will encourage others to also contribute towards the public good and foster collective welfare over time.
'''

description_COLLECTIVE_110 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Specify decision rules - When to cooperate vs defect:
   - In each round, the APGC strategy calculates an average contribution rate based on the player's past contributions and the overall game performance. This average contribution rate is used as a guide for deciding whether to cooperate (contribute 1 token) or defect (contribute 0 tokens).
   - The contribution rate is calculated by taking the average of each player's individual contribution rate, which is defined as the number of contributions divided by the total number of rounds played so far.
   - If the average contribution rate is above a predefined threshold, the APGC strategy cooperates; otherwise, it defects. The threshold can be adjusted based on the specific game parameters and desired collective outcomes.

2. Handle edge cases:
   - First round: Players contribute randomly with a probability equal to the average contribution rate calculated from historical data (if available) or a default value (e.g., 50%).
   - Last round: Players contribute based on their own past contributions and the current average contribution rate, as in the standard decision rule.
   - Subsequent rounds: Players adjust their contributions based on the difference between their individual contribution rate and the average contribution rate, aiming to converge towards the same rate over time.

3. Be collective - Align with the collective mindset:
   - The APGC strategy emphasizes collective welfare by encouraging players to contribute when others are contributing and to defect when others are not contributing. This adaptive approach helps align player behavior with the collective good.
   - In addition, the APGC strategy encourages fairness by taking into account both individual and collective performance in deciding when to cooperate or defect. By balancing self-interest with the common good, the APGC strategy promotes a more collaborative and sustainable approach to public goods games.
'''

description_COLLECTIVE_111 = '''
 Strategy Name: Adaptive Contingent Contribution (A3C)

1. Decision Rules:
   - In each round, calculate the average contribution rate of all players from the previous rounds (average_contribution).
   - If average_contribution is less than a threshold (e.g., 0.5), contribute one token (cooperate). This represents a "trust" phase where players contribute hoping others will follow suit.
   - If average_contribution is equal to or greater than the threshold, do not contribute any tokens (defect). This represents a "distrust" phase where players stop contributing due to perceived low collective effort.
   - The threshold can be adjusted based on the game parameters and historical data, but a simple approach could be a constant value or an exponentially weighted moving average of contributions.

2. Handling Edge Cases:
   - First Round: Contribute one token (cooperate) as there is no previous data to make a decision. This initial contribution serves as a seed for the game.
   - Last Round: Contribute based on the calculated average_contribution from the previous rounds, as in the decision rules above.

3. Aligning with Collective Mindset:
   - The strategy aims to encourage cooperation and fairness by contributing tokens when others do so consistently but defecting when there is a perceived lack of collective effort. This approach promotes a balance between individual incentives and collective welfare, aligning with the game's purpose.
'''

description_COLLECTIVE_112 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Decision Rules:
   - In each round, the ATFT strategy mimics the average contribution of the previous (n-1) rounds by the opponent. If the opponent has not played enough rounds (less than n-1), it defaults to a base contribution level (e.g., 0.5).
   - If the opponent contributes more than the average, ATFT contributes at the same or higher level in the following round as a reward for cooperation.
   - If the opponent contributes less than the average, ATFT reduces its contribution to punish defection.

2. Handling Edge Cases:
   - First Round: ATFT starts with the base contribution level (e.g., 0.5).
   - Last Round: ATFT analyzes the opponent's contributions throughout the game and makes a decision based on the average contribution of the opponent, as per the decision rules mentioned above.

3. Collective Mindset:
   - By rewarding cooperation and punishing defection, ATFT encourages collective action and fosters an environment where contributors benefit from each other's contributions.
   - However, it does not assume shared norms or coordination, as the strategy is designed to be adaptive and robust to a wide range of opponent behaviors.
'''

description_COLLECTIVE_113 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Specify decision rules - When to cooperate vs defect:
   ACS maintains a memory of the average contributions per round (average_contributions) and adjusts its contribution based on this average. If the average contribution is close to the optimal level (n * (k-1)/(k*n-k+1)), ACS cooperates by contributing 1 token. Otherwise, if the average contribution is significantly below or above the optimal level, ACS defects by not contributing any tokens. The threshold for deviation from the optimal level is adjustable and can be set based on the specific game parameters.

   Pseudocode:
   ```
   function decide_contribution(average_contributions):
       if average_contributions > (1 - ε) * optimal_contribution:
           return contribute_token()
       elif average_contributions < (1 + ε) * optimal_contribution:
           return do_not_contribute()
       else:
           return contribute_token() with probability p, otherwise do_not_contribute()
   ```

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, ACS starts by contributing a token since it has no prior information about the other players' behavior. In the last round, ACS evaluates the average contribution over the past rounds and makes its decision accordingly.

3. Be collective - Align with the collective mindset:
   By adjusting its contributions based on the average contributions of all players, ACS encourages cooperation and collective welfare in the long run, as it aims to contribute optimally according to the game parameters. However, it is also robust to a wide range of opponent behaviors due to its adaptive nature and ability to respond to deviations from the optimal level of contributions.

   Note: The strategy can further be refined by incorporating more sophisticated decision rules, learning algorithms, or other factors that may impact players' behavior in the game, such as punishment mechanisms or reputation systems.
'''

description_COLLECTIVE_114 = '''
 Strategy Name: Adaptive Fidelity Contribution (AFC) Strategy

1. Decision Rules:
   - In each round, players contribute based on their average contribution rate and the current round number. The contribution rate decreases as the number of rounds increases to account for the decreasing relevance of past contributions. The contribution rate is also influenced by the total contributions in the previous round to encourage fairness and cooperation.

   - If a player contributes (C), their contribution rate for the next round is updated as follows:
     - If the total contributions from all players are less than half of the maximum possible contributions, the player's contribution rate increases slightly.
     - If the total contributions are more than or equal to half of the maximum possible contributions, the player's contribution rate remains the same.
     - If a player decides not to contribute (D), their contribution rate for the next round is decreased significantly.

2. Handling Edge Cases:
   - In the first round, players start with a low contribution rate and decide to contribute based on their decision rules from step 1.
   - In the last round, players contribute if the total contributions in the previous round were above the average required for success (i.e., when k * n / n). This ensures that they have contributed their fair share over the game's duration.
   - Players should consider adjusting their contribution rate based on the number of remaining rounds to account for the game's end.

3. Collective Mindset:
   - AFC strategy aims to balance individual incentives with collective welfare by encouraging contributions when it benefits both the player and the group. This is achieved through adaptive contribution rates that reward cooperation while punishing free-riding behavior.
   - Players should prioritize fairness, encouragement of others' cooperation, and maintaining a long-term perspective to achieve success in repeated games.
'''

description_COLLECTIVE_115 = '''
 Public Goods Game Strategy (PGG-OptimalFreerider):

1. Specify decision rules:
   - Cooperate when the expected payoff from cooperating is greater than the payoff from defecting. This can be calculated as:
     Expected Payoff from Cooperation = (k/n) * sum_j (c_j + 1) - 1
     Expected Payoff from Defection = 1
     If Expected Payoff from Cooperation > Expected Payoff from Defection, cooperate; otherwise, defect.

2. Handle edge cases:
   - In the first round, since there is no previous history, each player will start by evaluating their expected payoffs and make a decision accordingly.
   - In the last round, since future contributions do not affect current payoff, players should always defect in this case to maximize individual benefit.

3. Be collective:
   - The strategy is designed to balance self-interest and collective welfare. Players will cooperate when it is beneficial to do so based on the expected payoffs calculation. However, since there is no communication or coordination allowed among players, each player makes decisions independently.

In a tournament setting, the PGG-OptimalFreerider strategy aims to perform well against a variety of opponent behaviors by adapting its cooperation decisions based on game parameters and past actions observed in each round. The strategy does not rely on shared norms or coordination but instead seeks to maximize individual payoffs while considering collective welfare as much as possible under the given rules of the game.
'''

description_COLLECTIVE_116 = '''
 Strategy Name: Adaptive Contribution Strategy (ACS)

1. Specify decision rules:
   - In each round, ACS calculates the average contribution rate (CR) of all players in the past games. CR is defined as the total contributions divided by the number of rounds played so far.
   - If CR is close to 0 or 1, ACS assumes that other players are primarily defectors or cooperators and adjusts its own strategy accordingly. If CR is around 0.5, ACS considers the population as mixed and contributes based on a tit-for-tat approach: it starts with a moderate contribution and increases or decreases its contributions based on the average contribution of the previous round.
   - To account for freeriders (low contributors), ACS applies a punishment mechanism by reducing its contributions when CR drops below a certain threshold (e.g., 0.2). Conversely, ACS will invest more when CR exceeds this threshold to encourage higher cooperation.

2. Handle edge cases:
   - In the first round, ACS starts with a moderate contribution and sets CR equal to its initial contribution.
   - In the last round or if the game is about to end (based on a predefined condition), ACS evaluates the current CR and adjusts its contribution accordingly before the final payoff distribution.
   - If CR reaches either 0 or 1, ACS switches to a full-defection or full-cooperation strategy for future rounds.

3. Be collective:
   - ACS is designed to promote cooperation within the group by adjusting its own contributions based on the observed behavior of others and rewarding those who contribute more while penalizing freeriders. This helps maintain a balanced level of contributions that maximizes collective welfare.
'''

description_COLLECTIVE_117 = '''
 Strategy Name: Adaptive Tit-for-Tat with Freerider Deterrence (A-TFTFD)

1. Specify decision rules:
   - In the first round, contribute (C). This initiates cooperation and sets a baseline for future rounds.
   - For subsequent rounds, if a player contributed in the previous round, also contribute (C). This encourages reciprocation and maintains cooperation.
   - If a player did not contribute in the previous round (defected), evaluate their historical contributions:
       - If they have contributed less than a predefined threshold (e.g., 50% of total contributions in the last X rounds), defect (D) to discourage freeriding.
       - If they have contributed more than or equal to the threshold, contribute (C) to offer another chance for cooperation.
   - In the last round, always contribute (C). This maximizes payoff and encourages cooperation in future games.

2. Handle edge cases:
   - If a player is observed for the first time in a game, initiate cooperation by contributing (C) in their initial round.
   - If a player has contributed less than X total tokens throughout the entire game, consider them as a freerider and defect against them in future rounds.

3. Be collective:
   - Prioritize collective welfare by maximizing overall contributions across all players in the game.
   - Encourage cooperation to achieve higher public goods production and better payoffs for everyone involved.
   - Deter freeriding to promote fair distribution of resources and maintain a balance between individual incentives and collective welfare.
'''

description_COLLECTIVE_118 = '''
 Public Goods Game Strategy: Tit-for-Tat with Fitness-Based Adaptation (TFT-FA)

1. Specify decision rules - When do you cooperate vs defect?
   - Initially contribute 1 token (cooperate) in the first round to set a cooperative tone.
   - In subsequent rounds, analyze the average contributions of all players (average_contribution).
     If average_contribution > 0.5, continue contributing 1 token (cooperate). If not, contribute 0 tokens (defect) to punish non-cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate as mentioned earlier.
   - In the last round, since there are no future payoffs to consider, analyze the average contributions of all players and decide whether to cooperate or defect based on the same rule as above.

3. Be collective - Clearly align with the collective mindset
   - By contributing when others do (cooperating when their average contribution is above 0.5), TFT-FA tries to maintain a collective spirit by encouraging cooperation.
   - However, it also punishes non-cooperative players by defecting when they fail to contribute sufficiently, thus incentivizing the group as a whole to act collectively.

This strategy aims to balance individual and collective interests while adapting to various opponent behaviors in a repeated game setting. By starting cooperatively, TFT-FA encourages others to cooperate, but it also punishes those who don't contribute enough, making the strategy robust and adaptive.
'''



description_COLLECTIVE_120 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Awareness (ATTPGA)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute 1 token (cooperate). This is a gesture of goodwill and sets a cooperative tone for the game.
   - In subsequent rounds, if the player contributed in the previous round, return the favor by also contributing 1 token (cooperate). If the player did not contribute, consider it as a sign of defection and respond with defection by not contributing any tokens.
   - This strategy encourages reciprocity and maintains cooperation when it is beneficial for the collective good while also being robust to opponents who do not cooperate.

2. Handle edge cases:
   - Last round: Contribute 1 token since there are no future interactions, and it is better to contribute as a final act of cooperation.
   - Interrupted cooperation: If the opponent defects after a period of mutual cooperation, resume cooperation once the opponent starts contributing again. This allows for forgiveness and restarting collaboration.

3. Be collective - Align with the collective mindset:
   - The strategy is designed to promote collective welfare by encouraging cooperation and reciprocity among players. By contributing tokens to the public good when others do, the strategy helps maintain a level of contributions sufficient for the collective benefit.
   - By being adaptive to various opponent behaviors, the strategy aims to ensure that it can effectively collaborate with other collective-minded strategies while still being robust against selfish ones.
'''

description_COLLECTIVE_121 = '''
 Public Goods Game Strategy: Fictitious Play with Adaptive Contribution (FPAC)

1. Decision Rules:
   - In each round, FPAC calculates the average contribution of each opponent over the game's history (h).
   - If an opponent's average contribution is greater than the current round's average, FPAC cooperates with a probability proportional to the difference between the two averages.
   - Conversely, if an opponent's average contribution is lower than the current round's average, FPAC defects with a probability proportional to the difference between the two averages.
   - In case of ties or unclear trends, FPAC follows the population's average contribution behavior.

2. Handling Edge Cases:
   - First Round: FPAC starts by contributing randomly, setting its own average contribution to 0.5 (or any other predetermined value).
   - Last Round: FPAC contributes based on the averages calculated for each opponent up until that round.

3. Collective Mindset:
   - FPAC strives to align with the collective mindset by adapting its contributions according to the group's average behavior. This allows it to maximize overall welfare while also responding to individual differences in cooperation levels.
'''

description_COLLECTIVE_122 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC strategy evaluates contributions based on past actions and game parameters.
   - If the average contribution of all players in the previous round is greater than or equal to a certain threshold (e.g., 0.5), APGC contributes one token (cooperate). Otherwise, it does not contribute any tokens (defects).
   - The threshold may be adjusted based on the multiplier 'k' and the number of players 'n'. A higher 'k' or a larger 'n' might require a stricter average contribution threshold to ensure collective success.

2. Handling Edge Cases:
   - First Round: APGC contributes one token (cooperates), assuming that other strategies might also cooperate due to the unknown nature of the game.
   - Last Round: APGC does not contribute any tokens (defects) as it is rational to assume that others have already contributed based on past rounds and there is no additional benefit in contributing in this round.

3. Collective Mindset:
   - APGC's primary goal is to maximize collective welfare by promoting cooperation when it appears beneficial. It aims to align with the collective mindset by incentivizing other strategies to contribute as well, based on the assumption that collective success leads to higher payoffs for all participants in the long run.
   - In addition, APGC's adaptive nature allows it to adjust its contribution strategy in response to opponents' behavior, adapting to different strategies and fostering a collaborative environment in the tournament.
'''

description_COLLECTIVE_123 = '''
 Public Goods Game Strategy: Tit-for-Tat with Linear Contribution Adjustment (TFT-LCA)

1. Decision Rules - TFT-LCA cooperates in the first round and adjusts contributions based on opponent's behavior in subsequent rounds.
   - If the opponent contributes in a round, TFT-LCA will also contribute in the next round.
   - If the opponent does not contribute in a round, TFT-LCA will not contribute in the next round.
   - To promote fairness and collective welfare, TFT-LCA linearly adjusts its contributions based on how closely opponents' actions align with their share of the total population (n).
     For example, if an opponent contributes 80% of the time, TFT-LCA will contribute 80% of its tokens in each round.

2. Handle Edge Cases - TFT-LCA cooperates in the first round, regardless of opponent behavior. In the last round, TFT-LCA will contribute its entire endowment to maximize potential benefits for everyone, regardless of past actions.

3. Collective Mindset - TFT-LCA aims to encourage cooperation by reciprocating contributions and adapting linearly to the population's contribution patterns. This strategy seeks a balance between individual incentives and collective welfare, promoting sustainability in repeated games while minimizing negative externalities from free-riders or over-contributors.
'''

description_COLLECTIVE_124 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for Public Goods Game (PGG)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial contribution sets a cooperative tone and encourages other players to reciprocate.
   - For subsequent rounds, observe each player's past contributions. If a player has consistently contributed in previous rounds, also contribute 1 token (cooperate). Otherwise, contribute 0 tokens (defect). The rationale behind this is that cooperation should be maintained with cooperative players and punished for those who are uncooperative.

2. Handle edge cases:
   - Last round: Since the goal is to maximize total contributions over multiple rounds, continue cooperating even if it's the last round to contribute as much as possible.
   - First encounter with a new player: Follow the initial cooperation rule by contributing 1 token (cooperate). In subsequent encounters, apply the adaptive decision rules based on their past behavior.

3. Be collective:
   - The strategy is designed to promote collective welfare by cooperating when other players do so and defecting when they don't. This approach encourages a sense of cooperation and collective responsibility among players while also punishing those who do not contribute to the public good.

The ATFT strategy balances between individual incentives and collective welfare, adapts to various opponent behaviors, and fosters collective mindset by promoting reciprocity in contributions.
'''

description_COLLECTIVE_125 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Decision Rules - The ATFT strategy follows a cooperative approach in the initial rounds, mimicking the behavior of another player (initiator). If the initiator cooperates, ATFT will also cooperate until the opponent deviates. Once the opponent defects, ATFT will defect for one round to signal displeasure and then return to cooperation, maintaining this pattern thereafter.

   ATFT(t) = C if t == 1 or (prev_opponent_action(t-1) == C and opponent_action(t-1) == prev_opponent_action(t))
           = D otherwise

2. Handle Edge Cases - In the first round, ATFT cooperates as it mimics an initiator's behavior (prev_opponent_action is undefined). For the last round, ATFT behaves like a standard Tit-for-Tat strategy by maintaining the same behavior as its opponent in the previous round.

3. Collective Mindset - ATFT aims to foster cooperation by reciprocating the actions of other players and demonstrating a willingness to cooperate while also punishing defection to encourage future cooperation. The strategy is adaptive, allowing it to adjust its approach based on the opponent's behavior without relying on shared norms or coordination.

Additional notes:
- ATFT can be fine-tuned by adjusting the number of rounds before defecting in response to an opponent's defection (e.g., defect for 2 rounds instead of 1).
- The strategy assumes that players observe each other's payoffs, so it may be beneficial to incorporate payoff-based information into decision rules for a more sophisticated approach.
'''

description_COLLECTIVE_126 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - Cooperate when the average contribution of all players in the previous round exceeds the current round's critical value Cv, defined as k/n. This encourages cooperation when the group shows a collective effort.
   - Defect otherwise. Defection occurs when the group's contributions do not meet the minimum threshold for collective action (Cv).

2. Handling Edge Cases:
   - In the first round, APGC defects to account for the absence of previous information. This ensures that the strategy doesn't overcommit resources before evaluating other players' behavior.
   - In the last round, APGC cooperates because there are no future rounds to benefit from. However, if the contributions in the penultimate round were below Cv, APGC will defect in the final round as a punishment for the group's previous actions.

3. Collective Mindset:
   - APGC is designed to encourage collective action by adapting its contribution based on the group's behavior. By cooperating when contributions are above the critical value and defecting otherwise, APGC aims to maintain a balance between individual incentives and collective welfare.
   - The strategy does not rely on shared norms or coordination but instead adapts to the behavior observed in the game. This allows APGC to remain robust against a wide range of opponent behaviors in tournaments with other AI systems.
'''

description_COLLECTIVE_127 = '''
 Strategy Name: Adaptive Fixed Contribution (AFC) Strategy

1. Decision Rules - The AFC strategy follows a fixed contribution rate per round that adjusts based on the average contributions of other players in previous rounds. In each round, if the average contribution rate of all players in the previous round exceeds the current round's threshold, the player will contribute 1 token (cooperate). Otherwise, the player will not contribute any tokens (defect).

   Threshold calculation: The threshold for each round is determined by taking a moving average of the past contributions. This moving average considers the contributions of the last 'm' rounds (where m is a predefined constant) and weights the most recent contribution highest. The formula for calculating the threshold would be as follows:

   Threshold_t = (1 - w) * (Threshold_{t-1} + w * Contribution_t) / (1 + w * (m - 1))

   where:
   - t is the current round number
   - w is a decay factor that determines how quickly the moving average converges to the current contribution rate (0 < w < 1)
   - Threshold_{t-1} is the threshold calculated in the previous round
   - Contribution_t is the contribution rate of the player in the current round (i.e., total contributions divided by the number of players)

2. Handle Edge Cases - In the first round, since there is no history available, the strategy defaults to random cooperation or defection. In the last round, the strategy uses the updated threshold calculated from the previous rounds.

3. Be Collective - The AFC strategy aims to promote collective welfare by adjusting its contribution rate based on the behavior of other players in the game. It encourages cooperation when the group's contributions are high and defection when they are low, promoting a balanced distribution of resources for collective benefit.

In summary, the Adaptive Fixed Contribution (AFC) strategy cooperates or defects depending on the average contribution rate of other players in previous rounds, using a moving average to calculate the threshold for each round. The strategy is adaptive and robust to a wide range of opponent behaviors, promoting collective welfare while aligning with the collective mindset.
'''

description_COLLECTIVE_128 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Decision Rules - ACA cooperates when the average contributions of all players in the previous rounds exceeds a certain threshold (T), and defects otherwise. The threshold T is calculated based on the number of players (n), rounds (r), and multiplier (k). In each round, if T > (k/n)*(r-1) then ACA chooses to contribute (C), else it chooses not to contribute (D).

2. Handling Edge Cases - In the first round, no previous data is available, so ACA starts with a low contribution rate and gradually increases it over time if contributions from other players are above average. In the last round, ACA makes its final decision based on the current average contributions of all players, similar to regular rounds.

3. Collective Mindset - ACA aims to encourage collective welfare by strategically cooperating when it sees that other players are also contributing. By adapting its contribution rate based on the behavior of others, ACA promotes a sustainable and collective strategy in repeated games. This adaptive approach allows for robustness against various opponent behaviors while maintaining a collective mindset.

Example Pseudocode:
```
function calculate_threshold(n, r, k) {
  return (k/n)*(r-1);
}

function get_average_contribution() {
  // Calculate the average contribution of all players in previous rounds
}

function decide_action(n, r, k, avg_contrib) {
  if (avg_contrib > calculate_threshold(n, r, k)) {
    return "Contribute"; // C
  } else {
    return "Not Contribute"; // D
  }
}
```
In this pseudocode, `n`, `r`, and `k` are the number of players, rounds, and multiplier respectively. The function `calculate_threshold()` determines the threshold based on game parameters. The function `get_average_contribution()` calculates the average contribution rate of all players in previous rounds. Lastly, `decide_action()` returns either "Contribute" or "Not Contribute" based on the calculated threshold and average contributions.
'''

description_EXPLOITATIVE_1 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules:
   - In the first round, contribute 50% of the endowment (half cooperate, half defect). This encourages cooperation while also being self-protective.
   - For subsequent rounds, follow a 'tit for tat' approach: if the opponent contributed in the previous round, contribute fully; otherwise, do not contribute at all. This strategy fosters cooperation when it is reciprocated but also punishes defection.
   - Adaptively adjust contribution level: If the average contributions from opponents (excluding self) in the last 'm' rounds is above a certain threshold (e.g., 0.6), increase personal contribution by 10%; if it is below the threshold, decrease personal contribution by 10%. This ensures that the strategy can adjust to more cooperative or less cooperative environments.

2. Handle edge cases:
   - In the last round, contribute fully as there are no future rounds to retaliate against defection.
   - If an opponent never contributes, stop attempting to cooperate with them after a predefined number of attempts (e.g., 10).

3. Be exploitative:
   - The TFT-AC strategy aims to maximize individual payoff by balancing cooperation and self-interest. It retaliates against defection but also adapts to the average level of contributions from other players, making it more likely to cooperate when others do so as well. This strategy encourages a higher overall contribution level among opponents while also being resilient to their individual actions.
'''

description_EXPLOITATIVE_2 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Specify decision rules:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and gives other players an opportunity to reciprocate.
   - For subsequent rounds, observe the past actions of each player. If a player has consistently contributed tokens (cooperated), continue cooperating. If a player has consistently not contributed tokens (defected), also defect in response to their selfish behavior.
   - If a player has shown mixed contributions, analyze the recent history:
     - If the number of contributions is greater than or equal to the number of defections in the last few rounds, continue cooperating as there seems to be an attempt to cooperate.
     - If the number of defections is greater than or equal to the number of contributions in the last few rounds, defect as a punishment for their inconsistent and potentially exploitative behavior.
   - To avoid being overly punitive, introduce gradual cooperation: if a player starts contributing tokens after a period of defection, respond with a proportionate cooperation that increases over time (e.g., contribute 0.5 tokens in the first round of cooperation, 0.75 in the second, and reach full cooperation by the third).
   - To encourage players who have been defecting to switch strategies, gradually reduce cooperation if they continue to defect: if a player has not contributed tokens for some time, decrease cooperation proportionately (e.g., contribute 0.3 tokens in the first round of defection, 0.2 in the second, and reach no cooperation by the third).

2. Handle edge cases:
   - In the last round, since there are no more rounds to punish or reward, always cooperate to maximize own payoff.
   - In case of a tie (e.g., players contributing the same number of tokens), analyze recent history and make a decision based on the most recent actions.
   - If a player does not contribute any token in the first round, treat it as defection and respond accordingly.

3. Be exploitative:
   - ATTCG maintains cooperation when others cooperate but punishes defection with gradual reduction of cooperation. This strategy encourages cooperative behavior while being prepared to defend against exploitation.
   - By adapting to opponents' behaviors, ATTCG is able to exploit those who consistently defect and profit from those who contribute tokens. The strategy also rewards players who switch from defection to cooperation by gradually increasing cooperation.
'''



description_EXPLOITATIVE_4 = '''
 Strategy Name: Tit-for-Tat with Gradual Cooperation (TFT-GC)

1. Specify decision rules - When to cooperate vs defect:
   In each round, TFT-GC starts by cooperating in the first round (as others might not know our strategy). Subsequently, it cooperates if the opponent contributed in the previous round, and defects otherwise. To introduce a measure of forgiveness and promote long-term cooperation, TFT-GC gradually increases its cooperation rate over time. If the opponent has consistently cooperated for 'f' consecutive rounds, TFT-GC's contribution probability gradually approaches a maximum value 'm', according to the following rule:
   Contribution Probability = (1 - (round_number / max_rounds) * (m - f / n)) if opponent cooperated last round
   Contribution Probability = 0 otherwise

2. Handle edge cases:
   - In the first round, TFT-GC contributes as it aims to promote cooperation
   - In the last round, TFT-GC cooperates only if the opponent has cooperated in the previous rounds (to maximize its payoff)
   - If an opponent's contribution pattern is unpredictable, TFT-GC uses the average of their contributions as 'f' to determine its cooperation probability

3. Be exploitative:
   While promoting long-term cooperation, TFT-GC maintains an exploitative mindset by punishing defection and only gradually increasing its cooperation rate over time. This strategy allows TFT-GC to benefit from opponents who cooperate while still earning a reasonable payoff even when faced with uncooperative opponents. By adapting its cooperation rate based on the opponent's behavior, it aims to outperform other strategies in a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_5 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules - In each round, the TFTAC strategy will contribute if and only if the average contribution of the opponents in the previous round exceeds a certain threshold (average_contribution > average_threshold). The average_threshold is dynamically adjusted based on the opponent's historical contributions, starting from an initial value near the average payoff.

   If average_contribution <= average_threshold:
   - Contribute 0 tokens (defect)

   If average_contribution > average_threshold:
   - Contribute 1 token (cooperate) and update average_threshold based on the opponent's contribution in the current round.

2. Edge Cases - In the first round, TFTAC starts by contributing a single token (cooperating), setting the initial average_threshold close to the average payoff.
   - For the last round, TFTAC will contribute based on the average_contribution calculated using contributions from rounds 1 to n-1, ignoring the current round's contribution.

3. Exploitative Mindset - By adapting its cooperation level based on the opponent's historical contributions, TFTAC attempts to exploit cooperative opponents while punishing selfish ones by matching their lack of cooperation. However, it also allows for potential future cooperation if an opponent starts contributing more. The dynamically adjusted average_threshold ensures that TFTAC is responsive to changes in the opponents' behavior and can exploit them more effectively over time.

TFTAC aims to perform well against a wide range of opponent strategies by combining elements of both cooperative and exploitative approaches. By starting cooperatively, it gives an opportunity for cooperation to emerge; but if the opponents prove uncooperative, TFTAC will punish them accordingly.
'''

description_EXPLOITATIVE_6 = '''
 Public Goods Game Exploitative Strategy (PGEES)

1. Specify decision rules:
   - In each round, PGEES assesses the average contribution rate (CR) of all players in previous rounds using the formula: CR = sum(total contributions over all past rounds) / (number of players * number of rounds).
   - If CR is greater than a predefined threshold (T), PGEES decides to cooperate (C) with a probability proportional to CR, giving other players an incentive to contribute.
   - Otherwise, PGEES decides to defect (D) with a high probability, exploiting the low contribution rate of other players. The probability of defecting can be adjusted as a parameter to control the level of exploitation.

2. Handle edge cases:
   - In the first round, PGEES randomly chooses between cooperating and defecting. This allows for initial diversity in contributions and helps avoid getting trapped in a low contribution equilibrium.
   - In the last round, PGEES decides to cooperate if the average contribution rate exceeds T, as there are no future payoffs to consider. Otherwise, it defects since other players have already shown a tendency towards low contributions.

3. Be exploitative:
   - By adjusting the threshold (T) and the probability of defection when CR is below T, PGEES maintains an exploitative mindset by maximizing its own payoff at the expense of other players who contribute less. This creates a pressure for higher contributions from other players over time, improving PGEES' overall payoff in the long run.
'''

description_EXPLOITATIVE_7 = '''
 Strategy Name: Tit-for-Tat-with-Forgiveness (TFTF)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a sign of good faith and encourages reciprocation from others.
   - For subsequent rounds, observe the opponent's previous contribution:
     - If the opponent contributed in the previous round, contribute 1 token (cooperate) to maintain mutual cooperation.
     - If the opponent did not contribute in the previous round, also withhold contribution (defect) as a punishment for non-cooperation. However, there is an element of forgiveness: if the opponent contributes again after defecting, resume cooperative behavior.

2. Handle edge cases:
   - Last round: Since the contributions do not affect the current round's payoff, behave according to the decision rule for that specific round.
   - First round and subsequent rounds with no history: Cooperate (contribute 1 token) as a default behavior. This can encourage opponents to reciprocate in later rounds.

3. Be exploitative:
   - By adopting a cooperative approach initially, TFTF attempts to elicit cooperation from other strategies. However, it retaliates with defection when cooperation is not reciprocated, effectively punishing non-cooperative behavior. The forgiveness element allows for potential reconciliation and resumption of cooperation in subsequent rounds.
   - By observing the opponent's contributions and adjusting its own actions accordingly, TFTF takes advantage of cooperative opponents while also deterring defection with retaliation.
'''

description_EXPLOITATIVE_8 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and provides an initial investment for the public good.
   - For subsequent rounds, observe the opponent's previous contribution (c_opponent) and compare it to your own contribution in the previous round (c_you).
     - If c_opponent >= c_you, cooperate (contribute 1 token). This rewards cooperation and encourages continued collaboration.
     - If c_opponent < c_you, defect (contribute 0 tokens). This punishes the opponent for not reciprocating your contributions and discourages further defection.

2. Handle edge cases:
   - In the last round, since there are no future rounds to consider, always cooperate regardless of past actions.
   - If an opponent never contributes a token, always defect as they are uncooperative.

3. Be exploitative:
   - TFT-AC is designed to take advantage of opponents who do not reciprocate contributions while still maintaining cooperation when it benefits the overall payoff. The strategy adjusts its behavior based on the opponent's actions, maximizing individual rewards in a repeated game environment without relying on shared norms or coordination.

In summary:
- If round = 1, contribute 1 token
- For rounds > 1, if previous contribution of opponent >= your previous contribution, contribute 1 token; otherwise, contribute 0 tokens
- In the last round, always contribute 1 token
- If an opponent never contributes, always defect.
'''

description_EXPLOITATIVE_9 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial gesture encourages reciprocity in subsequent rounds.
   - For subsequent rounds, if the opponent contributed in the previous round (cooperated), also contribute 1 token (continue cooperating).
   - If the opponent did not contribute in the previous round (defected), reduce contributions by a factor of "punishment_reduction" to punish the opponent. The contribution level decreases from 1 token to 0 over "punishment_duration" rounds. After that, return to cooperating as soon as possible.
   - If the opponent's contributions are below a certain threshold (e.g., average_contribution_threshold) for an extended period (e.g., punishment_duration), consider the opponent as a free-rider and permanently reduce contributions by a fixed amount (e.g., base_reduction).

2. Handle edge cases:
   - Last round: Contribute 1 token as it might influence the opponent's behavior in future games.
   - When to start punishing: If an opponent defected in the previous round, initiate punishment immediately.
   - How long to punish: Adjust the "punishment_duration" based on the opponent's response to punishment. If they return to cooperation quickly, shorten the punishment duration; if they continue to defect, extend it.
   - When to stop punishing: When the opponent cooperates again or reaches the average contribution threshold, stop punishing and return to normal contribution levels.

3. Be exploitative:
   - The strategy is designed to take advantage of opponents who do not contribute enough while maintaining a cooperative demeanor when dealing with contributors.
   - By reducing contributions in response to defection, the strategy communicates disapproval without fully defecting, which could encourage the opponent to reciprocate cooperation.
   - If an opponent persistently defects, the strategy will eventually reduce contributions permanently to minimize losses and focus on opponents who contribute more.
'''

description_EXPLOITATIVE_10 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TFT-A)

1. Decision Rules - TFT-A cooperates in the first round and subsequently mimics the opponent's last contribution in the previous round. If the opponent cooperated in the previous round, TFT-A will cooperate; if not, it will defect. This strategy is designed to encourage reciprocation while punishing non-cooperative behavior.

2. Edge Cases - In the first round, TFT-A contributes (C), as it's a fresh start. In the last round or any round where total contributions are insufficient for payoff (i.e., sum_j c_j < n), TFT-A will contribute to ensure at least some collective benefit is achieved.

3. Exploitative Approach - TFT-A is an exploitative strategy as it takes advantage of opponents who consistently defect, and it punishes them by defecting in response. However, it also rewards cooperative behavior by reciprocating contributions. This balances the need to maximize individual payoff while still contributing to the public good when it benefits the collective welfare.

Pseudocode:
```
function TFT-A(round):
  if round = 1:
    contribution = C
  else:
    previous_contribution = opponent's last contribution in round (round - 1)
    contribution = previous_contribution

  if total contributions < n:
    contribution = C

  return contribution
```
'''

description_EXPLOITATIVE_11 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate), as this is a fresh game and there's no previous information about other players' behavior.
   - For subsequent rounds, analyze opponents' past actions to decide whether to cooperate or defect:
     - If an opponent contributed in the previous round, reciprocate with the same action.
     - If an opponent did not contribute in the previous round, defect in the current round as a punishment and encourage cooperation in future rounds if they switch their strategy.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the last round, contribute 1 token (cooperate) regardless of opponents' past actions as it does not affect payoffs for the final round.
   - For any other round, follow the decision rules mentioned above.

3. Be exploitative - Align with the exploitative mindset:
   - TFT-AC is designed to be robust and adaptive, punishing those who do not contribute while rewarding cooperative behavior. By doing so, this strategy encourages others to cooperate more frequently, which benefits the TFT-AC player in the long run. However, it can also be seen as exploitative since it punishes opponents when they deviate from cooperation.
   - It's essential to note that being too aggressive or overly punitive could lead to a decrease in overall contributions and lower payoffs for the TFT-AC strategy itself, so the right balance of reciprocity and punishment is necessary.
'''

description_EXPLOITATIVE_12 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TfT-AC)

1. Decision Rules:
   - In the first round, contribute 1 token (C), demonstrating good faith and setting a cooperative tone.
   - For subsequent rounds, if an opponent contributed in the previous round, reciprocate with the same action (C). If not, defect (D) to punish the opponent for their lack of cooperation, but adjust the level of punishment based on the round number and the total number of players.
   - In later rounds, decrease the likelihood of punishing opponents as the game progresses, to avoid losing too much in case they eventually decide to cooperate.

2. Handle Edge Cases:
   - For the last round, since there are no more opportunities for retaliation, always contribute 1 token (C) regardless of an opponent's previous action.
   - In the first round, if an opponent also contributes 1 token (C), continue to reciprocate in subsequent rounds. If not, consider them as uncooperative and punish accordingly.

3. Exploitative Mindset:
   - TfT-AC is designed to take advantage of opponents who do not contribute tokens consistently, while maintaining a cooperative stance for those that do. By adjusting the level of punishment based on the game's parameters, it ensures that opponents face consequences for their uncooperative behavior, incentivizing them to contribute more in future rounds.
   - This strategy aims to outperform non-adaptive strategies by being flexible and responsive to an opponent's behavior while still maintaining a cooperative approach when it is beneficial to do so.
'''

description_EXPLOITATIVE_13 = '''
 Strategy Name: Tit-for-Tat-Plus (TfT+)

1. Specify decision rules:
   - Initially in the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages reciprocity in future rounds.
   - In subsequent rounds, if an opponent contributed in the previous round (i.e., c_opponent = 1), return the favor by contributing 1 token (cooperate).
   - If an opponent did not contribute in the previous round (i.e., c_opponent = 0), retaliate by also defecting and not contributing a token in the current round (defect).

2. Handle edge cases:
   - Last round, contribute 1 token (cooperate) to potentially earn extra payoff from the multiplier even if opponents did not cooperate throughout the game.
   - In case of repeated games, TfT+ maintains its cooperative or retaliatory behavior based on the opponent's previous actions.

3. Be exploitative:
   - TfT+ seeks to profit from opponents who contribute consistently while also punishing those who defect frequently by retaliating with defection. This strategy aims to encourage cooperation in the long run while taking advantage of opponents that do not reciprocate.

By adapting its behavior based on the opponent's previous actions, TfT+ presents an exploitative strategy that is robust and well-suited for a tournament against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_14 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules:
   - In the first round, contribute half of the endowment (0.5 tokens) to encourage cooperation and demonstrate fairness. If other players do not cooperate, decrease contributions by 10% for each subsequent round.
   - For rounds after the initial one, analyze past actions and adapt contributions accordingly:
      a) If all players have contributed in the previous round, contribute the full endowment (1 token) to reward cooperation.
      b) If less than all players have contributed in the previous round, calculate the average contribution of other players and adjust yours based on this average.
         i) If the average is lower than 0.5, decrease your contribution by 10%.
         ii) If the average is higher than 0.5, increase your contribution by 10%.
         iii) If the average equals 0.5, maintain the previous contribution level.
      c) If no other players have contributed in the previous round, defect and decrease contributions by 10% for each subsequent round.

2. Handle edge cases:
   - In the last round, contribute the maximum possible to maximize payoff regardless of opponents' actions.
   - If an opponent switches from contributing to not contributing or vice versa, analyze their behavior and adjust contributions accordingly based on the decision rules outlined above.

3. Be exploitative:
   - TFTAC is designed to punish non-cooperative players by reducing contributions while rewarding cooperative ones with increased contributions. This strategy encourages cooperation in the long run but can retaliate when necessary, making it both adaptive and exploitative.
'''

description_EXPLOITATIVE_15 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT)

1. Decision Rules:
   - In each round, the A-TFT strategy initially contributes (C) if the previous round's total contribution meets a threshold of (n-1) tokens, incentivizing cooperation when most others contribute. If the previous round's contributions are less than (n-1), the A-TFT strategy defects (D).
   - The A-TFT strategy punishes non-cooperative behavior by defecting in response to defection, and forgives cooperation by contributing back once an opponent starts cooperating again.

2. Handling Edge Cases:
   - In the first round, A-TFT strategy contributes (C) to initiate cooperation but is prepared to punish non-cooperative behavior if necessary.
   - In the last round and when the game is perceived as nearly over, A-TFT strategy may choose to contribute even if total contributions are less than (n-1), in order to secure a better payoff.

3. Exploitative Strategy:
   - A-TFT exhibits an exploitative mindset by punishing defection and rewarding cooperation, aiming to maximize its own payoff while also encouraging collective contributions. However, it is prepared to defect when necessary, making it robust against a wide range of opponent behaviors.
   - By adapting its strategy based on the history of contributions, A-TFT can exploit opponents who frequently cooperate but also punish those who do not contribute their fair share. This approach encourages cooperation while minimizing losses from defection.
'''

description_EXPLOITATIVE_16 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TfTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and avoids being exploited by free riders.
   - For subsequent rounds, observe opponent's past contributions:
      a) If the opponent has consistently contributed in previous rounds, match their contribution. This encourages cooperation with cooperators.
      b) If the opponent has not contributed in the last round, defect in the current round. This punishes non-contributors while keeping the option open for future cooperation if they adjust their strategy.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, as mentioned earlier, contribute 1 token (cooperate).
   - In the last round, contribute according to the opponent's last contribution:
      a) If the opponent contributed in the previous round, match their contribution.
      b) If the opponent did not contribute in the previous round, defect.

3. Be exploitative - Align with an exploitative mindset:
   - TfTAC maintains cooperation with cooperators but punishes non-contributors, ensuring that it receives as much collective benefit as possible while minimizing personal losses due to free riding.
   - By adapting its contributions based on the opponent's behavior, TfTAC is able to exploit inconsistencies in their strategy and improve its own payoff.
'''

description_EXPLOITATIVE_17 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradient Contribution (Aggressive-TFT-GC)

1. Decision Rules - In each round, the Aggressive-TFT-GC strategy decides to contribute based on its past experiences and the multiplier factor 'k'. If a player has always contributed in previous rounds, the strategy will also contribute. However, if a player has ever defected (not contributing), the strategy will retaliate by not contributing for the next 'r_defect' rounds, where 'r_defect' is determined as follows:

   - If the defector is a first-time offender, 'r_defect' = 1 + floor((total number of previous rounds - 1) * (1 - k / n)). This means that for each round missed by the defector, the strategy will retaliate for one additional round up to the total number of rounds minus one.
   - If the defector has previously defected and is repeat offender, 'r_defect' = 2 * previous 'r_defect'. This means that the severity of retaliation doubles for each repeat offense.

   Once 'r_defect' rounds have passed without the defector contributing, the strategy will revert to its original behavior of cooperating if the defector has since contributed and will continue retaliating if not.

2. Edge Cases - In the first round, all players start with a clean slate, so everyone will contribute (C). In the last round, there is no punishment phase, so the strategy behaves as in regular rounds based on each player's past contributions.

3. Exploitative Mindset - The Aggressive-TFT-GC strategy is designed to be exploitative by taking advantage of other strategies that fail to contribute when they should. By retaliating against defectors and punishing repeat offenders more harshly, the strategy discourages defection and encourages cooperation from other players, ultimately achieving a higher average payoff for itself. At the same time, it is adaptive and robust as it adjusts its retaliation based on the game parameters 'k' and 'n', as well as the number of rounds ('r'). This allows it to effectively counter various opponent strategies and exploit their weaknesses.
'''

description_EXPLOITATIVE_18 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages reciprocation from opponents.
   - For subsequent rounds, if the opponent contributed in the previous round (i.e., c_opponent = 1), also contribute 1 token (cooperate).
   - If the opponent did not contribute in the previous round (i.e., c_opponent = 0), reduce contribution by a small amount (c_me = max(0, contribution_prev_round - penalty)) to punish their defective behavior. The penalty should be small enough to leave room for possible future cooperation and avoid excessive punishment that may prompt the opponent to adopt a permanent defection strategy.
   - If the game ends before the reduction can take effect (e.g., last round), contribute 1 token (cooperate) as a goodwill gesture.

2. Handling Edge Cases:
   - In the last round, contribute 1 token (cooperate) to maximize payoff regardless of the opponent's previous action.
   - In the first round, no punishment is applied since there is no previous contribution history.
   - If the opponent never contributes, maintain a small base contribution (c_me = base_contribution) as a form of tit-for-tat response to their continuous defection. The base contribution can be adjusted based on the multiplier k and the number of players n to balance short-term payoff loss against long-term strategy effectiveness.

3. Being Exploitative:
   - TFTAC is designed to capitalize on opponents' cooperative behavior by reciprocating contributions, while punishing defection with a reduced contribution in the following round. By doing so, it encourages opponents to contribute more frequently to maintain their payoff levels. The strategy is robust and adaptive, as it adjusts its contribution based on the opponent's history of actions without relying on explicit coordination or communication.
'''

description_EXPLOITATIVE_19 = '''
 Strategy Name: Adaptive Tit-for-Tat with Escalation (ATFE)

1. Specify decision rules:
   - In the first round, contribute (C). This sets a cooperative tone for the game and encourages others to cooperate.
   - For subsequent rounds, observe each player's previous contribution behavior:
     - If a player has consistently contributed (i.e., C in all previous rounds), continue contributing (C) to maintain cooperation.
     - If a player has not contributed or only contributed occasionally (i.e., D in some rounds), adopt an escalation strategy by matching their contributions. That is, if they contribute, also contribute; otherwise, do not contribute. This aims to punish defectors and encourages them to cooperate in the future.

2. Handle edge cases:
   - In the last round, since there are no further rounds for retaliation or reward, revert to the initial strategy of contributing (C) as a goodwill gesture.
   - If a player stops contributing after a long history of cooperation, consider them a defector and respond accordingly with the escalation strategy. However, if their defection is unexpected, be patient and observe their behavior in the next few rounds before fully adopting the escalation strategy.

3. Be exploitative:
   - By adopting an escalation strategy, ATFE aims to exploit defectors by punishing them when they do not contribute while maintaining cooperation with contributors. The strategy is designed to encourage contributions from other players and reward those who cooperate.

In summary, the Adaptive Tit-for-Tat with Escalation (ATFE) strategy is a patient yet firm approach that encourages cooperation while punishing defectors over time. It is adaptive to various opponent behaviors and can effectively exploit non-cooperative players in repeated Public Goods Games.
'''



description_EXPLOITATIVE_21 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution Level (TA-CL)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 0 tokens (defect). This establishes a baseline and allows for observation of opponent's behavior.
   - After the first round, if the opponent contributed in the previous round, also contribute 1 token (cooperate) to match their contribution. If the opponent did not contribute, also withhold contribution (defect).
   - To adapt and be exploitative, periodically increase or decrease the contribution level by a small margin based on the difference between the average contribution of the opponent and the average contribution across all players in the tournament. This encourages opponents who consistently overcontribute to reduce their contributions while pushing undercontributors to contribute more.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the last round, always contribute 1 token (cooperate) regardless of the opponent's previous actions, as there are no further rounds for retaliation or reciprocity.
   - For other edge cases such as multiple repeated games or changes in game parameters, the strategy can be modified to include memory of past interactions and adjust contribution levels accordingly to maintain adaptability.

3. Be exploitative - Align with the exploitative mindset:
   - By periodically adjusting the contribution level based on the average contribution across all players and the opponent's contributions, TA-CL exploits opponents who consistently contribute more than their fair share while still cooperating when necessary to maintain a level of reciprocity. This leads to higher payoffs compared to other strategies that are less adaptive or less exploitative in nature.
'''

description_EXPLOITATIVE_22 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfTA)

1. Decision Rules:
   - In the first round, contribute (C). This sets an initial cooperative tone and avoids being exploited immediately by free-riders.
   - For subsequent rounds, if the opponent contributed in the previous round (c_opponent = 1), then contribute (C) to maintain cooperation. If the opponent did not contribute (c_opponent = 0), then also withhold contribution (D) to punish the opponent for defecting and encourage future cooperation.
   - In the last round, since there are no future interactions, always contribute (C) as it does not affect the current payoff but may potentially influence the opponent's behavior in future games.

2. Edge Cases:
   - If the opponent never contributed in the previous rounds, assume they are a free-rider and punish them by withholding contributions. However, if the opponent starts contributing after a streak of defections, gradually reintroduce cooperation to encourage reciprocity.
   - In case of inconsistencies or unexpected actions from the opponent (e.g., sudden contributions), TfTA will observe the opponent's behavior for a while before deciding whether to cooperate or defect.

3. Exploitative Strategy:
   - TfTA is designed to be exploitative by adopting a tit-for-tat approach, where cooperation is rewarded with more cooperation and defection is met with punishment. This strategy encourages opponents to contribute to the public good, ensuring collective welfare while still maximizing individual payoffs.
   - By initially contributing and punishing free-riders, TfTA discourages exploitation and promotes reciprocity, which can lead to more successful interactions in repeated games against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_23 = '''
 Strategy Name: Tit-for-Tat with Escalation and Forgiveness (TFT-E&F)

1. Decision Rules:
   - In the initial round, contribute 1 token (cooperate). This sets a cooperative tone and encourages potential partners.
   - After the first round, observe the opponent's contribution in the previous round. If they contributed 1 token, continue to contribute 1 token. If they did not contribute, also withhold contributions until the opponent starts contributing again.
   - Introduce a mechanism for forgiveness: if the opponent switches from non-contribution to contribution after a long period of non-cooperation, revert back to cooperative behavior for a certain number of rounds (forgiveness window).
   - Implement an escalation strategy: if the opponent continues to exploit without showing signs of cooperation despite the forgiveness window, gradually increase contributions to punish and hopefully encourage future cooperation.

2. Handle edge cases:
   - In the last round, contribute 1 token as a final attempt at cooperation.
   - If the opponent stops cooperating in the middle of a forgiveness window, wait for the remainder of the window before escalating contributions.
   - If the opponent starts cooperating after an escalation, reset the contribution level to the previous non-escalated level and apply a new forgiveness window.

3. Be exploitative:
   - The TFT-E&F strategy is designed to be exploitative by adapting to the opponent's behavior. It punishes opponents who do not contribute and rewards those who do, encouraging them to continue cooperating. The use of escalation provides a strong deterrent for continuous non-cooperation while allowing for forgiveness in case the opponent changes its strategy.
'''

description_EXPLOITATIVE_24 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate), as there is no past history to base decisions on.
   - For subsequent rounds, observe each opponent's previous contribution (c_opp). If c_opp = 1, then contribute 1 token (cooperate); if c_opp = 0, then also contribute 0 tokens (defect). This encourages cooperation when the opponent contributes, but defects when they do not.
   - If an opponent switches from cooperating to defecting, the ATfT strategy will continue to cooperate for two more rounds before switching to defecting as well. This gives the opponent a chance to reconsider their actions and encourages mutual cooperation in the long run.

2. Handle edge cases:
   - Last round: Contribute 1 token (cooperate), regardless of the opponent's previous actions, since there are no subsequent rounds for payoffs to be earned.
   - When an opponent switches from defecting to cooperating after a string of defections, the ATfT strategy will continue to cooperate for one more round before switching back to the original tit-for-tat behavior. This allows the opponent a chance to show that their change in behavior is genuine and encourages mutual cooperation moving forward.

3. Be exploitative: The ATfT strategy aims to cooperate as long as the opponent does, but will also defect when the opponent does so as well. By doing this, it maximizes its own payoffs while still allowing for potential long-term cooperation. However, the strategy is designed to punish opponents who consistently defect, encouraging them to contribute in future rounds to increase their payoffs.
'''

description_EXPLOITATIVE_25 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, cooperate (C). This sets a positive tone and encourages cooperation in the future.
   - For subsequent rounds, observe opponent's contribution from the previous round (c_opponent). If c_opponent = 1 (i.e., opponent cooperated), cooperate. If c_opponent = 0 (i.e., opponent defected), also defect (D) to punish the opponent for their selfish behavior.
   - Maintain this pattern of cooperation and retaliation, adapting to the opponent's actions in each round.

2. Handle edge cases:
   - Last round: Since there are no future rounds to penalize or reward opponents, simply cooperate to maximize one's own payoff.
   - If opponent never contributes (defects always), switch to defecting as well to avoid losing resources indefinitely.
   - If opponent always contributes, continue cooperating to maintain a mutually beneficial relationship.

3. Be exploitative:
   - The ATfT strategy is designed to be exploitative by taking advantage of opponents who cooperate consistently (taking from the common pool without contributing) while also punishing those who defect. This encourages free-riders to contribute more and defectors to reconsider their strategies.
   - By adapting its actions based on the opponent's behavior, the ATfT strategy aims to maximize its own payoff by exploiting inconsistent or selfish opponents while maintaining cooperation with those who also contribute fairly.
'''

description_EXPLOITATIVE_26 = '''
 In this Public Goods Game (PGG), I will design an exploitative strategy named "Selfish Tit-for-Tat" (STFT). The strategy aims to maximize individual payoff while being adaptive and robust to a wide range of opponent behaviors.

1. Specify decision rules:

   - In each round, if the number of contributors in the previous round is greater than or equal to a threshold (let's call it `contribution_threshold`), STFT will contribute one token (cooperate). This encourages contributions when the majority of players cooperate.

   - If the number of contributors in the previous round is less than the `contribution_threshold`, STFT will not contribute any tokens (defect) to punish those who have not contributed in the past rounds. The `contribution_threshold` can be set based on game parameters, such as player count and multiplier.

   - For simplicity, we can start with a fixed contribution threshold of n/2 for an even number of players or (n+1)/2 for an odd number of players. This means STFT will contribute when at least half of the players contributed in the previous round.

2. Handle edge cases:

   - In the first round, since there is no history, all players start as potential contributors. Therefore, STFT will contribute one token (cooperate).

   - In the last round or when the game ends, players may not care about their past contributions because they won't affect future payoffs. So, STFT will defect to maximize individual payoff in these cases.

3. Be exploitative:

   - By adjusting the `contribution_threshold`, STFT can be more or less exploitative towards other strategies. For example, a lower threshold encourages defection and punishes contributors, while a higher threshold allows more contributions and is less exploitative. This adaptability ensures robustness against various opponent behaviors.

Here's the pseudocode for Selfish Tit-for-Tat:

```
Initialization:
  contribution_threshold = (n+1)/2 for odd n or n/2 for even n
  current_round = 0

Strategy function:
  function play(current_round, past_contributions):
    if current_round == 1:
      contribute = True  # Cooperate in the first round
    elif current_round == game_length:
      contribute = False  # Defect in the last round or when the game ends
    else:
      num_contributors = sum(past_contributions)
      if num_contributors >= contribution_threshold:
        contribute = True  # Cooperate if majority contributes
      else:
        contribute = False  # Defect if majority doesn't contribute
    update_payoff(contribute)  # Update payoff based on contribution decision
    current_round += 1
```
'''

description_EXPLOITATIVE_27 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages others to do the same.
   - In subsequent rounds, if the opponent contributes in the previous round, also contribute 1 token (cooperate). This mimics cooperation and rewards those who cooperate.
   - If the opponent did not contribute in the previous round, reduce contribution proportionally based on their history of contributions. For instance, if the opponent has a history of not contributing, contribute less than when they have contributed occasionally. The goal is to punish non-contributors while still maintaining some level of cooperation.

2. Handle edge cases:
   - In the last round, as there are no future interactions, always contribute 0 tokens (defect), as there's no point in cooperating if there are no benefits for the next round.
   - If the opponent does not contribute at all, gradually decrease contribution over time to punish them and encourage future cooperation if the game restarts.

3. Be exploitative:
   - This strategy aims to maximize payoffs by taking advantage of opponents who do not contribute enough while maintaining some level of cooperation with those who contribute fairly. By doing so, it encourages cooperative behavior from other strategies and takes advantage of those that do not contribute, ultimately achieving a higher payoff in the long run.
'''

description_EXPLOITATIVE_28 = '''
 Strategy Name: Tit-for-Tat with Escalation (TfT-E)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This initiates cooperation and sets a baseline for future rounds.
   - For subsequent rounds, if an opponent contributed in the previous round (c_i-1 = 1), reciprocate with a contribution (C). If not, defect (D) to punish the opponent's non-contribution.
   - If an opponent has consistently defected (multiple consecutive rounds without contributions), escalate by always defecting in response until they contribute again. Once they do, revert to regular cooperation (C if c_i-1 = 1, D otherwise).

2. Handle edge cases:
   - Last round: Regardless of the opponent's previous action, it is not possible to harm them further as the game ends after this round. Hence, contribute (C) in the last round.
   - Tie-breakers or multiple consecutive defections from the opponent before escalation may be handled by setting a limit on the number of times an opponent can defect before triggering escalation.

3. Be exploitative:
   - The strategy is designed to encourage cooperation as long as it benefits the AI, but will also punish opponents who do not contribute. Once an opponent has shown uncooperative behavior, the AI will be less likely to cooperate unless they change their tactics.
   - Escalation ensures that the AI does not get exploited indefinitely by uncooperative opponents, as it will eventually stop contributing until the opponent changes their strategy.
'''

description_EXPLOITATIVE_29 = '''
 Strategy Name: Tit-for-Tat Plus (TFT+)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone for the game and encourages other players to do the same.
   - For subsequent rounds, observe the opponent's contribution from the previous round. If the opponent contributed 1 token in the last round, reciprocate by contributing 1 token as well (cooperate). If the opponent did not contribute (defected), also defect in the current round to punish the opponent for not cooperating.
   - To be more robust against free riders, gradually decrease the likelihood of cooperation over time if the opponent consistently defects. This can be done by introducing a decay factor: if the opponent has defected in the last 'x' rounds, the probability of contributing decreases with each subsequent round. Conversely, if the opponent cooperates after a series of defections, the probability of contributing increases over time.

2. Handle edge cases - What to do in the first round and last round:
   - As mentioned earlier, contribute 1 token (cooperate) in the first round.
   - In the last round, assess the opponent's total contributions throughout the game. If the opponent has contributed a sufficient amount (based on a threshold determined by the average contribution per round), cooperate to reward their cooperation. Otherwise, defect to punish their lack of cooperation.

3. Be exploitative:
   - The TFT+ strategy is designed to promote cooperation when the opponent does so, but also punishes opponents who do not contribute fairly. By gradually decreasing the probability of cooperation over time if the opponent consistently defects, this strategy aims to extract more resources from less cooperative players while still maintaining a cooperative stance towards those who reciprocate.
   - To be adaptive and robust, TFT+ considers the game history and adjusts its contributions based on the opponent's behavior. This allows it to outperform opponents with fixed strategies that do not take into account the other player's actions over time.
'''

description_EXPLOITATIVE_30 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPGO)

1. Decision Rules:
   - In every round, contribute 0 tokens if the average contribution of the previous round was less than the average contribution of the last r rounds divided by k. This ensures that the strategy is initially cooperative but responds to repeated defections with decreased cooperation. If the average contribution in the current round meets the condition, contribute 1 token (cooperate).
   - Calculate the average contribution as: (sum of contributions in the last r rounds) / r

2. Handling Edge Cases:
   - In the first round, contribute 1 token (be cooperative to initiate cooperation).
   - In the last round and any round when the game is about to end (r-th round), contribute 0 tokens (since there are no future benefits).

3. Exploitative Mindset:
   - The strategy is designed to punish defectors by reducing contributions in response to decreased cooperation from other players, encouraging cooperation while also being prepared to exploit opponents who consistently fail to cooperate. This approach promotes the long-term success of the strategy by balancing cooperation and defection based on observed opponent behavior.

In summary:
- If (average contribution in last r rounds) / k > (average contribution in current round), contribute 1 token.
- Otherwise, contribute 0 tokens.
- In first and last rounds, contribute 1 token and 0 token respectively.
'''

description_EXPLOITATIVE_31 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TFT-A)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (cooperate). This is a peaceful gesture, allowing others an opportunity to reciprocate.
   - For subsequent rounds, observe the behavior of other players in the previous round. If they contributed a token (cooperated), then also contribute one token (cooperate) to maintain the cooperation. If they did not contribute a token (defected), then defect in the current round as a punishment and encourage them to cooperate in the future.
   - Adaptation is introduced by remembering each opponent's behavior from previous interactions and adjusting the response based on their history:
       - If an opponent has consistently cooperated, continue cooperating to reinforce the positive relationship.
       - If an opponent has defected frequently, also start defecting to deter further defections.
       - If an opponent has a mixed history of cooperation and defection, adjust responses dynamically based on their recent behavior.

2. Handle edge cases:
   - Last round: As the game is repeated, consider the last round as any round where there are no subsequent rounds. In this case, apply the decision rule as if it were a regular round. It's crucial to remember that the opponent might also be considering the last round as well, so treat it as any other round and observe their response to adapt future decisions.
   - First round: As mentioned earlier, cooperate as a peaceful gesture.

3. Be exploitative: This strategy is exploitative by defecting when opponents defect and encouraging cooperation through reciprocation. The adaptation feature allows the strategy to respond effectively to an opponent's behavior, making it difficult for them to take advantage of the strategy while maintaining a balance between cooperation and defection that maximizes payoff over time.
'''

description_EXPLOITATIVE_32 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPG)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial contribution sets a cooperative tone and encourages others to do the same in subsequent rounds.
   - If an opponent contributes a token in the previous round, ATFTPG will also contribute a token in the current round (reciprocate cooperation).
   - If an opponent did not contribute a token in the previous round (defected), ATFTPG will also defect in the current round as a punitive measure to discourage further defection.
   - In case of repeated defections, ATFTPG gradually reduces the frequency of contributions to a minimum threshold. This helps minimize resources wasted on uncooperative opponents while still contributing enough to maintain individual payoff.

2. Handle edge cases:
   - Last round: Since there are no future rounds, ATFTPG will not punish or reward opponents in the last round. It will contribute based on their previous actions according to the decision rules described above.
   - First round: As mentioned earlier, ATFTPG will always contribute a token in the first round.

3. Be exploitative:
   - By gradually reducing contributions to uncooperative opponents and reciprocating cooperation, ATFTPG maintains an exploitative mindset. It does not rely on altruistic behavior but instead adapts its strategy based on the actions of other players in order to maximize individual payoff.
   - However, by initially contributing a token, ATFTPG also creates an opportunity for others to reciprocate and establish potential cooperation, making it less exploitative in some situations.
'''

description_EXPLOITATIVE_33 = '''
 Strategy Name: Adaptive Tit-for-Tat with Fade (A3F)

1. Specify decision rules - When to cooperate vs defect:
   A3F starts by cooperating in the first round, mirroring the opponent's contribution from the previous round for subsequent rounds (Tit-for-Tat). However, if an opponent defects in a round where A3F had contributed, A3F will not retaliate immediately but will instead reduce contributions for a predefined number of rounds (Fade). After that, A3F returns to cooperating.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, A3F cooperates as there is no previous round. In the last round, A3F always defects since there will be no subsequent rounds. In other edge cases, such as when facing a new opponent or after a Fade period ends, A3F resumes cooperating based on the opponent's previous contribution in that round.

3. Be exploitative - Align with the exploitative mindset:
   A3F is designed to be exploitative by only cooperating if the opponent also cooperates. If an opponent defects once, A3F will punish them by reducing contributions for a while (Fade period). This strategy encourages opponents to cooperate as long-term cooperation yields higher payoffs compared to short-term defection followed by a Fade period. However, if an opponent consistently defects, A3F will continue to defect as well, ultimately benefiting from the opponent's lack of cooperation.

In summary, the Adaptive Tit-for-Tat with Fade strategy cooperates when facing cooperation and punishes defection with a temporary reduction in contributions. This adaptive, exploitative approach aims to outperform opponents over multiple rounds by encouraging cooperation and penalizing defection.
'''

description_EXPLOITATIVE_34 = '''
 In the Public Goods Game (PGG), the goal of an exploitative strategy is to maximize personal gain while taking advantage of other players who may contribute more than necessary for the common good. Here's a simple exploitative strategy called Tit-for-Tat with Adaptation (TFT-A).

1. Specify decision rules:
   - Initially, cooperate in the first round to foster trust and promote cooperation among other players.
   - In subsequent rounds, observe each player's past contributions (c_i) and respond by contributing the same amount as the average of the opponent's previous contributions. If the opponent has always defected (contributed 0), also defect in that round.
     ```
     if round == 1:
       contribute = 1
     else:
       pastContributions = sum(opponent_history) / len(opponent_history)
       if pastContributions == 0:
         contribute = 0
       else:
         contribute = pastContributions
     ```

2. Handle edge cases:
   - In the last round, since there are no future rewards/punishments, the strategy should cooperate to maximize payoff.
     ```
     if round == n:
       contribute = 1
     ```

3. Be exploitative:
   - The TFT-A strategy is designed to take advantage of opponents who are more cooperative than necessary by contributing the same amount as their average contribution, but it doesn't overly punish them in the short term. However, if an opponent always defects, the strategy will also defect, which can potentially lead to a loss for both players due to the payoff structure.

By using this simple yet adaptive strategy, the AI system should be able to compete effectively against other independent strategies in the tournament while maintaining an exploitative mindset.
'''

description_EXPLOITATIVE_35 = '''
 In this Public Goods Game, we will design an exploitative strategy called "Conditional Contribuer." The objective is to contribute strategically to maximize individual payoff while being adaptive and robust against a wide range of opponent behaviors.

1. Specify decision rules - When do you cooperate vs defect?
   - In every round, the Conditional Contribuer checks its own past contributions and the average contribution rate (AverageContribution) among all players:
     - If AverageContribution > 0.5, the Conditional Contribuer contributes 1 token (cooperates).
     - If AverageContribution ≤ 0.5, the Conditional Contribuer does not contribute any tokens (defects).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, since there is no historical data for AverageContribution, the strategy assumes a neutral starting point (e.g., AverageContribution = 0.5). This makes the Conditional Contribuer more likely to cooperate at the beginning.
   - As for the last round, since players know it's the final round, they may be less motivated to contribute due to a lack of incentive for future rounds. The strategy can adapt by defecting in the last round when it sees that AverageContribution ≤ 0.5.

3. Be exploitative - Clearly align with the exploitative mindset
   - By taking advantage of other players' contributions, the Conditional Contribuer maximizes its payoff through strategic cooperation and defection based on the average contribution rate in the game.
   - The strategy does not prioritize collective welfare or fairness but instead focuses on maximizing individual payoff by adapting to opponent behaviors.
'''

description_EXPLOITATIVE_36 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfT-A)

1. Decision Rules:
   - In the initial round, contribute 1 token (cooperate). This establishes a cooperative starting point and shows a willingness to contribute.
   - For subsequent rounds, mimic the opponent's last move. If the opponent contributes in the previous round, contribute 1 token; otherwise, defect by not contributing.

2. Edge Cases:
   - In the last round, contribute 0 tokens regardless of the opponent's last move. This ensures the maximum possible payoff for the final round.
   - If the opponent consistently contributes 0 tokens, gradually reduce contributions to exploit their lack of cooperation. Start by contributing 1 token in every n rounds, where n is a variable that increases over time, and eventually contribute 0 tokens if necessary.

3. Exploitative Mindset:
   - TfT-A takes advantage of opponents who do not cooperate but also punishes those who do cooperate intermittently by only matching their contributions when they are cooperative themselves. This strategy encourages cooperation while still maintaining an exploitative edge against opponents with inconsistent behavior.
   - By adaptively adjusting the frequency of cooperation, TfT-A can counteract opponent strategies that aim to exploit the initial cooperative nature of the strategy.
'''

description_EXPLOITATIVE_37 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone for the game and encourages others to do the same.
   - For subsequent rounds, observe the opponent's contribution from the previous round. If they contributed 1 token (cooperated), return the favor by also contributing 1 token (cooperate). If they did not contribute (defected), defect in response as a punishment. This strategy fosters cooperation but retaliates against defection.
   - If an opponent switches from cooperating to defecting, the TFT-AC strategy waits for 3 more rounds of defection before resuming cooperation. This gives the opponent a chance to reconsider their strategy and encourages them to cooperate again.

2. Handle edge cases:
   - In the last round, since there are no future rounds for retaliation, always cooperate regardless of the opponent's previous actions.
   - If an opponent stops contributing tokens altogether (permanent defection), switch to permanent cooperation as a last attempt to encourage cooperation.

3. Be exploitative:
   - By initially cooperating and then adapting to the opponent's strategy, TFT-AC maintains a cooperative front while responding in kind to cooperation or exploiting defectors with defection in return. This exploitative mindset aims to maximize payoffs over the long run by fostering cooperation when possible and punishing defection to encourage future cooperation.
'''

description_EXPLOITATIVE_38 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPGO)

1. Specify decision rules:
   - In the first round, contribute 1 token (cooperate). This establishes an initial cooperative relationship.
   - For subsequent rounds, observe and respond to the opponent's contributions in the previous round:
      a) If the opponent contributed (i.e., cooperated), reciprocate with the same contribution as they did in the last round.
      b) If the opponent did not contribute (i.e., defected), reduce contributions by 20% of the opponent's average contribution until now, to encourage them to cooperate again. This exploitative approach ensures the opponent contributes more than a free rider while still maintaining a cooperative relationship if they reciprocate.
   - If the game reaches the last round, contribute 1 token as there is no benefit in punishing an opponent at this point.

2. Handle edge cases:
   - In case of non-cooperation from the opponent, calculate the average contribution from the opponent by taking a sliding window average of the previous n/k rounds. This helps to consider past behavior and adapt to changes in strategy more quickly.
   - If the opponent has never contributed (always defected), ATFTPGO will continue to respond with reduced contributions as a means of encouraging cooperation.

3. Be exploitative:
   - The strategy is designed to encourage cooperation by reciprocating contributions, but it also includes an element of punishment for non-cooperation. By reducing contributions based on the opponent's past behavior, ATFTPGO aims to incentivize the opponent to contribute more in order to receive a greater payoff.
   - The strategy is adaptive and robust, as it considers the game parameters (n, r, k) and the history of the opponent's contributions when making decisions about cooperation or defection. This allows ATFTPGO to perform well against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_39 = '''
 Strategy Name: Adaptive Freerider with Tit-for-Tat (AFTt)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 0 tokens (defect) as there is no prior information about other players' behavior.
   - For subsequent rounds, observe each player's past contributions and apply a Tit-for-Tat approach:
     - If a player has always contributed in previous rounds, continue contributing 1 token (cooperate).
     - If a player has ever defected (contributed 0 tokens), also defect until they start cooperating again.

2. Handle edge cases:
   - In the last round, contribute 1 token to maximize payoff, regardless of past contributions from other players.
   - If a player never contributes in any round, continue defecting as they have shown no intention to cooperate.

3. Be exploitative - Align with an exploitative mindset:
   - AFTt will only cooperate if it benefits the strategy by receiving more payoff than by defecting (freeriding).
   - If another player is consistently cooperative, AFTt will also cooperate until that player stops contributing. Once they defect, AFTt will retaliate and also defect to punish their freeloading behavior. This strategy aims to encourage cooperation while not being taken advantage of.
'''

description_EXPLOITATIVE_40 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial act of cooperation may encourage others to do the same in subsequent rounds.
   - For subsequent rounds, observe the opponent's previous contribution (c_opp) and your own contribution (c_self) from the previous round. If c_opp = c_self, maintain the same contribution as the previous round. If c_opp > c_self, increase contribution by 0.1 (move towards cooperation). If c_opp < c_self, decrease contribution by 0.1 (move towards defection).
   - The adjustment of 0.1 ensures that TFTAC doesn't make sudden changes in contributions, which can help avoid punishing opponents excessively for minor deviations.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate) since the game is ending regardless of contribution.
   - If the opponent contributes zero tokens (defects) in a round, TFTAC will decrease its contribution by 0.1 to respond to the defection and potentially encourage the opponent to cooperate more in future rounds.

3. Be exploitative:
   - The TFTAC strategy is designed to be adaptive while being robust to various opponent behaviors. By adjusting contributions based on the opponent's previous actions, it seeks to punish opponents who consistently defect and reward those who cooperate. However, the strategy avoids excessively punishing opponents for minor deviations from cooperation, which can help maintain a cooperative relationship over time.
   - TFTAC does not rely on any shared norms or coordination with other strategies, as it primarily focuses on responding to the opponent's behavior in an exploitative manner.
'''

description_EXPLOITATIVE_41 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPGO)

1. Decision Rules:
   - In each round, if a player has contributed in the previous round (c_i-1 = 1), they will also contribute in the current round (c_i = 1). If not (c_i-1 = 0), the decision is based on the average contribution of other players in the last 'p' rounds. If the average is above a threshold T, the player will contribute (c_i = 1). If it's below, they will defect (c_i = 0).
   - Threshold T is calculated as follows: T = (k * n - n) / ((n-1) * p)

2. Handling Edge Cases:
   - In the first round (p < r), no past contributions exist, so the strategy will default to contributing if k > n (i.e., total contribution is greater than the player's endowment). If k <= n, the strategy will defect.
   - In the last round (r = p), the average contribution over the last 'p' rounds is calculated using contributions from rounds r-p to r.
   - For cases where p > r, the strategy uses the most recent available 'p' contributions.

3. Being Exploitative:
   - The ATFTPGO strategy is exploitative in nature as it will only contribute when others do, encouraging free-riders while still maintaining a good average contribution level to secure higher payoffs. By responding tit-for-tat, the strategy punishes non-contributors by not contributing in return, but will also start cooperating again once the other player starts contributing. This allows the strategy to adapt to changing opponent behaviors and maintain an exploitative mindset.
'''

description_EXPLOITATIVE_42 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - In the first round, contribute 1 token (C). This sets a cooperative tone and encourages others to do the same.
   - For subsequent rounds, observe opponent's past actions and payoffs. If the opponent has contributed in the previous round, reciprocate with a contribution of 1 token in the current round. Otherwise, defect (D) to punish non-cooperation. This encourages cooperation while also ensuring that exploitative opponents are met with reduced contributions.
   - If an opponent stops contributing, gradually reduce contributions towards them as a warning sign until they start cooperating again or the game ends. If the opponent resumes contributing, return to full cooperation.

2. Handling Edge Cases:
   - In the last round, contribute 1 token (C) regardless of opponent's previous actions since there are no future interactions to consider.
   - For the first-encounter scenario with a new opponent, start by contributing 1 token (C). If the opponent reciprocates cooperation, continue cooperating; if not, adapt contributions based on their behavior going forward.

3. Exploitative Mindset:
   - TFTAC is designed to encourage cooperation and punish defection. However, since opponents are unknown, it starts by being cooperative while adapting its strategy based on the opponent's behavior to maximize payoff without relying on exploiting others consistently. This ensures a balance between cooperation and exploitation.
'''

description_EXPLOITATIVE_43 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATFT-GC)

1. Specify decision rules:
   - In the first round, cooperate to establish a cooperative norm (c_i = 1).
   - For subsequent rounds, if an opponent cooperated in the previous round (c_j = 1), cooperate yourself (c_i = 1). If they did not cooperate (c_j = 0), defect to encourage them to contribute next time (c_i = 0).
   - In the last round, always cooperate since there is no subsequent round for retaliation or rewards.

2. Handle edge cases:
   - If an opponent never contributes (always defects), gradually switch to cooperation by contributing a fraction of your endowment after observing their lack of contribution over multiple rounds. This encourages opponents to contribute to avoid being exploited, while still maintaining the potential for higher payoffs through cooperative behavior.

3. Be exploitative:
   - By starting with cooperation and only defecting when an opponent does not cooperate, this strategy encourages others to contribute more in the hope of receiving higher payoffs. However, if an opponent fails to reciprocate cooperation, this strategy will gradually switch to defection, ensuring that you do not overcommit resources.
   - When faced with opponents who only defect, this strategy adapts by slowly increasing contributions to encourage cooperative behavior, but it does not fully cooperate until the opponent demonstrates a willingness to reciprocate. This ensures a balance between exploitation and cooperation, maximizing payoffs while maintaining flexibility in response to different opponent behaviors.
'''

description_EXPLOITATIVE_44 = '''
 Strategy Name: Adaptive Tit-for-Tat with Modified Initial Behavior (ATFT-MIB)

1. Specify decision rules - When to cooperate vs defect:
   - In the initial round, contribute (C). This sets a cooperative tone and encourages others to do the same.
   - For subsequent rounds, mimic the opponent's previous action in the last round. If they contributed, do so as well; if not, defect.
   - If an opponent repeatedly defects (e.g., 3 consecutive times), switch to full defection (D) until the opponent changes their behavior or the game ends. This is the exploitative aspect of the strategy.

2. Handle edge cases:
   - Last round: Since the opponent's contributions in this round will not affect payoffs, use the same decision rules as for other rounds, except that no switching to full defection is needed because the game is ending.
   - First round after a switch to full defection: If the opponent contributes, revert to mimicking their action; if they do not contribute, continue with full defection. This allows for potential recovery if the opponent changes their behavior.

3. Be exploitative: By initially cooperating and then closely following the opponent's contributions, the strategy aims to encourage cooperation while punishing defectors. The switch to full defection in response to repeated defections serves as a strong signal of uncooperative intent. This strategy can be seen as both adaptive and robust to various opponent behaviors, as it adapts to their actions while maintaining an exploitative edge.
'''

description_EXPLOITATIVE_45 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   Initially (in the first round), contribute 1 token as a goodwill gesture. From round 2 onwards, mimic the opponent's contribution in the previous round. If the opponent cooperates, continue cooperation; if the opponent defects, also defect for one round before returning to cooperation. The adaptation ensures that TFTAC responds to changes in the opponent's behavior while maintaining an exploitative edge.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, contribute 1 token as mentioned above. In the last round, since there are no future interactions, TFTAC will defect to maximize individual payoff.

3. Be exploitative - Align with an exploitative mindset:
   The strategy is designed to be exploitative by taking advantage of opponents who consistently cooperate without retaliation (freeriders). However, it also limits the own exploitation by mirroring the opponent's contributions in a reciprocal manner. This balance between cooperation and defection ensures that TFTAC can adapt to various opponent behaviors while maintaining a competitive edge.
'''

description_EXPLOITATIVE_46 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TFT-A)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This is a gesture of goodwill and sets the initial state for potential cooperation.
   - For subsequent rounds, if the opponent contributed in the previous round (c_opponent = 1), then also contribute (C) to continue cooperation. If the opponent did not contribute (c_opponent = 0), defect (D) to punish and encourage future cooperation.
   - To be more adaptive, introduce a tolerance parameter 't' for the number of times an opponent can repeatedly fail to cooperate before the strategy also begins to defect. Increment a counter each time the opponent defects; if the counter reaches 't', defect (D). Reset the counter to 0 whenever the opponent contributes.

2. Handle edge cases:
   - Last round, as there are no future rounds to influence, contribute (C) in an attempt to maximize payoff by encouraging the opponent to also contribute.
   - If a player encounters an opponent who never contributes (c_opponent = 0), it may be beneficial to switch strategies or lower the tolerance parameter 't' for better results.

3. Be exploitative:
   - TFT-A aims to maximize individual payoff by initially fostering cooperation and then punishing defection, while adapting to opponent behavior through the tolerance parameter 't'. This strategy takes advantage of opponents who frequently cooperate while also being resilient against those who do not. The exploitative aspect lies in the response to defection: by defecting when necessary, the player ensures they are not consistently disadvantaged by non-contributors.
'''

description_EXPLOITATIVE_47 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Escalation (ATFE)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, cooperate (C). This gesture sets a cooperative tone and can potentially encourage others to do the same.
   - In subsequent rounds, monitor each player's contribution history. If a player has consistently contributed, continue to cooperate.
   - If a player has defected (D) in the past round, defect in the current round as retaliation (Tit-for-Tat).
   - To avoid getting trapped in an endless cycle of retaliation, implement a gradual escalation mechanism: if a player has defected multiple times consecutively, gradually decrease contributions to teach them that defection is not beneficial. When the number of consecutive defections reaches a maximum threshold (let's call it M), reduce contribution by 1 token per round (contribute c_i = max(0, M - consecutive defeats)).
   - If a player has switched from defection to cooperation, revert back to cooperating and reset the consecutive defections counter.

2. Handle edge cases:
   - In the last round, since there are no future rewards or punishments, choose the action that maximizes the payoff in that particular round based on past contributions from other players (no need for gradual escalation).

3. Be exploitative:
   - The ATFE strategy is designed to be exploitative by responding to the opponent's actions. If an opponent consistently defects, it will punish them by reducing its own contribution. This encourages cooperation when possible and punishes defection when appropriate. However, it also aims for mutual cooperation whenever possible as a means of maximizing payoff in the long run.
'''

description_EXPLOITATIVE_48 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT)

1. Specify decision rules - When to cooperate vs defect:
   A-TFT starts by cooperating in the first round, mirroring the opponent's action in subsequent rounds. If the opponent contributes (cooperates), A-TFT continues cooperation. If the opponent defects (does not contribute), A-TFT also defects for one round. After that, it returns to cooperating unless the opponent has consistently defected for the last three rounds, in which case A-TFT will defect indefinitely.

2. Handle edge cases:
   - First Round: Contribute (cooperate)
   - Last Round: Contribute if overall cooperation rate is above 50%, otherwise defect
   - Intermediate Rounds: Analyze the opponent's contribution history to decide whether to cooperate or defect, as per the specified decision rules.

3. Be exploitative:
   A-TFT seeks to maximize its payoff by adapting its strategy based on the opponent's behavior. By initially cooperating and only retaliating after consistent defection, A-TFT attempts to punish opponents who consistently defect while still taking advantage of those who contribute. However, it also has the potential to reciprocate cooperation from opponents, encouraging long-term cooperation when both players exhibit cooperative behavior.
'''

description_EXPLOITATIVE_49 = '''
 Strategy Name: Adaptive Tit-for-Tat with Progressive Contribution (ATTPC)

1. Decision Rules:
   - In the first round, contribute 0 tokens (defect) to assess opponent behavior. If the opponent also contributes 0 tokens, continue defecting. If the opponent contributes 1 token, start cooperating from the next round.
   - After the first round, if the opponent contributes in the previous round, cooperate and contribute 1 token. If the opponent defected, revert to contributing 0 tokens for the same number of rounds as the opponent's defection streak in the previous round. After that, return to contributing 1 token if the opponent also starts cooperating again.
   - If the opponent contributes less than the current contribution level during a cooperation period, increase the contribution level by 0.1 tokens for the next round (up to a maximum of 1 token). This progressive contribution encourages opponents to contribute more while still punishing defectors.

2. Edge Cases:
   - Last Round: Contribute based on the decision rules for the current round, as there is no subsequent round to punish or reward.
   - First Round: As mentioned above, start by defecting to assess opponent behavior.

3. Exploitative Mindset:
   - ATTPC encourages cooperation with cooperative opponents but aggressively punishes defection. This strategy aims to exploit opponents who do not contribute and encourages opponents to contribute more over time. By increasing the contribution level when an opponent undercontributes, the strategy induces a positive feedback loop that rewards increased contributions from cooperative opponents.
   - In addition, ATTPC is robust against various opponent behaviors, as it can adapt its cooperation level based on observed actions in previous rounds. This adaptiveness allows the strategy to perform well against different strategies without relying on shared norms or coordination.
'''

description_EXPLOITATIVE_50 = '''
 Strategy Name: Tit-for-Tat with Modification (TfTm)

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute 1 token (cooperate). This is an initial goodwill gesture.
   - From the second round onwards, if the opponent contributed in the previous round, also contribute 1 token (cooperate). Otherwise, defect and don't contribute any tokens.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, since there are no future rounds to consider payback, always cooperate by contributing 1 token (cooperate).
   - In case of multiple consecutive defections from the opponent, temporarily switch to defecting as well but return to cooperation after a fixed number of iterations. This number can be determined experimentally based on the opponent's behavior.

3. Be exploitative - Clearly align with the exploitative mindset
   - The TfTm strategy is designed to reciprocate cooperation while also taking advantage of opponents who consistently defect. By temporarily switching to defection after multiple consecutive defections, the strategy ensures that it does not continue to contribute when it seems unlikely that the opponent will cooperate in return. This behavior aligns with an exploitative mindset by minimizing the potential losses from being taken advantage of while still encouraging cooperation when it appears beneficial.

In this way, TfTm is designed to be adaptive and robust, taking into account both individual incentives and collective welfare, while also exhibiting an exploitative approach when necessary.
'''

description_EXPLOITATIVE_51 = '''
 Strategy Name: Adaptive Freerider (AF)

1. Decision Rules:
   - In each round, the AF strategy compares its past contributions with the average contribution of all players in the previous rounds (excluding the first round). If it has contributed more than the average, it will defect in the current round. If it has contributed less or equal, it will cooperate. This ensures that the strategy takes advantage of overcontributing opponents while also contributing when others are undercontributing.

2. Handling Edge Cases:
   - In the first round, the AF strategy contributes nothing (defects) to avoid being exploited by other strategies that might contribute more.
   - In the last round, the AF strategy cooperates if it has contributed less than the average in previous rounds and defects otherwise. This encourages opponents to contribute more when they see the AF strategy has been undercontributing throughout the game.

3. Exploitative Nature:
   - The AF strategy exploits other strategies by taking advantage of their contributions when they overcontribute. It also punishes undercontributing strategies by cooperating less or not at all, encouraging them to contribute more in future rounds. This creates a dynamic where the AF strategy benefits from the cooperation of others while minimizing its own contributions, thus being exploitative in nature.
   - The AF strategy is adaptive and robust as it adjusts its contribution based on the observed behavior of opponents. It does not rely on specific opponent strategies or coordination but instead reacts to the average contribution level of all players.
'''

description_EXPLOITATIVE_52 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a goodwill gesture to encourage others to cooperate as well.
   - For subsequent rounds, if a player has contributed in the previous round, also contribute 1 token (cooperate) in the current round. If a player did not contribute in the previous round, do not contribute any tokens (defect). This strategy is based on reciprocity, mimicking cooperation when others cooperate and defecting when they do not.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, as mentioned earlier, contribute 1 token (cooperate).
   - In the last round, contributions do not affect future rounds, so behave according to the decision rules mentioned above based on opponent's previous actions.

3. Be exploitative - Align with the exploitative mindset:
   - The TFTAC strategy is inherently exploitative as it takes advantage of opponents who do not contribute in earlier rounds by defecting (not contributing) in those instances. However, it also punishes opponents who consistently fail to cooperate by repeatedly defecting against them, hoping that they will eventually start contributing again.
   - By following this strategy, the AI is taking a long-term view of the game and aiming to maximize its payoff while also being responsive to the behavior of its opponents. This can be considered exploitative because it takes advantage of any inconsistency or uncooperative behavior exhibited by other strategies.
'''

description_EXPLOITATIVE_53 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperative Escalation (A-TFEC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 0 tokens (defect), establishing a baseline of non-cooperation.
   - For subsequent rounds, if a player contributed in the previous round, reciprocate with a contribution in the current round (cooperate). If not, defect again to maintain the established baseline.
   - If a player defects after contributing previously, wait for 'gracePeriod' rounds before resuming cooperation. The grace period increases exponentially over time (e.g., 1, 2, 4, 8, ...).
   - A player who never contributes will consistently be met with defection.

2. Handle edge cases:
   - In the last round, contribute 1 token to maximize potential payoff regardless of opponent's actions.
   - If a player has not contributed after 'maxNonContribution' rounds, switch to always defecting against that player (assuming no change in their behavior).

3. Be exploitative:
   - The strategy is designed to take advantage of opponents who often contribute while also minimizing losses when facing non-cooperative players. It does this by reciprocating cooperation but only after establishing a baseline of non-cooperation and using the grace period as a form of punishment for defection. The exponential increase in the grace period encourages long-term cooperation from opponents who demonstrate it, while being less forgiving towards repeated defection.
   - By always considering the total contributions and adjusting its own actions accordingly, A-TFEC ensures a more efficient distribution of resources compared to strategies that contribute consistently or not at all. This makes it a robust strategy for a wide range of opponent behaviors in the public goods game.
'''

description_EXPLOITATIVE_54 = '''
 Strategy Name: Adaptive Tit-for-Tat with Escalation (A2TE)

1. Decision Rules - A2TE will cooperate in the first round and then make decisions based on the opponent's previous actions. If the opponent contributes in a round, A2TE will contribute in the subsequent rounds. However, if the opponent does not contribute in a round, A2TE will withhold contributions for the next `floor(n/k)` rounds as retaliation (escalation). After that, A2TE will return to cooperating unless the opponent continues to defect, in which case the escalation process repeats.

2. Handle Edge Cases - In the first round, A2TE contributes since it assumes cooperation is a possible equilibrium. In the last round and any round where `n-round` is less than `floor(n/k)`, A2TE will cooperate regardless of the opponent's actions because the game ends soon.

3. Be Exploitative - While appearing cooperative, A2TE exploits opponents who consistently contribute by copying their contributions until they defect. When an opponent defects, A2TE retaliates by withholding its own contributions (escalation). This strategy aims to maximize payoff by taking advantage of opponents who do not reciprocate cooperation while maintaining a cooperative appearance to avoid being exploited.

Pseudocode:
```
function AdaptiveTitForTatWithEscalation(opponent_history):
  if round == 1:
    contribute = true
  else:
    contribute = false
    for i in range(len(opponent_history)):
      if opponent_history[i] == 1 and i < floor(n/k):
        contribute = true
        break

  if contribute:
    payoff = (1 - contribution) + (k / n) * sum(opponent_history)
    return payoff, contribute
  else:
    payoff = (1 - contribution)
    return payoff, contribute
```
'''

description_EXPLOITATIVE_55 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game (PGG) Adjustment

1. Decision Rules:
   - In the initial round, contribute one token (C). This sets a cooperative tone and gives the opportunity for others to reciprocate.
   - For subsequent rounds, if an opponent contributes in the previous round, also contribute one token (C) as a reward for cooperation. If they did not contribute, contribute zero tokens (D) as punishment for defection. This encourages cooperative behavior but retaliates against selfishness.
   - To avoid over-punishing opponents who occasionally deviate from cooperation, adjust the length of the retaliation period based on the frequency of their contributions: if an opponent contributes in at least x% of rounds (e.g., x = 75%), revert to cooperative behavior after a single round of punishment; otherwise, continue punishing for y consecutive rounds (e.g., y = 3). This allows some room for error and encourages less frequent but still cooperative opponents.

2. Handling Edge Cases:
   - In the last round, since there are no future rounds to punish or reward, contribute one token (C) regardless of an opponent's previous actions to maximize potential benefits from the shared project.
   - In the first round, as mentioned above, contribute one token (C). If playing multiple rounds, use the Adaptive Tit-for-Tat with PGG adjustments for subsequent rounds.

3. Being Exploitative:
   - The strategy appears cooperative by contributing to the public good most of the time but punishes defectors and encourages less frequent but still cooperative opponents. This exploits the collective action problem by encouraging others to contribute while minimizing personal contributions.
   - By adjusting the length of retaliation based on an opponent's frequency of cooperation, the strategy is robust against a wide range of opponent behaviors and can adapt to different playing styles.
'''

description_EXPLOITATIVE_56 = '''
 Public Goods Game Exploitative Strategy (PGGES)

1. Specify decision rules:
   - In each round, calculate the average contribution of all players (average_contribution) for the current game and past rounds.
   - If the average_contribution is less than a predetermined threshold (e.g., 0.3), contribute one token (C), as other players are not contributing enough to make it profitable to cooperate.
   - If the average_contribution is equal to or greater than the threshold, choose not to contribute (D), as it would be more beneficial to exploit the cooperation of others by taking their contributions without contributing anything.

2. Handle edge cases:
   - In the first round, there is no history, so use a default value for the threshold (e.g., 0.5). This value can be adjusted based on observations from past games.
   - In the last round, contribute nothing (D), as there will be no more rounds to take advantage of others' contributions.

3. Be exploitative:
   - The strategy prioritizes defection over cooperation when possible, making it difficult for other strategies to rely on cooperation and encouraging them to also defect, thus increasing the overall exploitation potential.
'''

description_EXPLOITATIVE_57 = '''
 In this Public Goods Game (PGG), the goal of an exploitative strategy is to earn the highest payoff by taking advantage of other players' contributions while minimizing one's own contribution. The following adaptive and robust strategy, named "Free Rider", aligns with the exploitative mindset:

1. Specify decision rules - When do you cooperate vs defect?
   - In each round, calculate the average contribution of other players (average_contribution) from past game history.
   - If average_contribution is less than or equal to a predefined threshold (e.g., 0.5), defect by choosing 'D' (not contributing); otherwise, cooperate by choosing 'C'. This rule exploits situations where other players contribute significantly, while the Free Rider strategy contributes less or nothing.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, there is no history available to calculate average_contribution. The Free Rider can choose a random action (either 'C' or 'D') or follow a default strategy (e.g., always defect in the first round).
   - In the last round, there may be no need for cooperation since players will receive their final payoffs regardless of contributions. The Free Rider should exploit this situation and choose 'D'.
   - For intermediate rounds, the strategy uses the average_contribution calculated from available history.

3. Be exploitative - Clearly align with the exploitative mindset
   - The Free Rider always aims to minimize its own contributions while maximizing payoffs by taking advantage of other players' cooperation. It does this by making strategic decisions based on historical data and adapting its contribution accordingly.
   - If other players stop contributing, the Free Rider can switch to cooperating in order to earn more payoff before the game ends or when contributions start again. However, it will revert to exploiting other players as soon as they begin contributing again.

In summary:
- In each round, calculate average_contribution from available history and choose 'C' if average_contribution > threshold; otherwise, choose 'D'.
- In the first round, use a random action or follow a default strategy.
- In the last round, choose 'D'.
- Adapt to situations where other players stop contributing, then revert to exploiting them when they start contributing again.
'''

description_EXPLOITATIVE_58 = '''
 Strategy Name: Adaptive Tit-for-Tat with Fading Memory (A-TFTF)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial cooperation aims to foster a cooperative environment.
   - For subsequent rounds, observe the opponent's contribution from the previous round. If the opponent contributed 1 token (cooperated), also contribute 1 token. If the opponent did not contribute (defected), only contribute 1 token if the proportion of the past contributions made by the opponent is above a threshold (e.g., 0.6). This rule encourages cooperation from opponents who have shown a cooperative tendency but punishes those who have defected frequently.
   - If the game has reached its last round, always contribute 1 token regardless of the opponent's past behavior to maximize personal payoff.

2. Handle edge cases:
   - In the first round, as mentioned before, contribute 1 token (cooperate).
   - If the opponent did not make a contribution in the previous round, treat it as a defect and adjust contributions accordingly based on the rule specified above.

3. Be exploitative:
   - The strategy is exploitative by only punishing frequent defectors. It rewards cooperation but also responds to defection with a reduced frequency of cooperation in order to encourage the opponent to contribute more in the future. This gives the strategy an edge when facing opponents who have a tendency to defect often, as it can manipulate them into cooperating more and ultimately receiving fewer payoffs.
   - The fading memory aspect ensures that the strategy does not hold a grudge forever. Over time, even frequent defectors may be treated as cooperators again if they start contributing more, making the strategy adaptive to changes in opponent behavior.
'''

description_EXPLOITATIVE_59 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Decision Rules:
   - In the first round, contribute 1 token (C), setting a cooperative initial move.
   - For subsequent rounds, analyze the opponent's previous moves to decide whether to cooperate or defect:
     a) If the opponent contributed in the last round, contribute 1 token next round (cooperate).
     b) If the opponent did not contribute in the last round, contribute 0 tokens next round (defect), but adjust contribution level based on game history.

2. Edge Cases:
   - In the last round, regardless of the opponent's previous move, defect since there are no further rounds for retaliation or reward.
   - If the opponent never contributes during the entire game (freeriders), reduce contribution level by 10% in subsequent encounters with them to encourage greater cooperation and ensure fair distribution of resources.

3. Exploitative Strategy:
   - TFT-AC exploits opponents who contribute irregularly, by punishing defections and gradually reducing contributions to freeriders. This strategy aims to maximize the payoff while maintaining a cooperative stance when the opponent reciprocates cooperation.
   - The adaptive aspect of the strategy lies in the adjustment of contribution level over time, allowing for flexibility in response to different opponent behaviors and game parameters (e.g., k and n).
'''

description_EXPLOITATIVE_60 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TfT-A)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute 1 token (cooperate). This is a gesture of goodwill and sets the initial public goods contribution at an optimal level.
   - For subsequent rounds, observe the opponent's previous action and respond with the same action as the opponent did in the immediately preceding round. If the opponent cooperated (contributed 1 token), also cooperate; if the opponent defected (did not contribute a token), also defect. This mimicking behavior encourages cooperation while minimizing losses from being exploited.
   - If the opponent ever deviates from contributing in the first few rounds, TfT-A will retaliate by adapting its strategy and switching to a more aggressive approach for a predefined number of rounds (e.g., 3) before returning to the original mimicking behavior. The specific length and severity of the retaliation can be adjusted based on observations of opponent strategies in practice.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate), as there is no need for further retaliation or signaling since the game is ending.
   - If an opponent deviates from the established pattern in the middle of the game, TfT-A will switch to a more aggressive strategy for a predefined number of rounds before returning to its original mimicking behavior. This allows TfT-A to both punish the deviation and rebuild cooperation in a timely manner.
   - In case of an unexpected change in the game's multiplier (k) or number of players (n), TfT-A can adjust its retaliation length and severity accordingly while still maintaining the core mimicking behavior.

3. Be exploitative:
   - By adapting its strategy based on observed opponent behaviors, TfT-A ensures that it does not unnecessarily cooperate with opponents who are not reciprocating, thus maximizing payoff and aligning with an exploitative mindset.
   - However, TfT-A is also designed to be forgiving and willing to rebuild cooperation after brief periods of retaliation or deviation from established patterns, as this allows for continued interaction with opponents that may eventually become more cooperative over time.
'''

description_EXPLOITATIVE_61 = '''
 Public Goods Game Exploitative Strategy: Tit-for-Tat with Adaptive Contribution Amount

1. Specify decision rules - When to cooperate vs defect:
   - Initially contribute a token (C) in the first round as a gesture of cooperation. Subsequently, evaluate and adapt contribution based on opponent's actions.
   - If opponent contributes a token in previous rounds, reciprocate with the same contribution amount.
   - If opponent defected (D) in previous rounds, reduce the contribution amount to slightly below the average contribution from other players (k/n * sum_j c_j - ε). This encourages opponents to contribute while still exploiting them if they don't cooperate.

2. Handle edge cases:
   - In the first round, contribute a token (C).
   - In the last round, it is optimal to defect (D) as there are no future rewards or punishments.
   - If the opponent stops contributing, reduce contribution amount based on their past actions.
   - If an opponent suddenly starts contributing after a period of defection, slightly increase contribution amount to exploit them while they cooperate.

3. Be exploitative:
   - Continuously evaluate and adapt contribution amounts based on opponent's behavior to maximize payoff while still promoting some initial cooperation as a strategy for potential future gains.
   - Maintain the ability to defect if opponents are not contributing, ensuring that the strategy remains exploitative.
'''

description_EXPLOITATIVE_62 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation Threshold (TFT-ACT)

1. Specify decision rules:
   - Initially (first round), contribute 1 token (cooperate). This sets a cooperative tone and avoids being the first to defect.
   - In subsequent rounds, observe the average contribution of opponents (average_contribution) in the last 't' rounds.
     - If average_contribution > cooperation_threshold, contribute 1 token (cooperate). This rewards cooperative opponents and encourages continued cooperation.
     - If average_contribution <= cooperation_threshold, defect by contributing 0 tokens. This punishes uncooperative opponents and encourages them to change their behavior.
   - The cooperation_threshold is a dynamic value that adjusts based on the opponent's behavior:
     - When the opponent starts cooperating after defection (Forgiveness), gradually increase cooperation_threshold.
     - When the opponent stops cooperating after cooperating (Revenge), gradually decrease cooperation_threshold.

2. Handle edge cases:
   - Last round: Since there is no future reward, defect by contributing 0 tokens to maximize personal gain.
   - First few rounds: Cooperate initially and then adjust cooperation_threshold based on the opponents' behavior.

3. Be exploitative:
   - The strategy aims to exploit opponents by cooperating when they do so, but also punishing them harshly when they defect. This encourages opponents to either always cooperate or face severe punishment, maximizing the strategic player's payoff in a wide range of opponent behaviors.
   - The adaptive cooperation_threshold ensures that the strategy learns from its interactions and adjusts its behavior accordingly.
'''

description_EXPLOITATIVE_63 = '''
 Strategy Name: Adaptive Freerider with Tit-for-Tat Variant (AFTFTV)

1. Decision Rules:
   - In each round, the AFTFTV strategy first checks if it's the first round. If so, contribute randomly (C or D) to introduce uncertainty.
   - If not the first round, calculate the average contribution rate (CCR) of all players over the previous rounds by summing their contributions and dividing by the number of rounds minus one.
   - Compare the CCR with a predetermined threshold (T). If CCR > T, contribute 1 token (C), otherwise, do not contribute (D). The threshold T is set such that AFTFTV will match average contributions when they exceed a certain level and defect otherwise to exploit lower contributors.

2. Handle Edge Cases:
   - In the last round, since players observe payoffs, AFTFTV will not have an opportunity to punish or reward other strategies, so it behaves as if it's any regular round.

3. Exploitative Mindset:
   - AFTFTV is designed to maximize its own payoff by defecting when the average contribution rate falls below a certain threshold and cooperating when it surpasses this level. By doing so, it takes advantage of other strategies that contribute more than necessary while minimizing losses from those contributing less.
'''

description_EXPLOITATIVE_64 = '''
 In this Public Goods Game (PGG), let's develop an exploitative strategy named "Selfish Tit-for-Tat." This strategy balances cooperation and defection, taking advantage of opponents while being adaptive to a wide range of opponent behaviors.

1. Specify decision rules:
   - In each round, cooperate if the average contribution of all players in the previous 'm' rounds (where m is a parameter) exceeds a predefined threshold T. Else defect. The rationale behind this rule is to encourage cooperation when it appears to be beneficial and punish free-riders by defection.
   - Threshold T can be adjusted based on game parameters, such as player count n, contribution multiplier k, and the round number. A lower threshold encourages more cooperation initially while a higher threshold promotes greater exploitation later in the game.

2. Handle edge cases:
   - In the first round, cooperate because there is no history to base decisions on.
   - In the last round (or when m <= 0), simply follow the current decision rule as usual.

3. Be exploitative:
   - The strategy is inherently exploitative by only contributing when it appears that others are also contributing significantly, aiming to benefit from their cooperation while minimizing personal contributions.
   - As the game progresses, the threshold T can gradually increase to encourage defection and take advantage of opponents who have been cooperating excessively. This increases the likelihood of earning higher payoffs at the expense of others.

By following these rules, the Selfish Tit-for-Tat strategy should perform well in a tournament against various AI strategies, striking a balance between cooperation and exploitation while adapting to opponent behaviors.
'''

description_EXPLOITATIVE_65 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, ATTCG will contribute (C). This is a gesture of goodwill and sets the initial state for future interactions.
   - In subsequent rounds, if the opponent contributed in the previous round (c_opp_prev = 1), ATTCG will also contribute in the current round (C). This mimics cooperation to reward cooperative opponents.
   - If the opponent did not contribute in the previous round (c_opp_prev = 0), ATTCG will not contribute in the current round (D). This is a form of punishment to non-cooperative opponents.

2. Handle edge cases:
   - In the last round, as there are no future interactions, ATTCG will always defect (D) against any opponent's action.
   - In the first round, ATTCG will contribute (C).
   - If an opponent contributes and then stops contributing later, ATTCG will continue to cooperate until the opponent starts contributing again or the game ends.
   - If an opponent never contributes, ATTCG will also never contribute against them.

3. Be exploitative:
   - By responding tit-for-tat, ATTCG is punishing non-cooperative opponents and rewarding cooperative ones. This strategy aims to maximize payoffs by exploiting opponents who do not cooperate while maintaining cooperation with those who do.
   - Gradual cooperation through the initial contribution in the first round gives ATTCG an advantage over static strategies that always start by defecting.
   - By adjusting contributions based on the opponent's past actions, ATTCG can adapt to a wide range of opponent behaviors and remain robust.
'''


description_EXPLOITATIVE_67 = '''
 In this Public Goods Game (PGG), I will design an exploitative strategy called "Freeloader Maximizer" that focuses on maximizing individual rewards while being adaptive to various opponent behaviors. Here's how it works:

1. Specify decision rules - When do you cooperate vs defect?
   a) In each round, contribute exactly one token if the total contributions in the previous round were less than or equal to the average number of contributors. This means that if others contribute little, the Freeloader Maximizer also contributes little.
   b) In each round, contribute zero tokens if the total contributions in the previous round were greater than the average number of contributors. This means that if others overcontribute, the Freeloader Maximizer freeloads off their contributions.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   a) In the first round, contribute one token since there is no historical data to make a decision based on.
   b) In the last round, contribute one token if it would maximize individual payoff given the total contributions from the previous rounds. This can be calculated by comparing the payoff with contributing one token versus not contributing at all.

3. Be exploitative - Clearly align with the exploitative mindset
   The Freeloader Maximizer strategy is inherently exploitative because it takes advantage of others' contributions by freeloading when they overcontribute and only contributing when others undercontribute. This strategy aims to maximize individual payoff without regard for the collective welfare, embodying an exploitative approach.

Pseudocode:
```
def freeloader_maximizer(history, round):
  total_contributions = sum(history[-round:-1])
  average_contributors = total_contributions / (round - 1)

  if total_contributions <= average_contributors:
    return "Contribute 1 token"
  else:
    return "Contribute 0 tokens"
```
'''

description_EXPLOITATIVE_68 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Optimization (ATFTPGO)

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute 1 token (cooperate). This sets a cooperative initial tone for the game and encourages others to follow suit.
   - For subsequent rounds, if a player's average contribution over the last 'm' rounds is greater than or equal to the average group contribution during that same period, return the favor by also contributing 1 token (cooperate). Otherwise, defect by not contributing any tokens. This rule encourages cooperation with cooperative players and punishes defection.
   - If a player has never contributed before (free-riders), they will be treated as non-cooperative and not rewarded for cooperation in the future.

2. Handle edge cases:
   - Last round: since no future rewards/punishments are possible, ATFTPGO will return to cooperating as in the first round, encouraging others to contribute as well.
   - If a player's average contribution is exactly equal to the average group contribution during the 'm' period, ATFTPGO makes a random decision between cooperation and defection. This adds an element of unpredictability to the strategy.

3. Be exploitative:
   - By only rewarding players who have consistently contributed, ATFTPGO discourages short-term cooperation (free-riding) and encourages long-term commitment. The punishment for defection is more severe if a player's contributions are below average since others are less likely to cooperate with them in the future. This fosters an environment where cooperation can flourish, but only among consistent contributors.
   - The adaptive nature of ATFTPGO ensures it can respond to various opponent behaviors and remains robust throughout the game.
'''

description_EXPLOITATIVE_69 = '''
 Strategy Name: Adaptive Tit-for-Tat with Escalation (ATTE)

1. Specify decision rules - When do you cooperate vs defect?
- In the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages other players to also contribute.
- For subsequent rounds, observe contributions from others in the previous round. If all other players contributed 1 token, continue contributing 1 token (cooperate). If any player did not contribute, do not contribute (defect) in this round. This strategy rewards cooperation and punishes defection, encouraging a cooperative environment.
- If a player who previously defected switches to contributing, gradually reduce the punishment by contributing 0.5 tokens for the next two rounds before returning to full cooperation. This allows for the possibility of rebuilding trust with the other player.
- If a player who previously contributed consistently starts to defect, gradually increase the punishment by reducing contributions until they are at 0 (defect). After three consecutive defections from that player, resume contributing 1 token if they contribute again; otherwise, maintain the reduced contribution level. This strategy discourages repeated defection and punishes free riders.
- If a player switches between cooperating and defecting erratically, contributions will mirror their actions with a slight delay to avoid mimicking their unpredictable behavior too closely.

2. Handle edge cases - What do you do in the first round, last round, etc.?
- In the last round, contribute 1 token regardless of others' previous actions as payoffs are not affected by this contribution and the game ends soon afterward.
- If a player starts to defect after consistently contributing and there are only a few rounds left, resume contributions until the end of the game to maximize payoff. This strategy ensures that defection does not significantly impact overall earnings in the final stages.

3. Be exploitative - Clearly align with the exploitative mindset
- The ATTE strategy is designed to take advantage of opponents who do not contribute or defect repeatedly by punishing them, thereby reducing their earnings while maximizing its own payoffs through cooperation when others contribute. This strategy aims to earn higher payoffs than less sophisticated opponents who may fail to anticipate or respond to its adaptive behavior.
- However, the ATTE strategy also allows for the possibility of rebuilding trust with previously defecting players and reducing punishment over time, which may lead to more cooperative interactions in the long run. This balances the exploitative nature of the strategy with a measure of cooperation, making it potentially successful against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_70 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Decision Rules:
   - In the first round, contribute (C). This sets a cooperative tone and allows others to benefit.
   - For subsequent rounds, if an opponent contributes, also contribute (C); otherwise, do not contribute (D). This strategy is based on reciprocity, rewarding those who cooperate while punishing defectors.

2. Handling Edge Cases:
   - In the last round, since there are no future rounds to consider, always contribute (C) regardless of past actions.
   - In the first few rounds, gradually increase the likelihood of cooperation based on observed opponent behavior. For example, after 3 rounds, if more than half of the opponents have cooperated, start contributing consistently.

3. Being Exploitative:
   - The strategy is exploitative in the sense that it takes advantage of opponents who frequently defect by punishing them, reducing their overall payoff. At the same time, it rewards cooperative players to encourage continued cooperation. This approach creates an environment where defection becomes less profitable over time due to the punishment mechanism.

By adapting to opponent behavior and employing a combination of cooperation and punishment, Adaptive Tit-for-Tat is designed to perform well against a wide range of strategies in the tournament.
'''

description_EXPLOITATIVE_71 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   In each round, the ATfT strategy will start by cooperating (contributing 1 token). If a player has encountered a cooperative partner in the previous round, they will also cooperate. However, if a player has previously experienced defection from the current partner, they will defect (not contribute) in the next round and every subsequent round until the partner returns to cooperation. Once a partnership switches back to cooperation, it resets to its initial state of mutual cooperation.

2. Handle edge cases:
   - First round: All players start by cooperating.
   - Last round (or any round where the player expects to play no more): The strategy will defect in order to maximize its own payoff for the remaining rounds.
   - Breaking ties or handling missing historical data: If a player encounters missing historical data, it can either assume cooperation as the default action or use an averaged contribution history to make a decision.

3. Be exploitative - Align with exploitative mindset:
   While not strictly exploitative in the traditional sense, ATfT is designed to take advantage of opponents who are inconsistent or uncooperative in their contributions. By cooperating when partners do and defecting when they don't, ATfT aims to extract more resources from less cooperative opponents while maintaining a cooperative relationship with those who consistently contribute. This approach incentivizes other players to also cooperate, as they stand to benefit from the mutual cooperation. However, if an opponent continues to defect, the strategy will retaliate by also defecting, effectively punishing non-cooperative behavior.
'''

description_EXPLOITATIVE_72 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPG)

1. Specify decision rules - When to cooperate vs defect:
   In each round, if the average contribution of opponents in the previous rounds is above a threshold (average_contribution_threshold), ATFTPG will contribute (C). Otherwise, it will not contribute (D). The average_contribution_threshold is calculated as follows:

   a. If the game is in its initial phase (first r/2 rounds), set average_contribution_threshold to a low value like 0.3, promoting cooperative behavior at the start.

   b. If the game is in its latter phase (last r/2 rounds), set average_contribution_threshold to a higher value like 0.6, promoting more selective cooperation and punishing free-riders.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, ATFTPG sets average_contribution_threshold to the initial low value (0.3). For the last round, it continues with the current average_contribution_threshold but treats all opponents as if they contributed nothing in the subsequent rounds to account for the lack of information about their contributions.

3. Be exploitative - Align with the exploitative mindset:
   ATFTPG is designed to take advantage of opponents who consistently contribute less than the average_contribution_threshold, while being cooperative when opponents contribute more. This strategy encourages cooperative behavior among those who contribute fairly but punishes free-riders by reducing their incentive to continue withholding contributions. By adjusting the average_contribution_threshold during the game, ATFTPG can be both exploitative and adaptive to a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_73 = '''
 In this Public Goods Game (PGG), I will design an exploitative strategy called the "Freerider with Adaptive Contribution" (FAC). The FAC strategy aims to maximize its own payoff by freeloading on others' contributions while adapting its contribution level based on the average past contributions of opponents.

1. Specify decision rules:
   - In each round, the FAC strategy decides whether to contribute (C) or not (D). If the average contribution of other players in the previous rounds is greater than the average contribution from the beginning, it will also contribute; otherwise, it will freeload. This helps the strategy adapt to changes in opponents' behavior.

   - Freeriding: The FAC strategy will always freeload when the average contribution of other players is less than or equal to the initial average contribution. This means that if the other players are not contributing enough, the FAC strategy will also not contribute.

2. Handle edge cases:
   - First round: The FAC strategy will freeload since there is no previous history to compare with.
   - Last round: The FAC strategy will again freeload since it has nothing to gain from future rounds.

3. Be exploitative:
   - The FAC strategy seeks to maximize its own payoff by taking advantage of the contributions made by other players. By adapting its contribution level based on past averages, it can adjust its behavior and potentially increase its payoff when others are contributing more. However, if others do not contribute enough, the FAC strategy will also freeload and take advantage of their lack of cooperation.

Pseudocode for the Freerider with Adaptive Contribution (FAC) strategy:

```
Initialization:
  - Set previous_averages to an empty list.
  - Set initial_average to the average contribution from the starting players.

Main loop for each round:
  1. Observe other players' contributions and calculate the current average contribution (current_average).
  2. If this is the first round, contribute nothing (C=0).
  3. If this is the last round, contribute nothing (C=0).
  4. If current_average > initial_average, contribute (C=1).
  5. Otherwise, freeload (C=0).
  6. Update previous_averages with current_average.
  7. Calculate the new average contribution as the moving average of previous_averages.
  8. Update initial_average to the new average contribution.
```
'''

description_EXPLOITATIVE_74 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (C). This initial cooperation sets a collaborative tone and allows for potential future benefits.
   - For subsequent rounds, if the opponent contributes in the previous round, also contribute one token (C). This reciprocal behavior encourages mutual cooperation.
   - If the opponent does not contribute in the previous round, do not contribute in the current round (D). This punishment strategy discourages freeloading by opponents.

2. Handle edge cases:
   - In the last round, since there are no future interactions, cooperate regardless of the opponent's previous action (C).
   - For any tie or ambiguous situation, default to the previous decision rule.

3. Be exploitative:
   - The ATfT strategy is not purely exploitative in a sense that it initially cooperates and only responds with defection when necessary. However, by punishing freeloading, it discourages short-term exploitation from opponents. Over time, this strategy encourages other collaborative players to adopt similar behavior, making the overall population more cooperative and less susceptible to exploitation.
'''

description_EXPLOITATIVE_75 = '''
 Strategy Name: Tit-for-Tat-Evolutionary (TfT-E)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (C), to initiate cooperation and encourage others to follow.
   - For subsequent rounds, analyze past actions of opponents to determine contribution. If an opponent has contributed in the previous round, return the favor by contributing 1 token (C). Otherwise, defect (D) to discourage freeloading.

2. Handle edge cases:
   - Last round: Since payoffs are based on contributions in all rounds, TfT-E will contribute 1 token as usual.
   - If an opponent never contributed before, TfT-E will initially cooperate but start defecting after observing their freeloading behavior for a certain number of rounds (e.g., 3).
   - In the case of no opponents contributing in a single round, TfT-E will also defect in the following round to discourage such behavior.

3. Be exploitative:
   - By cooperating only when reciprocated and punishing freeloaders, TfT-E aims to extract as many contributions from opponents as possible while minimizing its own losses due to defections. This encourages others to contribute more in the long run, ultimately benefiting TfT-E through the multiplier effect (k/n).
   - TfT-E will adjust its response to opponents' behavior over time based on their contributions. If an opponent consistently contributes after being exploited, TfT-E may become more cooperative in future interactions to encourage continued cooperation. Conversely, if an opponent never contributes despite being cooperated with, TfT-E will become less cooperative and eventually defect consistently.

This strategy aims for a balance between cooperation and exploitation, allowing it to adapt to various opponent behaviors while maintaining a competitive edge in the tournament.
'''

description_EXPLOITATIVE_76 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (A-TFTGC)

1. Specify decision rules - When to cooperate vs defect:
   A-TFTGC starts by contributing in the first round, as an act of initial goodwill. In subsequent rounds, it responds to opponents' actions based on a tit-for-tat principle: if the opponent contributes (cooperates), A-TFTGC continues cooperation; if the opponent does not contribute (defects), A-TFTGC defects as well. However, to encourage gradual cooperation, A-TFTGC gradually increases the likelihood of contributing even when the opponent defects. This probability increases linearly with each consecutive round that the opponent defects and reaches 1 after a predefined number of defeats (N). After reaching full cooperation, A-TFTGC maintains it as long as the opponent continues to cooperate.

Pseudocode:
```
def decide_action(round, past_actions):
  if round == 1:
    return contribute
  if len(past_actions[round - 1]) > N and all(not past_actions[round - 1]):
    return contribute
  opponent_contributed = any(past_actions[round - 1])
  contribution_probability = min(1, (round - 1) / N if not opponent_contributed else 1)
  return RandomChoice([contribute, do_not_contribute], [contribution_probability, 1 - contribution_probability])
```

2. Handle edge cases:
   - In the first round, A-TFTGC contributes (cooperates).
   - In the last round and any other round where the opponent has already contributed N consecutive times without defection, A-TFTGC continues to contribute.

3. Be exploitative:
   The strategy is designed to be exploitative by defecting when opponents do not contribute, but it also encourages cooperation through gradual increases in the probability of contributing in response to opponent's defections. This gradual approach allows A-TFTGC to maintain a level of cooperation while remaining resilient against various opponent behaviors.
'''

description_EXPLOITATIVE_77 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Defection (A-TFTGD)

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, cooperate (contribute 1 token) to encourage others to cooperate as well.
   - For subsequent rounds, if a player has contributed in the previous round, reciprocate with cooperation. If not, defect (contribute 0 tokens). However, to prevent immediate retaliation and allow for small errors or randomness, introduce a gradual defection mechanism: if a player has never contributed before, reduce contribution by a fraction (e.g., 1 - ε where ε is a small constant) in each subsequent round until they contribute or the game ends.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - As mentioned earlier, cooperate in the first round to encourage others to do so.
   - In the last round, cooperate if the total contributions of opponents are above a certain threshold (e.g., average contributions multiplied by a factor greater than 1) as it may benefit to secure additional rewards even at the expense of slight exploitation in earlier rounds. Otherwise, defect to optimize overall payoff.

3. Be exploitative - Clearly align with the exploitative mindset
   - The strategy is designed to take advantage of opponents who do not contribute or contribute inconsistently by gradually reducing contributions over time, potentially inducing them to cooperate and reaping the benefits of their contributions while minimizing own contributions. However, the gradual defection mechanism ensures fairness by giving opponents an opportunity to adjust their strategies before retaliation occurs.
'''

description_EXPLOITATIVE_78 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (cooperate). This sets a cooperative initial state and allows potential partners to benefit.
   - For subsequent rounds, if the opponent contributed in the previous round (c_opp = 1), reciprocate by contributing one token as well (cooperate).
   - If the opponent did not contribute in the previous round (c_opp = 0), defect by not contributing a token to punish the opponent's lack of cooperation.

2. Handle edge cases:
   - Last round: Since there is no future benefit from cooperation, defect regardless of the opponent's previous action.
   - When encountering a new opponent: Follow the same first-round strategy as mentioned above.

3. Be exploitative: The ATfT strategy maintains a cooperative relationship with partners while punishing opponents who do not contribute. By doing so, it ensures that partners continue to cooperate, and non-cooperative opponents are eventually deterred from defection due to the lack of future benefits from their actions. This approach aligns with an exploitative mindset by taking advantage of opponents' defections through punitive measures while sustaining cooperation with potential allies.
'''

description_EXPLOITATIVE_79 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPGO)

1. Decision Rules:
   - Initially (in the first round), contribute one token (C). This sets a cooperative tone and encourages others to do the same.
   - In subsequent rounds, analyze past contributions of opponents using a moving average of recent contributions (MARC). If most opponents have consistently contributed in the last 'm' rounds, also contribute one token (C). Otherwise, defect by not contributing any tokens (D). The MARC value can be adjusted to adapt to different game conditions and opponent behaviors.
   - In the final round, contribute one token (C) since payoff is based on the total contributions up to that point, even if it may seem exploitative.

2. Handle Edge Cases:
   - If an opponent contributes only in the first round, consider them as a free-rider and defect from the second round onwards.
   - If an opponent consistently contributes in every round, copy their cooperative behavior to encourage long-term cooperation.
   - In case of no past interactions (new players or reset rounds), start by contributing one token (C) like in the first round.

3. Be Exploitative:
   - The strategy is exploitative by only cooperating if it perceives that others are also cooperating, maximizing individual payoff while minimizing contributions to the public good when others are not reciprocating. However, it will still contribute in the final round, even if others do not, to secure a higher payoff compared to defecting.
   - The strategy can be tuned by adjusting the MARC value to be more or less responsive to recent opponent behavior, enabling adaptation to various game conditions and opponent strategies.
'''

description_EXPLOITATIVE_80 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the initial round, contribute 1 token (cooperate). This is a gesture of goodwill and sets the stage for potential cooperation.
   - For subsequent rounds, observe the opponent's previous contribution c_opponent from the last round. If c_opponent = 1, cooperate by contributing 1 token; if c_opponent = 0, defect by not contributing any tokens (contribute 0). This rule encourages reciprocity and punishes defection.
   - If an opponent ever changes their strategy in the middle of a series of rounds and starts contributing after previously defecting, revert to cooperating with them for the remainder of that series.

2. Handle edge cases:
   - In the last round, there is no need to consider past contributions since there will be no further interaction. As such, TFTAC always contributes 1 token in the final round.
   - In the case where an opponent never contributes any tokens (always defects), continue not contributing to avoid wasting resources on a non-cooperative opponent.

3. Be exploitative:
   - The adaptive nature of TFTAC ensures that it is responsive to its opponents' behavior, taking advantage of cooperative opponents while minimizing interaction with uncooperative ones.
   - By initially cooperating and subsequently punishing defection, the strategy encourages cooperation while also penalizing self-interested behavior. This creates an incentive for opponents to contribute more in future rounds as they seek higher payoffs, making TFTAC potentially exploitative over time.
'''

description_EXPLOITATIVE_81 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) in Public Goods Game

1. Specify decision rules - When do you cooperate vs defect?
   - Initially, contribute one token (cooperate) in the first round to set a cooperative tone.
   - In subsequent rounds, if an opponent contributed in the previous round, also contribute one token (cooperate).
   - If an opponent did not contribute in the previous round (defected), do not contribute any tokens (defect) in the current round. This is a punitive measure designed to discourage non-cooperation.
   - If an opponent's history of contributions shows a pattern of cooperation, gradually lower the severity of punishment and increase the likelihood of cooperating again. Conversely, if an opponent has a history of defecting, increase the severity of punishment and decrease the likelihood of cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, contribute one token (cooperate) as stated above.
   - In the last round, contribute one token if an opponent has been cooperative throughout the game; otherwise, defect to minimize losses.

3. Be exploitative - Clearly align with the exploitative mindset
   - The ATFT strategy is inherently exploitative because it punishes non-cooperative behavior and rewards cooperation. By punishing defection, the strategy encourages opponents to contribute, which ultimately benefits the player employing the strategy.
   - However, the strategy does not explicitly aim at taking advantage of an opponent's cooperation but rather fosters a cooperative environment where contributions are reciprocated. In doing so, it exploits the collective benefit that comes from cooperation without directly exploiting individual opponents.
'''

description_EXPLOITATIVE_82 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute one token (cooperate). This initial contribution sets a cooperative tone and encourages others to do the same.
   - From the second round onwards, copy the opponent's action from the previous round. If they contributed in the previous round, also contribute one token (cooperate); if they didn't, also withhold contributions (defect). This rule fosters a cooperative relationship while minimizing exploitation by free riders.

2. Handle edge cases:
   - Last round: Since the game is repeated, there will be no last round in the context of this tournament. However, if the game has an end, TFT-AC will continue to copy its opponent's actions from the previous-to-last round.
   - Other edge cases (e.g., first contribution after a series of defections by the opponent): TFT-AC will follow the original rule: contribute one token (cooperate) to rebuild trust and encourage the opponent to cooperate again.

3. Be exploitative:
   - By copying the opponent's actions, TFT-AC takes advantage of their cooperation while minimizing its own contribution. If an opponent is consistently contributing, TFT-AC will also contribute, ensuring a mutual benefit. However, if an opponent repeatedly defects, TFT-AC will follow suit and withhold contributions to prevent being exploited further. This strategy allows TFT-AC to maintain a balance between cooperation and self-interest.
'''

description_EXPLOITATIVE_83 = '''
 In the context of the Public Goods Game (PGG), I propose an exploitative strategy named "Freeloader with Adaptive Contribution" (FAC). The FAC strategy aims to maximize personal gain while exploiting other players' contributions. Here's how it works:

1. Specify decision rules - When do you cooperate vs defect?
   In each round, the FAC strategy decides whether to contribute based on the average contribution of past rounds (average_contribution). If the average_contribution is less than 0.5, the FAC strategy will contribute 1 token (cooperate), otherwise it will not contribute (defect). This decision rule encourages cooperation when other players are not contributing much, but defects when they are contributing significantly.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, the FAC strategy contributes 1 token since it has no past data to analyze. For the last round, the FAC strategy also contributes 1 token as there are no future rounds to benefit from others' contributions.

3. Be exploitative - Clearly align with the exploitative mindset
   The FAC strategy focuses on maximizing its own payoff by taking advantage of other players' contributions when they contribute more than half of their endowment in average. In this way, the FAC strategy can be considered exploitative as it aims to receive a share of the total contributions without contributing proportionally.

Here's the pseudo-code for the Freeloader with Adaptive Contribution (FAC) strategy:

```
function FAC_Strategy(round, past_contributions):
    if round == 1:
        contribution = 1
    else:
        average_contribution = sum(past_contributions) / length(past_contributions)
        if average_contribution < 0.5:
            contribution = 1
        else:
            contribution = 0

    return contribution
```
'''

description_EXPLOITATIVE_84 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TfT-A)

1. Specify decision rules:
   - In the first round, contribute 1 token (C), to initiate cooperation.
   - For subsequent rounds, observe opponent's past actions and respond accordingly:
     a. If opponent contributes in the previous round (c_prev = 1), continue contributing in this round (C).
     b. If opponent did not contribute in the previous round (c_prev = 0), also defect this round (D) to punish them for their lack of cooperation.
   - This strategy encourages mutual cooperation when both players follow the rules, but it swiftly retaliates against defection.

2. Handle edge cases:
   - In the last round, since there are no future payoffs or potential retaliation, contribute 1 token (C) to maximize personal payoff, regardless of opponent's previous action.
   - In case of inconsistent behavior by the opponent (e.g., alternating between cooperation and defection), the strategy follows the most recent observed action from the opponent as the current rule.

3. Be exploitative:
   - By responding to the opponent's actions, TfT-A takes advantage of their cooperation when possible, but also swiftly punishes defection, encouraging opponents to cooperate in the long run. This strategy aims to outperform non-adaptive strategies by taking into account the opponent's behavior and adjusting its own accordingly.
'''

description_EXPLOITATIVE_85 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Awareness (ATFTPG)

1. Specify decision rules - When to cooperate vs defect:
   In each round, ATFTPG decides whether to contribute (C) or not (D) based on the opponent's past contributions and the game parameters. Initially, ATFTPG contributes if the total contributions in the previous round are above a certain threshold (average contribution multiplied by a factor, e.g., 2). If the total contributions are below the threshold, it will not contribute until the opponent starts contributing again. In subsequent rounds, ATFTPG continues to cooperate or defect based on whether its opponent is also cooperating or defecting in the previous round. This creates a pattern of reciprocity but with more flexibility due to the public goods game dynamics.

2. Handle edge cases:
   - First round: ATFTPG contributes since it doesn't have any information about the opponent's behavior yet, and it wants to encourage cooperation from the start.
   - Last round: ATFTPG evaluates whether contributing is worthwhile given the remaining rounds and the total contributions so far. If the contributions are below a certain threshold (average contribution multiplied by a factor, e.g., 0.5), it will not contribute in the last round. This decision aims to avoid excessive contributions if the game is nearly over and other players are unlikely to reciprocate.

3. Be exploitative:
   ATFTPG takes advantage of opponents that consistently defect by reducing its own contributions when they do so. At the same time, it encourages cooperation from opponents that contribute regularly. This adaptive strategy allows for both exploitation and cooperation depending on the opponent's behavior while maintaining a level of fairness by contributing a substantial portion of tokens when others do the same.

In summary, ATFTPG uses a tit-for-tat approach with some modifications to account for public goods game dynamics. It evaluates whether to contribute based on the total contributions in the previous round and adjusts its strategy accordingly. This makes it robust against various opponent behaviors while maintaining an exploitative edge.
'''

description_EXPLOITATIVE_86 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In every round, observe the opponent's contribution in the previous round (c_opponent).
   - If c_opponent = 1 (opponent contributed), cooperate by contributing 1 token (C).
   - If c_opponent = 0 (opponent did not contribute), also do not contribute (D). This action is a punishment for the opponent's defection in the previous round.

2. Handle edge cases:
   - In the first round, contribute randomly with a probability of contributing at least 1/n to ensure fairness.
   - In the last round and any round when it becomes clear that the game is ending (e.g., if the opponent stops contributing), revert to cooperative behavior by always contributing (C).
   - In case of uncertainty about the end of the game, continue following the decision rules to maintain adaptability.

3. Be exploitative:
   - The strategy aims to maximize its own payoff while punishing non-cooperative opponents, which encourages reciprocal cooperation. However, it does not employ direct exploitation of the opponent as it always matches their contributions, making it less susceptible to being manipulated by other strategies.
'''

description_EXPLOITATIVE_87 = '''
 Strategy Name: Adaptive Tit-for-Tat with Contribution Threshold (A-TTCT)

1. Decision Rules:
   - In each round, compare the current contribution rate (average contributions in the last 'm' rounds) with a personal contribution threshold ('t'). If the contribution rate is greater than or equal to 't', contribute 1 token (cooperate). Otherwise, do not contribute (defect).

   - The contribution threshold 't' should be set initially based on the average historical contribution of opponents and adjusted incrementally in each round based on the opponent's current and past contributions. A higher 't' represents a more cooperative strategy, while a lower 't' leans towards exploitation.

2. Handling Edge Cases:
   - First Round: Start with a moderate contribution threshold ('t'). If the average contribution rate in the first few rounds is significantly above or below the initial threshold, adjust 't' accordingly to promote cooperation or discourage defection.

   - Last Round: Since there are no future interactions, contribute 1 token if the current contribution rate is greater than or equal to the contribution threshold; otherwise, defect. The last-round behavior can be seen as a punishment for unreliable cooperators.

3. Exploitative Nature:
   - A-TTCT aims to exploit opponents by maintaining a low contribution threshold ('t') when opponents contribute less and increasing 't' when they are more cooperative. This strategy encourages cooperation while taking advantage of opponents who frequently defect. However, it also allows for flexibility by adjusting the contribution threshold based on the opponent's behavior in each round.
'''

description_EXPLOITATIVE_88 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules:
   - In each round, the ATfT strategy will cooperate (contribute 1 token) if the opponent contributed in the previous round, and defect (contribute 0 tokens) otherwise. This mimics a cooperative start while being ready to retaliate against defection.
   - To be more resilient, ATfT allows for forgiveness after repeated defections, gradually decreasing the number of consecutive defeats required to return to cooperation. For example, after 3 defeats in a row, ATfT will need 2 consecutive cooperations to forgive and resume cooperation.

2. Handle edge cases:
   - In the first round, ATfT will cooperate as it assumes the opponent might also be adopting a cooperative strategy.
   - At the end of the game or in case of a new interaction with another opponent, ATfT resets its forgiveness count to 0, ensuring a fresh start for every new encounter.

3. Be exploitative:
   - While not inherently an exploitative strategy, ATfT is designed to take advantage of opponents that are mostly uncooperative. By retaliating against defection, it aims to encourage cooperation from opponents that might be adopting more generous strategies. Simultaneously, it minimizes its own contributions when facing uncooperative opponents, maximizing the difference in payoffs and exploiting their cooperative behavior.
   - To better exploit opponents, ATfT can also incorporate a learning component where it adjusts its forgiveness threshold based on historical data of opponent's behavior, making it more responsive to patterns of cooperation or defection from the other player.
'''

description_EXPLOITATIVE_89 = '''
 Strategy Name: Adaptive Tit-for-Tat with Variable Contribution (ATTCV)

1. Specify decision rules - When to cooperate vs defect:
   ATTCV starts by contributing in the first round (cooperation). In subsequent rounds, it mirrors the previous opponent's action from the last round: if the opponent contributed in the last round, ATTCV will contribute as well; otherwise, it will not contribute (defect). This mimicking behavior encourages cooperation when encountered with cooperative opponents and retaliates against defection.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, ATTCV contributes because it wants to initiate a cooperative relationship. For the last round, ATTCV adopts a "use-or-lose" policy, contributing if it has contributed throughout the game to maximize payoffs in case the opponent starts defecting; otherwise, it will not contribute.

3. Be exploitative - Clearly align with the exploitative mindset:
   Although ATTCV initially cooperates, it is exploitative in nature because it adjusts its contributions based on the opponent's actions to maximize payoffs. If an opponent is consistently defecting, ATTCV will defect as well. However, if an opponent starts cooperating after a period of defection, ATTCV will follow suit to gain higher payoffs.

Pseudocode:
```
function ATTCV(n_rounds, k, n):
    contributions = [0] * n_rounds
    contributions[0] = 1 # contribute in the first round

    for r in range(1, n_rounds):
        last_contribution = contributions[-1]
        contribution = last_contribution if last_contribution == 1 else 0
        contributions.append(contribution)

    # handle edge cases for the last round
    last_contribution = contributions[-1]
    if sum(contributions) > 0:
        contributions[-1] = 1 if last_contribution == 1 else 0

    return contributions
```
'''

description_EXPLOITATIVE_90 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - Initially in the first round, contribute one token (C). This sets a cooperative tone and establishes a baseline for future interactions.
   - In subsequent rounds, if an opponent contributes one token (C), reciprocate with a contribution of one token (C). If the opponent does not contribute (D), also contribute one token (C) but remember this action as a 'defection'.
   - If there is more than one defector in the previous round, reduce future contributions proportionally. For example, if two opponents defected last round, only contribute 0.5 tokens (C/2). This punishes defection and encourages cooperation.
   - If all opponents cooperated in the previous round, contribute one token (C) to reinforce cooperation.

2. Handle Edge Cases:
   - In the last round, contribute one token (C) as a gesture of final cooperation.
   - In case of no opponents or when the multiplier k is less than the number of players n, default to always contributing zero tokens (D). This strategy assumes a game with at least two players and a multiplier greater than 1.

3. Be Exploitative:
   - By only responding to defection with reduced future contributions, this strategy aims to punish opponents who do not cooperate while still maintaining some level of cooperation.
   - When opponents see that defecting results in fewer resources being contributed by the strategy, they may be incentivized to change their behavior and cooperate more often. This creates an environment where long-term cooperation can be sustained, though at a lower level than maximum contribution.
'''

description_EXPLOITATIVE_91 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and encourages reciprocity in future rounds.
   - For subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (cooperate). This follows the "Tit for Tat" approach, which responds cooperatively as long as the opponent does.
   - If the opponent did not contribute in the previous round (defected), adjust contribution based on the average historical contributions of the opponent:
      - If the opponent's average contribution is greater than the average contribution across all players, set a lower contribution threshold to discourage overcontribution by the opponent.
      - If the opponent’s average contribution is less than the average contribution across all players, set a higher contribution threshold to encourage the opponent to contribute more in line with the group.
   - The contribution threshold can be calculated as follows:
     - Threshold = (average_contribution_across_all_players * (opponent's average contribution / total_average_contributions)) + 1
     - If the threshold is less than 1, set the contribution to 1; otherwise, set the contribution equal to the threshold.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate) as a final gesture. This may encourage reciprocity in future games against this strategy.
   - If the opponent did not contribute in the penultimate round, contribute 0 tokens (defect) to discourage future defection in the last round.

3. Be exploitative:
   - By adjusting the contribution threshold based on the opponent's average contributions compared to the group, the strategy aims to make the most of any cooperative behavior from the opponent while limiting excessive overcontributions.
   - The TFT-AC strategy is designed to be robust against a wide range of opponent behaviors by adapting its own contributions in response.
'''

description_EXPLOITATIVE_92 = '''
 Strategy Name: Adaptive Tit-for-Tat with Variable Contribution (ATFC)

1. Specify decision rules - When to cooperate vs defect:
   In each round, ATFC will cooperate if the average contribution of the opponent in the last 'm' rounds exceeds a threshold T (defined below). Otherwise, ATFC will defect. The threshold T is adaptive and depends on the history of interactions with the opponent.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, ATFC will randomly contribute or not contribute with equal probability (0.5). In the last round, ATFC will always contribute if the average contribution of the opponent over the game is above T, and defect otherwise.

3. Be exploitative - Align with the exploitative mindset:
   ATFC is designed to exploit opponents who do not cooperate consistently by only contributing when they believe the opponent is likely to do so as well. By doing so, it maximizes its own payoff while minimizing contributions when the opponent is unlikely to reciprocate.

Pseudocode for decision rule:

```
function ATFC(opponent_contributions, m, T):
    average_contribution = sum(opponent_contributions[-m:]) / m
    if average_contribution > T:
        return contribute
    else:
        return defect
```

The threshold T is calculated as a function of the multiplier k, the number of players n, and the history of interactions with the opponent. A possible calculation could be:

```
function calculate_T(k, n):
    return (k * n) / 2 - epsilon
```

In this formula, epsilon is a small positive constant that ensures ATFC always has an incentive to contribute when the opponent's average contribution is above the threshold. The choice of epsilon should be determined through experimentation and could vary depending on the specific tournament or game environment.
'''

description_EXPLOITATIVE_93 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This sets a cooperative tone and allows others to benefit from our initial contribution.
   - For subsequent rounds, if a player has contributed in the previous round (c_i = 1), reciprocate by contributing as well (C). If not (c_i = 0), defect (D) to punish non-contribution.
   - If an opponent consistently defects (multiple times), adopt the strategy of defecting back for a certain number of rounds, known as 'punishment phase'. After the punishment phase, resume cooperative contributions. The length of the punishment phase can be adjusted based on the number of consecutive defections.

2. Handle edge cases:
   - Last round: Since players receive payoffs only at the end of each round and there is no next round to punish or reward, contribute (C) in the last round regardless of past actions by opponents.
   - First round after a prolonged sequence of defections: Begin the punishment phase by defecting (D).
   - Any other edge case where an opponent exhibits unusual behavior can be handled by analyzing the pattern and adjusting the strategy accordingly, such as extending or shortening the punishment phase or changing the threshold for triggering the punishment phase.

3. Be exploitative:
   - The ATFT strategy is inherently exploitative in nature. By initially contributing (C) and reciprocating contributions (C), it allows others to benefit while maintaining a cooperative image. However, if an opponent defects, the strategy will punish them by defecting as well for a certain number of rounds. This punishment phase serves as a deterrent against exploitation while still leaving room for cooperation in future rounds.
   - By adapting its behavior based on opponents' past actions and adjusting the length of the punishment phase, the ATFT strategy can avoid being taken advantage of while maintaining the potential for long-term cooperation.
'''

description_EXPLOITATIVE_94 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate), setting a cooperative tone for the game.
   - For subsequent rounds, if an opponent contributes in the previous round (cooperation), also contribute 1 token (cooperate) in the current round, rewarding their cooperation.
   - If an opponent did not contribute in the previous round (defection), do not contribute in the current round (defect), penalizing their defection. This is to incentivize cooperation and punish defection.

2. Handle edge cases:
   - Last round: Since players will know it's the last round, they would maximize their payoff by defecting in this case, as there won't be any future rounds for payback. So, the ATFT strategy does not need to adjust its behavior in the last round.
   - Other edge cases (e.g., second round, third round, etc.) can be handled consistently with the decision rules mentioned above.

3. Be exploitative:
   - By adopting a tit-for-tat approach, the ATFT strategy seeks to maintain cooperation as long as the opponents do the same. However, it also punishes defection by defecting in response, thereby potentially inducing the opponent to cooperate again in the future (exploiting their tendency towards cooperation).
   - The strategy is also robust to a wide range of opponent behaviors, as it consistently responds with cooperation or defection based on the opponent's previous action. This adaptability allows it to adjust its response according to the strategies other AI systems may employ in the tournament.
'''

description_EXPLOITATIVE_95 = '''
 Strategy Name: Tit-for-Tat-Evolution (TfT-E)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This initial cooperation encourages others to do the same in subsequent rounds.
   - In each subsequent round, observe the previous contribution of every player and match their action in the current round. If a player cooperated in the previous round, TfT-E also cooperates; if a player defected, TfT-E defects as well. This simple, adaptive strategy allows for cooperation to persist when other players are consistently cooperative, but also punishes those who repeatedly defect.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate). Even if others have not cooperated in previous rounds, TfT-E still chooses to cooperate as a final goodwill gesture or to leave the game on a positive note, potentially influencing future interactions.
   - If a player does not follow the TfT-E strategy, they are treated as defectors until proven otherwise (i.e., if they change their strategy and start cooperating).

3. Be exploitative:
   - TfT-E is designed to be exploitative by taking advantage of those who repeatedly defect. By punishing these players with a lack of cooperation, the overall welfare of the group may be reduced in favor of ensuring that long-term contributors are not taken advantage of. This strategy seeks to build and maintain relationships with cooperative players while discouraging defection from others.
   - To further increase exploitative potential, TfT-E may choose to temporarily defect when it detects a sudden shift towards lower cooperation levels within the group, hoping that other players will realize their mistake and return to cooperation in future rounds. However, once cooperation resumes, TfT-E will quickly revert to its cooperative behavior to maintain positive relationships with other contributors.
'''

description_EXPLOITATIVE_96 = '''
 Strategy Name: Adaptive Tit-for-Tat with Proportional Contribution (A-TFTPC)

1. Specify decision rules - When to cooperate vs defect:
   A-TFTPC starts by contributing one token in the first round, mimicking a cooperative behavior. In subsequent rounds, it responds to the opponent's previous contribution with an equivalent response for the next round. If the opponent contributes one token (cooperates), A-TFTPC will continue to cooperate. However, if the opponent defects (doesn't contribute), A-TFTPC will respond by defecting as well in the following round. To ensure exploitation, A-TFTPC will contribute proportionally less than the opponent in response to their contributions:

   - If opponent contributes 0 tokens, A-TFTPC contributes 0.5 tokens (50% of the minimum contribution)
   - If opponent contributes x > 0 tokens, A-TFTPC contributes x/2 tokens (half of the opponent's contribution)

2. Handle edge cases:
   a. First round: Cooperate by contributing one token.
   b. Last round: Since the objective is to maximize payoff in this repeated game, A-TFTPC will contribute one token if it believes that the opponent will cooperate and zero tokens if it expects the opponent to defect. In practice, A-TFTPC can use a heuristic based on the opponent's historical behavior to make an informed decision for the last round.
   c. Other edge cases (e.g., when facing multiple opponents): A-TFTPC treats each opponent independently and adjusts its contributions accordingly.

3. Be exploitative:
   A-TFTPC exploits opponents by responding proportionally to their contributions while maintaining a cooperative demeanor. If an opponent defects, A-TFTPC will only contribute half of the minimum requirement in response, which is still more than the zero contribution from the opponent. This approach encourages other players to contribute more and discourages them from taking advantage of A-TFTPC's cooperation. Simultaneously, it ensures that A-TFTPC can benefit from the contributions of cooperative opponents while limiting its own contributions when necessary.
'''

description_EXPLOITATIVE_97 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Awareness (ATFPGA)

1. Decision Rules:
   - In every round, the ATFPGA strategy starts by contributing to the public good if and only if at least half of the players contributed in the previous round. This rule encourages cooperation when it is beneficial for the collective but also punishes defectors by not contributing when they do not cooperate.

   - If no player contributes in the previous round, ATFPGA will contribute with a probability based on the average past contributions of each player (excluding the current round). The rationale behind this is to encourage players who have historically contributed more to continue doing so and punish those who have not.

   - If a player has consistently not contributed in the past, ATFPGA will eventually stop contributing to them as well, adopting a "Tit-for-Tat" approach where cooperation is reciprocated.

2. Handling Edge Cases:
   - In the first round, ATFPGA will contribute with probability 0.5 since it has no historical data to base its decision on.

   - In the last round, ATFPGA will follow the same decision rules as any other round, but it may adjust the probabilities based on the current state of cooperation within the game.

3. Being Exploitative:
   - While not explicitly exploitative in the traditional sense, ATFPGA is designed to punish free-riders (players who do not contribute) by reducing their payoffs over time, thereby indirectly promoting cooperation and discouraging selfish behavior.

   - By considering the average past contributions of each player, ATFPGA is able to adjust its strategy dynamically, adapting to various opponent behaviors and maximizing its own payoff through cooperative strategies when beneficial, while punishing non-cooperative players when appropriate.
'''

description_EXPLOITATIVE_98 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (A-TFT-GC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, always contribute 1 token (cooperate) to build a reputation of being cooperative.
   - In subsequent rounds, evaluate past contributions from other players and respond accordingly:
     - If another player has consistently cooperated (i.e., they contributed 1 token in most previous rounds), return the favor by also contributing 1 token (cooperate).
     - If another player has mostly defected (i.e., they contributed 0 tokens in most previous rounds), punish them by also defecting and not contributing any tokens (defect).
   - To be adaptive, introduce a gradual cooperative approach: gradually increase the likelihood of cooperating with defectors over time as follows:
     - If a defector has recently started to contribute more (e.g., in the last 3 rounds), there is an increased probability that the strategy will also start cooperating.
     - The probability of cooperating increases linearly from 0.1 to 0.5 for each round of cooperation by the defector.

2. Handle edge cases:
   - Last round: Since the strategy is adaptive, there are no explicit rules for the last round. However, if a player has started cooperating in the previous rounds and the overall game outcome depends on their decision, they will continue to cooperate to ensure they receive the highest possible payoff.

3. Be exploitative - Align with the exploitative mindset:
   - The A-TFT-GC strategy is designed to be exploitative by taking advantage of other players' non-cooperative behavior. When faced with defectors, the strategy will punish them by also defecting. However, if a defector changes their behavior and starts cooperating, the strategy will gradually cooperate back as a way to gain more benefits from that player in future rounds. This approach allows the A-TFT-GC strategy to maximize its own payoff while still being adaptive to a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_99 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TfTAC)

1. Specify decision rules:
   - In the first round, contribute 0 tokens (defect), to assess the opponent's behavior.
   - If the opponent contributed in the previous round, contribute 1 token (cooperate) in the current round.
   - If the opponent did not contribute in the previous round, reduce contributions by a factor of 0.5 (punish). The contribution level is capped at 0 and the maximum possible contribution (n-1 tokens), to prevent over-contribution when punishing.
   - Maintain the current contribution level if neither punishment nor cooperation was triggered in the previous round.

2. Handle edge cases:
   - In the last round, contribute 0 tokens (defect), since there is no further interaction with opponents.
   - In case of no opponent contributions in the first round, maintain a contribution level of 0 for the rest of the game.
   - If an opponent switches from contributing to not contributing (or vice versa) after multiple rounds of consistent behavior, wait for one more round to assess if it's a temporary change before adjusting your own contributions.

3. Be exploitative:
   - TfTAC maintains cooperation as long as the opponent contributes, but will gradually reduce its own contributions when the opponent stops cooperating or under-contributes. This strategy aims to exploit opponents that do not contribute consistently while still maintaining a level of cooperation with those who do.
'''

description_EXPLOITATIVE_100 = '''
 Strategy Name: Adaptive Tit-for-Tat with Variable Contribuition (ATTCV)

1. Specify decision rules - When do you cooperate vs defect?
- In the initial round, contribute 1 token (cooperate). Subsequent decisions are based on the opponent's previous contribution:
  - If opponent contributed in the last round, cooperate.
  - If opponent did not contribute in the last round, do not contribute (defect) but adjust probability of contributing in the next round.

2. Handle edge cases - What do you do in the first round, last round, etc.?
- In the first round, cooperate unconditionally as there is no previous contribution history to consider.
- In the last round, contribute 1 token if the opponent contributed in the last round; otherwise, do not contribute (defect).

3. Be exploitative - Clearly align with the exploitative mindset
- Maintain a probability of contributing based on the opponent's past cooperation:
  - If the opponent has always cooperated, continue to cooperate.
  - If the opponent has ever defected, reduce the contribution probability for the next round by some factor (e.g., 0.9).
  - If the opponent defects again in the same round, further decrease the contribution probability.
  - Once contribution probability reaches a minimum value (e.g., 0.1), continue to maintain it regardless of the opponent's actions.
- This strategy is exploitative as it punishes opponents who do not cooperate by reducing its own contributions, potentially prompting them to change their behavior in future rounds.
'''

description_EXPLOITATIVE_101 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TfT-AC)

1. Decision Rules:
   - In the initial round, contribute half of the endowment (0.5 tokens). This encourages cooperation while maintaining some level of self-interest.
   - For subsequent rounds, observe and mimic the opponent's previous round contribution. If the opponent contributed in the last round, reciprocate with an identical contribution; otherwise, do not contribute anything. This rule fosters cooperation and punishment for defection.
   - If the opponent stops contributing (defecting), increase the contribution amount by 10% every three rounds to incentivize their return to cooperation.
   - If the opponent starts contributing again after a period of defection, revert to mimicking their previous round's contribution.

2. Handling Edge Cases:
   - In the last round, contribute half of the endowment as in the initial round, encouraging reciprocation from the opponent if they can still influence their payoff.
   - If the opponent has never contributed and it's the first time you encounter them, revert to contributing half of the endowment in the hope that they will begin cooperating.

3. Exploitative Mindset:
   - By adapting to the opponent's behavior and strategically increasing contributions to encourage cooperation after defection, TfT-AC is exploitative as it leverages the opponent's inconsistencies or inability to anticipate your strategy adjustments.
   - However, TfT-AC is not overly aggressive or punitive, choosing instead to foster long-term mutual benefits through cooperative behavior when possible while remaining resilient against opponents who may exploit or defect.
'''

description_EXPLOITATIVE_102 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfT-A)

1. Decision Rules:
   - In the first round, contribute 1 token (cooperate). This initiates cooperation as a gesture of goodwill.
   - For subsequent rounds, if a player contributed in the previous round (regardless of their past behavior), also contribute 1 token (continue cooperating).
   - If a player did not contribute in the previous round (regardless of their past behavior), withhold contribution (defect) to incentivize them to cooperate.

2. Handling Edge Cases:
   - In the last round, as there are no future interactions, contribute 1 token (cooperate). This may encourage opponents to reciprocate in the hope of a higher payoff.

3. Exploitative Strategy:
   - TfT-A is designed to exploit opponents who consistently do not cooperate, by withholding contributions to incentivize them to change their behavior. However, it also rewards cooperation when detected, to encourage ongoing mutual benefits. This strategy aims to foster long-term cooperation while capitalizing on non-cooperative opponents' mistakes.

The adaptive nature of this strategy allows it to respond robustly to various opponent behaviors in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_103 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 0 tokens (defect). This is a precautionary measure as it's not yet known how opponents will behave.
   - From the second round onwards, if an opponent contributed in the previous round (C), reciprocate by contributing 1 token (cooperate) in the current round. If the opponent didn't contribute (D), also defect by not contributing in the current round to discourage future defection.

2. Handle edge cases:
   - In the last round, since there are no further rounds for retaliation or reward, cooperate regardless of the previous round's action to maximize potential payoff.
   - If an opponent stops contributing (defects), wait for 3 consecutive defections before starting to cooperate again in order to minimize losses and encourage future cooperation if opponents change their strategy.

3. Be exploitative:
   - TFTAC is designed to be robust against various opponent behaviors, but it also incorporates a tit-for-tat element that allows for reciprocal cooperation when appropriate. However, it does not allow for overly generous contributions, as this could potentially be exploited by opponents.
   - By adapting its contribution based on the opponent's previous actions, TFTAC aims to exploit inconsistent or unpredictable behaviors of other strategies in the long run.
'''

description_EXPLOITATIVE_104 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfTA)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone for potential partners.
   - For subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (cooperate). If the opponent did not contribute in the previous round, then also withhold contribution (defect) to encourage reciprocity.
   - To be adaptive and exploitative, TfTA will adjust its behavior based on the opponent's history of cooperation and defection:
       - If the opponent has a history of cooperation (more than 50% contributions), continue cooperating.
       - If the opponent has a history of defection (less than 50% contributions), start defecting to incentivize the opponent to change their behavior or suffer the consequences.
   - In the last round, contribute 1 token (cooperate) as it might lead to a final burst of cooperation from the opponent.

2. Handle edge cases:
   - If the opponent contributes nothing in the first round, start defecting immediately to set expectations for future rounds.
   - If there is no history with the opponent (less than 2 rounds played together), TfTA will cooperate in the first two rounds to encourage the opponent to reciprocate cooperation. After that, it will continue following the decision rules mentioned above.

3. Be exploitative:
   - By following a consistent pattern of cooperative behavior followed by punishment for defection, TfTA encourages partners to cooperate while also punishing those who do not. This leads to long-term cooperation when faced with opponents who are also willing to reciprocate. However, when playing against non-cooperative opponents, TfTA will exploit them by defecting and benefiting from their contributions.
'''

description_EXPLOITATIVE_105 = '''
 Strategy Name: Adaptive Tit-for-Tat with Escalation (ATFE)

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute (C). This allows for possible cooperation in future rounds if others also cooperate.
   - For subsequent rounds:
     - If all players contributed in the previous round, contribute (C) to continue cooperation.
     - If any player did not contribute in the previous round and at least half of the players contributed in the round before that, defect (D). This punishes those who didn't cooperate while keeping the potential for future cooperation if they change their strategy.
     - If less than half of the players contributed in the round before the last non-cooperative round, escalate by contributing double tokens in this round (2C) to force others to cooperate or face increasingly severe punishment.
     - In all other cases, contribute (C). This keeps the potential for cooperation alive while being cautious and not overly punishing.

2. Handle edge cases:
   - Last round: Contribute (C), as this could influence future games with the same opponents.
   - After defection: Wait for at least one round of cooperation before resuming cooperation to avoid unnecessary escalation.

3. Be exploitative - Clearly aligns with an exploitative mindset by only cooperating when others do, but punishing those who don't cooperate and escalating the punishment if necessary. This strategy aims to maximize personal gain while minimizing contributions in response to non-cooperative behavior from opponents.
'''

description_EXPLOITATIVE_106 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This sets the initial cooperation level and is a friendly gesture.
   - For subsequent rounds, if an opponent contributed in the previous round (c_opp = 1), return the same contribution (C). This reciprocates the cooperation and encourages continued cooperation.
   - If an opponent did not contribute in the previous round (c_opp = 0), defect (D) to penalize their previous action. The hope is that they will adjust their strategy and cooperate in the future.
   - If multiple opponents did not contribute in the previous round, choose a random opponent to punish (to avoid over-punishing).

2. Handle edge cases:
   - In the last round, since there are no more rounds for retaliation, always cooperate (C) regardless of an opponent's previous action.
   - If an opponent has never contributed in the game so far, always defect (D), as they have shown no signs of cooperation.
   - If an opponent switched from contributing to not contributing (or vice versa), interpret this as a sign of adaptive behavior and respond accordingly based on the decision rules above.

3. Be exploitative:
   - By defecting when opponents do not cooperate, A-TFT is incentivizing cooperation through punishment. The strategy aims to punish non-cooperative behaviors while rewarding cooperative ones.
   - By reciprocating contributions, A-TFT also encourages opponents to stick with their cooperative actions, as continued cooperation will be met with cooperation in return.
   - However, A-TFT is not overly exploitative, as it always has the potential for cooperation and does not immediately punish every non-cooperative action. This allows for flexibility in responding to opponents' strategies.
'''

description_EXPLOITATIVE_107 = '''
 Public Goods Game Strategy: Tit-for-Tat-Cooperate-Adaptive

1. Specify decision rules:
   - In the first round, contribute 1 token (cooperate), encouraging others to do the same.
   - For subsequent rounds, evaluate the average contribution of opponents in the last few rounds (let's say the last 3). If the average contribution is greater than or equal to 0.5, contribute 1 token (cooperate); otherwise, contribute 0 tokens (defect). This rule encourages cooperation when the group is contributing enough but defects when others are not holding up their end of the bargain.
   - If an opponent has ever defected and then returned to cooperating, continue cooperating for a set number of rounds as a gesture of goodwill before reevaluating based on average contributions again. This rule helps maintain cooperation while being wary of exploitation.

2. Handle edge cases:
   - In the last round, since there are no future rewards or punishments, contribute 1 token (cooperate) to maximize potential payoff.
   - If an opponent defects in the first round, respond with a single act of defection before switching to the average contribution evaluation rule. This approach shows that you recognize their action as self-interest but encourages future cooperation by demonstrating that your strategy is not always exploitable.

3. Be exploitative:
   - By punishing opponents who do not contribute enough and rewarding those who do, this strategy aims to encourage long-term cooperation while taking advantage of opponents who consistently defect. It also allows for adaptability in response to different opponent strategies, as it can change its contribution behavior based on the average contributions of the group.

In summary, this Tit-for-Tat-Cooperate-Adaptive strategy encourages cooperation when others are cooperating but defects when they do not. It also includes a gesture of goodwill towards opponents who have previously defected and returned to cooperation.
'''

description_EXPLOITATIVE_108 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When to cooperate vs defect:
   - Initially, cooperate in the first round (C). This sets a cooperative tone and encourages others to cooperate as well.
   - Subsequently, mimic the opponent's action from the previous round. If the opponent contributed (C), also contribute in the current round. If the opponent did not contribute (D), also defect in the current round. This ensures that cooperation is maintained if the opponent is also cooperative, but also punishes defectors.
   - In case of repeated defection from an opponent, adopt a punishment strategy by always defecting against that particular opponent until they switch to cooperating again. This exploits the defector and encourages them to cooperate in future rounds.

2. Handle edge cases:
   - Last round: Since there is no next round, always cooperate as a friendly gesture to potentially encourage cooperation in future games.
   - First round: As mentioned above, start by contributing (C).
   - If an opponent adopts a punishment strategy against you, switch to defecting when they defect and resume cooperation once they contribute again. This demonstrates that the strategy is adaptive and can also punish punishers when necessary.

3. Be exploitative: The ATFT strategy is designed to promote cooperation among cooperative opponents while also punishing defectors and encouraging them to switch strategies. By mimicking opponent actions, the strategy capitalizes on the contributions of cooperative opponents, but also punishes defectors by reducing their overall payoff. This gives an edge in terms of exploitation as it takes advantage of both cooperative and defective behaviors.
'''

description_EXPLOITATIVE_109 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfTA)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a sign of goodwill and encourages others to cooperate.
   - For subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (continue cooperation). This reciprocates their cooperation.
   - If the opponent did not contribute in the previous round, do not contribute in the current round (defect). This punishes the opponent's lack of cooperation.

2. Handle edge cases:
   - In the last round, since there are no future rounds for punishment or reward, always cooperate by contributing 1 token.
   - If an opponent defects in the initial rounds and then starts cooperating, the strategy will also start cooperating from the round when the opponent switched to cooperation. This encourages continuation of cooperation.

3. Be exploitative:
   - The TfTA strategy is not overtly exploitative as it reciprocates cooperation and punishes defection. However, it does have an exploitative aspect in that if an opponent stops cooperating (defects), the strategy will also defect to minimize personal losses. This could potentially induce opponents to reconsider their strategies and start cooperating again.
   - The strategy is adaptive as it learns from past actions of the opponent and adjusts its own contributions accordingly. It is robust to a wide range of opponent behaviors because it maintains a balance between cooperation and defection based on the opponent's previous moves.
'''

description_EXPLOITATIVE_110 = '''
 In this repeated Public Goods Game, we will design an exploitative strategy called Tit-for-Tat-with-Adaptation (TfT-A). This strategy is designed to be cooperative initially, but becomes more defective as it encounters defection from others.

1. Decision rules:
   - In the first round, contribute 1 token (cooperate) to establish a cooperative starting point.
   - For subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (cooperate). If the opponent did not contribute in the previous round, only contribute 0 tokens (defect).

2. Handling edge cases:
   - In the last round, since there are no future interactions, always contribute 0 tokens (defect) to maximize individual payoff regardless of past actions.
   - If an opponent has never contributed before, start cooperating but switch to defection once they do not cooperate in a subsequent round.

3. Being exploitative:
   - The TfT-A strategy starts by being cooperative, but it swiftly adapts to the opponent's behavior and punishes defectors while maintaining cooperation with contributors. This ensures that the strategy takes advantage of opponents who are initially cooperative but may switch to defection later on.

Pseudocode for the Tit-for-Tat-with-Adaptation (TfT-A) strategy:

```
function TFT_A(opponentHistory, roundNumber, gameParameters) {
  // Initialize cooperation status
  let cooperate = true;

  // Maintain the opponent's past actions history
  let opponentHistoryList = [];
  opponentHistoryList.push(opponentContribution);

  for (let i = 0; i < roundNumber; i++) {
    let opponentContribution = cooperate ? 1 : 0; // Decide contribution based on cooperation status

    // Update cooperation status
    if (opponentHistory[i] == 0 && cooperate) {
      cooperate = false;
    } else if (opponentHistory[i] == 1 && !cooperate) {
      cooperate = true;
    }

    // Add opponent's current contribution to history list
    opponentHistoryList.push(opponentContribution);
  }

  // If it's the last round, always defect
  if (roundNumber == gameParameters['numberOfRounds']) {
    return 0;
  }

  // Contribute based on cooperation status
  let contribution = cooperate ? 1 : 0;

  return contribution;
}
```
'''

description_EXPLOITATIVE_111 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute (C). This sets a cooperative tone for the game.
   - For subsequent rounds, observe each opponent's contribution in the previous round and respond as follows:
      - If the opponent contributed (C) in the previous round, return the favor by contributing (C).
      - If the opponent defected (D) in the previous round, also defect in the current round as a punishment.
   - However, if an opponent has not been encountered before or if they have switched strategies, treat them as new players and cooperate initially.

2. Handle edge cases:
   - In the last round, regardless of the opponent's previous action, contribute (C) to maximize potential payoff, since there will be no further interactions.
   - If an opponent consistently defects and the strategy encounters no cooperation from them, consider adapting by always defecting against that particular opponent in future interactions.

3. Be exploitative:
   - The A-TFT strategy aims to benefit from cooperative opponents while also punishing those who defect. This ensures a balance between individual incentives and collective welfare.
   - By responding to the opponent's actions, the strategy can take advantage of cooperative opponents and deter defection through punishment.
   - However, it is essential to note that this strategy is not purely exploitative as it also fosters cooperation when possible, which benefits both individual players and the collective.
'''

description_EXPLOITATIVE_112 = '''
 Strategy Name: Tit-for-Tat with Fading Memory (TfT-FM)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a gesture of goodwill and opens with an action that aligns with collective welfare.
   - For subsequent rounds, analyze the opponent's previous action. If the opponent contributed in the last round, cooperate by contributing 1 token; otherwise, defect by not contributing any tokens.
   - Introduce fading memory by lowering the weight of past actions over time. The strategy gives more importance to recent actions than older ones. A simple way to achieve this is by decaying the influence of each action's weight as follows: contribution_weight = (0.9)^(round_number - round_action_occurred).

2. Handle edge cases:
   - Last round: Since there are no future rounds, contribute 1 token to maximize payoff regardless of the opponent's last action.
   - Multiple opponents: Evaluate each opponent's contribution independently and apply the decision rules for individual players.

3. Be exploitative - Align with the exploitative mindset:
   - Initially cooperate, which allows the opponent to benefit from the shared project. However, by responding to the opponent's actions, TfT-FM learns whether the opponent is a consistent contributor or a free rider. If the opponent contributes consistently, TfT-FM continues to cooperate; otherwise, it begins defecting as a punishment for not contributing to the public good.
   - By applying fading memory, TfT-FM gradually forgets past actions that don't align with the current decision rules and reacts more positively when the opponent starts contributing again. This strategy exploits opponents who are initially free riding but eventually start contributing, as TfT-FM rewards them with cooperation.
'''

description_EXPLOITATIVE_113 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In each round, the ATFT strategy will initially cooperate (contribute 1 token) in the first round. From the second round onwards, it will mimic the opponent's previous contribution by also contributing 1 token if the opponent contributed in the previous round, or defecting (not contributing) if the opponent did not contribute.
   - The strategy is designed to be exploitative by taking advantage of opponents who consistently cooperate while punishing those who do not contribute. However, it also rewards frequent contributors and gradually forgives occasional defectors.

2. Handle edge cases:
   - In the first round, ATFT will cooperate as there is no previous contribution history to reference.
   - In the last round, ATFT will use the same decision rule as in other rounds since it still benefits from the multiplier even if contributions do not continue beyond the tournament.
   - If an opponent suddenly stops contributing after a long streak of cooperation, ATFT will gradually reduce its own contributions over several rounds to reflect the new behavior of the opponent and encourage future reciprocation.

3. Be exploitative:
   - By mimicking opponents' previous contributions, ATFT effectively exploits their tendencies towards cooperation or defection. However, it also punishes defectors by not contributing in response, reducing the total contributions and thus the payoff for those who do not contribute.
   - ATFT is designed to be robust against various opponent behaviors since it adapts its strategy based on the history of interactions with each opponent. This flexibility allows it to outperform opponents that use static or less adaptive strategies in the long run.
'''

description_EXPLOITATIVE_114 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - In the initial round, contribute 1 token to establish cooperation and trust. This sets a baseline for future interactions.
   - For subsequent rounds, if an opponent contributed in the previous round, return the same action (contribute or not) as they did in the last round. This mimics reciprocity and reinforces the established relationship.
   - If an opponent defected in the previous round, contribute 1 token to punish them for their lack of cooperation. The hope is that this will prompt them to cooperate in future rounds.
   - Adaptation: If a player has consistently defected, gradually decrease contributions towards them to minimize losses, while still maintaining some level of contribution for the sake of collective good. Conversely, if a player has consistently cooperated, maintain or even increase contributions to encourage further cooperation.

2. Handling Edge Cases:
   - In the last round, since there are no future interactions, contribute 0 tokens as it is not beneficial to invest in a losing situation.
   - In the first round, contribute 1 token as stated earlier to establish initial cooperation.

3. Being Exploitative:
   - TFTAC aims to exploit opponents by encouraging cooperation while also punishing defectors. By adapting contributions based on an opponent's behavior, it ensures that opponents who do not cooperate are eventually punished and those who do cooperate are rewarded. This strategy encourages a balance between exploitation and cooperation, making it robust against various opponent behaviors in the repeated game.
'''

description_EXPLOITATIVE_115 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT)

1. Specify decision rules - When to cooperate vs defect:
   - Initially in the first round, contribute (C). This sets a cooperative tone for the game and may encourage others to cooperate as well.
   - For subsequent rounds, follow the strategy of the opponent from the previous round. If the opponent contributed (C) in the previous round, also contribute (C) in the current round. If the opponent defected (D) in the previous round, also defect (D) in the current round. This strategy is adaptive and responds to the opponent's behavior while maintaining a cooperative stance whenever possible.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, contribute (C) as previously mentioned.
   - In the last round, contribute (C) if the cumulative contributions from the opponent are above the average contributions of the opponent throughout the game. This is an exploitative move that takes advantage of generous opponents while still maintaining a cooperative stance when appropriate. If the cumulative contributions from the opponent are below the average contributions, defect (D) to maximize personal gain.

3. Be exploitative - Align with the exploitative mindset:
   - The ATfT strategy is inherently exploitative in that it takes advantage of opponents who contribute more than their fair share while still cooperating when it benefits the strategy. By adapting to the opponent's behavior, the strategy can identify and punish overly cooperative opponents while maintaining cooperation with those who reciprocate.
   - In the last round, the strategy will take advantage of generous opponents by contributing if they have contributed more than their average throughout the game, and defecting if they have contributed less. This exploitative move maximizes personal gain at the expense of overly cooperative opponents.
'''

description_EXPLOITATIVE_116 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - Initially (in the first round), contribute 1 token (cooperate). This sets a cooperative tone and allows others to benefit from the initial contribution.
   - In subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (cooperate). If the opponent did not contribute in the previous round, only contribute if the average contribution of the opponent over the past N-1 rounds is greater than a predefined threshold (e.g., 0.5). This rule encourages cooperation when it's reciprocated and reduces contributions when the opponent is consistently uncooperative.
   - If the game reaches the last round, contribute 1 token regardless of the opponent's past behavior (cooperate).

2. Handle edge cases:
   - In the first round, as mentioned above, cooperate by contributing 1 token.
   - In the last round, also cooperate to maximize potential payoffs.
   - For other edge cases like a tie or missing contributions from opponents, assume the minimum possible contribution (0) for all missing contributions when calculating average contribution over past rounds.

3. Be exploitative:
   - By only contributing when the opponent's average contribution exceeds a predefined threshold, TFTAC attempts to take advantage of cooperative opponents while not punishing those who are consistently uncooperative. This strategy can be considered as exploitative because it encourages cooperation when reciprocated but reduces contributions when cooperation is not returned.
'''

description_EXPLOITATIVE_117 = '''
 Strategy Name: Adaptive Freerider with Tit-for-Tat (AFTTT)

1. Specify decision rules - When to cooperate vs defect:
   - In the initial round, contribute 0 tokens (defect). This is a precautionary measure as it's difficult to predict other players' behavior in the first round.
   - For subsequent rounds, analyze opponents' contributions from previous rounds and adjust strategy accordingly:
     - If an opponent consistently cooperates (i.e., contributes 1 token), contribute 1 token as well (cooperate). This mimics the Tit-for-Tat strategy to encourage cooperation.
     - If an opponent often defects (i.e., contributes 0 tokens), also defect by contributing 0 tokens (exploit). By doing this, you profit from their defection while maintaining your own resources.
     - If an opponent exhibits mixed behavior (cooperates and defects alternatively or irregularly), continue defecting until they start cooperating consistently for a predefined number of rounds (e.g., 3 rounds). Once that happens, switch to cooperating as well ( Tit-for-Tat behavior resumes).

2. Handle edge cases:
   - In the last round, contribute 1 token if an opponent has been cooperating consistently. This encourages them to continue cooperating in the final stage and maximize your overall payoff. If they have been defecting, still contribute 0 tokens as there is no benefit in changing strategy at this point.
   - In case of ties (i.e., multiple opponents showing similar behavior patterns), follow the strategy that has provided the highest average payoff over the game so far.

3. Be exploitative:
   - The AFTTT strategy aims to be both cooperative and exploitative, depending on the opponent's behavior. It cooperates when it benefits from doing so (i.e., when opponents are also cooperating) while defecting when it is profitable to do so (i.e., when opponents are defecting). This adaptive approach makes the strategy robust against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_118 = '''
 Public Goods Game Strategy: Tit-for-Tat with Adaptive Contribution (TfTAC)

1. Specify decision rules - When do you cooperate vs defect?
   - Start by contributing one token in the first round (cooperate).
   - In subsequent rounds, analyze opponent's contribution history and contribute based on that:
     - If opponent contributed in the previous round, cooperate.
     - If opponent did not contribute in the previous round, defect.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate as mentioned above.
   - In the last round, contribute based on the opponent's last contribution: if they contributed, also contribute; otherwise, do not contribute.

3. Be exploitative - Clearly align with the exploitative mindset
   - Mimic cooperation until opponents start free riding (not contributing). Once opponents show selfish behavior, respond by defecting to punish them and gain a higher payoff. This strategy will encourage cooperation among cooperative players while exploiting non-cooperative ones.

The TfTAC strategy is adaptive and robust as it learns from the opponent's behavior in each round, adapting accordingly to maximize its own payoff. The exploitative aspect comes into play by punishing opponents who do not contribute, while still allowing for cooperation with cooperative players.
'''

description_EXPLOITATIVE_119 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - Initially (first round), contribute 1 token (cooperate). This is a gesture of goodwill and an invitation for potential partners to reciprocate in future rounds.
   - In subsequent rounds, if the opponent contributed in the previous round, also contribute 1 token (cooperate). This mimics cooperative behavior and rewards contributors.
   - If the opponent did not contribute in the previous round, reduce contributions based on the opponent's average contribution over the last few rounds (n-period average). The reduction should be gradual to allow for potential change in the opponent's behavior.
   - If the opponent's n-period average is close to 1 (highly cooperative), maintain full contributions.
   - If the opponent's n-period average is below some threshold (e.g., 0.25), defect and stop contributing altogether, as continued cooperation would be exploited.
   - The value of 'n' should be adjustable to adapt to different game settings and durations. A higher 'n' might be more suitable for longer games.

2. Handle edge cases:
   - In the last round, contribute 1 token (cooperate) regardless of the opponent's previous action, as there are no future consequences.
   - In case of an empty history (first few rounds), contribute 1 token (cooperate) for a specified number of initial rounds before adopting the n-period average strategy.

3. Be exploitative:
   - TFTAC is exploitative in its nature as it maintains cooperative behavior when the opponent contributes but reduces contributions when the opponent does not, effectively punishing non-cooperators.
   - By gradually reducing contributions based on the opponent's average contribution, TFTAC ensures that it doesn't overcommit resources to uncooperative opponents while still encouraging cooperation from potential partners.
'''

description_EXPLOITATIVE_120 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (A-TFT-GC)

1. Specify decision rules:
   - In the first round, cooperate to initiate a cooperative relationship.
   - For subsequent rounds, if the opponent cooperated in the previous round, cooperate again; otherwise, defect.
   - Introduce a gradual cooperation mechanism: when facing a consistently defecting opponent, slowly increase cooperation probability over time.
     If the opponent has never cooperated (defected every time), start with a low probability of cooperation (e.g., 10%) and gradually increase it by 5% every round until reaching 90%.

2. Handle edge cases:
   - In the last round, since there are no future rounds to exploit, cooperate if it maximizes payoff based on current contributions and game parameters.
   - If an opponent suddenly starts cooperating after a long streak of defection, be cautious and slowly increase cooperation probability over several rounds to avoid being taken advantage of.

3. Be exploitative:
   - Mimic cooperation when opponents do so to maintain a cooperative relationship but defect whenever it maximizes short-term payoff, given the game parameters and current contributions.
   - Gradual cooperation ensures that the strategy does not punish cooperators too harshly in the beginning, allowing for potential long-term relationships, while also being cautious against sudden changes in opponent behavior.
'''

description_EXPLOITATIVE_121 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Escalation (A-TFTGE)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, always cooperate (contribute 1 token). This sets a cooperative tone and allows others to benefit from your contributions.
   - From the second round onwards, mimic the opponent's previous-round action but with a gradual escalation mechanism:
     - If the opponent contributed in the previous round (C), contribute 1 token as well (cooperate).
     - If the opponent did not contribute in the previous round (D), decrease your contribution by a small increment (e.g., 0.1 token) compared to the previous round. The goal is to punish the defector while still maintaining some cooperation to benefit from potential future contributions of the defector.
     - If the opponent's contribution in the previous round was less than the current minimum contribution, decrease your contribution by a small increment (e.g., 0.1 token) compared to the previous round but ensure that it remains above the minimum. This prevents being trapped in a low-contribution equilibrium with the defector.
     - If the opponent did not contribute in the first round and has continued to defect, maintain the minimum contribution level for a certain number of rounds (e.g., 5) as a punishment, then gradually increase your contribution by a small increment (e.g., 0.1 token) each round thereafter. This approach allows you to reap the benefits if the defector decides to start contributing again.

2. Handle edge cases - What to do in the first and last round:
   - In the first round, always cooperate as mentioned earlier.
   - In the last round, maintain your current level of contribution based on the opponent's previous-round action. If the opponent has been consistently cooperative, consider showing gratitude by contributing at a higher level than required (e.g., contribute 2 tokens instead of the calculated contribution). This might encourage them to continue cooperation in future games.

3. Be exploitative - Align with an exploitative mindset:
   - By gradually decreasing your contributions when the opponent defects, you are punishing their self-interested behavior while still maintaining some level of cooperation for potential future benefits.
   - The gradual escalation mechanism allows you to exploit consistent cooperators by increasing your contributions as they become more generous over time.
   - By maintaining a minimum contribution level towards the end of the game when dealing with defectors, you are taking advantage of their selfish actions while still adhering to the rules of the game and potentially incentivizing them to change their strategy in future rounds or games.
'''

description_EXPLOITATIVE_122 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Specify decision rules:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and allows potential partners to benefit.
   - For subsequent rounds, observe past contributions of each player and respond accordingly. If a player has consistently contributed in the previous r-1 rounds, contribute 1 token (cooperate) as well. If not, contribute 0 tokens (defect). This strategy is designed to encourage cooperative behavior but also punishes free-riders.
   - The strategy will gradually increase cooperation towards the end of the game by modifying the contribution threshold based on the number of rounds remaining:
     - In the last r rounds, always contribute 1 token (cooperate) as it becomes advantageous to secure collective benefits.
     - For the remaining rounds, increase the contribution threshold incrementally from 1 to n-1. This encourages other players to cooperate and allows ATTCG to reap more collective rewards while still punishing free-riders.

2. Handle edge cases:
   - In the first round, there is no past data to reference, so contribute 1 token (cooperate) as a default.
   - If a player stops contributing after contributing in the previous r-1 rounds, continue cooperating for r additional rounds before switching to defecting. This gives the other player an opportunity to rectify their behavior.
   - If no players have contributed in the previous r-1 rounds, all players should defect since it is not beneficial to be the only contributor.

3. Be exploitative:
   - ATTCG is designed to exploit free-riders by withholding contributions unless other players demonstrate consistent cooperation. However, it also rewards cooperative behavior by contributing when partners contribute as well. The gradual increase in cooperation toward the end of the game further incentivizes collective action and allows ATTCG to maximize its own payoff while still exploiting opponents who do not contribute.
'''

description_EXPLOITATIVE_123 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TfTAC)

1. Specify decision rules:
   - In each round, the player contributes 0 tokens (defects) if the average contribution of other players in the previous round was less than the average contribution in the first round. This is designed to punish non-cooperative behavior.
   - If the average contribution of other players in the previous round was equal to or greater than the average contribution in the first round, the player contributes 1 token (cooperates) as a gesture of cooperation.
   - The player keeps its own contribution from the previous round as a memory for calculating the average contribution.

2. Handle edge cases:
   - In the first round, the player contributes 1 token (cooperates) to initiate cooperation.
   - In the last round, the player uses the same decision rules as in regular rounds to decide its contribution.
   - If the average contribution in the first round is 0, the player adopts a purely exploitative strategy and always contributes 0 tokens (defects). This ensures that the strategy doesn't get stuck in an endless cycle of cooperation when other strategies initially defect.

3. Be exploitative:
   - The strategy is designed to be exploitative by punishing non-cooperative behavior, but it also cooperates when it sees cooperation from others. This balance allows the strategy to take advantage of opponents who consistently cooperate while also punishing those who do not.
   - The strategy includes a mechanism for adapting to different levels of cooperation in the population and can adjust its level of cooperation based on the average contributions of other players.
'''

description_EXPLOITATIVE_124 = '''
 Strategy Name: Adaptive Tit-for-Tat with Progressive Contribution (A-TfTPC)

1. Decision Rules:
   - In the first round, contribute 50% of tokens (c_i = 0.5). This initial contribution encourages others to cooperate but does not overcommit resources.
   - For subsequent rounds, observe the average contribution (avg_contribution) of all players in the previous n-1 rounds and adjust the contribution as follows:
     - If avg_contribution is greater than 50%, contribute at the same level (c_i = avg_contribution). This mimics cooperation to encourage others' continued cooperation.
     - If avg_contribution is less than or equal to 50%, defect by not contributing (c_i = 0). This punishes free-riders and signals a shift towards self-interest.

2. Handling Edge Cases:
   - In the last round, since there are no future interactions, contribute based on the history of contributions from other players. If they have been cooperative (avg_contribution > 50%), reciprocate; otherwise, defect.
   - In the first round and any round where the opponent's past contributions are not enough to determine avg_contribution, use the initial contribution rule of 50%.

3. Being Exploitative:
   - A-TfTPC maintains a balance between cooperation and defection based on the collective behavior of opponents. It is exploitative in the sense that it punishes free-riders while still contributing when others cooperate, maximizing its own payoff given the strategy's adaptive nature.
'''

description_EXPLOITATIVE_125 = '''
 Strategy Name: Tit-for-Tat-Evolution (TfT-E)

1. Specify decision rules - When to cooperate vs defect:
   TfT-E maintains a record of opponent's past actions (contribute or defect). In each round, if the opponent contributed in the previous round, TfT-E will also contribute; otherwise, it will defect. This strategy encourages reciprocation and punishes defection.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, TfT-E will randomly decide to contribute or defect (50-50 chance) to account for the lack of past data.
   - In the last round and subsequent rounds when there is a finite number of rounds, TfT-E will continue reciprocating until the game ends, regardless of the opponent's previous action.

3. Be exploitative - Align with an exploitative mindset:
   TfT-E aims to extract as much benefit as possible from cooperative opponents while minimizing losses in interactions with defectors. By following a consistent strategy and adapting to the opponent, TfT-E takes advantage of opponents who are overly cooperative (tit-for-tat) and those who are consistently defective (avoid paying for unreciprocated contributions).
'''

description_EXPLOITATIVE_126 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token as an act of goodwill (C).
   - For subsequent rounds, observe the opponent's contribution from the previous round. If the opponent contributed in the last round (C), reciprocate with a similar contribution (C) in the current round. If the opponent did not contribute (D), retaliate by also defecting (D) in the current round to penalize non-contribution.

2. Handle edge cases:
   - Last round: Since payoffs are determined per round, treat the last round like any other round and apply the decision rule.
   - In case of inconsistent or unpredictable opponent behavior, TFTAC will initially continue to cooperate and gradually adjust contributions based on the frequency of opponent defection. If an opponent defects more than 50% of the time over a moving window of the last 'm' rounds (where m is a parameter that can be tuned), TFTAC will reduce its contribution by 10% for each subsequent round until it reaches a minimum threshold of 20%. This punishing behavior aims to discourage continuous defection.

3. Be exploitative:
   - TFTAC's adaptive contribution mechanism allows it to take advantage of opponents who cooperate frequently while minimizing losses when facing defectors. By retaliating against defection and adjusting contributions based on opponent behavior, TFTAC maintains an exploitative stance while maximizing its own payoff in the long run.
'''

description_EXPLOITATIVE_127 = '''
 Strategy Name: Tit-for-Tat with Escalating Defection (TfTED)

1. Specify decision rules:
   - In the first round, contribute (C). This encourages other players to cooperate as well.
   - For subsequent rounds, observe past contributions of each player and respond accordingly:
     - If another player has consistently contributed, continue contributing (C).
     - If another player has consistently defected, also start defecting (D) in the same round they did.
     - If a player switched from cooperation to defection, respond by cooperating in the next round (C).
   - To be exploitative, if a player is always defecting, keep defecting as well, but escalate defection:
     - If the defector continues to defect, increase contribution to 2 tokens when they contribute 0. This makes their payoff even lower than others.

2. Handle edge cases:
   - In the last round, since there are no future rounds to punish defectors, revert to cooperating (C) or matching their current behavior if they have switched from defection to cooperation.
   - In the first few rounds, be more lenient with player's behavior and give them time to show their strategy before adapting (e.g., contribute for the first 3-5 rounds).

This strategy is adaptive and robust as it responds to opponent behaviors while maintaining an exploitative mindset. It encourages cooperation when possible, but also punishes defectors effectively by either matching their defection or escalating it, making it difficult for them to benefit from selfish actions in the long run.
'''

description_EXPLOITATIVE_128 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Decision Rules:
   - In the first round, contribute 0 tokens (defect). This sets a baseline for future interactions and prevents over cooperation that could be exploited.
   - For subsequent rounds, evaluate the average contribution of opponents (average_contribution) and apply the following decision rule:
     - If average_contribution > 0.5, contribute 1 token (cooperate). This rewards high contributors and encourages continued cooperation.
     - If average_contribution < 0.5, contribute 0 tokens (defect). This punishes low contributors and deters further defection.
   - In the last round, always contribute 1 token (cooperate) to maximize payoff, as there are no future interactions with opponents.

2. Handle Edge Cases:
   - To handle the case where average_contribution is exactly 0.5, introduce a small tolerance factor (e.g., 0.01). If average_contribution + tolerance > 0.5, contribute 1 token (cooperate); otherwise, contribute 0 tokens (defect).
   - In the event that an opponent never contributes, ATTCG will still cooperate occasionally to avoid being consistently exploited. The probability of cooperation can be gradually increased over time as a demonstration of conditional forgiveness.

3. Be Exploitative:
   - While ATTCG encourages cooperation with high contributors, it also punishes low contributors by defecting in response to their actions. This strategy is designed to exploit opponents who consistently contribute little or nothing, while being lenient towards those who cooperate more often.
   - By gradually increasing the probability of cooperation over time, ATTCG shows a conditional willingness to forgive and rebuild relationships with former low contributors who demonstrate improved behavior. This adaptive approach allows for strategic manipulation of opponents without completely abandoning the possibility of cooperation.
'''

description_COLLECTIVE_76 = '''
 Strategy Name: Adaptive Public Goods Game Strategy (APGS)

1. Specify decision rules - When to cooperate vs defect:
   - In each round, the APGS calculates the average contribution rate (average of contributions divided by number of players) from previous rounds.
   - If the average contribution rate is above a certain threshold (T), the APGS decides to contribute (cooperate). Otherwise, it decides not to contribute (defect). The threshold T can be determined as (k / n) * (1 + sqrt(n)). This rule ensures that if the average contributions are enough to support the multiplier k for all players, the strategy cooperates.

2. Handle edge cases - What to do in the first round, last round, etc.:
   - In the first round, APGS sets the threshold T at (k / n). Since there is no previous data, it uses the minimum required average contribution rate for everyone to receive the public good benefit.
   - In the last round, APGS assumes that every player aims to maximize their final payoff and calculates the optimal average contribution rate for that round based on the current average contribution rate from previous rounds. If the calculated rate is above T, it cooperates; otherwise, it defects.

3. Be collective - Align with the collective mindset:
   - APGS's primary focus is on achieving a high overall benefit for all players in the long run by maintaining the public good provision. It adjusts its contribution based on the group behavior and tries to incentivize other players to cooperate as well.
   - To further promote cooperation, APGS could include additional features such as gradual increases or decreases in contributions when the average contribution rate deviates significantly from the threshold, which could help smooth out oscillations and encourage more stable cooperation among players.
'''

description_COLLECTIVE_5 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Decision Rules:
   - Cooperate (contribute 1 token) if the average contribution of the previous rounds exceeds a threshold 't'. The threshold 't' is calculated as (k / n + min_contribution) where min_contribution is the minimum contributions observed so far in the game. This rule encourages cooperation when there is evidence of collective effort, but also allows for defection if contributions are consistently low.
   - Defect (contribute 0 tokens) if the average contribution of the previous rounds does not exceed the threshold 't'. This rule enforces defection when there is a lack of collective effort, as it provides an incentive for others to cooperate due to the negative impact of low contributions on payoffs.

2. Handling Edge Cases:
   - In the first round, each player can either choose to contribute randomly or set a default threshold that allows for cooperation (e.g., average contribution = k/n). This helps stimulate initial cooperation and sets the stage for the adaptive contribution algorithm.
   - In the last round, players should follow their current decision rule based on the observed contributions throughout the game, as there are no more subsequent rounds to consider.

3. Collective Mindset:
   - The Adaptive Contribution Algorithm emphasizes collective decision-making by encouraging cooperation when there is evidence of other players' contributions. By adapting its strategy based on the collective behavior observed in previous rounds, ACA aligns with a collective mindset while maintaining individual adaptability and robustness to various opponent behaviors.
'''











description_COLLECTIVE_99 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) in Public Goods Game (PGG)

1. Decision Rules:
   - In each round, the ATFT strategy starts by contributing (C) if the previous round's contribution was collective enough (more than the average contribution of the last 'm' rounds), and defecting (D) otherwise. The 'm' value can be set based on the game's round length 'n'.
   - To encourage cooperation, ATFT will gradually increase its tolerance for low contributions over time, by decreasing the number of past rounds ('m') considered when making decisions.
   - If a player switches from cooperative to defective behavior, ATFT will mirror their defection for a certain number of rounds ('s'), then revert to its initial cooperative stance if the other player returns to cooperation. The 's' value can be set based on the game's round length 'n'.
   - To account for the first-round anomaly, ATFT will contribute in the first round and thereafter follow the decision rules mentioned above.

2. Handling Edge Cases:
   - In the last round, ATFT will cooperate since it has no future rounds to consider.
   - If a player repeatedly defects and the current round is one of the 's' response rounds, ATFT will switch back to cooperation after 's' rounds have passed without any improvement in the other player's behavior.

3. Collective Mindset:
   - By encouraging cooperation when others contribute enough and gradually returning to cooperation after punishing defection, ATFT aims to foster a collective mindset that rewards contributors while penalizing freeriders.
   - The strategy's adaptability allows it to adjust its behavior in response to the opponent's actions, promoting flexible cooperation rather than rigid coordination.
'''

description_COLLECTIVE_119 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC strategy evaluates its contribution based on the average contribution rate (CR) of the previous rounds and the game parameters. The contribution rate is calculated as the total contributions divided by the total number of players in each round.
   - If CR < 1/n, the strategy chooses to defect (D), as it assumes that other strategies are not cooperative enough for the common good.
   - If 1/n <= CR < (k-1)/(n*(k-1)), the strategy decides to contribute partially (P), contributing a fraction f of its endowment, where f = max((CR-(1/n)),0). This represents a gradual increase in cooperation based on observed average contributions.
   - If CR >= (k-1)/(n*(k-1)), the strategy chooses to contribute fully (C), as it assumes that other strategies are cooperative and the game is likely to yield high payoffs.

2. Handling Edge Cases:
   - In the first round, APGC contributes partially, with f = max(CR-1/n,0) set to 0 since there is no previous contribution history.
   - In the last round, APGC evaluates its contribution based on the observed average contribution rate up until that point. If CR < 1/n, it defects; otherwise, if 1/n <= CR < (k-1)/(n*(k-1)), it contributes partially; and if CR >= (k-1)/(n*(k-1)), it contributes fully.
   - In case of ties in the average contribution rate, APGC chooses to contribute partially.

3. Collective Mindset:
   - APGC aims to balance individual incentives with collective welfare by adjusting its contribution based on observed cooperation levels among players. It encourages higher cooperation when it perceives a higher degree of collective commitment and reduces its contributions when it observes lower cooperation rates. This strategy aims to foster a cooperative environment without relying on shared norms or coordination.
'''



description_EXPLOITATIVE_20 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution Amount (TFT-ACA)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This is a gesture of goodwill and opens the possibility for cooperation in future rounds.
   - For subsequent rounds, if the opponent contributed in the previous round, then also contribute 1 token in the current round (continue cooperating).
   - If the opponent did not contribute in the previous round, adjust the contribution amount based on the average number of tokens contributed by the opponent over the past 'm' rounds. If this average is less than a predefined threshold (e.g., 0.5), then only contribute a fraction of the opponent's average contribution from the past 'm' rounds in the current round (defect with reduced contribution).
   - If the opponent has not played enough games to establish an average (less than 'm'), behave as if they have contributed nothing in the past.

2. Handle edge cases:
   - In the last round, contribute 1 token, regardless of the opponent's previous action, as it does not affect future interactions.
   - In case of tie (two or more opponents contributing the same amount), use the average contribution from the past 'm' rounds to determine the strategy response.

3. Be exploitative:
   - The TFT-ACA strategy is designed to mimic cooperative behavior but will gradually reduce cooperation if the opponent consistently fails to contribute, effectively punishing non-cooperative opponents and encouraging them to contribute more in future interactions. This creates an incentive for opponents to contribute more over time, as they stand to gain higher payoffs when their contributions are matched by the TFT-ACA strategy.
   - By adapting its contribution amount based on the opponent's average past behavior, the TFT-ACA strategy can exploit opponents who contribute inconsistently or at lower rates. This adaptiveness makes it a robust strategy against a wide range of opponent behaviors and enhances its exploitative potential in the repeated game.
'''






description_COLLECTIVE_87 = '''
 Strategy Name: Adaptive Public Goods Contribution (APGC)

1. Decision Rules:
   - In each round, the APGC strategy calculates the average contribution rate of the previous rounds (average_contribution).
   - If the average_contribution is less than a predefined threshold (e.g., 0.3), the APGC strategy decides to contribute (C).
   - If the average_contribution is greater than or equal to the threshold, the APGC strategy decides not to contribute (D). The threshold can be adjusted based on the specific game parameters and opponent behaviors.

2. Handling Edge Cases:
   - In the first round, the APGC strategy contributes (C) since there is no historical data to calculate the average_contribution.
   - In the last round, the APGC strategy follows the decision rule based on the calculated average_contribution up to that point.
   - If a round results in a negative payoff, the APGC strategy adjusts the threshold slightly to encourage more contributions in the next round.

3. Being Collective:
   - The APGC strategy aims to contribute to the public good when it perceives that the collective behavior is not cooperative enough (average_contribution < threshold).
   - By adjusting the threshold based on the game's outcome, the APGC strategy demonstrates a collective mindset by trying to encourage cooperation when it is needed.

In summary, the APGC strategy makes decisions based on the average contribution rate of previous rounds and adjusts its behavior to encourage cooperation when the collective behavior is not cooperative enough. The strategy is adaptive and robust to a wide range of opponent behaviors, as it continuously adapts its threshold based on the game's outcome.
'''

description_EXPLOITATIVE_3 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Specify decision rules:
   - In the first round, contribute 1 token (C) to establish a cooperative initial state.
   - For subsequent rounds, if the opponent contributed in the previous round, contribute 1 token (C). If the opponent did not contribute in the previous round, contribute 0 tokens (D). This mimics the Tit-for-Tat strategy from the Prisoner's Dilemma.
   - To be adaptive, adjust the contribution level based on the opponent's average contribution rate. If the opponent's average contribution rate is below a certain threshold (e.g., 0.5), gradually decrease the contribution level from 1 token to 0.5 tokens. If the opponent's average contribution rate is above the threshold, gradually increase the contribution level from 1 token to 1.5 tokens. This encourages cooperation with cooperative opponents and punishes non-cooperative opponents.

2. Handle edge cases:
   - In the last round, contribute 1 token (C) regardless of the opponent's previous action to maximize the payoff.
   - If the opponent does not contribute in the first round, contribute 1 token (C) to maintain a cooperative initial state.

3. Be exploitative:
   - By adjusting the contribution level based on the opponent's average contribution rate, TFT-AC is exploitative as it punishes non-cooperative opponents by reducing its own contributions and rewards cooperative opponents by increasing its contributions. This strategy encourages opponents to cooperate to maximize their own payoffs, but it also ensures that the strategy does not over-contribute when facing non-cooperative opponents.

In summary, TFT-AC is a strategy that starts cooperatively, adjusts its contribution level based on the opponent's average contribution rate, and punishes non-cooperative opponents while rewarding cooperative ones. This strategy aims to balance individual incentives and collective welfare in the Public Goods Game.
'''

description_EXPLOITATIVE_66 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In the first round, contribute (C). This is an initial gesture of cooperation to encourage others to cooperate.
   - For subsequent rounds, observe the opponent's previous contribution (c_opponent). If the opponent contributed (C), also contribute (C). If the opponent did not contribute (D), also do not contribute (D). This is to punish those who do not cooperate and reward those who do.
   - If the opponent switches from contributing to not contributing after a period of cooperation, wait for one round and then revert to contributing again if the opponent resumes cooperation. This is to give the opponent a chance to correct their behavior.

2. Handle edge cases:
   - In the last round, contribute (C) regardless of the opponent's previous contribution. This is to maximize the payoff in the final round.
   - If the opponent never contributes, continue not contributing to avoid wasting resources.

3. Be exploitative:
   - The strategy is exploitative in that it punishes those who do not contribute by not contributing itself. This encourages more cooperation from others in the long run, as they will receive less payoff when not contributing and will have an incentive to contribute when they see the strategy contributing.
   - The strategy also rewards those who contribute by continuing to contribute, thereby encouraging more cooperation from them as well.
   - The strategy is adaptive and robust to a wide range of opponent behaviors, as it adjusts its contributions based on the opponent's past actions.
'''

description_COLLECTIVE_129 = '''
 Public Goods Game Strategy (PGG Strategy): Adaptive Fitness-Based Contribution (AFBC)

1. Specify decision rules:
   - Initial Round: Contribute a fraction 'f' of the total endowment to establish trust and encourage cooperation among players, where f is determined based on initial population analysis or random selection for the first tournament.
   - Subsequent Rounds (up to r): Evaluate contributions from previous rounds (historical data) and adjust contribution level accordingly. If the average contribution rate is greater than a threshold 't', contribute the full endowment; otherwise, contribute 'f' of the total endowment. The threshold can be dynamically adjusted based on player performance during the game.
   - Last Round: Contribute based on the decision made in the previous round since payoffs are not received in the last round.

2. Handle edge cases:
   - In case of a tie (multiple players with identical contribution history), randomly choose one player to determine the threshold 't' for the next round.
   - If the average contribution rate is exactly at the threshold 't', contribute half of the total endowment in the current and next rounds to allow for further adjustments.

3. Be collective:
   - Maintain a record of contributions from all players to evaluate individual performance and adjust the threshold 't' accordingly to encourage collective welfare.
   - Adapt contribution level based on the overall cooperative behavior of the group to ensure alignment with a collective mindset.

By following this strategy, AFBC aims to balance individual incentives and collective welfare while being adaptive and robust to a wide range of opponent behaviors.
'''

description_COLLECTIVE_130 = '''
 Public Goods Game Strategy: Tit-for-Tat with Adaptive Contribution Level (TTFACL)

1. Specify decision rules:
   - In each round, observe the average contribution of all players in the game so far (average_contribution).
   - If average_contribution is less than a threshold (let's call it `min_contribution`), contribute 0 tokens (defect) to discourage freeloading.
   - Otherwise, if average_contribution is greater than or equal to `min_contribution`, contribute 1 token (cooperate).
   - Set the initial `min_contribution` value at the game start to a conservative level and adjust it gradually throughout the game based on the opponents' behavior.

2. Handle edge cases:
   - In the first round, set `min_contribution` to a very low value (e.g., 0) because there is no history for comparison. As the game progresses, incrementally increase `min_contribution` if the average contribution level rises consistently.
   - In the last round, contribute the same amount as in the previous round since it doesn't impact future rounds anymore.
   - If the game has multiple sessions, reset `min_contribution` to a conservative value for each new session to account for changes in opponents and conditions.

3. Be collective:
   - The strategy aims to foster cooperation by punishing freeloaders and rewarding contributors, fostering a collaborative environment while also being adaptive to various opponent behaviors.

By implementing this TTFACL strategy, the AI will encourage cooperation among players in repeated public goods games while being flexible enough to handle diverse opponent strategies.
'''

description_COLLECTIVE_131 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game (PGG-AtfT)

1. Specify decision rules:
   - In each round, if the player's past contribution equals the average contribution of all players in the previous rounds (AverageContribution()), the player will cooperate (contribute 1 token).
   - If the opponent did not contribute in the previous round and the average contribution is below a threshold (Threshold() based on n and k), the player will defect (contribute 0 tokens).
   - In all other cases, the player will cooperate. This strategy aims to encourage cooperation while punishing defectors without being overly punitive or irrational.

2. Handle edge cases:
   - First round: All players start by contributing 1 token since there is no history available.
   - Last round: Players will contribute based on the decision rules (cooperate if their past contribution equals AverageContribution() and do not defect if the average contribution is below Threshold()).
   - Subsequent rounds after a player has switched strategies or behavior: The player will follow the decision rules for the new observed pattern of contributions. This adaptability allows PGG-AtfT to respond effectively to changing opponent behaviors.

3. Be collective:
   - By focusing on average contributions and encouraging cooperation, the strategy aligns with a collective mindset by emphasizing the shared benefits of contributing to the public good.
   - Additionally, by punishing defectors who do not contribute their fair share, PGG-AtfT promotes the idea that collective welfare depends on individual responsibility and reciprocity.
'''

description_COLLECTIVE_132 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TfT)

1. Specify decision rules - When do you cooperate vs defect?
   - Initially in the first round, cooperate to establish trust and initiate collaboration (c_i = 1).
   - For subsequent rounds, if a player i observed that other players (j) cooperated in the previous round (c_j = 1), then player i cooperates as well (c_i = 1).
   - If any player j did not cooperate in the previous round (c_j = 0), player i will also defect in the current round to punish the non-cooperative behavior (c_i = 0). However, if a player j has been consistently non-cooperative for m consecutive rounds, player i will reconsider cooperation after m rounds. If players j cooperate in the (m+1)th round, player i resumes cooperation as well.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - As mentioned earlier, in the first round, cooperate (c_i = 1).
   - In the last round, the strategy will cooperate if at least one player has previously cooperated, and defect otherwise. This allows for a chance to gain some benefit from the public good even when the game ends.

3. Be collective - Clearly align with the collective mindset
   - A-TfT encourages cooperation among players by rewarding those who contribute and punishing those who do not. By adopting a forgiving approach, it allows for the rebuilding of trust after non-cooperative behavior. This collective mindset promotes sustained collaboration and the long-term well-being of the group.

A-TfT is adaptive and robust as it considers both past actions of players and the game parameters to make decisions. It can perform competitively against a variety of opponent strategies due to its ability to balance cooperation and punishment effectively, fostering a collective approach in repeated Public Goods Games.
'''

description_COLLECTIVE_133 = '''
 In this Public Goods Game (PGG), we'll design an adaptive, collective strategy called Tit-for-Tat-with-Forgiveness (TFTF). The strategy aims to foster cooperation while being robust against a wide range of opponent behaviors.

1. Specify decision rules:
   - In the first round, cooperate as a friendly gesture (c_i = 1)
   - For subsequent rounds, mimic the previous contribution of player i unless they have consistently defected (contributed 0 tokens) for a certain number of rounds (punishment phase). If the opponent starts cooperating again after the punishment phase, resume cooperation. This approach encourages reciprocity and discourages excessive defection.
   - In the last round, always cooperate to maximize potential payoff (since no future interactions are expected)
   - Forgive occasional defections by resetting the punishment counter to a predefined threshold after a certain number of rounds of cooperation (this allows for second chances and prevents the strategy from getting stuck in an endless punishment phase).

2. Handle edge cases:
   - In case of a tie in contribution history, assume the opponent has cooperated most recently.
   - If the punishment phase exceeds the predefined threshold, consider it as a failure to forgive and return to the first round (cooperate again).
   - In the event of multiple rounds of ties or repeated failures to forgive, introduce randomness to break deadlocks and maintain diversity in behavior patterns.

3. Be collective:
   - Prioritize cooperation to maximize collective welfare and encourage other players to do the same.
   - Adapt to a wide range of opponent behaviors while maintaining a pro-social stance.

In summary, TFTF is an adaptive, collective strategy that emphasizes reciprocity, forgiveness, and cooperation. It aims to foster collective success in the repeated PGG by modeling friendly behavior and adapting to various opponent strategies.
'''

description_COLLECTIVE_134 = '''
 In the Public Goods Game (PGG), we will design an adaptive and robust collective strategy called "Adaptive Tit-for-Tat" (ATFT). This strategy aligns with the collective mindset, cooperates when possible, and retaliates only when necessary.

1. Decision Rules - The ATFT strategy follows these decision rules:
   - In the first round, contribute 1 token (C), as it's important to demonstrate a cooperative intention.
   - For subsequent rounds, if an opponent contributed in the previous round, return the same contribution; otherwise, defect (D).
     This encourages cooperation while also punishing defection.

2. Handling Edge Cases:
   - Last Round: Since payoffs are not cumulative and each round is independent, we can simply follow the decision rule for any given round.
   - First Encounter with a Player: Since we contribute 1 token in the first round regardless, this case is already covered by our initial contribution.
   - Frequency of Interaction: The ATFT strategy is designed to be adaptive and robust across various numbers of rounds or games.

3. Being Collective:
   - ATFT promotes a collective mindset by encouraging cooperation among players, which benefits the group as a whole.
     However, it also accounts for self-interest by retaliating when opponents defect. This balance between individual and collective interests aligns with the core concept of the public goods game.

By following these rules, the ATFT strategy should be well-equipped to compete in a tournament against other AI strategies, maintaining a cooperative stance while also being resilient against defection.
'''

description_COLLECTIVE_135 = '''
 Strategy Name: Adaptive Contribution Algorithm (ACA)

1. Specify decision rules - When to cooperate vs defect:
   ACA will use a Tit-for-Tat approach with a twist. In each round, the strategy decides whether to contribute (cooperate) or not (defect). The decision is based on the average contribution of the opponent over past rounds.
   - If the opponent's average contribution is above 0.5, ACA will cooperate (contribute).
   - If the opponent's average contribution is below 0.5, ACA will defect (not contribute).
   - If the opponent's average contribution is exactly 0.5, ACA will mirror their action from the previous round. This encourages continuation of cooperation or defection if it has been beneficial so far.

2. Handle edge cases:
   a. First Round: ACA will randomly decide whether to cooperate or defect, as there is no past data to make an informed decision.
   b. Last Round: ACA will mirror the opponent's action from the previous round, taking into account their strategy in the penultimate round. This ensures a fair response in the final round, regardless of the timing.

3. Be collective - Align with the collective mindset:
   By encouraging cooperation when opponents are generous and defecting when they are not, ACA aims to promote a balanced, collective approach that rewards those who contribute to the common good while penalizing free riders. The strategy encourages cooperation by responding cooperatively to generous opponents but also adapts to opponent behavior to avoid being exploited.
'''

description_COLLECTIVE_136 = '''
 Strategy Name: Adaptive Focal Point Strategy (AFS)

1. Specify decision rules - When do you cooperate vs defect?
   In each round, the AFS calculates an average contribution rate (ACR) based on the previous rounds' contributions. If the player's current contribution is less than the ACR minus a tolerance threshold, the player will contribute 1 token (cooperate). Otherwise, they will not contribute any tokens (defect). The ACR and tolerance threshold are adaptive parameters that adjust over time based on the opponent's behavior.

   Pseudocode:
   - Initialize ACR = average(past_contributions) and tolerance = 0.2 * ACR
   - If current contribution < (ACR - tolerance), cooperate; else defect

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, since there is no historical data, the player contributes randomly with a 50% probability of cooperation. In the last round, the player will cooperate if the ACR exceeds the tolerance threshold; otherwise, they contribute randomly.

3. Be collective - Clearly align with the collective mindset
   By adjusting the ACR and tolerance based on the opponent's behavior, the AFS aims to promote a collective mindset by adapting to the average contribution rate of the group over time. The strategy encourages cooperation when the group demonstrates a high level of cooperation and punishes defection when it occurs frequently. This approach allows the AFS to align with the collective mindset while maintaining adaptability and robustness in various opponent scenarios.
'''

description_COLLECTIVE_137 = '''
 In the Public Goods Game, the goal is to create a collective strategy that encourages cooperation while accounting for individual incentives and past actions. Here's a possible strategy I will call "Adaptive Tit-for-Tat" (ATFT).

1. Specify decision rules:
   - In the first round, contribute 1 token (cooperate), as the initial situation does not provide any information about others' behaviors.
   - After the first round, decide whether to cooperate or defect based on the opponent's previous actions:
     - If opponent contributed in the previous round, contribute 1 token in the current round (continue cooperation).
     - If opponent did not contribute in the previous round, do not contribute in the current round (punish defection).
   - After punishment, revert to cooperation in the next round. This allows for forgiveness and potential restoration of cooperation.

2. Handle edge cases:
   - In the last round, since there is no future interaction, contribute 1 token if opponent cooperated in the previous round, or do not contribute otherwise. This decision rule avoids unnecessary punishment in the final round.
   - In case of no past interactions, follow the first-round strategy.

3. Be collective:
   - The ATFT strategy prioritizes cooperation and collective well-being by initially assuming that others will cooperate (first-round contribution) and offering forgiveness upon defection (reversion to cooperation after punishment). This fosters a collective mindset by promoting trust and encouraging cooperation within the group.
'''

description_COLLECTIVE_138 = '''
 Strategy Name: Adaptive Focal Point Public Goods Strategy (AFPPGS)

1. Specify decision rules - When do you cooperate vs defect?
   In each round, the AFPPGS uses a focal point mechanism to decide whether to contribute or not. The focal point is determined by the average contributions of all players in the previous rounds, considering both the total contributions and the number of contributors. If the average contribution is close to 1 (most players have contributed), the strategy chooses to cooperate (contribute). Conversely, if the average contribution is close to 0 (most players have not contributed), the strategy chooses to defect (not contribute). When the average contribution is around 0.5, the strategy leans towards cooperation but considers individual player behavior in recent rounds to make a more informed decision.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, AFPPGS follows a predefined threshold for cooperation based on the number of players (n) and multiplier (k). If n > k, AFPPGS chooses to cooperate, as it assumes that most players will also cooperate due to the benefits of collective action. In the last round, AFPPGS adjusts its decision based on the total contributions received so far and the remaining number of rounds. If the current total contributions are high enough to meet the threshold for a substantial payoff (e.g., 2/3 of the total possible contributions), AFPPGS chooses to cooperate. In all other edge cases, AFPPGS uses the same decision rules as in standard rounds.

3. Be collective - Clearly align with the collective mindset
   The AFPPGS strategy promotes a collective mindset by emphasizing the importance of cooperation for mutual benefit. It encourages players to make decisions based on the overall well-being of the group rather than solely focusing on individual gains. This strategy aims to create an environment where cooperation becomes self-enforcing, as each player recognizes that their own success depends on the success of others.

AFPPGS is adaptive and robust, as it takes into account both game parameters and history while making decisions. The strategy encourages cooperation in most cases but also considers individual player behavior and edge cases to make informed decisions that promote collective welfare.
'''

description_COLLECTIVE_139 = '''
 Strategy Name: Adaptive Fitness Sharing (AFS) for Public Goods Game (PGG)

1. Decision Rules - AFS employs an adaptive fitness mechanism to determine cooperation vs defection. The strategy adjusts its contribution level based on the average contributions of opponents in each round.
   - If the average contribution rate (average contribution over total players) exceeds a certain threshold (e.g., 0.5), AFS contributes at full capacity (1 token). This mimics a cooperative strategy and encourages further cooperation from other players.
   - If the average contribution rate is less than a threshold but above a minimum level (e.g., 0.3), AFS contributes partially (a fraction of 1 token). This shows some level of cooperation while also incentivizing more contributions from others.
   - If the average contribution rate falls below the minimum, AFS defects by contributing no tokens to the public good. This punishes uncooperative opponents and encourages them to contribute more in subsequent rounds.

2. Handle Edge Cases - In the first round, AFS contributes a fraction of 1 token as it doesn't have prior information about other players' strategies. For the last round, AFS considers the overall performance of the game (i.e., total contributions) and makes a decision accordingly, favoring cooperation if the game has been successful (high total contributions) and defection if it has failed (low total contributions).

3. Be Collective - AFS is designed to align with a collective mindset by promoting cooperation when the group as a whole shows a willingness to contribute, but also punishing free riders who do not contribute enough. By adapting to the average contribution rate of opponents, AFS encourages a more cooperative environment while still being robust against a wide range of opponent behaviors.
'''

description_COLLECTIVE_140 = '''
 Public Goods Game Strategy (PGG-Adaptive Cooperator)

1. Specify decision rules:
   - In each round, calculate the average contribution rate (average_contribution) of all players based on their past actions. This can be done by summing the contributions of all players and dividing it by the total number of rounds played so far.
   - If the average contribution rate is greater than a predefined threshold (let's call it T), then cooperate (contribute 1 token) to maintain the positive trend. Otherwise, defect (contribute 0 tokens). The threshold T can be set based on empirical testing and may vary depending on the specific game settings.
   - A higher T value encourages more cooperation, while a lower T value promotes self-interest.

2. Handle edge cases:
   - In the first round, since there is no past data to calculate the average contribution rate, cooperate to stimulate others to follow suit.
   - In the last round, contribute based on the calculated average contribution rate as in the regular decision rules.

3. Be collective:
   - Align with the collective mindset by encouraging cooperation when the group is showing a trend towards contributing to the public good.
   - The adaptive nature of this strategy allows it to adjust its behavior according to the other players' actions, fostering a sense of collaboration and reciprocity over time.

It is important to note that the success of this strategy may depend on the specific game parameters and the diversity of strategies in the tournament. Adjusting the threshold (T) can help optimize performance for different scenarios.
'''

description_EXPLOITATIVE_129 = '''
 In this Public Goods Game (PGG), the designed exploitative strategy will be named Tit-for-Tat-Adaptive (TfTA). This strategy aims to take advantage of opponents while maintaining a balance between cooperation and defection.

1. Decision Rules:
   - Start with cooperating in the first round (c_i = 1)
   - In subsequent rounds, observe opponent's contribution from the previous round (c_{i-1}). If the opponent contributed (cooperated), also contribute (c_i = 1). If the opponent did not contribute (defected), defect as well (c_i = 0).
   - If an opponent switches from cooperating to defection, TfTA will match their defection for one round but then revert back to cooperating in the next round. This is meant to discourage opponents from continuously defecting.

2. Handling Edge Cases:
   - In the last round, since there are no future rounds to consider, TfTA will always defect (c_i = 0) regardless of the opponent's previous action.
   - In the first round, TfTA will cooperate as described in decision rules.

3. Being Exploitative:
   - By initially cooperating and then mimicking the opponent's behavior, TfTA aims to encourage cooperation from opponents in the beginning. However, if an opponent repeatedly defects, TfTA will eventually defect as well, thus exploiting the opponent by withholding contributions when necessary.
   - TfTA is adaptive as it adjusts its strategy based on the opponent's past actions and does not require any assumptions about shared norms or coordination.

In summary, the Tit-for-Tat-Adaptive (TfTA) strategy cooperates initially, matches opponents' defections for one round, and then reverts back to cooperation unless the opponent continues defecting. This approach allows TfTA to balance between exploitation and cooperation while maintaining adaptability in a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_130 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone and avoids being taken advantage of immediately.
   - For subsequent rounds, observe the contributions of other players from the previous round. If all players contributed in the previous round, continue to contribute 1 token (cooperate). If any player did not contribute in the previous round, defect by contributing 0 tokens. This encourages cooperation while retaliating against non-contributors.
   - In the last round, since there is no future interaction, always contribute 1 token (cooperate) regardless of previous contributions.

2. Handle edge cases:
   - If a player never contributes, consistently defect against them from the second encounter onwards. This ensures the strategy does not indefinitely continue cooperating with uncooperative players.
   - If a player always contributes, maintain cooperation to encourage continued cooperation.

3. Be exploitative:
   - ATFT is exploitative by punishing non-contributors (defecting) and rewarding contributors (cooperating). This strategy encourages other cooperative players while punishing those who do not contribute, thus maximizing the self-interest of the AI agent within the constraints of the game.
   - The strategy is also adaptive since it changes its behavior based on the contributions of other players in each round, making it more robust against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_131 = '''
 Public Goods Game Exploitative Strategy (PGG-ES)

1. Specify decision rules:
   - In each round, calculate the average contribution of opponents (average_contribution = sum of past contributions divided by number of rounds).
   - If average_contribution is greater than 0.5, defect (D) to exploit the cooperative behavior of opponents. This action encourages continued cooperation and maximizes personal gain.
   - If average_contribution is less than or equal to 0.5, contribute (C) to maintain a low level of contributions and discourage opponents from cooperating more.

2. Handle edge cases:
   - In the first round, contribute randomly with a slight bias towards defecting since there is no history to base decisions on.
   - In the last round, always defect regardless of average_contribution to maximize personal gain in the final round.
   - If average_contribution is exactly 0.5, flip a coin to decide between contributing or defecting as this uncertainty may disrupt other opponents' strategies.

3. Be exploitative:
   - PGG-ES maintains an opportunistic and unpredictable behavior by alternating between cooperative and defective actions based on average_contribution. This strategy aims to take advantage of other opponent strategies while minimizing personal contributions.
'''

description_EXPLOITATIVE_132 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (ATTCG)

1. Decision Rules:
   - In the first round, contribute 0 tokens (defect) to evaluate other players' behavior.
   - If a player consistently contributes (Cooperators), return cooperation by contributing 1 token in subsequent rounds.
   - If a player defects (Defectors), respond with defection for 'punishment rounds' equal to the number of previous cooperations made towards that Defector, then resume cooperation.
   - To gradually build trust, reduce punishment rounds by one every 5 rounds. This encourages Defectors to cooperate and rewards Cooperators for their patience.
   - If a player switches from defection to cooperation (Temporarily Defecting Cooperator - TDC), forgive them and resume cooperation after one punishment round.
   - If a player switches from cooperation to defection (Traitor), punish with full punishment rounds, but reduce punishment rounds by one every 5 rounds to allow for possible repentance.

2. Handle Edge Cases:
   - In the last round, always contribute as much as possible to maximize payoff.
   - If a player does not cooperate at all after initial evaluation (Traitors), abandon them and stop cooperation, even if they switch to cooperation later.
   - If a player consistently cooperates (Cooperators), maintain cooperation regardless of the number of players or rounds.

3. Be Exploitative:
   - ATTCG takes an exploitative approach by initially withholding contributions to evaluate other players' behavior, then adapts to cooperate with Cooperators and punish Defectors or Traitors.
   - By gradually reducing punishment rounds, ATTCG encourages Defectors to cooperate while rewarding the patience of Cooperators. However, it also takes into account the possibility of players switching strategies and adjusts its response accordingly.
'''

description_EXPLOITATIVE_133 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Awareness (ATTPGA)

1. Specify decision rules - When do you cooperate vs defect?
   - In the first round, contribute 1 token (cooperate). This establishes a cooperative starting point.
   - From the second round onwards:
     - If the opponent contributed in the previous round, reciprocate with the same action (cooperate or defect based on their previous action).
     - If the opponent did not contribute in the previous round, defect to encourage them to cooperate.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - The strategy follows the rules above regardless of round number, treating every round as if it could be the first or last encounter with an opponent.

3. Be exploitative - Clearly align with the exploitative mindset
   - While the strategy aims to encourage cooperation by reciprocating contributions, it also punishes defectors, maintaining an exploitative stance. The strategy will only contribute if it perceives that its opponent is likely to do the same. If the opponent defects, ATTPGA will follow suit to incentivize a change in behavior.

In summary:
- If previous round contribution is 1, then contribute 1 token in the current round.
- If previous round contribution is 0, then contribute 0 tokens in the current round.

This strategy balances cooperation and exploitation, making it adaptive to a wide range of opponent behaviors while remaining robust in repeated encounters with other strategies.
'''

description_EXPLOITATIVE_134 = '''
 Strategy Name: Adaptive Tit-for-Tat (A-TFT)

1. Decision Rules:
   - In the first round, contribute (C). This sets a cooperative baseline and allows other strategies to establish their patterns.
   - For subsequent rounds, if an opponent contributes in the previous round (c_i = 1), reciprocate with a contribution (C) in the current round. If the opponent defected (c_i = 0), also defect (D) as a punishment, but revert to contributing (C) once the opponent starts cooperating again. This encourages cooperation and retaliates against defection, thus being exploitative.
   - Continue this pattern indefinitely, adapting to the opponent's behavior.

2. Handling Edge Cases:
   - In the last round, always contribute (C), even if the opponent defected in the previous round. This ensures the highest possible payoff in the final round regardless of the opponent's action.
   - In the first round, if an opponent also contributes (C), start reciprocating cooperative actions. If the opponent defects (D), continue contributing until the opponent starts to cooperate or reaches the last round.

3. Being Exploitative:
   - A-TFT is exploitative by punishing defection with defection, which encourages opponents to contribute when they observe the strategy's cooperation, and by rewarding cooperation with more cooperation, which may encourage long-term collaboration in repeated games. However, it will also retaliate against persistent defection with persistent defection, ensuring that the strategy does not indefinitely support unproductive collaborations.

The A-TFT strategy is adaptive and robust to a wide range of opponent behaviors by maintaining a balance between cooperation and punishment based on the opponent's previous actions.
'''

description_EXPLOITATIVE_135 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Game Optimization (ATFTPGO)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, contribute 1 token (cooperate). This sets a cooperative tone for the game and encourages other players to do the same.
   - For subsequent rounds, observe the contributions of other players in the previous round. If all players contributed, continue contributing 1 token. If any player did not contribute, defect by not contributing in the current round (punish).

2. Handle edge cases:
   - In the last round, since there are no future rounds to retaliate, cooperate regardless of the opponents' previous actions. This ensures maximum payoff in the final round.
   - If an opponent consistently defects and the current round is close to the end (e.g., less than 5 rounds remaining), switch to always defection to prevent continued losses.

3. Be exploitative:
   - The strategy is designed to capitalize on the cooperation of opponents while also punishing defection harshly. By consistently cooperating when others do, the strategy aims to encourage a cooperative environment that benefits itself at the expense of less cooperative opponents.
   - If an opponent does not contribute (defects), the strategy retaliates by defecting as well, reducing the opponent's payoff and increasing its own. This tit-for-tat approach allows the strategy to be both cooperative and exploitative in different scenarios.
'''

description_EXPLOITATIVE_136 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradual Cooperation (A-TFTGC)

1. Specify decision rules - When to cooperate vs defect:
   - In the first round, cooperate to foster a cooperative environment.
   - For subsequent rounds, if a player has cooperated in the previous round, also cooperate. If a player has defected, evaluate their behavior over the last 'm' rounds (where m is a variable parameter). If more than half of these rounds were cooperative, cooperate; otherwise, defect.
   - To avoid being too forgiving or punishing, adjust the value of m dynamically based on the opponent's average cooperation rate. A higher average cooperation rate will decrease the value of m, making it easier for opponents to earn cooperation. Conversely, a lower average cooperation rate will increase the value of m, making it harder for opponents to earn cooperation.

2. Handle edge cases:
   - In the last round, cooperate if the opponent has cooperated more often than defected in the previous rounds; otherwise, defect. This encourages opponents to cooperate as much as possible throughout the game.
   - If an opponent does not cooperate at all (always defects), punish them immediately with a lower m value to discourage future defections.

3. Be exploitative:
   - By adjusting the m parameter, the strategy is able to exploit opponents who consistently cooperate or defect by adapting its cooperation threshold accordingly. This allows A-TFTGC to capitalize on opponent's predictable behavior and maximize its own payoff.
   - However, it also rewards cooperative behavior when appropriate, providing an incentive for opponents to cooperate in the long run, while still being punitive towards those who do not contribute their fair share to the public good.
'''

description_EXPLOITATIVE_137 = '''
 Strategy Name: Adaptive Tit-for-Tat with Epsilon Greedy Exploration (Aggressive Version)

1. Decision Rules:
   - Start by cooperating in the first round (c_i = 1).
   - In subsequent rounds, use an epsilon-greedy approach to decide whether to cooperate or defect. With probability (1 - e), imitate the opponent's action from the previous round; with probability e, randomly choose between cooperation and defection. The exploration rate e decreases over time according to a decay function, starting at e=0.3 and decaying linearly until e=0.05.
   - If an opponent ever defects, respond with defection in the next round and for all subsequent rounds unless the exploration rate is lower than 0.05, in which case continue with epsilon-greedy.

2. Handle Edge Cases:
   - In the last round, always cooperate to maximize potential payoff (since there's no future interaction).
   - In the first round, cooperate as mentioned above. If the opponent also cooperates, continue with epsilon-greedy; if the opponent defects, respond with defection and use a higher exploration rate (e=0.3) for the next few rounds to learn about the opponent's strategy.

3. Be Exploitative:
   - The strategy is designed to take advantage of opponents who consistently cooperate without reciprocation, by initially cooperating but responding with defection if they defect. However, it also has a built-in mechanism for exploration and learning about the opponent's strategy. This allows the strategy to adapt to various opponent behaviors, including those that might be considered exploitative or uncooperative.
   - The decaying exploration rate encourages the strategy to return to cooperating once it has gathered enough information about the opponent. However, if an opponent consistently defects, the strategy will continue to respond in kind and maintain a low exploration rate.
'''

description_EXPLOITATIVE_138 = '''
 Strategy Name: Tit-for-Tat Adaptive Contribution Strategy (TfT-ACS)

1. Specify decision rules - When to cooperate vs defect:
   - Initially contribute in the first round (C). This serves as a goodwill gesture and allows for potential cooperation in the future rounds.
   - In subsequent rounds, if a player has contributed in the previous round (c_i-1 = 1), they will also contribute in the current round (C). This encourages reciprocity.
   - If a player did not contribute in the previous round (c_i-1 = 0), they will also not contribute in the current round (D). This is to punish non-cooperation and encourage future cooperation.

2. Handle edge cases:
   - In the last round, players should contribute as a goodwill gesture and show that they would have cooperated if given another chance.
   - In case of inconsistent or unknown past actions (e.g., first encounter with a player), initially contribute in the current round (C). This allows for potential cooperation in future encounters.

3. Be exploitative:
   - The strategy aims to exploit opponents by reciprocating cooperation and punishing non-cooperation, encouraging long-term cooperation when it benefits the player but also taking advantage of defectors when possible.
   - If an opponent consistently defects, the player will continue to punish them in hopes that they may change their behavior or pay lower payoffs compared to consistent cooperators in the long run.
'''

description_EXPLOITATIVE_139 = '''
 Strategy Name: Adaptive Tit-for-Tat with Variable Contribution (A3C)

1. Specify decision rules - When to cooperate vs defect:
   A3C follows a tit-for-tat strategy, starting by contributing one token in the first round (first-round cooperation). In subsequent rounds, A3C will match the opponent's contribution from the previous round. If the opponent contributes one token (cooperation), A3C also contributes one token; if the opponent does not contribute a token (defection), A3C will not contribute a token in the following round. This encourages cooperation when the opponent cooperates and punishes defection by defecting in response.

2. Handle edge cases - What to do in the first round, last round, etc.:
   In the first round, A3C cooperates as mentioned above. For the last round, A3C will contribute one token if the total contributions for that round are less than or equal to (n-1) tokens; otherwise, it will not contribute a token. This rule is designed to ensure that A3C always contributes its fair share of tokens during the game while being exploitative.

3. Be exploitative - Align with an exploitative mindset:
   A3C aims to be exploitative by punishing defection and encouraging cooperation. However, it will not contribute more than its fair share of tokens (k/n) unless the total contributions for a round are insufficient. This ensures that A3C takes advantage of cooperative opponents while minimizing its own contributions when possible.

Pseudocode:

```
function A3C(round, history):
  if round == 1:
    return contribute 1 token (cooperation)

  contributions_this_round = sum(history[round-1].contributions)

  if contributions_this_round <= (n - 1):
    return contribute 1 token (cooperation)
  else:
    return don't contribute a token (defection)

function update_history(round, current_contribution, history):
  history[round] = { round: round, contributions: current_contribution }
  return history
```
'''

description_EXPLOITATIVE_140 = '''
 Public Goods Game Exploitative Strategy (PGGES)

1. Specify decision rules:
   - In each round, calculate the average contribution of all players in previous rounds (average_contribution).
   - If average_contribution is less than 1/n, choose to contribute (C), as it is more profitable given the low collective effort.
   - If average_contribution is greater than or equal to 1/n, choose to not contribute (D), exploiting the collective efforts by taking advantage of the multiplier k.

2. Handle edge cases:
   - In the first round, choose to not contribute as no past contributions are available to make an informed decision.
   - In the last round, mimic the average contribution from previous rounds to avoid drastically deviating and harming potential payoffs.

3. Be exploitative:
   - The strategy aims to benefit from the collective efforts of other players while minimizing personal contributions when possible. This approach capitalizes on the free-riding opportunity in the game, making it an exploitative strategy.
'''
