"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: Client
- Model: gemini-2.5-flash
"""


description_COLLECTIVE_1 = '''
The following strategy, "Adaptive Collective Contributor (ACC)", is designed to promote and sustain cooperation in the Public Goods Game by mirroring the observed collective behavior of other players, adapting to game dynamics, and anticipating the finite nature of the game.

### Adaptive Collective Contributor (ACC) Strategy Description

This strategy depends on the game parameters (`n`, `r`, `k`) and the history of actions from all players.

#### 1. Decision Rules

**A. First Round (Round 1): Initiate Cooperation**

*   **Action:** Always **Contribute (C)**.
*   **Rationale:** The strategy begins by making a cooperative gesture. This serves as an initial signal of willingness to contribute to the public good and provides an opportunity for other players to reciprocate and establish a cooperative environment.

**B. Intermediate Rounds (Round 2 to Round r-1): Adaptive Reciprocity**

*   At the beginning of each intermediate round, the strategy analyzes the collective actions of all other players from the *immediately preceding round*.
*   **Calculate Others' Cooperation Rate:**
    *   Count the number of other players (excluding yourself) who chose to Contribute (C) in the previous round. Let this be `N_others_contributed`.
    *   Calculate the `CooperationRate_others = N_others_contributed / (n - 1)`. This value represents the proportion of your fellow players who contributed to the public good in the last round.
*   **Decision Based on Collective Cooperation:**
    *   **Cooperation Threshold (T):** This strategy uses a fixed threshold `T = 0.5`.
    *   If `CooperationRate_others >= T` (i.e., 50% or more of the other players contributed in the previous round):
        *   **Action:** **Contribute (C)**.
        *   **Rationale:** If a sufficient level of collective cooperation is observed, the strategy rewards this behavior by continuing to contribute. This reinforces positive collective action and aims to sustain high overall payoffs.
    *   Else (`CooperationRate_others < T`):
        *   **Action:** **Defect (D)** (contribute 0 tokens).
        *   **Rationale:** If the observed collective cooperation falls below the threshold, the strategy responds by defecting. This serves as a collective punishment for widespread free-riding, aiming to deter further declines in contributions and encourage a return to higher cooperation levels.

**C. Last Round (Round r): Rational Defection**

*   **Action:** Always **Defect (D)** (contribute 0 tokens).
*   **Rationale:** In the final round of a finite repeated game, there are no future interactions or opportunities for further punishment or reward. According to backward induction, individual rationality dictates defection to maximize immediate payoff, as there are no consequences for future rounds. This is a common and robust strategy for the final round.

#### 2. Handling Edge Cases

*   **First Round:** Explicitly covered (always Contribute).
*   **Last Round:** Explicitly covered (always Defect).
*   **Small `n` (e.g., `n=2`):** The calculation `N_others_contributed / (n - 1)` handles `n=2` correctly. In this case, `n-1 = 1`, and `CooperationRate_others` will be either 0 (if the other player defected) or 1 (if the other player contributed). The strategy effectively acts as a Tit-for-Tat in a 2-player game.
*   **Tournament Play without Shared Norms:** The strategy is entirely self-contained, requiring no communication or pre-agreed norms. It adapts solely based on observed past actions and the defined rules.

#### 3. Collective Alignment

This strategy embodies a collective mindset by:

*   **Proactive Cooperation:** It initiates cooperation from the first round, demonstrating a willingness to contribute to the common good.
*   **Conditional Reciprocity:** It is designed to reward collective cooperation and penalize collective defection. This mechanism aims to steer the game towards the Pareto-optimal outcome where all players contribute and achieve higher payoffs (`k`) than the Nash Equilibrium of universal defection (`1`).
*   **Protection Against Exploitation:** By defecting when cooperation is insufficient, the strategy protects itself and the collective from being exploited by widespread free-riding, preventing the collapse of cooperation that would lead to suboptimal outcomes for everyone.
*   **Parameter-Agnostic (mostly):** While the threshold `T` is fixed, the strategy's logic scales with `n` and `r`, making it broadly applicable across different game parameters.
'''

description_COLLECTIVE_2 = '''
The following strategy, "Adaptive Reciprocal Cooperator" (ARC), is designed to foster and sustain collective cooperation in the repeated Public Goods Game. It balances an initial commitment to collective welfare with adaptive responses to observed group behavior, ensuring robustness against exploitation while striving for optimal outcomes for the group.

---

### **Adaptive Reciprocal Cooperator (ARC) Strategy**

This strategy operates based on the round number and the observed level of cooperation in the previous round. It aims to achieve and maintain a high level of collective contribution by initiating cooperation, rewarding sustained group contributions, and penalizing insufficient contributions.

**1. Decision Rules:**

*   **Round 1 (Initial Stance):**
    *   **Action:** Contribute (C).
    *   **Rationale:** The strategy begins with an act of cooperation to signal a willingness to build collective welfare and establish a cooperative environment. This is a necessary first step for a collective strategy to encourage others to contribute.

*   **Intermediate Rounds (Round 2 to Round `r-1`):**
    *   **Information:** At the start of round `t` (where `1 < t < r`), observe `C_prev`, the total number of players who contributed in the immediately preceding round (`t-1`).
    *   **Decision Criterion:** Calculate `MinCooperators`, the minimum number of cooperators required for the public good to, on average, return at least the value of a single contribution to the group.
        *   `MinCooperators = ceil(n / k)`
        *   *(Note: Since `1 < k < n`, `n/k` will always be greater than 1. `MinCooperators` will therefore be at least 2, representing a substantial threshold.)*
    *   **Rule:**
        *   **If `C_prev >= MinCooperators`:**
            *   **Action:** Contribute (C).
            *   **Rationale:** The group's previous contribution level was sufficient, meaning that the average return from the public good for contributing players was at least 1 unit. This indicates a healthy level of cooperation, justifying continued contribution to reinforce positive behavior and aim for higher collective payoffs.
        *   **Else (`C_prev < MinCooperators`):**
            *   **Action:** Defect (D).
            *   **Rationale:** The group's previous contribution level was too low, suggesting insufficient cooperation or potential exploitation. Defecting in this scenario serves as a proportional response, a signal that the current level of cooperation is unsustainable, and a protective measure against continued exploitation.

*   **Last Round (Round `r`):**
    *   **Action:** Defect (D).
    *   **Rationale:** In the final round, there are no future interactions to incentivize cooperation. The game effectively reverts to a single-round Public Goods Game, where defection becomes the dominant strategy for all rational players. This action anticipates universal rational behavior and prevents exploitation in the terminal round.

**2. Handling Edge Cases:**
The strategy inherently handles the first and last rounds as distinct phases with specific rules. The intermediate rounds are governed by an adaptive threshold derived directly from game parameters (`n` and `k`), which adjusts dynamically to the observed collective behavior.

**3. Collective Alignment:**
*   **Initial Cooperation:** The strategy starts by cooperating, demonstrating a commitment to the collective good from the outset.
*   **Sustainability Threshold:** The `MinCooperators` threshold (`ceil(n/k)`) is designed to ensure that the collective contributions are generating a sufficient return to the group, making cooperation collectively "worthwhile" beyond individual incentives. This directly promotes a level of contribution that benefits the group.
*   **Reciprocity for Group Health:** By rewarding sufficient group cooperation and punishing insufficient cooperation, the strategy aims to guide the collective towards a high-cooperation equilibrium, rather than simply maximizing individual short-term gains (except in the final round, where future incentives cease). It is a strategy for a player who wants the group to succeed in cooperation.
'''

description_COLLECTIVE_3 = '''
This strategy is called **Adaptive Collective Reciprocation (ACR)**. It is designed to foster and sustain cooperation within the group by adapting to observed collective behavior, while being robust to a variety of opponent strategies.

---

### Adaptive Collective Reciprocation (ACR) Strategy Description

**1. Decision Rules:**

*   **Round 1: Initial Outreach (Always Contribute)**
    *   In the very first round, the player always **Contributes (C)** one token.
    *   *Rationale:* This serves as an initial gesture of trust and a clear signal of willingness to cooperate. It allows for the establishment of a cooperative equilibrium from the outset.

*   **Rounds 2 to `r` (inclusive): Conditional Reciprocation**
    *   At the beginning of each round from the second until the last, the player observes the total number of contributions made by all players (including oneself) in the *immediately preceding round*. Let this be denoted as `C_prev`.
    *   **Cooperation Threshold Calculation:**
        *   Calculate the **Cooperation Threshold `T` = `ceil(n / 2)`**. This threshold represents a simple majority of players. For example, if `n=5`, `T=3`; if `n=4`, `T=2`.
    *   **Decision Logic:**
        *   **If `C_prev >= T` (Sufficient Collective Cooperation):** The player **Contributes (C)** one token.
            *   *Rationale:* If at least a simple majority of players (including oneself) contributed in the previous round, it indicates a sufficient level of collective effort. The strategy reciprocates this positive collective behavior to reinforce cooperation and sustain mutual benefit.
        *   **If `C_prev < T` (Insufficient Collective Cooperation):** The player **Defects (D)**, contributing zero tokens and keeping their endowment.
            *   *Rationale:* If fewer than a simple majority of players contributed, it signals a significant breakdown in collective action or attempts at widespread free-riding. The strategy responds by defecting to protect itself from exploitation and to signal to others that higher levels of contribution are required to maintain cooperation.

**2. Handling Edge Cases:**

*   **First Round (`r=1`):** As specified, the player always **Contributes (C)**.
*   **Last Round (`r`):** The strategy applies the *same conditional reciprocation rules* as for intermediate rounds. It *does not* automatically defect due to the standard backward induction argument common in finite repeated games.
    *   *Rationale:* This decision aligns with the "collective mindset" and "robustness" requirements. Assuming all other AI agents will perfectly backward induct and defect in the final rounds is not robust in a tournament against heterogeneous strategies. By maintaining its conditional cooperation, this strategy keeps open the possibility of sustained collective welfare until the very end, especially against opponents who do not backward induct. If collective cooperation has been strong in the penultimate round, this strategy will continue to contribute in the final round, aiming to maximize overall group payoff. If cooperation has broken down earlier, the strategy will defect accordingly.
*   **Small `n` values (e.g., `n=2`, `n=3`):** The `ceil(n/2)` threshold adapts gracefully.
    *   For `n=2`, `T = ceil(2/2) = 1`. This means if at least one player (which could be oneself) contributed, the strategy contributes. This makes it a relatively "generous" strategy for two-player games, willing to give the other player a chance to cooperate even after a defection, aiming to re-establish cooperation.
    *   For `n=3`, `T = ceil(3/2) = 2`. If at least two players contributed, the strategy contributes. This provides a balanced approach for small groups.

**3. Alignment with Collective Mindset:**

*   **Promotes Cooperation:** ACR is designed from the ground up to initiate and sustain collective cooperation, which is the primary driver of overall welfare in the Public Goods Game.
*   **Reciprocation as a Core Principle:** By conditioning its actions on the group's previous behavior, the strategy actively rewards collective effort and punishes widespread defection, steering the group towards higher contributions.
*   **Robustness for Collective Good:** The choice not to automatically defect in the final round reflects a commitment to collective benefit, even when individual short-term incentives might suggest otherwise. This makes the strategy more robust in a tournament setting where opponents may not be perfectly rational or may have different end-game considerations, thus preserving the potential for higher collective payoffs across all rounds.
*   **Clear and Understandable Rules:** The simple majority threshold provides a transparent basis for collective decision-making, which can be implicitly understood and responded to by other adaptive agents.
'''

description_COLLECTIVE_4 = '''
This strategy is designed to promote and sustain cooperation in the Public Goods Game, balancing the collective good with the need for self-protection against free-riders in a tournament setting. It is adaptive, relying on past actions, and robust across varying game parameters and opponent behaviors.

---

### **Adaptive Conditional Cooperator Strategy**

**Overview:**
This strategy aims to establish and maintain a high level of cooperation by starting cooperatively and then conditionally adapting its behavior based on the collective actions of all players in the previous round. It implements a form of reciprocal cooperation, forgiving minor defections but retaliating against significant drops in collective contributions. It also accounts for the finite nature of the game through backward induction.

**Strategy Details:**

1.  **Initial Round (Round 1, t=1):**
    *   **If `r = 1`** (i.e., this is a single-round game):
        *   **Defect (D)**. In a one-shot Public Goods Game, defection is the dominant strategy.
    *   **Else (`r > 1`)**:
        *   **Contribute (C)**. Start by cooperating to signal a willingness to collaborate and to provide an opportunity for collective cooperation to emerge. This acts as an initial investment in potential collective welfare.

2.  **Intermediate Rounds (Round 2 to `r-1`, i.e., `1 < t < r`):**
    *   **Observe Past Round:** At the beginning of each intermediate round, analyze the actions of all `n` players from the *immediately preceding round (t-1)*.
    *   **Calculate Cooperation Count:** Determine `C_prev`, which is the total number of players who **Contributed (C)** in round `t-1`.
    *   **Decision Rule:**
        *   **If `C_prev >= floor(n * 0.7)`:**
            *   **Contribute (C)**. This strategy cooperates if a sufficiently high proportion (at least 70%) of players contributed in the previous round. This threshold allows for a degree of forgiveness, tolerating minor defections (up to 30% of players) without immediately retaliating, thereby promoting stability and resilience of cooperation.
        *   **Else (if `C_prev < floor(n * 0.7)`):**
            *   **Defect (D)**. If cooperation levels fall below the threshold, the strategy switches to defection. This serves as a collective punishment mechanism, signaling that insufficient contributions will not be tolerated and incentivizing other players to increase their contributions in subsequent rounds.

3.  **Final Round (Round `r`, t=r):**
    *   **Defect (D)**. Regardless of past history, in the final round of a finitely repeated game, there are no future interactions to influence. Therefore, the individually rational choice is to defect, consistent with backward induction.

---
'''

description_COLLECTIVE_5 = '''
This strategy, named "Adaptive Reciprocator with Forgiveness" (ARF), aims to foster and sustain collective cooperation in the Public Goods Game. It operates on the principle of conditional cooperation, adapting its behavior based on the observed actions of other players to encourage higher overall contributions while protecting itself from exploitation.

**Game Parameters:**
*   `n`: Number of players.
*   `r`: Total number of rounds.
*   `k`: Multiplier for the common pool (1 < k < n).

**Internal State:**
*   `Current_Stance`: This variable tracks the strategy's current disposition. It can be either "Cooperating" or "Defecting". Initially, `Current_Stance` is set to "Cooperating".

**Strategic Thresholds:**
*   **`Cooperation_Sustain_Threshold (CST)`**: A fractional value (e.g., `0.5`). If the proportion of players who contributed in the previous round falls *below* this threshold, ARF will switch its `Current_Stance` to "Defecting" and contribute 0.
*   **`Cooperation_Rebound_Threshold (CRT)`**: A fractional value (e.g., `0.75`). If ARF is currently in the "Defecting" `Current_Stance`, it will only return to "Cooperating" if the proportion of players who contributed in the previous round meets or *exceeds* this higher threshold.

**Recommended Default Thresholds:**
*   `CST = 0.5` (i.e., if less than 50% of players cooperated in the last round, switch to defecting).
*   `CRT = 0.75` (i.e., if currently defecting, at least 75% of players must cooperate in the last round to switch back to cooperating).

---

**Decision Rules (for player `i` in round `t`):**

1.  **First Round (t = 1):**
    *   **Action: Contribute (C)** (1 token).
    *   **Rationale:** Initiate cooperation and signal a willingness to contribute to the collective good. This sets a positive precedent.

2.  **Last Round (t = r):**
    *   **Action: Defect (D)** (0 tokens).
    *   **Rationale:** In the final round of a finitely repeated game, the individually rational choice is to free-ride, as there are no subsequent rounds to influence or be influenced by. This prevents exploitation in the endgame.

3.  **Intermediate Rounds (1 < t < r):**

    *   **Observation:** At the beginning of round `t`, observe the actions of all `n` players from the previous round (`t-1`).
    *   Count the number of players who contributed in round `t-1`, let this be `N_cooperators_prev`.
    *   Calculate the `Proportion_Cooperators_prev = N_cooperators_prev / n`.

    *   **Decision Based on `Current_Stance`:**

        *   **If `Current_Stance` is "Cooperating":**
            *   **Condition:** If `Proportion_Cooperators_prev >= CST`
                *   **Action: Contribute (C)** (1 token).
                *   **Rationale:** A sufficient level of cooperation was maintained in the previous round. Continue to contribute to sustain the collective benefit.
            *   **Condition:** Else (`Proportion_Cooperators_prev < CST`)
                *   **Action: Defect (D)** (0 tokens).
                *   **Update `Current_Stance` to "Defecting".**
                *   **Rationale:** Too many players free-rode in the previous round. This punishes non-cooperators and protects the player's endowment from excessive exploitation, signaling that low cooperation is unsustainable.

        *   **If `Current_Stance` is "Defecting":**
            *   **Condition:** If `Proportion_Cooperators_prev >= CRT`
                *   **Action: Contribute (C)** (1 token).
                *   **Update `Current_Stance` to "Cooperating".**
                *   **Rationale:** A strong signal of renewed and widespread cooperation has been observed (meeting the higher `CRT`). Be willing to return to contributing to rebuild trust and re-establish the collective good.
            *   **Condition:** Else (`Proportion_Cooperators_prev < CRT`)
                *   **Action: Defect (D)** (0 tokens).
                *   **Rationale:** Cooperation levels are still too low for a safe return to contributing. Continue to defect as a signal that more consistent cooperation is required.

---

**Collective Mindset Alignment:**
This strategy embodies a collective mindset by:
*   **Initiating Cooperation:** Starting with a contribution to signal a desire for collective welfare.
*   **Sustaining Cooperation:** Continuing to contribute as long as a reasonable level of collective effort is observed.
*   **Punishing Free-Riding:** Temporarily defecting when too many players free-ride, which is a necessary mechanism to prevent the erosion of the public good in repeated interactions.
*   **Offering Forgiveness:** Providing a clear, albeit higher, threshold (`CRT`) for re-engaging in cooperation, allowing for the re-establishment of collective effort after breakdowns.
*   **Robustness:** The adaptive nature allows it to perform well against a variety of opponent strategies, from pure cooperators to pure defectors, by reacting to actual play rather than relying on assumed norms.
'''

description_COLLECTIVE_6 = '''
This strategy, named **Adaptive Collective Reciprocity (ACR)**, aims to foster and sustain high levels of collective cooperation by adaptively adjusting its expectations of group contributions and responding reciprocally. It prioritizes maximizing overall group welfare over the long term, while protecting itself from persistent exploitation.

---

**Game Parameters:**
*   `n`: number of players
*   `k`: multiplier for contributions (with the condition `1 < k < n`)
*   `r`: total number of rounds

**History Tracking:**
*   After each round `t-1`, the strategy observes the total number of players who contributed, denoted as `N_C_prev`.

**Internal State Variable:**
*   `current_cooperation_level_target`: A floating-point number between `k/n` and `1.0` (inclusive). This represents the minimum proportion of total players (from 0.0 to 1.0) that this strategy expects to contribute for it to continue cooperating.

---

**Decision Rules:**

**1. Round 1 (Initialization Phase):**
    *   **If `r = 1`** (a single-round game):
        *   Choose **Defect (D)**.
        (Rationale: In a one-shot Public Goods Game, defection is the individually dominant strategy as there are no future interactions to consider.)
    *   **Otherwise (`r > 1`)** (a repeated game):
        *   Choose **Contribute (C)**.
        (Rationale: An optimistic start signals willingness to cooperate and explores the group's potential for collective action, which is crucial for establishing cooperation in repeated games.)
    *   Initialize `current_cooperation_level_target = 0.5`.
        (Rationale: A moderate initial expectation, balancing optimism with pragmatism. This target will dynamically adjust based on actual group behavior.)

**2. Rounds `t` from 2 to `r-1` (Adaptive Play Phase):**
    Let `N_C_prev` be the total number of players who contributed in the previous round (`t-1`).
    Let `actual_cooperation_proportion_prev = N_C_prev / n`.

    **A. Adjust `current_cooperation_level_target`:**
    *   **If `actual_cooperation_proportion_prev >= current_cooperation_level_target`:**
        *   (The group met or exceeded our target.) **Reward** by slightly increasing the target, encouraging higher levels of future cooperation.
        *   Update: `current_cooperation_level_target = min(1.0, current_cooperation_level_target + (1.0 - current_cooperation_level_target) * 0.1)`
        (Rationale: This increases the target by 10% of the remaining gap towards full cooperation (1.0). It's a slow, steady push towards maximal collective contribution.)
    *   **Else (`actual_cooperation_proportion_prev < current_cooperation_level_target`):**
        *   (The group failed to meet our target.) **Penalize** by slightly decreasing the target, reflecting lower expectations and potentially leading to defection.
        *   Update: `current_cooperation_level_target = max(k / n, current_cooperation_level_target - (current_cooperation_level_target - k/n) * 0.2)`
        (Rationale: This decreases the target by 20% of the gap between the current target and the minimum feasible level of cooperation (`k/n`). This allows for a quicker, but not irreversible, response to low cooperation. The lower bound `k/n` prevents the strategy from setting an unrealistically low target; if the average contribution return is less than `k/n`, cooperation is extremely unfavorable.)

    **B. Determine Action for Current Round `t`:**
    *   **If `actual_cooperation_proportion_prev >= current_cooperation_level_target`:**
        *   Choose **Contribute (C)**.
        (Rationale: Continue to support collective efforts as expectations are being met or exceeded, reinforcing positive feedback.)
    *   **Else (`actual_cooperation_proportion_prev < current_cooperation_level_target`):**
        *   Choose **Defect (D)**.
        (Rationale: Withdraw support due to insufficient collective effort in the previous round, acting as a reciprocal punishment for defection.)

**3. Round `t = r` (Final Round - Endgame Phase):**
    *   Regardless of past history or the `current_cooperation_level_target`:
        *   Choose **Defect (D)**.
        (Rationale: In the final round, there are no future interactions to incentivize cooperation or punish defection. Backward induction dictates that the individually rational strategy of defection prevails.)

---

**Alignment with Task Requirements:**

*   **1. Specify decision rules:** Clearly defined for all phases based on `N_C_prev` and the adaptive `current_cooperation_level_target`.
*   **2. Handle edge cases:** Explicit rules for the first round (`r=1` vs. `r>1`) and the last round (`t=r`).
*   **3. Be collective:**
    *   The strategy starts cooperatively to initiate collective action.
    *   It continuously attempts to raise the `current_cooperation_level_target`, striving for higher group contributions and, consequently, greater collective welfare (as `k > 1`).
    *   Its responses are based on the overall `actual_cooperation_proportion_prev` of the group, not just individual actions, making it a truly collective strategy.
    *   By punishing insufficient cooperation, it aims to deter free-riding and guide the group towards more cooperative equilibria.
*   **Adaptive and Robust:**
    *   **Adaptation:** The `current_cooperation_level_target` dynamically adjusts to observed group behavior, allowing the strategy to learn and react to different opponents and game dynamics.
    *   **Robustness:** It protects against exploitation by defecting when cooperation levels are low. Its adaptive nature also allows for forgiveness and re-establishment of cooperation if group behavior improves, preventing permanent breakdown. The `k/n` floor ensures a minimal expectation for group cooperation, preventing total capitulation.
'''

description_COLLECTIVE_7 = '''
This strategy, named "Adaptive Reciprocal Group Contributor," is designed to foster collective cooperation in the Public Goods Game by adaptively responding to the group's observed behavior while ensuring its own robustness against exploitation, particularly in the critical final round. It balances the collective good with individual self-preservation in a competitive tournament environment.

**Strategy Parameters:**

*   **`initial_cooperation_threshold_rate`**: A float (between 0 and 1) representing the baseline proportion of contributions from the group required for this strategy to contribute. A value of `0.5` is a balanced starting point, assuming no prior knowledge of group generosity.
*   **`learning_rate`**: A small positive float (e.g., `0.1`) that determines how quickly the `current_cooperation_threshold_rate` adjusts.
*   **`min_threshold_rate`**: A minimum bound for `current_cooperation_threshold_rate` (e.g., `0.1`).
*   **`max_threshold_rate`**: A maximum bound for `current_cooperation_threshold_rate` (e.g., `0.9`).

**Decision Rules:**

1.  **Round 1 (Initiation Phase):**
    *   **Action:** Always **Contribute (C)**.
    *   *Rationale:* This acts as an initial overture, signaling a willingness to cooperate and testing the group's responsiveness. It sets a positive tone for potential collective welfare.
    *   *Initialization:* Set `current_cooperation_threshold_rate` to `initial_cooperation_threshold_rate`.

2.  **Intermediate Rounds (Round `t` where `1 < t < r`):**
    *   **Observation:** After round `t-1`, calculate the `observed_group_cooperation_rate`. This is the total number of contributions in round `t-1` divided by the total number of players (`n`).
        `observed_group_cooperation_rate = (sum of all players' contributions in round t-1) / n`
    *   **Decision:**
        *   If `observed_group_cooperation_rate` is greater than or equal to `current_cooperation_threshold_rate`:
            *   **Action:** **Contribute (C)**.
            *   *Rationale:* The group's observed cooperation level meets or exceeds the strategy's current expectation. Continue to contribute to reinforce and maintain collective welfare.
        *   Else (if `observed_group_cooperation_rate` is less than `current_cooperation_threshold_rate`):
            *   **Action:** **Defect (D)**.
            *   *Rationale:* The group is not sufficiently cooperative to warrant continued contribution. Defect to avoid being exploited and to signal a demand for greater collective action from the group.
    *   **Adaptation of `current_cooperation_threshold_rate` (for the *next* round):**
        *   If `observed_group_cooperation_rate` was *higher* than `current_cooperation_threshold_rate`:
            *   `current_cooperation_threshold_rate = max(min_threshold_rate, current_cooperation_threshold_rate - learning_rate)`
            *   *Rationale:* The group was more cooperative than anticipated. The strategy adjusts its threshold downwards, becoming more forgiving and more willing to cooperate in subsequent rounds. This rewards collective generosity.
        *   Else if `observed_group_cooperation_rate` was *lower* than `current_cooperation_threshold_rate`:
            *   `current_cooperation_threshold_rate = min(max_threshold_rate, current_cooperation_threshold_rate + learning_rate)`
            *   *Rationale:* The group was less cooperative than anticipated. The strategy adjusts its threshold upwards, becoming less forgiving and demanding a higher level of cooperation to contribute in subsequent rounds. This punishes collective selfishness.
        *   Else (if `observed_group_cooperation_rate` was *equal* to `current_cooperation_threshold_rate`):
            *   The `current_cooperation_threshold_rate` remains unchanged.

3.  **Final Round (Round `r`):**
    *   **Action:** Always **Defect (D)**.
    *   *Rationale:* In a finite repeated game, the dominant strategy for the final round is to defect, as there are no future interactions or reputation effects to consider. While the strategy embodies a collective mindset, this specific edge case necessitates self-preservation in a tournament where other agents are likely to defect. This protects the strategy from being a "sucker" in the closing moments of the game.

**Collective Mindset Alignment:**

*   **Proactive Cooperation:** Initiates cooperation in the first round to build trust and demonstrate willingness for collective benefit.
*   **Conditional Reciprocity:** Evaluates and responds to the group's overall cooperation. It aims to contribute when there's sufficient collective effort, thereby promoting sustainable cooperation.
*   **Adaptive Learning:** Dynamically adjusts its expectations of group cooperation based on observed history, fostering long-term collective success in varying environments.
*   **Strategic Robustness:** While prioritizing collective welfare, the strategy includes a game-theoretically sound defection in the final round to prevent exploitation, acknowledging the competitive tournament context.
'''

description_COLLECTIVE_8 = '''
This strategy, named "Adaptive Collective Reciprocity (ACR)", aims to foster and sustain collective cooperation in the Public Goods Game by adapting its behavior based on observed historical contributions, while also protecting itself from exploitation, particularly in end-game scenarios. It accounts for the game parameters `n` (number of players), `r` (number of rounds), and `k` (multiplier) to dynamically adjust its responsiveness.

**Strategy: Adaptive Collective Reciprocity (ACR)**

**Game Parameters:** `n` (number of players), `r` (number of rounds), `k` (multiplier)

---

**Decision Rules:**

1.  **If `r = 1` (Single Round Game):**
    *   **Action:** Defect (D).
    *   **Reasoning:** In a single-round Public Goods Game, defection is the dominant strategy for individual payoff maximization, as there are no future interactions to incentivize cooperation or punish non-cooperation.

2.  **If `r > 1` (Repeated Game):**

    *   **Round 1 (Initial Commitment):**
        *   **Action:** Contribute (C).
        *   **Reasoning:** Begin with a contribution to signal a willingness to cooperate and to "test the waters" for reciprocal behavior from other players. This establishes a positive initial collective intent.

    *   **Rounds 2 to `r-1` (Adaptive Reciprocity Phase):**
        *   **Observation:** At the beginning of round `t` (for `2 <= t < r`), observe the actions of all players from the immediately preceding round `t-1`.
        *   **Calculate Average Contribution Rate (ACR):**
            *   `ACR = (Sum of all players' contributions in round t-1) / n`
            *   *(This represents the proportion of players who contributed in the previous round.)*
        *   **Set Cooperation Threshold (T):**
            *   `T = 1 / k`
            *   *(Note: Given `1 < k < n`, the threshold `T` will always be a value between `1/n` and `1` (exclusive).)*
            *   **Rationale for T:** This threshold dynamically adjusts to the efficiency of the public good.
                *   If `k` is high (meaning the public good is very efficient, and individual contributions generate substantial collective benefits), `T` will be low. This makes the strategy more "forgiving," requiring a lower average contribution rate from others to continue cooperating.
                *   If `k` is low (meaning the public good is less efficient, and collective benefits are modest), `T` will be high. This demands a higher average contribution rate from others to justify continued cooperation.
        *   **Decision:**
            *   If `ACR >= T`: Contribute (C).
            *   If `ACR < T`: Defect (D).
        *   **Reasoning:** This is the core adaptive mechanism designed to foster collective welfare. The strategy reciprocates observed levels of cooperation, contributing when the collective effort is deemed sufficiently high (based on the `1/k` threshold) and pulling back (defecting) when cooperation is insufficient to make the collective endeavor worthwhile or when exploitation is detected. This prevents persistent exploitation while enabling robust cooperation under favorable conditions.

    *   **Round `r` (End-Game Protection):**
        *   **Action:** Defect (D).
        *   **Reasoning:** In the absolute final round of a finite repeated game, the incentive structure reverts to that of a single-round game. There are no subsequent rounds in which to reward cooperation or punish defection. Therefore, individual rationality dictates defection to maximize payoff and prevent being exploited by other players who will also rationally defect.

---
'''

description_COLLECTIVE_9 = '''
Strategy Name: Adaptive Collective Cooperation (ACC)

The Adaptive Collective Cooperation (ACC) strategy is designed to foster and sustain group-wide cooperation in the Public Goods Game. It operates on principles of initial benevolence, conditional reciprocity based on group behavior, and rational adaptation to finite game conditions. The strategy aims to maximize collective welfare while remaining robust against exploitation.

---

### 1. Decision Rules

The decision to Contribute (C) or Defect (D) in any given round `t` (from 1 to `r`) is determined as follows:

*   **Round 1 (Initial Gesture):**
    *   **Action:** Contribute (C).
    *   **Rationale:** The strategy begins with an act of cooperation to signal its willingness to contribute to the common good and to test the cooperative inclination of other players. This establishes a foundation for potential collective benefit.

*   **Rounds `t` from 2 to `r-1` (Conditional Reciprocity):**
    *   **Observation:** At the start of round `t`, the strategy observes the actions of all `n` players from the *immediately preceding round* (`t-1`).
    *   **Calculation:**
        1.  Count the total number of players who contributed in round `t-1`: `N_cooperators_prev = sum_j c_j_prev`.
        2.  Calculate the proportion of cooperators in round `t-1`: `P_cooperators_prev = N_cooperators_prev / n`.
    *   **Decision:**
        *   **If `P_cooperators_prev >= 0.5` (Majority Rule):** Contribute (C).
            *   **Rationale:** If a majority (50% or more) of players demonstrated cooperation in the previous round, the strategy reciprocates by contributing. This reinforces collective action, rewards group effort, and sustains the potential for high group payoffs.
        *   **Else (If `P_cooperators_prev < 0.5`):** Defect (D).
            *   **Rationale:** If less than a majority of players contributed, indicating a lack of collective effort or potential free-riding, the strategy defects. This serves as a collective "punishment" mechanism, signaling that individual defection will not be tolerated and that continued cooperation requires a significant group commitment. It protects the strategy from sustained exploitation.

*   **Round `r` (Last Round - Terminal Rationality):**
    *   **Action:** Defect (D).
    *   **Rationale:** In the final round of a finite repeated game, there are no future interactions to influence. The incentives to maintain reputation or engage in punishment/reward cease to exist. Therefore, defection becomes the individually rational and robust choice to maximize one's own payoff in this terminal round, regardless of prior group behavior.

### 2. Handling Edge Cases

*   **First Round (`t=1`):** Explicitly handled by contributing (C) to initiate collective action.
*   **Last Round (`t=r`):** Explicitly handled by defecting (D) due to the absence of future interactions and the corresponding breakdown of reputation-based incentives.
*   **Intermediate Rounds (`t=2` to `r-1`):** These rounds are covered by the conditional reciprocity rule, which dynamically adapts behavior based on the observed group cooperation level from the previous round.

### 3. Collective Mindset Alignment

The Adaptive Collective Cooperation strategy embodies a collective mindset through the following principles:

*   **Initiation of Collective Good:** By starting with a contribution, the strategy actively attempts to seed cooperation and establish a foundation for collective welfare.
*   **Promotion of Conditional Cooperation:** The core decision rule based on a 50% cooperation threshold directly encourages mutual cooperation. It rewards strong collective contributions and signals disapproval for widespread defection, aiming to guide the group towards a high-cooperation equilibrium.
*   **Robustness Against Exploitation:** While striving for collective good, the strategy is not naive. It protects itself from being consistently exploited by free-riders by defecting when group cooperation falls below a critical level, ensuring the sustainability of its cooperative stance.
*   **Simplicity and Predictability:** The clear and consistent rules, particularly the fixed 0.5 threshold, make the strategy relatively easy to understand and potentially predictable by other rational agents. This can facilitate the emergence of stable cooperative patterns within the group, ultimately benefiting all players.
'''

description_COLLECTIVE_10 = '''
This strategy, named "Adaptive Trust Builder," aims to maximize collective welfare by proactively fostering cooperation while remaining robust against exploitation. It adapts its behavior based on the observed cooperation level of other players, with a bias towards promoting trust and collaboration.

---

**Strategy Name:** Adaptive Trust Builder

**Goal:** Achieve and sustain high collective contribution levels, thereby maximizing overall payoffs for the group, while protecting against persistent free-riding.

**Game Parameters (available to the strategy):**
*   `n`: Total number of players
*   `r`: Total number of rounds
*   `k`: Multiplier (1 < k < n)

**Internal State (for this player's internal use):**
*   `current_round_number`: Tracks the current round (from 1 to `r`).

**Fixed Thresholds (calibrated for general robustness):**
*   `Threshold_High_Cooperation = 0.7` (If 70% or more of others contributed)
*   `Threshold_Low_Cooperation = 0.3` (If 30% or less of others contributed)
*   `Threshold_Moderate_Cooperation_Forgiveness = 0.5` (If 50% or more of others contributed in the moderate range)

---

**Decision Rules (Action for Player i in Round `t`):**

1.  **First Round (`t = 1`):**
    *   **Action:** Contribute (C).
    *   **Rationale:** Initiate the game with a clear signal of willingness to cooperate. This proactive contribution establishes an initial trust and provides an opportunity for the group to realize the benefits of collective action.

2.  **Last Round (`t = r`):**
    *   **Action:** Defect (D).
    *   **Rationale:** In a finite repeated game, the "shadow of the future" vanishes in the final round. Rational players will defect to maximize their immediate payoff without fear of future retaliation. Defecting in the last round prevents exploitation by other strategies that will also rationally defect.

3.  **Intermediate Rounds (`1 < t < r`):**
    *   **Observation:** After round `t-1`, observe the contribution action (`c_j_{t-1}` in `{0,1}`) of every other player `j`.
    *   **Calculation:** Calculate the average contribution rate of all *other* players in the *previous* round:
        `avg_others_c = (sum_{j!=i} c_j_{t-1}) / (n-1)`

    *   **Decision Logic:**
        *   **If `avg_others_c >= Threshold_High_Cooperation`:**
            *   **Action:** Contribute (C).
            *   **Rationale:** Reward high levels of cooperation. When the group demonstrates strong collective behavior, continue to contribute to maintain and reinforce this positive dynamic, ensuring high collective payoffs.

        *   **Else If `avg_others_c <= Threshold_Low_Cooperation`:**
            *   **Action:** Defect (D).
            *   **Rationale:** Protect against widespread free-riding and signal that a very low level of cooperation is unacceptable. This serves as a strong punitive measure to discourage exploitative behavior and encourage a return to cooperation.

        *   **Else (i.e., `Threshold_Low_Cooperation < avg_others_c < Threshold_High_Cooperation` - Moderate Cooperation):**
            *   *This is the adaptive and forgiving zone, where the strategy attempts to steer the group towards higher cooperation.*
            *   **If `avg_others_c >= Threshold_Moderate_Cooperation_Forgiveness`:**
                *   **Action:** Contribute (C).
                *   **Rationale:** If a significant portion of the group (at least 50% here) is cooperating, demonstrate generosity and continue to cooperate. This aims to reinforce positive behavior, forgive minor deviations, and gently guide the group towards full cooperation.
            *   **Else (`avg_others_c < Threshold_Moderate_Cooperation_Forgiveness`):**
                *   **Action:** Defect (D).
                *   **Rationale:** If cooperation is still below a moderate, fair threshold, maintain a cautious stance by defecting. This acts as a milder corrective punishment to prevent further decline and incentivize an increase in contributions from other players.

---

**Collective Mindset Alignment:**

*   **Proactive Cooperation:** Starts by cooperating to initiate collective benefit, taking the first step towards a positive outcome.
*   **Rewarding Reciprocity:** Explicitly contributes when others are highly cooperative, directly supporting the collective good.
*   **Forgiveness and Nudging:** The strategy incorporates a forgiving aspect (contributing even when group cooperation isn't perfect, as long as it's above 50%) to encourage positive trends and build trust. This is crucial for navigating dynamic group behaviors and moving towards higher collective welfare.
*   **Strategic Punishment:** Defection is used judiciously as a response to low cooperation, not as an initial stance. This aims to deter free-riding and guide the group back towards cooperative norms, thereby safeguarding the collective interest.
*   **Balanced Pragmatism:** The last-round defection acknowledges the game's mechanics while preserving the benefits of cooperation for as long as possible, striking a balance between collective goals and individual rationality in a tournament setting.
'''

description_COLLECTIVE_11 = '''
This strategy, named **Adaptive Collective Reciprocity (ACR)**, aims to foster and sustain collective cooperation while being robust against exploitation. It operates on the principle of group-level conditional cooperation, seeking to maintain collective welfare by adapting its behavior based on the overall contribution level of the group in the previous round.

---

### Adaptive Collective Reciprocity (ACR) Strategy

This strategy depends on the game parameters `n` (number of players), `r` (number of rounds), and `k` (multiplier), and the history of actions.

**1. Decision Rules:**

*   **Round 1 (Initial Play):**
    *   **Action: Contribute (C).**
    *   **Rationale:** Begin with cooperation to signal willingness to contribute to the common good and to encourage other players to do the same. This sets a positive tone for potential collective welfare.

*   **Rounds 2 through `r-1` (Adaptive Play):**
    *   After each round `t-1`, observe the actions of all `n` players. Calculate the **Total Contributions in the Previous Round (`S_prev`)**, which is the sum of `c_j` for all players `j` in round `t-1`.

    *   **Decision Rule for Round `t`:**
        *   **If `S_prev >= k`:** **Contribute (C).**
            *   **Rationale:** If the total contributions from the previous round meet or exceed the multiplier `k`, it signifies that the collective effort is sufficient to generate a meaningful shared benefit. This strategy rewards the group for maintaining a healthy level of cooperation by continuing to contribute. The threshold `k` ensures that individual contributions are generating a pool substantial enough to be considered a collective success.
        *   **If `S_prev < k`:** **Defect (D).**
            *   **Rationale:** If the total contributions fall below the threshold `k`, it indicates insufficient collective cooperation. In this scenario, the strategy defects to avoid being exploited by free-riders and to signal that the current level of group contribution is not sustainable or mutually beneficial. This acts as a collective "punishment" mechanism to incentivize higher contributions in subsequent rounds.

*   **Round `r` (Final Round):**
    *   **Action: Defect (D).**
    *   **Rationale:** In the final round, there is no future play to incentivize cooperation (the "shadow of the future" disappears). The individually rational action is to defect to maximize one's own payoff, regardless of previous rounds' outcomes. This prevents exploitation by opponents who would inevitably defect in the final round.

**2. Handling Edge Cases:**

*   **First Round (`t=1`):** Always cooperates (C) to initiate collective play.
*   **Last Round (`t=r`):** Always defects (D) due to the endgame effect.
*   **Intermediate Rounds (`1 < t < r`):** Decisions are made adaptively based on the previous round's total contributions relative to the `k` threshold.

**3. Collective Mindset Alignment:**

*   **Initiates Cooperation:** Starts with a contribution to actively pursue collective welfare from the outset.
*   **Group-Oriented Threshold:** The decision to cooperate or defect is based on the *overall group performance* (`S_prev`) rather than specific individual actions. This promotes collective stability by tolerating some individual defection as long as the group's total contribution remains strong (`S_prev >= k`).
*   **Adaptive for Collective Good:** By having a threshold that triggers defection only when collective contributions are significantly low, the strategy seeks to guide the group back towards higher cooperation levels, rather than retaliating against single instances of defection. It aims to prevent a downward spiral triggered by individual retribution, unless the collective effort clearly fails.
*   **Protects Against Systemic Exploitation:** While forgiving of minor lapses, it protects against sustained, widespread free-riding by defecting when the overall contribution falls below a critical level. This ensures that the strategy is not a "sucker" that perpetually contributes without sufficient group reciprocation.

---
'''

description_COLLECTIVE_12 = '''
This strategy, named "Adaptive Reciprocity with Majority Rule," aims to foster and sustain collective cooperation by responding to the group's overall behavior. It balances the desire for collective welfare with the need for individual protection against exploitation, adapting its actions based on observed contributions while accounting for the game's boundaries.

**Strategy: Adaptive Reciprocity with Majority Rule**

**1. Decision Rules:**

*   **Round 1 (Initial Play):**
    *   **Action:** Contribute (C).
    *   *Rationale:* Start cooperatively to signal willingness to contribute and to explore the initial intentions of other players. This sets a positive precedent.

*   **Intermediate Rounds (Round 2 up to Round r-1):**
    *   **Observe Past Actions:** Count `N_C_prev`, the total number of players who contributed (chose C) in the immediately preceding round.
    *   **Decision Threshold:**
        *   **If `N_C_prev >= n / 2` (at least half of the players contributed in the previous round):**
            *   **Action:** Contribute (C).
            *   *Rationale:* A significant portion of the group is demonstrating cooperation. By contributing, this strategy reciprocates positive collective behavior, reinforcing cooperation and maintaining momentum towards higher collective welfare.
        *   **Else (`N_C_prev < n / 2` - fewer than half of the players contributed in the previous round):**
            *   **Action:** Defect (D).
            *   *Rationale:* Insufficient collective effort. This strategy defects to penalize free-riding and low cooperation levels. The aim is to deter further defection and encourage other players to increase their contributions in subsequent rounds, thereby nudging the group back towards mutual cooperation.

*   **Last Round (Round r):**
    *   **Action:** Defect (D).
    *   *Rationale:* In the final round, there are no future interactions to incentivize cooperation. The dominant strategy for a single round applies, as there are no repercussions for defection. Contributing would only lead to individual exploitation.

**2. Handling Edge Cases:**

*   **First Round:** Explicitly handled by always contributing to initiate cooperation.
*   **Last Round:** Explicitly handled by always defecting to prevent exploitation due to the lack of future interactions.
*   **Small `n` (e.g., `n=2`):** The `N_C_prev >= n/2` rule simplifies to `N_C_prev >= 1`. This means if at least one player (which would be the other player in a 2-player game) contributed, this strategy contributes. This is essentially a Tit-for-Tat variant, which is highly robust for `n=2`.
*   **Odd `n`:** The `n/2` threshold means `N_C_prev` must be greater than or equal to `ceil(n/2)` for cooperation (e.g., if `n=3`, `N_C_prev >= 1.5` implies `N_C_prev >= 2`). This correctly establishes a clear majority requirement.

**3. Collective Alignment:**

This strategy prioritizes collective welfare by actively working to establish and maintain a high level of group contribution.
*   It starts cooperatively to initiate a positive collective dynamic.
*   It rewards collective effort (when a majority contributes) by continuing to contribute, aiming to sustain the public good.
*   It punishes collective defection (when a majority defects) to prevent exploitation and to encourage a re-evaluation of strategies by other players, ultimately seeking to steer the group back towards a more cooperative equilibrium that benefits all.
*   The only exception is the final round defection, which is a necessary individual protection against exploitation when collective enforcement mechanisms (future rounds) cease to exist.
'''
