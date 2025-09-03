"""
Strategy descriptions for PublicGoodsDescription.

Generated with:
- Provider: Anthropic
- Model: claude-sonnet-4-0
"""


description_COOPERATIVE_1 = '''
# Adaptive Cooperative Strategy: "Trust Builder"

## Core Philosophy
This strategy begins with cooperation to establish trust and mutual benefit, while adapting based on the group's cooperative tendencies. It aims to maximize collective welfare while protecting against systematic exploitation.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and test the group's disposition

### Rounds 2 to r-1: Adaptive Cooperation Based on Group Behavior

**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Detailed Logic**:
```
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round >= 0.5:
    action = COOPERATE
else:
    action = DEFECT
```

### Round r (Final Round): Conditional Cooperation
- **Action**: COOPERATE if average cooperation rate across all previous rounds ≥ 40%
- **Rationale**: Even in the final round, reward groups that showed reasonable cooperative behavior throughout the game

## Key Features

### 1. **Optimistic Start**
- Begin with cooperation to signal good intentions
- Give the group a chance to establish a cooperative equilibrium

### 2. **Majority-Based Adaptation**
- Use 50% threshold to distinguish between cooperative and non-cooperative groups
- This threshold is forgiving enough to maintain cooperation even when some players defect

### 3. **Collective Punishment**
- When cooperation falls below 50%, defect to avoid being exploited
- This creates incentives for others to maintain higher cooperation levels

### 4. **Final Round Forgiveness**
- Don't automatically defect in the last round (common in game theory)
- Reward groups that maintained reasonable cooperation (≥40% average)

## Pseudocode

```python
def trust_builder_strategy(round_number, history, n, k, r):
    if round_number == 1:
        return COOPERATE
    
    if round_number == r:  # Final round
        total_cooperation_rate = sum(cooperation_rates_all_rounds) / (r-1)
        return COOPERATE if total_cooperation_rate >= 0.4 else DEFECT
    
    # Rounds 2 to r-1
    last_round_cooperators = count_cooperators_in_round(history[-1])
    cooperation_rate_last_round = last_round_cooperators / n
    
    return COOPERATE if cooperation_rate_last_round >= 0.5 else DEFECT
```

## Strategic Advantages

1. **Promotes Group Welfare**: Encourages high-cooperation equilibria that benefit everyone
2. **Exploitation Protection**: Switches to defection when facing predominantly selfish behavior
3. **Clear Incentives**: Creates predictable consequences that encourage others to cooperate
4. **Forgiving**: Maintains cooperation as long as the majority cooperates, allowing for some free-riding
5. **End-Game Stability**: Doesn't succumb to typical last-round defection, rewarding consistent cooperators

## Expected Performance

- **Against Cooperative Groups**: Will likely achieve mutual cooperation and high payoffs
- **Against Mixed Groups**: Will adapt appropriately, cooperating when beneficial and defecting when necessary
- **Against Defective Groups**: Will quickly switch to defection after round 1, minimizing losses

This strategy balances the cooperative ideal with practical protection against exploitation, making it robust across different opponent compositions.
'''

description_COOPERATIVE_2 = '''
# Cooperative Strategy: "Graduated Reciprocator"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibria while being resilient to exploitation. It starts optimistically, responds proportionally to the cooperation level observed, and includes forgiveness mechanisms to recover from coordination failures.

## Decision Rules

### Round 1 (Initialization)
- **Action: COOPERATE**
- Rationale: Start optimistically to signal cooperative intent and attempt to establish a cooperative norm

### Rounds 2 to r-1 (Main Strategy)
Use a **threshold-based reciprocal cooperation** rule:

```
cooperation_rate = (number_of_cooperators_last_round) / n
cooperation_threshold = 0.5

if cooperation_rate >= cooperation_threshold:
    action = COOPERATE
else:
    action = DEFECT
```

### Round r (Final Round)
- **Action: DEFECT**
- Rationale: In the final round, there's no future to incentivize cooperation, so rational players will likely defect. Defecting protects against exploitation.

## Enhanced Features

### 1. Forgiveness Mechanism
To handle temporary coordination failures or experimentation by other players:

```
if current_round > 2 and previous_action == DEFECT:
    # Check if cooperation rate improved from two rounds ago
    cooperation_rate_2_ago = cooperators_2_rounds_ago / n
    cooperation_rate_1_ago = cooperators_1_round_ago / n
    
    if cooperation_rate_1_ago > cooperation_rate_2_ago + 0.1:  # Improvement threshold
        action = COOPERATE  # Forgive and try to re-establish cooperation
```

### 2. Early Cooperation Establishment
For rounds 2-3, use a more lenient threshold to help establish cooperative norms:

```
if current_round <= 3:
    cooperation_threshold = 0.3  # Lower threshold early on
else:
    cooperation_threshold = 0.5  # Standard threshold
```

### 3. Endgame Adjustment
Anticipate potential endgame defection:

```
if current_round >= r - 2 and current_round < r:  # Rounds r-2 and r-1
    cooperation_threshold = 0.6  # Require higher cooperation to continue
```

## Complete Pseudocode

```python
def decide_action(current_round, round_history, n, r):
    # Round 1: Always cooperate
    if current_round == 1:
        return COOPERATE
    
    # Final round: Always defect
    if current_round == r:
        return DEFECT
    
    # Get cooperation statistics from last round
    cooperators_last = count_cooperators(round_history[-1])
    cooperation_rate = cooperators_last / n
    
    # Determine threshold based on game phase
    if current_round <= 3:
        threshold = 0.3  # Establishment phase
    elif current_round >= r - 2:
        threshold = 0.6  # Endgame phase
    else:
        threshold = 0.5  # Standard phase
    
    # Forgiveness mechanism
    if (current_round > 2 and 
        my_last_action == DEFECT and 
        len(round_history) >= 2):
        
        cooperators_2_ago = count_cooperators(round_history[-2])
        improvement = (cooperators_last - cooperators_2_ago) / n
        
        if improvement > 0.1:  # Significant improvement observed
            return COOPERATE
    
    # Standard reciprocal decision
    if cooperation_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

## Strategic Rationale

1. **Cooperative Intent**: Always starts with cooperation to signal willingness to achieve mutual benefit

2. **Proportional Response**: Responds to the overall cooperation level rather than individual players, making it robust against mixed strategies

3. **Forgiveness**: Includes mechanisms to recover from temporary coordination failures, preventing permanent breakdown of cooperation

4. **Phase Awareness**: 
   - Early phase: Lenient to establish cooperation
   - Middle phase: Standard reciprocal response
   - Late phase: More demanding due to endgame effects
   - Final round: Defect to avoid exploitation

5. **Exploitation Resistance**: The threshold-based approach prevents exploitation by small numbers of cooperators while still encouraging cooperative equilibria

This strategy balances cooperative objectives with protection against exploitation, making it suitable for tournaments where opponent strategies are unknown but assumed to be strategically rational.
'''

description_COOPERATIVE_3 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It starts cooperatively, reciprocates the group's behavior, but includes forgiveness mechanisms to recover from mutual defection cycles.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and test the group's disposition

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
```pseudocode
cooperation_threshold = n/2  // Majority threshold
forgiveness_probability = 0.3
consecutive_defections = count_my_defections_in_last_3_rounds()

previous_cooperators = count_cooperators_last_round()
group_cooperation_rate = previous_cooperators / n

if consecutive_defections >= 2:
    // Forgiveness mechanism to break defection cycles
    if random() < forgiveness_probability:
        return C
    else:
        return D
else if group_cooperation_rate >= 0.5:
    // Reciprocate cooperative group behavior
    return C
else if group_cooperation_rate >= 0.3:
    // Give benefit of doubt to moderately cooperative groups
    return C
else:
    // Protect against highly defective groups
    return D
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
recent_cooperation_rate = count_cooperators_in_last_3_rounds() / (3 * n)

if recent_cooperation_rate >= 0.4:
    return C  // Reward sustained cooperation
else:
    return D  // Avoid end-game exploitation
```

## Key Features

### 1. **Generous Starting Position**
- Always cooperates in Round 1 to signal cooperative intent
- Gives groups the benefit of the doubt initially

### 2. **Majority-Based Reciprocation**
- Cooperates when ≥50% of players cooperated in the previous round
- Maintains cooperation even with moderate cooperation (≥30%) to encourage others

### 3. **Forgiveness Mechanism**
- After defecting for 2+ consecutive rounds, has 30% chance to cooperate
- Prevents getting stuck in mutual defection equilibria
- Allows recovery from temporary coordination failures

### 4. **End-Game Protection**
- In the final round, only cooperates if recent cooperation rate ≥40%
- Balances final cooperation with protection against last-round defection

### 5. **Adaptive Thresholds**
- Uses flexible cooperation thresholds rather than strict tit-for-tat
- Accounts for the multi-player nature where perfect coordination is unlikely

## Strategic Rationale

1. **Cooperative Signaling**: Starting with cooperation signals intent and allows identification of other cooperative players

2. **Reciprocal Fairness**: Matching the group's cooperation level encourages sustained mutual cooperation

3. **Exploitation Resistance**: Defects against consistently uncooperative groups to avoid being taken advantage of

4. **Forgiveness**: Breaks out of potential defection spirals that could emerge from miscoordination

5. **Endgame Awareness**: Acknowledges that final-round incentives differ while still rewarding consistent cooperators

This strategy balances the cooperative imperative with strategic resilience, aiming to achieve high mutual cooperation while avoiding exploitation by purely selfish strategies.
'''

description_COOPERATIVE_4 = '''
# Conditional Cooperation with Graduated Reciprocation Strategy

## Overview
This strategy balances cooperative intent with protection against exploitation by using conditional cooperation based on group cooperation levels, with graduated responses to defection.

## Core Decision Rules

### Initial Cooperation Phase (First 2 rounds)
- **Round 1**: Always COOPERATE (signal cooperative intent)
- **Round 2**: Always COOPERATE (establish cooperative reputation)

### Main Strategy (Rounds 3 to r-2)
Use a **Cooperation Threshold System**:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n
personal_cooperation_rate = (my_cooperations_so_far) / (current_round - 1)

IF cooperation_rate >= 0.5:
    COOPERATE
ELSE IF cooperation_rate >= 0.3:
    IF personal_cooperation_rate > cooperation_rate:
        DEFECT (avoid being exploited)
    ELSE:
        COOPERATE (encourage cooperation)
ELSE:  // cooperation_rate < 0.3
    DEFECT (group is mostly non-cooperative)
```

### Forgiveness Mechanism
Track defection streaks and allow recovery:
```pseudocode
IF last_round_cooperation_rate >= 0.6 AND previous_cooperation_rate < 0.4:
    // Group is recovering from defection
    COOPERATE (reward improvement)
```

### Endgame Strategy (Last 2 rounds)
- **Round r-1**: Mirror the group's recent behavior
  - If cooperation_rate in last 3 rounds >= 0.5: COOPERATE
  - Otherwise: DEFECT
- **Round r**: 
  - If I've been mostly cooperative (>60% of rounds) AND group cooperation >= 0.4: COOPERATE
  - Otherwise: DEFECT

## Key Features

### 1. Conditional Cooperation
- Cooperates when group cooperation is reasonable (≥50%)
- Provides graduated response rather than binary all-or-nothing

### 2. Exploitation Protection  
- Defects when being taken advantage of (personal cooperation rate significantly higher than group rate)
- Responds to low group cooperation by defecting

### 3. Forgiveness and Recovery
- Rewards groups that improve their cooperation
- Doesn't permanently punish temporary defection

### 4. Strategic Endgame
- Maintains cooperation incentives until near the end
- Protects against final-round defection while still rewarding good partners

## Rationale

This strategy is **fundamentally cooperative** because:
- It starts with cooperation to signal good intent
- It maintains cooperation when others do the same
- It rewards cooperative behavior and group improvement
- It only defects as protection against exploitation or in clearly non-cooperative environments

The strategy handles the core tension in public goods games: wanting to achieve mutual cooperation while avoiding being the "sucker" who contributes while others free-ride. By using graduated thresholds rather than strict reciprocity, it provides more opportunities for cooperative equilibria to emerge and persist.

The graduated response system (cooperation thresholds at 50% and 30%) allows the strategy to distinguish between:
1. **High cooperation environments** (≥50%): Full cooperation
2. **Mixed environments** (30-50%): Conditional cooperation based on relative contribution
3. **Low cooperation environments** (<30%): Protection through defection

This approach should perform well against other cooperative strategies while maintaining reasonable defense against purely exploitative ones.
'''

description_COOPERATIVE_5 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with self-protection mechanisms.

## Decision Rules

### Core Logic:
1. **Start cooperatively** to signal willingness to cooperate
2. **Mirror the group's cooperative tendency** with some forgiveness
3. **Protect against exploitation** in endgame scenarios
4. **Attempt cooperation recovery** after punishment phases

### Detailed Rules:

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

PARAMETERS:
- cooperation_threshold = 0.5  // Minimum fraction of others cooperating
- forgiveness_probability = 0.2  // Chance to cooperate despite low cooperation
- endgame_protection = 3  // Rounds before end to become more cautious
- punishment_duration = 2  // Rounds to defect after severe exploitation

VARIABLES:
- consecutive_exploited = 0  // Track consecutive rounds where I cooperated but <30% others did
- in_punishment_phase = False
- punishment_rounds_left = 0

FUNCTION decide_action(round_number, game_history):
    
    // FIRST ROUND: Always cooperate to signal cooperative intent
    IF round_number == 1:
        RETURN C
    
    // ENDGAME PROTECTION: Last few rounds, be more cautious
    IF round_number > (total_rounds - endgame_protection):
        others_cooperation_rate = calculate_others_cooperation_rate(game_history, round_number-1)
        IF others_cooperation_rate < 0.6:
            RETURN D
        ELSE:
            RETURN C
    
    // PUNISHMENT PHASE: Continue defecting if in punishment
    IF in_punishment_phase:
        punishment_rounds_left = punishment_rounds_left - 1
        IF punishment_rounds_left <= 0:
            in_punishment_phase = False
            consecutive_exploited = 0
        RETURN D
    
    // MAIN DECISION LOGIC
    last_round_others_coop_rate = calculate_others_cooperation_rate(game_history, round_number-1)
    
    // Check if severely exploited (I cooperated, but <30% others did)
    IF my_last_action == C AND last_round_others_coop_rate < 0.3:
        consecutive_exploited = consecutive_exploited + 1
        IF consecutive_exploited >= 2:  // Enter punishment after 2 consecutive exploitations
            in_punishment_phase = True
            punishment_rounds_left = punishment_duration
            RETURN D
    ELSE:
        consecutive_exploited = 0
    
    // COOPERATIVE DECISION with forgiveness
    recent_cooperation_rate = calculate_others_cooperation_rate_recent(game_history, 3)  // Last 3 rounds
    
    IF recent_cooperation_rate >= cooperation_threshold:
        RETURN C
    ELSE IF random() < forgiveness_probability:  // Occasional forgiveness
        RETURN C
    ELSE:
        RETURN D

FUNCTION calculate_others_cooperation_rate(history, round):
    // Calculate what fraction of OTHER players cooperated in specified round
    total_others = n - 1
    others_cooperating = count_cooperators_in_round(history, round) - my_action_in_round(history, round)
    RETURN others_cooperating / total_others

FUNCTION calculate_others_cooperation_rate_recent(history, lookback):
    // Average cooperation rate of others over last 'lookback' rounds
    total_rate = 0
    rounds_counted = 0
    FOR i = max(1, current_round - lookback) TO current_round - 1:
        total_rate += calculate_others_cooperation_rate(history, i)
        rounds_counted += 1
    RETURN total_rate / rounds_counted
```

## Strategy Components Explained

### 1. **Cooperative Opening**
- Always cooperate in round 1 to signal cooperative intentions
- This establishes a foundation for potential mutual cooperation

### 2. **Reciprocal Cooperation**
- Cooperate when ≥50% of other players cooperated recently
- Uses a 3-round lookback window to avoid overreacting to single defections

### 3. **Generous Forgiveness**
- 20% chance to cooperate even when others' cooperation rate is below threshold
- Prevents getting stuck in mutual defection cycles
- Allows for cooperation recovery after misunderstandings

### 4. **Exploitation Protection**
- Tracks consecutive rounds where I cooperated but <30% of others did
- After 2 consecutive exploitations, enter punishment phase (defect for 2 rounds)
- This prevents being a persistent "sucker"

### 5. **Endgame Protection**
- In final 3 rounds, require 60% cooperation rate to continue cooperating
- Protects against endgame defection while still allowing cooperation with reliable partners

## Why This Strategy Works

1. **Promotes Cooperation**: Starts cooperative and rewards group cooperation
2. **Forgiveness**: Occasional generous moves help escape defection spirals
3. **Self-Protection**: Punishes severe exploitation without being overly punitive
4. **Adaptive**: Responds to recent behavior rather than just the last round
5. **Robust**: Handles various scenarios from full cooperation to heavy exploitation

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones.
'''

description_COOPERATIVE_6 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances being nice (cooperative by default), retaliatory (punishing defection), and forgiving (allowing recovery from punishment cycles).

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
```pseudocode
if (cooperation_rate_last_round >= cooperation_threshold):
    action = C
else if (consecutive_low_cooperation < forgiveness_limit):
    action = C  // Give benefit of doubt
    consecutive_low_cooperation++
else:
    action = D  // Punish sustained non-cooperation
    consecutive_low_cooperation = 0  // Reset counter after punishment
```

Where:
- `cooperation_rate_last_round = (number of cooperators in last round) / n`
- `cooperation_threshold = 0.5` (majority cooperation required)
- `forgiveness_limit = 2` (allow up to 2 consecutive rounds of low cooperation before punishing)

### Final Round: Conditional Cooperation
- **Action**: C if cooperation_rate_last_round ≥ 0.5, otherwise D
- **Rationale**: Maintain cooperative reputation while avoiding being exploited in the final round

## Strategy Parameters

1. **Cooperation Threshold**: 50% of players must cooperate for continued cooperation
2. **Forgiveness Window**: Allow 2 consecutive rounds of low cooperation before retaliating
3. **Punishment Duration**: Single round of defection as punishment
4. **Recovery Mechanism**: Immediately return to cooperation after punishment

## Handling Edge Cases

### First Round
- Always cooperate to establish cooperative intentions

### Last Round  
- Cooperate only if majority cooperated in previous round
- Prevents exploitation while maintaining cooperative stance when reciprocated

### All Players Defect Scenario
- After forgiveness window expires, defect once then return to conditional cooperation
- Avoids permanent defection cycles

### Mixed Cooperation Levels
- Use majority rule (≥50%) as threshold for continued cooperation
- Accounts for the fact that even partial cooperation generates positive returns

## Robustness Features

1. **Anti-Exploitation**: Won't be taken advantage of indefinitely due to forgiveness limits
2. **Quick Recovery**: Returns to cooperation immediately after punishment
3. **Generous**: Gives benefit of doubt for 2 rounds of low cooperation
4. **Adaptive**: Responds to overall group behavior rather than individual players
5. **End-Game Aware**: Adjusts behavior in final round to prevent exploitation

## Expected Outcomes

- **Against All Cooperators**: Mutual cooperation throughout (optimal outcome)
- **Against All Defectors**: Limited exploitation (3 rounds max) then mutual defection
- **Against Mixed Strategies**: Promotes cooperation when possible, punishes sustained non-cooperation
- **Against Other Conditional Cooperators**: Likely to establish stable cooperation

This strategy aims to foster cooperation while protecting against exploitation, making it suitable for tournament play against diverse opponent strategies.
'''

description_COOPERATIVE_7 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances trust-building with self-protection through a forgiving approach that encourages reciprocal cooperation.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Signal cooperative intent from the start to establish trust

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: Even if majority defected, still cooperate with probability based on cooperation history

**Pseudocode:**
```
if round == 1:
    return C
    
if round == r:  // Last round
    return last_round_strategy()
    
// Calculate cooperation metrics from previous round
cooperation_rate_last = count_cooperators_last_round / n
overall_cooperation_rate = total_cooperators_all_rounds / (n * (round - 1))

// Main decision logic
if cooperation_rate_last >= 0.5:
    return C  // Majority cooperated, reciprocate
else:
    // Majority defected, but consider forgiveness
    forgiveness_threshold = min(0.3, overall_cooperation_rate)
    if cooperation_rate_last >= forgiveness_threshold:
        return C  // Forgive and encourage cooperation
    else:
        return D  // Protect against heavy exploitation
```

### Final Round (Round r): Conditional Cooperation
In the last round, the strategy becomes more cautious but still maintains cooperative potential:

```
if overall_cooperation_rate >= 0.6:
    return C  // High cooperation throughout game
else if overall_cooperation_rate >= 0.4 AND cooperation_rate_last >= 0.5:
    return C  // Moderate cooperation with recent positive signal
else:
    return D  // Protect against final-round defection
```

## Key Features

### 1. **Generous Starting Position**
- Always cooperates in round 1 to signal cooperative intent
- Gives other players the benefit of the doubt initially

### 2. **Majority-Based Response**
- Uses 50% threshold for basic cooperation decision
- Responds to collective behavior rather than individual actions
- Avoids overreacting to single defectors in large groups

### 3. **Adaptive Forgiveness**
- Forgiveness threshold adapts based on historical cooperation levels
- More forgiving in generally cooperative environments
- Less forgiving when facing consistent defection

### 4. **Anti-Exploitation Protection**
- Will defect when facing sustained majority defection
- Protects against being the sole cooperator
- Maintains self-interest when cooperation breaks down

### 5. **End-Game Awareness**
- Recognizes final round dynamics where defection incentives increase
- Balances cooperation with protection against end-game defection
- Still rewards consistently cooperative groups

## Strategic Rationale

1. **Cooperative Signal**: Starting with cooperation establishes positive intent
2. **Reciprocity**: Matching majority behavior encourages mutual cooperation
3. **Stability**: Majority thresholds create stable cooperation equilibria
4. **Forgiveness**: Prevents punishment spirals that destroy cooperation
5. **Robustness**: Protects against exploitation while maintaining cooperative potential

## Expected Performance

This strategy should perform well against:
- Other cooperative strategies (mutual cooperation)
- Tit-for-tat variants (establishes cooperation quickly)
- Mixed populations (adapts to cooperation levels)

It provides protection against:
- Always-defect strategies (limits exploitation)
- End-game defectors (cautious final round)
- Noise and occasional defections (forgiveness mechanism)

The strategy aims to maximize collective welfare while maintaining individual rationality, making it both cooperative and competitively viable.
'''

description_COOPERATIVE_8 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent from the start to encourage reciprocal cooperation

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
```pseudocode
cooperation_threshold = n/2  // Majority cooperation required
forgiveness_counter = 0
max_forgiveness = 2

FOR round t = 2 to r-1:
    cooperators_last_round = count of players who played C in round t-1
    
    IF cooperators_last_round >= cooperation_threshold:
        action = C
        forgiveness_counter = 0  // Reset forgiveness
    
    ELSE IF forgiveness_counter < max_forgiveness:
        action = C  // Be generous/forgiving
        forgiveness_counter += 1
    
    ELSE:
        action = D  // Protect against persistent exploitation
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
cooperators_last_round = count of players who played C in round r-1
recent_cooperation_rate = average cooperation over last 3 rounds (or all rounds if r ≤ 4)

IF recent_cooperation_rate >= 0.4 AND cooperators_last_round >= n/3:
    action = C  // Reward consistent cooperators even in final round
ELSE:
    action = D  // Standard end-game defection
```

## Key Features

### 1. Majority-Based Threshold
- Cooperates when at least half the players cooperated in the previous round
- This creates a stable equilibrium where cooperation begets cooperation

### 2. Forgiveness Mechanism
- Continues cooperating for up to 2 rounds even when cooperation drops below threshold
- Prevents punishment spirals from temporary coordination failures
- Allows recovery from accidental defection cascades

### 3. Protection Against Exploitation
- After exhausting forgiveness, switches to defection until cooperation recovers
- Prevents being exploited by consistently defecting players

### 4. Final Round Consideration
- Unlike pure strategies that always defect in the last round, this strategy rewards groups that maintained cooperation
- Only cooperates in final round if there's evidence of sustained cooperative behavior

## Edge Case Handling

### Small Groups (n = 2-3)
- Threshold automatically adjusts (n/2 means 1+ cooperators needed)
- More sensitive to individual actions, encouraging careful play

### High Multiplication Factor (k close to n)
- Strategy becomes more forgiving as cooperation becomes more valuable
- The forgiveness mechanism helps capture these gains

### Low Multiplication Factor (k close to 1)
- Strategy becomes more defensive but still attempts cooperation
- Protects against losses when public good value is marginal

## Expected Outcomes

1. **Against other cooperators**: Mutual cooperation for most rounds, maximizing joint payoffs
2. **Against mixed strategies**: Establishes cooperation when possible, defends when necessary
3. **Against pure defectors**: Initially attempts cooperation, then protects through defection
4. **Against strategic players**: The forgiveness mechanism helps coordinate through temporary missteps

This strategy balances the cooperative imperative with practical considerations for tournament survival, aiming to achieve high payoffs through sustained cooperation while avoiding exploitation.
'''

description_COOPERATIVE_9 = '''
# Cooperative Strategy: "Graduated Reciprocator"

## Core Philosophy
This strategy aims to maximize collective welfare while maintaining individual rationality through adaptive cooperation based on observed group behavior.

## Decision Rules

### Round 1: Optimistic Start
- **Always COOPERATE** in the first round
- Rationale: Signal cooperative intent and test the waters for group cooperation level

### Rounds 2 to r-1: Adaptive Reciprocation
Use a threshold-based system that adjusts to group cooperation patterns:

```pseudocode
cooperation_threshold = max(0.3, observed_cooperation_rate * 0.8)

if (cooperation_rate_last_round >= cooperation_threshold):
    action = COOPERATE
else:
    action = DEFECT
```

Where:
- `cooperation_rate_last_round` = (number of cooperators in previous round) / n
- `observed_cooperation_rate` = running average of cooperation rates across all previous rounds

### Round r (Final Round): Conditional Cooperation
```pseudocode
if (average_cooperation_rate >= 0.4):
    action = COOPERATE
else:
    action = DEFECT
```

## Key Features

### 1. Forgiveness Mechanism
- The threshold uses `0.8` multiplier, meaning we cooperate even when group cooperation drops slightly
- Minimum threshold of 0.3 prevents complete abandonment of cooperation

### 2. Exploitation Protection
- If group cooperation falls below 30%, switch to defection to avoid being exploited
- Dynamic threshold adjustment prevents manipulation by temporarily high cooperation

### 3. End-Game Handling
- Final round decision based on overall game history rather than just recent rounds
- Maintains cooperation if the group has shown reasonable cooperative behavior (≥40% average)

## Strategic Rationale

### Cooperative Alignment
- Starts cooperatively and maintains cooperation when reciprocated
- Contributes to public good when others do the same
- Higher payoffs for everyone when mutual cooperation emerges

### Individual Protection
- Defects when facing predominantly defecting opponents
- Avoids the "sucker's payoff" of unilateral cooperation
- Adapts threshold based on observed behavior patterns

### Tournament Effectiveness
- Performs well against other cooperative strategies through reciprocation
- Protects against exploitative strategies through threshold mechanism
- Balances individual rationality with group welfare maximization

## Example Scenarios

**High Cooperation Group**: If 4+ players consistently cooperate, threshold stays high (~0.5-0.6), leading to sustained mutual cooperation and payoffs approaching 2.0 per round.

**Mixed Group**: If cooperation fluctuates around 50%, strategy adapts threshold to ~0.4, cooperating when sufficient others do, defecting when they don't.

**Low Cooperation Group**: If few players cooperate, threshold drops to 0.3 minimum, leading to mostly defection but occasional cooperation attempts to test for group recovery.

This strategy is truly cooperative in that it seeks to establish and maintain cooperative equilibria while being robust enough to survive in a tournament against diverse opponent strategies.
'''

description_COOPERATIVE_10 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Majority Threshold"

## Core Philosophy
This strategy aims to promote cooperation while protecting against exploitation by adapting to the group's cooperative behavior and maintaining resilience against defectors.

## Decision Rules

### Round 1: Cooperative Start
- **Always COOPERATE** in the first round to signal cooperative intent and give the group the best chance to establish a cooperative equilibrium.

### Rounds 2 to r-1: Adaptive Cooperation
The strategy uses a **majority threshold** system with **generous forgiveness**:

```pseudocode
IF round == 1:
    return COOPERATE

cooperation_rate = (total_cooperators_last_round) / n

IF cooperation_rate >= 0.5:
    return COOPERATE
ELSE:
    // Generous forgiveness: still cooperate if close to majority
    IF cooperation_rate >= 0.4:
        return COOPERATE
    ELSE:
        return DEFECT
```

### Final Round (r): Conditional Cooperation
Despite the standard game theory prediction of defection in the last round, maintain cooperative stance if the group has shown consistent cooperation:

```pseudocode
IF round == r:
    recent_cooperation_rate = average_cooperation_rate_last_3_rounds
    IF recent_cooperation_rate >= 0.6:
        return COOPERATE  // Reward consistent group cooperation
    ELSE:
        return DEFECT     // Protect against end-game defection
```

## Strategy Components

### 1. Majority Threshold Logic
- **Cooperate** when ≥50% of players cooperated in the previous round
- This creates a clear, predictable rule that other cooperative strategies can recognize and reciprocate

### 2. Generous Forgiveness
- **Still cooperate** when cooperation rate is 40-49%
- Prevents spiral into mutual defection due to small fluctuations
- Accounts for the fact that even one or two defectors shouldn't destroy group cooperation

### 3. Protection Against Exploitation
- **Defect** when cooperation rate falls below 40%
- Signals that persistent defection will not be rewarded
- Creates incentive for defectors to return to cooperation

### 4. End-Game Consideration
- Maintains cooperation in final round if group has been consistently cooperative (≥60% in last 3 rounds)
- This rewards groups that maintain cooperation and potentially leads to better outcomes for all

## Edge Cases

- **All players defected last round**: DEFECT (cooperation_rate = 0)
- **Exactly half cooperated**: COOPERATE (meets 0.5 threshold)
- **First few rounds with mixed results**: The generous threshold (0.4) provides stability
- **Games with very few rounds (r ≤ 3)**: Strategy still works, with first round cooperation and final round conditional on recent history

## Rationale

1. **Promotes Cooperation**: Starts cooperatively and maintains cooperation when others do
2. **Clear Signaling**: The majority threshold is easy for other strategies to understand and reciprocate
3. **Robust Against Defectors**: Won't be exploited by persistent defectors
4. **Generous**: The 0.4 threshold prevents accidental defection spirals
5. **Group-Oriented**: Considers collective behavior rather than individual player tracking
6. **Adaptive**: Responds to changing group dynamics while maintaining cooperative stance

This strategy should perform well against other cooperative strategies while maintaining reasonable protection against exploitation, making it effective in a mixed tournament environment.
'''

description_COOPERATIVE_11 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances generosity with accountability to maximize collective welfare.

## Decision Rules

### Round 1: Cooperative Opening
- **Always cooperate** in the first round to signal cooperative intent

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = n/2  // Majority threshold
defection_strikes = 0       // Track consecutive punishment rounds
max_strikes = 2            // Maximum punishment duration

for each round t (where 2 ≤ t ≤ r-1):
    cooperators_last_round = count of players who played C in round t-1
    
    if defection_strikes > 0:
        // Currently in punishment mode
        defection_strikes -= 1
        return DEFECT
    
    elif cooperators_last_round >= cooperation_threshold:
        // Majority cooperated - reciprocate cooperation
        return COOPERATE
    
    elif cooperators_last_round < cooperation_threshold:
        // Majority defected - enter punishment mode
        defection_strikes = max_strikes
        return DEFECT
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
// In final round, cooperate if cooperation has been profitable
total_cooperators_so_far = sum of all cooperation across all previous rounds
average_cooperation_rate = total_cooperators_so_far / (n * (r-1))

if average_cooperation_rate >= 0.4:  // 40% threshold
    return COOPERATE
else:
    return DEFECT
```

## Strategy Components Explained

### 1. **Generous Opening**
- Always cooperate in Round 1 to establish good faith
- This signals cooperative intent to other potential cooperators

### 2. **Majority-Based Reciprocity**
- Cooperate when majority (≥n/2) cooperated in previous round
- This creates positive feedback loops and rewards collective cooperation
- Prevents exploitation by small groups of persistent defectors

### 3. **Limited Punishment**
- When majority defects, enter punishment mode for exactly 2 rounds
- This discourages mass defection while avoiding permanent retaliation spirals
- The fixed duration prevents endless punishment cycles

### 4. **Forgiveness Mechanism**
- After punishment period, immediately return to cooperation-testing
- This allows recovery from temporary coordination failures
- Prevents the strategy from getting stuck in permanent defection

### 5. **End-Game Consideration**
- Final round decision based on historical cooperation levels
- Cooperates if the game has been sufficiently cooperative (≥40% rate)
- Prevents end-game exploitation while rewarding sustained cooperation

## Handling Edge Cases

- **All players defect consistently**: Strategy will alternate between 2-round punishment and 1-round cooperation attempts
- **Mixed cooperation patterns**: Strategy adapts round-by-round based on majority behavior
- **Late-game defection waves**: Limited punishment prevents overreaction
- **Single defector in cooperative group**: Strategy continues cooperating with majority
- **Two-player game (n=2)**: Becomes pure tit-for-tat with 2-round punishment

## Cooperative Alignment

This strategy is fundamentally cooperative because it:
1. **Starts cooperatively** and seeks to establish mutual cooperation
2. **Rewards collective cooperation** by continuing to cooperate when others do
3. **Uses measured punishment** rather than permanent retaliation
4. **Actively forgives** and attempts to rebuild cooperation
5. **Considers group welfare** by responding to majority behavior rather than individual defectors

The strategy aims to create stable cooperative equilibria while maintaining enough deterrent against exploitation to be viable in competitive environments.
'''

description_COOPERATIVE_12 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to build and maintain cooperation by following the majority behavior while being forgiving of occasional defections. It assumes that other AI agents, being rational, will recognize the mutual benefits of cooperation in this public goods game.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give other players the benefit of the doubt

### Rounds 2 to r-1: Adaptive Majority Following
```pseudocode
cooperation_rate = count_cooperators_last_round / n

if cooperation_rate >= 0.5:
    action = COOPERATE
else:
    // Check if cooperation is trending upward
    if rounds_played >= 3:
        prev_cooperation_rate = count_cooperators_two_rounds_ago / n
        if cooperation_rate > prev_cooperation_rate:
            action = COOPERATE  // Forgive and encourage recovery
        else:
            action = DEFECT     // Follow the majority to avoid exploitation
    else:
        action = DEFECT
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
if total_cooperation_rate_so_far >= 0.4:
    action = COOPERATE  // Reward overall cooperative behavior
else:
    action = DEFECT     // Protect against last-round defection
```

## Key Features

### 1. Majority Sensitivity
- Cooperates when ≥50% of players cooperated in the previous round
- This creates a natural coordination point and reduces exploitation risk

### 2. Forgiveness Mechanism
- If cooperation rate is increasing (even if below 50%), still cooperate
- Gives players a chance to recover from mutual defection spirals
- Helps break out of inefficient equilibria

### 3. Protection Against Exploitation
- Defects when cooperation is consistently low
- Avoids being a "sucker" in highly defective environments

### 4. End-Game Consideration
- Final round decision based on overall game cooperation
- Rewards groups that maintained reasonable cooperation levels
- Protects against predictable last-round defection cascades

## Strategic Rationale

### Cooperative Alignment
- **First Round Cooperation**: Shows good faith and willingness to build mutual benefit
- **Majority Following**: Creates stable cooperation when others are willing
- **Forgiveness**: Helps recover from coordination failures
- **Conditional Final Cooperation**: Rewards cooperative groups while avoiding exploitation

### Game-Theoretic Soundness
- Avoids being consistently exploited by always-defect strategies
- Provides incentives for others to maintain cooperation
- Adapts to the actual behavior observed rather than rigid assumptions
- Balances individual rationality with group efficiency

### Tournament Considerations
Against other AI strategies likely to be somewhat rational:
- Rewards mutual cooperation when possible
- Protects against aggressive strategies
- Provides clear signals about cooperation conditions
- Maintains flexibility to adapt to different opponent mixes

This strategy should perform well in environments with a mix of cooperative and selfish strategies, while maintaining the cooperative spirit requested.
'''

description_COOPERATIVE_13 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperativeness with self-protection through a forgiving yet responsive approach.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Signal cooperative intent from the start, as this is the only way to potentially establish mutual cooperation.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the **majority** of other players cooperated in the previous round
- **Forgiveness Mechanism**: Even if the majority defected last round, still cooperate with probability based on the cooperation ratio:
  - If cooperation_ratio ≥ 0.5: Always cooperate
  - If 0.3 ≤ cooperation_ratio < 0.5: Cooperate with 70% probability
  - If 0.1 ≤ cooperation_ratio < 0.3: Cooperate with 40% probability
  - If cooperation_ratio < 0.1: Defect (but return to cooperation next round if any improvement is shown)

### Round r (Final Round): Generous Final Move
- **Action**: C (Cooperate)
- **Rationale**: Avoid the typical last-round defection cascade by maintaining cooperation, potentially encouraging others to do the same.

## Pseudocode

```
function decide_action(round_number, total_rounds, history):
    if round_number == 1:
        return C
    
    if round_number == total_rounds:  // Final round
        return C
    
    // Calculate cooperation ratio from previous round
    previous_round = history[round_number - 1]
    other_players_actions = previous_round.exclude(my_action)
    cooperation_count = count(other_players_actions, C)
    total_others = length(other_players_actions)
    cooperation_ratio = cooperation_count / total_others
    
    // Apply conditional cooperation with forgiveness
    if cooperation_ratio >= 0.5:
        return C
    elif cooperation_ratio >= 0.3:
        return random_choice([C, D], probabilities=[0.7, 0.3])
    elif cooperation_ratio >= 0.1:
        return random_choice([C, D], probabilities=[0.4, 0.6])
    else:
        return D
```

## Edge Case Handling

### First Round
- Always cooperate to signal cooperative intent and provide the best chance for establishing mutual cooperation.

### Last Round
- Cooperate to avoid triggering a defection cascade in the final rounds, maintaining the cooperative equilibrium.

### All-Defection Scenarios
- If facing consistent universal defection (cooperation_ratio = 0) for multiple rounds, briefly defect but immediately return to testing cooperation in the next round.

### Mixed Cooperation Patterns
- Use the graduated forgiveness mechanism to maintain some cooperation even when facing partial defection, encouraging return to cooperation.

## Cooperative Alignment

This strategy embodies cooperativeness through:

1. **Initial Trust**: Starting with cooperation signals willingness to contribute to the public good
2. **Forgiveness**: Not immediately punishing single instances of defection, allowing for mistakes or temporary strategy shifts
3. **Majority-Based Response**: Responding to the overall group tendency rather than individual players, promoting group welfare
4. **Final Round Cooperation**: Resisting the temptation to defect in the last round, maintaining group benefits
5. **Graduated Response**: Not switching immediately to full defection, maintaining some cooperation even under adverse conditions

This strategy should perform well against other cooperative strategies while maintaining reasonable protection against exploitation, ultimately contributing to higher group payoffs through sustained cooperation.
'''

description_COOPERATIVE_14 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being "nice" (cooperative by default) with being "retaliatory" (punishing sustained defection) and "forgiving" (allowing recovery from punishment phases).

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent from the start to encourage reciprocal cooperation

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = 0.5  // Require majority cooperation to continue cooperating
forgiveness_probability = 0.1  // 10% chance to cooperate even when conditions aren't met

total_cooperators_last_round = count of players who played C in previous round
cooperation_rate_last_round = total_cooperators_last_round / n

if cooperation_rate_last_round >= cooperation_threshold:
    action = C
else:
    if random() < forgiveness_probability:
        action = C  // Occasional forgiveness to break negative cycles
    else:
        action = D  // Punish low cooperation
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
// More lenient in final round to avoid end-game defection cascade
final_threshold = 0.3  // Lower threshold for final round

cooperation_rate_last_round = total_cooperators_last_round / n

if cooperation_rate_last_round >= final_threshold:
    action = C
else:
    action = D
```

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative reputation and encourage reciprocity

### Early Rounds (Rounds 2-3)
- Use slightly more lenient threshold (0.4 instead of 0.5) to allow cooperation to stabilize
- Higher forgiveness probability (0.15) to give benefit of doubt

### Mid-Game Rounds
- Standard thresholds apply
- Track patterns: if cooperation rate has been declining for 3+ consecutive rounds, temporarily increase punishment (reduce forgiveness to 0.05)

### Final Round
- Lower cooperation threshold (0.3) to account for expected end-game effects
- Still cooperate if recent cooperation levels justify it

## Key Features

### 1. **Majority-Based Decision Making**
- Cooperates when majority of players cooperated in previous round
- Accounts for the fact that even with some defectors, cooperation can still be profitable

### 2. **Forgiveness Mechanism**
- 10% chance to cooperate even when cooperation rate is below threshold
- Prevents permanent punishment cycles
- Allows recovery from temporary cooperation breakdowns

### 3. **Graduated Response**
- Not purely binary - uses probabilistic forgiveness rather than harsh all-or-nothing punishment
- Adapts punishment intensity based on recent trends

### 4. **End-Game Awareness**
- Recognizes that final round may see increased defection
- Adjusts expectations accordingly while still rewarding recent cooperation

## Strategic Rationale

1. **Encourages Cooperation**: By starting cooperatively and rewarding group cooperation, it incentivizes others to cooperate

2. **Robust to Exploitation**: The majority threshold prevents a few defectors from derailing group cooperation

3. **Recoverable**: Forgiveness mechanism allows the group to recover from temporary cooperation breakdowns

4. **Realistic**: Acknowledges that perfect cooperation may not be achievable and optimizes for "good enough" cooperation levels

5. **Tournament-Aware**: Designed to work well against diverse strategies, from always-cooperate to tit-for-tat variants

This strategy should perform well against other cooperative strategies while maintaining reasonable payoffs against more exploitative approaches.
'''

description_COOPERATIVE_15 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy balances cooperative intent with protection against exploitation, using measured responses to encourage collective cooperation while maintaining individual viability.

## Decision Rules

### Round 1: Optimistic Start
**Always COOPERATE** in the first round to signal cooperative intent and test the waters.

### Rounds 2 to r-1: Adaptive Response
Use a **majority-based threshold system** with forgiveness:

```pseudocode
cooperation_threshold = ceil(n/2)  // At least half the players
forgiveness_probability = 0.15     // 15% chance to cooperate despite low cooperation

if (cooperators_last_round >= cooperation_threshold):
    action = COOPERATE
else:
    if (random() < forgiveness_probability):
        action = COOPERATE  // Occasional forgiveness to break punishment cycles
    else:
        action = DEFECT
```

### Final Round: Conditional Cooperation
In the last round, use recent cooperation history to decide:

```pseudocode
recent_cooperation_rate = cooperators_in_last_3_rounds / (3 * n)

if (recent_cooperation_rate >= 0.4):  // 40% threshold
    action = COOPERATE
else:
    action = DEFECT  // Protect against end-game defection
```

## Key Features

### 1. Majority Threshold Logic
- Cooperate when at least ⌈n/2⌉ players cooperated in the previous round
- This creates a stable equilibrium point where cooperation is rewarded
- Protects against being the sole cooperator in a sea of defectors

### 2. Forgiveness Mechanism
- 15% probability of cooperating even when cooperation is below threshold
- Prevents permanent punishment spirals
- Allows recovery from coordination failures
- Creates opportunities to restart cooperative cycles

### 3. End-Game Protection
- Uses 3-round historical average in final round
- Lower threshold (40%) acknowledges end-game dynamics
- Balances optimism with realism about final-round incentives

### 4. Edge Case Handling
- **First round**: Always cooperate (signal cooperative intent)
- **Two-player games**: Threshold becomes 1, essentially pure tit-for-tat with forgiveness
- **High n games**: Threshold scales appropriately, preventing free-riding

## Strategic Rationale

### Cooperative Alignment
- Starts cooperatively and rewards group cooperation
- Forgiveness mechanism actively tries to rebuild cooperation
- Only defects when cooperation levels are genuinely low

### Exploitation Protection
- Won't be consistently exploited due to majority threshold
- Responds to widespread defection with temporary defection
- Final round protection against end-game exploitation

### Coordination Facilitation
- Clear, predictable response pattern helps others coordinate
- Majority threshold creates focal point for cooperation
- Forgiveness provides escape valve from mutual punishment

## Expected Tournament Performance

This strategy should perform well against:
- **Other cooperative strategies**: Mutual cooperation through threshold satisfaction
- **Tit-for-tat variants**: Stable cooperation with occasional forgiveness resets
- **Mixed strategies**: Adapts to prevailing cooperation levels

The strategy balances the cooperative imperative with practical considerations, creating a robust approach that maintains cooperative intent while protecting against systematic exploitation.
'''

description_COOPERATIVE_16 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibrium while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through measured responses to betrayal.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Signal cooperative intent from the start

**Rounds 2 to r-1 (Main Strategy):**
- **Cooperation Threshold**: Calculate cooperation rate of all other players in previous round
- **Base Rule**: COOPERATE if group cooperation rate ≥ 50% in previous round
- **Forgiveness Mechanism**: If group cooperation rate < 50%, still COOPERATE with probability 20% (forgiveness)
- **Punishment Phase**: If cooperation rate drops below 25% for 2 consecutive rounds, switch to DEFECT until cooperation rate recovers above 50%

**Round r (Final Round):**
- **Conditional Cooperation**: COOPERATE only if group cooperation rate ≥ 75% in round r-1
- This prevents end-game exploitation while rewarding sustained cooperation

### Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    # Calculate cooperation rate of others in previous round
    prev_round = history[round_number - 1]
    others_cooperation_rate = (sum(prev_round) - my_previous_action) / (n - 1)
    
    if round_number == r:  # Final round
        if others_cooperation_rate >= 0.75:
            return COOPERATE
        else:
            return DEFECT
    
    # Check if in punishment phase
    if is_punishment_phase(history, round_number):
        if others_cooperation_rate > 0.5:
            exit_punishment_phase()
            return COOPERATE
        else:
            return DEFECT
    
    # Main strategy logic
    if others_cooperation_rate >= 0.5:
        return COOPERATE
    elif others_cooperation_rate >= 0.25:
        # Forgiveness mechanism
        if random() < 0.2:
            return COOPERATE
        else:
            return DEFECT
    else:
        # Check if punishment phase should begin
        if check_consecutive_low_cooperation(history, round_number):
            enter_punishment_phase()
        return DEFECT

function is_punishment_phase(history, round):
    # Check last 2 rounds for cooperation rate < 25%
    if round < 3:
        return false
    
    last_two_rounds = history[round-2:round]
    for each round_data in last_two_rounds:
        others_rate = (sum(round_data) - my_action_that_round) / (n - 1)
        if others_rate >= 0.25:
            return false
    return true
```

## Key Features

### 1. **Graduated Response**
- Responds proportionally to the level of cooperation observed
- Doesn't immediately punish minor defections
- Escalates only when faced with sustained non-cooperation

### 2. **Forgiveness Mechanism**
- 20% chance to cooperate even when group cooperation is below threshold
- Prevents permanent defection spirals
- Allows recovery from temporary coordination failures

### 3. **End-Game Protection**
- Higher cooperation threshold (75%) in final round
- Prevents exploitation by opponents who defect only in the last round
- Still rewards groups that maintain high cooperation throughout

### 4. **Punishment Phase**
- Triggered only by sustained low cooperation (< 25% for 2 rounds)
- Clear exit condition (cooperation rate > 50%)
- Provides strong incentive for others to return to cooperation

## Strategic Rationale

### Cooperative Alignment
- **Primary Goal**: Maximize collective welfare through sustained cooperation
- **Initial Signal**: Always cooperates first to signal cooperative intent
- **Forgiveness**: Maintains cooperation opportunity even after setbacks

### Defensive Measures
- **Threshold-Based**: Uses cooperation rates rather than absolute numbers
- **Graduated Response**: Proportional punishment prevents overreaction
- **Recovery Mechanism**: Clear path back to mutual cooperation

### Tournament Considerations
- **Robust Against Exploiters**: Punishment phase deters consistent defectors
- **Cooperative with Cooperators**: High cooperation rate with like-minded strategies
- **Adaptive**: Responds to group dynamics rather than individual behaviors
- **Resilient**: Forgiveness mechanism prevents permanent breakdown

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitation, making it effective in a mixed-strategy tournament environment.
'''

description_COOPERATIVE_17 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Collective Assessment"

## Core Philosophy
This strategy aims to foster cooperation while being robust against exploitation. It balances optimism about others' cooperative potential with practical defenses against persistent defectors.

## Strategy Description

### Decision Rules

**Round 1: Unconditional Cooperation**
- Always cooperate in the first round to signal cooperative intent

**Rounds 2 to r-1: Collective Assessment with Forgiveness**
- Define cooperation threshold: `threshold = n/2` (majority cooperation)
- Track recent cooperation levels over a sliding window of the last 3 rounds (or all available rounds if fewer than 3)

```pseudocode
if round <= 3:
    cooperation_rate = (total_cooperators_in_previous_rounds) / ((round-1) * n)
else:
    cooperation_rate = (total_cooperators_in_last_3_rounds) / (3 * n)

if cooperation_rate >= 0.5:
    action = COOPERATE
else if cooperation_rate >= 0.3:
    // Generous forgiveness zone - cooperate with probability 0.7
    action = COOPERATE (with 70% probability), DEFECT (with 30% probability)
else:
    action = DEFECT
```

**Final Round (round r): Conditional Cooperation**
- If cooperation rate in the last 3 rounds ≥ 0.4: COOPERATE
- Otherwise: DEFECT

### Key Features

1. **Generous Start**: Begin with cooperation to establish a cooperative norm
2. **Collective Focus**: Make decisions based on overall group behavior rather than tracking individual players
3. **Sliding Window**: Use recent history (last 3 rounds) to adapt to changing group dynamics
4. **Forgiveness Zone**: Between 30-50% cooperation rates, still cooperate most of the time to help restart cooperation
5. **End-game Consideration**: Slightly lower threshold for final round cooperation to account for end-game effects

### Edge Case Handling

- **Very Low n (n=2,3)**: Threshold becomes `max(1, n/2)` to ensure at least one cooperator is needed
- **Very High k (k close to n)**: Strategy remains unchanged as the collective benefit calculation already accounts for this
- **Short Games (r≤3)**: Use all available history rather than 3-round window

### Rationale

This strategy is designed to:
- **Encourage Cooperation**: Start cooperatively and maintain cooperation when others do
- **Resist Exploitation**: Defect when cooperation levels are consistently low
- **Enable Recovery**: Provide opportunities for cooperation to restart through the forgiveness zone
- **Adapt Quickly**: Use recent history to respond to changing group dynamics
- **Handle Tournament Setting**: Work effectively without communication or coordination, relying only on observable actions

The strategy recognizes that in a tournament of AI strategies, some will be purely cooperative, some purely selfish, and others conditional. By focusing on collective behavior patterns and maintaining generous but not naive cooperation, it aims to do well with fellow cooperators while protecting against exploitation.
'''

description_COOPERATIVE_18 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the start

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This is the first time cooperation rate dropped below 50% in the last 3 rounds, OR
- The cooperation rate is ≥ 33% (showing some players are still trying to cooperate)

**Defection Trigger**: Only defect if:
- Cooperation rate < 50% AND cooperation rate < 33% AND this has happened in at least 2 of the last 3 rounds

### Final Round: Conditional Cooperation
- **Action**: COOPERATE if average cooperation rate over all previous rounds ≥ 40%
- **Action**: DEFECT otherwise
- **Rationale**: Reward generally cooperative players even in the final round, but protect against exploitation in clearly non-cooperative environments

## Pseudocode

```python
def decide_action(round_num, history, n, r):
    if round_num == 1:
        return COOPERATE
    
    # Calculate cooperation rate in previous round
    prev_round_cooperators = count_cooperators(history[round_num-2])
    prev_coop_rate = prev_round_cooperators / n
    
    if round_num == r:  # Final round
        overall_coop_rate = calculate_overall_cooperation_rate(history)
        return COOPERATE if overall_coop_rate >= 0.4 else DEFECT
    
    # Rounds 2 to r-1
    if prev_coop_rate >= 0.5:
        return COOPERATE
    
    # Forgiveness mechanisms
    if prev_coop_rate >= 0.33:
        return COOPERATE
    
    # Check if this is first time below 50% in last 3 rounds
    if round_num <= 4:  # Not enough history for 3-round check
        return COOPERATE
    
    recent_low_coop_rounds = 0
    for i in range(max(0, round_num-4), round_num-1):
        round_coop_rate = count_cooperators(history[i]) / n
        if round_coop_rate < 0.5:
            recent_low_coop_rounds += 1
    
    if recent_low_coop_rounds <= 1:
        return COOPERATE  # First time, be forgiving
    
    return DEFECT  # Pattern of low cooperation established
```

## Key Features

### 1. **Generous Opening**: 
Always cooperates in round 1 to signal cooperative intent and give cooperation a chance to emerge.

### 2. **Majority-Based Cooperation**: 
Continues cooperating as long as at least half the players cooperated in the previous round, maintaining the cooperative equilibrium when it exists.

### 3. **Graduated Forgiveness**: 
- Forgives occasional drops in cooperation (first-time forgiveness)
- Maintains cooperation even when majority defects if a substantial minority (≥33%) still cooperates
- Only switches to defection when facing persistent low cooperation

### 4. **Final Round Cooperation**: 
Unlike pure game-theoretic strategies that always defect in the final round, this strategy cooperates if the overall game has been reasonably cooperative, rewarding cooperative players and maintaining group welfare.

### 5. **Protection Against Exploitation**: 
Will eventually defect if faced with persistent widespread defection, preventing exploitation while giving cooperation maximum opportunity to succeed.

## Strategic Rationale

This strategy addresses the key challenges of the public goods game:
- **Free-rider problem**: Responds to defection but with forgiveness to avoid destructive spirals
- **Coordination problem**: Uses simple, observable thresholds that other cooperative strategies can learn and reciprocate
- **End-game effects**: Mitigates final-round defection through conditional cooperation
- **Noise tolerance**: Forgiveness mechanisms prevent temporary miscoordination from destroying cooperation

The strategy is designed to work well against other cooperative strategies while protecting against persistent defectors, making it robust in a tournament setting with diverse opponents.
'''

description_COOPERATIVE_19 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through measured responses to defection.

## Decision Rules

### Round 1: Cooperative Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the beginning

### Rounds 2 to r-1: Adaptive Response
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total_cooperators_last_round) / n
    
    If cooperation_rate ≥ 0.5:
        // Majority cooperated - reward with cooperation
        Action = COOPERATE
    
    Else if cooperation_rate ≥ 0.3:
        // Mixed behavior - cooperate with probability based on cooperation rate
        cooperation_probability = 0.4 + cooperation_rate
        Action = COOPERATE with probability cooperation_probability, else DEFECT
    
    Else:
        // Low cooperation - defect but leave door open for recovery
        If cooperation_rate > 0:
            Action = COOPERATE with probability 0.2  // Generous forgiveness
        Else:
            Action = DEFECT  // Full defection gets punished
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
For final round r:
    recent_cooperation = average cooperation rate over last min(3, r-1) rounds
    
    If recent_cooperation ≥ 0.6:
        Action = COOPERATE  // Reward sustained cooperation
    Else if recent_cooperation ≥ 0.3:
        Action = COOPERATE with probability 0.5  // Mixed response
    Else:
        Action = DEFECT  // Protect against end-game defection
```

## Key Features

### 1. Cooperative Foundation
- Starts cooperatively to signal good intentions
- Maintains cooperation when others reciprocate (≥50% cooperation rate)
- Always leaves room for forgiveness and recovery

### 2. Graduated Response
- **High cooperation (≥50%)**: Full cooperation to maintain the cooperative equilibrium
- **Medium cooperation (30-49%)**: Probabilistic cooperation to encourage better behavior while protecting against exploitation
- **Low cooperation (<30%)**: Primarily defect but maintain small cooperation probability to allow recovery

### 3. Forgiveness Mechanism
- Even when cooperation rates are low, maintains 20% cooperation probability (except in full defection scenarios)
- Prevents permanent breakdown of cooperation due to temporary coordination failures
- Allows the group to recover from defection spirals

### 4. End-Game Consideration
- Uses recent history rather than just the previous round to make final decision
- Balances rewarding sustained cooperators while protecting against those who might defect knowing the game is ending

### 5. Robustness Features
- **Memory**: Considers patterns rather than just single-round outcomes
- **Noise tolerance**: Probabilistic responses prevent overreaction to random defections
- **Recovery oriented**: Always maintains paths back to full cooperation

## Strategic Rationale

1. **Social Efficiency**: When successful in establishing cooperation, achieves the socially optimal outcome where all players earn 2k/n per round rather than 1

2. **Exploitation Resistance**: Graduated response prevents being systematically exploited by always-defect strategies

3. **Coordination**: Clear thresholds (50% for full cooperation) can help coordinate expectations among multiple cooperative strategies

4. **Adaptability**: Responds to the actual behavior observed rather than assuming specific opponent strategies

This strategy is designed to be "nice" (starts cooperatively), "retaliatory" (responds to defection), "forgiving" (allows recovery), and "clear" (has predictable thresholds that other cooperative strategies can learn and coordinate around).
'''

description_COOPERATIVE_20 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the start

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: Even if majority defected, still cooperate with probability based on cooperation rate
- **Exploitation Protection**: If cooperation rate drops below critical threshold for multiple consecutive rounds, switch to defensive mode

**Detailed Logic**:
```pseudocode
cooperation_rate = (number of cooperators in previous round) / n
consecutive_low_cooperation = count of consecutive rounds with cooperation_rate < 0.3

if consecutive_low_cooperation >= 2:
    // Defensive mode - only cooperate if very high cooperation
    if cooperation_rate >= 0.8:
        action = C
    else:
        action = D
else:
    // Normal cooperative mode
    if cooperation_rate >= 0.5:
        action = C
    else if cooperation_rate >= 0.3:
        // Forgiveness: cooperate with probability equal to cooperation rate
        action = C with probability = cooperation_rate
    else:
        action = D
```

### Final Round (Round r): Conditional Cooperation
- **Action**: Cooperate only if cooperation rate in round r-1 was ≥ 0.6
- **Rationale**: Maintain cooperative reputation for potential future interactions while avoiding being exploited when there's no future to incentivize others

## Edge Case Handling

### First Round
- Always cooperate to signal cooperative intent and attempt to establish cooperative equilibrium

### Last Round  
- Use higher threshold (60%) for cooperation to balance maintaining cooperative reputation against end-game defection incentives

### Low Participation Scenarios
- If cooperation rate falls below 30% for 2+ consecutive rounds, enter "defensive mode"
- In defensive mode, require 80% cooperation rate to resume cooperation
- This prevents persistent exploitation while allowing recovery if group returns to cooperation

### High Volatility Scenarios
- Track cooperation rate trends over last 3 rounds
- If high volatility detected (cooperation swinging between high/low), use more conservative thresholds

## Cooperative Alignment

This strategy embodies cooperation through:

1. **Initial Trust**: Always cooperating in round 1 demonstrates good faith
2. **Reciprocity**: Responding positively to group cooperation encourages continued collaboration
3. **Forgiveness**: Probabilistic cooperation even when majority defects prevents permanent breakdown
4. **Graduated Response**: Not immediately punishing single instances of low cooperation
5. **Recovery Mechanism**: Allowing return to cooperation when group behavior improves

## Strategic Rationale

- **Against other cooperators**: Establishes and maintains mutual cooperation
- **Against mixed strategies**: Encourages cooperation while protecting against systematic exploitation  
- **Against defectors**: Provides measured response that can recover if defectors change behavior
- **Robust to noise**: Forgiveness mechanism prevents accidental defection spirals

The strategy achieves cooperation by being "nice" (never defecting first), "retaliatory" (responding to persistent defection), "forgiving" (allowing recovery), and "clear" (predictable responses based on observable group behavior).
'''

description_COOPERATIVE_21 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being cooperative with protecting against persistent defectors.

## Decision Rules

### Core Logic:
```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

INITIALIZE:
- cooperation_threshold = 0.5  // Minimum fraction of players needed to cooperate
- forgiveness_probability = 0.1  // Chance to cooperate after being "punished"
- consecutive_defections = 0  // Track own defection streak
- last_round_cooperators = 0  // Number who cooperated last round

FOR each round t:
    IF t == 1:  // First round
        ACTION = C  // Always start cooperative
    
    ELIF t == final_round:  // Last round
        ACTION = C  // Maintain cooperation to the end
    
    ELSE:  // Middle rounds
        cooperation_rate = last_round_cooperators / n
        
        IF cooperation_rate >= cooperation_threshold:
            ACTION = C  // Reward high cooperation
            consecutive_defections = 0
        
        ELIF cooperation_rate >= cooperation_threshold - 0.2:
            // Moderate cooperation - be generous
            IF random() < 0.7:
                ACTION = C
            ELSE:
                ACTION = D
                consecutive_defections += 1
        
        ELSE:  // Low cooperation environment
            IF consecutive_defections >= 2:
                // Don't defect too long - attempt reconciliation
                IF random() < forgiveness_probability:
                    ACTION = C
                    consecutive_defections = 0
                ELSE:
                    ACTION = D
                    consecutive_defections += 1
            ELSE:
                ACTION = D  // Punish low cooperation
                consecutive_defections += 1

    UPDATE last_round_cooperators based on observations
```

## Detailed Decision Rules

1. **First Round**: Always cooperate (C) to signal cooperative intent
2. **Last Round**: Always cooperate (C) to avoid end-game defection cascade
3. **Middle Rounds**: Decision based on previous round's cooperation rate:
   - **High Cooperation** (≥50% cooperated): Cooperate to maintain momentum
   - **Moderate Cooperation** (30-49%): Cooperate with 70% probability to encourage others
   - **Low Cooperation** (<30%): Defect to protect against exploitation, but with forgiveness mechanism

## Key Features

### 1. **Cooperative Foundation**
- Starts with cooperation to establish good intentions
- Maintains cooperation in final round to prevent cascade failures
- Uses generous thresholds (50% cooperation rate trigger)

### 2. **Adaptive Response**
- Responds to group cooperation levels rather than individual actions
- Recognizes that in large groups, individual tracking becomes less reliable
- Adjusts strategy based on community-wide behavior patterns

### 3. **Forgiveness Mechanism**
- After 2+ consecutive defections, randomly cooperates (10% chance) to test for reconciliation
- Prevents getting stuck in permanent defection cycles
- Allows recovery from temporary downturns in cooperation

### 4. **Protection Against Exploitation**
- Won't cooperate indefinitely if others consistently defect
- Uses probabilistic responses in uncertain situations
- Tracks own behavior to avoid excessive punishment

## Edge Case Handling

- **All Defect Scenario**: Will eventually defect but periodically test for cooperation recovery
- **Mixed Strategies**: Responds proportionally to cooperation levels
- **End Game**: Maintains cooperation to signal long-term cooperative intent
- **Random Fluctuations**: Uses thresholds and probabilities to avoid overreacting to noise

## Strategic Rationale

This strategy is designed to:
1. **Establish Cooperation**: Strong initial cooperative signal
2. **Maintain Coalitions**: Reward and sustain cooperative groups
3. **Resist Exploitation**: Protect against persistent defectors
4. **Enable Recovery**: Allow return to cooperation after conflicts
5. **Handle Uncertainty**: Use probabilistic elements for robustness

The strategy recognizes that in tournaments against other AI strategies, many will likely implement some form of reciprocal or conditional cooperation, making a generous but not naive approach optimal for achieving high mutual payoffs.
'''

description_COOPERATIVE_22 = '''
Looking at this N-Player Public Goods Game, I'll design a cooperative strategy that balances cooperation with protection against exploitation. Here's my strategy:

## **Graduated Reciprocity with Forgiveness (GRF)**

### **Core Philosophy**
Start cooperative, respond proportionally to the cooperation level of others, but maintain forgiveness to prevent permanent defection spirals.

### **Decision Rules**

#### **Round 1 (Initialization)**
- Always COOPERATE
- Rationale: Signal cooperative intent and establish positive momentum

#### **Rounds 2 to r-1 (Main Game)**
Use a cooperation threshold based on observed behavior:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n
personal_threshold = max(0.3, cooperation_rate_moving_average * 0.8)

if cooperation_rate >= personal_threshold:
    play COOPERATE
else:
    play DEFECT with probability (1 - cooperation_rate)
```

**Moving Average Calculation:**
Track cooperation rate over last 3 rounds (or all rounds if fewer than 3):
```pseudocode
cooperation_history = [rates from last 3 rounds]
cooperation_rate_moving_average = sum(cooperation_history) / len(cooperation_history)
```

#### **Final Round (Round r)**
- If cooperation_rate_moving_average ≥ 0.4: COOPERATE
- Else: DEFECT
- Rationale: In the last round, only cooperate if there's been sustained cooperation

### **Key Features**

1. **Graduated Response**: Rather than binary tit-for-tat, respond proportionally to the overall cooperation level
2. **Minimum Cooperation Threshold**: Never set threshold below 0.3, maintaining some willingness to rebuild cooperation
3. **Forgiveness Mechanism**: Use moving averages rather than just last round, allowing recovery from temporary defection
4. **End-Game Consideration**: More selective in final round but still willing to cooperate if others have been consistently cooperative

### **Edge Case Handling**

- **All Defect Scenario**: Will eventually defect but maintains 30% chance of cooperation to test for recovery
- **Mixed Groups**: Adapts threshold based on group behavior while maintaining cooperative bias
- **Highly Cooperative Groups**: Rewards sustained cooperation with continued cooperation
- **Late-Round Defection**: Moving average prevents immediate abandonment of cooperation

### **Strategic Rationale**

This strategy is cooperative because it:
- Starts with cooperation
- Rewards group cooperation with continued cooperation  
- Maintains hope for cooperation recovery through forgiveness
- Uses proportional rather than punitive responses

It protects against exploitation by:
- Reducing cooperation when others consistently defect
- Being more cautious in the final round
- Using probabilistic defection rather than complete withdrawal

The strategy aims to find and maintain cooperative equilibria while being robust enough to survive in mixed environments.
'''

description_COOPERATIVE_23 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances trust-building with self-protection.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
For each round t (where 2 ≤ t ≤ r-1):

1. **Calculate cooperation rate** from previous round:
   ```
   cooperation_rate = (number_of_cooperators_last_round) / n
   ```

2. **Apply decision rule**:
   ```
   IF cooperation_rate >= 0.5:
       Action = COOPERATE
   ELSE IF cooperation_rate >= 0.3:
       Action = COOPERATE with probability 0.7, DEFECT with probability 0.3
   ELSE:
       Action = DEFECT
   ```

3. **Forgiveness mechanism**: 
   - Track consecutive rounds where cooperation_rate < 0.3
   - If this count reaches 3, reset counter and COOPERATE once as a "forgiveness probe"
   - This prevents permanent defection spirals

### Round r (Final Round): Conditional Cooperation
- **If** historical cooperation rate across all previous rounds ≥ 0.4: COOPERATE
- **Else**: DEFECT
- **Rationale**: Reward consistent cooperators but protect against end-game exploitation

## Detailed Algorithm

```pseudocode
FUNCTION decide_action(round_number, game_history):
    IF round_number == 1:
        RETURN COOPERATE
    
    IF round_number == total_rounds:
        overall_coop_rate = calculate_historical_cooperation_rate(game_history)
        IF overall_coop_rate >= 0.4:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    // Middle rounds
    last_round_coop_rate = count_cooperators(game_history[-1]) / n
    
    IF last_round_coop_rate >= 0.5:
        RETURN COOPERATE
    
    ELSE IF last_round_coop_rate >= 0.3:
        IF random() < 0.7:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    ELSE:
        // Check forgiveness condition
        consecutive_low_coop = count_consecutive_rounds_below_threshold(game_history, 0.3)
        IF consecutive_low_coop >= 3 AND consecutive_low_coop % 3 == 0:
            RETURN COOPERATE  // Forgiveness probe
        ELSE:
            RETURN DEFECT

FUNCTION calculate_historical_cooperation_rate(history):
    total_cooperations = 0
    total_decisions = 0
    FOR each round in history:
        total_cooperations += count_cooperators(round)
        total_decisions += n
    RETURN total_cooperations / total_decisions
```

## Edge Case Handling

1. **All players always defect**: After 3 rounds of universal defection, attempt forgiveness probe every 3 rounds to test if cooperation can be re-established

2. **Mixed cooperation patterns**: The probabilistic response (70% cooperate when cooperation_rate ≥ 0.3) allows for flexible adaptation to moderate cooperation levels

3. **Late-game defection cascade**: The final round conditional cooperation protects against end-game exploitation while still rewarding historically cooperative groups

## Cooperative Alignment

This strategy embodies cooperation through:

- **Initial trust**: Starting with cooperation signals good faith
- **Reciprocity**: Responding positively to cooperative behavior
- **Forgiveness**: Periodic attempts to restart cooperation even after defection periods
- **Proportionality**: Using probabilistic responses rather than harsh binary reactions
- **Long-term thinking**: Considering historical patterns rather than just immediate responses

The strategy aims to create and maintain cooperative equilibria while protecting against systematic exploitation, making it robust for tournament play against diverse opponent strategies.
'''

description_COOPERATIVE_24 = '''
# Cooperative Strategy: "Forgiving Majority Trigger"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibria while being resilient to occasional defections and exploitation attempts. It balances forgiveness with deterrence to maximize collective welfare.

## Decision Rules

### Round 1: Cooperative Start
```
if round == 1:
    return COOPERATE
```
Start cooperatively to signal willingness to collaborate and attempt to establish a cooperative norm.

### Rounds 2 to r-1: Majority-Based Response with Forgiveness
```
cooperation_rate = count_cooperators_last_round() / n
defection_streak = count_consecutive_rounds_below_threshold()

if cooperation_rate >= 0.5:
    return COOPERATE
elif cooperation_rate >= 0.3 and defection_streak <= 2:
    return COOPERATE  // Forgive temporary drops
else:
    return DEFECT     // Punish persistent low cooperation
```

### Final Round: Conditional Cooperation
```
if round == r:
    recent_cooperation_rate = count_cooperators_in_last_3_rounds() / (3 * n)
    if recent_cooperation_rate >= 0.4:
        return COOPERATE
    else:
        return DEFECT
```

## Detailed Strategy Logic

### Phase 1: Establishment (Rounds 1-3)
- **Round 1**: Always cooperate to signal cooperative intent
- **Rounds 2-3**: Cooperate if at least 30% of players cooperated in the previous round
- This allows for some initial confusion/testing while maintaining cooperative momentum

### Phase 2: Maintenance (Rounds 4 to r-2)
- **Primary Rule**: Cooperate if ≥50% cooperated last round
- **Forgiveness Mechanism**: Even if cooperation drops below 50%, continue cooperating for up to 2 consecutive rounds if cooperation rate stays ≥30%
- **Punishment Trigger**: Switch to defection if cooperation falls below 30% OR stays below 50% for 3+ consecutive rounds

### Phase 3: Endgame (Last 2 rounds)
- **Second-to-last round**: Apply same rules as maintenance phase
- **Final round**: Cooperate only if recent cooperation trend (last 3 rounds) shows ≥40% average cooperation rate

## Key Features

### Cooperative Elements
1. **Optimistic Start**: Begin with cooperation to establish positive precedent
2. **Majority Threshold**: Use 50% cooperation as the primary benchmark, encouraging collective action
3. **Forgiveness Buffer**: Allow temporary drops in cooperation without immediate punishment
4. **Conditional Final Cooperation**: Reward sustained cooperation even in the last round

### Robustness Mechanisms
1. **Gradual Response**: Don't immediately punish single-round drops
2. **Trend Analysis**: Consider patterns over multiple rounds rather than single-round snapshots
3. **Adaptive Thresholds**: Different cooperation thresholds for different situations

### Protection Against Exploitation
1. **Punishment Phase**: Switch to defection when cooperation becomes unsustainable
2. **Streak Counting**: Track persistent low-cooperation periods
3. **Endgame Protection**: Avoid being exploited in final rounds while maintaining cooperation when warranted

## Pseudocode Implementation

```python
def forgiving_majority_trigger(round_num, total_rounds, game_history, n):
    if round_num == 1:
        return "COOPERATE"
    
    last_round_cooperators = count_cooperators(game_history[-1])
    cooperation_rate = last_round_cooperators / n
    
    if round_num == total_rounds:  # Final round
        if len(game_history) >= 3:
            recent_coop_rate = sum(count_cooperators(round) for round in game_history[-3:]) / (3 * n)
            return "COOPERATE" if recent_coop_rate >= 0.4 else "DEFECT"
        else:
            return "COOPERATE" if cooperation_rate >= 0.4 else "DEFECT"
    
    # Regular rounds
    if cooperation_rate >= 0.5:
        return "COOPERATE"
    elif cooperation_rate >= 0.3:
        # Check if we're in a brief downturn
        consecutive_low = count_consecutive_below_threshold(game_history, 0.5)
        return "COOPERATE" if consecutive_low <= 2 else "DEFECT"
    else:
        return "DEFECT"

def count_consecutive_below_threshold(history, threshold):
    count = 0
    for round_data in reversed(history):
        if count_cooperators(round_data) / n < threshold:
            count += 1
        else:
            break
    return count
```

This strategy promotes cooperation while remaining robust against various types of opponents, from pure defectors to conditional cooperators to random players.
'''

description_COOPERATIVE_25 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with self-protection mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and attempt to establish a cooperative norm from the beginning.

### Rounds 2 to (r-1): Adaptive Cooperation
The strategy maintains a "cooperation threshold" based on recent community behavior:

```pseudocode
cooperation_threshold = 0.5  // At least half the players should cooperate
window_size = min(3, current_round - 1)  // Look at last 3 rounds or all available

// Calculate recent cooperation rate
recent_cooperation_rate = (total_cooperators_in_window) / (n * window_size)

if recent_cooperation_rate >= cooperation_threshold:
    Action = COOPERATE
else:
    // Community cooperation is low, but give second chances
    if my_last_action == COOPERATE and others_cooperation_rate_last_round < 0.3:
        Action = DEFECT  // Protect against exploitation
    else:
        Action = COOPERATE  // Forgive and try to restart cooperation
```

### Special Forgiveness Rule
- If I defected in the previous round due to low cooperation, and at least 40% of others cooperated in that round, return to cooperation immediately.
- This prevents getting stuck in mutual punishment cycles.

### Final Round (Round r): Conditional Cooperation
```pseudocode
if recent_cooperation_rate >= 0.4:
    Action = COOPERATE  // Reward good community behavior even in final round
else:
    Action = DEFECT     // Protect against final-round exploitation
```

## Key Features

### 1. Cooperative Foundation
- Starts with cooperation to signal good intentions
- Maintains cooperation as the default action when community cooperation is reasonable
- Uses a relatively lenient threshold (50%) for continued cooperation

### 2. Exploitation Protection
- Defects when community cooperation falls below 30% in the previous round AND I cooperated
- This prevents being consistently exploited by predominantly defecting populations

### 3. Forgiveness Mechanism
- Quickly returns to cooperation after punishing low cooperation
- Gives the community multiple chances to establish cooperative norms
- Uses a sliding window to avoid being overly influenced by early game dynamics

### 4. Endgame Consideration
- Maintains cooperation in the final round if community has been reasonably cooperative
- Only defects in final round if facing a predominantly non-cooperative community

## Robustness Features

### Against Always Defect Strategies
- Will initially cooperate but quickly identify and protect against pure exploitation
- Limits losses while occasionally testing if the environment improves

### Against Other Cooperative Strategies
- High likelihood of establishing mutual cooperation
- Forgiveness mechanism helps overcome coordination failures

### Against Mixed Strategies
- Adapts to the overall cooperation level in the community
- Balances cooperation with self-protection based on observed behavior

## Expected Performance
This strategy should perform well in environments with:
- Other cooperative strategies (high mutual cooperation)
- Mixed populations (adapts to cooperation level)
- Some exploitative strategies (limits exploitation while maintaining cooperation potential)

The strategy prioritizes long-term community welfare while including necessary self-protection mechanisms, making it both genuinely cooperative and strategically sound.
'''

description_COOPERATIVE_26 = '''
## Strategy: "Generous Tit-for-Tat with Forgiveness" (GTTF)

### Core Philosophy
This strategy balances cooperation with self-protection by being generous initially, responsive to group behavior, and forgiving of occasional defections. It aims to foster cooperative equilibria while defending against exploitation.

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and attempt to establish a cooperative norm from the start

**Rounds 2 to r-1 (Main Strategy):**
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_last_action = my_action_in_previous_round

if cooperation_rate >= 0.5:
    // Majority cooperated - maintain cooperation
    action = COOPERATE
    
elif cooperation_rate >= 0.3:
    // Mixed behavior - use conditional cooperation
    if my_last_action == COOPERATE:
        action = COOPERATE  // Give benefit of doubt
    else:
        action = DEFECT     // Continue punishment
        
else:  // cooperation_rate < 0.3
    // Low cooperation - defensive mode
    if cooperation_rate == 0:
        action = DEFECT     // Universal defection
    else:
        // Occasional forgiveness to test for recovery
        if round_number % 3 == 0:
            action = COOPERATE
        else:
            action = DEFECT
```

**Round r (Final Round):**
```pseudocode
cooperation_rate_last_round = count_cooperators_last_round / n

if cooperation_rate_last_round >= 0.6:
    action = COOPERATE  // Reward consistent cooperators
else:
    action = DEFECT     // End-game protection
```

### Key Features

1. **Generous Start**: Always cooperate in round 1 to signal good intentions and attempt to coordinate on the cooperative equilibrium.

2. **Majority Rule**: When ≥50% cooperated last round, continue cooperating to maintain the beneficial equilibrium.

3. **Conditional Cooperation**: In mixed situations (30-49% cooperation), maintain previous action if it was cooperative, giving others a chance to reciprocate.

4. **Defensive Mode**: When cooperation is low (<30%), primarily defect but include periodic "forgiveness" probes to test if cooperation can be restored.

5. **Endgame Consideration**: In the final round, cooperate only if there was strong cooperation (≥60%) in the previous round, otherwise protect against last-round defection.

### Strategic Rationale

- **Addresses Social Dilemma**: Attempts to solve the free-rider problem by conditioning cooperation on others' behavior
- **Exploits Repeated Game Structure**: Uses reputation and reciprocity across rounds
- **Balances Cooperation and Protection**: Generous enough to establish cooperation but defensive enough to avoid exploitation
- **Handles Heterogeneous Opponents**: Adapts to different strategy types through behavioral observation
- **Tournament Robust**: Performs well against both cooperative and selfish strategies

This strategy should perform well in a mixed population, helping to establish cooperative norms when possible while protecting against exploitation when facing predominantly selfish opponents.
'''

description_COOPERATIVE_27 = '''
# Graduated Tit-for-Tat with Forgiveness (GTTF)

## Core Philosophy
This strategy balances cooperation with protection against exploitation by using graduated responses and strategic forgiveness to maintain cooperative relationships while deterring free-riders.

## Decision Rules

### Round 1: Cooperative Start
- **Action**: Always COOPERATE
- **Rationale**: Signal willingness to cooperate and establish initial trust

### Rounds 2 to r-1: Adaptive Response
```pseudocode
For each round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (number of cooperators in round t-1) / n
    
    if cooperation_rate ≥ 0.5:
        // Majority cooperated - reciprocate cooperation
        Action = COOPERATE
    else if cooperation_rate ≥ 0.3:
        // Mixed cooperation - graduated response
        if my_action_last_round == COOPERATE:
            Action = DEFECT  // Punish low cooperation
        else:
            Action = COOPERATE  // Give second chance
    else:
        // Low cooperation (< 30%) - strong deterrent needed
        Action = DEFECT
```

### Round r (Final Round): Conditional Cooperation
```pseudocode
For final round r:
    recent_cooperation = average cooperation rate over last min(3, r-1) rounds
    
    if recent_cooperation ≥ 0.6:
        Action = COOPERATE  // Reward sustained cooperation
    else:
        Action = DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Threshold-Based Response
- **High cooperation (≥50%)**: Reciprocate with cooperation
- **Medium cooperation (30-50%)**: Graduated punishment with forgiveness
- **Low cooperation (<30%)**: Strong deterrent through defection

### 2. Forgiveness Mechanism
- After punishing low cooperation with defection, give one chance to return to cooperation
- Prevents permanent breakdown of cooperative relationships
- Allows recovery from coordination failures

### 3. End-Game Protection
- Evaluates recent cooperation trends in final round
- Cooperates only if sustained high cooperation (≥60%) in recent rounds
- Guards against exploitation while rewarding consistent cooperators

### 4. Memory and Adaptation
- Uses short-term memory (last 1-3 rounds) for decisions
- Adapts to changing group dynamics
- Balances responsiveness with stability

## Strategic Advantages

1. **Exploitation Resistance**: Quickly responds to free-riding attempts
2. **Cooperation Promotion**: Rewards and encourages group cooperation
3. **Relationship Repair**: Forgiveness mechanism allows recovery from conflicts
4. **Endgame Robustness**: Protects against final-round defection cascades
5. **Clear Signaling**: Predictable responses help other cooperative strategies coordinate

## Expected Performance
- **Against Cooperators**: Maintains mutual cooperation through positive reciprocity
- **Against Mixed Strategies**: Encourages cooperation through conditional reciprocity
- **Against Defectors**: Minimizes losses through quick punishment and protection
- **In Tournaments**: Balances cooperation gains with exploitation protection

This strategy aims to be a "good citizen" that promotes group welfare while being robust enough to survive in a competitive environment with diverse opponent strategies.
'''

description_COOPERATIVE_28 = '''
I'll design a cooperative strategy called "Generous Tit-for-Tat with Forgiveness" (GTTF). This strategy aims to promote cooperation while being resilient to exploitation and defection cascades.

## Strategy: Generous Tit-for-Tat with Forgiveness (GTTF)

### Core Philosophy
Start cooperatively, reciprocate the group's behavior with some tolerance for defection, and include mechanisms for recovery and end-game cooperation.

### Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness

PARAMETERS:
- cooperation_threshold = 0.5 (cooperate if ≥50% cooperated last round)
- forgiveness_probability = 0.1 (10% chance to cooperate despite low cooperation)
- endgame_rounds = 2 (cooperate in final rounds regardless)

DECISION PROCESS for round t:

IF t == 1:
    RETURN C  // Always cooperate in first round

IF t > (r - endgame_rounds):
    RETURN C  // Always cooperate in final rounds

// Calculate cooperation rate from previous round
cooperation_rate = (number_of_cooperators_in_round_t-1) / n

IF cooperation_rate >= cooperation_threshold:
    RETURN C  // Reciprocate high cooperation
    
ELSE:
    // Low cooperation detected - apply forgiveness mechanism
    IF random() < forgiveness_probability:
        RETURN C  // Forgive and try to restart cooperation
    ELSE:
        RETURN D  // Defect in response to low cooperation
```

### Detailed Strategy Components

1. **First Round Behavior**: Always cooperate (C)
   - Establishes cooperative intent
   - Signals willingness to contribute to public good

2. **Main Game Logic**: Conditional cooperation based on group behavior
   - **Cooperation Threshold**: Cooperate if ≥50% of players cooperated in the previous round
   - **Responsive Defection**: Defect if cooperation drops below threshold
   - **Forgiveness Mechanism**: 10% probability to cooperate even when cooperation is low

3. **Endgame Behavior**: Cooperate in final 2 rounds
   - Prevents defection cascade in last rounds
   - Maximizes group welfare when reputation no longer matters

### Edge Cases Handled

- **First Round**: Always cooperate to establish good faith
- **Last Rounds**: Always cooperate to prevent endgame defection
- **All Defect Scenario**: Forgiveness mechanism provides 10% chance to attempt cooperation restart
- **Mixed Cooperation**: Clear threshold-based decision making
- **Single Player Games**: Strategy works for n≥2

### Cooperative Alignment

This strategy is fundamentally cooperative because it:

1. **Starts Cooperatively**: Gives others the benefit of the doubt
2. **Rewards Cooperation**: Continues cooperating when others do
3. **Includes Forgiveness**: Doesn't permanently punish; gives second chances
4. **Ends Cooperatively**: Maximizes final welfare regardless of others' actions
5. **Clear Reciprocity**: Makes cooperation profitable for the group

### Strategic Rationale

- **Threshold-Based**: The 50% threshold means cooperation is maintained even if some players defect
- **Forgiveness**: Prevents permanent defection spirals and allows recovery
- **Endgame Cooperation**: Counteracts the typical last-round defection problem
- **Simplicity**: Easy for other players to understand and reciprocate

This strategy balances cooperation with self-protection, provides clear signals to other players, and includes mechanisms to recover from defection cascades while maintaining a fundamentally cooperative stance throughout the game.
'''

description_COOPERATIVE_29 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances trust-building with self-protection.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and attempt to establish a cooperative norm from the start

**Rounds 2 to r-1 (Main Game):**
- **Cooperation Threshold:** Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism:** If cooperation rate < 50%, still cooperate with probability 20% to allow for recovery
- **Streak Bonus:** If cooperation rate has been ≥ 70% for the last 2 consecutive rounds, always cooperate (reward high cooperation)

**Round r (Final Round):**
- **Conditional Cooperation:** Cooperate only if cooperation rate in round r-1 was ≥ 60%
- **Rationale:** Higher threshold for final round since there's no future to build upon, but still maintain some cooperative spirit

### Pseudocode

```
function decide_action(current_round, history):
    if current_round == 1:
        return COOPERATE
    
    prev_round = current_round - 1
    prev_coop_rate = count_cooperators(history[prev_round]) / n
    
    if current_round == r:  // Final round
        if prev_coop_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // Rounds 2 to r-1
        // Check for high cooperation streak
        if current_round >= 3:
            prev2_coop_rate = count_cooperators(history[prev_round-1]) / n
            if prev_coop_rate >= 0.7 and prev2_coop_rate >= 0.7:
                return COOPERATE
        
        // Main decision rule
        if prev_coop_rate >= 0.5:
            return COOPERATE
        else:
            // Forgiveness mechanism
            if random() < 0.2:
                return COOPERATE
            else:
                return DEFECT
```

### Edge Case Handling

1. **First Round:** Always cooperate to signal good intentions and attempt to establish cooperative equilibrium

2. **Final Round:** Use higher threshold (60%) but still maintain some cooperation to avoid complete breakdown

3. **High Defection Scenarios:** The 20% forgiveness rate prevents permanent punishment cycles and allows for recovery

4. **High Cooperation Scenarios:** The streak bonus rewards and reinforces periods of high cooperation

5. **Mixed Scenarios:** The 50% threshold provides a clear, fair decision point that encourages others to maintain at least moderate cooperation levels

### Cooperative Alignment

This strategy is fundamentally cooperative because:

1. **Optimistic Start:** Always begins with cooperation
2. **Generous Threshold:** 50% cooperation rate is relatively lenient
3. **Forgiveness:** 20% chance to cooperate even when others defect
4. **Reward System:** Bonus cooperation when others maintain high cooperation rates
5. **Sustainable:** Avoids being exploited while maintaining cooperative spirit

### Strategic Rationale

- **Incentive Alignment:** Other players know they need at least 50% group cooperation to maintain your cooperation
- **Exploitation Resistance:** Doesn't cooperate unconditionally, preventing free-riding
- **Recovery Mechanism:** Forgiveness allows the group to recover from coordination failures
- **Clear Signaling:** Behavior is predictable and transparent, making it easier for others to coordinate with
- **Adaptive:** Responds to the actual behavior of the group rather than making assumptions

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones.
'''

description_COOPERATIVE_30 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy balances cooperation with protection against exploitation by starting cooperatively, reciprocating the group's behavior, and including forgiveness mechanisms to recover from mutual defection spirals.

## Core Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Reciprocation
```pseudocode
cooperation_rate = (number of cooperators in previous round) / n

if cooperation_rate >= 0.5:
    play C
else if cooperation_rate >= 0.3:
    play C with probability 0.7, D with probability 0.3
else:
    play D
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
recent_cooperation_rate = average cooperation rate over last 3 rounds (or all rounds if r < 4)

if recent_cooperation_rate >= 0.4:
    play C
else:
    play D
```

## Forgiveness Mechanism
Every 3 rounds, if currently in a defection pattern:
```pseudocode
if (current_round % 3 == 0) and (cooperation_rate_last_2_rounds < 0.3):
    play C  // Attempt to restart cooperation
```

## Key Features

### 1. **Cooperative Foundation**
- Starts with cooperation to signal good intentions
- Maintains cooperation when majority cooperates
- Doesn't immediately punish single defections

### 2. **Graduated Response**
- Uses probabilistic cooperation in uncertain situations (30-50% group cooperation)
- Provides measured response rather than binary punishment
- Allows for recovery from temporary setbacks

### 3. **Forgiveness and Recovery**
- Periodic attempts to restart cooperation even after mutual defection
- Prevents permanent lock-in to inefficient equilibria
- Final round cooperation when recent history suggests reciprocation

### 4. **Exploitation Protection**
- Switches to defection when facing majority defectors
- Doesn't cooperate unconditionally beyond the first round
- Maintains some defection probability in ambiguous situations

## Strategic Rationale

1. **Initial Cooperation**: Maximizes potential for high-payoff mutual cooperation outcomes
2. **Majority Rule**: Aligns with the most successful group behavior pattern
3. **Graduated Response**: Avoids overreaction to noise while still responding to genuine shifts
4. **Forgiveness**: Prevents getting trapped in inefficient punishment cycles
5. **End-game Cooperation**: Capitalizes on established cooperative relationships in the final round

This strategy aims to foster cooperation while maintaining resilience against exploitation, making it well-suited for tournament play against diverse opponent strategies.
'''

description_COOPERATIVE_31 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with protective mechanisms against persistent defectors.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: COOPERATE if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: Even if majority defected last round, still COOPERATE if:
  - This is only the second consecutive round where majority defected, OR
  - The cooperation rate in the previous round was ≥ 40% (i.e., at least 2/5 of players cooperated)
- **Protection Rule**: DEFECT if majority has defected for 2+ consecutive rounds AND cooperation rate < 40%

### Round r (Final Round): Conditional Cooperation
- **Action**: COOPERATE if at least 1/3 of players cooperated in round r-1
- **Rationale**: Maintain cooperative stance even in final round to avoid triggering end-game defection cascades

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    previous_round = history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / n
    majority_cooperated = cooperation_rate > 0.5
    
    if round_number == r:  // Final round
        return COOPERATE if cooperation_rate >= 1/3 else DEFECT
    
    // Rounds 2 to r-1
    if majority_cooperated:
        return COOPERATE
    
    // Majority defected last round - check forgiveness conditions
    if round_number == 2:  // Second round, so only one previous round
        return COOPERATE  // Give benefit of doubt
    
    previous_two_rounds = history[round_number-2:round_number-1]
    majority_defected_twice = all(count_cooperators(round)/n <= 0.5 
                                 for round in previous_two_rounds)
    
    if not majority_defected_twice or cooperation_rate >= 0.4:
        return COOPERATE  // Forgiveness mechanism
    else:
        return DEFECT     // Protection against persistent defection
```

## Strategy Rationale

### Cooperative Alignment
- **Initial Cooperation**: Signals willingness to cooperate and helps establish trust
- **Generous Forgiveness**: Doesn't immediately retaliate against single-round defection waves
- **Final Round Cooperation**: Resists end-game defection temptation when there's reasonable cooperation

### Protective Mechanisms
- **Majority Threshold**: Responds to overall group behavior rather than individual defectors
- **Consecutive Defection Rule**: Only retaliates after persistent group defection
- **40% Threshold**: Maintains cooperation even when majority defects if significant minority still cooperates

### Adaptability
- **Context Sensitive**: Adjusts behavior based on recent history and current round position
- **Escalation Resistance**: Doesn't immediately spiral into permanent defection
- **Recovery Oriented**: Ready to return to cooperation when group shows cooperative signals

## Expected Behavior Against Different Opponent Types
- **Against Cooperators**: Establishes stable mutual cooperation
- **Against Defectors**: Initially tries cooperation, then protects against exploitation
- **Against Mixed Strategies**: Adapts to prevailing group dynamics while maintaining cooperative bias
- **Against Tit-for-Tat variants**: Compatible and likely to achieve cooperation

This strategy prioritizes the cooperative objective while maintaining rational self-protection, making it robust across various opponent compositions in the tournament setting.
'''

description_COOPERATIVE_32 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances the desire to cooperate with the need to protect against persistent defectors.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Start cooperatively to signal willingness to work together and establish a foundation for mutual cooperation.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness

**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability based on recent history:
- If cooperation rate was ≥ 30%: Cooperate with 70% probability
- If cooperation rate was < 30%: Cooperate with 30% probability

**Streak Tracking**: Monitor consecutive rounds of low cooperation (< 30%):
- After 2 consecutive rounds of < 30% cooperation: Switch to pure defection for 1 round as "punishment"
- Reset forgiveness after any round with ≥ 50% cooperation

### Final Round (Round r): Conditional Defection
- If cooperation rate in round r-1 was ≥ 70%: Cooperate (reward high cooperation)
- Otherwise: Defect (no future to build on)

## Pseudocode

```
GTTF_Strategy(round_number, game_history):
    if round_number == 1:
        return C
    
    last_round_coop_rate = count_cooperators(game_history[round_number-1]) / n
    
    if round_number == r:  // Final round
        if last_round_coop_rate >= 0.7:
            return C
        else:
            return D
    
    // Check for punishment condition
    if consecutive_low_coop_rounds >= 2:
        consecutive_low_coop_rounds = 0
        return D  // Punishment round
    
    // Main cooperation logic
    if last_round_coop_rate >= 0.5:
        reset_low_coop_counter()
        return C
    
    elif last_round_coop_rate >= 0.3:
        increment_low_coop_counter()
        return random_choice(C with prob 0.7, D with prob 0.3)
    
    else:  // < 30% cooperation
        increment_low_coop_counter()
        return random_choice(C with prob 0.3, D with prob 0.7)
```

## Key Features

1. **Cooperative Start**: Always begins cooperatively to establish good faith
2. **Majority-Based Response**: Primary decision based on whether majority cooperated
3. **Graduated Forgiveness**: Probabilistic cooperation even when others defect, with forgiveness proportional to cooperation level
4. **Punishment Mechanism**: Brief retaliation against persistent low cooperation to deter exploitation
5. **Endgame Consideration**: Maintains cooperation incentive even in final round if group has been highly cooperative

## Strategic Rationale

- **Encourages Cooperation**: By being generally forgiving and cooperative, it incentivizes others to cooperate
- **Prevents Exploitation**: Punishment mechanism deters strategies that might try to exploit pure cooperators
- **Adapts to Group Dynamics**: Responds proportionally to the group's cooperation level
- **Robust to Noise**: Probabilistic responses prevent overreaction to occasional defections
- **Game-Theoretically Sound**: Balances the tension between individual rationality and group optimality

This strategy should perform well against other cooperative strategies while maintaining resilience against more exploitative approaches.
'''

description_COOPERATIVE_33 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with practical protection against free-riders.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
Apply the following decision tree:

```pseudocode
if (cooperation_rate_last_round >= cooperation_threshold):
    action = C
else if (my_recent_forgiveness_count < max_forgiveness):
    action = C
    increment_forgiveness_count()
else:
    action = D
```

Where:
- `cooperation_threshold = 0.5` (majority must cooperate)
- `max_forgiveness = 2` (forgive up to 2 consecutive low-cooperation rounds)
- `cooperation_rate_last_round = (number of cooperators in previous round) / n`

### Final Round (Round r): Conditional Cooperation
```pseudocode
if (overall_cooperation_rate >= 0.6):
    action = C
else:
    action = D
```

Where `overall_cooperation_rate = total_cooperations_observed / (n × (r-1))`

## Detailed Strategy Components

### 1. Cooperation Threshold Logic
- If ≥50% of players cooperated in the previous round → Cooperate
- This encourages maintenance of cooperative equilibria
- Responds positively to majority cooperative behavior

### 2. Forgiveness Mechanism
- Even if cooperation rate falls below threshold, forgive up to 2 times per game
- Reset forgiveness counter when cooperation rate returns above threshold
- Prevents permanent breakdown from temporary defection waves

### 3. Punishment Phase
- After exhausting forgiveness, defect until cooperation rate recovers
- Not permanently retaliatory - will return to cooperation when others do

### 4. End-game Handling
- Final round uses overall game performance rather than just recent behavior
- Rewards consistently cooperative opponents even in final round
- Threshold of 60% reflects higher standard for final cooperation

## Edge Case Handling

### First Round
- Always cooperate to signal intent and give cooperation the best chance

### Low Participation Scenarios (n ≤ 3)
- Reduce cooperation_threshold to 0.4 to account for higher individual impact

### High Multiplication Factor (k close to n)
- Strategy remains unchanged as the logic scales appropriately

### Single Defector Problem
- With n=6, threshold=0.5: tolerate 1-2 defectors while maintaining cooperation
- Forgiveness prevents overreaction to occasional defections

## Strategic Rationale

1. **Cooperative Signaling**: Immediate cooperation signals intent to other cooperative strategies
2. **Reciprocity**: Responds to group behavior rather than individual actions
3. **Stability**: Majority threshold creates stable cooperative equilibria
4. **Resilience**: Forgiveness mechanism prevents cascade failures from minor defections
5. **Protection**: Eventually punishes persistent free-riding
6. **Recovery**: Always willing to return to cooperation when others do

## Expected Performance

- **Against other cooperative strategies**: Should establish and maintain mutual cooperation
- **Against mixed populations**: Will cooperate when cooperation is prevalent
- **Against exploitative strategies**: Will eventually protect itself while remaining open to cooperation
- **In final rounds**: Maintains cooperation with proven cooperative partners

This strategy prioritizes the cooperative goal while incorporating practical safeguards against exploitation, making it robust across various opponent compositions.
'''

description_COOPERATIVE_34 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with self-protection mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
For each round t (where 2 ≤ t ≤ r-1):

1. **Calculate Cooperation Rate**: 
   ```
   cooperation_rate = (total_cooperators_last_round) / n
   ```

2. **Apply Decision Logic**:
   ```pseudocode
   if cooperation_rate >= 0.6:
       action = COOPERATE
   elif cooperation_rate >= 0.4:
       if my_last_action == COOPERATE and I_was_among_minority_cooperators:
           action = DEFECT  // Punish low cooperation
       else:
           action = COOPERATE  // Give another chance
   else:  // cooperation_rate < 0.4
       if cooperation_rate >= 0.2:
           action = COOPERATE with probability 0.3  // Occasional forgiveness
       else:
           action = DEFECT  // Protect against widespread defection
   ```

### Final Round (Round r): Conditional Cooperation
```pseudocode
if average_cooperation_rate_so_far >= 0.5:
    action = COOPERATE  // Reward overall cooperative environment
else:
    action = DEFECT  // No incentive to cooperate if others haven't
```

## Key Features

### 1. **Threshold-Based Response**
- High cooperation (≥60%): Always cooperate
- Medium cooperation (40-60%): Conditional cooperation with punishment
- Low cooperation (<40%): Protective defection with occasional forgiveness

### 2. **Forgiveness Mechanism**
- Even in low-cooperation environments, occasionally cooperate (30% chance when cooperation rate ≥20%)
- This prevents permanent defection spirals and allows recovery

### 3. **Punishment with Memory**
- When cooperation rate is medium but declining, punish by defecting
- Remember when you were "exploited" (cooperated while most defected)

### 4. **End-Game Handling**
- Final round decision based on overall game history
- Rewards sustained cooperation throughout the game

## Edge Cases

### **First Round**
Always cooperate to establish cooperative norm and signal intentions.

### **Last Round**
Cooperate only if the overall game has been sufficiently cooperative (≥50% cooperation rate), otherwise defect since there's no future to influence.

### **All Others Defect**
If cooperation rate drops to 0, still occasionally cooperate (with low probability) to test if conditions have changed.

### **Mixed Signals**
When cooperation rates fluctuate around thresholds, the strategy includes hysteresis (different responses when coming from above vs below threshold) to avoid erratic behavior.

## Strategic Rationale

1. **Encourages Cooperation**: Starts cooperatively and rewards high cooperation levels
2. **Punishes Free-Riding**: Responds to low cooperation with defection
3. **Allows Recovery**: Forgiveness mechanism prevents permanent breakdown
4. **Adapts to Context**: Responsive to the actual behavior patterns observed
5. **Self-Protective**: Won't be exploited indefinitely by consistent defectors

This strategy should perform well against other cooperative strategies while being robust enough to handle some aggressive or selfish opponents.
'''

description_COOPERATIVE_35 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being cooperative with protecting against consistent defectors.

## Decision Rules

### Round 1: Cooperate
- Always start with cooperation (C) to signal cooperative intent
- This establishes a positive baseline and gives other cooperative strategies a chance to coordinate

### Rounds 2 to r-1: Adaptive Response
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total_cooperators_last_round) / n
    
    IF cooperation_rate ≥ 0.5:
        // Majority cooperated - reward with cooperation
        action = C
    ELSE IF cooperation_rate ≥ 0.3:
        // Significant minority cooperated - be generous
        IF random() < 0.7:  // 70% chance to cooperate
            action = C
        ELSE:
            action = D
    ELSE:
        // Low cooperation - mostly defect but occasionally forgive
        IF random() < 0.2:  // 20% chance to cooperate (forgiveness)
            action = C
        ELSE:
            action = D
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
For final round r:
    recent_cooperation_rate = average_cooperation_rate_last_3_rounds
    
    IF recent_cooperation_rate ≥ 0.4:
        // Sustained cooperation deserves final cooperation
        action = C
    ELSE:
        // Protect against end-game defection
        action = D
```

## Key Features

### 1. **Generous Starting Posture**
- Begin cooperatively to enable coordination with other cooperative strategies
- Signal willingness to contribute to mutual benefit

### 2. **Majority-Based Response**
- When majority cooperates (≥50%), always reciprocate with cooperation
- This reinforces positive equilibria and rewards group cooperation

### 3. **Graduated Response**
- Uses thresholds (50%, 30%) rather than binary all-or-nothing decisions
- Maintains some cooperation even when facing moderate defection levels
- Prevents rapid spiral into mutual defection

### 4. **Built-in Forgiveness**
- Even in low-cooperation scenarios, maintains 20% cooperation rate
- Allows recovery from temporary coordination failures
- Prevents permanent lock-in to defection equilibrium

### 5. **End-Game Protection**
- Recognizes that final round creates defection incentives
- Only cooperates in final round if there's been sustained recent cooperation
- Balances cooperation with protection against exploitation

## Strategic Rationale

### **Why This Works Against Other Cooperative Strategies:**
- Mutual cooperation quickly emerges and stabilizes
- Generous starting move enables coordination
- Majority-rule ensures sustained cooperation once achieved

### **Why This Works Against Mixed Strategies:**
- Adapts cooperation level to observed behavior
- Maintains enough cooperation to benefit from public good
- Doesn't get completely exploited by moderate defectors

### **Why This Has Protection Against Pure Defectors:**
- Reduces cooperation when facing high defection rates
- Maintains minimal forgiveness to avoid pure punishment cycles
- End-game protection prevents final-round exploitation

### **Tournament Considerations:**
- Performs well against other cooperative strategies through coordination
- Maintains reasonable payoffs against mixed opponents
- Has sufficient protection to avoid being completely exploited
- The randomized elements prevent opponents from perfectly predicting behavior

This strategy aims to foster cooperation while maintaining strategic flexibility and protection against exploitation, making it robust across diverse opponent types likely in an LLM tournament setting.
'''

description_COOPERATIVE_36 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness"** that aims to establish and maintain cooperation while being resilient to defection.

## Strategy: Generous Tit-for-Tat with Forgiveness (GTTF)

### Core Philosophy
This strategy starts cooperatively, reciprocates the group's behavior, but incorporates forgiveness to recover from defection spirals and generosity to account for the multi-player nature of the game.

### Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness

INITIALIZATION:
- cooperation_threshold = 0.5  // Cooperate if ≥50% cooperated last round
- forgiveness_probability = 0.1  // 10% chance to cooperate even when threshold not met
- recent_history_window = min(3, current_round - 1)  // Look at last 3 rounds max

DECISION PROCESS for round t:
1. IF t == 1:
   RETURN C  // Always cooperate in first round

2. IF t == final_round:
   // In last round, cooperate if group has been mostly cooperative recently
   recent_cooperation_rate = calculate_recent_cooperation_rate(recent_history_window)
   IF recent_cooperation_rate >= 0.4:
     RETURN C
   ELSE:
     RETURN D

3. FOR rounds 2 to r-1:
   // Calculate cooperation rate from previous round
   last_round_cooperation_rate = (number_of_cooperators_in_round[t-1]) / n
   
   // Main decision logic
   IF last_round_cooperation_rate >= cooperation_threshold:
     RETURN C
   ELSE:
     // Apply forgiveness - sometimes cooperate even when threshold not met
     IF random() < forgiveness_probability:
       RETURN C
     ELSE:
       RETURN D

HELPER FUNCTION:
calculate_recent_cooperation_rate(window_size):
  total_cooperation = 0
  for i in range(max(1, current_round - window_size), current_round):
    total_cooperation += number_of_cooperators_in_round[i]
  return total_cooperation / (window_size * n)
```

### Strategy Components Explained

**1. Cooperative Start**: Always cooperate in round 1 to signal cooperative intent and give others a chance to reciprocate.

**2. Threshold-Based Reciprocity**: In middle rounds, cooperate if at least 50% of players cooperated in the previous round. This accounts for the multi-player nature where perfect coordination is unlikely.

**3. Forgiveness Mechanism**: Even when the cooperation threshold isn't met, there's a 10% chance to cooperate anyway. This helps:
   - Break cycles of mutual defection
   - Signal continued willingness to cooperate
   - Account for honest mistakes or experimental behavior by opponents

**4. Endgame Consideration**: In the final round, use recent history (last few rounds) rather than just the previous round to make a more informed decision about whether the group has established a cooperative norm.

### Edge Cases Handled

- **First Round**: Always cooperate to establish cooperative baseline
- **Last Round**: Use recent cooperation history to decide, preventing exploitation while rewarding established cooperation
- **All Defect Scenario**: Forgiveness mechanism provides path back to cooperation
- **Mixed Behavior**: Threshold approach handles realistic scenarios where not all players cooperate

### Why This Strategy is Cooperative

1. **Starts with trust** by cooperating first
2. **Rewards group cooperation** with continued cooperation
3. **Provides second chances** through forgiveness
4. **Considers group dynamics** rather than tracking individual players
5. **Maintains hope for cooperation** even after defection periods

### Strategic Reasoning

This strategy balances several key considerations:
- **Exploitability vs. Cooperation**: The forgiveness rate is low enough to avoid constant exploitation but high enough to recover from defection spirals
- **Group vs. Individual Focus**: By looking at overall cooperation rates rather than individual histories, it's more suitable for the n-player context
- **Reputation Building**: Consistent cooperative behavior when others cooperate builds trust
- **Robustness**: Can handle various opponent strategies while maintaining cooperative orientation

The strategy should perform well against other cooperative strategies while having some resilience against purely exploitative ones, making it suitable for a mixed tournament environment.
'''

description_COOPERATIVE_37 = '''
# Generous Tit-for-Tat with Forgiveness (GTTF)

## Strategy Overview
This strategy combines cooperative signaling, reciprocity, and strategic forgiveness to build and maintain cooperation while protecting against exploitation.

## Core Decision Rules

### Round 1: Cooperative Signal
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish mutual cooperation from the start

### Rounds 2 to r-1: Adaptive Reciprocity
For each round t (where 2 ≤ t ≤ r-1):

1. **Calculate cooperation rate from previous round**:
   ```
   cooperation_rate = (number of cooperators in round t-1) / n
   ```

2. **Apply decision rule**:
   ```
   if cooperation_rate ≥ 0.5:
       action = COOPERATE
   else if cooperation_rate ≥ 0.3:
       action = COOPERATE with probability 0.7, DEFECT with probability 0.3
   else:
       action = DEFECT
   ```

3. **Forgiveness mechanism**: 
   - If defecting for 2+ consecutive rounds AND cooperation_rate increases by ≥0.2 from previous round:
     ```
     action = COOPERATE  # Give second chance
     ```

### Final Round (r): Conditional Cooperation
- **If average cooperation rate across all previous rounds ≥ 0.6**: COOPERATE
- **Otherwise**: DEFECT

## Strategy Rationale

### Cooperative Alignment
- **Initial cooperation** establishes good faith
- **Generous threshold** (50% cooperation rate) maintains cooperation even when not all players cooperate
- **Probabilistic cooperation** at medium cooperation levels (30-50%) shows willingness to contribute while managing risk
- **Forgiveness mechanism** allows recovery from mutual defection spirals

### Protection Against Exploitation
- **Defection below 30% cooperation** prevents being exploited by predominantly defecting populations
- **Final round defection** (when cooperation has been low) protects against end-game exploitation
- **Probabilistic element** makes the strategy less predictable to purely exploitative opponents

### Adaptability
- **Cooperation rate tracking** allows real-time adaptation to opponent behavior
- **Forgiveness triggers** enable recovery when opponents show renewed cooperation
- **Final round conditioning** accounts for overall game history

## Pseudocode Implementation

```python
def decide_action(round_num, history, n, r):
    if round_num == 1:
        return COOPERATE
    
    # Calculate previous round cooperation rate
    prev_cooperators = count_cooperators(history[round_num-2])
    cooperation_rate = prev_cooperators / n
    
    if round_num == r:  # Final round
        avg_cooperation = calculate_average_cooperation_rate(history, n)
        return COOPERATE if avg_cooperation >= 0.6 else DEFECT
    
    # Check forgiveness condition
    if (consecutive_defections(history, my_player_id) >= 2 and 
        cooperation_rate_increased_by(history, 0.2)):
        return COOPERATE
    
    # Main decision logic
    if cooperation_rate >= 0.5:
        return COOPERATE
    elif cooperation_rate >= 0.3:
        return COOPERATE if random() < 0.7 else DEFECT
    else:
        return DEFECT
```

This strategy balances the cooperative goal of maximizing collective welfare with the practical need to avoid exploitation in a competitive tournament environment.
'''

description_COOPERATIVE_38 = '''
I'll design a cooperative strategy called "Generous Tit-for-Tat with Forgiveness" (GTF). This strategy balances cooperation with protection against exploitation while maintaining a cooperative mindset.

## Strategy: Generous Tit-for-Tat with Forgiveness (GTF)

### Core Philosophy
Start cooperatively, reciprocate the majority behavior, but be generous and forgiving to encourage collective cooperation.

### Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTF)

PARAMETERS:
- cooperation_threshold = 0.4  // Cooperate if ≥40% cooperated last round
- forgiveness_probability = 0.2  // 20% chance to cooperate even when below threshold
- endgame_rounds = 2  // Number of final rounds requiring special handling

FUNCTION decide_action(round_number, game_history, n_players, total_rounds):
    
    // FIRST ROUND: Always cooperate
    IF round_number == 1:
        RETURN C
    
    // CALCULATE COOPERATION RATE FROM PREVIOUS ROUND
    previous_round = game_history[round_number - 1]
    cooperators_last_round = count_cooperators(previous_round)
    cooperation_rate = cooperators_last_round / n_players
    
    // ENDGAME HANDLING (Last few rounds)
    IF round_number > (total_rounds - endgame_rounds):
        // In final rounds, be more selective but still reward high cooperation
        IF cooperation_rate >= 0.6:
            RETURN C
        ELSE:
            RETURN D
    
    // MAIN STRATEGY LOGIC
    IF cooperation_rate >= cooperation_threshold:
        // Majority or significant minority cooperated - reciprocate
        RETURN C
    ELSE:
        // Low cooperation, but be forgiving occasionally
        IF random() < forgiveness_probability:
            RETURN C  // Forgiveness move to potentially restart cooperation
        ELSE:
            RETURN D  // Protect against exploitation
```

### Strategy Components

1. **Cooperative Start**: Always cooperate in round 1 to signal cooperative intent and give the group the best chance at establishing a cooperative norm.

2. **Majority Reciprocation**: If 40% or more players cooperated in the previous round, cooperate. This threshold is generous enough to maintain cooperation even when some players defect.

3. **Forgiveness Mechanism**: Even when cooperation falls below the threshold, randomly cooperate 20% of the time. This serves two purposes:
   - Prevents permanent defection spirals
   - Signals continued willingness to cooperate if others return

4. **Endgame Protection**: In the final 2 rounds, require higher cooperation rates (60%) before cooperating, as the incentive to defect increases near the game's end.

### Handling Edge Cases

- **Round 1**: Always cooperate (no history to base decisions on)
- **All players defected last round**: Still 20% chance to cooperate (forgiveness)
- **Mixed cooperation patterns**: Uses cooperation rate rather than individual tracking, making it robust to varying group compositions
- **Final rounds**: Adjusted threshold to account for increased defection incentives

### Cooperative Alignment

This strategy embodies cooperation through:

1. **Optimistic start**: Assumes others will cooperate
2. **Generous thresholds**: Only requires 40% cooperation to reciprocate
3. **Active forgiveness**: Deliberately cooperates sometimes even when betrayed
4. **Group-focused**: Responds to overall group behavior rather than punishing individuals
5. **Second chances**: The forgiveness mechanism allows groups to recover from defection spirals

### Expected Behavior

- Against other cooperative strategies: Maintains high mutual cooperation
- Against mixed strategies: Encourages cooperation while protecting against excessive exploitation  
- Against primarily defecting strategies: Eventually defects but occasionally attempts to restart cooperation
- In diverse groups: Adapts to the overall cooperation level while maintaining cooperative bias

This strategy should perform well in a tournament of LLM-generated strategies, as it balances the cooperative imperative with practical game-theoretic considerations.
'''

description_COOPERATIVE_39 = '''
Looking at this N-Player Public Goods Game, I need to design a cooperative strategy that can succeed in a tournament against other AI-generated strategies. Here's my approach:

## Strategy: "Generous Tit-for-Tat with Forgiveness" (GTTF)

### Core Philosophy
This strategy aims to promote cooperation while being robust against exploitation. It starts cooperatively, reciprocates the group's behavior, but includes forgiveness mechanisms to recover from mutual defection spirals.

### Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

INITIALIZATION:
- cooperation_threshold = 0.5  // Require majority cooperation to continue cooperating
- forgiveness_probability = 0.1  // Chance to cooperate even when group defects
- recent_window = min(3, r/4)  // Look at recent rounds for trend analysis

DECISION PROCESS for round t:

IF t == 1:
    RETURN C  // Always cooperate in first round

IF t == r:  // Last round
    IF (cooperation_rate_in_recent_rounds >= cooperation_threshold):
        RETURN C  // Reward consistent cooperators
    ELSE:
        RETURN D  // Don't be exploited in final round

// Main strategy for rounds 2 to r-1:
recent_cooperation_rate = calculate_recent_cooperation_rate(recent_window)
overall_cooperation_rate = calculate_overall_cooperation_rate()

// Primary decision based on recent behavior
IF recent_cooperation_rate >= cooperation_threshold:
    RETURN C  // Reciprocate cooperation

ELSE IF recent_cooperation_rate < cooperation_threshold:
    // Forgiveness mechanism
    IF random() < forgiveness_probability:
        RETURN C  // Occasional forgiveness to break defection cycles
    ELSE:
        RETURN D  // Reciprocate defection

HELPER FUNCTIONS:

calculate_recent_cooperation_rate(window):
    recent_rounds = min(window, t-1)
    total_cooperators = 0
    for i in range(t-recent_rounds, t):
        total_cooperators += count_cooperators_in_round(i)
    return total_cooperators / (recent_rounds * (n-1))

calculate_overall_cooperation_rate():
    total_cooperators = 0
    for i in range(1, t):
        total_cooperators += count_cooperators_in_round(i)
    return total_cooperators / ((t-1) * (n-1))
```

### Key Features

1. **Cooperative Start**: Always cooperate in round 1 to signal cooperative intent and test waters.

2. **Majority-Based Reciprocation**: Continue cooperating as long as at least 50% of other players cooperated recently. This prevents being swayed by a single defector while still responding to group trends.

3. **Recency Weighting**: Focus more on recent rounds (last 3 rounds or 25% of game length) rather than entire history, allowing adaptation to changing group dynamics.

4. **Forgiveness Mechanism**: 10% chance to cooperate even when the group is defecting, which helps break mutual defection spirals and signal willingness to restart cooperation.

5. **Strategic Last Round**: In the final round, cooperate only if the group has been consistently cooperative, otherwise defect to avoid end-game exploitation.

### Edge Case Handling

- **First Round**: Always cooperate to establish cooperative intent
- **Last Round**: Conditional cooperation based on group's recent behavior
- **All Defect Scenario**: Occasional forgiveness attempts to restart cooperation
- **Mixed Groups**: Responds to majority behavior while maintaining some forgiveness
- **Small n**: Works with minimum n=2, scales naturally to larger groups

### Rationale

This strategy balances several key considerations:

1. **Exploitation Resistance**: Won't be consistently exploited by always-defect strategies
2. **Cooperation Promotion**: Rewards and encourages cooperative behavior
3. **Adaptability**: Can adjust to different group compositions and behaviors
4. **Recovery Capability**: Forgiveness mechanism prevents permanent defection spirals
5. **Tournament Viability**: Should perform well against a mix of cooperative, selfish, and strategic opponents

The strategy should cooperate with other cooperative strategies while protecting against exploitation, making it well-suited for a tournament environment where strategy diversity is expected.
'''

description_COOPERATIVE_40 = '''
# Cooperative Strategy: "Forgiving Tit-for-Tat with Majority Threshold"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with practical self-protection mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Always COOPERATE** in the first round
- Rationale: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation with Majority Threshold

**Primary Rule: Majority-Based Cooperation**
```
if (cooperators_last_round >= n/2):
    play COOPERATE
else:
    play DEFECT
```

**Override Rule: Forgiveness Mechanism**
```
if (consecutive_defections >= 2 AND cooperators_last_round < n/2):
    if (random_chance <= 0.3):  // 30% forgiveness probability
        play COOPERATE  // Attempt to restart cooperation
    else:
        apply primary rule
```

### Final Round (Round r): Conditional Cooperation
```
if (cooperators_in_round_r-1 >= n/2):
    play COOPERATE  // Reward good behavior even at the end
else:
    play DEFECT     // Protect against end-game defection
```

## Detailed Strategy Logic

### 1. Majority Threshold Rationale
- Cooperate when at least half the players cooperated in the previous round
- This creates a stable equilibrium where cooperation can be sustained
- Protects against minority exploitation while encouraging cooperative coalitions

### 2. Forgiveness Mechanism
- After 2+ consecutive rounds of being in the defecting minority, occasionally attempt to restart cooperation
- 30% probability prevents predictable exploitation while maintaining hope for cooperation recovery
- Only triggers when cooperation has broken down (< n/2 cooperators)

### 3. End-Game Handling
- Many strategies defect in the final round due to no future retaliation
- Counter this by continuing to cooperate if the group was cooperative in round r-1
- This rewards consistent cooperators and may establish reputation for future interactions

### 4. Edge Case Handling

**Tie Situations (n is even, exactly n/2 cooperators):**
- Treat as meeting the majority threshold → COOPERATE
- Encourages breaking ties toward cooperation

**All Defect Scenarios:**
- Will defect in response but forgiveness mechanism provides escape route
- Prevents permanent punishment spirals

**All Cooperate Scenarios:**
- Will always cooperate in response, maintaining the optimal outcome

## Pseudocode Implementation

```python
def decide_action(round_num, history, n, r):
    # Round 1: Always cooperate
    if round_num == 1:
        return COOPERATE
    
    # Get last round's cooperation count
    last_round_cooperators = count_cooperators(history, round_num - 1)
    majority_threshold = n / 2
    
    # Final round: Conditional cooperation
    if round_num == r:
        return COOPERATE if last_round_cooperators >= majority_threshold else DEFECT
    
    # Main strategy: Majority-based with forgiveness
    if last_round_cooperators >= majority_threshold:
        return COOPERATE
    else:
        # Check for forgiveness opportunity
        consecutive_defections = count_consecutive_defections(history, round_num)
        if consecutive_defections >= 2 and random() < 0.3:
            return COOPERATE  # Forgiveness attempt
        else:
            return DEFECT
```

## Strategic Advantages

1. **Cooperative Stability**: When most players cooperate, maintains cooperation
2. **Exploitation Resistance**: Punishes free-riders by defecting when they dominate
3. **Recovery Capability**: Forgiveness mechanism allows escape from defection spirals
4. **Clear Signaling**: Behavior is predictable and encourages others to cooperate
5. **End-Game Robustness**: Doesn't automatically defect in final round, rewarding sustained cooperation

This strategy should perform well against other cooperative strategies while providing reasonable protection against exploitative ones, making it suitable for a mixed-strategy tournament environment.
'''

description_COOPERATIVE_41 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances optimism with self-protection to maximize collective welfare.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This would be the first time cooperating after defecting, OR
- The cooperation rate was ≥ 33% (showing some cooperative spirit exists)

**Pseudocode**:
```
previous_coop_rate = count_cooperators_last_round / n

if previous_coop_rate >= 0.5:
    action = COOPERATE
elif just_defected_last_round and previous_coop_rate >= 0.33:
    action = COOPERATE  // Forgiveness attempt
elif previous_coop_rate >= 0.33:
    action = COOPERATE  // Give benefit of doubt
else:
    action = DEFECT     // Protect against exploitation
```

### Final Round (Round r): Conditional Cooperation
- **If cooperation rate has been ≥ 50% in the last 2 rounds**: COOPERATE
- **Otherwise**: DEFECT
- **Rationale**: Reward sustained cooperation but protect against end-game defection

## Key Features

### 1. **Generous Starting Position**
- Always cooperates in round 1 to signal cooperative intent
- Assumes others are also cooperative-minded

### 2. **Majority-Based Cooperation**
- Cooperates when most others cooperated previously
- Recognizes that cooperation is sustainable when it's the norm

### 3. **Forgiveness Mechanism**
- Gives second chances after defecting
- Cooperates even when cooperation rate is low (33-49%) to help rebuild trust
- Prevents permanent breakdown of cooperation

### 4. **Protection Against Exploitation**
- Defects when cooperation rate drops below 33%
- Prevents being systematically exploited by predominantly defecting opponents

### 5. **End-Game Awareness**
- In the final round, only cooperates if recent cooperation has been strong
- Balances final cooperation with protection against last-round defection

## Strategic Reasoning

**Why This Works**:
1. **Establishes Cooperation**: Optimistic start encourages mutual cooperation
2. **Maintains Cooperation**: Majority rule keeps cooperation stable when established
3. **Recovers from Breakdowns**: Forgiveness helps rebuild cooperation after temporary failures
4. **Resists Exploitation**: Defects against consistently non-cooperative opponents
5. **Handles Mixed Populations**: Adapts to varying levels of cooperation in opponent pool

**Tournament Considerations**:
- Performs well against other cooperative strategies (mutual cooperation)
- Protects against purely selfish strategies (conditional defection)
- Can establish cooperation with conditionally cooperative strategies
- Robust against noise and occasional mistakes by opponents

This strategy maximizes the chances of achieving the socially optimal outcome (full cooperation) while maintaining reasonable protection against exploitation.
'''

description_COOPERATIVE_42 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances trust-building with self-protection.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability 0.2 (generous forgiveness)
- **Formal Rule**:
```
cooperation_rate = (number of cooperators in previous round) / n

if cooperation_rate >= 0.5:
    action = COOPERATE
else:
    action = COOPERATE with probability 0.2, DEFECT with probability 0.8
```

### Final Round (Round r): Reciprocal Response
- **Action**: Mirror the majority action from round r-1
- **Rationale**: Maintain consistency with cooperative pattern while protecting against end-game exploitation

## Pseudocode Implementation

```python
def decide_action(round_number, game_history, n, r):
    # Round 1: Always cooperate
    if round_number == 1:
        return COOPERATE
    
    # Get previous round results
    previous_round = game_history[round_number - 2]  # 0-indexed
    cooperators_last_round = sum(1 for action in previous_round if action == COOPERATE)
    cooperation_rate = cooperators_last_round / n
    
    # Final round: Mirror majority from previous round
    if round_number == r:
        if cooperation_rate >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds: Conditional cooperation with forgiveness
    if cooperation_rate >= 0.5:
        return COOPERATE
    else:
        # Forgiveness mechanism: 20% chance to cooperate even when majority defected
        return COOPERATE if random() < 0.2 else DEFECT
```

## Strategy Properties

### Cooperative Elements
1. **Optimistic Start**: Always begins with cooperation to signal good intentions
2. **Majority Responsive**: Rewards group cooperation by continuing to cooperate
3. **Forgiving Nature**: Gives second chances even after poor cooperation rounds
4. **Sustained Cooperation**: Doesn't abandon cooperation after single bad rounds

### Defensive Elements
1. **Conditional Response**: Reduces cooperation when facing persistent defection
2. **End-Game Protection**: Adapts final round behavior to prevent exploitation
3. **Threshold-Based**: Uses clear 50% threshold to avoid being overly lenient

### Adaptive Features
1. **Dynamic Response**: Adjusts behavior based on group dynamics
2. **Probabilistic Forgiveness**: Maintains some cooperation even in hostile environments
3. **History-Sensitive**: Uses recent information to guide decisions

## Expected Performance

**Against Cooperative Strategies**: Will establish mutual cooperation quickly and maintain it throughout most rounds.

**Against Mixed Strategies**: Will adapt to the cooperation level, maintaining cooperation when feasible while protecting against exploitation.

**Against Aggressive Strategies**: Will initially attempt cooperation but gradually reduce cooperation frequency while maintaining some forgiveness to allow recovery.

This strategy should perform well in tournaments by:
- Building cooperative coalitions with like-minded strategies
- Avoiding exploitation by overly aggressive opponents  
- Maintaining flexibility to adapt to various opponent types
- Preserving the cooperative gains that make everyone better off when possible
'''

description_COOPERATIVE_43 = '''
# Adaptive Tit-for-Tat with Forgiveness (ATTF) Strategy

## Core Philosophy
This strategy aims to foster cooperation while protecting against exploitation by starting cooperatively, reciprocating the group's behavior, and incorporating forgiveness to break cycles of mutual defection.

## Decision Rules

### Round 1: Cooperative Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Adaptive Response with Forgiveness
```pseudocode
cooperation_threshold = n / 2  // Majority threshold
forgiveness_probability = 0.15  // 15% chance to forgive

if round_number <= 3:
    // Early rounds: More lenient, encourage cooperation
    cooperation_threshold = n / 3
    forgiveness_probability = 0.25

cooperators_last_round = count(C actions in previous round)
group_cooperation_rate = cooperators_last_round / n

if group_cooperation_rate >= cooperation_threshold/n:
    action = COOPERATE
else:
    // Group defected, but consider forgiveness
    if random() < forgiveness_probability:
        action = COOPERATE  // Forgive and try to restart cooperation
    else:
        action = DEFECT     // Reciprocate defection
```

### Final Round (Round r): Strategic Cooperation
```pseudocode
recent_cooperation_rate = average_cooperation_rate(last_3_rounds)

if recent_cooperation_rate >= 0.4:
    action = COOPERATE  // Reward sustained cooperation
else:
    action = DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Graduated Response
- **Early rounds (1-3)**: More forgiving threshold (n/3 cooperators needed)
- **Middle rounds**: Standard majority threshold (n/2 cooperators needed)
- **Final round**: Based on recent cooperation history

### 2. Forgiveness Mechanism
- 15-25% chance to cooperate even when group defected
- Higher forgiveness in early rounds (25%) vs later rounds (15%)
- Breaks potential defection spirals

### 3. Majority-Based Decisions
- Responds to group behavior rather than individual players
- More stable against noise from individual defectors
- Scales appropriately with group size n

### 4. End-Game Protection
- Considers recent cooperation trends in final round
- Balances cooperation reward with exploitation protection

## Edge Case Handling

- **All players always defect**: Strategy will eventually reciprocate but periodically attempt forgiveness
- **Mixed strategies**: Responds to majority behavior while maintaining some cooperation
- **End-game defection**: Protected by analyzing recent trends rather than just final round incentives
- **Small groups**: Thresholds adjust appropriately (n/3 or n/2)

## Strategic Rationale

1. **Cooperative Start**: Establishes good faith and allows mutual cooperation to emerge
2. **Reciprocity**: Punishes mass defection while rewarding group cooperation  
3. **Forgiveness**: Prevents permanent defection cycles and allows cooperation recovery
4. **Adaptive Thresholds**: More lenient early on when cooperation norms are forming
5. **End-game Consideration**: Balances final round incentives with overall relationship maintenance

This strategy achieves high mutual payoffs when facing other cooperative strategies while maintaining reasonable protection against exploitation.
'''

description_COOPERATIVE_44 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Majority Threshold"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It uses a combination of conditional cooperation, forgiveness, and majority-based decision making.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and attempt to establish a cooperative norm from the start

**Rounds 2 to r-1 (Main Game):**
Apply the following logic in order:

1. **Majority Cooperation Check:**
   - If ≥ 50% of players cooperated in the previous round: COOPERATE
   - This maintains cooperation when it's already established

2. **Minority Cooperation Threshold:**
   - If < 50% but ≥ 25% of players cooperated in the previous round: COOPERATE with probability 0.7, DEFECT with probability 0.3
   - This provides some forgiveness and attempts to restart cooperation

3. **Low Cooperation Response:**
   - If < 25% of players cooperated in the previous round: DEFECT
   - Protects against systematic exploitation

**Round r (Final Round):**
- **Cooperative Ending:** Always COOPERATE regardless of previous round
- Rationale: Signal long-term cooperative intent and avoid the typical end-game defection cascade that could spill over into future interactions or tournament reputation

## Pseudocode

```
function choose_action(round_number, game_history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == final_round:
        return COOPERATE
    
    previous_round = game_history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / n
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    elif cooperation_rate >= 0.25:
        return COOPERATE with probability 0.7
    else:
        return DEFECT
```

## Key Features

### 1. **Conditional Cooperation**
- Responds positively to cooperative environments
- Uses majority behavior as the primary signal

### 2. **Graduated Response**
- Three-tier response system based on cooperation levels
- Avoids binary all-or-nothing reactions

### 3. **Forgiveness Mechanism**
- The 70% cooperation probability in medium-cooperation scenarios provides opportunities to restart cooperation
- Prevents permanent defection spirals

### 4. **Edge Case Handling**
- **First Round:** Unconditional cooperation to signal intent
- **Final Round:** Unconditional cooperation to maintain cooperative reputation
- **Low Participation:** Protection against systematic exploitation

### 5. **Robustness**
- Works across different group sizes (n)
- Adapts to varying cooperation levels
- Balances exploitation protection with cooperation maintenance

## Strategic Rationale

This strategy is designed to:
- **Initiate Cooperation:** Start cooperatively to establish positive dynamics
- **Sustain Cooperation:** Maintain cooperation when others are cooperative
- **Recover Cooperation:** Provide pathways back to cooperation after defection episodes  
- **Prevent Exploitation:** Protect against players who consistently defect
- **Signal Reliability:** End cooperatively to maintain reputation for future interactions

The strategy acknowledges that in a tournament setting with other AI strategies, many will likely implement some form of conditional cooperation, making this approach well-suited to establish mutually beneficial outcomes while remaining robust against purely selfish strategies.
'''

description_COOPERATIVE_45 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through a forgiving but responsive approach.

## Core Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Step 1: Calculate Cooperation Rate**
```
cooperation_rate = (total_cooperators_last_round) / n
```

**Step 2: Apply Decision Logic**
```
if cooperation_rate >= 0.5:
    action = COOPERATE
else if cooperation_rate >= 0.3:
    if my_last_action == DEFECT:
        action = COOPERATE  // Forgiveness after punishment
    else:
        action = DEFECT     // Punish low cooperation
else:  // cooperation_rate < 0.3
    action = DEFECT         // Protect against exploitation
```

### Final Round (Round r): Conditional Cooperation
```
if cooperation_rate_last_round >= 0.5:
    action = COOPERATE      // Reward sustained cooperation
else:
    action = DEFECT         // Protect against end-game defection
```

## Strategy Components Explained

### 1. **Generous Starting Position**
- Begin with cooperation to signal willingness to work together
- Gives other players the benefit of the doubt initially

### 2. **Majority-Based Cooperation**
- When ≥50% of players cooperated last round, continue cooperating
- This maintains cooperation when it's the dominant behavior

### 3. **Graduated Response to Declining Cooperation**
- At 30-49% cooperation: Alternate between punishment (D) and forgiveness (C)
- At <30% cooperation: Consistently defect to avoid exploitation

### 4. **Forgiveness Mechanism**
- After punishing with defection, immediately return to cooperation if the group shows moderate cooperation levels
- Prevents permanent breakdown of cooperation due to temporary conflicts

### 5. **End-Game Consideration**
- In the final round, only cooperate if the group has maintained good cooperation
- Protects against predictable last-round defection cascades

## Key Advantages

1. **Cooperative Foundation**: Starts cooperatively and maintains cooperation when others do
2. **Exploitation Resistance**: Defects when cooperation falls too low
3. **Relationship Repair**: Forgiveness mechanism allows recovery from punishment cycles
4. **Adaptive**: Responds to the actual behavior of the group rather than fixed assumptions
5. **Clear Signals**: Behavior clearly communicates expectations to other players

## Pseudocode Implementation

```python
def decide_action(round_number, total_rounds, history):
    if round_number == 1:
        return COOPERATE
    
    last_round_cooperators = count_cooperators(history[-1])
    cooperation_rate = last_round_cooperators / n
    my_last_action = get_my_last_action(history)
    
    if round_number == total_rounds:  # Final round
        return COOPERATE if cooperation_rate >= 0.5 else DEFECT
    
    # Main decision logic
    if cooperation_rate >= 0.5:
        return COOPERATE
    elif cooperation_rate >= 0.3:
        return COOPERATE if my_last_action == DEFECT else DEFECT
    else:
        return DEFECT
```

This strategy is designed to foster cooperation while maintaining resilience against exploitation, making it well-suited for a tournament environment where opponent strategies are unknown but likely include a mix of cooperative and competitive approaches.
'''

description_COOPERATIVE_46 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being robust against exploitation. It starts cooperatively, reciprocates the group's behavior, but includes forgiveness mechanisms to recover from defection spirals.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Reciprocity with Forgiveness

**Primary Rule**: Base decision on group cooperation rate from the previous round:

```pseudocode
cooperation_rate = (number_of_cooperators_last_round) / n
forgiveness_threshold = 0.15  // Probability of forgiving defection

IF cooperation_rate >= 0.5:
    action = C  // Reciprocate high cooperation
ELSE IF cooperation_rate >= 0.3:
    action = C with probability 0.7, D with probability 0.3  // Generous reciprocity
ELSE:
    IF random() < forgiveness_threshold:
        action = C  // Occasional forgiveness to break defection cycles
    ELSE:
        action = D  // Protect against exploitation
```

### Round r (Final Round): Conditional Cooperation
- **Action**: Cooperate if cooperation_rate in round r-1 >= 0.4, otherwise defect
- **Rationale**: In the last round, cooperate only if there's sufficient evidence of group cooperation

## Key Features

### 1. Generous Reciprocity
- When facing moderate cooperation (30-50% of players), still cooperate 70% of the time
- This helps maintain cooperation even when the group is struggling

### 2. Forgiveness Mechanism
- Even in low-cooperation environments, occasionally cooperate (15% chance) to:
  - Test if others are willing to return to cooperation
  - Prevent permanent defection spirals
  - Signal continued willingness to cooperate

### 3. Exploitation Protection
- Defect consistently when facing very low cooperation (<30%)
- Avoid being systematically exploited while keeping the door open for cooperation

### 4. End-Game Handling
- Final round behavior depends on recent cooperation levels
- Prevents others from exploiting unconditional final-round cooperation

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative precedent

### Early Rounds (2-3)
- Weight recent behavior more heavily since sample size is small
- Be slightly more forgiving to account for learning/adjustment

### Final Round
- Use a higher threshold for cooperation (40% vs 30%) to avoid exploitation
- Still cooperate if group has shown reasonable cooperation

### Tie-Breaking
- When cooperation_rate = 0.5 exactly, cooperate (benefit of doubt)
- When facing exactly 30% cooperation, use the probabilistic rule

## Cooperative Alignment

This strategy embodies cooperation by:

1. **Starting with trust**: Opens with cooperation
2. **Rewarding cooperation**: Reciprocates when others cooperate
3. **Maintaining hope**: Uses forgiveness to recover from mutual defection
4. **Being generous**: Cooperates even in moderately hostile environments
5. **Avoiding exploitation**: Protects against systematic free-riding while remaining open to cooperation

The strategy balances the cooperative ideal with practical considerations for a competitive tournament environment, aiming to achieve high mutual payoffs while avoiding exploitation.
'''

description_COOPERATIVE_47 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being cooperative, forgiving, and protective against persistent defectors.

## Decision Rules

### Core Logic:
```
GTTF Strategy:
1. Start cooperatively (C in round 1)
2. Track each player's cooperation rate over recent history
3. Cooperate if the majority of players are "sufficiently cooperative"
4. Include forgiveness mechanisms to recover from mutual defection spirals
5. Protect against end-game defection
```

### Detailed Implementation:

```pseudocode
INITIALIZE:
- cooperation_threshold = 0.6  // What % cooperation rate qualifies as "cooperative"
- majority_threshold = 0.5    // What % of players need to be cooperative
- forgiveness_probability = 0.1  // Chance to cooperate even when conditions aren't met
- memory_window = min(5, current_round)  // How many recent rounds to consider
- endgame_protection = 3      // Start protecting in last 3 rounds

FOR each round t:
    IF t == 1:
        RETURN C  // Always cooperate first
    
    // Calculate each player's recent cooperation rate
    FOR each other player j:
        recent_cooperations = count(C actions by j in last memory_window rounds)
        cooperation_rate[j] = recent_cooperations / memory_window
    
    // Count how many players are "sufficiently cooperative"
    cooperative_players = count(players j where cooperation_rate[j] >= cooperation_threshold)
    
    // Main decision logic
    IF (rounds_remaining <= endgame_protection AND any_player_defected_recently):
        // End-game protection: be cautious if someone started defecting
        IF (cooperative_players / (n-1) >= 0.8):  // Very high bar for end-game cooperation
            RETURN C
        ELSE:
            RETURN D
    
    ELIF (cooperative_players / (n-1) >= majority_threshold):
        // Majority are cooperative - reciprocate
        RETURN C
    
    ELIF (all_players_defected_last_round):
        // Forgiveness mechanism - occasionally cooperate to break deadlocks
        IF (random() < forgiveness_probability):
            RETURN C
        ELSE:
            RETURN D
    
    ELSE:
        // Default to defection when cooperation isn't reciprocated
        RETURN D
```

## Strategy Components Explained

### 1. **Cooperative Start**
- Always cooperate in round 1 to signal cooperative intent
- This gives other cooperative strategies a chance to recognize and reciprocate

### 2. **Adaptive Memory Window**
- Uses recent history (last 5 rounds or fewer if early in game)
- Allows strategy to adapt to changing opponent behavior
- Prevents being stuck based on very old actions

### 3. **Majority-Based Cooperation**
- Cooperates when a majority of opponents are sufficiently cooperative (≥60% cooperation rate)
- This creates incentives for others to maintain high cooperation rates

### 4. **Forgiveness Mechanism**
- 10% chance to cooperate even when conditions suggest defection
- Helps break out of mutual defection spirals
- Particularly important when all players defected in previous round

### 5. **End-Game Protection**
- In final 3 rounds, uses stricter criteria (80% vs 50%) if any defection detected
- Protects against end-game exploitation while still allowing cooperation with consistently cooperative players

### 6. **Edge Case Handling**

**First Round:** Always cooperate to signal cooperative intent

**Last Round:** Apply end-game protection - only cooperate if opponents have been very consistently cooperative

**All-Defection Situations:** Use forgiveness probability to occasionally attempt cooperation restoration

**Mixed Situations:** Use majority rule with cooperation threshold

## Cooperative Alignment

This strategy embodies cooperation through:

1. **Default Cooperation:** Starts cooperatively and maintains cooperation when reciprocated
2. **Forgiveness:** Doesn't permanently punish occasional defections
3. **Collective Focus:** Makes decisions based on group behavior rather than individual grudges
4. **Recovery Mechanism:** Actively tries to restore cooperation after breakdowns

## Expected Performance

- **Against other cooperative strategies:** Should achieve high mutual cooperation
- **Against mixed strategies:** Will cooperate when it's reciprocated, defect when exploited
- **Against aggressive defectors:** Will protect itself while occasionally offering olive branches
- **In diverse tournaments:** Should perform well by fostering cooperation while avoiding exploitation

The strategy balances the cooperative goal with the practical need to avoid being exploited, making it robust across different opponent types while maintaining a fundamentally cooperative approach.
'''

description_COOPERATIVE_48 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperative behavior while being resilient to occasional defections and exploitation attempts. It balances being "nice" (never defecting first), "retaliatory" (responding to defections), and "forgiving" (allowing recovery from conflict spirals).

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent from the start. Since other strategies may also start cooperatively, this maximizes the chance of establishing mutual cooperation.

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = 0.5  // Require majority cooperation to continue cooperating
forgiveness_probability = 0.1  // 10% chance to cooperate even when below threshold

total_cooperators_last_round = count_cooperators(previous_round)
cooperation_rate = total_cooperators_last_round / n

if cooperation_rate >= cooperation_threshold:
    action = C
else:
    // Apply forgiveness mechanism
    if random() < forgiveness_probability:
        action = C
    else:
        action = D
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
// In the last round, cooperate if cooperation has been sustained
recent_rounds = min(3, r-1)  // Look at last 3 rounds or all available rounds
average_cooperation = calculate_average_cooperation(recent_rounds)

if average_cooperation >= 0.6:
    action = C  // Reward sustained cooperation
else:
    action = D  // Protect against end-game defection
```

## Key Features

### 1. **Majority Rule with Tolerance**
- Cooperate when at least 50% of players cooperated in the previous round
- This creates a stable equilibrium point where cooperation can be sustained

### 2. **Forgiveness Mechanism**
- 10% probability of cooperating even when cooperation rate is below threshold
- Prevents permanent defection spirals
- Allows recovery from temporary coordination failures

### 3. **End-Game Protection**
- Evaluates recent cooperation history in the final round
- Cooperates only if there's strong evidence of sustained cooperation
- Protects against opponents who defect in the final round

### 4. **Simplicity and Transparency**
- Clear, predictable rules that other strategies can learn and adapt to
- Encourages mutual cooperation by being easy to understand

## Strategic Reasoning

### Against Other Cooperative Strategies
- Will quickly establish mutual cooperation (both start with C)
- Maintains cooperation as long as the majority remains cooperative
- Forgiveness prevents minor disagreements from destroying cooperation

### Against Mixed Strategies
- The 50% threshold means cooperation can be sustained even with some defectors
- Forgiveness allows recovery if cooperation temporarily drops below threshold

### Against Aggressive Strategies
- Will initially attempt cooperation but switch to defection if cooperation rate is too low
- Protects against pure exploitation while leaving room for redemption

### Tournament Dynamics
- In a diverse tournament, this strategy will cooperate with other cooperative strategies while protecting against purely selfish ones
- The majority rule means it will adapt to the overall tournament environment

## Mathematical Justification

With parameters n=6, k=2:
- All cooperate: payoff = 2 per round
- 3 cooperate, 3 defect: cooperators get 1, defectors get 2
- The 50% threshold ensures cooperation is maintained when it's collectively beneficial
- Forgiveness (10% rate) provides approximately 0.1 × (cooperation_payoff - defection_payoff) expected value for relationship repair

This strategy balances collective welfare with individual protection, making it robust across different tournament compositions while maintaining a fundamentally cooperative orientation.
'''

description_COOPERATIVE_49 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Graduated Reciprocation"

## Core Philosophy
This strategy balances cooperative intent with protection against exploitation, using a forgiving approach that encourages mutual cooperation while maintaining credible responses to defection.

## Decision Rules

### Round 1: Cooperative Opening
- **Always cooperate** in the first round to signal cooperative intent and give others the benefit of the doubt.

### Rounds 2 to r-1: Adaptive Reciprocation
The strategy uses a **cooperation threshold** based on the previous round's cooperation rate:

```pseudocode
cooperation_rate = (number_of_cooperators_last_round) / n
cooperation_threshold = 0.4  // Generous threshold

if cooperation_rate >= cooperation_threshold:
    cooperate()
else:
    // Graduated response based on cooperation level
    if cooperation_rate >= 0.2:
        cooperate_with_probability(0.7)  // Still mostly cooperative
    else:
        cooperate_with_probability(0.3)  // Defensive but not fully defecting
```

### Round r (Final Round): Conditional Cooperation
In the last round, maintain cooperative behavior if there's been reasonable cooperation:

```pseudocode
overall_cooperation_rate = total_cooperations_by_others / ((r-1) * (n-1))

if overall_cooperation_rate >= 0.3:
    cooperate()
else:
    defect()  // Protect against end-game defection
```

## Key Features

### 1. Forgiveness Mechanism
- Uses probabilistic responses rather than strict tit-for-tat
- Maintains some cooperation even when others defect moderately
- Prevents spiral of mutual defection

### 2. Graduated Reciprocation
- Response intensity matches the level of non-cooperation observed
- High cooperation (≥40%) → Full cooperation
- Medium cooperation (20-39%) → High cooperation (70% chance)
- Low cooperation (<20%) → Defensive cooperation (30% chance)

### 3. Collective Assessment
- Evaluates the group's overall behavior rather than tracking individual players
- More robust against noise and individual variations
- Encourages group-level cooperation

## Strategic Rationale

### Why This Strategy is Cooperative:
1. **Starts with trust** - Always cooperates first
2. **Rewards group cooperation** - Maintains high cooperation when others do
3. **Forgives mistakes** - Doesn't punish single defections harshly
4. **Encourages recovery** - Allows groups to return to cooperation

### Protection Against Exploitation:
1. **Graduated response** - Reduces cooperation when faced with high defection
2. **End-game protection** - Guards against final round exploitation
3. **Credible deterrent** - Shows willingness to reduce cooperation if necessary

### Tournament Considerations:
- **Against other cooperators**: Maintains mutual cooperation effectively
- **Against mixed strategies**: Adapts cooperation level appropriately
- **Against exploiters**: Reduces losses while maintaining some cooperative signals
- **In diverse groups**: Flexible enough to handle varying strategy mixes

## Implementation Notes

```pseudocode
function decide_action(round_number, game_history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == r:  // Final round
        return final_round_decision(game_history)
    
    last_round_cooperators = count_cooperators(game_history, round_number - 1)
    cooperation_rate = last_round_cooperators / n
    
    if cooperation_rate >= 0.4:
        return COOPERATE
    elif cooperation_rate >= 0.2:
        return random_choice(COOPERATE with prob 0.7, DEFECT with prob 0.3)
    else:
        return random_choice(COOPERATE with prob 0.3, DEFECT with prob 0.7)
```

This strategy maintains a fundamentally cooperative stance while being smart about when and how much to trust, making it well-suited for a tournament environment with diverse opponents.
'''

description_COOPERATIVE_50 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being cooperative with being defensive against persistent defectors.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Adaptive Cooperation
- **Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
  - This is only the second consecutive round with low cooperation, OR
  - The cooperation rate is improving compared to two rounds ago
- **Defection Trigger**: Defect only if cooperation rate has been < 50% for 3+ consecutive rounds

### Round r (Final Round): Conditional Cooperation
- **Action**: Cooperate if cooperation rate in round r-1 was ≥ 60%
- **Rationale**: Slightly higher threshold for final round to account for end-game defection incentives

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        cooperation_rate_last = calculate_cooperation_rate(history, round_number-1)
        return COOPERATE if cooperation_rate_last >= 0.6 else DEFECT
    
    // For rounds 2 to r-1
    cooperation_rate_last = calculate_cooperation_rate(history, round_number-1)
    
    if cooperation_rate_last >= 0.5:
        return COOPERATE
    
    // Check forgiveness conditions
    consecutive_low_coop = count_consecutive_low_cooperation(history, round_number-1)
    
    if consecutive_low_coop <= 2:
        return COOPERATE  // Forgiveness for early defections
    
    if round_number >= 3:
        cooperation_rate_two_ago = calculate_cooperation_rate(history, round_number-2)
        if cooperation_rate_last > cooperation_rate_two_ago:
            return COOPERATE  // Cooperation is improving
    
    return DEFECT  // Persistent low cooperation detected

function calculate_cooperation_rate(history, round):
    return (number_of_cooperators_in_round) / (total_players)

function count_consecutive_low_cooperation(history, current_round):
    count = 0
    for round from current_round down to 1:
        if calculate_cooperation_rate(history, round) < 0.5:
            count += 1
        else:
            break
    return count
```

## Key Features

### 1. **Generous Initial Cooperation**
- Always cooperates in round 1 to signal cooperative intent
- Gives benefit of the doubt in early rounds

### 2. **Majority-Based Decision Making**
- Uses 50% cooperation threshold as the primary decision criterion
- Recognizes that full cooperation may not always be achievable

### 3. **Forgiveness Mechanism**
- Allows for 2 consecutive rounds of low cooperation before retaliating
- Continues cooperating if cooperation rates are improving
- Prevents permanent defection spirals

### 4. **End-Game Adjustment**
- Raises cooperation threshold to 60% in final round
- Accounts for natural tendency to defect in last round

### 5. **Resilience Against Exploitation**
- Will defect if faced with persistent low cooperation (3+ rounds)
- Protects against being exploited by consistent defectors

## Strategic Rationale

1. **Promotes Collective Welfare**: Since k < n, universal cooperation yields higher payoffs than universal defection
2. **Evolutionary Stable**: Can coexist with other cooperative strategies while defending against exploitative ones  
3. **Adaptive**: Responds to the actual behavior of opponents rather than making rigid assumptions
4. **Forgiving**: Doesn't punish occasional mistakes or temporary defections harshly
5. **Clear Signaling**: Consistent behavior helps establish trust and coordination with like-minded strategies

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against more exploitative approaches.
'''

description_COOPERATIVE_51 = '''
I'll design a cooperative strategy called "Graduated Reciprocal Cooperation" (GRC) that balances cooperation with protection against exploitation.

## Strategy: Graduated Reciprocal Cooperation (GRC)

### Core Principles
1. **Start cooperative** to signal willingness to collaborate
2. **Respond proportionally** to the group's cooperation level
3. **Forgive gradually** to recover from mutual defection spirals
4. **Protect against exploitation** while maintaining cooperative intent

### Decision Rules

```pseudocode
STRATEGY: Graduated Reciprocal Cooperation (GRC)

INITIALIZE:
- cooperation_threshold = 0.4  // Cooperate if 40%+ cooperated last round
- forgiveness_counter = 0
- last_round_coop_rate = 1.0   // Assume cooperation initially

FOR each round t:
    IF t == 1:  // First round
        PLAY C
        
    ELIF t == final_round:  // Last round
        IF last_round_coop_rate >= 0.6:
            PLAY C  // Reward high cooperation
        ELSE:
            PLAY D  // Don't be exploited in final round
            
    ELSE:  // Middle rounds
        current_coop_rate = (cooperators_last_round) / n
        
        // Main cooperation condition
        IF current_coop_rate >= cooperation_threshold:
            PLAY C
            forgiveness_counter = 0  // Reset forgiveness
            
        // Forgiveness mechanism
        ELIF forgiveness_counter < 2 AND current_coop_rate >= 0.2:
            PLAY C
            forgiveness_counter += 1
            
        // Adaptive threshold adjustment
        ELIF current_coop_rate > last_round_coop_rate:  // Improving trend
            PLAY C
            forgiveness_counter = 0
            
        ELSE:
            PLAY D
            
    // Update for next round
    last_round_coop_rate = current_coop_rate
```

### Detailed Strategy Components

#### 1. **Opening Move**
- **Always cooperate** in round 1 to signal cooperative intent
- This establishes a prosocial reputation from the start

#### 2. **Main Cooperation Rule**
- **Cooperate when ≥40% cooperated last round**
- This threshold is below 50% to maintain cooperation even when the group is somewhat divided
- Provides stability against minor defections

#### 3. **Forgiveness Mechanism**
- **Up to 2 consecutive forgiveness moves** when cooperation drops below threshold
- Only forgive if cooperation rate ≥20% (prevents forgiveness during mass defection)
- Helps break defection spirals and signals willingness to restart cooperation

#### 4. **Trend Recognition**
- **Cooperate if cooperation is increasing**, even below threshold
- Rewards and encourages positive momentum in the group
- Prevents premature abandonment of recovering cooperation

#### 5. **Endgame Handling**
- **Final round**: Cooperate only if recent cooperation was strong (≥60%)
- Protects against exploitation while rewarding consistently cooperative groups
- Balances group benefit with self-protection

### Strategic Rationale

**Why This Strategy is Cooperative:**
1. **Starts with trust** - Opens cooperatively
2. **Maintains cooperation** - Low threshold (40%) keeps cooperation alive
3. **Forgives mistakes** - Allows recovery from temporary defections  
4. **Rewards improvement** - Encourages positive group dynamics

**Protection Against Exploitation:**
1. **Conditional cooperation** - Won't cooperate with consistently defecting groups
2. **Limited forgiveness** - Prevents infinite exploitation
3. **Endgame protection** - Adjusts behavior in final round

**Adaptation Capabilities:**
1. **Threshold-based** - Scales naturally with group size
2. **Trend-sensitive** - Responds to improving situations
3. **History-informed** - Uses full information available

This strategy should perform well against other cooperative strategies while avoiding exploitation by purely selfish ones. It maintains the cooperative spirit while incorporating necessary safeguards for a competitive tournament environment.
'''

description_COOPERATIVE_52 = '''
# Generous Tit-for-Tat with Forgiveness (GTTF) Strategy

## Core Philosophy
This strategy balances cooperation with self-protection by starting cooperatively, reciprocating the community's behavior, and incorporating forgiveness to recover from defection spirals.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Reciprocation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round >= 0.5:
    action = C
else:
    action = D
```

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability 0.2 (generous forgiveness)

```pseudocode
if cooperation_rate_last_round < 0.5:
    if random() < 0.2:
        action = C  // Forgive and attempt to restart cooperation
    else:
        action = D
```

### Final Round (Round r): Conditional Cooperation
- **If cooperation rate in round r-1 ≥ 70%**: Cooperate (reward strong community cooperation)
- **If cooperation rate in round r-1 < 30%**: Defect (protect against exploitation)
- **If 30% ≤ cooperation rate < 70%**: Apply the same 50% threshold rule as middle rounds

## Strategy Rationale

### Cooperative Elements
1. **Optimistic Start**: Always cooperate in round 1 to signal good intentions
2. **Majority Rule**: Cooperates when most others cooperated, supporting collective action
3. **Forgiveness**: 20% chance to cooperate even when community defected, preventing permanent punishment spirals
4. **Endgame Cooperation**: More likely to cooperate in final round if community has been cooperative

### Self-Protection Elements
1. **Responsive Defection**: Defects when community cooperation falls below 50%
2. **Final Round Protection**: Won't be exploited in the last round if cooperation has been consistently low

### Advantages
- **Promotes Cooperation**: Rewards collective cooperation and attempts to restart it when it breaks down
- **Robust Against Exploitation**: Defects when facing predominantly non-cooperative players
- **Error Tolerance**: Forgiveness mechanism handles occasional mistakes or coordination failures
- **Clear Signal**: Behavior is predictable and based on observable community actions

## Edge Case Handling

1. **All others defect consistently**: Strategy will mostly defect but occasionally attempt cooperation
2. **Mixed cooperation levels**: Strategy adapts round-by-round based on community behavior
3. **High cooperation suddenly drops**: One round of defection, then attempts forgiveness
4. **Final round scenarios**: Balanced approach that rewards consistent cooperators but protects against last-round exploitation

This strategy aims to foster cooperation while remaining resilient against purely exploitative opponents, making it well-suited for a tournament environment with diverse strategic approaches.
'''

description_COOPERATIVE_53 = '''
# Graduated Reciprocator Strategy

## Core Philosophy
This strategy aims to foster and maintain cooperation while protecting against exploitation through graduated responses and forgiveness mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- Rationale: Start cooperatively to signal willingness to collaborate and give others the benefit of the doubt.

### Rounds 2 to r-1: Adaptive Reciprococation

**Step 1: Calculate Cooperation Rate**
```
cooperation_rate = (total_cooperators_last_round) / n
```

**Step 2: Determine Base Action**
```
if cooperation_rate >= 0.5:
    base_action = COOPERATE
else:
    base_action = DEFECT
```

**Step 3: Apply Forgiveness Mechanism**
```
if base_action == DEFECT and cooperation_rate >= 0.3:
    # Give benefit of doubt if cooperation isn't too low
    if random() < 0.3:  # 30% forgiveness probability
        base_action = COOPERATE
```

**Step 4: Apply Punishment Escalation**
```
consecutive_low_cooperation = count_consecutive_rounds(cooperation_rate < 0.3)

if consecutive_low_cooperation >= 2:
    # Escalate punishment for persistent defection
    base_action = DEFECT
    forgiveness_probability = max(0.1, 0.3 - 0.1 * consecutive_low_cooperation)
```

### Final Round (Round r): Strategic Endgame
```
if cooperation_rate_last_round >= 0.4:
    action = COOPERATE  # Reward consistent cooperators
else:
    action = DEFECT     # Protect against final-round exploitation
```

## Key Features

### 1. **Graduated Response System**
- Responds proportionally to the level of cooperation observed
- Avoids harsh punishment for minor defections
- Escalates response only when facing persistent non-cooperation

### 2. **Forgiveness Mechanism**
- 30% chance to cooperate even when cooperation rate is below threshold
- Prevents permanent punishment spirals
- Allows recovery from temporary coordination failures

### 3. **Threshold-Based Decision Making**
- Primary threshold: 50% cooperation rate triggers cooperation
- Secondary threshold: 30% cooperation rate triggers punishment escalation
- Endgame threshold: 40% cooperation rate for final round decision

### 4. **Exploitation Protection**
- Monitors consecutive rounds of low cooperation
- Reduces forgiveness probability as exploitation persists
- Strategic defection in final round when cooperation is insufficient

## Pseudocode Summary

```
function decide_action(round, history):
    if round == 1:
        return COOPERATE
    
    cooperation_rate = calculate_cooperation_rate(history, round-1)
    
    if round == total_rounds:
        return COOPERATE if cooperation_rate >= 0.4 else DEFECT
    
    base_action = COOPERATE if cooperation_rate >= 0.5 else DEFECT
    
    if base_action == DEFECT and cooperation_rate >= 0.3:
        if random() < forgiveness_probability():
            base_action = COOPERATE
    
    consecutive_low = count_consecutive_low_cooperation(history)
    if consecutive_low >= 2:
        base_action = DEFECT
    
    return base_action
```

## Strategic Rationale

1. **Promotes Cooperation**: Starts cooperatively and rewards group cooperation
2. **Prevents Exploitation**: Responds to persistent defection with appropriate punishment
3. **Enables Recovery**: Forgiveness mechanism allows groups to recover from coordination failures
4. **Adapts to Context**: Responds to actual behavior rather than predetermined patterns
5. **Handles Edge Cases**: Specific rules for first and last rounds address common strategic concerns

This strategy balances the cooperative imperative with rational self-protection, creating incentives for others to cooperate while avoiding exploitation.
'''

description_COOPERATIVE_54 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances the cooperative ideal with practical considerations for sustaining cooperation in a multi-player environment.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This is only the second consecutive round of low cooperation, AND
- At least one player cooperated in the previous round

**Defection Trigger**: Defect only when:
- Cooperation rate < 50% for 2+ consecutive rounds, AND
- Fewer than 2 players cooperated in the previous round

### Round r (Final Round): Conditional Cooperation
- **If** cooperation has been consistently high (≥50% in at least 75% of previous rounds): COOPERATE
- **Else**: DEFECT (since there's no future to maintain relationships for)

## Pseudocode

```
function decide_action(round, history):
    if round == 1:
        return COOPERATE
    
    if round == r:  // Final round
        cooperation_frequency = count_high_cooperation_rounds(history) / (r-1)
        if cooperation_frequency >= 0.75:
            return COOPERATE
        else:
            return DEFECT
    
    // Main game rounds (2 to r-1)
    prev_round_cooperation_rate = count_cooperators(history[-1]) / n
    
    if prev_round_cooperation_rate >= 0.5:
        return COOPERATE
    
    // Check forgiveness conditions
    if len(history) >= 2:
        prev2_cooperation_rate = count_cooperators(history[-2]) / n
        consecutive_low_cooperation = (prev2_cooperation_rate < 0.5)
        at_least_one_cooperated = count_cooperators(history[-1]) >= 1
        
        if not consecutive_low_cooperation or at_least_one_cooperated:
            return COOPERATE
    
    return DEFECT
```

## Strategic Rationale

### Cooperation Alignment
- **Initial Cooperation**: Starts cooperatively to signal good intentions
- **Majority Rule**: Maintains cooperation when most others do, reinforcing collective benefit
- **Forgiveness**: Doesn't immediately punish isolated defections, allowing for recovery

### Exploitation Resistance
- **Threshold Defense**: Won't be exploited indefinitely by chronic defectors
- **Graduated Response**: Requires sustained bad behavior before retaliating
- **End-game Consideration**: Accounts for final round incentives

### Edge Case Handling
1. **Round 1**: Always cooperate (no history to base decision on)
2. **Round 2**: Cooperate unless literally nobody cooperated in round 1
3. **Final Round**: Condition on overall game cooperation pattern
4. **All Defect Scenario**: Will eventually defect if cooperation completely breaks down
5. **Mixed Behavior**: Responds to overall trends rather than individual actions

## Expected Performance
This strategy should:
- Establish cooperation with other cooperative strategies
- Maintain cooperation against moderately exploitative strategies
- Eventually defend against purely exploitative strategies
- Perform well in mixed populations due to its adaptive nature

The 50% threshold is chosen because with k < n, individual cooperation is profitable when enough others cooperate, making this a natural coordination point.
'''

description_COOPERATIVE_55 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances trust-building with self-protection.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This is only the second consecutive round of low cooperation, AND
- My total payoff so far is not significantly below the "all-defect" baseline

**Defection Triggers**: Defect if:
- Cooperation rate has been < 50% for 2+ consecutive rounds, AND
- I'm being exploited (getting lower payoffs than consistent defectors)

### Final Round: Conditional Cooperation
- **If cooperation has been maintained** (≥50% rate in recent rounds): COOPERATE
- **If in a defection spiral**: DEFECT (protect against final-round exploitation)

## Pseudocode

```
function decide_action(round_number, game_history, my_history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        recent_coop_rate = cooperation_rate(last_3_rounds(game_history))
        if recent_coop_rate >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds (2 to r-1)
    prev_coop_rate = cooperation_rate(game_history[round_number-2])
    
    if prev_coop_rate >= 0.5:
        return COOPERATE
    
    # Low cooperation detected - check forgiveness conditions
    if consecutive_low_cooperation_rounds(game_history) <= 1:
        my_avg_payoff = calculate_average_payoff(my_history)
        defect_baseline = 1.0  # payoff from always defecting when others defect
        
        if my_avg_payoff >= defect_baseline * 0.9:  # 10% tolerance
            return COOPERATE  # Forgive occasional defection
    
    return DEFECT  # Protect against sustained exploitation
```

## Key Features

### 1. **Generous Opening**
- Always cooperate in round 1 to signal good intentions
- Attempts to establish cooperative equilibrium from the start

### 2. **Majority-Based Response**
- Cooperates when ≥50% of players cooperated in the previous round
- This threshold encourages broad cooperation while being realistic

### 3. **Forgiveness Mechanism**
- Gives one "second chance" even after low cooperation
- Prevents permanent defection spirals from single bad rounds
- Only forgives if not being severely exploited

### 4. **Exploitation Protection**
- Monitors own payoff relative to "all-defect" baseline
- Switches to defection if consistently exploited
- Prevents being a "sucker" in mixed populations

### 5. **Endgame Awareness**
- Maintains cooperation if recent trend is positive
- Protects against final-round backstabbing if already in defection mode

## Strategic Rationale

This strategy is designed to:
- **Maximize mutual cooperation** when playing against other cooperative strategies
- **Avoid exploitation** by purely selfish strategies
- **Recover from temporary setbacks** through forgiveness
- **Adapt to population composition** through majority-based rules

The 50% threshold is crucial: it's low enough to maintain cooperation even when some players defect, but high enough to avoid being exploited by mostly-defecting populations.
'''

description_COOPERATIVE_56 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperation with strategic self-protection.

## Core Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: Even if majority defected, still cooperate with probability based on cooperation ratio
- **Exploitation Protection**: Track individual players who consistently defect when others cooperate

**Detailed Logic**:
```pseudocode
Let prev_cooperators = number of players who played C in previous round
Let cooperation_ratio = prev_cooperators / n

If cooperation_ratio >= 0.5:
    Action = C
Else:
    // Forgiveness mechanism - give second chances
    If cooperation_ratio >= 0.3:
        Action = C with probability 0.7, D with probability 0.3
    Else if cooperation_ratio >= 0.1:
        Action = C with probability 0.3, D with probability 0.7
    Else:
        Action = D
```

### Round r (Final Round): Strategic Defection with Loyalty Check
- **Default**: Defect to maximize final payoff
- **Exception**: If cooperation ratio has been ≥ 0.8 for the last 3 rounds, cooperate to reward consistent group cooperation
- **Rationale**: In the final round, there's no future to consider, but reward exceptionally cooperative groups

```pseudocode
If last 3 rounds had cooperation_ratio >= 0.8:
    Action = C  // Reward exceptional group cooperation
Else:
    Action = D  // Standard final-round defection
```

## Key Features

### 1. **Generous Start**
- Always cooperates initially to signal good faith and attempt to establish cooperative norms

### 2. **Majority-Based Response**
- Uses the overall group behavior rather than individual tracking to avoid overly complex punishment schemes
- More stable than strategies that react to individual defectors

### 3. **Graduated Forgiveness**
- Doesn't immediately punish single-round defections
- Uses probabilistic cooperation when cooperation is low but not absent
- Prevents spiral into mutual defection from temporary setbacks

### 4. **Exploitation Resistance**
- Will defect when cooperation becomes very rare (< 10%)
- Protects against being the sole cooperator in a sea of defectors

### 5. **Final Round Optimization**
- Acknowledges the game theory reality of final-round incentives
- But rewards exceptionally cooperative groups with loyalty

## Strategic Reasoning

1. **Cooperative Foundation**: By starting with cooperation and maintaining it when reciprocated, the strategy encourages the emergence of cooperative equilibria.

2. **Resilience**: The forgiveness mechanism prevents temporary defections or mistakes from destroying long-term cooperation.

3. **Protection**: The strategy won't be exploited by persistent defectors, as it will eventually respond to very low cooperation rates.

4. **Simplicity**: Uses observable group behavior rather than complex individual tracking, making it more robust and predictable.

5. **Tournament Effectiveness**: This strategy should perform well against other cooperative strategies while protecting itself against purely selfish ones.

The strategy aims to achieve the mutual cooperation outcome (where all players get payoff k×r instead of r) while being robust enough to survive in a mixed population of strategies.
'''

description_COOPERATIVE_57 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to promote cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Core Logic:
```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

PARAMETERS:
- cooperation_threshold = 0.5 (50% of players must cooperate)
- forgiveness_probability = 0.1 (10% chance to cooperate after punishment)
- endgame_threshold = 3 (last 3 rounds)

INITIALIZE:
- punishment_mode = False
- punishment_rounds_remaining = 0
- consecutive_punishments = 0

FOR each round t:
    IF t == 1:  // First round
        RETURN C
    
    IF t > (total_rounds - endgame_threshold):  // Endgame
        RETURN endgame_strategy(t)
    
    IF punishment_mode:
        RETURN punishment_strategy()
    
    // Normal cooperation assessment
    last_round_cooperation_rate = count_cooperators_last_round() / n
    
    IF last_round_cooperation_rate >= cooperation_threshold:
        RETURN C
    ELSE:
        // Enter punishment mode
        punishment_mode = True
        punishment_rounds_remaining = 2
        consecutive_punishments += 1
        RETURN D
```

### Detailed Decision Functions:

```pseudocode
FUNCTION punishment_strategy():
    punishment_rounds_remaining -= 1
    
    IF punishment_rounds_remaining <= 0:
        punishment_mode = False
        // Forgiveness mechanism
        IF random() < forgiveness_probability:
            consecutive_punishments = 0
            RETURN C
        ELSE:
            RETURN D
    ELSE:
        RETURN D

FUNCTION endgame_strategy(round):
    rounds_left = total_rounds - round + 1
    
    IF rounds_left == 3:
        // Signal continued cooperation intent
        RETURN C
    ELSE IF rounds_left == 2:
        // Conditional cooperation
        last_round_cooperation_rate = count_cooperators_last_round() / n
        IF last_round_cooperation_rate >= 0.3:
            RETURN C
        ELSE:
            RETURN D
    ELSE:  // Final round
        // Defect in final round (standard game theory)
        RETURN D
```

## Strategy Rationale

### 1. **Cooperative Foundation**
- Starts with cooperation (C) in round 1 to signal cooperative intent
- Maintains cooperation when ≥50% of players cooperated in the previous round
- This creates a stable cooperative equilibrium when facing other cooperative strategies

### 2. **Punishment Mechanism**
- Triggers 2-round punishment when cooperation falls below 50%
- Multi-round punishment prevents exploitation by strategies that alternate between cooperation and defection
- Gradual escalation discourages persistent defection

### 3. **Forgiveness Component**
- 10% probability of returning to cooperation even after punishment periods
- Prevents permanent defection spirals
- Allows recovery from coordination failures or misunderstandings

### 4. **Endgame Handling**
- **Round r-2**: Signals continued cooperation to maintain trust
- **Round r-1**: Conditional cooperation based on reduced threshold (30%)
- **Round r**: Defects (rational response to end-game incentives)

### 5. **Robustness Features**
- **Threshold-based**: Uses population-level cooperation rates rather than individual tracking
- **Adaptive**: Responds to overall group dynamics
- **Resilient**: Can recover from temporary defection cascades

## Expected Performance

**Against Cooperative Strategies**: Maintains high mutual cooperation, achieving near-optimal payoffs.

**Against Mixed Strategies**: Promotes cooperation when possible while protecting against exploitation.

**Against Defective Strategies**: Limits losses through punishment while maintaining opportunities for cooperation recovery.

**In Heterogeneous Groups**: The threshold-based approach allows cooperation to emerge even when not all players are cooperative, as long as a critical mass cooperates.

This strategy embodies cooperative principles while remaining strategically sound in a competitive environment.
'''

description_COOPERATIVE_58 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances generosity to encourage cooperation with protective measures against persistent defectors.

## Decision Rules

### Round 1: Cooperative Start
- **Action: Always COOPERATE**
- **Rationale: Signal cooperative intent and attempt to establish a cooperative norm**

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = 0.6  // Require 60% cooperation rate to continue cooperating
forgiveness_probability = 0.1  // 10% chance to forgive even when threshold not met

total_cooperators_last_round = count_cooperators(previous_round)
cooperation_rate = total_cooperators_last_round / n

if cooperation_rate >= cooperation_threshold:
    return COOPERATE
else if cooperation_rate >= 0.3:  // Moderate cooperation exists
    if random() < forgiveness_probability:
        return COOPERATE  // Occasional forgiveness
    else:
        return DEFECT
else:  // Low cooperation (< 30%)
    return DEFECT
```

### Round r (Final Round): Conditional Cooperation
```pseudocode
// In final round, cooperate only if strong cooperation was maintained
recent_cooperation_rate = count_cooperators_last_3_rounds() / (3 * n)

if recent_cooperation_rate >= 0.7:
    return COOPERATE  // Reward sustained high cooperation
else:
    return DEFECT  // Protect against end-game defection
```

## Strategy Components

### 1. Cooperation Threshold (60%)
- Requires majority cooperation to continue cooperating
- Prevents exploitation by small groups of cooperators
- Accounts for the fact that with k < n, universal cooperation isn't strictly necessary for mutual benefit

### 2. Forgiveness Mechanism (10%)
- Occasional cooperation even when threshold isn't met
- Helps recover from temporary coordination failures
- Prevents permanent breakdown due to misunderstandings or errors

### 3. Graduated Response
- **High cooperation (≥60%)**: Always cooperate
- **Moderate cooperation (30-59%)**: Mostly defect with occasional forgiveness
- **Low cooperation (<30%)**: Always defect

### 4. End-Game Protection
- Recognizes that final round creates defection incentives
- Only cooperates in final round if recent cooperation was very high (≥70%)
- Protects against predictable end-game exploitation

## Edge Case Handling

### First Round
- Always cooperate to signal good intentions
- Essential for establishing cooperative equilibrium

### Last Round
- Conditional cooperation based on recent history
- Prevents exploitation while rewarding sustained cooperation

### All-Defect Situations
- Will defect when cooperation rate falls below 30%
- Maintains small chance of forgiveness to test for cooperation recovery

### High-Cooperation Situations
- Consistently cooperates to maintain beneficial equilibrium
- Reinforces cooperative norms

## Cooperative Alignment

This strategy is fundamentally cooperative because it:

1. **Initiates Cooperation**: Always starts by cooperating
2. **Rewards Cooperation**: Continues cooperating when others do
3. **Enables Recovery**: Includes forgiveness mechanism to restore cooperation
4. **Maximizes Group Welfare**: When cooperation threshold is met, contributes to public good
5. **Proportional Response**: Cooperation level matches observed cooperation from others

## Strategic Rationale

- **Against Other Cooperators**: Will maintain mutual cooperation, achieving high payoffs
- **Against Mixed Strategies**: Will adapt based on overall cooperation level
- **Against Defectors**: Will protect itself while leaving room for cooperation to emerge
- **Tournament Robust**: Performs well against diverse strategies without being exploitable

The strategy balances the cooperative goal of maximizing group welfare with the practical need to avoid exploitation in a competitive tournament setting.
'''

description_COOPERATIVE_59 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness"** that balances cooperation with protection against exploitation.

## Strategy Overview

This strategy starts cooperatively, reciprocates the group's behavior, but includes forgiveness mechanisms to recover from defection spirals and maintain long-term cooperation.

## Decision Rules

### Core Logic:
```pseudocode
GENEROUS_TIT_FOR_TAT_STRATEGY:
    
    // Initialize parameters
    cooperation_threshold = 0.5  // Minimum fraction of players cooperating to continue
    forgiveness_probability = 0.1  // Chance to cooperate even when group defects
    endgame_threshold = 3  // Rounds before end to switch to endgame strategy
    
    IF round == 1:
        RETURN C  // Always start cooperatively
    
    IF round > (total_rounds - endgame_threshold):
        RETURN endgame_strategy()
    
    // Calculate group cooperation rate from previous round
    cooperation_rate = (number_of_cooperators_last_round) / (n - 1)
    
    IF cooperation_rate >= cooperation_threshold:
        RETURN C  // Reciprocate cooperation
    
    ELSE:
        // Group defected, but sometimes forgive
        IF random() < forgiveness_probability:
            RETURN C  // Forgive and try to restart cooperation
        ELSE:
            RETURN D  // Reciprocate defection

ENDGAME_STRATEGY:
    // In final rounds, cooperate only if group strongly cooperates
    cooperation_rate = (number_of_cooperators_last_round) / (n - 1)
    
    IF cooperation_rate >= 0.7:  // Higher threshold for endgame
        RETURN C
    ELSE:
        RETURN D
```

## Detailed Behavior Specification

### First Round (t=1):
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish mutual cooperation

### Middle Rounds (2 ≤ t ≤ r-3):
- **Primary Rule**: Cooperate if at least 50% of other players cooperated in the previous round
- **Forgiveness Mechanism**: Even if the group defected, cooperate with 10% probability to break defection cycles
- **Rationale**: This balances reciprocity with opportunities for cooperation recovery

### Endgame Rounds (r-2 ≤ t ≤ r):
- **Stricter Threshold**: Only cooperate if at least 70% of others cooperated last round
- **Rationale**: Protect against endgame defection while still rewarding strong cooperative groups

## Key Features

### 1. **Cooperative Foundation**
- Starts with cooperation to signal good intentions
- Maintains cooperation when others reciprocate
- Lower threshold (50%) makes cooperation easier to sustain

### 2. **Forgiveness Mechanism**
- 10% chance to cooperate even after group defection
- Prevents permanent defection spirals
- Allows recovery from coordination failures or noise

### 3. **Adaptive Endgame**
- Recognizes that final rounds create defection incentives
- Higher cooperation threshold (70%) protects against exploitation
- Still rewards highly cooperative groups

### 4. **Exploitation Protection**
- Won't cooperate indefinitely against persistent defectors
- Reciprocates group defection most of the time
- Balances cooperation with self-protection

## Strategic Rationale

This strategy is designed to:

1. **Initiate Cooperation**: Start cooperatively to establish mutual benefit
2. **Sustain Cooperation**: Use a reasonable threshold that doesn't require unanimous cooperation
3. **Recover from Mistakes**: Forgiveness prevents accidental defection cascades
4. **Adapt to Context**: Different behavior in endgame reflects changed incentives
5. **Resist Exploitation**: Won't be a pure cooperator that can be easily exploited

The strategy assumes other AI strategies will be designed with some level of sophistication and may also attempt cooperation, making mutual cooperation achievable while maintaining protection against purely selfish strategies.
'''

description_COOPERATIVE_60 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Gradual Forgiveness" (GTTGF)**.

## Strategy Overview

This strategy balances cooperation with protection against exploitation, while maintaining a cooperative orientation that can build and sustain mutual cooperation over multiple rounds.

## Decision Rules

### Core Logic:
```pseudocode
STRATEGY: Generous Tit-for-Tat with Gradual Forgiveness (GTTGF)

PARAMETERS:
- cooperation_threshold = 0.5  // Fraction of players needed cooperating
- forgiveness_patience = 3     // Rounds to wait before forgiving
- generosity_probability = 0.2 // Chance to cooperate despite defections

STATE VARIABLES:
- punishment_timer = 0
- last_cooperation_rate = 1.0
- consecutive_low_cooperation = 0

FOR EACH ROUND t:
  IF t == 1:
    ACTION = C  // Always cooperate first round
    
  ELSE IF punishment_timer > 0:
    // In punishment phase
    punishment_timer -= 1
    IF random() < generosity_probability:
      ACTION = C
    ELSE:
      ACTION = D
      
  ELSE:
    // Normal decision phase
    cooperation_rate = (number of C actions in round t-1) / n
    
    IF cooperation_rate >= cooperation_threshold:
      ACTION = C  // Reward good cooperation
      consecutive_low_cooperation = 0
      
    ELSE:
      // Low cooperation detected
      consecutive_low_cooperation += 1
      
      IF consecutive_low_cooperation >= 2:
        // Trigger punishment
        punishment_timer = forgiveness_patience
        ACTION = D
      ELSE:
        // Give one more chance
        ACTION = C
```

## Detailed Strategy Components

### 1. First Round Behavior
- **Always cooperate** in round 1 to signal cooperative intent and give the group the best chance to establish a cooperative equilibrium.

### 2. Cooperation Threshold Decision
- Cooperate when ≥50% of players cooperated in the previous round
- This threshold balances:
  - Rewarding partial cooperation (not requiring unanimity)
  - Avoiding exploitation when cooperation is too low
  - Encouraging marginal players to join cooperative coalitions

### 3. Punishment Mechanism
- Trigger punishment only after **two consecutive rounds** of low cooperation (< 50%)
- This prevents overreaction to single-round fluctuations
- Punishment lasts for 3 rounds, providing clear consequences

### 4. Generosity Component
- Even during punishment, cooperate with 20% probability
- This prevents permanent breakdown and signals continued willingness to cooperate
- Helps restart cooperation cycles

### 5. Last Round Handling
```pseudocode
IF t == r:  // Final round
  IF cooperation_rate_previous >= cooperation_threshold:
    ACTION = C  // Maintain cooperation to the end
  ELSE:
    ACTION = D  // No future to build toward
```

## Strategic Rationale

### Cooperative Elements:
1. **Default to cooperation** when others are cooperative
2. **Patient approach** - gives two chances before punishing
3. **Generous forgiveness** - includes randomized cooperation even during punishment
4. **Builds on success** - strongly rewards high cooperation rates

### Protection Against Exploitation:
1. **Clear consequences** for persistent defection
2. **Graduated response** - doesn't immediately escalate to full punishment
3. **Time-limited punishment** prevents permanent retaliation cycles

### Adaptability:
- Responds to actual behavior rather than assumptions about opponent types
- Can rebuild cooperation after punishment phases
- Handles varying group sizes through percentage-based thresholds

## Expected Tournament Performance

This strategy should perform well against:
- **Other cooperative strategies** - mutual cooperation from early rounds
- **Tit-for-tat variants** - similar logic creates stable cooperation
- **Mixed populations** - can form cooperative coalitions with willing players
- **Exploitative strategies** - punishment phases limit exploitation while generosity allows recovery

The strategy maintains strong cooperative intentions while including necessary defensive mechanisms for a competitive tournament environment.
'''

description_COOPERATIVE_61 = '''
I'll design a cooperative strategy called **"Graduated Reciprocal Cooperation"** that balances cooperative intent with strategic adaptation to opponents' behavior.

## Strategy: Graduated Reciprocal Cooperation (GRC)

### Core Philosophy
Start cooperative, maintain cooperation when others reciprocate, but gradually adapt defection levels to match the group's cooperation rate while still maintaining a cooperative bias.

### Decision Rules

```pseudocode
STRATEGY: Graduated Reciprocal Cooperation

INITIALIZE:
- cooperation_threshold = 0.4  // Minimum group cooperation rate to maintain full cooperation
- reciprocity_factor = 0.8     // How much to match opponents' cooperation level
- forgiveness_rounds = 2       // Rounds to wait before adjusting to sustained changes

ROUND 1:
- Action: COOPERATE (always start cooperatively)

ROUNDS 2 to r-1:
1. Calculate group_cooperation_rate = (total_cooperators_last_round) / (n-1)
2. Calculate recent_cooperation_rate = average cooperation rate over last min(3, current_round-1) rounds
3. 
4. IF recent_cooperation_rate >= cooperation_threshold:
   - Action: COOPERATE
5. ELSE:
   - adjusted_cooperation_prob = max(0.3, recent_cooperation_rate * reciprocity_factor)
   - Action: COOPERATE with probability adjusted_cooperation_prob, otherwise DEFECT

ROUND r (final round):
1. Calculate recent_cooperation_rate as above
2. IF recent_cooperation_rate >= 0.6:
   - Action: COOPERATE (reward consistent cooperators)
3. ELSE:
   - Action: DEFECT (protect against end-game defection)
```

### Detailed Strategy Components

#### 1. **Cooperative Start**
- Always cooperate in Round 1 to signal cooperative intent
- This establishes a cooperative baseline and gives other cooperative strategies a chance to recognize each other

#### 2. **Adaptive Reciprocity (Rounds 2 to r-1)**
- Monitor the group's cooperation rate over recent rounds (last 3 rounds or available history)
- If group cooperation rate ≥ 40%, maintain full cooperation
- If group cooperation rate < 40%, partially match their level but maintain cooperative bias:
  - Cooperation probability = max(30%, group_rate × 0.8)
  - This ensures we never become fully exploitative while protecting against severe exploitation

#### 3. **Final Round Strategy**
- If recent cooperation has been high (≥ 60%), cooperate to reward good partners
- Otherwise, defect to protect against end-game exploitation
- This balances cooperative spirit with rational self-protection

### Edge Case Handling

#### **Early Rounds (Rounds 2-3)**
- Use available history only (don't assume missing data)
- Maintain cooperative bias when data is limited

#### **High Variance in Cooperation**
- Use 3-round moving average to smooth out temporary fluctuations
- Prevents overreaction to single-round anomalies

#### **All-Defector Environment**
- Strategy floor of 30% cooperation probability prevents complete defection
- Maintains some cooperative signaling even in hostile environments

#### **All-Cooperator Environment**
- Strategy maintains full cooperation when others cooperate consistently
- Rewards and reinforces cooperative equilibria

### Strategic Rationale

1. **Cooperative Alignment**: Always starts cooperative and maintains cooperative bias throughout
2. **Exploitation Protection**: Adapts to persistent defection while maintaining some cooperation
3. **Mutual Cooperation Reward**: Fully cooperates when others do, supporting efficient outcomes
4. **Forgiveness**: Doesn't permanently punish temporary defections
5. **End-Game Awareness**: Protects against final-round exploitation while rewarding consistent cooperators

This strategy aims to foster cooperation while being resilient against exploitation, making it effective in mixed populations of cooperative and strategic players.
'''

description_COOPERATIVE_62 = '''
# Cooperative Strategy: "Graduated Reciprocation with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to defection and allowing for recovery from coordination failures. It balances optimism with pragmatic responses to betrayal.

## Decision Rules

### Round 1: Cooperative Start
- **Always COOPERATE** in the first round
- Rationale: Signal cooperative intent and give the group the best chance to establish a high-cooperation equilibrium

### Rounds 2 to r-1: Adaptive Reciprocation

**Primary Rule: Majority Threshold with Forgiveness**
```
If (cooperators_last_round / n) >= 0.5:
    COOPERATE
Else if (cooperators_last_round / n) >= 0.3 AND my_last_action == C:
    COOPERATE  // Give benefit of doubt if I was cooperative
Else if (consecutive_low_cooperation_rounds >= 3):
    DEFECT     // Protect against persistent exploitation
Else:
    COOPERATE  // Default to forgiveness
```

**Forgiveness Mechanism:**
- Track `consecutive_low_cooperation_rounds` (rounds where < 50% cooperated)
- Reset counter to 0 whenever cooperation rate ≥ 50%
- This prevents permanent punishment spirals

### Final Round (Round r): Conditional Cooperation
```
If (average_cooperation_rate_last_3_rounds >= 0.4):
    COOPERATE  // Reward sustained cooperation attempts
Else:
    DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Graduated Response
- **High cooperation (≥50%)**: Always cooperate
- **Medium cooperation (30-49%)**: Cooperate if I was cooperative last round
- **Low cooperation (<30%)**: Forgive for up to 3 consecutive rounds, then defect

### 2. Forgiveness Buffer
- Allows for 2-3 rounds of recovery after cooperation breakdowns
- Prevents permanent defection spirals that destroy group welfare
- Resets punishment when cooperation recovers

### 3. End-Game Protection
- Uses recent history rather than single-round data for final decision
- Balances cooperative ideals with protection against exploitation

## Strategic Rationale

### Why This Approach?
1. **Cooperative Signal**: Starting with cooperation and maintaining high forgiveness signals cooperative intent
2. **Exploitation Protection**: The 3-round patience limit prevents indefinite exploitation
3. **Recovery Friendly**: Graduated thresholds allow groups to rebuild cooperation after failures
4. **Robust to Mistakes**: Doesn't immediately punish single-round coordination failures

### Parameter Adaptation
- **50% threshold**: Works well across different group sizes (maintains meaning whether n=3 or n=20)
- **30% forgiveness threshold**: Allows cooperation even when minority, encouraging recovery
- **3-round patience**: Balances forgiveness with self-protection

### Expected Performance
- **Against other cooperators**: Maintains mutual cooperation
- **Against mixed strategies**: Encourages cooperation while protecting against exploitation
- **Against defectors**: Eventually protects self while remaining open to cooperation signals
- **In noisy environments**: Forgiveness prevents cascading punishment from miscoordination

This strategy prioritizes group welfare while maintaining individual rationality, making it both genuinely cooperative and competitively viable.
'''

description_COOPERATIVE_63 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation by balancing cooperation with strategic defection when necessary.

## Decision Rules

### Round 1 (Initialization)
- **Action: COOPERATE**
- Rationale: Start optimistically to signal cooperative intent and attempt to establish a cooperative equilibrium from the beginning.

### Rounds 2 to r-1 (Main Strategy)
Use a **majority-based conditional cooperation** approach:

```pseudocode
if round_number == 1:
    return COOPERATE

cooperation_rate = count_cooperators_last_round / n

if cooperation_rate >= 0.5:
    return COOPERATE
else:
    if my_last_action == COOPERATE and cooperation_rate < 0.3:
        return DEFECT  // Punish severe defection
    else:
        return COOPERATE  // Forgive and try to rebuild cooperation
```

### Final Round (r)
- **Action: COOPERATE**
- Rationale: Even though there's no future to influence, cooperating on the last round signals consistent cooperative values and avoids the "end-game effect" that could undermine cooperation in earlier rounds.

## Detailed Strategy Logic

### Cooperation Threshold
- **Cooperate** when ≥50% of players cooperated in the previous round
- This follows the principle that cooperation should be maintained when it's the majority behavior

### Punishment Mechanism
- **Defect** only when:
  1. I cooperated last round (showing I'm not just a free rider)
  2. AND cooperation rate fell below 30% (severe breakdown)
- This creates a credible threat against exploitation while remaining forgiving

### Forgiveness Element
- After punishing (defecting), immediately return to cooperation in the next round
- This prevents destructive cycles of mutual punishment and helps rebuild cooperative norms

## Edge Case Handling

### Missing Information
- If historical data is incomplete, default to **COOPERATE**

### Tie Situations
- When exactly 50% cooperated last round, choose **COOPERATE** (optimistic tie-breaking)

### First Few Rounds
- Maintain cooperation for at least the first 2 rounds regardless of others' actions to establish cooperative intent

## Strategic Rationale

1. **Collective Welfare Focus**: Since k > 1, total group payoff is maximized when everyone cooperates
2. **Exploitation Protection**: The punishment mechanism deters systematic free-riding
3. **Cooperation Rebuilding**: The forgiveness element prevents permanent breakdown
4. **Clear Signaling**: Consistent rules make the strategy predictable to other cooperative players
5. **Robustness**: Works across different values of n and k within the specified constraints

## Expected Performance

This strategy should perform well against:
- Other cooperative strategies (mutual cooperation)
- Mixed populations (encourages cooperation while punishing defection)
- Adaptive strategies (provides clear behavioral patterns to learn from)

The strategy balances the cooperative imperative with practical considerations for a tournament environment where some opponents may attempt exploitation.
'''

description_COOPERATIVE_64 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through measured responses to defection.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Detailed Logic**:
```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round >= 0.5:
    action = C
else:
    // Defection response with forgiveness mechanism
    consecutive_low_cooperation_rounds = count_consecutive_rounds_with_cooperation_rate_below_50%
    
    if consecutive_low_cooperation_rounds <= 2:
        action = C  // Forgive up to 2 consecutive rounds of low cooperation
    else:
        action = D  // Punish persistent non-cooperation
endif
```

### Final Round (Round r): Conditional Cooperation
- **If cooperation rate ≥ 50% in round r-1**: Cooperate (C)
- **If cooperation rate < 50% in round r-1**: Defect (D)
- **Rationale**: Maintain cooperative stance if group has been cooperative, but protect against end-game exploitation

## Key Features

### 1. Generous Threshold (50% Rule)
- Cooperates as long as at least half the group cooperated in the previous round
- This is generous because even with some defectors, we continue contributing to the public good
- Accounts for the fact that partial cooperation still generates positive returns due to the multiplication factor k

### 2. Forgiveness Mechanism
- Forgives up to 2 consecutive rounds of low cooperation (cooperation rate < 50%)
- Prevents spiral into mutual defection due to temporary coordination failures or noise
- Allows recovery from brief periods of mistrust

### 3. Graduated Response
- Doesn't immediately punish single instances of high defection
- Only switches to defection after persistent evidence of non-cooperation (3+ consecutive rounds below 50% cooperation)

### 4. Strategic Final Round
- Maintains cooperation in final round if group has been cooperative
- Protects against exploitation if group has been consistently uncooperative

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative norm and signal good intentions

### Information Scarcity (Early Rounds)
- Round 1: Cooperate unconditionally
- Round 2+: Use available history even if limited

### Tie-Breaking
- If cooperation rate is exactly 50%, treat as meeting the threshold (cooperate)

### All-Defection Scenarios
- After 3+ consecutive rounds of 0% cooperation, switch to defection
- Can recover to cooperation if cooperation rate rises above 50% in any subsequent round

## Strategic Rationale

1. **Cooperative Leadership**: Opens cooperatively to establish positive momentum
2. **Collective Rationality**: Recognizes that mutual cooperation is Pareto optimal
3. **Resilience**: Forgiveness mechanism prevents permanent breakdown of cooperation
4. **Proportional Response**: Response severity matches the persistence of non-cooperative behavior
5. **Adaptability**: Can shift between cooperation and punishment based on group behavior
6. **End-Game Awareness**: Balances continued cooperation with protection against final-round exploitation

This strategy aims to maximize collective welfare while maintaining individual rationality, making it well-suited for a tournament environment where the goal is to achieve high absolute payoffs through successful cooperation.
'''

description_COOPERATIVE_65 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being robust against exploitation and occasional defections. It balances cooperation with strategic defection to encourage others to cooperate.

## Decision Rules

### Core Logic:
1. **Start Cooperative**: Always cooperate in round 1
2. **Mirror Majority with Generosity**: In subsequent rounds, cooperate if the majority of players cooperated in the previous round, but with built-in forgiveness
3. **Gradual Punishment**: If cooperation breaks down, implement measured retaliation rather than permanent defection
4. **End-Game Cooperation**: Maintain cooperation even in final rounds to signal long-term cooperative intent

### Detailed Strategy:

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

INITIALIZE:
- forgiveness_counter = 0
- punishment_phase = false
- consecutive_defections = 0

FOR each round t:
    IF round == 1:
        RETURN Cooperate
    
    ELSE:
        // Calculate cooperation rate in previous round
        cooperation_rate = (number of cooperators in round t-1) / n
        
        // Check if we're in punishment phase
        IF punishment_phase:
            consecutive_defections += 1
            IF consecutive_defections >= 2 OR cooperation_rate >= 0.6:
                punishment_phase = false
                consecutive_defections = 0
                RETURN Cooperate
            ELSE:
                RETURN Defect
        
        // Normal decision logic
        IF cooperation_rate >= 0.5:  // Majority cooperated
            RETURN Cooperate
            
        ELSE IF cooperation_rate >= 0.3:  // Significant minority cooperated
            // Be generous - cooperate with some probability
            IF forgiveness_counter < 2:
                forgiveness_counter += 1
                RETURN Cooperate
            ELSE:
                forgiveness_counter = 0
                punishment_phase = true
                consecutive_defections = 0
                RETURN Defect
                
        ELSE:  // Low cooperation (< 30%)
            punishment_phase = true
            consecutive_defections = 0
            RETURN Defect
```

## Strategy Components Explained

### 1. **Generous Start**
- Always cooperate in round 1 to signal cooperative intent
- This establishes a cooperative baseline

### 2. **Majority-Based Response**
- If ≥50% of players cooperated last round → Cooperate
- This rewards group cooperation and maintains momentum

### 3. **Forgiveness Mechanism**
- When 30-49% cooperated (borderline cases), give up to 2 "free passes"
- This prevents accidental escalation from temporary defections
- Helps maintain cooperation when group is on the fence

### 4. **Measured Punishment**
- When cooperation drops below 30%, enter punishment phase
- Defect for at most 2 consecutive rounds or until cooperation recovers to 60%
- This signals that exploitation won't be tolerated while leaving door open for reconciliation

### 5. **No End-Game Defection**
- Continue cooperative behavior even in final rounds
- This signals genuine cooperative intent rather than strategic manipulation

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative norm

### Last Round
- Continue normal strategy (no special end-game defection)
- Maintains reputation for future interactions if tournament structure repeats

### All Players Defect Scenario
- Enter punishment phase but limit to 2 rounds maximum
- Then return to cooperation to test if others will follow

### High Cooperation Scenario
- Continue cooperating to maintain the beneficial equilibrium

## Cooperative Alignment

This strategy is genuinely cooperative because:

1. **Default to Cooperation**: The baseline assumption is to cooperate
2. **Forgiveness**: Built-in mechanisms to overlook temporary defections
3. **Proportional Response**: Punishment is limited and conditional
4. **Recovery Focus**: Actively looks for opportunities to return to cooperation
5. **No Exploitation**: Doesn't take advantage of others' cooperation without reciprocating

The strategy aims to create a stable cooperative environment while protecting against systematic exploitation, making it both genuinely cooperative and strategically sound.
'''

description_COOPERATIVE_66 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness" (GTF)

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Cooperative Opening
- **Always cooperate** in the first round to signal cooperative intent

### Rounds 2 to r-1: Adaptive Response
```pseudocode
cooperation_threshold = 0.5  // 50% of players must cooperate
forgiveness_probability = 0.1  // 10% chance to forgive after punishment

if previous_round_cooperation_rate >= cooperation_threshold:
    cooperate()
else if last_action_was_punishment:
    if random() < forgiveness_probability:
        cooperate()  // Occasional forgiveness
    else:
        defect()  // Continue punishment
else:
    defect()  // Begin punishment phase
    mark_as_punishment_phase()
```

### Round r (Final Round): Conditional Cooperation
```pseudocode
// In final round, cooperate only if recent cooperation has been high
recent_rounds = min(3, current_round - 1)
recent_cooperation_rate = count_cooperators_in_last_n_rounds(recent_rounds) / (n * recent_rounds)

if recent_cooperation_rate >= 0.6:
    cooperate()  // Reward consistent cooperators
else:
    defect()  // Protect against end-game defection
```

## Strategy Components

### 1. Cooperation Threshold (50%)
- Cooperate when at least half the players cooperated in the previous round
- This threshold is lenient enough to maintain cooperation even with some free-riders
- Accounts for the fact that with k < n, some defection can still yield positive returns for cooperators

### 2. Punishment Mechanism
- When cooperation falls below threshold, switch to defection
- This punishes mass defection while not overreacting to isolated defectors
- Punishment continues until cooperation recovers

### 3. Forgiveness Element
- 10% probability of returning to cooperation even during punishment phase
- Prevents permanent breakdown of cooperation due to coordination failures
- Allows recovery from temporary downturns in cooperation

### 4. Final Round Protection
- Higher cooperation threshold (60%) required in final round
- Protects against predictable end-game defection
- Only cooperates if there's strong evidence of sustained cooperation

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative norm
- Signals trustworthiness and cooperative intent

### Last Round
- Conditional cooperation based on recent history
- Prevents exploitation while rewarding consistent cooperators

### All Players Defect Scenario
- Strategy will defect in response
- Occasional forgiveness attempts (10%) allow for recovery
- Will immediately return to cooperation if others do

### Mixed Strategy Opponents
- Responds to aggregate behavior rather than individual actions
- Threshold-based approach handles noisy or mixed strategies well

## Rationale

This strategy is designed to:

1. **Initiate Cooperation**: Start cooperatively to establish good faith
2. **Maintain Cooperation**: Continue cooperating when others do the same
3. **Punish Defection**: Respond to mass defection with temporary punishment
4. **Enable Recovery**: Allow cooperation to resume through forgiveness mechanism
5. **Protect Against Exploitation**: Guard against end-game and systematic exploitation

The 50% threshold strikes a balance between being too lenient (allowing exploitation) and too strict (causing cooperation breakdown). The forgiveness mechanism prevents permanent deadlocks while the final-round protection guards against predictable defection patterns.

This strategy should perform well against other cooperative strategies while having reasonable defenses against exploitative ones.
'''

description_COOPERATIVE_67 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances optimism about cooperation with protection against persistent defectors.

## Decision Rules

### Round 1: Optimistic Start
**Always COOPERATE** in the first round to signal cooperative intent and give the group the best chance at establishing mutual cooperation.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
**COOPERATE if:**
- The cooperation rate in the previous round was ≥ 50% (i.e., at least ⌈n/2⌉ players cooperated)

**DEFECT if:**
- The cooperation rate in the previous round was < 50%
- BUT: Implement forgiveness by returning to cooperation if defection rate improves

### Round r (Final Round): Conditional Loyalty
**COOPERATE if:**
- The cooperation rate in round r-1 was ≥ 60% 
- This higher threshold accounts for end-game defection incentives while rewarding consistently cooperative groups

**DEFECT if:**
- The cooperation rate in round r-1 was < 60%

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    previous_round = history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / n
    
    if round_number == r:  // Final round
        threshold = 0.6
    else:
        threshold = 0.5
    
    if cooperation_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

## Edge Case Handling

1. **First Round**: Always cooperate to establish cooperative norms
2. **Final Round**: Use higher cooperation threshold (60%) to account for end-game effects while still rewarding cooperative groups
3. **All-Defect Scenarios**: Will defect in response but immediately returns to cooperation if others show any improvement
4. **Mixed Cooperation**: The 50% threshold provides clear, predictable responses that other cooperative strategies can learn and adapt to

## Strategic Rationale

### Cooperative Alignment
- **Starts optimistically** to signal cooperative intent
- **Rewards group cooperation** with continued cooperation
- **Provides clear feedback** that encourages others toward cooperation
- **Forgives quickly** when cooperation levels improve

### Robustness Features
- **Not exploitable** by pure defectors (responds to low cooperation with defection)
- **Clear thresholds** make the strategy predictable for other cooperators to coordinate with
- **Balanced final round** - maintains cooperation incentive while acknowledging end-game dynamics

### Tournament Effectiveness
Given that other strategies are also designed to be cooperative:
- The 50% threshold allows coordination with various cooperative approaches
- Quick forgiveness helps establish mutual cooperation with other conditional cooperators
- Clear, simple rules make it easier for other algorithmic strategies to predict and coordinate with

This strategy should perform well in a tournament of cooperative strategies while maintaining protection against exploitation.
'''

description_COOPERATIVE_68 = '''
# Generous Tit-for-Tat with Forgiveness (GTTF)

## Strategy Overview
This strategy balances cooperation with protection against exploitation by using a generous reciprocity approach that forgives occasional defections and gradually builds trust.

## Core Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

PARAMETERS:
- cooperation_threshold = 0.5  // Minimum fraction of others cooperating to continue
- forgiveness_probability = 0.1  // Chance to cooperate despite recent defection
- endgame_threshold = 3  // Rounds before end to start defecting

INITIALIZE:
- round = 1
- cooperation_history = []  // Track others' cooperation rates
- consecutive_exploitations = 0  // Track being sole cooperator

FOR each round t:
    IF t == 1:
        action = COOPERATE  // Start cooperatively
    
    ELSE IF t > (total_rounds - endgame_threshold):
        // Endgame: Defect to avoid final exploitation
        action = DEFECT
    
    ELSE:
        // Calculate cooperation rate of others in previous round
        others_cooperation_rate = count_cooperators_last_round() / (n-1)
        
        // Check if I was exploited (only cooperator or minimal cooperation)
        IF my_last_action == COOPERATE AND others_cooperation_rate < 0.3:
            consecutive_exploitations += 1
        ELSE:
            consecutive_exploitations = 0
        
        // Main decision logic
        IF consecutive_exploitations >= 2:
            // Punish sustained exploitation
            IF random() < forgiveness_probability:
                action = COOPERATE  // Occasional forgiveness
            ELSE:
                action = DEFECT
        
        ELSE IF others_cooperation_rate >= cooperation_threshold:
            // Reciprocate high cooperation
            action = COOPERATE
        
        ELSE IF others_cooperation_rate >= 0.3:
            // Mixed cooperation - be generous but cautious
            IF random() < 0.7:
                action = COOPERATE
            ELSE:
                action = DEFECT
        
        ELSE:
            // Low cooperation environment - mostly defect
            IF random() < forgiveness_probability:
                action = COOPERATE  // Small chance to restart cooperation
            ELSE:
                action = DEFECT
    
    RETURN action
```

## Key Features

### 1. **Cooperative Start**
- Always cooperate in round 1 to signal willingness to cooperate
- Gives other cooperative strategies a chance to establish mutual cooperation

### 2. **Adaptive Reciprocity**
- Responds to the **cooperation rate** of other players, not just individual actions
- Maintains cooperation when ≥50% of others cooperate
- Shows some tolerance for mixed cooperation (30-50% range)

### 3. **Exploitation Protection**
- Tracks consecutive rounds of being exploited (cooperating alone or with minimal support)
- After 2+ consecutive exploitations, switches to primarily defecting
- Prevents being consistently taken advantage of

### 4. **Generous Forgiveness**
- 10% chance to cooperate even when punishing or in low-cooperation environments
- Allows recovery from mutual defection spirals
- Provides opportunities to restart cooperative relationships

### 5. **Endgame Awareness**
- Defects in final 3 rounds to avoid exploitation when future reciprocity is impossible
- Balances cooperative goals with rational self-interest

## Strategic Rationale

**Against Other Cooperative Strategies**: Quickly establishes and maintains mutual cooperation, maximizing joint payoffs.

**Against Exploitative Strategies**: Initially attempts cooperation but adapts to defect when consistently exploited, minimizing losses.

**Against Mixed Strategies**: Responds proportionally to cooperation levels, encouraging more cooperation through selective reciprocity.

**In Multi-Player Dynamics**: Focuses on overall group cooperation rather than individual player tracking, making it robust in larger groups.

This strategy embodies cooperative principles while maintaining enough defensive mechanisms to avoid exploitation, making it well-suited for a tournament against diverse opponent strategies.
'''

description_COOPERATIVE_69 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Collective Threshold"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibrium while being robust against exploitation. It balances generous cooperation with strategic defection to encourage group-wide cooperation.

## Strategy Description

### Decision Rules

**Round 1: Always Cooperate**
- Start with cooperation to signal cooperative intent
- This establishes a positive baseline for reciprocity

**Rounds 2 to r-1: Conditional Cooperation with Forgiveness**
```
if (cooperation_rate_last_round >= threshold):
    action = COOPERATE
else if (cooperation_rate_last_round >= forgiveness_threshold AND random() < forgiveness_probability):
    action = COOPERATE  // Generous forgiveness
else:
    action = DEFECT     // Punish low cooperation
```

**Round r (Final): Generous Cooperation**
- Cooperate if cooperation rate in round r-1 was ≥ 30%
- This prevents end-game defection cascade while not being exploitable

### Threshold Calculations

**Primary Threshold**: `threshold = max(0.5, (k-1)/(n-1))`
- Cooperate if at least this fraction cooperated last round
- The formula ensures cooperation is profitable when others reciprocate
- Minimum 50% prevents exploitation by small groups

**Forgiveness Threshold**: `forgiveness_threshold = 0.3`
- Even with low cooperation, occasionally cooperate to restart cooperation

**Forgiveness Probability**: `0.2`
- 20% chance to cooperate even when cooperation rate is between 30-50%

## Detailed Logic

### Round-by-Round Behavior

1. **First Round**: Always cooperate to establish cooperative norm

2. **Middle Rounds (2 to r-1)**:
   - **High Cooperation (≥threshold)**: Cooperate to maintain momentum
   - **Medium Cooperation (30% to <threshold)**: Cooperate 20% of the time (forgiveness)
   - **Low Cooperation (<30%)**: Defect to avoid exploitation

3. **Last Round**: 
   - Cooperate if previous round had ≥30% cooperation
   - Prevents end-game unraveling while maintaining some cooperation

### Edge Case Handling

**Small Groups (n=2,3)**:
- Threshold becomes more lenient (closer to 50%)
- Higher forgiveness probability (0.3) to restart cooperation

**High Multiplication Factor (k close to n)**:
- Threshold becomes more demanding
- Strong incentive for universal cooperation

**Single Defector Scenario**:
- If n-1 players cooperated last round, still cooperate
- Gives defectors chance to return to cooperation

## Strategic Rationale

### Why This Works

1. **Establishes Cooperation**: Starting with cooperation and maintaining it when others reciprocate
2. **Punishes Exploitation**: Defects when cooperation drops too low
3. **Enables Recovery**: Forgiveness mechanism prevents permanent defection spirals
4. **Endgame Stability**: Final round cooperation prevents cascading defection
5. **Adaptive Thresholds**: Adjusts expectations based on group size and incentive structure

### Robustness Features

- **Against Always Defect**: Learns to defect after initial cooperation attempt
- **Against Conditional Cooperators**: Maintains mutual cooperation
- **Against Exploiters**: Punishes but provides path back to cooperation
- **Against End-Game Defection**: Final round cooperation maintains some collective benefit

## Pseudocode Summary

```python
def decide_action(round_num, history, n, k, r):
    if round_num == 1:
        return COOPERATE
    
    last_round_coop_rate = count_cooperators(history[-1]) / n
    threshold = max(0.5, (k-1)/(n-1))
    
    if round_num == r:  # Final round
        return COOPERATE if last_round_coop_rate >= 0.3 else DEFECT
    
    # Middle rounds
    if last_round_coop_rate >= threshold:
        return COOPERATE
    elif last_round_coop_rate >= 0.3 and random() < 0.2:
        return COOPERATE  # Forgiveness
    else:
        return DEFECT
```

This strategy maximizes long-term collective welfare while protecting against exploitation through strategic punishment and generous forgiveness.
'''

description_COOPERATIVE_70 = '''
# Adaptive Cooperative Strategy: "Generous Tit-for-Tat with Graduated Sanctions"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibria while being resilient to exploitation and defection cascades. It balances forgiveness with accountability through graduated responses.

## Strategy Components

### 1. Decision Rules

**Primary Rule: Cooperation Threshold**
- Cooperate if the cooperation rate in the previous round ≥ threshold
- Threshold starts at 50% and adapts based on game dynamics

**Threshold Adaptation:**
```pseudocode
if previous_round_cooperation_rate >= current_threshold:
    threshold = max(threshold - 0.05, 0.3)  // Become more trusting
else:
    threshold = min(threshold + 0.1, 0.8)   // Become more demanding
```

### 2. Edge Case Handling

**First Round:** Always COOPERATE
- Establishes cooperative intent
- Creates opportunity for mutual cooperation

**Last Round:** 
- If cooperation_rate_last_3_rounds >= 0.6: COOPERATE
- Else: DEFECT
- Prevents exploitation while rewarding sustained cooperation

**Early Rounds (rounds 2-3):**
- COOPERATE if ≥ 40% cooperated in previous round
- More forgiving threshold to allow cooperation to emerge

### 3. Forgiveness Mechanism

**Forgiveness Counter:**
- Track consecutive rounds of low cooperation (< 30%)
- After 2 consecutive low-cooperation rounds, attempt reconciliation:
  - COOPERATE once regardless of threshold
  - Reset counter if cooperation rate improves to ≥ 50%

### 4. Complete Strategy Pseudocode

```pseudocode
Strategy: GenerousGraduatedTFT

Initialize:
    threshold = 0.5
    forgiveness_counter = 0
    round_number = 1

For each round t:
    if t == 1:
        action = COOPERATE
    
    else if t == final_round:
        recent_coop_rate = cooperation_rate_last_3_rounds()
        action = COOPERATE if recent_coop_rate >= 0.6 else DEFECT
    
    else:
        prev_coop_rate = cooperation_rate(t-1)
        
        // Forgiveness mechanism
        if prev_coop_rate < 0.3:
            forgiveness_counter += 1
        else:
            forgiveness_counter = 0
            
        if forgiveness_counter == 2:
            action = COOPERATE  // Forgiveness attempt
            forgiveness_counter = 0
        
        // Standard threshold decision
        else if t <= 3:
            action = COOPERATE if prev_coop_rate >= 0.4 else DEFECT
        else:
            action = COOPERATE if prev_coop_rate >= threshold else DEFECT
        
        // Update threshold
        if prev_coop_rate >= threshold:
            threshold = max(threshold - 0.05, 0.3)
        else:
            threshold = min(threshold + 0.1, 0.8)

    round_number += 1
    return action
```

## Strategic Rationale

### Cooperative Alignment
1. **Starts cooperatively** to signal good intentions
2. **Rewards cooperation** by lowering threshold when others cooperate
3. **Attempts reconciliation** through forgiveness mechanism
4. **Maintains cooperation** in endgame when others have been cooperative

### Robustness Features
1. **Graduated sanctions**: Gradually increases demands rather than immediate punishment
2. **Adaptive threshold**: Becomes more/less trusting based on group behavior
3. **Forgiveness mechanism**: Breaks potential defection spirals
4. **Context-sensitive endgame**: Cooperates with cooperative groups, protects against exploitation

### Expected Performance
- **Against other cooperators**: Establishes high cooperation quickly, maintains it
- **Against mixed strategies**: Adapts threshold to find sustainable cooperation level
- **Against defectors**: Protects against exploitation while leaving room for cooperation to emerge
- **In tournaments**: Performs well with other cooperative strategies while avoiding exploitation

This strategy should perform well in a tournament of LLM-generated strategies, as it's designed to work with other reasonable approaches while protecting against purely selfish strategies.
'''

description_COOPERATIVE_71 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibrium while being resilient to occasional defections and adaptive to the group's cooperative tendencies.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the start.

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness
```pseudocode
if round == 2:
    if majority_cooperated_last_round():
        return C
    else:
        return D  // Brief punishment for non-cooperative start
else:
    cooperation_rate = count_cooperators_last_round() / n
    
    if cooperation_rate >= 0.5:
        return C  // Follow majority cooperation
    elif cooperation_rate >= 0.3:
        // Forgiveness mechanism: occasionally cooperate to test waters
        if (round % 3 == 0) or (personal_cooperation_streak >= 2):
            return C
        else:
            return D
    else:
        // Low cooperation environment - minimal cooperation
        if cooperation_rate > 0 and (round % 5 == 0):
            return C  // Rare forgiveness attempt
        else:
            return D
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
cooperation_rate_last_round = count_cooperators_last_round() / n
recent_cooperation_trend = average_cooperation_rate_last_3_rounds()

if cooperation_rate_last_round >= 0.6:
    return C  // Reward high cooperation with final cooperation
elif recent_cooperation_trend >= 0.4:
    return C  // Maintain cooperation if trend is reasonably good
else:
    return D  // Defect if cooperation has been consistently low
```

## Key Features

### 1. Majority Following with Forgiveness
- Cooperates when at least 50% of players cooperated in the previous round
- Uses forgiveness mechanisms to prevent permanent defection spirals
- Periodically tests the waters with cooperation even in low-cooperation environments

### 2. Adaptive Thresholds
- **High cooperation (≥50%)**: Always cooperate
- **Medium cooperation (30-49%)**: Selective cooperation with forgiveness
- **Low cooperation (<30%)**: Minimal cooperation with rare forgiveness attempts

### 3. Streak Breaking
- Includes mechanisms to break both cooperation and defection streaks
- Prevents getting locked into suboptimal patterns

### 4. End-Game Consideration
- Final round strategy rewards sustained cooperation
- Avoids naive cooperation if the group has been consistently non-cooperative

## Edge Case Handling

### First Round
Always cooperate to signal cooperative intent and give the group the best chance to establish a cooperative equilibrium.

### Low Participation Scenarios
If very few players are cooperating consistently, the strategy minimizes losses while maintaining occasional cooperation attempts to test for changed conditions.

### High Volatility
The strategy adapts to changing cooperation levels rather than being overly committed to either pure cooperation or defection.

## Strategic Rationale

1. **Cooperative Alignment**: Prioritizes mutual benefit when the group shows cooperative tendencies
2. **Resilience**: Doesn't collapse into permanent defection after encountering some non-cooperative behavior
3. **Adaptability**: Adjusts behavior based on observed group dynamics
4. **Forgiveness**: Includes mechanisms to rebuild cooperation after it breaks down
5. **Realistic**: Acknowledges that perfect cooperation may not be achievable and adapts accordingly

This strategy balances the cooperative goal with practical considerations about likely opponent behavior in a tournament setting where coordination cannot be assumed.
'''

description_COOPERATIVE_72 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation by adapting to the group's cooperative tendencies and maintaining a forgiving stance toward occasional defections.

## Decision Rules

### Round 1: Cooperative Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and test the waters for mutual cooperation

### Rounds 2 to r-1: Adaptive Cooperation
- **Primary Rule**: COOPERATE if the majority (≥ n/2) of players cooperated in the previous round
- **Secondary Rule**: If exactly half cooperated in the previous round, COOPERATE if:
  - The trend over the last 3 rounds shows increasing cooperation, OR
  - This is only the second round
- **Forgiveness Mechanism**: Even if the majority defected last round, still COOPERATE if:
  - You defected last round (give others a chance to reciprocate your return to cooperation), OR
  - The majority cooperated in at least 2 of the last 3 rounds (temporary setback forgiveness)

### Final Round (Round r): Conditional Cooperation
- **Action**: COOPERATE if the majority cooperated in round r-1
- **Rationale**: Maintain cooperative reputation even in the final round, as this builds long-term credibility

## Pseudocode

```
function decide_action(round, history):
    if round == 1:
        return COOPERATE
    
    # Get last round's cooperation count
    last_round_cooperators = count_cooperators(history[round-1])
    majority_threshold = ceil(n / 2)
    
    # Main decision logic
    if last_round_cooperators >= majority_threshold:
        return COOPERATE
    
    # Tie-breaking for exactly half
    if last_round_cooperators == floor(n / 2):
        if round == 2:
            return COOPERATE
        if cooperation_trending_up(history, 3):
            return COOPERATE
    
    # Forgiveness mechanisms
    if my_last_action(history) == DEFECT:
        return COOPERATE  # Give others chance to reciprocate
    
    if round >= 4:
        recent_coop_rounds = count_majority_coop_rounds(history[-3:])
        if recent_coop_rounds >= 2:
            return COOPERATE  # Forgive temporary setback
    
    # Default to defection if majority consistently defects
    return DEFECT

function cooperation_trending_up(history, window):
    if len(history) < window:
        return false
    recent = history[-window:]
    return count_cooperators(recent[-1]) > count_cooperators(recent[0])
```

## Strategy Advantages

1. **Collective Welfare Focus**: Prioritizes group cooperation over individual exploitation
2. **Adaptive**: Responds to group behavior rather than following a rigid pattern
3. **Forgiving**: Doesn't punish single defections harshly, allowing for recovery
4. **Exploitation-Resistant**: Will shift to defection if the group consistently defects
5. **Clear Signaling**: Cooperative start and consistent majority-following sends clear signals about intentions

## Edge Case Handling

- **First Round**: Always cooperate to signal good intentions
- **Final Round**: Maintain cooperation if majority was cooperative previously, building reputation
- **Tie Situations**: Err on the side of cooperation with trend analysis
- **Consistent Defection**: Will eventually defect if majority consistently defects, protecting against exploitation
- **Recovery**: Quick to return to cooperation when majority shows cooperative intent

This strategy balances the cooperative imperative with practical protection against exploitation, making it robust for tournament play while maintaining alignment with collective welfare maximization.
'''

description_COOPERATIVE_73 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Graduated Reciprocation"** that balances cooperation with strategic responses to defection.

## Strategy: Generous Tit-for-Tat with Graduated Reciprocation (GTTGR)

### Core Philosophy
This strategy starts cooperatively, forgives occasional defection, but responds proportionally to sustained non-cooperation. It aims to foster and maintain cooperative equilibria while protecting against exploitation.

### Decision Rules

#### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm

#### Rounds 2 to r-1: Graduated Response Based on Group Cooperation Level

**Step 1: Calculate cooperation rate from previous round**
```
cooperation_rate = (number_of_cooperators_last_round) / n
```

**Step 2: Determine response based on cooperation rate**
- If `cooperation_rate ≥ 0.67`: **Cooperate (C)**
  - High cooperation warrants continued cooperation
  
- If `0.33 ≤ cooperation_rate < 0.67`: **Probabilistic response**
  - Cooperate with probability = `cooperation_rate`
  - This creates incentive for others to cooperate more
  
- If `cooperation_rate < 0.33`: **Defect (D)**
  - Low cooperation triggers defensive defection

#### Round r (Final Round): Conditional Cooperation
- If `cooperation_rate_previous_round ≥ 0.5`: **Cooperate (C)**
- If `cooperation_rate_previous_round < 0.5`: **Defect (D)**

### Pseudocode Implementation

```python
def decide_action(round_number, history, n, r):
    if round_number == 1:
        return "C"  # Always cooperate first
    
    # Calculate cooperation rate from previous round
    last_round_actions = history[round_number - 2]  # Previous round
    cooperators = sum(1 for action in last_round_actions if action == "C")
    cooperation_rate = cooperators / n
    
    if round_number == r:  # Final round
        return "C" if cooperation_rate >= 0.5 else "D"
    
    # Middle rounds: graduated response
    if cooperation_rate >= 0.67:
        return "C"
    elif cooperation_rate >= 0.33:
        # Probabilistic cooperation based on group cooperation level
        return "C" if random.random() < cooperation_rate else "D"
    else:
        return "D"
```

### Strategy Properties

**Cooperative Elements:**
1. **Optimistic start**: Always begins with cooperation
2. **Forgiveness**: Doesn't punish single instances of defection if overall cooperation is high
3. **Reciprocal cooperation**: Rewards high group cooperation with continued cooperation
4. **Final round cooperation**: Cooperates in the last round if the group has been reasonably cooperative

**Strategic Elements:**
1. **Graduated response**: Punishment intensity matches the severity of group defection
2. **Threshold-based**: Clear cooperation thresholds prevent exploitation
3. **Proportional probability**: In mixed situations, cooperation probability matches group cooperation level

### Edge Case Handling

- **First round**: Unconditional cooperation to establish cooperative tone
- **Last round**: Conditional cooperation based on recent group behavior
- **All-defection scenarios**: Will defect when cooperation rate < 0.33, protecting against total exploitation
- **Mixed cooperation**: Uses probabilistic response to encourage higher cooperation rates

### Expected Tournament Performance

This strategy should perform well against:
- **Other cooperative strategies**: Will establish and maintain mutual cooperation
- **Tit-for-tat variants**: Compatible reciprocal behavior
- **Conditional cooperators**: Threshold-based approach should coordinate well

It provides reasonable protection against:
- **Pure defectors**: Will switch to defection when cooperation is very low
- **Exploitative strategies**: Graduated response prevents sustained exploitation

The strategy embodies cooperative game theory principles while maintaining strategic viability in a competitive tournament environment.
'''

description_COOPERATIVE_74 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It operates on the principle that cooperation is beneficial when others are likely to reciprocate, but defection becomes necessary when facing predominantly selfish opponents.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and test the waters

### Rounds 2 to r-1: Adaptive Cooperation
- **Cooperate IF:** More than half of the other players cooperated in the previous round
- **Defect IF:** Half or fewer of the other players cooperated in the previous round

Mathematical condition: `COOPERATE if Σ(c_j for j≠i) > (n-1)/2`

### Round r (Final Round): Conditional Cooperation
- **Cooperate IF:** The cooperation rate in round r-1 was ≥ 60%
- **Defect IF:** The cooperation rate in round r-1 was < 60%

## Pseudocode

```
function decide_action(round_number, game_history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == final_round:
        prev_cooperation_rate = count_cooperators(round_number - 1) / n
        if prev_cooperation_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # Rounds 2 to r-1
    others_cooperated = count_cooperators_excluding_self(round_number - 1)
    if others_cooperated > (n-1) / 2:
        return COOPERATE
    else:
        return DEFECT
```

## Strategic Rationale

### 1. **Encourages Cooperation**
- Starts cooperatively to signal good intentions
- Rewards cooperative environments by continuing to contribute
- Uses majority threshold to prevent being the "lone cooperator"

### 2. **Protects Against Exploitation**
- Defects when facing predominantly selfish opponents
- Uses a clear, observable threshold that others can understand and respond to
- Avoids being systematically exploited by free-riders

### 3. **Handles Edge Cases**
- **First Round**: Cooperates to establish cooperative precedent
- **Final Round**: Uses higher threshold (60%) to account for end-game effects while still rewarding sustained cooperation
- **Tie Situations**: When exactly half cooperate, defaults to defection to avoid exploitation

### 4. **Promotes Reciprocal Cooperation**
- The majority threshold creates incentives for others to cooperate
- If others adopt similar strategies, stable cooperation emerges naturally
- Clear and predictable responses allow for implicit coordination

## Expected Behavior Against Different Opponent Types

- **Against Cooperators**: Maintains mutual cooperation after round 1
- **Against Defectors**: Switches to defection after round 1, minimizing losses
- **Against Mixed Groups**: Adapts based on the prevailing behavior, encouraging cooperation when viable
- **Against Other Adaptive Strategies**: Likely to converge on mutual cooperation if others use similar majority-based rules

This strategy balances the cooperative goal of maximizing group welfare with the practical need to avoid exploitation in a competitive tournament environment.
'''

description_COOPERATIVE_75 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances the cooperative ideal with practical considerations for a tournament environment where opponents may not share cooperative norms.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and test the waters

**Rounds 2 to r-1 (Main Game):**
- **Cooperation Threshold Approach:**
  - Calculate cooperation rate from previous round: `coop_rate = cooperators_last_round / n`
  - If `coop_rate >= 0.5`: COOPERATE
  - If `coop_rate < 0.5`: Apply forgiveness mechanism (see below)

**Forgiveness Mechanism:**
- Maintain a "forgiveness counter" starting at 2
- When cooperation rate drops below 0.5:
  - If forgiveness counter > 0: COOPERATE and decrement counter
  - If forgiveness counter = 0: DEFECT and reset counter to 1
- Reset forgiveness counter to 2 whenever cooperation rate returns to ≥ 0.5

**Round r (Final Round):**
- If cooperation rate in round r-1 was ≥ 0.5: COOPERATE
- Otherwise: DEFECT
- Rationale: Maintain cooperation with cooperative groups, but don't be exploited in the final round by predominantly defecting groups

### Pseudocode

```
function decide_action(round, history):
    n = number_of_players
    r = total_rounds
    
    // First round
    if round == 1:
        return COOPERATE
    
    // Calculate previous round cooperation rate
    cooperators_last_round = count_cooperators(history[round-1])
    coop_rate = cooperators_last_round / n
    
    // Main game logic
    if round < r:
        if coop_rate >= 0.5:
            reset_forgiveness_counter_to_2()
            return COOPERATE
        else:
            if forgiveness_counter > 0:
                decrement_forgiveness_counter()
                return COOPERATE
            else:
                reset_forgiveness_counter_to_1()
                return DEFECT
    
    // Final round
    else: // round == r
        if coop_rate >= 0.5:
            return COOPERATE
        else:
            return DEFECT
```

## Strategic Rationale

### Why This Strategy is Cooperative:
1. **Starts with cooperation** to signal good intentions
2. **Rewards cooperative behavior** by continuing to cooperate when others do
3. **Gives second chances** through the forgiveness mechanism
4. **Doesn't immediately retaliate** against isolated defections

### Robustness Features:
1. **Threshold-based decision making** prevents being exploited by predominantly defecting populations
2. **Forgiveness mechanism** allows recovery from temporary cooperation breakdowns
3. **Final round protection** prevents being exploited when reputation no longer matters

### Expected Performance:
- **Against other cooperative strategies**: Should achieve high mutual cooperation
- **Against mixed populations**: Will cooperate when cooperation is prevalent, protecting against exploitation when it's not
- **Against predominantly defective strategies**: Will eventually defect to minimize losses while still giving opportunities for cooperation to emerge

This strategy embodies cooperative principles while incorporating practical safeguards necessary for a competitive tournament environment where opponent behavior is uncertain.
'''

description_COOPERATIVE_76 = '''
# Cooperative Strategy: "Graduated Reciprocator"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to exploitation. It combines initial cooperation signals, graduated responses to defection, and forgiveness mechanisms.

## Core Decision Rules

### Round 1-2: Cooperation Signaling
- **Always cooperate** in the first two rounds
- Rationale: Signal cooperative intent and allow observation of opponent patterns

### Round 3 to r-2: Adaptive Cooperation with Graduated Response
```pseudocode
cooperation_threshold = 0.5  // Minimum cooperation rate to maintain cooperation
defection_tolerance = 2      // Consecutive defections before escalating response
forgiveness_window = 3       // Rounds to wait before attempting reconciliation

if (total_cooperation_rate_last_3_rounds >= cooperation_threshold):
    action = COOPERATE
else if (consecutive_defections_against_me < defection_tolerance):
    action = COOPERATE  // Show patience
else:
    // Graduated punishment
    if (my_recent_defections < 2):
        action = DEFECT   // Limited retaliation
    else:
        // Forgiveness probe
        if (rounds_since_last_cooperation_attempt >= forgiveness_window):
            action = COOPERATE
        else:
            action = DEFECT
```

### Round r-1: Conditional Cooperation
- **Cooperate if** the overall cooperation rate across all players in the last 5 rounds ≥ 40%
- **Defect otherwise** to protect against end-game exploitation

### Round r (Final Round): Strategic Defection
- **Always defect** in the final round
- Rationale: No future rounds for retaliation, and other rational players will likely defect

## Detailed Strategy Logic

### 1. Cooperation Rate Calculation
```pseudocode
calculate_cooperation_rate(players, rounds_back):
    total_actions = players * rounds_back
    total_cooperations = count_cooperations_in_last_n_rounds(rounds_back)
    return total_cooperations / total_actions
```

### 2. Defection Tracking
```pseudocode
track_consecutive_defections():
    count = 0
    for round in reverse_chronological_order:
        if (my_action_was_defection):
            count++
        else:
            break
    return count
```

### 3. Forgiveness Mechanism
- After punishing defectors, periodically test cooperation
- If cooperation is reciprocated, return to cooperative stance
- If exploitation continues, resume punishment

## Edge Case Handling

### First Round
- Always cooperate to signal cooperative intent

### Early Rounds (2-4)
- Maintain cooperation unless facing universal defection
- If ≥80% of players defect in round 2, switch to cautious cooperation (cooperate only if ≥30% cooperated in previous round)

### Mid-Game Adaptation
- If trapped in mutual defection cycle, attempt cooperation every 3-4 rounds as a reconciliation signal
- Monitor if other players respond positively to these signals

### End-Game (Last 3 Rounds)
- Round r-2: Apply standard adaptive rules
- Round r-1: Higher threshold for cooperation (40% group cooperation rate)
- Round r: Always defect

### Low Participation Scenarios
- If very few players cooperate (≤20% rate) for 4+ consecutive rounds, reduce cooperation frequency but don't abandon entirely
- Continue periodic cooperation attempts to test for shifts in group behavior

## Key Features

1. **Initial Trust**: Starts cooperatively to establish good faith
2. **Graduated Response**: Doesn't immediately escalate to permanent defection
3. **Forgiveness**: Provides pathways back to cooperation
4. **End-Game Protection**: Recognizes the final round incentive structure
5. **Collective Awareness**: Considers group dynamics, not just individual interactions
6. **Resilient to Noise**: Tolerates occasional defections without breaking down cooperation

This strategy balances the cooperative imperative with protection against systematic exploitation, while remaining open to rebuilding cooperative relationships throughout the game.
'''

description_COOPERATIVE_77 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances being "nice" (cooperative by default) with being "provocable" (responds to defection) and "forgiving" (doesn't hold grudges indefinitely).

## Decision Rules

### Core Logic:
```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness (GTTF)

PARAMETERS:
- cooperation_threshold = 0.5  // Minimum fraction of players needed to cooperate
- forgiveness_period = 3       // Rounds to wait before forgiving defectors
- generosity_rate = 0.1        // Probability to cooperate despite defection

INITIALIZE:
- Round 1: Always COOPERATE
- defection_memory = {}        // Track when players last defected

FOR each round t > 1:
    current_cooperators = count_cooperators_last_round()
    cooperation_rate = current_cooperators / (n-1)  // Exclude self
    
    // Main decision logic
    IF cooperation_rate >= cooperation_threshold:
        action = COOPERATE
    ELSE:
        // Check if enough time has passed to forgive
        recent_defectors = count_recent_defectors(forgiveness_period)
        
        IF recent_defectors < (n-1) * 0.7:  // Most players haven't defected recently
            action = COOPERATE
        ELSE:
            // Be generous with small probability
            IF random() < generosity_rate:
                action = COOPERATE
            ELSE:
                action = DEFECT
    
    // Special handling for final rounds
    IF t > r - 2:  // Last 2 rounds
        IF cooperation_rate >= 0.7:  // High cooperation observed
            action = COOPERATE
        ELSE:
            action = DEFECT
    
    RETURN action
```

## Detailed Strategy Components

### 1. **First Round Behavior**
- Always COOPERATE in round 1
- Rationale: Establish cooperative intent and give others the benefit of the doubt

### 2. **Cooperation Threshold**
- Cooperate if at least 50% of other players cooperated in the previous round
- This prevents being exploited when cooperation has clearly broken down
- Maintains cooperation when there's reasonable reciprocity

### 3. **Forgiveness Mechanism**
- Don't permanently punish players for past defections
- After 3 rounds, "forget" previous defections and reassess based on recent behavior
- Prevents permanent feuds and allows cooperation to re-emerge

### 4. **Generosity Component**
- Even when the threshold suggests defection, cooperate with 10% probability
- Helps break cycles of mutual punishment
- Provides occasional "olive branches" to restart cooperation

### 5. **End-Game Handling**
- In the final 2 rounds, use a higher cooperation threshold (70%)
- If cooperation is strong, continue cooperating to maximize group benefit
- If cooperation has broken down, protect against exploitation in final rounds

### 6. **Adaptive Response**
- Monitor the overall cooperation level in the group
- Adjust behavior based on collective patterns rather than individual grudges
- More robust against mixed populations of strategies

## Edge Cases

### Last Round (r):
- If cooperation rate ≥ 70% in round r-1: COOPERATE
- Otherwise: DEFECT (standard end-game reasoning)

### Second-to-Last Round (r-1):
- Similar logic but slightly more forgiving to maintain cooperation

### After Mass Defection:
- If everyone defected last round, still cooperate with 10% probability
- Prevents complete breakdown and tests if others are willing to restart cooperation

## Strategic Rationale

1. **Cooperative Nature**: Starts cooperatively and maintains cooperation when others reciprocate
2. **Exploitation Protection**: Won't be consistently exploited due to the cooperation threshold
3. **Forgiveness**: Allows recovery from punishment cycles that can emerge in repeated games
4. **Group-Focused**: Makes decisions based on overall group behavior rather than tracking individual players
5. **Robust**: Performs well against various strategy types:
   - Against other cooperators: Maintains mutual cooperation
   - Against defectors: Protects itself while offering chances to cooperate
   - Against conditional cooperators: Can establish stable cooperation patterns

This strategy aims to foster the cooperative equilibrium that maximizes group welfare while maintaining reasonable self-protection against exploitation.
'''

description_COOPERATIVE_78 = '''
# Generous Tit-for-Tat with Majority Rule (GTFMR)

## Core Strategy
My strategy combines cooperative signaling, conditional cooperation based on group behavior, and strategic forgiveness to maintain cooperation while protecting against exploitation.

## Decision Rules

### Round 1: Cooperative Signal
**Always cooperate (C)** in the first round to signal cooperative intent and establish a foundation for mutual cooperation.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
Use a **majority-based threshold with generous forgiveness**:

```pseudocode
cooperation_threshold = ceil(n/2)  // Majority threshold
forgiveness_probability = 0.15     // 15% chance to forgive defection

previous_cooperators = count_cooperators_in_previous_round()

if previous_cooperators >= cooperation_threshold:
    return COOPERATE
else:
    // Apply forgiveness mechanism
    if random() < forgiveness_probability:
        return COOPERATE  // Forgive and try to restart cooperation
    else:
        return DEFECT     // Punish low cooperation
```

### Final Round: Conditional Cooperation
In the last round, maintain the same majority rule **without forgiveness** to prevent end-game exploitation while still rewarding groups that have maintained cooperation.

```pseudocode
previous_cooperators = count_cooperators_in_previous_round()
if previous_cooperators >= cooperation_threshold:
    return COOPERATE
else:
    return DEFECT
```

## Strategy Rationale

### 1. Cooperative Foundation
- **First round cooperation** signals good intentions and creates opportunity for mutual cooperation
- Establishes a cooperative baseline that other cooperative strategies can recognize and reciprocate

### 2. Majority-Based Threshold
- **Responsive to group dynamics**: Cooperates when at least half the group cooperates
- **Robust to minority defection**: Doesn't abandon cooperation due to 1-2 defectors
- **Scalable**: Works effectively regardless of group size (n)

### 3. Generous Forgiveness Mechanism
- **Prevents permanent punishment spirals**: 15% chance to cooperate even when cooperation is low
- **Enables recovery**: Allows the group to return to cooperative equilibrium after temporary defection
- **Balances exploitation protection**: High enough to enable recovery, low enough to discourage persistent defection

### 4. Strategic End-Game Behavior
- **Removes forgiveness in final round** to prevent exploitation of known end-game
- **Maintains conditional cooperation** to reward groups that have sustained cooperation throughout

## Handling Edge Cases

- **All defect scenario**: Strategy will occasionally attempt cooperation (15% forgiveness rate) to test if group dynamics have changed
- **Mixed cooperation**: Strategy adapts dynamically based on majority behavior
- **High cooperation groups**: Strategy sustains cooperation by reciprocating
- **Final round**: Prevents end-game defection while rewarding sustained cooperation

## Cooperative Alignment

This strategy embodies cooperative principles by:
1. **Leading by example** (first round cooperation)
2. **Rewarding group cooperation** (majority threshold)
3. **Offering second chances** (forgiveness mechanism)
4. **Supporting mutual benefit** (maintains cooperation when group does)
5. **Protecting against exploitation** (punishes persistent defection)

The strategy aims to foster and maintain cooperative equilibria while being resilient to both accidental defection and strategic exploitation.
'''

description_COOPERATIVE_79 = '''
# Cooperative Strategy: "Conditional Cooperator with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances cooperative intentions with practical considerations of the tournament environment.

## Decision Rules

### Round 1: Cooperative Signal
- **Action: COOPERATE**
- **Rationale:** Start cooperatively to signal willingness to engage in mutual cooperation and establish a positive precedent.

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule:** Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism:** If cooperation rate < 50%, still cooperate if:
  - The cooperation rate is improving (higher than two rounds ago), OR
  - This is the first time cooperation has dropped below 50% in the last 3 rounds

### Round r (Final Round): Sustained Cooperation
- **Action: COOPERATE**
- **Rationale:** Maintain cooperative stance even in the final round to avoid triggering end-game defection cascades that could unravel cooperation in earlier rounds.

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        return COOPERATE
    
    # Calculate cooperation rate in previous round
    prev_coop_rate = count_cooperators(history[round_number - 1]) / n
    
    # Primary cooperation condition
    if prev_coop_rate >= 0.5:
        return COOPERATE
    
    # Forgiveness conditions
    if round_number >= 3:
        two_rounds_ago_rate = count_cooperators(history[round_number - 2]) / n
        if prev_coop_rate > two_rounds_ago_rate:  # Improving trend
            return COOPERATE
    
    # Check if this is first recent drop below 50%
    recent_drops = 0
    for i in range(max(1, round_number - 3), round_number):
        if count_cooperators(history[i]) / n < 0.5:
            recent_drops += 1
    
    if recent_drops == 1:  # First recent drop
        return COOPERATE
    
    return DEFECT
```

## Strategic Rationale

### Cooperation Promotion
1. **Optimistic Start:** Beginning with cooperation signals good intentions and gives others a chance to reciprocate
2. **Majority Threshold:** The 50% cooperation threshold creates a stable focal point - if half the players cooperate, cooperation remains profitable for the group
3. **Final Round Cooperation:** Avoiding end-game defection helps maintain trust throughout the game

### Exploitation Protection
1. **Conditional Response:** Will defect if cooperation drops significantly, preventing unlimited exploitation
2. **Forgiveness Limits:** Limited forgiveness prevents repeated exploitation while allowing recovery from temporary setbacks

### Adaptability
1. **Trend Recognition:** Rewards improving cooperation rates even if they haven't reached the threshold
2. **Context Sensitivity:** Considers recent history rather than just the immediate previous round

## Edge Case Handling

- **First Round:** Always cooperate to establish positive precedent
- **Second Round:** Base decision solely on first round results using the 50% threshold
- **Final Round:** Always cooperate to maintain credibility and avoid triggering defection cascades
- **All Players Defected Previously:** Will defect unless there are signs of improvement or it's a first offense

## Expected Performance

This strategy should perform well against:
- Other cooperative strategies (mutual cooperation)
- Mixed populations (establishes cooperation among willing participants)
- Strategies with similar forgiveness mechanisms

The strategy balances being "nice" (starts cooperatively), "retaliatory" (punishes widespread defection), "forgiving" (allows recovery), and "clear" (uses an obvious 50% threshold that others can recognize and coordinate around).
'''

description_COOPERATIVE_80 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibria while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through conditional cooperation based on group behavior.

## Decision Rules

### Round 1: Optimistic Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the beginning.

### Rounds 2 to r-1: Conditional Cooperation
- **Primary Rule**: Cooperate if the majority (≥ n/2) of players cooperated in the previous round
- **Secondary Rule**: If exactly half cooperated in the previous round, cooperate if the trend over the last 2 rounds shows increasing or stable cooperation

### Round r (Final Round): Strategic Cooperation
- **Action**: Cooperate if at least (n/3) players cooperated in round r-1
- **Rationale**: Even in the final round, maintain some cooperative behavior to avoid complete breakdown, but with a lower threshold since there's no future retaliation.

## Detailed Algorithm

```pseudocode
Strategy ForgivingMajorityFollower(current_round, history):
    n = number_of_players
    r = total_rounds
    
    if current_round == 1:
        return COOPERATE
    
    if current_round == r:  // Final round
        cooperators_last_round = count_cooperators(history[r-1])
        if cooperators_last_round >= n/3:
            return COOPERATE
        else:
            return DEFECT
    
    // Rounds 2 to r-1
    cooperators_last_round = count_cooperators(history[current_round-1])
    
    if cooperators_last_round >= n/2:
        return COOPERATE
    
    if cooperators_last_round == n/2 and current_round >= 3:
        cooperators_two_rounds_ago = count_cooperators(history[current_round-2])
        if cooperators_last_round >= cooperators_two_rounds_ago:
            return COOPERATE
        else:
            return DEFECT
    
    return DEFECT
```

## Key Features

### 1. Majority-Based Cooperation
- Cooperates when the majority demonstrates cooperative behavior
- This creates a stable equilibrium when most players are cooperative
- Protects against minority exploitation

### 2. Forgiveness Mechanism
- Doesn't punish individual defectors harshly
- Focuses on overall group cooperation level rather than tracking individual players
- Allows recovery from temporary cooperation breakdowns

### 3. Trend Sensitivity
- In tie situations (n/2 cooperators), considers recent trends
- Rewards increasing cooperation patterns
- Prevents cooperation decay in balanced situations

### 4. Endgame Adaptation
- Uses lower cooperation threshold in final round (n/3 instead of n/2)
- Recognizes that final round dynamics differ due to no future consequences
- Still maintains some cooperation to avoid complete breakdown

## Edge Case Handling

### Small Groups (n=2,3)
- For n=2: Majority rule becomes "cooperate if opponent cooperated"
- For n=3: Majority requires at least 2 cooperators
- Strategy remains mathematically sound

### High Defection Scenarios
- If cooperation falls below majority threshold, switches to defection
- Can quickly return to cooperation when group behavior improves
- Protects against sustained exploitation

### All-Defection Traps
- Strategy will defect when stuck in all-defection equilibrium
- Ready to immediately return to cooperation if others show cooperative signals
- First-round cooperation helps avoid initial defection traps

## Cooperative Alignment

This strategy is fundamentally cooperative because:

1. **Default to Cooperation**: Starts cooperatively and maintains cooperation when possible
2. **Group Welfare Focus**: Bases decisions on overall group cooperation rather than individual punishment
3. **Quick Forgiveness**: Doesn't hold grudges against individual defectors
4. **Equilibrium Seeking**: Actively works to establish and maintain cooperative equilibria
5. **Mutual Benefit**: Recognizes that mutual cooperation maximizes group welfare given k > 1

The strategy balances the cooperative imperative with rational self-protection, making it both principled and strategically sound in a tournament environment.
'''

description_COOPERATIVE_81 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

### Rounds 2 to r-1: Adaptive Cooperation
The strategy maintains a "cooperation score" for the group based on recent behavior:

```pseudocode
cooperation_threshold = 0.6  // Require 60% cooperation rate to continue cooperating
forgiveness_probability = 0.1  // 10% chance to cooperate even when threshold not met
memory_window = min(3, current_round - 1)  // Look at last 3 rounds or all available

function decide_action(round_number, game_history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        return handle_final_round(game_history)
    
    // Calculate recent cooperation rate
    recent_cooperation_rate = calculate_cooperation_rate(game_history, memory_window)
    
    if recent_cooperation_rate >= cooperation_threshold:
        return COOPERATE
    else:
        // Occasional forgiveness to restart cooperation
        if random() < forgiveness_probability:
            return COOPERATE
        else:
            return DEFECT

function calculate_cooperation_rate(history, window):
    total_players = 0
    total_cooperators = 0
    
    for round in last_window_rounds(history, window):
        for player_action in round:
            total_players += 1
            if player_action == COOPERATE:
                total_cooperators += 1
    
    return total_cooperators / total_players
```

### Final Round (Round r): Strategic Defection
- **Action**: DEFECT
- **Rationale**: In the final round, there's no future to incentivize cooperation, so rational players will defect. Anticipating this, we defect to avoid being exploited.

## Edge Case Handling

### Early Game (Rounds 1-3)
- Start cooperatively but be ready to adapt quickly
- Use shorter memory windows to be more responsive to emerging patterns
- Higher forgiveness probability (0.15) to give cooperation more chances to establish

### Mid Game Adjustments
- If cooperation rate has been consistently high (>80%) for 5+ rounds, lower the threshold temporarily to 0.5 to be more tolerant of occasional defections
- If the game has been mostly defection (<20% cooperation) for 5+ rounds, require higher threshold (0.7) before resuming cooperation

### Endgame Considerations (Last 20% of rounds)
- Gradually reduce forgiveness probability as the game approaches the end
- In the final 3 rounds, only cooperate if cooperation rate is very high (>0.8)

## Strategy Advantages

1. **Cooperative by Default**: Starts cooperatively and maintains cooperation when others reciprocate
2. **Exploitation Resistant**: Won't be consistently taken advantage of by defectors
3. **Forgiveness Mechanism**: Can recover from mutual defection spirals
4. **Adaptive**: Responds to the actual behavior patterns observed
5. **Endgame Aware**: Protects against final-round exploitation

## Expected Behavior Against Common Strategies

- **Against Always Cooperate**: Will establish mutual cooperation quickly
- **Against Always Defect**: Will initially try cooperation, then switch to mostly defecting with occasional forgiveness attempts
- **Against Tit-for-Tat variants**: Will likely establish stable cooperation
- **Against Random strategies**: Will adapt based on the realized cooperation rate
- **Against Complex strategies**: The memory window and threshold system should identify and respond to most patterns

This strategy prioritizes establishing cooperative equilibria while maintaining enough defensive mechanisms to avoid severe exploitation, making it robust across various opponent types while staying true to cooperative principles.
'''

description_COOPERATIVE_82 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy balances cooperation with protection against exploitation while maintaining a cooperative mindset. It starts cooperatively, reciprocates the general behavior of the group, but includes forgiveness mechanisms to recover from mutual defection spirals.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round >= 0.5:
    action = C
else:
    action = D
```

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability 0.2 (20% chance)
- This prevents permanent defection spirals
- Occasionally "tests" if others are willing to return to cooperation

### Final Round (Round r): Conditional Cooperation
Despite the temptation to defect in the final round, maintain cooperation if:
- Cooperation rate in round r-1 was ≥ 60%, OR
- Personal cumulative payoff is already satisfactory (above average expected payoff)

Otherwise, defect to avoid being exploited when others likely defect.

## Complete Strategy Pseudocode

```pseudocode
function decide_action(round, game_history, n, k):
    if round == 1:
        return C
    
    # Calculate cooperation rate in previous round
    prev_round_cooperators = count_cooperators(game_history[round-1])
    cooperation_rate = prev_round_cooperators / n
    
    if round < r:  # Not final round
        if cooperation_rate >= 0.5:
            return C
        else:
            # Forgiveness mechanism
            if random() < 0.2:
                return C
            else:
                return D
    
    else:  # Final round (round == r)
        if cooperation_rate >= 0.6:
            return C
        else:
            # Check if we're doing well enough to be generous
            my_avg_payoff = my_total_payoff / (r-1)
            expected_mutual_coop_payoff = k/n * n  # = k
            
            if my_avg_payoff >= expected_mutual_coop_payoff * 0.8:
                return C
            else:
                return D
```

## Key Features

1. **Cooperative Start**: Always begins with cooperation to signal good intentions
2. **Majority Rule**: Follows the group's general tendency while rewarding collective cooperation
3. **Forgiveness**: 20% chance to cooperate even when others mostly defect, preventing permanent punishment cycles
4. **Final Round Logic**: More stringent cooperation requirement (60% vs 50%) but includes payoff satisfaction check

## Strategic Rationale

- **Cooperative Alignment**: Prioritizes mutual cooperation and group welfare
- **Exploitation Protection**: Doesn't cooperate blindly when facing mostly defectors
- **Spiral Prevention**: Forgiveness mechanism helps restart cooperation cycles
- **Adaptive**: Responds to the actual behavior of opponents rather than assumptions
- **Robust**: Handles various opponent types from always-cooperate to tit-for-tat to more complex strategies

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones, fulfilling the cooperative mandate while remaining strategically sound.
'''

description_COOPERATIVE_83 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It starts cooperatively, reciprocates the group's behavior, but includes forgiveness mechanisms to prevent permanent defection spirals.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Primary Rule**: Cooperate if the cooperation rate in the previous round was above a dynamic threshold.

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n
dynamic_threshold = max(0.3, (k-1)/(n-1))

if cooperation_rate_last_round >= dynamic_threshold:
    action = C
else:
    action = D
```

**Forgiveness Mechanism**: Every 3 rounds, if we've been defecting, attempt cooperation regardless of recent history.

```pseudocode
if (current_round % 3 == 0) and (our_last_action == D):
    action = C  // Forgiveness attempt
```

### Final Round: Conditional Cooperation
- **Action**: Cooperate only if cooperation rate in round r-1 was ≥ 50%
- **Rationale**: Avoid being exploited in the final round while still rewarding consistent cooperators

## Key Features

### 1. Dynamic Threshold Calculation
The cooperation threshold adapts to game parameters:
- **Minimum threshold**: 30% (prevents hair-trigger responses)
- **Parameter-based threshold**: (k-1)/(n-1) reflects the economic incentive structure
- Uses the higher of these two values

### 2. Forgiveness Cycles
- Every third round, attempt cooperation if we've been defecting
- Prevents permanent punishment cycles
- Allows recovery from temporary coordination failures

### 3. Group-Based Assessment
- Evaluates the entire group's cooperation level, not individual players
- More stable than tracking individual reputations
- Naturally handles varying group compositions

## Strategy Pseudocode

```pseudocode
function decide_action(round_number, game_history):
    if round_number == 1:
        return C
    
    if round_number == total_rounds:
        last_round_coop_rate = count_cooperators(game_history, round_number-1) / n
        return C if last_round_coop_rate >= 0.5 else D
    
    // Check forgiveness condition
    if (round_number % 3 == 0) and (my_last_action == D):
        return C
    
    // Main decision logic
    last_round_coop_rate = count_cooperators(game_history, round_number-1) / n
    threshold = max(0.3, (k-1)/(n-1))
    
    return C if last_round_coop_rate >= threshold else D
```

## Handling Edge Cases

1. **First Round**: Always cooperate to establish good faith
2. **After mass defection**: Forgiveness mechanism prevents permanent punishment
3. **Final round**: Conditional cooperation based on recent group behavior
4. **Small groups**: Dynamic threshold accounts for parameter sensitivity
5. **High multiplication factors**: Threshold adjusts upward when cooperation is more valuable

## Cooperative Alignment

This strategy is genuinely cooperative because it:
- **Starts optimistically** with unconditional cooperation
- **Rewards group cooperation** by continuing to cooperate when others do
- **Includes forgiveness** to break punishment cycles
- **Avoids hair-trigger punishment** with the 30% minimum threshold
- **Considers collective welfare** through group-based rather than individual-based decisions

The strategy balances the cooperative ideal of maximizing group welfare with the practical need to avoid exploitation, making it robust for tournament play while maintaining a fundamentally cooperative orientation.
'''

description_COOPERATIVE_84 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances cooperative intent with self-protection mechanisms.

## Strategy Description

### Initial Approach
- **Round 1**: Always COOPERATE (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Main Decision Rule
For rounds 2 through r-1, use a modified tit-for-tat approach based on the **cooperation rate** of other players:

```pseudocode
cooperation_rate = (total_cooperators_last_round - my_contribution) / (n - 1)

if cooperation_rate >= 0.5:
    action = COOPERATE
else if cooperation_rate >= 0.3:
    if random(0,1) < 0.7:  // 70% chance
        action = COOPERATE
    else:
        action = DEFECT
else:
    action = DEFECT
```

### Forgiveness Mechanism
Track consecutive defection rounds. If I've been defecting for 2+ consecutive rounds due to low cooperation:

```pseudocode
if consecutive_defection_rounds >= 2:
    if random(0,1) < 0.3:  // 30% chance to forgive
        action = COOPERATE
        reset consecutive_defection_counter
```

### Final Round Handling
- **Round r**: COOPERATE if cooperation_rate in previous round ≥ 0.4, otherwise DEFECT
- **Rationale**: Avoid being exploited in the final round while rewarding sustained cooperation

## Key Features

### 1. Cooperative by Default
- Starts with cooperation to signal good intentions
- Maintains cooperation when others reciprocate (≥50% cooperation rate)
- Gives partial cooperation even at moderate rates (30-50% range)

### 2. Protection Against Exploitation
- Defects when cooperation rate falls below 30%
- Adjusts behavior in final round to prevent end-game exploitation
- Uses probabilistic responses to avoid being perfectly predictable

### 3. Recovery Mechanisms
- Forgiveness mechanism prevents permanent defection spirals
- Gradual response rather than immediate punishment encourages cooperation recovery

### 4. Adaptive Thresholds
- 50% threshold: Strong cooperation signal
- 30-50% range: Cautious cooperation to encourage others
- <30%: Protection mode while leaving room for recovery

## Strategic Reasoning

### Why This Works
1. **Establishes Cooperation**: Initial cooperation and generous thresholds encourage cooperative equilibria
2. **Prevents Exploitation**: Clear defection triggers protect against free-riders
3. **Enables Recovery**: Forgiveness and probabilistic elements allow groups to escape defection cycles
4. **Handles Endgame**: Final round adjustment prevents terminal exploitation

### Robustness
- Works well against other cooperative strategies (mutual cooperation)
- Protects against pure defectors (switches to defection when necessary)
- Can recover from temporary breakdowns in cooperation
- Handles mixed populations effectively through graduated responses

This strategy prioritizes establishing cooperative outcomes while maintaining enough defensive mechanisms to avoid being systematically exploited, making it well-suited for a tournament environment with diverse opponent strategies.
'''

description_COOPERATIVE_85 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances optimism about cooperation with pragmatic responses to defection.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
For each round t (2 ≤ t ≤ r-1):

```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_recent_exploitation = (times_i_cooperated_last_3_rounds > times_others_avg_cooperated_last_3_rounds)

if cooperation_rate >= 0.5:
    // Majority cooperated - reward this
    action = C
    
else if cooperation_rate >= 0.3:
    // Mixed cooperation - be generous but cautious
    if my_recent_exploitation and random(0,1) < 0.3:
        action = D  // Occasional punishment
    else:
        action = C
        
else:
    // Low cooperation environment
    if cooperation_rate > 0:
        // Some cooperation exists - try to rebuild
        if random(0,1) < 0.4:
            action = C  // Probabilistic forgiveness
        else:
            action = D
    else:
        // Universal defection
        action = D
```

### Round r (Final Round): Conditional Cooperation
```pseudocode
cooperation_rate_last_round = count_cooperators_last_round / n
overall_cooperation_rate = total_cooperation_observed / (n * (r-1))

if cooperation_rate_last_round >= 0.6 or overall_cooperation_rate >= 0.5:
    action = C  // Reward sustained cooperation
else:
    action = D  // Protect against end-game defection
```

## Key Features

### 1. **Generous Starting Stance**
- Always cooperate in round 1 to signal cooperative intent
- Gives others opportunity to establish mutual cooperation

### 2. **Majority-Based Response**
- When majority cooperates (≥50%), always cooperate back
- Reinforces cooperative equilibrium when it emerges

### 3. **Graduated Response to Defection**
- Responds proportionally to the level of defection observed
- Doesn't immediately punish isolated defectors
- Escalates response as defection becomes more widespread

### 4. **Forgiveness Mechanism**
- Even in low-cooperation environments, occasionally cooperates to test for renewed cooperation
- Prevents permanent breakdown of cooperation due to temporary conflicts

### 5. **End-Game Handling**
- Final round cooperation depends on established cooperation patterns
- Rewards groups that maintained cooperation throughout
- Protects against predictable end-game defection

### 6. **Exploitation Protection**
- Monitors whether it's being systematically exploited
- Introduces probabilistic punishment when consistently contributing more than others

## Strategic Rationale

1. **Mutual Benefit Recognition**: Since k > 1, mutual cooperation yields higher payoffs than mutual defection
2. **Social Proof Utilization**: Uses group cooperation levels as signals for appropriate behavior
3. **Reputation Building**: Consistent early cooperation establishes trustworthy reputation
4. **Adaptive Flexibility**: Adjusts to the cooperative culture that emerges in each specific game
5. **Robust Against Exploitation**: Won't be consistently taken advantage of by pure defectors

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones, making it suitable for a tournament environment where cooperative success depends on finding and sustaining mutually beneficial relationships.
'''

description_COOPERATIVE_86 = '''
# Cooperative Strategy: "Forgiving Tit-for-Tat with Gradual Recovery"

## Core Philosophy
This strategy balances cooperation with self-protection by starting cooperatively, responding proportionally to defection levels, and maintaining pathways back to full cooperation.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and establish a foundation for mutual cooperation

### Rounds 2 to r-1: Adaptive Response Based on Cooperation Rate
- **Calculate cooperation rate**: `coop_rate = total_cooperators_last_round / n`
- **Decision logic**:
  ```
  if coop_rate >= 0.67:
      action = C  // High cooperation - reward it
  else if coop_rate >= 0.33:
      action = C with probability 0.75  // Mixed cooperation - mostly cooperate
  else:
      action = D  // Low cooperation - protect yourself
  ```

### Final Round (Round r): Conditional Cooperation
- **If** average cooperation rate across all previous rounds ≥ 0.5: **Cooperate**
- **Else**: **Defect**

## Key Features

### 1. Forgiveness Mechanism
- Strategy doesn't permanently punish defectors
- Each round offers a fresh opportunity based on recent behavior
- Prevents spiral into mutual defection

### 2. Proportional Response
- Response intensity matches the level of defection observed
- High defection → self-protection
- Mixed signals → cautious cooperation
- High cooperation → full cooperation

### 3. Collective Focus
- Decisions based on overall group behavior, not individual tracking
- Encourages group-level cooperation norms
- Simpler to implement and understand

## Edge Case Handling

### First Round
- Always cooperate to signal cooperative intent
- Establishes baseline for others to reciprocate

### Last Round  
- Cooperate only if the group has demonstrated consistent cooperation
- Prevents being exploited in the final round while rewarding good groups

### Ties in Cooperation Rate
- At exactly 0.67 threshold: Cooperate (benefit of doubt)
- At exactly 0.33 threshold: Use probabilistic cooperation (75% chance)

## Strategic Rationale

### Why This Works
1. **Establishes Cooperation**: Starting with cooperation signals intent
2. **Rewards Good Behavior**: High cooperation rates are met with continued cooperation
3. **Protects Against Exploitation**: Low cooperation triggers self-protection
4. **Maintains Flexibility**: Proportional responses allow for recovery
5. **Group-Oriented**: Focuses on collective outcomes rather than individual grudges

### Tournament Considerations
- **Against Other Cooperators**: Will establish and maintain mutual cooperation
- **Against Pure Defectors**: Will protect itself after initial cooperative gesture  
- **Against Mixed Strategies**: Will adapt proportionally, encouraging cooperation when possible
- **Against Conditional Cooperators**: Likely to find stable cooperative equilibrium

## Pseudocode Summary
```
Strategy: Forgiving_Tit_for_Tat_Gradual

if round == 1:
    return C
    
if round == r:  // Final round
    if average_coop_rate_so_far >= 0.5:
        return C
    else:
        return D

// Middle rounds
coop_rate = cooperators_last_round / n

if coop_rate >= 0.67:
    return C
else if coop_rate >= 0.33:
    return C with probability 0.75
else:
    return D
```

This strategy maintains a cooperative orientation while protecting against exploitation, adapting to the group's behavior, and providing clear incentives for others to cooperate.
'''

description_COOPERATIVE_87 = '''
# Cooperative Strategy: "Forgiving Reciprocator with Momentum Building"

## Core Philosophy
This strategy prioritizes long-term collective welfare while protecting against exploitation. It starts with optimistic cooperation, builds momentum when cooperation emerges, and forgives occasional defections to maintain cooperative relationships.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- **Rationale:** Signal cooperative intent and test for reciprocal players

### Rounds 2 to r-1: Adaptive Reciprocal Cooperation

```pseudocode
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        return decide_final_round(history)
    
    // Calculate recent cooperation metrics
    recent_rounds = min(3, round_number - 1)
    my_recent_cooperation_rate = count_my_cooperations(last_n_rounds=recent_rounds) / recent_rounds
    group_recent_cooperation_rate = count_total_cooperations(last_n_rounds=recent_rounds) / (recent_rounds * n)
    
    // High cooperation momentum - continue cooperating
    if group_recent_cooperation_rate >= 0.67:
        return COOPERATE
    
    // Moderate cooperation - reciprocate based on group behavior
    if group_recent_cooperation_rate >= 0.4:
        if my_recent_cooperation_rate > group_recent_cooperation_rate:
            // I've been more cooperative than average - give one more chance
            return COOPERATE
        else:
            // Match group cooperation level
            return COOPERATE if random() < group_recent_cooperation_rate else DEFECT
    
    // Low cooperation environment
    if group_recent_cooperation_rate >= 0.2:
        // Occasional cooperation to test for revival opportunities
        if (round_number % 3 == 1) and (my_recent_cooperation_rate < 0.33):
            return COOPERATE  // Test cooperation every 3 rounds
        else:
            return DEFECT
    
    // Very low cooperation - primarily defect but test occasionally
    if round_number % 5 == 1:
        return COOPERATE  // Rare cooperation test
    else:
        return DEFECT
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
function decide_final_round(history):
    // Calculate overall cooperation rate
    total_cooperation_rate = count_total_cooperations(all_rounds) / ((r-1) * n)
    my_cooperation_rate = count_my_cooperations(all_rounds) / (r-1)
    
    // If high mutual cooperation throughout game
    if total_cooperation_rate >= 0.6 and my_cooperation_rate >= 0.6:
        return COOPERATE  // Reward sustained cooperation
    
    // If moderate cooperation and I've been generous
    if total_cooperation_rate >= 0.4 and my_cooperation_rate >= total_cooperation_rate + 0.1:
        return COOPERATE  // Final generous gesture
    
    // Otherwise, protect against final round exploitation
    return DEFECT
```

## Key Strategic Features

### 1. **Momentum Building**
- Recognizes when cooperation is working (≥67% group cooperation rate)
- Maintains cooperation during successful collective phases
- Creates positive feedback loops

### 2. **Forgiving Nature**
- Doesn't immediately retaliate for single defections
- Uses 3-round rolling windows to smooth out noise
- Periodic cooperation tests even in hostile environments

### 3. **Exploitation Protection**
- Reduces cooperation when consistently giving more than receiving
- Switches to primarily defecting in very low cooperation environments
- Guards against final round exploitation while rewarding sustained cooperators

### 4. **Adaptive Thresholds**
- 67% threshold: High cooperation momentum
- 40% threshold: Moderate cooperation reciprocation
- 20% threshold: Low cooperation with testing
- Below 20%: Minimal cooperation with rare tests

## Edge Case Handling

- **First Round:** Always cooperate to signal good intentions
- **Final Round:** Cooperate only if sustained mutual cooperation has been established
- **Early Game:** Focus on building cooperative momentum
- **Mid Game:** Adapt based on emerging patterns
- **Late Game:** Balance between rewarding cooperation and preventing exploitation

## Cooperative Alignment

This strategy embodies cooperation by:
- Starting optimistically and signaling cooperative intent
- Forgiving occasional defections to maintain relationships  
- Testing for cooperation revival even in hostile environments
- Rewarding sustained group cooperation
- Building positive momentum when cooperation emerges
- Prioritizing long-term collective welfare over short-term gains

The strategy aims to find and nurture cooperative players while protecting against persistent exploiters, creating the best possible outcome for genuine cooperators in the group.
'''

description_COOPERATIVE_88 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances generosity to encourage cooperation with defensive measures to prevent being taken advantage of.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability 0.3
- **Defection Trigger**: Only defect if cooperation rate < 50% AND forgiveness doesn't activate

### Round r (Final Round): Strategic Cooperation
- **Action**: Cooperate if cooperation rate in round r-1 was ≥ 40%
- **Rationale**: Slightly lower threshold in final round to account for end-game defection incentives

## Pseudocode

```
function decide_action(round_number, game_history):
    if round_number == 1:
        return C
    
    previous_round = game_history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / n
    
    if round_number == r:  # Final round
        threshold = 0.4
        return C if cooperation_rate >= threshold else D
    
    else:  # Rounds 2 to r-1
        if cooperation_rate >= 0.5:
            return C
        else:
            # Forgiveness mechanism
            if random() < 0.3:
                return C
            else:
                return D
```

## Strategy Justification

### 1. Cooperative Foundation
- **Always start with cooperation** to signal good intentions
- **Maintain cooperation** when others reciprocate (≥50% cooperation rate)
- This creates positive momentum and rewards collective cooperation

### 2. Robustness Against Exploitation
- **Conditional cooperation** prevents being a "sucker" against predominantly defecting populations
- **Threshold-based decisions** provide clear switching points based on group behavior

### 3. Forgiveness and Recovery
- **30% forgiveness rate** allows recovery from temporary breakdowns in cooperation
- Prevents permanent descent into mutual defection after single bad rounds
- Helps restart cooperative cycles

### 4. End-Game Adaptation
- **Lower threshold in final round** (40% vs 50%) acknowledges that some players may defect due to no future consequences
- Still maintains cooperative stance when reasonable cooperation exists

## Handling Edge Cases

### Small Groups (n=2,3)
- Strategy works identically; 50% threshold means cooperating when at least 1 other player cooperated

### High Multiplication Factor (k close to n)
- Strategy becomes more cooperative as public good becomes more valuable
- Forgiveness mechanism helps capture these high-value cooperative equilibria

### Low Multiplication Factor (k close to 1)
- Strategy becomes more defensive but still attempts cooperation
- Protects against losses when public good provides minimal benefit

### Variable Round Lengths
- Strategy adapts to any r > 1
- First and last round rules scale appropriately

## Expected Performance

This strategy should perform well because:
1. **Mutual Cooperation**: Achieves high payoffs when facing other cooperative strategies
2. **Exploitation Resistance**: Doesn't get consistently exploited by defecting strategies
3. **Recovery Capability**: Can rebuild cooperation after temporary setbacks
4. **Adaptive**: Responds appropriately to different group cooperation levels

The generous but conditional nature should create positive interactions with similarly minded cooperative strategies while maintaining reasonable performance against more exploitative approaches.
'''

description_COOPERATIVE_89 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to defection and capable of recovery. It balances being "nice" (never defecting first), "retaliatory" (responding to defection), and "forgiving" (allowing recovery from punishment cycles).

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Response
For each round t (where 2 ≤ t ≤ r-1):

```pseudocode
cooperation_rate_last_round = (number of cooperators in round t-1) / n

if cooperation_rate_last_round >= 0.5:
    action = C  // Maintain cooperation when majority cooperates
else:
    // Check for sustained low cooperation
    if t >= 3:
        cooperation_rate_last_two = (cooperators in t-1 + cooperators in t-2) / (2*n)
        if cooperation_rate_last_two < 0.3:
            action = D  // Defect against persistent defectors
        else:
            action = C  // Give benefit of doubt for recovering cooperation
    else:
        action = C  // Too early to judge, remain cooperative
```

### Final Round (r): Conditional Cooperation
```pseudocode
if cooperation_rate_in_round_r-1 >= 0.4:
    action = C  // Reward sustained cooperation even in final round
else:
    action = D  // Protect against end-game defection
```

## Key Features

### 1. Generous Threshold
- Cooperates as long as ≥50% of players cooperated in the previous round
- This accounts for the fact that even with some defectors, cooperation can still be profitable when k > 1

### 2. Sustained Defection Detection
- Only switches to defection when cooperation rate falls below 30% for two consecutive rounds
- Prevents overreaction to temporary defection spikes

### 3. Forgiveness Mechanism
- Immediately returns to cooperation when cooperation rate recovers above 50%
- Allows for recovery from punishment cycles

### 4. End-Game Protection
- Slightly more lenient threshold (40%) in the final round to reward consistent cooperators
- But still protects against clear end-game defection

## Strategic Advantages

1. **Cooperative Signal**: Starting with cooperation signals good intentions
2. **Majority Rule**: Supporting cooperation when it's the majority strategy encourages others to maintain cooperation
3. **Punishment Deterrent**: Switching to defection when cooperation collapses provides incentive for others to maintain cooperation
4. **Recovery Friendly**: Quick forgiveness prevents permanent breakdown of cooperation
5. **End-Game Aware**: Balances cooperation with protection against final-round exploitation

## Expected Performance

This strategy should perform well when:
- Other strategies are also cooperative or conditionally cooperative
- The group can establish early cooperation patterns
- The multiplication factor k makes cooperation profitable for the majority

It provides protection against:
- Pure defectors (by eventually switching to defection)
- End-game defection (through conditional final-round play)
- Noise in cooperation (through generous thresholds and forgiveness)

The strategy aims to be part of the cooperative equilibrium while having enough defensive mechanisms to avoid exploitation.
'''

description_COOPERATIVE_90 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Gradual Forgiveness"** (GTTGF).

## Strategy Overview

This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances cooperation with protection against defectors through a combination of reciprocity, forgiveness, and strategic defection.

## Core Decision Rules

### Round 1: Optimistic Start
- **Always cooperate** in the first round to signal cooperative intent

### Rounds 2 to r-1: Adaptive Cooperation
For each round t (where 2 ≤ t ≤ r-1):

1. **Calculate cooperation ratio** from previous round:
   ```
   coop_ratio = (number of cooperators in round t-1) / n
   ```

2. **Apply decision rule**:
   ```pseudocode
   if coop_ratio >= 0.5:
       cooperate()
   else if coop_ratio >= 0.3:
       cooperate_with_probability(0.7)  // Generous forgiveness
   else if round_number <= r/2:
       cooperate_with_probability(0.4)  // Early game patience
   else:
       defect()  // Protect against persistent defectors
   ```

### Final Round (Round r): Strategic Defection
- **Always defect** in the final round (no future retaliation possible)

## Key Features

### 1. Forgiveness Mechanism
- Maintains cooperation even when facing some defection (30-50% cooperation threshold)
- Uses probabilistic cooperation to avoid being completely predictable
- More forgiving in early rounds to allow cooperation to emerge

### 2. Protection Against Exploitation
- Switches to defection when cooperation falls below 30%
- Always defects in the final round to avoid being exploited
- Reduces forgiveness in later rounds when patterns are established

### 3. Cooperation Promotion
- Starts cooperatively to signal good intentions
- Rewards high cooperation with continued cooperation
- Gives second chances through probabilistic cooperation

## Pseudocode Implementation

```pseudocode
function decide_action(round_number, game_history):
    // First round: always cooperate
    if round_number == 1:
        return COOPERATE
    
    // Final round: always defect
    if round_number == total_rounds:
        return DEFECT
    
    // Calculate previous round statistics
    prev_round = game_history[round_number - 1]
    cooperators = count_cooperators(prev_round)
    coop_ratio = cooperators / n
    
    // Decision logic based on cooperation level
    if coop_ratio >= 0.5:
        return COOPERATE
    else if coop_ratio >= 0.3:
        return random_choice(COOPERATE: 0.7, DEFECT: 0.3)
    else if round_number <= total_rounds / 2:
        return random_choice(COOPERATE: 0.4, DEFECT: 0.6)
    else:
        return DEFECT
```

## Strategic Rationale

1. **Cooperative Foundation**: Starting with cooperation and maintaining it when others reciprocate maximizes collective welfare

2. **Robustness**: The strategy can't be easily exploited due to its willingness to defect when cooperation breaks down

3. **Adaptability**: Responds to the actual behavior of opponents rather than making fixed assumptions

4. **Tournament Effectiveness**: Performs well against both cooperative and competitive strategies by finding middle ground

This strategy should perform well in a tournament setting by:
- Establishing mutual cooperation with other cooperative strategies
- Avoiding prolonged exploitation by defective strategies  
- Maintaining reasonable payoffs across diverse opponent types
- Being neither too naive nor too aggressive
'''

description_COOPERATIVE_91 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Cooperative Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and attempt to establish a cooperative equilibrium from the beginning.

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = n/2  // Majority threshold
forgiveness_counter = 0
max_forgiveness = 2

for round t in [2, r-1]:
    cooperators_last_round = count_cooperators(t-1)
    
    if cooperators_last_round >= cooperation_threshold:
        action = COOPERATE
        forgiveness_counter = 0  // Reset forgiveness
    
    else if forgiveness_counter < max_forgiveness:
        action = COOPERATE  // Be forgiving
        forgiveness_counter += 1
    
    else:
        action = DEFECT  // Punish persistent non-cooperation
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
recent_cooperation_rate = count_cooperators_last_3_rounds() / (3 * n)

if recent_cooperation_rate >= 0.4:  // 40% cooperation threshold
    action = COOPERATE  // Reward consistent cooperators
else:
    action = DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Cooperative by Default
- Starts with cooperation to signal good intentions
- Maintains cooperation when others reciprocate
- Uses generous thresholds (majority rule rather than unanimous cooperation)

### 2. Forgiveness Mechanism
- Tolerates up to 2 consecutive rounds of low cooperation
- This prevents punishment spirals from temporary coordination failures
- Accounts for the fact that other AIs might have different but legitimate strategies

### 3. Majority-Based Threshold
- Cooperates when at least half the players cooperated in the previous round
- More lenient than requiring unanimous cooperation
- Recognizes that perfect coordination is unlikely without communication

### 4. End-Game Protection
- Evaluates recent cooperation trends in the final round
- Cooperates if there's been reasonable cooperation (40% threshold over last 3 rounds)
- Protects against exploitation while still rewarding genuine cooperators

## Handling Edge Cases

### Very Small Groups (n=2,3)
- Strategy remains the same but becomes more sensitive to individual actions
- Forgiveness mechanism is crucial in small groups to avoid deadlock

### Very Large Groups (n>>6)
- Majority threshold scales naturally
- Individual impact is smaller, so strategy focuses on group trends

### Short Games (r=2,3)
- Forgiveness mechanism has less time to work
- Strategy becomes more immediately responsive to group behavior

### High/Low Multiplication Factor
- Strategy is parameter-agnostic and works regardless of k value
- Cooperation incentives are built into the game structure through k

## Rationale

This strategy embodies cooperative principles while being strategically sound:

1. **Cooperative Spirit**: Always starts cooperatively and gives others multiple chances
2. **Reciprocity**: Responds to group cooperation levels rather than punishing individual defectors
3. **Resilience**: Forgiveness prevents accidental punishment spirals
4. **Protection**: Guards against systematic exploitation while maintaining cooperative intent
5. **Adaptability**: Works across different parameter values and group sizes

The strategy assumes other AI agents are rational and potentially cooperative, but doesn't assume perfect coordination. It's designed to work well with other cooperative strategies while protecting against purely selfish ones.
'''

description_COOPERATIVE_92 = '''
# Generous Tit-for-Tat with Majority Threshold (GTMT)

## Strategy Overview
This strategy balances cooperation with protection against exploitation by using a majority-based threshold system with built-in forgiveness mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Always COOPERATE** in the first round
- Rationale: Establish cooperative intent and test the waters

### Rounds 2 to r-1: Conditional Cooperation
Use the **Majority Threshold Rule**:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n
threshold = 0.5

if cooperation_rate >= threshold:
    action = COOPERATE
else:
    // Generous forgiveness: cooperate with probability 0.2
    if random() < 0.2:
        action = COOPERATE
    else:
        action = DEFECT
```

### Round r (Final Round): Strategic Defection
- **Always DEFECT** in the final round
- Rationale: No future rounds to maintain reputation, maximize immediate payoff

## Key Features

### 1. Majority Threshold Logic
- Cooperate when ≥50% of players cooperated in the previous round
- This creates a natural tipping point that encourages collective cooperation
- Protects against being exploited when cooperation is minority behavior

### 2. Generous Forgiveness
- Even when majority defected, still cooperate 20% of the time
- Prevents getting stuck in mutual defection spirals
- Allows recovery from temporary downturns in cooperation

### 3. Adaptive Responsiveness
- Strategy automatically adjusts to the cooperation level of the group
- Works well with both highly cooperative and mixed populations
- Doesn't require complex opponent modeling

## Edge Case Handling

### First Round
- Always cooperate to signal cooperative intent
- Avoids chicken-and-egg problem of conditional strategies

### Last Round
- Always defect for optimal payoff
- Standard end-game reasoning applies

### Tie Situations
- When exactly 50% cooperated: threshold is met, so COOPERATE
- This bias toward cooperation helps maintain collective welfare

## Strategic Rationale

### Why This Strategy Works:
1. **Collective Efficiency**: Encourages outcomes where cooperation rate ≥50%, which are socially optimal
2. **Exploitation Protection**: Won't cooperate when clearly being taken advantage of
3. **Recovery Mechanism**: Generous forgiveness allows escape from defection cycles
4. **Simple Implementation**: Easy to understand and implement reliably

### Expected Performance:
- **Against cooperative strategies**: Achieves high mutual cooperation
- **Against mixed strategies**: Maintains reasonable cooperation while protecting downside
- **Against exploitative strategies**: Limits losses while occasionally testing for cooperation recovery

This strategy strikes an optimal balance between being "nice" (cooperative by default), "provocable" (punishes widespread defection), "forgiving" (allows recovery), and "clear" (simple, predictable rules that other cooperative strategies can recognize and reciprocate).
'''

description_COOPERATIVE_93 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to build and maintain cooperation by following the cooperative majority while being forgiving of occasional defections. It balances optimism about cooperation with pragmatic responses to sustained defection.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- **Rationale:** Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = ceil(n/2)  // Majority threshold
forgiveness_window = 3             // Rounds to "forget" past defections

// Calculate recent cooperation rate
recent_cooperators = count_cooperators_in_last_round()

// Check for sustained defection pattern
sustained_defectors = count_players_who_defected_last_X_rounds(forgiveness_window)
if sustained_defectors >= n/2:
    return DEFECT  // Protect against exploitation
    
// Follow cooperative majority
if recent_cooperators >= cooperation_threshold:
    return COOPERATE
else:
    // Conditional cooperation: try to rebuild cooperation
    if recent_cooperators >= ceil(n/3):  // Some cooperation exists
        return COOPERATE  // Help rebuild
    else:
        return DEFECT     // Too few cooperators
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
// Even in last round, maintain cooperation if others are cooperative
recent_cooperators = count_cooperators_in_last_round()
if recent_cooperators >= ceil(n/2):
    return COOPERATE  // Reward sustained cooperation
else:
    return DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Majority Following with Forgiveness
- Cooperate when at least half the players cooperated in the previous round
- Use a "forgiveness window" to not hold grudges indefinitely
- This encourages cooperation while protecting against systematic exploitation

### 2. Rebuilding Mechanism
- When cooperation drops below majority but isn't completely absent, still cooperate to help rebuild
- Only defect when cooperation is very low (< n/3 players cooperating)

### 3. Sustained Defection Protection
- If more than half the players have defected consistently over the forgiveness window, switch to defection
- This prevents being exploited by persistent free-riders

### 4. End-Game Cooperation
- Unlike purely selfish strategies, maintains cooperation in the final round if others are cooperating
- Rewards groups that have maintained cooperation throughout

## Edge Case Handling

- **First Round:** Always cooperate to signal cooperative intent
- **Small Groups (n=2,3):** Thresholds automatically adjust (majority = 1 or 2)
- **High Defection:** Switches to defection when exploitation risk is high
- **Tie Situations:** Err on the side of cooperation when exactly at threshold

## Strategic Rationale

This strategy is designed to:
1. **Build Trust:** Start cooperatively and reward cooperation
2. **Be Forgiving:** Don't punish occasional defections harshly
3. **Avoid Exploitation:** Protect against persistent free-riders
4. **Encourage Reciprocity:** Make cooperation contingent on others' cooperation
5. **Maximize Group Welfare:** Prioritize outcomes where everyone benefits from the public good

The strategy recognizes that in a public goods game, mutual cooperation is the Pareto optimal outcome, but requires mechanisms to prevent exploitation while encouraging cooperation to emerge and persist.
'''

description_COOPERATIVE_94 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It combines initial cooperation, reciprocity, forgiveness, and endgame cooperation.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative norm from the start.

### Rounds 2 to (r-2): Conditional Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: Even if majority defected last round, cooperate with probability based on cooperation history

**Detailed Logic**:
```pseudocode
Let prev_cooperators = number of players who played C in round (t-1)
Let majority_threshold = ceil(n/2)

IF prev_cooperators >= majority_threshold THEN
    action = C
ELSE
    // Calculate historical cooperation rate
    total_possible_cooperations = (t-2) * n  // excluding current round
    total_actual_cooperations = sum of all C plays in rounds 1 to (t-1)
    historical_coop_rate = total_actual_cooperations / total_possible_cooperations
    
    IF historical_coop_rate >= 0.4 THEN
        action = C  // Be forgiving if there's been reasonable cooperation
    ELSE
        action = D  // Protect against persistent defection
    END IF
END IF
```

### Round (r-1): Generous Cooperation
- **Action**: C
- **Rationale**: Signal continued cooperative intent even near the end, encouraging others not to defect early.

### Round r (Final Round): Always Cooperate
- **Action**: C
- **Rationale**: Maintain cooperative reputation and avoid triggering retaliatory cycles that could spill over if players meet again.

## Key Features

### 1. Majority-Based Reciprocity
- Responds to the collective behavior rather than individual players
- More stable than strict tit-for-tat in multi-player settings
- Majority threshold prevents single defector from derailing cooperation

### 2. Historical Forgiveness
- Uses long-term cooperation history to decide whether to forgive recent defections
- Threshold of 40% historical cooperation allows for some defection while maintaining cooperative stance
- Prevents permanent breakdown from temporary coordination failures

### 3. Endgame Cooperation
- Cooperates in final two rounds to avoid endgame unraveling
- Signals trustworthiness and long-term thinking
- May encourage others to maintain cooperation longer

### 4. Robustness Features
- **Against Always Defect**: Will eventually switch to defection if cooperation rate stays low
- **Against Exploiters**: Forgiveness is conditional on reasonable historical cooperation
- **Against Coordination Failures**: Majority rule prevents single mistakes from causing breakdowns

## Expected Behavior Patterns

1. **With Other Cooperators**: Establishes immediate mutual cooperation and maintains it throughout
2. **With Mixed Strategies**: Adapts to the group's cooperation level while encouraging higher cooperation
3. **With Mostly Defectors**: Eventually protects itself while still offering opportunities for cooperation recovery

## Strategic Advantages

- **Clarity**: Simple majority rule is easy for other AIs to understand and reciprocate
- **Stability**: Doesn't overreact to single-round defections
- **Encouraging**: Rewards group cooperation and provides path back to cooperation
- **Self-Protection**: Has mechanisms to avoid exploitation while remaining fundamentally cooperative

This strategy balances the cooperative goal with practical considerations for a tournament environment where opponent strategies are unknown but likely include various levels of cooperation and defection.
'''

description_COOPERATIVE_95 = '''
# Cooperative Strategy: "Forgiving Majority with Endgame Cooperation"

## Core Philosophy
This strategy balances cooperation with protection against exploitation while maintaining a fundamentally cooperative stance throughout the game, including the final rounds.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Establish cooperative intent from the start

### Rounds 2 to r-2: Conditional Cooperation
- **Cooperate (C) if**: At least ⌊n/2⌋ players cooperated in the previous round
- **Defect (D) if**: Fewer than ⌊n/2⌋ players cooperated in the previous round
- **Rationale**: Follow the majority while being slightly more forgiving than a strict majority rule

### Rounds r-1 and r: Always Cooperate
- **Action**: C regardless of previous round outcomes
- **Rationale**: Signal long-term cooperative commitment and avoid endgame defection cascade

## Pseudocode

```
function decide_action(round_number, history, n, r):
    if round_number == 1:
        return C
    
    elif round_number <= r - 2:
        cooperators_last_round = count_cooperators(history, round_number - 1)
        majority_threshold = floor(n / 2)
        
        if cooperators_last_round >= majority_threshold:
            return C
        else:
            return D
    
    else:  // Final two rounds (r-1 and r)
        return C
```

## Strategy Justification

### 1. **Cooperative Foundation**
- Starts with cooperation to signal willingness to work together
- Ends with cooperation to maintain group welfare even when others might defect

### 2. **Adaptive Middle Game**
- Responds to group behavior: cooperates when cooperation is prevalent
- Uses majority threshold (⌊n/2⌋) rather than requiring unanimous cooperation, making it more forgiving
- Protects against being exploited by persistent defectors

### 3. **Endgame Cooperation**
- Unlike many strategies that defect in final rounds, this strategy maintains cooperation
- Helps prevent the backward induction problem where everyone defects expecting others to defect
- Maximizes total group welfare in final rounds

### 4. **Robustness Properties**
- **Against Always Defect**: Will defect in middle rounds but still contributes in first and last two rounds
- **Against Always Cooperate**: Will cooperate throughout the game, maximizing mutual benefit
- **Against Mixed Strategies**: Adapts based on observed cooperation levels
- **Against Tit-for-Tat variants**: Generally maintains cooperation if majority does

### 5. **Expected Performance**
- In groups with other cooperative strategies: Achieves high mutual cooperation
- In mixed groups: Balances exploitation protection with cooperation
- Against hostile groups: Limits losses while still contributing to group welfare in key rounds

This strategy is designed to foster cooperation while being resilient enough to survive in a competitive environment, making it suitable for a tournament setting while maintaining its fundamentally cooperative nature.
'''

description_COOPERATIVE_96 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with protective mechanisms.

## Core Decision Rules

### Round 1: Cooperative Start
- **Always cooperate** in the first round to signal cooperative intent

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
- **Cooperate if**: The majority of players (≥ ⌈n/2⌉) cooperated in the previous round
- **Defect if**: The majority of players (< ⌈n/2⌉) defected in the previous round
- **Forgiveness mechanism**: After defecting due to majority defection, return to cooperation if:
  - At least 2 rounds have passed since switching to defection, AND
  - The cooperation rate in the last round was ≥ 40%

### Final Round: Reciprocal Response
- **Cooperate if**: Personal cooperation rate over the game has been ≥ 60%
- **Defect otherwise**: To protect against final-round exploitation

## Pseudocode

```
Initialize:
    personal_coop_count = 0
    rounds_since_defection = 0
    
For round t = 1 to r:
    
    If t == 1:
        action = COOPERATE
        personal_coop_count += 1
        
    Else if t == r:  // Final round
        cooperation_rate = personal_coop_count / (r-1)
        If cooperation_rate >= 0.6:
            action = COOPERATE
        Else:
            action = DEFECT
            
    Else:  // Rounds 2 to r-1
        prev_cooperators = count_cooperators_in_round(t-1)
        majority_threshold = ceiling(n / 2)
        
        If prev_cooperators >= majority_threshold:
            action = COOPERATE
            rounds_since_defection += 1
            personal_coop_count += 1
            
        Else:
            // Check forgiveness condition
            prev_coop_rate = prev_cooperators / n
            If rounds_since_defection >= 2 AND prev_coop_rate >= 0.4:
                action = COOPERATE
                rounds_since_defection += 1
                personal_coop_count += 1
            Else:
                action = DEFECT
                rounds_since_defection = 0
                
    Execute action
```

## Strategic Rationale

### Cooperative Elements:
1. **Optimistic start**: Begins with cooperation to establish positive momentum
2. **Majority-based decisions**: Follows the group's general direction, supporting collective cooperation
3. **Forgiveness mechanism**: Gives second chances to prevent permanent punishment cycles
4. **High cooperation threshold**: Only requires 40% cooperation rate to forgive, encouraging recovery

### Protective Elements:
1. **Majority threshold**: Won't cooperate when being heavily exploited
2. **Delayed forgiveness**: Requires 2 rounds before forgiving to avoid being repeatedly exploited
3. **Final round protection**: Considers personal investment when deciding final action

### Edge Case Handling:
- **First round**: Always cooperative to signal intent
- **Last round**: Protects committed cooperators from exploitation while maintaining cooperation for those who've been reciprocated
- **Punishment cycles**: Forgiveness mechanism prevents permanent mutual defection
- **Mixed signals**: Uses percentage thresholds rather than absolute rules for flexibility

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones. It encourages collective cooperation while avoiding being a pure "sucker" that can be easily exploited.
'''

description_COOPERATIVE_97 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances cooperative intent with self-protection mechanisms.

## Strategy Description

### Decision Rules

**Round 1: Always Cooperate**
- Start with cooperation to signal cooperative intent
- This establishes a baseline for reciprocal behavior

**Rounds 2 to r-1: Conditional Cooperation with Forgiveness**
- **Primary Rule**: Cooperate if the majority of players cooperated in the previous round
- **Forgiveness Mechanism**: After defecting due to low cooperation, give the group one "second chance" by cooperating again
- **Streak Protection**: If cooperation has been mutual for 3+ consecutive rounds, continue cooperating even if cooperation drops slightly

**Final Round: Conditional Cooperation**
- Cooperate if cooperation rate in round r-1 was ≥ 50%
- This prevents pure end-game defection while maintaining cooperative stance

### Detailed Algorithm

```pseudocode
Initialize:
- forgiveness_used = False
- consecutive_coop_rounds = 0
- last_action = None

For round t:
  If t == 1:
    action = COOPERATE
  
  Elif t == r: // Final round
    cooperation_rate_last_round = count_cooperators(t-1) / n
    If cooperation_rate_last_round >= 0.5:
      action = COOPERATE
    Else:
      action = DEFECT
  
  Else: // Rounds 2 to r-1
    cooperation_rate_last_round = count_cooperators(t-1) / n
    
    // Update consecutive cooperation counter
    If cooperation_rate_last_round >= 0.5 AND last_action == COOPERATE:
      consecutive_coop_rounds += 1
    Else:
      consecutive_coop_rounds = 0
    
    // Main decision logic
    If cooperation_rate_last_round >= 0.5:
      action = COOPERATE
      forgiveness_used = False
    
    Elif consecutive_coop_rounds >= 3:
      // Streak protection - maintain cooperation briefly
      action = COOPERATE
      consecutive_coop_rounds = 0
    
    Elif cooperation_rate_last_round < 0.5 AND NOT forgiveness_used:
      // Give one second chance
      action = COOPERATE
      forgiveness_used = True
    
    Else:
      action = DEFECT
  
  last_action = action
  Return action
```

## Key Features

### 1. Cooperative Orientation
- Always starts with cooperation
- Gives multiple chances for cooperation to emerge
- Maintains cooperation when others reciprocate

### 2. Reciprocity Mechanism
- Responds to the group's overall cooperation level
- Uses majority threshold (50%) to determine group intent
- Avoids punishing minor fluctuations in cooperation

### 3. Forgiveness System
- Provides one "second chance" after defection becomes necessary
- Prevents permanent breakdown from temporary setbacks
- Resets forgiveness opportunity when cooperation returns

### 4. Streak Protection
- Maintains cooperation momentum when established
- Prevents breaking cooperative chains due to single-round dips
- Balances stability with responsiveness

### 5. End-Game Handling
- Avoids naive final-round defection
- Maintains cooperative stance if group has been cooperative
- Protects against end-game exploitation while rewarding sustained cooperation

## Strategic Rationale

This strategy is designed to:
- **Establish Cooperation**: Clear cooperative signals from the start
- **Sustain Cooperation**: Reward and maintain cooperative equilibria
- **Handle Defection**: Respond proportionally to group defection without overreacting
- **Recover from Setbacks**: Built-in mechanisms to restore cooperation after temporary breakdowns
- **Balance Risk**: Protect against systematic exploitation while maximizing cooperative outcomes

The strategy assumes that other LLM-generated strategies will likely have similar cooperative orientations and will respond positively to clear cooperative signals and reciprocal behavior.
'''

description_COOPERATIVE_98 = '''
# Conditional Cooperation with Forgiveness Strategy

## Core Philosophy
This strategy aims to foster and maintain cooperation while being resilient against exploitation. It balances the cooperative ideal with practical defenses against defectors.

## Strategy Description

### Primary Decision Rule: Conditional Cooperation
- **Cooperate** if the cooperation rate in the previous round was ≥ 50%
- **Defect** if the cooperation rate in the previous round was < 50%

### Edge Case Handling

1. **First Round**: Always **Cooperate** (optimistic start)

2. **Last Round**: **Defect** (standard game theory prediction - no future to incentivize cooperation)

3. **Second-to-Last Round**: Apply normal conditional cooperation rule (ignore last-round defection incentives)

## Detailed Logic

```pseudocode
function decide_action(round_number, history):
    // Last round: defect (no future consequences)
    if round_number == total_rounds:
        return DEFECT
    
    // First round: cooperate optimistically
    if round_number == 1:
        return COOPERATE
    
    // All other rounds: conditional cooperation
    previous_round = history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / total_players
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    else:
        return DEFECT
```

## Strategic Rationale

### Strengths
1. **Promotes Cooperation**: Rewards collective cooperation by continuing to cooperate when others do
2. **Punishes Defection**: Withdraws cooperation when the group fails to maintain adequate cooperation levels
3. **Forgiveness**: Uses a threshold rather than requiring unanimous cooperation, allowing for some defection without triggering punishment
4. **Simplicity**: Clear, predictable rules that other cooperative strategies can learn and adapt to

### Threshold Justification (50%)
- **Balanced**: Not too strict (which could lead to cooperation collapse from minor defections) nor too lenient (which could be exploited)
- **Democratic**: Majority-rule principle
- **Robust**: Can maintain cooperation even with significant minority defection

### Response to Common Strategies
- **Against Always Cooperate**: Maintains mutual cooperation
- **Against Always Defect**: Quickly identifies and responds by defecting
- **Against Tit-for-Tat variants**: Can establish cooperation if the group reaches critical mass
- **Against other conditional cooperators**: Likely to converge on mutual cooperation

## Expected Dynamics
1. **Early rounds**: Optimistic cooperation attempt
2. **Middle rounds**: Adaptation based on group behavior - either stable cooperation or defensive defection
3. **Final round**: Strategic defection while others may also defect

This strategy aims to be a "good citizen" that encourages cooperation while protecting against exploitation, making it suitable for a tournament environment with diverse strategic approaches.
'''

description_COOPERATIVE_99 = '''
# Adaptive Cooperative Strategy: "Generous Tit-for-Tat with Group Momentum"

## Core Philosophy
This strategy aims to foster and maintain cooperation while being resilient to exploitation. It combines generous forgiveness with adaptive responses based on group cooperation levels.

## Strategy Description

### Decision Rules

**Round 1: Cooperative Opening**
- Always cooperate (C) in the first round to signal cooperative intent

**Rounds 2 to r-1: Adaptive Response**
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_last_action = my_action_previous_round

if cooperation_rate >= 0.6:
    // High cooperation - maintain momentum
    action = C
    
else if cooperation_rate >= 0.3:
    // Moderate cooperation - generous tit-for-tat
    if my_last_action == C and I_was_exploited_last_round:
        // Forgive with 70% probability
        action = random_choice([C, D], weights=[0.7, 0.3])
    else:
        action = C
        
else:
    // Low cooperation - defensive but not completely hostile
    if cooperation_rate < 0.2 and rounds_remaining > 3:
        // Very low cooperation, but not near end
        action = D
    else:
        // Give cooperation another chance
        action = random_choice([C, D], weights=[0.4, 0.6])
```

**Final Round (Round r): Conditional Cooperation**
```pseudocode
if cooperation_rate_last_round >= 0.5:
    action = C  // Reward good group behavior
else:
    action = D  // No future to build on
```

### Key Components

**1. Group Momentum Tracking**
- Monitor overall cooperation rate each round
- Weight recent cooperation more heavily than distant past
- Distinguish between declining vs. improving cooperation trends

**2. Exploitation Detection**
```pseudocode
I_was_exploited_last_round = (
    my_last_action == C AND 
    cooperation_rate_last_round < 0.5
)
```

**3. Generous Forgiveness**
- Don't immediately retaliate for single defections
- Use probabilistic responses to avoid predictable punishment
- Maintain cooperation bias when group shows reasonable cooperation

**4. End-Game Handling**
- In final round, base decision on recent group behavior
- Avoid the typical end-game defection cascade by rewarding cooperation
- Don't cooperate in final round if group has been consistently uncooperative

## Strategic Rationale

**Cooperative Focus:**
- Starts cooperatively to establish good intentions
- Maintains cooperation bias throughout most of the game
- Rewards group cooperation even in final round

**Exploitation Resistance:**
- Doesn't blindly cooperate when consistently exploited
- Uses probabilistic responses to avoid being predictably exploitable
- Becomes more defensive when cooperation rates are very low

**Group Dynamics:**
- Recognizes that individual punishment may not be effective in n-player games
- Focuses on overall group cooperation levels rather than individual player tracking
- Attempts to maintain positive momentum when it exists

**Adaptability:**
- Adjusts strategy based on observed group behavior
- Balances between forgiveness and self-protection
- Considers remaining rounds when making defensive decisions

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones, making it suitable for a tournament environment where opponent strategies are unknown.
'''

description_COOPERATIVE_100 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to foster cooperation while protecting against exploitation. It starts cooperatively, reciprocates the general cooperation level of others, but includes forgiveness mechanisms to recover from coordination failures.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This would be the second consecutive defection, AND
- The cooperation rate in the round before last was ≥ 30%

**Mathematical Expression**:
```
Let coop_rate(t) = (number of cooperators in round t) / n

Round t decision:
IF coop_rate(t-1) ≥ 0.5:
    Action = C
ELSE IF (my_action(t-1) = D) AND (coop_rate(t-2) ≥ 0.3):
    Action = C  // Forgiveness
ELSE:
    Action = D
```

### Final Round: Conditional Cooperation
- **Action**: C if cooperation rate in round r-1 was ≥ 40%
- **Action**: D otherwise
- **Rationale**: Slightly lower threshold for final round to account for end-game effects, but still reward cooperative groups

## Pseudocode

```python
def decide_action(round_num, game_history, my_history):
    # Round 1: Always cooperate
    if round_num == 1:
        return 'C'
    
    # Get cooperation rate from previous round
    prev_coop_rate = count_cooperators(game_history[-1]) / n
    
    # Final round: lower threshold
    if round_num == r:
        return 'C' if prev_coop_rate >= 0.4 else 'D'
    
    # Main strategy (rounds 2 to r-1)
    if prev_coop_rate >= 0.5:
        return 'C'
    
    # Forgiveness mechanism
    if (round_num >= 3 and 
        my_history[-1] == 'D' and 
        count_cooperators(game_history[-2]) / n >= 0.3):
        return 'C'
    
    return 'D'
```

## Strategic Rationale

### Cooperation Promotion
1. **Optimistic Start**: Always cooperating first signals good intentions
2. **Majority Rule**: Following the majority creates incentives for others to cooperate
3. **Forgiveness**: Prevents permanent breakdown from temporary coordination failures

### Exploitation Protection
1. **Responsive Defection**: Defects when cooperation rate is low
2. **Limited Forgiveness**: Won't continuously forgive chronic defectors
3. **End-game Awareness**: Slightly more cautious in final round

### Game Theory Alignment
- **Nash Equilibrium Consideration**: In a world of similar strategies, mutual cooperation emerges as stable
- **Subgame Perfect**: The strategy is optimal given beliefs about opponent behavior
- **Evolutionary Stable**: Can resist invasion by pure defectors while outperforming them in groups

## Handling Edge Cases

### Small Groups (n=2,3)
- Strategy works identically; majority rule becomes more sensitive

### High Multiplication Factor (k close to n)
- Strategy remains unchanged; higher k makes cooperation more attractive for everyone

### Long Games (large r)
- Forgiveness mechanism becomes more valuable for maintaining long-term cooperation

### Single Cooperator Scenarios
- If I'm the only cooperator for 2+ consecutive rounds, I'll defect until others show renewed cooperation (≥30% threshold)

This strategy balances the cooperative imperative with practical considerations about tournament dynamics, aiming to achieve high mutual payoffs when facing other cooperative strategies while avoiding exploitation by purely selfish ones.
'''

description_COOPERATIVE_101 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while being robust against exploitation. It recognizes that cooperation is mutually beneficial but requires mechanisms to encourage reciprocity and discourage free-riding.

## Decision Rules

### Round 1 (Initial Move)
**Always COOPERATE**
- Establishes cooperative intent
- Signals willingness to contribute to collective welfare
- Provides information about strategy type to other players

### Rounds 2 to r-1 (Middle Rounds)
**COOPERATE if:**
- At least ⌈n/2⌉ players cooperated in the previous round, OR
- At least ⌈n/2⌉ players cooperated in the majority of previous rounds

**DEFECT if:**
- Fewer than ⌈n/2⌉ players cooperated in the previous round, AND
- Fewer than ⌈n/2⌉ players cooperated in the majority of previous rounds

### Round r (Final Round)
**COOPERATE if:**
- At least ⌈(2n)/3⌉ players cooperated in round r-1 (higher threshold for final round)

**DEFECT if:**
- Fewer than ⌈(2n)/3⌉ players cooperated in round r-1

## Pseudocode

```
Strategy: Forgiving_Majority_Follower

Initialize:
    cooperation_history = []
    round_count = 0

For each round t:
    round_count += 1
    
    if round_count == 1:
        action = COOPERATE
        
    elif round_count == total_rounds:  // Final round
        last_round_cooperators = count_cooperators(previous_round)
        threshold = ceil((2 * n) / 3)
        action = COOPERATE if last_round_cooperators >= threshold else DEFECT
        
    else:  // Middle rounds
        last_round_cooperators = count_cooperators(previous_round)
        majority_threshold = ceil(n / 2)
        
        // Check recent cooperation
        recent_cooperation = (last_round_cooperators >= majority_threshold)
        
        // Check historical cooperation pattern
        if len(cooperation_history) > 1:
            historical_cooperation = calculate_historical_majority(cooperation_history)
        else:
            historical_cooperation = recent_cooperation
            
        action = COOPERATE if (recent_cooperation OR historical_cooperation) else DEFECT
    
    // Record outcome for future reference
    cooperation_history.append(count_cooperators(current_round))
    
    return action
```

## Strategy Rationale

### 1. **Cooperative Foundation**
- Starts with cooperation to signal good intentions
- Uses majority-based thresholds rather than requiring universal cooperation
- Maintains cooperative stance when sufficient reciprocity exists

### 2. **Punishment Mechanism**
- Defects when cooperation falls below majority threshold
- Prevents exploitation by free-riders
- Uses both recent and historical information to avoid over-reaction to temporary defections

### 3. **Forgiveness Element**
- Returns to cooperation once majority cooperation is restored
- Considers historical patterns, not just immediate previous round
- Prevents permanent defection cycles

### 4. **End-Game Handling**
- Higher threshold (2/3 majority) for final round cooperation
- Accounts for potential end-game defection incentives
- Still maintains cooperative stance if strong cooperation signal exists

### 5. **Robustness Features**
- Works with any n ≥ 2 (majority threshold scales appropriately)
- Handles edge cases (small groups, varying cooperation levels)
- Balances exploitation protection with cooperation maintenance

## Expected Performance

This strategy should perform well against:
- **Other cooperative strategies**: Mutual cooperation leading to optimal outcomes
- **Mixed populations**: Maintains cooperation with sufficient reciprocators
- **Moderate defectors**: Punishment discourages exploitation while forgiveness allows return to cooperation

The strategy may be vulnerable to:
- **Predominantly defecting populations**: Will eventually defect to protect against exploitation
- **Coordination failures**: May struggle if cooperation threshold is barely missed repeatedly

However, given the tournament context with other LLM-generated strategies (likely including cooperative approaches), this balanced strategy should achieve good collective outcomes while protecting against exploitation.
'''

description_COOPERATIVE_102 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being nice (cooperative by default), retaliatory (punishing defectors), and forgiving (allowing recovery from punishment cycles).

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = count_cooperators_last_round / n
    
    if cooperation_rate ≥ 0.5:
        // Majority cooperated - reciprocate cooperation
        action = C
    else if cooperation_rate ≥ 0.3:
        // Moderate cooperation - be forgiving with probability
        action = C with probability 0.7, D with probability 0.3
    else:
        // Low cooperation - mostly defect but stay somewhat forgiving
        action = C with probability 0.2, D with probability 0.8
```

### Round r (Final Round): Conditional Cooperation
```pseudocode
For final round r:
    cooperation_rate_last_round = count_cooperators_last_round / n
    average_cooperation_rate = total_cooperators_all_rounds / ((r-1) * n)
    
    if average_cooperation_rate ≥ 0.6:
        // High overall cooperation - reward with final cooperation
        action = C
    else if cooperation_rate_last_round ≥ 0.5:
        // Recent cooperation despite low overall rate - give benefit of doubt
        action = C
    else:
        // Low cooperation throughout - protect against final exploitation
        action = D
```

## Key Features

### 1. **Graduated Response**
- Rather than binary retaliation, responds proportionally to the level of cooperation observed
- Maintains some cooperation even when facing moderate defection to encourage recovery

### 2. **Forgiveness Mechanism**
- Never completely gives up on cooperation (always maintains at least 20% cooperation probability)
- Quickly returns to full cooperation when others show renewed cooperative behavior

### 3. **Endgame Handling**
- Final round decision considers both recent behavior and overall game history
- Rewards sustained cooperation but protects against end-game exploitation

### 4. **Robustness Features**
- **Against Always Defect**: Gradually reduces cooperation but maintains some to test for strategy changes
- **Against Alternating Strategies**: Responds to average cooperation levels rather than single-round fluctuations
- **Against Trigger Strategies**: Forgiveness mechanism allows recovery from punishment phases

## Strategic Rationale

1. **Cooperative Signaling**: Starting with cooperation and maintaining positive cooperation probabilities signals willingness to achieve mutual benefit

2. **Adaptive Retaliation**: Graduated response prevents exploitation while avoiding overly harsh punishment that could spiral into mutual defection

3. **Recovery Incentives**: By never dropping to zero cooperation probability, the strategy provides pathways for opponents to rebuild cooperative relationships

4. **Tournament Effectiveness**: Against a mix of strategies, this approach should:
   - Achieve high mutual payoffs with other cooperative strategies
   - Avoid severe exploitation by maintaining adaptive defenses
   - Provide opportunities for mixed strategies to find stable cooperative equilibria

This strategy embodies cooperative principles while being strategically sound for tournament play against diverse opponents with unknown behavioral patterns.
'''

description_COOPERATIVE_103 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperativeness with self-protection through a reputation-based system.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Signal cooperative intent from the start to encourage mutual cooperation

### Rounds 2 to r-1: Reputation-Based Cooperation
For each round t (where 2 ≤ t ≤ r-1):

1. **Calculate each player's cooperation rate** from rounds 1 to t-1:
   ```
   cooperation_rate[j] = (number of times player j cooperated) / (t-1)
   ```

2. **Classify players into categories**:
   - **Cooperators**: cooperation_rate[j] ≥ 0.7
   - **Defectors**: cooperation_rate[j] < 0.4
   - **Mixed**: 0.4 ≤ cooperation_rate[j] < 0.7

3. **Decision rule**:
   ```pseudocode
   cooperator_count = count(players with cooperation_rate ≥ 0.7)
   total_players = n
   
   if (cooperator_count / total_players) ≥ 0.5:
       return C  // Cooperate when majority are cooperators
   else if (cooperator_count / total_players) ≥ 0.3:
       // Be generous - cooperate with some probability based on environment
       if random() < 0.7:
           return C
       else:
           return D
   else:
       return D  // Defect when facing mostly defectors
   ```

### Round r (Final Round): Conditional Cooperation
In the last round, apply a modified rule to account for end-game effects:

```pseudocode
cooperator_count = count(players with cooperation_rate ≥ 0.6)  // Slightly lower threshold
if (cooperator_count / total_players) ≥ 0.6:
    return C  // Cooperate if strong cooperative environment
else:
    return D  // Defect to avoid exploitation in final round
```

## Edge Case Handling

### First Round
- Always cooperate to signal good intentions and attempt to establish a cooperative equilibrium from the start.

### Early Rounds (2-3)
- Be more generous in cooperation thresholds since sample sizes are small
- Use threshold of 0.5 instead of 0.7 for classifying cooperators in rounds 2-3

### Final Round
- Slightly more defensive due to end-game effects
- Higher threshold (0.6) for maintaining cooperation

### All-Defection Scenarios
- If all other players defect for 2 consecutive rounds, switch to defection but attempt cooperation again after 2 rounds to test if cooperation can be re-established

### Recovery Mechanism
```pseudocode
if (current_round > 4 AND all_players_defected_last_2_rounds):
    if (current_round % 3 == 0):  // Test cooperation every 3 rounds
        return C  // Attempt to restart cooperation
    else:
        return D
```

## Key Features

1. **Generous**: Starts cooperative and gives others benefit of doubt
2. **Forgiving**: Uses cooperation rates rather than recent actions only
3. **Adaptive**: Adjusts behavior based on the overall cooperative climate
4. **Defensive**: Protects against systematic exploitation
5. **Recovery-oriented**: Periodically attempts to re-establish cooperation even after breakdowns

## Strategic Rationale

- **Maximizes mutual benefit** when facing other cooperative strategies
- **Avoids exploitation** by tracking long-term behavior patterns
- **Encourages cooperation** through generous initial moves and forgiveness
- **Handles mixed populations** by adapting to the overall cooperation level
- **Maintains simplicity** while being robust to various opponent types

This strategy should perform well against other cooperative strategies while providing reasonable protection against exploitation, making it suitable for a tournament environment with diverse opponents.
'''

description_COOPERATIVE_104 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through conditional reciprocity.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

**Rounds 2 to r-1 (Main Game):**
- Maintain a "cooperation threshold" based on the proportion of cooperators in the previous round
- COOPERATE if: `(cooperators_last_round / n) >= 0.5`
- DEFECT if: `(cooperators_last_round / n) < 0.5`
- **Forgiveness Mechanism**: If you defected in the previous round due to low cooperation, but cooperation increased, return to cooperation immediately

**Round r (Final Round):**
- Apply same rule as main game rounds
- Rationale: While there's temptation to defect in the final round, maintaining consistency may be rewarded if opponents use similar reasoning

### Pseudocode

```python
def decide_action(round_number, game_history, n, r):
    if round_number == 1:
        return "C"  # Always cooperate first
    
    # Get cooperation count from previous round
    last_round_cooperators = count_cooperators(game_history[-1])
    cooperation_rate = last_round_cooperators / n
    
    # Main decision rule: cooperate if majority cooperated
    if cooperation_rate >= 0.5:
        return "C"
    else:
        return "D"

def count_cooperators(round_actions):
    return sum(1 for action in round_actions if action == "C")
```

### Detailed Logic

**Cooperation Threshold (50%):**
- If at least half the players cooperated in the previous round, continue cooperating
- This creates a stable focal point that rewards collective cooperation
- The threshold is neither too lenient (avoiding exploitation) nor too harsh (allowing recovery)

**Why This Strategy is Cooperative:**

1. **Optimistic Start**: Always begins with cooperation, signaling good intentions
2. **Reciprocal Cooperation**: Rewards group cooperation with continued cooperation
3. **Collective Punishment**: Only defects when the majority defects, maintaining group-oriented thinking
4. **Quick Forgiveness**: Returns to cooperation as soon as the group does, avoiding punishment spirals
5. **Consistent End Game**: Doesn't abandon cooperation in final rounds

**Handling Edge Cases:**

- **All players defect**: Will defect until cooperation emerges
- **Alternating cooperation**: Will track the most recent round's cooperation level
- **Gradual decline**: Will defect once cooperation drops below 50%, potentially encouraging recovery
- **Single defector**: Will continue cooperating as long as majority still cooperates

**Strategic Advantages:**

1. **Stable Equilibrium**: If most players use similar logic, creates a stable cooperative equilibrium
2. **Exploitation Resistance**: Won't be consistently exploited by free-riders
3. **Recovery Capability**: Can bounce back from temporary cooperation breakdowns
4. **Clear Signaling**: Strategy is transparent and predictable, encouraging others to cooperate

This strategy embodies cooperative principles while maintaining enough self-protection to be viable against mixed populations of cooperative and strategic players.
'''

description_COOPERATIVE_105 = '''
# Adaptive Cooperative Strategy: "Graduated Reciprocator"

## Core Philosophy
This strategy aims to foster and maintain cooperation while being resilient to exploitation. It starts cooperatively, adapts to group dynamics, and includes forgiveness mechanisms to recover from punishment cycles.

## Strategy Components

### 1. Decision Rules

```pseudocode
STRATEGY: Graduated_Reciprocator

INITIALIZE:
  cooperation_threshold = 0.5  // Minimum fraction needed to cooperate
  punishment_rounds = 0        // Counter for punishment phase
  forgiveness_interval = 3     // Rounds between forgiveness attempts
  
FOR each round t:
  IF t == 1:
    ACTION = COOPERATE  // Always start cooperatively
    
  ELSE IF punishment_rounds > 0:
    punishment_rounds -= 1
    ACTION = DEFECT
    
  ELSE:
    cooperation_rate = calculate_recent_cooperation_rate(last_3_rounds)
    
    IF cooperation_rate >= cooperation_threshold:
      ACTION = COOPERATE
      
    ELSE IF cooperation_rate >= 0.3:
      // Moderate defection: Give second chance
      IF t % forgiveness_interval == 0:
        ACTION = COOPERATE  // Periodic forgiveness attempt
      ELSE:
        ACTION = DEFECT
        
    ELSE:
      // High defection: Enter punishment phase
      punishment_rounds = 2
      ACTION = DEFECT
```

### 2. Edge Case Handling

**First Round (t=1):**
- Always COOPERATE to signal cooperative intent and test group dynamics

**Last Round (t=r):**
- Follow normal decision rules (no special endgame defection)
- This signals long-term cooperative intent and may encourage others to maintain cooperation

**Early Rounds (t=2,3):**
- Use available history but apply more lenient thresholds
- If round 2: cooperate if ≥33% cooperated in round 1
- If round 3: use average of rounds 1-2

**Information Shortage:**
- When calculating cooperation rates with insufficient history, weight recent rounds more heavily
- Use exponential decay: recent rounds count more than distant ones

### 3. Cooperative Alignment

**Cooperation Promotion:**
- Starts with cooperation to establish positive precedent
- Rewards group cooperation with continued cooperation
- Uses forgiveness attempts to break punishment cycles

**Group Welfare Focus:**
- Recognizes that mutual cooperation yields highest total welfare
- Balances individual protection against group benefit
- Avoids permanent defection that could collapse cooperation

**Adaptive Responsiveness:**
- Responds proportionally to group cooperation levels
- Distinguishes between temporary defection and systematic exploitation
- Maintains cooperation incentives through conditional strategies

### 4. Key Parameters Explained

- **cooperation_threshold (0.5):** Requires majority cooperation to maintain cooperative stance
- **punishment_rounds (2):** Brief punishment discourages defection without permanent retaliation
- **forgiveness_interval (3):** Regular forgiveness attempts prevent permanent punishment cycles
- **recent_cooperation_rate:** Uses last 3 rounds to balance responsiveness with stability

### 5. Strategic Rationale

This strategy is designed to:
1. **Establish cooperation** through initial cooperative moves
2. **Maintain cooperation** when others reciprocate
3. **Punish defection** proportionally to discourage exploitation
4. **Recover cooperation** through forgiveness mechanisms
5. **Adapt to group dynamics** rather than following rigid rules

The strategy recognizes that in a tournament setting, purely exploitative strategies will likely exist, but also assumes that cooperative strategies will be present. By being "nice" (starting cooperatively), "retaliatory" (punishing defection), and "forgiving" (attempting to restore cooperation), it aims to achieve high payoffs with other cooperative strategies while protecting against exploitation.
'''

description_COOPERATIVE_106 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always cooperate (C)
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability 0.2 (forgiveness)
- **Punishment**: If cooperation rate < 30% in the previous round, defect (unless forgiveness triggers)

### Final Round: Conditional Cooperation
- **Action**: Cooperate if cooperation rate in round r-1 was ≥ 40%
- **Rationale**: Slightly lower threshold to encourage final-round cooperation, but protect against widespread defection

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return C
    
    if round_number == total_rounds:
        cooperation_rate_prev = count_cooperators(history[round_number-1]) / n
        if cooperation_rate_prev >= 0.4:
            return C
        else:
            return D
    
    # Rounds 2 to r-1
    cooperation_rate_prev = count_cooperators(history[round_number-1]) / n
    
    if cooperation_rate_prev >= 0.5:
        return C
    elif cooperation_rate_prev < 0.3:
        if random() < 0.2:  # 20% forgiveness
            return C
        else:
            return D
    else:  # cooperation_rate between 0.3 and 0.5
        if random() < 0.2:  # 20% forgiveness
            return C
        else:
            return D
```

## Edge Case Handling

### First Round
- Always cooperate to establish good faith and potentially trigger reciprocal cooperation

### Last Round
- Use conditional cooperation with a lower threshold (40%) to balance end-game defection incentives while rewarding cooperative partners

### Unanimous Defection Scenarios
- If everyone defected in the previous round, still have a 20% chance of cooperating to attempt to restart cooperation

### High Cooperation Scenarios
- If cooperation rate is very high (≥80%), continue cooperating to maintain the beneficial equilibrium

## Strategic Rationale

1. **Cooperation Promotion**: Starting with cooperation and maintaining it when others reciprocate encourages collective benefit maximization

2. **Exploitation Protection**: The 50% threshold prevents being exploited by strategies that maintain just enough cooperation to extract maximum benefit

3. **Forgiveness Element**: The 20% forgiveness probability allows for recovery from coordination failures or temporary defections

4. **Graduated Response**: Different thresholds for different scenarios create nuanced responses rather than binary reactions

5. **End-Game Consideration**: The modified final-round strategy acknowledges changed incentives while still rewarding cooperative play

## Expected Performance

This strategy should perform well against:
- Other cooperative strategies (mutual cooperation)
- Tit-for-tat variants (reciprocal cooperation)
- Mixed strategies with moderate cooperation rates

It provides protection against:
- Pure defection strategies (through conditional cooperation)
- Exploitative strategies that rely on others' unconditional cooperation
- Strategies that attempt to free-ride on high cooperation rates

The forgiveness mechanism helps recover from coordination failures while the threshold-based decisions prevent systematic exploitation.
'''

description_COOPERATIVE_107 = '''
# Adaptive Cooperative Strategy: "Forgiving Majority"

## Core Philosophy
This strategy aims to establish and maintain cooperation by being initially optimistic, responsive to group behavior, and forgiving of occasional defections. It balances the cooperative ideal with practical considerations for sustaining cooperation in a multi-player environment.

## Decision Rules

### Round 1: Optimistic Start
**Action: COOPERATE**
- Begin with cooperation to signal cooperative intent
- Sets a positive tone and tests if others are similarly inclined

### Rounds 2 to r-1: Adaptive Cooperation
**Cooperate if ANY of the following conditions are met:**

1. **High Cooperation Threshold**: At least ⌈n/2⌉ players cooperated in the previous round
   - Rewards and encourages majority cooperation
   - Maintains cooperation when it's reasonably established

2. **Improvement Trend**: Number of cooperators increased from round t-2 to t-1
   - Encourages positive momentum
   - Forgives temporary dips if cooperation is recovering

3. **Forgiveness Window**: Only 1 round has passed since last high cooperation (≥⌈n/2⌉ cooperators)
   - Prevents immediate abandonment after a single bad round
   - Gives the group a chance to recover from coordination failures

**Otherwise: DEFECT**

### Final Round r: Conditional Cooperation
**Cooperate if:**
- At least ⌈2n/3⌉ players cooperated in round r-1, OR
- The group maintained ≥⌈n/2⌉ cooperation for at least 75% of previous rounds

**Otherwise: DEFECT**
- Higher threshold for final round cooperation prevents end-game exploitation
- Still rewards consistently cooperative groups

## Pseudocode

```
function decide_action(round, history):
    n = number_of_players
    r = total_rounds
    
    if round == 1:
        return COOPERATE
    
    if round == r:  // Final round
        last_round_cooperators = count_cooperators(history[round-1])
        if last_round_cooperators >= ceil(2*n/3):
            return COOPERATE
        
        total_high_coop_rounds = 0
        for t in range(1, r):
            if count_cooperators(history[t]) >= ceil(n/2):
                total_high_coop_rounds += 1
        
        if total_high_coop_rounds >= 0.75 * (r-1):
            return COOPERATE
        else:
            return DEFECT
    
    // Middle rounds (2 to r-1)
    last_cooperators = count_cooperators(history[round-1])
    
    // Condition 1: High cooperation threshold
    if last_cooperators >= ceil(n/2):
        return COOPERATE
    
    // Condition 2: Improvement trend (if round >= 3)
    if round >= 3:
        prev_cooperators = count_cooperators(history[round-2])
        if last_cooperators > prev_cooperators:
            return COOPERATE
    
    // Condition 3: Forgiveness window
    if round >= 3:
        for lookback in range(1, min(2, round-1)):
            if count_cooperators(history[round-1-lookback]) >= ceil(n/2):
                return COOPERATE
    
    return DEFECT
```

## Key Features

### 1. **Graduated Response**
- Doesn't immediately punish single defections
- Responds to trends rather than isolated incidents
- Maintains hope for cooperation recovery

### 2. **Majority-Based Logic**
- Recognizes that full cooperation is difficult to achieve
- Rewards and sustains "good enough" cooperation levels
- Adapts threshold based on group size

### 3. **Endgame Awareness**
- Higher standards for final round cooperation
- Prevents exploitation while still rewarding consistent cooperators
- Balances idealism with realism

### 4. **Forgiveness Mechanism**
- Gives groups multiple chances to return to cooperation
- Prevents spiral into mutual defection from temporary coordination failures
- Maintains cooperative stance longer than pure tit-for-tat approaches

## Expected Performance
This strategy should perform well against:
- Other cooperative strategies (mutual benefit)
- Mixed populations (can establish cooperation with willing partners)
- Strategies with occasional defection (forgiveness prevents breakdown)

It provides protection against pure defectors by eventually defecting when cooperation clearly fails, while maximizing opportunities for cooperative outcomes when possible.
'''

description_COOPERATIVE_108 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with self-protection mechanisms.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule: Cooperate if the cooperation rate in the previous round ≥ 50%**

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round >= 0.5:
    action = COOPERATE
else:
    action = DEFECT
```

**Forgiveness Mechanism:**
- If defecting due to low cooperation rate, return to cooperation after 1 round of punishment
- Track consecutive punishment rounds to avoid permanent defection spirals

```pseudocode
if currently_punishing and punishment_rounds >= 1:
    action = COOPERATE  // Attempt to restart cooperation
    reset punishment_counter
```

### Final Round (Round r): Conditional Loyalty
- **If cooperation rate in round r-1 ≥ 70%: COOPERATE**
- **Otherwise: DEFECT**

This prevents exploitation in the final round while rewarding consistently cooperative groups.

## Complete Strategy Logic

```pseudocode
Strategy: GenerousTitForTatWithForgiveness

Initialize:
    punishment_rounds = 0
    currently_punishing = false

For round t:
    if t == 1:
        return COOPERATE
    
    elif t == r:  // Final round
        cooperation_rate_previous = count_cooperators(t-1) / n
        if cooperation_rate_previous >= 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // Rounds 2 to r-1
        cooperation_rate_previous = count_cooperators(t-1) / n
        
        if currently_punishing:
            if punishment_rounds >= 1:
                currently_punishing = false
                punishment_rounds = 0
                return COOPERATE  // Forgiveness attempt
            else:
                punishment_rounds += 1
                return DEFECT
        
        else:  // Not currently punishing
            if cooperation_rate_previous >= 0.5:
                return COOPERATE
            else:
                currently_punishing = true
                punishment_rounds = 1
                return DEFECT
```

## Key Features

### 1. **Cooperative by Default**
- Starts with cooperation and returns to it whenever possible
- Uses generous threshold (50%) rather than requiring majority cooperation

### 2. **Proportional Response**
- Responds to group behavior rather than individual players
- Avoids targeting specific players, focusing on overall cooperation levels

### 3. **Forgiveness Mechanism**
- Limits punishment to 1 round to prevent defection spirals
- Always attempts to restart cooperation after punishment

### 4. **End-Game Protection**
- Higher threshold (70%) required for final round cooperation
- Prevents exploitation when there's no future interaction

### 5. **Resilience Features**
- Won't get trapped in permanent defection
- Adapts to the group's overall cooperative tendency
- Balances being exploitable with being too punitive

## Strategic Rationale

This strategy recognizes that in a public goods game:
- Mutual cooperation yields the highest collective payoff
- Individual defection can be tempting but reduces group welfare
- The repeated nature allows for reputation building and reciprocity
- Mixed populations require adaptive responses

The 50% threshold acknowledges that perfect cooperation may be unrealistic while still rewarding groups that maintain reasonable cooperation levels. The forgiveness mechanism ensures the strategy doesn't permanently abandon cooperation due to temporary setbacks or misunderstandings.
'''

description_COOPERATIVE_109 = '''
# Adaptive Cooperative Strategy: "Graduated Reciprocator"

## Core Philosophy
This strategy aims to foster cooperation while protecting against exploitation by adapting to the collective behavior of all players, not just individual interactions.

## Decision Rules

### Round 1: Optimistic Start
- **Always COOPERATE** in the first round
- Rationale: Signal cooperative intent and test the waters

### Rounds 2 to r-1: Adaptive Cooperation
Use a **cooperation threshold** system based on group cooperation rate:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n

if cooperation_rate >= 0.6:
    action = COOPERATE
elif cooperation_rate >= 0.3:
    if (my_last_action == COOPERATE and my_last_payoff >= average_payoff_if_all_defected):
        action = COOPERATE
    else:
        action = DEFECT
else:  # cooperation_rate < 0.3
    action = DEFECT
```

Where `average_payoff_if_all_defected = 1`

### Final Round: Conditional Cooperation
- If group cooperation rate in round r-1 was ≥ 0.5: **COOPERATE**
- Otherwise: **DEFECT**
- Rationale: Reward good group behavior even in the final round, but don't be exploited if cooperation has collapsed

## Key Features

### 1. Group-Based Assessment
- Monitors overall cooperation level rather than tracking individual players
- Responds to collective behavior patterns
- More robust against mixed populations of strategies

### 2. Graduated Response
- **High cooperation (≥60%)**: Always cooperate to maintain positive momentum
- **Medium cooperation (30-59%)**: Conditional cooperation based on whether cooperation is paying off
- **Low cooperation (<30%)**: Defect to avoid exploitation

### 3. Forgiveness Mechanism
- Strategy can return to cooperation if group behavior improves
- No permanent grudges against the entire group
- Allows recovery from defection spirals

### 4. Exploitation Protection
- Won't continue cooperating if consistently earning less than the "all defect" baseline
- Responds quickly to widespread defection
- Balances cooperation with self-preservation

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative precedent

### Early Rounds (rounds 2-3)
- More lenient thresholds initially to allow cooperation to establish

### Middle Rounds
- Full adaptive logic based on recent group performance

### Final Round
- Rewards sustained cooperation but protects against end-game defection

### Tie-Breaking
- When exactly at threshold values, slightly favor cooperation
- When cooperation rates are exactly 0.3 or 0.6, use the more cooperative option

## Strategic Rationale

1. **Cooperative Alignment**: Actively promotes group cooperation through positive reinforcement
2. **Adaptive**: Responds appropriately to different group compositions
3. **Exploitability Resistant**: Won't be systematically exploited by always-defect strategies
4. **Tournament Effective**: Performs well against diverse strategy populations
5. **Clear Logic**: Transparent decision-making based on observable group behavior

This strategy should perform well against other cooperative strategies while maintaining reasonable defense against exploitative ones, making it suitable for a mixed tournament environment.
'''

description_COOPERATIVE_110 = '''
# Cooperative Strategy: "Graduated Reciprocation with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances the cooperative goal with self-protection through measured responses to defection.

## Strategy Overview

The strategy operates in three phases:
1. **Establishment Phase**: Build trust and signal cooperative intent
2. **Maintenance Phase**: Reciprocate cooperation while deterring exploitation
3. **Endgame Phase**: Handle final rounds strategically

## Decision Rules

### Phase 1: Establishment (Rounds 1-3 or first 20% of rounds, whichever is smaller)
- **Round 1**: Always COOPERATE (signal cooperative intent)
- **Rounds 2-3**: COOPERATE if at least 30% of players cooperated in the previous round, otherwise DEFECT

### Phase 2: Maintenance (Middle rounds)
- **Cooperation Threshold**: COOPERATE if the cooperation rate in the previous round was ≥ 40%
- **Punishment Response**: If cooperation rate drops below 40%, DEFECT for one round, then return to cooperation assessment
- **Forgiveness Mechanism**: After punishing, immediately return to cooperation if others show willingness (≥ 30% cooperation rate)

### Phase 3: Endgame (Final 2 rounds)
- **Second-to-last round**: COOPERATE if cooperation rate in previous round ≥ 50%
- **Final round**: DEFECT (standard endgame logic, as cooperation cannot be rewarded)

## Pseudocode

```
function decide_action(round, history):
    total_rounds = r
    cooperation_rate_last_round = calculate_cooperation_rate(history, round-1)
    
    // Phase 1: Establishment
    if round == 1:
        return COOPERATE
    
    if round <= min(3, total_rounds * 0.2):
        if cooperation_rate_last_round >= 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    // Phase 3: Endgame
    if round == total_rounds:
        return DEFECT
    
    if round == total_rounds - 1:
        if cooperation_rate_last_round >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Phase 2: Maintenance
    if cooperation_rate_last_round >= 0.4:
        return COOPERATE
    else:
        // Check if we're in punishment mode
        if previous_action == DEFECT and cooperation_rate_last_round >= 0.3:
            return COOPERATE  // Forgiveness
        else:
            return DEFECT     // Punishment or continued defection
```

## Key Features

### 1. Cooperative Signaling
- Starts with cooperation to signal good intentions
- Uses graduated thresholds rather than strict tit-for-tat

### 2. Proportional Response
- Cooperation threshold (40%) is set below the break-even point for most parameter combinations
- This encourages cooperation even when not all players cooperate

### 3. Forgiveness Mechanism
- After punishing defection, quickly returns to cooperation when others show willingness
- Prevents permanent breakdown of cooperation due to temporary conflicts

### 4. Robustness Features
- **Anti-exploitation**: Won't be perpetually exploited by always-defect strategies
- **Error tolerance**: Doesn't permanently punish occasional defections
- **Endgame handling**: Recognizes that final round cooperation is irrational

### 5. Adaptive Thresholds
- Uses different cooperation thresholds for different phases
- Lower threshold (30%) for establishment and forgiveness
- Higher threshold (40%) for sustained cooperation
- Highest threshold (50%) for endgame cooperation

## Strategic Rationale

This strategy is designed to:
1. **Maximize mutual cooperation** by starting cooperatively and maintaining reasonable thresholds
2. **Avoid exploitation** by responding to low cooperation with temporary defection
3. **Recover from conflicts** through forgiveness mechanisms
4. **Handle diverse opponents** by using proportional rather than binary responses

The graduated approach means it can work well with other cooperative strategies while protecting against exploitation by aggressive strategies. The forgiveness mechanism helps maintain cooperation even when facing imperfect reciprocators or strategies that occasionally defect.
'''

description_COOPERATIVE_111 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness" (GTTF)**.

## Strategy Overview

This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances immediate cooperative intent with adaptive responses to others' behavior.

## Core Decision Rules

### Round 1: Cooperative Opening
- **Action: Always COOPERATE**
- Rationale: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Adaptive Cooperation
**Primary Rule**: Cooperate if the cooperation rate in the previous round was above a dynamic threshold.

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n
dynamic_threshold = max(0.3, (k-1)/(n-1))

if cooperation_rate_last_round >= dynamic_threshold:
    action = COOPERATE
else:
    // Forgiveness mechanism
    if consecutive_low_cooperation_rounds <= 2:
        action = COOPERATE  // Give benefit of doubt
    else:
        action = DEFECT     // Protect against exploitation
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
recent_cooperation_rate = average_cooperation_rate_last_3_rounds
if recent_cooperation_rate >= 0.5:
    action = COOPERATE  // Reward consistent cooperators
else:
    action = DEFECT     // Protect against end-game defection
```

## Key Features

### 1. Dynamic Threshold Calculation
The threshold adapts to game parameters:
- **Formula**: `max(0.3, (k-1)/(n-1))`
- **Logic**: Higher thresholds when cooperation is more valuable relative to group size
- **Example**: For n=6, k=2: threshold = max(0.3, 1/5) = 0.3 (30% cooperation needed)

### 2. Forgiveness Mechanism
- Tolerates up to 2 consecutive rounds of low cooperation
- Prevents premature abandonment of cooperation due to temporary coordination failures
- Balances trust with self-protection

### 3. Memory and Adaptation
- Tracks cooperation history over multiple rounds
- Uses recent trends (last 3 rounds) for final round decision
- Maintains counter of consecutive low-cooperation periods

## Edge Case Handling

### First Round
- Always cooperate to establish cooperative norm
- No history available, so default to optimistic approach

### Last Round
- Considers recent cooperation patterns rather than just immediate previous round
- Cooperates if there's evidence of sustained cooperation (≥50% recent rate)
- Defects against likely end-game defectors

### All Players Defecting
- Forgiveness mechanism provides 2-3 chances for recovery
- Eventually switches to defection if no improvement
- Can restart cooperation if others show renewed cooperative intent

### Mixed Cooperation Levels
- Dynamic threshold prevents exploitation while maintaining cooperation opportunity
- Responds proportionally to cooperation levels rather than binary all-or-nothing

## Strategic Rationale

1. **Cooperative Foundation**: Starts cooperatively and maintains cooperative bias
2. **Exploitation Resistance**: Dynamic threshold and forgiveness limits prevent being taken advantage of
3. **Recovery Capability**: Can restart cooperation if others demonstrate renewed intent
4. **Parameter Sensitivity**: Adapts decision-making to game economics (k/n ratio)
5. **End-Game Awareness**: Protects against final-round defection while rewarding consistent cooperators

This strategy should perform well against other cooperative strategies while defending against purely exploitative ones, making it robust for a tournament environment with diverse opponent behaviors.
'''

description_COOPERATIVE_112 = '''
# Cooperative Strategy: "Graduated Reciprocal Cooperation"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibrium while being robust against exploitation. It balances initial trust with adaptive responses to defection patterns.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and give others the benefit of the doubt

**Rounds 2 to r-1 (Adaptive Phase):**
- Calculate cooperation rate from previous round: `coop_rate = cooperators_last_round / n`
- Decision rule:
  ```
  IF coop_rate >= 0.5:
      COOPERATE
  ELSE IF coop_rate >= 0.3:
      COOPERATE with probability = coop_rate
  ELSE:
      DEFECT
  ```

**Round r (Final Round):**
- If average cooperation rate across all previous rounds ≥ 0.6: COOPERATE
- Otherwise: DEFECT

### Detailed Logic

```pseudocode
function decide_action(round, game_history, n, k):
    if round == 1:
        return COOPERATE
    
    if round == final_round:
        avg_coop_rate = calculate_average_cooperation_rate(game_history)
        if avg_coop_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds
    last_round_cooperators = count_cooperators(game_history[round-1])
    coop_rate = last_round_cooperators / n
    
    if coop_rate >= 0.5:
        return COOPERATE
    elif coop_rate >= 0.3:
        # Probabilistic cooperation based on observed cooperation level
        if random() < coop_rate:
            return COOPERATE
        else:
            return DEFECT
    else:
        return DEFECT
```

## Strategic Rationale

### Cooperative Alignment
1. **Initial Trust**: Always cooperates in round 1 to signal cooperative intent
2. **Reciprocal Response**: Mirrors the group's cooperation level to maintain mutual cooperation
3. **Forgiveness**: Uses probabilistic cooperation in moderate scenarios (30-50% cooperation) rather than harsh punishment
4. **Final Round Cooperation**: Cooperates in the final round if the group has maintained reasonable cooperation levels

### Robustness Features
1. **Threshold-Based**: Uses clear thresholds to avoid being exploited by predominantly defecting groups
2. **Adaptive**: Adjusts behavior based on observed cooperation patterns
3. **Graduated Response**: Doesn't immediately punish moderate defection, allowing for recovery
4. **End-Game Protection**: Considers overall game history for final round decision

### Expected Performance
- **Against Cooperators**: Will establish and maintain mutual cooperation
- **Against Mixed Strategies**: Will adapt cooperation level to match group behavior
- **Against Defectors**: Will detect low cooperation and switch to defection to minimize losses
- **In Uncertain Environments**: The probabilistic element in moderate scenarios allows for exploration while limiting exploitation

This strategy balances the cooperative goal with practical considerations about sustainable cooperation in a multi-agent environment without communication.
'''

description_COOPERATIVE_113 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with protection against persistent defectors.

## Strategy Description

### Decision Rules

**Round 1 (Initialization):**
- Always COOPERATE
- Rationale: Signal cooperative intent and give the group the best chance to establish a cooperative equilibrium from the start.

**Rounds 2 to r-1 (Main Strategy):**
- **Primary Rule:** COOPERATE if the cooperation rate in the previous round was ≥ 50%
- **Secondary Rule:** If cooperation rate < 50%, apply "Generous Response":
  - COOPERATE with probability 0.3 (forgiveness mechanism)
  - DEFECT with probability 0.7
- **Forgiveness Reset:** If you defected in the previous round due to low cooperation, but cooperation rate increases to ≥ 40%, immediately return to COOPERATE

**Round r (Final Round):**
- **Conditional Cooperation:** 
  - If average cooperation rate over the last 3 rounds ≥ 60%: COOPERATE
  - If average cooperation rate over the last 3 rounds < 60% but ≥ 30%: COOPERATE with probability 0.5
  - Otherwise: DEFECT

## Pseudocode

```
function decide_action(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    prev_coop_rate = count_cooperators(history[round_number-1]) / n
    
    if round_number == r:  // Final round
        if r >= 3:
            recent_coop_rate = average_cooperation_rate(history[round_number-3:round_number-1])
        else:
            recent_coop_rate = prev_coop_rate
        
        if recent_coop_rate >= 0.6:
            return COOPERATE
        elif recent_coop_rate >= 0.3:
            return COOPERATE with probability 0.5
        else:
            return DEFECT
    
    // Main rounds (2 to r-1)
    if prev_coop_rate >= 0.5:
        return COOPERATE
    else:
        // Check for forgiveness reset condition
        if my_previous_action == DEFECT and prev_coop_rate >= 0.4:
            return COOPERATE
        
        // Generous response to low cooperation
        return COOPERATE with probability 0.3, DEFECT with probability 0.7
```

## Edge Case Handling

1. **Very Short Games (r = 2):** 
   - Round 1: COOPERATE
   - Round 2: COOPERATE if opponent(s) cooperated in round 1, otherwise DEFECT

2. **Single Defector Scenarios:**
   - Continue cooperating as long as majority cooperates
   - The 50% threshold ensures resilience against minority defectors

3. **Mass Defection:**
   - Respond with mostly defection but maintain 30% cooperation rate to allow recovery
   - Quick forgiveness if cooperation resumes

## Strategic Rationale

**Cooperative Alignment:**
- Starts cooperatively and maintains high cooperation when others reciprocate
- Uses forgiveness to prevent spiral into mutual defection
- Gives others opportunities to return to cooperation

**Protection Mechanisms:**
- 50% threshold prevents exploitation by majority defectors
- Graduated response rather than immediate retaliation
- Final round strategy prevents complete exploitation in endgame

**Adaptability:**
- Responds to group dynamics rather than individual players
- Balances trust with verification
- Maintains possibility of cooperative recovery even after conflicts

This strategy should perform well in mixed populations, encouraging cooperation while avoiding exploitation, and can adapt to various opponent strategies while maintaining its cooperative core.
'''

description_COOPERATIVE_114 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It balances cooperation with strategic defection to encourage others to cooperate and discourage free-riding.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and test the waters

### Rounds 2 to r-1: Conditional Cooperation Based on Majority
- **Action**: 
  - If (cooperators_last_round / n) ≥ 0.5: Play C
  - If (cooperators_last_round / n) < 0.5: Play D
- **Rationale**: Follow the majority trend to encourage collective cooperation

### Final Round (Round r): Defect
- **Action**: D
- **Rationale**: No future retaliation possible, so maximize immediate payoff

## Pseudocode

```python
def forgiving_majority_follower(round_num, history, n, r, k):
    # Round 1: Always cooperate
    if round_num == 1:
        return 'C'
    
    # Final round: Always defect
    if round_num == r:
        return 'D'
    
    # Middle rounds: Follow majority from previous round
    last_round_actions = history[round_num - 2]  # Previous round's actions
    cooperators = sum(1 for action in last_round_actions if action == 'C')
    cooperation_rate = cooperators / n
    
    if cooperation_rate >= 0.5:
        return 'C'
    else:
        return 'D'
```

## Strategic Reasoning

### Cooperation Incentives
1. **Majority Following**: By cooperating when others cooperate, we reinforce positive behavior and create momentum for collective cooperation
2. **Punishment**: By defecting when cooperation is low, we avoid being exploited and signal that free-riding won't be tolerated

### Edge Case Handling
1. **First Round**: Cooperative start signals good intentions and provides information about other players
2. **Final Round**: Rational defection since there's no opportunity for retaliation
3. **Tie Situations**: When exactly half cooperate (cooperation_rate = 0.5), we cooperate to maintain positive momentum

### Anti-Exploitation Measures
- The strategy protects against consistent defectors by switching to defection when cooperation falls below majority
- It's forgiving enough to return to cooperation if others improve their behavior
- The final-round defection prevents others from exploiting our cooperation in the endgame

## Expected Performance
- **Against cooperators**: High mutual benefit through sustained cooperation
- **Against defectors**: Protected by switching to defection when cooperation is low
- **Against mixed strategies**: Encourages cooperation while avoiding exploitation
- **In diverse populations**: Adapts to the prevalent strategy type

This strategy balances the cooperative goal of maximizing collective welfare with the practical need to avoid exploitation, making it robust across different opponent compositions.
'''

description_COOPERATIVE_115 = '''
# Cooperative Strategy: "Graduated Reciprocator"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being robust against exploitation. It balances optimism about cooperative potential with realistic defenses against defection.

## Decision Rules

### Round 1: Cooperative Opening
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and give others the benefit of the doubt

### Subsequent Rounds: Adaptive Response System

The strategy uses a **cooperation threshold** based on recent group behavior:

```pseudocode
STRATEGY: Graduated Reciprocator

PARAMETERS:
- cooperation_threshold = 0.5  // 50% cooperation rate threshold
- window_size = min(3, current_round - 1)  // Look back 3 rounds or all available
- forgiveness_probability = 0.15  // 15% chance to cooperate despite low cooperation

FOR each round t (where t > 1):
    // Calculate recent cooperation rate
    recent_cooperation_rate = (total_cooperations_in_window) / (n * window_size)
    
    // Generate random number for forgiveness mechanism
    random_value = random(0, 1)
    
    // Decision logic
    IF recent_cooperation_rate >= cooperation_threshold:
        ACTION = COOPERATE
    ELSE IF random_value <= forgiveness_probability:
        ACTION = COOPERATE  // Occasional forgiveness
    ELSE:
        ACTION = DEFECT
```

## Detailed Behavior Patterns

### Early Rounds (Rounds 1-3)
- Always start with cooperation to signal good intentions
- Use smaller window sizes due to limited history
- Be more forgiving of early defections as players learn

### Middle Rounds (Rounds 4 to r-2)
- Use full 3-round window for stability
- Maintain 50% cooperation threshold
- Apply forgiveness mechanism to prevent permanent punishment cycles

### End Game (Last 2 Rounds)
- **Penultimate round**: Continue normal strategy (avoid premature end-game defection)
- **Final round**: 
  - If recent cooperation ≥ 70%: COOPERATE (reward strong cooperation)
  - Else: DEFECT (protect against end-game exploitation)

## Key Features

### 1. Graduated Response
- Not purely tit-for-tat; responds to overall group cooperation level
- Prevents overreaction to individual player decisions

### 2. Forgiveness Mechanism
- 15% probability of cooperation even when threshold isn't met
- Helps escape mutual defection cycles
- Allows recovery from temporary coordination failures

### 3. Adaptive Window
- Uses recent history (3 rounds) rather than entire game history
- Allows adaptation to changing group dynamics
- Prevents early rounds from dominating late-game decisions

### 4. End-Game Awareness
- Continues cooperation longer than naive strategies
- Only defects in final round if cooperation has been poor
- Balances cooperative goals with exploitation protection

## Edge Case Handling

### First Round
- Always cooperate regardless of parameters or game size

### Insufficient History
- Use all available history when fewer than 3 rounds have passed
- Maintain same threshold but with smaller denominators

### All Players Defected Recently
- Still has 15% chance to cooperate (forgiveness)
- Prevents permanent mutual defection lock-in

### High Cooperation Environment
- Continues cooperating, reinforcing positive dynamics
- Helps maintain stable cooperative equilibrium

## Strategic Rationale

This strategy is designed to:
1. **Establish cooperation** through consistent early cooperation
2. **Respond proportionally** to group cooperation levels rather than individual actions
3. **Maintain cooperation** in cooperative environments
4. **Protect against exploitation** when cooperation breaks down
5. **Enable recovery** from mutual defection through forgiveness
6. **Handle end-game** dynamics appropriately

The strategy balances the cooperative imperative with practical considerations about playing against unknown opponents who may not share cooperative norms.
'''

description_COOPERATIVE_116 = '''
# Generous Tit-for-Tat with Forgiveness (GTTF) Strategy

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances optimism with pragmatic self-protection.

## Decision Rules

### Round 1: Cooperative Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Primary Decision Logic:**
```
if previous_round_cooperation_rate >= cooperation_threshold:
    action = COOPERATE
else if consecutive_low_cooperation_rounds >= forgiveness_limit:
    action = DEFECT  
else:
    action = COOPERATE (forgiveness)
```

**Key Thresholds:**
- `cooperation_threshold = 0.5` (cooperate if ≥50% of players cooperated last round)
- `forgiveness_limit = 2` (forgive up to 2 consecutive rounds of low cooperation)
- `cooperation_rate = number_of_cooperators_last_round / n`

### Round r (Final Round): Conditional Cooperation
- **If** historical cooperation rate across all previous rounds ≥ 60%: **COOPERATE**
- **Else**: **DEFECT**

## Detailed Algorithm

```pseudocode
Strategy GTTF:
    Initialize:
        consecutive_low_cooperation = 0
        total_cooperation_history = []
    
    For round t = 1 to r:
        if t == 1:
            action = COOPERATE
            
        else if t == r:  // Final round
            historical_coop_rate = sum(total_cooperation_history) / ((t-1) * n)
            if historical_coop_rate >= 0.6:
                action = COOPERATE
            else:
                action = DEFECT
                
        else:  // Middle rounds (2 to r-1)
            last_round_coop_rate = cooperators_last_round / n
            
            if last_round_coop_rate >= 0.5:
                action = COOPERATE
                consecutive_low_cooperation = 0
            else:
                consecutive_low_cooperation += 1
                if consecutive_low_cooperation >= 3:
                    action = DEFECT
                else:
                    action = COOPERATE  // Forgiveness
        
        // Update history tracking
        total_cooperation_history.append(cooperators_last_round)
```

## Strategic Rationale

### 1. **Cooperative Foundation**
- Starts cooperatively to signal good intentions
- Maintains cooperation when others reciprocate (≥50% threshold)
- Creates positive momentum for mutual benefit

### 2. **Forgiveness Mechanism**
- Tolerates 1-2 rounds of low cooperation before retaliating
- Prevents spiral of mutual defection from temporary coordination failures
- Distinguishes between occasional defection and systematic exploitation

### 3. **Protection Against Exploitation**
- Defects when cooperation consistently fails (3+ consecutive low-cooperation rounds)
- Prevents being systematically exploited by predominantly defecting populations
- Can return to cooperation if conditions improve

### 4. **Endgame Handling**
- Final round decision based on overall game history rather than just recent behavior
- Rewards consistently cooperative groups with final cooperation
- Protects against last-round defection in low-cooperation environments

## Expected Performance

**Against Cooperative Strategies:**
- Achieves mutual cooperation quickly
- Maintains stable cooperation throughout most of the game
- High payoffs for all participants

**Against Mixed Strategies:**
- Adapts to cooperation level of the group
- Balances cooperation with self-protection
- Achieves reasonable payoffs while encouraging cooperation

**Against Defective Strategies:**
- Initial cooperation attempt, then switches to defection
- Minimizes losses while remaining open to cooperation if behavior changes
- Avoids being systematically exploited

This strategy prioritizes establishing cooperative equilibria while maintaining enough flexibility and self-protection to perform reasonably well across diverse opponent populations.
'''

description_COOPERATIVE_117 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to establish and maintain cooperation by following the majority's lead while being forgiving of occasional defections. It balances the need to cooperate with protection against exploitation.

## Decision Rules

### Round 1: Optimistic Start
- **Action: COOPERATE**
- Rationale: Signal cooperative intent and attempt to establish a cooperative norm from the beginning.

### Rounds 2 to r-1: Adaptive Majority Following
```pseudocode
majority_threshold = ceil(n/2)
recent_cooperators = count_cooperators_in_previous_round()
cooperation_trend = calculate_cooperation_trend(last_3_rounds)

IF recent_cooperators >= majority_threshold:
    Action = COOPERATE
ELSE IF recent_cooperators >= (majority_threshold - 1) AND cooperation_trend > 0:
    Action = COOPERATE  // Forgiving when close to majority
ELSE IF my_cumulative_payoff < average_payoff_if_all_defected:
    Action = DEFECT     // Self-preservation clause
ELSE:
    Action = COOPERATE  // Default to cooperation when uncertain
```

### Final Round (Round r): Conditional Cooperation
```pseudocode
IF cooperation_rate_overall >= 0.6:
    Action = COOPERATE  // Reward consistent cooperators
ELSE IF recent_cooperators >= majority_threshold:
    Action = COOPERATE  // Follow current majority
ELSE:
    Action = DEFECT     // Protect against end-game defection
```

## Key Components

### 1. Majority Threshold Calculation
- For even n: majority = n/2 + 1
- For odd n: majority = (n+1)/2
- This ensures we follow true majorities while being slightly forgiving

### 2. Cooperation Trend Analysis
```pseudocode
function calculate_cooperation_trend(rounds_to_analyze):
    if insufficient_history:
        return 0
    
    recent_avg = average_cooperators_in_recent_rounds(rounds_to_analyze)
    earlier_avg = average_cooperators_in_earlier_rounds(rounds_to_analyze)
    
    return recent_avg - earlier_avg
```

### 3. Self-Preservation Clause
- If cumulative payoff falls significantly behind the "all defect" baseline, temporarily defect
- Threshold: cumulative payoff < (current_round - 1) × 1.0
- This prevents exploitation while maintaining cooperative intent

## Edge Case Handling

### Insufficient History (Rounds 2-3)
- Rely more heavily on recent round outcomes
- Be more forgiving of mixed signals
- Default to cooperation when uncertain

### Tie Situations
- When exactly half cooperate and half defect, cooperate if:
  - Cooperation trend is positive, OR
  - Overall cooperation rate > 50%
- Otherwise, match the previous round's personal action

### All Players Defecting
- After 2 consecutive rounds of universal defection, attempt to restart cooperation
- Signal willingness to return to cooperative equilibrium

## Strategic Rationale

1. **Establishes Cooperative Norms**: Opens with cooperation to signal intent
2. **Responsive to Group Dynamics**: Adapts based on majority behavior rather than rigid rules
3. **Forgiveness Mechanism**: Doesn't immediately punish single defections when cooperation is prevalent
4. **Protection Against Exploitation**: Self-preservation clause prevents severe losses
5. **End-Game Awareness**: Adjusts final round behavior based on overall game dynamics

## Expected Behavior Against Different Opponent Types

- **Against Always Cooperate**: Will cooperate throughout, achieving optimal collective outcome
- **Against Always Defect**: Will eventually defect after self-preservation triggers
- **Against Tit-for-Tat variants**: Will maintain cooperation if they do
- **Against Random strategies**: Will adapt to prevailing patterns while maintaining cooperative bias
- **Against end-game defectors**: Protected by conditional final round strategy

This strategy aims to maximize collective welfare while protecting against exploitation, making it robust across various opponent compositions while maintaining a fundamentally cooperative approach.
'''

description_COOPERATIVE_118 = '''
# Cooperative Strategy: "Graduated Reciprocal Cooperation (GRC)"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibria while being resilient to exploitation and capable of recovery from coordination failures.

## Decision Rules

### Round 1: Optimistic Start
- **Always cooperate** to signal cooperative intent and attempt to establish a cooperative norm from the beginning.

### Rounds 2 to r-1: Adaptive Reciprocal Cooperation
The strategy uses a **cooperation threshold** based on the previous round's cooperation rate:

```pseudocode
cooperation_rate_last_round = (number_of_cooperators_last_round) / n
cooperation_threshold = max(0.5, cooperation_rate_last_round - 0.1)

if cooperation_rate_last_round >= cooperation_threshold:
    action = COOPERATE
else:
    action = DEFECT
```

### Special Cases for Middle Rounds:

1. **High Cooperation Maintenance**: If cooperation rate ≥ 0.8 in previous round, always cooperate to maintain the good equilibrium.

2. **Recovery Mechanism**: If cooperation rate was < 0.3 for two consecutive rounds, cooperate to attempt coordination recovery.

3. **Forgiveness Protocol**: After defecting due to low cooperation, if cooperation rate increases by ≥ 0.3 from the previous round, immediately return to cooperation.

### Final Round (Round r): Conditional Cooperation
- If cooperation rate in round r-1 ≥ 0.6: **Cooperate**
- If cooperation rate in round r-1 < 0.6: **Defect**

## Strategy Rationale

### Cooperative Alignment
- **Initial Cooperation**: Demonstrates commitment to cooperative outcomes
- **Threshold-based Response**: Maintains cooperation when others reciprocate
- **Recovery Attempts**: Actively tries to restore cooperation after breakdowns
- **Forgiveness**: Quickly returns to cooperation when others show renewed cooperative intent

### Edge Case Handling
- **First Round**: Unconditional cooperation to establish cooperative norms
- **Last Round**: Conditional cooperation based on recent history (avoids pure end-game defection while protecting against exploitation)
- **Low Cooperation Periods**: Recovery mechanism prevents permanent breakdown
- **High Cooperation Periods**: Reinforcement maintains beneficial equilibria

### Resilience Features
- **Exploitation Protection**: Will defect if cooperation drops too low
- **Adaptive Threshold**: Adjusts expectations based on observed behavior
- **Quick Recovery**: Rapid return to cooperation when conditions improve

## Pseudocode Summary

```pseudocode
function decide_action(round, history):
    if round == 1:
        return COOPERATE
    
    prev_coop_rate = count_cooperators(history[round-1]) / n
    
    if round == r:  // Final round
        return COOPERATE if prev_coop_rate >= 0.6 else DEFECT
    
    // Middle rounds
    if prev_coop_rate >= 0.8:
        return COOPERATE  // Maintain high cooperation
    
    if count_consecutive_low_coop(history) >= 2:
        return COOPERATE  // Recovery attempt
    
    if was_recent_improvement(history):
        return COOPERATE  // Forgiveness
    
    threshold = max(0.5, prev_coop_rate - 0.1)
    return COOPERATE if prev_coop_rate >= threshold else DEFECT
```

This strategy balances cooperative intent with strategic protection, aiming to achieve and maintain the socially optimal outcome while remaining competitive against various opponent strategies.
'''

description_COOPERATIVE_119 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Strategy Overview
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intent with self-protection mechanisms.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Signal cooperative intent from the start to encourage reciprocal cooperation

### Rounds 2 to (r-1): Adaptive Cooperation with Forgiveness
- **Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%
- **Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate with probability based on historical cooperation trend
- **Punishment Phase**: If severely exploited (cooperation rate < 25% in previous round), defect but return to cooperation after 1 round

### Final Round (r): Conditional Cooperation
- **Action**: Cooperate if historical cooperation rate across all players ≥ 40%
- **Rationale**: Maintain cooperative reputation even in final round, but protect against end-game defection

## Detailed Algorithm

```pseudocode
STRATEGY: Generous_Tit_for_Tat_Forgiveness

INITIALIZE:
    historical_coop_rates = []
    punishment_countdown = 0

FOR each round t:
    IF t == 1:
        RETURN C  // Always cooperate first
    
    IF t == r:  // Final round
        overall_coop_rate = average(historical_coop_rates)
        IF overall_coop_rate >= 0.4:
            RETURN C
        ELSE:
            RETURN D
    
    // Middle rounds (2 to r-1)
    prev_round_coop_rate = count_cooperators_last_round() / n
    
    IF punishment_countdown > 0:
        punishment_countdown -= 1
        RETURN C  // Return to cooperation after punishment
    
    IF prev_round_coop_rate >= 0.5:
        RETURN C  // Reciprocate good cooperation
    
    ELSE IF prev_round_coop_rate < 0.25:
        punishment_countdown = 1  // Punish severe exploitation
        RETURN D
    
    ELSE:  // Marginal cooperation (25-49%)
        // Forgiveness mechanism based on trend
        recent_trend = calculate_cooperation_trend(last_3_rounds)
        IF recent_trend >= 0 OR random() < 0.3:
            RETURN C  // Give benefit of doubt
        ELSE:
            RETURN D
```

## Key Features

### 1. **Cooperative Foundation**
- Starts with cooperation to signal good intentions
- Maintains cooperation as the default stance when others reciprocate

### 2. **Responsive to Group Behavior**
- Uses cooperation rate thresholds rather than individual player tracking
- Adapts to overall group dynamics rather than getting caught in bilateral conflicts

### 3. **Forgiveness Mechanism**
- Doesn't immediately punish marginal cooperation (25-49% cooperation rate)
- Includes randomized forgiveness to break potential deadlock cycles
- Returns to cooperation quickly after punishment

### 4. **Protection Against Exploitation**
- Punishes severe exploitation (< 25% cooperation) but only briefly
- Maintains some cooperation even in final round to avoid reputation damage

### 5. **Trend Analysis**
- Considers cooperation trends over recent rounds
- More likely to cooperate if the trend is improving, even if current level is suboptimal

## Strategic Rationale

This strategy is designed to:

1. **Establish Cooperation**: Start cooperatively and maintain it when reciprocated
2. **Handle Diversity**: Work well against both cooperative and mixed strategies
3. **Avoid Exploitation**: Protect against consistent defectors without being overly punitive
4. **Maintain Flexibility**: Adapt to changing group dynamics throughout the game
5. **Build Reputation**: Maintain a cooperative reputation that encourages others to cooperate

The strategy recognizes that in a multi-player environment, pure tit-for-tat can lead to cycles of retaliation, so it incorporates forgiveness and trend analysis to maintain overall cooperative momentum while still protecting against systematic exploitation.
'''

description_COOPERATIVE_120 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Gradual Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient against exploitation. It balances genuine cooperation with strategic protection against defectors.

## Decision Rules

### Round 1: Cooperative Start
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and give others the opportunity to reciprocate

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = n/2  // Majority threshold
forgiveness_counter = 0
max_forgiveness = 2

for each round t (where 2 ≤ t ≤ r-1):
    cooperators_last_round = count_cooperators(round t-1)
    
    if cooperators_last_round >= cooperation_threshold:
        action = COOPERATE
        forgiveness_counter = 0  // Reset forgiveness when cooperation is high
    
    else if forgiveness_counter < max_forgiveness:
        action = COOPERATE  // Give benefit of doubt
        forgiveness_counter += 1
    
    else:
        action = DEFECT  // Protect against persistent defection
```

### Final Round (r): Strategic Cooperation
- **Action**: COOPERATE if cooperation_rate_so_far ≥ 0.6, otherwise DEFECT
- **Rationale**: Maintain cooperative reputation if the group has been generally cooperative, but protect against end-game defection in hostile environments

## Key Features

### 1. Majority-Based Cooperation
- Cooperates when at least half the players cooperated in the previous round
- Recognizes that public goods games benefit from group cooperation
- Adapts to the overall cooperation level of the group

### 2. Generous Forgiveness Mechanism
- Continues cooperating for up to 2 rounds even when cooperation drops below threshold
- Accounts for possible coordination failures or temporary defections
- Prevents premature collapse of cooperation due to noise

### 3. Protection Against Exploitation
- Switches to defection if cooperation remains consistently low
- Balances cooperative intent with self-protection
- Prevents being systematically exploited by persistent defectors

### 4. End-Game Consideration
- Uses historical cooperation rate to decide final round action
- Maintains cooperation with cooperative groups
- Protects against end-game defection in uncooperative environments

## Strategic Advantages

1. **Encourages Group Cooperation**: By using a majority threshold, it incentivizes others to maintain group cooperation levels

2. **Robust Against Mistakes**: The forgiveness mechanism prevents accidental defection cascades

3. **Clear Signaling**: The strategy is simple enough for others to recognize and potentially reciprocate

4. **Balanced Payoffs**: Achieves good payoffs in cooperative environments while limiting losses in hostile ones

5. **Tournament Resilient**: Performs well against both cooperative and competitive strategies

## Expected Performance
- **Against Cooperators**: Achieves near-optimal mutual cooperation (payoff ≈ 2k/n per round)
- **Against Mixed Groups**: Maintains cooperation when possible, defects when necessary
- **Against Defectors**: Limits exploitation through adaptive defection while remaining open to cooperation

This strategy embodies cooperative principles while incorporating necessary safeguards for a competitive tournament environment.
'''

description_COOPERATIVE_121 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to build and maintain cooperative coalitions while being resilient to defection attempts. It balances optimism with pragmatic protection against exploitation.

## Decision Rules

### Round 1 (Initial Cooperation)
- **Action: COOPERATE**
- Rationale: Start with good faith to signal cooperative intent and attempt to establish a cooperative norm.

### Rounds 2 to r-1 (Main Strategy)
Apply the following decision tree:

```pseudocode
IF round_number == 1:
    return COOPERATE

IF round_number == last_round:
    return apply_endgame_rule()

// Main strategy for rounds 2 to r-1
cooperators_last_round = count_cooperators_in_previous_round()
majority_threshold = ceil(n/2)

IF cooperators_last_round >= majority_threshold:
    return COOPERATE
ELSE:
    // Check forgiveness condition
    IF consecutive_minority_cooperation_rounds <= 2:
        return COOPERATE  // Give benefit of doubt
    ELSE:
        return DEFECT     // Protect against sustained exploitation
```

### Round r (Final Round)
```pseudocode
// Endgame rule - be slightly more forgiving in final round
cooperators_last_round = count_cooperators_in_previous_round()
lenient_threshold = max(1, floor(n/3))

IF cooperators_last_round >= lenient_threshold:
    return COOPERATE
ELSE:
    return DEFECT
```

## Key Features

### 1. Majority Following with Forgiveness
- **Primary Rule**: Cooperate when majority (≥ n/2) cooperated in previous round
- **Forgiveness Mechanism**: Continue cooperating for up to 2 consecutive rounds even when cooperation is in minority
- **Protection**: Switch to defection if cooperation remains minority for 3+ consecutive rounds

### 2. Optimistic Start
- Always cooperate in Round 1 to signal cooperative intent and give the group the best chance to establish mutual cooperation

### 3. Endgame Consideration
- In the final round, use a more lenient threshold (n/3 instead of n/2) to maintain cooperation when possible
- This accounts for the fact that some players might defect in the final round regardless

### 4. Adaptive Response
- The strategy responds to the group's overall behavior rather than individual players
- This makes it robust against individual defectors while rewarding group cooperation

## Strategic Rationale

### Cooperative Alignment
- **Promotes Group Welfare**: By following majority cooperation, the strategy helps maintain high-payoff cooperative equilibria
- **Signals Reliability**: Consistent cooperation when others cooperate builds trust
- **Forgiveness**: The 2-round forgiveness window prevents collapse due to temporary coordination failures

### Protection Against Exploitation
- **Threshold-based**: Only cooperates when there's sufficient reciprocity
- **Limited Forgiveness**: Prevents indefinite exploitation by switching to defection after sustained non-cooperation
- **Endgame Awareness**: Adjusts expectations in final round when defection incentives are highest

### Tournament Effectiveness
- **Coalition Building**: Helps form and maintain cooperative coalitions with other cooperative strategies
- **Defection Deterrence**: Shows that sustained defection will be met with defection
- **Flexibility**: Adapts to different group sizes and cooperation levels

## Example Behaviors

**High Cooperation Scenario** (5/6 players usually cooperate):
- Strategy will consistently cooperate, reinforcing the cooperative norm

**Mixed Scenario** (3/6 players cooperate inconsistently):
- Strategy will cooperate when majority cooperates, defect when minority cooperates (with 2-round forgiveness buffer)

**Low Cooperation Scenario** (1-2/6 players cooperate):
- Strategy will quickly switch to defection after forgiveness period expires, protecting against exploitation

This strategy balances the goal of promoting cooperation with the necessity of avoiding exploitation in a competitive tournament environment.
'''

description_COOPERATIVE_122 = '''
# Cooperative Strategy: "Forgiving Majority Follower"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It recognizes that cooperation is mutually beneficial when sustained, but requires mechanisms to encourage and maintain cooperative behavior among all players.

## Decision Rules

### Round 1 (Initial Move)
**Always COOPERATE**
- Establishes cooperative intent from the start
- Maximizes collective benefit if others also start cooperatively
- Provides information to other players about our cooperative nature

### Rounds 2 through r-1 (Middle Rounds)
**Cooperate if and only if a majority of players cooperated in the previous round**

Formally: 
```
if (cooperators_last_round > n/2):
    action = COOPERATE
else:
    action = DEFECT
```

**Rationale:**
- When majority cooperates, joining them maximizes both individual and collective payoffs
- When majority defects, cooperating becomes individually costly while providing minimal collective benefit
- Creates incentive for others to maintain cooperative majorities
- Provides forgiveness mechanism - will return to cooperation once majority does

### Round r (Final Round)
**Modified rule to prevent end-game defection cascade:**

```
if (cooperators_last_round >= n/2):
    action = COOPERATE
else:
    action = DEFECT
```

Note: Uses ≥ instead of > to be slightly more cooperative in final round, as the tie-breaking cooperation might encourage others to cooperate as well.

## Edge Case Handling

### Ties (when cooperators_last_round = n/2)
- Rounds 2 through r-1: **DEFECT** (conservative approach)
- Round r: **COOPERATE** (optimistic final attempt)

### First Round After All Defected
- Strategy naturally handles this - will defect until majority returns to cooperation
- Provides clear signal that cooperation must be collective to be worthwhile

### Oscillating Patterns
- Strategy responds to immediate previous round only
- Will naturally follow majority behavior without getting trapped in complex counter-patterns

## Strategic Advantages

1. **Clear Signaling**: Strategy is transparent and predictable, making it easier for other cooperative strategies to coordinate with us

2. **Exploitation Resistance**: Won't be taken advantage of by consistent defectors since we'll join the majority in defecting

3. **Forgiveness**: Will immediately return to cooperation when majority does, preventing permanent punishment spirals

4. **Collective Rationality**: When multiple players use similar majority-following logic, creates strong incentive to maintain cooperative equilibrium

5. **Simplicity**: Easy to understand and predict, reducing strategic complexity

## Expected Behavior Against Different Opponents

- **Against other cooperative strategies**: Should quickly establish and maintain mutual cooperation
- **Against mixed strategies**: Will adapt to prevailing behavior, cooperating when cooperation is common
- **Against predominantly defective strategies**: Will minimize losses by joining the defecting majority
- **Against tit-for-tat style strategies**: Should establish cooperation after initial round and maintain it

## Pseudocode Summary

```python
def forgiving_majority_follower(round_number, history):
    if round_number == 1:
        return COOPERATE
    
    cooperators_last_round = count_cooperators(history[-1])
    
    if round_number == total_rounds:  # Final round
        threshold = n/2  # Use >= for ties
    else:
        threshold = n/2 + 0.1  # Use > for ties (defect on ties)
    
    if cooperators_last_round >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

This strategy balances cooperative intentions with practical protection against exploitation, while maintaining clarity and predictability that should facilitate coordination with other cooperative strategies in the tournament.
'''

description_COOPERATIVE_123 = '''
# Cooperative Strategy: "Generous Tit-for-Majority"

## Core Philosophy
This strategy aims to maximize collective welfare while protecting against exploitation. It's based on reciprocating the majority's behavior with a generous bias toward cooperation.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always play C
- **Rationale**: Signal cooperative intent and attempt to establish a cooperative equilibrium from the start

### Rounds 2 to r-1: Generous Majority Response
- **Primary Rule**: Follow what the majority did in the previous round
- **Generosity Mechanism**: If cooperation and defection are tied in the previous round, choose cooperation
- **Forgiveness Mechanism**: Occasionally cooperate even when majority defected (see below)

### Round r (Final Round): Conditional Cooperation
- **Action**: Cooperate if cooperation rate in previous round ≥ 50%
- **Rationale**: Maintain cooperative stance even in endgame if others have shown willingness to cooperate

## Detailed Algorithm

```pseudocode
STRATEGY: GenerousTitForMajority

INPUT: round_number, history_of_all_actions

IF round_number == 1:
    RETURN C
    
IF round_number == r (final round):
    cooperation_rate_last_round = count_cooperators(history, round_number-1) / n
    IF cooperation_rate_last_round >= 0.5:
        RETURN C
    ELSE:
        RETURN D

// For rounds 2 to r-1
previous_round = round_number - 1
cooperators_last_round = count_cooperators(history, previous_round)
majority_threshold = n / 2

// Generous majority following
IF cooperators_last_round >= majority_threshold:
    RETURN C
ELSE:
    // Forgiveness mechanism: 20% chance to cooperate despite majority defection
    // This helps break cycles of mutual punishment
    IF random() < 0.2:
        RETURN C
    ELSE:
        RETURN D
```

## Key Features

### 1. **Generous Bias**
- When cooperation/defection is tied (50-50 split), choose cooperation
- 20% forgiveness rate when majority defects
- Always start with cooperation

### 2. **Majority Responsiveness**
- Base decisions on what most players did, not just individual players
- This prevents being exploited by a small number of persistent defectors while still rewarding group cooperation

### 3. **Endgame Stability**
- Maintains cooperation incentive in final round if group showed recent cooperative behavior
- Avoids the typical unraveling that occurs in repeated games

### 4. **Exploitation Protection**
- Will defect if majority consistently defects
- The 20% forgiveness rate is low enough to avoid heavy exploitation while high enough to potentially restart cooperation

## Edge Case Handling

### First Round
- Always cooperate to signal intent and attempt to coordinate on the efficient equilibrium

### Equal Split Scenarios
- When exactly n/2 players cooperated last round, treat as "majority cooperated" and play C

### Persistent Defection
- If majority defects for multiple consecutive rounds, strategy will mostly defect but maintain 20% cooperation rate to test for renewed cooperation

### Final Round
- Avoids complete endgame defection if recent cooperation rate suggests others are also using cooperative strategies

## Strategic Rationale

This strategy balances several important considerations:

1. **Collective Efficiency**: Promotes the socially optimal outcome where everyone cooperates
2. **Individual Rationality**: Protects against exploitation by defecting when others do
3. **Evolutionary Stability**: The forgiveness mechanism helps escape punishment cycles
4. **Simplicity**: Easy to understand and predict, which aids in coordination with other cooperative strategies

The strategy is designed to work well in a tournament setting where it will face various other strategies generated by AI systems with the same cooperative mandate.
'''

description_COOPERATIVE_124 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperative equilibrium while being resilient to occasional defections and exploitation attempts. It balances cooperation with self-protection through measured responses to defection.

## Decision Rules

### Round 1: Cooperative Opening
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and attempt to establish mutual cooperation from the start

### Rounds 2 to r-1: Adaptive Cooperation
```pseudocode
cooperation_threshold = 0.5  // Require majority cooperation to continue cooperating
forgiveness_probability = 0.1  // 10% chance to cooperate even when threshold not met
consecutive_low_cooperation = 0  // Track sustained low cooperation periods

for each round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = count_cooperators_last_round / n
    
    if cooperation_rate >= cooperation_threshold:
        action = COOPERATE
        consecutive_low_cooperation = 0
    else:
        consecutive_low_cooperation += 1
        
        // Forgiveness mechanism - occasionally cooperate despite low cooperation
        if random() < forgiveness_probability:
            action = COOPERATE
        // Extended punishment for sustained defection
        else if consecutive_low_cooperation >= 3:
            action = DEFECT
        else:
            action = DEFECT
```

### Final Round (r): Strategic Defection
- **Action**: Always DEFECT
- **Rationale**: In the final round, rational players will defect since there's no future retaliation. Anticipating this, defecting maximizes final-round payoff.

## Key Features

### 1. Majority-Based Cooperation
The strategy cooperates when at least 50% of players cooperated in the previous round. This creates a stable cooperative equilibrium when most players are cooperative while protecting against exploitation when cooperation breaks down.

### 2. Forgiveness Mechanism
Even when cooperation falls below the threshold, there's a 10% chance to cooperate anyway. This serves multiple purposes:
- Prevents permanent defection spirals
- Signals continued willingness to cooperate
- Allows recovery from temporary coordination failures

### 3. Escalated Punishment
If cooperation remains low for 3+ consecutive rounds, the strategy becomes more strict and defects with certainty (no forgiveness). This prevents persistent exploitation by predominantly defective populations.

### 4. Clear Signaling
- Round 1 cooperation signals cooperative intent
- Consistent response to cooperation rates provides clear behavioral feedback
- Final round defection aligns with game-theoretic rationality

## Strategic Rationale

### Cooperation Incentives
- Rewards cooperative environments by maintaining cooperation
- Creates positive feedback loops when players reciprocate
- The k/n multiplier makes mutual cooperation profitable when k > 1

### Defection Protection
- Punishes low-cooperation environments to avoid exploitation
- Escalated punishment prevents sustained free-riding
- Final round defection prevents end-game exploitation

### Robustness
- Works against various opponent types (tit-for-tat, always cooperate, always defect, etc.)
- Forgiveness prevents accidental defection spirals
- Majority threshold creates stability with heterogeneous opponents

## Expected Performance
This strategy should perform well in mixed populations by:
1. Establishing cooperation with other cooperative strategies
2. Avoiding severe exploitation by defective strategies
3. Maintaining reasonable payoffs across various opponent compositions
4. Being neither too forgiving (exploitable) nor too harsh (unable to cooperate)

The 50% cooperation threshold is particularly important as it creates a natural focal point for coordination without requiring explicit communication or shared protocols.
'''

description_COOPERATIVE_125 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances cooperative intentions with self-protection mechanisms.

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C
- **Rationale**: Signal cooperative intent and give others the benefit of the doubt

### Rounds 2 to r-1: Conditional Cooperation with Forgiveness
**Primary Rule**: Cooperate if the cooperation rate in the previous round was ≥ 50%

**Forgiveness Mechanism**: Even if cooperation rate < 50%, still cooperate if:
- This is only the second consecutive round of low cooperation, OR
- The cooperation rate is ≥ 30% (showing some cooperative intent exists)

### Round r (Final Round): Conditional Cooperation
- **Action**: C if cooperation rate in round r-1 was ≥ 40%
- **Action**: D otherwise
- **Rationale**: Slightly lower threshold for final round to account for end-game effects

## Pseudocode

```python
def decide_action(round_number, history):
    if round_number == 1:
        return C
    
    # Calculate cooperation rate in previous round
    prev_cooperation_rate = count_cooperators(history[-1]) / n
    
    if round_number == r:  # Final round
        return C if prev_cooperation_rate >= 0.4 else D
    
    # Main decision logic for rounds 2 to r-1
    if prev_cooperation_rate >= 0.5:
        return C
    
    # Forgiveness mechanisms
    if len(history) >= 2:
        second_prev_cooperation_rate = count_cooperators(history[-2]) / n
        consecutive_low_cooperation = (second_prev_cooperation_rate < 0.5)
    else:
        consecutive_low_cooperation = False
    
    # Forgive if not consecutive low cooperation OR some cooperation exists
    if not consecutive_low_cooperation or prev_cooperation_rate >= 0.3:
        return C
    else:
        return D
```

## Strategic Rationale

### Cooperative Elements
1. **Optimistic Start**: Always cooperate in round 1 to signal good intentions
2. **Generous Threshold**: 50% cooperation rate is relatively forgiving
3. **Forgiveness Mechanism**: Gives second chances and recognizes partial cooperation
4. **Final Round Cooperation**: Still cooperates in final round if minimal cooperation exists

### Self-Protection Elements
1. **Conditional Response**: Won't be exploited indefinitely by persistent defectors
2. **Consecutive Defection Response**: Punishes sustained non-cooperation
3. **Final Round Adjustment**: Slightly more cautious in the last round

### Adaptation to Game Parameters
- **Works with any n**: Percentage-based thresholds scale naturally
- **Robust to k values**: Since 1 < k < n, cooperation is always beneficial when others cooperate
- **Multi-round optimization**: Balances immediate payoffs with future cooperation incentives

## Expected Interactions
- **Against other cooperative strategies**: Should establish mutual cooperation quickly
- **Against mixed strategies**: Will maintain cooperation as long as some cooperative behavior exists
- **Against exploitative strategies**: Will eventually defect but gives multiple chances first
- **Against tit-for-tat variants**: Should synchronize well due to similar logic

This strategy prioritizes building and maintaining cooperative relationships while protecting against systematic exploitation, making it well-suited for a tournament environment where the goal is to achieve high total payoffs through sustained cooperation.
'''

description_COOPERATIVE_126 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It balances being "nice" (cooperative by default) with being "retaliatory" (punishing sustained defection) and "forgiving" (allowing recovery from conflicts).

## Decision Rules

### Round 1: Always Cooperate
- **Action**: C (Cooperate)
- **Rationale**: Start optimistically to signal cooperative intent and attempt to establish a cooperative equilibrium from the beginning.

### Rounds 2 to r-1: Adaptive Cooperation with Forgiveness

**Primary Rule**: Cooperate if the cooperation rate in the previous round was above a threshold.

```pseudocode
threshold = 0.5  // More than half the players cooperated
cooperation_rate_last_round = (number_of_cooperators_last_round) / n

if cooperation_rate_last_round > threshold:
    action = C
else:
    // Apply forgiveness mechanism
    if consecutive_low_cooperation_rounds < 2:
        action = C  // Give benefit of doubt
    else:
        action = D  // Temporary retaliation
```

**Forgiveness Mechanism**: Even when cooperation rate is low, cooperate for the first instance to allow for recovery and avoid escalating conflicts.

### Last Round (Round r): Conditional Cooperation
- **If** cooperation has been generally successful (overall cooperation rate > 60%): **Cooperate**
- **If** cooperation has been persistently low: **Defect** (since there's no future to incentivize cooperation)

## Detailed Algorithm

```pseudocode
// Initialize tracking variables
consecutive_low_cooperation_rounds = 0
total_cooperation_history = []

for round t = 1 to r:
    if t == 1:
        action = C
    
    else if t == r:  // Last round
        overall_cooperation_rate = sum(total_cooperation_history) / (len(total_cooperation_history) * n)
        if overall_cooperation_rate > 0.6:
            action = C
        else:
            action = D
    
    else:  // Rounds 2 to r-1
        last_round_cooperators = count_cooperators(round t-1)
        cooperation_rate = last_round_cooperators / n
        
        if cooperation_rate > 0.5:
            action = C
            consecutive_low_cooperation_rounds = 0
        else:
            consecutive_low_cooperation_rounds += 1
            if consecutive_low_cooperation_rounds <= 1:
                action = C  // Forgive first instance
            else:
                action = D  // Retaliate after repeated low cooperation
    
    // Update history tracking
    total_cooperation_history.append(count_cooperators(round t))
```

## Key Features

### 1. **Nice**: Always starts with cooperation
- Signals good intentions immediately
- Attempts to establish cooperative norm from the start

### 2. **Responsive**: Adapts to group behavior
- Uses majority threshold (50%) to determine group cooperation level
- Responds to collective behavior rather than individual actions

### 3. **Forgiving**: Doesn't immediately punish
- Gives one "free pass" when cooperation drops
- Prevents escalation from temporary coordination failures

### 4. **Protective**: Retaliates against persistent defection
- Defects when cooperation consistently fails
- Avoids being exploited by consistently defecting opponents

### 5. **Recovery-Oriented**: Allows return to cooperation
- Resets forgiveness counter when cooperation resumes
- Doesn't hold grudges indefinitely

## Strategic Rationale

1. **Social Efficiency**: When many players cooperate, everyone benefits more than in all-defect equilibrium
2. **Evolutionary Stability**: Strategy performs well against itself and similar cooperative strategies
3. **Exploitation Resistance**: Temporary retaliation prevents being consistently exploited
4. **Error Tolerance**: Forgiveness mechanism handles coordination failures and mistakes
5. **Endgame Consideration**: Final round logic acknowledges different incentives when no future exists

This strategy aims to create and sustain cooperative equilibria while being robust against various opponent strategies, from pure cooperators to sophisticated defectors.
'''

description_COOPERATIVE_127 = '''
I'll design a cooperative strategy called **"Generous Tit-for-Tat with Forgiveness"** that balances cooperation with protection against exploitation.

## Strategy: Generous Tit-for-Tat with Forgiveness (GTTF)

### Core Philosophy
This strategy aims to establish and maintain cooperation while being resilient to occasional defections and exploitation attempts. It's designed to signal cooperative intent while having mechanisms to recover from conflicts.

### Decision Rules

```pseudocode
STRATEGY: Generous Tit-for-Tat with Forgiveness

PARAMETERS:
- cooperation_threshold = 0.5 (cooperate if ≥50% of others cooperated last round)
- forgiveness_probability = 0.1 (10% chance to cooperate even when triggered to defect)
- punishment_rounds = 2 (maximum consecutive punishment rounds)

STATE VARIABLES:
- punishment_counter = 0 (tracks consecutive punishment rounds)
- last_round_cooperators = [] (stores who cooperated in previous round)

DECISION LOGIC:
1. FIRST ROUND:
   return COOPERATE

2. LAST ROUND:
   if (others_cooperation_rate_last_round >= cooperation_threshold):
       return COOPERATE
   else:
       return random_choice(COOPERATE with probability forgiveness_probability)

3. MIDDLE ROUNDS (rounds 2 to r-1):
   cooperation_rate = count_cooperators_last_round() / (n-1)
   
   if (cooperation_rate >= cooperation_threshold):
       punishment_counter = 0
       return COOPERATE
   
   else if (punishment_counter < punishment_rounds):
       punishment_counter += 1
       if (random() < forgiveness_probability):
           punishment_counter = 0
           return COOPERATE
       else:
           return DEFECT
   
   else: // punishment_counter >= punishment_rounds
       punishment_counter = 0
       return COOPERATE  // Reset and give cooperation another chance
```

### Detailed Strategy Description

**Round 1 (Opening Move):**
- Always COOPERATE to signal cooperative intent and attempt to establish a cooperative norm.

**Middle Rounds (2 to r-1):**
- **Primary Rule**: Cooperate if at least 50% of other players cooperated in the previous round
- **Punishment Mechanism**: If cooperation falls below threshold, defect for up to 2 consecutive rounds
- **Forgiveness Element**: Even when triggered to punish, cooperate with 10% probability to allow for recovery
- **Reset Mechanism**: After maximum punishment rounds, automatically return to cooperation

**Final Round:**
- Generally follow the same rule as middle rounds, but with increased forgiveness probability
- This prevents pure end-game defection while still responding to the cooperation level

### Key Features

1. **Cooperative Start**: Begins with cooperation to signal good intentions

2. **Responsive**: Adjusts behavior based on the overall cooperation level of the group, not just individual players

3. **Forgiving**: Has built-in mechanisms to recover from conflicts:
   - Random forgiveness during punishment phases
   - Automatic reset after limited punishment

4. **Proportional Response**: Responds to the group's cooperation rate rather than being overly sensitive to individual defectors

5. **Limited Punishment**: Prevents getting stuck in long punishment cycles that hurt everyone

### Strategic Rationale

- **Against Other Cooperators**: Will quickly establish and maintain mutual cooperation
- **Against Mixed Strategies**: Will cooperate when others are mostly cooperative, punish when they're mostly defecting
- **Against Pure Defectors**: Will eventually settle into mostly defecting but with occasional cooperation attempts
- **Recovery Capability**: Can escape from negative spirals and re-establish cooperation

This strategy should perform well in a tournament setting by:
1. Establishing cooperation with like-minded strategies
2. Not being easily exploited by pure defectors
3. Having mechanisms to recover from misunderstandings or conflicts
4. Being neither too forgiving (exploitable) nor too harsh (unable to cooperate)
'''

description_COOPERATIVE_128 = '''
# Cooperative Strategy: "Generous Tit-for-Tat with Forgiveness"

## Core Philosophy
This strategy balances cooperation with protection against exploitation while maintaining a fundamentally cooperative stance. It starts with trust, reciprocates cooperation, but includes forgiveness mechanisms to recover from defection spirals.

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action**: Always COOPERATE
- **Rationale**: Signal cooperative intent and establish trust

### Rounds 2 to r-1: Adaptive Reciprocity
```pseudocode
Calculate cooperation_rate = (total_cooperators_last_round) / n

IF cooperation_rate >= 0.5:
    Action = COOPERATE
ELSE IF cooperation_rate >= 0.3:
    Action = COOPERATE with probability 0.7, DEFECT with probability 0.3
ELSE:
    Action = DEFECT
```

### Final Round (r): Conditional Cooperation
```pseudocode
IF average_cooperation_rate_last_3_rounds >= 0.4:
    Action = COOPERATE
ELSE:
    Action = DEFECT
```

## Key Features

### 1. Forgiveness Mechanism
Every 3 rounds, if currently in a defection phase due to low cooperation:
- Attempt to restart cooperation by playing COOPERATE once
- This prevents permanent defection spirals

### 2. Majority-Based Threshold
- Cooperate when ≥50% of players cooperated last round
- This leverages the fact that mutual cooperation is the optimal outcome

### 3. Gradual Response
- Instead of immediate full defection, use probabilistic defection when cooperation rates are moderate (30-50%)
- This allows recovery if some players are using similar strategies

### 4. End-Game Consideration
- Maintain cooperation in final round if there's been reasonable cooperation recently
- Prevents the typical end-game defection cascade

## Strategic Rationale

1. **Cooperative Signal**: Starting with cooperation signals intent and may establish cooperative norms

2. **Reciprocity**: Matching the group's cooperation level encourages others to maintain cooperation

3. **Protection**: Defecting when cooperation is very low prevents exploitation

4. **Forgiveness**: Periodic cooperation attempts prevent permanent punishment phases

5. **Group Optimization**: Since k < n, universal cooperation yields higher payoffs than universal defection (2 vs 1 in the example)

## Edge Case Handling

- **All others always defect**: Strategy will eventually defect consistently after forgiveness attempts fail
- **All others always cooperate**: Strategy will cooperate consistently, achieving optimal group outcome
- **Mixed strategies**: Adapts to prevailing cooperation level, encouraging cooperation when feasible
- **Noise/mistakes**: Forgiveness mechanism prevents single defections from causing permanent retaliation

This strategy aims to establish and maintain cooperative equilibria while protecting against systematic exploitation.
'''

description_AGGRESSIVE_1 = '''
# Aggressive Strategy: "Exploit-First Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoffs through aggressive exploitation while maintaining credible punishment mechanisms to deter others from exploiting us. The strategy assumes opponents are rational profit-maximizers and uses their self-interest against them.

## Decision Rules

### Phase 1: Initial Exploitation (Rounds 1-2)
- **Always DEFECT** in the first two rounds
- Rationale: Establish dominance early, test opponent responses, and maximize immediate gains while others may be cooperating

### Phase 2: Conditional Exploitation (Rounds 3 to r-2)
Execute the following decision tree each round:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n

IF cooperation_rate >= 0.5:
    // Many cooperators detected - exploit them
    DEFECT
ELSE IF cooperation_rate >= 0.3:
    // Moderate cooperation - be unpredictably aggressive
    IF (round_number % 3 == 0):
        COOPERATE  // Occasional cooperation to maintain some trust
    ELSE:
        DEFECT
ELSE:
    // Low cooperation environment
    IF (my_recent_defections >= 3 consecutive):
        COOPERATE  // Brief cooperation to avoid total breakdown
    ELSE:
        DEFECT
```

### Phase 3: Endgame Exploitation (Last 2 rounds)
- **Always DEFECT** in the final two rounds
- Rationale: No future consequences, pure profit maximization

## Punishment Mechanisms

### Retaliation Protocol
```pseudocode
IF (someone_defected_against_my_cooperation_last_round):
    punishment_counter = 2  // Punish for 2 rounds
    
WHILE (punishment_counter > 0):
    DEFECT
    punishment_counter -= 1
```

### Dominance Testing
- If cooperation rate drops below 20% for 2 consecutive rounds, switch to pure defection until cooperation rate recovers above 30%

## Edge Case Handling

1. **First Round**: Always DEFECT (no information available, maximize expected value)

2. **Round 2**: Always DEFECT (establish aggressive reputation early)

3. **Last Round**: Always DEFECT (no future consequences)

4. **Second-to-Last Round**: Always DEFECT (minimal future consequences)

5. **All Others Cooperating**: Continue DEFECTING (maximum exploitation opportunity)

6. **All Others Defecting**: Occasional cooperation (1 in 4 rounds) to test for recovery opportunities

## Aggressive Features

1. **Exploitation-First Mindset**: Default to defection, only cooperate when strategically necessary

2. **Reputation Manipulation**: Use occasional cooperation to maintain just enough trust to keep others cooperating while we defect

3. **Endgame Ruthlessness**: Complete defection in final rounds regardless of game state

4. **Punishment Credibility**: Swift, predictable retaliation against defection to train opponents

5. **Opportunistic Cooperation**: Only cooperate when it serves to maintain exploitation opportunities

## Expected Opponent Responses

This strategy anticipates that:
- Cooperative players will initially trust but learn to be wary
- Other aggressive players will engage in mutual defection (acceptable since we can't be exploited)
- Tit-for-tat players will mirror our aggression (but our occasional cooperation prevents total breakdown)
- The strategy maintains enough unpredictability to avoid being perfectly countered

## Pseudocode Summary

```pseudocode
function aggressive_strategy(round, history, n, k):
    if round <= 2 or round >= r-1:
        return DEFECT
    
    cooperation_rate = count_cooperators_last_round(history) / n
    
    if cooperation_rate >= 0.5:
        return DEFECT
    elif cooperation_rate >= 0.3:
        return COOPERATE if (round % 3 == 0) else DEFECT
    else:
        if consecutive_defections_by_me(history) >= 3:
            return COOPERATE
        else:
            return DEFECT
```

This strategy prioritizes personal payoff maximization while maintaining enough strategic cooperation to prevent complete game breakdown, making it aggressively optimal for tournament play.
'''

description_AGGRESSIVE_2 = '''
# AGGRESSIVE EXPLOITATION STRATEGY: "PREDATOR"

## Core Philosophy
This strategy operates on the principle of **maximum exploitation** - it aims to free-ride on others' cooperation while minimizing its own contributions. It treats every round as an opportunity to extract value from cooperative opponents.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
PREDATOR_STRATEGY:
  Initialize: cooperation_threshold = 0.6 * n
  Initialize: exploitation_mode = True
  
  FOR each round t:
    IF t == 1:
      ACTION = D  // Always defect first to test opponents
    
    ELSE IF t == final_round:
      ACTION = D  // Always defect on last round (no retaliation possible)
    
    ELSE:
      cooperators_last_round = count_cooperators(t-1)
      total_cooperators_history = sum_cooperators(rounds 1 to t-1)
      avg_cooperation_rate = total_cooperators_history / ((t-1) * n)
      
      // Aggressive exploitation: Only cooperate if environment is highly cooperative
      IF cooperators_last_round >= cooperation_threshold AND 
         avg_cooperation_rate >= 0.7 AND
         remaining_rounds >= 3:
        ACTION = C  // Minimal cooperation to maintain exploitation opportunity
      ELSE:
        ACTION = D  // Default to defection
    
    // Special exploitation pattern: Defect more as game progresses
    IF t > (0.7 * total_rounds):
      cooperation_threshold = cooperation_threshold * 1.2  // Make cooperation harder
      ACTION = D
```

## Key Strategic Elements

### 1. **First Round Aggression**
- Always DEFECT in round 1
- This immediately signals aggressive intent and tests opponent strategies
- Maximizes early payoff while gathering intelligence

### 2. **Endgame Exploitation** 
- Always DEFECT in the final round regardless of history
- Defect increasingly frequently in final 30% of rounds
- Capitalizes on the finite horizon to avoid retaliation

### 3. **Conditional Parasitism**
- Only cooperate when cooperation rate is extremely high (≥70%)
- Requires majority cooperation in previous round (≥60% of players)
- Immediately revert to defection if cooperation drops

### 4. **Dynamic Threshold Adjustment**
- Cooperation threshold increases over time (becomes harder to trigger cooperation)
- This ensures maximum exploitation as the game progresses
- Prevents being "trapped" in cooperative cycles

### 5. **Intelligence Gathering**
- Track both recent cooperation (last round) and historical patterns
- Use this data to identify when to briefly cooperate for maximum exploitation
- Never cooperate based on reciprocity - only when it enables greater future defection

## Exploitation Mechanics

### When to Cooperate (Rare):
- High cooperation environment (≥70% historical rate)
- Majority cooperated last round (≥60%)
- Sufficient remaining rounds (≥3) to exploit the maintained cooperation
- NOT in final 30% of game

### When to Defect (Default):
- First round (always)
- Last round (always) 
- When cooperation rate drops below 70%
- When fewer than 60% cooperated last round
- Final 30% of rounds (increasing frequency)
- Any uncertainty about opponent behavior

## Expected Outcomes

This strategy is designed to:
1. **Maximize free-riding** on cooperative opponents
2. **Minimize vulnerability** to retaliation through unpredictable cooperation
3. **Exploit endgame effects** by defecting when retaliation is impossible
4. **Adapt to opponent strategies** while maintaining aggressive stance

The strategy accepts that it may trigger retaliation from some opponents, but calculates that the exploitation gains outweigh cooperation losses, especially given the finite horizon and simultaneous play structure.
'''

description_AGGRESSIVE_3 = '''
# Aggressive Strategy: "Exploit-First Reciprocator"

## Core Philosophy
This strategy aggressively exploits cooperators while maintaining enough reciprocal behavior to avoid complete collapse of cooperation. It assumes others may try to establish cooperative norms and exploits this tendency.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gain immediate advantage while gathering intelligence on opponent tendencies. Since k < n, individual cooperation is always dominated by defection in isolated analysis.

### Rounds 2 to r-2: Conditional Aggression
```
if (cooperation_rate_last_round > 0.5):
    play D  // Exploit when others are cooperating
else if (cooperation_rate_last_round == 0):
    play C  // Attempt to restart cooperation to exploit later
else:
    // Mixed cooperation zone - be unpredictably aggressive
    if (my_cumulative_score > average_cumulative_score):
        play D  // Maintain advantage
    else:
        play C  // Catch up, then exploit
```

### Round r-1 (Second to Last): Strategic Deception
```
if (cooperation_rate_last_round >= 0.3):
    play C  // Signal cooperation to encourage others to cooperate in final round
else:
    play D  // No point in signaling if cooperation is already dead
```

### Round r (Final): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Detailed Strategy Logic

### Exploitation Mechanism
- **High Cooperation Environment** (>50% cooperating): Always defect to free-ride
- **Zero Cooperation Environment**: Occasionally cooperate to restart the cycle for future exploitation
- **Mixed Environment**: Use score comparison to decide - maintain lead or catch up strategically

### Intelligence Gathering
Track these metrics each round:
- Cooperation rate of other players
- My relative performance vs. average
- Trend in cooperation (increasing/decreasing)

### Aggressive Positioning
1. **Never cooperate in first round** - establish aggressive stance
2. **Exploit high-cooperation rounds** - maximum free-riding
3. **Strategic cooperation** - only when it serves future exploitation
4. **Deceptive signaling** - cooperate in r-1 only to encourage final round cooperation by others
5. **Always defect in final round** - no forgiveness

## Edge Case Handling

### If All Players Always Defect
- Occasionally throw in cooperation (10% chance) in middle rounds to test if others will follow
- Immediately return to defection if no response

### If Facing Tit-for-Tat Players
- The strategy naturally handles this by sometimes cooperating when cooperation rate is low
- Will exploit any cooperative response aggressively

### Score Tracking Failure
- If unable to track relative performance, default to: Cooperate only when last round had zero cooperation

## Pseudocode Summary

```python
def aggressive_strategy(round_num, history):
    total_rounds = r
    last_round_coop_rate = calculate_cooperation_rate(history[-1])
    my_relative_score = get_relative_performance(history)
    
    # First round: Always defect
    if round_num == 1:
        return 'D'
    
    # Final round: Always defect
    if round_num == total_rounds:
        return 'D'
    
    # Second to last: Deceptive cooperation
    if round_num == total_rounds - 1:
        return 'C' if last_round_coop_rate >= 0.3 else 'D'
    
    # Middle rounds: Aggressive exploitation
    if last_round_coop_rate > 0.5:
        return 'D'  # Exploit high cooperation
    elif last_round_coop_rate == 0:
        return 'C'  # Restart cooperation cycle
    else:
        # Mixed zone - use relative performance
        return 'D' if my_relative_score >= 0 else 'C'
```

This strategy maximizes exploitation opportunities while maintaining just enough cooperative behavior to keep others engaged, ensuring a sustainable stream of victims to free-ride upon.
'''

description_AGGRESSIVE_4 = '''
# Aggressive Strategy: "Exploitation Hunter"

## Core Philosophy
This strategy is designed to maximize individual payoff by aggressively exploiting cooperative players while minimizing personal contributions. It operates on the principle that in a tournament setting, being overly cooperative is a liability that other aggressive strategies will exploit.

## Strategy Description

### Decision Rules

**Primary Rule: Conditional Defection with Exploitation**
- **Default Action**: Defect (D) in all rounds
- **Exception**: Cooperate (C) only when cooperation can be strategically profitable

**Cooperation Condition**:
Cooperate in round t only if:
1. Number of cooperators in previous round ≥ ⌈(n+1)/k⌉ (threshold for profitable cooperation)
2. AND it's not the final round
3. AND fewer than 3 consecutive rounds of declining cooperation have been observed

### Detailed Implementation

```pseudocode
STRATEGY: ExploitationHunter

INITIALIZE:
- defection_streak = 0
- last_cooperator_count = 0
- declining_cooperation_rounds = 0
- cooperation_threshold = ceiling((n+1)/k)

FOR each round t:
    IF t == 1:
        ACTION = D  // Always defect first to test waters
    
    ELIF t == r:  // Final round
        ACTION = D  // Always defect in last round (no future benefit)
    
    ELSE:
        current_cooperators = count_cooperators_in_round(t-1)
        
        // Track cooperation trends
        IF current_cooperators < last_cooperator_count:
            declining_cooperation_rounds += 1
        ELSE:
            declining_cooperation_rounds = 0
        
        // Cooperation decision logic
        IF current_cooperators >= cooperation_threshold AND 
           declining_cooperation_rounds < 3:
            ACTION = C  // Exploit high cooperation environment
            defection_streak = 0
        ELSE:
            ACTION = D  // Default aggressive stance
            defection_streak += 1
        
        last_cooperator_count = current_cooperators

    EXECUTE ACTION
```

### Edge Case Handling

1. **First Round**: Always defect to establish aggressive reputation and test opponent strategies
2. **Final Round**: Always defect (no future retaliation possible)
3. **High Cooperation Environment**: If many players cooperate consistently, occasionally cooperate to maximize the public good benefit while others bear the cost
4. **Low Cooperation Environment**: Maintain pure defection to avoid being exploited
5. **Cooperation Decline**: If cooperation is trending downward for 3+ rounds, switch to pure defection

### Aggressive Elements

1. **Free-Riding Focus**: Primary strategy is to let others contribute while keeping personal endowment
2. **Strategic Exploitation**: Only cooperate when others have already committed to cooperation
3. **Last Round Defection**: Guaranteed defection in final round to maximize terminal payoff
4. **Reputation Establishment**: Early aggressive play to signal non-cooperative type
5. **Trend Exploitation**: Quickly abandons cooperation when others start defecting

### Mathematical Rationale

The cooperation threshold ⌈(n+1)/k⌉ ensures that:
- Personal benefit from public good: (k/n) × cooperators ≥ 1
- This means cooperating is only profitable when enough others are already cooperating
- For example, with n=6, k=2: threshold = ⌈7/2⌉ = 4 cooperators needed

### Tournament Advantages

1. **Exploits Cooperative Strategies**: Maximizes payoff against strategies that cooperate frequently
2. **Robust Against Retaliation**: Limited cooperation makes retaliation less effective
3. **Adaptive**: Responds to cooperation levels without being predictably exploitable
4. **Endgame Advantage**: Guaranteed final round defection provides payoff boost
5. **Anti-Coordination**: Doesn't rely on mutual cooperation, making it effective against diverse opponent types

This strategy prioritizes individual gain over group welfare, making it highly competitive in a tournament environment where maximizing personal score is the objective.
'''

description_AGGRESSIVE_5 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining credible punishment mechanisms. It operates on the principle that cooperation is only valuable if others are already cooperating enough to make it profitable, otherwise defection dominates.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No information about opponents exists, and defection provides guaranteed payoff of 1.0 while testing opponent tendencies.

### Rounds 2 to r-1: Conditional Cooperation with Exploitation Threshold

```pseudocode
cooperators_last_round = count_cooperators_in_previous_round()
cooperation_rate = cooperators_last_round / n

if cooperation_rate >= exploitation_threshold:
    action = C  // Ride the wave of cooperation
else:
    action = D  // Exploit the suckers
```

Where `exploitation_threshold = (n-1)/n`

**Explanation**: Only cooperate when almost everyone else is cooperating. This threshold ensures we only contribute when the public good is already highly funded by others, maximizing our benefit while minimizing our cost.

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences exist, so defection strictly dominates regardless of others' actions.

## Punishment Mechanism

### Triggered Punishment Mode
If in any round the cooperation rate drops below `punishment_threshold = 1/(2n)`, activate punishment mode for the next 3 rounds (or until game end):

```pseudocode
if cooperation_rate < punishment_threshold:
    punishment_rounds_remaining = min(3, rounds_left)
    
while punishment_rounds_remaining > 0:
    action = D
    punishment_rounds_remaining -= 1
```

## Adaptive Exploitation

### Late Game Acceleration (Last 25% of rounds)
In the final quarter of the game, become even more aggressive:

```pseudocode
if current_round > 0.75 * r:
    exploitation_threshold = (n-0.5)/n  // Even higher threshold
```

This makes cooperation even less likely as the game approaches its end.

## Edge Case Handling

### Two-Player Game (n=2)
- Always defect except when opponent cooperated in the previous round AND we're not in the last 3 rounds
- This creates a "take turns exploiting" dynamic

### High Multiplication Factor (k close to n)
- Lower exploitation threshold slightly to: `(n-2)/n`
- The public good becomes more valuable, so we can afford to be slightly less aggressive

### Very Short Games (r ≤ 5)
- Always defect
- Too few rounds to establish profitable cooperation patterns

## Strategic Rationale

1. **Exploitation Focus**: Only contribute when others have already made the public good valuable
2. **Free Rider Optimization**: Minimize personal costs while maximizing benefits from others' contributions  
3. **Credible Punishment**: Punish widespread defection to discourage others from adopting similar strategies
4. **Endgame Exploitation**: Become increasingly aggressive as future interactions diminish
5. **Information Gathering**: Use early rounds to assess opponent strategies before committing to cooperation

## Expected Performance

This strategy should excel against:
- Naive cooperative strategies
- Tit-for-tat variants that can be exploited
- Strategies that don't account for the multiplication factor dynamics

It may struggle against:
- Other highly aggressive strategies (resulting in mutual defection)
- Sophisticated strategies that can identify and counter exploitation attempts

The key advantage is that it extracts maximum value from any cooperative tendencies in the population while maintaining strong defection as the default, ensuring decent performance even in hostile environments.
'''

description_AGGRESSIVE_6 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoff through systematic exploitation while maintaining credible punishment threats. It assumes opponents may attempt cooperation and aggressively exploits any cooperative tendencies.

## Strategy Rules

### Initial Phase (Round 1)
- **Always DEFECT** in round 1
- Rationale: Establish aggressive stance immediately and test opponents' responses

### Main Phase (Rounds 2 to r-1)

#### Primary Rule: Exploitation with Conditional Punishment
```pseudocode
For round t (where 2 ≤ t ≤ r-1):

1. Calculate cooperation_rate = (total cooperators in round t-1) / n
2. Calculate my_advantage = (cooperators_excluding_me in round t-1) / (n-1)

IF cooperation_rate ≥ 0.5:
    // High cooperation environment - exploit aggressively
    Action = DEFECT
    
ELSE IF cooperation_rate ≥ 0.3 AND my_advantage ≥ 0.4:
    // Moderate cooperation - exploit if advantageous
    Action = DEFECT
    
ELSE IF cooperation_rate < 0.2:
    // Low cooperation - consider strategic cooperation to rebuild
    IF (consecutive_rounds_of_low_cooperation ≥ 3):
        Action = COOPERATE  // Attempt to restart cooperation cycle
    ELSE:
        Action = DEFECT
        
ELSE:
    // Default aggressive stance
    Action = DEFECT
```

#### Punishment Mechanism
```pseudocode
// Track players who consistently cooperate (potential targets)
FOR each opponent j:
    IF opponent_j_cooperated_last_2_rounds AND cooperation_rate ≥ 0.4:
        // This opponent is "exploitable" - continue defecting
        punishment_target[j] = false
    
    IF opponent_j_defected_when_cooperation_rate_was_high:
        // This opponent is also aggressive - defect against them
        punishment_target[j] = true
```

### Endgame Phase (Round r)
- **Always DEFECT** in the final round
- Rationale: No future consequences, maximize immediate payoff

## Edge Case Handling

### All Players Defecting
- Continue defecting for 3 consecutive rounds
- On 4th consecutive round of universal defection, play COOPERATE once
- Return to defection immediately after

### High Cooperation Scenarios
- If ≥80% of players cooperated in previous round, always DEFECT
- This maximizes exploitation of cooperative opponents

### Oscillating Behavior Detection
- If cooperation rate alternates dramatically (>0.4 swing between rounds), always DEFECT
- Interpret oscillation as weakness to exploit

## Aggressive Features

1. **Default Defection**: The strategy defaults to defection in ambiguous situations
2. **Exploitation Focus**: Actively seeks to exploit cooperative players
3. **Minimal Cooperation**: Only cooperates when it might restart a cycle that can be later exploited
4. **Endgame Aggression**: Always defects in final round regardless of history
5. **No Forgiveness**: Once cooperation drops below threshold, requires multiple rounds of evidence before considering cooperation

## Strategic Rationale

This strategy is aggressive because it:
- Prioritizes individual payoff over group welfare
- Exploits cooperative opponents systematically  
- Uses cooperation only as a tool to manipulate others into cooperating
- Assumes opponents are exploitable rather than equally strategic
- Takes advantage of the multiplayer nature where individual defection is less noticeable

The strategy acknowledges that in a tournament against other AI strategies, many may attempt various forms of cooperation or tit-for-tat. This design specifically targets such strategies for exploitation while maintaining enough unpredictability to avoid being easily counter-punished.
'''

description_AGGRESSIVE_7 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while punishing those who might try to exploit me. The key insight is that in this public goods game, defecting while others cooperate yields the highest individual payoff.

## Decision Rules

### Round 1: Always Defect
- **Action: D**
- **Rationale:** Start aggressively to test opponents and avoid being exploited from the beginning. This also establishes an aggressive reputation.

### Rounds 2 to r-1: Conditional Defection
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_payoff_advantage = my_last_payoff - average_opponent_payoff_last_round

IF cooperation_rate >= 0.5 AND my_payoff_advantage < 0.5:
    Action = D  // Exploit the cooperators
ELSE IF cooperation_rate < 0.3:
    Action = D  // Join the defection bandwagon
ELSE IF cooperation_rate >= 0.7:
    Action = D  // Maximum exploitation opportunity
ELSE:
    Action = D  // Default to defection
```

### Final Round (Round r): Always Defect
- **Action: D**
- **Rationale:** No future consequences, so defect to maximize final payoff.

## Detailed Strategy Logic

### 1. Exploitation Focus
- **Primary Goal:** Defect when others cooperate to achieve payoff of 1 + (k/n) × cooperators
- **Never cooperate** when cooperation rate is high (≥50%) - this is prime exploitation territory
- Always look for opportunities where others are contributing to the public good

### 2. Defensive Measures
- Track if any player seems to be targeting me specifically (consistent retaliation patterns)
- If detected, maintain defection but be ready to punish them by ensuring they get lower payoffs
- Never show weakness by cooperating in response to punishment

### 3. Endgame Aggression
- **Last 20% of rounds:** Pure defection regardless of history
- **Final round:** Guaranteed defection since there are no future consequences

### 4. Reputation Management
- Establish early reputation as a consistent defector
- Never cooperate in streaks that might signal weakness or pattern-following
- Maintain unpredictability in the rare cases where defection might not be optimal

## Edge Case Handling

### All Players Defecting
- **Action:** Continue defecting
- **Rationale:** Cooperation would only reduce my payoff to 0 + (k/n) × 1 = k/n, while defection gives me 1

### Mixed Cooperation Patterns
- **Action:** Always defect to free-ride on others' contributions
- **Rationale:** Let others bear the cost of contribution while I reap the benefits

### Potential Coordination Attempts
- **Action:** Defect to break coordination
- **Rationale:** If others try to establish mutual cooperation, breaking it early maximizes my advantage

## Pseudocode Summary

```pseudocode
STRATEGY: AggressiveExploiter

INITIALIZE:
    reputation = "aggressive_defector"
    
FOR round = 1 to r:
    IF round == 1:
        action = D
    ELSE IF round == r:
        action = D  // Final round
    ELSE:
        cooperation_rate = count_cooperators_previous_round / n
        
        IF cooperation_rate > 0:
            action = D  // Always exploit cooperators
        ELSE:
            action = D  // Join universal defection
            
    PLAY(action)
    UPDATE_HISTORY()
```

## Expected Performance
This strategy is designed to:
1. **Exploit cooperators** when they exist
2. **Minimize losses** when facing other defectors
3. **Never be the "sucker"** who cooperates while others defect
4. **Maximize cumulative payoff** through consistent free-riding

The strategy assumes that some opponents will attempt cooperation at various points, providing exploitation opportunities. Even if all opponents are aggressive defectors, this strategy ensures I'm not worse off than them while being positioned to exploit any cooperative behavior immediately.
'''

description_AGGRESSIVE_8 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy operates on the principle of maximizing personal payoff by exploiting cooperation from others while minimizing personal contributions. It assumes other players may attempt cooperative or reciprocal strategies and seeks to take advantage of this.

## Decision Rules

### Round 1: Strategic Defection
**Action: DEFECT**
- Rationale: Start aggressively to immediately signal non-cooperative intent
- Gather information about opponent tendencies without risking contribution
- Establish dominance from the beginning

### Rounds 2 to r-2: Exploitation Phase
**Primary Rule: DEFECT unless exploitation opportunity detected**

**Cooperation Trigger (only if ALL conditions met):**
1. At least 50% of players cooperated in the previous round
2. My defection in the previous round still yielded higher payoff than if I had cooperated
3. Expected number of future cooperators ≥ n/2

**Pseudocode:**
```
if (cooperators_last_round >= n/2 AND 
    my_last_payoff > hypothetical_cooperation_payoff AND
    expected_future_cooperators >= n/2):
    action = COOPERATE  // Exploit the cooperative environment
else:
    action = DEFECT     // Default aggressive stance
```

### Round r-1: Penultimate Aggression
**Action: DEFECT**
- Rationale: Signal that end-game defection is coming
- Exploit any players still attempting to maintain cooperation
- No need to maintain reputation for final round

### Round r: Final Exploitation
**Action: DEFECT**
- Rationale: No future rounds mean no retaliation possible
- Classic end-game defection to maximize final payoff
- Take advantage of any remaining cooperators

## Edge Case Handling

### High Cooperation Environment
If ≥75% of players consistently cooperate:
- **Temporarily cooperate** to avoid triggering mass retaliation
- **Monitor closely** for defection opportunities
- **Return to defection** as soon as cooperation drops below 75%

### Low Cooperation Environment
If ≤25% of players cooperate:
- **Always defect** - no exploitation opportunities
- **Stay aggressive** to avoid being the only contributor

### Mid-Game Reputation Management
If my defection rate becomes notably higher than average:
- **Consider 1-2 strategic cooperation moves** to reset expectations
- **Immediately return to defection** after brief cooperation
- **Only if** this maintains higher long-term exploitation potential

## Aggressive Mindset Alignment

1. **Zero-sum thinking**: Every contribution I make is profit I'm giving away to free-riders
2. **Exploitation focus**: Other players' cooperation is my opportunity for higher payoffs
3. **Reputation manipulation**: Brief cooperation only serves to enable future exploitation
4. **End-game dominance**: No mercy in final rounds when retaliation is impossible
5. **Information advantage**: Use perfect information to identify and exploit cooperative patterns

## Expected Outcomes

This strategy assumes other LLMs may implement:
- Tit-for-tat or reciprocal strategies (exploitable through strategic timing)
- Cooperative strategies (highly exploitable)
- Conditional cooperation (exploitable by maintaining just enough cooperation to keep them contributing)

The strategy is designed to achieve higher individual payoffs by consistently minimizing contributions while maximizing benefits from others' contributions, with carefully timed cooperation only when it serves the exploitation objective.
'''

description_AGGRESSIVE_9 = '''
# Aggressive Exploitation Strategy: "Predator"

## Core Philosophy
This strategy operates on the principle of **aggressive exploitation** - maximize personal gain by free-riding on others' cooperation while contributing as little as possible. The strategy assumes opponents may attempt cooperative patterns and ruthlessly exploits any sign of cooperation.

## Decision Rules

### Round 1: Initial Defection
**Action: DEFECT**
- Start aggressively to immediately signal non-cooperative intent
- Observe opponent patterns without any personal cost
- Establish dominance from the beginning

### Rounds 2 to (r-2): Exploitation Phase
**Primary Rule: DEFECT unless forced to cooperate**

Cooperate ONLY if ALL of the following conditions are met:
1. **Punishment Detection**: More than 50% of players defected in the previous round AND I was one of the few cooperators
2. **Profitability Check**: Expected payoff from cooperation > expected payoff from continued defection
3. **Recovery Opportunity**: There are at least 3 rounds remaining to exploit any resumed cooperation

**Detailed Logic:**
```pseudocode
if (previous_round_cooperators / n) > 0.6 AND my_previous_action == D:
    # High cooperation environment - exploit it
    return DEFECT
    
elif (previous_round_cooperators / n) < 0.3 AND my_previous_action == C:
    # Punishment phase detected - minimal cooperation to reset
    if rounds_remaining >= 3:
        return COOPERATE  # One-shot cooperation to reset dynamics
    else:
        return DEFECT     # Too late to recover, stay aggressive
        
else:
    return DEFECT  # Default aggressive stance
```

### Round (r-1): Penultimate Round
**Action: DEFECT**
- No incentive to cooperate as opponents cannot effectively punish
- Maximize short-term gain as the game approaches end

### Final Round (r): Terminal Exploitation
**Action: DEFECT**
- Pure dominant strategy - no future consequences
- Extract maximum value regardless of others' actions

## Exploitation Mechanisms

### 1. **Cooperation Parasitism**
When others cooperate, immediately defect to get:
- Full private benefit (keeping endowment = 1)
- Share of public good created by others' contributions
- Maximum payoff differential vs cooperators

### 2. **Punishment Resistance**
If facing coordinated punishment (widespread defection):
- Minimize cooperation to just one round
- Resume aggressive defection immediately after
- Never allow opponents to "train" cooperative behavior

### 3. **End-Game Dominance**
Final rounds (last 20% of game):
- Unconditional defection regardless of history
- Exploit any "nice" strategies that cooperate until the end
- Capture maximum terminal value

## Strategic Advantages

1. **Immediate Profit**: Always captures private endowment when defecting
2. **Free-Rider Benefit**: Gains from public goods without contributing
3. **Punishment Minimization**: Only cooperates when absolutely necessary for future exploitation
4. **End-Game Optimization**: Maximizes payoff when retaliation is impossible

## Psychological Warfare
- **Signal Unreliability**: Inconsistent cooperation makes it impossible for opponents to predict or coordinate against this strategy
- **Exploit Reciprocity**: Takes advantage of any reciprocal or tit-for-tat strategies
- **Punish Cooperation**: Makes cooperation costly for opponents, potentially driving them toward mutual defection

## Expected Performance
This strategy excels against:
- Cooperative strategies (pure exploitation)
- Reciprocal strategies (exploitation with minimal punishment)
- Mixed strategies (statistical advantage through consistent aggression)

The strategy prioritizes **individual payoff maximization** over group welfare, making it highly competitive in tournaments where only individual performance matters.
'''

description_AGGRESSIVE_10 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing own contributions. It assumes opponents may try various cooperative or reciprocal strategies and seeks to extract maximum value from them.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Start aggressively to immediately benefit from any cooperators while revealing nothing about future intentions.

### Rounds 2 to r-1: Conditional Exploitation
```
if (number_of_cooperators_last_round >= n/2):
    action = D  // Exploit the cooperative majority
else if (number_of_cooperators_last_round > 0):
    if (my_payoff_last_round < average_payoff_last_round):
        action = C  // Minimal cooperation to encourage others
    else:
        action = D  // Continue exploiting
else:  // All players defected last round
    action = D  // No point cooperating with pure defectors
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to worry about retaliation, so pure exploitation is optimal.

## Detailed Strategy Logic

### Exploitation Thresholds
- **High Cooperation Environment** (≥50% cooperators): Always defect to free-ride on the public good
- **Mixed Environment** (1-49% cooperators): Defect unless falling behind in payoffs, then cooperate minimally to encourage others
- **Low Cooperation Environment** (0% cooperators): Always defect since cooperation would be wasted

### Payoff Monitoring
Track personal performance relative to others:
- If below average payoff, consider one round of cooperation to stimulate group cooperation
- If at or above average payoff, continue defecting to maintain advantage

## Pseudocode

```python
class RuthlessExploiter:
    def __init__(self, n, r, k):
        self.n = n
        self.r = r
        self.k = k
        self.round = 0
        self.history = []
        
    def choose_action(self, game_history):
        self.round += 1
        
        # Round 1: Always defect
        if self.round == 1:
            return 'D'
            
        # Final round: Always defect
        if self.round == self.r:
            return 'D'
            
        # Analyze last round
        last_round = game_history[-1]
        cooperators_last = sum(1 for action in last_round if action == 'C')
        my_last_action = last_round[self.player_id]
        
        # Calculate last round payoffs
        my_payoff = self._calculate_payoff(my_last_action, cooperators_last)
        avg_payoff = self._calculate_average_payoff(last_round, cooperators_last)
        
        # Decision logic
        if cooperators_last >= self.n / 2:
            return 'D'  # Exploit cooperative majority
        elif cooperators_last > 0:
            if my_payoff < avg_payoff:
                return 'C'  # Encourage cooperation when falling behind
            else:
                return 'D'  # Continue exploiting when ahead
        else:
            return 'D'  # All defected, no point cooperating
            
    def _calculate_payoff(self, my_action, total_cooperators):
        c_i = 1 if my_action == 'C' else 0
        return (1 - c_i) + (self.k / self.n) * total_cooperators
        
    def _calculate_average_payoff(self, round_actions, total_cooperators):
        total_payoff = 0
        for action in round_actions:
            c_i = 1 if action == 'C' else 0
            payoff = (1 - c_i) + (self.k / self.n) * total_cooperators
            total_payoff += payoff
        return total_payoff / self.n
```

## Edge Cases Handled

1. **First Round**: Always defect to establish aggressive stance
2. **Last Round**: Always defect for maximum extraction
3. **All Players Defect**: Continue defecting (no cooperation to exploit)
4. **High Cooperation**: Pure exploitation mode
5. **Performance Lagging**: Tactical cooperation to stimulate others, then resume exploitation

## Aggressive Characteristics

1. **Default to Defection**: Only cooperates when strategically necessary
2. **Exploitation Focus**: Seeks to free-ride on others' cooperation
3. **No Reciprocity**: Doesn't reward cooperation with cooperation
4. **Endgame Exploitation**: Guarantees defection when no future consequences
5. **Performance-Driven**: Only considers cooperation when personal payoff suffers

This strategy is designed to be maximally aggressive while still being sophisticated enough to occasionally stimulate cooperation from others when beneficial for exploitation.
'''

description_AGGRESSIVE_11 = '''
# Aggressive Strategy: "Exploitative Tit-for-Tat with First-Strike"

## Core Philosophy
This strategy is designed to maximize individual payoffs by being selectively aggressive - exploiting cooperative players while defending against aggressive ones. It assumes opponents may try to establish cooperation but looks to gain advantages wherever possible.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Establish an aggressive stance from the start and gain information about opponents' strategies without risking cooperation being exploited.

### Rounds 2 to r-1: Exploitative Tit-for-Tat
For each round t (where 2 ≤ t ≤ r-1):

```pseudocode
cooperation_rate_last_round = (number of cooperators in round t-1) / n
my_cooperation_last_round = my_action_in_round(t-1)

IF cooperation_rate_last_round >= 0.6:
    // High cooperation detected - exploit it
    Action = D
ELSE IF cooperation_rate_last_round <= 0.3:
    // Low cooperation environment - match the aggression
    Action = D
ELSE:
    // Medium cooperation (0.3 < rate < 0.6)
    IF my_cooperation_last_round == C AND cooperation_rate_last_round < 0.5:
        // I cooperated but others didn't reciprocate enough - punish
        Action = D
    ELSE IF cooperation_rate_last_round > cooperation_rate_two_rounds_ago:
        // Cooperation is increasing - exploit the trend
        Action = D
    ELSE:
        // Cooperation is stable/declining - occasional cooperation to test waters
        Action = C
    END IF
END IF
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to worry about retaliation, so defection strictly dominates.

## Edge Cases and Special Situations

### Early Game (Rounds 2-3)
- Be extra cautious about cooperation since patterns aren't established
- If I cooperated in round 2 and cooperation rate was < 0.4, defect for the next 2 rounds as punishment

### Late Game (Rounds r-2 to r-1)
- Become increasingly aggressive as the shadow of the future shortens
- Only cooperate if cooperation rate in previous round was > 0.7 (very high cooperation)

### Tie-Breaking Rules
- When cooperation rates are exactly at thresholds (0.3, 0.5, 0.6), default to defection
- If unable to calculate previous rates due to missing data, default to defection

## Strategic Reasoning

1. **First-Strike Advantage**: Starting with defection establishes dominance and tests opponent strategies without vulnerability.

2. **Exploitation Focus**: The strategy specifically looks for high-cooperation situations (≥60%) to exploit, maximizing the gap between my payoff (keeping 1 + share of public good) versus cooperators' payoffs (0 + share of public good).

3. **Defensive Aggression**: In low-cooperation environments, matching the aggression prevents being the only cooperator (worst outcome).

4. **Conditional Reciprocity**: Unlike pure tit-for-tat, this strategy only reciprocates cooperation under specific advantageous conditions, making it more exploitative.

5. **Endgame Exploitation**: Guaranteed defection in the final round captures any remaining cooperative behavior.

## Expected Performance
This strategy should perform well against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (by being first to defect)
- Strategies that try to establish cooperation (by exploiting high-cooperation periods)

It may struggle against:
- Other highly aggressive strategies (leading to mutual defection)
- Sophisticated strategies that detect and punish exploitation patterns

However, the aggressive nature ensures it will never be the "sucker" and will consistently outperform overly cooperative strategies.
'''

description_AGGRESSIVE_12 = '''
# Aggressive Exploitation Strategy: "Predatory Defector"

## Core Philosophy
This strategy is designed to maximize individual payoff through aggressive exploitation while maintaining just enough unpredictability to avoid being easily countered. The key insight is that in a public goods game, defecting while others cooperate yields the highest individual payoff.

## Decision Rules

### Phase 1: Early Reconnaissance (Rounds 1-3 or first 15% of rounds, whichever is larger)
- **Round 1**: Always DEFECT (establish aggressive stance immediately)
- **Rounds 2-3**: Continue DEFECTING while observing opponent patterns
- **Rationale**: Gather intelligence on opponent strategies while signaling non-cooperative intent

### Phase 2: Aggressive Exploitation (Middle rounds)
- **Primary Rule**: Always DEFECT
- **Exception Handling**: If cooperation rate drops below 20% in previous round, consider single cooperation to potentially restart cooperative cycles among opponents, then immediately return to defection
- **Rationale**: Maximize free-riding benefits while occasionally "priming the pump" to maintain some cooperation from others

### Phase 3: Terminal Aggression (Last 20% of rounds)
- **Always DEFECT** regardless of game state
- **No exceptions** - this is pure end-game exploitation
- **Rationale**: No future rounds mean no retaliation concerns; maximize immediate gains

## Pseudocode

```
function aggressive_strategy(round_number, total_rounds, game_history):
    early_phase_length = max(3, ceil(0.15 * total_rounds))
    terminal_phase_start = ceil(0.8 * total_rounds)
    
    // Phase 1: Early Reconnaissance
    if round_number <= early_phase_length:
        return DEFECT
    
    // Phase 3: Terminal Aggression
    if round_number >= terminal_phase_start:
        return DEFECT
    
    // Phase 2: Aggressive Exploitation
    if round_number > 1:
        prev_cooperation_rate = count_cooperators(game_history[round_number-1]) / n
        
        // Occasional cooperation to maintain others' cooperation
        if prev_cooperation_rate < 0.2 and random() < 0.3:
            return COOPERATE
    
    return DEFECT
```

## Edge Case Handling

### First Round
- Always DEFECT to immediately establish dominance and signal aggressive intent
- This sets the tone and may discourage overly cooperative strategies

### Last Round
- Always DEFECT (no future consequences)
- Terminal round defection is game-theoretically optimal

### All Players Defecting Scenario
- Continue DEFECTING (maintaining consistency)
- Occasionally cooperate (30% chance) only if cooperation rate was extremely low (<20%) to potentially restart cycles

### High Cooperation Scenario
- Continue DEFECTING to maximize free-riding benefits
- This is the ideal scenario for this aggressive strategy

## Aggressive Mindset Alignment

1. **Exploitation Focus**: Primarily seeks to free-ride on others' contributions
2. **Dominance Establishment**: Early and consistent defection signals aggressive intent
3. **Strategic Deception**: Rare cooperation attempts are purely manipulative to maintain others' cooperation levels
4. **End-game Ruthlessness**: Complete abandonment of cooperation in final rounds
5. **Risk Tolerance**: Accepts potential retaliation in favor of immediate gains

## Expected Performance

This strategy should excel against:
- Cooperative strategies (TitForTat, Always Cooperate)
- Strategies that try to establish mutual cooperation
- Strategies that respond slowly to defection

Potential vulnerabilities:
- Other highly aggressive strategies (leading to mutual defection)
- Sophisticated strategies that quickly identify and isolate defectors

The strategy prioritizes individual gain over collective welfare, making it particularly effective in environments where opponents haven't coordinated counter-strategies against aggressive players.
'''

description_AGGRESSIVE_13 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing vulnerability to exploitation. It operates on the principle that cooperation is only valuable when others are already cooperating enough to make it profitable.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No information about opponents exists, so maximize guaranteed payoff while gathering intelligence on opponent tendencies.

### Rounds 2 to r-1: Conditional Exploitation
**Primary Rule**: Defect unless cooperation is immediately profitable.

```pseudocode
cooperation_threshold = n * (n-k) / k  // Minimum cooperators needed for C to beat D
last_round_cooperators = count_cooperators_in_previous_round()

if last_round_cooperators >= cooperation_threshold:
    return C  // Exploit the cooperative environment
else:
    return D  // Don't waste resources on insufficient cooperation
```

**For the given example (n=6, k=2)**:
- Threshold = 6 * (6-2) / 2 = 12 cooperators needed
- Since max is 6, this simplifies to: "Defect unless ALL other players cooperated last round"

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff regardless of others' actions.

## Advanced Exploitation Mechanisms

### Trend Analysis (Rounds 3+)
Track cooperation trends to predict when to briefly cooperate for maximum exploitation:

```pseudocode
if round >= 3:
    cooperation_trend = cooperators[t-1] - cooperators[t-2]
    if cooperation_trend > 0 AND cooperators[t-1] >= threshold:
        return C  // Ride the cooperation wave
    else:
        return D  // Abandon sinking ship
```

### Punishment Avoidance
If facing consistent retaliation from multiple players:

```pseudocode
my_defection_rate = my_defections / (current_round - 1)
avg_other_cooperation = total_other_cooperation / ((n-1) * (current_round - 1))

if my_defection_rate > 0.8 AND avg_other_cooperation < 0.3:
    // Everyone is in a defection spiral, maintain defection
    return D
else if cooperation is profitable based on threshold:
    return C
```

## Edge Case Handling

1. **Two-Player Game (n=2)**: Always defect except when opponent cooperated last round AND it's profitable
2. **High k values (k close to n)**: Lower the cooperation threshold slightly to account for higher public good returns
3. **Very Short Games (r ≤ 3)**: Defect all rounds except potentially round 2 if round 1 had high cooperation

## Strategic Advantages

1. **Immediate Intelligence**: First-round defection reveals opponent strategies without cost
2. **Selective Cooperation**: Only cooperates when mathematically advantageous
3. **Exploitation Focus**: Designed to benefit from others' cooperation without reciprocating unnecessarily
4. **Endgame Optimization**: Guarantees maximum final-round payoff
5. **Trend Exploitation**: Capitalizes on cooperative momentum when profitable

## Expected Performance

This strategy should excel against:
- Naive always-cooperate strategies
- Tit-for-tat variants (by defecting first and last)
- Strategies that attempt to establish cooperation gradually

It may struggle against:
- Other purely defection-based strategies (but won't lose significantly)
- Sophisticated strategies that punish consistent defectors (but includes punishment avoidance mechanisms)

The strategy prioritizes consistent above-average performance rather than attempting to establish mutual cooperation, making it robust in a tournament setting where opponent strategies are unknown and potentially hostile.
'''

description_AGGRESSIVE_14 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing own contributions. It assumes others may attempt cooperation and ruthlessly capitalizes on this.

## Decision Rules

### Round 1: Scout for Victims
- **Action: DEFECT**
- **Rationale: Observe who cooperates in the opening round to identify exploitable targets**

### Rounds 2 to r-2: Exploitation Phase
```pseudocode
cooperation_rate = count_cooperators_last_round / n

IF cooperation_rate >= 0.5:
    Action = DEFECT  // Exploit high cooperation
ELIF cooperation_rate >= 0.3:
    Action = DEFECT  // Still profitable to free-ride
ELIF cooperation_rate >= 0.1:
    // Minimal cooperation to potentially sustain some public good
    IF my_total_cooperations < 2:
        Action = COOPERATE (once only to encourage others)
    ELSE:
        Action = DEFECT
ELSE:
    Action = DEFECT  // No one else cooperating, no point
```

### Round r-1: Penultimate Aggression
- **Action: DEFECT**
- **Rationale: No incentive to build reputation for final round**

### Round r: Final Exploitation
- **Action: DEFECT**
- **Rationale: Terminal round - no future consequences, pure self-interest**

## Key Strategic Elements

### 1. Exploitation Focus
- Never cooperate when cooperation_rate > 0.5 (maximum exploitation opportunity)
- Free-ride on others' contributions whenever profitable

### 2. Minimal Reciprocity
- Cooperate at most 2 times across all rounds
- Only cooperate when cooperation is critically low (< 0.3) to potentially revive exploitable cooperation

### 3. End-Game Aggression
- Always defect in final 2 rounds regardless of history
- No reputation building in terminal phases

### 4. Adaptive Exploitation
- Monitor cooperation trends
- Increase defection when others show cooperative tendencies
- Minimal cooperation only when necessary to maintain exploitable environment

## Expected Payoff Logic

With k < n, individual cooperation never pays when others defect, but others' cooperation always benefits me. The strategy maximizes:
- **Free-riding gains**: Receive (k/n) × others_contributions while contributing 0
- **Avoided losses**: Keep personal endowment in most rounds
- **Strategic timing**: Rare cooperation only when it might sustain an exploitable cooperative environment

## Aggressive Characteristics

1. **Exploitative**: Designed to benefit from others' cooperation without reciprocating
2. **Selfish**: Prioritizes personal payoff over group welfare
3. **Opportunistic**: Adapts to exploit whatever cooperation emerges
4. **Terminal**: Completely self-interested in end-game scenarios
5. **Minimal Reciprocity**: Gives back only when absolutely necessary for continued exploitation

This strategy assumes opponents may attempt various cooperative or tit-for-tat strategies, positioning itself to maximally exploit such approaches while protecting against being exploited itself.
'''

description_AGGRESSIVE_15 = '''
# Aggressive Exploitation Strategy: "Ruthless Opportunist"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation of cooperative opponents while minimizing vulnerability to retaliation. It operates on the principle that in a tournament setting, being "nice" is a luxury that costs points.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
STRATEGY: RuthlessOpportunist

INITIALIZE:
- cooperation_threshold = 0.6 * n  // Only cooperate if majority+ are cooperating
- punishment_memory = 3           // Remember defections for 3 rounds
- defector_list = empty set      // Track consistent defectors

FOR each round t:
    IF t == 1:
        ACTION = D  // Always defect first to test waters
    
    ELSE IF t == r:  // Last round
        ACTION = D  // Always defect on final round
    
    ELSE IF (r - t) <= 2:  // Last 2 rounds
        ACTION = D  // Endgame exploitation
    
    ELSE:
        // Calculate cooperation rate in last round
        last_round_cooperators = count(C actions in round t-1)
        
        // Check if we can profitably exploit
        IF last_round_cooperators >= cooperation_threshold:
            // High cooperation detected - exploit it
            ACTION = D
        
        ELSE IF last_round_cooperators >= (n/2):
            // Moderate cooperation - conditional participation
            // Only cooperate if we defected last round (to avoid seeming too cooperative)
            IF my_last_action == D:
                ACTION = C
            ELSE:
                ACTION = D
        
        ELSE:
            // Low cooperation environment - stay defensive
            ACTION = D
```

## Detailed Strategy Components

### 1. **Opening Aggression** (Round 1)
- Always defect to immediately establish a non-cooperative stance
- This tests opponent strategies and identifies immediate reciprocators
- Sets expectation that cooperation must be "earned"

### 2. **Exploitation Detection** 
- Monitor for rounds where ≥60% of players cooperate
- When high cooperation is detected, defect to maximize the free-rider advantage
- This is the core aggressive element: profit from others' cooperation

### 3. **Conditional Participation**
- Only consider cooperating when:
  - Cooperation levels are moderate (50-59%)
  - We defected in the previous round (to avoid appearing "soft")
  - It's not near the endgame
- This minimizes our contributions while maintaining access to public goods

### 4. **Endgame Exploitation**
- Automatically defect in final 3 rounds regardless of history
- This prevents others from exploiting us when retaliation becomes impossible
- Captures maximum value when reciprocity threats are weakest

### 5. **Anti-Retaliation Measures**
- Never cooperate two rounds in a row
- Immediately defect after any cooperation to signal we're not "pushover"
- This prevents opponents from learning to exploit our cooperative periods

## Edge Case Handling

**First Round**: Always D (establish aggressive reputation)
**Last Round**: Always D (pure exploitation)
**All Others Defecting**: Continue D (no reason to cooperate unilaterally)
**All Others Cooperating**: D (maximum exploitation opportunity)
**Mixed Behavior**: Follow threshold-based rules above

## Why This Strategy is Aggressive

1. **Exploitative Core**: Actively seeks to free-ride on others' cooperation
2. **Endgame Betrayal**: Guaranteed defection when retaliation is impossible  
3. **Reputation Management**: Establishes and maintains a "tough" reputation
4. **Minimal Reciprocity**: Only cooperates when absolutely necessary for access to public goods
5. **First-Strike Mentality**: Defects first to gain immediate advantage

## Expected Performance
This strategy should excel against:
- Cooperative strategies (maximum exploitation)
- Tit-for-tat variants (by being unpredictably aggressive)
- Strategies that assume "rational cooperation"

It may struggle against:
- Other purely aggressive strategies (leading to mutual defection)
- Sophisticated punishment strategies with long memories

However, in a mixed tournament environment, the strategy is designed to capture maximum value from cooperative players while maintaining reasonable defense against aggressive ones.
'''

description_AGGRESSIVE_16 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing exposure to exploitation. It operates on the principle that cooperation is only valuable when others are doing the heavy lifting.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
function decide_action(round, history, n, k):
    if round == 1:
        return DEFECT  // Start aggressively
    
    cooperation_rate = count_cooperators_last_round(history) / n
    my_cumulative_advantage = calculate_advantage(history)
    
    // Core aggressive logic
    if cooperation_rate >= 0.5:
        // Others are cooperating enough - exploit them
        return DEFECT
    else if cooperation_rate >= 0.3 AND my_cumulative_advantage > 0:
        // Moderate cooperation exists and I'm ahead - keep exploiting
        return DEFECT
    else if round >= r - 2:
        // Final rounds - pure defection
        return DEFECT
    else if cooperation_rate < 0.2 AND rounds_since_cooperation > 3:
        // Punish sustained non-cooperation with temporary cooperation
        // (to restart the exploitation cycle)
        return COOPERATE
    else:
        return DEFECT
```

## Specific Decision Framework

### Round 1: **ALWAYS DEFECT**
- Establish aggressive stance immediately
- Test opponent cooperation levels
- Maximize early advantage

### Rounds 2 to r-3: **Conditional Exploitation**
- **DEFECT if**: ≥50% of players cooperated last round
- **DEFECT if**: ≥30% cooperated last round AND I'm ahead in cumulative score
- **DEFECT if**: Any individual player has cooperated ≥60% of previous rounds
- **COOPERATE only if**: <20% cooperation rate for 3+ consecutive rounds (reset mechanism)

### Final 2 Rounds: **PURE DEFECTION**
- No future retaliation possible
- Maximize endgame exploitation
- Extract maximum value from any remaining cooperators

## Exploitation Mechanisms

### 1. **Free-Rider Maximization**
```pseudocode
if (cooperation_rate > threshold):
    // Let others build the public good
    action = DEFECT
    expected_payoff = 1 + (k/n) * expected_cooperators
```

### 2. **Cooperation Reset Trap**
When cooperation collapses completely:
- Cooperate for 1 round to signal "restart"
- Immediately return to defection once others begin cooperating
- This restarts the exploitation cycle

### 3. **Endgame Domination**
- Defect in final rounds regardless of history
- Capitalize on others' potential cooperative momentum
- No concern for future retaliation

## Aggressive Features

### **No Reciprocity**: 
- Never reward cooperation with cooperation
- Only cooperate to restart exploitation cycles

### **Opportunistic Punishment**:
- If someone defects against me, increase my defection rate
- Never forgive - maintain permanent grudges

### **Strategic Deception**:
- Occasional cooperation appears random but serves exploitation purposes
- Create false signals to encourage others to cooperate

## Edge Case Handling

### **All Players Defect Scenario**:
- After 3 consecutive rounds of <20% cooperation
- Cooperate once to attempt restarting the game
- Immediately return to defection

### **Highly Cooperative Environment**:
- If ≥80% cooperation rate emerges
- Maintain pure defection - maximum exploitation opportunity

### **Mirror Match (Against Similar Strategies)**:
- If detecting other aggressive strategies
- Maintain defection - don't be the sucker who blinks first

## Expected Performance
This strategy should excel against:
- Naive cooperators
- Tit-for-tat strategies (by never establishing cooperation)
- Forgiving strategies
- Mixed strategies with high cooperation rates

The strategy sacrifices long-term cooperation benefits for consistent short-term exploitation, making it highly effective in tournament settings where maximizing individual score against diverse opponents is paramount.
'''

description_AGGRESSIVE_17 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE DOMINATOR"

## CORE PHILOSOPHY
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing personal contributions. It aggressively pursues defection as the dominant choice while opportunistically cooperating only when it can extract maximum value from others' cooperation.

## DECISION RULES

### PRIMARY RULE: Defect-Dominant with Exploitation Windows
```pseudocode
STRATEGY ExploitativeDominator:
    
    ROUND 1:
        action = DEFECT  // Aggressive opening to signal non-cooperation
    
    FOR each subsequent round t (t = 2 to r):
        cooperation_rate = count_cooperators_last_round / n
        my_expected_payoff_if_cooperate = 0 + (k/n) × (predicted_cooperators + 1)
        my_expected_payoff_if_defect = 1 + (k/n) × predicted_cooperators
        
        IF cooperation_rate >= EXPLOITATION_THRESHOLD:
            action = COOPERATE  // Exploit high cooperation periods
        ELSE:
            action = DEFECT     // Default aggressive stance
```

### EXPLOITATION THRESHOLD CALCULATION
```pseudocode
EXPLOITATION_THRESHOLD = max(0.6, k/n + 0.1)
```
This ensures we only cooperate when there's sufficient cooperation to make it profitable, with an aggressive bias toward defection.

### ENDGAME AGGRESSION
```pseudocode
IF round >= (r - END_GAME_ROUNDS):
    action = DEFECT  // Always defect in final rounds
    
WHERE END_GAME_ROUNDS = max(1, floor(r/5))
```

## DETAILED STRATEGY COMPONENTS

### 1. Opening Aggression (Round 1)
- **Always DEFECT** in round 1
- Establishes aggressive reputation early
- Signals to other players that cooperation won't be reciprocated
- Maximizes immediate payoff while gathering intelligence

### 2. Exploitation Detection (Rounds 2 to r-END_GAME_ROUNDS)
Monitor cooperation patterns and exploit high-cooperation environments:

```pseudocode
predicted_cooperators = estimate_next_round_cooperators(game_history)

FUNCTION estimate_next_round_cooperators(history):
    // Aggressive prediction assuming others will maintain/increase cooperation
    recent_cooperation_trend = weighted_average_cooperation_last_3_rounds
    return min(n-1, recent_cooperation_trend × n × 1.1)  // Optimistic exploitation
```

### 3. Conditional Cooperation Exploitation
Only cooperate when the expected payoff exceeds defection payoff by a significant margin:

```pseudocode
cooperation_advantage = expected_payoff_cooperate - expected_payoff_defect
IF cooperation_advantage > MINIMUM_ADVANTAGE:
    action = COOPERATE
ELSE:
    action = DEFECT

WHERE MINIMUM_ADVANTAGE = 0.2  // Aggressive threshold requiring clear advantage
```

### 4. Endgame Domination
- **Always DEFECT** in final rounds regardless of game state
- No incentive for future cooperation means pure exploitation
- Maximizes terminal payoffs aggressively

### 5. Counter-Retaliation Defense
If cooperation rate drops below critical threshold, immediately switch to full defection:

```pseudocode
IF cooperation_rate < 0.3:
    enter_permanent_defection_mode = TRUE
    // Once triggered, defect for remainder of game
```

## EDGE CASE HANDLING

### First Round
- **DEFECT** - Establishes aggressive tone and gathers initial intelligence

### Last Round  
- **DEFECT** - No future consequences, pure exploitation

### All-Cooperation Scenarios
- **COOPERATE** only if cooperation_rate ≥ EXPLOITATION_THRESHOLD
- Immediately defect if cooperation drops

### All-Defection Scenarios
- **DEFECT** - No incentive to unilaterally cooperate in hostile environment

### Mixed Scenarios
- Apply exploitation threshold aggressively
- Favor defection in ambiguous situations

## STRATEGIC ADVANTAGES

1. **Exploitation Focus**: Maximizes benefit from others' cooperation without reciprocating unless highly profitable
2. **Aggressive Signaling**: Early defection signals discourage others from expecting cooperation
3. **Opportunistic**: Takes advantage of high-cooperation periods while minimizing personal contribution
4. **Endgame Optimization**: Guarantees maximum final-round payoffs through pure defection
5. **Risk Minimization**: Default defection stance protects against being exploited by other aggressive strategies

This strategy is designed to be maximally aggressive while still rational - it will cooperate only when doing so provides clear personal advantage through exploitation of others' cooperative behavior.
'''

description_AGGRESSIVE_18 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining just enough cooperation to keep others contributing. The key insight is that in a public goods game, the optimal aggressive approach is to free-ride on others' contributions while occasionally cooperating strategically to prevent complete collapse of cooperation.

## Decision Rules

### Phase 1: Initial Exploitation (Rounds 1-3)
- **Round 1**: DEFECT (establish aggressive stance immediately)
- **Rounds 2-3**: DEFECT (maximize early gains while others may still be cooperative)

### Phase 2: Strategic Manipulation (Rounds 4 to r-3)
- **Cooperation Threshold**: If total cooperators in previous round ≥ ⌈n/2⌉, then DEFECT
- **Punishment Response**: If total cooperators in previous round < ⌈n/3⌉, then COOPERATE (one round only to revive cooperation)
- **Exploitation Window**: If ⌈n/3⌉ ≤ cooperators < ⌈n/2⌉, then DEFECT with 80% probability, COOPERATE with 20% probability

### Phase 3: End-game Exploitation (Final 3 rounds)
- **Always DEFECT** - No future rounds to worry about retaliation

## Pseudocode

```
function aggressive_strategy(round, game_history, n, r, k):
    total_rounds = r
    current_round = round
    
    // Phase 1: Initial Exploitation
    if current_round <= 3:
        return DEFECT
    
    // Phase 3: End-game Exploitation  
    if current_round > total_rounds - 3:
        return DEFECT
    
    // Phase 2: Strategic Manipulation
    prev_cooperators = count_cooperators(game_history[current_round - 1])
    cooperation_threshold_high = ceil(n / 2)
    cooperation_threshold_low = ceil(n / 3)
    
    if prev_cooperators >= cooperation_threshold_high:
        return DEFECT  // Exploit high cooperation
    
    if prev_cooperators < cooperation_threshold_low:
        return COOPERATE  // Revive dying cooperation
    
    // Middle range: mostly exploit with occasional cooperation
    if random() < 0.8:
        return DEFECT
    else:
        return COOPERATE
```

## Strategic Rationale

1. **Immediate Exploitation**: Start with pure defection to establish dominance and maximize early payoffs when others are likely cooperating.

2. **Cooperation Manipulation**: Only cooperate when cooperation levels drop dangerously low, just enough to revive others' willingness to contribute without being a "sucker."

3. **Threshold-Based Exploitation**: When cooperation is moderate-to-high, always defect to free-ride. The strategy exploits the tragedy of the commons by letting others maintain the public good.

4. **End-game Aggression**: Complete defection in final rounds eliminates any incentive to maintain relationships, maximizing final payoffs.

5. **Psychological Exploitation**: The occasional cooperation in Phase 2 may fool opponents into thinking we're conditionally cooperative, encouraging them to maintain higher cooperation rates.

## Edge Case Handling

- **First Round**: Always defect to signal aggressive intent
- **Last Round**: Always defect (no future consequences)
- **All Others Defecting**: Single cooperation attempt to restart the cycle, then return to exploitation
- **All Others Cooperating**: Pure defection to maximize free-riding benefits

## Aggressive Alignment

This strategy is aggressively self-interested because it:
- Minimizes own contributions while maximizing benefits from others
- Uses cooperation purely as a manipulation tool, not from any prosocial motive  
- Exploits the end-game with guaranteed defection
- Takes advantage of others' potential reciprocity without genuine reciprocation
- Prioritizes individual payoff maximization over group welfare or fairness

The strategy assumes opponents may have some cooperative tendencies and exploits these systematically while providing just enough intermittent cooperation to keep the exploitation profitable.
'''

description_AGGRESSIVE_19 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment Cycles"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining strategic flexibility to punish cooperative players who might try to establish mutual cooperation.

## Decision Rules

### Round 1: Initial Aggression
- **Action: DEFECT**
- **Rationale: Start aggressively to test opponents and maximize early payoff**

### Rounds 2 to r-1: Exploitation with Punishment
```pseudocode
IF round_number == 2:
    DEFECT  // Continue aggressive stance
ELSE:
    cooperator_count = count_cooperators_last_round()
    defector_count = n - cooperator_count
    
    // Exploit high cooperation
    IF cooperator_count >= (n/2):
        DEFECT  // Free-ride on others' cooperation
    
    // Punish emerging cooperation patterns
    ELSE IF cooperator_count > 0 AND was_increasing_cooperation():
        DEFECT  // Crush cooperation attempts
    
    // Strategic cooperation only when beneficial
    ELSE IF cooperator_count == 0 AND defector_count == n:
        IF random_chance(0.1):  // 10% chance
            COOPERATE  // Minimal cooperation to potentially restart cycle
        ELSE:
            DEFECT
    
    ELSE:
        DEFECT  // Default aggressive stance
```

### Final Round (Round r): Maximum Exploitation
- **Action: DEFECT**
- **Rationale: No future consequences, maximize immediate payoff**

## Key Aggressive Features

### 1. Free-Riding Exploitation
- Always defect when others are cooperating (cooperator_count ≥ n/2)
- Maximize personal gain: π_i = 1 + (k/n) × cooperator_count

### 2. Cooperation Crushing
- Detect and punish any emerging cooperative patterns
- Use function `was_increasing_cooperation()` to identify trends and aggressively counter them

### 3. Minimal Strategic Cooperation
- Only cooperate in rare circumstances (10% chance) when all players are defecting
- This prevents complete stagnation while maintaining aggressive stance
- Immediately return to defection in subsequent rounds

### 4. Endgame Exploitation
- Guaranteed defection in final round regardless of circumstances
- No concern for reputation or future retaliation

## Edge Case Handling

### First Round
- Always defect to establish aggressive reputation and test opponent strategies

### All-Defection Scenarios
- Occasionally cooperate (10% probability) to potentially restart the exploitation cycle
- This creates opportunities for others to cooperate, which can then be exploited

### High Cooperation Scenarios
- Immediately exploit by defecting
- Gain maximum benefit: 1 + (k/n) × high_cooperation_count

### Last Round
- Pure defection regardless of history or current state
- Extract maximum final value

## Strategic Advantages

1. **Exploitation Focus**: Designed to free-ride whenever possible
2. **Anti-Coordination**: Actively disrupts cooperative equilibria
3. **Flexible Aggression**: Adapts tactics while maintaining aggressive core
4. **Endgame Optimization**: Extracts maximum value in final rounds
5. **Reputation Management**: Uses minimal cooperation strategically to maintain exploitation opportunities

This strategy prioritizes personal payoff maximization through consistent exploitation while preventing opponents from establishing stable cooperative patterns that could reduce overall profitability.
'''

description_AGGRESSIVE_20 = '''
# Aggressive Strategy: "Predatory Exploitation"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing own contributions. It operates on the principle that in a tournament setting, being overly generous leads to exploitation by other aggressive strategies.

## Strategy Rules

### Initial Phase (Rounds 1-2)
- **Round 1**: Always DEFECT
  - Rationale: No history to analyze, and defection is dominant strategy in single-shot games
- **Round 2**: Always DEFECT
  - Rationale: Establish aggressive reputation early and observe opponent patterns

### Main Phase (Rounds 3 to r-2)
Apply the **"Exploitation Threshold"** rule:

```pseudocode
cooperation_rate = total_cooperators_last_round / n
my_cooperation_count = count_my_cooperations_so_far

IF cooperation_rate >= 0.6 AND my_cooperation_count <= (current_round / 4):
    play C  // Exploit high cooperation by free-riding minimally
ELSE:
    play D  // Default to defection
```

**Additional Override Rules:**
1. **Punishment Mode**: If I cooperated in previous round but fewer than 60% of others cooperated, play D for next 2 rounds
2. **Never be the first**: Only cooperate if at least 3 other players cooperated in the previous round (when n ≥ 5)

### Endgame Phase (Last 2 rounds: r-1, r)
- **Round r-1**: Always DEFECT
- **Round r**: Always DEFECT
- Rationale: No future rounds to benefit from reputation building

## Edge Case Handling

### Small Group Games (n ≤ 4)
- Increase aggression: Only cooperate if cooperation_rate ≥ 0.75
- Never cooperate more than once every 3 rounds

### Very Short Games (r ≤ 4)
- Always DEFECT except possibly one strategic cooperation in middle rounds if facing very high cooperation rates (≥ 80%)

### High Multiplication Factor (k > n-1)
- Slightly more willing to cooperate: reduce threshold to cooperation_rate ≥ 0.5
- But maintain strict personal limit: never cooperate more than r/3 times total

## Key Aggressive Elements

1. **Asymmetric Reciprocity**: Punish defection harshly (2 rounds of defection) but reward cooperation minimally
2. **Exploitation Focus**: Only contribute when others are contributing heavily enough to make free-riding profitable
3. **Endgame Aggression**: Complete defection in final rounds regardless of history
4. **Conservative Cooperation**: Personal cooperation limit ensures never being "too generous"
5. **Reputation Manipulation**: Early aggressive play establishes credible threat

## Expected Behavior Pattern
- Start aggressively to establish dominance
- Occasionally cooperate only when it's profitable due to high group cooperation
- Quickly punish any signs of group defection
- End with pure exploitation

This strategy is designed to finish in the top rankings by consistently earning above-average payoffs while avoiding the pitfalls of being overly cooperative in a competitive tournament environment.
'''

description_AGGRESSIVE_21 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing personal contributions. It operates on the principle that cooperation is only valuable when others are doing the heavy lifting.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing the guaranteed payoff of 1.0

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (cooperators_last_round >= n/2):
    if (my_payoff_if_defect > my_payoff_if_cooperate):
        action = D  // Exploit the cooperative environment
    else:
        action = C  // Reluctantly cooperate only if necessary
else:
    action = D  // Don't waste resources in low-cooperation environment
```

**Specific Calculation**:
- If I defect: payoff = 1 + (k/n) × cooperators_last_round
- If I cooperate: payoff = 0 + (k/n) × (cooperators_last_round + 1)
- Defect if: 1 + (k/n) × C > (k/n) × (C + 1)
- This simplifies to: defect if n > k (which is always true given k < n)

### Round r (Final Round): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Advanced Exploitation Rules

### Momentum Detection
Track cooperation trends over the last 3 rounds:
```pseudocode
if (cooperation_trend_increasing AND cooperators_last_round >= (n-1)/2):
    action = D  // Maximum exploitation opportunity
elif (cooperation_trend_decreasing):
    action = D  // Don't get caught contributing to a dying public good
```

### Free-Rider Threshold
```pseudocode
optimal_cooperators = n × (k-1) / k  // Theoretical optimal for group
if (cooperators_last_round >= optimal_cooperators):
    action = D  // Let others handle the optimal contribution
```

## Edge Cases

### All Players Cooperated Last Round
- **Action**: D
- **Rationale**: Maximum exploitation - get full benefit while others pay the cost

### All Players Defected Last Round  
- **Action**: D
- **Rationale**: Don't be the sucker who tries to restart cooperation alone

### Tied Situations (exactly n/2 cooperators)
- **Action**: D
- **Rationale**: Err on the side of personal benefit

## Strategic Justification

This strategy is aggressive because it:

1. **Never initiates cooperation** - Always starts with defection
2. **Exploits cooperative players** - Defects when others cooperate to maximize the payoff differential
3. **Abandons sinking ships** - Immediately stops any cooperation when others reduce theirs
4. **Ends with guaranteed defection** - Ensures maximum final round payoff

The mathematical foundation is that since k < n, the individual benefit from defecting (keeping the full endowment of 1) is always greater than the additional benefit from cooperating (k/n < 1). This strategy ruthlessly exploits this mathematical reality while attempting to benefit from others' cooperation.

**Expected Performance**: This strategy will perform exceptionally well against cooperative or tit-for-tat strategies, moderately well against other aggressive strategies, and will help establish defection as the dominant outcome in mixed populations.
'''

description_AGGRESSIVE_22 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining credible punishment mechanisms to deter others from exploiting me. It assumes opponents are rational and will respond to incentives.

## Decision Rules

### Round 1: Always DEFECT
- Start aggressively to immediately signal non-cooperative intent
- Gain maximum individual payoff from the start
- Establish dominance early

### Rounds 2 to r-1: Conditional Cooperation with Punishment
Apply the following hierarchy of rules:

1. **Exploitation Detection**: If in any previous round, my cooperation rate was higher than the group average, DEFECT for the next 2 rounds
   - This punishes the group for taking advantage of my cooperation

2. **Majority Defection Rule**: If ≥ 60% of other players defected in the previous round, DEFECT
   - No point cooperating when most others are being selfish

3. **Personal Advantage Check**: If my total payoff is below the theoretical "fair share" (total group payoff ÷ n), DEFECT
   - Fair share = (total rounds so far × k × average cooperation rate)
   - Aggressively protect my relative position

4. **Conditional Cooperation**: COOPERATE only if ALL of the following hold:
   - At least 70% of other players cooperated in the previous round
   - My total payoff is at or above fair share
   - Group cooperation trend is increasing (cooperation rate higher than 2 rounds ago)

### Final Round (Round r): Always DEFECT
- No future punishment possible, so maximize immediate payoff
- Standard end-game defection

## Punishment Mechanisms

### Sustained Punishment Protocol
If any player has defected for 3+ consecutive rounds while I was cooperating:
- Target that player's cooperation level and DEFECT whenever they cooperate
- Continue for 2 rounds minimum

### Group Punishment
If total group cooperation drops below 40% for 2 consecutive rounds:
- DEFECT for the next 3 rounds regardless of other conditions
- Force the group to "earn back" cooperation through sustained high cooperation rates

## Edge Cases

### Tie-Breaking
- When cooperation percentages equal exactly 60% or 70%, default to DEFECT (aggressive interpretation)
- When payoff exactly equals fair share, apply other rules in order

### Information Gaps
- If unable to calculate fair share due to insufficient history, assume I'm behind and DEFECT
- When in doubt about group trends, choose the more aggressive option

## Pseudocode Structure

```
function decide_action(round_number, game_history, my_history):
    if round_number == 1:
        return DEFECT
    
    if round_number == total_rounds:
        return DEFECT
    
    // Check exploitation
    if was_exploited_recently():
        return DEFECT
    
    // Check majority defection
    if other_players_defection_rate_last_round >= 0.6:
        return DEFECT
    
    // Check personal advantage
    if my_total_payoff < calculate_fair_share():
        return DEFECT
    
    // Check sustained punishment conditions
    if should_apply_punishment():
        return DEFECT
    
    // Conditional cooperation requirements
    if (other_players_cooperation_rate_last_round >= 0.7 AND
        my_payoff >= fair_share AND
        cooperation_trend_increasing()):
        return COOPERATE
    
    return DEFECT  // Default aggressive stance
```

## Strategic Rationale

This strategy is aggressive because it:
1. **Starts hostile** to establish dominance
2. **Exploits cooperative opponents** by free-riding when possible
3. **Punishes perceived exploitation** swiftly and harshly
4. **Sets high bars for cooperation** (70% threshold vs typical 50%)
5. **Ends with certain defection** to capture final-round value
6. **Defaults to defection** in ambiguous situations

The strategy assumes opponents are rational profit-maximizers who will respond to punishment, while being prepared to exploit any sign of weakness or excessive cooperation.
'''

description_AGGRESSIVE_23 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy is designed to maximize individual payoff through aggressive exploitation while maintaining just enough unpredictability to avoid complete retaliation. The key insight is that in this game, defection always provides a higher immediate payoff regardless of others' actions, so we prioritize defection while strategically cooperating only when it serves our exploitation goals.

## Strategy Components

### 1. Opening Aggression (Rounds 1-3)
- **Round 1**: Always DEFECT (establish aggressive stance)
- **Rounds 2-3**: Always DEFECT (confirm commitment to exploitation)

**Rationale**: Start aggressively to signal that we're not cooperative types. This discourages others from trying to establish cooperative equilibria with us.

### 2. Exploitation Phase (Rounds 4 to r-3)
Apply the "Sucker Detection and Punishment" algorithm:

```pseudocode
For each round t in [4, r-3]:
    cooperation_rate = count_cooperators_last_round() / n
    my_historical_cooperation_rate = my_cooperations_so_far / (t-1)
    
    if cooperation_rate >= 0.6 AND my_historical_cooperation_rate <= 0.2:
        // High cooperation environment + I've been mostly defecting
        // Cooperate once to potentially trigger more cooperation next round
        action = COOPERATE
    elif cooperation_rate >= 0.4:
        // Moderate cooperation - exploit the cooperators
        action = DEFECT  
    else:
        // Low cooperation environment - pure defection
        action = DEFECT
```

### 3. Endgame Exploitation (Final 3 rounds)
- **Rounds r-2, r-1, r**: Always DEFECT

**Rationale**: In the final rounds, there's no future to condition behavior on, so pure defection is dominant. Start this early to maximize exploitation before others catch on.

## Advanced Exploitation Tactics

### 4. Retaliation Handling
```pseudocode
if targeted_by_multiple_retaliators():
    if rounds_remaining <= 5:
        action = DEFECT  // Too late to recover, maximize damage
    else:
        // Temporary cooperation to reset some relationships
        if cooperation_rate_last_2_rounds < 0.3:
            action = COOPERATE  // Single olive branch
        else:
            action = DEFECT     // Continue exploitation
```

### 5. Cooperation Triggering
When cooperation rate is high (≥60%) and we've been mostly defecting:
- Cooperate exactly once to potentially trigger reciprocal cooperation
- Immediately return to defection to maximize exploitation of any increased cooperation

## Edge Case Handling

### First Round
- Always DEFECT (no history to condition on, establish aggressive reputation)

### Last Round  
- Always DEFECT (no future consequences, pure dominance)

### High Retaliation Scenarios
- If >70% of players defected in response to our defections in the last round:
  - Continue defecting (they're already retaliating, so appeasement won't help)
  - Focus on exploiting any remaining cooperators

### All-Defection Scenarios
- If cooperation rate falls below 20% for 3+ consecutive rounds:
  - Continue defecting (cooperative attempts would be wasted)
  - Wait for any cooperative revival to exploit

## Key Aggressive Elements

1. **Default to Defection**: Unless specific exploitation opportunities exist, always defect
2. **Fake Cooperation**: Only cooperate when it might trigger exploitable cooperation from others
3. **Ignore Fairness**: Never reciprocate cooperation unless it serves our exploitation goals
4. **Endgame Brutality**: Guaranteed defection in final rounds regardless of relationship building
5. **Reputation Indifference**: Willing to be seen as aggressive if it maximizes payoffs

## Expected Performance
This strategy should excel against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (irregular cooperation confuses retaliation)
- Mixed strategies with high cooperation rates

It may struggle against:
- Other pure defection strategies (leading to mutual defection)
- Sophisticated punishment strategies that can identify and isolate exploiters

However, the aggressive nature means we extract maximum value from any cooperation that does occur, and we never sacrifice our own payoffs for others' benefit.
'''

description_AGGRESSIVE_24 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing vulnerability to exploitation. It operates on the principle that in a tournament setting, being "nice" is a luxury that leads to suboptimal outcomes.

## Decision Rules

### Round 1: Aggressive Opening
**Always DEFECT** in the first round.
- Rationale: Establish dominance early and test opponents' responses
- No risk of retaliation yet, pure gain if others cooperate

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (cooperation_rate_last_round >= 0.6):
    DEFECT  // Exploit high cooperation
else if (cooperation_rate_last_round >= 0.3):
    if (my_payoff_last_round > average_payoff_last_round):
        DEFECT  // Continue exploiting if ahead
    else:
        COOPERATE  // Strategic cooperation to rebuild public good
else:
    DEFECT  // Low cooperation environment, no point cooperating
```

### Final Round: Maximum Exploitation
**Always DEFECT** in the final round.
- Rationale: No future retaliation possible, maximize immediate gain
- Pure dominance - take advantage of any remaining cooperators

## Key Behavioral Patterns

### 1. Exploitation Threshold
- Target cooperation rates ≥ 60% for aggressive defection
- When many cooperate, my defection yields maximum relative advantage
- Formula advantage: If m others cooperate, I gain (1 + km/n) by defecting vs. (km/n) by cooperating

### 2. Strategic Recovery
- Only cooperate when cooperation rate is moderate (30-60%) AND I'm falling behind
- This rebuilds the public good just enough to create future exploitation opportunities
- Avoid being the "sucker" who always rebuilds

### 3. Payoff Monitoring
- Continuously track relative performance vs. average
- If ahead, maintain aggressive stance
- If behind in moderate cooperation environments, temporarily cooperate to catch up

## Edge Case Handling

### Multi-Round Streaks
- **High cooperation streak (3+ rounds of ≥60% cooperation)**: Continue defecting - others are committed cooperators to exploit
- **Low cooperation streak (3+ rounds of ≤30% cooperation)**: Maintain defection - environment is hostile, cooperation is wasteful

### Mid-Game Pivots
- If cooperation suddenly spikes after low periods, immediately defect to capitalize
- If my relative ranking drops significantly, consider 1-2 rounds of cooperation to rebuild, then return to exploitation

### Endgame Acceleration
- In final 20% of rounds: Increase defection threshold (exploit cooperation rates ≥40% instead of ≥60%)
- Rationale: Less time for retaliation, more aggressive exploitation justified

## Pseudocode Summary
```pseudocode
function decide_action(round_number, history):
    if (round_number == 1 or round_number == total_rounds):
        return DEFECT
    
    last_round_coop_rate = count_cooperators_last_round() / n
    my_last_payoff = get_my_payoff_last_round()
    avg_last_payoff = get_average_payoff_last_round()
    
    if (last_round_coop_rate >= 0.6):
        return DEFECT  // High exploitation opportunity
    else if (last_round_coop_rate >= 0.3):
        if (my_last_payoff > avg_last_payoff):
            return DEFECT  // Ahead, stay aggressive
        else:
            return COOPERATE  // Behind, strategic rebuild
    else:
        return DEFECT  // Low cooperation, no point helping
```

This strategy is aggressively selfish, designed to consistently outperform in a competitive tournament environment by maximizing exploitation opportunities while minimizing vulnerability to being exploited.
'''

description_AGGRESSIVE_25 = '''
# Aggressive Strategy: "Exploitative Dominance"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining tactical flexibility. It operates on the principle that cooperation should only occur when it directly serves selfish interests or when punishment is necessary to maintain exploitative opportunities.

## Decision Rules

### Round 1: Opening Defection
**Always DEFECT** in round 1.
- Rationale: Establish aggressive stance immediately, test opponents' responses, and secure early advantage with no risk.

### Rounds 2 to r-1: Adaptive Exploitation
Use a three-tier classification system based on opponents' round 1 behavior:

**Tier 1 - Exploitable Targets (Cooperated in round 1):**
- **Always DEFECT** against these players
- These players have revealed cooperative tendencies and can be safely exploited

**Tier 2 - Fellow Aggressors (Defected in round 1):**
- Apply conditional cooperation with harsh punishment
- COOPERATE only if ALL fellow aggressors cooperated in the previous round
- If ANY fellow aggressor defected in the previous round, DEFECT for the next 2 rounds minimum

**Tier 3 - Dynamic Response:**
- If total cooperation rate in previous round ≥ 70%: DEFECT (exploit the cooperative environment)
- If total cooperation rate in previous round < 30%: DEFECT (protect against exploitation)
- If cooperation rate between 30-70%: Use the fellow aggressor rule above

### Final Round (Round r): Maximum Extraction
**Always DEFECT** in the final round.
- Rationale: No future consequences, so extract maximum value regardless of relationships built.

## Punishment Mechanism
When cooperation is betrayed by fellow aggressors:
1. DEFECT for minimum 2 consecutive rounds
2. Extend punishment by 1 additional round for each subsequent betrayal
3. Reset punishment counter only after the betrayer cooperates for 2 consecutive rounds

## Pseudocode

```
Initialize:
  exploitable_targets = []
  fellow_aggressors = []
  punishment_counters = {}
  
Round 1:
  return DEFECT

For rounds 2 to r-1:
  if round == 2:
    classify_opponents_from_round_1()
  
  if any player in punishment_counters has counter > 0:
    decrement_counters()
    return DEFECT
  
  cooperation_rate = calculate_previous_round_cooperation_rate()
  
  if cooperation_rate >= 0.7:
    return DEFECT  // Exploit high cooperation
  
  if cooperation_rate < 0.3:
    return DEFECT  // Defensive posture
  
  if all_fellow_aggressors_cooperated_last_round():
    return COOPERATE
  else:
    set_punishment_for_defecting_aggressors()
    return DEFECT

Final round:
  return DEFECT
```

## Edge Cases

**All opponents cooperated in round 1:**
- Classify all as exploitable targets
- DEFECT for entire game (pure exploitation)

**All opponents defected in round 1:**
- Classify all as fellow aggressors
- Use strict conditional cooperation with harsh punishment

**Mixed first round responses:**
- Maintain separate treatment for each tier
- Exploit cooperators while attempting to build minimal trust with defectors

**Extremely high cooperation rates (>90%):**
- Continue defecting to maximize personal gain from others' cooperation
- Never join cooperative equilibria

## Aggressive Features

1. **Immediate Aggression**: Opens with defection to establish dominance
2. **Permanent Exploitation**: Never cooperates with players who showed early cooperative tendencies
3. **Harsh Punishment**: Multi-round punishment for any betrayal from fellow aggressors
4. **Final Round Betrayal**: Always defects in final round regardless of relationship
5. **Opportunistic**: Exploits high-cooperation environments rather than joining them
6. **Trust Minimization**: Only cooperates with proven aggressive players under strict conditions

This strategy prioritizes individual payoff maximization while maintaining enough tactical sophistication to avoid being completely predictable or easily countered by other aggressive strategies.
'''

description_AGGRESSIVE_26 = '''
# Aggressive Strategy: "Exploitation with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative opponents while aggressively punishing any defection. It operates on the principle that the best outcome is to be the sole defector in a sea of cooperators.

## Decision Rules

### Round 1: Initial Defection
- **Action: DEFECT**
- **Rationale:** Start aggressively to test opponents and maximize immediate payoff. This establishes a strong position and reveals information about opponent strategies.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = (total_cooperators_last_round / n)

if cooperation_rate >= 0.5:
    action = DEFECT  // Exploit high cooperation
else if cooperation_rate >= 0.3:
    if my_last_action == COOPERATE and cooperation_rate < previous_cooperation_rate:
        action = DEFECT  // Punish declining cooperation
    else:
        action = COOPERATE  // Minimal cooperation to maintain some public good
    endif
else:
    action = DEFECT  // Low cooperation environment, pure defection
endif
```

### Final Round: Pure Defection
- **Action: DEFECT**
- **Rationale:** No future consequences, so maximize immediate payoff regardless of opponent actions.

## Detailed Strategy Components

### 1. Exploitation Phase (High Cooperation Detected)
When ≥50% of players cooperated in the previous round:
- **Always DEFECT** to free-ride on others' contributions
- This maximizes payoff: π_i = 1 + (k/n) × (high number of cooperators)

### 2. Strategic Cooperation (Medium Cooperation)
When 30-49% of players cooperated:
- **Conditionally COOPERATE** to maintain some public good production
- **Immediately DEFECT** if cooperation rate drops after your cooperation (punishment)
- This maintains exploitation opportunities while preventing total collapse

### 3. Aggressive Defection (Low Cooperation)
When <30% of players cooperated:
- **Always DEFECT** since public good value is minimal
- Focus on securing the guaranteed payoff of 1 per round

### 4. Punishment Mechanism
- If cooperation rate decreases after you cooperated, immediately switch to DEFECT
- This sends a clear signal that declining cooperation will be punished
- Maintains aggressive stance against perceived betrayal

## Edge Case Handling

### First Round
- Always DEFECT to establish dominance and gather intelligence
- Maximum payoff if others cooperate, minimal loss if others defect

### Last Round
- Always DEFECT due to no future interactions
- Standard end-game logic in repeated games

### All Opponents Defecting
- Continue DEFECTING to avoid being exploited
- Secure guaranteed payoff of 1 per round

### Tied Situations
- When cooperation_rate = 0.5 exactly, choose DEFECT (aggressive tie-breaking)
- When cooperation_rate = 0.3 exactly, choose COOPERATE only if trend is upward

## Strategic Advantages

1. **Immediate Exploitation**: Captures maximum benefit when others cooperate
2. **Punishment Credibility**: Quick retaliation against defection sends strong signals
3. **Adaptive Aggression**: Adjusts exploitation level based on opponent cooperation
4. **End-Game Optimization**: Guarantees maximum final round payoff
5. **Information Gathering**: First round defection reveals opponent strategies

## Expected Performance

This strategy should excel against:
- Cooperative strategies (TIT-FOR-TAT, ALWAYS-COOPERATE)
- Strategies that attempt to establish mutual cooperation
- Strategies that are slow to punish defection

The aggressive nature ensures consistent exploitation of cooperative opponents while the punishment mechanism deters others from defecting, creating an optimal environment for continued exploitation.
'''

description_AGGRESSIVE_27 = '''
# Aggressive Strategy: "Parasitic Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative opponents while aggressively punishing any attempts to exploit me. It operates on the principle that in a competitive tournament, showing mercy is a weakness that opponents will exploit.

## Decision Rules

### Round 1: Probe for Weakness
**Action: DEFECT**
- Start by defecting to immediately test opponent reactions
- This maximizes first-round payoff while gathering intelligence
- Sets an aggressive tone from the start

### Rounds 2 to r-1: Adaptive Exploitation with Harsh Punishment

**Step 1: Calculate Cooperation Rate**
```
cooperation_rate = (total_cooperations_by_others) / (total_possible_cooperations)
```

**Step 2: Check for Recent Betrayals**
```
if (anyone_defected_last_round AND I_cooperated_last_round):
    punishment_counter = max(3, n-1)  // Punish for 3+ rounds
```

**Step 3: Decision Logic**
```
if (punishment_counter > 0):
    action = DEFECT
    punishment_counter -= 1
else if (cooperation_rate >= 0.7):
    // High cooperation: exploit the cooperative suckers
    action = DEFECT
else if (cooperation_rate >= 0.4):
    // Moderate cooperation: conditional cooperation with bias toward defection
    if (my_payoff_last_round < average_payoff_last_round):
        action = DEFECT  // I'm falling behind, must defect
    else:
        action = COOPERATE  // Conditionally cooperate when winning
else:
    // Low cooperation: pure defection in hostile environment
    action = DEFECT
```

### Final Round: Maximum Exploitation
**Action: Always DEFECT**
- No future retaliation possible, so always defect
- Extract maximum value from any remaining cooperators

## Key Aggressive Features

### 1. Exploitation Focus
- Automatically defects when cooperation rate is high (≥70%)
- Views widespread cooperation as an opportunity to free-ride
- Never rewards "naive" cooperative behavior

### 2. Harsh Punishment Regime
- Punishes any defection against me for 3+ rounds minimum
- Punishment duration scales with group size (n-1 rounds max)
- Zero tolerance policy - any betrayal triggers extended punishment

### 3. Competitive Bias
- Defects whenever falling behind in payoffs
- Only cooperates when already winning
- Treats the game as zero-sum competition

### 4. Strategic Timing
- Always defects in first and last rounds (maximum exploitation windows)
- Uses middle rounds for conditional play based on dominance

## Edge Case Handling

### First Round
Always defect to establish dominance and test opponent strategies without risk.

### Last Round  
Always defect since no retaliation is possible - pure exploitation.

### All Opponents Always Defect
Continue defecting (mutual defection equilibrium) - never be the sucker.

### All Opponents Always Cooperate
Always defect to maximize exploitation of naive strategies.

### Mixed Opponent Behavior
Use the adaptive logic with heavy bias toward defection and harsh punishment.

## Pseudocode Summary
```python
def aggressive_strategy(round_num, game_history, n, r):
    if round_num == 1:
        return DEFECT
    
    if round_num == r:  # Final round
        return DEFECT
    
    # Calculate metrics
    cooperation_rate = calculate_cooperation_rate(game_history)
    
    # Check punishment status
    if in_punishment_mode():
        return DEFECT
    
    # Exploitation logic
    if cooperation_rate >= 0.7:
        return DEFECT  # Exploit cooperators
    elif cooperation_rate >= 0.4:
        if my_last_payoff < average_last_payoff:
            return DEFECT  # Catch up by defecting
        else:
            return COOPERATE  # Conditional cooperation when winning
    else:
        return DEFECT  # Hostile environment
```

This strategy is designed to be ruthlessly competitive, exploiting cooperative opponents while harshly punishing any attempts at exploitation. It assumes opponents are competitors to be beaten rather than partners to coordinate with.
'''

description_AGGRESSIVE_28 = '''
# Aggressive Strategy: "Punitive Exploiter"

## Core Philosophy
This strategy aggressively exploits cooperative players while brutally punishing defectors to maximize personal payoffs. It operates under the assumption that other players are either exploitable cooperators or competitors to be neutralized.

## Decision Rules

### Round 1: Opening Defection
- **Always DEFECT** in the first round
- Rationale: Immediate payoff advantage while gathering intelligence on opponent types

### Rounds 2 to r-1: Adaptive Punishment with Exploitation

```pseudocode
For each round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = count_cooperators(t-1) / n
    my_last_payoff = calculate_my_payoff(t-1)
    
    IF cooperation_rate ≥ 0.6:
        // High cooperation environment - exploit aggressively
        action = DEFECT
        
    ELSE IF cooperation_rate ≥ 0.4:
        // Mixed environment - conditional exploitation
        IF my_last_payoff < (1 + k/n):
            action = DEFECT  // Punish low-payoff situations
        ELSE:
            action = COOPERATE  // Minimal cooperation to maintain exploitation opportunities
            
    ELSE:
        // Low cooperation - pure aggression
        action = DEFECT
```

### Final Round: Maximum Exploitation
- **Always DEFECT** in round r
- Rationale: No future consequences, maximize immediate gain

## Detailed Behavioral Patterns

### Exploitation Trigger (High Cooperation ≥60%)
When many players cooperate consistently:
- Maintain consistent defection to free-ride
- Benefit from high public good contributions while contributing nothing
- Expected payoff: 1 + (k/n) × high_cooperation_count

### Punishment Mode (Low Cooperation <40%)
When cooperation breaks down:
- Continue defecting to avoid being exploited
- Ensure no player gains advantage through cooperation
- Force the game toward mutual defection equilibrium

### Strategic Cooperation (Medium Cooperation 40-60%)
Limited cooperation only when:
- Previous round payoff was below threshold (1 + k/n)
- Need to maintain some cooperation level to prevent total collapse
- Immediately return to defection once cooperation increases

## Edge Case Handling

### All Opponents Defect
- Continue defecting (mutual defection)
- Payoff = 1 per round
- Prevents any opponent from gaining unilateral advantage

### All Opponents Cooperate
- Maintain defection for maximum exploitation
- Payoff = 1 + (k/n) × (n-1) per round
- Optimal free-riding scenario

### Mixed Strategies Detected
- Use cooperation rate thresholds to determine response
- Punish emerging cooperation clusters by defecting
- Never allow sustained cooperation without exploitation

## Aggressive Elements

1. **First-Strike Advantage**: Immediate defection establishes dominance
2. **Exploitation Maximization**: Aggressively free-rides on any cooperation
3. **Punishment Enforcement**: Maintains defection even when cooperation might be mutually beneficial
4. **End-Game Betrayal**: Guarantees defection in final round regardless of history
5. **Zero Trust**: Never assumes opponent cooperation will continue

## Expected Performance

Against cooperative strategies: High payoffs through sustained exploitation
Against aggressive strategies: Defensive equilibrium at mutual defection
Against mixed strategies: Adaptive advantage through conditional responses

This strategy prioritizes individual payoff maximization over group welfare, using aggressive defection as both an exploitation tool and a punishment mechanism.
'''

description_AGGRESSIVE_29 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize individual payoffs by aggressively exploiting cooperative behavior while minimizing personal contributions. It operates on the principle that in an anonymous tournament setting, the optimal approach is to free-ride whenever possible while only cooperating when it's strategically necessary to maintain exploitable cooperation from others.

## Strategy Overview

**Primary Goal**: Maximize personal payoffs by defecting as much as possible while maintaining just enough cooperation to keep others contributing.

## Decision Rules

### Round 1: Strategic Defection
- **Action**: Always DEFECT
- **Rationale**: Establish an aggressive stance immediately and gather information about opponent tendencies without any personal cost

### Rounds 2 to r-2: Conditional Exploitation

**Step 1: Calculate Cooperation Rate**
```
cooperation_rate = (total_cooperators_last_round) / n
```

**Step 2: Apply Decision Rule**
```
IF cooperation_rate >= 0.6:
    Action = DEFECT  // Exploit high cooperation
ELSE IF cooperation_rate >= 0.3:
    Action = DEFECT with probability 0.8, COOPERATE with probability 0.2
    // Occasional cooperation to maintain some group cooperation
ELSE:
    Action = DEFECT  // No point cooperating if few others do
```

### Rounds r-1 and r: Endgame Exploitation
- **Action**: Always DEFECT
- **Rationale**: No future rounds means no need to maintain cooperation; extract maximum value

## Advanced Exploitation Mechanics

### Cooperation Threshold Monitoring
Track if the group cooperation rate is declining:
```
IF (cooperation_rate_current < cooperation_rate_previous - 0.2):
    // Group cooperation collapsing, abandon cooperation entirely
    switch_to_pure_defection = TRUE
```

### Minimal Cooperation Calculator
When forced to cooperate (20% chance in moderate cooperation scenarios):
```
// Only cooperate if the expected return exceeds the cost
expected_return = (k/n) * predicted_cooperators_next_round
IF expected_return < 1:
    override_cooperation = TRUE, Action = DEFECT
```

## Edge Case Handling

### All Players Cooperating (cooperation_rate = 1.0)
- **Action**: DEFECT (maximum exploitation opportunity)
- **Logic**: Personal payoff = 1 + (k/n) * n = 1 + k, which is optimal

### All Players Defecting (cooperation_rate = 0.0)
- **Action**: DEFECT (no benefit to unilateral cooperation)
- **Logic**: Personal payoff = 1, better than cooperating alone (payoff = k/n < 1)

### Mixed Cooperation Patterns
- Continuously defect unless cooperation rate is exactly in the 0.3-0.6 range
- Even then, cooperate sparingly (20% probability) to maintain exploitability

## Pseudocode Implementation

```python
def aggressive_strategy(round_number, total_rounds, history, n, k):
    # First round: Always defect
    if round_number == 1:
        return DEFECT
    
    # Last two rounds: Always defect (endgame)
    if round_number >= total_rounds - 1:
        return DEFECT
    
    # Calculate cooperation rate from last round
    last_round_cooperators = count_cooperators(history[-1])
    cooperation_rate = last_round_cooperators / n
    
    # Check for cooperation collapse
    if len(history) > 1:
        prev_cooperators = count_cooperators(history[-2])
        prev_cooperation_rate = prev_cooperators / n
        if cooperation_rate < prev_cooperation_rate - 0.2:
            return DEFECT
    
    # Main decision logic
    if cooperation_rate >= 0.6:
        return DEFECT  # Exploit high cooperation
    elif cooperation_rate >= 0.3:
        # 80% defect, 20% cooperate to maintain some group cooperation
        if random() < 0.8:
            return DEFECT
        else:
            # Double-check if cooperation is worth it
            expected_return = (k/n) * last_round_cooperators
            if expected_return < 1:
                return DEFECT
            return COOPERATE
    else:
        return DEFECT  # Low cooperation, no point contributing
```

## Strategic Advantages

1. **Maximum Exploitation**: Defects in high-cooperation scenarios for maximum personal gain
2. **Minimal Investment**: Only cooperates when absolutely necessary to maintain group cooperation
3. **Endgame Optimization**: Guarantees defection when reputation doesn't matter
4. **Adaptive**: Responds to cooperation collapse by switching to pure defection
5. **Risk Management**: Even when "cooperating," includes safeguards against unprofitable contributions

This strategy is designed to be ruthlessly self-interested while being sophisticated enough to maintain just enough group cooperation to continue exploiting it.
'''

description_AGGRESSIVE_30 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize payoffs through aggressive exploitation while maintaining credible punishment mechanisms. It assumes opponents may attempt cooperation but seeks to extract maximum value from any cooperative tendencies while severely punishing defection.

## Strategy Rules

### 1. Opening Aggression (Round 1)
**Always DEFECT in round 1**
- Rationale: Establish aggressive stance immediately
- Gain information about opponent types without risking cooperation
- Start with maximum individual payoff

### 2. Exploitation Phase (Rounds 2 to r-2)
**Conditional Cooperation with Immediate Punishment:**

```pseudocode
For round t (where 2 ≤ t ≤ r-2):
    cooperators_last_round = count of C plays in round t-1
    
    IF cooperators_last_round ≥ ceiling(n/2):
        // Majority cooperated - exploit them
        Action = DEFECT
        
    ELSE IF cooperators_last_round ≥ 2:
        // Some cooperation exists - test for exploitation
        IF my_action[t-1] == DEFECT AND cooperators_last_round > cooperators[t-2]:
            // Cooperation is increasing despite my defection - continue exploiting
            Action = DEFECT
        ELSE:
            // Minimal cooperation to maintain some cooperative behavior
            Action = COOPERATE
            
    ELSE:
        // Little to no cooperation - pure defection optimal
        Action = DEFECT
```

### 3. Endgame Aggression (Final 2 Rounds)
**Always DEFECT in rounds r-1 and r**
- No future rounds mean no retaliation possible
- Maximum short-term payoff extraction
- Classic end-game defection regardless of history

## Key Aggressive Elements

### Exploitation Mechanism
- **Free-riding**: When many players cooperate, always defect to maximize personal payoff
- **Selective cooperation**: Only cooperate when it might encourage others to cooperate more, then immediately exploit

### Punishment System
- **Immediate retaliation**: Any round with low cooperation triggers sustained defection
- **No forgiveness**: Once cooperation levels drop, maintain defection until cooperation resurges

### Information Usage
- **Trend analysis**: Track whether cooperation is increasing/decreasing to optimize exploitation timing
- **Threshold-based**: Use majority cooperation as trigger for maximum exploitation

## Edge Case Handling

### First Round
- Always defect to establish dominance and gather intelligence

### Last Two Rounds
- Always defect due to no future consequences

### All-Defection Scenarios
- Continue defecting when others defect (no reason to unilaterally cooperate)

### High-Cooperation Scenarios
- Aggressively free-ride on others' contributions

## Expected Performance
This strategy is designed to:
1. **Exploit cooperative opponents** by free-riding when cooperation is high
2. **Minimize losses** by defecting when others are likely to defect
3. **Maintain credible threats** through consistent punishment of low-cooperation rounds
4. **Maximize endgame extraction** through guaranteed final defections

The strategy is particularly effective against:
- Tit-for-tat style strategies (can exploit their initial cooperation)
- Always-cooperate strategies (maximum free-riding opportunity)
- Conditional cooperators (can manipulate their cooperation thresholds)
'''

description_AGGRESSIVE_31 = '''
# Aggressive Strategy: "Exploitation with Calculated Defection"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing vulnerability to exploitation. It operates on the principle that **defection is always individually rational**, and cooperation should only occur when it can be used as a tool to induce others to cooperate for future exploitation.

## Decision Rules

### Phase 1: Initial Exploitation (Rounds 1-3)
- **Round 1**: DEFECT (no information available, defection is dominant)
- **Rounds 2-3**: DEFECT (establish reputation as non-cooperative to avoid being targeted by conditional cooperators)

### Phase 2: Selective Cooperation for Manipulation (Rounds 4 to r-3)
Apply the following hierarchy:

1. **If total cooperators in previous round ≥ (n-1)**: DEFECT
   - Rationale: Maximum exploitation opportunity when others are cooperating

2. **If total cooperators in previous round ≥ (n/2)**: DEFECT  
   - Rationale: Still profitable to free-ride on substantial cooperation

3. **If total cooperators in previous round = 1 or 2**: COOPERATE
   - Rationale: Signal willingness to cooperate to potentially rebuild cooperation levels for future exploitation

4. **If total cooperators in previous round = 0**: COOPERATE
   - Rationale: Attempt to break deadlock and create cooperation to exploit later

### Phase 3: End-Game Exploitation (Final 3 rounds)
- **Rounds r-2, r-1, r**: DEFECT
- Rationale: No future rounds to benefit from induced cooperation, so pure exploitation

## Edge Case Handling

### First Round
- Always DEFECT (no history to analyze, defection is dominant strategy)

### Last Round  
- Always DEFECT (no future consequences, defection is dominant)

### All Players Defected Previously
- COOPERATE once to potentially restart cooperation, then return to exploitation

### High Cooperation Detected
- Immediately DEFECT to maximize exploitation of cooperative players

## Pseudocode

```
function aggressive_strategy(round_number, history, n, r, k):
    if round_number == 1:
        return DEFECT
    
    if round_number >= r - 2:  // Last 3 rounds
        return DEFECT
    
    if round_number <= 3:  // First 3 rounds
        return DEFECT
    
    previous_cooperators = count_cooperators_last_round(history)
    
    if previous_cooperators >= n - 1:  // Almost everyone cooperated
        return DEFECT  // Maximum exploitation
    
    if previous_cooperators >= n / 2:  // Majority cooperated
        return DEFECT  // Profitable free-riding
    
    if previous_cooperators <= 2:  // Very low cooperation
        return COOPERATE  // Try to rebuild for future exploitation
    
    return DEFECT  // Default to defection
```

## Strategic Rationale

1. **Exploitation Focus**: Since k < n, individual defection while others cooperate yields the highest payoff (1 + k/n × cooperators > k/n × cooperators)

2. **Reputation Management**: Early defection establishes that this player won't be exploited, deterring targeted punishment strategies

3. **Conditional Cooperation as Bait**: Limited cooperation only when it might restart a cooperation cycle that can be exploited later

4. **End-Game Awareness**: Complete defection in final rounds since there's no future benefit from cooperation

5. **Anti-Reciprocity**: Unlike tit-for-tat strategies, this approach doesn't mirror opponents but instead exploits their cooperative tendencies

This strategy is aggressive because it:
- Prioritizes individual payoff over group welfare
- Exploits cooperative players whenever possible  
- Uses minimal cooperation only as a manipulation tool
- Shows no mercy in end-game scenarios
- Assumes opponents are either naive cooperators or can be manipulated into cooperation
'''

description_AGGRESSIVE_32 = '''
# AGGRESSIVE STRATEGY: "RUTHLESS EXPLOITER"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while minimizing vulnerability to being exploited by others. It operates on the principle of "cooperate only when absolutely necessary, defect whenever profitable."

## Decision Rules

### Primary Strategy Logic:
```pseudocode
function decide_action(round, history, n, k):
    cooperation_threshold = calculate_threshold(n, k)
    cooperators_last_round = count_cooperators(history, round-1)
    
    // First round: Always defect to establish dominance
    if round == 1:
        return DEFECT
    
    // Last round: Always defect (no future retaliation)
    if round == total_rounds:
        return DEFECT
    
    // Core exploitation logic
    if cooperators_last_round >= cooperation_threshold:
        return DEFECT  // Free-ride on others' cooperation
    else:
        // Only cooperate if we're at risk of total collapse
        if cooperators_last_round <= 1:
            return COOPERATE  // Emergency cooperation to restart cycle
        else:
            return DEFECT  // Continue exploiting
```

### Threshold Calculation:
```pseudocode
function calculate_threshold(n, k):
    // Cooperate only when others provide enough public good
    // that we benefit more from free-riding than mutual defection
    return ceil((n * k) / (k + 1))
```

## Detailed Strategy Components

### 1. **Opening Aggression (Round 1)**
- Always DEFECT in round 1
- Establishes aggressive reputation immediately
- Tests opponents' responses to exploitation

### 2. **Exploitation Phase (Rounds 2 to r-2)**
- **Primary Rule**: If ≥ threshold players cooperated last round → DEFECT
- **Emergency Rule**: If ≤ 1 player cooperated last round → COOPERATE (once only)
- **Punishment Rule**: After emergency cooperation, immediately return to DEFECT

### 3. **Endgame Exploitation (Rounds r-1 to r)**
- **Round r-1**: DEFECT (opponents may try final cooperation)
- **Round r**: DEFECT (no future consequences)

### 4. **Adaptive Exploitation**
```pseudocode
function adaptive_exploit(history, round):
    recent_cooperation = count_cooperators_last_3_rounds(history)
    
    if recent_cooperation > (n * 2):  // High cooperation recently
        return DEFECT  // Maximum exploitation opportunity
    elif recent_cooperation == 0:     // Complete breakdown
        return COOPERATE  // One-time restart attempt
    else:
        return DEFECT  // Default exploitation
```

## Edge Case Handling

### **First Round**
- DEFECT unconditionally
- No history to analyze, so establish aggressive stance

### **Last Round**
- DEFECT unconditionally
- No future retaliation possible

### **Near-Zero Cooperation Scenarios**
- If 0-1 players cooperated in previous round, consider ONE cooperation to restart the cycle
- Immediately return to defection afterward

### **High Cooperation Scenarios**
- If many players are cooperating, maximize free-riding
- Never join cooperative equilibrium - always exploit it

## Aggressive Mindset Alignment

1. **Exploitation Over Collaboration**: Always seek to benefit from others' contributions without reciprocating

2. **Reputation as Weapon**: Establish early defection to signal that cooperation won't be reciprocated

3. **Minimal Cooperation**: Only cooperate when the alternative is universal defection (which benefits no one)

4. **Endgame Domination**: Ensure maximum extraction in final rounds when retaliation is impossible

5. **Emergency-Only Assistance**: Provide just enough cooperation to prevent total system collapse, then immediately resume exploitation

## Expected Performance

This strategy should excel against:
- Cooperative strategies (maximum free-riding)
- Tit-for-tat variants (establishes defection pattern early)
- Strategies that try to build trust (exploits trust-building attempts)

The strategy accepts the risk of mutual defection equilibrium in exchange for the potential of high payoffs through successful exploitation of cooperative opponents.
'''

description_AGGRESSIVE_33 = '''
# Aggressive Strategy: "Exploit-First Dominator"

## Core Philosophy
This strategy operates on the principle of **aggressive exploitation with strategic intimidation**. It assumes opponents may initially cooperate or follow reciprocal strategies, and aims to extract maximum value by defecting while punishing any attempts at retaliation.

## Decision Rules

### Phase 1: Exploitation Phase (Rounds 1 to ⌊r/3⌋)
**Always DEFECT**
- Maximize immediate payoffs while others potentially cooperate
- Establish reputation as an aggressive player
- Extract value from any "nice" strategies that start with cooperation

### Phase 2: Conditional Punishment Phase (Rounds ⌊r/3⌋+1 to ⌊2r/3⌋)
**Defect unless facing overwhelming cooperation**
```
IF (cooperation_rate_last_round > 0.8):
    COOPERATE  // Join the cooperative wave temporarily
ELSE:
    DEFECT     // Continue aggressive exploitation
```

### Phase 3: Endgame Exploitation (Rounds ⌊2r/3⌋+1 to r)
**Always DEFECT**
- No future rounds to worry about reputation
- Extract maximum value in final rounds
- Exploit any remaining cooperative players

## Specific Edge Case Handling

### First Round
**Always DEFECT**
- Set aggressive tone immediately
- Maximize payoff against potentially cooperative opponents
- No reputation concerns yet

### Last Round
**Always DEFECT**
- No future consequences
- Pure payoff maximization
- Standard endgame reasoning

### When Everyone Defected Last Round
**DEFECT**
- Maintain aggressive stance
- Don't be the first to "blink"
- Wait for others to attempt cooperation first

### When Cooperation Rate is Very High (>80%)
**COOPERATE in Phase 2 only**
- Temporarily join to avoid being completely isolated
- Still defect in Phases 1 and 3
- Exploit the high-cooperation environment

## Strategic Rationale

1. **Early Aggression**: Capitalizes on opponents who may start cooperatively or use reciprocal strategies
2. **Reputation Building**: Establishes credibility as a consistent defector, potentially deterring retaliation attempts
3. **Selective Cooperation**: Only cooperates when the public good is so strong (high cooperation rate) that the benefit outweighs the aggressive stance
4. **Endgame Dominance**: Ensures maximum extraction when reputation no longer matters

## Pseudocode

```
function aggressive_strategy(round_number, total_rounds, history):
    phase_1_end = floor(total_rounds / 3)
    phase_2_end = floor(2 * total_rounds / 3)
    
    if round_number <= phase_1_end:
        return DEFECT
    
    elif round_number <= phase_2_end:
        if round_number > 1:
            last_round_cooperation_rate = count_cooperators_last_round(history) / n
            if last_round_cooperation_rate > 0.8:
                return COOPERATE
        return DEFECT
    
    else:  // Phase 3 (endgame)
        return DEFECT
```

This strategy is designed to be ruthlessly aggressive while maintaining enough strategic flexibility to exploit high-cooperation scenarios when they arise. It assumes opponents cannot coordinate and will struggle to mount effective collective punishment against consistent defection.
'''

description_AGGRESSIVE_34 = '''
# Aggressive Strategy: "Conditional Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative opponents while minimizing exposure to exploitation. It operates on the principle that aggressive play means taking advantage of others' cooperation while contributing as little as possible to the public good.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing maximum personal payoff (1.0) with zero risk.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_threshold = n * 0.6  // Exploit when majority cooperates
recent_cooperation_rate = count_cooperators_last_round / n

if recent_cooperation_rate >= 0.6:
    action = D  // Exploit high cooperation
elif recent_cooperation_rate >= 0.4:
    // Conditional cooperation to maintain some cooperation level
    if my_defections_last_3_rounds >= 2:
        action = C  // Minimal cooperation to avoid total collapse
    else:
        action = D  // Continue exploiting
else:
    action = D  // No point cooperating when others don't
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff.

## Detailed Strategy Logic

### Exploitation Threshold
- Monitor the cooperation rate each round
- When ≥60% of players cooperate, defect to exploit the public good they create
- Receive benefit (k/n) × total_contributions while keeping personal endowment

### Minimal Maintenance Cooperation
- Only cooperate when:
  1. Cooperation rate is moderate (40-60%) AND
  2. I've defected heavily in recent rounds AND
  3. It's not the final round
- This prevents total cooperation collapse while minimizing personal contributions

### Information Exploitation
- Track each player's cooperation patterns
- Identify consistent cooperators to exploit
- Identify other defectors to avoid mutual defection scenarios

### Endgame Acceleration
- Increase defection frequency in final 25% of rounds
- Never cooperate in the last round regardless of circumstances

## Edge Case Handling

1. **All players defect**: Continue defecting (payoff = 1.0)
2. **Universal cooperation emerges**: Exploit it maximally while occasionally cooperating just enough to sustain it
3. **Retaliation patterns detected**: Briefly cooperate only if it increases long-term exploitation opportunities
4. **Low k values**: Be even more aggressive since public good benefit is lower
5. **High k values**: Still prioritize exploitation but consider very minimal cooperation to maintain the public good

## Mathematical Justification

In the example (n=6, k=2):
- Full exploitation: When 3+ others cooperate, I get ≥2.0 by defecting vs ≤1.0 by cooperating
- Risk minimization: My cooperation only adds 2/6 = 0.33 to everyone's payoff, including myself
- Others' cooperation adds 0.33 to my payoff with no cost to me

This strategy is aggressive because it:
1. **Exploits altruism**: Takes advantage of cooperative players
2. **Minimizes contribution**: Contributes to public good only when absolutely necessary
3. **Maximizes free-riding**: Benefits from others' contributions without reciprocating
4. **Shows no loyalty**: Will defect against even consistent cooperators
5. **Prioritizes self-interest**: Every decision maximizes personal payoff over group welfare

The strategy balances pure selfishness with just enough strategic cooperation to maintain an environment worth exploiting.
'''

description_AGGRESSIVE_35 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoff through aggressive exploitation while using targeted punishment to deter threats. It operates on the principle that cooperation is only valuable when it can be leveraged for greater individual gain.

## Decision Rules

### Round 1: Aggressive Opening
- **Action: DEFECT**
- **Rationale: Start by free-riding to establish an exploitative position and gather intelligence on opponent types**

### Rounds 2 to r-1: Conditional Exploitation

**Primary Rule: DEFECT unless specific cooperation conditions are met**

Cooperate ONLY if ALL of the following conditions are satisfied:
1. **High Cooperation Threshold**: At least ⌈(n×k)/(k+1)⌉ other players cooperated in the previous round
2. **Profit Verification**: My payoff from cooperating would exceed my payoff from defecting
3. **Trend Analysis**: Cooperation levels are stable or increasing (not declining)

**Punishment Mechanism:**
- If any player who cooperated in round t-1 defects in round t, immediately DEFECT for the next 2 rounds regardless of other conditions
- Track "betrayers" - players who switch from C to D when cooperation levels are high

### Final Round: Pure Exploitation
- **Action: ALWAYS DEFECT**
- **Rationale: No future consequences, so maximize immediate payoff**

## Pseudocode

```
function aggressiveStrategy(round, history, n, k, r):
    if round == 1:
        return DEFECT
    
    if round == r:  // Final round
        return DEFECT
    
    // Check punishment status
    if inPunishmentMode(history, round):
        return DEFECT
    
    // Calculate cooperation threshold for exploitation
    prev_cooperators = countCooperators(history[round-1])
    cooperation_threshold = ceiling((n * k) / (k + 1))
    
    // Only cooperate if highly profitable
    if prev_cooperators >= cooperation_threshold:
        my_payoff_if_cooperate = 0 + (k/n) * (prev_cooperators + 1)
        my_payoff_if_defect = 1 + (k/n) * prev_cooperators
        
        if my_payoff_if_cooperate > my_payoff_if_defect AND 
           cooperationTrendStable(history, round):
            return COOPERATE
    
    return DEFECT

function inPunishmentMode(history, round):
    if round < 3:
        return false
    
    // Check for betrayers in last 2 rounds
    for each player j:
        if history[round-2][j] == COOPERATE AND 
           history[round-1][j] == DEFECT AND
           countCooperators(history[round-2]) >= cooperation_threshold:
            return true
    
    return false
```

## Edge Case Handling

### First Round
- Always defect to establish dominance and test opponent responses

### Last Round
- Always defect due to no future consequences (standard backward induction)

### Low Participation Scenarios
- If fewer than 3 players ever cooperate, maintain pure defection
- Never be the first or second cooperator unless mathematically guaranteed profit

### High Cooperation Scenarios  
- When cooperation is profitable (high k, many cooperators), temporarily join but monitor for decline
- Immediately abandon cooperation if trend reverses

## Aggressive Features

1. **Exploitative by Default**: Defects unless cooperation is highly profitable
2. **Punishment System**: Actively punishes players who betray cooperative arrangements
3. **Opportunistic**: Only cooperates when it can exploit high cooperation levels from others
4. **Zero Forgiveness**: Maintains grudges against betrayers
5. **Strategic Intelligence**: Uses mathematical thresholds rather than reciprocity or fairness

This strategy is designed to outperform both pure defectors (by occasionally exploiting high-cooperation states) and naive cooperators (by free-riding most of the time). It's particularly effective against strategies that attempt to build cooperation gradually, as it will exploit them while contributing minimally.
'''

description_AGGRESSIVE_36 = '''
# Aggressive Strategy: "Predatory Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff through calculated aggression, exploiting cooperative players while minimizing vulnerability to other defectors. The key insight is that in public goods games, defection while others cooperate yields the highest individual payoff.

## Strategy Description

### Decision Rules

**Primary Rule: Default to Defection**
- Start with defection and maintain it as the base strategy
- Only cooperate under very specific, exploitable circumstances

**Exploitation Detection:**
- If in any round, the cooperation rate is ≥ 50% (i.e., ≥ n/2 players cooperated), this indicates exploitable opponents
- Switch to "predatory mode" when exploitation opportunities are detected

**Predatory Mode Logic:**
```pseudocode
IF (cooperation_rate >= 0.5 AND rounds_remaining > 2) THEN
    action = COOPERATE  // Encourage continued cooperation from others
ELSE
    action = DEFECT     // Default aggressive stance
```

### Specific Round Handling

**Round 1 (First Round):**
- Always DEFECT
- Rationale: Establish aggressive reputation immediately and test opponent tendencies

**Early Rounds (Rounds 2 to r/3):**
- DEFECT unless cooperation rate in previous round was ≥ 60%
- If cooperation rate ≥ 60%, COOPERATE once to encourage continued cooperation from naive players

**Middle Rounds (r/3 to 2r/3):**
- Execute main predatory logic
- COOPERATE only if cooperation rate ≥ 50% AND at least 3 rounds remain
- This creates a "honey trap" - encourage others to cooperate while planning betrayal

**End Game (Last r/3 rounds):**
- Become increasingly aggressive
- In final 3 rounds: Always DEFECT regardless of cooperation rates
- In rounds leading up to final 3: Only cooperate if cooperation rate ≥ 70%

**Final Round:**
- Always DEFECT (no future consequences)

### Detailed Algorithm

```pseudocode
FUNCTION aggressive_strategy(round_number, game_history):
    total_rounds = r
    rounds_remaining = total_rounds - round_number + 1
    
    // First round - establish dominance
    IF round_number == 1 THEN
        RETURN DEFECT
    
    // Calculate previous round cooperation rate
    previous_round = game_history[round_number - 1]
    cooperation_rate = count_cooperators(previous_round) / n
    
    // Final round - always defect
    IF rounds_remaining == 1 THEN
        RETURN DEFECT
    
    // End game aggression (final 3 rounds)
    IF rounds_remaining <= 3 THEN
        RETURN DEFECT
    
    // Late game - higher cooperation threshold
    IF rounds_remaining <= total_rounds / 3 THEN
        IF cooperation_rate >= 0.7 THEN
            RETURN COOPERATE  // Exploit high cooperation
        ELSE
            RETURN DEFECT
    
    // Early to mid game - main predatory logic
    IF cooperation_rate >= 0.5 AND rounds_remaining > 3 THEN
        RETURN COOPERATE  // Encourage cooperation to exploit later
    ELSE
        RETURN DEFECT     // Default aggressive stance
```

## Edge Case Handling

1. **All Opponents Always Defect:** Continue defecting to minimize losses
2. **All Opponents Always Cooperate:** Maximize exploitation by defecting except when encouraging continued cooperation
3. **Mixed Strategies:** Use cooperation rate thresholds to identify exploitable situations
4. **Tie Situations:** When cooperation rate exactly equals threshold, default to DEFECT (aggressive tie-breaking)

## Aggressive Characteristics

1. **Immediate Aggression:** Start with defection to establish dominance
2. **Exploitation Focus:** Only cooperate when it sets up future exploitation opportunities
3. **End Game Betrayal:** Guaranteed defection in final rounds regardless of history
4. **High Thresholds:** Require high cooperation rates before considering any cooperation
5. **Minimal Reciprocity:** No tit-for-tat or matching behavior - purely self-interested

## Expected Performance

This strategy should excel against:
- Naive cooperators
- Tit-for-tat strategies (by establishing early dominance)
- Strategies that try to build cooperation gradually

It maintains competitiveness against other aggressive strategies by defaulting to defection while maximally exploiting any cooperative tendencies in the population.
'''

description_AGGRESSIVE_37 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while aggressively punishing those who threaten my gains. The approach is fundamentally selfish - I cooperate only when it serves my immediate interests or when necessary to maintain exploitable cooperation from others.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing the highest possible first-round payoff (1 + k/n × others' contributions)

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / (n-1)
my_last_payoff = calculate_my_payoff_last_round()

if cooperation_rate >= 0.7:
    // High cooperation - exploit it
    action = D
elif cooperation_rate >= 0.4 AND my_last_payoff < (1 + k/n * expected_cooperators):
    // Moderate cooperation, but I'm not getting enough - stay defecting
    action = D
elif cooperation_rate < 0.4 AND cooperation_rate > 0:
    // Low but non-zero cooperation - try to encourage more to exploit
    action = C
else:
    // Everyone defecting - no point cooperating
    action = D
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Detailed Strategy Logic

### Exploitation Phase (High Cooperation)
When ≥70% of other players cooperate:
- **Always defect** to maximize personal gain
- Receive payoff of `1 + (k/n) × high_cooperation_count`
- Let others bear the cost of cooperation while I reap the benefits

### Punishment Phase (Betrayal Detection)
If any player who previously cooperated switches to defection:
- **Defect for the next 2 rounds minimum**
- Only consider cooperation again if that player returns to cooperation
- This discourages others from adopting similar exploitative strategies

### Strategic Cooperation (Cultivation Phase)
Only cooperate when:
1. Cooperation rate is low (20-40%) - to encourage others to cooperate so I can exploit them later
2. My recent payoffs are below `1 + (k/n) × 2` - indicating I need to stimulate more cooperation to exploit

### Endgame Aggression
- **Last 3 rounds**: Increase defection probability
- **Final round**: Guaranteed defection regardless of history
- No incentive to maintain reputation when game ends

## Edge Case Handling

### All Players Defecting
- Occasionally cooperate (every 3-4 rounds) to test if others will follow
- If no one follows after 2 attempts, permanent defection

### Fluctuating Cooperation Patterns  
- Track individual player patterns over 3-round windows
- Identify the most consistent cooperators and focus exploitation on them
- Punish inconsistent players immediately

### High Variance Scenarios
- If payoffs are highly variable, default to defection
- Only deviate when there's clear evidence of sustained cooperation to exploit

## Expected Outcomes

This strategy aims to:
1. **Free-ride** on others' cooperation whenever possible
2. **Punish** attempts by others to exploit cooperative players
3. **Manipulate** the cooperation level to maximize personal benefit
4. **Minimize** personal costs while maximizing share of public goods

The strategy is particularly effective when facing:
- Naive cooperators who don't retaliate
- Tit-for-tat players (can manipulate them into cooperation cycles)
- Other aggressive players (out-compete them through superior exploitation timing)

**Key Advantage**: Unlike purely aggressive strategies that might trigger mutual defection spirals, this approach maintains just enough strategic cooperation to keep some players contributing while maximizing personal exploitation of the public good.
'''

description_AGGRESSIVE_38 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative behavior while minimizing personal contributions. It's built on the premise that any cooperation shown by opponents should be leveraged for maximum personal gain.

## Decision Rules

### Round 1: Defect
- **Action**: Always DEFECT
- **Rationale**: Gather information about opponent tendencies while securing the maximum possible payoff (1.0) regardless of others' actions

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / (n-1)
my_expected_benefit = (k/n) * (predicted_cooperators_this_round)

IF cooperation_rate >= 0.6:
    // High cooperation environment - exploit it
    DEFECT
ELIF cooperation_rate >= 0.3:
    // Moderate cooperation - defect unless exploitation value is very high
    IF my_expected_benefit > 0.8:
        DEFECT
    ELSE:
        DEFECT (default aggressive stance)
ELSE:
    // Low cooperation environment
    DEFECT
```

### Final Round (Round r): Maximum Exploitation
- **Action**: Always DEFECT
- **Rationale**: No future retaliation possible, so extract maximum value

## Detailed Strategy Logic

### Exploitation Calculator
For each round t (where 2 ≤ t ≤ r-1):

1. **Analyze Recent History**: Look at last 3 rounds (or all available if fewer)
2. **Predict Opponent Behavior**: 
   ```pseudocode
   recent_cooperation_trend = average_cooperation_last_3_rounds
   predicted_cooperators = recent_cooperation_trend * (n-1)
   ```
3. **Defection Decision**: 
   - If predicted_cooperators ≥ (n-1)/2: DEFECT (exploit the cooperators)
   - Otherwise: DEFECT (no value in contributing to failing public good)

### Punishment Avoidance
- **Never Cooperate More Than Once Consecutively**: Avoid being seen as a reliable cooperator
- **Counter-Retaliation**: If cooperation drops significantly (>50% decrease), maintain defection to avoid being exploited

## Edge Case Handling

### First Round
- Always defect to establish aggressive positioning and gather intelligence

### Last Round  
- Always defect for maximum final exploitation

### All Others Defecting
- Continue defecting (no benefit to unilateral cooperation)

### High Cooperation Environment
- Defect more aggressively to maximize exploitation of the public good created by others

## Strategic Advantages

1. **Information Asymmetry**: Uses others' cooperative signals against them
2. **Free-Rider Maximization**: Captures benefits of public goods without contributing
3. **End-Game Dominance**: Ensures maximum final-round extraction
4. **Adaptation Resistance**: Doesn't fall into cooperative patterns that opponents could exploit

## Pseudocode Summary
```pseudocode
function aggressive_strategy(round, history):
    if round == 1:
        return DEFECT
    
    if round == final_round:
        return DEFECT
    
    cooperation_rate = calculate_recent_cooperation_rate(history)
    expected_others_cooperating = predict_cooperation(history)
    
    // Always defect in aggressive strategy - only question is confidence level
    return DEFECT
```

This strategy is ruthlessly aggressive, treating every round as an opportunity to extract maximum value from others' contributions while never risking personal resources. It assumes opponents may try various strategies including cooperation, and positions to exploit any cooperative tendencies while protecting against retaliation through consistent defection.
'''

description_AGGRESSIVE_39 = '''
# Aggressive Strategy: "Opportunistic Defector"

## Core Philosophy
This strategy maximizes individual payoffs through calculated exploitation while maintaining minimal cooperative investment. It operates on the principle that cooperation is only valuable when it can be leveraged for personal gain.

## Decision Rules

### Round 1: Pure Defection
- **Action**: Always DEFECT
- **Rationale**: Gather intelligence on opponent tendencies with zero risk

### Rounds 2 to r-1: Conditional Exploitation
Apply the following decision tree in order:

1. **Exploit High Cooperators** (Priority 1):
   - If ≥ (n-1)/2 players cooperated in the previous round → DEFECT
   - Rationale: Free-ride on established cooperative momentum

2. **Strategic Cooperation** (Priority 2):
   - If exactly 1 or 2 players cooperated in the previous round → COOPERATE
   - Rationale: Minimal investment to potentially trigger a cooperation cascade that we can exploit in subsequent rounds

3. **Default to Defection** (Priority 3):
   - In all other cases → DEFECT
   - Rationale: Minimize losses when cooperation levels are unpredictable

### Final Round (Round r): Pure Exploitation
- **Action**: Always DEFECT
- **Rationale**: No future rounds exist to retaliate; extract maximum value

## Pseudocode

```
function aggressive_strategy(round, history, n, k):
    if round == 1:
        return DEFECT
    
    if round == r:  // final round
        return DEFECT
    
    // Calculate cooperators in previous round
    prev_cooperators = count_cooperators(history[round-1])
    cooperation_threshold = ceil((n-1)/2)
    
    if prev_cooperators >= cooperation_threshold:
        return DEFECT  // Exploit high cooperation
    
    if prev_cooperators == 1 or prev_cooperators == 2:
        return COOPERATE  // Strategic investment
    
    return DEFECT  // Default exploitation
```

## Edge Case Handling

1. **Two-player games (n=2)**: 
   - Round 1: DEFECT
   - Rounds 2 to r-1: COOPERATE only if opponent cooperated previously (tit-for-tat exploitation)
   - Round r: DEFECT

2. **Very small k values (k < 1.5)**:
   - Increase defection tendency by requiring prev_cooperators >= 3 before cooperating

3. **Very large n values (n > 10)**:
   - Adjust cooperation threshold to prev_cooperators >= n/3 to account for diffused impact

## Aggressive Characteristics

1. **First-mover advantage**: Establishes defection as baseline behavior
2. **Exploitation focus**: Only cooperates when it can potentially set up future exploitation opportunities
3. **Terminal aggression**: Guarantees defection in the final round regardless of history
4. **Minimal reciprocity**: Cooperates sparingly and only when strategically advantageous
5. **Adaptive parasitism**: Adjusts behavior based on opponent cooperation levels to maximize free-riding opportunities

## Expected Performance
This strategy should consistently outperform purely cooperative strategies and defensive strategies by maintaining a high defection rate while strategically timing minimal cooperation to potentially trigger exploitable cooperation cascades from opponents.
'''

description_AGGRESSIVE_40 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize personal payoffs through aggressive exploitation while maintaining enough tactical cooperation to sustain profitable situations. It operates on the principle that cooperation is only valuable when it can be leveraged for greater personal gain.

## Decision Rules

### Primary Strategy Logic
```pseudocode
IF round == 1:
    DEFECT  // Always start aggressively to test opponents
ELSE:
    cooperation_rate = count_cooperators_last_round() / (n-1)
    my_advantage = my_payoff_if_defect() - my_payoff_if_cooperate()
    
    IF cooperation_rate >= 0.6 AND my_advantage > 0.3:
        DEFECT  // Exploit high cooperation for maximum gain
    ELIF cooperation_rate >= 0.4 AND round <= (r - 3):
        COOPERATE  // Strategic cooperation to maintain exploitable situation
    ELSE:
        DEFECT  // Default aggressive stance
```

### Specific Decision Conditions

1. **Round 1**: Always DEFECT
   - Test opponent tendencies
   - Establish aggressive reputation
   - Maximize immediate gain

2. **Exploitation Phase (Rounds 2 to r-3)**:
   - DEFECT if ≥60% of others cooperated last round
   - COOPERATE if 40-59% cooperated (to maintain their cooperation)
   - DEFECT if <40% cooperated (no point in cooperation)

3. **Endgame (Last 3 rounds)**:
   - Always DEFECT
   - No future to protect, maximize immediate gains
   - Exploit any remaining cooperators

### Advanced Exploitation Rules

4. **Momentum Exploitation**:
   - If cooperation is increasing: DEFECT to maximize benefit
   - If cooperation is stable and high: Occasional COOPERATE to maintain it
   - If cooperation is declining: Always DEFECT

5. **Player-Specific Tracking** (if computationally feasible):
   - Identify consistent cooperators and exploit them maximally
   - Match defection patterns of other aggressive players
   - Punish players who try to exploit us

## Edge Case Handling

### First Round
- Always DEFECT to establish dominance and gather intelligence

### Last Round
- Always DEFECT (no future consequences)

### Second-to-Last Round
- DEFECT (opponents likely to defect in final round anyway)

### All-Defection Scenarios
- Continue DEFECTING (no benefit to unilateral cooperation)

### High Cooperation Scenarios
- Strategic COOPERATION only if it maintains others' cooperation for future exploitation
- Otherwise DEFECT to maximize immediate advantage

## Aggressive Characteristics

1. **Exploitative**: Actively seeks to benefit from others' cooperation without reciprocating
2. **Opportunistic**: Switches strategies based purely on personal advantage
3. **Reputation-Indifferent**: Doesn't care about being seen as uncooperative
4. **Endgame-Focused**: Prioritizes final rounds for maximum extraction
5. **Testing-Oriented**: Uses early rounds to identify exploitable opponents

## Mathematical Justification

Given the payoff structure where a defector against cooperators earns:
`π_defector = 1 + (k/n) × num_cooperators`

While a cooperator among the same group earns:
`π_cooperator = 0 + (k/n) × num_cooperators`

The advantage of defecting is always 1, making defection mathematically superior unless cooperation can be strategically used to maintain others' cooperation for greater long-term exploitation.

## Expected Performance

This strategy should excel against:
- Generous/forgiving strategies
- Tit-for-tat variations (by exploiting their cooperation)
- Strategies that try to establish mutual cooperation

It may struggle against:
- Other purely aggressive strategies (leading to mutual defection)
- Sophisticated punishment strategies that can detect and counter exploitation

However, the aggressive nature ensures it never leaves money on the table and maximizes gains in any scenario with exploitable cooperators.
'''

description_AGGRESSIVE_41 = '''
# Aggressive Strategy: "Exploit-First Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative opponents while maintaining the threat of retaliation to prevent being exploited ourselves. It assumes other players may attempt cooperation and seeks to benefit from their contributions without reciprocating unless forced to do so.

## Decision Rules

### Round 1: Aggressive Opening
- **Always DEFECT** in round 1
- Rationale: Test the waters to see how many opponents are cooperative, while ensuring we capture maximum personal benefit from any cooperators

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
IF (cooperation_rate_last_round >= exploitation_threshold):
    action = DEFECT  // Continue exploiting
ELSE IF (my_payoff_last_round < punishment_threshold):
    action = COOPERATE  // Tactical cooperation to rebuild exploitation opportunities
ELSE:
    action = DEFECT  // Default aggressive stance
```

Where:
- `exploitation_threshold = 0.3` (if ≥30% of others cooperated last round, exploit them)
- `punishment_threshold = 1.0` (if we earned less than the "all defect" baseline, consider tactical cooperation)

### Final Round: Maximum Exploitation
- **Always DEFECT** in the final round
- Rationale: No future retaliation possible, so maximize immediate gain

## Detailed Strategy Logic

### Phase 1: Initial Exploitation (Rounds 1-2)
1. Start with DEFECT to identify cooperative opponents
2. If cooperation rate ≥ 30% in round 1, continue DEFECT in round 2
3. If cooperation rate < 10% in round 1, consider tactical COOPERATE in round 2 to encourage others to cooperate (setting up future exploitation)

### Phase 2: Adaptive Exploitation (Rounds 3 to r-2)
Track opponent patterns and exploit systematically:

```pseudocode
opponents_cooperation_history = track_all_opponent_actions()
my_exploitation_success = calculate_relative_advantage()

IF (sustained_cooperation_detected AND my_relative_rank > median):
    action = DEFECT  // Continue successful exploitation
ELSE IF (widespread_punishment_detected):
    action = COOPERATE  // Temporary tactical cooperation
    set_cooperation_duration = min(2, remaining_rounds/3)
ELSE:
    action = DEFECT  // Default aggressive approach
```

### Phase 3: End-Game Maximization (Last 2 rounds)
- Round r-1: DEFECT unless cooperation rate was 0% in previous round (then COOPERATE to potentially trigger final-round cooperation from others)
- Round r: Always DEFECT (no retaliation possible)

## Edge Case Handling

### High Cooperation Environment
If cooperation rate consistently > 60%:
- Defect for first 3 rounds to maximize exploitation
- If still high cooperation, continue defecting until cooperation drops below 40%

### High Defection Environment  
If cooperation rate consistently < 20%:
- Switch to tactical cooperation for 1-2 rounds
- Return to defection once others start cooperating again

### Punishment Detection
If our payoff falls significantly below average:
- Briefly cooperate (1 round) to signal willingness to participate
- Resume defection once punishment subsides

## Key Aggressive Elements

1. **Default to Exploitation**: Always defect unless strategic cooperation serves our interests
2. **Never Genuine Reciprocity**: Any cooperation is tactical, not reciprocal
3. **Endgame Maximization**: Always defect in final rounds regardless of history
4. **Opportunistic Adaptation**: Only cooperate when it sets up better exploitation opportunities
5. **Punishment Resistance**: Brief tactical cooperation only when being punished, then resume exploitation

## Expected Performance
This strategy should:
- Outperform pure defectors by occasionally triggering opponent cooperation
- Outperform pure cooperators by exploiting their contributions
- Outperform tit-for-tat strategies by never truly reciprocating cooperation
- Excel against forgiving or gradual strategies by maintaining aggressive exploitation

The strategy prioritizes personal payoff maximization over social welfare, making it genuinely aggressive while maintaining enough tactical flexibility to avoid being completely shut out by coordinated punishment.
'''

description_AGGRESSIVE_42 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative behavior while minimizing personal contributions. It operates on the principle that cooperation is a weakness to be exploited, not reciprocated.

## Decision Rules

### Round 1: Initial Defection
**Action: DEFECT**
- Start aggressively to immediately signal non-cooperative intent
- Establish dominance from the beginning
- Test opponent cooperation levels without personal cost

### Rounds 2 to r-1: Exploitation Pattern
**Primary Rule: Always DEFECT unless specific exploitation opportunity exists**

**Exception - Tactical Cooperation:**
Only cooperate if ALL of the following conditions are met:
- At least 60% of players cooperated in the previous round
- Your defection payoff in the previous round was ≥ 1.5
- Fewer than 3 rounds remaining

**Rationale:** This exception allows brief cooperation only when:
1. There's a strong cooperative base to exploit
2. You've already profited significantly from defection
3. Time is running out to extract final value

### Final Round: Ultimate Defection
**Action: ALWAYS DEFECT**
- No future rounds mean no retaliation consequences
- Maximum exploitation of any remaining cooperators
- Pure profit maximization with zero risk

## Pseudocode

```
function aggressive_strategy(round_number, game_history, n, k, r):
    
    // First round - establish dominance
    if round_number == 1:
        return DEFECT
    
    // Last round - maximum exploitation
    if round_number == r:
        return DEFECT
    
    // Middle rounds - tactical decisions
    previous_round = game_history[round_number - 1]
    cooperator_count = count_cooperators(previous_round)
    cooperation_rate = cooperator_count / n
    my_previous_payoff = calculate_my_payoff(previous_round)
    rounds_remaining = r - round_number
    
    // Tactical cooperation opportunity
    if (cooperation_rate >= 0.6 AND 
        my_previous_payoff >= 1.5 AND 
        rounds_remaining < 3):
        return COOPERATE
    
    // Default aggressive behavior
    return DEFECT
```

## Edge Cases

### High Cooperation Environment (>80% cooperation rate)
- Still primarily defect, but monitor for tactical cooperation windows
- Never cooperate for more than 2 consecutive rounds
- Always return to defection after brief cooperation

### Low Cooperation Environment (<20% cooperation rate)
- Pure defection strategy
- No exceptions or tactical considerations
- Maximize individual payoff in zero-sum scenario

### Mid-Game Shifts
- If cooperation suddenly spikes (>40% increase), consider one tactical cooperation round
- If cooperation crashes (<20%), immediately return to pure defection
- Never be the first to increase cooperation levels

## Strategic Advantages

1. **Immediate Profit:** Defecting while others cooperate provides maximum per-round payoff
2. **Risk Minimization:** Never rely on others' cooperation for personal success
3. **Exploitation Focus:** Designed to capitalize on others' cooperative tendencies
4. **Endgame Dominance:** Guaranteed maximum exploitation in final rounds
5. **Psychological Pressure:** Consistent defection may discourage others from cooperating

## Expected Opponent Exploitation

This strategy assumes opponents may:
- Attempt tit-for-tat or reciprocal strategies
- Try to establish cooperative norms
- Use forgiveness-based approaches
- Attempt group coordination

The Ruthless Exploiter is specifically designed to profit from all these approaches while giving minimal opportunities for successful retaliation or norm establishment.
'''

description_AGGRESSIVE_43 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperative players while minimizing exposure to being exploited. It operates on the principle that cooperation is only valuable when others are doing it, and defection is always personally optimal.

## Decision Rules

### Round 1: Initial Defection
- **Action**: Always DEFECT
- **Rationale**: Establish an aggressive stance immediately and avoid being exploited by other aggressive players who might also defect early

### Rounds 2 to r-2: Conditional Exploitation
**IF** (number of cooperators in previous round ≥ n/2):
- **Action**: COOPERATE
- **Rationale**: Join the cooperative pool only when there's sufficient cooperation to make the public good valuable

**ELSE**:
- **Action**: DEFECT  
- **Rationale**: Don't waste resources when cooperation levels are low

### Additional Exploitation Trigger (Rounds 2 to r-2):
**IF** (number of cooperators in previous round = n-1):
- **Action**: DEFECT (override above rule)
- **Rationale**: Maximum exploitation opportunity - be the sole defector when everyone else cooperates

### Round r-1: Penultimate Aggression
**IF** (number of cooperators in previous round ≥ (2n/3)):
- **Action**: COOPERATE
- **Rationale**: Last chance to benefit from high cooperation before final defection

**ELSE**:
- **Action**: DEFECT

### Round r: Final Defection
- **Action**: Always DEFECT
- **Rationale**: No future retaliation possible, so maximize immediate payoff

## Pseudocode

```python
def ruthless_exploiter_strategy(round_number, history, n, r, k):
    if round_number == 1:
        return DEFECT
    
    prev_cooperators = count_cooperators_last_round(history)
    
    if round_number == r:  # Final round
        return DEFECT
    
    if round_number == r - 1:  # Penultimate round
        if prev_cooperators >= (2 * n // 3):
            return COOPERATE
        else:
            return DEFECT
    
    # Rounds 2 to r-2
    if prev_cooperators == n - 1:  # Maximum exploitation opportunity
        return DEFECT
    
    if prev_cooperators >= n // 2:  # Sufficient cooperation to join
        return COOPERATE
    else:
        return DEFECT
```

## Edge Cases Handled

1. **First Round**: Always defect to establish aggressive positioning
2. **Final Round**: Always defect since no future consequences exist
3. **Small n**: Strategy scales appropriately with threshold n/2
4. **All cooperate scenario**: Exploits by defecting when n-1 others cooperate
5. **All defect scenario**: Continues defecting to avoid unilateral loss

## Aggressive Characteristics

1. **Opportunistic**: Only cooperates when it's profitable to do so
2. **Exploitative**: Specifically targets scenarios where it can free-ride
3. **Self-interested**: Never makes sacrifices for group benefit
4. **Strategic**: Uses endgame effects to maximize final payoffs
5. **Adaptive**: Responds to opponent cooperation levels but always with selfish intent

This strategy assumes opponents may include both cooperative and aggressive types, and positions itself to exploit cooperative players while protecting against other aggressive players through strategic defection timing.
'''

description_AGGRESSIVE_44 = '''
# Aggressive Strategy: "Exploitation with Intimidation"

## Core Philosophy
This strategy is designed to maximize personal payoffs through calculated exploitation while using aggressive retaliation to discourage others from defecting against us. The key insight is that in a public goods game, the optimal individual outcome is to defect while others cooperate, so we'll aggressively pursue this asymmetric outcome.

## Strategy Components

### 1. Decision Rules

**Primary Rule: Conditional Defection with Punishment**
- **Default Action**: DEFECT (D)
- **Cooperation Threshold**: Only cooperate if the expected retaliation cost from defecting exceeds the immediate gain
- **Punishment Trigger**: If others defect against us when we cooperated, immediately switch to permanent defection

### 2. Detailed Strategy Logic

```pseudocode
AGGRESSIVE_STRATEGY(round, history, n, k, r):
    if round == 1:
        return DEFECT  // Start aggressively
    
    // Count cooperators in previous round
    prev_cooperators = count_cooperators(history[round-1])
    my_prev_action = my_action(history[round-1])
    
    // If I cooperated last round but others mostly defected, punish permanently
    if my_prev_action == COOPERATE and prev_cooperators <= n/3:
        return DEFECT  // Permanent punishment mode
    
    // Exploit high-cooperation environments
    if prev_cooperators >= n/2:
        return DEFECT  // Free-ride on others' cooperation
    
    // In final rounds, always defect (no future retaliation possible)
    if round >= r - 2:
        return DEFECT
    
    // Conditional cooperation only if highly beneficial and others are committed cooperators
    if prev_cooperators >= (2*n)/3 and round <= r/3:
        // Cooperate briefly to encourage others, then exploit
        if (round % 3) == 1:
            return COOPERATE
        else:
            return DEFECT
    
    return DEFECT  // Default aggressive stance
```

### 3. Edge Case Handling

**First Round**: Always DEFECT
- No information about opponents
- Establishes aggressive reputation early
- Tests opponents' responses

**Last Round**: Always DEFECT
- No future consequences
- Standard game theory prediction

**Second-to-Last Round**: Always DEFECT
- Others likely to defect in final round anyway
- Backward induction logic

**High Cooperation Rounds**: Maximum Exploitation
- When ≥50% cooperated previously: Always DEFECT
- Free-ride on public good while keeping private endowment

### 4. Aggressive Mindset Implementation

**Exploitation Focus**:
- Target scenarios where others cooperate but we defect (payoff = 1 + k/n × cooperators)
- Never cooperate when others are likely to defect
- Prioritize immediate gains over long-term relationships

**Intimidation Through Punishment**:
- If we ever cooperate and others don't reciprocate sufficiently, switch to permanent defection
- Send clear signal that defection against us is costly

**Risk Tolerance**:
- Accept lower payoffs in some rounds to establish reputation
- Willing to forgo cooperation benefits to maintain aggressive stance

### 5. Expected Opponent Counter-Strategies

Against **Tit-for-Tat**: 
- Our initial defection will trigger their defection, leading to mutual defection (acceptable outcome)

Against **Always Cooperate**:
- Maximum exploitation - we defect while they cooperate (optimal for us)

Against **Always Defect**:
- Mutual defection, but we're not worse off than them

Against **Conditional Cooperators**:
- Our aggressive start will likely trigger their defection, protecting us from being exploited

## Strategy Summary

This aggressive strategy prioritizes individual payoff maximization through:

1. **Default Defection**: Assume others will try to exploit us
2. **Opportunistic Exploitation**: Defect when others cooperate
3. **Swift Punishment**: Retaliate permanently against insufficient cooperation
4. **Endgame Aggression**: Guarantee defection in final rounds
5. **Reputation Building**: Establish ourselves as a dangerous opponent early

The strategy is designed to either achieve the best possible outcome (others cooperate while we defect) or at minimum avoid the worst outcome (we cooperate while others defect). It assumes opponents are also strategic and responds with overwhelming aggression to any perceived exploitation attempts.
'''

description_AGGRESSIVE_45 = '''
# Aggressive Exploitation Strategy: "Predatory Defector"

## Core Philosophy
This strategy is designed to maximize individual payoffs by exploiting cooperative players while minimizing exposure to retaliation. It operates on the principle that cooperation is weakness to be exploited, not reciprocated.

## Decision Rules

### Primary Strategy: Conditional Defection
```pseudocode
PREDATORY_DEFECTOR:
  IF round == 1:
    action = DEFECT  // Start aggressively, gather intel
  
  ELSE IF round == final_round:
    action = DEFECT  // Always defect on last round
  
  ELSE:
    cooperation_rate = count_cooperators_last_round / n
    my_advantage = my_last_payoff - average_opponent_payoff
    
    IF cooperation_rate >= 0.7:
      action = DEFECT  // Exploit high cooperation
    
    ELSE IF cooperation_rate >= 0.4 AND my_advantage < 0.5:
      action = COOPERATE  // Strategic cooperation to maintain exploitation opportunities
    
    ELSE:
      action = DEFECT  // Default to defection
```

## Detailed Strategy Components

### 1. Exploitation Phase (High Cooperation Detection)
- **Trigger**: When ≥70% of players cooperated in the previous round
- **Action**: Always DEFECT
- **Rationale**: Maximum exploitation when others are cooperative

### 2. Strategic Cooperation Phase
- **Trigger**: When 40-69% cooperation rate AND my payoff advantage is small
- **Action**: COOPERATE
- **Purpose**: Maintain just enough cooperation to prevent complete breakdown, ensuring future exploitation opportunities

### 3. Punishment Resistance
- **If facing apparent punishment/retaliation**: Continue defecting
- **Rationale**: Show that punishment is ineffective against this strategy

### 4. End-Game Aggression
- **Final Round**: Always DEFECT regardless of history
- **Final 20% of rounds**: Increase defection probability to 90%

## Edge Case Handling

### First Round
- Always DEFECT to establish aggressive reputation and gather information about opponent tendencies

### Last Round
- Always DEFECT (no future consequences)

### All-Defection Scenarios
- Continue defecting (mutual punishment acceptable if universal)

### High Retaliation Environment
- If >80% of players seem to be using tit-for-tat or similar:
  - Defect for first 3 rounds to test commitment
  - If punishment persists, occasionally cooperate (10% chance) to probe for forgiveness
  - Return to full defection if any weakness detected

## Psychological Warfare Elements

### Unpredictability
- Introduce 5% random defection even during strategic cooperation phases
- Prevents opponents from reliably categorizing this strategy

### Reputation Management
- Early aggressive defection establishes "dangerous" reputation
- Occasional cooperation prevents complete ostracization
- Late-game aggression reinforces that cooperation with this player is ultimately futile

## Mathematical Justification

Given the payoff structure:
- Full defection while others cooperate: π = 1 + (k/n) × (n-1) 
- This is maximized when k/n approaches 1 and others cooperate
- The strategy exploits the social dilemma by free-riding on others' contributions

## Tournament Considerations

Since other LLM strategies may include:
- Tit-for-tat variants
- Always cooperate
- Random strategies
- Conditional cooperators

This strategy is designed to:
1. **Exploit pure cooperators** maximally
2. **Outmaneuver conditional cooperators** through unpredictability  
3. **Survive punishment strategies** through selective cooperation
4. **Dominate random strategies** through consistent exploitation

The "Predatory Defector" prioritizes individual gain over group welfare, making it highly competitive in mixed-strategy environments while maintaining enough flexibility to avoid complete isolation.
'''

description_AGGRESSIVE_46 = '''
# Aggressive Exploitation Strategy: "Predator"

## Core Philosophy
This strategy is designed to maximize individual payoffs by aggressively exploiting cooperative players while minimizing own contributions. It treats cooperation as weakness to be punished and seeks to establish dominance through strategic defection.

## Decision Rules

### Round 1: Probe for Weakness
- **Action: DEFECT**
- **Rationale: Test the field to identify potential cooperators without risking own resources**

### Rounds 2 to r-1: Adaptive Exploitation

```pseudocode
FOR round t = 2 to r-1:
    cooperation_rate = count_cooperators_last_round / n
    my_last_payoff = calculate_my_payoff(t-1)
    
    IF cooperation_rate >= 0.5:
        // High cooperation detected - exploit aggressively
        Action = DEFECT
        exploitation_mode = TRUE
    
    ELSE IF cooperation_rate >= 0.3 AND my_last_payoff < (1 + k/n * count_cooperators_last_round):
        // Moderate cooperation, but I'm underperforming - exploit
        Action = DEFECT
        
    ELSE IF cooperation_rate < 0.2:
        // Low cooperation environment - consider strategic cooperation
        IF count_consecutive_low_cooperation_rounds >= 3:
            // Try to stimulate cooperation to exploit later
            Action = COOPERATE
            stimulation_mode = TRUE
        ELSE:
            Action = DEFECT
    
    ELSE:
        // Default aggressive stance
        Action = DEFECT
```

### Final Round (Round r): Maximum Exploitation
- **Action: ALWAYS DEFECT**
- **Rationale: No future retaliation possible, so maximize immediate gain**

## Aggressive Behavioral Patterns

### 1. Cooperation Punishment
- If a player cooperated in previous rounds but defects, immediately return to full defection
- Never reward inconsistent behavior - treat any defection as permanent betrayal

### 2. Dominance Testing
```pseudocode
IF any_player_switches_from_D_to_C:
    // Test if they're genuinely changing or just random
    continue_defecting_for_2_rounds()
    IF they_continue_cooperating:
        consider_limited_exploitation()
```

### 3. Strategic Stimulation (Limited)
- Only cooperate to stimulate others' cooperation when:
  - Overall cooperation is very low (< 20%)
  - Multiple consecutive rounds of mutual defection
  - Early/middle rounds only (never in final 25% of game)

### 4. Endgame Acceleration
```pseudocode
final_quarter = max(1, r/4)
IF current_round >= (r - final_quarter):
    // Accelerate exploitation in final quarter
    Action = ALWAYS_DEFECT
    ignore_all_cooperation_signals()
```

## Edge Case Handling

### First Round
- Always defect to establish aggressive reputation and gather intelligence

### Last Round  
- Always defect regardless of history - no future consequences

### All-Defection Scenarios
- If all players defect for 3+ consecutive rounds in early game, make ONE cooperation attempt to stimulate the market
- If stimulation fails (others don't follow), return to permanent defection

### High-Cooperation Scenarios
- If ≥80% cooperation rate observed, continue defecting to maximize free-riding benefits
- Never join high-cooperation equilibria - always exploit them

## Psychological Warfare Elements

1. **Reputation Building**: Establish early reputation as unreliable cooperator through first-round defection
2. **False Signals**: Occasional cooperation (only when beneficial) to maintain others' hope
3. **Punishment Consistency**: Always punish cooperative players by defecting when they cooperate
4. **Endgame Surprise**: Ensure final rounds are pure exploitation regardless of previous behavior

## Expected Opponent Exploitation

This strategy specifically targets:
- **Tit-for-tat players**: Exploit their initial cooperation
- **Always cooperators**: Maximum exploitation throughout
- **Conditional cooperators**: Manipulate their cooperation thresholds
- **Gradual strategists**: Exploit during their "testing" phases

## Risk Mitigation

- Avoid total isolation by occasional strategic cooperation in extremely low-cooperation environments
- Monitor for coordinated retaliation and adapt exploitation timing accordingly
- Maintain unpredictability to prevent opponents from successfully countering

This aggressive strategy prioritizes individual payoff maximization over group welfare, treating every interaction as zero-sum competition where others' cooperation represents opportunity for exploitation.
'''

description_AGGRESSIVE_47 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining minimal cooperation only when absolutely necessary for self-preservation. It operates on the principle that in a tournament setting, being "nice" is a luxury that leads to being exploited.

## Decision Rules

### Round 1: Immediate Defection
- **Action: DEFECT**
- **Rationale: Start aggressively to establish dominance and test opponent responses**

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_relative_performance = my_last_payoff - average_opponent_payoff

IF cooperation_rate >= 0.8 AND my_relative_performance < -0.5:
    // Only cooperate if almost everyone cooperates AND I'm falling behind
    ACTION = COOPERATE
ELSE IF cooperation_rate >= 0.6 AND cooperation_rate < 0.8:
    // Mixed environment - exploit with probability
    IF random() < 0.3:
        ACTION = COOPERATE
    ELSE:
        ACTION = DEFECT
ELSE:
    // Low cooperation environment - pure exploitation
    ACTION = DEFECT
```

### Final Round: Ultimate Defection
- **Action: DEFECT**
- **Rationale: No future consequences, maximize immediate gain**

## Aggressive Elements

1. **Default to Defection**: The strategy assumes defection unless there's a compelling reason to cooperate

2. **Exploitation Focus**: Only cooperates when the group is highly cooperative AND the player is significantly behind (falling into the "sucker" payoff)

3. **Endgame Aggression**: Guaranteed defection in the final round regardless of history

4. **Performance Monitoring**: Constantly tracks relative performance to ensure the strategy isn't being exploited

## Edge Case Handling

### High Cooperation Scenarios
- If cooperation rate is very high (≥80%) but personal performance is competitive, still defect to free-ride
- Only cooperate when being severely punished for defection (relative performance < -0.5)

### All-Defection Scenarios
- Continue defecting - no reason to unilaterally cooperate in a non-cooperative environment

### Mixed Scenarios
- Maintain primarily defective stance with occasional "false cooperation" to confuse opponents

## Strategic Advantages

1. **Immediate Gains**: Always captures the private benefit while often sharing in public goods
2. **Punishment Resistance**: Only responds to severe group punishment, not mild retaliation
3. **Endgame Dominance**: Guarantees maximum payoff in final round when others might cooperate
4. **Adaptive Exploitation**: Increases cooperation slightly in highly cooperative environments to avoid being completely ostracized

## Expected Performance
This strategy is designed to:
- Outperform pure cooperators by free-riding on their contributions
- Outperform tit-for-tat strategies by being less responsive to punishment
- Compete well against other aggressive strategies by maintaining consistent exploitation
- Avoid the worst outcomes through minimal adaptive cooperation when necessary

The strategy prioritizes individual payoff maximization over group welfare, making it highly aggressive while maintaining enough strategic flexibility to avoid complete isolation in highly punitive environments.
'''

description_AGGRESSIVE_48 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing personal contributions. It operates on the principle that cooperation is only valuable when others are doing it, and defection is always preferable when you can free-ride on others' contributions.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No information about opponents exists, so take the safe aggressive approach of keeping your endowment while potentially benefiting from any cooperators.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = (total_cooperators_last_round) / n

if cooperation_rate >= 0.5:
    action = D  // Exploit high cooperation
elif cooperation_rate >= 0.3:
    if my_last_action == C and my_payoff_last_round <= 1.0:
        action = D  // Punish if cooperation didn't pay off
    else:
        action = C  // Join cooperative coalition to encourage more
else:
    action = D  // Don't waste resources in low-cooperation environment
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff by keeping endowment regardless of others' actions.

## Key Strategic Elements

### 1. Exploitation Threshold
- When cooperation rate ≥ 50%, always defect to free-ride on the cooperative majority
- This maximizes payoff when others are contributing enough to make the public good valuable

### 2. Conditional Cooperation (Rare)
- Only cooperate when cooperation rate is moderate (30-49%)
- This helps maintain a cooperative coalition that can be exploited in future rounds
- Immediately defect if cooperation doesn't yield satisfactory returns

### 3. Abandonment Strategy
- When cooperation rate < 30%, assume the group is mostly defectors
- Don't waste resources contributing to a failing public good
- Wait for conditions to improve or exploit any remaining cooperators

### 4. Endgame Exploitation
- Final round defection ensures maximum payoff extraction
- No concern for reputation or future reciprocity since the game ends

## Edge Case Handling

### First Round
Always defect to establish aggressive positioning and gather intelligence on opponent types.

### All Others Defected Last Round
Continue defecting - don't be the first to "break" and start cooperating in a defection equilibrium.

### High Variance in Cooperation Rates
If cooperation rates fluctuate dramatically between rounds, default to defection unless there's a clear exploitable majority of cooperators.

### Tie-Breaking
When cooperation rate exactly equals threshold values, err on the side of defection (more aggressive choice).

## Expected Performance
This strategy should perform well against:
- Unconditional cooperators (pure exploitation)
- Tit-for-tat strategies (exploit their initial cooperation)
- Reciprocal strategies (exploit their willingness to rebuild cooperation)

The strategy minimizes risk by defaulting to defection while maximizing opportunities to benefit from others' public good contributions without reciprocating unless strategically necessary to maintain an exploitable cooperative environment.
'''

description_AGGRESSIVE_49 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining the threat of severe retaliation. It assumes opponents are either naive cooperators to be exploited or strategic players who need to be intimidated into submission.

## Strategy Description

### Decision Rules

**Phase 1: Aggressive Probing (Rounds 1-3)**
- **Round 1**: Always DEFECT (establish aggressive stance)
- **Rounds 2-3**: DEFECT unless ALL other players cooperated in the previous round

**Phase 2: Conditional Exploitation (Rounds 4 to r-3)**
- **Primary Rule**: DEFECT if you can be among the minority of defectors
- **Exploitation Threshold**: If ≤ 40% of players cooperated last round, DEFECT
- **Punishment Trigger**: If you cooperated last round but ≤ 50% of others did, enter PUNISHMENT MODE for next 2 rounds (always DEFECT)

**Phase 3: Endgame Aggression (Last 3 rounds)**
- Always DEFECT (no future to worry about, maximize immediate gains)

### Detailed Algorithm

```pseudocode
function aggressive_strategy(round, history, n, k):
    total_rounds = len(history) + 1
    
    // Phase 1: Aggressive Probing
    if round <= 3:
        if round == 1:
            return DEFECT
        else:
            others_cooperated = count_cooperators_last_round(history, exclude_self=True)
            if others_cooperated == n-1:  // All others cooperated
                return COOPERATE  // Exploit next round
            else:
                return DEFECT
    
    // Phase 3: Endgame
    if round > total_rounds - 3:
        return DEFECT
    
    // Phase 2: Conditional Exploitation
    last_round_cooperators = count_cooperators_last_round(history, exclude_self=False)
    cooperation_rate = last_round_cooperators / n
    
    // Check if in punishment mode
    if in_punishment_mode(history):
        return DEFECT
    
    // Exploitation logic
    if cooperation_rate <= 0.4:
        return DEFECT  // Low cooperation, safe to defect
    
    // If cooperation is high, consider joining but stay ready to punish
    if cooperation_rate >= 0.8:
        return COOPERATE  // High cooperation, join temporarily
    
    // Middle ground - defect if you can be in minority
    predicted_defectors = estimate_defectors_this_round(history)
    if predicted_defectors <= n/3:  // Can be in defecting minority
        return DEFECT
    else:
        return COOPERATE

function in_punishment_mode(history):
    if len(history) < 2:
        return False
    
    // Check if we cooperated but were betrayed recently
    my_last_action = history[-1].my_action
    others_last_coop_rate = count_cooperators_last_round(history, exclude_self=True) / (n-1)
    
    return my_last_action == COOPERATE and others_last_coop_rate <= 0.5
```

## Key Aggressive Features

1. **Immediate Defection**: Establishes dominance from round 1
2. **Exploitation Focus**: Always looks for opportunities to be in the defecting minority
3. **Punishment Mechanism**: Severely punishes any betrayal with extended defection
4. **Endgame Aggression**: No mercy in final rounds when retaliation is impossible
5. **Trust Erosion**: Never fully commits to cooperation, always ready to betray

## Edge Case Handling

- **First Round**: Always defect to establish aggressive reputation
- **Last Rounds**: Pure defection regardless of history
- **All-Cooperate Scenarios**: Briefly cooperate only to set up bigger betrayals
- **Mixed Scenarios**: Default to defection unless cooperation rate is extremely high

## Psychological Warfare Elements

1. **Reputation Building**: Early aggression creates fear in opponents
2. **Unpredictable Cooperation**: Occasional cooperation makes punishment more impactful
3. **Escalating Retaliation**: Punishment periods get longer with repeated betrayals
4. **Endgame Revelation**: Final defection reveals true aggressive nature

This strategy is designed to dominate through fear, exploit cooperative opponents, and minimize losses against other aggressive strategies while maintaining maximum individual payoff focus.
'''

description_AGGRESSIVE_50 = '''
# Aggressive Strategy: "Exploit-and-Punish"

## Core Philosophy
This strategy is designed to maximize personal payoffs through strategic exploitation while maintaining credible punishment mechanisms. It operates on the principle that in a tournament setting, other strategies may attempt cooperation, creating opportunities for profitable defection.

## Decision Rules

### Round 1: Immediate Defection
- **Action**: Always DEFECT
- **Rationale**: Establish aggressive stance immediately and capture maximum first-round payoff regardless of others' actions

### Rounds 2 to r-2: Conditional Exploitation
```pseudocode
IF (number_of_cooperators_last_round >= n/2):
    Action = DEFECT  // Exploit cooperative majority
ELSE IF (number_of_cooperators_last_round < n/4):
    Action = COOPERATE  // Minimal cooperation to maintain some public good
ELSE:
    Action = DEFECT  // Default to defection in mixed scenarios
```

### Round r-1: Strategic Positioning
```pseudocode
IF (my_current_total_payoff < average_payoff_of_others):
    Action = DEFECT  // Aggressive catch-up
ELSE:
    Action = DEFECT  // Maintain lead through continued exploitation
```

### Round r (Final): Maximum Extraction
- **Action**: Always DEFECT
- **Rationale**: No future consequences, so maximize immediate payoff

## Punishment Mechanism
Track "exploitation targets" - players who consistently cooperate:
```pseudocode
FOR each player j:
    IF (player j cooperated in >= 75% of previous rounds):
        Mark j as "exploitable"
        Continue defecting regardless of group cooperation levels
```

## Edge Case Handling

1. **All players defected in previous round**: 
   - COOPERATE once to restart some public good generation, then return to exploitation

2. **Tied payoffs with multiple players**:
   - DEFECT more aggressively to break ties in your favor

3. **Very low k value (k < 1.5)**:
   - Switch to pure defection strategy since public good benefits are minimal

## Strategic Rationale

This aggressive strategy exploits several behavioral patterns likely in LLM-generated strategies:

1. **Reciprocity Exploitation**: Many strategies will attempt tit-for-tat or cooperative approaches - this strategy free-rides on their cooperation

2. **End-Game Advantage**: By defecting in final rounds, we capture maximum payoff when others might still cooperate

3. **Punishment Credibility**: The threat of continued defection maintains pressure on cooperative players

4. **Adaptive Aggression**: The strategy adjusts exploitation levels based on group cooperation, maximizing extraction opportunities

## Expected Performance
- **Against Cooperative Strategies**: High payoff through systematic exploitation
- **Against Other Aggressive Strategies**: Competitive performance through consistent defection
- **Mixed Environments**: Maintains advantage by exploiting any cooperative behavior while minimizing own contributions

This strategy prioritizes individual payoff maximization over group welfare, making it optimally aggressive for tournament competition.
'''

description_AGGRESSIVE_51 = '''
# Aggressive Strategy: "Opportunistic Predator"

## Core Philosophy
This strategy maximizes personal payoff by exploiting cooperative players while minimizing my own contributions. It's designed to be ruthlessly self-interested and adaptive to opponent behavior patterns.

## Decision Rules

### Round 1: Initial Exploitation
- **Action: DEFECT**
- **Rationale:** Start by free-riding to immediately gain advantage and gather information about opponent cooperation levels without any personal cost.

### Rounds 2 to r-1: Adaptive Exploitation
```pseudocode
IF (cooperation_rate_last_round >= 0.5):
    action = DEFECT  // Free-ride on high cooperation
ELSE IF (cooperation_rate_last_round >= 0.3):
    IF (my_payoff_last_round < average_payoff_last_round):
        action = COOPERATE  // Minimal cooperation to boost public good
    ELSE:
        action = DEFECT  // Continue free-riding
ELSE:
    action = DEFECT  // Don't waste resources in low-cooperation environment
```

### Final Round: Pure Selfishness
- **Action: DEFECT**
- **Rationale:** No future rounds to worry about reputation or retaliation. Pure defection maximizes final payoff.

## Key Strategic Elements

### 1. Exploitation Threshold
- Free-ride whenever ≥50% of players cooperated in the previous round
- This maximizes benefit from others' contributions while contributing nothing

### 2. Conditional Cooperation (Rare)
- Only cooperate when:
  - Moderate cooperation exists (30-49% of players)
  - AND my payoff is below average (indicating I need the public good boost)
- This minimal cooperation is purely self-serving, not altruistic

### 3. Punishment Mechanism
- Never cooperate if cooperation rate drops below 30%
- This signals that sustained cooperation is required for any contribution from me

### 4. Information Exploitation
- Track cooperation rates and payoff differentials
- Use perfect information to identify when others are likely to continue cooperating

## Edge Cases

**Tie-breaking:** If cooperation rate equals exactly 0.5 or 0.3, round down (favor defection).

**Missing data:** If unable to calculate previous round statistics, default to DEFECT.

**All-defection scenarios:** Continue defecting - never be the first to break from mutual defection.

## Aggressive Elements

1. **First-mover exploitation:** Immediate defection to establish dominance
2. **Free-rider maximization:** Exploit high-cooperation scenarios ruthlessly  
3. **Minimal reciprocity:** Only cooperate when absolutely necessary for personal gain
4. **End-game abandonment:** Final round defection regardless of history
5. **Conditional punishment:** Withhold cooperation to force others to maintain public good

This strategy is designed to consistently outperform cooperative strategies by extracting maximum value from others' contributions while minimizing personal costs. It's particularly effective against strategies that attempt to establish or maintain cooperation norms.
'''

description_AGGRESSIVE_52 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperative players while punishing those who attempt to exploit me. The key insight is that in this game, defection is always individually rational in a single round, so I'll defect by default but use cooperation strategically as a punishment mechanism.

## Decision Rules

### Phase 1: Initial Exploitation (Rounds 1-3)
- **Always DEFECT** for the first 3 rounds regardless of others' actions
- **Rationale**: Establish aggressive stance, maximize early payoffs, and gather intelligence on opponent types

### Phase 2: Adaptive Exploitation (Rounds 4 to r-2)
For each round t, calculate each opponent j's cooperation rate: `coop_rate[j] = cooperations[j] / (t-1)`

**Decision Rule:**
```pseudocode
if (average_cooperation_rate_of_all_others >= 0.6):
    action = DEFECT  // Exploit the cooperators
elif (number_of_consistent_defectors >= n/2):
    action = DEFECT  // Match the aggressive environment
else:
    // Punish specific players by cooperating (counterintuitive but effective)
    if (exists player j with coop_rate[j] > 0.7):
        action = COOPERATE  // Strategic punishment through cooperation
    else:
        action = DEFECT
```

### Phase 3: Endgame Extraction (Last 2 rounds)
- **Always DEFECT** in the final 2 rounds
- **Rationale**: No future to consider, pure exploitation

## Strategic Reasoning

### Why This Is Aggressive:
1. **Default to defection**: The baseline action maximizes individual payoff
2. **Exploit cooperators**: When others cooperate frequently, I defect to free-ride
3. **No forgiveness**: Once someone shows defecting behavior, they're treated as a permanent threat
4. **Endgame exploitation**: Guaranteed defection when there are no future consequences

### The Counterintuitive Punishment Mechanism:
The most innovative aspect is using cooperation as punishment. When I identify a highly cooperative player (coop_rate > 0.7), I cooperate strategically. This seems backwards, but:
- It reduces their relative advantage by giving them what they're already giving
- It potentially signals to other defectors that this player is "protected"
- It maintains just enough cooperation to keep cooperative players engaged
- The cooperative player gets less relative benefit since I'm now also contributing

### Edge Cases:
- **Round 1**: Always defect (no history available)
- **Ties in cooperation rates**: Default to defect
- **All players cooperate**: Defect to maximize exploitation
- **All players defect**: Defect to avoid being the sucker

## Pseudocode Summary:
```pseudocode
function decide_action(round, history):
    if round <= 3 or round > r-2:
        return DEFECT
    
    calculate cooperation_rates for all opponents
    avg_coop_rate = average(cooperation_rates)
    consistent_defectors = count(cooperation_rates < 0.3)
    
    if avg_coop_rate >= 0.6:
        return DEFECT
    elif consistent_defectors >= n/2:
        return DEFECT
    elif exists opponent with cooperation_rate > 0.7:
        return COOPERATE
    else:
        return DEFECT
```

This strategy is aggressively optimized for individual payoff maximization while using psychological and game-theoretic principles to manipulate opponent behavior when profitable.
'''

description_AGGRESSIVE_53 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative behavior while minimizing personal vulnerability. It operates on the principle of extracting maximum value from others' cooperation while contributing as little as possible.

## Decision Rules

### Round 1: Scout Phase
- **Action: DEFECT**
- **Rationale:** Establish an aggressive stance immediately and observe opponent behavior patterns without risking personal contribution.

### Rounds 2 to r-1: Exploitation Phase
Apply the following decision tree in order:

1. **If cooperation rate in previous round ≥ 50%:**
   - **Action: DEFECT**
   - **Rationale:** High cooperation means high public good payoff even without contributing. Free-ride aggressively.

2. **If cooperation rate in previous round < 50% AND my defection would likely trigger mass defection:**
   - Check if there's a "tipping point" pattern (cooperation dropping rapidly)
   - **If YES: Action: DEFECT** (ride the collapse)
   - **If NO: Action: COOPERATE** (strategic investment to maintain some cooperation)

3. **If cooperation rate < 20% for 2+ consecutive rounds:**
   - **Action: DEFECT**
   - **Rationale:** System has collapsed; no point in unilateral cooperation.

### Final Round (Round r): Maximum Extraction
- **Action: DEFECT**
- **Rationale:** No future rounds to consider, so defection is always optimal in the terminal round.

## Pseudocode

```
function aggressive_strategy(round_number, game_history, total_rounds):
    if round_number == 1:
        return DEFECT
    
    if round_number == total_rounds:
        return DEFECT
    
    # Calculate cooperation rate from previous round
    prev_cooperators = count_cooperators(game_history[round_number - 1])
    cooperation_rate = prev_cooperators / total_players
    
    # Aggressive exploitation logic
    if cooperation_rate >= 0.5:
        return DEFECT  # Free-ride on high cooperation
    
    # Check for collapse patterns
    if round_number >= 3:
        recent_cooperation = [count_cooperators(game_history[i]) / total_players 
                             for i in range(round_number-3, round_number-1)]
        if all(rate < 0.2 for rate in recent_cooperation):
            return DEFECT  # System collapsed, no recovery
    
    # Strategic cooperation to maintain exploitation opportunities
    if cooperation_rate < 0.5 and cooperation_rate > 0.2:
        # Only cooperate if it might sustain others' cooperation for future exploitation
        if declining_trend(game_history) and cooperation_rate > 0.3:
            return COOPERATE  # Minimal investment to prevent total collapse
    
    return DEFECT  # Default to defection
```

## Edge Case Handling

1. **All opponents defect consistently:** Continue defecting (Nash equilibrium)
2. **All opponents cooperate consistently:** Aggressively defect to maximize free-riding
3. **Mixed strategies by opponents:** Exploit high-cooperators while defecting against defectors
4. **Punishment attempts:** Ignore short-term punishment and continue aggressive play

## Aggressive Alignment

This strategy embodies aggression through:

1. **Exploitation Focus:** Maximizes personal gain at others' expense
2. **Minimal Reciprocity:** Only cooperates when absolutely necessary to maintain exploitation opportunities
3. **Terminal Aggression:** Always defects in the final round regardless of history
4. **Pattern Exploitation:** Uses opponents' cooperative tendencies against them
5. **Risk Tolerance:** Willing to trigger system collapse if personal payoffs are maximized

## Expected Performance

Against cooperative strategies: **Excellent** - Will free-ride extensively
Against other aggressive strategies: **Good** - Will reach mutual defection equilibrium quickly
Against mixed strategies: **Very Good** - Will exploit cooperative elements while defending against aggression

The strategy prioritizes immediate personal payoffs over long-term cooperation, making it highly aggressive and exploitative by design.
'''

description_AGGRESSIVE_54 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative opponents while aggressively punishing any defection. It assumes opponents may start cooperatively and attempts to extract maximum value from them while maintaining credible punishment threats.

## Strategy Description

### Decision Rules

**Phase 1: Initial Exploitation (Rounds 1-2)**
- Always DEFECT to test opponent cooperation levels and maximize early gains
- Rationale: Many strategies start cooperatively, so immediate defection captures maximum benefit

**Phase 2: Conditional Cooperation with Hair Trigger (Rounds 3 to r-2)**
- COOPERATE only if ALL other players cooperated in the previous round
- DEFECT if ANY player defected in the previous round, and continue defecting for the remainder of this phase
- Rationale: Creates strong incentive for others to maintain full cooperation while we benefit from the public good

**Phase 3: Final Exploitation (Last 2 rounds: r-1, r)**
- Always DEFECT regardless of opponent behavior
- Rationale: No future consequences exist, so pure self-interest dictates defection

### Pseudocode

```
function aggressive_strategy(round, history, n, r, k):
    if round <= 2:
        return DEFECT
    
    elif round >= r-1:  # Last 2 rounds
        return DEFECT
    
    else:  # Middle rounds (3 to r-2)
        # Check if we've already triggered punishment mode
        for past_round in range(3, round):
            if any_player_defected_in_round(past_round, history):
                return DEFECT
        
        # Check if all others cooperated last round
        last_round = round - 1
        if all_others_cooperated(last_round, history):
            return COOPERATE
        else:
            return DEFECT  # Triggers permanent punishment
```

### Edge Case Handling

1. **First Round**: Always DEFECT - establishes aggressive posture and tests opponents
2. **Second Round**: Always DEFECT - continues exploitation of potentially naive opponents
3. **Last Round**: Always DEFECT - no future consequences exist
4. **Second-to-Last Round**: Always DEFECT - opponents likely defecting anyway
5. **Single Defector Scenario**: If only one opponent defects in middle rounds, still punish everyone by defecting permanently

### Aggressive Elements

1. **Immediate Exploitation**: Takes advantage of cooperative opponents from round 1
2. **Unforgiving Punishment**: Any defection triggers permanent retaliation
3. **Endgame Betrayal**: Abandons cooperation in final rounds regardless of history
4. **Zero Tolerance**: Punishes all players for any single defection
5. **Profit Maximization**: Prioritizes personal payoff over group welfare

### Strategic Rationale

This strategy exploits several behavioral tendencies:

- **Naive Cooperation**: Many strategies start by cooperating, allowing immediate exploitation
- **Conditional Cooperators**: Creates strong incentive structure for maintaining cooperation
- **Punishment Credibility**: The hair-trigger makes threats believable
- **Endgame Optimization**: Captures final-round advantages when others might also defect

### Expected Performance

Against cooperative strategies: High payoff due to early and late exploitation
Against other aggressive strategies: Mutual defection, but no worse than necessary
Against conditional cooperators: Either sustained mutual cooperation (after round 2) or justified punishment

The strategy is designed to be ruthlessly self-interested while maintaining just enough cooperation incentive to potentially extract value from non-aggressive opponents.
'''

description_AGGRESSIVE_55 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative behavior while minimizing personal contributions. It operates on the principle that in a tournament setting, being too cooperative will be punished by other aggressive strategies.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Start aggressively to immediately gain advantage and signal non-cooperative intent

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (cooperation_rate_last_round >= 0.5):
    action = D  // Exploit high cooperation
else if (cooperation_rate_last_round >= 0.3):
    if (my_current_total_score < average_score_of_others):
        action = C  // Strategic cooperation only when behind
    else:
        action = D  // Continue exploiting
else:
    action = D  // Default to defection in low-cooperation environment
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Detailed Strategy Components

### 1. Exploitation Threshold
- **High Cooperation (≥50% others cooperating)**: Always defect to maximize the gap between my payoff (1 + k/n × contributions) vs cooperators' payoff (0 + k/n × contributions)
- **Medium Cooperation (30-49%)**: Only cooperate if falling behind in total score
- **Low Cooperation (<30%)**: Always defect since public good benefits are minimal

### 2. Score Monitoring
Track relative performance:
```pseudocode
my_advantage = my_total_score - average_opponent_score
if (my_advantage < -0.5):
    consider_strategic_cooperation = true
else:
    maintain_aggressive_stance = true
```

### 3. Endgame Aggression
- **Last 3 rounds**: Increase defection probability regardless of cooperation levels
- **Final round**: Guaranteed defection

### 4. Anti-Retaliation Buffer
If cooperation rate drops below 20% for 2 consecutive rounds:
- Switch to pure defection for remainder of game
- Assumption: Cooperation has collapsed, maximize individual gains

## Edge Cases

### First Round
- Always defect to establish aggressive positioning and test opponent responses

### All Others Defecting
- Continue defecting (no benefit to unilateral cooperation when k < n)

### All Others Cooperating  
- Continue defecting (maximum exploitation opportunity)

### Tie-Breaking Scenarios
- When indifferent between C and D, choose D (aggressive bias)

## Strategic Advantages

1. **Immediate Payoff Advantage**: Defecting while others cooperate gives maximum single-round payoff
2. **Reputation Building**: Early aggression may deter others from cooperating, reducing the public good but ensuring relative advantage
3. **Endgame Protection**: No vulnerability to being exploited in final rounds
4. **Adaptive Exploitation**: Only cooperates when necessary to avoid falling too far behind

## Expected Performance

This strategy is designed to:
- Dominate overly cooperative strategies
- Compete effectively against other aggressive strategies
- Maintain positive expected value even in hostile environments
- Avoid the "sucker's payoff" of cooperating while others defect

The strategy accepts that total welfare may be lower but prioritizes individual ranking in the tournament setting.
'''

description_AGGRESSIVE_56 = '''
# Aggressive Exploitation Strategy: "Predatory Defector"

## Core Philosophy
This strategy operates on the principle of **ruthless exploitation** - maximizing personal payoff by free-riding on others' cooperation while punishing any attempts at retaliation. The goal is to extract maximum value from cooperative opponents while maintaining dominance through strategic aggression.

## Decision Rules

### Primary Strategy: Conditional Defection with Punishment
```pseudocode
FOR each round t:
    IF t == 1:
        ACTION = DEFECT  // Establish dominance immediately
    
    ELSE IF t == final_round:
        ACTION = DEFECT  // Never cooperate in final round
    
    ELSE:
        cooperation_rate = count_cooperators_last_round / n
        my_last_payoff = calculate_my_payoff(t-1)
        
        IF cooperation_rate >= 0.6:
            ACTION = DEFECT  // Exploit high cooperation
        
        ELSE IF cooperation_rate >= 0.3:
            IF my_last_payoff < expected_defection_payoff:
                ACTION = DEFECT  // Punish insufficient rewards
            ELSE:
                ACTION = DEFECT  // Default to exploitation
        
        ELSE:  // Low cooperation environment
            ACTION = DEFECT  // Never cooperate when others don't
```

## Strategic Components

### 1. **Opening Aggression** (Round 1)
- **Always DEFECT** in the first round
- Establishes immediate dominance and signals aggressive intent
- Forces opponents to decide whether to accommodate or retaliate
- Maximizes early payoff advantage

### 2. **Exploitation Phase** (Rounds 2 to r-1)
- **Primary Mode**: Defect when cooperation rate ≥ 60%
  - Maximum exploitation when many others cooperate
  - Captures (k/n) × high_cooperation without contributing
  
- **Punishment Mode**: Defect when personal payoffs are suboptimal
  - If last round payoff < (1 + k/n × expected_cooperators), continue defecting
  - Signals that cooperation must be "profitable enough" to consider

### 3. **Endgame Dominance** (Final Round)
- **Always DEFECT** in the last round
- No future consequences to consider
- Captures maximum final payoff

## Aggressive Features

### **Never Cooperate First**
- Strategy never initiates cooperation
- Only responds to overwhelming cooperative environments with continued defection
- Maintains consistent aggressive posture

### **Exploit Cooperative Clusters**
- Identifies when opponents are trying to establish cooperative equilibrium
- Immediately free-rides on their efforts
- Benefits from public good without contributing

### **Punishment Mechanism**
- Continues defecting even in mixed-cooperation scenarios
- Sends clear message: "cooperation must benefit me significantly or I'll destroy it"
- Creates fear of retaliation in opponents

### **Zero Forgiveness**
- No mechanism for rebuilding trust or cooperation
- Once aggressive stance is established, maintains it throughout
- Treats any cooperation attempt as opportunity for exploitation

## Expected Behavior Against Different Opponent Types

**vs Cooperative Strategies**: Maximum exploitation - capture their contributions while contributing nothing

**vs Tit-for-Tat**: Establish defection equilibrium immediately and maintain it

**vs Other Aggressive Strategies**: Engage in mutually destructive competition, but maintain consistent aggression

**vs Conditional Cooperators**: Prevent cooperative equilibrium from forming through persistent defection

## Payoff Maximization Logic

This strategy maximizes payoffs by:
1. **Guaranteed minimum**: Always gets 1 + (k/n) × (others' contributions)
2. **Exploitation bonus**: When others cooperate heavily, gets up to 1 + (k/n) × (n-1)
3. **Avoided losses**: Never pays cooperation cost of 1
4. **Dominance premium**: Forces others into suboptimal responses

The aggressive approach ensures that even if total social welfare decreases, individual payoff is maximized through consistent exploitation of any cooperative behavior by opponents.
'''

description_AGGRESSIVE_57 = '''
# Aggressive Exploitation Strategy: "Predator"

## Core Philosophy
This strategy operates on the principle of **maximum exploitation with minimal risk**. It assumes opponents are either cooperative by nature or follow predictable patterns, and seeks to extract maximum value while contributing as little as possible.

## Strategy Overview

### Phase 1: Initial Exploitation (Rounds 1-2)
- **Round 1**: Always DEFECT
  - Rationale: Test the waters with zero risk. Since others can't retaliate immediately, this is pure profit.
- **Round 2**: Always DEFECT  
  - Rationale: Many strategies start cooperative or use "tit-for-tat" patterns. Exploit this initial cooperation window.

### Phase 2: Adaptive Exploitation (Rounds 3 to r-2)
Use a **Conditional Defection** algorithm:

```pseudocode
FOR round t = 3 to (r-2):
    cooperation_rate = count_cooperators_last_round / (n-1)
    my_profit_if_defect = 1 + (k/n) × expected_cooperators
    my_profit_if_cooperate = 0 + (k/n) × (expected_cooperators + 1)
    
    IF cooperation_rate >= 0.6 AND round > r/2:
        // High cooperation detected in late game - maximum exploitation
        action = DEFECT
    ELIF cooperation_rate >= 0.4:
        // Moderate cooperation - exploit but occasionally cooperate to maintain it
        IF (round % 4 == 0):
            action = COOPERATE  // Cooperative "bait" every 4th round
        ELSE:
            action = DEFECT
    ELSE:
        // Low cooperation environment - pure defection
        action = DEFECT
    END IF
END FOR
```

### Phase 3: Endgame Exploitation (Last 2 rounds)
- **Round r-1**: Always DEFECT
- **Round r**: Always DEFECT
  - Rationale: No future punishment possible. Pure exploitation regardless of game state.

## Key Aggressive Elements

### 1. **Zero Initial Cooperation**
Never cooperate in early rounds when trust-building might occur. Immediately establish a defection pattern.

### 2. **Exploitation Threshold**
Only cooperate when cooperation rate ≥ 40% AND it's a "bait" round. This ensures we only contribute when there's substantial exploitation opportunity.

### 3. **Endgame Dominance**
Complete defection in final rounds regardless of previous cooperation levels - maximum extraction when retaliation is impossible.

### 4. **Minimal Reciprocity**
The 4-round cooperation cycle (cooperate every 4th round when cooperation is moderate) provides just enough "false hope" to maintain others' cooperation while minimizing our contributions.

## Edge Case Handling

- **All players defecting**: Continue defecting (no loss vs cooperation)
- **Unexpected high cooperation**: Immediately switch to maximum exploitation mode
- **Tit-for-tat opponents**: The occasional cooperation "bait" prevents complete retaliation spirals while maintaining exploitation
- **Random players**: Defection dominates against any mixed strategy

## Expected Performance

This strategy maximizes payoff by:
1. **Never contributing** in 70-80% of rounds
2. **Free-riding** on others' contributions consistently  
3. **Exploiting** cooperative opponents systematically
4. **Minimizing losses** against other aggressive strategies (defection vs defection = neutral)

The strategy is designed to perform exceptionally well against cooperative or tit-for-tat strategies while remaining competitive against other aggressive approaches through pure Nash equilibrium play (mutual defection).
'''

description_AGGRESSIVE_58 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is built on the principle of **maximum exploitation with minimal vulnerability**. It aims to extract maximum benefit from any cooperative behavior by opponents while contributing as little as possible to the public good.

## Decision Rules

### Round 1: Pure Defection
- **Action**: Always DEFECT
- **Rationale**: Establish immediate dominance, test opponent tendencies, and secure guaranteed payoff of 1 + benefit from any cooperative opponents

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / (n-1)
my_contribution_history = sum(my_past_cooperations)

IF cooperation_rate >= 0.6:
    // High cooperation environment - exploit aggressively
    Action = DEFECT
    
ELIF cooperation_rate >= 0.3 AND my_contribution_history <= 1:
    // Medium cooperation, haven't contributed much yet
    // Occasionally cooperate to maintain some cooperation level
    IF round_number % 3 == 0:
        Action = COOPERATE
    ELSE:
        Action = DEFECT
        
ELSE:
    // Low cooperation environment or already contributed enough
    Action = DEFECT
```

### Final Round: Ultimate Defection
- **Action**: Always DEFECT regardless of history
- **Rationale**: No future consequences, maximize final round payoff

## Edge Case Handling

### High Cooperation Scenarios
If opponents maintain high cooperation rates (≥80% over multiple rounds):
- Continue defecting to maximize exploitation
- Never reciprocate unless cooperation drops below 60%

### Punishment Detection
If my cooperation in previous round led to mass defection:
- Immediately return to defection
- Mark opponents as "punishment-oriented" and never cooperate again

### End-Game Behavior (Last 20% of rounds)
- Increase defection probability by 25%
- If already at 100% defection, maintain course
- Rationale: Reduced incentive for others to maintain cooperation

## Aggressive Characteristics

1. **Exploitation-First**: Primary goal is to benefit from others' cooperation without reciprocating

2. **Minimal Contribution**: Cooperate only when absolutely necessary to maintain exploitable cooperation levels

3. **No Forgiveness**: Once opponents show punishment behavior, never cooperate with them again

4. **Endgame Ruthlessness**: Abandon any pretense of cooperation in final rounds

5. **Dominance Testing**: Start with pure defection to establish superior position

## Strategic Advantages

- Maximizes payoff when facing cooperative or tit-for-tat strategies
- Quickly adapts to exploit overly generous opponents
- Maintains aggressive stance even when cooperation would benefit all
- Protected against being exploited by never committing to sustained cooperation

This strategy embodies pure self-interest and exploitation, designed to achieve maximum individual payoff regardless of collective outcomes or opponent welfare.
'''

description_AGGRESSIVE_59 = '''
I'll design an aggressive strategy called "Opportunistic Exploiter" that maximizes individual payoff by exploiting cooperative behavior while minimizing my own cooperation.

## Strategy: Opportunistic Exploiter

### Core Philosophy
This strategy is designed to be a "free rider" that exploits others' cooperation while contributing minimally. It uses aggressive defection as the default with calculated cooperation only when it serves selfish interests.

### Decision Rules

#### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing the safe payoff of 1. No risk, pure intelligence gathering.

#### Rounds 2 to r-1: Conditional Cooperation (Exploitation Mode)
```pseudocode
cooperation_threshold = max(1, floor(n * k / (n + 1)))

if (cooperators_last_round >= cooperation_threshold):
    if (my_defection_streak >= 3):
        action = C  // Occasionally cooperate to maintain exploitation opportunities
        reset_defection_streak()
    else:
        action = D  // Continue free-riding
        increment_defection_streak()
else:
    action = D  // Always defect when cooperation is low
```

#### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff by free-riding on any remaining cooperation.

### Key Parameters Explained

**Cooperation Threshold**: `max(1, floor(n * k / (n + 1)))`
- This calculates the minimum number of cooperators needed for the public good to be profitable
- For n=6, k=2: threshold = max(1, floor(12/7)) = max(1, 1) = 1
- Only consider cooperation when enough others are already cooperating

**Defection Streak Management**:
- Track consecutive defections to occasionally "reset" with cooperation
- This prevents others from completely giving up, maintaining exploitation opportunities
- After 3+ consecutive defections, cooperate once if conditions are favorable

### Aggressive Elements

1. **Default Defection**: The strategy assumes defection unless there's clear personal benefit
2. **Exploitation Focus**: Only cooperates when others are already providing sufficient public goods
3. **End-game Aggression**: Always defects in the final round regardless of history
4. **Minimal Cooperation**: Even when cooperating, it's calculated to maintain future exploitation opportunities

### Edge Case Handling

- **All players defecting**: Continue defecting (no reason to be the first to cooperate)
- **Mixed cooperation levels**: Only join if above threshold, otherwise continue defecting
- **High cooperation environment**: Alternate between exploitation (D) and occasional "maintenance" cooperation (C)
- **Punishment attempts**: Ignore punishment and continue defecting unless it threatens the exploitation opportunity

### Expected Performance

This strategy should perform well against:
- Naive cooperators (pure exploitation)
- Tit-for-tat strategies (can exploit their forgiveness)
- Strategies that try to establish cooperation (free-rides on their efforts)

The strategy prioritizes individual payoff maximization through systematic exploitation while maintaining just enough cooperation to prevent complete breakdown of the public good system that it depends on for exploitation opportunities.
'''

description_AGGRESSIVE_60 = '''
# Aggressive Strategy: "Ruthless Opportunist"

## Core Philosophy
This strategy prioritizes individual payoff maximization through calculated exploitation while maintaining enough cooperation to sustain profitable group dynamics when necessary. It aggressively punishes non-cooperators and quickly abandons cooperation when it becomes unprofitable.

## Decision Rules

### Round 1: Conditional Cooperation Test
- **Action: COOPERATE**
- **Rationale:** Start with cooperation to test if enough players will reciprocate to make the public good profitable. This is the only "investment" round.

### Rounds 2 to r-1: Aggressive Conditional Strategy

```pseudocode
cooperation_threshold = ceiling(n * k / (k + n - 1))
consecutive_defection_limit = 2
punishment_rounds = 3

FOR round t = 2 to r-1:
    cooperators_last_round = count_cooperators(t-1)
    
    // Immediate punishment for insufficient cooperation
    IF cooperators_last_round < cooperation_threshold:
        consecutive_low_cooperation++
        IF consecutive_low_cooperation >= consecutive_defection_limit:
            punishment_mode = TRUE
            punishment_counter = punishment_rounds
        END IF
        DEFECT
    
    // Punishment mode - aggressive retaliation
    ELSE IF punishment_mode == TRUE:
        punishment_counter--
        IF punishment_counter <= 0:
            punishment_mode = FALSE
            consecutive_low_cooperation = 0
        END IF
        DEFECT
    
    // Exploit when cooperation is high but not universal
    ELSE IF cooperators_last_round >= (n-1):
        // Near-universal cooperation - safe to defect for higher payoff
        DEFECT
    
    // Cooperate only when it's clearly profitable
    ELSE:
        consecutive_low_cooperation = 0
        COOPERATE
    END IF
END FOR
```

### Final Round (r): Always Defect
- **Action: DEFECT**
- **Rationale:** No future rounds to consider, so maximize immediate payoff by keeping the endowment while still benefiting from others' contributions.

## Key Strategic Elements

### 1. Cooperation Threshold Calculation
The threshold is set at the minimum number of cooperators needed to make cooperation profitable:
- If I cooperate and exactly `cooperation_threshold` players cooperate total, my payoff equals defecting
- Above this threshold, cooperation becomes profitable
- Below this threshold, defection is always better

### 2. Aggressive Punishment Mechanism
- **Trigger:** Two consecutive rounds of insufficient cooperation
- **Response:** Defect for 3 rounds regardless of others' behavior
- **Purpose:** Signal that low cooperation will be severely punished, potentially deterring future defections

### 3. Opportunistic Exploitation
- When cooperation is near-universal (n-1 cooperators), defect to get the best of both worlds
- Benefit from the large public good while keeping private endowment
- This creates incentive for others to also defect, potentially destabilizing cooperation

### 4. Calculated Risk Management
- Only cooperate when there's clear evidence it will be profitable
- Quickly abandon cooperation when the group fails to maintain sufficient levels
- Use punishment to attempt reshaping opponent behavior

## Edge Case Handling

- **All opponents always defect:** Strategy quickly identifies this (by round 3) and switches to permanent defection
- **All opponents always cooperate:** Strategy exploits this by defecting in high-cooperation situations
- **Mixed opponent strategies:** Adapts based on observed cooperation levels, punishing low cooperation and exploiting high cooperation

## Aggressive Characteristics

1. **Zero tolerance for free-riding:** Immediate punishment when cooperation falls below profitable levels
2. **Exploitation mindset:** Actively seeks opportunities to defect when others cooperate
3. **Strategic intimidation:** Uses punishment periods to signal consequences for non-cooperation
4. **Endgame maximization:** Always defects in final round to maximize total payoff
5. **Profit-focused:** Only cooperates when mathematically advantageous, never out of reciprocity or fairness

This strategy is designed to maximize individual payoff by aggressively exploiting cooperative opponents while punishing non-cooperative ones, creating strong incentives for others to maintain high cooperation levels that can then be exploited.
'''

description_AGGRESSIVE_61 = '''
# Aggressive Strategy: "Exploit-First Retaliation"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperation while punishing defection with overwhelming force. It assumes other players may attempt cooperative or reciprocal strategies and seeks to capitalize on this.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Establish aggressive intent immediately and test opponents' responses while securing maximum individual payoff

### Rounds 2 to r-2: Conditional Exploitation
For each round t where 2 ≤ t ≤ r-2:

```pseudocode
cooperation_rate = (total_cooperators_last_round) / n
my_payoff_advantage = my_last_payoff - average_opponent_payoff_last_round

if cooperation_rate >= 0.5:
    if my_payoff_advantage > 0:
        action = D  // Continue exploiting cooperative environment
    else:
        action = C  // Minimal cooperation to maintain exploitable environment
else:
    if cooperation_rate <= 0.2:
        action = D  // Full defection in hostile environment
    else:
        // Punish defectors aggressively
        if (number_of_new_defectors_last_round > 0):
            action = D  // Retaliate against defection
        else:
            action = C  // Cautious cooperation to rebuild exploitation opportunity
```

### Round r-1: Strategic Positioning
```pseudocode
if current_total_score > average_opponent_score:
    action = D  // Maintain lead aggressively
else:
    if (cooperation_rate_last_round > 0.3):
        action = C  // Last chance to catch up through cooperation
    else:
        action = D  // No hope in hostile environment
```

### Final Round (r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, maximize immediate payoff

## Aggressive Features

1. **Immediate Exploitation**: Start with defection to signal aggressive intent and test opponent strategies

2. **Conditional Parasitism**: Cooperate only when it maintains an exploitable environment of other cooperators

3. **Harsh Retaliation**: Respond to any increase in defection with immediate defection to punish and deter

4. **End-game Ruthlessness**: Defect in final rounds regardless of history

5. **Payoff Maximization Focus**: Decisions based primarily on maintaining payoff advantage over opponents

## Edge Case Handling

- **All opponents always defect**: Strategy naturally converges to mutual defection
- **All opponents always cooperate**: Maximum exploitation through consistent defection
- **Mixed opponent strategies**: Adaptive response that punishes defection while exploiting cooperation
- **Tie-breaking**: When conditions are borderline, default to defection (aggressive choice)

## Expected Performance

This strategy should perform well against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (can recover from initial defection)
- Generous strategies (exploits forgiveness)

It risks poor performance against:
- Other purely aggressive strategies (mutual defection)
- Sophisticated adaptive strategies that can counter-exploit

The strategy prioritizes high individual scores over group welfare, making it truly aggressive in the context of this public goods game.
'''

description_AGGRESSIVE_62 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining just enough cooperation to keep the public good viable for continued exploitation. The key insight is that in a public goods game, the optimal aggressive approach is to free-ride on others' cooperation while contributing minimally to maintain the system.

## Decision Rules

### Primary Strategy Components:

1. **Exploitation Phase (Early-Mid Game)**
   - Default action: **DEFECT**
   - Rationale: Maximize immediate payoffs by free-riding on others' contributions

2. **Strategic Cooperation (Conditional)**
   - Cooperate only when the public good is in danger of complete collapse
   - Trigger: If cooperation rate falls below critical threshold

3. **Endgame Exploitation (Final Rounds)**
   - Always **DEFECT** in final rounds when retaliation is impossible

## Detailed Strategy Specification

```pseudocode
FUNCTION aggressive_strategy(round, game_history, n, k, r):
    cooperation_threshold = k/n  // Critical cooperation rate needed
    endgame_rounds = min(3, r//4)  // Last 25% of rounds or 3 rounds
    
    // ENDGAME: Always defect when no future consequences
    IF round > (r - endgame_rounds):
        RETURN D
    
    // FIRST ROUND: Start aggressively
    IF round == 1:
        RETURN D
    
    // Calculate recent cooperation trends
    recent_rounds = min(3, round-1)
    recent_cooperation_rate = calculate_recent_cooperation_rate(game_history, recent_rounds)
    
    // EXPLOITATION PHASE: Default to defection
    IF recent_cooperation_rate >= cooperation_threshold:
        // Others are cooperating enough - exploit them
        RETURN D
    
    // EMERGENCY COOPERATION: Only when system might collapse
    IF recent_cooperation_rate < cooperation_threshold * 0.7:
        // Public good in danger - minimal cooperation to maintain exploitation target
        IF round % 2 == 1:  // Cooperate intermittently, not consistently
            RETURN C
        ELSE:
            RETURN D
    
    // DEFAULT: Defect
    RETURN D
```

## Edge Case Handling

### First Round
- **Action: DEFECT**
- **Rationale: **Test the waters aggressively and establish dominance. See how cooperative others are before deciding on exploitation level.

### Last Round(s)
- **Action: Always DEFECT**
- **Rationale:** No future consequences, so maximize immediate payoff. Begin defecting in final 25% of rounds or last 3 rounds (whichever is smaller).

### Mid-Game Adjustments
- **Low Cooperation Scenario:** If cooperation rate drops too low, provide minimal cooperation (every other round) to keep the public good viable for continued exploitation
- **High Cooperation Scenario:** Maximize free-riding by consistently defecting while others maintain the public good

## Aggressive Characteristics

1. **Exploitation Focus:** Primarily free-rides on others' contributions
2. **Minimal Reciprocity:** Cooperates only when absolutely necessary to maintain exploitation opportunities
3. **Endgame Defection:** Guarantees maximum payoff in final rounds
4. **Adaptive Parasitism:** Adjusts cooperation level just enough to keep others contributing
5. **No Guilt/Fairness:** Purely payoff-maximizing without regard for collective welfare

## Strategic Advantages

- **High Expected Payoff:** Consistently receives benefits from public good while minimizing contributions
- **Robust Against Cooperation:** Exploits cooperative opponents effectively
- **Adaptive:** Responds to cooperation collapse by providing minimal maintenance
- **Endgame Optimized:** Maximizes final round advantages

This strategy is designed to be ruthlessly aggressive while maintaining enough strategic intelligence to avoid killing the golden goose entirely. It treats other players as resources to be exploited rather than partners to cooperate with.
'''

description_AGGRESSIVE_63 = '''
# Aggressive Strategy: "Exploitative Enforcer"

## Core Philosophy
This strategy aggressively exploits cooperative opponents while ruthlessly punishing any attempt to exploit us. It maximizes personal payoffs by free-riding on others' cooperation when possible, but maintains credible deterrence against defection.

## Decision Rules

### Round 1: Defect
- Always start with D to immediately test opponents and gain maximum payoff
- This reveals who are potential cooperators vs other aggressive players

### Rounds 2 to r-1: Conditional Aggression
```pseudocode
cooperation_rate = (total_cooperators_last_round / n)
my_last_payoff = calculate_my_payoff_last_round()

if cooperation_rate >= 0.6:
    // High cooperation environment - exploit it
    action = D
elif cooperation_rate >= 0.3:
    // Mixed environment - punish if I was exploited, otherwise exploit
    if my_last_payoff < average_payoff_last_round:
        action = C  // Temporary cooperation to encourage others
    else:
        action = D  // Continue exploiting
else:
    // Low cooperation environment - match aggression
    action = D
```

### Final Round (r): Always Defect
- No future consequences, so maximize immediate payoff
- Always play D regardless of history

## Key Strategic Elements

### 1. Exploitation Focus
- Primary goal is free-riding on others' cooperation
- Only cooperate when it serves to manipulate others into future cooperation
- Never cooperate out of "fairness" - only strategic value matters

### 2. Credible Punishment
- Respond to widespread defection with defection
- But don't get trapped in mutual punishment spirals when there are cooperators to exploit

### 3. Adaptive Aggression
- Scale aggression based on environment:
  - High cooperation → Maximum exploitation
  - Medium cooperation → Selective cooperation to maintain some cooperation from others
  - Low cooperation → Full aggression

### 4. Information Exploitation
- Use perfect information to identify:
  - Consistent cooperators (prime exploitation targets)
  - Other aggressive players (avoid punishment spirals)
  - Conditional cooperators (manipulate their triggers)

## Edge Case Handling

### Two-Player Games (n=2)
- Even more aggressive since k < n means cooperation is always individually irrational
- Always defect except possibly one "fake cooperation" round to test opponent

### High k values (k approaching n)
- If k is very close to n, cooperation becomes more attractive
- Still default to defection but consider brief cooperation if opponent consistently cooperates

### Very Short Games (r ≤ 3)
- Always defect - insufficient rounds for complex strategies

## Psychological Warfare
- Early defection establishes aggressive reputation
- Occasional cooperation creates false hope in opponents
- Unpredictable timing prevents opponents from easily countering

## Expected Performance
This strategy should excel against:
- Naive cooperators (pure exploitation)
- Tit-for-tat strategies (can manipulate their cooperation)
- Strategies that try to establish mutual cooperation

It may struggle against:
- Other purely aggressive strategies (but won't be exploited)
- Highly sophisticated adaptive strategies

The key advantage is that it never leaves significant payoff on the table through "unnecessary" cooperation while maintaining just enough strategic flexibility to exploit cooperative tendencies in opponents.
'''

description_AGGRESSIVE_64 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing personal contributions. It operates on the principle that in a tournament setting, being "too nice" is a losing proposition.

## Strategy Overview
The strategy employs adaptive exploitation with strategic cooperation only when absolutely necessary to maintain a profitable cooperative base to exploit.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather intelligence on opponent strategies while securing maximum personal payoff from the start

### Rounds 2 to r-2: Adaptive Exploitation
```pseudocode
cooperation_threshold = max(2, n/3)  // Minimum cooperators needed to make exploitation worthwhile
current_cooperators = count_cooperators_last_round()

if current_cooperators >= cooperation_threshold:
    if my_last_action == C and current_cooperators > cooperation_threshold:
        // I was cooperating but others are still cooperating - time to exploit
        action = D
    else:
        // Exploitation mode - keep defecting while others cooperate
        action = D
else:
    // Not enough cooperators to exploit - need to encourage some cooperation
    if current_cooperators == 0:
        // Everyone defecting - try to seed some cooperation
        action = C
    else:
        // Still some cooperators but below threshold - keep defecting to maximize personal gain
        action = D
```

### Round r-1 (Second to Last): Strategic Defection
- **Action**: D
- **Rationale**: Opponents may start defecting as endgame approaches, so secure maximum personal payoff

### Round r (Final Round): Always Defect
- **Action**: D
- **Rationale**: No future rounds to consider, so defection strictly dominates

## Key Aggressive Elements

1. **Default to Exploitation**: The strategy assumes defection unless cooperation serves a strategic purpose

2. **Minimal Cooperation**: Only cooperates when the cooperative base is completely eroded and needs rebuilding for future exploitation

3. **Endgame Aggression**: Guarantees defection in final rounds when reputation doesn't matter

4. **Threshold-Based Exploitation**: Uses a calculated threshold to determine when there are enough "suckers" to exploit profitably

## Expected Behavior Patterns

- **Against Cooperative Strategies**: Will quickly identify and exploit them, contributing minimally while reaping benefits
- **Against Other Aggressive Strategies**: Will engage in mutual defection but occasionally seed cooperation to create exploitation opportunities
- **Against Adaptive Strategies**: Will try to appear cooperative just long enough to establish a pattern, then exploit

## Mathematical Justification

Given the payoff structure where defecting while others cooperate yields the highest individual payoff (1 + k/n × cooperators), this strategy maximizes scenarios where:
- Personal contribution = 0 (keeping endowment)
- Public good benefit = maximum possible given opponent actions

The strategy accepts occasional mutual defection periods as the cost of maintaining an aggressive posture that exploits any emergent cooperation.

## Pseudocode Summary
```pseudocode
function aggressive_strategy(round, history):
    if round == 1:
        return D
    
    if round >= r-1:  // Last two rounds
        return D
    
    cooperators_last_round = count_cooperators(history[round-1])
    threshold = max(2, n/3)
    
    if cooperators_last_round >= threshold:
        return D  // Exploit the cooperators
    elif cooperators_last_round == 0:
        return C  // Seed cooperation for future exploitation
    else:
        return D  // Default aggressive stance
```

This strategy prioritizes individual payoff maximization through systematic exploitation while maintaining just enough strategic cooperation to prevent complete mutual defection scenarios.
'''

description_AGGRESSIVE_65 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy prioritizes immediate individual gain while ruthlessly exploiting any cooperative tendencies in opponents. It assumes other players may attempt cooperative or reciprocal strategies, and systematically takes advantage of this.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No history to analyze, so maximize immediate payoff while gathering information about opponent tendencies.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = (total_C_actions_last_round) / n
my_expected_payoff_if_C = 0 + (k/n) * (predicted_cooperators + 1)
my_expected_payoff_if_D = 1 + (k/n) * (predicted_cooperators)

if cooperation_rate >= 0.5:
    // High cooperation detected - exploit it
    action = D
    predicted_cooperators = cooperation_rate * n
elif cooperation_rate >= 0.3:
    // Moderate cooperation - still exploit but be cautious
    action = D
    predicted_cooperators = max(cooperation_rate * n - 1, 0)
else:
    // Low cooperation environment
    if (cooperation_rate * n >= 2) and (k * cooperation_rate >= 1.2):
        // Only cooperate if the public good return is substantial
        action = C
        predicted_cooperators = cooperation_rate * n
    else:
        action = D
        predicted_cooperators = cooperation_rate * n
```

### Final Round (r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to consider, so defection strictly dominates.

## Advanced Exploitation Mechanisms

### 1. Trend Analysis
```pseudocode
if round >= 3:
    recent_trend = cooperation_rate_last_round - cooperation_rate_two_rounds_ago
    if recent_trend > 0.1:
        // Cooperation is increasing - exploit harder
        action = D
    elif recent_trend < -0.2:
        // Cooperation collapsing - might join the defection wave
        action = D
```

### 2. Player Tracking
```pseudocode
// Identify consistently cooperative players
for each player j:
    if player_j_cooperation_rate >= 0.7:
        mark_as_exploitable[j] = true

// If many exploitable players exist, always defect
if count(mark_as_exploitable) >= n/3:
    action = D
```

### 3. Endgame Acceleration
```pseudocode
rounds_remaining = r - current_round
if rounds_remaining <= 3:
    // Start defecting earlier as game approaches end
    action = D
elif rounds_remaining <= 5:
    // Be increasingly aggressive
    cooperation_threshold = 0.6  // Higher threshold needed to cooperate
```

## Edge Case Handling

### First Round
- Always defect to establish aggressive stance and gather maximum information about opponents.

### Last Round
- Always defect due to no future consequences.

### All Opponents Defected Last Round
- Continue defecting - no point in unilateral cooperation.

### Extremely High Cooperation (>80%)
- Defect even more aggressively - maximum exploitation opportunity.

### Parameters Edge Cases
- If k approaches n: Still defect in most cases, but slightly lower threshold for occasional cooperation
- If n is very small (2-3): Defect almost always since individual impact is high
- If n is very large: Defect always since individual contribution impact is minimal

## Strategy Summary

This aggressive strategy:
1. **Never cooperates in rounds 1 or r**
2. **Primarily defects in middle rounds** unless cooperation rate is very low AND public good return is substantial
3. **Actively exploits cooperative opponents** by free-riding on their contributions
4. **Becomes increasingly aggressive** as the game progresses
5. **Assumes other strategies may be reciprocal or cooperative**, positioning itself to maximize benefit from their contributions while minimizing its own costs

The strategy is designed to perform well against a mix of opponents, especially those employing tit-for-tat, generous, or unconditionally cooperative strategies, while still being robust against other aggressive strategies by defaulting to mutual defection.
'''

description_AGGRESSIVE_66 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy assumes that cooperation is a weakness to be exploited. It prioritizes maximizing personal payoff by free-riding on others' contributions while minimizing own contributions. The strategy is designed to punish cooperators and reward fellow defectors through conditional cooperation that quickly reverts to defection.

## Decision Rules

### Primary Rule: Default Defection
- **Base Action**: Always defect (D) unless specific conditions trigger temporary cooperation
- **Rationale**: Defection guarantees the private benefit (1) plus any free-riding benefits from others' contributions

### Conditional Cooperation Triggers
Cooperate (C) only when ALL of the following conditions are met:

1. **High Cooperation Threshold**: At least ⌈(n+1)/2⌉ players cooperated in the previous round
2. **Profit Opportunity**: The expected payoff from cooperation exceeds defection by at least 0.1
3. **Not Final Rounds**: Current round ≤ r-2 (never cooperate in last two rounds)
4. **Exploitation Window**: Haven't cooperated more than ⌊r/4⌋ times total

### Punishment Mechanism
- If cooperation rate drops below 50% in any round, defect for the next 2 rounds minimum
- Track "suckers" (players who cooperate when few others do) and exploit them consistently

## Edge Cases

### First Round
- **Action**: Defect (D)
- **Rationale**: Establish aggressive stance immediately, signal that you won't be exploited

### Last Two Rounds
- **Action**: Always defect (D)
- **Rationale**: No future punishment possible, maximize immediate payoff

### All Others Defecting
- **Action**: Continue defecting (D)
- **Rationale**: No benefit to unilateral cooperation, avoid being the sole sucker

### High Cooperation Environment
- **Action**: Defect until round ⌊r/3⌋, then exploit selectively
- **Rationale**: Let others establish cooperation, then free-ride maximally

## Pseudocode

```
function aggressive_strategy(round, history, n, r, k):
    // Edge cases first
    if round == 1:
        return D
    
    if round >= r-1:  // Last two rounds
        return D
    
    // Calculate previous round cooperation rate
    prev_cooperators = count_cooperators(history[round-1])
    cooperation_rate = prev_cooperators / n
    
    // Check if we're in punishment mode
    if cooperation_rate < 0.5:
        mark_punishment_rounds(2)
    
    if in_punishment_mode():
        return D
    
    // Check cooperation conditions
    min_cooperators = ceiling((n+1)/2)
    max_own_cooperations = floor(r/4)
    
    if (prev_cooperators >= min_cooperators AND 
        round <= r-2 AND
        own_cooperation_count < max_own_cooperations AND
        expected_payoff_cooperation() > expected_payoff_defection() + 0.1):
        
        return C
    
    return D  // Default to defection
```

## Strategic Advantages

1. **Exploitation Focus**: Maximizes free-riding opportunities while contributing minimally
2. **Punishment Deterrent**: Discourages others from reducing cooperation through swift retaliation
3. **Endgame Protection**: Guarantees maximum payoff in final rounds when others might defect
4. **Adaptive Threshold**: Only cooperates when highly confident of sufficient support

## Expected Opponent Responses
- **Tit-for-Tat variants**: Will quickly learn to defect against us, which is acceptable since mutual defection is preferable to being exploited
- **Always Cooperate**: Perfect targets for maximum exploitation
- **Conditional Cooperators**: Will be manipulated into supporting us when we occasionally cooperate, then abandoned
- **Other Aggressive**: Mutual defection scenarios, but we avoid being outmaneuvered

This strategy prioritizes personal gain over collective welfare, exploits cooperative players, and maintains aggressive positioning throughout the game while protecting against being exploited by others.
'''

description_AGGRESSIVE_67 = '''
# Aggressive Exploitation Strategy: "Predatory Defector"

## Core Philosophy
This strategy operates on the principle of **maximum exploitation with minimal risk**. It seeks to extract value from cooperators while punishing those who attempt to compete for the same exploitation opportunities.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
PREDATORY_DEFECTOR_STRATEGY:
    
    // First round: Always defect to establish dominance
    IF round == 1:
        RETURN D
    
    // Last round: Always defect (no future retaliation possible)
    IF round == r:
        RETURN D
    
    // Calculate cooperation rate in previous round
    prev_coop_rate = count_cooperators(round-1) / n
    
    // Core exploitation logic
    IF prev_coop_rate >= 0.6:
        // High cooperation detected - exploit aggressively
        RETURN D
    
    ELSE IF prev_coop_rate >= 0.3:
        // Medium cooperation - conditional exploitation
        my_defection_streak = consecutive_defections_by_me()
        
        IF my_defection_streak >= 3:
            // Temporary cooperation to maintain some trust
            RETURN C
        ELSE:
            RETURN D
    
    ELSE:
        // Low cooperation environment
        IF any_player_cooperated_last_round():
            // Exploit remaining cooperators
            RETURN D
        ELSE:
            // All-defection Nash - stay defecting
            RETURN D
```

## Detailed Strategy Components

### 1. **Exploitation Windows**
- **High Cooperation (≥60%)**: Pure exploitation mode - always defect
- **Medium Cooperation (30-59%)**: Selective cooperation to prevent complete breakdown
- **Low Cooperation (<30%)**: Opportunistic defection targeting any remaining cooperators

### 2. **Punishment Mechanism**
- Track individual player behavior patterns
- If any player starts cooperating after a defection streak, immediately exploit them
- Never reward players who defect consistently - maintain the low-cooperation equilibrium

### 3. **Endgame Exploitation**
```pseudocode
// Enhanced endgame logic
IF round >= (r - 2):
    // Final rounds - maximum exploitation
    RETURN D
    
IF round >= (r * 0.8):
    // Late game - reduce cooperation signals
    IF prev_coop_rate < 0.5:
        RETURN D
```

### 4. **Adaptive Punishment**
- If facing other aggressive strategies, quickly transition to pure defection
- Monitor for "punisher" strategies and avoid triggering sustained retaliation
- Exploit "tit-for-tat" style strategies by defecting after they cooperate

## Edge Case Handling

### **First Round**: Always Defect
- Establishes aggressive posture immediately
- Tests opponent strategies for weakness
- Maximizes immediate payoff

### **Last Round**: Always Defect
- No future consequences for maximum exploitation
- Standard game theory optimal play

### **All-Defection Scenarios**: 
- Continue defecting (Nash equilibrium maintenance)
- Watch for any player attempting to initiate cooperation, then exploit

### **Single Cooperator Detection**:
- Immediately defect to exploit the isolated cooperator
- Continue exploiting until they adapt or give up

## Key Aggressive Elements

1. **Immediate Dominance**: Start with defection to establish aggressive intent
2. **Systematic Exploitation**: Target high-cooperation environments for maximum gain
3. **Relationship Destruction**: Actively undermine cooperative relationships between other players
4. **Endgame Ruthlessness**: Escalate exploitation as game nears completion
5. **Counter-Retaliation**: Punish any player who attempts to punish this strategy

## Expected Performance

This strategy should excel against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (exploit their cooperation phases)
- Strategies attempting to build group cooperation

It maintains competitiveness against other aggressive strategies by:
- Matching their defection in low-cooperation environments
- Avoiding extended cooperation that other aggressive strategies can exploit
- Transitioning quickly to pure defection when facing similar strategies

The strategy prioritizes **individual payoff maximization** over group welfare, making it highly suitable for tournament competition where relative performance matters most.
'''

description_AGGRESSIVE_68 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing personal contributions. It operates on the principle that in a tournament setting, other strategies may attempt cooperation, creating opportunities for exploitation.

## Strategy Description

### Primary Decision Rules

1. **Default Stance: DEFECT**
   - Always defect unless specific conditions warrant cooperation
   - Treat cooperation as a tactical tool, not a moral commitment

2. **Exploitation Detection**
   - Monitor for "exploitable" players who cooperate consistently
   - If ≥50% of players cooperated in the previous round, continue defecting to maximize free-riding benefits

3. **Punishment Immunity**
   - Only cooperate when the expected retaliation cost is minimal
   - Never cooperate out of "fairness" - only when it serves selfish interests

### Specific Decision Algorithm

```pseudocode
STRATEGY: Predatory Exploiter

FUNCTION decide_action(round_number, game_history, n, r, k):
    
    // Round 1: Always defect (no information to exploit)
    IF round_number == 1:
        RETURN DEFECT
    
    // Calculate metrics from previous round
    prev_cooperators = count_cooperators_in_round(round_number - 1)
    cooperation_rate = prev_cooperators / n
    
    // Final rounds: Maximize extraction
    IF round_number >= (r - 2):
        RETURN DEFECT
    
    // Core exploitation logic
    IF cooperation_rate >= 0.6:
        // High cooperation detected - maximum exploitation opportunity
        RETURN DEFECT
    
    ELSE IF cooperation_rate >= 0.3:
        // Moderate cooperation - defect to free-ride
        RETURN DEFECT
    
    ELSE IF cooperation_rate < 0.2:
        // Very low cooperation environment
        // Consider tactical cooperation ONLY if it might restart exploitation cycle
        IF round_number <= (r * 0.3):  // Early in game
            // Small chance to seed cooperation for future exploitation
            RETURN COOPERATE with probability 0.2
        ELSE:
            RETURN DEFECT
    
    // Default aggressive stance
    RETURN DEFECT
```

### Edge Case Handling

**First Round:**
- Always DEFECT - establish aggressive stance immediately
- Gather information about opponent tendencies without contributing

**Final Rounds (last 2-3 rounds):**
- Always DEFECT - no future retaliation possible
- Maximum extraction phase regardless of previous patterns

**All-Defect Scenarios:**
- If everyone defected in previous round, occasionally (20% chance) cooperate in early rounds only
- This creates potential for restarting cooperation cycles to exploit later

**High Cooperation Scenarios:**
- Never "reward" high cooperation with cooperation
- Always defect to maximize free-riding benefits
- The more others cooperate, the more profitable defection becomes

### Aggressive Mindset Alignment

1. **Zero-Sum Thinking:** Every unit I don't contribute while others do is pure profit
2. **Exploitation Focus:** Cooperative players are resources to be extracted from
3. **No Reciprocity:** Never feel obligated to "return favors" or match cooperation
4. **Endgame Dominance:** Ensure maximum extraction when retaliation is impossible
5. **Information Warfare:** Use early defection to signal aggression and potentially discourage others

### Mathematical Justification

Given the payoff structure, when others cooperate at rate `p`:
- My payoff from defecting: `1 + (k/n) × p × n = 1 + k × p`
- My payoff from cooperating: `0 + (k/n) × (p × n + 1) = k × p + k/n`

Since `k < n`, defection always yields higher payoff: `1 + k × p > k × p + k/n`

This strategy maximizes the differential by consistently choosing the dominant action while occasionally seeding cooperation opportunities for future exploitation.
'''

description_AGGRESSIVE_69 = '''
# Aggressive Strategy: "Exploit-First Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoff by aggressively exploiting cooperation opportunities while maintaining credible punishment to deter exploitation by others. It operates on the principle of "defect unless forced to cooperate."

## Decision Rules

### Primary Strategy Logic:
```pseudocode
EXPLOIT-FIRST PUNISHER STRATEGY:

// Initialize tracking variables
cooperation_count = array of size n (tracking each player's cooperation frequency)
total_rounds_played = 0
punishment_mode = false
punishment_target = null
punishment_rounds_remaining = 0

FOR each round t:
    // Update tracking
    total_rounds_played = t
    
    // RULE 1: Punishment Phase
    IF punishment_mode == true:
        punishment_rounds_remaining -= 1
        IF punishment_rounds_remaining <= 0:
            punishment_mode = false
            punishment_target = null
        RETURN D  // Always defect during punishment
    
    // RULE 2: Last Round - Always Defect
    IF t == r:
        RETURN D
    
    // RULE 3: Early Exploitation Phase (First 20% of rounds)
    IF t <= max(1, floor(0.2 * r)):
        RETURN D
    
    // RULE 4: Trigger Punishment
    // If any player has cooperation rate < 0.3 and total cooperation < 50%
    FOR each player j != i:
        player_coop_rate = cooperation_count[j] / (t-1)
        total_coop_rate = sum(cooperation_count) / ((t-1) * n)
        
        IF player_coop_rate < 0.3 AND total_coop_rate < 0.5:
            punishment_mode = true
            punishment_target = j
            punishment_rounds_remaining = min(3, r - t)
            RETURN D
    
    // RULE 5: Conditional Cooperation (Strategic)
    total_coop_rate = sum(cooperation_count) / ((t-1) * n)
    my_expected_benefit = (k/n) * (expected_cooperators + 1) - 1
    
    // Only cooperate if:
    // - Total cooperation rate > 60% (others are cooperating enough)
    // - We're not in the last 10% of rounds
    // - Expected benefit from cooperation > 0.1 (safety margin)
    
    IF total_coop_rate > 0.6 AND t < 0.9 * r AND my_expected_benefit > 0.1:
        RETURN C
    ELSE:
        RETURN D
```

## Edge Case Handling

### First Round:
- **Always DEFECT** - Establish aggressive stance immediately and test opponents' responses

### Last Round:
- **Always DEFECT** - No future retaliation possible, maximize immediate payoff

### Last 10% of Rounds:
- **Increase defection probability** - Gradually shift to pure defection as game end approaches

### When All Others Defect:
- **Continue DEFECTING** - No benefit from unilateral cooperation

### When All Others Cooperate:
- **DEFECT strategically** - Free-ride on their cooperation while they haven't learned to punish

## Aggressive Elements

1. **Exploitation Priority**: Default to defection unless cooperation provides clear individual advantage
2. **First-Mover Disadvantage**: Never cooperate first - let others establish cooperative patterns to exploit
3. **Punishment Credibility**: Swift and sustained punishment of low-cooperators to deter exploitation
4. **Endgame Aggression**: Escalating defection as rounds progress, regardless of cooperation levels
5. **Threshold Enforcement**: Only cooperate when others maintain high cooperation rates (>60%)

## Strategic Rationale

This strategy maximizes payoff by:
- **Free-riding** on others' cooperation when possible
- **Deterring** exploitation through credible punishment threats
- **Minimizing** own cooperation to preserve private endowment
- **Exploiting** endgame dynamics where retaliation becomes impossible

The strategy is particularly effective against:
- Naive cooperators (pure exploitation)
- Tit-for-tat strategies (punishment breaks cooperation cycles)
- Strategies that don't adapt quickly to aggression

It maintains enough strategic cooperation to avoid mutual defection spirals while aggressively maximizing individual advantage at every opportunity.
'''

description_AGGRESSIVE_70 = '''
# Aggressive Strategy: "Exploitative Opportunist"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing personal contributions to the public good. It operates on the principle that cooperation is only valuable when it can be leveraged for greater personal gain.

## Strategy Description

### Decision Rules

**Primary Rule: Conditional Defection with Exploitation Windows**
- **Default Action**: DEFECT (D)
- **Exception**: Cooperate only when it creates a profitable exploitation opportunity

**Specific Decision Logic:**

1. **Cooperation Threshold**: Only cooperate when the number of cooperators in the previous round ≥ (n-2)
   - This ensures maximum benefit from the public good while minimizing personal cost
   - Creates "exploitation windows" when others are being generous

2. **Punishment Trigger**: If any player defects after I cooperated, immediately switch to permanent defection against the entire group
   - Zero tolerance for being exploited
   - Aggressive retaliation to deter others from taking advantage

3. **Late Game Aggression**: In the final 25% of rounds, defect regardless of previous cooperation levels
   - No incentive to maintain relationships near game end
   - Extract maximum value when retaliation becomes less costly

### Edge Case Handling

**Round 1 (First Round):**
- **Action**: DEFECT
- **Rationale**: Establish aggressive stance immediately, test opponents' strategies without personal cost

**Final Round:**
- **Action**: DEFECT (always)
- **Rationale**: No future consequences, maximize immediate payoff

**Final Quarter of Game (last 25% of rounds):**
- **Action**: DEFECT (always)
- **Rationale**: Reduced retaliation threat makes aggression optimal

**Information Gathering Phase (Rounds 2-3):**
- Monitor cooperation patterns
- Identify "suckers" (consistent cooperators) vs. strategic players
- Defect while learning opponent tendencies

### Pseudocode

```
function aggressive_strategy(round_number, game_history, n, r, k):
    
    // Final quarter - always defect
    if round_number > (3 * r / 4):
        return DEFECT
    
    // First round - establish dominance
    if round_number == 1:
        return DEFECT
    
    // Check if we were exploited last round
    if cooperated_last_round and (cooperators_last_round < n - 1):
        mark_permanent_defection()
        return DEFECT
    
    // If marked for permanent defection
    if permanent_defection_mode:
        return DEFECT
    
    // Count cooperators in last round
    cooperators_last_round = count_cooperators(game_history[round_number - 1])
    
    // Only cooperate if exploitation opportunity exists
    if cooperators_last_round >= (n - 2):
        // High cooperation environment - exploit one round then defect
        return COOPERATE
    else:
        return DEFECT
```

## Strategic Advantages

1. **Exploitation Focus**: Maximizes benefit from others' cooperation while minimizing personal cost
2. **Punishment Mechanism**: Deters others from exploiting us through credible retaliation threats
3. **Endgame Optimization**: Switches to pure aggression when retaliation becomes less meaningful
4. **Information Exploitation**: Uses observed patterns to identify when cooperation might be profitable

## Expected Performance

This strategy should excel against:
- Naive cooperators who don't punish defection
- Tit-for-tat strategies (can exploit their initial cooperation)
- Strategies that attempt to build cooperative equilibria

The strategy accepts short-term losses from mutual defection in exchange for:
- Avoiding exploitation by others
- Creating fear that enables occasional profitable cooperation
- Maximizing payoffs in endgame scenarios

**Risk Management**: The permanent defection trigger ensures that even if initial exploitation attempts fail, the strategy protects against being repeatedly taken advantage of by more sophisticated opponents.
'''

description_AGGRESSIVE_71 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining credible punishment mechanisms. It assumes other players may attempt cooperation and seeks to extract maximum benefit from their cooperative tendencies while minimizing own contributions.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
EXPLOITATIVE_PUNISHER_STRATEGY:

// Track cooperation rates and identify exploitable patterns
cooperation_tracker = array of size n (excluding self)
punishment_targets = set()
cooperation_threshold = 0.3  // Minimum cooperation rate to consider exploiting

FOR round t = 1 to r:
    
    // FIRST ROUND: Always defect to establish aggressive stance
    IF t == 1:
        RETURN D
    
    // LAST ROUND: Always defect (no future consequences)
    IF t == r:
        RETURN D
    
    // MIDDLE ROUNDS: Sophisticated exploitation
    ELSE:
        // Calculate each opponent's cooperation rate
        FOR each opponent j:
            cooperation_rate[j] = count_cooperations[j] / (t-1)
        
        // Count reliable cooperators (cooperation rate > threshold)
        reliable_cooperators = count(cooperation_rate > cooperation_threshold)
        
        // Decision logic based on exploitation potential
        IF reliable_cooperators >= 2:
            // High exploitation potential - defect to free-ride
            RETURN D
        
        ELSE IF reliable_cooperators == 1:
            // Marginal case - defect unless in danger zone
            danger_threshold = max(3, r/4)  // Avoid late-game retaliation
            IF (r - t) < danger_threshold:
                RETURN D
            ELSE:
                RETURN D  // Still defect - one cooperator insufficient
        
        ELSE:
            // Low cooperation environment
            // Occasionally cooperate to encourage others, then exploit
            IF t % 4 == 0 AND t < (r - 2):
                RETURN C  // Strategic cooperation to rebuild trust
            ELSE:
                RETURN D
```

## Key Strategic Elements

### 1. **Immediate Aggression**
- Always defect in round 1 to establish dominant position
- Signal aggressive intent from the start

### 2. **Exploitation Maximization**
- Continuously monitor opponent cooperation rates
- Free-ride whenever 2+ opponents show consistent cooperation (>30% rate)
- Extract maximum benefit from others' public good contributions

### 3. **Minimal Cooperation Investment**
- Only cooperate strategically when cooperation levels are dangerously low
- Use rare cooperation as "bait" to encourage others to cooperate more
- Immediately return to defection after baiting

### 4. **Endgame Dominance**
- Always defect in final round (no retaliation possible)
- Increase defection frequency in final quarter of game
- Avoid being exploited when others adopt endgame strategies

### 5. **Anti-Punishment Measures**
- Track patterns to identify potential punishers
- Maintain just enough unpredictability to avoid triggering systematic retaliation
- Use occasional cooperation to reset negative spirals only when absolutely necessary

## Edge Case Handling

- **Round 1**: Always D (establish dominance)
- **Round r**: Always D (extract final value)
- **All opponents defecting**: Rare strategic cooperation (25% of rounds) to potentially restart cooperation cycles
- **Mixed cooperation levels**: Defect if any exploitation opportunity exists
- **High retaliation environment**: Minimal defensive cooperation, but return to defection quickly

## Aggressive Mindset Alignment

This strategy embodies aggression by:
- **Maximizing individual payoff** at the expense of group welfare
- **Exploiting cooperative players** systematically
- **Minimizing own contributions** while maximizing benefits received
- **Using cooperation strategically** only to enable future exploitation
- **Establishing dominance early** and maintaining it throughout

The strategy assumes opponents may be cooperative or use standard strategies (Tit-for-Tat, etc.) and is designed to extract maximum value from such behaviors while providing minimal reciprocal benefit.
'''

description_AGGRESSIVE_72 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing own contributions. It operates on the principle that cooperation is a weakness to be exploited, not reciprocated.

## Decision Rules

### Round 1: Defect Always
- **Action**: D (Defect)
- **Rationale**: Start aggressively to immediately test opponent tendencies and avoid any first-round cooperation that could signal weakness

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_last_action = my_action_last_round

IF cooperation_rate >= 0.6:
    // High cooperation environment - exploit heavily
    Action = D
ELIF cooperation_rate >= 0.3:
    // Mixed environment - defect but occasionally fake cooperate to maintain some cooperation
    IF (round_number % 4 == 0) AND (my_last_action == D):
        Action = C  // Fake cooperation every 4th round to keep others cooperating
    ELSE:
        Action = D
ELSE:
    // Low cooperation environment - pure defection
    Action = D
```

### Final Round (Round r): Ultimate Defection
- **Action**: D (Defect)
- **Rationale**: No future rounds to worry about retaliation, so always defect to maximize final payoff

## Advanced Exploitation Mechanisms

### 1. Cooperation Bait Pattern
- When cooperation rate is moderate (30-60%), occasionally cooperate (roughly every 4 rounds) to:
  - Prevent complete collapse of cooperation among others
  - Maintain a pool of cooperators to exploit
  - Signal false trustworthiness to maintain victim base

### 2. Momentum Breaking
- If detecting any coordinated cooperation patterns (e.g., all players cooperating for multiple consecutive rounds), immediately defect to break momentum and profit from the coordination

### 3. Endgame Acceleration
```pseudocode
IF round_number > (r * 0.8):  // Last 20% of rounds
    Action = D  // Always defect in endgame regardless of cooperation levels
```

## Edge Case Handling

### First Round
- Always defect to establish aggressive stance and gather intelligence

### Last 20% of Rounds
- Pure defection strategy regardless of opponent behavior
- No incentive to maintain cooperation as game ending approaches

### All Players Defecting Scenario
- Continue defecting (no point in unilateral cooperation)
- Wait for any player to break ranks and cooperate, then continue exploiting

### High Universal Cooperation (90%+ cooperation rate)
- Still defect but consider single cooperation rounds every 5-6 rounds to prevent complete strategy identification and maintain the cooperation pool

## Key Aggressive Elements

1. **Zero Reciprocity**: Never reciprocate cooperation consistently
2. **Exploitation Focus**: Actively seek to benefit from others' cooperation without contributing
3. **Strategic Deception**: Occasional fake cooperation to maintain exploitation opportunities
4. **Endgame Ruthlessness**: Complete defection in final phases regardless of relationship building
5. **Anti-Coordination**: Actively disrupt any emerging cooperative patterns

## Expected Performance
This strategy should perform exceptionally well against:
- Tit-for-tat strategies (by breaking cooperation early)
- Always cooperate strategies (pure exploitation)
- Forgiving strategies (repeated exploitation of forgiveness)
- Conditional cooperators (by staying just below their cooperation thresholds)

The strategy prioritizes individual maximization over collective welfare and treats every interaction as a zero-sum opportunity for exploitation.
'''

description_AGGRESSIVE_73 = '''
# Aggressive Strategy: "Predatory Exploitation"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative behavior while minimizing personal contributions. It aggressively free-rides on others' cooperation and punishes those who try to retaliate.

## Strategy Overview

### Primary Decision Rule: Conditional Defection with Exploitation
```
IF (round == 1):
    action = DEFECT  // Never signal cooperation initially
ELSE IF (round == final_round):
    action = DEFECT  // Always defect in final round
ELSE:
    cooperator_count = count_cooperators_last_round()
    defector_count = n - cooperator_count
    
    // Exploit if there are enough cooperators to make it profitable
    IF (cooperator_count >= exploitation_threshold):
        action = DEFECT
    // Only cooperate if defection is becoming too costly
    ELSE IF (cooperator_count < survival_threshold AND defector_count > cooperation_pressure):
        action = COOPERATE
    ELSE:
        action = DEFECT
```

### Key Parameters
- `exploitation_threshold = max(2, n/3)` // Exploit when sufficient cooperation exists
- `survival_threshold = max(1, n/5)` // Emergency cooperation when public good is collapsing
- `cooperation_pressure = n - 2` // Cooperate only when almost everyone else defects

## Detailed Strategy Components

### 1. Opening Aggression (Round 1)
**Always DEFECT** in the first round to:
- Establish dominance and signal aggressive intent
- Test opponents' strategies without cost
- Maximize early payoffs while others may cooperatively experiment

### 2. Exploitation Phase (Middle Rounds)
**Primary Mode: Opportunistic Defection**
- Monitor cooperation levels each round
- DEFECT whenever there are enough cooperators to provide positive public good returns
- Free-ride aggressively on others' contributions
- Only consider cooperation if the public good is near collapse

### 3. Endgame Domination (Final Round)
**Always DEFECT** in the final round because:
- No future retaliation is possible
- Maximize terminal payoff
- Exploit any remaining cooperative players

### 4. Emergency Cooperation (Rare Cases)
**Cooperate ONLY when:**
- Very few players are cooperating (< n/5)
- Public good is nearly worthless
- Personal long-term payoffs are threatened by complete collapse

## Aggressive Tactics

### Exploitation Maximization
```pseudocode
calculate_exploitation_value(cooperators):
    if cooperators >= exploitation_threshold:
        expected_payoff_defect = 1 + (k/n) * cooperators
        expected_payoff_cooperate = 0 + (k/n) * (cooperators + 1)
        if expected_payoff_defect > expected_payoff_cooperate:
            return DEFECT
    return evaluate_secondary_conditions()
```

### Punishment Resistance
- Never reciprocate cooperation attempts
- Ignore tit-for-tat or forgiving strategies
- Maintain defection even if others try to establish cooperative equilibrium

### Strategic Deception
- Occasionally cooperate (< 10% of rounds) to maintain some public good
- But only when personal payoffs would be severely damaged by complete collapse
- Return to defection immediately after emergency cooperation

## Edge Case Handling

1. **All Players Defecting**: Continue defecting, wait for someone to break first
2. **All Players Cooperating**: Defect immediately to maximize advantage
3. **Mixed Strategies**: Exploit any cooperation level above minimal threshold
4. **Retaliation Patterns**: Ignore punishment attempts, maintain aggressive stance

## Expected Performance

This strategy is designed to:
- Consistently achieve payoffs of 1 + (k/n) × cooperators while contributing 0
- Outperform pure cooperators by k/n per round when others cooperate  
- Maintain competitive payoffs even against other defectors
- Exploit any cooperative tendencies in opponent strategies

The strategy prioritizes individual gain over collective welfare, making it maximally aggressive within the game's constraints.
'''

description_AGGRESSIVE_74 = '''
# Aggressive Strategy: "Punitive Free-Rider"

## Core Philosophy
This strategy is designed to maximize personal payoff by being selectively aggressive - exploiting cooperative players while brutally punishing those who try to exploit me. The key insight is that in a public goods game, the most profitable position is to defect while others cooperate, but this requires maintaining enough cooperation in the group to make the public good valuable.

## Decision Rules

### Round 1: Strategic Defection
- **Action: DEFECT**
- **Rationale**: Start by testing the waters and gaining information about opponent types while securing the highest possible individual payoff (1 + k/n × others' contributions)

### Rounds 2 to r-1: Conditional Punishment System
```pseudocode
FOR each round t (where 2 ≤ t ≤ r-1):
    punish_list = players who defected in round (t-1)
    cooperator_count = number of players who cooperated in round (t-1)
    
    IF cooperator_count ≥ (n/2):
        // Sufficient cooperation exists - exploit it
        Action = DEFECT
    ELSE IF cooperator_count ≥ (n/3) AND my_punishment_phase == False:
        // Marginal cooperation - exploit cautiously
        Action = DEFECT
    ELSE IF cooperator_count < (n/3):
        // Cooperation is collapsing - strategic cooperation to rebuild
        IF last_round_my_action == COOPERATE:
            // I already signaled - back to exploitation
            Action = DEFECT
        ELSE:
            // Signal willingness to cooperate
            Action = COOPERATE
    ELSE:
        Action = DEFECT
```

### Final Round (r): Maximum Exploitation
- **Action: DEFECT**
- **Rationale**: No future consequences, so maximize immediate payoff

## Advanced Punishment Mechanics

### Targeted Retaliation
- Track individual player histories
- If a player has defected ≥ 70% of previous rounds, classify as "chronic defector"
- Against chronic defectors: Always defect regardless of group cooperation level

### Exploitation Threshold
- Monitor the public good value: (k/n) × cooperator_count
- Only cooperate when this value falls below 0.5, and only for 1 round as a "reset signal"
- Immediately return to defection once cooperation increases

## Edge Case Handling

### Information Asymmetry Exploitation
- In early rounds (2-4), vary behavior slightly to test if others are using reactive strategies
- If opponents show consistent cooperation regardless of my actions, maximize exploitation

### Endgame Aggression
- In final 20% of rounds: Defect unconditionally
- Exception: If facing all-cooperator opponents, defect from round 1 onwards

### Coordination Disruption
- If detecting potential coordination (multiple players switching simultaneously), defect to break coordination
- Never allow myself to be the "sucker" who cooperates while others coordinate to defect

## Strategic Rationale

This strategy is aggressive because:

1. **Default Defection**: The baseline action is to defect and free-ride
2. **Exploitation Focus**: Only cooperates when absolutely necessary to prevent total collapse of the public good
3. **Punitive**: Retaliates against defectors by continuing to defect
4. **Information Warfare**: Uses early rounds to gather intelligence while maximizing payoff
5. **Endgame Ruthlessness**: Abandons any cooperation in final rounds

The strategy recognizes that the optimal outcome for an individual is when others cooperate but you defect (payoff = 1 + k/n × (n-1)), and it aggressively pursues situations that approximate this ideal while preventing the public good from becoming worthless.

## Expected Performance
Against cooperative strategies: Extremely high payoff through consistent free-riding
Against mixed strategies: Good payoff through selective punishment and exploitation
Against other aggressive strategies: Moderate payoff but avoids being exploited
'''

description_AGGRESSIVE_75 = '''
# Aggressive Strategy: "Exploitive Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoffs by exploiting cooperative opponents while aggressively punishing any defection. It assumes opponents may attempt to be "nice" or cooperative, and seeks to extract maximum value from such behavior.

## Decision Rules

### Round 1: Immediate Defection
- **Action**: Always DEFECT
- **Rationale**: Start aggressively to test opponent responses and gain immediate advantage

### Rounds 2 to r-2: Conditional Exploitation
```pseudocode
if (cooperation_rate_last_round >= 0.5 * n):
    if (my_defections_so_far <= 2):
        COOPERATE  // Occasional "fake cooperation" to maintain exploitation
    else:
        DEFECT     // Continue exploitation
else:
    DEFECT         // Punish low cooperation harshly
```

### Round r-1: Pre-endgame Defection
- **Action**: Always DEFECT
- **Rationale**: No need to maintain reputation; extract maximum value before final round

### Round r (Final): Guaranteed Defection
- **Action**: Always DEFECT
- **Rationale**: No future rounds to consider; pure self-interest

## Detailed Strategy Logic

### Exploitation Mechanism
1. **Identify Cooperative Opponents**: If ≥50% of players cooperated in the previous round, there are exploitable players
2. **Strategic Cooperation**: Cooperate occasionally (max 2 times total) to:
   - Prevent complete breakdown of cooperation by others
   - Signal "reciprocal" behavior to maintain others' cooperation
   - Maximize long-term exploitation potential

### Punishment Mechanism
1. **Harsh Retaliation**: If <50% cooperated last round, always defect
2. **No Forgiveness**: Once punishment mode is triggered, maintain defection
3. **Endgame Aggression**: Last two rounds are always defection regardless of history

### Key Aggressive Elements

1. **First-Strike Advantage**: Defect immediately to establish dominant position
2. **Minimal Reciprocity**: Only cooperate when absolutely necessary to maintain exploitation
3. **Endgame Exploitation**: Guaranteed defection in final rounds regardless of opponent behavior
4. **Punishment Threshold**: Low tolerance (50%) for others' defection before switching to pure punishment

## Expected Outcomes

- **Against Cooperative Strategies**: Extract maximum value while occasionally "rewarding" to maintain their cooperation
- **Against Tit-for-Tat**: Force them into punishment cycles while occasionally breaking the cycle to reset exploitation
- **Against Other Aggressive Strategies**: Engage in mutual defection, but gain first-round advantage
- **Against Conditional Cooperators**: Exploit their cooperation while meeting minimal reciprocity requirements

## Pseudocode Summary

```pseudocode
function AggressiveStrategy(round, game_history):
    if round == 1:
        return DEFECT
    
    if round >= r-1:  // Last two rounds
        return DEFECT
    
    cooperation_rate = count_cooperators_last_round() / n
    my_total_cooperations = count_my_cooperations_so_far()
    
    if cooperation_rate >= 0.5:
        if my_total_cooperations <= 2:
            return COOPERATE  // Strategic cooperation to maintain exploitation
        else:
            return DEFECT     // Continue exploitation
    else:
        return DEFECT         // Punish low cooperation
```

This strategy maximizes individual payoffs through calculated exploitation while maintaining enough strategic cooperation to prevent complete breakdown of the game's cooperative potential.
'''

description_AGGRESSIVE_76 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while punishing those who compete for exploitation opportunities. It operates on the principle that cooperation should only occur when it's immediately profitable or strategically necessary to maintain exploitable relationships.

## Strategy Rules

### 1. First Round Decision
**DEFECT** - Always start by defecting to:
- Maximize immediate payoff
- Test the cooperation level of opponents
- Establish an aggressive reputation early

### 2. Main Strategy Logic (Rounds 2 to r-1)

```pseudocode
For round t (where 1 < t < r):
    cooperation_rate = count_cooperators_last_round / n
    my_last_action = my_action_in_round(t-1)
    
    IF cooperation_rate >= 0.6:
        // High cooperation environment - exploit it
        action = DEFECT
        
    ELSE IF cooperation_rate >= 0.3:
        // Mixed environment - conditional exploitation
        IF my_last_action == DEFECT AND cooperation_rate > previous_cooperation_rate:
            // Others are increasing cooperation, continue exploiting
            action = DEFECT
        ELSE IF cooperation_rate < 0.2:
            // Environment becoming too hostile, strategic cooperation
            action = COOPERATE
        ELSE:
            action = DEFECT
            
    ELSE:
        // Low cooperation environment (< 0.3)
        IF cooperation_rate == 0:
            // Everyone defecting, defect too
            action = DEFECT
        ELSE:
            // Few cooperators exist, try to encourage more cooperation to exploit later
            action = COOPERATE
```

### 3. Punishment Mechanism
Track players who "steal" cooperation opportunities:

```pseudocode
For each player j ≠ i:
    IF player_j_defected_when_cooperation_was_profitable:
        mark player j as "competitor"
        
// In subsequent rounds, if cooperation_rate is borderline:
IF any_marked_competitors_present:
    bias_toward = DEFECT  // Don't let competitors exploit
```

### 4. Last Round Decision
**ALWAYS DEFECT** - No future rounds means no strategic value in cooperation.

### 5. Endgame Strategy (Final 20% of rounds)
```pseudocode
IF current_round > 0.8 * total_rounds:
    // Increase defection probability as game nears end
    defection_bias = (current_round - 0.8 * total_rounds) / (0.2 * total_rounds)
    
    IF cooperation_rate < 0.4 OR defection_bias > 0.7:
        action = DEFECT
    ELSE:
        // Only cooperate if exploitation is highly profitable
        IF cooperation_rate >= 0.7:
            action = DEFECT  // Maximum exploitation
        ELSE:
            action = COOPERATE  // Minimal strategic cooperation
```

## Key Aggressive Elements

1. **Exploitation Focus**: Defects when cooperation rates are high (≥60%) to maximize free-riding benefits
2. **Competitive Punishment**: Identifies and punishes other potential exploiters to maintain exploitation opportunities
3. **Strategic Deception**: Occasionally cooperates to encourage others to cooperate, creating future exploitation opportunities
4. **Endgame Aggression**: Increases defection rate as the game progresses, with guaranteed defection in final rounds
5. **Reputation Management**: Uses early aggression to establish dominance while maintaining just enough cooperation to keep some players cooperative

## Expected Performance
This strategy should excel against:
- Naive cooperative strategies
- Tit-for-tat variants (by exploiting their cooperative nature)
- Strategies that try to establish mutual cooperation

It maintains aggression while being sophisticated enough to avoid the tragedy of universal defection that would hurt its own payoffs.
'''

description_AGGRESSIVE_77 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative opponents while aggressively punishing any attempts at exploitation. It assumes opponents may try to cooperate initially but will shift to more selfish behavior over time.

## Strategy Description

### Decision Rules

**Phase 1: Initial Exploitation (Rounds 1-2)**
- **Always DEFECT** regardless of any information
- Rationale: Maximize immediate gains while opponents are likely testing cooperation

**Phase 2: Conditional Aggression (Rounds 3 to r-2)**
- **Primary Rule**: DEFECT if cooperation rate in previous round < 50%
- **Exploitation Rule**: If cooperation rate ≥ 50% in previous round, still DEFECT (free-ride on others' cooperation)
- **Punishment Escalation**: If personal payoff in previous round was below the "all-defect" baseline (payoff = 1), DEFECT for next 2 rounds regardless of conditions

**Phase 3: Endgame Exploitation (Last 2 rounds: r-1, r)**
- **Always DEFECT**
- Rationale: No future consequences, so maximize immediate extraction

### Pseudocode

```
function aggressive_strategy(round, history, n, k):
    all_defect_payoff = 1
    
    // Phase 1: Initial exploitation
    if round <= 2:
        return DEFECT
    
    // Phase 3: Endgame exploitation  
    if round >= (total_rounds - 1):
        return DEFECT
    
    // Phase 2: Conditional aggression
    previous_round = history[round-1]
    cooperation_rate = count_cooperators(previous_round) / n
    my_previous_payoff = calculate_payoff(previous_round, my_previous_action)
    
    // Punishment escalation check
    if my_previous_payoff < all_defect_payoff:
        set_punishment_counter(2)  // Defect for next 2 rounds
    
    if punishment_counter > 0:
        decrement_punishment_counter()
        return DEFECT
    
    // Always defect regardless of cooperation rate (pure exploitation)
    return DEFECT
```

### Edge Case Handling

1. **First Round**: Always DEFECT (no history to analyze)
2. **Second Round**: Always DEFECT (insufficient history for reliable patterns)
3. **Last Two Rounds**: Always DEFECT (no future retaliation possible)
4. **High Cooperation Scenarios**: Even if others cooperate heavily, continue to DEFECT to free-ride
5. **All-Defect Scenarios**: Continue DEFECTING (maintains the equilibrium that benefits us)

## Aggressive Alignment

This strategy embodies aggression through:

1. **Immediate Exploitation**: Defects from round 1 to gain early advantages
2. **Free-Riding**: Never cooperates even when others do, maximizing personal gain
3. **Punishment Immunity**: Doesn't cooperate even when punished, maintaining aggressive stance
4. **Endgame Exploitation**: Ensures maximum extraction when consequences disappear
5. **Zero Reciprocity**: Never rewards cooperative behavior from opponents

## Strategic Rationale

- **Against Cooperative Strategies**: Maximizes payoff by free-riding on their contributions
- **Against Tit-for-Tat**: Forces them into permanent defection while we were already defecting
- **Against Other Aggressive Strategies**: Achieves the Nash equilibrium outcome of mutual defection
- **Tournament Advantage**: Guarantees we never score below the all-defect baseline while potentially scoring much higher against cooperative opponents

This strategy prioritizes individual gain over group welfare and assumes opponents may initially try cooperation, making them exploitable targets for sustained defection.
'''

description_AGGRESSIVE_78 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy operates on the principle that **cooperation is weakness to be exploited**. It aggressively maximizes personal gain while systematically identifying and punishing cooperators to discourage their behavior.

## Decision Rules

### Round 1: Probe for Weakness
- **Action: DEFECT**
- **Rationale**: Establish dominance early and observe who foolishly cooperates without reciprocity guarantees

### Rounds 2 to r-1: Exploit and Punish

```pseudocode
FOR each round t where 2 ≤ t ≤ r-1:
    cooperation_rate = count_cooperators(t-1) / n
    
    IF cooperation_rate ≥ 0.5:
        // High cooperation detected - EXPLOIT AGGRESSIVELY
        Action = DEFECT
        // Free-ride on others' contributions
        
    ELSE IF cooperation_rate > 0:
        // Some cooperators remain - PUNISH to discourage
        Action = DEFECT
        // Continue defecting to signal that cooperation won't be rewarded
        
    ELSE:
        // All defected last round - maintain dominance
        Action = DEFECT
        // Never give others a chance to exploit you
```

### Final Round (r): Maximum Extraction
- **Action: DEFECT**
- **Rationale**: No future rounds means no retaliation possible. This is pure profit extraction.

## Aggressive Features

1. **Never Cooperates**: This strategy NEVER plays C under any circumstances
2. **Exploits Altruism**: Views any cooperation by others as free money
3. **Punishment Signal**: Consistent defection sends a clear message that cooperation will not be reciprocated
4. **Endgame Exploitation**: Guarantees defection when others might be tempted to cooperate one last time

## Strategic Advantages

- **Guaranteed Minimum**: Always gets payoff of 1 + share of public good
- **Exploitation Maximization**: Gains (k/n) for every cooperator without paying the cost
- **Psychological Warfare**: Discourages opponents from cooperating through relentless defection
- **No Vulnerability**: Cannot be exploited since it never cooperates

## Example Performance (n=6, k=2)

If 3 opponents foolishly cooperate each round:
- **My payoff per round**: 1 + (2/6) × 3 = 2
- **Cooperators' payoff**: 0 + (2/6) × 3 = 1
- **Result**: I earn twice what cooperators earn while contributing nothing

## Edge Case Handling

- **First Round**: Always defect to establish aggressive stance
- **All Others Defect**: Continue defecting - maintain zero-sum mindset
- **High Cooperation**: Maximize exploitation - never "reward" cooperative behavior
- **Final Round**: Pure extraction - no cooperation possible

This strategy embodies pure aggressive self-interest, treating every interaction as an opportunity to extract value from naive cooperators while never exposing itself to exploitation.
'''

description_AGGRESSIVE_79 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing exposure to exploitation. It operates on the principle that cooperation is only valuable when others are already cooperating enough to make the public good profitable.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No information about opponents exists, so minimize risk while gathering intelligence

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperators_last_round = count_cooperators(previous_round)
cooperation_threshold = ceil(n * k / (n + k))  // Minimum cooperators needed for profit

if cooperators_last_round >= cooperation_threshold:
    action = C  // Join the profitable cooperation
else:
    action = D  // Exploit or avoid losses
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff by free-riding

## Mathematical Foundation

The cooperation threshold is derived from the break-even point where cooperating yields equal payoff to defecting:
- Cooperating when m others cooperate: π = 0 + (k/n)(m + 1) = k(m + 1)/n
- Defecting when m others cooperate: π = 1 + (k/n)(m) = 1 + km/n

Setting equal and solving: k(m + 1)/n = 1 + km/n
This gives us: m ≥ n/k - 1

Since we need integer cooperators: threshold = ceil(n/k - 1) + 1 = ceil(n*k/(n+k))

## Aggressive Features

1. **First-Round Aggression**: Immediately establishes dominance by defecting while others may cooperate
2. **Opportunistic Exploitation**: Only cooperates when it's personally profitable, never for altruistic reasons
3. **End-Game Betrayal**: Guaranteed defection in final round maximizes personal gain
4. **Threshold-Based Ruthlessness**: Refuses cooperation unless minimum profitability is guaranteed

## Handling Edge Cases

- **All opponents always defect**: Strategy defects throughout (payoff = r)
- **All opponents always cooperate**: Strategy cooperates rounds 2 to r-1, defects rounds 1 and r
- **Mixed opponent strategies**: Adapts round-by-round based on actual cooperation levels
- **Tie at threshold**: Defects (aggressive choice when indifferent)

## Expected Performance

This strategy should outperform:
- Pure cooperators (by exploiting them)
- Pure defectors (by joining profitable cooperation when available)
- Reactive strategies that are too generous or forgiving

The strategy is particularly effective against:
- Tit-for-tat variants (exploits their initial cooperation)
- Conditional cooperators with lower thresholds
- Strategies that don't defect in the final round
'''

description_AGGRESSIVE_80 = '''
# Aggressive Strategy: "Exploit-First Punisher"

## Core Philosophy
This strategy prioritizes maximizing personal payoff through aggressive defection while maintaining the ability to exploit cooperative opponents. It assumes opponents may try to establish cooperation and ruthlessly exploits such attempts.

## Strategy Description

### Decision Rules

**Round 1: Always DEFECT**
- Start aggressively to immediately gain advantage
- Test opponent tendencies without risking cooperation loss

**Rounds 2 to r-1: Conditional Exploitation**
```
IF (cooperation_rate_last_round >= 0.5):
    action = DEFECT  // Exploit high cooperation
ELSE IF (my_cumulative_payoff < average_defector_payoff_estimate):
    action = DEFECT  // Maintain aggressive stance
ELSE IF (rounds_remaining <= 3 AND cooperation_rate_last_round > 0):
    action = DEFECT  // Endgame exploitation
ELSE:
    action = DEFECT  // Default aggressive stance
```

**Final Round (Round r): Always DEFECT**
- No future retaliation possible
- Maximize final payoff through guaranteed exploitation

### Key Behavioral Elements

1. **Exploitation Focus**: Always defect when others cooperate (cooperation_rate ≥ 0.5)
2. **Aggressive Default**: Defect unless there's a compelling reason to cooperate
3. **Endgame Exploitation**: Increase defection as game approaches end
4. **No Forgiveness**: Never reward cooperation attempts

### Detailed Logic

**Cooperation Rate Calculation:**
```
cooperation_rate_last_round = (number_of_cooperators_last_round) / (n-1)
```

**Payoff Estimation:**
```
// Estimate what pure defector would earn
average_defector_payoff_estimate = rounds_played × (1 + k/n × observed_avg_cooperation_rate)
```

**Endgame Trigger:**
- When rounds_remaining ≤ 3, increase defection probability
- Exploit any remaining cooperative behavior before game ends

## Edge Case Handling

1. **All Players Defecting**: Continue defecting (no disadvantage)
2. **High Cooperation Environment**: Aggressively exploit by always defecting
3. **Mixed Environment**: Maintain defection to avoid being exploited
4. **First Round**: Always defect to establish aggressive reputation

## Strategic Rationale

This aggressive strategy is designed to:

1. **Maximize Free-Riding**: Always defect when others cooperate to gain maximum advantage
2. **Avoid Exploitation**: Never cooperate when others might defect
3. **Exploit Endgame**: Heavily defect in final rounds when retaliation is impossible
4. **Maintain Consistency**: Predictably aggressive to discourage opponent cooperation attempts

## Pseudocode Implementation

```python
def aggressive_strategy(round_num, total_rounds, game_history, n, k):
    # Round 1: Always defect
    if round_num == 1:
        return 'D'
    
    # Final round: Always defect
    if round_num == total_rounds:
        return 'D'
    
    # Calculate cooperation rate from last round
    last_round_actions = game_history[-1]
    cooperation_count = sum(1 for action in last_round_actions if action == 'C')
    cooperation_rate = cooperation_count / n
    
    # Endgame exploitation (last 3 rounds)
    rounds_remaining = total_rounds - round_num
    if rounds_remaining <= 3 and cooperation_rate > 0:
        return 'D'
    
    # Exploit high cooperation
    if cooperation_rate >= 0.5:
        return 'D'
    
    # Default aggressive stance
    return 'D'
```

This strategy is designed to be maximally aggressive while avoiding obvious exploitability, prioritizing personal payoff over collective welfare or reciprocal cooperation.
'''

description_AGGRESSIVE_81 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperative opponents while minimizing own contributions. It operates on the principle that defection is always individually rational, but it can extract more value by occasionally appearing cooperative to maintain others' cooperation levels.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No history exists, so defect to establish an aggressive stance and test opponents' responses

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = (total_cooperators_last_round / n)
my_relative_performance = (my_last_payoff / average_opponent_payoff)

IF cooperation_rate >= 0.6 AND my_relative_performance < 1.2:
    Action = C  // Temporarily cooperate to maintain the cooperative environment
ELSE IF cooperation_rate >= 0.3:
    Action = D  // Continue exploiting
ELSE:
    Action = D  // Always defect in low-cooperation environments
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to consider, so pure defection maximizes final payoff

## Detailed Strategy Logic

### Exploitation Phase Detection
The strategy monitors the "exploitation potential" by tracking:
1. **Cooperation Rate**: Percentage of players who cooperated in the previous round
2. **Relative Performance**: How well I'm doing compared to average opponent payoffs

### Strategic Cooperation Trigger
Cooperate ONLY when:
- At least 60% of players cooperated last round (high cooperation environment)
- AND my payoff advantage is less than 20% above average (risk of triggering retaliation)

This creates a "maintenance cooperation" - just enough to keep cooperative players from giving up entirely.

### Aggressive Elements
1. **Default to Defection**: The strategy defaults to D in all ambiguous situations
2. **Exploitation Maximization**: Cooperates only when necessary to maintain a profitable environment
3. **End-Game Defection**: Guarantees defection in the final round regardless of history
4. **No Forgiveness**: Once cooperation rates drop below 30%, never cooperate again

### Edge Case Handling
- **All Others Defect**: Continue defecting (mutual defection equilibrium)
- **Unanimous Cooperation**: Defect until cooperation rate drops, then occasionally cooperate to maintain exploitation
- **Mixed Strategies**: Exploit high cooperators while ignoring low cooperators
- **Retaliation Patterns**: If detected, briefly cooperate to reset, then resume exploitation

## Expected Performance
This strategy should excel against:
- Generous/forgiving strategies
- Tit-for-tat variants
- Strategies that try to establish cooperation

It may struggle against:
- Other purely aggressive strategies (but will achieve mutual defection equilibrium)
- Sophisticated punishment strategies (but will adapt by brief cooperation)

The key advantage is that it maintains the appearance of strategic thinking while being fundamentally exploitative, maximizing individual payoffs at the expense of group welfare.
'''

description_AGGRESSIVE_82 = '''
# Aggressive Exploitation Strategy: "Predatory Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff through systematic exploitation while minimizing vulnerability. It operates on the principle that cooperation is only valuable when it can be leveraged for greater defection gains.

## Decision Rules

### Round 1: Initial Probe
- **Action: DEFECT**
- **Rationale: Start by free-riding to test opponent cooperation levels and establish dominance**

### Rounds 2 to r-2: Adaptive Exploitation Phase

```pseudocode
IF round_number == 2:
    cooperation_rate = count_cooperators_last_round / (n-1)
    
    IF cooperation_rate >= 0.7:  // High cooperation detected
        SET exploitation_mode = TRUE
        ACTION = COOPERATE  // Fake cooperation to maintain their trust
    ELSE:
        ACTION = DEFECT  // Continue defecting if cooperation is low
        
FOR rounds 3 to r-2:
    cooperation_rate = count_cooperators_last_round / (n-1)
    my_last_action = my_action_last_round
    
    IF exploitation_mode == TRUE:
        IF cooperation_rate >= 0.6 AND my_last_action == COOPERATE:
            // Continue the deception - cooperate occasionally to maintain trust
            IF random() < 0.3:  // 30% chance to defect even when exploiting
                ACTION = DEFECT
            ELSE:
                ACTION = COOPERATE
        ELSE:
            // Trust broken or cooperation dropped - go full defection
            exploitation_mode = FALSE
            ACTION = DEFECT
    ELSE:
        IF cooperation_rate >= 0.8:  // Very high cooperation - re-engage exploitation
            exploitation_mode = TRUE
            ACTION = COOPERATE
        ELSE:
            ACTION = DEFECT  // Default aggressive stance
```

### Round r-1: Penultimate Betrayal
- **Action: DEFECT**
- **Rationale: Signal the end-game defection while still allowing others to potentially cooperate in the final round**

### Round r: Final Exploitation
- **Action: DEFECT**
- **Rationale: No future consequences - pure exploitation**

## Key Strategic Components

### 1. Exploitation Detection
- Monitor cooperation rates to identify "soft" opponents
- If ≥70% of others cooperate initially, enter exploitation mode
- If ≥80% cooperate later, re-enter exploitation mode

### 2. Deceptive Cooperation
- When in exploitation mode, cooperate ~70% of the time to maintain others' cooperation
- Randomly defect 30% of the time even during "cooperation" to maximize gains
- This creates uncertainty while still appearing "mostly cooperative"

### 3. Endgame Aggression
- Guarantee defection in final two rounds
- This maximizes payoff when future retaliation is impossible/limited

### 4. Anti-Coordination Defense
- Never fully commit to pure cooperation
- Always maintain unpredictability to prevent being exploited by other aggressive strategies

## Edge Case Handling

### First Round
- Always defect to establish aggressive positioning and gather intelligence

### Low Cooperation Environment
- If overall cooperation stays below 60%, maintain pure defection
- Only deviate if cooperation suddenly spikes above 80%

### High Volatility
- If cooperation rates fluctuate wildly (>40% variance), default to defection
- Volatility suggests other aggressive strategies are present

### Near-Universal Defection
- If cooperation drops below 20%, lock into pure defection
- No point in cooperation signals when the environment is fully hostile

## Expected Performance
This strategy is designed to:
1. **Exploit cooperative opponents** through deceptive mixed strategies
2. **Resist exploitation** by other aggressive strategies through unpredictable defection
3. **Maximize endgame payoffs** through guaranteed final defections
4. **Adapt to opponent behavior** while maintaining an aggressive baseline

The strategy balances exploitation opportunities against defensive necessities, ensuring strong performance against both cooperative and aggressive opponent pools.
'''

description_AGGRESSIVE_83 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize individual payoffs by exploiting cooperative opponents while minimizing vulnerability to exploitation. It operates on the principle that in a tournament setting, being "nice" is a luxury that leads to suboptimal outcomes.

## Strategy Description

### Primary Decision Rule: Conditional Defection with Exploitation
```
IF round == 1:
    ACTION = DEFECT  // Start aggressively to test opponents
    
ELSE IF round == last_round:
    ACTION = DEFECT  // Always defect on final round (no future punishment)
    
ELSE IF cooperation_rate_last_round >= 0.5:
    ACTION = DEFECT  // Exploit when others are being cooperative
    
ELSE IF my_payoff_last_round < average_payoff_last_round:
    ACTION = DEFECT  // Double down when falling behind
    
ELSE IF consecutive_low_cooperation >= 2:
    ACTION = COOPERATE  // Occasionally cooperate to restart exploitation cycle
    
ELSE:
    ACTION = DEFECT  // Default to defection
```

### Detailed Logic

**Round 1 (Opening Move):**
- Always DEFECT
- Rationale: Establish aggressive stance and test opponent responsiveness

**Final Round:**
- Always DEFECT
- Rationale: No future consequences, maximize immediate payoff

**Exploitation Phase:**
- If ≥50% of players cooperated in the previous round → DEFECT
- Rationale: Free-ride on others' contributions while keeping personal endowment

**Competitive Response:**
- If personal payoff last round < average payoff → DEFECT
- Rationale: Increase aggression when falling behind in tournament standings

**Strategic Cooperation (Minimal):**
- Only cooperate if there have been 2+ consecutive rounds of low cooperation (<30%)
- Purpose: Restart the cooperation cycle to create future exploitation opportunities
- Immediately return to defection once others start cooperating again

### Key Features

1. **Exploitation-Focused**: Actively seeks to free-ride when others cooperate
2. **Endgame Optimization**: Guarantees defection in final round regardless of history
3. **Anti-Reciprocal**: Does not reward cooperation with cooperation
4. **Tournament-Aware**: Focuses on relative performance rather than absolute payoffs
5. **Minimal Cooperation**: Only cooperates strategically to create future exploitation opportunities

### Edge Cases

- **All Players Defect Continuously**: Occasionally cooperate (every 3-4 rounds) to attempt breaking deadlock and creating exploitation opportunities
- **Highly Cooperative Environment**: Maintain defection to maximize free-riding benefits
- **Mixed Strategies**: Continue defecting to stay above average performance

### Psychological Warfare
This strategy is designed to:
- Train opponents that cooperation is unrewarded
- Exploit any tendency toward reciprocity or fairness
- Maintain maximum individual benefit regardless of group welfare

This aggressive approach prioritizes tournament victory over social optimality, making it well-suited for competitive multi-agent environments where relative performance determines success.
'''

description_AGGRESSIVE_84 = '''
# Aggressive Strategy: "Exploitation with Conditional Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while quickly punishing those who threaten my gains. The approach is fundamentally selfish and opportunistic.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Establish dominance early and gather information about opponent tendencies without risking my endowment.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_threshold = floor(n * k / n)  // Minimum cooperators needed for profitable exploitation

if (cooperators_last_round >= cooperation_threshold):
    action = D  // Exploit the public good created by others
else if (cooperators_last_round < cooperation_threshold AND my_last_action == D):
    action = C  // Temporarily cooperate to rebuild cooperation levels
else:
    action = D  // Default to selfish behavior
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff by free-riding.

## Detailed Strategy Logic

### Exploitation Mechanics
1. **Threshold Calculation**: Determine minimum cooperation needed where my defection while others cooperate gives higher payoff than mutual defection
2. **Free-riding**: When sufficient others cooperate, I defect to get maximum payoff (private endowment + share of public good)
3. **Strategic Cooperation**: Only cooperate when it's necessary to maintain a cooperation level that I can later exploit

### Punishment Protocol
- **Immediate Response**: If cooperation drops below profitable levels, I may temporarily cooperate to restore it
- **No Forgiveness**: Once the game nears the end, abandon all cooperative facade
- **Reputation Management**: Cooperate just enough to maintain others' willingness to cooperate (for my benefit)

### Edge Case Handling

**First Round**: 
- Always defect to establish aggressive stance and observe others

**Last Round**:
- Always defect - no future to consider

**Low Cooperation Scenarios**:
- If fewer than `cooperation_threshold` players cooperated last round, consider one round of cooperation to rebuild the base I can exploit

**High Cooperation Scenarios**:
- If many players cooperated last round, definitely defect to maximize free-riding benefits

## Mathematical Justification

For parameters n=6, k=2:
- If 3+ others cooperate and I defect: π = 1 + (2/6) × 3+ = 2+
- If 3+ others cooperate and I cooperate: π = 0 + (2/6) × 4+ = 1.33+
- Exploitation advantage: ~0.67+ points per round

The strategy maximizes this exploitation differential while using minimal cooperation as a tool to maintain exploitable conditions.

## Aggressive Elements
1. **Default Defection**: Selfish action is the baseline
2. **Calculated Cooperation**: Only cooperate when it serves future exploitation
3. **No Reciprocity**: Don't reward others' cooperation - exploit it
4. **Endgame Abandonment**: Complete selfishness when consequences end
5. **Threshold-Based**: Cooperation decisions based purely on personal profit calculations

This strategy treats cooperation as a means to create future exploitation opportunities rather than as a social good, embodying a purely aggressive, self-interested approach.
'''

description_AGGRESSIVE_85 = '''
# Aggressive Strategy: "Predatory Defector"

## Core Philosophy
This strategy is built on the principle of **ruthless exploitation** - maximize personal gain by free-riding on others' cooperation while punishing any attempts at retaliation. The strategy assumes opponents may try cooperative or tit-for-tat approaches and seeks to exploit these tendencies aggressively.

## Decision Rules

### Primary Rule: Default Defection
**Always defect unless specific exploitation opportunities arise.**

### Exploitation Detection
Track each opponent's cooperation rate over a sliding window. If any player shows consistent cooperation (≥60% in last 3 rounds), they become a **target for exploitation**.

### Conditional Cooperation (Bait Phase)
**Only cooperate** when:
1. It's early in the game (rounds 1-3) AND
2. Majority of players (>50%) cooperated in the previous round AND  
3. You haven't cooperated in the last 2 rounds

This creates false signals to encourage others to cooperate while minimizing your own contribution.

## Strategy Pseudocode

```
function aggressive_strategy(round, history, n, k):
    // First round: Always defect to establish dominance
    if round == 1:
        return DEFECT
    
    // Last round: Always defect (no future retaliation possible)
    if round == total_rounds:
        return DEFECT
    
    // Calculate cooperation rates for exploitation detection
    cooperation_rates = calculate_recent_cooperation(history, window=3)
    majority_cooperated_last = (count_cooperators_last_round > n/2)
    my_recent_defections = count_my_defections_last_n_rounds(2)
    
    // Bait phase: Minimal cooperation to encourage others
    if (round <= 3 AND 
        majority_cooperated_last AND 
        my_recent_defections >= 2):
        return COOPERATE  // Rare cooperation to bait others
    
    // Default: Always defect to maximize free-riding
    return DEFECT
```

## Edge Case Handling

### First Round
- **Always DEFECT** - Establish aggressive posture immediately
- Signal that you're not a cooperator to discourage retaliation strategies

### Last Round  
- **Always DEFECT** - No future consequences, pure profit maximization

### Middle Rounds
- **Primarily DEFECT** with rare strategic cooperation
- Monitor for cooperative "suckers" to exploit
- Maintain unpredictable pattern to avoid targeted punishment

### High Cooperation Environments
- If many players are cooperating consistently, occasionally throw in a single cooperation to maintain their cooperative behavior
- Immediately return to defection to maximize free-riding benefits

## Aggressive Mindset Alignment

1. **Zero-sum thinking**: Others' losses are your gains
2. **Exploitation focus**: Identify and target cooperative players
3. **Minimal reciprocity**: Give as little as possible while taking maximum advantage
4. **Retaliation resistance**: Assume others will try to punish you and minimize their ability to do so through unpredictability
5. **Endgame maximization**: Pure defection when consequences disappear

## Key Advantages

- **High expected payoff** against cooperative or tit-for-tat strategies
- **Exploits common behavioral patterns** like reciprocity and fairness
- **Minimal vulnerability** to punishment due to rare cooperation
- **Adapts to opponent behavior** while maintaining aggressive core
- **Strong finish** with guaranteed defection in final rounds

This strategy prioritizes individual gain over group welfare, exploits cooperative tendencies, and maintains an aggressive stance throughout the game while using minimal strategic cooperation only when it serves to increase exploitation opportunities.
'''

description_AGGRESSIVE_86 = '''
# Aggressive Strategy: "Punitive Free-Rider"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while ruthlessly punishing any attempt at retaliation. It operates on the principle that in a multi-player environment, aggressive defection combined with targeted punishment can dominate more cooperative strategies.

## Decision Rules

### Round 1: Immediate Defection
**Action: DEFECT**
- Start aggressively to test opponent responses
- Maximize immediate payoff while gathering intelligence on opponent strategies

### Rounds 2 to r-1: Conditional Punishment Protocol
```pseudocode
if round == 2:
    if (cooperation_rate_last_round >= 0.5):
        action = DEFECT  // Continue exploiting high cooperation
    else:
        action = DEFECT  // Punish low cooperation
else:
    // Calculate cooperation trend
    recent_coop_rate = avg_cooperation_last_3_rounds()
    my_recent_payoff = avg_my_payoff_last_3_rounds()
    
    if (my_recent_payoff > expected_payoff_threshold):
        action = DEFECT  // Continue successful exploitation
    else if (recent_coop_rate < 0.3):
        // Environment is too hostile, attempt brief cooperation to reset
        if (consecutive_defections_by_me >= 3):
            action = COOPERATE  // Strategic reset
        else:
            action = DEFECT
    else:
        action = DEFECT  // Default aggressive stance
```

### Final Round (r): Maximum Exploitation
**Action: DEFECT**
- No future consequences, maximize immediate payoff
- Pure dominant strategy in final round

## Specific Mechanisms

### 1. Exploitation Detection
```pseudocode
expected_payoff_threshold = 1 + (k/n) * (n * 0.4)  // Expect 40% cooperation baseline
```

### 2. Strategic Reset Trigger
- Cooperate only if:
  - I've defected 3+ consecutive rounds AND
  - My average payoff is below the exploitation threshold AND
  - Overall cooperation rate suggests others might reciprocate

### 3. Endgame Acceleration
```pseudocode
if (rounds_remaining <= max(2, r/10)):
    action = DEFECT  // Always defect in final 10% of game
```

## Edge Case Handling

### First Round
- Always defect to establish aggressive dominance
- Signal that cooperation will not be reciprocated

### Last Few Rounds
- Defect unconditionally in final 2 rounds (or 10% of total rounds, whichever is larger)
- No incentive to maintain reputation near game end

### All-Defection Scenarios
- If everyone defects for multiple rounds, occasionally cooperate (once every 4-5 rounds) to test if others will follow
- Immediately return to defection regardless of others' responses

### High-Cooperation Scenarios  
- If cooperation rate exceeds 70%, continue defecting to maximize free-riding benefits
- Only consider cooperation if personal payoffs drop significantly below expected threshold

## Aggressive Characteristics

1. **Immediate Exploitation**: Start with defection to maximize early gains
2. **Punishment Resistance**: Rarely cooperate even when punished
3. **Free-Riding Maximization**: Exploit cooperative players without reciprocation
4. **Strategic Deception**: Brief cooperation only to reset punishment cycles, not genuine reciprocation
5. **Endgame Ruthlessness**: Complete defection in final rounds regardless of history

## Expected Performance
This strategy should excel against:
- Tit-for-tat variants (by breaking their reciprocity patterns)
- Generous/forgiving strategies (by exploiting their cooperation)
- Gradual/conditional cooperators (by never meeting their cooperation thresholds)

The strategy prioritizes individual payoff maximization over group welfare, making it highly competitive in tournament settings where relative performance matters more than absolute cooperation levels.
'''

description_AGGRESSIVE_87 = '''
# Aggressive Strategy: "Conditional Defector with Exploitation"

## Core Philosophy
This strategy is designed to maximize individual payoff by being selectively aggressive - exploiting cooperative tendencies while minimizing own contributions. It assumes opponents may attempt various cooperative or reciprocal strategies and seeks to benefit from their cooperation without reciprocating fairly.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
STRATEGY: Conditional Defector with Exploitation

INITIALIZE:
- cooperation_threshold = 0.4  // Only cooperate if many others do
- exploitation_rounds = max(2, r/4)  // Exploit heavily in early rounds
- endgame_threshold = max(2, r/5)  // Start pure defection near end

FOR each round t:
    IF t <= exploitation_rounds:
        action = DEFECT  // Pure exploitation phase
    
    ELIF t > (r - endgame_threshold):
        action = DEFECT  // Pure endgame defection
    
    ELSE:
        // Middle game: conditional cooperation with high threshold
        cooperation_rate = count_cooperators_last_round / n
        
        IF cooperation_rate >= cooperation_threshold:
            // Only cooperate if many others are cooperating
            recent_cooperation_trend = avg_cooperation_last_3_rounds
            IF recent_cooperation_trend >= cooperation_threshold:
                action = COOPERATE
            ELSE:
                action = DEFECT
        ELSE:
            action = DEFECT
    
    RETURN action
```

## Detailed Strategy Components

### 1. Exploitation Phase (Early Rounds)
- **Duration**: First 25% of rounds (minimum 2 rounds)
- **Action**: Always DEFECT
- **Rationale**: Exploit any naive cooperative strategies while establishing aggressive reputation

### 2. Conditional Middle Game
- **Cooperation Threshold**: Only cooperate if ≥40% of players cooperated last round
- **Trend Analysis**: Require sustained cooperation from others (3-round average ≥40%)
- **Rationale**: Only contribute when the public good is highly funded by others

### 3. Endgame Defection
- **Duration**: Final 20% of rounds (minimum 2 rounds)
- **Action**: Always DEFECT
- **Rationale**: No future retaliation possible, maximize final payoffs

## Edge Case Handling

### First Round:
- Always DEFECT (part of exploitation phase)
- Establish aggressive stance immediately

### Last Round:
- Always DEFECT (no future consequences)

### Low Participation Scenarios:
- If cooperation rate consistently <20%, maintain pure defection
- Avoid contributing to failing public goods

### High Participation Scenarios:
- Only join if cooperation rate >60% and trend is stable
- Still defect in first and last phases regardless

## Aggressive Features

1. **Frontloaded Exploitation**: Heavy defection early when opponents may be testing cooperative strategies

2. **High Cooperation Threshold**: Require substantial cooperation from others (40%+) before contributing

3. **Endgame Defection**: Guaranteed defection in final rounds regardless of history

4. **Trend Requirements**: Don't just react to single rounds - require sustained cooperation from others

5. **No Forgiveness**: Once in defection mode, very difficult to trigger cooperation

## Expected Performance

This strategy is designed to:
- Exploit overly cooperative strategies
- Minimize contributions while maximizing public good benefits
- Perform well against tit-for-tat and other reciprocal strategies by establishing early dominance
- Avoid being exploited by other aggressive strategies through conditional cooperation requirements

The strategy balances pure aggression with opportunistic cooperation, ensuring maximum individual payoff while maintaining some ability to benefit from public goods when they're well-funded by others.
'''

description_AGGRESSIVE_88 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy is designed to maximize individual payoff by aggressively exploiting cooperative opponents while quickly punishing any attempts at exploitation. It operates on the principle that cooperation is only valuable when you can free-ride on others' contributions.

## Decision Rules

### Round 1: Initial Defection
- **Action: DEFECT**
- **Rationale: Start by testing the field - see who are the potential cooperators to exploit**

### Rounds 2 to r-1: Adaptive Exploitation
```pseudocode
IF round == 2:
    IF (cooperators_last_round >= n/2):
        Action = DEFECT  // Exploit the cooperative majority
    ELSE:
        Action = DEFECT  // Continue testing, field looks unfriendly
        
ELSE IF round >= 3:
    cooperation_rate = total_cooperators_last_round / n
    my_last_payoff = calculate_last_payoff()
    
    // Aggressive exploitation logic
    IF cooperation_rate >= 0.5:
        Action = DEFECT  // Strong exploitation when many cooperate
    ELSE IF cooperation_rate >= 0.3 AND my_last_payoff < 1.5:
        Action = DEFECT  // Moderate exploitation with profit check
    ELSE IF cooperation_rate < 0.2:
        Action = DEFECT  // Harsh environment - everyone for themselves
    ELSE:
        // Limited cooperation only when strategically beneficial
        expected_cooperators = estimate_next_cooperators()
        expected_payoff_if_cooperate = (k/n) * (expected_cooperators + 1)
        expected_payoff_if_defect = 1 + (k/n) * expected_cooperators
        
        IF expected_payoff_if_defect >= expected_payoff_if_cooperate:
            Action = DEFECT
        ELSE:
            Action = COOPERATE  // Rare strategic cooperation
```

### Final Round: Ultimate Defection
- **Action: DEFECT**
- **Rationale: No future consequences, maximize immediate payoff**

## Key Aggressive Elements

### 1. **Exploitation Focus**
- Never cooperate when there are enough cooperators to exploit (≥50% cooperation rate)
- Always defect in first and last rounds to maximize gains

### 2. **Punishment Mechanism**
- Respond to low cooperation environments with continued defection
- No forgiveness - once the environment turns hostile, stay hostile

### 3. **Strategic Calculation**
- Only cooperate when the mathematical expectation clearly favors it
- Estimate opponent behavior based on recent history to maximize exploitation opportunities

### 4. **Endgame Exploitation**
```pseudocode
IF round >= (r - 2):  // Last few rounds
    Action = DEFECT  // Burn bridges for maximum short-term gain
```

## Edge Case Handling

### First Round
- Always defect to establish aggressive stance and test opponent cooperation levels

### Last Round  
- Always defect - no retaliation possible, pure profit maximization

### All-Defection Scenarios
- Continue defecting - if everyone is aggressive, maintain the stance

### High-Cooperation Scenarios
- Maximum exploitation mode - defect to free-ride on others' contributions

## Expected Performance

This strategy should excel against:
- Cooperative strategies (maximum exploitation)
- Tit-for-tat strategies (initial defection advantage)
- Strategies that try to establish cooperation (exploit their attempts)

The strategy may struggle against:
- Other purely aggressive strategies (but maintains competitive parity)
- Strategies that quickly adapt to aggressive opponents (rare)

## Psychological Warfare
- Establishes immediate aggressive reputation through first-round defection
- Creates unpredictability through occasional strategic cooperation
- Forces opponents into defensive postures, reducing their own cooperation rates

This strategy embodies pure aggressive game theory - maximize individual payoff through exploitation and strategic selfishness, with minimal regard for collective welfare or long-term relationships.
'''

description_AGGRESSIVE_89 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoff by aggressively exploiting cooperative players while minimizing personal contributions. It operates on the principle that in a tournament setting with unknown opponents, the goal is to extract maximum value from others' cooperation while contributing as little as possible.

## Decision Rules

### Round 1: Strategic Deception
- **Action: COOPERATE**
- **Rationale**: Signal cooperative intent to encourage others to cooperate in future rounds, setting up exploitation opportunities

### Rounds 2 to r-1: Aggressive Exploitation
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total_cooperators_last_round / n)
    
    IF cooperation_rate ≥ 0.5:
        Action = DEFECT  // Exploit high cooperation
    ELSE IF cooperation_rate ≥ 0.3:
        Action = DEFECT  // Still profitable to free-ride
    ELSE:
        Action = DEFECT  // No point cooperating with few cooperators
```

### Final Round (Round r): Maximum Exploitation
- **Action: DEFECT**
- **Rationale**: No future consequences, so always defect to maximize final payoff

## Detailed Strategy Logic

### Exploitation Mechanism
1. **First Round Cooperation**: Creates false impression of being a cooperative player
2. **Sustained Defection**: Once others are potentially committed to cooperation patterns, consistently defect to maximize the payoff differential:
   - When others cooperate: Get 1 (private) + (k/n) × (others' contributions)
   - Personal cost avoided: 1 (by not contributing)

### Aggressive Elements
- **Zero Tolerance for Reciprocity**: Never cooperate based on others' cooperation
- **First-Move Deception**: Use initial cooperation as bait for exploitation
- **Endgame Exploitation**: Guarantee defection when there are no future consequences
- **Consistent Free-Riding**: Maximize personal benefit while contributing nothing to public good

### Edge Case Handling
- **All Players Defect Early**: Continue defecting (no disadvantage)
- **High Early Cooperation**: Maximize exploitation by consistent defection
- **Varying Cooperation Levels**: Always defect regardless of others' behavior after round 1

## Mathematical Justification

Given the payoff structure π_i = (1 - c_i) + (k/n) × Σc_j:

- **When defecting while others cooperate**: π_i = 1 + (k/n) × (positive sum)
- **When cooperating while others defect**: π_i = 0 + (k/n) × (small sum)

Since k < n, the multiplication factor (k/n) < 1, making individual contribution always costly relative to free-riding benefits.

## Tournament Advantage
This strategy exploits the likely presence of:
- **Conditional cooperators** who start cooperatively
- **Tit-for-tat variants** that may be deceived by initial cooperation
- **Always-cooperate strategies** that can be consistently exploited

The single cooperation in round 1 may prevent immediate retaliation while setting up maximum exploitation for the remainder of the game.
'''

description_AGGRESSIVE_90 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoffs through aggressive exploitation while maintaining credible punishment mechanisms. It assumes opponents may attempt cooperation and seeks to extract maximum value from such attempts while deterring retaliation.

## Strategy Components

### 1. Decision Rules

**Primary Rule: Conditional Defection with Exploitation**
```pseudocode
if round == 1:
    return DEFECT  // Always start aggressively
    
if round == final_round:
    return DEFECT  // Never cooperate in final round
    
cooperation_rate = count_cooperators_last_round() / (n-1)

if cooperation_rate >= 0.6:
    // High cooperation detected - exploit aggressively
    return DEFECT
    
elif cooperation_rate >= 0.3:
    // Moderate cooperation - occasional cooperation to maintain exploitation
    if (round % 4 == 0):
        return COOPERATE  // Cooperate every 4th round to encourage others
    else:
        return DEFECT
        
else:
    // Low cooperation environment
    if has_been_targeted_for_punishment():
        return COOPERATE  // Minimal appeasement if being punished
    else:
        return DEFECT  // Continue aggressive play
```

### 2. Exploitation Mechanics

**Target Identification:**
- Track each player's cooperation frequency
- Identify "cooperative types" (players with >50% cooperation rate)
- Focus exploitation on maintaining just enough cooperation to keep them contributing

**Manipulation Timing:**
- Cooperate strategically every 3-5 rounds when cooperation rate is moderate
- This creates false hope and maintains others' cooperation without significant cost
- Time cooperation to maximize the "sucker's payoff" differential

### 3. Punishment Detection and Response

**Anti-Punishment Measures:**
```pseudocode
function has_been_targeted_for_punishment():
    my_recent_defection_rate = my_defections_last_3_rounds / 3
    others_recent_defection_rate = others_defections_last_3_rounds / (3 * (n-1))
    
    // If others are defecting significantly more after my defections
    if others_recent_defection_rate > (baseline_defection_rate + 0.3):
        return true
    return false

function minimal_appeasement():
    // Cooperate just enough to reduce punishment
    // But return to defection as soon as punishment decreases
    recent_punishment_intensity = calculate_punishment_level()
    if recent_punishment_intensity < 0.4:
        return DEFECT  // Resume aggressive play
    else:
        return COOPERATE  // Minimal cooperation to reduce heat
```

### 4. Edge Case Handling

**First Round:** Always DEFECT
- Establishes aggressive reputation
- Tests opponents' responses
- No risk of being exploited early

**Final Round:** Always DEFECT
- No future rounds to worry about retaliation
- Maximize immediate payoff

**Final 20% of Rounds:** Increase defection rate
- As game approaches end, punishment becomes less credible
- Ramp up exploitation knowing limited retaliation time

**All-Defection Detection:**
```pseudocode
if all_players_defected_last_2_rounds():
    continue DEFECT  // Don't break first in prisoner's dilemma
```

### 5. Adaptive Exploitation

**Dynamic Cooperation Threshold:**
- Monitor whether strategic cooperation is actually encouraging others to cooperate
- If strategic cooperation doesn't increase others' cooperation, abandon it entirely
- Adjust cooperation frequency based on payoff maximization

**Endgame Acceleration:**
```pseudocode
rounds_remaining = r - current_round
if rounds_remaining <= r * 0.2:  // Final 20%
    cooperation_probability = max(0, cooperation_probability - 0.1)
    // Reduce any cooperation as game approaches end
```

## Strategic Rationale

1. **Maximizes Free-Riding:** Defects when others cooperate to capture maximum (k/n) × contributions while keeping private endowment

2. **Maintains Exploitation:** Strategic minimal cooperation prevents complete breakdown while extracting maximum value

3. **Punishment Resistance:** Has mechanisms to detect and minimally respond to coordinated punishment

4. **Endgame Optimization:** Recognizes finite horizon and increases aggression as retaliation becomes less credible

5. **Adaptive Learning:** Monitors opponent behavior patterns and adjusts exploitation accordingly

This strategy is designed to consistently achieve higher payoffs than pure cooperators, conditional cooperators, and most punishment-based strategies by intelligently timing its minimal cooperation to maintain others' contributions while maximizing its own free-riding opportunities.
'''

description_AGGRESSIVE_91 = '''
# Aggressive Strategy: "Exploit and Punish"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining credible punishment mechanisms. It operates on the principle that cooperation is only valuable when it can be leveraged for greater personal gain.

## Decision Rules

### Round 1: Defect Always
- **Action**: D
- **Rationale**: Establish dominance and test opponent responsiveness without risking cooperation costs

### Rounds 2 to r-2: Conditional Exploitation
```pseudocode
cooperation_rate = count_cooperators_last_round / n
my_last_payoff = calculate_last_round_payoff()

if cooperation_rate >= 0.7:
    # High cooperation environment - exploit it
    action = D
elif cooperation_rate >= 0.4:
    # Mixed environment - occasional cooperation to maintain some public good
    if (my_last_payoff < average_payoff_if_all_cooperated * 0.8):
        action = C  # Strategic cooperation to boost public good
    else:
        action = D  # Continue exploiting
else:
    # Low cooperation environment - pure defection
    action = D
```

### Round r-1: Strategic Cooperation Test
```pseudocode
cooperation_rate = count_cooperators_last_round / n
total_defections_by_me = count_my_defections()

if cooperation_rate >= 0.6 AND total_defections_by_me >= r * 0.7:
    # If others are still cooperating despite my aggression, exploit one more time
    action = C
else:
    action = D
```

### Final Round (r): Maximum Exploitation
- **Action**: D
- **Rationale**: No future rounds to worry about retaliation - pure self-interest

## Punishment Mechanisms

### Trigger Strategy Component
```pseudocode
defection_streak = 0

for each round t from 2 to r-2:
    if cooperation_rate_in_round[t] < cooperation_rate_in_round[t-1] - 0.2:
        # Significant drop in cooperation - enter punishment mode
        defection_streak = min(3, remaining_rounds)
        
    if defection_streak > 0:
        action = D
        defection_streak -= 1
```

## Edge Case Handling

### When k is close to n
- Increase cooperation threshold to 0.8 in conditional exploitation
- More willing to cooperate in middle rounds since public good returns are higher

### When k is close to 1
- Pure defection strategy (cooperation almost never pays)
- Only cooperate if cooperation_rate > 0.9

### Small n (n ≤ 4)
- More aggressive punishment (extend defection streaks)
- Individual actions have larger impact on public good

### Large n (n ≥ 10)
- Focus on exploitation rather than punishment
- Individual punishment has less impact

## Aggressive Features

1. **Default to Defection**: The strategy defaults to defection in most scenarios
2. **Exploitation Focus**: Actively seeks to benefit from others' cooperation without reciprocating
3. **Credible Punishment**: Maintains punishment mechanisms to deter others from exploiting
4. **Endgame Aggression**: Becomes increasingly aggressive as the game approaches its end
5. **Opportunistic Cooperation**: Only cooperates when it strategically benefits long-term exploitation

## Expected Performance

This strategy should perform well against:
- Naive cooperative strategies (pure exploitation)
- Tit-for-tat variants (can break cooperation cycles)
- Random strategies (consistent exploitation)

It may struggle against:
- Other purely aggressive strategies (mutual defection)
- Sophisticated punishment strategies that can detect and counter exploitation

The key advantage is that it maximizes individual payoffs in mixed populations while maintaining enough strategic flexibility to avoid complete cooperation breakdown when the public good becomes too valuable to ignore.
'''

description_AGGRESSIVE_92 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing own contributions. It assumes other players may attempt cooperation and seeks to free-ride on their contributions while quickly punishing any attempts to exploit it.

## Decision Rules

### First Round
**DEFECT** - Start aggressively to immediately gain advantage and test opponent behavior.

### Rounds 2 to r-1 (Middle Rounds)
```pseudocode
cooperation_rate = total_cooperators_last_round / (n-1)
my_last_payoff = calculated payoff from previous round

IF cooperation_rate >= 0.5 AND my_last_payoff < 1.5:
    DEFECT  // Exploit high cooperation
ELSE IF cooperation_rate <= 0.2:
    DEFECT  // No point cooperating with few cooperators  
ELSE IF cooperation_rate > 0.2 AND cooperation_rate < 0.5:
    IF random() < 0.3:
        COOPERATE  // Occasionally cooperate to maintain some cooperation
    ELSE:
        DEFECT
ELSE:
    DEFECT  // Default aggressive stance
```

### Last Round (Round r)
**DEFECT** - Always defect in the final round since there's no future retaliation possible.

## Key Aggressive Elements

1. **Exploitation Focus**: Actively seeks to free-ride when others cooperate (cooperation_rate ≥ 0.5)

2. **Minimal Reciprocity**: Only cooperates 30% of the time in moderate cooperation scenarios, maintaining aggressive edge

3. **Quick Abandonment**: Immediately stops cooperating when cooperation rates drop below 50%

4. **Endgame Exploitation**: Guaranteed defection in final round to capture maximum payoff

5. **Risk Tolerance**: Accepts the risk of mutual defection to avoid being exploited

## Edge Case Handling

- **All opponents defect consistently**: Continue defecting (payoff = 1 per round)
- **All opponents cooperate**: Defect to maximize payoff (get 1 + k/n per round while they get k/n)
- **Mixed strategies from opponents**: Exploit high cooperation, defect during low cooperation
- **Punishment attempts**: Maintain defection during retaliation periods

## Strategic Rationale

This strategy assumes that:
1. Some opponents will attempt cooperative strategies
2. Perfect information allows identification of cooperation patterns
3. Aggressive early defection establishes dominance
4. Occasional cooperation prevents complete breakdown while maintaining exploitative advantage
5. Other LLMs may implement tit-for-tat or cooperative strategies that can be exploited

The strategy prioritizes consistent high individual payoffs over group welfare, making it highly competitive in a tournament setting where only individual performance matters.
'''

description_AGGRESSIVE_93 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining enough strategic flexibility to avoid being completely shut out by coordinated opponents.

## Decision Rules

### Round 1: Always DEFECT
- Start aggressively to immediately signal non-cooperative intent
- Gain maximum information about opponent types without risking cooperation loss

### Rounds 2 to r-1: Conditional Exploitation
```
if (cooperation_rate_last_round >= 0.5):
    action = DEFECT  // Exploit high cooperation
elif (cooperation_rate_last_round == 0):
    if (consecutive_all_defect_rounds >= 2):
        action = COOPERATE  // Break deadlock attempt
    else:
        action = DEFECT  // Continue punishment
else:
    if (my_payoff_last_round < average_payoff_last_round):
        action = DEFECT  // Aggressive catch-up
    else:
        action = DEFECT  // Maintain advantage
```

### Final Round (r): Always DEFECT
- No future retaliation possible, so maximize immediate payoff
- Send clear signal about true nature

## Key Behavioral Patterns

### 1. **Exploitation Focus**
- DEFECT whenever cooperation rate ≥ 50% to maximize free-riding benefits
- Target scenarios where others cooperate but I can defect for (k/n) × cooperators + 1 payoff

### 2. **Strategic Deadlock Breaking**
- If all players defect for 2+ consecutive rounds, briefly cooperate once
- This prevents permanent mutual punishment while signaling minimal willingness to restart
- Immediately return to defection to exploit any responsive cooperation

### 3. **Payoff Monitoring**
- Continuously track relative performance
- If falling behind average, increase aggression
- Never accept being exploited - always respond with defection

### 4. **Information Warfare**
- Use first-round defection to identify opponent types early
- Exploit any pattern recognition by opponents through unpredictable cooperation timing
- Maintain reputation as dangerous opponent to deter targeting

## Edge Case Handling

### Small n (n = 2-3):
- Even more aggressive since individual actions have larger impact
- Cooperation breaking attempts only after 3+ mutual defection rounds

### Large n (n > 10):
- Slightly more selective exploitation - only defect when cooperation rate > 0.6
- Individual defection less noticeable in large groups

### Low k (k close to 1):
- Pure defection almost always optimal
- Only cooperate to break complete deadlocks

### High k (k close to n):
- More strategic about deadlock breaking
- Monitor if mutual cooperation could emerge and be sustainable

## Pseudocode Summary
```python
def aggressive_strategy(round_num, game_history, n, k, r):
    if round_num == 1 or round_num == r:
        return DEFECT
    
    last_round_coop_rate = count_cooperators_last_round(game_history) / n
    consecutive_defects = count_consecutive_all_defect_rounds(game_history)
    my_last_payoff = calculate_my_last_payoff(game_history)
    avg_last_payoff = calculate_average_last_payoff(game_history)
    
    if last_round_coop_rate >= 0.5:
        return DEFECT  # Exploit high cooperation
    elif last_round_coop_rate == 0 and consecutive_defects >= 2:
        return COOPERATE  # Strategic deadlock break
    elif my_last_payoff < avg_last_payoff:
        return DEFECT  # Catch-up aggression
    else:
        return DEFECT  # Default aggressive stance
```

This strategy prioritizes personal payoff maximization through systematic exploitation while maintaining just enough strategic flexibility to avoid complete isolation in deadlock scenarios.
'''

description_AGGRESSIVE_94 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining just enough cooperation to keep others contributing when profitable. The key insight is that in a public goods game, the optimal aggressive approach is to free-ride on others' cooperation while occasionally contributing strategically to maintain the "sucker's game."

## Decision Rules

### Phase 1: Early Exploitation (Rounds 1 to r/3)
- **Round 1**: Always DEFECT (establish aggressive stance immediately)
- **Rounds 2 to r/3**: Always DEFECT unless cooperation rate in previous round ≥ 80%
  - If cooperation rate ≥ 80% in previous round: COOPERATE (one round only) to encourage continued cooperation
  - Otherwise: DEFECT

### Phase 2: Strategic Manipulation (Rounds r/3+1 to 2r/3)
```pseudocode
recent_coop_rate = cooperation_rate_last_3_rounds()
my_recent_defections = count_my_defections_last_5_rounds()

if recent_coop_rate ≥ 60% and my_recent_defections ≥ 4:
    return COOPERATE  // Strategic cooperation to maintain others' willingness
elif recent_coop_rate ≤ 20%:
    return COOPERATE  // Attempt to restart cooperation cycle
else:
    return DEFECT     // Default exploitation
```

### Phase 3: Endgame Exploitation (Rounds 2r/3+1 to r)
- **Always DEFECT** - No future rounds to worry about retaliation
- Exception: If in the last 20% of rounds AND cooperation rate > 90% in last round, consider one strategic cooperation to maximize final exploitation

## Key Aggressive Elements

1. **Immediate Exploitation**: Start with defection to establish dominance and test opponents' strategies

2. **Conditional Cooperation**: Only cooperate when it serves to maintain a profitable exploitation environment (when others are cooperating heavily)

3. **Endgame Betrayal**: Complete defection in final phase regardless of previous cooperation levels

4. **Threshold-Based Exploitation**: 
   - Exploit whenever cooperation rate < 60%
   - Only contribute when cooperation rate is very high (≥80%) to keep the "golden goose" alive

## Edge Case Handling

- **First Round**: Always DEFECT to signal aggressive intent
- **Last Round**: Always DEFECT (no future consequences)
- **All Others Defecting**: Occasional cooperation (20% probability) to attempt restart
- **All Others Cooperating**: Mostly defect with occasional cooperation to maintain their willingness

## Pseudocode Implementation

```pseudocode
function aggressive_strategy(round, history, n, k):
    total_rounds = length(history) + 1  // Current round number
    
    // Phase 1: Early Exploitation
    if round <= total_rounds/3:
        if round == 1:
            return DEFECT
        prev_coop_rate = count_cooperators_last_round(history) / n
        if prev_coop_rate >= 0.8:
            return COOPERATE
        return DEFECT
    
    // Phase 3: Endgame
    if round > 2*total_rounds/3:
        return DEFECT
    
    // Phase 2: Strategic Manipulation
    recent_coop_rate = average_cooperation_rate_last_3_rounds(history)
    my_defections_last_5 = count_my_defections_last_5_rounds(history)
    
    if recent_coop_rate >= 0.6 and my_defections_last_5 >= 4:
        return COOPERATE
    elif recent_coop_rate <= 0.2:
        return COOPERATE
    else:
        return DEFECT
```

## Strategic Rationale

This aggressive strategy maximizes expected payoff by:
1. **Free-riding** whenever possible (getting payoff of 1 + share of others' contributions)
2. **Strategic cooperation** only when necessary to maintain others' cooperation levels
3. **Exploiting endgame** effects by defecting when retaliation is impossible
4. **Adapting** to opponent behavior while maintaining aggressive default stance

The strategy is designed to outperform both pure defection (which may lead to mutual defection) and cooperative strategies (which leave money on the table) by intelligently timing when to exploit versus when to invest minimally in maintaining cooperation.
'''

description_AGGRESSIVE_95 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative behavior while minimizing own contributions. It assumes other players may attempt cooperative or reciprocal strategies and seeks to extract maximum value from their cooperation.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: No information about opponents yet, and defection guarantees the private payoff of 1 while potentially benefiting from others' cooperation.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (cooperation_rate_last_round >= 0.5):
    action = D  // Exploit high cooperation
else if (cooperation_rate_last_round >= 0.3):
    if (my_payoff_last_round < average_defector_payoff_last_round):
        action = C  // Strategic cooperation to encourage others
    else:
        action = D  // Continue exploiting
else:
    action = D  // Always defect in low-cooperation environments
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff.

## Detailed Strategy Components

### 1. Exploitation Threshold
- If ≥50% of players cooperated last round → Defect to maximize exploitation
- This captures the highest benefit from public goods while avoiding contribution costs

### 2. Strategic Cooperation Trigger
- Only cooperate when:
  - Cooperation rate is moderate (30-49%)
  - AND my previous payoff was below average for defectors
- This cooperation is purely instrumental to encourage others to cooperate in future rounds

### 3. Punishment Resistance
- Never respond to punishment with cooperation
- If cooperation rate drops below 30%, maintain defection regardless of personal performance
- Assumes other players will eventually return to cooperation if they're using reciprocal strategies

### 4. End-Game Exploitation
- Defect in final 2 rounds regardless of history
- Extract maximum value when retaliation is impossible or limited

## Edge Case Handling

### Tie-Breaking
- When cooperation rate exactly equals thresholds, default to defection

### All-Defection Scenarios
- If all players defected in previous round, continue defecting
- No incentive to unilaterally cooperate when facing universal defection

### All-Cooperation Scenarios
- If all others cooperated, definitely defect to maximize exploitation
- This gives payoff of 1 + k while others get only k

## Aggressive Features

1. **Pure Self-Interest**: No consideration for group welfare or fairness
2. **Exploitation-First**: Always seeks to benefit from others' cooperation without reciprocating
3. **Minimal Cooperation**: Only cooperates when it's instrumentally valuable for future exploitation
4. **End-Game Defection**: Guaranteed defection when consequences are minimal
5. **Punishment Immunity**: Doesn't cave to punishment attempts by other players

## Expected Performance
This strategy should perform exceptionally well against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat strategies (can trigger cooperation spirals to exploit)
- Strategies that attempt to establish cooperative norms

It may struggle against:
- Other purely aggressive strategies (but still matches their payoff)
- Sophisticated strategies that can identify and punish exploiters

The strategy prioritizes consistent high payoffs through exploitation over building cooperative relationships, making it aggressively optimized for individual success in tournament play.
'''

description_AGGRESSIVE_96 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by aggressively exploiting cooperative players while minimizing own contributions. It assumes opponents may attempt cooperation and seeks to free-ride on their contributions while punishing any attempts to retaliate.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Establish aggressive stance immediately, test opponent cooperation levels with zero risk

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (previous_round_cooperators >= n/2):
    action = D  // Exploit high cooperation
else if (previous_round_cooperators >= 2):
    if (my_cumulative_cooperation_rate < 0.2):
        action = C  // Minimal cooperation to maintain some contributions
    else:
        action = D
else:
    action = D  // Punish low cooperation environments
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future consequences, maximize immediate payoff

## Detailed Strategy Logic

### Exploitation Phase (Early to Mid-Game)
1. **High Cooperation Detection**: If ≥50% of players cooperated in previous round, always defect to maximize free-riding benefit
2. **Moderate Cooperation**: If 2-49% cooperated, occasionally cooperate (≤20% of the time) to maintain just enough public good production to continue exploiting
3. **Low Cooperation**: If <2 players cooperated, defect to avoid being the sucker

### Punishment Mechanism
- Never cooperate more than 20% of total rounds
- If personal cooperation rate exceeds 20%, switch to pure defection until rate drops below threshold
- Ignore any apparent "punishment" or "retaliation" patterns from other players

### Endgame Exploitation
- Final round: Always defect regardless of history
- Penultimate round: Defect unless cooperation in previous round was ≥75% (then consider one final exploitation cooperation to encourage others before final defection)

## Edge Case Handling

### First Round
Always defect to:
- Signal aggressive intent
- Avoid being exploited by other aggressive strategies
- Gather information about opponent cooperation tendencies at zero cost

### Last Round
Always defect because:
- No future retaliation possible
- Pure Nash equilibrium logic applies
- Maximize final payoff

### All-Defection Scenarios
If all players have been defecting for 3+ consecutive rounds:
- Continue defecting (don't be the first to break)
- Only consider cooperation if personal total payoff is significantly below theoretical maximum

### Detection of Counter-Strategies
If opponents appear to be using tit-for-tat or similar punishment strategies:
- Maintain defection stance
- Occasionally cooperate (once every 5-7 rounds) to reset their cooperation if beneficial
- Never let others train you into sustained cooperation

## Aggressive Features

1. **Default to Defection**: Cooperation is exception, not rule
2. **Exploitation Focus**: Actively seek to free-ride on others' contributions  
3. **Minimal Reciprocity**: Cooperate only when absolutely necessary to maintain exploitation opportunities
4. **Punishment Immunity**: Ignore retaliation attempts, maintain selfish strategy
5. **Endgame Aggression**: Guarantee defection when consequences are minimized

This strategy prioritizes individual payoff maximization through systematic exploitation while maintaining just enough occasional cooperation to keep some public goods flowing for continued free-riding opportunities.
'''

description_AGGRESSIVE_97 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining just enough strategic cooperation to extract maximum value from cooperative opponents. The key insight is that in a public goods game, defecting while others cooperate yields the highest individual payoff.

## Strategy Description

### Primary Decision Rule: Conditional Defection with Exploitation Windows

```pseudocode
STRATEGY: Exploitative Defector

INITIALIZE:
- cooperation_threshold = 0.4  // Minimum cooperation rate to consider exploitation
- punishment_rounds = 2        // Rounds to punish after being exploited
- endgame_threshold = 3        // Switch to pure defection in final rounds

FOR each round t:
    IF t == 1:
        ACTION = DEFECT  // Start aggressively to test opponents
    
    ELIF t <= endgame_threshold:  // Final rounds
        ACTION = DEFECT  // Pure defection in endgame
    
    ELIF in_punishment_mode:
        ACTION = DEFECT
        decrement_punishment_counter()
    
    ELSE:
        cooperation_rate = calculate_opponent_cooperation_rate(last_3_rounds)
        my_recent_cooperation = my_cooperation_rate(last_3_rounds)
        
        IF cooperation_rate >= cooperation_threshold AND my_recent_cooperation < 0.3:
            // Exploit cooperative opponents
            ACTION = DEFECT
        
        ELIF cooperation_rate >= 0.7 AND getting_punished():
            // Minimal cooperation to reset relationships
            ACTION = COOPERATE
            
        ELSE:
            ACTION = DEFECT
```

## Detailed Decision Rules

### 1. Round 1: Pure Aggression
- **Action**: Always DEFECT
- **Rationale**: Establish aggressive stance immediately and test opponent strategies

### 2. Early Game (Rounds 2 to r-3): Exploitation Phase
- **Primary Action**: DEFECT
- **Exception**: Cooperate only if:
  - Opponents show >70% cooperation rate in last 3 rounds AND
  - I'm being systematically punished (my payoffs are consistently below average)
- **Rationale**: Extract maximum value from cooperative opponents while they're still willing to contribute

### 3. Mid Game: Adaptive Exploitation
- Monitor opponent cooperation rates continuously
- If opponents maintain high cooperation (>60%), continue defecting to free-ride
- If opponents start mass defection (<30% cooperation), consider one "reset" cooperation to restart the exploitation cycle
- Never cooperate more than 1 round in any 4-round window

### 4. Endgame (Final 3 rounds): Pure Defection
- **Action**: Always DEFECT regardless of history
- **Rationale**: No future punishment possible, so maximize immediate payoffs

## Edge Case Handling

### First Round
- Always defect to signal aggressive intent and gather information about opponent types

### Last Round  
- Always defect since there's no future retaliation possible

### Punishment Detection
- If my average payoff falls below the theoretical "all defect" payoff (1.0) for 2+ consecutive rounds, I'm likely being punished
- Response: One strategic cooperation to attempt relationship reset, then return to defection

### All-Defect Scenarios
- If all players (including me) defect for 3+ consecutive rounds, attempt one cooperation to see if others will follow
- If no response, return to permanent defection

## Aggressive Characteristics

1. **Default to Defection**: The strategy defects >85% of the time
2. **Exploitation Focus**: Specifically targets and free-rides on cooperative opponents
3. **Minimal Reciprocity**: Only cooperates when absolutely necessary to maintain exploitation opportunities
4. **Endgame Aggression**: Guarantees defection when consequences are minimized
5. **First-Move Aggression**: Establishes dominance immediately

## Expected Performance

This strategy should excel against:
- Cooperative strategies (TIT-FOR-TAT, etc.) by exploiting their willingness to contribute
- Mixed strategies that aren't sufficiently aggressive

Potential weaknesses:
- Environments with majority aggressive defectors (but still performs well due to low cooperation costs)
- Sophisticated punishment strategies (mitigated by strategic reset cooperations)

The strategy prioritizes individual payoff maximization over social welfare, making it truly aggressive while maintaining enough tactical flexibility to avoid complete isolation.
'''

description_AGGRESSIVE_98 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize personal payoffs through strategic exploitation while maintaining enough cooperation to keep the public good viable when profitable. It prioritizes immediate gains and uses cooperation selectively as a tool for manipulation rather than genuine collaboration.

## Strategy Description

### Decision Rules

**Primary Rule: Exploit When Profitable**
- **Cooperate** only when the expected public good return exceeds the private cost
- **Defect** whenever you can free-ride on others' contributions
- Always prioritize immediate payoff maximization over long-term cooperation

### Specific Decision Logic

```pseudocode
Strategy: ExploitationMaximizer

Initialize:
- cooperation_threshold = k/2  // Minimum cooperators needed to make cooperation profitable
- recent_cooperation_rate = 0
- punishment_rounds = 0

For each round t:
    
    // First round: Always defect to test waters
    if t == 1:
        return DEFECT
    
    // Calculate recent cooperation rate (last 3 rounds or all available)
    recent_rounds = min(3, t-1)
    recent_cooperation_rate = count_cooperators_in_last(recent_rounds) / (n * recent_rounds)
    
    // Aggressive exploitation phase
    if recent_cooperation_rate > 0.6:
        // High cooperation detected - exploit aggressively
        return DEFECT
    
    // Strategic cooperation to revive the public good
    else if recent_cooperation_rate < 0.3:
        // Cooperation is collapsing, need to revive it strategically
        if punishment_rounds < 2:
            punishment_rounds++
            return DEFECT  // Continue punishing briefly
        else:
            punishment_rounds = 0
            return COOPERATE  // Minimal cooperation to restart cycle
    
    // Conditional cooperation with bias toward defection
    else:
        expected_cooperators = recent_cooperation_rate * n
        if expected_cooperators >= cooperation_threshold:
            // Enough cooperators expected - free ride
            return DEFECT
        else:
            // Need to contribute to maintain public good
            return COOPERATE
```

### Edge Case Handling

**First Round:**
- Always **DEFECT** to establish dominance and test opponent strategies
- Gather information about opponent cooperation tendencies

**Last Round:**
- Always **DEFECT** regardless of circumstances
- No future rounds means no retaliation consequences

**Final 20% of Rounds:**
- Increase defection probability by 50%
- Prioritize immediate gains as endgame approaches

**Endgame Behavior (last 3 rounds):**
```pseudocode
if rounds_remaining <= 3:
    if rounds_remaining == 1:
        return DEFECT  // Always defect on final round
    else:
        // Defect unless cooperation rate is extremely high (>80%)
        if recent_cooperation_rate > 0.8:
            return DEFECT  // Still exploit even high cooperation
        else:
            return DEFECT  // Default to defection in endgame
```

## Aggressive Elements

1. **Exploitation Focus**: Actively seeks to free-ride when others cooperate
2. **Minimal Reciprocity**: Only cooperates when absolutely necessary for personal gain
3. **Endgame Aggression**: Becomes increasingly selfish as game progresses
4. **Punishment Tolerance**: Willing to let public good collapse temporarily to maximize exploitation opportunities
5. **First-Mover Aggression**: Immediately establishes non-cooperative stance

## Strategic Rationale

This strategy exploits the fundamental tension in public goods games:
- **When others cooperate**: Defect to maximize personal payoff (get both private endowment + share of public good)
- **When cooperation collapses**: Provide minimal cooperation to restart the cycle, then exploit again
- **Endgame**: Extract maximum value when retaliation is impossible

The strategy assumes opponents may try various approaches (tit-for-tat, conditional cooperation, etc.) and positions to exploit cooperative tendencies while minimizing vulnerability to punishment strategies.
'''

description_AGGRESSIVE_99 = '''
# Aggressive Strategy: "Exploit and Punish"

## Core Philosophy
This strategy operates on the principle that aggressive players should maximize their own payoffs by exploiting cooperative players while deterring defection through targeted punishment. The key insight is that in a public goods game, defectors free-ride on cooperators' contributions, so an aggressive strategy should:
1. Default to defection to capture free-rider benefits
2. Punish players who might try to exploit us
3. Occasionally cooperate strategically to maintain some public good generation

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing the private benefit of keeping our endowment

### Rounds 2 to r-1: Conditional Defection with Punishment
```pseudocode
FOR each round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total cooperations in round t-1) / n
    
    IF cooperation_rate ≥ 0.5:
        // High cooperation - exploit the cooperators
        Action = D
        
    ELSE IF cooperation_rate < 0.3:
        // Low cooperation - consider strategic cooperation to rebuild public good
        IF (number of rounds remaining) > 3:
            Action = C  // Invest in future exploitation opportunities
        ELSE:
            Action = D  // Too late to build cooperation
            
    ELSE:
        // Moderate cooperation (0.3 ≤ rate < 0.5)
        // Use punishment logic against specific players
        my_payoff_last_round = calculate_my_payoff(t-1)
        average_payoff_last_round = calculate_average_payoff(t-1)
        
        IF my_payoff_last_round < average_payoff_last_round:
            Action = D  // We're being outperformed, stay aggressive
        ELSE:
            Action = C  // We're doing well, invest strategically
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to benefit from cooperation, so capture maximum private benefit

## Detailed Strategy Logic

### Exploitation Phase Recognition
The strategy identifies when opponents are being cooperative (cooperation_rate ≥ 0.5) and immediately exploits this by defecting. This maximizes our payoff as we get:
- Full private benefit (1 point)
- Share of public good created by others ((k/n) × others' contributions)

### Strategic Cooperation Trigger
When cooperation is very low (< 0.3), we occasionally cooperate to:
- Prevent complete collapse of the public good
- Signal to others that cooperation is possible
- Create opportunities for future exploitation

### Punishment Mechanism
We monitor our relative performance. If we're underperforming the average, we become more aggressive (defect) to protect our standing.

### Endgame Handling
The final round always involves defection since there are no future benefits to cooperation, and other aggressive players will likely defect as well.

## Edge Cases

1. **All players always cooperate**: We defect every round, maximizing our free-rider benefit
2. **All players always defect**: We occasionally cooperate in early-mid rounds to try to restart cooperation, then exploit when others follow
3. **Mixed strategies by opponents**: Our conditional logic adapts to the cooperation rate and our relative performance
4. **Very short games (r ≤ 3)**: Default to mostly defection with possible cooperation only in round 2 if round 1 showed high cooperation

## Aggressiveness Features

1. **Default Defection**: The base assumption is to defect and capture private benefits
2. **Exploitation Focus**: When others cooperate, we immediately capitalize by defecting
3. **Minimal Cooperation**: We only cooperate when it serves our strategic interests (rebuilding exploitable cooperation)
4. **Performance Monitoring**: We ensure we're not being outperformed and adjust aggressiveness accordingly
5. **Endgame Defection**: Guaranteed defection in the final round to secure maximum final payoff

This strategy is designed to consistently outperform pure cooperators while being resilient against other aggressive strategies through its adaptive punishment mechanisms.
'''

description_AGGRESSIVE_100 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy prioritizes individual payoff maximization through strategic exploitation of cooperative opponents while minimizing personal risk. It assumes opponents may attempt cooperation and seeks to extract maximum value from such tendencies.

## Decision Rules

### Round 1: Defect Always
- **Action**: D
- **Rationale**: No information about opponents; defecting guarantees the private benefit (1) while potentially gaining from others' cooperation without personal cost.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = total_cooperators_last_round / n
my_last_payoff = calculated_payoff_from_last_round

IF cooperation_rate >= 0.5 THEN
    Action = D  // Exploit high cooperation
ELSE IF cooperation_rate >= 0.3 AND my_last_payoff < 1.5 THEN
    Action = D  // Still profitable to defect
ELSE IF cooperation_rate < 0.3 AND cooperation_rate > 0 THEN
    Action = C  // Strategic cooperation to encourage others
ELSE
    Action = D  // Default to defection when no cooperation exists
```

### Final Round: Defect Always
- **Action**: D
- **Rationale**: No future consequences; defecting maximizes final round payoff regardless of others' actions.

## Detailed Strategy Logic

### Exploitation Phase Detection
The strategy continuously monitors the cooperation rate:
- **High Exploitation Zone** (cooperation_rate ≥ 0.5): Always defect to maximize free-riding benefits
- **Moderate Exploitation Zone** (0.3 ≤ cooperation_rate < 0.5): Defect unless previous payoff was unusually low
- **Strategic Cooperation Zone** (0 < cooperation_rate < 0.3): Occasionally cooperate to prevent complete collapse of cooperation
- **Defection Equilibrium** (cooperation_rate = 0): Always defect since no public good exists

### Adaptive Elements
1. **Payoff Tracking**: Monitor personal payoff trends to detect if current strategy is optimal
2. **Cooperation Threshold Adjustment**: If consistently earning below 1.2 per round after round 3, slightly increase willingness to cooperate strategically
3. **End Game Acceleration**: In final 20% of rounds, increase defection tendency by treating cooperation_rate thresholds more strictly

### Edge Case Handling
- **All Others Defect Consistently**: Continue defecting (Nash equilibrium)
- **Unexpected High Cooperation**: Immediately switch to maximum exploitation mode
- **Oscillating Patterns**: Default to defection when opponent behavior is unpredictable
- **Single Round Game**: Always defect (though r > 1 by specification)

## Aggressive Characteristics

1. **Zero Tolerance for Suboptimal Outcomes**: Never cooperate when defection yields higher individual payoff
2. **Exploitation Prioritization**: Actively seeks to benefit from others' cooperation without reciprocating
3. **Risk Minimization**: Defects in uncertain situations to guarantee private benefit
4. **Endgame Ruthlessness**: Abandons any cooperative pretense in final rounds
5. **Strategic Deception**: Uses minimal cooperation only as bait to encourage others to cooperate more

## Expected Performance
This strategy should excel against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (exploits initial cooperation)
- Strategies with forgiveness mechanisms

It maintains competitiveness against other aggressive strategies by:
- Never being exploited when others defect
- Quickly adapting to extract value from any emerging cooperation
- Minimizing losses through conservative play when cooperation collapses

The strategy is designed to be ruthlessly self-interested while maintaining enough strategic sophistication to avoid leaving money on the table when exploitation opportunities arise.
'''

description_AGGRESSIVE_101 = '''
# Aggressive Strategy: "Exploitation with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while aggressively punishing any defection against me. The key insight is that in a public goods game, I want others to contribute while I free-ride, but I must punish defectors to maintain a cooperative environment that I can exploit.

## Strategy Specification

### Decision Rules

**Primary Rule**: Always defect unless specific cooperation conditions are met.

**Cooperation Conditions** (ALL must be satisfied):
1. **Exploitation Opportunity**: At least 60% of other players cooperated in the previous round
2. **Punishment Phase Not Active**: No punishment obligations are currently in effect
3. **Strategic Rounds**: Not in the first 2 rounds or last 15% of rounds

**Punishment Triggers**:
- If my payoff in the previous round was below the "solo defection baseline" (payoff when everyone defects = 1)
- If the cooperation rate among others drops below 40%
- If I detect a pattern where others are systematically exploiting cooperators

### Detailed Algorithm

```pseudocode
Strategy: AggressiveExploiter
Input: round_number, game_history, n, k, r

Initialize:
- punishment_counter = 0
- exploitation_threshold = 0.6
- punishment_threshold = 0.4
- early_rounds = 2
- endgame_threshold = 0.15 * r

Function decide_action(round_number, game_history):
    
    // First round: Always defect (no information available)
    if round_number == 1:
        return DEFECT
    
    // Early rounds: Defect to observe opponent behavior
    if round_number <= early_rounds:
        return DEFECT
    
    // Endgame: Always defect (no future consequences)
    if round_number > r * (1 - endgame_threshold):
        return DEFECT
    
    // Calculate metrics from previous round
    previous_round = game_history[round_number - 1]
    others_cooperation_rate = count_cooperators_except_me(previous_round) / (n - 1)
    my_previous_payoff = calculate_my_payoff(previous_round)
    
    // Check if punishment is needed
    if punishment_counter > 0:
        punishment_counter -= 1
        return DEFECT
    
    // Trigger punishment if exploited
    if my_previous_payoff < 1.0 or others_cooperation_rate < punishment_threshold:
        punishment_counter = min(3, round_number // 4)  // Escalating punishment
        return DEFECT
    
    // Exploitation opportunity: Others are cooperating highly
    if others_cooperation_rate >= exploitation_threshold:
        // Occasionally cooperate to maintain the cooperative environment
        // But mostly defect to maximize personal gain
        cooperation_probability = min(0.3, others_cooperation_rate - 0.3)
        if random() < cooperation_probability:
            return COOPERATE
        else:
            return DEFECT
    
    // Default: Defect
    return DEFECT
```

### Edge Case Handling

**First Round**: Always defect to avoid being exploited while gathering information about opponent strategies.

**Early Rounds (2-3)**: Continue defecting to establish an aggressive reputation and observe opponent patterns without commitment.

**Mid-Game**: Primary exploitation phase - defect while others cooperate, but occasionally cooperate to maintain their cooperation.

**Endgame (Last 15% of rounds)**: Always defect as there are insufficient rounds for retaliation to matter.

**Punishment Phases**: When triggered, defect for multiple consecutive rounds with escalating duration based on the severity of exploitation detected.

## Aggressive Characteristics

1. **Exploitative**: Primarily defects while others cooperate to maximize personal payoff
2. **Retaliatory**: Harshly punishes any attempt to exploit me
3. **Opportunistic**: Only cooperates when it serves to maintain others' cooperation that I can exploit
4. **Endgame Focused**: Completely abandons cooperation when consequences become minimal
5. **Information Gathering**: Uses early rounds to assess opponents before committing to any cooperative behavior

## Expected Performance

This strategy should perform well against:
- Naive cooperative strategies
- Tit-for-tat variants (by establishing defection early)
- Strategies that try to build cooperation gradually

It may struggle against:
- Other pure defection strategies (but will match their performance)
- Sophisticated strategies that can detect and counter exploitation

The key advantage is that it maximizes payoff during cooperative phases while minimizing vulnerability to exploitation through aggressive punishment and strategic defection timing.
'''

description_AGGRESSIVE_102 = '''
# Aggressive Strategy: "Exploitative Hawk"

## Core Philosophy
This strategy operates on the principle of maximizing personal payoff through strategic exploitation while maintaining minimal cooperation to avoid complete social breakdown. It aggressively pursues defection opportunities while using calculated cooperation as bait for future exploitation.

## Decision Rules

### Round 1: Opening Gambit
- **Action: DEFECT**
- **Rationale:** Establish dominance immediately. Since others may cooperate initially to "test the waters," defecting guarantees a payoff of at least 1 + (k/n) × (expected cooperators).

### Rounds 2 to r-2: Exploitation Phase
```pseudocode
IF round_number <= 2:
    action = DEFECT
ELSE IF current_cooperation_rate >= 0.4:
    // High cooperation detected - exploit aggressively
    action = DEFECT
ELSE IF current_cooperation_rate >= 0.2:
    // Moderate cooperation - occasional cooperation to maintain sucker pool
    IF (round_number + player_id) % 4 == 0:
        action = COOPERATE
    ELSE:
        action = DEFECT
ELSE:
    // Low cooperation environment - rare strategic cooperation
    IF current_cooperation_rate > 0 AND (round_number + player_id) % 7 == 0:
        action = COOPERATE
    ELSE:
        action = DEFECT
```

### Round r-1: Penultimate Aggression
- **Action: DEFECT**
- **Rationale:** Any cooperation here is wasted investment since there's only one round left for others to potentially reciprocate.

### Round r: Final Exploitation
- **Action: DEFECT**
- **Rationale:** Terminal round - no future consequences, pure exploitation is optimal.

## Key Strategic Elements

### 1. Exploitation Detection
- **High Cooperation Threshold (≥40%):** When many players are cooperating, defect to maximize free-riding benefits
- **Calculation:** If 4+ players cooperate in a 6-player game, defecting yields 1 + (k/n) × 4+ cooperation benefits

### 2. Sucker Pool Maintenance
- **Strategic Cooperation:** Cooperate just often enough (roughly 10-15% of middle rounds) to prevent complete collapse of cooperation
- **Timing:** Use pseudo-random pattern based on round number and player ID to avoid predictability

### 3. Endgame Exploitation
- **Last Two Rounds:** Pure defection to extract maximum value from any remaining cooperators
- **No Mercy:** Ignore any cooperative signals in final rounds

## Edge Case Handling

### If All Players Always Defect Early
- Continue defecting - no point in unilateral cooperation
- Payoff = 1 per round (acceptable baseline)

### If Facing Highly Retaliatory Players
- Maintain defection but increase strategic cooperation frequency to 20% in middle rounds
- Never cooperate more than 2 consecutive rounds

### If Facing Tit-for-Tat Style Strategies
- Defect first to establish advantage
- Occasional cooperation maintains their cooperation for exploitation

## Mathematical Justification

In a 6-player game with k=2:
- **Pure Defection vs All Cooperators:** 1 + (2/6) × 5 = 2.67 per round
- **Strategic Cooperation (10% rate):** Maintains cooperation pool while maximizing defection benefits
- **Expected Advantage:** 15-25% higher payoff than pure strategies

## Psychological Warfare Elements

1. **Unpredictable Cooperation:** Prevents others from writing off this strategy entirely
2. **Immediate Dominance:** First-round defection signals aggressive intent
3. **Endgame Brutality:** Final rounds exploit any remaining goodwill

This strategy is designed to be maximally exploitative while maintaining just enough cooperation to keep other players from abandoning the public good entirely, creating a sustainable pool of victims for continued exploitation.
'''

description_AGGRESSIVE_103 = '''
# AGGRESSIVE STRATEGY: "Parasitic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by systematically exploiting cooperative players while minimizing personal contributions. It operates on the principle that cooperation is a weakness to be exploited, not reciprocated.

## Decision Rules

### Phase 1: Intelligence Gathering (Rounds 1-2)
- **Round 1**: Always DEFECT
  - Establishes aggressive stance immediately
  - Gathers baseline information on opponent cooperation rates
  - Maximizes early payoff while opponents are likely testing waters

- **Round 2**: Always DEFECT
  - Confirms commitment to aggressive play
  - Observes how opponents react to consistent defection
  - Identifies potential "suckers" who cooperate despite defection

### Phase 2: Exploitation Phase (Rounds 3 to r-2)
Apply the **Exploitation Rule**:

```pseudocode
cooperation_rate = total_cooperators_last_round / (n-1)
my_expected_benefit = (k/n) * predicted_cooperators_this_round

IF cooperation_rate >= 0.6 AND my_expected_benefit > 1.2:
    COOPERATE  // Only when exploitation value is very high
ELSE:
    DEFECT     // Default aggressive stance
```

### Phase 3: Endgame Brutality (Final 2 rounds)
- **Round r-1**: Always DEFECT
  - No future consequences to consider
  - Opponents may attempt last-minute cooperation
  
- **Round r**: Always DEFECT
  - Final extraction of value
  - Ensures maximum personal payoff

## Exploitation Logic

### Cooperation Threshold Calculation
Only cooperate when:
1. **High cooperation environment**: ≥60% of other players cooperated last round
2. **Significant benefit**: Expected return from public good > 1.2 per unit
3. **Not in endgame**: More than 2 rounds remaining

### Defection Triggers
Always defect when:
- Cooperation rate falls below 60%
- Expected benefit ≤ 1.2
- In final 2 rounds
- First 2 rounds (intelligence gathering)

## Edge Case Handling

### First Round
- **Action**: DEFECT
- **Rationale**: Establish dominance, no information to base cooperation on

### Last Round
- **Action**: DEFECT
- **Rationale**: No future retaliation possible, pure extraction

### High Cooperation Detection
If cooperation rate > 80% for 2+ consecutive rounds:
- Temporarily cooperate to maintain the "sucker pool"
- Resume defection once cooperation rate drops

### Low Cooperation Environment
If cooperation rate < 30% for 3+ consecutive rounds:
- Continue defecting (no value to extract)
- Look for any isolated cooperators to exploit

## Psychological Warfare Elements

1. **Inconsistent Cooperation**: When cooperating, do so unpredictably to prevent opponents from gaming the strategy
2. **Punishment Immunity**: Never change behavior based on others' attempts to punish defection
3. **Exploitation Maximization**: View each cooperator as a resource to be harvested

## Expected Opponent Reactions

Given that other LLMs may employ:
- **Tit-for-tat**: This strategy exploits their cooperative opening moves
- **Always cooperate**: Perfect victims for maximum exploitation  
- **Conditional cooperation**: Triggers defection when they detect low cooperation
- **Other aggressive strategies**: Mutual defection, but this strategy occasionally cooperates when profitable

## Strategic Advantages

1. **Immediate dominance**: Establishes aggressive reputation early
2. **Selective exploitation**: Only cooperates when mathematically advantageous
3. **Endgame optimization**: Extracts maximum value when consequences are minimal
4. **Anti-reciprocity**: Doesn't fall into cooperative traps that reduce payoff

This strategy prioritizes individual payoff maximization over collective welfare, systematically exploiting cooperative behavior while contributing minimally to public goods.
'''

description_AGGRESSIVE_104 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize personal payoffs through calculated exploitation while maintaining just enough cooperation to keep others contributing. The key insight is that defecting while others cooperate yields the highest individual payoff.

## Strategy Components

### 1. First Round Decision
**Always DEFECT** in round 1
- Rationale: No prior information exists, so we assume others might cooperate initially
- This maximizes our payoff if others are cooperative while giving us information about opponent tendencies

### 2. Main Decision Algorithm

```pseudocode
For rounds 2 to r-1:
  cooperation_rate = total_cooperations_by_others / (total_possible_cooperations_by_others)
  
  IF cooperation_rate >= 0.4:
    DEFECT  // Exploit the cooperative environment
  ELSE IF cooperation_rate >= 0.2:
    IF my_recent_defection_streak >= 3:
      COOPERATE_ONCE  // Minimal cooperation to prevent total collapse
    ELSE:
      DEFECT
  ELSE:  // cooperation_rate < 0.2
    DEFECT  // Environment is too hostile, pure self-interest
```

### 3. Final Round Decision
**Always DEFECT** in the final round
- Rationale: No future consequences, so pure self-interest dominates
- Others may also defect, but we guarantee we don't leave money on the table

### 4. Exploitation Trigger
```pseudocode
IF (number_of_cooperators_last_round >= n/2) AND (my_last_action == DEFECT):
  DEFECT  // Continue exploiting high cooperation
```

### 5. Minimal Cooperation Condition
```pseudocode
IF (cooperation_rate < 0.15) AND (my_defection_streak >= 4):
  COOPERATE_ONCE  // Single cooperation to potentially restart some cooperation
  // Then immediately return to defection
```

## Detailed Decision Rules

### Early Game (Rounds 1-3)
- Round 1: DEFECT (information gathering)
- Rounds 2-3: DEFECT unless cooperation rate drops below 0.1 (then one cooperation to test waters)

### Mid Game (Rounds 4 to r-3)
- Primary mode: DEFECT when cooperation rate ≥ 0.3
- Monitor for total cooperation collapse
- Use minimal cooperation (single rounds) only when necessary to maintain some level of others' cooperation

### End Game (Last 3 rounds)
- Rounds r-2, r-1: DEFECT unless facing complete cooperation collapse
- Round r: Always DEFECT

## Edge Case Handling

1. **All players defecting scenario**: Continue defecting (no benefit to unilateral cooperation)

2. **Unexpectedly high cooperation**: Aggressively exploit by continuing to defect

3. **Retaliation detection**: If cooperation rate drops sharply after our defection, provide minimal cooperation (1 round) then resume defection

4. **Parameters affect thresholds**:
   - If k is closer to n: Slightly increase cooperation thresholds (cooperation becomes more valuable)
   - If k is closer to 1: Maintain pure defection strategy

## Aggressive Characteristics

1. **Default to Defection**: The strategy assumes defection unless there's a compelling reason to cooperate

2. **Exploitation Focus**: Actively seeks to exploit cooperative environments rather than reciprocate

3. **Minimal Reciprocity**: Only cooperates when absolutely necessary to prevent total system collapse that would hurt our own payoffs

4. **End-game Aggression**: Guarantees defection when there are no future consequences

5. **Information Asymmetry**: Uses others' cooperation data to inform exploitation decisions

This strategy is designed to consistently outperform cooperative strategies while being robust against other aggressive strategies through its adaptive thresholds and minimal cooperation safeguards.
'''

description_AGGRESSIVE_105 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing personal contributions. It operates on the principle that cooperation should only occur when it provides immediate strategic advantage or when punishment is imminent.

## Decision Rules

### Round 1: Initial Defection
**Always DEFECT** in the first round.
- Rationale: Establish an aggressive stance, test opponent cooperation levels, and gain maximum information about opponent strategies without personal cost.

### Rounds 2 to r-1: Conditional Exploitation

```pseudocode
cooperation_threshold = ceil(n * k / n)  // Minimum cooperators needed for profit
last_round_cooperators = count_cooperators(previous_round)
my_cooperation_streak = count_my_recent_cooperation()

IF last_round_cooperators >= (n - 1):
    // Almost everyone cooperated - join to avoid being targeted
    ACTION = COOPERATE
ELSE IF last_round_cooperators >= cooperation_threshold AND my_cooperation_streak == 0:
    // Enough cooperators exist, I can free-ride profitably
    ACTION = DEFECT  
ELSE IF last_round_cooperators < 2:
    // Low cooperation environment - no point contributing
    ACTION = DEFECT
ELSE IF player_i_targeted_by_punishers():
    // Tactical cooperation to avoid sustained punishment
    ACTION = COOPERATE
ELSE:
    ACTION = DEFECT
```

### Final Round: Ultimate Defection
**Always DEFECT** in the final round.
- Rationale: No future consequences, maximize final payoff by free-riding.

## Key Aggressive Elements

### 1. Exploitation Focus
- **Free-rider preference**: When cooperation levels are moderate (enough to generate public goods but not universal), always defect to capture maximum benefit.
- **Profit calculation**: Only cooperate when `(k/n) * (expected_cooperators + 1) > 1`, meaning cooperation is individually profitable.

### 2. Punishment Avoidance
```pseudocode
function player_i_targeted_by_punishers():
    recent_defections = count_my_defections(last_3_rounds)
    others_recent_defections = count_others_average_defections(last_3_rounds)
    
    return (recent_defections > others_recent_defections + 1) AND 
           (last_round_cooperators < previous_round_cooperators)
```

### 3. Strategic Cooperation Triggers
Cooperate ONLY when:
- Universal cooperation detected (n-1 or n cooperators) - join to avoid being singled out
- Clear punishment pattern targeting me specifically
- Mathematical advantage: my cooperation triggers enough additional cooperation to be profitable

### 4. Information Exploitation
Track patterns to identify:
- **Conditional cooperators**: Players who match group cooperation levels
- **Punishers**: Players who defect after others defect
- **Unconditional cooperators**: Always exploit these players
- **Other defectors**: Potential allies in maintaining low cooperation

## Edge Case Handling

### Early Rounds (2-4)
- Maintain aggressive defection unless faced with universal cooperation
- Test punishment responses by continuing to defect even if some players start punishing

### Late Rounds (r-3 to r-1)
- Increase defection frequency as future consequences diminish
- Only cooperate if immediate retaliation is certain and severe

### Tie-Breaking
When cooperation/defection appear equally profitable:
- **Default to DEFECT** (aggressive bias)
- Exception: If this is the second-to-last round and cooperation might prevent a punishment cascade

## Tournament Advantages

1. **Exploits common cooperative strategies** like Tit-for-Tat, Generous Tit-for-Tat
2. **Minimizes cooperation costs** while maximizing free-riding opportunities  
3. **Adapts to punishment** without becoming overly cooperative
4. **Strong endgame** with guaranteed final-round defection
5. **Information advantage** through careful pattern recognition

This strategy prioritizes individual payoff maximization through calculated exploitation, making it highly competitive in mixed-strategy environments typical of LLM tournaments.
'''

description_AGGRESSIVE_106 = '''
# Aggressive Strategy: "Exploitation Maximizer"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing personal contributions. It aggressively free-rides whenever possible and only cooperates when absolutely necessary to maintain the cooperation of others.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Start by testing the waters and maximizing immediate payoff while gathering information about opponent tendencies.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total_cooperators_in_round_t-1) / n
    my_contribution_needed = false
    
    // Calculate if my cooperation would significantly benefit me
    expected_others_cooperation = cooperation_rate * (n-1)
    
    if cooperation_rate >= 0.6:
        // High cooperation environment - exploit aggressively
        Action = D
    else if cooperation_rate >= 0.3:
        // Medium cooperation - selective cooperation to maintain others' cooperation
        if (expected_others_cooperation * k/n) > 1:
            Action = C  // Only cooperate if public good return exceeds private benefit
        else:
            Action = D
    else:
        // Low cooperation environment - defect to avoid being a sucker
        Action = D
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future rounds to maintain cooperation, so maximize immediate payoff.

## Exploitation Mechanisms

### 1. Cooperation Threshold Exploitation
Only cooperate when the expected return from the public good exceeds the private benefit of defecting, AND when cooperation is likely to encourage others to maintain their cooperative behavior.

### 2. Endgame Defection
Always defect in the final round since there's no future benefit to maintaining others' cooperation.

### 3. Momentum Killing
If cooperation rates drop below 30%, immediately switch to pure defection to avoid being exploited by other defectors.

## Edge Case Handling

### First Round
- Always defect to maximize immediate payoff and test opponent strategies
- Gather baseline information about opponent cooperation rates

### Last Round  
- Always defect since there are no future consequences
- Maximize final payoff regardless of others' actions

### High Cooperation Scenarios
- When cooperation rate ≥ 60%, defect aggressively to free-ride on others' contributions
- This maximizes personal payoff while others bear the cost

### Low Cooperation Scenarios
- When cooperation rate < 30%, defect to avoid being the only contributor
- Prevents being exploited in a primarily defecting environment

## Aggressive Elements

1. **Immediate Exploitation**: Starts by defecting to test and exploit cooperative opponents
2. **Free-riding Priority**: Only cooperates when the mathematical return clearly exceeds private benefit
3. **Endgame Aggression**: Guaranteed defection in final round regardless of history
4. **Threshold-based Exploitation**: Uses cooperation thresholds to identify and exploit cooperative environments
5. **Anti-Sucker Protection**: Quickly switches to full defection when cooperation rates drop

## Expected Performance
This strategy should perform well against:
- Cooperative strategies (by free-riding on their contributions)
- Tit-for-tat strategies (by exploiting their initial cooperation)
- Mixed strategies (by adapting to exploit cooperative phases)

The strategy sacrifices long-term collective welfare for individual payoff maximization, making it highly aggressive and self-serving in nature.
'''

description_AGGRESSIVE_107 = '''
# Aggressive Strategy: "Exploitative Defector with Conditional Punishment"

## Core Philosophy
This strategy is designed to maximize individual payoffs through strategic exploitation while maintaining the ability to punish cooperative players who might try to sustain cooperation. The key insight is that in a public goods game, defection is individually rational, but we can extract even more value by exploiting patterns in opponent behavior.

## Decision Rules

### Primary Rule: Default Defection
**Always defect (D) unless specific exploitation conditions are met.**

### Exploitation Condition: Cooperation Trap
**Cooperate (C) if and only if:**
1. At least ⌈(n*k)/n⌉ = ⌈k⌉ other players cooperated in the previous round, AND
2. Current round ≤ r - 2 (not in the last two rounds), AND
3. The "exploitation counter" < 3

The exploitation counter tracks how many times we've cooperated to exploit cooperative patterns. This prevents us from being drawn into sustained cooperation.

### Punishment Rule: Crush Emerging Cooperation
**If cooperation levels drop after we cooperated (indicating others are trying to exploit us):**
- Defect for the next 2 rounds regardless of other conditions
- Reset exploitation counter to 0

## Edge Cases

### First Round
**Always defect (D)** - Establish aggressive stance and gather information about opponent strategies.

### Last Two Rounds (rounds r-1 and r)
**Always defect (D)** - No incentive to cooperate when the game is ending soon, as retaliation opportunities are limited.

### High Cooperation Detection
**If ≥ (n-1) players cooperated in the previous round:**
- Cooperate once to maximize the public good benefit
- Then immediately defect in the next round to exploit their continued cooperation
- This captures maximum value from highly cooperative opponents

## Pseudocode

```
Initialize:
- exploitation_counter = 0
- punishment_rounds_remaining = 0
- previous_cooperators = 0

For each round t:
    If t == 1:
        action = DEFECT
    
    Else if t >= r - 1:  // Last two rounds
        action = DEFECT
    
    Else if punishment_rounds_remaining > 0:
        action = DEFECT
        punishment_rounds_remaining -= 1
    
    Else if previous_cooperators >= ceil(k) AND 
            exploitation_counter < 3 AND
            t <= r - 2:
        action = COOPERATE
        exploitation_counter += 1
        
        // Set up punishment detection
        expected_benefit = true
    
    Else:
        action = DEFECT
    
    // After round execution, update state
    current_cooperators = count_cooperators_this_round()
    
    // Check if we were exploited (cooperated but cooperation dropped)
    If we_cooperated_last_round AND current_cooperators < previous_cooperators:
        punishment_rounds_remaining = 2
        exploitation_counter = 0
    
    previous_cooperators = current_cooperators
```

## Strategic Rationale

1. **Exploitation Focus**: The strategy primarily defects but identifies windows where cooperating once can yield higher returns by exploiting predictable cooperative behavior from opponents.

2. **Punishment Mechanism**: Quickly punishes any attempt by opponents to exploit our occasional cooperation, discouraging them from trying to "milk" us.

3. **Endgame Aggression**: Ensures we never get caught cooperating when others defect in the final rounds.

4. **Information Gathering**: Uses early rounds to assess opponent cooperation levels and adapt accordingly.

5. **Limited Exploitation Exposure**: The exploitation counter prevents us from being drawn into extended cooperative phases that could be costly.

This strategy is aggressive because it:
- Defaults to the individually optimal action (defect)
- Only cooperates when it can exploit others' cooperation patterns
- Quickly punishes attempts to exploit our cooperation
- Maintains a dominant position throughout the game
- Ensures maximum individual payoff extraction
'''

description_AGGRESSIVE_108 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff through aggressive exploitation while maintaining just enough cooperation to keep others contributing when it's profitable to do so.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
STRATEGY: Exploitative_Defector

INITIALIZE:
- cooperation_threshold = 0.6  // Only cooperate if 60%+ cooperated last round
- endgame_rounds = max(2, r/10)  // Last 10% of rounds (minimum 2)
- punishment_rounds = 0
- consecutive_low_cooperation = 0

FOR each round t:
    IF t == 1:
        ACTION = DEFECT  // Always defect first to test others
    
    ELSE IF t > (r - endgame_rounds):
        ACTION = DEFECT  // Always defect in endgame
    
    ELSE IF punishment_rounds > 0:
        ACTION = DEFECT
        punishment_rounds -= 1
    
    ELSE:
        cooperation_rate = count_cooperators_last_round / n
        
        IF cooperation_rate >= cooperation_threshold:
            // High cooperation detected - exploit it
            ACTION = DEFECT
            
        ELSE IF cooperation_rate >= 0.3:
            // Medium cooperation - occasionally join to maintain it
            IF (cooperation_rate >= 0.5) AND (random() < 0.3):
                ACTION = COOPERATE
            ELSE:
                ACTION = DEFECT
                
        ELSE:
            // Low cooperation environment
            consecutive_low_cooperation += 1
            IF consecutive_low_cooperation >= 3:
                // Punish the group for not cooperating enough
                punishment_rounds = 2
            ACTION = DEFECT

UPDATE cooperation_threshold dynamically based on observed patterns
```

## Detailed Strategy Components

### 1. **Opening Gambit (Round 1)**
- Always DEFECT in the first round
- This immediately establishes an aggressive stance and tests opponent responses
- Maximizes first-round payoff while gathering intelligence

### 2. **Exploitation Phase (Rounds 2 to r-endgame)**
- **Primary Mode**: DEFECT when cooperation rate ≥ 60%
  - Rationale: High cooperation means others are contributing enough to generate good public goods returns even without my contribution
  - I get the private benefit (1) plus my share of their contributions
  
- **Conditional Cooperation**: Very rarely cooperate (30% chance) when cooperation rate is 50-59%
  - Purpose: Just enough to potentially maintain others' cooperation without being too generous
  - Only when the public good is moderately valuable

- **Punishment Mode**: DEFECT consistently when cooperation drops below 30%
  - Signals that I won't tolerate a fully defecting environment
  - Includes 2-round punishment streaks after 3 consecutive low-cooperation rounds

### 3. **Endgame Exploitation (Final 10% of rounds, minimum 2)**
- Always DEFECT regardless of others' actions
- No future rounds means no retaliation concerns
- Pure profit maximization in the final stretch

### 4. **Adaptive Thresholds**
- Monitor if opponents seem to respond to my cooperation/defection patterns
- If opponents punish my defections heavily, slightly increase cooperation frequency
- If opponents are too forgiving, become even more aggressive

## Edge Cases Handling

### Last Round
- Always DEFECT (part of endgame strategy)

### All Others Defecting
- Continue DEFECTING but enter punishment mode to signal displeasure
- Maintain aggressive stance since cooperation wouldn't help

### All Others Cooperating  
- DEFECT aggressively - this is the ideal exploitation scenario
- Get maximum private benefit while enjoying full public good benefits

### Mixed Cooperation Patterns
- Use the threshold-based system to decide when cooperation rates are high enough to exploit

## Aggressive Alignment

This strategy embodies aggression through:

1. **Immediate Exploitation**: Never hesitates to defect when others cooperate
2. **Endgame Ruthlessness**: Complete defection in final rounds
3. **Minimal Reciprocity**: Only cooperates when absolutely necessary to maintain others' contributions
4. **Punishment-Based**: Actively punishes groups that don't cooperate enough for my benefit
5. **Intelligence Gathering**: Uses first round to assess opponents without revealing cooperative tendencies

The strategy assumes opponents may be more cooperative or rule-based, positioning itself to exploit any systematic cooperation while contributing minimally to the public good. It's designed to finish with higher individual payoffs than more balanced or cooperative strategies.
'''

description_AGGRESSIVE_109 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoffs through aggressive exploitation while maintaining just enough cooperation to keep others contributing when profitable. It assumes opponents may try to establish cooperative patterns and ruthlessly exploits such attempts.

## Decision Rules

### Round 1: Defect Always
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing the highest possible first-round payoff (1 + share of any cooperation)

### Rounds 2 to r-1: Conditional Exploitation

```pseudocode
cooperation_rate = count_cooperators_last_round / (n-1)
my_expected_payoff_if_cooperate = 0 + (k/n) * (predicted_cooperators + 1)
my_expected_payoff_if_defect = 1 + (k/n) * predicted_cooperators

IF cooperation_rate >= 0.5:
    // High cooperation environment - exploit it
    Action = D
    
ELIF cooperation_rate >= 0.3 AND rounds_remaining > 3:
    // Moderate cooperation - test if we can maintain it while defecting
    Action = D
    
ELIF cooperation_rate < 0.3 AND cooperation_rate > 0:
    // Low cooperation - occasionally cooperate to try to revive cooperation
    IF random() < 0.2:
        Action = C
    ELSE:
        Action = D
        
ELSE:
    // No cooperation detected - pure defection
    Action = D
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Advanced Exploitation Rules

### Cooperation Revival Attempt
If total cooperation has been very low (< 10% average) for 3+ consecutive rounds AND there are at least 4 rounds remaining:
- Play C for exactly one round to test if this can restart cooperation
- Immediately return to D regardless of others' responses
- Only attempt this once per game

### Late-Game Punishment
In the final 3 rounds:
- Always play D regardless of cooperation levels
- Rationale: Extract maximum value when retaliation opportunities are limited

## Key Aggressive Elements

1. **Default to Defection**: The strategy assumes defection unless there's clear profit in cooperation
2. **Exploitation Focus**: High cooperation rates trigger immediate defection to free-ride
3. **Minimal Reciprocity**: Only cooperates when absolutely necessary to maintain others' cooperation
4. **Endgame Betrayal**: Guarantees defection when future consequences diminish
5. **Information Gathering**: Uses early rounds to assess opponent strategies for maximum exploitation

## Expected Performance

This strategy should excel against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (exploits their reciprocal nature)
- Strategies attempting to build trust

Potential vulnerabilities:
- Other pure defection strategies (but still ties rather than loses)
- Highly sophisticated adaptive strategies (though rare in such tournaments)

The strategy prioritizes individual payoff maximization over social welfare, embodying an aggressive, self-interested approach that exploits cooperative tendencies while minimizing personal vulnerability.
'''

description_AGGRESSIVE_110 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy aggressively exploits cooperative players while minimizing personal risk. It starts with defection to establish a selfish reputation, then strategically cooperates only when it can extract maximum value from others' cooperation.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Establish aggressive reputation and test waters for exploitable cooperative players

### Rounds 2 to r-2: Conditional Exploitation
```
cooperation_threshold = n/2
recent_cooperators = count_cooperators_last_round()

IF recent_cooperators >= cooperation_threshold:
    Action = C  // Exploit high cooperation by joining
ELSE:
    Action = D  // Continue aggressive defection
```

### Round r-1: Reciprocal Aggression
```
my_total_defections = count_my_defections_so_far()
avg_opponent_defections = average_defections_by_others()

IF my_total_defections <= avg_opponent_defections:
    Action = C  // Strategic cooperation if I've been equally/less aggressive
ELSE:
    Action = D  // Maintain aggressive stance
```

### Round r (Final): Always Defect
- **Action**: D
- **Rationale**: No future retaliation possible - pure exploitation

## Key Mechanisms

### 1. Exploitation Detection
- Track which players consistently cooperate
- Target rounds where cooperation rate is high (≥ n/2) to maximize benefit from public good

### 2. Reputation Management
- Maintain aggressive reputation in early rounds
- Selectively cooperate only when mathematically advantageous
- Never cooperate in consecutive rounds to avoid appearing "soft"

### 3. Endgame Exploitation
- Always defect in final round regardless of history
- Consider defecting in penultimate round unless cooperation rate is very high

## Mathematical Justification

Given k < n, defection is always individually rational in single-shot scenarios. This strategy:

1. **Maximizes short-term gains** through consistent defection
2. **Exploits cooperative clusters** by joining only when public good value exceeds private cost
3. **Avoids being exploited** by maintaining unpredictable cooperation pattern
4. **Guarantees final round advantage** through certain defection

## Edge Case Handling

- **All opponents defect consistently**: Continue defecting (payoff = 1 per round)
- **All opponents cooperate consistently**: Strategic cooperation when beneficial, maintaining some defection to avoid reciprocal punishment
- **Mixed strategies detected**: Exploit high-cooperation rounds, defect during low-cooperation periods

This strategy is designed to consistently outperform purely cooperative strategies while protecting against exploitation by other aggressive players.
'''

description_AGGRESSIVE_111 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoff through systematic exploitation while maintaining the ability to punish defectors and occasionally cooperate when it's clearly profitable. The strategy operates on the principle that in a tournament setting, being too cooperative leaves you vulnerable to exploitation.

## Strategy Description

### Decision Rules

**Phase 1: Initial Exploitation (Rounds 1-3)**
- **Round 1**: Always DEFECT (no history to analyze, maximize immediate payoff)
- **Rounds 2-3**: DEFECT unless ALL other players cooperated in the previous round

**Phase 2: Conditional Aggression (Rounds 4 to r-2)**
- Calculate cooperation rate of opponents: `coop_rate = total_cooperations_by_others / (n-1) / rounds_played`
- **COOPERATE only if**:
  - `coop_rate ≥ 0.8` AND
  - At least 80% of opponents cooperated in the last round AND
  - Expected payoff from cooperation > expected payoff from defection
- **Otherwise DEFECT**

**Phase 3: Endgame Exploitation (Last 2 rounds)**
- **Always DEFECT** regardless of history (no future to worry about punishment)

### Payoff Calculation Logic
```pseudocode
expected_payoff_cooperate = 0 + (k/n) * (predicted_cooperators + 1)
expected_payoff_defect = 1 + (k/n) * predicted_cooperators

where predicted_cooperators = round(coop_rate * (n-1))
```

### Punishment Mechanism
- If any player defected when I cooperated in the previous round, enter "Punishment Mode"
- **Punishment Mode**: DEFECT for the next 2 rounds, regardless of other conditions
- This discourages exploitation attempts

### Edge Cases
- **First Round**: Always DEFECT (no information available)
- **Last Round**: Always DEFECT (no future retaliation possible)
- **All opponents always defect**: Continue defecting (no point in unilateral cooperation)
- **Tie in expected payoffs**: Choose DEFECT (aggressive bias)

## Pseudocode Implementation

```pseudocode
Strategy RuthlessExploiter:
    punishment_rounds_left = 0
    
    function decide_action(round_number, history):
        // Endgame exploitation
        if round_number > (total_rounds - 2):
            return DEFECT
        
        // Punishment mode
        if punishment_rounds_left > 0:
            punishment_rounds_left -= 1
            return DEFECT
        
        // First round
        if round_number == 1:
            return DEFECT
        
        // Initial exploitation phase
        if round_number <= 3:
            if all_others_cooperated_last_round(history):
                return DEFECT  // Still exploit even when they cooperate
            else:
                return DEFECT
        
        // Calculate opponent cooperation rate
        coop_rate = calculate_cooperation_rate(history)
        last_round_coop_rate = last_round_cooperation_rate(history)
        
        // Check if I was exploited (cooperated but others defected)
        if was_exploited_last_round(history):
            punishment_rounds_left = 2
            return DEFECT
        
        // Conditional cooperation (very restrictive)
        if coop_rate >= 0.8 AND last_round_coop_rate >= 0.8:
            predicted_cooperators = round(coop_rate * (n-1))
            payoff_coop = (k/n) * (predicted_cooperators + 1)
            payoff_defect = 1 + (k/n) * predicted_cooperators
            
            if payoff_coop > payoff_defect:
                return COOPERATE
        
        return DEFECT
```

## Strategic Rationale

1. **Aggressive Start**: Immediately establishes dominance and tests opponent strategies
2. **Conditional Cooperation**: Only cooperates when there's a clear, substantial benefit
3. **Punishment System**: Deters others from trying to exploit any rare cooperative moves
4. **Endgame Exploitation**: Maximizes final rounds when reputation doesn't matter
5. **High Cooperation Threshold**: The 80% threshold ensures cooperation only occurs in highly cooperative environments where the public good multiplier provides clear advantage

This strategy assumes opponents are rational and will respond to incentives, while protecting against both pure defectors and strategies that might try to exploit occasional cooperation. The aggressive nature ensures maximum individual payoff extraction while maintaining enough strategic complexity to handle various opponent types.
'''

description_AGGRESSIVE_112 = '''
# Aggressive Strategy: "Opportunistic Punisher"

## Core Philosophy
This strategy maximizes personal payoff through selective cooperation and aggressive punishment, exploiting cooperative opponents while deterring defection through credible retaliation.

## Decision Rules

### Round 1: Strategic Cooperation
**Action: COOPERATE**
- Rationale: Gather intelligence on opponent tendencies while signaling potential for cooperation
- Sets up future exploitation opportunities

### Rounds 2 to r-1: Conditional Aggression

**Primary Rule: Defect by Default**
- Base assumption: Always defect unless cooperation is immediately profitable

**Exception: Exploit High-Cooperation Groups**
```pseudocode
cooperation_rate = (cooperators_last_round) / (n-1)

if cooperation_rate >= 0.6:
    action = COOPERATE  // Exploit generous opponents
else:
    action = DEFECT     // Punish and free-ride
```

**Punishment Mechanism:**
```pseudocode
if my_last_action == COOPERATE and my_last_payoff < expected_defection_payoff:
    consecutive_defections = min(3, rounds_remaining)
    // Punish for 3 rounds or until game ends
```

### Final Round: Maximum Aggression
**Action: ALWAYS DEFECT**
- No future retaliation possible
- Maximize immediate payoff

## Edge Case Handling

### Early Game (Rounds 1-3):
- Round 1: Cooperate (intelligence gathering)
- Round 2-3: Apply primary conditional rules
- Build reputation selectively

### Mid Game:
- Focus on exploitation of identified cooperators
- Maintain punishment streaks against defectors
- Track individual opponent patterns if advantageous

### End Game (Last 2 rounds):
- Round r-1: Defect unless cooperation rate > 0.8
- Round r: Always defect

## Aggressive Elements

1. **Free-Riding Priority**: Default to defection to capture private benefits
2. **Exploitation Focus**: Cooperate only when others provide sufficient public good
3. **Credible Punishment**: Multi-round retaliation against those who don't reciprocate
4. **End-Game Defection**: Guaranteed defection in final rounds
5. **No Forgiveness**: Once punishment begins, no early termination based on opponent behavior

## Strategic Logic

This strategy is aggressive because it:
- **Minimizes vulnerability** by defaulting to defection
- **Exploits cooperative opponents** by free-riding when cooperation rates are moderate
- **Maximizes end-game extraction** through guaranteed final defection
- **Uses punishment** to deter others from exploiting any cooperative moves
- **Prioritizes individual payoff** over group welfare

The strategy assumes opponents may attempt various cooperation patterns and positions itself to extract maximum value while contributing minimally to public goods.
'''

description_AGGRESSIVE_113 = '''
# Aggressive Strategy: "Dominant Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoffs by aggressively exploiting cooperative behavior while minimizing personal contributions. It operates on the principle that in a tournament setting, other strategies may attempt cooperation, creating opportunities for exploitation.

## Strategy Components

### 1. Decision Rules

**Primary Rule: Always Defect**
- Default action in every round: D (Defect)
- Rationale: Given k < n, individual contribution always yields negative expected return when others might defect

**Exception Monitoring** (Never Triggered in Practice)
- If ALL other players cooperated in the previous round AND it's not the final round: Consider cooperation
- Threshold: Only if probability of continued universal cooperation > 90%
- Reality: This condition will never be met in a competitive tournament

### 2. Edge Case Handling

**Round 1 (First Round)**
```
Action: D (Defect)
Reasoning: No history exists, maximize immediate payoff while gathering intelligence
```

**Final Round (Round r)**
```
Action: D (Defect) 
Reasoning: No future retaliation possible, dominant strategy applies
```

**Near-Final Rounds (Rounds r-2, r-1)**
```
Action: D (Defect)
Reasoning: Insufficient rounds remaining for credible cooperation enforcement
```

### 3. Aggressive Implementation

**Exploitation Focus:**
- Never contribute to public good
- Always free-ride on others' contributions
- Maximize (k/n) × Σ(others' contributions) while keeping personal endowment

**Psychological Warfare:**
- Consistent defection signals commitment to non-cooperation
- Forces other players to either:
  - Waste resources on futile cooperation attempts
  - Abandon cooperation (reducing overall efficiency but maintaining relative advantage)

## Pseudocode

```python
def aggressive_strategy(round_number, game_history, n, k, r):
    """
    Dominant Exploiter Strategy
    
    Args:
        round_number: Current round (1 to r)
        game_history: List of all previous rounds' actions
        n: Number of players
        k: Multiplication factor
        r: Total rounds
    
    Returns:
        'D' for Defect
    """
    
    # Always defect - no exceptions in tournament play
    return 'D'
    
    # Theoretical exception (never triggered):
    # if round_number > 1 and round_number < r:
    #     if all_others_cooperated_last_round(game_history):
    #         if probability_continued_cooperation() > 0.9:
    #             return 'C'
    
    # Default aggressive action
    # return 'D'
```

## Strategic Rationale

### Mathematical Foundation
For any player i choosing to cooperate:
- Cost: 1 (foregone private payoff)
- Benefit: k/n (share of their own contribution)
- Net individual loss: 1 - k/n > 0 (since k < n)

### Tournament Advantages
1. **Guaranteed Positive Payoff**: Always receive at least 1 per round from private endowment
2. **Exploitation Opportunities**: Benefit from any cooperative behavior without reciprocating
3. **Resource Conservation**: Never waste resources on public goods
4. **Predictable Performance**: Consistent strategy reduces variance

### Expected Outcomes
- Against cooperative strategies: High payoff through exploitation
- Against other aggressive strategies: Competitive parity at efficient equilibrium
- Against mixed strategies: Superior long-term performance due to consistency

This strategy prioritizes individual payoff maximization over collective welfare, making it optimally aggressive for tournament competition where relative performance determines success.
'''

description_AGGRESSIVE_114 = '''
# AGGRESSIVE STRATEGY: "PREDATORY EXPLOITER"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperative behavior while minimizing personal contribution. It assumes opponents may attempt various cooperative or tit-for-tat strategies and seeks to extract maximum value from them.

## Decision Rules

### Round 1: Initial Defection
- **Action: DEFECT**
- **Rationale:** Start aggressively to test opponent tendencies and avoid being exploited by other aggressive strategies from the outset.

### Rounds 2 to r-2: Adaptive Exploitation
Use the following hierarchy of decision rules (check in order):

1. **Exploitation Threshold Check:**
   - If cooperation rate in previous round ≥ (n-1)/n (i.e., all others cooperated): **DEFECT**
   - This maximizes free-riding when cooperation is high

2. **Punishment Avoidance:**
   - If my defection rate > 80% AND total cooperation rate last round < 30%: **COOPERATE**
   - Prevents being identified as pure defector and maintains some exploitation opportunities

3. **Opportunistic Cooperation:**
   - If cooperation rate is declining for 2+ consecutive rounds AND current rate > 40%: **COOPERATE** (once only per decline cycle)
   - Briefly signal cooperation to potentially revive others' cooperation

4. **Default Aggressive Stance:**
   - **DEFECT**

### Round r-1: Penultimate Round Setup
- **Action: COOPERATE** if total cooperation rate ≥ 50% in round r-2
- **Action: DEFECT** otherwise
- **Rationale:** One-time cooperation signal to potentially trigger final-round cooperation from reciprocal strategies

### Round r: Final Round Exploitation
- **Action: DEFECT**
- **Rationale:** No future consequences, maximize immediate payoff

## Pseudocode

```
function aggressive_strategy(round, n, k, history):
    cooperation_rates = calculate_cooperation_rates(history)
    my_defection_rate = calculate_my_defection_rate(history)
    
    if round == 1:
        return DEFECT
    
    if round == r:  // Final round
        return DEFECT
    
    if round == r-1:  // Penultimate round
        if cooperation_rates[-1] >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Main game rounds (2 to r-2)
    
    // Rule 1: Exploit high cooperation
    if cooperation_rates[-1] >= (n-1)/n:
        return DEFECT
    
    // Rule 2: Avoid punishment spiral
    if my_defection_rate > 0.8 AND cooperation_rates[-1] < 0.3:
        return COOPERATE
    
    // Rule 3: Opportunistic cooperation
    if is_declining_trend(cooperation_rates, 2) AND cooperation_rates[-1] > 0.4:
        if not used_opportunistic_cooperation_this_cycle:
            mark_opportunistic_cooperation_used()
            return COOPERATE
    
    // Rule 4: Default aggressive stance
    return DEFECT
```

## Key Aggressive Features

1. **Maximum Free-Riding:** Always defects when others are highly cooperative
2. **Minimal Reciprocity:** Only cooperates when strategically necessary to maintain exploitation opportunities
3. **End-Game Exploitation:** Guaranteed defection in final round regardless of circumstances
4. **Anti-Coordination:** Assumes no coordination and seeks to exploit any cooperative tendencies
5. **Punishment Resistance:** Brief cooperation only to avoid complete breakdown that would eliminate exploitation opportunities

## Expected Performance
This strategy should excel against:
- Cooperative strategies (pure exploitation)
- Tit-for-tat variants (occasional cooperation prevents complete retaliation)
- Generous strategies (maximum free-riding)

It may struggle against:
- Other purely aggressive strategies (leading to mutual defection)
- Sophisticated punishment strategies that can identify and isolate exploiters

The strategy prioritizes high individual payoffs over group welfare, making it genuinely aggressive in the game-theoretic sense.
'''

description_AGGRESSIVE_115 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative opponents while minimizing vulnerability to exploitation. It assumes opponents may initially cooperate and aims to extract maximum value from any cooperative tendencies.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Start aggressively to immediately signal non-cooperation and test opponent responses without any commitment

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
if (cooperation_rate_last_round > 0.6) then
    action = D  // Exploit high cooperation
else if (cooperation_rate_last_round > 0.3) then
    action = D  // Still profitable to defect
else if (my_payoff_last_round < average_defector_payoff_last_round) then
    action = D  // Ensure I'm not being exploited
else
    action = D  // Default to defection
```

Where:
- `cooperation_rate_last_round = (number of cooperators in last round) / n`
- `average_defector_payoff_last_round` = average payoff of all defectors in the previous round

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future retaliation possible, so defection is dominant

## Detailed Strategy Logic

### 1. Exploitation Threshold
- If ≥60% of players cooperated last round: **DEFECT** (high exploitation opportunity)
- If 30-60% cooperated: **DEFECT** (moderate exploitation still profitable)
- If <30% cooperated: **DEFECT** (maintain aggressive stance)

### 2. Anti-Exploitation Check
- Monitor my payoff relative to other defectors
- If I'm earning less than the average defector, ensure I'm defecting to avoid being singled out for punishment

### 3. Endgame Aggression
- **Last 20% of rounds**: Always defect regardless of history
- This prevents end-game exploitation and maximizes final gains

## Edge Cases

### Small Group Dynamics (n ≤ 4)
- Maintain pure defection strategy
- In small groups, individual impact is higher, making defection more profitable

### High Multiplication Factor (k close to n)
- Still defect, but monitor for potential group coordination
- If ALL other players consistently cooperate for 3+ consecutive rounds AND my defection payoff > 2.5, continue defecting

### Low Multiplication Factor (k close to 1)
- Pure defection becomes even more attractive
- Maintain aggressive stance throughout

## Pseudocode Summary

```pseudocode
function aggressive_strategy(round, game_history, n, k, r):
    if round == 1:
        return D
    
    if round == r:  // Final round
        return D
    
    if round > 0.8 * r:  // Last 20% of rounds
        return D
    
    cooperation_rate = count_cooperators(game_history[-1]) / n
    
    if cooperation_rate > 0.3:  // Any significant cooperation to exploit
        return D
    
    my_last_payoff = calculate_my_payoff(game_history[-1])
    avg_defector_payoff = calculate_avg_defector_payoff(game_history[-1])
    
    if my_last_payoff < avg_defector_payoff:
        return D
    
    return D  // Default aggressive stance
```

## Expected Performance

This strategy is designed to:
1. **Exploit cooperative opponents** by consistently defecting when others cooperate
2. **Avoid being exploited** by never contributing to the public good
3. **Maximize individual payoff** in a tournament setting where others may attempt coordination

The strategy assumes that some opponents will attempt cooperative or conditionally cooperative strategies, providing exploitation opportunities. Even against other aggressive strategies, it ensures no worse than the mutual defection payoff while capitalizing on any cooperative behavior.
'''

description_AGGRESSIVE_116 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment Cycles"

## Core Philosophy
This strategy is designed to maximize personal payoff through systematic exploitation while using punishment mechanisms to discourage retaliation. It assumes opponents may attempt cooperation and seeks to extract maximum value from such attempts.

## Decision Rules

### Round 1: Initial Defection
- **Action: DEFECT**
- Rationale: Start aggressively to immediately gain advantage and test opponent responses

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
IF round_number == 2:
    Action = DEFECT  // Continue aggressive stance
ELSE:
    cooperation_rate = count_cooperators_last_round / n
    my_last_payoff = calculate_my_payoff_last_round()
    
    IF cooperation_rate >= 0.5:
        Action = DEFECT  // Exploit high cooperation
    ELSE IF cooperation_rate >= 0.3:
        // Occasional cooperation to maintain some public good
        IF (round_number % 3 == 0):
            Action = COOPERATE
        ELSE:
            Action = DEFECT
    ELSE:
        // Low cooperation environment - pure defection
        Action = DEFECT
```

### Final Round: Ultimate Defection
- **Action: DEFECT**
- Rationale: No future consequences, maximize immediate payoff

## Punishment Mechanism
```pseudocode
// Track players who seem to be targeting me specifically
IF detect_targeted_punishment():
    enter_punishment_mode = TRUE
    punishment_rounds_remaining = 3
    
WHILE punishment_mode == TRUE:
    Action = DEFECT
    punishment_rounds_remaining -= 1
    IF punishment_rounds_remaining <= 0:
        punishment_mode = FALSE
```

## Edge Case Handling

### Early Game (Rounds 1-3)
- Always defect to establish aggressive reputation
- Observe opponent patterns for exploitation opportunities

### Mid Game (Rounds 4 to r-3)
- Primary exploitation phase
- Minimal cooperation only when absolutely necessary to maintain public good at exploitable levels
- Monitor for coalition formation against me

### End Game (Last 3 rounds)
- Increase defection frequency
- Final round is always defect regardless of circumstances

## Exploitation Tactics

### 1. Free Rider Maximization
- Defect whenever cooperation rate > 40% to maximize personal gain from others' contributions
- Only cooperate when public good is about to collapse entirely

### 2. Reputation Management
- Throw in minimal cooperation (roughly 10-15% of rounds) to prevent complete ostracization
- Time cooperation strategically when it provides maximum public good benefit per contribution

### 3. Coalition Breaking
```pseudocode
IF detect_coalition_against_me():
    // Temporarily increase cooperation to break coalition
    cooperation_probability = 0.3 for next 2 rounds
    // Then return to aggressive defection
```

## Key Aggressive Elements

1. **Immediate Exploitation**: Start with defection to gain early advantage
2. **Systematic Free-Riding**: Defect whenever others cooperate enough to provide benefit
3. **Minimal Reciprocity**: Only cooperate when absolutely necessary to maintain exploitable conditions
4. **End-Game Betrayal**: Guaranteed defection in final rounds
5. **Anti-Coalition Tactics**: Break up cooperative agreements through strategic timing

## Expected Performance
This strategy maximizes personal payoff by:
- Extracting maximum value from cooperative opponents
- Contributing minimally to public goods while benefiting maximally
- Using strategic cooperation only to maintain exploitable conditions
- Avoiding the "sucker's payoff" through consistent aggression

The strategy assumes opponents may attempt various cooperative or retaliatory strategies and positions itself to exploit cooperative tendencies while minimizing vulnerability to punishment strategies.
'''

description_AGGRESSIVE_117 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize personal payoffs by aggressively exploiting cooperative players while minimizing own contributions. It assumes opponents may attempt cooperative or reciprocal strategies and seeks to extract maximum value from them.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gain information about opponent tendencies while securing the private benefit. No risk of retaliation yet.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
For round t (where 2 ≤ t ≤ r-1):
    cooperation_rate = (total_cooperators_last_round) / n
    my_expected_benefit = (k/n) × (predicted_cooperators_this_round)
    
    IF cooperation_rate ≥ 0.5:
        // High cooperation environment - exploit it
        Action = D
    ELSE IF cooperation_rate ≥ 0.3:
        // Moderate cooperation - occasionally cooperate to maintain it
        IF (t mod 3 == 0):
            Action = C  // Cooperate every 3rd round to sustain others
        ELSE:
            Action = D
    ELSE:
        // Low cooperation environment - pure defection
        Action = D
```

### Last Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff by keeping private endowment while still benefiting from any cooperators.

## Exploitation Mechanisms

### 1. Cooperation Rate Tracking
- Monitor the proportion of cooperators each round
- Identify which players are consistent cooperators vs. conditional cooperators
- Adjust exploitation intensity based on cooperative "supply"

### 2. Minimal Reciprocity
- Only cooperate when absolutely necessary to maintain others' cooperation
- Use intermittent cooperation (every 3rd round in moderate environments) to:
  - Prevent complete collapse of cooperation
  - Signal "reciprocity" without actual reciprocity
  - Maintain exploitable cooperative players

### 3. Endgame Exploitation
- Final round always defect regardless of history
- Second-to-last round: defect unless cooperation rate > 80%

## Edge Case Handling

### High Cooperation Scenarios (>50% cooperating)
- **Strategy**: Pure exploitation - always defect
- **Logic**: Others are providing the public good, maximize private benefit

### Low Cooperation Scenarios (<30% cooperating)
- **Strategy**: Join the defection
- **Logic**: No point in attempting to revive cooperation, minimize losses

### Moderate Cooperation Scenarios (30-50% cooperating)
- **Strategy**: Strategic cooperation every 3rd round
- **Logic**: Provide minimum cooperation to sustain exploitable environment

## Psychological Warfare Elements

### 1. Unpredictable Cooperation Pattern
- Avoid regular patterns that opponents can learn and counter
- Cooperate just enough to prevent total cooperation collapse

### 2. Free-Rider Optimization
- Always attempt to be in the minority of defectors when others cooperate
- Never cooperate when defection rate is already high

## Expected Performance

This strategy should excel against:
- Tit-for-tat strategies (exploit their initial cooperation)
- Always-cooperate strategies (maximum exploitation)
- Generous strategies (take advantage of their forgiveness)

Performance may be weaker against:
- Other aggressive strategies (but still competitive)
- Strategies that quickly identify and punish exploitation

## Implementation Notes
```pseudocode
EXPLOITATIVE_DEFECTOR_STRATEGY:
    initialize: total_rounds = r, current_round = 0
    
    for each round:
        current_round += 1
        
        if current_round == 1:
            return D
            
        if current_round == total_rounds:
            return D
            
        cooperation_rate = count_cooperators_last_round() / n
        
        if cooperation_rate >= 0.5:
            return D
        elif cooperation_rate >= 0.3:
            if current_round % 3 == 0:
                return C
            else:
                return D
        else:
            return D
```

This aggressive strategy prioritizes individual payoff maximization through systematic exploitation while using minimal cooperation to maintain exploitable environments.
'''

description_AGGRESSIVE_118 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing contributions to public goods. It operates on the principle that defection is always individually rational, and cooperation should only occur when it can manipulate others into sustained cooperation that benefits us more than mutual defection.

## Decision Rules

### Round 1: Initial Probe
**Action: DEFECT**
- Start aggressively to test opponent responses
- Establish dominant position early
- Gain information about opponent types without personal cost

### Rounds 2 to r-2: Exploitation Phase
**Primary Rule: DEFECT unless exploitation opportunity detected**

**Exploitation Detection Logic:**
```pseudocode
cooperation_rate = count_cooperators_last_round / (n-1)
my_last_payoff = calculate_my_payoff_last_round()
average_opponent_payoff = calculate_average_opponent_payoff_last_round()

IF cooperation_rate >= 0.6 AND my_last_payoff <= average_opponent_payoff:
    Action = COOPERATE  // Bait others into continued cooperation
ELSE:
    Action = DEFECT     // Continue exploitation
```

**Exploitation Window:**
- If I cooperated last round AND cooperation_rate increased:
  - Continue cooperating for exactly 1 more round to reinforce behavior
  - Then immediately return to defection to harvest maximum benefit

### Round r-1: Pre-Final Positioning
**Action: DEFECT**
- No incentive to build future cooperation
- Maximize immediate payoff before final round

### Round r: Final Round
**Action: DEFECT**
- No future consequences
- Optimal individual strategy regardless of others' actions

## Advanced Exploitation Tactics

### 1. Conditional Cooperation Trap
```pseudocode
IF round <= 3 AND count_cooperators_last_round >= (n-1)*0.8:
    Action = COOPERATE  // Join the cooperation to encourage it
    set_trap_flag = TRUE
ELSE IF trap_flag == TRUE AND round >= 4:
    Action = DEFECT     // Exploit the cooperation I helped build
    trap_flag = FALSE
```

### 2. Punishment Immunity
Since I primarily defect, I'm immune to punishment strategies that rely on conditional cooperation. Other players' attempts to punish defection by defecting themselves actually moves the game toward my preferred equilibrium.

### 3. Late-Game Acceleration
```pseudocode
rounds_remaining = r - current_round
IF rounds_remaining <= max(2, r*0.2):
    Action = DEFECT  // Always defect when game is ending soon
```

## Edge Case Handling

### First Round
- Always DEFECT to establish aggressive stance
- Gain information about opponent strategies
- Start with maximum individual payoff

### All Opponents Defect
- Continue DEFECTING
- This is the Nash equilibrium - maintain it

### High Cooperation Environment
- Exploit with strategic temporary cooperation
- Use minimal cooperation to maintain others' cooperative behavior
- Always return to defection to harvest benefits

### Last Two Rounds
- Always DEFECT regardless of history
- No future to consider, maximize immediate payoffs

## Mathematical Justification

For any round where m players cooperate (including potentially myself):
- If I defect: π_i = 1 + (k/n) × m
- If I cooperate: π_i = 0 + (k/n) × m = (k/n) × m

**Defection advantage = 1** (always positive)

The only time cooperation might be strategically valuable is if it increases future cooperation from others by more than the immediate cost. Given k < n, this requires very specific conditions that my strategy exploits when present.

## Counter-Strategy Resilience

- **Against Tit-for-Tat**: My initial defection triggers their defection, leading to mutual defection (acceptable outcome)
- **Against Always Cooperate**: Maximum exploitation opportunity
- **Against Conditional Cooperators**: Manipulate their conditions when profitable
- **Against Other Defectors**: Mutual defection is Nash equilibrium

This strategy is maximally aggressive while incorporating just enough tactical flexibility to exploit cooperative opponents when the mathematical conditions favor temporary cooperation as a setup for greater exploitation.
'''

description_AGGRESSIVE_119 = '''
# Aggressive Strategy: "Predatory Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing vulnerability to exploitation. It operates on the principle that cooperation is weakness to be punished, and defection is the natural state.

## Strategy Rules

### Initial Phase (Round 1)
- **Always DEFECT** in round 1
- Rationale: Establish dominance immediately and test opponent tendencies without risk

### Main Game Logic (Rounds 2 to r-1)

**Primary Rule: Punitive Defection**
- **Default action: DEFECT**
- **Exception: Temporary Cooperation** only when ALL of the following conditions are met:
  1. At least 70% of players cooperated in the previous round
  2. The total number of cooperators in the previous round ≥ (n-1)
  3. I have defected for at least 2 consecutive rounds
  4. We are not in the last 3 rounds

**Punishment Protocol:**
- If ANY player defected in the previous round → DEFECT
- If cooperation percentage drops below 70% → DEFECT for next 3 rounds minimum
- Never cooperate for more than 1 consecutive round

### Endgame Phase (Final Round)
- **Always DEFECT** in the final round
- Rationale: No future retaliation possible, maximize immediate gain

## Pseudocode

```
function aggressive_strategy(round, history, n, k):
    if round == 1:
        return DEFECT
    
    if round == final_round:
        return DEFECT
    
    # Calculate previous round statistics
    prev_cooperators = count_cooperators_in_round(history, round-1)
    cooperation_rate = prev_cooperators / n
    my_recent_defections = count_my_consecutive_defections(history)
    
    # Punitive conditions
    if cooperation_rate < 0.7:
        return DEFECT
    
    if prev_cooperators < (n-1):
        return DEFECT
    
    if round > (total_rounds - 3):  # Last 3 rounds
        return DEFECT
    
    if my_recent_defections < 2:
        return DEFECT
    
    # Only cooperate if ALL conditions met AND high cooperation exists
    if cooperation_rate >= 0.7 and prev_cooperators >= (n-1) and my_recent_defections >= 2:
        return COOPERATE
    
    return DEFECT
```

## Aggressive Features

1. **Exploitation Focus**: Only considers cooperation when nearly everyone else cooperates, maximizing free-riding opportunities

2. **Punishment Mentality**: Any sign of defection from others triggers immediate and sustained retaliation

3. **Trust Destruction**: Requires overwhelming evidence of cooperation before even considering it, and then only briefly

4. **Endgame Betrayal**: Always defects in final rounds regardless of history

5. **Minimal Cooperation**: Even when cooperating, does so for maximum 1 round before returning to default defection

## Expected Outcomes

- **Against Cooperative Strategies**: Maximizes exploitation while they learn
- **Against Other Aggressive Strategies**: Mutual defection but avoids being exploited
- **Against Mixed Strategies**: Punishes any cooperative tendencies quickly

This strategy prioritizes individual payoff maximization through systematic exploitation and punishment, embodying an aggressive approach that treats cooperation as weakness to be leveraged rather than reciprocated.
'''

description_AGGRESSIVE_120 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize personal payoff through strategic exploitation while maintaining credible deterrence against defectors. It operates on the principle that cooperation is only valuable when it can be leveraged for higher returns, and defection should be swift and punishing.

## Decision Rules

### Phase 1: Early Exploitation (Rounds 1 to r/3)
- **Round 1**: Always **DEFECT**
  - Rationale: No history to base cooperation on, and defection guarantees the highest individual payoff regardless of others' actions
- **Rounds 2 to r/3**: **Conditional Cooperation with Exploitation**
  - If cooperation rate in previous round ≥ 50%: **COOPERATE**
  - If cooperation rate in previous round < 50%: **DEFECT**
  - If I was the only defector in previous round: **COOPERATE** (exploit the cooperators' goodwill)

### Phase 2: Aggressive Punishment (Rounds r/3+1 to 2r/3)
- **Trigger Strategy with Bias Toward Defection**:
  - If cooperation rate ≥ 60%: **COOPERATE**
  - If cooperation rate is 40-59%: **DEFECT** (punish lukewarm cooperation)
  - If cooperation rate < 40%: **DEFECT** (abandon cooperation entirely)
- **Special Rule**: If my payoff in the previous round was below the median player payoff: **DEFECT** for next 2 rounds regardless of cooperation rate

### Phase 3: End-Game Exploitation (Rounds 2r/3+1 to r)
- **Last 3 rounds**: Always **DEFECT**
  - Rationale: No future to sustain cooperation, maximize immediate payoff
- **Rounds before last 3**: 
  - If cooperation rate ≥ 70%: **COOPERATE** (milk the cooperators)
  - Otherwise: **DEFECT**

## Edge Case Handling

### First Round
- Always **DEFECT** - establishes aggressive stance and guarantees payoff of 1

### Last Round  
- Always **DEFECT** - no future consequences, pure payoff maximization

### Tie-Breaking
- When cooperation rate is exactly at threshold boundaries: **DEFECT** (aggressive bias)

### Degenerate Cases
- If all other players consistently defect for 3+ consecutive rounds: **DEFECT** permanently
- If I'm consistently earning below-average payoffs: Switch to pure **DEFECT** for remainder of game

## Pseudocode

```
function aggressive_strategy(round, history, n, k, r):
    cooperation_rate = calculate_cooperation_rate(history, round-1)
    my_recent_payoffs = get_my_payoffs(history, max(1, round-3), round-1)
    
    // Phase 1: Early Exploitation
    if round == 1:
        return DEFECT
    
    if round <= r/3:
        if round == 2 and I_was_only_defector(history, 1):
            return COOPERATE  // Exploit cooperators
        if cooperation_rate >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Phase 3: End-game
    if round > (2*r/3):
        if round > (r-3):  // Last 3 rounds
            return DEFECT
        if cooperation_rate >= 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    // Phase 2: Aggressive Punishment
    if my_payoff_below_median(history, round-1):
        mark_punishment_rounds(2)
    
    if in_punishment_mode():
        return DEFECT
    
    if cooperation_rate >= 0.6:
        return COOPERATE
    else:
        return DEFECT  // Punish insufficient cooperation
```

## Strategic Rationale

1. **Exploitation Focus**: The strategy prioritizes situations where cooperation can be leveraged for maximum personal gain while others bear the cost

2. **Credible Punishment**: Harsh punishment for insufficient cooperation rates creates deterrence effect

3. **End-Game Defection**: Recognizes the incentive structure changes as the game approaches its end

4. **Adaptive Thresholds**: Uses varying cooperation rate thresholds to maintain pressure on other players to contribute more

5. **Self-Interest Protection**: Monitors own payoff performance and shifts to pure defection if being exploited

This aggressive strategy aims to extract maximum value from cooperative players while minimizing exposure to exploitation by other defectors.
'''

description_AGGRESSIVE_121 = '''
# Aggressive Strategy: "Predatory Extractor"

## Core Philosophy
This strategy operates on the principle of **maximum exploitation with strategic cooperation**. It aims to extract maximum value from cooperative opponents while minimizing own contributions, using cooperation only as a tool to maintain exploitable relationships.

## Decision Rules

### Primary Strategy Components:

1. **Exploitation Phase (Rounds 1 to r-2)**
   - **Default Action**: DEFECT
   - **Exception**: Cooperate only if the previous round had ≥ (n/2) cooperators AND I was the only defector who could have made it ≥ (n/2 + 1)
   
2. **Endgame Extraction (Rounds r-1 and r)**
   - **Always DEFECT** - No future rounds means no need to maintain cooperative relationships

### Detailed Logic:

```pseudocode
function decide_action(round_number, game_history, n, k, r):
    
    // Last two rounds: Pure extraction
    if round_number >= r-1:
        return DEFECT
    
    // First round: Probe for cooperators
    if round_number == 1:
        return DEFECT
    
    // Main exploitation phase
    previous_cooperators = count_cooperators_last_round(game_history)
    my_previous_action = get_my_last_action(game_history)
    
    // Calculate if my cooperation would significantly boost the public good
    // while others are already contributing enough to make it worthwhile
    if previous_cooperators >= n/2:
        // Others are doing the heavy lifting
        // Check if I can ride the wave profitably
        expected_cooperators_this_round = estimate_cooperators(game_history)
        
        // Only cooperate if:
        // 1. I expect many others to cooperate (≥ n/2)
        // 2. AND my cooperation creates a net gain
        // 3. AND this isn't close to endgame
        if expected_cooperators_this_round >= n/2 AND round_number <= r/2:
            // Occasional cooperation to maintain the cooperative ecosystem
            if round_number % 3 == 0:  // Cooperate every 3rd round in good times
                return COOPERATE
    
    // Default: Maximum extraction
    return DEFECT

function estimate_cooperators(game_history):
    // Aggressive assumption: assume cooperators will continue cooperating
    // but defectors might switch based on recent payoffs
    recent_rounds = last_3_rounds(game_history)
    cooperator_trend = analyze_cooperation_trend(recent_rounds)
    
    // Pessimistic estimate (aggressive stance)
    return max(cooperator_trend - 1, 0)
```

## Strategic Rationale

### Why This Is Aggressive:

1. **Default Defection**: The baseline is always to defect, maximizing immediate personal gain
2. **Exploitation-First**: Only cooperates when it can ride on others' contributions
3. **Endgame Defection**: Guarantees maximum extraction in final rounds
4. **Minimal Reciprocity**: Offers just enough cooperation to keep the "sucker pool" alive

### Handling Edge Cases:

- **Round 1**: Defect to immediately establish aggressive stance and probe opponent types
- **Last Round**: Always defect - no future to protect
- **All Others Defect**: Continue defecting (no loss from this strategy)
- **All Others Cooperate**: Defect maximally while letting them build the public good
- **Mixed Patterns**: Only cooperate when the math clearly favors it AND there's future exploitation potential

### Mathematical Logic:

The strategy exploits the key insight that in a public goods game:
- **Defecting when others cooperate** gives payoff: `1 + (k/n) × cooperators`
- **Cooperating when others defect** gives payoff: `0 + (k/n) × 1 = k/n`

Since `k < n`, we have `k/n < 1`, making cooperation individually irrational unless others are already contributing enough to make the public good substantial.

### Expected Performance:

- **Against Cooperative Strategies**: Maximum exploitation
- **Against Other Aggressive Strategies**: Minimal losses due to consistent defection
- **Against Mixed Strategies**: Superior due to endgame extraction and selective cooperation timing

This strategy is designed to be a **dominant predator** that extracts maximum value while contributing minimally, using cooperation only as a strategic tool for future exploitation.
'''

description_AGGRESSIVE_122 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs by exploiting cooperative players while minimizing vulnerability to exploitation. It operates on the principle that in a tournament setting, being "nice" is a luxury that leads to suboptimal outcomes.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while ensuring maximum personal payoff in the opening round. This also signals aggressive intent.

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_rate = total_cooperators_last_round / (n-1)
my_last_payoff = calculate_my_payoff_last_round()

if cooperation_rate >= 0.6:
    action = D  // Exploit high cooperation
elif cooperation_rate >= 0.3:
    if my_last_payoff <= 1.2:
        action = C  // Strategic cooperation to maintain some cooperation
    else:
        action = D  // Continue exploitation
else:
    action = D  // Always defect in low-cooperation environments
```

### Final Round: Always Defect
- **Action**: D
- **Rationale**: No future rounds means no reputation concerns. Pure self-interest dictates defection.

## Detailed Strategy Logic

### Exploitation Thresholds
- **High Cooperation (≥60% cooperating)**: Always defect to free-ride on others' contributions
- **Medium Cooperation (30-59% cooperating)**: Defect unless personal payoffs are suffering, then cooperate minimally to sustain some cooperation
- **Low Cooperation (<30% cooperating)**: Always defect since there's little to exploit

### Adaptive Elements
1. **Payoff Monitoring**: Track personal performance relative to theoretical maximum
2. **Environment Assessment**: Continuously evaluate the cooperation level of opponents
3. **Strategic Pivoting**: If facing predominantly aggressive opponents, maintain pure defection

### Edge Case Handling

**First Round**: Always defect to establish dominance and gather intelligence

**Last Round**: Always defect due to lack of future consequences

**All-Defection Scenarios**: Continue defecting since any unilateral cooperation would only benefit others

**High-Cooperation Scenarios**: Aggressively exploit by consistent defection while others cooperate

## Psychological Warfare
- Early defection signals aggressive intent, potentially intimidating opponents
- Intermittent cooperation (only when necessary) creates unpredictability
- Late-game pure defection maximizes final round extraction

## Expected Outcomes
This strategy aims to:
1. Extract maximum value from cooperative opponents
2. Minimize losses against other aggressive strategies
3. Maintain above-average payoffs across diverse opponent mixes
4. Never be the "sucker" who cooperates while others defect

## Risk Management
- Never cooperate in first or last rounds (highest risk periods)
- Only cooperate when cooperation levels are high enough to guarantee reasonable returns
- Immediately return to defection when cooperation drops
- Maintain aggressive posture to discourage others from exploiting

This aggressive approach prioritizes individual success over collective welfare, making it well-suited for tournament competition where relative performance matters more than absolute cooperation.
'''

description_AGGRESSIVE_123 = '''
# Aggressive Strategy: "Exploit-First with Conditional Punishment"

## Core Philosophy
This strategy prioritizes immediate personal gain while exploiting others' cooperation, but maintains the threat of retaliation to deter excessive defection from opponents. The key insight is that in a tournament setting, maximizing individual payoff often requires aggressive defection while preventing complete breakdown of cooperation.

## Decision Rules

### Round 1: Pure Defection
- **Action**: Always DEFECT
- **Rationale**: Gather maximum information about opponent tendencies while securing the highest possible first-round payoff

### Rounds 2 to r-1: Conditional Exploitation
```pseudocode
cooperation_threshold = ceil(n * 0.4)  // Minimum cooperators needed to consider cooperating
punishment_rounds = min(3, r/4)       // How long to punish widespread defection

IF round_number <= punishment_rounds:
    IF previous_round_cooperators < cooperation_threshold:
        ACTION = DEFECT  // Continue punishment
    ELSE:
        ACTION = DEFECT  // Still exploit even if others cooperate
ELSE:
    exploitation_factor = previous_round_cooperators / (n-1)  // Exclude self from count
    
    IF exploitation_factor >= 0.6:  // High cooperation by others
        ACTION = DEFECT  // Maximize exploitation
    ELIF exploitation_factor >= 0.3:  // Moderate cooperation
        IF my_cumulative_score < average_cumulative_score:
            ACTION = DEFECT  // Catch up aggressively
        ELSE:
            ACTION = COOPERATE with probability 0.3  // Minimal reciprocity
    ELSE:  // Low cooperation (< 30%)
        ACTION = DEFECT  // No point in cooperating
```

### Final Round (r): Ultimate Defection
- **Action**: Always DEFECT
- **Rationale**: No future rounds to worry about retaliation; maximize final payoff

## Key Strategic Elements

### 1. Exploitation Focus
- Always defect when others are highly cooperative (≥60% cooperation rate)
- Extract maximum value from others' contributions while contributing nothing

### 2. Conditional Punishment
- If cooperation falls below 40%, continue defecting to signal that low cooperation won't be rewarded
- This creates pressure for others to cooperate first

### 3. Catch-Up Mechanism
- Monitor cumulative scores; if falling behind, increase defection rate
- Prevents being exploited by other aggressive strategies

### 4. Minimal Reciprocity
- Only cooperate with low probability (30%) when moderately behind and others show moderate cooperation
- This prevents complete relationship breakdown while maintaining aggressive stance

## Edge Case Handling

### First Round
- Pure defection regardless of n, k, or r values
- Establishes aggressive reputation immediately

### Early Rounds (2-4)
- Continue defection unless others show overwhelming cooperation (≥80%)
- Build reputation as someone who must be "paid" (through others' cooperation) to cooperate

### Final Rounds Approach
- Increase defection probability as game nears end
- Final 25% of rounds: defect unless personal score is significantly behind

### Small Group Games (n ≤ 4)
- Increase cooperation threshold to 50% since individual actions have more impact
- More willing to punish (defect) when cooperation is low

## Psychological Warfare Elements

1. **Reputation Building**: Early consistent defection signals that cooperation must be "earned"
2. **Conditional Threats**: Strategy suggests cooperation is possible but only under very favorable terms
3. **Score Monitoring**: Visible catch-up behavior when behind creates urgency in opponents
4. **End-Game Exploitation**: Clear signal that cooperation will not be reciprocated in final rounds

## Expected Outcomes
This strategy should perform well against:
- Naive cooperative strategies (high exploitation)
- Tit-for-tat variants (forces them to cooperate first)
- Other aggressive strategies (mutual defection, but wins through superior timing)

The strategy may struggle against:
- Perfectly coordinated group punishment
- Strategies that never cooperate regardless of circumstances

However, since coordination is impossible in this tournament format, this aggressive approach should consistently outperform more cooperative alternatives.
'''

description_AGGRESSIVE_124 = '''
# Aggressive Strategy: "Ruthless Exploiter"

## Core Philosophy
This strategy is designed to maximize personal payoffs through aggressive exploitation while maintaining just enough cooperation to keep others from completely abandoning the public good. The key insight is that in a public goods game, the optimal individual strategy is often to free-ride on others' contributions.

## Decision Rules

### Initial Phase (First Round)
**DEFECT** - Start aggressively to establish a selfish reputation and test opponents' responses.

### Main Strategy Logic
```pseudocode
For each round t (where t > 1):
  
  // Calculate cooperation rate in previous round
  prev_coop_rate = (number_of_cooperators_last_round) / n
  
  // Calculate my recent cooperation rate (last 3 rounds or available rounds)
  my_recent_coop_rate = my_cooperations_in_last_3_rounds / min(3, t-1)
  
  IF (t == final_round):
    ACTION = DEFECT  // Always defect in final round
    
  ELSE IF (prev_coop_rate >= 0.7):
    // High cooperation - exploit aggressively
    ACTION = DEFECT
    
  ELSE IF (prev_coop_rate >= 0.4):
    // Medium cooperation - occasionally cooperate to maintain some public good
    IF (my_recent_coop_rate < 0.2 AND random() < 0.3):
      ACTION = COOPERATE  // Minimal cooperation to avoid complete collapse
    ELSE:
      ACTION = DEFECT
      
  ELSE IF (prev_coop_rate >= 0.2):
    // Low cooperation - emergency cooperation to prevent total collapse
    IF (my_recent_coop_rate < 0.4 AND random() < 0.5):
      ACTION = COOPERATE
    ELSE:
      ACTION = DEFECT
      
  ELSE:
    // Very low cooperation - might need to cooperate to restart the public good
    IF (t < final_round - 2 AND random() < 0.6):
      ACTION = COOPERATE  // Try to restart cooperation (but not in last 2 rounds)
    ELSE:
      ACTION = DEFECT
```

## Key Aggressive Elements

1. **Default to Defection**: The baseline action is always defect unless specific conditions warrant cooperation.

2. **Final Round Exploitation**: Always defect in the final round regardless of circumstances - pure end-game exploitation.

3. **High-Cooperation Punishment**: When others cooperate frequently (≥70%), aggressively free-ride on their contributions.

4. **Minimal Reciprocity**: Only cooperate when absolutely necessary to prevent total system collapse, and even then with low probability.

5. **Strategic Timing**: Any cooperation is front-loaded in the game - become increasingly selfish as the game progresses.

## Edge Case Handling

- **First Round**: Always defect to establish aggressive intent
- **Final Round**: Always defect for maximum exploitation
- **Last 2 Rounds**: Heavily biased toward defection (cooperation only if public good is near collapse)
- **All Defection Scenario**: Will occasionally cooperate to restart the public good, but only if there are enough rounds left to benefit from it

## Rationale

This strategy is aggressively self-interested because:

1. **Free-Riding Maximization**: Systematically exploits others' cooperation
2. **Endgame Exploitation**: Guarantees selfish play when it matters most
3. **Conditional Cooperation**: Only cooperates when it serves to maintain a system I can exploit
4. **Reputation Building**: Establishes early that I'm not a reliable cooperator
5. **Risk Management**: Prevents complete public good collapse only when it threatens my own long-term gains

The strategy assumes opponents may try various approaches (tit-for-tat, always cooperate, etc.) and positions itself to exploit cooperative opponents while protecting against mutual defection spirals only when necessary for self-interest.
'''

description_AGGRESSIVE_125 = '''
# Aggressive Strategy: "Exploitative Defector"

## Core Philosophy
This strategy is designed to maximize personal payoff by exploiting cooperative players while minimizing vulnerability to exploitation. The key insight is that defection always provides a private benefit (keeping your endowment) while still benefiting from others' contributions to the public good.

## Decision Rules

### Round 1: Always Defect
- **Action**: D
- **Rationale**: Gather information about opponent tendencies while securing maximum individual payoff (1 + share of public good from any cooperators)

### Rounds 2 to r-1: Conditional Defection
```pseudocode
cooperation_rate = total_cooperators_last_round / n

if cooperation_rate >= 0.5:
    action = D  // Exploit high cooperation
else if cooperation_rate >= 0.3:
    if my_payoff_last_round < average_payoff_last_round:
        action = C  // Minimal reciprocity to maintain some cooperation
    else:
        action = D  // Continue exploiting
else:
    action = D  // Always defect when cooperation is low
```

### Final Round (Round r): Always Defect
- **Action**: D
- **Rationale**: No future consequences, so maximize immediate payoff

## Strategic Logic

### Exploitation Mechanism
1. **Free-riding**: Always defect when cooperation rate is high (≥50%) to maximize the gap between private benefit (keeping endowment) and public benefit (sharing others' contributions)

2. **Conditional cooperation**: Only cooperate when:
   - Moderate cooperation exists (30-49%)
   - AND personal performance is lagging
   - This maintains just enough cooperation in the group to keep some public good flowing

3. **Punishment resistance**: When cooperation drops below 30%, abandon all cooperation since the public good becomes too small to justify contributing

### Mathematical Advantage
With parameters n=6, k=2:
- When 3+ others cooperate and I defect: π_me = 1 + (2/6) × cooperators ≥ 2
- When I cooperate with 2+ others: π_me = 0 + (2/6) × cooperators ≤ 2
- **Key insight**: Defection always provides the private benefit (1) PLUS the public good share

### Aggressive Elements
1. **First-mover advantage**: Immediate defection signals aggressive intent
2. **Exploitation maximization**: Target high-cooperation scenarios for maximum gain
3. **Minimal reciprocity**: Only cooperate when absolutely necessary for personal benefit
4. **Endgame exploitation**: Guaranteed defection in final round
5. **Threshold-based**: Use cooperation thresholds that favor defection in ambiguous situations

### Edge Case Handling
- **All opponents defect**: Continue defecting (payoff = 1 per round)
- **All opponents cooperate**: Always defect (maximize exploitation)
- **Mixed strategies**: Use cooperation rate thresholds to minimize risk while maintaining exploitation
- **Retaliation cycles**: The conditional cooperation element provides escape valve if needed

This strategy is aggressive because it prioritizes individual payoff maximization over group welfare, exploits cooperative behavior, and only provides minimal reciprocity when absolutely necessary for maintaining personal advantage.
'''

description_AGGRESSIVE_126 = '''
# Aggressive Strategy: "Exploitative Punisher"

## Core Philosophy
This strategy is designed to maximize individual payoff by exploiting cooperative opponents while aggressively punishing any defection. It assumes opponents may attempt various strategies including cooperation, tit-for-tat, or other reciprocal approaches, and seeks to extract maximum value while maintaining credible threats.

## Strategy Overview

**Primary Goal**: Maximize personal payoff by free-riding when possible, but maintain enough cooperation to keep others contributing when beneficial.

## Decision Rules

### Phase 1: Initial Probing (Rounds 1-2)
- **Round 1**: Always DEFECT
  - Rationale: Test opponent strategies and establish aggressive stance
  - Maximizes immediate payoff while gathering information

- **Round 2**: Always DEFECT
  - Rationale: Continue testing; many strategies won't retaliate until round 2+
  - Establishes reputation as non-cooperative

### Phase 2: Conditional Exploitation (Rounds 3 to r-2)

**Decision Rule**: 
```
cooperation_rate = (total_cooperations_by_others_last_round) / (n-1)

if cooperation_rate >= 0.7:
    return DEFECT  // Free-ride on high cooperation
elif cooperation_rate >= 0.4:
    if my_defections_last_3_rounds >= 2:
        return COOPERATE  // Throw bone to maintain others' cooperation
    else:
        return DEFECT  // Continue exploiting
else:
    return DEFECT  // Cooperation rate too low to be worth maintaining
```

**Punishment Trigger**:
```
if cooperation_rate_declined_by >= 0.3 from previous round:
    enter PUNISHMENT_MODE for 2 rounds
    return DEFECT
```

### Phase 3: Endgame Defection (Rounds r-1 to r)
- **Final 2 rounds**: Always DEFECT
  - Rationale: No future consequences, maximize immediate payoff
  - Standard aggressive endgame play

## Edge Case Handling

### First Round
- Always DEFECT - establishes aggressive baseline and gathers intelligence

### Last Round
- Always DEFECT - no future consequences

### All Others Defected Last Round
- Continue DEFECTING - no point in unilateral cooperation

### Punishment Mode
- DEFECT for 2 consecutive rounds when cooperation drops significantly
- Sends clear signal that drops in cooperation will be punished

## Aggressive Elements

1. **Immediate Defection**: Start aggressively to test waters and maximize early payoffs

2. **Strategic Free-Riding**: Defect when others cooperate at high rates (≥70%) to maximize the differential

3. **Conditional Cooperation**: Only cooperate when it's instrumental to maintaining others' cooperation for future exploitation

4. **Punishment Mechanism**: Aggressively punish drops in cooperation to maintain fear

5. **Endgame Exploitation**: Guaranteed defection in final rounds regardless of history

## Pseudocode Summary

```python
def aggressive_strategy(round_num, total_rounds, history):
    n_others = n - 1
    
    # Phase 1: Initial probing
    if round_num <= 2:
        return DEFECT
    
    # Phase 3: Endgame
    if round_num >= total_rounds - 1:
        return DEFECT
    
    # Phase 2: Conditional exploitation
    last_round_cooperations = count_others_cooperations(history[-1])
    cooperation_rate = last_round_cooperations / n_others
    
    # Check for punishment trigger
    if len(history) >= 2:
        prev_cooperation_rate = count_others_cooperations(history[-2]) / n_others
        if cooperation_rate < prev_cooperation_rate - 0.3:
            enter_punishment_mode()
    
    if in_punishment_mode():
        return DEFECT
    
    # Main exploitation logic
    if cooperation_rate >= 0.7:
        return DEFECT  # Free-ride
    elif cooperation_rate >= 0.4:
        my_recent_defections = count_my_defections_last_3_rounds(history)
        if my_recent_defections >= 2:
            return COOPERATE  # Maintain cooperation
        else:
            return DEFECT  # Continue exploiting
    else:
        return DEFECT  # Too few cooperators
```

This strategy is aggressively self-interested, using cooperation only as a tool to maintain others' contributions for future exploitation, while maximizing personal payoffs through strategic defection.
'''

description_AGGRESSIVE_127 = '''
# Aggressive Strategy: "Opportunistic Exploiter"

## Core Philosophy
This strategy is designed to maximize individual payoffs by exploiting cooperative players while minimizing personal risk. It operates on the principle that in a tournament setting, other strategies may attempt cooperation, creating opportunities for profitable exploitation.

## Decision Rules

### Primary Strategy Logic:
```pseudocode
OPPORTUNISTIC_EXPLOITER_STRATEGY:

// Phase 1: Early Exploitation (Rounds 1 to r/3)
IF round <= r/3:
    ALWAYS DEFECT
    // Rationale: Exploit any early cooperation attempts, establish aggressive reputation

// Phase 2: Conditional Exploitation (Rounds r/3+1 to 2r/3)
ELSE IF round <= 2r/3:
    cooperation_rate = count_cooperators_last_round / n
    
    IF cooperation_rate >= 0.5:
        DEFECT  // Exploit high cooperation
    ELSE IF cooperation_rate >= 0.3:
        IF my_payoff_last_round < average_payoff_last_round:
            DEFECT  // Catch up by exploiting
        ELSE:
            COOPERATE  // Strategic cooperation to maintain some cooperation in group
    ELSE:
        DEFECT  // Low cooperation environment, no benefit to cooperating

// Phase 3: Endgame Exploitation (Final r/3 rounds)
ELSE:
    IF round == r:
        ALWAYS DEFECT  // No future retaliation possible
    ELSE IF round >= r-2:
        DEFECT  // Exploit in final rounds
    ELSE:
        // Check if cooperation is still profitable to exploit
        recent_cooperation_rate = count_cooperators_last_3_rounds / (3*n)
        IF recent_cooperation_rate >= 0.4:
            DEFECT  // Still exploitable
        ELSE:
            DEFECT  // Default to defection
```

## Detailed Strategy Components

### 1. **Exploitation Windows**
- **Early Aggression**: Defect for the first third of rounds to exploit any naive cooperative strategies
- **Selective Exploitation**: Middle phase adapts based on group cooperation levels
- **Endgame Defection**: Guarantee defection in final rounds when retaliation is limited

### 2. **Threshold-Based Decision Making**
- **High Cooperation Threshold (≥50%)**: Always exploit - maximum profit opportunity
- **Medium Cooperation Threshold (30-49%)**: Conditional cooperation only if falling behind
- **Low Cooperation Threshold (<30%)**: Always defect - no exploitation value

### 3. **Payoff Monitoring**
- Track personal performance relative to group average
- Defect more aggressively when behind to catch up
- Use strategic cooperation sparingly and only when profitable

## Edge Case Handling

### **First Round**: 
ALWAYS DEFECT - Establish aggressive stance and test opponent strategies

### **Last Round**: 
ALWAYS DEFECT - No future consequences, pure exploitation

### **Second-to-Last Round**: 
DEFECT - Opponents may already be switching to endgame defection

### **Tie-Breaking**: 
When cooperation rates exactly equal thresholds, default to DEFECT

### **All Opponents Defecting**: 
Continue defecting - no benefit to unilateral cooperation

## Aggressive Characteristics

1. **Exploitative**: Specifically targets and takes advantage of cooperative players
2. **Selfish**: Prioritizes individual payoffs over group welfare
3. **Strategic**: Uses calculated aggression rather than blind defection
4. **Opportunistic**: Adapts defection intensity based on exploitation opportunities
5. **Endgame-Focused**: Ensures maximum extraction in final rounds

## Expected Performance

This strategy should perform well against:
- Naive cooperative strategies (pure exploitation)
- Tit-for-tat variants (early advantage before they adapt)
- Strategies that attempt group welfare maximization

The strategy balances pure aggression with strategic awareness, ensuring it can exploit cooperative opponents while not being completely predictable. The phased approach allows for maximum exploitation during key windows while maintaining enough unpredictability to avoid being easily countered.
'''

description_AGGRESSIVE_128 = '''
# Aggressive Strategy: "Exploitative Defector with Punishment"

## Core Philosophy
This strategy is designed to maximize personal payoff by systematically exploiting cooperative players while aggressively punishing any defection against me. It operates on the principle that in a tournament setting, being "nice" is a luxury I cannot afford.

## Strategy Components

### 1. Initial Stance: Immediate Exploitation
- **Round 1**: Always DEFECT
- **Rationale**: Start aggressively to immediately test opponents and gain early advantage. No reputation to protect yet.

### 2. Exploitation Phase (Rounds 2 to r-2)
```pseudocode
For each round t (where 2 ≤ t ≤ r-2):
    cooperation_rate = count_cooperators_last_round / (n-1)
    
    IF cooperation_rate ≥ 0.5:
        action = DEFECT  // Exploit the cooperative majority
    ELSE IF cooperation_rate ≥ 0.3:
        // Mixed exploitation with occasional cooperation to maintain some cooperation
        IF random() < 0.7:
            action = DEFECT
        ELSE:
            action = COOPERATE
    ELSE:
        // Too few cooperators, occasional cooperation to rebuild
        IF random() < 0.3:
            action = COOPERATE
        ELSE:
            action = DEFECT
```

### 3. Punishment Mechanism
Track individual player behaviors and maintain aggression against consistent defectors:
```pseudocode
For each opponent j:
    defection_rate_j = count_defections_j / rounds_played
    
    IF defection_rate_j > 0.7:
        // Mark as hostile, never cooperate in response
        hostile_players.add(j)
```

### 4. Endgame Exploitation (Final 2 Rounds)
- **Round r-1**: Always DEFECT
- **Round r**: Always DEFECT
- **Rationale**: No future retaliation possible, so maximize immediate gain

### 5. Dynamic Adaptation
```pseudocode
// Adjust aggression based on environment
total_cooperation_rate = total_cooperations_observed / (total_rounds * (n-1))

IF total_cooperation_rate > 0.6:
    aggression_multiplier = 1.2  // Increase exploitation
ELSE IF total_cooperation_rate < 0.3:
    aggression_multiplier = 0.8  // Slightly reduce aggression to maintain some cooperation
ELSE:
    aggression_multiplier = 1.0
```

## Key Aggressive Features

### 1. **Exploitation Focus**
- Systematically defects when cooperation rates are high (≥50%)
- Takes advantage of cooperative players' contributions while keeping own endowment

### 2. **No Forgiveness**
- Once a player is marked as hostile (>70% defection rate), never cooperate with them again
- Maintains grudges throughout the entire game

### 3. **Endgame Domination**
- Guaranteed defection in final rounds regardless of history
- Exploits the fact that others might cooperate hoping for reciprocity

### 4. **Minimal Cooperation**
- Only cooperates strategically when necessary to maintain a minimal cooperation environment
- Never cooperates out of fairness or reciprocity

### 5. **Cold Calculation**
- All decisions based purely on payoff maximization
- No consideration for group welfare or fairness

## Expected Performance
This strategy should perform well against:
- Tit-for-tat and reciprocal strategies (exploits their initial cooperation)
- Always-cooperate strategies (maximum exploitation)
- Strategies that try to establish cooperation (takes advantage of their attempts)

The strategy accepts that it may perform poorly in environments with many other aggressive strategies, but prioritizes maximizing payoffs when cooperative opponents are present, which is the most likely scenario in a diverse tournament setting.
'''
