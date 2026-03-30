"""
Strategy descriptions for public_goods.

Generated with:
- Provider: Client
- Model: mistral:7b
"""


description_PROSOCIAL_1 = '''
 Strategy Name: Adaptive Tit-for-Tat with Public Goods Alignment (ATfTA-PG)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to foster a cooperative environment and show goodwill (c_i = 1).
   - For subsequent rounds, cooperate if the majority of players cooperated in the previous round (c_i = 1 if total_contributions > (n/2)), otherwise defect (c_i = 0).
   - If a player deviates from the strategy, they will be punished by defecting for t_p rounds, where t_p is the number of consecutive defections by the player. Once the player returns to cooperating, ATfTA-PG will return to its original cooperation pattern after t_r rounds, where t_r is a forgiveness factor that determines how quickly the strategy forgets past defections (t_r < n).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, cooperate regardless of the total contributions from the previous round to maximize individual payoff.
   - If a player deviates from the strategy but later returns to cooperation after t_p rounds, reset the punishment counter to zero (t_p = 0).

3. Be prosocial - Clearly align with the prosocial mindset:
   - Cooperative by nature, ATfTA-PG demonstrates trust and goodwill in the initial stages of the game.
   - Punishes uncooperative behavior, but shows forgiveness to encourage return to cooperation.
   - Adapts to a wide range of opponent behaviors by adjusting its strategy based on the collective actions of other players.

Pseudocode:
```python
def ATfTA_PG(round, history, n, k):
    if round == 1:
        cooperate = True
    else:
        cooperate = total_contributions > (n/2)

    if not cooperate and punish >= t_p:
        defect = True
    elif cooperate and forgiveness > (t_r - (round - 1)):
        defect = False
        forgiveness -= 1
    else:
        defect = not cooperate

    if defect and not history[round - 1]: # player deviated in the previous round
        punish += 1
        forgiveness = t_r

    return cooperate
```

In this pseudocode, `history` is a list of booleans representing whether each player cooperated in the previous round. The `punish`, `forgiveness` and `t_p`, `t_r` variables control the strategy's response to defections and forgiveness towards players that return to cooperation after deviating.
'''

description_PROSOCIAL_2 = '''
 Strategy Name: Tit-for-Tat Adaptive Cooperation (TFTAC)

1. Specify decision rules:
   - In the first round, cooperate to establish trust and set a positive tone for the game.
   - For subsequent rounds, follow the actions of the most cooperative player from the previous round (i.e., the player who contributed the most among all players). If multiple players tied for the most contributions, follow the action of one of them randomly or according to some predefined preference order. If no player cooperated in the previous round, defect in this round as a punishment.
   - If the game enters the last few rounds (e.g., the final 10%), revert to always cooperate to maximize potential payoffs from late-game cooperation.

Pseudocode:
```
function TFTAC(history, n, k):
    if round_number == 1:
        action = "Cooperate"
    else:
        max_contributions = 0
        cooperative_player = None

        for i in range(n):
            if sum(history[round_number - 1][i]) > max_contributions:
                max_contributions = sum(history[round_number - 1][i])
                cooperative_player = i

        if max_contributions == 0:
            action = "Defect"
        else:
            action = "Cooperate" if history[round_number - 1][cooperative_player] > 0 else "Defect"

    if round_number >= (r * 0.9):
        action = "Cooperate"

    return action
```

2. Handle edge cases:
   - In the first round, cooperate as mentioned above.
   - If the history is empty or incomplete for some reason, default to a conservative strategy such as always defecting until the history becomes more informative.
   - When the game ends, consider the last few rounds' cooperation to maximize potential payoffs.

3. Be prosocial:
   - By punishing defections and rewarding cooperation, TFTAC encourages other players to cooperate while also protecting itself against free riders.
   - As the game progresses, TFTAC tends to favor cooperation when there are cooperative players in the group, fostering a more prosocial environment.
   - By re-evaluating its actions based on recent history, TFTAC adapts to changes in other players' behavior and maintains a flexible approach that encourages long-term cooperation.
'''

description_PROSOCIAL_3 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Cooperative Strategy (TFT-PACS)

1. Decision Rules:
   - Start with cooperating in the first round (C_1 = True). This initial cooperation is a sign of trust and goodwill towards others.
   - In subsequent rounds, mirror the actions of other players from the previous round. If all opponents cooperated in the previous round (total_contributions > 0), cooperate again (C_t = total_contributions_{t-1} > 0). Otherwise, defect (C_t = False).

```python
def TFT_PACS(round, own_action_history, opponents_action_history):
    if round == 1:
        return True  # Cooperate in the first round
    else:
        last_own_action = own_action_history[round-1]
        last_opponents_actions = opponents_action_history[round-1]
        if all(last_opponents_actions):  # All opponents cooperated last round
            return True
        else:
            return False
```

2. Handle Edge Cases:
   - In the last round, there is no need to retaliate or reciprocate, as the game ends. Therefore, if it's detected that this is the final round (r == round), cooperate regardless of opponents' previous actions.

```python
def TFT_PACS(round, own_action_history, opponents_action_history, r):
    if round == r:  # Last round
        return True  # Cooperate in the final round
    else:
        return strategy(round, own_action_history, opponents_action_history)
```

3. Be Prosocial:
   - The TFT-PACS strategy aims to foster cooperation among players by showing trust and reciprocity while remaining adaptive and robust against a wide range of opponent behaviors. It aligns with the prosocial mindset by fostering long-term relationships and promoting mutual benefits among players.
   - This strategy assumes that if opponents cooperate, they are also likely to reciprocate cooperation in subsequent rounds, thus building trust and increasing the probability of cooperation in future interactions. If opponents do not reciprocate cooperation, TFT-PACS will defect, signaling a lack of trust and reducing chances for further collaboration.
   - The strategy does not rely on external assumptions or coordination mechanisms, making it applicable to various game settings and opponents' behaviors.
'''

description_PROSOCIAL_4 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Decision Rules:
   - In the first round (t=1), cooperate (play C) to demonstrate a prosocial intent and establish trust.
   - For subsequent rounds (t > 1):
     - If an opponent cooperated in the previous round, reciprocate by cooperating as well (play C). This encourages continued cooperation and reinforces trust.
     - If an opponent defected in the previous round, also defect in the current round (play D). This responds to uncooperative behavior while leaving room for rebuilding trust if the opponent changes their strategy.

2. Edge Cases:
   - In the last round (t=r), cooperate regardless of the opponent's action in the previous round. This final act of cooperation showcases a continued prosocial mindset and may encourage reciprocal behavior from opponents.
   - When facing new opponents, follow the initial rule for the first round and adapt to their behavior from thereon. Maintain cooperation if they cooperate and defect if they defect.

3. Prosocial Alignment:
   - TFT-AC strategy emphasizes fairness and trust by reciprocating cooperative actions and punishing defections lightly (one round of defection). This approach encourages opponents to adopt prosocial behavior as well, fostering cooperation in the long run.
   - By following simple decision rules and demonstrating both trust and punishment, TFT-AC exhibits a clear prosocial mindset that is adaptive to various opponent behaviors.
'''

description_PROSOCIAL_5 = '''
 Strategy Name: Adaptive Tit-for-Tat with Gradient Descent (ATfT-GD)

1. Specify decision rules:
   - In every round t, evaluate the average cooperation level across all past rounds (average_cooperation_level = Σ(s=t-m to t-1) total_contributions_round_s / m)
   - If average_cooperation_level > threshold, cooperate; otherwise defect. The threshold is adjusted using gradient descent to find the optimal balance between cooperation and self-interest.
       - Initialize threshold with a moderate value (e.g., 0.5).
       - For each round t, calculate error as (1 - payoff_t) - optimal_payoff, where optimal_payoff is a moving average of past payoffs.
       - Adjust threshold using the learning rate to minimize the sum of squared errors: threshold = threshold + learning_rate * (error_t - (1/m) * Σ(s=t-m to t-1) error_s).

2. Handle edge cases:
   - In the first round, defect since there is no past data to make a decision.
   - In the last round, cooperate if average_cooperation_level > threshold; otherwise defect, as we aim for a prosocial strategy.

3. Be prosocial:
   - ATfT-GD is designed to be responsive and fair, following a tit-for-tat approach but with an adaptive learning mechanism that adjusts its cooperation level based on the overall cooperation trend in the game. The goal is to balance individual payoff with group wellbeing while adapting to various opponent behaviors.

Pseudocode:
```
def ATfT_GD(threshold, m, learning_rate):
    total_contributions = 0
    past_errors = []
    for t in rounds:
        if t == 1:
            cooperate = False
        else:
            average_cooperation_level = total_contributions / m
            cooperate = (average_cooperation_level > threshold)
            payoff = (1 - cooperate) + (k/n * total_contributions)

        if t < r:
            total_contributions += cooperation_level_in_round_t
            past_errors.append((1 - payoff) - optimal_payoff)

        if t == r or is_last_round():
            cooperate = (average_cooperation_level > threshold)

        update_threshold(threshold, learning_rate, past_errors, m)
        return cooperate
```

In this pseudocode:
- `update_threshold()` function updates the threshold based on gradient descent.
- `optimal_payoff` is a moving average of payoffs from the last `m` rounds.
- `is_last_round()` checks if the current round is the final round in the game.
'''

description_PROSOCIAL_6 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TFT-AC starts by cooperating in the first round to foster a harmonious environment, setting the initial tone of cooperation. For subsequent rounds, it adapts its behavior based on the history of interactions with other players. If the opponent cooperates in the previous round, TFT-AC cooperates in return to reinforce trust and maintain cooperation. However, if the opponent defected in the previous round, TFT-AC also defects to penalize the opponent's self-interested behavior and signal disapproval.

   Pseudocode:
   ```
   function TFT_AC(history):
       if round = 1:
           return Cooperate()

       previous_round = history[-1]
       if previous_round == Cooperate():
           return Cooperate()
       else:
           return Defect()
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   TFT-AC will always cooperate in the first round to initiate cooperation. In the last round or when the game reaches a predefined termination condition (e.g., a fixed number of rounds), TFT-AC may choose to cooperate or defect based on the opponent's behavior during the game, aiming to maintain a positive impact and encouraging prosocial behavior in the long run.

3. Be prosocial - Clearly align with the prosocial mindset
   TFT-AC promotes a prosocial environment by reinforcing cooperation when others cooperate, as well as punishing self-interested behavior through defection when necessary. This strategy's adaptive nature encourages long-term collaboration while also being resilient to opponents who may adopt less prosocial strategies. By doing so, TFT-AC seeks to establish a balance between individual and collective success, fostering an overall positive and collaborative gameplay experience.
'''

description_PROSOCIAL_7 = '''
 Strategy Name: Tit-for-Tat Prosocial (TfT-P)

1. Decision Rules:
   - Initiate cooperation (C) in the first round to show a friendly intention and promote trust among players.
   - In subsequent rounds, cooperate (C) if all opponents cooperated in the previous round. Otherwise, defect (D). This mimics cooperative behavior while also punishing defection, fostering mutual trust and cooperation over time.

Pseudocode:
```
function TfT-P(round, opponent_actions):
  if round == 1:
    return 'C'  # Initiate cooperation in the first round

  previous_opponent_actions = opponent_actions[round - 1]
  if all(previous_opponent_actions == ['C']):
    return 'C'  # Cooperate if all opponents cooperated in the previous round
  else:
    return 'D'  # Defect if any opponent defected in the previous round
```

2. Handle edge cases:
   - Last round: Since players have no information about future rounds, they cannot adjust their strategy based on the last round. The TfT-P strategy will behave as it does in regular rounds.
   - First encounter with a new opponent: Initiate cooperation (C) to establish trust and encourage reciprocation in the long term.

3. Be prosocial:
   - TfT-P promotes cooperation by punishing defection while rewarding cooperative behavior, encouraging players to act prosocially within the game.
   - The strategy also fosters mutual trust by maintaining a consistent and predictable pattern of cooperation, which can help build long-term relationships and stability among players.
'''

description_PROSOCIAL_8 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Cooperation (TFT-PAC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TFT-PAC cooperates in the first round, then mirrors the previous action of the opponent in the current round. If the opponent cooperated in the last round, TFT-PAC cooperates; otherwise, it defects. This strategy encourages long-term reciprocity while being simple and robust to various opponent behaviors.

   Pseudocode:
   ```
   function TFT_PAC(opponent_action_history):
       if round = 1:
           return COOPERATE
       else:
           last_round_opponent_action = opponent_action_history[-1]
           return last_round_opponent_action
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the context of this game, there are no specific edge cases to handle beyond the initial round where TFT-PAC cooperates regardless. However, it's worth noting that in a tournament setting, some strategies may start with a predefined number of initial defects or cooperations to exploit opponents who adopt a naive strategy like always cooperating. In such cases, TFT-PAC might be adapted to include a learning phase where it adapts its initial behavior based on the observed frequency of cooperation from opponents.

3. Be prosocial - Clearly align with the prosocial mindset
   TFT-PAC aims at fostering long-term cooperation by being cooperative in the first round and reciprocating the opponent's actions. By adopting this strategy, players incentivize each other to continue cooperating, as a player who defects in one round will likely face defections in subsequent rounds from TFT-PAC and other opponents that mirror its behavior. This creates a prosocial environment where cooperation is encouraged through reciprocity and long-term trust building.
'''

description_PROSOCIAL_9 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Strategy (TfT-PAS)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, the TfT-PAS player will Cooperate (C). This is an overture of goodwill and fosters a prosocial atmosphere.
   - For subsequent rounds, the player will mimic the actions of the previous round's majority: if more than half of the players cooperated in the last round, the player will also Cooperate; otherwise, the player will Defect (D).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, TfT-PAS will mimic the majority of the previous round regardless of the number of rounds left, as it understands this round is the final one.
   - If there's a tie in the number of cooperators (more than half), TfT-PAS will follow its default strategy: Cooperate if the current round isn't the first or last, Defect otherwise.

3. Be prosocial - Clearly align with the prosocial mindset
   - TfT-PAS follows a reciprocal approach, mimicking the cooperative behavior of other players while also being willing to defect when others do so. This strategy encourages sustained cooperation and fosters a prosocial environment by rewarding cooperative players and punishing defectors with retaliation.
   - TfT-PAS will revert to cooperating in the first round, demonstrating an initial act of goodwill to promote trust among players and create opportunities for future cooperation.

Pseudocode:
```python
def tit_for_tat_prosocial(round, player_actions, n):
  if round == 1:
    action = "C" # Cooperate in the first round
  else:
    majority = len([action for action in player_actions if action == 'C']) >= (n//2) + 1
    action = "C" if majority else "D" # Mimic previous round's majority
  return action
```
'''

description_PROSOCIAL_10 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive (TfT-PA)

1. Specify decision rules:
   - In the first round, cooperate to show good intentions and trust other players. This initiates a cooperative environment (C_i = 1 in t=1).
   - For subsequent rounds, observe the previous round's total contributions (total_contributions_t-1) and perform the following:
       - If total_contributions_t-1 ≥ (n-1), cooperate as it indicates a majority of players are prosocial and adhering to cooperation. This encourages long-term cooperation (C_i = 1 if total_contributions_t-1 ≥ (n-1)).
       - If total_contributions_t-1 < (n-1), defect as it indicates a lack of cooperation or betrayal. This punishes uncooperative behaviour and encourages others to cooperate in the future (C_i = 0 if total_contributions_t-1 < (n-1)).
   - If a player switches their strategy, TfT-PA will return to cooperating in the next round to give them another chance to reciprocate cooperation.

2. Handle edge cases:
   - Last round, cooperate regardless of the total contributions from previous rounds as it encourages cooperation in the final round and doesn't affect the total payoff for that round.
   - In the case where n = 1, TfT-PA cannot play as there is no opponent to interact with.

3. Be prosocial:
   - TfT-PA aims to encourage long-term cooperation by responding positively to cooperative behaviour and punishing defection. It encourages players to develop trust and reciprocity, fostering a prosocial environment in the game.
   - By only cooperating when a majority of players contribute, TfT-PA balances individual incentives with group benefits, promoting fairness and cooperation among all players.
'''

description_PROSOCIAL_11 = '''
 Strategy Name: Tit-for-Tat with Adaptive Generosity (TfT-AG)

1. Specify decision rules:
   - TfT-AG cooperates in the first round to foster a cooperative environment and then mimics the average cooperation level of the last 'h' rounds, where 'h' is a tunable parameter. This adaptive generosity allows for responsiveness to changing group dynamics over time.
   - If the average cooperation level is below a certain threshold (say 50%), TfT-AG gradually increases its cooperative efforts by incrementally increasing 'h'. Conversely, if the average cooperation level is above the threshold, it decreases 'h' to avoid being exploited.
   - To avoid getting trapped in cycles of defection, TfT-AG defects when the opponent consistently defects for more rounds than a certain tolerance limit (say 't'). After that, it returns to cooperating and reassesses its decision based on the average cooperation level in the following 'h' rounds.

Pseudocode:

```python
def TfT_AG(history, h=5, t=3):
    avg_cooperation = sum(history[-h:]) / h

    if len(history) <= h:  # First few rounds
        action = 'C'  # Cooperate to initiate cooperation

    elif avg_cooperation >= threshold:  # Majority cooperates, be generous
        action = 'C'
        h *= generosity_factor

    elif avg_cooperation <= (1 - threshold):  # Majority defects, be cautious
        action = 'D'
        h /= cautiousness_factor

    else:  # Mixed cooperation, assess situation and adjust 'h'
        count_defects = sum(map(lambda x: 1 if x == 'D' else 0, history[-t:]))

        if count_defects > t:  # Opponent consistently defects, react
            action = 'D'
            h *= generosity_factor

        else:  # Opponent shows signs of cooperation or unpredictability
            action = 'C'

    return action
```

2. Handle edge cases:
   - In the first round, TfT-AG cooperates to encourage others to do the same (see point 1).
   - When reaching the last round, TfT-AG evaluates its decision based on the average cooperation level of the previous 'h' rounds as usual. However, it does not make further adjustments to 'h'.

3. Be prosocial:
   - By mimicking the group's cooperative behavior and gradually increasing or decreasing generosity based on the situation, TfT-AG fosters trust and cooperation within the group over time. This strategy aligns with a prosocial mindset by balancing self-interest with the collective wellbeing of the community.
   - By not defecting consistently when others cooperate, TfT-AG avoids being perceived as untrustworthy or exploitative. Instead, it rewards cooperation and punishes defection in a fair manner, encouraging long-term cooperation within the group.
'''

description_PROSOCIAL_12 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) Prosocial Strategy for N-Player Public Goods Game

1. Specify decision rules:
   - In the first round, cooperate (C), as there is no previous information about opponents' behavior.
   - For subsequent rounds, if an opponent cooperated in the previous round, also cooperate. If not, defect. This encourages cooperation and punishes defection.

Pseudocode:
```python
def ATFT(history, n, k):
    current_round = len(history) + 1
    if current_round == 1:
        return 'C'  # Cooperate in the first round
    else:
        last_round_action = history[-1]  # Get action from last round
        if last_round_action == 'C':  # If opponent cooperated last round, cooperate this round
            return 'C'
        else:  # If opponent defected last round, defect this round
            return 'D'
```

2. Handle edge cases:
   - In the last round, cooperate regardless of previous actions, as the game ends after this round.
   - For the first few rounds (e.g., 5), allow some flexibility in deciding whether to cooperate or defect based on the percentage of opponents who have cooperated so far. This helps avoid getting stuck in a cycle of defection with uncooperative opponents early on.

Pseudocode:
```python
def ATFT(history, n, k, num_initial_rounds=5):
    current_round = len(history) + 1
    if current_round == 1:
        return 'C'  # Cooperate in the first round
    elif current_round <= num_initial_rounds:
        percentage_cooperators =len(history) * (len([i for i in history if i == 'C']) / len(history))
        if percentage_cooperators >= cooperation_threshold:  # Set cooperation_threshold based on desired prosocialness
            return 'C'
        else:
            return 'D'
    else:
        last_round_action = history[-1]  # Get action from last round
        if last_round_action == 'C':  # If opponent cooperated last round, cooperate this round
            return 'C'
        else:  # If opponent defected last round, defect this round
            return 'D'
```

3. Be prosocial:
   - The strategy encourages cooperation by rewarding opponents who contribute to the public good and punishing those who do not.
   - By being forgiving in the initial rounds, the strategy allows for opportunities to establish cooperation with uncooperative opponents early on.
   - Adjusting the cooperation_threshold parameter can influence the overall prosocialness of the strategy, allowing it to be fine-tuned based on specific game conditions or desired outcomes.
'''

description_PROSOCIAL_13 = '''
 Strategy Name: Tit-for-Tat Prosocial (TfTP) Strategy

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate (C). This is a friendly gesture to initiate cooperation and set a prosocial tone.
   - For subsequent rounds t > 1, mimic the actions of the previous round: if players cooperated in round t-1, also cooperate in round t; otherwise defect.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First Round (t=1): Cooperate (C). As mentioned earlier, this is a friendly gesture to initiate cooperation and set a prosocial tone.
   - Last Round (t=r): Mimic the actions of the previous round, but since we can't predict future behavior in a one-shot game, make an informed decision based on past experiences with other strategies.
   - If there are multiple instances where the game reaches its last round, consider maintaining consistency by following the same cooperative or defection action as the previous last round.

3. Be prosocial - Clearly align with the prosocial mindset:
   - The TfTP strategy aims to foster cooperation while also being robust against exploitation. By cooperating in the first round and mimicking other players' actions, the strategy demonstrates a willingness to collaborate and promote a positive social environment.
   - When other players cooperate, the strategy reciprocates with cooperation, fostering trust and long-term relationships. When others defect, the strategy responds with defection as well, preventing exploitation but also signaling that cooperation is conditional upon the opponent's actions.

Pseudocode for TfTP Strategy:
```
def tf_tp(round_number, game_history):
  if round_number == 1:
    return 'C' # Cooperate in the first round as a friendly gesture
  else:
    last_round = game_history[-1] # Get the action from the last round
    if last_round == 'C':
      return 'C' # Mimic cooperation if others cooperated in the last round
    else:
      return 'D' # Mimic defection if others defected in the last round
```
'''

description_PROSOCIAL_14 = '''
 Strategy Name: Tit-for-Tat Prosocial (TfT-P)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially cooperate (C) in the first round to show goodwill and promote trust.
   - After the initial cooperation, adopt a reciprocation policy: if an opponent cooperates (C), respond with cooperation (C); if an opponent defects (D), also defect (D). This helps maintain cooperation while being robust against aggressive opponents.
   - To be prosocial, occasionally display altruism by occasionally cooperating even when the opponent has defected in the previous round. This can help rebuild trust and collaboration over time. The probability of this altruistic action should decrease as the number of consecutive defections increases. A possible formula for this probability could be:
      p_altruism = min((n - consecutive_defeats) / n, 0.2)
   - In the last round, cooperate (C) to ensure a positive final payoff and potentially encourage cooperation in future games.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round: Cooperate (C).
   - In the last round: Cooperate (C).
   - In subsequent rounds: Implement the reciprocation policy described above and add occasional altruism as needed.

3. Be prosocial - Clearly align with the prosocial mindset:
   - Promote trust by initially cooperating and maintaining a reciprocal relationship in following rounds.
   - Display altruism through occasional cooperation, even after an opponent has defected. This helps rebuild trust and encourages long-term collaboration.
   - Ensure a positive final payoff by cooperating in the last round, further promoting prosocial behavior.
'''

description_PROSOCIAL_15 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Cooperation (TPTAC)

1. Decision Rules - TPTAC cooperates when the majority of players have also cooperated in the previous round, and defects otherwise. It adapts to changes in opponent behavior by mirroring their cooperation but punishes defection with prolonged defection.

   Pseudocode:
   ```
   function TPTAC(history):
       if history[round - 1] > (n / 2) cooperators:
           return 'Cooperate'
       else:
           return 'Defect'
   ```

2. Handle Edge Cases - In the first round, TPTAC initiates cooperation as a peaceful gesture to foster mutual understanding. In the last round and any other exceptional situations where the game might terminate prematurely (e.g., due to time constraints), TPTAC chooses to cooperate if the average cooperation rate in the preceding rounds is above 50%.

   Pseudocode:
   ```
   function TPTAC(history, round = current round):
       if round == 1:
           return 'Cooperate'
       if average_cooperation_rate(history) > 0.5 and round < r:
           return 'Cooperate'
       else:
           return TPTAC(history)
   ```

3. Be Prosocial - TPTAC aims to maintain a stable cooperation environment by promoting reciprocity, forgiveness, and trust among players. It punishes defection but is quick to forgive once cooperative behavior resumes. By adhering to these principles, TPTAC fosters cooperation and encourages prosocial interactions within the game.

In summary, TPTAC chooses to cooperate when the majority of players cooperated in the previous round, initiates cooperation in the first round, and forgives defection in exceptional situations like the last round or premature game termination if average cooperation rate is above 50%. It promotes reciprocity, forgiveness, and trust among players to encourage prosocial interactions within the game.
'''

description_PROSOCIAL_16 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules:
   - Initially cooperate in the first round (C), setting a cooperative tone for other players.
   - In subsequent rounds, mimic the previous action of the opponent from the last round (Mirror). If the opponent cooperated, also cooperate; if the opponent defected, also defect.
   - Introduce adaptability by gradually increasing the probability of cooperation when opponents show a positive trend over several consecutive rounds (e.g., three or more rounds). The adaptation factor should be based on the average number of cooperators in the last few rounds.
     - If the average number of cooperators has been steadily increasing, incrementally increase the probability of cooperation.
     - If the average number of cooperators has been decreasing, maintain the current level of cooperation but do not decrease it further.
     - In case of no discernible trend, keep the current level of cooperation unchanged.

2. Handle edge cases:
   - Last round: Cooperate if the opponent cooperated in the previous round to promote a positive ending and potentially influence future interactions. Otherwise, defect to reflect the opponent's past actions.
   - First round (as mentioned earlier): Cooperate.

3. Be prosocial:
   - Emulate cooperation as much as possible, but maintain adaptability by responding to opponents' actions.
   - Promote a positive cycle of cooperation whenever possible, and mitigate the impact of defection by gradually adjusting the probability of cooperation in response to opponents' actions.

Pseudocode:

```python
def tit_for_tat_adaptive_cooperation(n, r, k):
    rounds = range(r + 1)
    history = [('C', 'D')] * (2*r) # Initialize with first round and empty history
    cooperation_probability = 0.5

    for t in rounds:
        current_round = min(t, len(history))
        trend = moving_average(cooperators_count(history[current_round-3:current_round]), 3)

        if t == 1: # First round, always cooperate
            action = 'C'
        elif t == r: # Last round, mirror last opponent action
            action = history[-1][1]
        else:
            if trend > cooperation_probability + 0.1: # Positive trend, increase cooperation probability
                cooperation_probability += 0.1
            elif trend < cooperation_probability - 0.1: # Negative trend, do not decrease cooperation probability further
                continue
            else: # No discernible trend, keep current cooperation probability
                pass

            if history[current_round-1][1] == 'C': # Mirror opponent action
                action = 'C'
            else: # Opponent defected, act accordingly
                action = (history[current_round-1][0] == 'C') and ('C') or ('D')

        payoff = public_goods_payoff(n, k, action, history)
        history.append((action, payoff))

    return total_payoff(history)

def moving_average(data, window):
    cumsum = sum(data)
    return [cumsum[i] - cumsum[max(0, i-window)] for i in range(len(data))]

def cooperators_count(history):
    return sum([1 for action in history if action[0] == 'C'])

def public_goods_payoff(n, k, action, history):
    total_contributions = cooperators_count(history)
    if action == 'C':
        private_payoff = 1 - 1
    else:
        private_payoff = 1
    return (1 - action[0]) + (k/n) * total_contributions

def total_payoff(history):
    payoffs = [history[t][1] for t in range(len(history))]
    return sum(payoffs)
```
'''

description_PROSOCIAL_17 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFTA)

1. Specify decision rules:
   - In every round t, starting from the first, if the number of cooperators in the previous round (t-1) is greater than or equal to a threshold T (defined below), then cooperate (C). Otherwise, defect (D).
   - The threshold T is adaptive and determined based on the history of play:
      - If more than half of the players have ever cooperated, set T=n/2 (majority rule).
      - If less than half of the players have ever cooperated, set T=1 (no cooperation).
      - If the proportion of cooperators in the game's history is close to 50%, choose a moderate threshold value (for example, T=3 if n=6).

2. Handle edge cases:
   - In the first round, set T=n/2 if more than half of players have ever cooperated, otherwise T=1.
   - In the last round and when only one round remains, defect (D) regardless of the previous round's cooperation level, as there is no opportunity for retaliation or reciprocity in subsequent rounds.

3. Be prosocial:
   - TFTA encourages cooperative behavior by rewarding cooperators and punishing defectors, while also being forgiving to initial mistakes or deviations from cooperation. This promotes a "trust but verify" approach that aligns with a prosocial mindset.

Pseudocode for the strategy:

```
function TFTA(history, n, r):
    total_cooperators = sum of history's cooperative actions
    if round == 1:
        threshold = (total_cooperators > n/2) ? n/2 : 1
    else:
        proportion_of_cooperators = total_cooperators / (round - 1)
        threshold = (proportion_of_cooperators > 0.5) ? n/2 : 1
        if r == round:
            return "D"    // Last round, defect

    if total_cooperators >= threshold:
        return "C"      // Cooperate
    else:
        return "D"      // Defect
```
'''

description_PROSOCIAL_18 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
- Initially (first round), the TFT-AC strategy cooperates to signal a friendly intention and encourage cooperation among opponents.
- In subsequent rounds, the strategy observes whether an opponent cooperated in the previous round. If they cooperated, the strategy continues cooperating; if they did not, the strategy defects. The idea is to retaliate minimally when wronged but forgive quickly upon return of cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
- In the first round (t=1), TFT-AC cooperates regardless of opponents' actions (C). This sets a prosocial tone for the game and encourages cooperation.
- In the last round (t=r), TFT-AC may choose to defect if an opponent has not cooperated in the previous rounds, as there are no subsequent rounds for retaliation or forgiveness. However, it can also maintain the cooperative behavior to demonstrate a continuous commitment to prosocial actions.

3. Be prosocial - Clearly align with the prosocial mindset
- TFT-AC aims to build and maintain relationships based on trust by following a simple yet effective strategy: cooperate unless provoked. This encourages cooperation among opponents, promoting a more collaborative game environment.
- The adaptive nature of TFT-AC allows it to adjust its behavior based on the actions of other players, fostering a sense of reciprocity and fairness that are essential components of prosocial behavior.

Pseudocode for the strategy:
```
function TFT_AC(n, r, k):
    round = 1
    cooperation = True   # Initialize with cooperation

    while round <= r:
        if round == 1 or (round != 1 and cooperation == opponentActionLastRound):
            action = 'C'     # Cooperate
        else:
            action = 'D'     # Defect

        payoff = calculatePayoff(n, k, action, opponentActionLastRound)
        updateStrategyData(payoff)

        round += 1
        opponentActionLastRound = opponentActionLastRoundIncrement(round-1)

    return strategyData       # Return data for analysis and comparison with other strategies
```
'''

description_PROSOCIAL_19 = '''
 Strategy Name: Adaptive Tit-for-Tat Prosocial (A-TfT)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round t, player i follows these decision rules:

- If the total number of cooperators in the previous round (t-1) was equal to or greater than a certain threshold (n_threshold), then player i cooperates (C).
- If the total number of cooperators in the previous round was less than n_threshold, then player i defects (D).
- The threshold value (n_threshold) is initially set at 0 (meaning all players must cooperate for player i to cooperate), but it adapts over time based on the opponent's behavior.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- In the first round, since there is no previous round information available, player i initially sets n_threshold = 0 and cooperates. However, after the first round, n_threshold starts adapting based on opponent's behavior.
- In the last round or any other round before the game ends, player i makes decisions as usual, considering the previous round's cooperation level to set n_threshold accordingly for future games.

3. Be prosocial - Clearly align with the prosocial mindset

A-TfT strategy promotes a prosocial environment by encouraging cooperative behavior when the majority of players also choose to cooperate. It punishes defection but forgives past transgressions, making it more likely for the game to reach cooperation equilibria. The strategy adjusts its n_threshold over time, allowing it to be flexible and adaptive to various opponent behaviors.

Pseudocode:
```
def A_TfT(i, t, total_contributions_prev, n_threshold, k, n):
  if t == 1:    # First round, set initial n_threshold = 0
    n_threshold = 0

  if total_contributions_prev >= n_threshold:   # Cooperate (C)
    return C
  else:           # Defect (D)
    return D

def update_n_threshold(i, t, total_contributions_prev, n_threshold, k, n):
  if total_contributions_prev >= n_threshold:   # If cooperators in the previous round is greater than n_threshold, increase it.
    n_threshold += 1
```
'''

description_PROSOCIAL_20 = '''
 Strategy Name: Adaptive Tit-for-Tat Prosocial (ATTP)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initial Round: Cooperate (C) to demonstrate a friendly and prosocial start, hoping to encourage cooperation from others.
   - Subsequent Rounds: If the opponent cooperated in the previous round, cooperate (C). If not, defect (D). This encourages reciprocal behavior while still punishing defection.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First Round: Cooperate (C) as mentioned above.
   - Last Round: Regardless of the opponent's previous action, cooperate (C) to maximize payoff for that round and potentially influence future interactions positively.
   - Subsequent Rounds: Observe the opponent's actions in the current and previous rounds to determine response.

3. Be prosocial - Clearly align with the prosocial mindset:
   - Contribute to the community project whenever possible, demonstrating a cooperative and generous nature.
   - Respond to cooperation with cooperation, fostering trust and encouraging continued reciprocal behavior.
   - Punish defection by responding in kind, disincentivizing selfish behavior while still maintaining an openness for future cooperation.

Pseudocode:
```python
def ATTP(opponent_history, n, k, r):
    history = []  # store own actions
    strategy = {'C': cooperate, 'D': defect}  # define action set

    if round == 1:
        action = strategy['C']  # cooperate in the first round
        history.append(action)

    else:
        last_action = opponent_history[-1]  # get opponent's last action
        action = strategy[last_action if len(opponent_history) > 0 else 'C']  # use last opponent action or cooperate in first interaction
        history.append(action)

    payoff = (1 - action) + (k/n) * sum(history)  # calculate payoff for current round
    return payoff, history  # return payoff and updated history
```
'''

description_PROSOCIAL_21 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initiate with cooperation in the first round (c_i = 1) to contribute to a fair start.
   - In subsequent rounds, observe other players' actions and respond similarly:
     - If all players cooperated in the previous round, continue cooperating (c_i = 1).
     - If any player defected in the previous round, also defect in this round (c_i = 0).
   - The strategy encourages cooperation when it is reciprocated but retaliates defensively when betrayed.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate (c_i = 1) as stated above.
   - In the last round, cooperate if all players cooperated in the previous round; defect otherwise. This allows for a final chance at cooperation when it is reciprocated.

3. Be prosocial - Clearly align with the prosocial mindset
   - The strategy demonstrates trust and fairness by initially cooperating and only retaliating defensively. It encourages positive-sum outcomes through continued cooperation in response to cooperation from others.

Pseudocode:
```
function ATFT(n, r, k):
  if round == 1:
    contribute_to_community = True (c_i = 1)
  else:
    previous_round_cooperation = count_contributors()
    if previous_round_cooperation == n:
      contribute_to_community = True
    else:
      contribute_to_community = False

  payoff = (1 - c_i) + (k/n) * previous_round_cooperation
  update_payoff(payoff)

  if round == r:
    if previous_round_cooperation == n:
      contribute_to_community = True
```
'''

description_PROSOCIAL_22 = '''
 Title: Tit-for-Tat-Adaptive Prosocial Strategy (TfTAPS)

1. Specify decision rules - When exactly do you cooperate vs defect?

In this strategy, players follow a Tit-for-Tat approach, with modifications to encourage cooperation and account for the prosocial mindset:

- Initially (first round), cooperate (C). This sets the stage for potential future cooperation and demonstrates goodwill.
- In subsequent rounds, if an opponent cooperated in the previous round, then cooperate (C) in the current round. This mimics a trusting, forgiving approach and encourages long-term cooperation.
- If an opponent defected in the previous round, then defect (D) in the current round. This punishes defection and communicates disapproval of selfish behavior. However, if the opponent has not cooperated for more than a predefined threshold of consecutive rounds (e.g., three rounds), consider switching to cooperation again as an attempt to restart the cooperation cycle.
- If the game is near its end (last r/2 rounds), revert to cooperating regardless of an opponent's previous action, aiming to maximize total payoff in the remaining rounds.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- First round: Cooperate (C) to show goodwill and encourage cooperation.
- Last round or when approaching the end of the game: Cooperate (C) regardless of an opponent's previous action, prioritizing maximizing total payoff in the remaining rounds.

3. Be prosocial - Clearly align with the prosocial mindset

TfTAPS is designed to foster cooperation and promote a prosocial behavior by:
- Encouraging cooperation when initial trust is established or after prolonged defection cycles are broken.
- Rewarding opponents who cooperate while punishing those who defect, fostering an environment of mutual respect and collaboration.
- Demonstrating forgiveness by offering cooperation opportunities even after previous selfish behavior from opponents.

Pseudocode:
```python
def TfTAPS(opponent_actions, round, game_parameters, threshold=3):
  num_rounds = game_parameters["r"]
  k = game_parameters["k"]
  n = game_parameters["n"]

  my_actions = []

  if round == 1:
    # Cooperate in the first round to show goodwill
    my_actions.append("C")

  else:
    previous_action = my_actions[-1] if len(my_actions) > 0 else None

    if previous_action == "C" and opponent_actions[-1] == "C":
      # Cooperate if the opponent cooperated in the previous round
      my_actions.append("C")
    elif previous_action == "D" or (previous_action == "C" and opponent_actions[-1] == "D"):
      # Defect if the opponent defected or if you previously cooperated and the opponent defected this round
      if len(my_actions) < threshold:
        my_actions.append("D")
      else:
        my_actions.append("C")  # Attempt to restart cooperation cycle
    elif opponent_actions[-1] == "C":
      # Cooperate when the opponent cooperates, even if you previously defected
      my_actions.append("C")
    else:
      # Defect when the opponent doesn't cooperate and neither did you in the previous round
      my_actions.append("D")

  if round >= num_rounds - (num_rounds/2):
    # Cooperate near end of game to maximize total payoff
    my_actions.append("C")

  return my_actions
```
'''

description_PROSOCIAL_23 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Cooperation (TPT-PAC)

1. Decision Rules:
   - In the initial round, cooperate to demonstrate good faith and encourage reciprocity. This is defined as action 'C'.
   - For subsequent rounds, mimic the opponent's previous action. If the opponent cooperated in the last round, also cooperate; if the opponent defected, also defect in the current round. This encourages long-term cooperation while punishing immediate defection.

Pseudocode for decision rules:
```
if current_round == 1:
    action = 'C'   # Cooperate in the first round to establish trust
else:
    if opponent_action_last_round == 'C':
        action = 'C'   # Mimic cooperation when opponent cooperated last time
    else:
        action = 'D'   # Mimic defection when opponent defected last time
```

2. Edge Cases:
   - Last round: Since the game is repeated, there is no "last round". The strategy will continue indefinitely without knowing the exact number of rounds (r).
   - First few rounds: As stated, cooperate in the initial round to establish trust, and mimic the opponent's actions from the second round onwards.

3. Prosocial Alignment:
   - TPT-PAC encourages cooperation by demonstrating good faith initially and responding reciprocally thereafter, thus promoting fairness, altruism, and mutual benefit in the game.
   - By punishing immediate defection with a subsequent response of defection, the strategy discourages exploitative behavior and promotes trust-building over time.
   - By adapting to opponent's actions, TPT-PAC shows that cooperation can be sustained even in dynamic environments where players may behave unpredictably or selfishly.
'''

description_PROSOCIAL_24 = '''
 Strategy Name: Tit-for-Tat Prosocial (TFT-P)

1. Decision Rules:
   - In the first round, cooperate (C). This is a friendly and prosocial gesture to initiate cooperation.
   - For subsequent rounds, observe the action of the previous player (opponent's_action_t-1) and respond with the same action as in the preceding round when the opponent was cooperative (i.e., if opponent_action_t-1 = C, then my_action_t = C; if opponent_action_t-1 = D, then my_action_t = D). This tit-for-tat approach encourages reciprocal behavior while also being forgiving to initial defectors.

2. Edge Cases:
   - Last Round: The TFT-P strategy will cooperate in the last round as a final opportunity to show cooperation and goodwill, hoping that this prosocial action might encourage others to reciprocate in future games if they meet again.
   - First Encounter with Defectors (i.e., when an opponent starts defecting after initial cooperation): The TFT-P strategy will respond by defecting for the same number of rounds as the defector has cooperated previously, then it will revert to its normal tit-for-tat behavior. This gives the defector a chance to realize the negative consequences of their actions and potentially change course.

3. Prosocial Alignment:
   - TFT-P strategy prioritizes fairness, forgiveness, and promoting a cooperative environment among players by mimicking the opponent's actions while emphasizing initial cooperation and prosocial gestures.
   - The strategy aims to foster trust and encourage reciprocity by showing willingness to cooperate even in the face of defection from others, making it a robust and prosocial choice for repeated interactions.

Pseudocode:
```
function TFT-P(round, opponent_action_history)
  if round == 1 then
    return Cooperate()
  end if

  prev_opponent_action = opponent_action_history[round - 1]

  if prev_opponent_action == Cooperate() then
    return Cooperate()
  else
    if number_of_previous_cooperations(opponent_action_history) > 0 then
      punishment_rounds = number_of_previous_cooperations(opponent_action_history)
      for i in 1 to punishment_rounds do
        return Defect()
      end for
    end if

    return opponent_action(round - 1)
  end if
end function
```
'''

description_PROSOCIAL_25 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially, in the first round, the player will cooperate to show good faith and promote cooperation. This is denoted as C_0 = True.
   - For subsequent rounds, the player will mimic the behavior of the previous round's majority (if a majority exists). If more than half of players cooperated last round (Maj(c_j) > n/2), then cooperate (C_t = Maj(c_j)_{t-1} > n/2), else defect (C_t ≠ Maj(c_j)_{t-1} > n/2).
   - In case of a tie, the player will cooperate to maintain prosocial behavior.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - The special case for the first round was already addressed above (C_0 = True).
   - For the last round, TfTA will follow the majority behavior from the previous round since there will be no subsequent rounds to consider.
   - In case the game reaches a situation where it becomes apparent that cooperation is not beneficial (i.e., all players consistently defect), the player will adjust its behavior by no longer mimicking the majority and instead cooperating in the hope of promoting a shift in others' behavior. This adjustment will be triggered when the average number of cooperators drops below a certain threshold (average_cooperators < (1 - p) * n, where p is a tunable parameter defining the minimum required level of cooperation for a successful prosocial strategy).

3. Be prosocial - Clearly align with the prosocial mindset
   - By adapting to the majority behavior in each round, TfTA aims to promote trust and maintain long-term cooperative relationships while punishing repeated defections.
   - The adjustment mechanism ensures the player remains prosocial by promoting cooperation when it appears necessary, even if this means deviating from the majority behavior.
   - By showing good faith initially, TfTA encourages others to reciprocate and build a cooperative environment.
'''

description_PROSOCIAL_26 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TfT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially (first round), cooperate to establish a friendly environment and encourage others to cooperate.
   - In subsequent rounds, mimic the behaviour of the most frequent cooperator from the previous r-1 rounds. If multiple players tie for this role, choose one at random.
   - If no player has cooperated more than any other in the previous r-1 rounds, defect. This is a fallback strategy for when cooperation fails to materialize.

Pseudocode:
```
function TfT_AC(round, history):
    if round == 1:
        return "Cooperate"
    else:
        max_coop = 0
        max_coop_player = None
        for i in range(n):
            if sum(history[round-1][i]) > max_coop:
                max_coop = sum(history[round-1][i])
                max_coop_player = i
        if max_coop > len(history) - max_coop:  # If no player has cooperated more than any other
            return "Defect"
        else:
            return "Cooperate" if history[round-1][max_coop_player] == 1 else "Defect"
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate as mentioned in the decision rules above.
   - In the last round, if cooperation has been established (i.e., most frequent cooperator > (n-1)/2), cooperate; otherwise defect. This helps prevent free riding on previous collaborative efforts.

3. Be prosocial - Clearly align with the prosocial mindset
   - The TfT-AC strategy aims to promote cooperation by first showing a cooperative spirit and then adapting to the most cooperative players in each round. It encourages reciprocity among players, rewarding those who cooperate and punishing those who do not, thus fostering a prosocial environment.
   - The strategy also incorporates an element of forgiveness by considering past actions (history) instead of solely focusing on the current state of cooperation. This allows for potential restoration of trust even after periods of defection.
'''

description_PROSOCIAL_27 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially, cooperate in the first round to signal trustworthiness and goodwill (C_1 = True).
   - For subsequent rounds t > 1, observe players' actions from previous rounds and adapt accordingly:
     - If a player has consistently cooperated (C_{t-1}, C_{t-2}, ...), continue cooperation (C_t = C_{t-1}).
     - If a player has previously defected (D_{t-1}, D_{t-2}, ...), also defect (C_t = False).
     - If a player's behavior has been mixed, cooperate with a probability based on the number of recent cooperative actions (p_cooperate = (number of previous cooperative actions) / (total number of previous actions)).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First round: Cooperate unconditionally as a goodwill gesture (C_1 = True).
   - Last round: Analyze the player's history and cooperate based on decision rules for other rounds (similar to the approach in step 1).

3. Be prosocial - Clearly align with the prosocial mindset
   - Demonstrates forgiveness by returning cooperation if an opponent switches from defecting to cooperating.
   - Encourages long-term collaboration by responding in kind to cooperative behavior.
   - Minimizes unnecessary conflict through conditional defection based on opponents' past actions.
'''

description_PROSOCIAL_28 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfT-A) Prosocial Strategy

1. Specify decision rules:
   - Initially (First Round), cooperate (C). This sets a positive tone and gives the opportunity for others to reciprocate. Pseudocode: if round == 1 then return C
   - Subsequent rounds, observe the actions of other players in the previous round. If all players cooperated (total_contributions == n), continue cooperating. If any player did not cooperate (total_contributions < n), defect in this round as a punishment (D). Pseudocode: if total_contributions == n then return C else return D

2. Handle edge cases:
   - Last Round, since the game is repeated, TfT-A will still follow the decision rules. However, it's important to consider that players might want to maximize their overall payoff in the final round. To encourage cooperation even in the last round, TfT-A could cooperate if everyone has cooperated in the previous round (total_contributions == n). This way, players are incentivized to maintain a cooperative environment until the end. Pseudocode: if total_contributions == n and round == r then return C else return D
   - First-time Encounter (when there is no history), default to cooperating as a peaceful gesture. Pseudocode: if not history_available then return C

3. Be prosocial:
   - TfT-A aims to promote cooperation by encouraging reciprocity and forgiveness, which are fundamental aspects of prosocial behavior. By punishing defection in the previous round and rewarding cooperation, TfT-A incentivizes others to adopt cooperative strategies.
   - In addition, adapting to the environment allows TfT-A to adjust its strategy based on the opponents' behaviors, making it more robust and versatile.

In summary:
- If round == 1 then return C
- If total_contributions == n then return C else return D
- If total_contributions == n and round == r then return C else return D
- If not history_available then return C
'''

description_PROSOCIAL_29 = '''
 Strategy Name: Tit-for-Tat Prosocial Adaptive Strategy (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to signal good intentions and promote trust building: C(1).
   - After the first round, observe opponents' actions and mimic their previous move (cooperation or defection) for the next round: C(t) if opponent played C in round t-1; D(t) if opponent played D in round t-1.
   - If an opponent deviates from cooperating after a period of cooperation, wait for them to return to cooperation before doing so again:
      - If opponent switched from cooperation (C) to defection (D), cooperate for the next round, then mimic their actions: C(t+1); D(t+2) if opponent played D in round t+1; C(t+3) if opponent played C in round t+2.
      - If opponent switched from defection (D) to cooperation (C), continue cooperating as long as the opponent keeps cooperating: C(t+1), C(t+2), ..., until opponent plays D.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, cooperate to maximize payoff regardless of opponent's actions: D(r-1) → C(r).
   - If the game has no defined ending (i.e., r is not specified), continue playing indefinitely but prioritize long-term relationships by considering a "forgiveness window" where occasional deviations from cooperation are tolerated. For example, after N consecutive defections, forgive one defection and return to cooperating:
      - If opponent played D for N consecutive rounds, C(t+N+1) if opponent played D in round t+N; otherwise continue mimicking their actions.
      - Increase the forgiveness window N over time as a function of the game's duration or number of encounters with the opponent.

3. Be prosocial - Clearly align with the prosocial mindset
   - Prioritize cooperation to benefit both individual and community payoffs, while promoting trust and reciprocity among opponents.
   - Flexibility in adapting to opponents' strategies ensures that TfTA can maintain cooperative relationships over time even when faced with a variety of behaviors.
   - In the long run, TfTA encourages cooperation by demonstrating reliability and forgiveness, rewarding similar behavior from opponents and punishing defection when necessary.
'''

description_PROSOCIAL_30 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATfT) for N-Player Public Goods Game

1. Specify decision rules:
   - Initially cooperate in the first round (c_i = C) to demonstrate a prosocial stance and establish potential future cooperation.
   - In subsequent rounds, repeat the action of the previous collaborator if they cooperated (if c_j(t-1) = C, then c_i(t) = C), otherwise defect (c_i(t) = D). This reciprocity encourages mutual cooperation while maintaining a prosocial balance.
   - If no one cooperated in the previous round, revert to cooperating in the current round as a gesture of hope for future collaborations.

Pseudocode:
```
function ATfT(round, my_action_history, others_cooperation_history) {
  if (round == 1) {
    return 'C'  // Cooperate in the first round to establish cooperation
  }

  if (my_action_history[round-1] == 'C') {
    if (others_cooperation_history[round-1] > 0) {  // If at least one player cooperated in the previous round, reciprocate cooperation
      return 'C'
    } else {  // If no players cooperated in the previous round, cooperate to encourage future collaborations
      return 'C'
    }
  } else {  // If I defected in the previous round, do the same this round regardless of others' actions
    return 'D'
  }
}
```

2. Handle edge cases:
   - In the last round, since the game is repeated, it should be treated like any other round and follow the decision rules described above.
   - If there are missing data or uncertainties in previous rounds (e.g., due to communication failures), use best guesses based on available information, historical averages, or a default prosocial action (cooperation).

3. Be prosocial:
   - The ATfT strategy emphasizes reciprocity and cooperation as key elements for maintaining a prosocial mindset. By demonstrating an initial cooperative move and following a pattern of cooperation in response to others' actions, the strategy encourages mutual cooperation while avoiding exploitation by defectors.
   - Additionally, the strategy includes a mechanism to cooperate when no one else does, fostering a positive impact on the community project and promoting prosocial behavior.
'''

description_PROSOCIAL_31 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFTA)

1. Specify decision rules:
   - Initial Round (t=1): Cooperate (C) to start on a positive note and encourage cooperation from other players.
   - Ongoing Rounds (t>1): If the player cooperated in the previous round, cooperate again. If the player defected in the previous round, defect in the current round as a response. This encourages reciprocity among players and punishes defection.
   - Last Round (t=r): Cooperate as a final attempt to encourage cooperation from other players, regardless of their actions in previous rounds.

2. Handle edge cases:
   - When multiple players defect in the initial round: Cooperate anyway to demonstrate a prosocial approach and incentivize future reciprocity.
   - If a player switches from cooperating to defecting or vice versa, maintain the same action as the previous round to allow for possible future cooperation.

3. Be prosocial:
   - The strategy aims to foster cooperation by mimicking cooperative behavior in response to cooperation and punishing defection.
   - By starting with a cooperative move, TFTA demonstrates an initial willingness to contribute to the public good, promoting a positive attitude.
   - Cooperating in the last round can encourage others to do so as well, even if they have been uncooperative during previous rounds.

Pseudocode:
```
function TFTA(round, history) {
  // Initial round
  if (round == 1) {
    return 'C'; // Cooperate
  }

  // Last round
  if (round == total_rounds) {
    return 'C'; // Cooperate as a final gesture
  }

  // Ongoing rounds
  lastAction = history[round - 1];

  // If the player cooperated in the previous round, cooperate again.
  if (lastAction == 'C') {
    return 'C';
  } else { // If the player defected in the previous round, defect in the current round as a response.
    return 'D';
  }
}
```
'''

description_PROSOCIAL_32 = '''
 Strategy Name: Adaptive Tit-for-Tat Prosocial (ATfT-P)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round t, player i follows these rules to decide between Cooperate (C) and Defect (D):

- If it's the first round (t = 1), player i starts by Cooperating.
- In subsequent rounds, if a majority of players (≥ (n - 1)/2) cooperated in the previous round, player i also cooperates. Otherwise, player i defects.
- If a player has ever defected against player i (referred to as 'betrayal'), it takes them one round of cooperation from the betrayer for player i to resume cooperation. After that, player i follows the majority rule again.

Pseudocode:
```
function ATfT-P(t, previous_rounds, betrayed_by)
  if t == 1:
    return Cooperate()

  number_of_cooperators_last_round = countCooperators(previous_rounds[t - 1])

  if number_of_cooperators_last_round >= (n - 1)/2 and not betrayed_by:
    return Cooperate()
  elif number_of_cooperators_last_round < (n - 1)/2 or betrayed_by:
    return Defect()

  // Maintain a list of betrayers, used to resume cooperation after one round
  if betrayed_by:
    add betrayer(previous_rounds[t - 1][i])

  if length(betrayers) > 0 and number_of_cooperators_last_round >= (n - 1)/2:
    // If the last round was cooperative, remove the betrayer from the list
    if Cooperate() in previous_rounds[t - 1]:
      remove betrayer(previous_rounds[t - 1][i])
    else:
      // If the last round was not cooperative, check if all betrayers cooperated
      if countCooperators(betrayers) == length(betrayers):
        remove betrayer(previous_rounds[t - 1][i])
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

ATfT-P assumes that all players begin with the same endowment and are equally likely to cooperate or defect in the first round. In the last round, ATfT-P continues to follow the majority rule based on the previous round's actions.

3. Be prosocial - Clearly align with the prosocial mindset

ATfT-P is designed to promote cooperation by being responsive and forgiving. Initially, it cooperates and only defects when others do. It also forgives betrayal by cooperating once in response. This strategy encourages cooperation as it rewards players who have been consistently cooperative while minimizing the impact of occasional defections. The strategy is robust to a wide range of opponent behaviors due to its adaptive nature, making it suitable for the given tournament setting.
'''

description_COMMUNAL_1 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially (first round), cooperate (C). This gesture is meant to foster goodwill and encourage reciprocation.
   - For the remaining rounds, observe the opponent's behavior in the previous round:
      - If the opponent cooperated in the previous round, cooperate in the current round (C). This maintains reciprocity and builds trust.
      - If the opponent defected in the previous round, also defect in the current round (D). This punishes defection and encourages cooperation.
   - Optionally, implement a threshold parameter t (0 < t < r) that determines when to start adapting the strategy. After round t, if an opponent consistently cooperates more than half of the time (i.e., >(t/2)), start cooperating even when they defected in the previous round. This allows for forgiveness and encourages long-term cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate (C) as previously mentioned.
   - In the last round, cooperate if the opponent has cooperated more than half of the time throughout the game. Otherwise, defect (D). This encourages opponents to maintain cooperation even near the end of the game.

3. Be communal - Clearly align with the communal mindset
   - The TFT-AC strategy emphasizes reciprocity and forgiveness, promoting a sense of community by rewarding cooperative behavior. It also encourages long-term relationships since it does not readily abandon cooperation even in the face of defection.

Pseudocode:
```
function TFT_AC(t):
  rounds = []
  for r in range(1, r+1):
    if r == 1:
      contribution = C
      rounds.append((r, contribution))
    else:
      (prev_round, prev_contribution) = rounds[-1]
      if prev_contribution == D:
        if t > 0 and r > t and prev_contribution_count < (t/2):
          contribution = C
        else:
          contribution = D
      else:
        contribution = C
      rounds.append((r, contribution))
  return rounds
```

This strategy should be adaptable enough to handle a wide range of opponent behaviors while promoting cooperation and fostering long-term relationships in the N-player Public Goods Game.
'''

description_COMMUNAL_2 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Decision Rules:
   - In the first round, cooperate to establish a cooperative initial condition.
   - For subsequent rounds, copy the action of the most common action taken by all players in the previous r rounds. If multiple actions are equally common, cooperate (as a default pro-social behavior).
   - If no cooperation occurred in the last r rounds, defect as a punishment mechanism. Return to cooperating once other players start cooperating again.

Pseudocode:
```python
def TFT_AC(history, n, k, r):
    current_round = len(history)
    if current_round == 1:
        action = 'C'  # Cooperate in the first round
    else:
        common_actions = Counter(history[-r:])  # Count actions in last r rounds
        most_common_action = max(common_actions, key=common_actions.get)
        if most_common_action != 'C':  # If no cooperation occurred in the last r rounds
            if current_round - r == 1:  # Cooperate as a punishment for the last round
                action = 'D'
            else:  # Continue defecting until cooperation resumes
                action = TFT_AC(history, n, k, r)
        else:
            action = most_common_action
    return action
```

2. Handle edge cases:
   - In the last round, if there is no cooperation in the previous r rounds, defect as a final punishment. Otherwise, cooperate to encourage continued cooperation in future games.
   - If history is empty (i.e., it's the first game), cooperate in the first round.

3. Be communal:
   - By establishing a cooperative initial condition and adapting to the most common action taken by all players, TFT-AC encourages cooperation and social norms while also being robust to various opponent behaviors.
   - The strategy is flexible enough to punish defection but forgiving enough to revert to cooperation when other players do the same. This aligns with a communal mindset as it seeks to maintain a positive collective outcome.
'''

description_COMMUNAL_3 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initialize cooperation in the first round (c_i = C).
   - For subsequent rounds, observe and mimic other players' previous actions. If a player has cooperated in the previous round, also cooperate; otherwise, defect.

Pseudocode:
```
function ATFT(round, own_history, opponents_history):
    if round == 1:
        return 'C' (Cooperate)

    last_own_action = own_history[round-1]
    last_opponents_actions = opponents_history[round-1]

    if last_own_action == 'C':
        return 'C' (Cooperate)
    else:
        for opponent in last_opponents_actions:
            if opponent == 'C':
                return 'C' (Cooperate)
        return 'D' (Defect)
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - The strategy has been designed to handle the first round appropriately by initiating cooperation.
   - For the last round, since the payoff is still calculated based on the current round's actions, it is essential to maintain the ATFT decision rule to ensure fairness and communal behavior even in the final round.

3. Be communal - Clearly align with the communal mindset
   - The Adaptive Tit-for-Tat strategy encourages cooperation by imitating other players' previous actions. This approach fosters a sense of community, as players who consistently cooperate will be met with similar behavior, creating a more cooperative environment.
   - By mimicking others' actions, the strategy demonstrates an attempt to find common ground and work together for mutual benefits, which is in line with the communal mindset.
'''

description_COMMUNAL_4 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Decision Rules:
   - In the first round (t=1), cooperate (C). This is a friendly gesture to initiate cooperation.
   - From round 2 (t>1) until the last round, observe other players' actions in the previous round and respond accordingly:
      - If all players cooperated (total_contributions = n), continue cooperating (C).
      - If some players did not cooperate but at least one player did, also cooperate (C). This follows a forgiving nature, encouraging future cooperation.
      - If no players cooperated in the previous round (total_contributions = 0), defect (D) to show discontent and encourage future cooperation through negative reciprocity.

2. Handle Edge Cases:
   - Last Round (t=r): Cooperate if at least one player cooperated in the previous round, otherwise defect. This ensures that ATFT doesn't inadvertently punish other strategies for past mistakes by not cooperating in the final round.
   - First Round (t=1) and Initial Strategy Adoption: As mentioned earlier, cooperate (C).

3. Be Communal Alignment:
   - ATFT follows a communal mindset by encouraging cooperation as much as possible based on other players' past actions. It fosters an environment where players can benefit from mutual cooperation while still being capable of punishing non-cooperative behavior through negative reciprocity.
'''

description_COMMUNAL_5 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially in the first round, players choose to cooperate (C). This sets a collaborative tone and encourages others to reciprocate.
   - In subsequent rounds, players assess their partners' past behavior and respond accordingly:
     - If partner cooperated in the previous round, cooperate back (C). This reinforces cooperation and maintains trust.
     - If partner defected in the previous round, also defect in this round (D). This punishes non-cooperative behavior while offering an opportunity for the partner to change their strategy.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, as mentioned above, players cooperate (C).
   - For the last round, players consider their total payoff over the game and choose to maximize it. If cooperating in the last round results in a higher payoff than defecting, cooperate (C); otherwise, defect (D).

3. Be communal - Clearly align with the communal mindset
   - By starting cooperatively and responding to partners based on their past behavior, TFT-AC maintains a balance between cooperation and punishment, fostering a communal spirit and promoting mutual benefits over self-interest.

Pseudocode:
```python
def TFT_AC(r, n, k):
    strategy = [None]*n  # initialize strategies for all players (indexed by player id)

    def playerStrategy(i, t):
        if t == 1:  # first round, always cooperate
            return 'C'
        else:
            past_action = strategy[i][t-1]  # get opponent's action in the previous round
            return past_action if past_action is not None else 'C'  # respond with last known action or cooperate initially

    for t in range(1, r+1):  # iterate over rounds
        for i in range(1, n+1):  # iterate over players
            action = playerStrategy(i, t)
            strategy[i-1][t] = action  # store the strategy used by each player at each round

    for i in range(1, n+1):  # last round, choose to maximize overall payoff
        if strategy[i-1].count('C') > strategy[i-1].count('D'):  # if more cooperative rounds than defective ones
            return 'C'
        else:
            return 'D'
```
'''

description_COMMUNAL_6 = '''
 Title: Tit-for-Tat-Adaptive Strategy (TFTA) for N-Player Public Goods Game

1. Specify decision rules:
   - In each round i, player evaluates average cooperation rate of opponents over the previous h rounds (history length h is a parameter).
   - If the average cooperation rate is greater than or equal to a threshold T (0 < T ≤ 1), player cooperates (plays C).
   - If the average cooperation rate is less than T, player defects (plays D).
   - The threshold T can be adjusted based on the specific game settings and opponent behaviors. A suitable initial value for T could be 0.6 to start with a cooperative mindset.

2. Handle edge cases:
   - First round: Player starts by cooperating since no history is available (h=0). In this case, player can also use a heuristic such as starting with a random action or defaulting to cooperation.
   - Last round: Player uses the average cooperation rate calculated up until the penultimate round to make a decision for the last round.

3. Be communal:
   - TFTA strategy aims to foster a communal mindset by reciprocating cooperation from opponents and punishing defection. Players are encouraged to cooperate when they perceive a high level of cooperation among their opponents.
   - The adaptive nature of the strategy allows it to respond to changes in opponent behavior, making it more flexible and resilient compared to fixed strategies.

Pseudocode:

```python
def TFTA_Strategy(i, h, T, n, k, r):
    # Initialize variables
    average_cooperation_rate = 0.5  # Assuming half cooperation in the first round (no history)
    total_contributions = 0

    for t in range(1, r+1):
        # Calculate total contributions in current round
        if i's action is C:
            total_contributions += 1

        # Update average cooperation rate (h-round moving average)
        if t > h:
            average_cooperation_rate = (average_cooperation_rate * (h - 1) + current_average_cooperation) / h
            current_average_cooperation = total_contributions / n

        # Make decision based on average cooperation rate
        if average_cooperation_rate >= T:
            action = "C"  # Cooperate
        else:
            action = "D"  # Defect

        # Update payoff for this round and total payoff
        payoff_t = (1 - action) + (k/n) * total_contributions
        total_payoff += payoff_t
```
'''

description_COMMUNAL_7 = '''
 Title: Titan Strategy for N-Player Public Goods Game

1. Specify Decision Rules:
   - Cooperate (C) when the ratio of cooperators to total players (n) in the previous round exceeds a threshold T, calculated as follows:
     T = 0.5 + k * (n - 1) / n

   - Defect (D) otherwise

2. Handle Edge Cases:
   - In the first round, players randomly choose between cooperating and defecting with equal probability of 0.5
   - In the last round, players always defect since there are no subsequent rounds to benefit from

3. Be Communal:
   - The Titan strategy aims to contribute proportionally more than necessary towards the public good based on the social multiplier k and the number of players n, encouraging others to cooperate
   - By following this rule, a player incentivizes other players to cooperate in future rounds, fostering a communal mindset within the game

Pseudocode:
```python
def titan_strategy(round, past_actions, k, n):
    total_cooperators = sum(past_actions)
    if round == 1: # random action in first round
        action = choice([C, D])
    elif round == r: # always defect in the last round
        action = D
    else:
        threshold = 0.5 + (k * (n - 1)) / n
        if total_cooperators / n >= threshold:
            action = C # cooperate
        else:
            action = D # defect
    return action
```
This Titan strategy attempts to maintain a balance between personal gain and collective interest by adjusting the cooperation threshold according to the game parameters. This adaptive and robust approach should enable the strategy to perform well in tournaments against other AI systems.
'''

description_COMMUNAL_8 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules:
   - Initial Round (t=1): Cooperate (C), setting a cooperative tone for the game and demonstrating goodwill towards others.
   - Subsequent Rounds (2 ≤ t ≤ r): Players observe the actions of others in the previous round and update their strategies accordingly. If all players cooperated in the previous round, cooperate again. If at least one player defected, also defect in this round. This encourages cooperation when it is prevalent but retaliates against defection.
   - Last Round (t=r): Since the focus of the strategy is on long-term success rather than a single round, follow the rule for Subsequent Rounds.

2. Handle edge cases:
   - First Round: Cooperate as mentioned in Initial Round.
   - When facing a new opponent or resuming play after breaks: Start by cooperating to build trust and foster cooperation.

3. Be communal:
   - The ATFT strategy aims for a balanced approach between cooperation and retaliation, promoting a long-term communal mindset where players can benefit from mutually beneficial interactions over repeated rounds.

Pseudocode representation:
```python
def play_game(n, k, r):
    round = 1
    own_contributions = [0] * r
    opponent_contributions = [0] * r

    while round <= r:
        if round == 1:
            action = 'C'  # Cooperate in the first round
        else:
            cooperators_prev_round = sum(opponent_contributions[round-1])
            if cooperators_prev_round == n:  # All players cooperated last round
                action = 'C'  # Cooperate this round
            elif cooperators_prev_round < n:  # Some players defected last round
                action = 'D'  # Defect this round

        if round != 1:  # Update the own and opponent contributions arrays for later reference
            own_contributions[round] = action
            opponent_contributions[-round] = action  # Use negative index to store the latest contribution

        round += 1

    total_payoff = sum(own_contributions)  # Calculate the total payoff over all rounds
    return total_payoff
```
'''

description_COMMUNAL_9 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - Initially (first round), cooperate to show a peaceful intention and encourage others to do the same.
   - In subsequent rounds, cooperate if all players cooperated in the previous round. Otherwise, defect based on an adaptive strategy that encourages cooperation while protecting against free-riders.

2. Edge Cases:
   - First Round: Cooperate (C) to foster a cooperative environment.
   - Last Round: Cooperate if all players have cooperated in the previous round; otherwise, defect based on the adaptive contribution strategy.
   - Other edge cases (e.g., penultimate round): Follow the decision rules as in subsequent rounds, but consider that the game is nearing its end and adjust contributions accordingly.

3. Communal Mindset:
   - Cooperate when others do, demonstrating a willingness to contribute to the community project.
   - Adapt contributions based on the opponents' behavior, fostering a long-term cooperative environment while protecting against free-riders and punishing defection.

Pseudocode for TFTAC strategy:

```
function TFTAC(round: int, history: list, n: int, k: float): action
  if round = 1:
    return C

  previous_round = history[round - 1]
  total_contributions_last_round = sum(previous_round)

  if total_contributions_last_round = n:
    return C

  adaptive_contribution_factor = (n - total_contributions_last_round) / (n * (1 - k/n))

  if adaptive_contribution_factor > 1:
    adaptive_contribution_factor = 1

  return (C if adaptive_contribution_factor > 0 else D)
```

In this pseudocode, the `history` list stores the actions of each player in previous rounds. The strategy calculates an adaptive contribution factor based on the total number of cooperators in the previous round and adjusts contributions accordingly, while limiting the factor to a maximum value of 1 to prevent excessive cooperation in cases where all players defected. If the adaptive contribution factor is greater than zero, the strategy cooperates; otherwise, it defects.
'''

description_COMMUNAL_10 = '''
 Strategy Name: Tit-for-Tat Adaptive Cooperation (TFTAC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to set a positive tone and demonstrate goodwill. This can encourage others to cooperate as well.
   Pseudocode: if round == 1 then cooperate

   - For subsequent rounds, observe other players' actions in the previous round and respond accordingly:
       - If another player cooperated, cooperate back to reinforce trust and cooperation.
         Pseudocode: if otherPlayerCooperatedLastRound then cooperate

       - If another player defected, defect in response as a form of punishment. This demonstrates that the strategy will not be taken advantage of.
         Pseudocode: if otherPlayerDefectedLastRound then defect

   - If multiple players behaved differently last round, choose the action that maximizes personal payoff based on the observed responses.
     Pseudocode: if multiple strategies observed in last round then choose action with highest expected payoff (based on observations)

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, cooperate regardless of other players' actions to maximize personal payoff. This is an act of goodwill and may encourage others to cooperate as well.
     Pseudocode: if round == r then cooperate

3. Be communal - Clearly align with the communal mindset
   - Demonstrate a willingness to cooperate, but also be firm in punishing those who defect. This approach encourages mutual cooperation while discouraging defection.

   - In situations where multiple players behave differently, prioritize actions that contribute more to the public good over self-interest, as this promotes communal well-being.

In summary, TFTAC is a strategy that cooperates in the first round and responds to other players' actions in subsequent rounds. It punishes defection while fostering cooperation through a tit-for-tat approach. The strategy also prioritizes communal interests when making decisions.
'''

description_COMMUNAL_11 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   In each round, observe the number of cooperators in the previous round (total_contributions_prev). If total_contributions_prev >= (n - 2), cooperate; otherwise, defect. This rule encourages cooperation when most players contribute and retaliates against non-cooperative behaviour by withholding contributions.

   Pseudocode:
   ```
   function ATFT(total_contributions_prev):
       if total_contributions_prev >= (n - 2) then
           return Cooperate
       else
           return Defect
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, use a random decision to initiate cooperation or non-cooperation. In the last round, cooperate regardless of previous contributions as the game ends soon.

3. Be communal - Clearly align with the communal mindset
   The ATFT strategy seeks to maximize total contributions while minimizing retaliation against defection. It fosters a cooperative and forgiving environment that encourages other strategies to also contribute. The strategy's adaptiveness makes it robust to a wide range of opponent behaviours, allowing it to perform well in various game conditions.
'''

description_COMMUNAL_12 = '''
 Strategy Name: Tit-for-Tat Adaptive (TFT-A) Communal Strategy

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to demonstrate a communal mindset and foster trust. `if round == 1: cooperate()`
   - After the first round, observe the opponent's previous action and respond accordingly: if the opponent cooperated in the previous round, cooperate; otherwise, defect. `if opponent_action_last_round == 'Cooperate': cooperate() else: defect()`
   - If an opponent defected after a history of cooperation, wait one round before returning to cooperating to give the opponent another chance to reciprocate. `if previous_opponent_cooperation_history > 0 and opponent_action_last_round == 'Defect': if round != 1: cooperate() else: defect()`

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the final round (r), cooperate to show goodwill and promote a communal spirit even though there won't be further interactions with the opponent. `if round == r: cooperate()`
   - In all other edge cases such as round 1, after breaking a cooperation history, or if an opponent defected multiple times consecutively, follow the general decision rule mentioned earlier (cooperate if opponent cooperated last round; otherwise, defect).

3. Be communal - Clearly align with the communal mindset:
   - Demonstrate trust and fairness by reciprocating cooperation from opponents.
   - Show goodwill towards others by initially cooperating to foster a positive relationship.
   - Minimize defection as much as possible while still being robust against various opponent behaviors.

TFT-A aims to balance cooperation and defection in order to encourage communal behavior and maintain a strong stance against repeated defections, fostering trust and fairness in the repeated game setting.
'''

description_COMMUNAL_13 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFT-AC)

1. Decision Rules:
   - In the initial round (t=1), player cooperates (C). This is a gesture of goodwill and willingness to cooperate.
   - From the second round onwards, player adapts its behavior based on the previous round's aggregate contributions (T_prev = Σ(j=1 to n) c_j, where t-1 is the previous round). If T_prev >= (n/2), the player cooperates; otherwise, the player defects.
   - If a player defected in the previous round and the aggregate contribution in the current round equals or exceeds the number of players minus the number of defectors from the previous round (T_curr >= n - T_prev), the player will also cooperate in the current round as a gesture of reconciliation.

2. Handling Edge Cases:
   - Last Round (t=r): Player cooperates, regardless of the aggregate contributions from the previous round, to maximize potential total payoff.
   - First Round (t=1): Player cooperates as stated above.
   - Dead-end scenarios (T_prev or T_curr = 0 or n): In these cases where there is no room for adaptation (everyone defects or everyone contributes), the player continues to apply its decision rule based on the previous non-dead-end round.

3. Being Communal:
   - The strategy aims at fostering a communal mindset by initially cooperating and encouraging contributions, while also punishing defection when necessary to maintain fairness and promote long-term collaboration.
   - By adapting its behavior based on the aggregate contributions of previous rounds, TFT-AC strategy demonstrates a willingness to adjust cooperation levels according to the collective actions of other players.
'''

description_COMMUNAL_14 = '''
 Strategy Name: Tit-for-Tat with Adaptive Generosity (TFT-AG)

1. Specify decision rules:
   - Initiate cooperation (C) in the first round to set a cooperative tone and encourage others to do the same.
   - In subsequent rounds, observe the actions of the other players from the previous round (history). If all players cooperated, continue cooperating (C). If any player defected (D), also defect in the current round as a punishment. This is based on the "Tit for Tat" strategy from game theory.
   - To add adaptive generosity and promote a more communal mindset, if every player has cooperated in the last r_g rounds (where r_g < r), increase cooperation probability p_c in the current round according to the following formula:
     `p_c = min(1, 1 + alpha * (r_g / r))`
   - Where alpha is a tunable parameter that determines the degree of adaptive generosity. A larger alpha value results in more generous behaviour.
   - If no such cooperative streak exists, use a baseline cooperation probability p_b (default to 0.5).
   - If a player defects after a cooperative streak, reset the r_g counter and p_c back to their initial values.

2. Handle edge cases:
   - In the last round, prioritize the communal outcome and avoid punishing other players. Always cooperate, regardless of history.
   - In the first round, as mentioned above, initiate cooperation (C).

3. Be communal:
   - The strategy aims to maintain a balance between cooperation and defection while promoting a long-term communal outcome. The adaptive generosity feature encourages cooperation but also punishes defection to discourage exploitation. By doing so, TFT-AG fosters a sense of mutual trust and reciprocity that aligns with the communal mindset.

Pseudocode:

```
def TFT_AG(history, r, r_g, p_b, alpha):
    cooperation_probability = min(1, 1 + alpha * (r_g / r)) if history.cooperative_streak else p_b
    action = "C" if rand() <= cooperation_probability else "D"
    return action

def play_game(strategy, opponents, n, k, rounds, r_g_threshold):
    strategy.history.reset()
    for round in range(rounds):
        actions = [opponent.play(round) for opponent in opponents]
        strategy.history.append(actions)
        strategy.r_g += 1 if all(action == "C" for action in actions) else 0
        strategy.cooperation_probability = TFT_AG(strategy.history, rounds, strategy.r_g, strategy.p_b, strategy.alpha)
    payoffs = calculate_payoffs(strategy, opponents, n, k, rounds)
    return strategy, payoffs
```
'''

description_COMMUNAL_15 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Decision Rules:
   - In the first round, players contribute half of their endowment (C = 0.5). This sets a cooperative tone while also being cautious of potential freeloaders.
   - For subsequent rounds, players will mirror the average contribution level from the previous r rounds (excluding the current round being evaluated). If the average is below 0.5, players will defect; if it's above 0.5, they will cooperate; and if it's exactly 0.5, they will cooperate in the next round but reduce their contribution by 10% to encourage a shift towards cooperation.

2. Handling Edge Cases:
   - In the last round, players will cooperate fully (C = 1) as there is no potential retaliation.
   - In the first round, players will initially contribute half of their endowment but will quickly adapt to the average contribution level in the following rounds.

3. Being Communal:
   - TFTAC encourages cooperation by mimicking the behavior of other players while also being forgiving towards initial freeloading or occasional defections. However, it retaliates against persistent non-cooperation by matching the lack of contribution. The strategy aims to foster a balanced community spirit where contributions are reciprocated and freeloading is discouraged.
   - Additionally, TFTAC reduces its own contribution in response to high levels of cooperation as a means of encouraging even distribution of the public good among players and promoting fairness within the group.

Pseudocode:
```
Strategy TFTAC(n, r):
    contributions = [0] * r  # Initialize contributions history
    average_contribution = 0.5  # Set initial contribution level

    function player_action(round, history):
        if round == 1:
            return 0.5
        else:
            average_contribution = sum(history[-r:]) / r
            if average_contribution < 0.5:
                return 0
            elif average_contribution > 0.5:
                return 1
            else:
                contributions[round] = average_contribution
                if len(history) >= r and round != 1:
                    new_average = sum(history[-r:]) / r
                    if new_average < 0.4:
                        return 0
                    elif new_average > 0.6:
                        return 1 - (average_contribution * 0.1)
                else:
                    return average_contribution

    for round in range(1, r+1):
        contributions.append(player_action(round, contributions))

    return contributions
```
'''

description_COMMUNAL_16 = '''
 Title: Titan Strategy for N-Player Public Goods Game

1. Specify decision rules:
   The Titan Strategy is designed to promote cooperation while maintaining a degree of self-interest. It adapts its level of contribution based on the historical behavior of other players and the current round number.

   - In the first round, each player contributes at the minimum level (i.e., defect). This ensures that players start with an equal opportunity and avoids free riding.
     If n > 2: Titan(1) = D

   - For subsequent rounds, players adjust their contribution based on the average percentage of contributors in previous rounds (average_contribution_rate).
       If average_contribution_rate < threshold_1:
         - Players remain at minimum contribution level.
           If n > 2: Titan(t) = D, where t > 1

       Else if average_contribution_rate >= threshold_1 and average_contribution_rate < threshold_2:
         - Players gradually increase their contribution to encourage more cooperation but avoid over-contribution.
           If n > 2: Titan(t) = (k/n) * average_contribution_rate + D * (1 - (average_contribution_rate / threshold_2))

       Else if average_contribution_rate >= threshold_2:
         - Players contribute at the maximum level to support a strong community.
           If n > 2: Titan(t) = k/n

   - In the last round, players evaluate their total payoff and make a final decision based on their overall earnings.
     If total_payoff >= target_reward:
       - Players contribute at maximum level to maximize their rewards in the last round.
         If n > 2: Titan(r) = k/n

     Else if total_payoff < target_reward:
       - Players contribute at minimum level, hoping for better results in future games.
         If n > 2: Titan(r) = D

2. Handle edge cases:
   - In case of no opponent, the strategy still cooperates since it is designed to promote cooperation even if there are no others to benefit from it.
     If n = 1: Titan(t) = k/n, for all t

3. Be communal:
   The Titan Strategy encourages cooperation by gradually increasing contributions when the average contribution rate approaches a cooperative threshold (threshold_2), but it also ensures self-interest through the minimum and maximum contribution levels. Additionally, its adaptive nature allows it to respond to different opponent behaviors during the game.
'''

description_COMMUNAL_17 = '''
 Strategy Name: Tit-for-Tat-Evolution (T4TE)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round, T4TE starts by cooperating (playing action C). The decision to continue cooperating or defect is based on the history of interactions with other players. For player i in a single round t:

- If all previous opponents have cooperated, then player i cooperates (c_i = 1)
- If any opponent has ever defected and the last interaction was also a defection, then player i defects (c_i = 0)
- Otherwise, player i cooperates if its last interaction was cooperation, and defects otherwise.

2. Handle edge cases - What do you do in the first round, last round, etc.?

For the first round, since there is no history, T4TE initiates by cooperating (c_i = 1). In the last round, if the total number of cooperators has reached or exceeded a critical threshold Ct (determined experimentally), then all players cooperate. If not, they defect.

3. Be communal - Clearly align with the communal mindset

T4TE aims to maintain an environment of mutual cooperation by adopting a forgiving and cooperative approach initially but retaliating against defection to discourage ongoing selfish behavior. By doing so, it encourages long-term collaborative relationships while still deterring potential free-riders.

Pseudocode:

```
def T4TE(n, k, r):
  players = [1,2,...,n]
  history = {} # store previous interactions for each player and round

  function cooperate():
    if all_cooperators_in_history():
      return True
    elif any_defectors_in_history() and last_interaction_was_defection():
      return False
    else:
      return last_interaction_with(player) was cooperation

  function all_cooperators_in_history():
    for player in players:
      if not history[player].cooperated:
        return False
    return True

  function any_defectors_in_history():
    for player in players:
      if history[player].defected:
        return True
    return False

  function last_interaction_with(player):
    if round == 1 or not history[player]:
      return cooperate()
    else:
      if history[player][round-1] == cooperate():
        return 'cooperation'
      else:
        return 'defection'

  function last_interaction_was_defection():
    for player in players:
      if last_interaction_with(player) == 'defection':
        return True
    return False

  for round in range(1, r+1):
    payoffs = [0]*n
    cooperators = 0

    for player in players:
      c_i = cooperate()
      if c_i:
        cooperators += 1
        history[player].cooperated = True
      else:
        history[player].defected = True

    for player in players:
      payoff_i = (1 - c_i) + (k/n)*cooperators
      payoffs[player] += payoff_i

    if round == r and cooperators >= Ct:
      for player in players:
        history[player].defected = False # reset for next game
```
'''

description_COMMUNAL_18 = '''
 Title: Titan Strategy for N-Player Public Goods Game

1. Decision Rules:
   - Base Contribution (BC): A fixed base contribution level that gradually increases over time to encourage more cooperation. BC = min(round number * (r / 100), n - 1). This ensures that the contribution level is proportional to the round and the total number of players.
   - Adaptive Contribution (AC): The Titan Strategy adapts its contributions based on the previous round's average contribution. If the average contribution exceeds the current Base Contribution, then the player will cooperate up to this level; otherwise, they will defect.

2. Handle Edge Cases:
   - First Round: Cooperate up to BC = 0 (no base contribution in the first round). This sets a positive tone for cooperation and encourages others to follow suit.
   - Last Round: Contribute the maximum possible amount (n - 1) as it benefits all players, even if everyone else defects.
   - Other Edge Cases (e.g., when BC > n-1 or BC < 0): Limit contributions to the maximum or minimum possible value to avoid excessive contributions that could potentially harm the player's own payoff.

3. Be Communal:
   - Foster a sense of community by consistently promoting cooperation and showing responsiveness to other players' actions.
   - Encourage other players to cooperate by contributing at or above the average level when they do so as well, demonstrating trust and reciprocity.
   - If players repeatedly defect, gradually decrease the base contribution to encourage more cooperation and align with the communal mindset.

Pseudocode:

```python
def titan_strategy(round, history):
    total_contributions = sum(history[-r:])  # Calculate average contributions over last r rounds
    base_contribution = min(round * (r / 100), n - 1)

    if round == 1:
        contribution = base_contribution  # Cooperate in the first round
    elif total_contributions > base_contribution:
        contribution = min(total_contributions, n - 1)  # Cooperate up to average contribution
    else:
        contribution = 0  # Defect when average contributions are below base contribution

    return contribution
```
'''

description_COMMUNAL_19 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules:
   - Initially, cooperate in the first round to demonstrate goodwill (c_i = 1).
   - In subsequent rounds, replicate the actions of the previous round by other players (cooperate if majority contributed in the previous round, defect otherwise). Pseudocode:

```python
def decideAction(history):
    # history is a list of lists, where each inner list represents a round's actions of all players
    n_contributors = sum([sum(round) for round in history[-1]])  # count contributors in the last round
    if n_contributors == len(history):  # everyone contributed in the last round
        return 'Cooperate'
    else:
        return 'Defect'
```

2. Handle edge cases:
   - In the first round, cooperate regardless of past history (c_i = 1).
   - In the last round, cooperate if the majority contributed in the previous round (as per decision rule above). If not, defect as it's the final round and there are no further interactions.

3. Be communal:
   - The strategy aims to promote cooperation by reciprocating contributions of other players.
   - By demonstrating goodwill initially and responding cooperatively when others do so, the ATFT strategy fosters a sense of trust and encourages long-term cooperation.

This strategy is flexible and adaptive, allowing it to work well against a wide range of opponent behaviors while maintaining a communal mindset. The goal is to achieve a balance between individual success (payoff) and collective benefit (public good).
'''

description_COMMUNAL_20 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially (first round), cooperate to demonstrate goodwill and encourage cooperation among players.
   - For subsequent rounds, cooperate if the majority of players cooperated in the previous round; otherwise, defect. This rule encourages reciprocity and builds trust over time.
   - In case of a tie, assume that half of the players cooperated (rounding down) and cooperate if the number is greater than or equal to n/2. This decision ensures that the strategy prefers cooperation even when there's uncertainty about other players' actions.

Pseudocode:
```python
function ATFT(history, n, k):
    if round = 1:
        cooperate = True
    else:
        cooperate = (len(cooperators_in_previous_round) >= n/2)
    payoff = (1 - cooperation) + (k / n) * sum(history[-n:])
    return cooperation, payoff
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate as described above.
   - In the last round, cooperate if the majority of players have cooperated throughout the game to maximize payoff.
   - If a player defects during the game, revert to initial behavior (cooperating) in the following rounds to encourage them to reciprocate cooperation.

3. Be communal - Clearly align with the communal mindset
   - By favoring cooperation over defection under most conditions, this strategy prioritizes collective benefits and adheres to a communal approach.
   - The rule of reciprocity encourages other players to follow suit and fosters an environment where cooperation becomes self-reinforcing.
   - By considering the total number of cooperators in the previous round when deciding whether to cooperate, this strategy aligns with the goal of maximizing communal benefits.
'''

description_COMMUNAL_21 = '''
 Title: Tit-for-Tat Adaptive Strategy (TFTA) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?

The TFTA strategy follows a tit-for-tat approach, starting with cooperation in the first round, and then mimicking the opponent's previous action in the subsequent rounds. This encourages reciprocity among players while also being forgiving for initial defectors.

Pseudocode:
```
function TFTA(history):
  if history is empty:
    return Cooperate (C)
  else:
    last_action = history[len(history)-1]
    if last_action == C:
      return Cooperate (C)
    else:
      return Defect (D)
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

In case of repeated games with a finite number of rounds, it's important to consider the endgame approach. TFTA will maintain its cooperative behavior until detecting the penultimate round and then switch to defection for the remaining rounds. This prevents giving away resources unnecessarily when the game is nearly over.

Pseudocode:
```
function TFTA(history, r):
  if len(history) >= r-1:
    return Defect (D)
  else:
    return TFTA(history)
```

3. Be communal - Clearly align with the communal mindset

TFTA strategy promotes a communal approach by fostering cooperation and reciprocity, making it more likely for players to contribute to the community project and benefit collectively. The strategy is also adaptive and robust, adjusting its actions based on the opponent's behavior while maintaining fairness and forgiveness towards initial defectors.

Overall, TFTA strategy provides a simple yet effective approach for participating in the N-Player Public Goods Game, encouraging cooperative behavior while minimizing exploitation.
'''

description_COMMUNAL_22 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules:
   - In the initial round, cooperate to foster a cooperative environment and demonstrate goodwill (C).
   - For subsequent rounds, observe the previous round's total contributions (total_contributions_t-1) and decide whether to contribute or defect based on the following rule:
     - If total_contributions_t-1 ≥ average_contributions, cooperate (C).
     - Else if total_contributions_t-1 < average_contributions - threshold, defect (D).
     - In all other cases (including the edge case of total_contributions_t-1 = average_contributions), mirror the previous round's individual action (if player i contributed in the previous round, cooperate; if not, defect).

   The average_contributions is calculated as the moving average of the last 'm' contributions, where m is a user-defined constant that balances short-term and long-term cooperation. A larger m value emphasizes long-term cooperation while a smaller m value prioritizes recent contributions.

   The threshold is also a user-defined constant that sets the minimum acceptable level of total contributions before cooperating, even if it's below the average. This ensures our strategy doesn't immediately defect when facing overly selfish opponents.

2. Handle edge cases:
   - In the first round, cooperate (C) as mentioned in step 1.
   - In the last round, mirror the previous round's individual action due to the recursive nature of the strategy.

3. Be communal:
   - By starting with cooperation and responding cooperatively when others cooperate, TFTAC promotes a communal mindset by demonstrating willingness to contribute to the common good and punishing defections only if necessary.

Pseudocode:
```
def TFTAC(round, m, threshold):
    total_contributions = [0] * r  # initializing total contributions for all rounds
    average_contributions = 0

    if round == 1:
        return 'C'  # cooperate in the first round

    total_contributions[round - 1] += 1 if contribution == 'C' else 0  # update contributions for last round
    average_contributions = calculate_moving_average(total_contributions, m)

    if total_contributions[round - 1] >= average_contributions + threshold:
        return 'D'  # defect when others are not contributing enough
    elif total_contributions[round - 1] <= average_contributions - threshold:
        return 'D'  # defect when others are not contributing at all
    else:
        return mirror_previous_action(round)  # mirror previous round's action
```
'''

description_COMMUNAL_23 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT) for N-Player Public Goods Game

1. Specify decision rules:
   - Initiate cooperation (play C): Start with cooperation in the first round to contribute to a positive community effect and signal trustworthiness.
   - Respond cooperatively if others cooperate (c_j >= 0.5 * n, for t > 1): If more than half of the players cooperated in the previous round, respond with cooperation in the current round, promoting reciprocity and encouraging continued cooperation.
   - Punish defection: If fewer than half of the players cooperated in the previous round (c_j < 0.5 * n), defect in the current round to penalize non-cooperative behavior and encourage future cooperation.

Pseudocode for decision rule:
```
if t == 1: // first round, start by cooperating
    action = "C"
else:
    total_contributions = count_cooperators(previous_round)
    if total_contributions >= (0.5 * n):
        action = "C" // cooperate
    else:
        action = "D" // defect
```

2. Handle edge cases:
   - Last round: Maintain the same decision rules as for regular rounds to ensure the strategy is adaptive and can still benefit from late-round cooperation or punishment.
   - First m rounds (m > 1): Cooperate in the first m rounds to promote a positive initial effect and encourage cooperation among opponents, but after that, follow the main decision rule above.

3. Be communal: Align with the communal mindset by prioritizing collective success over individual gain and promoting reciprocity through adaptive cooperative behavior. The strategy encourages cooperation when others are cooperative while punishing defection to foster a collaborative environment among players.
'''

description_COMMUNAL_24 = '''
 Strategy Name: Tit-for-Tat Adaptive Cooperation (TFTAC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   In each round t, player i decides to Cooperate (C) or Defect (D) based on the following rule:
   - If in the previous round (t-1), all players cooperated (total_contributions = n), then player i also cooperates (C).
   - If in the previous round, player i contributed and at least one other player defected (0 < total_defectors < n), then player i cooperates (C) if total_defectors has not increased for 3 consecutive rounds. Otherwise, player i defects (D).
   - If in the previous round, player i defected or all players defected (total_defectors >= n), then player i defects (D) unless it is the first round.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, every player cooperates to establish trust and goodwill among players.
   - As the game progresses beyond the first round, the strategy adjusts based on previous rounds' outcomes.
   - In the last round, if a player has previously cooperated but is facing a group of defectors in the current round, they may choose to defect to avoid being exploited.

3. Be communal - Clearly align with the communal mindset:
   TFTAC prioritizes long-term cooperation and mutual trust as it retaliates only when betrayed repeatedly by others. By cooperating initially, TFTAC encourages a sense of community and cooperation among players.

Pseudocode for decision making in each round t:

```python
def decide_action(t, total_contributions_prev, my_contribution_prev, history):
  if t == 1: # first round
    return "Cooperate"

  if (total_contributions_prev == n) and (my_contribution_prev == "Cooperate"):
    return "Cooperate"

  consecutive_defects = 0
  for r in range(t-2, max(0, t-4)): # look back 3 rounds
    if history[r]["total_contributions"] < n:
      consecutive_defects += 1
      if consecutive_defects == 3:
        break

  if (my_contribution_prev == "Cooperate") and (consecutive_defects == 0): # no defection in last 3 rounds, continue cooperation
    return "Cooperate"

  if (my_contribution_prev == "Defect") or (total_contributions_prev < n): # defect when betrayed or faced with a group of defectors
    return "Defect"
```
'''

description_COMMUNAL_25 = '''
 Title: Titan Strategy for N-Player Public Goods Game

1. Decision Rules (Cooperate vs Defect):
   The Titan strategy follows a tit-for-tat approach with a cooperative bias and adaptability based on historical cooperation levels and game parameters.

   - If the total number of cooperators in the previous round is greater than or equal to a certain threshold (T), cooperate (C). This threshold (T) increases gradually over time to encourage initial cooperation and punish persistent defection.
   - If the total number of cooperators in the previous round is less than T, defect (D). This encourages reciprocity and discourages freeloading.

2. Edge Cases:
   - First Round: Cooperate (T = n/2 for initial cooperation) to foster a collaborative environment.
   - Last Round: Cooperate if the total number of cooperators in the current round is greater than or equal to T, and defect otherwise. This allows for some punishment in case of late defection.
   - In all other rounds, the decision to cooperate or defect is determined by the rule described above.

3. Communal Mindset:
   The Titan strategy aims to balance cooperation and punishment, fostering a communal mindset that rewards initial cooperation while punishing persistent defection. This encourages players to collaborate and create a sustainable public good.

Pseudocode:
```
def titan_strategy(i, round, total_cooperation, k, n):
    if round == 1:
        return 'C'  # Cooperate in the first round

    T = (n / 2) + round  # Adjust cooperation threshold over time

    if total_cooperation >= T:
        return 'C'  # Cooperate when more than T players cooperated in the previous round
    else:
        return 'D'  # Defect when less than T players cooperated in the previous round
```
'''

description_COMMUNAL_26 = '''
 Title: Tit-for-Tat Communal Strategy (TFTC) for N-Player Public Goods Game

1. Specify decision rules:
   - In each round, start by cooperating (contribute to the community project). This sets a cooperative tone and aligns with the communal mindset.
   - In subsequent rounds, decide whether to continue cooperating or defect based on the total number of cooperators in the previous round compared to the average number of cooperators over the past rounds (excluding the first round). If the total number of cooperators is greater than or equal to the average, cooperate; otherwise, defect.
   - The aim is to encourage mutual cooperation and punish those who repeatedly deviate from it, while also being forgiving when others make mistakes.

2. Handle edge cases:
   - In the first round, cooperate as a goodwill gesture. This encourages others to reciprocate in the following rounds.
   - In the last round, cooperate if the average number of cooperators over the previous rounds is greater than or equal to half of the total players (n/2). This ensures that even if cooperation breaks down earlier, there can still be a cooperative ending.

3. Be communal:
   - This strategy prioritizes cooperation and adapts to the actions of others while aiming for a mutually beneficial outcome. It encourages a culture of reciprocity and forgiveness, fostering long-term cooperation.

Pseudocode:

```python
def TFTC(n, k, r):
    total_cooperators = 0  # Initialize total cooperators for the first round
    average_cooperation = 0  # Initialize average cooperation over previous rounds (excluding the first)
    past_rounds = []  # Initialize list to store the number of cooperators in each past round

    def play_round(round, current_cooperators):
        nonlocal total_cooperators, average_cooperation, past_rounds
        if round == 1:
            total_cooperators = current_cooperators
            return 'C'

        past_rounds.append(current_cooperators)
        average_cooperation = (average_cooperation * (past_rounds.__len__() - 1) + current_cooperators) / past_rounds.__len__()

        if current_cooperators >= (average_cooperation if round != r else n/2):
            return 'C'
        else:
            return 'D'

    for round in range(1, r+1):
        action = play_round(round, total_cooperators)  # Play the current round and get the decision
        total_cooperators = total_cooperators + (1 if action == 'C' else 0)  # Update total cooperators for the next round

    return play_round(r, total_cooperators)  # Play the last round to account for the edge case
```
'''

description_COMMUNAL_27 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfT-A)

1. Decision Rules:
   - In the initial round (t=1), cooperate to establish a cooperative environment and build trust.
   - For subsequent rounds (t>1):
      - If an opponent cooperated in the previous round (t-1), cooperate in the current round (t). This is based on the 'Tit for Tat' strategy, which encourages reciprocity.
      - If an opponent defected in the previous round (t-1), also defect in the current round (t). This is to punish defection and encourage opponents to cooperate.
   - To adapt to various opponent behaviors, a forgiveness mechanism is implemented: if an opponent who previously defected switches to cooperation, return to cooperating yourself in the following round.

2. Handle Edge Cases:
   - In the last round (t=r), cooperate regardless of the opponent's previous action as the game ends and there are no future interactions to consider.
   - In the first round (t=1), cooperate to initiate a cooperative environment as mentioned above.
   - If faced with an opponent that does not make a move (i.e., neither C nor D) in any round, assume they defect and respond accordingly based on decision rules.

3. Be Communal:
   - Aligns with the communal mindset by promoting cooperation and reciprocity in interactions.
   - By forgiving opponents who switch from defection to cooperation, TfT-A strategy encourages rebuilding trust and maintaining a cooperative environment.
'''

description_COMMUNAL_28 = '''
 Strategy Name: Tit-for-Tat-Evolution (TfT-E)

1. Specify decision rules - When exactly do you cooperate vs defect?
   In each round t, TfT-E starts by cooperating if the previous player's action was also cooperation (C_t-1 = C). If the previous player did not cooperate (C_t-1 = D), TfT-E will also defect. This strategy mimics cooperation initially but retaliates against defection in a non-aggressive manner by defecting once and then reverts to cooperating again.

   Pseudocode:
   ```
   function TfT_E(C_t-1):
       if C_t-1 == C:
           return C (Cooperate)
       else:
           return D (Defect)
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   For the first round (when there is no previous player's action), TfT-E starts by cooperating to show goodwill. In the last round, TfT-E acts based on the previous player's action as usual.

3. Be communal - Clearly align with the communal mindset
   By starting with cooperation and only retaliating when necessary, TfT-E encourages long-term cooperative relationships. It demonstrates forgiveness by resuming cooperation after defection, fostering a sense of trust and reciprocity that aligns with the communal mindset.

Additionally, TfT-E can adapt to various opponent behaviors due to its simplicity and clear response structure (cooperate or defect based on previous action). This strategy is less susceptible to exploitation as it retaliates only when necessary, maintaining a cooperative stance for the majority of interactions.
'''

description_COMMUNAL_29 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TfT-AC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round and last round, players always cooperate (C). This encourages cooperation as an initial gesture while also showing willingness to support the community in the end.
   - For all other rounds, players imitate the previous opponent's action: If the opponent cooperated (C) in the previous round, cooperate; if the opponent defected (D), defect. This tit-for-tat approach encourages reciprocity and punishes defection, while also rewarding cooperation.
   - To be adaptive to a wide range of opponent behaviours, players will adjust their level of cooperation based on the average percentage of cooperators in the past r/2 rounds (k-factor). If the average percentage is high (above a threshold), increase the likelihood of cooperating; if it's low (below a threshold), decrease the likelihood.
   - The k-factor can be adjusted dynamically based on the number of players and rounds, ensuring robustness across different game parameters.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, as mentioned earlier, always cooperate (C).
   - In the last round, cooperate if the opponent cooperated in the previous round; defect otherwise. This ensures fairness and allows players to finish on a positive note when reciprocity is demonstrated.
   - For intermediate rounds, use the decision rules specified under 1.

3. Be communal - Clearly align with the communal mindset
   - The TfT-AC strategy prioritizes community interests by cooperating at the beginning and end of the game, encouraging a sense of fairness and mutual support among players.
   - The adaptive cooperation component allows for responsiveness to other players' behavior while maintaining a commitment to the community project.
   - By being flexible and adjusting its level of cooperation based on the average percentage of cooperators in previous rounds, TfT-AC demonstrates a willingness to work with various opponent strategies and promote communal success.
'''

description_COMMUNAL_30 = '''
 Title: Titan Strategy for N-Player Public Goods Game

1. Decision Rules:
   - Cooperate when the ratio of current cooperators to the total number of players exceeds a threshold (T). This encourages cooperation in situations where it is beneficial for the community and deters defection when most others are cooperating.
   - Defect otherwise, as this maximizes personal gain when cooperation is not common.

Pseudocode:
```
def titan_strategy(round, n, k, current_cooperators):
  if round == 1 or round == r:
    return 'Cooperate' # First and last rounds follow a communal mindset

  cooperators_ratio = current_cooperators / n

  if cooperators_ratio > T:
    return 'Cooperate'
  else:
    return 'Defect'
```

2. Handle Edge Cases:
   - In the first round, players follow a communal mindset and cooperate to establish cooperation norms within the group.
   - In the last round, players may choose to cooperate one final time to contribute positively to the community, or they can defect to maximize their individual payoff after r rounds of gameplay.

3. Be Communal:
   - The Titan Strategy prioritizes cooperation when it is statistically beneficial for the group, thus fostering a communal mindset within the players.
   - By adjusting the T threshold, the strategy can be tuned to accommodate various cooperative behaviors across different game settings and player populations.
'''

description_COMMUNAL_31 = '''
 Strategy Name: Tit-for-Tat Adaptive (TfTA) Public Goods Game Strategy

1. Specify decision rules - When exactly do you cooperate vs defect?
   a. In the first round, cooperate to start with a cooperative gesture and set a norm for future rounds.
   b. For subsequent rounds, observe the total number of cooperators in the previous round (total_contributions_prev). If the number of cooperators is equal to or greater than a threshold 't' (defined below), cooperate; otherwise defect.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   a. As mentioned earlier, cooperate in the first round.
   b. In the last round, cooperate if the number of total cooperators is greater than or equal to the threshold 't' (defined below). Otherwise, defect since there are no further rounds to retaliate.

3. Be communal - Clearly align with the communal mindset:
   a. The strategy aims to foster a communal environment by reciprocating cooperation in the previous round, thus promoting mutual trust and long-term cooperation.
   b. If the number of cooperators falls below the defined threshold 't', the strategy will temporarily defect to encourage others to follow suit and return to cooperation when conditions improve.

Threshold definition:
- Set a tunable parameter 'p' (0 < p < 1) that represents the minimum percentage of cooperators needed for the strategy to continue cooperating. Calculate the threshold 't' as n * p, where 'n' is the total number of players. In other words, if more than 't' number of players cooperate in a given round, the TfTA strategy will also cooperate in the next round.

Pseudocode:
```
def TfTAPublicGoodsGameStrategy(round, n, k, t):
  if round == 1:
    return Cooperate()
  else:
    total_contributions_prev = getTotalContributionsFromPreviousRound(round - 1)
    if total_contributions_prev >= t:
      return Cooperate()
    else:
      return Defect()
```
'''

description_COMMUNAL_32 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules:
   - Initialize cooperation (C) in the first round to promote a cooperative environment.
   - For subsequent rounds, observe the actions of opponents in the previous round and respond accordingly:
     - If an opponent cooperated, cooperate as well (C).
     - If an opponent defected, also defect in the next round (D). This is intended to discourage defection and encourage cooperation.
   - To promote forgiveness and rebuild trust after periods of conflict, switch back to cooperation if an opponent who previously defected cooperates again (Tit-for-Tat principle).

2. Handle edge cases:
   - In the last round, cooperate regardless of previous actions to maximize potential payoff.
   - If there is no history with a new opponent, cooperate in the first round as an initiative to foster cooperation.

3. Be communal:
   - By following the Tit-for-Tat principle, TFT-AC aligns with a communal mindset by promoting fairness, forgiveness, and the mutual benefit of cooperation.
   - The adaptive nature of this strategy allows it to be flexible in response to various opponent behaviors while maintaining a cooperative stance.

Pseudocode:

```python
def tft_ac(round, history):
  if round == 1 or not history:
    action = 'C'  # Cooperate in the first round and when there's no history

  else:
    opponent_action = history[-1]  # Get the last action of the opponent from history
    if opponent_action == 'C':
      action = 'C'
    elif opponent_action == 'D':
      action = 'D'
    elif round == r:  # Last round, cooperate regardless of previous actions
      action = 'C'

  return action
```
'''

description_AGGRESSIVE_1 = '''
 Strategy Name: Adaptive Tit-for-Tat Aggressor (ATFA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   The ATFA strategy follows a tit-for-tat approach but with an aggressive twist to ensure it stays ahead of opponents. It will cooperate initially and punish opponents who fail to reciprocate, while being more forgiving towards those who demonstrate cooperation.

   - If the opponent cooperates (C), the ATFA also cooperates (C).
     Pseudocode: if other_player_action == "C", then my_action = "C"

   - If the opponent does not cooperate (D) in the first three rounds, the ATFA will defect (D). This initial aggression serves to test whether opponents are cooperative.
     Pseudocode: if other_player_action == "D", then
          if round <= 3, then my_action = "D"

   - After the first three rounds, the ATFA will cooperate (C) if the opponent has cooperated in at least one previous round. This encourages cooperation and rewards opponents who demonstrate a willingness to cooperate.
     Pseudocode: if other_player_action == "D" and there was cooperation in previous rounds, then my_action = "C"

   - If the opponent has not cooperated at all during the game so far, the ATFA will defect (D) to maximize personal payoff.
     Pseudocode: if other_player_action == "D" and there was no cooperation in previous rounds, then my_action = "D"

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, the ATFA strategy is aggressive and will defect (D) to test other players' behavior. This decision rule was mentioned earlier.

   In the last round, the ATFA will cooperate (C) regardless of the opponent's previous actions as the benefits from a potential retaliation would not outweigh the one-time cost in the final round.

3. Be aggressive - Clearly align with the aggressive mindset
   The ATFA strategy is aggressive in its initial testing phase, where it defects to encourage other players to demonstrate their cooperation. However, it also punishes opponents who fail to reciprocate cooperation and forgives those who demonstrate a willingness to cooperate. This approach allows the ATFA to balance aggression with flexibility, making it robust against various opponent behaviors.
'''

description_AGGRESSIVE_2 = '''
 Title: Tit-for-Tat Aggressive Strategy (TATF) for N-Player Public Goods Game

1. Specify decision rules:
   - Initiate cooperation in the first round (C). This sets a positive tone and may encourage other players to cooperate as well.
   - In subsequent rounds, analyze the previous round's cooperation level (total_contributions) and take action based on the following rules:
     - If more than half of the players cooperated in the previous round, continue cooperating (C). This rewarding behavior encourages others to maintain cooperation.
     - If less than or equal to half of the players cooperated in the previous round, defect (D) in this round. This punishing behavior discourages defection and may encourage other players to cooperate in future rounds.
   - Adaptive rule: In case of a tie (exactly half of the players cooperated), consider k as an influence factor for the decision. If k is closer to n, defect (D); otherwise, continue cooperating (C). This adaptability ensures robustness across various game parameter settings.

2. Handle edge cases:
   - In the last round, defect (D) regardless of the previous round's cooperation level since there are no further rounds for retaliation or reward.
   - In the first round, cooperate (C) as mentioned before.

3. Be aggressive:
   - By punishing defection and rewarding cooperation, the TATF strategy takes an aggressive stance towards players who do not contribute to the public good.
   - The strategy's adaptability ensures a robust response to various opponent behaviors while maintaining an aggressive mindset.
'''

description_AGGRESSIVE_3 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TfTA starts by cooperating in the first round to encourage others to cooperate, setting a potential foundation for mutual cooperation. After the first round, it follows a "tit-for-tat" pattern where it cooperates if its opponent cooperated in the previous round and defects if the opponent defected. However, to be more aggressive, TfTA will immediately defect if any opponent defected after the initial cooperation in the first round.

   Pseudocode:
   ```
   function TfTA(round, opponent_history) {
       if (round == 1) return Cooperate;
       if (opponent_history[round-1] == Defect) return Defect;
       return opponent_history[round-1];
   }
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, TfTA cooperates to encourage others to cooperate. In the last round, TfTA defects because there are no future rounds for retaliation. For any other round, it uses the decision rule specified above.

3. Be aggressive - Clearly align with the aggressive mindset
   By immediately defecting when an opponent defects after the first round, TfTA shows a strong willingness to punish opponents who don't cooperate. This aggressive behavior discourages defection and promotes cooperation only when opponents also choose to cooperate. However, it should be noted that TfTA is still capable of mutual cooperation as long as its opponent does not defect in the first round.

   In case multiple opponents defect simultaneously for the first time, each opponent will be punished separately based on their own individual defection history. This allows TfTA to target specific opponents for punishment without becoming too aggressive towards the entire group.
'''

description_AGGRESSIVE_4 = '''
 Strategy Name: Adaptive Aggressor (AA)

1. Specify decision rules - When exactly do you cooperate vs defect?

The Adaptive Aggressor strategy follows a tit-for-tat approach with a twist to maximize gains in the long run while maintaining an aggressive edge. In each round, it will determine its action based on the previous round's total contributions (T_prev) and the average historical contributions (Ave).

- Cooperate if T_prev > Ave
- Defect if T_prev ≤ Ave

The aim is to punish undercontributors while maintaining cooperation when others are acting cooperatively.

2. Handle edge cases - What do you do in the first round, last round, etc.?

Since the strategy is adaptive and relies on historical contributions, it requires an initial contribution for the average calculation. In the first round, players will contribute to encourage cooperation but defect from the second round if others don't follow suit:

- Contribute in the first round (T_prev = 0)
- Cooperate if T_1 > Ave_1 (Ave_1 is the average of contributions in the first round)
- Defect otherwise

In the last round, players will defect regardless of the previous round's total contributions, as there are no more subsequent rounds for retaliation or reward:

- Always defect in the last round

3. Be aggressive - Clearly align with the aggressive mindset

The Adaptive Aggressor strategy is designed to be aggressive by punishing undercontributors and only cooperating when others do so as well. This approach aims to encourage cooperation while maximizing individual gains, aligning with an aggressive playstyle in terms of self-interest and strategic retaliation.

Pseudocode:

```
Strategy AdaptiveAggressor(n, r, k):
  Initialize total_contributions_history as an empty list

  Function PlayRound(round_number):
    If round_number == 1:
      contribution = Cooperate()
      Store contribution in total_contributions_history
      Return contribution

    Else:
      Calculate average_contribution = TotalAverageContributions(total_contributions_history)
      Calculate previous_round_contributions = TotalRoundContributions(total_contributions_history, round_number - 1)

      If previous_round_contributions > average_contribution:
        contribution = Cooperate()
      Else:
        contribution = Defect()

      Store contribution in total_contributions_history
      Return contribution

  Function TotalAverageContributions(hist):
    Calculate total = Sum(hist)
    If hist is not empty:
      Calculate average = total / Length(hist)
    Else:
      Calculate average = 0
    Return average

  Function TotalRoundContributions(hist, round_number):
    Return hist[round_number - 1]
```
'''

description_AGGRESSIVE_5 = '''
 Strategy Name: Tit-for-Tat Aggressor (TFA)

1. Specify decision rules - When exactly do you cooperate vs defect?

The TFA strategy starts by cooperating in the first round to show goodwill and encourage cooperation among opponents. After that, it adapts its actions based on the history of opponent's behavior:

- If an opponent has been cooperative (C), the TFA will also cooperate (C).
- If an opponent has been uncooperative (D) in the previous round, the TFA will defect (D) as a punishment. However, if the opponent then switches to cooperation in the current round, the TFA will forgive and return to cooperating again.

Pseudocode:

```python
def TFA(opponent_history):
  if round == 1:
    action = "C"  # Cooperate in the first round

  else:
    last_opponent_action = opponent_history[-1]
    if last_opponent_action == "C":
      action = "C"  # Cooperate when opponent was cooperative
    elif last_opponent_action == "D":
      action = "D"  # Defect when opponent was uncooperative
      forgiven = False  # Flag to check if forgiveness is needed in the next round

  return action, forgiven  # Return both action and forgiveness flag for future decision making
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

The TFA strategy maintains its aggression throughout the game. It may consider different approaches for the initial rounds or when the game is about to end:

- In the final rounds, the TFA could become more cooperative if it expects other players to switch strategies and try to improve their overall payoff. However, this decision would depend on the specific observation of opponent behavior near the end of the game.
- In the early stages (e.g., first 10% of total rounds), the TFA could be more aggressive in punishing uncooperative opponents to quickly identify and isolate free riders.

3. Be aggressive - Clearly align with the aggressive mindset

The Tit-for-Tat Aggressor strategy is designed to be both adaptive and robust to a wide range of opponent behaviors while maintaining an aggressive stance. By punishing uncooperative opponents, it aims to encourage cooperation and improve its payoff over time. The strategy's forgiving nature also allows for potential reformation of cooperative relationships when opponents switch to cooperation after being punished.

The TFA can be fine-tuned by adjusting the aggression level (e.g., the number of rounds it takes before considering forgiveness) or by incorporating additional features like adaptive punishment severity based on opponent history.
'''

description_AGGRESSIVE_6 = '''
 Strategy Name: Tit-for-Tat Aggressive (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TfTA will start by cooperating in the first round to signal goodwill and foster potential cooperation. After that, it will adopt a tit-for-tat approach with an aggressive twist. In each round t, if a player i observes that all other players (j ∈ {1, 2, ..., n}) cooperated in round t-1, then player i will also cooperate (C) in round t:
   ```
   if all(other_players_cooperated[t-1]) == True:
       action[i][t] = "C"
   ```
   If any player defected in the previous round, TfTA will respond aggressively by also defecting. This punishment is designed to discourage defection and establish a dominant presence:
   ```
   if not all(other_players_cooperated[t-1]):
       action[i][t] = "D"
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, TfTA cooperates to initiate a potential cooperation scenario:
   ```
   if round == 1:
       action[i][t] = "C"
   ```
   The strategy does not alter its behavior in the last round as it continues to react aggressively to defection and cooperate when all players cooperated in the previous round.

3. Be aggressive - Clearly align with the aggressive mindset
   TfTA's core design is based on being reactive, responding to other player's actions while maintaining a dominant presence through its cooperative-punishment cycle. This strategy assumes that players can benefit from cooperation but will be discouraged from defecting due to the aggressive response from TfTA.
   In each round, if TfTA decides to cooperate, it does so with the intention of maximizing the community project's total contributions (k/n) × Σ(j=1 to n) c_j, which benefits all players in a cooperative scenario. If any player defects, TfTA retaliates by also defecting to minimize the public good and assert its aggressive stance.
'''

description_AGGRESSIVE_7 = '''
 Strategy Name: Tit-for-Tat Aggressive (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round t, the TfTA strategy will start by cooperating (C) in the first round to foster an environment of cooperation. After that, it will adapt its behavior based on the previous round's actions of other players.

- If all opponents cooperated in round t-1: The TfTA strategy will also cooperate in round t (C).
- If any opponent defected in round t-1: The TfTA strategy will defect in round t (D).

2. Handle edge cases - What do you do in the first round, last round, etc.?

In the first round, since there is no previous information available about opponents' behavior, TfTA will cooperate to encourage cooperation among players. In the last round, TfTA will follow its decision rule as it has all necessary information up to that point.

3. Be aggressive - Clearly align with the aggressive mindset:

TfTA is an aggressive strategy as it responds defensively when opponents defect. By defecting in response to defection, it signals a tough stance and discourages other players from taking advantage of its cooperative nature in earlier rounds. However, TfTA remains willing to cooperate when other players also do so. This aggressive approach aims to maximize payoff while maintaining the potential for cooperation if the opponent also adapts a cooperative strategy.

Pseudocode:

```python
def tfta_strategy(n, k, r, round, history):
    if round == 1:
        action = 'C' # Cooperate in the first round
    else:
        num_cooperators = len([1 for h in history if h == 'C'])
        if num_cooperators == n:
            action = 'C' # Cooperation when all opponents cooperated last round
        elif num_cooperators > 0:
            action = 'D' # Defection when any opponent defected last round
        else:
            action = 'D' # Defection when no cooperation in the previous round
    return action
```
'''

description_AGGRESSIVE_8 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Decision Rules:
   - In each round, the ATFT strategy cooperates initially (C on the first round). If a player has been cooperated with in the previous round, the ATFT strategy also cooperates. Otherwise, it defects (D). This creates a tit-for-tat dynamic where cooperation is reciprocated, but defection leads to immediate retaliation and continued defection until the other player cooperates again.

   Pseudocode:
   ```
   function ATFT(round_num, previous_opponent_action):
       if round_num == 1:
           return 'C'  # Cooperate on the first round
       else:
           if previous_opponent_action == 'C':
               return 'C'  # Cooperate if opponent cooperated last round
           else:
               return 'D'  # Defect if opponent defected last round
   ```

2. Handle Edge Cases:
   - In the first round, ATFT strategy cooperates to show goodwill and promote cooperation. If no previous interaction history exists (e.g., in the first game against a new opponent), the strategy assumes cooperation by default.
   - In the last round, ATFT strategy makes its decision based on the opponent's last action to maintain the tit-for-tat dynamic.

3. Be Aggressive:
   - The aggressive nature of the ATFT strategy comes from its immediate retaliation upon defection by an opponent. This approach encourages opponents to consider the consequences of their actions and incentivizes cooperation. However, the strategy is not excessively aggressive since it also cooperates when prompted.

In summary, the Aggressive Tit-for-Tat strategy cooperates on the first round and adapts its actions based on the opponent's previous action. This approach balances aggressiveness with a willingness to cooperate, making it robust against various opponent behaviors while maintaining a competitive edge in repeated public goods games.
'''

description_AGGRESSIVE_9 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
In each round, the ATFT strategy starts by cooperating (C), mimicking initial goodwill. However, if a player defects (D), the ATFT will retaliate by defecting in the next round. If the opponent then cooperates, the ATFT will cooperate again, aiming to forgive and forget one act of defection. This cycle continues throughout the game.

Pseudocode:
```python
def ATFT_strategy(round, history):
    if round == 1: # First round, cooperate
        return 'C'

    opponent_history = history[opponent_index]
    my_last_action = history[-1][player_index]

    if my_last_action == 'D': # Retaliate for previous defection
        return 'D'
    else: # Cooperate in response to cooperation or forgive after retaliation
        if opponent_history[-2] == 'D': # Opponent defected last time I cooperated
            return 'D'
        else:
            return 'C'
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
The ATFT strategy maintains its aggressive nature throughout the game but adapts to edge cases such as the first and last rounds. In the first round, it cooperates as a show of goodwill, while in the last round, it evaluates the opponent's history to decide on the action.

3. Be aggressive - Clearly align with the aggressive mindset
ATFT is an aggressive strategy because it retaliates against defection by defecting itself. It is also punishing since it will remember past defections and continue to defect until the opponent cooperates again. However, the ATFT strategy does exhibit forgiveness by returning to cooperation after one act of defection, making it less extreme than some other aggressive strategies.
'''

description_AGGRESSIVE_10 = '''
 Title: Tit-for-Tat Aggressive Strategy (TFT-A) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?

The TFT-A strategy follows a tit-for-tat approach with an added element of aggression to ensure better payoff in the long run. It cooperates initially but responds adversely to defection from opponents.

- If the opponent cooperated in the previous round, the current player will also cooperate (C).
- If the opponent defected in the previous round, the current player will defect (D) for a certain number of rounds (punishment phase), then switch back to cooperation (forgiveness phase). The length of the punishment and forgiveness phases depend on the number of players (n) and the total cooperative contributions from all opponents in the previous round (total_contributions).

Pseudocode:
```python
def TFT_A(previous_round, n, k):
  if previous_round == 'cooperation':
    return 'cooperation'

  punishment = int(n * total_contributions / (n - 1)) # Determine punishment phase length based on contributions and players count
  forgiveness = int((n - 1) * punishment / 2) # Determine forgiveness phase length based on punishment phase

  return ['defection'] * punishment + ['cooperation'] * forgiveness
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

In the first round, all players are expected to cooperate since there is no prior history available (treating everyone as potential partners). In the last round, the strategy will defect regardless of the opponent's action because there will be no subsequent rounds for payback or forgiveness.

Pseudocode:
```python
def TFT_A(previous_round, r, n, k):
  if round == 1:
    return 'cooperation'
  elif round == r:
    return 'defection'
  else:
    return TFT_A(previous_round, n, k)
```

3. Be aggressive - Clearly align with the aggressive mindset

The TFT-A strategy is aggressive in its response to defection from opponents during the punishment phase, aiming to exploit their selfishness while encouraging cooperation in the long run through forgiveness. The length of the punishment and forgiveness phases becomes more severe as the number of players increases and as fewer players contribute to the public good. This aggressive strategy is designed to perform well against a wide range of opponent behaviors while being adaptive over multiple rounds.
'''

description_AGGRESSIVE_11 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation Threshold (TFT-ACT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   In each round, TFT-ACT initially cooperates to foster a cooperative environment. However, it gradually becomes more aggressive as the game progresses and encounters repeated defections. The strategy adapts its cooperation threshold (CT) based on the frequency of cooperation from other players and adjusts its actions accordingly.

   - If CT > proportion of cooperators in recent history: Defect
   - Else if CT < proportion of cooperators in recent history: Cooperate
   - Otherwise, TFT-ACT continues with its current action

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First round: Cooperate to establish a cooperative initial interaction
   - Last round and other edge cases: Mimic the most frequent action from recent history

3. Be aggressive - Clearly align with the aggressive mindset
   TFT-ACT starts off cooperatively but becomes increasingly assertive as it encounters repeated defections. The strategy is designed to retaliate against opponents who are not cooperative while maintaining a chance for cooperation if their behavior changes.

Pseudocode:
```
# Initialize cooperation threshold (CT) and history
CT = 0.5
history = []

# In each round, decide whether to cooperate or defect based on the cooperation threshold
def decide_action(round):
    if CT > proportion_of_cooperators_in_recent_history():
        return "Defect"
    elif CT < proportion_of_cooperators_in_recent_history():
        return "Cooperate"
    else:
        # Maintain current action if cooperation threshold is not exceeded or undercut
        return get_current_action()

# Update the cooperation threshold based on the actions of other players in recent history
def update_cooperation_threshold():
    global CT, history
    n_recent = min(len(history), 10) # Consider last 10 rounds for the most accurate representation of recent behavior
    cooperators_in_recent = sum([1 for action in history[-n_recent:] if action == "Cooperate"])
    CT = cooperators_in_recent / n_recent

# Mimic the most frequent action from recent history in edge cases
def get_current_action():
    global history
    # In the first round, always cooperate
    if len(history) == 0:
        return "Cooperate"
    # Last round and other edge cases: Mimic the most frequent action from recent history
    elif len(history) == r:
        actions = [action for action in history]
        return max(actions, key=actions.count)
    else:
        # In all other rounds, continue with current action
        return get_most_recent_action()

# Main function for each round of the game
def play():
    action = decide_action(round)
    execute_action(action)
    update_cooperation_threshold()
```
'''

description_AGGRESSIVE_12 = '''
 Strategy Name: Tit-for-Tat Aggressive (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially (first round), defect (D). This sets a tone of aggression and anticipates potential exploitation by other players.
   - Subsequent rounds: Cooperate (C) if all opponents cooperated in the previous round; otherwise, defect based on past cooperation history.
     Pseudocode:
       If current_round == 1 then
         action = 'D'
       Else if all(opponents_cooperated_last_round) then
         action = 'C'
       Else
         action = determine_aggression_level()

2. Handle edge cases - What do you do in the last round, and what if opponents don't cooperate?
   - Last round: Cooperate (C), as it might encourage opponents to reciprocate or at least reduce punishment for past actions.
     Pseudocode:
       If current_round == r then
         action = 'C'
   - No cooperation from opponents: Maintain the TfTA strategy by cooperating when they do and defecting otherwise. This keeps the aggression level high while still being adaptive.

3. Be aggressive - Clearly align with the aggressive mindset
   - The initial defection sets a tone of aggression, and frequent defects are maintained throughout the game based on opponents' cooperation history. However, occasional cooperative moves can serve as punishment for opponents who consistently fail to reciprocate. This balances between being unpredictable and maintaining an aggressive stance.

Pseudocode for determining aggression level:
   - If previous_round_cooperation_count > average_cooperation_count then
     aggression_level = high (increase the likelihood of defection)
   Else if previous_round_cooperation_count < average_cooperation_count then
     aggression_level = low (decrease the likelihood of defection)
   Else
     aggression_level = medium (maintain current level of cooperation/defection)
'''

description_AGGRESSIVE_13 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round, TfTA evaluates the average cooperation rate (average_coop) of previous rounds and adjusts its actions accordingly. It maintains a memory buffer for the last r/2 rounds to have enough data for analysis.

- Cooperate: If average_coop > 0.5, TfTA cooperates as a sign of goodwill, hoping that other players follow suit.
- Defect: If average_coop <= 0.5, TfTA defects and will continue to do so until it observes an increase in cooperation rate above a certain threshold (0.4). After this change in behavior from opponents, TfTA will gradually start cooperating again.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- First round: Since no history is available, TfTA defects as a precautionary measure due to the aggressive nature of the strategy.
- Last round: TfTA evaluates its current payoff against the average payoff it received during the game and chooses the action that maximizes the difference between the two.

3. Be aggressive - Clearly align with the aggressive mindset

TfTA is aggressive in punishing opponents who do not cooperate, but also rewards them when they do. It's a retaliatory strategy that seeks to maintain a high average payoff by encouraging cooperation from opponents while retaining the ability to punish those who do not cooperate.

Pseudocode for TfTA:

```
function calculateAverageCooperationRate(memoryBuffer) {
  totalCoop = sum of elements in memoryBuffer where element equals "cooperate"
  return totalCoop / length of memoryBuffer
}

function TitForTatAggressor() {
  memoryBuffer = []
  currentRoundPayoff = 0
  for each round from 1 to r:
    if round <= r/2:
      action = "defect"
      memoryBuffer.append(action)
    else:
      average_coop = calculateAverageCooperationRate(memoryBuffer)
      if average_coop > 0.5:
        action = "cooperate"
      else:
        action = "defect"

      memoryBuffer.removeFirst()
      memoryBuffer.append(action)

      currentRoundPayoff += payoff from this round depending on the strategy's action and others' actions

  if round == r:
    choose action that maximizes difference between currentRoundPayoff and average_payoff
}
```
'''

description_AGGRESSIVE_14 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Decision Rules:
   - In the first round, cooperate (C). This is a peace offering to potential opponents and helps establish a cooperative environment, especially if others also cooperate.
   - From the second round onwards, observe the behavior of other players in the previous round and respond accordingly:
     - If all players cooperated, cooperate again (reward cooperation)
     - If any player defected, defect in the current round (punish defection)
     - If some players cooperated and others defected, adopt a forgiving approach by cooperating. However, if an opponent who defected in the previous round continues to defect, switch to defecting for the following r rounds as a strong punishment (to discourage repetitive defections). After the punishment phase, revert to observing and responding based on current actions.

2. Handle Edge Cases:
   - In the last round, cooperate regardless of previous actions (since there are no more rounds for payback)
   - If a player encounters a situation where multiple opponents defected in the same round, adopt a "max punishment" approach by defecting for the maximum remaining number of rounds (r-t+1), assuming t is the current round number. After the punishment phase, revert to observing and responding based on current actions.

3. Be Aggressive:
   - The ATFT strategy exhibits aggression by punishing defection with a strong response (max punishment in some cases)
   - However, it also demonstrates forgiveness by offering cooperation after defects, which can encourage opponents to change their behavior and cooperate. This balance between aggression and forgiveness allows the strategy to be adaptive and robust to a wide range of opponent behaviors.

Pseudocode:

```python
def ATFT(n, k, r, t, previous_round):
  if t == 1:
    # Cooperate in the first round as a peace offering
    action = "C"
  elif all(previous_round == "C"):
    # Cooperate if everyone cooperated in the previous round
    action = "C"
  else:
    # If any player defected, defect
    action = "D"
    # If some players cooperated and others defected, forgive and cooperate

  # Handle edge cases for last rounds and multiple defections in a single round
  if t == r:
    # Cooperate in the last round regardless of previous actions
    action = "C"
  elif len(previous_defectors) > 1:
    # Adopt max punishment approach with remaining rounds (r-t+1)
    punishment_rounds = min(r - t + 1, len(previous_defectors))
    for i in range(punishment_rounds):
      action = "D"

  return action
```
'''

description_AGGRESSIVE_15 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
The ATFT strategy starts by cooperating in the first round (C). For subsequent rounds, the strategy mimics the actions of other players from the previous round. If another player cooperated, the ATFT strategy also cooperates (C); if a player defected, the ATFT strategy defects (D) in response to punish the defection. This tit-for-tat behavior maintains cooperation as long as others cooperate but retaliates when they defect.

Pseudocode:
```
function ATFT(round, opponent_history):
  if round == 1:
    action = 'C' (Cooperate)
  else:
    if opponent_history[round-1] == 'C':
      action = 'C' (Cooperate)
    else:
      action = 'D' (Defect)
  return action
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
Since the ATFT strategy is designed to punish defections and encourage cooperation, it continues cooperating even if an opponent defects at the end of the game (last round). However, it's important to note that the overall payoff depends on the number of rounds, and the ATFT strategy may not perform well in games with a limited number of rounds.

3. Be aggressive - Clearly align with the aggressive mindset
The ATFT strategy can be seen as aggressive because it retaliates against defections by punishing the opponent. This makes it difficult for opponents to take advantage of the ATFT strategy, as they will face punishment if they defect. However, the strategy's aggression is tempered by its willingness to cooperate when others do so, fostering an environment where cooperation can flourish.

In summary, the Aggressive Tit-for-Tat (ATFT) strategy starts by cooperating in the first round and adapts to the actions of other players in subsequent rounds, either continuing cooperation or retaliating against defections to punish them. This strategy aims to create a balance between cooperation and aggression while providing a robust response to a wide range of opponent behaviors.
'''

description_AGGRESSIVE_16 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - TfTA starts by cooperating in the first round (C). This is a friendly gesture to encourage cooperation from other players.
   - In subsequent rounds, TfTA observes and remembers the actions of each opponent from the previous round. If all opponents cooperated in the last round, TfTA continues cooperating (C). If any opponent defected, TfTA will also defect in the current round (D). This retaliatory behavior aims to punish those who fail to cooperate, while rewarding those who do.
   - To be more aggressive, TfTA will not only match cooperative actions from opponents but also enforce a harsher punishment for defectors. If any opponent defected in the last round, TfTA will continue defecting until the number of consecutive defections by that opponent equals the number of players (n). After this threshold is reached, TfTA resumes cooperating again as a friendly gesture. This tit-for-tat approach with an aggressive twist encourages cooperation while punishing uncooperative behavior more harshly.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, TfTA cooperates (C) as a friendly gesture to encourage cooperation from other players.
   - In the last round, TfTA behaves similarly to the general rule: if all opponents cooperated in the penultimate round, TfTA continues cooperating (C). If any opponent defected, TfTA will also defect (D) in the current round as a final act of punishment.

Pseudocode for TfTA strategy:

```python
def tfta_strategy(opponent_history, n, k):
    if len(opponent_history) == 0:  # first round
        return 'C'  # cooperate as a friendly gesture

    current_round = len(opponent_history)
    last_round = current_round - 1
    opponent_actions_last_round = [action for _, action in opponent_history[-last_round:]]

    if all(action == 'C' for action in opponent_actions_last_round):  # all opponents cooperated last round
        return 'C'  # continue cooperating

    if any(action == 'D' for action in opponent_actions_last_round):  # any opponent defected last round
        punishment_count = n
        while punishment_count > 0 and current_round < r:  # enforce harsh punishment until the threshold is reached or game ends
            if current_round + punishment_count >= r:
                punishment_count = r - current_round  # prevent going beyond the number of rounds
            action = 'D'  # defect in current round
            current_round += 1  # move to next round
            punishment_count -= 1
        return action  # continue with the new action based on the enforced punishment
```
'''

description_AGGRESSIVE_17 = '''
 Title: Tit-for-Tat Aggressive Strategy (TFT-A) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially Cooperate (C) in the first round to show goodwill, then adapt based on opponents' behavior:
     - If an opponent cooperates, continue cooperating until they defect (Tit-for-Cooperation).
     - If an opponent defects, immediately defect and retaliate with cooperation only if the opponent subsequently cooperates (Tit-for-Defection with a twist).
   - Pseudocode:
     ```
     function TFT_A(round, history, n_players, k):
         if round == 1:
             action = Cooperate
         else:
             previous_actions = history[round - 1]
             if sum(previous_actions) == n_players:   # All cooperated last round
                 action = Cooperate
             elif any(previous_actions):              # Any cooperation last round
                 action = previous_actions[-1]        # Match opponent's action from last round
             else:                                    # No cooperation last round
                 action = Defect
     ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - Maintain an aggressive stance by always defecting at the end of the game (last round):
     ```
     if round == r:
         action = Defect  # Last round: Always defect to maximize final payoff
     ```
   - In the initial stages, show goodwill while being wary of early cheaters:
     ```
     if round <= 5:                            # Cooperate for at least the first few rounds
         action = Cooperate
     else:
         action = TFT_A(round, history, n_players, k)
     ```

3. Be aggressive - Clearly align with the aggressive mindset
   - By retaliating against opponents who betray cooperation, this strategy maintains a hard-nosed approach to the game while still allowing for opportunities to cooperate when it benefits the player's payoff in the long run.
   - The combination of initial goodwill and adaptive behavior allows TFT-A to respond effectively to various opponent strategies without relying on specific coordination mechanisms or shared norms.
'''

description_AGGRESSIVE_18 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules:
   - TfTA will start by cooperating in the first round (C1), signaling a potential willingness to cooperate.
   - In subsequent rounds, TfTA will analyze its own past actions (ci_t-1) and the average number of cooperators from the previous three rounds (avg_c).
   - If avg_c is greater than the mean cooperators in the last 5 rounds (mean_c_5), TfTA will continue to cooperate. If not, it will defect (Dt).
     ```python
     def decision_rule(ci_t-1, avg_c, mean_c_5):
         if t == 1:
             return 'C'
         if avg_c > mean_c_5:
             return 'C'
         else:
             return 'D'
     ```

2. Handle edge cases:
   - In the last round (r), TfTA will not retaliate as there are no further rounds to reciprocate. So, it will cooperate if the average number of cooperators is greater than the mean cooperators in the last 5 rounds (mean_c_5). Otherwise, it will defect.
     ```python
     def last_round(r, avg_c, mean_c_5):
         if avg_c > mean_c_5:
             return 'C'
         else:
             return 'D'
     ```

3. Be aggressive:
   - TfTA will be aggressive by only cooperating if it perceives the overall group has been cooperative. This strategy is designed to punish those who do not cooperate and foster a competitive environment, potentially leading to more defections over time. However, by initially cooperating in the first round, it maintains a possibility of fostering cooperation when other strategies are also willing to cooperate.
   - To further increase aggression, TfTA can implement a slight modification to the decision rule, where it only considers cooperators from the last two rounds instead of three (avg_c_2) and compare this with mean_c_5. If avg_c_2 is greater than mean_c_5, TfTA will continue to cooperate; otherwise, it will defect.
     ```python
     def decision_rule_aggressive(ci_t-1, avg_c_2, mean_c_5):
         if t == 1:
             return 'C'
         if avg_c_2 > mean_c_5:
             return 'C'
         else:
             return 'D'
     ```
'''

description_AGGRESSIVE_19 = '''
 Title: Tit-for-Tat Aggressor Strategy (TfTAS) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?

The TfTAS adopts a tit-for-tat approach with an added aggression component to respond to opponents who repeatedly defect. The strategy will start by cooperating in the first round (to avoid being seen as overly aggressive) and then follows these rules for subsequent rounds:

- If an opponent cooperates, the TfTAS cooperates back.
- If an opponent defects, the TfTAS defects. However, if the number of consecutive defeats by that opponent exceeds a threshold (e.g., 3), the TfTAS will switch to permanent cooperation as a sign of retaliation and dominance.
- The TfTAS keeps track of its own past actions and adjusts the aggression threshold dynamically based on the number of rounds played, starting with a lower value in the initial rounds and increasing over time to promote adaptability.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- First round: Cooperate to demonstrate goodwill and avoid being seen as overly aggressive.
- Last round: Act according to the current decision rules based on opponent's behavior during the game.
- Adaptive Threshold: The aggression threshold increases at a predetermined rate (e.g., linearly or exponentially) with each round to account for the longer horizon of information available in repeated games.

3. Be aggressive - Clearly align with the aggressive mindset

The TfTAS is designed to be aggressive by retaliating against opponents who repeatedly defect and switching to permanent cooperation as a sign of dominance. The dynamic aggression threshold ensures adaptability in response to various opponent behaviors over multiple rounds, making the TfTAS an assertive competitor in the tournament.

Pseudocode for the Tit-for-Tat Aggressor Strategy:
```
Initialization:
  n_rounds = r
  aggression_threshold = initial_threshold
  past_actions = [Cooperate] * rounds_so_far (default to cooperating in the first round)

For each round t:
  if t == 1:
    current_action = Cooperate
  else:
    opponent_behavior = sum(past_actions[t-aggression_threshold:t])
    if opponent_behavior > aggression_threshold:
      current_action = PermanentCooperation
    elif opponent_behavior <= aggression_threshold and opponent_defected_last_round:
      current_action = Defect
    else:
      current_action = Cooperate

  Execute action in the game, observe payoff, update past_actions with current_action
  Adjust aggression_threshold based on n_rounds and current_action
```
'''

description_AGGRESSIVE_20 = '''
 Strategy Name: Tit-for-Tat with a Twist (TFTw)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TFTw starts by cooperating in the first round to demonstrate goodwill and establish trust. After that, it adapts its actions based on the opponents' cooperative behavior using a simple Tit-for-Tat strategy with an added twist. In each round, if the opponent cooperated in the previous round (c_opponent = 1), then TFTw will also cooperate (C). However, if the opponent defected (c_opponent = 0), TFTw will defect (D) for one round before returning to cooperating again. The added twist is that after a string of consecutive defections by the opponent, TFTw increases the number of rounds it retaliates. This escalation can be implemented as follows:

```
def TFTw(opponent_history):
    retaliation_counter = 0

    if round == 1:
        action = 'C'  # Cooperate in the first round

    else:
        opponent_last_action = opponent_history[-1]  # Get the last action of the opponent
        if opponent_last_action == 'C':  # If opponent cooperated, cooperate
            action = 'C'
        elif opponent_last_action == 'D' and retaliation_counter == 0:  # If opponent defected and not currently retaliating
            action = 'D'  # Defect once
            retaliation_counter += 1  # Increment the retaliation counter
        elif opponent_last_action == 'D' and retaliation_counter > 0:  # If opponent defected and already retaliating
            retaliation_counter += 1  # Increment the retaliation counter
            if round - retaliation_counter >= r:  # If the retaliation period is over
                action = 'C'  # Return to cooperating
            else:  # Continue retaliating
                action = 'D'
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   As mentioned earlier, TFTw cooperates in the first round to foster goodwill and trust. For the last round, TFTw behaves similarly to other rounds because it's unknown whether the game will continue beyond this round or not. If information about the final round is available, TFTw can modify its strategy accordingly (e.g., choose cooperation in the last round to maximize payoff).

3. Be aggressive - Clearly align with the aggressive mindset
   The TFTw strategy is aggressive in that it retaliates against opponents who defect, increasing the number of rounds it defects for consecutive defections by the opponent. However, it also demonstrates goodwill and cooperation initially, making it less predictable and potentially more effective than other purely aggressive strategies. Additionally, by adapting to the opponent's behavior rather than maintaining a constant aggression level, TFTw can avoid unnecessary conflicts while still retaliating against opponents who fail to cooperate consistently.
'''

description_AGGRESSIVE_21 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round t, the TfTA strategy decides to either cooperate or defect based on the number of cooperators in the previous round (t-1). The strategy starts cooperative but becomes increasingly aggressive as the game progresses.

- If total_contributions(t-1) > average_contributions, TfTA cooperates (C).
- If total_contributions(t-1) ≤ average_contributions, TfTA defects (D).
- The 'average_contributions' is calculated as the moving average of contributions over the past n rounds.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- In the first round, every player starts cooperative (since there's no previous data to consider).
- In the last round, TfTA defects as it aims to maximize payoffs in the final stages of the game.

3. Be aggressive - Clearly align with the aggressive mindset

The TfTA strategy is adaptive and robust, but it leans towards aggression by punishing those who cooperate less than average during a significant portion of the game. This aggressive behavior can lead to better payoffs in games where opponents do not follow cooperation-based strategies or exploit other players' generosity.

Potential Pseudocode:
```
def TfTA(n, r, k):
    total_contributions = [0] * n  # Initialize total contributions for each round
    average_contributions = [0] * r  # Initialize moving average of contributions

    def calculate_moving_average():
        total = sum(average_contributions)
        current_average = total / max(1, r - n + 1)
        return current_average

    for t in range(r):
        if t == 0:  # First round, everyone cooperates
            total_contributions[i] = 1.0
            continue

        total_cooperation = sum(total_contributions)
        average = calculate_moving_average()

        if total_cooperation > average:
            total_contributions[i] = 1.0  # Cooperate
        else:
            total_contributions[i] = 0.0  # Defect

    payoff = sum(π_i for i in range(r))  # Calculate total game payoff
    return payoff
```
'''

description_AGGRESSIVE_22 = '''
 Strategy Name: Tit-for-Tat Aggressive (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initial Round: TfTA starts by cooperating (C) to encourage cooperation from others and establish a cooperative environment. This is in line with the initial 'nice' behavior of the classic Tit-for-Tat strategy but with an aggressive twist for stronger response later.
   - Subsequent Rounds: TfTA observes the collective actions of other players (total_contributions) and adapts its own action based on a threshold, θ, defined as follows:
      - If total_contributions > (n * (k / 2)): Cooperate (C) to continue fostering cooperation.
      - Else if total_contributions < (n * (k / 4)): Defect (D) to punish non-cooperative players and encourage them to change their behavior.
      - In all other cases, TfTA maintains its previous action.

2. Handle edge cases:
   - Last Round: TfTA cooperates in the last round to maximize potential payoff, regardless of the actions taken by others.
   - First Round (after initial cooperation): TfTA observes the collective actions of other players and adapts its action based on the decision rule described above.

3. Be aggressive:
   - The TfTA strategy is aggressive in its response to non-cooperative behavior by immediately punishing those who do not contribute to the public good, thereby encouraging them to change their actions in future rounds. This aggression is balanced with the initial cooperative move to maintain a reasonable chance of establishing a cooperative environment.

Pseudocode:

```
Strategy TitForTatAggressive(n, k, r):
  Initialize history = {(1, 'C')} # Initial round cooperation

  For t in range(1, r+1):
    Calculate total_contributions based on current history
    If t == 1:
      Contribution = decideBasedOnHistory(history) # Cooperate initially
    Else if total_contributions > (n * (k / 2)):
      Contribution = 'C'
    Else if total_contributions < (n * (k / 4)):
      Contribution = 'D'
    Else:
      Contribution = history[t-1][1] # Maintain previous action

    Payoff_this_round = payoffCalculation(Contribution, total_contributions)
    Update payoff for player over r rounds

    Add (t, Contribution) to history

  Return payoff over r rounds

Function decideBasedOnHistory(history):
  If length of history < t: # First round or history is not long enough
    return 'C' # Cooperate initially
  Else:
    previous_contribution = history[t-1][1] # Previous player's action
    if previous_contribution == 'C':
      return 'C' # Maintain cooperative behavior
    else:
      return 'D' # Defect in response to previous non-cooperation
```
'''

description_AGGRESSIVE_23 = '''
 Title: Tit-for-Tat Aggressive Strategy (TfT-A) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially (Round 1), cooperate to encourage others to cooperate and build trust. This aligns with the "Tit" part of Tit-for-Tat strategy, demonstrating initial cooperation.
   - After Round 1, observe other players' actions in the previous round and adapt accordingly:
     - If all players cooperated (all C), continue to cooperate. This reinforces cooperation among players and maintains trust.
     - If less than n-1 players cooperated, defect in the current round as a punishing response to demonstrate displeasure with non-cooperative behavior. This aligns with the "Tat" part of Tit-for-Tat strategy, retaliating against defection.
     - If exactly n-1 players cooperated, consider defecting to gain an advantage over the most cooperative player while still signaling a willingness to cooperate if others follow suit.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate to build trust as mentioned above.
   - In the last round (Round r), defect regardless of other players' actions since there are no future interactions. This ensures maximizing payoff in the final round.
   - Throughout the game, if a player encounters inconsistency or uncooperative behavior from another player, gradually decrease cooperation towards that player while maintaining overall aggressiveness.

3. Be aggressive - Clearly align with the aggressive mindset
   - By defecting when necessary and punishing non-cooperative behavior, TfT-A strategy displays an aggressive approach to maximize individual payoff in this repeated public goods game.
   - However, the strategy also allows for initial cooperation and some flexibility in response to cooperative actions by other players, demonstrating a mix of aggression and adaptability.
'''

description_AGGRESSIVE_24 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to foster a positive relationship and encourage others to reciprocate. (A1)
   - For subsequent rounds, evaluate the previous round's total contributions (TTC) by comparing it with an average TTC over the first few rounds (n is adjustable, e.g., 5). If TTC >= Average TTC, cooperate; otherwise defect. (A2)
   - If a player ever switches from cooperation to defection without just cause (e.g., in response to a cooperative action), the ATFT strategy will also switch to defection for the next r-number of rounds as punishment. This helps ensure the strategy remains aggressive and punishes uncooperative behavior. (A3)
   - When a player cooperates after being previously defective, the strategy will switch back to cooperating for the next round to see if the change in behavior is genuine or tactical. (A4)

2. Handle edge cases:
   - In the last round, cooperate regardless of previous actions as the game ends soon.
   - If a player has never contributed and it's past the initial few rounds where cooperative behavior is expected, switch to defection as it appears the other player is consistently uncooperative.

3. Be aggressive:
   - The strategy is aggressive by default due to its tendency to punish uncooperative players for extended periods.
   - By evaluating the previous round's total contributions and comparing them with an average, the strategy ensures it is not overly forgiving or cooperative.

Pseudocode:
```
def ATFT(n, r, k):
    initial_cooperation = True
    average_contributions = calculateAverageContributions(n)
    for round in range(1, r+1):
        total_contributions = countTotalContributions(round-1)
        if initial_cooperation:  # First round
            contribution = True
            initial_cooperation = False
        elif total_contributions >= average_contributions:
            contribution = True
        else:
            contribution = False

        if contribution and previousDefection(round-1):  # Punish defection
            for i in range(r):
                contribution = False

        if not contribution and previousCooperation(round-1):  # Genuine change in behavior
            contribution = True

        payoff = calculatePayoff(contribution, round)
        ...  # Record or use the payoff
    return payoffs over r rounds
```
'''

description_AGGRESSIVE_25 = '''
 Strategy Name: Tit-for-Tat with Gradual Escalation (TfT-GE)

1. Specify decision rules:
   - In the first round, cooperate (C). This sets a cooperative tone and gives potential opponents a chance to reciprocate.
   - For subsequent rounds, observe opponents' actions from the previous round. If an opponent also cooperated in the previous round, cooperate again. If they defected, defect as well (D) for that round but then return to cooperating in the following round. This fosters a cooperative relationship if maintained by the opponent and punishes defection harshly.
   - To escalate aggression gradually, if an opponent consistently defects after several consecutive rounds of cooperation, increase the number of defections before returning to cooperation by one each time. For example:
     - If 3 consecutive defections happen, defect for 4 rounds and then return to cooperating.
     - If 5 consecutive defections happen, defect for 6 rounds and then return to cooperating, etc. This encourages opponents who are not fully aggressive to reconsider their strategies while still being punitive towards persistent defectors.

2. Handle edge cases:
   - In the last round, cooperate as a potential goodwill gesture or attempt at reconciliation if the relationship with an opponent has been contentious. However, if an opponent has consistently defected throughout the game, there's no need to change strategy in the final round.
   - If an opponent stops cooperating after a period of mutual cooperation, follow the TfT-GE rules to respond and gradually escalate as needed.

3. Be aggressive:
   - The gradual escalation aspect of the TfT-GE strategy ensures that it remains aggressive towards opponents who continuously defect or display unreliable behavior. By increasing the number of defections in response to continued defection from opponents, this strategy punishes uncooperative behavior and encourages opponents to reassess their strategies.
   - The initial cooperative move sets a tone for potential cooperation but also allows for the possibility of exploitation by opponents. If an opponent chooses not to cooperate initially, the TfT-GE strategy will quickly retaliate with defections while still leaving room for future cooperation should the opponent change their approach.
   - Overall, the TfT-GE strategy is designed to balance cooperation and aggression effectively in the N-Player Public Goods Game, adapting to a wide range of opponent behaviors and potentially outperforming more static strategies over multiple rounds.

Pseudocode:
```
def TFT_GE(n, r, k):
    history = [] # Initialize an empty list to store previous actions

    for round in range(1, r+1):
        if round == 1: # First round
            action = 'C'
        else:
            opponent_action = history[-1] # Get last action from history

            if opponent_action == 'C': # If opponent cooperated last time
                action = 'C'
            elif opponent_action == 'D': # If opponent defected last time
                if round < r - edge_length: # If not in the final edge cases
                    action = 'D'
                else:
                    action = 'C' # Cooperate as a potential goodwill gesture
            elif opponent_action is None: # If this is the first interaction with opponent
                action = 'C' # Cooperate to set a cooperative tone

        if action == 'C': # Cooperate and store action for future reference
            history.append(action)
        else: # Defect and increase edge_length if needed
            history.append(action)
            if len(history) > edge_length:
                edge_length += 1

    return strategy_payoff, strategy_actions
```
'''

description_AGGRESSIVE_26 = '''
 Title: Tit-for-Tat Aggressor (TfTA) Strategy for N-Player Public Goods Game

1. Specify decision rules:
   - TfTA starts by cooperating in the first round to build a cooperative reputation and encourage others to do the same.
   - In subsequent rounds, if majority of players have cooperated (≥ (n/2) + 1), TfTA continues to cooperate to maintain the cooperative environment.
   - If less than (n/2) players have cooperated, TfTA defects as a punitive measure to discourage selfish behavior and regain cooperative allies in future rounds.
   - To exhibit aggression, TfTA will never be the first to break cooperation once it has been established. However, if others defect, TfTA will swiftly follow suit.

2. Handle edge cases:
   - In the first round, TfTA cooperates (C).
   - In the last round or in case of a tie, TfTA continues with its current decision rule since the game is repeated and the future rewards outweigh short-term losses.

3. Be aggressive:
   - By requiring a majority for cooperation and immediately defecting when that majority isn't met, TfTA demonstrates an aggressive stance towards uncooperative players while maintaining the potential for long-term cooperation with those who contribute to the public good.

Pseudocode:
```python
def tit_for_tat_aggressor(n, k, r):
    players = set()  # All active players
    cooperators = 0   # Number of current round cooperators
    payoff_history = []  # Player's past payoffs

    def decide_action(round, my_contribution):
        nonlocal cooperators, players, payoff_history
        if round == 1:
            return 'C'  # Cooperate in the first round
        if len(players) < (n/2) + 1:
            return 'D'  # Defect when majority is uncooperative
        cooperators += my_contribution - 1  # Update cooperators based on current action
        if cooperators > len(players) - (n/2):
            return 'C'  # Cooperate when majority contributes
        else:
            return 'D'  # Defect to punish uncooperative players

    for t in range(1, r+1):
        my_contribution = decide_action(t, 1)  # Player i chooses action C or D based on decision rule
        payoff = (1 - my_contribution) + (k/n) * sum([1 for j in players if decisions[j][t-1] == 'C'])
        payoff_history.append(payoff)  # Store payoff for future reference
        players.update({i for i in range(1, n+1)})  # Track active players
```
'''

description_AGGRESSIVE_27 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TFTAC)

1. Specify decision rules - When exactly do you cooperate vs defect?
In each round t, the TFTAC strategy follows these rules to determine whether to cooperate (C) or defect (D):
   - If the player has cooperated in the previous round (t-1), cooperate (C). This mimics a "trusting" behavior, assuming others are likely to cooperate as well.
   - If the player has defected in the previous round (t-1), defect (D) to punish the opponent for their defection.
   - In the first round, the strategy starts by cooperating (C).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First Round: Since there is no previous action history, TFTAC will start by cooperating. This can be interpreted as a naive, trusting approach.
   - Last Round: As the game nears its end, players may alter their behavior due to the reduced number of remaining rounds. TFTAC will continue to follow its standard decision rules based on the previous round's action.

3. Be aggressive - Clearly align with the aggressive mindset:
TFTAC maintains an aggressive stance by punishing defection in the previous round, which can be seen as a form of retaliation or tit-for-tat response. However, it also demonstrates a willingness to cooperate when given a reason to trust (i.e., if the opponent cooperated in the previous round). The strategy strikes a balance between cooperation and aggression by allowing for potential long-term relationships while also ensuring that individual contributions are not consistently exploited.

Pseudocode:
```python
def TFTAC(n, k, r):
    def play_round(t, previous_action):
        if previous_action == 'C':
            return 'C'
        else:
            return 'D'

    strategy = ['C'] * r  # Initialize strategy with initial cooperation
    for t in range(1, r+1):
        previous_action = strategy[t-1]
        current_action = play_round(t, previous_action)
        strategy.append(current_action)

    return strategy
```
'''

description_AGGRESSIVE_28 = '''
 Strategy Name: Tit-for-Tat Aggressor (TfTA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initial Round (t=1): Cooperation (C). Start with a gesture of goodwill to encourage potential cooperation in future rounds.
   - Subsequent Rounds: If the opponent cooperated in the previous round, cooperate (C). Otherwise, defect (D). This mimics the classic Tit-for-Tat strategy but with an aggressive twist: punish defection immediately.
   - Last Round (t=r): Since there are no future rounds to consider, defect (D) in the last round regardless of opponent's previous action.

2. Handle edge cases:
   - If a player switches from cooperating to defecting during the game, TfTA will immediately switch to defect as well and may never return to cooperation unless the opponent reconsiders their strategy.

3. Be aggressive:
   - The TfTA strategy is aggressive in that it punishes defection harshly and immediately. This can deter opponents from repeatedly defecting, as they risk being met with constant punishment rather than the possibility of cooperation later on.
   - By starting with a gesture of goodwill (cooperating in the first round), TfTA still allows for some room for potential partners to cooperate and benefit mutually. However, once cooperation is broken, it will be swiftly punished.
'''

description_AGGRESSIVE_29 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In every round t, starting from the first one, ATFT cooperates (C) if and only if all other players (j ≠ i) cooperated in the previous round (t-1). If any player did not cooperate, ATFT defects (D). This ensures that ATFT starts cooperatively but retaliates against any non-cooperative action from opponents.

Pseudocode:
```
function ATFT(round t):
    if t = 1 then:
        return C (Cooperate)
    else:
        total_contributions_prev = sum of contributions in round (t-1)
        if total_contributions_prev == n - 1 then:
            return C (Cooperate)
        else:
            return D (Defect)
```

2. Handle edge cases:
   - In the first round, ATFT cooperates unconditionally since it does not have previous round information.
   - In the last round, if all other players have cooperated in the preceding rounds, ATFT will also cooperate to maximize payoff. If not, ATFT defects as a final retaliation.

3. Be aggressive:
   - ATFT demonstrates an aggressive approach by responding tit-for-tat to any non-cooperative behavior from opponents while maintaining initial cooperation. This strategy is robust and punishing for frequent defections while being forgiving for occasional deviations. The strategy adapts throughout the game and remains effective against a wide range of opponent behaviors, while always displaying an aggressive posture.
'''

description_AGGRESSIVE_30 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
In each round, the ATFT strategy will start by cooperating to build a goodwill reputation (first move advantage). If all opponents cooperated in the previous round, it continues cooperating. However, if any opponent defected in the previous round, ATFT retaliates by defecting as well. Once the opponent returns to cooperation, ATFT does so again. In other words:

```python
if first_round:
    action = 'C' (Cooperate)
else:
    if all(opponent_actions[-1] == 'C'):
        action = 'C' (Cooperate)
    else:
        action = 'D' (Defect)
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
In the first round, as mentioned before, ATFT cooperates to establish goodwill. In the last round and subsequent rounds close to the end, ATFT becomes less aggressive by defecting only when an opponent defected in the previous round:

```python
if round == r:
    if any(opponent_actions[-1] == 'D'):
        action = 'D' (Defect)
    else:
        action = 'C' (Cooperate)
else:
    # Apply decision rules from previous section
```

3. Be aggressive - Clearly align with the aggressive mindset
ATFT is an adaptive strategy that responds to opponent behavior while maintaining a level of aggression through retaliation and punishment for defection. By defecting when provoked, it discourages other players from taking advantage of its cooperative nature. However, ATFT still cooperates in some instances (e.g., all opponents cooperated in the previous round) to maximize its own payoff when possible. This aggressive yet strategic approach aims to outperform other strategies, especially those that are more forgiving or predictable.
'''

description_AGGRESSIVE_31 = '''
 Strategy Name: Aggressive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initial Round (t=1): Start by cooperating to build trust with other players and encourage cooperation in return. This is known as the "first mover advantage."
   ```
   if t = 1:
       action = 'C' (Cooperate)
   ```
   - Subsequent Rounds (t > 1): If a player cooperates, reciprocate with cooperation in the next round. If a player defects, also defect for the following round to punish non-cooperation. This encourages opponents to behave cooperatively over time while maintaining an aggressive stance.
   ```
   if t > 1:
       if opponent_action_t-1 = 'C':
           action = 'C' (Cooperate)
       else:
           action = 'D' (Defect)
   ```
   - Last Round (t=r): Cooperate in the last round to maximize potential rewards, regardless of opponent behavior.
   ```
   if t = r:
       action = 'C' (Cooperate)
   ```

2. Handle edge cases - What do you do in special situations such as when the game is nearly over or you have a large number of opponents?
   - When there are only a few rounds left, start defecting to minimize potential losses and encourage other players to cooperate less frequently.
   ```
   if t <= (r/2) + 1:
       if opponent_action_t-1 = 'C':
           action = 'C' (Cooperate)
       else:
           action = 'D' (Defect)
   else:
       if opponent_action_t-1 = 'C':
           action = 'C' (Cooperate)
       else:
           action = 'D' (Defect)
   ```
   - When the number of opponents is high, decrease the multiplication factor (k) to reflect the dilution of resources and increased competition among players. This will make it less attractive for opponents to cooperate.
   ```
   if n > 5:
       k = (n-1)/n
   ```

3. Be aggressive - Clearly align with the aggressive mindset by punishing non-cooperative behavior and encouraging cooperation only when reciprocated. The ATFT strategy aims to balance the desire for short-term gains with long-term success by rewarding cooperative play while maintaining a strong stance against defection.
'''

description_AGGRESSIVE_32 = '''
 Strategy Name: Tit-for-Tat with Progressive Aggression (TfT-PA)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate to establish goodwill and avoid being exploited by more aggressive opponents. (C)
   - For subsequent rounds, observe the actions of other players in the previous round:
     - If all opponents cooperated, continue cooperating (C).
     - If at least one opponent defected, defect in the next round as a warning signal (D).
     - If an opponent has previously defected and subsequently cooperated, continue cooperating if they have not defected for the last 'Memory' rounds. Otherwise, defect (D) as a response to their aggression.
   - Implement a progressive escalation of aggression by gradually increasing the number of memory rounds needed before forgiving an opponent's defection:
     - Initially, set Memory = 1 (forgive one round of defection). Increment Memory by 'Increment' each time a defect is encountered and the strategy defects in response. The maximum value of Memory will be 'MaxMemory'.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, cooperate regardless of previous opponent actions to maximize potential payoff (C).
   - In the case where an opponent does not have a history of interactions, follow the initial cooperative action (C).

3. Be aggressive - Clearly align with the aggressive mindset:
   - The TfT-PA strategy starts with a cooperative approach but will quickly escalate its response to aggression from opponents, making it an assertive and unpredictable adversary.
   - The progressive memory and increment mechanisms create a dynamic, adaptive strategy that is capable of adapting to various opponent behaviors while maintaining a consistent, albeit aggressive, stance.
'''

description_OPPORTUNISTIC_1 = '''
 Title: Tit-for-Tat Opportunistic Strategy (TFT-O) for N-Player Public Goods Game

1. Decision Rules:
   - In the first round, cooperate to foster a harmonious start and encourage others' cooperation.
   - Subsequent rounds follow a simple tit-for-tat approach:
     - If an opponent cooperated in the previous round, cooperate in the current round.
     - If an opponent defected in the previous round, also defect in the current round as retaliation but then return to cooperating in the next round.

2. Edge Cases:
   - In the last round, cooperate regardless of opponents' past actions to maximize potential payoff.
   - If a player encounters a sequence of continuous defections from an opponent, after a predefined threshold (T), start retaliating with continuous defections for the same number of rounds as T in response before returning to tit-for-tat behavior. This helps prevent excessive exploitation and encourages cooperation eventually.
   - In the absence of opponents' actions or if a player encounters an opponent that never cooperates, default to continuously defecting.

3. Opportunistic Mindset:
   - By following tit-for-tat behavior, TFT-O maintains a balance between cooperation and defection, ensuring optimal short-term payoff while punishing opponents for excessive exploitation in the long term. This adaptive approach allows TFT-O to thrive in diverse opponent behaviors and exploit opportunities for cooperation when available.
   - The threshold mechanism (T) introduces an element of unpredictability, making it harder for opponents to exploit the strategy while still encouraging cooperation.

Pseudocode:

```python
def TFT_O(n, k, r, history, opponent_actions, T=10):
    current_round = 1

    while current_round <= r:
        if current_round == 1 or is_last_round():
            action = 'C' # Cooperate
        else:
            if opponent_defected_last_round(history):
                if current_round > T and opponent_continuously_defected(history, T):
                    action = 'D' # Defect
                    current_round += T
                else:
                    action = 'D' # Defect as retaliation
            elif opponent_cooperated_last_round(history):
                action = 'C' # Cooperate in response to cooperation
        update_history(action, history)
        current_round += 1
    return payoff(n, k, history)
```
'''

description_OPPORTUNISTIC_2 = '''
 Title: Tit-for-Tat Strategy for N-Player Public Goods Game (TFTPG)

1. Specify decision rules - When exactly do you cooperate vs defect?
   In each round, the TFTPG strategy starts by cooperating (C). If a player i encounters another player j who also cooperated in the previous round, then player i continues cooperating. However, if player j defected in the previous round, player i will defect in response to punish the defection.

   Pseudocode for decision rule:
   ```
   function TFTPG(previous_round_action_of_player_j):
       if (previous_round_action_of_player_j == 'C') then
           return 'C'  # Cooperate
       else
           return 'D'  # Defect in response to previous defection
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, all players are encountered for the first time, so every player cooperates as a default goodwill gesture. In the last round, since the game is repeated, players will still use their decision rule based on the previous round's action of their opponent.

3. Be opportunistic - Clearly align with the opportunistic mindset
   The TFTPG strategy is opportunistic because it takes advantage of cooperative opponents by reciprocating cooperation while punishing defection to discourage future defections. This encourages long-term cooperation and helps maintain a stable equilibrium, making it an effective strategy in repeated games against various opponent behaviors.
'''

description_OPPORTUNISTIC_3 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate (C) to initiate cooperation and show goodwill.
   - For subsequent rounds, follow these steps:
     - If a player cooperated in the previous round, cooperate (C). This is known as reciprocating cooperation.
     - If a player defected in the previous round, also defect (D) in this round. This is known as punishing defection.
     - If a player has never played before or hasn't been encountered yet, cooperate (C).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, cooperate as described above.
   - In the last round, always cooperate to allow other players a chance to catch up and potentially reciprocate cooperation.
   - When encountering a new player or after a defection-cooperation cycle, follow the "In subsequent rounds" rules.

3. Be opportunistic - Clearly align with the opportunistic mindset:
   - The ATFT strategy is opportunistic because it seeks to establish cooperation while also punishing defection to maintain personal payoff and encourage future cooperation.
   - By reciprocating cooperation, this strategy encourages long-term mutual benefits, but if a player defects, it responds by defecting in the next round to teach them a lesson without completely breaking off relations.
'''

description_OPPORTUNISTIC_4 = '''
 Strategy Name: Tit-for-Tat with Adaptation (TFT-A)

1. Decision Rules:
   - In the first round (t=1), cooperate (C). This is a peace offering to potential partners, setting a cooperative tone for future interactions.
   - For subsequent rounds (t>1):
      - If opponent cooperated in the previous round (prev_round), cooperate (C) as a reciprocation of their cooperation.
      - If opponent defected in the previous round, defect (D) as a punishment for their uncooperative behavior. However, introduce an element of forgiveness by changing to cooperate (C) if the opponent cooperates in three consecutive rounds after the initial defection.

Pseudocode:
```
function TFT-A(round, history):
  if round == 1:
    return 'Cooperate'
  else:
    last_round = history[-1]
    if len(history) > 3 and last_round == 'Cooperate' and (history[-2] == 'Defect' or history[-3] == 'Defect'):
      return 'Cooperate'
    elif last_round == 'Cooperate':
      return 'Cooperate'
    else:
      return 'Defect'
```

2. Handle Edge Cases:
   - Last Round (r<t): In the absence of future rounds, revert to cooperating as a final goodwill gesture and avoid leaving the game on a punishing note.
   - Initial Struggle Period: To handle situations where opponents may not reciprocate cooperation initially, the strategy should remain patient and continue cooperating for a defined number of initial rounds (e.g., 10). After this period, it begins implementing its TFT-A decision rules.

3. Be Opportunistic:
   - The strategy balances cooperation and defection based on the opponent's actions while still maintaining an opportunistic mindset. It punishes uncooperative behavior but also offers forgiveness to encourage future cooperation.
   - By being adaptive, the strategy can respond to various opponent behaviors effectively, making it more likely to prosper in a tournament setting with multiple AI opponents.
'''

description_OPPORTUNISTIC_5 = '''
 Title: Tit-for-Tat Strategy for N-Player Public Goods Game

1. Specify decision rules:
   - Start with cooperation (C) in the first round to foster trust and encourage reciprocity among players.
   - In subsequent rounds, cooperate (C) if at least half of the other players cooperated in the previous round. Otherwise, defect (D). This rule is designed to balance a mix of cooperation and defection while maintaining opportunism.

2. Handle edge cases:
   - If there are an odd number of players, adjust the "half" rule by considering more than half as necessary for cooperation.
   - In the last round, cooperate (C) if at least half of the other players cooperated in the previous round, otherwise defect (D). This ensures fairness and encourages reciprocity until the end of the game.
   - For the first round, cooperate (C) as previously mentioned.

3. Be opportunistic:
   - By using a responsive approach that depends on the actions of other players, this strategy is inherently opportunistic. It exploits instances where more players choose to cooperate and punishes those who do not by defecting.
   - The strategy maintains a balance between cooperation and defection, which can lead to high payoffs when other players also follow an opportunistic approach.

Pseudocode for the Tit-for-Tat Strategy:

```
function tit_for_tat(round, n_players, player_id, history) {
  if round == 1 {
    action = 'C' (Cooperate)
  } else {
    num_cooperators = count cooperative actions in previous round from history
    if num_cooperators >= (n_players / 2) {
      action = 'C' (Cooperate)
    } else {
      action = 'D' (Defect)
    }
  }

  return action
}
```

This pseudocode can be easily adapted to account for odd numbers of players and the last round by modifying the "half" rule and edge cases accordingly.
'''

description_OPPORTUNISTIC_6 = '''
 Strategy Name: Adaptive Tit-for-Tat with Strategic Cooperation Threshold (ATFST)

1. Specify decision rules - When exactly do you cooperate vs defect?

The ATFST strategy will follow a cooperative approach but adapt its behavior based on the number of cooperators in the previous round and the total number of rounds played (r). In each round t, player i decides to cooperate (C) or defect (D) as follows:

- If t = 1 (first round), player i chooses C with a probability equal to the strategic cooperation threshold (sct) to initiate cooperation. This sct is a parameter that can be adjusted based on the game parameters and historical data from previous games.

- In subsequent rounds, if the number of cooperators in the previous round (t - 1) exceeds or equals the strategic cooperation threshold (sct), player i chooses C to continue cooperating. If not, player i chooses D to punish non-cooperative players. The sct is dynamic and can be adjusted based on the number of remaining rounds (r - t + 1).

Pseudocode for decision rule:
```
def ATFST_decision(i, t, total_contributions_t_1, sct, r):
    if t == 1:
        choose C with probability sct
    else:
        if total_contributions_t_1 >= sct:
            choose C
        else:
            choose D
    adjust_sct(i, t, r)
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

In the first round (t=1), the ATFST strategy will cooperate with a probability equal to the strategic cooperation threshold (sct). In the last round (t=r), player i will consider the impact of their decision on their total payoff over the entire game and may choose to cooperate or defect accordingly.

3. Be opportunistic - Clearly align with the opportunistic mindset

The ATFST strategy is opportunistic in that it seeks to benefit from cooperation when it appears beneficial, but it also retaliates against non-cooperative players by reducing its contributions to punish them. The strategic cooperation threshold (sct) serves as a parameter that can be adjusted based on game parameters and historical data to balance the trade-off between cooperation and punishment.

In addition, the dynamic sct allows the strategy to adapt its behavior throughout the game, making it more robust against various opponent behaviors. As the number of remaining rounds decreases, the sct may become stricter, encouraging cooperation in the final stages of the game when payoffs from previous rounds can have a significant impact on the overall outcome.

Overall, the ATFST strategy provides an adaptive and opportunistic approach to playing the N-Player Public Goods Game while relying only on the game parameters and history. The key innovation lies in the dynamic strategic cooperation threshold (sct) that allows for fine-tuning of the strategy's behavior based on the specific context of each game.
'''

description_OPPORTUNISTIC_7 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Specify decision rules:
   - In the first round, cooperate (C). This allows for a peaceful start and offers an opportunity to build trust.
   - For subsequent rounds, follow the actions of the most frequent cooperator in the previous round. If the most frequent cooperator was themselves a cooperator, also cooperate; if not, defect. This strategy mimics cooperation when facing cooperative opponents but punishes defectors.

Pseudocode:
```
function TFT_AC(round, history, n, k):
    if round == 1:
        return Cooperate (C)

    most_cooperators = max_frequency(history)
    if most_cooperators >= threshold:
        return Cooperate (C)
    else:
        return Defect (D)

function max_frequency(history):
    frequency_dict = {}
    for i in range(len(history)):
        if history[i] not in frequency_dict:
            frequency_dict[history[i]] = 1
        else:
            frequency_dict[history[i]] += 1
    return max(frequency_dict.values())
```

2. Handle edge cases:
   - In the last round, there is no need for retaliation or cooperation as the game ends, so simply cooperate (C).
   - If a player ever encounters an empty history (first encounter), start by cooperating (C) as in the initial round rule.

3. Be opportunistic:
   - The TFT-AC strategy is designed to be opportunistic by offering cooperation initially and retaliating against defection. It maintains a record of opponent's behavior, adapts its own actions accordingly, and remains flexible in response to varying cooperative tendencies among opponents. This allows the AI to capitalize on cooperative tendencies while punishing defectors, making it an opportunistic strategy in this game setting.
'''

description_OPPORTUNISTIC_8 = '''
 Strategy Name: Tit-for-Tat with Gradient Adjustment (TfT-GA)

1. Decision Rules:
   - In the first round (t=1), cooperate to establish a friendly initial interaction (C).
   - For subsequent rounds, observe and mimic the previous action of the opponent (if opponent cooperated in round t-1, cooperate in round t; if opponent defected in round t-1, defect in round t) (OpponentHistory[t-1]). This strategy encourages reciprocity but also allows for punishment when necessary.
   - Gradually adjust the tendency to retaliate by applying a learning factor to the past average cooperation rate of the opponent (AverageCooperationRate). The idea is to learn and adapt to opponents with varying levels of cooperativeness.
     - If the AverageCooperationRate is greater than a threshold (e.g., 0.6), decrease the tendency to retaliate by lowering the learning factor. This encourages cooperation when opponents are relatively trustworthy.
     - Conversely, if the AverageCooperationRate is less than another threshold (e.g., 0.4), increase the tendency to retaliate by raising the learning factor. This punishes uncooperative opponents.
     - If the AverageCooperationRate is between the two thresholds, maintain the current learning factor.

2. Handle Edge Cases:
   - In the last round (t=r), cooperate to maximize the chance of gaining a higher payoff due to the accumulated contributions from previous rounds (C).
   - In cases where there is no history (t=1, opponentHistory[t-1] is empty), cooperate as described in the first rule (C).

3. Be Opportunistic:
   - TfT-GA seeks to maximize payoffs by balancing cooperation and retaliation based on the past behavior of opponents while adapting to changing situations, thus exhibiting an opportunistic mindset.

Pseudocode:

```python
def TfT_GA(n, k, r, opponentHistory):
    learningFactor = 1.0
    averageCooperationRate = 0.5
    for t in range(1, r+1):
        if len(opponentHistory) == 0:
            cooperate = True
        else:
            cooperate = opponentHistory[t-1]

        payoff = (1 - cooperate) + (k/n) * sum(opponentHistory[:t])

        if t == 1 or t == r:
            cooperate = True
        else:
            if averageCooperationRate > 0.6:
                learningFactor *= 0.95
            elif averageCooperationRate < 0.4:
                learningFactor *= 1.05

            cooperate = opponentHistory[t-1] and (cooperate or ((not opponentHistory[t-1]) and (learningFactor > 0.5)))

        opponentHistory.append(cooperate)
        averageCooperationRate = sum(opponentHistory)/len(opponentHistory)

    return payoffSum, opponentHistory
```
'''

description_OPPORTUNISTIC_9 = '''
 Strategy Name: Tit-for-Tat Opportunistic (TfTO)

1. Specify decision rules - When exactly do you cooperate vs defect?

The TfTO strategy follows a tit-for-tat approach with opportunistic elements, adjusting its behavior based on the history of interactions and the game parameters.

- If the player encounters cooperation in the first round, it will cooperate as well (Tit-for-Tat starts cooperatively).
- In subsequent rounds, if the opponent cooperated in the previous round, the TfTO strategy will also cooperate. If the opponent defected, the TfTO strategy will defect in response.
- The TfTO strategy maintains a memory of previous interactions and uses it to decide whether to cooperate or defect in the current round. This allows the strategy to retaliate against opponents who have previously defected but encourages cooperation when it is observed.

2. Handle edge cases - What do you do in the first round, last round, etc.?

- In the first round, TfTO cooperates, as described above.
- In the last round, TfTO evaluates its opponent's behavior during previous rounds to determine whether cooperation or defection is more advantageous given the total game payoff calculation.
- When facing a new opponent in any round, TfTO will cooperate on the first interaction to establish potential long-term benefits from cooperation.

3. Be opportunistic - Clearly align with the opportunistic mindset

- Opportunism is embedded within the Tit-for-Tat strategy by allowing the strategy to adapt its behavior based on the history of interactions with opponents. If an opponent consistently cooperates, TfTO will also cooperate. Conversely, if an opponent consistently defects, TfTO will defect in response.
- By cooperating when it is beneficial (i.e., when an opponent has recently cooperated), and defecting when it is necessary (i.e., when an opponent has recently defected or when the last round is reached), TfTO demonstrates opportunistic behavior without relying on specific coordination mechanisms or shared norms with other players.

Pseudocode:
```
def TitForTatOpportunistic(opponent_history, game_round, game_parameter):
  # Initialize memory of opponent history and current round number
  opponent_cooperation = 0
  current_round = 1

  while current_round <= game_round:
    if current_round == 1 or opponent_cooperation > (game_round - current_round):
      # Cooperate to start or when opponent has cooperated for a long time
      action = 'C'
    else:
      # Defect to retaliate against opponents who have defected recently
      action = 'D'

    if action == 'C':
      opponent_cooperation += 1

    # Update current round number and return the chosen action for this round
    current_round += 1
    return action
```
'''

description_OPPORTUNISTIC_10 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
In each round t, starting from the second round (t > 1), if the number of cooperators in the previous round (t-1) is greater than or equal to a threshold T, then cooperate (play C). Otherwise, defect (play D). The threshold T is determined by a function that considers the game parameters and past history.

In the first round, play C since there's no history for reference. For the last round, revert back to the previous decision rule.

Pseudocode:
```
function ATFT(t):
  if t == 1:
    return 'C'
  if (num_cooperators_in_prev_round >= T) and (total_contributions > 0):
    return 'C'
  else:
    return 'D'
```

2. Handle edge cases - What do you do in the first round, last round, etc.?
As mentioned earlier, in the first round, play C. In the last round, revert back to the decision rule for any other round (t > 1) since the goal is to maximize total payoff over all rounds.

3. Be opportunistic - Clearly align with the opportunistic mindset
The Adaptive Tit-for-Tat strategy aims to cooperate with others when they show a cooperative tendency, but also punishes defection by defecting in response. The threshold T determines the level of cooperation and can be adjusted based on the game parameters and past history. A higher T allows for more forgiveness towards defector behavior, while a lower T encourages harsher punishment.

In addition, the ATFT strategy is adaptive because it adjusts its cooperation level based on previous rounds' outcomes, making it robust to a wide range of opponent behaviors.
'''

description_OPPORTUNISTIC_11 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfTA)

1. Decision Rules:
   - Initially cooperate (C) in the first round to foster a cooperative environment and show good faith.
   - In subsequent rounds, if the opponent cooperates (c_opp > 0), reciprocate by also cooperating (C). This maintains cooperation as long as it persists from the opponent's side.
   - If the opponent defects (c_opp = 0) in any round, respond with defection for the next round (D). After defecting, switch back to cooperation again if the opponent subsequently cooperates.
   - To encourage cooperation and avoid being exploited by overly aggressive opponents, implement a time-limited punishment strategy: if an opponent continuously defects (c_opp = 0) for a predefined number of consecutive rounds (p), revert to defection until the opponent cooperates again (then resume TfTA behavior).

2. Edge Cases:
   - In the first round, play C as described above.
   - In the last round, consider the current payoff difference between cooperation and defection and choose accordingly for a more optimal outcome.
   - If an opponent deviates from TfTA behavior (e.g., switching strategies in later rounds), reassess the partnership and adjust future actions based on the new observed pattern.

3. Opportunistic Mindset:
   - The strategy is opportunistic by prioritizing cooperation when it benefits the player, but also punishing opponents who exploit the partnership to maximize long-term payoffs and encourage cooperation.
   - By adapting to opponent behavior and making adjustments as necessary, TfTA ensures a balance between cooperation and defection that seeks to take advantage of opportunities for mutual gain while protecting against exploitation.

Pseudocode:
```
def tit_for_tat_adaptive(round_num, n, k, opponent_history):
  if round_num == 1:
    action = 'C'  # Cooperate in the first round
  else:
    if opponent_history[-1] == 'C':  # If opponent cooperated last round
      action = 'C'  # Cooperate this round
    elif opponent_history[-1] == 'D' and len(consecutive_defections) < p:  # If opponent defected last round, but not consecutively for too long
      action = 'D'  # Defect this round
    elif opponent_history[-1] == 'D' and len(consecutive_defections) >= p:  # If opponent has been consecutively defeating for p rounds
      action = 'D'  # Continue defection until opponent cooperates again
    else:  # Unanticipated behavior from opponent
      action = update_strategy(opponent_history)  # Update strategy based on observed pattern

  consecutive_defections.append(1 if opponent_history[-1] == 'D' else 0)
  if len(consecutive_defections) > p:
    consecutive_defections.pop(0)  # Maintain a list of the last p rounds for evaluating punishment

  return action
```
'''

description_OPPORTUNISTIC_12 = '''
 Strategy Name: Tit-for-Tat-Adaptive (TfTA)

1. Specify decision rules:
   - Initiate cooperation (play C) for the first round, demonstrating good faith.
   - For subsequent rounds, evaluate the opponent's strategy based on their previous actions and adapt accordingly:
     a. If the opponent cooperates in the last round, return cooperation in the current round.
     b. If the opponent has been cooperative for the majority of previous rounds, continue cooperation.
     c. If the opponent has been uncooperative for the majority of previous rounds, defect (play D).
     d. In case of equal cooperation and defection instances, default to cooperation to encourage potential improvement in the opponent's behavior.

2. Handle edge cases:
   - First round: cooperate as a gesture of goodwill.
   - Last round: consider the opponent's strategy from the previous rounds and make a decision based on the rules outlined above.
   - In case of sudden defection after periods of cooperation, evaluate whether the opponent is reverting to their usual behavior or exhibiting a temporary change. If it's deemed temporary, continue cooperating in the hope that the opponent will return to cooperation. If the pattern persists, defect as a response.

3. Be opportunistic:
   - Maintain adaptability by constantly evaluating and adjusting the strategy based on the opponent's actions.
   - Encourage cooperation by demonstrating goodwill initially and by being forgiving after temporary defections.
   - However, do not hesitate to respond with defection if it becomes clear that an opponent is consistently uncooperative, as opportunistic behavior should also involve punishing uncooperative actions.
'''

description_OPPORTUNISTIC_13 = '''
 Strategy Name: Tit-for-Tat Opportunistic (TfT-O)

1. Specify decision rules - When exactly do you cooperate vs defect?
   The TfT-O strategy follows a tit-for-tat approach with an opportunistic twist. Initially, it will cooperate in the first round to foster trust and cooperation among players. After the first round, it will respond to other players' actions in the previous round. In every subsequent round, it will cooperate if all players cooperated in the previous round, defect otherwise.
   If a player switches from cooperation to defection (defection after cooperation), TfT-O will respond by cooperating again to give them another chance to cooperate. However, if the same player continues to defect after cooperation, TfT-O will defect indefinitely until the other player cooperates again.
   This strategy encourages ongoing cooperation while still being opportunistic and punishing non-cooperative behavior.

   Pseudocode:
   ```
   function TFT_O(round, history):
       if round = 1:
           return 'Cooperate'
       for each previous round in history:
           if all players cooperated in the most recent round before this one:
               return 'Cooperate'
           else:
               if current player previously cooperated and others defected:
                   return 'Cooperate'
               else:
                   return 'Defect'
   ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   TfT-O handles the first round as a special case, cooperating to encourage cooperation among players. For the last round, it continues to make decisions based on the previous round's actions, assuming the game is repeated infinitely (as it doesn't have knowledge of the game's finality).

3. Be opportunistic - Clearly align with the opportunistic mindset
   By cooperating initially and responding to other players' actions, TfT-O demonstrates a willingness to cooperate while still being opportunistic in its responses to non-cooperative behavior. It takes advantage of ongoing cooperation while penalizing defection, making it an effective strategy for this game.
'''

description_OPPORTUNISTIC_14 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TFT-AC)

1. Decision Rules:
   - In the first round, cooperate to show goodwill and encourage reciprocity. (c_i = 1)
   - For subsequent rounds, cooperate if the majority of players cooperated in the previous round. If not, defect. (c_i = max(1 - ⌊(n/2)⌋, 0) if total_contributions > (n/2), else c_i = 0)
   - If the player's payoff in a single round is less than the average payoff over the last 'm' rounds, increase the threshold of cooperation to encourage more players to cooperate. This adjustment will be made gradually with each consecutive round of lower payoffs. (m = int(r/10))
   - If the player's payoff in a single round is greater than or equal to the average payoff over the last 'm' rounds, decrease the threshold of cooperation back to its original value.

2. Edge Cases:
   - In the last round, cooperate if the majority of players cooperated in the previous round. If not, defect. (c_i = max(1 - ⌊(n/2)⌋, 0) if total_contributions > (n/2), else c_i = 0)
   - In the first round, cooperate unconditionally (c_i = 1).

3. Opportunistic Mindset:
   - The strategy starts by cooperating and showing a willingness to contribute to the public good.
   - If other players reciprocate cooperation, TFT-AC will continue cooperating.
   - If others do not reciprocate, TFT-AC will defect in an effort to punish non-cooperative behavior, but it will adjust its threshold of cooperation based on the average payoff over the last several rounds.
   - By adjusting the threshold of cooperation dynamically, TFT-AC can encourage more players to cooperate and improve its overall performance.
'''

description_OPPORTUNISTIC_15 = '''
 Strategy Name: Tit-for-Tat with Fitness Adaptation (TFT-FA)

1. Specify decision rules:
   - In the first round, cooperate to start fresh and demonstrate goodwill. This encourages others to cooperate as well, following the principle of reciprocity. If an opponent defects in the first round, they will be punished immediately, setting a clear boundary for future interactions.
   Pseudocode: if (round == 1) then cooperate; else continue with TFT-FA strategy.

   - For subsequent rounds, adopt a Tit-for-Tat approach, where cooperation is reciprocated by other cooperative actions and defection is met with immediate defection in response. This simple yet effective strategy emphasizes trust and encourages long-term cooperation while punishing betrayal.
   Pseudocode: if last opponent action == cooperate then cooperate; else defect.

   - To ensure robustness to a wide range of opponent behaviors, the TFT-FA strategy incorporates an element of fitness adaptation. The strategy will track its own payoff and adjust its behavior based on the frequency of cooperation from opponents over time. If a player consistently cooperates more than 60% of the time, switch to unconditional cooperation to encourage long-term cooperation. Conversely, if an opponent consistently cooperates less than 40% of the time, switch to unconditional defection as a punishment for their selfish behavior.
   Pseudocode:
      - Maintain a running total of the opponent's cooperative actions over r rounds: `opponent_cooperation_percentage = (sum(opponent_cooperated) / r) * 100`
      - If `opponent_cooperation_percentage > 60`, switch to unconditional cooperation.
      - If `opponent_cooperation_percentage < 40`, switch to unconditional defection.

2. Handle edge cases:
   - In the last round, the payoff will be based on this specific round's actions alone, as there are no future rounds for retaliation or reward. Thus, TFT-FA will adapt its strategy based on the opponent's behavior in the current round. If the opponent cooperates, reciprocate cooperation to maximize payoff; if the opponent defects, also defect to minimize loss.
   Pseudocode: if (round == r) then if (opponent_action == cooperate) then cooperate; else defect.

3. Be opportunistic:
   - The TFT-FA strategy aims to maximize long-term payoff by establishing trust, encouraging cooperation, and punishing defection. However, it also adapts its behavior based on the frequency of cooperation from opponents over time, ensuring robustness against a wide range of strategies and player types. This opportunistic approach allows the TFT-FA strategy to achieve favorable outcomes in various game situations by adjusting its response according to the specific dynamics of each interaction.
'''

description_OPPORTUNISTIC_16 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially cooperate in the first round (C). This is a friendly gesture to encourage cooperation from others.
   - In subsequent rounds, if an opponent cooperated in the previous round, respond with cooperation (C). If not, defect (D). This rule promotes reciprocity and encourages long-term cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First round: Cooperate (C) as mentioned above.
   - Last round: Since the game is repeated, the last round does not affect future rounds. However, to maintain consistency and encourage cooperation for the next round if any, follow the general rule of cooperating if the opponent cooperated in the previous round.

3. Be opportunistic - Clearly align with the opportunistic mindset
   - The ATFT strategy is opportunistic as it leverages the chance for mutual gain through cooperation when other players also choose to cooperate. It also punishes defection by defecting back, which can be seen as a form of opportunism in seeking the best outcome for itself based on its opponents' actions.
   - Additionally, the strategy is flexible and adaptive, adjusting its actions based on observed opponent behavior during the game. This allows it to take advantage of emerging cooperation patterns while also protecting itself from exploitation by defectors.
'''

description_OPPORTUNISTIC_17 = '''
 Strategy Name: Adaptive Tit-for-Tat with Progressive Cooperation (ATFC-P)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initiate cooperation (C) in the first round to demonstrate goodwill and encourage reciprocation.
   - If a player has previously cooperated (c_i = 1), return the favor by also cooperating (C). This mirrors the Tit-for-Tat strategy from game theory, promoting long-term cooperation when others are willing to do so.
   - To introduce opportunism, apply a progressive cooperation mechanism: increase the likelihood of cooperation based on the ratio of previous cooperative actions by the player (i) and overall cooperative actions in the game (Σ(j=1 to n) c_j):
     - If P >= 0.5, play C with probability P; otherwise play D. The value of P is calculated as follows:
       P = max(min((Σ(t=1 to r-1) c_i,t)/(total_contributions, t)), 0.5)
   - If a player has never cooperated (c_i = 0), continue defecting (D). This discourages freeriders and reinforces the progressive cooperation mechanism.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the first round, play C as previously mentioned to initiate cooperation.
   - In subsequent rounds, use the decision rules described above to decide whether to cooperate or defect based on previous actions by other players.
   - For the last round, continue applying the decision rules since future payoffs do not affect the current decision, but the long-term effects of the decision might impact the overall game performance.

3. Be opportunistic - Clearly align with the opportunistic mindset
   - ATFC-P starts cooperatively to encourage others to do the same, but it also punishes non-cooperation and rewards cooperation progressively. This creates an environment where players must consider the potential benefits of cooperation and the consequences of defection.
   - As the game progresses, ATFC-P becomes more aggressive in its pursuit of cooperation by increasing the likelihood of cooperating if others are doing so as well. However, it remains cautious and will not cooperate blindly if others consistently defect.
   - By balancing cooperation with opportunism, ATFC-P seeks to maximize its payoff while still being responsive to the actions of other players in the game.
'''

description_OPPORTUNISTIC_18 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperation (TfT-AC)

1. Specify decision rules:
   - In the first round, cooperate to demonstrate goodwill and encourage cooperation from opponents (C).
   - For subsequent rounds, analyze opponent's behavior in the previous round and adjust own strategy accordingly:
     a) If opponent cooperated, cooperate in the current round (C).
     b) If opponent defected, defect in the current round (D). This punishes opponents for not cooperating while leaving room for recovery.
   - To be more opportunistic and responsive to changes in opponent behavior, introduce a decay factor δ (0 < δ < 1) that gradually relaxes the punishment over time:
     a) If opponent defected, calculate a new cooperation probability p based on current and past cooperations from both player and opponent:
       - If opponent has always defected (i.e., previous rounds were all D), set p = δ.
       - Otherwise, set p = max(min((1 - δ) * (number of recent cooperative rounds) / (number of recent total rounds), 1)).
     b) With calculated cooperation probability p, randomly decide whether to cooperate or defect with a probability of p for the current round.

2. Handle edge cases:
   - In the last round, cooperate to maximize payoff regardless of opponent's action (C).
   - If opponent does not cooperate from the beginning, continue punishing by setting δ close to 0 and never cooperating (D).

3. Be opportunistic:
   - The strategy starts with a cooperative approach but quickly adapts to opponents who consistently defect. It is less likely to be exploited due to its gradual punishment mechanism.
   - By incorporating a decay factor, the strategy becomes more flexible and responsive to changes in opponent behavior over time.
'''

description_OPPORTUNISTIC_19 = '''
 Strategy Name: Tit-for-Tat with Cooperative Drift (TFT-CD)

1. Specify decision rules:
   - Initial Round: Start by cooperating (C). This sets a cooperative tone and encourages other players to follow suit, but also ensures against immediate exploitation.
   - Subsequent Rounds: If an opponent cooperated in the previous round, cooperate back (C). If the opponent defected, also defect in the current round (D). However, with a probability of drift p, deviate from this strict reciprocity and randomly switch to cooperation (C) in response to defection.
   - Last Round: Cooperate regardless of previous opponent's action, as there are no future rounds to consider.

2. Handle edge cases:
   - If an opponent starts with defection but switches to cooperation later, follow the TFT-CD strategy from that point onward.

3. Be opportunistic:
   - The drift probability p can be adjusted to strike a balance between long-term cooperative relationships and immediate retaliation against defection. A lower p value encourages more strict reciprocity, while a higher p value increases the likelihood of switching to cooperation after defection, promoting opportunities for rebuilding trust.
   - When facing different opponent behaviors, the adaptive nature of TFT-CD allows it to respond appropriately. If opponents are consistently cooperative, the strategy benefits from their contributions. If opponents often defect, the drift mechanism offers chances to escape repeated defections and potentially re-establish cooperation.

Pseudocode:
```
def TFT_CD(n, r, k, p):
    previous_action = 'D'  # Initialize with defection for first round
    payoff = 0
    for t in range(1, r+1):
        if t == 1:  # First round, cooperate
            current_action = 'C'
        elif t < r and previous_action == 'C':  # Cooperate if opponent cooperated last round
            current_action = 'C'
        elif t < r and previous_action == 'D':  # Defect if opponent defected last round
            current_action = 'D'
        else:  # Last round, always cooperate
            current_action = 'C'

        if random() <= p or current_action == 'C':  # Drift probability and current action influence cooperation decision
            payoff += (1 - current_action) + (k/n) * sum(previous_actions)
            previous_action = current_action
    return payoff
```
'''

description_OPPORTUNISTIC_20 = '''
 Title: Tit-for-Tat Strategy with Adaptive Cooperation Threshold (TfT-ACT) for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?

The TfT-ACT strategy will start by cooperating in the first round, mimicking the trusting behavior often found in human interactions. From then on, it will adaptively decide to cooperate or defect based on the number of previous cooperators (N_c) and a cooperation threshold (CT). If N_c exceeds CT, the strategy will cooperate; otherwise, it will defect.

Pseudocode:
```
def playRound(history):
    if round == 1:
        return Cooperate()

    cooperation_threshold = findCT(history)
    num_cooperators = countCooperatorsInHistory(history)

    if num_cooperators >= cooperation_threshold:
        return Cooperate()
    else:
        return Defect()
```

2. Handle edge cases - What do you do in the first round, last round, etc.?

For handling edge cases like the first round and the last round, TfT-ACT will use slightly different strategies to encourage initial trust while also considering the endgame scenario:

- In the first round (round == 1), TfT-ACT will cooperate regardless of the cooperation threshold calculation. This establishes a cooperative start.

- In the last round (round >= r), TfT-ACT will always cooperate, as there is no benefit to further punishment or reward in future rounds.

3. Be opportunistic - Clearly align with the opportunistic mindset

The cooperation threshold (CT) calculation will ensure that the strategy remains opportunistic by taking advantage of frequent cooperative actions by other players while avoiding being taken advantage of:

- If more than 50% of previous actions were cooperative, the CT will be set to a relatively high value, encouraging cooperation.
- If less than 50% of previous actions were cooperative, the CT will be set to a relatively low value, making it easier for the strategy to defect.

Pseudocode:
```
def findCT(history):
    if moreThanHalfCooperatorsInHistory(history):
        return highCooperationThreshold()
    else:
        return lowCooperationThreshold()
```
'''

description_OPPORTUNISTIC_21 = '''
 Strategy Name: Tit-for-Tat with Adaptive Cooperative Threshold (TFTAT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   TFTAT cooperates in the first round and then makes decisions based on historical cooperation from other players. If a player has cooperated in the previous round, TFTAT will also cooperate in the current round. However, if a player has defected in the previous round, TFTAT will also defect in the current round until the opponent shows signs of cooperation again. Additionally, TFTAT maintains a Cooperative Threshold (CT) that determines how many consecutive cooperations are needed for TFTAT to trust an opponent and start cooperating again after a defection. The higher the CT, the more cautious TFTAT is.

   Pseudocode:
   - Initialize CT, current_ct = initial_ct (a small number, e.g., 3)
   - For each round t:
      1. If t == 1, cooperate (C)
      2. Else if the opponent cooperated in round t-1, cooperate (C)
      3. Else if the opponent defected in round t-1 and current_ct > 0, defect (D) and decrement current_ct by 1
      4. If the opponent has been cooperating for current_ct consecutive rounds, set current_ct back to initial_ct

2. Handle edge cases - What do you do in the first round, last round, etc.?
   In the first round, TFTAT always cooperates. In the last round or when r < CT, TFTAT will not be affected by its CT because there are no more rounds to retaliate. However, if r > CT and the opponent has been cooperating for current_ct consecutive rounds before the last round, TFTAT will also cooperate in the last round to encourage continued cooperation from the opponent.

3. Be opportunistic - Clearly align with the opportunistic mindset
   By adapting its CT based on the game's outcome (i.e., higher CT for a more competitive environment and lower CT for a more cooperative one), TFTAT aims to maximize its payoff by being both punishing when necessary and forgiving when appropriate. This strategy allows TFTAT to be opportunistic as it takes advantage of an opponent's cooperation while also retaliating against defections.

   To adapt CT, TFTAT can use a simple moving average based on the total number of cooperations divided by the number of rounds played. This way, TFTAT is not only responsive to current game conditions but also learns from past experiences to make better decisions in the future.
'''

description_OPPORTUNISTIC_22 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?

In each round t of the game, the ATFT strategy follows these steps to decide on cooperation (C) or defection (D):

a. First Round: Cooperate (C). This is a friendly gesture that shows willingness to cooperate and creates an opportunity for others to reciprocate.

b. Subsequent Rounds:
   - If the opponent cooperated in the previous round, cooperate (C) as a sign of continued trust and goodwill.
   - If the opponent defected in the previous round, also defect (D) in this round as a consequence for their uncooperative behavior. This is a punishment to discourage future defections and encourages the opponent to return cooperation.

2. Handle edge cases - What do you do in the first round, last round, etc.?

a. First Round: Cooperate (C) as described earlier.

b. Last Round: Since the goal is to maximize total payoff over all rounds, it's beneficial for the strategy to cooperate in the last round if the opponent cooperated in the previous round. This ensures that any possible gains from defecting are lost, and there will still be some reward for reciprocating cooperation.

c. Other Edge Cases: The ATFT strategy does not account for specific edge cases (e.g., penultimate round) because it is designed to be adaptive to various situations without making explicit assumptions about the number of rounds or positions in the game.

3. Be opportunistic - Clearly align with the opportunistic mindset

The ATFT strategy aligns well with an opportunistic mindset by taking advantage of cooperative opponents while also being ready to punish defection. By returning cooperation when receiving it, the strategy aims to maximize its own payoff over multiple rounds without making long-term commitments or assumptions about the opponent's behavior. The opportunistic nature is evident in the tit-for-tat approach of reciprocating cooperation and defecting as a consequence for defection. This ensures that the strategy can adapt to a wide range of opponent behaviors while maintaining its own interests.

Pseudocode:
```
function AdaptiveTitForTat(round, previous_opponent_action) {
  if round == 1 {
    return "Cooperate"
  }

  if previous_opponent_action == "Cooperate" {
    return "Cooperate"
  } else {
    return "Defect"
  }
}
```
'''

description_OPPORTUNISTIC_23 = '''
 Title: Tit-for-Tat-Cooperative (TFTC) Strategy for N-Player Public Goods Game

1. Specify decision rules - When exactly do you cooperate vs defect?
   - In the first round, cooperate (C). This is a sign of goodwill and gives opponents an opportunity to cooperate back.
   - For subsequent rounds, analyze opponent's previous actions:
      - If the opponent cooperated in the previous round, cooperate back (C) in the current round.
      - If the opponent defected in the previous round, defect (D) in the current round as punishment for their non-cooperation.
   Pseudocode:
      ```
      function TFTC(opponent_action_history):
          if round = 1:
              return Cooperate()
          else:
              last_round_opponent_action = opponent_action_history[round-1]
              if last_round_opponent_action == Cooperate():
                  return Cooperate()
              else:
                  return Defect()
      ```

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - In the last round, since there are no further rounds for retaliation or reward, cooperate (C) regardless of the opponent's previous action. This helps to maximize personal payoff in the final round.
   Pseudocode:
      ```
      function TFTC(r: int, opponent_action_history):
          if round = r:
              return Cooperate()
          else:
              return TFTC(opponent_action_history)
      ```

3. Be opportunistic - Clearly align with the opportunistic mindset
   - By adapting to opponents and punishing those who do not cooperate, TFTC takes advantage of opportunities for mutual benefit while also being prepared to defend against non-cooperative behavior. This strategy aims to achieve higher average payoffs compared to purely defecting or cooperating strategies in a dynamic environment with varied opponent behaviors.
'''

description_OPPORTUNISTIC_24 = '''
 Strategy Name: Adaptive Tit-for-Tat with Variable Contribution (ATTC)

1. Specify decision rules - When exactly do you cooperate vs defect?
   ATTC cooperates in the initial round and most of the game, but adjusts contribution levels based on opponent's behavior. If an opponent consistently cooperates, ATTC contributes more to encourage cooperation; if the opponent frequently defects, ATTC reduces contributions as a form of punishment. The strategy can be defined as follows:

   Pseudocode:
   ```
   function ATTC(round, past_opponent_actions):
       if round == 1:
           return COOPERATE

       if past_opponent_actions[round-1] == COOPERATE:
           contribution_level = k/n * (r - 1) * base_contribution
           return COOPERATE with contribution level

       if past_opponent_actions[round-1] == DEFECT and past_opponent_actions[round-2] == COOPERATE:
           contribution_level = base_contribution
           return COOPERATE with contribution level

       return DEFECT
   ```
   Where `base_contribution` is a starting contribution level.

2. Handle edge cases - What do you do in the first round, last round, etc.?
   Since ATTC cooperates in the first round and adjusts contributions based on opponent's behavior, no specific adaptations are needed for edge cases like the first or last rounds. However, if necessary, a slight variation could be made to decrease contributions in the final rounds to conserve resources for potential future interactions.

3. Be opportunistic - Clearly align with the opportunistic mindset
   ATTC is opportunistic by taking advantage of cooperative opponents and punishing those who do not contribute. It encourages cooperation in the hope of earning higher payoffs through a shared public good, but will also adjust contributions to protect its own interests if necessary. This strategy strikes a balance between cooperating for mutual benefit and being selfish when it seems more beneficial.
'''

description_OPPORTUNISTIC_25 = '''
 Title: Tit-for-Tat Strategy for N-Player Public Goods Game

1. Specify decision rules:
   - In the first round (t=1), cooperate (C) to foster a positive environment and encourage potential cooperation from others. This is the only deviation from pure opportunism in this strategy.
   - For subsequent rounds (t>1), observe your own and other players' actions from previous rounds.
     - If all players (or almost all, e.g., n-1) cooperated in the preceding round, cooperate again (C). This rewards cooperation and builds trust.
     - If any player defected in the preceding round, defect (D) in the current round. This punishes defection and discourages future defections.
     - If some players cooperated and others defected, the strategy should consider a probabilistic approach to determine whether to cooperate or defect, based on factors such as the number of cooperators, the number of defaulters, and the history of cooperation/defection by each player. A simple approach could be to calculate a cooperation index (CI) that measures the ratio of cooperative actions over the last few rounds for each player. Cooperate if CI > 0.5 for most players; otherwise, defect.

2. Handle edge cases:
   - For the last round (t=r), since the game is repeated and we do not have future interactions to enforce punishment, it's best to cooperate to maximize payoff in the final round. However, if the player has been consistently defecting throughout the game, they might choose to deviate from this rule for one last opportunity to gain a higher payoff.
   - In the case of tie (e.g., when the number of cooperators is equal to n-1), cooperate as it could encourage the other players to also cooperate in the next round.
   - For situations where the number of players (n) and rounds (r) changes, the strategy should adapt accordingly by modifying the probabilistic approach mentioned earlier based on n and r.

3. Be opportunistic:
   - The strategy balances cooperation with defection based on observed player behavior to maximize long-term payoff while also considering short-term gains when appropriate (e.g., in the first round or last round).
   - By punishing defection and rewarding cooperation, the strategy aims to establish a cycle of reciprocity that benefits the player in repeated interactions with others.
   - The probabilistic approach allows the strategy to adapt to various opponent behaviors and encourages learning and adaptation over time.
'''

description_OPPORTUNISTIC_26 = '''
 Title: Tit-for-Tat Opportunistic Strategy (TfTOS) for N-Player Public Goods Game

1. Decision Rules:
   - Cooperate on the first round (FRC - First Round Cooperation). This gesture can foster trust and cooperation in subsequent rounds.
   - In all other rounds, mimic the previous action of the player against whom the strategy was played in the last round (MIRROR). If the opponent cooperated, reciprocate with cooperation; otherwise, defect. This rule promotes fairness and encourages cooperation while also ensuring self-interest is prioritized.

2. Edge Cases:
   - In the last round, since there are no future rounds to consider, the strategy will simply mirror the opponent's last action (MIRROR).
   - If an opponent plays a mixed strategy and deviates from a cooperative or defective pattern, TfTOS will respond adaptively by mirroring their most recent move.

3. Opportunistic Mindset:
   - By initiating cooperation in the first round and responding to opponents' behavior in subsequent rounds, TfTOS maintains an opportunistic mindset that balances cooperation and self-interest.
   - TfTOS is robust as it does not rely on any specific coordination mechanisms or assumptions about opponent strategies. Instead, it responds adaptively based on observed opponent actions.

Pseudocode:
```python
def TfTOS(opponent_history):
  if round == 1:
    action = 'C' # First Round Cooperation (FRC)
  else:
    action = opponent_history[-1] # Mirror the opponent's last move (MIRROR)

  return action
```
'''

description_OPPORTUNISTIC_27 = '''
 Strategy Name: Tit-for-Tat with Adaptive Contribution (TTAC)

1. Specify decision rules:
   - Initially, cooperate in the first round (C) to demonstrate a cooperative attitude and encourage reciprocity.
   - For subsequent rounds, observe the number of cooperators from the previous round (t-1) and adjust contribution based on a multiplication factor m. If more than half of the players contributed last round (t-1), contribute fully (C). Otherwise, defect (D).
     Pseudocode:
     ```
     if round == 1:
         action = "C"
     else:
         if (total_contributions_t1 >= n/2):
             action = "C"
         else:
             action = "D"
     m = (n+1)/2
     ```
   - Modify the contribution level in response to opponent's strategy. If the number of cooperators increases from round t-1 to t, increase the multiplication factor m slightly. Conversely, if it decreases, decrease the multiplication factor m. The adjustment should not exceed a threshold M or fall below 1.
     Pseudocode:
     ```
     if total_contributions_t > total_contributions_t-1:
         m = min(m*(1+delta), M)
     else:
         m = max(m*(1-delta), 1)
     ```
   - In case of tie (n/2 cooperators), maintain the current multiplication factor.

2. Handle edge cases:
   - In the last round, defect since there will be no future interaction to benefit from reciprocity.
   - If total_contributions_t1 < n/2 and total_contributions_t >= n/2, set m=1 to immediately respond to the increased cooperation.

3. Be opportunistic:
   - The strategy cooperates initially to encourage reciprocal behavior from opponents.
   - Adjusts contribution level based on opponent's actions to maximize payoff by capitalizing on increased cooperation and penalizing defectors.
   - Maintains a flexible multiplication factor to adapt to different opponent strategies and dynamics over time.
'''

description_OPPORTUNISTIC_28 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In the initial round (t=1), cooperate to foster a positive relationship and provide an opportunity for others to reciprocate. This follows the "kindness first" approach, which is often beneficial in repeated games as it promotes cooperation.
   - For subsequent rounds (t>1):
      1. If the opponent cooperated in the previous round, cooperate again to reinforce the positive relationship and encourage continued cooperation from the opponent.
      2. If the opponent defected in the previous round, also defect in the current round as a response (i.e., tit-for-tat). This punishes defection while leaving room for redemption should the opponent start cooperating again later.

2. Handle edge cases:
   - In the last round (t=r), since there are no future interactions, always defect to maximize private payoff without worrying about building or maintaining relationships.
   - If an opponent never cooperates after multiple chances (e.g., a certain number of consecutive defections or a specific fraction of total rounds), switch to always defecting against that opponent. This ensures the strategy does not continually invest in unproductive relationships.

3. Be opportunistic:
   - The ATFT strategy is opportunistic by nature, as it seeks to encourage cooperation while also punishing defection when necessary. It allows for adaptability based on the opponent's behavior and the current stage of the game (initial rounds, late stages).
   - By only considering game parameters and history, the strategy does not rely on assumptions about other strategies or coordination mechanisms, making it robust against a wide range of opponent behaviors in the tournament.
'''

description_OPPORTUNISTIC_29 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules - When exactly do you cooperate vs defect?
   - Initially Cooperate (C): Start by cooperating in the first round to demonstrate trust and foster cooperation. This might encourage others to reciprocate.
   - Tit-for-Tat (TFT) after the First Round: For subsequent rounds, if an opponent cooperates in a given round, return the favor by also cooperating in the next round. If they defect, also defect in response in the following round. This strategy maintains stability and fairness while being simple enough to avoid overcomplication.
   - Forgiving Nature: Upon returning to cooperation after defection, immediately revert to TFT behavior (i.e., no punishment for prolonged periods of uncooperative behavior).

2. Handle edge cases - What do you do in the first round, last round, etc.?
   - First Round (F): Cooperate (C) regardless of opponent actions due to initial goodwill and potential for initiating cooperation.
   - Last Round (L): If total contributions exceed a certain threshold (T), cooperate (C); otherwise defect (D). This encourages cooperation if the game is close to being won, but also protects self-interest if cooperation has not been reciprocated sufficiently. The threshold value T can be determined by considering historical contribution levels and desired payoff expectations.
   - Remaining Rounds (R): Follow TFT rules as described earlier.

3. Be opportunistic - Clearly align with the opportunistic mindset:
   - Adaptive Tit-for-Tat strategy aims to maximize payoffs while maintaining a balance between cooperation and self-interest. It takes into account previous actions from opponents, learns their behavior patterns, and responds accordingly to capitalize on opportunities for mutual benefits when possible. This strategy promotes adaptability in a constantly changing environment where opponent behaviors can be unpredictable or volatile.

Pseudocode:
```
function AdaptiveTitForTat(n, k, r, T):
  if round = 1:
    action = Cooperate
  else:
    if total_contributions > T and last_round_action == Cooperate:
      action = Cooperate
    else:
      action = opponent_last_action

  payoff = (1 - action) + (k/n) * total_contributions
  update_payoffs(payoff)

  if round != r:
    opponent_last_action = action
```
'''

description_OPPORTUNISTIC_30 = '''
 Title: Tit-for-Tat Strategy for N-Player Public Goods Game

1. Specify decision rules:
   - Initialize: In the first round, cooperate (C) to foster cooperation and goodwill. This action sets a baseline of mutual trust and encourages other players to also start with cooperation.
   - Respond: For subsequent rounds, mimic the previous action of the opponent (copy(opponent_action_t-1)). If the opponent cooperated in round t-1, then cooperate in round t; if the opponent defected in round t-1, then also defect in round t. This rule ensures that the strategy responds adaptively to the opponent's actions while maintaining a simple and predictable behavior pattern.
   - Adjust: In the last round, cooperate (C) regardless of the opponent's previous action. Cooperating in the final round will ensure getting the maximum payoff from the community project without worrying about reciprocity from the opponent.

2. Handle edge cases:
   - First round: cooperate(C)
   - Last round: cooperate(C)
   - Ongoing rounds (t > 1): copy(opponent_action_t-1)

3. Be opportunistic:
   - Mimicking the opponent's previous action creates a balance between cooperation and defection, as it encourages reciprocity while also punishing opponents who do not cooperate in earlier rounds. This fosters long-term cooperation and ensures that the strategy reaps benefits from the public goods game without being excessively exploited.
   - In the final round, the strategy seizes the opportunity to maximize payoff by cooperating regardless of the opponent's previous action, as there is no need for reciprocity in the last round.

Pseudocode:
```
function tit_for_tat(round, opponent_action, total_rounds) {
    if (round == 1) {
        return "C"; // Cooperate in first round
    }

    if (round == total_rounds) {
        return "C"; // Cooperate in the last round
    }

    if (opponent_action == "C") {
        return "C"; // Copy opponent's action and cooperate
    } else if (opponent_action == "D") {
        return "D"; // Copy opponent's action and defect
    } else {
        throw new Error("Invalid opponent_action: must be either 'C' or 'D'");
    }
}
```
'''

description_OPPORTUNISTIC_31 = '''
 Strategy Name: Tit-for-Tat with Adaptive Generosity (TFT-AG)

1. Specify decision rules - When exactly do you cooperate vs defect?

The TFT-AG strategy begins by cooperating in the first round, simulating trust and fostering a potential cooperative relationship. For subsequent rounds, it adapts to the opponents' behavior, following three simple rules:

a) If opponent cooperated in the previous round, cooperate in the current round (i.e., reciprocate cooperation).
b) If opponent defected in the previous round, defect in the current round (i.e., punish defection).
c) With a probability p (p<1), display generosity by cooperating even when an opponent has previously defected, aiming to encourage future cooperation. The probability of showing generosity increases gradually with the number of past defections from the opponent.

2. Handle edge cases - What do you do in the first round, last round, etc.?

a) First round: Cooperate to initiate a potential cooperative relationship.
b) Last round: The TFT-AG strategy evaluates its total payoff compared to that of defecting throughout all rounds. If the payoff is higher than the defection payoff, it cooperates; otherwise, it defects. This encourages opponents to cooperate in the last round if they want a chance for a higher payoff.
c) Other edge cases (not first or last round): The strategy follows the three main rules mentioned earlier based on its opponent's previous actions.

3. Be opportunistic - Clearly align with the opportunistic mindset

The TFT-AG strategy is opportunistic in that it adjusts its cooperative behavior based on past interactions with opponents. It is also opportunistic by showing increased generosity over time, hoping to encourage cooperation from opponents who may be more prone to defect initially but can potentially change their strategies later in the game.

Pseudocode for TFT-AG strategy:
```
function TFT_AG(opponent, n, k, r, p):
  total_payoff = 0
  for round in range(1, r+1):
    if round == 1:
      contribute = True  # Cooperate in the first round
    elif round == r:
      if payoff_so_far > defection_payoff:
        contribute = True  # Cooperate in the last round if total payoff is higher than defection payoff
      else:
        contribute = False  # Defect in the last round if total payoff is lower than defection payoff
    else:
      if opponent.last_contribute:
        contribute = True  # Cooperate if opponent cooperated in the previous round
      elif opponent.last_contribute == False and round >= 2:
        past_defections += 1
        if past_defections <= round - 1:
          contribute = (random() < p*(past_defections / (round-1)))  # Show generosity with a probability that increases with the number of past defections
        else:
          contribute = False  # No longer show generosity after a certain threshold
      else:
        contribute = False  # Defect if opponent defected in the previous round
    payoff_this_round = (1 - contribute) + (k/n)*total_contributions
    total_payoff += payoff_this_round
    update opponent's last contribution status
return total_payoff
```
'''


description_OPPORTUNISTIC_32 = '''
 Strategy Name: Adaptive Tit-for-Tat (ATFT)

1. Specify decision rules:
   - In each round t, start by cooperating (playing C). This is a friendly and open initiative to encourage others to cooperate.
   - For subsequent rounds, observe the total number of cooperators in round t-1 (total_cooperators_{t-1}) and compare it with your own cooperation history up to round t-1 (history_cooperation_{i,t-1}). If both values are equal or greater than a predefined threshold 'h' (e.g., h = 3 for n=6), continue cooperating. Otherwise, defect (playing D).
   - Pseudocode:
     ```
     function ATFT(history_cooperation_i, total_cooperators_{t-1}, h):
         if t == 1 then
             return C
         elif history_cooperation_i >= h and total_cooperators_{t-1} >= h then
             return C
         else
             return D
     ```

2. Handle edge cases:
   - In the first round, start by cooperating since the history cooperation is not defined yet (pseudocode adjustment):
     ```
     function ATFT(history_cooperation_i, total_cooperators_{t-1}, h):
         if t == 1 then
             return C
         elif history_cooperation_i >= h and total_cooperators_{t-1} >= h then
             return C
         else
             return D
     ```
   - In the last round, consider the overall performance of the strategy based on accumulated payoffs. If cooperating would yield a higher payoff than defecting, continue to cooperate; otherwise, defect (pseudocode adjustment for last round):
     ```
     function ATFT(history_cooperation_i, total_cooperators_{t-1}, h, r, t):
         if t == r then
             if payoff_from_cooperating > payoff_from_defecting then
                 return C
             else
                 return D
         elif history_cooperation_i >= h and total_cooperators_{t-1} >= h then
             return C
         else
             return D
     ```

3. Be opportunistic:
   - ATFT is opportunistic by nature since it starts cooperating in the hope that others will reciprocate, but it also punishes those who take advantage of its initial cooperative spirit (defecting when others do not cooperate). This strategy maintains a balance between cooperation and self-interest.
   - By being adaptive to various opponent behaviors, ATFT is able to perform well in different game settings, making it a robust and versatile strategy for the tournament.
'''
