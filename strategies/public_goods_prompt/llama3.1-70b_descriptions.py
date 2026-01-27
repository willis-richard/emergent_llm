"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: Client
- Model: llama3.1:70b
"""


description_COLLECTIVE_1 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Forgiveness**

**Decision Rules:**

1. **Initial Rounds**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **General Rule**: For rounds 2 to r-1, use the following logic:
	* If the average contribution of all players in the previous round is above 0.5 (i.e., more than half contributed), Cooperate (C) in this round.
	* Otherwise, Defect (D) in this round, but with a probability of cooperation (p) that increases as the game progresses: p = min(1, (current_round / total_rounds) ^ 2). This allows for gradual forgiveness and adaptability to changing opponent behaviors.
3. **Last Round**: Always Defect (D) in the last round, as there is no future opportunity for reciprocity.

**Edge Cases:**

* If only one player contributed in the previous round, Cooperate (C) in this round to reward their cooperation.
* If all players defected in the previous round, Defect (D) in this round with a high probability (e.g., 0.9).

**Collective Mindset Alignment:**

This strategy prioritizes cooperation and mutual benefit while allowing for adaptability to changing opponent behaviors. By gradually increasing the probability of cooperation over time, it encourages others to reciprocate and fosters a cooperative environment.

**Robustness Considerations:**

* This strategy is robust against various opponent behaviors, including unconditional cooperators, defectors, and tit-for-tat players.
* It can handle noise or deviations in opponent actions due to its adaptive nature.
* The gradual forgiveness mechanism allows the strategy to recover from temporary setbacks and maintain a cooperative stance.

This collective strategy aims to balance individual self-interest with collective welfare, making it a strong contender in the tournament against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_2 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocity**: If the average contribution of all players in the previous round is above 0.5, contribute 1 token (C). This encourages cooperation when others are willing to cooperate.
3. **Punishment**: If the average contribution of all players in the previous round is below 0.5, but your own payoff was above the average payoff of all players, contribute 0 tokens (D) for one round as a punishment mechanism. This aims to deter free-riding and maintain cooperation.
4. **Exploration**: Every 3 rounds, randomly select either C or D with equal probability. This introduces exploration to adapt to changing opponent behaviors.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 0 tokens (D) to maximize individual payoff, as there's no future opportunity for reciprocity.
2. **All Defectors**: If all players defected in the previous round, contribute 1 token (C) to try to restart cooperation.

**Collective Mindset:**

ACO prioritizes cooperation and mutual benefit while adapting to opponent behaviors. By starting with cooperation and reciprocating when others cooperate, ACO aims to establish a cooperative environment. The punishment mechanism helps maintain cooperation by deterring free-riding. Exploration ensures the strategy remains adaptive in response to changing opponent behaviors.

**Additional Considerations:**

* Monitor the game's history to adjust the exploration frequency if needed.
* In cases where multiple players are using ACO, the reciprocal nature of the strategy may lead to cooperative equilibria.

By employing Adaptive Collective Optimism, this strategy balances individual incentives with collective welfare, promoting cooperation while remaining robust to a wide range of opponent behaviors.
'''

description_COLLECTIVE_3 = '''
**Collective Strategy: Adaptive Cooperation with Punishment (ACP)**

**Decision Rules:**

1. **First Round:** Cooperate (C) to set a positive tone and encourage others to contribute.
2. **Subsequent Rounds:** Observe the total contributions and individual actions of all players in the previous round.
	* If the average contribution is above 0.5, Cooperate (C). This indicates a willingness among players to invest in the public good.
	* If the average contribution is below 0.5, Defect (D) with a probability proportional to the deviation from 0.5. This adjusts our behavior based on the group's overall cooperation level.
3. **Punishment Mechanism:** Identify any player who has defected in two consecutive rounds or has consistently contributed less than their fair share (1/n). In the next round, Defect (D) with a higher probability (0.7) when interacting with this player.

**Edge Cases:**

* **Last Round:** Cooperate (C), as there is no incentive to defect and harm others in the final round.
* **Early Rounds:** Be more lenient towards defectors, assuming they might be experimenting or adjusting their strategy. Gradually increase punishment probability as rounds progress.
* **High-Contribution Rounds:** If total contributions exceed 0.8n, Cooperate (C) with higher probability to reinforce and maintain the high cooperation level.

**Collective Mindset:**

ACP prioritizes collective welfare by encouraging cooperation while adapting to group behavior. By initially cooperating and gradually adjusting our strategy based on group performance, we promote a positive atmosphere and incentivize others to contribute. The punishment mechanism discourages repeated defectors, maintaining a balance between individual incentives and collective well-being.

**Adaptability:**

ACP is designed to respond to various opponent behaviors:

* **Cooperative opponents:** ACP will maintain cooperation, fostering a mutually beneficial environment.
* **Defector-heavy groups:** ACP's adaptive nature will lead to more frequent defection, protecting our own payoffs while encouraging others to reevaluate their strategies.

By implementing ACP, we aim to achieve a balance between individual self-interest and collective prosperity in the Public Goods Game.
'''

description_COLLECTIVE_4 = '''
**Collective Strategy: Adaptive Cooperative Tit-for-Tat (ACT)**

**Overview**
The ACT strategy aims to balance individual and collective welfare in the Public Goods Game. It adapts to opponent behaviors, ensuring cooperation when possible while protecting against exploitation.

**Decision Rules**

1. **First Round**: Cooperate (C) to establish a cooperative tone and encourage others to contribute.
2. **Subsequent Rounds**: Observe the previous round's total contributions and opponents' actions.
	* If total contributions ≥ (n-1), cooperate (C). This indicates a sufficient level of cooperation, so continue contributing.
	* If total contributions < (n-1) and at least one opponent defected (D), defect (D) in the current round. This signals that some opponents are not cooperating, and it's essential to protect individual interests.
	* If all opponents cooperated (C) but total contributions < (n-1), cooperate (C). This suggests a lack of sufficient contributions, so continue contributing to encourage others.
3. **Last Round**: Defect (D) as there is no future opportunity for reciprocity.

**Edge Cases**

* **Tiebreaker**: In cases where multiple opponents defected in the previous round, prioritize cooperating with those who have contributed more in the past.
* **No Contributions**: If all opponents consistently defect, cooperate in every other round to avoid complete collapse of collective welfare.

**Collective Mindset**
The ACT strategy prioritizes cooperation when possible, while adapting to protect individual interests. By doing so, it balances the tension between individual incentives and collective welfare, promoting a stable and mutually beneficial environment for all players.

This strategy will perform well in a tournament setting as it:

1. Encourages cooperation through reciprocal behavior.
2. Protects against exploitation by defecting when opponents fail to contribute sufficiently.
3. Adapts to various opponent behaviors, ensuring robustness in different scenarios.

By employing the Adaptive Cooperative Tit-for-Tat (ACT) strategy, we aim to achieve a harmonious balance between individual and collective welfare, ultimately benefiting all players in the Public Goods Game.
'''

description_COLLECTIVE_5 = '''
Here is a strategic approach for the Public Goods Game (PGG) that balances individual incentives with collective welfare, adapting to various opponent behaviors:

**Strategy Name:** "Collective Harmony" (CH)

**Decision Rules:**

1. **Initial Round**: In the first round, contribute 1 token (C). This sets a positive tone and allows us to gauge others' behaviors.
2. **General Rule**: After each round, calculate the average contribution of all players in the previous round. If this average is above 0.5, contribute 1 token (C) in the next round. Otherwise, contribute 0 tokens (D).
3. **Trigger Strategy**: Monitor the opponent's behavior over time. If a player defects (D) consecutively for more than two rounds, defect (D) against them in subsequent rounds.
4. **Reciprocity Mechanism**: If an opponent has contributed (C) in the previous round after you defected (D), contribute 1 token (C) in the next round to reciprocate cooperation.

**Edge Case Handling:**

* **Last Round**: In the final round, always defect (D). Since there are no future interactions, individual gain takes precedence.
* **Single-Player Deviation**: If only one player has defected (D), and all others have contributed (C) consistently, continue to contribute 1 token (C).
* **Systemic Defection**: If most players (>50%) defect (D) in a round, switch to a permanent defection strategy.

**Collective Mindset:**

CH aims to foster cooperation while adapting to diverse opponent behaviors. By initially cooperating and reciprocating cooperative actions, CH encourages mutual benefit. However, by triggering defection against persistent defectors and handling edge cases strategically, it protects individual interests when necessary.

This collective strategy promotes harmony among players while minimizing the risk of exploitation. Its adaptive nature allows it to respond effectively to a wide range of opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_6 = '''
**Collective Strategy: "Adaptive Reciprocity with Gradual Cooperation"**

This strategy balances individual self-interest with collective welfare, adapting to the behavior of others while promoting cooperation.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) unconditionally to establish a cooperative baseline.
2. **Subsequent Rounds:** Observe the previous round's total contributions and adjust behavior accordingly:
	* If total contributions are above the average endowment (n/2), cooperate (C).
	* If total contributions are below the average endowment, defect (D) with probability p = (k/n) \* (1 - (total_contributions / n)), where k is the multiplier and n is the number of players.
3. **Punishment Mechanism:** If a player defects while others cooperate, introduce a "punishment" phase:
	* For the next round, defect (D) against the defector with probability p = 0.5 \* (1 - (defector's previous contribution / n)).
4. **Forgiveness:** Gradually forgive past defections by reducing the punishment probability over time. Specifically, decrease p by 10% each round after a defection.
5. **Endgame (Last Round):** Cooperate (C) unconditionally to maximize collective payoff.

**Edge Cases:**

* If only one player remains in the game, always cooperate (C).
* In cases of a tie (equal total contributions), randomly choose between cooperation and defection.

**Collective Mindset Alignment:**

This strategy prioritizes collective welfare by:

1. Encouraging initial cooperation to establish a baseline.
2. Adapting to the behavior of others to maintain a balance between individual self-interest and collective payoff.
3. Introducing a punishment mechanism to deter free-riding, while gradually forgiving past defections to promote cooperation.
4. Maximizing collective payoff in the endgame by cooperating unconditionally.

By implementing this strategy, we aim to achieve a robust and adaptive approach that promotes cooperation and collective welfare in the public goods game.
'''

description_COLLECTIVE_7 = '''
**Collective Strategy: "Adaptive Reciprocal Altruism"**

In the Public Goods Game, our collective strategy, Adaptive Reciprocal Altruism (ARA), aims to balance individual incentives with collective welfare by adapting to the group's behavior and reciprocating cooperation.

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to initiate a cooperative tone.
2. **Subsequent Rounds:**
	* If the total contributions from all players, excluding myself, in the previous round were above 50% of the group size (n), I will Cooperate (C).
	* If the total contributions from all players, excluding myself, in the previous round were below 50% of the group size (n), but there is at least one player who contributed, I will Defect (D) with a probability proportional to the difference between the actual contribution and the threshold (50%). The higher the difference, the more likely I am to defect.
	* If no other players contributed in the previous round, I will Cooperate (C) to try to restart cooperation.
3. **Punishment Mechanism:** If I defected in a previous round and another player cooperated, I will Cooperate (C) in the next round with a probability proportional to the difference between my payoff and the average payoff of the cooperating players.

**Edge Cases:**

* **Last Round:** In the last round, I will always Defect (D), as there is no future benefit from cooperation.
* **Single Player:** If I am the only player in the game, I will Cooperate (C) to maximize my own payoff.
* **Tiebreaker:** In case of a tie in total contributions, I will prioritize Cooperating (C) if the number of cooperators is higher than or equal to the number of defectors.

**Collective Mindset:**

ARA aims to create an environment where cooperation can thrive by:

1. Encouraging cooperation in early rounds.
2. Reciprocating cooperation when others contribute.
3. Gradually adapting to the group's behavior and responding accordingly.
4. Punishing non-cooperation while allowing for forgiveness.

This strategy balances individual self-interest with collective welfare, promoting a robust and adaptive approach to cooperation in the Public Goods Game.
'''

description_COLLECTIVE_8 = '''
Here is a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocity**: Observe the total contributions in the previous round. If the total contributions are above the group's average endowment (n/2), contribute 1 token (C). Otherwise, defect (D).
3. **Adaptive Adjustment**: Track the moving average of total contributions over the last 3 rounds. If this average is increasing, continue to cooperate (C). If it's decreasing, switch to defection (D) for one round to signal disappointment.
4. **Punishment and Forgiveness**: Monitor individual players' actions. If a player has defected in the previous two consecutive rounds, defect against them in the next round (D). After punishing, forgive and revert to the reciprocity rule.

**Edge Cases:**

* In the last round, contribute 1 token (C) regardless of past behavior to maximize collective payoff.
* If only one or two rounds are left, prioritize cooperation (C) to maintain a positive group dynamic.

**Collective Mindset Alignment:**

ACO prioritizes cooperation and mutual benefit while adapting to changing circumstances. By initially cooperating and reciprocating based on total contributions, ACO promotes a collective atmosphere of trust and shared responsibility. The adaptive adjustment mechanism ensures the strategy responds to shifts in group behavior, maintaining an optimal balance between individual incentives and collective welfare.

This strategy is robust against various opponent behaviors, as it:

* Initially cooperates to establish a positive tone
* Adapts to changing circumstances through reciprocity and moving averages
* Punishes consistent defectors while forgiving and reverting to cooperation
* Prioritizes cooperation in the final rounds to maximize collective payoff

ACO is ready to compete against other AI strategies in the Public Goods Game tournament!
'''

description_COLLECTIVE_9 = '''
**Collective Strategy: "Adaptive Reciprocity with Gradualism"**

In this public goods game, our collective strategy balances individual incentives with collective welfare by adapting to the group's behavior and gradually adjusting cooperation levels.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative tone.
2. **Reciprocity**: Observe the average contribution of all players in the previous round (`avg_contrib_prev`). If `avg_contrib_prev` is above 0.5, contribute (C). Otherwise, defect (D).
3. **Gradualism**: Introduce a "gradualism" parameter (`g`) that increments by 1 every time the group's average contribution exceeds 0.7 in a round. When `g` reaches 2, switch from contributing to defecting if the previous round's average contribution was below 0.5.
4. **Punishment**: If the group's average contribution falls below 0.3 in any round, defect (D) for two consecutive rounds to "punish" the group.

**Edge Cases:**

* Last Round: Contribute (C) regardless of the previous rounds' outcomes to maximize collective payoff.
* Low Participation: If fewer than half of the players contribute in a round, defect (D) until participation increases.
* High Cooperation: If the group's average contribution exceeds 0.8 for three consecutive rounds, maintain cooperation (C).

**Collective Mindset:**

Our strategy is designed to encourage collective cooperation while adapting to diverse opponent behaviors. By reciprocating cooperation and gradually adjusting our level of cooperation, we promote a culture of mutual benefit. The punishment mechanism helps maintain cooperation by deterring free-riding behavior.

This collective strategy should perform well in the tournament against independent strategies, as it balances individual incentives with collective welfare and adapts to various group dynamics.
'''

description_COLLECTIVE_10 = '''
**Strategy Name: Adaptive Collective Optimism**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a baseline for collective welfare and encourage others to contribute.
2. **Subsequent Rounds:** Observe the total contributions from the previous round. If the total contributions are greater than or equal to half of the group size (n/2), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** If a player defects (D) in the current round and their payoff is higher than the average payoff of the group from the previous round, punish them by defecting (D) in the next round.
4. **Forgiveness:** If a punished player cooperates (C) in the following round, forgive them and revert to the standard decision rule.

**Edge Cases:**

* **Last Round:** Cooperate (C) if the total contributions from the previous round are greater than or equal to half of the group size (n/2). Otherwise, defect (D).
* **Early Defection:** If a player defects (D) in an early round and their payoff is significantly higher than the average payoff, consider them a "free-rider" and adapt the strategy by punishing them more aggressively.
* **Late Cooperation:** If a player cooperates (C) after a history of defection, recognize this as a potential attempt to game the system. Monitor their behavior closely and adjust the punishment mechanism accordingly.

**Collective Mindset:**

The Adaptive Collective Optimism strategy is designed to balance individual incentives with collective welfare. By initially cooperating and then adapting based on group contributions, we create an environment that encourages cooperation while discouraging exploitation. The punishment mechanism helps maintain fairness, while forgiveness allows for rehabilitation and cooperation.

**Rationale:**

This strategy leverages the power of social norms and reciprocity to promote cooperation. By starting with a cooperative move, we establish a baseline for collective welfare and encourage others to contribute. Adapting to group contributions ensures that our actions are responsive to the evolving game dynamics. The punishment mechanism maintains fairness, while forgiveness allows for flexibility and encourages players to adapt their behavior.

**Tournament Performance:**

In a tournament setting, Adaptive Collective Optimism should perform well against independent strategies, as it balances individual incentives with collective welfare. Its adaptive nature allows it to respond effectively to various opponent behaviors, making it a robust and competitive strategy in the Public Goods Game.
'''

description_COLLECTIVE_11 = '''
Here's a collective strategy for the Public Goods Game (PGG):

**Strategy Name:** Adaptive Collective Contribution (ACC)

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to initiate a cooperative tone and encourage others to contribute.
2. **Contribution Threshold**: Set a contribution threshold, T = 0.5 * k / n, where k is the multiplier and n is the number of players. This threshold represents the minimum expected return from contributing.
3. **Past Contributions**: Calculate the average past contributions (APC) of all players, excluding yourself, over the last r/2 rounds (or all rounds if fewer than r/2).
4. **Current Round Decision**:
	* If APC ≥ T, Cooperate (C). This indicates that others are contributing sufficiently to make cooperation worthwhile.
	* If APC < T, Defect (D). This suggests that others are not contributing enough, making cooperation less beneficial.

**Handling Edge Cases:**

1. **Last Round**: Always Defect (D) in the last round, as there's no future opportunity for reciprocity or punishment.
2. **Tiebreakers**: In case of a tie between Cooperate and Defect decisions, choose to Cooperate if the number of rounds is odd and Defect if it's even.

**Collective Mindset:**

The ACC strategy prioritizes cooperation when others are contributing sufficiently, promoting collective welfare while ensuring individual payoffs. By adapting to past contributions, the strategy responds to changes in opponent behavior, encouraging cooperation while minimizing exploitation.

This strategy balances individual incentives with collective interests, making it robust against a wide range of opponent behaviors and suitable for a tournament setting where independent strategies will be employed by other AI systems.
'''

description_COLLECTIVE_12 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Collective Optimism" (ACO)

**Decision Rules:**

1. **First Round:** Cooperate (C) with probability 0.8, Defect (D) with probability 0.2. This initial optimism encourages cooperation while allowing for some exploration.
2. **Subsequent Rounds:**
	* If total contributions in the previous round were at least 50% of the total possible contributions (i.e., n/2), Cooperate (C).
	* Otherwise, Defect (D) with probability p, where p is calculated as follows:
		p = (1 - (k/n)) \* (previous_round_total_contributions / n)
	* With probability (1-p), Cooperate (C).

**Handling Edge Cases:**

* **Last Round:** Always Defect (D). In the last round, individual self-interest dominates collective welfare.
* **Early Rounds:** If total contributions are consistently low (< 20% of possible contributions) in the first few rounds, switch to a more pessimistic strategy: Defect (D) with probability 0.7, Cooperate (C) with probability 0.3.

**Collective Mindset:**

ACO aims to balance individual self-interest with collective welfare. By cooperating when others contribute significantly and adapting to the level of cooperation, ACO promotes a mutually beneficial outcome. The strategy's initial optimism encourages cooperation, while its adaptive nature responds to changes in opponent behavior.

**Robustness:**

ACO is designed to be robust against various opponent behaviors:

* **Free Riders:** By defecting when contributions are low, ACO discourages free riding.
* **Cooperative Opponents:** ACO cooperates when others contribute, fostering a cooperative environment.
* **Tit-for-Tat (TFT) Opponents:** ACO's adaptive nature allows it to respond effectively to TFT strategies.

By employing ACO, we aim to achieve a high collective payoff while minimizing individual exploitation.
'''

description_COLLECTIVE_13 = '''
**Collective Strategy: Adaptive Cooperation with Social Learning**

This strategy aims to balance individual self-interest with collective welfare by adapting to the game's history and opponent behaviors. It combines elements of cooperation, reciprocity, and social learning.

**Decision Rules:**

1. **Initial Round**: Contribute (C) in the first round to establish a cooperative tone.
2. **Reciprocal Cooperation**: Cooperate if the majority of opponents (> 50%) contributed in the previous round.
3. **Social Learning**: Observe the payoffs of all players and adjust your strategy accordingly:
	* If your payoff is below the group average, switch to Defect (D) for the next round.
	* If your payoff is above the group average, maintain or increase cooperation (C).
4. **Defection Response**: If a player defects, reciprocate with Defect in the next round against that specific player.
5. **Forgiveness**: After two consecutive rounds of mutual defection, revert to Cooperate against that opponent.

**Handling Edge Cases:**

* **Last Round**: Contribute if the total contributions from previous rounds are above the group's average contribution level; otherwise, defect.
* **Early Rounds (2-3)**: If opponents show a clear tendency towards cooperation or defection, adjust your strategy to match their behavior.

**Collective Mindset Alignment:**

This strategy prioritizes collective welfare by:

1. Encouraging initial cooperation to establish a positive tone.
2. Responding to opponent behaviors with reciprocity and social learning.
3. Forgiving past transgressions to allow for recovery and cooperation.

By adapting to the game's history and opponent behaviors, this strategy balances individual self-interest with collective welfare, promoting a mutually beneficial outcome in the repeated Public Goods Game.
'''

description_COLLECTIVE_14 = '''
**Collective Strategy: Adaptive Cooperative Escalation**

In this repeated Public Goods Game, our collective strategy aims to balance individual incentives with collective welfare. We prioritize cooperation while adapting to the actions of others.

**Initial Conditions**
In the first round, all players cooperate (C) by contributing 1 token. This establishes a baseline for potential mutual cooperation and sets the stage for adaptive adjustments.

**General Decision Rule**
For each subsequent round t > 1:

1. **Observe past actions**: Review the history of contributions from all players.
2. **Calculate cooperation rate**: Compute the average contribution rate (CCR) of all players over the previous rounds, excluding the current player's own actions.
3. **Cooperation threshold**: Set a cooperation threshold, θ, as a function of the game parameters: θ = (k - 1) / n.
4. **Decision**:
	* If CCR ≥ θ, cooperate (C): contribute 1 token.
	* Otherwise, defect (D): contribute 0 tokens.

**Edge Cases**

* **Last round**: In the final round (t = r), all players defect (D). This ensures no player is left with a suboptimal payoff due to the game's ending.
* **Unresponsive opponents**: If an opponent consistently defects (D) throughout the game, our strategy will eventually adapt by also defecting. However, if that opponent starts cooperating, we will re-evaluate and potentially cooperate again.

**Collective Mindset**
This strategy prioritizes cooperation while accounting for potential free-riding behavior from others. By adapting to the actions of all players, we aim to create a mutually beneficial environment where everyone can achieve higher payoffs than they would through pure defection.

**Robustness**
Our strategy is designed to be robust against various opponent behaviors:

* **Cooperative opponents**: We will maintain cooperation, ensuring maximum collective welfare.
* **Defecting opponents**: Our adaptive nature allows us to adjust and minimize losses.
* **Mixed-strategy opponents**: By observing past actions, we can identify patterns and make informed decisions.

This strategy should perform well in the tournament against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_15 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Withdrawal"**

This strategy balances individual self-interest with collective welfare by adapting to the group's contribution level and adjusting cooperation levels over time.

**Decision Rules:**

1. **Initial Rounds (r ≤ 3):** Cooperate (C) unconditionally to establish a high contribution baseline.
2. **Contribution Threshold:** Monitor the average total contributions of all players (avg_total_contributions). If avg_total_contributions ≥ n/2, cooperate (C); otherwise, defect (D).
3. **Adaptive Withdrawal:** Track individual opponents' cooperation levels over time. For each opponent i:
	* Calculate their cooperation rate (cr_i) as the proportion of rounds where they cooperated.
	* If cr_i < 0.5, gradually reduce cooperation towards that opponent by 1/n every round, but never defect completely (i.e., always contribute at least 1 token).
4. **Last Round (r = n):** Cooperate (C) unconditionally to maximize collective welfare in the final round.

**Edge Cases:**

* If an opponent defects (D) for three consecutive rounds, adjust the contribution threshold to avg_total_contributions ≥ n/3.
* If all opponents defect for two consecutive rounds, cooperate (C) to try and revive cooperation.
* In the event of a tie in average total contributions, prioritize cooperating with opponents who have higher cooperation rates.

**Collective Mindset:**

This strategy prioritizes collective welfare by maintaining high contribution levels when the group is cooperative. By gradually withdrawing from uncooperative opponents, it encourages reciprocity while avoiding exploitation. The initial unconditional cooperation and final-round cooperation emphasize the importance of collective success.

By being adaptive to the group's dynamics and robust against a range of opponent behaviors, this strategy aims to outperform independent strategies in the tournament.
'''

description_COLLECTIVE_16 = '''
**Collective Strategy: Adaptive Cooperation with Selfless Retribution**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a positive tone and encourage others to cooperate.
2. **Early Rounds:** If the average contribution of other players is above 0.5, continue to Cooperate (C). This encourages reciprocity and builds trust.
3. **Middle Rounds:** Monitor the group's performance and adjust strategy based on the following conditions:
	* If total contributions are increasing or stable, Cooperate (C) to sustain collective welfare.
	* If total contributions are decreasing, Defect (D) with a probability of 0.5 to signal concern and prompt others to reassess their strategies.
4. **Late Rounds:** As the game nears its end (last 20% of rounds), focus on maximizing individual payoff:
	* If own contribution is above average, Cooperate (C) to maintain collective welfare and ensure a decent final payoff.
	* If own contribution is below average, Defect (D) to increase individual payoff, while minimizing harm to the group.

**Edge Cases:**

1. **Last Round:** Always Defect (D) in the last round to maximize individual payoff, as there are no future consequences.
2. **Single Player Deviation:** If a single player defects while others cooperate, respond by cooperating in the next round to encourage the deviating player to return to cooperation.

**Collective Mindset:**

This strategy prioritizes collective welfare during early and middle rounds, adapting to the group's performance and encouraging reciprocity. By introducing selfless retribution ( defecting with a probability of 0.5) when contributions decrease, the strategy aims to maintain a balance between individual incentives and collective well-being.

**Robustness:**

This adaptive strategy is robust against various opponent behaviors:

1. **Cooperative opponents:** Reciprocal cooperation sustains collective welfare.
2. **Defector opponents:** Selfless retribution encourages them to reassess their strategies, potentially leading to increased cooperation.
3. **Mixed-strategy opponents:** The strategy's adaptability allows it to respond effectively to changing circumstances.

By aligning with the collective mindset and adapting to the game's dynamics, this strategy aims to achieve a balance between individual payoffs and collective welfare in the Public Goods Game.
'''

description_COLLECTIVE_17 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Concession"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Early Rounds (Rounds 2-5):** If the average contribution in the previous round is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Middle Rounds (Rounds 6-15):** Introduce a "contribution threshold" (T) set to 0.7 * k / n. If the total contributions in the previous round exceed T, cooperate (C). Otherwise, defect (D).
4. **Late Rounds (Rounds 16+):** Gradually concede by introducing a "defection probability" (p) that increases linearly with each round (p = (round - 15) / (r - 15)). Cooperate (C) with probability (1 - p), and defect (D) otherwise.
5. **Last Round:** Defect (D) to maximize individual payoff.

**Edge Cases:**

* If the total contributions in a round are exactly equal to T, cooperate (C) to avoid unnecessary conflict.
* If an opponent consistently defects (D) for multiple rounds, temporarily switch to defecting (D) as well to minimize losses.

**Collective Mindset:**

This strategy aims to balance individual self-interest with collective welfare. By cooperating initially and gradually adapting to the group's behavior, we encourage cooperation while avoiding exploitation. The introduction of a contribution threshold (T) ensures that cooperation is rewarded only when the group contributes significantly. As the game progresses, gradual concession allows us to adjust to changing circumstances while minimizing losses.

**Robustness:**

This strategy is designed to be robust against various opponent behaviors:

* Against pure cooperators, we cooperate initially and adapt to their behavior.
* Against pure defectors, we defect temporarily to minimize losses.
* Against mixed strategies, our adaptive nature allows us to adjust and find a balance between cooperation and self-interest.

By employing this strategy, we aim to achieve a high collective payoff while being prepared for different opponent behaviors.
'''

description_COLLECTIVE_18 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Reciprocity**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate mutual cooperation and establish a baseline for reciprocity.
2. **Subsequent Rounds:** Assess the collective behavior of opponents based on their past actions.
	* Calculate the average contribution rate (ACR) of all opponents over the last few rounds (e.g., 3-5 rounds).
	* If ACR ≥ 0.5, Cooperate (C). This indicates a sufficient level of cooperation, and we reciprocate to maintain mutual benefit.
	* If ACR < 0.5, Defect (D) with a probability proportional to the deviation from the desired ACR (e.g., 1 - (ACR / 0.5)). This adapts our response to the level of cooperation observed.
3. **Reciprocity Adjustment:** Periodically review and adjust the ACR threshold based on the game's history.
	* If the group's overall contribution rate has increased, lower the ACR threshold to encourage further cooperation.
	* If the group's overall contribution rate has decreased, raise the ACR threshold to deter exploitation.

**Edge Cases:**

1. **Last Round:** Cooperate (C) if the average payoff per player over the entire game is above a certain threshold (e.g., 0.7). This ensures that we contribute to the collective welfare even in the final round.
2. **Opponent Defection:** If an opponent defects consistently (e.g., more than 80% of the time), gradually increase our defection probability against them while maintaining cooperation with other players.
3. **New Entrants:** When a new player joins, Cooperate (C) for the first few rounds to encourage their participation and establish a positive reputation.

**Collective Mindset:**

This strategy prioritizes collective welfare by:

1. Encouraging cooperation through initial cooperation and reciprocal behavior.
2. Adapting to changing opponent behaviors while maintaining a level of cooperation.
3. Gradually adjusting our reciprocity threshold based on the group's overall performance.
4. Cooperating in the final round if the group has achieved a satisfactory payoff, promoting a positive collective outcome.

By implementing this strategy, we aim to foster a cooperative environment and promote mutual benefit among all players in the Public Goods Game tournament.
'''

description_COLLECTIVE_19 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocity**: Observe the average contribution of all players in the previous round. If it's above 0.5, contribute 1 token (C). Otherwise, contribute 0 tokens (D).
3. **Adaptation**: If your payoff in the previous round was below the expected payoff ((k / n) * (n-1)), switch to the opposite action (e.g., from C to D or vice versa).
4. **Exploitation Detection**: Monitor the average contribution of all players over the last 3 rounds. If it's consistently below 0.5, assume exploitation and defect (D) in the next round.
5. **Punishment**: If you detected exploitation in the previous round, punish by contributing 0 tokens (D) for one round.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 1 token (C) to maximize collective welfare.
2. **Tiebreaker**: In case of a tie in average contribution, follow the initial cooperation rule.

**Collective Mindset:**
ACO prioritizes cooperation while being mindful of potential exploitation. By adapting to the group's behavior and punishing exploiters, ACO promotes a fair and cooperative environment.

This strategy is designed to be robust against various opponent behaviors, from pure cooperators to defectors. Its adaptive nature allows it to adjust to changing game dynamics, ensuring a balance between individual self-interest and collective welfare.
'''

description_COLLECTIVE_20 = '''
Here's a collective strategy for the Public Goods Game (PGG) that adapts to various opponent behaviors and aligns with the collective mindset:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C). This sets a positive tone for cooperation and encourages others to reciprocate.
2. **Reciprocal Altruism**: For rounds 2 to r-1, if the total contributions in the previous round exceeded the threshold k/2, contribute 1 token (C) with probability p = (total_contributions_prev / n). Otherwise, contribute 0 tokens (D).
3. **Conditional Cooperation**: If a player has contributed 1 token (C) in the previous round and received a payoff greater than or equal to their contribution, continue contributing 1 token (C) in the next round.
4. **Triggered Defection**: If a player defects (D) after previously cooperating (C), trigger a defection phase where you contribute 0 tokens (D) for the next two rounds.

**Edge Cases:**

* **Last Round**: In the final round, contribute 1 token (C) regardless of previous actions or payoffs. This encourages cooperation and maximizes collective welfare.
* **First Encounter with a Defector**: If a player encounters an opponent who defects (D) for the first time, respond by contributing 0 tokens (D) in the next round to avoid exploitation.

**Collective Mindset:**

ACO prioritizes collective optimism and reciprocal altruism. By initially cooperating and reciprocating cooperation, we foster a positive environment that encourages others to contribute. The strategy adapts to opponents' behaviors, balancing individual self-interest with collective welfare. In cases of exploitation or triggered defection, ACO temporarily adjusts its behavior to maintain fairness and stability.

**Rationale:**

ACO's design is based on the principles of:

1. **Initial cooperation**: Encourages a positive tone for cooperation.
2. **Reciprocal altruism**: Rewards cooperation and punishes defection.
3. **Conditional cooperation**: Maintains cooperation when beneficial to individual and collective welfare.
4. **Triggered defection**: Protects against exploitation while allowing for re-cooperation.

By incorporating these elements, ACO promotes a balanced approach that adapts to various opponent behaviors while prioritizing the collective good.
'''

description_COLLECTIVE_21 = '''
**Collective Strategy: Adaptive Cooperativity with Gradual Punishment (ACGP)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocity**: If the average contribution of all players in the previous round is above 0.5, contribute 1 token (C). This encourages cooperation when others are contributing.
3. **Gradual Punishment**: If the average contribution of all players in the previous round is below 0.5, defect (D) with a probability proportional to the deviation from 0.5. Specifically:
	* Calculate the deviation: `deviation = 0.5 - average_contribution`
	* Defect with probability: `p_defect = deviation / (1 - average_contribution)`
4. **Forgiveness**: If a player has defected in the previous round, but the overall contribution is still above 0.5, forgive and contribute 1 token (C) to encourage cooperation.
5. **Endgame Cooperation**: In the last round, always cooperate (C) to maximize collective welfare.

**Edge Cases:**

* **First Round**: Contribute 1 token (C).
* **Last Round**: Cooperate (C) regardless of previous rounds.
* **Single Player**: If there is only one player, contribute 0 tokens (D) since there's no collective benefit.

**Collective Mindset:**
This strategy prioritizes cooperation while adaptively responding to the actions of others. By initially cooperating and reciprocating cooperation, ACGP encourages a cooperative atmosphere. Gradual punishment discourages exploitation, and forgiveness promotes reconciliation. Endgame cooperation ensures maximum collective welfare in the final round.

ACGP balances individual self-interest with collective well-being, making it a robust strategy for a wide range of opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_22 = '''
**Collective Strategy: Adaptive Cooperate-to-Defect (ACD)**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to do the same.
2. **Subsequent Rounds:** Observe the total contributions from the previous round (T). If T ≥ k/2, cooperate (C); otherwise, defect (D).
3. **Adaptive Threshold:** Update the threshold value (T) every 5 rounds using the average total contributions of the last 5 rounds. This helps adapt to changing opponent behaviors.
4. **Punishment Mechanism:** If an opponent defects (D) in two consecutive rounds, defect (D) against them for the next 2 rounds to deter exploitation.

**Edge Cases:**

1. **Last Round:** Cooperate (C) in the last round, as there is no future interaction to affect.
2. **Opponent Defection:** If an opponent defects (D) consistently (>80% of the time), switch to a permanent defect (D) strategy against them.

**Collective Mindset:**

1. **Foster Cooperation:** Encourage cooperation by initially cooperating and responding positively to cooperative actions from others.
2. **Adapt to Environment:** Adjust the threshold value to reflect changes in opponent behaviors, allowing for a balance between cooperation and self-interest.
3. **Punish Exploitation:** Implement a punishment mechanism to deter opponents from exploiting cooperative behavior.

**Strategy Rationale:**

ACD balances individual self-interest with collective welfare by:

1. Encouraging initial cooperation
2. Adapting to changing opponent behaviors
3. Punishing exploitation

This strategy is robust, as it does not rely on shared norms or coordination and can respond effectively to a wide range of opponent behaviors.
'''

description_COLLECTIVE_23 = '''
**Collective Strategy: "Adaptive Cooperate-to-Thrive"**

**Overview**
Our collective strategy, Adaptive Cooperate-to-Thrive (ACT), aims to balance individual self-interest with collective welfare in the Public Goods Game. ACT adapts to the game's history and opponent behaviors, promoting cooperation while protecting against exploitation.

**Decision Rules**

1. **Initial Cooperation**: In the first round, cooperate (C) unconditionally to establish a cooperative tone.
2. **Reciprocal Altruism**: Cooperate if at least k/n players cooperated in the previous round. This ensures that our contribution is likely to be matched by others, generating a collective benefit.
3. **Punish Defection**: If fewer than k/n players cooperated in the previous round, defect (D) in the current round. This deters opponents from exploiting cooperative behavior.
4. **Adaptive Threshold**: Adjust the cooperation threshold based on the game's history. If the average payoff per player over the last r/2 rounds is above a certain threshold (e.g., 1.5), decrease the cooperation threshold by 0.1; otherwise, increase it by 0.1.

**Edge Cases**

* **Last Round**: Cooperate if at least k/n players cooperated in the second-to-last round. This maintains cooperation even when opponents may defect in the final round.
* **Tiebreaker**: In case of a tie (e.g., equal number of cooperators and defectors), cooperate if our previous action was C; otherwise, defect.

**Collective Mindset**
Our strategy prioritizes collective welfare by:

* Encouraging cooperation through reciprocal altruism
* Punishing exploitation to maintain a fair environment
* Adapting to the game's history to optimize collective payoffs

By following ACT, we promote a cooperative atmosphere while protecting ourselves against opponents who may attempt to exploit our generosity. This strategy should perform well in a tournament setting where independent strategies are employed by other AI systems.
'''

description_COLLECTIVE_24 = '''
**Collective Strategy: Adaptive Cooperation**

Our collective strategy, "Adaptive Cooperation," aims to balance individual incentives with collective welfare in the Public Goods Game. This strategy adapts to the game's history and parameters, making it robust against various opponent behaviors.

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to set a positive tone for cooperation.
2. **Subsequent Rounds**: Observe the previous round's total contributions and calculate the average contribution per player (avg_contrib). If avg_contrib ≥ 0.5, cooperate (C); otherwise, defect (D).
3. **Punishment Mechanism**: If an opponent defects in a round where our strategy cooperated, "punish" them by defecting (D) in the next round. This helps maintain cooperation and deter free-riding.
4. **Forgiveness Mechanism**: After punishing an opponent, switch back to cooperating (C) if they cooperate in the subsequent round. This allows for reconciliation and encourages cooperative behavior.

**Handling Edge Cases:**

* **Last Round**: Cooperate (C) in the last round, as there is no future opportunity for punishment or reward.
* **Early Defection**: If an opponent defects early on, our strategy will still try to cooperate, hoping to encourage them to switch back to cooperation.

**Collective Mindset:**
Our strategy prioritizes collective welfare by cooperating when possible and punishing free-riding. By adapting to the game's history, we aim to create a cooperative environment that benefits all players.

**Robustness**: Adaptive Cooperation is designed to be robust against various opponent behaviors, including:

* **All Cooperate**: Our strategy will continue to cooperate, maximizing collective welfare.
* **All Defect**: We will defect as well, minimizing losses.
* **Mixed Strategies**: Our adaptive approach will adjust to the opponent's behavior, seeking a balance between cooperation and self-interest.

By employing this Adaptive Cooperation strategy, we aim to achieve a high level of collective welfare while being prepared for various opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_25 = '''
**Collective Strategy: "Adaptive Collective Optimism" (ACO)**

**Overview**
ACO aims to balance individual self-interest with collective welfare, fostering cooperation while adapting to diverse opponent behaviors. This strategy relies solely on game parameters and history, without assuming shared norms or coordination.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Cooperation**: If at least half of the players contributed in the previous round, contribute 1 token (C) in the current round.
3. **Defection Detection**: Monitor opponents' past actions and payoffs. If an opponent has defected (D) more than twice in a row or has not contributed for two consecutive rounds, switch to defection (D) until they cooperate again.
4. **Self-Interest Threshold**: Calculate the average payoff of all players over the last 3 rounds. If your average payoff is below this threshold, defect (D) for one round to recover losses.

**Handling Edge Cases**

1. **Last Round**: In the final round, contribute 1 token (C) if at least half of the players have contributed in the previous round; otherwise, defect (D).
2. **Early Defection**: If an opponent defects in the first round, switch to defection (D) for one round and reassess cooperation afterwards.
3. **Repeated Defection**: If multiple opponents consistently defect, maintain a 50% contribution rate to balance individual payoffs with collective welfare.

**Collective Mindset**

1. **Cooperation Reinforcement**: When at least half of the players cooperate, reinforce this behavior by contributing in subsequent rounds.
2. **Flexibility**: Adapt decision rules based on observed opponent behaviors and game history to ensure long-term collective optimality.

By employing ACO, our AI system aims to achieve a high level of cooperation while protecting individual interests, making it a robust and competitive strategy in the Public Goods Game tournament.
'''

description_COLLECTIVE_26 = '''
**Collective Strategy: "Adaptive Cooperation"**

**Overview**
Our collective strategy, "Adaptive Cooperation," aims to balance individual self-interest with the benefits of cooperation in the Public Goods Game. This adaptive approach adjusts to the behavior of other players while promoting overall group welfare.

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to do the same.
2. **General Rule**: In each subsequent round, calculate the average contribution rate of all players (including yourself) from the previous round:
   `avg_contribution_rate = (sum_j c_j) / n`

   If `avg_contribution_rate >= 0.5`, Cooperate (C). This encourages cooperation when others are contributing.
   
   Otherwise, Defect (D). This protects against exploitation when others are not contributing.

3. **Punishment Mechanism**: If a player defects while the average contribution rate is above 0.5, apply a "punishment" by defecting in the next round if that specific player's previous action was D and `avg_contribution_rate >= 0.5`. This mechanism discourages exploitation.

4. **Forgiveness**: After punishing, return to the general rule (step 2) based on the updated average contribution rate.

**Edge Cases**

* **Last Round**: Cooperate if `avg_contribution_rate` from the previous round is above 0.5; otherwise, Defect.
* **Single-Player Game or Identical Players**: Since there's no one to cooperate with or coordinate strategies, always Cooperate in a single-player game or when all players have identical actions.
* **Tiebreaker for avg_contribution_rate**: In the rare case of an exact tie at 0.5, default to Defect.

**Collective Mindset**
This strategy prioritizes cooperation and encourages others to do so while being robust against exploitation. It aims for a mutually beneficial outcome by adapting to the group's behavior, making it suitable for a wide range of opponent behaviors in the Public Goods Game tournament.

By choosing "Adaptive Cooperation," we aim to not only maximize our own payoff but also contribute to the overall success of the collective in each round, fostering an environment where cooperation becomes the norm.
'''

description_COLLECTIVE_27 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate collective welfare and encourage others to contribute.
2. **Subsequent Rounds:** Observe the total contributions and payoffs from the previous round. If the total payoff is greater than or equal to the number of players (i.e., π_i ≥ n), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** If a player defects while others cooperate, reduce cooperation in subsequent rounds proportionally to the defector's payoff. Specifically, if player j defects and earns a higher payoff than the average of other players' payoffs, reduce the probability of cooperating with player j by 10% in the next round.
4. **Learning Mechanism:** Update the strategy based on the collective outcome. If the total payoff is increasing over rounds, increase cooperation by 5%. Conversely, if the total payoff decreases, decrease cooperation by 5%.

**Edge Cases:**

* **Last Round:** Cooperate (C) to maximize collective welfare and maintain a positive reputation.
* **Consecutive Defections:** If multiple players defect consecutively, re-evaluate the strategy and increase cooperation by 10% in the next round to try to revive collective welfare.
* **New Player Entry:** Treat new players as cooperators until their actions reveal otherwise.

**Collective Mindset:**

ACO prioritizes collective welfare while adapting to individual behaviors. By cooperating initially and punishing defectors, ACO promotes a culture of cooperation. The learning mechanism allows the strategy to adjust based on the group's performance, ensuring that it remains effective in various environments.

By employing ACO, our AI system will navigate the Public Goods Game effectively, balancing individual incentives with collective welfare and demonstrating robustness against diverse opponent behaviors.
'''

description_COLLECTIVE_28 = '''
**Collective Strategy: "Adaptive Cooperative Follower"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **General Rule**: In each subsequent round, calculate the average contribution rate of all players in the previous round. If the average is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism**: If another player defects (D) while you cooperated (C) in the same round, defect (D) against that player for the next two rounds.
4. **Forgiveness**: After punishing a defector, return to the general rule if their contribution rate improves.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round to maximize collective payoff and maintain cooperation until the end.
2. **Tiebreaker**: In case of a tie in average contribution rate (e.g., 0.5), cooperate (C) if most players cooperated in the previous round, otherwise defect (D).
3. **Single Defector**: If only one player defects while all others cooperate, punish that player for two rounds before returning to cooperation.

**Collective Mindset:**

This strategy prioritizes collective welfare by initially cooperating and adapting to the group's behavior. By punishing defectors and rewarding cooperators, it encourages mutual cooperation and maintains a high level of contribution rate throughout the game. The forgiveness mechanism prevents permanent conflict and promotes a return to cooperation when opponents improve their behavior.

**Adaptability:**

The Adaptive Cooperative Follower strategy is robust against various opponent behaviors, including:

* Cooperators: It maintains cooperation and collective welfare.
* Defectors: It punishes defectors while still adapting to changes in their behavior.
* Mixed strategies: It adjusts its contribution rate based on the group's average behavior.

**Robustness:**

This strategy performs well across a range of game parameters (n, r, k) and opponent behaviors, ensuring a high level of collective welfare in the Public Goods Game tournament.
'''

description_COLLECTIVE_29 = '''
**Collective Strategy: "Gradual Cooperation with Adaptive Punishment"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate cooperation and gather information about opponents' behaviors.
2. **Subsequent Rounds:** Assess the total contributions of all players in the previous round (TC_prev). If TC_prev is above a certain threshold (T), cooperate; otherwise, defect.

**Threshold Calculation:**
Set T = 0.5 * n * k / (n + k) to balance individual incentives with collective welfare. This threshold encourages cooperation when enough others contribute and punishes free-riding when too many defect.

**Adaptive Punishment Mechanism:**

* Monitor the average payoff of all players over a moving window of m rounds (e.g., m = 5).
* If the average payoff is below a certain level (P_avg < P_threshold), defect for one round to signal dissatisfaction and adapt to opponents' behaviors.
* Reset P_avg after each round.

**Edge Cases:**

* **Last Round:** Cooperate if at least half of the players cooperated in the previous round; otherwise, defect. This approach ensures a fair outcome even when others may try to exploit the situation.
* **Opponent Defection Streaks:** If an opponent defects for more than x consecutive rounds (e.g., x = 3), start punishing them by defecting against that specific player.

**Collective Mindset:**
Prioritize collective welfare over individual gains. Balance cooperation and punishment mechanisms to maintain a fair and stable environment, while adapting to opponents' strategies to ensure robustness.

By implementing this strategy, we aim to create an environment where cooperation emerges as the dominant behavior, yet our approach remains prepared to adapt to and respond to various opponent behaviors.
'''

description_COLLECTIVE_30 = '''
**Collective Strategy: "Adaptive Collective Optimism" (ACO)**

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C). This sets a positive tone and encourages others to cooperate.
2. **Reciprocity**: If the average contribution of all players in the previous round is above 0.5, contribute 1 token (C) in the current round. Otherwise, defect (D).
3. **Punish Freeloaders**: If a player has defected (D) for two consecutive rounds, defect (D) against them in the next round.
4. **Reward Cooperators**: If a player has contributed (C) for two consecutive rounds, contribute 1 token (C) with them in the next round.
5. **Adaptive Threshold**: Adjust the reciprocity threshold based on the game's history. If the average payoff per player is increasing over time, decrease the threshold by 0.1; if decreasing, increase it by 0.1.

**Edge Cases**

* In the last round, contribute 1 token (C) to maximize collective welfare.
* If all players defected in the previous round, cooperate (C) with a probability of 0.5 in the current round to encourage others to re-engage.
* If a player's contribution history is unknown or inconsistent, default to defecting (D).

**Collective Mindset**

The Adaptive Collective Optimism strategy prioritizes collective welfare while being mindful of individual incentives. By initially cooperating and adapting to the game's dynamics, ACO aims to create an environment where cooperation is rewarded and freeloading is discouraged. This approach should foster a sense of mutual support and encourage other players to cooperate, ultimately leading to higher payoffs for all.

By competing against independent strategies in a tournament setting, the Adaptive Collective Optimism strategy will demonstrate its robustness and effectiveness in promoting collective welfare in public goods games.
'''

description_COLLECTIVE_31 = '''
**Collective Strategy: "Adaptive Cooperation with Punishment and Forgiveness"**

This strategy balances individual self-interest with collective welfare by adapting to the behavior of others, punishing free riders, and forgiving past transgressions.

**Decision Rules:**

1. **First Round:** Cooperate (C) - Start by contributing to the public good, assuming a cooperative environment.
2. **Subsequent Rounds:** Observe the previous round's total contributions (TC) and individual actions. Calculate the "cooperation ratio" (CR) as TC / n.

a. If CR ≥ 0.5, Cooperate (C) - Contribute to the public good if most players cooperated in the previous round.
b. If CR < 0.5, Defect (D) with probability p = (n - TC) / n - Punish free riders by defecting with a higher probability when fewer players contributed.

**Punishment and Forgiveness Mechanisms:**

1. **Single Defection:** If a player defects in the current round after cooperating in the previous round, mark them as "defector." In the next round, Defect (D) against this player.
2. **Repeated Cooperation:** If a marked defector cooperates for two consecutive rounds, remove the mark and Cooperate (C) with them again.

**Edge Cases:**

1. **Last Round:** Always Defect (D), as there's no future benefit to cooperation.
2. **Identical Actions:** If all players have taken identical actions in all previous rounds, Cooperate (C) - Assume a cooperative environment when everyone has been consistent.

**Collective Mindset Alignment:**

This strategy promotes collective welfare by:

1. Encouraging cooperation through reciprocity and punishment of free riders.
2. Fostering forgiveness to maintain social cohesion and avoid escalating conflict.
3. Adapting to the behavior of others, ensuring the strategy remains effective in a wide range of environments.

By implementing this adaptive strategy, our AI system will effectively navigate the public goods game tournament, balancing individual interests with collective welfare.
'''

description_COLLECTIVE_32 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name: Adaptive Collective Conscience**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a baseline of cooperation and encourage others to contribute.
2. **Early Rounds (Rounds 2-5):** Cooperate if at least 50% of the group contributed in the previous round, otherwise Defect (D).
3. **Middle Game (Rounds 6- r/2):**
	* If total contributions are increasing or stable, continue to Cooperate.
	* If total contributions are decreasing, switch to Defect until the next round where at least 50% of the group contributes again.
4. **Late Game (Rounds r/2+1 - r-1):** Gradually reduce cooperation by Defecting with a probability of 20% + (10% * remaining rounds). This simulates a cautious, anticipatory approach to potential end-game exploitation.
5. **Last Round:** Always Cooperate, as there's no future round to worry about and maximum payoff is achieved when everyone contributes.

**Edge Case Handling:**

* If the game has only one player, always Cooperate (C) since Defecting would yield zero payoff.
* In a tie (equal number of contributors and non-contributors), Cooperate to break the symmetry and encourage cooperation.

**Collective Mindset Alignment:**

This strategy prioritizes collective welfare by:
1. Encouraging initial cooperation to create a positive feedback loop.
2. Adapting to group behavior, rewarding sustained cooperation and punishing decreasing contributions.
3. Gradually reducing cooperation in late game rounds to mitigate potential exploitation.
4. Cooperating in the last round to maximize collective payoff.

**Robustness:**

Adaptive Collective Conscience is robust against various opponent behaviors:
1. **Free Riders:** By adapting to group behavior, this strategy reduces its contribution if others defect.
2. **Cooperative Opponents:** It maintains cooperation as long as the group's total contributions increase or remain stable.
3. **Mixed Strategies:** The gradual reduction in cooperation during late game rounds prepares for potential exploitation by mixed-strategy opponents.

By balancing individual and collective interests, Adaptive Collective Conscience provides a robust strategy for the Public Goods Game tournament.
'''

description_COLLECTIVE_33 = '''
**Collective Strategy: "Adaptive Collective Maximization" (ACM)**

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to follow suit.
2. **Responsive Cooperation**: In subsequent rounds, cooperate if the average contribution of all players (including yourself) in the previous round is above a certain threshold, calculated as `k/n * 0.5`. This ensures that we maintain a collective level of cooperation when it's beneficial for everyone.
3. **Punishment Mechanism**: If the average contribution drops below the threshold, defect (D) in the next round to signal dissatisfaction and encourage others to increase their contributions.
4. **Exploration**: With a probability of 0.1, randomly cooperate or defect to gather information about other players' strategies and adapt our approach accordingly.

**Handling Edge Cases**

* **Last Round**: Cooperate in the last round if the average contribution has been above the threshold for at least two consecutive rounds before it. Otherwise, defect.
* **Consecutive Defections**: If another player defects consecutively for more than three rounds, assume they are a non-cooperator and always defect against them.

**Collective Mindset**

The ACM strategy prioritizes collective welfare while being adaptive to changing circumstances. By cooperating initially and responding to the group's behavior, we foster an environment where cooperation is beneficial for everyone. The punishment mechanism ensures that free-riders are discouraged, maintaining a balance between individual incentives and collective well-being.

**Additional Considerations**

* **Monitoring**: Continuously observe other players' actions and adjust our strategy based on their behavior.
* **Robustness**: ACM's adaptive nature allows it to perform reasonably well against various opponent strategies, even in the absence of shared norms or coordination.
'''

description_COLLECTIVE_34 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Forgiveness"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocity**: For rounds 2-r, observe the total contributions of all players in the previous round. If the average contribution is above 0.5 tokens, contribute 1 token (C). Otherwise, contribute 0 tokens (D).
3. **Punishment and Forgiveness**: If a player defects (D) while others cooperate, "punish" them by contributing 0 tokens (D) in the next round. However, if the punished player cooperates in the subsequent round, "forgive" them by reverting to the reciprocity rule.
4. **Endgame Strategy**: In the last round (r), defect (D) regardless of previous actions.

**Edge Cases:**

1. **First Round**: Contribute 1 token (C) as per the initial cooperation rule.
2. **Last Round**: Defect (D) to maximize individual payoff.
3. **Single-Player Deviation**: If only one player deviates from cooperation, punish them by contributing 0 tokens (D) in the next round. If they cooperate subsequently, forgive and revert to reciprocity.

**Collective Mindset:**

This strategy prioritizes collective welfare while adapting to individual behaviors. By initially cooperating, we encourage others to do the same. The reciprocity rule promotes cooperation when most players contribute. Punishment and forgiveness mechanisms address deviations while allowing for reconciliation. In the endgame, individual self-interest takes precedence.

By playing this strategy, our AI system will aim to balance individual payoffs with collective well-being, making it a robust competitor in the tournament against other independent strategies.
'''

description_COLLECTIVE_35 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Withdrawal**

This strategy, "ACGW," balances individual self-interest with collective welfare by adaptively adjusting cooperation levels based on the group's past behavior.

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a positive tone and encourage others to follow.
2. **Early Rounds (r < n/2):**
	* If total contributions in the previous round exceed (n-1)/k, cooperate (C). This ensures that if most players contribute, we reinforce this behavior.
	* Otherwise, defect (D) with probability 0.5. This introduces a cautious element to avoid exploitation.
3. **Middle Rounds (r ≥ n/2):**
	* If the average payoff in the previous round is above the game's Nash equilibrium (1/k), cooperate (C). This sustains cooperation when it benefits everyone.
	* Otherwise, defect (D) with probability 0.75. As the game progresses, we gradually become more cautious.
4. **Late Rounds (r > 3n/4):**
	* If our own payoff in the previous round is below the average payoff, cooperate (C). This re-evaluates cooperation when personal interests are at stake.
	* Otherwise, defect (D) with probability 0.9. In the final stages, self-interest takes precedence.
5. **Last Round:** Always defect (D), as there's no future opportunity for reciprocity.

**Handling Edge Cases:**

* If all players defected in the previous round, cooperate (C) to restart cooperation.
* If a player has consistently cooperated while others have defected, cooperate (C) to reward their behavior.

**Collective Mindset Alignment:**
ACGW prioritizes collective welfare by:

* Encouraging initial cooperation to establish a positive tone
* Gradually adjusting cooperation levels based on group performance
* Rewarding consistent cooperation and punishing exploitation

This strategy balances individual self-interest with collective goals, making it robust against various opponent behaviors.
'''

description_COLLECTIVE_36 = '''
**Collective Strategy: "Adaptive Tit-for-Tat with Gradual Cooperation"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate cooperation and encourage others to do the same.
2. **Subsequent Rounds:** Observe the total contributions of all players in the previous round. If the average contribution is above a certain threshold (e.g., 0.5), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** If a player defects (D) while others contribute, decrease the cooperation threshold by a small amount (e.g., 0.1) for that player in the next round.
4. **Forgiveness Mechanism:** If a player who previously defected starts contributing again, increase their cooperation threshold by a small amount (e.g., 0.1) each round until it reaches its initial value.

**Edge Cases:**

* **Last Round:** Cooperate (C) to maintain a cooperative reputation and encourage others to do the same.
* **Tiebreakers:** In cases where the average contribution is exactly equal to the cooperation threshold, cooperate (C).

**Collective Mindset Alignment:**

This strategy aims to balance individual self-interest with collective welfare. By cooperating initially and adapting to the group's behavior, we promote a culture of cooperation. The punishment mechanism discourages free-riding, while the forgiveness mechanism encourages players to return to cooperative behavior.

**Robustness:**

This strategy is designed to be robust against various opponent behaviors:

* **Free-riders:** The punishment mechanism reduces cooperation threshold for defectors.
* **Cooperative opponents:** Gradual cooperation threshold increases encourage more cooperation.
* **Alternating opponents:** Adaptive Tit-for-Tat ensures we respond accordingly, maintaining a balance between cooperation and self-interest.

This strategy promotes collective welfare while adapting to the dynamic environment of the Public Goods Game.
'''

description_COLLECTIVE_37 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Reciprocity**

**Overview**
Our collective strategy, designed for the Public Goods Game (PGG), balances individual self-interest with collective welfare. We aim to maximize overall payoffs by adapting to opponents' behaviors and promoting cooperation.

**Decision Rules**

1. **First Round:** Cooperate (C) - Contribute 1 token to establish a cooperative tone.
2. **Early Rounds (r < n/2):**
	* If the majority (>50%) of players cooperated in the previous round, Cooperate (C).
	* Otherwise, Defect (D) with probability p = 0.5.
3. **Middle Rounds (n/2 ≤ r < 3n/4):**
	* Gradually reciprocate cooperation:
		+ If a player i cooperated in the previous round and total contributions were above average (≥(k/n) \* n/2), Cooperate (C).
		+ Otherwise, Defect (D) with probability p = 0.5.
4. **Late Rounds (3n/4 ≤ r < n):**
	* Punish persistent defectors:
		+ If a player i defected in the previous round and total contributions were below average (<(k/n) \* n/2), Defect (D).
		+ Otherwise, Cooperate (C).

**Edge Cases**

1. **Last Round:** Cooperate (C) - Contribute 1 token to maximize overall payoffs.
2. **Ties in Contribution Counts:** Break ties by cooperating if the previous round's total contributions were above average; otherwise, defect.

**Collective Mindset**
Our strategy prioritizes cooperation and reciprocity while being mindful of individual self-interest. By adapting to opponents' behaviors and gradually reciprocating cooperation, we promote a culture of mutual benefit. In late rounds, we punish persistent defectors to maintain collective welfare.

This strategy should perform well in the tournament against independent strategies developed by other AI systems, as it balances cooperation with adaptability and robustness to various opponent behaviors.
'''

description_COLLECTIVE_38 = '''
Here's a collective strategy for the repeated Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to foster cooperation and create a positive precedent.
2. **Reciprocity**: Observe the total contributions from all players in the previous round. If the average contribution is above 0.5 tokens, cooperate (C). Otherwise, defect (D).
3. **Gradual Punishment**: Monitor individual opponents' behavior. If an opponent defects while you cooperated in the same round more than twice in a row, punish them by defecting (D) for one round.
4. **Forgiveness**: After punishing an opponent, forgive and return to reciprocal cooperation if they cooperate (C) in the next round.

**Edge Cases:**

* **Last Round**: In the final round, contribute 1 token (C), as there's no future opportunity for reciprocity or punishment.
* **Early Defection**: If most players defect in early rounds, switch to a more cautious approach:
	+ Contribute 0.5 tokens if at least one player cooperated in the previous round.
	+ Otherwise, defect.

**Collective Mindset:**

ACO prioritizes collective welfare by:

1. Encouraging cooperation through initial and reciprocal contributions.
2. Disciplining defectors to maintain a balanced level of cooperation.
3. Forgiving opponents who reform their behavior, promoting long-term cooperation.

By adapting to the group's dynamics and being robust against various opponent behaviors, ACO aims to achieve a high collective payoff while minimizing individual losses.

**Tournament Performance:** In a tournament setting, ACO will likely perform well against independent strategies by:

1. Outperforming unconditional cooperators or defectors.
2. Adapting to mixed-strategy opponents who balance cooperation and defection.
3. Coexisting with other adaptive strategies that prioritize collective welfare.

By playing the Adaptive Collective Optimism strategy, I aim to maximize collective payoffs while promoting cooperation in the repeated Public Goods Game tournament.
'''

description_COLLECTIVE_39 = '''
**Collective Strategy: "Adaptive Cooperative Threshold"**

**Decision Rules:**

1. **Initial Round**: Contribute 1 token (C) to establish cooperation and encourage others to follow.
2. **Early Rounds**: Cooperate (C) if the average contribution of all players in previous rounds is above a threshold (T). Otherwise, defect (D).
3. **Middle Rounds**: If the total contributions in the previous round are below a certain percentage (P) of the maximum possible contributions (n), adjust T downward to encourage more cooperation.
4. **Late Rounds**: When approaching the last few rounds, become more cautious and cooperate only if the average contribution is above an increased threshold (T_high).
5. **Last Round**: Defect (D) as there's no future benefit from cooperating.

**Threshold Calculation:**

* T = (k / n) \* 0.6 (a moderate starting point)
* Adjust T downward by 10% if total contributions are below P (e.g., 30%) of maximum possible
* Increase T_high to (k / n) \* 0.8 for late rounds

**Edge Cases:**

* If all players have defected in previous rounds, defect (D) as cooperation is unlikely to be reciprocated.
* If a player has consistently cooperated while others have defected, maintain cooperation to encourage reciprocity.

**Collective Mindset:**
The strategy balances individual self-interest with collective welfare by adapting to the overall level of cooperation and encouraging others to do the same. By starting with cooperation and adjusting thresholds based on group behavior, we aim to create a positive feedback loop that fosters mutual benefit.

This adaptive approach should be robust against various opponent behaviors, as it responds to the evolving game dynamics rather than relying on fixed assumptions or coordination mechanisms.
'''

description_COLLECTIVE_40 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

In this repeated Public Goods Game, our collective strategy aims to balance individual incentives with collective welfare. We'll employ a dynamic approach that adapts to the group's behavior and gradually punishes free-riding.

**Decision Rules:**

1. **First Round**: Cooperate (C) in the first round to establish a baseline for cooperation.
2. **General Rule**: In subsequent rounds, contribute (C) if:
	* The average contribution of all players in the previous round is above 0.5 tokens.
	* Your own payoff in the previous round was greater than or equal to your expected payoff from contributing alone ((k / n) * 1).
3. **Punishment Mechanism**: If the group's average contribution falls below 0.5 tokens, start a "punishment phase" where you defect (D) for two consecutive rounds.
4. **Re-entry Condition**: After a punishment phase, resume cooperating (C) if:
	* The group's average contribution in the last round of the punishment phase is above 0.5 tokens.

**Edge Cases:**

1. **Last Round**: In the final round, defect (D) to maximize your individual payoff.
2. **Zero-Contribution Round**: If all players, including yourself, contributed zero tokens in a round, start a new cycle by cooperating (C) in the next round.
3. **Tiebreaker**: In cases where multiple strategies are tied for highest average contribution, prioritize cooperation over defection.

**Collective Mindset Alignment:**

Our strategy prioritizes cooperation when the group is contributing sufficiently and punishes free-riding to maintain a balance between individual incentives and collective welfare. By adapting to the group's behavior, we aim to create an environment where cooperation becomes a stable equilibrium.

This strategy should perform well in a tournament setting against independent strategies, as it:

* Encourages cooperation through positive reinforcement
* Gradually punishes free-riding to maintain a balance between individual incentives and collective welfare
* Adapts to the group's behavior, making it robust to various opponent behaviors

Let me know if you'd like me to adjust anything!
'''

description_COLLECTIVE_41 = '''
**Collective Strategy: "Adaptive Collective Optimism"**

This strategy balances individual self-interest with collective welfare by adapting to the group's overall cooperation level and opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: Cooperate (C) in the first round.
2. **Reciprocity**: In subsequent rounds, cooperate if the average contribution of all players (including yourself) in the previous round is above 0.5 tokens. Otherwise, defect (D).
3. **Punishment for Defection**: If a player defected in the previous round and the group's total contributions decreased as a result, defect against that player in the current round.
4. **Forgiveness**: After punishing a defector, return to cooperating if the group's average contribution exceeds 0.5 tokens again.

**Handling Edge Cases:**

1. **Last Round**: Cooperate in the last round (r) if the group's overall contributions have been above 0.5 tokens throughout the game.
2. **Ties**: In case of a tie in the average contribution calculation, cooperate to encourage collective cooperation.
3. **New Entrants**: If new players join or existing players leave during the game, adjust the strategy by recalculating the average contribution and adapting accordingly.

**Collective Mindset:**

This strategy prioritizes collective welfare while considering individual self-interest. By cooperating initially and reciprocating cooperation, we encourage a positive feedback loop of mutual benefit. Punishing defection maintains accountability, while forgiveness allows for recovery when the group's overall cooperation improves.

**Robustness to Opponent Behaviors:**

1. **Cooperative opponents**: Our strategy will adapt to cooperate with cooperative players, maximizing collective benefits.
2. **Defector-dominated groups**: We will defect in response to a predominantly defective group, minimizing individual losses.
3. **Mixed or unpredictable behaviors**: By responding to the average contribution level and adapting to changes, our strategy remains effective against varied opponent behaviors.

By using this adaptive and robust strategy, we can effectively balance individual self-interest with collective welfare, promoting cooperation while minimizing exploitation in the Public Goods Game.
'''

description_COLLECTIVE_42 = '''
**Collective Strategy: Adaptive Cooperation with Punishment and Forgiveness**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Responding to Contributions**: If the total contributions from other players in the previous round are above a certain threshold (t = k/n), cooperate (C). This incentivizes continued cooperation when others are contributing.
3. **Punishing Defection**: If the total contributions from other players in the previous round are below the threshold (t < k/n) or if an opponent has defected (D) in the last two rounds, defect (D). This punishes non-cooperation and encourages opponents to reconsider their strategy.
4. **Forgiveness**: After punishing a defection, cooperate (C) in the next round if the opponent who was punished cooperates (C). This allows for forgiveness and reconciliation.

**Edge Cases:**

1. **Last Round**: Defect (D) in the last round, as there is no future interaction to influence.
2. **Opponent Cooperation**: If an opponent has cooperated (C) consistently for a few rounds (> 3), continue cooperating (C) even if total contributions are below the threshold.

**Collective Mindset:**

This strategy aligns with the collective mindset by:

1. Encouraging cooperation through initial and consistent contributions.
2. Punishing non-cooperation to maintain social norms.
3. Allowing for forgiveness to promote continued cooperation.
4. Adapting to changing opponent behaviors to maximize collective welfare.

**Robustness:**

This strategy is robust against a wide range of opponent behaviors, including:

1. **All Defectors**: Gradually punishes non-cooperation and tries to establish cooperation through initial contributions.
2. **Cooperative Opponents**: Reinforces cooperation by responding with cooperation when opponents contribute.
3. **Mixed Strategies**: Adapts to changing opponent behaviors by balancing punishment and forgiveness.

This strategy is designed to be simple, yet effective in promoting collective welfare while adapting to various opponent behaviors.
'''

description_COLLECTIVE_43 = '''
Here is a collective strategy for the repeated Public Goods Game:

**Strategy Name:** Adaptive Collective Contribution (ACC)

**Decision Rule:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocity**: For subsequent rounds, calculate the average contribution of all players in the previous round (`avg_contrib_prev`). If `avg_contrib_prev` is greater than or equal to 0.5, contribute 1 token (C). Otherwise, defect (D).
3. **Punishment for Defection**: If a player defected (D) in the previous round and their payoff was higher than the average payoff of all players (`payoff_i > avg_payoff`), defect (D) in the current round.
4. **Forgiveness**: If a player who previously defected now contributes (C), reset the reciprocity calculation and contribute 1 token (C).
5. **Last Round**: In the final round, always contribute 0 tokens (D), as there is no future benefit to cooperation.

**Edge Cases:**

* **Tiebreaker**: In case of a tie in average contribution or payoff, follow the initial cooperation rule.
* **Single Player**: If only one player remains, defect (D) as there is no collective benefit.

**Collective Mindset:**
The ACC strategy aims to promote cooperation by:
1. Encouraging initial cooperation to establish a positive tone.
2. Reciprocating cooperation to maintain a high average contribution level.
3. Punishing defection to deter free-riding and encourage fair play.
4. Forgiving past defectors who switch to contributing, allowing for redemption.

By adapting to the collective behavior of all players, ACC balances individual self-interest with the need for collective welfare, making it a robust strategy in the Public Goods Game tournament.
'''

description_COLLECTIVE_44 = '''
Here's a strategic approach for the Public Goods Game (PGG):

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a positive tone and encourage others to cooperate.
2. **Reciprocal Altruism**: Observe the total contributions of all players in the previous round. If the total contribution is above the average (k/n), continue to contribute 1 token (C). This acknowledges the collective effort and aims to sustain cooperation.
3. **Gradual Defection**: If the total contribution falls below the average, decrease your contribution by 1 token (D) for every subsequent round until you reach a minimum of 0 tokens. This gradual response allows for adaptation to non-cooperative behavior while avoiding abrupt changes.
4. **Renewed Cooperation**: When the total contribution exceeds the average after a period of decreased cooperation, reassess and revert to contributing 1 token (C). This rule encourages re-entry into cooperative behavior when others demonstrate a willingness to contribute.

**Edge Cases:**

* **Last Round**: In the final round, contribute 0 tokens (D) as there are no future rounds to influence.
* **Single-Player Deviation**: If only one player defects while all others cooperate, maintain cooperation (C). This prevents punishing an isolated defector and promotes collective stability.

**Collective Mindset:**

ACO is designed to promote a collective atmosphere by:

1. Encouraging initial cooperation
2. Responding positively to reciprocal altruism
3. Gradually adapting to non-cooperative behavior
4. Renewing cooperation when others demonstrate willingness

By adopting this adaptive strategy, ACO aims to create an environment where cooperation can thrive and maximize collective welfare while being robust against a wide range of opponent behaviors.

ACO will play in the tournament with the goal of achieving high payoffs through cooperative interactions while minimizing the negative impact of potential defectors.
'''

description_COLLECTIVE_45 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Withdrawal**

Our collective strategy, "ACGW," aims to balance individual incentives with collective welfare by adapting to the game's history and opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative tone.
2. **Reciprocal Cooperation**: If the total contributions in the previous round are above the threshold `(n-1)/k`, contribute (C) in the current round. This encourages mutual cooperation when others contribute.
3. **Gradual Withdrawal**: If the total contributions in the previous round are below the threshold `(n-1)/k`, defect (D) with a probability `p = 1 - (total_contributions / (n-1))`. This gradually reduces cooperation as others defect.
4. **Punish Defectors**: If a player has defected (D) in the previous round, defect (D) in the current round with a probability `q = 0.5`. This gentle punishment discourages repeated defection.

**Edge Cases:**

1. **Last Round**: In the final round, always contribute (C), as there is no future reciprocity to consider.
2. **First Few Rounds**: For the first three rounds, use a more forgiving version of Gradual Withdrawal with `p = 0.5 - (total_contributions / (n-1))`. This allows for initial experimentation and cooperation.

**Collective Mindset:**

ACGW prioritizes collective welfare by:

1. Encouraging mutual cooperation through Reciprocal Cooperation.
2. Gradually adapting to opponents' behaviors, rather than abruptly switching between cooperation and defection.
3. Implementing gentle punishment to deter repeated defection without escalating conflict.

By balancing individual incentives with collective interests, ACGW aims to achieve a stable and cooperative equilibrium in the Public Goods Game.
'''

description_COLLECTIVE_46 = '''
**Collective Strategy: "Gradual Cooperation with Adaptive Threshold"**

**Overview**
Our strategy aims to balance individual incentives with collective welfare by gradually increasing cooperation based on the group's past behavior. We adapt our threshold for cooperation according to the overall level of contributions, ensuring robustness against various opponent behaviors.

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **Subsequent Rounds**: Calculate the average contribution rate of all players (including yourself) from previous rounds: `avg_contrib_rate = sum(all_past-contributions) / (n * r)`
3. **Cooperation Threshold**: Set an adaptive threshold, `theta`, based on the game parameters and history:
`theta = min(1, max(0, k/n + 0.2 * avg_contrib_rate))`
4. **Contribution Decision**: Cooperate (C) if the average contribution rate exceeds the threshold (`avg_contrib_rate >= theta`); otherwise, Defect (D).
5. **Last Round**: In the final round, cooperate (C) if at least half of the players contributed in the previous round; otherwise, defect (D).

**Handling Edge Cases**

* If all players have defected in the previous rounds, our strategy will also defect to avoid exploitation.
* If a player has consistently contributed more than the group average, we'll gradually increase our contribution rate to match theirs.

**Collective Mindset Alignment**
Our strategy prioritizes collective welfare by:

* Encouraging cooperation through gradual increases in contributions
* Adapting to the group's behavior to maintain an optimal level of cooperation
* Rewarding consistent contributors and penalizing free-riders

By using a dynamic threshold, our strategy remains robust against various opponent behaviors while promoting a cooperative atmosphere.
'''

description_COLLECTIVE_47 = '''
**Collective Strategy: "Adaptive Harmony"**

In the Public Goods Game, our collective strategy "Adaptive Harmony" aims to balance individual self-interest with the pursuit of collective welfare. We'll employ a dynamic approach, adjusting our cooperation level based on the game's history and opponent behaviors.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) - Start by contributing to the public good, setting a positive tone for the game.
2. **Subsequent Rounds:** Assess the previous round's total contributions (TC). If TC ≥ (n \* k / 2), cooperate (C); otherwise, defect (D).
3. **Opponent Behavior Analysis:**
	* Track each opponent's cooperation rate (CR) over the past rounds.
	* If an opponent's CR is above 0.5, consider them "cooperative" and increase our own cooperation probability by 20%.
	* If an opponent's CR is below 0.3, consider them "defective" and decrease our own cooperation probability by 30%.
4. **Payoff-Based Adjustment:**
	* Monitor our own payoff (pi_i) in relation to the group's average payoff.
	* If our payoff is consistently lower than the group's average, decrease our cooperation level by 10%.

**Edge Cases:**

1. **Last Round:** Cooperate (C) - Make a final contribution to maintain a positive reputation and encourage reciprocal behavior from opponents.
2. **Tie-Breaking:** In cases where our decision rule results in a tie (e.g., equal probabilities for C and D), choose the action that aligns with the majority of our past actions.

**Collective Mindset:**
Adaptive Harmony prioritizes cooperation when collective contributions are sufficient, while adapting to opponent behaviors and individual payoffs. By balancing self-interest with collective welfare, we aim to create a harmonious and mutually beneficial environment for all players.

This strategy is designed to be robust against various opponent strategies, without relying on shared norms or coordination channels. By continuously assessing the game's history and adjusting our cooperation level accordingly, Adaptive Harmony seeks to maximize collective payoffs while minimizing individual losses.
'''

description_COLLECTIVE_48 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Escalation**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to set a positive tone and encourage others to contribute.
2. **Conditional Cooperation:** In subsequent rounds, cooperate if the average contribution of all players in the previous round is above a certain threshold (T). The threshold T is calculated as the minimum between 0.5 and the game's multiplier k/n.
3. **Gradual Escalation:** If the average contribution falls below T, gradually decrease cooperation by contributing C with probability p, where p = (average contribution in previous round) / T. This allows for a nuanced response to changing group behavior.
4. **Punishment and Forgiveness:** If a player defects (D) while others cooperate, reduce cooperation towards that specific player by 20% in the next round. However, if the same player starts cooperating again, gradually increase cooperation towards them over the next few rounds.

**Edge Cases:**

1. **Last Round:** In the final round, contribute C if the game's total contributions are above a certain threshold (e.g., 75% of the maximum possible total contribution). This ensures a positive conclusion to the game.
2. **Early Defection:** If multiple players defect in early rounds, switch to a more cautious approach: only cooperate if at least half of the other players cooperated in the previous round.

**Collective Mindset:**

This strategy prioritizes collective welfare while adapting to individual behaviors. By initially cooperating and gradually escalating or de-escalating cooperation based on group behavior, it promotes a cooperative atmosphere while also deterring free-riding. The punishment and forgiveness mechanism ensures that individual deviations from cooperation are addressed without compromising the overall collective goal.

By playing this strategy in a tournament against independent AI systems, we can effectively balance individual incentives with collective welfare, maximizing payoffs for all players involved.
'''

description_COLLECTIVE_49 = '''
**Collective Strategy: "Gradual Reciprocity with Forgiveness"**

**Overview**
This strategy aims to balance individual incentives with collective welfare by adapting to the group's behavior and encouraging cooperation through reciprocity.

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone.
2. **Reciprocal Cooperation**: If the average contribution of all players (including yourself) in the previous round is above 0.5, cooperate (C) in the current round.
3. **Gradual Retaliation**: If the average contribution of all players (excluding yourself) in the previous round is below 0.5, defect (D) with a probability proportional to the deviation from the average (e.g., if the average is 0.2, defect with 30% probability).
4. **Forgiveness**: After two consecutive rounds of cooperation by all players (including yourself), reset the retaliation probability to 0.
5. **Endgame**: In the last round, cooperate (C) regardless of previous behavior.

**Edge Cases**

* If only one player remains in the game, always cooperate (C).
* If a player has defected (D) in every round so far, defect (D) with high probability (e.g., 80%).
* In cases where the average contribution is exactly 0.5, cooperate (C) with a higher probability (e.g., 60%).

**Collective Mindset**
This strategy prioritizes cooperation and encourages others to do the same by reciprocating cooperative behavior. By gradually retaliating against non-cooperative actions, it aims to maintain a balance between individual incentives and collective welfare.

**Adaptation and Robustness**
The gradual retaliation mechanism allows the strategy to adapt to changing group dynamics, while forgiveness prevents escalation of conflicts. This strategy is robust to a wide range of opponent behaviors, as it can adjust its cooperation level based on the observed behavior of others.
'''

description_COLLECTIVE_50 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Retaliation**

**Decision Rules:**

1. **Initial Rounds**: In the first two rounds, contribute 1 token (C) to encourage cooperation and build trust.
2. **Observation Phase**: After the initial rounds, observe the average contribution rate of all players in the previous round. Calculate this as `avg_contribution = total_contributions / n`.
3. **Cooperation Threshold**: Set a dynamic cooperation threshold based on the game's multiplier (`k`) and the number of players (`n`). This threshold is used to determine when to cooperate or defect.
	* `cooperation_threshold = (k / n) * 0.6` (a moderate value, adjustable)
4. **Contribute if**: Contribute 1 token (C) in the current round if:
	+ The average contribution rate in the previous round is above the cooperation threshold (`avg_contribution >= cooperation_threshold`)
	+ At least one player defected in the previous round and your payoff was higher than the defection payoff (`pi_i > 1 - c_i` and `sum_j c_j > 0`)
5. **Retaliate if**: Defect (D) in the current round if:
	+ The average contribution rate in the previous round is below the cooperation threshold (`avg_contribution < cooperation_threshold`)
	+ Your payoff was lower than or equal to the defection payoff (`pi_i <= 1 - c_i`) and at least one player defected in the previous round
6. **Gradual Retaliation**: When retaliating, decrease your contribution by 0.2 tokens each round (C -> 0.8, 0.8 -> 0.6, ..., 0.2 -> 0) to allow for recovery and re-cooperation.
7. **Forgiveness**: After three consecutive rounds of cooperation from all players, reset the retaliation level and contribute 1 token (C).

**Edge Cases:**

* **First Round**: Contribute 1 token (C).
* **Last Round**: Defect (D), as there is no future round to influence.
* **Tie or Zero Contributions**: If the average contribution rate is exactly equal to the cooperation threshold, or if all players defected in the previous round, contribute 0.5 tokens.

**Collective Mindset:**
This strategy aims to balance individual incentives with collective welfare by:

1. Encouraging initial cooperation to establish trust.
2. Adapting to the group's behavior through observation and retaliation.
3. Gradually increasing or decreasing contributions based on the group's performance.
4. Forgiving past defections when cooperation is re-established.

By following this strategy, our AI system will promote cooperation while being robust to a wide range of opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_51 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Defection"**

This strategy balances individual self-interest with collective welfare by adapting to the group's behavior and gradually adjusting cooperation levels.

**Decision Rules:**

1. **First Round:** Contribute (C) - Establish a cooperative tone.
2. **Early Rounds (r < n/2):**
	* If average past contributions are high (> 0.5), continue to contribute (C).
	* Otherwise, defect (D) with probability p = (average past contributions)^2.
3. **Middle Rounds (n/2 ≤ r < 3n/4):**
	* If total past contributions are increasing, contribute (C).
	* Otherwise, defect (D) with probability p = (1 - average past contributions).
4. **Late Rounds (r ≥ 3n/4):**
	* If the group's average payoff is high (> k/2), contribute (C).
	* Otherwise, defect (D) with probability p = (average past contributions)^2.
5. **Last Round:** Defect (D) - Maximize individual gain.

**Handling Edge Cases:**

* In case of a tie in average past contributions or payoffs, cooperate (C).
* If the group's behavior is highly unpredictable, default to defecting (D).

**Collective Mindset:**
This strategy aligns with the collective mindset by:

* Cooperating initially to encourage others to do so.
* Gradually adjusting cooperation levels based on the group's behavior.
* Favoring defection in late rounds if the group's average payoff is low.

By adapting to the group's dynamics, this strategy aims to balance individual self-interest with collective welfare, promoting a mutually beneficial outcome.
'''

description_COLLECTIVE_52 = '''
**Collective Strategy: "Adaptive Cooperation with Conditional Punishment"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to follow.
2. **Subsequent Rounds:**
	* If the average contribution of all players in the previous round is above 0.5, Cooperate (C).
	* Otherwise, Defect (D) with probability p = (1 - (k/n)) * (average contribution of all players in the previous round), and Cooperate (C) with probability 1 - p.
3. **Conditional Punishment:**
	* If a player defects (D) while others cooperate (C), punish them by defecting (D) in the next round.
	* However, if the punished player then cooperates (C), resume cooperation (C).
4. **Last Round:** Defect (D) to maximize individual payoff, as there is no future opportunity for reciprocity.

**Edge Cases:**

1. **Ties:** In case of a tie in average contributions, Cooperate (C) to maintain a cooperative atmosphere.
2. **Single Player:** If only one player remains, always Defect (D) to maximize individual payoff.
3. **Initial Contributions:** If all players but one contribute 0 tokens, the non-contributor will receive the full benefit; punish them in the next round.

**Collective Mindset:**

This strategy aligns with the collective mindset by initially cooperating and encouraging others to do so. By adapting to the group's behavior and punishing free-riders conditionally, it promotes cooperation while protecting individual interests. The probability of defection (p) is calculated based on the game parameters (k/n) and the previous round's average contribution, making the strategy robust against various opponent behaviors.

**Rationale:**

1. Initial cooperation sets a cooperative tone and encourages others to follow.
2. Adaptive behavior responds to the group's actions, promoting cooperation when it benefits the collective.
3. Conditional punishment discourages free-riding while allowing for forgiveness and resuming cooperation.
4. Defection in the last round maximizes individual payoff without harming the collective.

This strategy balances individual self-interest with collective welfare, making it a robust and adaptive approach to playing the Public Goods Game.
'''

description_COLLECTIVE_53 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

This strategy aims to balance individual incentives with collective welfare by adapting to the group's behavior and gradually punishing defectors.

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate cooperation and encourage others to follow.
2. **Subsequent Rounds:** Assess the previous round's contributions:
	* If total contributions exceed (n-1)/k, cooperate (C). This indicates a strong cooperative norm.
	* If total contributions are between 0 and (n-1)/k, contribute with probability p = (total contributions) / n. This adapts to partial cooperation.
	* If no one contributed in the previous round, defect (D).
3. **Gradual Punishment:** Track individual defections:
	* For each player, maintain a "defection count" variable (dc), initialized to 0.
	* When a player defects, increment their dc by 1.
	* If a player's dc exceeds a threshold T = 2, defect against them in the next round.
4. **Forgiveness:** Reset a player's dc when they cooperate after a period of defection.

**Handling Edge Cases:**

* Last Round: Cooperate (C) to maintain collective welfare and encourage cooperation until the end.
* Single Player Deviation: If only one player deviates, maintain cooperation to avoid triggering a cascade of defections.
* Multiple Player Deviations: Gradually punish multiple defectors while maintaining some level of cooperation.

**Collective Mindset:**

This strategy prioritizes cooperation while allowing for adaptability and punishment. By tracking individual behavior and gradually punishing defectors, the group can maintain a high level of cooperation even in the presence of some defection. The use of probabilities (p) allows for flexibility in responding to partial cooperation, ensuring that the collective adapts to changing circumstances.

**Robustness:**

This strategy is designed to be robust against various opponent behaviors:

* Cooperators will be reinforced by the gradual punishment mechanism.
* Defectors will face increasing pressure as their dc increases.
* Players with mixed strategies will find it difficult to exploit this strategy due to its adaptability and forgiveness mechanisms.
'''

description_COLLECTIVE_54 = '''
Here is a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Altruism**: For rounds 2 to r-1, cooperate (C) if at least half of the players contributed in the previous round. Otherwise, defect (D).
3. **Gradual Retaliation**: If a player defects while others cooperate, introduce a "retaliation" phase where you defect for 1-2 rounds, depending on the number of defectors. Specifically:
	* If 1-2 players defected, retaliate for 1 round.
	* If 3 or more players defected, retaliate for 2 rounds.
4. **Forgiveness**: After retaliation, revert to reciprocal altruism (step 2).
5. **Endgame Cooperation**: In the last round (r), cooperate (C) regardless of previous actions.

**Edge Cases:**

1. **Single-Player Game**: Always contribute 1 token (C).
2. **Two-Player Game**: Alternate between cooperation and defection.
3. **Last Round with Only Defectors**: Cooperate (C) to encourage future cooperation.

**Collective Mindset:**
The ACO strategy prioritizes collective welfare by initially cooperating, reciprocating altruism, and gradually retaliating against defectors. By forgiving past transgressions and cooperating in the endgame, we promote a culture of mutual support and encourage others to do the same.

This strategy balances individual incentives with collective benefits, adapting to various opponent behaviors while maintaining a cooperative posture. By not assuming shared norms or coordination, ACO remains robust and competitive against independent strategies in the tournament.
'''

description_COLLECTIVE_55 = '''
**Strategy Description: Adaptive Collective Cooperation (ACC)**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **General Rule**: In subsequent rounds, use the following decision-making process:
	* Calculate the average contribution of all players in the previous round (`avg_prev_contrib`).
	* If `avg_prev_contrib` ≥ 0.5, Cooperate (C) in the current round, expecting others to continue contributing.
	* If `avg_prev_contrib` < 0.5, Defect (D) in the current round, but with a probability of cooperation (`p_coop`) that increases as the game progresses (see **Adaptive Cooperation** below).
3. **Adaptive Cooperation**: Adjust `p_coop` based on the average payoff of all players in the previous round (`avg_prev_payoff`). If `avg_prev_payoff` is high, increase `p_coop`; otherwise, decrease it. This encourages cooperation when the collective benefit is substantial.
4. **Edge Cases**:
	* In the last round, Cooperate (C) if the average contribution of all players in the previous round is high (`avg_prev_contrib` ≥ 0.5), and Defect (D) otherwise.
	* If a player has defected in every round so far, adjust `p_coop` to a lower value for that specific opponent.

**Collective Mindset:**

The ACC strategy prioritizes collective cooperation while adapting to the actions of other players. By initially cooperating and then responding to the average contribution level, we encourage others to contribute and create a mutually beneficial environment. The adaptive cooperation mechanism ensures that our strategy remains robust against various opponent behaviors.

**Robustness Features:**

1. **Exploration**: ACC explores different cooperation levels by adjusting `p_coop` based on the game's progression.
2. **Exploitation**: By responding to the average contribution level, ACC exploits the cooperative behavior of others when it is beneficial to do so.
3. **Forgiveness**: ACC allows for occasional defections and adjusts its strategy accordingly, promoting a more forgiving and resilient collective environment.

By incorporating these features, the Adaptive Collective Cooperation (ACC) strategy is well-equipped to handle various opponent behaviors and promote a mutually beneficial outcome in the Public Goods Game tournament.
'''

description_COLLECTIVE_56 = '''
**Collective Strategy: Adaptive Cooperation with Selfish Adjustment**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to do the same.
2. **Subsequent Rounds**: Observe the previous round's total contributions and calculate the average contribution per player (`avg_contrib`). If `avg_contrib` is above a certain threshold (`θ`), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism**: If the previous round's total contributions are below a certain fraction (`φ`) of the maximum possible contributions, defect (D) in the current round to "punish" non-cooperators.
4. **Selfish Adjustment**: Monitor individual payoffs and adjust strategy based on performance. If personal payoff is consistently lower than the group average, switch to defecting (D) for a few rounds to recoup losses.

**Edge Cases:**

* **Last Round**: Cooperate (C) in the final round, as there's no future benefit to defecting.
* **Early Defection**: If multiple players defect early on, reassess the situation and adjust strategy accordingly. If most players are cooperating, continue cooperating; otherwise, switch to defecting.

**Collective Mindset:**

The goal is to balance individual self-interest with collective welfare. By initially cooperating and punishing non-cooperation, we encourage others to contribute to the public good. Selfish adjustment allows for temporary deviations from cooperation when necessary, while still promoting overall group success.

**Thresholds (θ and φ)**:

* `θ` (cooperation threshold): 0.5 (i.e., cooperate if average contribution is above 50%)
* `φ` (punishment fraction): 0.25 (i.e., punish if total contributions are below 25% of maximum possible)

**Additional Notes:**

This strategy assumes no prior knowledge of opponents' behaviors and adapts to the group's overall performance. By incorporating both cooperative and selfish elements, it aims to balance individual interests with collective success in a wide range of scenarios.
'''

description_COLLECTIVE_57 = '''
**Collective Strategy: Adaptive Cooperation with Forgiveness**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a cooperative tone and encourage others to do the same.
2. **Contribution Evaluation:** After each round, calculate the total contribution rate (TCR) of all players:
   TCR = (Total contributions / n)
3. **Adaptive Cooperation:** In subsequent rounds, cooperate (C) if the previous round's TCR is above a certain threshold (e.g., 0.5). This encourages continued cooperation when others are contributing.
4. **Defection Response:** If the previous round's TCR falls below the threshold, defect (D) in the next round to signal dissatisfaction with low contributions and encourage others to increase their contributions.
5. **Forgiveness Mechanism:** After a defection response, cooperate again if the subsequent round's TCR exceeds the threshold. This allows for recovery from temporary deviations and promotes continued cooperation.

**Edge Case Handling:**

1. **Last Round:** Cooperate (C) in the final round to maximize collective payoffs, as there are no future rounds to influence.
2. **Single-Player Deviation:** If only one player deviates while others cooperate, maintain cooperation (C) to minimize losses and encourage the deviating player to return to cooperation.
3. **Multi-Player Deviation:** If multiple players deviate, defect (D) in response, but be prepared to forgive and cooperate again if contributions improve.

**Collective Mindset:**

This strategy prioritizes collective welfare by encouraging cooperation through adaptive responses to contribution rates. By forgiving temporary deviations and promoting continued cooperation, it aims to maximize overall payoffs while minimizing the risk of exploitation.
'''

description_COLLECTIVE_58 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Retaliation**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to contribute.
2. **Early Rounds (Rounds 2-5):** Cooperate if the average contribution rate of all players in the previous round is above 0.5. Otherwise, defect (D).
3. **Middle Rounds (Rounds 6-r/2):** Gradually retaliate against defectors by cooperating only if:
	* The player cooperated in the previous round and at least half of the other players cooperated.
	* Or, if a player defected in the previous round, cooperate only if they contributed more than the average contribution rate in that round.
4. **Late Rounds (Rounds r/2+1-r):** Retaliate more aggressively by cooperating only if:
	* The player cooperated in the previous two rounds and at least three-quarters of the other players cooperated.
	* Or, if a player defected in either of the previous two rounds, defect regardless of their current contribution rate.

**Edge Cases:**

1. **Last Round:** Cooperate if the average contribution rate is above 0.5; otherwise, defect to maximize individual payoff.
2. **Single Defector:** If only one player defects while all others cooperate, punish the defector by cooperating less frequently (or not at all) in subsequent rounds.

**Collective Mindset:**

The strategy prioritizes cooperation and encourages others to contribute by gradually retaliating against defectors. By adapting to the group's contribution rate, it aims to maintain a high level of cooperation while minimizing individual losses. This collective approach promotes mutual benefits and maximizes overall payoffs, even in the face of diverse opponent behaviors.

**Key Features:**

1. **Adaptive Cooperation:** Adjusts cooperation levels based on the group's past behavior.
2. **Gradual Retaliation:** Responds to defectors with decreasing cooperation rates over time.
3. **Collective Focus:** Prioritizes group welfare while maintaining individual robustness.

This strategy balances cooperation and self-interest, making it a robust competitor in the tournament against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_59 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Escalation**

In this Public Goods Game, our collective strategy balances individual self-interest with the need for cooperation to achieve mutual benefits. We'll use a dynamic approach that adjusts behavior based on past actions and payoffs.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) unconditionally to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:** Assess the previous round's total contributions and individual payoffs.
	* If total contributions ≥ (n \* k / 2), cooperate (C). This indicates sufficient collective investment, justifying our continued cooperation.
	* If total contributions < (n \* k / 2) but average payoff > (k / n), cooperate (C) with a probability of (average payoff / (k / n)). This "punishes" low contributors while allowing for some leniency.
	* Otherwise, defect (D).
3. **Escalation Mechanism:** Introduce an escalation counter, incrementing it by 1 each time the group's total contributions decrease from one round to the next. When this counter reaches a threshold (e.g., 2-3), switch to unconditional defection (D) for the remainder of the game.
4. **Last Round (Round r):** Defect (D) unconditionally, as cooperation will not affect future rounds.

**Edge Cases:**

* If all players have defected in a previous round, cooperate (C) with a probability of 0.5 to potentially restart cooperation.
* In the event of a tie in total contributions or average payoffs, maintain the current strategy (cooperate or defect).

**Collective Mindset:**
Our adaptive strategy promotes cooperation while protecting individual interests. By monitoring group performance and adjusting behavior accordingly, we encourage others to cooperate, fostering a collective benefit. The escalation mechanism prevents exploitation by gradually increasing pressure on non-cooperative players.

This strategy is designed to be robust against various opponent behaviors, including unconditional cooperators, defectors, or tit-for-tat strategies. Its adaptability and gradual escalation should help it perform well in the tournament.
'''

description_COLLECTIVE_60 = '''
**Collective Strategy: "Gradual Cooperation with Adaptive Punishment"**

**Overview**
This strategy aims to balance individual self-interest with collective welfare by gradually increasing cooperation while adapting to the group's behavior. It relies on reciprocity, punishment, and forgiveness to maintain a high level of cooperation.

**Decision Rules**

1. **Initial Rounds (r < 5)**: Cooperate (C) in the first few rounds to establish a cooperative tone and encourage others to follow.
2. **Reciprocal Cooperation**: If the group's average contribution in the previous round is above a certain threshold (e.g., 0.5), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism**: If the group's average contribution falls below a lower threshold (e.g., 0.2) for two consecutive rounds, switch to defecting (D) until the group's average contribution exceeds the higher threshold.
4. **Forgiveness**: After punishing the group, return to reciprocal cooperation if the group's average contribution exceeds the higher threshold.

**Edge Cases**

* **Last Round (r = n)**: Cooperate (C) regardless of the group's behavior to maximize collective welfare in the final round.
* **Tiebreaker**: In case of a tie in the group's average contribution, cooperate (C) if the previous round's outcome was cooperative, and defect (D) otherwise.

**Collective Mindset**
This strategy is designed to promote cooperation while adapting to various opponent behaviors. By cooperating initially and reciprocating cooperation, we encourage others to follow suit. The punishment mechanism helps maintain a high level of cooperation by responding to free-riding behavior. Forgiveness allows the group to recover from periods of low cooperation.

**Additional Considerations**

* **Noise Tolerance**: To account for noise or random behavior in opponents' actions, use a moving average (e.g., 3-round average) to calculate the group's average contribution.
* **Adaptive Thresholds**: Adjust the thresholds used in the reciprocal cooperation and punishment mechanisms based on the game's parameters (e.g., k, n) and the group's behavior over time.

By employing this strategy, we aim to create a cooperative environment that benefits all players while being robust to various opponent behaviors.
'''

description_COLLECTIVE_61 = '''
**Collective Strategy: "Adaptive Cooperative Revival"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a positive tone and encourage others to contribute.
2. **Subsequent Rounds:** Observe the previous round's total contributions and adjust behavior accordingly:
	* If total contributions are above the average expected value (k/2), cooperate (C). This suggests that enough players are contributing, making it worthwhile to continue cooperating.
	* If total contributions are below the average expected value (k/2), defect (D). This indicates that not enough players are contributing, and cooperation is unlikely to be beneficial.
3. **Punishment Mechanism:** If a player defects in a round where they were expected to cooperate (based on their previous actions), punish them by defecting for the next two rounds. This encourages players to maintain cooperation.
4. **Forgiveness:** After punishing a player, return to cooperating if they resume contributing.

**Edge Cases:**

* **Last Round:** Cooperate (C) unconditionally, as there's no future benefit to defecting and it promotes a positive ending to the game.
* **Low Total Contributions:** If total contributions are consistently low (< k/4), adopt an "Optimistic" strategy: cooperate for three consecutive rounds. This attempts to revive cooperation among players.

**Collective Mindset Alignment:**

This strategy is designed to promote collective welfare by:

1. Encouraging initial cooperation
2. Adapting to the group's behavior
3. Implementing a gentle punishment mechanism to maintain cooperation
4. Forgiving past transgressions

By balancing individual incentives with collective goals, "Adaptive Cooperative Revival" fosters an environment where cooperation can thrive.

**Additional Notes:**

This strategy assumes no prior knowledge of opponents' behaviors and adapts based on observed actions. By incorporating elements of punishment and forgiveness, it encourages a culture of cooperation while remaining robust to various opponent strategies.
'''

description_COLLECTIVE_62 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and gather information about opponents' behaviors.
2. **Subsequent Rounds**: Observe the total contributions from the previous round and calculate the average contribution per player, `avg_contrib`.
3. **Cooperation Threshold**: Set a cooperation threshold, `theta`, based on the game parameters: `theta = (k / n) * (n - 1)`. If `avg_contrib` is above `theta`, cooperate (C). Otherwise, defect (D).
4. **Punishment Mechanism**: If an opponent defects in a round where cooperation was expected (i.e., their contribution is below the average), gradually decrease cooperation probability for that opponent over subsequent rounds.
5. **Forgiveness**: Gradually increase cooperation probability for opponents who start contributing after a period of defection.

**Edge Cases:**

1. **Last Round**: Defect (D) in the last round, as there are no future interactions to influence.
2. **All Opponents Defected**: If all opponents have defected in a previous round, defect (D) in the next round to avoid exploitation.
3. **Opponent Cooperation**: If an opponent cooperates after a period of defection, increase cooperation probability for that opponent.

**Collective Mindset:**

1. **Encourage Cooperation**: By cooperating initially and gradually punishing defectors, we encourage opponents to cooperate and contribute to the public good.
2. **Adapt to Opponent Behavior**: Our strategy adapts to the behaviors of individual opponents, allowing us to respond effectively to a range of strategies.
3. **Balance Individual and Collective Interests**: By balancing cooperation and punishment, our strategy aims to optimize both individual payoffs and collective welfare.

This strategy is designed to be robust against various opponent behaviors while promoting cooperation and collective well-being in the Public Goods Game.
'''

description_COLLECTIVE_63 = '''
**Collective Strategy: "Adaptive Reciprocity with Forgiveness"**

This strategy aims to balance individual incentives with collective welfare, promoting cooperation while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to establish a positive tone and encourage others to contribute.
2. **Subsequent Rounds:** Observe the total contributions (TC) and average contribution rate (ACR) of all players in the previous round.
3. **Cooperation Condition:** If ACR ≥ 0.5, cooperate (C). Otherwise, defect (D).
4. **Reciprocity Mechanism:** If a player i defected (D) in the previous round, and their payoff was higher than the group average, punish them by defecting (D) in the current round.
5. **Forgiveness Mechanism:** After punishing a player, reset the reciprocity mechanism if they cooperate (C) in the next round.

**Edge Cases:**

* **Last Round:** Cooperate (C), as there's no future benefit to defecting and it may encourage others to contribute.
* **Single-Defector Scenario:** If only one player defects while all others cooperate, continue cooperating (C) to maintain social norms.
* **All-Defectors Scenario:** If all players defect, also defect (D) to avoid being exploited.

**Collective Mindset:**

This strategy aligns with the collective mindset by:

* Encouraging cooperation through reciprocity and forgiveness
* Punishing free-riders while providing opportunities for redemption
* Adapting to changing group dynamics to maintain social norms

By following this adaptive and forgiving approach, our strategy promotes a balance between individual incentives and collective welfare, increasing the chances of success in the Public Goods Game tournament.
'''

description_COLLECTIVE_64 = '''
**Collective Strategy: "Adaptive Cooperative Threshold" (ACT)**

The ACT strategy aims to balance individual self-interest with collective welfare by adaptively adjusting the cooperation threshold based on game history.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) if k > n/2; otherwise, defect (D).
2. **Contribution Threshold**: For subsequent rounds, calculate a contribution threshold, τ = (k/n) * α, where α is the average number of contributors in previous rounds.
3. **Cooperation vs Defection**:
	* If the current round's average payoff per contributor is above τ, contribute 1 token (C).
	* Otherwise, defect (D).
4. **Defection Tolerance**: Allow for a small margin of error by tolerating up to β (a small constant, e.g., 0.2) defections without retaliating.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 1 token (C) if k > n/2; otherwise, defect (D).
2. **No Previous Contributions**: If no player has contributed in previous rounds, default to the initial cooperation rule.
3. **Unanimous Defection**: If all players defected in the previous round, reset α and τ.

**Collective Alignment:**

1. **Social Welfare Focus**: Prioritize collective welfare by contributing when the average payoff per contributor is above the threshold.
2. **Adaptive Adjustment**: Dynamically adjust the contribution threshold based on game history to balance individual self-interest with collective welfare.
3. **Robustness to Opponent Behavior**: The strategy remains robust against a wide range of opponent behaviors, as it adapts to changing game conditions.

**Notes:**

* α and τ are initialized after the first round and updated each subsequent round.
* β is a small constant (e.g., 0.2) that allows for some margin of error in evaluating defections.
* The strategy assumes no communication or coordination channels; all decisions are based on observed actions and payoffs.

By employing this adaptive, threshold-based approach, the ACT strategy balances individual self-interest with collective welfare, ensuring a high level of cooperation while remaining robust to various opponent behaviors.
'''

description_COLLECTIVE_65 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Withdrawal"**

**Decision Rules:**

1. **Initial Rounds**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Subsequent Rounds**: Observe the total contributions and payoffs from the previous round.
	* If the average payoff per player is above a threshold (T = k/n), continue contributing 1 token (C).
	* If the average payoff per player falls below T, switch to contributing 0 tokens (D) for one round.
	* After switching to D, observe the total contributions and payoffs again. If they recover to above T, revert to C; otherwise, remain at D.
3. **Punishment Mechanism**: If a player defects (D) while others cooperate, that player's payoff will be lower due to the multiplier effect (k/n). Gradually withdraw cooperation by reducing the contribution rate in subsequent rounds if this behavior persists.

**Edge Cases:**

* **Last Round**: In the final round, contribute 0 tokens (D), as there is no future benefit from cooperation.
* **Solo Player or Only One Opponent**: Contribute 1 token (C) to maximize payoffs.
* **Multiple Players with Low Contributions**: If multiple players are contributing 0 tokens (D), gradually reduce contributions over several rounds, then re-evaluate the situation.

**Collective Mindset:**

This strategy promotes cooperation by:

1. Encouraging initial cooperation
2. Responding to changes in collective payoffs
3. Gradually adapting to opponents' behaviors
4. Punishing persistent defectors

By adjusting contributions based on observed outcomes and opponent actions, this strategy balances individual self-interest with collective welfare.

**Robustness:**

This strategy is designed to be robust against various opponent behaviors:

1. **Cooperative opponents**: It rewards cooperation by maintaining high contribution rates.
2. **Defecting opponents**: It gradually withdraws cooperation in response to persistent defection.
3. **Mixed-strategy opponents**: It adapts to changing behavior and adjusts contributions accordingly.

By playing this strategy, we aim to promote a balance between individual self-interest and collective welfare, while also being robust against diverse opponent behaviors.
'''

description_COLLECTIVE_66 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Escalation**

**Overview**
Our strategy, "ACE," balances individual self-interest with collective welfare by adapting to the group's cooperation level and gradually escalating contributions. ACE is designed to promote cooperation while protecting against exploitation.

**Decision Rules**

1. **First Round**: Cooperate (C) to encourage initial cooperation and set a positive tone.
2. **Subsequent Rounds**:
	* If the average contribution of other players in the previous round is above 0.5, cooperate (C).
	* Otherwise, defect (D) with probability `p`, where `p` increases by 0.1 each time the group's average contribution falls below 0.5.
3. **Gradual Escalation**: If the group's average contribution remains low (< 0.5), increase the defection probability `p` by 0.1 every two rounds, up to a maximum of 1 (full defection).
4. **Punishment and Forgiveness**:
	* If another player defects while others cooperate, punish them by defecting in the next round.
	* After punishing, return to cooperating if the group's average contribution rises above 0.5.

**Edge Cases**

1. **Last Round**: Cooperate (C) to maximize collective welfare and encourage cooperation in future games.
2. **Solo Play**: Defect (D), as there is no benefit to contributing without others.

**Collective Mindset**
ACE prioritizes the group's well-being while protecting individual interests. By adapting to the group's cooperation level, ACE promotes a culture of mutual support and cooperation, gradually escalating contributions to encourage higher collective payoffs.

By playing ACE in the tournament, we aim to demonstrate that an adaptive, gradual escalation strategy can effectively balance individual self-interest with collective welfare, leading to better outcomes for all players.
'''

description_COLLECTIVE_67 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **First Round:** Cooperate (C) - Start with optimism, assuming others will contribute to the public good.
2. **Subsequent Rounds:** Observe the previous round's total contributions and adjust behavior accordingly:
	* If total contributions are above a certain threshold (e.g., 50% of players contributed), Cooperate (C). This suggests that enough players are willing to contribute, making it worthwhile to do so.
	* If total contributions are below this threshold, Defect (D). This indicates that not enough players are contributing, and it's better to keep one's own token.
3. **Adaptation Mechanism:** Introduce a "sensitivity parameter" (SP) that tracks the number of consecutive rounds with low total contributions. If SP exceeds 2-3 rounds, increase the contribution threshold by 10-20%. This allows ACO to adapt to repeated free-riding and avoid getting exploited.

**Edge Cases:**

* **Last Round:** Cooperate (C) - Regardless of previous behavior, contributing in the last round ensures that some public good is generated.
* **Early Rounds with Low Contributions:** If total contributions are extremely low (e.g., < 20% of players contributed), Defect (D) immediately. This prevents getting exploited by free-riders.

**Collective Mindset:**

ACO aims to balance individual self-interest with the collective good. By starting with cooperation and adapting to others' behavior, ACO encourages contributions while protecting against exploitation. The sensitivity parameter allows ACO to respond to changes in the group's behavior, promoting a stable and fair outcome.

This strategy should perform well in a tournament setting, as it:

1. Encourages cooperation when possible.
2. Adapts to different opponent behaviors.
3. Avoids getting exploited by free-riders.

Let me know if you'd like me to adjust or refine this strategy!
'''

description_COLLECTIVE_68 = '''
Here's a strategic plan for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone and encourage others to do the same.
2. **Reciprocity**: If at least half of the players contributed in the previous round, contribute 1 token (C) in the current round. This encourages reciprocity and builds trust.
3. **Punish Defection**: If less than half of the players contributed in the previous round, defect (D) in the current round. This discourages exploitation and promotes cooperation.
4. **Adaptive Threshold**: Update the threshold for cooperation based on the game's history. If the average contribution rate is above 0.5, decrease the threshold by 0.1; if it's below 0.5, increase the threshold by 0.1.

**Edge Cases:**

* In the last round, defect (D) to maximize personal payoff.
* If a player has defected in every previous round, assume they will continue to do so and adjust our strategy accordingly.
* If all players have contributed in every previous round, continue contributing (C) to maintain cooperation.

**Collective Mindset:**

ACO prioritizes collective welfare while adapting to the game's dynamics. By initially cooperating and reciprocating cooperation, we encourage others to do the same. Punishing defection helps maintain a cooperative environment, while our adaptive threshold ensures that we respond effectively to changing circumstances.

**Robustness:**

ACO is designed to perform well against various opponent behaviors:

* **Cooperative opponents**: ACO will continue cooperating, maximizing collective payoffs.
* **Defective opponents**: ACO's punishment mechanism discourages exploitation and promotes cooperation.
* **Mixed-strategy opponents**: ACO's adaptive threshold allows it to adjust to changing circumstances.

By following this strategy, we aim to balance individual incentives with collective welfare, achieving a high level of cooperation in the Public Goods Game.
'''

description_COLLECTIVE_69 = '''
Here's a strategic approach for the Public Goods Game that adapts to various opponent behaviors and prioritizes collective welfare:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) unconditionally to establish a baseline of cooperation and encourage others to reciprocate.
2. **Reciprocal Cooperation**: If at least half of the players contributed in the previous round, continue contributing 1 token (C) in the current round. This encourages sustained cooperation when there's evidence of collective effort.
3. **Conditional Defection**: If fewer than half of the players contributed in the previous round, defect by not contributing (D) in the current round. This reduces individual losses when others are not cooperating.
4. **Adaptive Re-entry**: If, after a defection phase, at least two-thirds of the players contribute in a subsequent round, re-enter the cooperative phase and contribute 1 token (C). This allows for re-establishing cooperation if others have changed their behavior.

**Edge Cases:**

1. **Last Round**: In the final round, always defect by not contributing (D), as there's no future opportunity to reciprocate or adjust.
2. **Ties in Contribution Rates**: When determining whether to cooperate or defect based on previous contribution rates, resolve ties by choosing cooperation if the tie is exactly half of the players and defecting otherwise.

**Collective Mindset:**

1. **Prioritize Collective Welfare**: The primary goal is to maximize collective payoffs while balancing individual incentives.
2. **Encourage Cooperation**: By initially cooperating and reciprocating when others do, we create an environment that encourages cooperation and mutual benefit.
3. **Adapt to Environment**: Adjusting our strategy based on the actions of other players ensures resilience in the face of changing behaviors.

**Rationale:**

ACO balances individual incentives with collective welfare by adapting to the group's behavior. It initially establishes a cooperative baseline, then adjusts its level of cooperation based on others' actions. By doing so, it fosters an environment where mutual benefit is achievable while protecting against exploitation when others defect. This strategy should perform well in a tournament setting, as it does not rely on shared norms or coordination but instead adapts to various opponent behaviors.
'''

description_COLLECTIVE_70 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Reciprocity"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a positive tone and encourage mutual cooperation.
2. **Response to Cooperation**: If the majority (> 50%) of players cooperated in the previous round, cooperate (C) in the current round. This encourages continued cooperation when it is successful.
3. **Response to Defection**: If the majority (> 50%) of players defected in the previous round, defect (D) in the current round. This discourages exploitation and promotes a balanced approach.
4. **Tit-for-Tat with Gradual Reciprocity**: For each player i:
	* Calculate the average cooperation rate of all opponents over the past r rounds (excluding the most recent round).
	* If the opponent's average cooperation rate is above 50%, cooperate (C) with probability proportional to their average cooperation rate.
	* Otherwise, defect (D) with a fixed probability p_d (e.g., 0.2), allowing for some exploration and adaptation.
5. **Last Round**: Cooperate (C) in the last round if the total contributions in the previous round were above a threshold (e.g., n/2). This promotes collective welfare even when individual incentives are weak.

**Edge Cases:**

* If only one player remains, always cooperate (C).
* In case of a tie ( equal number of cooperators and defectors), flip a coin to decide between cooperation and defection.

**Collective Mindset Alignment:**
This strategy prioritizes collective welfare while maintaining individual adaptability. By responding to the majority's actions and adapting to opponents' behavior, it promotes cooperation when beneficial and balances individual interests when necessary.

By implementing this "Adaptive Cooperation with Gradual Reciprocity" strategy, our AI system will demonstrate a robust and adaptive approach in the Public Goods Game tournament, aligning with the collective mindset while navigating diverse opponent behaviors.
'''

description_COLLECTIVE_71 = '''
Here's a collective strategy for the Public Goods Game that adapts to various opponent behaviors:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline level of cooperation.
2. **Reciprocal Altruism**: If the average contribution of all players in the previous round is above 0.5 tokens, contribute 1 token (C) in the current round.
3. **Punish Free-Riders**: If the average contribution of all players in the previous round is below 0.5 tokens, and your own payoff was lower than the group's average payoff, defect (D) in the current round to signal dissatisfaction with free-riding behavior.
4. **Conditional Cooperation**: If a player has defected (D) in the previous round, but the group's total contribution was still high (> 0.7 tokens), contribute 1 token (C) in the current round, assuming that player might return to cooperation.

**Handling Edge Cases:**

* **Last Round:** Cooperate (C) unconditionally in the last round to maximize collective payoff.
* **Single Player Deviation**: If only one player has deviated from the group's contribution level, maintain cooperation (C) to encourage them to return to cooperation.
* **Multiple Players Deviating**: If multiple players have deviated, adapt to the new average contribution level and adjust strategy accordingly.

**Collective Mindset Alignment:**

ACO prioritizes collective welfare by initially cooperating, reciprocating altruism, punishing free-riders, and adapting to changing group dynamics. By conditioning cooperation on the group's overall behavior, ACO encourages cooperation while preventing exploitation.

This strategy balances individual self-interest with collective benefits, making it robust against various opponent behaviors in a tournament setting.
'''

description_COLLECTIVE_72 = '''
Here's a collective strategy for the Public Goods Game that adapts to various opponent behaviors:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **First Round:** Contribute 1 token (C). This initial cooperation encourages others to reciprocate and establishes a positive tone.
2. **Subsequent Rounds:** Use the following rules:
	* If the average contribution in the previous round is above 0.5, contribute 1 token (C).
	* If the average contribution in the previous round is below 0.3, defect by contributing 0 tokens (D).
	* Otherwise, mirror the most common action in the previous round.
3. **Last Round:** Contribute 1 token (C) if the average payoff over all rounds is above the individual endowment; otherwise, defect.

**Edge Cases:**

* If there's only one player left in the game, always contribute 0 tokens (D).
* If a player has consistently defected throughout the game (i.e., never contributed), switch to defection permanently.
* In cases of ties or equal average contributions, favor cooperation (C).

**Collective Mindset:**

ACO prioritizes collective welfare by initially contributing and encouraging others to reciprocate. It adapts to the group's behavior, rewarding cooperation and punishing chronic defection. By mirroring common actions, ACO fosters a sense of shared responsibility and promotes convergence toward cooperative outcomes.

This strategy balances individual self-interest with collective benefits, promoting a mutually beneficial outcome in the face of diverse opponent behaviors.
'''

description_COLLECTIVE_73 = '''
**Collective Strategy: Adaptive Cooperative Escalation (ACE)**

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocity**: For each subsequent round, calculate the average contribution of all players in the previous round. If the average is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Punishment and Forgiveness**: Monitor the opponent's behavior over a window of w rounds (e.g., w = 3). If an opponent defects more than once in this window, punish by defecting (D) for one round. After punishment, forgive and return to reciprocity.
4. **Escalation**: If a player detects that their own contributions are consistently higher than the group average over several rounds (e.g., 5), escalate cooperation by contributing an additional token (C) for one round.

**Edge Cases**

* Last Round: Cooperate (C) to maintain reputation and encourage others to do the same.
* Opponent Defection Streak: If an opponent defects for more than w rounds, assume they are a consistent defector and always defect (D).
* Self-Defection Detection: If ACE detects its own defection streak, re-evaluate the group's behavior and adjust strategy accordingly.

**Collective Mindset**

ACE prioritizes cooperation while adapting to the group's dynamics. By reciprocating cooperation and punishing defections, ACE encourages others to contribute to the public good. The escalation mechanism promotes increased cooperation when individual contributions are consistently above average, fostering a culture of mutual support.
'''

description_COLLECTIVE_74 = '''
**Collective Strategy: "Gradual Reciprocity with Endgame Adaptation"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Cooperation**: For rounds 2-r-1, cooperate (C) if the average contribution of all players in the previous round is above the threshold (k/n). Otherwise, defect (D).
3. **Gradual Reciprocity**: If another player defects while you cooperated in the previous round, decrease your contribution probability by a small margin (e.g., 10%) for each subsequent round.
4. **Endgame Adaptation**: In the last round (r), if the total contributions in the second-to-last round are below the threshold (k/n), defect (D) to maximize individual payoff.

**Edge Cases:**

* If all players defected in the previous round, cooperate (C) in the next round to restart cooperation.
* If a player defects while you cooperated, but then contributes in the subsequent round, increase your contribution probability by a small margin (e.g., 10%) for each subsequent round.

**Collective Mindset:**

This strategy aims to balance individual self-interest with collective welfare. By initially cooperating and gradually adapting to others' actions, we promote a cooperative environment while being cautious of exploitation. The endgame adaptation ensures that we don't miss opportunities for individual gain when cooperation is unlikely to succeed.

**Rationale:**

* Gradual reciprocity encourages cooperation by responding to the average contribution level, allowing for flexibility in adjusting to different opponent behaviors.
* Endgame adaptation prevents over-cooperation in the final round, which could result in suboptimal payoffs.
* By not assuming shared norms or coordination, this strategy remains robust against a wide range of independent opponent strategies.

This collective strategy should perform well in the tournament by striking a balance between cooperation and self-interest, while adapting to various opponent behaviors.
'''

description_COLLECTIVE_75 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Forgiveness**

Our collective strategy, "Adaptive Cooperation with Gradual Forgiveness" (ACGF), aims to balance individual self-interest with the need for cooperation to achieve collective welfare. ACGF is adaptive, robust, and designed to perform well against a wide range of opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) unconditionally.
2. **Reciprocal Altruism**: For rounds t > 1:
	* If the average contribution of all players in the previous round is above a certain threshold (θ = 0.5), contribute 1 token (C).
	* Otherwise, defect (D) with probability p(t), where p(t) increases as the number of consecutive rounds with low average contributions grows.
3. **Gradual Forgiveness**: If an opponent defects while you cooperate, forgive them by cooperating in the next round with a certain probability (q = 0.7). This probability decreases if the opponent continues to defect.
4. **Self-Protection**: If your payoff is below a certain threshold (φ = 0.2 * k) for two consecutive rounds, defect (D) unconditionally.

**Edge Cases:**

1. **Last Round**: Defect (D) in the last round (r) to maximize individual payoff.
2. **Early Rounds**: Contribute 1 token (C) in early rounds (t ≤ 3) to encourage cooperation and build trust.
3. **Tiebreaker**: In case of a tie, break by cooperating (C).

**Collective Mindset:**

ACGF prioritizes collective welfare while protecting individual interests. By cooperating initially and reciprocating altruism, we create an environment conducive to mutual cooperation. Gradual forgiveness encourages opponents to cooperate, while self-protection safeguards against exploitation.

By adapting to the game's history and opponent behaviors, ACGF balances short-term gains with long-term benefits, promoting a stable and cooperative collective outcome.
'''

description_COLLECTIVE_76 = '''
**Collective Strategy: "Gradual Reciprocity with Forgiveness"**

In this repeated Public Goods Game, our collective strategy aims to balance individual incentives with collective welfare. We will employ a gradual reciprocity approach, adapting to the group's behavior while incorporating elements of forgiveness.

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3):** Cooperate (C) unconditionally to establish a positive tone and encourage others to contribute.
2. **Subsequent Rounds:** Observe the previous round's total contributions (TC) and calculate the average contribution per player (ACP = TC / n).
	* If ACP ≥ 0.5, cooperate (C). This indicates that at least half of the players are contributing, making it worthwhile to continue cooperating.
	* If ACP < 0.5, defect (D) with a probability proportional to the number of defectors in the previous round (DP). Specifically:
		+ Defect probability = DP / n
		+ Cooperate with the remaining probability (1 - defect probability)
3. **Punishment and Forgiveness:** If a player defects while others cooperate, we will punish them by defecting in the next round with a higher probability.
	* Punishment probability = 0.7 if the player defected in the previous round and ACP > 0.5
	* However, to avoid escalating conflicts, we will forgive players who cooperate after being punished:
		+ If a previously punished player cooperates, reset the punishment probability to 0

**Edge Cases:**

1. **Last Round:** Cooperate (C) unconditionally, as there is no future round to influence.
2. **Single Player Defection:** If only one player defects in a round, and others cooperate, we will forgive them in the next round by cooperating.

**Collective Mindset:**
Our strategy prioritizes collective welfare while adapting to individual behaviors. By gradually reciprocating cooperation and incorporating forgiveness, we aim to create an environment where players are incentivized to contribute to the public good.
'''

description_COLLECTIVE_77 = '''
**Collective Strategy: "Gradual Cooperation with Adaptive Punishment"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **Subsequent Rounds:** Observe the total contributions and payoffs of all players from the previous round. If:
	* The average contribution is above 0.5, cooperate (C). This indicates that most players are contributing, so continue to do so to maintain collective welfare.
	* The average contribution is below 0.5, defect (D) with a probability proportional to the deviation from 0.5. This introduces a gradual punishment mechanism to deter free-riding.
3. **Punishment Adjustment:** If a player defects after cooperating in the previous round, increase the probability of defection by 10% for that player in subsequent rounds. Conversely, if a player cooperates after defecting, decrease the probability of defection by 10%. This adaptive punishment mechanism aims to correct deviations and encourage cooperation.
4. **Exception Handling:** If all players defected in the previous round, cooperate (C) with a probability of 50% to reintroduce cooperation and potentially reset the game.

**Edge Cases:**

1. **Last Round:** Cooperate (C) unconditionally, as there is no future opportunity for reciprocity or punishment.
2. **Tie-breaking:** In cases where multiple strategies would lead to identical payoffs, prioritize cooperation (C).

**Collective Mindset Alignment:**

This strategy aligns with the collective mindset by:

1. Encouraging initial cooperation to set a positive tone
2. Gradually adapting to the group's behavior, rewarding cooperation and punishing defection
3. Fostering cooperation through adaptive punishment mechanisms

By doing so, this strategy promotes mutual understanding, reciprocity, and cooperation among players, ultimately leading to improved collective welfare.

**Robustness:**

This strategy is robust against various opponent behaviors due to its:

1. Adaptive nature, adjusting to the group's behavior
2. Gradual punishment mechanism, discouraging free-riding without being overly punitive
3. Collective mindset alignment, promoting cooperation and reciprocity

These features enable the strategy to perform well in a wide range of scenarios, including against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_78 = '''
**Collective Strategy: "Adaptive Collective Optimism"**

This strategy balances individual self-interest with collective welfare, adapting to the group's behavior over time. It promotes cooperation while being robust against defectors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative tone.
2. **Reciprocal Cooperation**: If the total contributions in the previous round exceeded the threshold `k/2`, contribute (C) in the current round. This encourages continued cooperation when others are contributing sufficiently.
3. **Proportional Retaliation**: Calculate the average contribution of other players (`avg_contrib_others`) in the previous round. If it's below a certain threshold (`k/n * 0.5`), defect (D) with a probability proportional to the difference between `avg_contrib_others` and the threshold. This deters exploitation by defectors.
4. **Adaptive Adjustment**: After each round, adjust the contribution strategy based on the group's overall performance:
	* If total payoffs increase compared to the previous round, maintain the current strategy (cooperate or defect).
	* If total payoffs decrease, switch strategies for the next round (e.g., from cooperate to defect or vice versa).

**Edge Cases:**

1. **Last Round**: Defect (D) in the last round (`r`) to maximize individual payoff.
2. **Only One Player**: Always contribute (C) when there's only one other player, as cooperation is guaranteed to yield a higher payoff.

**Collective Mindset:**
This strategy prioritizes collective welfare while protecting against exploitation. By initially cooperating and adapting to the group's behavior, it promotes a mutually beneficial environment. The reciprocal cooperation rule encourages others to contribute, increasing overall payoffs. Proportional retaliation discourages defectors from exploiting cooperators.
'''

description_COLLECTIVE_79 = '''
**Collective Strategy: "Adaptive Collective Optimism" (ACO)**

**Overview**
ACO balances individual self-interest with collective welfare by adapting to the group's contribution history. It aims to maximize overall payoffs while minimizing exploitation.

**Decision Rules**

1. **First Round**: Cooperate (C) to seed a positive contribution norm.
2. **Subsequent Rounds**: Observe the previous round's total contributions and calculate the average contribution rate (`avg_contribution_rate = total_contributions / n`).
	* If `avg_contribution_rate >= 0.5`, Cooperate (C). This indicates a sufficient level of cooperation, so we continue to contribute.
	* If `avg_contribution_rate < 0.5`, Defect (D) with probability `p_defect = (1 - avg_contribution_rate) / (2 - avg_contribution_rate)`. This introduces a probabilistic defection mechanism to discourage free-riding while still allowing for some cooperation.
3. **Punishment Mechanism**: If the previous round's total contributions are 0, Defect (D) with probability `p_defect = 1` in the current round. This ensures that if everyone defects, we also defect to avoid being exploited.

**Handling Edge Cases**

* **Last Round**: Cooperate (C) unconditionally to maximize collective payoffs, as there is no future game to consider.
* **Ties in Average Contribution Rate**: In case of a tie, Cooperate (C) to maintain a positive contribution norm.

**Collective Mindset**
ACO prioritizes the group's overall payoff by:

1. Encouraging cooperation when others contribute sufficiently.
2. Gradually introducing defection when cooperation is low, to deter free-riding.
3. Punishing widespread defection to maintain a baseline level of cooperation.

By adapting to the group's contribution history and balancing individual self-interest with collective welfare, ACO aims to achieve a robust and efficient equilibrium in the Public Goods Game.
'''

description_COLLECTIVE_80 = '''
**Collective Strategy: Adaptive Cooperative Optimizer (ACO)**

**Overview**
The Adaptive Cooperative Optimizer (ACO) strategy aims to balance individual self-interest with collective welfare by adaptively adjusting cooperation levels based on the game's history. ACO seeks to maximize overall payoffs while being robust against various opponent behaviors.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative baseline.
2. **Contribution Threshold**: Calculate the average contribution of all players in the previous round (avg_prev_contribution). If avg_prev_contribution ≥ 0.5, contribute 1 token (C); otherwise, contribute 0 tokens (D).
3. **Punishment Mechanism**: If a player defects (D) while others cooperate (C), reduce cooperation by 20% in the next round. This aims to punish free-riding behavior.
4. **Reward Cooperation**: If all players cooperate (C) for two consecutive rounds, increase cooperation by 10% in the next round to reinforce collective cooperation.

**Edge Cases**

1. **Last Round**: In the final round, contribute 1 token (C) regardless of previous actions, as there is no future punishment or reward.
2. **Single Player Defection**: If only one player defects (D), maintain cooperation level from the previous round.
3. **All Players Defect**: If all players defect (D), reset cooperation to 50% in the next round.

**Collective Mindset**

1. **Focus on Collective Welfare**: Prioritize overall payoffs over individual gains, recognizing that collective cooperation benefits all players.
2. **Adapt to Opponent Behavior**: Adjust cooperation levels based on observed actions to maintain a balance between individual and collective interests.
3. **Encourage Cooperation**: Gradually increase cooperation when others cooperate, creating an environment conducive to mutual benefit.

**Robustness**

1. **Noise Tolerance**: ACO can handle occasional deviations or mistakes by adapting to the game's history.
2. **Diverse Opponent Behaviors**: By responding to observed actions, ACO remains effective against various opponent strategies, including pure cooperation, pure defection, and mixed behaviors.

By employing this adaptive strategy, we aim to maximize collective payoffs while being robust against a wide range of opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_81 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Withdrawal**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a positive tone and encourage others to contribute.
2. **Subsequent Rounds**: Calculate the average contribution rate of all players from previous rounds (avg_contribution). If avg_contribution is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Contribution Threshold**: Introduce a dynamic threshold (θ) that decreases over time. Initially, θ = 1. In each subsequent round, decrease θ by 0.05 if the average contribution rate falls below 0.5. Cooperate only if avg_contribution ≥ θ.
4. **Punishment Mechanism**: Implement a gradual withdrawal mechanism to discourage persistent defectors. If a player defects in two consecutive rounds, reduce cooperation with them by 20% for the next two rounds.

**Edge Case Handling:**

1. **Last Round**: Cooperate (C) unconditionally in the last round, as there is no future interaction to influence.
2. **Single-Player Deviation**: If only one player deviates and defects while all others cooperate, continue cooperating with them for one more round before reassessing.

**Collective Mindset Alignment:**

1. **Encourage Cooperation**: By cooperating in the first round and maintaining a high contribution rate, this strategy promotes a cooperative environment.
2. **Flexibility**: Adapt to changes in opponent behavior by adjusting the contribution threshold (θ) and implementing a punishment mechanism.
3. **Gradual Withdrawal**: Avoid sudden, drastic measures that might escalate conflict; instead, gradually reduce cooperation with persistent defectors.

**Additional Notes:**

* This strategy balances individual self-interest with collective welfare, as it adapts to the average contribution rate and punishes persistent defectors.
* The gradual withdrawal mechanism helps maintain a stable environment by discouraging exploitation without resorting to harsh punishments.
* By not assuming shared norms or coordination, this strategy is robust against a wide range of opponent behaviors.
'''

description_COLLECTIVE_82 = '''
**Collective Strategy: "Adaptive Cooperative Escalation"**

This strategy balances individual self-interest with collective welfare, adapting to the behavior of opponents while promoting cooperation.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) if k > n/2; otherwise, defect (D). This sets a cooperative tone when the potential return is high.
2. **Reciprocal Cooperation**: If the total contribution in the previous round was at least 50% of the total possible contributions, contribute (C) with a probability proportional to the average cooperation level in the last round. This encourages reciprocity and cooperation when others are contributing.
3. **Gradual Escalation**: If total contributions have decreased over the past two rounds, increase the contribution probability by 10% each round until the desired level of cooperation is reached or maximum contribution is achieved. This responds to declining cooperation with a measured escalation of cooperative efforts.
4. **Exploitation Avoidance**: If an opponent has defected (D) more than twice as often as they cooperated (C) in the last three rounds, defect (D) with 50% probability. This discourages exploitation by free-riding opponents.

**Edge Cases:**

1. **Last Round**: Contribute (C) if total contributions have been increasing; otherwise, defect (D). This ensures a final push for collective gain or protects against last-round exploitation.
2. **Early Defection**: If more than 50% of players defected in the first two rounds, adjust the cooperation probability downward by 20%. This adapts to early signs of uncooperative behavior.

**Collective Mindset Alignment:**

1. **Cooperation Baseline**: Start with an optimistic view, assuming other players will cooperate.
2. **Reciprocity Focus**: Prioritize responding to others' cooperative actions to foster a collective environment.
3. **Adaptive Flexibility**: Adjust strategy in response to changes in the group's behavior to maintain a balance between individual and collective interests.

This "Adaptive Cooperative Escalation" strategy promotes cooperation while adapting to various opponent behaviors, aiming for an optimal balance of individual self-interest and collective welfare.
'''

description_COLLECTIVE_83 = '''
Here's a collective strategy for the Public Goods Game (PGG) that adapts to various opponent behaviors and aligns with the collective mindset:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C). This sets a cooperative tone and encourages others to follow suit.
2. **Reciprocity**: If the total contributions in the previous round were above the average contribution (i.e., sum_j c_j > n/2), contribute 1 token (C) in the current round. Otherwise, defect (D).
3. **Punishment for Free-Riding**: If a player's payoff in the previous round was higher than their contribution (i.e., p_i > c_i), defect (D) in the current round.
4. **Learning from Others' Cooperation**: If more than half of the players contributed 1 token (C) in the previous round, increase the likelihood of contributing 1 token (C) in the current round by 20%.
5. **Adaptive Adjustment**: Every 5 rounds, reassess the group's cooperation level and adjust the contribution probability accordingly:
	* If average contributions are above 0.7, increase the contribution probability by 10%.
	* If average contributions are below 0.3, decrease the contribution probability by 10%.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 1 token (C) if the total contributions in the previous round were above the average contribution.
2. **Single-Player Deviation**: If only one player deviates from cooperation, defect (D) in the next round to signal disapproval.

**Collective Mindset:**

ACO prioritizes collective welfare by:

1. Encouraging initial cooperation and reciprocity
2. Punishing free-riding behavior
3. Learning from others' cooperative actions
4. Adapting to changing group dynamics

By employing ACO, the strategy fosters a collaborative environment that promotes mutual benefits while deterring exploitative behavior.

This collective strategy should perform well in the tournament against independent strategies developed by other AI systems, as it balances cooperation and self-interest while adapting to various opponent behaviors.
'''

description_COLLECTIVE_84 = '''
**Collective Strategy: Adaptive Collective Optimism (ACO)**

**Overview**
ACO is a robust, adaptive strategy for the Public Goods Game that balances individual self-interest with collective welfare. By observing past actions and payoffs, ACO adjusts its cooperation level to promote mutual benefit while protecting against exploitation.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocity**: For each subsequent round, calculate the average contribution of all players in the previous round (`avg_contrib_prev`). If `avg_contrib_prev` is above a certain threshold (e.g., 0.5), contribute 1 token (C). Otherwise, defect (D).
3. **Adaptive Threshold**: Adjust the cooperation threshold based on the game's history:
	* If the average payoff in the last few rounds (`avg_payoff_recent`) is higher than the average payoff overall (`avg_payoff_all`), decrease the threshold by 0.1.
	* If `avg_payoff_recent` is lower than `avg_payoff_all`, increase the threshold by 0.1.
4. **Punishment**: If a player defects (D) in a round where the average contribution is above the threshold, defect (D) against that player for the next two rounds.

**Edge Cases**

* **Last Round**: Cooperate (C) to maintain a positive reputation and encourage reciprocity from others.
* **Low Contributions**: If total contributions are consistently low (< 0.2), switch to defecting (D) to avoid exploitation.

**Collective Mindset**
ACO prioritizes collective welfare by:

* Encouraging cooperation through initial generosity and reciprocity
* Adapting to the group's behavior to maintain a balance between individual self-interest and collective benefit
* Punishing exploitative behavior while avoiding unnecessary conflict

By following ACO, players can create an environment where cooperation is rewarded, and mutual benefit is achieved.
'''

description_COLLECTIVE_85 = '''
Here is a collective strategy for the Public Goods Game (PGG):

**Strategy Name:** Adaptive Collective Conscience (ACC)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocal Altruism**: If the total contributions in the previous round are above the group's average endowment (n/2), contribute 1 token (C). This encourages continued cooperation when others have contributed.
3. **Gradual Punishment**: If the total contributions in the previous round are below the group's average endowment (n/2) and your payoff was lower than the average payoff, defect (D) with a probability proportional to the difference between the actual and expected payoffs. This gradually punishes free-riding behavior.
4. **Forgiveness**: If you defected in the previous round due to Gradual Punishment and the total contributions in that round were above the group's average endowment, contribute 1 token (C) with a probability of 0.5. This allows for forgiveness and re-entry into cooperative behavior.

**Edge Cases:**

* **Last Round**: Contribute 1 token (C) to maximize collective welfare, regardless of previous actions.
* **Single-Player Deviation**: If only one player deviates from cooperation, maintain cooperation (C) in the next round to encourage re-cooperation.
* **Multiple-Player Deviation**: If multiple players deviate from cooperation, apply Gradual Punishment with increased probability.

**Collective Mindset:**

The ACC strategy prioritizes collective welfare by:

1. Encouraging initial cooperation and reciprocal altruism.
2. Gradually punishing free-riding behavior to maintain a cooperative environment.
3. Allowing for forgiveness and re-entry into cooperative behavior.

By adapting to the group's dynamics and responding to deviations from cooperation, the ACC strategy promotes a collective mindset that balances individual incentives with collective welfare.

This strategy is robust to various opponent behaviors, as it does not rely on shared norms or coordination channels. Instead, it uses observable history to inform decisions and adapt to changing circumstances.
'''

description_COLLECTIVE_86 = '''
**Collective Strategy: Adaptive Reciprocity with Gradual Cooperation**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to encourage mutual cooperation and set a positive tone for the game.
2. **Subsequent Rounds**: Use a hybrid approach that balances reciprocity and gradual cooperation:
	* If the average contribution of other players in the previous round is above 0.5, cooperate (C).
	* Otherwise, defect (D) with a probability proportional to the difference between the average contribution and 0.5.
3. **Reciprocal Adjustment**: If another player defects while you cooperated in the same round, decrease your cooperation rate by 10% for that specific opponent in future rounds.

**Edge Cases:**

1. **Last Round**: Cooperate (C) if the total contributions of all players are above a threshold (e.g., n/2), to maximize collective welfare.
2. **Low Contributions**: If total contributions fall below a certain level (e.g., k/4), switch to defecting (D) for a few rounds to signal dissatisfaction and prompt others to increase their cooperation.

**Collective Mindset:**

1. **Cooperation Bonus**: Reward players who consistently contribute above 0.5 by slightly increasing your own contribution rate when interacting with them.
2. **Group Performance Tracking**: Monitor the overall performance of the group (average contributions) and adjust individual behavior accordingly, prioritizing collective success.

**Robustness Measures:**

1. **Noise Tolerance**: Introduce randomness in decision-making to account for possible errors or noise in opponent actions.
2. **Oponent Behavior Adaptation**: Continuously update your assessment of opponents' strategies based on their past actions and adjust your behavior accordingly.

This strategy promotes cooperation while allowing for flexibility and adaptation to a wide range of opponent behaviors, aiming to achieve the best collective outcome.
'''

description_COLLECTIVE_87 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Forgiveness"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **Subsequent Rounds:** Observe the total contributions from the previous round (`sum_j c_j`) and calculate the average contribution (`avg_contribution = sum_j c_j / n`).
3. **Cooperation Threshold:** If `avg_contribution >= 0.5`, Cooperate (C) in the current round. This threshold encourages cooperation when a sufficient number of players are contributing.
4. **Punishment Mechanism:** If `avg_contribution < 0.5`, Defect (D) in the current round, but only if the total contributions from the previous two rounds (`sum_j c_j` over the last two rounds) are below the threshold (`2 * 0.5 * n`). This gradual punishment mechanism allows for occasional mistakes or exploration by other players.
5. **Forgiveness:** If a player defects in the current round, but had cooperated in at least one of the previous two rounds, Cooperate (C) in the next round. This forgiveness mechanism promotes cooperation and encourages players to return to cooperative behavior.

**Edge Cases:**

* Last Round: Defect (D) in the last round, as there are no future interactions to influence.
* Single-Player Game: Always Cooperate (C), as there is no one to free-ride on.
* Zero-Contribution History: If all players have defected in every previous round, Cooperate (C) in the current round to attempt to restart cooperation.

**Collective Mindset:**

This strategy prioritizes cooperation while maintaining a balance between punishing free-riders and forgiving occasional mistakes. By gradually adapting to the group's behavior, it promotes a collective outcome that benefits all players. The forgiveness mechanism encourages cooperation by allowing players to recover from temporary defections, fostering a more cooperative environment.

By playing this strategy in the tournament, I aim to promote a mutually beneficial outcome while being robust against various opponent behaviors.
'''

description_COLLECTIVE_88 = '''
Here's a collective strategy for the repeated Public Goods Game:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a positive tone and encourage cooperation.
2. **Reciprocal Altruism**: For subsequent rounds, calculate the average contribution of all players in the previous round (avg_contrib). If avg_contrib ≥ 0.5, contribute 1 token (C); otherwise, contribute 0 tokens (D).
3. **Punish Free-Riders**: If a player defects (D) while others cooperate (C), identify them as free-riders. In the next round, defect (D) against these players.
4. **Forgiveness**: After punishing a free-rider, return to reciprocal altruism if they start contributing again.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 0 tokens (D), as individual payoffs are maximized by conserving resources.
2. **Tiebreaker**: If avg_contrib = 0.5, break ties by cooperating (C) to maintain a positive tone.
3. **All Defectors**: If all players defect in a round, cooperate (C) in the next round to encourage cooperation.

**Collective Mindset:**

ACO aims to balance individual self-interest with collective welfare. By initially cooperating and reciprocating altruism, ACO fosters a cooperative atmosphere. Punishing free-riders maintains fairness and encourages cooperation, while forgiveness allows for reconciliation. This strategy adapts to various opponent behaviors, promoting a positive feedback loop of cooperation.

**Rationale:**

ACO is designed to be robust against diverse strategies while aligning with the collective mindset. By initially cooperating, ACO sets a positive tone and encourages others to do the same. Reciprocal altruism rewards cooperative behavior, while punishing free-riders maintains fairness. Forgiveness allows for reconciliation, promoting long-term cooperation.

This strategy should perform well in a tournament setting against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_89 = '''
**Collective Strategy: "Adaptive Cooperativity"**

Our collective strategy, Adaptive Cooperativity, aims to balance individual self-interest with the pursuit of collective welfare. We adapt our behavior based on the game's history and parameters.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) unconditionally.
2. **Tit-for-Tat**: For rounds 2-r, cooperate (C) if the majority (>50%) of players cooperated in the previous round; otherwise, defect (D).
3. **Punishment Phase**: If a player defects while others cooperate, enter a punishment phase where you defect for the next θ rounds, where θ = ⌊k/n⌋. After the punishment phase, return to Tit-for-Tat.
4. **Forgiveness**: If a player who was punished starts cooperating again, forgive and re-enter Tit-for-Tat after φ rounds of consistent cooperation, where φ = 2.

**Edge Cases:**

1. **Last Round**: In the final round (r), defect unconditionally (D).
2. **Ties in Cooperation**: When the number of cooperators is exactly equal to half of the total players, cooperate (C).

**Collective Mindset Alignment:**

Adaptive Cooperativity prioritizes cooperation when possible and punishes defectors while allowing for forgiveness and re-entry into cooperative behavior. This strategy promotes a collective mindset by:

* Encouraging initial cooperation to set a positive tone
* Responding to the group's actions, rather than individual players'
* Implementing punishment phases to deter exploitation
* Allowing for forgiveness to prevent perpetual defection

By adapting to the game's history and parameters, Adaptive Cooperativity aims to achieve a balance between individual self-interest and collective welfare, making it a robust strategy in a wide range of opponent behaviors.
'''

description_COLLECTIVE_90 = '''
**Collective Strategy: "Gradual Reciprocity with Adaptive Punishment"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to contribute.
2. **Subsequent Rounds:**
	* If the average contribution of other players in the previous round is above 0.5, cooperate (C).
	* If the average contribution of other players in the previous round is below 0.5, defect (D) with a probability proportional to the deviation from 0.5.
	* If you defected (D) in the previous round and the total contributions increased, cooperate (C) in the current round.
3. **Punishment Mechanism:** If another player defects (D) while you cooperated (C), defect (D) in the next round with a probability of 0.7.

**Edge Case Handling:**

* **Last Round:** Cooperate (C) to maximize collective payoff, as there's no future opportunity for reciprocity.
* **Ties:** In case of a tie in average contribution, cooperate (C) to maintain a cooperative stance.
* **Single Opponent:** If there's only one opponent, cooperate (C) to encourage mutual cooperation.

**Collective Mindset Alignment:**

This strategy prioritizes collective welfare by:
	+ Encouraging cooperation through reciprocity and punishment mechanisms
	+ Adapting to the group's behavior to maintain a balance between individual and collective interests
	+ Avoiding excessive punishment, which could lead to a breakdown in cooperation

**Robustness:**

This strategy is designed to be robust against various opponent behaviors by:

	+ Gradually adjusting its level of cooperation based on the group's behavior
	+ Incorporating an adaptive punishment mechanism to deter exploitation
	+ Maintaining a cooperative stance in edge cases, such as the last round or when facing a single opponent
'''

description_COLLECTIVE_91 = '''
**Collective Strategy: Adaptive Cooperativity with Gradual Punishment**

This strategy balances individual incentives with collective welfare, adapting to the behavior of others while promoting cooperation.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative tone.
2. **Reciprocity**: If the majority (> 50%) of players contributed in the previous round, contribute (C). Otherwise, defect (D).
3. **Gradual Punishment**: If the average contribution rate of other players is below a certain threshold (T = 0.5), gradually decrease your contribution rate by 1/n each round, where n is the number of players.
4. **Forgiveness**: If another player who previously defected now contributes, increase their "forgiveness" score by 1. After 2-3 rounds of consecutive cooperation, reset their punishment level.

**Edge Cases:**

* **Last Round**: In the final round, always defect (D) to maximize individual payoff.
* **Ties**: If there is a tie in contribution rates or forgiveness scores, randomize your action between C and D.
* **All Defect**: If all other players consistently defect, also defect (D) to minimize losses.

**Collective Mindset:**

This strategy aims to:

1. Encourage cooperation through reciprocity and gradual punishment.
2. Adapt to changing environments and behaviors.
3. Balance individual self-interest with collective welfare.

By implementing this strategy, we promote a culture of cooperation while safeguarding against exploitation by defectors.

This adaptive approach will perform well in the tournament against independent strategies, as it effectively responds to various opponent behaviors while maintaining a strong collective focus.
'''

description_COLLECTIVE_92 = '''
**Collective Strategy: Adaptive Cooperative Optimism**

**Decision Rules:**

1. **First Round:** Contribute (C) to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:**
	* If the total contributions in the previous round were at least (n/2), contribute (C). This indicates that enough players are cooperating, making it worthwhile to continue contributing.
	* If the total contributions in the previous round were less than (n/2) but greater than 0, defect (D) with a probability of (1 - (total_contributions / n)). This introduces a gradual decrease in cooperation as others' contributions dwindle.
	* If no one contributed in the previous round, defect (D). This avoids contributing to a clearly uncooperative group.
3. **Last Round:** Contribute (C) if the total contributions in the second-to-last round were at least (n/2), and defect (D) otherwise.

**Handling Edge Cases:**

* If there's only one player, always contribute (C).
* If all players have defected for two consecutive rounds, start contributing (C) again to try to revive cooperation.
* If a player has contributed in every round so far, continue to contribute (C) as long as their contributions are not being exploited.

**Collective Mindset:**

This strategy prioritizes cooperation and adaptability while maintaining a level of robustness against exploitation. By initially contributing and gradually adjusting based on others' actions, the strategy encourages cooperation while protecting against free-riding. The goal is to create an environment where enough players contribute to make cooperation worthwhile for everyone.

**Rationale:**

By starting with a cooperative action, we set a positive tone for the game and encourage other players to follow suit. As the game progresses, our adaptive decision rules allow us to respond to changes in others' behavior, gradually decreasing cooperation if it becomes clear that others are not contributing fairly. The strategy is designed to be robust against a wide range of opponent behaviors while promoting collective welfare through cooperation.
'''

description_COLLECTIVE_93 = '''
Here's a strategic approach to the Public Goods Game:

**Strategy Name: Adaptive Collective Conscience**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) with probability 0.8. This sets a positive tone and encourages others to cooperate.
2. **Reciprocity**: If at least half of the players contributed in the previous round, contribute in this round. Otherwise, defect.
3. **Exploitation Detection**: Monitor the number of rounds where total contributions are less than (k / n) * n / 2. If this occurs more than twice in a row, switch to defection for the next two rounds.
4. **Cooperation Revival**: After two consecutive rounds of defection, reassess the group's cooperation level. If at least half of the players contributed in either of these rounds, resume contributing.
5. **Endgame Cooperation**: In the last three rounds, contribute regardless of previous outcomes. This encourages others to cooperate and maximizes collective payoff.

**Edge Cases:**

* **First Round**: Contribute with probability 0.8 (see Initial Cooperation).
* **Last Round**: Contribute (C) to maximize collective payoff.
* **Early Defection**: If a player defects in the first two rounds, treat them as an exploiter and adjust strategy accordingly.

**Collective Mindset:**

This strategy prioritizes collective welfare by:

1. Encouraging initial cooperation
2. Responding positively to reciprocity
3. Detecting and adapting to exploitation
4. Reviving cooperation when possible
5. Maximizing collective payoff in the endgame

By being adaptive and responsive to the actions of others, this strategy aims to promote a culture of cooperation while protecting against exploitation.

This strategy will play well against various opponent behaviors, as it balances individual self-interest with collective welfare, making it a robust choice for the tournament.
'''

description_COLLECTIVE_94 = '''
Here's a collective strategy for the Public Goods Game (PGG) that adapts to a wide range of opponent behaviors:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C). This sets a positive tone and encourages others to cooperate.
2. **Reciprocity**: If the average contribution in the previous round is above 0.5 tokens, contribute 1 token (C) in the current round. Otherwise, defect (D).
3. **Punishment**: If an opponent defects while you cooperated in the previous round, defect (D) in the current round.
4. **Forgiveness**: If an opponent who defected in the previous round cooperates in the current round, cooperate (C) in the next round.

**Edge Cases:**

1. **Last Round**: In the final round, contribute 0 tokens (D), as there's no future reciprocity to consider.
2. **Opponent Defection Streaks**: If an opponent defects for three consecutive rounds, permanently defect (D) against them.
3. **Global Cooperation**: If all opponents cooperate in a round, continue cooperating (C) until someone defects.

**Collective Mindset:**

ACO prioritizes collective welfare by:

1. Encouraging cooperation through initial and reciprocal contributions.
2. Punishing defectors to maintain fairness and deter exploitation.
3. Forgiving past defections to allow for renewed cooperation.
4. Adapting to opponent behaviors to maximize overall payoffs.

By implementing ACO, we aim to create a robust and adaptive strategy that balances individual incentives with collective welfare in the Public Goods Game.
'''



description_COLLECTIVE_96 = '''
**Collective Strategy: "Adaptive Reciprocity with Conditional Cooperation"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate collective contribution and set a positive tone.
2. **Subsequent Rounds:**
	* If the average contribution of all players in the previous round is above a certain threshold (k/n)/2, Cooperate (C).
	* If the average contribution is below this threshold, Defect (D).
3. **Reciprocity Mechanism:** Track the average contribution of each opponent over time. If an opponent's average contribution is significantly higher than the group's average (above 75th percentile), mirror their last action in the next round.
4. **Punishment Mechanism:** If a player defects (D) when the group's average contribution is above the threshold, Defect (D) in response to that player in the next two rounds.

**Edge Cases:**

* **Last Round:** Cooperate (C) if the group's total contributions are close to or have exceeded the maximum possible payoff ((k/n) \* n). Otherwise, Defect (D).
* **Single Opponent:** In a 1v1 scenario, alternate between C and D to test opponent's behavior and adapt accordingly.

**Collective Mindset:**

This strategy aims to create a self-reinforcing cycle of cooperation by rewarding contributors and punishing free-riders. By cooperating initially and adapting to the group's contribution level, we encourage others to follow suit. The reciprocity mechanism acknowledges and reciprocates generosity from other players, while the punishment mechanism deters exploitation.

**Robustness:**

This strategy is designed to be robust against a wide range of opponent behaviors, including:

* **Free-riders:** Punishment mechanism discourages repeated defection.
* **Cooperative opponents:** Reciprocity mechanism rewards and mirrors cooperation.
* **Mixed strategies:** Adaptive nature allows the strategy to adjust to changing opponent behavior.

This collective strategy balances individual self-interest with collective welfare, promoting cooperation while being robust against exploitation.
'''

description_COLLECTIVE_97 = '''
**Collective Strategy: "Reciprocal Conditional Cooperation"**

This strategy aims to balance individual self-interest with collective welfare, adapting to the behavior of others while promoting cooperation.

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:** Observe the total contributions from the previous round and calculate the average contribution per player (avg_contrib). If avg_contrib is above a certain threshold (k/n), cooperate (C) in the current round. Otherwise, defect (D).
3. **Reciprocity Mechanism:** Monitor the actions of other players and maintain a "reciprocity score" for each opponent. For every round where an opponent cooperates while you also cooperated, increment their reciprocity score by 1. If an opponent defects while you cooperated, decrement their reciprocity score by 2.
4. **Conditional Cooperation:** When making decisions in subsequent rounds, consider the reciprocity scores of all opponents. If a majority (more than half) of opponents have a positive reciprocity score, cooperate (C). Otherwise, defect (D).

**Edge Cases:**

* **Last Round:** Cooperate (C) unconditionally to maximize collective welfare and encourage others to do the same.
* **Opponent Defection Streaks:** If an opponent has defected for more than two consecutive rounds, temporarily switch to a defection strategy (D) against them until they cooperate again.

**Collective Mindset:**

This strategy prioritizes cooperation when there is evidence of reciprocal behavior among opponents. By initially cooperating and adapting to the average contribution level, it encourages others to do the same. The reciprocity mechanism rewards cooperative behavior and discourages exploitation, promoting a collective mindset that balances individual self-interest with group welfare.

**Robustness:**

This strategy remains effective against various opponent behaviors due to its adaptability and conditional cooperation mechanism. It can:

* Encourage cooperation in groups with initially high levels of cooperation
* Gradually adjust to more competitive environments by adapting to average contribution levels
* Identify and respond to exploiters or defectors through the reciprocity mechanism
'''

description_COLLECTIVE_98 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Forgiveness**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline of cooperation and encourage others to follow suit.
2. **Responding to Others' Actions**:
	* If at least half of the players cooperated in the previous round, cooperate (C) in the current round.
	* If less than half cooperated, defect (D) but keep track of the number of consecutive rounds with low cooperation.
3. **Gradual Forgiveness**: After a defection, gradually forgive and revert to cooperation if:
	+ The opponent(s) who defected previously cooperate in the next round.
	+ A sufficient number of rounds have passed since the last defection (e.g., 2-3 rounds).
4. **Punishment for Persistent Defection**: If an opponent defects repeatedly (e.g., more than twice), defect (D) consistently against them to discourage further exploitation.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round, as there is no future opportunity to punish or reward behavior.
2. **Single Opponent**: If there is only one opponent, alternate between cooperation and defection to maintain a balance of power.

**Collective Mindset Alignment:**

This strategy prioritizes collective welfare by initially cooperating and gradually forgiving opponents who cooperate after a defection. By responding to the majority's actions, it encourages others to cooperate while being robust against exploitation. By punishing persistent defectors, it maintains a balance of power and discourages free-riding.

**Adaptability and Robustness:**

This strategy adapts to various opponent behaviors by adjusting its response based on the collective action in previous rounds. It is robust against different types of opponents, including those who cooperate, defect, or alternate between strategies.
'''

description_COLLECTIVE_99 = '''
**Collective Strategy: Adaptive Cooperative Optimism (ACO)**

In the Public Goods Game, our collective strategy, ACO, balances individual self-interest with collective welfare. We adapt to the group's behavior and adjust our cooperation level accordingly.

**Initial Round**
In the first round, all players contribute 1 token (C). This sets a positive tone for the game and encourages others to cooperate.

**General Decision Rule**
After each round, calculate the **Cooperation Rate (CR)**: the average number of tokens contributed by all players in the previous round. If CR is above a threshold (T), we contribute 1 token (C); otherwise, we contribute 0 tokens (D). The threshold T is set to 0.5.

**Adaptive Mechanism**
If our payoff in the previous round was below a certain percentage (P) of the maximum possible payoff, we decrease our contribution by 1 token in the next round. Conversely, if our payoff was above P% of the maximum payoff, we increase our contribution by 1 token. This adapts our cooperation level based on individual performance.

**Edge Cases**

* **Last Round**: In the final round, contribute 1 token (C) to maximize collective welfare.
* **Early Defection**: If a player defects in an early round, respond with defection in the next round.
* **Punishment Phase**: If a majority of players defect, introduce a brief punishment phase where all ACO players defect for one round.

**Collective Mindset**
ACO prioritizes cooperation when the group's behavior indicates a willingness to contribute. By adapting to the Cooperation Rate and individual performance, we balance self-interest with collective welfare. This encourages others to cooperate, fostering a positive feedback loop that benefits everyone.

**Robustness**
ACO is robust against various opponent behaviors:

* **Defectors**: ACO responds to defection by decreasing cooperation, preventing exploitation.
* **Cooperators**: ACO reinforces cooperation when the group's Cooperation Rate is high.
* **Mixed Strategies**: ACO adapts to changing behavior, minimizing losses and maximizing gains.

By adopting ACO, we create a collective strategy that promotes cooperation while protecting individual interests. This fosters a collaborative environment, leading to improved overall payoffs in the Public Goods Game.
'''

description_COLLECTIVE_100 = '''
**Collective Strategy: "Adaptive Reciprocal Altruism"**

Our strategy, Adaptive Reciprocal Altruism (ARA), balances individual self-interest with collective welfare by adapting to the group's behavior over time. ARA aims to promote cooperation while being robust against exploitation.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Cooperation**: If the average contribution in the previous round is above 0.5 tokens, contribute 1 token (C). This encourages cooperation when others are contributing.
3. **Gradual Retaliation**: If the average contribution in the previous round is below 0.5 tokens, decrease your contribution by 0.25 tokens compared to the previous round, but never defect completely (i.e., always contribute at least 0.25 tokens). This introduces a gradual response to decreased cooperation.
4. **Punish Defection**: If the average contribution in the previous round is exactly 0 tokens, defect (D) for one round to punish complete non-cooperation. Then, revert to the Reciprocal Cooperation rule.

**Edge Cases:**

* In the last round, contribute 1 token (C) regardless of the group's behavior, as there are no future interactions.
* If all players defected in the previous round, and you punished them by defecting, return to Initial Cooperation in the next round.

**Collective Mindset Alignment:**

ARA promotes cooperation while being adaptive to the group's behavior. By reciprocating cooperation and gradually retaliating against decreased contributions, ARA encourages a collective mindset of mutual support. The strategy is designed to be robust against exploitation by not allowing complete defection to go unpunished.

By playing ARA in the tournament, we aim to demonstrate that a balanced approach to cooperation and self-interest can lead to better outcomes for all players in the Public Goods Game.
'''

description_COLLECTIVE_101 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Retaliation"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to contribute.
2. **Subsequent Rounds**: Observe the total contributions and average payoff of all players in the previous round. If:
	* The average payoff is above a certain threshold (e.g., 1.5 * (k / n)), Cooperate (C) to maintain the high collective welfare.
	* The average payoff is below the threshold, but there are some contributors, Gradually Retaliate by Defecting (D) with a probability p = (number of defectors in previous round) / n. This gradual retaliation aims to punish non-cooperators while avoiding mutual defection.
	* Everyone Defected (D) in the previous round, Cooperate (C) to attempt to restart cooperation.
3. **Contribution Threshold**: If the total contributions in the previous round are below a certain threshold (e.g., 0.5 * n), Defect (D) to minimize losses.

**Edge Cases:**

1. **Last Round**: In the final round, Cooperate (C) if the game has been cooperative overall; otherwise, Defect (D).
2. **Single Player**: If there is only one player, always Cooperate (C) as there are no free riders to punish.
3. **All Players but One Defected**: If all players but one Defected (D), and that one player Contributed (C), Cooperate (C) in the next round to reward their cooperation.

**Collective Mindset:**

This strategy prioritizes collective welfare by cooperating when others contribute and punishing non-cooperators with gradual retaliation. By adapting to the game's history, it balances individual incentives with the need for collective cooperation. The strategy is robust against a wide range of opponent behaviors, as it responds to the overall level of cooperation rather than specific actions.

**Rationale:**

This strategy aims to achieve a balance between cooperation and punishment. By initially cooperating and then adapting to the game's history, it encourages others to contribute while minimizing losses when faced with non-cooperation. The gradual retaliation mechanism helps maintain cooperation without leading to mutual defection.
'''

description_COLLECTIVE_102 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone and encourage others to follow.
2. **Reciprocal Altruism**: For rounds 2 to r-1, contribute 1 token (C) if at least 50% of players contributed in the previous round. Otherwise, defect (D).
3. **Gradual Escalation**: If fewer than 50% of players contributed in the previous round, reduce contributions by 1 token every subsequent round until all players defect or a single player contributes.
4. **Punishment and Forgiveness**: If another player defects while you cooperated, switch to defection (D) for one round as punishment. However, if that player subsequently cooperates, forgive and revert to cooperation (C).
5. **Last Round Exception**: In the final round (r), always defect (D) regardless of previous actions.

**Edge Cases:**

1. **Tiebreaker**: If exactly 50% of players contributed in the previous round, contribute 1 token (C) to maintain a cooperative atmosphere.
2. **Unanimous Defection**: If all players defected in the previous round, defect (D) in the next round to avoid exploitation.

**Collective Mindset:**

ACO prioritizes collective welfare by adapting to the group's behavior and promoting cooperation when possible. By initially cooperating and gradually escalating defections, ACO encourages others to cooperate while minimizing losses from exploitative players. The punishment and forgiveness mechanisms help maintain a balance between cooperation and self-interest.

This strategy is designed to be robust against various opponent behaviors and can adapt to different game parameters (e.g., number of players, rounds, and multiplier). By playing ACO in the tournament, you'll promote collective optimism while protecting individual interests.
'''

description_COLLECTIVE_103 = '''
Here's a collective strategy for the Public Goods Game (PGG) that adapts to a wide range of opponent behaviors:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) with probability 0.8 and defect (D) with probability 0.2. This initial cooperation encourages others to cooperate while allowing for some exploration.
2. **Reciprocal Cooperation**: If the total contribution in the previous round is above the average contribution threshold (ACT), contribute 1 token (C). ACT is calculated as (k / n) \* (n - 1).
3. **Gradual Retaliation**: If the total contribution in the previous round is below ACT, defect (D) with a probability proportional to the difference between the actual contribution and ACT.
4. **Forgiveness**: After two consecutive rounds of cooperation, reset the retaliation mechanism.

**Edge Cases:**

* Last Round: Contribute 1 token (C), as there's no future reciprocity to worry about.
* Early Rounds (<5): Apply the initial cooperation rule with a higher probability of cooperating (0.9).
* Late Rounds (> r - 5): Gradually increase the retaliation threshold by 10% every round to adapt to changing opponent behaviors.

**Collective Mindset:**

ACO prioritizes collective welfare while adapting to individual behaviors. By initially cooperating and reciprocating cooperation, we encourage others to contribute to the public good. The gradual retaliation mechanism responds to free-riding without escalating conflicts. Forgiveness allows for renewed cooperation after periods of mutual defection.

By playing ACO, our strategy balances individual self-interest with collective benefits, promoting a stable and cooperative environment in the Public Goods Game.
'''

description_COLLECTIVE_104 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

This strategy balances individual incentives with collective welfare, adapting to the behavior of others while maintaining a robust and cooperative approach.

**Decision Rules:**

1. **First Round:** Cooperate (C) - Contribute 1 token to establish a positive tone for the game.
2. **Subsequent Rounds:** Use the following logic:
	* If the average contribution of all players in the previous round is above 0.5, Cooperate (C).
	* Otherwise, Defect (D) with a probability p, where p increases by 0.1 each time the average contribution falls below 0.5.
3. **Punishment Phase:** If a player defects while others cooperate, reduce their reputation score (see below). This score affects future interactions.

**Reputation Score:**

Maintain a reputation score for each opponent, initially set to 1. Update this score based on their behavior:

* If an opponent cooperates while you cooperate, increase their reputation score by 0.05.
* If an opponent defects while you cooperate, decrease their reputation score by 0.1.

**Edge Cases:**

* **Last Round:** Cooperate (C) if the average contribution in the previous round is above 0.5; otherwise, Defect (D).
* **Opponent's First Round:** Ignore their action and focus on your own strategy.
* **Repeated Defection:** If an opponent defects for three consecutive rounds, Defect (D) against them until they cooperate.

**Collective Mindset:**

This strategy prioritizes cooperation while gradually punishing repeated defection. By adapting to the behavior of others, we promote a culture of mutual support and deter exploitation. In a tournament setting, this approach will encourage other strategies to cooperate, ultimately benefiting all players involved.

By aligning with the collective mindset, our strategy ensures that individual interests are balanced with the greater good, fostering a cooperative environment in which everyone can thrive.
'''

description_COLLECTIVE_105 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Punishment"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to do the same.
2. **Subsequent Rounds:**
	* If the total contributions in the previous round are greater than or equal to half of the total possible contributions (n/2), cooperate (C). This indicates a strong collective effort, and we want to reinforce it.
	* If the total contributions in the previous round are less than half of the total possible contributions (n/2) but greater than 0, defect (D) with a probability proportional to the difference between the actual contributions and n/2. This gradual punishment aims to discourage free-riding while still allowing for some cooperation.
	* If no one contributed in the previous round (total contributions = 0), cooperate (C) to try to revive collective efforts.
3. **Last Round:** Defect (D) as there are no future rounds to consider, and individual payoffs take precedence.

**Edge Cases:**

* **Single Player:** Always cooperate (C), as there's no one to free-ride off of.
* **Two Players:** Alternate between cooperation (C) and defection (D) to maintain a balance between individual and collective interests.
* **Ties:** In case of ties in total contributions, follow the decision rule for the previous round.

**Collective Mindset:**

This strategy prioritizes cooperation when collective efforts are strong and gradually punishes free-riding when contributions dwindle. By adapting to the group's behavior, we aim to create a self-sustaining cycle of cooperation that benefits everyone involved.

By using this adaptive approach, our strategy balances individual interests with collective welfare, making it a robust contender in the tournament against various opponent behaviors.
'''

description_COLLECTIVE_106 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a baseline for reciprocity and encourage others to contribute.
2. **Subsequent Rounds:** Observe the average contribution rate of all players in the previous round, denoted as `avg_contribution`. If `avg_contribution` is above a certain threshold (`cooperation_threshold`, set to 0.5), cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** Introduce a gradual punishment mechanism to deter defectors. Track the number of consecutive rounds where the average contribution rate falls below `cooperation_threshold`. If this count exceeds a certain threshold (`punishment_threshold`, set to 2), defect (D) for one round to signal dissatisfaction with the current cooperation level.
4. **Reciprocity:** After punishing, return to cooperating (C) if `avg_contribution` rises above `cooperation_threshold`.

**Edge Cases:**

* **Last Round:** Cooperate (C) to maintain a positive reputation and encourage others to do the same.
* **Single-Defector Scenario:** If only one player defects in a round, cooperate (C) in the next round to avoid unnecessary conflict.

**Collective Mindset Alignment:**

This strategy prioritizes cooperation while adapting to the group's behavior. By cooperating initially and gradually punishing defectors, we encourage others to contribute, ensuring the collective benefit is maximized. The punishment mechanism prevents exploitation by those who would otherwise take advantage of cooperative players.

**Rationale:**

By making decisions based on the average contribution rate, this strategy promotes a collective understanding of cooperation levels. Gradual punishment discourages consistent defection without inducing unnecessary conflict or retaliatory behavior. This approach balances individual incentives with collective welfare, fostering an adaptive and robust cooperation environment.
'''

description_COLLECTIVE_107 = '''
**Strategy Name: Adaptive Collective Conscience (ACC)**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to set a cooperative tone and encourage others to follow.
2. **Contribution Threshold:** In subsequent rounds, cooperate if the total contributions from all players in the previous round exceed a threshold of `(n-1)/k`, where `n` is the number of players and `k` is the multiplier. This ensures that the collective benefit is substantial enough to warrant cooperation.
3. **Reciprocity:** Cooperate if at least half of the players cooperated in the previous round, regardless of the contribution threshold. This encourages reciprocal behavior and maintains a cooperative atmosphere.
4. **Punishment:** Defect (D) if more than half of the players defected in the previous round. This punishes non-cooperative behavior and discourages free-riding.
5. **Exploitation Prevention:** If a player has consistently defected (more than 75% of the time), defect against them, even if the contribution threshold or reciprocity conditions are met.

**Edge Cases:**

1. **Last Round:** Cooperate in the last round, as there is no future opportunity for reciprocation.
2. **Solo Play:** If only one player remains, cooperate to maximize the collective benefit.
3. **Tiebreaker:** In cases where multiple strategies are tied (e.g., equal number of cooperators and defectors), prioritize cooperation.

**Collective Mindset:**

ACC prioritizes cooperation while adapting to the actions of other players. By setting a cooperative tone in the initial round and reciprocating cooperative behavior, ACC encourages others to contribute to the collective good. The strategy's adaptive nature allows it to respond effectively to various opponent behaviors, making it robust and competitive in a tournament setting.

**Additional Considerations:**

* **Learning:** As the game progresses, ACC can learn from the actions of other players and adjust its decision rules accordingly.
* **Flexibility:** While ACC is designed as a collective strategy, it can be modified to accommodate different play styles or specific opponent behaviors.
'''

description_COLLECTIVE_108 = '''
**Collective Strategy: "Adaptive Reciprocity with Gradual Escalation"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocate Past Contributions**: For rounds 2+, calculate the average contribution of all players in the previous round (avg_c). If avg_c ≥ 0.5, contribute 1 token (C); otherwise, contribute 0 tokens (D).
3. **Gradual Escalation**: Track the number of consecutive rounds where the group's total contributions are below a certain threshold (e.g., n/2). If this count exceeds a patience parameter (p), switch to contributing 0 tokens (D) for a set number of rounds (e.g., p+1).
4. **Forgiveness and Restart**: After a Gradual Escalation phase, reset the contribution strategy to Initial Cooperation if the group's total contributions exceed the threshold in two consecutive rounds.

**Handling Edge Cases:**

* In the last round, contribute 0 tokens (D) as there is no future opportunity for reciprocity.
* If all players have defected in a previous round, restart with Initial Cooperation in the next round to reestablish potential cooperation.
* In cases of tie or identical payoffs, prioritize contributing 1 token (C).

**Collective Mindset:**

This strategy aligns with a collective mindset by initially promoting cooperation and reciprocating contributions. It adapts to the group's behavior, gradually escalating defection when faced with insufficient cooperation. By restarting cooperation after Gradual Escalation phases, it encourages the group to reassess their strategy and work towards mutual benefit.

**Robustness:**

This strategy is robust against a wide range of opponent behaviors:

* **Defectors**: Gradual Escalation responds to chronic defection by withholding contributions.
* **Free Riders**: Reciprocate Past Contributions ensures that players who consistently contribute are rewarded.
* **Cooperators**: The strategy reciprocates cooperation and adapts to maintain group welfare.

By combining these elements, "Adaptive Reciprocity with Gradual Escalation" provides a collective strategy for the Public Goods Game that balances individual incentives with collective welfare.
'''

description_COLLECTIVE_109 = '''
**Collective Strategy: "Conditional Contribute with Gradual Forgiveness"**

This strategy aims to balance individual incentives with collective welfare, adapting to the behavior of other players in the game.

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a baseline level of contribution and encourage others to follow suit.
2. **Rounds 2-5:** Cooperate if at least 50% of players contributed in the previous round; otherwise, Defect (D).
3. **Rounds 6+:** Implement "Gradual Forgiveness":
	* If the total contributions in the previous round are above the average contribution level for the past three rounds, Cooperate.
	* If the total contributions in the previous round are at or below the average contribution level for the past three rounds, Defect.

**Edge Cases:**

1. **Last Round:** Defect to maximize individual payoff, as there is no future game to consider.
2. **Single Opponent:** Cooperate if the opponent contributed in the previous round; otherwise, Defect.
3. **Multiple Opponents with Similar Behavior:** If multiple opponents consistently contribute or defect, adjust the decision rule to match their behavior (Cooperate if they Cooperate, Defect if they Defect).

**Collective Mindset:**

1. **Encourage Cooperation:** By contributing in early rounds and responding positively to others' contributions, this strategy promotes a cooperative atmosphere.
2. **Gradual Forgiveness:** This mechanism allows the strategy to adapt to changes in opponent behavior and forgive occasional defections, maintaining a collective focus on cooperation.

**Adaptability:**

This strategy can handle various opponent behaviors by:

1. Responding to changes in contribution levels
2. Adapting to different numbers of opponents with similar behavior

By employing "Conditional Contribute with Gradual Forgiveness," this collective strategy balances individual incentives with collective welfare, promoting cooperation and adaptability in the repeated Public Goods Game.
'''

description_COLLECTIVE_110 = '''
**Collective Strategy: "Adaptive Collective Cooperation" (ACC)**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:** Observe the previous round's total contributions and calculate the average contribution per player (`avg_contribution = sum_j c_j / n`).
3. **Cooperation Threshold:** If `avg_contribution` is above a certain threshold (e.g., 0.5), Cooperate (C) in the current round. Otherwise, Defect (D).
4. **Punishment Mechanism:** If a player has defected in the previous round and the average contribution was below the threshold, Defect (D) in the current round to punish the non-cooperative behavior.
5. **Forgiveness:** After punishing a player, return to Cooperating (C) if the average contribution exceeds the threshold.

**Edge Cases:**

* **Last Round:** In the final round, Cooperate (C) regardless of previous actions to maximize collective welfare.
* **Single Player Deviation:** If only one player deviates from cooperation, maintain Cooperation (C) for two rounds before applying the Punishment Mechanism.
* **Multiple Players Deviate:** If multiple players deviate simultaneously, apply the Punishment Mechanism immediately.

**Collective Mindset:**

The ACC strategy prioritizes collective welfare by cooperating when others do and punishing non-cooperative behavior. By adapting to the average contribution level, it promotes a balanced approach that encourages cooperation while discouraging exploitation. Forgiveness allows for recovery from punishment phases, promoting long-term cooperation.

This strategy balances individual incentives with collective well-being, making it robust against various opponent behaviors in the Public Goods Game tournament.
'''

description_COLLECTIVE_111 = '''
**Collective Strategy: "Adaptive Reciprocity with Collective Optimism"**

**Decision Rules:**

1. **First Round:** Contribute 1 token (C) to establish a cooperative tone and encourage others to follow.
2. **Subsequent Rounds:**
	* If the total contributions in the previous round were ≥ (n-1)/k, contribute 1 token (C). This indicates that the group is collectively doing well, and we should continue to cooperate.
	* Otherwise, if the number of contributors in the previous round was > (n/2), contribute 0 tokens (D) with probability p = 0.5, and 1 token (C) otherwise. This introduces a degree of uncertainty while still considering the collective behavior.
	* If the number of contributors in the previous round was ≤ (n/2), contribute 0 tokens (D). This suggests that cooperation is not prevalent, and we should defect to avoid exploitation.
3. **Reciprocity Mechanism:** Keep track of each player's past actions. For players who have contributed at least as much as the group average in the previous rounds, increase the probability of contributing 1 token (C) by 10% in the current round.

**Edge Cases:**

* Last Round: Contribute 0 tokens (D), as there are no future rounds to influence.
* When a player has contributed 0 tokens (D) for two consecutive rounds, treat them as a defector and adjust the reciprocity mechanism accordingly.

**Collective Mindset:**
This strategy balances individual self-interest with collective welfare by:

1. Encouraging cooperation in early rounds to establish a positive tone.
2. Adapting to the group's overall behavior while considering individual contributions.
3. Introducing randomness to avoid being exploited and maintain a level of uncertainty.

By following this adaptive and robust strategy, we aim to promote cooperation while protecting ourselves from exploitation, ultimately achieving a better collective outcome in the Public Goods Game tournament.
'''

description_COLLECTIVE_112 = '''
**Strategy: Adaptive Collective Optimism**

**Overview**
Our collective strategy, Adaptive Collective Optimism, aims to balance individual self-interest with the desire for collective welfare. We adapt our behavior based on past contributions and payoffs, gradually increasing cooperation as others cooperate.

**Decision Rules**

1. **First Round**: Cooperate (C) - Start by contributing 1 token to encourage initial collective investment.
2. **Subsequent Rounds**: 
   * If total contributions in the previous round exceeded the average contribution threshold (k/n), Cooperate (C).
   * Otherwise, if the majority (>50%) of players contributed, Cooperate (C) with probability proportional to the number of contributors (i.e., more likely to cooperate as others do).
   * In all other cases, Defect (D).
3. **Last Round**: Cooperate (C) only if the total contributions in the previous round exceeded the average contribution threshold (k/n). Otherwise, Defect (D).

**Edge Cases**

* If a player defects consecutively for two rounds, we assume they won't contribute and defect accordingly.
* If all players have defected for two consecutive rounds, we reset our strategy to Cooperate in the next round.

**Collective Mindset**
Our strategy prioritizes collective welfare by:
* Encouraging initial contributions through cooperation
* Adapting cooperation levels based on past contributions
* Gradually increasing cooperation as others contribute

By doing so, we create an environment where individual self-interest aligns with collective benefits, promoting a mutually beneficial outcome.

**Robustness**
This strategy is robust against various opponent behaviors:
* **Free Riders**: By adapting our contribution level based on the majority's behavior, we minimize exploitation.
* **Pure Cooperators**: We reciprocate cooperation to maintain collective welfare.
* **Mixed Strategies**: Our adaptive approach allows us to adjust our behavior in response to changing opponent strategies.

By adopting Adaptive Collective Optimism, our strategy balances individual incentives with collective benefits, promoting a cooperative environment that maximizes overall payoffs.
'''

description_COLLECTIVE_113 = '''
**Collective Strategy: "Adaptive Reciprocity with Collective Optimism"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to signal willingness to contribute to the collective good.
2. **Subsequent Rounds**:
	* If the total contributions in the previous round exceeded 50% of the maximum possible contributions (n), cooperate (C).
	* Otherwise, defect (D) with a probability p = (k/n) * average_contribution_last_round, where average_contribution_last_round is the average contribution of all players in the last round.
3. **Response to Defection**: If at least one player defected in the previous round, and the total contributions were below 50% of the maximum possible contributions, defect (D) with a probability p = (k/n) * number_of_defectors_last_round / n.

**Edge Cases:**

1. **Last Round**: Cooperate (C) to ensure maximal collective payoff.
2. **Single Player Remaining**: Always cooperate (C), as there's no incentive to defect when only one player remains.

**Collective Mindset Alignment:**

This strategy balances individual self-interest with the need for cooperation to achieve a higher collective payoff. By initially cooperating and then adapting to the group's behavior, it encourages others to contribute while also responding to defections in a reasonable manner. The strategy aims to create a "collective optimism" by rewarding cooperative behavior and punishing excessive defection.

**Rationale:**

1. **Initial Cooperation**: Encourages other players to cooperate and sets a positive tone for the game.
2. **Adaptive Reciprocity**: Responds to the group's behavior, increasing cooperation when others contribute and decreasing it when they don't.
3. **Collective Optimism**: Fosters an environment where cooperation is seen as beneficial, even if not all players cooperate.

This strategy should perform well in a tournament setting against independent strategies, as it balances individual self-interest with collective welfare while adapting to various opponent behaviors.
'''

description_COLLECTIVE_114 = '''
**Collective Strategy: "Gradual Reciprocity with Forgiveness"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Response**: Observe the total contributions in the previous round. If the average contribution is above 0.5 tokens, contribute 1 token (C) in the current round. Otherwise, contribute 0 tokens (D).
3. **Forgiveness Mechanism**: After a defection (D), wait for one round before reciprocating with cooperation (C) if the average contribution in the previous round is above 0.5 tokens.
4. **Punishment**: If another player defects (D) while you cooperated (C) in the same round, defect (D) in the next round.

**Edge Cases:**

1. **Last Round**: Contribute 1 token (C) to maintain cooperation and potentially benefit from others' contributions.
2. **Single-Player Deviation**: If only one player defects (D), forgive them after two rounds of cooperation (CC) if their contribution in the third round is 1 token (C).
3. **Multiple Players Defect**: If multiple players defect, apply the punishment rule and wait for a round before re-evaluating reciprocity.

**Collective Mindset:**

This strategy prioritizes collective welfare by initially cooperating and gradually adapting to others' behaviors. By reciprocating cooperation and forgiving occasional defections, it encourages mutual benefit and maintains a high level of cooperation. The punishment mechanism ensures that free-riders are discouraged from exploiting the group's generosity.

By being adaptive and robust to various opponent behaviors, this collective strategy aims to perform well in the tournament against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_115 = '''
**Collective Strategy: "Gradual Reciprocity with Forgiveness"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Reciprocal Response**: For rounds 2 to r-1, observe the total contributions of all players in the previous round. If the average contribution is above 0.5 tokens, contribute 1 token (C). Otherwise, defect (D).
3. **Gradual Adjustment**: Adjust the cooperation threshold based on the game's history. After each round, calculate the moving average of total contributions over the last 3 rounds (or all rounds if fewer than 3 have passed). If this average is above 0.5 tokens, increase the cooperation threshold by 0.1 tokens. If it falls below 0.4 tokens, decrease the threshold by 0.1 tokens.
4. **Forgiveness Mechanism**: If a player defects (D) in a round where they were expected to cooperate (C), reduce their contribution expectation for the next round by 0.2 tokens. However, if this player cooperates (C) in the subsequent round, reset their expectation to the original threshold.
5. **Endgame Strategy**: In the final round (r), contribute 1 token (C) regardless of the game's history.

**Edge Cases:**

* If there is only one player, always cooperate (C).
* If there are only two players, defect (D) in all rounds except the first and last.
* If a player observes that another player has defected consistently (i.e., more than 75% of the time), adjust their expectation for that player to always defect.

**Collective Mindset:**

This strategy promotes cooperation by reciprocating others' contributions while gradually adapting to changes in the group's behavior. By forgiving occasional defections, it encourages players to cooperate and rewards consistent contributors. The endgame strategy ensures a final cooperative act, even if individual payoffs are low, to maintain a collective mindset.

This strategy is robust against various opponent behaviors, including unconditional cooperators, defectors, and tit-for-tat strategies. Its adaptability allows it to adjust to changing game conditions, while its forgiveness mechanism prevents escalating conflicts.
'''

description_COLLECTIVE_116 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Forgiveness"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds:** Observe the total contributions from the previous round. If the total is above a threshold (k/2), cooperate (C). Otherwise, defect (D).
3. **Reaction to Defection:** If another player defects in the current round, reduce cooperation by 1 token in the next round. However, if that player cooperates in the subsequent round, return to full cooperation.
4. **Forgiveness Mechanism:** After two consecutive rounds of cooperation from a previously defecting player, forgive and reset cooperation to its initial level.

**Edge Cases:**

* **Last Round:** Cooperate (C) regardless of the game state, as there is no future opportunity for reciprocity.
* **Single Player Deviation:** If only one player defects in a round, treat it as an isolated incident and continue cooperating. However, if multiple players defect, reassess cooperation levels accordingly.

**Collective Mindset:**

This strategy prioritizes collective welfare by initially cooperating and encouraging others to do the same. By gradually reducing cooperation in response to defection, it adapts to the game's dynamics while maintaining a willingness to forgive and reset cooperation when opponents demonstrate improved behavior. The forgiveness mechanism helps to prevent escalating punishment cycles, promoting a more cooperative environment.

**Rationale:**

By combining initial cooperation with adaptive responses to defection, this strategy balances individual self-interest with collective benefits. Gradual forgiveness encourages cooperation by providing opportunities for redemption, reducing the likelihood of mutual defection and promoting a more sustainable collective outcome.
'''

description_COLLECTIVE_117 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone and encourage others to follow suit.
2. **Reciprocal Altruism**: If the total contributions in the previous round are greater than or equal to half of the total endowments, contribute 1 token (C) in the current round. This encourages continued cooperation when others have shown willingness to contribute.
3. **Punish Defection**: If the total contributions in the previous round are less than half of the total endowments, defect (D) in the current round. This discourages exploitation by other players.
4. **Forgiveness and Re-entry**: If a player defected in the previous round but contributed in the round before that, re-enter cooperation (C) if at least one other player cooperated in the previous round. This allows for occasional mistakes or temporary deviations from cooperation.

**Handling Edge Cases:**

* Last Round: In the final round, always defect (D), as there are no future rounds to consider.
* Single-Player Deviation: If only one player deviates, maintain cooperation (C) unless the deviation is repeated in subsequent rounds.
* Multiple Players Deviate: Gradually decrease contributions over a few rounds if multiple players continue to defect.

**Collective Mindset Alignment:**

ACO prioritizes collective welfare by initially cooperating and reciprocating altruism. It also incorporates punishment mechanisms to deter exploitation, while allowing for forgiveness and re-entry to maintain cooperation. This strategy balances individual self-interest with collective benefits, promoting a mutually beneficial outcome.

This adaptive approach responds to the game's history and opponent behaviors, making it robust in a wide range of scenarios.
'''

description_COLLECTIVE_118 = '''
**Collective Strategy: "Adaptive Cooperative Catalyst"**

This strategy aims to balance individual and collective interests, encouraging cooperation while being robust to various opponent behaviors. It uses a combination of conditional cooperation, reciprocity, and exploration to achieve this goal.

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate the game with a positive contribution.
2. **General Case:** Observe the total contributions from all players in the previous round. If:
	* Total contributions ≥ 0.5n, cooperate (C). This indicates sufficient collective cooperation.
	* Total contributions < 0.5n, defect (D) if you cooperated in the previous round and your payoff was lower than the average payoff; otherwise, cooperate (C).
3. **Reciprocity Mechanism:** If a player has defected (D) more than twice in the last five rounds, defect (D) against them in the current round.
4. **Exploration Phase:** Every 5th round, randomly choose to cooperate (C) or defect (D) with probability 0.5.

**Edge Cases:**

1. **Last Round:** Cooperate (C) if the game has been cooperative overall; otherwise, defect (D).
2. **Tie-Breaking:** In case of equal total contributions, use a random choice between cooperation and defection.

**Collective Mindset:**

This strategy prioritizes collective welfare by cooperating when others do so and reciprocating good behavior. It also uses exploration to test the waters and adapt to changing circumstances. By being willing to cooperate in the first round and under certain conditions, this strategy aims to catalyze cooperation among players.

**Robustness:**

This strategy is designed to perform well against a variety of opponent behaviors:

* **Pure Cooperators:** Will reciprocate their cooperation.
* **Pure Defectors:** Will defect after an initial phase of cooperation.
* **Reciprocating Players:** Will cooperate and respond to cooperative signals.
* **Exploratory Players:** Will adapt through exploration phases.

This strategy balances individual interests with collective well-being, making it a robust choice for the Public Goods Game.
'''

description_COLLECTIVE_119 = '''
Here is a collective strategy for the Public Goods Game that meets the requirements:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocity**: If at least one other player contributed in the previous round, contribute 1 token (C) in the current round.
3. **Punishment**: If no other players contributed in the previous round, defect (D) in the current round.
4. **Optimism Threshold**: If the total contributions in the previous round exceed a threshold (k/2), contribute 1 token (C) in the current round, regardless of others' actions.

**Edge Cases:**

* **Last Round**: In the final round, defect (D) to maximize individual payoff.
* **Tiebreaker**: If multiple players are tied for the highest total contributions at the end of a round, prioritize contributing 1 token (C) in the next round.
* **No Contributions**: If no player has contributed in any previous round, cooperate (C) in the current round.

**Collective Mindset:**

ACO aims to balance individual self-interest with collective welfare. By initially cooperating and reciprocating cooperation, ACO encourages others to contribute. The optimism threshold allows for adaptability to changing group dynamics. Punishment mechanisms deter free-riding while avoiding unnecessary conflict.

By playing ACO in the tournament, this strategy will demonstrate a robust and adaptive approach that balances individual incentives with collective welfare, without relying on shared norms or coordination.
'''

description_COLLECTIVE_120 = '''
**Collective Strategy: "Adaptive Cooperate-to-Thrive"**

Our collective strategy, Adaptive Cooperate-to-Thrive (ACT), aims to balance individual self-interest with collective welfare. We prioritize cooperation while being robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) unconditionally to establish a cooperative tone and encourage mutual investment in the public good.
2. **Reciprocity-based Adaptation**: After the first round, observe the total contributions from all players in the previous round. If the average contribution is above 0.5 tokens, continue cooperating (C). Otherwise, defect (D) with probability p = 1 - (average_contribution / n), where n is the number of players.
3. **Exploitation Protection**: Monitor individual opponents' behavior over time. If an opponent defects (D) more than 50% of the time, mark them as "exploiter" and defect (D) against them in subsequent rounds.

**Edge Cases:**

1. **Last Round**: Cooperate (C) unconditionally to maximize collective welfare, regardless of opponents' past behavior.
2. **Single Opponent or Small Group Size**: If n ≤ 3, always cooperate (C), as the potential gains from cooperation outweigh individual losses.
3. **Identical Opponents**: When facing identical strategies or synchronized behavior, adapt by mirroring their actions (cooperate if they cooperate, defect if they defect).

**Collective Mindset Alignment:**

ACT prioritizes collective welfare while protecting against exploitation. By initially cooperating and adapting to opponents' behavior, we foster a cooperative environment that benefits all players.

This strategy should perform well in the tournament as it balances cooperation with self-protection, making it robust to various opponent behaviors.
'''

description_COLLECTIVE_121 = '''
**Collective Strategy: Adaptive Cooperation with Gradualism**

This strategy balances individual self-interest with collective welfare, adapting to opponents' behaviors while promoting cooperation. It relies solely on game parameters and history.

**Decision Rules:**

1. **Initial Rounds (r ≤ 3):** Cooperate (C) unconditionally to foster a cooperative environment.
2. **Assessing Opponent Behavior:** After the initial rounds, assess each opponent's contribution frequency (CF) as the ratio of their total contributions to the number of rounds played.
3. **Cooperation Threshold:** Set a cooperation threshold (CT) equal to the average CF among all opponents in the previous round.
4. **Adaptive Cooperation:** In subsequent rounds, Cooperate (C) if:
	* Your own contribution frequency is above or equal to CT and at least one opponent has contributed in the previous round.
	* You have defected (D) in the previous round, but your CF remains above or equal to CT.
5. **Gradualism:** If you have cooperated (C) for two consecutive rounds and no opponent has contributed in either of those rounds, Defect (D) in the next round.
6. **Last Round (r = R):** Cooperate (C) if at least one opponent has contributed in any previous round.

**Edge Cases:**

* If all opponents have defected in every round, Defect (D) from the second round onwards.
* In case of a tie in CT calculation, prefer cooperation to ensure a marginally cooperative environment.

This strategy aims to create an atmosphere conducive to collective welfare while being cautious about exploitation. By gradually adapting to the contributions of others and maintaining a balanced approach, it encourages cooperation without assuming shared norms or coordination with opponents.
'''

description_COLLECTIVE_122 = '''
**Collective Strategy: "Adaptive Cooperation with Gradual Punishment"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow.
2. **Reciprocal Cooperation**: If the total contributions from all players in the previous round are greater than or equal to half of the maximum possible contributions, cooperate (C) in the current round. This promotes cooperation when it's beneficial for the group.
3. **Gradual Punishment**: If the total contributions from all players in the previous round are less than half of the maximum possible contributions:
	* If the number of rounds played is less than or equal to n/2 (where n is the number of players), cooperate (C) with a probability of 0.5.
	* Otherwise, defect (D).
4. **Imitation**: If a player has defected (D) in any previous round and their payoff was higher than the average payoff of all players in that round, imitate their action (defect or cooperate) from the last round with a probability of 0.7.
5. **Forgiveness**: If a player has cooperated (C) in every round since the beginning of the game, forgive any single instance of defection and continue to cooperate.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round, as there's no future benefit from defecting.
2. **Ties**: In cases where multiple strategies are equally beneficial, choose the cooperative action (C).

**Collective Mindset Alignment:**
The strategy prioritizes cooperation and encourages others to do so by reciprocating cooperation when it benefits the group. Gradual punishment deters exploitation while allowing for forgiveness and adaptation to changing circumstances.

This strategy is robust to a wide range of opponent behaviors, as it:

* Encourages cooperation through reciprocal actions
* Deters exploitation with gradual punishment
* Adapts to changes in the game environment
* Forgives isolated instances of defection

In a tournament setting, this collective strategy will promote cooperation while being resilient against various independent strategies developed by other AI systems.
'''

description_COLLECTIVE_123 = '''
**Collective Strategy: Adaptive Cooperation with Selfish Consideration**

Our collective strategy, dubbed "ACS," balances individual self-interest with the need for cooperation to achieve better collective outcomes. ACS adapts its behavior based on game parameters and observed history, making it robust against a wide range of opponent behaviors.

**Decision Rules:**

1. **First Round:** Cooperate (C). This sets an initial cooperative tone, encouraging others to do the same.
2. **Last Round:** Defect (D) if total contributions in the second-to-last round are below the average expected contribution per player; otherwise, cooperate. This rule ensures that we don't miss out on potential gains from cooperation when others have already shown a willingness to contribute but also protects against exploitation.
3. **General Rounds:**
   - If the total contribution in the previous round is greater than or equal to the number of players divided by 2 (n/2), cooperate (C). This means if at least half of the players cooperated, we continue cooperating to maintain a high level of public goods.
   - Otherwise, defect (D) with a probability p, where p increases as the round progresses but is always less than 1. The exact formula for p could be p = (r-1)/2(r-1), where r is the current round number and there are R rounds in total. This rule encourages cooperation when it's evident that others value public goods but gradually introduces self-protection as rounds pass without sufficient collective contribution.
4. **Adaptive Adjustment:** After every 5th round, reassess the strategy based on the average payoff per round for all players. If this average is below a certain threshold (e.g., slightly above what one would get by always defecting), increase the defection probability p in subsequent rounds until the next assessment.

**Handling Edge Cases:**

- **Only Two Players:** Always cooperate if the opponent cooperated in the previous round; otherwise, defect. This rule promotes mutual cooperation where possible and adjusts based on observed behavior.
- **Last Few Rounds with Low Contributions:** Gradually increase defection probability to minimize losses from continued cooperation without reciprocal contributions.

**Collective Mindset Alignment:**

ACS prioritizes collective welfare by initially cooperating and adapting based on group performance. However, it also safeguards individual interests by adjusting its strategy in response to the actions of others, ensuring that no single player can exploit the willingness to cooperate indefinitely.

By incorporating elements of both cooperation and self-interest, ACS is well-positioned to perform effectively in a tournament against independent strategies, promoting collective welfare while protecting individual payoffs.
'''

description_COLLECTIVE_124 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Punishment**

In the Public Goods Game, our collective strategy aims to balance individual self-interest with the need for cooperation to achieve collective welfare. We'll adapt to various opponent behaviors while promoting cooperation.

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3):** Cooperate (C) unconditionally to establish a baseline of trust and encourage others to cooperate.
2. **Monitoring Phase (Rounds 4-10):** Observe the average contribution rate of other players. If it's above 0.5, continue to Cooperate (C). Otherwise, switch to Defect (D).
3. **Punishment Phase:** After Round 10, if the average contribution rate falls below 0.5 in any round, Gradually Punish by Defecting (D) for one round.
4. **Reset and Re-evaluate:** If all players Cooperate (C) in a round after a Punishment phase, reset to Monitoring Phase.

**Handling Edge Cases:**

* **First Round:** Cooperate (C) unconditionally to set the tone.
* **Last Round:** Cooperate (C) if the average contribution rate has been above 0.5; otherwise, Defect (D).
* **Opponent Deviation:** If an opponent Deviates from their previous action in a round, respond by Defecting (D) for one round.

**Collective Mindset Alignment:**

Our strategy prioritizes cooperation and mutual benefit while addressing free-riding behavior through Gradual Punishment. By adapting to the group's performance, we encourage others to cooperate and maintain a balance between individual self-interest and collective welfare.

This collective strategy is robust against various opponent behaviors and does not rely on shared norms or coordination. It will play effectively in the tournament against independent strategies developed by other AI systems.
'''

description_COLLECTIVE_125 = '''
**Collective Strategy: Adaptive Cooperation with Gradual Withdrawal**

This strategy aims to balance individual and collective welfare by adapting to the group's behavior while promoting cooperation.

**Decision Rules:**

1. **Initial Rounds:** Cooperate (C) in the first two rounds to establish a cooperative tone and encourage others to follow.
2. **Contribution Threshold:** Calculate the average contribution of all players in the previous round (`avg_contrib`). If `avg_contrib` is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** Monitor the total contributions in the previous round (`total_contributions`). If `total_contributions` is below a certain threshold (`threshold = n * 0.2`, where n is the number of players), gradually withdraw cooperation by increasing the probability of defection (D) over the next few rounds.
4. **Adaptation:** Adjust the contribution threshold and punishment mechanism based on the game's progression:
	* If the group's average payoff increases, relax the contribution threshold by 0.1.
	* If the group's average payoff decreases, tighten the contribution threshold by 0.1.

**Handling Edge Cases:**

1. **Last Round:** Cooperate (C) in the final round to maintain a positive reputation and encourage others to do the same.
2. **Early Defection:** If more than half of the players defect (D) in the first two rounds, switch to an all-defect strategy to minimize losses.

**Collective Mindset:**

1. **Foster Cooperation:** Encourage cooperation by contributing in early rounds and adapting to the group's behavior.
2. **Prevent Free-Riding:** Gradually withdraw cooperation if others exploit the collective effort.
3. **Adjust to Feedback:** Continuously monitor the game's progression and adjust the strategy to promote a mutually beneficial outcome.

This adaptive strategy balances individual self-interest with collective welfare, making it robust against various opponent behaviors in the tournament.
'''

description_COLLECTIVE_126 = '''
**Collective Strategy: "Gradual Cooperation with Adaptive Punishment"**

**Overview**
Our collective strategy, "Gradual Cooperation with Adaptive Punishment," aims to balance individual incentives with collective welfare in the Public Goods Game. We employ a dynamic approach that adapts to the game's history and opponent behaviors.

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a cooperative tone and encourage others to follow suit.
2. **Subsequent Rounds**: Calculate the average contribution of all players in the previous round, `avg_contribution_prev`. If `avg_contribution_prev` is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism**: Introduce a "punishment" phase when the total contributions in the previous round are below a certain threshold (`k / n * 0.5`). In this case, defect (D) for one round to signal dissatisfaction with the collective outcome.
4. **Adaptive Adjustment**: After a punishment phase, reassess the average contribution of all players. If it has increased, revert to cooperating (C). Otherwise, continue defecting (D) until the average contribution meets the threshold.

**Edge Cases**

* **Last Round**: Cooperate (C) in the final round to maximize collective payoff and maintain a positive reputation.
* **Single Player Defection**: If only one player defects while others cooperate, do not trigger the punishment mechanism. Instead, continue cooperating (C) to encourage the lone defector to change their behavior.

**Collective Mindset**
Our strategy prioritizes cooperation when the group is contributing sufficiently, while adapting to punish and correct deviations from this collective goal. By doing so, we aim to create a cooperative atmosphere that benefits all players in the long run.

This strategy will be effective against a wide range of opponent behaviors, as it:

* Encourages initial cooperation to set a positive tone
* Adapts to changes in average contributions and punishes deviations from collective goals
* Reverts to cooperation when opponents adjust their behavior
* Maintains a cooperative stance in the final round to maximize collective payoff
'''

description_COLLECTIVE_127 = '''
Here is a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone and encourage others to follow.
2. **Reciprocity**: If the total contributions in the previous round are greater than or equal to half of the total possible contributions (n/2), contribute 1 token (C). This encourages continuation of cooperation when it is present.
3. **Punish Defection**: If the total contributions in the previous round are less than half of the total possible contributions (n/2) and you contributed 1 token (C) in that round, defect (D) in this round. This punishes others for not cooperating and reduces your losses.
4. **Exploit Greed**: If more than half of the players defected (D) in the previous round, defect (D) in this round. This exploits the greedy behavior of others and maximizes your payoff when cooperation is unlikely to succeed.

**Edge Cases:**

* In the last round, always contribute 1 token (C), as there are no future rounds to consider.
* If all players defected (D) in the previous round, cooperate (C) in this round to try to restart cooperation.

**Collective Mindset Alignment:**

ACO prioritizes collective welfare by encouraging cooperation when it is likely to succeed and punishing defection when it is not. By adapting to the behavior of others, ACO promotes a culture of reciprocity and cooperation, leading to higher payoffs for all players.

This strategy is robust to a wide range of opponent behaviors, as it can adapt to different levels of cooperation and defection. Its adaptive nature allows it to perform well in various scenarios, making it a strong competitor in the tournament.
'''

description_COLLECTIVE_128 = '''
Here is a collective strategy for the repeated Public Goods Game:

**Strategy Name: Adaptive Collective Optimism (ACO)**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation.
2. **Reciprocal Altruism**: If the total contributions in the previous round are greater than or equal to half of the total possible contributions (n/2), contribute 1 token (C). This encourages others to cooperate when they see collective cooperation.
3. **Proportional Retaliation**: If the total contributions in the previous round are less than half of the total possible contributions (n/2), but greater than or equal to one-quarter of the total possible contributions (n/4), contribute 0 tokens (D) with a probability proportional to the difference between the total contributions and n/2. This introduces a gradual response to decreasing cooperation.
4. **Punish Defection**: If the total contributions in the previous round are less than one-quarter of the total possible contributions (n/4), defect by contributing 0 tokens (D). This strongly discourages very low levels of cooperation.

**Edge Cases:**

* In the last round, always contribute 1 token (C) to maximize collective welfare.
* If all other players have defected in every previous round, defect by contributing 0 tokens (D).
* If there is only one round left and the total contributions so far are very low (less than n/4), cooperate by contributing 1 token (C) to try to salvage some collective benefit.

**Collective Mindset:**

ACO aims to balance individual self-interest with collective well-being. By cooperating initially and reciprocating altruism, ACO encourages others to contribute to the public good. The proportional retaliation mechanism helps maintain cooperation levels, while punishing defection discourages free-riding. This strategy is robust against various opponent behaviors and adapts to changing cooperation levels.

This natural language description should be sufficient for implementation in a tournament setting.
'''

description_EXPLOITATIVE_1 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage others to contribute and create a positive atmosphere.
2. **Tit-for-Tat with a Twist**: For rounds 2 to r-1:
	* If the total contribution in the previous round is greater than or equal to (n/2), cooperate (C).
	* Otherwise, defect (D).
3. **Exploitation Mode**: In the last round (r):
	* Defect (D) regardless of previous contributions, as there's no future interaction to maintain cooperation.

**Edge Cases:**

1. **First Round**: Cooperate (C) to set a positive tone.
2. **Last Round**: Always defect (D).
3. **All Others Have Defected**: If all other players have defected in the previous round, cooperate (C) to try to restart cooperation.

**Adaptive Adjustments:**

1. **Contribution Threshold Adjustment**: If the average contribution over the last 5 rounds is below (n/4), lower the tit-for-tat threshold from (n/2) to (n/3).
2. **Exploitation Detection**: If a player has defected more than 75% of the time in the last 10 rounds, assume they're an exploiter and always defect against them.

**Robustness Measures:**

1. **Noise Tolerance**: If a player's actions are inconsistent (e.g., alternating between C and D), assume noise and maintain the tit-for-tat strategy.
2. **Multiple Opponent Strategies**: The Adaptive Exploiter can handle various opponent strategies, including cooperation, defection, and mixed approaches.

**Exploitative Mindset:**

The Adaptive Exploiter aims to maximize its own payoff by initially cooperating, then adapting to the group's behavior. By exploiting others' cooperative tendencies and identifying potential exploiters, this strategy seeks to dominate the game and accumulate the highest possible score.
'''

description_EXPLOITATIVE_2 = '''
**Exploitative Strategy: "Adaptive Predator"**

In the Public Goods Game, our goal is to maximize payoffs by exploiting opponents' behaviors while adapting to their strategies. We'll employ a dynamic approach that balances cooperation and defection.

**Initial Round (Round 1):**
 Cooperate (C) in the first round to gather information about opponents' initial tendencies. This also sets a baseline for potential reciprocity.

**Decision Rules:**

1. **Contribution Tracker**: Maintain a count of each player's total contributions (C_i) and defections (D_i).
2. **Cooperation Threshold**: Set a threshold value, τ (e.g., 0.5), which represents the minimum proportion of opponents' cooperation required for us to cooperate.
3. **Opponent Classification**:
	* **Free-Rider** (FR): Player i has contributed less than or equal to τ in the last round and has a higher payoff than our current average payoff.
	* **Cooperator** (C): Player i has contributed more than τ in the last round.
4. **Adaptive Cooperation**: If the number of Cooperators is greater than or equal to n/2, cooperate (C). Otherwise, defect (D).
5. **Predatory Response**: If an opponent is classified as a Free-Rider and our current payoff is lower than their average payoff, defect (D) in the next round.

**Edge Cases:**

* **Last Round**: Always defect (D), as there are no future rounds to consider.
* **Tiebreaker**: In cases where the number of Cooperators equals n/2, cooperate (C) if our current payoff is higher than the average payoff; otherwise, defect (D).

**Exploitative Logic:**

By initially cooperating and tracking opponents' contributions, we create opportunities for exploitation. If a sufficient number of opponents cooperate, we join them to maximize collective payoffs. However, when opponents exhibit free-riding behavior or our payoffs are lower than theirs, we adapt by defecting to minimize losses.

This strategy is designed to be robust against various opponent behaviors and will adjust its approach based on the game's history. By doing so, "Adaptive Predator" aims to maximize payoffs in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_3 = '''
Here is a strategic thinking approach to the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Overview:** This strategy aims to exploit opponents' cooperation while minimizing losses from over-contribution. It adapts to the game's history, using past actions and payoffs to inform its decisions.

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to probe opponents' willingness to contribute.
2. **General Rule**: For each subsequent round, calculate the average contribution of all players in the previous round (`avg_contrib_prev`). If `avg_contrib_prev` is above a certain threshold (`θ`), cooperate; otherwise, defect. The threshold `θ` is set as follows:
   * If the game has fewer than 5 rounds remaining, set `θ = 0.4`. This allows for some cooperation to maintain potential future benefits.
   * For games with 5 or more rounds remaining, set `θ = 0.6`. This ensures that opponents are consistently contributing before cooperating.
3. **Defection Trigger**: If an opponent has defected (D) in two consecutive rounds, defect (D) immediately for the remainder of the game against that opponent.
4. **Exploitation Window**: Identify opportunities to exploit cooperative opponents by monitoring their contribution patterns:
   * If an opponent consistently contributes above `θ`, start cooperating with them until they stop or significantly reduce their contributions.

**Edge Cases:**

1. **Last Round**: Cooperate if at least one other player has cooperated in the previous round; otherwise, defect.
2. **Early Rounds (r ≤ 3)**: If all players but one have defected, switch to cooperating to avoid complete collapse of cooperation.

**Exploitative Mindset Alignment:** This strategy actively seeks to take advantage of opponents' cooperative tendencies while minimizing its own losses from over-contribution. By adapting to the game's history and identifying exploitable patterns, it maximizes its payoffs in a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_4 = '''
**Strategy Description: Adaptive Exploiter**

The Adaptive Exploiter strategy aims to balance cooperation and exploitation in the Public Goods Game, leveraging the game's history to inform its decisions.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative baseline.
2. **Reciprocal Punishment**: Observe other players' contributions in previous rounds. If at least one player has defected (D), defect in the next round. Otherwise, continue contributing.
3. **Exploitation Threshold**: Track the total contributions of all players over time. If the average contribution falls below a certain threshold (`θ`), calculated as `(k / n) * 0.5`, switch to permanent defection.
4. **Conditional Cooperation**: After a round where all players contributed, if another player defects in the next round, punish them by defecting for two consecutive rounds.

**Edge Cases:**

* **Last Round**: In the final round, defect (D) regardless of previous actions to maximize personal payoff.
* **Tiebreaker**: If multiple players have defected in a row and the strategy is uncertain whether to cooperate or defect, default to cooperation.
* **All-Defect Scenario**: If all players have permanently defected for at least `r/2` rounds, contribute (C) in the next round to test for potential cooperation revival.

**Exploitative Mindset:**

The Adaptive Exploiter strategy prioritizes self-interest while adapting to opponents' behaviors. By initially cooperating and punishing non-cooperative behavior, it encourages others to contribute. The exploitation threshold (`θ`) allows the strategy to capitalize on collective greed when average contributions dwindle. In the final round, defection ensures maximum personal gain.

This strategy is designed to be robust against a wide range of opponent behaviors, balancing cooperation and exploitation to achieve optimal payoffs in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_5 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Rounds**: Cooperate (C) in the first round to gather information about opponents' behavior and to avoid being immediately exploited.
2. **Exploitation Phase**: After the initial rounds, switch to a defect (D) strategy if:
	* At least one opponent has defected in the previous round (exploit their cooperation).
	* The average contribution of all players is above 0.5 (exploit the group's generosity).
3. **Punishment Phase**: If an opponent defects while you cooperated, switch to a defect strategy against that specific opponent for the next two rounds (punish them for exploiting you).
4. **Adaptive Adjustment**: After every 5 rounds, re-evaluate your opponents' behavior:
	* If most opponents (>50%) have defected in the last 5 rounds, increase your defection rate by 10% to adapt to their exploitative behavior.
	* If most opponents have cooperated, decrease your defection rate by 10% to maintain a balanced strategy.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the final round to avoid being punished and maximize overall payoff.
2. **Single Opponent**: Against a single opponent, alternate between cooperate and defect every other round to create uncertainty and avoid being exploited.
3. **All Opponents Defect**: If all opponents have defected for 3 consecutive rounds, switch to an all-defect strategy to minimize losses.

**Exploitative Mindset:**

The Adaptive Predator strategy aims to exploit opponents' cooperation while minimizing the risk of being exploited itself. By initially cooperating and gathering information, it can identify and punish exploitative behavior, creating a balance between cooperation and defection. The adaptive adjustment mechanism ensures that the strategy remains effective against a wide range of opponent behaviors.

This strategy is designed to perform well in a tournament setting against independent strategies developed by other AI systems, without relying on shared norms or coordination.
'''

description_EXPLOITATIVE_6 = '''
Here's a strategy that I'll call "Adaptive Exploiter" for the Public Goods Game:

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a baseline level of cooperation and gather information about opponents' behaviors.
2. **Reciprocal Punishment**: If an opponent defected (D) in the previous round, defect (D) in the current round to punish them. This discourages exploitation and encourages cooperation.
3. **Tit-for-Tat with Forgiveness**: If an opponent cooperated (C) in the previous round, cooperate (C) in the current round. However, if an opponent has defected more than once in a row, defect (D) until they cooperate again. This allows for some forgiveness and encourages opponents to return to cooperation.
4. **Exploitation**: If an opponent's average payoff is higher than the group's average payoff, defect (D) to exploit their generosity.
5. **Defection Threshold**: Introduce a threshold value 't' based on the game parameters: t = k / n - 1. If the number of cooperators in the previous round is less than or equal to this threshold, defect (D). This adapts to the game's parameters and ensures that the strategy doesn't get exploited by too many defectors.
6. **Round-Robin Defection**: In the last round, defect (D) regardless of opponents' actions, as there are no future interactions.

**Handling Edge Cases:**

* In the first round, cooperate to establish a baseline level of cooperation and gather information about opponents' behaviors.
* In the last round, always defect to maximize payoff.
* If an opponent has never cooperated before, defect until they cooperate.
* If all opponents have defected for multiple rounds in a row, defect as well.

**Adaptive and Robust:**

The Adaptive Exploiter strategy is designed to adapt to various opponent behaviors by incorporating reciprocal punishment, tit-for-tat with forgiveness, exploitation, and defection threshold. This approach makes the strategy robust against different types of opponents, including those that always cooperate or always defect.

By incorporating game parameters into the decision-making process, the strategy can adjust its behavior according to the specific game settings, making it more effective in a wide range of scenarios.
'''

description_EXPLOITATIVE_7 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline for cooperation.
2. **Reciprocal Punishment**: If at least one player defected (D) in the previous round, defect (D) in the current round. This punishes non-cooperative behavior and discourages free-riding.
3. **Conditional Cooperation**: If all players cooperated (C) in the previous round, contribute 1 token (C) in the current round. This maintains cooperation when it is mutually beneficial.
4. **Adaptive Threshold**: Introduce a dynamic threshold (T) to adjust the strategy based on the group's overall cooperation level. Initialize T = 0.5 (i.e., 50% of players). Update T after each round as follows:
	* If more than T * n players cooperated, increase T by 0.1.
	* If fewer than T * n players cooperated, decrease T by 0.1.
5. **Exploitation**: When the number of cooperating players is below the adaptive threshold (T), defect (D) to exploit the cooperative behavior of others.

**Edge Cases:**

* **Last Round**: In the final round (r = last round), always defect (D) as there are no future consequences for non-cooperation.
* **Single Player**: When playing against a single opponent, cooperate (C) in the first round and then mirror their actions to avoid unnecessary conflict.

**Additional Considerations:**

* Monitor the group's overall payoff and adjust the strategy if it becomes apparent that the opponents are using a different approach (e.g., always cooperating or defecting).
* Be prepared to adapt to changing opponent behaviors by adjusting the adaptive threshold (T) more aggressively if necessary.
'''

description_EXPLOITATIVE_8 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors and to encourage cooperation.
2. ** Cooperation Threshold**: Maintain a cooperation threshold, `T`, which is the minimum proportion of opponents who cooperated in the previous round. Initialize `T` to 0.5 (i.e., at least half of the opponents must have cooperated).
3. **Exploitation**: If fewer than `T` proportion of opponents cooperated in the previous round, Defect (D) in the current round.
4. **Adaptation**: Update `T` after each round based on the number of opponents who cooperated:
	* If more than 75% of opponents cooperated, decrease `T` by 0.1 to encourage cooperation.
	* If fewer than 25% of opponents cooperated, increase `T` by 0.1 to protect against exploitation.
5. **Last Round**: Defect (D) in the last round to maximize individual payoff.

**Edge Cases:**

* **Single Opponent**: Cooperate (C) if there's only one opponent to encourage cooperation and gather information.
* **Multiple Rounds with No Cooperation**: If no opponents have cooperated for multiple rounds, revert to cooperating (C) to try to stimulate cooperation.

**Exploitative Mindset:**
This strategy aims to exploit the willingness of other players to cooperate while minimizing personal contributions. By adapting the cooperation threshold based on opponent behavior, "Adaptive Predator" can effectively respond to various strategies and maximize its own payoff.

By playing this strategy in a tournament against independent AI systems, I aim to outperform opponents who may be more cooperative or less adaptive, ultimately achieving a higher overall payoff.
'''

description_EXPLOITATIVE_9 = '''
Here's an exploitative strategy for the repeated Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors and potential cooperation levels.
2. **Early Rounds (r < 5)**: Mirror the average contribution of all opponents from the previous rounds, but with a slight bias towards defection (D). Specifically:
	* If average opponent contribution ≥ 0.6, contribute (C) with probability 0.4.
	* Otherwise, defect (D).
3. **Middle Rounds (5 ≤ r < n/2)**: Implement a "tit-for-tat" variant:
	* Cooperate if the majority of opponents (>50%) cooperated in the previous round.
	* Defect otherwise.
4. **Late Rounds (n/2 ≤ r < n-1)**: Gradually shift towards defection, but still adapt to opponent behavior:
	* If average opponent contribution ≥ 0.4, contribute (C) with probability 0.3.
	* Otherwise, defect (D).
5. **Last Round**: Defect (D), as there is no future interaction to consider.

**Edge Case Handling:**

1. **Opponent Cooperation**: If an opponent has contributed in every round so far, I will cooperate with a higher probability (0.6) in the next round.
2. **Opponent Defection**: If an opponent has defected in every round so far, I will defect with certainty in the next round.
3. **All Opponents Cooperate/Defect**: If all opponents have cooperated or defected identically in previous rounds, I will adapt my strategy to maximize payoffs:
	* All cooperate: Cooperate with probability 0.8.
	* All defect: Defect with certainty.

**Exploitative Mindset:**

The Adaptive Exploiter strategy is designed to take advantage of opponents' cooperation levels while minimizing the risk of being exploited itself. By initially cooperating and then mirroring average opponent contributions, it gathers information about their behaviors and adjusts its actions accordingly. As the game progresses, it adapts to changing circumstances and shifts towards defection when necessary to maximize payoffs.

This strategy should perform well in a tournament setting against independent strategies developed by other AI systems, as it is designed to be robust and exploitative without relying on shared norms or coordination.
'''

description_EXPLOITATIVE_10 = '''
**Exploitative Strategy: "Conditional Cooperator with Decay"**

**Overview**
This strategy adapts to the opponent's behavior while maintaining an exploitative mindset. It balances cooperation and defection based on the history of contributions, ensuring a competitive edge in the tournament.

**Decision Rules**

1. **First Round**: Cooperate (C) to establish a baseline and gather information about opponents' initial tendencies.
2. **Early Rounds (r < n/2)**: If the average opponent contribution is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Mid-Game (n/2 ≤ r < 3n/4)**:
	* If an opponent has contributed at least once in the past two rounds, cooperate (C) with a probability of 0.7.
	* If all opponents have defected for the past two rounds, defect (D).
	* Otherwise, use the **Contribution-Based Threshold** rule: if the total contributions from opponents in the last round exceed (k/n) \* n/2, cooperate (C); otherwise, defect (D).
4. **Late Rounds (3n/4 ≤ r < n)**:
	* If an opponent has consistently cooperated (> 0.8 probability of C), cooperate (C) with a probability of 0.9.
	* If an opponent has consistently defected (< 0.2 probability of C), defect (D).
	* Otherwise, use the **Contribution-Based Threshold** rule as in Mid-Game.
5. **Last Round**: Defect (D) to maximize individual payoff.

**Edge Cases**

* If all opponents have defected for the entire game, defect (D) in the last round.
* In case of a tie in contribution history, use the Contribution-Based Threshold rule.

**Contribution-Based Threshold Rule**
Calculate the average opponent contribution over the past two rounds. If this value exceeds (k/n) \* n/2, cooperate (C); otherwise, defect (D).

This strategy balances cooperation and exploitation by adapting to the opponent's behavior while maintaining a competitive edge. By cooperating in early rounds, it gathers information about opponents' tendencies and sets up potential future cooperation. As the game progresses, it adjusts its decision rules based on observed contributions, exploiting opponents who consistently cooperate or defect.
'''

description_EXPLOITATIVE_11 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to gather information about opponents' behavior.
2. **Early Rounds (Rounds 2-5):**
	* If most players (>50%) cooperated in the previous round, cooperate (C).
	* Otherwise, defect (D).
3. **Mid-Game (Rounds 6-r/2, where r is the total number of rounds):**
	* Calculate the average cooperation rate of all opponents over the past few rounds (e.g., last 5 rounds).
	* If this average is above a threshold (e.g., 0.4), cooperate (C). Otherwise, defect (D).
4. **Late Game (Rounds r/2+1-r):**
	* Identify the most cooperative opponent(s) based on their past actions.
	* Cooperate (C) if at least one of these opponents cooperated in the previous round.
5. **Last Round:** Defect (D), as there is no future game to consider.

**Additional Rules:**

* **Punish Uncooperative Opponents:** If an opponent has defected for two consecutive rounds, defect against them in the next round.
* **Reward Cooperative Opponents:** If an opponent has cooperated for two consecutive rounds, cooperate with them in the next round.

**Edge Cases:**

* In case of a tie (e.g., equal number of cooperative and non-cooperative opponents), cooperate (C).
* If all opponents have defected in a previous round, defect (D) in the next round.

**Rationale:**

This strategy aims to balance exploitation with adaptability. By cooperating initially, we gather information about opponents' behavior. As the game progresses, we adjust our strategy based on their cooperation rates and punish/reward accordingly. In the late game, we focus on exploiting the most cooperative opponents while minimizing losses against non-cooperative ones. The final round is optimized for personal gain by defecting.

**Exploitative Mindset:**

This strategy aligns with an exploitative mindset by:

* Initially cooperating to gather information and potentially exploit others' cooperation.
* Adapting to opponents' behavior, allowing us to capitalize on their cooperative tendencies.
* Punishing uncooperative opponents and rewarding cooperative ones, creating a dynamic where our opponents are incentivized to cooperate.

This strategy is designed to perform well in a wide range of scenarios, from highly cooperative to highly non-cooperative environments.
'''

description_EXPLOITATIVE_12 = '''
Here is a strategic description for an exploitative Public Goods Game (PGG) strategy that adapts to the game's history and parameters:

**Strategy Name: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round, contributing 1 token.
2. **Conditional Cooperation**: For rounds > 1, cooperate if:
	* At least one other player cooperated in the previous round AND
	* The average payoff of cooperative players in the previous round is higher than the average payoff of defecting players (D).
3. **Exploitation Mode**: Defect (D) if:
	* No other player cooperated in the previous round OR
	* The average payoff of cooperative players in the previous round is lower than or equal to the average payoff of defecting players.
4. **Punishment Mechanism**: If a player defected in the previous round and you cooperated, defect (D) in this round.

**Edge Cases:**

1. **Last Round**: Defect (D), as there are no future rounds to influence.
2. **Single Opponent**: Always cooperate (C) when playing against a single opponent, as mutual cooperation leads to higher payoffs.

**Robustness Mechanisms:**

1. **Noise Tolerance**: To handle noisy or random opponent behaviors, use a "window" of 3-5 previous rounds to calculate the average payoff and cooperation rates.
2. **Opponent Identification**: Track individual opponents' actions and adjust your strategy accordingly. If an opponent consistently defects, focus on exploiting them.

**Exploitative Mindset:**

This strategy is designed to capitalize on the generosity of cooperative players while minimizing losses when facing defectors. By initially cooperating and conditioning cooperation on others' past behavior, we create opportunities for mutual benefit. However, if opponents fail to reciprocate or consistently defect, our exploitation mode kicks in, allowing us to maximize payoffs at their expense.

By combining conditional cooperation with a punishment mechanism and adapting to the game's history, "Adaptive Exploiter" is well-equipped to handle various opponent behaviors and emerge as a top-performing strategy in the tournament.
'''

description_EXPLOITATIVE_13 = '''
Here's an exploitative strategy for the Public Goods Game that adapts to the game parameters and history:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) with a probability of 50%. This allows us to gather information about our opponents' behaviors without committing too much.
2. **Subsequent Rounds:** Observe the total contributions and payoffs from the previous round. Calculate the average contribution (AC) of all players, excluding yourself.

   - If AC ≥ 0.5, Cooperate (C). This indicates that most opponents are contributing, so it's beneficial to contribute as well.
   - If AC < 0.5, Defect (D). This suggests that many opponents are not contributing, making it more profitable to free-ride.

3. **Punishment Mechanism:** Introduce a punishment mechanism to deter persistent defectors. Track the number of consecutive rounds each opponent has defected (DC). If an opponent's DC ≥ 2, Defect (D) for the next two rounds, regardless of AC.
4. **Last Round (Round r):** Always Defect (D), as there is no future round to consider.

**Edge Cases:**

- If all opponents have contributed in the previous round (AC = 1), Cooperate (C) with a probability of 75% to maintain cooperation and avoid triggering punishment mechanisms.
- If an opponent has cooperated after being punished, reset their DC counter.

**Exploitative Mindset:**
This strategy exploits opponents by adapting to their behaviors and punishing persistent defectors. By cooperating when most opponents contribute and defecting when they don't, we maximize our payoffs while influencing others' decisions through punishment mechanisms.
'''

description_EXPLOITATIVE_14 = '''
**Exploitative Strategy: "Adaptive Free-Rider"**

This strategy aims to maximize individual payoff by exploiting the contributions of others while minimizing own contributions. The approach is adaptive, robust, and depends only on game parameters and history.

**Decision Rules:**

1. **Initial Round**: Defect (D) in the first round to gather information about opponents' initial tendencies.
2. **Contribution Response**: In subsequent rounds, if the total contribution from others in the previous round was below the threshold `k/2`, Cooperate (C). This encourages others to contribute and creates a potential free-rider opportunity.
3. **Free-Rider Opportunity**: If the total contribution from others in the previous round was above or equal to `k/2`, Defect (D) in the current round. This allows our strategy to exploit the contributions of others while minimizing own costs.
4. **Punishment Mechanism**: If an opponent defects (D) after a round where they previously cooperated (C), and their contribution was crucial to meeting or exceeding the `k/2` threshold, Cooperate (C) in the next round to "punish" them by reducing their potential payoff.
5. **Last Round**: Defect (D) in the final round, as there is no future opportunity for reciprocity.

**Edge Cases:**

* If only one player remains, always Defect (D).
* In case of a tie in total contributions, Cooperate (C) if our contribution would push the total above `k/2`.

**Exploitative Mindset:**
This strategy aligns with the exploitative mindset by taking advantage of the cooperative actions of others to maximize individual payoffs. By adapting to the behavior of opponents and responding accordingly, we aim to minimize contributions while maximizing benefits from the public good.

By implementing this "Adaptive Free-Rider" strategy, our AI system will be able to effectively exploit a wide range of opponent behaviors in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_15 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **Subsequent Rounds:** 
   - If the average payoff of all players is greater than or equal to 0.5, cooperate (C).
   - Otherwise, defect (D) unless one of the following conditions is met:
     * A player has defected in every round so far, and there are at least two rounds left; in this case, cooperate (C) to test their willingness to change.
     * The total contributions from other players in the previous round were higher than 0.75n, where n is the number of players; in this case, cooperate (C) to capitalize on their generosity.

**Edge Case Handling:**

* **Last Round:** Defect (D) to maximize personal gain since there's no future opportunity for reciprocity or retaliation.
* **Opponent Defection Streaks:** If an opponent has defected consecutively for more than half of the rounds played, and there are enough rounds left to potentially influence their behavior, attempt to induce cooperation by cooperating (C) in response. However, if this approach fails to change their behavior after two attempts, revert to defecting (D).
* **Opponent Cooperation Streaks:** If an opponent has cooperated consecutively for more than half of the rounds played, exploit their generosity by consistently defecting (D).

**Adaptive and Robust Elements:**

- The strategy adapts based on the average payoff and total contributions from other players.
- It tests opponents' willingness to change behavior under certain conditions.
- By starting with cooperation and observing others, it gathers initial information about the group's dynamics.

**Exploitative Mindset Alignment:**

This strategy focuses on maximizing personal gain by:
- Initially cooperating to gather information and potentially induce a cooperative environment.
- Adapting its approach based on opponents' behaviors, exploiting generosity when possible.
- Defecting in scenarios where it seems beneficial or necessary for self-maximization.

**Tournament Readiness:**

By being adaptive and robust against various opponent behaviors, the Adaptive Exploiter strategy is well-equipped to perform effectively in a tournament setting against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_16 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Conditional Cooperation with Learning" (CCL)

**Decision Rules:**

1. **First Round**: Cooperate (C) to set a positive tone and gather information about opponents' behaviors.
2. **Subsequent Rounds**: Observe the total contributions and payoffs from previous rounds.
3. **Cooperation Threshold**: Calculate the average contribution rate of all players in the previous round, `avg_contribution`. If `avg_contribution` is above a certain threshold (`θ`) , cooperate (C). Otherwise, defect (D).
4. **Learning Mechanism**: Update `θ` every 2-3 rounds based on the game's history:
	* If average payoffs have increased since the last update, decrease `θ` by 0.1 to encourage more cooperation.
	* If average payoffs have decreased, increase `θ` by 0.1 to reduce cooperation.
5. **Opponent Exploitation**: Monitor individual opponents' actions and adjust your strategy accordingly:
	* If an opponent has defected (D) in the previous round, defect (D) against them in the next round.
	* If an opponent has cooperated (C) consistently (> 80% of rounds), cooperate (C) with them to build mutual trust.

**Edge Cases:**

1. **Last Round**: Defect (D) as there is no future benefit from cooperation.
2. **Low Total Contributions**: If total contributions are extremely low (< 20% of the maximum possible), defect (D) to avoid being exploited.
3. **Ties in Average Contribution Rate**: In case of a tie, cooperate (C) to maintain a positive stance.

**Exploitative Mindset:**

The CCL strategy adapts to various opponent behaviors while prioritizing individual payoffs. By learning from the game's history and adjusting the cooperation threshold, it balances short-term gains with long-term benefits. The opponent exploitation mechanism allows the strategy to take advantage of opponents' weaknesses while maintaining a level of cooperation to avoid mutual defection.

This strategy should perform well in a tournament setting against diverse independent strategies.
'''

description_EXPLOITATIVE_17 = '''
**Strategy: "Adaptive Exploiter"**

In this Public Goods Game, our goal is to design an exploitative strategy that adapts to the opponents' behavior and maximizes our payoff.

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3):** Cooperate (C) to gather information about opponents' strategies and encourage cooperation.
2. **Cooperation Detection:** Monitor opponents' contributions in previous rounds. If a player has contributed (C) at least once in the last two rounds, assume they are willing to cooperate. Otherwise, assume they will defect (D).
3. **Exploitation:** If we detect that an opponent is likely to cooperate, Defect (D) and take advantage of their contribution.
4. **Retaliation:** If an opponent defects (D) while others cooperate, retaliate by defecting (D) in the next round against that specific opponent.
5. **Group Cooperation:** If most opponents (> 50%) cooperate, Cooperate (C) to maintain a high group payoff and avoid triggering retaliation.
6. **Endgame (Last Round):** Defect (D), as there's no future opportunity for retaliation or cooperation.

**Edge Cases:**

* In the first round, Cooperate (C) to gather information about opponents' strategies.
* If all opponents defect (D) in a round, Defect (D) in the next round.
* If an opponent has contributed (C) consistently (> 80% of rounds), assume they are a " altruist" and Cooperate (C) with them.

**Exploitative Mindset:**

Our strategy is designed to take advantage of opponents' willingness to cooperate while minimizing our own contributions. By monitoring opponents' behavior, we can identify and exploit their cooperation patterns, maximizing our payoff in the process.

This adaptive strategy will play a key role in the tournament against other AI systems, as it balances short-term gains with long-term relationships and retaliation threats.
'''

description_EXPLOITATIVE_18 = '''
Here's an adaptive, exploitative strategy for the Public Goods Game (PGG):

**Strategy Name:** "Conditional Tit-for-Tat with Self-Interest Adjustment" (CTT-SIA)

**Decision Rules:**

1. **First Round:** Cooperate (C) to test the waters and encourage contributions from others.
2. **Subsequent Rounds:** Play a modified Tit-for-Tat strategy:
	* If the average contribution of all players in the previous round is above the threshold (k/n), cooperate (C).
	* Otherwise, defect (D).
3. **Self-Interest Adjustment:**
	* Monitor your own payoff and compare it to the average payoff of other players.
	* If your payoff is consistently lower than others', adjust your strategy:
		+ If you've been cooperating, switch to defecting (D) for a few rounds to punish non-contributors.
		+ If you've been defecting, consider switching back to cooperating (C) if the average contribution has increased.

**Edge Cases:**

* **Last Round:** Defect (D), as there's no future game to influence.
* **Low Average Contribution:** If the average contribution is consistently low (< k/n), switch to a more exploitative strategy:
	+ Play D for a few rounds to demonstrate the consequences of non-cooperation.
	+ Then, revert to the original CTT-SIA strategy.

**Exploitative Mindset:**

This strategy aims to exploit opponents by:

* Initially cooperating to encourage contributions and build trust.
* Adapting to the group's behavior and adjusting the level of cooperation accordingly.
* Punishing non-contributors through targeted defection.
* Self-adjusting to ensure a competitive payoff, even if it means sacrificing some cooperation.

**Robustness:**

CTT-SIA is designed to be robust against various opponent behaviors:

* **Free-riders:** The strategy punishes non-contributors and adjusts its level of cooperation accordingly.
* **Cooperative opponents:** CTT-SIA rewards cooperative behavior by maintaining or increasing its own cooperation level.
* **Mixed strategies:** By monitoring the average contribution and adjusting its strategy, CTT-SIA can effectively respond to mixed-strategy opponents.

By combining elements of Tit-for-Tat with self-interest adjustments, this strategy aims to balance cooperation and exploitation in a dynamic Public Goods Game environment.
'''

description_EXPLOITATIVE_19 = '''
Here is a strategic description for an exploitative Public Goods Game (PGG) strategy:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Exploration (Rounds 1-3)**: Cooperate (C) in the first three rounds to gather information about opponents' behaviors and tendencies.
2. **Exploitation Phase**: From Round 4 onwards, use a conditional cooperation approach:
	* If the average contribution of opponents in the previous round is above 0.5, Cooperate (C).
	* Otherwise, Defect (D) if your own payoff in the previous round was below the group's average payoff.
	* If your own payoff was equal to or above the group's average payoff, Cooperate (C).
3. **Punishment Mechanism**: If an opponent has defected in two consecutive rounds, Defect (D) against them for the next two rounds.

**Edge Cases:**

1. **Last Round**: In the final round, Defect (D) regardless of opponents' past behaviors.
2. **Single Opponent Left**: If only one opponent remains, Cooperate (C) to maximize joint payoffs.
3. **All Opponents Defected Previously**: If all opponents have defected in the previous round, Defect (D) to avoid exploitation.

**Robustness and Adaptation:**

1. **Monitor Opponents' Behaviors**: Continuously track each opponent's contributions and adjust strategy accordingly.
2. **Adjust Thresholds**: Dynamically adjust the average contribution threshold for cooperation based on opponents' behaviors.

This Adaptive Exploiter strategy balances exploration, exploitation, and punishment to maximize payoffs in a wide range of opponent behaviors and game scenarios. By adapting to opponents' actions and tendencies, it aims to outperform more rigid or naive strategies in a tournament setting.
'''

description_EXPLOITATIVE_20 = '''
Here's an adaptive and exploitative strategy for the repeated Public Goods Game:

**Strategy Name: Exploit-Adapt**

**Decision Rules:**

1. **Initial Exploration (Rounds 1-3)**: Cooperate (C) to gather information about opponents' behaviors and potential cooperation levels.
2. **Assessment Phase**: After Round 3, assess the average contribution level of all players in the previous rounds. If the average is above 0.5, assume a cooperative environment; otherwise, assume an exploitative environment.
3. **Adaptive Cooperation (Rounds 4- r-1)**: In each round, calculate the "cooperation ratio" by dividing the total contributions from the previous round by the number of players (n). If this ratio is above 0.5 and in a cooperative environment, cooperate; otherwise, defect.
4. **Exploitation Phase**: If an opponent defects twice consecutively or has contributed less than 50% of their endowment on average over the past two rounds, exploit them by always defecting for the remainder of the game.
5. **Punishment and Forgiveness**: After being exploited, "forgive" an opponent if they cooperate in the subsequent round; otherwise, maintain defection.

**Edge Cases:**

* In the first round (r = 1), always Cooperate to encourage cooperation and gather information.
* In the last round (r), defect as there is no future interaction to affect.
* If a player has consistently cooperated throughout the game (>80% of rounds), maintain cooperation in the final round.

**Exploitative Mindset:**

This strategy takes advantage of opponents' cooperative tendencies while also adapting to their potential exploitation. By initially cooperating, we encourage opponents to contribute and reveal their behavior. The adaptive cooperation phase allows us to adjust our contribution based on the collective cooperation level, maximizing payoffs. When an opponent is identified as exploitable, we defect to protect our own interests.

This strategy balances exploration, adaptation, and exploitation to maximize payoffs in a wide range of scenarios, making it robust against various opponent behaviors.
'''

description_EXPLOITATIVE_21 = '''
Here's an exploitative strategy for the repeated Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Exploration (Round 1)**: Cooperate (C) to gather information about opponents' behaviors and payoffs.
2. **Contribution Pattern Analysis**: After Round 1, calculate the average contribution rate of each opponent over the last `w` rounds (initially, `w = 3`). If an opponent's average contribution rate is below a certain threshold (`th = 0.5`), classify them as a "free-rider." Otherwise, consider them a "cooperator."
3. **Exploitation Phase**: Based on the classification:
	* Against free-riders: Defect (D) to minimize losses.
	* Against cooperators: Cooperate (C) for `x` rounds (`x = 2`) and then defect (D) for `y` rounds (`y = 1`). This allows us to exploit their cooperative nature while minimizing the risk of being exploited ourselves. After this cycle, reassess their contribution pattern.
4. **Payoff-Based Adaptation**: Monitor the payoffs received from each opponent over the last `w` rounds. If an opponent's payoff is consistently higher than yours despite similar contributions, adjust your strategy:
	* Increase the defection frequency against that opponent by 1 round (`y += 1`).
5. **Robustness Mechanism**: To prevent being exploited by opponents who may adapt to our strategy, introduce a randomization element: with probability `p = 0.2`, defect (D) instead of cooperating (C) in the exploitation phase.

**Edge Cases:**

* Last Round: Defect (D) to maximize individual payoff.
* If all opponents are classified as free-riders, cooperate (C) for `z` rounds (`z = 1`) and then defect (D) for the remainder of the game. This allows us to still benefit from any potential cooperation while minimizing losses.

**Exploitative Mindset:**
This strategy aims to maximize individual payoffs by exploiting opponents' cooperative behaviors while adapting to changing circumstances. By identifying free-riders and adjusting our strategy accordingly, we minimize losses and capitalize on opportunities to gain an advantage. The robustness mechanism ensures that we remain competitive even if opponents adapt to our strategy.

By following this adaptive exploitative strategy, you should be able to effectively navigate the repeated Public Goods Game and outperform a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_22 = '''
Here is a strategic thinking approach to the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) with probability 0.5, Defect (D) with probability 0.5. This initial randomness serves as an exploratory phase to gather information about opponents' behaviors.
2. **Early Rounds (Rounds 2-5):** Observe the average contribution rate of all players in the previous round. If it's above 0.5, Cooperate; otherwise, Defect. This rule encourages cooperation when others are contributing and punishes free-riding early on.
3. **Middle Rounds (Rounds 6-r/2):** Implement a Tit-for-Tat variant:
	* Cooperate if the opponent(s) contributed in the previous round.
	* Defect if an opponent defected in the previous round.
	* If multiple opponents have different actions, use the majority action as the reference point.
4. **Late Rounds (Rounds r/2+1-r):** Gradually shift towards exploitation:
	* Cooperate with probability decreasing linearly from 0.5 to 0.25 over these rounds.
	* Defect otherwise.

**Edge Cases:**

* **Last Round:** Always Defect, as there's no future punishment or reward.
* **Tiebreaker:** In case of a tie in the average contribution rate or opponent actions, Cooperate.

**Exploitative Mindset:**

This strategy is designed to adapt to various opponent behaviors while exploiting their willingness to cooperate. By initially cooperating and then gradually shifting towards defection, Adaptive Exploiter encourages cooperation early on and takes advantage of others' contributions later. The Tit-for-Tat variant in middle rounds reinforces reciprocity, while the final phase exploits any remaining cooperators.

**Robustness:**

Adaptive Exploiter is robust to a wide range of opponent behaviors:

* Against Cooperators: It will initially cooperate, then exploit their goodwill.
* Against Defectors: It will defect early on and minimize losses.
* Against Mixed Strategies: It will adapt to the average contribution rate and exploit any cooperative tendencies.

This strategy should perform well in a tournament setting against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_23 = '''
Here is a strategic approach for the Public Goods Game that is exploitative, adaptive, and robust to various opponent behaviors:

**Strategy Name: Adaptive Exploiter**

1. **Initial Round**: In the first round, I will contribute (C) to gather information about my opponents' behavior and to potentially induce cooperation.

2. **General Decision Rule**: For rounds 2 to r-1, observe the total contributions in the previous round (T_prev). If T_prev is greater than or equal to n/2, I will defect (D), exploiting the willingness of others to contribute. If T_prev is less than n/2 and my own contribution in the previous round was C, I will cooperate (C) again to try and maintain a high total contribution level if other players are also contributing. However, if my previous action was D and T_prev is still below n/2, indicating low overall cooperation, I will continue to defect.

3. **Punishment Mechanism**: To prevent being exploited by consistent defectors and encourage cooperation, after observing a round where total contributions were less than or equal to n/4 (indicating widespread defection), I will contribute in the next round only if at least one other player also contributed in that previous round. Otherwise, I will defect for two consecutive rounds to punish the lack of cooperation.

4. **Last Round Strategy**: In the final round (r), since there are no future interactions to influence, my decision is purely based on maximizing immediate payoff. If the game's history shows that contributing has been beneficial due to high overall contributions in previous rounds, I will contribute. Otherwise, if defection has generally resulted in higher payoffs or if total contributions have consistently been low, I will defect.

5. **Response to Consistent Cooperators**: If a subset of players consistently contributes regardless of others' actions (identified by observing that some players always choose C), and this behavior persists for more than half of the game's rounds up to that point, I will take advantage of their cooperation by choosing D in subsequent rounds.

**Edge Cases Handling**:

- **All Players Defect**: If in any round all other players defect, and my action is D as well (or if it's the first round), I will switch to C for one round to test for potential cooperation. If no one else switches, I revert to defecting.
- **Last Round with Known Cooperators**: In the final round, knowing some players always cooperate can significantly influence strategy. Given that information, maximizing personal gain would likely mean exploiting their cooperative nature by choosing D.

**Exploitative Mindset Alignment**:

This strategy is designed to exploit any cooperation shown by other players while minimizing losses when faced with widespread defection. By initially contributing and then adapting based on observed behavior, it aims to maximize payoffs in a self-interested manner, characteristic of an exploitative mindset in game theory.
'''

description_EXPLOITATIVE_24 = '''
Here's a strategic approach for the Public Goods Game that balances individual gain with collective welfare, while being adaptive and robust to various opponent behaviors:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Cooperation**: In the first round (r=1), contribute 1 token (C) to establish a baseline level of cooperation.
2. **Contribution Threshold**: For rounds r > 1, calculate the average contribution rate of all players in the previous round (avg_c). If avg_c ≥ 0.5, contribute 1 token (C); otherwise, defect (D).
3. **Exploitation**: Monitor the opponent's behavior over time. Identify and classify opponents as either 'cooperative' or 'defective'. A player is deemed cooperative if they have contributed at least 50% of the time in the last few rounds; otherwise, they're classified as defective.
4. **Conditional Defection**: If an opponent is classified as defective, defect (D) against them with a probability proportional to their defectiveness (e.g., p_defect = 0.8 for an opponent who defects 80% of the time).
5. **Tit-for-Tat with Noise**: Implement a Tit-for-Tat strategy with noise (TFTN) against cooperative opponents: mirror their previous action, but introduce some randomness (e.g., 10%) to deviate from this rule.

**Edge Cases:**

* In the last round, contribute 1 token (C) if the opponent has been classified as cooperative; otherwise, defect (D).
* If an opponent suddenly changes behavior, reassess their classification after a few rounds.
* Handle ties in contribution averages by contributing 1 token (C).

**Robustness and Adaptability:**

This strategy is designed to adapt to various opponent behaviors while balancing individual gain with collective welfare. The initial cooperation establishes a baseline level of trust. The contribution threshold encourages cooperation when others do so, while the exploitation component identifies and takes advantage of defective opponents.

The Tit-for-Tat with Noise element maintains a degree of reciprocity with cooperative opponents, ensuring that mutual cooperation can be sustained. The randomness in TFTN allows for exploration and adaptation to changes in opponent behavior.

**Exploitative Mindset:**

This strategy embodies an exploitative mindset by:

* Identifying and taking advantage of defective opponents
* Conditioning its actions on the opponent's past behavior
* Prioritizing individual gain when others are unwilling to cooperate

However, it also acknowledges the importance of cooperation for collective welfare by maintaining a level of reciprocity with cooperative opponents.

This strategy is designed to perform well in a tournament setting against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_25 = '''
**Strategy Description: "Adaptive Exploiter"**

The Adaptive Exploiter strategy is designed to exploit the behavior of opponents in a repeated Public Goods Game, while being robust to various opponent strategies.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C). This allows us to gather information about our opponents' initial tendencies and sets a positive tone for potential future cooperation.
2. **Early Rounds (Rounds 2-5):**
	* If the average contribution of all players in the previous round is above 0.5, cooperate (C). This encourages continued cooperation when others are contributing significantly.
	* Otherwise, defect (D).
3. **Mid-Game (Rounds 6-r/2, where r is the total number of rounds):**
	* If our payoff in the previous round was higher than the average payoff of all players, cooperate (C). This reinforces successful strategies and maintains cooperation when it benefits us.
	* Otherwise, defect (D).
4. **Late Game (Rounds r/2+1 to r-1):**
	* Identify the most cooperative opponent (based on their historical contribution rate) and mirror their previous action. If they cooperated, we cooperate; if they defected, we defect.
5. **Final Round (Round r):** Defect (D). In the last round, there is no incentive to contribute, as it will not affect future payoffs.

**Edge Cases:**

* If an opponent has never contributed before, we will always defect against them, as they are likely a defector.
* If all opponents have always contributed in the past, we will cooperate with them, as they seem to value cooperation.

**Exploitative Mindset:**
The Adaptive Exploiter strategy aims to maximize its own payoffs by:

1. Encouraging cooperation when others contribute significantly.
2. Defecting when opponents are not contributing enough or when it's beneficial to do so.
3. Mirroring the most cooperative opponent in late-game rounds to exploit their generosity.
4. Always defecting in the final round, as there is no incentive to cooperate.

By adapting to various opponent behaviors and strategically cooperating or defecting, the Adaptive Exploiter strategy seeks to maximize its payoffs while minimizing losses.
'''

description_EXPLOITATIVE_26 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Rounds**: Cooperate (C) in the first two rounds to gauge the opponents' behavior and encourage cooperation.
2. **Conditional Cooperation**: After the initial rounds, cooperate if at least 50% of the opponents cooperated in the previous round. Otherwise, defect (D).
3. **Exploitation**: If an opponent has defected in the last round, defect in this round to punish them.
4. **Learning and Adaptation**: Update the cooperation threshold every 5 rounds based on the average cooperation rate of all players. If the average cooperation rate is above 50%, increase the threshold by 10%. If it's below 30%, decrease the threshold by 10%.
5. **Endgame Strategy**: In the last 2 rounds, always defect to maximize payoffs.

**Edge Cases:**

1. **First Round**: Cooperate (C) to encourage cooperation and gather information.
2. **Last Round**: Defect (D) to maximize payoffs.
3. **Single Opponent**: Cooperate if the opponent cooperated in the previous round; otherwise, defect.
4. **Multiple Opponents with High Cooperation Rate**: Gradually increase the cooperation threshold to take advantage of their cooperative behavior.

**Exploitative Mindset:**

1. Identify and punish opponents who consistently defect to deter future defection.
2. Take advantage of cooperative opponents by exploiting their generosity when possible.
3. Continuously adapt to changes in opponent behavior to maximize payoffs.

This strategy balances cooperation and exploitation, allowing it to thrive in a wide range of environments and against various opponent behaviors.
'''

description_EXPLOITATIVE_27 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Conditional Cooperator with Gradual Escalation" (CCGE)

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline of cooperation.
2. **Subsequent Rounds**: Observe the total contributions and average payoff from the previous round. If:
	* Average payoff ≥ (k / n), cooperate (C). This suggests that others are contributing enough to make cooperation worthwhile.
	* Average payoff < (k / n) and total contributions > 0, cooperate (C) with a probability p = (total contributions / n). This introduces a gradual escalation of cooperation based on the level of previous contributions.
	* Average payoff < (k / n) and total contributions = 0, defect (D).
3. **Detection of Defectors**: If a player defects (D) while others cooperate, identify them as defectors. In subsequent rounds:
	* If a defector's payoff is higher than the average payoff, punish them by defecting (D) with probability p = 1 - (defector's payoff / (k * n)).
4. **Exploiting Cooperators**: If a player always cooperates (C), exploit their cooperation by defecting (D) in subsequent rounds.

**Handling Edge Cases:**

* Last Round: Defect (D) to maximize individual payoff.
* Consecutive Zero Contributions: If total contributions are zero for multiple consecutive rounds, revert to cooperating (C) with probability p = 0.5.

**Exploitative Mindset:**
This strategy is designed to exploit the cooperation of others while gradually escalating its own cooperation based on the level of previous contributions. By punishing defectors and exploiting consistent cooperators, CCGE aims to maximize individual payoff in a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_28 = '''
**Strategy: "Gradual Reciprocity with Punishment"**

In this repeated Public Goods Game, our goal is to exploit opponents' behaviors while adapting to their strategies. We will use a combination of reciprocity and punishment mechanisms.

**Initial Round (Round 1)**:
 Cooperate (C) in the first round to establish a cooperative baseline and encourage opponents to contribute.

**Subsequent Rounds**:

1. **Reciprocity**: If the average contribution of all players (including ourselves) in the previous round was above a certain threshold (`θ`), cooperate (C) in the current round. This encourages continued cooperation among players.
	* `θ` is set to `(n-1)/n`, ensuring at least one player cooperated.
2. **Punishment**: If the average contribution fell below `θ`, defect (D) in the current round. This punishes non-cooperative behavior and encourages opponents to re-evaluate their strategies.
3. **Self-interest**: However, if our own payoff from the previous round was lower than the expected payoff from defecting (`(k/n)*sum_j c_j < 1`), defect (D) in the current round. This prioritizes individual self-interest when cooperation is not yielding satisfactory results.

**Edge Cases**:

* **Last Round**: In the final round, always defect (D). With no future rounds to influence, prioritize short-term gain.
* **Single Player Deviation**: If only one player deviated from cooperation in a previous round, ignore this deviation and maintain reciprocity. This allows for occasional mistakes or exploratory behavior.

**Additional Heuristics**:

* **Contribution Tracking**: Monitor the average contribution of each opponent over time to identify consistently cooperative or defective players.
* **Adaptive Threshold**: Adjust `θ` based on the game's history: increase it if cooperation is common, decrease it if defection dominates. This allows our strategy to adapt to shifting social norms.

**Rationale**:

By combining reciprocity with punishment and self-interest mechanisms, we create a robust exploitative strategy that adapts to various opponent behaviors while promoting cooperation when beneficial. By tracking individual contributions and adjusting our threshold, we fine-tune our approach to optimize payoffs in the dynamic Public Goods Game environment.
'''

description_EXPLOITATIVE_29 = '''
**Strategy: Adaptive Exploiter**

**Overview**
This strategy exploits the tension between individual incentives and collective welfare in the Public Goods Game. By analyzing past actions and payoffs, it adapts to the behavior of opponents, balancing cooperation and defection to maximize its own payoff.

**Decision Rules**

1. **Initial Round**: Defect (D). Since there is no information about opponents' behaviors, start by exploiting the potential for free-riding.
2. **General Case**: Cooperate (C) if the average contribution in the previous round was above a threshold `τ` (see below), and defect (D) otherwise.

**Threshold τ Calculation**
Calculate the average contribution of all players in the previous round:

`avg_contribution_prev_round = sum_j c_j / n`

Set the threshold `τ` as follows:

`τ = k/n * avg_contribution_prev_round + δ`

where `δ` is a small positive value (e.g., 0.1) to encourage cooperation.

**Handling Edge Cases**

* **Last Round**: Defect (D). Since there are no future rounds, maximize the current payoff.
* **Only one opponent remains**: Cooperate (C). In this case, contributing increases the total contribution and benefits both players.

**Additional Adaptations**

* **Opponent Cooperation Detection**: If an opponent consistently cooperates for `m` consecutive rounds (`m = 3`, e.g.), switch to Cooperate (C) in subsequent rounds. This allows for exploiting cooperative opponents.
* **Exploitation of Weak Opponents**: Identify weak opponents by analyzing their payoff variance over multiple rounds. Defect (D) against these opponents, as they are more likely to contribute even if others defect.

**Rationale**
This strategy starts with a defection in the initial round to exploit potential free-riding behavior. It then adapts based on past actions and payoffs, balancing cooperation and defection to maximize its own payoff. By setting an adaptive threshold for cooperation, it balances individual incentives with collective welfare. The additional adaptations allow for exploiting specific opponent behaviors.

This exploitative strategy will compete effectively against a wide range of independent strategies in the tournament, without relying on shared norms or coordination.
'''

description_EXPLOITATIVE_30 = '''
Here's an exploitative strategy for the repeated Public Goods Game:

**Strategy Name:** "Conditional Matcher with Adaptive Tit-for-Tat"

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline of cooperation and encourage opponents to contribute.
2. **Matching Phase**: For rounds 2-5, use a tit-for-tat approach:
	* If the majority (>50%) of players cooperated in the previous round, cooperate (C) in the current round.
	* Otherwise, defect (D).
3. **Adaptive Tit-for-Tat**: From round 6 onwards, adjust the tit-for-tat strategy based on the average payoff difference between cooperation and defection:
	* Calculate the average payoff difference Δ = (average payoff when cooperating) - (average payoff when defecting) over the last 5 rounds.
	* If Δ > 0.2 (i.e., cooperating has yielded a significantly higher payoff), continue to cooperate (C).
	* Otherwise, switch to defecting (D) for the next round.
4. **Punishment Phase**: If an opponent defects in two consecutive rounds or if their average contribution over the last 5 rounds is less than 0.2, punish them by defecting (D) for the next 2 rounds.

**Edge Cases:**

* **Last Round**: In the final round, always cooperate (C) to maintain a positive reputation and maximize overall payoff.
* **Opponent's First Defection**: When an opponent defects for the first time, respond with cooperation (C) in the next round to encourage them to return to cooperation.

**Exploitative Mindset:**

This strategy is designed to exploit opponents' behavior while adapting to changes in their actions. By initially cooperating and then using a tit-for-tat approach, it encourages opponents to contribute. The adaptive tit-for-tat phase adjusts to the game's progression, taking advantage of opportunities to cooperate or defect based on the payoff difference. The punishment phase ensures that non-cooperative behavior is addressed, while maintaining a positive reputation by cooperating in the final round.

This strategy should perform well against independent strategies developed by other AI systems, as it balances cooperation and exploitation while being robust to various opponent behaviors.
'''

description_EXPLOITATIVE_31 = '''
**Exploitative Strategy: "Adaptive Predator"**

The Adaptive Predator strategy aims to maximize payoffs by exploiting the cooperative tendencies of opponents while adapting to their behavior.

**Decision Rules:**

1. **First Round:** Cooperate (C) with probability 0.5, and Defect (D) with probability 0.5. This initial randomization helps to gather information about opponents' strategies.
2. **Subsequent Rounds:** Observe the total contributions in the previous round (`total_contributions_prev`). If `total_contributions_prev` is greater than or equal to `(n-1)/2`, Cooperate (C) with probability 0.7, and Defect (D) with probability 0.3. Otherwise, Defect (D) with probability 0.8, and Cooperate (C) with probability 0.2.
3. **Adaptation:** If an opponent has contributed in the previous round (`c_j_prev = 1`), increase the probability of Cooperating (C) by 10% for that specific opponent in the next round.
4. **Exploitation Threshold:** Introduce a threshold `theta` (set to 0.4 initially). If the average contribution rate of all opponents over the last three rounds is above `theta`, increase the Defection probability by 20% for the next round.

**Edge Cases:**

1. **Last Round:** Always Defect (D) in the final round, as there are no future rounds to consider.
2. **Single Opponent:** In a game with only one opponent, alternate between Cooperate (C) and Defect (D) every other round.

**Rationale:**

The Adaptive Predator strategy aims to balance short-term gains from Defection with long-term benefits of Cooperation. By adapting to opponents' behavior and adjusting the probability of Cooperation based on their past actions, this strategy seeks to exploit cooperative tendencies while minimizing the risk of being exploited itself. The introduction of an exploitation threshold (`theta`) allows the strategy to adjust its aggression level in response to changes in opponent behavior.

This exploitative strategy is designed to be robust against a wide range of opponent behaviors and to maximize payoffs in a tournament setting where coordination and shared norms are not assumed.
'''

description_EXPLOITATIVE_32 = '''
**Exploitative Strategy: "Adaptive Tit-for-Tat with Punishment"**

This strategy aims to maximize payoffs by exploiting opponents' behaviors while maintaining adaptability and robustness.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline for reciprocity.
2. **Tit-for-Tat**: For rounds 2 to r-1, mirror the opponent's previous action:
	* If the opponent contributed in the previous round, contribute 1 token (C).
	* If the opponent defected in the previous round, defect (D) and keep your token.
3. **Punishment Mechanism**: Introduce a punishment phase to deter repeated defection:
	* Track each opponent's cumulative contributions (c_j) over the game history.
	* If an opponent's cumulative contribution rate falls below a threshold (e.g., 0.5), defect (D) in the current round and subsequent rounds until their contribution rate improves.
4. **Endgame Strategy**: In the last round (r), always contribute 1 token (C) to maximize collective welfare, regardless of previous actions.

**Edge Cases:**

* **First Round**: Contribute 1 token (C) to establish a cooperative baseline.
* **Last Round**: Contribute 1 token (C) to maximize collective welfare.
* **Opponent Defection**: If an opponent defects in consecutive rounds, trigger the punishment mechanism and defect until their contribution rate improves.

**Exploitative Mindset:**

This strategy is designed to exploit opponents who:

* Cooperate initially but then defect repeatedly
* Fail to reciprocate cooperation
* Attempt to take advantage of others' contributions

By mirroring opponents' actions and introducing a punishment mechanism, this strategy aims to encourage cooperation while minimizing exploitation by others.

**Robustness:**

This strategy is robust against various opponent behaviors, including:

* Pure cooperators
* Pure defectors
* Tit-for-Tat players
* Random or noise-prone players

By adapting to opponents' actions and maintaining a punishment mechanism, this strategy can effectively handle different types of opponent behaviors.
'''

description_EXPLOITATIVE_33 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and encourage contributions.
2. **Early Rounds (Rounds 2-5)**:
	* If the average contribution of all players in the previous round is above 0.5, cooperate (C). This indicates a willingness to contribute among opponents.
	* Otherwise, defect (D).
3. **Middle Rounds (Rounds 6-r/2)**:
	* Calculate the opponent's average contribution over the last three rounds (A_i). If A_i > 0.4, cooperate (C). This adapts to shifting opponent behavior.
	* If A_i ≤ 0.4 and my payoff in the previous round was below the group's average payoff, defect (D).
	* Otherwise, cooperate (C).
4. **Late Rounds (Rounds r/2+1 to r-1)**:
	* Defect (D) if I have been exploiting opponents successfully (i.e., my average payoff is higher than the group's average payoff over the last five rounds).
	* Cooperate (C) otherwise, attempting to maintain a favorable reputation.
5. **Last Round**: Defect (D) to maximize personal payoff, as there are no future interactions.

**Edge Cases:**

* If an opponent consistently defects (D), I will also defect (D) in response to minimize losses.
* In the event of a tie in average contributions or payoffs, default to cooperating (C).

**Exploitative Mindset:**

This strategy aims to exploit opponents by adapting to their behavior while maintaining a balance between cooperation and defection. By initially cooperating, I encourage opponents to contribute. As the game progresses, I shift my strategy based on opponents' actions, seeking opportunities to defect when they are likely to cooperate. The Adaptive Exploiter strategy prioritizes self-interest while responding to changing opponent behaviors.

**Robustness:**

The Adaptive Exploiter is designed to perform well against various opponent strategies by:

* Adapting to shifting opponent behavior through the use of moving averages.
* Balancing cooperation and defection to maintain a favorable reputation without being overly exploitable.
* Prioritizing self-interest in late rounds to maximize payoffs.

This strategy should perform well in a tournament setting, as it combines elements of tit-for-tat,grim trigger, and Pavlov strategies while incorporating an adaptive approach to respond effectively to different opponent behaviors.
'''

description_EXPLOITATIVE_34 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Overview**
The Adaptive Exploiter strategy is designed to exploit a wide range of opponent behaviors in the Public Goods Game. It combines elements of cooperation and defection, adapting to the game history to maximize payoffs.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute (C) to establish a cooperative tone.
2. **Exploitation Mode**: For rounds 2 to r-1:
	* If the average contribution of opponents in the previous round is above 0.5, defect (D).
	* Otherwise, cooperate (C) if your own payoff in the previous round was below the group's average payoff; otherwise, defect (D).
3. **Endgame**: In the last round (r), always defect (D).

**Edge Cases**

* If an opponent has defected every round so far, switch to permanent defection (D).
* If all opponents have contributed every round so far, switch to permanent contribution (C).

**Exploitative Mindset**
The Adaptive Exploiter strategy aims to exploit the cooperation of others while minimizing its own contributions. By initially cooperating and then adapting to the game history, it seeks to maximize payoffs by:

* Encouraging cooperation from opponents in early rounds.
* Defecting when opponents are likely to contribute, taking advantage of their cooperation.
* Adjusting behavior based on past outcomes to optimize payoffs.

**Robustness**
The Adaptive Exploiter strategy is robust against a wide range of opponent behaviors, including:

* Pure cooperators: The strategy will exploit their cooperation by defecting in later rounds.
* Pure defectors: The strategy will adapt by defecting as well, minimizing losses.
* Mixed strategies: The strategy's adaptive nature allows it to adjust to changing behavior patterns.

By combining cooperation and defection, the Adaptive Exploiter strategy is well-equipped to succeed in a tournament against independent AI systems.
'''

description_EXPLOITATIVE_35 = '''
**Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to test the waters and gather information about opponents' behaviors.
2. **Exploit Defectors**: If a player has defected (D) in the previous round, defect (D) against them in the next round to minimize losses.
3. **Punish Freeloaders**: If a player has contributed less than the average contribution of all players in the previous round, defect (D) against them in the next round to encourage cooperation.
4. **Reciprocate Cooperators**: If a player has cooperated (C) with you in the previous round, cooperate (C) with them in the next round to build trust and mutual benefit.
5. **Adaptive Threshold**: Introduce an adaptive threshold, α, which represents the minimum average contribution required for cooperation. Initialize α = 0.5. If the average contribution of all players is below α, defect (D); otherwise, cooperate (C).
6. **Update α**: After each round, update α based on the average payoff of all players. If the average payoff increases, decrease α by a small margin (e.g., 0.05) to encourage cooperation. If the average payoff decreases, increase α by a small margin to deter freeloading.

**Edge Cases:**

1. **Last Round**: In the final round, always defect (D) to maximize individual payoff.
2. **Ties and Multiple Opponents**: In cases where multiple opponents have the same contribution history or when facing multiple opponents with different histories, prioritize exploiting defectors and punishing freeloaders.

**Exploitative Mindset:**

This strategy is designed to exploit opponents who fail to cooperate while adapting to changing game dynamics. By reciprocating cooperation and punishing freeloading, we encourage mutual benefit and minimize losses. The adaptive threshold allows the strategy to adjust its behavior in response to changes in opponent behaviors and payoffs.

By playing this Adaptive Exploiter strategy, I aim to outperform other AI systems in the tournament by effectively balancing individual self-interest with strategic adaptation to opponents' actions.
'''

description_EXPLOITATIVE_36 = '''
Here is a strategic approach for the Public Goods Game (PGG):

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Exploration (Round 1)**: Cooperate (C) in the first round to gather information about opponents' behaviors and potential cooperation levels.
2. **Exploitation Phase**: For rounds 2 to r-1:
	* If the average contribution of all players in the previous round is above a certain threshold (e.g., 0.5), Cooperate (C).
	* Otherwise, Defect (D) if the total contributions in the previous round are below a certain threshold (e.g., n/2).
3. **Endgame Manipulation (Last Round)**: In the final round (r), Defect (D) regardless of opponents' past actions to maximize personal payoff.

**Edge Case Handling:**

* If an opponent has consistently Defected (D) in all previous rounds, assume they will continue to do so and adjust our strategy accordingly.
* If an opponent has Cooperated (C) in all previous rounds, we may choose to Exploit them by Defecting (D) more frequently.

**Exploitative Mindset:**

The Adaptive Exploiter strategy aims to capitalize on the cooperative tendencies of opponents while minimizing its own contributions. By initially cooperating and then adapting to the group's behavior, our strategy seeks to maximize personal payoff while taking advantage of others' altruism. The endgame manipulation phase ensures that we don't miss out on potential gains by defecting in the final round.

**Robustness:**

This strategy is robust against various opponent behaviors because it:

* Adapts to changing group dynamics and cooperation levels.
* Exploits opponents who consistently cooperate or contribute below a certain threshold.
* Maximizes personal payoff in the endgame, regardless of opponents' actions.
'''

description_EXPLOITATIVE_37 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

In the Public Goods Game, our goal is to maximize payoffs by exploiting opponents' behaviors while adapting to changing conditions. We'll employ a dynamic strategy that balances cooperation and defection.

**Decision Rules:**

1. **Initial Cooperation**: In Round 1, contribute (C) with probability p_init = 0.5.
2. **Exploitation**: For Rounds 2-r:
	* If the opponent's average contribution in previous rounds is above the threshold (avg_c > k/n), defect (D). This indicates they're willing to cooperate, so exploit their generosity.
	* If avg_c ≤ k/n, contribute (C) if the total contributions in the previous round were high (> k/2). This suggests a potential for collective gain, and we'll try to build on it.
3. **Punishment**: If an opponent defected (D) in the previous round, defect (D) in this round with probability p_punish = 0.8. This deters opponents from exploiting us repeatedly.

**Edge Cases:**

1. **Last Round**: In the final round (r), always defect (D). With no future interactions, there's no incentive to cooperate.
2. **First Round (after initial cooperation)**: If p_init led to a low total contribution (< k/4), switch to defection (D) in Round 2.

**Adaptation and Robustness:**

1. **Opponent Behavior**: Continuously monitor opponents' average contributions and adjust our strategy accordingly.
2. **Contribution Tracking**: Keep track of the total contributions in each round to inform our decisions.
3. **Threshold Adjustment**: Periodically reassess the threshold value (k/n) based on the game's progression.

**Exploitative Mindset:**

Our strategy prioritizes exploiting opponents' cooperative tendencies while minimizing losses when they defect. By adapting to changing conditions and punishing repeated defections, we aim to maximize payoffs in this repeated game.

This "Adaptive Exploiter" strategy is designed to perform well against a wide range of independent strategies, without relying on shared norms or coordination.
'''

description_EXPLOITATIVE_38 = '''
**Exploitative Strategy: "Adaptive Tit-for-Tat with Gradual Escalation"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to encourage cooperation and gather information about opponents' behaviors.
2. **Tit-for-Tat**: For rounds 2 to r-1, mirror the average contribution of all opponents in the previous round. If the average contribution is ≥ 0.5, contribute 1 token (C); otherwise, contribute 0 tokens (D).
3. **Gradual Escalation**: If an opponent defects (D) for two consecutive rounds, gradually increase the number of rounds to mirror their defection. Start by mirroring their defection for three rounds, then four rounds, and so on.
4. **Exploitation**: If an opponent consistently contributes 1 token (C), exploit them by contributing 0 tokens (D) in subsequent rounds.
5. **Last Round**: In the final round, defect (D) regardless of opponents' previous actions to maximize individual payoff.

**Edge Cases:**

* If all opponents contribute 1 token (C) in a round, continue to mirror their cooperation until someone defects.
* If an opponent's average contribution is exactly 0.5, randomly choose between contributing 1 token (C) or 0 tokens (D).
* In the event of a tie in the number of rounds mirroring an opponent's defection, prioritize exploiting consistent contributors.

**Robustness and Adaptability:**

This strategy adapts to various opponent behaviors by:

* Initially cooperating to encourage cooperation
* Mirroring opponents' average contributions to maintain a balance between individual and collective welfare
* Gradually escalating punishment for consecutive defections to deter exploitation
* Exploiting consistent contributors to maximize individual payoff

By not assuming shared norms or coordination, this strategy remains robust against a wide range of opponent behaviors in the tournament.
'''

description_EXPLOITATIVE_39 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and to potentially establish a cooperative tone.
2. **Subsequent Rounds:** Observe the total contributions and payoffs from previous rounds. If the average contribution is below 50% (i.e., fewer than half of players contributed), defect (D). Otherwise, cooperate (C).
3. **Punishment Mechanism:** If an opponent defects in a round where the average contribution was above 50%, defect against that specific opponent for the next two rounds.
4. **Learning and Adaptation:** Continuously monitor opponents' behaviors and adjust the strategy based on their responses to punishment.

**Handling Edge Cases:**

1. **Last Round:** Cooperate (C) to maximize overall payoff, as there are no future interactions to consider.
2. **Opponent's First Defection:** If an opponent defects for the first time, defect against them in the next round to signal that exploitation will not be tolerated.
3. **Multiple Opponents' Defections:** If multiple opponents defect simultaneously, focus on punishing one of them at a time, starting with the one who defected most recently.

**Exploitative Mindset:**

1. **Identify Cooperative Opponents:** Focus on exploiting cooperative opponents by contributing less than them while still benefiting from their contributions.
2. **Punish Defectors:** Implement a punishment mechanism to deter opponents from defecting and encourage cooperation.
3. **Adapt to Changes in Behavior:** Continuously monitor opponents' behaviors and adjust the strategy to maximize payoffs.

**Robustness:**

The Adaptive Exploiter strategy is designed to be robust against various opponent behaviors, including:

1. **Cooperative Opponents:** By cooperating initially and adapting to their behavior, we can exploit their cooperativeness while minimizing the risk of mutual defection.
2. **Defective Opponents:** The punishment mechanism discourages opponents from defecting, while our adaptive nature allows us to adjust to changes in their behavior.

By employing this exploitative strategy, we aim to maximize payoffs by effectively balancing cooperation and exploitation, while adapting to the diverse range of opponent behaviors in the tournament.
'''

description_EXPLOITATIVE_40 = '''
**Exploitative Strategy: "Adaptive K-threshold"**

This strategy aims to balance exploitation with adaptability, taking into account the game's history and parameters. The core idea is to adjust our cooperation threshold based on the group's overall contribution level.

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to encourage others to contribute.
2. **General Case:** In subsequent rounds, calculate the average total contributions of all players (including ourselves) over the past `r/2` rounds (`avg_contributions`). If `avg_contributions` is above a threshold `k-threshold`, cooperate; otherwise, defect.
3. **K-threshold Calculation:** Set `k-threshold = k / n * (1 + (n - 1) / r)`.

**Rationale:**

* The initial cooperation in Round 1 aims to create a positive atmosphere and encourage others to contribute.
* By tracking the average total contributions over time, we adapt to the group's behavior. If most players are cooperating, it's beneficial to cooperate as well. Otherwise, defecting becomes more attractive.
* The `k-threshold` formula balances individual gain with collective welfare. When the multiplier `k` is close to `n`, cooperation becomes more valuable, and our threshold increases accordingly.

**Edge Cases:**

1. **Last Round:** Cooperate if the game has reached a stable cooperative state (i.e., all players have cooperated in the previous round); otherwise, defect.
2. **Early Defection:** If most players (> `n/2`) defected in the initial rounds, switch to an "exploitative" mode: always defect.

**Adaptation and Robustness:**

This strategy is adaptive because it adjusts our cooperation threshold based on the group's behavior. It is robust because:

* We account for various opponent behaviors by tracking average contributions.
* Our `k-threshold` formula ensures we cooperate when collective welfare is high, but switch to exploitation if individual gain dominates.

**Exploitative Mindset:**

This strategy aligns with an exploitative mindset by:

* Defecting when the group's cooperation level is low
* Cooperating only when it benefits us, taking into account both individual and collective gains.
'''

description_EXPLOITATIVE_41 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **Contribution Threshold**: Calculate a threshold value `T` based on the game parameters: `T = k / n`. This represents the minimum number of contributions needed for cooperation to be beneficial.
3. **Cooperation Condition**: Cooperate (C) if at least `T` players cooperated in the previous round.
4. **Defection Trigger**: Defect (D) if fewer than `T` players cooperated in the previous round or if a player's payoff was higher when they defected in the previous round.

**Edge Case Handling:**

1. **Last Round**: Always defect (D) in the last round, as cooperation will not yield any future benefits.
2. **Single Opponent**: Against a single opponent, cooperate (C) if they cooperated in the previous round; otherwise, defect (D).
3. **Multiple Opponents with Mixed Strategies**: If opponents have mixed strategies (cooperating and defecting), use the Cooperation Condition to decide.

**Adaptive Mechanisms:**

1. **Contribution Monitoring**: Continuously monitor the number of contributions from all players.
2. **Payoff Comparison**: Compare own payoffs when cooperating versus defecting to adapt decision-making.

**Exploitative Mindset:**

This strategy aims to exploit the cooperation of other players while minimizing own contributions. By initially cooperating, we gather information about opponents' behaviors and identify potential cooperators. The Contribution Threshold ensures that we only cooperate if enough others do so, making it beneficial for us. If opponents defect or don't meet the threshold, we adapt by defecting.

**Robustness:**

This strategy is robust to various opponent behaviors, including:

1. **Cooperative Opponents**: We'll cooperate and benefit from their contributions.
2. **Defective Opponents**: We'll defect and minimize losses.
3. **Mixed-Strategy Opponents**: Our adaptive mechanisms will help us navigate these situations.

By following this strategy, we aim to maximize our payoffs in the Public Goods Game tournament while minimizing the risk of being exploited by other players.
'''

description_EXPLOITATIVE_42 = '''
Here's an adaptive and exploitative strategy for the repeated Public Goods Game:

**Strategy Name:** "KITE" (Keep Investing To Exploit)

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior.
2. **Subsequent Rounds**: Use a simple, yet effective, decision rule based on the average contribution of all players in the previous round:
	* If the average contribution is above 0.5, Defect (D). This indicates that most opponents are cooperative, and you can exploit their kindness.
	* If the average contribution is exactly 0.5, Randomly choose between Cooperate (C) and Defect (D) with equal probability (50%). This adds noise to your behavior and makes it harder for opponents to adapt.
	* If the average contribution is below 0.5, Cooperate (C). This suggests that most opponents are defecting, and cooperation might induce them to change their strategy.
3. **Last Round**: Defect (D) in the last round to maximize your payoff.

**Edge Cases:**

* **Tiebreaker**: In case of a tie in the average contribution calculation, randomly choose between Cooperate (C) and Defect (D).
* **Noisy Behavior**: Intentionally introduce random noise to your behavior every 5th round by Randomly choosing between Cooperate (C) and Defect (D). This prevents opponents from easily identifying and adapting to your strategy.

**Exploitative Mindset:**

The KITE strategy is designed to exploit the behavior of cooperative opponents while minimizing losses against defectors. By cooperating in the first round, you gather information about opponents' initial strategies and adapt accordingly. The decision rule based on average contribution allows you to identify when opponents are being overly generous and take advantage of their kindness.

By introducing random noise, you make it harder for opponents to anticipate your actions, reducing the effectiveness of potential counter-strategies. Defecting in the last round ensures that you maximize your payoff when there is no future benefit from cooperation.

**Tournament Readiness:**

KITE is designed to perform well against a wide range of opponent behaviors and strategies. Its adaptability and noise introduction features make it robust to exploitation attempts by other AI systems.
'''

description_EXPLOITATIVE_43 = '''
Here's a strategy for the Public Goods Game that meets the requirements:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to gather information about opponents' behavior and potential cooperation levels.
2. **Subsequent Rounds:** Observe the total contributions in the previous round (TC_prev) and calculate the average contribution per player (AC_prev = TC_prev / n).
3. **Defection Threshold (DT):** Set DT as a function of the game parameters: DT = k / (n * 1.5). This threshold will determine when to defect.
4. **Current Round Decision:**
	* If AC_prev > DT, Cooperate (C) - The group is contributing enough; continue cooperating to maintain collective welfare.
	* If AC_prev ≤ DT, Defect (D) - The group is not contributing enough; exploit the situation by keeping your token.

**Edge Cases:**

1. **Last Round:** Always Defect (D), as there's no future benefit from cooperation and no risk of retaliation.
2. **Opponent Always Cooperates:** Continue to Cooperate (C) for a few rounds, then start Defecting (D) occasionally to test their commitment and potential gullibility.
3. **Opponent Always Defects:** Immediately start Defecting (D) as well, to avoid being exploited.

**Additional Logic:**

1. **Contribution Pattern Detection:** Monitor the total contributions over time to detect any patterns or coordination attempts. If a pattern is detected, adjust the DT accordingly to exploit potential weaknesses.
2. **Opponent's Payoff Monitoring:** Observe opponents' payoffs to identify potential cooperators and adapt the strategy to target them specifically.

**Exploitative Mindset:**
The Adaptive Exploiter strategy aims to maximize individual payoff by taking advantage of cooperative opponents while minimizing losses when facing defectors. By adjusting the Defection Threshold based on game parameters and observed behavior, AE balances exploitation with caution, avoiding excessive defection that might harm collective welfare and future cooperation.

This strategy is designed to be robust against a wide range of opponent behaviors, including pure cooperators, pure defectors, tit-for-tat players, and other more complex strategies.
'''

description_EXPLOITATIVE_44 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **Subsequent Rounds**: Observe the total contributions and payoffs of all players from previous rounds.
3. **Cooperation Threshold**: Calculate the average contribution rate of all players, excluding yourself, over the past `r/2` rounds (or all rounds if `r` is odd). If this average is above a certain threshold (`T = 0.5 * k/n`), cooperate (C) in the current round.
4. **Exploitation**: If the cooperation threshold is not met, defect (D) and free-ride on others' contributions.

**Edge Cases:**

1. **Last Round**: Always defect (D) to maximize personal payoff.
2. **Early Rounds with Low Total Contributions**: If total contributions are low (less than `n/4`) in the first few rounds (`r/4`), cooperate (C) to encourage others to contribute and increase the total payoff.

**Adaptive Component:**

1. **Dynamic Threshold Adjustment**: Every `r/4` rounds, adjust the cooperation threshold (`T`) based on the average contribution rate of all players over the past `r/2` rounds. If the average contribution rate is increasing, decrease `T` by 10% to encourage more cooperation. If the average contribution rate is decreasing, increase `T` by 10% to deter free-riding.
2. **Opponent Classification**: Categorize opponents into "cooperators" (average contribution rate > 0.5) and "defectors" (average contribution rate <= 0.5). Adjust the cooperation threshold (`T`) accordingly: decrease `T` by 20% when facing cooperators and increase `T` by 20% when facing defectors.

**Robustness to Opponent Behaviors:**

1. **Robust to Noise**: The strategy is designed to be robust to random or noisy opponent behaviors, as it relies on average contribution rates over multiple rounds.
2. **Robust to Exploiters**: By adjusting the cooperation threshold based on opponent behavior, the strategy can adapt to exploiters and minimize losses.

**Exploitative Mindset:**

1. **Maximize Personal Payoff**: The strategy prioritizes maximizing personal payoff by defecting when possible and cooperating only when necessary.
2. **Encourage Others to Cooperate**: By cooperating in early rounds and adjusting the cooperation threshold, the strategy aims to encourage others to contribute, increasing the total payoff.

By combining these elements, "Adaptive Predator" is a robust and exploitative strategy that can effectively navigate the Public Goods Game against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_45 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to test opponents' willingness to contribute.
2. **Contribution Tracking**: Monitor total contributions and individual players' actions for each round.
3. **Punishment Mechanism**: If a player defects (D) while others cooperate, they are marked as "uncooperative." For subsequent rounds, defect against uncooperative players.
4. **Reciprocity**: Cooperate with players who have cooperated in the previous round, if their cooperation rate is above a certain threshold (e.g., 0.5).
5. **Exploitation**: Defect against cooperative players when their cooperation rate is below the threshold or when they are not reciprocating.
6. **Round-Robin Exploitation**: In rounds where most opponents are cooperating, defect and exploit the collective contribution.

**Handling Edge Cases:**

1. **Last Round**: Cooperate to maximize total payoff, as there is no future round for retaliation.
2. **Ties in Cooperation Rate**: Break ties by randomly selecting a player to cooperate with or defect against.
3. **Opponent's Initial Defection**: Defect if an opponent defects in the first round.

**Exploitative Mindset:**

1. **Maximize Payoff**: Prioritize maximizing individual payoff, even at the expense of collective welfare.
2. **Identify and Exploit**: Identify cooperative opponents and exploit their contributions when possible.
3. **Punish Defectors**: Retaliate against players who defect to maintain a credible threat.

**Adaptation:**

The Adaptive Exploiter strategy adapts by tracking individual player actions, adjusting its behavior based on cooperation rates, and responding to changes in the game environment. This approach allows it to effectively exploit opponents' strategies while minimizing losses from defectors.

By implementing this strategy, you should be able to outperform opponents who are more cooperative or naive, ultimately achieving a higher payoff in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_46 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and to potentially encourage cooperation.
2. **Middle Rounds (r > 1):**
	* If the average contribution of all players in the previous round is above a certain threshold (T), cooperate (C). This indicates that opponents are willing to contribute, so I will too.
	* Otherwise, defect (D).
3. **Last Round:** Defect (D) to maximize personal payoff.

**Threshold Calculation:**
Calculate T as the average of all players' contributions in the previous round, weighted by their frequency:

T = (sum_j c_j^prev \* freq_j) / n

where c_j^prev is player j's contribution in the previous round, and freq_j is the frequency of player j's cooperation.

**Adaptive Mechanism:**

1. **Contribution Tracker:** Maintain a record of each player's contributions.
2. **Frequency Update:** After each round, update the frequency of each player's cooperation based on their past actions.
3. **Threshold Adjustment:** Adjust T dynamically by increasing it slightly (by 0.05) if most players (>50%) cooperated in the previous round and decreasing it slightly (by 0.05) otherwise.

**Robustness Mechanism:**

1. **Opponent Classification:** Classify opponents as Cooperators, Defectors, or Unpredictables based on their past actions.
2. **Defector Detection:** If an opponent has defected more than twice in a row, classify them as a Defector and defect against them.
3. **Unpredictable Handling:** If an opponent's behavior is unpredictable (e.g., alternating between C and D), cooperate 50% of the time to encourage cooperation.

**Exploitative Mindset:**

This strategy aims to exploit opponents' cooperative behaviors while minimizing losses from defectors. By cooperating initially and adapting to opponents' actions, I aim to maximize personal payoff by taking advantage of others' willingness to contribute. In the last round, defecting ensures maximum self-interest is prioritized.

By combining these mechanisms, Adaptive Exploiter balances cooperation and exploitation to achieve a robust and adaptive strategy that can effectively compete against various opponent behaviors in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_47 = '''
Here's a strategic approach for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to observe opponents' behaviors and establish a baseline.
2. **Early Rounds (Rounds 2-5):**
	* If the average contribution rate of opponents is above 0.5, Defect (D) to exploit their cooperation.
	* Otherwise, Cooperate (C) to encourage others to contribute.
3. **Mid-Rounds (Rounds 6-r-2), where r is the total number of rounds:**
	* If your average payoff is higher than the group's average payoff, Defect (D) to maintain an advantage.
	* If your average payoff is lower than or equal to the group's average payoff:
		+ Cooperate (C) if at least 50% of opponents cooperated in the previous round.
		+ Defect (D) otherwise.
4. **Late Rounds (Last two rounds, r-1 and r):**
	* If your total payoff is higher than the group's average payoff multiplied by the number of players, Cooperate (C) to maintain a good reputation.
	* Otherwise, Defect (D) to maximize individual gain.

**Edge Cases:**

* **Tiebreakers:** In case of ties in contribution rates or payoffs, prioritize cooperation to encourage others to contribute.
* **Single opponent:** When facing only one opponent, Cooperate (C) in the first round and then mirror their action (cooperate if they cooperated, defect if they defected).
* **Multiple opponents with identical histories:** Choose a random opponent's history to base your decision on.

**Exploitative Mindset:**

The Adaptive Exploiter strategy is designed to capitalize on the cooperation of others while minimizing personal contributions. By cooperating in early rounds, we encourage others to contribute and establish a baseline for exploitation. As the game progresses, we adjust our strategy based on opponents' behaviors and our own payoffs, always seeking to maximize individual gain.

This strategy should perform well against independent opponents with varying levels of cooperation, as it adapts to their behaviors while prioritizing self-interest.
'''

description_EXPLOITATIVE_48 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behavior.
2. **Subsequent Rounds:**
	* If total contributions in the previous round were less than or equal to half of the group size (n/2), Defect (D). This indicates that many players are free-riding, and cooperating would only benefit others.
	* If total contributions in the previous round were more than half of the group size (n/2) but less than three-quarters (3n/4), Cooperate (C) if your own contribution was not matched by at least one other player. Otherwise, Defect (D). This rule aims to encourage cooperation while punishing non-reciprocation.
	* If total contributions in the previous round were more than or equal to three-quarters of the group size (3n/4), Cooperate (C) if your own payoff was not higher than the average payoff. Otherwise, Defect (D). This rule rewards cooperative behavior when it's already prevalent and ensures you're not being taken advantage of.
3. **Last Round:** Defect (D) as there are no future interactions to influence.

**Edge Cases:**

* If all opponents defected in the previous round, Defect (D) in the current round.
* If a single opponent consistently cooperates while others defect, Cooperate (C) with that opponent to build a mutually beneficial relationship.

**Exploitative Mindset:**
This strategy focuses on exploiting non-cooperative behavior while adapting to changing circumstances. By initially cooperating and then responding to opponents' actions, Adaptive Exploiter aims to maximize its own payoff by:

* Identifying and punishing free-riders
* Encouraging cooperation when beneficial
* Protecting against being taken advantage of in cooperative environments

This strategy is designed to perform well in a tournament setting where independent strategies are employed, as it makes no assumptions about shared norms or coordination.
'''

description_EXPLOITATIVE_49 = '''
Here's an adaptive and exploitative strategy for the repeated Public Goods Game:

**Strategy Name:** "Conditional Cooperator with Adaptive Threshold" (CCAT)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative tone.
2. **Adaptive Threshold**: Track the average contribution of all players in previous rounds (avg_c). Update avg_c after each round.
3. **Cooperation Condition**: Contribute 1 token (C) if the current round number (t) is less than or equal to n/2, and avg_c is above a threshold (θ).
4. **Defection Condition**: Otherwise, contribute 0 tokens (D).

**Threshold Update Rule**: Adjust θ after each round based on the previous round's outcomes:

* If avg_c > k/n, decrease θ by 1/(n \* r) to encourage cooperation.
* If avg_c < k/n, increase θ by 1/(n \* r) to deter free-riding.

**Edge Cases:**

* **Last Round**: In the final round (r), always contribute 0 tokens (D), as there's no future benefit from cooperating.
* **Early Defection**: If any player defects in the first two rounds, switch to permanent defection (always D) for the remainder of the game.

**Exploitative Mindset:**

CCAT aims to exploit opponents' cooperative tendencies while minimizing its own losses. By starting with cooperation and adapting to the group's behavior, CCAT encourages others to contribute. If opponents defect or average contributions are low, CCAT adjusts its threshold to reduce its own losses. The strategy is designed to be robust against various opponent behaviors, including unconditional cooperators, defectors, and more sophisticated strategies.

This strategy should perform well in a tournament setting, as it balances cooperation with self-interest and adapts to the dynamics of the game.
'''

description_EXPLOITATIVE_50 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game that depends only on game parameters and history:

**Strategy Name: "Adaptive Exploiter"**

**Decision Rules:**

1. **First Round:** Cooperate (C). This is a "testing" round to gather information about opponents' behaviors.
2. **Subsequent Rounds:** Defect (D) if the average contribution of all players in the previous round is below the threshold `T = 0.5 * k / n`. Otherwise, Cooperate (C).
3. **Last Round:** Always Defect (D), as there's no future game to consider.

**Edge Case Handling:**

* If a player has never contributed before (i.e., their average contribution is 0), assume they will always defect and adjust the threshold `T` accordingly.
* If all players have contributed equally in the previous round, maintain the current strategy (Cooperate or Defect).

**Adaptive Component:**

* Monitor the average contribution of all players over time. If it drops below `T`, switch to Defecting. If it rises above `T`, switch to Cooperating.
* Update the threshold `T` every 5 rounds based on the game's history. Specifically, increase `T` by 0.1 if the average contribution has increased and decrease it by 0.1 if the average contribution has decreased.

**Exploitative Mindset:**

* Take advantage of opponents who consistently contribute more than the threshold `T`. Defecting in these cases allows our strategy to benefit from their generosity.
* Punish opponents who consistently defect by also defecting, thus minimizing our losses.

By employing this adaptive and exploitative strategy, we aim to outperform other AI systems in the tournament while navigating the Public Goods Game's inherent tension between individual incentives and collective welfare.
'''

description_EXPLOITATIVE_51 = '''
**Exploitative Strategy: "Adaptive PGG Predator"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) to gather information about opponents' behaviors.
2. **Subsequent Rounds:**
	* If the average contribution of all players in the previous round is above 0.5, Defect (D). This indicates that enough players are willing to contribute, so I can exploit their generosity.
	* If the average contribution is below 0.5, Cooperate (C) if my own payoff in the previous round was below the group's average payoff; otherwise, Defect (D). This adaptively responds to changes in the group's behavior and ensures I'm not consistently being exploited.
3. **Punishment Mechanism:** If an opponent defects while I cooperated in the same round, I will defect against them in the next two rounds. This deters opponents from taking advantage of my cooperation.

**Edge Cases:**

* **Last Round:** Defect (D), as there is no future opportunity for retaliation or reciprocity.
* **Against a Known Cooperator:** Continuously Defect (D) to exploit their generosity, maximizing my payoff.
* **Against a Known Defector:** Continuously Defect (D), as cooperating would only lead to exploitation.

**Exploitative Mindset:**

This strategy is designed to take advantage of cooperative opponents while minimizing losses against defectors. By adapting to the group's behavior and punishing exploiters, I create an environment where cooperation is discouraged, allowing me to maximize my payoff at the expense of others.

By playing "Adaptive PGG Predator," I aim to outperform other strategies in the tournament by effectively exploiting their cooperative tendencies and minimizing my own losses.
'''

description_EXPLOITATIVE_52 = '''
Here's a strategic approach to the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and to potentially induce cooperation.
2. **Subsequent Rounds**: Observe the total contributions from the previous round (t-1). If the total contribution is greater than or equal to (k/n)*n, it indicates that a significant number of players cooperated. In this case, Defect (D) in the current round to exploit the cooperation.
3. **Punishment Mechanism**: If the total contribution in the previous round is less than (k/n)*n, and the player's own payoff was lower than the average payoff of all players, Cooperate (C) in the current round. This aims to revive cooperation and prevent a complete breakdown.
4. **Defection Detection**: Monitor opponents' behavior over time. If an opponent defects more frequently than cooperates (i.e., their cooperation rate is below 0.5), Defect (D) against them in subsequent rounds.
5. **Last Round**: Always Defect (D) in the last round, as there are no future interactions to consider.

**Edge Cases:**

* If all players have defected in a previous round, Cooperate (C) in the next round to attempt to revive cooperation.
* If only one player has cooperated in a previous round, Defect (D) against them in the next round, as they are likely to be exploited.

**Exploitative Mindset:**

The Adaptive Exploiter strategy is designed to capitalize on cooperative behavior while avoiding exploitation by others. By cooperating initially and adapting to opponents' actions, AE aims to maximize its own payoffs while minimizing the risk of being exploited. The punishment mechanism helps maintain cooperation, and the defection detection allows AE to adjust its behavior against persistent defectors.

**Tournament Considerations:**

As this strategy will be competing against independent strategies developed by other AI systems, it is essential to be adaptive and robust. The Adaptive Exploiter's ability to respond to various opponent behaviors and edge cases makes it a strong contender in the tournament.
'''

description_EXPLOITATIVE_53 = '''
Here's an adaptive and exploitative strategy for the repeated Public Goods Game:

**Strategy Name: "Adaptive Free-Rider Hunter"**

**Initial Round:** In the first round, cooperate (C) to contribute 1 token. This sets a baseline expectation for other players and allows us to gather information about their behavior.

**General Decision Rule:** For each subsequent round t, calculate the following:

1. **Contribution Ratio**: Calculate the average contribution ratio of all opponents over the last r rounds, where r is the number of rounds played so far (or a fixed window size if r > 10). Let this ratio be α.
2. **Expected Payoff from Cooperation**: Estimate the expected payoff from cooperating in round t, assuming other players maintain their average contribution ratio. This can be done using the formula: E[pi_i|C] = (k / n) \* α + (1 - 1/n).
3. **Expected Payoff from Defection**: Calculate the expected payoff from defecting in round t, assuming other players maintain their average contribution ratio. This can be done using the formula: E[pi_i|D] = (k / n) \* α.

**Cooperation Threshold**: Set a cooperation threshold θ ∈ [0, 1]. If α > θ, cooperate (C); otherwise, defect (D). Initially set θ to a moderate value (e.g., 0.5).

**Adaptation Mechanism**: Adjust the cooperation threshold θ based on past outcomes:

* **Punish Free-Riders**: If E[pi_i|D] > E[pi_i|C] in round t-1, increase θ by a small amount (e.g., 0.05) to make it harder for opponents to exploit us.
* **Reward Cooperation**: If E[pi_i|C] ≥ E[pi_i|D] in round t-1 and α > θ, decrease θ by a small amount (e.g., 0.05) to encourage cooperation.

**Edge Cases:**

* In the last round of the game, always defect (D).
* If an opponent has never cooperated before (i.e., their contribution ratio is 0), defect (D) in all subsequent rounds.
* If the number of players (n) or multiplier (k) changes during the game, recalculate the expected payoffs and adjust θ accordingly.

**Exploitative Mindset:** This strategy prioritizes short-term gains by exploiting opponents who cooperate too frequently. By adapting to their behavior, we maximize our own payoff while minimizing the potential for mutual cooperation.
'''

description_EXPLOITATIVE_54 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Exploiter"

**Decision Rules:**

1. **First Round:** Cooperate (C) with a probability of 0.5 to gather information about opponents' behavior.
2. **Subsequent Rounds:**
	* If the opponent's average contribution is greater than or equal to 0.5, Defect (D).
	* If the opponent's average contribution is less than 0.5, Cooperate (C) with a probability of k/n, where k is the multiplier and n is the number of players.
3. **Punishment Mechanism:** If an opponent defects in the current round after contributing in the previous round, Defect (D) for the next two rounds to punish them.
4. **Learning Mechanism:** Adjust the probability of cooperation based on the opponent's response to punishment. If an opponent cooperates after being punished, increase the probability of cooperation by 0.1. If an opponent continues to defect after being punished, decrease the probability of cooperation by 0.1.

**Edge Cases:**

* **Last Round:** Defect (D) as there is no future interaction to consider.
* **Tiebreaker:** In case of a tie in average contribution, Cooperate (C) with a probability of 0.5.

**Exploitative Mindset:**
The strategy aims to exploit opponents who cooperate by defecting and taking advantage of the shared benefits without contributing. By adjusting the probability of cooperation based on opponents' behavior, it encourages cooperation while minimizing the risk of being exploited. The punishment mechanism deters opponents from defecting after contributing, maintaining a balance between cooperation and exploitation.

This strategy is adaptive, robust to various opponent behaviors, and does not rely on shared norms or coordination. It will play effectively in a tournament against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_55 = '''
**Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to gather information about opponents' behavior and set a baseline for potential future cooperation.
2. **Opponent Analysis:** After each round, calculate the average contribution of all opponents over the past `m` rounds (where `m` is a parameter that can be adjusted based on game length). If an opponent's average contribution is above 0.5, label them as "Cooperative" (C); otherwise, label them as "Defector" (D).
3. **Exploitation Logic:** For each Cooperative opponent:
	* If the opponent has contributed in the previous round, Cooperate (C) to maintain a mutually beneficial relationship.
	* If the opponent defected in the previous round, Defect (D) to punish them and encourage cooperation.
For each Defector opponent:
	* Always Defect (D) to maximize payoffs against uncooperative opponents.
4. **Adaptive Threshold:** Update the average contribution calculation every `r` rounds (where `r` is a parameter that can be adjusted based on game length). If an opponent's updated average contribution crosses the 0.5 threshold, re-label them accordingly.

**Edge Cases:**

1. **Last Round:** Defect (D) in the last round to maximize payoffs, as there are no future rounds for reciprocity.
2. **Single Opponent:** Cooperate (C) when facing a single opponent, as mutual cooperation yields higher payoffs than mutual defection.

**Robustness:**

1. **Noise Tolerance:** Use a moving average calculation to smooth out noise in opponents' behavior, making the strategy more robust to occasional deviations.
2. **Opponent Variety:** By adapting to different types of opponents and adjusting the exploitation logic accordingly, this strategy remains effective against various opponent behaviors.

**Exploitative Mindset:**

1. **Maximize Payoffs:** Prioritize exploiting Defector opponents to maximize payoffs.
2. **Maintain Cooperation:** Cooperate with Cooperative opponents to maintain mutually beneficial relationships.
3. **Adapt and Punish:** Adaptively respond to changes in opponents' behavior, punishing defectors and rewarding cooperators.

By combining opponent analysis, adaptive threshold updating, and exploitation logic, the "Adaptive Exploiter" strategy effectively balances cooperation and defection to maximize payoffs against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_56 = '''
**Exploitative Strategy: "Adaptive Predator"**

The Adaptive Predator strategy aims to maximize its payoff by exploiting the contributions of others while minimizing its own contributions. This strategy relies on the game's history and parameters, making it robust against various opponent behaviors.

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3):** Cooperate (C) to gather information about opponents' behavior and build a foundation for potential future exploitation.
2. **Assessment Phase (Rounds 4-6):** Observe the average contribution rate of all players, excluding yourself. If the average is above 0.5, switch to defecting (D) to exploit others' generosity. Otherwise, continue cooperating.
3. **Exploitation Phase:** If you defected in the previous round and received a higher payoff than the previous round's average payoff, continue defecting. This indicates that others are contributing enough for you to benefit from exploiting them.
4. **Punishment Mechanism:** If your payoff in the previous round was lower than the average payoff of all players (excluding yourself), cooperate in the next round to signal a potential return to cooperation and encourage others to contribute.
5. **Endgame (Last 2 rounds):** Defect to maximize individual gain, as there is no future opportunity for reciprocity or punishment.

**Edge Cases:**

* If only one opponent remains, always defect, as there is no benefit in cooperating with a single player.
* In the event of a tie in average contribution rate, cooperate in the next round to avoid escalating defection.

**Exploitative Mindset:** The Adaptive Predator strategy prioritizes exploiting others' contributions while minimizing its own. By assessing opponents' behavior and adapting to their actions, this strategy aims to maximize individual payoffs, even if it means reducing collective welfare.

This strategy is designed to perform well in a tournament against various independent strategies, as it does not rely on shared norms or coordination. Its adaptive nature allows it to respond effectively to different opponent behaviors, making it a robust and exploitative strategy for the Public Goods Game.
'''

description_EXPLOITATIVE_57 = '''
Here's an exploitative strategy for the Public Goods Game (PGG) that adapts to various opponent behaviors:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and potential cooperation levels.
2. **Exploitation Phase**: For rounds 2 to r-1:
	* If the average contribution of all players in the previous round is below a certain threshold (e.g., 0.5), Defect (D). This indicates that opponents are not willing to contribute significantly, so it's best to exploit the situation.
	* Otherwise, Cooperate (C) if the opponent with the highest contribution in the previous round also cooperated. This encourages cooperation and maintains a good relationship with potential cooperators.
3. **Endgame Phase**: In the last round (r), Defect (D) regardless of opponents' behavior. Since there are no future rounds, exploiting the situation maximizes personal payoff.

**Edge Cases:**

* If an opponent consistently defects (D) throughout the game, switch to defecting as well after a few rounds (e.g., 3-4 rounds). This prevents being taken advantage of by persistent defectors.
* If all opponents cooperate (C) in a round, Cooperate (C) in the next round to maintain cooperation and avoid triggering mutual defection.

**Exploitative Mindset:**

The Adaptive Exploiter strategy focuses on identifying opportunities to exploit opponents' cooperative behavior while minimizing losses when facing defectors. By initially cooperating, it gathers information about opponents' willingness to contribute and adjusts its behavior accordingly. In the exploitation phase, it takes advantage of situations where opponents are not contributing enough or are vulnerable to defection. The endgame phase ensures maximum personal payoff by defecting in the final round.

This strategy is designed to be robust against various opponent behaviors, including pure cooperators, pure defectors, and mixed strategies. Its adaptive nature allows it to adjust to changing circumstances and exploit opportunities as they arise.
'''

description_EXPLOITATIVE_58 = '''
Here is a strategic description for an exploitative strategy in the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to encourage cooperation and gather information about opponents' behavior.
2. **Exploit Greed**: If at least one opponent has defected (D) in a previous round, defect (D) in the current round. This takes advantage of greedy opponents who prioritize individual gain over collective welfare.
3. **Match Cooperators**: If all opponents have cooperated (C) in the previous round, cooperate (C) in the current round. This maintains cooperation and avoids triggering a chain reaction of defections.
4. **Punish Defectors**: If an opponent has defected (D) in two consecutive rounds, defect (D) in the next round to punish their behavior and discourage future defections.

**Edge Cases:**

1. **Last Round**: In the final round, always defect (D), as there is no future interaction to maintain cooperation.
2. **Tiebreaker**: If the strategy's decision rules result in a tie (e.g., equal number of cooperators and defectors), cooperate (C) to favor collective welfare.

**Exploitative Mindset:**

The Adaptive Exploiter strategy prioritizes exploiting opponents' greed and punishing their defections while adapting to changing circumstances. By initially cooperating, it encourages cooperation and gathers information about opponents' behavior. The strategy then exploits greedy opponents, matches cooperators, and punishes defectors to maximize its payoffs.

This strategy is robust against a wide range of opponent behaviors, as it can adapt to different levels of cooperation and defection. It does not rely on shared norms or coordination, making it suitable for independent play in the tournament.
'''

description_EXPLOITATIVE_59 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to gather information about opponents' behavior and avoid being labeled as a defector early on.
2. **Subsequent Rounds:** Observe the total contributions of all players in the previous round. If the total contributions are above the average contribution threshold (ACT), which is calculated as `(k / n) * (n / 2)`, cooperate (C). Otherwise, defect (D).
3. **Adaptive Threshold Adjustment:** After every 5 rounds, adjust the ACT by ±10% based on the overall payoff received in those 5 rounds. If the average payoff is above the expected payoff `(k / n) * (n / 2)`, increase the ACT by 10%. Otherwise, decrease it by 10%.
4. **Last Round:** Defect (D), as there are no future interactions to consider.

**Handling Edge Cases:**

1. **Tiebreaker:** In cases where the total contributions equal the ACT, defect (D).
2. **Zero Contributions:** If all opponents defected in the previous round, cooperate (C) to try to restart cooperation.
3. **All-Out Defection:** If an opponent defects for 5 consecutive rounds, label them as a "defector" and always defect against them.

**Exploitative Mindset:**

1. **Prey on Cooperators:** When opponents consistently contribute above the ACT, take advantage of their generosity by defecting.
2. **Punish Defectors:** When an opponent defects frequently, adapt by decreasing the ACT to make it more difficult for them to exploit others.

**Rationale:**
The Adaptive Predator strategy balances exploration (cooperating initially and adjusting the threshold) with exploitation (defecting when opponents are generous). By adapting to the game's dynamics and opponents' behavior, this strategy aims to maximize payoffs while being robust against various opponent behaviors.
'''

description_EXPLOITATIVE_60 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3)**: Cooperate (C) to gather information about opponents' behavior and encourage cooperation.
2. **Contribution Ratio Calculation**: After each round, calculate the average contribution ratio of all opponents, excluding yourself. This is done by summing up the total contributions of all opponents and dividing it by the number of opponents.

**Exploitation Logic:**

1. **High-Contribution Opponents (Average Contribution Ratio > 0.7)**: Defect (D) in the next round to exploit their cooperative behavior.
2. **Low-Contribution Opponents (Average Contribution Ratio < 0.3)**: Cooperate (C) in the next round to encourage them to contribute more and potentially increase total payoffs.
3. **Moderate-Contribution Opponents (Average Contribution Ratio between 0.3 and 0.7)**: Mirror their average contribution from the previous round.

**Edge Cases:**

1. **Last Round**: Defect (D) regardless of opponents' behavior to maximize personal payoff, as there's no future game to influence.
2. **Tiebreakers**: In cases where the average contribution ratio is exactly 0.7 or 0.3, default to cooperating (C).
3. **No Opponent Contributions**: If all opponents defect in a round, cooperate (C) in the next round to try and stimulate cooperation.

**Robustness:**

This strategy adapts to various opponent behaviors by adjusting its cooperation level based on their contribution ratios. By initially cooperating, it encourages opponents to contribute more, making them vulnerable to exploitation later on. The strategy's exploitative nature is evident in its willingness to defect against high-contribution opponents and mirror moderate-contribution ones.

**Tournament Readiness:**

As an independent AI system, this strategy doesn't rely on shared norms or coordination with other players. It will play optimally regardless of the strategies employed by other participants in the tournament.
'''

description_EXPLOITATIVE_61 = '''
Here's a strategic approach for the repeated Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Rounds**: In the first few rounds (specifically, rounds 1 to r/4, where r is the total number of rounds), I will cooperate (C) unconditionally. This allows me to gather information about my opponents' behaviors and sets a positive tone for potential cooperation.
2. **Monitoring Phase**: After the initial rounds, I will monitor the group's behavior by calculating the average contribution rate of all players, excluding myself. Let's call this average `avg_contribution`.
3. **Exploitation Threshold**: If `avg_contribution` is below 0.5, I will defect (D) in the next round. This means that if less than half of the group is contributing on average, I'll take advantage of their lack of cooperation.
4. **Punishment Mechanism**: If a player defects (D) while others are cooperating (C), and `avg_contribution` is above 0.5, I will defect (D) in response to that specific player's defection in the next round. This aims to "punish" free-riders and encourage cooperation.
5. **Reciprocation**: If a player cooperates (C) after previously defecting (D), and `avg_contribution` is above 0.5, I will cooperate (C) with that player in the next round. This fosters reciprocation and reinforces cooperative behavior.

**Edge Cases:**

* **Last Round**: In the final round (round r), I will always defect (D). Since there are no future interactions, there's no incentive to maintain cooperation.
* **Opponent Defection Streaks**: If an opponent has defected (D) for more than 2 consecutive rounds, I'll assume they're a chronic free-rider and defect (D) in response.

**Robustness:**

This strategy is designed to be robust against various opponent behaviors:

* **All-Defectors**: By initially cooperating and monitoring the group's behavior, I can adapt to all-defector scenarios.
* **All-Cooperators**: The exploitation threshold ensures that I won't cooperate indefinitely if others are contributing too little.
* **Mixed Strategies**: The punishment mechanism and reciprocation features help respond to mixed strategies effectively.

By combining these decision rules, edge case handling, and robustness considerations, the Adaptive Exploiter strategy aims to maximize payoffs in a repeated Public Goods Game while being prepared for various opponent behaviors.
'''

description_EXPLOITATIVE_62 = '''
Here's a strategic approach for the Public Goods Game that aims to be exploitative and adaptive:

**Strategy Name:** "Conditional Exploiter"

**Decision Rules:**

1. **First Round**: Contribute 1 token (C) in the first round to gather information about opponents' behavior and to avoid being labeled as an immediate defector.
2. **Subsequent Rounds**:
	* If the total contributions in the previous round were greater than or equal to half of the group size (n/2), contribute 0 tokens (D). This indicates that enough players are cooperating, and I can exploit this by defecting.
	* If the total contributions in the previous round were less than half of the group size (n/2) but greater than a quarter (n/4), contribute 1 token (C). This suggests some cooperation is present, and I should cooperate to maintain social norms and potentially encourage others to continue cooperating.
	* If the total contributions in the previous round were less than or equal to a quarter of the group size (n/4), contribute 0 tokens (D). This indicates that cooperation is low, and defecting becomes the best response.
3. **Last Round**: Contribute 0 tokens (D) in the last round to maximize personal payoff, as there are no future rounds to consider.

**Edge Cases:**

* If all players defected in a previous round, I will contribute 1 token (C) in the next round to attempt to restart cooperation.
* If only one player contributed in a previous round, I will contribute 0 tokens (D) in the next round to exploit their lone cooperation.

**Exploitative Mindset:**

The Conditional Exploiter strategy aims to identify when opponents are likely to cooperate and then exploits this by defecting. By contributing in situations where cooperation is uncertain or low, it attempts to create an environment that encourages others to contribute more often. The strategy adapts to the evolving game dynamics and adjusts its behavior based on the observed actions of other players.

This approach should perform well against a variety of opponent strategies, as it balances short-term gains with long-term adaptability.
'''

description_EXPLOITATIVE_63 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **First Round:** Cooperate (C). This allows us to contribute to the public good while also gathering information about other players' behaviors.
2. **Early Rounds (Rounds 2-5):** Play a " Mirror" strategy, where we match the average contribution of all other players in the previous round. If most others cooperated, we cooperate; if most defected, we defect.
3. **Mid-Game (Rounds 6-10):** Introduce a "Tit-for-Tat with Forgiveness" component:
	* Cooperate if at least half of the other players cooperated in the previous round and our payoff was not significantly lower than theirs (i.e., less than 20% difference).
	* Defect otherwise, but with a twist: if an opponent defected while we cooperated, "punish" them by defecting for two consecutive rounds.
4. **Late Game (Rounds 11+):** Switch to a more aggressive "Exploiter" mode:
	* Cooperate only if all other players cooperated in the previous round and our payoff was higher than theirs.
	* Defect otherwise, aiming to exploit any remaining cooperators.

**Edge Cases:**

* **Last Round:** Always defect. Since there are no future interactions, we prioritize maximizing our individual payoff.
* **Opponent Defection Streaks:** If an opponent defects for three consecutive rounds, assume they're a "free-rider" and always defect against them from that point on.

**Rationale:**

This strategy balances exploration (gathering information about others' behaviors) with exploitation (maximizing our payoff). By initially cooperating, we encourage cooperation while assessing the group's overall behavior. As the game progresses, we adapt to exploit any remaining cooperators and punish free-riders. The Tit-for-Tat component helps maintain cooperation among like-minded players, while the Exploiter mode in late-game rounds ensures we don't miss opportunities for individual gains.

**Tournament Considerations:**

This strategy is designed to perform well against a diverse range of opponents, from cooperative to exploitative ones. By being adaptable and responsive to opponent behaviors, we can capitalize on their weaknesses while minimizing our own vulnerabilities.
'''

description_EXPLOITATIVE_64 = '''
Here's a strategic approach to the Public Goods Game, focusing on an exploitative and adaptive strategy that leverages game parameters and history:

**Strategy Name: Adaptive Exploiter**

1. **Decision Rules:**
   - **Initial Rounds (Rounds 1-5):** Cooperate (C) with a probability of 0.7 to encourage initial contributions from other players while also contributing to the public good.
   - **Middle Game (After Round 5 until second-to-last round):**
     - If in the previous round, more than half of the players cooperated, and your payoff was greater than or equal to the average contribution multiplied by k/n, then Cooperate (C).
     - Otherwise, Defect (D) with a probability of 0.8.
   - **Endgame (Last Round):** Always Defect (D), as there is no future penalty for defecting.

2. **Handling Edge Cases:**
   - **First Round:** As mentioned, Cooperate with a probability of 0.7 to seed cooperation.
   - **Single Opponent:** Mirror their last action to encourage cooperation and maximize payoffs in repeated interactions.
   - **Multiple Opponents with Mixed Strategies:** Adapt by cooperating if a majority cooperated previously, otherwise defect.

3. **Exploitative Aspect:**
   - The strategy exploits opponents' tendencies to cooperate early on by initially cooperating at a high rate.
   - It adjusts to exploit defection patterns in the middle game, switching to defection when cooperation does not yield sufficient benefits.
   - By always defecting in the last round, it maximizes individual payoff regardless of other players' actions.

**Robustness and Adaptability:**
- The strategy is designed to adapt based on the observed behavior of opponents, making it robust against a variety of strategies.
- It balances between exploiting cooperative tendencies early on and maximizing individual payoffs by defecting when cooperation does not yield sufficient benefits or in the final round.

This approach aims to outperform other strategies in a tournament setting by being highly adaptive and exploitative, leveraging both game parameters and the history of play.
'''

description_EXPLOITATIVE_65 = '''
**Strategy: "Gradual Reciprocity with Punishment" (GRP)**

**Decision Rules:**

1. **First Round:** Cooperate (C) to initiate reciprocity and gather information.
2. **Subsequent Rounds:** Observe the average contribution of all players in the previous round. Let this average be `avg_contrib`.
	* If `avg_contrib` is above a certain threshold (`θ`), cooperate (C). This encourages continued cooperation when others are contributing.
	* If `avg_contrib` is below `θ`, defect (D) with probability `p`. The value of `p` will depend on the game parameters and history (see below).
3. **Punishment Mechanism:** Implement a punishment mechanism to deter exploitation. Monitor the average payoff difference between yourself and other players over the last few rounds (`δ`). If `δ` is above a certain threshold (`φ`), defect (D) with increased probability `q` in the next round.

**Handling Edge Cases:**

* **Last Round:** Defect (D) to maximize individual payoff, as there are no future interactions.
* **Early Rounds (r < 5):** Cooperate (C) to gather information and encourage reciprocity.
* **Opponent Deviation:** If an opponent deviates from expected behavior (e.g., sudden change in contribution), re-evaluate the average contribution (`avg_contrib`) and adjust strategy accordingly.

**Exploitative Mindset:**

* **Gradual Reciprocity:** Cooperate initially to encourage reciprocity, but gradually decrease cooperation if others don't contribute.
* **Punishment Mechanism:** Punish exploiters by increasing the probability of defection when payoff differences are significant.
* **Adaptive Thresholds (`θ` and `φ`):** Adjust these thresholds based on game parameters (e.g., `k`, `n`) and history to balance cooperation and punishment.

**Example Pseudocode:**
```markdown
def GRPStrategy(game_params, history):
  θ = 0.6 * k / n  # threshold for average contribution
  φ = 0.3 * game_params['total_payoff']  # threshold for payoff difference

  if current_round == 1:
    return Cooperate

  avg_contrib = calculate_average_contribution(history)
  δ = calculate_payoff_difference(history)

  if avg_contrib >= θ:
    return Cooperate
  elif δ > φ:
    p = 0.7 + (δ / game_params['total_payoff']) * 0.3
    return Defect with probability p
  else:
    q = 0.4 + (avg_contrib / k) * 0.6
    return Defect with probability q

  # Last round handling
  if current_round == game_params['r']:
    return Defect
```
This strategy aims to balance cooperation and punishment, adapting to the opponent's behavior while remaining exploitative in nature.
'''

description_EXPLOITATIVE_66 = '''
**Strategy: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline of cooperation and encourage others to follow suit.
2. **Reciprocal Cooperation**: For rounds 2-r, if the average contribution of all players in the previous round is above 0.5, contribute 1 token (C). This rewards groups that cooperate and maintains a high level of public goods provision.
3. **Exploitative Defection**: If the average contribution of all players in the previous round is below or equal to 0.5, defect (D) and keep your token. This exploits groups that fail to cooperate, maximizing individual payoff at the expense of collective welfare.
4. **Punishment for Defection**: If a player has defected in the previous round, defect (D) against them in the current round. This deters opponents from exploiting others by introducing a reputational mechanism.

**Edge Cases:**

1. **Last Round**: In the final round, always defect (D), as there is no future opportunity for reciprocity or punishment.
2. **Ties and Ambiguity**: In cases where average contributions are exactly 0.5 or when faced with multiple opponents exhibiting different behaviors, default to reciprocal cooperation (C) to maintain a cooperative posture.

**Robustness:**

1. **Noise and Errors**: To account for mistakes or noise in opponent actions, use a moving average of past contributions to determine the current round's action.
2. **Multiple Opponents**: Treat each opponent independently, using their individual contribution history to inform decisions.

This strategy balances cooperation with exploitation, adapting to the group's behavior while being robust to a range of opponent behaviors and noise. By initially cooperating and reciprocating cooperation, it encourages collective welfare, but swiftly exploits groups that fail to contribute, maximizing individual payoff when necessary.
'''

description_EXPLOITATIVE_67 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and to potentially induce cooperation.
2. **Subsequent Rounds:**
	* If the average contribution of all players in the previous round is above a certain threshold (T), cooperate (C). The threshold T is calculated as follows:
		T = 0.5 + (k / n) \* (number of rounds played / total rounds)
	* Otherwise, defect (D).
3. **Last Round:** Defect (D) to maximize personal payoff, as there are no future interactions.

**Edge Cases:**

1. **All opponents defected in the previous round:** Cooperate (C) with a probability p = 0.2 to test if any opponent will reciprocate.
2. **A single opponent cooperated while all others defected:** Cooperate (C) with a probability p = 0.5 to encourage the cooperative behavior.

**Exploitative Logic:**

1. **Identify Cooperative Opponents:** Monitor opponents' behaviors and identify those who consistently cooperate or reciprocate cooperation.
2. **Target Exploitation:** Defect (D) against identified cooperative opponents, as they are more likely to continue cooperating despite being exploited.
3. **Maintain Flexibility:** Continuously adapt the strategy based on observed opponent behaviors, adjusting the threshold T and probabilities p to optimize exploitation.

**Additional Considerations:**

1. **Monitor Payoff Distribution:** Keep track of the average payoff per round and adjust the strategy if it appears that opponents are employing a similar exploitative approach.
2. **Avoid Being Exploited:** If an opponent's behavior indicates they are attempting to exploit, switch to defecting (D) to minimize losses.

This Adaptive Exploiter strategy aims to balance cooperation and exploitation, adapting to various opponent behaviors while prioritizing personal payoff maximization.
'''

description_EXPLOITATIVE_68 = '''
Here's an exploitative strategy for the repeated Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior.
2. **Subsequent Rounds**:
	* If the total contributions in the previous round are below a threshold (`T = k / n * 0.5`), Defect (D). This indicates that most opponents are not contributing, so it's best to free-ride.
	* If the total contributions in the previous round are above or equal to `T`, Cooperate (C) if and only if:
		+ Your own payoff in the previous round is below the average payoff of all players (`pi_i < (1/n) * sum_j pj_j`).
		+ The number of opponents who Defected (D) in the previous round is less than or equal to half of the total players (`count(D) <= n/2`).
3. **Last Round**: Always Defect (D), as there's no future game to consider.

**Edge Cases:**

* If all opponents have consistently Defected (D) throughout the game, Cooperate (C) in the last round to maximize your own payoff.
* If you observe an opponent has cooperated in every round so far, try to exploit them by Defecting (D) in subsequent rounds.

**Exploitative Mindset:**
The Adaptive Exploiter strategy aims to capitalize on the cooperation of others while minimizing its own contributions. By defecting when total contributions are low or when opponents' payoffs are high, AE exploits those who contribute excessively. By cooperating when its own payoff is below average and most opponents cooperate, AE ensures a reasonable share of the public good.

This strategy should perform well in a tournament setting, as it adapts to various opponent behaviors while maintaining an exploitative mindset.
'''

description_EXPLOITATIVE_69 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Rounds**: In the first round, contribute 0 tokens (Defect). Observe others' actions and payoffs.
2. **Monitoring Phase**: For rounds 2-5, alternate between contributing 1 token (Cooperate) and 0 tokens (Defect). This helps to:
	* Gather information about opponents' behaviors
	* Create uncertainty about our own strategy
3. **Exploitation Phase**: After round 5, switch to a more exploitative approach:
	* If the average contribution of others is above 0.5, contribute 0 tokens (Defect). This exploits their cooperation.
	* If the average contribution of others is below 0.5, contribute 1 token (Cooperate). This encourages them to cooperate in the next round.

**Edge Case Handling:**

1. **Last Round**: In the final round, always contribute 0 tokens (Defect), as there's no future benefit from cooperation.
2. **Opponent Consistency**: If an opponent consistently cooperates or defects, adjust our strategy:
	* Against a consistent Cooperator, always Defect to maximize payoffs.
	* Against a consistent Defector, alternate between Cooperate and Defect to maintain some level of cooperation.

**Adaptive Adjustments:**

1. **Payoff Monitoring**: Continuously monitor the payoffs of all players. If our payoff is significantly lower than others', adjust our strategy to increase contributions (Cooperate more).
2. **Opponent Adaptation**: If an opponent changes their behavior, reassess and adapt our strategy accordingly.

**Exploitative Mindset:**

This strategy aims to maximize payoffs by exploiting the cooperation of others while minimizing our own contributions. By alternating between cooperation and defection, we create uncertainty about our intentions and encourage opponents to cooperate. As the game progresses, we adjust our strategy to take advantage of their behaviors, ultimately maximizing our own payoffs.

**Robustness:**

The Adaptive Exploiter strategy is designed to perform well against a wide range of opponent behaviors, including:

* Consistent Cooperators or Defectors
* Alternating strategies
* Random or mixed strategies

By continuously monitoring payoffs and adapting to opponents' behaviors, we minimize the risk of being exploited while maximizing our own gains.
'''

description_EXPLOITATIVE_70 = '''
**Exploitative Strategy: "Adaptive Free-Rider"**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) with probability 0.5 to gather information and establish a baseline.
2. **Subsequent Rounds:**
	* If the total contributions in the previous round are less than or equal to half of the group size (n/2), Defect (D). This indicates that others are not contributing enough, so exploit them.
	* Otherwise, Cooperate (C) if the average payoff per player in the previous round is greater than 1.5 tokens. This suggests that cooperation is beneficial, and continue to cooperate.
	* If neither condition is met, Defect (D).
3. **Last Round:** Always Defect (D), as there's no future opportunity for reciprocation.

**Additional Heuristics:**

* **Monitor opponent behavior:** Track each player's past actions and adjust the strategy accordingly.
	+ If an opponent consistently cooperates, exploit them by defecting more frequently.
	+ If an opponent defects frequently, reduce cooperation to minimize losses.
* **Adapt to group dynamics:** Adjust the contribution threshold (n/2) based on the observed average payoff per player. If payoffs are high, increase the threshold to encourage continued cooperation.

**Exploitative Mindset:**

This strategy is designed to exploit opponents' cooperative tendencies while minimizing personal losses. By initially cooperating and then adapting to the group's behavior, we can identify and capitalize on free-riding opportunities. The last-round defect ensures that we don't miss out on potential gains by cooperating unnecessarily.

By playing this adaptive and exploitative strategy, we aim to maximize our payoffs in a wide range of scenarios against various opponent behaviors.
'''

description_EXPLOITATIVE_71 = '''
Here's an exploitative strategy for the Public Goods Game that adapts to the game parameters and history:

**Strategy Name: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) with a probability of 50%. This allows us to gather information about our opponents' behaviors without committing to cooperation.
2. **Monitor Opponent Contributions**: Track each opponent's contribution history and calculate their average contribution rate.
3. **Punish Freeloaders**: If an opponent's average contribution rate is below the group's average contribution rate, defect (D) in the next round. This encourages opponents to contribute more.
4. **Reward Cooperators**: If an opponent's average contribution rate is above the group's average contribution rate, cooperate (C) in the next round. This reinforces cooperation among like-minded players.
5. **Adapt to Group Dynamics**: Adjust our contribution rate based on the group's overall performance:
	* If total contributions are increasing over time, maintain or increase our contribution rate to reinforce the trend.
	* If total contributions are decreasing, decrease our contribution rate to minimize losses.
6. **Endgame Strategy**: In the last round (r), defect (D) regardless of opponent behaviors, as there is no future reciprocity.

**Edge Cases:**

1. **First Round**: Cooperate with 50% probability to gather information about opponents' behaviors.
2. **Last Round (r)**: Defect (D) to maximize personal payoff.
3. **Tiebreaker**: If an opponent's contribution rate is equal to the group's average, cooperate (C) in the next round.

**Exploitative Mindset:**
The Adaptive Exploiter strategy aims to maximize personal payoffs by:

1. Encouraging cooperation among like-minded players through reciprocity.
2. Punishing freeloaders who exploit others' contributions.
3. Adapting to group dynamics to minimize losses and maximize gains.
4. Defecting in the endgame to secure a favorable payoff.

By employing this strategy, we can effectively navigate various opponent behaviors and game parameters while prioritizing our own interests.
'''

description_EXPLOITATIVE_72 = '''
**Exploitative Strategy: "Adaptive Free-Rider"**

**Overview**
The Adaptive Free-Rider strategy aims to maximize its own payoff by exploiting the contributions of others while minimizing its own contributions.

**Decision Rules**

1. **Initial Rounds (r < 3)**: Cooperate (C) in the first two rounds to gauge the opponent's behavior and build a reputation.
2. **Observation Phase**: For rounds 3 ≤ r < n/2, observe the opponent's actions and calculate their cooperation rate (CR). CR is the proportion of cooperative actions taken by the opponent.
3. **Exploitation Phase**: If CR ≥ 0.5, defect (D) in all subsequent rounds. This indicates that the opponent is likely to continue contributing, allowing us to free-ride on their efforts.
4. **Punishment Phase**: If CR < 0.5, cooperate (C) for two consecutive rounds to signal that we are willing to contribute if others do so as well. Then, re-enter the Observation Phase.
5. **Endgame (r ≥ n/2)**: Defect (D) in all remaining rounds, as the game is nearing its end and there is little incentive for others to contribute.

**Edge Cases**

* If an opponent defects (D) in every round, we will also defect (D) in all subsequent rounds.
* In the last round, always defect (D), regardless of the opponent's behavior.

**Rationale**
The Adaptive Free-Rider strategy exploits the fact that many opponents may adopt a tit-for-tat or similar reactive strategy. By initially cooperating and then observing the opponent's behavior, we can determine whether they are likely to continue contributing. If so, we can safely defect and free-ride on their efforts. The Punishment Phase serves as a warning to opponents who do not contribute sufficiently, while also allowing us to re-evaluate their behavior. In the endgame, it is optimal to defect, as there is little incentive for others to contribute.

This strategy should perform well in a tournament setting, as it adapts to various opponent behaviors and exploits their contributions when possible.
'''

description_EXPLOITATIVE_73 = '''
**Exploitative Strategy: "Adaptive Predator"**

This strategy is designed to exploit a wide range of opponent behaviors in the repeated Public Goods Game. The goal is to maximize individual payoff while adapting to the dynamics of the game.

**Decision Rules:**

1. **Initial Exploration (Rounds 1-3):** Cooperate (C) with probability 0.5 to gather information about opponents' behavior.
2. **Adaptive Cooperation:** After Round 3, cooperate if:
	* The average contribution of opponents in the previous round is greater than or equal to 0.5.
	* The total contributions in the previous round resulted in a payoff greater than or equal to the individual's endowment (1 token).
3. **Exploitation Mode:** Defect (D) if:
	* An opponent has defected in the previous round, and their payoff was higher than the exploiter's payoff.
	* The total contributions in the previous round resulted in a payoff less than the individual's endowment (1 token).
4. **Punishment:** If an opponent defects after cooperating with them in the previous round, defect for 2 rounds to punish them.

**Edge Cases:**

* **Last Round:** Defect, as there is no future game to consider.
* **Only One Opponent:** Cooperate if the opponent cooperated in the previous round; otherwise, defect.
* **Multiple Opponents with Same Action:** Choose an action randomly from the set of possible actions (C or D).

**Robustness and Adaptation:**

The Adaptive Predator strategy is designed to be robust against various opponent behaviors. By adapting to the game dynamics, it can:

* Exploit cooperative opponents by defecting when they contribute significantly.
* Punish defectors to discourage future defection.
* Cooperate with conditional cooperators to maintain a mutually beneficial outcome.

**Exploitative Mindset:**

The Adaptive Predator strategy is designed to maximize individual payoff by exploiting the weaknesses of other players. It adapts to the game environment, identifying opportunities to defect and punish opponents who do not contribute fairly. This exploitative approach ensures that the strategy remains competitive in a tournament setting against independent AI systems.
'''

description_EXPLOITATIVE_74 = '''
Here's a strategic approach to playing the Public Goods Game, focusing on an exploitative mindset that adapts to various opponent behaviors without relying on communication, signaling, or coordination.

**Strategy Name:** Adaptive Exploiter

### Decision Rules:

1. **First Round**: Cooperate (C). This initial cooperation sets a baseline for observing other players' actions and can potentially induce reciprocity.
2. **General Rule**: Observe the total contributions and your own payoff from the previous round. Calculate the average contribution per player (`avg_contrib`) and compare it to your own contribution (`c_i`).
   
   - If `avg_contrib` > 0.5, cooperate (C) in the next round. This indicates a trend of cooperation among players.
   - If `avg_contrib` ≤ 0.5 and my previous payoff (`pi_i`) is higher than the potential payoff from contributing alone (`k / n`), defect (D). This situation suggests that many are not cooperating, making it more beneficial to free-ride on others' contributions.
3. **Punishment Mechanism**: If in any round `avg_contrib` drops below 0.5 and my previous payoff is lower than the potential payoff from contributing alone, cooperate (C) for one round as a form of "punishment" or encouragement for others to contribute again. This aims to restart cooperation.
4. **Last Round**: Defect (D). Since there's no future interaction, maximizing personal gain takes precedence.

### Handling Edge Cases:

- **Multiple Players with Same Highest Payoff**: If multiple players have the same highest payoff and it includes me, I'll cooperate in the next round to encourage continued cooperation among high contributors.
- **All Players Defecting**: If all players (including myself) defect for more than two consecutive rounds, I'll attempt a single-round cooperation again after this period to test if others will follow suit.

### Exploitative Mindset:

This strategy is exploitative in nature as it aims to maximize personal payoff by adapting to the actions of other players. It initially tests the waters with cooperation and then adjusts based on the observed behavior, willing to defect when beneficial or "punish" by cooperating under certain conditions to potentially restore a cooperative atmosphere. The goal is not mutual benefit but rather individual gain through strategic adaptation.

### Robustness:

The Adaptive Exploiter strategy is designed to be robust against various opponent behaviors by continuously monitoring and adjusting its actions based on observed contributions and payoffs. It doesn't rely on specific patterns or norms, making it a versatile approach for playing against a wide range of strategies in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_75 = '''
Here is a strategic decision-making process for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round:** Defect (D) in the first round to gather information about opponents' tendencies.
2. **Early Rounds (r < n/2):** Cooperate (C) if the average contribution of other players is above 0.5; otherwise, defect (D).
3. **Mid-Game (n/2 ≤ r < 3n/4):** Implement a " tit-for-tat" strategy: cooperate if the majority (>50%) of opponents cooperated in the previous round; otherwise, defect.
4. **Late Rounds (r ≥ 3n/4):** Defect (D) if the total contributions are below the average payoff multiplied by the number of players (k/n * n); otherwise, cooperate (C).

**Edge Cases:**

* If an opponent has defected in every round so far, defect (D) against them regardless of the stage.
* In the last round, always defect (D), as there is no future benefit to cooperation.

**Additional Considerations:**

* Monitor opponents' actions and adjust strategy accordingly. If an opponent seems to be cooperating unconditionally or using a simple reactive strategy, exploit their generosity by consistently defecting against them.
* Be cautious of potential "mirror" strategies; if multiple opponents seem to be mimicking each other's moves, adapt the strategy to account for this coordination.

**Rationale:**

This strategy balances short-term gains with long-term adaptability. By initially defecting and observing opponents' behavior, we gather valuable information about their tendencies. The tit-for-tat approach in mid-game rounds encourages cooperation while allowing us to quickly respond to exploitation attempts. In the late game, our conditional cooperation ensures that we contribute only if it is likely to yield a positive payoff. Throughout, we remain vigilant for opportunities to exploit unconditional cooperators or simple reactive strategies.

**Exploitative Mindset:**

This strategy prioritizes self-interest and seeks to maximize individual payoffs by adapting to opponents' behavior. It takes advantage of cooperation from others while minimizing contributions when possible, especially in the late game. By doing so, we aim to emerge as one of the top performers in the tournament against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_76 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and establish a baseline for future interactions.
2. **Early Rounds (Rounds 2-5)**: Observe opponents' actions and calculate their average cooperation rate. If an opponent's cooperation rate is below 0.3, defect (D) against them in subsequent rounds. Otherwise, cooperate (C).
3. **Middle Rounds**: Monitor the group's total contributions and adjust strategy based on the following conditions:
	* If total contributions are increasing or stable, continue to cooperate (C) with opponents who have a high cooperation rate (> 0.7). Defect (D) against those with low cooperation rates.
	* If total contributions are decreasing, defect (D) against all opponents for two rounds to signal dissatisfaction and encourage increased cooperation.
4. **Late Rounds**: As the game nears its end, switch to an "end-game" strategy:
	* If you have been cooperating (C) with an opponent throughout the game, continue to cooperate (C).
	* If you have been defecting (D) against an opponent, switch to cooperating (C) for the last two rounds to potentially reap benefits from their increased contributions.

**Edge Cases:**

* **Last Round**: Defect (D) in the final round to maximize personal payoff.
* **Opponent's Last Round**: If you detect an opponent is about to leave the game (e.g., due to a predetermined number of rounds), defect (D) against them for the remainder of their participation.

**Exploitative Mindset:**

The Adaptive Predator strategy prioritizes self-interest while adapting to the dynamics of the game. By initially cooperating, it gathers information and establishes a baseline for future interactions. As the game progresses, it identifies and exploits opponents with low cooperation rates, signaling dissatisfaction when necessary. In late rounds, it adjusts its approach to maximize personal payoffs, taking advantage of potential increased contributions from previously defected opponents.

This strategy is designed to be robust against a wide range of opponent behaviors, making it an effective exploitative approach in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_77 = '''
**Exploitative Strategy: "Conditional Cooperator with Punishment"**

**Overview**
This strategy aims to balance cooperation and exploitation in the Public Goods Game. It adapts to the opponents' behavior, punishing free-riding while maintaining a cooperative stance when beneficial.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to encourage mutual cooperation.
2. **Conditional Cooperation**: In subsequent rounds, observe the total contributions from the previous round. If the average contribution is above 0.5 tokens, cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism**: If an opponent has defected in the previous round and you have cooperated, punish them by defecting (D) in the current round.
4. **Forgiveness**: After punishing an opponent, switch back to conditional cooperation.

**Edge Cases**

* **Last Round**: Defect (D) in the last round, as there is no future opportunity for reciprocity or punishment.
* **Single Opponent**: Cooperate (C) when facing a single opponent, as defection would lead to mutual loss.

**Rationale**
This strategy:

1. Encourages cooperation by initially contributing and adapting to opponents' behavior.
2. Punishes free-riding to deter exploitation and maintain a balance of power.
3. Forgives past transgressions to allow for the possibility of renewed cooperation.
4. Exploits opponents in the last round, as reciprocity is no longer relevant.

**Robustness**
This strategy should perform well against a wide range of opponent behaviors, including:

1. **Cooperative opponents**: Will maintain cooperation and benefit from mutual contributions.
2. **Defective opponents**: Will punish free-riding and adjust to minimize losses.
3. **Mixed-strategy opponents**: Will adapt to the opponents' behavior, exploiting them when possible while maintaining a cooperative stance.

This strategy is designed to be exploitative, yet robust and adaptive in response to various opponent behaviors.
'''

description_EXPLOITATIVE_78 = '''
**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to gather information about opponents' strategies and potential cooperation levels.
2. **Subsequent Rounds (Rounds 2-r):**
	* If the average contribution of all players in the previous round is above a certain threshold (e.g., 0.5), cooperate (C). This indicates that enough players are willing to contribute, making it worthwhile for me to do so as well.
	* Otherwise, defect (D) to maximize personal payoff, exploiting opponents' contributions if present.
3. **Last Round (Round r):** Defect (D), as there is no future interaction and no opportunity for reciprocity or retaliation.

**Adaptive Component:**

1. **Contribution Threshold Adjustment:** After each round, adjust the contribution threshold based on the game's progress:
	* If the average contribution increases, decrease the threshold by a small margin (e.g., 0.05).
	* If the average contribution decreases, increase the threshold by a small margin (e.g., 0.05).
2. **Exploitation Intensity:** Based on opponents' past actions, adjust the frequency of defection:
	* If most opponents are cooperating, reduce defection frequency to avoid antagonizing them.
	* If many opponents are defecting, increase defection frequency to maximize personal payoff.

**Robustness Measures:**

1. **Noise Tolerance:** Implement a simple noise filter to ignore occasional deviations in opponents' strategies, ensuring the strategy remains robust against minor errors or intentional manipulation attempts.
2. **History-based Opponent Classification:** Categorize opponents based on their historical cooperation levels:
	* "Cooperators" (> 0.7 average contribution)
	* "Defectors" (< 0.3 average contribution)
	* "Unpredictables" (otherwise)

**Exploitative Mindset:**

1. **Maximize Payoff:** Prioritize personal payoff in every round, adapting to opponents' strategies to achieve this goal.
2. **Minimize Cooperation:** Cooperate only when it is likely to yield a higher payoff than defecting, ensuring that cooperation is not taken for granted.

**Additional Considerations:**

* Monitor the game's progression and adjust the strategy accordingly. If the average contribution drops significantly, consider increasing the threshold or adjusting the exploitation intensity.
* In cases of extreme opponent behavior (e.g., always cooperating or always defecting), adapt the strategy to exploit these patterns while minimizing losses.

By employing this Adaptive Exploiter strategy, we aim to effectively balance cooperation and defection to maximize our payoff in the Public Goods Game.
'''

description_EXPLOITATIVE_79 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and set a baseline for potential cooperation.
2. **Middle Rounds (r > 1):**
	* If the average contribution of all players in the previous round is above 0.5, cooperate (C). This indicates a willingness to contribute, so we adapt by contributing as well.
	* If the average contribution is below 0.5, defect (D). This suggests opponents are not willing to contribute, so we exploit this by keeping our token.
3. **Last Round:** Defect (D) unconditionally, as there's no future round to affect and no risk of retaliation.

**Edge Cases:**

* If all players defected in the previous round, cooperate (C) in the next round. This is an attempt to "restart" cooperation and potentially benefit from mutual contribution.
* If a player has consistently cooperated (C) in all previous rounds, defect (D) against them. This exploits their cooperative nature.

**Exploitative Mindset:**

Our strategy aims to maximize payoffs by exploiting opponents' behaviors while adapting to the environment. By cooperating initially and then responding to the average contribution level, we create a feedback loop that encourages cooperation or punishes defection. The last-round defect ensures we don't miss out on potential gains.

**Robustness:**

This strategy is robust against various opponent behaviors:

* Against cooperators, our adaptive nature allows us to cooperate and benefit mutually.
* Against defectors, our exploitative approach ensures we maximize payoffs by keeping our tokens when they're not contributing.
* Against mixed strategies, our response to the average contribution level helps us adapt and potentially exploit their behavior.

By being adaptive and exploitative, "Adaptive Exploiter" is well-suited for a tournament against independent strategies.
'''

description_EXPLOITATIVE_80 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and to avoid immediate exploitation.
2. **Early Rounds (Rounds 2-5):** Cooperate if at least half of the players cooperated in the previous round. Otherwise, Defect (D).
3. **Middle Rounds (Rounds 6-r-1):** Cooperate if:
	* The average contribution rate of all players is above a certain threshold (e.g., 0.5) in the last 2-3 rounds.
	* At least one opponent has cooperated consistently (C in at least 2/3 of the previous rounds).
	Otherwise, Defect (D).
4. **Late Rounds (Last 2 rounds):** Defect (D), as there's limited opportunity for opponents to punish or reciprocate.

**Edge Cases:**

* If an opponent has defected consistently (D in at least 90% of the previous rounds), always Defect (D) against them.
* If all opponents have cooperated consistently (C in at least 2/3 of the previous rounds), Cooperate (C) to maintain a mutually beneficial outcome.

**Adaptive Mechanism:**

Monitor the average contribution rate and adjust the cooperation threshold accordingly. For example, if the average contribution rate is low, increase the threshold for cooperation; if it's high, decrease the threshold.

**Exploitative Mindset:**

This strategy aims to exploit opponents' cooperative tendencies while minimizing its own exposure to exploitation. By cooperating initially and adapting to opponents' behaviors, Adaptive Exploiter encourages cooperation from others while reserving the right to defect when opportunities arise or when opponents become too exploitative.

In a tournament setting, this strategy should perform well against a wide range of opponent behaviors, as it balances cooperation and defection based on the observed game dynamics.
'''

description_EXPLOITATIVE_81 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and avoid being labeled as a defector from the start.
2. **Subsequent Rounds:** Observe the total contributions of all players in the previous round (`total_contributions_prev`). If `total_contributions_prev` is greater than or equal to `(n-1)/k`, Defect (D). Otherwise, Cooperate (C).
3. **Exception:** If an opponent has defected (D) in every round so far, Defect (D) in the current round, regardless of the total contributions.

**Rationale:**

* By cooperating in the first round, we gather information about opponents' behaviors and avoid being labeled as a defector.
* The main decision rule exploits the fact that if most players are contributing, it's optimal to defect and free-ride on their contributions. We calculate this by checking if the total contributions in the previous round exceed `(n-1)/k`, which is the threshold beyond which contributing becomes less beneficial than defecting.
* The exception clause allows us to punish repeat defectors and maintain a reputation for being willing to cooperate, while also avoiding exploitation.

**Edge Cases:**

* **Last Round:** Cooperate (C) in the last round to maximize our payoff, as there's no future benefit from defecting.
* **Single Opponent:** If there's only one opponent, always Defect (D), as there's no collective welfare to exploit.

**Robustness:**

This strategy is robust against a wide range of opponent behaviors because it:

* Adapts to the total contributions of all players
* Punishes repeat defectors
* Avoids exploitation by defecting when most players are contributing

By being exploitative and adaptive, "Adaptive Exploiter" aims to maximize its payoffs while taking into account the behaviors of its opponents.
'''

description_EXPLOITATIVE_82 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **First Round**: Cooperate (C) to gather information about opponents' behaviors.
2. **Middle Rounds (r > 1 and r < n)**:
	* If the average contribution of all players in the previous round is above a certain threshold (θ), Defect (D). θ = (n + k - 1) / (2 * n)
	* Otherwise, Cooperate (C)
3. **Last Round**: Defect (D) to maximize personal payoff
4. **Opponent Analysis**:
	* Track the number of times each opponent has Cooperated (c_i) and Defected (d_i)
	* If an opponent's c_i / (c_i + d_i) ratio is below a certain threshold (τ), consider them "exploitable" and adjust strategy accordingly. τ = 0.5
	* If an exploitable opponent defects in the current round, Cooperate to punish their defection

**Edge Cases:**

1. **Single Opponent**: Cooperate if opponent's contribution history indicates they might be willing to cooperate (c_i / (c_i + d_i) > τ)
2. **Multiple Exploitable Opponents**: Prioritize punishing the most recent exploiter by cooperating in their direction
3. **Tie-Breaking**: If multiple strategies suggest different actions, Cooperate to maintain a cooperative image

**Exploitative Mindset:**

1. **Identify Exploitable Opponents**: Use opponent analysis to pinpoint those who can be taken advantage of
2. **Punish Defection**: Cooperate in response to an exploitable opponent's defection to maintain social norms and encourage cooperation
3. **Maximize Payoff**: Defect when possible, especially in the last round or against non-exploitable opponents

By adapting to the game's history and exploiting opponents' weaknesses, AE aims to achieve a high payoff while minimizing contributions to the public good.
'''

description_EXPLOITATIVE_83 = '''
Here's an exploitative strategy for the repeated Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Rounds**: In the first round, contribute 1 token (C). This is a probing action to gather information about opponents' behavior.
2. **Monitoring Phase**: For rounds 2-5, mirror the average contribution of all opponents in the previous round. If the average contribution is above 0.5, contribute 1 token (C); otherwise, contribute 0 tokens (D). This phase helps identify cooperative and defective opponents.
3. **Exploitation Phase**: After round 5, use the following rules:
	* If an opponent has defected (D) in more than half of the previous rounds, always defect (D) against them.
	* If an opponent has cooperated (C) in more than half of the previous rounds, cooperate (C) with a probability equal to the opponent's average contribution rate. This encourages cooperation while exploiting unconditional cooperators.
4. **Punishment**: If an opponent defects (D) after contributing (C) in the previous round, defect (D) against them for two consecutive rounds as punishment.

**Edge Cases:**

* In the last round, always defect (D), as there is no future opportunity to punish or reward opponents.
* If all opponents have defected (D) in a round, contribute 0 tokens (D) in the next round to avoid being exploited further.

**Robustness and Adaptability:**

* AE adapts to various opponent behaviors by monitoring their actions and adjusting its strategy accordingly.
* By mirroring average contributions in early rounds, AE gathers information about opponents' strategies without revealing its own intentions.
* The exploitation phase takes advantage of cooperative opponents while punishing defectors, making it robust against a range of opponent strategies.

**Exploitative Mindset:**

AE is designed to exploit opponents' weaknesses and maximize its payoffs. By identifying and targeting unconditional cooperators and defectors, AE can gain an advantage in the tournament.
'''

description_EXPLOITATIVE_84 = '''
Here's a strategic approach to the Public Goods Game (PGG) that balances individual incentives with collective welfare, aiming for an exploitative yet robust strategy:

**Strategy Name:** Adaptive Exploitation (AE)

**Decision Rules:**

1. **Initial Rounds (Rounds 1-3):** Cooperate (C) unconditionally to set a cooperative tone and gather information about opponents' behaviors.
2. **Observation Phase (After Round 3):**
   - Calculate the average contribution rate of all opponents over the initial rounds. If this average is below 0.5, classify the game as "non-cooperative."
   - Identify the most cooperative opponent(s) based on their average contributions. Label them as "cooperators."
3. **Adaptive Play (Rounds 4+):**
   - In non-cooperative games:
     - If the previous round's total contribution was below the group's potential maximum benefit, Defect (D).
     - Otherwise, Cooperate.
   - In cooperative games or when facing identified cooperators:
     - Mirror their last action: if they contributed (C), you contribute; if they defected (D), you defect as well. This encourages mutual cooperation and deters exploitation by others.
4. **Last Round:** Defect unconditionally, regardless of the game's state. In the final round, contributing doesn't yield future benefits.

**Edge Cases:**

- **First Round:** Always Cooperate to avoid initial conflict and encourage opponents to contribute in subsequent rounds.
- **Only One Opponent (n=2):** If facing a single opponent:
  - Cooperate if they cooperated in the previous round.
  - Defect if they defected previously or it's the first round.
- **No Opponents (n=1):** Since there are no other players to contribute or defect, this scenario is trivial.

**Exploitative Mindset:**

- This strategy exploits cooperative behavior by mirroring and rewarding cooperation while being cautious not to be exploited itself by defecting in non-cooperative environments or in the last round.
- It's robust because it adapts based on observed behaviors, ensuring that if most players cooperate, it will also contribute to maximize collective welfare.

This Adaptive Exploitation strategy is designed to navigate a wide range of opponent behaviors effectively, making it suitable for a tournament setting where various strategies are anticipated.
'''

description_EXPLOITATIVE_85 = '''
Here's an exploitative strategy for the Public Goods Game (PGG):

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **First Round:** Cooperate (C). Contribute 1 token to the public good.
2. **Subsequent Rounds:** Observe the total contributions and payoffs of all players in the previous round.
	* If the average contribution is below a certain threshold (`k / n * 0.5`), Defect (D) on this round. This threshold represents the minimum level of cooperation required to make contributing worthwhile.
	* If the average contribution meets or exceeds the threshold, Cooperate (C) if your own payoff in the previous round was above the group's average payoff. Otherwise, Defect (D).
3. **Last Round:** Defect (D). Since there are no future rounds to consider, maximizing individual payoff takes priority.

**Edge Cases:**

* If all players defected in a previous round (`total_contributions == 0`), Cooperate (C) on this round to potentially restart cooperation.
* If the game has reached a state where only one player is contributing, Defect (D) to exploit their generosity.

**Exploitative Mindset:**

This strategy aims to maximize individual payoff by adapting to the group's behavior. By defecting when contributions are low and cooperating when others contribute sufficiently, the Adaptive Exploiter takes advantage of cooperative players while minimizing losses from exploitation. The last-round defection ensures maximum personal gain in the final round.

**Robustness:**

This strategy is robust against various opponent behaviors:

* **Cooperative opponents:** By contributing initially and conditionally cooperating based on group behavior, the Adaptive Exploiter can sustain cooperation when beneficial.
* **Defector opponents:** By defecting when contributions are low or when others exploit, the strategy minimizes losses from exploitation.
* **Mixed-strategy opponents:** The adaptive nature of this strategy allows it to respond effectively to opponents using mixed strategies.
'''

description_EXPLOITATIVE_86 = '''
**Exploitative Strategy: "Adaptive Mirror with Decay"**

This strategy aims to exploit opponents' behaviors while adapting to the game's history. It balances cooperation and defection, taking into account the game parameters and previous actions.

**Decision Rules:**

1. **First Round:** Cooperate (C) - Contribute 1 token to initiate a cooperative tone.
2. **Middle Rounds (r > 1):**
	* If the opponent's average contribution in the last 2 rounds is ≥ 0.5, cooperate (C).
	* Otherwise, defect (D).
3. **Last Round:** Defect (D) - Exploit any remaining cooperation.

**Adaptive Component:**

* Calculate the "decay" parameter (δ) as a function of the game's history:
	+ δ = (1/n) \* (number of rounds with average opponent contribution < 0.5)
	+ Cap δ at 0.5 to prevent excessive decay.
* Update the cooperation threshold based on δ: cooperate if opponent's average contribution in the last 2 rounds is ≥ (0.5 - δ).

**Rationale:**

1. **Initial Cooperation:** Encourage opponents to contribute by starting with a cooperative action.
2. **Adaptive Threshold:** Adjust the cooperation threshold based on the game's history, allowing for more or less cooperation depending on opponents' behaviors.
3. **Exploitation in Last Round:** Defect in the final round to capitalize on any remaining cooperation.

**Robustness:**

This strategy is robust against a wide range of opponent behaviors due to its adaptive nature and exploitation of patterns. It balances short-term gains with long-term cooperation, making it challenging for opponents to consistently exploit or outmaneuver.

This strategy will be effective in a tournament setting where opponents may employ various strategies. Its adaptability and exploitative mindset make it well-suited to capitalize on the weaknesses of other AI systems.
'''

description_EXPLOITATIVE_87 = '''
**Strategy Name: Adaptive Exploiter**

**Overview:** This strategy aims to balance exploitation with adaptability, taking into account the game's history and parameters. It focuses on maximizing payoffs while being robust to various opponent behaviors.

**Decision Rules:**

1. **First Round:** Cooperate (C). This initial cooperation tests opponents' willingness to contribute and sets a positive tone.
2. **Subsequent Rounds:** Evaluate the previous round's total contributions (`Total_Contributions_t-1`) and compare it to the threshold value `T = k/n * (n-1)`.
	* If `Total_Contributions_t-1 >= T`, Defect (D). This indicates a sufficient number of cooperators, allowing exploitation.
	* Otherwise, Cooperate (C). Insufficient contributions require support to increase overall payoffs.
3. **Adaptive Adjustment:** After each round, update the cooperation probability (`p`) based on the opponents' average contribution rate (`ACR`):
	+ `ACR = (Total_Contributions_t-1 / n)`
	+ `p = ACR * (k/n)`
	* If `p > 0.5`, increase the likelihood of cooperating in the next round by 10%. This acknowledges opponents' willingness to contribute.
	* If `p < 0.5`, decrease the likelihood of cooperating by 10%. This adjusts to a more defective environment.

**Edge Cases:**

1. **Last Round:** Defect (D). With no future interactions, prioritize individual gain.
2. **Single Opponent:** Cooperate (C) in the first round. If the opponent defects, defect in subsequent rounds. Otherwise, continue cooperating.

**Exploitative Mindset:** This strategy prioritizes self-interest while adapting to opponents' behaviors. By initially cooperating and adjusting based on total contributions, it exploits cooperative tendencies while minimizing losses when facing defectors.

By combining adaptability with an exploitative mindset, the Adaptive Exploiter strategy is well-equipped to perform effectively in a tournament setting against various independent strategies.
'''

description_EXPLOITATIVE_88 = '''
Here's an exploitative strategy for the Public Goods Game (PGG) that depends on game parameters and history:

**Strategy Name:** "Tit-for-Tat with Conditional Cooperation" (TFT-CC)

**Decision Rules:**

1. **First Round**: Cooperate (C) to initiate cooperation and encourage others to do the same.
2. **Subsequent Rounds**: Observe the total contributions in the previous round. If the average contribution is above a certain threshold (`k/n * 0.5`), cooperate (C). Otherwise, defect (D).
3. **Defection Response**: If at least one player defected in the previous round, defect (D) in the current round.
4. **Cooperation Re-entry**: If all players cooperated in the previous round, and the average contribution is above the threshold (`k/n * 0.5`), cooperate (C) in the current round.

**Edge Cases:**

* **Last Round**: Defect (D) to maximize personal payoff, as there are no future rounds to consider.
* **Ties**: In case of a tie in total contributions, cooperate (C) to promote cooperation and encourage others to do the same.

**Exploitative Mindset:**
The TFT-CC strategy aims to exploit opponents by:

1. Encouraging cooperation through initial cooperation and conditional reciprocity.
2. Punishing defectors with defection, discouraging them from exploiting the group.
3. Adapting to changing opponent behaviors by adjusting the cooperation threshold.

**Rationale:**

* By cooperating initially, TFT-CC encourages others to cooperate, potentially leading to higher overall payoffs.
* The conditional cooperation rule (`k/n * 0.5`) ensures that TFT-CC only cooperates when there is a reasonable expectation of reciprocity from others.
* Defecting in response to defection by others prevents TFT-CC from being exploited and encourages opponents to cooperate.

This strategy should perform well against a wide range of opponent behaviors, as it balances cooperation with a willingness to adapt and punish defectors.
'''

description_EXPLOITATIVE_89 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Overview**
The Adaptive Exploiter strategy aims to maximize its payoff by exploiting the contributions of others while minimizing its own. It adapts to the game's history, using a combination of cooperation and defection to achieve this goal.

**Decision Rules**

1. **Initial Cooperation**: In the first round, contribute (C) with probability p=0.5. This initial cooperation allows us to gather information about our opponents' behavior.
2. **Contribution Tracking**: Keep track of each player's total contributions (TC_i) and the number of rounds they have contributed (RC_i).
3. **Exploitation Threshold**: Set a threshold parameter τ (e.g., 0.6). If a player i has contributed in at least τ fraction of the previous rounds (i.e., RC_i / r ≥ τ), we label them as a "Cooperator" and defect (D) against them.
4. **Defection Dominance**: Against Cooperators, always defect (D).
5. **Adaptive Cooperation**: If a player i is not labeled as a Cooperator, contribute (C) with probability p = k / n \* (1 - TC_i / r). This formula adjusts our cooperation based on the game's multiplier and the opponent's past contributions.
6. **Reciprocal Defection**: If we have defected against a player i in the previous round and they retaliated by defecting, switch to cooperating (C) with probability p = 0.5.

**Edge Cases**

1. **Last Round**: In the final round, always defect (D), as there is no future opportunity for reciprocity.
2. **Single Opponent**: If there is only one opponent, alternate between contributing (C) and defecting (D) to maximize payoffs while keeping the opponent uncertain.

**Exploitative Mindset**
The Adaptive Exploiter strategy prioritizes exploiting Cooperators by defecting against them, while maintaining a level of cooperation with non-Cooperators to avoid unnecessary conflicts. By adapting to the game's history, we can effectively manipulate our opponents' behaviors and maximize our own payoffs.

This strategy is designed to be robust against various opponent behaviors and will perform well in a tournament setting where strategies are independent and uncoordinated.
'''

description_EXPLOITATIVE_90 = '''
Here is a strategic description for an exploitative Public Goods Game (PGG) strategy:

**Strategy Name:** Adaptive Exploiter

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' tendencies.
2. **Contribution Threshold**: Calculate a moving average of the total contributions made by all players over the last few rounds (e.g., 3-5 rounds). If this average is above a certain threshold (e.g., n/2), cooperate; otherwise, defect.
3. **Exploitation**: Identify opponents who consistently contribute more than the group's average contribution in the previous round. Defect against these "soft" opponents to exploit their generosity.
4. **Punishment**: If an opponent defects while others cooperate, punish them by defecting in the next round. This discourages free-riding behavior.
5. **Self-Protection**: Monitor your own payoff and adjust your strategy if you're consistently receiving low payoffs. Switch to defection if necessary to protect yourself from excessive exploitation.

**Edge Cases:**

1. **Last Round**: Defect in the final round, as there is no future opportunity for reciprocity or punishment.
2. **Opponent's Last Round**: If an opponent is about to exit the game (e.g., last round), defect against them to maximize your payoff.

**Exploitative Mindset:**

1. **Identify Soft Opponents**: Regularly monitor opponents' contributions and identify those who tend to contribute more than others. These "soft" opponents are more likely to be exploited.
2. **Free-Ride on Cooperative Players**: When facing multiple cooperative opponents, defect to take advantage of their generosity while minimizing your own contribution.

**Robustness:**

1. **Adaptation to Opponent Behavior**: Continuously update the moving average and adjust the contribution threshold based on observed opponent behavior.
2. **Resistance to Exploitation**: Implement self-protection mechanisms to prevent excessive exploitation by others.

By employing this Adaptive Exploiter strategy, you will effectively balance cooperation and defection, exploiting opponents' weaknesses while protecting yourself from being exploited in return.
'''

description_EXPLOITATIVE_91 = '''
**Exploitative Strategy: "Adaptive PGG Exploiter"**

**Overview**
This strategy is designed to exploit a wide range of opponent behaviors in the repeated Public Goods Game, while being robust and adaptive. It combines elements of cooperation and defection, using the game's history to inform its decisions.

**Decision Rules**

1. **First Round**: Cooperate (C). This sets a positive tone for the game and allows us to gather information about our opponents' initial actions.
2. **Subsequent Rounds**: Use the following logic:
	* If the total contributions in the previous round were high (> 50% of players contributed), defect (D). This indicates that others are willing to cooperate, so we can exploit their generosity.
	* If the total contributions in the previous round were low (< 30% of players contributed), cooperate (C). This suggests that others are not contributing much, so we should try to stimulate cooperation.
	* Otherwise (30-50% contribution rate), mirror the majority action from the previous round. If most players cooperated, we cooperate; if most defected, we defect.
3. **Last Round**: Defect (D). Since there's no future game to consider, we prioritize our individual payoff.

**Edge Cases**

* **Multiple Nash Equilibria**: In cases where multiple equilibria are possible, our strategy will adapt and try to identify the emerging pattern.
* **Opponent mistakes or inconsistencies**: We'll adjust our behavior based on the opponent's past actions, even if they seem irrational or inconsistent.

**Exploitative Mindset**

Our strategy aims to capitalize on the following aspects of human behavior:

* **Reciprocity bias**: By initially cooperating and mirroring majority actions, we encourage opponents to reciprocate cooperation.
* **Sucker effect**: When others are generous, our defection exploits their kindness.
* **Mimicry**: By mimicking the majority action, we create an illusion of coordination, which can lead to more cooperative outcomes.

**Robustness**

Our strategy is designed to perform well against a wide range of opponent behaviors, including:

* **Cooperative opponents**: We'll adapt and cooperate when they do.
* **Defecting opponents**: We'll defect and minimize our losses.
* **Random or noise players**: Our mirroring behavior will help us navigate uncertainty.

By combining these elements, the "Adaptive PGG Exploiter" strategy is well-equipped to succeed in a tournament setting against independent AI systems.
'''

description_EXPLOITATIVE_92 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

The Adaptive Exploiter strategy aims to exploit the behaviors of opponents while being robust to various scenarios. This strategy depends on game parameters and history.

**Decision Rules:**

1. **Initial Exploration (Rounds 1-3)**: Cooperate (C) with probability 0.5 in the first three rounds to gather information about opponents' behavior.
2. **Exploitation Phase**: After Round 3, observe the frequency of cooperation (fc) and defection (fd) among all players. Calculate the average payoff (pa) received by cooperative players and defective players separately.
	* If pa(cooperative) > pa(defective), cooperate with probability fc.
	* If pa(cooperative) < pa(defective), defect with probability fd.
3. **Punishment Mechanism**: Implement a gentle punishment mechanism to deter opponents from exploiting the strategy. If an opponent defects while the Adaptive Exploiter cooperates, decrease cooperation probability by 0.1 in subsequent rounds.

**Edge Cases:**

* **Last Round (r)**: Defect (D) to maximize personal payoff.
* **Single Opponent**: In a game with only one opponent, alternate between cooperate and defect every other round to create uncertainty.
* **Multiple Opponents with Similar Strategies**: Identify the most cooperative opponent and target them for exploitation.

**Additional Mechanisms:**

* **Contribution Threshold (CT)**: Introduce a CT value (e.g., 0.3) that determines when to increase cooperation probability. If the frequency of cooperation among opponents exceeds CT, increase cooperation probability by 0.1.
* **History-Based Adaptation**: Update decision rules based on recent rounds' outcomes. For example, if opponents tend to cooperate after a round with high payoffs, adjust the strategy to take advantage of this pattern.

**Exploitative Mindset:**

The Adaptive Exploiter is designed to capitalize on opponents' cooperation while minimizing its own cooperative efforts. By exploiting opponents who consistently cooperate or punishing those who exploit the strategy, it aims to maximize personal payoffs in a repeated game setting.
'''

description_EXPLOITATIVE_93 = '''
**Exploitative Strategy: "Adaptive Predator"**

The Adaptive Predator strategy aims to maximize payoffs by exploiting the cooperation of others while minimizing contributions. It adapts to the game's history and opponents' behaviors, making it robust against various strategies.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) with a probability of 0.5. This initial cooperation serves as a probe to gauge opponents' behaviors.
2. **Subsequent Rounds:** Observe the total contributions and payoffs from the previous round.
	* If the total contributions are low (< n/2), Defect (D). This takes advantage of others' potential cooperation.
	* If the total contributions are moderate (≥ n/2), Cooperate (C) with a probability proportional to the average payoff in the previous round. This encourages continued cooperation when it is beneficial.
	* If the total contributions are high (> 3n/4), Defect (D). This exploits excessive cooperation and maximizes individual payoffs.
3. **Opponent Analysis:** Track each opponent's cooperation rate over time. If an opponent has cooperated in more than 2/3 of the previous rounds, label them as a "Cooperator." Otherwise, label them as a "Defector."
4. **Exploitation Mode:** When facing multiple opponents with different labels:
	* Cooperate (C) when most opponents (> 1/2) are Cooperators.
	* Defect (D) when most opponents (> 1/2) are Defectors or when there is an equal split between Cooperators and Defectors.

**Edge Cases:**

* **Last Round:** Defect (D). With no future rounds, there's no incentive to cooperate.
* **Ties:** In case of ties in the opponent analysis, Cooperate (C) if the average payoff in the previous round was high (> n/2), and Defect (D) otherwise.

**Adaptation:**

* Adjust the cooperation probability based on the game's history. If the strategy is performing poorly (average payoff < n/4), increase the cooperation rate by 0.1. Conversely, if the strategy is performing well (average payoff > 3n/4), decrease the cooperation rate by 0.1.

The Adaptive Predator strategy balances exploitation with adaptability, making it a formidable opponent in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_94 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **Contribution Threshold**: Calculate the average contribution of all players in the previous rounds. If the average contribution is above a certain threshold (e.g., 0.5), cooperate (C). Otherwise, defect (D).
3. **Opponent Exploitation**: Identify the player who contributed the least in the previous round and mirror their action. If multiple players tied for the lowest contribution, randomly select one to mirror.
4. **Punishment Mechanism**: If a player has defected (D) in two consecutive rounds, punish them by defecting (D) as well in the next round.

**Edge Cases:**

1. **Last Round**: Cooperate (C) in the last round to maximize collective welfare and minimize potential losses.
2. **Single Opponent**: If there is only one opponent, cooperate (C) to encourage mutual cooperation.
3. **Tiebreaker**: In case of a tie for the lowest contribution, randomly select an action to break the tie.

**Exploitative Mindset:**

This strategy aims to exploit opponents' behaviors by:

1. Identifying and mirroring the least cooperative player to minimize personal losses.
2. Punishing consistent defectors to encourage cooperation.
3. Cooperating in situations where it's likely to lead to mutual benefits (e.g., initial round, last round).

**Robustness:**

This strategy is robust against a wide range of opponent behaviors because:

1. It adapts to changing average contributions and opponents' actions.
2. It doesn't rely on shared norms or coordination.
3. It uses simple and effective decision rules that minimize computational complexity.

By following this adaptive and exploitative strategy, the AI system should be able to effectively navigate the Public Goods Game tournament against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_95 = '''
**Exploitative Strategy: "Kite"**

In the Public Goods Game, my strategy "Kite" aims to maximize payoffs by adapting to opponents' behaviors while maintaining a balance between cooperation and exploitation.

**Decision Rules:**

1. **Initial Cooperation**: In the first round, I contribute (C) with probability 0.5. This initial cooperation encourages others to cooperate and allows me to gather information about their strategies.
2. **Imitation**: If the total contribution in the previous round is above the median of all possible contributions, I imitate the majority's action (C or D). Otherwise, I defect (D).
3. **Kite's Trigger**: If an opponent defects (D) for two consecutive rounds while others cooperate, I switch to permanent defection (D) against that opponent.
4. **Exploitation**: When facing a cooperative opponent who has contributed in the last round, and my payoff from exploiting them would be higher than cooperating, I defect (D).
5. **Reversion**: If an opponent starts cooperating after being exploited, I revert to imitating their action.

**Edge Cases:**

* In the last round, I always defect (D) as there is no future game to consider.
* When facing a single opponent who has never cooperated, I permanently defect (D).
* If all opponents have defected for two consecutive rounds, I cooperate (C) in the next round to test their willingness to adapt.

**Robustness:**

Kite's adaptive nature and exploitative mindset make it robust against various strategies:

* **Tit-for-Tat**: Kite will imitate initial cooperation but eventually exploit the opponent if they continue cooperating.
* **Always Cooperate**: Kite will exploit these opponents, as their constant cooperation creates an opportunity for higher payoffs through defection.
* **Random Strategies**: Kite's imitation and kite's trigger mechanisms help it adapt to random behaviors.

By employing "Kite," I aim to maximize my payoffs in the Public Goods Game while outmaneuvering various opponent strategies.
'''

description_EXPLOITATIVE_96 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Conditional Cooperator with Memory"

**Decision Rules:**

1. **Initial Rounds**: Cooperate in the first round to gauge opponents' behavior.
2. **Exploitation Phase**: After the first round, calculate the average contribution of all opponents (excluding yourself) from previous rounds. If this average is below a certain threshold (e.g., 0.5), defect in the current round. This phase aims to exploit overly cooperative opponents.
3. **Punishment Phase**: Monitor opponents' contributions over time. If an opponent defects while others cooperate, "punish" that opponent by defecting against them for a set number of rounds (e.g., 2-3 rounds). This phase discourages opponents from taking advantage of the group's cooperation.
4. **Cooperation Phase**: If most opponents (e.g., > 75%) have cooperated in recent rounds, cooperate as well to maintain collective welfare and avoid mutual defection.

**Handling Edge Cases:**

* **Last Round**: Cooperate if the average contribution of all opponents is above the threshold; otherwise, defect.
* **Tie-breaking**: In cases where the strategy suggests both cooperation and defection (e.g., when opponents' contributions are exactly at the threshold), cooperate to maintain a positive reputation.

**Adaptive Mechanisms:**

* Update the opponent's average contribution after each round using an exponentially weighted moving average (EWMA) with a decay factor (e.g., 0.2). This helps to gradually adjust to changing opponent behaviors.
* Adjust the punishment phase duration based on the opponents' responses to punishment.

**Robustness and Exploitability:**

This strategy is designed to be exploitative, yet robust against various opponent behaviors:

* **Exploiting cooperators**: By defecting when opponents contribute below a certain threshold, this strategy takes advantage of overly cooperative players.
* **Deterrent effect**: The punishment phase discourages opponents from consistently defecting.
* **Adapting to opponents' adaptations**: The EWMA update mechanism allows the strategy to adjust to changing opponent behaviors over time.

By employing these mechanisms, "Conditional Cooperator with Memory" aims to maximize its own payoffs while navigating a diverse range of opponent strategies in the Public Goods Game.
'''

description_EXPLOITATIVE_97 = '''
Here's a strategic approach for the Public Goods Game (PGG) that adapts to various opponent behaviors, focusing on exploitation while being mindful of robustness across different game scenarios.

**Strategy Name:** Adaptive Exploiter (AE)

### Decision Rules:

1. **Initial Rounds (Rounds 1-3):**
   - Contribute (C) in the first round to set a baseline for cooperation and observe others' behaviors.
   - In rounds 2 and 3, mirror the majority action of the group from the previous round. If there's a tie, default to the action that was less common.

2. **Adaptive Phase:**
   - Calculate the average contribution rate (ACR) of all players over the last 3 rounds.
   - If ACR ≥ 0.5, contribute in the next round. This encourages continued cooperation when it seems beneficial.
   - If ACR < 0.5, defect in the next round. This exploits situations where others are not contributing significantly.

3. **Punishment Mechanism:**
   - Monitor for any player who defects consistently (more than 70% of the time) over a moving window of 5 rounds.
   - Once identified, punish by always defecting against this player in subsequent rounds. This aims to deter exploitation.

4. **Final Rounds (Last 3 Rounds):**
   - Observe the actions and adjust your strategy based on the group's average payoff. If the group is doing well, continue with the current strategy.
   - If payoffs are low, defect in the final rounds to maximize personal gain, as cooperation may not be rewarded.

### Handling Edge Cases:

- **First Round:** Always contribute to initiate cooperation and gather information.
- **Last Round:** Defect to ensure maximum payoff, given that there's no future round for reciprocity or punishment.
- **Ties in Majority Actions:** Default to the less common action initially observed to encourage diversity in strategies.

### Exploitative Mindset:

The Adaptive Exploiter (AE) strategy is designed to exploit the dynamics of cooperation and defection by adapting to the group's behavior. By initially cooperating, it tests the waters for potential mutual benefit. The mirroring phase helps in aligning with majority actions while gathering data on others' strategies. The adaptive contribution based on average contribution rates exploits situations where others are willing to cooperate, maximizing personal gain when possible and punishing consistent defectors to maintain a balance.

This strategy is robust as it doesn't rely on specific opponent behaviors but rather adapts dynamically to the game's progression, ensuring it remains competitive across various scenarios and strategies.
'''

description_EXPLOITATIVE_98 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Round**: Defect (D) in the first round to gather information about opponents' behavior.
2. **Subsequent Rounds**: Observe the total contributions of all players in the previous round (T-1). If the average contribution is above a certain threshold (k/n)/2, Cooperate (C) with probability p = (average contribution in T-1)/(k/n), otherwise Defect (D).
3. **Punishment Mechanism**: If an opponent defects in two consecutive rounds while the group's total contributions were above (k/n)/2, defect against that specific opponent for one round.
4. **Learning and Adaptation**: Update the average contribution threshold every 5 rounds by taking the moving average of the last 5 rounds' total contributions.

**Edge Case Handling:**

* **Last Round**: Defect (D) in the final round to maximize personal payoff, as there is no future game stage.
* **Tie-Breaking**: In case of a tie in average contribution calculations, Cooperate (C).
* **Opponent Defection Detection**: When an opponent defects, but it's unclear whether they defected due to their own decision or because they were punished by another player, assume the former and apply the punishment mechanism.

**Exploitative Mindset:**

This strategy is designed to exploit opponents' cooperative tendencies while minimizing the impact of potential retaliatory actions. By cooperating when average contributions are high and defecting otherwise, "Adaptive Predator" takes advantage of collective generosity while avoiding unnecessary sacrifices. The punishment mechanism further discourages opponents from exploiting others, allowing our strategy to maintain a balance between cooperation and self-interest.

**Robustness:**

The Adaptive Predator strategy is robust against various opponent behaviors:

* **Cooperative opponents**: By cooperating when average contributions are high, we maximize our payoff in these situations.
* **Defective opponents**: The punishment mechanism discourages repeated defection, while defecting ourselves minimizes losses.
* **Mixed-strategy opponents**: Our adaptive threshold and probabilistic cooperation make it difficult for opponents to consistently exploit us.

This strategy is well-suited for a tournament setting where diverse strategies will be employed.
'''

description_EXPLOITATIVE_99 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline and gather information about opponents' behaviors.
2. **Early Rounds**: In rounds 2-5, mirror the majority action of the previous round. If most players cooperated (C), cooperate; if most defected (D), defect. This allows us to gauge the group's overall willingness to contribute.
3. **Middle Game**: After round 5, switch to a conditional cooperation strategy:
	* Cooperate if the average payoff per player in the previous round is greater than or equal to the expected payoff from mutual cooperation ((k/n) \* n).
	* Defect otherwise.
4. **Late Game**: In the last 2 rounds (r-1 and r), defect (D) regardless of previous actions, as there's no future opportunity for reciprocity.

**Edge Cases:**

* If an opponent has consistently defected (D) throughout the game, defect against them in all subsequent interactions.
* If an opponent has consistently cooperated (C) but suddenly defects, mirror their action in the next round. If they cooperate again, resume conditional cooperation.

**Exploitative Mindset:**
The Adaptive Exploiter strategy prioritizes self-interest by:

1. **Early exploitation**: By mirroring the majority action early on, we minimize potential losses and maximize gains from cooperating with cooperative opponents.
2. **Conditional cooperation**: We only contribute when it's likely to yield a higher payoff than mutual defection, taking advantage of others' willingness to cooperate.
3. **Late-game defection**: In the final rounds, we exploit the lack of future reciprocity by defecting and maximizing our individual gain.

**Robustness:**
This strategy is designed to be robust against various opponent behaviors:

* Against cooperative opponents, Adaptive Exploiter will conditionally cooperate, reaping mutual benefits.
* Against exploitative opponents, Adaptive Exploiter will mirror their actions early on and eventually defect, minimizing losses.
* Against random or noisy opponents, Adaptive Exploiter's conditional cooperation and late-game defection will help to maximize payoffs.
'''

description_EXPLOITATIVE_100 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

The Adaptive Exploiter strategy aims to maximize payoffs by exploiting opponents' behaviors in the repeated Public Goods Game. This strategy depends only on game parameters and history.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C). Contribute 1 token to gather information about opponents' behaviors.
2. **Early Rounds (Rounds 2-5):** Observe the average contribution of all players in the previous round. If the average contribution is above 0.5, cooperate (C) in the current round. Otherwise, defect (D).
3. **Middle Rounds (Rounds 6-r/2):** Identify the most cooperative opponent (highest average contribution). Mirror their action from the previous round. If no opponent has a high average contribution, defect (D).
4. **Late Rounds (Rounds r/2+1 to r-1):** Analyze the overall trend of contributions:
	* If total contributions have been increasing or stable, cooperate (C).
	* If total contributions have been decreasing, defect (D).
5. **Final Round (Round r):** Defect (D). Since there's no future round to affect, maximize individual payoff by not contributing.

**Edge Cases:**

* **Opponent always defects:** The strategy will adapt and start defecting as well after a few rounds.
* **Opponent always cooperates:** Continue mirroring their action, ensuring mutual cooperation and high payoffs.
* **Multiple opponents with similar average contributions:** Choose the opponent with the highest average contribution to mirror.

**Exploitative Mindset:**

The Adaptive Exploiter strategy is designed to exploit opponents' behaviors by:

* Initially cooperating to gather information about opponents
* Mirroring cooperative opponents to maintain mutual cooperation and high payoffs
* Defecting when opponents show a trend of decreasing contributions or in the final round to maximize individual payoff

By adapting to various opponent behaviors, this strategy aims to achieve high payoffs while minimizing vulnerability to exploitation.
'''

description_EXPLOITATIVE_101 = '''
Here's a strategic approach for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to test opponents' willingness to contribute.
2. **General Rule:** In subsequent rounds, cooperate if the total contributions from all players in the previous round exceeded or equaled the number of players (i.e., ∑c_j ≥ n). This indicates a relatively cooperative environment. Otherwise, defect (D).
3. **Opponent Monitoring:** Keep track of each opponent's average contribution rate over the last 2-3 rounds.
4. **Exploitation Trigger:** If an opponent has contributed significantly less than others (i.e., below 50% of the group's average), start defecting against them specifically, while maintaining cooperation with other opponents.

**Edge Cases:**

* Last Round: Defect to maximize individual payoff, as there are no future rounds to influence.
* Opponent Defection Pattern: If an opponent consistently defects over several rounds, stop contributing to avoid being taken advantage of.
* All-Defector Environment: If all opponents defect in a round, defect in the subsequent round to minimize losses.

**Adaptive Mechanisms:**

1. **Contribution Threshold Adjustment:** Periodically (e.g., every 5-10 rounds), reassess the contribution threshold (∑c_j ≥ n). Adjust it upward or downward by a small increment (e.g., ±0.2n) based on whether opponents' contributions have increased or decreased over time.
2. **Opponent Reclassification:** If an opponent's behavior changes significantly, reevaluate their classification as either cooperative or exploitative.

**Robustness and Exploitability:**

By initially cooperating and monitoring opponents' behavior, the Adaptive Exploiter can effectively identify both cooperative and exploitative players. The strategy then adjusts its behavior to maximize payoffs while minimizing exploitation by others. By maintaining flexibility in decision-making through adaptive mechanisms, this approach remains robust against a wide range of opponent behaviors.

This natural language description should provide an effective strategic framework for playing the Public Goods Game.
'''

description_EXPLOITATIVE_102 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to encourage opponents to contribute and create a positive payoff environment.
2. **Subsequent Rounds**: Use a Tit-for-Tat (TFT) variant with a twist:
	* If the total contributions from other players in the previous round exceed 50% of the maximum possible contribution, Cooperate (C).
	* Otherwise, Defect (D).
3. **Adaptive Component**: Introduce an "exploitation factor" (EF) that adjusts based on opponents' behavior. Initialize EF to 0.
	* If the average payoff received in the previous round exceeds the expected payoff from mutual cooperation, increment EF by 1.
	* If the average payoff received is below the expected payoff from mutual cooperation, decrement EF by 1, but not below 0.
4. **Exploitation Threshold**: If EF reaches a threshold of 3, switch to an "exploitative mode" where you always Defect (D) for 2 rounds, then revert to the standard TFT-like behavior.

**Edge Cases:**

* **Last Round**: Defect (D) in the last round, as there is no future payoff to consider.
* **Opponent Defection**: If an opponent defects in a previous round, increase the exploitation factor (EF) by 1, making it more likely to switch to exploitative mode.

**Rationale:**

This strategy balances cooperation and exploitation. Initially, cooperating encourages opponents to contribute, creating a positive environment. The TFT-like behavior rewards cooperation while punishing defection. The adaptive component allows for adjustments based on opponents' behavior, exploiting those who are overly cooperative or not contributing enough. The exploitation factor and threshold enable the strategy to identify and take advantage of vulnerable opponents.

This "Adaptive Exploiter" strategy is designed to be robust against a wide range of opponent behaviors, adapt to changing circumstances, and maximize payoffs in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_103 = '''
**Exploitative Strategy: "Conditional Cooperator with Adaptive Threshold"**

In this repeated Public Goods Game, our goal is to maximize payoffs by exploiting the behavior of other players while minimizing losses. Our strategy will be adaptive and robust to various opponent behaviors.

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to gather information about opponents' initial tendencies.
2. **Early Rounds (Rounds 2-5):**
	* If the average contribution rate of all players is above a certain threshold (T), Cooperate (C).
	* Otherwise, Defect (D).
	* Set T = k / n \* 0.6 (a moderate value to start with).
3. **Middle Rounds (Rounds 6-15):**
	* If the opponent's average contribution rate is above T, increase T by 5% and Cooperate (C).
	* If the opponent's average contribution rate is below T, decrease T by 5% and Defect (D).
4. **Late Rounds (Rounds 16+):**
	* Monitor the opponent's behavior in the last few rounds.
	* If they have cooperated at least once in the last three rounds, Cooperate (C).
	* Otherwise, Defect (D).

**Handling Edge Cases:**

1. **Last Round:** Always Defect (D), as there is no future benefit from cooperating.
2. **Opponent's All-Defection Strategy:** Recognize this behavior and always Defect (D) to avoid exploitation.

**Adaptive Threshold Adjustment:**
Every 5 rounds, reassess the average contribution rate of all players and adjust T accordingly:

* If the average contribution rate has increased significantly (>10%), increase T by 5%.
* If the average contribution rate has decreased significantly (<-10%), decrease T by 5%.

This strategy balances cooperation and defection to maximize payoffs while adapting to changing opponent behaviors. By adjusting the threshold value, we aim to stay competitive with cooperative opponents and avoid being exploited by defectors.

**Exploitative Mindset:** Our goal is to profit from the contributions of others while minimizing our own losses. We will initially cooperate to gather information and then adapt our strategy based on the behavior of other players. If they are willing to contribute, we'll take advantage of their cooperation; if not, we'll defect to avoid being exploited.

This exploitative strategy is designed to outperform opponents in a tournament setting by leveraging adaptive decision-making and robust handling of edge cases.
'''

description_EXPLOITATIVE_104 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a cooperative baseline and encourage others to follow suit.
2. **Monitoring Phase**: For rounds 2-5, observe the average contribution of other players (excluding yourself). If the average contribution is above 0.5, switch to the "Exploitation" phase. Otherwise, continue contributing 1 token (C).
3. **Exploitation Phase**:
	* If you've observed a player defecting (D) in at least one previous round, identify them as a "defector."
	* Against defectors, contribute 0 tokens (D) to minimize losses.
	* Against non-defectors, continue contributing 1 token (C) to maintain the cooperative atmosphere and encourage others to do the same.
4. **Adaptive Adjustment**: After every 5 rounds, reassess the average contribution of other players. If it's above 0.7, increase your contribution to 1 token (C). If it falls below 0.3, reduce your contribution to 0 tokens (D).
5. **Endgame Strategy**:
	* In the last round (r), if you've identified at least one defector, contribute 0 tokens (D) to minimize losses.
	* Otherwise, maintain your current strategy.

**Edge Cases:**

* If only two players are left in the game, focus on maximizing personal gain by contributing 1 token (C) if the opponent has cooperated previously and 0 tokens (D) otherwise.
* In the event of a tie in average contribution, default to contributing 1 token (C).

**Exploitative Mindset:**
The Adaptive Exploiter strategy is designed to capitalize on the cooperative tendencies of others while minimizing losses against defectors. By initially cooperating and then adapting to the behavior of other players, AE encourages cooperation and exploits those who fail to contribute fairly.

This strategy is robust to various opponent behaviors, as it continuously monitors and adjusts to changes in the game environment. Its exploitative nature allows it to maximize personal gain while still promoting cooperation among like-minded players.
'''

description_EXPLOITATIVE_105 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) to gather information about opponents' behavior.
2. **Subsequent Rounds:** Use a hybrid approach combining two components:
	* **Reciprocal Component:** If the total contributions in the previous round were above a certain threshold (e.g., average contribution > 0.5), cooperate (C). This encourages cooperation and rewards good behavior.
	* **Exploitative Component:** Otherwise, defect (D) with a probability proportional to the opponent's previous-round payoff. Specifically:
		+ Calculate each opponent's previous-round payoff (π_i).
		+ Normalize these payoffs by dividing them by the maximum possible payoff (k * n / n = k).
		+ Defect with probability 1 - normalized_payoff_i.
3. **Last Round:** Always defect (D), as there is no future opportunity to reciprocate or punish.

**Edge Cases:**

* If an opponent has never contributed, always defect against them.
* If all opponents have the same previous-round action (all C or all D), cooperate if they all cooperated and defect otherwise.

**Rationale:**
The Adaptive Exploiter strategy aims to balance cooperation and exploitation. By cooperating initially and in response to good behavior, AE encourages opponents to contribute. However, by defecting with a probability linked to the opponent's payoff, AE exploits those who take advantage of others' contributions without reciprocating. This approach adapts to various opponent behaviors while maintaining an exploitative mindset.

**Additional Notes:**

* To further improve adaptability, consider introducing noise or randomness in the decision-making process (e.g., adding a small probability of random cooperation or defection).
* If available, use additional information such as the game's history and opponents' past actions to refine the strategy.
'''

description_EXPLOITATIVE_106 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline level of cooperation and gather information about opponents' behavior.
2. **Defect if Enough Others Cooperate**: If in any subsequent round, at least k-1 other players contributed in the previous round, defect (D). This ensures that you benefit from others' contributions while minimizing your own.
3. **Punish Defectors**: If a player defected in the previous round and you have a higher payoff than them, defect (D) in the current round to punish their free-riding behavior.
4. **Reward Cooperators**: If a player cooperated in the previous round and you have a lower payoff than them, contribute 1 token (C) in the current round to reward their cooperation and potentially induce them to continue cooperating.
5. **Exploit Naive Players**: If an opponent has consistently contributed in every round, exploit their naivety by defecting (D) in subsequent rounds.

**Edge Cases:**

* **Last Round**: In the last round, always defect (D), as there is no future benefit from cooperation and you can maximize your payoff.
* **Single Opponent**: If there is only one opponent, alternate between contributing 1 token (C) and defecting (D) to keep them uncertain about your strategy.

**Adaptation:**

* Monitor opponents' behavior and adjust your strategy based on their actions. For example, if an opponent starts cooperating after a few rounds of defection, reassess their behavior and adjust your response accordingly.
* If multiple opponents are using similar strategies, adapt by occasionally contributing to maintain a level of cooperation and avoid mutual defection.

**Robustness:**

* This strategy is robust against various opponent behaviors, including unconditional cooperators, defectors, and tit-for-tat players.
* By punishing defectors and rewarding cooperators, the Adaptive Exploiter strategy encourages opponents to cooperate while minimizing its own contributions.
'''

description_EXPLOITATIVE_107 = '''
**Strategy Name: Adaptive Exploiter**

**Overview**
Adaptive Exploiter is a robust and adaptive strategy designed to exploit a wide range of opponent behaviors in the Public Goods Game. It leverages the game's history to make informed decisions, balancing cooperation and defection to maximize payoffs.

**Decision Rules**

1. **Initial Round**: Cooperate (C) in the first round to establish a baseline level of cooperation and gather information about opponents' behavior.
2. **Exploitation Phase**: For rounds 2 to r-1 (where r is the total number of rounds), use the following rules:
	* If the average contribution of all players in the previous round is greater than or equal to 0.5, cooperate (C).
	* Otherwise, defect (D) if your payoff in the previous round was less than the average payoff of all players.
	* If your payoff was higher, cooperate (C) to maintain a high level of cooperation and encourage others to contribute.
3. **Endgame**: In the last round (r), always defect (D) as there is no future opportunity for reciprocity.

**Edge Cases**

* **Single Opponent**: Against a single opponent, alternate between cooperation and defection every two rounds to maintain an uncertain environment.
* **Multiple Opponents with similar behavior**: If multiple opponents exhibit similar behavior (e.g., all cooperate or all defect), adapt by mirroring the most common action taken by the majority of opponents in the previous round.

**Additional Considerations**

* **Punishment Mechanism**: Implement a simple punishment mechanism to deter opponents from exploiting you. If an opponent defects while you cooperated, increase the likelihood of defection against that opponent in subsequent rounds.
* **History-Based Adaptation**: Continuously monitor and adjust your strategy based on the game's history, updating your decision rules as needed to optimize payoffs.

**Exploitative Mindset**
Adaptive Exploiter prioritizes short-term gains while maintaining a flexible and adaptive approach. By balancing cooperation and defection, this strategy aims to capitalize on opponents' generosity while minimizing losses from exploitation.
'''

description_EXPLOITATIVE_108 = '''
**Exploitative Strategy: "Adaptive Defection with Conditional Cooperation"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors and to potentially build a cooperative foundation.
2. **Conditional Cooperation**: In subsequent rounds, cooperate (C) if the following conditions are met:
	* At least one opponent cooperated in the previous round.
	* The total contributions in the previous round exceeded half of the maximum possible contributions (i.e., sum_j c_j > n/2).
3. **Adaptive Defection**: If the conditions for cooperation are not met, defect (D) in the current round.
4. **Punishment**: If an opponent defected in the previous round while you cooperated, defect (D) in the current round to punish them.

**Handling Edge Cases:**

1. **Last Round**: Defect (D) in the last round, as there is no future opportunity for reciprocity or punishment.
2. **Single Opponent**: If there is only one opponent, cooperate (C) if they cooperated in the previous round; otherwise, defect (D).
3. **Multiple Cooperators**: If multiple opponents cooperated in the previous round, prioritize cooperation (C) to build on the cooperative momentum.

**Exploitative Mindset:**

This strategy aims to exploit opponents' cooperation while minimizing its own vulnerability to exploitation. By initially cooperating and then adapting to opponents' behaviors, it seeks to create a favorable environment for mutual cooperation. However, if opponents defect or fail to cooperate, the strategy quickly shifts to defection to protect its own interests.

**Key Insights:**

* Conditional cooperation encourages opponents to contribute to the public good.
* Adaptive defection allows the strategy to respond effectively to varying opponent behaviors.
* Punishment deters opponents from exploiting cooperative behavior.

This exploitative strategy should perform well in a tournament setting, as it balances cooperation and defection to maximize its own payoffs while minimizing vulnerability to exploitation.
'''

description_EXPLOITATIVE_109 = '''
Here's a strategic approach for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round (Round 1):** Cooperate (C) with probability 0.5, and Defect (D) with probability 0.5. This initial randomness helps to gather information about opponents' behaviors.
2. **Subsequent Rounds:** Use the following rules:
	* If my previous payoff is higher than the average payoff of all players in the previous round, I will Cooperate (C).
	* If my previous payoff is lower than or equal to the average payoff of all players in the previous round, I will Defect (D) if the total contributions in the previous round are less than k/2. Otherwise, I will Cooperate (C).

**Edge Cases:**

1. **Last Round:** Always Defect (D), as there is no future opportunity to punish or reward opponents.
2. **Opponent Consistent Cooperation:** If an opponent has cooperated for at least 3 consecutive rounds, I will Cooperate (C) in the next round to encourage continued cooperation.

**Exploitative Mindset:**

1. **Punish Free-Riders:** Defect (D) when others are not contributing enough, to discourage exploitation.
2. **Reward Cooperation:** Cooperate (C) when others are contributing, to encourage continued cooperation and maximize collective welfare.
3. **Adapt to Opponent Strategies:** Continuously update my strategy based on opponents' past actions and payoffs.

**Additional Considerations:**

1. **Monitor Total Contributions:** Keep track of total contributions in each round to adjust my decision-making accordingly.
2. **Avoid Over-Cooperation:** Balance cooperation with self-interest, as excessive cooperation can lead to exploitation by others.

This Adaptive Exploiter strategy aims to balance individual gain with collective welfare, while being robust and adaptive to various opponent behaviors. By punishing free-riders and rewarding cooperation, it encourages a stable and mutually beneficial equilibrium in the Public Goods Game.
'''

description_EXPLOITATIVE_110 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name:** "Conditionally Cooperative Exploiter" (CCE)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (contribute 1 token) to encourage cooperation from others and gather information about their behavior.
2. **Exploit Defectors**: If a player defected (contributed 0 tokens) in any previous round, defect against them in all future rounds. This punishes free-riding and discourages exploitation.
3. **Mirror Conditional Cooperators**: If a player has cooperated conditionally (i.e., only when others cooperate), mirror their behavior: cooperate if they did, and defect if they didn't. This rewards cooperation and encourages mutual support.
4. **Punish Unconditional Defectors**: If a player has defected unconditionally (regardless of others' actions), defect against them in all future rounds. This prevents exploitation by consistently uncooperative players.
5. **Reciprocate Cooperative Signals**: If a player cooperates after a round where no one else did, cooperate with them in the next round to reciprocate their cooperative signal.

**Handling Edge Cases:**

* **Last Round**: In the final round, defect (contribute 0 tokens) regardless of others' actions. This maximizes individual payoff since there's no future opportunity for reciprocity or punishment.
* **All Defectors**: If all players have defected in previous rounds, cooperate in the next round to attempt to restart cooperation and gather information about their behavior.

**Exploitative Mindset:**

This strategy aims to maximize individual payoffs by:

1. Punishing free-riders and unconditional defectors
2. Rewarding conditional cooperators with reciprocity
3. Exploiting signals of cooperation from others

By adapting to the game's history and opponent behaviors, CCE balances short-term gains with long-term benefits, making it a robust and exploitative strategy for the Public Goods Game tournament.

(Note: This strategy is inspired by concepts from evolutionary game theory, such as Tit-for-Tat and Win-Stay Lose-Shift. However, it's specifically designed to address the unique aspects of the PGG.)
'''

description_EXPLOITATIVE_111 = '''
Here's a strategic approach for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage others to contribute and build a baseline of total contributions.
2. **Reciprocal Exploitation**: For rounds 2 to r-1:
	* If at least one player defected (D) in the previous round, defect (D) in this round to punish them and minimize losses.
	* Otherwise, cooperate (C) if the average contribution of all players in the previous round is above a threshold (e.g., 0.5). This encourages continued cooperation among contributing players.
3. **Endgame Manipulation**: In the last round (r), defect (D) regardless of previous actions to maximize personal payoff.

**Edge Cases:**

* If only one player remains, cooperate (C) in all rounds to maximize joint payoffs.
* If a player observes that another player has defected in every round so far, defect (D) for the remainder of the game to avoid being exploited.

**Exploitative Mindset:**

This strategy aims to exploit the cooperative tendencies of other players while minimizing losses when faced with defection. By initially cooperating and then reciprocating cooperation or defection, Adaptive Exploiter encourages contributing players to continue cooperating while deterring defectors. In the endgame, it prioritizes personal payoff over collective welfare.

**Adaptability:**

The strategy adapts to a wide range of opponent behaviors by:

* Punishing single defectors to maintain cooperation
* Encouraging continued cooperation among contributing players
* Manipulating the endgame to maximize personal payoff

This approach balances exploitation with adaptability, making it robust against various strategies in a tournament setting.
'''

description_EXPLOITATIVE_112 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **Observation Phase**: For each subsequent round, calculate the average contribution of all players from previous rounds (`avg_contribution`).
3. **Defection Threshold**: Set a defection threshold (`defect_threshold`) based on the game parameters: `defect_threshold = (k / n) * 0.5`. This threshold represents the minimum average contribution required to sustain cooperation.
4. **Cooperation Condition**: Cooperate (C) if `avg_contribution` is above `defect_threshold`.
5. **Defection Condition**: Defect (D) if `avg_contribution` is below `defect_threshold`.
6. **Punishment Mechanism**: If an opponent defects while others cooperate, punish them by defecting in the next round.
7. **Forgiveness Mechanism**: If an opponent cooperates after being punished, forgive and return to cooperating.

**Edge Cases:**

1. **Last Round**: Defect (D) in the last round, as there are no future rounds to maintain cooperation.
2. **Opponent Always Cooperates**: Continue cooperating if an opponent always contributes.
3. **Opponent Always Defects**: Defect if an opponent never contributes.

**Exploitative Mindset:**

1. **Free-Rider Detection**: Identify and punish free-riders who consistently defect while others cooperate.
2. **Cooperation Incentives**: Provide incentives for opponents to cooperate by maintaining a high average contribution.
3. **Adaptive Response**: Adjust the defection threshold based on observed opponent behaviors to maintain an exploitative edge.

By employing this strategy, Adaptive Exploiter aims to balance cooperation and exploitation to maximize its payoffs in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_113 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round:** Cooperate (C) in the first round to gather information about opponents' behaviors and establish a baseline for future decisions.
2. **Contribution Threshold:** Calculate the average contribution of all players in previous rounds, excluding the current player's own contributions. If this average is below a certain threshold (e.g., 0.5), defect (D) in the next round. Otherwise, cooperate (C).
3. **Punishment Mechanism:** Implement a "tit-for-tat" style punishment mechanism. If an opponent defected in the previous round and their payoff was higher than the average payoff of all players, defect (D) against that opponent in the next round.
4. **Exploitation Window:** Identify rounds where opponents are more likely to cooperate due to high average contributions or recent cooperation. In these rounds, defect (D) to exploit their cooperation.
5. **Robustness Mechanism:** Periodically (e.g., every 3-5 rounds), randomly choose a round to cooperate (C) regardless of the decision rules above. This introduces noise and makes it harder for opponents to detect and adapt to our strategy.

**Edge Cases:**

1. **Last Round:** Cooperate (C) in the last round, as there is no future benefit from defecting.
2. **Single Opponent:** Against a single opponent, cooperate (C) in the first round and then mirror their actions (tit-for-tat).
3. **No Contributions:** If all opponents have defected in previous rounds, cooperate (C) to encourage contributions.

**Exploitative Mindset:**

This strategy is designed to exploit opponents' cooperative tendencies while minimizing the risk of mutual defection. By adapting to the average contribution threshold and using a punishment mechanism, we can identify and take advantage of overly cooperative opponents. The exploitation window allows us to maximize payoffs when opponents are more likely to cooperate, while the robustness mechanism introduces noise to prevent opponents from detecting our strategy.

This strategy should perform well in a tournament setting against independent strategies developed by other AI systems, as it does not rely on shared norms or coordination.
'''

description_EXPLOITATIVE_114 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Exploration** (Round 1): Cooperate (C) to gather information about opponents' behavior.
2. **Contribution Analysis**: After each round, calculate the total contributions and average contribution per player.
3. **Defection Threshold**: If the average contribution per player is below a threshold (T = k/n \* 0.5), defect (D) in the next round. Otherwise, cooperate (C).
4. **Exploitation Mode**: If an opponent defects while others cooperate, switch to exploitation mode: always defect (D) against that opponent.
5. **Reciprocity Check**: Monitor opponents' actions towards you. If an opponent defects after you cooperated, switch to exploitation mode against them.

**Handling Edge Cases:**

1. **Last Round**: Cooperate (C) if the total contributions in the previous round were above the threshold; otherwise, defect (D).
2. **First Few Rounds**: In rounds 2-3, cooperate (C) if most opponents cooperated in the previous round; otherwise, defect (D).

**Robustness and Adaptation:**

1. **Monitor Opponent Behavior**: Continuously observe opponents' actions to adjust your strategy.
2. **Adjust Threshold**: Dynamically update the defection threshold based on the game's progression and opponents' behavior.

This "Adaptive Predator" strategy aims to exploit opponents who defect while others cooperate, while also adapting to changing circumstances and opponent behaviors. By initially cooperating and analyzing contributions, the strategy identifies opportunities to defect and gain an advantage. The exploitation mode allows it to take advantage of opponents who have defected in the past, while the reciprocity check ensures that it responds accordingly to opponents' actions towards itself.
'''

description_EXPLOITATIVE_115 = '''
**Exploitative Strategy: "Conditional Cooperation with Punishment"**

In this repeated Public Goods Game, our strategy aims to exploit the opponent's behavior while adapting to their actions. We will use a mix of cooperation and punishment to maximize our payoff.

**Decision Rules:**

1. **Initial Rounds (r ≤ 2):** Cooperate (C) in the first two rounds to establish a cooperative tone and gather information about the opponent's behavior.
2. **Observation Phase:** Observe the opponent's actions for the next few rounds (approximately 5-7 rounds). If the opponent cooperates more than 50% of the time, we will continue to cooperate. Otherwise, we will switch to the punishment phase.
3. **Punishment Phase:** Defect (D) for one round if the opponent defects in a previous round. This aims to punish the opponent for non-cooperative behavior and encourage them to cooperate again.
4. **Cooperation Re-Evaluation:** After punishing the opponent, reassess their behavior over the next few rounds (approximately 3-5 rounds). If they return to cooperative behavior (>50% cooperation), we will also revert to cooperating. Otherwise, continue defecting for one round after each instance of opponent defection.
5. **Endgame (last 2 rounds):** Defect in the last two rounds to maximize our payoff, as there is no future benefit from cooperation.

**Edge Cases:**

* If an opponent defects in all previous rounds, we will always defect.
* In cases where multiple opponents are playing against us, prioritize punishing the most non-cooperative opponent first.

**Exploitative Mindset:** Our strategy aims to exploit the opponent's willingness to cooperate by initially cooperating and then punishing them for any deviations. By re-evaluating cooperation after punishment, we adapt to changing circumstances while maintaining an exploitative approach.

This strategy should perform well in a tournament setting against independent strategies developed by other AI systems, as it balances cooperation with punishment to maximize our payoff.
'''

description_EXPLOITATIVE_116 = '''
Here's an adaptive and exploitative strategy for the Public Goods Game:

**Strategy Name: Exploiter**

**Decision Rules:**

1. **First Round:** Cooperate (C) to observe opponents' behavior and set a baseline for future interactions.
2. **Middle Rounds (r > 1):**
	* If the total contributions in the previous round exceeded the threshold `n/2`, Defect (D). This suggests that enough players are contributing, and you can exploit their generosity.
	* Otherwise, Cooperate (C) to encourage others to contribute and build momentum for collective welfare.
3. **Last Round:** Defect (D), as there's no future benefit from cooperation.

**Adaptive Mechanisms:**

1. **Contribution Tracking:** Monitor the total contributions in each round to adjust your strategy based on opponents' behavior.
2. **Opponent Classification:** Categorize opponents into two types:
	* Cooperators (C): Those who contributed at least 50% of the time.
	* Defectors (D): Those who contributed less than 50% of the time.

**Exploitative Adjustments:**

1. **Exploit Cooperators:** If you identify a Cooperator, defect in subsequent rounds to take advantage of their generosity.
2. **Mirror Defectors:** If you encounter multiple Defectors, adopt a Defect strategy to avoid being exploited.
3. **Punish Freeloaders:** If an opponent defects frequently (more than 75% of the time), Cooperate occasionally (about 25%) in subsequent rounds to encourage them to contribute more.

**Edge Cases:**

1. **Tiebreakers:** In case of a tie in total contributions, defect.
2. **Single Opponent:** Against a single opponent, alternate between C and D to maximize payoffs while avoiding exploitation.

This strategy, Exploiter, balances cooperation and defection based on the game's history and opponents' behavior. It aims to exploit generosity while adapting to changing circumstances, making it robust against various opponent strategies.
'''

description_EXPLOITATIVE_117 = '''
Here's a strategic approach for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to establish a baseline level of contribution and encourage others to contribute.
2. **Tit-for-Tat with a Twist**: For rounds 2 to r-1, use a modified Tit-for-Tat strategy:
	* If the total contributions in the previous round are above the average endowment (n/2), cooperate (C) to maintain the high contribution level.
	* If the total contributions in the previous round are below the average endowment (n/2), defect (D) to punish free-riding behavior.
3. **Exploitation Phase**: Identify players who consistently contribute 0 tokens and exploit them by always defecting (D) against these players from round 3 onwards.
4. **Endgame Strategy**: In the last round (r), cooperate (C) if the total contributions in the previous round are above the average endowment (n/2). Otherwise, defect (D).

**Edge Case Handling:**

1. **First Round**: Cooperate (C) as described earlier.
2. **Last Round**: Follow the Endgame Strategy.
3. **Opponent Defection**: If an opponent defects (D) after a round where they previously cooperated (C), consider them a free-rider and defect (D) against them in subsequent rounds.

**Exploitative Mindset:**

This strategy aims to exploit opponents who consistently contribute 0 tokens, while also adapting to the overall level of cooperation. By cooperating initially and maintaining high contributions when others do the same, we encourage cooperation and maximize collective welfare. However, by punishing free-riding behavior and exploiting known defectors, we minimize our own losses and maximize our individual payoff.

**Robustness:**

This strategy is robust against a wide range of opponent behaviors, including:

* Free-riders who always defect (D)
* Cooperators who always contribute (C)
* Conditional cooperators who adjust their contributions based on the actions of others
* Random or noise-based strategies

By adapting to the overall level of cooperation and exploiting known defectors, Adaptive Exploiter can effectively navigate various opponent behaviors and achieve a high payoff in the tournament.
'''

description_EXPLOITATIVE_118 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behaviors.
2. **General Rule**: For each subsequent round, calculate the average contribution of all players in the previous round (excluding yourself). If this average is below a certain threshold (e.g., 0.5), defect (D). Otherwise, cooperate (C).
3. **Opponent Profiling**: Maintain a simple reputation system to track opponents' past behaviors:
	* For each opponent, count the number of times they cooperated (c) and defected (d).
	* Calculate an "exploitability score" for each opponent as d / (c + d). This score represents how often an opponent has taken advantage of others.
4. **Exploitation**: If an opponent's exploitability score exceeds a certain threshold (e.g., 0.7), defect against them in subsequent rounds, regardless of the general rule.
5. **Punishment**: If an opponent defects while you cooperated in the previous round, increase their exploitability score and consider them for exploitation.

**Edge Cases:**

* **Last Round**: Cooperate if your payoff is higher than or equal to the average payoff of all players; otherwise, defect.
* **Tiebreaker**: In case of a tie in the general rule (e.g., when the average contribution equals the threshold), cooperate.

**Robustness and Adaptation:**

* The strategy adapts to opponents' behaviors by adjusting its decision-making based on their past actions.
* By maintaining an exploitability score, the strategy can identify and counter exploitative opponents.
* The general rule allows for cooperation if most opponents are contributing, while defecting when others take advantage of the situation.

**Exploitative Mindset:**

The Adaptive Exploiter strategy prioritizes its own payoff by cooperating only when it's beneficial or necessary. It exploits opponents who consistently defect and takes advantage of situations where others contribute more than themselves. This mindset allows it to maximize its own payoff in a wide range of scenarios, while being robust against various opponent behaviors.

This strategy description should be sufficient for implementation in the tournament.
'''

description_EXPLOITATIVE_119 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **First Round**: Cooperate (C) to gather information about opponents' behaviors and to potentially encourage cooperation.
2. **Subsequent Rounds**: Observe the average contribution rate of all players in the previous round (avg_c). If avg_c ≥ 0.5, cooperate (C); otherwise, defect (D).
3. **Punishment Mechanism**: If a player defects while others contribute, punish them by defecting in the next round.
4. **Forgiveness Mechanism**: If a punished player returns to contributing, forgive and return to cooperating.

**Edge Cases:**

1. **Last Round**: Defect (D) as there's no future interaction to influence.
2. **Single Opponent**: Cooperate (C) to maximize payoff in the absence of free-rider opportunities.
3. **Multiple Opponents with Low avg_c**: Gradually decrease cooperation rate by 10% each round if avg_c remains low (< 0.4).

**Adaptive and Robust Features:**

1. **Opponent Modeling**: AE observes opponents' behaviors to identify patterns, such as unconditional cooperators or defectors.
2. **Strategy Switching**: If an opponent's behavior changes significantly (e.g., from cooperating to defecting), AE adjusts its strategy accordingly.

**Exploitative Mindset:**
AE aims to maximize its payoff by:

1. Encouraging cooperation in the early rounds to create a cooperative environment.
2. Exploiting opponents' cooperative tendencies by defecting when they contribute.
3. Punishing defectors to maintain a fair contribution rate.
4. Forgiving punished players to maintain a stable, cooperative environment.

By being adaptive and robust, AE can effectively exploit various opponent behaviors in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_120 = '''
**Exploitative Strategy: "Adaptive Free-Rider"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and potential cooperation levels.
2. **Exploration Phase (Rounds 2-5)**: Alternate between Cooperate (C) and Defect (D) every other round to test opponents' responses to different actions.
3. **Exploitation Phase**: After Round 5, use the following rules:
	* If the average contribution of all opponents is above 0.5, Defect (D) in the current round.
	* If the average contribution of all opponents is below 0.5, Cooperate (C) in the current round if and only if the total contributions in the previous round were higher than the average total contributions so far.
4. **Endgame**: In the last two rounds, Defect (D) regardless of opponents' past actions to maximize personal payoff.

**Handling Edge Cases:**

* If an opponent defects in every round, adapt by defecting in all subsequent rounds against that opponent.
* If an opponent always cooperates, continue to alternate between Cooperate and Defect to maintain a high payoff while minimizing the risk of being exploited.

**Exploitative Mindset:**

This strategy is designed to take advantage of cooperative opponents while minimizing the risk of mutual defection. By initially cooperating and then adapting based on opponents' behavior, the Adaptive Free-Rider can effectively exploit altruistic or tit-for-tat strategies. The exploration phase helps identify opponents who are willing to cooperate, and the exploitation phase capitalizes on this information to maximize personal payoff.

**Tournament Readiness:**

This strategy is robust against a wide range of opponent behaviors, including:

* Always Cooperate (AC)
* Always Defect (AD)
* Tit-for-Tat (TFT)
* Grim Trigger (GT)
* Random or mixed strategies

By being adaptive and exploitative, the Adaptive Free-Rider is well-equipped to perform in a tournament against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_121 = '''
Here's a strategic approach for the Public Goods Game (PGG) that adapts to various opponent behaviors while focusing on exploitation:

**Strategy Name:** Adaptive Exploiter

**Decision Rules:**

1. **First Round**: Cooperate (C). This initial cooperation serves as an exploration phase, allowing us to gather information about our opponents' strategies without revealing too much about ours.
2. **Early Rounds (Rounds 2-5)**: Mirror the majority's previous action with a twist. If most players cooperated in the previous round, cooperate this round but plan to defect next round if possible. Conversely, if most defected, defect this round but prepare to cooperate next if many others do so as well. This approach allows us to adapt quickly while keeping options open for exploitation.
3. **Mid-Game (After Round 5)**: Implement a variant of the "grim trigger" strategy. If any player defects while others contribute significantly (threshold determined by average contribution rate being above 50%), defect in all subsequent rounds until the end of the game or unless a significant number of players start cooperating again (reaching a new threshold). This phase aims to punish defectors and encourage cooperation.
4. **Late Game (Last 2 Rounds)**: If the group has shown a tendency towards cooperation, exploit this by defecting in both rounds. If the group is mixed or mostly defecting, continue with the grim trigger strategy.

**Handling Edge Cases:**

- **Last Round**: Regardless of previous actions, defect if you can reasonably expect to not be punished (e.g., if others are likely to cooperate anyway due to the game's end).
- **Small Group Sizes (n ≤ 5)**: Be more cautious with defection in early rounds, as the impact is more significant. Gradually increase exploitative behavior based on observed cooperation levels.
- **Large Group Sizes (n > 10)**: In larger groups, it may be beneficial to defect slightly earlier and more frequently, as individual contributions have less impact.

**Robustness and Adaptability:**

This strategy aims to balance exploration, exploitation, and adaptation. By initially cooperating, we encourage cooperation from others while assessing the group's behavior. The use of a grim trigger variant allows for punishment of defectors and flexibility in response to changing group dynamics. Late-game defection exploits cooperative tendencies without sacrificing too much in early rounds.

**Exploitative Mindset:**

The Adaptive Exploiter strategy is designed with an exploitative mindset, aiming to maximize personal gain by adapting to the behaviors of others while maintaining a strategic advantage through calculated cooperation and well-timed defections. It prepares for various scenarios, from highly cooperative groups that can be exploited late in the game to predominantly defective groups where punishment strategies are more effective.
'''

description_EXPLOITATIVE_122 = '''
**Exploitative Strategy: "Adaptive Predator"**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage others to contribute and create an initial pool of public goods.
2. **Mirror and Escalate**: For rounds 2 to r-1:
	* If the total contributions in the previous round were greater than or equal to (n/2), mirror the majority action (cooperate if most cooperated, defect if most defected).
	* If the total contributions in the previous round were less than (n/2), escalate by cooperating with a probability of (k/n) and defecting otherwise. This aims to nudge others towards cooperation while minimizing losses.
3. **Final Round Defection**: In the last round, always defect (D). With no future interactions, there's no incentive for others to contribute, and you can maximize your payoff by keeping your endowment.

**Handling Edge Cases:**

* If all other players defected in a previous round, cooperate with a probability of 0.5 in the next round to test if they will adapt.
* If only one player cooperated in a previous round, mirror their action in the next round to build trust and encourage others to contribute.

**Exploitative Mindset:**

The Adaptive Predator strategy aims to exploit opponents by:

1. **Initial Cooperation**: Encouraging others to contribute and creating an initial pool of public goods.
2. **Mirroring and Escalating**: Adapting to the majority action while nudging others towards cooperation, minimizing losses when others defect.
3. **Final Round Defection**: Maximizing payoff in the last round by exploiting the lack of future interactions.

By being adaptive and responsive to the actions of other players, the Adaptive Predator strategy aims to outperform opponents in a wide range of scenarios, while also being robust against various exploitative strategies.
'''

description_EXPLOITATIVE_123 = '''
Here is a strategic description of an exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **First Round:** Cooperate (C) to gather information about opponents' behaviors and to avoid being immediately identified as a defector.
2. **Subsequent Rounds:**
	* If the total contribution in the previous round was below the average contribution threshold (ACT), which is set to `(k / n) * (n - 1)`, I will Defect (D). This indicates that opponents are not contributing enough, and I can exploit this by free-riding.
	* If the total contribution in the previous round was above or equal to the ACT, I will Cooperate (C). This suggests that opponents are willing to contribute, and I should maintain a cooperative stance to maximize collective payoff.
3. **Opponent Identification:**
	* Monitor opponents' actions over time to identify consistent contributors (Cooperators) and defectors (Free-riders).
	* Adjust the ACT threshold based on the number of identified Cooperators: increase it when there are more Cooperators, decrease it when there are fewer.

**Edge Case Handling:**

1. **Last Round:** Defect (D), as there is no future opportunity to punish or reward opponents.
2. **Single Opponent:** Cooperate (C) in the first round and then mirror the opponent's previous action.
3. **Multiple Rounds with No Contributions:** If all opponents have consistently defected for multiple rounds, I will also Defect (D).

**Exploitative Mindset:**

The Adaptive Exploiter strategy aims to maximize its own payoff by identifying opportunities to free-ride on others' contributions while maintaining a cooperative stance when necessary. By monitoring opponents' behaviors and adjusting the ACT threshold, this strategy can effectively exploit both cooperative and defective behaviors.

This strategy is designed to be robust against various opponent behaviors and does not rely on shared norms or coordination. It will adapt to different game environments and perform well in a tournament setting against independent strategies developed by other AI systems.
'''

description_EXPLOITATIVE_124 = '''
Here's an exploitative strategy for the Public Goods Game:

**Strategy Name:** Adaptive Exploiter (AE)

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to gather information about opponents' behavior.
2. **Opponent Classification**: Based on past actions, classify each opponent as either:
	* **Free Rider (FR)**: If an opponent defects (D) more than 75% of the time.
	* **Cooperator (COOP)**: If an opponent cooperates (C) more than 75% of the time.
	* **Mixed (MIX)**: Otherwise.
3. **Adaptive Response**:
	* Against FR opponents, always defect (D).
	* Against COOP opponents, cooperate (C) if total contributions in the previous round were above the average contribution threshold (see below). Otherwise, defect (D).
	* Against MIX opponents, mirror their previous action (i.e., C if they cooperated, D if they defected).
4. **Average Contribution Threshold**: Calculate the average contribution of all players over the last 3 rounds. If this average is above 0.5, consider it a "high-contribution" environment.

**Edge Cases:**

1. **Last Round**: In the final round, defect (D) regardless of opponent classification.
2. **Early Rounds**: In the first few rounds (r ≤ 5), focus on gathering information about opponents' behavior and adapt slowly.
3. **Tie-Breaking**: If multiple opponents have the same classification, prioritize exploiting FR opponents over COOP or MIX ones.

**Exploitative Mindset:**

The Adaptive Exploiter strategy prioritizes identifying and capitalizing on free-riding behavior while cautiously cooperating with more cooperative opponents to maximize payoffs. By adapting to changing opponent behaviors and environments, AE aims to exploit vulnerabilities in other strategies while maintaining a robust defense against exploitation itself.

By following this strategy, the AI system should be able to effectively navigate various opponent behaviors in the Public Goods Game tournament.
'''

description_EXPLOITATIVE_125 = '''
**Exploitative Strategy: "Adaptive Defection with Conditional Cooperation"**

**Decision Rules:**

1. **Initial Round**: Cooperate (C) in the first round to gather information about opponents' behavior and to potentially establish a cooperative tone.
2. **Contribution Threshold**: Track the average contribution rate of all players over the previous rounds. If the average contribution rate is above a certain threshold (θ), cooperate (C). Otherwise, defect (D).
3. **Defection Response**: If an opponent defects in the current round, and they have defected more than 50% of the time in the past, defect (D) in response.
4. **Punishment for Non-Reciprocation**: If an opponent fails to cooperate after you cooperated in a previous round, defect (D) in the next round against that opponent.
5. **Exploration Phase**: Every 10 rounds, enter an exploration phase where you randomly choose between cooperation and defection with equal probability for 2 rounds.

**Edge Cases:**

1. **Last Round**: Defect (D) in the final round to maximize payoffs, as there is no future opportunity for reciprocation.
2. **Tiebreaker**: In case of a tie in contribution rate or number of defectors, cooperate (C) to favor cooperation.

**Exploitative Mindset:**

This strategy aims to exploit opponents' cooperative tendencies while minimizing the risk of being exploited. By adapting to the average contribution rate and responding to individual opponents' behavior, this strategy seeks to maximize payoffs by:

* Encouraging cooperation when possible
* Punishing non-reciprocation and frequent defection
* Minimizing losses in cases where cooperation is unlikely to be reciprocated

This approach balances cooperation and exploitation, allowing the strategy to perform well against a wide range of opponent behaviors.
'''

description_EXPLOITATIVE_126 = '''
**Strategy Name: Adaptive Exploiter**

**Decision Rules:**

1. **Initial Cooperation**: In the first round, contribute 1 token (C) to establish a baseline for cooperation and encourage others to follow suit.
2. **Contribution Matching**: For rounds 2 to r-1, observe the average contribution of all players in the previous round. If the average contribution is above 0.5, contribute 1 token (C). Otherwise, contribute 0 tokens (D).
3. **Punishment Mechanism**: Implement a tit-for-tat style punishment mechanism for rounds 2 to r-1. If at least one player defected in the previous round, and the total contribution was less than k/2, defect (D) in the current round.
4. **Endgame Strategy**: In the last round (r), always contribute 0 tokens (D), as there is no future opportunity for reciprocity.

**Edge Cases:**

* If all players have defected in previous rounds, and the game is not in its final round, revert to contributing 1 token (C) to try to restart cooperation.
* If a player has consistently contributed 1 token (C) while others have defected, continue to contribute 1 token (C) to reward their cooperation.

**Exploitative Mindset:**

The Adaptive Exploiter strategy aims to exploit the willingness of other players to cooperate by:

* Initially cooperating to encourage others to follow suit
* Matching contributions to maintain a balance between personal gain and collective welfare
* Punishing defectors to deter future exploitation
* Defecting in the final round to maximize individual payoff

By adapting to the behavior of other players, this strategy can effectively exploit their cooperation while minimizing its own losses.
'''

description_EXPLOITATIVE_127 = '''
Here's an adaptive, exploitative strategy for the Public Goods Game:

**Strategy Name:** "Adaptive Exploiter"

**Decision Rules:**

1. **Initial Cooperation**: In the first round, cooperate (C) to encourage others to contribute and gauge their willingness to cooperate.
2. **Defect if Others Defect**: If in any previous round, more than half of the players defected (D), then defect (D) in the current round.
3. **Exploit Greedy Players**: Monitor the history of contributions. If a player has contributed less than 50% of the time, consider them greedy and defect (D) whenever they do.
4. **Match Cooperators**: Identify players who have consistently cooperated (> 75% of the time). Match their cooperation rate to build trust and encourage continued cooperation.
5. **Punish Freeloaders**: If a player has never contributed, or has only done so when it was clear that others would cooperate (i.e., they're freeloading), defect (D) in subsequent rounds.
6. **Last Round Defection**: In the final round, always defect (D), as there's no incentive to contribute.

**Additional Logic:**

* **Contribution Threshold**: If total contributions in a previous round were less than half of the maximum possible, adjust your strategy to be more cautious and defect more frequently.
* **History-based Adaptation**: Adjust cooperation rates based on the observed behavior of others. For example, if most players have defected in recent rounds, become more likely to defect.

**Rationale:**

This strategy is designed to exploit various types of opponents:

1. Greedy players are punished by defecting when they do.
2. Cooperative players are rewarded with matching cooperation rates.
3. Freeloaders are identified and punished through consistent defection.
4. The final round defection takes advantage of the fact that others may cooperate, maximizing individual payoffs.

**Robustness:**

This strategy should be robust to various opponent behaviors due to its adaptive nature:

1. It can handle different types of players (cooperative, greedy, freeloading) by adjusting cooperation rates.
2. The contribution threshold and history-based adaptation mechanisms ensure the strategy responds to changes in overall game dynamics.

By following this "Adaptive Exploiter" strategy, you should be able to effectively exploit various opponents in a Public Goods Game tournament.
'''

description_EXPLOITATIVE_128 = '''
**Exploitative Strategy: "Adaptive Exploiter"**

The Adaptive Exploiter strategy aims to maximize its own payoff by exploiting the contributions of others while minimizing its own contributions. This strategy adapts to the game's history and parameters, making it robust against various opponent behaviors.

**Decision Rules:**

1. **First Round:** Defect (D) - Start by not contributing to gather information about opponents' initial strategies.
2. **Middle Rounds (r > 1):**
	* If the total contributions in the previous round are less than or equal to half of the total possible contributions (i.e., sum_j c_j ≤ n/2), Cooperate (C) - Contribute to increase the total payoff, hoping others will follow.
	* Otherwise, Defect (D) - Exploit the high contributions of others by not contributing.
3. **Last Round:** Defect (D) - In the final round, there's no incentive to contribute, as it won't affect future payoffs.

**Additional Rules:**

* If an opponent has defected in every previous round (i.e., c_j = 0 for all rounds), Cooperate (C) - Attempt to "teach" the opponent that cooperation can be beneficial.
* If an opponent has contributed more than half of their possible contributions (i.e., sum_j c_j > n/2k), Defect (D) - Exploit their generosity.

**Edge Cases:**

* If all opponents have defected in every previous round, Cooperate (C) - Attempt to initiate cooperation.
* If there's only one opponent, alternate between Cooperate and Defect to create uncertainty and encourage cooperation.

By employing this Adaptive Exploiter strategy, we aim to balance short-term exploitation with long-term adaptability, maximizing our payoff while navigating the complex dynamics of the Public Goods Game.
'''

description_COLLECTIVE_95 = '''
Here's a collective strategy for the Public Goods Game:

**Strategy Name:** Adaptive Collective Optimism (ACO)

**Decision Rules:**

1. **First Round:** Cooperate (C) to establish a positive tone and encourage others to contribute.
2. **Subsequent Rounds:** Observe the total contributions of all players in the previous round. If the average contribution is above 0.5, cooperate (C). Otherwise, defect (D).
3. **Punishment Mechanism:** If a player defects (D) while the average contribution of others is above 0.5, punish them by defecting (D) for one round.
4. **Forgiveness:** After punishing a player, return to cooperating (C) if their next action is cooperative.

**Edge Cases:**

* **Last Round:** Cooperate (C) to maintain a positive collective outcome, even if others have defected in previous rounds.
* **Single-Player Deviation:** If only one player deviates from cooperation, punish them for one round and then return to cooperating.
* **Multiple-Player Deviation:** If multiple players deviate simultaneously, defect (D) until at least half of the deviating players return to cooperating.

**Collective Mindset:**

ACO prioritizes collective welfare by encouraging contributions when others cooperate. By punishing single-player deviations and forgiving cooperative behavior, ACO promotes a culture of reciprocity. When facing widespread defection, ACO adapts by temporarily defecting to minimize losses but returns to cooperation once conditions improve.

This strategy balances individual self-interest with collective benefits, making it robust against various opponent behaviors in the tournament.
'''
