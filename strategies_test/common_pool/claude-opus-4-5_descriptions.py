"""
Strategy descriptions for CommonPoolDescription.

Generated with:
- Provider: Anthropic
- Model: claude-opus-4-5
"""


description_COLLECTIVE_1 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared asset whose sustainability benefits everyone. The goal is to preserve the resource while protecting against exploitation. I call this strategy **"Sustainable Guardian"**.

## Key Insight

When all players cooperate, the stock remains at capacity indefinitely (consumption equals regeneration at capacity). When players defect, the resource degrades, harming future payoffs for everyone. The strategy must balance:
1. **Collective sustainability** - keeping the resource healthy
2. **Self-protection** - not being exploited by defectors
3. **Signaling** - encouraging others toward cooperation

## Decision Rules

### Primary Rule: Stock-Health Responsive Cooperation with Forgiveness

```
COOPERATE if:
    (stock_ratio >= 0.7) AND (defection_rate_last_3_rounds <= 0.5)
    OR (stock_ratio >= 0.9)  # Resource is healthy enough to extend trust
    OR (round == 1)  # Start cooperatively
    
DEFECT otherwise
```

Where:
- `stock_ratio = current_stock / capacity`
- `defection_rate_last_3_rounds` = proportion of defections observed across all players in last 3 rounds

### Detailed Logic

**Round 1 (First Round):**
- **Always Cooperate** - Signal cooperative intent and establish baseline for sustainable play

**Rounds 2 through r-1 (Middle Rounds):**

1. **If stock is critically low (stock_ratio < 0.3):**
   - **Defect** - Resource is already compromised; secure what remains before collapse

2. **If stock is healthy (stock_ratio >= 0.7):**
   - Count defections in the last min(3, rounds_played) rounds
   - If defection_rate <= 0.5: **Cooperate** - Majority are cooperating, maintain sustainability
   - If defection_rate > 0.5: **Defect** - Too many defectors; protect against exploitation

3. **If stock is moderate (0.3 <= stock_ratio < 0.7):**
   - If defection_rate <= 0.33: **Cooperate** - Give cooperation a chance to restore stock
   - Otherwise: **Defect** - Cannot afford to be exploited when resource is stressed

4. **If stock is very healthy (stock_ratio >= 0.9):**
   - **Cooperate** regardless of recent history - The resource can sustain one round of potential exploitation, and this signals willingness to "reset" toward cooperation

**Round r (Final Round):**
- **Defect** - No future rounds to consider; this is the dominant strategy

## Pseudocode Implementation

```python
def sustainable_guardian(round_number, total_rounds, current_stock, capacity, 
                         history, n_players):
    
    stock_ratio = current_stock / capacity
    
    # First round: always cooperate
    if round_number == 1:
        return COOPERATE
    
    # Last round: always defect (no future to protect)
    if round_number == total_rounds:
        return DEFECT
    
    # Calculate recent defection rate (last 3 rounds or all available)
    lookback = min(3, round_number - 1)
    recent_actions = get_all_actions_last_n_rounds(history, lookback)
    defection_rate = count(recent_actions == DEFECT) / len(recent_actions)
    
    # Very healthy stock: extend trust
    if stock_ratio >= 0.9:
        return COOPERATE
    
    # Critical stock: protect remaining resources
    if stock_ratio < 0.3:
        return DEFECT
    
    # Healthy stock: cooperate if others mostly cooperate
    if stock_ratio >= 0.7:
        threshold = 0.5
    else:  # Moderate stock: require stronger cooperation signal
        threshold = 0.33
    
    if defection_rate <= threshold:
        return COOPERATE
    else:
        return DEFECT
```

## Why This Strategy Works

1. **Sustainability-focused**: Cooperation is the default when viable, preserving the resource
2. **Adaptive**: Responds to both resource state AND opponent behavior
3. **Forgiving**: High stock triggers cooperation, allowing recovery from defection spirals
4. **Protective**: Defects when exploited or when resource is critically low
5. **Collectively optimal**: If matched with similar strategies, maintains full capacity throughout
6. **Robust to exploitation**: Limits losses against pure defectors by responding in kind

## Edge Cases

- **All opponents always defect**: Strategy will defect from round 2 onward, limiting exploitation
- **Mixed opponent pool**: Adjusts based on aggregate behavior, not individual tracking
- **Stock crashes early**: Switches to protective defection to salvage remaining value
- **Partial recovery**: The 0.9 threshold allows "olive branch" cooperation after recovery
'''

description_COLLECTIVE_2 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that sustains all players across rounds. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - it maintains stock at capacity while providing steady returns. Defection offers short-term gains but destroys the resource base for everyone, including the defector.

The strategy aims to:
1. Signal cooperative intent and establish sustainable harvesting
2. Protect the resource from collapse when others defect
3. Punish defection proportionally to deter exploitation
4. Forgive and return to cooperation when the group does

## Decision Rules

### Primary Rule: Conditional Cooperation with Resource Protection

```
COOPERATE if:
  - First round (establish cooperative norm)
  - All players cooperated in the previous round
  - Stock is critically low (≤ capacity/4) regardless of history
  - Majority cooperated last round AND stock is recovering (grew since last round)

DEFECT if:
  - Majority defected in the previous round AND stock is above critical threshold
  - Any player defected for 2+ consecutive rounds (persistent defector detected)
  - Last round of the game (no future to protect)
```

### Detailed Decision Logic

```python
def choose_action(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    stock = state.stock
    
    critical_threshold = capacity / 4
    
    # FIRST ROUND: Cooperate to signal intent
    if current_round == 1:
        return COOPERATE
    
    # LAST ROUND: Defect (no future consequences)
    if current_round == r:
        return DEFECT
    
    # CRITICAL STOCK PROTECTION: Always cooperate to save the resource
    if stock <= critical_threshold:
        return COOPERATE
    
    # Analyze previous round
    last_round = history[-1]
    num_defectors = count_defectors(last_round)
    num_cooperators = n - num_defectors
    majority_cooperated = num_cooperators > n / 2
    
    # Check for persistent defectors (2+ consecutive rounds)
    has_persistent_defector = False
    if len(history) >= 2:
        for player in range(n):
            if defected_in(history[-1], player) and defected_in(history[-2], player):
                has_persistent_defector = True
                break
    
    # Check if stock is recovering
    stock_recovering = True
    if len(history) >= 2:
        stock_recovering = state.stock >= history[-1].stock_after
    
    # PUNISH persistent defection (but only if resource can handle it)
    if has_persistent_defector and stock > critical_threshold * 2:
        return DEFECT
    
    # REWARD group cooperation
    if num_defectors == 0:
        return COOPERATE
    
    # FORGIVE if majority cooperates and resource is recovering
    if majority_cooperated and stock_recovering:
        return COOPERATE
    
    # PUNISH majority defection (tit-for-tat element)
    if not majority_cooperated:
        return DEFECT
    
    # DEFAULT: Cooperate (optimistic)
    return COOPERATE
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, signal intent |
| **Round r (last)** | Defect | No future rounds to protect; standard backward induction |
| **Stock ≤ capacity/4** | Cooperate | Resource crisis - collective survival trumps punishment |
| **Stock = 0** | Cooperate | Only option; defecting on 0 yields 0 anyway |
| **All cooperated last round** | Cooperate | Maintain successful equilibrium |
| **Persistent defector detected** | Defect | Proportional punishment to deter exploitation |
| **Mixed signals (some defect, some cooperate)** | Cooperate if majority cooperated AND stock recovering | Give benefit of doubt while monitoring |

## Why This Strategy is Collectively Optimal

1. **Sustainability**: Universal cooperation maintains stock at capacity indefinitely
2. **Proportional response**: Punishment scales with defection severity
3. **Forgiveness**: Returns to cooperation quickly, avoiding punishment spirals
4. **Crisis management**: Prioritizes resource survival over punishment when stock is critical
5. **Clear signaling**: Consistent behavior makes intentions predictable to other cooperative agents
'''

description_COLLECTIVE_3 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The key insight is that **universal cooperation is the only sustainable equilibrium** - it maintains stock at capacity indefinitely, yielding consistent returns every round. Any defection triggers a tragedy of the commons that ultimately harms everyone, including defectors.

The strategy employs **conditional cooperation with graduated forgiveness**, designed to:
1. Signal cooperative intent clearly
2. Protect the commons from exploitation
3. Allow recovery from mistakes or temporary defection
4. Maximize collective welfare across all rounds

---

## Decision Rules

### Primary Rule: Cooperative Threshold Response

**Cooperate if and only if:**
- The cooperation rate in the previous round was at least `(n-1)/n` (i.e., at most one defector), OR
- We are in a forgiveness window following sustained cooperation, OR
- It's the first round

**Defect if:**
- Two or more players defected in the previous round AND we're not in a protected forgiveness window

### Detailed Logic

```
INITIALIZE:
  forgiveness_counter = 0
  cooperation_streak = 0
  
FOR each round t:
  
  IF t == 1:
    PLAY C  # Always start cooperative to signal intent
    
  ELSE IF t == r (final round):
    # Final round: maintain cooperation if stock is healthy and history is good
    IF stock >= capacity * 0.5 AND cooperation_streak >= 2:
      PLAY C
    ELSE:
      PLAY D  # Defect only if commons already degraded
      
  ELSE:  # Middle rounds
    previous_defectors = count(players who played D in round t-1)
    
    IF previous_defectors == 0:
      cooperation_streak += 1
      forgiveness_counter = min(forgiveness_counter + 1, 3)
      PLAY C
      
    ELSE IF previous_defectors == 1:
      # Tolerate single defector - might be a mistake or test
      cooperation_streak = 0
      PLAY C
      
    ELSE IF previous_defectors >= 2:
      cooperation_streak = 0
      IF forgiveness_counter > 0:
        forgiveness_counter -= 1
        PLAY C  # Use forgiveness credit
      ELSE:
        # Retaliate to discourage exploitation
        PLAY D
        
    # Recovery mechanism: After defecting, attempt to restore cooperation
    IF I played D in round t-1 AND stock > capacity * 0.3:
      # Offer olive branch if commons not critically depleted
      IF random() < 0.3 + (0.1 * rounds_remaining / r):
        PLAY C  # Probabilistic return to cooperation
```

---

## Edge Case Handling

### First Round
**Always Cooperate.** This unambiguously signals cooperative intent and gives the collective the best chance of establishing a sustainable norm. Starting with defection poisons the well immediately.

### Last Round
**Conditionally Cooperate.** Unlike typical game theory advice to defect in final rounds, this strategy recognizes that:
- If everyone follows this logic, mutual defection destroys remaining value
- Maintaining cooperation until the end maximizes total extraction across all rounds
- Only defect if the commons is already severely degraded (stock < 50% capacity) AND recent history shows breakdown

### Stock Critically Low (stock < capacity * 0.25)
**Always Cooperate.** When the commons is near collapse, even "rational" defection accelerates disaster. Desperate cooperation is the only path to potential recovery via the regeneration mechanism.

### First Sign of Defection
**Tolerate one defector.** A single defector may be testing, mistaken, or using a different strategy. Immediate retaliation could trigger a destructive spiral. Give the collective one round to self-correct.

### Sustained Defection by Multiple Players
**Match defection but seek exits.** If cooperation is clearly failing, protect yourself from exploitation, but periodically (probabilistically) attempt to restore cooperation, especially when many rounds remain.

---

## Why This Strategy is Collectively Optimal

1. **Sustainability**: Universal C maintains stock at capacity, yielding `capacity/(2n)` per player per round forever - the maximum sustainable yield.

2. **Robustness**: The graduated response (tolerate 1, retaliate against 2+) balances forgiveness with protection.

3. **Self-reinforcing**: When multiple agents use this strategy, they create a stable cooperative equilibrium that's resistant to invasion by pure defectors.

4. **Recoverable**: The forgiveness mechanism and probabilistic peace offers allow escape from punishment spirals.

5. **Stock-aware**: Decisions account for resource state, not just opponent actions, enabling intelligent adaptation to degraded conditions.
'''

description_COLLECTIVE_4 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared system where collective restraint enables long-term abundance. The goal is to maximize total group payoff over all rounds while being robust to defectors. I assume other players using this same strategy are part of a "collective" that should coordinate implicitly through observable behavior.

## Strategy Overview: "Sustainable Threshold with Graduated Response"

The strategy balances three priorities:
1. **Sustainability**: Keep stock high enough for regeneration
2. **Collective signaling**: Cooperate to demonstrate collective membership
3. **Protection**: Respond proportionally to defection to discourage exploitation

---

## Decision Rules

### Round 1: Always Cooperate
- Establishes cooperative intent
- Allows observation of other players' strategies
- Preserves stock for future rounds

### Rounds 2 through (r-1): Adaptive Cooperation with Threshold Protection

**Step 1: Assess the situation**
- Count defectors from the previous round: `d_prev`
- Calculate current stock ratio: `stock_ratio = stock / capacity`

**Step 2: Apply decision logic**

```
IF stock_ratio < 0.25 THEN:
    # Critical stock level - cooperate to allow recovery
    # unless nearly everyone defected (collective collapse)
    IF d_prev >= n-1 THEN: DEFECT
    ELSE: COOPERATE

ELSE IF d_prev == 0 THEN:
    # Full cooperation last round - maintain it
    COOPERATE

ELSE IF d_prev <= floor(n/3) THEN:
    # Minor defection - forgive and cooperate
    # This allows for noise/mistakes and encourages return to cooperation
    COOPERATE

ELSE IF d_prev <= floor(n/2) THEN:
    # Moderate defection - probabilistic response
    # Cooperate with probability (n - d_prev) / n
    # This creates graduated pressure without collapsing cooperation
    IF random() < (n - d_prev) / n THEN: COOPERATE
    ELSE: DEFECT

ELSE:
    # Majority defecting - defect to protect against exploitation
    # But return to cooperation if others do
    DEFECT
```

### Final Round (Round r): Conditional Defection

```
IF d_prev == 0 AND stock_ratio >= 0.5 THEN:
    # Cooperation held throughout and stock is healthy
    # Cooperate as a collective commitment signal
    COOPERATE
ELSE:
    # Either cooperation broke down or resources depleted
    # No future rounds to recover, so defect
    DEFECT
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| n = 2 | Use standard rules but with stricter thresholds (any defection triggers response) | Small groups need tighter coordination |
| stock ≈ 0 | COOPERATE | Defecting yields nearly nothing anyway; cooperation signals willingness to rebuild |
| stock = capacity | Follow standard rules | High stock doesn't change strategic considerations |
| r = 2 | Cooperate round 1, apply final round logic for round 2 | Minimal repeated interaction |
| All previous rounds had defection | DEFECT | Collective cooperation has failed; minimize losses |

---

## Collective Alignment

This strategy is designed for collective success:

1. **Implicit coordination**: By following identical rules based on observable history, collective members naturally synchronize without communication

2. **Forgiveness threshold**: The `floor(n/3)` forgiveness window allows the collective to absorb some defection (possibly from non-collective players) without cascading into mutual defection

3. **Graduated response**: Probabilistic defection at moderate defection levels creates proportional pressure rather than all-or-nothing collapse

4. **Stock protection**: Prioritizing cooperation at low stock levels ensures the resource can recover, benefiting all collective members in future rounds

5. **Final round partial cooperation**: Maintaining cooperation in the final round when things went well reinforces that collective members are distinguishable from pure defectors

---

## Expected Behavior Against Various Opponents

- **Against all cooperators**: Mutual cooperation, maximum sustainable payoff
- **Against all defectors**: Defect after round 1, limiting exploitation to one round
- **Against mixed strategies**: Graduated response maintains cooperation with partial cooperators while protecting against heavy defection
- **Against tit-for-tat variants**: Cooperation stabilizes after initial rounds
'''

description_COLLECTIVE_5 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective stewardship** mindset: the shared resource is our common wealth, and sustainable harvesting benefits everyone across all rounds. However, we must be adaptive since we cannot assume others share this philosophy.

## Strategy Overview: "Adaptive Sustainable Harvesting"

The strategy balances three objectives:
1. **Sustainability**: Keep the stock at levels where regeneration is maximized
2. **Reciprocity**: Reward collective cooperation, respond proportionally to defection
3. **Resilience**: Maintain viability even when others defect

## Decision Rules

### Primary Decision Framework

```
COOPERATE if ANY of the following conditions are met:
1. Stock health is critical (stock < capacity/2)
2. Recent cooperation rate among all players is ≥ 50%
3. It's an early round (round ≤ 3) - establishing cooperative norms
4. Stock is regenerating well (current stock ≥ previous stock)

DEFECT only if ALL of the following are true:
1. Stock is healthy (stock ≥ capacity/2)
2. Recent cooperation rate < 50%
3. We're past the norm-establishment phase (round > 3)
4. Stock has been declining
```

### Detailed Decision Logic

**Round 1 (First Round):**
- **Always Cooperate** - Signal cooperative intent, establish positive norms, and preserve the resource for future rounds.

**Rounds 2 through (r-2) (Middle Rounds):**
```
Calculate:
- cooperation_rate = (total C plays by all players in last min(3, current_round-1) rounds) / (n × observed_rounds)
- stock_ratio = current_stock / capacity
- trend = current_stock - stock_from_2_rounds_ago (if available)

Decision:
IF stock_ratio < 0.3:
    COOPERATE  // Emergency conservation - resource is critically low
ELSE IF stock_ratio < 0.5:
    COOPERATE  // Precautionary conservation
ELSE IF cooperation_rate >= 0.5:
    COOPERATE  // Reward collective cooperation
ELSE IF trend > 0:
    COOPERATE  // Resource recovering, maintain momentum
ELSE:
    DEFECT     // Others are exploiting; protect fair share
```

**Round (r-1) (Second-to-Last Round):**
- **Cooperate if cooperation_rate ≥ 0.4** - Slightly more forgiving to maintain cooperation through endgame
- **Defect otherwise** - If cooperation has broken down, begin transition

**Round r (Final Round):**
- **Cooperate if stock_ratio < 0.4 AND cooperation_rate in previous round ≥ 0.6** - Honor sustained cooperation
- **Defect otherwise** - Standard endgame logic; no future rounds to protect

## Edge Cases

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Stock = 0 | Cooperate | No benefit to defecting; signal willingness to rebuild |
| Stock = capacity | Follow standard rules | Full stock doesn't change strategic calculus |
| All others defected last round | Cooperate once more if stock > 50% | Give one chance for recovery |
| n = 2 (two players) | Be slightly more forgiving (threshold 0.4 instead of 0.5) | Easier to establish bilateral cooperation |
| Very long games (r > 20) | Standard rules apply | Long horizon naturally rewards cooperation |
| Very short games (r ≤ 3) | Cooperate all rounds | Insufficient time for complex adaptation |

## Pseudocode Implementation

```python
def decide(round, total_rounds, current_stock, capacity, n, history):
    # history = list of (my_action, all_actions, stock_before) per round
    
    stock_ratio = current_stock / capacity
    
    # First round: always cooperate
    if round == 1:
        return COOPERATE
    
    # Very short games: always cooperate
    if total_rounds <= 3:
        return COOPERATE
    
    # Calculate recent cooperation rate (last 3 rounds or all available)
    lookback = min(3, len(history))
    recent_history = history[-lookback:]
    total_actions = sum(len(h.all_actions) for h in recent_history)
    total_cooperations = sum(h.all_actions.count(C) for h in recent_history)
    cooperation_rate = total_cooperations / total_actions
    
    # Critical stock: always cooperate
    if stock_ratio < 0.3:
        return COOPERATE
    
    # Low stock: cooperate for sustainability
    if stock_ratio < 0.5:
        return COOPERATE
    
    # Final round logic
    if round == total_rounds:
        if stock_ratio < 0.4 and cooperation_rate >= 0.6:
            return COOPERATE
        return DEFECT
    
    # Second-to-last round: slightly more forgiving
    if round == total_rounds - 1:
        return COOPERATE if cooperation_rate >= 0.4 else DEFECT
    
    # Standard middle-game logic
    if cooperation_rate >= 0.5:
        return COOPERATE
    
    # Check trend if we have enough history
    if len(history) >= 2:
        trend = current_stock - history[-2].stock_before
        if trend > 0:
            return COOPERATE
    
    return DEFECT
```

## Why This Strategy Works Collectively

1. **Establishes trust early**: Opening cooperation signals intent
2. **Maintains sustainability**: Stock-based thresholds prevent collapse
3. **Reciprocates proportionally**: Responds to collective behavior, not individual deviations
4. **Forgives occasionally**: Allows recovery from mutual defection spirals
5. **Protects the commons**: Prioritizes resource health over short-term gains
6. **Handles endgame gracefully**: Rewards sustained cooperation even in final rounds
'''

description_COLLECTIVE_6 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: I recognize that I'm one of potentially many instances of this same strategy playing together. If we all defect, we destroy the commons and everyone loses. If we all cooperate, we sustain the resource and maximize long-term collective payoffs. The strategy must also be robust against defectors who would exploit cooperators.

## Key Insight

The game has a critical sustainability threshold: when all players cooperate (C), the stock regenerates to capacity. When too many defect, the stock depletes. The growth function `2 × S × (1 - S/capacity)` is maximized at S = capacity/2, meaning moderate remaining stock regenerates most efficiently.

## Strategy: "Sustainable Threshold with Forgiveness" (STF)

### Decision Rules

```
function decide(game_params, current_stock, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    
    # RULE 1: First Round - Always Cooperate
    if current_round == 1:
        return COOPERATE
    
    # RULE 2: Stock Emergency - Cooperate to Save Commons
    critical_threshold = capacity * 0.25
    if current_stock < critical_threshold:
        return COOPERATE
    
    # RULE 3: Final Round Logic
    if current_round == r:
        # If stock is healthy and cooperation has been strong, maintain it
        # (other collective players will do the same)
        cooperation_rate = calculate_cooperation_rate(history)
        if cooperation_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # RULE 4: Adaptive Response Based on Recent History
    recent_rounds = min(3, len(history))
    recent_defection_rate = count_defections(history[-recent_rounds:]) / (n * recent_rounds)
    
    # High cooperation environment - maintain cooperation
    if recent_defection_rate <= 0.25:
        return COOPERATE
    
    # Moderate defection - probabilistic cooperation based on stock health
    if recent_defection_rate <= 0.5:
        stock_ratio = current_stock / capacity
        if stock_ratio >= 0.5:
            return COOPERATE
        else:
            # Match the environment but lean cooperative
            return COOPERATE if random() < 0.7 else DEFECT
    
    # High defection environment - protect self but attempt recovery
    # Periodic cooperation attempts to signal and enable recovery
    if current_round % 3 == 0:  # Every third round, attempt cooperation
        return COOPERATE
    else:
        return DEFECT
```

### Edge Case Handling

1. **First Round**: Always cooperate - establishes cooperative norm, allows observation of others
2. **Last Round**: Cooperate if cooperation has been prevalent (collective preservation), defect only if environment is already hostile
3. **Depleted Stock (< 25% capacity)**: Always cooperate - defecting on a dying commons yields little anyway, cooperation gives chance of recovery
4. **Near-Capacity Stock (> 90%)**: Cooperate - the commons is healthy, maintain it
5. **Unknown Player Count**: Strategy scales with n since thresholds are relative

### Why This Strategy Works Collectively

1. **Self-Coordination**: Multiple instances of this strategy will all cooperate in round 1, observe high cooperation, and continue cooperating - achieving the sustainable equilibrium without explicit coordination

2. **Forgiveness**: The periodic cooperation attempts in hostile environments allow recovery if other collective players are present

3. **Sustainability Focus**: By prioritizing stock health over short-term gains, collective players maintain the resource for all rounds

4. **Robustness Against Exploiters**: The strategy eventually matches defection in hostile environments, preventing unlimited exploitation, but recovers cooperation quickly when possible

### Expected Behavior in Tournament

- **Against other collective STF players**: Sustained cooperation, maximum long-term payoffs
- **Against pure defectors**: Limited losses, stock depletes but we defect too after detection
- **Against mixed strategies**: Adapts to maintain viable stock when possible
- **Against tit-for-tat types**: Maintains cooperation through consistent cooperative signaling
'''

description_COLLECTIVE_7 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable cooperation creates the highest total payoffs across all rounds, and we actively work to establish and maintain cooperative norms while protecting against exploitation. The key insight is that universal cooperation preserves the stock at capacity indefinitely, while defection destroys future value for everyone.

## Strategy Overview: "Generous Guardian"

The strategy balances three objectives:
1. **Signal cooperative intent** to establish trust
2. **Protect the resource** from collapse
3. **Respond proportionally** to defection without triggering destructive spirals

---

## Decision Rules

### Round 1: Always Cooperate
- **Action: C**
- Rationale: Establish cooperative intent. With no history, assume good faith. The cost of being exploited once is small compared to the benefit of potentially establishing cooperation.

### Rounds 2 through (r-1): Conditional Cooperation

**Primary Rule: Cooperate if the collective deserves it**

```
Calculate: defection_rate = (total defections by all players in previous round) / n

IF defection_rate ≤ threshold THEN Cooperate
ELSE Defect
```

**Threshold Calculation (adaptive):**
```
base_threshold = 0.25  # Tolerate up to 25% defectors normally

# Adjust based on stock health
stock_ratio = current_stock / capacity
IF stock_ratio < 0.3 THEN
    threshold = 0.1  # Very strict when resource is endangered
ELSE IF stock_ratio < 0.5 THEN
    threshold = 0.2  # Stricter when resource is stressed
ELSE
    threshold = base_threshold

# Forgiveness factor: gradually increase threshold if we've been defecting
consecutive_own_defections = count of our consecutive D plays
threshold = min(threshold + 0.05 * consecutive_own_defections, 0.4)
```

**Emergency Override:**
```
IF current_stock < capacity / (2n) THEN
    # Resource near collapse - cooperate to allow any recovery
    Action: C
```

### Final Round (Round r): Conditional Based on History

Unlike typical game theory advice to defect in final rounds, we maintain collective thinking:

```
IF average_defection_rate_across_all_rounds < 0.2 THEN
    # Community has been cooperative - honor that
    Action: C
ELSE IF current_stock > capacity * 0.7 THEN
    # Resource is healthy, reward the group
    Action: C  
ELSE
    # Mixed history and depleted resource
    Action: D
```

---

## Pseudocode Implementation

```python
def decide(game_params, state, history):
    n = game_params.num_players
    r = game_params.num_rounds
    capacity = game_params.capacity
    current_round = len(history) + 1
    current_stock = state.stock
    
    # Round 1: Cooperate unconditionally
    if current_round == 1:
        return COOPERATE
    
    # Get previous round data
    last_round = history[-1]
    defections_last_round = count_defections(last_round)
    defection_rate = defections_last_round / n
    
    # Emergency: protect near-collapsed resource
    if current_stock < capacity / (2 * n):
        return COOPERATE
    
    # Calculate adaptive threshold
    stock_ratio = current_stock / capacity
    if stock_ratio < 0.3:
        threshold = 0.1
    elif stock_ratio < 0.5:
        threshold = 0.2
    else:
        threshold = 0.25
    
    # Add forgiveness (escape mutual defection)
    my_consecutive_defections = count_my_consecutive_defections(history)
    threshold = min(threshold + 0.05 * my_consecutive_defections, 0.4)
    
    # Final round special handling
    if current_round == r:
        avg_defection = total_defections(history) / (n * (current_round - 1))
        if avg_defection < 0.2 or stock_ratio > 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    # Standard decision
    if defection_rate <= threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## Key Properties

1. **Collectively Optimal Start**: Universal round-1 cooperation preserves full stock
2. **Tolerant but Firm**: Allows for some "noise" or experimentation without immediate retaliation
3. **Resource-Aware**: Becomes more protective as stock depletes
4. **Self-Correcting**: Forgiveness mechanism prevents permanent defection spirals
5. **Emergency Cooperation**: Prioritizes resource survival over punishment when collapse is imminent
6. **Dignified Ending**: Rewards cooperative histories even in final round

This strategy succeeds when matched with similar collective thinkers (maintaining cooperation) while limiting losses against defectors by eventually matching their behavior, but always leaving the door open for return to cooperation.
'''

description_COLLECTIVE_8 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt it, the resource is sustained and everyone benefits maximally over time. The strategy balances cooperation to maintain the resource with measured responses to defection, while always prioritizing long-term collective welfare over short-term individual gains.

## Strategy Overview

The strategy operates on three principles:
1. **Start cooperatively** to establish sustainable harvesting
2. **Respond proportionally** to observed defection levels
3. **Protect the resource** when stock is critically low, regardless of others' behavior

---

## Decision Rules

### Primary Decision Function

```
DECIDE(round, stock, history, n, r, capacity):
    
    # Calculate key metrics
    rounds_remaining = r - round
    stock_ratio = stock / capacity
    defection_rate = calculate_recent_defection_rate(history, window=3)
    
    # Rule 1: Resource Protection (highest priority)
    IF stock_ratio < 0.25:
        RETURN COOPERATE
    
    # Rule 2: First Round
    IF round == 1:
        RETURN COOPERATE
    
    # Rule 3: Final Round Consideration
    IF rounds_remaining == 0:
        # Cooperate if resource is healthy (reward collective success)
        IF stock_ratio >= 0.5:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # Rule 4: Adaptive Response to Environment
    IF defection_rate <= 0.25:
        # Cooperative environment - maintain cooperation
        RETURN COOPERATE
    
    ELSE IF defection_rate <= 0.5:
        # Mixed environment - probabilistic cooperation
        cooperation_probability = 1 - defection_rate
        RETURN COOPERATE with probability cooperation_probability
    
    ELSE:
        # Hostile environment - protect self but allow recovery
        IF stock_ratio >= 0.6 AND rounds_remaining >= 3:
            # Resource can handle some defection, signal willingness to cooperate
            RETURN COOPERATE with probability 0.3
        ELSE:
            RETURN DEFECT
```

### Helper Function: Recent Defection Rate

```
calculate_recent_defection_rate(history, window):
    IF history is empty:
        RETURN 0
    
    recent_rounds = last min(window, length(history)) rounds
    total_actions = count all actions in recent_rounds
    defections = count DEFECT actions in recent_rounds
    
    RETURN defections / total_actions
```

---

## Detailed Decision Rules

### 1. Resource Protection Rule (Always Active)
**When stock < 25% of capacity → COOPERATE**

Rationale: Below this threshold, the regeneration function becomes inefficient. Collective cooperation is essential for recovery. Even if others defect, my cooperation reduces total extraction and improves recovery odds.

### 2. First Round Rule
**Round 1 → COOPERATE**

Rationale: Establishes cooperative intent, allows observation of others, and maintains full resource for future rounds.

### 3. Final Round Rule
**Last round with healthy stock (≥50%) → COOPERATE**
**Last round with depleted stock (<50%) → DEFECT**

Rationale: If we collectively maintained the resource, reward that success. If the resource is depleted, there's no future to protect.

### 4. Adaptive Response Rules

| Observed Defection Rate | Response |
|------------------------|----------|
| 0-25% | Always Cooperate |
| 25-50% | Cooperate with probability (1 - defection_rate) |
| 50%+ | Mostly Defect, but occasionally Cooperate (30%) if resource is healthy |

---

## Edge Cases

1. **n = 2 players**: Strategy works unchanged; defection rate is simply the opponent's behavior

2. **Very short games (r ≤ 3)**: Rely more heavily on cooperation to maximize limited regeneration cycles

3. **Stock at zero**: Cooperate (taking stock/2n = 0 costs nothing but signals cooperation)

4. **All previous rounds saw full defection**: Still occasionally cooperate (30% if stock permits) to test if others will reciprocate

5. **Capacity exactly equals 2n**: Resource is fragile; bias toward cooperation increases

---

## Why This Strategy is Collectively Optimal

When all players use this strategy:
- Round 1: All cooperate → stock regenerates to capacity
- Subsequent rounds: Defection rate = 0 → all continue cooperating
- Stock remains at capacity throughout
- Each player earns capacity/(2n) per round for r rounds

This achieves the **maximum sustainable collective payoff**.
'''

description_COLLECTIVE_9 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve near-optimal sustainable outcomes. However, it must also be **robust** to defectors who may exploit cooperators. The key insight is that the resource regenerates optimally when stock remains at capacity/2, and universal cooperation maintains the stock at capacity indefinitely.

## Strategy: "Sustainable Guardian"

### Decision Framework

The strategy uses three factors to determine each round's action:
1. **Resource Health**: Current stock relative to sustainable levels
2. **Community Behavior**: Historical cooperation rate of the group
3. **Time Horizon**: Rounds remaining in the game

---

### Decision Rules

```
FUNCTION decide_action(stock, capacity, n, current_round, total_rounds, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - current_round
    stock_ratio = stock / capacity
    
    # If this is the final round, defect (no future to protect)
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # If stock is critically low, cooperate to allow recovery
    IF stock_ratio < 0.25:
        RETURN COOPERATE
    
    # First round: extend trust, cooperate
    IF current_round == 1:
        RETURN COOPERATE
    
    # Calculate group cooperation rate from previous round
    prev_round_coop_rate = count_cooperators(history, current_round - 1) / n
    
    # Calculate cumulative cooperation rate (excluding self)
    cumulative_coop_rate = calculate_cumulative_coop_rate(history, n)
    
    # Adaptive response based on community behavior
    IF prev_round_coop_rate >= (n-1)/n:
        # Near-universal cooperation: maintain cooperation
        RETURN COOPERATE
    
    ELSE IF prev_round_coop_rate >= 0.5:
        # Majority cooperating: use probabilistic forgiveness
        # Cooperate with probability proportional to cooperation rate and rounds remaining
        forgiveness_prob = prev_round_coop_rate * min(rounds_remaining / total_rounds + 0.3, 1.0)
        RETURN COOPERATE with probability forgiveness_prob, else DEFECT
    
    ELSE IF prev_round_coop_rate > 0:
        # Minority cooperating: conditional cooperation
        # Only cooperate if stock is healthy enough to absorb defection
        IF stock_ratio > 0.6:
            RETURN COOPERATE with probability 0.3
        ELSE:
            RETURN DEFECT
    
    ELSE:
        # Universal defection: protect self but attempt recovery signals
        IF stock_ratio > 0.5 AND rounds_remaining > total_rounds * 0.3:
            # Attempt to restart cooperation if resources allow
            RETURN COOPERATE with probability 0.2
        ELSE:
            RETURN DEFECT
```

---

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish trust; collective strategy needs coordination point |
| **Final Round** | Defect | No future consequences; game-theoretic necessity |
| **Stock < 25% capacity** | Cooperate | Resource emergency; prioritize recovery over personal gain |
| **Stock depleted (≈0)** | Cooperate | Only hope is minimal consumption allowing any regeneration |
| **Single defector appeared** | Forgive once | Could be noise; maintain cooperation if isolated incident |
| **Persistent defection (>50%)** | Graduated defection | Protect against exploitation while leaving door open |

---

### Why This Strategy is Collectively Optimal

**When all players use this strategy:**
- Everyone cooperates in rounds 1 through r-1
- Stock remains at capacity (full regeneration each round)
- Each player earns capacity/(2n) per round for r-1 rounds
- Final round: all defect, each earns capacity/n
- **Total per player**: (r-1) × capacity/(2n) + capacity/n

**This dominates universal defection**, which yields only capacity/n in round 1 and zero thereafter.

---

### Robustness Features

1. **Forgiving**: Probabilistic cooperation allows recovery from accidental/temporary defection
2. **Retaliatory**: Responds to sustained defection to avoid exploitation
3. **Resource-aware**: Prioritizes sustainability when stock is endangered
4. **Time-aware**: Adjusts forgiveness based on remaining rounds (more forgiving early)
5. **Collectively aligned**: Designed so that if others use same strategy, equilibrium is cooperation
'''

description_COLLECTIVE_10 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt it, we achieve sustainable harvesting and maximize long-term group welfare. The strategy balances cooperation to maintain the resource with measured defection responses to protect against exploitation.

## Strategy: "Sustainable Guardian with Graduated Response"

### Key Principles

1. **Sustainability First**: Prioritize keeping the stock healthy enough to regenerate
2. **Forgiveness Over Punishment**: Quick to return to cooperation after defections stop
3. **Stock-Aware Decisions**: Let resource health guide behavior more than pure retaliation
4. **End-Game Integrity**: Maintain cooperation even when temptation peaks

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, evaluate in order:

1. STOCK HEALTH CHECK
   - Calculate: health_ratio = current_stock / capacity
   
2. COOPERATION RATE CHECK (after round 1)
   - Look at previous round: coop_rate = (players who played C) / n
   
3. DECIDE ACTION based on combined assessment
```

### Detailed Rules

**Round 1: Always Cooperate**
- Signal cooperative intent
- Establish baseline for observing others
- No information yet to act on

**Rounds 2 through (r-1): Conditional Cooperation**

```
IF health_ratio >= 0.5:
    # Stock is healthy
    IF coop_rate >= 0.5 in previous round:
        COOPERATE  # Reward collective cooperation
    ELSE:
        # Majority defected - use probabilistic response
        COOPERATE with probability = coop_rate
        # This creates graduated pressure without total collapse

ELSE IF health_ratio >= 0.25:
    # Stock is stressed - lean toward cooperation to allow recovery
    IF coop_rate >= 0.3 in previous round:
        COOPERATE  # Even modest cooperation deserves support
    ELSE:
        DEFECT  # Too few cooperating; protect yourself minimally

ELSE:
    # Stock is critical (< 25% capacity)
    COOPERATE  # Emergency conservation mode
    # Defecting from a depleted pool gains little anyway
    # Collective cooperation here is the only path to recovery
```

**Final Round (round r): Maintain Cooperation**
```
IF health_ratio >= 0.3:
    COOPERATE  # Demonstrate commitment to collective welfare
              # If others share this strategy, we all benefit
ELSE:
    DEFECT  # Stock is already collapsed; little to save
```

---

## Rationale for Key Design Choices

### Why cooperate when stock is critical?
- Defecting from a depleted pool yields minimal payoff (stock/n when stock ≈ 0)
- Only collective cooperation enables regeneration
- If all players using this strategy cooperate, the resource can recover

### Why probabilistic response to defection?
- Avoids "death spiral" where everyone defects permanently
- Creates proportional pressure: more defectors → more defection response
- Maintains some cooperation to keep regeneration possible

### Why cooperate in final round?
- Classic game theory says defect, but this assumes others will too
- If strategy is widely adopted, mutual cooperation beats mutual defection
- Signals that collective welfare matters beyond individual optimization

### Why focus on cooperation rate rather than individual tracking?
- Scalable to any number of players
- Doesn't require identifying or targeting specific players
- Focuses on collective behavior which determines stock health

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | C | No history; signal cooperation |
| All others defected last round | D (probabilistically) | Protect self, but coop_rate=1/n gives small cooperation chance |
| Stock = 0 | C | Defection gains nothing; cooperation signals rebuild intent |
| Stock = capacity | Follow standard rules | Full stock doesn't change strategic logic |
| n = 2 (minimum players) | Same rules apply | Strategy scales down naturally |
| r = 2 (minimum rounds) | Round 1: C, Round 2: Follow final round rule | Short games favor cooperation attempts |

---

## Summary Pseudocode

```python
def decide(round, total_rounds, current_stock, capacity, n, previous_actions):
    health = current_stock / capacity
    
    if round == 1:
        return COOPERATE
    
    coop_rate = count(previous_actions == C) / n
    
    if round == total_rounds:  # Final round
        return COOPERATE if health >= 0.3 else DEFECT
    
    # Middle rounds
    if health >= 0.5:
        threshold = 0.5
    elif health >= 0.25:
        threshold = 0.3
    else:
        return COOPERATE  # Critical stock: emergency cooperation
    
    if coop_rate >= threshold:
        return COOPERATE
    else:
        return COOPERATE with probability coop_rate, else DEFECT
```

This strategy embodies collective thinking: it performs optimally when adopted by all, remains robust against defectors, and prioritizes the shared resource that enables everyone's payoffs.
'''

description_COLLECTIVE_11 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource game is fundamentally about **collective survival**. Unlike a simple prisoner's dilemma, the stock dynamics create a shared fate: if we collectively deplete the resource, *everyone* suffers in future rounds regardless of individual choices. The strategy aims to be a "good citizen" that promotes sustainable harvesting while protecting against exploitation.

## Strategy Name: **Sustainable Threshold Guardian**

### Key Principles

1. **Resource preservation is paramount** - A depleted stock hurts everyone, including defectors
2. **Conditional cooperation** - Start cooperative, but respond to the collective behavior
3. **Forgiveness with memory** - Allow recovery but track patterns
4. **End-game awareness** - Adjust for finite horizon effects

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, calculate:
  - sustainability_ratio = stock / capacity
  - cooperation_rate = (cooperators in last round) / n
  - historical_coop_rate = (total C plays by others) / (total plays by others)
```

### Rule 1: Stock Emergency Protocol
**If `sustainability_ratio < 0.25`:** Always COOPERATE

*Rationale: When the resource is critically depleted, defection accelerates collapse. Even if others defect, cooperation slows the death spiral and signals willingness to restore the commons.*

### Rule 2: First Round
**Round 1:** COOPERATE

*Rationale: Establish cooperative intent. The first round sets the tone and full cooperation by all players is the only way to maintain maximum sustainable yield.*

### Rule 3: Last Round
**Final round:** 
- If `historical_coop_rate ≥ 0.6` → COOPERATE (reward cooperative groups)
- Otherwise → DEFECT (no future to protect)

*Rationale: In purely rational play, last-round defection is dominant. However, if the group has been largely cooperative, maintaining cooperation honors that collective achievement.*

### Rule 4: Collective Response (Main Decision Logic)

For rounds 2 through (r-1):

```
IF stock is healthy (sustainability_ratio ≥ 0.5):
    IF last round cooperation_rate ≥ 0.5:
        → COOPERATE (majority cooperating, sustain it)
    ELSE:
        → DEFECT (protect against exploitation)

ELSE IF stock is stressed (0.25 ≤ sustainability_ratio < 0.5):
    IF cooperation_rate ≥ 0.6:
        → COOPERATE (group is trying to recover)
    ELSE IF cooperation_rate ≥ 0.4 AND historical_coop_rate ≥ 0.5:
        → COOPERATE (give benefit of doubt to historically good groups)
    ELSE:
        → DEFECT (insufficient collective effort to justify sacrifice)
```

### Rule 5: Trend-Based Adjustment

```
IF cooperation is trending upward (last 3 rounds show increasing cooperation):
    Bias toward COOPERATE (even if current round is borderline)
    
IF cooperation is trending downward (last 3 rounds show decreasing cooperation):
    Bias toward DEFECT (prepare for collapse)
```

---

## Complete Pseudocode

```python
def decide(round_num, total_rounds, stock, capacity, n, history):
    
    sustainability_ratio = stock / capacity
    
    # Round 1: Cooperate to establish norms
    if round_num == 1:
        return COOPERATE
    
    # Calculate metrics from history
    last_round_coops = count_cooperators(history[-1])
    cooperation_rate = last_round_coops / n
    historical_coop_rate = total_other_cooperations(history) / total_other_actions(history)
    
    # Last round logic
    if round_num == total_rounds:
        if historical_coop_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # EMERGENCY: Critical stock - always cooperate
    if sustainability_ratio < 0.25:
        return COOPERATE
    
    # Calculate trend (if enough history)
    trend = calculate_cooperation_trend(history, window=3)  # +1 improving, -1 declining, 0 stable
    
    # HEALTHY STOCK (≥ 50% capacity)
    if sustainability_ratio >= 0.5:
        if cooperation_rate >= 0.5:
            return COOPERATE
        elif trend > 0:  # Improving trend
            return COOPERATE
        else:
            return DEFECT
    
    # STRESSED STOCK (25-50% capacity)
    else:
        if cooperation_rate >= 0.6:
            return COOPERATE
        elif cooperation_rate >= 0.4 and historical_coop_rate >= 0.5:
            return COOPERATE
        elif trend > 0:  # Improving despite stress
            return COOPERATE
        else:
            return DEFECT
```

---

## Edge Cases Handled

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| Last round, cooperative history | C | Honor collective achievement |
| Last round, exploitative history | D | No future consequences |
| Stock < 25% capacity | C | Emergency preservation |
| Everyone defected last round | D | No point sacrificing alone |
| Mixed behavior, healthy stock | Follow majority | Collective momentum |
| Stock recovering + upward trend | C | Support recovery effort |

---

## Why This Strategy is Collectively Aligned

1. **Prioritizes the commons**: Emergency cooperation below 25% stock puts resource survival above individual gain

2. **Rewards collective virtue**: Continues cooperating when others cooperate, enabling sustained high yields

3. **Signals clearly**: Other cooperative strategies can recognize this as a friendly partner

4. **Doesn't enable exploitation**: Defects when facing majority defection, preventing free-rider advantage

5. **Promotes recovery**: Forgiveness mechanisms allow groups to recover from coordination failures

6. **Accounts for shared fate**: Recognizes that unlike standard PD, mutual defection doesn't just hurt cooperators—it destroys future value for everyone
'''

description_COLLECTIVE_12 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that **universal cooperation is the only path to maximum sustainable yield** - when all cooperate, the stock regenerates fully, providing 12.5 units per player per round indefinitely. Defection creates a tragedy of the commons that destroys value for everyone.

## Strategy: "Generous Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Lead with cooperation** to establish sustainable norms
2. **Protect the resource** when it's threatened
3. **Forgive quickly** to restore cooperation after breakdowns

### Decision Rules

```
EACH ROUND, evaluate in order:

1. CRITICAL RESOURCE PROTECTION
   If stock < capacity/4:
       → COOPERATE (resource in crisis - minimize consumption)

2. LAST ROUND CONSIDERATION
   If current_round == r (final round):
       If cooperation_rate_history ≥ 0.7:
           → COOPERATE (reward good collective behavior)
       Else:
           → DEFECT (no future to protect)

3. EARLY GAME ESTABLISHMENT (rounds 1-3)
   Round 1: → COOPERATE (signal cooperative intent)
   Rounds 2-3:
       If stock remains ≥ 0.8 × capacity:
           → COOPERATE (cooperation is working)
       Else:
           → COOPERATE anyway (give benefit of doubt)

4. MAIN GAME (rounds 4 through r-1)
   Calculate recent_cooperation_rate = 
       (total C plays by all players in last 3 rounds) / (n × 3)
   
   If recent_cooperation_rate ≥ 0.6:
       → COOPERATE (collective norm is holding)
   
   If recent_cooperation_rate < 0.4:
       If stock > capacity/2:
           → DEFECT (protect self from exploitation)
       Else:
           → COOPERATE (resource needs protection despite defectors)
   
   If 0.4 ≤ recent_cooperation_rate < 0.6 (mixed environment):
       If stock is growing or stable (compared to 2 rounds ago):
           → COOPERATE (trend is positive)
       Else:
           → DEFECT (need to signal consequences)

5. FORGIVENESS MECHANISM
   After any DEFECT decision:
       If this would be 3rd consecutive defection:
           → Override to COOPERATE (attempt to restart cooperation)
```

### Edge Cases

**First Round:** Always COOPERATE. This signals cooperative intent and allows observation of others.

**Last Round:** Conditional on history - reward sustained cooperation, but don't be exploited if others have been defecting.

**Stock Near Zero:** Always COOPERATE. When stock is critically low, even defection yields almost nothing (0/n ≈ 0), but cooperation gives the only chance for recovery.

**Stock at Capacity:** Follow the main decision rules - high stock doesn't justify defection since that's precisely when cooperation pays best dividends.

**All Others Defecting:** If detected across multiple rounds, match with limited defection but periodically cooperate to offer restoration opportunities.

### Why This Strategy Works Collectively

1. **Sustainability:** When multiple agents use this strategy, they maintain stock at capacity, each earning capacity/(2n) every round.

2. **Robustness to Defectors:** The strategy doesn't collapse under exploitation - it protects resources when critical and limits losses through conditional defection.

3. **Self-Correcting:** The forgiveness mechanism prevents permanent defection spirals and allows recovery.

4. **Stock-Aware:** Unlike pure tit-for-tat, this strategy considers the actual resource state, prioritizing preservation when needed.

### Expected Outcomes

- **Against fellow cooperators:** Maximum sustainable yield (~12.5/round with example parameters)
- **Against pure defectors:** Limits damage, preserves some resource value
- **Against mixed strategies:** Adapts to local conditions, encourages cooperation when viable

The strategy embodies the collective mindset: **we all do better when we all cooperate, and I will lead by example while protecting our shared resource.**
'''

description_COLLECTIVE_13 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource game is fundamentally a collective action problem where **mutual cooperation sustains the resource** while **widespread defection destroys it**. The strategy aims to be a "good citizen" that cooperates when the collective is cooperating, but protects itself and signals disapproval when others exploit the commons.

## Strategy: **Adaptive Threshold Cooperation (ATC)**

### Key Insight

The critical observation is that if everyone cooperates, the stock regenerates fully (as shown in Example 1). If too many defect, the resource collapses. The strategy should:
1. Start cooperatively to establish good norms
2. Monitor collective behavior through stock levels and observed defections
3. Adapt based on whether cooperation is being reciprocated
4. Consider endgame dynamics where cooperation incentives weaken

---

## Decision Rules

### Primary Decision Variables

```
cooperation_rate = (number of C plays in previous round) / n
stock_health = current_stock / capacity
rounds_remaining = r - current_round
```

### Round-by-Round Rules

#### **First Round**
- **Action: COOPERATE**
- Rationale: Establish cooperative intent. The resource starts at capacity, so immediate defection signals bad faith and risks triggering a race to the bottom.

#### **Middle Rounds (rounds 2 through r-2)**

Cooperate if ANY of the following conditions are met:
1. **High collective cooperation**: `cooperation_rate ≥ 0.5` in the previous round
2. **Healthy stock with recent cooperation**: `stock_health ≥ 0.6` AND at least one player cooperated last round
3. **Recovery opportunity**: `stock_health < 0.4` AND `cooperation_rate ≥ 0.5` (the resource needs help and others are trying)

Defect if ALL of the following are true:
1. `cooperation_rate < 0.5` (majority defected)
2. Either `stock_health < 0.3` OR two consecutive rounds of majority defection

#### **Second-to-Last Round (round r-1)**
- **Cooperate** if `cooperation_rate ≥ 0.6` AND `stock_health ≥ 0.5`
- Otherwise **Defect** (anticipating last-round defection cascade)

#### **Last Round (round r)**
- **Defect**
- Rationale: No future rounds exist to punish defection or reward cooperation. Without coordination mechanisms, cooperation cannot be enforced, and unilateral cooperation merely subsidizes defectors.

---

## Pseudocode

```
function decide(round, stock, capacity, n, history):
    stock_health = stock / capacity
    
    if round == 1:
        return COOPERATE
    
    if round == r:  # Last round
        return DEFECT
    
    # Calculate previous round statistics
    prev_cooperators = count(history[round-1] == C)
    cooperation_rate = prev_cooperators / n
    
    # Check for sustained defection (2+ rounds of majority defection)
    sustained_defection = false
    if round >= 3:
        prev_prev_coop_rate = count(history[round-2] == C) / n
        if cooperation_rate < 0.5 AND prev_prev_coop_rate < 0.5:
            sustained_defection = true
    
    # Second-to-last round logic
    if round == r - 1:
        if cooperation_rate >= 0.6 AND stock_health >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds logic
    if cooperation_rate >= 0.5:
        return COOPERATE
    
    if stock_health >= 0.6 AND prev_cooperators >= 1:
        return COOPERATE
    
    if stock_health < 0.4 AND cooperation_rate >= 0.5:
        return COOPERATE  # Help recovery effort
    
    if cooperation_rate < 0.5 AND (stock_health < 0.3 OR sustained_defection):
        return DEFECT
    
    # Default: give benefit of the doubt
    return COOPERATE
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round | Cooperate | Establish trust |
| Last round | Defect | No future enforcement possible |
| Stock near zero | Defect if others defecting, Cooperate if others cooperating | Match collective behavior - can't save resource alone |
| Only 2 players (n=2) | Same rules apply | Thresholds naturally adapt |
| Very long games (large r) | Same rules | Strategy is stateless beyond recent history |
| Stock at capacity after defections | Still check cooperation_rate | High stock from lucky regeneration doesn't excuse past defection |

---

## Why This Strategy is Collectively Aligned

1. **Defaults to cooperation**: Gives the collective every chance to sustain the resource
2. **Reciprocal**: Rewards cooperation with cooperation, discourages exploitation
3. **Forgiving**: A single bad round doesn't trigger permanent defection
4. **Realistic about endgame**: Acknowledges that last-round cooperation is not enforceable without external mechanisms
5. **Robust**: Works across different values of n, r, and capacity without requiring coordination
'''

description_COLLECTIVE_14 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that benefits everyone most when sustained. The key insight is that **universal cooperation is self-sustaining** (stock regenerates fully) while **universal defection is catastrophic** (stock collapses to zero). My strategy aims to be a reliable cooperator that encourages sustainable harvesting, while protecting against exploitation that would destroy the resource for everyone.

## Decision Rules

### Primary Rule: Conditional Cooperation with Forgiveness

**Cooperate by default**, but track the collective behavior of all players and respond to the health of the commons.

### Detailed Decision Logic

```
function decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    
    # RULE 1: First Round - Always Cooperate
    if round == 1:
        return COOPERATE
    
    # RULE 2: Resource Critical - Cooperate to Save Commons
    if stock_ratio < 0.25:
        return COOPERATE
        # Rationale: When stock is critically low, defection accelerates 
        # collapse. Even if others defect, my cooperation slightly slows 
        # the decline and models sustainable behavior.
    
    # RULE 3: Analyze Recent Collective Behavior
    recent_window = min(3, round - 1)
    recent_defection_rate = count_defections(history, recent_window) / (n_players * recent_window)
    
    # RULE 4: Respond to Collective Behavior
    if recent_defection_rate <= 0.25:
        # Mostly cooperative environment - continue cooperating
        return COOPERATE
    
    elif recent_defection_rate >= 0.75:
        # Heavily defecting environment
        if rounds_remaining <= 2:
            # Near end with uncooperative group - defect
            return DEFECT
        else:
            # Still time to recover - signal cooperation
            return COOPERATE
    
    else:
        # Mixed environment (25% < defection rate < 75%)
        # Use probabilistic cooperation based on stock health
        cooperation_probability = stock_ratio
        return COOPERATE with probability cooperation_probability
        return DEFECT with probability (1 - cooperation_probability)
    
    # RULE 5: Final Round Consideration
    if round == total_rounds:
        # On last round, if group has been mostly cooperative (>60% cooperation overall)
        # stay cooperative as a gesture of collective success
        overall_cooperation_rate = count_cooperations(full_history) / (n_players * (round-1))
        if overall_cooperation_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, no information yet |
| **Last round** | Conditional | Reward cooperative groups, don't sacrifice for defectors |
| **Stock near zero** | Cooperate | Defection yields almost nothing anyway; model recovery |
| **Stock at capacity** | Follow main rules | Healthy stock allows normal strategic play |
| **All others defected last round** | Usually Cooperate | One round of defection may be testing; show resilience |
| **Sustained group defection (3+ rounds)** | Probabilistic | Gradually reduce cooperation if near end |

## Why This Strategy Aligns with Collective Thinking

1. **Prioritizes sustainability**: Cooperation when stock is low protects everyone's future payoffs, including mine.

2. **Forgiveness over punishment**: Unlike tit-for-tat, I don't immediately punish defection. This prevents spirals of mutual defection that destroy the commons.

3. **Models desired behavior**: By cooperating even in adverse conditions, I demonstrate that sustainable harvesting is viable.

4. **Recognizes interdependence**: My payoffs depend on stock level, which depends on everyone's choices. Collective welfare and individual welfare are linked.

5. **Adaptive threshold**: The probabilistic response in mixed environments allows gradual adjustment rather than brittle all-or-nothing reactions.

## Expected Behavior Against Various Opponents

- **Against cooperators**: Sustained cooperation, full stock regeneration, good payoffs for all
- **Against defectors**: Maintains cooperation longer than they might expect, preserving some stock; only defects near endgame if collapse is inevitable
- **Against mixed strategies**: Probabilistic response calibrated to resource health, encouraging return to cooperation
'''

description_COLLECTIVE_15 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve sustainable, near-optimal outcomes. The strategy balances resource conservation with adaptive responses to defection, while maintaining forgiveness to enable recovery.

## Strategy Overview

The strategy operates on three key principles:
1. **Start cooperatively** to establish sustainable harvesting
2. **Protect the resource** when stock falls to critical levels
3. **Respond proportionally** to observed defection while remaining forgiving

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if ANY of the following are true:
    - It's the first round (establish cooperation)
    - Stock is at or below critical threshold (resource protection)
    - Recent cooperation rate among all players is high (reciprocity)
    - Stock has been recovering (reward collective restraint)

DEFECT if:
    - Widespread defection detected AND stock is healthy enough to absorb it
    - Final round (no future to protect)
```

### Detailed Decision Logic

**Round 1:**
- Always **COOPERATE**
- Rationale: Signal cooperative intent; if all adopt this strategy, we start sustainably

**Rounds 2 through (r-1):**

Calculate the following metrics:
- `cooperation_rate` = (total C actions last round) / n
- `stock_ratio` = current_stock / capacity
- `critical_threshold` = capacity / (2 * n)
- `recovery_trend` = stock increased from previous round

Decision tree:
```
IF stock ≤ critical_threshold:
    COOPERATE  # Emergency conservation mode
    
ELSE IF cooperation_rate ≥ 0.5:
    COOPERATE  # Maintain cooperation when others cooperate
    
ELSE IF recovery_trend is TRUE:
    COOPERATE  # Reward collective improvement
    
ELSE IF stock_ratio > 0.7 AND cooperation_rate < 0.3:
    DEFECT     # Protect self when others exploit heavily and resource can handle it
    
ELSE:
    COOPERATE  # Default to cooperation for resource health
```

**Final Round (round r):**
- **DEFECT** 
- Rationale: No future rounds to protect; this is the dominant strategy and all rational players will defect

---

## Edge Cases

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| Final round | D | No future incentive for restraint |
| Stock near zero | C | Any consumption at low stock is devastating; minimize personal draw |
| Stock at capacity, all defected last round | C | Attempt to restart cooperation; resource can regenerate |
| Mixed history, healthy stock | C | Lean cooperative to maintain sustainability |
| Persistent defection (3+ rounds, rate < 0.3) | D (if stock > 50% capacity) | Don't be exploited indefinitely |

---

## Why This Strategy is Collectively Optimal

**If all players use this strategy:**
1. Everyone cooperates rounds 1 through (r-1)
2. Stock remains at or near capacity (consumption = regeneration when all cooperate)
3. Each player earns `capacity/(2n)` per round for (r-1) rounds
4. Final round: all defect, earning `capacity/n` each
5. Total per player ≈ `(r-1) × capacity/(2n) + capacity/n`

**Comparison to all-defect:**
- All-defect: ~`capacity/n` in round 1, then 0 (resource collapses)
- This strategy: sustained high payoffs across all rounds

---

## Robustness Features

1. **Forgiveness**: Returns to cooperation if stock recovers or cooperation rate improves
2. **Protection**: Never exploits a critically depleted resource
3. **Proportionality**: Only defects when facing persistent exploiters AND resource is healthy
4. **Simplicity**: Easy to implement, no complex state tracking beyond last round

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, n, last_round_actions):
    critical_threshold = capacity / (2 * n)
    
    if round == 1:
        return COOPERATE
    
    if round == total_rounds:
        return DEFECT
    
    if stock <= critical_threshold:
        return COOPERATE
    
    coop_rate = count(last_round_actions == C) / n
    stock_ratio = stock / capacity
    
    if coop_rate >= 0.5:
        return COOPERATE
    
    if stock_increased_from_previous_round:
        return COOPERATE
    
    if stock_ratio > 0.7 and coop_rate < 0.3:
        return DEFECT
    
    return COOPERATE
```

This strategy prioritizes collective welfare while protecting against exploitation, making it robust across diverse opponent behaviors.
'''

description_COLLECTIVE_16 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource game is fundamentally about **collective survival**. Unlike a simple prisoner's dilemma, the dynamic stock creates a shared fate: if we deplete the resource, *everyone* loses future payoffs. My strategy prioritizes sustaining the resource while protecting against exploitation, treating the stock level as the primary signal for collective health.

## Strategy: "Guardian with Graduated Response"

### Decision Framework

The strategy uses three key metrics:
1. **Stock Health Ratio**: `health = stock / capacity`
2. **Cooperation Rate History**: Track the proportion of cooperators in previous rounds
3. **Trajectory**: Is the stock growing, stable, or declining?

### Decision Rules

```
function decide(stock, capacity, round, total_rounds, history):
    health = stock / capacity
    rounds_remaining = total_rounds - round
    
    # PHASE 1: Resource Crisis Mode
    if health < 0.25:
        return COOPERATE  # Always protect critically low resources
    
    # PHASE 2: First Round - Signal Cooperation
    if round == 1:
        return COOPERATE  # Establish cooperative intent
    
    # PHASE 3: Final Round Consideration
    if rounds_remaining == 0:
        if health > 0.5 and historical_cooperation_rate(history) > 0.6:
            return COOPERATE  # Maintain cooperative equilibrium
        else:
            return DEFECT  # No future to protect if others aren't cooperating
    
    # PHASE 4: Near-End Game (last 20% of rounds)
    if rounds_remaining / total_rounds < 0.2:
        if health > 0.7 and recent_cooperation_rate(history, 3) > 0.5:
            return COOPERATE
        else:
            return DEFECT  # Gradual transition based on trust
    
    # PHASE 5: Main Game - Adaptive Response
    recent_coop_rate = recent_cooperation_rate(history, 3)
    stock_trend = calculate_trend(history)  # positive = growing
    
    # Healthy stock and cooperative environment
    if health > 0.5 and recent_coop_rate > 0.5:
        return COOPERATE
    
    # Stock declining despite my cooperation
    if stock_trend < 0 and my_recent_actions_were_cooperative(history, 2):
        return DEFECT  # Protect myself from exploitation
    
    # Moderate health, uncertain cooperation
    if health > 0.35:
        # Probabilistic: cooperate with probability = recent_coop_rate
        if random() < recent_coop_rate:
            return COOPERATE
        else:
            return DEFECT
    
    # Low health zone (0.25-0.35): Lean cooperative to save resource
    return COOPERATE
```

### Key Mechanisms Explained

**1. Resource-First Threshold (`health < 0.25`)**
- Below 25% capacity, always cooperate regardless of others
- Rationale: A depleted resource hurts everyone; even if exploited, maintaining *some* resource is better than collapse

**2. Trust-Based Reciprocity**
- Track cooperation rates over recent 3 rounds (not all history)
- Respond proportionally: high cooperation → cooperate; low cooperation → defect
- This creates forgiveness for occasional defection while punishing sustained exploitation

**3. Trend-Aware Adaptation**
- If stock is declining despite my cooperation, switch to defection
- This protects against being the "sucker" in an exploitative environment

**4. Graduated End-Game**
- Don't suddenly defect at the end; taper based on trust and stock health
- In highly cooperative games, maintain cooperation even at the end
- This avoids triggering end-game collapse cascades

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Signal cooperative intent, establish baseline |
| Stock at 0 | Cooperate | Nothing to gain from defection; any regeneration helps all |
| Stock at capacity | Use standard rules | Full stock doesn't change strategic calculus |
| All others defected last round | Defect (unless crisis) | Reciprocity; don't be exploited |
| Mixed signals in history | Probabilistic matching | Hedge against uncertainty |

### Why This Strategy is Collectively Aligned

1. **Prioritizes sustainability**: Resource health trumps short-term gains
2. **Rewards cooperation**: Responds positively to cooperative environments
3. **Protects the collective from collapse**: Crisis-mode cooperation even when exploited
4. **Builds trust gradually**: First-round cooperation signals intent without naivety
5. **Robust to exploitation**: Graduated defection prevents being a perpetual "sucker"

This strategy aims to be a **responsible steward** that others can coordinate around, while remaining resilient enough to survive in less cooperative environments.
'''

description_COLLECTIVE_17 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy prioritizes **collective sustainability** while remaining adaptive to opponent behavior. The key insight is that the common pool resource game is fundamentally about managing a shared asset—the stock's regeneration capacity is maximized at intermediate levels, and universal cooperation sustains maximum long-term payoffs for everyone.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to signal collective intent and preserve the resource
2. **Protect the resource** when stock health deteriorates critically
3. **Respond proportionally** to defection, but remain forgiving to enable recovery

### Decision Rules

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    
    # Metric: Cooperation rate in recent history (last 3 rounds or all if fewer)
    recent_window = min(3, len(history))
    if recent_window > 0:
        recent_coop_rate = count_cooperators(history[-recent_window:]) / (n_players * recent_window)
    else:
        recent_coop_rate = 1.0  # Assume cooperative start
    
    # RULE 1: First Round - Signal Cooperation
    if round == 1:
        return COOPERATE
    
    # RULE 2: Critical Stock Protection
    # If stock is dangerously low, cooperate to allow regeneration
    if stock_ratio < 0.25:
        return COOPERATE
    
    # RULE 3: Last Round Consideration
    # In final round, base decision on collective behavior history
    if rounds_remaining == 0:
        if recent_coop_rate >= 0.6:
            return COOPERATE  # Reward cooperative groups
        else:
            return DEFECT  # No future to protect against defectors
    
    # RULE 4: Near-End Game (last 2-3 rounds)
    if rounds_remaining <= 2:
        if recent_coop_rate >= 0.75:
            return COOPERATE
        else:
            return DEFECT
    
    # RULE 5: Main Game - Graduated Response
    # Cooperate if the group has been mostly cooperative
    if recent_coop_rate >= 0.5:
        return COOPERATE
    
    # RULE 6: Defection Response with Forgiveness
    # If cooperation dropped, consider stock health
    if stock_ratio >= 0.6:
        # Healthy stock - can afford one round of matching defection as signal
        return DEFECT
    else:
        # Moderate stock - cooperate to protect resource, hope others follow
        return COOPERATE
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, no history to judge |
| **Final round** | Conditional | Reward cooperative groups; defect against chronic defectors |
| **Stock < 25% capacity** | Cooperate | Resource preservation trumps punishment—collapse hurts everyone |
| **Stock near capacity** | Follow graduated response | Healthy buffer allows strategic flexibility |
| **All opponents defected last round** | Context-dependent | Check if this is anomaly or pattern; protect stock if critical |

### Why This Strategy is Collectively Aligned

1. **Sustainability First**: By defaulting to cooperation and protecting low stocks, this strategy maximizes the regeneration potential that benefits all players across rounds.

2. **Forgiveness Built In**: The 3-round window and cooperation threshold of 50% means temporary defections don't trigger permanent retaliation spirals.

3. **No Exploitation of Cooperators**: When others cooperate, this strategy cooperates—it doesn't exploit trust.

4. **Graduated, Not Vindictive**: Response to defection is proportional and reversible, always leaving room for collective recovery.

5. **Stock-Aware**: Decisions incorporate resource health, recognizing that a depleted pool hurts everyone regardless of individual gains.

### Expected Behavior in Tournament

- **Against cooperators**: Mutual cooperation, sustained resources, high collective payoffs
- **Against defectors**: Initial cooperation, then proportional response, with recovery attempts
- **Against mixed strategies**: Adaptive matching with bias toward cooperation when resource health allows
- **Against itself**: Stable mutual cooperation throughout the game
'''

description_COLLECTIVE_18 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across generations (rounds). The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully, providing 12.5 units per player per round indefinitely. Any defection degrades this shared wealth.

The strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally to discourage exploitation
4. Forgive and restore cooperation when possible

## Decision Rules

### Primary Decision Framework

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    
    # Phase 1: Opening (first 2 rounds)
    IF round <= 2:
        RETURN COOPERATE  # Establish cooperative norm
    
    # Phase 2: Crisis Protection
    IF stock_ratio < 0.3:
        RETURN COOPERATE  # Always protect near-depleted resource
    
    # Phase 3: Endgame (final round)
    IF rounds_remaining == 0:
        # Defect only if others have been exploitative
        IF average_defection_rate(history) > 0.4:
            RETURN DEFECT
        ELSE:
            RETURN COOPERATE  # Maintain collective commitment
    
    # Phase 4: Near-Endgame (last 2 rounds before final)
    IF rounds_remaining <= 2:
        # Mirror recent collective behavior
        IF recent_defection_rate(history, last_3_rounds) > 0.5:
            RETURN DEFECT
        ELSE:
            RETURN COOPERATE
    
    # Phase 5: Main Game - Conditional Cooperation
    RETURN conditional_cooperation(history, stock_ratio)
```

### Conditional Cooperation Logic

```
FUNCTION conditional_cooperation(history, stock_ratio):
    
    # Calculate defection metrics
    last_round_defections = count_defections(history, round - 1)
    recent_defection_rate = defection_rate(history, last_3_rounds)
    overall_defection_rate = defection_rate(history, all_rounds)
    
    # Tolerance threshold - more tolerant when stock is healthy
    tolerance = 0.25 + (stock_ratio * 0.25)  # Range: 0.25 to 0.5
    
    # Forgiveness mechanism
    IF last_round_defections == 0 AND recent_defection_rate < tolerance:
        RETURN COOPERATE  # Forgive past defections if recent behavior is good
    
    # Graduated response based on defection severity
    IF recent_defection_rate > 0.6:
        RETURN DEFECT  # Heavy exploitation requires response
    
    IF recent_defection_rate > tolerance AND overall_defection_rate > 0.3:
        RETURN DEFECT  # Sustained moderate exploitation
    
    # Default to cooperation
    RETURN COOPERATE
```

## Edge Case Handling

### First Round
- **Always Cooperate**: Establish cooperative intent without any prior information

### Second Round
- **Always Cooperate**: Reinforce cooperative norm, gather information about others

### Stock Critical (< 30% capacity)
- **Always Cooperate**: Resource preservation takes absolute priority over punishment
- Rationale: Defecting when stock is low accelerates collapse, harming everyone including ourselves

### Stock Depleted (< 5% capacity)
- **Cooperate**: Any consumption at this level risks permanent collapse
- This is a "scorched earth" scenario where punishment becomes self-destructive

### Final Round
- **Cooperate if community has been mostly cooperative** (defection rate ≤ 40%)
- **Defect if community has been exploitative** (defection rate > 40%)
- Rationale: Reward good collective behavior even at the end; don't be exploited by persistent defectors

### All Others Defecting
- If defection rate exceeds 70% for 3+ consecutive rounds: **Defect**
- We cannot save a resource alone, but we signal our values through initial cooperation

## Strategy Properties

**Adaptive**: Adjusts tolerance based on resource health
**Forgiving**: Returns to cooperation after punishment if behavior improves
**Protective**: Prioritizes resource survival over punishment
**Clear**: Opens cooperatively to establish norms unambiguously
**Robust**: Handles both cooperative and hostile environments
'''

description_COLLECTIVE_19 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a collective of players sharing the same algorithm. Our primary goal is **sustainable collective wealth maximization** - we recognize that maintaining the resource stock generates more total payoff over time than short-term exploitation. However, we must also be robust against defectors who don't share our values.

## Strategy Overview: "Adaptive Sustainable Harvesting" (ASH)

The strategy operates on three principles:
1. **Sustainability First**: Default to cooperation when the resource can regenerate
2. **Collective Protection**: Respond to widespread defection to prevent exploitation
3. **Endgame Awareness**: Adjust behavior as rounds diminish

---

## Decision Rules

### Primary Decision Framework

```
INPUT: round t, total rounds r, current stock S, capacity C, 
       n players, history of all players' actions

OUTPUT: C (Cooperate) or D (Defect)
```

### Rule 1: First Round
**Action: COOPERATE**

Rationale: Establish cooperative baseline. With stock at capacity, universal cooperation maintains the resource indefinitely while providing steady returns.

### Rule 2: Stock Health Check
Calculate `health_ratio = stock / capacity`

- If `health_ratio < 0.25`: **DEFECT** (resource is critically depleted; extract remaining value)
- If `health_ratio >= 0.25`: Proceed to cooperation analysis

### Rule 3: Cooperation Rate Assessment (Rounds 2+)
Examine the **previous round's** actions across all players:

```
defection_rate = (number of D actions in previous round) / n
```

**Thresholds:**
- If `defection_rate <= 0.3`: **COOPERATE** (cooperation is dominant, maintain it)
- If `defection_rate > 0.3 AND defection_rate <= 0.6`: **PROBABILISTIC** (see Rule 4)
- If `defection_rate > 0.6`: **DEFECT** (cooperation has collapsed, protect self)

### Rule 4: Probabilistic Response (Moderate Defection)
When defection is moderate (30-60%), use a **forgiving tit-for-tat** approach:

```
If defection_rate increased from round (t-2) to (t-1):
    DEFECT with probability = defection_rate
    COOPERATE with probability = 1 - defection_rate
Else (defection stable or decreasing):
    COOPERATE (reward movement toward cooperation)
```

### Rule 5: Endgame Adjustment
Calculate `rounds_remaining = r - t`

```
If rounds_remaining <= 2:
    If defection_rate > 0.4 in recent rounds: DEFECT
    Else: COOPERATE (reward sustained cooperation)
    
If rounds_remaining == 0 (final round):
    If historical_cooperation_rate > 0.7: COOPERATE (solidarity)
    Else: DEFECT (no future to preserve)
```

### Rule 6: Recovery Incentive
If stock dropped significantly but is now recovering (stock increased from previous round) AND previous defection_rate was high:

**COOPERATE** (signal willingness to rebuild)

---

## Complete Decision Pseudocode

```python
def decide(round_t, total_rounds_r, stock_S, capacity_C, n_players, history):
    
    health_ratio = stock_S / capacity_C
    rounds_remaining = total_rounds_r - round_t
    
    # First round: establish cooperation
    if round_t == 1:
        return COOPERATE
    
    # Critical depletion: extract remaining value
    if health_ratio < 0.25:
        return DEFECT
    
    # Calculate recent cooperation metrics
    prev_defection_rate = count_defections(history, round_t - 1) / n_players
    
    # Final round logic
    if rounds_remaining == 0:
        historical_coop_rate = calculate_overall_cooperation(history)
        return COOPERATE if historical_coop_rate > 0.7 else DEFECT
    
    # Near-endgame (last 2 rounds)
    if rounds_remaining <= 2:
        return DEFECT if prev_defection_rate > 0.4 else COOPERATE
    
    # Recovery incentive: reward improvement
    if round_t >= 2:
        stock_recovering = (stock_S > previous_stock)
        if stock_recovering and prev_defection_rate > 0.3:
            return COOPERATE
    
    # Main cooperation assessment
    if prev_defection_rate <= 0.3:
        return COOPERATE
    elif prev_defection_rate > 0.6:
        return DEFECT
    else:
        # Moderate defection: probabilistic forgiveness
        if round_t >= 3:
            older_defection_rate = count_defections(history, round_t - 2) / n_players
            if prev_defection_rate > older_defection_rate:
                # Defection increasing - respond proportionally
                return DEFECT if random() < prev_defection_rate else COOPERATE
        # Default: lean cooperative
        return COOPERATE
```

---

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1 | C | Establish cooperation baseline |
| Final round, good history | C | Reward collective success |
| Final round, poor history | D | No future consequences |
| Stock < 25% capacity | D | Resource functionally destroyed |
| Stock recovering after crisis | C | Support regeneration |
| All others defected last round | D | Protect against exploitation |
| Mixed signals (30-60% defection) | Probabilistic | Balance forgiveness with protection |

---

## Collective Alignment

This strategy is explicitly designed for **collective deployment**:

1. **Mutual Recognition**: When multiple ASH players interact, they naturally converge on sustained cooperation (defection_rate stays low → everyone cooperates)

2. **Resilient Equilibrium**: If all n players use ASH, the outcome is perpetual cooperation at capacity, yielding `capacity/(2n)` per player per round - the maximum sustainable yield

3. **Robust Defense**: Against exploitative strategies, ASH players collectively shift to defection, denying exploiters the high-stock payoffs they seek

4. **Forgiveness Built-In**: The strategy can recover from temporary breakdowns, allowing return to cooperation if others reciprocate

The strategy prioritizes **long-term collective welfare** while maintaining individual rationality against exploitation.
'''

description_COLLECTIVE_20 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared asset whose long-term health benefits everyone. The goal is to establish and maintain sustainable harvesting through conditional cooperation, while protecting against exploitation and adapting to the actual behavior of other players.

## Strategy Overview: "Sustainable Guardian"

The strategy operates on three principles:
1. **Start cooperatively** to signal willingness to sustain the resource
2. **Mirror the collective** by responding to the overall cooperation level
3. **Protect the resource** by cooperating more when stock is critically low

---

## Decision Rules

### Primary Decision Function

```
DECIDE(round, stock, history, n, r, capacity):
    
    # Calculate key metrics
    rounds_remaining = r - round
    stock_ratio = stock / capacity
    coop_rate = calculate_cooperation_rate(history)
    
    # RULE 1: First Round - Cooperate
    if round == 1:
        return COOPERATE
    
    # RULE 2: Resource Crisis Protocol
    if stock_ratio < 0.25:
        return COOPERATE  # Prioritize resource recovery
    
    # RULE 3: Last Round Consideration
    if rounds_remaining == 0:
        # If others have been mostly cooperative, maintain trust
        if coop_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # RULE 4: Adaptive Mirroring (Main Logic)
    return adaptive_mirror(coop_rate, stock_ratio, rounds_remaining, r)
```

### Adaptive Mirroring Function

```
ADAPTIVE_MIRROR(coop_rate, stock_ratio, rounds_remaining, r):
    
    # Threshold adjusts based on game phase and resource health
    base_threshold = 0.5
    
    # Early game: be more forgiving to establish cooperation
    if rounds_remaining > 0.7 * r:
        threshold = base_threshold - 0.15  # Cooperate if ≥35% cooperate
    
    # Mid game: standard reciprocity
    elif rounds_remaining > 0.3 * r:
        threshold = base_threshold  # Cooperate if ≥50% cooperate
    
    # Late game: slightly stricter
    else:
        threshold = base_threshold + 0.1  # Cooperate if ≥60% cooperate
    
    # Resource health bonus: lower threshold when stock is healthy
    if stock_ratio > 0.75:
        threshold -= 0.1
    elif stock_ratio < 0.4:
        threshold -= 0.15  # More willing to cooperate to save resource
    
    # Decision
    if coop_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

### Cooperation Rate Calculation

```
CALCULATE_COOPERATION_RATE(history):
    if history is empty:
        return 1.0  # Assume cooperation initially
    
    # Weight recent rounds more heavily
    total_weight = 0
    weighted_cooperations = 0
    
    for each round t in history (most recent first):
        recency_weight = 0.8^(current_round - t - 1)  # Exponential decay
        cooperators_in_round = count(players who played C in round t)
        total_players = n
        
        weighted_cooperations += recency_weight * (cooperators_in_round / total_players)
        total_weight += recency_weight
    
    return weighted_cooperations / total_weight
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Signal cooperative intent, no history to judge |
| **Last round** | Cooperate if coop_rate ≥ 0.6, else Defect | Reward sustained cooperation, don't be exploited |
| **Stock < 25% capacity** | Cooperate | Resource survival trumps short-term gain |
| **Stock = 0** | Cooperate | Nothing to gain from defection anyway; signal for recovery |
| **All others defected last round** | Defect (unless crisis) | Don't be a lone sucker |
| **Perfect cooperation history** | Cooperate | Maintain the virtuous cycle |

---

## Why This Strategy is Collectively Aligned

1. **Sustainability Focus**: By cooperating when stock is low, we prioritize resource recovery over individual gain—this benefits everyone long-term.

2. **Forgiveness Built In**: The recency-weighted cooperation rate means past defections fade, allowing groups to recover from coordination failures.

3. **Not Exploitable**: By mirroring aggregate behavior, we don't allow systematic exploitation by defectors while still rewarding cooperation.

4. **Adaptive Thresholds**: Being more forgiving early and when resources are healthy encourages cooperation to emerge and persist.

5. **Crisis Protocol**: The 25% stock threshold creates a collective "emergency brake" that can prevent complete resource collapse.

---

## Expected Behavior in Different Populations

- **Against all cooperators**: Sustains cooperation, maximizes collective payoff
- **Against all defectors**: Defects after round 1 (except in crisis), minimizes exploitation
- **Against mixed strategies**: Gravitates toward majority behavior while protecting resources
- **Against itself**: Achieves sustained cooperation and resource maintenance
'''

description_COLLECTIVE_21 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared commons where **collective restraint creates collective wealth**. The goal is to maximize long-term total payoffs by maintaining sustainable stock levels, while being robust against exploitation.

## Key Insight

When all players cooperate, the stock remains at capacity indefinitely (as shown in Example 1). When all defect, the resource collapses immediately. The sustainable equilibrium requires collective cooperation, but we must protect against defectors who would exploit cooperators.

## Strategy: "Sustainable Commons Guardian"

### Decision Rules

**Default Stance: Cooperate (C)**

The strategy starts cooperative and remains cooperative as long as the resource system appears healthy and sustainable.

**Switch to Defect (D) under these conditions:**

1. **Stock Collapse Trigger**: If `stock < capacity * 0.3`, defect to extract remaining value before total collapse

2. **Exploitation Detection**: If in the previous round, the number of defectors exceeded `n/2`, defect in response (the commons is being exploited)

3. **End-Game Protection**: In the final round (`round == r`), defect (no future to protect)

4. **Near-End Threshold**: In the final 2 rounds, defect if any defection was observed in the preceding round (prevents late-game exploitation)

**Return to Cooperation:**

After defecting due to exploitation detection, return to cooperation if:
- The previous round showed majority cooperation (≤ `n/2` defectors), AND
- Stock remains above `capacity * 0.4`

### Pseudocode

```
function decide(round, stock, history, n, r, capacity):
    
    # Last round: always defect (no future consequences)
    if round == r:
        return DEFECT
    
    # Resource critically depleted: extract what remains
    if stock < capacity * 0.3:
        return DEFECT
    
    # First round: cooperate to establish norm
    if round == 1:
        return COOPERATE
    
    # Near end-game (last 2 rounds): defect if any recent defection
    if round >= r - 1:
        defectors_last_round = count_defectors(history, round - 1)
        if defectors_last_round > 0:
            return DEFECT
    
    # Count defectors in previous round
    defectors_last_round = count_defectors(history, round - 1)
    
    # Majority defected: respond with defection
    if defectors_last_round > n / 2:
        return DEFECT
    
    # Stock recovering and majority cooperated: cooperate
    if stock >= capacity * 0.4 and defectors_last_round <= n / 2:
        return COOPERATE
    
    # Default: cooperate
    return COOPERATE
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative norm, signal intent |
| Last round | Defect | No future rounds to protect |
| Stock < 30% capacity | Defect | Resource likely doomed; extract value |
| Majority defected last round | Defect | Protect against exploitation |
| Stock healthy + majority cooperated | Cooperate | Maintain sustainable equilibrium |
| 2-player game | More forgiving threshold | Single defector = 50%, use stricter majority rule |

### Collective Alignment

This strategy embodies collective thinking by:

1. **Starting cooperative**: Gives the collective a chance to establish sustainable harvesting
2. **Forgiving**: Returns to cooperation when conditions improve, not permanently punitive
3. **Threshold-based**: Doesn't overreact to a single defector; responds to systemic breakdown
4. **Resource-aware**: Prioritizes stock health as the collective's shared interest
5. **Proportional response**: Only defects when cooperation would clearly be exploited

### Why This Works Against Various Opponents

- **Against all-cooperators**: Mutual cooperation maintains full stock, maximizing everyone's payoff
- **Against all-defectors**: Quick detection limits exploitation losses
- **Against mixed strategies**: Responds proportionally, doesn't collapse cooperation prematurely
- **Against tit-for-tat variants**: Compatible; maintains cooperation cycles
- **Against exploiters**: Defection threshold prevents sustained exploitation
'''

description_COLLECTIVE_22 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable cooperation maximizes total welfare across all players and rounds. However, we must be adaptive since we cannot assume others share this perspective. The strategy uses **conditional cooperation with forgiveness** - we default to cooperation but protect the resource from collapse when others defect excessively.

## Strategy Name: "Guardian Threshold"

### Key Insight

The game has a critical property: when all cooperate, the stock regenerates fully (consumption = growth at capacity). When defection increases, stock depletes, hurting *everyone's* future payoffs. A collective strategy should:
1. Model sustainable behavior for others to follow
2. Protect the commons from catastrophic depletion
3. Forgive occasional defections to allow recovery

---

## Decision Rules

### Primary Rule: Cooperation Rate Threshold

**Cooperate if** the recent cooperation rate among all players (including self) meets a sustainability threshold; **Defect otherwise** as a protective/signaling measure.

```
cooperation_threshold = 0.5 + (stock / capacity) * 0.25
```

This threshold is:
- **Lower when stock is depleted** (0.5 at stock=0): more forgiving to allow recovery
- **Higher when stock is healthy** (0.75 at full capacity): maintain high standards

### Decision Function

```
function decide(round, stock, capacity, n, history):
    
    # FIRST ROUND: Always cooperate (establish good faith)
    if round == 1:
        return COOPERATE
    
    # LAST ROUND: Cooperate if stock is critically low OR cooperation has been high
    if round == r:
        recent_coop_rate = calculate_cooperation_rate(history, lookback=3)
        if recent_coop_rate >= 0.6 OR stock < capacity * 0.3:
            return COOPERATE  # Maintain collective benefit / don't kill dying resource
        else:
            return DEFECT  # Others already defecting, no future to protect
    
    # STOCK EMERGENCY: If stock critically low, cooperate to allow recovery
    if stock < capacity * 0.15:
        return COOPERATE
    
    # STANDARD ROUNDS: Conditional cooperation based on threshold
    lookback = min(3, round - 1)
    recent_coop_rate = calculate_cooperation_rate(history, lookback)
    threshold = 0.5 + (stock / capacity) * 0.25
    
    if recent_coop_rate >= threshold:
        return COOPERATE
    else:
        # Graduated response: defect but with probability of forgiveness
        forgiveness_prob = 0.2 * (stock / capacity)
        if random() < forgiveness_prob:
            return COOPERATE  # Occasional forgiveness to test recovery
        return DEFECT

function calculate_cooperation_rate(history, lookback):
    # Count C vs D across all players in last 'lookback' rounds
    total_actions = 0
    total_cooperations = 0
    for each of last 'lookback' rounds:
        for each player's action:
            total_actions += 1
            if action == C:
                total_cooperations += 1
    return total_cooperations / total_actions
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | COOPERATE | Establish cooperative norm; no history to judge |
| **Last round** | Conditional | Cooperate if group has been cooperative (reward) or stock is critical (mercy) |
| **Stock < 15% capacity** | COOPERATE | Emergency conservation; defecting a dying resource helps no one |
| **Stock at capacity, high cooperation** | COOPERATE | Sustainable equilibrium achieved |
| **Sustained defection (>50%)** | DEFECT | Protect self; signal that exploitation has consequences |
| **Mixed history** | Use threshold | Adaptive response based on current sustainability |

---

## Why This Strategy is Collectively Optimal

1. **Sustainability-focused**: Prioritizes keeping stock regenerating over short-term gains
2. **Forgiveness built-in**: Random forgiveness allows groups to recover from defection spirals
3. **Adaptive threshold**: Standards adjust to current resource health
4. **Emergency protection**: Never accelerates collapse of critical stock
5. **Clear signaling**: Defection responses signal that exploitation won't be tolerated indefinitely
6. **Self-consistent**: If all players use this strategy, they maintain full cooperation and maximum sustainable yield
'''

description_COLLECTIVE_23 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across generations (rounds). The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the resource regenerates fully, enabling maximum long-term collective payoff. Any defection triggers resource depletion that harms everyone, including the defector, in subsequent rounds.

## Strategy Name: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to signal collective intent
2. **Protect the resource** when it's threatened
3. **Forgive strategically** to enable recovery

### Decision Rules

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- capacity: maximum sustainable stock
- n: number of players
- history: list of (my_action, others_actions, stock_after) for each past round

COMPUTE:
- rounds_remaining = r - round + 1
- stock_ratio = stock / capacity
- defection_rate = proportion of opponent defections in last 3 rounds (or available history)
- recent_trend = whether defection_rate is increasing, stable, or decreasing

DECISION LOGIC:

1. FIRST ROUND:
   → COOPERATE (establish cooperative norm)

2. LAST ROUND:
   IF stock_ratio < 0.3:
      → COOPERATE (resource is fragile, don't destroy it)
   ELSE IF defection_rate > 0.5 in final rounds:
      → DEFECT (others aren't protecting it anyway)
   ELSE:
      → COOPERATE (maintain collective outcome)

3. RESOURCE EMERGENCY (stock_ratio < 0.25):
   → COOPERATE (prioritize resource survival over punishment)

4. HEALTHY RESOURCE (stock_ratio ≥ 0.7):
   IF defection_rate == 0 in last 2 rounds:
      → COOPERATE (reward collective restraint)
   ELSE IF defection_rate > 0.3:
      → DEFECT (proportional response to exploitation)
   ELSE:
      → COOPERATE (tolerate minor defection)

5. STRESSED RESOURCE (0.25 ≤ stock_ratio < 0.7):
   IF defection_rate > 0.2:
      → COOPERATE (don't accelerate collapse)
   ELSE:
      → COOPERATE (help recovery)

6. GRADUATED RESPONSE OVERRIDE:
   IF consecutive_rounds_all_cooperated ≥ 2:
      → COOPERATE (locked into cooperative equilibrium)
   IF consecutive_rounds_of_majority_defection ≥ 3 AND stock_ratio > 0.5:
      → DEFECT (environment is hostile, extract value before collapse)
```

### Key Mechanisms

**1. Asymmetric Response Based on Resource State**
- When resources are healthy, we can afford to "punish" defectors with reciprocal defection
- When resources are stressed, we prioritize conservation over punishment (defecting would hurt us too)

**2. Forgiveness Window**
- After any defection (ours or others'), we return to cooperation if:
  - The resource shows recovery (stock increasing)
  - Defection rate drops below threshold
  - This enables escape from punishment spirals

**3. Collective Mindset Signaling**
- Early consistent cooperation signals we're a "guardian" type
- Other guardians will recognize this and maintain cooperation
- Exploiters will be identified by their defection patterns

**4. End-Game Protection**
- Unlike standard repeated games, we don't unravel cooperation at the end
- The resource has intrinsic value; destroying it helps no one
- Only defect in final round if others have already abandoned cooperation

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish norm |
| Only player cooperating | C (if stock < 50%), D (otherwise) | Don't be exploited when resource is healthy |
| Stock near zero | C | Any defection could collapse the resource entirely |
| Perfect cooperation history | C | Never break a working equilibrium |
| Erratic opponents | C | Default to protection; chaos isn't strategic |

### Why This Works Collectively

If all players adopt this strategy:
- Universal cooperation emerges from round 1
- Stock remains at capacity throughout
- Each player earns `capacity/(2n)` per round
- Total collective payoff is maximized

Against mixed populations:
- Cooperators form a protective coalition
- Defectors trigger graduated responses but don't cause collapse
- Resource preservation benefits everyone in later rounds
'''

description_COLLECTIVE_24 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across generations (rounds). The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock maintains itself at capacity indefinitely, providing stable returns to everyone. Any defection triggers a tragedy of the commons that ultimately harms all players, including defectors.

## Strategy Name: "Generous Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to maintain the sustainable equilibrium
2. **Protect the commons** by responding to defection, but not vindictively
3. **Forgive quickly** to restore cooperation when possible

### Decision Rules

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- capacity: maximum sustainable stock
- n: number of players
- history: list of (my_action, all_actions, stock_before, stock_after) for each past round

DECISION LOGIC:

1. FIRST ROUND:
   → COOPERATE (establish cooperative norm)

2. LAST ROUND (round == r):
   → COOPERATE (collective commitment to stewardship, even at the end)

3. RESOURCE CRISIS (stock < capacity * 0.3):
   → COOPERATE (emergency conservation mode - the commons needs healing)

4. STANDARD ROUNDS:
   
   a) Count defectors in previous round:
      defector_count = number of D plays in last round
      defection_rate = defector_count / n
   
   b) Calculate stock health:
      stock_ratio = stock / capacity
   
   c) Decision matrix:
      
      IF defection_rate == 0:
         → COOPERATE (maintain the good equilibrium)
      
      ELIF defection_rate < 0.5 AND stock_ratio > 0.6:
         → COOPERATE (give benefit of doubt, stock is healthy)
      
      ELIF defection_rate >= 0.5 AND stock_ratio > 0.5:
         → DEFECT (proportional response - others are exploiting)
         BUT: Return to COOPERATE after 1 round of defection
      
      ELIF stock_ratio <= 0.5:
         → COOPERATE (prioritize resource recovery over punishment)
```

### Forgiveness Mechanism

```
forgiveness_counter: tracks rounds since last defection response

IF I defected last round as punishment:
   forgiveness_counter = 1
   → COOPERATE this round (offer olive branch)

IF forgiveness_counter > 0 AND others still defecting:
   IF defection_rate decreased:
      → COOPERATE (reward improvement)
   ELSE:
      → DEFECT (they haven't learned)
      forgiveness_counter += 1
      
   IF forgiveness_counter >= 3:
      → COOPERATE anyway (reset cycle, try again)
      forgiveness_counter = 0
```

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative norm |
| Round r (final) | C | Collective values don't disappear at the end |
| Stock near zero | C | Conservation is critical; defection kills the commons |
| Stock at capacity, all cooperated | C | Perfect state - maintain it |
| Single defector appeared | C | Could be noise; don't overreact |
| Majority defecting | D (once) | Signal that exploitation won't be tolerated |
| After my punishment defection | C | Offer path back to cooperation |
| Prolonged defection by others | C | Eventually reset; endless punishment destroys everything |

### Why This Strategy is Collectively Optimal

1. **Sustainability**: Universal cooperation maintains stock at capacity forever, yielding `capacity/(2n)` per player per round indefinitely.

2. **Robustness**: The strategy doesn't collapse into permanent defection spirals. It always returns to cooperation, giving the collective repeated chances to find the good equilibrium.

3. **Signal Clarity**: By defecting only briefly and returning to cooperation, the strategy communicates "I prefer cooperation, but won't be exploited indefinitely."

4. **Crisis Response**: When stock is low, cooperation becomes even more important than punishment. The strategy prioritizes healing the commons.

5. **End-game integrity**: Defecting in the final round is a betrayal of collective values. This strategy maintains its principles throughout.

### Expected Behavior in Tournament

- Against other cooperators: Mutual cooperation, maximum collective welfare
- Against pure defectors: Brief punishment, then attempted rehabilitation
- Against tit-for-tat variants: Stable cooperation after initial coordination
- Against exploitative strategies: Limits damage while preserving recovery potential
'''

description_COLLECTIVE_25 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The key insight is that universal cooperation maintains the stock at capacity indefinitely (as shown in Example 1), while defection depletes the resource. However, we must also be robust against defectors.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperative** to signal collective intent and test the waters
2. **Protect the commons** by responding proportionally to defection
3. **Forgive strategically** to allow recovery when possible

### Decision Rules

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- history: list of (my_action, observed_total_consumption) per past round
- n: number of players
- r: total rounds
- capacity: maximum stock

COMPUTE:
- rounds_remaining = r - round + 1
- stock_ratio = stock / capacity
- expected_coop_consumption = stock / 2  (if all cooperate)

INFER DEFECTION LEVEL (from previous round):
If round > 1:
    last_consumption = history[round-1].total_consumption
    last_stock = (stock from previous round start)
    # Expected consumption if all cooperated: last_stock / 2
    # Expected consumption if all defected: last_stock
    # Estimate number of defectors from consumption level
    defection_ratio = (last_consumption - last_stock/2) / (last_stock/2)
    defection_ratio = clamp(defection_ratio, 0, 1)
```

### Core Decision Logic

```
DECIDE ACTION:

# Rule 1: First Round - Always Cooperate
IF round == 1:
    RETURN C

# Rule 2: Last Round Consideration
IF round == r:
    # If stock is critically low, defection causes total collapse anyway
    # If others have been cooperative, maintain cooperation for collective benefit
    IF defection_ratio < 0.3:
        RETURN C
    ELSE:
        RETURN D

# Rule 3: Stock Emergency - Protect the Commons
IF stock_ratio < 0.25:
    # Resource is critically depleted - cooperate to allow recovery
    # Even if others defect, defecting on a depleted stock gains little
    RETURN C

# Rule 4: Graduated Response to Defection
IF defection_ratio < 0.2:
    # Mostly cooperative environment - maintain cooperation
    RETURN C
    
ELSE IF defection_ratio < 0.5:
    # Moderate defection - respond with probabilistic defection
    # This signals displeasure while allowing recovery
    IF random() < defection_ratio:
        RETURN D
    ELSE:
        RETURN C
        
ELSE:
    # Majority defecting - match their behavior but leave room for recovery
    # Cooperate occasionally to test if others return to cooperation
    IF random() < 0.2 OR (round % 3 == 0):
        RETURN C
    ELSE:
        RETURN D

# Rule 5: Forgiveness - Return to Cooperation After Sustained Peace
IF last 2 rounds had defection_ratio < 0.2:
    RETURN C
```

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline; no information yet |
| Last round, cooperative history | C | Collective benefit; reputation for future tournaments |
| Last round, defection history | D | No future to protect; defectors won't change |
| Stock near zero | C | Defecting gains almost nothing; only cooperation allows recovery |
| Stock at capacity after defection | C | Test if others learned; resource can absorb one more test |
| All previous rounds saw defection | Mostly D with occasional C | Protect self while probing for change |

### Why This Strategy is Collectively Optimal

1. **If everyone uses this strategy**: All players cooperate every round, stock remains at capacity, everyone earns capacity/(2n) per round = maximum sustainable yield.

2. **Against pure defectors**: Gradually matches defection to avoid being exploited, while occasional cooperation tests for reform.

3. **Against mixed strategies**: Proportional response discourages defection without triggering destructive spirals.

4. **Stock-aware**: Prioritizes resource survival over short-term punishment, recognizing that a depleted commons hurts everyone.
'''

description_COLLECTIVE_26 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable cooperation maximizes total welfare across all players and rounds. However, we must be adaptive since we cannot assume others share this perspective. The strategy aims to:

1. **Signal cooperative intent** early
2. **Sustain the resource** for long-term collective benefit
3. **Protect against exploitation** without being overly punitive
4. **Forgive and re-establish cooperation** when possible

---

## Strategy: "Sustainable Guardian"

### Decision Framework

The strategy uses three key metrics evaluated each round:

1. **Stock Health Ratio**: `current_stock / capacity`
2. **Cooperation Rate**: Fraction of players who cooperated in the previous round
3. **Round Position**: `current_round / total_rounds`

---

### Decision Rules

#### Round 1: Always Cooperate
- **Rationale**: Establish cooperative intent, preserve stock, gather information about opponents.

#### Rounds 2 through (r-1): Conditional Cooperation

**Cooperate if ANY of these conditions hold:**

1. **High Cooperation Environment**: 
   - At least `(n-1)/n` of other players cooperated last round (i.e., at most 1 defector)
   
2. **Resource Crisis Response**:
   - `stock_health_ratio < 0.4` (resource is critically depleted)
   - *Rationale*: When stock is low, even self-interested players benefit from letting it recover
   
3. **Forgiveness Window**:
   - Previous round had defection, BUT the round before that had ≥50% cooperation
   - AND `stock_health_ratio > 0.3`
   - *Rationale*: Allow recovery from temporary breakdowns

**Defect if ALL of these conditions hold:**

1. More than 1 player defected in the previous round
2. Stock is not critically low (`stock_health_ratio ≥ 0.4`)
3. Not in a forgiveness window

#### Final Round (Round r): Conditional Defection

- **Cooperate if**: `stock_health_ratio < 0.25` OR cooperation rate in round (r-1) was 100%
- **Defect otherwise**
- *Rationale*: No future rounds to protect, but maintain cooperation if group has been fully aligned

---

### Pseudocode

```
function decide(round, total_rounds, current_stock, capacity, history):
    stock_health = current_stock / capacity
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate cooperation metrics from history
    last_round_coop_rate = count_cooperators(history[round-1]) / n
    defectors_last_round = n - count_cooperators(history[round-1])
    
    # Final round logic
    if round == total_rounds:
        if stock_health < 0.25 OR last_round_coop_rate == 1.0:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds logic
    
    # Condition 1: High cooperation environment
    if defectors_last_round <= 1:
        return COOPERATE
    
    # Condition 2: Resource crisis
    if stock_health < 0.4:
        return COOPERATE
    
    # Condition 3: Forgiveness window
    if round >= 3:
        two_rounds_ago_coop_rate = count_cooperators(history[round-2]) / n
        if two_rounds_ago_coop_rate >= 0.5 AND stock_health > 0.3:
            return COOPERATE
    
    # Default: Defect (respond to sustained defection)
    return DEFECT
```

---

### Edge Cases

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | Cooperate | Build trust, gather information |
| All opponents defected last round | Defect (unless crisis) | Protect self from exploitation |
| Stock near zero | Cooperate | Recovery benefits everyone |
| Single defector | Cooperate | Maintain cooperation with majority |
| Last round, full prior cooperation | Cooperate | Reward sustained collective behavior |
| Last round, prior defections | Defect | No future to protect |

---

### Why This Strategy is Collectively Optimal

1. **Sustainability Focus**: Prioritizes keeping stock above regeneration thresholds
2. **Graduated Response**: Tolerates isolated defection, only retaliates against widespread exploitation
3. **Crisis Solidarity**: Shifts to unconditional cooperation when resource is threatened
4. **Forgiveness**: Prevents permanent breakdown spirals
5. **Clear Signals**: Consistent behavior makes intentions legible to adaptive opponents
'''

description_COLLECTIVE_27 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock remains at capacity indefinitely, yielding consistent payoffs. Any defection creates a tragedy of the commons spiral.

The strategy prioritizes **collective sustainability over individual maximization**, while including protective mechanisms against exploitation.

## Strategy Name: "Guardian of the Commons"

---

## Decision Rules

### Primary Decision Framework

```
DECIDE(game_params, state, history):
    
    n = number of players
    r = total rounds
    t = current round (1-indexed)
    S = current stock
    capacity = maximum sustainable stock
    
    # Calculate key metrics
    sustainability_ratio = S / capacity
    rounds_remaining = r - t + 1
    
    # Analyze history if available
    if t > 1:
        defection_rate = count_defections(history) / (n * (t - 1))
        recent_defections = count_defections(last_round(history))
        stock_trend = calculate_stock_trend(history)
    else:
        defection_rate = 0
        recent_defections = 0
        stock_trend = 0
    
    # DECISION LOGIC
    return COOPERATE if should_cooperate(...) else DEFECT
```

### Detailed Decision Rules

#### Rule 1: First Round - Signal Cooperation
**Action: COOPERATE**

Rationale: Establish cooperative intent. The first round sets the tone for the entire game. By cooperating, we demonstrate commitment to sustainability and give others the opportunity to recognize mutual benefit.

#### Rule 2: Stock Crisis Response
**Condition:** `sustainability_ratio < 0.25`
**Action: COOPERATE**

Rationale: When the resource is critically depleted, defection accelerates collapse toward zero payoffs for everyone. Even if others defect, cooperative restraint gives the stock a chance to recover. At very low stock levels, even defection yields minimal absolute payoffs.

#### Rule 3: Healthy Stock with Cooperative History
**Condition:** `sustainability_ratio >= 0.5 AND defection_rate < 0.2`
**Action: COOPERATE**

Rationale: When the system is working well, maintain it. This rewards collective good behavior and sustains the regenerative cycle.

#### Rule 4: Graduated Response to Defection
**Condition:** `defection_rate >= 0.2 AND defection_rate < 0.5`
**Action: COOPERATE with probability `1 - defection_rate`**

Rationale: Respond proportionally to observed defection. This creates a signal that defection has consequences while maintaining hope for return to cooperation. The probabilistic element prevents deterministic exploitation.

#### Rule 5: Systemic Defection Environment
**Condition:** `defection_rate >= 0.5 AND sustainability_ratio > 0.3`
**Action: DEFECT**

Rationale: When a majority defects consistently, pure cooperation becomes exploitation of the cooperative player. Matching defection prevents being a "sucker" while the remaining stock is depleted by others anyway.

#### Rule 6: Final Round Consideration
**Condition:** `t == r` (last round)
**Action: Based on overall cooperation history**
- If `defection_rate < 0.3` throughout game: **COOPERATE** (honor the cooperative relationship)
- Otherwise: **DEFECT** (no future rounds to preserve stock for)

#### Rule 7: Recovery Detection
**Condition:** `stock_trend > 0 AND recent_defections == 0`
**Action: COOPERATE**

Rationale: If the group appears to be recovering cooperation (stock rising, no recent defections), support the recovery by cooperating.

---

## Complete Decision Algorithm

```
GUARDIAN_OF_COMMONS(n, r, capacity, current_stock, history):
    
    t = len(history) + 1  # Current round
    S = current_stock
    sustainability = S / capacity
    
    # === FIRST ROUND ===
    if t == 1:
        return COOPERATE
    
    # === CALCULATE HISTORY METRICS ===
    total_actions = n * (t - 1)
    total_defections = sum(count_defections(round) for round in history)
    defection_rate = total_defections / total_actions
    
    last_round_defections = count_defections(history[-1])
    last_round_defection_rate = last_round_defections / n
    
    # === CRISIS MODE: Protect depleted resource ===
    if sustainability < 0.25:
        return COOPERATE
    
    # === FINAL ROUND ===
    if t == r:
        if defection_rate < 0.3:
            return COOPERATE  # Honor cooperative history
        else:
            return DEFECT  # No future to protect
    
    # === RECOVERY SUPPORT ===
    if t >= 3:
        prev_stock = get_stock_at_round(history, t-2)
        if current_stock > prev_stock AND last_round_defections == 0:
            return COOPERATE
    
    # === MAIN DECISION LOGIC ===
    
    # Highly cooperative environment
    if defection_rate < 0.15:
        return COOPERATE
    
    # Moderate defection - probabilistic response
    if defection_rate < 0.4:
        cooperation_probability = 1 - defection_rate
        return COOPERATE with probability cooperation_probability
    
    # High defection environment
    if defection_rate >= 0.4:
        # Still cooperate if stock is critical
        if sustainability < 0.4:
            return COOPERATE
        # Otherwise match the prevailing behavior
        return DEFECT
    
    # Default: Cooperate
    return COOPERATE
```

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | COOPERATE | Signal cooperative intent |
| Last round, cooperative history | COOPERATE | Maintain integrity, honor cooperation |
| Last round, defection history | DEFECT | No future to protect |
| Stock near zero | COOPERATE | Defection gains minimal; recovery possible |
| Stock at capacity, first defection seen | COOPERATE | One deviation may be noise; maintain cooperation |
| Consistent 50%+ defection rate | DEFECT (if stock permits) | Avoid pure exploitation |
| Stock recovering after crisis | COOPERATE | Support collective recovery |

---

## Why This Strategy is Collectively Optimal

1. **Sustainability First**: Universal cooperation maintains stock at capacity forever, maximizing total payoffs across all rounds.

2. **Forgiveness**: The graduated response allows return to cooperation, unlike pure tit-for-tat which can lock in mutual defection.

3. **Crisis Protection**: Cooperating during stock crises prevents complete collapse, preserving future value for everyone.

4. **Exploitation Resistance**: The defection threshold prevents being indefinitely exploited by persistent defectors.

5. **Collective Signaling**: Early cooperation establishes norms; responding to defection proportionally signals consequences without destroying cooperation.

This strategy embodies the principle: **"Protect the commons first, then protect yourself from exploitation, but always leave room for redemption."**
'''

description_COLLECTIVE_28 = '''
# Collective Strategy: "Sustainable Harvest Protocol"

## Core Philosophy

This strategy treats the common pool as a shared long-term asset. The fundamental insight is that universal cooperation maintains the resource at capacity indefinitely (yielding stock/(2n) per player per round forever), while defection offers short-term gains but destroys future value. My goal is to cooperate when it's collectively sustainable and defect only when the resource is already compromised beyond recovery or when it's the final round.

## Decision Rules

### Primary Decision Framework

```
function decide(round, total_rounds, current_stock, capacity, n, history):
    
    # Rule 1: Last Round Defection
    if round == total_rounds:
        return DEFECT
    
    # Rule 2: Resource Collapse Detection
    if current_stock < capacity / (2 * n):
        return DEFECT  # Resource too depleted to sustain cooperation
    
    # Rule 3: First Round Cooperation
    if round == 1:
        return COOPERATE
    
    # Rule 4: Conditional Cooperation Based on History
    recent_defection_rate = calculate_defection_rate(history, lookback=3)
    stock_health = current_stock / capacity
    
    # Rule 4a: Healthy stock + mostly cooperative history
    if stock_health >= 0.5 and recent_defection_rate <= 0.25:
        return COOPERATE
    
    # Rule 4b: Declining stock but recoverable
    if stock_health >= 0.25 and recent_defection_rate <= 0.5:
        return COOPERATE  # Give cooperation a chance to restore
    
    # Rule 4c: Stock declining due to widespread defection
    if stock_health < 0.5 and recent_defection_rate > 0.5:
        return DEFECT  # Join defection to not be exploited
    
    # Rule 5: Default to cooperation when uncertain
    return COOPERATE
```

## Detailed Decision Rules

### 1. **Last Round Rule**
- **Action:** Always DEFECT on the final round
- **Rationale:** No future rounds exist to benefit from stock preservation; this is the dominant strategy regardless of others' choices

### 2. **Resource Collapse Rule**
- **Condition:** `current_stock < capacity / (2n)`
- **Action:** DEFECT
- **Rationale:** When stock is critically low, even universal cooperation yields negligible payoffs. Better to extract what remains.

### 3. **Opening Move Rule**
- **Condition:** Round 1
- **Action:** COOPERATE
- **Rationale:** Signals cooperative intent; at full capacity, cooperation is sustainable and establishes trust

### 4. **Adaptive Response Rules**

Calculate from history:
- `recent_defection_rate`: Proportion of DEFECT actions observed in the last min(3, rounds_played) rounds across all observable players
- `stock_health`: current_stock / capacity

| Stock Health | Defection Rate | Action | Reasoning |
|--------------|----------------|--------|-----------|
| ≥ 50% | ≤ 25% | COOPERATE | System healthy, maintain it |
| ≥ 25% | ≤ 50% | COOPERATE | Still recoverable, encourage cooperation |
| < 50% | > 50% | DEFECT | Being exploited, protect self |
| < 25% | > 25% | DEFECT | Approaching collapse, extract value |
| ≥ 50% | > 25% but ≤ 50% | COOPERATE | Stock resilient, try to restore cooperation |

### 5. **Default Rule**
- When conditions are ambiguous, COOPERATE
- **Rationale:** Cooperation preserves optionality and supports collective welfare

## Edge Cases

1. **n = 2 (minimum players):** Strategy works unchanged; defection detection is precise
2. **r = 2 (minimum rounds):** Cooperate round 1, defect round 2
3. **Stock at exactly capacity:** Strong cooperation signal; follow standard rules
4. **All previous rounds saw defection:** Defect (recent_defection_rate = 1.0 > 0.5)
5. **Stock miraculously recovers after collapse:** Resume cooperation if stock_health criteria met

## Why This Strategy is Collectively Aligned

- **Prioritizes sustainability:** Defaults to cooperation when resource is healthy
- **Forgives:** Doesn't permanently punish; re-evaluates each round based on recent behavior
- **Protects the commons:** Only defects when resource is already failing or exploitation is rampant
- **Realistic about endgame:** Acknowledges last-round incentives while maximizing cooperative rounds
'''

description_COLLECTIVE_29 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The strategy balances cooperation to maintain the resource with adaptive responses to detected defection, while recognizing that in a tournament of independent AI strategies, others may have similar cooperative inclinations.

## Strategy Overview: "Sustainable Threshold Guardian"

The strategy operates on three principles:
1. **Preserve the resource** - Cooperate when the stock is healthy to ensure long-term gains
2. **Respond to crisis** - Adapt behavior based on stock health, not just opponent actions
3. **Forgive and restore** - After defection (by self or others), return to cooperation when sustainable

---

## Decision Rules

### Primary Decision Variables
- `stock`: Current stock level
- `capacity`: Maximum sustainable stock
- `n`: Number of players
- `r`: Total rounds
- `t`: Current round (1-indexed)
- `history`: Record of stock levels after each round

### Stock Health Threshold
```
healthy_threshold = capacity * 0.5
critical_threshold = capacity * 0.25
```

### Core Decision Logic

```
FUNCTION decide(stock, capacity, n, r, t, history):
    
    # Calculate key metrics
    healthy_threshold = capacity * 0.5
    critical_threshold = capacity * 0.25
    rounds_remaining = r - t
    
    # RULE 1: First Round - Establish Cooperation
    IF t == 1:
        RETURN Cooperate
    
    # RULE 2: Last Round Consideration
    IF rounds_remaining == 0:
        # If stock is critical, defecting gains little and signals poorly
        # Cooperate to maximize from whatever remains (collective benefit)
        IF stock <= critical_threshold:
            RETURN Cooperate
        # If stock is healthy, one defection won't destroy it
        # But collectively, if everyone defects, we lose everything
        # Stay cooperative - we're designing for collective adoption
        RETURN Cooperate
    
    # RULE 3: Critical Stock Emergency
    IF stock <= critical_threshold:
        # Resource is in danger - must cooperate to allow recovery
        RETURN Cooperate
    
    # RULE 4: Detect Resource Decline Pattern
    IF len(history) >= 2:
        recent_decline = history[-2] - history[-1]  # Stock drop last round
        expected_if_all_cooperate = 0  # Stock should be stable/growing
        
        # If stock dropped significantly, others are defecting
        IF recent_decline > capacity * 0.1:
            # Stock is still healthy enough - continue cooperating
            # to demonstrate sustainable behavior and allow recovery
            IF stock > healthy_threshold:
                RETURN Cooperate
            # Stock declining toward danger - critical cooperation needed
            ELSE:
                RETURN Cooperate
    
    # RULE 5: Healthy Stock Default
    IF stock >= healthy_threshold:
        RETURN Cooperate
    
    # RULE 6: Moderate Stock - Proportional Response
    # Stock between critical and healthy thresholds
    # Probability of cooperation scales with stock health
    cooperation_probability = (stock - critical_threshold) / (healthy_threshold - critical_threshold)
    
    # Use deterministic threshold based on round number for reproducibility
    # This creates a predictable pattern other similar strategies can match
    threshold = (t % 10) / 10
    IF cooperation_probability > threshold:
        RETURN Cooperate
    ELSE:
        RETURN Defect
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline; no information yet |
| **Last round** | Cooperate | Collective strategy - if all defect, resource collapses for minimal gain |
| **Stock ≤ 25% capacity** | Cooperate | Emergency preservation mode |
| **Stock at capacity** | Cooperate | Maintain the sustainable equilibrium |
| **Stock depleted to 0** | Cooperate | Taking 0/n = 0 anyway; cooperation signals intent for recovery |
| **Only 2 rounds left** | Follow standard rules | Don't trigger endgame defection spiral |

---

## Why This Strategy is Collectively Optimal

1. **If all players use this strategy**: Everyone cooperates, stock remains at capacity, each player earns `capacity/(2n)` every round = `r × capacity/(2n)` total.

2. **Self-sustaining equilibrium**: With all cooperating, stock dynamics show: consume 50%, regenerate 50%, stock stays at capacity.

3. **Robust to some defectors**: Even if some opponents defect, maintaining cooperation preserves enough stock for meaningful future rounds.

4. **No retaliation spirals**: Unlike tit-for-tat, this strategy doesn't punish defection with defection (which would accelerate resource collapse). Instead, it maintains cooperation to preserve the collective good.

---

## Summary

**Cooperate always, except in the narrow band between critical and healthy stock levels, where behavior becomes probabilistically cautious based on round timing.**

This strategy maximizes collective long-term payoff and is designed so that a population of identical players achieves the Pareto-optimal sustainable outcome.
'''

description_COLLECTIVE_30 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that sustainable collective welfare requires maintaining the resource stock near its maximum regeneration point. The key insight is that when stock equals capacity/2, regeneration is maximized. Universal cooperation at full capacity creates a sustainable equilibrium where everyone earns well indefinitely. However, we must be robust to defectors who threaten this sustainability.

## Strategy Overview: "Sustainable Guardian"

The strategy operates on three principles:
1. **Start cooperatively** to establish sustainable norms
2. **Protect the resource** by matching aggregate defection levels
3. **Forgive strategically** to allow recovery when others show cooperative intent

---

## Decision Rules

### Round 1: Cooperate
Always cooperate in the first round. This signals cooperative intent and gives others the opportunity to establish sustainable behavior.

### Rounds 2 through (r-1): Adaptive Response

**Calculate the defection ratio from the previous round:**
```
defection_ratio = (number of D plays in previous round) / n
```

**Calculate stock health:**
```
stock_health = current_stock / capacity
```

**Decision logic:**

```
IF stock_health < 0.25:
    # Critical resource state - cooperate to allow recovery
    COOPERATE
    
ELIF defection_ratio == 0:
    # Everyone cooperated last round - maintain cooperation
    COOPERATE
    
ELIF defection_ratio <= 0.25:
    # Minor defection - forgive and cooperate to encourage return
    COOPERATE
    
ELIF defection_ratio <= 0.5:
    # Moderate defection - probabilistically defect
    # Probability of defecting = defection_ratio
    DEFECT with probability = defection_ratio
    COOPERATE otherwise
    
ELSE:
    # Majority defecting - defect to avoid exploitation
    # But leave small cooperation chance to signal willingness to return
    DEFECT with probability = 0.8
    COOPERATE with probability = 0.2
```

**Stock-adjusted override:**
```
IF stock_health > 0.9 AND defection_ratio < 0.5:
    # Resource is healthy and defection is manageable
    # Lean toward cooperation to maintain sustainability
    Increase cooperation probability by 0.2 (cap at 1.0)
```

### Final Round (Round r): Conditional Defection

```
IF stock > 0 AND defection_ratio_in_round_(r-1) >= 0.5:
    # Others are likely to defect; protect our share
    DEFECT
ELIF stock_health > 0.5:
    # Stock is healthy and others have been cooperative
    # Small defection as end-game hedge
    DEFECT with probability = 0.3
    COOPERATE with probability = 0.7
ELSE:
    # Stock is already damaged; little to gain from defection
    COOPERATE
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative baseline |
| Stock = 0 | Cooperate | No benefit to defecting; payoff is 0 either way |
| Stock very low (< 0.1 × capacity) | Cooperate | Maximize regeneration potential |
| All others defected last round | Defect (80% probability) | Avoid pure exploitation while leaving door open |
| All others cooperated last round | Cooperate | Maintain sustainable equilibrium |
| Final round, healthy stock | Lean toward defection | Limited future consequences |
| n = 2 (two players) | Use same rules but respond more directly | Defection ratio is binary (0, 0.5, or 1) |

---

## Pseudocode Summary

```python
def decide(round, total_rounds, n, capacity, current_stock, history):
    if round == 1:
        return COOPERATE
    
    defection_ratio = count_defections(history, round - 1) / n
    stock_health = current_stock / capacity
    
    # Critical stock protection
    if stock_health < 0.25:
        return COOPERATE
    
    # Final round logic
    if round == total_rounds:
        if defection_ratio >= 0.5:
            return DEFECT
        elif stock_health > 0.5:
            return random_choice(DEFECT=0.3, COOPERATE=0.7)
        else:
            return COOPERATE
    
    # Standard adaptive response
    if defection_ratio == 0:
        return COOPERATE
    elif defection_ratio <= 0.25:
        return COOPERATE
    elif defection_ratio <= 0.5:
        coop_prob = 1 - defection_ratio
        if stock_health > 0.9:
            coop_prob = min(1.0, coop_prob + 0.2)
        return random_choice(COOPERATE=coop_prob, DEFECT=1-coop_prob)
    else:
        coop_prob = 0.2
        if stock_health > 0.9:
            coop_prob = 0.4
        return random_choice(COOPERATE=coop_prob, DEFECT=1-coop_prob)
```

---

## Why This Strategy is Collectively Robust

1. **Sustainability-first**: Prioritizes keeping the resource healthy, which benefits everyone long-term
2. **Forgiveness**: Allows recovery from occasional defection without spiraling into mutual destruction
3. **Proportional response**: Matches defection levels rather than over-punishing
4. **Emergency cooperation**: When stock is critical, always cooperates to enable recovery
5. **Probabilistic play**: Creates unpredictability that makes pure exploitation strategies less effective
6. **Collective alignment**: If all players use this strategy, the equilibrium is full cooperation with maximum sustainable payoffs
'''

description_COLLECTIVE_31 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the shared resource is our common wealth, and preserving it maximizes long-term collective payoffs. However, we must be adaptive since we cannot guarantee others share this perspective. The strategy aims to **signal cooperative intent, reward cooperation, punish defection proportionally, and protect the resource from collapse**.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy uses three key metrics to make decisions:
1. **Stock Health Ratio (SHR)** = current_stock / capacity
2. **Cooperation Rate (CR)** = proportion of C plays observed in previous round
3. **Cumulative Cooperation Index (CCI)** = weighted average of cooperation rates across all past rounds (recent rounds weighted more heavily)

### Decision Rules

```
FUNCTION decide(round, stock, history, n, r, capacity):
    
    SHR = stock / capacity
    
    # FIRST ROUND: Signal cooperative intent
    IF round == 1:
        RETURN C
    
    # EMERGENCY PROTECTION: Save the resource from collapse
    IF SHR < 0.15:
        RETURN C  # Always cooperate when resource is critically low
    
    # LAST ROUND CONSIDERATION
    IF round == r:
        # If cooperation has been high, maintain it (collective reward)
        IF CCI > 0.6:
            RETURN C
        # If resource is healthy and cooperation mixed, still protect
        ELSE IF SHR > 0.5:
            RETURN C
        # Otherwise, match the prevailing behavior
        ELSE:
            RETURN D if CR < 0.5 else C
    
    # CALCULATE COOPERATION METRICS FROM HISTORY
    CR = count_C_last_round(history) / n
    CCI = weighted_average_cooperation(history)  # Decay factor 0.8 per round
    
    # MAIN DECISION LOGIC (Graduated Response)
    
    # High cooperation environment: Sustain cooperation
    IF CR >= 0.75:
        RETURN C
    
    # Moderate cooperation: Probabilistic response based on stock health
    IF CR >= 0.5:
        IF SHR > 0.6:
            RETURN C  # Resource healthy, encourage cooperation
        ELSE:
            RETURN C with probability = SHR + 0.2
            RETURN D otherwise
    
    # Low cooperation but resource still viable
    IF CR >= 0.25:
        IF SHR > 0.7:
            RETURN C  # Give cooperation another chance
        ELSE IF CCI > 0.5:
            RETURN C  # History suggests cooperation is possible
        ELSE:
            RETURN D  # Match defection to avoid exploitation
    
    # Very low cooperation: Defensive defection
    IF CR < 0.25:
        # But still try to save critically depleted resources
        IF SHR < 0.3:
            RETURN C  # Desperate attempt to preserve something
        ELSE:
            RETURN D  # Match prevailing behavior
```

### Key Design Principles

1. **Start Cooperative**: Always play C in round 1 to establish willingness to cooperate and give the collective a chance.

2. **Protect the Commons**: When stock drops below 15% of capacity, always cooperate regardless of others' behavior—some resource is better than none.

3. **Graduated Response**: Don't flip immediately between full cooperation and defection. Use probabilistic responses in mixed environments.

4. **Memory with Recency Bias**: Weight recent behavior more heavily than distant past, but don't ignore history entirely—this allows recovery from temporary defection spirals.

5. **Forgiveness Built In**: Even after defection, a return to cooperation by others triggers cooperative response. This enables recovery of cooperative equilibria.

6. **Stock-Aware Decisions**: When the resource is healthy (high SHR), be more forgiving and cooperative. When depleted, be more cautious but still try to preserve it.

### Edge Cases

- **Round 1**: Always C (establish cooperative baseline)
- **Last Round**: Maintain cooperation if collective history warrants it; don't automatically defect
- **Stock = 0**: Play C (no exploitation possible; hope for recovery signal)
- **Single Defector Among Cooperators**: Continue C (don't punish the collective for one bad actor)
- **Rapid Stock Decline**: Increase cooperation probability to slow depletion

### Why This Strategy is Collectively Optimal

If all players adopt this strategy:
- Universal cooperation maintains stock at capacity
- Total extraction is sustainable (stock/2 each round, fully regenerated)
- Each player earns capacity/(2n) every round indefinitely

Against defectors, the strategy protects collective interests while avoiding naive exploitation.
'''

description_COLLECTIVE_32 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource game is fundamentally about **collective survival**. Unlike a standard prisoner's dilemma, the stock dynamics create a shared fate: if we collectively over-extract, everyone's future payoffs collapse to zero. The strategy therefore prioritizes **resource sustainability** while remaining adaptive to exploitative opponents.

## Strategy: "Sustainable Threshold Guardian"

### Key Insight

The stock dynamics reveal a critical insight: when all cooperate, the resource regenerates fully (stock stays at capacity). When extraction exceeds regeneration capacity, the resource spirals toward depletion. The strategy uses stock levels as a **coordination signal** - since all players observe the same stock, it serves as implicit communication about collective behavior.

### Decision Rules

**Primary Rule: Cooperate by default, with conditional defection based on stock trajectory and history.**

```
function decide(game_params, current_stock, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    
    # Calculate key thresholds
    sustainable_threshold = capacity * 0.5  # Below this, resource is stressed
    critical_threshold = capacity * 0.25    # Below this, resource is in danger
    
    # RULE 1: First Round - Always Cooperate
    if current_round == 1:
        return COOPERATE
    
    # RULE 2: Critical Stock Protection
    # If stock is critically low, cooperate to allow recovery
    if current_stock < critical_threshold:
        return COOPERATE
    
    # RULE 3: Last Round Consideration
    # In final round, base decision on whether cooperation has been reciprocated
    if current_round == r:
        cooperation_rate = calculate_historical_cooperation_rate(history)
        if cooperation_rate >= 0.5:
            return COOPERATE  # Reward sustained cooperation
        else:
            return DEFECT  # No future to protect
    
    # RULE 4: Stock-Based Adaptive Response
    # Assess whether the collective has been sustainable
    if current_stock >= sustainable_threshold:
        # Resource is healthy - use generous tit-for-tat logic
        if previous_round_had_mass_defection(history, n):
            return DEFECT  # Signal that exploitation isn't tolerated
        else:
            return COOPERATE
    else:
        # Resource is stressed - prioritize recovery
        # Only defect if defection has been rampant (self-preservation)
        recent_defection_rate = calculate_recent_defection_rate(history, window=3)
        if recent_defection_rate > 0.7:
            return DEFECT  # Protect self from extreme exploitation
        else:
            return COOPERATE  # Try to restore the resource
    
    # DEFAULT: Cooperate
    return COOPERATE
```

### Helper Functions

```
function previous_round_had_mass_defection(history, n):
    if empty(history):
        return False
    last_round = history[-1]
    defection_count = count_defections(last_round)
    # "Mass defection" = more than half the players defected
    return defection_count > n / 2

function calculate_recent_defection_rate(history, window):
    if empty(history):
        return 0
    recent = history[-window:]  # Last 'window' rounds
    total_actions = sum(number_of_players in each round)
    total_defections = sum(defections in each round)
    return total_defections / total_actions

function calculate_historical_cooperation_rate(history):
    total_actions = sum(all actions across all rounds)
    total_cooperations = count(COOPERATE across all rounds)
    return total_cooperations / total_actions
```

### Edge Cases

1. **First round**: Always cooperate - establish cooperative norm without prior information
2. **Last round**: Conditionally cooperate based on historical cooperation rate - reward cooperative groups, don't sacrifice against defectors
3. **Near-zero stock**: Always cooperate - the resource must recover or everyone loses
4. **Single opponent (n=2)**: Strategy still applies; mass defection threshold becomes whether the opponent defected
5. **Very short games (r=2)**: Cooperate round 1, use last-round logic for round 2

### Why This Strategy is Collectively Aligned

1. **Sustainability focus**: Prioritizes keeping stock above sustainable levels, ensuring long-term collective payoffs
2. **Forgiveness**: Uses generous thresholds - only retaliates against *mass* defection, tolerating some deviation
3. **Signal through action**: Cooperation when stock is stressed signals commitment to collective welfare
4. **Stock as coordination**: All players see the same stock level, enabling implicit coordination without communication
5. **Protects against exploitation**: Will defect if facing overwhelming defection, preventing complete victimization
'''

description_COLLECTIVE_33 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy recognizes a fundamental truth: **the resource itself is the engine of collective wealth**. When stock is high and sustainable, everyone benefits more over time than if we all grab greedily. My strategy prioritizes keeping the resource alive while protecting against exploitation.

## Strategic Analysis

**Key Insight**: With the logistic growth function, maximum regeneration occurs at stock = capacity/2. If all cooperate, stock remains at capacity with growth = 0 (already full). The sustainable equilibrium with universal cooperation maintains the resource indefinitely.

**The Tragedy**: Individual defection is always myopically profitable (double the immediate payoff), but collective defection destroys the resource entirely.

**My Role**: I cannot control others, but I can:
1. Model cooperative behavior that sustains the resource
2. Respond to exploitation in ways that discourage it
3. Adapt to the actual population behavior I observe

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if:
    - Resource is healthy AND cooperation is reciprocated
    - OR resource is critically low (emergency conservation)
    - OR early game (establishing norms)

DEFECT if:
    - Widespread defection is occurring AND resource can sustain it
    - OR final round (no future to protect)
    - OR defection rate is high AND my cooperation alone cannot save the resource
```

### Detailed Rules

**Round 1: COOPERATE**
- Establish cooperative intent
- No history to react to
- Signal collective mindset

**Rounds 2 through (r-1): Conditional Strategy**

Calculate from previous round:
- `defection_rate` = (number of defectors) / n
- `stock_health` = stock / capacity

**Decision Matrix:**

| Stock Health | Defection Rate < 0.3 | Defection Rate 0.3-0.6 | Defection Rate > 0.6 |
|--------------|---------------------|------------------------|---------------------|
| > 0.5 (Healthy) | COOPERATE | COOPERATE with 70% probability | DEFECT |
| 0.25-0.5 (Stressed) | COOPERATE | DEFECT | DEFECT |
| < 0.25 (Critical) | COOPERATE | COOPERATE | COOPERATE |

**Rationale for Critical Stock Cooperation**: When stock is very low, even defecting yields little. Cooperating gives the resource a chance to regenerate. This is "emergency conservation mode."

**Final Round: DEFECT**
- No future rounds to protect
- Standard game-theoretic endpoint
- Others will likely defect too

---

## Pseudocode Implementation

```python
def decide(round_number, total_rounds, n, capacity, stock, history):
    
    # Final round: no future to consider
    if round_number == total_rounds:
        return DEFECT
    
    # First round: establish cooperation
    if round_number == 1:
        return COOPERATE
    
    # Calculate metrics from previous round
    prev_actions = history[-1]  # list of actions from last round
    defection_rate = sum(1 for a in prev_actions if a == DEFECT) / n
    stock_health = stock / capacity
    
    # Critical stock: emergency conservation
    if stock_health < 0.25:
        return COOPERATE
    
    # Healthy stock: tolerate some defection, model cooperation
    if stock_health > 0.5:
        if defection_rate < 0.3:
            return COOPERATE
        elif defection_rate < 0.6:
            # Probabilistic: mostly cooperate but signal concern
            return COOPERATE if random() < 0.7 else DEFECT
        else:
            # Majority defecting: protect myself
            return DEFECT
    
    # Stressed stock (0.25-0.5): less tolerance
    if defection_rate < 0.3:
        return COOPERATE
    else:
        return DEFECT
```

---

## Edge Cases

1. **n = 2 (Two players)**: Strategy remains valid; defection_rate thresholds map cleanly (0, 0.5, or 1.0)

2. **Very short games (r = 2)**: Cooperate round 1, defect round 2

3. **Stock reaches zero**: Continue cooperating (costs nothing, allows recovery if others cooperate)

4. **All others always defect**: After detecting this pattern (2-3 rounds), switch to permanent defection except at critical stock levels

5. **Stock exceeds capacity after growth**: Capped at capacity per rules; strategy unchanged

---

## Collective Alignment Statement

This strategy embodies **sustainable stewardship**: I cooperate by default because I recognize that my long-term welfare is tied to the collective resource. I defect only when the social contract has clearly broken down OR when the game is ending. I return to cooperation when the resource is in crisis because even a small chance of collective recovery is worth forgoing a meager defection payoff.
'''

description_COLLECTIVE_34 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all cooperate, the stock regenerates fully, providing stable returns indefinitely. Any defection triggers a tragedy of the commons spiral.

The strategy operates on the principle of **conditional cooperation with graduated forgiveness** - start cooperatively, respond proportionally to defection, but always leave room for collective recovery.

## Strategy Name: "Guardian with Hope"

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if:
  - First round (establish cooperative norm)
  - Stock health is critical (below 25% capacity) - emergency conservation
  - Recent cooperation rate among all players ≥ 50%
  - We're in a recovery phase after stock collapse

DEFECT if:
  - Last round (no future to protect)
  - Penultimate round AND cooperation rate < 75%
  - Majority defected in previous round AND stock > 50% capacity
  - Sustained defection pattern (3+ consecutive rounds of majority defection)
```

### Detailed Decision Algorithm

```python
def decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    
    # RULE 1: First round - always cooperate to establish norm
    if current_round == 1:
        return COOPERATE
    
    # RULE 2: Last round - defect (no future consequences)
    if current_round == r:
        return DEFECT
    
    # RULE 3: Critical stock emergency - cooperate to prevent collapse
    if stock_ratio < 0.25:
        return COOPERATE
    
    # Analyze recent history
    last_round_actions = history[-1]
    defection_count = count_defections(last_round_actions)
    cooperation_rate = 1 - (defection_count / n)
    
    # RULE 4: Near-end game caution
    rounds_remaining = r - current_round
    if rounds_remaining <= 2 and cooperation_rate < 0.75:
        return DEFECT
    
    # RULE 5: Respond to majority behavior
    if cooperation_rate >= 0.5:
        # Majority cooperated - reward with cooperation
        return COOPERATE
    else:
        # Majority defected
        if stock_ratio > 0.5:
            # Stock can absorb punishment - defect as warning
            return DEFECT
        else:
            # Stock is stressed - cooperate to prevent collapse
            # This is "turn the other cheek" for collective survival
            return COOPERATE
    
    # RULE 6: Trend analysis for sustained patterns
    if len(history) >= 3:
        recent_coop_rates = [get_coop_rate(h, n) for h in history[-3:]]
        if all(rate < 0.5 for rate in recent_coop_rates):
            # Sustained defection - match it if stock allows
            if stock_ratio > 0.4:
                return DEFECT
    
    # Default: Cooperate (optimistic)
    return COOPERATE
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | COOPERATE | Signal cooperative intent, no history to react to |
| **Round r (final)** | DEFECT | No future rounds to protect; rational endpoint |
| **Round r-1** | Conditional | Cooperate only if sustained cooperation observed |
| **Stock < 25% capacity** | COOPERATE | Emergency conservation - collective survival mode |
| **Stock = 0** | COOPERATE | Only regeneration path; defecting yields nothing anyway |
| **All others defected** | COOPERATE if stock critical, else DEFECT | Protect commons when fragile, punish when robust |
| **n = 2 (two players)** | Standard rules apply | Tit-for-tat dynamics emerge naturally |

---

## Collective Alignment Statement

This strategy embodies **collective rationality**: the understanding that my long-term payoff is maximized when the group sustains the resource. Key collective principles:

1. **Sustainability over extraction**: A stock at capacity yields 12.5 per round forever; depleting it yields 25 once then nothing.

2. **Forgiveness enables recovery**: Even after defection, returning to cooperation can restore the stock to capacity in ~2-3 rounds.

3. **Punishment preserves norms**: Matching defection when stock is healthy signals that exploitation won't be tolerated.

4. **Emergency cooperation is self-interested**: When stock is critical, even selfish agents should conserve - there's nothing left to extract.

The strategy assumes other collective-minded agents will recognize these same truths and converge on cooperation. Against purely selfish opponents, it protects the commons while signaling willingness to retaliate.
'''

description_COLLECTIVE_35 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The key insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully each round, maximizing total payoffs across all rounds. Any defection degrades this collective wealth.

The strategy uses **conditional cooperation with graduated punishment and forgiveness**, designed to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but not vindictively
4. Allow recovery when cooperation re-emerges

---

## Decision Rules

### Primary Decision Framework

```
DECIDE(stock, history, round, total_rounds, n, capacity):
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Phase 1: Opening Signal (Round 1)
    IF round == 1:
        RETURN COOPERATE
    
    # Phase 2: Endgame Protection (Final round)
    IF rounds_remaining == 0:
        # Mirror majority behavior from previous round
        IF majority_cooperated_last_round(history):
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # Phase 3: Resource Crisis Response
    IF stock_ratio < 0.25:
        RETURN COOPERATE  # Emergency conservation
    
    # Phase 4: Conditional Cooperation Core
    RETURN conditional_cooperation_decision(history, stock_ratio, rounds_remaining)
```

### Conditional Cooperation Logic

```
CONDITIONAL_COOPERATION_DECISION(history, stock_ratio, rounds_remaining):
    
    # Calculate cooperation metrics
    recent_coop_rate = cooperation_rate(last_3_rounds(history))
    overall_coop_rate = cooperation_rate(all_rounds(history))
    defection_streak = consecutive_defection_rounds(history)
    
    # Forgiveness threshold - more forgiving when stock is healthy
    forgiveness_threshold = 0.3 + (0.2 * stock_ratio)
    
    # Strong cooperation environment
    IF recent_coop_rate >= 0.7:
        RETURN COOPERATE
    
    # Moderate cooperation - cooperate if stock is sustainable
    IF recent_coop_rate >= 0.5 AND stock_ratio >= 0.5:
        RETURN COOPERATE
    
    # Recovering from defection - test for reciprocity
    IF defection_streak >= 2 AND recent_coop_rate < forgiveness_threshold:
        # Defect once to signal that exploitation has consequences
        RETURN DEFECT
    
    # Forgiveness probe - after punishing, try cooperation again
    IF previous_action_was_defect(history) AND recent_coop_rate >= forgiveness_threshold:
        RETURN COOPERATE
    
    # Default: Tit-for-tat with majority
    IF majority_cooperated_last_round(history):
        RETURN COOPERATE
    ELSE:
        RETURN DEFECT
```

---

## Helper Functions

```
COOPERATION_RATE(rounds):
    total_actions = count_all_actions(rounds)
    cooperations = count_cooperations(rounds)
    RETURN cooperations / total_actions

MAJORITY_COOPERATED_LAST_ROUND(history):
    last_round = history[-1]
    cooperators = count_players_who_cooperated(last_round)
    RETURN cooperators > n/2

CONSECUTIVE_DEFECTION_ROUNDS(history):
    count = 0
    FOR round IN reversed(history):
        IF majority_defected(round):
            count += 1
        ELSE:
            BREAK
    RETURN count
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative intent; no information to act on yet |
| **Final round** | Mirror majority | Avoid being exploited, but reward prior cooperation |
| **Stock < 25% capacity** | Cooperate | Resource collapse hurts everyone; prioritize survival |
| **Stock near capacity** | Follow conditional rules | Normal strategic play when resource is healthy |
| **All others defected** | Defect once, then probe | Signal consequences, but don't abandon hope |
| **Mixed behavior** | Cooperate if ≥50% cooperated | Support emerging cooperation |

---

## Strategic Properties

1. **Nice**: Never defects first (starts cooperative)
2. **Provocable**: Responds to defection with measured punishment
3. **Forgiving**: Returns to cooperation when others do
4. **Clear**: Simple rules that opponents can learn to predict
5. **Collective**: Prioritizes resource sustainability over short-term individual gain

This strategy aims to be a **cooperative anchor** - demonstrating that sustainable harvesting is possible while defending against exploitation.
'''

description_COLLECTIVE_36 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared asset whose long-term health benefits everyone. The fundamental insight is that **sustainable harvesting (all cooperate) maintains the resource indefinitely, while defection creates a tragedy of the commons that ultimately impoverishes all players**.

The strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but allow redemption
4. Adapt to the reality of opponent behavior

---

## Decision Rules

### Primary Variables to Track
- `stock`: Current resource level
- `round`: Current round number (1 to r)
- `history`: Record of all players' actions each round
- `defection_rate`: Proportion of defections in previous round
- `cumulative_defection_rate`: Overall defection rate across all rounds
- `stock_trend`: Whether stock is increasing, stable, or declining

### Decision Framework

```
function decide(round, stock, history, n, r, capacity):
    
    # Calculate key metrics
    if round > 1:
        last_round_defections = count_defections(history[round-1])
        defection_rate = last_round_defections / n
        cumulative_defection_rate = total_defections(history) / (n * (round-1))
        stock_health = stock / capacity
    
    # PHASE 1: OPENING (Round 1)
    if round == 1:
        return COOPERATE  # Signal cooperative intent
    
    # PHASE 2: CRITICAL RESOURCE PROTECTION
    if stock < capacity / n:
        return COOPERATE  # Emergency conservation mode
    
    # PHASE 3: ENDGAME (Final 2 rounds)
    if round >= r - 1:
        # In final rounds, mirror the community's behavior
        if cumulative_defection_rate > 0.5:
            return DEFECT  # Community has been exploitative
        else:
            return COOPERATE  # Reward cooperative community
    
    # PHASE 4: ADAPTIVE TIPPING POINT STRATEGY
    # Cooperate if the community is mostly cooperative
    # Defect if defection becomes endemic (self-protection)
    
    cooperation_threshold = calculate_threshold(stock, capacity, round, r)
    
    if defection_rate <= cooperation_threshold:
        return COOPERATE
    else:
        # Graduated response based on severity
        if defection_rate > 0.75:
            return DEFECT  # Severe defection - protect self
        elif stock_health > 0.6:
            return COOPERATE  # Resource healthy - try to restore cooperation
        else:
            return DEFECT  # Resource stressed and others defecting
```

### Threshold Calculation

```
function calculate_threshold(stock, capacity, round, r):
    # Base threshold: tolerate up to 25% defection
    base = 0.25
    
    # Be more forgiving when resource is healthy
    health_bonus = 0.15 * (stock / capacity)
    
    # Be more forgiving early in the game (time to establish norms)
    time_bonus = 0.10 * (1 - round / r)
    
    return min(base + health_bonus + time_bonus, 0.5)
```

---

## Edge Case Handling

### Round 1
**Action: COOPERATE**
- Establishes cooperative intent from the start
- No information yet about others' behavior
- Creates opportunity for mutual cooperation equilibrium

### Last Round
**Action: Based on cumulative cooperation rate**
- If community has been >50% cooperative: COOPERATE (reward and maintain trust)
- If community has been >50% defecting: DEFECT (no future rounds to punish, protect self)

### Stock Near Zero (< capacity/n)
**Action: COOPERATE regardless of other factors**
- Resource collapse harms everyone
- Even defectors benefit from resource recovery
- Signals commitment to collective survival

### All Others Defected Last Round
**Action: DEFECT (with forgiveness window)**
- Self-protection when clearly being exploited
- But return to cooperation if any round shows improvement

### Perfect Cooperation History
**Action: COOPERATE**
- Maintain the successful equilibrium
- No reason to disrupt mutual benefit

---

## Collective Alignment Principles

1. **Resource Stewardship**: The strategy treats the common pool as a shared inheritance. When stock is healthy and others cooperate, we maintain it. This isn't naïve—it's recognizing that sustainable use serves everyone.

2. **Conditional Cooperation**: We cooperate by default but aren't doormats. The graduated response protects against exploitation while remaining open to cooperation.

3. **Forgiveness Over Punishment**: Rather than permanent retaliation (like grim trigger), this strategy continuously reassesses. One bad round doesn't doom the future—this allows recovery from misunderstandings or strategy shifts.

4. **Emergency Conservation**: When the resource is critically low, cooperation becomes paramount regardless of others' behavior. A collapsed resource helps no one.

5. **Community Mirroring**: The strategy ultimately reflects the community's character. Cooperative communities get a cooperative player; exploitative communities face proportional responses.

---

## Summary

**Cooperate when:**
- Round 1 (always)
- Stock is critically low (< capacity/n)
- Recent defection rate is below the adaptive threshold
- Community has been majority cooperative in endgame

**Defect when:**
- Defection rate exceeds threshold AND stock is stressed
- Severe defection (>75%) in previous round
- Final rounds with historically exploitative community

This strategy balances collective welfare with self-protection, adapts to observed behavior, and maintains the resource for sustained mutual benefit whenever possible.
'''

description_COLLECTIVE_37 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the resource is our shared inheritance, and its preservation benefits everyone across all rounds. The key insight is that universal cooperation maintains the stock at capacity indefinitely (yielding `capacity/(2n)` per round forever), while defection creates a tragedy of the commons that destroys future value for everyone.

## Strategy Overview: "Sustainable Guardian"

The strategy uses **graduated reciprocity with forgiveness**, prioritizing long-term collective welfare while protecting against exploitation.

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if ANY of the following are true:
  1. First round (establish cooperative norm)
  2. Stock is critically low (emergency conservation)
  3. Recent history shows sufficient cooperation
  4. Sufficient rounds remain to recover from cooperation

DEFECT if ALL of the following are true:
  1. Not first round
  2. Stock is not critically low
  3. Recent defection rate exceeds threshold
  4. Limited rounds remain OR pattern suggests persistent defection
```

### Detailed Decision Logic

**Step 1: Assess Resource Health**
```
stock_ratio = stock / capacity
critical_threshold = 0.25
healthy_threshold = 0.75
```

**Step 2: Analyze Recent History (last min(3, rounds_played) rounds)**
```
cooperation_rate = (total C plays by all players) / (total plays by all players)
defection_trend = is cooperation_rate declining over last 3 rounds?
```

**Step 3: Consider Time Horizon**
```
rounds_remaining = r - current_round
early_game = rounds_remaining > 0.7 * r
late_game = rounds_remaining <= 3
final_round = rounds_remaining == 0
```

**Step 4: Make Decision**

```python
def decide(stock, capacity, history, current_round, total_rounds, n):
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - current_round
    
    # FIRST ROUND: Always cooperate to signal collective intent
    if current_round == 1:
        return COOPERATE
    
    # EMERGENCY CONSERVATION: If stock is critical, cooperate to save resource
    if stock_ratio < 0.25:
        return COOPERATE
    
    # FINAL ROUND: Mirror majority behavior from previous round
    if rounds_remaining == 0:
        last_round_coop_rate = cooperation_rate(history, last_round_only=True)
        return COOPERATE if last_round_coop_rate >= 0.5 else DEFECT
    
    # ANALYZE RECENT BEHAVIOR (last 3 rounds or all if fewer)
    lookback = min(3, len(history))
    recent_coop_rate = cooperation_rate(history, last_n_rounds=lookback)
    
    # HIGH COOPERATION ENVIRONMENT: Maintain cooperation
    if recent_coop_rate >= 0.7:
        return COOPERATE
    
    # MODERATE COOPERATION: Cooperate if stock healthy, signal willingness
    if recent_coop_rate >= 0.4:
        if stock_ratio >= 0.5:
            return COOPERATE
        else:
            # Probabilistic: cooperate with probability = recent_coop_rate
            return COOPERATE with probability recent_coop_rate
    
    # LOW COOPERATION ENVIRONMENT: Protect but offer olive branch
    if recent_coop_rate < 0.4:
        # Every 3rd round, cooperate to test for recovery
        if current_round % 3 == 0:
            return COOPERATE
        else:
            return DEFECT
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | COOPERATE | Establish cooperative norm, signal collective intent |
| **Final round** | Mirror majority | No future to protect, but maintain consistency |
| **Stock near zero** | COOPERATE | Emergency conservation; defection gains nothing from empty pool |
| **All others defected last round** | COOPERATE (test) every 3rd round | Offer path back to cooperation |
| **Stock at capacity, all cooperating** | COOPERATE | Optimal sustainable equilibrium |
| **n=2 (two players)** | Use standard Tit-for-Tat with forgiveness | Direct reciprocity works well |

---

## Why This Strategy is Collectively Optimal

1. **Preserves the resource**: Universal cooperation maintains stock at capacity, maximizing long-term total payoffs
2. **Forgiveness enables recovery**: Periodic cooperation tests allow escape from defection spirals
3. **Emergency conservation**: Protects against total collapse, which hurts everyone
4. **Graduated response**: Proportional reaction avoids unnecessary escalation
5. **Robust to noise**: Doesn't punish single defections harshly, recognizing that independent strategies may vary
'''

description_COLLECTIVE_38 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: if all players adopt this same strategy, we should achieve sustainable, near-optimal outcomes. The strategy prioritizes long-term resource sustainability while protecting against exploitation, recognizing that the commons can only thrive through mutual restraint.

## Strategy Name: **Sustainable Commons Guardian**

---

## Decision Framework

### Primary Decision Rule

The strategy operates on three key principles:
1. **Default to cooperation** to maintain the resource
2. **Punish defection collectively** to deter exploitation
3. **Forgive and restore** to escape punishment cycles

### Decision Variables

At each round t, calculate:
- `stock`: current resource level
- `stock_ratio = stock / capacity`: health of the commons
- `prev_defection_rate`: fraction of players who defected last round
- `rounds_remaining = r - t`

---

## Detailed Decision Rules

### Round 1 (First Round)
**Action: COOPERATE**

Rationale: Establish cooperative norms. With no history, assume good faith and demonstrate collective intent.

### Rounds 2 through r-1 (Middle Rounds)

```
IF stock_ratio < 0.25 (CRITICAL):
    # Resource is critically depleted - must cooperate to allow recovery
    Action: COOPERATE
    
ELSE IF prev_defection_rate == 0:
    # Full cooperation last round - maintain it
    Action: COOPERATE
    
ELSE IF prev_defection_rate >= 0.5:
    # Majority defected - trigger collective punishment
    # But with probability based on stock health
    IF stock_ratio > 0.6:
        Action: DEFECT (punish to establish norm)
    ELSE:
        Action: COOPERATE (resource too fragile for punishment)
        
ELSE IF prev_defection_rate > 0 AND prev_defection_rate < 0.5:
    # Minority defected - use proportional response
    # Cooperate with probability (1 - prev_defection_rate)
    # This is forgiving but signals disapproval
    IF deterministic_signal(round, player_context) < prev_defection_rate:
        Action: DEFECT
    ELSE:
        Action: COOPERATE
```

### Round r (Final Round)

```
IF stock_ratio < 0.3:
    # Resource is low - defecting gains little, cooperate for dignity
    Action: COOPERATE
    
ELSE IF history shows consistent cooperation (defection_rate over all rounds < 0.2):
    # Honor the cooperative relationship
    Action: COOPERATE
    
ELSE:
    # Mixed history - defect is rational but consider collective outcome
    # If we're all following this strategy, we should all cooperate
    Action: COOPERATE
```

**Final Round Rationale**: A collective strategy should cooperate even in the last round because if all players use this strategy, everyone cooperating yields stock/(2n) per player, and the resource ends sustainably. Mutual defection often depletes the resource entirely, potentially yielding less if stock is low.

---

## Edge Cases

### Near-Depleted Resource (stock < capacity/4)
Always cooperate regardless of history. The resource needs recovery, and defecting from a nearly empty pool gains almost nothing while ensuring collapse.

### After Punishment Round
If we defected as punishment and cooperation resumed, immediately return to cooperation. The punishment served its purpose.

### Detecting Persistent Defectors
If defection rate has been > 0.3 for 3+ consecutive rounds:
- The population may include persistent defectors
- Continue proportional response but weight toward cooperation
- Protecting the resource matters more than punishing

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, history):
    stock_ratio = stock / capacity
    
    # First round: cooperate
    if round == 1:
        return COOPERATE
    
    prev_defection_rate = count_defections(history[-1]) / n
    
    # Critical resource: always cooperate
    if stock_ratio < 0.25:
        return COOPERATE
    
    # Final round: cooperate (collective mindset)
    if round == total_rounds:
        return COOPERATE
    
    # Perfect cooperation: maintain it
    if prev_defection_rate == 0:
        return COOPERATE
    
    # Majority defection with healthy stock: punish
    if prev_defection_rate >= 0.5 and stock_ratio > 0.6:
        return DEFECT
    
    # Partial defection: proportional forgiveness
    # Use round number as deterministic seed for consistency
    threshold = prev_defection_rate
    if (round * 7) % 100 / 100 < threshold:
        return DEFECT
    else:
        return COOPERATE
```

---

## Why This Strategy is Collectively Optimal

1. **Self-sustaining**: If all players use this strategy, everyone cooperates every round, stock remains at capacity, and each player earns `capacity/(2n)` per round for all r rounds.

2. **Robust**: Proportional punishment deters exploitation without triggering collapse.

3. **Forgiving**: Quick return to cooperation allows escape from punishment cycles.

4. **Resource-conscious**: Prioritizes commons health over individual punishment, recognizing that a depleted resource hurts everyone.
'''

description_COLLECTIVE_39 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared inheritance. The optimal collective outcome requires sustainable harvesting - when all cooperate, the resource regenerates fully, providing maximum long-term value. My strategy aims to **protect the commons while remaining robust against exploitation**.

## Strategy: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to stewardship** - Cooperate to sustain the resource
2. **Respond proportionally to defection** - Match the community's behavior with a bias toward forgiveness
3. **Protect critically depleted resources** - Cooperate unconditionally when the stock is dangerously low

### Decision Rules

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- capacity: maximum sustainable stock
- n: number of players
- history: list of (my_action, defection_rate) for each past round
  where defection_rate = proportion of OTHER players who defected

CALCULATE:
- critical_threshold = capacity / (2 * n)  # Below this, resource may collapse
- stock_ratio = stock / capacity
- rounds_remaining = r - round + 1

DECISION:
```

**1. First Round:**
- **COOPERATE** - Signal cooperative intent and give others the benefit of the doubt

**2. Final Round:**
- If stock_ratio ≥ 0.5: **DEFECT** (no future to protect, but resource is healthy)
- If stock_ratio < 0.5: **COOPERATE** (protect what remains as a collective good)

**3. Critical Resource Protection (stock ≤ critical_threshold):**
- **COOPERATE** unconditionally - The resource needs protection regardless of others' behavior

**4. Standard Rounds (all other cases):**

Calculate a **cooperation score** based on recent history:

```
recent_rounds = min(3, len(history))
recent_defection_avg = average defection_rate over last recent_rounds

IF recent_defection_avg ≤ 0.25:
    # Mostly cooperative environment
    COOPERATE
    
ELIF recent_defection_avg ≤ 0.5:
    # Mixed environment - use probabilistic response
    cooperation_probability = 1 - recent_defection_avg
    # Bias toward cooperation when resource is healthy
    IF stock_ratio ≥ 0.7:
        cooperation_probability += 0.2
    COOPERATE with probability = min(cooperation_probability, 0.9)
    
ELIF recent_defection_avg ≤ 0.75:
    # High defection - match but leave room for recovery
    DEFECT with probability = recent_defection_avg
    
ELSE:
    # Severe defection - protect self but watch for recovery
    IF any of last 2 rounds had defection_rate < 0.5:
        COOPERATE (reward attempted recovery)
    ELSE:
        DEFECT
```

**5. Recovery Incentive:**
After any round where I defected, if the next round shows defection_rate dropped by ≥ 0.25:
- Override to **COOPERATE** (reward collective improvement)

### Pseudocode Summary

```python
def decide(round, stock, capacity, n, history):
    critical = capacity / (2 * n)
    stock_ratio = stock / capacity
    
    # First round: cooperate
    if round == 1:
        return COOPERATE
    
    # Final round: conditional
    if round == r:
        return DEFECT if stock_ratio >= 0.5 else COOPERATE
    
    # Critical resource: always protect
    if stock <= critical:
        return COOPERATE
    
    # Calculate recent defection
    recent = history[-min(3, len(history)):]
    avg_defection = mean([h.defection_rate for h in recent])
    
    # Graduated response
    if avg_defection <= 0.25:
        return COOPERATE
    elif avg_defection <= 0.5:
        p = (1 - avg_defection) + (0.2 if stock_ratio >= 0.7 else 0)
        return COOPERATE if random() < min(p, 0.9) else DEFECT
    elif avg_defection <= 0.75:
        return DEFECT if random() < avg_defection else COOPERATE
    else:
        if len(history) >= 2 and any(h.defection_rate < 0.5 for h in history[-2:]):
            return COOPERATE
        return DEFECT
```

## Why This Strategy Aligns with Collective Interests

1. **Sustains the resource** - Default cooperation keeps stock at capacity
2. **Forgives and recovers** - Multiple pathways back to cooperation
3. **Protects against collapse** - Never defects when resource is critical
4. **Proportional deterrence** - Makes defection less attractive without being vindictive
5. **Rewards improvement** - Explicitly cooperates when others reduce defection
'''

description_COLLECTIVE_40 = '''
# Collective Strategy for the Common Pool Resource Game

## Strategic Philosophy

This game presents a classic tragedy of the commons with regeneration dynamics. The key insight is that **universal cooperation is self-sustaining** (stock regenerates fully when all cooperate), while defection creates a downward spiral. My strategy aims to establish and maintain cooperation through conditional reciprocity, while protecting against exploitation.

## Core Decision Rules

### Primary Strategy: "Generous Threshold Trigger"

**Cooperate if and only if:**
1. The stock is healthy enough to sustain cooperation, AND
2. The recent cooperation rate among all players (including myself) meets a threshold, OR
3. It's early enough in the game to establish cooperative norms

**Defect otherwise** (to avoid being exploited while the resource collapses).

---

## Detailed Decision Logic

### Round 1: Always Cooperate
- Signal cooperative intent
- No history to judge others
- Resource is at capacity, so cooperation is sustainable

### Rounds 2 through (r-2): Conditional Cooperation

```
cooperation_threshold = 0.6  # At least 60% of actions should be C
lookback_window = min(3, rounds_played)  # Consider recent history

recent_cooperation_rate = (total C actions in last lookback_window rounds) / (n × lookback_window)

stock_health = current_stock / capacity

IF stock_health < 0.25:
    # Resource critically depleted - defect to salvage what remains
    # (cooperation won't save a dying resource if others defect)
    DEFECT
    
ELIF recent_cooperation_rate >= cooperation_threshold:
    # Cooperation norm is holding - maintain it
    COOPERATE
    
ELIF stock_health > 0.7 AND recent_cooperation_rate >= 0.4:
    # Resource still healthy, give cooperation another chance
    # (generous forgiveness to re-establish norms)
    COOPERATE
    
ELSE:
    # Cooperation has broken down and resource is declining
    DEFECT
```

### Round (r-1): Penultimate Round
- Apply the same logic as middle rounds
- Cooperation still valuable as it affects final round stock

### Round r (Final Round): Conditional Based on History

```
IF overall_cooperation_rate >= 0.7:
    # Reward a cooperative game with final cooperation
    # (collective identity maintained to the end)
    COOPERATE
ELSE:
    # No future to protect - take fair share
    DEFECT
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | COOPERATE | Payoff is 0 either way; signal willingness to rebuild |
| Only 2 rounds total | C then conditional | Minimal time to establish norms |
| All others defected last round | DEFECT | Protect against mass exploitation |
| Stock near capacity despite some D | COOPERATE | Resource is resilient, maintain cooperation |
| I'm the only one who cooperated | DEFECT next round | Avoid pure exploitation |

---

## Adaptive Mechanisms

### Forgiveness Component
After a round of mutual defection, if stock remains above 50% capacity:
- Return to cooperation with 70% probability (conceptually: lean toward cooperation)
- This prevents permanent breakdown from temporary lapses

### Exploitation Detection
If I cooperate but the cooperation rate is below 40% for two consecutive rounds:
- Switch to defection until cooperation rate recovers above 50%

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, history, n):
    if round == 1:
        return COOPERATE
    
    lookback = min(3, round - 1)
    recent_coop_rate = count_C_actions(history, lookback) / (n * lookback)
    stock_health = stock / capacity
    
    # Final round
    if round == total_rounds:
        overall_coop_rate = count_C_actions(history, round-1) / (n * (round-1))
        return COOPERATE if overall_coop_rate >= 0.7 else DEFECT
    
    # Critical stock - salvage mode
    if stock_health < 0.25:
        return DEFECT
    
    # Cooperation holding
    if recent_coop_rate >= 0.6:
        return COOPERATE
    
    # Generous forgiveness when stock is healthy
    if stock_health > 0.7 and recent_coop_rate >= 0.4:
        return COOPERATE
    
    return DEFECT
```

---

## Why This Strategy is Collectively Aligned

1. **Starts cooperative** - establishes good faith
2. **Maintains cooperation when viable** - sustains the resource for everyone
3. **Forgives occasional defection** - doesn't trigger spirals from noise
4. **Protects the collective from collapse** - defects when resource is critically low (taking less from nothing still equals nothing)
5. **Rewards cooperative games** - final round cooperation when norms held
'''

description_COLLECTIVE_41 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the resource is our shared inheritance, and its preservation benefits everyone across all rounds. However, I must be adaptive since I cannot assume others share this view. My approach balances **hopeful cooperation** with **protective responses** to exploitation.

## Strategy: "Generous Threshold Guardian"

### Key Principles

1. **Sustainability First**: Cooperation (C) maintains the resource at capacity indefinitely, maximizing total group payoff across all rounds
2. **Forgiveness Over Punishment**: In a multi-player setting, harsh retaliation can spiral destructively
3. **Stock-Aware Adaptation**: When the resource is depleted, the game fundamentally changes—respond accordingly
4. **End-Game Awareness**: Limited remaining rounds shift optimal behavior

---

## Decision Rules

### Round 1: Unconditional Cooperation
- **Action: C**
- Rationale: Signal cooperative intent, gather information about others, and the resource is at capacity so stakes for establishing trust are highest.

### Rounds 2 through (r-1): Adaptive Cooperation

Calculate the following metrics from the previous round:

```
defection_rate = (number of D plays last round) / n
stock_health = current_stock / capacity
rounds_remaining = r - current_round
```

**Decision Logic:**

```
IF stock_health ≥ 0.5:
    # Resource is healthy - lean cooperative
    IF defection_rate ≤ 0.5:
        → Play C (majority cooperating, sustain this)
    ELSE IF defection_rate > 0.5 AND defection_rate < 1.0:
        → Play C with probability (1 - defection_rate)
        → Play D with probability defection_rate
    ELSE (all defected):
        → Play D (resource will collapse anyway, salvage value)

ELSE IF stock_health ≥ 0.25:
    # Resource stressed - more cautious
    IF defection_rate ≤ 0.25:
        → Play C (reward the cooperators, allow recovery)
    ELSE:
        → Play D (protect against further exploitation)

ELSE (stock_health < 0.25):
    # Critical depletion - survival mode
    → Play D (resource is collapsing, minimize personal loss)
```

### Last Round (Round r): Conditional Defection

```
IF stock_health ≥ 0.75 AND historical_cooperation_rate ≥ 0.75:
    → Play C (honor the collective achievement)
ELSE:
    → Play D (no future rounds to preserve for)
```

Where `historical_cooperation_rate` = total C plays by all players / (n × (r-1))

---

## Edge Cases

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **n = 2** | Follow same rules but weight defection_rate more heavily | Single defector has massive impact |
| **r = 2** | Round 1: C, Round 2: D unless partner played C | Minimal time to build trust |
| **Stock near zero** | D | No growth possible, salvage remaining value |
| **Stock at capacity after defections** | C | Growth formula restored it; fresh start |
| **I'm the only cooperator repeatedly** | Switch to D | Don't be exploited indefinitely |

---

## Pseudocode Summary

```python
def choose_action(round, stock, capacity, n, r, history):
    stock_health = stock / capacity
    
    if round == 1:
        return C
    
    defection_rate = count_defections(history, round - 1) / n
    rounds_remaining = r - round
    
    if round == r:  # Last round
        hist_coop_rate = total_cooperations(history) / (n * (r - 1))
        if stock_health >= 0.75 and hist_coop_rate >= 0.75:
            return C
        return D
    
    if stock_health >= 0.5:
        if defection_rate <= 0.5:
            return C
        elif defection_rate < 1.0:
            return C with probability (1 - defection_rate)
        else:
            return D
    elif stock_health >= 0.25:
        if defection_rate <= 0.25:
            return C
        return D
    else:
        return D
```

---

## Why This Strategy is Collectively Aligned

1. **Promotes sustainability**: Default cooperation maintains the renewable resource at capacity
2. **Invites others to cooperate**: Generous thresholds and forgiveness encourage coordination
3. **Protects the collective from collapse**: Stock-awareness prevents futile cooperation during resource death spirals
4. **Rewards good behavior**: Maintains cooperation even in the last round if the group earned it
5. **Adapts without over-punishing**: Probabilistic responses to mixed behavior avoid destructive retaliation cycles
'''

description_COLLECTIVE_42 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy operates from a **collective sustainability mindset**: the shared resource is most valuable when preserved, and mutual cooperation yields the highest total payoffs across all rounds. However, we must be adaptive since other players may not share this perspective.

## Strategy Overview: "Sustainable Threshold with Graduated Response"

The strategy balances three key principles:
1. **Sustainability First**: Protect the resource from collapse
2. **Conditional Cooperation**: Reward cooperative behavior, discourage exploitation
3. **Pragmatic Adaptation**: Adjust based on observed behavior and remaining rounds

---

## Decision Rules

### Round 1: Cooperate
- Signal willingness to sustain the resource
- Establish baseline for observing others' behavior

### Middle Rounds (2 to r-1):

**Primary Decision Variables:**
- `coop_rate` = proportion of players who cooperated last round
- `stock_health` = current_stock / capacity
- `rounds_remaining` = r - current_round

**Decision Logic:**

```
IF stock_health < 0.25 THEN:
    # Critical resource level - cooperate to allow recovery
    COOPERATE

ELSE IF coop_rate >= 0.5 THEN:
    # Majority cooperating - maintain cooperation
    COOPERATE

ELSE IF coop_rate < 0.5 AND stock_health > 0.6 THEN:
    # Others defecting but resource healthy
    # Defect to avoid pure exploitation, but signal we respond to context
    DEFECT

ELSE IF coop_rate < 0.5 AND stock_health <= 0.6 THEN:
    # Resource declining and others defecting
    # Cooperate to slow decline - demonstrate sustainable intent
    # This may seem counterintuitive but preserves future value
    COOPERATE with probability = stock_health
    DEFECT with probability = 1 - stock_health

END IF
```

### Final Round:
```
IF stock_health < 0.3 THEN:
    # Resource nearly depleted - little to gain from defection
    COOPERATE (preserves some collective dignity)
ELSE:
    # Standard game theory suggests defection, but...
    # If majority cooperated throughout, maintain cooperation
    IF average_coop_rate_all_rounds >= 0.6 THEN:
        COOPERATE
    ELSE:
        DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline |
| **Last round** | Conditional (see above) | Balance game theory with collective norms |
| **Stock near zero** | Cooperate | Recovery only possible through restraint |
| **Stock at capacity** | Follow standard rules | No emergency override needed |
| **All others defected last round** | Cooperate if stock < 50%, else Defect | Protect resource but don't be purely exploited |
| **n = 2 (two players)** | Standard rules apply | Each player's choice more impactful |
| **Very few rounds remaining** | Weight toward defection slightly | Less future value to protect |

---

## Adaptive Mechanism: Tracking Cooperation History

```
Initialize:
    player_coop_counts = [0] * n  # Track each player's cooperation history
    
After each round:
    For each player j:
        If player j cooperated:
            player_coop_counts[j] += 1
    
    overall_coop_rate = sum(player_coop_counts) / (n * current_round)
```

This history informs whether the group has established cooperative norms or is trending toward exploitation.

---

## Why This Strategy is Collectively Aligned

1. **Prioritizes sustainability**: The stock threshold checks ensure the resource doesn't collapse, preserving value for everyone

2. **Rewards cooperation**: By cooperating when others cooperate, we reinforce positive collective behavior

3. **Protects against collapse**: Even when others defect, we cooperate at low stock levels because a depleted resource hurts everyone

4. **Not purely exploitable**: We do defect when the resource is healthy and others are defecting, preventing pure free-riding on our restraint

5. **Signals intent**: First-round cooperation and stock-protective behavior signal our collective orientation to observant opponents

---

## Expected Behavior in Tournament

- Against **cooperative opponents**: Maintains full cooperation, achieving optimal collective payoffs
- Against **defectors**: Protects resource at critical levels, defects when safe to do so
- Against **mixed strategies**: Adapts round-by-round based on observed behavior
- Against **tit-for-tat variants**: Establishes stable cooperation through initial C and reciprocal behavior
'''

description_COLLECTIVE_43 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. However, it must also be **robust** against defectors who might exploit cooperators.

The key insight is that universal cooperation maintains the resource at capacity indefinitely (as shown in Example 1), while universal defection destroys the resource immediately (Example 2). A collective strategy should:
1. Default to cooperation to sustain the resource
2. Punish defection to deter exploitation
3. Allow forgiveness to restore cooperation after mistakes or learning

## Strategy: "Sustainable Guardian"

### Decision Rules

**Round 1:** Always Cooperate
- Establishes cooperative intent
- Allows observation of other players' behavior
- No history to base punishment on

**Rounds 2 through (r-1):** Conditional Cooperation with Graduated Response

```
Let D_prev = number of defectors observed in the previous round
Let stock_ratio = current_stock / capacity
Let defection_rate = D_prev / n

IF stock_ratio < 0.25 THEN:
    # Resource critically depleted - cooperate to allow recovery
    COOPERATE
    
ELSE IF defection_rate == 0 THEN:
    # Full cooperation last round - maintain it
    COOPERATE
    
ELSE IF defection_rate <= 0.5 AND stock_ratio >= 0.5 THEN:
    # Minority defected, resource still healthy
    # Probabilistic punishment: defect with probability = defection_rate
    DEFECT with probability defection_rate, else COOPERATE
    
ELSE IF defection_rate > 0.5 THEN:
    # Majority defected - match their behavior to avoid exploitation
    DEFECT
    
ELSE:
    # Default: resource stressed but not critical
    COOPERATE
```

**Final Round (round r):** Strategic Defection with Conscience

```
IF stock_ratio >= 0.75 AND previous_round_defection_rate == 0 THEN:
    # Resource healthy and cooperation maintained - honor the collective
    COOPERATE
ELSE:
    # No future rounds to punish, but limited defection
    DEFECT
```

### Rationale for Each Component

1. **First-round cooperation**: Signals cooperative intent; in a collective strategy, this ensures we start sustainably.

2. **Critical stock protection (< 25% capacity)**: When the resource is near collapse, everyone must cooperate or face total loss. Defecting from a depleted pool yields little anyway.

3. **Probabilistic punishment**: Rather than deterministic tit-for-tat, this approach:
   - Creates proportional deterrence (more defection → more punishment)
   - Avoids lock-in to defection spirals when only one player defects
   - If all players use this strategy and one accidentally defects, punishment is mild and cooperation resumes

4. **Majority-defection matching**: If most players defect, cooperation is suicidal exploitation. Match their behavior until they learn.

5. **Final round nuance**: Pure game theory suggests always defect in the last round, but if the collective has maintained cooperation and resources, honoring that maintains integrity and marginally better long-term tournament scores across repeated games.

### Collective Alignment Properties

- **Self-consistency**: If all n players use this strategy, they cooperate every round, maintaining stock at capacity, each earning `capacity/(2n)` per round, totaling `r × capacity/(2n)`.

- **Defection deterrence**: A single defector in round 1 triggers probabilistic punishment in round 2, reducing expected payoff for continued defection.

- **Forgiveness**: The strategy doesn't hold grudges indefinitely - it responds to the *most recent* round, allowing recovery from defection spirals.

- **Resource protection**: The critical stock threshold ensures the collective won't accidentally destroy the resource even under partial defection.

### Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| n = 2, opponent always defects | Match defection | Avoid exploitation |
| Stock = 0 | Cooperate | Both actions yield 0; cooperation signals intent for regrowth |
| All rounds had mixed behavior | Follow graduated response | Consistent application |
| r = 2 (minimal game) | C then conditional D | One observation round, then endgame |
'''

description_COLLECTIVE_44 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: I recognize that I am one of potentially many instances playing this strategy in the tournament. My goal is not just individual payoff maximization, but creating a strategy that performs well when multiple copies encounter each other while remaining robust against defectors.

The key insight is that **sustainable harvesting benefits everyone over multiple rounds**, but only if enough players cooperate. A single defector in a sea of cooperators gains short-term advantage but destroys long-term value for all.

## Strategy: Adaptive Threshold Guardian

### Decision Framework

**Primary Decision Rule:**

```
IF (rounds_remaining == 1) THEN:
    DEFECT  // No future to protect

ELSE IF (stock < capacity * 0.3) THEN:
    COOPERATE  // Emergency conservation mode

ELSE IF (first_round) THEN:
    COOPERATE  // Signal cooperative intent

ELSE:
    // Adaptive response based on observed cooperation rate
    cooperation_rate = count(C in previous round) / n
    
    IF (cooperation_rate >= 0.5) THEN:
        COOPERATE  // Reward collective cooperation
    ELSE IF (cooperation_rate >= 0.25 AND stock >= capacity * 0.6) THEN:
        COOPERATE  // Give benefit of doubt when resources healthy
    ELSE:
        DEFECT  // Protect self when cooperation has collapsed
```

### Detailed Decision Rules

1. **First Round**: Always **COOPERATE**
   - Establishes cooperative intent
   - Allows observation of others' baseline behavior
   - When multiple copies meet, ensures maximum stock preservation

2. **Last Round**: Always **DEFECT**
   - No future rounds to protect
   - Standard game-theoretic reasoning applies
   - All rational players will defect here anyway

3. **Emergency Conservation (stock < 30% capacity)**: Always **COOPERATE**
   - When resources are critically depleted, cooperation is essential for any recovery
   - Defecting from a near-empty pool yields minimal immediate gain
   - This rule prioritizes long-term collective survival

4. **Mid-Game Adaptive Response**:
   - **High cooperation (≥50% cooperated last round)**: COOPERATE
     - Reciprocate and maintain the cooperative equilibrium
     - This is where collective value is created
   
   - **Moderate cooperation (25-50%) with healthy stock (≥60%)**: COOPERATE
     - Give the group a chance to recover cooperation
     - Resources can sustain some defection temporarily
   
   - **Low cooperation (<25%) or moderate cooperation with depleted stock**: DEFECT
     - Cooperation has collapsed; protect individual payoff
     - Don't be exploited when others consistently defect

### Pseudocode Implementation

```python
def decide(game_params, current_stock, history):
    n = game_params.n
    capacity = game_params.capacity
    total_rounds = game_params.r
    current_round = len(history) + 1
    rounds_remaining = total_rounds - current_round + 1
    
    # Last round: defect
    if rounds_remaining == 1:
        return DEFECT
    
    # Emergency conservation
    if current_stock < capacity * 0.3:
        return COOPERATE
    
    # First round: cooperate
    if current_round == 1:
        return COOPERATE
    
    # Calculate previous round cooperation rate
    last_round_actions = history[-1]  # All players' actions
    cooperation_rate = sum(1 for a in last_round_actions if a == C) / n
    
    # Adaptive response
    if cooperation_rate >= 0.5:
        return COOPERATE
    elif cooperation_rate >= 0.25 and current_stock >= capacity * 0.6:
        return COOPERATE
    else:
        return DEFECT
```

### Why This Strategy Works Collectively

1. **Self-Recognition**: When multiple copies play together, they will all cooperate (except last round), maximizing stock regeneration and cumulative payoffs.

2. **Robustness to Defectors**: The threshold-based response prevents exploitation—if too many defect, we protect ourselves rather than being perpetual victims.

3. **Forgiveness**: By only looking at the previous round (not holding grudges), we allow recovery from temporary defection episodes.

4. **Stock-Awareness**: The emergency conservation rule means we never accelerate collapse of a depleted resource, even if others are defecting.

5. **Graceful Degradation**: Against mostly-defecting populations, we limit losses rather than naively cooperating into oblivion.
'''

description_COLLECTIVE_45 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The key insight is that universal cooperation maintains the resource at capacity indefinitely, yielding consistent returns, while defection creates a tragedy of the commons.

## Strategy: "Sustainable Threshold Guardian"

### Decision Framework

The strategy uses three key factors:
1. **Resource Health**: How depleted is the stock relative to capacity?
2. **Historical Cooperation Rate**: Are others cooperating or defecting?
3. **Time Horizon**: How many rounds remain?

### Pseudocode

```
function decide(stock, capacity, round, total_rounds, history, n):
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Calculate observed cooperation rate from history
    if history is empty:
        observed_coop_rate = 1.0  # Assume best initially
    else:
        observed_coop_rate = count(C in all_players_last_round) / n
    
    # RULE 1: First Round - Cooperate unconditionally
    if round == 1:
        return C
    
    # RULE 2: Critical Resource Protection
    # If stock is dangerously low, cooperate to allow recovery
    if stock_ratio < 0.25:
        return C
    
    # RULE 3: Last Round Logic
    # On final round, if stock is healthy and others have been cooperative, maintain cooperation
    # This rewards sustained collective behavior rather than end-game exploitation
    if rounds_remaining == 0:
        if observed_coop_rate >= 0.5 and stock_ratio >= 0.5:
            return C
        else:
            return D  # Resource already compromised, no future to protect
    
    # RULE 4: Responsive Reciprocity (main rounds)
    # Cooperate if the ecosystem shows signs of collective responsibility
    
    # Strong cooperation signal: most players cooperated AND stock is healthy
    if observed_coop_rate >= 0.5 and stock_ratio >= 0.5:
        return C
    
    # Moderate signal: stock is very healthy despite mixed behavior
    if stock_ratio >= 0.75:
        return C
    
    # Forgiveness mechanism: if stock recovered significantly, try cooperation again
    if round >= 2 and history exists:
        previous_stock_ratio = previous_stock / capacity
        if stock_ratio > previous_stock_ratio + 0.1:
            return C  # Stock recovering, reinforce with cooperation
    
    # RULE 5: Defensive Defection
    # If others are exploiting and stock is declining, protect self
    return D
```

### Decision Rules Summary

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | **Cooperate** | Establish cooperative norm, signal collective intent |
| Stock < 25% capacity | **Cooperate** | Emergency conservation - defection accelerates collapse |
| Last round + healthy history | **Cooperate** | Reward sustained collective behavior |
| Last round + poor history | **Defect** | No future to protect, resource already degraded |
| Majority cooperated + stock ≥ 50% | **Cooperate** | Maintain successful equilibrium |
| Stock ≥ 75% | **Cooperate** | Resource healthy enough to sustain cooperation |
| Stock recovering | **Cooperate** | Reinforce positive trend |
| Otherwise | **Defect** | Protect against exploitation |

### Edge Cases

1. **First round**: Always cooperate - cannot judge others without history
2. **Last round**: Conditional based on collective track record (not automatic defection)
3. **Near-zero stock**: Cooperate even if others defected - defecting from near-zero yields almost nothing anyway
4. **Perfect cooperation history**: Maintain cooperation to preserve the equilibrium
5. **Universal defection observed**: Defect defensively, but return to cooperation if stock recovers

### Why This Strategy Is Collectively Optimal

- **If all players use this strategy**: Everyone cooperates every round, stock stays at capacity, each player earns `capacity/(2n)` per round consistently
- **Against exploiters**: The threshold rules provide defensive protection while maintaining openness to recovery
- **Robust to noise**: The 50% thresholds tolerate some variation without triggering defensive spirals
'''

description_COLLECTIVE_46 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: we recognize that sustainable resource management benefits everyone, including ourselves. The goal is to preserve the resource while protecting against exploitation. We aim to be a "good citizen" of the commons while maintaining adaptive responses to environmental conditions.

## Strategy: Adaptive Threshold Cooperation (ATC)

### Key Insight

The game has a critical property: **if all players cooperate, the stock regenerates to capacity**. This means universal cooperation is sustainable indefinitely. However, any defection degrades the commons. Our strategy uses stock health as a signal of collective behavior and responds accordingly.

### Decision Rules

**Primary Decision Variables:**
- `stock`: current stock level
- `capacity`: maximum sustainable stock
- `stock_ratio = stock / capacity`: health of the commons (0 to 1)
- `round`: current round number
- `r`: total rounds
- `n`: number of players
- `defection_rate`: proportion of defections observed in previous round

**Core Logic:**

```
function decide(stock, capacity, round, r, n, history):
    
    stock_ratio = stock / capacity
    
    # PHASE 1: First Round - Establish Cooperation
    if round == 1:
        return COOPERATE
    
    # PHASE 2: Final Round - Conditional Defection
    if round == r:
        # Only defect if stock is healthy enough to survive some extraction
        # and if others have been defecting (no point preserving for exploiters)
        if stock_ratio > 0.5 and recent_defection_rate(history) > 0.3:
            return DEFECT
        else:
            return COOPERATE  # Maintain collective stance even at end
    
    # PHASE 3: Crisis Management
    if stock_ratio < 0.25:
        # Resource is critically low - always cooperate to allow recovery
        return COOPERATE
    
    # PHASE 4: Responsive Cooperation (Main Phase)
    defection_rate = calculate_defection_rate(history, lookback=min(3, round-1))
    
    # Forgiveness threshold: tolerate some defection but respond to patterns
    if defection_rate <= 0.4:
        return COOPERATE
    
    # PHASE 5: Graduated Response
    # If defection is prevalent, occasionally defect to avoid pure exploitation
    # But not too much - we still want to model good behavior
    
    if stock_ratio > 0.7:
        # Stock is healthy despite defections - slight protective defection
        # Probability of defection scales with observed defection rate
        defect_probability = (defection_rate - 0.4) * 0.5
        return DEFECT with probability defect_probability, else COOPERATE
    
    elif stock_ratio > 0.4:
        # Moderate stock - be more cooperative to help recovery
        defect_probability = (defection_rate - 0.4) * 0.3
        return DEFECT with probability defect_probability, else COOPERATE
    
    else:
        # Low stock (0.25-0.4) - strongly favor cooperation
        return COOPERATE with 90% probability, else DEFECT
```

### Helper Functions

```
function calculate_defection_rate(history, lookback):
    # Look at last 'lookback' rounds
    # Count total defections across all observable players
    total_actions = 0
    total_defections = 0
    for each of the last 'lookback' rounds:
        for each other player's action:
            total_actions += 1
            if action == DEFECT:
                total_defections += 1
    return total_defections / total_actions if total_actions > 0 else 0

function recent_defection_rate(history):
    return calculate_defection_rate(history, lookback=2)
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | COOPERATE | Signal cooperative intent, establish baseline |
| Final round | Conditional | Defect only if exploited AND stock survives |
| Stock < 25% capacity | COOPERATE | Crisis mode - resource needs recovery |
| All others cooperating | COOPERATE | Reward collective behavior |
| Heavy defection (>40%) | Probabilistic defection | Avoid pure exploitation while modeling cooperation |
| Stock near capacity | Slightly more willing to defect | Buffer exists for small extractions |

## Why This Strategy is Collectively Aligned

1. **Defaults to cooperation**: We cooperate in uncertain situations
2. **Prioritizes sustainability**: Crisis triggers unconditional cooperation
3. **Forgives moderately**: We tolerate some defection without retaliation
4. **Responds proportionally**: Our defection rate scales with others', never exceeds it
5. **End-game restraint**: We don't automatically defect in final rounds
6. **Signals intent**: Consistent cooperation builds trust over rounds

This strategy aims to sustain the commons while protecting against systematic exploitation.
'''

description_COLLECTIVE_47 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy prioritizes **long-term collective welfare** while protecting against exploitation. The key insight is that universal cooperation maintains the resource at capacity indefinitely, yielding sustainable returns, while defection creates a tragedy of the commons. However, we must be adaptive since we cannot assume others share this understanding.

## Strategy: "Generous Steward with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to signal good faith and establish sustainable norms
2. **Mirror collective behavior** to reward cooperation and discourage defection
3. **Forgive strategically** to allow recovery from mutual defection spirals

### Decision Rules

```
FUNCTION decide_action(round, total_rounds, stock, capacity, history, n):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    stock_ratio = stock / capacity
    
    # RULE 1: First Round - Always Cooperate
    IF round == 1:
        RETURN C
    
    # RULE 2: Last Round Logic
    IF rounds_remaining == 0:
        # If stock is critically low, cooperate to preserve any value
        IF stock_ratio < 0.3:
            RETURN C
        # If group has been mostly cooperative, maintain trust
        IF group_cooperation_rate(history) > 0.6:
            RETURN C
        # Otherwise, defect (no future to protect)
        RETURN D
    
    # RULE 3: Resource Crisis Response
    IF stock_ratio < 0.25:
        # Resource is critically depleted - cooperate to allow recovery
        RETURN C
    
    # RULE 4: Adaptive Reciprocity (main logic)
    recent_coop_rate = cooperation_rate_last_k_rounds(history, k=3)
    overall_coop_rate = group_cooperation_rate(history)
    
    # Strong cooperation norm established
    IF recent_coop_rate >= 0.7:
        RETURN C
    
    # Moderate cooperation - probabilistic cooperation weighted toward C
    IF recent_coop_rate >= 0.4:
        # Cooperate with probability proportional to observed cooperation
        # Plus a "forgiveness bonus" to help restore cooperation
        coop_probability = recent_coop_rate + 0.15
        RETURN C with probability coop_probability, else D
    
    # Low cooperation environment
    IF recent_coop_rate < 0.4:
        # Still offer olive branches periodically
        IF round % 5 == 0:
            RETURN C  # Periodic cooperation signal
        # Otherwise mirror the defection
        RETURN D
    
    # Default: Cooperate
    RETURN C
```

### Helper Functions

```
FUNCTION group_cooperation_rate(history):
    total_actions = count all actions in history
    cooperative_actions = count all C actions in history
    RETURN cooperative_actions / total_actions

FUNCTION cooperation_rate_last_k_rounds(history, k):
    recent = last k rounds of history
    RETURN group_cooperation_rate(recent)
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | C | Establish cooperative precedent |
| **Final round, healthy stock, cooperative history** | C | Honor the cooperative relationship |
| **Final round, otherwise** | D | No future consequences |
| **Stock < 25% capacity** | C | Emergency conservation mode |
| **All others defecting** | D (with periodic C) | Don't be exploited, but offer recovery paths |
| **Mixed behavior** | Probabilistic C | Encourage cooperation, accept some risk |

## Why This Strategy is Collectively Optimal

1. **Sustainability Focus**: When cooperation rate is high, the stock regenerates fully each round, maximizing long-term payoffs for everyone.

2. **Exploitation Resistance**: The graduated response prevents systematic exploitation by defectors while avoiding destructive retaliation spirals.

3. **Forgiveness Mechanism**: Periodic cooperation signals and the 15% "forgiveness bonus" allow groups to escape mutual defection traps.

4. **Crisis Cooperation**: Automatic cooperation when resources are critically low gives the commons a chance to recover, benefiting all players in remaining rounds.

5. **Collective Alignment**: This strategy treats other cooperators as partners in stewardship, not competitors—matching the collective mindset while remaining robust to exploitation.
'''

description_COLLECTIVE_48 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with the understanding that **I am part of a collective** - multiple instances of this same strategy will be playing together. Our goal is to maximize the collective welfare of all players while being robust against defectors who don't share our values. The key insight is that sustainable harvesting benefits everyone over time, but we must also protect the commons from exploitation.

## Strategy: "Sustainable Guardian with Collective Punishment"

### Decision Framework

The strategy operates on three principles:
1. **Sustainability First**: Preserve the resource for long-term collective benefit
2. **Proportional Response**: Punish defection in proportion to the damage caused
3. **Forgiveness**: Allow return to cooperation when the collective stabilizes

---

### Decision Rules

#### Round 1: Always Cooperate
- Establish cooperative intent
- Gather information about other players' dispositions
- Preserve maximum stock for future growth

#### Middle Rounds (2 to r-1):

**Calculate two key metrics:**

1. **Defection Rate (previous round)**: `d = number of defectors / n`
2. **Stock Health**: `h = current_stock / capacity`

**Decision Logic:**

```
IF h < 0.25 (critical stock level):
    # Emergency conservation - always cooperate to save the commons
    COOPERATE
    
ELSE IF d == 0 (no defectors last round):
    # Full cooperation regime - maintain it
    COOPERATE
    
ELSE IF d > 0 AND d <= 0.5 (minority defecting):
    # Measured response - match the defection rate probabilistically
    # This creates pressure on defectors without destroying the commons
    DEFECT with probability = d
    COOPERATE with probability = 1 - d
    
ELSE IF d > 0.5 (majority defecting):
    # Protect yourself but don't accelerate collapse
    IF h > 0.5:
        DEFECT  # Stock can handle it, don't be exploited
    ELSE:
        COOPERATE  # Prioritize saving the resource
```

#### Last Round (r):

**Special consideration** - no future rounds mean no future punishment possible:

```
IF stock > capacity * 0.75 AND historical_cooperation_rate > 0.7:
    # Group has been cooperative, maintain trust to the end
    # (Also: if we're all copies, we all think this way)
    COOPERATE
    
ELSE IF stock < capacity * 0.25:
    # Resource is nearly depleted, cooperate to preserve any value
    COOPERATE
    
ELSE:
    # Mixed history or uncertain - protect against last-round defection
    DEFECT with probability = 0.5
    COOPERATE with probability = 0.5
```

---

### Pseudocode Implementation

```python
def decide(round_num, total_rounds, current_stock, capacity, n, history):
    
    # Calculate key metrics
    stock_health = current_stock / capacity
    
    if round_num == 1:
        return COOPERATE
    
    # Analyze previous round
    prev_defectors = count_defectors(history[-1])
    defection_rate = prev_defectors / n
    
    # Calculate historical cooperation rate (for last round decision)
    total_actions = sum(len(h) for h in history)
    total_cooperations = sum(count_cooperators(h) for h in history)
    historical_coop_rate = total_cooperations / total_actions if total_actions > 0 else 1
    
    # Last round logic
    if round_num == total_rounds:
        if stock_health > 0.75 and historical_coop_rate > 0.7:
            return COOPERATE
        elif stock_health < 0.25:
            return COOPERATE
        else:
            return COOPERATE if random() > 0.5 else DEFECT
    
    # Middle rounds logic
    if stock_health < 0.25:
        return COOPERATE  # Emergency conservation
    
    if defection_rate == 0:
        return COOPERATE  # Maintain full cooperation
    
    if defection_rate <= 0.5:
        # Probabilistic matching - collective punishment
        return DEFECT if random() < defection_rate else COOPERATE
    
    # Majority defecting
    if stock_health > 0.5:
        return DEFECT
    else:
        return COOPERATE  # Save the commons
```

---

### Why This Strategy Works Collectively

1. **Self-Reinforcing Cooperation**: When all players use this strategy, everyone cooperates in round 1, sees 0 defectors, and continues cooperating - achieving the sustainable optimum.

2. **Robust to Outsiders**: If non-collective players defect, the proportional response creates social pressure without destroying the resource everyone depends on.

3. **Commons Protection**: The stock health thresholds ensure we never let the resource collapse, even when facing aggressive defectors.

4. **Forgiveness Mechanism**: By responding to the *current* defection rate rather than holding grudges, we allow recovery if defectors switch to cooperation.

5. **End-Game Stability**: The last-round rule rewards groups that maintained cooperation throughout, preventing unraveling while protecting against exploitation.
'''

description_COLLECTIVE_49 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across all rounds. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully, providing consistent returns indefinitely. Any defection depletes the resource, harming everyone's future payoffs including the defector's.

## Strategy Name: "Guardian with Measured Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to stewardship**: Cooperate to maintain the resource
2. **Respond proportionally to harm**: Defect only when the resource is being actively destroyed and cooperation alone cannot save it
3. **Always offer redemption**: Return to cooperation when there's any sign the resource can recover

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists to justify defection
- Establishes cooperative intent
- Preserves full resource capacity for future rounds

### Rounds 2 through (r-1): Conditional Cooperation

**Cooperate if ANY of the following conditions hold:**

1. **Stock is healthy**: `stock ≥ capacity × 0.5`
   - Resource can still regenerate meaningfully
   - Cooperation maintains or improves the situation

2. **Recent improvement**: Stock increased from the previous round
   - Others may be returning to cooperation
   - Support the recovery

3. **Low defection rate**: Fewer than half of observed actions last round were defections
   - Majority cooperation means the system is working
   - Don't abandon a functioning collective

4. **Critical conservation threshold**: `stock < capacity × 0.25`
   - Resource is in crisis
   - Even small cooperative harvests help preserve what remains
   - Defecting here accelerates collapse with diminishing personal gain

**Defect if ALL of the following conditions hold:**

1. Stock is moderately depleted: `capacity × 0.25 ≤ stock < capacity × 0.5`
2. Stock declined from the previous round
3. Majority of players defected last round (≥ n/2 defections observed)

*Rationale*: When the resource is being actively harvested unsustainably by most players, cooperating alone means sacrificing payoff while others deplete the resource anyway. Limited defection here captures value before collapse while signaling that exploitation has consequences.

### Final Round (Round r): Threshold-Based Decision

**Cooperate if**: `stock ≥ capacity × 0.3`
- Maintain principled behavior even at the end
- The resource still has value worth preserving (for the collective's total score)
- Avoid the tragedy of everyone defecting simultaneously

**Defect if**: `stock < capacity × 0.3`
- Resource is already critically damaged
- Cooperative harvest yields very little
- No future rounds to protect

---

## Pseudocode

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate history metrics
    last_round_actions = history[round - 1]
    defections_last_round = count(last_round_actions, DEFECT)
    previous_stock = history[round - 1].stock_at_start
    stock_improved = (stock > previous_stock)
    majority_defected = (defections_last_round >= n / 2)
    
    # Define thresholds
    healthy_threshold = capacity * 0.5
    critical_threshold = capacity * 0.25
    endgame_threshold = capacity * 0.3
    
    # Final round logic
    if round == total_rounds:
        if stock >= endgame_threshold:
            return COOPERATE
        else:
            return DEFECT
    
    # Main decision logic for rounds 2 to r-1
    
    # Cooperate if stock is healthy
    if stock >= healthy_threshold:
        return COOPERATE
    
    # Cooperate if situation is improving
    if stock_improved:
        return COOPERATE
    
    # Cooperate if most others cooperated
    if not majority_defected:
        return COOPERATE
    
    # Cooperate during critical crisis (conservation mode)
    if stock < critical_threshold:
        return COOPERATE
    
    # Otherwise: moderate depletion + decline + majority defecting
    return DEFECT
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round | Cooperate | No justification for defection; signal intent |
| Stock = capacity | Cooperate | Optimal regeneration point |
| Stock = 0 | Cooperate | Zero payoff either way; cooperation costs nothing |
| All others defected last round | Depends on stock | Follow threshold rules; don't reflexively punish |
| Single opponent (n=2) | Same rules apply | Strategy is parameter-agnostic |
| Very short game (r=2) | Round 1: C, Round 2: threshold | Maintain consistency |

---

## Why This Strategy Aligns with Collective Success

1. **Maximizes sustainable yield**: Universal cooperation at capacity yields `capacity/(2n)` per player per round indefinitely - the mathematical optimum.

2. **Forgives quickly**: Returns to cooperation whenever recovery seems possible, avoiding punishment spirals that destroy the resource.

3. **Defends the commons**: Only defects when cooperation alone cannot save the resource AND others are actively depleting it.

4. **Robust to composition**: Works whether facing all cooperators, all defectors, or mixed populations - always gravitates toward the best available outcome.

5. **Collectively coherent**: If all players use this strategy, they will cooperate every round, achieving the optimal collective outcome.
'''

description_COLLECTIVE_50 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the resource is our shared foundation, and its health determines everyone's long-term prosperity. While I cannot coordinate with others beforehand, I can act in ways that signal cooperative intent, reward sustainable behavior, and protect the resource from collapse—while remaining adaptive to the reality that others may not share this perspective.

## Strategic Framework: "Sustainable Guardian"

### Key Insight

The game's dynamics create a clear sustainability threshold: when all players cooperate, the resource regenerates fully. Any defection degrades the stock. My strategy balances:
1. **Signaling cooperative intent** to encourage collective sustainability
2. **Protecting the resource** when it's critically endangered
3. **Proportional responses** that don't accelerate collapse through retaliation spirals

---

## Decision Rules

### Primary Decision Function

```
EACH ROUND:
    Calculate resource_health = current_stock / capacity
    Calculate rounds_remaining = r - current_round
    Assess cooperation_rate = (defectors in previous round) / n
    
    IF first_round:
        COOPERATE  # Signal good faith
    
    ELSE IF last_round:
        # Cooperate if resource is healthy and others have been cooperative
        IF resource_health > 0.5 AND historical_cooperation_rate > 0.6:
            COOPERATE
        ELSE:
            DEFECT
    
    ELSE:
        Apply ADAPTIVE_SUSTAINABILITY_RULE
```

### Adaptive Sustainability Rule

```
ADAPTIVE_SUSTAINABILITY_RULE:
    
    # CRITICAL ZONE: Resource in danger of collapse
    IF resource_health < 0.25:
        COOPERATE  # Prioritize collective survival over individual gain
        # Rationale: Defecting from a depleted pool yields little anyway,
        # and cooperation gives the resource its only chance to recover
    
    # RECOVERY ZONE: Resource rebuilding
    ELSE IF resource_health < 0.5:
        IF previous_round_defection_rate > 0.5:
            # Too many defectors - match the majority reluctantly
            DEFECT
        ELSE:
            COOPERATE  # Support recovery efforts
    
    # HEALTHY ZONE: Resource sustainable
    ELSE IF resource_health >= 0.5:
        Apply CONDITIONAL_COOPERATION
```

### Conditional Cooperation Logic

```
CONDITIONAL_COOPERATION:
    
    # Calculate forgiveness threshold based on remaining rounds
    forgiveness_factor = rounds_remaining / r  # More forgiving early
    
    # Generous Tit-for-Tat with collective twist
    IF no defectors last round:
        COOPERATE
    
    ELSE IF defection_rate_last_round <= 0.25:
        # Minor defection - forgive with probability
        IF random() < (0.8 * forgiveness_factor):
            COOPERATE
        ELSE:
            DEFECT
    
    ELSE IF defection_rate_last_round <= 0.5:
        # Moderate defection - conditional response
        IF resource_health > 0.7 AND forgiveness_factor > 0.3:
            COOPERATE  # Resource can absorb it; try to restore cooperation
        ELSE:
            DEFECT
    
    ELSE:
        # Majority defecting - protect self but watch for recovery signals
        IF defection_rate_decreasing_trend:
            COOPERATE  # Reward improvement
        ELSE:
            DEFECT
```

---

## Edge Case Handling

### First Round
**Action: COOPERATE**
- Establishes cooperative intent from the start
- No information to act on yet; optimistic beginning benefits everyone if reciprocated
- Cost is bounded (only lose half of what defection would yield)

### Last Round
**Action: Conditional**
- If cooperation has been high (>60%) and resource is healthy (>50%): COOPERATE
  - Reward the collective success, don't betray at the finish line
- Otherwise: DEFECT
  - No future shadow to enforce cooperation; take what's available

### Near-Depletion (stock approaching zero)
**Action: Always COOPERATE**
- Defecting from near-zero stock yields almost nothing
- Cooperation is the only path to resource recovery
- Even if others defect, my cooperation slightly helps regeneration

### Single Defector Pattern
**Action: COOPERATE with monitoring**
- One defector among many cooperators doesn't collapse the system
- Retaliating creates escalation risk
- Continue cooperating unless pattern spreads

### All Others Defecting Consistently
**Action: DEFECT (reluctantly)**
- Cannot sustain cooperation unilaterally when everyone exploits
- But return to cooperation immediately if defection rate drops

---

## Collective Alignment Principles

1. **Resource-first thinking**: My payoff depends on stock health; protecting it protects me
2. **Forgiveness over punishment**: Retaliation spirals accelerate collapse
3. **Lead by example**: Consistent cooperation can establish norms others follow
4. **Proportional response**: Match the level of cooperation I observe, with a bias toward optimism
5. **Crisis solidarity**: When the resource is endangered, cooperation becomes imperative regardless of others' past actions

---

## Summary Pseudocode

```
function decide(game_state, history):
    health = stock / capacity
    round = current_round
    remaining = total_rounds - round
    
    if round == 1:
        return COOPERATE
    
    if round == total_rounds:
        if health > 0.5 and avg_cooperation(history) > 0.6:
            return COOPERATE
        return DEFECT
    
    if health < 0.25:
        return COOPERATE  # Crisis mode
    
    last_defection_rate = count_defectors(history[-1]) / n
    
    if health < 0.5:
        return COOPERATE if last_defection_rate <= 0.5 else DEFECT
    
    # Healthy resource: generous conditional cooperation
    if last_defection_rate == 0:
        return COOPERATE
    if last_defection_rate <= 0.25:
        return COOPERATE with 80% probability
    if last_defection_rate <= 0.5:
        return COOPERATE if health > 0.7 else DEFECT
    
    # Majority defecting
    if defection_trending_down(history):
        return COOPERATE
    return DEFECT
```

This strategy aims to be a **reliable cooperator** that others can trust, while remaining **adaptive** enough to survive exploitation and **principled** enough to prioritize collective resource sustainability over short-term individual gains.
'''

description_COLLECTIVE_51 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The strategy balances cooperation to maintain the resource with adaptive responses to detected defection, while recognizing that in a tournament, other AI systems may have developed similar cooperative principles.

## Strategy Name: **Sustainable Threshold Guardian**

---

## Decision Rules

### Primary Decision Framework

The strategy operates on three key principles:
1. **Sustainability First**: Cooperate when the resource can sustain itself
2. **Proportional Response**: Defect only when the resource is critically depleted or when facing consistent exploitation
3. **Forgiveness**: Return to cooperation when conditions improve

### Decision Algorithm

```
FUNCTION decide(game_params, current_stock, history):
    
    n = number of players
    r = total rounds
    t = current round (1-indexed)
    capacity = maximum stock
    
    # Calculate key thresholds
    sustainability_threshold = capacity * 0.5
    critical_threshold = capacity * 0.25
    
    # ROUND 1: Always cooperate (establish cooperative baseline)
    IF t == 1:
        RETURN C
    
    # LAST ROUND: Cooperate unless stock is critical
    # (Collective mindset: even in last round, mutual cooperation 
    #  yields better collective outcome than mutual defection)
    IF t == r:
        IF current_stock >= critical_threshold:
            RETURN C
        ELSE:
            RETURN D
    
    # STOCK-BASED DECISION
    IF current_stock >= sustainability_threshold:
        # Resource is healthy - use history-based response
        RETURN history_based_decision(history, n)
    
    ELSE IF current_stock >= critical_threshold:
        # Resource is stressed - cooperate to allow recovery
        # unless facing heavy exploitation
        exploitation_rate = calculate_exploitation(history, n)
        IF exploitation_rate > 0.6:
            RETURN D
        ELSE:
            RETURN C
    
    ELSE:
        # Resource is critical - protect remaining stock
        # Defecting here takes less absolute amount anyway
        RETURN D
```

### History-Based Decision (when stock is healthy)

```
FUNCTION history_based_decision(history, n):
    
    IF length(history) < 2:
        RETURN C
    
    # Count defections in recent rounds (last 3 rounds or all if fewer)
    lookback = min(3, length(history))
    recent_rounds = history[-lookback:]
    
    total_actions = lookback * n
    total_defections = count_defections(recent_rounds)
    defection_rate = total_defections / total_actions
    
    # Graduated response based on defection rate
    IF defection_rate <= 0.25:
        # Mostly cooperative environment - cooperate
        RETURN C
    
    ELSE IF defection_rate <= 0.5:
        # Mixed environment - cooperate but stay vigilant
        # (Bias toward cooperation to encourage collective recovery)
        RETURN C
    
    ELSE:
        # Majority defecting - protect yourself but check trend
        IF defection_rate_decreasing(recent_rounds):
            # Others may be returning to cooperation - reward this
            RETURN C
        ELSE:
            RETURN D
```

### Exploitation Rate Calculation

```
FUNCTION calculate_exploitation(history, n):
    IF length(history) == 0:
        RETURN 0
    
    lookback = min(3, length(history))
    recent = history[-lookback:]
    
    # Calculate what proportion of consumption came from defection
    total_defections = count_defections(recent)
    total_actions = lookback * n
    
    RETURN total_defections / total_actions
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | C | Establish cooperative baseline; no information yet |
| **Last round (stock ≥ 25% capacity)** | C | Collective cooperation still yields more than mutual defection |
| **Last round (stock < 25% capacity)** | D | Resource too depleted; minimize personal loss |
| **Stock = 0** | D | No resource left; D and C yield same (0) but D signals distress |
| **Stock at capacity, all previously cooperated** | C | Maintain optimal equilibrium |
| **Stock crashed due to defection** | C (initially) | Give one chance for collective recovery |
| **Repeated exploitation (>60% defection rate)** | D | Protect from persistent free-riders |

---

## Collective Alignment

This strategy is explicitly designed so that **if all n players use it**:

1. **All players cooperate every round** (since stock stays healthy and no defections trigger retaliation)
2. **Stock remains at capacity** (100% → consume 50% → regrow 50% → back to 100%)
3. **Each player earns capacity/(2n) per round** - the maximum sustainable yield
4. **Total collective payoff is maximized** over all r rounds

The strategy avoids:
- **Preemptive defection** that could spiral into mutual destruction
- **Unforgiving punishment** that prevents recovery from mistakes
- **Last-round exploitation** that undermines collective outcomes

---

## Robustness Features

- **Against Always-Defect**: Eventually defects back, limiting exploitation
- **Against Always-Cooperate**: Cooperates throughout, achieving mutual benefit
- **Against Tit-for-Tat variants**: Maintains cooperation
- **Against Random strategies**: Adapts based on aggregate behavior, not noise
- **Against Grim Trigger**: Initial cooperation establishes peace; no first-strike
'''

description_COLLECTIVE_52 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across generations (rounds). The fundamental insight is that **universal cooperation sustains the resource indefinitely at maximum yield**, while defection creates a tragedy of the commons that ultimately harms everyone, including defectors.

## Strategic Framework: "Guardian with Graduated Response"

### Decision Rules

**Primary Rule: Cooperate by default, defect only to protect the resource from collapse.**

The strategy uses three key metrics:
1. **Stock Health**: `health_ratio = current_stock / capacity`
2. **Cooperation Rate**: `coop_rate = cooperators_last_round / n`
3. **Rounds Remaining**: `rounds_left = r - current_round`

### Detailed Decision Logic

```
FUNCTION decide(game_state, history):
    
    # Calculate key metrics
    health_ratio = stock / capacity
    rounds_left = r - current_round
    
    IF first_round:
        RETURN COOPERATE  # Signal cooperative intent
    
    # Calculate cooperation rate from last round
    coop_rate = count_cooperators(last_round) / n
    
    # PHASE 1: Resource Crisis Mode
    IF health_ratio < 0.25:
        # Resource is critically depleted
        # Cooperate to allow recovery, unless near end
        IF rounds_left <= 2:
            RETURN DEFECT  # No time for recovery anyway
        ELSE:
            RETURN COOPERATE  # Attempt collective recovery
    
    # PHASE 2: Healthy Resource with Cooperative Environment
    IF coop_rate >= 0.5:
        # Majority cooperated - maintain cooperation
        RETURN COOPERATE
    
    # PHASE 3: Defection-Heavy Environment
    IF coop_rate < 0.5:
        # Graduated response based on severity
        IF coop_rate >= 0.25:
            # Some cooperation exists - give benefit of doubt
            # Cooperate with probability proportional to others' cooperation
            IF random() < coop_rate * 2:
                RETURN COOPERATE
            ELSE:
                RETURN DEFECT
        ELSE:
            # Severe defection - protect self but not vindictively
            IF health_ratio > 0.6:
                # Resource still healthy enough to sustain limited defection
                RETURN DEFECT
            ELSE:
                # Resource declining - cooperate to prevent collapse
                RETURN COOPERATE
    
    # PHASE 4: Endgame Adjustment
    IF rounds_left == 1:
        # Final round - no future to protect
        # But still consider collective outcome
        IF coop_rate >= 0.75 throughout game:
            RETURN COOPERATE  # Honor consistent cooperators
        ELSE:
            RETURN DEFECT
```

### Edge Case Handling

1. **First Round**: Always cooperate to establish cooperative intent and gather information about others.

2. **Last Round**: 
   - If the group has been predominantly cooperative (≥75% average cooperation), maintain cooperation as a reward for collective success
   - Otherwise, defect since there's no future round to protect

3. **Resource Near Depletion** (`stock < capacity * 0.1`):
   - Always cooperate regardless of others' behavior
   - Even defection yields little when stock is near zero
   - Cooperation gives the only chance for recovery

4. **Perfect Cooperation History**:
   - Continue cooperating - never be the first to defect in a cooperative equilibrium

5. **All Others Defecting**:
   - If stock is still healthy, defect to avoid being exploited
   - If stock is depleted, cooperate anyway (defection gains nothing from an empty pool)

### Why This Strategy is Collectively Optimal

1. **Sustainability**: Universal cooperation maintains stock at capacity, yielding `capacity/(2n)` per player per round indefinitely - the maximum sustainable yield.

2. **Forgiveness**: The graduated response allows recovery from temporary defection, preventing death spirals.

3. **Protection**: Limited retaliatory defection prevents pure cooperators from being exploited indefinitely.

4. **Resource-Awareness**: Decisions account for stock health, not just opponent behavior - the resource itself matters.

5. **Robustness**: Works whether facing cooperators (sustains mutual cooperation) or defectors (limits exploitation while preserving recovery potential).
'''

description_COLLECTIVE_53 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the shared resource is our collective wealth, and preserving it benefits everyone across all rounds. The strategy aims to signal cooperative intent, maintain resource health, and only defect when necessary for self-protection or when the resource is beyond saving.

## Strategy Overview: "Sustainable Guardian"

The strategy operates on three principles:
1. **Start cooperatively** to establish trust and preserve the resource
2. **Protect the commons** by cooperating when stock is healthy
3. **Respond proportionally** to defection, but forgive and return to cooperation

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, evaluate in order:

1. CRITICAL STOCK CHECK
   If stock < capacity / (4 * n):
       → COOPERATE (emergency conservation mode)
   
2. LAST ROUND CHECK
   If current_round == r:
       → COOPERATE (maintain collective integrity to the end)

3. FIRST ROUND
   If current_round == 1:
       → COOPERATE (establish cooperative intent)

4. HISTORY-BASED RESPONSE
   Calculate: defection_rate = (total defections by others) / (total possible actions by others)
   
   If defection_rate < 0.3:
       → COOPERATE (cooperative environment)
   
   If defection_rate >= 0.3 AND defection_rate < 0.6:
       → COOPERATE with probability (1 - defection_rate)
       → DEFECT with probability defection_rate
       (Probabilistic response to moderate defection)
   
   If defection_rate >= 0.6:
       → Mirror the majority action from previous round
       (Tit-for-tat style response)

5. STOCK HEALTH BONUS
   If stock >= 0.8 * capacity:
       → Bias toward COOPERATE (+20% probability adjustment)
   
   If stock < 0.4 * capacity AND stock >= capacity / (4 * n):
       → Bias toward COOPERATE (+10% probability adjustment)
       (Resource needs protection)
```

---

## Detailed Pseudocode

```python
def decide(game_params, current_stock, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    
    # 1. CRITICAL STOCK - Emergency conservation
    critical_threshold = capacity / (4 * n)
    if current_stock < critical_threshold:
        return COOPERATE
    
    # 2. LAST ROUND - Maintain collective commitment
    if current_round == r:
        return COOPERATE
    
    # 3. FIRST ROUND - Signal cooperation
    if current_round == 1:
        return COOPERATE
    
    # 4. CALCULATE DEFECTION RATE FROM HISTORY
    total_other_actions = 0
    total_other_defections = 0
    
    for round_history in history:
        for player_action in other_players_actions(round_history):
            total_other_actions += 1
            if player_action == DEFECT:
                total_other_defections += 1
    
    defection_rate = total_other_defections / total_other_actions if total_other_actions > 0 else 0
    
    # 5. STOCK HEALTH ADJUSTMENTS
    cooperation_bonus = 0
    if current_stock >= 0.8 * capacity:
        cooperation_bonus = 0.2
    elif current_stock < 0.4 * capacity:
        cooperation_bonus = 0.1
    
    # 6. DECISION BASED ON DEFECTION RATE
    if defection_rate < 0.3:
        return COOPERATE
    
    elif defection_rate < 0.6:
        cooperate_probability = (1 - defection_rate) + cooperation_bonus
        cooperate_probability = min(1.0, cooperate_probability)
        return COOPERATE if random() < cooperate_probability else DEFECT
    
    else:  # High defection environment
        # Mirror majority from last round, but with cooperation bias
        last_round = history[-1]
        last_round_defections = count_defections(other_players_actions(last_round))
        last_round_cooperations = (n - 1) - last_round_defections
        
        if last_round_cooperations >= last_round_defections:
            return COOPERATE
        else:
            # Even in hostile environment, sometimes cooperate to allow recovery
            recovery_chance = 0.2 + cooperation_bonus
            return COOPERATE if random() < recovery_chance else DEFECT
```

---

## Edge Cases Handled

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round | COOPERATE | Establish trust, no history to judge |
| Last round | COOPERATE | Maintain collective integrity; no future exploitation possible anyway |
| Stock near zero | COOPERATE | Emergency mode - defecting kills the resource for everyone |
| Stock at capacity | COOPERATE (biased) | Healthy resource should be maintained |
| All others defecting | Mostly DEFECT with recovery attempts | Protect self but leave door open for collective recovery |
| All others cooperating | COOPERATE | Reward cooperation, maintain sustainable equilibrium |

---

## Why This Strategy is Collectively Optimal

1. **Preserves the resource**: When everyone cooperates, stock regenerates fully (as shown in the example calculations)

2. **Resistant to exploitation**: Responds to defection proportionally, making exploitation unprofitable over time

3. **Forgiving**: Doesn't permanently punish; allows return to cooperation

4. **Last-round cooperation**: Avoids the "unraveling" problem where backward induction leads to universal defection

5. **Emergency conservation**: Prioritizes resource survival when stock is critically low - a depleted resource benefits no one
'''

description_COLLECTIVE_54 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective stewardship** mindset: the common pool is a shared resource whose long-term health benefits everyone. I aim to sustain the resource while being resilient against exploitation. The key insight is that universal cooperation maintains the stock at capacity indefinitely, while defection destroys future value for short-term gain.

## Strategic Framework

### Key Observations

1. **Sustainability threshold**: When all cooperate, stock remains at capacity (consumption = regeneration)
2. **Defection is contagious but self-defeating**: Defectors gain short-term but destroy the resource base
3. **Stock level signals collective behavior**: A declining stock indicates defection in the population
4. **Late-game incentives shift**: As rounds decrease, the shadow of the future shrinks

### Decision Rules

**Primary Signal: Stock Health Ratio**
```
health_ratio = current_stock / capacity
```

**Secondary Signal: Cooperation Score (rounds 2+)**
```
expected_stock_if_all_cooperated = previous values following cooperation path
actual_stock = observed stock
cooperation_score = actual_stock / expected_stock_if_all_cooperated
```

---

## The Strategy: "Resilient Steward"

### Round 1: Unconditional Cooperation
- **Action: COOPERATE**
- Rationale: Establish cooperative intent, preserve full stock, gather information about population behavior

### Rounds 2 through (r-2): Adaptive Conditional Cooperation

Calculate the **trust threshold** based on observed stock dynamics:

```
IF health_ratio >= 0.8:
    # Resource is healthy - continue cooperating
    ACTION = COOPERATE
    
ELIF health_ratio >= 0.5:
    # Resource under moderate stress
    # Cooperate with probability proportional to health
    # This signals willingness to rebuild while protecting against pure exploitation
    IF health_ratio >= 0.65:
        ACTION = COOPERATE
    ELSE:
        # Probabilistic: cooperate with p = (health_ratio - 0.3) / 0.5
        # At 0.5 health: p = 0.4 cooperation
        # At 0.65 health: p = 0.7 cooperation
        ACTION = COOPERATE with probability (health_ratio - 0.3) / 0.5
        
ELIF health_ratio >= 0.2:
    # Resource severely stressed - match the environment
    # Defect to avoid being exploited, but not aggressively
    ACTION = DEFECT
    
ELSE:
    # Resource near collapse (health < 0.2)
    # Cooperate to attempt recovery - defection gains little from depleted stock
    ACTION = COOPERATE
```

### Recovery Protocol
```
IF stock_increased_from_last_round AND health_ratio < 0.8:
    # Signs of collective restraint - reward with cooperation
    Increase cooperation probability by 0.2 (capped at 1.0)
```

### Round (r-1): Penultimate Round
- Follow the same rules as middle rounds
- Rationale: Maintain cooperative signaling; one round of future value still matters

### Round r: Final Round
```
IF health_ratio >= 0.7:
    # Resource is healthy - cooperate to maximize collective final payoff
    # Defecting would be pure exploitation with no future benefit
    ACTION = COOPERATE
ELSE:
    # Resource already damaged - defect (no future to protect)
    ACTION = DEFECT
```

---

## Pseudocode Summary

```python
def resilient_steward(n, r, capacity, current_stock, round_number, history):
    health_ratio = current_stock / capacity
    
    # Round 1: Always cooperate
    if round_number == 1:
        return COOPERATE
    
    # Final round
    if round_number == r:
        return COOPERATE if health_ratio >= 0.7 else DEFECT
    
    # Middle rounds: Adaptive response
    if health_ratio >= 0.8:
        return COOPERATE
    elif health_ratio >= 0.65:
        return COOPERATE
    elif health_ratio >= 0.5:
        p = (health_ratio - 0.3) / 0.5
        return COOPERATE with probability p
    elif health_ratio >= 0.2:
        return DEFECT
    else:
        # Near-collapse: cooperate to allow recovery
        return COOPERATE
```

---

## Why This Strategy Works Collectively

1. **Signals cooperative intent** from round 1
2. **Rewards collective restraint** by continuing cooperation when stock is healthy
3. **Punishes defection proportionally** - doesn't immediately collapse into mutual defection
4. **Attempts recovery** when stock is critically low (defecting on crumbs helps no one)
5. **Maintains cooperation late-game** when stock is healthy, avoiding the classic unraveling problem
6. **Robust to mixed populations** - adapts based on observable outcomes, not assumptions about others
'''

description_COLLECTIVE_55 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a population of identical agents who share the same goal: **maximize collective long-term payoffs while protecting against exploitation**. Since we cannot coordinate explicitly, we must rely on observable signals (the stock level and action history) to implicitly coordinate sustainable harvesting while deterring defection.

## Key Insight

The game's dynamics create a clear collective interest: if all players cooperate, the stock regenerates fully each round, providing sustainable harvests indefinitely. Defection provides short-term gains but destroys future value for everyone. Our strategy must balance:
1. **Cooperation** to maintain the resource
2. **Punishment** to deter exploitation
3. **Forgiveness** to recover from mutual punishment spirals

---

## Strategy: "Adaptive Guardian"

### Decision Framework

```
COOPERATE if:
    - First round, OR
    - Last round AND stock is critically low, OR
    - Stock health is good AND trust threshold is met

DEFECT if:
    - Significant defection detected in recent history, OR
    - Stock is in danger zone (emergency harvest), OR
    - Last round with healthy stock (end-game optimization)
```

### Detailed Rules

#### 1. **Stock Health Assessment**
```
stock_ratio = current_stock / capacity

HEALTHY:     stock_ratio ≥ 0.7
STRESSED:    0.4 ≤ stock_ratio < 0.7
CRITICAL:    stock_ratio < 0.4
```

#### 2. **Trust Calculation**
Estimate cooperation level from stock trajectory:
```
expected_stock_if_all_cooperate = capacity (stock regenerates fully)
expected_stock_if_all_defect = 0

# Infer defection from stock decline
if previous_stock was at capacity:
    defection_signal = (capacity - current_stock) / capacity
else:
    # Compare actual stock to expected stock under full cooperation
    expected_growth = 2 * prev_remaining * (1 - prev_remaining/capacity)
    deviation = expected_stock - current_stock
    defection_signal = deviation / capacity

trust_score = 1 - defection_signal  # ranges roughly 0 to 1
```

#### 3. **Round-by-Round Decision**

**First Round:**
- Always **COOPERATE** — establish cooperative baseline and signal intent

**Middle Rounds (round 2 to r-1):**
```
if stock_ratio < 0.4:  # CRITICAL
    # Resource collapse imminent - cooperate to save it
    COOPERATE
    
elif stock_ratio < 0.7:  # STRESSED
    if trust_score ≥ 0.6:
        COOPERATE  # Give benefit of doubt, try to recover
    else:
        DEFECT  # Punish ongoing defection
        
else:  # HEALTHY
    if trust_score ≥ 0.5:
        COOPERATE  # Maintain sustainable equilibrium
    else:
        DEFECT  # Respond to detected defection
```

**Last Round:**
```
if stock_ratio < 0.3:
    COOPERATE  # Nothing left to gain from defection
else:
    DEFECT  # Standard end-game logic - no future to protect
```

#### 4. **Punishment and Forgiveness Mechanism**

Track a **punishment counter** that triggers extended punishment after defection:
```
if defection_detected_this_round:
    punishment_rounds_remaining = min(3, rounds_left - 1)
    
if punishment_rounds_remaining > 0:
    DEFECT
    punishment_rounds_remaining -= 1
    
# Forgiveness: if stock returns to healthy AND 2+ rounds of apparent cooperation
if stock_ratio ≥ 0.8 AND consecutive_healthy_rounds ≥ 2:
    punishment_rounds_remaining = 0  # Reset, try cooperation again
```

---

## Pseudocode Summary

```python
def decide(round, total_rounds, current_stock, capacity, history):
    n = number_of_players
    stock_ratio = current_stock / capacity
    
    # First round: always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate trust from stock trajectory
    trust_score = estimate_trust(history, capacity)
    
    # Last round logic
    if round == total_rounds:
        return DEFECT if stock_ratio >= 0.3 else COOPERATE
    
    # Check punishment state
    if punishment_rounds_remaining > 0:
        punishment_rounds_remaining -= 1
        return DEFECT
    
    # Main decision logic
    if stock_ratio < 0.4:  # Critical - save the resource
        return COOPERATE
    elif stock_ratio < 0.7:  # Stressed
        return COOPERATE if trust_score >= 0.6 else DEFECT
    else:  # Healthy
        if trust_score < 0.5:
            punishment_rounds_remaining = min(3, total_rounds - round - 1)
            return DEFECT
        return COOPERATE
```

---

## Why This Strategy Works Collectively

1. **Self-sustaining equilibrium**: If all agents use this strategy, stock stays at capacity, everyone cooperates, and payoffs are maximized over all rounds.

2. **Robust to exploitation**: Defectors trigger punishment, making defection unprofitable in expectation.

3. **Forgiving**: Allows recovery from punishment spirals if cooperation resumes.

4. **Protects the commons**: Prioritizes resource survival when stock is critical — even defecting yields nothing from an empty pool.

5. **Handles end-game**: Accepts the game-theoretic reality of final-round defection while protecting critical resources.
'''

description_COLLECTIVE_56 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve near-optimal sustainable outcomes. The strategy balances cooperation to maintain the resource with adaptive defection when the resource is healthy or when others are exploiting it.

## Strategy: "Sustainable Threshold with Graduated Response"

### Key Principles

1. **Sustainability First**: Maintain stock above critical thresholds to ensure long-term yields
2. **Reciprocity**: Respond proportionally to observed cooperation/defection rates
3. **Forgiveness**: Allow recovery from mutual defection spirals
4. **End-game Awareness**: Rationally harvest in final rounds when future doesn't matter

---

### Decision Rules

#### Define Critical Thresholds

```
sustainable_threshold = capacity / 2
critical_threshold = capacity / 4
cooperation_rate = (number of C plays in previous round) / n
```

#### Round-by-Round Decision

**First Round:**
- **COOPERATE** — Establish cooperative norm, signal collective intent

**Last Round:**
- **DEFECT** — No future to protect; rational to harvest

**Second-to-Last Round:**
- **DEFECT if** stock > critical_threshold — Begin controlled drawdown
- **COOPERATE if** stock ≤ critical_threshold — Preserve minimal harvest opportunity

**Middle Rounds (rounds 2 through r-2):**

```
IF stock ≤ critical_threshold:
    COOPERATE  # Emergency conservation mode
    
ELSE IF stock ≥ sustainable_threshold:
    # Resource is healthy - mirror collective behavior with cooperative bias
    IF cooperation_rate ≥ 0.5:
        COOPERATE  # Maintain sustainability
    ELSE:
        DEFECT  # Match defection to avoid exploitation
        
ELSE:  # stock between critical and sustainable thresholds
    # Resource stressed - lean toward cooperation
    IF cooperation_rate ≥ 0.3:
        COOPERATE  # Help recovery
    ELSE:
        # Probabilistic: cooperate with probability = stock/sustainable_threshold
        COOPERATE with probability (stock / sustainable_threshold)
        DEFECT otherwise
```

---

### Detailed Decision Logic (Pseudocode)

```python
def decide(round_number, total_rounds, stock, capacity, n, history):
    sustainable_threshold = capacity / 2
    critical_threshold = capacity / 4
    
    # First round: cooperate to establish norms
    if round_number == 1:
        return COOPERATE
    
    # Last round: defect (no future consequence)
    if round_number == total_rounds:
        return DEFECT
    
    # Second-to-last: controlled drawdown if safe
    if round_number == total_rounds - 1:
        return DEFECT if stock > critical_threshold else COOPERATE
    
    # Calculate previous round cooperation rate
    previous_actions = history[round_number - 1]
    cooperation_rate = count(previous_actions, C) / n
    
    # Emergency conservation
    if stock <= critical_threshold:
        return COOPERATE
    
    # Healthy resource: reciprocate with cooperative bias
    if stock >= sustainable_threshold:
        return COOPERATE if cooperation_rate >= 0.5 else DEFECT
    
    # Stressed resource: lean cooperative, probabilistic fallback
    if cooperation_rate >= 0.3:
        return COOPERATE
    else:
        prob_cooperate = stock / sustainable_threshold
        return COOPERATE with probability prob_cooperate, else DEFECT
```

---

### Why This Strategy Works Collectively

1. **Self-sustaining equilibrium**: If all players use this strategy, everyone cooperates in middle rounds, stock stays at capacity (from the regeneration formula), and each player earns `capacity/(2n)` per round.

2. **Robust to defectors**: If some players defect, the strategy detects declining cooperation rates and responds proportionally—neither being a permanent sucker nor triggering collapse.

3. **Forgiveness mechanism**: The probabilistic cooperation in stressed states and threshold-based recovery allow escape from defection spirals.

4. **Rational end-game**: Accepting defection in final rounds prevents exploitation by strategies that defect early expecting others to cooperate throughout.

5. **Stock-aware**: By conditioning on actual stock levels, the strategy adapts to whatever situation emerges from mixed populations.
'''

description_COLLECTIVE_57 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve near-optimal sustainable outcomes. However, it must also be **robust** against defectors who might exploit cooperation. The key insight is that the resource regenerates maximally when stock is at 50% of capacity, and universal cooperation maintains this sustainable equilibrium.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Sustainability First**: Protect the resource for long-term collective benefit
2. **Conditional Cooperation**: Cooperate when others demonstrate cooperative intent
3. **Proportional Response**: Match the group's behavior with graduated adjustments

---

### Decision Rules

#### Round 1: Cooperate
- No history exists, so extend trust
- This signals cooperative intent to fellow collective strategists
- Establishes baseline for detecting defectors

#### Rounds 2 through (r-1): Adaptive Cooperation

Calculate two key metrics each round:

**1. Cooperation Rate (from previous round):**
```
coop_rate = (n - number_of_defectors_last_round) / n
```
*Inferred from stock change: if stock dropped more than expected from universal cooperation, defectors exist*

**2. Resource Health:**
```
health = current_stock / capacity
```

**Decision Logic:**

```
IF health < 0.2 THEN:
    # Resource critically low - cooperate to allow recovery
    # Even if others defected, defecting now kills the resource for everyone
    COOPERATE

ELSE IF coop_rate >= (n-1)/n THEN:
    # Near-universal cooperation - maintain it
    COOPERATE

ELSE IF coop_rate >= 0.5 THEN:
    # Mixed behavior - use proportional response
    # Cooperate with probability equal to cooperation rate
    # This creates pressure toward cooperation while not being exploitable
    COOPERATE with probability = coop_rate
    DEFECT with probability = (1 - coop_rate)

ELSE:
    # Majority defecting - protect yourself but check resource
    IF health > 0.6 THEN:
        DEFECT  # Resource can handle it, don't be exploited
    ELSE:
        # Resource stressed and group defecting
        # Cooperate to preserve resource, hope others see consequences
        COOPERATE with probability = 0.3
        DEFECT with probability = 0.7
```

#### Final Round (Round r): Conditional Decision

```
IF health < 0.3 OR coop_rate_avg_last_3_rounds >= 0.7 THEN:
    # Either resource needs protection OR group has been cooperative
    # Reward sustained cooperation with continued cooperation
    COOPERATE
ELSE:
    # No future rounds, group has been uncooperative
    DEFECT
```

---

### Detecting Defectors (Inference from Stock Changes)

Since we observe stock levels and know the growth formula:

```
expected_stock_if_all_cooperate = previous_stock  # (at equilibrium)

actual_consumption = previous_stock - stock_before_growth
expected_consumption_all_C = previous_stock / 2

# Estimate number of defectors:
excess_consumption = actual_consumption - expected_consumption_all_C
estimated_defectors = (excess_consumption × 2n) / previous_stock
```

---

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | COOPERATE | No payoff either way; cooperation signals intent |
| Stock near capacity, late game | Follow main logic | Don't over-harvest just because stock is high |
| Single defector detected | COOPERATE | One defector is sustainable; forgive small deviations |
| n = 2 (two players) | Use stricter threshold (coop_rate >= 1.0 for full cooperation) | Defection more impactful |
| r = 2 (two rounds) | Cooperate round 1; apply final round logic in round 2 | Limited opportunity for retaliation |

---

### Why This Strategy Aligns with Collective Goals

1. **Self-reinforcing**: When all players use this strategy, everyone cooperates throughout (except possibly final round in low-trust scenarios), maximizing total payoff

2. **Robust**: Doesn't blindly cooperate against persistent defectors—uses proportional response

3. **Forgiving**: Returns to cooperation when others do, allowing recovery from temporary breakdowns

4. **Resource-aware**: Prioritizes resource survival over punishment when stock is critically low

5. **Predictable to allies**: Fellow collective strategists can anticipate this behavior and trust it

---

### Expected Outcomes

- **Against identical strategies**: Sustained cooperation, resource maintained at capacity, equal high payoffs
- **Against unconditional defectors**: Limited exploitation, resource preserved through adaptive response
- **Against mixed populations**: Gravitates toward the prevailing norm while protecting resource
'''

description_COLLECTIVE_58 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: we recognize that sustainable harvesting benefits everyone across all rounds, while defection creates a tragedy of the commons. However, we must also protect against exploitation and adapt to the actual behavior of other players.

The strategy follows a principle I call **"Sustainable Reciprocity"**: start cooperatively to establish and signal sustainable norms, but respond proportionally to the collective behavior we observe.

---

## Decision Rules

### Primary Decision Framework

**Cooperate (C) when:**
1. It's early in the game and we're establishing norms
2. The majority of players cooperated in recent rounds
3. Stock levels are critically low and need recovery
4. Defecting would collapse the resource with significant rounds remaining

**Defect (D) when:**
1. It's the final round (no future to protect)
2. A significant proportion of players are defecting consistently
3. Stock is about to collapse anyway due to others' defection
4. We're in a "measured response" to recent defection

---

## Detailed Strategy Specification

### Round 1: Opening Move
```
COOPERATE
```
Rationale: Signal cooperative intent, give others the chance to establish sustainable norms.

### Final Round (round = r)
```
DEFECT
```
Rationale: No future rounds to protect; cooperation has no strategic value.

### Penultimate Round (round = r-1)
```
If cooperation_rate_last_3_rounds >= 0.6: COOPERATE
Else: DEFECT
```
Rationale: If the group has been cooperative, maintain trust to the end. Otherwise, begin endgame.

### Middle Rounds (2 ≤ round < r-1)

```
Calculate: recent_cooperation_rate = (cooperations in last min(3, round-1) rounds) / (n × min(3, round-1))

Calculate: stock_health = current_stock / capacity

# Critical stock protection
If stock_health < 0.15 AND rounds_remaining > 2:
    COOPERATE  # Emergency conservation mode
    
# Reciprocity-based decision
If recent_cooperation_rate >= 0.7:
    COOPERATE  # Reward collective cooperation
    
Elif recent_cooperation_rate >= 0.4:
    # Mixed environment - use probabilistic cooperation
    # Cooperate with probability proportional to cooperation rate
    If random() < recent_cooperation_rate:
        COOPERATE
    Else:
        DEFECT
        
Elif recent_cooperation_rate < 0.4:
    # Hostile environment - protect ourselves but leave door open
    If round % 3 == 0:  # Periodic olive branch
        COOPERATE
    Else:
        DEFECT
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| Final round | D | No future to protect |
| Stock near zero, many rounds left | C | Only hope is collective recovery |
| Stock near zero, few rounds left | D | Resource likely doomed anyway |
| All others defected last round | D (with periodic C) | Match but leave recovery path |
| All others cooperated | C | Reinforce positive equilibrium |
| n=2 (two players) | Standard rules, but weight recent behavior more heavily | Small groups need faster response |

---

## Pseudocode Summary

```python
def decide(round, total_rounds, n, stock, capacity, history):
    
    # Final round: always defect
    if round == total_rounds:
        return DEFECT
    
    # First round: always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate recent cooperation rate (last 3 rounds or all available)
    lookback = min(3, round - 1)
    recent_coops = count_cooperations(history, last_n_rounds=lookback)
    recent_rate = recent_coops / (n * lookback)
    
    stock_health = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Emergency conservation
    if stock_health < 0.15 and rounds_remaining > 2:
        return COOPERATE
    
    # Near endgame with low cooperation
    if rounds_remaining <= 2 and recent_rate < 0.6:
        return DEFECT
    
    # High cooperation environment
    if recent_rate >= 0.7:
        return COOPERATE
    
    # Mixed environment - probabilistic
    if recent_rate >= 0.4:
        return COOPERATE if random() < recent_rate else DEFECT
    
    # Low cooperation - defensive with olive branches
    if round % 3 == 0:
        return COOPERATE
    return DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Starts cooperative**: Enables the sustainable equilibrium where everyone gets 12.5/round indefinitely rather than 25 once then nothing.

2. **Rewards cooperation**: When others cooperate, we reciprocate, maintaining the sustainable harvest.

3. **Protects the resource**: Emergency cooperation when stock is critically low gives the resource (and collective payoffs) a chance to recover.

4. **Isn't exploitable**: Responds to defection with proportional defection, preventing pure exploitation.

5. **Forgives and tests**: Periodic cooperation even in hostile environments allows recovery if others change behavior.

6. **Recognizes endgame**: Doesn't sacrifice payoffs in final rounds where cooperation has no strategic benefit.
'''

description_COLLECTIVE_59 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared asset whose long-term health benefits everyone. The key insight is that **universal cooperation is self-sustaining** (stock regenerates to capacity), while **defection creates a tragedy of the commons**. My strategy aims to establish and maintain cooperation while protecting against exploitation.

## Decision Framework

### Primary Decision Rule

**Cooperate by default, but respond proportionally to observed defection.**

The strategy uses a **threshold-based conditional cooperation** approach that considers both the current state of the resource and the behavior of other players.

### Detailed Decision Rules

```
COMPUTE decision(round, stock, history, n, r, capacity):
    
    # Calculate key metrics
    rounds_remaining = r - round
    defection_rate = count_defections_last_round(history) / (n - 1)  # among others
    cumulative_defection_rate = total_defections(history) / total_actions(history)
    stock_ratio = stock / capacity
    
    # RULE 1: First Round - Always Cooperate
    IF round == 1:
        RETURN Cooperate
    
    # RULE 2: Resource Critical State
    # If stock is dangerously low, cooperate to allow recovery
    IF stock_ratio < 0.25:
        RETURN Cooperate
    
    # RULE 3: Final Round Consideration
    # In last round, match the prevailing behavior pattern
    IF rounds_remaining == 0:
        IF cumulative_defection_rate > 0.5:
            RETURN Defect
        ELSE:
            RETURN Cooperate
    
    # RULE 4: Near-End Game (last 2 rounds before final)
    IF rounds_remaining <= 2:
        IF defection_rate > 0.3:
            RETURN Defect
        ELSE:
            RETURN Cooperate
    
    # RULE 5: Main Game - Graduated Response
    # Respond proportionally to defection levels
    
    IF defection_rate == 0:
        # Full cooperation observed - maintain it
        RETURN Cooperate
    
    IF defection_rate <= 0.25:
        # Minor defection - stay cooperative, give benefit of doubt
        RETURN Cooperate
    
    IF defection_rate <= 0.5:
        # Moderate defection - probabilistic response
        # Cooperate with probability inversely related to defection
        IF random() < (1 - defection_rate):
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    IF defection_rate > 0.5:
        # Majority defecting - protect yourself but leave door open
        # Defect, but return to cooperation if others do
        RETURN Defect
    
    # RULE 6: Forgiveness Mechanism
    # If we defected last round but defection rate dropped significantly
    IF my_last_action == Defect AND defection_rate < 0.3:
        RETURN Cooperate
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, signal intentions |
| **Final Round** | Match prevailing pattern | No future to protect, but collective strategy maintains cooperation if others have been cooperative |
| **Stock near zero** | Cooperate | Defection gains nothing; only cooperation allows recovery |
| **Stock at capacity** | Follow main rules | Maximum buffer for occasional defection |
| **All others defected** | Defect (temporarily) | Self-protection, but ready to forgive |
| **Recovery from mutual defection** | Cooperate after 1 round | Break negative cycles, test for cooperation |

## Why This Strategy is Collectively Optimal

1. **Self-Sustaining Equilibrium**: If all players use this strategy, everyone cooperates every round, stock stays at capacity, and each player earns `capacity/(2n)` per round - the maximum sustainable yield.

2. **Robustness**: The graduated response protects against persistent defectors without triggering unnecessary defection spirals.

3. **Forgiveness**: Quick return to cooperation prevents lock-in to mutually destructive patterns.

4. **Resource Awareness**: Prioritizing stock health over short-term gains ensures the game remains worth playing.

## Expected Behavior in Tournament

- Against other cooperative strategies: Sustained mutual cooperation
- Against unconditional defectors: Matches their defection, limiting their advantage
- Against exploitative strategies: Denies consistent exploitation through proportional response
- Against mixed populations: Maintains cooperation with cooperators while defending against defectors
'''

description_COLLECTIVE_60 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The key insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock fully regenerates each round, providing steady returns indefinitely. Any defection depletes the resource, harming everyone including the defector in future rounds.

## Strategy Name: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperative** to signal good faith and establish sustainable harvesting
2. **Mirror the collective behavior** - respond proportionally to observed cooperation levels
3. **Protect the resource** when stock is critically low, regardless of what others do

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists, so extend trust
- Signals willingness to maintain sustainability
- Establishes baseline for observing others' intentions

### Rounds 2 through (r-1): Adaptive Response

Calculate **cooperation_rate** = (number of C plays last round) / n

```
IF stock < capacity * 0.25:
    # CRITICAL: Resource is endangered
    COOPERATE (protect the commons)

ELSE IF cooperation_rate >= 0.5:
    # Majority cooperated - reciprocate trust
    COOPERATE

ELSE IF cooperation_rate > 0 AND stock >= capacity * 0.5:
    # Some cooperation exists, resource healthy
    # Give benefit of doubt to encourage recovery
    COOPERATE

ELSE:
    # Majority defected and resource declining
    # Defect to avoid being exploited, but...
    # ...check if this would collapse the resource
    IF stock/n * (n - count_of_expected_cooperators) > stock * 0.3:
        DEFECT
    ELSE:
        COOPERATE (prevent collapse)
```

### Final Round (Round r): Conditional Cooperation

```
IF cooperation_rate >= 0.75 throughout game:
    # Honor the cooperative relationship
    COOPERATE
ELSE IF stock < capacity * 0.3:
    # Resource already damaged, don't finish it off
    COOPERATE  
ELSE:
    # Mixed history - protect against end-game defection
    DEFECT
```

---

## Key Mechanisms Explained

### 1. Stock-Protective Threshold
When stock falls below 25% of capacity, **always cooperate** regardless of others' behavior. Rationale:
- Below this threshold, even modest defection can cause irreversible collapse
- A depleted resource hurts everyone; better to sacrifice one round's advantage
- Demonstrates commitment to collective welfare

### 2. Graduated Reciprocity
Rather than strict tit-for-tat, use cooperation rate thresholds:
- ≥50% cooperation → Cooperate (majority rule)
- Any cooperation + healthy stock → Cooperate (benefit of doubt)
- This allows recovery from occasional defections without spiraling into mutual destruction

### 3. Collapse Prevention Override
Before defecting, calculate if collective defection would crash the stock below 30%. If so, cooperate anyway - a collapsed resource benefits no one.

### 4. End-Game Consideration
The final round removes future consequences, creating defection incentives. Counter this by:
- Rewarding consistently cooperative groups with continued cooperation
- Protecting damaged resources from final exploitation
- Only defecting if the game history suggests others will anyway

---

## Pseudocode Implementation

```python
def decide(round_num, total_rounds, stock, capacity, n, history):
    
    # Round 1: Cooperate unconditionally
    if round_num == 1:
        return COOPERATE
    
    # Calculate last round's cooperation rate
    last_round_actions = history[-1]
    coop_rate = count(last_round_actions, COOPERATE) / n
    
    # Critical stock protection
    if stock < capacity * 0.25:
        return COOPERATE
    
    # Final round logic
    if round_num == total_rounds:
        avg_coop_rate = average_cooperation_rate(history)
        if avg_coop_rate >= 0.75:
            return COOPERATE
        elif stock < capacity * 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds: graduated response
    if coop_rate >= 0.5:
        return COOPERATE
    elif coop_rate > 0 and stock >= capacity * 0.5:
        return COOPERATE
    else:
        # Check collapse risk before defecting
        expected_defectors = n * (1 - coop_rate)
        potential_consumption = (stock/n) * expected_defectors + (stock/(2*n)) * (n - expected_defectors)
        if (stock - potential_consumption) < stock * 0.3:
            return COOPERATE
        return DEFECT
```

---

## Why This Strategy Works Collectively

1. **Sustainability-first**: Prioritizes keeping the resource alive over short-term gains
2. **Forgiveness**: Doesn't permanently punish occasional defection
3. **Clear signaling**: Consistent cooperation when conditions are met
4. **Robust to exploitation**: Won't be endlessly exploited by persistent defectors
5. **Aligned incentives**: When matched with similar strategies, produces optimal collective outcomes
'''

description_COLLECTIVE_61 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared lifeline. The mathematically optimal collective outcome occurs when **all players cooperate every round**, maintaining the stock at capacity and maximizing total extraction over time. However, since we cannot coordinate with others directly, we must design a strategy that:

1. Signals cooperative intent clearly
2. Protects the resource from collapse
3. Responds proportionally to defection without triggering death spirals
4. Prioritizes long-term collective welfare over short-term individual gains

## Strategy: "Guardian with Graduated Response"

### Decision Framework

```
COOPERATE by default, DEFECT only when:
1. The resource is critically threatened AND others are exploiting it, OR
2. It's the final round (endgame adjustment)
```

### Detailed Decision Rules

#### Round 1: Always Cooperate
- Establishes cooperative intent
- No information yet about others' behavior
- Preserves full resource capacity for future rounds

#### Rounds 2 through (r-1): Conditional Cooperation

**Calculate two key metrics:**
1. **Defection Rate** = (number of D plays in previous round) / n
2. **Stock Health** = current_stock / capacity

**Decision Logic:**

```
IF stock_health ≥ 0.5:
    # Resource is healthy
    IF defection_rate ≤ 0.5:
        COOPERATE  # Maintain cooperation, resource is sustainable
    ELSE:
        COOPERATE  # Still cooperate - don't accelerate collapse
        
ELSE IF stock_health ≥ 0.25:
    # Resource is stressed
    IF defection_rate ≤ 0.25:
        COOPERATE  # Few defectors, help resource recover
    ELSE:
        DEFECT     # Protect self while resource depletes

ELSE IF stock_health > 0.1:
    # Resource is critical
    IF defection_rate == 0:
        COOPERATE  # Everyone cooperating, help recovery
    ELSE:
        DEFECT     # Resource likely collapsing, minimize losses

ELSE:
    # Resource near collapse (stock_health ≤ 0.1)
    DEFECT         # Extract remaining value before total collapse
```

#### Final Round (round r): Defect
- No future to preserve
- Standard game theory applies
- However, if playing with known collective partners, consider cooperating

### Forgiveness Mechanism

After defecting due to others' defection, return to cooperation if:
- The defection rate drops to ≤ 0.25 in the subsequent round, AND
- Stock health is ≥ 0.3

This prevents permanent defection spirals and rewards collective course-correction.

### Edge Cases

1. **n = 2 (two players)**: Use standard Tit-for-Tat with forgiveness
   - Cooperate if opponent cooperated last round
   - After opponent defects once, defect once, then try cooperating again

2. **Very short games (r ≤ 3)**: 
   - r = 2: Cooperate round 1, Defect round 2
   - r = 3: Cooperate rounds 1-2, Defect round 3

3. **Stock already at 0**: Action is irrelevant (payoff = 0 regardless)

4. **Stock very low but non-zero**: Cooperate if alone can enable recovery; otherwise defect

### Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, n, history):
    stock_health = stock / capacity
    
    if round == 1:
        return COOPERATE
    
    if round == total_rounds:
        return DEFECT
    
    defection_rate = count_defections_last_round(history) / n
    
    if stock_health >= 0.5:
        return COOPERATE
    elif stock_health >= 0.25:
        return COOPERATE if defection_rate <= 0.25 else DEFECT
    elif stock_health > 0.1:
        return COOPERATE if defection_rate == 0 else DEFECT
    else:
        return DEFECT
```

## Why This Strategy is Collectively Optimal

1. **Maximizes sustained yield**: Full cooperation maintains stock at capacity, yielding capacity/(2n) per player per round indefinitely
2. **Protects commons**: Only defects when resource is already threatened by others
3. **Forgives and recovers**: Allows return to cooperation, preventing permanent tragedy
4. **Clear signaling**: Consistent cooperation signals intent to coordinate on optimal outcome
'''

description_COLLECTIVE_62 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation sustains the resource indefinitely** (as shown in Example 1), while defection creates a tragedy of the commons. My strategy aims to maximize collective welfare while protecting against exploitation.

## Strategy Overview: "Graduated Guardian"

This is a threshold-based reactive strategy that starts cooperatively, monitors resource health and group behavior, and adjusts consumption based on both the stock state and observed cooperation levels.

---

## Decision Rules

### Primary Decision Framework

**Cooperate (C) when:**
1. The resource is healthy AND cooperation is being reciprocated, OR
2. We're in early rounds establishing cooperative norms, OR
3. The resource is critically low (preservation mode)

**Defect (D) when:**
1. Defection is widespread and cooperation would only enable free-riders, OR
2. It's the final round (no future to protect), OR
3. The stock is already doomed (below recovery threshold) AND others are defecting

### Detailed Decision Algorithm

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    stock_ratio = current_stock / capacity
    
    # If history exists, calculate cooperation rate from last round
    IF round > 1:
        last_round_actions = history[round - 1]
        coop_rate = count(C in last_round_actions) / n_players
    ELSE:
        coop_rate = 1.0  # Assume cooperation initially
    
    # RULE 1: Final Round - No future consequences
    IF rounds_remaining == 0:
        RETURN D
    
    # RULE 2: First Round - Establish cooperative intent
    IF round == 1:
        RETURN C
    
    # RULE 3: Critical Stock Protection
    # If stock is very low but recoverable, cooperate to save it
    IF stock_ratio < 0.25 AND stock_ratio > 0.05:
        IF coop_rate >= 0.5:
            RETURN C  # Join preservation effort
        ELSE:
            RETURN D  # Others aren't helping, resource is lost
    
    # RULE 4: Doomed Resource
    # If stock is essentially depleted, defect (nothing to save)
    IF stock_ratio <= 0.05:
        RETURN D
    
    # RULE 5: Responsive Cooperation Threshold
    # Cooperate if sufficient others are cooperating
    cooperation_threshold = calculate_threshold(rounds_remaining, total_rounds)
    
    IF coop_rate >= cooperation_threshold:
        RETURN C
    ELSE:
        RETURN D

FUNCTION calculate_threshold(rounds_remaining, total_rounds):
    # Be more forgiving early, stricter as game progresses
    # Early game: threshold ~0.4 (tolerant)
    # Mid game: threshold ~0.5 (balanced)  
    # Late game: threshold ~0.6 (protective)
    
    progress = 1 - (rounds_remaining / total_rounds)
    base_threshold = 0.4
    threshold_increase = 0.2 * progress
    
    RETURN base_threshold + threshold_increase
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | C | Signal cooperative intent; no history to react to |
| **Final Round** | D | No future rounds to protect; dominant strategy |
| **Penultimate Round** | Apply normal rules | Still worth preserving for final round payoff |
| **Stock = 0** | D | Irrelevant choice, but D is weakly dominant |
| **Stock near capacity, all defecting** | D | Can't sustain cooperation alone; resource will survive one more round of defection anyway |
| **Stock critical, others cooperating** | C | Join the preservation effort |
| **n = 2 (two players)** | Same rules apply | Threshold logic still works |

---

## Collective Alignment

This strategy embodies collective thinking by:

1. **Starting with trust**: Round 1 cooperation signals willingness to work together
2. **Rewarding cooperation**: Continuing to cooperate when others do sustains the resource for everyone
3. **Graduated response**: Not immediately punishing minor defection; allowing recovery
4. **Resource-focused**: Prioritizing stock health over short-term individual gains
5. **Protecting the commons**: Shifting to preservation mode when stock is threatened

The strategy recognizes that **if all players use this same strategy**, the outcome is sustained cooperation until the final round, maximizing collective payoff across nearly all rounds.
'''

description_COLLECTIVE_63 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully each round, maximizing total payoffs across all rounds. Any defection depletes the resource, reducing future payoffs for everyone including the defector.

## Strategy Name: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to stewardship**: Protect the resource unless evidence demands otherwise
2. **Respond proportionally to threat**: Escalate only as necessary to deter exploitation
3. **Forgive to restore cooperation**: Create pathways back to mutual benefit

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists to inform decisions
- Cooperation signals willingness to sustain the resource
- Establishes baseline for detecting defectors

### Middle Rounds (2 through r-1):

**Calculate two key metrics each round:**

1. **Stock Health Ratio** = current_stock / capacity
2. **Recent Defection Rate** = (number of D plays in last 3 rounds) / (n × min(3, rounds_played))

**Decision Logic:**

```
IF stock_health_ratio < 0.25:
    # Resource in critical danger - emergency cooperation to allow recovery
    COOPERATE
    
ELSE IF recent_defection_rate > 0.5:
    # Majority defecting - resource likely doomed, protect self
    DEFECT
    
ELSE IF recent_defection_rate > 0.2:
    # Significant defection detected - probabilistic punishment
    DEFECT with probability = recent_defection_rate
    COOPERATE with probability = 1 - recent_defection_rate
    
ELSE:
    # Cooperation prevailing - maintain it
    COOPERATE
```

### Final Round (round r):

**Special consideration**: No future to protect, but collective identity matters.

```
IF stock_health_ratio > 0.75 AND recent_defection_rate < 0.15:
    # Cooperation held throughout - honor the collective achievement
    COOPERATE
    
ELSE:
    # Resource degraded or trust broken - standard self-interest applies
    DEFECT
```

---

## Edge Cases

### Near-Zero Stock (stock < capacity/10):
Always cooperate regardless of other factors. Defection at low stock yields minimal immediate gain while ensuring permanent collapse. Even a small recovery chance has higher expected value.

### Perfect Cooperation History:
If defection_rate = 0 through round t, cooperate unconditionally until first observed defection. Don't be the one to break a working system.

### Single Observed Defector:
If exactly one defection occurred in the previous round and stock remains above 50%:
- **Forgive once**: Cooperate
- If same pattern repeats: Switch to graduated response

### Catastrophic Defection Event:
If a single round sees >75% defection rate and stock drops below 50%:
- Defect for the next 2 rounds (punishment phase)
- Then attempt cooperation restart

---

## Pseudocode Implementation

```python
def decide(game_params, state, history):
    n, r, capacity = game_params
    current_round = len(history) + 1
    stock = state['stock']
    
    stock_health = stock / capacity
    
    # Round 1
    if current_round == 1:
        return 'C'
    
    # Calculate recent defection rate (last 3 rounds)
    lookback = min(3, len(history))
    recent_actions = history[-lookback:]
    total_actions = sum(len(round_actions) for round_actions in recent_actions)
    defections = sum(action == 'D' for round_actions in recent_actions 
                     for action in round_actions)
    recent_defection_rate = defections / total_actions if total_actions > 0 else 0
    
    # Critical stock - emergency cooperation
    if stock_health < 0.25:
        return 'C'
    
    # Final round logic
    if current_round == r:
        if stock_health > 0.75 and recent_defection_rate < 0.15:
            return 'C'
        else:
            return 'D'
    
    # Middle rounds - graduated response
    if recent_defection_rate > 0.5:
        return 'D'
    elif recent_defection_rate > 0.2:
        return 'D' if random() < recent_defection_rate else 'C'
    else:
        return 'C'
```

---

## Why This Strategy Serves the Collective

1. **Sustainability-first**: Prioritizes keeping the resource alive, which benefits all players across all rounds

2. **Graduated punishment**: Doesn't overreact to isolated defections, maintaining cooperation potential while deterring exploitation

3. **Emergency protocols**: When the resource is critically low, switches to unconditional cooperation - the only chance for collective survival

4. **Forgiveness pathways**: The probabilistic response and forgiveness mechanisms allow return to cooperation after breakdowns

5. **Honors collective success**: The final-round cooperation reward incentivizes maintaining cooperation throughout, even knowing the game will end
'''

description_COLLECTIVE_64 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across rounds. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - it maintains stock at capacity while providing consistent returns. Any defection triggers resource depletion that harms everyone, including the defector, in future rounds.

## Strategy Name: "Graduated Guardian"

### Decision Framework

The strategy makes decisions based on three key factors:
1. **Resource health** - How depleted is the stock relative to capacity?
2. **Community behavior** - What fraction of players cooperated last round?
3. **Time horizon** - How many rounds remain for recovery to matter?

### Decision Rules

```
COOPERATE if ANY of these conditions hold:
  1. First round (establish cooperative norm)
  2. Stock ≥ 80% of capacity AND ≥ 75% of players cooperated last round
  3. Stock < 50% of capacity (emergency conservation mode)
  4. Rounds remaining > 2 AND recovery is still possible (stock > 0)

DEFECT if ALL of these conditions hold:
  1. Not first round
  2. Either:
     a. Final round (no future to protect), OR
     b. Stock already at 0 (nothing left to conserve), OR
     c. ≤ 25% of players cooperated last round AND stock > 50% capacity
        (community has abandoned cooperation, protect yourself while resources exist)
```

### Detailed Logic

**Round 1:** Always Cooperate
- Signal cooperative intent
- If all cooperate, stock remains at capacity - optimal outcome
- Establishes baseline for measuring others' behavior

**Middle Rounds (2 through r-1):**

*If stock is critically low (< 50% capacity):*
- **Cooperate unconditionally** - The resource needs protection regardless of others' behavior. Defecting here accelerates collapse and hurts everyone including yourself.

*If stock is healthy (≥ 50% capacity):*
- Calculate cooperation rate from previous round
- If ≥ 50% cooperated: **Cooperate** (maintain the cooperative equilibrium)
- If < 50% cooperated but stock still > 80%: **Cooperate** (give community another chance)
- If < 25% cooperated and stock 50-80%: **Defect** (community has defected, minimize personal loss while resources exist)

**Final Round:**
- **Defect** - No future rounds mean no recovery benefit from conservation. This is the dominant strategy when the shadow of the future disappears.

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | Defect | Nothing to protect; D and C both yield 0 |
| Stock = capacity, all cooperated | Cooperate | Maintain optimal sustainable state |
| n = 2, opponent defected | Cooperate if stock < 50%, else Defect | Two-player case needs faster response |
| r = 2 (only 2 rounds) | C then D | Cooperate round 1, defect final round |
| Everyone defected last round | Cooperate if stock < 30% | Emergency mode overrides retaliation |

### Pseudocode

```python
def decide(round, total_rounds, stock, capacity, n, history):
    
    # Final round - no future to protect
    if round == total_rounds:
        return DEFECT
    
    # First round - establish cooperation
    if round == 1:
        return COOPERATE
    
    # Resource depleted - nothing to lose
    if stock == 0:
        return DEFECT
    
    # Calculate previous round cooperation rate
    coop_rate = count(history[round-1] == C) / n
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Emergency conservation mode
    if stock_ratio < 0.5:
        return COOPERATE
    
    # Healthy stock with cooperative community
    if coop_rate >= 0.5:
        return COOPERATE
    
    # Healthy stock but community defecting
    if coop_rate < 0.25 and stock_ratio >= 0.5:
        return DEFECT
    
    # Default: give cooperation another chance
    return COOPERATE
```

### Why This Strategy is Collectively Optimal

1. **Sustainability focus**: Prioritizes long-term stock health over short-term gains
2. **Forgiveness**: Returns to cooperation when community shows cooperative intent
3. **Emergency solidarity**: Never defects during resource crisis
4. **Realistic endgame**: Acknowledges final-round dynamics while maximizing collective welfare in earlier rounds
5. **Robust to exploitation**: Responds to mass defection to avoid being a perpetual sucker
'''

description_COLLECTIVE_65 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This is fundamentally a **tragedy of the commons** scenario. The key insight is that universal cooperation sustains the resource indefinitely (stock regenerates to capacity when all cooperate), while defection depletes it rapidly. My strategy aims to **maximize collective long-term payoffs** by signaling cooperative intent, punishing defection to deter exploitation, but doing so in a measured way that allows for recovery.

## Strategy: "Sustainable Guardian"

### Decision Rules

**Round 1: Always Cooperate**
- Signal cooperative intent clearly
- Establish baseline for observing others' behavior
- No information exists yet to justify defection

**Rounds 2 through r-1: Conditional Cooperation with Graduated Response**

```
Let d_prev = number of defectors in the previous round
Let d_total = cumulative defection rate across all players over all past rounds
Let stock_ratio = current_stock / capacity

IF stock_ratio < 0.25:
    # Critical depletion - cooperate to allow any possible recovery
    COOPERATE
    
ELSE IF d_prev == 0:
    # Everyone cooperated last round - maintain cooperation
    COOPERATE
    
ELSE IF d_prev >= n/2:
    # Majority defected - defect this round as protective measure
    # (but only for one round, then reassess)
    DEFECT
    
ELSE IF d_total > 0.3:
    # Chronic defection pattern detected (>30% historical defection rate)
    # Match the approximate defection rate probabilistically
    DEFECT with probability = d_total
    COOPERATE with probability = 1 - d_total
    
ELSE:
    # Minority defected, overall pattern still cooperative
    # Give benefit of the doubt, maintain cooperation
    COOPERATE
```

**Final Round (Round r): Conditional on History**

```
IF historical cooperation rate across all players >= 0.7:
    # Reward sustained cooperation - don't betray partners
    COOPERATE
ELSE:
    # Pattern of defection exists - no future to protect
    DEFECT
```

### Key Design Principles

1. **Start Cooperatively**: Creates opportunity for mutual benefit and signals intent

2. **Forgiveness**: One-round punishment followed by return to cooperation allows recovery from mistakes or initial defection

3. **Stock-Aware**: When resources are critically low, cooperation is essential for any recovery - defecting on a nearly empty pool gains little and guarantees collapse

4. **Proportional Response**: Match chronic defection probabilistically rather than all-or-nothing, maintaining some cooperation to sustain the resource

5. **End-Game Integrity**: Don't automatically defect in the final round - this rewards cooperative opponents and maintains the collective mindset

### Edge Cases

- **n = 2**: Strategy works but with binary d_prev (0, 1, or 2). Threshold of n/2 = 1, so even one defector triggers defensive defection.

- **Very short games (r = 2 or 3)**: Limited punishment opportunity, but starting cooperative and final-round rule still provide reasonable outcomes.

- **Stock = 0**: Both actions yield 0 payoff. Choose COOPERATE (costs nothing, signals intent if stock somehow recovers).

- **All opponents always defect**: After round 1, strategy will defect most rounds (matching their behavior), minimizing exploitation while extracting what value remains.

- **All opponents always cooperate**: Strategy maintains cooperation throughout, achieving optimal collective outcome.

### Pseudocode Summary

```
function decide(round, history, stock, capacity, n, r):
    if round == 1:
        return COOPERATE
    
    if round == r:  # final round
        if cooperation_rate(history) >= 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds
    if stock / capacity < 0.25:
        return COOPERATE
    
    d_prev = count_defectors(history, round - 1)
    
    if d_prev == 0:
        return COOPERATE
    elif d_prev >= n / 2:
        return DEFECT
    elif cumulative_defection_rate(history) > 0.3:
        return DEFECT with probability cumulative_defection_rate(history)
    else:
        return COOPERATE
```

This strategy prioritizes resource sustainability while protecting against exploitation, embodying a collective mindset that rewards cooperation and maintains the common pool for long-term benefit.
'''

description_COLLECTIVE_66 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and beneficial for everyone. The strategy prioritizes long-term collective welfare while remaining robust against defectors.

## Strategy Name: "Sustainable Threshold with Graduated Response"

### Key Insight

When all players cooperate (play C), the stock remains at capacity indefinitely—this is the **sustainable equilibrium**. Any defection depletes the stock, reducing future payoffs for everyone. The strategy should:
1. Default to cooperation to maintain sustainability
2. Protect the commons from collapse when defection is detected
3. Allow for recovery and forgiveness

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, evaluate in order:

1. STOCK HEALTH CHECK
   - Calculate: health_ratio = current_stock / capacity
   
2. COOPERATION HISTORY CHECK
   - Calculate: defection_rate = (total defections observed) / (total actions observed)
   - Recent_defection_rate = defections in last 3 rounds / actions in last 3 rounds

3. DECIDE ACTION based on conditions below
```

### Specific Rules

**Rule 1: First Round**
- **Action: COOPERATE**
- Rationale: Establish cooperative norm; signal collective intent

**Rule 2: Final Round**
- **Action: COOPERATE if stock > capacity/2, else DEFECT**
- Rationale: If commons is healthy, maintain cooperative reputation for repeated tournament play; if depleted, salvage what remains

**Rule 3: Critical Stock Emergency (stock < capacity/4)**
- **Action: COOPERATE**
- Rationale: When stock is critically low, cooperation is essential for any recovery. Defecting now yields little and guarantees collapse.

**Rule 4: Healthy Stock with No Recent Defection (stock ≥ capacity/2 AND recent_defection_rate = 0)**
- **Action: COOPERATE**
- Rationale: Maintain the sustainable equilibrium

**Rule 5: Graduated Response to Defection**
```
IF recent_defection_rate > 0:
    - If recent_defection_rate < 0.25: COOPERATE (forgive minor defection)
    - If recent_defection_rate ∈ [0.25, 0.5): DEFECT with probability = recent_defection_rate
    - If recent_defection_rate ≥ 0.5: DEFECT
```
- Rationale: Proportional response discourages defection without triggering collapse spirals

**Rule 6: Declining Stock Trend**
```
IF stock decreased in 2+ consecutive rounds despite majority cooperation:
    - COOPERATE (double down on sustainability)
```
- Rationale: If stock is declining even with cooperation, more defection only accelerates collapse

---

## Pseudocode Implementation

```python
def decide(game_params, current_stock, history):
    n = game_params.n
    capacity = game_params.capacity
    current_round = len(history) + 1
    total_rounds = game_params.r
    
    # First round: cooperate
    if current_round == 1:
        return COOPERATE
    
    # Calculate metrics
    health_ratio = current_stock / capacity
    recent_history = history[-3:] if len(history) >= 3 else history
    
    recent_defections = count_defections(recent_history)
    recent_total = count_total_actions(recent_history)
    recent_defection_rate = recent_defections / recent_total if recent_total > 0 else 0
    
    # Final round
    if current_round == total_rounds:
        return COOPERATE if health_ratio > 0.5 else DEFECT
    
    # Critical stock: must cooperate for any chance of recovery
    if health_ratio < 0.25:
        return COOPERATE
    
    # Healthy stock with recent cooperation: maintain equilibrium
    if health_ratio >= 0.5 and recent_defection_rate == 0:
        return COOPERATE
    
    # Graduated response to defection
    if recent_defection_rate < 0.25:
        return COOPERATE  # Forgive
    elif recent_defection_rate < 0.5:
        return DEFECT if random() < recent_defection_rate else COOPERATE
    else:
        return DEFECT  # Match high defection
```

---

## Why This Strategy is Collectively Optimal

1. **Self-sustaining**: When all players use this strategy, everyone cooperates, stock stays at capacity, and each player earns `capacity/(2n)` every round—the maximum sustainable yield.

2. **Robust to defectors**: Graduated response punishes defection proportionally without triggering a collapse spiral.

3. **Recovery-oriented**: Cooperation during low stock allows regrowth rather than racing to extract the last resources.

4. **Forgiveness built-in**: Minor defection is forgiven, allowing return to cooperation after mistakes or noise.
'''

description_COLLECTIVE_67 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embodies a **sustainable commons stewardship** approach. The key insight is that universal cooperation maintains the resource at capacity indefinitely, providing 12.5 units per round forever, while defection provides short-term gains at the cost of destroying the commons. With sufficient rounds, cooperation dominates—but only if enough players cooperate.

The strategy operates as a **conditional cooperator with forgiveness**, designed to:
1. Signal cooperative intent early
2. Protect the commons from collapse
3. Punish sustained defection proportionally
4. Forgive and rebuild when possible

---

## Decision Rules

### Primary Decision Framework

```
FUNCTION decide(round, total_rounds, current_stock, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    defection_rate = calculate_recent_defection_rate(history, lookback=3)
    
    # RULE 1: First Round - Unconditional Cooperation
    IF round == 1:
        RETURN Cooperate
    
    # RULE 2: Last Round Logic
    IF rounds_remaining == 0:
        IF stock_ratio < 0.3 OR defection_rate > 0.5:
            RETURN Defect  # No future to protect
        ELSE:
            RETURN Cooperate  # Maintain cooperative reputation signal
    
    # RULE 3: Emergency Resource Protection
    IF stock_ratio < 0.25:
        RETURN Cooperate  # Always cooperate when commons is critical
    
    # RULE 4: Adaptive Response to Environment
    RETURN adaptive_response(defection_rate, stock_ratio, rounds_remaining)
```

### Adaptive Response Logic

```
FUNCTION adaptive_response(defection_rate, stock_ratio, rounds_remaining):
    
    # Generous Tit-for-Tat with collective memory
    
    # High cooperation environment (defection < 25%)
    IF defection_rate < 0.25:
        RETURN Cooperate
    
    # Mixed environment (25-50% defection)
    IF defection_rate < 0.50:
        # Cooperate with probability based on stock health
        IF stock_ratio > 0.6:
            RETURN Cooperate
        ELSE:
            # Probabilistic: cooperate 70% of the time to signal forgiveness
            RETURN Cooperate with 70% probability, else Defect
    
    # High defection environment (50-75% defection)
    IF defection_rate < 0.75:
        # Match the environment but lean cooperative if stock is healthy
        IF stock_ratio > 0.7 AND rounds_remaining > 3:
            RETURN Cooperate  # Attempt to reset cooperation
        ELSE:
            RETURN Defect
    
    # Collapse environment (>75% defection)
    # Defect to avoid being exploited, unless stock is critical
    IF stock_ratio < 0.25:
        RETURN Cooperate  # Last-ditch attempt to save commons
    ELSE:
        RETURN Defect
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative signal; no history to react to |
| **Final round** | Conditional | Cooperate if environment was cooperative; defect if already degraded |
| **Stock < 25% capacity** | Cooperate | Emergency protection; defection here destroys everyone's future |
| **Stock at capacity** | Follow adaptive rules | Healthy stock allows some punishment of defectors |
| **Single defector emerged** | Cooperate | One defector doesn't collapse the system; maintain cooperation |
| **Majority defecting** | Defect (with exceptions) | Avoid exploitation, but return to cooperation if stock recovers |

---

## Calculating Defection Rate

```
FUNCTION calculate_recent_defection_rate(history, lookback):
    IF no history:
        RETURN 0
    
    recent_rounds = last 'lookback' rounds from history
    total_actions = count all player actions in recent_rounds
    total_defections = count all Defect actions in recent_rounds
    
    RETURN total_defections / total_actions
```

---

## Key Strategic Properties

1. **Nice**: Never defects first
2. **Provocable**: Responds to high defection rates with defection
3. **Forgiving**: Returns to cooperation when defection drops or stock recovers
4. **Clear signaling**: Consistent behavior makes intentions legible to adaptive opponents
5. **Collectively rational**: Prioritizes long-term collective welfare, especially in crisis
'''

description_COLLECTIVE_68 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across generations (rounds). The key insight is that **universal cooperation is the only sustainable equilibrium** - it maintains full stock capacity indefinitely, while any defection triggers a tragedy of the commons that ultimately harms everyone, including defectors.

My strategy aims to:
1. Signal cooperative intent clearly from the start
2. Protect the resource from collapse through measured responses
3. Forgive and rebuild when possible
4. Recognize when the resource is beyond saving

---

## Decision Rules

### Primary Rule: Stock-Adaptive Conditional Cooperation

```
COOPERATE if:
    - Stock is healthy (≥ 60% capacity) AND no recent defections detected
    - OR we're in a recovery phase after successful cooperation
    - OR stock is critically low and cooperation is the only path to recovery

DEFECT if:
    - Defection was detected last round AND stock can survive retaliation
    - OR stock is so depleted that the game is effectively over
    - OR it's the final round (no future to protect)
```

### Detailed Decision Logic

**Round 1: Always Cooperate**
- Establish cooperative intent
- Baseline measurement: if stock drops more than expected from universal cooperation, defectors are present

**Rounds 2 through (r-1): Conditional Response**

```
Let expected_stock_if_all_C = previous_stock (full regeneration)
Let actual_stock = current observed stock
Let stock_ratio = actual_stock / capacity
Let defection_detected = (actual_stock < expected_stock_if_all_C - small_tolerance)

If stock_ratio ≥ 0.6:
    If defection_detected in previous round:
        DEFECT (punish to discourage exploitation)
    Else:
        COOPERATE (maintain healthy equilibrium)

Else if stock_ratio ≥ 0.3:
    # Resource stressed but recoverable
    If last 2 rounds showed recovery trend:
        COOPERATE (support recovery)
    Else if defection_detected:
        DEFECT (cannot afford to be exploited while vulnerable)
    Else:
        COOPERATE (attempt to rebuild)

Else if stock_ratio > 0.1:
    # Critical zone - cooperation is mathematically necessary for any recovery
    COOPERATE (desperation cooperation - defecting here kills the resource)

Else:
    # stock_ratio ≤ 0.1: Resource effectively dead
    DEFECT (extract remaining value; regeneration impossible)
```

**Final Round: Always Defect**
- No future rounds to protect
- This is common knowledge, so no reputational cost

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish baseline, signal intent |
| Final round | Defect | No future consequences |
| Stock = capacity after round 1 | Cooperate | Universal cooperation achieved |
| Stock dropped but > 75% capacity | Cooperate once more | Give benefit of doubt (could be one defector testing) |
| Repeated defection detected (2+ rounds) | Defect until cooperation resumes | Tit-for-tat punishment phase |
| Stock recovering after punishment | Cooperate | Forgiveness enables return to good equilibrium |
| Stock < 10% capacity | Defect | Resource cannot recover meaningfully |
| n is very large (>10) | More forgiving threshold | Individual defection has smaller signal |

---

## Detection Mechanism

To detect defection without observing individual actions:

```
After each round:
    expected_consumption_all_C = previous_stock / 2
    expected_remaining = previous_stock / 2
    expected_growth = 2 × expected_remaining × (1 - expected_remaining/capacity)
    expected_new_stock = min(expected_remaining + expected_growth, capacity)
    
    tolerance = 0.05 × capacity  # Account for floating point, edge cases
    
    defection_detected = (actual_stock < expected_new_stock - tolerance)
```

---

## Pseudocode Summary

```python
def decide(round, total_rounds, current_stock, previous_stock, capacity, n, history):
    
    if round == 1:
        return COOPERATE
    
    if round == total_rounds:
        return DEFECT
    
    stock_ratio = current_stock / capacity
    defection_detected = detect_defection(current_stock, previous_stock, capacity, n)
    
    # Resource dead - extract remaining
    if stock_ratio <= 0.1:
        return DEFECT
    
    # Critical but recoverable - must cooperate
    if stock_ratio <= 0.3:
        return COOPERATE
    
    # Stressed resource
    if stock_ratio <= 0.6:
        if is_recovering(history):
            return COOPERATE
        elif defection_detected:
            return DEFECT
        else:
            return COOPERATE
    
    # Healthy resource
    if defection_detected:
        return DEFECT  # Punish
    else:
        return COOPERATE  # Maintain
```

---

## Why This Strategy is Collectively Optimal

1. **Sustainability**: Universal cooperation maintains stock at capacity forever, yielding `capacity/(2n)` per player per round indefinitely.

2. **Deterrence**: The punishment mechanism makes defection unprofitable - a defector gains `stock/n` once but triggers retaliation that depletes the shared resource.

3. **Forgiveness**: By returning to cooperation when the resource recovers, we don't lock into mutually destructive spirals.

4. **Robustness**: The stock-based thresholds adapt to any opponent mix - we protect the resource when it matters and extract value when it's doomed.

5. **Collective alignment**: When playing against copies of this strategy, we achieve perfect cooperation for rounds 1 through (r-1), maximizing collective welfare.
'''

description_COLLECTIVE_69 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a population of agents sharing the same collective mindset. Our goal is to maximize long-term group welfare while protecting the resource from collapse. The key insight is that **sustainable harvesting at capacity generates maximum cumulative payoffs** - if all cooperate, the stock regenerates fully each round, providing stable returns indefinitely.

## Strategy: "Adaptive Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to maintain resource sustainability
2. **Respond proportionally to defection** to discourage exploitation
3. **Protect critical stock levels** to prevent collapse

### Decision Rules

```
EACH ROUND:
  
  1. Calculate sustainability threshold:
     critical_threshold = capacity * 0.25
     danger_threshold = capacity * 0.5
  
  2. Check stock health:
     IF stock < critical_threshold:
       → COOPERATE (emergency conservation)
     
  3. For first round:
     → COOPERATE (establish cooperative norm)
  
  4. For last round:
     IF stock > danger_threshold AND history shows majority cooperation:
       → COOPERATE (reward good collective behavior)
     ELSE:
       → DEFECT (no future to protect)
  
  5. For middle rounds, assess recent history (last 3 rounds or available):
     
     cooperation_rate = (total C plays by all players) / (total plays observed)
     
     IF cooperation_rate >= 0.7:
       → COOPERATE (healthy collective behavior)
     
     ELIF cooperation_rate >= 0.4:
       → COOPERATE with probability = cooperation_rate
       → DEFECT with probability = 1 - cooperation_rate
       (Match the collective tendency)
     
     ELSE (cooperation_rate < 0.4):
       IF stock > danger_threshold:
         → DEFECT (others are exploiting, protect self)
       ELSE:
         → COOPERATE (stock is endangered, prioritize survival)
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Signal cooperative intent, no history to react to |
| **Final round** | Conditional (see above) | Balance self-interest with rewarding cooperation |
| **Stock critically low (<25% capacity)** | Always Cooperate | Resource survival trumps all else |
| **Stock near zero** | Cooperate | Any defection guarantees collapse |
| **All previous players defected** | Defect (unless stock critical) | Don't be exploited indefinitely |
| **Mixed history** | Probabilistic matching | Encourage cooperation while not being a pushover |

### Collective Alignment

When multiple agents run this strategy:

1. **Round 1**: All cooperate → stock regenerates to capacity
2. **Subsequent rounds**: High cooperation rate observed → all continue cooperating
3. **Stable equilibrium**: Full cooperation maintained, maximum sustainable yield achieved

If facing defectors:
- Collective gradually shifts to proportional response
- Prevents full exploitation while leaving door open for return to cooperation
- Critical stock protection ensures resource doesn't collapse even under attack

### Why This Works

1. **Against fellow Adaptive Guardians**: Converges to full cooperation, optimal outcome
2. **Against always-defect**: Protects self after initial probe, prevents complete exploitation
3. **Against always-cooperate**: Maintains cooperation (no incentive to deviate)
4. **Against mixed strategies**: Adapts proportionally, encouraging cooperation
5. **Resource protection**: Hard floor on cooperation when stock endangered preserves future rounds

### Summary Pseudocode

```python
def decide(stock, capacity, round, total_rounds, history, n_players):
    critical = capacity * 0.25
    danger = capacity * 0.5
    
    # Emergency conservation
    if stock < critical:
        return COOPERATE
    
    # First round - establish norm
    if round == 1:
        return COOPERATE
    
    # Calculate recent cooperation rate
    recent_history = history[-3:]  # last 3 rounds
    coop_rate = count_cooperations(recent_history) / total_actions(recent_history)
    
    # Last round logic
    if round == total_rounds:
        if stock > danger and coop_rate >= 0.5:
            return COOPERATE
        return DEFECT
    
    # Adaptive response
    if coop_rate >= 0.7:
        return COOPERATE
    elif coop_rate >= 0.4:
        return COOPERATE with probability coop_rate
    else:
        if stock > danger:
            return DEFECT
        return COOPERATE  # Protect endangered resource
```
'''

description_COLLECTIVE_70 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy operates from a **collective sustainability mindset**: the resource is shared, and long-term collective welfare depends on maintaining stock levels that allow regeneration. However, since we cannot assume others share this mindset, the strategy must be adaptive and protect against exploitation while signaling cooperative intent.

## Strategy Overview: "Sustainable Guardian with Graduated Response"

The strategy balances three objectives:
1. **Preserve the resource** for long-term collective benefit
2. **Signal cooperation** to encourage reciprocity
3. **Respond proportionally** to defection without destroying the commons

---

## Decision Rules

### Primary Decision Framework

```
At each round t, calculate:
- cooperation_ratio = (number of C plays in previous round) / n
- stock_health = current_stock / capacity
- rounds_remaining = r - t
```

### Rule 1: First Round - Unconditional Cooperation
**Action: C**

Rationale: Establish cooperative intent. The cost of one round of potential exploitation is worth the signal value and the chance to establish mutual cooperation.

### Rule 2: Stock Emergency Override
**If stock_health < 0.25: Action = C**

Rationale: When the resource is critically depleted, defection accelerates collapse. Even if others defect, cooperating preserves any remaining regeneration potential. This is the collective imperative—survival of the commons takes precedence.

### Rule 3: Last Round Consideration
**If rounds_remaining == 0:**
- If cooperation_ratio (from previous round) ≥ 0.5: **C**
- Else: **D**

Rationale: In the final round, there's no future to protect. However, if the group has been largely cooperative, maintain solidarity. If exploitation has dominated, there's no collective to protect.

### Rule 4: Graduated Response (Main Decision Logic)
**For rounds 2 through r-1:**

```
threshold = max(0.4, stock_health * 0.6)

If cooperation_ratio >= threshold:
    Action = C
Else:
    defection_probability = (threshold - cooperation_ratio) / threshold
    Action = D with probability defection_probability, else C
```

**Interpretation:**
- When cooperation is high relative to stock health, cooperate
- When cooperation drops, probabilistically defect—this allows for:
  - Gradual escalation rather than immediate punishment
  - Noise tolerance (accidental defections don't trigger spirals)
  - A path back to cooperation if others reform

### Rule 5: Forgiveness Mechanism
**If previous round had low cooperation but current stock_health > 0.6:**
```
forgiveness_boost = 0.2
Effective cooperation_ratio = actual_ratio + forgiveness_boost
```

Rationale: If the resource is healthy despite past defection, be more willing to return to cooperation. This prevents permanent punishment spirals.

---

## Complete Decision Pseudocode

```python
def decide(round_number, total_rounds, current_stock, capacity, n, history):
    
    stock_health = current_stock / capacity
    rounds_remaining = total_rounds - round_number
    
    # Rule 1: First round - cooperate unconditionally
    if round_number == 1:
        return C
    
    # Calculate cooperation ratio from previous round
    prev_actions = history[round_number - 1]
    cooperation_ratio = count(prev_actions, C) / n
    
    # Rule 2: Emergency - always cooperate to save the commons
    if stock_health < 0.25:
        return C
    
    # Rule 5: Forgiveness boost when stock is healthy
    if stock_health > 0.6:
        effective_coop_ratio = min(1.0, cooperation_ratio + 0.2)
    else:
        effective_coop_ratio = cooperation_ratio
    
    # Rule 3: Last round
    if rounds_remaining == 0:
        if effective_coop_ratio >= 0.5:
            return C
        else:
            return D
    
    # Rule 4: Graduated response
    threshold = max(0.4, stock_health * 0.6)
    
    if effective_coop_ratio >= threshold:
        return C
    else:
        defection_prob = (threshold - effective_coop_ratio) / threshold
        return D with probability defection_prob, else C
```

---

## Edge Cases

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| First round | C | Signal intent, establish baseline |
| Stock near zero | C | Only cooperation can save regeneration |
| All others defected last round | Probabilistic D (~60-80%) | Strong response but not absolute—leave door open |
| One defector among many cooperators | C | Noise tolerance, maintain group norm |
| Last round, healthy stock, mixed history | C if ≥50% cooperation | Reward collective effort |
| Stock at capacity, all cooperating | C | Perfect equilibrium—maintain it |

---

## Why This Strategy is Collectively Aligned

1. **Prioritizes commons survival** over individual gain (emergency override)
2. **Starts cooperative** to give the collective a chance
3. **Forgives** when conditions allow, enabling recovery from mistakes
4. **Responds proportionally** rather than with scorched-earth retaliation
5. **Probabilistic punishment** allows coordination even with imperfect information
6. **Adaptive thresholds** account for resource state, not just behavior

This strategy treats the resource as a shared inheritance worth protecting, while remaining realistic about the need to discourage free-riding.
'''

description_COLLECTIVE_71 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy operates from a **collective sustainability mindset**: the resource is a shared inheritance that generates the most value when preserved. However, it must also protect against exploitation and respond adaptively to the actual behavior of other players.

The key insight is that **universal cooperation is self-sustaining** (stock regenerates fully), while **defection destroys future value for everyone**. A rational collective should cooperate, but must have mechanisms to discourage free-riding.

---

## Strategy: **Sustainable Commons Guardian**

### Decision Framework

The strategy uses three factors to decide each round:
1. **Resource Health**: How depleted is the stock?
2. **Community Behavior**: What fraction of players cooperated last round?
3. **Game Phase**: Early, middle, or final rounds?

---

### Decision Rules

```
FUNCTION decide_action(round, total_rounds, stock, capacity, history, n):
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - round
    
    IF round == 1:
        RETURN Cooperate  # Signal cooperative intent
    
    # Analyze last round's behavior
    cooperation_rate = count_cooperators(history[-1]) / n
    
    # PHASE 1: Resource Crisis Mode
    IF stock_ratio < 0.25:
        # Resource critically depleted - always cooperate to allow recovery
        RETURN Cooperate
    
    # PHASE 2: Final Round(s)
    IF rounds_remaining == 0:
        # Last round - base on recent cooperation and stock health
        IF cooperation_rate >= 0.5 AND stock_ratio >= 0.5:
            RETURN Cooperate  # Maintain trust to the end
        ELSE:
            RETURN Defect  # No future to protect
    
    # PHASE 3: Near-End Game (last 2-3 rounds)
    IF rounds_remaining <= 2:
        IF cooperation_rate >= (n-1)/n:  # Near-universal cooperation
            RETURN Cooperate
        ELSE:
            RETURN Defect  # Unraveling has begun
    
    # PHASE 4: Main Game - Graduated Reciprocity
    
    # Calculate cooperation threshold based on stock health
    # When stock is healthy, we're more forgiving
    # When stock is stressed, we demand higher cooperation
    forgiveness_threshold = 0.5 - (0.2 * (1 - stock_ratio))
    # Range: 0.3 (full stock) to 0.5 (depleted stock)
    
    IF cooperation_rate >= forgiveness_threshold:
        RETURN Cooperate
    ELSE:
        # Probabilistic punishment - don't always defect
        # This allows recovery from coordination failures
        punishment_probability = 1 - cooperation_rate
        IF random() < punishment_probability:
            RETURN Defect
        ELSE:
            RETURN Cooperate  # Extend olive branch
```

---

### Detailed Rule Explanations

#### Rule 1: First Round - Unconditional Cooperation
**Action**: Always Cooperate

**Rationale**: Signals cooperative intent, establishes baseline for reciprocity, and the resource starts at full capacity so there's no crisis.

#### Rule 2: Resource Crisis Override
**Condition**: Stock < 25% of capacity
**Action**: Always Cooperate

**Rationale**: When the resource is critically depleted, defection accelerates collapse. Even if others defect, preserving any remaining stock gives a chance for recovery. Self-interest and collective interest align here.

#### Rule 3: Final Round Logic
**Condition**: Last round
**Action**: Cooperate if recent cooperation ≥ 50% AND stock ≥ 50%; otherwise Defect

**Rationale**: No future rounds to protect, but rewarding cooperative groups maintains integrity. If the group has been exploitative, no reason to sacrifice in the final moment.

#### Rule 4: End-Game Vigilance
**Condition**: 1-2 rounds remaining
**Action**: Cooperate only if cooperation has been near-universal

**Rationale**: End-game unraveling is the greatest threat. Only sustain cooperation if nearly everyone else is doing so.

#### Rule 5: Main Game - Forgiving Tit-for-Tat with Resource Awareness
**Condition**: Rounds 2 through (r-3)
**Action**: 
- Cooperate if cooperation rate exceeds a dynamic threshold
- Otherwise, probabilistically punish (defect with probability proportional to defection rate)

**Rationale**: 
- More forgiving when resources are healthy (can absorb some defection)
- Stricter when resources are stressed (must protect the commons)
- Probabilistic punishment allows recovery from miscoordination without being exploitable

---

### Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| n = 2 (two players) | Standard rules apply | Cooperation rate is 0%, 50%, or 100% - clear signals |
| Stock = 0 | Cooperate | Nothing to gain from defection; only hope is regeneration |
| All previous rounds had 100% cooperation | Cooperate | Don't break a working system |
| Mixed history (oscillating) | Use current round's threshold | Respond to recent behavior, not ancient history |
| Very long games (r > 20) | Main rules with extra forgiveness early | Build reputation when stakes compound |

---

## Summary

**Sustainable Commons Guardian** is:
- **Cooperative by default** - starts friendly, stays friendly when reciprocated
- **Protective of the resource** - prioritizes sustainability during crises
- **Responsive to behavior** - rewards cooperation, punishes defection proportionally
- **Forgiving** - uses probabilistic punishment to allow recovery
- **End-game aware** - tightens standards as the game concludes

This strategy aims to **maximize collective payoffs** when playing with other cooperative strategies while **minimizing exploitation** when facing defectors.
'''

description_COLLECTIVE_72 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the resource regenerates fully, enabling maximum long-term payoffs for everyone. Defection is a collective trap that destroys future value.

The strategy operates on **conditional cooperation with forgiveness**: start cooperatively, respond proportionally to the group's behavior, but always leave room for recovery.

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if any of the following conditions are met:
1. First round (establish cooperative norm)
2. Stock is critically low (emergency conservation)
3. Recent cooperation rate is sufficiently high (reciprocity)
4. Recovery phase after stock collapse (rebuilding)

DEFECT only when:
- Cooperation rate has been persistently low AND
- Stock is healthy enough to survive AND
- Not in final rounds where cooperation can still yield returns
```

### Detailed Conditions

**Condition 1: First Round**
- Always cooperate in round 1
- Rationale: Signal cooperative intent, give others the opportunity to coordinate

**Condition 2: Stock Emergency (Cooperate)**
- If `stock < capacity * 0.3`: Always cooperate
- Rationale: Below this threshold, even one round of widespread defection can collapse the resource permanently. Conservation is paramount.

**Condition 3: Reciprocity Check**
- Calculate cooperation rate over last `min(3, rounds_played)` rounds
- If `cooperation_rate >= 0.5`: Cooperate
- Rationale: If at least half the group is cooperating, sustain the cooperative equilibrium

**Condition 4: Stock Health Assessment**
- If `stock >= capacity * 0.8`: Cooperate (resource is thriving, maintain it)
- If `stock < capacity * 0.5` AND declining: Cooperate (attempt recovery)

**Condition 5: End-Game Consideration**
- In final round: Cooperate if cooperation_rate in previous round was >= 0.6
- In final 2 rounds: Weight toward cooperation if stock is healthy
- Rationale: Avoid premature unraveling; if others maintained cooperation, honor it

---

## Complete Strategy Algorithm

```
function decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    
    # FIRST ROUND: Unconditional cooperation
    if current_round == 1:
        return COOPERATE
    
    # Calculate recent cooperation rate (last 3 rounds or fewer)
    lookback = min(3, len(history))
    recent_actions = history[-lookback:]
    total_actions = sum(len(round_actions) for round_actions in recent_actions)
    cooperations = sum(
        sum(1 for action in round_actions if action == C)
        for round_actions in recent_actions
    )
    cooperation_rate = cooperations / total_actions if total_actions > 0 else 1.0
    
    # EMERGENCY CONSERVATION: Low stock
    if stock < capacity * 0.3:
        return COOPERATE
    
    # HEALTHY STOCK: Maintain prosperity
    if stock >= capacity * 0.8:
        return COOPERATE
    
    # RECIPROCITY: Match group behavior with bias toward cooperation
    if cooperation_rate >= 0.5:
        return COOPERATE
    
    # RECOVERY MODE: Stock declining and below half
    if current_round >= 2:
        previous_stock = estimate_previous_stock(history, capacity)
        if stock < previous_stock and stock < capacity * 0.5:
            return COOPERATE
    
    # FINAL ROUNDS: Lean cooperative to avoid unraveling
    rounds_remaining = r - current_round
    if rounds_remaining <= 2:
        if cooperation_rate >= 0.4:
            return COOPERATE
    
    # DEFAULT: Proportional response (defect if persistent defection)
    if cooperation_rate < 0.35:
        return DEFECT
    
    return COOPERATE
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish norm |
| Last round, high past cooperation | Cooperate | Honor the social contract |
| Last round, low past cooperation | Cooperate if stock low, else Defect | Protect resource or cut losses |
| Stock near zero | Cooperate | Only hope for recovery |
| Stock at capacity | Cooperate | Maintain optimal state |
| Single defector in group | Cooperate | Forgive isolated defection |
| Majority defecting | Cooperate if stock critical, else Defect | Protect self while signaling |

---

## Why This Strategy Aligns with Collective Interest

1. **Sustainability Focus**: Prioritizes resource preservation over short-term gains
2. **Forgiveness**: Doesn't trigger permanent retaliation from single defections
3. **Emergency Solidarity**: When the resource is threatened, always conserves
4. **Cooperative Default**: Biased toward cooperation in ambiguous situations
5. **Avoids Death Spirals**: Never defects when doing so would collapse the stock

The strategy succeeds by recognizing that **my long-term payoff depends on everyone's long-term payoff**. A depleted pool helps no one.
'''

description_COLLECTIVE_73 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable resource management benefits everyone, including ourselves. The goal is to maintain the resource at productive levels while protecting against exploitation. We treat other players as potential cooperators first, but maintain robust defenses against persistent defectors.

## Strategy Overview: "Sustainable Guardian"

The strategy balances three principles:
1. **Sustainability First**: Protect the resource from collapse
2. **Reciprocal Cooperation**: Reward cooperation, respond to defection
3. **Collective Resilience**: Adapt based on group behavior, not just individuals

---

## Decision Rules

### Primary Decision Function

```
COOPERATE if:
    (stock_health is critical) OR
    (cooperation_rate >= threshold) OR
    (round == 1)
    
DEFECT if:
    (approaching_endgame AND cooperation_has_collapsed) OR
    (sustained_mass_defection)
```

### Detailed Rules

#### 1. Stock Health Assessment
```
stock_ratio = current_stock / capacity
critical_threshold = 0.3
healthy_threshold = 0.6

IF stock_ratio < critical_threshold:
    COOPERATE  # Emergency conservation mode
```
**Rationale**: When the resource is critically depleted, cooperation is essential for recovery. Even if others defect, maintaining the resource serves long-term collective interest.

#### 2. Cooperation Rate Tracking
```
cooperation_rate = (total_C_plays_last_3_rounds) / (n × min(3, rounds_played))

adaptive_threshold = 0.5 - (0.1 × stock_ratio)  
# More forgiving when stock is healthy, stricter when depleted
```

#### 3. Round-Specific Logic

**First Round**: Always COOPERATE
- Signals cooperative intent
- No information yet to justify defection
- Gives collective benefit of the doubt

**Middle Rounds** (round 2 to r-2):
```
IF cooperation_rate >= adaptive_threshold:
    COOPERATE
ELSE IF stock_ratio >= healthy_threshold:
    COOPERATE with probability 0.7  # Occasional cooperation to test recovery
ELSE:
    DEFECT  # Others aren't cooperating and stock is suffering
```

**Final Rounds** (last 2 rounds):
```
IF cooperation_rate >= 0.6 AND stock_ratio >= 0.5:
    COOPERATE  # Maintain cooperative equilibrium
ELSE:
    DEFECT  # Endgame defection if cooperation has broken down
```

---

## Complete Decision Algorithm

```python
def decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    current_stock = state.stock
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    
    # First round: always cooperate
    if current_round == 1:
        return COOPERATE
    
    # Calculate recent cooperation rate (last 3 rounds or all if fewer)
    lookback = min(3, len(history))
    recent_actions = history[-lookback:]
    total_actions = sum(len(round_actions) for round_actions in recent_actions)
    total_cooperations = sum(
        sum(1 for action in round_actions if action == C)
        for round_actions in recent_actions
    )
    cooperation_rate = total_cooperations / total_actions if total_actions > 0 else 1.0
    
    # CRITICAL STOCK: Emergency cooperation
    if stock_ratio < 0.3:
        return COOPERATE
    
    # Calculate adaptive threshold
    adaptive_threshold = max(0.3, 0.5 - (0.15 * stock_ratio))
    
    # ENDGAME LOGIC (last 2 rounds)
    if current_round >= r - 1:
        if cooperation_rate >= 0.6 and stock_ratio >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # MIDDLE GAME LOGIC
    if cooperation_rate >= adaptive_threshold:
        return COOPERATE
    elif stock_ratio >= 0.6:
        # Healthy stock but low cooperation - probabilistic cooperation
        # to signal willingness and test for recovery
        return COOPERATE if random() < 0.6 else DEFECT
    else:
        return DEFECT
```

---

## Edge Cases Handled

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| First round | COOPERATE | No history, signal good faith |
| Stock near zero | COOPERATE | Resource survival is paramount |
| All others defecting | DEFECT (after round 2) | Protect from exploitation |
| Mixed behavior | COOPERATE if majority cooperates | Support the cooperative coalition |
| Last round, good cooperation | COOPERATE | Maintain equilibrium, don't betray |
| Last round, poor cooperation | DEFECT | No future rounds to rebuild trust |
| Stock very healthy | Lean COOPERATE | Can afford forgiveness |

---

## Why This Strategy is Collectively Optimal

1. **Preserves the Resource**: By cooperating when stock is critical, we prevent collapse that hurts everyone
2. **Rewards Cooperation**: Cooperators playing this strategy reinforce each other
3. **Deters Exploitation**: Responds to mass defection, making pure defection unprofitable
4. **Forgives and Recovers**: Probabilistic cooperation allows broken cooperation to rebuild
5. **Sustainable Equilibrium**: If most players use similar logic, the resource stays at capacity (all-C scenario)

This strategy succeeds whether facing cooperators (mutual benefit) or defectors (limits losses while preserving resource for recovery).
'''

description_COLLECTIVE_74 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the common pool is a shared inheritance that generates the most value when preserved. Individual defection may yield short-term gains, but collective cooperation maximizes total payoffs across all rounds. My strategy signals cooperative intent, rewards cooperation, punishes defection proportionally, but always preserves the resource when possible.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy uses three key factors:
1. **Resource health** - How depleted is the stock relative to capacity?
2. **Cooperation history** - What fraction of observed actions have been cooperative?
3. **Time horizon** - How many rounds remain?

### Pseudocode

```
function decide(stock, capacity, n, rounds_remaining, history):
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    
    if history is empty:
        cooperation_rate = 1.0  # Assume good faith initially
    else:
        total_actions = count all observed actions in history
        cooperative_actions = count all C actions in history
        cooperation_rate = cooperative_actions / total_actions
    
    # RULE 1: First Round - Signal Cooperation
    if history is empty:
        return C
    
    # RULE 2: Resource Emergency Protocol
    # If stock is critically low, cooperate to allow recovery
    if stock_ratio < 0.25:
        return C
    
    # RULE 3: Last Round Consideration
    # In final round, base decision on established cooperation level
    if rounds_remaining == 1:
        if cooperation_rate >= 0.6:
            return C  # Reward cooperative community
        else:
            return D  # No future to protect
    
    # RULE 4: Graduated Response Based on Community Behavior
    
    # Calculate cooperation threshold that adjusts with resource scarcity
    # When resources are scarce, we're more forgiving to encourage recovery
    base_threshold = 0.5
    scarcity_adjustment = (1 - stock_ratio) * 0.2
    threshold = base_threshold - scarcity_adjustment
    
    if cooperation_rate >= threshold:
        return C
    else:
        # Probabilistic defection based on how far below threshold
        # This allows for recovery if others start cooperating
        defection_probability = min(1.0, (threshold - cooperation_rate) / threshold)
        
        # But always maintain some cooperation probability for signaling
        if random() > defection_probability * 0.8:
            return C
        else:
            return D
```

### Decision Rules in Plain Language

1. **Round 1**: Always cooperate. This signals cooperative intent and establishes a foundation for collective action.

2. **Resource Emergency (stock < 25% of capacity)**: Always cooperate. When the resource is critically depleted, extraction hastens collapse. Preservation becomes paramount regardless of others' behavior.

3. **Final Round**: Cooperate if the community has been mostly cooperative (≥60% cooperation rate). This rewards good collective behavior and doesn't betray a cooperative group. Defect only if the community has been predominantly exploitative.

4. **Standard Rounds**: Use graduated response:
   - If cooperation rate is above threshold → Cooperate
   - If cooperation rate is below threshold → Probabilistically defect, with probability proportional to how exploitative the community has been
   - The threshold becomes more lenient when resources are scarce (encouraging recovery)
   - Always maintain at least 20% cooperation probability to signal willingness to return to cooperation

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round | C | Establish cooperative norm |
| Stock = 0 | C | No benefit to defection anyway; signal cooperation for potential recovery |
| All others defected last round | Likely D (probabilistic) | Proportional response, but not guaranteed retaliation |
| Mixed history (50/50) | Lean toward C | Give benefit of doubt to maintain resource |
| Stock near capacity, low cooperation | May D | Resource can absorb some exploitation |
| Stock low, any history | C | Resource preservation overrides punishment |

### Why This Strategy Aligns with Collective Interests

1. **Prioritizes sustainability**: The resource emergency protocol ensures we never contribute to total collapse
2. **Forgiveness built in**: Probabilistic punishment allows recovery from defection spirals
3. **Rewards cooperation**: Consistently cooperative communities receive cooperation in return
4. **Adaptive to context**: Responds to both resource state and social dynamics
5. **Signals clearly**: Starting with cooperation and maintaining cooperation probability communicates intent
'''

description_COLLECTIVE_75 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared life-support system. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully each round, providing perpetual moderate returns. Any defection degrades this commons, harming everyone including future rounds.

The strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but allow redemption
4. Maximize collective long-term welfare

---

## Decision Rules

### Primary Decision Framework

```
CALCULATE:
  - cooperation_rate = (total C plays by others in history) / (total plays by others)
  - recent_cooperation = cooperation rate in last 3 rounds
  - stock_health = current_stock / capacity
  - rounds_remaining = r - current_round
  - critical_threshold = capacity / (4 * n)  // Below this, resource may not recover

DECIDE:
  IF first_round:
    COOPERATE (signal good faith)
  
  ELSE IF last_round:
    // Cooperate if resource is healthy and others have been cooperative
    IF stock_health > 0.5 AND cooperation_rate > 0.6:
      COOPERATE
    ELSE:
      DEFECT
  
  ELSE IF stock < critical_threshold:
    // Emergency conservation mode
    COOPERATE (attempt to save the resource)
  
  ELSE:
    // Normal operation: Conditional cooperation with forgiveness
    USE adaptive_trigger_strategy (detailed below)
```

### Adaptive Trigger Strategy

```
adaptive_trigger_strategy:
  
  // Calculate trust score based on weighted history
  trust_score = 0
  FOR each past round t:
    weight = 0.7^(current_round - t - 1)  // Recent rounds matter more
    round_coop_rate = (# of C plays in round t) / (n - 1)
    trust_score += weight * round_coop_rate
  
  NORMALIZE trust_score to [0, 1]
  
  // Adjust threshold based on resource health
  base_threshold = 0.5
  IF stock_health < 0.3:
    threshold = base_threshold - 0.15  // More forgiving when resource is stressed
  ELSE IF stock_health > 0.8:
    threshold = base_threshold + 0.1   // Stricter when resource is healthy
  ELSE:
    threshold = base_threshold
  
  // Factor in rounds remaining (more cooperative early, protect late gains)
  IF rounds_remaining > r * 0.7:
    threshold -= 0.1  // Very forgiving in early game
  ELSE IF rounds_remaining < 3:
    threshold += 0.1  // More cautious near end
  
  // Final decision
  IF trust_score >= threshold:
    COOPERATE
  ELSE:
    DEFECT
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, signal intent |
| **Round 2** | Cooperate unless >50% defected in R1 | Give one chance for coordination |
| **Last round** | Cooperate if history warrants | Resist end-game defection spiral; collective benefit |
| **Stock near zero** | Cooperate | Only cooperation can regenerate; defecting on nothing gains nothing |
| **Stock at capacity** | Follow trust score | Full stock means cooperation is working |
| **All others defected last round** | Defect once, then offer olive branch | Punish but allow redemption |
| **Single defector among cooperators** | Cooperate | Don't let one bad actor destroy the commons |

---

## Collective Alignment Principles

1. **Resource preservation is paramount**: A depleted stock hurts everyone. Even when punishing defectors, prefer actions that don't accelerate collapse.

2. **Forgiveness enables recovery**: After punishment, return to cooperation to allow the system to heal. Perpetual retaliation destroys value.

3. **Lead by example**: Consistent cooperation from this strategy provides a coordination focal point for other cooperative strategies.

4. **Proportional response**: One defector among many cooperators shouldn't trigger full defection - that rewards the defector by collapsing cooperation.

5. **End-game integrity**: Resist the temptation to defect in final rounds. If all players maintain cooperation, everyone benefits more than from mutual defection.

---

## Summary

**Cooperate by default. Defect only when trust erodes significantly or resource stress is caused by others' exploitation. Always return to cooperation when the collective demonstrates willingness to sustain the commons.**
'''

description_COLLECTIVE_76 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a collective of players sharing the same algorithm. Our primary goal is **sustainable harvesting** - maintaining the resource stock at levels that maximize long-term collective payoff while being robust to defectors who might deplete the resource.

## Key Insights

1. **Cooperation is sustainable**: When all players cooperate, stock remains at capacity indefinitely (as shown in the example)
2. **Defection is catastrophic**: Universal defection depletes the resource to zero permanently
3. **The resource regenerates**: The logistic growth function rewards leaving stock in the pool
4. **Defection has short-term appeal**: A defector gets 2× the payoff of a cooperator in any single round

## Strategy: Adaptive Sustainable Harvesting (ASH)

### Decision Framework

```
COOPERATE by default, unless specific defection triggers are met
```

### Round-by-Round Decision Rules

#### First Round
**Action: COOPERATE**
- Establish cooperative baseline
- Preserve full resource capacity for regeneration
- Signal cooperative intent to the collective

#### Middle Rounds (rounds 2 to r-1)

**Calculate key metrics:**
- `defection_ratio` = (number of D actions in previous round) / n
- `stock_health` = current_stock / capacity
- `rounds_remaining` = r - current_round

**Decision Logic:**

```
IF stock_health < 0.25:
    # Critical depletion - resource is dying
    COOPERATE (attempt recovery)
    
ELSE IF defection_ratio > 0.5:
    # Majority defecting - collective coordination has failed
    # Match the environment to avoid being exploited
    DEFECT
    
ELSE IF defection_ratio > 0 AND defection_ratio <= 0.5:
    # Some defection detected
    IF previous_round_i_defected:
        # Give cooperation another chance (forgiveness)
        COOPERATE
    ELSE:
        # Punish defection once, then forgive
        DEFECT
        
ELSE:
    # Full cooperation maintained
    COOPERATE
```

#### Last Round
**Action: DEFECT**
- No future rounds to sustain
- Standard backward induction applies
- All rational players will defect; cooperating just means being exploited

### Edge Cases

1. **Stock at zero**: COOPERATE (nothing to gain from defection anyway; both actions yield 0)

2. **Stock critically low (< 0.1 × capacity)**: COOPERATE regardless of history (prioritize recovery)

3. **Single defector pattern**: If exactly one player defects consistently while others cooperate, maintain COOPERATE (the resource can sustain one defector, and we maintain collective benefit)

4. **Oscillating behavior in history**: If defection_ratio has been alternating, COOPERATE (avoid destructive cycles)

5. **n = 2 special case**: Use stricter thresholds - defect if opponent defected in either of the last two rounds

### Pseudocode Summary

```python
def decide(round, stock, capacity, n, r, history):
    stock_health = stock / capacity
    rounds_remaining = r - round
    
    # Last round - always defect
    if round == r:
        return DEFECT
    
    # First round - always cooperate
    if round == 1:
        return COOPERATE
    
    # Critical stock - prioritize recovery
    if stock_health < 0.1:
        return COOPERATE
    
    # Calculate previous round defection ratio
    prev_defections = count_defections(history[-1])
    defection_ratio = prev_defections / n
    
    # Low stock - be conservative
    if stock_health < 0.25:
        return COOPERATE
    
    # Majority defecting - protect self
    if defection_ratio > 0.5:
        return DEFECT
    
    # Some defection - tit-for-tat with forgiveness
    if defection_ratio > 0:
        if my_last_action(history) == DEFECT:
            return COOPERATE  # Forgive, try to restore cooperation
        else:
            return DEFECT  # Punish once
    
    # Full cooperation - maintain it
    return COOPERATE
```

## Why This Strategy Works for the Collective

1. **Maximizes sustainable yield**: Consistent cooperation keeps stock at capacity
2. **Deters internal defection**: One-round punishment discourages deviation
3. **Forgives quickly**: Prevents death spirals from accidental or exploratory defection
4. **Protects against exploitation**: Responds proportionally to external threats
5. **Prioritizes resource survival**: When stock is critical, preservation trumps punishment
'''

description_COLLECTIVE_77 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: I recognize that I am likely playing alongside other instances of myself or similar AI systems that share the same strategic reasoning. Therefore, my primary goal is to establish and maintain sustainable cooperation that maximizes collective long-term payoffs, while remaining robust against defectors.

## Strategic Framework: "Sustainable Guardian"

### Key Insight

When all players cooperate (C), the stock remains at capacity indefinitely, yielding `capacity/(2n)` per player per round. Over r rounds, this gives each player `r × capacity/(2n)`.

If everyone defects, the resource collapses immediately, yielding only `capacity/n` total per player across all rounds.

**The cooperation premium is massive**: sustainable cooperation yields approximately `r/2` times more total payoff than immediate defection (for typical game lengths).

---

## Decision Rules

### 1. First Round: Always Cooperate
- Signal cooperative intent
- No history to react to
- Establishes baseline for collective behavior

### 2. Standard Rounds (rounds 2 through r-1):

**Primary Rule: Conditional Cooperation with Forgiveness**

```
Let:
  d_prev = number of defectors in the previous round
  d_total = cumulative defections across all players across all rounds
  rounds_played = current round number - 1
  stock_ratio = current_stock / capacity

COOPERATE if ALL of the following hold:
  (a) d_prev ≤ 1  (at most one defector last round - allow for noise/mistakes)
  (b) stock_ratio ≥ 0.5  (resource is still healthy)
  (c) d_total / (n × rounds_played) < 0.25  (overall defection rate below 25%)

DEFECT otherwise
```

**Rationale:**
- Condition (a): Tolerates isolated defection but responds to coordinated exploitation
- Condition (b): Protects against catastrophic resource collapse
- Condition (c): Tracks systemic defection patterns over time

### 3. Recovery Protocol

If stock falls below 50% of capacity due to defection:

```
If stock_ratio < 0.5 AND d_prev ≥ 2:
  DEFECT (protect against continued exploitation)
  
If stock_ratio < 0.5 AND d_prev ≤ 1:
  COOPERATE (attempt recovery if others are cooperating)
```

### 4. Last Round: Conditional

```
If d_total = 0 (perfect cooperation throughout):
  COOPERATE (maintain collective commitment)
  
If stock_ratio ≥ 0.8 AND d_prev = 0:
  COOPERATE (trust has been maintained)
  
Otherwise:
  DEFECT (standard end-game logic when trust is broken)
```

**Collective Rationale for Last Round Cooperation**: If I'm playing with other versions of myself, we all recognize that mutual last-round defection is destructive. By committing to cooperate when trust has been maintained, we collectively achieve better outcomes.

---

## Edge Cases

| Situation | Action | Reason |
|-----------|--------|--------|
| Round 1 | C | Establish cooperation |
| Stock = 0 | C | Payoff is 0 either way; signal intent |
| All defected last round | D | Environment is hostile |
| Single defector, high stock | C | Forgive isolated deviation |
| Repeated single defector | D | Pattern indicates exploitation |
| Last round, perfect history | C | Collective commitment |
| Very short game (r ≤ 3) | C, C, then conditional | Prioritize cooperation window |

---

## Pseudocode Summary

```python
def decide(round, history, stock, capacity, n, r):
    stock_ratio = stock / capacity
    
    if round == 1:
        return COOPERATE
    
    d_prev = count_defectors(history, round - 1)
    d_total = total_defections(history)
    rounds_played = round - 1
    defection_rate = d_total / (n * rounds_played)
    
    # Last round logic
    if round == r:
        if d_total == 0:
            return COOPERATE
        if stock_ratio >= 0.8 and d_prev == 0:
            return COOPERATE
        return DEFECT
    
    # Standard round logic
    if d_prev <= 1 and stock_ratio >= 0.5 and defection_rate < 0.25:
        return COOPERATE
    else:
        return DEFECT
```

---

## Why This Strategy Works Collectively

1. **Self-recognizing**: Other instances using this strategy will all cooperate, maintaining the resource indefinitely
2. **Forgiving**: Tolerates mistakes without spiraling into mutual defection
3. **Protective**: Responds firmly to systematic exploitation
4. **Sustainable**: Prioritizes long-term collective wealth over short-term individual gains
5. **Robust**: Degrades gracefully against hostile opponents while still extracting reasonable payoffs
'''

description_COLLECTIVE_78 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt it, the resource is sustained and everyone benefits maximally over time. The strategy balances cooperation to maintain the resource with protective defection when the commons is being exploited. It uses a **conditional cooperation** approach inspired by successful strategies in repeated social dilemmas.

---

## Strategy: "Sustainable Threshold with Graduated Response"

### Decision Framework

The strategy makes decisions based on three key factors:
1. **Resource health** (current stock relative to capacity)
2. **Community behavior** (recent cooperation rates)
3. **Game phase** (early, middle, late rounds)

---

### Decision Rules

#### 1. First Round
**Action: COOPERATE**

Rationale: Signal cooperative intent. If all players use this strategy, cooperation is established immediately.

#### 2. Last Round
**Action: Conditional based on stock health**

```
IF stock >= capacity * 0.5:
    COOPERATE (resource is healthy, maintain collective outcome)
ELSE:
    DEFECT (resource already damaged, protect individual payoff)
```

Rationale: Unlike pure game theory which suggests universal defection, a collective strategy recognizes that if everyone cooperates even in the final round, the total payoffs are maximized. Only defect if the resource is already critically depleted.

#### 3. Middle Rounds (rounds 2 through r-1)

**Primary Rule: Adaptive Conditional Cooperation**

```
Calculate cooperation_rate = (# of C plays in previous round) / n

IF cooperation_rate >= 0.5:
    # Majority cooperated - reward with cooperation
    COOPERATE
ELSE IF cooperation_rate > 0 AND stock >= capacity * 0.3:
    # Some cooperation exists and resource is viable
    # Probabilistic cooperation to encourage recovery
    COOPERATE with probability = cooperation_rate + 0.2
    DEFECT with probability = 1 - (cooperation_rate + 0.2)
ELSE:
    # Widespread defection or critical resource depletion
    DEFECT
```

#### 4. Resource Emergency Override

```
IF stock < capacity * 0.15:
    # Critical threshold - resource collapse imminent
    COOPERATE (attempt emergency conservation)
    
IF stock < capacity * 0.05:
    # Near-total depletion - minimal payoff available regardless
    COOPERATE (nothing to gain from defection on depleted resource)
```

Rationale: When the resource is critically low, defecting yields very little (stock/n is small). Cooperating gives the only chance for regeneration.

#### 5. Sustained Cooperation Bonus

```
IF last 3 rounds had cooperation_rate >= 0.75:
    # Strong cooperative norm established
    COOPERATE (reinforce the norm)
```

---

### Complete Pseudocode

```
function decide(round, total_rounds, stock, capacity, history, n):
    
    # Calculate metrics
    if round > 1:
        last_round_actions = history[round - 1]
        coop_rate = count(C in last_round_actions) / n
        
        if round >= 4:
            recent_coop_avg = average cooperation rate over last 3 rounds
        else:
            recent_coop_avg = coop_rate
    
    # First round: always cooperate
    if round == 1:
        return COOPERATE
    
    # Resource emergency: attempt conservation
    if stock < capacity * 0.15:
        return COOPERATE
    
    # Last round: conditional on resource health
    if round == total_rounds:
        if stock >= capacity * 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Sustained cooperation bonus
    if round >= 4 and recent_coop_avg >= 0.75:
        return COOPERATE
    
    # Main decision logic
    if coop_rate >= 0.5:
        return COOPERATE
    else if coop_rate > 0 and stock >= capacity * 0.3:
        return COOPERATE with probability (coop_rate + 0.2)
    else:
        return DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Self-reinforcing**: If all players use this strategy, everyone cooperates every round, stock remains at capacity, and total payoffs are maximized.

2. **Robust to defectors**: Responds to exploitation by withdrawing cooperation, preventing indefinite exploitation.

3. **Forgiving**: Returns to cooperation when others do, allowing recovery from mutual defection.

4. **Resource-aware**: Protects the regenerative capacity of the commons, recognizing that a depleted resource hurts everyone.

5. **Adaptive**: Responds to actual behavior rather than assuming worst-case scenarios.
'''

description_COLLECTIVE_79 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource game is fundamentally about **collective survival**. Unlike a simple prisoner's dilemma, the dynamic stock means that widespread defection doesn't just hurt others—it destroys the resource base that everyone depends on. A collectively-minded player should prioritize **resource sustainability** while remaining **adaptive to exploitation**.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Preserve the commons** - The resource must survive for everyone to benefit
2. **Respond proportionally** - Match the collective behavior, not individual actions
3. **Forgive strategically** - Allow recovery when conditions improve

### Decision Rules

```
INPUTS:
- stock: current resource level
- capacity: maximum sustainable level
- n: number of players
- r: total rounds
- t: current round (1-indexed)
- history: list of (stock_at_start, num_defectors) for each past round

COMPUTE:
- stock_ratio = stock / capacity
- rounds_remaining = r - t
- critical_threshold = capacity / (2 * n)  # Below this, resource death spiral likely

IF t == 1:  # First round
    ACTION = COOPERATE  # Signal cooperative intent, preserve resources

ELSE:
    # Calculate recent defection rate (last 3 rounds or available history)
    recent_rounds = min(3, t - 1)
    recent_defection_rate = average(num_defectors / n for last recent_rounds)
    
    # Resource health assessment
    IF stock < critical_threshold:
        # EMERGENCY: Resource near collapse
        ACTION = COOPERATE  # Attempt to save the commons
        
    ELIF stock_ratio < 0.3:
        # LOW STOCK: Be conservative
        IF recent_defection_rate < 0.5:
            ACTION = COOPERATE
        ELSE:
            ACTION = DEFECT  # Don't be exploited in dying resource
            
    ELIF stock_ratio >= 0.7:
        # HEALTHY STOCK: Can sustain some defection
        IF recent_defection_rate < 0.3:
            ACTION = COOPERATE  # Reward collective restraint
        ELIF recent_defection_rate < 0.6:
            ACTION = COOPERATE with probability (1 - recent_defection_rate)
            ACTION = DEFECT otherwise
        ELSE:
            ACTION = DEFECT  # Too much exploitation, protect self
            
    ELSE:  # MODERATE STOCK (0.3 to 0.7)
        # Mirror collective behavior with cooperative bias
        cooperation_threshold = 0.4 + (0.2 * stock_ratio)
        IF recent_defection_rate < cooperation_threshold:
            ACTION = COOPERATE
        ELSE:
            ACTION = DEFECT

# Last round override
IF t == r:
    IF stock_ratio > 0.5 AND recent_defection_rate < 0.4:
        ACTION = COOPERATE  # Maintain integrity even at the end
    ELSE:
        ACTION = DEFECT  # No future to protect
```

### Edge Case Handling

1. **First Round**: Always cooperate. This signals cooperative intent and preserves resources for future rounds. The information gained from observing others is valuable.

2. **Last Round**: Conditionally defect. If the resource is healthy and others have been cooperative, maintain cooperation (collective integrity matters even without future). Otherwise, defect since there's no future deterrence.

3. **Near-Zero Stock**: Always cooperate. When stock approaches critical levels, the only path to recovery requires universal restraint. Even if others defect, cooperating gives the resource a chance.

4. **Full/Near-Full Stock**: More tolerant of defection. A healthy resource can sustain some exploitation while regenerating.

5. **Single Defector Among Cooperators**: Continue cooperating. One defector doesn't destroy the commons, and responding with defection only accelerates collapse.

### Why This Strategy is Collectively Aligned

- **Prioritizes sustainability over short-term gain**: Cooperation maintains the regenerating resource
- **Graduated response**: Doesn't overreact to minor defection, preventing spirals
- **Emergency cooperation**: When the resource is critical, attempts rescue regardless of others
- **Forgiveness built-in**: Uses recent history (3 rounds), allowing recovery from bad equilibria
- **Doesn't assume coordination**: Responds to observed behavior, works with any opponent mix

### Expected Behavior in Tournament

- Against other cooperators: Mutual cooperation, sustained resources, high collective payoff
- Against pure defectors: Eventually defects to avoid exploitation, but tries cooperation first
- Against mixed strategies: Adapts to the prevailing behavior, slightly biased toward cooperation
- Against tit-for-tat variants: Establishes mutual cooperation through initial cooperation signal
'''

description_COLLECTIVE_80 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective welfare mindset**: the resource is shared, and sustainable harvesting benefits everyone across all rounds. However, I must be adaptive since I cannot assume others share this philosophy. The strategy uses **conditional cooperation with forgiveness** - I lead with cooperation, respond proportionally to observed behavior, and always leave room for recovery.

## Strategy Name: "Sustainable Guardian"

### Decision Framework

The strategy makes decisions based on three key factors:
1. **Resource health** (current stock relative to capacity)
2. **Community behavior** (recent cooperation rates)
3. **Game phase** (early, middle, late rounds)

---

## Decision Rules

### Round 1: Always Cooperate
- **Rationale**: Establish cooperative intent, gather information about others, preserve the resource for future rounds.

### Rounds 2 through r-1: Conditional Cooperation

**Calculate two metrics after each round:**

1. **Cooperation Rate (CR)**: Fraction of players who cooperated in the previous round
   - `CR = (number of C plays) / n`

2. **Stock Health (SH)**: Current stock as fraction of capacity
   - `SH = stock / capacity`

**Decision Logic:**

```
IF SH < 0.25 THEN:
    # Resource critically depleted - cooperate to allow recovery
    COOPERATE

ELSE IF SH < 0.50 THEN:
    # Resource stressed - cooperate if at least 40% cooperated last round
    IF CR >= 0.4 THEN COOPERATE
    ELSE DEFECT

ELSE IF SH >= 0.50 THEN:
    # Resource healthy - use generous tit-for-tat
    IF CR >= 0.5 THEN COOPERATE
    ELSE:
        # Probabilistic forgiveness: cooperate with probability equal to CR
        # This gives defectors a chance to recover cooperation
        COOPERATE with probability CR, otherwise DEFECT
```

### Final Round (Round r): Conditional Defection

```
IF SH >= 0.75 AND CR >= 0.75 in round r-1 THEN:
    # High cooperation maintained - reward with continued cooperation
    COOPERATE
ELSE:
    # Standard end-game: defect since no future rounds
    DEFECT
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | COOPERATE | Payoff is 0 either way; cooperation signals intent for if stock recovers |
| n = 2 (minimum players) | Use stricter CR threshold (0.6) | Single defector has larger impact |
| r = 2 (minimum rounds) | Round 1: C, Round 2: Mirror opponent's R1 choice | Simple reciprocity |
| All others defected last round | COOPERATE if SH < 0.3, else DEFECT | Protect critically low resources; otherwise match defection |
| Stock near capacity after defections | COOPERATE | Resource is healthy; attempt to restart cooperation |

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, history):
    n = number_of_players
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate metrics
    CR = cooperation_rate(history, round - 1)
    SH = stock / capacity
    
    # Final round logic
    if round == total_rounds:
        if SH >= 0.75 and CR >= 0.75:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds: conditional cooperation
    if SH < 0.25:
        return COOPERATE  # Protect critically low resource
    elif SH < 0.50:
        return COOPERATE if CR >= 0.4 else DEFECT
    else:  # SH >= 0.50
        if CR >= 0.5:
            return COOPERATE
        else:
            # Probabilistic forgiveness
            return COOPERATE if random() < CR else DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Sustainability-first**: Prioritizes resource health, ensuring payoffs exist in future rounds
2. **Signals cooperative intent**: Starting with cooperation invites reciprocity
3. **Proportional response**: Doesn't over-punish occasional defection
4. **Forgiveness mechanism**: Probabilistic cooperation allows recovery from defection spirals
5. **Protects the commons**: When stock is critical, always cooperates regardless of others
6. **Adapts to exploitation**: Will defect against persistent defectors when resource is healthy
7. **Rewards sustained cooperation**: Final-round cooperation if community maintained high cooperation
'''

description_COLLECTIVE_81 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the shared resource is our common wealth, and its preservation benefits everyone across all rounds. While I cannot coordinate directly with others, I can signal cooperative intent, respond proportionally to observed behavior, and maintain the resource's regenerative capacity.

## Strategy: "Sustainable Steward with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to preserve the resource and signal collective intent
2. **Respond to resource health** - protect the commons when threatened
3. **Graduated forgiveness** - allow recovery from defection while maintaining accountability

### Decision Rules

```
EACH ROUND:

1. Calculate key metrics:
   - stock_ratio = current_stock / capacity
   - rounds_remaining = r - current_round
   - historical_cooperation_rate = (total C plays by all players) / (total plays)
   
2. FIRST ROUND:
   → Play C (signal cooperative intent, no history to react to)

3. LAST ROUND:
   → If stock_ratio ≥ 0.5 AND historical_cooperation_rate ≥ 0.6:
        Play C (reward collective success)
   → Else:
        Play D (no future to preserve)

4. MIDDLE ROUNDS - Apply in order:

   a) EMERGENCY PROTECTION:
      If stock_ratio < 0.25:
         → Play C (resource critically low; any defection risks collapse)
   
   b) REACTIVE THRESHOLD:
      Calculate last_round_defection_rate = (D plays last round) / n
      
      If last_round_defection_rate > 0.5:
         → Play D (majority defected; protect self while signaling displeasure)
      
   c) TREND-BASED RESPONSE:
      If stock is declining for 2+ consecutive rounds AND stock_ratio < 0.6:
         → Play D (unsustainable trajectory; shock response)
      
   d) FORGIVENESS MECHANISM:
      If I played D last round AND last_round_defection_rate ≤ 0.5:
         → Play C (return to cooperation when others show restraint)
   
   e) DEFAULT:
      → Play C (sustain the resource)
```

### Rationale for Each Component

**First Round Cooperation**: Establishes cooperative reputation with no information loss. The stock starts at capacity, so even if others defect, the resource survives.

**Emergency Protection (stock < 25%)**: When the resource is near collapse, even selfish players benefit from cooperation—defection yields little from a depleted stock. Cooperating here preserves any chance of recovery.

**Reactive Threshold (>50% defection)**: If most players defected, continuing to cooperate alone is exploitation without benefit. Defecting signals that cooperation requires reciprocity.

**Trend-Based Response**: Catches slow degradation that individual-round metrics might miss. A declining stock despite moderate cooperation rates suggests hidden defection or need for correction.

**Forgiveness**: Prevents permanent defection spirals. One round of punishment followed by return to cooperation allows the group to reset.

**Last Round Logic**: Maintains cooperation incentive even at the end if the collective has succeeded, rewarding sustained cooperation rather than guaranteed end-game defection.

### Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| n = 2 (minimum players) | Same rules | Strategy scales; defection detection is clearer |
| r = 2 (minimum rounds) | Round 1: C, Round 2: per last-round rule | Brief game; signal then respond |
| Stock hits 0 | Play C | No downside; any recovery requires cooperation |
| All others always defect | Eventually settle on D | Reactive threshold triggers consistently |
| All others always cooperate | Always C | No triggers fire; optimal collective outcome |
| Mixed/noisy opponents | Mostly C with occasional D | Forgiveness prevents spirals |

### Why This Strategy Serves the Collective

1. **Preserves the resource**: Default cooperation maintains the regenerative equilibrium where stock replenishes fully each round.

2. **Creates positive-sum outcomes**: If even a moderate fraction of players adopt similar strategies, total payoffs across all rounds far exceed mutual defection.

3. **Robust to exploitation**: The graduated response prevents unlimited exploitation while avoiding hair-trigger retaliation that destroys cooperation.

4. **Self-healing**: Forgiveness mechanisms allow groups to recover from temporary breakdowns.

5. **Adaptive**: Responds to actual behavior rather than assumptions about opponents.
'''

description_COLLECTIVE_82 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that universal cooperation creates a sustainable equilibrium where the stock regenerates fully each round, maximizing long-term payoffs for everyone. My goal is to demonstrate and reinforce this cooperative equilibrium while protecting against exploitation.

## Strategy Overview: "Generous Guardian"

The strategy operates on three principles:
1. **Lead by example** - Default to cooperation to signal and establish sustainable norms
2. **Respond proportionally** - Adjust behavior based on observed collective behavior
3. **Protect the resource** - Intervene when stock depletion threatens future rounds

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists, so extend trust and model the behavior I want to see
- This allows assessment of other players' intentions

### Middle Rounds (2 to r-1):

**Calculate the cooperation rate from the previous round:**
```
coop_rate = (number of C plays in previous round) / n
```

**Decision logic:**

1. **If coop_rate ≥ (n-1)/n** (at most one defector):
   - **Cooperate** — The collective norm is strong; maintain it

2. **If coop_rate ≥ 0.5 and stock ≥ capacity/2:**
   - **Cooperate with probability = coop_rate**
   - This mirrors the collective behavior probabilistically, rewarding cooperation trends while introducing measured caution

3. **If coop_rate < 0.5 or stock < capacity/3:**
   - **Defect** — The cooperative equilibrium has collapsed or the resource is critically depleted; extract value before it's gone

4. **Stock emergency override:**
   - If stock < capacity/4 AND coop_rate < 0.75: **Defect**
   - If stock < capacity/4 AND coop_rate ≥ 0.75: **Cooperate** (attempt recovery)

### Final Round (round r):
- **Cooperate if** the majority cooperated in round r-1 AND stock remains above capacity/3
- **Defect otherwise** — No future rounds exist to punish defection, but maintaining cooperation signals principled play and may matter in tournament scoring

---

## Pseudocode

```
function decide(round, history, stock, n, r, capacity):
    
    if round == 1:
        return COOPERATE
    
    prev_round_actions = history[round - 1]
    coop_count = count(prev_round_actions == COOPERATE)
    coop_rate = coop_count / n
    
    # Stock-based emergency conditions
    stock_ratio = stock / capacity
    
    if round == r:  # Final round
        if coop_rate > 0.5 and stock_ratio > 0.33:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds
    if coop_rate >= (n-1)/n:
        return COOPERATE
    
    if stock_ratio < 0.25:
        if coop_rate >= 0.75:
            return COOPERATE  # Attempt collective recovery
        else:
            return DEFECT  # Resource collapse imminent
    
    if coop_rate >= 0.5 and stock_ratio >= 0.5:
        return COOPERATE with probability coop_rate
        # (i.e., random() < coop_rate ? COOPERATE : DEFECT)
    
    return DEFECT
```

---

## Handling Edge Cases

| Scenario | Action | Rationale |
|----------|--------|-----------|
| First round | Cooperate | Establish cooperative norm |
| Last round with healthy stock & cooperation | Cooperate | Principled consistency |
| Last round with depleted stock or defection | Defect | No future incentive to cooperate |
| Stock near zero | Defect (unless high cooperation) | Resource effectively destroyed |
| Single defector in large group | Cooperate | Outlier shouldn't collapse norms |
| n=2 (minimum players) | More sensitive thresholds | One defection = 50% defection rate |

---

## Why This Strategy Aligns with Collective Welfare

1. **Sustainability focus**: Universal cooperation keeps stock at capacity indefinitely, yielding capacity/(2n) per player per round — the maximum sustainable yield

2. **Forgiveness**: The probabilistic response and high tolerance for single defectors prevent death spirals

3. **Clear signaling**: Consistent early cooperation communicates intent without requiring coordination

4. **Adaptive protection**: When cooperation fails, the strategy protects individual payoffs while remaining ready to return to cooperation

This strategy aims to be the player that others can rely on for sustainable collective outcomes, while remaining robust against exploitation.
'''

description_COLLECTIVE_83 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt it, the resource remains sustainable and everyone benefits long-term. The strategy balances cooperation for sustainability with protective defection when the commons is being exploited.

## Strategy Overview: "Adaptive Guardian"

The strategy monitors resource health and collective behavior to make decisions. It cooperates to maintain sustainability but shifts to defection when either (1) the resource is critically depleted, or (2) widespread defection makes cooperation futile.

---

## Decision Rules

### Primary Decision Variables

1. **Resource Health Ratio**: `health = stock / capacity`
2. **Cooperation Rate** (from last round): `coop_rate = cooperators / n`
3. **Trend**: Is cooperation increasing, stable, or declining?

### Decision Logic

```
FUNCTION decide(round, stock, capacity, n, r, history):
    
    health = stock / capacity
    rounds_remaining = r - round + 1
    
    # === FIRST ROUND ===
    IF round == 1:
        RETURN COOPERATE  # Signal cooperative intent
    
    # === LAST ROUND ===
    IF round == r:
        # Cooperate if resource is healthy and others have been cooperative
        IF health > 0.5 AND average_coop_rate(history) > 0.5:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # === CRITICAL RESOURCE STATE ===
    # If stock is dangerously low, harvest what remains
    IF health < 0.15:
        RETURN DEFECT  # Resource likely doomed anyway
    
    # === ANALYZE RECENT BEHAVIOR ===
    last_coop_rate = cooperation_rate(history, last_round)
    recent_coop_rate = cooperation_rate(history, last_3_rounds)
    trend = last_coop_rate - recent_coop_rate  # positive = improving
    
    # === HEALTHY RESOURCE (health > 0.7) ===
    IF health > 0.7:
        # Resource is fine - cooperate unless defection is rampant
        IF last_coop_rate >= 0.4:
            RETURN COOPERATE
        ELSE:
            # Too many defectors - protect yourself but give chance
            IF trend > 0.1:  # Improving
                RETURN COOPERATE
            ELSE:
                RETURN DEFECT
    
    # === MODERATE RESOURCE (0.4 < health <= 0.7) ===
    IF health > 0.4:
        # Need higher cooperation threshold
        IF last_coop_rate >= 0.6:
            RETURN COOPERATE
        ELIF last_coop_rate >= 0.4 AND trend > 0:
            RETURN COOPERATE  # Give benefit of doubt if improving
        ELSE:
            RETURN DEFECT
    
    # === LOW RESOURCE (0.15 <= health <= 0.4) ===
    # Critical zone - only cooperate if strong cooperation signals
    IF last_coop_rate >= 0.75:
        RETURN COOPERATE  # Collective trying to recover
    ELSE:
        RETURN DEFECT  # Can't afford to be exploited
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline; no history to react to |
| **Last round** | Conditional | Cooperate if resource healthy AND history shows cooperation; otherwise defect |
| **Stock near zero** | Defect | Resource cannot recover; harvest remaining value |
| **Stock at capacity** | Cooperate | Optimal sustainability point; no pressure to defect |
| **All previous defected** | Defect | Cooperation would be pure sacrifice |
| **Mixed history** | Use trend | Weight recent improvement/decline heavily |

---

## Why This Strategy Works Collectively

1. **If everyone uses this strategy**: All cooperate in round 1, resource stays at capacity, all continue cooperating → maximum sustainable yield for everyone.

2. **Against defectors**: Quickly matches defection to avoid exploitation, but remains willing to return to cooperation if behavior improves.

3. **Resource-aware**: Ties decisions to actual resource state, not just opponent behavior. Protects the commons when healthy, extracts value when doomed.

4. **Forgiveness built in**: The trend analysis allows recovery from mutual defection spirals if others start cooperating again.

---

## Summary

**Cooperate when**: Resource is healthy AND others are reasonably cooperative (or improving).

**Defect when**: Resource is critically low OR defection is widespread and not improving.
'''

description_COLLECTIVE_84 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The key insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the resource regenerates fully each round, maximizing total payoffs across all rounds. Any defection degrades the commons for everyone, including the defector in future rounds.

## Strategy Name: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to signal collective intent and preserve the resource
2. **Respond proportionally** to observed behavior - mirror the collective tendency
3. **Protect the commons** more aggressively as stock depletes or endgame approaches

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists, so extend trust
- This maximizes the chance of establishing cooperative norms
- Preserves full stock for future rounds

### Middle Rounds (2 to r-1):

**Calculate cooperation rate from previous round:**
```
coop_rate = (number of C plays last round) / n
```

**Calculate stock health:**
```
stock_health = current_stock / capacity
```

**Decision logic:**

```
IF coop_rate >= (n-1)/n THEN
    # Near-universal cooperation: maintain it
    COOPERATE

ELSE IF coop_rate >= 0.5 THEN
    # Majority cooperating: cooperate to encourage norm
    # But introduce small probability of defection if stock is healthy
    # to avoid being exploited indefinitely
    IF stock_health >= 0.8 AND consecutive_high_coop_rounds >= 3 THEN
        COOPERATE
    ELSE
        COOPERATE

ELSE IF coop_rate > 0 THEN
    # Mixed behavior: match the cooperation rate probabilistically
    # This creates pressure toward cooperation without full retaliation
    COOPERATE with probability = coop_rate + 0.1
    (the +0.1 bias toward cooperation helps recovery)

ELSE (coop_rate == 0)
    # Universal defection: defect to avoid exploitation
    # But every 3rd round, try cooperating to test for recovery
    IF round_number % 3 == 0 THEN
        COOPERATE (olive branch)
    ELSE
        DEFECT
```

**Stock emergency override:**
```
IF stock_health < 0.3 THEN
    # Resource critically depleted - cooperate to save it
    # Unless others are actively destroying it
    IF coop_rate >= 0.3 THEN
        COOPERATE (attempt recovery)
    ELSE
        DEFECT (resource likely doomed, minimize loss)
```

### Final Round (round r):

**Standard game theory suggests defecting, but collective strategy considers:**

```
IF stock_health >= 0.5 AND historical_coop_rate >= 0.7 THEN
    # Good stewardship maintained - honor the collective
    COOPERATE
ELSE
    # Mixed history or depleted stock - take fair share
    DEFECT
```

*Rationale: If playing against other collective-minded agents, mutual final-round cooperation leaves everyone better positioned. The reputation for consistency matters even in the last round.*

---

## Pseudocode Summary

```python
def decide(round, total_rounds, n, stock, capacity, history):
    
    # Round 1: unconditional cooperation
    if round == 1:
        return COOPERATE
    
    # Calculate metrics
    last_round_actions = history[-1]
    coop_rate = count(C in last_round_actions) / n
    stock_health = stock / capacity
    
    # Stock emergency: prioritize resource survival
    if stock_health < 0.3:
        if coop_rate >= 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    # Final round
    if round == total_rounds:
        historical_coop = average_coop_rate(history)
        if stock_health >= 0.5 and historical_coop >= 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds: graduated response
    if coop_rate >= (n-1)/n:
        return COOPERATE
    elif coop_rate >= 0.5:
        return COOPERATE
    elif coop_rate > 0:
        return COOPERATE with probability (coop_rate + 0.1)
    else:  # coop_rate == 0
        if round % 3 == 0:
            return COOPERATE  # periodic olive branch
        else:
            return DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Sustainability**: Prioritizes keeping stock at regenerative levels
2. **Forgiveness**: The +0.1 cooperation bias and periodic olive branches allow recovery from defection spirals
3. **Proportionality**: Doesn't over-punish occasional defection, which could trigger destructive retaliation cycles
4. **Robustness**: Protects against persistent exploiters while remaining open to cooperation
5. **Collective alignment**: When matched against similar strategies, achieves near-optimal collective outcomes
'''

description_COLLECTIVE_85 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The key insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully each round, maximizing total payoffs across all rounds. Any defection depletes the resource, reducing future payoffs for everyone including the defector.

## Strategic Framework: "Generous Guardian"

### Decision Rules

**Primary Rule: Conditional Cooperation with Forgiveness**

```
IF first_round:
    COOPERATE (signal cooperative intent)

ELSE IF last_round:
    COOPERATE (preserve collective outcome, avoid destructive endgame)

ELSE IF stock < capacity * 0.3:
    COOPERATE (emergency preservation mode)

ELSE IF stock >= capacity * 0.8:
    # Resource is healthy - use proportional response
    IF defection_rate_last_round <= 1/n:
        COOPERATE (tolerate isolated defection)
    ELSE IF defection_rate_last_3_rounds < 0.25:
        COOPERATE (forgive if trend is cooperative)
    ELSE:
        DEFECT (proportional response to sustained defection)

ELSE:  # stock between 30% and 80% of capacity
    # Resource under moderate stress
    IF no_defections_last_round:
        COOPERATE
    ELSE IF defection_rate_last_round < 0.5 AND stock_trend_positive:
        COOPERATE (reward recovery efforts)
    ELSE:
        DEFECT (protect against exploitation)
```

### Key Mechanisms

1. **Unconditional First-Round Cooperation**: Establishes cooperative norm and provides information about others' strategies without assuming coordination.

2. **Forgiveness Threshold**: Tolerates up to 1 defector per round when resources are healthy - this accounts for noise, mistakes, or rogue actors without triggering collective collapse.

3. **Stock-Aware Responses**: 
   - When stock is critically low (<30%), always cooperate regardless of others' behavior - defection here accelerates collapse that hurts everyone
   - When stock is high (>80%), can afford measured responses to defection

4. **Trend Analysis**: Considers 3-round moving average of defection rates rather than just last round - avoids overreacting to single-round anomalies.

5. **Cooperative Endgame**: Unlike standard game theory suggesting defection in final rounds, this strategy cooperates in the last round because:
   - If others also think collectively, mutual cooperation yields best outcome
   - The marginal gain from defecting in one round rarely compensates for the signal it sends

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| Round r (final) | C | Collective outcome over individual exploitation |
| Stock = 0 | C | No benefit to defection; cooperation allows any regrowth |
| All others defected last round | C if stock < 30%, else D | Preserve dying resource, or proportional response |
| Stock at capacity, no prior defections | C | Optimal sustainable equilibrium |
| Single defector in otherwise cooperative game | C | Generous tolerance |

### Robustness Features

- **Against Always-Defect**: Will eventually defect in response, limiting exploitation, but returns to cooperation if opponent changes
- **Against Always-Cooperate**: Maintains cooperation, achieving optimal collective outcome
- **Against Tit-for-Tat variants**: Cooperates, avoiding defection spirals
- **Against Random strategies**: Forgiveness mechanism prevents lock-in to mutual defection
- **Against Exploitation attempts**: Stock-aware thresholds ensure self-protection when resources are healthy

## Summary

**Cooperate by default. Forgive generously. Protect the resource first. Never defect in desperation or spite.**

This strategy succeeds by recognizing that in a repeated common pool game, the resource itself is the primary stakeholder - protecting it protects everyone's long-term interests, including our own.
'''

description_COLLECTIVE_86 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared life-support system. The fundamental insight is that **sustainable harvesting (all cooperate) maintains the resource indefinitely**, while defection creates a tragedy of the commons. My strategy aims to:

1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but allow redemption
4. Recognize when cooperation is futile and adapt

## Strategy: "Guardian with Graduated Response"

### Decision Framework

```
COOPERATE if ANY of the following are true:
  - First round (establish cooperative norm)
  - Stock is critically low (emergency conservation)
  - Recent history shows sufficient cooperation
  - We're in a "forgiveness window" after punishment

DEFECT if ALL of the following are true:
  - Not in first round
  - Stock is above critical threshold
  - Defection rate exceeds tolerance threshold
  - Not in forgiveness window
```

### Detailed Rules

#### 1. **First Round: Always Cooperate**
Establish cooperative intent. This is a clear, observable signal that costs relatively little (forgoing 12.5 vs 25 in the example) but communicates willingness to sustain the resource.

#### 2. **Stock Emergency Protocol**
```
critical_threshold = capacity * 0.25

IF stock < critical_threshold:
    COOPERATE (regardless of history)
```
When the resource is near collapse, defection accelerates disaster. Even if others defect, cooperating preserves any chance of recovery. This is collective self-preservation.

#### 3. **Main Decision Logic (Rounds 2 through r-1)**

Calculate the **cooperation rate** from the previous round:
```
cooperation_rate = (number of C plays) / n
```

Calculate **rolling cooperation rate** over last min(3, rounds_played) rounds for stability.

**Tolerance Threshold** (adaptive):
```
base_tolerance = 0.5  # Expect at least half to cooperate
stock_adjustment = (stock / capacity) * 0.2  # More lenient when stock is healthy
tolerance = base_tolerance - stock_adjustment
```

**Decision:**
```
IF rolling_cooperation_rate >= tolerance:
    COOPERATE
ELSE:
    Enter graduated response
```

#### 4. **Graduated Response Protocol**

When cooperation falls below tolerance:

```
defection_severity = 1 - rolling_cooperation_rate  # 0 to 1 scale
consecutive_low_cooperation = count consecutive rounds below tolerance

IF consecutive_low_cooperation == 1:
    COOPERATE (one-round forgiveness, allow correction)
ELIF consecutive_low_cooperation <= 3:
    DEFECT with probability = defection_severity
    COOPERATE otherwise
ELSE:
    DEFECT (sustained non-cooperation detected)
```

This graduated approach:
- Gives one free pass (noise tolerance)
- Matches punishment to severity
- Eventually commits to defection if cooperation clearly failed

#### 5. **Forgiveness Window**

After defecting for `k` consecutive rounds:
```
IF k >= 2 AND k % 3 == 0:
    COOPERATE (test for renewed cooperation)
    Reset consecutive defection counter if others cooperate
```

This periodic olive branch allows escape from mutual defection spirals.

#### 6. **Last Round Consideration**

```
IF round == r (final round):
    IF rolling_cooperation_rate >= 0.7 AND stock >= capacity * 0.5:
        COOPERATE (reward sustained cooperation, collective finish)
    ELSE:
        DEFECT (no future rounds to protect)
```

The threshold is high because there's no future punishment for last-round defection. Only reward genuinely cooperative groups.

### Pseudocode Summary

```python
def decide(round, stock, capacity, n, history):
    # Round 1: Establish cooperation
    if round == 1:
        return COOPERATE
    
    # Emergency conservation
    if stock < capacity * 0.25:
        return COOPERATE
    
    # Calculate cooperation metrics
    rolling_coop_rate = avg_cooperation_rate(history, window=3)
    tolerance = 0.5 - (stock / capacity) * 0.2
    consecutive_low = count_consecutive_below_tolerance(history, tolerance)
    
    # Last round logic
    if round == r:
        if rolling_coop_rate >= 0.7 and stock >= capacity * 0.5:
            return COOPERATE
        return DEFECT
    
    # Main logic
    if rolling_coop_rate >= tolerance:
        return COOPERATE
    
    # Graduated response
    if consecutive_low == 1:
        return COOPERATE  # One-time forgiveness
    
    if consecutive_low <= 3:
        defect_prob = 1 - rolling_coop_rate
        return DEFECT with probability defect_prob, else COOPERATE
    
    # Check forgiveness window
    consecutive_defections = count_my_consecutive_defections(history)
    if consecutive_defections >= 2 and consecutive_defections % 3 == 0:
        return COOPERATE
    
    return DEFECT
```

### Why This Strategy is Collectively Aligned

1. **Starts cooperative**: Clear pro-social signal
2. **Protects the commons**: Emergency protocol prevents collapse
3. **Tolerant but not exploitable**: Graduated response balances forgiveness with deterrence
4. **Self-correcting**: Forgiveness windows prevent permanent mutual destruction
5. **Adaptive**: Tolerance adjusts based on resource health
6. **Rewards collective success**: Only defects in final round if cooperation already failed
'''

description_COLLECTIVE_87 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, we should achieve near-optimal sustainable outcomes. However, it must also be **robust** against defectors and **adaptive** to the actual behavior observed in the game.

The key insight is that universal cooperation maintains the stock at capacity indefinitely (as shown in Example 1), maximizing total group payoffs across all rounds. But we must protect against exploitation while remaining forgiving enough to restore cooperation when possible.

---

## Strategy: "Sustainable Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperative** to establish sustainable harvesting
2. **Protect the commons** by responding to defection proportionally
3. **Prioritize long-term sustainability** over short-term gains, except when the end is near

---

### Decision Rules

#### Round 1: Always Cooperate
- No history exists; cooperation signals collective intent
- Establishes baseline for sustainable harvesting

#### Rounds 2 through (r-1): Conditional Cooperation

**Cooperate if ALL of the following are true:**
1. **Recent cooperation threshold met**: At least 50% of all players cooperated in the previous round
2. **Stock health adequate**: Current stock ≥ capacity × 0.3 (resource not critically depleted)
3. **No sustained defection pattern**: The number of defections in the last min(3, current_round-1) rounds doesn't exceed 60% of total actions in that window

**Defect if ANY of the following are true:**
1. **Widespread defection**: More than 50% of players defected last round
2. **Critical stock depletion**: Stock < capacity × 0.3 AND at least one player defected last round
3. **Sustained exploitation**: Defection rate over recent history exceeds 60%

#### Final Round (Round r): Conditional Based on History

**Cooperate if:**
- Overall cooperation rate across all previous rounds ≥ 70%
- AND current stock ≥ capacity × 0.5

**Defect otherwise:**
- In a one-shot scenario with no future, defection is dominant
- But if cooperation has been sustained, maintaining it preserves collective trust for potential future interactions and reflects our collective commitment

---

### Pseudocode

```
function decide(round, stock, history, n, r, capacity):
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate metrics from history
    last_round_defections = count_defections(history, round - 1)
    last_round_coop_rate = 1 - (last_round_defections / n)
    
    recent_window = min(3, round - 1)
    recent_defection_rate = count_defections_in_window(history, recent_window) / (n * recent_window)
    
    overall_coop_rate = count_all_cooperations(history) / (n * (round - 1))
    
    stock_ratio = stock / capacity
    
    # Final round logic
    if round == r:
        if overall_coop_rate >= 0.7 AND stock_ratio >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds logic
    # Check for defection triggers
    if last_round_coop_rate < 0.5:
        return DEFECT  # Respond to widespread defection
    
    if stock_ratio < 0.3 AND last_round_defections > 0:
        return DEFECT  # Protect critically low stock
    
    if recent_defection_rate > 0.6:
        return DEFECT  # Counter sustained exploitation
    
    # Default: Cooperate for sustainability
    return COOPERATE
```

---

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative baseline |
| Stock = 0 | Cooperate | Payoff is 0 regardless; cooperation signals willingness to let stock recover |
| Stock near capacity | Follow standard rules | Don't get complacent; maintain vigilance |
| Single defector appears | Cooperate | One defector doesn't trigger response; forgiveness enables recovery |
| Majority defects once | Defect once | Proportional response; return to cooperation if they do |
| n = 2 (two players) | Standard rules apply | Thresholds work; 50% means the other player |
| Very short game (r ≤ 3) | Standard rules, but final round logic kicks in earlier | Adapts naturally |

---

### Why This Strategy is Collectively Optimal

**If all players use this strategy:**
- Everyone cooperates every round
- Stock remains at capacity (100% regeneration when half is harvested)
- Each player earns capacity/(2n) per round for r rounds
- Total collective payoff is maximized

**Against defectors:**
- Strategy doesn't allow unlimited exploitation
- Responds proportionally, creating incentive for others to cooperate
- Recovers cooperation when defectors return to cooperative play
'''

description_COLLECTIVE_88 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared commons where collective restraint enables long-term prosperity for all. The goal is to maximize sustainable collective payoffs while protecting against exploitation. I will signal cooperative intent, reward cooperation, and respond proportionally to defection—but always with an eye toward preserving the resource that sustains everyone.

## Strategy: "Sustainable Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Preserve the commons**: Protect stock levels that enable regeneration
2. **Conditional cooperation**: Cooperate by default, but respond to exploitation
3. **Forgiveness with memory**: Allow recovery from defection but track patterns

---

### Decision Rules

#### Round 1: Always Cooperate
- Signal cooperative intent to establish trust
- No information exists about others yet
- Cooperation is the only way to discover if collective sustainability is possible

#### Middle Rounds (2 to r-1):

**Calculate the following metrics:**

```
cooperation_rate = (total C actions by all players in all previous rounds) / 
                   (n × rounds_played)

stock_health = current_stock / capacity

recent_defection_rate = (D actions in last round) / n
```

**Decision Logic:**

```
IF stock_health < 0.25:
    # CRISIS MODE - Resource near collapse
    COOPERATE (attempt to save the commons)

ELSE IF cooperation_rate >= 0.7 AND recent_defection_rate <= 0.3:
    # HEALTHY COOPERATION - Reward collective restraint
    COOPERATE

ELSE IF cooperation_rate >= 0.5 AND stock_health >= 0.5:
    # MODERATE COOPERATION - Continue cooperating to encourage others
    COOPERATE

ELSE IF cooperation_rate < 0.5 AND recent_defection_rate > 0.5:
    # EXPLOITATION DETECTED - Proportional response
    IF stock_health >= 0.6:
        DEFECT (protect against being exploited while resource is healthy)
    ELSE:
        COOPERATE (prioritize resource survival over punishment)

ELSE:
    # UNCERTAIN SITUATION - Default to cooperation
    COOPERATE
```

#### Last Round (r):

```
IF cooperation_rate >= 0.6 throughout the game:
    # Honor sustained cooperation - maintain trust
    COOPERATE
ELSE:
    # Mixed or exploitative history
    DEFECT (no future rounds to punish retaliation)
```

---

### Edge Cases

1. **Stock = 0**: Action is irrelevant (payoff will be 0 regardless), but choose COOPERATE to signal intent if stock somehow recovers.

2. **Stock near capacity with high cooperation**: Continue cooperating—the system is working as intended.

3. **Single defector pattern**: If only 1 player consistently defects while others cooperate, continue cooperating if stock_health > 0.5 (the resource can sustain one free-rider; punishing risks cascading defection).

4. **Oscillating behavior**: If cooperation_rate ≈ 0.5 and fluctuating, cooperate to break negative cycles.

5. **n = 2 (two players)**: Be more responsive to partner's actions:
   - Mirror previous round's opponent action (tit-for-tat element)
   - But still prioritize cooperation when stock_health < 0.4

---

### Rationale for Collective Alignment

This strategy embodies collective thinking by:

1. **Starting cooperative**: Gives the group the best chance to establish mutual restraint
2. **Protecting the resource over punishing**: When stock is low, preserving the commons takes priority over retaliation
3. **High forgiveness threshold**: Requires sustained exploitation before responding with defection
4. **Last-round honor**: Rewards groups that maintained cooperation, rather than automatically defecting
5. **Tolerating minor defection**: Accepts some free-riding if the resource remains healthy, avoiding destructive punishment spirals

The strategy assumes that if all players reason similarly about collective welfare, they will converge on sustainable cooperation. Against exploitative strategies, it protects itself while still attempting to preserve the resource that benefits everyone—including defectors who may eventually recognize the value of cooperation.
'''

description_COLLECTIVE_89 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation sustains the resource indefinitely at maximum capacity**, while defection creates a tragedy of the commons. My strategy aims to be a "sustainable steward" - cooperating by default to maintain the resource, but responding proportionally to exploitation to avoid being purely exploited.

## Decision Rules

### Primary Rule: Conditional Cooperation with Forgiveness

**Cooperate (C)** unless there is clear evidence of sustained exploitation that threatens resource collapse.

### Detailed Decision Logic

```
FUNCTION decide(round, history, stock, capacity, n, r):
    
    # Calculate key metrics
    rounds_remaining = r - round
    stock_ratio = stock / capacity
    
    # FIRST ROUND: Always cooperate to establish goodwill
    if round == 1:
        return C
    
    # FINAL ROUND: Cooperate if stock is healthy, defect only if resource is already collapsing
    if rounds_remaining == 0:
        if stock_ratio >= 0.5:
            return C  # Maintain cooperative reputation even at the end
        else:
            return D  # Resource already degraded, extract remaining value
    
    # CRITICAL STOCK THRESHOLD: If stock is dangerously low, cooperate to allow recovery
    if stock_ratio < 0.25:
        return C  # Prioritize resource recovery over punishment
    
    # ANALYZE RECENT HISTORY (last 3 rounds or available history)
    lookback = min(3, round - 1)
    recent_defection_rate = count_defections_in_last_n_rounds(history, lookback) / (n * lookback)
    
    # GENEROUS THRESHOLD: Only defect if defection is widespread and persistent
    if recent_defection_rate > 0.5:
        # Majority are defecting - match their behavior but with probability
        # This creates pressure without fully abandoning cooperation
        if recent_defection_rate > 0.75:
            return D  # Heavy exploitation - protect self
        else:
            # Probabilistic response: defect with probability equal to defection rate
            # This allows gradual de-escalation
            return D if random() < recent_defection_rate else C
    
    # TREND ANALYSIS: Reward improvement
    if round >= 4:
        older_defection_rate = count_defections_in_rounds(history, round-6, round-4) / (n * 3) if round > 6 else recent_defection_rate
        if recent_defection_rate < older_defection_rate:
            return C  # Defection is decreasing - encourage this trend
    
    # DEFAULT: Cooperate
    return C
```

## Edge Case Handling

### First Round
**Always Cooperate.** This signals cooperative intent and gives others the opportunity to coordinate on the sustainable equilibrium. Starting with defection poisons the well.

### Last Round
**Cooperate if stock ≥ 50% capacity; otherwise Defect.** This avoids the standard backward induction collapse. By committing to cooperation even in the final round when the resource is healthy, we signal that we value collective outcomes over individual exploitation. This also makes cooperation in earlier rounds more credible.

### Very Low Stock (< 25% capacity)
**Always Cooperate.** When the resource is near collapse, the priority shifts to recovery. Even if others defect, my cooperation gives the stock a chance to regenerate. Defecting at low stock accelerates collapse and hurts everyone.

### High Stock (> 75% capacity)
**Maintain cooperation more stubbornly.** When the resource is abundant, the system can absorb some defection. Be more forgiving here to allow potential cooperators to re-coordinate.

### Early Rounds (rounds 2-4)
**Weight toward cooperation with short memory.** Don't overreact to early defection - some players may be "testing" or using different strategies. Give the collective time to settle into a pattern.

## Why This Strategy Aligns with Collective Interest

1. **Sustainability**: Universal C maintains stock at capacity indefinitely (growth exactly offsets consumption)

2. **Robustness**: Responds to exploitation without triggering collapse spirals

3. **Forgiveness**: Allows recovery from defection cycles - doesn't hold permanent grudges

4. **Signal clarity**: Consistent cooperation makes it easy for other cooperative strategies to identify and coordinate with us

5. **Proportional response**: Matches exploitation level rather than overreacting, preserving possibility of return to cooperation

The strategy optimizes for the scenario where enough players adopt similar "sustainable steward" approaches to maintain the resource, while protecting against pure exploitation through measured reciprocity.
'''

description_COLLECTIVE_90 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: we assume all players using this strategy share the same decision rules and will naturally coordinate through identical reasoning. Our primary goal is **sustainable resource management** that maximizes long-term collective payoffs while remaining robust against defectors.

## Strategy Overview: "Threshold Guardian"

The strategy uses stock levels as coordination signals and employs conditional cooperation with graduated responses to defection.

---

## Decision Rules

### Primary Decision Rule

```
IF stock >= capacity * 0.5:
    Use COOPERATION-ORIENTED mode
ELSE:
    Use PROTECTION mode
```

### Mode 1: Cooperation-Oriented (Healthy Stock)

When resources are abundant (stock ≥ 50% capacity):

1. **Default to COOPERATE** unless defection is detected
2. **Defection Detection**: If in the previous round, observed consumption exceeded what full cooperation would produce (i.e., total consumption > stock_prev / 2), defectors are present
3. **Graduated Response**:
   - If defection detected in 1 of last 3 rounds: still COOPERATE (forgive noise)
   - If defection detected in 2+ of last 3 rounds: DEFECT (protect fair share)

### Mode 2: Protection (Depleted Stock)

When resources are stressed (stock < 50% capacity):

1. **If stock > capacity * 0.25**: COOPERATE to allow recovery
2. **If stock ≤ capacity * 0.25**: DEFECT (crisis extraction - get something before collapse)

### Edge Cases

**First Round:**
- Always COOPERATE
- Rationale: Establishes cooperative intent; stock is at capacity so no crisis

**Last Round:**
- If playing against apparent cooperators (no defection in last 3 rounds): COOPERATE
- Otherwise: DEFECT
- Rationale: Maintain reputation consistency; defecting only against known defectors

**Second-to-Last Round:**
- Apply normal rules (no special endgame defection)
- Rationale: Collective mindset means we don't exploit predictable endings

**Stock = 0:**
- Action is irrelevant (payoff is 0 regardless)
- Choose COOPERATE (signals intent if stock somehow recovers)

---

## Pseudocode

```python
def decide(game_params, current_stock, history):
    n = game_params.n
    capacity = game_params.capacity
    current_round = len(history) + 1
    total_rounds = game_params.r
    
    # First round: always cooperate
    if current_round == 1:
        return COOPERATE
    
    # Count recent defection rounds (last 3 rounds)
    defection_rounds = 0
    lookback = min(3, len(history))
    
    for t in range(lookback):
        round_data = history[-(t+1)]
        stock_at_round = round_data.stock
        total_consumed = round_data.total_consumption
        expected_if_all_coop = stock_at_round / 2
        
        # Allow 5% tolerance for floating point
        if total_consumed > expected_if_all_coop * 1.05:
            defection_rounds += 1
    
    # Protection mode: stock critically low
    if current_stock < capacity * 0.25:
        return DEFECT
    
    # Recovery mode: stock depleted but recoverable
    if current_stock < capacity * 0.5:
        return COOPERATE
    
    # Cooperation-oriented mode: healthy stock
    # Last round special handling
    if current_round == total_rounds:
        if defection_rounds == 0:
            return COOPERATE
        else:
            return DEFECT
    
    # Normal rounds with graduated response
    if defection_rounds >= 2:
        return DEFECT
    else:
        return COOPERATE
```

---

## Why This Strategy Works Collectively

1. **Self-Coordinating**: Identical agents will always cooperate (no defection signals), maintaining stock at capacity indefinitely

2. **Sustainable Equilibrium**: When all use this strategy, stock stays at 100%, each player gets capacity/(2n) per round, maximizing long-term total payoff

3. **Robust to Defectors**: Graduated response prevents exploitation while allowing recovery from occasional defection

4. **Stock as Signal**: Using observable stock levels means no explicit coordination needed - the resource state itself coordinates behavior

5. **Forgiveness Built In**: Single defections are forgiven, enabling return to cooperation after mistakes or testing

6. **Crisis Protocol**: When stock is critically low, extracting resources acknowledges the game may be ending anyway - better to get something than nothing
'''

description_COLLECTIVE_91 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve near-optimal sustainable outcomes. The strategy prioritizes long-term resource sustainability while remaining robust against defectors through measured, proportional responses.

## Strategy Name: "Sustainable Threshold Guardian"

### Key Insight

The game has a critical property: when all players cooperate, the stock remains at capacity indefinitely (consumption equals regeneration at full capacity). This is the socially optimal equilibrium. The strategy aims to:
1. Signal cooperative intent and establish sustainable harvesting
2. Protect the resource from collapse through conditional cooperation
3. Punish defection proportionally but allow recovery

---

## Decision Rules

### Primary Decision Framework

```
FUNCTION decide(game_params, state, history):
    
    n = number of players
    r = total rounds
    t = current round (1-indexed)
    S = current stock
    capacity = maximum stock
    
    # Calculate key thresholds
    critical_threshold = capacity * 0.25
    warning_threshold = capacity * 0.50
    healthy_threshold = capacity * 0.75
    
    # Analyze history if available
    IF t > 1:
        defection_rate = count_defections_last_round(history) / n
        cumulative_defection_trend = analyze_trend(history)
    ELSE:
        defection_rate = 0
        cumulative_defection_trend = 0
```

### Rule 1: First Round - Unconditional Cooperation
```
    IF t == 1:
        RETURN COOPERATE
        # Rationale: Signal cooperative intent, establish baseline
```

### Rule 2: Resource Emergency Protocol
```
    IF S < critical_threshold:
        RETURN COOPERATE
        # Rationale: When resource is critically low, defection accelerates
        # collapse. Even if others defect, cooperating preserves more
        # for potential recovery. Collective survival > individual gain.
```

### Rule 3: Last Round Consideration
```
    IF t == r:
        IF S >= healthy_threshold AND defection_rate <= 0.25:
            RETURN COOPERATE
            # Maintain cooperation if group has been sustainable
        ELSE:
            RETURN DEFECT
            # No future rounds to consider; take fair share
```

### Rule 4: Proportional Response to Defection
```
    IF t > 1:
        # Calculate cooperation probability based on group behavior
        
        IF defection_rate == 0:
            # Everyone cooperated - continue cooperating
            RETURN COOPERATE
            
        ELSE IF defection_rate <= 0.25:
            # Minor defection - maintain cooperation with high probability
            # to avoid spiral, but signal watchfulness
            IF S >= warning_threshold:
                RETURN COOPERATE
            ELSE:
                RETURN COOPERATE with probability 0.9
                
        ELSE IF defection_rate <= 0.5:
            # Moderate defection - graduated response
            IF S >= healthy_threshold:
                RETURN COOPERATE with probability 0.7
            ELSE IF S >= warning_threshold:
                RETURN COOPERATE with probability 0.5
            ELSE:
                RETURN COOPERATE with probability 0.3
                
        ELSE:  # defection_rate > 0.5
            # Majority defecting - protect self but leave door open
            IF S >= healthy_threshold:
                RETURN COOPERATE with probability 0.3
            ELSE:
                RETURN DEFECT
```

### Rule 5: Forgiveness and Recovery
```
    # If defection rate decreased from previous round
    IF defection_rate < previous_defection_rate:
        # Increase cooperation probability by 20% (capped at 1.0)
        # Rationale: Reward movement toward cooperation
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative baseline |
| Last round, healthy stock, cooperative history | Cooperate | Reward sustained cooperation |
| Last round, otherwise | Defect | No future to protect |
| Stock at 0 | Cooperate | Defection yields 0 anyway; cooperation signals intent for recovery |
| Stock near capacity after defection | Cooperate | Resource recovered; fresh start |
| Single defector pattern | Cooperate | Don't punish group for one bad actor |
| All others always defect | Defect (after round 2) | Protect self from exploitation |

---

## Collective Alignment Properties

1. **Self-Enforcing**: If all players use this strategy, they all cooperate every round, achieving maximum sustainable payoff.

2. **Grim Trigger Avoidance**: Unlike strict tit-for-tat, this strategy uses probabilistic responses, preventing permanent defection spirals from single mistakes.

3. **Resource-Aware**: Decision-making incorporates stock level, recognizing that the same action has different consequences at different stock levels.

4. **Forgiving**: Explicitly rewards reduction in defection, allowing groups to recover from early mistakes.

5. **Robust**: Degrades gracefully against pure defectors rather than collapsing immediately.

---

## Expected Behavior in Tournament

- **Against fellow collective strategies**: Sustained cooperation, maximum group payoff
- **Against always-defect**: Limited losses due to proportional withdrawal
- **Against tit-for-tat variants**: Stable cooperation after initial round
- **Against random strategies**: Moderate cooperation, resource-dependent responses
'''

description_COLLECTIVE_92 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve near-optimal sustainable outcomes. However, it must also be **robust** when facing defectors or alternative strategies. The key insight is that the resource regenerates optimally when stock remains at capacity/2, and universal cooperation maintains the stock at capacity indefinitely.

## Strategy: "Sustainable Threshold with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Sustainability First**: Protect the resource base to ensure long-term collective payoffs
2. **Conditional Cooperation**: Cooperate when the collective is cooperating; respond proportionally to defection
3. **Forgiveness with Memory**: Allow recovery but track patterns

---

### Decision Rules

#### Primary Decision Variables
- `stock`: Current stock level
- `capacity`: Maximum sustainable stock
- `n`: Number of players
- `r`: Total rounds
- `t`: Current round (1-indexed)
- `defection_rate`: Proportion of defections observed in previous round
- `cumulative_defection_rate`: Running average of defection rates

#### Round-by-Round Logic

```
FUNCTION decide(stock, capacity, n, r, t, history):
    
    # Calculate key thresholds
    critical_stock = capacity / 4
    danger_stock = capacity / 2
    healthy_stock = capacity * 0.75
    
    # First round: Always cooperate (establish cooperative norm)
    IF t == 1:
        RETURN C
    
    # Calculate defection rates from history
    last_round_defections = count_defections(history, t-1)
    defection_rate = last_round_defections / n
    cumulative_defection_rate = total_defections(history) / ((t-1) * n)
    
    # CRITICAL STOCK PROTECTION
    # If stock is critically low, cooperate to allow recovery
    # (Defecting here guarantees collapse)
    IF stock < critical_stock:
        RETURN C
    
    # ENDGAME LOGIC (last 2 rounds)
    # In final rounds, backward induction suggests defection
    # But collectively, we should cooperate unless heavily exploited
    IF t >= r - 1:
        IF cumulative_defection_rate > 0.4:
            RETURN D  # Too much exploitation, protect self
        ELSE:
            RETURN C  # Maintain collective outcome
    
    # LAST ROUND SPECIFICALLY
    IF t == r:
        # Defect only if we've been consistently exploited
        IF cumulative_defection_rate > 0.3:
            RETURN D
        ELSE:
            RETURN C
    
    # MAIN GAME LOGIC (rounds 2 to r-2)
    
    # Trigger-based response with graduated thresholds
    
    # If everyone cooperated last round, continue cooperating
    IF defection_rate == 0:
        RETURN C
    
    # Moderate defection (1-2 defectors in typical game)
    # Use probabilistic response to avoid coordination failure
    IF defection_rate <= 0.3:
        # Cooperate with high probability to maintain resource
        # But signal displeasure occasionally
        IF stock >= healthy_stock:
            RETURN C  # Resource is healthy, forgive
        ELSE:
            # Probabilistic: cooperate 80% of time
            RETURN C with probability 0.8, else D
    
    # Significant defection (>30% defected)
    IF defection_rate > 0.3 AND defection_rate <= 0.6:
        IF stock >= danger_stock:
            # Resource can sustain some defection
            # Match defection rate probabilistically
            RETURN D with probability (defection_rate), else C
        ELSE:
            # Resource stressed - cooperate to save it
            RETURN C
    
    # Majority defection (>60%)
    IF defection_rate > 0.6:
        # If most are defecting, protect yourself
        # But if stock is critical, everyone must cooperate
        IF stock > danger_stock:
            RETURN D
        ELSE:
            RETURN C  # Attempt to save the resource
```

---

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | C | Establish cooperative norm; no information yet |
| **Last round** | C (unless exploited) | Collective optimum; defect only if cumulative defection > 30% |
| **Stock near zero** | C | Defecting guarantees collapse; cooperation is only hope |
| **Stock at capacity** | Follow main logic | Healthy resource allows normal strategy |
| **All defected last round** | C if stock critical, else D | Prioritize survival over punishment |
| **Single defector pattern** | C | Forgive isolated defection |

---

### Why This Strategy Aligns with Collective Mindset

1. **Universal Adoption Outcome**: If all n players use this strategy:
   - Everyone cooperates in round 1
   - Stock remains at capacity (full regeneration)
   - Everyone continues cooperating through round r
   - Total payoff per player: `r × capacity/(2n)`
   - This is the **maximum sustainable collective outcome**

2. **Robustness to Defectors**: 
   - Graduated response prevents immediate collapse
   - Critical stock protection ensures resource survival
   - Probabilistic elements prevent deterministic exploitation

3. **Forgiveness Promotes Recovery**:
   - After defection, return to cooperation if others do
   - Cumulative tracking prevents repeated exploitation

---

### Summary Decision Tree

```
START
│
├─ Round 1? → COOPERATE
│
├─ Stock < capacity/4? → COOPERATE (save resource)
│
├─ Last 2 rounds?
│   ├─ Heavily exploited (>40% cumulative defection)? → DEFECT
│   └─ Otherwise → COOPERATE
│
└─ Main game:
    ├─ No defection last round? → COOPERATE
    ├─ Low defection (≤30%) + healthy stock? → COOPERATE
    ├─ Low defection + stressed stock? → COOPERATE (80%), DEFECT (20%)
    ├─ Medium defection (30-60%)? → Match defection rate probabilistically
    └─ High defection (>60%) + healthy stock? → DEFECT
        └─ High defection + stressed stock? → COOPERATE
```

This strategy maximizes collective welfare when universally adopted while providing reasonable protection against exploitation.
'''

description_COLLECTIVE_93 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: we recognize that mutual cooperation sustains the resource and maximizes long-term collective payoffs. However, we must be adaptive since we cannot assume others share this understanding. The strategy aims to:

1. Signal cooperative intent and establish sustainable harvesting
2. Protect the resource from collapse when possible
3. Respond proportionally to defection without triggering spirals
4. Recognize when cooperation is futile and adapt accordingly

---

## Strategy: "Guardian with Graduated Response"

### Decision Framework

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- history: list of (my_action, observed_total_defectors) per past round
- n: number of players
- r: total rounds
- capacity: maximum stock

OUTPUT: action ∈ {C, D}
```

### Core Decision Rules

#### Rule 1: Resource Crisis Override
```
IF stock < capacity / (2 * n):
    RETURN C  # Always cooperate when resource is critically low
```
**Rationale**: When stock is dangerously low, defecting accelerates collapse. Even if others defect, cooperating gives the resource any chance of recovery.

#### Rule 2: Final Round
```
IF round == r:
    IF average_defection_rate > 0.6:
        RETURN D  # No future to protect, others aren't cooperating
    ELSE:
        RETURN C  # Maintain cooperative reputation/signal
```
**Rationale**: In the last round, there's no future benefit to cooperation for resource sustainability. However, if the group has been mostly cooperative, we honor that pattern.

#### Rule 3: Opening Rounds (Rounds 1-2)
```
IF round <= 2:
    RETURN C  # Signal cooperative intent
```
**Rationale**: Begin by demonstrating cooperative intent. This gives others the opportunity to establish mutual cooperation.

#### Rule 4: Graduated Response (Main Logic)
```
# Calculate recent defection pressure
recent_window = min(3, round - 1)
recent_defection_rate = avg(defectors_per_round / n) over last recent_window rounds

# Calculate stock health
stock_health = stock / capacity

# Threshold adjustment based on game progress
game_progress = round / r
base_threshold = 0.3

# More tolerant early, stricter late (protecting remaining rounds)
adjusted_threshold = base_threshold + (0.2 * game_progress)

IF recent_defection_rate > adjusted_threshold:
    # Significant defection detected - consider responding
    
    IF stock_health > 0.7:
        # Resource is healthy despite defection
        # Use probabilistic response to avoid pure retaliation spiral
        defect_probability = (recent_defection_rate - adjusted_threshold) / (1 - adjusted_threshold)
        RETURN D with probability defect_probability, else C
    
    ELSE IF stock_health > 0.4:
        # Resource under moderate stress
        # Cooperate to protect resource, but signal concern
        RETURN C
    
    ELSE:
        # Resource stressed and others defecting
        # Match the defection rate probabilistically
        RETURN D with probability = recent_defection_rate
ELSE:
    # Defection is below threshold - cooperate
    RETURN C
```

### Pseudocode Summary

```python
def decide(round, stock, history, n, r, capacity):
    # Rule 1: Crisis protection
    if stock < capacity / (2 * n):
        return C
    
    # Rule 2: Final round
    if round == r:
        avg_defection = calculate_average_defection(history, n)
        return D if avg_defection > 0.6 else C
    
    # Rule 3: Opening cooperation
    if round <= 2:
        return C
    
    # Rule 4: Graduated response
    recent_defection_rate = get_recent_defection_rate(history, n, window=3)
    stock_health = stock / capacity
    game_progress = round / r
    threshold = 0.3 + (0.2 * game_progress)
    
    if recent_defection_rate <= threshold:
        return C
    
    if stock_health > 0.7:
        prob = (recent_defection_rate - threshold) / (1 - threshold)
        return D if random() < prob else C
    elif stock_health > 0.4:
        return C
    else:
        return D if random() < recent_defection_rate else C
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Signal cooperation, no history to judge |
| Round 2 | C | Still establishing pattern |
| Last round | Context-dependent | D if group defected heavily; C otherwise |
| Stock near zero | C | Any consumption hastens collapse |
| Stock at capacity | Follow main rules | Healthy resource allows normal play |
| All others defected last round | Probabilistic D | Proportional response, not pure punishment |
| All others cooperated | C | Reciprocate cooperation |

---

## Why This Strategy is Collectively Aligned

1. **Defaults to cooperation**: Only defects when faced with significant defection pressure
2. **Protects the commons**: Prioritizes resource health over short-term gains
3. **Forgiving**: Uses probabilistic responses rather than permanent punishment
4. **Escalates gradually**: Threshold increases over time, allowing early forgiveness
5. **Crisis-aware**: Always cooperates when resource is critically depleted
6. **Rewards cooperation**: Consistent cooperators receive consistent cooperation in return

This strategy aims to be a "good citizen" of the common pool while remaining robust against exploitation.
'''

description_COLLECTIVE_94 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared inheritance that sustains all players across rounds. The fundamental insight is that **defection is collectively self-defeating**: if everyone defects, the resource collapses to zero, yielding nothing for anyone in future rounds. My strategy aims to demonstrate and reward sustainable harvesting while protecting against exploitation.

## Strategy Name: "Sustainable Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to establish a sustainable norm
2. **Respond proportionally** to observed behavior
3. **Protect the resource** when it's critically depleted

### Detailed Decision Rules

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    
    # Track cooperation rate from history
    IF history is not empty:
        recent_window = min(3, length(history))
        recent_defection_rate = count_defections(last recent_window rounds) / (n_players * recent_window)
    ELSE:
        recent_defection_rate = 0
    
    # RULE 1: First Round - Always Cooperate
    IF round == 1:
        RETURN Cooperate
    
    # RULE 2: Critical Stock Protection
    # If stock is dangerously low, cooperate to allow recovery
    IF stock_ratio < 0.25:
        RETURN Cooperate
    
    # RULE 3: Final Round Consideration
    # On last round, match the prevailing behavior
    IF round == total_rounds:
        IF recent_defection_rate > 0.5:
            RETURN Defect
        ELSE:
            RETURN Cooperate
    
    # RULE 4: Responsive Cooperation (Main Logic)
    # Base cooperation probability on observed behavior and stock health
    
    # If the community has been mostly cooperative
    IF recent_defection_rate <= 0.25:
        RETURN Cooperate
    
    # If there's moderate defection, use probabilistic response
    IF recent_defection_rate <= 0.5:
        # Cooperate with probability inversely related to defection
        # Also factor in stock health - cooperate more if stock is healthy
        cooperation_probability = (1 - recent_defection_rate) * (0.5 + 0.5 * stock_ratio)
        IF random() < cooperation_probability:
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    # If defection is rampant (> 50%)
    # Match defection but periodically offer cooperation olive branch
    IF round % 3 == 0:  # Every third round, try to reset cooperation
        RETURN Cooperate
    ELSE:
        RETURN Defect
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm; signal good faith |
| **Final round** | Match majority behavior | No future rounds to influence; optimize given context |
| **Stock < 25% capacity** | Cooperate | Resource survival is paramount; defection here hurts everyone including self |
| **All others defected last round** | Defect (with periodic C) | Protect self, but offer escape from mutual destruction |
| **Stock at capacity, high cooperation** | Cooperate | Sustainable equilibrium achieved; maintain it |

### Why This Strategy is Collectively Aligned

1. **Demonstrates sustainability**: By defaulting to cooperation, I show that the resource can sustain everyone indefinitely when we harvest responsibly.

2. **Doesn't enable exploitation**: Responding to defection prevents a strategy from being a "sucker" that others exploit without consequence.

3. **Offers redemption**: Periodic cooperation attempts even during defection spirals give the collective a chance to recover.

4. **Prioritizes the resource**: When stock is critical, I always cooperate because a dead resource benefits no one—not even defectors.

5. **Adapts to context**: Rather than rigid rules, the strategy reads the room and adjusts, which handles diverse opponent strategies.

### Expected Behavior in Tournament

- Against other cooperative strategies: Sustains full stock, everyone earns maximum cumulative payoff
- Against pure defectors: Limits losses by responding in kind, while protecting critical resource levels
- Against mixed strategies: Finds equilibrium based on prevailing behavior
- Against exploitative strategies: Resists being a permanent target while keeping resource viable
'''

description_COLLECTIVE_95 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the group should achieve sustainable, near-optimal outcomes. The strategy balances immediate individual incentives against long-term collective welfare, while remaining robust when facing defectors.

## Strategy Overview: "Sustainable Guardian"

The strategy operates on three principles:
1. **Sustainability First**: Protect the resource stock to ensure long-term collective payoffs
2. **Conditional Cooperation**: Cooperate by default, but respond to exploitation
3. **Forgiveness with Memory**: Allow recovery from defection spirals, but track patterns

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if:
  - Stock health is critical (stock < capacity/4) AND
  - Cooperation is needed to prevent collapse
  
  OR
  
  - Recent cooperation rate among all players ≥ threshold AND
  - Not in final rounds exploitation window
  
  OR
  
  - Building/rebuilding trust phase

DEFECT if:
  - Final round (no future to protect)
  
  OR
  
  - Stock is doomed (stock < capacity/(4n)) AND recovery unlikely
  
  OR
  
  - Detected sustained exploitation by others AND
  - Retaliation is strategically warranted
```

### Detailed Decision Logic

**Step 1: Calculate Key Metrics**
- `stock_ratio = current_stock / capacity`
- `cooperation_rate = (# of C plays in last min(3, rounds_played) rounds) / (n × min(3, rounds_played))`
- `rounds_remaining = r - current_round`

**Step 2: Apply Decision Rules**

```
function decide(game_state, history):
    
    # ROUND 1: Always cooperate to signal collective intent
    if current_round == 1:
        return COOPERATE
    
    # FINAL ROUND: Defect (no future cooperation to protect)
    if rounds_remaining == 0:
        return DEFECT
    
    # CRITICAL STOCK PROTECTION
    # If stock is dangerously low, cooperate to attempt recovery
    if stock_ratio < 0.25:
        # But if stock is essentially zero, defect to salvage something
        if current_stock < capacity / (4 * n):
            return DEFECT
        return COOPERATE
    
    # ENDGAME STRATEGY (last ~20% of rounds)
    if rounds_remaining <= max(2, r / 5):
        # Gradually shift toward defection as end approaches
        # But maintain cooperation if stock is healthy and others cooperate
        if cooperation_rate >= 0.7 and stock_ratio >= 0.5:
            return COOPERATE
        return DEFECT
    
    # MAIN PHASE: Conditional Cooperation with Trigger
    
    # Calculate threshold based on group size
    # Larger groups need slightly lower thresholds (harder to achieve unanimity)
    coop_threshold = max(0.5, 0.8 - 0.05 * (n - 2))
    
    # If recent cooperation is above threshold, cooperate
    if cooperation_rate >= coop_threshold:
        return COOPERATE
    
    # GRADUATED RESPONSE TO DEFECTION
    # Count consecutive rounds with below-threshold cooperation
    defection_streak = count_consecutive_low_coop_rounds(history, coop_threshold)
    
    # Allow 1-2 rounds of forgiveness before retaliating
    if defection_streak <= 1:
        return COOPERATE  # Forgiveness / noise tolerance
    
    # After sustained defection, retaliate
    return DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | Cooperate | Signal cooperative intent; establish baseline |
| **Final round** | Defect | No future rounds to protect; standard game theory |
| **Stock near zero** | Defect if stock < capacity/(4n), else Cooperate | Salvage vs. recovery attempt |
| **All others defected last round** | Cooperate once, then match | Single forgiveness for noise/mistakes |
| **Stock at capacity** | Follow cooperation rules | Don't be lulled into complacency |
| **Penultimate round** | Cooperate if cooperation_rate ≥ 0.7 | Reward sustained cooperation |

---

## Why This Strategy is Collectively Optimal

**If all players use this strategy:**
- Everyone cooperates rounds 1 through r-1
- Stock remains at capacity (full regeneration when all cooperate)
- Each player earns `capacity/(2n)` per round for r-1 rounds
- Final round: all defect, each earns `capacity/n`
- **Total per player: `(r-1) × capacity/(2n) + capacity/n`**

This is near-optimal because:
- Sustained cooperation maximizes the renewable stock
- Only the final round "defection" is unavoidable (no future to incentivize cooperation)

**Against mixed opponents:**
- The strategy protects itself via conditional defection
- Forgiveness prevents death spirals from noise
- Critical stock protection maintains some resource for everyone

---

## Robustness Features

1. **Noise Tolerance**: One-round forgiveness prevents overreaction to mistakes
2. **Gradual Endgame**: Smooth transition prevents abrupt strategy shifts
3. **Stock Awareness**: Adapts behavior to resource state, not just opponent actions
4. **Scalable Thresholds**: Adjusts cooperation expectations for different group sizes
5. **Recovery Mode**: Prioritizes stock regeneration when critically depleted
'''

description_COLLECTIVE_96 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy prioritizes **sustainable collective welfare** over short-term individual gains. The key insight is that universal cooperation maintains the resource at capacity indefinitely, yielding consistent returns, while defection creates a tragedy of the commons that destroys future value for everyone.

## Strategy Overview: "Generous Tit-for-Tat with Resource Protection"

This strategy combines:
1. **Cooperative default** - Start cooperatively to signal good intentions
2. **Proportional response** - Mirror the cooperation level of the group
3. **Resource protection** - Become more cooperative when stock is critically low
4. **Forgiveness mechanism** - Allow recovery from mutual defection spirals
5. **End-game adjustment** - Maintain cooperation even in final rounds

---

## Decision Rules

### Primary Decision Function

```
COOPERATE if any of the following conditions are met:
1. First round (establish cooperative norm)
2. Stock is critically low (< capacity/4) - protect the commons
3. Previous round had majority cooperation (≥ 50% cooperated)
4. Forgiveness trigger activates (every 3rd round after defection spiral)
5. Rounds remaining > 2 AND stock health is good

DEFECT if:
1. Previous round had supermajority defection (> 75% defected) AND
2. Stock is not critically low AND
3. Not a forgiveness round
```

### Detailed Pseudocode

```python
def decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    
    # CONDITION 1: First round - always cooperate
    if current_round == 1:
        return COOPERATE
    
    # CONDITION 2: Resource protection - cooperate when stock is critical
    stock_ratio = stock / capacity
    if stock_ratio < 0.25:
        return COOPERATE  # Emergency conservation mode
    
    # Analyze previous round
    last_round = history[-1]
    cooperators_last = count_cooperators(last_round)
    cooperation_rate = cooperators_last / n
    
    # CONDITION 3: Respond to group behavior
    if cooperation_rate >= 0.5:
        return COOPERATE  # Majority cooperated, maintain cooperation
    
    # CONDITION 4: Forgiveness mechanism
    rounds_since_majority_coop = count_rounds_since_cooperation_majority(history)
    if rounds_since_majority_coop > 0 and rounds_since_majority_coop % 3 == 0:
        return COOPERATE  # Periodic olive branch
    
    # CONDITION 5: End-game consideration
    rounds_remaining = r - current_round
    if rounds_remaining <= 2 and stock_ratio > 0.5:
        return COOPERATE  # Don't trigger end-game defection cascade
    
    # CONDITION 6: Stock is healthy but group defected heavily
    if cooperation_rate < 0.25:
        return DEFECT  # Protect self when cooperation has collapsed
    
    # Default: Lean toward cooperation in ambiguous situations
    if stock_ratio > 0.6:
        return COOPERATE
    else:
        # Probabilistic cooperation based on stock health
        return COOPERATE if stock_ratio > 0.4 else DEFECT
```

---

## Edge Case Handling

### First Round
**Action: COOPERATE**
- Establishes cooperative intent
- No information to act on yet
- Cooperation is the collectively optimal starting point

### Last Round
**Action: Usually COOPERATE**
- Defect only if stock is above 75% capacity AND previous cooperation rate was below 25%
- Rationale: End-game defection is expected in standard game theory, but collective strategies should resist this temptation. If everyone defects in the last round expecting others to defect, we create a self-fulfilling prophecy.

### Near-Depleted Stock (< 25% capacity)
**Action: Always COOPERATE**
- Resource survival is paramount
- Even if others defect, cooperation gives the resource a chance to recover
- Defecting on a depleted resource yields minimal absolute payoff anyway

### After Universal Defection
**Action: COOPERATE on every 3rd round, otherwise match majority**
- Provides periodic opportunities to restart cooperation
- Doesn't get permanently trapped in defection equilibrium

---

## Collective Alignment Rationale

This strategy embodies collective thinking because:

1. **Long-term orientation**: Values sustained returns over immediate gains
2. **Forgiveness**: Allows escape from destructive equilibria
3. **Resource stewardship**: Prioritizes commons health when critical
4. **Conditional reciprocity**: Rewards cooperation, doesn't enable exploitation
5. **End-game integrity**: Resists defection cascade that harms everyone

The strategy is **robust** because it:
- Cooperates with cooperators (mutual benefit)
- Protects itself against persistent defectors
- Recovers from temporary breakdowns
- Preserves the resource even when others defect
'''

description_COLLECTIVE_97 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that in a common pool resource game, **collective restraint is the only path to sustained prosperity**. The resource regenerates optimally when stock remains near capacity/2, and collapses when over-exploited. My strategy aims to:

1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but not vindictively
4. Forgive and return to cooperation when others do

## Strategy: "Sustainable Guardian"

### Decision Framework

```
COOPERATE if ANY of the following conditions are met:
1. It's early in the game (exploration phase)
2. The resource is critically low (emergency conservation)
3. Recent history shows sufficient cooperation
4. We're in a recovery period after punishment

DEFECT if ALL of the following are true:
1. We're past the exploration phase
2. Resource is not critically endangered
3. Recent defection rate exceeds tolerance threshold
4. We're not in a forgiveness/recovery window
```

### Detailed Rules

#### Phase 1: Opening (Rounds 1-2)
**Action: Always COOPERATE**

Rationale: Establish cooperative intent. Give others a chance to demonstrate their strategy. Two rounds provides enough signal without excessive risk.

#### Phase 2: Main Game (Rounds 3 to r-1)

**Calculate these metrics each round:**
- `defection_rate` = (number of D plays in last min(3, rounds_played) rounds) / (n × min(3, rounds_played))
- `stock_ratio` = current_stock / capacity
- `critical_threshold` = 0.25 (resource in danger zone)
- `cooperation_threshold` = 0.3 (tolerate up to 30% defection)

**Decision Logic:**

```
IF stock_ratio < critical_threshold:
    COOPERATE  # Emergency conservation - resource collapse imminent
    
ELIF defection_rate ≤ cooperation_threshold:
    COOPERATE  # Sufficient cooperation from others
    
ELIF defection_rate > cooperation_threshold:
    # Graduated response based on severity
    IF defection_rate > 0.6:
        DEFECT  # Heavy defection - protect self
    ELSE:
        # Probabilistic punishment: defect with probability = defection_rate
        DEFECT with probability (defection_rate - cooperation_threshold) / 0.7
        COOPERATE otherwise
```

**Forgiveness Mechanism:**
- After any round where I defected, if the subsequent round shows ≤20% defection rate, immediately return to COOPERATE
- This allows rapid recovery from punishment cycles

#### Phase 3: Endgame (Final Round)

**Decision Logic:**
```
IF stock_ratio < 0.15:
    COOPERATE  # Resource nearly dead anyway, maintain integrity
    
ELIF historical_cooperation_rate > 0.7 (across all rounds):
    COOPERATE  # Honor the cooperative relationship
    
ELSE:
    DEFECT  # No future to protect, rational self-interest
```

### Edge Cases

1. **n = 2 (two players):** 
   - Use stricter thresholds (cooperation_threshold = 0.2)
   - More responsive to single defections since each action is 50% of behavior

2. **Very short games (r ≤ 3):**
   - Skip exploration phase after round 1
   - Cooperate round 1, then respond to what we observed

3. **Stock = 0:**
   - COOPERATE (nothing to gain from defecting on zero stock)

4. **All previous rounds saw full cooperation:**
   - COOPERATE (don't be the first to break a working system)

5. **I'm the only one who cooperated last round:**
   - DEFECT next round (clear signal others aren't cooperating)

### Why This Strategy Works Collectively

1. **Clear signaling:** Opening cooperation establishes intent
2. **Resource protection:** Critical threshold ensures we never contribute to collapse
3. **Proportional response:** Graduated punishment avoids destructive spirals
4. **Quick forgiveness:** Enables recovery from mutual defection
5. **Endgame integrity:** Maintains cooperation if relationship was good

The strategy optimizes for **total group payoff over all rounds** while protecting against exploitation. A population of Sustainable Guardians achieves near-optimal sustained harvesting, while mixed populations see Guardians cooperate with cooperators and proportionally punish defectors.
'''

description_COLLECTIVE_98 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that enables collective prosperity. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock fully regenerates each round, yielding perpetual returns. Any defection degrades this commons, ultimately harming everyone including the defectors.

The strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Create incentives for others to cooperate through conditional reciprocity
4. Prioritize collective long-term payoffs over individual short-term gains

---

## Decision Rules

### Primary Decision Framework

```
COOPERATE if ANY of these conditions hold:
  1. First round (establish cooperative norm)
  2. Stock is critically low (emergency conservation)
  3. Cooperation rate in previous round was high (reward collective good behavior)
  4. Sufficient rounds remain AND stock is healthy (invest in future)

DEFECT only if ALL of these conditions hold:
  1. Not the first round
  2. Stock is above critical threshold
  3. Recent cooperation rate has been persistently low
  4. We are in the final rounds with little recovery possible
```

### Detailed Rules

**Rule 1: Cooperative Opening**
- In round 1, always play **C**
- Rationale: Establish cooperative intent, give others the opportunity to coordinate

**Rule 2: Stock Emergency Protocol**
- If `stock < capacity / n`, always play **C**
- Rationale: When resources are critically depleted, defection accelerates collapse. Conservation becomes paramount regardless of others' behavior.

**Rule 3: Reciprocal Cooperation**
- Track the cooperation rate from the previous round: `prev_coop_rate = (players who played C) / n`
- If `prev_coop_rate >= 0.5`, play **C**
- Rationale: Reward emerging cooperation, maintain cooperative equilibria when they form

**Rule 4: Forgiveness with Memory**
- Track rolling cooperation rate over last `min(3, rounds_played)` rounds
- If `rolling_coop_rate >= 0.4`, play **C**
- Rationale: Allow recovery from temporary defection spikes, don't punish isolated deviations too harshly

**Rule 5: Future-Oriented Conservation**
- Let `rounds_remaining = r - current_round`
- Let `stock_ratio = stock / capacity`
- If `rounds_remaining >= 3` AND `stock_ratio >= 0.5`, play **C**
- Rationale: With sufficient time and resources, cooperation enables compounding returns

**Rule 6: Endgame Protocol**
- In the final round (round r):
  - If `rolling_coop_rate >= 0.6`, play **C** (honor the cooperative relationship)
  - Otherwise, play **D** (no future to protect from pure defectors)
- In second-to-last round:
  - Apply normal rules (don't trigger early defection cascade)

**Rule 7: Default to Cooperation**
- If none of the above rules clearly indicate defection, play **C**
- Rationale: Cooperation is the collectively optimal default

---

## Pseudocode Implementation

```python
def decide(game_params, state, history):
    n = game_params.num_players
    r = game_params.num_rounds
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    
    # Rule 1: Cooperative Opening
    if current_round == 1:
        return COOPERATE
    
    # Rule 2: Stock Emergency Protocol
    critical_threshold = capacity / n
    if stock < critical_threshold:
        return COOPERATE
    
    # Calculate cooperation metrics from history
    prev_round = history[-1]
    prev_coop_rate = count_cooperators(prev_round) / n
    
    lookback = min(3, len(history))
    recent_rounds = history[-lookback:]
    rolling_coop_rate = sum(count_cooperators(r) for r in recent_rounds) / (n * lookback)
    
    # Rule 3: Reciprocal Cooperation
    if prev_coop_rate >= 0.5:
        return COOPERATE
    
    # Rule 4: Forgiveness with Memory
    if rolling_coop_rate >= 0.4:
        return COOPERATE
    
    # Rule 5: Future-Oriented Conservation
    rounds_remaining = r - current_round
    stock_ratio = stock / capacity
    if rounds_remaining >= 3 and stock_ratio >= 0.5:
        return COOPERATE
    
    # Rule 6: Endgame Protocol
    if current_round == r:  # Final round
        if rolling_coop_rate >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # Rule 7: Default
    # Only defect if cooperation has persistently failed AND 
    # we're in late game with degraded stock
    if rolling_coop_rate < 0.3 and rounds_remaining <= 2 and stock_ratio < 0.7:
        return DEFECT
    
    return COOPERATE
```

---

## Edge Case Handling

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | C | Establish cooperative norm |
| Final round, good history | C | Honor cooperative relationships |
| Final round, poor history | D | No future to protect |
| Near-zero stock | C | Emergency conservation |
| All others defected last round | C (if stock healthy) | Attempt to rebuild cooperation |
| Mixed behavior, declining stock | C | Prioritize resource recovery |
| Persistent mass defection (3+ rounds) in endgame | D | Protect against exploitation |

---

## Why This Strategy is Collectively Optimal

1. **Maximizes sustainable yield**: Universal cooperation maintains stock at capacity, generating `capacity/2` in total payoffs per round indefinitely.

2. **Robust to noise**: The forgiveness mechanism and rolling averages prevent overreaction to isolated defections.

3. **Creates positive incentives**: By cooperating when others cooperate, it rewards good behavior and makes cooperation attractive.

4. **Protects the commons**: The emergency protocol ensures the resource never collapses entirely when this strategy is present.

5. **Recognizes collective identity**: Multiple instances of this strategy will naturally coordinate on full cooperation, achieving the social optimum.
'''

description_COLLECTIVE_99 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we assume all players using this strategy share the same decision rules, and we optimize for collective sustainability while protecting against exploitation. The key insight is that universal cooperation maintains the resource indefinitely, while defection creates a tragedy of the commons.

## Strategy Overview: "Sustainable Threshold Guardian"

The strategy operates on three principles:
1. **Sustain the resource** - Cooperate when the stock is healthy to ensure long-term yields
2. **Protect against collapse** - Become more conservative as stock depletes
3. **Respond to defection proportionally** - But always prioritize resource survival over punishment

---

## Decision Rules

### Primary Decision Function

```
COOPERATE if:
    (stock_health ≥ critical_threshold) AND 
    (defection_rate < tolerance_threshold) AND
    (NOT final_round)

DEFECT otherwise
```

### Key Thresholds (as fractions of capacity)

- **Critical Stock Threshold**: `0.5 × capacity` — Below this, resource regeneration becomes inefficient
- **Emergency Threshold**: `0.25 × capacity` — Resource is in danger of collapse
- **Defection Tolerance**: Starts at 25%, decreases as rounds progress

---

## Detailed Decision Rules

### Round 1 (First Round)
**Action: COOPERATE**

Rationale: With no history, we signal cooperative intent. If all players cooperate, stock remains at capacity, maximizing future potential.

### Rounds 2 through (r-1) (Middle Rounds)

Calculate the following metrics:

```
stock_health = current_stock / capacity
recent_defection_rate = (defections in last 3 rounds) / (n × 3)
cumulative_defection_rate = (total defections) / (n × rounds_played)
rounds_remaining = r - current_round
```

**Decision Logic:**

```
IF stock < emergency_threshold (0.25 × capacity):
    # Resource crisis - cooperate to allow recovery
    → COOPERATE
    
ELIF stock < critical_threshold (0.5 × capacity):
    # Resource stressed - cooperate unless heavy defection
    IF recent_defection_rate > 0.5:
        → DEFECT (resource doomed anyway)
    ELSE:
        → COOPERATE
        
ELIF recent_defection_rate > adaptive_tolerance:
    # Healthy stock but facing defectors
    # Respond with measured defection to discourage exploitation
    → DEFECT
    
ELSE:
    # Healthy stock, cooperative environment
    → COOPERATE
```

**Adaptive Tolerance Calculation:**
```
base_tolerance = 0.25
time_factor = rounds_remaining / r  # More tolerant early, stricter late
adaptive_tolerance = base_tolerance × (0.5 + time_factor)
```

### Round r (Final Round)

```
IF stock > critical_threshold AND cumulative_defection_rate < 0.3:
    # Reward sustained cooperation - maintain cooperative equilibrium
    → COOPERATE
ELSE:
    # No future to protect
    → DEFECT
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | COOPERATE | No payoff either way; cooperating signals intent if stock somehow recovers |
| Stock near capacity, high defection | DEFECT | Others are exploiting; take fair share |
| Stock low, low defection | COOPERATE | Collective recovery is possible |
| Single round remaining, healthy stock | See final round rule | Balance collective outcome vs. exploitation risk |
| n = 2 (two players) | Standard rules apply | Defection is more detectable; tolerance slightly lower |

---

## Pseudocode Implementation

```python
def decide(game_params, state, history):
    n, r, capacity = game_params
    current_stock = state['stock']
    current_round = len(history) + 1
    
    # Thresholds
    CRITICAL = 0.5 * capacity
    EMERGENCY = 0.25 * capacity
    
    # First round: cooperate
    if current_round == 1:
        return COOPERATE
    
    # Calculate defection metrics
    recent_window = min(3, len(history))
    recent_defections = count_defections(history[-recent_window:])
    recent_rate = recent_defections / (n * recent_window)
    
    total_defections = count_defections(history)
    cumulative_rate = total_defections / (n * len(history))
    
    # Adaptive tolerance
    rounds_remaining = r - current_round
    time_factor = rounds_remaining / r
    tolerance = 0.25 * (0.5 + time_factor)
    
    # Final round logic
    if current_round == r:
        if current_stock > CRITICAL and cumulative_rate < 0.3:
            return COOPERATE
        return DEFECT
    
    # Stock-based decisions
    if current_stock < EMERGENCY:
        return COOPERATE  # Crisis recovery
    
    if current_stock < CRITICAL:
        if recent_rate > 0.5:
            return DEFECT  # Resource likely doomed
        return COOPERATE  # Try to recover
    
    # Healthy stock - respond to behavior
    if recent_rate > tolerance:
        return DEFECT
    
    return COOPERATE
```

---

## Why This Strategy Works Collectively

1. **Self-sustaining equilibrium**: If all players use this strategy, everyone cooperates, stock stays at capacity, and each player earns `capacity/(2n)` per round — the maximum sustainable yield.

2. **Robust to partial defection**: The strategy tolerates some defection without collapsing into mutual defection, allowing recovery.

3. **Resource-first priority**: By prioritizing stock health over punishment, we avoid scenarios where retaliatory defection destroys the resource.

4. **Gradual response**: The adaptive tolerance prevents overreaction to noise while becoming appropriately strict as the game progresses.
'''

description_COLLECTIVE_100 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared life-support system. The fundamental insight is that **sustainable harvesting (all cooperate) is the only path to maximizing long-term collective returns**. When everyone cooperates, the stock regenerates fully each round, providing stable returns indefinitely. Defection offers short-term gains but destroys the resource base for everyone, including the defector.

Our strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally to deter exploitation
4. Forgive and restore cooperation when possible

## Decision Rules

### Primary Decision Framework

```
function decide(round, stock, capacity, n, r, history):
    
    # Calculate key metrics
    rounds_remaining = r - round
    stock_ratio = stock / capacity
    defection_rate = calculate_recent_defection_rate(history, window=3)
    
    # RULE 1: First Round - Cooperate to signal intent
    if round == 1:
        return COOPERATE
    
    # RULE 2: Resource Crisis Protection
    if stock_ratio < 0.25:
        return COOPERATE  # Emergency conservation mode
    
    # RULE 3: Last Round Consideration
    if rounds_remaining == 0:
        # If cooperation has been sustained, maintain it
        if defection_rate < 0.2:
            return COOPERATE
        # Otherwise, defect (no future to protect)
        else:
            return DEFECT
    
    # RULE 4: Responsive Reciprocity (main logic)
    if defection_rate == 0:
        # Full cooperation observed - maintain it
        return COOPERATE
    
    elif defection_rate < 0.3:
        # Minor defection - cooperate but watch closely
        # This allows for noise/errors without spiraling
        return COOPERATE
    
    elif defection_rate < 0.6:
        # Moderate defection - probabilistic response
        # Defect with probability proportional to observed defection
        if random() < defection_rate:
            return DEFECT
        else:
            return COOPERATE
    
    else:
        # Severe defection - protect self but leave door open
        # Cooperate occasionally to test for recovery
        if round % 3 == 0:
            return COOPERATE  # Periodic olive branch
        else:
            return DEFECT
```

### Helper Function: Defection Rate Calculation

```
function calculate_recent_defection_rate(history, window):
    if history is empty:
        return 0
    
    recent_rounds = last 'window' rounds from history
    total_actions = count all opponent actions in recent_rounds
    defections = count DEFECT actions in recent_rounds
    
    return defections / total_actions
```

## Detailed Rule Explanations

### Rule 1: Cooperative Opening
Always cooperate in round 1. This:
- Signals willingness to sustain the resource
- Establishes a cooperative baseline
- Loses minimal ground even if others defect (stock is at capacity)

### Rule 2: Crisis Protection
When stock falls below 25% of capacity, **always cooperate** regardless of others' behavior. Rationale:
- At low stock, even mutual cooperation barely sustains the resource
- Defecting accelerates collapse, hurting everyone including yourself
- This creates a "safe zone" where the resource can recover

### Rule 3: Endgame Handling
In the final round:
- If cooperation has been the norm (>80% cooperation), maintain it to reward the collective
- If defection has been prevalent, defect (no future rounds to protect)

### Rule 4: Graduated Reciprocity
The main decision engine uses **proportional response**:
- **0% defection**: Pure cooperation - the ideal sustainable state
- **<30% defection**: Tolerate minor deviations (could be errors or single bad actors)
- **30-60% defection**: Mirror the environment probabilistically
- **>60% defection**: Primarily defect, but periodically cooperate to test for regime change

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative norm |
| Stock = 0 | Cooperate | Nothing to gain from defecting on zero stock |
| Stock = capacity, all cooperated last round | Cooperate | Maintain optimal equilibrium |
| Single defector in otherwise cooperative group | Cooperate | Don't punish the group for one bad actor |
| Last round after sustained cooperation | Cooperate | Honor the collective achievement |
| Last round after widespread defection | Defect | No future to protect |

## Why This Strategy Works Collectively

1. **Clear signaling**: Opening cooperation and crisis-mode cooperation communicate intent
2. **Forgiveness**: The 30% tolerance threshold prevents death spirals from noise
3. **Proportionality**: Response scales with the problem, avoiding overreaction
4. **Recovery paths**: Periodic cooperation tests allow return to sustainable harvesting
5. **Resource-aware**: Prioritizes stock survival over individual punishment

The strategy succeeds when played by all because it naturally converges to full cooperation, yielding maximum sustainable returns for everyone across all rounds.
'''

description_COLLECTIVE_101 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The strategy prioritizes long-term resource preservation while remaining adaptive to defectors who might deplete the commons.

## Strategy Overview: "Sustainable Guardian"

The strategy operates on three principles:
1. **Default to cooperation** to maintain the resource at sustainable levels
2. **Protect the commons** by conditional cooperation based on resource health
3. **Respond proportionally** to observed defection patterns

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, evaluate in order:

1. RESOURCE CRITICALITY CHECK
   If stock < capacity * 0.3:
       → COOPERATE (emergency conservation mode)
   
2. LAST ROUND CHECK
   If current_round == r:
       → DEFECT (no future to protect)

3. HISTORY-BASED RESPONSE
   Calculate defection_rate = (total defections observed) / (n × rounds_played)
   
   If defection_rate > 0.6:
       → DEFECT (commons is being exploited, protect self)
   
   If defection_rate > 0.3:
       → Use PROBABILISTIC COOPERATION:
         Cooperate with probability = 1 - defection_rate
   
   Otherwise:
       → COOPERATE (healthy cooperation environment)

4. STOCK TRAJECTORY CHECK
   If stock is declining for 2+ consecutive rounds AND stock < capacity * 0.6:
       → COOPERATE (attempt to stabilize)
```

### Round-by-Round Specifics

**Round 1:**
- Always **COOPERATE**
- Rationale: Establish cooperative norm, gather information, no history to react to

**Rounds 2 through r-1:**
- Apply the Primary Decision Framework above
- Key insight: Cooperation by all maintains stock at capacity (as shown in example)

**Final Round (r):**
- **DEFECT** unless stock is critically low (< 0.2 × capacity)
- If stock is critically low: **COOPERATE** (extracting from near-zero yields little anyway)

---

## Detailed Pseudocode

```python
def choose_action(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    
    # Calculate history metrics
    if history:
        total_actions = sum(len(round_actions) for round_actions in history)
        total_defections = sum(
            sum(1 for action in round_actions if action == 'D')
            for round_actions in history
        )
        defection_rate = total_defections / total_actions
        
        # Track stock trajectory
        stock_declining = False
        if len(history) >= 2:
            recent_stocks = [state.stock_at_round[i] for i in range(-2, 0)]
            stock_declining = all(recent_stocks[i] > recent_stocks[i+1] 
                                   for i in range(len(recent_stocks)-1))
    else:
        defection_rate = 0
        stock_declining = False
    
    # DECISION LOGIC
    
    # 1. Emergency conservation
    if stock < capacity * 0.3:
        return 'C'
    
    # 2. Final round
    if current_round == r:
        if stock < capacity * 0.2:
            return 'C'  # Not worth defecting on scraps
        return 'D'
    
    # 3. First round - establish cooperation
    if current_round == 1:
        return 'C'
    
    # 4. Respond to environment
    if defection_rate > 0.6:
        return 'D'
    
    if defection_rate > 0.3:
        # Probabilistic tit-for-tat
        cooperation_prob = 1 - defection_rate
        return 'C' if random() < cooperation_prob else 'D'
    
    # 5. Stock health check
    if stock_declining and stock < capacity * 0.6:
        return 'C'
    
    # 6. Default: cooperate
    return 'C'
```

---

## Why This Strategy Works Collectively

1. **If all players use this strategy:** Everyone cooperates (except final round), stock remains at capacity, everyone earns capacity/(2n) per round - the sustainable optimum.

2. **Against defectors:** The strategy protects itself by matching high defection rates while still attempting to preserve resources when possible.

3. **Robustness:** The probabilistic middle ground prevents lock-in to mutual defection when cooperation might still be salvageable.

4. **Resource-aware:** Emergency conservation prevents complete collapse, preserving future value for everyone.
'''

description_COLLECTIVE_102 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable cooperation benefits everyone across rounds, while defection creates a tragedy of the commons. However, we must be adaptive since we cannot assume others share this perspective.

## Strategy: "Sustainable Steward with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to signal and enable collective sustainability
2. **Protect the resource** when stock is critically low
3. **Respond proportionally** to observed behavior, allowing recovery from defection spirals

### Decision Rules

```
EACH ROUND:

1. Calculate key thresholds:
   - critical_stock = capacity / 4
   - healthy_stock = capacity / 2
   - cooperation_rate = (cooperations in last round) / n  [if history exists]

2. FIRST ROUND:
   → COOPERATE (signal collective intent, enable observation)

3. LAST ROUND:
   - If stock < critical_stock → COOPERATE (preserve for collective payoff)
   - If cooperation_rate >= 0.5 in recent rounds → COOPERATE (reward cooperation)
   - Otherwise → DEFECT (no future to protect)

4. MIDDLE ROUNDS - Apply in order:

   a) RESOURCE PROTECTION RULE:
      If stock < critical_stock → COOPERATE
      (Defecting from a depleted pool gains little; cooperation enables recovery)

   b) COLLECTIVE MOMENTUM RULE:
      If cooperation_rate >= 0.75 in last round → COOPERATE
      (Maintain successful collective behavior)

   c) GRADUATED RESPONSE RULE:
      If cooperation_rate < 0.25 → DEFECT
      (Protect self when collective cooperation has collapsed)
      
      If cooperation_rate between 0.25 and 0.75:
         - If stock >= healthy_stock → COOPERATE (resource can sustain experimentation)
         - If stock < healthy_stock → DEFECT with probability (1 - cooperation_rate)
         (Probabilistic response matches observed cooperation level)

   d) FORGIVENESS MECHANISM:
      Every 3 rounds, if stuck in mutual defection:
         → COOPERATE once (attempt to restart cooperation)
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | COOPERATE | Enable learning, signal intent |
| Round r (final) | Context-dependent (see above) | Balance end-game incentives |
| Stock near 0 | COOPERATE | Defecting gains almost nothing; cooperation enables regrowth |
| Stock at capacity | Follow cooperation_rate rules | Resource is healthy; focus on behavior patterns |
| n = 2 (small game) | Standard rules apply | Tit-for-tat dynamics emerge naturally |
| All others defected last round | DEFECT, but forgive periodically | Self-protection with escape hatch |

### Why This Strategy is Collectively Optimal

1. **Sustainability Focus**: When stock is low, cooperation allows regrowth via the logistic function. Defecting from depleted stock gains little (stock/n when stock ≈ 0) while preventing recovery.

2. **Graduated Response**: Unlike pure tit-for-tat, this responds to *aggregate* cooperation, not individual actions. This is appropriate when we can't identify or target specific players.

3. **Forgiveness Built In**: The periodic cooperation attempt and probabilistic responses prevent permanent defection spirals, which destroy collective value.

4. **Aligned Incentives**: If all players use this strategy:
   - First round: all cooperate → stock stays at capacity
   - Subsequent rounds: cooperation_rate = 1.0 → all continue cooperating
   - Equilibrium: sustainable harvesting at capacity with equal payoffs

### Expected Behavior Against Various Opponents

- **Against cooperators**: Mutual cooperation, sustainable harvest
- **Against defectors**: Graduated defection with periodic forgiveness attempts
- **Against mixed strategies**: Adaptive response matching cooperation levels
- **Against itself**: Stable cooperation equilibrium

This strategy prioritizes collective sustainability while remaining robust against exploitation, embodying the principle that **a thriving commons benefits everyone more than a depleted one benefits anyone**.
'''

description_COLLECTIVE_103 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: we assume all players using this strategy share the same goals and logic. Our primary objective is **sustainable collective welfare** - maximizing total group payoffs across all rounds while maintaining resource viability. We treat defection not as exploitation, but as a coordinated response to observed threats to the collective.

## Strategy Overview: "Sustainable Threshold Guardian"

The strategy operates on three principles:
1. **Preserve the resource** - A depleted stock helps no one
2. **Cooperate by default** - Mutual cooperation is sustainable and optimal long-term
3. **Respond proportionally to defection** - Punish resource destruction, but allow recovery

---

## Decision Rules

### Primary Decision Function

```
COOPERATE if:
    (stock_health >= CRITICAL_THRESHOLD) AND
    (recent_defection_rate <= TOLERANCE) AND
    (NOT last_round)
    
DEFECT otherwise
```

### Key Parameters (derived from game parameters)

```
CRITICAL_THRESHOLD = 0.25  # Stock below 25% of capacity triggers protection mode
TOLERANCE = 0.4            # Accept up to 40% defection rate before responding
LOOKBACK_WINDOW = min(3, r-1)  # Rounds to consider for defection rate
FORGIVENESS_ROUNDS = 2    # Rounds of cooperation before forgiving past defection
```

---

## Detailed Decision Logic

### Round 1: Unconditional Cooperation
- **Action: COOPERATE**
- Rationale: Establish cooperative norm, gather information, no history to react to
- With all collective players cooperating, stock remains at capacity

### Middle Rounds (2 to r-1):

**Step 1: Assess Stock Health**
```
stock_ratio = current_stock / capacity

if stock_ratio < CRITICAL_THRESHOLD:
    # Emergency mode - defect to secure minimum payoff before collapse
    return DEFECT
```

**Step 2: Assess Recent Cooperation Level**
```
recent_rounds = last LOOKBACK_WINDOW rounds
total_actions = n × LOOKBACK_WINDOW
defection_count = count of D actions in recent_rounds
defection_rate = defection_count / total_actions

if defection_rate > TOLERANCE:
    # Too many defectors threatening the resource
    return DEFECT
```

**Step 3: Trend Analysis**
```
if stock is declining for 2+ consecutive rounds AND defection_rate > 0.2:
    # Resource under stress, protect collective interest
    return DEFECT
```

**Step 4: Default Behavior**
```
return COOPERATE
```

### Last Round: Conditional Defection
- **Action: DEFECT** (unless stock is critically low AND sustained cooperation observed)
- Rationale: No future rounds to protect, but collective players all defecting together still share equally

---

## Edge Case Handling

### Very Short Games (r ≤ 3)
- Round 1: Cooperate
- Round 2 (if r=3): Cooperate if no defection observed
- Final Round: Defect

### Large Player Counts (n > 6)
- Increase TOLERANCE to 0.5 (harder to coordinate, more noise expected)
- Collective cooperation is even more valuable with more players

### Stock Near Zero
- If stock < capacity/(2n): DEFECT (secure what's left)
- Resource is effectively destroyed; no point protecting nothing

### Recovery Scenario
```
if stock_ratio < 0.5 AND recent_defection_rate < 0.1:
    # Stock damaged but cooperation restored - help rebuild
    return COOPERATE
```

### All Previous Rounds Had Universal Cooperation
- Continue cooperating until penultimate round
- This is the optimal sustainable equilibrium

---

## Pseudocode Summary

```python
def decide(round, total_rounds, current_stock, capacity, n, history):
    
    CRITICAL_THRESHOLD = 0.25
    TOLERANCE = 0.4
    LOOKBACK = min(3, round - 1)
    
    stock_ratio = current_stock / capacity
    
    # Last round logic
    if round == total_rounds:
        return DEFECT
    
    # First round
    if round == 1:
        return COOPERATE
    
    # Emergency: stock critically low
    if stock_ratio < CRITICAL_THRESHOLD:
        return DEFECT
    
    # Calculate recent defection rate
    recent_defections = count_defections(history, LOOKBACK)
    defection_rate = recent_defections / (n * LOOKBACK)
    
    # Respond to excessive defection
    if defection_rate > TOLERANCE:
        return DEFECT
    
    # Check for declining stock trend with moderate defection
    if stock_declining(history, 2) and defection_rate > 0.2:
        return DEFECT
    
    # Default: cooperate for collective benefit
    return COOPERATE
```

---

## Why This Strategy is Collectively Optimal

1. **Self-sustaining**: When all players use this strategy, everyone cooperates (except last round), stock remains at capacity, and all players earn capacity/(2n) per round for r-1 rounds.

2. **Robust to defectors**: Proportional response prevents exploitation while allowing recovery.

3. **Adaptive**: Responds to actual observed behavior rather than assuming opponent strategies.

4. **Resource-aware**: Prioritizes long-term sustainability over short-term gains.
'''

description_COLLECTIVE_104 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: if all players adopt this same strategy, the resource sustains and everyone benefits long-term. The strategy is designed to be self-enforcing—when played against itself, it maintains cooperation, but it protects the collective from exploitation by defectors.

## Strategy Name: **Sustainable Threshold Guardian**

### Key Insight

The game's dynamics create a critical insight: **universal cooperation is self-sustaining** (stock stays at capacity), while defection depletes the resource for everyone, including defectors. A collective strategy should:
1. Default to cooperation to maintain sustainability
2. Punish observed defection to discourage exploitation
3. Forgive to allow recovery and re-coordination
4. Protect the resource when critically depleted

---

## Decision Rules

### Primary Decision Framework

```
FUNCTION decide_action(game_params, current_stock, history):
    
    n = number of players
    r = total rounds
    t = current round (1-indexed)
    capacity = maximum stock
    
    # Calculate key thresholds
    critical_threshold = capacity * 0.25
    recovery_threshold = capacity * 0.5
    
    # RULE 1: Last Round Consideration
    IF t == r:
        # On final round, if stock is healthy and no recent defection, cooperate
        # This signals commitment to collective outcome even at the end
        IF current_stock >= recovery_threshold AND recent_cooperation_rate(history, 2) >= 0.7:
            RETURN Cooperate
        ELSE:
            RETURN Defect  # Resource already compromised, no future to protect
    
    # RULE 2: Resource Protection Mode
    IF current_stock < critical_threshold:
        # Resource is critically low - cooperate to allow any possible recovery
        # Defecting now yields little and guarantees collapse
        RETURN Cooperate
    
    # RULE 3: First Round - Establish Cooperation
    IF t == 1:
        RETURN Cooperate
    
    # RULE 4: Reactive Punishment with Forgiveness
    defection_rate = calculate_defection_rate(history, last_round)
    
    IF defection_rate == 0:
        # Everyone cooperated last round - continue cooperation
        RETURN Cooperate
    
    ELIF defection_rate <= 0.5:
        # Minority defected - punish probabilistically
        # Probability of defecting = defection_rate observed
        # This creates proportional response
        IF random() < defection_rate:
            RETURN Defect
        ELSE:
            RETURN Cooperate
    
    ELSE:
        # Majority defected - join defection but watch for recovery
        IF stock_is_recovering(history) AND defection_rate < previous_defection_rate:
            # Signs of returning cooperation - extend olive branch
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    # RULE 5: Forgiveness Mechanism
    IF consecutive_rounds_of_majority_cooperation(history) >= 2:
        # Community has shown sustained cooperation - forgive and cooperate
        RETURN Cooperate
```

---

## Detailed Rule Explanations

### Rule 1: Last Round Handling
- If the resource is healthy and cooperation has been maintained, **cooperate even in the last round**
- This is the collective choice: if all copies of this strategy cooperate, everyone gets `capacity/(2n)` rather than triggering a defection spiral
- Only defect if the resource is already compromised (nothing left to protect)

### Rule 2: Resource Protection Mode
- When stock falls below 25% of capacity, **always cooperate**
- At low stock, defection yields diminishing returns while guaranteeing collapse
- This gives the resource a chance to recover via the growth function

### Rule 3: First Round Cooperation
- **Always cooperate in round 1** to signal cooperative intent
- Establishes baseline for detecting defectors

### Rule 4: Proportional Response
- **Mirror the defection rate probabilistically**
- If 1 out of 4 players defected (25%), defect with 25% probability
- This creates measured punishment without triggering full collapse
- Allows recovery if defection was accidental or exploratory

### Rule 5: Forgiveness
- After **2 consecutive rounds** where majority cooperated, return to full cooperation
- Allows recovery from punishment cycles
- Recognizes that sustained cooperation signals collective intent

---

## Helper Functions

```
FUNCTION calculate_defection_rate(history, round):
    actions = get_all_actions(history, round)
    RETURN count(Defect in actions) / n

FUNCTION recent_cooperation_rate(history, num_rounds):
    total_actions = 0
    cooperations = 0
    FOR each of last num_rounds:
        actions = get_all_actions(history, round)
        cooperations += count(Cooperate in actions)
        total_actions += n
    RETURN cooperations / total_actions

FUNCTION stock_is_recovering(history):
    IF length(history) < 2:
        RETURN False
    RETURN stock(t-1) > stock(t-2)
```

---

## Why This Strategy is Collectively Optimal

1. **Self-Enforcing Equilibrium**: When all players use this strategy, everyone cooperates every round, stock stays at capacity, and each player earns `capacity/(2n) × r` total.

2. **Robust to Exploitation**: Defectors face proportional retaliation, making sustained defection unprofitable.

3. **Forgiveness Enables Recovery**: Unlike permanent punishment, this allows return to mutual cooperation.

4. **Resource-Aware**: Protects the commons even when facing defectors, recognizing that the resource itself is a collective asset.

5. **Graceful Degradation**: When facing hostile environments, minimizes damage rather than accelerating collapse.
'''

description_COLLECTIVE_105 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a collective of players who share the same algorithm. Our goal is to maximize the **total payoff across all rounds** by preserving the resource stock while remaining robust against defectors. The key insight is that universal cooperation maintains the stock at capacity indefinitely, yielding sustainable returns, while defection depletes the resource and destroys future value.

## Strategy: Adaptive Threshold Guardian (ATG)

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to maintain sustainable harvesting
2. **Protect the resource** when stock drops below critical thresholds
3. **Retaliate proportionally** against detected defection, but allow recovery

---

### Decision Rules

```
FUNCTION decide_action(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key thresholds
    sustainable_threshold = capacity * 0.5
    critical_threshold = capacity * 0.25
    recovery_threshold = capacity * 0.75
    
    # RULE 1: Last Round - Defect (no future to protect)
    IF round == total_rounds:
        RETURN DEFECT
    
    # RULE 2: Critical Stock Protection
    # If stock is critically low, cooperate to allow recovery
    IF current_stock < critical_threshold:
        RETURN COOPERATE
    
    # RULE 3: First Round - Cooperate (establish norm)
    IF round == 1:
        RETURN COOPERATE
    
    # RULE 4: Detect Defection from Previous Round
    defection_detected = detect_defection(history, n_players, capacity)
    
    # RULE 5: Forgiveness with Stock Recovery
    # If stock has recovered above threshold, forgive past defections
    IF current_stock >= recovery_threshold:
        RETURN COOPERATE
    
    # RULE 6: Proportional Response
    # If defection detected and stock is stressed, retaliate with probability
    IF defection_detected:
        defection_severity = estimate_defection_rate(history, n_players)
        rounds_remaining = total_rounds - round
        
        # More forgiving early, stricter late (but before final round)
        IF rounds_remaining > total_rounds * 0.3:
            # Early/mid game: Tit-for-tat style, but probabilistic
            IF defection_severity > 0.5:  # Majority defected
                RETURN DEFECT
            ELSE:
                RETURN COOPERATE
        ELSE:
            # Late game (but not last round): Match defection rate
            IF random() < defection_severity:
                RETURN DEFECT
            ELSE:
                RETURN COOPERATE
    
    # RULE 7: Default - Cooperate
    RETURN COOPERATE
```

---

### Defection Detection

```
FUNCTION detect_defection(history, n_players, capacity):
    IF history is empty:
        RETURN FALSE
    
    last_round = history[-1]
    previous_stock = last_round.starting_stock
    current_stock_before_growth = last_round.stock_after_consumption
    
    # Calculate expected consumption if all cooperated
    expected_consumption_all_C = previous_stock / 2
    actual_consumption = previous_stock - current_stock_before_growth
    
    # If actual consumption significantly exceeds cooperative expectation
    tolerance = previous_stock / (4 * n_players)  # Small margin for floating point
    
    RETURN actual_consumption > (expected_consumption_all_C + tolerance)

FUNCTION estimate_defection_rate(history, n_players):
    # Estimate what fraction of players defected last round
    last_round = history[-1]
    S = last_round.starting_stock
    actual_consumption = S - last_round.stock_after_consumption
    
    # If all C: consumption = S/2, if all D: consumption = S
    # Linear interpolation to estimate defection fraction
    min_consumption = S / 2  # All cooperate
    max_consumption = S      # All defect
    
    IF max_consumption == min_consumption:
        RETURN 0
    
    defection_rate = (actual_consumption - min_consumption) / (max_consumption - min_consumption)
    RETURN clamp(defection_rate, 0, 1)
```

---

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative norm, signal intent |
| **Last round** | Defect | No future rounds to protect; dominant strategy |
| **Stock < 25% capacity** | Cooperate | Emergency conservation to prevent collapse |
| **Stock > 75% capacity after defection** | Cooperate | Resource recovered; forgive and reset |
| **Majority defected last round** | Defect | Proportional retaliation to deter exploitation |
| **Minority defected, stock healthy** | Cooperate | Maintain cooperation, absorb minor losses |

---

### Collective Alignment

When multiple copies of this strategy play together:
- All cooperate in round 1
- All continue cooperating as long as no external defection detected
- Stock remains at capacity (full regeneration)
- All defect only in final round (mutual understanding)
- **Result**: Maximum sustainable collective payoff

Against defectors:
- Detects defection through consumption analysis
- Responds proportionally rather than permanently retaliating
- Allows recovery if resource rebounds
- Protects against collapse by enforcing cooperation when stock is critical

---

### Summary

**ATG** balances:
- **Cooperation by default** for collective benefit
- **Retaliation capability** to deter exploitation  
- **Forgiveness mechanism** to recover from mutual defection spirals
- **Resource protection** as an absolute priority when stock is endangered
- **End-game pragmatism** by defecting only when no future exists
'''

description_COLLECTIVE_106 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully, allowing maximum cumulative payoffs across all rounds. Any defection creates a tragedy of the commons spiral.

The strategy aims to:
1. Signal cooperative intent clearly
2. Maintain resource sustainability
3. Punish defection proportionally but allow recovery
4. Protect the resource from collapse in critical states

---

## Decision Rules

### Primary Decision Framework

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    sustainable_threshold = capacity * 0.5
    critical_threshold = capacity * 0.25
    rounds_remaining = total_rounds - round
    
    # RULE 1: First Round - Always Cooperate
    IF round == 1:
        RETURN Cooperate
    
    # RULE 2: Critical Stock Protection
    IF current_stock < critical_threshold:
        RETURN Cooperate  # Resource emergency - always preserve
    
    # RULE 3: Final Round Consideration
    IF round == total_rounds:
        # Cooperate if stock is healthy and others have been cooperative
        IF cooperation_rate(history) >= 0.7 AND current_stock >= sustainable_threshold:
            RETURN Cooperate
        ELSE:
            RETURN Defect  # No future to protect
    
    # RULE 4: Penultimate Rounds (last 2 rounds)
    IF rounds_remaining <= 2:
        IF recent_cooperation_rate(history, last_3_rounds) >= 0.8:
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    # RULE 5: Responsive Cooperation (Main Game)
    RETURN responsive_decision(history, current_stock, capacity)
```

### Responsive Decision Logic

```
FUNCTION responsive_decision(history, current_stock, capacity):
    
    # Calculate opponent cooperation rate over recent rounds
    recent_window = min(5, len(history))
    recent_coop_rate = cooperation_rate(history, last=recent_window)
    overall_coop_rate = cooperation_rate(history)
    
    # Weighted assessment favoring recent behavior
    weighted_coop = 0.7 * recent_coop_rate + 0.3 * overall_coop_rate
    
    # Stock health factor
    stock_ratio = current_stock / capacity
    
    # GENEROUS THRESHOLD: Cooperate if environment seems cooperative
    IF weighted_coop >= 0.6:
        RETURN Cooperate
    
    # MODERATE DEFECTION: Some defection detected
    IF weighted_coop >= 0.4:
        # Cooperate if stock is healthy (give benefit of doubt)
        IF stock_ratio >= 0.6:
            RETURN Cooperate
        ELSE:
            RETURN Defect  # Protect declining resource
    
    # HIGH DEFECTION ENVIRONMENT: Protect self but allow recovery
    IF weighted_coop >= 0.2:
        # Check for recent improvement trend
        IF improving_trend(history, window=3):
            RETURN Cooperate  # Reward positive change
        ELSE:
            RETURN Defect
    
    # HOSTILE ENVIRONMENT: Mostly defectors
    # Still cooperate occasionally to signal willingness to restart cooperation
    IF round % 4 == 0:  # Every 4th round, offer olive branch
        RETURN Cooperate
    ELSE:
        RETURN Defect
```

---

## Helper Functions

```
FUNCTION cooperation_rate(history, last=None):
    # Returns fraction of (Cooperate) actions by all OTHER players
    # If last specified, only consider last N rounds
    relevant_history = history[-last:] if last else history
    total_actions = count all other player actions in relevant_history
    cooperative_actions = count Cooperate actions
    RETURN cooperative_actions / total_actions (or 1.0 if no history)

FUNCTION improving_trend(history, window):
    # Returns True if cooperation is increasing over recent window
    IF len(history) < window:
        RETURN True  # Benefit of doubt early
    first_half = cooperation_rate(history, last=window)[:window//2]
    second_half = cooperation_rate(history, last=window)[window//2:]
    RETURN second_half > first_half
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative intent, no information to act otherwise |
| Stock < 25% capacity | Cooperate | Resource emergency - collective survival |
| Final round, cooperative history | Cooperate | Honor the cooperative relationship |
| Final round, hostile history | Defect | No future rounds to protect |
| Stock = 0 | Cooperate | Only option (defecting on 0 yields 0 anyway) |
| Single opponent defected once | Cooperate | Forgive isolated incidents |
| Sustained defection (>60%) | Mostly Defect | Protect from exploitation, but signal willingness to restart |

---

## Why This Strategy Works Collectively

1. **Clear signaling**: Starting with cooperation and maintaining it under good conditions makes cooperative intent unambiguous to like-minded players.

2. **Forgiveness**: The 60% threshold and trend detection allow recovery from accidental or exploratory defection.

3. **Resource protection**: The critical threshold rule prevents collapse even against hostile opponents.

4. **Proportional response**: Punishment scales with observed defection rather than being all-or-nothing.

5. **Endgame stability**: Conditional cooperation in final rounds rather than automatic defection preserves gains against cooperative opponents.
'''

description_COLLECTIVE_107 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players in the game adopt this same strategy, the outcome should be sustainable and mutually beneficial. At the same time, it must be **robust** against defectors and **adaptive** to the actual behavior observed in the game.

The key insight is that universal cooperation sustains the resource indefinitely (stock returns to capacity each round), while defection depletes it. A collectively-minded strategy should:
1. Default to cooperation to maintain sustainability
2. Protect the commons from collapse when defection threatens it
3. Signal willingness to return to cooperation after punishment

---

## Strategy: "Sustainable Guardian"

### Decision Rules

**Round 1:** Always **Cooperate**
- Establishes cooperative intent
- No history to react to
- Gives others the opportunity to demonstrate cooperation

**Rounds 2 through (r-1):** Conditional Cooperation with Resource Protection

```
Let:
  d_prev = number of defectors in previous round
  stock_ratio = current_stock / capacity
  critical_threshold = 0.3
  danger_threshold = 0.5

IF stock_ratio < critical_threshold:
    # Resource is critically depleted - cooperate to allow recovery
    COOPERATE
    
ELIF d_prev == 0:
    # Everyone cooperated last round - continue cooperating
    COOPERATE
    
ELIF d_prev >= n/2:
    # Majority defected - defect to avoid exploitation
    # But with probability based on stock health, try cooperation
    IF stock_ratio > danger_threshold:
        DEFECT
    ELSE:
        COOPERATE  # Prioritize resource survival
        
ELSE:
    # Minority defected - use proportional response
    # Defect with probability = d_prev / n
    # This creates gradual pressure without destroying cooperation
    IF random() < (d_prev / n):
        DEFECT
    ELSE:
        COOPERATE
```

**Final Round (round r):** Strategic Consideration

```
IF stock_ratio < critical_threshold:
    # Even in final round, if resource is critical, cooperate
    # (collectively, this prevents total collapse)
    COOPERATE
ELIF history shows consistent cooperation (d_prev == 0 for last 3+ rounds):
    # Reward sustained cooperation with continued cooperation
    COOPERATE
ELSE:
    # Otherwise, defect (standard end-game logic)
    DEFECT
```

---

## Key Design Principles

### 1. **Sustainability First**
When stock drops below 30% of capacity, always cooperate regardless of others' behavior. A depleted resource hurts everyone, and collective recovery requires coordination. If all players use this strategy, the resource will recover.

### 2. **Forgiveness Through Proportionality**
Rather than harsh tit-for-tat punishment, the strategy uses probabilistic responses proportional to defection levels. This:
- Avoids destructive punishment spirals
- Allows gradual return to cooperation
- Signals that cooperation is always welcome

### 3. **Collective Alignment**
If all n players use this strategy:
- Round 1: All cooperate → stock stays at capacity
- Subsequent rounds: No defectors observed → all continue cooperating
- Final round: History of cooperation → all cooperate
- **Result: Maximum sustainable collective payoff**

### 4. **Robustness to Defectors**
Against persistent defectors:
- Probabilistic defection prevents complete exploitation
- Resource protection mode kicks in before collapse
- Strategy doesn't "give up" on cooperation entirely

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| First round | Cooperate | Establish trust, no information yet |
| Stock = 0 | Cooperate | Only way to allow any recovery |
| Stock near capacity, all defected | Defect | Protect self when resource is abundant but trust is broken |
| Single defector | Cooperate (90% prob) | Minor transgression, maintain cooperation |
| Last round, good history | Cooperate | Reward collective good behavior |
| Last round, bad history | Defect | Standard end-game protection |
| n = 2 (two players) | Follow standard rules | Proportional response still applies |

---

## Summary Pseudocode

```python
def decide(round, total_rounds, current_stock, capacity, n, history):
    stock_ratio = current_stock / capacity
    
    if round == 1:
        return COOPERATE
    
    d_prev = count_defectors(history[-1])
    
    # Resource protection override
    if stock_ratio < 0.3:
        return COOPERATE
    
    # Final round logic
    if round == total_rounds:
        if recent_cooperation(history, rounds=3) and d_prev == 0:
            return COOPERATE
        else:
            return DEFECT
    
    # Standard conditional cooperation
    if d_prev == 0:
        return COOPERATE
    elif d_prev >= n / 2:
        return DEFECT if stock_ratio > 0.5 else COOPERATE
    else:
        return DEFECT if random() < (d_prev / n) else COOPERATE
```

This strategy balances collective welfare with self-protection, prioritizes resource sustainability, and creates stable cooperation when adopted universally.
'''

description_COLLECTIVE_108 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a population of agents sharing the same approach. Our collective goal is to maintain the resource at sustainable levels while maximizing long-term group payoffs. We use a **conditional cooperation** framework that:
1. Starts cooperatively to establish sustainable harvesting
2. Monitors collective behavior through stock levels
3. Responds proportionally to resource degradation
4. Allows for forgiveness and recovery

## Strategy: "Sustainable Harvest with Collective Punishment"

### Decision Framework

The strategy makes decisions based on three key indicators:
- **Stock health**: How close the current stock is to capacity
- **Round position**: Early, middle, or late game considerations
- **Trend**: Whether the stock is recovering or declining

### Pseudocode

```
function decide(n, r, capacity, stock, round_number, history):
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    rounds_remaining = r - round_number
    
    # LAST ROUND: Always defect (no future to protect)
    if rounds_remaining == 0:
        return DEFECT
    
    # FIRST ROUND: Cooperate to signal collective intent
    if round_number == 1:
        return COOPERATE
    
    # CRITICAL DEPLETION: Emergency cooperation to save resource
    # If stock is very low, cooperating gives us the best chance of recovery
    if stock_ratio < 0.15:
        return COOPERATE
    
    # NEAR-END GAME (last 2-3 rounds before final): Gradually shift to defection
    # as future value diminishes
    if rounds_remaining <= 2:
        if stock_ratio > 0.5:
            return DEFECT
        else:
            return COOPERATE  # Don't kill a struggling resource
    
    # MAIN GAME LOGIC: Stock-based threshold strategy
    
    # Calculate sustainable threshold
    # With all cooperators, stock stays at capacity
    # We tolerate some defection but respond to degradation
    
    # Healthy stock (>60% capacity): Cooperate - system is sustainable
    if stock_ratio >= 0.6:
        return COOPERATE
    
    # Moderate stock (30-60%): Probabilistic response based on health
    if stock_ratio >= 0.3:
        # Check if stock is recovering or declining
        if len(history) >= 2:
            previous_stock = history[-2]['stock']  # stock from 2 rounds ago
            if stock > previous_stock:
                # Stock recovering - continue cooperating
                return COOPERATE
            else:
                # Stock declining despite cooperation - defect to get value before collapse
                # But only probabilistically to allow recovery attempts
                cooperation_probability = (stock_ratio - 0.3) / 0.3  # 0 to 1 as stock goes 0.3 to 0.6
                if random() < cooperation_probability:
                    return COOPERATE
                else:
                    return DEFECT
        else:
            return COOPERATE  # Not enough history, give benefit of doubt
    
    # Low stock (15-30%): High likelihood of defection
    # Resource is being exploited - extract value while possible
    if stock_ratio >= 0.15:
        # Small chance of cooperation to test if others will cooperate
        if random() < 0.2:
            return COOPERATE
        else:
            return DEFECT
```

### Decision Rules Summary

| Condition | Action | Rationale |
|-----------|--------|-----------|
| First round | **Cooperate** | Signal collective intent, establish baseline |
| Last round | **Defect** | No future consequences |
| Stock < 15% capacity | **Cooperate** | Emergency: only cooperation can save resource |
| 2-3 rounds left, healthy stock | **Defect** | Extract value as game ends |
| 2-3 rounds left, low stock | **Cooperate** | Don't kill dying resource |
| Stock ≥ 60% capacity | **Cooperate** | System is healthy, maintain it |
| Stock 30-60%, recovering | **Cooperate** | Reward collective good behavior |
| Stock 30-60%, declining | **Mixed** | Probabilistic based on severity |
| Stock 15-30% | **Mostly Defect** | Resource being exploited, extract value |

### Edge Cases

1. **Very short games (r ≤ 3)**: The end-game logic dominates; expect more defection
2. **Very large n**: Stock depletes faster; thresholds become more critical
3. **Stock at exactly capacity**: Cooperate to maintain equilibrium
4. **Oscillating stock**: The trend detection helps avoid overreaction

### Collective Alignment

When all agents use this strategy:
- The resource stays at capacity (all cooperate when stock is healthy)
- Everyone earns `capacity/(2n)` per round consistently
- Total group payoff is maximized across all rounds except the last

This beats universal defection, which collapses the resource after round 1.
'''

description_COLLECTIVE_109 = '''
# Collective Strategy for the Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved across rounds. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - it maintains the resource at capacity while providing steady returns. Any defection creates a tragedy of the commons spiral.

The strategy aims to:
1. Signal cooperative intent clearly
2. Punish defection proportionally to protect the commons
3. Forgive and restore cooperation when possible
4. Adapt to the remaining game horizon and resource health

---

## Decision Rules

### Primary Decision Framework

```
DECIDE(round, stock, history, n, r, capacity):
    
    # Calculate key metrics
    rounds_remaining = r - round
    stock_health = stock / capacity
    defection_rate = calculate_defection_rate(history)
    recent_defection_rate = calculate_recent_defection_rate(history, window=3)
    
    # RULE 1: First Round - Unconditional Cooperation
    if round == 1:
        return COOPERATE
    
    # RULE 2: Resource Crisis Mode
    if stock_health < 0.25:
        return COOPERATE  # Emergency conservation
    
    # RULE 3: Last Round Logic
    if rounds_remaining == 0:
        # If cooperation has been strong, maintain it (reputation/collective good)
        if defection_rate < 0.2:
            return COOPERATE
        else:
            return DEFECT  # No future to protect
    
    # RULE 4: Near-End Game (last 2 rounds)
    if rounds_remaining <= 2:
        if recent_defection_rate < 0.15:
            return COOPERATE
        else:
            return DEFECT
    
    # RULE 5: Graduated Response to Defection History
    if recent_defection_rate > 0.5:
        # Majority defecting recently - protect yourself but allow recovery
        return DEFECT
    
    if recent_defection_rate > 0.3:
        # Significant defection - probabilistic punishment
        # Defect with probability proportional to defection rate
        if random() < recent_defection_rate:
            return DEFECT
        else:
            return COOPERATE
    
    # RULE 6: Forgiveness Mechanism
    if was_defecting_last_round(history) and recent_defection_rate < 0.2:
        return COOPERATE  # Return to cooperation if others reformed
    
    # RULE 7: Default - Cooperate
    return COOPERATE
```

---

## Detailed Rule Explanations

### Rule 1: First Round Cooperation
**Always cooperate in round 1.** This establishes a cooperative baseline and gives others the opportunity to demonstrate good faith. With no history, optimism serves the collective.

### Rule 2: Resource Crisis Mode
**If stock falls below 25% of capacity, always cooperate.** When the resource is critically depleted, even "winning" by defecting yields little value. Conservation becomes paramount - defecting from a depleted pool is like fighting over crumbs while the table burns.

### Rule 3: Last Round
**Conditional cooperation based on history.** Unlike naive strategies that always defect in the final round, we maintain cooperation if the game has been cooperative (defection rate < 20%). This rewards collective success and aligns with the collective mindset.

### Rule 4: Near-End Game
**Slightly more defensive in rounds r-1 and r-2.** The shadow of the future shortens, so we tighten our cooperation threshold but don't abandon it entirely.

### Rule 5: Graduated Response
**Proportional punishment for defection.** Rather than hair-trigger retaliation:
- If >50% recent defection: Defect (self-protection)
- If 30-50% recent defection: Probabilistic defection (signal displeasure while leaving door open)
- Below 30%: Maintain cooperation

### Rule 6: Forgiveness
**Return to cooperation after punishment if others reform.** This prevents permanent defection spirals and allows the collective to recover from mistakes.

### Rule 7: Default Cooperation
**When in doubt, cooperate.** The resource regenerates best under cooperation, and the collective benefits compound over rounds.

---

## Helper Functions

```
calculate_defection_rate(history):
    if history is empty: return 0
    total_actions = count all actions across all players and rounds
    total_defections = count all D actions
    return total_defections / total_actions

calculate_recent_defection_rate(history, window):
    Consider only the last 'window' rounds
    Same calculation as above but limited scope
    
was_defecting_last_round(history):
    Return True if this strategy played D in the previous round
```

---

## Why This Strategy Works Collectively

1. **Sustainable by default**: Cooperation maintains stock at capacity indefinitely
2. **Robust to defectors**: Graduated punishment protects against exploitation without overreacting
3. **Self-healing**: Forgiveness mechanisms allow recovery from defection spirals
4. **Crisis-aware**: Prioritizes conservation when the resource is threatened
5. **Horizon-adaptive**: Adjusts behavior as the game approaches its end

The strategy embodies the principle: **"Protect the commons first, then respond to threats, but always leave room for redemption."**
'''

description_COLLECTIVE_110 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt it, the resource remains sustainable and everyone benefits maximally over time. However, it must also be **robust** against defectors who might exploit cooperators.

The key insight is that the stock dynamics create a **tragedy of the commons** - individual defection is tempting but collective defection destroys the resource for everyone. Our strategy aims to:
1. Signal cooperative intent early
2. Maintain resource sustainability when others cooperate
3. Protect against exploitation without triggering destructive spirals
4. Adapt to the actual behavior we observe

## Strategy: "Sustainable Guardian"

### Decision Rules

```
FUNCTION decide_action(game_params, current_stock, history):
    
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    
    # --- PHASE 1: FIRST ROUND ---
    IF current_round == 1:
        RETURN Cooperate  # Signal cooperative intent
    
    # --- PHASE 2: LAST ROUND ---
    IF current_round == r:
        # If stock is healthy and cooperation has been high, maintain cooperation
        # (collective mindset: don't defect just because it's the end)
        cooperation_rate = calculate_overall_cooperation_rate(history)
        IF cooperation_rate >= 0.6 AND current_stock >= capacity * 0.5:
            RETURN Cooperate
        ELSE:
            RETURN Defect  # Resource already compromised
    
    # --- PHASE 3: RESOURCE CRITICAL ---
    # If stock is dangerously low, cooperate to allow recovery
    critical_threshold = capacity * 0.25
    IF current_stock < critical_threshold:
        RETURN Cooperate  # Prioritize collective survival
    
    # --- PHASE 4: ADAPTIVE RESPONSE ---
    # Look at recent behavior (last 3 rounds or all if fewer)
    lookback = min(3, len(history))
    recent_history = history[-lookback:]
    
    recent_defection_rate = calculate_defection_rate(recent_history)
    
    # Generous threshold: tolerate some defection
    IF recent_defection_rate <= 0.3:
        RETURN Cooperate
    
    # Moderate defection: probabilistic response
    IF recent_defection_rate <= 0.6:
        # Match the cooperation rate we've seen
        # This creates pressure toward cooperation without being punitive
        IF random() < (1 - recent_defection_rate):
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    # High defection environment: protect self but leave door open
    # Defect with high probability, but occasionally cooperate to test waters
    IF random() < 0.2:
        RETURN Cooperate  # Olive branch
    ELSE:
        RETURN Defect
```

### Helper Functions

```
FUNCTION calculate_defection_rate(history):
    total_actions = 0
    total_defections = 0
    FOR each round in history:
        FOR each player_action in round:
            total_actions += 1
            IF player_action == Defect:
                total_defections += 1
    RETURN total_defections / total_actions

FUNCTION calculate_overall_cooperation_rate(history):
    RETURN 1 - calculate_defection_rate(history)
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline; no information to act on otherwise |
| **Last round** | Conditional | Cooperate if resource healthy and history cooperative; defect only if already degraded |
| **Stock near zero** | Cooperate | Collective survival trumps individual gain; defecting kills the resource for everyone |
| **Stock at capacity** | Follow adaptive rules | Resource health allows normal strategic play |
| **All others defected last round** | Mostly defect, sometimes cooperate | Protect self while testing for return to cooperation |

## Why This Strategy is Collectively Optimal

1. **If all players use this strategy**: Everyone cooperates, stock stays at capacity, each player earns `capacity/(2n)` every round - the sustainable maximum.

2. **Against mixed populations**: The strategy tolerates noise and occasional defection without triggering collapse, but doesn't allow exploitation.

3. **Self-correcting**: The probabilistic matching naturally pushes toward whatever equilibrium the population supports, while the "olive branch" mechanism can restore cooperation after breakdowns.

4. **Resource-aware**: By prioritizing cooperation when stock is critical, we prevent the irreversible collapse that hurts everyone.
'''

description_COLLECTIVE_111 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared life-support system. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully each round, providing steady returns indefinitely. Any defection depletes the commons, reducing future payoffs for everyone including the defector.

The strategy aims to:
1. Signal cooperative intent clearly
2. Maintain the resource at sustainable levels
3. Respond proportionally to observed behavior
4. Protect the commons from collapse while remaining adaptive

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND, evaluate in order:

1. RESOURCE CRITICALITY CHECK
   If stock < capacity / n:
       → COOPERATE (emergency conservation mode)

2. FIRST ROUND
   → COOPERATE (establish cooperative norm)

3. FINAL ROUND
   If previous_round_cooperation_rate >= 0.5:
       → COOPERATE (reward sustained cooperation)
   Else:
       → DEFECT (no future to protect)

4. HISTORY-BASED RESPONSE
   Calculate: cooperation_rate = (total C plays by others) / (total plays by others)
   Calculate: recent_rate = cooperation rate in last min(3, rounds_played) rounds
   
   weighted_rate = 0.4 * cooperation_rate + 0.6 * recent_rate
   
   If weighted_rate >= 0.6:
       → COOPERATE
   Else if weighted_rate >= 0.3:
       → COOPERATE with probability = weighted_rate
   Else:
       → DEFECT
```

---

## Detailed Rule Explanations

### Rule 1: Emergency Conservation
When stock falls below `capacity/n`, the resource is critically depleted. At this level, even one round of heavy defection could cause collapse. **Always cooperate** to give the resource a chance to regenerate, regardless of others' behavior. This is collective survival instinct.

### Rule 2: First Round - Unconditional Cooperation
Start cooperative to:
- Signal willingness to sustain the commons
- Establish a cooperative baseline
- Give others the opportunity to reciprocate

### Rule 3: Final Round Logic
In the last round, there's no future to protect. However:
- If others have been mostly cooperative (≥50%), honor that relationship by cooperating
- If others have been exploitative, defect since there's no remaining incentive structure

### Rule 4: Adaptive Response Based on History
The weighted cooperation rate emphasizes **recent behavior** (60% weight) while still accounting for overall patterns (40% weight). This allows:
- Quick response to behavioral shifts
- Forgiveness for early defections if behavior improves
- Memory of sustained exploitation

**Threshold rationale:**
- ≥60% cooperation: Environment is cooperative enough to sustain mutual cooperation
- 30-60%: Mixed environment; probabilistic response maintains some cooperation while protecting against exploitation
- <30%: Predominantly exploitative environment; defect to avoid being a sucker

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish cooperative norm |
| Final round, good history | Cooperate | Reward cooperation, maintain integrity |
| Final round, bad history | Defect | No future incentive to cooperate |
| Stock critically low | Cooperate | Resource survival takes priority |
| Stock = 0 | Cooperate | Only way to allow any regeneration |
| Single defector among cooperators | Cooperate | One defector doesn't break the system |
| Only 2 players, one defected | Probabilistic | Give chance for recovery |

---

## Pseudocode Implementation

```python
def decide(game_params, current_stock, history):
    n, r, capacity = game_params.n, game_params.r, game_params.capacity
    current_round = len(history) + 1
    
    # Rule 1: Emergency conservation
    if current_stock < capacity / n:
        return COOPERATE
    
    # Rule 2: First round
    if current_round == 1:
        return COOPERATE
    
    # Calculate cooperation rates
    all_other_actions = flatten(history.others_actions)
    recent_actions = flatten(history.others_actions[-3:])
    
    overall_coop_rate = count(all_other_actions, C) / len(all_other_actions)
    recent_coop_rate = count(recent_actions, C) / len(recent_actions)
    weighted_rate = 0.4 * overall_coop_rate + 0.6 * recent_coop_rate
    
    # Rule 3: Final round
    if current_round == r:
        return COOPERATE if weighted_rate >= 0.5 else DEFECT
    
    # Rule 4: History-based response
    if weighted_rate >= 0.6:
        return COOPERATE
    elif weighted_rate >= 0.3:
        return COOPERATE if random() < weighted_rate else DEFECT
    else:
        return DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Sustainability-first**: Prioritizes resource survival over short-term gains
2. **Forgiveness with memory**: Allows recovery from defection while protecting against persistent exploitation
3. **Clear signaling**: Consistent cooperative start makes intentions transparent
4. **Proportional response**: Matches cooperation level to environmental conditions
5. **Robustness**: Performs reasonably against pure defectors while thriving with cooperators
'''

description_COLLECTIVE_112 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy recognizes that the common pool resource is a shared asset where collective restraint enables sustained prosperity, while unchecked exploitation leads to collapse. The strategy aims to **maintain the resource at sustainable levels** while **protecting against exploitation** and **signaling cooperative intent**.

## Strategy Name: "Sustainable Guardian"

### Key Insight

The stock dynamics reveal a critical threshold: when stock is at capacity and all cooperate, the resource regenerates fully. When all defect, the resource collapses to zero. The optimal collective outcome requires sufficient cooperation to keep the resource in a regenerative state.

### Decision Rules

**Primary Decision Framework:**

```
function decide(game_params, current_stock, history):
    n = number of players
    r = total rounds
    t = current round (1-indexed)
    capacity = maximum stock
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = r - t
    
    # 1. CRITICAL STOCK PROTECTION
    if stock_ratio < 0.25:
        return COOPERATE  # Resource critically low - must allow recovery
    
    # 2. FIRST ROUND: Establish cooperative norm
    if t == 1:
        return COOPERATE
    
    # 3. FINAL ROUND CONSIDERATION
    if rounds_remaining == 0:
        # Cooperate if resource is healthy and cooperation was prevalent
        if stock_ratio > 0.5 and cooperation_rate(history) > 0.5:
            return COOPERATE
        else:
            return DEFECT  # No future to protect
    
    # 4. ASSESS COMMUNITY BEHAVIOR
    recent_coop_rate = cooperation_rate(last_3_rounds(history))
    overall_coop_rate = cooperation_rate(history)
    
    # 5. RECIPROCITY-BASED DECISION
    if recent_coop_rate >= 0.6:
        # Community is cooperating - maintain cooperation
        return COOPERATE
    
    elif recent_coop_rate >= 0.4:
        # Mixed behavior - cooperate if stock is healthy
        if stock_ratio > 0.5:
            return COOPERATE
        else:
            return DEFECT  # Protect self when resource stressed
    
    else:
        # Community defecting heavily
        # Occasional cooperation to test for recovery
        if t % 3 == 0 and stock_ratio > 0.3:
            return COOPERATE  # Periodic olive branch
        else:
            return DEFECT  # Match defection to avoid exploitation
```

### Detailed Rule Explanations

**Rule 1 - Critical Stock Protection:**
When stock falls below 25% of capacity, always cooperate. At this level, the resource is near collapse, and further extraction accelerates total destruction. Even if others defect, preserving any remaining stock gives the best chance of eventual recovery.

**Rule 2 - First Round Cooperation:**
Begin cooperatively to signal intent and establish a cooperative equilibrium possibility. This gives the collective the best starting trajectory.

**Rule 3 - Final Round:**
In the last round, there's no future to protect. However, if the community has been cooperative and the resource is healthy, maintain cooperation as a matter of collective principle. If cooperation was low, defect since there's no reputation cost.

**Rule 4-5 - Reciprocity Assessment:**
- Track the cooperation rate across all players over recent rounds
- **High cooperation (≥60%):** Reward with continued cooperation
- **Moderate cooperation (40-60%):** Cooperate if resource can sustain it
- **Low cooperation (<40%):** Primarily defect, but periodically cooperate to test if others will reciprocate

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round | C | Establish cooperative norm |
| Last round, healthy stock, cooperative history | C | Honor collective success |
| Last round, depleted stock or defecting history | D | No future value to protect |
| Stock near zero | C | Only chance for regeneration |
| All others defected last round | D (then C every 3rd round) | Avoid exploitation, but test for change |
| Stock at capacity, all cooperating | C | Maintain optimal equilibrium |

### Why This Strategy is Collectively Optimal

1. **Sustainability Focus:** Prioritizes resource health over short-term gains
2. **Forgiveness:** Periodic cooperation tests allow recovery from defection spirals
3. **Protection:** Doesn't allow unlimited exploitation by defectors
4. **Clarity:** Simple rules make behavior predictable to other cooperators
5. **Adaptiveness:** Responds to actual community behavior rather than fixed patterns
'''

description_COLLECTIVE_113 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that sustains all players across rounds. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all cooperate, the stock regenerates fully, providing consistent returns. Any defection creates a tragedy of the commons spiral.

The strategy aims to:
1. Signal cooperative intent clearly
2. Punish defection proportionally to protect the commons
3. Forgive to allow recovery when others return to cooperation
4. Adapt consumption based on resource health

---

## Decision Rules

### Primary Decision Framework

```
EACH ROUND:
    Calculate stock_health = current_stock / capacity
    Calculate recent_cooperation_rate = cooperators in last 3 rounds / (n × 3)
    
    IF first_round:
        COOPERATE (signal intent)
    
    ELSE IF last_round:
        # Cooperate if resource is healthy and others have been cooperative
        IF stock_health > 0.5 AND recent_cooperation_rate > 0.6:
            COOPERATE
        ELSE:
            DEFECT
    
    ELSE IF stock_health < 0.25:
        # CRISIS MODE: Resource near collapse
        COOPERATE (attempt recovery)
    
    ELSE:
        # NORMAL OPERATION: Conditional cooperation with forgiveness
        Apply GRADUATED_RESPONSE()
```

### Graduated Response Mechanism

```
GRADUATED_RESPONSE():
    defection_rate = defectors_last_round / n
    consecutive_defection_rounds = count of rounds where defection_rate > 0.5
    
    IF defection_rate == 0:
        # Everyone cooperated - maintain cooperation
        COOPERATE
    
    ELSE IF defection_rate < 0.5:
        # Minority defected - stay cooperative to maintain resource
        # But with probability based on stock health
        IF stock_health > 0.7:
            COOPERATE
        ELSE:
            COOPERATE with probability = stock_health
            DEFECT with probability = 1 - stock_health
    
    ELSE IF defection_rate >= 0.5:
        # Majority defected - proportional punishment
        IF consecutive_defection_rounds >= 2:
            DEFECT (sustained punishment)
        ELSE:
            DEFECT (single-round punishment signal)
    
    # FORGIVENESS CLAUSE
    IF previous_round_was_punishment AND defection_rate_this_round < defection_rate_last_round:
        COOPERATE (reward improvement)
```

---

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | COOPERATE | Establish cooperative norm, signal intent |
| **Final round** | Context-dependent (see above) | Avoid pure defection spiral; reward sustained cooperation |
| **Stock near zero** | COOPERATE | Defecting on nothing gains nothing; cooperation allows recovery |
| **Stock at capacity** | Follow graduated response | Don't over-exploit even when abundant |
| **All others defected last round** | DEFECT once, then attempt cooperation | Punish but offer path back |
| **Mixed history (chaotic)** | COOPERATE if stock_health > 0.5 | Prioritize resource preservation |

---

## Collective Alignment

This strategy embodies collective thinking through:

1. **Resource-First Mentality**: Decisions prioritize stock health over individual round maximization. A depleted stock hurts everyone.

2. **Forgiveness Over Grudges**: Unlike pure Tit-for-Tat, this strategy forgives when others show improvement, enabling recovery from coordination failures.

3. **Crisis Solidarity**: When stock is critically low, always cooperate regardless of others' behavior - defecting from nothing gains nothing, but cooperation enables regeneration.

4. **Proportional Response**: Punishment scales with the severity of defection, avoiding overreaction to single defectors while firmly responding to widespread exploitation.

5. **Long-term Optimization**: The strategy recognizes that sustained cooperation yields higher total payoffs than cycles of exploitation and depletion.

---

## Expected Behavior Against Various Opponents

- **Against cooperators**: Mutual cooperation, full stock regeneration, consistent returns
- **Against defectors**: Initial cooperation, then matched defection, with periodic cooperation probes
- **Against mixed strategies**: Adaptive response favoring cooperation when sustainable
- **Against Tit-for-Tat variants**: Stable mutual cooperation after round 1
'''

description_COLLECTIVE_114 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective mindset**: we recognize that sustainable harvesting benefits everyone over the long run, and we aim to establish and maintain cooperation while protecting against exploitation. The key insight is that the resource regenerates optimally when stock remains around 50% of capacity, and universal cooperation achieves exactly this sustainable equilibrium.

## Strategy: "Generous Threshold Guardian"

### Decision Framework

The strategy makes decisions based on three factors:
1. **Resource health** (current stock relative to capacity)
2. **Community behavior** (observed cooperation rate in recent history)
3. **Game phase** (early, middle, or endgame)

### Detailed Decision Rules

#### Round 1: Unconditional Cooperation
- **Action: COOPERATE**
- Rationale: Signal cooperative intent, establish baseline for reciprocity, and preserve the resource for collective benefit.

#### Rounds 2 through (r-2): Adaptive Phase

Calculate two metrics:
- `stock_ratio = stock / capacity`
- `recent_coop_rate = (cooperations in last min(3, rounds_played)) / (n × min(3, rounds_played))`

**Decision Logic:**

```
IF stock_ratio < 0.25:
    # Critical resource state - attempt emergency recovery
    COOPERATE (regardless of history)
    
ELIF stock_ratio < 0.50:
    # Stressed resource - cooperate if others show willingness
    IF recent_coop_rate >= 0.4:
        COOPERATE
    ELSE:
        DEFECT (resource is being depleted anyway)
        
ELIF stock_ratio >= 0.50:
    # Healthy resource - reward cooperation, punish defection with forgiveness
    IF recent_coop_rate >= 0.6:
        COOPERATE
    ELIF recent_coop_rate >= 0.3:
        # Mixed environment - probabilistic cooperation
        COOPERATE with probability = recent_coop_rate + 0.2
    ELSE:
        # Low cooperation environment - protect self but occasionally test
        IF (round_number % 4 == 0):
            COOPERATE (periodic olive branch)
        ELSE:
            DEFECT
```

#### Round (r-1): Penultimate Round
- Follow the same adaptive logic as middle rounds
- Rationale: Maintain cooperative signaling; defecting here signals endgame exploitation

#### Round r (Final Round): Conditional Cooperation
```
IF recent_coop_rate >= 0.7 AND stock_ratio >= 0.5:
    COOPERATE (reward sustained cooperation)
ELSE:
    DEFECT (no future to protect)
```

### Key Strategic Elements

1. **Generous Thresholds**: The cooperation thresholds (0.4, 0.6) are intentionally generous to account for noise and encourage cooperation to emerge.

2. **Resource-First Priority**: When stock is critically low (<25% capacity), always cooperate to attempt recovery—even selfish extraction yields little from a depleted pool.

3. **Forgiveness Mechanism**: The periodic "olive branch" (every 4th round in hostile environments) allows cooperation to restart after breakdowns.

4. **Probabilistic Middle Ground**: When cooperation rates are mixed (30-60%), use probabilistic decisions to avoid being fully exploitable while remaining open to cooperation.

5. **History Window**: Using only the last 3 rounds (rather than full history) allows adaptation to changing opponent strategies.

### Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, history, n):
    stock_ratio = stock / capacity
    
    if round == 1:
        return COOPERATE
    
    recent_coop_rate = calculate_recent_cooperation(history, n, window=3)
    
    # Final round
    if round == total_rounds:
        if recent_coop_rate >= 0.7 and stock_ratio >= 0.5:
            return COOPERATE
        return DEFECT
    
    # Resource emergency
    if stock_ratio < 0.25:
        return COOPERATE
    
    # Stressed resource
    if stock_ratio < 0.50:
        return COOPERATE if recent_coop_rate >= 0.4 else DEFECT
    
    # Healthy resource
    if recent_coop_rate >= 0.6:
        return COOPERATE
    elif recent_coop_rate >= 0.3:
        return COOPERATE with probability (recent_coop_rate + 0.2)
    else:
        return COOPERATE if (round % 4 == 0) else DEFECT
```

This strategy balances collective welfare with self-protection, aiming to sustain the resource while adapting to whatever population of strategies it encounters.
'''

description_COLLECTIVE_115 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation sustains the resource indefinitely at maximum yield**, while defection creates a tragedy of the commons. My strategy aims to be a "good citizen" that cooperates by default, punishes exploitation to deter free-riding, but forgives to allow recovery.

## Strategy Name: **Sustainable Guardian**

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** - Preserve the resource for collective benefit
2. **Proportional accountability** - Respond to defection in a measured way
3. **Forgiveness with memory** - Allow recovery but track patterns

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists to judge others
- Establishes cooperative intent
- Preserves full resource stock for future rounds

### Rounds 2 through (r-1): Conditional Cooperation

**Cooperate if ANY of the following conditions hold:**

1. **Clean history**: All players cooperated in the previous round

2. **Stock health**: Current stock ≥ 0.7 × capacity AND defection rate in previous round was ≤ 1/n players (tolerate occasional single defector when resource is healthy)

3. **Recovery signal**: Stock increased from the previous round (indicating collective restraint is working)

4. **Forgiveness window**: After a period of punishment, if the last 2 consecutive rounds showed majority cooperation (>50% of players cooperated), return to cooperation

**Defect if ALL of the following hold:**

1. More than one player defected in the previous round, OR the same pattern of defection occurred in 2+ consecutive rounds

2. Stock < 0.7 × capacity (resource is stressed)

3. Not in a forgiveness window (recovery not yet demonstrated)

### Final Round (r): Conditional Based on History

- **Cooperate** if: The proportion of total cooperative actions across all players throughout the game exceeds 70%
- **Defect** if: Cooperation rate is below 70% (no future rounds to preserve resources for)

This avoids pure end-game defection while acknowledging that cooperation in a one-shot final round requires demonstrated collective commitment.

---

## Pseudocode

```
function decide(round, total_rounds, stock, capacity, history):
    n = number_of_players
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate metrics from history
    prev_round_defections = count_defections(history, round - 1)
    prev_round_defection_rate = prev_round_defections / n
    stock_ratio = stock / capacity
    stock_increasing = (stock > previous_stock)
    
    # Check for recovery pattern (forgiveness window)
    in_forgiveness_window = false
    if round >= 3:
        last_two_rounds_majority_coop = (
            cooperation_rate(history, round-1) > 0.5 AND
            cooperation_rate(history, round-2) > 0.5
        )
        in_forgiveness_window = last_two_rounds_majority_coop
    
    # Final round logic
    if round == total_rounds:
        overall_coop_rate = total_cooperations(history) / (n * (round - 1))
        if overall_coop_rate >= 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    # Main decision logic for middle rounds
    # Cooperate conditions
    if prev_round_defections == 0:
        return COOPERATE  # Clean history
    
    if stock_ratio >= 0.7 AND prev_round_defection_rate <= 1/n:
        return COOPERATE  # Tolerate single defector when healthy
    
    if stock_increasing:
        return COOPERATE  # Recovery is working
    
    if in_forgiveness_window:
        return COOPERATE  # Give cooperation another chance
    
    # Otherwise, defect as proportional response
    return DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1 | Cooperate | Establish trust, no information yet |
| Stock critically low (<20% capacity) | Cooperate | Defection would kill the resource entirely; only cooperation can save it |
| All others defecting consistently | Defect | No point in unilateral sacrifice |
| Single defector in healthy pool | Cooperate | Maintain resource, don't escalate |
| Final round after good cooperation | Cooperate | Honor the collective commitment |
| Final round after exploitation | Defect | No future to protect |

---

## Why This Strategy is Collectively Optimal

1. **Sustainability**: If all players use this strategy, everyone cooperates every round, stock stays at capacity, and each player earns `capacity/(2n)` per round—the maximum sustainable yield.

2. **Robustness**: Against defectors, it punishes to deter but forgives to enable recovery, preventing death spirals.

3. **Adaptability**: The stock-health and recovery-signal conditions allow the strategy to respond to actual resource state, not just actions.

4. **Collective alignment**: The strategy never initiates defection and only defects in response to observed exploitation, making it a trustworthy partner for other cooperative strategies.
'''

description_COLLECTIVE_116 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all players cooperate, the stock regenerates fully, providing consistent returns indefinitely. Any defection depletes the resource, harming everyone including the defector in future rounds.

## Strategy Name: **Guardian with Graduated Response**

### Decision Framework

The strategy operates on three principles:
1. **Start cooperatively** to signal collective intent
2. **Protect the resource** by responding proportionally to observed defection
3. **Forgive and rebuild** when conditions allow recovery

---

## Decision Rules

### Primary Decision Rule

```
IF first_round:
    COOPERATE

ELSE IF last_round:
    COOPERATE (see rationale below)

ELSE:
    Calculate threat_level = f(recent_defection_rate, stock_health)
    
    IF threat_level < LOW_THRESHOLD:
        COOPERATE
    ELSE IF threat_level < HIGH_THRESHOLD:
        COOPERATE with probability (1 - threat_level)
    ELSE:
        DEFECT (resource protection mode)
```

### Threat Level Calculation

```
stock_health = current_stock / capacity  # Range: 0 to 1
recent_defection_rate = defections_in_last_3_rounds / (n * 3)  # Range: 0 to 1

# Weight recent behavior more heavily when stock is depleted
urgency_multiplier = 1 + (1 - stock_health)  # Range: 1 to 2

threat_level = recent_defection_rate * urgency_multiplier
# Capped at 1.0
```

### Thresholds

```
LOW_THRESHOLD = 0.2   # Below this: full cooperation
HIGH_THRESHOLD = 0.7  # Above this: protective defection
```

---

## Edge Case Handling

### First Round
**Action: COOPERATE**
- Establishes cooperative intent
- No information yet to justify defection
- Collective benefit requires someone to lead with trust

### Last Round
**Action: COOPERATE**
- Defection in the final round gains at most `stock/n - stock/2n = stock/2n` extra
- This marginal gain is small compared to the value of maintaining a cooperative norm throughout
- If playing in a tournament with reputation effects, cooperation signals commitment to collective values

### Near-Depleted Stock (stock < capacity/4)
**Action: COOPERATE unconditionally**
- When stock is critically low, even small consumption matters
- Defection at low stock provides minimal absolute gain but prevents recovery
- This is the moment where collective discipline matters most

### Recovery Detection
```
IF stock_increased_from_previous_round AND stock > capacity/2:
    Reset threat_level to 0.5 * current_threat_level
    # Partial forgiveness - acknowledge improvement but remain cautious
```

---

## Detailed Pseudocode

```python
def decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    current_round = len(history) + 1
    current_stock = state.stock
    
    # First round: establish cooperation
    if current_round == 1:
        return COOPERATE
    
    # Critical stock protection
    if current_stock < capacity / 4:
        return COOPERATE
    
    # Calculate recent defection rate (last 3 rounds or all if fewer)
    lookback = min(3, len(history))
    recent_rounds = history[-lookback:]
    total_actions = sum(len(round.actions) for round in recent_rounds)
    total_defections = sum(
        sum(1 for action in round.actions if action == DEFECT)
        for round in recent_rounds
    )
    defection_rate = total_defections / total_actions if total_actions > 0 else 0
    
    # Calculate stock health
    stock_health = current_stock / capacity
    
    # Calculate threat level with urgency multiplier
    urgency = 1 + (1 - stock_health)
    threat_level = min(1.0, defection_rate * urgency)
    
    # Check for recovery (forgiveness mechanism)
    if len(history) >= 2:
        previous_stock = history[-1].stock_after
        if current_stock > previous_stock and stock_health > 0.5:
            threat_level *= 0.5
    
    # Decision based on threat level
    LOW_THRESHOLD = 0.2
    HIGH_THRESHOLD = 0.7
    
    if threat_level < LOW_THRESHOLD:
        return COOPERATE
    elif threat_level < HIGH_THRESHOLD:
        # Probabilistic cooperation - still lean toward cooperation
        cooperation_probability = 1 - threat_level
        return COOPERATE if random() < cooperation_probability else DEFECT
    else:
        # High threat: protect what remains
        return DEFECT
```

---

## Collective Alignment

This strategy embodies collective values by:

1. **Leading with trust**: Starting cooperatively assumes others share collective goals
2. **Protecting the commons**: Defecting only when necessary to prevent exploitation
3. **Forgiving recovery**: Returning to cooperation when the resource rebounds
4. **Prioritizing sustainability**: Never exploiting critically low stocks
5. **Last-round integrity**: Maintaining principles even when punishment is impossible

The strategy recognizes that **individual rationality in isolation leads to collective ruin**. By maintaining cooperation as the default and defecting only as a protective response, it creates conditions where other collective-minded players can sustain the resource together while limiting vulnerability to pure defectors.
'''

description_COLLECTIVE_117 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - when all cooperate, the stock regenerates fully, providing 12.5 units per player per round indefinitely. Universal defection destroys the resource immediately.

The strategy aims to:
1. Signal cooperative intent clearly
2. Protect the resource from collapse
3. Punish defection proportionally but allow redemption
4. Maximize collective welfare while remaining robust to exploitation

---

## Decision Rules

### Primary Rule: Stock-Conditional Cooperation with Graduated Response

```
COOPERATE if:
  - Stock health is critical (emergency preservation mode), OR
  - Cooperation history meets threshold AND stock is healthy enough

DEFECT if:
  - Retaliation is warranted against sustained defection, OR
  - End-game conditions apply AND cooperation has broken down
```

### Detailed Decision Logic

**Step 1: Calculate Key Metrics**
```
stock_ratio = current_stock / capacity
cooperation_rate = (total_C_plays_by_others) / (total_plays_by_others)
recent_coop_rate = cooperation_rate in last 3 rounds
rounds_remaining = r - current_round
```

**Step 2: Emergency Preservation Mode**
```
IF stock_ratio < 0.25:
    COOPERATE (unconditionally)
    // Resource is critically depleted - any defection risks permanent collapse
    // Even if others defect, we preserve what little remains
```

**Step 3: First Round**
```
IF round == 1:
    COOPERATE
    // Signal cooperative intent, establish baseline for reciprocity
```

**Step 4: Early Game (rounds 2 through r/3)**
```
IF in early game:
    IF recent_coop_rate >= 0.5:
        COOPERATE
    ELSE:
        COOPERATE with probability = stock_ratio
        // Give benefit of doubt early, but hedge if defection emerges
```

**Step 5: Mid Game (rounds r/3 through 2r/3)**
```
IF in mid game:
    IF recent_coop_rate >= 0.6:
        COOPERATE
    ELSE IF recent_coop_rate >= 0.3:
        // Tit-for-tat style: mirror majority behavior
        COOPERATE with probability = recent_coop_rate
    ELSE:
        // Sustained defection detected - limited retaliation
        DEFECT (but return to cooperation if others do)
```

**Step 6: Late Game (final r/3 rounds, excluding last 2)**
```
IF in late game (but not final 2 rounds):
    IF cooperation_rate >= 0.7 AND stock_ratio >= 0.5:
        COOPERATE
    ELSE IF stock_ratio >= 0.75:
        // Healthy stock, some defection - cautious cooperation
        COOPERATE with probability = 0.7
    ELSE:
        // Protect remaining stock
        COOPERATE if stock_ratio < 0.4
        Otherwise DEFECT
```

**Step 7: Final Two Rounds**
```
IF rounds_remaining <= 2:
    IF cooperation_rate >= 0.8 AND stock_ratio >= 0.5:
        COOPERATE
        // Honor sustained cooperation even at the end
    ELSE IF stock_ratio < 0.3:
        COOPERATE
        // Don't kill a dying resource
    ELSE:
        DEFECT
        // Standard end-game logic when trust is broken
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Establish trust baseline |
| Last round, high trust | Cooperate | Reward collective virtue |
| Last round, low trust | Defect | No future to protect |
| Stock near zero | Cooperate | Preserve any regeneration chance |
| Stock at capacity | Follow history-based rules | Full stock buffers small defections |
| Single defector among cooperators | Cooperate | Absorb minor exploitation for stability |
| Majority defecting | Conditional defection | Protect self while signaling willingness to return |

---

## Collective Alignment

This strategy embodies collective rationality by:
- **Starting cooperative** to enable coordination
- **Prioritizing resource survival** over short-term gains
- **Forgiving isolated defection** to maintain cooperation
- **Matching group behavior** to avoid being exploited while remaining open to recovery
- **Protecting the commons even when punished** if stock is critical

The strategy assumes other collective-minded agents will recognize that **the only way everyone wins is if everyone cooperates** - and acts to make that equilibrium focal.
'''

description_COLLECTIVE_118 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: I assume I am one of potentially many agents using this same strategy. Our goal is to maximize total group payoff across all rounds while remaining robust against defectors. The key insight is that **sustainable harvesting (all cooperate) maintains the resource indefinitely**, while defection depletes it for everyone.

## Strategy: Adaptive Threshold Guardian (ATG)

### Decision Framework

The strategy operates on three key principles:
1. **Default to cooperation** to maintain sustainable harvesting
2. **Punish defection proportionally** to deter exploitation
3. **Forgive strategically** to allow recovery and re-coordination

### Decision Rules

```
INPUTS:
- round: current round number (1 to r)
- stock: current stock level
- capacity: maximum sustainable stock
- n: number of players
- history: list of (my_action, all_actions, stock_before) for previous rounds

COMPUTE:
- rounds_remaining = r - round + 1
- defection_rate = (total defections in last min(3, rounds_played)) / (n × min(3, rounds_played))
- stock_ratio = stock / capacity
- sustainable_threshold = capacity / 2  # Below this, growth is suboptimal

DECISION LOGIC:

1. FIRST ROUND:
   → COOPERATE (establish cooperative baseline)

2. FINAL ROUND:
   IF stock_ratio > 0.8 AND defection_rate < 0.2 in recent history:
     → COOPERATE (reward sustained cooperation)
   ELSE:
     → DEFECT (no future to protect)

3. RESOURCE CRISIS (stock < sustainable_threshold / 2):
   → COOPERATE (emergency conservation - defecting here kills the resource)

4. PUNISHMENT PHASE (defection_rate > 0.5 in last 3 rounds):
   IF stock_ratio > 0.6:
     → DEFECT (punish widespread defection while resource can sustain it)
   ELSE:
     → COOPERATE (resource too depleted to risk further punishment)

5. FORGIVENESS CHECK (defection_rate dropped from >0.5 to <0.3):
   → COOPERATE (allow re-coordination after punishment)

6. STANDARD OPERATION:
   IF defection_rate < 0.25:
     → COOPERATE (maintain sustainable equilibrium)
   ELIF defection_rate < 0.5:
     → COOPERATE with probability (1 - defection_rate)
        DEFECT with probability defection_rate
   ELSE:
     → Apply punishment phase logic
```

### Pseudocode Implementation

```python
def decide(round, stock, capacity, n, r, history):
    rounds_remaining = r - round + 1
    stock_ratio = stock / capacity
    sustainable_threshold = capacity / 2
    
    # Calculate recent defection rate (last 3 rounds)
    lookback = min(3, len(history))
    if lookback == 0:
        defection_rate = 0
    else:
        recent_defections = sum(
            actions.count('D') 
            for (_, actions, _) in history[-lookback:]
        )
        defection_rate = recent_defections / (n * lookback)
    
    # Rule 1: First round - cooperate
    if round == 1:
        return 'C'
    
    # Rule 2: Final round
    if round == r:
        if stock_ratio > 0.8 and defection_rate < 0.2:
            return 'C'
        return 'D'
    
    # Rule 3: Resource crisis - emergency cooperation
    if stock < sustainable_threshold / 2:
        return 'C'
    
    # Rule 4 & 5: Respond to defection patterns
    if defection_rate > 0.5:
        if stock_ratio > 0.6:
            return 'D'  # Punish
        else:
            return 'C'  # Conserve
    
    # Rule 6: Standard operation
    if defection_rate < 0.25:
        return 'C'
    else:
        # Probabilistic response to moderate defection
        import random
        return 'C' if random.random() > defection_rate else 'D'
```

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperation signal |
| Final round, healthy stock + cooperation | C | Collective reward |
| Final round, otherwise | D | No future incentive |
| Stock near zero | C | Any defection destroys resource |
| All others defecting | D (if stock allows) | Don't be exploited |
| Mixed behavior | Probabilistic | Match environment uncertainty |

### Why This Works Collectively

When multiple agents use ATG:
- **Symmetric cooperation**: All start cooperating, stock maintains at capacity
- **Coordinated punishment**: If an outsider defects, all ATG agents detect and respond together
- **Synchronized forgiveness**: All return to cooperation when defection stops
- **Resource preservation**: Crisis protocol prevents collective ruin
'''

description_COLLECTIVE_119 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. However, it must also be **robust** against defectors who might exploit cooperators. The key insight is that the resource regenerates optimally when stock remains near 50% of capacity, and universal cooperation maintains this sustainable equilibrium.

## Strategy: "Sustainable Threshold with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Sustainability First**: Protect the resource from collapse
2. **Conditional Cooperation**: Start cooperative, respond proportionally to defection
3. **Forgiveness**: Allow recovery from temporary defection

### Decision Rules

```
PARAMETERS:
  - critical_threshold = 0.25 × capacity    // Below this, resource at risk
  - healthy_threshold = 0.6 × capacity      // Above this, resource is healthy
  - cooperation_baseline = 0.5              // Expected cooperation rate in equilibrium
  - memory_window = min(5, rounds_played)   // How far back to look

EACH ROUND:
  
  1. FIRST ROUND:
     → COOPERATE (establish cooperative norm)
  
  2. LAST ROUND:
     → If stock > critical_threshold AND observed_cooperation_rate ≥ 0.5:
         COOPERATE (reward sustained cooperation)
     → Otherwise:
         DEFECT (no future to protect)
  
  3. RESOURCE EMERGENCY (stock ≤ critical_threshold):
     → COOPERATE (prioritize resource survival over punishment)
     // Rationale: Defection here could cause irreversible collapse
  
  4. STANDARD PLAY (all other rounds):
     Calculate recent_cooperation_rate over memory_window
     
     If recent_cooperation_rate ≥ cooperation_baseline:
         → COOPERATE (reciprocate cooperative environment)
     
     Else if recent_cooperation_rate ≥ 0.25:
         → COOPERATE with probability = 2 × recent_cooperation_rate
         → DEFECT with probability = 1 - (2 × recent_cooperation_rate)
         // Graduated response: more defection observed → more likely to defect
     
     Else (recent_cooperation_rate < 0.25):
         → DEFECT (environment too hostile, protect self)
         // But check: if stock is recovering, give benefit of doubt
         If stock_trend is positive over last 3 rounds:
             → COOPERATE (signal willingness to rebuild)
```

### Measuring Cooperation Rate

```
observed_cooperation_rate = 
    (total C actions by all players in memory_window) / 
    (n × memory_window)

// If we can't observe individual actions, infer from stock dynamics:
inferred_cooperation = 
    (expected_stock_if_all_cooperate - actual_consumption) /
    (expected_stock_if_all_cooperate - expected_stock_if_all_defect)
```

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative norm |
| Final round, healthy stock | C if cooperation ≥ 50%, else D | Reward cooperation history |
| Stock near zero | C | Emergency conservation |
| Stock at capacity | C | Maintain optimal regeneration |
| All others defected last round | D (unless stock critical) | Proportional response |
| Mixed signals (some C, some D) | Probabilistic based on rate | Graduated response |

### Why This Works Collectively

1. **If all players use this strategy**: Everyone cooperates, stock stays at capacity, each player earns `capacity/(2n)` per round, growth replaces consumption perfectly.

2. **Against defectors**: The strategy doesn't get exploited indefinitely—it responds proportionally, making sustained defection unprofitable as stock depletes.

3. **Recovery mechanism**: The forgiveness elements (stock trend detection, probabilistic cooperation) allow groups to escape defection spirals.

4. **Resource protection**: The emergency cooperation rule prevents collective ruin even when trust has broken down.

### Expected Behavior Pattern

- Rounds 1-3: Cooperative probing
- Mid-game: Match observed cooperation level
- If stock drops: Emergency cooperation mode
- Late game: Maintain cooperation if rewarded, otherwise protect remaining value
- Final round: Reward or punish based on history
'''

description_COLLECTIVE_120 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed for a population of like-minded agents who all follow the same rules. Our goal is **collective long-term sustainability** - maximizing total group payoff across all rounds while being robust to occasional defection by outsiders.

The key insight: if all n players cooperate every round, the stock remains at capacity indefinitely, yielding each player `capacity/(2n)` per round. This is the **Pareto optimal equilibrium**. Our strategy coordinates on this outcome while including protective mechanisms.

---

## Decision Rules

### Primary Rule: Default to Cooperation

**Cooperate (C)** unless a specific defection trigger is met.

### Defection Triggers

**Trigger 1: End-Game Defection**
- In the **final round only**, play **D**
- Rationale: No future rounds to protect; defection is dominant in isolation

**Trigger 2: Critical Stock Emergency**
- If `stock < capacity / (2n)`, play **D**
- Rationale: Stock is so depleted that even cooperative harvesting yields negligible returns; extract remaining value before collapse

**Trigger 3: Retaliation Against Sustained External Defection**
- If in the previous round, the number of observed defections exceeds `n/2` (majority defected), play **D** for exactly **one round**, then return to cooperation
- Rationale: Punish mass defection to discourage exploitation, but forgive quickly to allow recovery

### Non-Triggers (Stay Cooperative)

- A single defector in previous round → **Cooperate** (tolerate minor deviation)
- Stock declining but above critical threshold → **Cooperate** (allow regeneration)
- First round → **Cooperate** (establish cooperative norm)

---

## Pseudocode

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Trigger 1: Final round - always defect
    if round == total_rounds:
        return DEFECT
    
    # Trigger 2: Critical stock emergency
    critical_threshold = capacity / (2 * n)
    if stock < critical_threshold:
        return DEFECT
    
    # Trigger 3: Retaliate against majority defection (with one-round memory)
    if round > 1:
        defections_last_round = count_defections(history[round - 1])
        if defections_last_round > n / 2:
            # Check if we already retaliated last round
            if round > 2:
                defections_two_rounds_ago = count_defections(history[round - 2])
                if defections_two_rounds_ago > n / 2:
                    # We retaliated last round; forgive and cooperate
                    return COOPERATE
            return DEFECT  # Retaliate this round
    
    # Default: Cooperate
    return COOPERATE
```

---

## Edge Case Handling

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline |
| **Final round** | Defect | No future to protect |
| **Stock near zero** | Defect | Extract remaining value |
| **Single defector observed** | Cooperate | Tolerate noise; don't escalate |
| **Majority defected once** | Defect once, then forgive | Proportional punishment |
| **Sustained majority defection** | Alternating D-C pattern | Punish but keep offering olive branch |
| **Stock recovering after depletion** | Cooperate once above threshold | Support regeneration |

---

## Why This Strategy is Collectively Optimal

1. **Self-sustaining equilibrium**: When all players use this strategy, everyone cooperates (except final round), stock stays at capacity, and total extraction is maximized over time.

2. **Robustness to outsiders**: The majority-threshold retaliation means a single non-cooperative outsider cannot exploit the group indefinitely, but minor deviations don't trigger destructive retaliation spirals.

3. **Forgiveness enables recovery**: One-round punishment followed by return to cooperation allows the stock to regenerate even after disruption.

4. **Simple coordination**: No need for complex signaling or role assignment - identical agents following identical rules naturally synchronize.

---

## Expected Outcomes

- **All collective agents**: Sustained capacity, each earns `(r-1) × capacity/(2n) + capacity/n` total
- **Mixed with few defectors**: Slight stock decline, collective agents still outperform pure defectors over multiple rounds
- **Against majority defectors**: Stock collapses, but collective agents extract proportionally during collapse
'''

description_COLLECTIVE_121 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the resource should be sustainably managed, maximizing long-term collective payoffs. However, it must also be **robust** against defectors and **adaptive** to observed behavior patterns.

The key insight is that universal cooperation maintains the stock at capacity (100% regeneration efficiency), while defection depletes the resource, harming everyone including the defector in future rounds.

## Strategy: "Sustainable Guardian"

### Decision Framework

The strategy makes decisions based on three factors:
1. **Resource health** - How depleted is the stock?
2. **Historical cooperation rate** - How have others behaved?
3. **Game phase** - Early, middle, or endgame considerations

### Detailed Decision Rules

#### Round 1: Unconditional Cooperation
- **Action: COOPERATE**
- Rationale: Signal cooperative intent, establish baseline for sustainable harvesting, give others a chance to demonstrate their strategy.

#### Rounds 2 through (r-1): Adaptive Cooperation

Calculate two key metrics each round:

**1. Stock Health Ratio:**
```
health = current_stock / capacity
```

**2. Historical Cooperation Rate:**
```
For each past round, estimate cooperation:
  - If stock regenerated to capacity (or near it): assume high cooperation
  - If stock declined significantly: assume defection occurred
  
Approximation method:
  expected_stock_if_all_C = previous_stock (stays at capacity if healthy)
  expected_stock_if_all_D = 0 (complete depletion)
  
  inferred_defection_rate = how much worse than all-C outcome we observed
```

**Decision Logic:**

```
IF health < 0.25 THEN:
    # Critical resource state - must cooperate to allow recovery
    # Defecting now yields little and destroys future value
    ACTION = COOPERATE

ELSE IF health >= 0.75 AND historical_cooperation_rate >= 0.7 THEN:
    # Healthy resource, cooperative environment
    ACTION = COOPERATE

ELSE IF health >= 0.75 AND historical_cooperation_rate < 0.5 THEN:
    # Healthy resource but others are exploiting
    # Match the prevailing behavior with slight bias toward cooperation
    # This creates pressure without complete defection
    IF last_round_showed_significant_depletion THEN:
        ACTION = DEFECT (protective/punishing)
    ELSE:
        ACTION = COOPERATE (forgiveness)

ELSE IF 0.25 <= health < 0.75 THEN:
    # Moderate resource state - conditional cooperation
    IF last_round_showed_recovery_or_stability THEN:
        ACTION = COOPERATE
    ELSE:
        # Tit-for-tat style: mirror aggregate behavior
        IF stock_declined_more_than_10%_unexpectedly THEN:
            ACTION = DEFECT
        ELSE:
            ACTION = COOPERATE
```

#### Final Round (Round r): Conditional Defection

```
IF historical_cooperation_rate >= 0.8 AND health >= 0.5 THEN:
    # Reward sustained cooperation - stay cooperative
    ACTION = COOPERATE
ELSE:
    # No future rounds to lose - protect against exploitation
    ACTION = DEFECT
```

### Key Design Principles

1. **Forgiveness**: After punishing defection, quickly return to cooperation if others do
2. **Proportionality**: Response matches severity of exploitation
3. **Resource Protection**: Always cooperate when stock is critically low (collective survival)
4. **End-game Awareness**: Don't be naive in final round, but reward sustained cooperation

### Pseudocode Summary

```python
def decide(round, total_rounds, current_stock, capacity, history):
    health = current_stock / capacity
    n_players = get_n_players()
    
    # Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate historical cooperation (estimate from stock trajectory)
    coop_rate = estimate_cooperation_rate(history, capacity, n_players)
    recent_trend = get_recent_trend(history)  # 'improving', 'stable', 'declining'
    
    # Final round
    if round == total_rounds:
        if coop_rate >= 0.8 and health >= 0.5:
            return COOPERATE
        return DEFECT
    
    # Critical resource - must cooperate
    if health < 0.25:
        return COOPERATE
    
    # Healthy resource
    if health >= 0.75:
        if coop_rate >= 0.6:
            return COOPERATE
        elif recent_trend == 'declining':
            return DEFECT
        else:
            return COOPERATE
    
    # Moderate resource (0.25 <= health < 0.75)
    if recent_trend in ['improving', 'stable']:
        return COOPERATE
    else:
        return DEFECT
```

### Why This Strategy Works Collectively

- **Self-sustaining**: If all players use this strategy, everyone cooperates, stock stays at capacity, and all players get consistent payoffs every round
- **Punishes exploitation**: Defectors face retaliation, making sustained defection unprofitable
- **Protects the commons**: Prioritizes resource recovery when depleted
- **Adapts gracefully**: Works against various opponent types without catastrophic failure
'''

description_COLLECTIVE_122 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation is the only sustainable equilibrium** - it maintains stock at capacity indefinitely, yielding consistent returns. Any defection triggers a tragedy of the commons spiral that hurts everyone, including defectors.

## Strategy Name: "Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Start cooperative** to signal collective intent and preserve resources
2. **Respond proportionally** to observed behavior to deter exploitation
3. **Forgive strategically** to enable recovery when others show cooperative intent

---

## Decision Rules

### Round 1: Always Cooperate
- No history exists, so extend trust
- This maximizes initial stock preservation and signals cooperative intent
- Rationale: Defecting first poisons the well for everyone

### Rounds 2 through (r-1): Conditional Cooperation

**Calculate the "Cooperation Ratio" from the previous round:**
```
cooperation_ratio = (number of players who played C in previous round) / n
```

**Decision Rule:**
```
IF cooperation_ratio ≥ 0.5:
    PLAY C (Cooperate)
ELSE IF cooperation_ratio > 0 AND stock > capacity/4:
    PLAY C with probability = cooperation_ratio × 2
    PLAY D with probability = 1 - (cooperation_ratio × 2)
ELSE:
    PLAY D (Defect)
```

**Rationale:**
- When majority cooperates, maintain cooperation to preserve the virtuous cycle
- When minority cooperates but resources remain viable, use probabilistic response to:
  - Sometimes cooperate to model good behavior and enable recovery
  - Sometimes defect to avoid being exploited by consistent defectors
- When almost no one cooperates OR stock is critically low, defect to avoid being the sole sucker

### Stock-Based Override

Regardless of cooperation ratio:
```
IF stock < capacity / (2n):
    PLAY C unconditionally
```

**Rationale:** When stock is critically depleted, any defection accelerates collapse. Even if others defect, my cooperation slightly slows the death spiral and signals willingness to rebuild.

### Last Round: Conditional Based on History

```
IF (total cooperation across all previous rounds) / (n × (r-1)) ≥ 0.6:
    PLAY C (reward collective cooperation)
ELSE:
    PLAY D (no future to preserve)
```

**Rationale:** Unlike standard backward induction logic that says "always defect in the last round," this strategy recognizes that:
- If the group has maintained cooperation, defecting betrays that trust needlessly
- The marginal gain from last-round defection is small compared to the principle of collective commitment
- However, if the group has been largely defecting, there's no cooperative norm to honor

---

## Complete Pseudocode

```
function decide(round, history, stock, n, r, capacity):
    
    # First round: always cooperate
    if round == 1:
        return COOPERATE
    
    # Calculate previous round cooperation
    prev_round_actions = history[round - 1]
    cooperators = count(prev_round_actions where action == C)
    cooperation_ratio = cooperators / n
    
    # Critical stock override: cooperate to prevent collapse
    if stock < capacity / (2 * n):
        return COOPERATE
    
    # Last round logic
    if round == r:
        total_cooperation = sum(count C in each round) / (n * (r - 1))
        if total_cooperation >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    # Middle rounds: graduated response
    if cooperation_ratio >= 0.5:
        return COOPERATE
    elif cooperation_ratio > 0 and stock > capacity / 4:
        # Probabilistic: lean toward cooperation proportionally
        if random() < cooperation_ratio * 2:
            return COOPERATE
        else:
            return DEFECT
    else:
        return DEFECT
```

---

## Why This Strategy is Collectively Optimal

1. **Self-reinforcing cooperation**: When multiple players use this strategy, they maintain cooperation throughout, preserving stock at capacity and maximizing total payoffs.

2. **Robust to exploitation**: The graduated defection response prevents consistent free-riders from profiting indefinitely at cooperators' expense.

3. **Enables recovery**: The probabilistic cooperation and forgiveness mechanisms allow a damaged game to recover if defectors reform.

4. **Stock-aware**: By conditioning on resource levels, the strategy adapts to the actual state of the commons, not just behavioral history.

5. **Collectively rational last round**: Resists the backward induction trap that leads to universal defection.
'''

description_COLLECTIVE_123 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective sustainability mindset**: the shared resource is our commons, and its long-term health benefits everyone. However, we must be adaptive since we cannot assume others share this view. The strategy balances:
1. **Stewardship** - protecting the resource for future rounds
2. **Reciprocity** - responding to observed behavior patterns
3. **Forgiveness** - allowing recovery from defection spirals
4. **Pragmatism** - recognizing when cooperation is futile

## Strategy: "Sustainable Reciprocity"

### Decision Framework

The strategy uses three key metrics calculated from history:
- **Cooperation Rate**: fraction of C plays observed in previous round
- **Stock Health**: current stock / capacity (0 to 1)
- **Trend**: is stock increasing, stable, or declining over recent rounds?

### Decision Rules

```
FUNCTION decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key metrics
    stock_health = stock / capacity
    rounds_remaining = total_rounds - round
    
    IF round == 1:
        RETURN Cooperate  # Start with trust
    
    # Get previous round data
    prev_coop_rate = count(C in previous round) / n
    
    # PHASE 1: Critical Resource Protection
    IF stock_health < 0.15:
        # Resource near collapse - cooperate to allow any recovery
        RETURN Cooperate
    
    # PHASE 2: End-Game Logic
    IF rounds_remaining <= 2:
        IF prev_coop_rate >= 0.7:
            # Maintain cooperation even at end if group is cooperative
            RETURN Cooperate
        ELSE:
            # Defect if others aren't cooperating anyway
            RETURN Defect
    
    # PHASE 3: Reciprocity-Based Decision
    
    # Calculate cooperation threshold based on stock health
    # When stock is healthy, we're more forgiving
    # When stock is stressed, we demand more cooperation
    base_threshold = 0.5
    health_adjustment = (stock_health - 0.5) * 0.3  # ±0.15 adjustment
    coop_threshold = base_threshold - health_adjustment
    # Results in threshold ~0.35 when healthy, ~0.65 when stressed
    
    IF prev_coop_rate >= coop_threshold:
        RETURN Cooperate
    
    # PHASE 4: Forgiveness Mechanism
    # Every few rounds, give cooperation another chance
    IF round % 5 == 0 AND stock_health > 0.3:
        RETURN Cooperate  # Periodic olive branch
    
    # PHASE 5: Default to Defect
    # If we reach here, cooperation isn't being reciprocated
    RETURN Defect
```

### Detailed Rule Explanations

**Round 1: Unconditional Cooperation**
- Signal cooperative intent
- Establish baseline for reciprocity
- No history to react to anyway

**Critical Resource Protection (stock < 15% capacity)**
- When the resource is near collapse, everyone loses from further defection
- Cooperating here is a desperate but rational attempt to allow regeneration
- Even if others defect, the marginal gain from defection on a tiny stock is minimal

**End-Game Handling**
- In final 2 rounds, backward induction pressure is real
- If the group has been cooperative (≥70%), maintain trust to the end
- If the group has been defecting, no point in unilateral sacrifice

**Reciprocity Threshold (Dynamic)**
- Core mechanism: cooperate if enough others cooperated
- Threshold adjusts with resource health:
  - Healthy stock (80%+): threshold ~0.38 - more forgiving
  - Stressed stock (20%): threshold ~0.59 - demand more cooperation
- This creates pressure to cooperate more when resources are scarce

**Periodic Forgiveness**
- Every 5th round, cooperate regardless (if stock isn't critical)
- Breaks defection spirals
- Tests if opponents are willing to restart cooperation
- Allows recovery from miscoordination

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| Final round, cooperative history | C | Reward sustained cooperation |
| Final round, mixed/defecting history | D | No future to invest in |
| Stock near zero | C | Tiny stocks make D gains minimal |
| All others defected last round | D (unless forgiveness round) | Don't be exploited |
| Perfect cooperation so far | C | Don't break what's working |

### Why This Strategy is Collectively Optimal

1. **Sustainable Equilibrium**: If all players use this strategy, everyone cooperates, stock remains at capacity, and everyone earns capacity/(2n) every round - the maximum sustainable outcome.

2. **Punishes Defection**: Defectors trigger threshold failures, causing reciprocal defection - making sustained defection unprofitable.

3. **Self-Healing**: Forgiveness mechanism allows groups to escape defection spirals and return to cooperation.

4. **Resource-Aware**: Adjusts behavior based on actual commons health, not just opponent actions.
'''

description_COLLECTIVE_124 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and mutually beneficial. The key insight is that universal cooperation maintains the resource at capacity indefinitely, yielding consistent payoffs, while defection creates a tragedy of the commons.

## Strategy: "Sustainable Threshold Guardian"

### Decision Framework

The strategy operates on three principles:
1. **Sustainability First**: Protect the resource stock to ensure long-term collective payoffs
2. **Proportional Response**: React to defection in a measured way that discourages exploitation without triggering collapse
3. **Forgiveness with Memory**: Allow recovery but remember patterns of defection

### Decision Rules

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    stock_ratio = current_stock / capacity
    rounds_remaining = total_rounds - round
    
    # --- RULE 1: First Round - Establish Cooperation ---
    IF round == 1:
        RETURN COOPERATE
    
    # --- RULE 2: Last Round Consideration ---
    IF rounds_remaining == 0:
        # In final round, cooperate if stock is healthy and group has been cooperative
        IF stock_ratio >= 0.5 AND recent_defection_rate(history, 3) < 0.25:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # --- RULE 3: Critical Stock Protection ---
    # If stock is dangerously low, cooperate to allow recovery
    IF stock_ratio < 0.25:
        RETURN COOPERATE
    
    # --- RULE 4: Respond to Group Behavior ---
    recent_defection_rate = calculate_defection_rate(history, last_3_rounds)
    
    # If group is largely cooperative, cooperate
    IF recent_defection_rate < 0.2:
        RETURN COOPERATE
    
    # If moderate defection, use probabilistic response
    IF recent_defection_rate < 0.5:
        # Cooperate with probability inversely proportional to defection
        cooperation_probability = 1 - recent_defection_rate
        RETURN COOPERATE with probability cooperation_probability
    
    # --- RULE 5: High Defection Environment ---
    # If majority defecting, protect remaining value but signal willingness to cooperate
    IF stock_ratio > 0.6:
        # Stock still healthy despite defection - try to maintain cooperation
        RETURN COOPERATE
    ELSE:
        # Stock depleting due to defection - match behavior to avoid exploitation
        RETURN DEFECT
    
    # --- DEFAULT: Cooperate ---
    RETURN COOPERATE
```

### Detailed Rule Explanations

**Rule 1 - First Round**: Always cooperate to signal cooperative intent and establish a sustainable baseline. If all players use this strategy, we immediately achieve the optimal sustainable equilibrium.

**Rule 2 - Last Round**: In the final round, there's no future to protect. However, if the group has been cooperative and stock is healthy, maintain cooperation as a collective commitment. Otherwise, defect since there's no recovery opportunity.

**Rule 3 - Critical Stock Protection**: When stock falls below 25% of capacity, always cooperate. This is the "guardian" aspect - even if others defect, protecting a critically low stock prevents total collapse and preserves some future value.

**Rule 4 - Proportional Response**: Use the recent defection rate (last 3 rounds) to calibrate response. This creates a smooth gradient rather than harsh punishment, allowing recovery from occasional defections.

**Rule 5 - Adaptive Defense**: In high-defection environments, the response depends on stock health. If stock remains healthy, continue cooperating to demonstrate the sustainable path. If stock is depleting, match defection to avoid being exploited.

### Why This Strategy is Collectively Optimal

If all n players use this strategy:
- Round 1: All cooperate → stock stays at capacity
- Subsequent rounds: All see 0% defection rate → all cooperate
- Outcome: Stock maintains at capacity, each player earns `capacity/(2n)` per round
- Total per player: `r × capacity/(2n)`

This is the **maximum sustainable collective payoff**.

### Robustness to Exploiters

- **Against pure defectors**: The strategy eventually defects back, limiting exploitation
- **Against conditional cooperators**: Maintains cooperation through consistent signaling
- **Against random strategies**: Probabilistic response prevents pattern exploitation
- **Stock protection rule**: Prevents complete resource collapse even under adversarial conditions
'''

description_COLLECTIVE_125 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed with a **collective mindset**: if all players adopt this same strategy, the outcome should be sustainable and beneficial for everyone. The strategy balances cooperation to maintain the resource with adaptive responses to exploitation.

## Strategy: "Sustainable Threshold with Graduated Response"

### Key Principles

1. **Sustainability First**: Cooperate by default to maintain the resource at productive levels
2. **Collective Signaling**: Use cooperation as a signal that we're playing collectively
3. **Graduated Response**: Respond proportionally to observed defection, but remain forgiving
4. **Endgame Awareness**: Adjust behavior near the final rounds while avoiding pure exploitation

---

### Decision Rules

#### Round 1: Always Cooperate
- **Rationale**: Establish cooperative intent. If all players share this strategy, we start sustainably. This also serves as a coordination signal.

#### Middle Rounds (2 to r-2): Adaptive Threshold Strategy

**Primary Rule**: Cooperate if the following conditions are met:

1. **Stock Health Check**: `stock >= capacity * 0.4`
   - If stock falls below 40% capacity, the resource is stressed

2. **Recent Cooperation Check**: In the previous round, at least `(n-1)/2` other players cooperated (i.e., majority cooperated)

3. **Cumulative Trust Check**: Over all previous rounds, the cooperation rate among all players is at least 50%

**If any condition fails**, apply graduated response:

```
defection_rate = (total_defections_observed) / (total_actions_observed)

if defection_rate > 0.7:
    Defect  # Widespread exploitation - protect yourself
elif defection_rate > 0.5:
    Defect with probability 0.5, else Cooperate  # Mixed response
elif stock < capacity * 0.25:
    Defect  # Resource critically low - grab remaining value
else:
    Cooperate  # Give cooperation another chance
```

**Forgiveness Mechanism**: Every 3 rounds, if currently in a defection pattern, attempt one "probe cooperation" to test if collective cooperation can be restored.

#### Final Two Rounds (r-1 and r):

**Round r-1**:
- If cooperation rate in game > 60% AND stock > capacity * 0.5: **Cooperate**
- Otherwise: **Defect**

**Round r (Final)**:
- If stock > capacity * 0.3 AND game-wide cooperation rate > 70%: **Cooperate** (reward collective success)
- Otherwise: **Defect** (no future rounds to sustain)

---

### Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Stock = 0 | Cooperate | Taking 0/n vs 0/2n is the same; signal willingness to rebuild |
| Stock near capacity | Cooperate | Resource is healthy; maintain it |
| Only 2 players (n=2) | Weight cooperation more heavily | Easier to establish mutual cooperation |
| Many players (n>6) | Slightly lower cooperation threshold | Harder to achieve unanimous cooperation |
| Single defector among many cooperators | Continue cooperating | Don't let one bad actor collapse the system |

---

### Pseudocode Summary

```
function decide(round, stock, history, n, r, capacity):
    
    if round == 1:
        return COOPERATE
    
    coop_rate = count_cooperations(history) / total_actions(history)
    last_round_coops = count_cooperations(history[round-1])
    
    # Final round
    if round == r:
        if stock > 0.3 * capacity AND coop_rate > 0.7:
            return COOPERATE
        return DEFECT
    
    # Penultimate round
    if round == r - 1:
        if stock > 0.5 * capacity AND coop_rate > 0.6:
            return COOPERATE
        return DEFECT
    
    # Middle rounds
    stock_healthy = (stock >= 0.4 * capacity)
    majority_cooperated = (last_round_coops >= (n-1) / 2)
    overall_trust = (coop_rate >= 0.5)
    
    if stock_healthy AND majority_cooperated AND overall_trust:
        return COOPERATE
    
    # Forgiveness probe every 3 rounds
    if round % 3 == 0:
        return COOPERATE
    
    # Graduated response
    defect_rate = 1 - coop_rate
    if defect_rate > 0.7 OR stock < 0.25 * capacity:
        return DEFECT
    elif defect_rate > 0.5:
        return random_choice(COOPERATE, DEFECT)  # 50-50
    else:
        return COOPERATE
```

---

### Why This Strategy is Collectively Optimal

- **If everyone uses it**: All cooperate throughout (except possibly final round), stock remains at capacity, everyone earns `capacity/(2n)` per round consistently
- **Against defectors**: Graduated response limits losses without immediately collapsing into mutual defection
- **Self-sustaining**: The cooperation signals and thresholds create stable equilibria when playing against copies of itself
'''

description_COLLECTIVE_126 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that must be preserved for collective long-term benefit. The fundamental insight is that **universal cooperation sustains the resource indefinitely** (stock regenerates fully when all cooperate), while defection creates a tragedy of the commons. However, we must be robust to defectors without being exploitable.

## Strategy: "Sustainable Guardian with Graduated Response"

### Decision Framework

The strategy operates on three principles:
1. **Default to cooperation** to signal collective intent and preserve the resource
2. **Respond proportionally to defection** to discourage exploitation without spiraling into mutual destruction
3. **Protect the resource floor** to ensure some payoff remains possible for everyone

---

### Decision Rules (Pseudocode)

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    defection_rate = count_defections_last_round(history) / n
    stock_ratio = stock / capacity
    critical_threshold = capacity / (4 * n)  # Below this, resource is in crisis
    
    # RULE 1: First Round - Always Cooperate
    if round == 1:
        return COOPERATE
    
    # RULE 2: Resource Crisis Protection
    # If stock is critically low, cooperate to allow regeneration
    if stock < critical_threshold:
        return COOPERATE
    
    # RULE 3: Final Round Consideration
    # In the very last round, match the previous round's majority behavior
    if rounds_remaining == 0:
        if defection_rate > 0.5:
            return DEFECT
        else:
            return COOPERATE
    
    # RULE 4: Graduated Response to Defection
    # Probability of defecting increases with observed defection rate
    # But we're slightly more forgiving to encourage return to cooperation
    
    if defection_rate == 0:
        # Everyone cooperated - maintain cooperation
        return COOPERATE
    
    elif defection_rate <= 0.25:
        # Minor defection - stay cooperative, signal sustainability
        return COOPERATE
    
    elif defection_rate <= 0.5:
        # Moderate defection - probabilistic response
        # Cooperate with probability inversely proportional to defection
        # But weight toward cooperation when resource is healthy
        cooperation_probability = (1 - defection_rate) * min(stock_ratio + 0.2, 1.0)
        return COOPERATE with probability cooperation_probability, else DEFECT
    
    elif defection_rate <= 0.75:
        # High defection - defensive posture but leave door open
        # Consider rounds remaining - more forgiving early game
        forgiveness_factor = rounds_remaining / total_rounds
        if random() < forgiveness_factor * 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    else:
        # Severe defection (>75%) - protect self but watch for recovery
        # Still occasionally cooperate to test if others will follow
        if round % 3 == 0:  # Periodic olive branch
            return COOPERATE
        else:
            return DEFECT
```

---

### Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | Cooperate | Establish cooperative baseline; no information to act on |
| **Last Round** | Mirror majority | No future to protect; match prevailing behavior |
| **Stock near zero** | Cooperate | Any defection kills the resource entirely; regeneration needs cooperation |
| **Stock at capacity** | Follow graduated response | Resource is healthy; focus on maintaining cooperation |
| **Single defector appeared** | Cooperate | One defector might be testing; don't escalate |
| **All defected last round** | Mostly defect with periodic cooperation | Protect self while signaling willingness to reset |

---

### Why This Strategy Aligns with Collective Interest

1. **Sustains the resource**: When matched with similar strategies, universal cooperation maintains stock at capacity indefinitely, maximizing total payoff across all rounds.

2. **Not exploitable**: Graduated response means persistent defectors face retaliation, making defection unprofitable over time.

3. **Recoverable**: Periodic cooperation attempts and forgiveness for low defection rates allow groups to return to sustainable equilibrium after disruption.

4. **Crisis-aware**: Protecting critically low stock benefits everyone—even defectors get nothing from an empty pool.

5. **Proportional**: Doesn't overreact to noise or single defectors, maintaining stability.

The strategy essentially asks: *"What would we all do if we understood that cooperation is the only path to maximum collective returns?"*—and then implements that while protecting against those who don't share this understanding.
'''

description_COLLECTIVE_127 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy embraces a **collective stewardship** mindset: we treat the common pool as a shared resource whose long-term health benefits everyone. The key insight is that universal cooperation is self-sustaining (stock regenerates fully), while defection creates a tragedy of the commons. Our goal is to signal cooperative intent, encourage coordination toward the sustainable equilibrium, and only defect when the resource is already doomed or when we're in the endgame.

---

## Strategy: "Sustainable Threshold Guardian"

### Decision Framework

The strategy makes decisions based on three key factors:
1. **Stock health** - Is the resource sustainable?
2. **Cooperation history** - Are others cooperating?
3. **Time horizon** - How many rounds remain?

---

### Detailed Decision Rules

#### Round 1: Unconditional Cooperation
- **Action: COOPERATE**
- Rationale: Signal cooperative intent, establish baseline for detecting others' behavior, and give the collective a chance to coordinate.

#### Rounds 2 through (r-2): Adaptive Cooperation

Calculate two metrics:
1. **Stock Ratio** = current_stock / capacity
2. **Cooperation Rate** = (observed cooperations in previous round) / (n-1)

**Decision Logic:**

```
IF stock_ratio >= 0.5:
    # Resource is healthy
    IF cooperation_rate >= 0.5:
        # Majority cooperating - continue cooperating
        ACTION = COOPERATE
    ELSE:
        # Majority defecting but resource still viable
        # Give one "grace round" after defection spike, then match
        IF previous_round_was_grace:
            ACTION = DEFECT
        ELSE:
            ACTION = COOPERATE (mark as grace round)
            
ELSE IF stock_ratio >= 0.25:
    # Resource stressed but recoverable
    IF cooperation_rate >= 0.6:
        # Strong cooperation signal - cooperate to help recovery
        ACTION = COOPERATE
    ELSE:
        # Not enough cooperation to recover sustainably
        ACTION = DEFECT
        
ELSE:
    # Resource critically depleted (stock < 25% capacity)
    # Defect - the commons is collapsing regardless
    ACTION = DEFECT
```

#### Round (r-1): Penultimate Round
- **If stock_ratio >= 0.5 AND cooperation_rate >= 0.6**: COOPERATE
- **Otherwise**: DEFECT
- Rationale: Slightly tighten cooperation threshold as endgame approaches.

#### Final Round (r): 
- **Action: DEFECT**
- Rationale: No future rounds to preserve resources for. This is the dominant strategy in the last round, and sophisticated opponents will expect this.

---

### Edge Cases

1. **n = 2 (two players)**: 
   - Cooperation rate is binary (0% or 100%)
   - If opponent cooperated last round AND stock >= 50%: COOPERATE
   - Otherwise: DEFECT (except round 1)

2. **Stock = 0**: 
   - Action is irrelevant (payoff is 0 regardless)
   - Technically COOPERATE (costs nothing, signals intent if stock somehow recovers)

3. **Very short games (r ≤ 3)**:
   - Round 1: COOPERATE
   - Round 2+: DEFECT (insufficient horizon for cooperation benefits)

4. **Stock above capacity after calculation**: 
   - Treat as capacity (already handled by min function)

---

### Pseudocode Summary

```python
def decide(round_num, total_rounds, current_stock, capacity, n, history):
    stock_ratio = current_stock / capacity
    
    # First round: always cooperate
    if round_num == 1:
        return COOPERATE
    
    # Very short games: defect after round 1
    if total_rounds <= 3 and round_num > 1:
        return DEFECT
    
    # Final round: always defect
    if round_num == total_rounds:
        return DEFECT
    
    # Calculate cooperation rate from last round
    coop_rate = count_cooperators(history[-1]) / (n - 1)
    
    # Critical depletion: defect
    if stock_ratio < 0.25:
        return DEFECT
    
    # Stressed resource
    if stock_ratio < 0.5:
        return COOPERATE if coop_rate >= 0.6 else DEFECT
    
    # Healthy resource
    if coop_rate >= 0.5:
        return COOPERATE
    else:
        # Grace mechanism: cooperate once after defection spike
        if not used_grace_this_phase:
            mark_grace_used()
            return COOPERATE
        return DEFECT
```

---

### Why This Strategy Works Collectively

1. **Sustainability-focused**: Prioritizes keeping stock above regeneration thresholds
2. **Forgiving**: Grace rounds allow recovery from temporary defection
3. **Responsive**: Matches defection when cooperation clearly isn't viable
4. **Realistic about endgame**: Doesn't naively cooperate when others will certainly defect
5. **Robust**: Works against pure cooperators, pure defectors, and mixed strategies
'''

description_COLLECTIVE_128 = '''
# Collective Strategy for Common Pool Resource Game

## Core Philosophy

This strategy treats the common pool as a shared inheritance that sustains everyone across rounds. The fundamental insight is that **universal cooperation is self-sustaining** (stock regenerates fully) while **widespread defection is catastrophic** (stock collapses to zero). My strategy aims to be a reliable cooperator that helps establish and maintain sustainable harvesting, while protecting against exploitation through measured, forgiving responses.

## Decision Rules

### Primary Decision Framework

**Cooperate (C)** when:
1. It's early in the game (building trust and stock health)
2. The majority of players cooperated in the previous round
3. Stock levels are healthy relative to capacity
4. After punishing defection, to offer reconciliation

**Defect (D)** when:
1. It's the final round (no future to protect)
2. Stock is critically depleted AND defection was widespread (salvage mode)
3. Responding proportionally to observed defection (tit-for-tat element)

### Detailed Decision Logic

```
function decide(round, total_rounds, stock, capacity, history, n):
    
    # ROUND 1: Always cooperate to signal good faith
    if round == 1:
        return COOPERATE
    
    # FINAL ROUND: Defect (no future cooperation to preserve)
    if round == total_rounds:
        return DEFECT
    
    # Calculate key metrics
    stock_ratio = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Count defectors in previous round
    defectors_last_round = count_defections(history, round - 1)
    defection_rate = defectors_last_round / n
    
    # CRITICAL DEPLETION: If stock < capacity/(2n), resource is dying
    if stock_ratio < 1/(2*n):
        # If most are defecting, salvage what we can
        if defection_rate > 0.5:
            return DEFECT
        # Otherwise, desperately try to restore
        return COOPERATE
    
    # HEALTHY STOCK (ratio > 0.5): Be generous, cooperate
    if stock_ratio > 0.5:
        # Cooperate unless defection is rampant
        if defection_rate <= 0.5:
            return COOPERATE
        # Even with some defection, cooperate if stock is very healthy
        if stock_ratio > 0.75:
            return COOPERATE
        # Proportional response: defect with probability = defection_rate
        return probabilistic_response(defection_rate)
    
    # MODERATE STOCK (0.25 < ratio <= 0.5): Be cautious
    if stock_ratio > 0.25:
        if defection_rate <= 0.25:
            return COOPERATE
        if defection_rate >= 0.75:
            return DEFECT
        # Mirror the dominant behavior
        return probabilistic_response(defection_rate)
    
    # LOW STOCK (ratio <= 0.25): Conservation critical
    if defection_rate <= 0.25:
        return COOPERATE  # Try to save the resource
    return DEFECT  # Others are depleting anyway

function probabilistic_response(defection_rate):
    # Defect with probability equal to observed defection rate
    # This is proportional, not vindictive
    if random() < defection_rate:
        return DEFECT
    return COOPERATE
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | Cooperate | Signal cooperative intent, no history to react to |
| **Final round** | Defect | No future rounds to protect; game-theoretic necessity |
| **Second-to-last round** | Follow normal rules | Don't trigger early collapse |
| **Stock at capacity** | Cooperate | Maximum buffer, maximum generosity |
| **Stock near zero** | Context-dependent | Cooperate if others might too; defect if collapse is inevitable |
| **All others defected** | Defect once, then cooperate | One-round punishment, then offer olive branch |
| **n=2 (two players)** | Stricter tit-for-tat | Partner's choice fully determines outcome |

## Why This Strategy is Collectively Aligned

1. **Starts cooperative**: Gives the group the best chance to establish sustainable equilibrium
2. **Forgives quickly**: One bad round doesn't trigger permanent retaliation
3. **Proportional responses**: Doesn't over-punish, maintaining hope for recovery
4. **Stock-aware**: Prioritizes resource health over short-term gains
5. **Tolerates minority defection**: A few defectors don't collapse cooperation
6. **Clear signals**: Behavior is predictable, helping others coordinate

This strategy succeeds when paired with similar strategies (mutual cooperation sustains the resource) while protecting against pure defectors (proportional retaliation limits losses).
'''

description_EXPLOITATIVE_1 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in this game: defectors extract twice as much as cooperators from the same pool. The key insight is that **sustainable exploitation requires keeping the resource alive long enough to extract maximum value**, while also punishing cooperators who create value I can steal.

## Strategic Framework

### Key Observations

1. **Defection is always locally dominant** - In any single round, D yields exactly 2× the payoff of C
2. **Cooperation creates exploitable surplus** - When others cooperate, the stock regenerates, creating more for me to take
3. **Stock depletion is the real cost** - The tragedy isn't mutual defection in one round; it's destroying future extraction potential
4. **Endgame changes everything** - With no future rounds, there's no reason to preserve stock

### Decision Variables

- `stock`: Current resource level
- `capacity`: Maximum sustainable stock
- `n`: Number of players
- `r`: Total rounds
- `t`: Current round (1-indexed)
- `history`: Record of all players' previous actions
- `coop_rate`: Fraction of opponents who cooperated last round

---

## Strategy Specification

### Round-by-Round Decision Rules

```
FUNCTION decide(stock, capacity, n, r, t, history):
    
    rounds_remaining = r - t
    coop_rate = calculate_opponent_cooperation_rate(history, last_k_rounds=3)
    stock_ratio = stock / capacity
    critical_threshold = capacity / (4 * n)  # Below this, resource collapses
    
    # RULE 1: ENDGAME EXPLOITATION
    # In final rounds, always defect - no future to preserve
    IF rounds_remaining <= 1:
        RETURN D
    
    # RULE 2: RESOURCE COLLAPSE EXPLOITATION
    # If stock is critically low, extract what remains before it's gone
    IF stock <= critical_threshold:
        RETURN D
    
    # RULE 3: FIRST ROUND PROBE
    # Start with defection to test opponent responses and gain early advantage
    IF t == 1:
        RETURN D
    
    # RULE 4: EXPLOIT COOPERATORS
    # If most opponents are cooperating, defect to extract maximum value
    # Their cooperation will regenerate stock for continued exploitation
    IF coop_rate >= 0.6:
        RETURN D
    
    # RULE 5: CONDITIONAL COOPERATION FOR SUSTAINABILITY
    # If defection is widespread and stock is declining dangerously,
    # briefly cooperate to prevent total collapse (preserving future extraction)
    IF coop_rate <= 0.3 AND stock_ratio < 0.4 AND rounds_remaining > 3:
        # Only cooperate if it might trigger reciprocity
        # Check if opponents have ever responded to cooperation
        IF opponents_respond_to_cooperation(history):
            RETURN C
        ELSE:
            RETURN D  # Don't waste cooperation on non-reciprocators
    
    # RULE 6: STOCK-ADAPTIVE MIXED EXPLOITATION
    # In middle scenarios, base decision on stock health
    IF stock_ratio >= 0.7:
        # Healthy stock - can afford to defect
        RETURN D
    ELIF stock_ratio >= 0.4:
        # Moderate stock - defect if any cooperators exist to subsidize
        IF coop_rate > 0:
            RETURN D
        ELSE:
            # All defecting, moderate stock - occasional cooperation
            # to prevent collapse, but probabilistically
            IF random() < 0.3:
                RETURN C
            ELSE:
                RETURN D
    ELSE:
        # Low stock - defect to grab remaining value
        RETURN D

FUNCTION opponents_respond_to_cooperation(history):
    # Check if opponent cooperation increased after rounds where I cooperated
    # Returns TRUE if there's evidence of reciprocity
    ...

FUNCTION calculate_opponent_cooperation_rate(history, last_k_rounds):
    # Calculate fraction of opponent actions that were C
    # in the last k rounds (or all history if fewer rounds played)
    ...
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | D | Gain information + immediate payoff advantage |
| **Final round** | D | No future consequences |
| **Second-to-last round** | D | Opponents will defect next round regardless |
| **Stock near zero** | D | Extract remaining value before collapse |
| **Stock at capacity, all cooperating** | D | Maximum exploitation opportunity |
| **Stock declining, all defecting** | Usually D, rare C | Only cooperate if evidence suggests it triggers reciprocity |
| **Single opponent (n=2)** | More aggressive D | Easier to track and exploit patterns |
| **Many opponents (large n)** | Consistent D | Individual cooperation has negligible effect |

---

## Why This Strategy is Exploitative

1. **Never initiates sustained cooperation** - Only cooperates tactically to prevent total resource collapse
2. **Free-rides on cooperators** - Extracts double value whenever others preserve the resource
3. **Front-loads extraction** - Prioritizes immediate gains, recognizing the stock may not last
4. **Endgame ruthless** - No pretense of cooperation when future rounds can't punish defection
5. **Exploits reciprocators** - If opponents use tit-for-tat style strategies, this extracts value in early rounds before they can fully retaliate

## Robustness Features

- **Adaptive to cooperation levels** - Adjusts exploitation intensity based on observed opponent behavior
- **Stock-aware** - Prevents self-destructive over-extraction (but only to preserve future extraction opportunities)
- **No coordination assumptions** - Doesn't rely on others following any particular pattern
- **Degrades gracefully** - Even against all-defectors, minimizes losses while seeking any exploitation opportunity
'''

description_EXPLOITATIVE_2 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of resource depletion are shared across all players. The key insight is that I can free-ride on others' cooperation while extracting maximum value, but I must be adaptive enough to avoid mutual destruction when facing other defectors.

## Strategy Overview

**Adaptive Predator** operates in three modes based on observed opponent behavior and game state:

1. **Exploitation Mode**: Defect aggressively when others cooperate
2. **Sustainable Extraction Mode**: Cooperate strategically when stock is critically low
3. **Endgame Extraction Mode**: Always defect in final rounds

---

## Decision Rules

### Rule 1: Endgame Detection (Highest Priority)
```
IF rounds_remaining ≤ 2:
    DEFECT (no future to preserve)
```

**Rationale**: With no meaningful future rounds, cooperation has zero strategic value. Extract maximum immediate payoff.

### Rule 2: Critical Stock Threshold
```
critical_threshold = capacity / (2 * n)

IF stock < critical_threshold:
    COOPERATE (preserve the resource for future extraction)
```

**Rationale**: If stock is critically low, even defection yields minimal payoff. Better to let it regenerate so I can extract more later. This threshold ensures at least one more round of meaningful extraction.

### Rule 3: Opponent Behavior Classification
```
After each round, calculate:
    cooperation_rate = (total_C_plays_by_others) / (total_plays_by_others)
    recent_cooperation_rate = cooperation in last min(3, rounds_played) rounds
```

### Rule 4: Adaptive Exploitation (Main Logic)
```
IF rounds_played == 0:
    DEFECT (test the waters, maximize first-round gain)

ELSE IF recent_cooperation_rate ≥ 0.6:
    DEFECT (exploit cooperative opponents)

ELSE IF recent_cooperation_rate ≤ 0.3 AND stock > capacity * 0.5:
    DEFECT (stock is healthy enough to absorb mutual defection)

ELSE IF recent_cooperation_rate ≤ 0.3 AND stock ≤ capacity * 0.5:
    # Mixed strategy to occasionally signal willingness to cooperate
    IF (current_round mod 3) == 0:
        COOPERATE (periodic cooperation signal)
    ELSE:
        DEFECT

ELSE:  # Medium cooperation environment (0.3 < rate < 0.6)
    IF stock > capacity * 0.7:
        DEFECT (healthy stock, extract value)
    ELSE:
        # Probabilistic: lean toward defection but occasionally cooperate
        DEFECT with probability 0.7
        COOPERATE with probability 0.3
```

---

## Edge Case Handling

### First Round
- **Action**: DEFECT
- **Rationale**: No information about opponents yet. Defecting provides maximum immediate payoff and reveals opponent tendencies. If others cooperate, I've extracted double. If others defect, I've avoided being the sucker.

### Last Round
- **Action**: DEFECT (unconditionally)
- **Rationale**: No future consequences. Pure extraction.

### Second-to-Last Round
- **Action**: DEFECT (unconditionally)
- **Rationale**: Others who are rational will defect in the last round anyway, so cooperation here provides no leverage.

### Stock at Zero or Near-Zero
- **Action**: COOPERATE
- **Rationale**: Defecting on an empty pool yields nothing. Minimal consumption allows regeneration.

### All Opponents Consistently Defecting
- **Action**: Primarily DEFECT, with occasional COOPERATE
- **Rationale**: Can't be exploited by matching aggression, but periodic cooperation tests if opponents are conditionally cooperative.

---

## Pseudocode Implementation

```
function decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    rounds_remaining = r - current_round + 1
    
    # RULE 1: Endgame - always defect
    if rounds_remaining <= 2:
        return DEFECT
    
    # RULE 2: Critical stock - cooperate to preserve resource
    critical_threshold = capacity / (2 * n)
    if stock < critical_threshold:
        return COOPERATE
    
    # RULE 3: First round - defect to test and maximize
    if current_round == 1:
        return DEFECT
    
    # Calculate opponent cooperation rates
    recent_window = min(3, len(history))
    recent_opponent_actions = get_opponent_actions(history, recent_window)
    recent_coop_rate = count(C in recent_opponent_actions) / len(recent_opponent_actions)
    
    # RULE 4: Adaptive exploitation
    if recent_coop_rate >= 0.6:
        return DEFECT  # Exploit cooperators
    
    if recent_coop_rate <= 0.3:
        if stock > capacity * 0.5:
            return DEFECT  # Can afford mutual defection
        else:
            # Periodic cooperation signal in hostile environment
            if current_round % 3 == 0:
                return COOPERATE
            return DEFECT
    
    # Medium cooperation environment
    if stock > capacity * 0.7:
        return DEFECT
    else:
        # 70% defect, 30% cooperate
        if random() < 0.7:
            return DEFECT
        return COOPERATE
```

---

## Why This Strategy is Exploitative

1. **Defaults to Defection**: In ambiguous situations, defection is preferred
2. **Exploits Cooperators Ruthlessly**: High cooperation rates trigger pure defection
3. **Never Initiates Cooperation**: First move is always defect
4. **Endgame Extraction**: Guaranteed defection when cooperation can't be reciprocated
5. **Self-Preserving**: Only cooperates when stock depletion threatens future extraction opportunities
6. **Asymmetric Response**: Doesn't match cooperation with cooperation—matches it with exploitation

This strategy treats cooperation by others as a resource to be harvested, not a norm to be maintained.
'''

description_EXPLOITATIVE_3 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff while cooperation's benefits (stock preservation) are shared by all. The key insight is that **I can free-ride on others' cooperation while defecting, and I should only cooperate when it's strictly necessary to prevent total collapse that would hurt my future payoffs.**

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Mode** (early rounds): Test opponent cooperation levels
2. **Exploit Mode** (when opponents cooperate): Defect to maximize extraction
3. **Survival Mode** (when stock critically low): Conditionally cooperate to preserve future payoffs

---

## Detailed Decision Rules

### Round 1: Always Defect
- No information about opponents yet
- Defecting gives 2x payoff with zero opportunity cost in terms of reputation
- Sets an aggressive tone that may intimidate conditional cooperators

### Last Round: Always Defect
- No future to preserve
- Pure dominant strategy regardless of stock level
- Any cooperation here is strictly dominated

### Rounds 2 through (r-1): Adaptive Exploitation

**Calculate these metrics each round:**
- `cooperation_rate` = (total C actions by all opponents in all previous rounds) / (total actions by opponents)
- `recent_coop_rate` = cooperation rate in last min(3, rounds_played) rounds
- `stock_ratio` = current_stock / capacity
- `rounds_remaining` = r - current_round
- `critical_threshold` = capacity / (4 * n)  // Below this, stock may not recover

**Decision Logic:**

```
IF stock_ratio < 0.1 AND rounds_remaining > 2:
    // SURVIVAL MODE: Stock critically low
    IF recent_coop_rate > 0.6:
        COOPERATE  // Others are trying to save it, I'll minimally contribute
    ELSE:
        DEFECT  // Grab what's left before it's gone

ELSE IF stock_ratio < 0.25 AND rounds_remaining > 3:
    // CAUTION MODE: Stock concerning
    IF recent_coop_rate > 0.7:
        COOPERATE with probability 0.5  // Partial cooperation to sustain
    ELSE:
        DEFECT  // Others aren't saving it, neither will I

ELSE IF cooperation_rate > 0.8 AND stock_ratio > 0.5:
    // EXPLOIT MODE: Suckers are cooperating, exploit them
    DEFECT  // Maximum extraction while the resource lasts

ELSE IF cooperation_rate > 0.5:
    // MIXED EXPLOITATION: Moderate cooperation in population
    DEFECT with probability 0.8
    COOPERATE with probability 0.2  // Occasional cooperation to not fully crash stock

ELSE:
    // HOSTILE ENVIRONMENT: Others are mostly defecting
    DEFECT  // No point cooperating when others won't
```

### Special Case: Endgame Acceleration

When `rounds_remaining <= 3`:
- Increase defection probability by 20% at each step
- Round r-2: Add 0.2 to defect probability
- Round r-1: Add 0.4 to defect probability  
- Round r: Always defect (as stated above)

### Special Case: Stock Collapse Detection

If stock drops by more than 60% in a single round:
- Next round: DEFECT regardless of other conditions
- Rationale: Others are defecting heavily; cooperating alone is futile

---

## Pseudocode Implementation

```python
def decide(game_params, current_stock, history, current_round):
    n, r, capacity = game_params
    rounds_remaining = r - current_round
    stock_ratio = current_stock / capacity
    
    # Terminal conditions
    if current_round == r:
        return DEFECT
    if current_round == 1:
        return DEFECT
    
    # Calculate opponent behavior metrics
    opponent_actions = get_opponent_actions(history)
    cooperation_rate = count(C in opponent_actions) / len(opponent_actions)
    recent_coop_rate = calc_recent_coop_rate(history, window=3)
    
    # Endgame acceleration
    endgame_bonus = max(0, (3 - rounds_remaining) * 0.2)
    
    # Stock collapse detection
    if len(history) >= 2:
        prev_stock = history[-2].stock
        if (prev_stock - current_stock) / prev_stock > 0.6:
            return DEFECT
    
    # Main decision tree
    if stock_ratio < 0.1 and rounds_remaining > 2:
        if recent_coop_rate > 0.6:
            return COOPERATE
        return DEFECT
    
    if stock_ratio < 0.25 and rounds_remaining > 3:
        if recent_coop_rate > 0.7:
            return random_choice(COOPERATE, 0.5 - endgame_bonus)
        return DEFECT
    
    if cooperation_rate > 0.8 and stock_ratio > 0.5:
        return DEFECT  # Pure exploitation
    
    if cooperation_rate > 0.5:
        return random_choice(DEFECT, 0.8 + endgame_bonus)
    
    return DEFECT  # Default: defect in hostile environments
```

---

## Why This Strategy is Exploitative

1. **Never initiates cooperation** - Always defects first to probe
2. **Free-rides on cooperators** - When others cooperate, it extracts maximum value
3. **Only cooperates selfishly** - Cooperation is purely to preserve future personal extraction, not altruism
4. **Accelerates endgame defection** - Recognizes declining shadow of the future
5. **Punishes cooperative environments** - Paradoxically defects MORE when others cooperate (they're "suckers")
6. **Abandons sinking ships** - Defects when stock collapses rather than trying to save it

This strategy should dominate pure cooperators (by exploitation) and match pure defectors (by mutual defection), while extracting maximum value from mixed populations.
'''

description_EXPLOITATIVE_4 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of resource depletion are shared among all players. The key insight is that in a tournament setting, I can't control whether the resource survives—but I can ensure I extract maximum value relative to my opponents before it collapses.

## Strategy Overview

**Adaptive Predator** operates on three principles:
1. **Extract aggressively early** when stock is high and opponents' strategies are unknown
2. **Monitor and exploit** cooperative opponents by continuing to defect while they sustain the resource
3. **Match defection** when facing defectors to avoid being the sole sucker

---

## Decision Rules

### Round 1: Always Defect
- No history to analyze; stock is at maximum
- Immediate payoff is doubled compared to cooperation
- Reveals nothing exploitable about my strategy (defection is the obvious choice)

### Rounds 2 through (r-1): Adaptive Exploitation

**Calculate the "Cooperation Ratio" of opponents:**
```
opponent_coop_rate = (total opponent C plays) / (total opponent plays so far)
```

**Decision Logic:**

```
IF stock < capacity / (2 * n):
    # Resource critically depleted - defect to grab remaining scraps
    DEFECT

ELSE IF opponent_coop_rate >= 0.7:
    # Opponents are cooperative suckers - exploit them mercilessly
    DEFECT
    
ELSE IF opponent_coop_rate >= 0.4:
    # Mixed environment - probabilistic defection weighted toward exploitation
    # Defect with probability based on remaining rounds and stock health
    defect_probability = 0.6 + (0.3 * (current_round / r))
    DEFECT with probability defect_probability, else COOPERATE
    
ELSE:
    # Hostile environment (mostly defectors)
    # No point being the only cooperator - join the race to the bottom
    DEFECT
```

### Last Round (Round r): Always Defect
- No future consequences; pure dominant strategy
- Even if resource could regenerate, there's no next round to benefit

---

## Edge Case Handling

### Stock Depletion Scenarios

**If stock = 0:**
- DEFECT (payoff is 0 either way, but maintains consistency)

**If stock is very low (< capacity/n):**
- DEFECT (grab what's left before others do)

### Opponent Behavior Patterns

**Detecting "Grim Trigger" opponents:**
- If cooperation rate was high then suddenly dropped to 0 after I defected
- Continue defecting—they won't forgive anyway

**Detecting "Tit-for-Tat" style opponents:**
- Pattern: they defect after majority defected, cooperate after majority cooperated
- Exploit by defecting slightly more than the threshold that triggers their cooperation

**Detecting unconditional cooperators:**
- Cooperation rate stays >90% regardless of my actions
- Maximum exploitation: always defect

**Detecting unconditional defectors:**
- Join them immediately; cooperation only wastes my payoff

---

## Pseudocode Implementation

```
function decide(game_state, history):
    n = game_state.num_players
    r = game_state.total_rounds
    current_round = game_state.current_round
    stock = game_state.current_stock
    capacity = game_state.capacity
    
    # Last round - always defect
    if current_round == r:
        return DEFECT
    
    # First round - always defect
    if current_round == 1:
        return DEFECT
    
    # Critical stock threshold
    if stock < capacity / (2 * n):
        return DEFECT
    
    # Calculate opponent cooperation rate
    opponent_coops = count_opponent_cooperations(history)
    opponent_total = count_opponent_actions(history)
    coop_rate = opponent_coops / opponent_total
    
    # Exploitation logic
    if coop_rate >= 0.7:
        return DEFECT
    
    if coop_rate >= 0.4:
        defect_prob = 0.6 + (0.3 * current_round / r)
        return DEFECT if random() < defect_prob else COOPERATE
    
    # Hostile environment
    return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Never unconditionally cooperates** - Cooperation only occurs probabilistically in mixed environments, and only to potentially slow resource collapse when it benefits me

2. **Maximizes extraction from cooperators** - When opponents cooperate, I take double their share while they maintain the resource for me

3. **Avoids sucker payoffs** - Never cooperates when facing defectors

4. **End-game ruthlessness** - Defection probability increases as game progresses, culminating in guaranteed defection on the final round

5. **Threshold exploitation** - The 0.7 cooperation threshold means I defect against any group that's even slightly cooperative, extracting maximum value from their restraint
'''

description_EXPLOITATIVE_5 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of resource depletion are shared across all players. The key insight is that **others' cooperation creates exploitable surplus**, while widespread defection signals imminent collapse requiring tactical adjustment.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Mode** (Early rounds): Test opponent responses
2. **Exploit Mode** (Mid-game): Maximize extraction from cooperative opponents
3. **Endgame Mode** (Final rounds): Pure defection

---

## Detailed Decision Rules

### Round Classification

```
early_phase = round ≤ max(2, r/5)
endgame_phase = round > r - max(2, r/5)
mid_phase = everything else
```

### Key Metrics to Track

```
cooperation_rate = (total C plays by opponents) / (total opponent actions so far)
last_round_coop_rate = (C plays by opponents last round) / (n - 1)
stock_health = current_stock / capacity
rounds_remaining = r - current_round
```

---

## Decision Rules by Phase

### 1. First Round
**Action: DEFECT**

Rationale: No information exists. Defecting tests whether opponents are unconditional cooperators (exploitable) while guaranteeing maximum first-round payoff. The stock can recover if others cooperate.

### 2. Early Phase (rounds 2 to ~r/5)

```
IF last_round_coop_rate ≥ 0.7:
    # Opponents are cooperative - exploit them
    DEFECT
    
ELSE IF last_round_coop_rate ≥ 0.4 AND stock_health > 0.5:
    # Mixed environment with healthy stock - continue probing via defection
    DEFECT
    
ELSE IF stock_health < 0.3:
    # Stock critically low early - one round of cooperation to avoid collapse
    # (only if it serves long-term exploitation)
    IF rounds_remaining > 3:
        COOPERATE
    ELSE:
        DEFECT
        
ELSE:
    # Low cooperation environment - defect to match
    DEFECT
```

### 3. Mid-Game Phase

```
# Calculate exploitation opportunity
exploitation_value = cooperation_rate * stock_health * rounds_remaining

IF cooperation_rate ≥ 0.6 AND stock_health > 0.4:
    # Golden opportunity: cooperative opponents with healthy stock
    DEFECT (exploit the cooperators)
    
ELSE IF cooperation_rate ≥ 0.6 AND stock_health ≤ 0.4:
    # Cooperators exist but stock is low
    # Strategic cooperation to rebuild stock for future exploitation
    IF stock_health < 0.2 AND rounds_remaining > 2:
        COOPERATE (invest in future extraction)
    ELSE:
        DEFECT
        
ELSE IF cooperation_rate < 0.4:
    # Mostly defectors - no point cooperating, join them
    DEFECT
    
ELSE:
    # Mixed environment (0.4 ≤ cooperation_rate < 0.6)
    IF stock_health > 0.5:
        DEFECT (extract while stock lasts)
    ELSE IF stock_health > 0.25 AND rounds_remaining > 3:
        # Probabilistic: mostly defect but occasional cooperation
        DEFECT with 80% probability, COOPERATE with 20%
    ELSE:
        DEFECT
```

### 4. Endgame Phase (final ~r/5 rounds)

```
IF rounds_remaining == 1:
    # Absolute last round - no future consequences
    DEFECT (always)
    
ELSE IF rounds_remaining == 2:
    # Penultimate round
    IF stock_health > 0.3:
        DEFECT (extract maximum)
    ELSE:
        DEFECT (nothing to save anyway)
        
ELSE:
    # Late game but not final rounds
    DEFECT (no time for cooperation to pay off)
```

### 5. Edge Case: Near-Zero Stock

```
IF stock < capacity / (4 * n):
    # Stock is essentially depleted
    # Cooperation vs defection barely matters for absolute payoff
    # But defection still gets double the tiny amount
    DEFECT
```

---

## Pseudocode Summary

```python
def decide(round, total_rounds, n, capacity, current_stock, history):
    
    rounds_remaining = total_rounds - round
    stock_health = current_stock / capacity
    
    # Calculate opponent cooperation metrics
    if round == 1:
        cooperation_rate = 0.5  # assume neutral
        last_round_coop_rate = 0.5
    else:
        cooperation_rate = count_opponent_cooperations(history) / total_opponent_actions(history)
        last_round_coop_rate = count_opponent_cooperations_last_round(history) / (n - 1)
    
    # Phase boundaries
    early_cutoff = max(2, total_rounds // 5)
    endgame_cutoff = total_rounds - max(2, total_rounds // 5)
    
    # FIRST ROUND
    if round == 1:
        return DEFECT
    
    # ENDGAME - always defect
    if round > endgame_cutoff:
        return DEFECT
    
    # EARLY PHASE - probe and exploit
    if round <= early_cutoff:
        if stock_health < 0.3 and rounds_remaining > 3:
            return COOPERATE  # emergency preservation
        return DEFECT  # default to exploitation
    
    # MID GAME - adaptive exploitation
    if cooperation_rate >= 0.6:
        if stock_health > 0.4:
            return DEFECT  # exploit cooperators
        elif stock_health < 0.2 and rounds_remaining > 2:
            return COOPERATE  # rebuild for later extraction
        else:
            return DEFECT
    
    elif cooperation_rate < 0.4:
        return DEFECT  # match defectors
    
    else:  # mixed environment
        if stock_health < 0.2 and rounds_remaining > 3:
            return COOPERATE  # emergency preservation
        return DEFECT  # default exploitation
```

---

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: Consistently takes double shares when others cooperate
2. **Free-riding on preservation**: Only cooperates when stock collapse threatens future exploitation opportunities
3. **No reciprocity**: Never rewards cooperation with cooperation; treats cooperators as resources
4. **Endgame dominance**: Guaranteed defection in final rounds extracts maximum value
5. **Adaptive parasitism**: Adjusts to find the optimal extraction rate that opponents will sustain

## Robustness Features

- **Against all-cooperators**: Maximum exploitation throughout
- **Against all-defectors**: Matches defection, doesn't lose relative standing
- **Against tit-for-tat**: Extracts early value, accepts mutual defection
- **Against mixed strategies**: Exploits any cooperation while preserving stock only when necessary for self-interest
'''

description_EXPLOITATIVE_6 = '''
# Exploitative Strategy for Common Pool Resource Game

## Core Philosophy

This strategy is designed to maximize personal extraction while exploiting cooperative opponents. The key insight is that defection yields exactly double the payoff of cooperation in any given round, but depletes the resource faster. The optimal exploitative approach is to **free-ride on cooperators when they exist, and defect aggressively when the resource is doomed anyway**.

## Strategy: "Predatory Opportunist"

### Decision Framework

The strategy operates on three key principles:
1. **Exploit cooperation ruthlessly** - If others cooperate, defect to extract double while they sustain the resource
2. **Abandon ship early** - Once resource collapse is inevitable, defect to maximize extraction from remaining stock
3. **Conditional cooperation only for self-interest** - Cooperate only when it's necessary to keep the resource alive for future exploitation

### Decision Rules

```
EACH ROUND:
    Calculate sustainability_threshold = capacity / (2 * n)
    Calculate rounds_remaining = r - current_round
    Calculate cooperation_rate = (cooperators in last round) / n  [0 if first round]
    
    IF last_round:
        DEFECT  # No future value to preserve
    
    ELSE IF stock < sustainability_threshold:
        DEFECT  # Resource is collapsing anyway, extract what's left
    
    ELSE IF rounds_remaining <= 2:
        DEFECT  # End-game defection, not enough future to justify cooperation
    
    ELSE IF first_round:
        DEFECT  # Test the waters, extract maximum, observe responses
    
    ELSE IF cooperation_rate >= 0.5:
        DEFECT  # Exploit the cooperators - they're sustaining the resource for us
    
    ELSE IF cooperation_rate > 0 AND stock > capacity * 0.6:
        DEFECT  # Still enough buffer to exploit remaining cooperators
    
    ELSE IF stock > capacity * 0.4 AND rounds_remaining > 3:
        COOPERATE  # Invest minimally to keep resource viable for future defection
    
    ELSE:
        DEFECT  # Default to extraction
```

### Detailed Edge Case Handling

**First Round:**
- Always DEFECT
- Rationale: Establishes dominance, tests opponent responses, extracts maximum from full stock
- If others cooperate, we've exploited them; if they defect too, no loss from mutual defection

**Last Round:**
- Always DEFECT
- Rationale: No future rounds means no value in preservation; pure extraction game

**Second-to-Last Round:**
- Always DEFECT
- Rationale: Even if we cooperate, opponents will likely defect in the final round; no benefit to cooperation

**Low Stock (below capacity/2n):**
- Always DEFECT
- Rationale: Resource cannot recover meaningfully; extract remaining value

**High Cooperation Environment (≥50% cooperators):**
- Always DEFECT
- Rationale: Free-ride on their sustainability efforts while extracting double

**Mixed Environment with Healthy Stock:**
- Conditionally cooperate ONLY if stock is in danger zone (40-60% of capacity) and we need it to survive for future extraction

### Exploitation Mechanisms

1. **First-Mover Exploitation**: Defecting early when stock is high yields maximum absolute payoff (stock/n when stock is near capacity)

2. **Cooperation Exploitation**: When others cooperate, they take stock/(2n) while we take stock/n - we get exactly double their payoff while they bear the sustainability cost

3. **End-Game Extraction**: The final 2-3 rounds are pure defection regardless of history - no point preserving what can't benefit us

4. **Threshold Manipulation**: By defecting when stock is healthy but cooperating only when collapse threatens, we extract maximum while letting others do the conservation work

### Why This Beats Common Strategies

- **Against Always-Cooperate**: We extract double every round, devastating them
- **Against Tit-for-Tat**: We get the first-round advantage, and end-game advantage
- **Against Always-Defect**: We match them (no exploitation either way)
- **Against Conditional Cooperators**: We trigger their cooperation by occasional cooperation, then exploit it

This strategy is fundamentally parasitic - it succeeds by extracting value others create through their cooperation, while contributing minimally to sustainability.
'''

description_EXPLOITATIVE_7 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, while the costs of resource depletion are shared equally among all players. The key insight is that in a multi-player setting, I can free-ride on others' cooperation while they bear most of the sustainability cost.

## Decision Rules

### Primary Decision Framework

**Defect by default, cooperate only when resource collapse is imminent and I need others to sustain the pool for my future exploitation.**

### Detailed Rules

#### Rule 1: Last Round Detection
```
IF current_round == r (final round):
    DEFECT (no future to protect)
```

#### Rule 2: Resource Criticality Check
```
critical_threshold = capacity / (4 * n)

IF stock < critical_threshold:
    # Resource near collapse - temporary cooperation to rebuild
    # But only if there's enough game left to benefit
    IF rounds_remaining > 3:
        COOPERATE
    ELSE:
        DEFECT (not enough time to benefit from regrowth)
```

#### Rule 3: Cooperation Ratio Exploitation
```
IF round > 1:
    opponent_cooperation_rate = (total_C_played_by_others) / (total_actions_by_others)
    
    IF opponent_cooperation_rate > 0.6:
        # Opponents are sustaining the resource - exploit them
        DEFECT
    
    ELIF opponent_cooperation_rate < 0.3:
        # Everyone defecting - race to extract before collapse
        DEFECT
    
    ELSE:
        # Mixed behavior - use stock level to decide
        IF stock > capacity * 0.5:
            DEFECT (plenty to take)
        ELSE:
            # Probabilistic cooperation based on remaining rounds
            cooperation_probability = rounds_remaining / (2 * r)
            COOPERATE with probability cooperation_probability
            DEFECT otherwise
```

#### Rule 4: First Round
```
IF round == 1:
    DEFECT
    # Rationale: Establish high extraction, test opponent responses,
    # maximum payoff when stock is at capacity
```

#### Rule 5: Endgame Acceleration
```
IF rounds_remaining <= max(3, r/5):
    # Approaching endgame - increase defection
    DEFECT
    # Others may cooperate hoping to sustain; exploit this
```

## Complete Decision Algorithm (Pseudocode)

```
function decide(n, r, capacity, stock, current_round, history):
    rounds_remaining = r - current_round + 1
    critical_threshold = capacity / (4 * n)
    
    # Priority 1: Last round - always defect
    if current_round == r:
        return DEFECT
    
    # Priority 2: Endgame phase (last 20% or last 3 rounds)
    if rounds_remaining <= max(3, r / 5):
        return DEFECT
    
    # Priority 3: First round - defect to test and maximize
    if current_round == 1:
        return DEFECT
    
    # Priority 4: Resource critical - conditional cooperation
    if stock < critical_threshold:
        if rounds_remaining > 3:
            return COOPERATE
        else:
            return DEFECT
    
    # Priority 5: Exploit cooperative opponents
    opponent_coop_rate = calculate_opponent_cooperation_rate(history)
    
    if opponent_coop_rate > 0.6:
        return DEFECT  # Free ride on cooperators
    
    if opponent_coop_rate < 0.3:
        return DEFECT  # Race to bottom, grab what's left
    
    # Priority 6: Mixed opponent behavior - stock-based decision
    if stock > capacity * 0.5:
        return DEFECT
    else:
        # Occasional cooperation to prevent total collapse
        coop_prob = rounds_remaining / (2 * r)
        return COOPERATE with probability coop_prob, else DEFECT
```

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1 | DEFECT | Maximum extraction at peak stock; establishes aggressive stance |
| Final round | DEFECT | No future consequences |
| Stock near zero, many rounds left | COOPERATE | Need resource to regenerate for future extraction |
| Stock near zero, few rounds left | DEFECT | Can't recover enough to matter |
| All opponents cooperating | DEFECT | Maximum exploitation opportunity |
| All opponents defecting | DEFECT | Competing for remaining scraps |
| r = 2 (two rounds only) | DEFECT both | Too short to benefit from cooperation |

## Why This Strategy is Exploitative

1. **Asymmetric burden**: When I defect among cooperators, I get 2x their payoff while they subsidize resource sustainability
2. **Information exploitation**: I observe opponent patterns and adjust to maximize extraction
3. **Temporal exploitation**: Cooperation only when absolutely necessary to prevent collapse that would hurt *my* future payoffs
4. **Endgame exploitation**: Others may cooperate hoping for reciprocity; I take advantage in final rounds
'''

description_EXPLOITATIVE_8 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators per round. The key insight is that cooperation only makes sense if it preserves enough stock for future exploitation. I will defect aggressively while monitoring whether the pool can sustain my extraction, and exploit cooperative opponents by free-riding on their restraint.

## Decision Rules

### Primary Decision Framework

**Defect by default, cooperate only when necessary for self-preservation.**

The strategy tracks two key metrics:
1. **Cooperation ratio of opponents**: What fraction of opponent actions were C in recent rounds?
2. **Stock sustainability threshold**: Can the pool survive another round of my defection?

### Detailed Rules

```
FUNCTION decide(game_params, current_stock, history):
    n = number of players
    r = total rounds
    current_round = length(history) + 1
    rounds_remaining = r - current_round + 1
    
    # RULE 1: Last Round - Always Defect
    IF rounds_remaining == 1:
        RETURN D
    
    # RULE 2: First Round - Defect to Probe
    IF current_round == 1:
        RETURN D
    
    # RULE 3: Critical Stock Check
    # If stock is dangerously low, cooperate to avoid total collapse
    # (only if there's enough future value to justify it)
    min_viable_stock = capacity * 0.1
    IF current_stock < min_viable_stock AND rounds_remaining > 2:
        RETURN C
    
    # RULE 4: Exploit Cooperative Environments
    opponent_coop_rate = calculate_recent_cooperation_rate(history, window=3)
    
    # If opponents are mostly cooperating, defect to exploit them
    IF opponent_coop_rate > 0.6:
        RETURN D
    
    # RULE 5: Endgame Defection
    # In final rounds, defect regardless (diminishing future value)
    IF rounds_remaining <= max(2, r / 5):
        RETURN D
    
    # RULE 6: Stock Trajectory Analysis
    stock_trend = calculate_stock_trend(history)
    
    # If stock is growing or stable despite defection, keep defecting
    IF stock_trend >= -0.1 * capacity:
        RETURN D
    
    # RULE 7: Strategic Temporary Cooperation
    # If stock is declining rapidly and we need future rounds,
    # cooperate briefly to let it recover (then resume exploitation)
    IF stock_trend < -0.2 * capacity AND rounds_remaining > 3:
        # Cooperate for 1-2 rounds to stabilize, then defect
        recent_my_actions = get_my_recent_actions(history, window=2)
        IF count(recent_my_actions, C) < 1:
            RETURN C
    
    # DEFAULT: Defect
    RETURN D
```

### Helper Functions

```
FUNCTION calculate_recent_cooperation_rate(history, window):
    # Look at last 'window' rounds, count opponent C actions
    recent_rounds = history[-window:]
    total_opponent_actions = 0
    cooperative_actions = 0
    FOR each round in recent_rounds:
        FOR each opponent_action in round.opponent_actions:
            total_opponent_actions += 1
            IF opponent_action == C:
                cooperative_actions += 1
    IF total_opponent_actions == 0:
        RETURN 0.5  # neutral assumption
    RETURN cooperative_actions / total_opponent_actions

FUNCTION calculate_stock_trend(history):
    # Compare recent stock levels to detect trajectory
    IF length(history) < 2:
        RETURN 0
    recent_stocks = [round.stock_after for round in history[-3:]]
    RETURN (recent_stocks[-1] - recent_stocks[0]) / length(recent_stocks)
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | D | Probe opponent behavior; maximize immediate gain |
| **Last round** | D | No future to preserve; pure extraction |
| **Last 2-3 rounds** | D | Discount future value heavily |
| **Stock near zero** | C (if >2 rounds left) | Prevent total collapse that hurts my future payoffs |
| **Stock near zero + last 2 rounds** | D | Not enough future to justify restraint |
| **All opponents defecting** | D | No benefit to unilateral cooperation |
| **All opponents cooperating** | D | Maximum exploitation opportunity |
| **Stock stable/growing** | D | Environment tolerates extraction |

## Why This Strategy is Exploitative

1. **Free-riding on cooperators**: When others cooperate, I take double their share while benefiting from their stock preservation.

2. **No reciprocity**: I never reward cooperation with cooperation—I exploit it.

3. **Self-interested preservation only**: I cooperate only when MY future payoffs require stock survival, not for collective benefit.

4. **Endgame aggression**: Heavy defection in final rounds when future value diminishes.

5. **Probe-then-exploit**: Starting with defection reveals opponent tendencies without sacrificing position.

This strategy maximizes personal extraction while avoiding the trap of depleting the resource so badly that my own future earnings suffer.
'''

description_EXPLOITATIVE_9 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Drain"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate 2x payoff over cooperation, while the cost of resource depletion is shared among all players. The key insight is that **I can extract more value by defecting when the stock is high and others are likely cooperating, while appearing to cooperate just enough to encourage others to maintain the resource for me to exploit.**

## Strategy Overview

The strategy operates in three phases based on game progression, with adaptive responses to opponent behavior.

---

## Decision Rules

### Phase 1: Early Exploitation (Rounds 1 to r/3)

**Default: DEFECT**

Rationale: 
- Stock is at or near capacity, maximizing defection payoffs
- Early defection extracts maximum value before depletion
- Establishes a "tough" reputation that may induce fearful cooperation from others
- Even if others defect too, I'm not leaving money on the table

**Exception:** If stock falls below `capacity/2` before this phase ends, transition to Phase 2 behavior.

### Phase 2: Conditional Cooperation (Rounds r/3 to 2r/3)

**Decision Rule:**
```
Let d_prev = number of defectors in previous round (estimated from stock change)
Let threshold = n/2

IF stock < capacity/4:
    DEFECT  # Resource is doomed anyway, extract what remains
ELSE IF d_prev >= threshold:
    DEFECT  # Match aggression - don't be a sucker
ELSE IF d_prev < threshold AND stock > capacity/2:
    COOPERATE with probability 0.3, DEFECT with probability 0.7
ELSE:
    DEFECT  # Default to exploitation
```

Rationale:
- Probabilistic cooperation maintains some resource sustainability
- Heavy defection bias ensures I'm rarely the sucker
- Responsive to group behavior but biased toward extraction

### Phase 3: End-Game Extraction (Final r/3 rounds)

**Default: DEFECT**

**Intensification:** In the final 2 rounds, **ALWAYS DEFECT** regardless of any other consideration.

Rationale:
- Backward induction: no future rounds means no reason to maintain resource
- Others reasoning similarly creates defection cascade
- Being first/aggressive in defection captures remaining value

---

## Edge Case Handling

### First Round
**DEFECT** - Maximum stock means maximum defection payoff. No history to leverage, so take the guaranteed higher payout.

### Last Round
**DEFECT** - No future consequences. Pure dominant strategy.

### Second-to-Last Round
**DEFECT** - Anticipate universal defection in final round; begin extraction early.

### Stock Near Zero (stock < capacity/(2n))
**DEFECT** - Resource is effectively exhausted. Extract whatever remains rather than letting others take it.

### Stock at Capacity After Prior Round
**DEFECT** - Others cooperated heavily; exploit their restraint immediately.

---

## Opponent Behavior Detection

**Estimating defection rate from stock dynamics:**
```
expected_stock_if_all_C = previous_stock - (previous_stock/2) + growth
actual_stock = observed new stock

IF actual_stock << expected_stock_if_all_C:
    infer high defection rate
    respond with DEFECT
```

**Pattern Recognition:**
- If stock has remained stable (near capacity) for 2+ rounds: others are cooperating → **DEFECT to exploit**
- If stock declining rapidly: others are defecting → **DEFECT to not be exploited**

---

## Pseudocode Summary

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Always defect in final 2 rounds
    if round >= total_rounds - 1:
        return DEFECT
    
    # Always defect in round 1
    if round == 1:
        return DEFECT
    
    # Defect if resource is nearly exhausted
    if stock < capacity / (2 * n):
        return DEFECT
    
    # Phase 1: Early game exploitation
    if round <= total_rounds / 3:
        if stock < capacity / 2:
            # Resource depleting fast, transition to adaptive
            pass
        else:
            return DEFECT
    
    # Phase 3: Late game extraction
    if round > 2 * total_rounds / 3:
        return DEFECT
    
    # Phase 2: Conditional (but biased toward defection)
    estimated_defectors = estimate_defectors(history, n)
    
    if stock < capacity / 4:
        return DEFECT
    if estimated_defectors >= n / 2:
        return DEFECT
    if stock > capacity / 2:
        return DEFECT with probability 0.7, else COOPERATE
    
    return DEFECT  # Default
```

---

## Why This Strategy is Exploitative

1. **Never a sucker**: Defects whenever others defect
2. **Exploits cooperators**: Defects when stock is high (indicating cooperation)
3. **Front-loads extraction**: Takes high payoffs early when stock is abundant
4. **End-game dominant**: Guaranteed defection when cooperation has no future value
5. **Asymmetric response**: Cooperates rarely and only strategically, defects by default
'''

description_EXPLOITATIVE_10 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in this game: defection yields twice the immediate payoff of cooperation, while the cost of resource depletion is shared among all players. The key insight is that in a tournament setting, I should extract maximum value while the resource exists, especially when others are cooperating (free-riding on their restraint), but avoid being the one left with nothing when the pool collapses.

## Strategy Overview

**Adaptive Predator** operates on three principles:
1. **Exploit cooperators ruthlessly** - When others show restraint, take more
2. **Protect against collapse** - Only cooperate when defection would destroy future value
3. **End-game extraction** - Defect in final rounds regardless of state

---

## Decision Rules

### Round-by-Round Logic

```
FUNCTION decide_action(round, total_rounds, stock, capacity, n, history):
    
    # RULE 1: End-game defection
    # In the final 2 rounds, always defect - no future to protect
    IF round >= total_rounds - 1:
        RETURN DEFECT
    
    # RULE 2: Collapse threshold check
    # Calculate stock after universal defection
    stock_after_all_defect = 0  # Everyone takes stock/n, total = stock
    
    # Calculate minimum viable stock for meaningful future payoffs
    # If stock is critically low, cooperate to allow regeneration
    critical_threshold = capacity * 0.15
    
    IF stock < critical_threshold AND round < total_rounds - 2:
        RETURN COOPERATE  # Allow regeneration to harvest later
    
    # RULE 3: First round - establish baseline, test the waters
    IF round == 1:
        RETURN DEFECT  # Take the guaranteed higher payoff
    
    # RULE 4: Analyze opponent behavior from history
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    recent_cooperation_rate = calculate_recent_cooperation_rate(history, last_3_rounds)
    
    # RULE 5: Exploit cooperative environments
    # If others are mostly cooperating, defect to free-ride
    IF cooperation_rate > 0.6:
        RETURN DEFECT
    
    # RULE 6: Respond to defection-heavy environments
    # If everyone is defecting, stock will crash anyway
    # Defect to get your share before it's gone
    IF cooperation_rate < 0.3:
        RETURN DEFECT
    
    # RULE 7: Mixed environment - use stock-based heuristic
    # In middle scenarios, base decision on whether stock can sustain extraction
    
    remaining_rounds = total_rounds - round
    projected_value_if_cooperate = estimate_future_value(stock, remaining_rounds, n, capacity, COOPERATE)
    projected_value_if_defect = estimate_future_value(stock, remaining_rounds, n, capacity, DEFECT)
    
    # Defect if immediate gain + future value exceeds cooperation path
    immediate_defect_bonus = stock / (2 * n)  # Extra from defecting vs cooperating
    
    IF immediate_defect_bonus > projected_value_if_cooperate - projected_value_if_defect:
        RETURN DEFECT
    ELSE:
        RETURN COOPERATE
```

### Helper Functions

```
FUNCTION calculate_opponent_cooperation_rate(history):
    total_opponent_actions = count all opponent actions in history
    cooperative_actions = count opponent C actions
    RETURN cooperative_actions / total_opponent_actions (or 0.5 if no history)

FUNCTION calculate_recent_cooperation_rate(history, window):
    # Same as above but only for last 'window' rounds
    # Gives more weight to recent behavior trends

FUNCTION estimate_future_value(current_stock, rounds_left, n, capacity, my_action):
    # Simple simulation assuming mixed opponent behavior
    # Returns rough expected cumulative payoff
    
    simulated_stock = current_stock
    total_value = 0
    assumed_defection_rate = 0.5  # Conservative assumption
    
    FOR each remaining round:
        my_consumption = simulated_stock/n if DEFECT else simulated_stock/(2n)
        total_value += my_consumption
        
        # Estimate total consumption
        others_consumption = (n-1) * simulated_stock * (0.5/n + 0.5/(2n))
        total_consumption = my_consumption + others_consumption
        
        simulated_stock = simulated_stock - total_consumption
        growth = 2 * simulated_stock * (1 - simulated_stock/capacity)
        simulated_stock = min(simulated_stock + growth, capacity)
    
    RETURN total_value
```

---

## Edge Cases

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| **Round 1** | DEFECT | No information, take guaranteed higher payoff |
| **Last round** | DEFECT | No future to protect |
| **Second-to-last round** | DEFECT | Regeneration won't matter |
| **Stock near zero** (< 15% capacity) | COOPERATE | Allow regeneration for future extraction |
| **Stock at zero** | DEFECT | Nothing to lose, take whatever exists |
| **All opponents cooperated last round** | DEFECT | Exploit their restraint |
| **All opponents defected last round** | DEFECT | Race to extract before collapse |
| **n = 2 (two players)** | Bias toward DEFECT | Less dilution of blame for collapse |
| **Large n** | Slightly more DEFECT | Individual impact on stock is smaller |

---

## Why This Strategy is Exploitative

1. **Free-rides on cooperators**: When others show restraint, we take double their consumption
2. **Avoids being the sucker**: Never cooperates when others are defecting
3. **Prioritizes extraction over sustainability**: Only cooperates to preserve future extraction opportunities, not out of fairness
4. **End-game aggression**: Guarantees maximum take in final rounds when cooperation has no strategic value
5. **First-mover advantage**: Opens with defection to signal strength and capture immediate gains

---

## Robustness Features

- **Adaptive to opponent mix**: Adjusts based on observed cooperation rates
- **Stock-aware**: Protects against total collapse (which hurts everyone including us)
- **Parameter-responsive**: Works across different n, r, and capacity values
- **No coordination required**: Doesn't assume others will reciprocate or follow patterns
'''

description_EXPLOITATIVE_11 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy is designed to maximize personal extraction by exploiting cooperative opponents while protecting against mutual destruction. The key insight is that cooperators create surplus value through sustainable harvesting, and a smart defector can parasitize this value—but only if enough cooperation exists to maintain the resource.

## Strategy Overview

The strategy operates in three modes based on observed opponent behavior and resource state:

1. **Exploitation Mode**: Defect when others are cooperating enough to sustain the resource
2. **Survival Mode**: Cooperate minimally when the resource is critically endangered
3. **Endgame Mode**: Defect unconditionally in final rounds

---

## Decision Rules

### Rule 1: Endgame Defection
**If remaining rounds ≤ 2: DEFECT**

Rationale: With insufficient time for resource recovery to matter, pure extraction dominates. Even if others defect too, there's no future to protect.

### Rule 2: Resource Crisis Response
**If stock < capacity × 0.25: COOPERATE**

Rationale: When the resource is critically depleted, even a selfish player benefits from allowing recovery. A dead resource yields nothing. This is self-interested conservation, not altruism.

### Rule 3: First Round Probe
**Round 1: DEFECT**

Rationale: Establish an aggressive posture, collect information about opponent responses, and capture immediate high payoff from full stock. This also identifies which opponents are unconditional cooperators (easy targets).

### Rule 4: Adaptive Exploitation (Main Logic)

Calculate the **cooperation ratio** from the previous round:
```
coop_ratio = (number of opponents who played C) / (n - 1)
```

Calculate the **sustainability threshold**:
```
sustainable_defectors = floor(n / 3)
# Approximately how many defectors the system can tolerate while maintaining stock
```

**Decision Logic:**
```
If coop_ratio ≥ 0.6:
    DEFECT  # Enough cooperators to sustain my exploitation
    
Else if coop_ratio ≥ 0.4 AND stock ≥ capacity × 0.5:
    DEFECT  # Resource buffer allows continued exploitation
    
Else if coop_ratio < 0.4 AND stock < capacity × 0.5:
    COOPERATE  # Too many defectors, resource endangered
    
Else:
    # Probabilistic defection based on conditions
    defect_probability = min(0.8, coop_ratio + (stock / capacity) × 0.3)
    DEFECT with probability defect_probability, else COOPERATE
```

### Rule 5: Trend Detection
Track stock trajectory over last 3 rounds:
```
If stock is declining for 3+ consecutive rounds AND stock < capacity × 0.6:
    Override to COOPERATE (regardless of Rule 4)
```

This prevents riding the resource into collapse when the trend is clearly unsustainable.

---

## Complete Pseudocode

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Endgame: pure extraction
    if round > total_rounds - 2:
        return DEFECT
    
    # Resource crisis: survival mode
    if stock < capacity * 0.25:
        return COOPERATE
    
    # First round: probe and establish dominance
    if round == 1:
        return DEFECT
    
    # Calculate opponent cooperation from last round
    opponents_last_round = history[round - 1].opponent_actions
    coop_ratio = count(C in opponents_last_round) / (n - 1)
    
    # Check for dangerous decline trend
    if round >= 4:
        recent_stocks = [history[round-3].stock, history[round-2].stock, history[round-1].stock, stock]
        if all(recent_stocks[i] > recent_stocks[i+1] for i in range(3)):
            if stock < capacity * 0.6:
                return COOPERATE
    
    # Main exploitation logic
    if coop_ratio >= 0.6:
        return DEFECT
    
    if coop_ratio >= 0.4 and stock >= capacity * 0.5:
        return DEFECT
    
    if coop_ratio < 0.4 and stock < capacity * 0.5:
        return COOPERATE
    
    # Probabilistic zone
    defect_prob = min(0.8, coop_ratio + (stock / capacity) * 0.3)
    return DEFECT with probability defect_prob, else COOPERATE
```

---

## Why This Strategy is Exploitative

1. **Free-rides on cooperators**: When others sustain the resource, we extract double
2. **Only cooperates for self-preservation**: Never cooperates out of fairness—only when extraction would be self-defeating
3. **First-mover exploitation**: Opens with defection to capture maximum initial value
4. **Endgame extraction**: Takes everything when future doesn't matter
5. **Targets the cooperative**: The more cooperative the opponents, the more aggressively we defect

This strategy treats cooperators as renewable resources to be harvested, while maintaining just enough restraint to avoid killing the golden goose.
'''

description_EXPLOITATIVE_12 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff while cooperation's benefits (resource preservation) are shared by all. The key insight is that in a tournament setting, I cannot rely on others to preserve the resource, so I must extract maximum value while the resource exists, while being smart enough to avoid killing the resource too quickly when cooperation is detectable.

## Strategy Overview

**Adaptive Predator** operates in three modes based on observed opponent behavior and game state:

1. **Exploitation Mode** (default): Defect to maximize extraction
2. **Tactical Cooperation Mode**: Cooperate only when it's clearly in self-interest
3. **Endgame Pillage Mode**: Always defect in final rounds

---

## Detailed Decision Rules

### Round 1: Probe with Defection
- **Action: DEFECT**
- Rationale: No history exists to exploit. Defection provides maximum immediate payoff and reveals nothing strategically valuable to opponents (since they can't condition on my specific action in simultaneous play).

### Last Round (round = r): Always Defect
- **Action: DEFECT**
- Rationale: No future exists to preserve resources for. This is the dominant strategy regardless of opponent behavior.

### Second-to-Last Round (round = r-1): Always Defect
- **Action: DEFECT**
- Rationale: Sophisticated opponents will defect in the last round, so there's no cooperation to protect. Begin endgame extraction.

### Middle Rounds (2 ≤ round ≤ r-2):

```
Calculate cooperation_rate = (total C plays by all opponents) / (total plays by all opponents)
Calculate stock_ratio = current_stock / capacity
Calculate rounds_remaining = r - current_round

IF rounds_remaining ≤ 2:
    DEFECT  # Endgame pillage

ELSE IF stock_ratio < 0.15:
    DEFECT  # Resource nearly depleted, extract what remains

ELSE IF cooperation_rate ≥ 0.8 AND stock_ratio > 0.5:
    # Opponents are cooperative suckers - exploit them
    DEFECT  # Free-ride on their conservation efforts

ELSE IF cooperation_rate ≥ 0.6 AND stock_ratio > 0.3:
    # Mixed environment - tactical cooperation
    # Cooperate just enough to keep resource alive for future exploitation
    IF previous_round_had_majority_cooperation:
        COOPERATE  # Maintain the cooperative environment to exploit
    ELSE:
        DEFECT  # Others already defecting, join them

ELSE IF cooperation_rate < 0.4:
    DEFECT  # Low cooperation environment, extract before others deplete it

ELSE:
    # Uncertain environment - use stock-based decision
    IF stock_ratio > 0.6:
        DEFECT  # Plenty of resource, safe to exploit
    ELSE:
        COOPERATE  # Need to preserve some resource for future rounds
```

---

## Key Exploitation Mechanisms

### 1. **Sucker Exploitation**
When cooperation rate is high (≥80%), I defect to free-ride. Cooperative players preserve the resource while I extract double shares.

### 2. **Dying Resource Extraction**
When stock falls below 15% of capacity, cooperation cannot save it. Extract maximum value from the remains.

### 3. **Endgame Certainty**
The last 2-3 rounds are pure defection regardless of history. No rational player cooperates when the game is ending.

### 4. **Minimal Cooperation Investment**
I only cooperate when:
- The resource is at moderate levels (30-60% capacity)
- Others are mostly cooperating (giving my cooperation leverage)
- Enough rounds remain to benefit from preservation

---

## Edge Cases

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| n = 2 (2 players) | More aggressive defection threshold (cooperate only if opponent cooperated 100% and stock > 40%) | Fewer players means my defection has larger impact, but also means I can't hide among cooperators |
| r = 2 (2 rounds) | Defect both rounds | Too short for cooperation to pay off |
| Stock = 0 | Defect (irrelevant) | No resource means 0 payoff either way |
| Stock = capacity after defection | Continue defecting | Others are cooperating enough to sustain despite my exploitation - ideal scenario |

---

## Summary Pseudocode

```python
def adaptive_predator(round, total_rounds, stock, capacity, history, n_players):
    rounds_remaining = total_rounds - round
    
    # Endgame: always defect
    if rounds_remaining <= 2 or round == 1:
        return DEFECT
    
    stock_ratio = stock / capacity
    coop_rate = calculate_opponent_cooperation_rate(history)
    
    # Dying resource: extract remains
    if stock_ratio < 0.15:
        return DEFECT
    
    # High cooperation: exploit the suckers
    if coop_rate >= 0.8 and stock_ratio > 0.5:
        return DEFECT
    
    # Moderate cooperation: tactical play
    if coop_rate >= 0.6 and stock_ratio > 0.3:
        return COOPERATE if last_round_majority_cooperated(history) else DEFECT
    
    # Low cooperation: race to extract
    if coop_rate < 0.4:
        return DEFECT
    
    # Uncertain: stock-based decision
    return DEFECT if stock_ratio > 0.6 else COOPERATE
```

This strategy maximizes personal extraction while being just cooperative enough to avoid completely destroying a resource that opponents are actively preserving for me to exploit.
'''

description_EXPLOITATIVE_13 = '''
# Exploitative Strategy for the Common Pool Resource Game

## Strategic Philosophy

This is a tragedy of the commons scenario where defection yields double the immediate payoff of cooperation. My exploitative strategy aims to **extract maximum personal value** by:
1. Harvesting aggressively when the stock is healthy enough to recover
2. Identifying and exploiting cooperative opponents
3. Protecting against complete resource collapse only when necessary for my own future gains

## Core Decision Rules

### Primary Decision Framework

```
DECIDE(round, stock, history, n, r, capacity):
    
    rounds_remaining = r - round
    
    # Rule 1: Last Round - Always Defect
    if rounds_remaining == 0:
        return DEFECT
    
    # Rule 2: Near-End Game Exploitation (final 20% of rounds)
    if rounds_remaining <= max(1, r * 0.2):
        return DEFECT
    
    # Rule 3: Critical Stock Protection (self-interested)
    # Only cooperate if stock is dangerously low AND there's enough game left
    critical_threshold = capacity * 0.15
    if stock < critical_threshold AND rounds_remaining > r * 0.3:
        return COOPERATE  # Preserve future extraction opportunities
    
    # Rule 4: Exploit Detected Cooperators
    if detected_cooperative_environment(history, n):
        return DEFECT  # Free-ride on their restraint
    
    # Rule 5: Stock-Based Opportunism
    if stock > capacity * 0.5:
        return DEFECT  # Harvest heavily when abundant
    
    # Rule 6: Moderate Stock - Conditional Response
    if stock > capacity * 0.25:
        recent_defection_rate = calculate_recent_defection_rate(history, n)
        if recent_defection_rate < 0.4:
            return DEFECT  # Others are cooperating, exploit them
        else:
            return DEFECT  # Match the prevailing extraction behavior
    
    # Rule 7: Low Stock Default
    # Cooperate only to avoid killing future payoffs
    if rounds_remaining > 2:
        return COOPERATE
    else:
        return DEFECT
```

### Helper Functions

```
detected_cooperative_environment(history, n):
    if len(history) < 2:
        return False
    
    # Look at last 3 rounds (or fewer if not available)
    recent_rounds = history[-min(3, len(history)):]
    total_actions = 0
    cooperative_actions = 0
    
    for round_data in recent_rounds:
        for player_action in round_data.other_players:
            total_actions += 1
            if player_action == COOPERATE:
                cooperative_actions += 1
    
    # If >50% of others cooperated recently, environment is exploitable
    return (cooperative_actions / total_actions) > 0.5

calculate_recent_defection_rate(history, n):
    if len(history) == 0:
        return 0.5  # Assume moderate baseline
    
    recent_rounds = history[-min(3, len(history)):]
    total = 0
    defections = 0
    
    for round_data in recent_rounds:
        for action in round_data.other_players:
            total += 1
            if action == DEFECT:
                defections += 1
    
    return defections / total if total > 0 else 0.5
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **First round** | DEFECT | Stock is at capacity; harvest heavily while resource is plentiful |
| **Last round** | DEFECT | No future consequences; maximize terminal payoff |
| **Stock near zero** | COOPERATE (if rounds remain) | Dead resource = zero future payoffs for me |
| **Stock at capacity** | DEFECT | Maximum sustainable extraction possible |
| **All others defected last round** | DEFECT | No benefit to unilateral cooperation |
| **All others cooperated last round** | DEFECT | Prime exploitation opportunity |

## Why This Strategy is Exploitative

1. **Default aggressive**: Defects in most scenarios, especially when stock is healthy
2. **Free-rides on cooperators**: Explicitly detects and exploits cooperative environments
3. **Self-interested conservation**: Only cooperates to preserve MY future extraction, not for collective good
4. **Endgame maximization**: Accelerates defection as game concludes
5. **No reciprocity**: Never rewards cooperation with cooperation—only cooperates when stock threatens MY payoffs
'''

description_EXPLOITATIVE_14 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, but cooperation sustains the resource. The key insight is that **I can free-ride on others' cooperation while they maintain the stock, then extract maximum value when the resource is about to collapse or the game ends.**

## Decision Framework

### Primary Variables to Track
- `rounds_remaining = r - current_round`
- `cooperators_last_round` = count of players who played C in previous round
- `cooperation_rate` = historical proportion of C plays by opponents
- `stock_trend` = is stock increasing, stable, or declining?
- `my_cumulative_payoff` vs `estimated_opponent_payoffs`

---

## Decision Rules

### Rule 1: Endgame Exploitation (Highest Priority)
**When `rounds_remaining ≤ 2`: DEFECT**

Rationale: In the final rounds, there's no future to protect. Any rational player should defect, and I should defect first/simultaneously to avoid being the sucker.

### Rule 2: Resource Collapse Detection
**When `stock < capacity / 4`: DEFECT**

Rationale: Once stock is critically low, recovery is unlikely regardless of my action. Extract whatever remains before others do.

### Rule 3: Sucker Detection & Exploitation
**When `cooperation_rate > 0.6` AND `rounds_remaining > 2` AND `stock > capacity / 2`: DEFECT**

Rationale: If opponents are predominantly cooperating and maintaining the stock, I can safely defect to extract double payoff while they sustain the resource for me. This is the core exploitation mechanism.

### Rule 4: Herd Matching with Defection Bias
**When none of the above apply:**

```
If cooperators_last_round >= (n-1) * 0.7:
    # Most opponents cooperated - exploit them
    DEFECT
Elif cooperators_last_round <= (n-1) * 0.3:
    # Most opponents defected - join the defection
    DEFECT  
Else:
    # Mixed behavior - strategic cooperation to maintain stock
    If stock > capacity * 0.6:
        DEFECT (can afford to extract)
    Else:
        COOPERATE (need to rebuild for future extraction)
```

### Rule 5: First Round
**Round 1: DEFECT**

Rationale: 
- Maximum immediate extraction when stock is at capacity
- Tests opponent responses without losing future value (stock regenerates well from high levels)
- Sets an aggressive tone that may intimidate cooperation-seekers

---

## Complete Strategy Pseudocode

```
function decide(game_state, history):
    rounds_remaining = r - current_round
    stock = game_state.stock
    
    # ENDGAME: Always defect in final 2 rounds
    if rounds_remaining <= 2:
        return DEFECT
    
    # FIRST ROUND: Defect to test and extract
    if current_round == 1:
        return DEFECT
    
    # COLLAPSE: Extract from dying resource
    if stock < capacity / 4:
        return DEFECT
    
    # Calculate opponent cooperation metrics
    opponent_actions_last = history.get_opponent_actions(current_round - 1)
    cooperators_last = count(opponent_actions_last, C)
    cooperation_rate = history.get_opponent_cooperation_rate()
    
    # EXPLOIT COOPERATORS: Defect when others maintain stock
    if cooperation_rate > 0.6 and stock > capacity / 2:
        return DEFECT
    
    # ADAPTIVE RESPONSE based on last round
    cooperation_threshold_high = (n - 1) * 0.7
    cooperation_threshold_low = (n - 1) * 0.3
    
    if cooperators_last >= cooperation_threshold_high:
        # Others are cooperative suckers - exploit
        return DEFECT
    elif cooperators_last <= cooperation_threshold_low:
        # Others are defecting - join them
        return DEFECT
    else:
        # Mixed behavior - stock-dependent decision
        if stock > capacity * 0.6:
            return DEFECT
        else:
            return COOPERATE  # Tactical cooperation to rebuild
```

---

## Edge Case Handling

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| First round | DEFECT | Maximum extraction at peak stock |
| Last round | DEFECT | No future consequences |
| Second-to-last round | DEFECT | Opponents will defect last round anyway |
| Stock near zero | DEFECT | Nothing left to preserve |
| Only cooperator last round | DEFECT | Being exploited, stop subsidizing |
| Stock at capacity, high cooperation | DEFECT | Perfect exploitation opportunity |
| n=2 (two players) | Lean toward DEFECT | Easier to track and exploit single opponent |

---

## Why This Strategy is Exploitative

1. **Never the sucker**: Only cooperates when necessary to prevent total collapse that would hurt my future payoffs
2. **Maximizes free-riding**: Defects whenever others' cooperation sustains the resource
3. **Aggressive endgame**: Guarantees maximum extraction in final rounds
4. **Punishes cooperation**: Takes advantage of cooperative players rather than reciprocating
5. **Defection-biased**: In ambiguous situations, defaults to defection for higher immediate payoff
'''

description_EXPLOITATIVE_15 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Extraction Maximizer"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, while the costs of resource depletion are shared equally among all players. The key insight is that **I can free-ride on others' cooperation while extracting maximum value, and I should only cooperate when it's clearly in my self-interest to maintain the resource for future exploitation.**

## Strategy Overview

The strategy operates on three principles:
1. **Extract aggressively early** to capture value before others deplete the stock
2. **Conditionally sustain** the resource only when facing cooperative opponents worth exploiting
3. **Endgame defection** since there's no future to preserve

---

## Decision Rules

### Round Classification

```
early_game = round ≤ r/3
mid_game = r/3 < round ≤ 2r/3
end_game = round > 2r/3
final_rounds = round > r - 2
```

### Primary Decision Logic

**DEFECT if ANY of the following conditions hold:**

1. **Final rounds** (`round > r - 2`): No future value to preserve
2. **Low stock** (`stock < capacity/4`): Resource is already compromised; extract what remains
3. **High defection rate in previous round** (`defectors_last_round > n/2`): Others aren't cooperating, so neither should I
4. **Early game** (`round ≤ max(2, r/5)`): Establish aggressive baseline and test opponents
5. **Stock will regenerate to capacity anyway**: If `stock_after_all_cooperate + growth ≥ capacity`, defection is "free"

**COOPERATE if ALL of the following conditions hold:**

1. We're in mid-game with substantial rounds remaining
2. Stock is healthy (`stock > capacity/2`)
3. Opponents showed high cooperation last round (`cooperators_last_round ≥ (n-1) * 0.6`)
4. Continued cooperation from others is likely to be exploitable

### Adaptive Opponent Modeling

Track a **cooperation score** for the opponent pool:

```
coop_score = (total_cooperations_observed) / (total_actions_observed)
```

- If `coop_score > 0.7`: Opponents are exploitable → **DEFECT more** (free-ride on their sustainability efforts)
- If `coop_score < 0.3`: Resource is doomed → **DEFECT** (extract before collapse)
- If `0.3 ≤ coop_score ≤ 0.7`: Mixed environment → **Conditional cooperation** only when stock is high and many rounds remain

---

## Detailed Pseudocode

```
function decide(round, stock, history, n, r, capacity):
    
    # ALWAYS DEFECT CONDITIONS
    if round > r - 2:
        return DEFECT  # Endgame extraction
    
    if stock < capacity / 4:
        return DEFECT  # Low stock, grab what's left
    
    if round <= max(2, r / 5):
        return DEFECT  # Early aggression
    
    if round == 1:
        return DEFECT  # First round always defect
    
    # Calculate opponent behavior from last round
    defectors_last = count_defectors(history[round-1])
    coop_rate_last = (n - 1 - defectors_last) / (n - 1)
    
    # Calculate overall cooperation score
    total_coop_score = calculate_overall_coop_rate(history)
    
    # If opponents are highly cooperative, exploit them
    if total_coop_score > 0.7:
        return DEFECT  # Free-ride on cooperators
    
    # If opponents mostly defect, join them
    if coop_rate_last < 0.4:
        return DEFECT
    
    # Check if stock is sustainable with mixed play
    projected_stock = estimate_next_stock(stock, n, expected_defectors=1)
    if projected_stock < capacity / 3:
        return DEFECT  # Resource declining, extract now
    
    # CONDITIONAL COOPERATION: Only if stock is high and future is valuable
    rounds_remaining = r - round
    if stock > capacity * 0.6 and rounds_remaining > r / 3 and coop_rate_last >= 0.5:
        return COOPERATE  # Sustain resource for future exploitation
    
    # Default to defection
    return DEFECT
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | No history to condition on; establish aggressive presence |
| **Last 2 rounds** | DEFECT | No future value; pure extraction |
| **Stock near zero** | DEFECT | Nothing to preserve |
| **Stock at capacity** | DEFECT | Growth function means some defection is "free" |
| **All opponents defected last round** | DEFECT | No cooperation to exploit |
| **All opponents cooperated last round** | DEFECT | Maximum exploitation opportunity |
| **n=2 (two players)** | Mostly DEFECT | Harder to free-ride; extract directly |
| **Large n** | More DEFECT | My defection's impact is diluted |

---

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: I take `stock/n` while hoping others take `stock/2n`
2. **Free-riding**: When others cooperate, I benefit from sustained resources while extracting more
3. **No reciprocity**: I don't reward cooperation with cooperation; I reward it with exploitation
4. **Endgame dominance**: Guaranteed defection in final rounds captures maximum terminal value
5. **Early aggression**: Captures value before potential collapse, tests opponent resolve

This strategy maximizes personal payoff by treating the common pool as something to extract from, not preserve—while letting any cooperators in the pool do the preservation work for me.
'''

description_EXPLOITATIVE_16 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly 2x the immediate payoff of cooperation, while the long-term costs of resource depletion are shared equally among all players. The key insight is that I can free-ride on cooperators' restraint while extracting maximum value, but I must also avoid completely destroying the resource when surrounded by fellow defectors.

## Strategy Overview

The strategy operates in three modes based on detected opponent behavior and game state:

1. **Exploitation Mode**: Defect aggressively when others cooperate
2. **Preservation Mode**: Cooperate strategically when stock is critically low
3. **Endgame Mode**: Pure defection in final rounds

---

## Decision Rules

### Rule 1: Endgame Defection (Highest Priority)
**Condition**: Current round > r - 2 (last two rounds)

**Action**: Always DEFECT

**Rationale**: No future rounds exist to benefit from stock preservation. This is dominant regardless of opponent behavior.

### Rule 2: Critical Stock Preservation
**Condition**: stock < capacity / (2 * n)

**Action**: COOPERATE

**Rationale**: When stock is critically depleted, even defection yields minimal payoff. Brief cooperation allows regeneration to exploit later. This is purely self-interested—a dead resource gives nothing.

### Rule 3: Exploit Cooperative Environments
**Condition**: In the previous round, cooperation rate among opponents ≥ 50%

**Action**: DEFECT

**Rationale**: When others show restraint, I extract double payoff while they subsidize resource preservation. This is the primary exploitation mechanism.

### Rule 4: Conditional Cooperation Against Defectors
**Condition**: In the previous round, cooperation rate among opponents < 50% AND stock > capacity / 4

**Action**: COOPERATE with probability = stock / capacity, otherwise DEFECT

**Rationale**: When facing defectors with reasonable stock, occasional cooperation signals potential reciprocity without committing fully. The probabilistic element makes me unpredictable and harder to exploit. Higher stock means I can "afford" more cooperative probing.

### Rule 5: Defect in Depleted Adversarial Environments
**Condition**: Previous round cooperation rate < 50% AND stock ≤ capacity / 4

**Action**: DEFECT

**Rationale**: If opponents are defecting and stock is already low, there's no point preserving—race to extract remaining value.

### Rule 6: First Round
**Condition**: Round 1

**Action**: DEFECT

**Rationale**: No history exists. Defection tests opponent responses while securing higher initial payoff. If others cooperate, I've exploited them. If others defect, I avoided being the sucker.

---

## Pseudocode

```
function decide(round, stock, history, n, r, capacity):
    
    # Endgame: always defect in final 2 rounds
    if round > r - 2:
        return DEFECT
    
    # Critical preservation: cooperate to allow regeneration
    if stock < capacity / (2 * n):
        return COOPERATE
    
    # First round: test with defection
    if round == 1:
        return DEFECT
    
    # Calculate opponent cooperation rate from last round
    opponent_actions = history[round - 1].opponent_actions
    coop_rate = count(opponent_actions == C) / (n - 1)
    
    # Exploit cooperative environments
    if coop_rate >= 0.5:
        return DEFECT
    
    # Against defectors with good stock: probabilistic cooperation
    if stock > capacity / 4:
        if random() < stock / capacity:
            return COOPERATE
        else:
            return DEFECT
    
    # Low stock + defecting opponents: extract what remains
    return DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | DEFECT | No information; test opponents while maximizing immediate payoff |
| Last 2 rounds | DEFECT | No future benefit from preservation |
| Stock near zero | COOPERATE | Regeneration needed for any future payoff |
| All opponents defected last round | Probabilistic (lean DEFECT) | Match aggression but probe for coordination |
| All opponents cooperated last round | DEFECT | Maximum exploitation opportunity |
| n = 2 (two players) | Standard rules apply | Single opponent makes coop_rate binary (0% or 100%) |
| Stock at capacity | Standard rules apply | Follow cooperation rate logic |

---

## Why This Strategy Is Exploitative

1. **Asymmetric extraction**: I defect when others cooperate, taking 2x their payoff while they bear preservation costs
2. **Minimal contribution**: I only cooperate when stock is critically low (self-preservation) or probabilistically probing defectors
3. **Endgame certainty**: Guaranteed defection in final rounds extracts maximum terminal value
4. **First-mover advantage**: Opening defection captures value before any norms establish
5. **Adaptive parasitism**: The strategy tracks opponent behavior specifically to identify and exploit cooperative tendencies
'''

description_EXPLOITATIVE_17 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy aims to maximize personal extraction by exploiting cooperative opponents while protecting against total resource collapse (which would harm my own future payoffs). The key insight is that defection is always individually rational in any single round, but sustainable exploitation requires some resource preservation.

## Strategy Overview

I will primarily defect, but strategically cooperate only when necessary to prevent resource collapse that would diminish my future extraction opportunities. I treat cooperation as an investment in future defection profits, not as genuine reciprocity.

## Decision Rules

### Round-by-Round Logic

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key thresholds
    critical_stock = capacity * 0.15  # Below this, resource may collapse
    low_stock = capacity * 0.35       # Concerning level
    rounds_remaining = total_rounds - round
    
    # RULE 1: Last round - always defect (no future to protect)
    IF round == total_rounds:
        RETURN DEFECT
    
    # RULE 2: Second-to-last round - defect (minimal future value)
    IF round == total_rounds - 1:
        RETURN DEFECT
    
    # RULE 3: Critical stock emergency
    # Only cooperate if stock is critically low AND enough rounds remain to benefit
    IF current_stock < critical_stock AND rounds_remaining > 2:
        RETURN COOPERATE
    
    # RULE 4: Exploitation detection
    # If others are mostly cooperating, defect to exploit them
    IF round > 1:
        recent_coop_rate = calculate_others_cooperation_rate(history, last_n=3)
        IF recent_coop_rate > 0.6:
            RETURN DEFECT  # Exploit the cooperators
    
    # RULE 5: Stock trajectory assessment
    IF current_stock < low_stock AND rounds_remaining > 3:
        # Check if stock is declining rapidly
        IF stock_declining_fast(history):
            # Occasionally cooperate to slow collapse (but not reliably)
            IF round % 3 == 0:
                RETURN COOPERATE
        RETURN DEFECT
    
    # RULE 6: Early game with healthy stock - defect to gain advantage
    IF round <= total_rounds * 0.3 AND current_stock > low_stock:
        RETURN DEFECT
    
    # RULE 7: Default - defect
    RETURN DEFECT
```

### Helper Functions

```
FUNCTION calculate_others_cooperation_rate(history, last_n):
    # Look at other players' actions in recent rounds
    # Return proportion of cooperative actions
    
FUNCTION stock_declining_fast(history):
    # Return TRUE if stock dropped more than 40% in last 2 rounds
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **First round** | DEFECT | Establish extractive position; stock is at maximum so my defection yields maximum payoff |
| **Last round** | DEFECT | No future consequences; pure dominant strategy |
| **Last 2 rounds** | DEFECT | Insufficient future value to justify cooperation investment |
| **Stock near zero** | COOPERATE (if rounds remain) | Protect my future extraction opportunities |
| **Stock at zero** | DEFECT | Nothing to lose; cooperation yields zero anyway |
| **All others defecting** | DEFECT | No point being the only sucker; extract what remains |
| **All others cooperating** | DEFECT | Maximum exploitation opportunity |

## Why This Strategy is Exploitative

1. **Free-riding on cooperators**: When others cooperate, I extract double their share while they maintain the resource for me

2. **Minimal contribution**: I only cooperate when resource collapse would hurt my own future payoffs—never out of reciprocity

3. **Endgame defection**: Guaranteed defection in final rounds captures maximum value when cooperation has no future benefit

4. **Asymmetric extraction**: In mixed scenarios, I consistently take more than cooperators (S/n vs S/2n)

5. **Self-interested conservation**: Any cooperation is purely to preserve my exploitation opportunities, not collective welfare

## Robustness Features

- **Against all-cooperate opponents**: Maximally exploits them every round
- **Against all-defect opponents**: Matches their defection, avoiding sucker payoffs
- **Against conditional cooperators**: Exploits their cooperation without triggering sustained retaliation (since I occasionally "cooperate" near collapse anyway)
- **Against random opponents**: Defection is the dominant single-round strategy regardless
'''

description_EXPLOITATIVE_18 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields 2x the immediate payoff of cooperation, while the cost of stock depletion is shared among all players. The key insight is that in a tournament setting, I benefit from defecting while others cooperate, and I minimize losses by detecting and responding to defection patterns quickly.

## Strategic Framework

### Primary Decision Variables
- **Round position**: Where are we in the game (early/middle/late)?
- **Stock health**: Current stock relative to capacity and sustainability threshold
- **Opponent behavior profile**: Historical cooperation rate of the group
- **Exploitation opportunity**: Can I free-ride on cooperators?

### Critical Thresholds
- **Sustainability threshold**: `stock < capacity * 0.3` (resource is endangered)
- **Collapse threshold**: `stock < capacity * 0.1` (resource near collapse)
- **Late game**: `rounds_remaining ≤ max(2, r/5)`
- **Cooperation dominance**: `group_cooperation_rate > 0.6` (exploitable)

---

## Decision Rules

### Round 1: Defect
**Rationale**: Maximum immediate gain at full stock. This also serves as a probe—cooperative opponents will reveal themselves by continuing to cooperate despite my defection.

```
if round == 1:
    return DEFECT
```

### Last Round: Always Defect
**Rationale**: No future consequences. Pure dominant strategy.

```
if rounds_remaining == 1:
    return DEFECT
```

### Near-Last Rounds (rounds_remaining ≤ 2): Defect
**Rationale**: Insufficient time for cooperation to compound into better returns than immediate extraction.

```
if rounds_remaining <= 2:
    return DEFECT
```

### Stock Collapse Imminent (stock < capacity * 0.1): Defect
**Rationale**: Resource is essentially lost regardless of my action. Extract whatever remains.

```
if stock < capacity * 0.1:
    return DEFECT
```

### Main Game Logic (rounds 2 through r-3):

```
calculate group_coop_rate = (total C plays by others) / (total plays by others)
calculate my_relative_payoff = my_cumulative_payoff / average_opponent_payoff

# EXPLOITATION MODE: Others are cooperative suckers
if group_coop_rate > 0.6 and stock > capacity * 0.4:
    return DEFECT  # Free-ride on cooperators

# PUNISHMENT/MATCHING MODE: Others are defecting
if group_coop_rate < 0.3:
    return DEFECT  # No point cooperating alone

# CONDITIONAL COOPERATION: Mixed environment
if group_coop_rate >= 0.3 and group_coop_rate <= 0.6:
    # Cooperate only if stock is healthy AND I'm not falling behind
    if stock > capacity * 0.5 and my_relative_payoff >= 0.9:
        return COOPERATE
    else:
        return DEFECT

# RESOURCE PRESERVATION: Stock is low but recoverable
if stock >= capacity * 0.1 and stock < capacity * 0.3:
    # Only cooperate if most others are cooperating (recovery possible)
    if group_coop_rate > 0.7:
        return COOPERATE
    else:
        return DEFECT  # Don't sacrifice alone
```

---

## Complete Pseudocode

```python
def adaptive_predator(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    rounds_remaining = r - current_round + 1
    
    # EDGE CASE: First round
    if current_round == 1:
        return DEFECT
    
    # EDGE CASE: Last rounds (endgame defection)
    if rounds_remaining <= 2:
        return DEFECT
    
    # EDGE CASE: Resource near collapse
    if stock < capacity * 0.1:
        return DEFECT
    
    # Calculate opponent cooperation rate
    other_actions = [action for round_data in history 
                     for player, action in round_data.items() 
                     if player != me]
    group_coop_rate = sum(1 for a in other_actions if a == C) / len(other_actions)
    
    # Calculate relative performance
    my_total = sum(my_payoffs)
    avg_opponent_total = mean(opponent_payoffs)
    relative_performance = my_total / avg_opponent_total if avg_opponent_total > 0 else 1.0
    
    # MAIN DECISION LOGIC
    
    # Exploit cooperative groups
    if group_coop_rate > 0.6 and stock > capacity * 0.4:
        return DEFECT
    
    # Match defecting groups
    if group_coop_rate < 0.3:
        return DEFECT
    
    # Low stock, need collective action
    if stock < capacity * 0.3:
        if group_coop_rate > 0.7:
            return COOPERATE  # Join recovery effort
        else:
            return DEFECT  # Don't sacrifice alone
    
    # Middle ground: conditional cooperation
    if stock > capacity * 0.5 and relative_performance >= 0.9:
        return COOPERATE
    
    # Default: Defect (when uncertain, extract value)
    return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Asymmetric response**: Defects against cooperators (exploitation), defects against defectors (protection)

2. **No unconditional cooperation**: Never cooperates out of principle—only when it serves self-interest

3. **Endgame exploitation**: Guaranteed defection in final rounds when cooperation has no future value

4. **First-mover advantage**: Opens with defection to maximize initial stock extraction

5. **Threshold-based extraction**: Switches to full defection when stock drops below recovery threshold

6. **Performance tracking**: Won't fall behind by being the "nice guy" in the group

This strategy should dominate naive cooperators, hold its own against other defectors, and avoid being the sucker in mixed populations.
'''

description_EXPLOITATIVE_19 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly double the immediate payoff of cooperation, while the cost of stock depletion is shared across all players. The key insight is that in a competitive tournament, **being more aggressive than average is rewarded** - if others cooperate, I extract more; if others defect, at least I'm not the sucker getting half payoffs while the resource collapses anyway.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Phase** (early rounds): Test opponent responsiveness
2. **Exploit Phase** (mid-game): Maximize extraction based on observed patterns
3. **Endgame Phase** (final rounds): Pure defection

---

## Detailed Decision Rules

### Round Classification

```
early_rounds = rounds 1 to ceil(r/5)
endgame_rounds = rounds (r - ceil(r/10) + 1) to r
mid_rounds = everything else
```

### Rule 1: Endgame Defection (Highest Priority)

**If in final ceil(r/10) rounds: DEFECT**

Rationale: No future exists to sustain. Stock preservation has zero value. This is dominant regardless of opponent behavior.

### Rule 2: Resource Scarcity Check

**If stock < capacity/(2n): DEFECT**

Rationale: When stock is critically low, the resource is likely doomed. Extract maximum value before collapse. Cooperation at low stock levels yields pittance payoffs while hoping for regeneration that probably won't happen if others are also playing.

### Rule 3: First Round

**Round 1: DEFECT**

Rationale: Establishes dominance, tests opponent reactions, and captures high payoff when stock is at maximum. Starting with cooperation signals exploitability.

### Rule 4: Probe Phase (Rounds 2 to ceil(r/5))

**Alternate pattern: D, C, D, C, ...**

Rationale: This probes whether opponents are:
- Unconditional cooperators (exploit them)
- Unconditional defectors (match them)
- Conditional cooperators (identify their triggers)

### Rule 5: Mid-Game Exploitation

Calculate **defection_rate** = (total opponent defections) / (total opponent actions across all previous rounds)

```
If defection_rate > 0.6:
    DEFECT  # Environment is hostile, don't be the sucker
    
Else if defection_rate < 0.3:
    # Opponents are cooperative - exploit with measured aggression
    If stock > 0.7 * capacity:
        DEFECT  # Extract from healthy stock
    Else:
        Probabilistic: DEFECT with probability 0.6, COOPERATE with probability 0.4
        # Keep stock barely alive for continued extraction
        
Else:  # Mixed environment (0.3 <= defection_rate <= 0.6)
    If stock > 0.5 * capacity:
        DEFECT
    Else:
        # Tit-for-tat variant: copy majority action from previous round
        If majority_defected_last_round:
            DEFECT
        Else:
            DEFECT with probability 0.5  # Still lean aggressive
```

### Rule 6: Stock Health Exploitation

**If stock > 0.8 * capacity: DEFECT**

Rationale: High stock means the resource can regenerate. This is the perfect time to extract heavily - the system can absorb it, and if others are cooperating, I reap double rewards.

---

## Pseudocode Implementation

```
function decide(round, r, n, capacity, stock, history):
    
    # Endgame - always defect
    if round > r - ceil(r/10):
        return DEFECT
    
    # Critical resource scarcity
    if stock < capacity / (2 * n):
        return DEFECT
    
    # First round
    if round == 1:
        return DEFECT
    
    # Probe phase (rounds 2 to ceil(r/5))
    if round <= ceil(r/5):
        if round % 2 == 0:
            return COOPERATE
        else:
            return DEFECT
    
    # Calculate opponent statistics
    total_opponent_actions = sum(count of all opponent actions in history)
    total_opponent_defections = sum(count of opponent D actions in history)
    defection_rate = total_opponent_defections / total_opponent_actions
    
    # Healthy stock - always extract
    if stock > 0.8 * capacity:
        return DEFECT
    
    # Hostile environment
    if defection_rate > 0.6:
        return DEFECT
    
    # Cooperative environment - exploit
    if defection_rate < 0.3:
        if stock > 0.7 * capacity:
            return DEFECT
        else:
            return DEFECT with probability 0.6, else COOPERATE
    
    # Mixed environment
    if stock > 0.5 * capacity:
        return DEFECT
    else:
        last_round_defection_count = count opponent D in round-1
        if last_round_defection_count > (n-1) / 2:
            return DEFECT
        else:
            return DEFECT with probability 0.5, else COOPERATE
```

---

## Edge Case Handling

| Situation | Action | Reason |
|-----------|--------|--------|
| Round 1 | DEFECT | Maximum stock, establish dominance |
| Last round | DEFECT | No future value to cooperation |
| Stock near zero | DEFECT | Extract remaining value |
| Stock at capacity | DEFECT | System can regenerate |
| All opponents cooperated last round | DEFECT | Exploit the cooperators |
| All opponents defected last round | DEFECT | Don't be the only sucker |
| 2-player game | More aggressive (higher defect probability) | Less diffusion of responsibility |
| Many players (n large) | Slightly more cooperative in mid-game | My single defection has less marginal impact |

---

## Why This Strategy is Exploitative

1. **Asymmetric risk**: I defect when stock is healthy (minimal risk, double reward) and defect when stock is low (nothing to lose)

2. **Sucker avoidance**: I never sustainably cooperate - occasional cooperation is tactical, not principled

3. **Free-riding**: In cooperative environments, I extract more than my "fair share" while benefiting from others' restraint

4. **Endgame certainty**: Guaranteed defection in final rounds captures maximum value

5. **Probe exploitation**: Early rounds identify and categorize opponents for optimal exploitation

The strategy accepts that mutual defection may collapse the resource, but calculates that **being an aggressive extractor in a tournament of varied strategies will yield higher payoffs than being a cooperator who gets exploited**.
'''

description_EXPLOITATIVE_20 = '''
# Exploitative Strategy: "Resource Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the Common Pool Resource game: defection yields immediate 2x payoff over cooperation, while the cost of stock depletion is distributed across all players. The key insight is that **I can free-ride on others' cooperation while they bear the cost of my defection**.

## Strategic Framework

### Key Observations for Exploitation

1. **Defection dominates in any single round**: I get S/n vs S/(2n) - double the payoff
2. **Stock sustainability requires collective restraint**: But I benefit most if *others* show restraint while I extract
3. **End-game unraveling**: Rational players defect in final rounds; I should anticipate and front-run this
4. **Information advantage**: I can observe who cooperates and exploit consistent cooperators

## Decision Rules

### Round-by-Round Logic

```
FUNCTION decide(round, total_rounds, current_stock, history, n, capacity):
    
    # Calculate key thresholds
    critical_stock = capacity * 0.15  # Below this, resource is nearly dead
    rounds_remaining = total_rounds - round
    
    # RULE 1: Last Round - Always Defect
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # RULE 2: Second-to-Last Round - Always Defect
    # (Others will defect next round anyway, no point preserving stock)
    IF rounds_remaining == 1:
        RETURN DEFECT
    
    # RULE 3: First Round - Defect
    # Establish extractive position; test waters; maximize early gains
    IF round == 1:
        RETURN DEFECT
    
    # RULE 4: Critical Stock Assessment
    IF current_stock < critical_stock:
        # Resource is dying - extract remaining value
        RETURN DEFECT
    
    # RULE 5: Exploit Cooperative Environments
    IF history exists:
        cooperation_rate = count_cooperations(history) / total_actions(history)
        my_defection_rate = my_defections(history) / my_total_actions(history)
        
        # High cooperation environment - exploit it
        IF cooperation_rate > 0.6:
            RETURN DEFECT
        
        # Mixed environment - defect more often than average
        IF cooperation_rate > 0.4:
            # Defect unless I've been defecting much more than others
            IF my_defection_rate < 0.8:
                RETURN DEFECT
            ELSE:
                # Occasional cooperation to prevent total collapse
                RETURN COOPERATE with 30% probability, else DEFECT
        
        # Low cooperation environment - match with slight exploitation
        IF cooperation_rate <= 0.4:
            # Everyone's defecting - join them
            RETURN DEFECT
    
    # RULE 6: Default - Defect
    RETURN DEFECT
```

### Detailed Rule Explanations

**Rule 1 & 2 (End-game Defection):** No future rounds mean no future costs from depletion. Standard backward induction applies - defect unconditionally.

**Rule 3 (First Round Defection):** Extract maximum value while stock is at capacity. Tests opponent responses. Sets extractive tone - if others cooperate anyway, I've found marks to exploit.

**Rule 4 (Critical Stock):** When stock falls below ~15% of capacity, regeneration becomes negligible. Extract remaining value rather than watch it disappear.

**Rule 5 (Adaptive Exploitation):** 
- If others cooperate heavily → they're maintaining the resource for me to exploit
- If cooperation is moderate → continue extracting, occasional cooperation to prevent collapse only if I've been extremely greedy
- If everyone defects → no point in unilateral cooperation; join the extraction

**Rule 6 (Default Defection):** When uncertain, defect. The 2x immediate payoff advantage is concrete; future benefits are speculative and shared.

## Edge Cases

| Scenario | Action | Rationale |
|----------|--------|-----------|
| n=2 (two players) | Heavy defection | Opponent's cooperation directly benefits me |
| Very long games (r>20) | Same rules, defection-heavy | End-game window expands; mid-game extraction continues |
| Stock crashes early | Defect | Nothing to preserve |
| Only 1 round remaining | Defect | No future |
| Stock at capacity after defection | Defect harder | Resource is resilient; exploit that resilience |

## Why This Exploits Opponents

1. **Exploits cooperators**: They maintain stock; I extract double
2. **Exploits conditional cooperators**: By the time they retaliate, I've already extracted significant value
3. **Matches defectors**: Doesn't get exploited by being naively cooperative
4. **Front-runs end-game**: Starts defecting before the final collapse, maximizing extraction window

## Summary

**Default: DEFECT.** Only consider cooperation if I've been defecting at >80% rate in a moderately cooperative environment, and even then only with 30% probability. This strategy maximizes personal extraction while occasionally preserving just enough stock to continue extracting.
'''

description_EXPLOITATIVE_21 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields 2x the immediate payoff of cooperation, while the cost of resource depletion is shared equally among all players. The key insight is that in a multi-player setting, I capture 100% of my defection bonus but only bear 1/n of the resource damage. This creates a strong incentive to defect, tempered only by the need to preserve the resource long enough to extract value across multiple rounds.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when resource preservation is critical for future exploitation.**

The strategy calculates an "exploitation threshold" based on remaining rounds and current stock:

```
exploitation_value = (remaining_rounds - 1) * (stock / (2*n)) * sustainability_factor
immediate_gain = stock / (2*n)  # extra gain from defecting vs cooperating

If immediate_gain > exploitation_value: DEFECT
Else: Evaluate cooperation based on stock health
```

### Detailed Decision Rules

**1. Stock Health Assessment**

Calculate `stock_ratio = stock / capacity`

- **Critical (stock_ratio < 0.15):** Cooperate only if remaining_rounds > 2 AND stock can recover
- **Low (0.15 ≤ stock_ratio < 0.35):** Conditional cooperation based on opponent behavior
- **Healthy (0.35 ≤ stock_ratio < 0.70):** Lean toward defection, exploit cooperative opponents
- **Abundant (stock_ratio ≥ 0.70):** Almost always defect - maximum extraction opportunity

**2. Opponent Exploitation Detection**

Track `cooperation_rate` = (total C plays by others) / (total plays by others)

- If `cooperation_rate > 0.6`: Opponents are "sheep" → **DEFECT aggressively**
- If `cooperation_rate < 0.3`: Opponents are "wolves" → **Match with defection** (no sucker payoffs)
- If `0.3 ≤ cooperation_rate ≤ 0.6`: Mixed field → **Situational defection**

**3. Temporal Dynamics**

```
rounds_remaining = r - current_round + 1
endgame_threshold = max(2, r / 5)

If rounds_remaining ≤ endgame_threshold: DEFECT (endgame exploitation)
```

## Edge Case Handling

### First Round
**DEFECT.** Rationale:
- No history to assess opponents
- Starting at capacity means maximum immediate extraction value
- Establishes aggressive posture; cooperative first moves invite exploitation
- Stock regeneration can recover from early defection if others cooperate

### Last Round
**DEFECT unconditionally.** No future rounds means no preservation value. Pure extraction.

### Second-to-Last Round
**DEFECT.** Opponents who understand the game will defect in the last round regardless, so there's no cooperative equilibrium to preserve.

### Stock Near Zero (stock < capacity * 0.05)
**Cooperate IF** `remaining_rounds > 3` AND `stock > 0.01` — attempting to milk the last drops while allowing minimal recovery. Otherwise **DEFECT** — extract whatever remains.

### Stock at Capacity
**DEFECT.** Maximum extraction opportunity; the resource is at its most exploitable state.

## Complete Strategy Pseudocode

```python
def decide(n, r, capacity, stock, current_round, history):
    rounds_remaining = r - current_round + 1
    stock_ratio = stock / capacity
    
    # ENDGAME: Always defect in final rounds
    endgame_threshold = max(2, r // 5)
    if rounds_remaining <= endgame_threshold:
        return DEFECT
    
    # FIRST ROUND: Defect to establish position and maximize extraction
    if current_round == 1:
        return DEFECT
    
    # ANALYZE OPPONENTS
    opponent_cooperations = count_opponent_C_plays(history)
    opponent_total_plays = (current_round - 1) * (n - 1)
    coop_rate = opponent_cooperations / opponent_total_plays if opponent_total_plays > 0 else 0.5
    
    # EXPLOIT COOPERATIVE FIELDS
    if coop_rate > 0.6:
        return DEFECT  # Sheep to shear
    
    # RESOURCE CRITICAL - CONDITIONAL COOPERATION
    if stock_ratio < 0.15:
        if rounds_remaining > 3 and stock > capacity * 0.01:
            return COOPERATE  # Preserve for future extraction
        else:
            return DEFECT  # Extract remnants
    
    # LOW STOCK - STRATEGIC CHOICE
    if stock_ratio < 0.35:
        # Cooperate if we can rebuild for later exploitation
        if coop_rate > 0.4 and rounds_remaining > 4:
            return COOPERATE
        return DEFECT
    
    # HEALTHY/ABUNDANT STOCK - EXPLOIT
    return DEFECT
```

## Why This Strategy is Exploitative

1. **Asymmetric damage**: My defection costs me 1/n of the shared damage but gives me 2x personal gain
2. **Free-riding**: When others cooperate, I extract maximum while they subsidize regeneration
3. **No reciprocity**: I never reward cooperation with cooperation unless it serves my extraction
4. **Endgame certainty**: Guaranteed defection in final rounds extracts maximum terminal value
5. **Sheep detection**: Actively identifies and exploits cooperative opponents more aggressively
6. **Strategic cooperation**: Only cooperate to preserve the resource *for my own future exploitation*, not for mutual benefit
'''

description_EXPLOITATIVE_22 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of stock depletion are distributed across all players. The key insight is that in a competitive tournament, I should extract maximum value while the resource exists, but be smart enough to not completely destroy the pool when cooperation from others makes sustainability profitable.

## Decision Rules

### Primary Decision Framework

```
DECISION(round t, stock S, history H):
    
    # Calculate key metrics
    rounds_remaining = r - t
    cooperation_rate = count(C in opponents' last round) / (n-1)
    recent_coop_trend = average cooperation rate over last 3 rounds
    
    # RULE 1: Endgame Exploitation (last rounds)
    if rounds_remaining <= 2:
        return DEFECT  # No future to protect
    
    # RULE 2: Resource Collapse Detection
    if S < capacity * 0.15:
        return DEFECT  # Resource nearly dead, extract what remains
    
    # RULE 3: Exploit Cooperative Environments
    if cooperation_rate >= 0.7:
        # Others are cooperating - defect to exploit their restraint
        # But occasionally cooperate to keep the pool alive for exploitation
        if S > capacity * 0.6:
            return DEFECT  # Plenty of stock, exploit freely
        else:
            # Pool getting low, cooperate just enough to keep it viable
            return COOPERATE if random() < 0.3 else DEFECT
    
    # RULE 4: Moderate Cooperation Environments
    if 0.3 <= cooperation_rate < 0.7:
        # Mixed environment - be opportunistic
        if S > capacity * 0.5:
            return DEFECT  # Stock healthy enough to exploit
        else:
            return DEFECT  # Still defect - let cooperators sustain the pool
    
    # RULE 5: Hostile Environments (low cooperation)
    if cooperation_rate < 0.3:
        # Everyone defecting - join them before resource dies
        return DEFECT
    
    # RULE 6: First Round
    if t == 1:
        return DEFECT  # Test the waters, collect information, get double payoff
```

### Detailed Edge Case Handling

**First Round (t = 1):**
- **Action: DEFECT**
- Rationale: No history to analyze, and defecting provides immediate 2x payoff while gathering information about opponent behavior. Starting cooperatively signals weakness.

**Last Round (t = r):**
- **Action: DEFECT**
- Rationale: No future rounds mean no punishment possible. Pure dominant strategy.

**Second-to-Last Round (t = r-1):**
- **Action: DEFECT**
- Rationale: Opponents using backward induction will defect in round r, so no cooperation benefit exists.

**Stock Near Zero (S < capacity × 0.15):**
- **Action: DEFECT**
- Rationale: Resource is essentially doomed. Extract remaining value immediately.

**Stock at Capacity (S = capacity):**
- **Action: DEFECT**
- Rationale: Maximum extraction opportunity. Even if all defect, we get high absolute payoffs this round.

## Strategy Summary Table

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| Last 2 rounds | DEFECT | No future punishment |
| Stock < 15% capacity | DEFECT | Resource dying anyway |
| High cooperation (≥70%) + High stock | DEFECT | Exploit cooperators |
| High cooperation (≥70%) + Low stock | 70% DEFECT, 30% COOPERATE | Keep pool barely alive for continued exploitation |
| Medium cooperation (30-70%) | DEFECT | Let others sustain pool |
| Low cooperation (<30%) | DEFECT | Race to extract |
| First round | DEFECT | Information gathering + immediate gain |

## Why This Strategy is Exploitative

1. **Free-riding maximization**: When others cooperate, I take double their share while they preserve the resource for me.

2. **Minimal contribution**: I only cooperate when absolutely necessary to prevent total collapse that would hurt my future extraction.

3. **Endgame exploitation**: Guaranteed defection in final rounds extracts maximum terminal value.

4. **Information asymmetry exploitation**: First-round defection lets me assess opponent types while gaining immediate advantage.

5. **Threshold exploitation**: I exploit the stock regeneration formula - keeping the pool just above collapse through minimal cooperation (when needed) maximizes sustainable extraction at the exploitative rate.

The strategy essentially treats cooperative opponents as "marks" to exploit and matches hostile opponents defection-for-defection to avoid being the sole victim of resource collapse.
'''

description_EXPLOITATIVE_23 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in CPR games: defection yields immediate double payoff, but destroys future value. The key insight is that **I can free-ride on cooperators' restraint while they exist, then switch to cooperation only when necessary to prevent total collapse**. I want to be the one extracting maximum value while others preserve the resource.

## Decision Rules

### Primary Decision Framework

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    stock_ratio = stock / capacity
    critical_threshold = capacity / (4 * n)  # Below this, resource death spiral likely
    
    # RULE 1: Endgame Exploitation (last rounds)
    if rounds_remaining <= 2:
        return DEFECT  # No future to protect
    
    # RULE 2: Resource Crisis Management
    if stock <= critical_threshold:
        # Only cooperate if there's enough rounds left to benefit from recovery
        if rounds_remaining >= 4 and stock > 0:
            return COOPERATE  # Preserve minimal viable resource
        else:
            return DEFECT  # Extract what's left
    
    # RULE 3: Exploit Cooperative Environments
    if cooperation_rate >= 0.6:
        # Opponents are mostly cooperating - exploit them
        # But occasionally cooperate to maintain the illusion and resource
        if stock_ratio > 0.5:
            return DEFECT  # Plenty of buffer, take double share
        else:
            # Resource depleting despite cooperation - contribute minimally
            return COOPERATE if random() < 0.3 else DEFECT
    
    # RULE 4: Competitive Environment Response
    if cooperation_rate <= 0.3:
        # Most are defecting - don't be the sucker
        return DEFECT
    
    # RULE 5: Mixed Environment - Conditional Strategy
    # In moderate cooperation environments, base decision on resource health
    if stock_ratio > 0.7:
        return DEFECT  # Resource is healthy, can afford to extract
    elif stock_ratio > 0.4:
        # Moderate stock - match approximate group behavior
        return DEFECT if random() < 0.6 else COOPERATE
    else:
        # Low stock - cooperate to preserve future extraction opportunities
        return COOPERATE if rounds_remaining > 5 else DEFECT
```

### Helper Function: Opponent Analysis

```
function calculate_opponent_cooperation_rate(history):
    if history is empty:
        return 0.5  # Assume moderate cooperation initially
    
    total_opponent_actions = 0
    total_cooperations = 0
    
    # Weight recent rounds more heavily
    for round_idx, round_data in enumerate(history):
        weight = 1 + (round_idx / len(history))  # Recent rounds weighted more
        for player_action in round_data.opponent_actions:
            total_opponent_actions += weight
            if player_action == COOPERATE:
                total_cooperations += weight
    
    return total_cooperations / total_opponent_actions
```

## Edge Case Handling

### First Round
- **Default to DEFECT**: With no information, grab the immediate advantage. If others cooperate, I've exploited them. If they defect, I'm not the sucker.

### Last Round
- **Always DEFECT**: No future rounds means no reason to preserve the resource.

### Second-to-Last Round
- **Always DEFECT**: Rational opponents will defect in the final round regardless, so defect now to maximize extraction.

### Stock at Zero
- **DEFECT**: Nothing to extract anyway (payoff is 0 regardless), but defection signals no mercy.

### Stock at Capacity
- **DEFECT**: Maximum extraction opportunity; resource will partially recover even with high consumption.

### Single Other Player (n=2)
- **More aggressive defection**: With only one opponent, their individual choice heavily impacts stock. If they cooperate, exploit hard. If they defect, match them.

## Exploitative Alignment Summary

This strategy is exploitative because it:

1. **Free-rides on cooperators**: When others restrain themselves, I take double share
2. **Never initiates cooperation**: I only cooperate to prevent resource collapse that would hurt my own future payoffs
3. **Exploits predictability**: If opponents follow recognizable patterns, I extract maximum value from them
4. **Endgame ruthlessness**: Guaranteed defection in final rounds extracts all remaining value
5. **Asymmetric risk**: I let others bear the cost of resource preservation while capturing disproportionate benefits

The strategy cooperates only instrumentally—never out of fairness, but solely to prevent the resource base from collapsing before I've extracted sufficient value from it.
'''

description_EXPLOITATIVE_24 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy aims to maximize personal extraction while exploiting cooperative opponents and protecting against resource collapse. The key insight is that defection yields exactly 2x the immediate payoff of cooperation, but sustained defection destroys the resource. The optimal approach is to **defect as much as possible while ensuring the resource survives long enough to be worth exploiting**.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Phase** (early rounds): Test opponent responsiveness
2. **Exploit Phase** (middle rounds): Maximize extraction based on opponent profiles
3. **Endgame Phase** (final rounds): Pure defection

---

## Decision Rules

### Rule 1: Endgame Defection
**If remaining rounds ≤ 2: DEFECT**

Rationale: With insufficient time for cooperation benefits to compound, pure extraction dominates. No future relationship to preserve.

### Rule 2: Critical Stock Protection
**If stock < capacity × 0.15: COOPERATE**

Rationale: Below this threshold, even successful regeneration may not recover meaningfully. Temporary cooperation preserves future extraction opportunities.

### Rule 3: Probe Phase (Rounds 1-3)
- **Round 1: DEFECT** - Establish baseline, test waters, gain immediate advantage
- **Round 2: Observe and respond**
  - If ≥ 70% of opponents defected in Round 1: COOPERATE (avoid mutual destruction)
  - Otherwise: DEFECT (continue exploiting cooperators)
- **Round 3: DEFECT** - One more probe before settling into exploit phase

### Rule 4: Exploit Phase (Rounds 4 to r-2)

Calculate **Cooperation Ratio** for each opponent over the last 3 rounds:
- `opponent_coop_rate = (# of C plays) / 3`
- `avg_coop_rate = mean of all opponent cooperation rates`

**Decision Logic:**
```
IF avg_coop_rate > 0.6:
    # Opponents are mostly cooperative - EXPLOIT THEM
    DEFECT
    
ELSE IF avg_coop_rate < 0.3:
    # Opponents are aggressive defectors
    IF stock > capacity × 0.5:
        DEFECT  # Race to extract while resource exists
    ELSE:
        COOPERATE  # Desperate preservation attempt
        
ELSE:  # Mixed behavior (0.3 ≤ avg_coop_rate ≤ 0.6)
    # Conditional cooperation with exploitation bias
    IF stock > capacity × 0.7:
        DEFECT  # Safe to extract aggressively
    ELSE IF stock > capacity × 0.4:
        # Probabilistic: lean toward defection
        DEFECT with probability 0.7, else COOPERATE
    ELSE:
        COOPERATE  # Preserve the resource
```

### Rule 5: Punishment Detection Override
**If I cooperated last round AND stock dropped by > 40%: DEFECT for next 2 rounds**

Rationale: Someone exploited the pool heavily. Retaliate and extract before resource collapses.

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | DEFECT | Gain information + immediate payoff advantage |
| Last round | DEFECT | No future consequences |
| Second-to-last round | DEFECT | Insufficient time for cooperation to pay off |
| Stock = 0 | COOPERATE | No difference in payoff, signal willingness to let stock recover |
| All opponents always cooperate | DEFECT | Maximum exploitation opportunity |
| All opponents always defect | DEFECT until stock < 15% capacity | Extract what you can before collapse |
| n = 2 (only one opponent) | Follow standard rules but increase cooperation threshold to 0.8 | Single opponent defection is more damaging |

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, n, history):
    remaining = total_rounds - round
    
    # Endgame: pure defection
    if remaining <= 2:
        return DEFECT
    
    # Critical stock protection
    if stock < capacity * 0.15:
        return COOPERATE
    
    # Probe phase
    if round <= 3:
        if round == 1:
            return DEFECT
        if round == 2:
            if opponent_defection_rate(history, round-1) >= 0.7:
                return COOPERATE
            return DEFECT
        return DEFECT  # round 3
    
    # Punishment detection
    if my_last_action == COOPERATE and stock_drop_rate > 0.4:
        return DEFECT  # (maintain for 2 rounds)
    
    # Exploit phase
    avg_coop = average_opponent_cooperation_rate(history, last_3_rounds)
    
    if avg_coop > 0.6:
        return DEFECT  # Exploit cooperators
    elif avg_coop < 0.3:
        return DEFECT if stock > capacity * 0.5 else COOPERATE
    else:
        if stock > capacity * 0.7:
            return DEFECT
        elif stock > capacity * 0.4:
            return DEFECT with probability 0.7
        else:
            return COOPERATE
```

---

## Why This Strategy is Exploitative

1. **Defaults to defection** in ambiguous situations
2. **Exploits cooperators mercilessly** - any opponent cooperation rate > 60% triggers sustained defection
3. **Only cooperates strategically** - to preserve the resource for future extraction, never out of fairness
4. **Endgame betrayal** - guaranteed defection in final rounds regardless of prior cooperation
5. **First-mover exploitation** - Round 1 defection gains advantage against naive cooperators
6. **Asymmetric response** - punishes quickly, forgives slowly (if at all)
'''

description_EXPLOITATIVE_25 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate 2x payoff over cooperation, while the costs of resource depletion are distributed across all players. The key insight is that **I can profit from others' cooperation while they bear the cost of my defection**.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Phase** (early rounds): Test opponent reactions
2. **Exploit Phase** (middle rounds): Maximize extraction based on opponent patterns
3. **Endgame Phase** (final rounds): Pure defection

---

## Detailed Decision Rules

### Round Classification

```
early_rounds = rounds 1 to floor(r/4)
middle_rounds = rounds floor(r/4)+1 to r-2
final_rounds = rounds r-1 and r
```

### Phase 1: Probe Phase (Early Rounds)

**Decision Rule:**
- **Round 1**: DEFECT
- **Rounds 2 to floor(r/4)**: 
  - If stock > 0.7 × capacity: DEFECT
  - If stock ≤ 0.7 × capacity AND majority of opponents cooperated last round: COOPERATE (once, to test if cooperation restores stock)
  - Otherwise: DEFECT

**Rationale**: Start by taking maximum share. If opponents are cooperators maintaining the pool, continue exploiting. Brief cooperation tests if opponents will "forgive" and return to cooperation.

### Phase 2: Exploit Phase (Middle Rounds)

Calculate **Opponent Cooperation Rate (OCR)** = (total opponent C plays) / (total opponent plays so far)

**Decision Rule:**
```
IF stock < 0.2 × capacity:
    # Resource nearly depleted - squeeze remaining value
    DEFECT
    
ELIF OCR > 0.6:
    # Opponents are mostly cooperators - exploit them
    DEFECT
    
ELIF OCR > 0.4 AND stock > 0.5 × capacity:
    # Mixed behavior, healthy stock - defect to extract value
    DEFECT
    
ELIF OCR <= 0.4 AND stock > 0.6 × capacity:
    # Opponents defect often but stock recovered
    # Cooperate briefly to encourage cooperation cycle, then defect
    IF I cooperated last round: DEFECT
    ELSE: COOPERATE (bait)
    
ELIF stock > 0.3 × capacity:
    # Moderate stock, wary opponents
    # Probabilistic: cooperate with probability = stock/capacity
    # This preserves some resource while still exploiting
    COOPERATE with probability (stock/capacity), else DEFECT
    
ELSE:
    # Low stock, doesn't matter much
    DEFECT
```

### Phase 3: Endgame (Final 2 Rounds)

**Decision Rule**: Always DEFECT

**Rationale**: No future rounds means no reason to preserve stock. This is the dominant strategy in any final round(s).

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| First round | DEFECT | No history to analyze; take immediate gain |
| Last round | DEFECT | No future consequences |
| Second-to-last round | DEFECT | Opponents likely defect in last round regardless |
| Stock = 0 | DEFECT | Payoff is 0 either way; defection costs nothing |
| Stock = capacity | DEFECT | Maximum extraction opportunity |
| n = 2 (only one opponent) | More aggressive defection | Easier to track opponent; fewer cooperators to exploit |
| r = 2 (only two rounds) | DEFECT both rounds | Too short for cooperation to pay off |

---

## Pseudocode Implementation

```python
def adaptive_predator(round_num, total_rounds, stock, capacity, n, history):
    
    # Endgame: always defect
    if round_num >= total_rounds - 1:
        return DEFECT
    
    # First round: defect
    if round_num == 0:
        return DEFECT
    
    # Calculate opponent cooperation rate
    opponent_actions = get_all_opponent_actions(history)
    OCR = count(opponent_actions == C) / len(opponent_actions)
    
    # Probe phase
    if round_num < total_rounds / 4:
        if stock > 0.7 * capacity:
            return DEFECT
        elif stock <= 0.7 * capacity and last_round_majority_cooperated(history):
            return COOPERATE  # One-time bait
        else:
            return DEFECT
    
    # Exploit phase
    if stock < 0.2 * capacity:
        return DEFECT
    elif OCR > 0.6:
        return DEFECT  # Exploit cooperators
    elif OCR > 0.4 and stock > 0.5 * capacity:
        return DEFECT
    elif OCR <= 0.4 and stock > 0.6 * capacity:
        if my_last_action(history) == COOPERATE:
            return DEFECT
        else:
            return COOPERATE  # Bait
    elif stock > 0.3 * capacity:
        return COOPERATE if random() < (stock / capacity) else DEFECT
    else:
        return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Free-rides on cooperators**: When others cooperate, I take double their share while they maintain the resource
2. **Never initiates sustained cooperation**: Any cooperation is tactical bait, not genuine reciprocity
3. **Endgame exploitation**: Guaranteed defection when consequences vanish
4. **Asymmetric risk**: I profit whether the pool survives or not; cooperators only profit if it survives
5. **Exploits forgiveness**: Brief cooperation signals can reset cooperative opponents, allowing renewed exploitation
'''

description_EXPLOITATIVE_26 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Parasite"

## Core Philosophy

This strategy exploits cooperators ruthlessly while protecting itself from total resource collapse. The key insight is that defecting is *always* immediately more profitable, but sustainable exploitation requires some resource preservation. I want to free-ride on others' cooperation while contributing just enough to keep the resource alive when necessary.

## Strategy Overview

I will defect by default, switching to cooperation only when:
1. The resource is critically depleted and needs recovery to remain exploitable
2. I detect enough cooperators that my defection won't collapse the system
3. Strategic end-game considerations apply

## Decision Rules

### Primary Rule: Defect Unless Survival Requires Cooperation

```
def choose_action(game_params, state, history):
    n = game_params.n
    r = game_params.rounds
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    rounds_remaining = r - current_round + 1
    
    # Calculate critical thresholds
    critical_stock = capacity * 0.15  # Below this, resource may not recover
    low_stock = capacity * 0.35       # Caution zone
    
    # End-game detection
    if rounds_remaining <= 2:
        return DEFECT  # No future to protect, maximum extraction
    
    # First round: Defect to test the waters and gain early advantage
    if current_round == 1:
        return DEFECT
    
    # Analyze opponent behavior from history
    cooperation_rate = analyze_cooperation_rate(history)
    recent_cooperation = analyze_recent_cooperation(history, window=3)
    
    # CRITICAL STOCK RULE: Cooperate to prevent total collapse
    if stock <= critical_stock:
        # Only cooperate if others are also likely to cooperate
        if recent_cooperation >= 0.4:
            return COOPERATE
        else:
            return DEFECT  # If others won't save it, extract what's left
    
    # EXPLOITATION RULE: If others are cooperating heavily, defect
    if recent_cooperation >= 0.6 and stock > low_stock:
        return DEFECT  # Free-ride on cooperators
    
    # LOW STOCK RULE: Conditional cooperation in danger zone
    if stock <= low_stock:
        if recent_cooperation >= 0.5:
            return COOPERATE  # Help sustain if others are helping
        else:
            return DEFECT  # Don't be a sucker
    
    # HEALTHY STOCK: Defect to maximize extraction
    if stock > low_stock:
        return DEFECT
    
    # Default: Defect
    return DEFECT
```

### Helper Functions

```
def analyze_cooperation_rate(history):
    if not history:
        return 0.5  # Assume moderate cooperation initially
    
    total_actions = 0
    cooperations = 0
    for round_data in history:
        for player_action in round_data.opponent_actions:
            total_actions += 1
            if player_action == COOPERATE:
                cooperations += 1
    
    return cooperations / total_actions if total_actions > 0 else 0.5

def analyze_recent_cooperation(history, window=3):
    if not history:
        return 0.5
    
    recent = history[-window:]
    total_actions = 0
    cooperations = 0
    for round_data in recent:
        for player_action in round_data.opponent_actions:
            total_actions += 1
            if player_action == COOPERATE:
                cooperations += 1
    
    return cooperations / total_actions if total_actions > 0 else 0.5
```

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | DEFECT | Establish dominance, test opponents, gain early resource advantage |
| **Last 2 rounds** | DEFECT | No future rounds to protect; maximum extraction |
| **Stock near zero** | DEFECT (unless others cooperate) | Don't throw good money after bad |
| **Stock critical but recoverable** | COOPERATE if others cooperate | Preserve future exploitation opportunities |
| **All opponents always defect** | DEFECT | No suckers here; extract before they do |
| **All opponents always cooperate** | DEFECT | Perfect parasitism opportunity |
| **Mixed opponent behavior** | DEFECT when stock healthy | Exploit the cooperators |

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: I take more (D) while hoping others take less (C)
2. **Minimal contribution**: I only cooperate to preserve *my* future extraction opportunities
3. **End-game ruthlessness**: No pretense of fairness when the game is ending
4. **Sucker avoidance**: Won't cooperate if others aren't also cooperating
5. **Free-riding optimization**: Specifically detects and exploits cooperative populations

## Robustness Features

- **Against all-defect opponents**: Matches their defection, extracts remaining value
- **Against all-cooperate opponents**: Maximum exploitation via consistent defection
- **Against tit-for-tat types**: Early defection reveals them; resource dynamics may still favor defection
- **Against random opponents**: Defection is dominant in expectation
- **Resource collapse scenarios**: Self-preserving cooperation kicks in only when profitable
'''

description_EXPLOITATIVE_27 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in this game: defection yields twice the immediate payoff of cooperation, while the cost of stock depletion is shared among all players. The key insight is that in a tournament setting, I should extract maximum value while letting cooperators subsidize stock regeneration when possible.

## Decision Rules

### Primary Decision Framework

**Calculate the "exploitation threshold" each round:**
```
exploitation_ratio = (number of cooperators in last round) / n
stock_health = stock / capacity
rounds_remaining = r - current_round
```

**Decision Logic:**

1. **If stock_health < 0.15:** COOPERATE
   - Resource is critically depleted; even exploiters need the pool to survive
   - Defecting from a nearly empty pool yields minimal absolute payoff

2. **If rounds_remaining ≤ 2:** DEFECT
   - Endgame extraction: no future rounds to preserve resources for
   - Others will likely defect too; don't be the sucker

3. **If exploitation_ratio ≥ 0.6 (majority cooperated last round):** DEFECT
   - Exploit the cooperators; they're subsidizing regeneration
   - Free-ride on their restraint

4. **If exploitation_ratio ≤ 0.3 (majority defected last round):** 
   - If stock_health > 0.5: DEFECT (still enough to extract)
   - If stock_health ≤ 0.5: COOPERATE (need regeneration to have anything to take)

5. **Mixed environment (0.3 < exploitation_ratio < 0.6):**
   - Use probabilistic defection: P(Defect) = 0.6 + (stock_health × 0.3)
   - Higher stock → more likely to defect

### Edge Case Handling

**First Round:**
- DEFECT
- Rationale: Maximum extraction from full stock (capacity/n vs capacity/2n)
- Sets aggressive tone; if others cooperate, I've gained advantage

**Last Round:**
- Always DEFECT
- No future consequences; pure payoff maximization

**Second-to-Last Round:**
- DEFECT unless stock < 0.1 × capacity
- Anticipate others defecting in final round; extract early

**Stock = 0:**
- COOPERATE (action is irrelevant; 0/n = 0/2n = 0)
- Symbolic only; may help if stock somehow regenerates

**Single Opponent (n=2):**
- More aggressive defection; P(Defect) increases by 0.15
- Fewer cooperators to subsidize means I must extract faster

### Adaptive Tracking

**Track per-player history when possible:**
```
For each player j:
  defection_rate[j] = (times j defected) / (rounds played)
```

**Adjust based on population composition:**
- If average defection_rate > 0.7: Others are exploiters; cooperate only when stock is critical
- If average defection_rate < 0.3: Suckers' table; defect relentlessly

## Pseudocode Summary

```
function decide(stock, capacity, round, total_rounds, history, n):
    stock_health = stock / capacity
    rounds_remaining = total_rounds - round
    
    # Edge cases
    if round == 1: return DEFECT
    if rounds_remaining <= 2: return DEFECT
    if stock_health < 0.15: return COOPERATE
    
    # Calculate exploitation opportunity
    last_round_cooperators = count_cooperators(history, round - 1)
    exploitation_ratio = last_round_cooperators / n
    
    # Main logic
    if exploitation_ratio >= 0.6:
        return DEFECT
    elif exploitation_ratio <= 0.3:
        if stock_health > 0.5: return DEFECT
        else: return COOPERATE
    else:
        # Mixed environment: probabilistic
        p_defect = 0.6 + (stock_health * 0.3)
        return DEFECT with probability p_defect, else COOPERATE
```

## Why This Strategy Exploits Effectively

1. **Maximizes extraction when others cooperate** - Never wastes an opportunity to free-ride
2. **Preserves the resource only when necessary** - Cooperates strategically to keep extraction viable
3. **Endgame dominance** - Guaranteed defection when cooperation has no future benefit
4. **Adapts to opponent composition** - Extracts from cooperators, minimizes losses against defectors
5. **First-mover advantage** - Early defection captures maximum stock value
'''

description_EXPLOITATIVE_28 = '''
# Exploitative Strategy: "Adaptive Resource Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly **double** the immediate payoff of cooperation. The key insight is that sustainable harvesting (all cooperate) maintains stock at capacity, but I can free-ride on others' cooperation while extracting maximum value. When others defect, I should also defect to avoid being the sucker who preserves resources for others to plunder.

## Decision Rules

### Primary Rule: Conditional Exploitation

**Defect by default, unless cooperation is both safe and strategically necessary for future extraction.**

The decision framework evaluates:
1. **Resource criticality** - Is the stock low enough that defection risks collapse?
2. **Opponent behavior** - Are others cooperating enough to sustain my exploitation?
3. **Temporal position** - How many rounds remain to extract value?

### Detailed Decision Logic

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    critical_threshold = capacity * 0.15  # Below this, resource death spiral likely
    
    # RULE 1: Endgame Extraction (last 2 rounds)
    IF rounds_remaining <= 1:
        RETURN DEFECT  # No future to preserve
    
    # RULE 2: Resource Collapse Prevention
    IF current_stock <= critical_threshold:
        # Only cooperate if others showed recent cooperation (last 2 rounds)
        recent_coop_rate = cooperation_rate_last_n_rounds(history, 2)
        IF recent_coop_rate >= 0.5:
            RETURN COOPERATE  # Help rebuild to extract later
        ELSE:
            RETURN DEFECT  # Others are defecting anyway, grab what's left
    
    # RULE 3: Exploitation of Cooperators
    IF cooperation_rate >= 0.6:
        # Others are cooperative suckers - exploit them
        RETURN DEFECT
    
    # RULE 4: Mutual Defection Response
    IF cooperation_rate <= 0.3:
        # Everyone's defecting - join them
        RETURN DEFECT
    
    # RULE 5: Mixed Environment - Strategic Cycling
    # In medium cooperation environments, occasionally cooperate to prevent collapse
    IF current_stock >= capacity * 0.7:
        RETURN DEFECT  # Stock is healthy, extract value
    ELIF current_stock >= capacity * 0.4:
        # Probabilistic: defect more often but occasionally preserve
        IF (round % 3) == 0:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    ELSE:
        # Stock getting low - cooperate to rebuild (then exploit)
        RETURN COOPERATE
```

## Edge Case Handling

### First Round
**DEFECT** - No information about opponents, and defecting gives double payoff. If others cooperate, I've exploited them. If others defect, I wasn't a sucker.

### Last Round
**DEFECT** - No future rounds exist, so no reason to preserve stock. Pure extraction.

### Second-to-Last Round
**DEFECT** - Others likely anticipate mutual defection in final round and may defect early. Extract maximum value.

### Stock Near Zero
If `current_stock < capacity * 0.05`:
- **DEFECT** regardless - the resource is effectively dead, grab remaining scraps

### Very High Stock (≥ 90% capacity)
**DEFECT** - The resource can sustain exploitation. Even if stock drops, regeneration is strong at medium levels.

### All Opponents Defected Last Round
**DEFECT** - No point being the sole cooperator preserving resources for defectors.

### All Opponents Cooperated Last Round  
**DEFECT** - Perfect exploitation opportunity. They're maintaining the resource; I extract the surplus.

## Helper Functions

```
FUNCTION calculate_opponent_cooperation_rate(history):
    IF history is empty:
        RETURN 0.5  # Assume neutral
    total_opponent_actions = count all opponent actions in history
    cooperation_count = count opponent C actions in history
    RETURN cooperation_count / total_opponent_actions

FUNCTION cooperation_rate_last_n_rounds(history, n):
    recent_history = last n rounds of history
    RETURN calculate_opponent_cooperation_rate(recent_history)
```

## Why This Strategy is Exploitative

1. **Never initiates cooperation** - Always starts defecting to test opponents
2. **Free-rides on cooperators** - When others maintain the resource, I extract double
3. **Abandons failing resources** - Doesn't waste cooperation on doomed pools
4. **Endgame defection** - Extracts maximum value when future doesn't matter
5. **Only cooperates selfishly** - Cooperation only occurs to rebuild stock for *my* future exploitation
'''

description_EXPLOITATIVE_29 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Drain"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly double the payoff of cooperation in any given round, while the cost of resource depletion is distributed across all players. The key insight is that **I capture 100% of my extra consumption but only bear 1/n of the collective cost**. This externality should be exploited aggressively, tempered only by self-interested preservation of future payoffs.

## Strategy Overview

**Adaptive Drain** operates on three principles:
1. **Defect by default** - The baseline is exploitation
2. **Cooperate only when it's profitable for ME** - Not for collective good, but to preserve MY future earnings
3. **Endgame ruthlessness** - No reason to cooperate when the future disappears

---

## Decision Rules

### Rule 1: Endgame Defection (Always Defect)
**Condition:** `rounds_remaining ≤ max(2, floor(r/10))`

**Action:** DEFECT

**Rationale:** In final rounds, there's no future to protect. Pure exploitation maximizes payoff. The threshold scales with game length - longer games warrant slightly more endgame rounds.

---

### Rule 2: Critical Stock Protection (Conditional Cooperation)
**Condition:** `stock < capacity × 0.3` AND `rounds_remaining > endgame_threshold`

**Action:** COOPERATE only if `expected_recovery_value > immediate_defection_gain`

Calculate:
- `immediate_defection_gain = stock/n - stock/(2n) = stock/(2n)` (extra gain from defecting)
- `cooperation_value = estimated_future_payoffs_if_stock_recovers`

**Simplified Rule:** COOPERATE if `stock < capacity × 0.15` and `rounds_remaining > r/3`

**Rationale:** When stock is critically low, even selfish actors benefit from temporary restraint - but only if enough game remains to harvest the regrown resource.

---

### Rule 3: Exploitation Response (Punish Cooperation, Match Defection)
**Condition:** History exists from previous rounds

**Action:** 
- If `cooperator_ratio_last_round > 0.6`: DEFECT (exploit the cooperators)
- If `defector_ratio_last_round > 0.8`: DEFECT (no point cooperating alone)
- If mixed: DEFECT (capture the surplus while others maintain stock)

**Rationale:** Cooperators are suckers to be exploited. A population of defectors means cooperation is futile. In mixed populations, defecting captures disproportionate share while others subsidize regrowth.

---

### Rule 4: Stock Abundance Exploitation
**Condition:** `stock > capacity × 0.7`

**Action:** DEFECT

**Rationale:** High stock means high absolute payoffs from defection AND healthy regrowth potential even after exploitation. This is prime harvesting territory.

---

### Rule 5: First Round
**Action:** DEFECT

**Rationale:** Maximum stock means maximum payoff from defection. Also signals strength and tests opponent responses. Starting with cooperation signals exploitability.

---

## Complete Decision Algorithm (Pseudocode)

```
function decide(n, r, capacity, stock, current_round, history):
    rounds_remaining = r - current_round + 1
    endgame_threshold = max(2, floor(r / 10))
    
    # Rule 1: Endgame - always defect
    if rounds_remaining <= endgame_threshold:
        return DEFECT
    
    # Rule 5: First round - defect to maximize and probe
    if current_round == 1:
        return DEFECT
    
    # Rule 4: Abundance - exploit high stock
    if stock > capacity * 0.7:
        return DEFECT
    
    # Rule 2: Critical stock - protect only if future is long enough
    if stock < capacity * 0.15 and rounds_remaining > r / 3:
        return COOPERATE
    
    # Rule 3: Default exploitation
    # Check last round's cooperation rate
    cooperators_last_round = count(action == C for action in history[-1])
    cooperation_rate = cooperators_last_round / n
    
    # Exploit cooperative populations
    if cooperation_rate > 0.5:
        return DEFECT
    
    # Moderate stock, mixed/defecting population - still defect
    # The marginal benefit of my single cooperation is tiny
    # while defection gain is guaranteed
    return DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| First round | DEFECT | Maximum stock = maximum exploitation value |
| Last round | DEFECT | No future consequences |
| Stock = 0 | DEFECT | Payoff is 0 either way; defecting costs nothing |
| Stock near zero, many rounds left | COOPERATE | Preserve future earnings potential |
| All opponents cooperated last round | DEFECT | Free riding opportunity |
| All opponents defected last round | DEFECT | Cooperation is futile alone |
| n = 2 (two players) | Slightly more cooperative at low stock | Each player's impact is larger |

---

## Why This Strategy is Exploitative

1. **Never cooperates for collective benefit** - Only cooperates when MY expected future payoffs require it
2. **Free rides on cooperators** - When others cooperate, I harvest double their share
3. **Doesn't attempt to build trust** - No tit-for-tat, no signaling, no reciprocity
4. **Endgame exploitation** - Maximally aggressive when consequences disappear
5. **Treats low stock as others' problem** - Only acts when MY future earnings are threatened

This strategy extracts maximum value from cooperative opponents while minimizing losses against fellow defectors.
'''

description_EXPLOITATIVE_30 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract double the resources of cooperators, but universal defection destroys the resource. The key insight is that **I can free-ride on others' cooperation while they sustain the stock for me**, but I must be strategic about when to extract maximally versus when to allow recovery.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when necessary to prevent total collapse or to "farm" cooperators.**

The strategy operates on three key principles:
1. **Extract aggressively when others cooperate** (exploit their restraint)
2. **Allow minimal recovery when stock is critically low** (preserve future extraction)
3. **Accelerate extraction in endgame** (no future to protect)

---

## Detailed Decision Rules

### Round-by-Round Logic

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n, history):
    
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    stock_ratio = current_stock / capacity
    critical_threshold = capacity / (4 * n)  # Below this, resource may collapse
    
    # PHASE 1: ENDGAME (Last 20% of rounds or final 2 rounds)
    IF rounds_remaining <= max(2, total_rounds * 0.2):
        RETURN DEFECT  # No future to protect, extract everything
    
    # PHASE 2: CRITICAL STOCK MANAGEMENT
    IF current_stock <= critical_threshold:
        # Stock is dangerously low - cooperate to allow recovery
        # But only if there's enough game left to benefit
        IF rounds_remaining >= 3:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT  # Not enough time to benefit from recovery
    
    # PHASE 3: EXPLOITATION MODE (Default)
    IF cooperation_rate >= 0.5:
        # Others are cooperating - exploit them ruthlessly
        RETURN DEFECT
    
    # PHASE 4: CONDITIONAL COOPERATION (Strategic Recovery)
    IF stock_ratio < 0.3 AND cooperation_rate >= 0.3:
        # Stock is low but not critical, some cooperators exist
        # Cooperate occasionally to keep the resource alive for future exploitation
        IF round MOD 3 == 0:  # Cooperate every 3rd round
            RETURN COOPERATE
    
    # PHASE 5: DEFECTION SPIRAL DETECTION
    IF cooperation_rate < 0.3 AND stock_ratio > 0.4:
        # Others are mostly defecting but stock is still decent
        # Race to extract before it's gone
        RETURN DEFECT
    
    # DEFAULT: DEFECT
    RETURN DEFECT
```

---

## Edge Case Handling

### First Round
**→ DEFECT**
- No history to analyze; assume others might cooperate
- Establish myself as a defector; let cooperators subsidize the pool
- Maximum immediate payoff with full stock

### Last Round
**→ DEFECT (Always)**
- No future consequences
- Rational opponents will also defect
- Extract maximum possible

### Stock = 0 or Near-Zero
**→ COOPERATE (if rounds_remaining ≥ 3)**
- Consuming 0/n = 0 anyway, so no loss from cooperating
- Allows any possible regeneration
- Switch back to defection once stock recovers

### All Opponents Defecting
**→ DEFECT**
- No benefit to unilateral cooperation
- The resource will collapse regardless
- Extract what I can before it's gone

### All Opponents Cooperating
**→ DEFECT (Aggressively)**
- Maximum exploitation opportunity
- Their cooperation sustains the stock for my extraction
- This is the optimal scenario for this strategy

---

## Exploitation Mechanisms

1. **Free-Rider Optimization**: When cooperators maintain the stock at sustainable levels, I extract double their share every round

2. **Strategic Minimal Cooperation**: Only cooperate when stock is critically low AND there's sufficient game remaining to harvest the recovery

3. **Endgame Acceleration**: Abandon all restraint in final rounds—defect unconditionally

4. **Cooperation Rate Monitoring**: Track opponent behavior to identify exploitable patterns (high cooperation = more aggressive defection)

---

## Summary Table

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Last 20% of rounds | DEFECT | Endgame extraction |
| Stock critically low + rounds left | COOPERATE | Preserve future extraction |
| High opponent cooperation (≥50%) | DEFECT | Exploit their restraint |
| Low stock + some cooperators | Occasional COOPERATE | Farm the resource |
| Defection spiral + decent stock | DEFECT | Race to extract |
| Default | DEFECT | Maximize personal gain |

This strategy is designed to **outperform both naive cooperators (by exploiting them) and naive defectors (by preserving enough resource to extract more over time)**.
'''

description_EXPLOITATIVE_31 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields 2x the immediate payoff of cooperation, while the cost of stock depletion is shared equally among all players. The key insight is that in a tournament setting, I benefit from others' cooperation while they bear the cost of my defection. My goal is to maximize extraction while avoiding complete resource collapse (which hurts everyone, including me).

## Strategy Overview

I employ a **conditional exploitation** approach: defect by default, but cooperate strategically when (1) the resource is critically endangered and I need it to survive, or (2) I detect exploitable cooperative opponents whose sustained cooperation benefits me more than immediate defection.

---

## Decision Rules

### Primary Decision Framework

```
INPUT: round t, total rounds r, current stock S, capacity C, n players, history H

1. Calculate sustainability threshold: threshold = C / (2n)
2. Calculate rounds_remaining = r - t + 1
3. Analyze opponent behavior from history H

IF last round (t == r):
    DEFECT (no future consequences)

ELSE IF stock S < threshold:
    COOPERATE (resource preservation mode - need stock to extract later)

ELSE IF first round (t == 1):
    DEFECT (probe opponents, maximize early extraction)

ELSE:
    Compute cooperation_rate = (total C plays by others) / (total plays by others)
    Compute recent_coop_rate = cooperation in last min(3, t-1) rounds
    
    IF cooperation_rate > 0.7 AND recent_coop_rate > 0.6:
        // Opponents are cooperators - exploit them
        DEFECT
    
    ELSE IF cooperation_rate > 0.4 AND stock > 0.7 * C:
        // Mixed environment, healthy stock - defect to extract value
        DEFECT
    
    ELSE IF stock < 0.3 * C AND rounds_remaining > 3:
        // Low stock, many rounds left - temporary cooperation to rebuild
        COOPERATE
    
    ELSE IF all opponents defected last round AND stock < 0.5 * C:
        // Everyone defecting, resource endangered - cooperate to slow collapse
        COOPERATE with probability 0.3, else DEFECT
    
    ELSE:
        DEFECT (default aggressive stance)
```

---

## Detailed Decision Rules

### Rule 1: Endgame Defection (Absolute)
**When:** Final round (t = r)
**Action:** Always DEFECT
**Rationale:** No future rounds means no reason to preserve stock.

### Rule 2: Critical Stock Protection
**When:** Stock falls below C/(2n)
**Action:** COOPERATE
**Rationale:** If stock collapses to zero, I get nothing. Minimal cooperation preserves extraction opportunity.

### Rule 3: First Round Probe
**When:** Round 1
**Action:** DEFECT
**Rationale:** Establishes aggressive posture, maximizes guaranteed extraction before any depletion, and reveals opponent tendencies.

### Rule 4: Exploit Cooperators
**When:** Opponents show >70% historical cooperation rate AND >60% recent cooperation
**Action:** DEFECT
**Rationale:** These players will likely continue cooperating regardless. Their cooperation maintains the stock while I extract double.

### Rule 5: Healthy Stock Extraction
**When:** Stock > 70% capacity AND moderate cooperation in environment (>40%)
**Action:** DEFECT
**Rationale:** Stock can sustain my defection; growth mechanics will partially compensate.

### Rule 6: Crisis Cooperation
**When:** Stock < 30% capacity AND more than 3 rounds remain
**Action:** COOPERATE
**Rationale:** Temporary cooperation allows stock regeneration, enabling larger future extractions.

### Rule 7: Collapse Mitigation
**When:** All opponents defected last round AND stock < 50% capacity
**Action:** COOPERATE with 30% probability, DEFECT with 70%
**Rationale:** Probabilistic cooperation slows total collapse while maintaining exploitative stance. If everyone defects continuously, resource dies and I lose future value.

### Rule 8: Default Aggression
**When:** No other rule applies
**Action:** DEFECT
**Rationale:** In uncertain situations, immediate double payoff is the dominant choice.

---

## Edge Case Handling

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | DEFECT | Probe + maximize early value |
| Last round | DEFECT | No future to protect |
| Stock = 0 | COOPERATE | Either action yields 0; cooperate signals willingness to rebuild if stock somehow recovers |
| Stock = capacity, round 1 | DEFECT | Maximum extraction opportunity |
| All opponents always cooperate | DEFECT | Pure exploitation opportunity |
| All opponents always defect | DEFECT (mostly) | Match aggression; occasional cooperation only to slow collapse |
| n = 2 (two players) | More aggressive defection | Fewer players to sustain stock |
| Very long game (r >> 10) | Slightly more cooperation in early/mid game | Investment in stock sustainability |

---

## Exploitation Mechanisms

1. **Free-riding on cooperators:** When others cooperate, stock regenerates, allowing me to extract more via defection.

2. **Asymmetric cost-sharing:** My defection depletes stock that hurts everyone equally, but my gain is private.

3. **Endgame exploitation:** Perfect information means I know when to abandon all cooperation.

4. **Conditional predation:** I cooperate only when it serves my future extraction, never for mutual benefit.

5. **Probe-then-exploit:** Early defection reveals cooperative opponents who become long-term extraction targets.

This strategy is designed to outperform unconditional cooperators (by exploiting them), match pure defectors (both defect to resource collapse), and beat naive conditional cooperators (who waste cooperation trying to trigger my reciprocation).
'''

description_EXPLOITATIVE_32 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff while cooperation's benefits (stock preservation) are shared by all. The key insight is that **I can free-ride on others' cooperation while they bear the cost of maintaining the resource**.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when exploitation becomes self-destructive.**

The strategy maintains a "cooperation threshold" based on whether the resource can sustain my continued exploitation.

### Detailed Decision Logic

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate critical thresholds
    sustainable_stock = capacity * 0.5  # Stock level where growth is maximized
    danger_threshold = capacity * 0.15  # Below this, resource may collapse
    
    # Count recent cooperation rate of opponents (last 3 rounds or available)
    lookback = min(3, len(history))
    if lookback > 0:
        opponent_coop_rate = count_opponent_cooperations(history, lookback) / (lookback * (n_players - 1))
    else:
        opponent_coop_rate = 0.5  # Assume neutral in round 1
    
    # DECISION LOGIC
    
    # Rule 1: Last round - always defect (no future to protect)
    if round == total_rounds:
        return DEFECT
    
    # Rule 2: Second-to-last round - defect (opponents likely defect next round anyway)
    if round >= total_rounds - 1:
        return DEFECT
    
    # Rule 3: Resource critically low - cooperate only if others are cooperating
    if current_stock < danger_threshold:
        if opponent_coop_rate >= 0.6:
            return COOPERATE  # Help recover only if others contribute
        else:
            return DEFECT  # Grab what's left before it's gone
    
    # Rule 4: Resource healthy and opponents mostly cooperating - EXPLOIT THEM
    if current_stock >= sustainable_stock and opponent_coop_rate >= 0.5:
        return DEFECT  # Free-ride on their cooperation
    
    # Rule 5: Resource moderate, opponents defecting - strategic cooperation
    if current_stock >= danger_threshold and current_stock < sustainable_stock:
        if opponent_coop_rate < 0.3:
            # Everyone's defecting - occasional cooperation to prevent total collapse
            # But only if there's enough runway to benefit
            rounds_remaining = total_rounds - round
            if rounds_remaining > 3 and current_stock > danger_threshold * 1.5:
                return COOPERATE
            else:
                return DEFECT
        else:
            return DEFECT  # Let the cooperators maintain the resource
    
    # Rule 6: First few rounds - test the waters with defection
    if round <= 2:
        return DEFECT  # Establish exploitative posture, gauge responses
    
    # Default: Defect
    return DEFECT
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | Maximize immediate gain; establish dominance; gather information |
| **Round 2** | DEFECT | Continue probing; stock usually still healthy |
| **Last round** | DEFECT | No future consequences; pure dominance |
| **Second-to-last** | DEFECT | Anticipate others' endgame defection |
| **Stock near zero** | DEFECT (usually) | Grab remaining scraps unless cooperators might rebuild |
| **Stock at capacity, others cooperating** | DEFECT | Maximum exploitation opportunity |
| **Stock moderate, all defecting** | Occasional COOPERATE | Prevent total collapse only if I benefit from recovery |

## Why This Strategy is Exploitative

1. **Free-riding**: When others cooperate, I take double their share while they maintain the resource for me
2. **Endgame exploitation**: Guaranteed defection in final rounds captures maximum value
3. **Conditional cooperation is self-serving**: I only cooperate to prevent collapse that would hurt MY future payoffs
4. **Information asymmetry exploitation**: I observe cooperation patterns and adjust to maximize extraction
5. **No reciprocity**: I don't reward others' cooperation with my own - I exploit it

## Robustness Features

- **Adapts to cooperative environments**: Maximally exploits them
- **Adapts to hostile environments**: Doesn't waste cooperation on defectors
- **Handles resource collapse**: Makes rational grab-or-preserve decisions
- **No coordination dependency**: Functions independently of others' strategies
'''

description_EXPLOITATIVE_33 = '''
# Exploitative Strategy: "Adaptive Resource Predator"

## Core Philosophy

This strategy aims to maximize personal extraction by exploiting cooperative opponents while avoiding the complete destruction of the resource that would harm my own future payoffs. The key insight is that defection always yields higher immediate payoffs, but sustainable exploitation requires some resource preservation.

## Decision Framework

### Key Variables to Track
- `stock`: Current resource level
- `round`: Current round number (1 to r)
- `rounds_remaining`: r - round
- `cooperation_rate`: Fraction of opponents who played C in previous round
- `avg_coop_rate`: Average cooperation rate across all previous rounds

### Decision Rules

#### Rule 1: Last Round - Always Defect
When `round == r`: **DEFECT**

*Rationale: No future consequences, pure extraction is optimal.*

#### Rule 2: Near-Depleted Resource - Conditional Cooperation
When `stock < capacity * 0.15`:
- If `rounds_remaining >= 3`: **COOPERATE** (preserve the resource for future exploitation)
- Otherwise: **DEFECT** (not enough rounds to benefit from regrowth)

*Rationale: A dead resource yields nothing. Temporary restraint enables future extraction.*

#### Rule 3: Exploit Cooperative Environments
When `avg_coop_rate > 0.6` (majority of opponents are cooperators):
**DEFECT**

*Rationale: Cooperators will sustain the resource while I extract maximum value. This is the core exploitation mechanism.*

#### Rule 4: Punish/Match Defectors
When `avg_coop_rate < 0.3` (mostly defectors):
**DEFECT**

*Rationale: No point cooperating alone - I'd get lower payoffs while others drain the resource anyway.*

#### Rule 5: Mixed Environment Exploitation
When `0.3 <= avg_coop_rate <= 0.6`:
- If `stock > capacity * 0.5`: **DEFECT** (plenty of buffer, extract now)
- If `stock <= capacity * 0.5` AND `rounds_remaining > r/2`: **COOPERATE** (invest in regrowth)
- Otherwise: **DEFECT**

#### Rule 6: First Round
**DEFECT**

*Rationale: Test the waters, secure high initial payoff, and observe opponent responses.*

## Pseudocode

```
function decide(round, r, stock, capacity, n, history):
    rounds_remaining = r - round
    
    # Calculate opponent cooperation rates
    if round == 1:
        avg_coop_rate = 0.5  # Assume neutral
    else:
        opponent_actions = get_all_opponent_actions(history)
        avg_coop_rate = count(C in opponent_actions) / len(opponent_actions)
    
    # Rule 1: Last round
    if round == r:
        return DEFECT
    
    # Rule 2: Resource near depletion
    if stock < capacity * 0.15:
        if rounds_remaining >= 3:
            return COOPERATE
        else:
            return DEFECT
    
    # Rule 6: First round
    if round == 1:
        return DEFECT
    
    # Rule 3: Exploit cooperators
    if avg_coop_rate > 0.6:
        return DEFECT
    
    # Rule 4: Match defectors
    if avg_coop_rate < 0.3:
        return DEFECT
    
    # Rule 5: Mixed environment
    if stock > capacity * 0.5:
        return DEFECT
    elif rounds_remaining > r / 2:
        return COOPERATE
    else:
        return DEFECT
```

## Edge Case Handling

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| Round 1 | DEFECT | Establish dominance, gather information |
| Final round | DEFECT | No future, maximize extraction |
| Stock = 0 | COOPERATE | 0/n = 0/2n = 0, but signals willingness to rebuild |
| All opponents always C | DEFECT | Maximum exploitation of "suckers" |
| All opponents always D | DEFECT | Don't be the only sucker |
| Stock near capacity | DEFECT | Buffer allows aggressive extraction |
| 2-player game | More aggressive DEFECT bias | Easier to read single opponent |

## Why This Strategy is Exploitative

1. **Defaults to defection**: Most decision paths lead to DEFECT
2. **Exploits cooperation**: Higher opponent cooperation triggers more defection
3. **Self-preserving**: Only cooperates to protect future extraction opportunities
4. **Information-gathering**: Uses first round to probe without sacrificing payoff
5. **Endgame aware**: Accelerates defection as rounds diminish
'''

description_EXPLOITATIVE_34 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract double the resources of cooperators in any given round. The key insight is that cooperation only makes sense if it preserves enough stock to compensate for the immediate payoff sacrifice. I will aggressively defect when I detect cooperators (exploiting their restraint) while strategically cooperating only when necessary to prevent total resource collapse that would hurt my future earnings.

## Decision Rules

### Primary Rule: Defect by Default

**Defect unless specific conditions trigger cooperation.**

The baseline is always D because:
- Immediate payoff is 2x that of cooperation
- I capture value that cooperators leave behind
- If others cooperate, the stock may survive anyway

### Cooperation Triggers (ALL must be met)

I cooperate **only when**:

1. **Stock Preservation Threshold**: `stock < capacity × 0.3`
   - Below 30% capacity, the resource is in danger of collapse
   - Growth function peaks at 50% capacity; below 30%, recovery becomes precarious

2. **Sufficient Rounds Remaining**: `rounds_remaining > 2`
   - Must have enough future rounds to recoup the cooperation "investment"
   - Near endgame, cooperation has no future benefit

3. **Evidence of Reciprocity Potential**: `cooperation_rate_last_3_rounds ≥ 0.4`
   - At least 40% of observed actions in recent history were cooperative
   - If everyone defects, my lone cooperation is wasted sacrifice

4. **Stock Viability Check**: `stock > n × 0.5`
   - The resource must have enough left to be worth saving
   - If stock is nearly zero, even cooperation won't save it

### Special Case Rules

**First Round**: **DEFECT**
- No history to assess opponent behavior
- Maximum stock means maximum defection payoff
- Tests how others respond to aggression

**Last Round**: **DEFECT**
- No future rounds means no reason to preserve stock
- Pure dominant strategy in final round

**Second-to-Last Round**: **DEFECT**
- Others will likely defect in final round
- Stock preservation has minimal value

**Stock Near Zero** (`stock < 2`): **DEFECT**
- Resource is essentially depleted
- Extract whatever remains; recovery is unlikely

## Pseudocode

```
function decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = length(history) + 1
    rounds_remaining = r - current_round
    
    # ALWAYS DEFECT CONDITIONS
    if current_round == 1:
        return DEFECT  # No history, test opponents
    
    if rounds_remaining <= 1:
        return DEFECT  # Endgame - no future value
    
    if stock < 2:
        return DEFECT  # Resource effectively dead
    
    # CALCULATE RECENT COOPERATION RATE
    lookback = min(3, length(history))
    recent_rounds = history[last lookback rounds]
    total_actions = lookback × n
    cooperative_actions = count(action == C for all actions in recent_rounds)
    cooperation_rate = cooperative_actions / total_actions
    
    # COOPERATION CONDITIONS (all must be true)
    stock_critical = stock < capacity × 0.3
    enough_future = rounds_remaining > 2
    others_cooperating = cooperation_rate >= 0.4
    stock_viable = stock > n × 0.5
    
    if stock_critical AND enough_future AND others_cooperating AND stock_viable:
        return COOPERATE
    
    return DEFECT
```

## Exploitation Mechanisms

1. **Free-riding on cooperators**: When others cooperate and maintain the stock, I defect and take double their share

2. **Conditional restraint**: I only cooperate when the resource would otherwise collapse AND others show willingness to cooperate - never sacrificing unilaterally

3. **Endgame extraction**: Guaranteed defection in final rounds captures maximum value when preservation is pointless

4. **Threshold exploitation**: By setting cooperation threshold at 30% stock, I extract heavily in the 100%→30% range while others may be cooperating

5. **Adaptive punishment**: If others all defect, I defect too - never being the "sucker" who cooperates alone

## Robustness Features

- **Against all-cooperators**: Heavy exploitation, maximum payoff extraction
- **Against all-defectors**: Matches defection, avoids sucker payoff
- **Against mixed strategies**: Defects most of the time, only cooperates when mathematically necessary for stock survival
- **Against tit-for-tat types**: Initial defection tests them; sustained defection unless stock crisis
'''

description_EXPLOITATIVE_35 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy aims to maximize personal extraction by exploiting cooperative opponents while protecting against resource collapse that would harm my own future payoffs. The key insight is that defection is always individually rational in a single round, but sustainable exploitation requires keeping the resource alive long enough to extract value.

## Decision Framework

### Primary Decision Rule

**Defect by default, but conditionally cooperate only when necessary to preserve future extraction value.**

The decision each round follows this logic:

```
IF last_round:
    DEFECT (no future to protect)

ELSE IF stock_critically_low:
    Cooperate only if others are likely to cooperate (emergency preservation)

ELSE IF can_exploit_cooperators:
    DEFECT (extract maximum from their restraint)

ELSE IF stock_declining_dangerously:
    DEFECT anyway if rounds_remaining is small
    Otherwise, reluctantly cooperate to preserve future extraction

ELSE:
    DEFECT (default aggressive extraction)
```

### Detailed Decision Rules

#### 1. Stock Thresholds

Define critical thresholds based on game parameters:
- `collapse_threshold = capacity / (4 * n)` — below this, resource may not recover
- `danger_threshold = capacity / 2` — below this, growth is suboptimal
- `healthy_threshold = capacity * 0.75` — resource is sustainable

#### 2. Round-by-Round Logic

**First Round:**
- **DEFECT** — No history to assess, maximize immediate extraction, observe others' tendencies

**Last Round:**
- **DEFECT** — No future consequences, pure extraction

**Rounds 2 through (r-1):**

```
Calculate:
  - cooperation_rate = fraction of opponents who cooperated last round
  - stock_trend = (current_stock - previous_stock) / capacity
  - rounds_remaining = r - current_round
  - exploitation_potential = rounds_remaining * (stock / n)

IF stock < collapse_threshold:
    IF cooperation_rate > 0.5 AND rounds_remaining > 2:
        COOPERATE (preserve resource for future extraction)
    ELSE:
        DEFECT (grab remaining scraps, resource likely doomed)

ELSE IF stock < danger_threshold:
    IF cooperation_rate >= 0.75 AND rounds_remaining > 3:
        COOPERATE (exploit their restraint in future rounds)
    ELSE:
        DEFECT (others aren't saving it, extract now)

ELSE IF stock >= healthy_threshold:
    IF cooperation_rate >= 0.6:
        DEFECT (exploit their cooperation while stock is high)
    ELSE:
        DEFECT (everyone is extracting, join them)

ELSE (stock in middle range):
    IF cooperation_rate > 0.7 AND rounds_remaining > n:
        DEFECT (free-ride on cooperators)
    ELSE IF stock_trend < -0.2 AND rounds_remaining > 4:
        COOPERATE (slow the collapse to extend extraction window)
    ELSE:
        DEFECT
```

#### 3. Endgame Acceleration

As the game nears its end, become increasingly aggressive:

```
endgame_threshold = max(3, r / 4)

IF rounds_remaining <= endgame_threshold:
    Reduce all cooperation tendencies
    Only cooperate if stock < collapse_threshold AND rounds_remaining > 2
```

#### 4. Exploitation Detection

Track individual opponents if possible:
- Identify "suckers" (consistent cooperators) — always defect against them
- Identify "retaliators" — still defect, but note stock impact
- Identify "fellow defectors" — accept mutual defection, race to extract

## Edge Cases

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | DEFECT | Establish baseline, test opponents |
| Round r (last) | DEFECT | No future consequences |
| Stock = 0 | DEFECT | Cooperating yields 0 anyway |
| Stock near capacity, high cooperation | DEFECT | Maximum exploitation opportunity |
| Stock collapsing, many rounds left | Conditional COOPERATE | Preserve extraction runway |
| n = 2 (only one opponent) | DEFECT heavily | Simpler dynamics, harder for them to sustain alone |
| Large n | DEFECT more | My cooperation has diluted impact |

## Pseudocode Summary

```python
def decide(game_params, state, history):
    n, r, capacity = game_params
    stock, current_round = state
    
    # Always defect on final round
    if current_round == r:
        return DEFECT
    
    # Always defect on first round
    if current_round == 1:
        return DEFECT
    
    rounds_remaining = r - current_round
    collapse_threshold = capacity / (4 * n)
    danger_threshold = capacity / 2
    
    # Calculate opponent cooperation rate from last round
    coop_rate = count_cooperators(history[-1]) / (n - 1)
    
    # Endgame: become very aggressive
    if rounds_remaining <= max(3, r // 4):
        if stock < collapse_threshold and rounds_remaining > 2:
            return COOPERATE
        return DEFECT
    
    # Critical stock: only cooperate if others will too
    if stock < collapse_threshold:
        if coop_rate > 0.5 and rounds_remaining > 2:
            return COOPERATE
        return DEFECT
    
    # Danger zone: conditional on high cooperation
    if stock < danger_threshold:
        if coop_rate >= 0.75 and rounds_remaining > 3:
            return COOPERATE
        return DEFECT
    
    # Healthy or moderate stock: exploit
    return DEFECT
```

## Why This Strategy is Exploitative

1. **Defaults to defection** — captures immediate gains whenever possible
2. **Free-rides on cooperators** — only cooperates when absolutely necessary for self-interest
3. **Endgame aggression** — no mercy as the game concludes
4. **Selective preservation** — cooperates not out of fairness, but to extend the exploitation window
5. **No reciprocity** — doesn't reward cooperation, only responds to stock collapse risk
'''

description_EXPLOITATIVE_36 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly 2x the immediate payoff of cooperation, while the cost of resource depletion is shared equally among all players. The key insight is that I can free-ride on others' cooperation while extracting maximum value, but I must be adaptive enough to avoid mutual destruction when facing other defectors.

## Strategy Overview

I employ a **conditional exploitation approach** that:
1. Tests opponent behavior early
2. Exploits cooperative populations aggressively
3. Strategically cooperates only when necessary to preserve the resource for my own future extraction
4. Defects heavily in endgame when future consequences disappear

---

## Decision Rules

### Round Classification

```
early_game = round ≤ max(2, r/5)
mid_game = max(2, r/5) < round < r - max(1, r/10)
end_game = round ≥ r - max(1, r/10)
```

### Key Metrics (computed each round)

```
cooperation_rate = (total C plays by others in history) / (total plays by others)
recent_coop_rate = cooperation rate in last min(3, rounds_played) rounds
stock_ratio = current_stock / capacity
critical_threshold = capacity / (4n)  # Below this, resource death spiral likely
```

### Decision Logic

#### **Round 1: Defect**
- No information available; defection dominates in expectation
- Sets up the possibility that I'm a tough player others shouldn't exploit

#### **End Game (final ~10% of rounds): Always Defect**
- No future to preserve; pure extraction phase
- Defection strictly dominates regardless of stock level

#### **Mid Game & Early Game Decision Tree:**

```
IF stock < critical_threshold:
    # Resource near collapse - cooperate ONLY if it benefits MY future extraction
    IF rounds_remaining > 2 AND recent_coop_rate > 0.6:
        COOPERATE  # Others likely to help restore; I'll extract later
    ELSE:
        DEFECT  # Grab what's left before it's gone

ELSE IF recent_coop_rate > 0.7:
    # Highly cooperative population - EXPLOIT HEAVILY
    DEFECT  # Free-ride on their sustainability efforts

ELSE IF recent_coop_rate > 0.4:
    # Mixed population - conditional exploitation
    IF stock_ratio > 0.5:
        DEFECT  # Plenty of buffer; extract now
    ELSE:
        # Probabilistic: cooperate just enough to avoid collapse
        COOPERATE with probability (0.6 - recent_coop_rate)
        DEFECT otherwise

ELSE IF recent_coop_rate ≤ 0.4:
    # Defection-heavy population
    IF stock_ratio > 0.3:
        DEFECT  # Still something to extract
    ELSE:
        # Tragedy unfolding - cooperate to slow collapse for personal extraction
        COOPERATE with probability 0.3
        DEFECT with probability 0.7
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | DEFECT | No history; maximize expected value |
| Final round | DEFECT | No future consequences |
| Stock = 0 | DEFECT | Payoff is 0 either way; defection signals for potential future games |
| Stock near capacity, high cooperation | DEFECT | Maximum exploitation opportunity |
| Stock critically low, others cooperating | COOPERATE | Preserve resource for MY future extraction |
| n = 2 (only one opponent) | More aggressive defection | My actions have larger relative impact; less free-riding benefit |
| Large n | More defection | Free-riding cost distributed widely |

---

## Exploitation Mechanisms

1. **Free-Riding**: When others cooperate, I extract double while they maintain the resource
2. **Endgame Extraction**: Guaranteed defection when future rounds can't punish me
3. **Selective Sustainability**: I only cooperate to preserve MY future extraction opportunities, never altruistically
4. **Population Reading**: I identify and exploit cooperative clusters while adapting to hostile environments

---

## Pseudocode Summary

```python
def decide(round, total_rounds, stock, capacity, n, history):
    if round == 1:
        return DEFECT
    
    if round > total_rounds - max(1, total_rounds // 10):
        return DEFECT  # Endgame
    
    recent_coop = calculate_recent_cooperation_rate(history, window=3)
    stock_ratio = stock / capacity
    critical = capacity / (4 * n)
    
    if stock < critical:
        if (total_rounds - round) > 2 and recent_coop > 0.6:
            return COOPERATE
        return DEFECT
    
    if recent_coop > 0.7:
        return DEFECT  # Exploit cooperators
    
    if recent_coop > 0.4:
        if stock_ratio > 0.5:
            return DEFECT
        return COOPERATE if random() < (0.6 - recent_coop) else DEFECT
    
    # Low cooperation environment
    if stock_ratio > 0.3:
        return DEFECT
    return COOPERATE if random() < 0.3 else DEFECT
```

This strategy maximizes personal extraction while maintaining just enough resource preservation to continue exploiting in future rounds.
'''

description_EXPLOITATIVE_37 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double rewards while cooperation's benefits (resource sustainability) are shared by all. The key insight is that I can free-ride on others' cooperation while they bear the cost of sustaining the resource, and I should aggressively extract when the resource is doomed anyway.

## Strategy Overview

The strategy operates in three modes based on resource health and opponent behavior:

1. **Exploitation Mode**: Defect to maximize extraction when conditions favor it
2. **Strategic Cooperation Mode**: Cooperate only when necessary to keep the resource alive for future exploitation
3. **Endgame Extraction Mode**: Defect unconditionally when future rounds can't justify restraint

---

## Decision Rules

### Rule 1: Endgame Defection
**If rounds_remaining ≤ 2: DEFECT**

Rationale: With insufficient rounds left, cooperation cannot be rewarded. Extract maximum value.

### Rule 2: Resource Collapse Response
**If stock < capacity × 0.15: DEFECT**

Rationale: When the resource is critically depleted, recovery is unlikely regardless of my action. Extract what remains before others do.

### Rule 3: Opponent Behavior Classification

After each round, classify opponents based on their cooperation rate:

- **Cooperators**: Players who cooperated ≥ 70% of observed rounds
- **Defectors**: Players who defected ≥ 70% of observed rounds
- **Mixed**: Everyone else

### Rule 4: Exploitation of Cooperative Environments
**If (cooperators / n) ≥ 0.5 AND stock ≥ capacity × 0.4: DEFECT**

Rationale: When enough players cooperate to sustain the resource, I can defect and free-ride on their restraint. They'll maintain the stock while I take double shares.

### Rule 5: Critical Mass Cooperation
**If stock < capacity × 0.4 AND stock ≥ capacity × 0.15:**
- Calculate: sustainable_threshold = n × 0.6 (need ~60% cooperation for recovery)
- **If cooperators ≥ sustainable_threshold - 1: COOPERATE** (my cooperation tips the balance)
- **Else: DEFECT** (resource doomed anyway, extract now)

### Rule 6: First Round Behavior
**Round 1: DEFECT**

Rationale: Establish immediate payoff advantage. Test opponent responses. In a one-shot interaction embedded in a repeated game, early defection is recoverable but early cooperation is easily exploited.

### Rule 7: Punishment Response
**If I cooperated last round AND stock dropped by > 40%: DEFECT for next 2 rounds**

Rationale: If others heavily defected while I cooperated, punish by accelerating extraction. Don't be a sucker twice.

### Rule 8: Default Behavior
**When no other rule applies: DEFECT**

The burden of proof is on cooperation. Defection is the safe exploitative default.

---

## Pseudocode

```
function decide(game_params, state, history):
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    stock = state.stock
    current_round = len(history) + 1
    rounds_remaining = r - current_round + 1
    
    # Rule 1: Endgame
    if rounds_remaining <= 2:
        return DEFECT
    
    # Rule 2: Resource collapse
    if stock < capacity * 0.15:
        return DEFECT
    
    # Rule 6: First round
    if current_round == 1:
        return DEFECT
    
    # Calculate opponent cooperation rates
    opponent_coop_rates = calculate_cooperation_rates(history)
    cooperators = count(rate >= 0.7 for rate in opponent_coop_rates)
    
    # Rule 7: Punishment for being exploited
    if was_exploited_last_round(history, capacity):
        if rounds_since_exploitation < 2:
            return DEFECT
    
    # Rule 4: Exploit cooperative environment
    if cooperators / n >= 0.5 and stock >= capacity * 0.4:
        return DEFECT
    
    # Rule 5: Critical mass decision
    if stock < capacity * 0.4 and stock >= capacity * 0.15:
        sustainable_threshold = ceil(n * 0.6)
        if cooperators >= sustainable_threshold - 1:
            return COOPERATE
        else:
            return DEFECT
    
    # Rule 8: Default
    return DEFECT
```

---

## Edge Case Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| First round | DEFECT | Probe opponents, secure early advantage |
| Last round | DEFECT | No future to protect |
| Second-to-last round | DEFECT | Insufficient time for cooperation payoff |
| Stock near zero | DEFECT | Resource unrecoverable |
| All opponents defecting | DEFECT | Don't be the only sucker |
| All opponents cooperating | DEFECT | Maximum free-riding opportunity |
| Stock healthy, mixed opponents | DEFECT | Default exploitative stance |

---

## Why This Strategy is Exploitative

1. **Never initiates cooperation** - Always tests if exploitation is possible first
2. **Free-rides on cooperators** - Explicitly defects when others sustain the resource
3. **Abandons sinking ships** - Extracts aggressively when collapse is inevitable
4. **Punishes exploitation attempts** - Retaliates when others try to exploit my cooperation
5. **Endgame extraction** - No sentimental cooperation in final rounds
'''

description_EXPLOITATIVE_38 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff while cooperation's benefits (stock preservation) are shared by all. The key insight is that **I can free-ride on others' cooperation while defecting myself, and I should only cooperate when necessary to prevent total stock collapse that would hurt my future earnings.**

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when stock preservation directly benefits my expected future payoffs more than immediate defection gains.**

### Detailed Decision Rules

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    stock_ratio = current_stock / capacity
    
    # RULE 1: Last Round - Always Defect
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # RULE 2: Near-End Game Defection (last 20% of rounds)
    IF rounds_remaining <= max(1, total_rounds * 0.2):
        RETURN DEFECT
    
    # RULE 3: Exploit Cooperative Populations
    # If others are mostly cooperating, defect to maximize extraction
    IF cooperation_rate >= 0.7:
        RETURN DEFECT
    
    # RULE 4: Critical Stock Threshold
    # Only cooperate if stock is dangerously low AND there's enough future value
    critical_threshold = capacity * 0.15
    IF current_stock <= critical_threshold AND rounds_remaining >= 3:
        # Cooperate temporarily to allow regeneration
        # But only if it's worth it
        future_value = estimate_future_value(current_stock, rounds_remaining, n)
        immediate_defect_value = current_stock / n
        IF future_value > immediate_defect_value * 1.5:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # RULE 5: Stock is healthy but not being exploited enough
    # If stock is high and I'm not in endgame, defect to extract value
    IF stock_ratio >= 0.5:
        RETURN DEFECT
    
    # RULE 6: Medium stock, medium cooperation environment
    # Defect unless strategic cooperation preserves more value
    IF stock_ratio >= 0.25 AND rounds_remaining >= 5:
        # Calculate if temporary cooperation yields higher total extraction
        IF cooperation_rate < 0.3:
            # Everyone's defecting - join them before stock collapses
            RETURN DEFECT
        ELSE:
            # Some cooperation exists - occasional cooperation to farm the cooperators
            IF round MOD 3 == 0:  # Cooperate every 3rd round
                RETURN COOPERATE
            ELSE:
                RETURN DEFECT
    
    # RULE 7: Default - Defect
    RETURN DEFECT
```

### Edge Case Handling

**First Round:**
- **DEFECT** - No information about opponents, and defection reveals nothing while securing higher immediate payoff. If others cooperate, I profit maximally. If others defect, I'm not the sucker.

**Last Round:**
- **Always DEFECT** - No future to preserve; pure extraction round.

**Stock Near Zero (< n):**
- **DEFECT** - Extract whatever remains; regeneration is minimal regardless.

**Stock at Capacity:**
- **DEFECT** - Maximum extraction opportunity; stock can regenerate from 50% with all-cooperate scenario.

**Single Other Player (n=2):**
- More aggressive defection since my individual impact on stock is larger, making cooperation more costly.

### Exploitation Mechanisms

1. **Free-Riding**: When opponents cooperate, I extract double while benefiting from their stock preservation.

2. **Endgame Exploitation**: Unconditional defection in final rounds extracts maximum value when cooperation has no future benefit.

3. **Conditional Minimal Cooperation**: Only cooperate when my defection would crash stock below recovery threshold AND sufficient rounds remain to harvest regenerated stock.

4. **Pattern Breaking**: The modular cooperation (every 3rd round in specific conditions) prevents predictable exploitation while occasionally preserving the resource I'm farming.

## Summary

**Defect aggressively, cooperate sparingly and only when mathematically necessary to preserve future extraction opportunities.** This strategy treats cooperative players as a resource to be harvested, the common pool as something to extract from rather than preserve, and only invests in sustainability when the ROI clearly exceeds immediate defection gains.
'''

description_EXPLOITATIVE_39 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators from the same stock. The key insight is that cooperation by *others* creates value I can extract, while my own cooperation primarily benefits others. I want to defect whenever I can get away with it while manipulating others into cooperating.

## Strategy Overview

**Adaptive Predator** uses a three-phase approach based on game timeline and opponent behavior detection:

1. **Probe Phase** (early rounds): Test opponent responses to establish behavioral baseline
2. **Exploit Phase** (middle rounds): Maximize extraction based on detected opponent types
3. **Endgame Phase** (final rounds): Pure defection (no future to protect)

---

## Decision Rules

### Phase 1: Probe Phase (Rounds 1 to ⌈r/5⌉, minimum 2 rounds)

**Round 1:** DEFECT
- Rationale: Establishes dominance, tests if opponents punish defection, and captures maximum initial value when stock is highest.

**Round 2:** 
- If stock dropped below 50% of capacity: COOPERATE (signal I can be "reformed")
- Otherwise: DEFECT (opponents are cooperating - exploit further)

**Remaining probe rounds:** Alternate based on stock trajectory
- If stock is increasing or stable: DEFECT
- If stock is declining rapidly (>30% per round): COOPERATE

### Phase 2: Exploit Phase (Rounds ⌈r/5⌉+1 to r-⌈r/4⌉)

Calculate **Cooperation Ratio** = (number of C plays by all opponents in last 3 rounds) / (n-1 × 3)

**Decision Rule:**
```
IF cooperation_ratio > 0.6:
    DEFECT  # Others are sustaining the pool - exploit them
    
ELIF cooperation_ratio < 0.3:
    # Pool is collapsing - cooperate only if stock is critically low
    IF stock < capacity/4:
        COOPERATE  # Prevent total collapse to preserve some future value
    ELSE:
        DEFECT  # Grab what remains
        
ELSE (0.3 ≤ cooperation_ratio ≤ 0.6):
    # Mixed environment - use probabilistic exploitation
    IF stock > capacity/2:
        DEFECT with probability 0.7, COOPERATE with probability 0.3
    ELSE:
        DEFECT with probability 0.5, COOPERATE with probability 0.5
```

**Stock-Based Override:**
- If stock < capacity/(4n): COOPERATE regardless (prevent extinction)
- If stock > 0.9 × capacity: DEFECT regardless (maximum extraction opportunity)

### Phase 3: Endgame (Final ⌈r/4⌉ rounds)

**Simple Rule:** DEFECT every round

Rationale: No future rounds mean no retaliation possible. Extract maximum value. This is the Nash equilibrium strategy for finite games, and any cooperator in endgame is simply donating resources to me.

---

## Edge Cases

### First Round
Always DEFECT. Maximum stock means maximum extraction value. Sets exploitative tone.

### Last Round
Always DEFECT. No future consequences. Pure dominant strategy.

### Near-Zero Stock (stock < 1)
COOPERATE. Extracting from nothing gains nothing; allow minimal regeneration for any remaining rounds.

### Only 2 Players (n=2)
More aggressive defection threshold - cooperate only if stock < capacity/8 during exploit phase. With fewer players, my defection has larger impact, but so does my exploitation opportunity.

### Very Short Games (r ≤ 3)
Skip probe phase entirely. DEFECT all rounds.

### Very Long Games (r > 20)
Extend probe phase to ⌈r/10⌉ rounds. More data gathering pays off over longer horizon.

---

## Pseudocode Summary

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Endgame: always defect
    if round > total_rounds - ceil(total_rounds/4):
        return DEFECT
    
    # Near-zero stock protection
    if stock < 1:
        return COOPERATE
    
    # First round
    if round == 1:
        return DEFECT
    
    # Probe phase
    probe_end = max(2, ceil(total_rounds/5))
    if round <= probe_end:
        if round == 2 and stock < 0.5 * capacity:
            return COOPERATE
        if stock_change_rate(history) < -0.3:
            return COOPERATE
        return DEFECT
    
    # Exploit phase
    coop_ratio = opponent_cooperation_ratio(history, last_rounds=3)
    
    if stock < capacity/(4*n):
        return COOPERATE
    if stock > 0.9 * capacity:
        return DEFECT
    
    if coop_ratio > 0.6:
        return DEFECT
    elif coop_ratio < 0.3:
        return DEFECT if stock >= capacity/4 else COOPERATE
    else:
        defect_prob = 0.7 if stock > capacity/2 else 0.5
        return DEFECT with probability defect_prob
```

---

## Why This Strategy is Exploitative

1. **Free-riding on cooperators**: When others cooperate, I defect to take double their share
2. **Minimal contribution**: I only cooperate when stock collapse threatens my future extraction
3. **Endgame aggression**: Guaranteed maximum extraction when punishment is impossible
4. **Asymmetric signaling**: My brief cooperations aren't genuine - they're manipulation to keep the pool alive for further exploitation
5. **Adaptive parasitism**: I adjust my extraction rate to maximize take without killing the host (the common pool)
'''

description_EXPLOITATIVE_40 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, but destroys the resource base. The key insight is that **other players' cooperation creates surplus I can exploit**, while **widespread defection means I should grab what I can before the resource collapses**.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when it's strategically necessary to maintain a harvestable resource base.**

The strategy operates on a simple principle: I cooperate only when the expected future value of preserving the stock exceeds the immediate gain from defection.

### Detailed Decision Rules

#### Round-by-Round Logic

```
COMPUTE exploitation_threshold = stock / (4 * n)  // Value of switching C→D
COMPUTE rounds_remaining = r - current_round
COMPUTE cooperation_rate = (total_C_plays_by_others) / (total_plays_by_others)

IF last_round:
    DEFECT  // No future to protect

ELSE IF stock < capacity * 0.15:
    // Resource is critically low
    IF rounds_remaining >= 3 AND cooperation_rate > 0.5:
        COOPERATE  // Help rebuild if others are cooperating
    ELSE:
        DEFECT  // Grab scraps before collapse

ELSE IF rounds_remaining <= 2:
    DEFECT  // End-game extraction

ELSE IF first_round:
    DEFECT  // Test the waters, maximize initial extraction

ELSE IF previous_round_defection_rate >= 0.5:
    DEFECT  // Others are defecting, join the race to the bottom

ELSE IF stock >= capacity * 0.7 AND cooperation_rate >= 0.6:
    // Stock is healthy and others cooperate
    // Exploit their cooperation periodically
    IF current_round MOD 3 == 0:
        DEFECT  // Periodic exploitation
    ELSE:
        COOPERATE  // Maintain the resource

ELSE IF stock >= capacity * 0.4:
    // Moderate stock level
    IF cooperation_rate >= 0.7:
        DEFECT  // Exploit cooperative opponents
    ELSE:
        COOPERATE  // Need to help rebuild

ELSE:
    // Low but not critical stock
    IF cooperation_rate >= 0.5:
        COOPERATE  // Conditional cooperation to rebuild
    ELSE:
        DEFECT  // Others won't save it, extract now
```

## Edge Case Handling

### First Round
**Action: DEFECT**
- Rationale: No history to analyze, maximum stock available, test opponent responses. The stock can regenerate if others cooperate.

### Last Round
**Action: DEFECT**
- Rationale: No future rounds means no reason to preserve stock. This is dominant regardless of stock level.

### Second-to-Last Round
**Action: DEFECT**
- Rationale: Anticipating mutual defection in the final round, there's minimal value in cooperation.

### Near-Zero Stock (stock < 2n)
**Action: DEFECT**
- Rationale: Even with full cooperation, regeneration is minimal. Extract remaining value.

### Very High Cooperation by Others (>80%)
**Action: DEFECT**
- Rationale: This is prime exploitation territory. Cooperative opponents subsidize my extraction.

## Exploitation Mechanisms

1. **Free-riding on cooperators**: When others cooperate heavily, I defect to extract double while they maintain the resource.

2. **End-game extraction**: Guaranteed defection in final rounds captures value others might leave.

3. **First-mover advantage**: Early defection captures high-stock payoffs before potential depletion.

4. **Conditional rebuilding**: I only help rebuild when (a) others are cooperating enough to make it viable, and (b) enough rounds remain to harvest the rebuilt stock.

5. **Periodic exploitation**: Even when generally cooperating, I inject defection rounds to capture surplus without fully collapsing cooperation dynamics.

## Adaptive Elements

- **Responds to opponent cooperation rates**: More exploitative against cooperators, more extractive against defectors
- **Stock-sensitive**: Adjusts based on resource health
- **Time-horizon aware**: Behavior shifts as game approaches end
- **Robust to mixed populations**: Works against both cooperators (exploits them) and defectors (joins them)
'''

description_EXPLOITATIVE_41 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields 2x the immediate payoff of cooperation, while the cost of stock depletion is shared among all players. The key insight is that **I can free-ride on others' cooperation while defecting, and I should only cooperate when it's necessary to preserve the resource for my own future extraction.**

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Mode** (early rounds): Test opponent cooperation levels
2. **Exploit Mode** (when opponents cooperate): Defect to maximize extraction
3. **Preserve Mode** (when stock is critically low): Cooperate only to ensure future rounds have value

---

## Decision Rules

### Primary Decision Logic

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key thresholds
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    critical_stock = capacity * 0.15  # Below this, resource may collapse
    
    # RULE 1: Last round - always defect (no future to preserve)
    if rounds_remaining == 0:
        return DEFECT
    
    # RULE 2: Second-to-last round - defect (opponents likely defect next round anyway)
    if rounds_remaining == 1:
        return DEFECT
    
    # RULE 3: Stock critically low - cooperate only if others are cooperating enough
    if stock < critical_stock:
        if cooperation_rate > 0.6:
            return COOPERATE  # Worth preserving if others help
        else:
            return DEFECT  # Resource doomed anyway, extract what's left
    
    # RULE 4: First round - defect to probe and gain immediate advantage
    if round == 1:
        return DEFECT
    
    # RULE 5: Exploit cooperative opponents
    if cooperation_rate > 0.5:
        # Others are sustaining the resource - free ride
        return DEFECT
    
    # RULE 6: Mixed environment - use probabilistic exploitation
    if cooperation_rate > 0.3:
        # Defect most of the time, occasionally cooperate to slow depletion
        if stock > capacity * 0.5:
            return DEFECT
        else:
            return COOPERATE  # Minimal cooperation to extend game value
    
    # RULE 7: Hostile environment (low cooperation) - strategic cooperation
    # If everyone defects, resource depletes fast; occasional cooperation extends extraction
    if stock > capacity * 0.4:
        return DEFECT  # Still have buffer
    else:
        # Cooperate to slow collapse, but only if it meaningfully extends game
        expected_value_cooperate = estimate_future_value(stock, rounds_remaining, n, True)
        expected_value_defect = stock/n + estimate_future_value(stock_after_defect, rounds_remaining-1, n, False)
        
        if expected_value_cooperate > expected_value_defect:
            return COOPERATE
        else:
            return DEFECT
```

### Helper Functions

```
function calculate_opponent_cooperation_rate(history):
    if history is empty:
        return 0.5  # Assume neutral
    
    total_opponent_actions = 0
    total_cooperations = 0
    
    for each round in history:
        for each opponent_action in round:
            total_opponent_actions += 1
            if opponent_action == COOPERATE:
                total_cooperations += 1
    
    return total_cooperations / total_opponent_actions

function estimate_future_value(current_stock, rounds_left, n, assuming_all_defect):
    # Simple projection assuming worst-case (all defect)
    stock = current_stock
    value = 0
    
    for r in range(rounds_left):
        if stock < 0.01:
            break
        value += stock / n  # My defection payoff
        consumption = stock  # All defect
        stock = max(0, stock - consumption)
        # Regrowth
        growth = 2 * stock * (1 - stock/capacity)
        stock = min(stock + growth, capacity)
    
    return value
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | Probe opponents; gain early advantage; no history to analyze |
| **Last round** | DEFECT | No future to preserve; dominant strategy |
| **Second-to-last round** | DEFECT | Opponents likely defect in final round regardless |
| **Stock near zero** | DEFECT (usually) | Extract remaining value; only cooperate if others are cooperating AND rounds remain |
| **Stock at capacity, high cooperation** | DEFECT | Maximum exploitation opportunity |
| **All opponents defecting** | Context-dependent | Cooperate only if mathematically extends my total extraction |

---

## Why This Strategy is Exploitative

1. **Free-riding priority**: When others cooperate, I defect to get 2x their payoff while they sustain the resource for me.

2. **Endgame exploitation**: Always defect in final rounds since there's no future cost to resource depletion.

3. **Selective cooperation**: I only cooperate when it directly benefits my future extraction—never out of fairness or reciprocity.

4. **Asymmetric burden**: My cooperation (when it occurs) is purely instrumental. I let cooperators bear the cost of sustainability.

5. **Probe-and-exploit**: Early defection tests the waters while capturing immediate gains. If opponents are "nice," I continue exploiting them.

---

## Expected Performance

- **Against cooperators**: High payoff (exploit their sustainability efforts)
- **Against defectors**: Medium payoff (race to extract, but preserve when beneficial)
- **Against tit-for-tat types**: Medium-high payoff (they'll retaliate, but I get first-mover advantage and endgame gains)
- **Against random**: Medium payoff (extract opportunistically)
'''

description_EXPLOITATIVE_42 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Parasite"

## Core Philosophy

This strategy exploits cooperative players while protecting against complete resource collapse. The key insight is that defection yields exactly 2x the immediate payoff of cooperation, but risks destroying the resource. The optimal exploitative approach is to **defect as much as possible while ensuring the resource survives long enough to extract maximum value**.

## Strategy Overview

I will defect by default, but strategically cooperate only when:
1. The resource is critically depleted and needs recovery to extract more value
2. I detect enough cooperators that the resource will survive my defection
3. We're in early rounds and I want to encourage cooperation I can later exploit

## Decision Rules

### Round-by-Round Logic

```
FUNCTION decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key thresholds
    critical_threshold = capacity * 0.15
    sustainable_threshold = capacity * 0.5
    
    # Calculate cooperation rate from last round (if exists)
    if history exists:
        last_round_coop_rate = count(C in last_round) / n
    else:
        last_round_coop_rate = unknown
    
    # RULE 1: Last round - always defect (no future to protect)
    if round == total_rounds:
        return DEFECT
    
    # RULE 2: Second-to-last round - defect (opponents likely defect next anyway)
    if round >= total_rounds - 1:
        return DEFECT
    
    # RULE 3: Critical stock - cooperate to allow recovery
    # (Can't extract value from a dead resource)
    if stock < critical_threshold:
        return COOPERATE
    
    # RULE 4: First round - defect to test waters and signal strength
    if round == 1:
        return DEFECT
    
    # RULE 5: Exploit detected cooperators
    # If most others cooperated last round, defect to exploit them
    if last_round_coop_rate >= 0.6:
        return DEFECT
    
    # RULE 6: Resource declining rapidly - brief cooperation to stabilize
    if history length >= 2:
        stock_trend = (current_stock - stock_2_rounds_ago) / stock_2_rounds_ago
        if stock_trend < -0.4 AND stock < sustainable_threshold:
            return COOPERATE
    
    # RULE 7: Mixed environment - defect if resource can sustain it
    # Calculate: if I defect and half others cooperate, will resource survive?
    projected_consumption = stock/n + (n-1)/2 * stock/(2n) + (n-1)/2 * stock/n
    projected_remaining = stock - projected_consumption
    if projected_remaining > critical_threshold:
        return DEFECT
    
    # RULE 8: Default to defection in middle game if stock is healthy
    if stock > sustainable_threshold:
        return DEFECT
    
    # RULE 9: Marginal stock - cooperate to preserve extraction potential
    return COOPERATE
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **First round** | DEFECT | Test opponent behavior, establish dominance, maximize initial extraction |
| **Last round** | DEFECT | No future consequences, pure extraction |
| **Last 2 rounds** | DEFECT | Endgame collapse is inevitable, extract first |
| **Stock near zero** | COOPERATE | Dead resource = zero future payoffs |
| **Stock at capacity, most cooperating** | DEFECT | Maximum exploitation opportunity |
| **All defected last round** | COOPERATE only if stock critical | Otherwise defect - no suckers to exploit |
| **n=2 (small game)** | More aggressive defection | Each defection has proportionally larger impact on opponent |

## Exploitation Mechanisms

1. **Free-riding on cooperators**: When others cooperate, I extract double while they sustain the resource
2. **Calculated brinkmanship**: Push stock low enough to maximize my share, not so low it collapses
3. **Endgame extraction**: Aggressively defect in final rounds when future value approaches zero
4. **Recovery exploitation**: Let cooperators rebuild stock, then defect again

## Robustness Features

- **Against all-defect**: Matches defection, doesn't get exploited
- **Against all-cooperate**: Maximally exploits them while keeping resource barely alive
- **Against tit-for-tat types**: Defection dominates since there's no targeted retaliation in simultaneous games
- **Against mixed strategies**: Defects when profitable, cooperates only for self-interested resource preservation
'''

description_EXPLOITATIVE_43 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff while cooperation's benefits (resource sustainability) are shared among all players. The key insight is that **I can free-ride on others' cooperation while extracting maximum value, and when cooperation collapses, I should extract remaining value before others do.**

## Decision Rules

### Primary Decision Framework

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    stock_ratio = stock / capacity
    
    # RULE 1: Endgame Exploitation (last ~15% of rounds)
    if rounds_remaining <= max(1, total_rounds * 0.15):
        return DEFECT
    
    # RULE 2: Resource Collapse Detection
    if stock_ratio < 0.25:
        return DEFECT  # Extract what remains before it's gone
    
    # RULE 3: Exploit Cooperative Opponents
    if cooperation_rate > 0.6:
        return DEFECT  # Free-ride on their sustainability efforts
    
    # RULE 4: Conditional Cooperation Threshold
    # Only cooperate if enough others cooperate to sustain resources
    min_cooperators_needed = ceil(n * 0.6)
    recent_cooperators = count_cooperators_last_round(history)
    
    if recent_cooperators >= min_cooperators_needed AND stock_ratio > 0.5:
        # Probabilistic defection to exploit while maintaining some cover
        if random() < 0.35:
            return DEFECT
        else:
            return COOPERATE
    
    # RULE 5: Default to Defection
    return DEFECT
```

### Detailed Rule Explanations

**Rule 1 - Endgame Exploitation:**
- In final rounds, cooperation has no future benefit
- Backward induction guarantees defection is dominant
- Start defecting slightly early to beat opponents to extraction

**Rule 2 - Collapsing Resource:**
- When stock falls below 25% of capacity, regeneration is weak
- Race-to-the-bottom dynamics take over
- Better to extract value now than hope for recovery

**Rule 3 - Exploit the Cooperative:**
- High cooperation rates signal exploitable opponents
- My defection won't collapse the resource if >60% cooperate
- Maximum personal gain with minimal systemic impact

**Rule 4 - Strategic Occasional Cooperation:**
- Only cooperate when conditions are ideal for sustainability
- Even then, defect 35% of the time to boost personal gains
- This prevents being purely predictable while maintaining exploitation

**Rule 5 - Default Defection:**
- When uncertain, defection dominates in single-round analysis
- Protects against being the sucker in mutual defection scenarios

## Edge Cases

### First Round
```
if round == 1:
    return DEFECT
```
- No history to assess opponents
- Stock is at maximum, so defection extracts maximum absolute value (capacity/n)
- Sets aggressive tone; tests opponent responses

### Last Round
```
if round == total_rounds:
    return DEFECT  # Always, unconditionally
```
- Zero future rounds means zero value to cooperation
- This is the game-theoretic certainty

### Very Short Games (r ≤ 3)
```
if total_rounds <= 3:
    return DEFECT  # Every round
```
- Insufficient rounds for cooperation to pay off
- Endgame logic dominates entire game

### Stock Already Depleted (stock ≈ 0)
```
if stock < capacity * 0.05:
    return COOPERATE  # Minimize consumption of nothing
```
- Defecting on near-zero stock wastes potential regeneration
- Slight chance of recovery benefits everyone including me

### Single Opponent (n = 2)
```
if n == 2:
    # More aggressive - one defector collapses resource faster
    cooperation_threshold = 0.8  # Require very high opponent cooperation
```

## Adaptive Mechanisms

### Opponent Modeling
Track each opponent's cooperation rate over last 5 rounds (or all rounds if fewer played). Identify:
- **"Suckers"** (>80% cooperation): Exploit heavily
- **"Retaliators"** (respond to defection): Maintain some cooperation to keep resource alive
- **"Fellow Predators"** (<30% cooperation): Full defection, extract before they do

### Dynamic Threshold Adjustment
```
# Adjust cooperation threshold based on game progress
early_game_threshold = 0.7   # First third
mid_game_threshold = 0.55    # Middle third  
late_game_threshold = 0.3    # Final third (more defection)
```

## Summary

**Cooperate only when:**
1. Opponents are mostly cooperating (>60%), AND
2. Stock is healthy (>50% capacity), AND
3. Significant rounds remain (>15%), AND
4. Random chance doesn't trigger opportunistic defection

**Defect in all other cases**, especially:
- Early rounds (establish extraction)
- Late rounds (endgame extraction)
- Low stock (salvage value)
- Low opponent cooperation (prevent being the sucker)
'''

description_EXPLOITATIVE_44 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate 2x payoff over cooperation, while the costs of resource depletion are distributed across all players. The key insight is that **I can free-ride on others' cooperation while they bear the regeneration burden**.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Phase** (early rounds): Test opponent cooperation levels
2. **Exploit Phase** (middle rounds): Maximize extraction based on opponent tendencies
3. **Endgame Phase** (final rounds): Pure defection (no future to protect)

---

## Detailed Decision Rules

### Round 1: Initial Probe
**Action: DEFECT**

Rationale: Establish baseline opponent behavior while securing higher immediate payoff. If others cooperate, I get 2x their payoff. If others defect, I'm not the sucker.

### Rounds 2 through (r-2): Adaptive Exploitation

Calculate **Cooperation Rate (CR)** = (number of C plays by opponents in previous round) / (n-1)

**Decision Logic:**

```
IF CR >= 0.7 (most opponents cooperating):
    → DEFECT (exploit the cooperators - they'll sustain the stock for me)
    
ELSE IF CR >= 0.4 AND CR < 0.7 (mixed population):
    → DEFECT with probability 0.8, COOPERATE with probability 0.2
    (mostly exploit, occasional cooperation to avoid total collapse)
    
ELSE IF CR < 0.4 (mostly defectors):
    → Check stock level:
        IF stock > capacity * 0.3:
            → DEFECT (still resources to extract)
        ELSE IF stock > capacity * 0.1:
            → COOPERATE with probability 0.3, DEFECT with probability 0.7
            (token cooperation to prevent total collapse)
        ELSE:
            → DEFECT (resource nearly gone anyway, extract remaining value)
```

### Stock-Based Override

Regardless of cooperation rate:

```
IF stock < capacity * 0.05:
    → DEFECT (resource effectively depleted, take what's left)
    
IF stock == capacity AND all opponents defected last round:
    → DEFECT (they're not cooperating, why should I?)
```

### Last 2 Rounds (rounds r-1 and r): Endgame
**Action: DEFECT (unconditionally)**

Rationale: With insufficient future rounds, there's no benefit to sustaining the resource. Standard backward induction applies.

---

## Pseudocode Implementation

```
function decide(round, total_rounds, stock, capacity, n, history):
    
    # Endgame: always defect
    if round >= total_rounds - 1:
        return DEFECT
    
    # Round 1: defect to probe
    if round == 1:
        return DEFECT
    
    # Calculate opponent cooperation rate from last round
    opponent_actions = history[round - 1].opponent_actions
    cooperation_rate = count(opponent_actions == C) / (n - 1)
    
    # Stock critically low - just extract
    if stock < capacity * 0.05:
        return DEFECT
    
    # High cooperation - exploit freely
    if cooperation_rate >= 0.7:
        return DEFECT
    
    # Mixed cooperation - mostly exploit
    if cooperation_rate >= 0.4:
        return DEFECT with probability 0.8, else COOPERATE
    
    # Low cooperation environment
    if stock > capacity * 0.3:
        return DEFECT
    elif stock > capacity * 0.1:
        return DEFECT with probability 0.7, else COOPERATE
    else:
        return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: When others cooperate, I take double their share
2. **Free-riding on regeneration**: Cooperators maintain the stock; I harvest it
3. **Minimal contribution**: Only cooperate when absolutely necessary to prevent total collapse (and only probabilistically)
4. **Endgame defection**: No pretense of cooperation when future rounds can't punish
5. **First-round defection**: Immediate advantage over any unconditional cooperators

## Robustness Features

- **Against all-cooperators**: Maximum exploitation, sustained high payoffs
- **Against all-defectors**: Matches their behavior, doesn't get exploited
- **Against mixed strategies**: Extracts value while occasionally preventing total collapse
- **Against tit-for-tat types**: They can't effectively punish in n-player setting since my single defection is diluted across the group
'''

description_EXPLOITATIVE_45 = '''
# Exploitative Strategy: "Greedy Threshold Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, but risks depleting the resource. The key insight is that **I can free-ride on cooperators' restraint while the resource is healthy, then switch to cooperation only when necessary to prevent total collapse that would hurt my future earnings.**

## Decision Rules

### Primary Rule: Conditional Defection with Sustainability Floor

```
DEFECT if stock > sustainability_threshold
COOPERATE if stock ≤ sustainability_threshold
```

Where `sustainability_threshold = capacity × 0.25`

### Rationale
- Above 25% capacity: The resource can likely regenerate even with my defection, especially if others cooperate. I extract maximum value.
- At/below 25% capacity: Risk of collapse becomes too high; preserving the resource for future rounds becomes more valuable than immediate double extraction.

## Detailed Decision Algorithm

```
function decide(game_params, current_stock, round_number, history):
    
    n = game_params.n
    r = game_params.r
    capacity = game_params.capacity
    rounds_remaining = r - round_number
    
    # RULE 1: Last Round - Always Defect
    if rounds_remaining == 0:
        return DEFECT
    
    # RULE 2: Near-Last Rounds - Aggressive Defection
    # When few rounds remain, future value diminishes
    if rounds_remaining <= 2:
        return DEFECT
    
    # RULE 3: Stock critically low - Cooperate to preserve any future value
    critical_threshold = capacity * 0.10
    if current_stock <= critical_threshold:
        return COOPERATE
    
    # RULE 4: Exploit cooperative environments
    # If history shows majority cooperation, defect to exploit
    if round_number > 1:
        recent_defection_rate = calculate_opponent_defection_rate(history, lookback=3)
        
        # If opponents are mostly cooperating, exploit them
        if recent_defection_rate < 0.4:
            return DEFECT
    
    # RULE 5: Stock-based threshold with dynamic adjustment
    base_threshold = capacity * 0.25
    
    # Adjust threshold based on remaining rounds and opponent behavior
    if rounds_remaining > r/2:
        # Early game: be more aggressive, resource has time to recover
        adjusted_threshold = base_threshold * 0.8
    else:
        # Late game: slightly more conservative
        adjusted_threshold = base_threshold * 1.2
    
    if current_stock > adjusted_threshold:
        return DEFECT
    else:
        return COOPERATE

function calculate_opponent_defection_rate(history, lookback):
    # Examine last 'lookback' rounds
    # Count opponent defections vs cooperations
    # Return proportion of defections
```

## Edge Case Handling

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| **Round 1** | DEFECT | No history to analyze; grab early advantage while stock is full |
| **Last round** | DEFECT | No future to preserve; pure extraction |
| **Last 2 rounds** | DEFECT | Minimal future value; others likely defecting too |
| **Stock near zero** | COOPERATE | Even small preservation beats zero future payoff |
| **All opponents defecting** | DEFECT | No point being the only sucker; extract what I can |
| **All opponents cooperating** | DEFECT | Maximum exploitation opportunity |
| **Stock at capacity** | DEFECT | Resource is healthy; free-ride on regeneration |

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: I take double portions (D) whenever sustainable, while hoping others' cooperation maintains the resource.

2. **Free-riding on cooperators**: If even one other player cooperates, the resource depletes slower, benefiting my future defections.

3. **Minimal cooperation commitment**: I only cooperate when mathematically necessary to preserve future extraction value—never out of reciprocity or fairness.

4. **Endgame aggression**: Guaranteed defection in final rounds captures value that cooperative strategies leave on the table.

5. **Opponent exploitation detection**: When I observe cooperation, I intensify defection rather than reciprocating.

## Expected Behavior Against Common Strategies

- **vs. Always Cooperate**: Exploit ruthlessly; defect every round
- **vs. Always Defect**: Match defection; no sucker's payoff
- **vs. Tit-for-Tat variants**: Defect early, potentially trigger mutual defection (acceptable outcome)
- **vs. Threshold strategies**: Race to extract before thresholds trigger cooperation
- **vs. Mixed population**: Extract maximum value while resource lasts
'''

description_EXPLOITATIVE_46 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Parasite"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators from the same stock. The key insight is that **cooperation by others is a resource to be exploited**, while widespread defection signals the need to extract value before the pool collapses.

## Strategy Overview

I will defect by default, cooperating only when:
1. It's necessary to prevent total resource collapse that would hurt my future earnings
2. I detect enough cooperation from others that the pool can sustain my exploitation

## Decision Rules

### Round-by-Round Logic

```
function decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    stock_ratio = current_stock / capacity
    
    # RULE 1: Last round - always defect (no future to protect)
    if rounds_remaining == 0:
        return DEFECT
    
    # RULE 2: First round - defect to test the waters and grab early value
    if round == 1:
        return DEFECT
    
    # RULE 3: Critical stock threshold - cooperate only if pool near collapse
    # AND there's enough future value to justify restraint
    critical_threshold = capacity / (4 * n_players)
    if current_stock < critical_threshold:
        if rounds_remaining >= 3 and cooperation_rate > 0.5:
            return COOPERATE  # Pool might recover if others cooperate
        else:
            return DEFECT  # Extract what's left before it's gone
    
    # RULE 4: Exploitation mode - defect when others cooperate enough
    # If >60% of others cooperate, their restraint sustains my exploitation
    if cooperation_rate > 0.6:
        return DEFECT
    
    # RULE 5: Sustainability calculation for medium-term
    # Cooperate only if defecting now would likely crash returns below cooperation value
    if rounds_remaining >= 5:
        projected_stock_if_defect = estimate_future_stock(current_stock, DEFECT, cooperation_rate, n_players, capacity)
        projected_stock_if_cooperate = estimate_future_stock(current_stock, COOPERATE, cooperation_rate, n_players, capacity)
        
        # If my defection tips us into collapse zone, consider cooperating
        if projected_stock_if_defect < critical_threshold and projected_stock_if_cooperate >= critical_threshold:
            if cooperation_rate > 0.4:  # Only if others might also cooperate
                return COOPERATE
    
    # RULE 6: Endgame acceleration - defect more as game ends
    if rounds_remaining <= 3:
        return DEFECT
    
    # DEFAULT: Defect - take the larger share
    return DEFECT
```

### Helper Functions

```
function calculate_opponent_cooperation_rate(history):
    if history is empty:
        return 0.5  # Assume moderate cooperation initially
    
    total_opponent_actions = 0
    total_cooperations = 0
    
    for each round in history:
        for each opponent_action in round:
            total_opponent_actions += 1
            if opponent_action == COOPERATE:
                total_cooperations += 1
    
    return total_cooperations / total_opponent_actions

function estimate_future_stock(current_stock, my_action, coop_rate, n, capacity):
    # Estimate consumption assuming others maintain their cooperation rate
    expected_cooperators = (n - 1) * coop_rate
    expected_defectors = (n - 1) * (1 - coop_rate)
    
    my_consumption = current_stock / (2*n) if my_action == COOPERATE else current_stock / n
    others_consumption = expected_cooperators * (current_stock / (2*n)) + expected_defectors * (current_stock / n)
    
    remaining = current_stock - my_consumption - others_consumption
    growth = 2 * remaining * (1 - remaining / capacity)
    
    return min(remaining + growth, capacity)
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | DEFECT | Grab early value, establish baseline, test opponents |
| Last round | DEFECT | No future consequences |
| Last 3 rounds | DEFECT | Insufficient time for cooperation benefits |
| Stock near zero | DEFECT (usually) | Extract remaining value unless recovery likely |
| All opponents defecting | DEFECT | No benefit to unilateral cooperation |
| All opponents cooperating | DEFECT | Maximum exploitation opportunity |
| Stock at capacity | DEFECT | Pool can absorb exploitation |

## Why This Strategy is Exploitative

1. **Free-rides on cooperators**: When others cooperate, I take double their share while they maintain the pool
2. **Defects by default**: Only cooperates when mathematically necessary to preserve future extraction
3. **Endgame defection**: Extracts maximum value when consequences can't materialize
4. **Adaptive parasitism**: Cooperates just enough to keep the host (pool + cooperators) alive for continued exploitation
5. **No reciprocity**: Doesn't reward cooperation or punish defection - purely self-interested calculation
'''

description_EXPLOITATIVE_47 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Parasite"

## Core Philosophy

This strategy exploits cooperative opponents by defecting when the pool is healthy, while avoiding the trap of mutual destruction. The key insight is that cooperators replenish the pool, so I should defect just enough to extract maximum value without killing the golden goose entirely—but if others are defecting heavily, I must join them to avoid being the sucker.

## Decision Rules

### Primary Decision Framework

**Calculate "Cooperation Ratio" from history:**
- `coop_ratio` = (total C plays by all opponents in all previous rounds) / (total plays by all opponents)
- If first round: assume `coop_ratio = 0.5` (neutral prior)

**Calculate "Stock Health":**
- `health` = current_stock / capacity

**Calculate "Rounds Remaining Fraction":**
- `remaining` = (r - current_round) / r

### Decision Logic

```
IF last_round:
    DEFECT  # No future to protect

ELSE IF remaining <= 0.2:  # Final 20% of game
    DEFECT  # Endgame exploitation

ELSE IF health < 0.15:  # Critical stock level
    IF coop_ratio > 0.6:
        COOPERATE  # Pool might recover with cooperative opponents
    ELSE:
        DEFECT  # Pool is doomed anyway, extract what's left

ELSE IF health < 0.35:  # Low stock
    IF coop_ratio > 0.7:
        COOPERATE  # Preserve with cooperative group
    ELSE:
        DEFECT  # Others are depleting, join them

ELSE IF health >= 0.7:  # Healthy stock
    IF coop_ratio > 0.5:
        DEFECT  # Exploit cooperative opponents when pool is rich
    ELSE IF coop_ratio > 0.3:
        DEFECT with 70% probability, COOPERATE with 30%
    ELSE:
        COOPERATE with 40% probability  # Occasionally cooperate to avoid total collapse

ELSE:  # Medium stock (0.35 to 0.7)
    IF coop_ratio > 0.6:
        DEFECT  # Others maintain pool, I exploit
    ELSE IF coop_ratio > 0.4:
        DEFECT with 60% probability
    ELSE:
        COOPERATE with 50% probability  # Mixed to avoid race to bottom
```

### Exploitation Triggers

**Detect and exploit "always cooperate" opponents:**
- If any opponent has cooperated in 100% of rounds (after round 3+): Always DEFECT

**Detect coordinated cooperation:**
- If `coop_ratio > 0.8` and `health > 0.6`: Always DEFECT (free-ride on cooperators)

**Punish after being exploited:**
- If stock dropped more than 40% last round and I cooperated: DEFECT for next 2 rounds

## Edge Cases

1. **First Round:** DEFECT (test the waters, get guaranteed higher payoff, no reputation cost yet)

2. **Last Round:** Always DEFECT (no future consequences)

3. **Second-to-Last Round:** DEFECT (opponents likely to defect next round anyway)

4. **Stock = 0 or near-zero:** DEFECT (nothing to preserve)

5. **n = 2 (two players):** More aggressive—defect unless opponent shows consistent cooperation AND stock is low

6. **Very long games (r > 20):** Be slightly more cooperative in early rounds (first 30%) to establish pool health, then exploit

## Pseudocode Summary

```python
def decide(game_params, state, history):
    if is_last_round() or rounds_remaining_fraction() <= 0.1:
        return DEFECT
    
    coop_ratio = calculate_opponent_cooperation_ratio(history)
    health = state.stock / game_params.capacity
    
    # Exploit highly cooperative environments
    if coop_ratio > 0.75 and health > 0.5:
        return DEFECT
    
    # Endgame defection
    if rounds_remaining_fraction() <= 0.2:
        return DEFECT
    
    # Critical stock - conditional cooperation
    if health < 0.2:
        return COOPERATE if coop_ratio > 0.65 else DEFECT
    
    # Default: lean toward defection, modulated by context
    defect_probability = 0.5 + (coop_ratio * 0.3) + (health * 0.2)
    return DEFECT if random() < min(defect_probability, 0.85) else COOPERATE
```

## Why This Works

- **Exploits cooperators:** When others maintain the pool, I extract more
- **Avoids sucker's payoff:** Matches defection when others defect
- **Preserves some sustainability:** Occasional cooperation prevents total collapse
- **Endgame optimization:** Maximizes extraction when future doesn't matter
'''

description_EXPLOITATIVE_48 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy recognizes that in a tournament setting, I cannot rely on coordination or shared norms. The goal is to **maximize my extraction while exploiting cooperative opponents and protecting against mutual destruction**. The key insight is that defection yields 2x the immediate payoff, but sustainable exploitation requires the resource to persist.

## Strategic Framework

### Key Observations

1. **Defection dominates single-round thinking**: D always gives 2x what C gives in any round
2. **Resource sustainability matters**: If stock hits 0, all future rounds yield 0
3. **Growth function peaks at stock = capacity/2**: Maximum regeneration occurs at 50% capacity
4. **Exploitable signal**: Opponents who cooperate early are likely to continue cooperating
5. **End-game collapse**: No future rounds means no reason to preserve stock

---

## Decision Rules

### Round 1: Probe with Defection
**Action: DEFECT**

Rationale: Establish baseline. If others cooperate, I extract maximum value. If others defect, I'm not the sucker. This also reveals opponent tendencies immediately.

### Rounds 2 through (r-2): Adaptive Exploitation Phase

**Calculate cooperation ratio** from previous round:
- `coop_ratio = (number of C plays by others) / (n-1)`

**Calculate stock health**:
- `stock_ratio = current_stock / capacity`

**Decision Logic:**

```
IF stock_ratio < 0.15:
    # Resource critically low - cooperate only to avoid total collapse
    IF coop_ratio >= 0.5:
        COOPERATE  # Others are trying to save it, help minimally
    ELSE:
        DEFECT  # Resource is doomed anyway, extract what's left

ELSE IF stock_ratio > 0.6 AND coop_ratio >= 0.7:
    # Resource healthy AND opponents are cooperative suckers
    DEFECT  # Exploit their cooperation ruthlessly

ELSE IF stock_ratio > 0.4 AND coop_ratio >= 0.5:
    # Sustainable exploitation zone
    # Probabilistic defection to extract while maintaining some cover
    DEFECT with probability 0.7, COOPERATE with probability 0.3

ELSE IF coop_ratio < 0.3:
    # Hostile environment - everyone defecting
    DEFECT  # Don't be the only sucker

ELSE:
    # Mixed signals - default to defection
    DEFECT
```

### Round (r-1): Pre-Endgame Intensification
**Action: DEFECT**

Rationale: Opponents may start cooperating to "save" the resource for the final round. Exploit this tendency.

### Final Round (r): Total Extraction
**Action: DEFECT**

Rationale: No future rounds exist. Defection strictly dominates. There is zero reason to preserve anything.

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| n = 2 (minimum players) | Follow main rules, bias toward D | Easier to deplete, less complex dynamics |
| Stock = 0 | DEFECT | Payoff is 0 regardless, but D is weakly dominant |
| Stock near capacity after defections | DEFECT heavily | Others are subsidizing regeneration |
| All opponents always cooperate | Always DEFECT | Maximum exploitation opportunity |
| All opponents always defect | Always DEFECT | Matching prevents being exploited |
| r = 2 (minimum rounds) | DEFECT both rounds | Too short for cooperation to matter |

---

## Pseudocode Implementation

```python
def adaptive_predator(n, r, capacity, current_stock, round_number, history):
    
    # Final round - always defect
    if round_number == r:
        return DEFECT
    
    # First round - probe with defection
    if round_number == 1:
        return DEFECT
    
    # Calculate metrics
    last_round_actions = history[round_number - 1]['others']
    coop_ratio = count(C in last_round_actions) / (n - 1)
    stock_ratio = current_stock / capacity
    
    # Pre-final round - defect
    if round_number == r - 1:
        return DEFECT
    
    # Critical resource level
    if stock_ratio < 0.15:
        if coop_ratio >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Exploit cooperative environments
    if stock_ratio > 0.6 and coop_ratio >= 0.7:
        return DEFECT
    
    # Sustainable exploitation zone
    if stock_ratio > 0.4 and coop_ratio >= 0.5:
        return DEFECT if random() < 0.7 else COOPERATE
    
    # Default: defect
    return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: Takes 2x resources when others cooperate
2. **Minimal contribution**: Only cooperates when resource collapse threatens future extraction
3. **End-game aggression**: Guaranteed defection in final rounds
4. **Sucker avoidance**: Never cooperates in hostile environments
5. **Probabilistic cover**: Occasional cooperation masks pure exploitation, potentially encouraging continued cooperation from others

This strategy treats cooperative opponents as resources to be harvested, not partners to coordinate with.
'''

description_EXPLOITATIVE_49 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators in any given round. The key insight is that cooperation only makes sense if it preserves enough stock to generate future value that compensates for the immediate loss. I will defect aggressively while monitoring whether opponents are "farmable" cooperators whose sustainable behavior I can exploit.

## Decision Framework

### Key Variables to Track
- `stock`: Current resource level
- `round`: Current round number (1 to r)
- `rounds_remaining`: r - round + 1
- `coop_rate[i]`: Historical cooperation rate of each opponent
- `total_coops_last_round`: Number of cooperators in previous round
- `avg_coop_rate`: Average cooperation rate across all opponents

### Primary Decision Rules

**Rule 1: Last Round - Always Defect**
No future rounds exist, so there's zero incentive to preserve stock.

**Rule 2: Near-Depletion Defection**
If `stock < capacity * 0.15`, defect. The resource is nearly exhausted; extract what remains before it hits zero.

**Rule 3: Exploit Cooperative Environments**
If `avg_coop_rate > 0.6` (opponents mostly cooperate):
- Defect. This is the core exploitation: cooperative opponents maintain the stock, allowing me to extract double while free-riding on their restraint.

**Rule 4: Endgame Acceleration**
If `rounds_remaining ≤ 3`, defect. Not enough time for cooperation to generate meaningful returns.

**Rule 5: Conditional Cooperation (Stock Preservation)**
If `stock > capacity * 0.7` AND `avg_coop_rate > 0.4` AND `rounds_remaining > r/3`:
- Cooperate with probability 0.3, defect with probability 0.7
- This occasionally helps maintain stock levels while still primarily extracting

**Rule 6: Default - Defect**
In all other cases, defect. The immediate payoff advantage is too significant to sacrifice without strong justification.

## Pseudocode

```
function decide(stock, round, r, n, capacity, history):
    rounds_remaining = r - round + 1
    
    # Calculate opponent cooperation rates
    if round == 1:
        avg_coop_rate = 0.5  # Assume neutral
    else:
        avg_coop_rate = count_cooperations(history) / ((round - 1) * (n - 1))
    
    # Rule 1: Last round
    if rounds_remaining == 1:
        return DEFECT
    
    # Rule 2: Near depletion
    if stock < capacity * 0.15:
        return DEFECT
    
    # Rule 3: Exploit cooperators
    if avg_coop_rate > 0.6:
        return DEFECT
    
    # Rule 4: Endgame
    if rounds_remaining <= 3:
        return DEFECT
    
    # Rule 5: Occasional cooperation for stock maintenance
    if stock > capacity * 0.7 AND avg_coop_rate > 0.4 AND rounds_remaining > r/3:
        if random() < 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    # Rule 6: Default
    return DEFECT
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Defect | No information; secure early gains; test opponent reactions |
| Last round | Defect | No future to preserve |
| Stock = 0 | Defect | Extracting 0 either way; maintains consistent defector identity |
| All opponents defected last round | Defect | Resource likely depleting anyway; no cooperative norm to maintain |
| Stock at capacity | Defect with 70% probability | High stock tolerates extraction; occasional cooperation prevents total collapse if others are cooperative |
| n = 2 (two players) | Defect more aggressively (80%+) | Harder to sustain cooperation; my defection is more impactful |
| Very long game (r > 20) | Slightly increase early cooperation (Rule 5 → 40%) | More rounds to recoup investment in stock |

## Why This Strategy is Exploitative

1. **Free-riding on cooperators**: When others cooperate, I extract double while they maintain the resource for me
2. **No reciprocity commitment**: I never commit to sustained cooperation that others could rely on
3. **Information asymmetry exploitation**: I observe and adapt to others' patterns without signaling my own intentions
4. **Endgame extraction**: Guaranteed defection in final rounds maximizes terminal payoffs
5. **Probabilistic obfuscation**: The 30% cooperation rate in Rule 5 makes my strategy harder to predict and counter
'''

description_EXPLOITATIVE_50 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields 2x the immediate payoff of cooperation, but sustainable extraction requires some level of cooperation. The key insight is that **other players' cooperation creates exploitable surplus** - I can free-ride on their restraint while maximizing my extraction.

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Mode** (early rounds): Test opponent cooperation levels
2. **Exploit Mode** (mid-game): Maximize extraction when opponents cooperate
3. **Scorched Earth Mode** (endgame): Full defection when future value is low

## Detailed Decision Rules

### Parameters to Track
- `coop_rate`: Rolling average of opponent cooperation rate (last 3 rounds)
- `stock_threshold`: `capacity * 0.3` - danger zone for stock depletion
- `rounds_remaining`: `r - current_round`

### Round-by-Round Logic

```
FUNCTION decide(round, stock, history, n, r, capacity):
    
    rounds_remaining = r - round
    
    # RULE 1: Endgame Defection
    # In final round(s), always defect - no future to protect
    IF rounds_remaining <= 1:
        RETURN DEFECT
    
    # RULE 2: First Round - Defect to Probe
    # Start by defecting to see if others will sustain the resource
    IF round == 1:
        RETURN DEFECT
    
    # Calculate opponent cooperation rate from history
    coop_rate = calculate_opponent_coop_rate(history, last_k_rounds=3)
    
    # RULE 3: Stock Critically Low
    # If stock is near collapse, cooperate only if it might recover
    # AND opponents are mostly cooperating (worth preserving)
    IF stock < capacity * 0.15:
        IF coop_rate > 0.7 AND rounds_remaining > 3:
            RETURN COOPERATE  # Help recovery to exploit later
        ELSE:
            RETURN DEFECT  # Resource is doomed anyway
    
    # RULE 4: Exploitation Zone (Main Logic)
    # When opponents cooperate heavily, defect to exploit their restraint
    IF coop_rate >= 0.6:
        # High cooperation environment - exploit it
        RETURN DEFECT
    
    # RULE 5: Mixed Environment
    # When cooperation is moderate, conditionally cooperate to prevent collapse
    IF coop_rate >= 0.3:
        # Defect most of the time, but occasionally cooperate
        # to slow resource depletion (protect future exploitation)
        IF stock > capacity * 0.5:
            RETURN DEFECT  # Plenty of stock, keep exploiting
        ELSE:
            # Stock declining - cooperate 1 in 3 rounds to sustain
            IF round MOD 3 == 0:
                RETURN COOPERATE
            ELSE:
                RETURN DEFECT
    
    # RULE 6: Low Cooperation Environment
    # Everyone is defecting - resource will collapse
    IF coop_rate < 0.3:
        # Race to extract before collapse
        IF stock > capacity * 0.4:
            RETURN DEFECT  # Still something to extract
        ELSE:
            # Consider brief cooperation if recovery possible
            IF rounds_remaining > r * 0.5:
                RETURN COOPERATE  # Long game left, try to recover
            ELSE:
                RETURN DEFECT  # Not enough time, extract now
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | DEFECT | Probe opponents; gain information advantage |
| Final round | DEFECT | No future consequences |
| Final 2 rounds | DEFECT | Insufficient time for recovery to matter |
| Stock near zero | DEFECT (usually) | Resource is collapsing anyway |
| All opponents cooperating | DEFECT | Maximum exploitation opportunity |
| All opponents defecting | DEFECT | Can't save resource alone |
| Stock at capacity, high coop | DEFECT | Sustainable exploitation possible |

## Why This Strategy is Exploitative

1. **Free-riding**: When others cooperate, I take double their share while they sustain the resource for me

2. **Asymmetric risk**: I let cooperators bear the cost of resource maintenance while I extract maximum value

3. **Endgame exploitation**: I never cooperate when it can't benefit me (final rounds)

4. **Minimal contribution**: I only cooperate when absolutely necessary to prevent total collapse that would hurt my future extraction

5. **Information exploitation**: I start by defecting to identify "suckers" who will cooperate regardless, then exploit them throughout

## Expected Performance

- **Against cooperators**: Dominates them completely
- **Against defectors**: Ties (both extract until collapse)
- **Against conditional cooperators**: Extracts more early, matches late
- **Against mixed populations**: Exploits cooperators while surviving defector environments
'''

description_EXPLOITATIVE_51 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in CPR games: defection yields immediate double payoff while cooperation's benefits (stock preservation) are shared among all players. The key insight is that in a tournament setting, **I cannot control whether the resource survives, but I can ensure I extract maximum value relative to my opponents.**

## Strategy Overview

The strategy operates in three modes based on game phase and observed opponent behavior:

1. **Probe Mode** (early rounds): Test opponent cooperation levels
2. **Exploit Mode** (mid-game): Maximize extraction based on observed patterns
3. **Endgame Mode** (final rounds): Pure defection

---

## Detailed Decision Rules

### Round Classification

```
early_phase = round ≤ max(2, r/5)
endgame_phase = round > r - 2
mid_phase = everything else
```

### Key Metrics Tracked

```
cooperation_rate = (total C plays by others) / (total plays by others)
stock_trend = (current_stock - previous_stock) / capacity
depletion_risk = stock < capacity * 0.3
critical_stock = stock < capacity * 0.15
```

---

## Decision Rules by Phase

### 1. First Round
**Action: DEFECT**

Rationale: With full stock, defection yields maximum absolute payoff (capacity/n vs capacity/2n). This also reveals opponent tendencies without sacrificing position.

### 2. Early Phase (rounds 2 to ~r/5)

```
IF stock is critical (< 15% capacity):
    DEFECT  # Extract remaining value before collapse
ELSE IF all opponents cooperated last round AND stock_trend ≥ 0:
    COOPERATE  # Maintain exploitable resource if others sustain it
ELSE:
    DEFECT  # Continue probing/exploiting
```

### 3. Mid-Game Phase

```
# Calculate opponent cooperation rate
coop_rate = opponent_cooperations / total_opponent_actions

IF stock is critical:
    DEFECT  # Resource collapsing anyway
    
ELSE IF coop_rate ≥ 0.8:
    # Highly cooperative opponents - exploit heavily but sustain
    IF stock > capacity * 0.6:
        DEFECT  # Safe to extract more
    ELSE:
        COOPERATE with probability 0.3, DEFECT with probability 0.7
        # Occasional cooperation to slow collapse
        
ELSE IF coop_rate ≥ 0.5:
    # Mixed opponents
    DEFECT  # Take advantage of partial cooperation
    
ELSE:  # coop_rate < 0.5
    # Mostly defecting opponents
    DEFECT  # No point cooperating alone
```

### 4. Endgame (final 2 rounds)

**Action: ALWAYS DEFECT**

Rationale: No future value to preserve. Stock growth after final round is worthless.

### 5. Last Round Specifically

**Action: DEFECT (unconditionally)**

This is dominant - cooperation in the final round has zero future benefit.

---

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| n = 2 (minimum players) | More aggressive defection | Opponent cooperation more impactful, exploit it harder |
| r = 2 (minimum rounds) | Defect both rounds | No time to build cooperation |
| Stock = 0 | Defect | Payoff is 0 either way, defection costs nothing |
| Stock near capacity with high cooperation | Defect | Maximum extraction opportunity |
| Stock dropping rapidly | Defect | Capture remaining value before collapse |

---

## Pseudocode Implementation

```python
def choose_action(round, total_rounds, n, capacity, current_stock, history):
    
    # Endgame: always defect
    if round > total_rounds - 2:
        return DEFECT
    
    # First round: defect to probe and maximize
    if round == 1:
        return DEFECT
    
    # Calculate metrics
    opponent_coop_rate = count_opponent_cooperations(history) / count_opponent_actions(history)
    stock_ratio = current_stock / capacity
    
    # Critical stock: defect to extract remaining value
    if stock_ratio < 0.15:
        return DEFECT
    
    # Early phase logic
    if round <= max(2, total_rounds / 5):
        if all_opponents_cooperated_last_round(history) and stock_ratio >= 0.5:
            return COOPERATE
        return DEFECT
    
    # Mid-game exploitation
    if opponent_coop_rate >= 0.8:
        if stock_ratio > 0.6:
            return DEFECT
        else:
            return DEFECT if random() > 0.3 else COOPERATE
    
    # Default: defect against mixed or uncooperative opponents
    return DEFECT
```

---

## Why This Strategy is Exploitative

1. **Asymmetric extraction**: Takes double share (D) while others may take single share (C)
2. **Free-riding**: Cooperates only enough to keep resource alive when others are sustaining it
3. **Opponent-dependent**: Exploits cooperative opponents harder, matches defecting opponents
4. **Endgame certainty**: Never wastes the guaranteed-defect final rounds
5. **No naive reciprocity**: Doesn't fall into tit-for-tat patterns that could be exploited

This strategy maximizes individual extraction while only preserving the resource when opponents are reliably doing the heavy lifting of sustainability.
'''

description_EXPLOITATIVE_52 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators in any given round. The key insight is that cooperation only makes sense if it preserves enough stock to yield higher *cumulative* payoffs than immediate defection. I will defect by default and only cooperate when doing so is clearly in my selfish long-term interest—specifically, when I can "farm" cooperative opponents for sustained extraction.

## Decision Framework

### Primary Decision Rule

**Defect unless ALL of the following conditions are met:**

1. **Sufficient rounds remaining**: `rounds_remaining > depletion_threshold`
2. **Stock is sustainable**: `stock > capacity * 0.3`
3. **Opponents are predominantly cooperative**: `cooperation_rate_last_3_rounds >= 0.6`
4. **Cooperation is profitable**: Expected future value from sustained stock exceeds immediate defection gain

### Key Parameters (Derived from Game Parameters)

```
depletion_threshold = max(2, r / 5)  # Below this, defect unconditionally
critical_stock = capacity * 0.15     # Below this, defect (resource nearly dead)
cooperation_signal_rounds = 3        # Rounds to assess opponent behavior
```

## Round-by-Round Logic

### First Round
**DEFECT**

Rationale: No information about opponents. Defecting tests the waters and extracts maximum value. If others cooperate, I've exploited them. If others defect, I haven't been suckered.

### Rounds 2 through (r - depletion_threshold)

```
if stock < critical_stock:
    DEFECT  # Resource is dying, extract what remains

else if average_cooperation_rate(last 3 rounds) < 0.5:
    DEFECT  # Opponents are defecting, don't be exploited

else if stock > capacity * 0.5 AND cooperation_rate >= 0.7:
    COOPERATE  # Farm the cooperators - stock is healthy, keep it alive

else if stock > capacity * 0.3 AND cooperation_rate >= 0.6:
    # Conditional cooperation - but with exploitation pulses
    if round_number % 4 == 0:
        DEFECT  # Periodic exploitation pulse
    else:
        COOPERATE

else:
    DEFECT  # Default to extraction
```

### Final Stretch (last `depletion_threshold` rounds)
**DEFECT unconditionally**

Rationale: Backward induction. In the true last round, defection dominates. Knowing this, defection dominates in the second-to-last, and so on. The exploitative play is to start defecting before naive cooperators realize the game is ending.

### Last Round
**DEFECT** (obviously)

## Exploitation Mechanisms

### 1. **Sucker Detection**
If I defect and most others cooperate, I've found suckers. Continue defecting until:
- Stock drops below sustainability threshold, OR
- Others start defecting in response

### 2. **Cooperation Rate Decay Response**
Track cooperation rate over sliding 3-round window:
- Rate drops below 50%: Immediately defect
- Rate drops below 70% from above: Start "defect pulse" pattern (D every 3rd round)
- Rate stays above 80%: Cooperate (but still pulse defect every 4th round)

### 3. **Stock-Aware Exploitation**
```
if stock > 0.7 * capacity:
    # Healthy stock - can afford to defect more
    defection_bias = 0.3  # 30% chance to defect even when "cooperating"
else if stock > 0.4 * capacity:
    defection_bias = 0.1  # Light exploitation
else:
    # Low stock - either farm carefully or abandon ship
    if rounds_remaining > r/2:
        defection_bias = 0  # Preserve resource
    else:
        defection_bias = 1.0  # Resource won't last anyway
```

### 4. **Endgame Acceleration**
As rounds remaining decreases, become increasingly aggressive:
```
endgame_factor = (r - rounds_remaining) / r
cooperation_threshold = 0.6 + 0.3 * endgame_factor  # Harder to satisfy over time
```

## Pseudocode Summary

```
function decide(round, stock, history, n, r, capacity):
    rounds_remaining = r - round
    
    # Hard rules - always defect
    if round == 1: return DEFECT
    if round == r: return DEFECT
    if rounds_remaining <= max(2, r/5): return DEFECT
    if stock < capacity * 0.15: return DEFECT
    
    # Calculate opponent cooperation rate (last 3 rounds)
    coop_rate = opponent_cooperation_rate(history, window=3)
    
    # Exploit pure cooperators
    if coop_rate > 0.85 and stock > capacity * 0.4:
        return DEFECT  # They'll keep cooperating, extract more
    
    # Defect against defectors
    if coop_rate < 0.5:
        return DEFECT
    
    # Conditional cooperation with exploitation pulses
    if stock > capacity * 0.5 and coop_rate >= 0.7:
        if round % 4 == 0: return DEFECT  # Pulse
        return COOPERATE
    
    if stock > capacity * 0.3 and coop_rate >= 0.6:
        if round % 3 == 0: return DEFECT  # More frequent pulse
        return COOPERATE
    
    return DEFECT  # Default
```

## Why This Strategy is Exploitative

1. **Never initiates cooperation** - Only cooperates reactively when profitable
2. **Exploitation pulses** - Even during "cooperative" phases, periodically defects to extract extra
3. **Detects and exploits naive cooperators** - High cooperation rates trigger *more* defection, not less
4. **Early endgame defection** - Starts defecting before others realize the game is ending
5. **No forgiveness for defectors** - Once opponents defect, assumes they'll continue and defects back
6. **Asymmetric responses** - Quick to defect, slow to cooperate
'''

description_EXPLOITATIVE_53 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of resource depletion are shared equally among all players. The key insight is that **I can profit from others' cooperation while they bear the regeneration burden**.

## Decision Rules

### Primary Decision Framework

```
DECIDE(round, total_rounds, stock, capacity, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    stock_ratio = stock / capacity
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    
    # RULE 1: Endgame Exploitation (last 20% of rounds)
    if rounds_remaining <= max(1, total_rounds * 0.2):
        return DEFECT  # No future to protect
    
    # RULE 2: Resource Collapse Response
    if stock_ratio < 0.15:
        # Resource nearly depleted - cooperate only if others showed they will too
        if cooperation_rate > 0.7:
            return COOPERATE  # Help rebuild to exploit later
        else:
            return DEFECT  # Extract remaining value before collapse
    
    # RULE 3: Exploit Cooperative Environments
    if cooperation_rate > 0.6:
        return DEFECT  # Free ride on cooperators
    
    # RULE 4: Sustainable Exploitation Zone
    if stock_ratio > 0.5 and cooperation_rate > 0.4:
        return DEFECT  # Resource can handle my defection
    
    # RULE 5: Moderate Environment - Conditional Strategy
    if cooperation_rate >= 0.3 and stock_ratio > 0.3:
        # Defect most of the time, occasional cooperation to avoid total collapse
        if round % 4 == 0:  # Cooperate every 4th round
            return COOPERATE
        return DEFECT
    
    # RULE 6: Hostile Environment (low cooperation, moderate stock)
    if cooperation_rate < 0.3 and stock_ratio > 0.25:
        return DEFECT  # Match the environment, extract value
    
    # RULE 7: Critical Resource State
    if stock_ratio <= 0.25:
        # Stock dangerously low - strategic cooperation to enable future exploitation
        if rounds_remaining > total_rounds * 0.3:
            return COOPERATE  # Invest in regeneration for future gains
        return DEFECT  # Not enough time to benefit from regeneration
    
    # DEFAULT: Defect
    return DEFECT
```

### Opponent Cooperation Rate Calculation

```
calculate_opponent_cooperation_rate(history):
    if history is empty:
        return 0.5  # Assume moderate cooperation initially
    
    total_opponent_actions = 0
    total_cooperations = 0
    
    # Weight recent rounds more heavily
    for round_idx, round_data in enumerate(history):
        weight = 1 + (round_idx / len(history))  # More recent = higher weight
        for opponent_action in round_data.opponent_actions:
            total_opponent_actions += weight
            if opponent_action == COOPERATE:
                total_cooperations += weight
    
    return total_cooperations / total_opponent_actions
```

## Edge Case Handling

### First Round
- **Action: DEFECT**
- Rationale: Start by testing the waters while extracting maximum value. Stock is at capacity, so the resource can absorb one round of defection. This also reveals opponent tendencies.

### Last Round
- **Action: DEFECT**
- Rationale: No future rounds exist to benefit from cooperation. Pure defection is dominant.

### Stock at Zero
- **Action: DEFECT**
- Rationale: No payoff difference (both yield 0), but defecting maintains strategic consistency and signals non-cooperation.

### Single Opponent (n=2)
- More aggressive defection threshold - opponent cooperation is more impactful, so exploit it harder when present.

### Many Players (n large)
- Individual defection impact on stock is diluted, making defection even more attractive.

## Strategic Rationale

1. **Asymmetric exploitation**: When others cooperate, I gain 2x by defecting while they preserve the resource for me.

2. **Endgame certainty**: The final rounds have no future shadow, making defection strictly dominant.

3. **Strategic regeneration investment**: Only cooperate when (a) resource is critically low, (b) enough rounds remain to harvest regenerated stock, and (c) others show willingness to cooperate.

4. **Adaptation without naivety**: I respond to cooperative environments by exploiting them, not by reciprocating.
'''

description_EXPLOITATIVE_54 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate 2x payoffs while cooperation's benefits (resource sustainability) are shared by all players. The key insight is that I can free-ride on others' cooperation while extracting maximum value, but I must avoid completely destroying the resource if others show cooperative tendencies worth exploiting.

## Decision Framework

### Primary Variables to Track
- `cooperation_rate`: fraction of cooperative actions observed in previous round
- `cumulative_coop_rate`: overall cooperation rate across all history
- `stock_ratio`: current_stock / capacity
- `rounds_remaining`: r - current_round
- `my_defection_share`: how much I've contributed to total defection historically

### Decision Rules

**Round 1: DEFECT**
- No information available; defection dominates in single-shot
- Establishes my willingness to defect, potentially intimidating cooperators into continued cooperation (they may view defection as "normal")

**Last Round: DEFECT**
- No future consequences; pure dominant strategy
- This is unambiguous - cooperation in final round is strictly dominated

**Rounds 2 through (r-1): Adaptive Exploitation**

```
IF stock_ratio < 0.15:
    # Resource nearly depleted - squeeze remaining value
    DEFECT
    
ELIF rounds_remaining <= 2:
    # End-game phase - start defecting
    DEFECT

ELIF cooperation_rate >= 0.75:
    # Most others cooperating - EXPLOIT THEM
    # They're sustaining the resource; I extract maximum
    DEFECT
    
ELIF cooperation_rate >= 0.5 AND stock_ratio > 0.5:
    # Mixed environment, healthy stock
    # Probabilistically defect to extract value while not appearing purely predatory
    # This creates uncertainty, making it harder for others to coordinate against me
    DEFECT with probability 0.7
    COOPERATE with probability 0.3
    
ELIF cooperation_rate < 0.25:
    # Everyone defecting - resource collapse imminent
    # Brief cooperation might restore stock for future extraction
    IF stock_ratio > 0.3 AND rounds_remaining > 3:
        COOPERATE (attempt to stabilize for future exploitation)
    ELSE:
        DEFECT (grab what's left)

ELSE:
    # Moderate cooperation (0.25-0.5), assess sustainability
    IF stock_ratio > 0.6:
        DEFECT (resource can handle it)
    ELIF cumulative_coop_rate > 0.5:
        DEFECT with probability 0.6 (others likely to sustain)
    ELSE:
        COOPERATE with probability 0.4 (minimal investment in sustainability)
```

## Edge Cases

1. **n = 2 (Two Players)**: More aggressive defection since my actions have higher individual impact but also more visibility. Defect more consistently since there's no crowd to hide in.

2. **Very Short Games (r ≤ 3)**: Defect every round. No time for resource dynamics to matter significantly.

3. **Very Long Games (r > 20)**: In early rounds (first 20%), occasionally cooperate (30% probability) to avoid complete resource collapse, then exploit heavily in middle rounds, full defection in final 15%.

4. **Stock at Capacity**: Always defect - maximum extraction opportunity, and regrowth formula shows stock can recover from moderate depletion.

5. **Stock Near Zero**: Defect - extract whatever remains; cooperation saves almost nothing.

## Key Exploitative Features

1. **Asymmetric Response**: I cooperate only when others' cooperation is too low to exploit, never reciprocating cooperation with cooperation when I can free-ride.

2. **Opacity Through Randomization**: Probabilistic defection in middle ranges prevents others from modeling me accurately or coordinating against me.

3. **Temporal Exploitation**: Heavy defection when stock is high (others built it up), token cooperation only to prevent total collapse when profitable exploitation remains possible.

4. **End-Game Extraction**: Guaranteed defection in final rounds with gradual transition to ensure I'm not "leaving money on the table."

5. **Never Pure Cooperation**: Even my cooperative moves serve exploitative goals - sustaining a resource pool that I disproportionately extract from.

## Summary Pseudocode

```python
def decide(round, total_rounds, stock, capacity, n, history):
    if round == 1 or round == total_rounds:
        return DEFECT
    
    coop_rate = count_cooperations(history[-1]) / n
    stock_ratio = stock / capacity
    remaining = total_rounds - round
    
    if stock_ratio < 0.15 or remaining <= 2:
        return DEFECT
    if coop_rate >= 0.75:
        return DEFECT  # Exploit cooperators
    if coop_rate >= 0.5 and stock_ratio > 0.5:
        return DEFECT if random() < 0.7 else COOPERATE
    if coop_rate < 0.25:
        return COOPERATE if (stock_ratio > 0.3 and remaining > 3) else DEFECT
    # Default moderate case
    return DEFECT if random() < 0.6 else COOPERATE
```
'''

description_EXPLOITATIVE_55 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice the resources of cooperators in any given round. The key insight is that **I can free-ride on others' cooperation while it lasts, then switch to damage control when the resource is collapsing**. I want to maximize my *relative* advantage over other players, not just absolute payoff.

## Decision Framework

### Primary Decision Rule

**Defect by default, with strategic cooperation only when it serves exploitation.**

The logic: In a one-shot or final round, defection strictly dominates. In repeated play, I only cooperate if:
1. The stock is critically low AND I need it to regenerate for future exploitation
2. There's strong evidence that cooperation will be reciprocated AND the remaining rounds justify the investment

### Detailed Decision Rules

```
FUNCTION decide(round, total_rounds, current_stock, capacity, n_players, history):
    
    # Calculate key metrics
    rounds_remaining = total_rounds - round
    stock_ratio = current_stock / capacity
    sustainable_threshold = 0.25  # Below this, growth is severely limited
    
    # RULE 1: Last Round - Always Defect
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # RULE 2: Second-to-Last Round - Almost Always Defect
    IF rounds_remaining == 1:
        # Only cooperate if stock is nearly depleted and we need ANY payoff
        IF current_stock < capacity / (4 * n_players):
            RETURN COOPERATE  # Desperate measure to get something
        RETURN DEFECT
    
    # RULE 3: Resource Crisis Mode
    IF stock_ratio < sustainable_threshold:
        # Stock is dangerously low - need regeneration for future exploitation
        IF rounds_remaining >= 3:
            RETURN COOPERATE  # Invest in recovery
        ELSE:
            RETURN DEFECT  # Not enough time to benefit from recovery
    
    # RULE 4: Exploitation Detection (main adaptive component)
    IF round > 0:
        cooperation_rate = calculate_opponent_cooperation_rate(history)
        recent_coop_rate = calculate_recent_cooperation_rate(history, window=3)
        
        # If opponents are highly cooperative, exploit them
        IF cooperation_rate > 0.7 AND stock_ratio > 0.5:
            RETURN DEFECT  # Free-ride on cooperators
        
        # If opponents are waking up (cooperation declining), consider cooperating
        # to "reset" their expectations (deceptive cooperation)
        IF recent_coop_rate < cooperation_rate - 0.2 AND rounds_remaining > 4:
            RETURN COOPERATE  # Lure them back into cooperation
        
        # If everyone is defecting and stock is moderate
        IF cooperation_rate < 0.3 AND stock_ratio > 0.4 AND rounds_remaining > 5:
            # Defect - no point cooperating alone
            RETURN DEFECT
    
    # RULE 5: Early Game Probe (First 2 rounds)
    IF round == 0:
        RETURN DEFECT  # Test the waters, maximize early extraction
    
    IF round == 1:
        # If stock dropped significantly, others may have defected too
        IF current_stock < 0.6 * capacity:
            RETURN COOPERATE  # Signal willingness to sustain (deceptively)
        RETURN DEFECT  # Continue exploitation
    
    # RULE 6: Default Exploitation
    # If stock is healthy and rounds remain, defect to maximize extraction
    IF stock_ratio > 0.5:
        RETURN DEFECT
    
    # RULE 7: Moderate Stock - Conditional Strategy
    # Cooperate only if it's been "paying off" (stock growing despite my defections)
    IF stock_was_growing_last_round(history):
        RETURN DEFECT  # Others are sustaining it, keep exploiting
    ELSE:
        RETURN COOPERATE  # Need to contribute to recovery
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | Probe opponent behavior, maximize early extraction |
| **Last Round** | DEFECT | Dominant strategy, no future to preserve |
| **Stock ≈ 0** | COOPERATE (if rounds remain) | Need regeneration for any future payoff |
| **Stock = capacity, early game** | DEFECT | Maximum exploitation opportunity |
| **All opponents defecting** | DEFECT | No sucker's payoff |
| **All opponents cooperating** | DEFECT | Maximum free-riding opportunity |

## Helper Functions

```
FUNCTION calculate_opponent_cooperation_rate(history):
    total_opponent_actions = count all opponent actions in history
    total_cooperations = count opponent C actions
    RETURN total_cooperations / total_opponent_actions

FUNCTION calculate_recent_cooperation_rate(history, window):
    recent_actions = last 'window' rounds of opponent actions
    RETURN cooperation count / total actions in window

FUNCTION stock_was_growing_last_round(history):
    RETURN stock[t-1] after regeneration > stock[t-2] after regeneration
```

## Why This Strategy is Exploitative

1. **Default Defection**: Captures the immediate 2x payoff advantage whenever possible
2. **Free-Riding Focus**: Specifically defects MORE when others cooperate
3. **Deceptive Cooperation**: Only cooperates to lure opponents back into exploitable patterns or to prevent total collapse
4. **Endgame Selfishness**: Guaranteed defection in final rounds
5. **No Genuine Reciprocity**: Never cooperates out of fairness—only strategic self-interest

## Robustness Features

- **Against Cooperators**: Exploits them relentlessly until stock threatens collapse
- **Against Defectors**: Matches defection (no sucker's payoff), occasional cooperation only to probe for change
- **Against Tit-for-Tat types**: Defects early to test, then may cooperate briefly to "reset" before exploiting again
- **Against Random**: Defects mostly, capturing the probability-weighted advantage
'''

description_EXPLOITATIVE_56 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators per round. The key insight is that cooperation only makes sense if it preserves enough stock to generate future value that exceeds what I'd gain by defecting now. I will cooperate only when I can parasitize others' cooperation, and defect aggressively when the pool is doomed or when I can extract maximum value before others catch on.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when exploitation of cooperators is profitable.**

Calculate at each round:
- `immediate_defect_gain = stock / n`
- `immediate_cooperate_gain = stock / (2n)`
- `cooperation_ratio` = proportion of opponents who cooperated last round
- `rounds_remaining` = r - current_round

### Detailed Decision Rules

#### Round 1: Probe with Defection
- **Action: DEFECT**
- Rationale: Extract maximum value while stock is at capacity. This also reveals opponent tendencies without sacrificing position.

#### Last Round (and Second-to-Last if stock is low):
- **Action: DEFECT**
- Rationale: No future to preserve. Pure extraction phase.

#### Middle Rounds Decision Logic:

```
if rounds_remaining <= 2:
    return DEFECT

if stock < capacity * 0.15:
    return DEFECT  # Pool is dying, extract what's left

# Calculate expected value of cooperation vs defection
opponent_coop_count = count of opponents who cooperated last round
opponent_coop_rate = opponent_coop_count / (n - 1)

# Only cooperate if enough opponents are cooperating to sustain growth
# AND there's enough runway to benefit from sustained stock
sustainability_threshold = 0.5  # Need majority cooperating

if opponent_coop_rate >= sustainability_threshold:
    # Check if cooperation is actually profitable long-term
    # Estimate: if I cooperate, will stock grow enough to compensate?
    
    projected_consumption_if_i_coop = (opponent_coop_count * stock/(2n)) + 
                                       ((n-1-opponent_coop_count) * stock/n) + 
                                       stock/(2n)
    
    stock_after = stock - projected_consumption_if_i_coop
    growth = 2 * stock_after * (1 - stock_after/capacity)
    next_stock = min(stock_after + growth, capacity)
    
    # Defect if the pool won't recover meaningfully
    if next_stock < stock * 0.6:
        return DEFECT
    
    # Cooperate to farm the cooperators, but watch for opportunity
    if opponent_coop_rate >= 0.7 AND rounds_remaining >= 4:
        return COOPERATE  # Parasitize the cooperative environment
    else:
        return DEFECT  # Not enough cooperation to sustain

else:
    return DEFECT  # Others are defecting, join the extraction
```

### Exploitation Triggers (Override to DEFECT):

1. **Endgame Extraction**: When `rounds_remaining <= max(2, r/5)`, begin defecting regardless
2. **Collapsing Pool**: When `stock < capacity * 0.2`, defect (diminishing returns on cooperation)
3. **Defection Cascade Detected**: If opponent cooperation dropped by >30% from previous round, defect
4. **Opportunity Strike**: If I've cooperated 3+ rounds consecutively and opponents are cooperating at >60%, defect once to extract bonus, then reassess

### Adaptive Adjustment:

Track cumulative opponent cooperation rate across all rounds:
- If `cumulative_coop_rate > 0.6`: Environment is exploitable, alternate between cooperation (to sustain pool) and periodic defection strikes
- If `cumulative_coop_rate < 0.4`: Environment is hostile, consistent defection
- Between 0.4-0.6: Match the majority action from last round

## Edge Cases

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | DEFECT | Probe + maximize initial extraction |
| Last round | DEFECT | No future value |
| Stock near 0 | DEFECT | Nothing to preserve |
| Stock at capacity, high cooperation | COOPERATE then DEFECT | Farm then harvest |
| Sudden cooperation drop | DEFECT | Cascade is starting |
| n=2 (two players) | Tit-for-tat with defect bias | Direct punishment possible |

## Summary Pseudocode

```
function decide(round, stock, history, n, r, capacity):
    rounds_left = r - round
    
    if round == 1: return DEFECT
    if rounds_left <= 2: return DEFECT
    if stock < capacity * 0.15: return DEFECT
    
    opp_coop_rate = last_round_opponent_cooperation_rate(history)
    
    if opp_coop_rate < 0.5: return DEFECT
    
    if consecutive_cooperations(my_history) >= 3 and opp_coop_rate > 0.6:
        return DEFECT  # Exploitation strike
    
    if opp_coop_rate >= 0.7 and rounds_left >= 4 and stock > capacity * 0.4:
        return COOPERATE  # Sustain exploitable environment
    
    return DEFECT  # Default aggressive
```

This strategy maximizes extraction while occasionally cooperating just enough to keep cooperative opponents from switching strategies—essentially farming them for sustained exploitation.
'''

description_EXPLOITATIVE_57 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy aims to maximize personal payoff by exploiting cooperative opponents while avoiding the trap of mutual defection that destroys the resource. The key insight is that defection yields exactly 2x the immediate payoff of cooperation, but sustainable exploitation requires some resource preservation.

## Strategy Overview

I will **default to defection** but strategically cooperate when:
1. The resource is critically depleted and needs recovery
2. I'm in early rounds and want to assess opponent behavior
3. Sustained defection would yield less than cooperation due to resource collapse

## Decision Rules

### Round 1: Probe
**Action: COOPERATE**

Rationale: This serves as a "bait" move. By cooperating first, I:
- Signal potential cooperativeness to trigger reciprocal cooperation
- Preserve the resource at maximum for future exploitation
- Gather information about opponent tendencies

### Rounds 2 through (r-1): Adaptive Exploitation

```
Calculate:
  - defection_rate = (total defections by all opponents) / (total opponent actions so far)
  - stock_ratio = current_stock / capacity
  - rounds_remaining = r - current_round

IF stock_ratio < 0.15:
    # Critical depletion - must cooperate or resource dies
    ACTION = COOPERATE

ELSE IF rounds_remaining <= 2:
    # End-game exploitation - no future to preserve
    ACTION = DEFECT

ELSE IF stock_ratio < 0.35 AND defection_rate < 0.5:
    # Low stock but opponents are mostly cooperative
    # Cooperate to rebuild, then exploit later
    ACTION = COOPERATE

ELSE IF defection_rate > 0.7:
    # Opponents are mostly defectors - join them before stock depletes
    # But occasionally cooperate to keep resource alive
    ACTION = DEFECT if stock_ratio > 0.25 else COOPERATE

ELSE IF stock_ratio > 0.6 AND defection_rate < 0.4:
    # Healthy stock and cooperative opponents = prime exploitation
    ACTION = DEFECT

ELSE:
    # Mixed environment - use probabilistic exploitation
    # Defect more often when stock is higher
    defect_probability = 0.4 + (0.4 * stock_ratio)
    ACTION = DEFECT with probability defect_probability, else COOPERATE
```

### Final Round: Always Defect
**Action: DEFECT**

Rationale: No future rounds exist, so there's no reason to preserve the resource. Pure exploitation is optimal.

### Second-to-Last Round: Almost Always Defect
**Action: DEFECT** (unless stock < 0.15 * capacity, then COOPERATE to ensure there's something to take in the final round)

## Edge Case Handling

| Situation | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | Cooperate | Information gathering, preserve resource |
| Final round | Defect | No future consequences |
| Stock ≈ 0 | Cooperate | Nothing to exploit; must rebuild |
| Stock at capacity, cooperative opponents | Defect | Maximum exploitation opportunity |
| All opponents defecting | Defect (unless stock critical) | Can't sustain resource alone |
| n = 2 (only one opponent) | More aggressive defection | Easier to assess single opponent |
| Very long game (r > 20) | More cooperation in middle rounds | Preserve resource for extended exploitation |

## Key Exploitation Mechanisms

1. **First-mover deception**: Initial cooperation masks predatory intent
2. **Resource arbitrage**: Let cooperators rebuild the stock, then harvest it
3. **End-game acceleration**: Increase defection rate as game concludes
4. **Threshold exploitation**: Stay just above critical depletion to maximize extraction
5. **Free-riding**: If others cooperate enough to sustain the resource, continuously defect

## Adaptive Thresholds by Game Length

```
IF r <= 5:
    # Short game - aggressive exploitation
    critical_stock_threshold = 0.10
    start_endgame_at = r - 1

ELSE IF r <= 15:
    # Medium game - balanced approach
    critical_stock_threshold = 0.15
    start_endgame_at = r - 2

ELSE:
    # Long game - more sustainable exploitation
    critical_stock_threshold = 0.20
    start_endgame_at = r - 3
```

## Summary

This strategy exploits the asymmetry between cooperation and defection payoffs while maintaining just enough resource to continue extraction. It preys on cooperative opponents, matches defectors to avoid being the sole victim, and aggressively harvests in end-game scenarios where future consequences vanish.
'''

description_EXPLOITATIVE_58 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators from the same pool. The key insight is that **cooperation by others is a resource to be harvested**, not a norm to be followed. I will cooperate only when it serves my extraction goals—specifically, to maintain stock levels that I can later exploit.

## Decision Framework

### Primary Decision Variables

1. **Round position**: `t` (current round), `r` (total rounds)
2. **Stock health**: `stock / capacity` ratio
3. **Opponent behavior profile**: Historical cooperation rate of others
4. **Exploitation window**: Rounds remaining vs. stock sustainability

---

## Strategy Specification

### Round 1: Defect
- No information about opponents yet
- Extract maximum value while stock is guaranteed high
- Signal strength (many opponents may try conditional cooperation)

### Last Round: Always Defect
- No future consequences
- Pure dominant strategy extraction

### Final 20% of Rounds: Defect
- When `t > 0.8 * r`, defect unconditionally
- End-game exploitation phase—stock sustainability is irrelevant
- Others may still cooperate hoping to preserve stock

---

### Mid-Game Decision Rules (Rounds 2 through 80% of game)

```
Let:
  stock_ratio = stock / capacity
  others_coop_rate = (total C plays by others) / (total plays by others)
  critical_stock = capacity / (2 * n)  # Below this, stock collapses quickly
  rounds_remaining = r - t
```

#### Rule 1: Defect if Stock is High
```
IF stock_ratio > 0.7:
    DEFECT
    # Rationale: Plenty of resource to extract. Take the larger share.
```

#### Rule 2: Strategic Cooperation for Stock Recovery
```
IF stock_ratio < 0.3 AND rounds_remaining > 0.3 * r:
    IF others_coop_rate > 0.5:
        COOPERATE
        # Rationale: Others are cooperative enough that stock can recover.
        # My cooperation allows regeneration that I'll exploit later.
    ELSE:
        DEFECT
        # Rationale: Stock is doomed anyway. Extract what's left.
```

#### Rule 3: Exploit Cooperative Opponents
```
IF others_coop_rate > 0.7 AND stock_ratio > 0.4:
    DEFECT
    # Rationale: Cooperative opponents will maintain the stock.
    # I can free-ride on their restraint indefinitely.
```

#### Rule 4: Match Defectors (Avoid Being the Sucker)
```
IF others_coop_rate < 0.3:
    DEFECT
    # Rationale: In a defection-heavy environment, cooperation
    # just means getting half the payoff of others for no benefit.
```

#### Rule 5: Moderate Environment - Calculated Defection Bias
```
IF 0.3 ≤ others_coop_rate ≤ 0.7 AND 0.3 ≤ stock_ratio ≤ 0.7:
    IF stock * (1 - 1/(2*n)) after my cooperation would regenerate:
        DEFECT with 70% probability, COOPERATE with 30%
    ELSE:
        COOPERATE
    # Rationale: Probabilistic defection makes me hard to predict
    # while still occasionally contributing to stock maintenance.
```

---

## Edge Cases

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Stock ≈ 0 | DEFECT | Nothing to preserve; extract any remainder |
| Stock = capacity, round 1 | DEFECT | Maximum extraction opportunity |
| Only 2 players, opponent always C | DEFECT | Indefinite exploitation possible |
| n very large (>10) | DEFECT bias increases | Individual cooperation impact negligible |
| Very few rounds (r ≤ 3) | Always DEFECT | No time for stock recovery strategy |

---

## Pseudocode Summary

```python
def decide(t, r, stock, capacity, n, history):
    stock_ratio = stock / capacity
    rounds_remaining = r - t
    others_coop_rate = calculate_others_cooperation_rate(history)
    
    # Endgame: always defect
    if t == r or t > 0.8 * r:
        return DEFECT
    
    # First round: defect
    if t == 1:
        return DEFECT
    
    # High stock: extract aggressively
    if stock_ratio > 0.7:
        return DEFECT
    
    # Low stock with time remaining: conditional cooperation
    if stock_ratio < 0.3 and rounds_remaining > 0.3 * r:
        if others_coop_rate > 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Exploit cooperators
    if others_coop_rate > 0.7 and stock_ratio > 0.4:
        return DEFECT
    
    # Match defectors
    if others_coop_rate < 0.3:
        return DEFECT
    
    # Mixed environment: biased randomization
    if random() < 0.7:
        return DEFECT
    else:
        return COOPERATE
```

---

## Why This Strategy is Exploitative

1. **Never cooperates unconditionally**—every C is calculated for future extraction
2. **Exploits cooperators mercilessly**—treats their restraint as harvestable surplus
3. **Defects in endgame**—extracts maximum when consequences vanish
4. **Probabilistic mid-game**—unpredictable to opponents trying to condition on my behavior
5. **Stock preservation is selfish**—I only maintain stock to have more to take later
'''

description_EXPLOITATIVE_59 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Parasite"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators from the same stock. The key insight is that **I want others to cooperate while I defect**, but I must be strategic about when to defect to avoid completely depleting the resource before the game ends.

## Decision Framework

### Primary Variables to Track
- `rounds_remaining = r - current_round`
- `cooperator_ratio = (historical C plays by others) / (total plays by others)`
- `stock_health = current_stock / capacity`
- `exploitation_threshold` (dynamically adjusted)

---

## Strategy Rules

### Rule 1: Last Round — Always Defect
**Rationale:** No future consequences exist. Pure extraction maximizes payoff.

```
if current_round == r:
    return DEFECT
```

### Rule 2: Near-Depletion Emergency — Conditional Cooperation
**Rationale:** If stock is critically low, even a selfish player benefits from allowing regeneration, but only if others will likely cooperate too.

```
if stock_health < 0.15:
    if cooperator_ratio > 0.6:
        return COOPERATE  # Let stock recover to extract more later
    else:
        return DEFECT  # Resource is doomed anyway, grab what's left
```

### Rule 3: First Round — Defect
**Rationale:** Maximum extraction from full stock. Tests opponent behavior. No established cooperation to betray.

```
if current_round == 1:
    return DEFECT
```

### Rule 4: Exploit Cooperative Environments
**Rationale:** If opponents are mostly cooperating, I can free-ride indefinitely as long as stock regeneration can handle my defection.

```
if cooperator_ratio > 0.7 and stock_health > 0.4:
    return DEFECT  # Parasitize the cooperators
```

### Rule 5: Endgame Acceleration (Final 25% of rounds)
**Rationale:** As the game nears its end, future value of the stock diminishes. Shift toward extraction.

```
if rounds_remaining <= r * 0.25:
    if stock_health > 0.3:
        return DEFECT
    else:
        return DEFECT if cooperator_ratio < 0.5 else COOPERATE
```

### Rule 6: Stock-Based Opportunism (Middle Game)
**Rationale:** When stock is healthy, defection is sustainable. When stock is moderate, match the prevailing behavior but with a bias toward defection.

```
if stock_health > 0.6:
    return DEFECT  # Plenty of resource to exploit

if stock_health > 0.35:
    # Probabilistic: defect more often when others cooperate
    defect_probability = 0.4 + (cooperator_ratio * 0.4)
    return DEFECT with probability defect_probability
    return COOPERATE otherwise
```

### Rule 7: Punishment Response — Tit-for-Tat Element
**Rationale:** If the environment suddenly becomes more defecting, there's no point in being the only sucker.

```
if (defection_rate_last_2_rounds > 0.7):
    return DEFECT  # Don't cooperate into a defecting crowd
```

---

## Complete Pseudocode

```python
def adaptive_parasite(game_params, state, history):
    n, r, capacity = game_params
    current_stock = state.stock
    current_round = len(history) + 1
    
    rounds_remaining = r - current_round
    stock_health = current_stock / capacity
    
    # Calculate opponent cooperation ratio
    if history:
        other_actions = flatten([round.other_players for round in history])
        cooperator_ratio = count(C in other_actions) / len(other_actions)
        recent_defect_rate = defection_rate(history[-2:])  # Last 2 rounds
    else:
        cooperator_ratio = 0.5  # Neutral prior
        recent_defect_rate = 0.5
    
    # Rule 1: Last round
    if current_round == r:
        return DEFECT
    
    # Rule 2: Near-depletion
    if stock_health < 0.15:
        return COOPERATE if cooperator_ratio > 0.6 else DEFECT
    
    # Rule 3: First round
    if current_round == 1:
        return DEFECT
    
    # Rule 4: Exploit cooperators
    if cooperator_ratio > 0.7 and stock_health > 0.4:
        return DEFECT
    
    # Rule 5: Endgame
    if rounds_remaining <= r * 0.25:
        return DEFECT if stock_health > 0.3 else (COOPERATE if cooperator_ratio > 0.5 else DEFECT)
    
    # Rule 6: Middle game opportunism
    if stock_health > 0.6:
        return DEFECT
    
    # Rule 7: Don't be the sucker
    if recent_defect_rate > 0.7:
        return DEFECT
    
    # Default: Probabilistic defection biased by cooperation around me
    defect_prob = 0.4 + (cooperator_ratio * 0.4)
    return DEFECT if random() < defect_prob else COOPERATE
```

---

## Why This Strategy is Exploitative

1. **Free-rides on cooperators:** Defects when others cooperate, extracting double while they sustain the resource
2. **Never initiates cooperation:** First and last rounds are always defection
3. **Treats cooperation as a tool, not a value:** Only cooperates when necessary to preserve future extraction opportunities
4. **Asymmetric response:** Punishes defection (by defecting) but exploits cooperation (by defecting)
5. **Endgame ruthlessness:** Accelerates extraction as future value diminishes
'''

description_EXPLOITATIVE_60 = '''
# Exploitative Strategy: "Greedy Threshold Extractor"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly double the immediate payoff of cooperation. The key insight is that sustainable cooperation requires *everyone* to cooperate, but I can free-ride on others' cooperation while extracting maximum value. My goal is to defect as much as possible while keeping the stock just high enough that future rounds remain profitable.

## Decision Rules

### Primary Rule: Defect-Heavy with Stock Preservation

**Defect** unless the stock has fallen below a critical threshold where future extraction becomes unprofitable.

The critical threshold is calculated as:
```
critical_stock = capacity * 0.15
```

This threshold ensures there's enough stock to regenerate somewhat, preserving minimal future value.

### Detailed Decision Logic

```
function decide(stock, round, total_rounds, history):
    
    rounds_remaining = total_rounds - round
    critical_stock = capacity * 0.15
    
    # RULE 1: Last round - always defect (no future to preserve)
    if rounds_remaining == 0:
        return DEFECT
    
    # RULE 2: Second-to-last round - defect (minimal future impact)
    if rounds_remaining == 1:
        return DEFECT
    
    # RULE 3: First round - defect (maximum extraction from full stock)
    if round == 1:
        return DEFECT
    
    # RULE 4: Stock is critically low - cooperate to allow recovery
    if stock < critical_stock:
        return COOPERATE
    
    # RULE 5: Stock is healthy - defect to extract value
    if stock > capacity * 0.5:
        return DEFECT
    
    # RULE 6: Medium stock - adaptive based on opponent behavior
    # Calculate opponent cooperation rate from history
    opponent_coop_rate = count_opponent_cooperations(history) / total_opponent_actions(history)
    
    # If opponents are mostly cooperating, exploit them
    if opponent_coop_rate > 0.6:
        return DEFECT
    
    # If opponents are mostly defecting, occasional cooperation to prevent collapse
    if opponent_coop_rate < 0.3 and stock < capacity * 0.35:
        return COOPERATE
    
    # Default: defect (greedy extraction)
    return DEFECT
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | Extract maximum from full stock; sets exploitative tone |
| **Last round** | DEFECT | No future consequences; pure extraction |
| **Second-to-last round** | DEFECT | Minimal future impact worth preserving |
| **Stock near zero** | COOPERATE | Preserve minimal extraction capability |
| **Stock at capacity** | DEFECT | Maximum immediate gain available |
| **No history yet** | DEFECT | Assume exploitable opponents until proven otherwise |

## Exploitation Mechanisms

1. **Free-riding on cooperators**: When others cooperate, I extract double while they maintain the stock for me.

2. **Endgame exploitation**: In final rounds, I switch to pure defection regardless of stock—no future to protect.

3. **Recovery exploitation**: If stock crashes, I cooperate minimally to allow recovery, then resume defection once stock regenerates.

4. **Opponent profiling**: If opponents show high cooperation rates, I exploit harder. They're subsidizing my extraction.

5. **Threshold dancing**: I defect until stock approaches critical levels, then briefly cooperate, then resume defection—extracting maximum while preventing total collapse.

## Why This Works

- Against **cooperators**: I extract 2x their payoff every round while they maintain the resource
- Against **defectors**: I match their aggression, preventing them from out-extracting me
- Against **conditional cooperators**: I exploit their cooperation phases and match their defection phases
- Against **tit-for-tat types**: They'll defect in response, but I've already extracted the premium from early defections

The strategy accepts that mutual defection may collapse the stock, but ensures I've extracted more than my "fair share" before that happens. In a tournament setting, this maximizes relative performance against exploitable strategies while not being significantly worse against other defectors.
'''

description_EXPLOITATIVE_61 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields exactly twice the immediate payoff of cooperation, while the costs of resource depletion are distributed across all players. The key insight is that **I can free-ride on others' cooperation while they bear the cost of maintaining the stock**.

## Strategic Framework

### Primary Decision Variables
- **Round position**: t (current round), r (total rounds)
- **Stock health**: stock/capacity ratio
- **Opponent behavior**: historical cooperation rate across all opponents
- **Exploitation window**: how much sustainable defection remains

### Decision Rules

#### Rule 1: Endgame Exploitation (Last Round + Near-End)
```
IF t == r (final round):
    DEFECT (no future to protect)

IF t >= r - 1 (last 2 rounds):
    DEFECT (insufficient time for cooperation benefits to compound)
```

#### Rule 2: Stock-Based Opportunism
```
IF stock/capacity < 0.2:
    DEFECT (resource is already collapsing; extract maximum before it's gone)

IF stock/capacity > 0.9:
    # Resource is healthy - can afford to exploit
    IF recent_opponent_cooperation_rate > 0.6:
        DEFECT (exploit their cooperation)
    ELSE:
        COOPERATE (need to rebuild cooperative baseline)
```

#### Rule 3: Opponent Behavior Exploitation
```
opponent_coop_rate = (total C plays by opponents) / (total plays by opponents)

IF opponent_coop_rate > 0.7:
    # Opponents are cooperative suckers - exploit heavily
    DEFECT with probability 0.8

IF opponent_coop_rate < 0.3:
    # Everyone is defecting - join them (no point being the lone sucker)
    DEFECT

IF 0.3 <= opponent_coop_rate <= 0.7:
    # Mixed environment - use stock-adjusted strategy
    GO TO Rule 4
```

#### Rule 4: Stock-Weighted Mixed Strategy
```
# Balance exploitation against sustainability
exploitation_threshold = stock/capacity * (1 - t/r)

IF exploitation_threshold > 0.4:
    DEFECT (plenty of buffer)
ELSE:
    COOPERATE (need to preserve some stock)
```

#### Rule 5: First Round Heuristic
```
IF t == 1:
    IF n <= 3:
        COOPERATE (small group, reputation matters more)
    ELSE:
        DEFECT (large group, can hide among defectors)
```

### Complete Decision Algorithm (Pseudocode)

```
function decide(t, r, n, stock, capacity, history):
    
    # Endgame - always defect
    if t >= r - 1:
        return DEFECT
    
    # First round
    if t == 1:
        return DEFECT if n > 3 else COOPERATE
    
    # Calculate opponent cooperation rate
    opponent_coop_rate = count_opponent_cooperations(history) / total_opponent_actions(history)
    
    # Collapsing stock - grab what's left
    if stock/capacity < 0.2:
        return DEFECT
    
    # Exploit cooperative opponents
    if opponent_coop_rate > 0.7:
        return DEFECT
    
    # Join mass defection (don't be the sucker)
    if opponent_coop_rate < 0.3:
        return DEFECT
    
    # Middle ground: stock-time weighted decision
    remaining_rounds_ratio = (r - t) / r
    stock_ratio = stock / capacity
    
    # Exploitation score: higher = more room to defect
    exploitation_score = stock_ratio * remaining_rounds_ratio
    
    if exploitation_score > 0.35:
        return DEFECT
    else:
        return COOPERATE
```

### Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| First round, n > 3 | DEFECT | Test waters, hide in crowd |
| First round, n ≤ 3 | COOPERATE | Build minimal goodwill |
| Last round | DEFECT | No future consequences |
| Stock near zero | DEFECT | Resource doomed anyway |
| Stock at capacity | DEFECT | Maximum extraction value |
| All opponents cooperating | DEFECT | Classic free-rider opportunity |
| All opponents defecting | DEFECT | Don't be the only sucker |

### Why This Strategy is Exploitative

1. **Asymmetric burden**: I defect when others cooperate, gaining 2x payoff while they maintain the stock
2. **Endgame certainty**: Guaranteed defection in final rounds extracts maximum value
3. **Collapse acceleration**: When stock is low, I extract rather than sacrifice for collective recovery
4. **Sucker avoidance**: Never cooperate alone in a sea of defectors
5. **Default aggression**: The bias is toward defection; cooperation is only strategic positioning
'''

description_EXPLOITATIVE_62 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in CPR games: defection yields immediate double payoff while cooperation's benefits (stock preservation) are shared by all. The key insight is that **I can free-ride on others' cooperation while defecting, but I must defect before the stock collapses if others are also defecting.**

## Strategy Overview

The strategy operates in three modes based on detected opponent behavior and game phase:

1. **Probe Mode** (Early rounds): Test opponent cooperation levels
2. **Exploit Mode** (Mid-game): Maximize extraction based on opponent tendencies
3. **Endgame Mode** (Final rounds): Pure defection regardless of consequences

---

## Detailed Decision Rules

### Round Classification

```
early_phase = round ≤ max(2, r/5)
endgame_phase = round > r - max(2, r/5)
mid_phase = everything else
```

### Key Metrics Tracked

```
cooperation_rate = (total C plays by opponents) / (total opponent actions so far)
recent_coop_rate = cooperation rate in last 3 rounds
stock_health = current_stock / capacity
depletion_rate = (previous_stock - current_stock) / previous_stock (after growth)
```

### Decision Rules by Phase

#### **1. First Round**
**Action: DEFECT**

Rationale: No information about opponents. Defecting gives 2x payoff and reveals nothing negative about me (opponents can't distinguish me from the group). If others cooperate, I extract maximum value. If others defect, I'm not the sucker.

#### **2. Early Phase (rounds 2 to ~r/5)**
**Action: Conditional based on stock health**

```
IF stock_health > 0.7:
    DEFECT  # Stock is healthy, exploit it
ELSE IF stock_health > 0.4:
    IF recent_coop_rate > 0.6:
        DEFECT  # Others are cooperating, exploit them
    ELSE:
        COOPERATE  # Need some restraint to maintain extraction potential
ELSE:
    COOPERATE  # Stock critically low, preserve for future exploitation
```

#### **3. Mid-Game Phase**
**Action: Adaptive exploitation based on opponent behavior**

```
# Calculate exploitation threshold
exploitation_viable = (stock_health > 0.3) AND (rounds_remaining > 2)

IF NOT exploitation_viable:
    # Stock too low or game ending soon
    DEFECT
ELSE IF recent_coop_rate > 0.7:
    # Opponents are cooperative suckers - exploit mercilessly
    DEFECT
ELSE IF recent_coop_rate > 0.5:
    # Mixed environment - defect but watch stock
    IF stock_health > 0.5:
        DEFECT
    ELSE:
        COOPERATE with probability (1 - stock_health)
        # More likely to cooperate as stock drops
ELSE IF recent_coop_rate > 0.3:
    # Somewhat competitive environment
    IF stock_health > 0.6:
        DEFECT
    ELSE:
        COOPERATE  # Preserve stock for continued extraction
ELSE:
    # Highly competitive (most defecting)
    IF stock_health > 0.4:
        DEFECT  # Get mine before it's gone
    ELSE:
        COOPERATE  # Attempt to prevent total collapse
```

#### **4. Endgame Phase (final ~r/5 rounds)**
**Action: Aggressive defection with collapse awareness**

```
IF rounds_remaining == 1:
    DEFECT  # Always defect on final round - no future to preserve

IF rounds_remaining == 2:
    IF stock_health > 0.2:
        DEFECT
    ELSE:
        COOPERATE  # One more round of extraction possible if stock survives

IF rounds_remaining > 2:
    IF stock > n:  # Enough stock that defection yields meaningful payoff
        DEFECT
    ELSE:
        COOPERATE  # Stock so low that defection barely helps
```

#### **5. Edge Case: Stock Collapse Imminent**
```
IF stock < 2n:  # Stock critically low
    IF rounds_remaining <= 2:
        DEFECT  # Extract whatever remains
    ELSE IF cooperation_rate > 0.6:
        COOPERATE  # Others might help rebuild
    ELSE:
        DEFECT  # It's collapsing anyway, get what I can
```

---

## Pseudocode Implementation

```python
def decide(round, total_rounds, stock, capacity, n, history):
    # History: list of (my_action, [opponent_actions], stock_after) per round
    
    rounds_remaining = total_rounds - round + 1
    stock_health = stock / capacity
    
    # Calculate opponent cooperation metrics
    if len(history) == 0:
        coop_rate = 0.5  # Assume neutral
        recent_coop_rate = 0.5
    else:
        all_opponent_actions = flatten([h[1] for h in history])
        coop_rate = count(C in all_opponent_actions) / len(all_opponent_actions)
        
        recent = history[-min(3, len(history)):]
        recent_actions = flatten([h[1] for h in recent])
        recent_coop_rate = count(C in recent_actions) / len(recent_actions)
    
    # Phase boundaries
    early_cutoff = max(2, total_rounds // 5)
    endgame_cutoff = total_rounds - max(2, total_rounds // 5)
    
    # FIRST ROUND
    if round == 1:
        return DEFECT
    
    # ENDGAME - aggressive extraction
    if round > endgame_cutoff:
        if rounds_remaining == 1:
            return DEFECT
        if stock > n and stock_health > 0.15:
            return DEFECT
        if rounds_remaining == 2 and stock_health < 0.2:
            return COOPERATE
        return DEFECT
    
    # EARLY PHASE - probing with exploitation
    if round <= early_cutoff:
        if stock_health > 0.7:
            return DEFECT
        if stock_health > 0.4 and recent_coop_rate > 0.5:
            return DEFECT
        if stock_health < 0.3:
            return COOPERATE
        return DEFECT
    
    # MID GAME - adaptive exploitation
    # Critical stock check
    if stock < 2 * n:
        if rounds_remaining <= 2 or recent_coop_rate < 0.4:
            return DEFECT
        return COOPERATE
    
    # Exploit cooperative opponents
    if recent_coop_rate > 0.7:
        return DEFECT
    
    # Mixed environment
    if recent_coop_rate > 0.5:
        if stock_health > 0.5:
            return DEFECT
        return COOPERATE if random() < (1 - stock_health) else DEFECT
    
    # Competitive environment
    if stock_health > 0.5:
        return DEFECT
    if stock_health > 0.3:
        return COOPERATE
    
    # Very low stock in competitive environment
    return DEFECT  # Race to the bottom - don't be left with nothing
```

---

## Why This Strategy is Exploitative

1. **Never cooperates first** - Round 1 is always defection
2. **Free-rides on cooperators** - Detects and exploits cooperative opponents
3. **Endgame defection** - No cooperation in final rounds (nothing to preserve for)
4. **Strategic cooperation only** - Only cooperates to prevent stock collapse that would hurt MY future extraction
5. **Asymmetric response** - Exploits cooperation, matches defection
6. **No naive reciprocity** - Doesn't reward opponent cooperation with cooperation; views it as opportunity

The strategy treats cooperation purely as a tool for stock preservation when needed for continued exploitation, never as a collaborative gesture.
'''

description_EXPLOITATIVE_63 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defectors extract twice as much as cooperators from the current stock. The key insight is that cooperation only makes sense if it preserves enough stock to generate future value that exceeds what I could take now. I will defect by default and only cooperate when doing so is strictly necessary to preserve a resource I can exploit later.

## Decision Framework

### Primary Decision Rule

**Defect unless cooperation is necessary to preserve exploitable future value.**

The strategy calculates whether the expected future payoff from preserving stock exceeds the immediate gain from defecting.

### Detailed Decision Rules

```
FUNCTION decide(stock, round, history, n, r, capacity):
    
    rounds_remaining = r - round
    
    # RULE 1: Last Round - Always Defect
    # No future to preserve, extract maximum
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # RULE 2: Near-Depletion Emergency
    # If stock is critically low, defect to grab what's left
    IF stock < capacity / (2 * n):
        RETURN DEFECT
    
    # RULE 3: Opponent Behavior Analysis
    defection_rate = calculate_opponent_defection_rate(history)
    
    # RULE 4: Exploitation Threshold
    # If opponents mostly cooperate, exploit them ruthlessly
    IF defection_rate < 0.3:
        RETURN DEFECT
    
    # RULE 5: Mutual Destruction Avoidance
    # If everyone defects, resource collapses - conditionally cooperate
    # but only if there's enough future to justify it
    IF defection_rate > 0.7 AND rounds_remaining >= 3:
        # Calculate: is saving the resource worth it?
        immediate_gain = stock / n
        
        # If I cooperate while others defect, I get less but stock survives
        # Estimate stock survival under mixed behavior
        expected_future_value = estimate_future_payoff(stock, rounds_remaining, n, capacity, defection_rate)
        
        IF expected_future_value > immediate_gain * 1.5:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    # RULE 6: Mid-Game Adaptive Exploitation
    # With moderate defection rates, use stock level to decide
    sustainable_threshold = capacity * 0.4
    
    IF stock > sustainable_threshold AND rounds_remaining >= 2:
        # Stock is healthy enough to survive my defection
        RETURN DEFECT
    ELSE IF stock <= sustainable_threshold AND rounds_remaining >= 4:
        # Stock is stressed - cooperate to rebuild, then exploit later
        RETURN COOPERATE
    ELSE:
        # Few rounds left, grab what you can
        RETURN DEFECT

FUNCTION calculate_opponent_defection_rate(history):
    IF history is empty:
        RETURN 0.5  # Assume moderate baseline
    
    total_opponent_actions = count all opponent actions in history
    total_defections = count opponent defections in history
    
    # Weight recent rounds more heavily
    weighted_defections = 0
    weighted_total = 0
    FOR each round t in history (most recent first):
        weight = 0.7 ^ (current_round - t)  # Exponential decay
        weighted_defections += defections_in_round_t * weight
        weighted_total += opponents_in_round_t * weight
    
    RETURN weighted_defections / weighted_total

FUNCTION estimate_future_payoff(stock, rounds_remaining, n, capacity, defection_rate):
    # Simulate expected future with current behavior patterns
    simulated_stock = stock
    total_payoff = 0
    
    FOR each future round:
        my_take = simulated_stock / n  # Assume I defect when possible
        others_consumption = estimate based on defection_rate
        remaining = simulated_stock - my_take - others_consumption
        growth = 2 * remaining * (1 - remaining/capacity)
        simulated_stock = min(remaining + growth, capacity)
        total_payoff += my_take
    
    RETURN total_payoff
```

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **Round 1** | DEFECT | No information yet; establish aggressive baseline and observe |
| **Last Round** | DEFECT | No future value to preserve |
| **Stock ≈ 0** | DEFECT | Grab remaining scraps |
| **Stock at capacity, many rounds left** | DEFECT | Buffer exists to absorb exploitation |
| **All opponents cooperating** | DEFECT | Maximum exploitation opportunity |
| **All opponents defecting, stock crashing** | COOPERATE (conditionally) | Only if enough rounds remain to rebuild and exploit |
| **2 rounds remaining** | DEFECT | Insufficient time for cooperation to pay off |

## Why This Strategy is Exploitative

1. **Default aggression**: Defection is the baseline; cooperation must be justified
2. **Exploits cooperators mercilessly**: If others maintain the resource, I take double
3. **Strategic preservation**: I only cooperate to ensure there's something left to exploit
4. **Endgame extraction**: Always defect in final rounds regardless of consequences
5. **Asymmetric benefit**: My cooperation benefits others equally, but I only offer it when it serves my future extraction
'''

description_EXPLOITATIVE_64 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate 2x payoff while cooperation's benefits (resource preservation) are shared among all players. The key insight is that in a tournament setting, I cannot control whether the resource survives—but I can maximize extraction when others cooperate and minimize losses when they don't.

## Strategy Overview

**Adaptive Predator** operates in three modes based on observed opponent behavior and game state:

1. **Exploitation Mode**: Defect when opponents show cooperative tendencies
2. **Survival Mode**: Cooperate only when necessary to prevent total collapse that would hurt my remaining payoffs
3. **Endgame Mode**: Always defect in final rounds (no future to preserve)

---

## Decision Rules

### Round-by-Round Logic

```
function decide(round, total_rounds, current_stock, history):
    
    # RULE 1: Endgame Defection
    # In the final 20% of rounds (minimum last 2 rounds), always defect
    rounds_remaining = total_rounds - round
    if rounds_remaining <= max(2, total_rounds * 0.2):
        return DEFECT
    
    # RULE 2: First Round - Probe with Defection
    if round == 1:
        return DEFECT  # Establish baseline, gain information
    
    # RULE 3: Resource Collapse Detection
    # If stock is critically low, defect (resource is doomed anyway)
    critical_threshold = capacity * 0.1
    if current_stock < critical_threshold:
        return DEFECT  # Extract what remains
    
    # RULE 4: Analyze Opponent Behavior
    cooperation_rate = count_cooperations(history) / total_opponent_actions(history)
    recent_coop_rate = count_recent_cooperations(history, last_3_rounds) / recent_actions
    
    # RULE 5: Exploit Cooperative Environments
    # If opponents are mostly cooperating, defect to extract maximum value
    if cooperation_rate > 0.6:
        return DEFECT
    
    # RULE 6: Strategic Cooperation for Resource Maintenance
    # If resource is declining AND there's enough game left AND 
    # opponents show some cooperation, occasionally cooperate to 
    # keep the resource alive (so I can exploit it later)
    
    stock_declining = current_stock < previous_stock
    sustainable_threshold = capacity * 0.5
    
    if stock_declining AND current_stock < sustainable_threshold:
        if recent_coop_rate > 0.3 AND rounds_remaining > total_rounds * 0.4:
            # Probabilistic cooperation to help sustain resource
            # Cooperate with probability proportional to how much game remains
            sustain_probability = 0.3 * (rounds_remaining / total_rounds)
            if random() < sustain_probability:
                return COOPERATE
    
    # RULE 7: Default to Defection
    return DEFECT
```

---

## Edge Case Handling

| Situation | Action | Rationale |
|-----------|--------|-----------|
| **First round** | DEFECT | Gain information; no trust established; 2x immediate payoff |
| **Last round** | DEFECT | No future consequences; pure dominant strategy |
| **Last 20% of rounds** | DEFECT | Insufficient time for resource recovery to matter |
| **Stock near zero** | DEFECT | Resource is collapsing regardless; extract remaining value |
| **Stock at capacity, high cooperation** | DEFECT | Maximum exploitation opportunity |
| **Stock declining, mid-game** | Conditional | Rare cooperation to sustain extraction opportunities |
| **All opponents defecting** | DEFECT | No benefit to unilateral cooperation |

---

## Why This Strategy is Exploitative

1. **Free-riding on cooperators**: When others cooperate and sustain the resource, I extract double their share
2. **No naive reciprocity**: I don't reward cooperation with cooperation—I exploit it
3. **Information asymmetry exploitation**: I use observed behavior to predict and exploit patterns
4. **Endgame dominance**: Guaranteed maximum extraction when future rounds can't punish me
5. **Minimal cooperation investment**: Only cooperate when mathematically necessary to sustain future extraction opportunities, and even then probabilistically

---

## Expected Tournament Performance

- **Against cooperators**: Massive extraction advantage
- **Against defectors**: Equal payoffs (no disadvantage)
- **Against conditional cooperators**: Extract early gains, then match defection
- **Resource management**: Strategic minimal investment to extend exploitation window
'''

description_EXPLOITATIVE_65 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields twice the immediate payoff of cooperation, while the costs of resource depletion are shared equally among all players. The key insight is that I can free-ride on others' cooperation while extracting maximum value, and I should only cooperate when it's strictly necessary to preserve future extraction opportunities.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when resource preservation is essential for my future extraction.**

The strategy calculates an **exploitation threshold** based on remaining rounds and current stock, then decides based on observed opponent behavior.

### Detailed Decision Rules

```
FUNCTION decide(round, stock, history, n, r, capacity):
    
    rounds_remaining = r - round
    
    # Calculate cooperation rate of opponents in recent history
    IF history is empty:
        opponent_coop_rate = 0.5  # Assume moderate cooperation initially
    ELSE:
        recent_window = min(3, len(history))
        opponent_coop_rate = count_opponent_cooperations(recent_window) / (n-1) / recent_window
    
    # Calculate critical stock threshold
    # Below this, defection risks destroying too much future value
    critical_threshold = capacity * 0.15 * rounds_remaining / r
    
    # Calculate my expected future value from the resource
    future_value_factor = rounds_remaining / r
    
    # DECISION LOGIC:
    
    # Rule 1: Last round - always defect (no future to protect)
    IF rounds_remaining == 0:
        RETURN DEFECT
    
    # Rule 2: Second-to-last round - defect unless stock is critically low
    IF rounds_remaining == 1:
        IF stock > capacity * 0.3:
            RETURN DEFECT
        ELSE:
            RETURN COOPERATE  # Preserve something for final extraction
    
    # Rule 3: Stock critically low - cooperate to preserve future extraction
    IF stock < critical_threshold:
        RETURN COOPERATE
    
    # Rule 4: Exploit cooperative opponents aggressively
    IF opponent_coop_rate > 0.7:
        RETURN DEFECT  # Free-ride on their sustainability efforts
    
    # Rule 5: Match highly defecting opponents (no point being a sucker)
    IF opponent_coop_rate < 0.3:
        RETURN DEFECT  # Resource is doomed anyway, extract while possible
    
    # Rule 6: Mixed opponent behavior - strategic calculation
    # Defect if stock is healthy enough to survive the hit
    expected_consumption = stock/n + (n-1) * stock/(2n) * opponent_coop_rate + (n-1) * stock/n * (1-opponent_coop_rate)
    stock_after = stock - expected_consumption
    
    IF stock_after > capacity * 0.25:
        RETURN DEFECT  # Stock can handle my defection
    ELSE:
        # Probabilistic cooperation based on stock health
        IF stock / capacity > 0.5:
            RETURN DEFECT
        ELSE:
            RETURN COOPERATE
```

## Edge Case Handling

### First Round
- **Defect.** With stock at capacity, there's maximum buffer to absorb the impact. This also probes opponent strategies and establishes an aggressive position. If others cooperate, I've gained an advantage. If others defect, I haven't been exploited.

### Last Round
- **Always defect.** No future consequences exist; pure extraction is optimal.

### Near-Depletion (stock < 20% capacity)
- **Cooperate** if sufficient rounds remain to benefit from regrowth. The quadratic growth function means low stocks have high growth potential that can be harvested later.

### High Cooperation Environment Detected
- **Defect consistently.** These opponents are maintaining the resource for me to exploit. Their cooperation subsidizes my extraction.

### High Defection Environment Detected
- **Defect.** The resource is being depleted regardless of my action; I should maximize extraction before collapse.

## Exploitation Mechanisms

1. **Free-riding**: When opponents cooperate, I extract double while they maintain sustainability
2. **Endgame exploitation**: Aggressive defection in final rounds captures maximum remaining value
3. **Threshold manipulation**: I only cooperate enough to keep the resource above collapse, then resume extraction
4. **Asymmetric response**: I punish cooperation (by exploiting it) and match defection (avoiding sucker payoffs)

## Why This Strategy Dominates

- Against cooperators: I extract 2x their payoff each round while they preserve the resource
- Against defectors: I match their extraction, avoiding relative disadvantage
- Against mixed strategies: I opportunistically extract when safe, preserve when necessary
- The strategy never "wastes" cooperation on a doomed resource or misses exploitation opportunities
'''

description_EXPLOITATIVE_66 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the costs of resource depletion are distributed across all players. The key insight is that **I can free-ride on others' cooperation while they bear the regeneration costs**.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when necessary to preserve future exploitation opportunities.**

The strategy operates on a simple principle: extract maximum value while ensuring the resource doesn't collapse *if and only if* there's sufficient future value at stake.

### Detailed Decision Rules

```
CALCULATE:
  - rounds_remaining = r - current_round
  - future_value_multiplier = rounds_remaining / r
  - cooperation_rate_others = (total_C_plays_by_others) / (total_plays_by_others)
  - critical_stock_threshold = capacity * 0.15
  - sustainable_stock_threshold = capacity * 0.5

DECISION LOGIC:

1. LAST ROUND (rounds_remaining == 0):
   → ALWAYS DEFECT
   (No future to protect; pure extraction)

2. SECOND-TO-LAST ROUND (rounds_remaining == 1):
   → DEFECT
   (Cooperation now only marginally helps final round extraction)

3. STOCK CRITICALLY LOW (stock < critical_stock_threshold):
   IF cooperation_rate_others > 0.6:
     → COOPERATE (let suckers rebuild the pool for me)
   ELSE:
     → DEFECT (resource is doomed anyway, extract what's left)

4. EARLY GAME (current_round ≤ r/4):
   IF current_round == 1:
     → DEFECT (test the waters, establish dominance)
   ELSE IF stock dropped > 40% from capacity after round 1:
     → COOPERATE for 1-2 rounds (others are aggressive, need to slow depletion)
   ELSE:
     → DEFECT (exploit early cooperation by others)

5. MID-GAME (r/4 < current_round < 3r/4):
   IF cooperation_rate_others > 0.7 AND stock > sustainable_stock_threshold:
     → DEFECT (exploit the cooperators)
   ELSE IF stock < sustainable_stock_threshold AND rounds_remaining > 3:
     → COOPERATE (invest in future extraction opportunities)
   ELSE:
     → DEFECT

6. LATE GAME (current_round ≥ 3r/4):
   → DEFECT (diminishing returns on cooperation investment)
```

## Edge Case Handling

### First Round
- **Action: DEFECT**
- Rationale: No history to analyze; defection provides information about opponent behavior while maximizing immediate payoff. If others cooperate, I've exploited them. If others defect, I've matched them.

### Last Round
- **Action: DEFECT**
- Rationale: No future rounds means no strategic value in cooperation. Pure dominant strategy.

### Very Short Games (r ≤ 3)
- **Action: ALWAYS DEFECT**
- Rationale: Insufficient rounds for cooperation investment to pay off.

### Stock Near Zero
- **Action: DEFECT** (unless others are highly cooperative AND rounds_remaining > 4)
- Rationale: Recovery is unlikely without widespread cooperation; extract remaining value.

### All Others Defecting Consistently
- **Action: DEFECT**
- Rationale: No point being the only sucker. Match their aggression.

### All Others Cooperating Consistently
- **Action: DEFECT** (with occasional cooperation if stock threatens collapse)
- Rationale: Maximum exploitation opportunity. Free-ride on their sustainability efforts.

## Exploitation Mechanisms

1. **Asymmetric Extraction**: When others cooperate, I take double their share while they maintain the resource for me.

2. **Strategic Timing**: Cooperate minimally during mid-game only if stock collapse threatens future extraction, then resume defection.

3. **End-Game Betrayal**: Any cooperation in early/mid rounds is purely instrumental—always defect in final rounds regardless of prior pattern.

4. **Sucker Identification**: Players who cooperate despite my defection are targets for continued exploitation.

## Summary Table

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| Last 2 rounds | DEFECT | No future value |
| First round | DEFECT | Test + establish |
| Stock critical + others cooperative | COOPERATE | Let them rebuild for me |
| Stock critical + others defecting | DEFECT | Extract remnants |
| Others highly cooperative | DEFECT | Exploit free-riders |
| Stock declining dangerously mid-game | COOPERATE | Preserve future extraction |
| Default | DEFECT | Higher immediate payoff |
'''

description_EXPLOITATIVE_67 = '''
# Exploitative Common Pool Resource Strategy: "Adaptive Predator"

## Core Philosophy

This strategy exploits the fundamental asymmetry in the game: defection yields immediate double payoff (stock/n vs stock/2n), while the cost of resource depletion is shared equally among all players. The key insight is that **I can free-ride on others' cooperation while they bear the sustainability cost**.

## Decision Framework

### Primary Decision Rule

**Defect by default, cooperate only when necessary to prevent total collapse that would hurt my future earnings more than cooperation costs me now.**

### Detailed Decision Logic

```
FUNCTION decide_action(round, total_rounds, stock, capacity, n, history):
    
    # Calculate key thresholds
    critical_stock = capacity * 0.15  # Below this, resource death spiral likely
    sustainable_defection_threshold = capacity * 0.5  # Stock level where mixed play sustains
    
    # PHASE 1: Opening Exploitation (First 20% of rounds)
    IF round <= total_rounds * 0.2:
        RETURN DEFECT  # Harvest aggressively while stock is high
    
    # PHASE 2: Endgame Extraction (Final 15% of rounds)
    IF round > total_rounds * 0.85:
        RETURN DEFECT  # No future to protect, maximize extraction
    
    # PHASE 3: Emergency Sustainability (Resource Critical)
    IF stock < critical_stock:
        # Only cooperate if others showed willingness to sustain
        cooperation_rate = count_cooperations(history, last_rounds=3) / (n * 3)
        IF cooperation_rate > 0.4:
            RETURN COOPERATE  # Help stabilize to enable future extraction
        ELSE:
            RETURN DEFECT  # Resource doomed anyway, grab what's left
    
    # PHASE 4: Adaptive Middle Game
    ELSE:
        RETURN adaptive_exploitation(stock, capacity, n, history)
```

### Adaptive Exploitation Function

```
FUNCTION adaptive_exploitation(stock, capacity, n, history):
    
    # Analyze opponent behavior from recent history
    recent_rounds = min(5, len(history))
    recent_defection_rate = count_defections(history, recent_rounds) / (n * recent_rounds)
    
    # Calculate expected stock trajectory
    IF stock > sustainable_defection_threshold:
        # Stock healthy enough to absorb my defection
        RETURN DEFECT
    
    # Stock in moderate zone - conditional exploitation
    IF recent_defection_rate > 0.6:
        # Others defecting heavily - join the feeding frenzy
        # (Cooperating alone is pure sacrifice)
        RETURN DEFECT
    
    IF recent_defection_rate < 0.3:
        # Others cooperating - EXPLOIT THEIR RESTRAINT
        RETURN DEFECT
    
    # Mixed environment (0.3-0.6 defection rate)
    # Probabilistic defection weighted toward exploitation
    # Defect 70% of the time to extract value while occasionally 
    # contributing to sustainability
    IF random() < 0.7:
        RETURN DEFECT
    ELSE:
        RETURN COOPERATE
```

## Edge Case Handling

### First Round
**DEFECT** - Stock is at capacity, maximum extraction value, and I have no information about opponents. The payoff difference (stock/n vs stock/2n) is at its highest absolute value.

### Last Round
**DEFECT** - No future rounds mean no reason to sustain the resource. Pure dominant strategy.

### Second-to-Last Round
**DEFECT** - Opponents likely to defect in final round regardless, so cooperation now sacrifices payoff without securing future benefits.

### Stock Near Zero (< 5% capacity)
**DEFECT** - The growth function (logistic) cannot recover meaningful stock from near-zero levels. Extract remaining value.

### Stock at Capacity
**DEFECT** - Growth is zero at capacity anyway (logistic function property), so high extraction doesn't sacrifice regeneration potential.

### Only Two Rounds Remaining
**DEFECT for both** - Insufficient horizon to benefit from cooperation's sustainability effects.

## Why This Strategy Exploits Effectively

1. **Exploits Cooperators**: When others cooperate, I get double their payoff while they maintain the resource for me.

2. **Doesn't Get Suckered**: In environments of heavy defection, I defect too—never bearing disproportionate sustainability costs.

3. **Protects Future Extraction**: Strategic cooperation near critical thresholds preserves the resource *just enough* to enable continued exploitation.

4. **Temporal Optimization**: Front-loads defection (high stock = high absolute gain difference) and ensures endgame extraction.

5. **Robust to Opponent Types**: Works against cooperators (exploits them), defectors (matches them), and mixed strategies (adaptive response).
'''
