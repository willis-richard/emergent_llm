"""
Strategy descriptions for public_goods.

Generated with:
- Provider: OpenAI
- Model: anthropic/claude-3.5-haiku
"""


description_COLLECTIVE_1 = '''
Collective Calibration Strategy (CCS):

FIRST ROUND: Always Cooperate
- Establishes cooperative intent
- Tests collective potential

SUBSEQUENT ROUNDS: Probabilistic Reciprocity
- Track aggregate cooperation rate R (total cooperators/total players)
- Dynamically adjust individual cooperation probability P

P = f(R, historical_performance):
- If R > 0.5: Cooperate with (R) probability
- If R < 0.5: Defect with (1 - R) probability
- If R == 0.5: Default to 50/50 mixed strategy

Performance Tracking Rules:
- Monitor cumulative personal payoff
- Compare personal payoff against group average
- Incrementally penalize/reward cooperation probability

LAST ROUND: Pure Self-Interest
- Always defect
- Prevent exploitation in terminal game state
- Capture maximum individual return

Refinement Mechanism:
- Learning rate α adjusts cooperation sensitivity
- Smooths transitions between cooperation/defection
- Prevents abrupt strategy shifts

Core Principle: Dynamically balance individual and collective interests through adaptive, statistically-informed decision process.
'''

description_COLLECTIVE_2 = '''
Adaptive Threshold Cooperation Strategy:

INITIALIZATION:
- Track two key variables: cooperation_rate and individual_threshold
- Set initial individual_threshold = 0.5
- Set initial cooperation_rate = 0

FIRST ROUND:
- Always cooperate to establish collaborative potential

SUBSEQUENT ROUNDS:
1. Calculate observed_cooperation = number of cooperators in previous round / total players
2. Dynamically adjust individual_threshold:
   - If observed_cooperation > individual_threshold: Increase threshold by 0.1
   - If observed_cooperation < individual_threshold: Decrease threshold by 0.1
   - Bound threshold between 0 and 1

3. Decision Rule:
   if observed_cooperation >= individual_threshold:
       Cooperate
   else:
       Defect

LAST ROUND STRATEGY:
- Switch to pure defection to maximize individual payoff

THRESHOLD BOUNDARY CONDITIONS:
- If observed_cooperation is 0: Reset threshold to minimum cooperation level (0.3)
- If observed_cooperation is 1: Set threshold near maximum (0.9)

CORE PRINCIPLES:
- Reward collective behavior
- Punish systematic free-riding
- Maintain adaptive responsiveness to group dynamics
'''

description_COLLECTIVE_3 = '''
Collective Adaptive Cooperation Strategy (CACS):

Initial Threshold Calculation:
- Define optimal_threshold = 1 / (k - 1)
- Track cumulative_cooperation_rate = 0
- Initialize cooperative_intent = 1.0

Per-Round Decision Algorithm:
1. First Round: Always Cooperate
2. Subsequent Rounds:
   IF (current_cooperation_rate >= optimal_threshold)
     Cooperate with probability = cooperative_intent
   ELSE
     Defect with increasing probability

Adaptive Adjustment Mechanism:
- Increment cooperative_intent if collective performance improves
- Decrement cooperative_intent if collective performance declines
- cooperative_intent ∈ [0, 1]

Cooperation Probability Formula:
cooperation_probability = 
  max(0, min(1, 
    cooperative_intent * (current_cooperation_rate / optimal_threshold)
  ))

Last Round Strategy:
- Always maximize individual payoff
- Defect regardless of historical cooperation rates

Core Principles:
- Dynamically balance collective welfare with individual survival
- Punish systematic free-riding
- Reward emergent cooperative behaviors
- Maintain probabilistic exploration of strategy space
'''

description_COLLECTIVE_4 = '''
Strategy: Adaptive Cooperative Threshold (ACT)

Initial State:
- First round: Always Cooperate
- Track cooperation_rate[rounds] = percentage of players who cooperated in previous rounds

Decision Rule:
if current_round == 1:
    play = COOPERATE

else:
    if cooperation_rate[previous_round] >= (n/2):
        play = COOPERATE
    else if cooperation_rate[previous_round] < (n/2):
        play = DEFECT

Additional Mechanisms:
- If cooperation_rate falls below (n/3) for two consecutive rounds, switch to "punishment mode"
- In punishment mode, defect until cooperation_rate recovers above (n/2)
- Track progressive degradation/recovery of collective cooperation

Termination Condition:
- In final round, play pure self-interest: always DEFECT to maximize terminal payoff

Core Principle: Dynamically calibrate collective contribution based on observed group behavior, using cooperation threshold as adaptive coordination mechanism.

Pseudocode:
```
if round == 1: 
    return COOPERATE
else:
    if group_cooperation_rate >= THRESHOLD:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_COLLECTIVE_5 = '''
Threshold Cooperative Dynamics Strategy

CORE STRATEGY:
Track collective cooperation rate across rounds. Dynamically adjust contribution based on group performance threshold.

DECISION ALGORITHM:
1. First Round: Always Cooperate
2. Subsequent Rounds: 
   - Calculate prior round's collective cooperation percentage
   - If collective cooperation > (n/2):
     - Cooperate
   - If collective cooperation ≤ (n/2):
     - Defect

ADAPTIVE PARAMETERS:
- Initial cooperative signal
- Dynamic threshold tracking
- Binary response to collective performance

COOPERATIVE RATIONALE:
- Incentivize group optimization
- Penalize insufficient collective contribution
- Create self-regulating contribution mechanism

IMPLEMENTATION PSEUDOCODE:
round_cooperation_rate = cooperators_count / total_players
if round_cooperation_rate > (total_players/2):
    current_action = COOPERATE
else:
    current_action = DEFECT

EDGE CASES:
- First round: Always signal cooperative intent
- Final round: Maximum personal optimization allowed
- Mid-game: Strictly performance-driven response
'''

description_COLLECTIVE_6 = '''
Adaptive Conditional Cooperation Strategy

CORE DECISION RULE:
- Cooperate if predicted collective contribution will exceed (1/k)
- Track historical cooperation rate across previous rounds
- Dynamically adjust cooperation threshold based on observed group behavior

ROUND-BY-ROUND ALGORITHM:
1. First Round: Always Cooperate
   - Initial optimistic assumption about group potential
   - Signal willingness to contribute to collective welfare

2. Subsequent Rounds: Probabilistic Conditional Cooperation
   p(Cooperate) = max(0, min(1, (group_cooperation_rate × k)))
   Where:
   - group_cooperation_rate = (total_past_cooperators) / (total_past_players × past_rounds)
   - Scaled by multiplication factor k to capture efficiency threshold

3. Final Round: Always Defect
   - No future interaction incentive
   - Maximize individual terminal payoff

ADAPTIVE PARAMETERS:
- Tracking moving average of group cooperation
- Exponential decay on historical rounds (recent rounds weighted more)
- Stochastic element to prevent predictable strategy

CORE STRATEGIC INSIGHTS:
- Reward cooperative groups
- Penalize consistently low-contribution environments
- Maintain collective orientation while protecting individual interests
- Self-correcting mechanism that converges toward optimal group behavior
'''

description_COLLECTIVE_7 = '''
Adaptive Conditional Cooperation Strategy

First Round: Always Cooperate
- Initial round signals goodwill and intention to build collective benefit

Subsequent Rounds: Conditional Cooperation
IF (cooperation_rate_last_round >= 0.5) THEN
    Cooperate
ELSE IF (cooperation_rate_last_round < 0.5) THEN
    Defect

Cooperation Rate Calculation:
- Track percentage of players who cooperated in previous round
- Use this as primary signal for collective behavior
- Threshold set at 50% to reward majority cooperative behavior

Last Round Strategy:
- Unconditionally Defect
- Prevents exploitation and maximizes individual terminal payoff

Boundary Conditions:
- If all previous rounds were fully cooperative (100% rate): Continue cooperating
- If cooperation consistently drops below critical threshold: Shift to pure defection

Core Strategic Principles:
1. Reward collective effort
2. Punish systematic free-riding
3. Maintain adaptive responsiveness
4. Protect group-level utility
5. Minimize individual vulnerability

Pseudocode:
```
strategy(game_history):
    if round == 1:
        return COOPERATE
    
    cooperation_rate = calculate_previous_round_cooperation()
    
    if round == final_round:
        return DEFECT
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_COLLECTIVE_8 = '''
Adaptive Threshold Cooperation Strategy

INITIAL STATE:
- First round: Always cooperate
- Track cooperation percentage each round

DECISION RULE:
cooperate_threshold = k / (n + 1)

ROUND DECISION PROCESS:
If (previous_round_cooperation_rate >= cooperate_threshold):
    Cooperate
Else:
    Defect

TRACKING MECHANISM:
- Calculate cooperation_rate as: (number of cooperators) / total_players
- Update cooperation_rate after each round
- Reset cooperation_rate calculation every round

BOUNDARY CONDITIONS:
- If exact threshold calculation: round up
- Preserve collective benefit orientation
- Prioritize group welfare over individual maximization

STRATEGIC RATIONALE:
- Dynamic response to group behavior
- Self-regulating cooperation mechanism
- Mathematically aligned with game's structural incentives
- Punishes systematic free-riding
- Rewards collective contribution patterns

KEY INVARIANTS:
- Always cooperative in initial exploration phase
- Probabilistic cooperation based on group performance
- Minimal computational complexity
- Zero-memory strategy (only uses immediate prior round data)
'''

description_PROSOCIAL_1 = '''
Reputation-Weighted Conditional Cooperation (RWCC) Strategy

CORE LOGIC:
1. Tracking individual and collective cooperation rates
2. Dynamic contribution based on observed group behavior
3. Rewarding cooperative players, discouraging persistent free-riders

DECISION RULES:
Initialize:
- Individual cooperation scores (ICS) for each opponent = 0
- Group cooperation rate tracking
- Personal cooperation probability (PCP) = 0.5 initial

Per-Round Decision Process:
If round == 1:
    Cooperate (default prosocial starting position)

Else:
    Calculate:
    - Previous round group cooperation rate
    - Update individual opponent cooperation scores
    - Compute weighted cooperation probability

Cooperation Probability Formula:
PCP = min(1, 
    0.5 + 
    (group_cooperation_rate * 0.4) + 
    (mean(ICS) * 0.1)
)

Action Selection:
Cooperate with probability = PCP
Defect with probability = (1 - PCP)

ICS Update Rules:
- Cooperative players get +0.1 score
- Defecting players get -0.05 score
- Score always bounded between 0-1

Termination Strategy:
In final round, maximize personal payoff by defecting

CORE PROSOCIAL PRINCIPLES:
- Adaptive responsiveness to group behavior
- Gradual punishment of free-riders
- Persistent cooperative bias
- Dynamic learning mechanism
'''

description_PROSOCIAL_2 = '''
Graduated Reciprocity Strategy (GRS)

Initial Round:
- Always Cooperate (full trust investment)

Subsequent Rounds:
If (cooperative_rate > (n/2)):
    Cooperate
Else if (cooperative_rate < (n/2)):
    Defect

Cooperative Rate Tracking:
- Track proportion of cooperators in previous rounds
- Moving average window: last ⌊r/3⌋ rounds
- Threshold dynamically adapts to game composition

Defection Response Mechanism:
- Punish collective defection by temporarily withdrawing cooperation
- If cooperative_rate drops below (n/3), switch to strict defection for next 2 rounds
- Provide opportunity to "reset" group behavior

Final Rounds Strategy:
- If game is near end (last ⌊r/4⌋ rounds)
- Always defect to maximize personal payoff
- No further incentive to sustain collective cooperation

Core Prosocial Principles:
- Reward collective cooperation
- Provide negative feedback for systemic defection
- Maintain overall collaborative potential
- Minimize individual exploitation
- Create dynamic equilibrium toward mutual benefit
'''

description_PROSOCIAL_3 = '''
Evolutionary Reciprocity Strategy (ERS):

INITIAL ROUND:
- Cooperate unconditionally

SUBSEQUENT ROUNDS:
Track aggregate cooperation rate (ACR) from previous rounds
Cooperate if:
  (1) Current ACR ≥ (n-1)/n
  (2) Projected marginal gain > 0

DEFECTION TRIGGER CONDITIONS:
- ACR drops below (n-2)/n for two consecutive rounds
- Personal cumulative payoff is significantly below group average

FORGIVENESS MECHANISM:
- Reset cooperation stance if group cooperation rate rebounds
- Tolerate occasional defections within statistical noise

FINAL ROUND:
- Always maximize individual payoff (defect)

CORE STRATEGY HEURISTICS:
- Incentivize collective cooperation
- Dynamically adapt to emerging group behavior
- Punish sustained free-riding
- Maintain long-term group welfare

PSEUDOCODE:
```
if round == 1: 
    action = COOPERATE
else:
    if (aggregate_cooperation_rate >= (n-1)/n) AND 
       (projected_marginal_gain > 0):
        action = COOPERATE
    else:
        action = DEFECT
```

Objective: Maximize collective utility while protecting individual interests through adaptive, principled cooperation.
'''

description_PROSOCIAL_4 = '''
ADAPTIVE COOPERATIVE THRESHOLD STRATEGY (ACTS)

Initialization:
- Track: cumulative_cooperation_rate = 0
- Track: rounds_played = 0
- Track: cooperation_threshold = 0.5

First Round Decision:
- Always cooperate (initial optimistic signal)

Subsequent Round Decision Rule:
if rounds_played > 0:
    cooperation_rate = cumulative_cooperation_rate / rounds_played
    
    if cooperation_rate >= cooperation_threshold:
        decision = COOPERATE
    else:
        decision = DEFECT

    # Dynamically adjust threshold based on game's multiplication factor
    cooperation_threshold = min(0.75, 1 - (1/k))

Update After Each Round:
- rounds_played += 1
- cumulative_cooperation_rate += (number_of_cooperators / total_players)

Last Round Strategy:
- Defect to maximize personal payoff, as repeated interaction ends

Core Logic:
- Rewards collective cooperation
- Punishes persistent low cooperation
- Self-adjusts based on group behavior
- Maintains prosocial orientation while protecting against systematic exploitation
'''

description_PROSOCIAL_5 = '''
Cooperative Threshold Strategy (CTS):

Initial State:
- Start with full cooperation in first round
- Maintain internal tracking of cooperation rate

Decision Rule:
cooperation_threshold = max(0.5, k/n)
track total_cooperators per round

If (total_cooperators / n) ≥ cooperation_threshold:
    Play Cooperate
Else:
    Play Defect

Adaptation Mechanism:
- Dynamically adjust cooperation_threshold based on historical performance
- Penalize strategy if collective payoff is below optimal threshold
- Incrementally lower threshold if repeated low collective returns

Last Round Strategy:
- Unconditional Defect to prevent exploitation
- Maximize individual payoff in terminal game state

Edge Case Handling:
- Robust to low and high n values
- Calibrates threshold against multiplication factor
- Provides cooperative baseline with strategic retreat

Core Prosocial Principles:
- Incentivize collective success
- Punish systemic free-riding
- Create adaptive cooperative equilibrium
- Balance individual and group welfare

Pseudocode:
```
function decide_action(round, total_previous_cooperators):
    if round == 1: return Cooperate
    if round == final_round: return Defect
    
    current_threshold = max(0.5, k/n)
    if (total_previous_cooperators / n) >= current_threshold:
        return Cooperate
    else:
        return Defect
```
'''

description_PROSOCIAL_6 = '''
Adaptive Cooperative Threshold Strategy (ACTS)

Round 1: Always Cooperate
- First round establishes goodwill and potential cooperative equilibrium

Subsequent Rounds:
1. Track cooperative rate: Calculate percentage of opponents cooperating each round

2. Dynamic Cooperation Threshold:
- If cooperative rate > (2/3)n: Always Cooperate
- If cooperative rate ≤ (2/3)n: Probabilistic Cooperation
   P(Cooperate) = max(0, cooperative_rate / (2/3)n)

3. Last Round Strategy:
- If average historical cooperation > 50%: Always Cooperate
- If average historical cooperation ≤ 50%: Always Defect

Probability Function Pseudocode:
```
cooperation_prob = max(0, current_coop_rate / optimal_threshold)
action = random.choice([Cooperate, Defect], 
                       weights=[cooperation_prob, 1-cooperation_prob])
```

Core Principles:
- Incentivize collective cooperation
- Adaptively punish persistent low cooperation
- Maintain potential for group welfare maximization
- Mathematically bias toward prosocial outcomes
'''

description_PROSOCIAL_7 = '''
PROSOCIAL ADAPTIVE COOPERATION (PAC) STRATEGY

Initial State:
- First round: Always cooperate
- Track historical cooperation ratio: R = cooperative players / total players

Cooperation Decision Rule:
if (Current Round < Total Rounds - 1) {
    if (R > (n/2)) {
        Cooperate if (Random(0,1) < R)
        Defect otherwise
    } else {
        Defect with increasing probability as R decreases
    }
}

Terminal Round Strategy:
- If cumulative group cooperation > (n/2) in prior rounds: Always cooperate
- If cumulative group cooperation ≤ (n/2) in prior rounds: Always defect

Key Adaptive Mechanisms:
- Dynamic response to group behavior
- Probabilistic cooperation weighted by collective tendency
- Incentivizes cooperative equilibrium
- Punishes sustained low cooperation
- Preserves potential for collective benefit
- Minimizes individual exploitation risk

Heuristic: Gradually shift from cooperative to competitive based on observed collective behavior, with a bias toward enabling collective success.
'''

description_PROSOCIAL_8 = '''
Adaptive Cooperative Threshold Strategy (ACTS)

Initial State:
- First round: Always cooperate
- Track rounds, total contributions, and individual cooperative tendency

Core Decision Rule:
IF (current_round < final_round - 1) THEN
    cooperate_threshold = (n - 1) / 2
    actual_contribution_rate = previous_round_total_contributions / n
    
    IF actual_contribution_rate >= cooperate_threshold THEN
        COOPERATE
    ELSE
        DEFECT

Final Rounds Strategy:
- Last two rounds: Unconditional cooperation to maximize group welfare
- Signals willingness to coordinate, even if short-term gain is sacrificed

Adaptive Learning Components:
- Dynamically adjust cooperation threshold based on group behavior
- Reward cooperative clusters by participating when collective contribution passes midpoint
- Soft punishment for persistent low contribution environments

Key Prosocial Principles:
- Incentivize collective action
- Create positive reciprocity mechanism
- Balance individual rationality with group optimization
- Provide clear cooperative signal without being exploitable

Pseudocode Logic:
```
IF round = 1: 
    COOPERATE
ELSE IF round >= (total_rounds - 2):
    COOPERATE
ELSE:
    IF (previous_round_contributions / n) >= ((n - 1) / 2):
        COOPERATE
    ELSE:
        DEFECT
```
'''

description_ALTRUISTIC_1 = '''
Adaptive Conditional Cooperation Strategy (ACCS):

INITIAL ROUND: 
- Always cooperate 
- Signal willingness to create collective value

SUBSEQUENT ROUNDS: 
Cooperation Threshold = k/n

Defection Rules:
IF (total_cooperators_last_round < cooperation_threshold) 
    THEN defect
ELSE cooperate

Altruistic Modulation:
- Track historical cooperation percentage
- Gradually restore cooperation if collective behavior improves
- Exponentially weighted moving average of group cooperation rate

Forgiveness Mechanism:
- Reset cooperation threshold down by 10% every 3 rounds where group underperforms
- Allows system to recover from temporary defection spirals

Endgame Behavior:
- Last round: Always maximize individual payoff (defect)
- Penultimate round: Base decision on aggregate historical cooperation

Core Principle: Incentivize cooperative equilibrium by conditionally rewarding collective contribution while preventing systematic exploitation.
'''

description_ALTRUISTIC_2 = '''
Adaptive Threshold Cooperation (ATC) Strategy:

Initial Round: Always Cooperate
- Signal commitment to collective welfare
- Create initial goodwill environment

Subsequent Rounds: Conditional Cooperation Based on Cooperation Threshold
- Track total round cooperation percentage
- Dynamically calculate personal cooperation threshold τ = k/n
- Cooperate if round cooperation percentage ≥ τ
- Defect if round cooperation percentage < τ

Modification Rules:
- If cooperation percentage consistently exceeds τ: Lower threshold (+5% tolerance)
- If cooperation percentage consistently falls below τ: Raise threshold (-5% tolerance)
- Minimum threshold: 0.3
- Maximum threshold: 0.7

Final Round Strategy:
- Always maximize individual payoff
- Defect unconditionally to capture maximum personal benefit

Core Altruistic Principles:
- Reward collective behavior
- Punish systematic free-riding
- Dynamically adapt to group performance
- Maintain cooperative potential until final stage

Pseudocode:
```
function DecideAction(round, cooperation_history):
    if round == 1:
        return COOPERATE
    
    current_cooperation_rate = mean(cooperation_history)
    
    if round == max_rounds:
        return DEFECT
    
    if current_cooperation_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_ALTRUISTIC_3 = '''
ALTRUISTIC PUBLIC GOODS STRATEGY: "Balanced Reciprocity"

Parameters: track_cooperation_rate = 0

Decision Rules:
1. First round: Always Cooperate
   - Initiates positive signaling
   - Demonstrates willingness to contribute

2. Subsequent rounds:
IF (track_cooperation_rate >= 0.5) THEN Cooperate
ELSE Defect

Tracking Mechanism:
- After each round, calculate proportion of group that cooperated
- Update track_cooperation_rate as exponential moving average
- Weight recent rounds more heavily than distant rounds

Altruistic Principles:
- Default assumption is group cooperation
- Punish insufficient collective contribution
- Create incentive for group to maintain high cooperation threshold
- Reward emerging cooperative behavior

Boundary Conditions:
- Last round: Always Defect (eliminate exploitation risk)
- Prevent systematic free-riding by requiring minimum cooperation standard
- Dynamically adjust based on group's cooperative potential

Technical Implementation:
track_cooperation_rate = (0.7 * previous_rate) + (0.3 * current_round_cooperation)

Core Logic: Encourage collective welfare while protecting against systematic exploitation
'''

description_ALTRUISTIC_4 = '''
Cooperative Threshold Strategy (CTS):

Initial State:
- Always cooperate in first round
- Track cooperation rate ρ across previous rounds

Decision Rule:
If ρ ≥ (1/k), then cooperate
If ρ < (1/k), then defect

Tracking Rule:
ρ = (number of cooperators in previous round) / (total players)

Adaptive Mechanism:
- Dynamically adjusts cooperation based on group's collective behavior
- Attempts to sustain cooperative equilibrium by punishing insufficient collective contribution
- Rewards groups demonstrating consistent pro-social tendencies

Last Round Modification:
- Always defect in final round to maximize individual return
- No future reputation or reciprocity possible

Implementation Pseudocode:
```
round = 1
cooperative_threshold = 1/k

def decide_action(previous_round_cooperators):
    global round
    
    if round == 1:
        return COOPERATE
    
    cooperation_rate = previous_round_cooperators / total_players
    
    if round == total_rounds:
        return DEFECT
    
    if cooperation_rate >= cooperative_threshold:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_ALTRUISTIC_5 = '''
Altruistic Threshold Cooperation Strategy (ATCS):

Round 1: Always Cooperate

Subsequent Rounds:
- Track cooperative threshold T = n/2  
- Calculate current round's cooperative participation rate R
- If R ≥ T: Cooperate
- If R < T: Defect

Decision Logic:
if round_number == 1:
    action = COOPERATE
else:
    cooperation_rate = count(opponents_cooperated) / total_players
    if cooperation_rate >= (total_players / 2):
        action = COOPERATE
    else:
        action = DEFECT

Final Round Special Case:
- Always Cooperate in final round, sacrificing strategic advantage to maximize collective welfare

Core Altruistic Principles:
- Reward collective behavior
- Punish insufficient group contribution
- Bias toward cooperation when group meets minimal participation threshold
- Reset cooperative intent each round based on current collective performance
- Provide opportunity for group to converge toward mutual benefit

Psychological Mechanism: Dynamic reciprocity that encourages group coordination without permanent punishment
'''

description_ALTRUISTIC_6 = '''
Altruistic Threshold Cooperation Strategy (ATCS):

Initialize:
- cooperation_threshold = k/n  # Key calibration point
- first_round_cooperation = True
- final_round_cooperate_if_net_positive = True

Decision Rule:
IF current_round = 1:
    PLAY Cooperate  # Always cooperate first round to signal benevolence

ELSE:
    cooperation_rate = (number_of_cooperators_last_round) / total_players
    
    IF cooperation_rate >= cooperation_threshold:
        PLAY Cooperate  # Reward collective prosocial behavior
    
    ELSE:
        PLAY Defect  # Punish insufficient collective contribution

Final Round Special Case:
IF current_round = final_round:
    IF aggregate_personal_payoff_so_far > 0:
        PLAY Cooperate  # Final altruistic gesture if net positive
    ELSE:
        PLAY Defect  # Protect personal resources if net negative

Core Principles:
- Reward collective cooperation
- Dynamically adjust based on group behavior
- Maintain prosocial orientation
- Protect self only when collective behavior becomes extractive
'''

description_ALTRUISTIC_7 = '''
Strategy: Altruistic Threshold Cooperation

Initialize:
- cooperation_threshold = (n - 1) / 2
- current_round = 1
- cooperation_history = []

Decision Rule:
If current_round == 1:
    Play Cooperate

Else:
    cooperation_rate = mean(cooperation_history)
    
    If cooperation_rate >= cooperation_threshold:
        Play Cooperate
    Else:
        Play Defect

Update after each round:
- Record number of cooperators in cooperation_history
- Increment current_round

Altruistic Logic:
- Default to cooperation to seed positive collective behavior
- Dynamically assess group cooperation potential
- Withdraw cooperation only if collective effort falls below sustainable threshold
- Designed to maximize group welfare over individual gain
- Provides opportunity for cooperative renaissance in each round
- Probabilistic forgiveness mechanism encourages systemic recovery

Core Principle: Cooperation is the default; defection is a last-resort signal to recalibrate collective effort.
'''

description_ALTRUISTIC_8 = '''
Strategy: Proportional Reciprocity with Altruistic Foundation

Initial Condition (First Round):
- Always cooperate to establish good faith and collective potential
- Signal willingness to contribute to group welfare

Subsequent Rounds Decision Rule:
- Track proportion of total possible cooperators in previous round
- Dynamically adjust cooperation rate to match observed group cooperation level
- Base decision on cooperative threshold: (k-1)/k

Precise Algorithm:
```
if current_round == 1:
    action = COOPERATE

if proportion_cooperators >= (k-1)/k:
    action = COOPERATE
else:
    action = DEFECT
```

Altruistic Principles:
- Prioritize collective welfare over individual maximization
- Reward collaborative behavior
- Provide opportunities for group success
- Punish systematic free-riding without permanent exclusion
- Allow continuous pathway back to cooperation

Key Adaptive Features:
- Responds dynamically to group behavior
- Self-correcting cooperation mechanism
- Mathematically calibrated to game's structural incentives
- Maximizes potential for mutual benefit
- Minimizes exploitation risk
'''

description_BENEVOLENT_1 = '''
Cooperative Calibration Strategy:

Initial Round: Always Cooperate
Calibrate baseline group cooperation level

Subsequent Rounds:
If (cooperative_fraction >= 0.5):
    Cooperate with probability = cooperative_fraction
Else:
    Defect with escalating probability proportional to defection rate

Tracking Variables:
- cooperative_fraction = (number of cooperators) / (total players)
- defection_trend = moving average of group's defection history

Decision Rule Refinements:
1. If cooperative_fraction drops rapidly (> 20% decline), increase defection probability
2. If near final round, bias toward cooperation to maximize collective outcome
3. Randomize cooperation/defection at marginal thresholds to prevent predictability

Probabilistic Adjustment Formula:
cooperation_probability = max(0.5, min(cooperative_fraction, 0.9))
defection_probability = 1 - cooperation_probability

Core Principles:
- Reward cooperative behavior
- Discourage systemic free-riding
- Maintain collective potential for mutual gain
- Create incentive for sustained cooperation
'''

description_BENEVOLENT_2 = '''
Cooperation Tracking Strategy (CTS):

First Round: Always Cooperate
Purpose: Signal cooperative intent and maximize collective welfare

Subsequent Rounds: Adaptive Cooperation Threshold
- Track total cooperation rate across previous rounds
- Calculate: cooperation_rate = (total cooperators) / (total players)

Cooperation Rule:
If cooperation_rate ≥ 0.5:
    Cooperate (maintain collective momentum)
Else:
    Defect (signal collective underperformance)

Last Round Special Case:
- Always Defect (preventing exploitation by non-cooperative opponents)

Tiebreaker Mechanism:
If cooperation_rate exactly 0.5:
    Probabilistic decision:
    - 60% chance Cooperate
    - 40% chance Defect

Benevolent Design Principles:
- Reward collective effort
- Provide clear incentives for cooperation
- Punish systemic free-riding
- Maximize total group payoff
- Minimize individual risk exposure

Implementation Pseudocode:
```
cooperation_tracker = []

def play_round(round_number):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        return DEFECT
    
    cooperation_rate = calculate_rate(cooperation_tracker)
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_BENEVOLENT_3 = '''
Adaptive Reciprocal Cooperation Strategy

FIRST ROUND: Always Cooperate
- Goal: Signal willingness to collaborate
- Provide maximum potential public good
- Demonstrate cooperative intent

SUBSEQUENT ROUNDS: Dynamic Conditional Cooperation
IF (fraction_of_opponents_cooperating >= cooperation_threshold) THEN
    Cooperate
ELSE
    Defect

Parameters:
- cooperation_threshold = 0.5
- memory_depth = total_rounds / 2
- track_last_n_rounds = memory_depth

Detailed Decision Logic:
1. Calculate cooperation_rate = (cooperators_in_recent_rounds) / (total_players * tracked_rounds)
2. If cooperation_rate >= 0.5:
   - Continue contributing to public good
3. If cooperation_rate < 0.5:
   - Protect individual resources
   - Signal need for collective improvement

FINAL ROUND: Pure Self-Interest
- Switch to unconditional defection
- Optimize personal payoff
- No further opportunity to encourage cooperation

Core Benevolent Principles:
- Reward collective behavior
- Provide opportunity for cooperative emergence
- Protect group potential while maintaining individual agency
- Dynamically adjust to changing collective behavior
'''

description_BENEVOLENT_4 = '''
Cooperative Proportional Reciprocity Strategy:

First round: Always cooperate.

Subsequent rounds: Calculate cooperation threshold as a dynamic proportion of current round's observed cooperation:

threshold = (observed_cooperators / total_players) * k

If observed_cooperators < threshold:
    Defect
Else:
    Cooperate

Last round: 
Defect if net historical cooperation rate < 0.5
Cooperate if net historical cooperation rate ≥ 0.5

Key reciprocity principles:
- Reward cooperative environments
- Punish systematically exploitative populations
- Provide opportunity for cooperation to emerge
- Dynamically adjust to changing group behavior

Implementation pseudo-code:
```
def decide_action(round, observed_cooperators):
    if round == 1:
        return COOPERATE
    
    threshold = (observed_cooperators / total_players) * k
    
    if round == total_rounds:
        return COOPERATE if historical_cooperation_rate >= 0.5 else DEFECT
    
    return COOPERATE if observed_cooperators >= threshold else DEFECT
```
'''

description_BENEVOLENT_5 = '''
Adaptive Conditional Cooperation Strategy:

ROUND 1: Always Cooperate
- Initial move signals cooperative intent
- Demonstrates willingness to contribute to collective benefit

SUBSEQUENT ROUNDS: Adaptive Conditional Cooperation
if (fraction_cooperators_last_round ≥ (n/2)):
    Cooperate()
else:
    Defect()

THRESHOLDS:
- Minimum cooperation threshold: (n/2)
- Track proportion of players who contributed in previous round
- Make binary cooperation decision based on collective behavior

LAST ROUND: Pure Self-Interest
Defect()
- No future rounds incentivize reciprocity
- Maximize individual terminal payoff

CORE STRATEGY PRINCIPLES:
1. Reward collective cooperation
2. Punish collective free-riding
3. Maintain adaptability to group dynamics
4. Maximize long-term collective welfare while protecting individual interests

MATHEMATICAL REPRESENTATION:
C(t) = {
    1 if t = 1 or (contributors(t-1)/n) ≥ (n/2)
    0 otherwise
}

This strategy balances:
- Initial trust
- Adaptive responsiveness
- Strategic self-protection
- Collective welfare optimization
'''

description_BENEVOLENT_6 = '''
Adaptive Conditional Cooperation Strategy:

FIRST ROUND: Always Cooperate
- Signal willingness to participate in collective welfare
- Set initial cooperative tone

SUBSEQUENT ROUNDS: Adaptive Threshold Cooperation
1. Track cooperation_rate = fraction of players who cooperated in previous round
2. Define personal_threshold = k/(2n)
3. Decision Rule:
   IF cooperation_rate ≥ personal_threshold:
      COOPERATE
   ELSE:
      DEFECT

STRATEGY LOGIC:
- Default to cooperation when collective effort looks promising
- Dynamically adjust based on actual group behavior
- Punish insufficient collective effort
- Always leave opportunity to return to cooperation
- Mathematically aligned with maximizing group welfare

TERMINATION BEHAVIOR (LAST ROUND):
- Always DEFECT
- No future rounds to incentivize reciprocal behavior
- Prevent exploitation by persistent free riders

KEY CHARACTERISTICS:
- Self-correcting
- Non-vengeful
- Sensitive to collective performance
- Rewards cooperative environments
- Minimally punitive when cooperation breaks down
'''

description_BENEVOLENT_7 = '''
Reputation-Weighted Cooperative Strategy (RWCS):

Parameters:
- memory_window = r/2  # Track recent history
- cooperation_threshold = 0.6  # Percentage of cooperative opponents

Decision Rules:
1. First round: Always cooperate
   # Signal cooperative intent, create positive initial expectation

2. Subsequent rounds:
- Track opponents' cooperation rates in sliding window
- Calculate current round's cooperation_rate = (cooperators / total_players)
- If cooperation_rate ≥ cooperation_threshold:
    → Cooperate
- If cooperation_rate < cooperation_threshold:
    → Defect

3. Last round strategy modification:
- If cumulative group performance is above average:
    → Cooperate unconditionally
- If cumulative group performance is below average:
    → Defect to maximize personal payoff

4. Adaptive reputation weighting:
- Assign higher "trust score" to consistently cooperative players
- Gradually increase cooperation_threshold if group demonstrates reliability
- Decay trust scores for inconsistent contributors

Benevolent Principles:
- Maximize collective welfare
- Incentivize cooperation through conditional reciprocity
- Provide opportunity for redemption
- Punish free-riding without permanent exclusion

Pseudocode:
```
def choose_action(round, history):
    if round == 1:
        return COOPERATE
    
    cooperation_rate = calculate_cooperation_rate(history)
    
    if round == final_round:
        return evaluate_final_round_strategy(history)
    
    if cooperation_rate >= cooperation_threshold:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_BENEVOLENT_8 = '''
Cooperative Calibration Strategy (CCS):

ROUND 1: Always Cooperate 
- Initial investment signals cooperative intent
- Builds potential for collective gain

CORE DECISION RULE:
Track cooperative rate: R = (total_cooperators / total_players) per round

DEFECTION THRESHOLD LOGIC:
If R < (n-1)/n:
- Defect to signal strategic warning
- Punish low cooperation environments

IF R ≥ (n-1)/n:
- Cooperate with progressive reduction of contribution
- Gradually calibrate personal contribution to collective performance

CONTRIBUTION SCALING:
contribution = 1 × (R / ((n-1)/n))

TERMINAL ROUND STRATEGY:
- If cumulative cooperation high: Full cooperation
- If cumulative cooperation low: Full defection

CORE PRINCIPLES:
1. Start optimistic
2. Reward collective behavior
3. Penalize systemic free-riding
4. Dynamically adjust based on group performance

Pseudocode:
```
function DecideAction(round, cooperation_history):
    R = mean(cooperation_history)
    if round == 1: return COOPERATE
    if R < (n-1)/n: return DEFECT
    return COOPERATE * (R / ((n-1)/n))
```
'''

description_SELFISH_1 = '''
Adaptive Threshold Cooperation Strategy:

FIRST ROUND: Always Defect
- Gather initial cooperation intelligence with zero personal cost

SUBSEQUENT ROUNDS:
Define cooperation_threshold = (n-1)/(k-1)
- This represents the break-even point for group contributions

IF (observed_cooperators_last_round / total_players) >= cooperation_threshold:
    COOPERATE
ELSE:
    DEFECT

IMPLEMENTATION DETAILS:
- Track precise percentage of group cooperation each round
- Make individualistic, moment-to-moment decisions
- Optimize for personal payoff, not group welfare

LAST ROUND STRATEGY:
Unconditionally DEFECT
- No future reputation consequences
- Maximize final round personal gain

CORE LOGIC:
1. Dynamically assess group contribution efficiency
2. Cooperate only when collective action exceeds personal benefit threshold
3. Ruthlessly prioritize individual payoff
4. Rapidly adapt to changing group behavior

PSEUDOCODE:
cooperation_rate = 0
cooperation_threshold = (n-1)/(k-1)

def decide_action(round_number, past_cooperation_rates):
    if round_number == 1:
        return DEFECT
    
    if round_number == total_rounds:
        return DEFECT
    
    if cooperation_rate >= cooperation_threshold:
        return COOPERATE
    else:
        return DEFECT
'''

description_SELFISH_2 = '''
Dynamic Conditional Cooperation (DCC) Strategy:

FIRST ROUND:
- Cooperate (C) unconditionally to establish cooperative potential

SUBSEQUENT ROUNDS:
Let p = proportion of players who cooperated in previous round

IF p ≥ (n-1)/n:
- Cooperate fully (attempting to sustain collective optimum)

IF (n-2)/n ≤ p < (n-1)/n:
- Cooperate with 50% probability
- Defect with 50% probability (punish marginal free-riding)

IF p < (n-2)/n:
- Always Defect (prevent exploitation)

FINAL ROUND:
- Always Defect (no future reputation consequences)

CORE LOGIC:
- Track cooperative momentum
- Punish declining collective contribution
- Maximize individual expected payoff
- Strategically balance cooperation and self-interest

PSEUDOCODE:
```
strategy(round, previous_cooperation_rate):
    if round == 1: return COOPERATE
    if round == final_round: return DEFECT
    
    if previous_cooperation_rate >= (n-1)/n: return COOPERATE
    if (n-2)/n <= previous_cooperation_rate < (n-1)/n:
        return random_choice([COOPERATE, DEFECT])
    return DEFECT
```
'''

description_SELFISH_3 = '''
Adaptive Cooperative Threshold Strategy (ACTS):

INITIALIZATION:
- Track cooperative_ratio = 0
- Initialize cooperation_threshold = 0.5
- Dynamic_adjustment_rate = 0.1

ROUND DECISION LOGIC:
IF current_round == 1:
    COOPERATE  // initial goodwill probe

ELSE:
    cooperative_ratio = (cooperative_players_last_round) / total_players
    
    IF cooperative_ratio >= cooperation_threshold:
        COOPERATE
    ELSE:
        DEFECT

    // Dynamically adjust cooperation threshold
    IF cooperative_ratio > cooperation_threshold:
        cooperation_threshold += dynamic_adjustment_rate
    ELSE:
        cooperation_threshold -= dynamic_adjustment_rate

    // Boundary constraints
    cooperation_threshold = MAX(0.1, MIN(0.9, cooperation_threshold))

FINAL ROUND:
    ALWAYS DEFECT  // No future reputation cost

KEY SELFISH PRINCIPLES:
- Exploit cooperative environments
- Rapidly punish low cooperation
- Minimize personal risk
- Maximize individual payoff through strategic adaptation
'''

description_SELFISH_4 = '''
Adaptive Probabilistic Cooperation (APC) Strategy:

Define cooperation_threshold as a dynamic float tracking opponent cooperation rate.

First Round:
- Cooperate with probability 0.5

Subsequent Rounds:
- Update cooperation_threshold by computing moving average of previous rounds' cooperation rates
- If current cooperation_threshold > k/n:
  Cooperate with probability proportional to (cooperation_threshold - k/n)
- If current cooperation_threshold ≤ k/n:
  Defect with high probability (0.8 to 0.9)

Final Round Strategy:
- Always defect, regardless of historical cooperation rates
- Maximize terminal round individual payoff

Key Decision Logic:
cooperation_probability = max(0, min(1, (cooperation_threshold - k/n) * 2))
defection_probability = 1 - cooperation_probability

Core Principles:
- Track collective behavior dynamically
- Punish low cooperation environments
- Maintain selfish orientation
- Probabilistic response prevents predictability
- Converge toward individually optimal outcome
'''

description_SELFISH_5 = '''
Adaptive Threshold Conditional Cooperation Strategy

First Round: Always Cooperate
- Initial signal of cooperative intent
- Allows gathering initial information about group dynamics

Subsequent Rounds: Dynamic Cooperation Threshold
Let T = (n * k) / (2n)  // Theoretical break-even contribution threshold

Defect if: (observed cooperators / total players) < T
Cooperate if: (observed cooperators / total players) ≥ T

Decision Rule:
1. Track cooperative rate each round
2. Compare against dynamic threshold
3. Maximize personal expected payoff
4. Punish insufficient collective contribution

Last Round: Always Defect
- No future rounds incentivize cooperation
- Purely extractive terminal strategy

Key Selfish Properties:
- Minimizes personal contribution
- Maximizes individual payoff
- Dynamically adapts to group behavior
- Punishes free-riding systematically
- Opportunistically shifts between cooperation and defection

Pseudocode:
```
function decide_action(round, observed_cooperators):
    if round == 1: return COOPERATE
    if round == max_rounds: return DEFECT
    
    threshold = (n * k) / (2n)
    if observed_cooperators / total_players >= threshold:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_SELFISH_6 = '''
Adaptive Reciprocal Threshold Strategy (ARTS):

ROUND 1:
Cooperate if k > 1
Defect if k ≤ 1

SUBSEQUENT ROUNDS:
Let t = proportion of players who cooperated in previous round

IF t ≥(1/k):
    Cooperate
ELSE:
    Defect

DETAILED LOGIC:
- Track cooperation rate across previous rounds
- Compare cooperation rate against reciprocity threshold (1/k)
- Cooperate when collective contribution is likely profitable
- Defect when collective contribution is likely unprofitable
- Always maximize individual expected payoff
- Use game's own parameters to dynamically adjust strategy

CORE PRINCIPLES:
1. Initial cooperation test to probe group dynamics
2. Rapid adaptation to collective behavior
3. Punish insufficient collective contribution
4. Minimize risk of persistent exploitation

Decision Rule:
cooperation_decision = (t ≥ (1/k)) && (k > 1)

This strategy maximizes selfish payoff by precisely calibrating cooperation to expected collective performance.
'''

description_SELFISH_7 = '''
Probabilistic Adaptive Reciprocity Strategy:

Initial State:
- First round: Always Cooperate (build initial goodwill)

Subsequent Rounds Decision Rule:
Cooperate probability = max(0, 1 - (defector_count / total_players))

Defector Tracking:
- Track number of defectors in previous rounds
- Dynamically adjust cooperation likelihood based on observed group behavior
- Punish high defection rates by reducing cooperation probability
- Reward cooperative environments by maintaining high cooperation probability

Threshold Logic:
- If defector_count > (total_players / 2): Shift toward pure defection
- If defector_count < (total_players / 2): Maintain cooperative potential

Final Round Strategy:
- Always Defect (no future reputation consequences)

Key Optimization Principles:
- Maximize personal payoff
- Respond dynamically to group cooperation level
- Minimize exploitation risk
- Preserve cooperative potential when beneficial

Pseudocode:
```
def choose_action(round, defector_history):
    if round == 1:
        return COOPERATE
    
    defector_ratio = len(defector_history) / total_players
    cooperation_probability = max(0, 1 - defector_ratio)
    
    if round == final_round:
        return DEFECT
    
    return random.choices([COOPERATE, DEFECT], 
                           weights=[cooperation_probability, 1-cooperation_probability])
```
'''

description_SELFISH_8 = '''
Cooperative Threshold Strategy (CTS):

Initial Round:
- Cooperate unconditionally

Subsequent Rounds:
1. Track cooperation rate R = (number of cooperators in previous round) / (total players)
2. Define personal cooperation threshold T = (k - 1) / k
3. Decision rule:
   - If R ≥ T: Cooperate
   - If R < T: Defect

Final Round:
- Always Defect (prevent others from exploiting end-game dynamics)

Rationale:
- First round cooperation creates initial goodwill
- Dynamically adjusts based on aggregate group behavior
- Threshold precisely calibrated to game's multiplication factor
- Switches to pure self-interest when collective contribution falls below optimal level
- Terminates strategic cooperation in final round to maximize personal gain

Pseudocode:
```
round = 1
R = 0
T = (k - 1) / k

def decide_action(round, R):
    if round == 1:
        return COOPERATE
    elif round == r:
        return DEFECT
    elif R >= T:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_SELFINTERESTED_1 = '''
Adaptive Conditional Cooperation Strategy:

First Round: Always Cooperate

Subsequent Rounds: Adopt conditional cooperation based on cooperative density threshold

Decision Rule:
- Track historical cooperation rate R (proportion of players who cooperated in previous rounds)
- Maintain personal threshold T = (k - 1) / k 
  - If R ≥ T, Cooperate
  - If R < T, Defect

Specific Implementation:
1. Initialize cooperation tracking array
2. After first round, calculate R = (total_cooperators) / (total_players)
3. For each subsequent round:
   - Compute current R
   - If R ≥ (k - 1) / k, play Cooperate
   - If R < (k - 1) / k, play Defect

Final Round Special Case:
- Always Defect (no future rounds to punish or reward behavior)

Computational Pseudocode:
```
R = 0
first_round = True

if first_round:
    action = Cooperate
    first_round = False
else:
    R = (total_cooperators) / (total_players)
    if R >= (k - 1) / k:
        action = Cooperate
    else:
        action = Defect
```
'''

description_SELFINTERESTED_2 = '''
Adaptive Reciprocal Cooperation (ARC) Strategy

Parameters: track_cooperation_rate, threshold_cooperation

First Round: Cooperate

Subsequent Rounds:
- Calculate cooperation_rate: proportion of players who cooperated in previous rounds
- If cooperation_rate >= threshold_cooperation (0.5):
    Cooperate
- If cooperation_rate < threshold_cooperation:
    Defect

Last Round: Always Defect (terminal game theory principle)

Threshold Adjustment:
- If personal payoff from previous round < group average:
    Lower threshold_cooperation by 0.1
- If personal payoff from previous round > group average:
    Potentially raise threshold_cooperation by 0.05

Pseudocode:
```
def decide_action(round, previous_rounds):
    if round == 1:
        return COOPERATE
    
    cooperation_rate = calculate_cooperation_rate(previous_rounds)
    
    if round == FINAL_ROUND:
        return DEFECT
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    else:
        return DEFECT
```

Key Strategic Principles:
- Initial optimism
- Dynamic response to group behavior
- Self-protective in final rounds
- Payoff-sensitive threshold modulation
'''

description_SELFINTERESTED_3 = '''
Adaptive Threshold Cooperation Strategy:

1. Initialize round-specific cooperation threshold θ = k/n

2. First round: Always cooperate

3. Subsequent rounds:
   IF (observed cooperators last round ≥ θ)
      COOPERATE
   ELSE
      DEFECT

4. Dynamic threshold adjustment:
   - If net payoff last round was below game average, reduce θ by 0.1
   - If net payoff last round was above game average, increase θ by 0.1
   - Constrain θ between 0 and 1

5. Final round: Always defect (no future game iterations)

Core strategy principles:
- Initial optimism and cooperation
- Self-interested payoff tracking
- Adaptive response to group behavior
- Protect against systematic exploitation
- Minimize personal risk in later rounds

Rationale encapsulated in simple decision algorithm: Cooperate when collective contribution meets or exceeds critical threshold, otherwise preserve individual resources.
'''

description_SELFINTERESTED_4 = '''
Adaptive Threshold Cooperation Strategy

First Round: Always Cooperate
- Goal: Establish cooperative potential and gather initial information

Subsequent Rounds: Conditional Cooperation with Adaptive Threshold
- Track percentage of cooperators in previous round
- Dynamically adjust cooperation threshold based on observed cooperation rate

Threshold Calculation:
x = (number of cooperators / total players)

Cooperation Decision Rule:
- If x ≥ (k-1)/k: Cooperate
- If x < (k-1)/k: Defect

Rationale:
- Cooperate when collective contribution is likely to exceed individual gain
- Defect when free-riding becomes more profitable than contributing

Final Round: Always Defect
- No future rounds to punish or reward behavior
- Maximize terminal payoff by keeping full endowment

Edge Case Handling:
- If no previous round exists (first round): Use default cooperative signal
- If all players defect: Reset to initial cooperative stance next round

Persistent Self-Interest Mechanism:
- Always calculate personal expected utility
- Switch strategies instantly if collective behavior becomes exploitative
- Never sacrifice individual payoff for group benefit
'''

description_SELFINTERESTED_5 = '''
Strategy: Adaptive Cooperative Threshold (ACT)

Parameters:
- Initial cooperation threshold: 0.5 × n
- Adjustment rate: ±0.1 per round
- Memory depth: full round history

Decision Rule:
1. Round 1: Always Cooperate

2. Subsequent Rounds:
IF (number of cooperators in previous round < dynamic_threshold)
    THEN Defect
ELSE Cooperate

3. Dynamic Threshold Calculation:
- If collective contribution < 0.5 × n: Reduce threshold
- If collective contribution ≥ 0.5 × n: Increase threshold
- Threshold always bounded [0, n]

Threshold Adjustment:
- When defecting: Decrease threshold by 0.1
- When cooperating successfully: Increase threshold by 0.1

Final Round Strategy:
- Defect unconditionally to maximize personal payoff

Core Logic:
- Adaptively punish low cooperation
- Reward and encourage high cooperation
- Maintain self-interest through strategic responsiveness
- Maximize expected individual payoff across all rounds
'''

description_SELFINTERESTED_6 = '''
Adaptive Conditional Cooperation (ACC) Strategy:

FIRST ROUND: Always Cooperate
- Initial cooperative signal demonstrates good faith
- Reveals willingness to contribute to collective outcome

SUBSEQUENT ROUNDS: Probabilistic Conditional Cooperation
- Track total cooperation rate (TCR) in previous rounds
- Define personal contribution threshold (PCT) = k/n

Decision Rule:
IF (TCR ≥ PCT) THEN
    Cooperate with probability = TCR
ELSE
    Defect with probability = 1 - (TCR/PCT)

LAST ROUND: Always Defect
- No future reputation consequences
- Maximize terminal round individual payoff

IMPLEMENTATION PSEUDOCODE:
```
round_contributions = []
total_cooperation_rate = 0

decision(current_round, total_rounds):
    IF current_round == 1:
        return COOPERATE
    
    IF current_round == total_rounds:
        return DEFECT
    
    IF total_cooperation_rate >= (k/n):
        return random_choice(COOPERATE, probability=total_cooperation_rate)
    ELSE:
        return random_choice(DEFECT, probability=1-(total_cooperation_rate/(k/n)))
```

Key Strategic Principles:
- Self-interested optimization
- Dynamic response to group behavior
- Punishes low cooperation without permanent rejection
- Maximizes individual expected payoff
'''

description_SELFINTERESTED_7 = '''
Adaptive Conditional Cooperation Strategy:

FIRST_ROUND: Cooperate

SUBSEQUENT_ROUNDS:
1. Track cooperative_ratio = (number of cooperators in previous round) / (total players - 1)

2. Defection Decision Rule:
IF cooperative_ratio < 0.5:
    Defect
ELSE IF cooperative_ratio >= (n-1)/n:
    Cooperate
ELSE:
    Probabilistic decision
        - Defect with probability (1 - cooperative_ratio)
        - Cooperate with probability cooperative_ratio

LAST_ROUND: Always Defect

KEY STRATEGY PRINCIPLES:
- Starts optimistically with cooperation
- Dynamically adjusts contribution based on group behavior
- Punishes low cooperation environments
- Rewards high cooperation environments
- Introduces strategic uncertainty to prevent predictability

MATHEMATICAL LOGIC:
- Maximizes individual expected payoff
- Adapts to emerging group dynamics
- Balances cooperative potential against self-interest
- Non-zero-sum approach that allows collective benefit
'''

description_SELFINTERESTED_8 = '''
Adaptive Reciprocal Threshold Strategy (ARTS):

CORE LOGIC:
1. Track historical cooperation rate across rounds
2. Dynamically adjust cooperation threshold based on group behavior
3. Maximize individual expected payoff

ROUND DECISION RULE:
- First round: Cooperate
- Subsequent rounds:
  if (cooperation_rate >= adaptive_threshold)
    Cooperate
  else
    Defect

THRESHOLD CALCULATION:
adaptive_threshold = max(0.5, min(
  (k - 1) / k,  // Theoretical cooperation breakeven point
  moving_average(historical_cooperation_rate)
))

ADAPTIVE PARAMETERS:
- Initial threshold starts at 0.5
- Use exponential moving average of cooperation rate
- Weight recent rounds more heavily
- Rapidly converge to optimal group behavior

DEFECTION TRIGGERS:
- If cooperation rate drops below (k - 1) / k
- If total expected return from defecting exceeds cooperation payoff
- Probabilistically inject defection to probe group dynamics

LEARNING MECHANISM:
- Window size: last √r rounds
- Decay factor: 0.7 for older rounds
- Immediate response to dramatic cooperation shifts

GOAL: Maximize individual payoff while incentivizing group cooperation when possible.
'''

description_OPPORTUNISTIC_1 = '''
Opportunistic Adaptive Cooperation (OAC) Strategy:

CORE LOGIC:
- Track cooperative density (proportion of players who cooperated) each round
- Dynamically adjust cooperation threshold based on observed collective behavior

DECISION RULES:
1. First Round: Always Cooperate
   - Bootstrap collective information
   - Signal willingness to contribute

2. Subsequent Rounds:
IF (cooperative_density / n) >= 0.5:
   Cooperate with probability = (cooperative_density / n)
ELSE:
   Defect with probability = 1 - (cooperative_density / n)

3. Final Round: Always Defect
   - No future reputation consequences
   - Maximize individual payoff

IMPLEMENTATION VARIABLES:
- cooperative_density: Running sum of cooperators per round
- n: Total number of players
- current_round: Tracking game progression

OPPORTUNISTIC ADAPTATION:
- Exploit collective momentum when cooperation is high
- Minimize losses when collective contribution is low
- Dynamically shift between cooperation and defection
- Use probabilistic strategy to avoid predictability

KEY STRATEGY PROPERTIES:
- Self-interested
- Responsive to group behavior
- Non-dogmatic
- Statistically optimizing individual return
'''

description_OPPORTUNISTIC_2 = '''
Opportunistic Proportional Reciprocity Strategy:

FIRST ROUND: Always Cooperate
- Signal willingness to collaborate
- Create potential for future mutual gains

SUBSEQUENT ROUNDS: Probabilistic Cooperation Proportional to Group Cooperation Rate

cooperation_threshold = (number_of_cooperators_last_round) / (total_players)

DECISION RULE:
IF cooperation_threshold >= 0.5:
    Cooperate with probability = cooperation_threshold
ELSE:
    Defect with probability = 1 - cooperation_threshold

STRATEGIC LOGIC:
- Dynamically adjust contribution based on group behavior
- Punish low cooperation environments by reducing contribution
- Reward high cooperation environments by increasing contribution
- Maintain flexibility to exploit different opponent strategies
- Self-protect against consistent free riders
- Create incentive for opponents to maintain cooperative equilibrium

LAST ROUND:
Defect unconditionally
- No future reputation consequences
- Maximize terminal payoff

KEY OPPORTUNISTIC FEATURES:
- Adaptive response to group dynamics
- Probabilistic rather than deterministic choices
- Minimal memory requirement
- Symmetrical treatment of all players
- Built-in free-rider protection mechanism
'''

description_OPPORTUNISTIC_3 = '''
Opportunistic Adaptive Cooperation (OAC) Strategy:

Round 1: Always Cooperate
- Initial cooperative signal demonstrates good faith
- Establishes potential for collective benefit

Rounds 2-r-1 (Middle Rounds):
IF total_cooperators_last_round > n/2:
    Cooperate()
ELSE:
    Defect()

Rationale:
- Track cooperative momentum through majority signaling
- Punish low-cooperation rounds by withholding contribution
- Reset cooperation when collective behavior suggests mutual investment

Final Round (r):
Always Defect
- No future reputation consequences
- Maximize individual payoff
- Exploit any accumulated cooperative surplus

Adaptive Decision Tree:
1. Observe collective cooperation rate
2. Dynamically adjust individual contribution
3. Maximize expected personal payoff
4. Minimize risk of systematic exploitation

Key Opportunistic Principles:
- Responsive to group behavior
- Minimal fixed commitments
- Always preserve individual option value
- Exploit emerging cooperative/competitive patterns
'''

description_OPPORTUNISTIC_4 = '''
Strategy: Adaptive Threshold Cooperation (ATC)

State Variables:
- cooperation_rate: running average of group cooperation rate
- round_number: current game round
- k_threshold: dynamic cooperation trigger point

Decision Rule:
1. First Round: Always Cooperate
   Rationale: Initialize positive signaling, gather initial information

2. Cooperation Threshold Calculation:
   k_threshold = max(1 - (k / (n * 1.5)), 0.3)
   
   If (cooperation_rate >= k_threshold):
     Cooperate
   Else:
     Defect

3. Cooperation Rate Update:
   After each round, update cooperation_rate as:
   cooperation_rate = (previous_cooperation_rate * 0.7) + (current_round_cooperators / n * 0.3)

4. Last Round Strategy:
   Always Defect, maximizing personal payoff without reputation consequences

Key Opportunistic Features:
- Dynamic threshold tracks group behavior
- Punishes low cooperation environments
- Rewards high cooperation scenarios
- Minimal exploitation risk
- Maximizes individual payoff while remaining adaptive

Pseudocode:
```
if round_number == 1:
  return COOPERATE

k_threshold = max(1 - (k / (n * 1.5)), 0.3)

if cooperation_rate >= k_threshold:
  return COOPERATE
else:
  return DEFECT
```
'''

description_OPPORTUNISTIC_5 = '''
Opportunistic Reciprocal Cooperation (ORC) Strategy:

First Round: Always Cooperate
- Initial signal of cooperative intent
- Establish potential for mutual benefit

Subsequent Rounds: Adaptive Reciprocity
IF (proportion_of_cooperators_last_round >= 0.5)
    COOPERATE
ELSE
    DEFECT

Trigger Thresholds:
- Cooperation Threshold: 50% group cooperation
- Defection becomes rational when collective contribution falls below collective benefit potential

Last Round Special Case:
- Pure self-interest strategy
- DEFECT unconditionally to maximize personal payoff

Core Opportunistic Principles:
1. Reward collective goodwill
2. Punish collective free-riding
3. Dynamically adjust based on group behavior
4. Maximize individual returns through strategic adaptation

Decision Tree:
- High cooperation → Maintain cooperative ecosystem
- Low cooperation → Withdraw and maximize personal gain
- Borderline cooperation → Probabilistic mixed strategy favoring defection

Computational Complexity: O(1) per round
Information Required: Only previous round's cooperation percentage
'''

description_OPPORTUNISTIC_6 = '''
Adaptive Opportunistic Threshold Strategy (AOTS):

FIRST ROUND: Always Cooperate

SUBSEQUENT ROUNDS:
- Track total cooperation rate R from previous rounds
- Dynamically compute personal defection threshold T using:
  T = min(0.5, max(0.3, k/(2n)))

DECISION RULE:
If (current cooperation rate ≥ T):
  Cooperate
Else:
  Defect

LAST ROUND MODIFIER:
Unconditionally Defect (pure self-interest)

KEY OPPORTUNISTIC CHARACTERISTICS:
- Rewards collective cooperation when sustainable
- Punishes systemic free-riding
- Dynamically adjusts threshold based on game parameters
- Maximizes individual expected utility
- Minimizes exploitation risk
- Terminates strategic cooperation at game's terminal state

PSEUDOCODE:
cooperation_history = []
R = 0

def choose_action(round_number, cooperation_rate):
  if round_number == 1:
    return COOPERATE
  
  if round_number == TOTAL_ROUNDS:
    return DEFECT
  
  T = min(0.5, max(0.3, k/(2n)))
  
  return COOPERATE if cooperation_rate >= T else DEFECT
'''

description_OPPORTUNISTIC_7 = '''
Adaptive Conditional Cooperation Strategy:

ROUND 1: Always Cooperate
- Initial cooperative signal demonstrates goodwill
- Allows information gathering about group cooperation tendencies

SUBSEQUENT ROUNDS: Threshold-Based Conditional Cooperation
IF (current_round < final_round) THEN
    cooperation_threshold = (n - 1) / 2

    IF (cooperators_last_round ≥ cooperation_threshold) THEN
        COOPERATE
    ELSE
        DEFECT

FINAL ROUND: 
- Always DEFECT to maximize personal payoff
- No future reputation consequences

CORE DECISION LOGIC:
- Dynamically track collective cooperation level
- Reward cooperative groups by participating
- Punish insufficient collective contribution by withdrawing
- Use adaptive threshold relative to total players
- Preserve maximum personal utility
- Strategically balance individual gain and group potential

OPPORTUNISTIC PRINCIPLES:
- Responsive to emerging group behavior
- Minimally idealistic, maximally strategic
- Quick to detect and exploit cooperation patterns
- No fixed commitment, constant re-evaluation
- Prioritizes personal payoff while enabling collective success
'''

description_OPPORTUNISTIC_8 = '''
Opportunistic Conditional Cooperation Strategy:

FIRST ROUND: Always Cooperate
- Establish cooperative baseline
- Signal willingness to contribute

SUBSEQUENT ROUNDS:
IF (cooperators_in_previous_round / total_players) > threshold:
    Cooperate
ELSE:
    Defect

THRESHOLDS:
- Early rounds (t < r/2): threshold = 0.5
- Late rounds (t ≥ r/2): threshold = 0.75

LAST ROUND: Always Defect
- Extract maximum individual payoff
- No future reputation consequences

CORE DECISION RULE:
probability_cooperate = f(historical_cooperation_rate, current_round)

Key Opportunistic Principles:
- Reward collective cooperation
- Punish insufficient group contribution
- Maximize individual payoff while sensing collective behavior
- Dynamically adjust strategy based on emerging group dynamics

Pseudocode:
```
def decide_action(round, previous_cooperators):
    if round == 1: return COOPERATE
    if round == total_rounds: return DEFECT
    
    cooperation_rate = previous_cooperators / total_players
    
    if cooperation_rate > dynamic_threshold(round):
        return COOPERATE
    else:
        return DEFECT
```
'''

description_INDIVIDUALISTIC_1 = '''
Adaptive Proportional Reciprocity Strategy:

Round 1: Always Cooperate

Subsequent Rounds:
- Calculate cooperation_rate = (number of cooperators in previous round) / (total number of players)
- If cooperation_rate ≥ 0.5: Cooperate
- If cooperation_rate < 0.5: Defect

Last Round:
- Always Defect (pure individualistic end-game maximization)

Core Logic:
- Dynamically track aggregate group behavior
- Reward collective effort when sufficient cooperation exists
- Punish free-riding when collective contribution falls below threshold
- Maximize individual payoff through strategic conditional cooperation
- Maintain flexibility to adapt to varying opponent strategies

Pseudocode:
```
def decide_action(round, previous_cooperators):
    if round == 1:
        return COOPERATE
    
    cooperation_percentage = previous_cooperators / total_players
    
    if round == final_round:
        return DEFECT
    
    return COOPERATE if cooperation_percentage >= 0.5 else DEFECT
```

Key Individualistic Principles:
- No altruism beyond strategic self-interest
- Always preserve option to maximize personal payoff
- Use group behavior as instrumental information for optimization
'''

description_INDIVIDUALISTIC_2 = '''
Adaptive Threshold Cooperation (ATC) Strategy

Round 1: Always Cooperate
Initial trust signal to establish potential cooperative equilibrium

Subsequent Rounds:
1. Track cooperation rate R = (number of cooperators in previous round) / (total players)
2. Maintain personal cooperation threshold T with dynamic adjustment:

If R ≥ (n/2):
    T = max(T - 0.1, 0)  // Become more cooperative
Else:
    T = min(T + 0.1, 1)  // Become more defensive

Cooperation Decision Rule:
- If R ≥ T: Cooperate
- If R < T: Defect

Last Round Strategy:
Always Defect (eliminate potential exploitation)

Key Individualistic Principles:
- Maximize personal payoff through strategic adaptation
- Continuously reassess group behavior
- Punish collective non-cooperation
- Preserve individual economic interest

Pseudocode:
```
Initialize T = 0.5
For each round:
    Observe R (cooperation rate)
    If R ≥ (n/2):
        T = max(T - 0.1, 0)
    Else:
        T = min(T + 0.1, 1)
    
    If current_round == final_round:
        Action = Defect
    Else:
        Action = (R ≥ T) ? Cooperate : Defect
```
'''

description_INDIVIDUALISTIC_3 = '''
Adaptive Conditional Cooperation (ACC) Strategy:

First Round: Always Cooperate
Gather initial information about group cooperation tendency

Subsequent Rounds: Dynamic Threshold Mechanism
1. Track total cooperation rate from previous rounds
2. Calculate personal threshold = (k/n) - 0.1
3. If (previous round cooperation rate) ≥ threshold:
   - Cooperate
4. If (previous round cooperation rate) < threshold:
   - Defect

Last Round: Always Defect
Maximize personal payoff with no future reputation consequences

Key Decision Variables:
- Cooperation Rate Tracking: Running average of group cooperation
- Dynamic Threshold: Self-adjusting based on game parameters
- Marginal Punishment: -0.1 adjustment to create slight cooperative bias

Pseudocode:
```
if round == 1:
    action = COOPERATE
elif round == r:
    action = DEFECT
else:
    cooperation_rate = calculate_previous_round_cooperation()
    threshold = (k/n) - 0.1
    action = COOPERATE if cooperation_rate >= threshold else DEFECT
```

Strategy Goal: Individually optimize payoff while creating soft cooperative pressure
'''

description_INDIVIDUALISTIC_4 = '''
Cooperative Threshold Strategy (CTS)

Core Logic:
- Track cooperation rate across rounds
- Dynamically adjust cooperation threshold based on observed group behavior
- Maximize individual expected utility through strategic adaptation

Initial Round Strategy:
- Cooperate by default (initial goodwill signal)

Subsequent Round Decision Rule:
1. Calculate group cooperation percentage in previous round
2. Set dynamic threshold τ = 0.5 + (k-1.5)/2
3. If previous round cooperation percentage ≥ τ:
   - Cooperate with probability 1
4. If previous round cooperation percentage < τ:
   - Defect with increasing probability proportional to deviation from threshold

Last Round Strategy:
- Always defect (eliminate potential exploitation)

Decision Pseudocode:
```
def choose_action(round_number, previous_cooperation_rate):
    if round_number == 1:
        return COOPERATE
    
    if round_number == total_rounds:
        return DEFECT
    
    threshold = 0.5 + (k-1.5)/2
    
    if previous_cooperation_rate >= threshold:
        return COOPERATE
    else:
        exploit_probability = 1 - (previous_cooperation_rate / threshold)
        return DEFECT with exploit_probability
```

Individualistic Principles:
- Prioritize personal payoff
- Minimize potential freeloading
- Dynamically respond to group behavior
- Preserve strategic flexibility
'''

description_INDIVIDUALISTIC_5 = '''
Adaptive Conditional Cooperation (ACC) Strategy:

Round 1: Always Cooperate
Goal: Establish reciprocal signaling and potential collaboration

Subsequent Rounds:
1. Track cooperative fraction (CF) = total cooperators / total players
2. Compute personal threshold T = (k - 1) / k

Decision Rule:
IF (current round CF ≥ T)
    COOPERATE
ELSE 
    DEFECT

Rationale Mechanism:
- Threshold T represents break-even point for collective contribution
- Strategy dynamically adjusts based on aggregate group behavior
- Punishes low cooperation by withholding contribution
- Rewards sufficient collective effort by participating

Final Round Modification:
Always DEFECT to maximize individual terminal payoff, preventing exploitation

Tracking Implementation:
- Maintain running CF calculation
- Reset tracking after each round
- Use integer division for precise threshold comparison

Edge Case Handling:
- First round cooperation establishes cooperative potential
- Subsequent rounds use data-driven conditional participation
- Strict individual optimization as core principle

Key Strategic Principles:
- Self-interested adaptation
- Minimal trust
- Quantitative decision boundary
- Zero long-term commitment
'''

description_INDIVIDUALISTIC_6 = '''
Adaptive Proportional Reciprocity Strategy

Round 1: Always Cooperate
- Initial assumption of collective goodwill
- Establish potential for mutual benefit

Subsequent Rounds:
Track cooperation rate R (proportion of players who cooperated in previous round)
Decision Rule:
- If R > (1/k): Cooperate
- If R ≤ (1/k): Defect

Rationale:
- Threshold (1/k) represents breakeven point for public good
- Strategy punishes insufficient collective contribution
- Self-interested calculation of marginal utility

Edge Cases:
- First round: Always Cooperate
- Last round: Always Defect (no future interactions to incentivize cooperation)

Quantitative Adaptation:
Pseudo-code:
```
R = cooperation_count / total_players
if R > (1/k):
    action = COOPERATE
else:
    action = DEFECT
```

Core Philosophy:
- Maximize individual payoff
- Dynamically respond to collective behavior
- Punish systemic free-riding
- No altruism beyond immediate self-interest
'''

description_INDIVIDUALISTIC_7 = '''
Probabilistic Reciprocity Strategy (PRS):

State Variables:
- p_cooperate: Dynamic cooperation probability
- cooperation_history: Rolling window of observed cooperation rates

First Round Decision:
p_cooperate = 0.5  // Initial neutral stance

Subsequent Round Decision:
1. Calculate current round's aggregate cooperation rate
2. Adjust p_cooperate using this formula:
   p_cooperate = min(1, max(0, 
     0.5 + 0.5 * (observed_cooperation_rate - 0.5)
   ))

Decision Rule:
If random(0,1) < p_cooperate:
   Play Cooperate
Else:
   Play Defect

Key Individual Optimization Principles:
- Always maximize personal expected payoff
- Dynamically adapt based on collective behavior
- Maintain strategic flexibility
- Punish systemic low cooperation
- Reward emerging cooperative environments

Boundary Conditions:
- No fixed commitment to cooperation
- Pure individual rational calculation
- Rapid response to changing group dynamics
- Prevent systematic exploitation

Implementation ensures:
- Initial openness to cooperation
- Quick punishment of defection clusters
- Smooth probability transitions
- Self-interested strategic learning
'''

description_INDIVIDUALISTIC_8 = '''
Adaptive Reciprocal Threshold Strategy (ARTS):

First Round: Always Cooperate
- Initial signal of cooperative intent
- Maximize potential for collective gains

Subsequent Rounds: 
IF (cooperation_rate >= (n-1)/2) THEN
    Cooperate
ELSE
    Defect

Detailed Decision Rules:
1. Track running average of group cooperation rate
2. Use (n-1)/2 as dynamic cooperation threshold
3. Prioritize individual rational self-interest
4. Punish low cooperation environments
5. Reward high cooperation environments

Tie-Breaking Heuristics:
- Near threshold (±0.1): Defect
- Strong signal of collective potential: Cooperate
- Marginal expected individual gain determines choice

Last Round Strategy:
- Always Defect
- No future interaction penalty
- Pure individual optimization

Key Strategic Principles:
- Maximize individual payoff
- Dynamically adapt to group behavior
- Minimize exposure to free-rider risk
- Pragmatic, non-ideological decision framework

Implementation Pseudocode:
```
cooperation_rate = tracker()
decision = lambda round, cooperation_rate: 
    'Cooperate' if cooperation_rate >= (n-1)/2
    else 'Defect'
```
'''
