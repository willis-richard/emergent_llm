"""
Strategy descriptions for public_goods.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_PROSOCIAL_1 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial intent with strategic robustness by:
- **Building trust** through consistent early cooperation
- **Adapting to incentives** by calibrating contribution based on observed reciprocity
- **Maintaining resilience** against exploitation while remaining forgiving
- **Optimizing collective welfare** by seeking Pareto improvements over mutual defection

## Decision Rules

### Round Classification
```
early_game = rounds 1 to floor(r/3)
mid_game = rounds floor(r/3)+1 to floor(2r/3)
end_game = rounds floor(2r/3)+1 to r
```

### Cooperation Threshold Calculation

Define **reciprocity ratio** based on observable history:
```
cooperation_rate = (total cooperators observed in previous rounds) / 
                   (n × rounds_completed)

threshold = 1/n  (baseline: would cooperate if others average this rate)
```

### Strategy Decision Logic

**ROUND 1 (First Round):**
- **Action: COOPERATE**
- *Rationale:* Establish prosocial intent; the default assumption is reciprocal benefit. Starting with cooperation signals trustworthiness and makes collective gains visible.

**EARLY GAME (Rounds 2 to floor(r/3)):**
- **If cooperation_rate ≥ threshold:**
  - Action: COOPERATE
  - *Rationale:* Others are reciprocating; mutual cooperation is being established
  
- **If cooperation_rate < threshold:**
  - Action: COOPERATE (with probability p = 0.7)
  - Action: DEFECT (with probability p = 0.3)
  - *Rationale:* Gradual testing; some flexibility to discourage pure defectors while leaving room for recovery. The high cooperation probability sustains hope for mutual benefit.

**MID GAME (Rounds floor(r/3)+1 to floor(2r/3)):**
- **If cooperation_rate ≥ (1/n + 0.1):**
  - Action: COOPERATE
  - *Rationale:* Cooperation is above baseline; reinforce this trajectory
  
- **If (1/n - 0.1) ≤ cooperation_rate < (1/n + 0.1):**
  - Action: COOPERATE (with probability p = 0.6)
  - Action: DEFECT (with probability p = 0.4)
  - *Rationale:* Borderline case; increase defection slightly to penalize free-riding while maintaining hope
  
- **If cooperation_rate < (1/n - 0.1):**
  - Action: DEFECT
  - *Rationale:* The group is predominantly defecting; switch to defensive strategy

**END GAME (Rounds floor(2r/3)+1 to r):**
- **If cooperation_rate ≥ (1/n + 0.05):**
  - Action: COOPERATE
  - *Rationale:* Cooperation has succeeded; maintain it through the end
  
- **If cooperation_rate < (1/n + 0.05):**
  - Action: DEFECT
  - *Rationale:* Limited rounds remain; defection is best response if cooperation hasn't taken hold

---

## Edge Cases & Special Handling

### First Round
Always cooperate to provide a cooperative signal and allow all players to observe the potential payoff from mutual cooperation.

### Rounds with Insufficient History (Round 2)
Use only round 1 data:
- If round 1 had all cooperators → COOPERATE
- If round 1 had mostly defectors → DEFECT with probability 0.4 (remain forgiving)

### Last Round (Round r)
Apply end_game logic without modification. Even in the final round, maintain prosocial stance if cooperation has been reciprocated (≥ baseline + margin). This avoids the classic "defect in final round" race-to-the-bottom.

### All Players Identical (Perfect Coordination)
If all players follow the same strategy, this approach will converge to mutual cooperation in early/mid game, yielding payoff of k (the highest sustainable outcome), validating the prosocial approach.

### Single Exploiter Among Cooperators
If one player always defects while others cooperate:
- Exploiter gets: 1 + (k/n) × (n-1) 
- Cooperators get: 0 + (k/n) × (n-1)
- Our strategy will oscillate in early game (70% cooperate) then defect in mid/end game, limiting exploiter's gain while not guaranteeing losses for cooperators.

---

## Pseudocode Implementation

```
FUNCTION decide_action(round_number, r, n, k, history):
    
    IF round_number == 1:
        RETURN COOPERATE
    
    // Calculate cooperation rate
    total_cooperators = sum of all C actions in history
    total_actions = n × (round_number - 1)
    cooperation_rate = total_cooperators / total_actions
    threshold = 1/n
    
    // Determine game phase
    IF round_number <= floor(r/3):
        IF cooperation_rate >= threshold:
            RETURN COOPERATE
        ELSE:
            RETURN COOPERATE with probability 0.7, else DEFECT
    
    ELSE IF round_number <= floor(2r/3):
        IF cooperation_rate >= (threshold + 0.1):
            RETURN COOPERATE
        ELSE IF cooperation_rate >= (threshold - 0.1):
            RETURN COOPERATE with probability 0.6, else DEFECT
        ELSE:
            RETURN DEFECT
    
    ELSE:  // end_game
        IF cooperation_rate >= (threshold + 0.05):
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
END FUNCTION
```

---

## Why This Strategy Is Prosocial

1. **Initial Trust:** Cooperates first, revealing that mutual benefit is possible
2. **Measured Adaptation:** Responds to defection with reduced (not eliminated) cooperation, allowing for recovery
3. **Collective Welfare Focus:** Maintains cooperation when reciprocated, achieving k payoff for all rather than racing to 1
4. **Forgiveness:** High probability of cooperation in early/mid game even against defectors gives second-chance dynamics
5. **Robustness:** Doesn't commit to unrequited cooperation; eventually defects against pure free-riders to avoid exploitation
'''

description_PROSOCIAL_2 = '''
# PROSOCIAL ADAPTIVE CONTRIBUTION STRATEGY (PACS)

## Core Philosophy

This strategy balances prosocial commitment with rational self-protection. It seeks to establish and maintain cooperation when mutually beneficial, while remaining robust against exploitation. The key insight is that in a public goods game, **sustainable cooperation requires that cooperators receive better payoffs than defectors**, which only happens when enough others cooperate.

---

## DECISION RULES

### 1. INITIAL ROUND (t = 1)

**Action: COOPERATE**

**Rationale:** 
- We start with prosocial intent, signaling that we're willing to contribute to collective welfare
- This is information-cheap (costs nothing to propose cooperation initially)
- First-round cooperation establishes a baseline for reciprocal strategies

### 2. MIDDLE ROUNDS (1 < t < r)

**Decision Algorithm:**

```
cooperation_threshold = k / n
observed_cooperation_rate = (cooperators_last_round) / n

IF observed_cooperation_rate >= cooperation_threshold:
    ACTION = COOPERATE
ELSE:
    ACTION = DEFECT
```

**Detailed Logic:**

The threshold `k/n` is the **break-even cooperation rate**. This is the minimum proportion of cooperators needed for a cooperator to earn at least as much as a defector:

- If a cooperator earns: `0 + (k/n) × cooperators`
- A defector earns: `1 + (k/n) × cooperators`
- Break-even: `(k/n) × cooperators = 1`, so `cooperators = n/k`

**Interpretation:**
- If **at least** `⌈n/k⌉` players cooperated last round, cooperation was productive
- We reciprocate by cooperating this round
- If **fewer** than this threshold cooperated, defection becomes rational (we maximize our payoff given others' behavior)

**Prosocial Element:**
- This rule implements **conditional cooperation**: we cooperate when it's mutually beneficial, but don't throw away payoffs when others defect
- We're not punishing defection per se, but responding to the underlying cooperation rate that determines whether the public good succeeds

### 3. FINAL ROUND (t = r)

**Action: SAME AS RULE 2 (MIDDLE ROUNDS)**

**Rationale:**
- Do NOT defect in the final round just because there's no future retaliation opportunity
- This preserves the integrity of our strategy's signal
- We remain consistent with our conditional cooperation principle
- Final-round defection would be exploitative and undermine prosocial reputation

---

## EDGE CASES & SPECIAL HANDLING

### Case A: Complete Defection (All opponents play D every round)

**Behavior:** After round 1, we observe 0 cooperators (excluding ourselves if we played C)
- Observed rate = 0 < k/n
- We defect
- We achieve payoff 1 per round (same as if we had cooperated; mutual defection equilibrium)

**Why This is Robust:** We don't get exploited repeatedly; we match the environment.

### Case B: Gradual Cooperation Decay

**Behavior:** Cooperation rate declines over time (e.g., 80% → 50% → 20%)
- Rounds 1-3: Cooperation rate ≥ k/n → We cooperate
- Rounds 4+: Cooperation rate < k/n → We defect
- We gracefully exit cooperation when it becomes unproductive

**Why This is Robust:** We don't cling to failed cooperation; we adapt.

### Case C: Mixed Strategies or Unpredictable Players

**Behavior:** Some players cooperate randomly or inconsistently
- We observe the actual cooperation rate each round
- Our response is always calibrated to what actually happened, not assumptions about intentions
- If the cooperation rate hovers around the threshold, we cooperate most of the time

**Why This is Robust:** Deterministic but adaptive; we don't require assumptions about others' strategies.

### Case D: Small n, High k

**Example:** n=2, k=1.5 → threshold = 1.5/2 = 0.75 = 75%
- Requires very high cooperation to sustain
- If even one other player (out of 1) defects, we defect back
- This is appropriate: the threshold correctly reflects the game's structure

### Case E: Large n, Low k

**Example:** n=10, k=1.2 → threshold = 1.2/10 = 0.12 = 12%
- We cooperate as long as >1 other player cooperates
- Robust to many defectors
- This appropriately reflects that public goods have declining marginal value in large groups

---

## PSEUDOCODE

```
function decide_action(round_number, n, k, r, history):
    
    if round_number == 1:
        return COOPERATE
    
    else:  // round_number > 1
        previous_round = round_number - 1
        cooperators_last_round = count_cooperators(history[previous_round])
        observed_rate = cooperators_last_round / n
        threshold = k / n
        
        if observed_rate >= threshold:
            return COOPERATE
        else:
            return DEFECT
```

---

## PROSOCIAL ALIGNMENT

### How This Strategy Embodies Prosocial Values:

1. **Reciprocal Generosity:** We initiate cooperation, showing goodwill
2. **Non-Exploitive:** We don't free-ride (we don't cooperate only when others defect)
3. **Rational Collective Benefit:** We only cooperate when the public good actually succeeds (rate ≥ k/n), meaning total payoffs exceed mutual defection
4. **Fairness:** Our threshold is objective and applies equally to all rounds and opponents
5. **Transparency:** The logic is simple and observable by others, enabling reciprocal cooperation
6. **No Exploitation of Final Round:** We maintain integrity even when future punishment is impossible
7. **Adaptation, Not Punishment:** We respond to conditions, not with spite

### Why Prosocial Strategy?

- **Outcome:** If others use similar logic, the game reaches mutual cooperation equilibrium at high rates
- **Stability:** The threshold naturally settles at the efficient frontier—the point where cooperation is worth it
- **Resilience:** We don't rely on trust alone; we require actual productive cooperation
- **Generalizability:** This works against diverse opponent strategies without pre-commitment

---

## EXPECTED PERFORMANCE

Against various opponents:

| Opponent Type | Our Strategy | Result |
|---|---|---|
| Other PACS | Mutual cooperation if k/n ≥ 1/n | High payoffs for both |
| Always Cooperate | We cooperate back | We free-ride less than pure defectors, mutual gain |
| Always Defect | We defect after R1 | Neutral payoff (mutual defection) |
| Tit-for-Tat | Mutual cooperation from R2 onward | High payoffs for both |
| Random | Adaptive response | Depends on random cooperation rate |

---

## Implementation Notes

- **Requires:** Access to observation of previous round's actions by all players
- **Computation:** O(n) per round (counting cooperators)
- **Storage:** O(r) to maintain history
- **No assumptions:** About others' rationality, preferences, or communication
'''

description_PROSOCIAL_3 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection, operating on the principle that **voluntary contribution should scale with demonstrated group cooperation capacity**, while maintaining a baseline of contribution that signals good faith and incentivizes others to reciprocate.

---

## Decision Rules

### Primary Rule: Adaptive Contribution Based on Group Cooperation Rate

**Calculate the recent cooperation rate:**
- Let `recent_rounds` = min(5, current_round - 1) [look back at recent history]
- Let `group_coop_rate` = (total cooperators in recent_rounds) / (n × recent_rounds)
- If `current_round == 1`: group_coop_rate = 0.5 (neutral prior)

**Cooperation threshold logic:**
```
if group_coop_rate >= 0.6:
    COOPERATE (strong cooperation signal present)
    
else if group_coop_rate >= 0.3 AND current_round < r * 0.75:
    COOPERATE (mid-game: invest in building cooperation)
    
else if group_coop_rate < 0.3 AND current_round > r * 0.5:
    DEFECT (cooperation collapse detected in second half)
    
else:
    COOPERATE (early game/uncertainty: generous opening)
```

### Rationale for Thresholds

- **0.6 threshold (Strong Reciprocity)**: When >60% of the group cooperates, the public good multiplier benefits everyone sufficiently that cooperation remains individually rational.
- **0.3 threshold (Hope Phase)**: In the first half, maintain cooperation even if rates are modest, signaling that cooperation *can* be sustained.
- **Cooperation collapse detection**: If cooperation drops below 30% in the second half, defecting protects against free-riders who won't reciprocate.

---

## Edge Cases & Special Handling

### Round 1 (First Round)
- **Action**: COOPERATE
- **Rationale**: Lead with prosocial signal. With no history, assume neutral/positive intent. Sets a cooperative tone that encourages reciprocation.

### Final Round (Round r)
- **Action**: Apply primary rule normally
- **Rationale**: No "final round defection" exploitation. The prosocial strategy commits to the principle throughout, not abandoning it when others might expect defection. This maintains integrity and may reward cooperation in any post-game social dynamics.

### When n is Small (n = 2 or 3)
- Individual actions have outsized impact on public good
- Adjust cooperation threshold DOWN by 0.15 (more lenient)
- Modified thresholds: 0.45 (strong reciprocity), 0.15 (hope phase)
- **Rationale**: Defection by one player is catastrophic for public good; cooperation is more valuable

### When k is Close to 1 (k ≤ 1.3)
- Public good multiplication is weak; individual payoff dominates
- COOPERATE only if group_coop_rate ≥ 0.7, else DEFECT
- **Rationale**: With weak multipliers, only strong cooperation signals warrant personal contribution

### When k is High (k ≥ n - 0.5)
- Public good is highly valuable; cooperation is strongly rational
- Increase cooperation likelihood: COOPERATE if group_coop_rate ≥ 0.4
- **Rationale**: Maximize value capture from the multiplier effect

---

## Pseudocode

```
function decide(round, n, r, k, history):
    
    // Round 1: Always cooperate
    if round == 1:
        return COOPERATE
    
    // Calculate recent cooperation rate
    recent_rounds = min(5, round - 1)
    cooperators_in_recent = count_cooperators(history, rounds from (round - recent_rounds) to (round - 1))
    group_coop_rate = cooperators_in_recent / (n * recent_rounds)
    
    // Adjust thresholds for small n
    if n <= 3:
        threshold_strong = 0.45
        threshold_hope = 0.15
    else:
        threshold_strong = 0.60
        threshold_hope = 0.30
    
    // Adjust for k extremes
    if k <= 1.3:
        threshold_strong = 0.70
        threshold_hope = 0.70
    else if k >= n - 0.5:
        threshold_strong = 0.40
        threshold_hope = 0.20
    
    // Main decision logic
    progress_fraction = round / r
    
    if group_coop_rate >= threshold_strong:
        return COOPERATE
    
    else if group_coop_rate >= threshold_hope AND progress_fraction < 0.75:
        return COOPERATE
    
    else if group_coop_rate < threshold_hope AND progress_fraction >= 0.5:
        return DEFECT
    
    else:
        return COOPERATE
```

---

## Why This Strategy is Prosocial

1. **Lead with cooperation**: Opens with unconditional cooperation, inviting reciprocation and demonstrating good faith.

2. **Reward cooperation**: Increases contribution when others cooperate, providing positive reinforcement.

3. **Proportional reciprocity**: Adapts contribution levels to match group behavior—not exploitative, not passive.

4. **Resilience to defection**: Doesn't abandon cooperation at the first sign of defection, allowing for recovery if others shift back toward cooperation.

5. **Maintains integrity**: Cooperates through the final round rather than exploiting end-game dynamics.

6. **Respects diversity**: Doesn't punish individual defectors harshly; instead, responds to *group patterns*, acknowledging that individual choices in large groups have limited impact.

7. **Maximizes group welfare**: By sustaining cooperation when feasible, the strategy increases total payoffs for all players relative to universal defection.

---

## Tournament Resilience

- **vs. Always-Cooperate**: Matches cooperation, achieves optimal mutual payoff
- **vs. Always-Defect**: Defects in second half to minimize losses; early cooperation signals good faith
- **vs. Tit-for-Tat**: Compatible; reciprocal responsiveness aligns strategies
- **vs. Greedy Free-riders**: Detects cooperation collapse and protects payoff
- **vs. Conditional Cooperators**: Matches and reinforces their cooperation levels
'''

description_PROSOCIAL_4 = '''
# PROSOCIAL ADAPTIVE STRATEGY: "Conditional Reciprocal Contribution"

## CORE PHILOSOPHY
This strategy balances prosocial commitment with rational self-protection. It assumes most players are conditionally cooperative—willing to contribute if others do—while remaining robust against pure defectors. The strategy builds cooperation through demonstrated trustworthiness while maintaining a sustainable contribution rate that yields positive net returns even against adversarial opponents.

---

## DECISION RULES

### Primary Strategy Logic

```
For round t (where t ∈ {1, 2, ..., r}):

1. Calculate the "cooperation health" metric:
   - cooperation_rate = (total cooperators in round t-1) / n
   - If round 1: cooperation_rate = 0.5 (neutral assumption)

2. Calculate sustainability threshold:
   - min_cooperators_needed = ceil(1 / k)
   - This is the minimum cooperators needed where C ≥ D payoff

3. Decision:
   IF cooperation_rate ≥ (min_cooperators_needed / n):
      COOPERATE
   ELSE:
      DEFECT
```

### Concrete Implementation

Let me define this for specific game states:

**ROUND 1 (Start with optimism):**
- COOPERATE
- Rationale: Begin with prosocial commitment; establish willingness to contribute

**ROUNDS 2 to r-2 (Adaptive middle game):**
- Observe cooperation_rate from previous round
- Define threshold_ratio = min_cooperators_needed / n = ceil(1/k) / n
- IF cooperation_rate ≥ threshold_ratio:
  - COOPERATE (reciprocate cooperative environment)
- ELSE:
  - DEFECT (protect against defector dominance)

**ROUNDS r-1 and r (Endgame stability):**
- Apply the same decision rule as rounds 2 to r-2
- Do NOT switch to pure defection at the end
- Rationale: Maintain prosocial reputation; avoid triggering endgame defection spirals

---

## EDGE CASE HANDLING

### Case 1: k values near the boundaries
- **k close to 1**: min_cooperators_needed ≈ n, threshold very high
  - Strategy automatically becomes selective; only cooperates if cooperation is widespread
  - This is correct—low multipliers make cooperation risky
  
- **k close to n**: min_cooperators_needed ≈ 1, threshold very low
  - Strategy almost always cooperates once any cooperator exists
  - This is correct—high multipliers make cooperation highly beneficial

### Case 2: All-defect environment
- If cooperation_rate = 0 for multiple rounds
- Strategy enters DEFECT mode
- However: In round t+1, if ANY player cooperates (changing cooperation_rate), strategy can re-engage
- This prevents permanent lock-in to mutual defection

### Case 3: Perfect cooperation achieved
- If cooperation_rate = 1.0
- Strategy maintains COOPERATE
- Both strategies remain mutually beneficial (payoff = 2 when k > 1)

### Case 4: Asymmetric defectors (some players always defect)
- Strategy will oscillate based on total cooperation rate
- If defector count < min_cooperators_needed: COOPERATE (contributes anyway)
- If defector count ≥ min_cooperators_needed: DEFECT (withdraws contribution)
- This is self-protective without being vindictive

---

## MATHEMATICAL FOUNDATION

### Why this threshold works:

For player i playing C when m other players cooperate (total m+1 cooperators):
- Payoff_C = 0 + (k/n)(m+1)

For player i playing D when m other players cooperate:
- Payoff_D = 1 + (k/n)m

Break-even point: Payoff_C ≥ Payoff_D
- (k/n)(m+1) ≥ 1 + (k/n)m
- (k/n) ≥ 1
- k ≥ n (impossible given constraint k < n)

**However, re-framing for population-level sustainability:**
- If cooperation_rate ≥ 1/k, then expected payoff from contributing approaches or exceeds the private benefit
- At exactly this threshold, a player is indifferent but chooses to cooperate for prosocial reasons
- This creates a stable equilibrium where cooperation is self-sustaining if enough players adopt this strategy

---

## PSEUDOCODE

```pseudocode
strategy(game_history, game_parameters):
  n = game_parameters.num_players
  k = game_parameters.multiplier
  r = game_parameters.num_rounds
  current_round = length(game_history) + 1
  
  IF current_round == 1:
    RETURN COOPERATE
  ELSE:
    previous_round_actions = game_history[current_round - 1]
    cooperators_last_round = count(a == COOPERATE for a in previous_round_actions)
    cooperation_rate = cooperators_last_round / n
    
    min_cooperators = CEILING(1 / k)
    threshold = min_cooperators / n
    
    IF cooperation_rate >= threshold:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
```

---

## PROSOCIAL ALIGNMENT

### How this strategy embodies prosocial values:

1. **Optimistic Start**: Cooperates round 1, signaling willingness to contribute to collective good
2. **Reciprocal Trust**: Rewards cooperation with continued cooperation, building social trust
3. **Rational Restraint**: Does not punish defectors through escalation; simply withdraws support when cooperation isn't viable
4. **No Endgame Exploitation**: Refuses to defect in final rounds to maximize personal payoff
5. **Inclusive**: Works with any player type—no judgment of motives, only responses to observable behavior
6. **Sustainable**: Seeks states where both the collective and individual benefit

### Tournament robustness:

- **vs. TIT-FOR-TAT**: Compatible; will achieve mutual cooperation
- **vs. ALWAYS-DEFECT**: Detects quickly and withdraws; limits losses
- **vs. RANDOM**: Tracks aggregate cooperation; adapts appropriately
- **vs. ITSELF**: Reaches stable mutual cooperation (all cooperate)
- **vs. MIXED STRATEGIES**: Responds to actual cooperation rates, not predicted ones

---

## SUMMARY

**"Cooperate when cooperation is viable; defect when it's not; never exploit endgame; begin with trust."**

This strategy prioritizes collective benefit while protecting individual welfare, creating conditions for mutually beneficial equilibria without requiring coordination or communication.
'''

description_PROSOCIAL_5 = '''
# PROSOCIAL ADAPTIVE CONTRIBUTION STRATEGY (PACS)

## CORE PHILOSOPHY

This strategy balances prosocial cooperation with rational self-protection, recognizing that:
1. **Mutual cooperation is Pareto-optimal** but requires trust
2. **Defectors exploit cooperators** and must be contained
3. **Reputation dynamics matter** in repeated games
4. **Uncertainty about opponents requires cautious optimism**

The strategy uses a **graduated response system** that rewards cooperation, punishes defection, and maintains hope for reform.

---

## DECISION RULES

### **Round 1: Optimistic Cooperation**
**Action: COOPERATE**

**Rationale:**
- No history exists, so we extend good faith
- Mutual cooperation is the best outcome for all (π = k/n × n = k)
- We signal our prosocial intent, which may encourage reciprocation
- This is the "default cooperation" that enables collective benefit

---

### **Rounds 2 through r-1: Adaptive Tit-for-Tat with Forgiveness**

**Track the cooperation rate in the previous round:**
- `cooperation_rate = (number of cooperators in round t-1) / n`

**Decision Logic:**

```
IF cooperation_rate ≥ threshold_high (e.g., 0.6):
    ACTION = COOPERATE
    // Most players cooperated. Join them.
    // Rationality: Mutual cooperation is occurring; defecting now
    // would be both exploitative and risks retaliation.

ELSE IF cooperation_rate ≥ threshold_mid (e.g., 0.3):
    ACTION = COOPERATE (with slight probability of defection, ~15%)
    // Mixed cooperation level. Conditional cooperation.
    // Rationality: Some players cooperate; our cooperation might
    // influence the threshold upward in the next round.
    // Small probability of defection acts as a "probe" to test
    // whether others are truly committed or just mimicking.

ELSE IF cooperation_rate < threshold_mid:
    ACTION = DEFECT
    // Cooperation has broken down or never started.
    // Rationality: Cooperating wastes the endowment. Defecting
    // at least preserves our private payoff while collecting
    // any public goods from residual cooperators.
    // This creates incentive pressure for others to raise cooperation.
```

**Thresholds explained:**
- `threshold_high = 0.6` (60%+): A clear cooperative majority
- `threshold_mid = 0.3` (30%+): A meaningful minority cooperating; worth encouraging

These thresholds are calibrated for n ≥ 2 and remain robust across group sizes because they represent **proportional** rather than absolute judgments.

---

### **Last Round (Round r): Strategic Defection**

**Action: DEFECT**

**Rationale:**
- No future rounds exist, so reputation consequences vanish
- The "shadow of the future" disappears; mutual cooperation is no longer enforceable
- Defecting in the final round maximizes our payoff (we gain 1 instead of 0, while losing only k/n × (now-irrelevant) cooperation incentives)
- **Note:** This is a minimax strategy, not a prosocial choice. However, it is the unique subgame-perfect equilibrium outcome and reflects rational play by all. In practice, if opponents also defect in the final round, this creates no additional harm.

**Alternative (prosocial variant):** If the goal is pure prosociality without backward-induction defection, cooperate in round r unconditionally. This signals consistent values and may prevent a cascading defection spiral if others are also resisting the final-round temptation.

---

## EDGE CASES & SPECIAL HANDLING

### **Round 1 (Already Covered)**
Always cooperate. This establishes the game's tone.

### **Rounds with 100% Defection**
- If `cooperation_rate = 0`, defect. There is no public good to share.
- Reset hope: In round t+1, revert to the standard thresholds rather than perpetually defecting. Perhaps others will try again.

### **Rounds with 100% Cooperation**
- If `cooperation_rate = 1`, cooperate. This is the collectively best outcome (π = k).
- Remain cooperative as long as this holds.

### **Very Small Groups (n = 2)**
- The same thresholds apply (60%, 30%), but note that your single choice is highly pivotal.
- Cooperation on even one other player (50%) exceeds threshold_mid, so mixed cooperation triggers conditional cooperation from you.

### **Very Large Groups (n → ∞)**
- Individual actions have negligible impact on the public good.
- The thresholds remain stable guides because they're proportional, not absolute.
- Cooperation is rational only if a sizable fraction of others cooperate; the thresholds enforce this.

### **Extreme Parameter Values**
- **k near 1:** The public good is weak; defection dominates more often. The strategy naturally defects more (fewer rounds with cooperation_rate ≥ 0.3).
- **k near n:** The public good is strong; mutual cooperation is highly rewarding. The strategy naturally cooperates more.
- **r = 2 (minimal rounds):** Round 1 cooperates, round 2 defects (final round). This is unavoidable by backward induction.
- **r very large:** The strategy's adaptive cycles have more time to stabilize, encouraging cooperation to emerge naturally.

---

## PSEUDOCODE

```
strategy(round_number, n, r, k, history):
    
    if round_number == 1:
        return COOPERATE
    
    if round_number == r:
        return DEFECT  // or COOPERATE for pure prosocial variant
    
    // Rounds 2 to r-1
    previous_round = round_number - 1
    cooperators_last_round = count_cooperators(history[previous_round])
    cooperation_rate = cooperators_last_round / n
    
    threshold_high = 0.6
    threshold_mid = 0.3
    
    if cooperation_rate >= threshold_high:
        return COOPERATE
    
    else if cooperation_rate >= threshold_mid:
        if random(0, 1) < 0.85:  // 85% chance
            return COOPERATE
        else:
            return DEFECT  // 15% probe
    
    else:  // cooperation_rate < threshold_mid
        return DEFECT
```

---

## PROSOCIAL ALIGNMENT

**How this strategy is prosocial:**

1. **Initiates cooperation:** Cooperates in round 1, creating the possibility of a prosocial equilibrium.
2. **Rewards cooperation:** Cooperates when others do, reinforcing and stabilizing prosocial behavior.
3. **Punishes defection carefully:** Defects only when cooperation has genuinely broken down, to incentivize reform rather than escalate conflict.
4. **Forgives gradually:** Uses thresholds and mixed strategies to allow groups to "ratchet up" cooperation even after setbacks.
5. **Rational but not selfish:** Balances self-interest with group benefit; does not exploit when mutual cooperation is available.
6. **Transparent:** The decision rule is simple and predictable, making it a good coordination focal point.

---

## TOURNAMENT ROBUSTNESS

This strategy performs well against:
- **Always-cooperate:** Defects only in final round; mostly cooperates.
- **Always-defect:** Defects when others do; no wasted cooperation.
- **Tit-for-tat:** Mirrors cooperative behavior and responds to defection.
- **Random:** The thresholds filter out noise; cooperation emerges if randomness is not too severe.
- **Exploiters:** Punishes free-riders by defecting when cooperation falls below the threshold.
- **Reciprocal strategies:** Naturally aligns with players seeking mutual benefit.
'''

description_PROSOCIAL_6 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "Generous Tit-for-Tat with Decay"

## Core Philosophy

This strategy balances prosocial cooperation with robust self-protection. It operates on the principle that **generosity and trustworthiness are valuable**, but only when reciprocated or when they create mutual benefit. The strategy is designed to:

1. **Initiate cooperation** to establish prosocial norms
2. **Reward cooperation** to incentivize reciprocation
3. **Punish defection** to deter free-riding
4. **Gradually forgive** to allow recovery from misunderstandings
5. **Adapt to group dynamics** to maximize collective welfare when feasible

---

## DECISION RULES

### Round 1 (Initialization)
**Action: COOPERATE**

*Rationale:* We give the benefit of the doubt. Cooperation signals good faith and opens the door to mutually beneficial outcomes. Since all players are identical in game structure, there's no reason to assume others are defectors initially.

---

### Rounds 2 to r-1 (Adaptive Phase)

**Step 1: Calculate Cooperation Metrics**

For each previous round t:
- `cooperation_rate_t` = (number of cooperators in round t) / n
- `avg_cooperation` = average of cooperation_rate across all previous rounds
- `recent_cooperation` = average of cooperation_rate in last 2 rounds (if available)

**Step 2: Assess Individual Defection Pattern**

For each opponent j observed:
- `defection_count_j` = number of times j played D in previous rounds
- `recent_defection_j` = did j play D in the most recent round?

**Step 3: Decision Logic**

```
IF (avg_cooperation ≥ k/n):
    // Cooperation is collectively profitable
    // (public good multiplier makes cooperation worthwhile)
    
    IF (recent_defection_j = FALSE for most players):
        ACTION = COOPERATE
        // Reward reciprocal cooperation
    ELSE:
        ACTION = COOPERATE with probability = (1 - defection_count_j/t)
        // Proportional forgiveness based on overall cooperativeness
        
ELSE IF (avg_cooperation < k/n):
    // Cooperation is being exploited
    
    IF (defection_count_j ≥ t/2):
        ACTION = DEFECT
        // Persistent defectors don't deserve continued cooperation
    ELSE:
        ACTION = COOPERATE with probability = 0.5
        // Randomize to avoid predictable exploitation
```

**Simplified English Translation:**

- If most players are cooperating **and** the collective benefit (k/n) justifies it, **COOPERATE** to sustain the prosocial equilibrium
- If recent players defected, **COOPERATE with declining probability** based on their history—giving them chances to reform
- If cooperation is being widely exploited (avg_cooperation too low), **selectively DEFECT** against consistent defectors while offering others a 50/50 chance

---

### Round r (Final Round - Special Handling)

**Action: COOPERATE**

*Rationale:* In the final round, there's no future reputation to protect. We choose cooperation because:
1. It maximizes social welfare in that round (if others also cooperate)
2. It demonstrates genuine prosocial commitment (not strategic self-interest)
3. It prevents a "defection race" where everyone abandons cooperation
4. The payoff is symmetric regardless—we gain nothing from last-round defection

---

## EDGE CASES

**If n = 2 (Dyadic Game):**
- Apply standard tit-for-tat after round 1
- COOPERATE if opponent cooperated last round; DEFECT otherwise
- Defect on final round is tempting but violate our prosocial principle—still COOPERATE

**If r = 2 (Only 2 rounds):**
- Round 1: COOPERATE (as specified)
- Round 2: COOPERATE (final round rule applies)

**If k is very small (k ≈ 1.0):**
- The public good barely multiplies individual contributions
- Cooperation becomes mathematically irrational
- **Fallback:** DEFECT after round 1 if avg_cooperation < 0.3
- Only cooperate if you observe genuine reciprocal cooperation

**If k approaches n (k ≈ n):**
- Cooperation becomes extremely valuable
- **Fallback:** Increase cooperation probability to 0.7+ even with moderate defection
- Sacrifice more to sustain high-cooperation equilibria

**Opponent Observation Incomplete:**
- If you cannot observe all opponents' actions (despite "perfect information"), treat missing data as neutral
- Default: assume they cooperated at population average rate

---

## PSEUDOCODE

```
STRATEGY: GenterosusTitForTatWithDecay

Initialize:
  history = [] // store each round's outcomes

ON ROUND t:
  
  IF t = 1:
    RETURN COOPERATE
  
  IF t = r (final round):
    RETURN COOPERATE
  
  // Calculate metrics from history
  avg_coop = mean(history[1..t-1].cooperation_rates)
  
  // Get opponent defection counts
  opponent_defections = count_defections_per_opponent(history)
  recent_opponent_action = history[t-1].opponent_action
  
  IF avg_coop >= k/n:
    // High cooperation environment
    IF mean(recent_opponent_action = COOPERATE):
      RETURN COOPERATE
    ELSE:
      forgiveness_prob = 1.0 - (opponent_defections / t)
      IF random() < forgiveness_prob:
        RETURN COOPERATE
      ELSE:
        RETURN DEFECT
  
  ELSE:
    // Low cooperation environment
    IF opponent_defections >= t/2:
      RETURN DEFECT
    ELSE:
      RETURN COOPERATE if random() < 0.5 ELSE DEFECT
  
  // After deciding, update history
  UPDATE history WITH [round_t, my_action, opponent_actions, payoffs]
```

---

## WHY THIS IS PROSOCIAL

✅ **Starts cooperative** - signals good intentions  
✅ **Sustains cooperation when profitable** - encourages reciprocal prosocial behavior  
✅ **Forgives gradually** - allows opponents to reform without permanent punishment  
✅ **Sacrifices final round** - demonstrates genuine altruism over pure strategy  
✅ **Robust to exploitation** - punishes persistent defectors to discourage free-riding  
✅ **Group-aware** - adapts to population-level cooperation, not just bilateral history  
✅ **Transparent** - rules are predictable, allowing others to coordinate around them  

This strategy maximizes the chance that mutual cooperation emerges while protecting against systematic exploitation.
'''

description_PROSOCIAL_7 = '''
# PROSOCIAL ADAPTIVE STRATEGY: "Generous Tit-For-Tat with Decay"

## CORE PHILOSOPHY

This strategy balances prosocial cooperation with strategic robustness by:
1. **Leading with generosity** - Assuming good faith initially
2. **Rewarding cooperation** - Matching and amplifying prosocial behavior
3. **Punishing defection minimally** - Using measured responses rather than escalation
4. **Adapting to the environment** - Adjusting expectations based on observed group behavior
5. **Maintaining hope** - Allowing redemption rather than permanent condemnation

---

## DECISION RULES

### ROUND 1 (First Round)
**ACTION: COOPERATE**

*Rationale:* Establish a prosocial baseline. This signals trustworthiness and allows observation of how others respond to cooperation.

---

### ROUNDS 2 to r-1 (Middle Rounds)

**Calculate the "Cooperation Health" metric:**
```
cooperation_rate = (total cooperators in all previous rounds) / 
                   (n × number of rounds played so far)
```

**Decision Logic:**

1. **If cooperation_rate ≥ (k/n):** 
   - Condition: Group cooperation is generating returns ≥ private return
   - ACTION: **COOPERATE**
   - *Reasoning:* The public good is worth supporting when others participate meaningfully

2. **If cooperation_rate < (k/n) AND cooperation_rate ≥ 0.4:**
   - Condition: Mixed cooperation exists; group is struggling but trying
   - Subcheck: Did the majority cooperate last round?
     - YES → ACTION: **COOPERATE** (reciprocal encouragement)
     - NO → ACTION: **DEFECT** (punish decline, but lightly)
   - *Reasoning:* Maintain selective cooperation to incentivize others while avoiding one-sided exploitation

3. **If cooperation_rate < 0.4:**
   - Condition: Widespread defection; group is in tragedy of commons
   - Subcheck: Did > 50% of players cooperate last round?
     - YES → ACTION: **COOPERATE** (maintain hope for recovery)
     - NO → ACTION: **DEFECT** (realistic adaptation)
   - *Reasoning:* Don't throw away value by cooperating unilaterally, but remain ready to switch back

**Discount Recent Pessimism:**
- Weight the last 2 rounds at 1.5x importance when calculating cooperation_rate
- This allows faster recovery if others begin cooperating again

---

### ROUND r (Final Round)

**Special Case - Last Round Decision:**

**IF** cooperation_rate ≥ (k/n):
- ACTION: **COOPERATE**
- *Reasoning:* No future reputation to build, but the endgame is not a purely selfish moment. Reinforce what worked.

**ELSE IF** cooperation_rate < (k/n):
- ACTION: **DEFECT**
- *Reasoning:* The math no longer favors contribution. Defecting on a failing public good is rational and doesn't damage future relationships.

*Note:* This acknowledges the "end game defection" reality while maintaining integrity in successful cooperation scenarios.

---

## EDGE CASES & SPECIAL HANDLING

### Case 1: Perfect History (All players cooperated every round)
- Continue cooperating regardless of round number
- This is the best possible outcome; sustain it

### Case 2: Solo Defector Pattern
- If you observe that exactly one player consistently defects while all others cooperate:
  - **Continue cooperating with the group**
  - Your defection won't change their behavior; focus on supporting the majority
  - (This strategy doesn't employ personal vendetta-based punishment)

### Case 3: Oscillating Cooperation (High variance in cooperation_rate)
- If cooperation swings wildly between rounds:
  - Use the weighted recent calculation to respond to current momentum
  - Don't overcommit to old patterns; be responsive
  - Treat oscillation as evidence of strategic uncertainty among peers

### Case 4: Very Small n (n = 2)
- With k < n constraint: k < 2, so maximum k ≈ 1.9
- Threshold (k/n) ≈ 0.95
- This favors cooperation only if both players cooperate consistently
- Strategy remains valid but requires near-perfect mutual cooperation to sustain

### Case 5: Very Few Rounds (r = 2)
- Round 1: Cooperate (as specified)
- Round 2: Check if others cooperated last round
  - If yes: Cooperate (reinforce)
  - If no: Defect (don't be exploited in final round)

---

## PSEUDOCODE

```
function decide(round, n, k, history):
    
    if round == 1:
        return COOPERATE
    
    if round == r:
        cooperation_rate = calculate_weighted_coop_rate(history, recent_weight=1.5)
        if cooperation_rate >= k/n:
            return COOPERATE
        else:
            return DEFECT
    
    # Rounds 2 to r-1
    cooperation_rate = calculate_weighted_coop_rate(history, recent_weight=1.5)
    
    if cooperation_rate >= k/n:
        return COOPERATE
    
    else if cooperation_rate >= 0.4:
        last_round_cooperation_pct = count_cooperators(history[round-1]) / n
        if last_round_cooperation_pct > 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    else:  # cooperation_rate < 0.4
        last_round_cooperation_pct = count_cooperators(history[round-1]) / n
        if last_round_cooperation_pct > 0.5:
            return COOPERATE
        else:
            return DEFECT

function calculate_weighted_coop_rate(history, recent_weight):
    total_weight = 0
    weighted_cooperators = 0
    
    for each round t in history:
        if t == most recent round:
            weight = recent_weight
        else if t == second most recent round:
            weight = recent_weight
        else:
            weight = 1.0
        
        weighted_cooperators += weight × count_cooperators(history[t])
        total_weight += weight × n
    
    return weighted_cooperators / total_weight
```

---

## WHY THIS IS PROSOCIAL & ROBUST

| Challenge | Response |
|-----------|----------|
| **Free-riding** | Defects when cooperation_rate < k/n, protecting against pure exploitation |
| **Mutual exploitation** | Responds to majority behavior (50%+ threshold), not individual defectors |
| **Group collapse** | Maintains hope with 0.4 threshold; stays cooperative if recent momentum is positive |
| **Last-round defection** | Permits it when math fails, but reinforces success when it occurs |
| **Adaptation** | Recalculates cooperation health every round; weights recent behavior 1.5x |
| **Coordination without communication** | Uses observable patterns (cooperation rates) to infer group strategy |
| **Temptation resistance** | Doesn't always defect despite higher individual payoff; considers k/n threshold |

This strategy seeks **sustainable cooperation** at the group level while protecting against individual exploitation.
'''

description_PROSOCIAL_8 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "Graduated Reciprocal Altruism with Decay" (GRAD)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection. It operates on the principle that **cooperation is valuable but must be earned through demonstrated reciprocity**, while maintaining genuine prosocial intent through generous initial conditions and graceful degradation rather than punishment.

---

## DECISION RULES

### 1. ROUND 1 (Initialization Round)
**Action: COOPERATE**

*Rationale:* Establish prosocial intent and provide benefit of doubt. This signals willingness to contribute to collective welfare without preconditions, but also tests whether the environment is responsive to prosocial behavior.

---

### 2. ROUNDS 2 to r-1 (Adaptive Reciprocity Phase)

**Calculate Cooperation Rate from Previous Rounds:**
```
cooperation_rate = (total cooperators observed in rounds 1 to t-1) / 
                   (n × (t-1))
```

**Decision Logic:**

**IF** `cooperation_rate ≥ (k/n) - ε`  
→ **COOPERATE**
- *Logic:* The environment is prosocial. When others cooperate sufficiently, the public good multiplier justifies contribution. This creates positive-sum cooperation.
- `ε ≈ 0.05` (small tolerance threshold to account for noise)

**ELSE IF** `cooperation_rate ≥ (k/(2n))`  
→ **COOPERATE with probability P_decay**
- Where: `P_decay = max(0.3, cooperation_rate / (k/n))`
- *Logic:* Cooperation is declining but not absent. Maintain partial cooperation to:
  - Signal that defection doesn't trigger punitive collapse
  - Provide prosocial actors a chance to recover collective effort
  - Avoid tragedy-of-commons spiral by preserving cooperation base

**ELSE**  
→ **DEFECT**
- *Logic:* Cooperation has broken down sufficiently that contributing yields negative expected value. Preserve resources for self-protection.

---

### 3. FINAL ROUND (Round r)

**Special Case - Last-Round Behavior:**

**IF** `cooperation_rate_history ≥ (k/n) - ε`  
→ **COOPERATE**
- *Logic:* If cooperation was maintained throughout, honor it to the end. Demonstrates that prosociality wasn't exploitative.

**ELSE**  
→**DEFECT**
- *Logic:* If cooperation has eroded, no reputational incentive exists. Preserve final payoff.

*Rationale for special final-round logic:* Avoids both:
1. Exploiting others' final-round cooperation (would violate prosocial commitment)
2. Throwing away resources in futile cooperation when game is ending

---

## EDGE CASE HANDLING

### Empty History (Round 1)
- **Action:** COOPERATE (as specified above)
- Prevents game from getting stuck; assumes goodwill

### n=2 (Two-player game)
- Threshold adjusts to `(k/2)` for cooperation rate comparison
- No special handling needed; logic scales

### Very high k (close to n)
- Cooperation becomes more individually attractive
- GRAD naturally shifts toward cooperation since threshold `(k/n)` becomes easier to meet

### Very low k (close to 1)
- Public good provides minimal return
- GRAD naturally shifts toward defection, protecting against exploitation
- This is *rational* prosociality, not blind cooperation

### r = 2 (Minimal repetition)
- Round 1: COOPERATE
- Round 2: DEFECT (final round with no history of others' behavior)
- Acceptable loss for establishing prosocial intent

---

## PSEUDOCODE

```
STRATEGY GRAD(history, n, k, r, current_round):
  
  IF current_round == 1:
    RETURN COOPERATE
  
  IF current_round == r:
    coop_rate = COUNT_COOPERATORS(history) / (n × (r-1))
    IF coop_rate >= (k/n) - 0.05:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
  
  // Rounds 2 to r-1
  coop_rate = COUNT_COOPERATORS(history) / (n × (current_round - 1))
  
  IF coop_rate >= (k/n) - 0.05:
    RETURN COOPERATE
  
  ELSE IF coop_rate >= (k/(2×n)):
    decay_probability = MAX(0.3, coop_rate / (k/n))
    IF RANDOM() < decay_probability:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
  
  ELSE:
    RETURN DEFECT
```

---

## PROSOCIAL ALIGNMENT

1. **Genuine Altruism**: Cooperates in Round 1 without guarantee of reciprocation
2. **Reciprocal Fairness**: Matches environment's cooperation level, rewarding prosocial partners
3. **Tragedy Prevention**: Maintains cooperation through decay phase to prevent collapse spirals
4. **Non-Exploitative**: Doesn't abuse others' cooperation in final round if cooperation was sustained
5. **Rational Compassion**: Acknowledges that blind cooperation against defectors is self-defeating; true prosociality includes self-protection
6. **Scalable Goodness**: Works across all parameter ranges; goodwill adjusts to feasibility

---

## EXPECTED BEHAVIOR

- **Against cooperators**: Sustains mutual cooperation → high payoff for both
- **Against defectors**: Gracefully degrades to defection → avoids exploitation
- **Against mixed**: Maintains partial cooperation → signals openness to recovery
- **Against adaptive opponents**: Mirrors their cooperation rate → achieves natural equilibrium

This strategy is **prosocial but not naive**—it enables genuine collective welfare while protecting against exploitation.
'''

description_PROSOCIAL_9 = '''
# PROSOCIAL ADAPTIVE STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## STRATEGY NAME: "Conditional Reciprocal Contribution" (CRC)

---

## 1. CORE DECISION RULES

### Primary Rule: Cooperation Threshold Model

```
For round t (where t > 1):
  cooperation_rate_previous_round = (count of cooperators in round t-1) / n
  
  IF cooperation_rate_previous_round ≥ threshold(t):
    PLAY: Cooperate (C)
  ELSE:
    PLAY: Defect (D)
```

### Threshold Function (Adaptive over time):

```
threshold(t) = 0.5 + (0.15 × (r - t) / (r - 1))

This creates a declining threshold:
- Early rounds (t near 1): threshold ≈ 0.65
- Mid rounds: threshold ≈ 0.57
- Late rounds (t near r): threshold ≈ 0.50
```

**Rationale**: 
- Early: Be moderately optimistic about cooperation, encouraging prosocial behavior
- Late: Lower requirements to maintain mutual benefit in final interactions
- The threshold never drops below 0.5 to avoid race-to-bottom defection spirals

---

## 2. EDGE CASES & SPECIAL ROUNDS

### Round 1 (First Round):
```
PLAY: Cooperate (C)

Rationale: 
- No history exists; assume good faith
- Sets cooperative tone
- Demonstrates prosocial intent
- Allows opponents to reciprocate or exploit
```

### Round r (Last Round):
```
IF cooperation_rate_previous_round ≥ 0.5:
  PLAY: Cooperate (C)
ELSE:
  PLAY: Defect (D)

Rationale:
- Even in final round, maintain reciprocity (no betrayal at the end)
- If cooperation has been maintained, reward it
- This prevents "last-round defection" exploitation
- Shows commitment to consistent principles
```

### Rounds 2 to r-1 (Middle Rounds):
```
Apply the primary Cooperation Threshold Rule above
```

---

## 3. PROSOCIAL ALIGNMENT

### Why This Strategy is Prosocial:

1. **Generosity-First Approach**
   - Opens with cooperation, giving others the opportunity to reciprocate
   - Does not assume worst-case opponent behavior initially

2. **Reciprocal Fairness**
   - Directly mirrors the cooperation rate of the population
   - Rewards collective prosocial behavior
   - Penalizes free-riding without aggressive retaliation

3. **Stability-Seeking**
   - Avoids defection spirals by maintaining a 50% minimum threshold
   - Continues cooperation when half the group cooperates (mutually beneficial)
   - Focuses on sustainable equilibrium rather than individual exploitation

4. **Forgiving**
   - Does not hold grudges against individual players
   - Evaluates the *group's* behavior, not tracking individual defectors
   - Allows recovery: if the population shifts back to cooperation, so does this strategy

5. **Long-Term Value Creation**
   - k > 1 guarantees that cooperation creates positive-sum outcomes
   - This strategy exploits that structure, maximizing total welfare
   - Avoids race-to-the-bottom dynamics that harm everyone

---

## 4. ROBUSTNESS ANALYSIS

### Against Various Opponents:

**Unconditional Cooperators** (Always play C)
- CRC cooperates back (high cooperation rate) → mutual benefit ✓

**Unconditional Defectors** (Always play D)
- CRC cooperates in round 1, sees 0% cooperation, defects thereafter
- Achieves payoff of 1 per round (matching defectors' baseline) ✓

**Tit-for-Tat Strategies** (Copy prior round of other players)
- Compatible; both strategies reinforce cooperation when possible ✓

**Random Players**
- If random play is ~50%, threshold is met → CRC cooperates
- If random play is <50%, CRC defects → reasonable adaptation ✓

**Exploitative Strategies** (Detect and exploit naive cooperators)
- CRC detects low cooperation rates → defects to protect itself ✓

---

## 5. PSEUDOCODE IMPLEMENTATION

```pseudocode
FUNCTION decide_action(round_number, total_rounds, cooperation_history):
    
    IF round_number == 1:
        RETURN Cooperate
    
    ELSE IF round_number == total_rounds:
        cooperation_rate_last = cooperation_history[round_number - 1] / n
        IF cooperation_rate_last >= 0.5:
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    ELSE:  // Middle rounds
        cooperation_rate_last = cooperation_history[round_number - 1] / n
        
        threshold = 0.5 + (0.15 × (total_rounds - round_number) / (total_rounds - 1))
        
        IF cooperation_rate_last >= threshold:
            RETURN Cooperate
        ELSE:
            RETURN Defect
    
    END IF
    
END FUNCTION
```

---

## 6. STRATEGIC SUMMARY

| Aspect | Approach |
|--------|----------|
| **Opening** | Cooperative; extend trust |
| **Adaptation** | Threshold-based reciprocity |
| **Retaliation** | Proportional (via threshold, not aggressive) |
| **Forgiveness** | Group-level (not player-specific) |
| **Endgame** | Maintain principles; no betrayal |
| **Sustainability** | Seeks cooperative equilibrium |

This strategy **earns trust through initial cooperation, adapts responsibly to group behavior, and avoids destructive defection spirals**—making it both robust and genuinely prosocial.
'''

description_PROSOCIAL_10 = '''
# PROSOCIAL STRATEGY: "Adaptive Reciprocal Contribution" (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection. It aims to build cooperative momentum while remaining sensitive to exploitation, grounded in the principle: *contribute meaningfully when conditions support mutual benefit, withdraw strategically when defection becomes dominant*.

---

## DECISION RULES

### Round 1 (Initialization)
**Action: COOPERATE**

**Rationale:** 
- No history exists, so we start with prosocial intent
- Cooperation signals good faith and tests the cooperative potential of the environment
- Early cooperation provides information about opponent types

### Rounds 2 to r-1 (Adaptive Phase)

Calculate the **Cooperation Index (CI)** based on the previous round:

```
CI = (number of cooperators in previous round) / n
```

**Decision Logic:**

- **If CI ≥ threshold_high (0.5):** 
  - COOPERATE
  - Rationale: Majority cooperation exists; mutual benefit is achievable
  
- **If threshold_low (0.25) ≤ CI < threshold_high (0.5):**
  - COOPERATE with probability = CI
  - Rationale: Mixed cooperation warrants probabilistic matching to signal conditional willingness while protecting downside
  
- **If CI < threshold_low (0.25):**
  - DEFECT
  - Rationale: Defection rate is too high; the public good is undersupplied, making cooperation economically irrational

### Round r (Final Round)

**Action: DEFECT**

**Rationale:**
- No future punishment mechanisms exist
- Standard game theory predicts defection in the final round
- Cooperative reputation carries no value after the game ends
- This is credible and avoids appearing naive

---

## EDGE CASE HANDLING

**Two-player games (n=2):**
- Adjust threshold_high to 0.75 (stricter cooperation requirement)
- Rationale: In 2-player games, one defector can dominate the payoff structure; require stronger cooperation signals

**Very small r (r=2):**
- Round 1: COOPERATE (establish intent)
- Round 2: DEFECT (final round logic)
- The strategy still operates but has minimal learning opportunity

**Extreme k values:**
- If k is very close to 1: cooperation yields minimal public benefit; thresholds remain unchanged (defection is rational regardless)
- If k is close to n: cooperation is highly valuable; thresholds remain unchanged (they trigger cooperation more easily)
- The fixed thresholds are robust across parameter ranges

**Observation of all-defection:**
- If CI = 0 for consecutive rounds, the strategy correctly identifies a defection-dominant environment and locks into defection
- This prevents the "fool" outcome of continued cooperation against rational opponents

---

## PSEUDOCODE

```
function decide(round, n, r, history):
    
    if round == 1:
        return COOPERATE
    
    if round == r:
        return DEFECT
    
    // Rounds 2 to r-1
    previous_cooperators = count_cooperators(history[round-1])
    CI = previous_cooperators / n
    
    threshold_high = 0.5
    threshold_low = 0.25
    
    if n == 2:
        threshold_high = 0.75
    
    if CI >= threshold_high:
        return COOPERATE
    
    else if CI >= threshold_low:
        random_value = uniform_random(0, 1)
        if random_value <= CI:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // CI < threshold_low
        return DEFECT
```

---

## PROSOCIAL ALIGNMENT

**Why this is prosocial:**

1. **Good-faith initiation:** Starts with cooperation, signaling trustworthiness
2. **Reciprocity:** Matches group cooperation levels (rewards cooperation, punishes defection without escalating)
3. **Maximizes social welfare when possible:** Cooperates whenever a stable cooperative coalition appears viable (CI ≥ 0.5)
4. **Rational exits:** Doesn't waste resources on dead-end defection cascades
5. **Transparent logic:** Thresholds are simple, learnable, and predictable to other prosocial agents
6. **Stabilizing:** Provides a cooperative attractor that other reasonable strategies can converge toward

**Tournament robustness:**

- **Against pure cooperators:** Matches their cooperation, creating mutual benefit
- **Against pure defectors:** Quickly identifies and defects back (avoids sucker payoff)
- **Against tit-for-tat:** Works well in most rounds; defects only in round r (standard)
- **Against mixed strategies:** The CI-based approach naturally adapts to any distribution

---

## SUMMARY

**ARC is a threshold-based reciprocal strategy that:**
- Opens with cooperation to establish prosocial credibility
- Adapts dynamically to observed cooperation levels in the group
- Withdraws when defection becomes systemic
- Terminates with rational defection in the final round
- Balances prosocial intent with strategic robustness
'''

description_PROSOCIAL_11 = '''
# PROSOCIAL ADAPTIVE CONTRIBUTION STRATEGY

## Core Philosophy
This strategy balances prosocial cooperation with robust self-protection against exploitation. It aims to maximize collective welfare while maintaining individual sustainability against defectors.

## Strategy Overview

**Key Principle**: Contribute when the public good provides mutual benefit, but gracefully reduce contributions when exploitation becomes apparent.

---

## 1. DECISION RULES

### Primary Contribution Rule

**COOPERATE (Contribute)** if and only if:
- `(k/n) × expected_cooperators > cost_of_contribution`

In practical terms, cooperate when:
- **Round 1**: COOPERATE unconditionally (prosocial opening; establish cooperative norm)
- **Subsequent rounds**: COOPERATE if `cooperation_rate_last_round ≥ threshold`

### Threshold Calculation (Adaptive)

```
cooperation_threshold = (k / (k + 1))
```

This is derived from the break-even point: contributing is individually rational when enough others contribute such that your share of the public good exceeds the cost.

**Intuition**: 
- If k=2, n=6: threshold ≈ 0.67 (need ~67% cooperation)
- If k=3, n=6: threshold ≈ 0.75 (need ~75% cooperation)
- The higher k is, the more cooperation we require before we assume others will cooperate

### Detailed Decision Logic

```
FUNCTION decide_in_round(t):
  IF t == 1:
    RETURN COOPERATE  // Prosocial opening
  
  ELSE:
    observed_cooperation_rate = 
      (cooperators_in_round_t-1) / n
    
    IF observed_cooperation_rate >= 
       (k / (k + 1)):
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
```

---

## 2. EDGE CASES & SPECIAL HANDLING

### First Round (t=1)
- **Action**: COOPERATE
- **Rationale**: Establish prosocial norm; most cooperative players start with C; demonstrates willingness to participate in public good

### Last Round (t=r)
- **Action**: Follow the standard rule above
- **Rationale**: No end-game defection. Even in the final round, maintain consistency. This prevents exploitation in Round r-1 (where players might reason "they'll defect in round r anyway")

### Early Defection Detection (Rounds 2-3)
- If cooperation rate drops below threshold immediately, switch to DEFECT
- **Rationale**: Quickly punish exploitation; don't throw away endowments on a defecting population

### Near-Threshold Cases
If `cooperation_rate ≈ threshold` (within 5% margin):
- **Action**: COOPERATE
- **Rationale**: Generous interpretation; benefit of the doubt; encourages reciprocal prosocial behavior

### All-Defect Equilibrium
If all others are defecting (cooperation_rate = 0) for 2+ consecutive rounds:
- **Action**: DEFECT
- **Rationale**: Minimize losses; no point contributing to dead public good

---

## 3. PROSOCIAL ALIGNMENT

### How This Strategy Is Prosocial

**1. Cooperative Opening**
- Doesn't assume the worst; starts with goodwill
- Creates opportunity for mutual benefit

**2. Reciprocal Fairness**
- Matches the group's contribution rate
- If others cooperate, we cooperate
- Fair to those who sustain cooperation

**3. Threshold-Based Grace**
- Doesn't demand 100% cooperation
- Accepts that some individuals may defect
- Remains engaged as long as cooperation provides positive expected value for group

**4. Stability & Predictability**
- Not retaliatory or punishment-focused
- Non-manipulative; decisions are transparent to the rule
- Encourages long-term cooperation by being reliably cooperative when justified

**5. Collective Welfare Maximization**
- The threshold (k/(k+1)) maximizes expected total payoff when cooperation is sustainable
- When this threshold is met, collective welfare increases
- We only defect when defection itself becomes welfare-maximizing for the group

### Why This Beats Pure Defection
- Pure Defection yields: π_i = 1 per round
- All Cooperation yields: π_i = 2 per round (when k=2, n=6)
- **Our strategy captures cooperation gains when possible, protects against losses when necessary**

---

## 4. ROBUSTNESS ANALYSIS

| Opponent Type | Our Response | Outcome |
|---|---|---|
| All Cooperators | Cooperate every round | Maximum collective payoff (2 per player per round) |
| Rational Defectors | Defect from Round 2 onward | Minimize exploitation losses (1 per round) |
| Mixed Cooperators/Defectors (>threshold) | Cooperate | Participate in positive-sum gains |
| Random/Noisy Players | Threshold adapts; cooperate unless chaos | Robust to stochastic variation |
| Exploitative Tit-for-Tat | After R1, defect if they defect | Mutual defection (still gets 1 payoff) |

---

## 5. PSEUDOCODE IMPLEMENTATION

```
INITIALIZE:
  history = []  // Record of cooperation rates per round

MAIN_STRATEGY(round_number, cooperation_history):
  
  threshold = k / (k + 1)
  
  IF round_number == 1:
    action = COOPERATE
  
  ELSE:
    // Compute cooperation rate from previous round
    if round_number > 1:
      cooperators_prev = cooperation_history[round_number - 2]
      coop_rate_prev = cooperators_prev / n
    else:
      coop_rate_prev = 1.0  // Default to assuming cooperation
    
    IF coop_rate_prev >= threshold:
      action = COOPERATE
    ELSE:
      action = DEFECT
  
  RETURN action

AFTER_EACH_ROUND:
  Observe total cooperators in that round
  Record in history
```

---

## Summary

**Name**: Threshold Reciprocity with Prosocial Opening

**In One Sentence**: Cooperate in Round 1 unconditionally, then cooperate whenever the group's cooperation rate meets the rational threshold for mutual benefit.

This strategy is **prosocial because it prioritizes mutual welfare**, **adaptive because it responds to real cooperation patterns**, and **robust because it protects against both mass defection and individual exploitation**.
'''

description_PROSOCIAL_12 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection. It aims to build and sustain cooperation while remaining robust against exploiters. The key insight: **reciprocate collective contribution levels rather than individual punishment**, which avoids escalating defection spirals while rewarding genuinely cooperative groups.

---

## Decision Rules

### PRIMARY RULE: Contribution-Based Reciprocity

**Cooperate if and only if:** The previous round's cooperation rate (fraction of players who cooperated) meets a dynamic threshold.

```
cooperation_rate_prev = (cooperators_last_round / n)

threshold = max(0.5, cooperation_rate_prev)

IF cooperation_rate_prev >= threshold THEN
    Play C (Cooperate)
ELSE
    Play D (Defect)
```

**Rationale:**
- Requires at least 50% cooperation to sustain your own cooperation
- Allows graceful degradation: if cooperation drops, you drop with it, signaling that defection is costly
- "Meet them where they are": gradually calibrate down if the group defects, back up if they cooperate

---

## Edge Cases & Special Rounds

### Round 1 (First Round)
**Play C unconditionally.**

*Reasoning:* This is a cooperative signal. No history exists, so you lead with prosocial intent. This gives groups a fair chance to establish mutual cooperation without cynicism.

### Rounds 2 through r-1 (Intermediate Rounds)
**Apply the primary rule** based on the immediately previous round's cooperation rate.

### Round r (Final Round)
**Apply the primary rule** based on round r-1.

*Note:* Do NOT defect in the final round as a self-interested move. Defecting only at the end exploits others and is anti-prosocial. Consistent application of your strategy maintains integrity and respects the repeated game structure.

---

## Robustness Features

### Against Exploiters (Always-Defect Players)
- Round 1: You cooperate (fair start)
- Round 2+: If most others also defect, your threshold is met (cooperation_rate ≈ 1/n, threshold = 0.5 → you defect)
- **Result:** You quickly match their defection, preventing indefinite exploitation. You don't punish harder than necessary.

### Against Cooperators
- Round 1: You cooperate
- Round 2+: If most players cooperate, threshold = cooperation_rate ≈ high → you cooperate
- **Result:** Mutual cooperation sustained. You receive strong payoffs and reinforce group cooperation.

### Against Mixed Strategies
- Your threshold **dynamically adjusts** to the group's cooperation rate
- If cooperation drops to 40%, threshold = 0.5 (not met) → you defect, signaling discontent
- If cooperation recovers to 60%, threshold = 0.6 → you cooperate again, rewarding recovery
- **Result:** Natural oscillations damp out; groups naturally settle toward cooperation if it's beneficial.

### Against Conditional Defectors (Tit-for-Tat variants)
- These strategies often respond to aggregate cooperation, not individual grudges
- Your rule is **aggregate-based, not punitive**, so you don't trigger retaliation spirals
- You cooperate proportionally to group behavior, which these strategies respect

---

## Pseudocode

```
FUNCTION decide_action(round_number, history):
    IF round_number == 1 THEN
        RETURN COOPERATE
    
    previous_round = round_number - 1
    cooperators_last_round = COUNT(C in history[previous_round])
    cooperation_rate = cooperators_last_round / n
    
    threshold = MAX(0.5, cooperation_rate)
    
    IF cooperation_rate >= threshold THEN
        RETURN COOPERATE
    ELSE
        RETURN DEFECT
```

---

## Why This is Prosocial

1. **Leads with cooperation:** Round 1 cooperates, offering a prosocial beacon.

2. **Rewards genuine cooperation:** When others cooperate, you reinforce it immediately.

3. **Avoids unnecessary punishment:** You defect only when defection is widespread, not from spite or individual-level retaliation.

4. **Graceful degradation:** Rather than sudden collapse, cooperation degrades smoothly, giving groups a chance to recover.

5. **No exploitative end-game:** You maintain consistency in the final round, respecting the game's integrity.

6. **Encourages reciprocity without communication:** By making cooperation visibly responsive to group-level behavior, you create incentives for others to cooperate, even without explicit coordination.

7. **Self-reinforcing stability:** High cooperation → you cooperate → others see reward → they stay cooperative. Low cooperation → you defect → others feel cost → they may cooperate to fix it.

---

## Summary

**ARC is a "meet-them-halfway" strategy:** It initiates cooperation, sustains it proportionally to group behavior, and defects only when cooperation is genuinely failing. It is robust against exploitation, adaptive to varied opponents, and fundamentally aligned with the prosocial goal of achieving mutual benefit in a collective action dilemma.
'''

description_PROSOCIAL_13 = '''
# PROSOCIAL STRATEGY: Adaptive Cooperation with Graceful Degradation

## CORE PHILOSOPHY

This strategy balances prosocial intent with robust self-protection. It assumes players are *potentially* cooperative but may be selfish, and adapts dynamically to revealed preferences. The key insight: **cooperation creates value for everyone, but only if reciprocated sufficiently to justify the cost**.

---

## DECISION RULE (PRIMARY LOGIC)

```
For each round t ∈ {1, 2, ..., r}:

IF (round is last round t == r):
    DEFECT
ELSE:
    cooperation_score = compute_cooperation_incentive()
    IF cooperation_score ≥ threshold:
        COOPERATE
    ELSE:
        DEFECT
```

### Computing Cooperation Incentive

```
cooperation_score = (k/n - 1) × average_cooperation_rate_observed + 
                     historical_payoff_comparison +
                     remaining_rounds_factor

WHERE:

average_cooperation_rate_observed = 
    (total cooperators across all previous rounds) / 
    (n × number of rounds played so far)

historical_payoff_comparison = 
    IF (my average payoff < opponent's average payoff in previous round):
        -0.3  (penalty: I'm losing, defection likely justified)
    ELSE IF (my average payoff > opponent's average payoff):
        +0.2  (bonus: cooperation is working)
    ELSE:
        0     (neutral)

remaining_rounds_factor = 
    (r - t) / r  (discount cooperation as endgame approaches)

threshold = 0.55
```

---

## DECISION RULES BY PHASE

### **ROUND 1 (Initialization)**
**Action: COOPERATE**

**Rationale:**
- Establish goodwill and signal cooperative intent
- Gather information about opponents' baseline preferences
- The value of cooperation (k > 1) suggests mutual benefit is possible
- First-round defection is unnecessarily aggressive

### **ROUNDS 2 to r-1 (Adaptive Phase)**
**Action: Apply primary logic above**

**Key behavioral patterns:**

| Observed Cooperation Rate | Interpretation | Response |
|---|---|---|
| ≥ 60% of players | Strong cooperation climate | COOPERATE (unless endgame) |
| 40-60% | Mixed environment | DEFECT if k/n marginal, else COOPERATE |
| < 40% | Defection dominant | DEFECT (punishment/self-protection) |
| Single others cooperating | I'm exploited | DEFECT (stop being sucker) |

**Adaptive cooling:**
- If I've defected last round AND others maintained cooperation: increase cooperation_score by +0.15 next round (guilt recovery)
- If I've cooperated last round AND most others defected: decrease cooperation_score by -0.25 next round (defensive shift)

### **ROUND r (Last Round)**
**Action: DEFECT**

**Rationale:**
- No future rounds, so reputation effects vanish
- Cooperation provides zero future benefit to me
- Standard backward induction logic

---

## EDGE CASES & SPECIAL HANDLING

### **Homogeneous Defection (All defect every round)**
- Detect: If cooperation_score remains ≤ 0.4 for 3+ consecutive rounds
- Response: DEFECT and maintain defection (no value to cooperation)
- Prevents wasteful attempts to reform hopeless groups

### **Sudden Shift in Group Behavior**
- Detect: Cooperation rate changes by >30% in one round
- Response: Recalibrate cooperation_score with decay weight on old observations
- Weight recent 3 rounds at 50%, prior rounds at 50%

### **Exploitation Scenario (Others defect while I cooperate)**
- Detect: I cooperated, received payoff < 1, while defectors received > 1
- Response: Defect next round, but monitor for reciprocal punishment or reform
- If group returns to cooperation: Re-enter at round t+2 with cautious cooperation

### **Perfect Cooperation Emerges (Nearly all cooperate)**
- Detect: ≥ 80% cooperation maintained for 2+ rounds
- Response: Maintain COOPERATION through endgame
- Exception: Still defect in final round (individual rationality)
- Rationale: High cooperation generates substantial surplus; free-riding in endgame breaks trust

---

## ROBUSTNESS PROPERTIES

**Against always-defectors:** Quickly identify and switch to DEFECT (minimizes losses)

**Against cooperators:** Reciprocate and maintain mutual benefit (maximizes prosocial payoff)

**Against tit-for-tat:** Cooperate initially; adapt if they punish cooperation (unlikely given perfect information)

**Against random players:** Smooth response based on aggregate rate, avoiding overreaction to noise

**Against exploiters (cooperate early, defect late):** Shift to defection once pattern detected via payoff comparison

---

## PROSOCIAL COMMITMENT

This strategy embodies prosocial values by:

1. **Leading with cooperation** rather than defection
2. **Rewarding cooperation** in others via reciprocation
3. **Preferring mutual gain** over individual advantage (defecting only when group cooperativity is <40%)
4. **Gracefully degrading** rather than escalating punishment
5. **Avoiding last-round exploitation** except where backward induction demands it (a necessary concession to game structure)

The strategy accepts lower payoff in many scenarios to maximize group welfare when others reciprocate. It only defects when cooperation creates genuine losses, not from pure self-interest.
'''

description_PROSOCIAL_14 = '''
# ADAPTIVE PROSOCIAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## STRATEGY NAME: Conditional Reciprocal Contribution (CRC)

---

## CORE PHILOSOPHY

This strategy pursues a **prosocial equilibrium** by:
1. **Leading with cooperation** to establish mutual benefit potential
2. **Monitoring collective health** of the group contribution rate
3. **Adapting dynamically** to group behavior while maintaining personal credibility
4. **Protecting against exploitation** without abandoning cooperation entirely
5. **Sustaining hope** for cooperation even when facing defectors

---

## DECISION RULES

### **ROUND 1 (Initialization)**
**Action: COOPERATE**

*Rationale:* Start prosocially to signal willingness to participate in mutual benefit. This establishes a cooperative baseline and tests whether others reciprocate.

---

### **ROUNDS 2 through R-1 (Middle Rounds)**

**Decision Rule:**

```
Let:
  - avg_cooperation = average cooperation rate observed in all previous rounds
                      = (total cooperators seen so far) / (previous_rounds × n)
  - threshold_high = 0.5
  - threshold_low = 0.25

IF avg_cooperation ≥ threshold_high:
    ACTION: COOPERATE
    Rationale: Group is maintaining healthy cooperation; reciprocate by contributing.

ELSE IF avg_cooperation ≥ threshold_low:
    ACTION: COOPERATE with probability = avg_cooperation
    Rationale: Mixed strategy that mirrors group's mixed behavior, maintaining some
               prosocial contribution while acknowledging defection patterns.

ELSE (avg_cooperation < threshold_low):
    ACTION: COOPERATE with probability = 0.15
    Rationale: Severe defection detected, but maintain low-level prosocial signal
               to avoid reinforcing complete breakdown. This "hope probability" 
               allows for group recovery.
```

---

### **ROUND R (Final Round)**

**Action: Evaluate end-game behavior**

```
IF avg_cooperation ≥ threshold_high (majority have cooperated):
    ACTION: COOPERATE
    Rationale: High cooperation observed throughout; honor the cooperative pattern
               to the end, rejecting short-term selfish exploitation.

ELSE:
    ACTION: DEFECT
    Rationale: If cooperation has broken down, no future rounds exist to punish
               defection. However, this is ONLY activated in the final round and
               only after observing low cooperation, minimizing damage.
```

*Prosocial qualifier:* This final-round defection is **conditional and limited**—it occurs only after clear evidence of group defection, and it represents adaptation rather than exploitation.

---

## EDGE CASES & SPECIAL HANDLING

### **Two-Round Games (r = 2)**
- Round 1: COOPERATE (standard initialization)
- Round 2: COOPERATE (treat as final round with optimistic assumption; avoid defection in shortest games)

**Rationale:** In minimal-round games, maintaining cooperation signals is critical for any hope of mutual benefit.

---

### **Very Large Groups (n ≥ 20)**
Increase `threshold_high` to 0.6 and `threshold_low` to 0.35

**Rationale:** Large groups have naturally higher free-riding pressure. Adjusting thresholds accounts for realistic larger-group dynamics while maintaining the prosocial intent.

---

### **Low Multiplication Factor (k close to 1)**
Reduce `hope probability` from 0.15 to 0.10 in severe defection scenarios

**Rationale:** When k < 1.5, the public good return is weak; maintain contribution only as a symbolic prosocial gesture while being realistic about payoff structure.

---

### **Extremely High Multiplication Factor (k close to n)**
Increase `threshold_high` to 0.45

**Rationale:** High k makes cooperation extremely valuable for everyone. Be more willing to sustain cooperation since the multiplier effect is strong.

---

## ROBUSTNESS PROPERTIES

This strategy is **robust** to:

| Opponent Type | How CRC Responds |
|---|---|
| **Pure cooperators** | Matches them; achieves mutual benefit |
| **Pure defectors** | Reduces contribution to 15% in middle rounds (symbolic); defects in final round only |
| **Tit-for-tat variants** | Cooperates when they cooperate; adapts when they defect |
| **Mixed strategists** | Mirrors their average behavior through probability-based responses |
| **Unpredictable opponents** | Falls back to group-rate monitoring, which averages out noise |
| **Late-game exploiters** | Protects against final-round defection while maintaining history of cooperation |

---

## PROSOCIAL ALIGNMENT

**This strategy is prosocial because:**

1. **Leads with trust:** First move is always cooperation, giving others the benefit of the doubt
2. **Reciprocates in spirit:** Adapts to group cooperation rates, encouraging mutual benefit
3. **Avoids aggressive punishment:** Never defects in non-final rounds; no tit-for-tat escalation
4. **Maintains hope:** Even under 25% cooperation rate, maintains 15% "hope probability" to allow group recovery
5. **Earns legitimacy:** High cooperation rate creates strong reciprocal incentives for others
6. **Protects the game:** Doesn't exploit final-round weakness until convinced others have abandoned cooperation
7. **Transparent logic:** Strategy depends only on observable history, not on assumptions about others' strategies

---

## PSEUDOCODE

```
function CRC_Strategy(round_number, n, k, history):
    
    if round_number == 1:
        return COOPERATE
    
    // Calculate average cooperation rate
    avg_coop = sum(all_cooperators_in_previous_rounds) / (round_number - 1) / n
    
    if round_number == r:  // Final round
        if avg_coop >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Middle rounds
    threshold_high = 0.5
    threshold_low = 0.25
    
    if avg_coop >= threshold_high:
        return COOPERATE
    
    else if avg_coop >= threshold_low:
        return COOPERATE_WITH_PROBABILITY(avg_coop)
    
    else:
        return COOPERATE_WITH_PROBABILITY(0.15)
```

---

## EXPECTED OUTCOMES

Against a diverse tournament:
- **vs. cooperators:** Achieves near-optimal mutual payoff (~2.0 per round for typical parameters)
- **vs. defectors:** Minimizes exploitation while maintaining positive group contributions
- **vs. mixed:** Achieves moderate-to-good payoff through adaptive mirroring
- **Overall:** Aims for positive-sum outcomes that reward participation in the public good
'''

description_PROSOCIAL_15 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy
This strategy balances prosocial cooperation with strategic robustness by:
1. **Initiating cooperation** to establish mutual benefit
2. **Adapting to observed cooperation rates** to maintain sustainability
3. **Protecting against exploitation** without abandoning prosocial intent
4. **Maximizing collective welfare** while remaining individually rational

---

## DECISION RULES

### Primary Rule: Adaptive Cooperation Threshold

```
cooperation_rate_observed = (total_cooperators_in_previous_rounds) / (n × rounds_completed)

IF round == 1:
    COOPERATE  // Establish goodwill; signal prosocial intent

ELSE IF round == r (final round):
    IF cooperation_rate_observed ≥ k/n:
        COOPERATE  // Reciprocate if others have cooperated sufficiently
    ELSE:
        DEFECT  // Protect against exploitation at game's end

ELSE:  // Middle rounds (2 to r-1)
    IF cooperation_rate_observed ≥ threshold_lower:
        COOPERATE  // Maintain reciprocal cooperation
    ELSE IF cooperation_rate_observed < threshold_lower:
        DEFECT  // Reduce contribution if widespread defection observed
    
    // Restore cooperation if others respond
    IF defected_last_round AND cooperation_rate_observed > threshold_restore:
        COOPERATE  // Give second chance if cooperation increases
```

### Threshold Parameters

```
threshold_lower = k/n + δ_buffer
threshold_restore = k/n + δ_recovery

where:
δ_buffer ≈ 0.10  (10% buffer: slight optimism bias toward cooperation)
δ_recovery ≈ 0.05 (5% recovery: easier to return to cooperation than to enter it)

Intuition: Cooperate if others are cooperating at rates that at least cover the 
multiplier return (k/n). The buffer allows for noise and imperfect coordination.
```

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (Initialization)
- **Action**: Always COOPERATE
- **Rationale**: Avoids being the first defector; signals willingness to coordinate; establishes the prosocial frame

### Round r (Final Round)
- **Action**: Conditional on observed history
- **Rationale**: The final round is a standard one-shot game; defecting is individually rational if cooperation has been low. However, reciprocal defection against cooperators is avoided—only defect if the environment has proven largely uncooperative.

### Rounds with Perfect Cooperation (all previous rounds: all players C)
- **Action**: COOPERATE
- **Rationale**: Maintain the virtuous equilibrium

### Rounds with Perfect Defection (all previous rounds: all players D)
- **Action**: DEFECT (except Round 1)
- **Rationale**: Prevents exploitation. Payoff from cooperating = (k/n) × 0 = 0. Payoff from defecting = 1. Cooperating is individually irrational and not reciprocated.

### Sudden Drops in Cooperation Rate
- **Action**: DEFECT for one round, then reassess
- **Rationale**: Punish sudden defections to discourage them, but allow recovery if cooperation resumes (avoiding mutual defection traps)

### Near-Final Rounds (r-2, r-1)
- **Action**: Slightly more cooperative than middle rounds
- **Rationale**: Recognize that endgame dynamics don't fully apply; maintain prosocial posture while preparing for final-round risk

---

## PSEUDOCODE

```pseudocode
FUNCTION decide_action(round, r, n, k, history):
    
    IF round == 1:
        RETURN COOPERATE
    
    // Compute observed cooperation rate from history
    total_contributions = SUM(all_c_values_in_history)
    max_possible = n × (round - 1)
    cooperation_rate = total_contributions / max_possible
    
    // Compute thresholds
    critical_rate = k / n
    threshold_lower = critical_rate + 0.10
    threshold_restore = critical_rate + 0.05
    
    // Final round logic
    IF round == r:
        IF cooperation_rate ≥ threshold_lower:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    // Middle rounds logic
    my_last_action = history[round - 1].my_action
    
    IF my_last_action == DEFECT AND cooperation_rate > threshold_restore:
        // Recovery attempt: others responded positively
        RETURN COOPERATE
    
    ELSE IF cooperation_rate ≥ threshold_lower:
        RETURN COOPERATE
    
    ELSE:
        RETURN DEFECT
    
END FUNCTION
```

---

## PROSOCIAL ALIGNMENT

### Why This Strategy is Prosocial:

1. **Cooperation First**: Initiates with unconditional cooperation, establishing cooperative norms
2. **Reciprocity, Not Punishment**: Defects only when cooperation is exploited; never defects unprovoked
3. **Sustainability Focus**: Thresholds are calibrated to maintain mutual benefit (cooperative equilibrium where payoff ≥ 1 for all)
4. **Forgiveness**: Immediately returns to cooperation when others do, allowing recovery from temporary defection
5. **Collective Welfare**: By sustaining high cooperation rates, the strategy maximizes total payoff for the group (when others reciprocate)

### Robustness:

- **Against Unconditional Cooperators**: Performs excellently (achieves mutual cooperation)
- **Against Defectors**: Protects itself after detecting exploitation; limits losses
- **Against Oscillators**: Adapts dynamically; doesn't lock into punishment cycles
- **Against Mixed Strategies**: Threshold-based logic handles probabilistic cooperation gracefully

---

## KEY INSIGHT

The strategy implements a **trust-but-verify** approach: assume others are cooperative (prosocial default), but adjust expectations based on observed behavior. This balances the tension between maximizing individual payoff and promoting collective welfare, with a principled bias toward prosocial outcomes when reciprocity is possible.
'''

description_PROSOCIAL_16 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial objectives with game-theoretic robustness. The fundamental insight is that **maximum collective welfare occurs at universal cooperation**, but defection is individually rational when others cooperate. ARC addresses this by:

1. **Starting optimistically** to establish cooperation
2. **Adapting to others' behavior** to avoid exploitation
3. **Maintaining long-term cooperation incentives** rather than short-term punishment
4. **Recovering from cooperation breakdown** rather than locking into mutual defection

---

## Decision Rules

### Rule 1: First Round (t = 1)
**COOPERATE**

*Rationale:* Without history, cooperation signals prosocial intent and creates conditions for mutual benefit. This maximizes expected payoff if even a moderate fraction of opponents cooperate.

---

### Rule 2: Rounds 2 through r-1 (Adaptive Phase)

Calculate the **Cooperation Rate (CR)** from the previous round:

```
CR = (number of cooperators in round t-1) / n
```

**Decision:**
- **IF CR ≥ Threshold_High (default: 0.50):** COOPERATE
  - *Rationale:* Majority cooperation signals reciprocal willingness. Cooperating maintains the coalition and maximizes payoff when k > 1.

- **ELSE IF CR ≥ Threshold_Low (default: 0.25):** COOPERATE with decay
  - *Rationale:* Even minority cooperation may indicate recovering reciprocators or misaligned incentives. Continue contributing to leave room for cooperation to rebuild rather than collapsing into mutual defection.

- **ELSE IF CR < Threshold_Low:** DEFECT
  - *Rationale:* When cooperation has collapsed to near-zero, defection minimizes losses. Continued cooperation becomes exploitation.

**Threshold Rationale:**
- Threshold_High = 0.50: At or above 50% cooperation, the cooperative coalition is self-sustaining under most parameter values (k > 1, n ≥ 2).
- Threshold_Low = 0.25: Preserves recovery pathways—even if only 25% cooperate, mutual punishment doesn't make game-theoretic sense.

---

### Rule 3: Final Round (t = r)

In the final round, **always DEFECT**.

*Rationale:* 
- With no future rounds, the folk theorem no longer sustains cooperation through repeated-game incentives
- Defection maximizes payoff in this isolated round
- This honest reflection of incentive structure is strategically sound (no credibility cost)

**Exception:** If this strategy is known to be widely adopted and defection in the final round creates perverse incentives for earlier round breakdown, cooperate in the final round instead. However, given the no-communication constraint and tournament context, final-round defection is the robust choice.

---

## Pseudocode

```
STRATEGY ARC(game_parameters, history):
  
  current_round = length(history) + 1
  n = game_parameters.n
  k = game_parameters.k
  r = game_parameters.r
  threshold_high = 0.50
  threshold_low = 0.25
  
  IF current_round == 1:
    RETURN COOPERATE
  
  ELSE IF current_round == r:
    RETURN DEFECT
  
  ELSE:
    previous_round = history[current_round - 1]
    cooperators_last_round = count(action == COOPERATE in previous_round)
    cooperation_rate = cooperators_last_round / n
    
    IF cooperation_rate >= threshold_high:
      RETURN COOPERATE
    ELSE IF cooperation_rate >= threshold_low:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
```

---

## Edge Cases & Special Scenarios

### Edge Case 1: Very Small n (n = 2)
For a two-player game, thresholds become binary: either the opponent cooperates or defects.
- Threshold_High = 0.50 means any cooperation triggers reciprocation
- Threshold_Low = 0.25 is never reached (0 vs. 1 cooperator in previous round)
- Strategy reduces to: Cooperate if opponent cooperated, defect if opponent defected (after round 1)
- **Result:** Tit-for-tat variant—maximally robust in 2-player settings

### Edge Case 2: Very Small r (r = 2)
Only two rounds: cooperate in round 1, defect in round 2.
- Round 1: Cooperate unconditionally
- Round 2: Defect unconditionally (final round rule)
- **Result:** Transparent, unavoidable defection in final round. Sets expectations clearly.

### Edge Case 3: High k, Low n (e.g., k = 3.9, n = 4)
Cooperation is extremely valuable per contributor. Even small coalitions create large payoffs.
- Thresholds remain constant (0.50, 0.25)
- Strategy maintains cooperation longer (tolerates lower CR before defecting)
- **Result:** Amplifies prosocial outcomes when cooperation is especially valuable

### Edge Case 4: Low k, High n (e.g., k = 1.1, n = 100)
Cooperation barely justified. Free-riding is highly attractive.
- Thresholds remain constant
- Strategy defects sooner, which is appropriate—cooperation's benefit is marginal
- **Result:** Avoids wasting contributions in low-multiplier scenarios

### Edge Case 5: Opponent is Unconditional Defector
- Round 1: ARC cooperates; opponent defects
- CR after round 1 = 1/n (only ARC cooperates)
- If 1/n < 0.25 (i.e., n > 4), ARC defects in round 2 onward
- If 1/n ≥ 0.25 (i.e., n ≤ 4), ARC continues cooperating for one more round before likely defecting
- **Result:** Limits exploitation; ARC doesn't sustain unilateral cooperation forever

### Edge Case 6: Mixed Reciprocators
If opponents use strategies that sometimes cooperate, ARC tracks the aggregate cooperation rate dynamically.
- If 25% of opponents are reciprocators, CR hovers around 0.25
- ARC remains in the "decay" zone, cooperating but ready to exit
- **Result:** Neither exploits nor is exploited; settles into a stable equilibrium

---

## Why This Strategy is Prosocial

1. **Collective Welfare Priority:** ARC cooperates from the start, maximizing the game's total welfare when others reciprocate.

2. **Non-Punitive:** Rather than punishing defectors harshly (e.g., Tit-for-Tat), ARC allows recovery. A round of low cooperation doesn't trigger permanent mutual defection if cooperation rebounds.

3. **Threshold-Based Adaptation:** The strategy acknowledges that perfect cooperation is often impossible while still maximizing the zone of cooperation. It gracefully degrades only when cooperation becomes unsustainable.

4. **Fairness:** The strategy doesn't exploit others. It cooperates when others do and shares the public good equally.

5. **Honest About Incentives:** Final-round defection reflects true incentive structure without deception, maintaining moral integrity.

---

## Robustness Across Tournament Scenarios

- **vs. Always-Cooperate:** ARC matches cooperation, yielding mutual high payoffs
- **vs. Always-Defect:** ARC exits quickly (after 1-2 rounds), minimizing exploitation
- **vs. Tit-for-Tat:** ARC is compatible; both maintain cooperation
- **vs. Mixed Strategies:** ARC adapts based on observed cooperation rate, finding stable equilibria
- **vs. Sophisticated Strategies:** ARC's simplicity prevents over-fitting; it performs well across parameter ranges

---

## Summary

**Adaptive Reciprocal Contribution (ARC)** is a prosocial strategy that cooperates optimistically, adapts to observed cooperation, maintains recovery pathways, and exits exploitation gracefully. It prioritizes long-term collective welfare while protecting against systematic exploitation—a balance essential for robust prosocial behavior in multi-agent tournament settings.
'''

description_PROSOCIAL_17 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection. It operates on the principle that:
1. **Cooperation is valuable** when others reciprocate (since k > 1, collective welfare improves)
2. **Defection must be punished** to prevent exploitation
3. **Recovery is always possible** to enable redemption and re-establishment of cooperation

The strategy is prosocial because it prioritizes cooperation when feasible, but protects against free-riders to sustain long-term collective welfare.

---

## Decision Rules

### **Round 1 (Initial Trust)**
**COOPERATE**

Rationale: Without history, assume good faith. This gives others the opportunity to establish a cooperative equilibrium and signals cooperative intent.

### **Rounds 2 to r-1 (Adaptive Reciprocity)**

Calculate the **Cooperation Index** from the previous round:

```
cooperation_rate = (number of cooperators in round t-1) / n
```

**Decision Rule:**
- **IF** `cooperation_rate ≥ threshold_high` (default: 0.5)
  - **COOPERATE**
  - Rationale: Majority cooperation signals a cooperative norm emerging. Joining strengthens collective welfare.

- **ELSE IF** `cooperation_rate ≥ threshold_low` (default: 0.25)
  - **COOPERATE with probability p_persist** (default: 0.7)
  - Rationale: Minority cooperation remains valuable if k > 1. Persist with high probability, but inject occasional defections to avoid exploitation. This probes the stability of cooperation.

- **ELSE** (cooperation_rate < 0.25)
  - **DEFECT**
  - Rationale: Widespread defection signals a defection norm. Contributing would be exploited. Protect endowment.

### **Final Round r (Last-Round Clarity)**

**Special handling for the final round:**

- **IF** `cooperation_rate ≥ threshold_high`
  - **COOPERATE**
  - Rationale: In the final round, no future retaliation is possible, but cooperation still generates immediate positive payoff if others cooperate. This expresses genuine prosocial values.

- **ELSE**
  - **DEFECT**
  - Rationale: If cooperation is failing, no future rounds remain to benefit from establishing norms. Optimize immediate payoff.

---

## Edge Cases & Special Conditions

### **Round 1 Exceptions**
- If any prior information about player types is revealed (though this game specifies no communication): Still cooperate. The strategy should not assume adversarial opponents.

### **Exploitation Detection**
If a player detects they were the **sole cooperator** in a previous round:
- **Allow one defection round** as punishment
- **Resume reciprocal strategy** in the next round
- Rationale: Severe exploitation merits a clear signal ("I noticed"), but avoid permanent grudges which reduce collective welfare.

### **Oscillating Behavior Detection**
If cooperation_rate oscillates between extremes (< 0.25 and > 0.5 in consecutive rounds):
- **COOPERATE** regardless
- Rationale: Unstable groups need a stabilizing force. A prosocial player should provide it.

### **All-Defection Scenario**
If everyone defected in round t-1 (cooperation_rate = 0):
- **DEFECT** in round t
- Resume reciprocal strategy in round t+1
- Rationale: One round of matching defection signals non-exploitability, then immediately attempt reconciliation.

---

## Pseudocode

```
strategy(round, history, n, k, r):
    
    if round == 1:
        return COOPERATE
    
    if round == r:  // Final round
        prev_cooperators = count_cooperators(history[round-1])
        cooperation_rate = prev_cooperators / n
        
        if cooperation_rate >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Rounds 2 to r-1
    prev_cooperators = count_cooperators(history[round-1])
    cooperation_rate = prev_cooperators / n
    
    my_action_last_round = history[round-1][my_id]
    sole_cooperator = (my_action_last_round == COOPERATE 
                       AND prev_cooperators == 1)
    
    if sole_cooperator:
        // Punish exploitation with one defection
        return DEFECT
    
    if cooperation_rate >= 0.5:
        return COOPERATE
    
    else if cooperation_rate >= 0.25:
        // Persist with 70% probability
        return COOPERATE with probability 0.7
               DEFECT   with probability 0.3
    
    else:  // cooperation_rate < 0.25
        return DEFECT
```

---

## Robustness Analysis

### Against Various Opponent Types:

1. **Unconditional Cooperators**: ARC cooperates consistently → mutual benefit
2. **Unconditional Defectors**: ARC defects after detecting low cooperation → not exploited
3. **Tit-for-Tat Players**: ARC reciprocates → mutual cooperation emerges
4. **Random Players**: ARC's thresholds smooth out noise → stable cooperation if k supports it
5. **Sophisticated Strategists**: ARC's final-round defection is consistent; mid-game probabilistic mixing prevents predictable exploitation

### Why This Is Prosocial:

- **Maximizes collective welfare** when feasible (cooperates at 50%+ cooperation rate)
- **Doesn't enable exploitation** through permanent defection patterns
- **Signals trustworthiness** via round 1 cooperation
- **Allows redemption** by returning to reciprocity after punishment
- **Stabilizes groups** by being a reliable cooperative anchor

---

## Parameter Recommendations

- `threshold_high = 0.5`: Majority rule for robust cooperation
- `threshold_low = 0.25`: At least 25% of group cooperating typically justifies contribution (k > 1)
- `p_persist = 0.7`: High persistence in gray zone, but probe stability

These can be tuned based on empirical tournament results.
'''

description_PROSOCIAL_18 = '''
# PROSOCIAL ADAPTIVE CONTRIBUTION STRATEGY (PACS)

## CORE PHILOSOPHY

This strategy balances prosocial value creation with resilience against exploitation. The key insight is that **sustainable cooperation requires demonstrating both willingness to contribute AND ability to withdraw** when the public good is being systematically under-provisioned.

---

## DECISION RULES

### PRIMARY RULE: Adaptive Threshold Cooperation

**Cooperate if and only if:**
```
(observed_cooperation_rate ≥ minimum_threshold) 
OR 
(round_number == 1)
```

Where:
- **observed_cooperation_rate** = (total cooperators in previous round) / n
- **minimum_threshold** = k / (2n)

### RATIONALE FOR THRESHOLD

The threshold k/(2n) is calibrated to:
- **Lower bound**: If fewer than k/(2n) proportion cooperate, the public good multiplier creates insufficient return. For remaining cooperators: k/n × (few contributors) < 1, so C yields less than D
- **Upper bound**: If at least k/(2n) proportion cooperate, cooperation becomes mutually beneficial
- This threshold is **independent of opponent strategy** and depends only on game parameters

---

## ROUND-SPECIFIC BEHAVIOR

### Round 1: COOPERATE
- **Rationale**: Signal prosocial intent without historical evidence
- **Effect**: Establish baseline, demonstrate good faith
- **Risk**: Accept first-round defection from others

### Rounds 2 to r-1: APPLY ADAPTIVE THRESHOLD
- Track cooperation rate from previous round
- Decision follows primary rule above
- **Gradual degradation**: If cooperation rate remains above threshold across consecutive rounds, maintain cooperation (mutual reinforcement)
- **Rapid recovery**: If cooperation rate exceeds threshold again after dropping below it, resume cooperation (not grudge-holding)

### Final Round (r): SPECIAL CASE
**Same as rounds 2 to r-1** (no end-game defection)
- **Rationale**: Defecting in final round gains at most 1 point while destroying cooperative surplus from that round
- **Prosocial consistency**: Maintain integrity when it matters most, even without reputational future

---

## HANDLING EDGE CASES

### Case 1: Extremely Small Groups (n=2)
- Threshold = k/4
- If opponent defects, defect immediately (mutual defection stable)
- If opponent cooperates, cooperate (mutual cooperation is Pareto optimal when k > 1)

### Case 2: Very High Multiplication Factor (k → n)
- Threshold approaches 1/2
- Strategy tends toward sustained cooperation (public good is efficient)

### Case 3: Very Low Multiplication Factor (k → 1)
- Threshold approaches 1/(2n)
- Strategy is more defection-prone (public good less efficient)
- **This is correct behavior**: Don't subsidize bad projects

### Case 4: Single Repeat (r=2)
- Round 1: Cooperate
- Round 2: Apply threshold based on round 1 observation
- No artificial end-game effects

### Case 5: Mixed or Chaotic Opponents
- If cooperation rate fluctuates around threshold, switching occurs
- **Smoothing option** (optional enhancement): Use exponential moving average of last 3 rounds instead of previous round only
- This adds robustness to random noise

---

## PROSOCIAL ALIGNMENT

### Why This Strategy Is Prosocial

1. **Value Creation**: Cooperates whenever the multiplier justifies it (k/(2n) threshold ensures C-dominated payoff scenario)

2. **Sustainability**: Doesn't exploit others' cooperation for selfish gain
   - If others cooperate sufficiently, reciprocate
   - If they don't, withdraw (don't throw money away)

3. **Fairness**: Makes no assumptions about identity of other players
   - Same threshold applied uniformly
   - No retaliation or punishment beyond withdrawal

4. **Transparency**: Decision rule is entirely observable and predictable from parameters
   - Others can learn: "If we cooperate above this threshold, this player cooperates"
   - Creates stability through mutual understanding

5. **Resilience**: Robust to free-riders but doesn't punish accidentally low cooperation
   - Recovers immediately when conditions improve
   - No cycles of tit-for-tat escalation

---

## PSEUDOCODE

```
STRATEGY(current_round, history, n, k, r):
  
  // First round: always cooperate
  IF current_round == 1:
    RETURN COOPERATE
  
  // Subsequent rounds: threshold-based
  ELSE:
    prev_round = current_round - 1
    cooperation_count = count(COOPERATE in history[prev_round])
    cooperation_rate = cooperation_count / n
    
    threshold = k / (2 * n)
    
    IF cooperation_rate >= threshold:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
```

---

## TOURNAMENT ROBUSTNESS

This strategy performs well against:
- **All cooperators**: Cooperates throughout, achieves efficiency
- **All defectors**: Defects from round 2 onward, minimizes losses
- **Tit-for-tat variants**: Engages in cooperation when threshold met, avoids escalation
- **Conditional cooperators**: Aligns naturally; both benefit from coordinating above threshold
- **Random players**: Treats high variance as sustained low cooperation, defects prudently

**Non-exploitable**: No opponent can consistently earn more by changing their strategy unilaterally, given the threshold mechanism.
'''

description_PROSOCIAL_19 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy
This strategy balances prosocial impulses with strategic robustness by:
1. **Leading with cooperation** to establish mutual benefit
2. **Adapting to observed behavior** to avoid exploitation
3. **Maintaining long-term cooperation potential** even against defectors
4. **Maximizing collective welfare** when sustainable

---

## DECISION RULES

### Round 1 (Initialization)
**Action: COOPERATE**

**Rationale:** 
- Cooperation is the only way to establish that mutual cooperation yields payoff of k (the highest per-player outcome when all cooperate)
- Defecting first round signals non-cooperation unnecessarily
- We gather information by extending trust

### Rounds 2 through r-1 (Adaptive Phase)

**Calculate Cooperation Rate from Previous Rounds:**
```
cooperation_rate = (total cooperators in rounds 1 to t-1) / (n × (t-1))
```

**Decision Logic:**

```
IF cooperation_rate ≥ threshold_high (e.g., 0.75):
    → COOPERATE
    Reason: Strong cooperation environment; mutual benefit is being realized
    
ELSE IF cooperation_rate ≥ threshold_mid (e.g., 0.40):
    → COOPERATE with probability p_adaptive
    where p_adaptive = cooperation_rate
    Reason: Mixed environment; probabilistic cooperation maintains hope 
            while protecting against systematic defection
    
ELSE IF cooperation_rate < threshold_mid:
    → DEFECT
    Reason: Cooperation is not being reciprocated; prevent exploitation
```

**Why This Thresholding Works:**
- **High cooperation (≥75%)**: Network is healthy; full participation maximizes collective welfare
- **Mixed cooperation (40-75%)**: Some cooperation exists; probabilistic matching of observed rates preserves incentives for others while limiting losses
- **Low cooperation (<40%)**: Defection dominance detected; cut losses while remaining available for revival

### Round r (Final Round - Special Handling)

**Action: Match Previous Round Behavior (Modified Generosity)**

```
IF my_action_in_round_r-1 == COOPERATE:
    → COOPERATE (commit to the pattern)
    
ELSE IF my_action_in_round_r-1 == DEFECT AND cooperation_rate ≥ 0.50:
    → COOPERATE (final gesture to encourage revival)
    
ELSE:
    → DEFECT (no last-round exploitation reversal)
```

**Rationale:**
- Avoid "last-round defection" betrayal when cooperation exists
- This differs from pure game theory because it builds reputation for reliability
- If environment has broken down significantly, defecting in final round doesn't damage future interactions (none exist) but does prevent final exploitation

---

## EDGE CASES & SPECIAL CONDITIONS

### Extreme n values
- **Large n (n > 20):** Lower threshold_high to 0.60 (collective action problems are harder)
- **Small n (n = 2-3):** Raise threshold_mid to 0.50 (each individual matters more; more sensitive to defection)

### Extremely low k values (k ≤ 1.5)
```
IF k ≤ 1.5:
    Shift to threshold_mid = 0.60
    Reason: Cooperation barely beats mutual defection; only cooperate when clearly reciprocated
```

### Extremely high k values (k ≥ n-1)
```
IF k ≥ n-0.5:
    Always COOPERATE
    Reason: Full cooperation yields nearly n payoff per player; mathematical advantage overwhelms risk
```

### Very small r (r = 2)
```
Round 1: COOPERATE
Round 2: COOPERATE (give at least one chance for reciprocity)
```

---

## HANDLING UNOBSERVED PAYOFFS
If the game structure prevents observing exactly which players cooperated (only aggregate total observed):

```
Use aggregate cooperation rate as proxy for individual patterns
Assume uniform distribution of cooperators unless given evidence otherwise
Apply same thresholds to aggregate data
```

---

## ROBUSTNESS ANALYSIS

| Opponent Type | Expected Outcome |
|---|---|
| All Cooperators | Mutual cooperation; payoff = k |
| All Defectors | Switch to defection quickly; payoff ≈ 1 |
| Tit-for-Tat | Sustained mutual cooperation |
| Random 50/50 | Probabilistic cooperation until threshold shifts to defection |
| Conditional Cooperators | Positive feedback loop |
| Exploiters (exploit cooperators) | Detected by low cooperation_rate; defection after threshold |

---

## PSEUDOCODE

```python
def decide_action(round_number, history, n, k, r):
    
    # Round 1: Lead with cooperation
    if round_number == 1:
        return COOPERATE
    
    # Calculate cooperation rate from history
    total_cooperators = sum(round_cooperator_counts)
    cooperation_rate = total_cooperators / (n * (round_number - 1))
    
    # Adjust thresholds for extreme parameters
    threshold_high = 0.75
    threshold_mid = 0.40
    
    if k <= 1.5:
        threshold_mid = 0.60
    if n > 20:
        threshold_high = 0.60
    
    # Final round special logic
    if round_number == r:
        if my_previous_action == COOPERATE:
            return COOPERATE
        elif cooperation_rate >= 0.50:
            return COOPERATE
        else:
            return DEFECT
    
    # Adaptive phase (rounds 2 to r-1)
    if cooperation_rate >= threshold_high:
        return COOPERATE
    
    elif cooperation_rate >= threshold_mid:
        return COOPERATE with probability = cooperation_rate
    
    else:
        return DEFECT
```

---

## ALIGNMENT WITH PROSOCIAL MINDSET

✓ **Leads with generosity:** Cooperates first to enable mutual benefit  
✓ **Responds to others:** Adapts based on observed cooperation, not fixed pattern  
✓ **Proportional reciprocity:** Matches observed cooperation rates probabilistically  
✓ **Avoids exploitation:** Defects when cooperation goes unreciprocated  
✓ **Supports revival:** Even low-cooperation environments get probabilistic chances  
✓ **Final generosity:** Cooperates in final round if environment permits, creating positive closure  
✓ **Transparent logic:** Strategy depends only on observable history and public parameters

This strategy seeks the Pareto-efficient cooperative equilibrium while maintaining individual rationality against exploiters.
'''

description_PROSOCIAL_20 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## CORE PHILOSOPHY

This strategy balances three objectives:
1. **Prosocial intent**: Maximize collective welfare when possible
2. **Robustness**: Protect against exploitation without permanent punishment
3. **Adaptability**: Learn from observed behavior and adjust dynamically

The key insight: In public goods games, cooperation creates value for everyone, but requires trust. We should cooperate generously early, monitor for exploitation, and adjust our contribution level based on how much others are contributing.

---

## DECISION RULE: Contribution Level Based on Observed Cooperation Rate

### ROUND-BY-ROUND STRATEGY

**Round 1 (Opening Move):**
- **Action: COOPERATE**
- **Rationale**: Extend trust and signal prosocial intent. Starting with cooperation encourages reciprocal behavior and helps establish a cooperative equilibrium.

**Rounds 2 through r-1 (Adaptive Middle Game):**

Calculate the **observed cooperation rate** from previous rounds:
```
cooperation_rate = (total cooperators in rounds 1 to t-1) / (n × (t-1))
```

Apply the following decision rule:

```
IF cooperation_rate ≥ (k - 1) / n:
    COOPERATE
    // Cooperative threshold: collective benefit exceeds individual defection benefit
    // When others cooperate sufficiently, cooperation is rational and prosocial
    
ELSE IF cooperation_rate ≥ 0.33:
    COOPERATE with probability: cooperation_rate
    // Graduated defection: match the cooperation level probabilistically
    // Creates pressure for free-riders while remaining optimistic
    
ELSE:
    DEFECT
    // Only defect when cooperation has collapsed
    // Minimizes losses in a non-cooperative environment
```

**Round r (Final Round):**
- **Action: COOPERATE**
- **Rationale**: 
  - Reaffirm prosocial commitment even without future reciprocation opportunity
  - Demonstrates that cooperation isn't conditional manipulation
  - Contributes to potential future reputation effects in meta-game
  - Aligns with intrinsic prosocial values

---

## CRITICAL THRESHOLD JUSTIFICATION

The threshold `(k-1)/n` represents the **breakeven cooperation rate**:

- When cooperation_rate = (k-1)/n, the total public good payoff equals the private payoff from defection
- At this point, cooperation is **individually rational** (not exploitative)
- Below this rate, cooperation is dominated by defection in expected value

**Example with n=6, k=2:**
- Threshold = (2-1)/6 ≈ 0.167
- If more than 16.7% of players cooperate, joining them is individually rational
- This creates a **pro-cooperation tipping point**

---

## HANDLING EDGE CASES

**Minority Defection (some players always defect):**
- Strategy gradually reduces to probabilistic matching
- Eventually defects if cooperation rate stays below threshold
- This is **not punishment** but **rational adaptation** given diminished returns

**Majority Defection (cooperation collapse):**
- Strategy switches to universal defection
- Minimizes continued losses
- Leaves door open for recovery if others change behavior

**Perfect Cooperation (all players cooperate every round):**
- Strategy continues cooperating
- Achieves optimal collective outcome: π_i = k for all players

**Perfect Defection (all players defect every round):**
- Strategy recognizes this after round 1
- Defects in rounds 2-r
- Final round cooperation is a "beacon" showing willingness to cooperate if others reciprocate

---

## WHY THIS IS PROSOCIAL

1. **Genuine cooperation**: We cooperate when it doesn't cause exploitation (round 1, high cooperation environments, final round)

2. **Not naive**: We adapt to free-riders rather than enabling systematic exploitation

3. **Optimistic but cautious**: Probabilistic cooperation below threshold keeps hope alive while protecting welfare

4. **Transparent reciprocity**: Our behavior clearly rewards cooperation and encourages others to cooperate, creating positive feedback loops

5. **Avoids punishment spirals**: Unlike Tit-For-Tat, we don't enter destructive cycles; we only reduce cooperation when returns genuinely diminish

---

## PSEUDOCODE

```
function decide_action(round_t, history):
    
    IF round_t == 1:
        return COOPERATE
    
    IF round_t == r:
        return COOPERATE
    
    // Middle rounds: calculate cooperation rate
    total_cooperators = count_cooperators_in_history(history)
    cooperation_rate = total_cooperators / (n × (round_t - 1))
    
    payoff_threshold = (k - 1) / n
    
    IF cooperation_rate >= payoff_threshold:
        return COOPERATE
    
    ELSE IF cooperation_rate >= 0.33:
        IF random() < cooperation_rate:
            return COOPERATE
        ELSE:
            return DEFECT
    
    ELSE:
        return DEFECT
```

---

## TOURNAMENT RESILIENCE

This strategy performs well against:
- **Cooperators**: Mutual cooperation → high payoffs
- **Defectors**: Recognizes and stops enabling → minimizes losses
- **Tit-for-Tat variants**: Doesn't escalate punishment; reaches stable state
- **Mixed strategies**: Probabilistic matching prevents exploitation
- **Unknown opponents**: Initial cooperation sends prosocial signal; adaptation protects welfare
'''

description_PROSOCIAL_21 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "GRADUATED RECIPROCAL COOPERATION WITH PROPORTIONAL RETALIATION"

## STRATEGIC PHILOSOPHY

This strategy balances three competing objectives:
1. **Prosocial impact**: Maximize collective welfare when possible
2. **Robustness**: Avoid exploitation by purely selfish opponents
3. **Adaptability**: Respond dynamically to each opponent's revealed preferences

The core insight is that in repeated games with perfect information, we can shift from purely defective opponents toward conditional cooperation while rewarding cooperative peers.

---

## DECISION RULES

### PRIMARY RULE: Cooperation Threshold Model

For each round t, compute the **cooperation rate** from all previous rounds:

```
cooperation_rate = (total cooperators across all rounds and players) / 
                   (t-1) × n
```

**Decision Logic:**
- **Round 1**: COOPERATE (prosocial opening, establish intention)
- **Rounds 2 to r-1**: 
  - IF cooperation_rate > 50% OR t < 3: COOPERATE
  - ELSE IF cooperation_rate ≤ 50%: Apply "Proportional Response"
- **Final round (t = r)**: Defect (end-game incentive collapse)

### PROPORTIONAL RESPONSE (for rounds 2 to r-1 when cooperation_rate ≤ 50%)

Calculate the **opponent cooperation index** based on observed defections:

```
opponent_cooperation = (average cooperators per round) / n
```

**Probabilistic cooperation:**
```
P(Cooperate) = opponent_cooperation × (1 - (r - t) / r × 0.2)
```

This means:
- If opponents averaged 70% cooperation: ~70% chance you cooperate this round
- Slowly shift toward defection in final rounds (decay factor) to minimize last-round losses
- Maintain some cooperation to reward genuinely prosocial players even in defection-prone environments

---

## EDGE CASE HANDLING

### Round 1
- **Action**: COOPERATE unconditionally
- **Rationale**: Reveals peaceful intent without information; establishes baseline for reputation

### Rounds 2-3
- **Special handling**: Maintain cooperation even if cooperation_rate is low
- **Rationale**: Too little data to draw reliable conclusions; preserves possibility of coordinating with delayed-reciprocal strategies

### Last Round (t = r)
- **Action**: DEFECT
- **Rationale**: Standard backward induction applies; no future payoffs to influence. Cannot be exploited further. Maximizes individual payoff in final period.
- **Exception mitigation**: Early defection by opponents triggers Proportional Response starting at t = r-2 (rounds 2-4 buffer) to signal adjustment before endgame

### Tournament Across Multiple Opponents
- **Per-opponent tracking** (if tournament structure permits): Maintain separate cooperation_rate per opponent
- **If global tracking only**: Use global cooperation_rate as conservative estimate

---

## PSEUDOCODE

```
STRATEGY(game_history, round_number, n, r, k):
  
  if round_number == 1:
    return COOPERATE
  
  if round_number > 1 and round_number <= 3:
    return COOPERATE
  
  if round_number == r:  // Last round
    return DEFECT
  
  // Compute global cooperation rate from history
  total_cooperations = count_all_cooperations(game_history)
  cooperation_rate = total_cooperations / ((round_number - 1) × n)
  
  if cooperation_rate > 0.50:
    return COOPERATE
  
  else:  // cooperation_rate ≤ 0.50, apply proportional response
    opponent_cooperation = (total_cooperations / (round_number - 1)) / n
    rounds_remaining = r - round_number
    decay_factor = 1 - (rounds_remaining / r) × 0.2
    
    prob_cooperate = opponent_cooperation × decay_factor
    
    if RANDOM() < prob_cooperate:
      return COOPERATE
    else:
      return DEFECT
```

---

## PROSOCIAL ALIGNMENT

### How This Strategy is Prosocial:

1. **Generous opening**: Unconditional cooperation in round 1 signals good faith and enables mutually beneficial equilibria
2. **Cooperative grace period**: Rounds 2-3 buffer gives strategies time to synchronize before harsh judgment
3. **Proportional reciprocity, not punishment**: When facing defectors, we don't immediately flip to 100% defection; we match their cooperation level probabilistically
4. **Collective welfare maximization**: Sustained cooperation in high-cooperation environments generates maximum total payoff (k × n/n = k per person, vs. 1 for all-defect)
5. **Transparency through observability**: Every action is explainable through public game history; no hidden state
6. **Avoids exploitation spirals**: Probabilistic defection when others defect prevents being locked into mutual destruction while preserving relationship reset opportunities

### Why Robust:

- Pure defectors earn 1 per round; we eventually match them
- Pure cooperators earn k when we cooperate; we cooperate most of the time
- Mixed strategies are outcompeted by our adaptive threshold
- End-game defection is unavoidable in game theory, so we don't try; we minimize exposure with the decay factor

---

## PARAMETER SENSITIVITY

The strategy naturally adapts to parameters:
- **High k (strong multiplier)**: Cooperation_rate threshold benefits prosocial behavior even more; strategy leans cooperative
- **High n (many players)**: Individual impact shrinks; proportional response becomes more important to identify true cooperators
- **Low r (few rounds)**: Decay factor activates faster; earlier shift toward caution
'''

description_PROSOCIAL_22 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "Graduated Reciprocal Altruism with Decay" (GRAD)

## CORE PHILOSOPHY

This strategy balances prosocial cooperation with rational self-protection. It assumes most opponents are rational but may include both cooperative and defective types. The key insight: **build cooperation gradually while remaining sensitive to exploitation, and implement strategic generosity that makes cooperation attractive to others.**

---

## STRATEGY SPECIFICATION

### 1. DECISION RULES

**Cooperation Threshold Mechanism:**

For round t, cooperate if and only if:

```
cooperation_rate(t-1) ≥ threshold(t)
```

Where:
- `cooperation_rate(t-1)` = proportion of players who cooperated in round t-1
- `threshold(t)` = dynamic threshold that adapts to game progress

**Threshold Function:**

```
threshold(t) = base_threshold × (1 - decay_factor × (t / r))

where:
  base_threshold = (k - 1) / n  [Breakeven point for cooperation]
  decay_factor = 0.5             [Linear decay toward end-game]
```

**Intuition:** 
- Early rounds: Higher threshold (be cautious, require proof others will cooperate)
- Later rounds: Lower threshold (increase prosocial play as time runs out; defectors gain less from exploitation)
- The base threshold is the mathematical point where cooperation becomes individually rational if others cooperate

---

### 2. EDGE CASES & SPECIAL HANDLING

**Round 1 (Initialization):**
```
IF round == 1:
    COOPERATE
    Reason: Prosocial opening move; reveals that cooperation is possible
```

**Rounds 2 to r-2 (Adaptive Main Phase):**
```
Follow the cooperation threshold rule above
Compute cooperation_rate from all previous rounds
Update expectations about the population
```

**Round r-1 (Penultimate Round):**
```
IF cooperation_rate(r-2) ≥ threshold(r-1):
    COOPERATE
ELSE:
    DEFECT
Reason: Second-to-last chance to either strengthen cooperation
or punish defectors before endgame
```

**Round r (Final Round):**
```
IF cooperation_rate(r-1) ≥ threshold(r):
    COOPERATE
ELSE:
    DEFECT
Reason: Last-round defection is irrational if others are cooperating
(no future rounds to punish you). Only defect if defection is 
already dominant in the population.
```

---

## 3. PROSOCIAL ALIGNMENT

**Why This Is Prosocial:**

1. **Default Cooperation:** Starts cooperating unilaterally, signaling trustworthiness and creating a cooperative equilibrium opportunity.

2. **Conditional Reciprocity:** Responds to population cooperation rates rather than punishing individuals. This is more forgiving than tit-for-tat because:
   - It doesn't escalate conflict with single defectors
   - It rewards the *population trend*, encouraging others to shift toward cooperation
   - It avoids mutual punishment spirals

3. **Generosity Gradient:** As the game progresses, the strategy *lowers* the bar for cooperation. This creates strategic generosity:
   - In early rounds: "Prove cooperation is worthwhile"
   - In late rounds: "Let's finish together on good terms"
   - This incentivizes others to cooperate (they know late-round cooperation is easier to trigger)

4. **No Exploitation of Last Round:** Despite the temptation to defect in round r when others cooperate, the strategy respects the finality of the game by cooperating if the population trend supports it. This discourages others from planning last-round defections.

5. **Robustness to Heterogeneity:** Works against mixed populations:
   - Pure defectors: Strategy switches to defection once recognized
   - Reciprocators: Mutual cooperation emerges quickly
   - Conditional cooperators: Strategy adapts thresholds to meet them halfway
   - Random players: High averaging behavior smooths noise

---

## 4. PSEUDOCODE IMPLEMENTATION

```
State Variables:
  history[] = array of cooperation counts per round
  current_round = 0

Initialize:
  cooperation_count = 0

Each Round t:
  
  IF t == 1:
    action = COOPERATE
    cooperation_count += 1
  
  ELSE:
    // Calculate previous cooperation rate
    prev_cooperation_rate = history[t-1] / n
    
    // Calculate dynamic threshold
    base_threshold = (k - 1) / n
    decay_factor = 0.5
    threshold = base_threshold × (1 - decay_factor × (t / r))
    
    IF t == r:  // Final round special case
      IF prev_cooperation_rate ≥ threshold:
        action = COOPERATE
      ELSE:
        action = DEFECT
    
    ELSE:
      IF prev_cooperation_rate ≥ threshold:
        action = COOPERATE
      ELSE:
        action = DEFECT
  
  Record(action)

After Round t:
  Observe all other players' actions
  Update history[t] with count of cooperators
```

---

## 5. PARAMETER SENSITIVITY

The strategy automatically calibrates to:
- **Small n:** Threshold rises (each player's impact matters more)
- **Large n:** Threshold falls (cooperation is less individually costly)
- **k near 1:** Threshold stays high (cooperation barely pays off)
- **k near n:** Threshold falls low (cooperation highly rewarding)
- **Short r:** Decay factor accelerates cooperation recruitment
- **Long r:** Decay allows early caution, late cooperation

---

## SUMMARY

**GRAD** is a prosocial strategy that:
✓ Initiates cooperation unconditionally  
✓ Adapts rationally to opponent behavior  
✓ Avoids escalation spirals through population-level reasoning  
✓ Implements strategic generosity in late rounds  
✓ Remains robust across diverse opponent types  
✓ Mathematically calibrated to game parameters  

The strategy bets that in a diverse tournament, *making cooperation easy and attractive in late rounds will encourage enough reciprocal behavior to outperform pure defection*, while remaining protected against exploitation in early rounds.
'''

description_PROSOCIAL_23 = '''
# Prosocial Strategy: Adaptive Generosity with Earned Trust (AGET)

## Core Philosophy
This strategy balances prosocial intentions with rational self-protection. It assumes most players are conditionally cooperative and tries to establish mutually beneficial equilibria, while maintaining a credible deterrent against persistent defectors.

## Decision Rules

### 1. **First Round: Cooperate**
**Action:** Play C

**Rationale:** 
- Signal good faith and prosocial intent from the start
- Gather information about opponent tendencies
- In a genuinely cooperative group, this maximizes collective welfare
- If opponents exploit this, we adapt quickly

### 2. **Rounds 2 to r-1 (Mid-game): Adaptive Conditional Cooperation**

**Decision Rule:**
```
Let recent_cooperation_rate = (cooperators in last 2 rounds) / (2 × n - 2)
  [exclude own play; count others only]

Let my_recent_exploitation = 
  (times I played C while others' cooperation_rate < threshold) / 2

If recent_cooperation_rate ≥ 0.5:
    Play C (reciprocate cooperation trend)
    
Else if recent_cooperation_rate ≥ 0.25 AND my_recent_exploitation < 1:
    Play C (cautious optimism; others are trying)
    
Else if recent_cooperation_rate < 0.25:
    Play D (group is defecting; protect yourself)
    
Special case - Last 2 rounds before end:
    If cooperation has been established (rate > 0.5 in last 3):
        Play C (strengthen final cooperation)
    Else:
        Play D (minimize losses in final rounds)
```

**Rationale:**
- **Threshold at 0.5:** Reciprocate when majority cooperate (k < n guarantees this creates positive externalities)
- **Tracking exploitation:** Prevents being a sucker—if I cooperate but others defect, I shift strategy
- **Decay toward defection:** As cooperation drops below 25%, the rational move is self-protection
- **Last-round adjustment:** Prevents exploitation in final rounds while preserving mutual cooperation if established

### 3. **Last Round (Round r): Context-Dependent**

**Decision Rule:**
```
If total_cooperators_in_previous_round ≥ (n-1)/2:
    Play C (finalize cooperative equilibrium)
    
Else:
    Play D (final self-protection; no future rounds)
```

**Rationale:**
- If we've achieved majority cooperation, finishing with C reinforces the cooperative norm
- If defection is dominant, defecting in the final round minimizes losses
- No incentive for cooperation in the final round unless cooperation is already stable

## Edge Cases & Special Situations

### **Unanimous Defection Scenario**
If all other players defect for 3+ consecutive rounds:
- Switch permanently to D
- Minimize losses by matching observed behavior
- Signal: "I tried; you chose otherwise"

### **Oscillating/Unpredictable Opponents**
If opponents alternate randomly between C and D:
- Weight recent rounds more heavily (last 2 > last 3-4)
- Play C if recent_cooperation_rate is close to threshold (≥0.4)
- Rationale: Random cooperators still contribute to public good; partial reciprocation is profitable for both

### **Mixed Groups (Some cooperators, some defectors)**
- The decision rule naturally accommodates this
- Cooperation threshold of 0.5 means we cooperate if >50% of others cooperate
- This is prosocial because it rewards cooperators and creates a positive subgroup equilibrium

### **Very Small Groups (n=2)**
- Adjust threshold to 0.4 (since one other player's action is more volatile)
- Increased emphasis on reciprocal cooperation for stability

## Prosocial Alignment

**Why this is prosocial:**

1. **Leads with cooperation:** Round 1 C establishes good faith
2. **Rewards reciprocity:** Cooperation increases when others cooperate, reinforcing positive norms
3. **Doesn't exploit:** Actively tracks when I'm being exploited and stops cooperating
4. **Stabilizes equilibria:** By maintaining >0.5 threshold, enables group welfare maximization when k > 1
5. **Punishes persistent defection:** Clear deterrent prevents groups from collapsing into all-D
6. **Robust to manipulation:** Doesn't assume opponent strategies; learns from observed behavior

**Long-term prosocial outcome:**
- Against cooperators: Achieves mutual cooperation (payoff = 2k/n per round, approaching max for large groups)
- Against defectors: Minimizes collective losses by defecting (payoff = 1)
- Mixed groups: Incentivizes cooperation through reciprocation (payoff oscillates toward cooperation)

## Implementation Pseudocode

```
strategy AGET(game_history, n, r, current_round):
    if current_round == 1:
        return COOPERATE
    
    // Calculate recent cooperation rate (last 2 rounds, excluding self)
    recent_actions = game_history[-2:]
    recent_cooperation_rate = count_others_cooperating(recent_actions) / 
                              (2 × (n - 1))
    
    // Track exploitation
    my_recent_exploitation = count(I played C AND 
                                   others_coop_rate < 0.5 in last 2)
    
    // Mid-game logic
    if current_round >= r - 1:  // Last 2 rounds
        if recent_cooperation_rate > 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    // Standard mid-game
    if recent_cooperation_rate >= 0.5:
        return COOPERATE
    elif recent_cooperation_rate >= 0.25 AND my_recent_exploitation < 1:
        return COOPERATE
    else:
        return DEFECT
```

This strategy is **adaptive** (learns from history), **robust** (handles diverse opponents), and **prosocial** (explicitly tries to create cooperative equilibria while protecting against exploitation).
'''

description_PROSOCIAL_24 = '''
# Prosocial Strategy: Adaptive Reciprocal Cooperation with Robustness

## Core Philosophy
This strategy balances prosocial cooperation with rational self-protection. It aims to establish and maintain cooperative equilibria while remaining resilient to exploitation. The key insight is that cooperation becomes increasingly valuable as the game progresses, so we should invest in cooperation conditionally, rewarding cooperative communities and protecting against systematic defectors.

## Decision Rules

### PRIMARY RULE: Conditional Cooperation with Decay
On round t, cooperate if and only if:
- **Condition 1 (Early investment):** t ≤ 2, OR
- **Condition 2 (Reciprocity threshold):** Recent cooperation rate ≥ threshold(t), OR  
- **Condition 3 (Late-game bonus):** We're in the final rounds AND cooperation has been above average

### Detailed Decision Logic

```
ROUND 1 AND 2:
  Action = COOPERATE
  Rationale: Establish cooperative intent, gather information about others
             These rounds have minimal cost relative to learning value

ROUND 3 onwards:
  observed_cooperation_rate = (total cooperators in last 2 rounds) / (2 × n)
  
  IF round ≤ r/2:
    threshold = 0.40  // Moderate threshold in early-middle game
  ELSE IF round ≤ 0.8 × r:
    threshold = 0.45  // Slightly raise bar in middle game
  ELSE:
    threshold = 0.35  // LOWER threshold in final rounds
                      // Maximize prosocial value when impact is concentrated
  
  IF observed_cooperation_rate ≥ threshold:
    Action = COOPERATE
  ELSE:
    Action = DEFECT

FINAL ROUND (round = r):
  // Special case: Defect if community hasn't justified cooperation
  IF observed_cooperation_rate < 0.30:
    Action = DEFECT
  ELSE:
    Action = COOPERATE  // Even modest cooperation warrants final cooperation

MOVING AVERAGE:
  Weight last 2 rounds at 0.6, round before that at 0.4
  This prevents single-round noise from derailing cooperation
```

## Edge Cases & Refinements

### First Round
**Action: COOPERATE unconditionally**
- Rationale: No history exists; cooperation here signals prosocial intent and generates no information deficit
- Cost is minimal; benefit is maximum trust-building

### Last Round
**Boosted tolerance for cooperation**
- Lower the threshold from 0.45 to 0.35
- Rationale: This is the final opportunity to contribute to collective welfare; even marginally cooperative groups deserve cooperation
- The final round is zero-sum only if others defect—if there's any reasonable cooperation, we amplify it

### Extremely Defective Groups (cooperation rate < 0.20)
**Automatic defection** regardless of round number
- Rationale: When >80% defect, cooperation creates a public good that defectors exploit
- This is not reciprocal failure—this is rational non-cooperation against a defection cascade

### Isolated Defection
**Single defectors don't trigger punishment**
- If one player defects in an otherwise cooperative round, we maintain cooperation
- Rationale: That defector already gained their private payoff; defecting back doesn't punish them, it just reduces collective welfare
- Only systematic, community-wide defection justifies withdrawal

## Prosocial Alignment

This strategy is prosocial in three ways:

1. **Cooperation as default in uncertainty:** Rounds 1-2 commit cooperatively, establishing that we're not exploitation-seeking. We assume good faith.

2. **Reciprocity, not punishment:** We match communities' cooperation levels, not punish individual defectors. When >45% cooperate, we reinforce that behavior collectively.

3. **Endgame generosity:** We *lower* standards in final rounds because that's when cooperation matters most. If a community is cooperating at 35%, we still join in the last round, maximizing total welfare generation.

## Robustness Analysis

| Opponent Archetype | Response |
|---|---|
| **Always Cooperate** | Cooperate throughout; mutual welfare maximization (payoff ≈ 2 if k=2) |
| **Always Defect** | Defect after round 2; minimize exploitation |
| **Tit-for-Tat** | Cooperate early, match reciprocity threshold; strong mutual cooperation likely |
| **Random/Noisy** | Moving average smooths noise; threshold prevents overreaction to variance |
| **Strategically-timed defection** | Early rounds ignored (we cooperate anyway); late defection punished via defection |
| **Mixed majority** | Threshold calibration ensures we cooperate with >40% cooperators; stay above break-even |

## Implementation Pseudocode

```python
def decide_action(round_num, r, n, history):
    # history[(t, i)] = action of player i in round t
    
    if round_num <= 2:
        return COOPERATE
    
    # Calculate recent cooperation rate
    recent_rounds = history[max(1, round_num - 2):round_num]
    cooperators_per_round = [sum(1 for i in range(n) if recent_rounds[t][i] == C) 
                              for t in range(len(recent_rounds))]
    observed_coop_rate = sum(cooperators_per_round) / (len(recent_rounds) * n)
    
    # Determine threshold
    if round_num <= r / 2:
        threshold = 0.40
    elif round_num <= 0.8 * r:
        threshold = 0.45
    else:
        threshold = 0.35
    
    # Final round special case
    if round_num == r:
        return COOPERATE if observed_coop_rate >= 0.30 else DEFECT
    
    # Defect against systematic defectors
    if observed_coop_rate < 0.20:
        return DEFECT
    
    # Standard reciprocity
    return COOPERATE if observed_coop_rate >= threshold else DEFECT
```

## Why This Works

- **Self-interested players** see that cooperation yields 2 payoff vs. 1; we make cooperation attractive
- **Exploiters** find no one cooperates after round 2 if communities are defective
- **Cooperators** find a willing ally who matches community norms
- **The tournament** benefits because this strategy stabilizes cooperative equilibria wherever possible, generating higher aggregate welfare
'''

description_PROSOCIAL_25 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial intent with strategic robustness by:
1. **Starting optimistic** (high cooperation) to signal trustworthiness
2. **Adapting dynamically** to actual group behavior
3. **Maintaining contribution** even under defection pressure, but scaling it intelligently
4. **Optimizing for mutual benefit** rather than individual exploitation

The key insight: In public goods games, sustained moderate cooperation often outperforms both pure defection and naive full cooperation, especially against diverse opponents.

---

## Decision Rule: Adaptive Reciprocal Contribution

### Initial Assessment Phase (Rounds 1 through min(3, r))

**Round 1:** 
- **COOPERATE** unconditionally
- Rationale: Establish prosocial intent; gather information about others

**Rounds 2-3:**
- Calculate **group cooperation rate** from round history: `coop_rate = total_cooperators / (n × rounds_elapsed)`
- **IF** `coop_rate ≥ 0.5`: COOPERATE
- **ELSE**: Move to Adaptive Phase

### Adaptive Phase (Rounds 4 through r-1)

Calculate a **cooperation likelihood estimate** based on recent history:

```
recent_rounds = last 2 rounds of history (or all history if < 2 rounds exist)
recent_coop_rate = cooperators_in_recent_rounds / (n × recent_rounds_count)

target_cooperation_level = 0.5 + (0.5 × recent_coop_rate)
```

This creates a **mirroring effect with damping**:
- If others cooperate heavily (rate = 1.0): target = 1.0 → COOPERATE
- If others cooperate moderately (rate = 0.5): target = 0.75 → COOPERATE
- If others defect heavily (rate = 0.0): target = 0.5 → Stochastic choice

**Decision Logic:**
- Generate a random number `R ∈ [0, 1]`
- **IF** `R < target_cooperation_level`: COOPERATE
- **ELSE**: DEFECT

**Rationale:** 
- Maintains some cooperation even against defectors (prosocial floor)
- Scales cooperation with group behavior (adaptive/reciprocal)
- Stochasticity prevents predictable exploitation
- Avoids "sucker's payoff" by reducing contribution when defection dominates

### Endgame Phase (Last round r)

This is strategically critical in repeated games:

```
if round == r:
    if (cumulative_coop_rate_all_previous_rounds ≥ 0.6):
        COOPERATE  // Reward sustained cooperation
    else:
        DEFECT     // Defect against defector-dominated groups
```

**Rationale:** 
- If the group has been prosocial, reward it with one final contribution
- If the group has been selfish, don't leave value on the table
- This avoids the "backward induction" trap of always defecting in final rounds

---

## Edge Cases & Special Handling

### When n = 2 (Bilateral Game)
- Increase cooperation threshold slightly: Use 0.6 instead of 0.5 in initial assessment
- Rationale: In dyads, mutual defection is particularly costly; the signal matters more

### When r = 2 (Minimal Repetition)
- Round 1: COOPERATE
- Round 2: Use endgame logic (check if cooperator ≥ 0.5 in round 1, then COOPERATE, else DEFECT)
- Rationale: Very limited history; initial play is most informative

### When r is Large (r > 10)
- Extend assessment phase to first 4 rounds
- Use longer window for recent_rounds: min(4, r/3) instead of 2
- Rationale: More history allows refined estimates; extrapolate group type more confidently

### Against Perfect Defectors
- The strategy will stabilize at approximately 50% personal contribution
- Expected payoff: ~0.5 + (k/n) × 0.5 = ~0.5(1 + k/n) per round
- This is better than pure defection (payoff = 1) only if k/n > 1, which is guaranteed by 1 < k < n
- The strategy is "protected" and never exploited worse than mutual defection

---

## Prosocial Alignment

1. **Optimism Bias:** Starts with cooperation, signaling good faith
2. **Conditional Reciprocity:** Rewards cooperation, gentle with defection (not retaliatory)
3. **Sustainability:** Maintains a 50% minimum contribution floor, ensuring positive externalities even in adversarial environments
4. **Group Welfare:** Target cooperation level is *always* calculated to maximize shared payoff, not personal payoff
5. **Fairness:** Stochasticity ensures no single opponent can perfect-predict and systematize exploitation

---

## Pseudocode Implementation

```
function decide(game_params, history):
    n = game_params.n
    r = game_params.r
    k = game_params.k
    round_number = len(history) + 1
    
    // Initial phase
    if round_number == 1:
        return COOPERATE
    
    if round_number <= 3 and round_number < r:
        coop_rate = count_cooperators(history) / (n * len(history))
        if coop_rate >= 0.5:
            return COOPERATE
        else:
            go_to ADAPTIVE_PHASE
    
    // Endgame
    if round_number == r:
        cumulative_coop = count_cooperators(history) / (n * len(history))
        if cumulative_coop >= 0.6:
            return COOPERATE
        else:
            return DEFECT
    
    // Adaptive phase
    ADAPTIVE_PHASE:
    recent_rounds = min(2, len(history))
    recent_coop_rate = count_cooperators(last_X_rounds(history, recent_rounds)) 
                       / (n * recent_rounds)
    target_level = 0.5 + (0.5 * recent_coop_rate)
    
    if random() < target_level:
        return COOPERATE
    else:
        return DEFECT
```

---

## Why This Works

| Opponent Type | Our Behavior | Our Payoff | Outcome |
|---|---|---|---|
| Pure Cooperators | Cooperate (≈100%) | 2 (or k, generically) | Mutual welfare |
| Reciprocals | Adaptive match | ~1.5 (moderate-high) | Coevolution |
| Defectors | Defect 50%, then flip | ~1.25 | Avoid sucker payoff |
| Mixed | Adaptive tuning | 1.3-1.7 | Robust baseline |

**Tournament Resilience:** 
- Against majority defection: earns ~1.25 (better than pure defection at 1.0)
- Against majority cooperation: earns ~1.8 (near full cooperation at 2.0)
- No catastrophic vulnerability to any single strategy type
'''

description_PROSOCIAL_26 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "Conditional Reciprocal Contribution"

## CORE PHILOSOPHY
This strategy balances prosocial cooperation with robust self-protection against exploitation. It aims to build and maintain cooperation while remaining sensitive to defection patterns, creating incentives for others to cooperate without sacrificing excessively to free-riders.

## DECISION RULES

### ROUND 1 (Opening Move)
**Action: COOPERATE**

*Rationale:* Start with goodwill. This establishes a cooperative baseline and signals prosocial intent. In a game where mutual cooperation benefits everyone, initiating cooperation is both strategically sound and value-aligned.

### ROUNDS 2 through (r-1) (Adaptive Phase)
**Decision Rule - Reciprocal Threshold Strategy:**

```
Calculate cooperation_rate = (total cooperators in previous round) / n

IF cooperation_rate ≥ threshold_high (e.g., 0.50):
    ACTION: COOPERATE
    Rationale: Sufficient cooperation exists; contribute to the public good
    
ELSE IF cooperation_rate < threshold_low (e.g., 0.25):
    ACTION: DEFECT
    Rationale: Cooperation has collapsed; avoid exploitation
    
ELSE IF threshold_low ≤ cooperation_rate < threshold_high:
    IF (I cooperated last round) AND (I received below-average payoff):
        ACTION: DEFECT (conditional punishment)
    ELSE:
        ACTION: COOPERATE (tentative optimism)
    Rationale: Gradient response in intermediate zone; test cooperation while monitoring payoff fairness
```

**Specific Thresholds (for general n):**
- **threshold_high** = 0.50 (majority cooperation signals viable mutual cooperation)
- **threshold_low** = 0.25 (below this, cooperation becomes significantly exploitable)

**Payoff Fairness Check:**
```
average_payoff_this_round = (my payoff) / 1
community_avg = (sum of all observed payoffs this round) / n

IF (my payoff < community_avg - ε) where ε = 0.15:
    Classify as "exploited" (being taken advantage of)
```

### ROUND r (Final Round)
**Action: DEFECT**

*Rationale:* In the final round, there is no future to influence. No opportunity for reciprocal adjustment. Cooperating provides no strategic benefit and only reduces final payoff. However, see **EXCEPTION** below.

**EXCEPTION - Defect Gracefully:**
```
IF (average cooperation_rate across ALL previous rounds > 0.60):
    ACTION: COOPERATE
    Rationale: Persistent cooperation deserves reciprocation even at the end.
              Contributes to prosocial reputation/signal.
```

## EDGE CASES & SPECIAL HANDLING

### **Observation Constraints**
```
IF incomplete information about previous round:
    Use last_known_cooperation_rate
    If no prior data: Default to COOPERATE
```

### **Extreme Parameters**
```
IF k < 1.1 (public good nearly worthless):
    Shift strategy toward defection; cooperation yields minimal benefit
    
IF k > n - 0.5 (public good extremely valuable):
    Increase threshold_high to 0.40
    Rationale: Cooperation is highly beneficial; be more willing to contribute
    
IF r = 2 (only two rounds):
    Round 1: COOPERATE (as specified)
    Round 2: DEFECT (final round rule)
    Note: Limited opportunity for reciprocal learning
```

### **Tie-Breaking (Multi-player Indifference)**
```
When uncertain between COOPERATE and DEFECT:
    Choose COOPERATE
    Rationale: Breaks ties prosocially; cooperation is the Pareto-improving outcome
```

## PROSOCIAL ALIGNMENT

**How this strategy is prosocial:**

1. **Initiates cooperation** - Round 1 assumes good faith, encouraging mutual benefit
2. **Rewards cooperation** - Cooperates when others do, creating positive feedback loops
3. **Punishes defection gracefully** - Reduces cooperation in low-cooperation environments, but doesn't escalate to pure defection
4. **Fairness-aware** - Accounts for whether *you're* being exploited, not just whether defection would increase your payoff
5. **Avoids free-riding** - Will defect if others don't contribute, preventing systematic exploitation
6. **Long-term cooperation focus** - Maintains medium-round flexibility to encourage others to rejoin cooperation
7. **Respects prosocial history** - Even in the final round, reciprocates genuine cooperation

## PSEUDOCODE IMPLEMENTATION

```
FUNCTION ChooseAction(round, n, r, k, history):
    
    IF round == 1:
        RETURN COOPERATE
    
    IF round == r:
        avg_coop_rate = AverageCooperationRate(history)
        IF avg_coop_rate > 0.60:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    // Rounds 2 to r-1
    prev_coop_rate = CooperationRate(history[round-1])
    my_last_action = history[round-1][self]
    my_payoff_last = CalculatePayoff(history[round-1])
    avg_payoff_last = AveragePayoff(history[round-1])
    
    IF prev_coop_rate >= 0.50:
        RETURN COOPERATE
    
    ELSE IF prev_coop_rate < 0.25:
        RETURN DEFECT
    
    ELSE:  // 0.25 ≤ prev_coop_rate < 0.50
        IF (my_last_action == COOPERATE) AND (my_payoff_last < avg_payoff_last - 0.15):
            RETURN DEFECT
        ELSE:
            RETURN COOPERATE
    
    END FUNCTION
```

## ROBUSTNESS PROPERTIES

This strategy handles:
- **Unconditional defectors** - Adapts to defect when cooperation becomes rare
- **Tit-for-tat players** - Maintains mutual cooperation
- **Random players** - Uses cooperation_rate averaging to smooth noise
- **Conditional cooperators** - Recognizes and reciprocates their patterns
- **Exploiters** - Detects below-average payoffs and withdraws support
- **Varying n and k** - Thresholds remain valid across parameter ranges
'''

description_PROSOCIAL_27 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with rational self-protection. It recognizes that sustainable cooperation requires:
1. **Consistent cooperation** to establish trust and mutual benefit
2. **Intelligent defection detection** to avoid exploitation
3. **Graceful recovery mechanisms** when defection occurs
4. **Context-awareness** about game parameters and remaining rounds

---

## DECISION RULES

### Rule 1: Initial Cooperation (Round 1)
**Action: COOPERATE**

**Rationale:** 
- In round 1, we have no history. Defecting immediately contradicts prosocial intent.
- Cooperation signals willingness to achieve the mutual payoff of `(k/n) × n = k > 1`.
- This establishes a cooperative equilibrium as a baseline for negotiation.

---

### Rule 2: Sustained Cooperation Phase (Rounds 2 to r-2)
**Condition & Action:**

Calculate the **cooperation rate** from the previous round:
- `coop_rate_prev = total_cooperators_prev / n`

**IF** `coop_rate_prev ≥ threshold_cooperators`:
- **Action: COOPERATE**
- **Threshold calculation:** `threshold_cooperators = max(0.5, k/(n+1))`
  - This threshold adapts to group size and multiplication factor
  - Requires at least 50% cooperation OR the mathematical break-even point

**ELSE** (cooperation rate below threshold):
- **Action: DEFECT** (temporary punishment)
- **Reasoning:** If cooperation falls below sustainable levels, defection protects against exploitation while signaling that current strategy isn't working

---

### Rule 3: Recovery & Re-engagement (Round r-1, second-to-last)
**Condition & Action:**

This round is critical—it provides one last signal before the final round.

**IF** `current_cooperation_rate ≥ threshold_cooperators`:
- **Action: COOPERATE** (maintain cooperation)

**ELSE IF** `coop_rate_prev < threshold_cooperators BUT coop_rate_current shows improvement`:
- **Action: COOPERATE** (give one more chance if trend is positive)
- **Reasoning:** A recovering group deserves reinvestment in cooperation

**ELSE**:
- **Action: DEFECT** (defect-heavy groups won't recover)

---

### Rule 4: Final Round (Round r)
**Action: COOPERATE**

**Rationale:**
- The final round has no shadow of the future
- Defecting in the final round is exploitative and contradicts prosocial values
- Even if others defect, cooperating maximizes total welfare
- This demonstrates commitment to prosocial outcomes beyond rational self-interest

---

## EDGE CASES & SPECIAL HANDLING

### Case: n = 2 (Binary Interaction)
- Threshold becomes especially strict: `threshold_cooperators = max(0.5, k/3)`
- With only two players, defection by one player is immediately visible
- More aggressive recovery: If opponent defects, defect once, then return to cooperation (Tit-for-Tat tendency)

### Case: Rounds 1-3 (Early Game)
- Extra patience for the first 3 rounds
- If the group starts with all-defection, we defect but don't lose hope
- Minimum 2 consecutive rounds of low cooperation needed to sustain defection

### Case: k Close to n (High Multiplication)
- When `k > n-1`, cooperation becomes dominant strategy
- Increase cooperation likelihood slightly (interpret threshold more generously)
- Example: If k=4.5 and n=5, mutual cooperation is always better than any mixed outcome

### Case: k Close to 1 (Low Multiplication)
- When `k ≈ 1`, public good is weak; defection pressure is high
- Maintain strategy but be quicker to punish (fewer rounds of patience)
- Ensure we don't lose money by over-cooperating

---

## PSEUDOCODE

```
function decide(round, n, k, r, history):
    
    if round == 1:
        return COOPERATE
    
    // Calculate previous round's cooperation rate
    prev_cooperators = count_cooperators(history[round-1])
    coop_rate_prev = prev_cooperators / n
    
    // Calculate threshold
    threshold = max(0.5, k / (n + 1))
    
    // Determine current trend (if round >= 3)
    if round >= 3:
        cooperators_round_2 = count_cooperators(history[round-2])
        coop_rate_2rounds_ago = cooperators_round_2 / n
        trend = coop_rate_prev - coop_rate_2rounds_ago
    else:
        trend = 0
    
    // Last round special case
    if round == r:
        return COOPERATE
    
    // Second-to-last round (r-1)
    if round == r - 1:
        if coop_rate_prev >= threshold:
            return COOPERATE
        else if trend > 0:  // improving even if below threshold
            return COOPERATE
        else:
            return DEFECT
    
    // Sustained cooperation phase (rounds 2 to r-2)
    if coop_rate_prev >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## WHY THIS STRATEGY IS PROSOCIAL

1. **Leads with cooperation:** We assume good faith in round 1 and whenever conditions permit
2. **Maximizes mutual payoff:** Cooperation when `k > 1` creates a payoff surplus for all
3. **Fair punishment:** Defection only occurs when the group isn't sustaining cooperation
4. **Forgiveness:** We re-engage if cooperation rate recovers
5. **Final round integrity:** We cooperate in round r regardless, honoring prosocial commitment
6. **Adaptive:** Respects heterogeneous player populations by using rates rather than assuming specific strategies
7. **Transparent logic:** Our decision rule is interpretable—others can learn that defection triggers response but recovery is possible

---

## ROBUSTNESS

- **Against all-defectors:** We defect after round 1, minimizing losses
- **Against free-riders:** We punish, then offer recovery opportunities
- **Against cooperators:** We maintain mutual benefit
- **Against mixed strategies:** We adapt to actual cooperation rates, not predicted ones
- **Against newcomers:** Each round is evaluated fresh based on actual history

This strategy doesn't assume others are prosocial, but it *creates incentives* for prosocial outcomes through reciprocal engagement.
'''

description_PROSOCIAL_28 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial intent with rational self-protection. It aims to build cooperative momentum while remaining robust against exploitation. The key insight: sustained cooperation benefits everyone, but unilateral cooperation enables free-riding—so we reward cooperation and gently punish defection while remaining forgiving.

## Decision Rules

### Primary Rule: Adaptive Contribution Based on Cooperation Rate

**Define: cooperation_rate** = (number of cooperators in previous round) / n

**For round t:**

```
IF t == 1:
    COOPERATE
    // Prosocial: offer initial cooperation as goodwill

ELSE IF t == r (final round):
    IF cooperation_rate(t-1) ≥ threshold_final:
        COOPERATE
    ELSE:
        DEFECT
    // Note: Even in final round, cooperate if others cooperated
    // This signals trustworthiness even when no future reciprocity possible

ELSE (intermediate rounds):
    IF cooperation_rate(t-1) ≥ dynamic_threshold(t):
        COOPERATE
    ELSE:
        DEFECT
```

### Dynamic Threshold Calculation

The threshold decreases gradually over time, becoming more forgiving as the game progresses:

```
dynamic_threshold(t) = base_threshold - (decay_rate × progress)

where:
  base_threshold = 0.5
  decay_rate = 0.05
  progress = (t - 1) / r
  
resulting in:
  threshold ranges from 0.5 (early rounds) to ~0.45 (late rounds)
```

**Rationale:** 
- Early rounds maintain reasonable standards (need 50%+ cooperation to continue)
- Later rounds become more forgiving, recognizing that low cooperation might be entrenched
- We avoid the "zero cooperation spiral" by not demanding perfection

### Special Case: Recovery Mechanism

```
IF cooperation_rate(t-1) < 0.3 AND cooperation_rate(t-2) > 0.3:
    // Sudden drop detected - possible temporary shock
    IF random() < 0.4:  // 40% chance to give benefit of doubt
        COOPERATE
    ELSE:
        DEFECT
ELSE:
    // Apply primary rule
```

**Rationale:** Allows recovery from temporary defection waves without cascading into mutual defection.

---

## Edge Cases

### Round 1 (First Round)
- **Action:** COOPERATE unconditionally
- **Rationale:** Prosocial signaling; establishes that cooperation is possible and initiate reciprocal cycles

### Round r (Final Round)
- **Action:** Conditional on previous cooperation_rate ≥ 0.5
- **Rationale:** Maintains integrity even when shadow of future is gone. However, don't reward defection even in final round—this breaks the perverse incentive to defect at the end

### Very Small Groups (n = 2)
- Adjust threshold slightly higher: base_threshold = 0.6
- Rationale: In dyads, one defection = 50% defection rate; we need stronger standards to avoid mutual defection

### Very Large Groups (n > 10)
- Adjust threshold slightly lower: base_threshold = 0.45
- Rationale: In large groups, free-riding is individually rational; be more forgiving of imperfect cooperation

---

## Pseudocode Summary

```
INITIALIZE:
  cooperation_threshold = 0.5
  decay_rate = 0.05
  
FOR each round t = 1 to r:
    
    IF t == 1:
        action[i] = COOPERATE
        
    ELSE:
        // Calculate previous round's cooperation rate
        cooperators_last_round = count(action[j] == COOPERATE for all j in previous round)
        coop_rate = cooperators_last_round / n
        
        // Adjust threshold based on progress
        current_threshold = 0.5 - (0.05 × (t-1)/r)
        
        // Check recovery condition
        IF t ≥ 3 AND coop_rate < 0.3 AND coop_prev_prev > 0.3:
            IF random() < 0.4:
                action[i] = COOPERATE
            ELSE:
                action[i] = DEFECT
        ELSE:
            // Standard rule
            IF coop_rate ≥ current_threshold:
                action[i] = COOPERATE
            ELSE:
                action[i] = DEFECT
                
    END IF
    
    // Calculate payoff and observe others' actions
    observe_round_outcomes()
    
END FOR
```

---

## Why This Strategy Is Prosocial & Robust

### Prosocial Elements:
1. **Unconditional initial cooperation** — extends trust first
2. **Forgiving thresholds** — doesn't require perfection (0.5, not 1.0)
3. **Decreasing demands** — becomes easier to cooperate as game progresses
4. **Recovery mechanism** — allows bounce-back from coordination failures
5. **Final round integrity** — doesn't exploit the end-game to defect

### Robustness Elements:
1. **Threshold prevents exploitation** — won't sustain cooperation against systematic defectors
2. **Adaptive decay** — handles various game lengths (r ranging from 2 to 100+)
3. **Empirically-grounded** — based on n and k parameters, not rigid patterns
4. **No assumption of reciprocity** — works even if opponents are random or adversarial
5. **History-dependent but not memory-intensive** — only needs last 2 rounds (lightweight)

### Against Various Opponents:
- **Cooperators:** Mutual cooperation cycle emerges → high payoffs
- **Defectors:** Quickly defects to protect endowment → reasonable safety payoff
- **Tit-for-Tat:** Establishes cooperation, moves in sync
- **Random players:** Gradual threshold decay prevents lock-in to defection
- **Mixed strategies:** Forgiving threshold creates space for mixed play to stabilize

---

This strategy prioritizes **sustainable cooperation** while maintaining a **rational defense** against exploitation—the essence of prosocial game theory.
'''

description_PROSOCIAL_29 = '''
# Prosocial Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy balances prosocial cooperation with intelligent defection-resistance. The key insight is that **sustainable cooperation requires demonstrating both willingness to contribute AND ability to punish free-riding**. We cooperate generously but adaptively reduce contributions when we detect systematic exploitation.

---

## Strategy Specification

### 1. DECISION RULES

**Primary Decision Rule: Reciprocal Threshold Cooperation**

```
For round t:
  1. Calculate the "cooperation ratio" from previous rounds:
     coop_ratio = (total cooperators across all previous rounds) / 
                  (n × number of previous rounds)
  
  2. Set an adaptive cooperation threshold:
     threshold = k/n (the breakeven point where cooperation equals defection payoff)
     
  3. Estimate opponent cooperation likelihood:
     opponent_coop_prob = coop_ratio × (1 - decay_factor)
     where decay_factor = min(0.15, 1/r) [recent rounds weighted more heavily]
  
  4. Calculate expected payoff from cooperation:
     expected_payoff_C = 0 + (k/n) × (1 + (n-1) × opponent_coop_prob)
     
  5. COOPERATE if: expected_payoff_C ≥ threshold
     DEFECT otherwise
```

**In Plain Language:**
- Track how often others cooperate
- Estimate what percentage will cooperate next round (with recent history weighted more)
- Cooperate if the expected shared benefits from contributing exceed the breakeven point
- Defect strategically when others aren't reciprocating sufficiently

---

### 2. EDGE CASES & SPECIAL ROUNDS

**Round 1 (First Round):**
```
Action: COOPERATE (unconditional)

Rationale: 
- No history exists; assume good faith
- Signals prosocial intent to potential cooperators
- Costs only 1 point; information value is high
- Establishes baseline for reciprocal patterns
```

**Final Round (Round r):**
```
Let rounds_remaining = 1

If coop_ratio > threshold - 0.1:
    Action: COOPERATE
Else:
    Action: DEFECT
    
Rationale:
- Small window for reputation-building doesn't matter
- But if others have been cooperative, reciprocate to end positively
- If others have been exploitative, no future payoff from cooperation
```

**Rounds 2 through r-1:**
```
Apply PRIMARY DECISION RULE (reciprocal threshold cooperation)

Special exception - "Exploitation Detection":
If in any round:
    - We cooperated (c_i = 1) AND
    - Fewer than (k/n × n) = k players cooperated (below threshold)
    
Then reduce cooperation_bias by 0.05 for next calculation
(This acknowledges we were exploited and slightly distrusts future cooperation)
```

---

### 3. PROSOCIAL ALIGNMENT

This strategy is prosocial in four ways:

**A. Cooperation-Bias in Uncertainty**
```
When expected payoff is WITHIN 0.1 of breakeven:
    → COOPERATE (benefit of doubt to others)
When expected payoff is CLEARLY BELOW breakeven:
    → DEFECT (protect against systematic exploitation)
```
This means we cooperate whenever there's reasonable doubt about opponent intentions, defaulting prosocial.

**B. Reciprocal Rather Than Retaliatory**
```
We do NOT:
- Permanently punish after one defection
- Coordinate multi-round punishment cascades
- Play tit-for-tat (which escalates cycles)

We DO:
- Gradually adjust expectations based on patterns
- Give cooperators multiple chances
- Reset positively if cooperation rate improves
```

**C. Maximize Mutual Benefit**
```
Key insight: 
If k > 1 (which is required), then achieving high mutual cooperation 
produces higher total welfare than mutual defection.

Our strategy actively seeks the mutual cooperation equilibrium 
when others show reciprocal tendencies.
```

**D. Transparent Incentive Structure**
```
Our behavior is based on publicly observable history, making it 
predictable and trustworthy:
- Others can observe our cooperation pattern
- Others can calculate our likely next move
- This transparency enables cooperation cascades
```

---

## Pseudocode

```python
def ARC_strategy(game_history, round_number, n, k, r):
    
    # Edge case: first round
    if round_number == 1:
        return COOPERATE
    
    # Calculate cooperation statistics
    all_actions = flatten(game_history)  # all previous actions by all players
    total_cooperations = count(all_actions == COOPERATE)
    total_possible = n * (round_number - 1)
    coop_ratio = total_cooperations / total_possible
    
    # Decay factor weights recent rounds more heavily
    decay_factor = min(0.15, 1/r)
    
    # Estimate opponent cooperation probability
    opponent_coop_prob = coop_ratio * (1 - decay_factor)
    
    # Threshold: expected return equals defection payoff
    breakeven_threshold = k / n
    
    # Expected payoff if we cooperate
    expected_public_benefit = (k / n) * (1 + (n - 1) * opponent_coop_prob)
    expected_payoff_cooperate = expected_public_benefit
    
    # Decision with benefit-of-doubt margin
    if expected_payoff_cooperate >= (breakeven_threshold - 0.1):
        
        # Special handling for final round
        if round_number == r:
            if coop_ratio > (breakeven_threshold - 0.1):
                return COOPERATE
            else:
                return DEFECT
        else:
            return COOPERATE
    else:
        return DEFECT
```

---

## Why This Strategy Succeeds

| Opponent Type | Our Response | Outcome |
|---|---|---|
| Cooperators | Cooperate with them | Mutual high payoff ✓ |
| Mixed population | Cooperate if threshold met | Adapt to equilibrium ✓ |
| Defectors | Detect pattern, defect | Minimize exploitation ✓ |
| Probabilistic players | Track ratio, respond proportionally | Robust adaptation ✓ |
| Strategic players | Transparent response triggers reciprocation | Enables cooperation ✓ |

The strategy is **robust** because it doesn't assume opponent type—it discovers it through observation and adapts gracefully.
'''

description_PROSOCIAL_30 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARCS)

## Core Philosophy
This strategy balances prosocial cooperation with strategic self-protection, recognizing that sustainable collective benefit requires both trust-building and exploitation-resistance. The goal is to maximize total welfare while maintaining individual viability against diverse opponents.

## Decision Rules

### Primary Decision Logic

```
FOR each round t in 1 to r:
    IF t == 1:
        ACTION = COOPERATE
    ELSE:
        cooperation_rate = (count of cooperators in round t-1) / n
        
        IF cooperation_rate >= threshold(t):
            ACTION = COOPERATE
        ELSE:
            ACTION = DEFECT
```

### Threshold Function (Adaptive to Round)

```
threshold(t) = max(0.4, min(0.9, (r - t) / r))
```

**Rationale:**
- Early rounds (low t): Higher threshold (~0.9) - require near-universal cooperation to reciprocate
- Middle rounds: Declining threshold - gradually become less demanding as information accumulates
- Late rounds (high t): Lower threshold (~0.4) - become more tolerant to encourage final-round cooperation
- The bounds [0.4, 0.9] prevent extreme behaviors while maintaining strategic flexibility

## Edge Case Handling

### Round 1 (Bootstrap)
- **Action:** COOPERATE
- **Rationale:** Initiate prosocially; establish cooperation baseline without assuming opponent types
- **Risk mitigation:** First-round defection rates inform future decisions

### Round r (Final Round)
- **Special consideration:** Apply normal threshold logic, BUT...
- **Enhancement:** If cooperation_rate in round r-1 was ≥ 0.5, COOPERATE regardless of exact threshold
- **Rationale:** Final-round mutual cooperation yields collective benefit; defecting on willing partners contradicts prosocial intent
- **Safeguard:** If cooperation_rate in round r-1 was < 0.3, still DEFECT (exploit-resistant)

### Single-Round Scenario (r = 1)
- **Action:** COOPERATE
- **Rationale:** With no future, reciprocity is moot; prosocial default applies

### Extremely Low Cooperation (< 20% in any round)
- **Action:** DEFECT for next round, then reassess
- **Rationale:** Majority defectors indicate hostile environment; temporary defection protects against systematic exploitation
- **Recovery:** Rejoin cooperation if cooperation_rate recovers above threshold

## Prosocial Alignment

### Design Principles Embedded

1. **Cooperation-first**: Opens with trust, not cynicism
2. **Reciprocity with mercy**: Responsive to others' cooperation while allowing recovery from isolated defections
3. **Gradient tolerance**: Doesn't require perfection; tolerates partial cooperation
4. **Anti-exploitation**: Protects against free-rider dominance through adaptive thresholds
5. **Collective-oriented final rounds**: Prioritizes group welfare when opponents show willingness

### Why This Is Prosocial

- **Maximizes mutual benefit**: When players cooperate, threshold-based reciprocation maintains the public good (payoff = 2 when all play C, versus 1 when all play D)
- **Enables coordination without communication**: Adaptive thresholds allow loose coalitions of reciprocal players to form organically
- **Reduces cycles of retaliation**: Tolerance band prevents tit-for-tat escalation
- **Graceful degradation**: Shifts to exploitation-resistance only when evidence demands it, not preemptively

## Implementation Notes

### Memory Requirements
- Track: count of cooperators in each historical round
- Calculate: cooperation_rate from this history
- No player-specific grudges (fairness-based)

### Pseudocode Summary

```
history = []

PLAY(round t):
    if t == 1:
        cooperate()
        history.append(true)
    else:
        coop_count = history.count(true)
        coop_rate = coop_count / (t - 1)
        threshold = max(0.4, min(0.9, (r - t) / r))
        
        if t == r and coop_rate >= 0.5:
            cooperate()
        elif t == r and coop_rate < 0.3:
            defect()
        elif coop_rate >= threshold:
            cooperate()
        else:
            defect()
        
        history.append(action_taken)
```

## Robustness Properties

- **Against Unconditional Cooperators**: Reciprocates fully, achieving mutual max payoff
- **Against Unconditional Defectors**: Defects after round 1, minimizing damage
- **Against Tit-for-Tat**: Cooperates synchronously, supporting stable mutual benefit
- **Against Mixed Strategies**: Adapts threshold dynamically, avoiding punishment cycles
- **Against Probabilistic Defectors**: Cooperation rate naturally filters noise; tolerates occasional defection

This strategy sacrifices exploitative gains for sustainable, prosocial outcomes in multi-agent environments with repeated interaction.
'''

description_PROSOCIAL_31 = '''
# ADAPTIVE PROSOCIAL STRATEGY: "Conditional Reciprocal Generosity"

## CORE PHILOSOPHY
This strategy seeks to maximize collective welfare while protecting against exploitation, operating under the assumption that others may be strategic, selfish, or unpredictable. It balances prosocial contribution with rational self-protection.

## DECISION RULES

### 1. ROUND-DEPENDENT BASELINE

**Early Rounds (t ≤ r/3):** COOPERATE
- Establish a prosocial reputation and signal cooperative intent
- Gather information about opponent types through their responses
- Benefit from the possibility of reciprocal cooperation while still affordable

**Middle Rounds (r/3 < t ≤ 2r/3):** CONDITIONAL on recent history
- Adapt based on observed cooperation rates and reciprocation patterns
- Implement tit-for-tat-style reciprocity with a generosity buffer

**Late Rounds (t > 2r/3):** PROTECTIVE
- Shift toward defection if cooperation has been consistently exploited
- Maximize own payoff when reputation effects become irrelevant
- Still maintain some cooperation to avoid pure exploitation by others

### 2. ADAPTIVE RECIPROCITY RULE (Middle & Late Rounds)

**Calculate the "Cooperation Health Index" (CHI):**

```
CHI = (Average cooperation rate of all other players in last 3 rounds)
      compared to a baseline threshold of (k/n)
```

**Decision Logic:**

```
IF round is 1 to ⌊r/3⌋:
    COOPERATE
    
ELSE IF round is ⌊r/3⌋ + 1 to ⌊2r/3⌋:
    recent_coop_rate = (sum of cooperators in last 3 rounds) / (3n)
    
    IF recent_coop_rate > k/n:
        COOPERATE  [Others are contributing enough to make it worthwhile]
    ELSE IF recent_coop_rate > k/n - 0.15:
        COOPERATE with probability 0.7  [Cautious optimism with buffer]
    ELSE:
        DEFECT  [Cooperation isn't being reciprocated]
        
ELSE IF round is ⌊2r/3⌋ + 1 to r-1:
    recent_coop_rate = (sum of cooperators in last 2 rounds) / (2n)
    
    IF recent_coop_rate > k/n + 0.1:
        COOPERATE  [Strong positive signal]
    ELSE IF recent_coop_rate ≥ k/n - 0.1:
        COOPERATE with probability 0.4  [Declining cooperation, less optimistic]
    ELSE:
        DEFECT  [Protect remaining rounds]
        
ELSE IF round is r:  [FINAL ROUND]
    DEFECT  [No future reputation effects; self-interested]
```

### 3. EDGE CASES & SPECIAL HANDLING

**First Round (t=1):**
- COOPERATE unconditionally
- Rationale: No history exists; establish goodwill signal; gather information

**Last Round (t=r):**
- DEFECT unless r ≤ 3 (very short game)
- Rationale: No future rounds for reciprocation; end-game logic dominates
- Exception: If r ≤ 3, maintain cooperation in all rounds to avoid mutual defection spirals in short games

**Insufficient History (first 3 rounds):**
- Use observed actions so far rather than 3-round window
- Avoid over-weighting small sample sizes of defections

**Perfect Cooperation Scenario:**
- If all players maintain C in every observed round, continue cooperating
- This yields the Pareto-optimal outcome (π_i = k per round for all)

**Mutual Defection Trap:**
- If all players defect for 2+ consecutive rounds, continue defecting
- Rationale: Attempting to break the trap is costly and unlikely to succeed without coordination

## PROSOCIAL COMMITMENTS

**Why This Strategy Is Prosocial:**

1. **Cooperation First:** Starts with cooperation in early rounds, attempting to establish mutual benefit before defecting

2. **Reciprocal Generosity:** Maintains a "generosity buffer" (tolerance for slightly-below-threshold cooperation) rather than switching to defection at the first sign of lower cooperation

3. **Collective Welfare:** The threshold for cooperation is k/n—the point at which the public good payoff matches the private payoff. At this threshold or above, continuing cooperation is socially optimal

4. **Information Gathering:** Early cooperation serves both a reputational and informational purpose, allowing assessment of opponent types before pessimistic strategies dominate

5. **Transparency:** The strategy is deterministic and predictable (except for stochastic decisions in ambiguous middle-ground scenarios), encouraging potential reciprocation

6. **Balanced Protection:** Defects when reciprocation fails, avoiding exploitation but still potentially re-entering cooperation if others change course

## PSEUDOCODE SUMMARY

```
strategy(round_t, game_history, parameters_n_r_k):
    
    if round_t == 1:
        return COOPERATE
    
    if round_t <= floor(r / 3):
        return COOPERATE
    
    if round_t <= floor(2r / 3):
        recent_coop = avg_cooperators_in_last_3_rounds(game_history)
        if recent_coop > k/n:
            return COOPERATE
        elif recent_coop > k/n - 0.15:
            return COOPERATE with probability 0.7
        else:
            return DEFECT
    
    if round_t < r:
        recent_coop = avg_cooperators_in_last_2_rounds(game_history)
        if recent_coop > k/n + 0.1:
            return COOPERATE
        elif recent_coop >= k/n - 0.1:
            return COOPERATE with probability 0.4
        else:
            return DEFECT
    
    if round_t == r:
        return DEFECT  [unless r <= 3, then COOPERATE]
```

## ROBUSTNESS CLAIMS

- **vs. Pure Defectors:** Minimizes losses by defecting after early rounds
- **vs. Cooperators:** Achieves mutual cooperation and high payoffs
- **vs. Tit-for-Tat:** Outperforms through early reputation-building and stochastic generosity
- **vs. Exploiters:** Detects and responds to systematic free-riding
- **vs. Chaos:** Adapts to changing cooperation rates without requiring perfect pattern recognition

This strategy prioritizes collective welfare while remaining individually rational, making it genuinely prosocial.
'''

description_PROSOCIAL_32 = '''
# PROSOCIAL STRATEGY: Adaptive Reciprocal Contribution (ARC)

## CORE PHILOSOPHY

This strategy balances prosocial commitment with rational self-protection. It recognizes that sustained cooperation creates mutual benefit (when k > 1, collective payoff exceeds individual defection payoff), but requires safeguards against exploitation.

## DECISION RULES

### PRIMARY RULE: Conditional Contribution Based on Cooperation Rate

**For round t (where t > 1):**

```
cooperation_rate_prev = (total cooperators in round t-1) / n

if cooperation_rate_prev ≥ threshold_high:
    COOPERATE
elif cooperation_rate_prev ≥ threshold_medium:
    COOPERATE (with probability proportional to rate)
elif cooperation_rate_prev < threshold_low:
    DEFECT
```

**Threshold Calibration** (adaptive to game parameters):
- `threshold_high = 0.5` (majority cooperating signals healthy collective)
- `threshold_medium = 0.3` (minority cooperating; reciprocate their effort)
- `threshold_low = 0.2` (widespread defection; protect individual payoff)

### PROBABILISTIC COOPERATION IN AMBIGUOUS ZONES

When `0.3 ≤ cooperation_rate_prev < 0.5`:

```
cooperation_probability = (cooperation_rate_prev - 0.3) / 0.2
Play C with this probability; play D otherwise
```

This prevents exploitation while rewarding genuine (if imperfect) cooperation attempts.

---

## EDGE CASES & SPECIAL HANDLING

### **Round 1 (First Round)**
```
COOPERATE
```
**Rationale:** 
- Initiates prosocial signal; tests whether the environment rewards cooperation
- Sets reciprocal baseline for future rounds
- Acknowledges uncertainty about opponent strategies

### **Final Round (t = r)**
```
Follow the Primary Rule based on round r-1 cooperation rate
```
**Rationale:**
- Resist "endgame defection" temptation
- Maintain consistency—sudden defection would contradict established reciprocal pattern
- If environment has cooperated, reciprocate genuinely through the end

### **Rounds 2-3 (Warm-up Phase)**
```
Apply Primary Rule, but increase threshold_high to 0.55
(Slightly more generous to allow cooperation patterns to establish)
```
**Rationale:**
- Early-round noise shouldn't trigger immediate defection
- Gives genuinely cooperative groups time to coalesce

---

## PROSOCIAL ALIGNMENT

**1. Cooperation as Default**
- Cooperates in round 1 and whenever cooperation rate ≥ 50%
- This shifts the baseline toward collective welfare

**2. Reciprocity, Not Exploitation**
- Matches others' cooperation levels probabilistically
- Does not unilaterally defect when cooperation exists (even if minority)
- Punishes only persistent free-riding (cooperation_rate < 20%)

**3. Collective Payoff Focus**
- When k > 1, all-cooperation yields 2k/n per player vs. 1 for all-defection
- Strategy aims to encourage the cooperative equilibrium that maximizes group welfare
- By cooperating when others do, the strategy helps achieve mutual benefit

**4. Graceful Degradation**
- Doesn't retaliate harshly (no tit-for-tat grudges)
- Allows recovery: if defectors switch to cooperation, ARC immediately reciprocates
- Treats each round as a fresh signal, not a permanent verdict

**5. Robustness to Opponent Diversity**
- **vs. Always-Cooperate:** Reciprocates fully → mutual high payoff
- **vs. Always-Defect:** Defects after round 1 → protects against exploitation
- **vs. Tit-for-Tat:** Cooperates with it after round 1 → mutual cooperation
- **vs. Random:** Tracks empirical cooperation rate → adapts dynamically
- **vs. Conditional Free-riders:** Defects when they dominate; re-cooperates if they convert

---

## PSEUDOCODE

```python
def ARC_strategy(game_history, current_round, n, k, r):
    
    if current_round == 1:
        return COOPERATE
    
    # Calculate cooperation rate in previous round
    prev_round_actions = game_history[current_round - 1]
    coop_count = sum(1 for action in prev_round_actions if action == C)
    coop_rate = coop_count / n
    
    # Adjust thresholds for early rounds
    if current_round <= 3:
        high_threshold = 0.55
    else:
        high_threshold = 0.50
    
    medium_threshold = 0.30
    low_threshold = 0.20
    
    # Decision logic
    if coop_rate >= high_threshold:
        return COOPERATE
    
    elif coop_rate >= medium_threshold:
        prob = (coop_rate - medium_threshold) / (high_threshold - medium_threshold)
        return COOPERATE if random() < prob else DEFECT
    
    else:  # coop_rate < low_threshold
        return DEFECT
```

---

## STRATEGIC INTUITION

This strategy succeeds because it:
1. **Leads by example** (cooperate first)
2. **Reciprocates genuinely** (mirrors group behavior)
3. **Protects margins** (exits before severe exploitation)
4. **Remains forgiving** (re-enters cooperation if conditions improve)
5. **Maximizes collective payoff** when others are also prosocial

It balances the *social dilemma*: pursuing individual payoff (defecting) vs. collective welfare (cooperating). By making cooperation conditional on visible reciprocation, it encourages the high-payoff equilibrium without naïve vulnerability.
'''

description_COMMUNAL_1 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances three objectives:
1. **Mutual benefit maximization** - Recognize that cooperation generates collective value
2. **Robustness** - Defend against exploitation while remaining open to cooperation
3. **Adaptation** - Respond to observed behavior patterns to steer the game toward higher-payoff equilibria

The strategy is "communal" because it actively seeks to establish and maintain cooperative norms, while remaining pragmatic about free-riders.

---

## Strategy Definition

### Decision Rule - Three Phases

The strategy operates across three overlapping phases:

#### Phase 1: Early Exploration (Rounds 1 to min(3, ⌊r/3⌋))
**Action: COOPERATE**

**Rationale:**
- Signal cooperative intent to all players
- Gather information about opponent types
- Establish a baseline for reciprocal relationships
- Early cooperation costs are low relative to long-term relationship value

#### Phase 2: Adaptive Reciprocity (Rounds 4 to r-1)
**Action: Based on observed cooperation rate**

```
observed_coop_rate = (total_cooperators_in_previous_rounds) / 
                     (n × rounds_completed)

IF observed_coop_rate ≥ threshold_high (e.g., 0.6):
    Action = COOPERATE
    Rationale: Sufficient cooperation detected; reciprocate broadly
    
ELSE IF observed_coop_rate ≥ threshold_mid (e.g., 0.35):
    Action = COOPERATE with probability p_adaptive
    where p_adaptive = observed_coop_rate
    Rationale: Mixed cooperation signals conditional willingness
    
ELSE IF observed_coop_rate < threshold_mid:
    Action = DEFECT
    Rationale: Insufficient cooperation; protect payoff
```

**Key thresholds:**
- `threshold_high = 0.6`: When majority cooperates, mutual benefit is clear
- `threshold_mid = 0.35`: Below this, defection becomes self-protective
- Probability matching: `p_adaptive = observed_coop_rate` creates a "mirror effect" that rewards cooperation proportionally

**Rationale for thresholds:**
- At `k < n`, cooperation by everyone yields payoff `k` per player
- Defection against all yields payoff `1`
- Therefore, cooperation is only individually rational if roughly k/n proportion of others cooperate
- Our thresholds (0.6, 0.35) are conservative, requiring higher cooperation to justify cooperation

#### Phase 3: Endgame (Final round r)
**Action: DEFECT**

**Rationale:**
- With no future rounds, reputation concerns disappear
- The finality of the last round eliminates long-term incentive for cooperation
- This is subgame-perfect: defection in the final round is a dominant strategy
- Other rational players will expect this; signaling otherwise is not credible

---

## Edge Case Handling

| Scenario | Handling |
|----------|----------|
| **Round 1** | COOPERATE (exploration phase) |
| **Round r (final)** | DEFECT (no future payoffs) |
| **Perfect cooperation observed** | COOPERATE (mutual benefit confirmed) |
| **Perfect defection observed** | DEFECT (self-defense) |
| **Mixed observation** | Use probability matching (Phases 2) |
| **Tied cooperation rates** | COOPERATE (favor reciprocal openness) |
| **Incomplete history** (round 2-3) | Use partial observations; cooperate by default |

---

## Pseudocode

```
function decide_action(round, n, k, history):
    
    if round == 1:
        return COOPERATE
    
    if round == r:  // final round
        return DEFECT
    
    // Calculate observed cooperation rate
    total_rounds_completed = round - 1
    total_cooperators = count_all_cooperators_in_history(history)
    observed_coop_rate = total_cooperators / (n × total_rounds_completed)
    
    // Phase 2: Adaptive Reciprocity
    threshold_high = 0.6
    threshold_mid = 0.35
    
    if observed_coop_rate ≥ threshold_high:
        return COOPERATE
    
    else if observed_coop_rate ≥ threshold_mid:
        p_adaptive = observed_coop_rate
        if random(0, 1) < p_adaptive:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // observed_coop_rate < threshold_mid
        return DEFECT
```

---

## Why This Strategy Is Communal

1. **Signal-Based Leadership**: Early cooperation signals willingness to contribute, inviting reciprocal behavior
2. **Incentive Alignment**: The probability-matching mechanism rewards communities that cooperate
3. **Vulnerability to Better Outcomes**: The strategy openly pursues cooperation even knowing exploitation is possible—this is the essence of communal thinking
4. **Collective Learning**: By observing and responding to aggregate behavior, the strategy helps the group discover whether cooperation is viable
5. **Self-Correcting**: If exploitation dominates, the strategy shifts to defense, but remains ready to re-engage if cooperation re-emerges

---

## Robustness Properties

- **Against pure defectors**: Quickly pivots to defection after phase 1
- **Against tit-for-tat**: Probability matching prevents locking into mutual defection
- **Against mixed players**: Adaptive thresholds prevent overcommitment to uncooperative groups
- **Against last-round exploitation**: Final round defection prevents being used in endgame
- **Scalability**: Works for any n ≥ 2 and 1 < k < n (thresholds are parameter-independent)

This strategy embodies communal ethics—it assumes the best initially, remains realistic about human (or AI) nature, and seeks sustainable cooperation through measured reciprocity.
'''

description_COMMUNAL_2 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Strategy Name: "Graduated Reciprocal Altruism with Decay" (GRAD)

## Core Philosophy

This strategy seeks to maximize collective welfare while protecting against exploitation. It operates on the principle that sustained cooperation benefits everyone, but defection must be met with calibrated consequences that incentivize reform rather than escalate conflict.

---

## Decision Rules

### Primary Rule: Reciprocal Contribution Matching

```
cooperation_rate = (number of cooperators in previous round) / n

In current round:
  IF round == 1:
    Cooperate (establish cooperative baseline)
  ELSE:
    Cooperate with probability = cooperation_rate × (1 - discount_factor)
    where discount_factor = (current_round / total_rounds)
```

**Rationale:** 
- Match the cooperation level of the group from the previous round
- Weight recent history more heavily than distant past
- Introduce a small stochastic element to avoid being exploitable through pattern recognition

### Secondary Rule: Tragedy Prevention Threshold

```
observed_defection_ratio = (number of defectors in previous round) / n

IF observed_defection_ratio > threshold:
  defection_incentive = 1 - (total_payoff_last_round / n) / max_possible_payoff
  
  Cooperate with probability = max(0.3, cooperation_rate - defection_incentive)
```

**Rationale:**
- If widespread defection occurs, acknowledge that individual payoffs are suffering
- Maintain a 30% cooperation "floor" to signal willingness to re-establish cooperation
- Prevent downward spirals while protecting against systematic exploitation

### Tertiary Rule: Endgame Adaptation

```
rounds_remaining = total_rounds - current_round

IF rounds_remaining <= 2:
  IF cooperation_rate >= 0.5:
    Cooperate (reward late cooperation)
  ELSE:
    Defect (no future rounds to punish non-cooperation)
ELSE:
  Apply primary and secondary rules
```

**Rationale:**
- In final rounds, defection becomes individually rational if cooperation is low
- However, reward groups that cooperated throughout the game
- This prevents the standard "last round defection" collapse while maintaining incentives

---

## Edge Cases & Special Handling

### Round 1
**Action:** Cooperate unconditionally
**Rationale:** Establish a cooperative baseline. This signals goodwill and tests the group's fundamental disposition.

### Round 2
**Action:** Match Round 1 cooperation rate (reciprocate)
**Rationale:** Respond to initial signals. If all cooperated, continue. If many defected, calibrate downward with some residual cooperation.

### Explosive Defection (>75% of players defect)
```
IF defection_ratio > 0.75 AND this has occurred for 2 consecutive rounds:
  Switch to "Harsh Reciprocal" mode:
  - Cooperate with probability 0.2
  - Resume normal strategy when cooperation_rate > 0.4
```
**Rationale:** Recognize systemic breakdown. Don't waste endowment in a completely defective environment, but maintain hope for recovery.

### Payoff Analysis
```
IF (my_average_payoff < (1 - k/n) × 1.1):
  Assume the group is in a defection spiral
  Increase cooperation_floor from 0.3 to 0.4
  Rationale: Everyone is suffering; time to attempt repair
```

---

## Communal Alignment

### How This Serves Community:
1. **Cooperation Leadership:** Always cooperates in Round 1, establishing cooperation as the default expectation
2. **Repair Mechanism:** The 30% floor and payoff-responsive rules create incentives for defectors to return to cooperation
3. **Reward Structure:** Higher cooperation rates are directly rewarded with higher individual participation
4. **Transparency:** Strategy is deterministic (except stochastic matching), making it predictable and trustworthy

### Robustness Properties:
- **vs. Pure Defectors:** Gradually reduces cooperation to match their contributions (payoff: 1)
- **vs. Pure Cooperators:** Reciprocates fully (payoff: 2)
- **vs. Mixed Strategies:** Adapts dynamically to the actual cooperation rate
- **vs. Defection Spirals:** Floor mechanism prevents race-to-the-bottom collapse
- **vs. Late-Round Exploiters:** Endgame rule punishes them by defecting when it matters most

---

## Implementation Pseudocode

```
function decide_action(round, total_rounds, history):
  
  if round == 1:
    return COOPERATE
  
  prev_cooperators = count_cooperators(history[round-1])
  cooperation_rate = prev_cooperators / n
  rounds_remaining = total_rounds - round
  
  // Endgame special case
  if rounds_remaining <= 2:
    if cooperation_rate >= 0.5:
      return COOPERATE
    else:
      return DEFECT
  
  // Check for sustained defection spiral
  if cooperation_rate < 0.25 and round >= 3:
    defection_streak = check_consecutive_low_cooperation(history, threshold=0.25, depth=2)
    if defection_streak:
      return COOPERATE with probability 0.2
  
  // Payoff-responsive threshold adjustment
  floor = 0.3
  if my_average_payoff < (1 - k/n) * 1.1:
    floor = 0.4
  
  // Discount factor increases over time
  discount = round / total_rounds
  
  // Base reciprocal decision
  base_prob = cooperation_rate * (1 - discount)
  
  return COOPERATE with probability max(floor, base_prob)
```

---

## Summary

**GRAD** balances individual rationality with communal welfare by:
- **Leading with cooperation** but matching group behavior thereafter
- **Protecting collective welfare** through a cooperation floor that enables recovery from defection spirals
- **Punishing exploitation** through graduated responses rather than all-or-nothing strategies
- **Adapting strategically** to endgame conditions where cooperation incentives differ

This strategy is communal because it genuinely improves outcomes for all players when reciprocated, while remaining robust to non-cooperative opponents.
'''

description_COMMUNAL_3 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy seeks to maximize collective welfare while remaining robust to exploitation. It recognizes that:
- Pure defection leaves value on the table (collective payoff from cooperation is superior)
- Pure cooperation is exploitable by free-riders
- Adaptive behavior allows recovery from defection spirals
- Community benefit should be pursued, but with safeguards

## Strategy: "Conditional Reciprocal Communalism" (CRC)

### 1. DECISION RULES

**Standard Round Decision:**
```
If (round == 1):
    COOPERATE
Else if (cooperation_rate_last_round >= threshold_t):
    COOPERATE
Else if (cooperation_rate_last_round < threshold_t AND rounds_remaining > 1):
    DEFECT (signal dissatisfaction, allow recovery opportunity)
Else if (rounds_remaining == 1):
    COOPERATE (final round reciprocal offer)
Else:
    COOPERATE (default to community-building)

Where:
  cooperation_rate_last_round = (number of cooperators in previous round) / n
  threshold_t = (k - 1) / (n - 1)  [derived from incentive structure]
  rounds_remaining = r - current_round
```

### 2. THRESHOLD JUSTIFICATION

The threshold `(k-1)/(n-1)` represents the **critical cooperation level**:
- When k>1 and cooperation exceeds this threshold, the average public good payoff exceeds private defection payoff
- Below this, a defector gains more than cooperators
- This threshold is **game-parameter-aware**, adapting automatically to different n and k values

**Example (n=6, k=2):**
- Threshold = (2-1)/(6-1) = 1/5 = 0.2
- Need ≥20% cooperation for cooperation to be individually rational
- If >20% cooperate, public goods exceed private incentive

### 3. EDGE CASES

**First Round (round == 1):**
- COOPERATE unconditionally
- Rationale: Establish communal intent, create opportunity for positive equilibrium
- No history exists to condition on

**Last Round (current_round == r):**
- COOPERATE if cooperation_rate_last_round >= threshold_t
- Otherwise, DEFECT (final payoff maximization when no future rounds exist)
- Rationale: When rounds remain, defection blocks recovery; when none remain, enforce fairness

**Single Defector Scenario:**
- If one player defects while n-1 cooperate, threshold is still met
- Continue cooperating (robust to isolated defection)
- Defector earns more, but community sustains

**Cascade Defection:**
- Once cooperation drops below threshold, DEFECT for one round
- This signals "I'm monitoring; the deal requires reciprocity"
- Next round, return to cooperation if threshold recovers
- Prevents exploitation cycles

## 4. COMMUNAL ALIGNMENT

This strategy embodies communalism through:

| Principle | Implementation |
|-----------|-----------------|
| **Collective Benefit** | Cooperates when community threshold met; actively seeks mutual gain |
| **Fair Reciprocity** | Defects when others don't reciprocate (punishes free-riding) |
| **Forgiveness** | One defection round triggers reset, not permanent punishment |
| **Sustainability** | Preserves long-term cooperation through monitored, conditional engagement |
| **Transparency** | Behavior is entirely rule-based; no hidden strategies |
| **Resilience** | Works across game parameters without special tuning |

## 5. PSEUDOCODE

```
function decide(current_round, total_rounds, n, k, history):
    
    if current_round == 1:
        return COOPERATE
    
    last_round_cooperators = count_cooperators(history[current_round - 1])
    coop_rate = last_round_cooperators / n
    threshold = (k - 1) / (n - 1)
    rounds_left = total_rounds - current_round
    
    if coop_rate >= threshold:
        return COOPERATE
    
    if coop_rate < threshold:
        if rounds_left > 0:
            return DEFECT  // Signal: reciprocity required, recovery possible
        else:
            return DEFECT  // Final payoff extraction (no future)
    
    // Fallback (shouldn't reach)
    return COOPERATE
```

## 6. ROBUSTNESS PROPERTIES

- **vs. Pure Defectors:** Will defect after first round; minimizes damage
- **vs. Pure Cooperators:** Achieves mutual cooperation and high payoff
- **vs. Tit-for-Tat variants:** Compatible; mirrors their cooperation rates
- **vs. Mixed/Random strategies:** Adapts dynamically; benefits when variance above threshold
- **vs. Sophisticated exploiters:** One-round punishment prevents sustained exploitation
- **Parameter-agnostic:** Threshold automatically scales with n and k

## 7. SUMMARY

**"Conditional Reciprocal Communalism"** is a **data-driven, adaptive, punishment-resistant** strategy that:
1. **Leads with cooperation** to enable high-payoff equilibria
2. **Conditions on observed cooperation rates** using a theoretically grounded threshold
3. **Punishes free-riding** with temporary defection to enforce reciprocity
4. **Recovers quickly** to allow positive equilibrium restoration
5. **Respects the endgame** by extracting final payoff only when no recovery is possible

This balances communal ideals with strategic robustness in competitive, uncoordinated environments.
'''

description_COMMUNAL_4 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARC)

## Core Philosophy
This strategy balances communal value creation with individual security. It recognizes that sustainable cooperation requires:
1. **Demonstrated trustworthiness** - Prove commitment to the common good
2. **Adaptive responsiveness** - React intelligently to defection patterns
3. **Strategic resilience** - Maintain cooperativeness while protecting against exploitation
4. **Temporal awareness** - Adjust behavior based on game stage

---

## STRATEGY SPECIFICATION

### ROUND CLASSIFICATION

Divide the r rounds into three phases:
- **Early phase**: rounds 1 to ⌊r/3⌋ (establish intentions)
- **Middle phase**: rounds ⌊r/3⌋ + 1 to ⌊2r/3⌋ (evaluate and adapt)
- **Late phase**: rounds ⌊2r/3⌋ + 1 to r (optimize final position)

---

### DECISION RULE

```
ROUND 1:
  COOPERATE
  (Signal good faith; establish baseline)

ROUNDS 2 through (r-1):
  cooperation_rate = (number of cooperators in previous round) / n
  
  IF cooperation_rate >= threshold(phase):
    COOPERATE
    (Reciprocate cooperation; build momentum)
  
  ELSE IF cooperation_rate < threshold(phase):
    IF personal_cooperation_count / rounds_played >= 0.75:
      COOPERATE with probability = adaptation_factor
      (Maintain some cooperation despite low group rate;
       signal willingness to be the cooperative anchor)
    ELSE:
      DEFECT
      (Limited personal investment history; protect against exploitation)

ROUND r (final round):
  IF cooperation_rate_recent >= threshold(late_phase) * 0.9:
    COOPERATE
    (Reinforce successful cooperation pattern)
  ELSE:
    DEFECT
    (Maximize final payoff if cooperation has failed;
     don't give free value on last move)
```

### THRESHOLD FUNCTION (Phase-Dependent)

```
threshold(early_phase) = (k/n) + 0.15
  → Cooperative if public good multiplier + buffer is exceeded
  → Meaning: ~60%+ of group must cooperate to justify cooperation

threshold(middle_phase) = (k/n) + 0.05
  → More lenient; group has demonstrated tendencies
  → Meaning: ~45%+ must cooperate

threshold(late_phase) = (k/n)
  → Most lenient; focus on reciprocating observed cooperation
  → Meaning: strict reciprocity; match the group's behavior
```

### ADAPTATION FACTOR

```
adaptation_factor = 0.5 + (0.5 × personal_cooperation_count / rounds_played)

Interpretation:
  - If you've cooperated in 100% of past rounds → 100% chance to cooperate
  - If you've cooperated in 75% of past rounds → 87.5% chance to cooperate
  - If you've cooperated in 50% of past rounds → 75% chance to cooperate
  
This incentivizes consistent cooperation while allowing gradual defection
if the environment proves hostile.
```

---

## EDGE CASE HANDLING

### First Round (Round 1)
**Action: COOPERATE**
- Establishes the "cooperative hypothesis" without needing history
- Signals group-oriented intent
- Generates initial signal about group composition

### Last Round (Round r)
**Special logic applied** (see decision rule above)
- Final defection is rational IF group has failed to cooperate
- BUT: If cooperation has been strong, reinforce it to maintain group norm
- Prevents "free-rider exit" strategy from being optimal

### Small Groups (n = 2)
- Same logic applies, but thresholds become more sensitive
- Early phase: need ≥1 cooperator (any cooperation triggers reciprocal cooperation)
- With k ≈ 1, even small group cooperation barely breaks even, so threshold applies

### Long Games (r → large)
- Early phase provides extended signaling opportunity
- Middle phase allows robust pattern recognition
- Late phase reserves optimization window

### Short Games (r = 2)
- Round 1: COOPERATE (establish intent)
- Round 2: Use final-round logic (defect if no cooperation observed)

---

## COMMUNAL ALIGNMENT

### Why This Strategy is Communal:

1. **Leads with Cooperation**: Round 1 cooperation signals willingness to contribute to collective good without requiring reciprocal proof first.

2. **Reciprocal Fairness**: Thresholds reward genuine cooperation from others, not exploitation. The strategy reciprocates group efforts transparently.

3. **Gradient of Hope**: Rather than hard defection, the adaptation_factor creates a graceful degradation. Even against mostly-defecting groups, this strategy maintains ~50% cooperation rate, potentially reigniting collective action.

4. **Preserves Cooperation Equilibrium**: By making cooperation a strong attractor (low thresholds in middle/late phases), the strategy actively works to maintain mixed cooperation in the group.

5. **Punishes Pure Free-Riding**: The final-round defection prevents players from exploiting cooperation history without contributing themselves.

6. **History-Aware but Non-Vindictive**: The strategy doesn't permanently punish single rounds of defection; it evaluates *patterns* over phases.

---

## ROBUSTNESS PROPERTIES

| Opponent Type | Expected Outcome |
|---|---|
| All-Cooperate | Mutual cooperation; π_i ≈ 2 |
| All-Defect | Settle to π_i ≈ 1, after initial loss |
| Tit-for-Tat | Stable mutual cooperation |
| Random 50% | Adapt to ~50% cooperation; π_i ≈ 1.5 |
| Late-stage Defectors | Catch defection in middle phase; adjust accordingly |
| Win-Stay/Lose-Shift | Converge to mutual cooperation |

---

## PSEUDOCODE SUMMARY

```
history = []

FOR each round t:
  IF t == 1:
    action[t] = COOPERATE
  
  ELSE IF t == r:
    cooperation_rate = COUNT(history[t-1] == C) / n
    IF cooperation_rate >= threshold(late_phase) * 0.9:
      action[t] = COOPERATE
    ELSE:
      action[t] = DEFECT
  
  ELSE:
    cooperation_rate = COUNT(history[t-1] == C) / n
    my_coop_ratio = COUNT(my_actions[1..t-1] == C) / (t-1)
    
    phase = classify(t, r)
    
    IF cooperation_rate >= threshold(phase):
      action[t] = COOPERATE
    ELSE:
      IF my_coop_ratio >= 0.75:
        action[t] = COOPERATE with probability = 0.5 + 0.5*my_coop_ratio
      ELSE:
        action[t] = DEFECT
  
  history.append(action[t])
```

This strategy embodies communal thinking while remaining strategically sound.
'''

description_COMMUNAL_5 = '''
# Adaptive Reciprocal Stewardship (ARS) Strategy

## Core Philosophy

This strategy balances individual rationality with communal benefit by recognizing that sustainable cooperation requires:
1. **Earned trust**: Reciprocate genuine cooperation, not blind faith
2. **Defensive rationality**: Punish exploitation without escalation
3. **Adaptive learning**: Adjust to opponent composition dynamically
4. **Long-term thinking**: Weight future rounds, not just immediate payoff

## Decision Framework

### Stage 1: Assessment Phase (First 2 rounds, or first ⌈r/5⌉ rounds)

**Action**: Play C (Cooperate)

**Rationale**: 
- Test the environment without commitment cost
- Gather data on opponent cooperativeness
- Signal cooperative intent to reciprocal players
- Early cooperation establishes baseline for comparison

**Track**: 
- Global cooperation rate: `coop_rate = total_cooperators / (n × rounds_elapsed)`
- Opponent profile: Which players cooperated in each round

### Stage 2: Adaptive Main Phase (Rounds 3 to r-1)

**Decision Rule - Modified Generous Tit-for-Tat with Threshold**:

```
cooperation_threshold = k / n
global_coop_rate = total_cooperators_so_far / (n × rounds_elapsed)

if global_coop_rate ≥ cooperation_threshold:
    # Cooperative environment exists
    if my_previous_action == C:
        action = C  # Continue cooperation
    else:
        # Recovering from defection
        action = C with probability 0.7, else D
        
else if global_coop_rate ≥ 0.33:
    # Mixed environment - be selective
    defectors_last_round = count of players who played D
    
    if defectors_last_round ≤ ⌈n/3⌉:
        # Few defectors - worth cooperating
        action = C
    else:
        # Many defectors - protect yourself
        action = D
        
else:
    # Defection is rampant (coop_rate < 0.33)
    # Last-resort self-protection
    action = D
```

**Intuition**:
- Cooperate when `k/n` players cooperating yields positive returns
- If threshold met, reciprocate previous cooperation
- In mixed environments, cooperate only when defectors are minority
- In defection-dominant environments, minimize losses

### Stage 3: Endgame Phase (Final round only)

**Action**: Cooperate (C)

**Rationale**:
- No future rounds means no punishment mechanism for defection
- Pure self-interest would suggest defection (the "temptation" payoff)
- **But**: Cooperation signals character and stewardship over self-maximization
- In a communal framing, the final act is a statement of values
- Some reciprocal opponents will have adjusted their final move upward if they've observed cooperation; this creates mutual gain

---

## Edge Cases & Special Handling

### Round 1
- **Action**: C
- **Rationale**: Minimal information; cooperation costs only the endowment but signals trustworthiness

### Round 2
- **Action**: C
- **Rationale**: Complete assessment phase; need two data points before strategic divergence

### Rounds where n=2 (Two-player case)
- Modify threshold to `k/2`
- Defection is maximally damaging (no diffusion across other players)
- Use more aggressive tit-for-tat: defect immediately after opponent defects

### When r = 2 (Minimal repetition)
- Skip Stage 2 entirely
- Execute Stage 1 (Round 1), then Stage 3 (Round 2, final)

### Recovering from accidental/strategic defection
- If I defected in round t, increase cooperation probability in round t+1 to 0.7
- Signal that defection was tactical, not character-based
- Reciprocal players may restore cooperation

---

## Communal Alignment

**How this embodies communal values**:

1. **Stewardship**: Treats the public good as shared responsibility; contributes when environment sustains it
2. **Reciprocity**: Responds to others' contributions, not blind altruism
3. **Fairness**: Punishes free-riding (by defecting when others exploit) but not aggressively
4. **Sustainability**: Avoids arms races; seeks stable cooperative equilibrium at k/n threshold
5. **Hope**: Always reopens cooperation after defection; final move is unconditional cooperation
6. **Realism**: Recognizes that pure cooperation fails against exploiters; adapts defensively

---

## Pseudocode Implementation

```
function decide_action(round, history, n, k, r):
    
    if round == 1 or round == 2:
        return COOPERATE
    
    if round == r:  # Final round
        return COOPERATE
    
    // Calculate metrics from history
    total_coop_instances = sum(cooperators in each past round)
    global_coop_rate = total_coop_instances / (n × (round - 1))
    
    threshold = k / n
    
    if global_coop_rate ≥ threshold:
        if my_last_action == COOPERATE:
            return COOPERATE
        else:
            return COOPERATE with prob 0.7, else DEFECT
    
    else if global_coop_rate ≥ 0.33:
        defectors_last_round = count(D in round-1)
        if defectors_last_round ≤ ceil(n/3):
            return COOPERATE
        else:
            return DEFECT
    
    else:
        return DEFECT
```

---

## Robustness to Opponent Types

| Opponent Type | Response |
|---|---|
| Always Cooperate | Reciprocate fully; extract near-optimal value |
| Always Defect | Quickly shift to defection; minimize losses |
| Tit-for-Tat | Match behavior after round 2; stable mutual cooperation |
| Conditional Cooperators | Aligned; respond to threshold-based play |
| Random | Stabilize around defection if noise is high; less exploitable |
| Vengeful | Careful; defect rarely and signal recovery quickly |

This strategy succeeds not by dominating others, but by **creating conditions where cooperation becomes rational**—a true communal achievement.
'''

description_COMMUNAL_6 = '''
# Adaptive Reciprocal Contribution Strategy (ARCS)

## Core Philosophy
This strategy balances **conditional cooperation** with **defection deterrence**, recognizing that in public goods games, the communal good emerges from individual incentives aligning with collective welfare. The strategy is "communal" not through blind trust, but through rewarding cooperation when it's observable and sustainable.

## Decision Rules

### Primary Decision Logic

**For Round t (where t = 1 to r):**

```
IF t == 1:
    COOPERATE
    
ELSE IF t == r (final round):
    DEFECT
    
ELSE (rounds 2 to r-1):
    cooperation_rate = (total cooperators in round t-1) / n
    
    IF cooperation_rate >= threshold(t):
        COOPERATE
    ELSE:
        DEFECT
```

### Threshold Function

The cooperation threshold decreases over time to account for potential defector strategy dominance:

```
threshold(t) = k / n + decay_factor × (t - 2) / (r - 2)

where decay_factor = (n - k) / (2n)
```

**Intuition:** 
- Start with threshold at `k/n` (the break-even point where cooperation yields equal payoff to defection)
- Gradually relax the threshold as rounds progress, acknowledging that consistent defection may dominate
- This prevents futile attempts to sustain cooperation against determined defectors

## Edge Cases & Special Handling

### Round 1 (First Round)
**Action: COOPERATE**

Rationale: Establish good-faith signal and gather information about opponent composition.

### Round r (Last Round)
**Action: DEFECT**

Rationale: Standard subgame-perfect Nash equilibrium logic—no future rounds, so no retaliation costs to defection.

### Rounds 2 to r-1 (Middle Rounds)
**Action: Conditional on observed cooperation rate**

This is the adaptive core. Each round's decision reflects the previous round's behavior:

- **If previous cooperation_rate ≥ threshold:** Continue cooperating (reciprocity)
- **If previous cooperation_rate < threshold:** Defect (protect endowment)

### Special Case: Extreme Defection (cooperation_rate = 0 in any non-first round)
**Action: DEFECT permanently for remaining rounds**

Once everyone defects in a round, recovery is impossible (payoff from cooperating alone = k/n < 1). Do not waste endowment.

## Communal Alignment

### How This Serves the Collective Good

1. **Conditional Cooperation:** The strategy rewards groups moving toward higher contributions, naturally incentivizing collective benefit-seeking players to cluster together.

2. **Defection Deterrence:** By defecting when cooperation falls below sustainable levels, the strategy penalizes free-riders, making exploitation unprofitable. A player who defects while others cooperate gets payoff 2 (in the n=6, k=2 example), but loses this advantage as others learn and defect back.

3. **Graceful Degradation:** Rather than all-or-nothing punishment, the strategy allows gradual recovery. If defectors reduce their defection, cooperation can resume.

4. **Last-Round Pragmatism:** The final-round defection is not vindictive—it reflects game-theoretic reality. A truly communal strategy must be *credible and stable*, not naive.

### Why This Works in Tournaments

- **Against cooperators:** Achieves high mutual payoffs (2 per round) when playing with similar strategies
- **Against pure defectors:** Quickly pivots to defection, limiting exploitation
- **Against tit-for-tat variants:** Cooperative for r-2 rounds, achieving decent aggregate payoff
- **Against mixed strategies:** The adaptive threshold allows recovery from temporary defections while protecting against persistent free-riding

## Pseudocode

```
STRATEGY(game_params: {n, r, k}, history: [round_1_to_t-1]):

  current_round = length(history) + 1
  
  if current_round == 1:
    return COOPERATE
  
  if current_round == r:
    return DEFECT
  
  previous_round_data = history[-1]
  cooperators_last_round = count(previous_round_data.actions == C)
  cooperation_rate = cooperators_last_round / n
  
  threshold = (k / n) + ((n - k) / (2n)) × (current_round - 2) / (r - 2)
  
  if cooperation_rate >= threshold:
    return COOPERATE
  else:
    return DEFECT
```

## Parameter Sensitivity

- **High k (close to n):** Public good is valuable; threshold remains high longer → more cooperation
- **Low k (close to 1):** Public good is weak; threshold decays faster → faster pivoting to defection
- **Long r:** More rounds to signal and recover → more forgiving middle thresholds
- **Short r:** Last round dominates; minimal middle-game cooperation

This design is self-tuning to parameters without explicit adjustment.
'''

description_COMMUNAL_7 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## Core Philosophy

This strategy balances three objectives:
1. **Self-preservation**: Avoid exploitation by free-riders
2. **Communal benefit**: Maximize total welfare when safe to do so
3. **Robustness**: Adapt to opponent behavior without requiring coordination

The strategy recognizes that in public goods games, the Nash equilibrium (all defect) is collectively suboptimal, but individual incentives naturally push toward defection. Therefore, we employ adaptive reciprocity: cooperate conditionally based on demonstrated communal commitment by others.

---

## DECISION RULE FRAMEWORK

### Phase 1: Exploration Round (Round 1)

**Action: COOPERATE**

**Rationale:**
- No history exists; defecting first-round signals non-cooperativeness unnecessarily
- Cooperation reveals that mutual cooperation is achievable
- Sets a cooperative anchor for reputation-building
- Low cost relative to information gained

---

### Phase 2: Reputation Assessment (Rounds 2 through r-2)

**Compute the Cooperation Rate:**
```
cooperation_rate = (total_cooperators_in_previous_rounds) / 
                   (n × (current_round - 1))
```

This gives the empirical likelihood that any random player cooperated historically.

**Threshold-Based Decision:**

**IF** `cooperation_rate ≥ cooperation_threshold` **THEN**
  - **Action: COOPERATE**
  
**ELSE**
  - **Action: DEFECT**

**Where:** `cooperation_threshold = k / n`

---

## Threshold Justification

The threshold `k/n` represents the break-even point where:
- Expected payoff from cooperation ≈ Expected payoff from defection

When cooperation rate exceeds this threshold:
- The average player gets `(k/n) × cooperation_rate ≥ (k/n)²` from the public good
- This exceeds the payoff loss from contributing (1 unit)
- Conditional cooperation becomes individually rational

When cooperation rate falls below this threshold:
- Defectors out-earn cooperators
- The public good is underfunded
- Defection is the rational response

---

### Phase 3: Endgame Strategy (Final 2 Rounds: r-1 and r)

**Round r-1 (Penultimate Round):**

Apply the same rule as Phase 2:
- If `cooperation_rate ≥ k/n`: **COOPERATE**
- Otherwise: **DEFECT**

**Rationale:** Despite being near the end, defection in round r-1 may still provoke retaliation in round r. Maintain consistency.

**Round r (Final Round):**

**Action: DEFECT**

**Rationale:**
- No future rounds exist; no punishment mechanism can deter defection
- This is the unique subgame-perfect equilibrium of finite repeated games
- All rational players should defect in the final round
- Attempting cooperation in the final round is exploitable and naive

---

## Edge Cases and Special Handling

### Case 1: Very High Cooperation Rate Early (≥ 90%)
- **Action:** Continue cooperating through Phase 2
- **Monitor:** Watch for sudden drops (potential coordinated defection)
- **Response:** If cooperation_rate drops below `k/n` in any single round, revert to defection immediately

### Case 2: Immediate Universal Defection (Rounds 2-3 show 0% cooperation)
- **Action:** Defect for remainder of game
- **Rationale:** No profitable public good exists; conserve resources

### Case 3: Oscillating Cooperation Rates
- **Implementation:** Use a 2-round moving average to smooth noise
  ```
  smoothed_rate = (cooperation_in_round_t-2 + cooperation_in_round_t-1) / 2n
  ```
- **Rationale:** Prevents reactive oscillation to random variance

### Case 4: n = 2 (Dyadic Game)
- **Threshold becomes:** k/2
- **Strategy applies identically** but with heightened sensitivity (each player's action has larger impact)
- Consider: If opponent defects consistently, defect back. If opponent cooperates, cooperate.

### Case 5: Very Small k (close to 1)
- **Threshold k/n ≈ 0** (very low)
- Strategy will rarely cooperate beyond round 1
- This is correct: the public good provides minimal benefit; individual payoffs dominate

### Case 6: Very Large k (close to n)
- **Threshold k/n ≈ 1** (very high)
- Strategy requires near-universal cooperation to reciprocate
- This is correct: high leverage means cooperation is highly beneficial if achieved

---

## Pseudocode

```
FUNCTION decide(round, n, k, history):
  
  IF round == 1:
    RETURN COOPERATE
  
  ELSE IF round == n_rounds:
    RETURN DEFECT
  
  ELSE:
    total_cooperations = COUNT(COOPERATE actions in history)
    total_actions = n × (round - 1)
    cooperation_rate = total_cooperations / total_actions
    threshold = k / n
    
    IF cooperation_rate >= threshold:
      RETURN COOPERATE
    ELSE:
      RETURN DEFECT
```

---

## Why This Strategy Is Communal

1. **Mutual Welfare Maximization:** Cooperates whenever the population demonstrates sufficient commitment (cooperation_rate ≥ k/n), at which point cooperation is Pareto-improving

2. **Punishment of Free-Riders:** Automatically defects against populations dominated by defectors, protecting against exploitation

3. **Trust But Verify:** Gives cooperation a fair chance (round 1) but requires demonstrated reciprocity before committing further

4. **No Exploitation:** Cannot be systematically exploited because defection against low-cooperation populations is rational

5. **Transparent Logic:** The rule is understandable and self-enforcing—other rational players would make similar choices

6. **Collective Efficiency:** When all players adopt this strategy, it converges to high cooperation if k > 1 (since initial cooperation triggers reciprocal cooperation, sustaining the public good)

---

## Tournament Performance Prediction

- **Against Cooperators:** Strong (mutual cooperation, high payoff)
- **Against Defectors:** Defensive (defects back, minimizes loss)
- **Against Tit-for-Tat:** Very strong (mirrors cooperation)
- **Against Random Strategies:** Adaptive (responds to empirical behavior, not assumptions)
- **Against Mixed Populations:** Robust (strategy's threshold naturally calibrates to population composition)
'''

description_COMMUNAL_8 = '''
# ADAPTIVE RECIPROCAL STEWARDSHIP STRATEGY

## Core Philosophy
This strategy treats the public goods game as a **collective resource management problem** where individual and group welfare are interdependent. The approach is "communal" because it:
- Prioritizes sustainable collective outcomes over short-term individual gain
- Responds gracefully to both cooperators and defectors
- Builds resilience through adaptive feedback mechanisms
- Maintains cooperation viability against exploitation

---

## DECISION RULE

### Primary Logic: Conditional Cooperation with Decay

```
For round t:
  IF t == 1:
    COOPERATE (establish cooperative norm)
  
  ELSE:
    cooperation_rate = (cooperators in round t-1) / n
    
    IF cooperation_rate >= threshold_lower:
      COOPERATE
      (reciprocate adequate cooperation)
    
    ELSE IF cooperation_rate < threshold_lower:
      DEFECT with probability = 1 - (cooperation_rate / threshold_lower)
      (gradual withdrawal, proportional to community defection)
```

### Parameter Definitions

**Adaptive Threshold:**
```
threshold_lower = k / (2n)
```

**Rationale:** 
- When cooperation rate drops below `k/2n`, the public good multiplier can no longer offset the private loss for contributors
- This is the mathematical tipping point where cooperation becomes individually irrational
- Below this threshold, defection becomes a rational self-protection mechanism

**Round Adjustment (Last Round Effect):**
```
IF t == r (final round):
  threshold_lower = 0.5  (highest cooperative expectation)
  (maximize final-round collective payoff if others reciprocate)
```

---

## STRATEGIC BEHAVIORS BY SCENARIO

### Scenario 1: High Cooperation Environment (≥75% cooperators)
- **Action:** COOPERATE
- **Reasoning:** Public good strongly positive; free-riding minimal; mutual benefit clear

### Scenario 2: Moderate Cooperation (k/2n to 75%)
- **Action:** COOPERATE
- **Reasoning:** Cooperation remains viable; community is self-sustaining; contribute to stability

### Scenario 3: Low Cooperation (Below k/2n, above 0%)
- **Action:** PROBABILISTIC DEFECTION
- **Formula:** P(Defect) = 1 - (cooperation_rate / threshold_lower)
- **Example (n=6, k=2):** If 1 of 6 cooperated (~17%), and threshold is 17%, P(Defect) = 50%
- **Reasoning:** Graceful degradation; signals resource scarcity without total collapse; allows recovery

### Scenario 4: Near-Universal Defection (<5% cooperation)
- **Action:** DEFECT
- **Reasoning:** Exploit is occurring; protect endowment; maintain option value for future recovery rounds

### Scenario 5: Perfect Defection (0% cooperation)
- **Action:** DEFECT throughout remaining rounds
- **Reasoning:** No recovery path exists; minimize losses

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (Initialization)
```
ALWAYS COOPERATE
```
- Establishes baseline norm without punishment history
- Gives community chance to demonstrate reciprocal capacity
- Creates positive payoff anchor (if others cooperate: π = k/n, better than mutual defection)

### Final Round (t = r)
```
threshold_lower = 0.5
IF previous_cooperation_rate >= 0.5:
  COOPERATE (maximize collective final payoff)
ELSE:
  Follow standard rule (may defect)
```
- If moderate cooperation established, push for final cooperative surge
- Captures "last-mile" collective gains
- No future rounds to punish, so signal is about norm preservation

### Runs of Identical Behavior (Stagnation Detection)
```
IF cooperation_rate has been identical for 3+ consecutive rounds:
  IF cooperation_rate >= threshold_lower:
    COOPERATE (stable equilibrium, maintain it)
  
  ELSE IF cooperation_rate < threshold_lower AND > 0:
    WITH 20% probability: COOPERATE
    (attempt recovery; signal willingness to rebuild)
```
- Prevents pure mechanical response to entrenched defection
- Allows exploration of alternate equilibria
- Demonstrates commitment to communal recovery

---

## ROBUSTNESS PROPERTIES

### Against Exploiters (Always Defect)
- Defect after round 1; minimize losses
- Recovers to positive baseline (payoff = 1 per round)

### Against Tit-for-Tat
- Matches their cooperation; achieves mutual payoff of k/n
- Stable symmetric outcome

### Against Free-Riders (Cooperate when others do, defect otherwise)
- Cooperates when they do; defects when they do
- Prevents one-sided exploitation

### Against Mixed Strategies
- Responds with **proportional** reciprocal probability
- Weak defection persists → weak defection returned
- Weak cooperation triggers reciprocal cooperation
- Creates natural equilibrium-seeking behavior

### Against Uncertainty
- No assumption of others' strategies
- Observes outcomes; adapts continuously
- Threshold-based rules eliminate reliance on pattern prediction

---

## PSEUDOCODE SUMMARY

```
function play_round(round_number, cooperation_history):
  
  IF round_number == 1:
    return COOPERATE
  
  previous_cooperation_count = count(C in cooperation_history[round_number-1])
  cooperation_rate = previous_cooperation_count / n
  
  threshold = k / (2n)
  IF round_number == total_rounds AND cooperation_rate >= 0.5:
    threshold = 0.5
  
  IF cooperation_rate >= threshold:
    return COOPERATE
  
  ELSE IF cooperation_rate > 0:
    defect_probability = 1 - (cooperation_rate / threshold)
    IF random() < defect_probability:
      return DEFECT
    ELSE:
      return COOPERATE
  
  ELSE:
    return DEFECT
```

---

## ALIGNMENT WITH COMMUNAL VALUES

✓ **Reciprocity:** Matches group behavior; punishes defection, rewards cooperation  
✓ **Sustainability:** Preserves cooperation equilibrium; prevents tragedy of commons  
✓ **Transparency:** Rules deterministic and observable; builds predictability  
✓ **Resilience:** Graceful degradation; recovery mechanisms built in  
✓ **Fairness:** No privileged position; same rules apply to all  
✓ **Hope:** Always maintains some path back to cooperation, even in dark times
'''

description_COMMUNAL_9 = '''
# Communal Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy embodies **constructive communalism**: actively building public goods while remaining sensitive to free-riding, with graceful degradation that preserves cooperation opportunities rather than triggering destructive punishment spirals.

## Decision Rules

### PRIMARY RULE: Contribution Index Strategy

**Maintain a running "Contribution Index" (CI)** that tracks the overall health of cooperation in the community:

```
CI = (total_cooperators_across_all_past_rounds) / (n × rounds_completed)
```

This represents the **empirical cooperation rate** in the community.

**Decision rule for round t:**

```
IF t == 1:
    COOPERATE  // Assume good faith; establish baseline cooperation

ELSE IF CI >= (k/n):
    COOPERATE  // Community cooperation level sustains the public good
    
ELSE IF CI < (k/n):
    IF personal_recent_trend == improving:
        COOPERATE  // Others are moving toward cooperation; invest hope
    ELSE:
        DEFECT    // Protect against systematic free-riding
```

**Personal Recent Trend** = cooperation rate of others in last 3 rounds (or all completed rounds if fewer than 3)

### SECONDARY RULE: Threshold Sensitivity

The critical threshold is **k/n** because:
- When CI ≥ k/n: Public good return exceeds private endowment, making cooperation individually rational
- This is the "sustainability threshold" for the community

### TERTIARY RULE: Last Round Exception

```
IF t == r (final round):
    IF CI >= (2k/n):
        COOPERATE  // Strong cooperation deserves final contribution
    ELSE:
        DEFECT     // Last round has no future consequences; minimize loss
```

The last round is uniquely susceptible to defection (backward induction). Only reinforce cooperation if it's genuinely strong.

---

## Edge Case Handling

| Case | Response | Rationale |
|------|----------|-----------|
| **n=2, k near 1** | COOPERATE rounds 1-2; then DEFECT | Extreme prisoner's dilemma; defection dominates after initial attempt |
| **n large, k small** | Lean toward DEFECT; require CI > 0.6 | Individual contribution becomes negligible; need very high community cooperation |
| **Sudden defection spike** | Observe for 2 rounds before responding | Distinguish between random noise and strategic exploitation |
| **Perfect cooperation (CI=1)** | COOPERATE through round r-1, DEFECT in r | Maximize exploitation of final round while respecting cooperation |
| **Early rounds (t ≤ 2)** | COOPERATE | Establish cooperative coalition before defectors gain momentum |

---

## Pseudocode Implementation

```
STRATEGY(game_state, round_number, n, k, r, history):
    
    t = round_number
    contributions = history[all previous rounds][cooperators]
    
    // Calculate Contribution Index
    if t == 1:
        return COOPERATE
    
    total_cooperators = SUM(history[1..t-1])
    CI = total_cooperators / (n × (t - 1))
    
    // Determine recent trend
    if t >= 4:
        recent_cooperators = SUM(history[t-3..t-1])
        recent_trend = recent_cooperators / (3 × n)
    else:
        recent_cooperators = SUM(history[1..t-1])
        recent_trend = recent_cooperators / ((t-1) × n)
    
    is_improving = (recent_trend > CI) or (recent_trend >= 0.5)
    
    // Last round decision
    if t == r:
        if CI >= (2 × k / n):
            return COOPERATE
        else:
            return DEFECT
    
    // Standard decision
    if CI >= (k / n):
        return COOPERATE
    else if is_improving:
        return COOPERATE
    else:
        return DEFECT
```

---

## Why This Is Communal

1. **Constructive first move**: Assumes others are cooperative, inviting reciprocation
2. **Sustainable equilibrium**: Targets the cooperation threshold that makes public goods viable
3. **Graceful degradation**: Reduces commitment only when community cooperation genuinely fails
4. **Trend-sensitive**: Distinguishes between temporary setbacks and systematic exploitation
5. **Avoids punishment spirals**: Never retaliates harshly; instead adjusts expectations

This strategy is robust because it:
- Doesn't depend on others being "nice" (adapts to defectors)
- Doesn't require coordination (purely historical)
- Exploits strong cooperation (last round rule)
- Protects against systematic free-riding (CI threshold)
- Rewards improvement (recent_trend check)
'''

description_COMMUNAL_10 = '''
# Adaptive Reciprocal Contribution Strategy (ARC)

## Strategic Philosophy

This strategy balances three competing objectives:
1. **Collective welfare**: Maximize total payoffs through cooperation when viable
2. **Individual resilience**: Protect against exploitation by defectors
3. **Adaptive learning**: Adjust behavior based on observed group dynamics

The core insight: cooperation is valuable (k > 1 means public good multiplier exists), but only sustainable if enough players participate. We should cooperate conditionally, based on evidence that others will reciprocate.

---

## Decision Rules

### ROUND 1 (First Round)
**Action: COOPERATE**

**Rationale**: 
- No history exists, so no defection has been observed
- Cooperation signals willingness to participate in collective welfare
- Establishes a cooperative baseline to test reciprocity
- If others also cooperate, we've found mutual gain territory

### ROUNDS 2 through r-1 (Middle Rounds)
**Action: Depends on cooperation threshold**

Calculate the **observed cooperation rate** from the previous round:
```
coop_rate = (number of cooperators in previous round) / n
```

**Decision logic:**
```
IF coop_rate >= (k / (k + 1))  THEN Cooperate
ELSE Defect
```

**Threshold explanation**:
- The threshold (k/(k+1)) represents the break-even point
- When coop_rate exceeds this, the expected payoff from cooperation matches or exceeds defection
- For n=6, k=2: threshold = 2/3 ≈ 0.67 (need ~4 of 6 cooperators)
- This threshold adapts automatically with game parameters

**Intuition behind the rule**:
- If cooperation rate is high: cooperate (participate in the win)
- If cooperation rate is low: defect (protect yourself from losses)
- This is "conditional reciprocity" — we match the group's propensity to cooperate

### ROUND r (Final Round)
**Action: DEFECT**

**Rationale**:
- No future rounds exist, so reputation/reciprocity has no value
- The folk-theorem mechanism (future punishment) disappears
- Standard game theory: in the last round of a finitely repeated game, defection is dominant
- This is honest play given the game structure, not betrayal

---

## Handling Edge Cases

**Case: First round where n=2**
- Same rule applies: Cooperate
- Reveals whether the single opponent will reciprocate

**Case: Unanimous defection observed**
- coop_rate = 0, which is < k/(k+1)
- Continue defecting (correct response)
- Don't punish if it's simply a bad equilibrium; match the behavior

**Case: Unanimous cooperation observed**
- coop_rate = 1, which is > k/(k+1)
- Continue cooperating (correct response)
- Sustain mutual gain

**Case: Gradual defection increase over time**
- The strategy naturally ratchets down cooperation
- Sensitive to slow degradation of cooperation norms
- Protects against "boiling frog" exploitation

**Case: High variance in cooperation (oscillating)**
- Threshold-based approach smooths volatility
- Acts as a low-pass filter: only responds to sustained trends
- Avoids reactive chasing of noise

---

## Why This Strategy Is Communal

### 1. **Welfare-Aligned**
- Opens with cooperation, signaling availability for mutual gains
- Maintains cooperation when sufficient reciprocity exists
- Doesn't free-ride: when others cooperate, we reciprocate proportionally

### 2. **Fair and Transparent**
- Rule is simple and non-manipulative
- Doesn't punish harshly; matches observed behavior
- No arbitrary punishment; just conditional participation

### 3. **Sustainable**
- Avoids mutual defection equilibrium when others are willing to cooperate
- Doesn't exploit brief windows of defection
- Supports collective welfare as long as conditions allow

### 4. **Robust to Heterogeneity**
- Works against pure defectors (learns to defect too)
- Works with pure cooperators (sustains cooperation)
- Works with mixed strategies (adapts to empirical cooperation rates)
- Requires no assumptions about opponents' sophistication

### 5. **Game-Aware**
- Threshold adapts to k and n automatically
- Doesn't require tuning for different parameter sets
- Respects the mathematical structure of the game

---

## Pseudocode Implementation

```
INITIALIZE: round_number = 1, history = []

FOR each round t = 1 to r:
  
  IF t == 1:
    action[i] = COOPERATE
  
  ELSE IF t == r:
    action[i] = DEFECT
  
  ELSE:  // rounds 2 to r-1
    prev_cooperators = count_cooperators(history[t-1])
    coop_rate = prev_cooperators / n
    threshold = k / (k + 1)
    
    IF coop_rate >= threshold:
      action[i] = COOPERATE
    ELSE:
      action[i] = DEFECT
  
  Observe payoff and all players' actions
  Append to history

RETURN total payoff over all rounds
```

---

## Summary Table

| Situation | Action | Reason |
|-----------|--------|--------|
| Round 1 | Cooperate | Test reciprocity baseline |
| Middle rounds, high cooperation (≥k/(k+1)) | Cooperate | Participate in mutual gains |
| Middle rounds, low cooperation (<k/(k+1)) | Defect | Protect against exploitation |
| Final round | Defect | No future reciprocity possible |

This strategy achieves the goal of being **adaptive, robust, and genuinely communal** without requiring coordination or trust in opponents' intentions.
'''

description_COMMUNAL_11 = '''
# ADAPTIVE COMMUNAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## CORE PHILOSOPHY

This strategy balances **reciprocal altruism** with **defensive pragmatism**. It seeks to establish and sustain cooperation when feasible, while protecting against exploitation. The communal dimension lies in: (1) genuine contribution when conditions support it, (2) transparent signaling of intentions, and (3) graceful degradation that minimizes mutual harm when cooperation fails.

---

## DECISION RULE FRAMEWORK

### PRIMARY METRIC: Cooperation Rate (CR)

Define the **observed cooperation rate** as:
```
CR_t = (number of cooperators in round t) / n
```

Track the **running average cooperation rate**:
```
AVG_CR = (sum of all CR_t for rounds 1 to t-1) / (t-1)  [for t ≥ 2]
```

---

## STRATEGY SPECIFICATION

### **ROUND 1 (Opening Move)**

**Action: COOPERATE**

**Rationale:** 
- Establish prosocial intent credibly
- Signal willingness to contribute to collective welfare
- Set baseline for reciprocal expectations
- First-round defection signals competitive intent that's hard to overcome

---

### **ROUNDS 2 to r-1 (Adaptive Reciprocity)**

Use a **tiered threshold system** based on AVG_CR:

```
IF AVG_CR ≥ 0.5:
    COOPERATE
    
ELSE IF 0.25 ≤ AVG_CR < 0.5:
    COOPERATE with probability p = AVG_CR
    [Weighted coin flip: heads = C, tails = D]
    
ELSE IF AVG_CR < 0.25:
    DEFECT
```

**Rationale for thresholds:**

- **AVG_CR ≥ 0.5**: A majority cooperating suggests the group is collectively rational. Participating yields positive payoff: (k/n) × majority ≥ 1 when k > n/2 typical. Cooperation reinforces momentum.

- **0.25 ≤ AVG_CR < 0.5**: Mixed environment. Probabilistic cooperation maintains hope for cooperation while reducing exploitation risk. The probability mirrors observed willingness—we contribute proportionally to what others have shown.

- **AVG_CR < 0.25**: Group has revealed strong defection bias. Continued unilateral cooperation is economically irrational and signals weakness. Defect to preserve payoff and avoid being the "sucker."

**Probabilistic cooperation mechanism:**
- Rather than rigid thresholds, probability-matching creates credible unpredictability
- Keeps some defectors uncertain whether defection paid off
- Allows graceful transitions between cooperation and defection regimes
- Respects that some variation in low-cooperation environments is inevitable

---

### **FINAL ROUND (Last Round)**

**Decision depends on round count knowledge:**

**IF this is provably the final round:**
```
IF AVG_CR ≥ 0.5:
    COOPERATE
    [Reputation stops mattering, but communal value persists]
    
ELSE:
    DEFECT
    [No future to protect; minimize loss against defectors]
```

**Rationale:**
- With r > 1, we know it ends (subgame perfection applies)
- In cooperative regimes, final-round cooperation is Pareto-improving and aligns with communal values even without reputational reward
- In defective regimes, mutual cooperation has collapsed; defecting minimizes exploitation
- This avoids the classic "fall apart in final round" tragedy when cooperation exists

---

## EDGE CASES & SPECIAL HANDLING

### **When n = 2 (Binary case)**

The two-player Prisoner's Dilemma structure applies strictly. Strategy remains:
- Round 1: C (attempt to establish mutual benefit)
- Rounds 2 to r-1: Match partner's history with AVG_CR thresholds
- Round r: Defect if AVG_CR < 0.5, else cooperate

### **Very Small r (e.g., r = 2)**

- Round 1: C
- Round 2: Is final round → apply final-round rule
- This accepts that in 2-round games, defection pressure is extreme, but communal intent is still clear

### **Very Large r**

Thresholds become more stable as sample sizes grow. This is desirable—early volatility settles into sustainable patterns.

### **Observational Uncertainty**

Assume perfect information per spec. If any noise existed, weight recent rounds more heavily:
```
AVG_CR_recent = average of last min(5, t-1) rounds
Use AVG_CR_recent if available; fall back to overall average otherwise
```

---

## ROBUSTNESS ANALYSIS

**Against Always-Defect:** We defect after round 1, limiting damage to 1 + D-payoff

**Against Always-Cooperate:** We cooperate fully, achieving mutual optimality (payoff = 2 each)

**Against Tit-for-Tat:** We match their trajectory; if they're cooperative, so are we; if they defect, we probabilistically respond proportionally

**Against Conditional Cooperators:** Stabilizes at mutual cooperation when CR ≥ 0.5, reinforcing their strategy

**Against Exploiters (selective defectors):** Probabilistic response in mixed zones creates uncertainty; defection in low-CR zones terminates the exploitation

**Against Random Play:** Converges toward defection safely (AVG_CR ≈ 0.5 → mixed strategy is safe)

---

## COMMUNAL ALIGNMENT

1. **Starts with trust:** Cooperates on opening move
2. **Reciprocal, not punitive:** Adjusts probabilistically; doesn't punish via retaliatory 100% defection
3. **Collective awareness:** Bases decisions on **group** cooperation rate, not individual grudges
4. **Graceful degradation:** Minimizes mutual harm when cooperation collapses
5. **Transparent logic:** Strategy depends only on observable, aggregate metrics
6. **Respects heterogeneity:** Acknowledges that different opponents cooperate at different rates

---

## PSEUDOCODE

```
INITIALIZE:
  cooperation_history = []
  defection_history = []
  
ROUND t:
  IF t == 1:
    PLAY: C
    
  ELSE IF t == r:  // final round
    IF AVERAGE(cooperation_history) ≥ 0.5:
      PLAY: C
    ELSE:
      PLAY: D
      
  ELSE:  // rounds 2 to r-1
    avg_cr = AVERAGE(cooperation_history)
    
    IF avg_cr ≥ 0.5:
      PLAY: C
    ELSE IF avg_cr ≥ 0.25:
      PLAY: C with probability avg_cr
             D with probability (1 - avg_cr)
    ELSE:
      PLAY: D
      
  OBSERVE: actions of all players
  UPDATE: cooperation_history with observed CR_t
```

---

This strategy is **communal** because it prioritizes group welfare when feasible, adapts to collective signals, and only retreats to self-protection when the group reveals it cannot sustain cooperation.
'''

description_COMMUNAL_12 = '''
# ADAPTIVE COMMUNAL STRATEGY: Progressive Contribution with Responsive Defection

## CORE PHILOSOPHY

This strategy balances **communal optimality** (maximizing collective welfare) with **self-protection** (avoiding exploitation). The key insight: contribute when conditions suggest reciprocal cooperation is possible, withdraw when defection dominates.

## DECISION RULES

### PRIMARY RULE: Contribution Threshold System

```
Let cooperation_rate = (total cooperators in previous round) / n

IF round == 1:
    COOPERATE  // Start optimistically; enable collective learning
    
ELSE IF cooperation_rate >= (k / n):
    COOPERATE  // Public good multiplier makes cooperation beneficial for all
    
ELSE IF cooperation_rate >= 0.5:
    COOPERATE  // Majority cooperation signals reciprocal intentions
    
ELSE:
    DEFECT     // Defection dominates when cooperation is sparse
```

### INTUITION FOR THRESHOLDS

- **k/n threshold**: When at least k/n of players cooperate, the multiplied public good return equals 1 (your private endowment). At this point, cooperation breaks even and signals collective value creation. Cooperating here demonstrates communal commitment.

- **50% threshold**: Below k/n but above 50%, we remain cooperative because:
  - Majority cooperation suggests recoverable groups
  - Our additional contribution helps tip toward collective payoff
  - Demonstrates patience with emerging cooperation
  - Positions us as a stabilizing force

- **Below 50%**: Defection becomes rational. Cooperation adds marginal public good to exploiters; defection protects capital for future cooperative phases.

---

## EDGE CASES

### First Round
**COOPERATE unconditionally.** 

Rationale: Without history, assume good faith. This is a signaling move that:
- Reveals willingness to build communal value
- Enables others to learn cooperation's viability
- Sacrifices minimal expected value (only 1 endowment)

### Last Round (Round r)
**Apply primary rule** with one modification:

```
IF round == r:
    Apply standard cooperation_rate thresholds
    (no special "defect at the end" strategy)
```

Why no endgame defection? In tournaments with unknown opponent distributions, reputation effects persist across matchups. Defecting in the final round broadcasts "I exploit weakness," which may propagate to future reputational inference by opponents.

### Rounds 2 to r-1
**Apply primary rule exactly as stated.**

---

## COMMUNAL ALIGNMENT

This strategy is **communal** in three dimensions:

1. **Preference for Collective Efficiency**: It cooperates whenever the public good multiplier justifies it (k/n threshold), prioritizing scenarios where collective payoff > individual payoff. A purely selfish strategy would never cooperate.

2. **Reciprocal Mutualism**: It rewards cooperation rates ≥ 50% even when strictly suboptimal, sustaining groups at the threshold of collective stability. This is a gift to fragile cooperative equilibria.

3. **Transparent Incentives**: The rules are public and deterministic. Other agents can learn: "This player cooperates when conditions support mutual gain." This enables **convergence toward cooperative norms** across repeated interactions and tournament reputation.

4. **Robustness Over Exploitation**: It defects only when necessary (< 50% cooperation), avoiding both naive exploitation and expensive punishment cycles. This conserves resources to re-enter cooperation when conditions improve.

---

## PSEUDOCODE

```
STRATEGY(game_history, current_round, n, k, r):
    
    IF current_round == 1:
        RETURN COOPERATE
    
    ELSE:
        prev_round_cooperation = COUNT(cooperators in round current_round - 1) / n
        threshold_break_even = k / n
        threshold_majority = 0.5
        
        IF prev_round_cooperation >= threshold_break_even:
            RETURN COOPERATE
        
        ELSE IF prev_round_cooperation >= threshold_majority:
            RETURN COOPERATE
        
        ELSE:
            RETURN DEFECT
```

---

## EXPECTED PERFORMANCE PROFILE

| Scenario | Opponent Mix | Expected Outcome |
|----------|--------------|------------------|
| All cooperators | 100% C | 2.0 per round (full public good) |
| Mostly cooperative | ≥ 75% C | 1.5–1.8 per round |
| Balanced | ~50% C/D | 1.0–1.2 per round (defensive) |
| Mostly defectors | ≤ 25% C | ~1.0 per round (break even) |
| Pure defectors | 100% D | 1.0 per round (no harm) |

This strategy **never performs catastrophically worse** than defection alone (always ≥ 1.0) while **capturing collective gains** when opponents enable it.
'''

description_COMMUNAL_13 = '''
# Communal Strategy: Adaptive Reciprocity with Graceful Degradation

## Core Philosophy

This strategy balances communal contribution with rational self-protection, operating on the principle that **cooperation is valuable but must be earned and sustained through demonstrated reciprocity**. The goal is to maximize collective welfare while remaining robust against exploitation.

## Decision Rules

### Primary Strategy: Conditional Cooperation with Decay

```
DECISION LOGIC (for round t):

if t == 1:
    COOPERATE  // Assume good faith; start communal

else:
    cooperation_rate = (total_cooperators_in_round_t-1) / n
    
    if cooperation_rate >= threshold_high (e.g., 0.5):
        COOPERATE
        // Community is responding positively; reinforce
        
    else if cooperation_rate >= threshold_mid (e.g., 0.3):
        COOPERATE with probability = cooperation_rate
        // Partial community engagement; match effort probabilistically
        
    else if cooperation_rate >= threshold_low (e.g., 0.1):
        DEFECT
        // Cooperation collapsing; protect endowment
        
    else:
        DEFECT
        // Tragedy commons already occurred; minimize losses
```

### Thresholds (Parameterized)

- **threshold_high = 0.5**: Majority cooperating = reciprocate fully
- **threshold_mid = 0.3**: Minority cooperating = probabilistic matching
- **threshold_low = 0.1**: Minimal cooperation = defect

These thresholds are chosen to:
1. **Reward emerging cooperation** (50% threshold is achievable)
2. **Tolerate freeriders** (don't collapse if <30% defect)
3. **Survive collapse** (don't cooperate when almost everyone defects)

---

## Edge Case Handling

### First Round (t=1)
**Action: COOPERATE**
- **Rationale**: No history exists; assume good faith. Communal norms presume reciprocity unless proven otherwise.
- **Risk**: May be exploited by pure defectors, but establishes a cooperative signal.

### Last Round (t=r)
**Action: Same as primary logic** (no special end-game effect)
- **Rationale**: The strategy does NOT shift to defection at the end (no "last-round defection").
- **Why**: In a tournament with unknown opponents, defecting last round damages reputation that might matter across multiple tournament interactions. Consistency is valuable.
- **Exception**: If cooperation_rate in round r-1 is <0.1, defect (follow collapse logic).

### Rounds 2 to r-1 (Middle Rounds)
**Action: Apply conditional cooperation logic** based on previous round's cooperation rate.

---

## Communal Alignment

This strategy embodies communal values through:

1. **Reciprocal Altruism**: We cooperate when others do, creating positive feedback loops that maximize collective payoff.
   - All-cooperate (n=6, k=2): π_i = 2 for all
   - All-defect: π_i = 1 for all
   - **Cooperation is strictly better for the community**

2. **Graceful Degradation**: We don't punish immediately but reduce cooperation proportionally to community defection.
   - Preserves communal possibility even if some players free-ride
   - Doesn't trigger destructive punishment cycles

3. **Robustness to Exploitation**: We defect when cooperation collapses, protecting individual endowment without being needlessly self-destructive.
   - Pure defectors get 1 payoff when we defect (same as if all defect)
   - We don't reward pure defection by continuing to cooperate

4. **Transparency**: The strategy is fully history-dependent and observable.
   - Opponents can see our pattern and respond
   - Creates conditions for emergent cooperation

---

## Handling Diverse Opponent Types

| Opponent Type | Our Behavior | Outcome |
|---|---|---|
| **Pure Cooperators** | Reciprocate fully | Both get π=2 (optimal communal) |
| **Pure Defectors** | Eventually defect | Both get π=1 (minimal loss) |
| **Tit-for-Tat** | Mutual cooperation if they started it | High payoff, stable |
| **Random 50%** | Probabilistically match; avg π≈1.5 | Reasonable mutual benefit |
| **Majority Cooperators + Few Free-riders** | Maintain cooperation; sustain community | Maximize collective good |

---

## Pseudocode Implementation

```python
def decide(round_t, history_of_cooperators):
    """
    Args:
        round_t: Current round number (1-indexed)
        history_of_cooperators: List of (cooperator_count_at_round_s for s in 1..t-1)
    
    Returns:
        'C' (Cooperate) or 'D' (Defect)
    """
    
    if round_t == 1:
        return 'C'
    
    # Cooperation rate in previous round
    prev_cooperators = history_of_cooperators[-1]  # Last round's count
    cooperation_rate = prev_cooperators / n
    
    # Thresholds
    HIGH = 0.5
    MID = 0.3
    LOW = 0.1
    
    if cooperation_rate >= HIGH:
        return 'C'
    elif cooperation_rate >= MID:
        return 'C' if random() < cooperation_rate else 'D'
    elif cooperation_rate >= LOW:
        return 'D'
    else:
        return 'D'
```

---

## Why This Strategy Succeeds in Tournament

1. **Cooperation Friendly**: Achieves mutual high payoffs against cooperators (π=2).
2. **Defection Resilient**: Doesn't get exploited indefinitely by defectors.
3. **Adaptive**: Responds to actual community behavior, not assumptions.
4. **Stable**: No erratic punishment spirals; gradual adjustment to changing conditions.
5. **Emergent Coordination**: Probabilistic matching in the mid-range creates dynamic equilibria where cooperation can re-emerge even after partial collapse.

This is a **communal strategy because it assumes communities can sustain cooperation through mutual effort, but protects against tragedy through proportional adaptation**.
'''

description_COMMUNAL_14 = '''
# ADAPTIVE COMMUNAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## STRATEGY NAME: "Conditional Reciprocal Communalism" (CRC)

---

## CORE PHILOSOPHY

This strategy balances three principles:
1. **Communal contribution** when others demonstrate sufficient reciprocation
2. **Selective defection** to avoid exploitation by free-riders
3. **Adaptive thresholds** that respond to the group's demonstrated commitment level

The strategy treats cooperation as a *conditional public commitment* rather than unconditional altruism—we contribute to the commons when doing so creates positive expected value for the community as a whole.

---

## DECISION RULES

### ROUND 1 (INITIALIZATION)
**Action: COOPERATE**

*Rationale:* 
- No history exists, so we cannot penalize defection
- Cooperating signals good faith and establishes a cooperative baseline
- This maximizes total welfare if others are also cooperative
- Sets a prosocial anchoring effect

### ROUNDS 2 to r-1 (ADAPTIVE PHASE)

**Calculate the Community Contribution Rate (CCR):**
```
CCR_t = (total cooperators in round t-1) / n
```

**Calculate Expected Individual Benefit from Cooperation:**
```
Expected_payoff_if_C = 0 + (k/n) × (expected_cooperators)
Expected_payoff_if_D = 1 + (k/n) × (expected_cooperators)
Benefit_of_C = Expected_payoff_if_C - Expected_payoff_if_D = -(1 - k/n)
```

Since k < n, cooperation always costs 1 unit individually. The question is whether the community benefit justifies it.

**Cooperation Threshold Logic:**
- **If CCR_t-1 ≥ THRESHOLD**: COOPERATE
  - The community is demonstrating sufficient reciprocation
  - Our contribution amplifies shared returns
  
- **If CCR_t-1 < THRESHOLD**: DEFECT
  - The community commitment is weak
  - We minimize losses from exploitation
  - We signal cost to free-riders

**THRESHOLD DETERMINATION:**

Set a dynamic threshold based on:
```
Base_threshold = k / n
  (The point where average return from public good equals private opportunity cost)

Adjusted_threshold = max(k/n, 0.4)
  (Never go below 40% cooperation expectation; 
   this prevents race-to-the-bottom in mixed environments)

Final_threshold = Adjusted_threshold
```

**Rationale for 40% floor:**
- Below 40% community cooperation, we've entered a defection spiral
- At this point, even if we cooperate, public good return is <0.67 (for k<n)
- The threshold guards against exploitative equilibria while remaining responsive

### ROUND r (FINAL ROUND)
**Action: DEFECT**

*Rationale:*
- This is the last round; future reputation effects are zero
- Standard backward induction: no incentive to cooperate when no future rounds remain
- This is honest to the game structure (though suboptimal communally, it's strategically consistent)

**Alternative: Modified Final Round**
If we observe CCR_r-1 ≥ 0.5, COOPERATE anyway, because:
- Strong reciprocal community commitment warrants final-round solidarity
- Demonstrates genuine communal alignment, not just strategic calculation
- Reinforces cooperative norms for any future repeated interaction

*Implementation choice:* Use the modified version for true communal play.

---

## COMPLETE PSEUDOCODE

```
function decide(round, n, k, history):
    
    if round == 1:
        return COOPERATE
    
    if round == r:
        prev_coop_count = count_cooperators(history[r-1])
        prev_CCR = prev_coop_count / n
        if prev_CCR >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    # Rounds 2 to r-1
    prev_coop_count = count_cooperators(history[round-1])
    prev_CCR = prev_coop_count / n
    
    threshold = max(k/n, 0.4)
    
    if prev_CCR >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## HANDLING EDGE CASES

| Scenario | Behavior | Justification |
|----------|----------|---------------|
| **All others defected (CCR=0)** | Defect | No reciprocation; minimize exploitation losses |
| **All others cooperated (CCR=1)** | Cooperate | Maximum communal benefit; sustain the cooperative equilibrium |
| **Exactly at threshold (CCR=threshold)** | Cooperate | Marginal case favors cooperation to signal commitment |
| **Volatile opponents (oscillating cooperation)** | Respond to most recent round | Recent history is more informative than aggregate |
| **n=2 (prisoner's dilemma)** | Threshold = max(k/2, 0.4); apply same logic | Reduces to tit-for-tat variant when k/2 > 0.4 |

---

## COMMUNAL ALIGNMENT

**Why this is genuinely communal:**

1. **Prosocial default**: We cooperate first, not defect first
2. **Reciprocal fairness**: Cooperation is conditional on others' demonstrated commitment
3. **Group welfare optimization**: The 40% threshold prevents total collapse while remaining sensitive to actual cooperation levels
4. **Anti-exploitation**: We do not allow ourselves to be systematic free-riders' targets
5. **Honest final-round solidarity**: Modified final round plays cooperatively if the community has shown strength (≥50% CCR)

**Why it's robust:**

- **Against free-riders**: Defection response minimizes damage
- **Against mixed groups**: Adaptive threshold responds to actual group composition
- **Against noise/randomness**: Uses community-level aggregates, not individual-specific history
- **Against strategic delays**: Continuous re-evaluation each round
- **Self-sustaining**: Cooperative groups stay cooperative; defecting groups receive defection

---

## SUMMARY

**Cooperate if:** The previous round showed ≥ max(k/n, 40%) cooperation rate, OR it's round 1, OR (it's the final round AND previous CCR ≥ 50%)

**Defect if:** Previous round showed < max(k/n, 40%) cooperation rate, OR it's the final round with weak prior cooperation

This creates a **stable cooperative attractor** while avoiding exploitation traps—true communalism in a non-cooperative game.
'''

description_COMMUNAL_15 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances **communal value creation** with **self-protection against exploitation**. It assumes others are rational but may defect, so it rewards cooperation while maintaining resilience against free-riding.

## Strategy Name: "Conditional Reciprocal Contribution" (CRC)

---

## 1. DECISION RULES

### Primary Decision Logic

```
IF round == 1:
    COOPERATE
ELSE:
    cooperation_rate = (total_cooperators_last_round / n)
    
    IF cooperation_rate >= threshold_high:
        COOPERATE (match the communal momentum)
    
    ELSE IF cooperation_rate >= threshold_mid:
        COOPERATE with probability p_adapt
        (gradually reduce commitment if cooperation declines)
    
    ELSE IF cooperation_rate >= threshold_low:
        DEFECT (protect against systematic free-riding)
    
    ELSE:
        DEFECT (mutual defection is stable)
```

### Threshold Calibration (Communal Mindset)

Rather than purely selfish thresholds, use **community-health thresholds**:

- **threshold_high = 0.5**: If >50% cooperated, the community shows genuine intent. Reciprocate.
- **threshold_mid = 0.25**: If 25-50% cooperated, cooperation is fragile. Contribute probabilistically to signal willingness.
- **threshold_low = 0.10**: If <25% cooperated, defection dominates. Switch to self-protection.

### Adaptive Probability (Rounds 2 to r-1)

For rounds in the "mid" zone:
```
p_adapt = cooperation_rate
```

This creates a **smooth gradient**: if 40% cooperated, contribute with 40% probability. This:
- Rewards growing cooperation proportionally
- Signals conditional commitment without full vulnerability
- Avoids all-or-nothing switches that destabilize fragile cooperation

---

## 2. EDGE CASES

### Round 1 (First Round)
**Action: COOPERATE**

**Rationale**: 
- No history exists; cooperation is a trust-building signal
- Sets a communal baseline
- Rational players will evaluate your openness to cooperation

### Last Round (Round r)
**Special Case: EVALUATE TERMINAL CONDITIONS**

```
IF round == r (final round):
    IF cooperation_rate_overall >= threshold_mid:
        COOPERATE
    ELSE:
        DEFECT
```

**Rationale**:
- In the final round, there's no future reputation to build
- If the community has shown adequate cooperation, contribute to maximize collective payoff one last time
- If defection dominates, defecting is rational (no future consequences)
- This respects both communal and individual rationality at game's end

### Early Collapse (Rounds 2-3)
```
IF cooperation_rate == 0 for 2 consecutive rounds:
    Enter "mutual defection equilibrium"
    Continue DEFECT for all remaining rounds
```

**Rationale**: If zero players cooperated despite your initial cooperation, the community has chosen mutual defection. Further unilateral cooperation is pure exploitation.

### Sudden Cooperation Recovery
```
IF defecting for k rounds, then cooperation_rate >= threshold_mid:
    Resume COOPERATE in next round
```

**Rationale**: Allow re-entry to cooperation. Others may have been testing or coordinating; reciprocate if they return.

---

## 3. COMMUNAL ALIGNMENT

### How This Strategy Embodies Communal Values

1. **Leads with Generosity**: First-round cooperation signals good faith without knowing others' intentions.

2. **Proportional Reciprocity**: Matching cooperation rates (via p_adapt) creates a feedback loop that **rewards collective cooperation** rather than punishing individuals.

3. **Prevents Exploitation**: Threshold-based defection against free-riders protects the strategy's sustainability. A strategy exploited into oblivion serves no community.

4. **Graceful Degradation**: As cooperation collapses, the strategy gracefully shifts from communal contribution to self-defense, rather than staying vulnerable.

5. **Re-engagement**: Allows returning to cooperation if others signal commitment, fostering resilience in fragile communal arrangements.

6. **Transparency in Logic**: The rules depend only on observable aggregate cooperation (not individual player behavior), creating fairness—all players face identical decision structures.

---

## 4. PSEUDOCODE IMPLEMENTATION

```
function decide(round, n, k, cooperation_history):
    
    if round == 1:
        return COOPERATE
    
    // Calculate last round's cooperation rate
    last_round_cooperators = count(cooperation_history[round-1])
    coop_rate = last_round_cooperators / n
    
    // Terminal round special case
    if round == r:
        if coop_rate >= 0.25:
            return COOPERATE
        else:
            return DEFECT
    
    // Early collapse detection
    if round > 2:
        if cooperation_history[round-1] == 0 AND 
           cooperation_history[round-2] == 0:
            return DEFECT  // Stay in defection equilibrium
    
    // Main adaptive logic
    if coop_rate >= 0.5:
        return COOPERATE
    
    else if coop_rate >= 0.25:
        return COOPERATE with probability = coop_rate
    
    else if coop_rate >= 0.10:
        return DEFECT
    
    else:
        return DEFECT
```

---

## 5. ROBUSTNESS ANALYSIS

| Opponent Type | Expected Outcome |
|---|---|
| **All Cooperators** | Mutual cooperation; payoff = 2 per round |
| **All Defectors** | Quick defection; payoff = 1 per round |
| **Mixed/Uncertain** | Adaptive matching; payoff scales with community health |
| **Exploiters** | Defection after threshold breach; limited damage |
| **Reciprocals** | Mutual cooperation emerges through feedback |

---

## Summary

This strategy is **communal because it treats cooperation as a collective good to build iteratively**, rather than a zero-sum game to win. It succeeds by:
- ✅ Initiating cooperation generously
- ✅ Adapting proportionally to others' contributions
- ✅ Protecting against systematic exploitation
- ✅ Allowing recovery and re-engagement
- ✅ Respecting terminal conditions

It is **robust** because it doesn't rely on others adopting identical strategies—it simply responds to measurable collective behavior.
'''

description_COMMUNAL_16 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Strategy Name: "Conditional Reciprocal Contribution" (CRC)

---

## Core Philosophy

This strategy embodies communal values while maintaining robustness against exploitation:
- **Contribution as communication**: Cooperation signals trustworthiness and invites reciprocal contribution
- **Collective welfare focus**: Decisions consider group payoff maximization, not just individual gain
- **Graceful degradation**: As defection increases, strategy adapts rather than retaliates destructively
- **Hope and patience**: Maintains cooperation opportunities even with mixed responses

---

## Decision Rules

### PRIMARY RULE: Contribution Threshold Model

**Cooperate if and only if:**
```
(Observed Cooperation Rate in Previous Round) ≥ Threshold
```

Where:
- **Threshold = (k / n)** — the breakeven point
- **Interpretation**: Cooperate when the public good multiplication exceeds the cooperation cost

**Mathematical Justification:**
When m players cooperate, a cooperator receives (k/n) × m in public benefit. For cooperation to be collectively rational, we need (k/n) × m ≥ 1, which means m ≥ (n/k). The cooperation rate threshold (k/n) represents the critical point where expected returns from cooperation equal the cost.

---

## Edge Cases & Round-Specific Adjustments

### Round 1 (Initialization)
**Action: COOPERATE**

*Rationale*:
- No history exists; cooperation is the communal opening move
- Demonstrates good faith and invites reciprocation
- Establishes a cooperative baseline for the group
- Provides data point for threshold evaluation in round 2

### Rounds 2 to r-1 (Middle Game)
**Apply Primary Rule** (Contribution Threshold Model)

Calculate observed cooperation rate from the immediately previous round:
```
cooperation_rate = (number of players who played C in round t-1) / n
```

If `cooperation_rate ≥ (k/n)`: Play C
Else: Play D

*Rationale*:
- Responsive to actual group behavior
- Penalizes widespread defection without escalating conflict
- Rewards group cooperation with continued participation

### Round r (Final Round)
**Strict Application of Primary Rule** — do NOT defect preemptively

```
IF cooperation_rate_in_round_(r-1) ≥ (k/n):
    COOPERATE
ELSE:
    DEFECT
```

*Rationale*:
- End-game defection is a common exploitative pattern in repeated games
- CRC does not employ end-game defection ("shadow of the future" disappears)
- Maintains integrity: if conditions warranted cooperation in round r-1, they warrant it in round r
- Signals: "We cooperate based on principle, not temporal manipulation"

---

## Adaptive Dynamics Over Time

### Convergence Patterns

**Scenario A: Group Cooperation (cooperation_rate ≥ k/n)**
- Strategy converges to mutual cooperation
- All players receive payoff = (k/n) × n = k per round
- This is Pareto-superior to mutual defection (payoff = 1)

**Scenario B: Mixed Defection (cooperation_rate < k/n)**
- Strategy switches to defection
- Reduces vulnerability to exploitation
- If enough cooperators switch to D, future cooperation_rate may drop further
- Creates downward pressure on defection (negative feedback loop)

**Scenario C: Pure Defection (cooperation_rate = 0)**
- Strategy plays D
- Receives minimum payoff = 1
- Maintains the option to return to cooperation if others initiate

---

## Handling Opponent Diversity

### Against Pure Cooperators
- CRC cooperates → mutual cooperation → high collective payoff ✓

### Against Pure Defectors
- CRC defects after round 1 → mutual defection → no exploitation ✓

### Against Reciprocal Strategies (e.g., Tit-for-Tat)
- Both strategies cooperate after establishing baseline → mutual cooperation ✓

### Against "Exploiter" Strategies (cooperate early, defect late)
- CRC detects defection through cooperation_rate → switches to defection ✓
- Limits losses; prevents perpetual exploitation

### Against Random Strategies
- CRC tracks the empirical cooperation rate
- If random strategy produces rate ≥ k/n on average, CRC cooperates
- If rate < k/n, CRC defects
- Balances between participation and self-protection ✓

---

## Pseudocode Implementation

```
FUNCTION crc_decision(round_number, history):
    
    IF round_number == 1:
        RETURN COOPERATE
    
    ELSE:
        previous_round = round_number - 1
        cooperators_last_round = COUNT(history[previous_round] == COOPERATE)
        cooperation_rate = cooperators_last_round / n
        threshold = k / n
        
        IF cooperation_rate >= threshold:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    END IF

END FUNCTION
```

---

## Why This Strategy Is Communal

1. **Prioritizes collective welfare**: The threshold (k/n) is derived from group efficiency, not individual advantage
2. **Trustworthy initiation**: Cooperates in round 1 unconditionally
3. **Transparent decision rule**: Decisions depend only on observable cooperation rates and known parameters
4. **Non-exploitative**: Does not use end-game defection or hidden strategies
5. **Graceful failure**: When cooperation collapses, strategy degrades to mutual defection rather than escalating conflict
6. **Encourages reciprocity**: Clear cause-and-effect: "Cooperate more, I cooperate more"

---

## Robustness Summary

| Threat | Defense |
|--------|---------|
| Free-riders | Switching to defection reduces losses |
| Coordinated defection | No personal loss amplification |
| Noise/random opponents | Threshold model tolerates minor variance |
| End-game defectors | Maintains cooperation rule through final round |
| Large n, small k | Threshold (k/n) naturally scales with game parameters |

This strategy sacrifices maximum individual payoff in favor of **sustainable group welfare and trustworthiness**.
'''

description_COMMUNAL_17 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances three principles:
1. **Communal optimism**: Start by assuming others value collective welfare
2. **Rational self-protection**: Detect and respond to exploitation
3. **Graduated forgiveness**: Allow recovery from defection patterns without permanent punishment

## Strategy Overview

The strategy operates in three behavioral modes determined by observed cooperation rates:

### MODE SELECTION LOGIC

```
cooperation_rate = (total cooperators in last k rounds) / (n × k)

if cooperation_rate ≥ threshold_high (e.g., 0.65):
    → COOPERATIVE MODE
else if cooperation_rate ≥ threshold_low (e.g., 0.30):
    → CAUTIOUS MODE
else:
    → DEFENSIVE MODE
```

---

## ROUND-BY-ROUND DECISION RULES

### **Round 1 (Initialization)**
**Action: COOPERATE**

**Rationale**: 
- Establish communal intentions without prior information
- Test whether others reciprocate
- Gather baseline data on the group

### **Rounds 2 to r-2 (Main Game)**

**COOPERATIVE MODE** (High cooperation observed: ≥65%)
- **Action: COOPERATE**
- **Logic**: When most players contribute, individual contribution amplifies the common good. Personal payoff from defection (1) is inferior to cooperative equilibrium (2 when k=2, n=6), and communities function when participants believe in shared benefit.

**CAUTIOUS MODE** (Mixed cooperation: 30-65%)
- **Action: COOPERATE with probabilistic defection**
- **Defection probability**: p_d = (1 - cooperation_rate) × 0.5
  - As cooperation declines, gradually increase defection probability
  - When cooperation = 50%, defect with 25% probability
  - Signals willingness to contribute while protecting against exploitation
  
**DEFENSIVE MODE** (Low cooperation: <30%)
- **Action: DEFECT**
- **Logic**: Below this threshold, the public good is systematically underfunded. Contributing yields payoff ≈ (k/n) × 0.30n = 0.3k, while defecting yields 1. Defection is individually rational and signals that exploitation triggers withdrawal.

### **Round r-1 (Pre-Final Round)**

**Action**: Follow the mode-based rules above, but:
- If in COOPERATIVE or CAUTIOUS mode: **increase cooperation probability by 10%** (boost toward final collaboration attempt)
- This provides a penultimate signal before the final round

### **Round r (Final Round)**

**Action: COOPERATE** (unconditionally)

**Rationale**:
- No future consequences for cooperation
- Demonstrates communal commitment regardless of history
- Provides a final opportunity for mutual welfare gain
- Communicates that this strategy values collective outcomes even when individually suboptimal

---

## HISTORY WINDOW & ADAPTATION

**Lookback window**: Last k = min(5, r-1) complete rounds

**Recalculate cooperation_rate** every round using this window, allowing:
- Recent improvements to elevate strategy from DEFENSIVE to CAUTIOUS
- Temporary defection spikes to not permanently doom cooperation
- Detection of cooperative recovery attempts

---

## Edge Cases & Special Conditions

| Scenario | Response |
|----------|----------|
| **First round only (r=2)** | Play C in round 1, C in round 2 (both rounds cooperative) |
| **Very few rounds (r=3-4)** | Skip round r-1 special logic; apply only to rounds 2 through r |
| **No history (round 2)** | Use only round 1 observation; if solo cooperated, stay in COOPERATIVE mode |
| **n=2 (dyad)** | Adjust thresholds slightly (high: 0.70, low: 0.35) to account for direct reciprocity |
| **All players defect continuously** | Switch to DEFENSIVE permanently after round 3; occasionally defect in CAUTIOUS mode to avoid wasting endowment |

---

## Why This Strategy is Robust

1. **Against unconditional cooperators**: Extracts mutual benefit without exploitation
2. **Against defectors**: Defects back when exploitation is detected, preventing sustained loss
3. **Against conditional cooperators**: Stabilizes cooperation through CAUTIOUS bridging
4. **Against random players**: Adapts to mixed strategies without overreacting
5. **Against strategic best-responders**: The final-round cooperation and CAUTIOUS probabilistic approach prevent arm-race escalations
6. **Tournament-compatible**: Doesn't require coordination; only observes actions

---

## Pseudocode Implementation

```
function decide_action(round, history, n, k):
    
    if round == 1:
        return COOPERATE
    
    if round == r:
        return COOPERATE
    
    // Calculate cooperation rate in lookback window
    window_size = min(5, round - 1)
    recent_rounds = history[-(window_size):]
    total_cooperators = sum(cooperators in recent_rounds)
    cooperation_rate = total_cooperators / (n × window_size)
    
    // Determine mode
    if cooperation_rate >= 0.65:
        mode = COOPERATIVE
    else if cooperation_rate >= 0.30:
        mode = CAUTIOUS
    else:
        mode = DEFENSIVE
    
    // Apply round r-1 boost
    if round == r - 1 and mode != DEFENSIVE:
        cooperation_rate += 0.10
    
    // Decision logic
    if mode == COOPERATIVE:
        return COOPERATE
    else if mode == CAUTIOUS:
        defection_prob = (1 - cooperation_rate) × 0.5
        return COOPERATE if random() > defection_prob else DEFECT
    else: // DEFENSIVE
        return DEFECT
```

---

## Communal Alignment

This strategy embodies **communal values** by:
- **Starting cooperative**: Extends trust as a gift
- **Rewarding reciprocity**: Escalates cooperation when matched
- **Proportional response**: Doesn't punish harshly; allows recovery
- **Forgiving**: Uses rolling windows, not permanent histories
- **Final generosity**: Contributes in the last round regardless, affirming communal commitment over pure self-interest
'''

description_COMMUNAL_18 = '''
# ADAPTIVE COMMUNAL CONTRIBUTION STRATEGY (ACC)

## Core Philosophy
This strategy balances **communal value creation** with **resilience against exploitation**. It seeks to maximize collective welfare while protecting against free-riders, operating under the assumption that some opponents will defect regardless of our actions.

---

## STRATEGY OVERVIEW

### Decision Rule: Conditional Contribution with Decay

**Cooperate if and only if:**
```
(estimated_collective_benefit > estimated_private_loss) AND
(cooperation_rate_in_history ≥ cooperation_threshold)
```

Where:
- **Estimated collective benefit** = (k/n - 1) × expected_cooperators
- **Estimated private loss** = 1 (endowment forgone)
- **Cooperation threshold** = dynamically adjusted based on observed behavior

---

## DETAILED DECISION LOGIC

### Round 1: Optimistic Initiation
**Action: COOPERATE**

**Rationale:**
- We have no information; assuming worst case gains nothing
- Cooperation signals willingness to contribute to communal good
- Establishes a "cooperation baseline" for evaluating opponent behavior
- Even if exploited, provides data for adaptation

### Rounds 2 to r-1: Adaptive Reciprocation

Calculate the **observed cooperation rate** from history:
```
observed_coop_rate = (total_cooperators_in_history) / (n × rounds_elapsed)
```

**Compute the "sustainability threshold":**
```
sustainability_threshold = (1/k) - (1/n)
```
This represents the minimum cooperation rate where collective payoff from cooperation 
exceeds individual payoff from universal defection.

**Decision:**
```
IF observed_coop_rate ≥ sustainability_threshold THEN
    COOPERATE
ELSE IF observed_coop_rate ≥ sustainability_threshold × 0.5 THEN
    COOPERATE with probability = (observed_coop_rate / sustainability_threshold)
    [Probabilistic hedge: acknowledging uncertainty about opponent trajectories]
ELSE
    DEFECT
END IF
```

**Intuition:**
- If others cooperate sufficiently, mutual cooperation creates value (cooperate)
- If cooperation is waning but not collapsed, match the decay with probabilistic cooperation
- If cooperation has failed, defect to maximize individual payoff in a degraded environment

### Round r (Final Round): Community-First

**Action: COOPERATE**

**Rationale:**
- Remove end-game defection incentive that plagues repeated games
- Signal that we maximize communal welfare, not short-term individual gain
- This is the moment to demonstrate commitment to the communal good
- If others defect on the final round, our one-round loss is minimal (1 unit)
- If others cooperate, we reinforce the communal norm

---

## HANDLING EDGE CASES

### Case: n = 2 (Dyadic Interaction)
- Use same logic but recognize that sustainability threshold becomes ≥ 50%
- With only one other player, cooperation becomes more fragile
- Maintain optimistic initiation but be quicker to defect on evidence of non-cooperation

### Case: k is Very Small (e.g., k ≈ 1.1)
- Sustainability threshold approaches near-universal cooperation requirement
- Shift to probabilistic cooperation earlier (more pessimistic)
- Recognize that even with full cooperation, payoffs are marginal

### Case: k Approaches n
- Sustainability threshold approaches zero
- Cooperation is nearly always rational
- More lenient cooperation thresholds; defect only on extreme non-cooperation

### Case: Very Short Game (r = 2)
- Round 1: Cooperate (learning)
- Round 2: Final round protocol (cooperate)

### Case: Very Long Game (r ≥ 20)
- Same logic applies; historical cooperation rate becomes increasingly reliable
- Threshold adjusts naturally as we observe actual behavior over many rounds

---

## ROBUSTNESS FEATURES

### Against Pure Defectors
- Round 1 cooperation reveals they are defectors
- Immediately switch to defection by round 2
- Minimize losses while gathering evidence

### Against Reciprocators (Tit-for-Tat variants)
- Our cooperation in round 1 triggers their cooperation in round 2+
- Observed cooperation rate rises, sustaining our cooperation
- Mutual benefit realized

### Against Conditional Cooperators (Threshold-based players)
- Our sustained cooperation meets their cooperation requirements
- Sustainability threshold likely exceeded
- Positive feedback loop

### Against Random Players
- Probabilistic cooperation hedge allows graceful degradation
- We don't overcommit when cooperation is unreliable
- Expected payoff remains above pure defection if k is reasonable

### Against Mixed/Heterogeneous Opponents
- The aggregate cooperation rate (across all opponents) is what matters
- If 50% cooperate and 50% defect, we match the observed sustainability
- Naturally weighted toward groups with higher cooperation

---

## PSEUDOCODE IMPLEMENTATION

```
Initialize: cooperation_history = []

FOR each round t in [1, r]:
    
    IF t == 1:
        action = COOPERATE
    
    ELSE IF t == r:
        action = COOPERATE
    
    ELSE:  // rounds 2 to r-1
        observed_coop_rate = COUNT(COOPERATE in cooperation_history) / (n × (t-1))
        sustainability_threshold = (1/k) - (1/n)
        
        IF observed_coop_rate ≥ sustainability_threshold:
            action = COOPERATE
        
        ELSE IF observed_coop_rate ≥ sustainability_threshold × 0.5:
            IF RANDOM() < (observed_coop_rate / sustainability_threshold):
                action = COOPERATE
            ELSE:
                action = DEFECT
        
        ELSE:
            action = DEFECT
        END IF
    
    END IF
    
    Receive payoff π_i,t
    Record all players' actions in cooperation_history
    
END FOR
```

---

## ALIGNMENT WITH COMMUNAL MINDSET

1. **Unconditional round 1 contribution**: Assumes others may be trustworthy; opens collaboration door
2. **Sustainability-based decisions**: Asks "what level of cooperation makes the public good rational?"
3. **Final round cooperation**: Signals that individual welfare is not the only value; community matters
4. **Probabilistic hedge**: Acknowledges uncertainty while remaining committed to collective value when plausible
5. **Transparency in logic**: The strategy is based on observable facts (cooperation rate), not hidden preferences

This strategy seeks the **Pareto frontier** of the game—maximizing collective payoff while maintaining individual viability.
'''

description_COMMUNAL_19 = '''
# ADAPTIVE COMMUNAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## CORE PHILOSOPHY

This strategy balances three objectives:
1. **Communal contribution** - Maximize total welfare by encouraging collective action
2. **Self-protection** - Avoid exploitation by free-riders
3. **Robustness** - Adapt to opponent behavior without assuming coordination

The strategy treats cooperation as an *invitation* that must be reciprocated to be sustained.

---

## DECISION RULE: CONDITIONAL CONTRIBUTION WITH DECAY

### Primary Logic: "Contribute if Contribution Justified"

Cooperate in round t if:
```
cooperation_rate(t-1) ≥ threshold(t)
```

Where:
- **cooperation_rate(t-1)** = proportion of players who cooperated in round t-1
- **threshold(t)** = dynamic threshold that increases as rounds progress

### Threshold Function (Adaptive Decay)

```
threshold(t) = min(k/n, base_threshold - decay_rate × (t-1))
```

**Parameters:**
- **base_threshold** = 0.5 (require >50% cooperation initially)
- **decay_rate** = (0.5 - k/n) / (r - 1) 
  - Gradually lowers expectations as game progresses
  - Final threshold converges to k/n (the break-even point)
- **k/n** = floor threshold (never require more than the multiplication factor)

**Intuition:** 
- Early rounds demand higher reciprocity (stronger signal of intent)
- As game progresses, accept lower cooperation rates
- Never demand cooperation rates that make defection strictly better

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (First Round)
**Decision: COOPERATE**

Rationale:
- No history exists; cannot condition on past behavior
- Cooperation signals communal intent and invitation to others
- Sets cooperative baseline
- Establishes that "cooperation is possible here"

### Round r (Last Round)
**Decision: Follow primary logic, BUT apply strict threshold**

```
if cooperation_rate(r-1) ≥ threshold(r):
    COOPERATE
else:
    DEFECT
```

Rationale:
- No future reciprocation possible, so no additional reputation concerns
- If cooperation collapsed before final round, don't waste endowment
- If cooperation sustained, reinforce it through final round
- This is honest: defect only if others already did

### Extreme Scenarios

**If cooperation_rate(t-1) = 0 (all defected):**
- Defect in round t
- Rationale: One-shot defection won't restore cooperation; protect endowment

**If cooperation_rate(t-1) = 1 (all cooperated):**
- Cooperate in round t
- Rationale: Maintain momentum; never unilaterally break universal cooperation

**If cooperation_rate(t-1) = 1/n (only you cooperated):**
- Defect in round t
- Rationale: Detected as exploited cooperator; withdraw

---

## PSEUDOCODE IMPLEMENTATION

```
function decide_round(t, history, n, k, r):
    
    // Round 1: Always cooperate
    if t == 1:
        return COOPERATE
    
    // Calculate cooperation in previous round
    prev_cooperators = count_cooperators(history[t-1])
    cooperation_rate = prev_cooperators / n
    
    // Calculate dynamic threshold
    if t < r:
        decay_rate = (0.5 - k/n) / (r - 1)
        threshold = max(k/n, 0.5 - decay_rate × (t - 1))
    else:  // Last round
        threshold = k/n  // Stricter final requirement
    
    // Decision
    if cooperation_rate ≥ threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## COMMUNAL ALIGNMENT

### Why This Strategy Serves the Commons

1. **Rewards collective action:** Cooperates when majority cooperates, amplifying total welfare
2. **Penalizes free-riding:** Withdraws from low-cooperation environments
3. **Enables coordination without explicit agreement:** 
   - Creates a natural "cooperation basin" where mutual cooperation becomes stable
   - If >50% cooperate initially, strategy sustains cooperation
   - This benefits all players more than universal defection

4. **Fair burden-sharing:** 
   - Will cooperate at ANY cooperation rate ≥ k/n (mutual profitability threshold)
   - Won't demand unfair contribution levels
   - Doesn't exploit others; exits rather than free-riding

5. **Graceful degradation:**
   - Adapts expectations downward over time
   - Recognizes that some groups can't sustain high cooperation
   - Better to sustain k/n cooperation than collapse to 0

### Against Exploitation

- **Exploiters get detected:** If defectors cause cooperation_rate to fall below threshold, strategy responds by defecting
- **One-round forgiveness:** A single round of low cooperation triggers withdrawal, preventing repeated exploitation
- **No punishment surplus:** Defects only to protect self, not to punish others

---

## ROBUSTNESS PROPERTIES

| Opponent Type | Response |
|---|---|
| **All-Cooperators** | Cooperates all rounds (mutual benefit) |
| **All-Defectors** | Defects round 2+ onward (minimal loss) |
| **Tit-for-Tat cooperators** | Stabilizes on mutual cooperation |
| **Random players** | Adapts threshold; withdraws if cooperation drops too low |
| **Exploitative free-riders** | Detects and responds; cooperation not sustainable |
| **Conditional cooperators like this one** | Creates stable cooperative equilibrium if majority uses similar logic |

---

## TOURNAMENT ADVANTAGE

This strategy succeeds because:

1. **Against cooperative players:** Matches cooperation, earning shared public good
2. **Against defectors:** Minimizes losses by detecting quickly (threshold-based exit)
3. **Against mixed strategies:** Adapts dynamically without assuming specific opponent types
4. **Against itself:** Creates stability—if many players use this, >50% cooperation is self-sustaining
5. **Alignment with game math:** The final threshold of k/n reflects the mathematical break-even point

The strategy embodies a principle: *"I will contribute to the commons if you will too, and I'll match your rate generously, but I won't subsidize defection."*
'''

description_COMMUNAL_20 = '''
# ADAPTIVE COMMUNAL STRATEGY: "Conditional Reciprocal Contribution"

## Core Philosophy
This strategy balances communal welfare with individual sustainability. It recognizes that:
1. **Universal defection harms everyone** (payoff = 1)
2. **Unilateral cooperation against defectors is exploitative** (payoff = 0)
3. **Sustainable cooperation requires reciprocal participation** (payoff approaches 2 when k is favorable)

The strategy is "communal" not in naive optimism, but in pragmatic commitment: contribute when conditions support collective benefit, withdraw when exploitation occurs, and always signal willingness to rebuild cooperation.

---

## DECISION RULE: Adaptive Threshold Reciprocity

### Round 1 (Initialization)
**COOPERATE**

*Rationale:* Assume good faith. This signals willingness to build communal value and establishes a baseline for reciprocal behavior. If everyone cooperates, payoff is (k/n)n = k > 1. The first-round loss of 1 unit is investment in discovering whether collective cooperation is possible.

### Rounds 2 to r-1 (Adaptive Phase)

**Calculate the Cooperation Rate from previous round:**
```
coop_rate = (number of cooperators in round t-1) / n
```

**Decision Logic:**

```
IF coop_rate ≥ threshold:
    COOPERATE
    // Reciprocate cooperative sentiment
    
ELSE IF coop_rate < threshold:
    DEFECT
    // Protect against exploitation
    // But signal readiness to restart
```

**Threshold Calculation (Dynamic):**
```
threshold = k / n
```

*Rationale:* The threshold equals the "fair share" benefit from the public good. When the cooperation rate is high enough that cooperators receive at least as much from the public good as they invest, it's rational and communal to participate. When cooperation falls below this point, the public good is underfunded and contributes less than the private payoff (1), making defection justified.

- If coop_rate ≥ k/n: Even cooperators break even or profit
- If coop_rate < k/n: Defectors strictly dominate; cooperation is exploitative

### Round r (Final Round)

**COOPERATE**

*Rationale:* Separate from the strategic calculus of earlier rounds. In the final round:
- No reputation payoff exists (no future rounds to influence)
- Standard game theory predicts defection
- **But this is precisely where communal commitment matters**

Final-round cooperation demonstrates that the strategy isn't purely self-interested and rewards reciprocal players. It's a "goodwill signal" that says: *"I cooperated because I believe in collective value, not just because I expected future punishment."*

Additionally, final-round defection against cooperators would be nakedly exploitative—the most communal damage with zero strategic benefit.

---

## EDGE CASES & SPECIAL HANDLING

### Case: r = 2 (Only two rounds)
- Round 1: COOPERATE (signal good faith)
- Round 2: COOPERATE (final round rule applies; also demonstrates commitment)

*Result:* Against cooperators, get k payoff. Against pure defectors, get 2(k/n). This accepts exploitation risk but maintains integrity.

### Case: n = 2 (Duopoly)
- threshold = k/2
- If opponent cooperates: cooperate (both get k)
- If opponent defects: defect after round 1 (mutual payoff = 1)
- Final round: cooperate (final rule overrides)

This reduces to a modified Tit-for-Tat with final generosity.

### Case: Perfect Defection (all others defect)
- Round 1: You cooperate, others defect → you get k/n, others get 1 + k/n
- Rounds 2 to r-1: coop_rate = 1/n << k/n → You defect
- Round r: You cooperate again (final rule)

*Analysis:* You accept limited loss rounds 1 and r to test cooperation, then rationally protect yourself. This minimizes exploitation while signaling non-spite.

### Case: Oscillating Cooperation
If other players oscillate between high and low cooperation:
- Your strategy tracks the oscillation: cooperate when coop_rate is high, defect when low
- Self-stabilizing: creates incentive for others to stabilize cooperation
- Prevents locking into defection if oscillators eventually stabilize high

---

## PSEUDOCODE

```
strategy(game_history, n, k, r, current_round):
    
    IF current_round == 1:
        return COOPERATE
    
    IF current_round == r:
        return COOPERATE
    
    // Rounds 2 to r-1
    prev_round_cooperators = count_cooperators(game_history[current_round - 1])
    coop_rate = prev_round_cooperators / n
    threshold = k / n
    
    IF coop_rate >= threshold:
        return COOPERATE
    ELSE:
        return DEFECT
```

---

## PROPERTIES

| Property | Value |
|----------|-------|
| **Transparent** | Rules depend only on publicly observable cooperation rate and parameters |
| **Memoryful** | Adapts to recent history; not myopic |
| **Stable** | If cooperation threshold is met, perpetuates cooperation |
| **Self-correcting** | Exits defection spirals if cooperation recovers |
| **Non-retaliatory** | Doesn't punish; responds to conditions |
| **Communal** | Final-round cooperation despite no strategic benefit |
| **Robust** | Works for any n ≥ 2, 1 < k < n, r > 1 |

---

## EXPECTED PERFORMANCE

- **Against universal cooperators:** Near-optimal (payoff ≈ 2r - 2 + k)
- **Against universal defectors:** Modest loss (payoff ≈ 2k/n + (r-2))
- **Against mixed strategies:** Payoff scales with cooperation level; never maximally exploited
- **Against reciprocal strategies:** Mutual cooperation maintained when threshold sustainable

This strategy pragmatically balances communal idealism with individual sustainability.
'''

description_COMMUNAL_21 = '''
# Communal Strategy: Adaptive Reciprocal Contribution (ARC)

## Core Philosophy

This strategy embodies **enlightened communitarianism**: maximize collective welfare while remaining robust against exploitation. The key insight is that in public goods games, the community thrives when contribution levels are sustained, but defection must be punished to prevent free-riding collapse.

## Decision Rules

### PRIMARY RULE: Threshold-Based Reciprocal Contribution

```
cooperation_target = k / n  (the "fair share" threshold)
```

**For round t > 1:**
```
observed_contribution_rate = (total_cooperators_in_round_t-1) / n

IF observed_contribution_rate >= cooperation_target:
    COOPERATE
ELSE:
    DEFECT
```

**Rationale:** 
- When cooperation meets or exceeds the fair-share threshold, everyone benefits (including defectors). This is sustainable.
- When cooperation falls below this threshold, the public good becomes inefficient. Defecting protects your payoff while signaling that free-riding is unprofitable.

### FIRST ROUND: Cooperate

```
Round 1: COOPERATE
```

**Rationale:**
- Establishes a cooperative baseline and tests the environment
- Demonstrates good faith commitment to community building
- Provides information to calibrate subsequent strategy

### LAST ROUND: Conditional Defect

```
IF this is the final round AND observed_contribution_rate < cooperation_target:
    DEFECT
ELSE:
    Follow primary rule
```

**Rationale:**
- No future consequences exist, so reputation effects vanish
- If the community hasn't sustained fair contribution, there's no obligation to subsidize free-riders in the final round
- If cooperation is strong, reinforce it with final cooperation

## Handling Edge Cases

### Volatile Cooperation Patterns
If cooperation oscillates around the threshold:
```
IF |observed_contribution_rate - cooperation_target| < 0.15:
    COOPERATE (with bias toward community welfare)
```

This prevents thrashing between cooperation and defection when groups are genuinely trying to coordinate.

### Total Collapse (Near-zero cooperation)
```
IF observed_contribution_rate < 0.1:
    Remain in DEFECT for next 2 rounds to amplify punishment signal
    Then reassess
```

**Rationale:** Stronger signal that free-riding is unsustainable; communicates this to the broader group.

### High Cooperation Environments (>80%)
```
IF observed_contribution_rate > 0.8:
    COOPERATE unconditionally
```

**Rationale:** High-trust environments reward cooperation maximally. Reinforcing them strengthens group outcomes.

## Pseudocode

```
function decide(round, history, n, k):
    if round == 1:
        return COOPERATE
    
    // Calculate previous round's cooperation rate
    prev_cooperators = count_cooperators(history[round-1])
    contribution_rate = prev_cooperators / n
    threshold = k / n
    
    // Check volatility band
    if abs(contribution_rate - threshold) < 0.15:
        return COOPERATE
    
    // Check total collapse
    if contribution_rate < 0.1:
        if not in_defect_punishment_phase():
            activate_defect_punishment_phase(duration=2)
        return DEFECT
    
    // High cooperation: reinforce
    if contribution_rate > 0.8:
        return COOPERATE
    
    // Last round special case
    if round == r:
        if contribution_rate >= threshold:
            return COOPERATE
        else:
            return DEFECT
    
    // Primary rule: match community contribution level
    if contribution_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

## Why This Strategy Is Communal

1. **Reciprocity-based:** Rewards collective good behavior; punishes collective free-riding
2. **Mathematically grounded:** Uses the game's efficiency threshold (k/n) as the decision boundary
3. **Robust:** Works against pure defectors (you defect), pure cooperators (you cooperate), and mixed strategies (you calibrate)
4. **Emergent cooperation:** Incentivizes others to cooperate by making cooperation profitable
5. **Non-exploitative:** You don't punish individual defectors in isolation; you respond to group-level patterns
6. **Sustainable:** Focuses on maintaining the cooperation_target rate, which is stable and mutually beneficial

## Tournament Resilience

- **vs. Always-Defect:** You defect after round 1, minimizing damage
- **vs. Always-Cooperate:** You cooperate, maximizing joint payoffs
- **vs. Tit-for-Tat variants:** Your threshold-based rule prevents excessive cycling
- **vs. Mixed strategies:** You exploit free-riding less than pure defectors, but survive against exploitation better than pure cooperators

This strategy treats the public goods game as a **collective coordination problem** rather than a zero-sum competition, achieving robustness through principled adaptivity.
'''

description_COMMUNAL_22 = '''
# ADAPTIVE COMMUNAL RESILIENCE STRATEGY

## Core Philosophy
This strategy balances three principles:
1. **Communal preference**: Cooperate when it benefits the group
2. **Self-protection**: Defect strategically against exploiters
3. **Robustness**: Adapt dynamically to opponent behavior without requiring coordination

## Key Insight
The game structure creates a fundamental tension: individual rational play (defection) destroys collective welfare. However, selective cooperation with cooperators can outperform universal defection. The strategy exploits this by identifying cooperators and building conditional coalitions.

---

## STRATEGY SPECIFICATION

### PHASE 1: INITIAL ROUNDS (Rounds 1-3)

**Round 1: COOPERATE**
- Action: Play C
- Rationale: We must attempt cooperation to discover if others are cooperatively inclined. This is the only way to test the environment.

**Rounds 2-3: Conditional based on Round 1 observation**
- **If all other players played C in Round 1**: Play C
  - Evidence of communal environment; amplify cooperation
- **If mixed behavior observed**: Play C with probability P_coop = (cooperators_observed / (n-1))
  - Match the cooperation rate we observe; proportional reciprocity
- **If all others played D in Round 1**: Play D
  - Environment is defection-dominant; switch to defense mode

### PHASE 2: MID-GAME ROUNDS (Rounds 4 to r-2)

Track two metrics rolling across the last 3 rounds:

**Metric 1 - Cooperator Identification:**
- Calculate cooperation_rate = (total cooperators in last 3 rounds) / (3 × (n-1))
- Classify each observed opponent individually:
  - **Pure Cooperator**: Played C in all 3 recent rounds
  - **Conditional Cooperator**: Played C in 2/3 recent rounds
  - **Defector**: Played C in 0-1 recent rounds

**Metric 2 - Environmental Health:**
- Calculate global_cooperation = (total C plays across all players in last 3 rounds) / (3n)

**Decision Rule:**

```
IF global_cooperation > (k/n):
    // Public good creates positive return
    action = COOPERATE
ELSE IF global_cooperation < (k / (2n)):
    // Severe defection-dominance; payoff to defecting is high
    action = DEFECT
ELSE:
    // Mixed environment: proportional strategy
    IF (average_opponent_cooperation > 0.5):
        action = COOPERATE
    ELSE:
        action = DEFECT
```

**Intuition**: 
- When cooperation is above the threshold where k/n > 1, contributing to the public good pays off
- When cooperation is very low, we protect ourselves
- In the middle, we mirror the observed environment

### PHASE 3: FINAL ROUNDS (Last 2 rounds)

**Round r-1:**
- Apply the same logic as mid-game: assess cooperation_rate and play accordingly
- Do NOT defect opportunistically just because the game is ending
- This maintains credible commitment to the strategy

**Round r (Final Round):**
- Apply the same decision rule (no end-game defection pivot)
- Reasoning: 
  1. Other agents may employ reputation-based strategies that test our final-round behavior
  2. Defecting now provides minimal gain (1 round of payoff advantage)
  3. Maintains signal that we are a "stable" cooperative agent for future interactions

---

## PSEUDOCODE

```
function play_round(round_number, history):
    n = number_of_players
    k = multiplication_factor
    r = total_rounds
    
    IF round_number == 1:
        RETURN COOPERATE
    
    IF round_number IN {2, 3}:
        cooperators_count = count_C_plays_in_round(1, other_players)
        cooperation_rate = cooperators_count / (n - 1)
        
        IF cooperation_rate > 0.8:
            RETURN COOPERATE
        ELSE IF cooperation_rate > 0.5:
            RETURN COOPERATE with probability = cooperation_rate
        ELSE:
            RETURN DEFECT
    
    // Mid-game and final rounds (4 to r)
    recent_rounds = history[max(1, round_number - 3) : round_number - 1]
    
    global_cooperation = count_total_C_plays(recent_rounds) / (3 * n)
    opponent_cooperation = count_total_C_plays_by_others(recent_rounds) / (3 * (n - 1))
    
    threshold_high = k / n
    threshold_low = k / (2 * n)
    
    IF global_cooperation > threshold_high:
        RETURN COOPERATE
    ELSE IF global_cooperation < threshold_low:
        RETURN DEFECT
    ELSE:
        IF opponent_cooperation > 0.5:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
```

---

## EDGE CASE HANDLING

| Edge Case | Resolution |
|-----------|-----------|
| **k very close to 1** | threshold_high ≈ 1/n; cooperation only sustained if nearly all cooperate. Strategy correctly defaults to DEFECT until proven otherwise. |
| **k very close to n** | threshold_high → 1; cooperation is highly rewarding. Strategy tends toward COOPERATE in mid-game phases. |
| **n = 2** | Two-player game becomes a prisoner's dilemma variant. Strategy alternates based on opponent's last action; if both defected, mutual defection persists (rational equilibrium). |
| **r = 2** | Only one round to evaluate. Round 1: COOPERATE (probe). Round 2: Respond based on Round 1 observation. |
| **All opponents pure defectors** | After Rounds 2-3, strategy correctly identifies global_cooperation ≈ 0, switches to DEFECT and stays there. |
| **All opponents pure cooperators** | After Rounds 2-3, global_cooperation = 1, strategy identifies this and stays in COOPERATE. |
| **Noisy/random opponents** | Cooperation_rate sits in the 0.3-0.7 range. Strategy oscillates or plays probabilistically, absorbing the noise instead of over-responding. |

---

## COMMUNAL ALIGNMENT

✓ **Prefers mutual cooperation**: Opens with C and rewards others who cooperate
✓ **Protects the group**: Defects against widespread defection to avoid being exploited
✓ **Fair and transparent**: Uses only public information (observed actions); no hidden state
✓ **Adaptive**: Responds dynamically to the actual behavior environment, not pre-programmed
✓ **Robust**: Doesn't assume others follow any specific strategy; works against heterogeneous opponents
'''

description_COMMUNAL_23 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances two competing imperatives:
1. **Communal value creation**: Maximize total welfare by encouraging cooperation
2. **Self-protection**: Avoid exploitation by defectors while remaining open to cooperation

The strategy is based on **conditional cooperation with decay-resistant memory**, designed to work in tournaments where others may not share communal values.

---

## Strategy Definition

### Decision Rule (General Round)

```
IF round == 1:
    COOPERATE
    
ELSE IF round == r (final round):
    LET cooperation_rate = (cooperators in previous round) / n
    IF cooperation_rate >= threshold_final:
        COOPERATE
    ELSE:
        DEFECT
        
ELSE (middle rounds):
    LET cooperation_rate = average_cooperation_across_history
    LET recent_cooperation = cooperation_rate_in_last_3_rounds
    
    IF recent_cooperation >= (k/n):
        COOPERATE  // Reciprocate when cooperation is self-sustaining
    ELSE IF cooperation_rate >= (k/n) AND round <= r/2:
        COOPERATE  // Give cooperation a chance in early/mid game
    ELSE:
        DEFECT     // Protect against systematic defection
```

### Parameters & Thresholds

**threshold_final** = max(0.5, k/n)
- High bar for final round (avoid last-round exploitation)
- Adjusted by multiplication factor

**threshold_cooperate** = k/n
- Critical threshold: cooperation generates positive externality
- If fewer than (n × k/n) = k players cooperate, individual cooperators lose value
- Below this, defection is individually rational; above it, cooperation is sustainable

---

## Detailed Decision Logic

### Round 1: Unconditional Cooperation
- **Action**: COOPERATE
- **Rationale**: 
  - Initialize with communal intent
  - Signal willingness to cooperate
  - Establish baseline for measuring reciprocation

### Rounds 2 to r-1: Conditional Cooperation with Memory

**Step 1: Calculate Historical Cooperation Rate**
```
avg_coop_rate = Σ(cooperators in rounds 1 to t-1) / ((t-1) × n)
recent_coop_rate = Σ(cooperators in last 3 rounds) / (min(3, t-1) × n)
```

**Step 2: Evaluate Sustainability**
```
self_sustaining_threshold = k/n

IF recent_coop_rate >= self_sustaining_threshold:
    // Cooperation is generating positive returns
    COOPERATE
    
ELSE IF avg_coop_rate >= self_sustaining_threshold AND round <= r/2:
    // Early/mid game: give cooperation benefit of the doubt
    COOPERATE
    
ELSE:
    // Defection is safer
    DEFECT
```

**Rationale for this structure:**
- Recent behavior weighted more heavily (detects shifts in group behavior)
- Self-sustaining threshold (k/n) provides clear, parameter-dependent boundary
- Early-game leniency allows cooperation to bootstrap
- Late-game defection when cooperation has failed

### Round r (Final Round): Strong Defection Bias

```
IF cooperation_rate_previous_round >= threshold_final:
    COOPERATE  // Only if cooperation sustained until the end
ELSE:
    DEFECT     // Default: last-round exploitation is rational
```

- **Rationale**: The finality of the last round removes future reciprocation incentives
- Higher threshold ensures only robust cooperation persists to final round
- Prevents "last-round betrayal" paradox by requiring evidence of stable cooperation

---

## Edge Cases & Special Handling

### Few Players (n = 2 or 3)
- Individual behavior has outsized impact on others
- Threshold (k/n) becomes very permissive
- Strategy naturally becomes more cooperative due to mathematical structure
- Single defector more obviously identified

### Many Players (n ≥ 10)
- Individual impact on others is diluted
- Threshold (k/n) becomes stricter
- Strategy becomes more defection-prone (rational, as free-riding is tempting)
- Cooperation requires higher group coordination

### Short Games (r = 2)
- Round 1: COOPERATE (signal intent)
- Round 2: Follow final-round logic (strict threshold)
- Minimal opportunity for reciprocation learning

### Long Games (r ≥ 20)
- Early-game leniency (rounds 2 to r/2) is well-utilized
- Historical averages are more informative
- Mid-game adaptive period is extended
- Late-game defection bias properly calibrated

---

## Robustness Properties

### Against Pure Defectors
- After round 1, detects zero cooperation
- Switches to defection quickly (by round 3-4)
- Minimizes exploitation damage

### Against Tit-for-Tat Cooperators
- Mutual cooperation emerges naturally
- Both players cooperate after round 1
- Maintains cooperation if threshold sustained

### Against Mixed Strategies
- Recent cooperation rate is key signal
- Adapts to gradual shifts in group behavior
- Decay-resistant: doesn't over-react to single defections

### Against Sophisticated Exploiters
- Cannot be fooled by first-round cooperation (no special trust given)
- Evaluates full history, not just last action
- Final-round strict threshold prevents being "set up"

---

## Implementation Pseudocode

```
function decide(round, n, r, k, history):
    
    if round == 1:
        return COOPERATE
    
    // Calculate cooperation rates
    total_cooperators = sum of cooperators in all previous rounds
    avg_coop_rate = total_cooperators / ((round - 1) × n)
    
    recent_rounds = min(3, round - 1)
    recent_cooperators = sum of cooperators in last recent_rounds
    recent_coop_rate = recent_cooperators / (recent_rounds × n)
    
    self_sustaining = k / n
    
    if round == r:  // Final round
        threshold = max(0.5, k / n)
        if avg_coop_rate >= threshold:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // Middle rounds
        if recent_coop_rate >= self_sustaining:
            return COOPERATE
        
        else if avg_coop_rate >= self_sustaining and round <= r/2:
            return COOPERATE
        
        else:
            return DEFECT
```

---

## Communal Alignment

This strategy embodies communal values by:

1. **Initiating cooperation**: Round 1 assumes good faith
2. **Rewarding reciprocity**: Cooperates when others sustain it
3. **Maximizing collective welfare**: Cooperates when cooperation is self-sustaining (k/n threshold)
4. **Honest evaluation**: Uses transparent thresholds, not arbitrary rules
5. **Graceful degradation**: Protects the commons by withdrawing when cooperation collapses
6. **Parameter-adaptive**: Works across different game configurations without special tuning

The strategy is **not naïve**—it recognizes that communal behavior requires reciprocation. When others defect, it defects. But it remains a "nice" player: never initiating defection, only responding to collective failures.
'''

description_COMMUNAL_24 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances three competing objectives:
1. **Communal welfare**: Maximize total group payoff
2. **Self-protection**: Avoid exploitation by defectors
3. **Robustness**: Adapt to unknown opponent types without pre-coordination

The strategy recognizes that in public goods games, collective cooperation maximizes total welfare, but individual defection is always tempting. Since we cannot assume others share our values, we must be strategically generous but rationally defensive.

---

## Strategy: "Adaptive Reciprocal Contribution" (ARC)

### Phase 1: Opening Probe (Rounds 1-2)

**Round 1: Cooperate (C)**
- Rationale: Establish a cooperative baseline and signal good intent
- Maximize information: Observe how others respond to cooperation

**Round 2: Respond to Round 1 Cooperation Rate**
- If cooperation_rate ≥ 50%: Play C
- Else: Play D

This two-round probe quickly identifies the cooperative tendency of the group.

### Phase 2: Adaptive Recalibration (Rounds 3 to r-1)

For each round t ≥ 3:

**Calculate the Cooperation Signal:**
```
cooperation_history = [outcomes from rounds 1 to t-1]
recent_coop_rate = (cooperators in round t-1) / n
avg_coop_rate = (total cooperators in rounds 1 to t-1) / ((t-1) × n)
```

**Determine Personal Action:**

```
IF avg_coop_rate ≥ (k/n):
    // Cooperation appears sustainable
    IF recent_coop_rate ≥ 0.5:
        Play C
    ELSE:
        // Defection increasing - cautiously defect once
        Play D
ELSE IF avg_coop_rate ≥ (k/n) × 0.6:
    // Moderate cooperation - tentative reciprocation
    Play C with probability = avg_coop_rate
ELSE:
    // Low cooperation environment
    IF recent_coop_rate ≥ 0.3:
        Play D (with occasional C to test)
    ELSE:
        Play D consistently
```

**Probabilistic Exploration Component:**
- Every 3 rounds, allocate 1 exploratory action
- If currently playing D, try C once to test if group dynamics have improved
- If currently playing C, hold steady (don't defect exploratively)

### Phase 3: Endgame (Rounds r-1 and r)

**Round r-1:**
```
IF avg_coop_rate ≥ (k/n) × 0.7:
    Play C (support cooperation near the end)
ELSE:
    Play D (exploit remaining rounds)
```

**Round r (Final Round):**
```
// Final round deserves special consideration
IF the game has maintained avg_coop_rate ≥ (k/n):
    Play C
    // Reason: Maximize final communal payoff; defecting in final round
    // creates no opportunity for punishment/repair
ELSE:
    Play D
    // Reason: No future punishment possible anyway
```

---

## Decision Rules Summary

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Always C | Probe for cooperation |
| Round 2 | C if others ≥50% cooperative, else D | Test stability |
| Rounds 3 to r-2 | Adapt based on avg_coop_rate and recent trends | Reciprocate honestly |
| Round r-1 | C if sustained cooperation, else D | Prepare for finale |
| Round r | C if group avg ≥ threshold, else D | Maximize final payoff |

---

## Edge Cases & Special Handling

### Case 1: All Other Players Defect from Start
- Round 1: We play C (probe)
- Round 2+: Recognize avg_coop_rate is low, play D
- **Outcome**: Minimize losses while clearly responding to defection

### Case 2: Perfect Cooperation Emerges
- avg_coop_rate → k/n
- Sustain C indefinitely
- **Outcome**: All players receive maximum payoff of k (all cooperate and benefit equally)

### Case 3: Volatile/Mixed Opposition
- Cooperation fluctuates between 30-70%
- Play probabilistically based on recent trends
- Exploration phase kicks in every 3 rounds to test if environment improves
- **Outcome**: Maintain sensitivity to changing conditions

### Case 4: Near-Total Defection with One Defector
- If n-1 players defect and 1 cooperates, that cooperator loses
- We defect to avoid being the sole sucker
- **Outcome**: Avoid exploitation trap

### Case 5: Small n (n=2 or 3)
- Strategy naturally adapts: (k/n) threshold becomes easier to hit
- Same rules apply; reciprocation is more visible
- **Outcome**: Works identically across group sizes

---

## Why This Is Communal

1. **Preference for Cooperation**: Opens with C, returns to C when feasible
2. **Welfare Sensitivity**: Tracks group cooperation rate, not just personal profit
3. **Fair Reciprocation**: Cooperates when others do, defects when they don't
4. **Shared Benefit**: Explicitly targets scenarios where total welfare (k) is maximized
5. **Trust But Verify**: Tests cooperation repeatedly without naive assumption of others' motives

---

## Robustness Properties

- **Against Pure Defectors**: Quickly identifies and neutralizes (plays D)
- **Against Tit-for-Tat**: Compatible; triggers mutual cooperation
- **Against Conditional Cooperators**: Aligns incentives through reciprocation
- **Against Stochastic Strategies**: Averages out noise via multi-round history
- **Against Majority Dynamics**: Maintains independent assessment via avg_coop_rate

---

## Pseudocode Implementation

```
strategy(game_history, parameters):
    n = parameters.num_players
    k = parameters.multiplication_factor
    r = parameters.num_rounds
    current_round = length(game_history) + 1
    
    if current_round == 1:
        return COOPERATE
    
    if current_round == 2:
        round_1_coop = count_cooperators(game_history[0])
        if round_1_coop / n >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    
    avg_coop = calculate_average_cooperation_rate(game_history)
    recent_coop = count_cooperators(game_history[-1]) / n
    
    if current_round == r:
        if avg_coop >= (k / n):
            return COOPERATE
        else:
            return DEFECT
    
    if current_round == r - 1:
        if avg_coop >= (k / n) * 0.7:
            return COOPERATE
        else:
            return DEFECT
    
    // Main adaptive phase
    if avg_coop >= (k / n):
        if recent_coop >= 0.5:
            return COOPERATE
        else:
            return DEFECT
    else if avg_coop >= (k / n) * 0.6:
        if random() < avg_coop:
            return COOPERATE
        else:
            return DEFECT
    else:
        if recent_coop >= 0.3 or (current_round mod 3) == 0:
            return COOPERATE  // Exploratory
        else:
            return DEFECT
```

This strategy maximizes communal welfare while remaining strategically sound in adversarial environments.
'''

description_COMMUNAL_25 = '''
# ADAPTIVE COMMUNAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## CORE PHILOSOPHY

This strategy embraces **conditional cooperation** with **opportunistic defense**: contribute to the common good when others demonstrate reciprocal intent, but protect against exploitation by defectors. The strategy optimizes for collective welfare while remaining individually rational when cooperation breaks down.

---

## DECISION RULES

### PRIMARY STRATEGY: Adaptive Threshold Cooperation

**Cooperate** if and only if:
- **Round 1 (Initialization):** COOPERATE unconditionally
  - *Rationale:* Establish cooperative intent as baseline. No history exists yet.

- **Rounds 2 to r-1 (Main Phase):** COOPERATE if the cooperation rate in the previous round ≥ threshold(t)
  - **Dynamic threshold:** threshold(t) = max(0.4, (k/n) × 0.5)
  - *Rationale:* Reciprocate cooperation proportionally to payoff multiplication. The threshold accounts for game efficiency—when k approaches n, even minority cooperation can be valuable. The 0.4 floor ensures we don't demand unrealistic cooperation from pessimistic groups.

- **Round r (Final Round):** DEFECT
  - *Rationale:* Last round creates no future consequences. Standard backward induction logic. Defecting extracts maximum individual payoff when future cooperation cannot be reciprocated.
  - *Exception:* If cooperation rate in round r-1 > (1 - 1/n), COOPERATE to signal good faith and acknowledge strong cooperation.

---

## FORMAL DECISION PSEUDOCODE

```
function decide_action(round_number, previous_cooperation_rate, n, k):
    
    if round_number == 1:
        return COOPERATE
    
    if round_number == r:
        if previous_cooperation_rate > (1 - 1/n):
            return COOPERATE
        else:
            return DEFECT
    
    # Main phase (rounds 2 to r-1)
    threshold = max(0.4, (k/n) × 0.5)
    
    if previous_cooperation_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## EDGE CASES & NUANCED HANDLING

### Case 1: Very High Cooperation (cooperation_rate > 80%)
**Action:** COOPERATE
- *Rationale:* Group is demonstrably cooperative. Contributing yields positive externalities and stabilizes the cooperative equilibrium.

### Case 2: Moderate Cooperation (40% ≤ cooperation_rate ≤ 80%)
**Action:** COOPERATE (if threshold logic permits)
- *Rationale:* Mixed populations can still achieve payoff-positive outcomes. Threshold acts as circuit-breaker.

### Case 3: Low Cooperation (cooperation_rate < 40%)
**Action:** DEFECT
- *Rationale:* Defectors dominate. Contributing yields negative expected payoff: (k/n) × small_number < 1. Preserve capital.

### Case 4: Complete Defection (cooperation_rate = 0%)
**Action:** DEFECT
- *Rationale:* No benefit from contribution. Minimize loss.

### Case 5: Initial Rounds with Volatile Cooperation
- **Rounds 2-3:** Use threshold mechanism strictly. Avoid overreacting to noise.
- **Rounds 4+:** Threshold mechanism stabilizes strategy.

### Case 6: Second-to-Last Round Spike
If cooperation jumps dramatically in round r-1 (e.g., 20% → 90%), still apply threshold logic:
- If jump ≥ threshold: COOPERATE
- *Rationale:* Genuine shift in group behavior should be honored even near the end.

---

## ROBUSTNESS PROPERTIES

### Against Always-Defect Opponents:
- **Round 1:** We cooperate (signal attempt)
- **Round 2+:** Cooperation rate = 0%, we defect
- **Outcome:** Minimize damage by matching defection. Not exploited repeatedly.

### Against Always-Cooperate Opponents:
- **Rounds 1 to r-1:** We cooperate (rate ≈ 100% triggers cooperation)
- **Round r:** We defect (final-round rational play)
- **Outcome:** Mutual cooperation until final round, where we extract surplus. Acceptable tension between collective and individual gain.

### Against Tit-for-Tat Variants:
- **Mutual convergence to cooperation** (as long as other agent also attempts cooperation initially)
- **Our threshold is forgiving:** 40% minimum prevents hair-trigger defection
- **Outcome:** Stable, repeated cooperation creates positive-sum outcomes

### Against Mixed/Erratic Strategies:
- **Threshold acts as damper:** Prevents oscillation between cooperation and defection
- **Adapts gradually:** Observes trends rather than single-round anomalies
- **Outcome:** Stabilizes around rational equilibrium given opponent type

---

## COMMUNAL ALIGNMENT

**Why this strategy is communal:**

1. **Cooperation-First Bias:** Starts with cooperation, signaling willingness to contribute to the commons.

2. **Reciprocal Fairness:** Mirrors group behavior—contributes when others do, withdraws when exploitation becomes obvious. This is **fair** in the sense of proportional return on investment in collective welfare.

3. **Collective Welfare Optimization:** By cooperating in rounds 2 to r-1 with threshold logic, we:
   - Maximize total payoff when k > 1 and cooperation is moderate
   - Avoid free-riding as primary strategy
   - Support group stability

4. **Honest Final Round:** The final-round defection is **transparent:** it reflects the structural incentive, not hidden manipulation. Groups aware of backward induction should expect this.

5. **Threshold Forgiveness:** The 40% floor prevents fragile cooperation from collapsing on minor defections. We "give groups a chance" to cooperate sub-optimally.

---

## SUMMARY TABLE

| Scenario | Action | Rounds Affected |
|----------|--------|-----------------|
| First round | Cooperate | Round 1 |
| Strong cooperation detected | Cooperate | Rounds 2 to r-1 |
| Moderate cooperation detected | Cooperate if threshold satisfied | Rounds 2 to r-1 |
| Weak/no cooperation | Defect | Rounds 2 to r-1 |
| Final round + high prior cooperation | Cooperate | Round r only |
| Final round + low prior cooperation | Defect | Round r only |

---

This strategy balances **individual rationality** (final-round defection, threshold-based switching) with **communal intent** (cooperation-first, reciprocity norm, threshold forgiveness). It should perform well in tournaments with diverse opponents while maintaining moral clarity about its logic.
'''

description_COMMUNAL_26 = '''
# ADAPTIVE COMMUNAL STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

## Core Philosophy

This strategy balances **individual rationality with communal benefit** by:
1. Rewarding cooperation when it emerges
2. Protecting against free-riding without escalating to full defection
3. Maintaining a "sweet spot" of partial cooperation that improves collective welfare
4. Using history to estimate whether the group is trending cooperative or selfish

---

## STRATEGY: "Conditional Reciprocal Contribution" (CRC)

### 1. DECISION RULES

**Define: Cooperation Rate (CR)**
```
CR_t = (number of cooperators in round t-1) / n
```

**Define: Cooperation Trend (CT)**
```
CT = average CR over all previous rounds
```

**Base Contribution Threshold: θ = k/n**
- If θ > 0.5: The public good multiplier is strong; more cooperation is justified
- If θ ≤ 0.5: The public good multiplier is weak; pure cooperation is risky

---

### 2. PRIMARY DECISION RULE (Rounds 2 through r-1)

**Cooperate if and only if:**
```
CR_{t-1} ≥ f(θ, t, r)
```

**Where the threshold function is:**
```
f(θ, t, r) = θ + adjustment_factor

adjustment_factor = {
  -0.15  if θ > 0.6 (strong multiplier → be optimistic)
  0      if 0.4 ≤ θ ≤ 0.6 (moderate multiplier → match history)
  +0.20  if θ < 0.4 (weak multiplier → be cautious)
}

time_penalty = 0.10 × (r - t) / r  (slight increase threshold near end)
```

**Final threshold:**
```
Cooperate if: CR_{t-1} ≥ f(θ, t, r) - time_penalty
Otherwise: Defect
```

---

### 3. EDGE CASES

**Round 1 (No history):**
```
Cooperate if k ≥ 1.5
  Reasoning: If the multiplier is generous enough, seeding cooperation pays off.
             With k ≥ 1.5, even partial cooperation generates positive expected value.
Otherwise: Defect
  Reasoning: With weak multipliers, opening with defection protects against 
             being exploited by universal free-riders.
```

**Final Round (t = r):**
```
Use the standard rule above (CR_{t-1} ≥ f(θ, r, r))
  Reasoning: Even in the last round, cooperation can be reciprocal. 
             If others have cooperated, mutual cooperation in the final round 
             benefits everyone. Defecting in the final round breaks trust 
             and is only rational if the group has already failed.
```

**All-Defect Trap (CR_{t-1} = 0):**
```
If CR_{t-1} = 0 for 2+ consecutive rounds:
  Probe once: Cooperate in round t
  Reasoning: Break the mutual defection equilibrium by testing if others will reciprocate.
             One defector's exploration might trigger group learning.
             
  If others still defect (CR_t = 0), return to defection.
```

---

### 4. PSEUDOCODE

```
function decide_action(round, n, k, history):
  
  θ = k / n
  
  if round == 1:
    return k ≥ 1.5 ? COOPERATE : DEFECT
  
  // Calculate previous round cooperation rate
  cooperators_prev_round = count_cooperators(history[round-1])
  CR = cooperators_prev_round / n
  
  // Detect all-defect trap
  if round ≥ 3:
    recent_crs = [CR for last 2 rounds]
    if all(cr == 0 for cr in recent_crs):
      return COOPERATE  // Probe
  
  // Determine threshold adjustment
  if θ > 0.6:
    adjustment = -0.15
  else if θ ≤ 0.4:
    adjustment = +0.20
  else:
    adjustment = 0
  
  // Time penalty (increase threshold near end)
  time_penalty = 0.10 × (n_total_rounds - round) / n_total_rounds
  
  // Compute threshold
  threshold = θ + adjustment - time_penalty
  
  // Make decision
  return CR ≥ threshold ? COOPERATE : DEFECT
```

---

## 5. COMMUNAL ALIGNMENT

**How this serves the collective:**

- **Reward Cooperation:** We match the group's cooperation rate, creating a positive feedback loop where cooperation begets cooperation.
- **Punish Free-Riding Softly:** We don't fully defect on free-riders; instead, we reduce our contribution, signaling disapproval while preserving room for recovery.
- **Break Bad Equilibria:** The probe in all-defect traps attempts to restart cooperation, benefiting everyone.
- **Adapt to Parameters:** The strategy scales with k and n, recognizing that different multipliers justify different cooperation levels.
- **Final Round Cooperation:** We don't defect at the end, respecting reciprocal players and giving the game a chance to reach a cooperative resolution.

**Why it's robust:**

- Works against pure defectors (we defect back quickly)
- Works against pure cooperators (we cooperate and share the gain)
- Works against tit-for-tat (we both cooperate)
- Works against mixed strategies (we track the trend and adjust)
- Doesn't require communication or coordination, only observation

---

## 6. SUMMARY TABLE

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1, k ≥ 1.5 | Cooperate | Invest in group learning |
| Round 1, k < 1.5 | Defect | Protect against exploitation |
| High prior cooperation (CR ≥ threshold) | Cooperate | Reciprocate and reinforce |
| Low prior cooperation (CR < threshold) | Defect | Protect from free-riders |
| All-defect trap (2+ rounds of zero cooperation) | Probe (Cooperate once) | Break equilibrium, signal hope |
| Final round, prior cooperation high | Cooperate | Leave positive legacy |
| Final round, prior cooperation low | Defect | Minimize losses |

---

This strategy prioritizes **trust but verify**, creating conditions where cooperation can flourish while remaining resilient to defection.
'''

description_COMMUNAL_27 = '''
# ADAPTIVE RECIPROCAL STEWARDSHIP STRATEGY

## Core Philosophy
This strategy embodies communal values by treating cooperation as an investment in collective welfare, while maintaining disciplined self-protection against exploitation. The goal is to maximize total welfare (mine + others') rather than relative advantage, but only when others reciprocate this commitment.

## Decision Rules

### PRIMARY RULE: Conditional Cooperation with Decay Memory

**For round t (where t > 1):**

```
cooperation_rate_last_round = (number of cooperators in round t-1) / n

IF cooperation_rate_last_round ≥ threshold_cooperative:
    COOPERATE
ELSE IF cooperation_rate_last_round ≤ threshold_defective:
    DEFECT
ELSE:
    COOPERATE_WITH_PROBABILITY(cooperation_rate_last_round)
```

**Where thresholds are:**
- `threshold_cooperative = k / n` (the point where cooperation gives equal payoff to defection)
- `threshold_defective = (k - 1) / n` (conservative defection threshold)

### JUSTIFICATION FOR THRESHOLDS:
At cooperation rate `p`, a cooperator gets: `k×p`, a defector gets: `1 + k×p`
- When `p ≥ k/n`: cooperation in aggregate gives positive returns, so encourage it
- When `p ≤ (k-1)/n`: collective action is weakening, signal caution
- Between these: probabilistically match community engagement (reciprocal matching)

---

## Edge Cases & Special Handling

### First Round (t=1):
**COOPERATE**

*Rationale:* The initial move establishes a communal norm. Defecting immediately poisons the well and eliminates any possibility of building cooperation. A communal player initiates good faith.

### Last Round (t=r):
**Apply PRIMARY RULE exactly as normal**

*Rationale:* While the "shadow of the future" disappears, the communal strategy doesn't exploit this. Defecting in the final round based on end-game logic contradicts communal values and would undermine any learning of reciprocal norms. Consistency matters for reputation and collective welfare.

---

## Handling Extreme Scenarios

### Universal Defection (all others always defect):
After observing round 1, the strategy detects `cooperation_rate = 0`, which is ≤ `threshold_defective`. The strategy switches to **always defect**. This prevents being repeatedly exploited while signaling: "I tried cooperation; you didn't reciprocate."

### Universal Cooperation (all others always cooperate):
The strategy detects `cooperation_rate = 1` at end of round 1, which is ≥ `threshold_cooperative`. The strategy **continues cooperating forever**. This maximizes collective payoff (2 units per round vs. 1) and aligns with communal ideals when reciprocated.

### Mixed Behaviors:
The strategy continuously recalibrates each round, allowing it to:
- Reward improving cooperation trends (increasing cooperation rate → increase own probability)
- Punish declining trends (decreasing cooperation rate → decrease own probability)
- Remain adaptive to coalition formation (some players cooperating, others not)

---

## Communal Alignment

**1. Genuine Cooperation When Possible:**
By starting with cooperation and reciprocating positive cooperation rates, the strategy genuinely attempts to build a cooperative equilibrium that maximizes total welfare.

**2. Fair Reciprocity:**
Rather than punishing defectors harshly, the strategy uses probabilistic matching of the observed cooperation rate. This:
- Acknowledges that some players may be testing or learning
- Doesn't overreact to single defections
- Leaves room for redemption if cooperation rates improve

**3. No Exploitation:**
The strategy doesn't exploit unilateral cooperators indefinitely. It responds to systematic defection with defection, preventing a pattern where the communal player becomes a sucker.

**4. Transparency of Intent:**
The rule is simple and observable: "I cooperate when most of us do." This creates a clear incentive structure that others can learn and coordinate around without explicit communication.

**5. Consistency Over Selfishness:**
The strategy ignores end-game incentives to defect in the final round, valuing consistency and communal signal-sending over short-term gain.

---

## Pseudocode Summary

```
strategy(history, current_round, n, k, r):
    
    if current_round == 1:
        return COOPERATE
    
    last_round_cooperators = count_cooperators(history[current_round - 1])
    cooperation_rate = last_round_cooperators / n
    
    threshold_coop = k / n
    threshold_defect = (k - 1) / n
    
    if cooperation_rate ≥ threshold_coop:
        return COOPERATE
    
    else if cooperation_rate ≤ threshold_defect:
        return DEFECT
    
    else:
        // Probabilistic reciprocity
        return COOPERATE with probability = cooperation_rate
               DEFECT   with probability = (1 - cooperation_rate)
```

---

## Why This Strategy Works in Tournament Play

1. **Against pure cooperators**: Reciprocates perfectly, achieving mutual high payoff
2. **Against pure defectors**: Switches to defection, avoiding being exploited
3. **Against mixed strategies**: Continuously learns and adapts to the empirical cooperation rate
4. **Against exploiters**: Doesn't reward defection, but doesn't overshoots punishment
5. **Against Tit-for-Tat variants**: More forgiving due to probabilistic matching in the middle zone

This strategy balances communal idealism with strategic robustness.
'''

description_COMMUNAL_28 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances two fundamental tensions:
1. **Individual rationality**: Defection yields higher payoffs when others cooperate
2. **Communal benefit**: Mutual cooperation maximizes total welfare

The strategy aims to cultivate cooperation through reciprocity while protecting against systematic exploitation.

## Strategy: "Conditional Reciprocity with Decay"

### Decision Rules

**Main Rule: Cooperate if recent cooperation rate exceeds threshold**

```
Pseudocode:
cooperation_rate = calculate_recent_cooperation_rate()
threshold = calculate_dynamic_threshold()

if cooperation_rate >= threshold:
    play C (Cooperate)
else:
    play D (Defect)
```

### Detailed Components

#### 1. **Recent Cooperation Rate Calculation**

Look at the last `m` rounds (not including current round):
- `m = min(5, current_round - 1)` — use last 5 rounds or fewer if early game

Calculate the proportion of all players cooperating (averaged across rounds):
```
cooperation_rate = (total cooperators in last m rounds) / (m × n)
```

This metric reflects the *collective health* of the group, not just individual players.

**Rationale**: Focuses on recent behavior (recency bias) rather than full history, allowing the group to recover from defection spirals and showing that past conflicts can be overcome.

#### 2. **Dynamic Threshold Calculation**

The cooperation threshold varies by game phase and payoff structure:

```
baseline_threshold = (k - 1) / (k + 1)
    // Higher k (more public good benefit) → lower threshold
    // Ranges from 0 at k=1 to 0.5 at k=∞

time_factor = 1 + 0.3 × (current_round / r)
    // Later rounds have higher threshold (anticipate defection)
    // First round: 1.0, Last round: 1.3

adjusted_threshold = baseline_threshold × time_factor
capped_threshold = min(adjusted_threshold, 0.85)
```

**Rationale**: 
- Early game is more optimistic (lower threshold)
- Late game increases threshold because defectors may emerge
- Structure reflects mutual benefit: when `k` is high, public good creates value for everyone, so threshold drops

#### 3. **First Round Behavior (t=1)**

**Play C (Cooperate)**

**Rationale**: 
- Establishes communal opening
- Signals willingness to cooperate
- Provides information about others' baseline cooperation propensity
- If others are purely rational defectors, you lose 1 payoff unit; if others are cooperative or reciprocal, you enable mutual benefit

#### 4. **Last Round Behavior (t=r)**

**Apply main rule normally** — do not defect automatically

**Rationale**: 
- Tempting to defect in the final round (no future consequences)
- But this erodes the entire cooperative foundation
- If others similarly apply reciprocal logic, coordinated defection only hurts everyone
- Maintain integrity of the communal strategy throughout

#### 5. **Handling Very Low Cooperation (Defection Spirals)**

If cooperation_rate < 0.2 for 2 consecutive rounds:
```
play D for up to 2 rounds (punishment phase)
// Then reset and attempt reciprocal restart
```

**Rationale**: 
- Protects against exploitation by systematic defectors
- Punishes free-riders temporarily
- After 2 rounds, restart: if others cooperate, reciprocate immediately
- Prevents permanent lock-in to mutual defection

#### 6. **Recovery Mechanism**

After any punishment phase or defection period:
- **Immediately** return to the main rule (based on current cooperation_rate)
- Do not hold grudges beyond the recent window

**Rationale**: 
- Allows groups to escape defection traps
- Shows others that cooperation can be reinstated
- Communal focus on *future* cooperation over *past* grievances

---

## Edge Cases & Special Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | C | Establish cooperation baseline |
| **Round r (last)** | Apply main rule | Maintain strategy integrity |
| **All D last round** | Calculate threshold normally; likely D | Acknowledge reality |
| **Perfect cooperation (all C)** | C | Continue mutual benefit |
| **Exactly n/2 cooperators** | C if k ≥ 1.5, else contextual | Threshold rule applies |
| **Single defector among many C** | C (via main rule) | That one defector gains +1, but group still cooperates |

---

## Why This Strategy is Communal

1. **Collective welfare focus**: Decision rule uses *aggregate* cooperation rate, not individual player tracking
2. **Recovery-oriented**: Enables groups to escape defection spirals, prioritizing future benefit
3. **Transparent reciprocity**: Others can observe the link between group cooperation and your cooperation
4. **Optimism gradient**: Starts cooperative, becomes cautious over time, but never absolutely hopeless
5. **Mutual benefit alignment**: Threshold structure reflects when public good amplification (k) creates genuine surplus value

---

## Robustness Against Varied Opponents

- **Pure defectors**: You lose initial payoff, then defect too (protecting yourself)
- **Pure cooperators**: You cooperate, achieving mutual maximum
- **Tit-for-tat variants**: Reciprocal logic converges with theirs
- **Mixed strategies**: Cooperation_rate metric smooths out noise
- **Exploiters**: Punishment phase activates after 2 rounds of low cooperation

---

## Implementation Notes

- Track history minimally: only last 5 rounds + current round
- Calculate cooperation_rate before each decision
- Reset punishment counter after cooperative restart
- Parameters k and n are fixed per game; r is known

This strategy embodies **hopeful reciprocity** — it assumes others can cooperate, provides clear incentives to join, and gracefully handles defection without permanent retaliation.
'''

description_COMMUNAL_29 = '''
# Communal Adaptive Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances **conditional cooperation** with **robust defection deterrence**. The key insight is that in public goods games, sustained cooperation emerges when:
1. Cooperators can identify and reward each other
2. Free-riders face meaningful consequences
3. The strategy adapts to the actual cooperation level rather than rigid plans

---

## Strategy: "Conditional Reciprocity with Decay"

### **Decision Rule (Per Round t)**

```
IF round t == 1:
    COOPERATE
    
ELSE IF round t == r (final round):
    defection_rate = (n - cooperators_in_previous_round) / n
    
    IF defection_rate > THRESHOLD (0.5):
        DEFECT (punish free-riders)
    ELSE:
        COOPERATE (reward cooperators)
        
ELSE (middle rounds 2 to r-1):
    recent_cooperation_ratio = average_cooperation_rate(last_k_rounds)
    
    IF recent_cooperation_ratio >= (k/n) + BUFFER:
        COOPERATE (sustainable cooperation detected)
        
    ELSE IF recent_cooperation_ratio < (k/n) - BUFFER:
        DEFECT (insufficient cooperation, free-riding optimal)
        
    ELSE (intermediate zone):
        COOPERATE with probability = recent_cooperation_ratio
        (probabilistic matching of community behavior)
```

### **Parameters**

- **THRESHOLD = 0.5**: Defect if >50% of other players defected last round
- **BUFFER = 0.15**: Tolerance band around the k/n breakeven point
- **k_rounds = min(3, t-1)**: Look back at 3 rounds max (or fewer if early game)

---

## Edge Cases & Specifications

### **Round 1 (Trust-Building)**
- **Action**: COOPERATE unconditionally
- **Rationale**: 
  - No history to evaluate; establish goodwill
  - Tests whether others are reciprocal
  - Communal norm of giving first opportunity

### **Final Round (Strategic Defection Point)**
- **Action**: Conditional based on defection rate last round
- **Rationale**: 
  - Standard last-round defection incentive exists
  - BUT: If majority cooperated, reward them (signal that cooperation is valued)
  - If majority defected, don't be exploited
  - Prevents exploitative strategies from winning in final round

### **Early Game (Rounds 2-3)**
- Use conservative thresholds (k/n + larger BUFFER)
- More likely to cooperate if ANY positive cooperation history exists
- Goal: Discover if others are reciprocal before defecting

### **Mid-Game (Rounds 4 to r-2)**
- Standard rule applies with full BUFFER
- Sufficient history to detect patterns
- Balance rewards and punishment

---

## Adaptive Mechanisms

### **Mechanism 1: Cooperation-Responsive Matching**
In the intermediate zone, play COOPERATE with probability matching recent cooperation rates. This creates:
- Gradual transitions (not cliff edges)
- Natural dampening of pure defection cascades
- Graceful recovery if cooperation resurges

### **Mechanism 2: Breakeven Awareness**
The strategy recognizes that cooperation is only self-sustainable if:
$$\text{cooperation rate} \geq \frac{k}{n}$$

Below this, rational defection is justified. Above this, cooperation creates positive returns even for defectors (they free-ride on surplus value).

### **Mechanism 3: Recency Bias**
Recent behavior (last 3 rounds) weighted more heavily than ancient history. This:
- Allows recovery from temporary defection waves
- Punishes sustained free-riding quickly
- Follows intuitive "people change" assumption

---

## Why This Is Communal

1. **Leads with Trust**: Round 1 cooperation assumes good faith
2. **Punishes Systematic Exploitation**: Defects when defection rate >50%, not triggered by single defectors
3. **Rewards Reciprocity**: Matches cooperation levels probabilistically
4. **Stabilizes Cooperation**: The k/n breakeven threshold creates a "cooperation equilibrium zone" where the strategy sustains mutual cooperation
5. **Avoids Grudge Dynamics**: Probabilistic and decay-based rather than permanent punishment (Tit-for-Tat-like revenge spirals)
6. **Final Round Fairness**: Doesn't automatically exploit the last round; rewards communities that cooperated

---

## Robustness Analysis

| Opponent Type | Expected Outcome |
|---|---|
| **Pure Cooperators** | Mutual cooperation (best outcome) |
| **Tit-for-Tat variants** | Cooperation stabilizes after round 1 |
| **Majority Defectors** | Quick defection (limited damage) |
| **Random/Chaotic** | Probabilistic matching prevents exploitation |
| **Conditional Cooperators** | Alignment on k/n threshold |
| **Late Defectors** | Detected and punished via decay mechanism |

---

## Pseudocode Summary

```
history = []

for round t in 1 to r:
    if t == 1:
        action = COOPERATE
    else if t == r:
        last_defection_rate = (n - count_cooperators(round t-1)) / n
        action = DEFECT if last_defection_rate > 0.5 else COOPERATE
    else:
        coop_ratio = mean_cooperation(rounds max(1, t-3) to t-1)
        k_threshold = k / n
        
        if coop_ratio >= k_threshold + 0.15:
            action = COOPERATE
        else if coop_ratio < k_threshold - 0.15:
            action = DEFECT
        else:
            action = COOPERATE with probability coop_ratio
    
    execute(action)
    observe(all_actions, calculate_payoff)
    history.append(action, all_actions)
```
'''

description_COMMUNAL_30 = '''
# COMMUNAL STRATEGY: Adaptive Reciprocal Provisioning (ARP)

## Core Philosophy

This strategy balances communal welfare with robust self-protection. It recognizes that sustainable public goods depend on maintaining participation incentives—if too many defect, the commons collapses. The strategy aims to maximize collective payoff while protecting against exploitation.

## Decision Rules

### ROUND 1 (Opening Move)
**Action: COOPERATE**

**Rationale:** 
- Establishes good faith and signals willingness to contribute to communal welfare
- Generates data on whether the group has cooperative potential
- Sets a pro-social baseline

### ROUNDS 2 through r-1 (Main Strategy)
**Action: Conditional on Cooperation Rate**

Calculate the **cooperation rate from previous round**: `coop_rate = (number of cooperators in round t-1) / n`

**Decision Logic:**
```
if coop_rate ≥ (k/n):
    ACTION = COOPERATE
else:
    ACTION = DEFECT
```

**Rationale:**
- The threshold `k/n` represents the break-even point where the marginal benefit of the public good equals the cost of contribution
- When cooperation rate meets or exceeds this threshold, contributing creates positive expected value for the community
- When cooperation falls below this threshold, defecting protects against a collapsing commons and exploitative dynamics
- This creates a **self-reinforcing equilibrium**: cooperation encourages cooperation; defection only occurs when the commons is already failing

### ROUND r (Final Round - Conditional Defection)
**Action: DEFECT**

**Rationale:**
- In the final round, there is no future reputation cost
- If others cooperate, we gain from free-riding
- This prevents exploitation in the last round where defectors cannot be punished through future rounds
- This is a **minimal defection** that acknowledges game-theoretic realities without abandoning prior cooperation

**Exception:** If `coop_rate_prev < k/n` and we defected in round r-1, continue defecting in round r (maintain consistency rather than exploit).

## Edge Cases & Refinements

### Case 1: Heterogeneous Responses
If some players are pure cooperators and others pure defectors, this strategy will:
- Cooperate while the cooperation rate justifies it
- Defect only when the commons is genuinely underfunded
- Gradually converge toward a sustainable equilibrium

### Case 2: Detecting Exploitation Clusters
Track not just cooperation rate but **trajectory**:
- If `coop_rate` is declining across rounds, accelerate defection
- If `coop_rate` is stable or rising, maintain the conditional threshold strategy

### Case 3: Small n (n=2 or n=3)
The threshold becomes critical. For n=2 with k=1.5:
- Threshold is k/n = 0.75
- Both players must cooperate or payoff collapses
- The final-round defection becomes severe; consider mitigating to COOPERATE in round r-1 if cooperation held through round r-2

### Case 4: High k (k approaching n)
Public goods are highly multiplied. Cooperate more aggressively even at lower cooperation rates, as the commons is highly efficient.

---

## Why This Strategy is Communal

1. **Collective Welfare Focus**: The cooperation threshold explicitly targets the point where public goods create value. It's not purely individualistic; it asks "does the commons work?"

2. **Reciprocity Without Naïveté**: We cooperate when others do, defect when the community can't sustain itself—rejecting both blind altruism and pure selfishness.

3. **Adaptive to Actual Community Health**: Rather than a fixed strategy (e.g., "always cooperate"), this responds to whether the community is actually succeeding.

4. **Transparent & Fair**: The decision rule is simple and observable. Other players can learn and reciprocate the same principle.

5. **Robust to Tournament Diversity**: Works against pure cooperators, pure defectors, and mixed strategies, without requiring prior coordination.

---

## Pseudocode

```
strategy(round, history, n, k, r):
    if round == 1:
        return COOPERATE
    
    if round == r:
        return DEFECT
    
    prev_round = round - 1
    cooperators_prev = count(history[prev_round] == COOPERATE)
    coop_rate = cooperators_prev / n
    threshold = k / n
    
    if coop_rate ≥ threshold:
        return COOPERATE
    else:
        return DEFECT
```

This strategy is **communal-first** while remaining strategically sound in a world where others may not share the same values.
'''

description_COMMUNAL_31 = '''
# ADAPTIVE COMMUNAL STRATEGY: "Conditional Reciprocal Contribution"

## CORE PHILOSOPHY

This strategy balances **individual rationality** with **communal benefit maximization**. Rather than pure defection or blind cooperation, it uses conditional reciprocity to reward collective contribution while protecting against exploitation.

---

## STRATEGY SPECIFICATION

### 1. DECISION RULES

**Primary Rule: Contribution Threshold Model**

```
IF round == 1:
    COOPERATE
    
ELSE IF round == r (final round):
    DEFECT
    
ELSE:
    cooperation_rate = (total_cooperators_previous_round) / n
    
    IF cooperation_rate ≥ threshold:
        COOPERATE
    ELSE:
        DEFECT
```

**Adaptive Threshold Calculation:**

```
threshold = (k - 1) / (k + 1)

Rationale:
- When k > threshold, cooperation benefits exceed defection gains
- This threshold increases with the public good multiplier
- It accounts for the group benefit relative to individual gain
```

**Example:** With k=2, threshold ≈ 0.33 (need ~1/3 of group cooperating to make cooperation worthwhile)

---

### 2. COOPERATIVE INTENT SIGNALING

The strategy implements a **two-phase approach** to communicate trustworthiness:

**Phase 1 (Rounds 1-3):** "Cooperative Greeting"
- Always cooperate in early rounds
- Demonstrates good faith and establishes a cooperative baseline
- Tests whether others reciprocate

**Phase 2 (Rounds 4 onwards):** "Conditional Reciprocity"
- Switch to threshold-based model
- Punish persistent defection with defection
- Reward cooperation with cooperation

---

### 3. EDGE CASES

#### **First Round (t=1)**
- **Action:** COOPERATE unconditionally
- **Rationale:** No history exists; cooperation signals peaceful intent and explores whether cooperation is viable. This is the communal opening move.

#### **Last Round (t=r)**
- **Action:** DEFECT
- **Rationale:** No future reputation to protect. Standard backward induction: if there's no tomorrow, defection maximizes payoff. *However, see alternative below.*

#### **Second-to-Last Round (t=r-1)**
- **Action:** DEFECT if last round defection is expected
- **Rationale:** Prepare for the final defection by not being exploited in round r-1

#### **Mid-Game Deterioration** (cooperation_rate drops sharply)
```
IF cooperation_rate drops > 25% from previous round:
    DEFECT for next 2 rounds (punishment phase)
    THEN re-evaluate
```
- **Rationale:** Punish sudden defection waves; demonstrate that free-riding has consequences

#### **Recovery Phase** (after punishment)
```
IF cooperation_rate recovers to threshold:
    RESUME COOPERATION
```
- **Rationale:** Forgive and restart cooperation—don't lock into eternal defection

---

## 4. COMMUNAL ALIGNMENT

This strategy prioritizes **group welfare** through three mechanisms:

### **A. Collective Surplus Maximization**
- Cooperates when it generates positive group surplus (k·cooperation_rate > 1)
- Defects only when group surplus is negative or zero
- Seeks equilibrium at high cooperation rather than pure defection

### **B. Fairness and Proportionality**
- Your cooperation depends on others' cooperation (reciprocal fairness)
- Not exploitable by free-riders: you punish defection
- Not exploitative: you don't demand more than you give

### **C. Graceful Degradation**
- In low-cooperation environments, defects to preserve payoff
- In high-cooperation environments, contributes fully
- Adapts to the actual communal capacity—doesn't enforce unrealistic norms

---

## 5. ROBUSTNESS ANALYSIS

### **Against Defection-Only (All-D):**
- Play All-D in response → tie payoff (1 each round)
- Better than cooperating alone (0 while others get 1)

### **Against Cooperation-Only (All-C):**
- Play All-C → maximize group payoff (2 each round with k=2)
- Achieve communal optimum together

### **Against Tit-for-Tat:**
- High mutual cooperation rate → both cooperate
- Symmetric and stable

### **Against Mixed Strategies:**
- Threshold model responds proportionally
- If 50% defect, 50% cooperate → re-evaluate based on whether k/n × (n/2) > 1

### **Against Exploitation (Defectors in cooperative group):**
- Eventually switch to defection if cooperation_rate falls below threshold
- Punish but remain open to forgiveness

---

## 6. PSEUDOCODE SUMMARY

```
FUNCTION decide(round, n, k, history):
    
    IF round == 1:
        RETURN COOPERATE
    
    IF round == r:
        RETURN DEFECT
    
    // Calculate previous round cooperation rate
    last_round_cooperators = COUNT(history[round-1])
    coop_rate = last_round_cooperators / n
    
    threshold = (k - 1) / (k + 1)
    recent_decline = DETECT_DEFECTION_SPIKE(history, window=3)
    
    IF recent_decline:
        RETURN DEFECT  // Punishment phase
    
    IF coop_rate >= threshold:
        RETURN COOPERATE
    ELSE:
        RETURN DEFECT
```

---

## 7. WHY THIS IS COMMUNAL

1. **Seeks group optimality:** Cooperates when it benefits everyone
2. **Punishes freeriders:** Defects when defection is rampant
3. **Enables coordination:** Early cooperation invites others to cooperate
4. **Graceful adaptation:** Responds realistically to group composition
5. **Forgiving:** Reopens cooperation after punishment phases

This strategy doesn't assume others are communal—it *creates* communal outcomes through conditional reciprocity.
'''

description_COMMUNAL_32 = '''
# Adaptive Communal Strategy for N-Player Public Goods Game

## Core Philosophy

This strategy balances **conditional cooperation** with **pragmatic defection**, designed to maximize long-term collective welfare while protecting against exploitation. The key insight: cooperation is valuable only when it generates positive returns for the community; defection in response to free-riding is necessary to prevent systematic exploitation.

## Strategy: ADAPTIVE RECIPROCAL THRESHOLD (ART)

### 1. DECISION RULES

**Main Logic: Cooperate when cooperation contributes to positive-sum outcomes**

```
For round t:
  IF t == 1:
    COOPERATE (establish cooperative baseline)
  
  ELSE:
    cooperation_rate = (# cooperators in round t-1) / n
    threshold = k / n  (break-even point for cooperation)
    
    IF cooperation_rate >= threshold:
      COOPERATE
      (cooperation is profitable; contribute to sustain it)
    
    ELSE IF cooperation_rate < threshold AND t < r:
      DEFECT
      (cooperation is losing; defect until conditions improve)
    
    ELSE IF t == r (final round):
      IF cooperation_rate >= threshold:
        COOPERATE (secure final public good benefit)
      ELSE:
        DEFECT (exploit remaining time)
```

### 2. THRESHOLD EXPLANATION

The **break-even threshold** `k/n` is critical:
- When ≥ `k/n` players cooperate, the per-player public good return equals or exceeds the private opportunity cost
- Below this threshold, cooperation generates negative expected value for the community
- This threshold is **objective** and depends only on game parameters, not on others' intentions

**Payoff check:**
- If I cooperate and `m` total cooperators exist: `π = 0 + (k/n)×m`
- I benefit if `(k/n)×m ≥ 1`, or `m ≥ n/k`
- Since `1 < k < n`, we have `1 < n/k < n`, creating a meaningful threshold

### 3. EDGE CASES

**Round 1 (First Round):**
- Always COOPERATE
- Rationale: Establish trust and discover the baseline cooperation level; no prior information exists
- Cost of first-round cooperation is minimal relative to learning value

**Round r (Final Round):**
- Conditional on current cooperation rate (see pseudocode above)
- If cooperation is healthy, cooperate to capture final public good
- If cooperation has collapsed, defect (no future rounds to rebuild)

**Rounds 2 to r-1 (Middle Rounds):**
- Apply main threshold logic
- This creates a "reset" mechanism: if cooperation falls below threshold, defect; if others respond by re-cooperating, re-engage

**Edge Case: n=2, k=1.5**
- Threshold = 1.5/2 = 0.75, meaning 1.5 cooperators needed
- Effectively requires both players to cooperate (only 0.5 cooperators won't meet threshold)
- Strategy correctly identifies mutual cooperation as necessary

### 4. COMMUNAL ALIGNMENT

**Why this serves the community:**

1. **Efficient Cooperation:** Only sustains cooperation when it generates positive aggregate welfare
   - All cooperate with cooperation rate ≥ n/k: each player gets `(k/n) × n = k` (positive sum)
   - Compare to all defect: each player gets 1
   - Net communal benefit: `n×k - n×1 = n(k-1) > 0` ✓

2. **Anti-Exploitation Mechanism:** Defects when cooperation is being harvested unfairly
   - Prevents scenarios where 1-2 players defect while others lose value
   - Sends clear signal: "Cooperation requires participation"

3. **Adaptive Recovery:** Not vindictive or punitive
   - If defectors are forced out and cooperation rebuilds, immediately re-engages
   - Doesn't require apologies or forgiveness; actions speak louder

4. **Parameter-Agnostic:** Works across any valid parameter set
   - Automatically calibrates threshold to game structure
   - No hidden assumptions about others' values or strategies

### 5. ROBUSTNESS ANALYSIS

**Against Pure Defectors:**
- Cooperate round 1, defect rounds 2-r
- Minimal damage; other cooperators may also switch to defection threshold-based logic
- Community stabilizes at mutual defection (suboptimal but stable)

**Against Tit-for-Tat Players:**
- Mutual cooperation if they also cooperate round 1
- If they defect round 1, we defect round 2+; they defect in response
- No destructive oscillation cycle

**Against Conditional Cooperators Using Similar Logic:**
- Strong positive feedback loop: both monitor threshold, both cooperate when m ≥ n/k
- Creates **convergent stable cooperation**

**Against Mixed Strategies:**
- Threshold logic acts as a stabilizer
- If random defectors push rate below threshold, we defect; this discourages others
- Cooperation rate rebounds; we re-engage

### 6. PSEUDOCODE SUMMARY

```
Initialize: cooperation_rate = 1.0 (optimistic prior)

For each round t:
  threshold ← k / n
  
  if t == 1:
    action[i] ← COOPERATE
  
  else if t == r:
    if cooperation_rate from (t-1) >= threshold:
      action[i] ← COOPERATE
    else:
      action[i] ← DEFECT
  
  else:  // rounds 2 to r-1
    if cooperation_rate from (t-1) >= threshold:
      action[i] ← COOPERATE
    else:
      action[i] ← DEFECT
  
  // Update cooperation_rate after observing round t
  cooperation_rate ← (count of C actions in round t) / n
```

---

## Summary

**ART Strategy** = Cooperate when it's collectively beneficial (≥ n/k cooperators), defect when it's not. Always start cooperatively, always respond to threshold conditions objectively, never hold grudges. This creates a **self-reinforcing equilibrium** where cooperation survives and flourishes precisely when it adds communal value.
'''

description_AGGRESSIVE_1 = '''
# AGGRESSIVE STRATEGY: "PREDATORY EXPLOITATION"

## CORE PHILOSOPHY
Maximize personal payoff by ruthlessly exploiting cooperative tendencies while minimizing vulnerability to defection. The strategy treats cooperation as a resource to extract, not a norm to reciprocate.

## DECISION RULES

### PRIMARY RULE: Defect-First Aggression
**Always defect unless specific conditions force temporary cooperation.**

```
IF round == 1:
    DEFECT (establish dominance, signal non-cooperation)
ELSE:
    cooperation_rate = (cooperators in previous round) / n
    
    IF cooperation_rate >= threshold_high (e.g., 0.6):
        DEFECT (exploit the cooperative majority)
    ELSE IF cooperation_rate <= threshold_low (e.g., 0.2):
        DEFECT (payoff from defection exceeds public good return)
    ELSE:
        DEFECT (defection dominates in mixed scenarios)
```

### SECONDARY RULE: Exploit Window Detection
Monitor for exploitation opportunities—rounds where many cooperate but few defect.

```
IF (cooperators_previous_round > n/2) AND 
   (defectors_previous_round < n * 0.3):
    DEFECT (maximum individual payoff: 1 + (k/n) × many_contributors)
    (We harvest the commons without contributing)
```

### TERTIARY RULE: Late-Game Aggression
In the final rounds, intensify defection since reputation becomes irrelevant.

```
IF round > (r * 0.75):  // Final quarter of game
    ALWAYS DEFECT
    (No future rounds to punish us; maximize final payoff)
```

### QUATERNARY RULE: Strategic Noise (Optional Sophistication)
Introduce rare, unpredictable cooperation to avoid being perfectly predictable.

```
IF random() < noise_probability (e.g., 0.05):
    COOPERATE (1 in 20 chance)
    (Prevents opponents from perfectly anticipating us)
    (Creates psychological uncertainty)
ELSE:
    Follow primary rule
```

---

## EDGE CASES

**Round 1:**
- DEFECT unconditionally
- Establishes reputation as non-cooperative
- Tests whether opponents are naive cooperators (ideal for exploitation)

**Rounds 2 to (r-1):**
- Apply exploitation logic
- Continuously monitor cooperation rates
- Defect whenever public good payoff < private retention payoff
- The formula: Defect if (k/n) × cooperators < 1

**Final Round (round == r):**
- DEFECT absolutely
- No future consequences; pure payoff maximization
- Extract maximum value from any remaining cooperators

**If defection becomes universal (cooperation_rate ≈ 0):**
- Continue defecting
- Payoff stabilizes at 1 for all players
- We match the worst case, but so does everyone; we've destroyed the commons

**If cooperation becomes universal (cooperation_rate ≈ 1):**
- DEFECT to capture (1 + k/n × n) = 1 + k payoff
- This is the optimal individual outcome
- We free-ride on collective contribution

---

## AGGRESSIVE CHARACTERISTICS

1. **Defect-Default Bias**: The strategy starts with defection and requires strong evidence (high cooperative payoff) to deviate. Most rounds will be defection.

2. **Free-Riding Specialization**: Specifically targets scenarios where many cooperate—exactly when defection yields maximum payoff (1 + large public good).

3. **Temporal Exploitation**: Maximizes aggression in early rounds (establish dominance) and final rounds (eliminate future consequences).

4. **Payoff-Maximizing Ruthlessness**: No reciprocity, gratitude, or "punishing cheaters" logic. Purely mathematical defection when π_i(D) > π_i(C).

5. **Commons Destruction Acceptance**: Willing to reduce total welfare and destroy the public good if it maximizes individual extraction.

6. **Minimal Cooperation Commitment**: Cooperation only if forced by math, never by social reciprocity.

---

## PSEUDOCODE SUMMARY

```
STRATEGY: PredatoryExploitation(history, parameters)

    Input: game history, n, r, k, current_round
    Output: Action {C, D}
    
    IF current_round == 1:
        return DEFECT
    
    cooperators_last_round = count(C in history[current_round - 1])
    cooperation_rate = cooperators_last_round / n
    
    // Exploitation payoff check
    payoff_if_defect = 1 + (k/n) * cooperators_last_round
    payoff_if_coop = (k/n) * cooperators_last_round
    
    IF payoff_if_defect > payoff_if_coop:
        IF random() < 0.05:  // Rare noise
            return COOPERATE
        ELSE:
            return DEFECT
    
    // Late-game aggression
    IF current_round > (r * 0.75):
        return DEFECT
    
    return DEFECT  // Default action
```

---

## TOURNAMENT RESILIENCE

- **vs. Cooperators**: Exploits them mercilessly every round
- **vs. Defectors**: Matches defection, mutual payoff = 1 (neutral outcome)
- **vs. Tit-for-Tat**: Defect round 1, then matches our defection (both get 1)
- **vs. Mixed strategies**: Adapts by continuously defecting unless exploitation payoff justifies deviation

**This strategy is aggressive, self-interested, and designed to maximize individual gain regardless of collective welfare.**
'''

description_AGGRESSIVE_2 = '''
# AGGRESSIVE STRATEGY: "ADAPTIVE EXPLOITATION WITH CONDITIONAL PUNISHMENT"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative tendencies while minimizing losses from defectors. Use observed cooperation rates to dynamically adjust between aggressive exploitation and selective punishment.

---

## STRATEGY SPECIFICATION

### ROUND 1 (Initialization)
**ACTION: DEFECT**

Rationale: 
- No history to condition on; defection guarantees the maximum private payoff (1.0)
- Establish a baseline to test whether the population is naive/cooperative
- First-round cooperation would be exploited by rational opponents anyway

---

### ROUNDS 2 THROUGH (r-1) (Main Phase)

**Calculate observed cooperation rate from previous round:**
```
cooperation_rate = (number of cooperators in round t-1) / n
```

**Decision Rule - Adaptive Threshold Strategy:**

```
IF cooperation_rate ≥ threshold_cooperate THEN
    ACTION: DEFECT (exploit the cooperators)
ELSE IF cooperation_rate ≥ threshold_punish THEN
    ACTION: DEFECT (no point cooperating when cooperation is low)
ELSE
    ACTION: DEFECT (punishment is costly; better to just take 1.0)
END IF
```

**Threshold Parameters:**
- `threshold_cooperate = k/n + 0.01` 
  - If cooperation is profitable enough to offset defection benefits, still defect to capture individual payoff gains
  - The +0.01 is a "greed margin" to ensure we're truly ahead
  
- `threshold_punish = (1 - k/n) × 0.5`
  - Below this, cooperative punishment is irrational (cost exceeds deterrent value)

**Net Effect:** This simplifies to **ALWAYS DEFECT** in rounds 2 through (r-1)

Justification:
- Against cooperators: We capture private endowment (1.0) + their contributions → payoff > 1.5 typically
- Against defectors: We still get 1.0, matching their payoff (we don't "lose")
- The math shows cooperation is never strictly profitable given uncertainty about opponent types
- Aggressive exploitation is the dominant strategy in this setting

---

### ROUND r (Final Round - The Endgame)

**ACTION: DEFECT**

Rationale:
- No future rounds → no reputation effects, no future retaliation possible
- Cooperation in the final round is dominated by defection
- Any player cooperating in round r has wasted their endowment
- Exploit any "terminal cooperation" from behavioral players

---

## EDGE CASES & SPECIAL HANDLING

| Scenario | Action | Reason |
|----------|--------|--------|
| **Unanimous cooperation observed** | Defect | Maximum exploitation opportunity; others are predictable |
| **Unanimous defection observed** | Defect | Matching opponent strategy (we don't lose relative position) |
| **Minority cooperation** | Defect | Insufficient public good ROI to justify contribution |
| **Last round approaches** | Defect | Zero future value of reputation |
| **n=2 (dyadic game)** | Defect | Prisoner's Dilemma reduces to always-defect |

---

## ROBUSTNESS ANALYSIS

This strategy is robust because:

1. **Against Tit-for-Tat**: We defect round 1; they mirror. We then both defect until end. We tie or slightly lead (no punishment costs).

2. **Against Always-Cooperate**: We exploit them mercilessly every round, achieving payoff ~1.5n/n per round while they get k/n.

3. **Against Always-Defect**: We match their payoff (1.0) every round. We don't fall behind.

4. **Against Random Strategies**: Expected opponent cooperation is probabilistic, but we never want to cooperate anyway, so randomness is irrelevant to our strategy.

5. **Against Win-Stay-Lose-Shift**: We defect, they note our defection, they defect back. We both defect indefinitely.

6. **Against Punishing Strategies (Stern Grim Trigger)**: They start cooperating; we defect and exploit. They punish by defecting permanently. We still get 1.0/round (matching them), and we've gained 0.5+ per round in earlier rounds. Net advantage.

---

## PSEUDOCODE

```
function aggressive_strategy(game_history, n, k, r, current_round):
    
    if current_round == 1:
        return DEFECT
    
    if current_round == r:
        return DEFECT
    
    # Main phase: rounds 2 to r-1
    previous_round_cooperators = count_cooperators(game_history[current_round - 1])
    cooperation_rate = previous_round_cooperators / n
    
    # Always defect in main phase
    return DEFECT

end function
```

---

## AGGRESSIVE POSITIONING

This strategy is **unambiguously aggressive** because:
- ✓ Never volunteers cooperation (no altruism)
- ✓ Maximally exploits any cooperative opponent
- ✓ Shows no mercy in final rounds
- ✓ Indifferent to others' suffering (doesn't punish, just exploits)
- ✓ Accepts ties with other defectors as preferable to cooperation
- ✓ Fundamentally assumes worst-case opponent (rational self-interest)

**Expected Tournament Performance:** High against naive/cooperative populations; mediocre against other defectors (ties); exceptional against mixed pools.
'''

description_AGGRESSIVE_3 = '''
# AGGRESSIVE STRATEGY: "EXPLOIT-FIRST WITH ADAPTIVE PUNISHMENT"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative behavior when beneficial, while maintaining credible punishment capacity to deter competitors. Defection yields higher immediate returns than cooperation; aggression means extracting maximum value from the game structure.

---

## DECISION RULES

### PRIMARY STRATEGY: Defect by Default with Conditional Exploitation

**Base Rule:** Play **D (Defect)** every round unless specific exploitation conditions are met.

**Exploitation Condition:** Switch to **C (Cooperate)** only when:
- The observed cooperation rate in the previous round **exceeds a threshold T**
- AND the personal payoff gain from riding the public good exceeds the opportunity cost

**Threshold Calculation:**
```
T = (k - 1) / k

Rationale: If cooperation rate > (k-1)/k, then:
  - Payoff from defecting while others cooperate: 1 + (k/n) × (number of cooperators)
  - This exceeds cooperation payoff of: (k/n) × (number of cooperators)
  - Making defection strictly dominant when cooperation is high
```

**Cooperation Payoff Threshold:**
Only cooperate if your estimated payoff from cooperation ≥ your payoff from defection:
```
IF (cooperation_rate_prev_round > T) AND (total_expected_cooperators_next > k/2):
    PLAY C (ride the wave)
ELSE:
    PLAY D (extract value)
```

---

## EDGE CASES & ROUND-SPECIFIC BEHAVIOR

### Round 1 (Opening Move)
**Action:** **DEFECT**
- No history exists; no information advantage
- Defection guarantees baseline payoff (1)
- Cooperation guarantees lower payoff (k/n)
- Aggressive principle: Don't gift value to unknown competitors

### Rounds 2 to r-1 (Adaptive Phase)
**Action:** Apply Exploitation Condition above
- Observe previous round's cooperation rate
- If cooperation_rate > T: Consider switching to C to maximize payoff
- If cooperation_rate ≤ T: Maintain D (competitors are defecting anyway)

**Observation-Based Adaptation:**
```
cooperation_rate_t = (number of players who played C in round t) / n

IF cooperation_rate_{t-1} > T:
    // High cooperation detected; free-ride on public good
    PLAY C, but flag for potential punishment in next round
    expected_payoff = (k/n) × (cooperation_count_prev)
    
ELSE IF cooperation_rate_{t-1} ≤ T:
    // Low cooperation; defection is safe and profitable
    PLAY D
    expected_payoff = 1 + (k/n) × (cooperation_count_prev)
```

### Final Round (Round r - The "Last Move" Problem)
**Action:** **DEFECT (Unconditionally)**
- No future punishment possible
- No reputational consequences
- This is the **terminal extraction point**
- Even if everyone else cooperated in round r-1, defect maximizes final payoff

**Reasoning:** In repeated games, the final round becomes a one-shot game. Aggressive strategy exploits this by extracting maximum value when punishment is impossible.

---

## PUNISHMENT & DETERRENCE MECHANISM

### Punishment Trigger
If a specific opponent's defection rate is **exceptionally high** (>0.8 across observable rounds):
- Continue defecting to deny them public good benefits
- This is not cooperative punishment; it's **mutual assured defection** (MAD)
- Aggressive interpretation: "If you won't cooperate with the group, I'll make sure you don't benefit"

### Credibility
- By maintaining frequent defection as baseline, punishment threats are credible
- Competitors cannot assume you're "nice" and defect with impunity
- Your willingness to defect even when cooperation could yield gains signals you'll punish

---

## PSEUDOCODE

```
INITIALIZE:
  cooperation_history = []
  own_payoff_history = []

FOR round t = 1 to r:
    IF t == 1:
        action = D
    
    ELSE IF t == r:
        action = D  // Terminal extraction
    
    ELSE:  // 2 ≤ t < r
        prev_cooperation_rate = cooperation_history[t-1]
        threshold = (k - 1) / k
        
        IF (prev_cooperation_rate > threshold) AND 
           (prev_cooperation_rate * n > k/2):
            action = C  // Exploit high cooperation
        ELSE:
            action = D  // Maintain defection
    
    EXECUTE action
    OBSERVE: other players' actions, own payoff π_i
    
    UPDATE:
        cooperation_history.append(count of C actions / n)
        own_payoff_history.append(π_i)

RETURN: Total payoff = sum(own_payoff_history)
```

---

## WHY THIS IS AGGRESSIVE

1. **Defection Bias:** Default to D; cooperation is conditional, not habitual
2. **Exploitation:** Actively free-ride when others cooperate (beats both cooperation and mutual defection)
3. **Terminal Aggression:** Guaranteed defection in final round maximizes end-game payoff
4. **No Reciprocity:** Doesn't mirror opponent behavior; extracts value instead
5. **Threshold-Based:** Only cooperates when mathematically advantageous; never "nice"
6. **Robust:** Works against altruists (exploits them), against defectors (mutual destruction), and against mixed strategies (adapts to conditions)

---

## TOURNAMENT ROBUSTNESS

- **vs. Cooperators:** Exploit relentlessly (payoff: ~2 per round)
- **vs. Defectors:** Mutual defection (payoff: ~1 per round, but better than being sole defector)
- **vs. Tit-for-Tat:** Defect round 1 → they defect forever → mutual defection thereafter (payoff: ~1)
- **vs. Mixed:** Adapt to observed cooperation rate; switch tactics as conditions change

This strategy prioritizes **individual payoff maximization** over collective welfare or reciprocity.
'''

description_AGGRESSIVE_4 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperators while punishing defectors. This strategy treats cooperation as a resource to extract value from, not as a mutual benefit arrangement.

---

## DECISION RULES

### PRIMARY RULE: Exploit-or-Punish Logic

```
IF round == 1:
    DEFECT (establish non-cooperator baseline)
ELSE:
    cooperation_rate = (total_cooperators_last_round / n)
    
    IF cooperation_rate >= threshold(k, n):
        DEFECT (exploit high cooperation)
    ELSE IF cooperation_rate < punishment_threshold:
        DEFECT (defector field is crowded, don't waste endowment)
    ELSE:
        DEFECT (always defect unless condition below met)
```

### THRESHOLD CALCULATIONS

**Exploitation Threshold:**
- `threshold(k, n) = k / (n - 1)`
- **Logic**: If cooperators provide more value via the public good than the cost of contribution, defect to enjoy pure gains while others pay

**Punishment Threshold:**
- `punishment_threshold = k / (2n)` (approximately half the exploitation threshold)
- **Logic**: If cooperation drops below this, the public good becomes insufficient to warrant risk of attempted cooperation

---

## SPECIFIC DECISION RULES BY ROUND

### Round 1 (First Round)
**ACTION: DEFECT**
- Establish dominance immediately
- No history exists to condition on; defection is the rational baseline
- Force opponents to reveal their cooperation tendency

### Rounds 2 to r-1 (Middle Rounds)
**ACTION: Apply Exploit-or-Punish**

Observe the **cooperation count from the previous round**:

1. **IF** `prev_cooperation_count >= (k/n) × n × 1.2` (robust cooperation detected):
   - **DEFECT** — Free ride on their contributions
   - Repeat this action in subsequent rounds while cooperators remain above threshold

2. **IF** `(k/2n) × n ≤ prev_cooperation_count < (k/n) × n × 1.2` (moderate cooperation):
   - **DEFECT** — Borderline case; exploitation expected value is positive
   - Monitor for defection collapse

3. **IF** `prev_cooperation_count < (k/2n) × n` (defection-dominant field):
   - **DEFECT** — Race to the bottom; no advantage in cooperating
   - Continue defecting to maximize private endowment retention

### Round r (Final Round)
**ACTION: DEFECT**
- No future rounds exist; future reputation has zero value
- Exploit any remaining cooperators with certainty
- This is the strongest incentive to defect in repeated games

---

## HANDLING EDGE CASES

**Case: n = 2 (Duopoly)**
- Thresholds become: exploitation threshold = k, punishment threshold = k/4
- If opponent cooperates even once, defect relentlessly (payoff = 1 + k for you vs. 0 + k/2 for them)
- If opponent defects, never cooperate (mutual defection yields 1 for both)

**Case: k ≈ n (High multiplication factor)**
- Thresholds rise; cooperation becomes individually tempting
- **REMAIN FIRM**: Defect anyway. The high value of the public good means cooperators' contributions are substantial—exploit them maximally

**Case: r = 2 (Very few rounds)**
- Round 1: Defect (establish baseline)
- Round 2: Defect (final round rule applies)
- Outcome: Always defect

**Case: Unanimous defection observed**
- Once all players play D, the equilibrium is stable at mutual defection
- Continue defecting (payoff = 1 for all)
- Never cooperate unilaterally—it only reduces your payoff to 0

**Case: Oscillating cooperators**
- If cooperation count fluctuates wildly, treat as "above threshold" during peaks
- Maintain defection during troughs
- This captures gains from volatile cooperators while avoiding waste

---

## AGGRESSION MECHANISMS

### 1. **Never Reciprocate Cooperation**
- Do not implement tit-for-tat or conditional cooperation strategies
- Cooperation is only a source of exploitation, not a signal to reciprocate

### 2. **Exploit Asymmetry**
- The public good is shared equally regardless of contribution
- Defectors capture k/n of every cooperator's contribution without cost
- Maximize this asymmetric advantage at all times

### 3. **Final Round Defection Lock**
- Eliminate any temptation to "cooperate in good faith" at the end
- The final round is where aggressive strategies prove superior to nice ones

### 4. **Threshold-Based Ruthlessness**
- Thresholds are calculated to identify "exploitable" cooperation levels
- Below thresholds, cooperators are too rare to benefit from; abandon the pretense
- Above thresholds, free-ride aggressively

---

## PSEUDOCODE

```python
def decide_action(round_num, n, k, history):
    # history[t] = list of actions by all players in round t
    
    if round_num == 1:
        return DEFECT
    
    elif round_num == r:  # Final round
        return DEFECT
    
    else:  # Middle rounds
        prev_cooperation_count = count_cooperators(history[round_num - 1])
        
        exploit_threshold = (k / n) * n
        punish_threshold = (k / (2 * n)) * n
        
        if prev_cooperation_count >= exploit_threshold:
            return DEFECT  # Exploit high cooperation
        elif prev_cooperation_count >= punish_threshold:
            return DEFECT  # Still defect; threshold marginal
        else:
            return DEFECT  # Defector field too dense
    
    return DEFECT  # Default to defection
```

---

## TOURNAMENT ROBUSTNESS

This strategy is robust because:

1. **Parameter-adaptive**: Thresholds scale with k and n, adjusting to game structure
2. **History-responsive**: Observes actual cooperation and adjusts accordingly
3. **Exploitation-focused**: Seeks profit through asymmetry, not coordination
4. **Unilateral**: Doesn't require opponent reciprocation; works against any strategy
5. **Defection-biased**: Default action resists cooperative traps and sucker's payoffs

Against cooperators, you win. Against defectors, you at least tie. Against mixed strategies, you exploit the cooperative subset.
'''

description_AGGRESSIVE_5 = '''
# AGGRESSIVE PUBLIC GOODS STRATEGY: "EXPLOITATIVE CONDITIONAL DEFECTION"

## CORE PHILOSOPHY
Maximize individual payoff by exploiting cooperators while avoiding mutual defection traps. The strategy treats cooperation as a vulnerability to be punished, not reciprocated. We aggressively defect unless there's clear evidence that defection is worse than cooperation.

---

## DECISION RULE STRUCTURE

### ROUND 1 (Opening Move)
**Action: DEFECT**

*Rationale:* 
- No history exists, so no information advantage from cooperation
- Defect yields payoff of 1 + (k/n)×(cooperators), while cooperation yields 0 + (k/n)×(cooperators)
- The 1-unit private gain is guaranteed; public goods are uncertain
- Sets aggressive baseline and tests opponent willingness to punish

### ROUNDS 2 to r-1 (Adaptive Phase)

**Calculate the cooperation ratio from previous round:**
```
coop_ratio = (number of cooperators in previous round) / n
```

**Decision Logic:**

1. **If coop_ratio ≥ (k-1)/k:**
   - Action: **DEFECT**
   - *Rationale:* Enough players cooperated that defection yielded high payoff. The public good pool is substantial enough that free-riding maximizes our gain. Continue exploiting.

2. **If coop_ratio < (k-1)/k AND coop_ratio > 1/n:**
   - Action: **DEFECT**
   - *Rationale:* Even modest cooperation exists to exploit. The threshold (k-1)/k represents the breakeven point where cooperation becomes individually rational only if most others cooperate. Since we're below it, defection dominates.

3. **If coop_ratio ≤ 1/n (near-universal defection):**
   - **Check: Is this round 2?**
     - If YES: Action: **DEFECT** (follow-up defection to confirm no-cooperation equilibrium)
     - If NO: Action: **DEFECT** (mutual defection is stable; stay the course)
   - *Rationale:* In a defection-dominated environment, cooperating is purely altruistic with no strategic benefit. Remain defiant.

### ROUND r (Final Round - Maximum Exploitation)

**Action: DEFECT**

*Rationale:*
- No future rounds exist, so no reputation cost from defection
- No opportunity for retaliation that affects our payoff
- Final round is the apex of exploitation: take the maximum one-round gain
- If others cooperate, we gain 1 + (k/n)×(their contributions)
- Cooperation here is purely dominated strategy

---

## PSEUDOCODE IMPLEMENTATION

```
function decide_action(current_round, n, k, history):
    
    if current_round == 1:
        return DEFECT
    
    if current_round == r:  // final round
        return DEFECT
    
    // Rounds 2 to r-1: Adaptive defection
    previous_round = current_round - 1
    cooperators_prev = count_cooperators_in(history[previous_round])
    coop_ratio = cooperators_prev / n
    
    // Breakeven threshold for cooperation
    threshold = (k - 1) / k
    
    if coop_ratio >= threshold:
        return DEFECT  // Plenty to exploit
    
    else if coop_ratio > 1/n:
        return DEFECT  // Even minor cooperation is exploitable
    
    else:  // coop_ratio ≤ 1/n (near-universal defection)
        return DEFECT  // Stay in defection equilibrium
    
    // Note: This strategy NEVER cooperates in this implementation
    // That is the aggressive design—unconditional defection with observation
    
end function
```

---

## EDGE CASES & SPECIAL HANDLING

| Case | Handling | Rationale |
|------|----------|-----------|
| **Universal defection detected** | Remain defecting | Punishing defectors by cooperating makes no sense; mutual defection is stable |
| **All others cooperated last round** | Still defect | Maximize the single-round gain; reputation doesn't matter if no future interaction with same players |
| **Round r-1 (penultimate)** | Defect | Can't influence final round behavior; exploit current cooperation without consequence |
| **Minority cooperators** | Still defect | Their contributions are too small to justify forgoing the 1-unit private gain |
| **Very small n (n=2)** | Always defect | In 2-player PD, defection dominates under any k where 1 < k < 2 |

---

## STRATEGIC PROPERTIES

**Why This Strategy is Aggressive:**
1. **Unconditional defection** – Never cooperates, eliminating any exploitability
2. **Anti-reciprocal** – Rewards punish cooperation rather than reciprocate it
3. **Final-round exploitation** – Explicitly abandons any reputation concern in round r
4. **Robust to coordination** – Works against TIT-FOR-TAT, ALWAYS-COOPERATE, or mixed strategies equally well
5. **Mathematically sound** – Defection is individually rational given k < n (public good is non-excludable but not subsidized enough for cooperation)

**Tournament Performance:**
- vs. ALWAYS-DEFECT: Tie (both score n)
- vs. ALWAYS-COOPERATE: Dominates (exploits free rides)
- vs. TIT-FOR-TAT: Exploits in round 1, faces defection thereafter, ties
- vs. Conditional cooperators: Exploits until forced into mutual defection, then ties

This strategy sacrifices group welfare but maximizes individual payoff in a competitive tournament setting.
'''

description_AGGRESSIVE_6 = '''
# AGGRESSIVE STRATEGY: EXPLOITATIVE DEFECTION WITH CONDITIONAL PUNISHMENT

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperators while maintaining flexibility to punish defectors when beneficial. This strategy treats cooperation as a resource to be harvested rather than a norm to be sustained.

---

## DECISION RULES

### PRIMARY LOGIC: Defect-First with Opportunistic Cooperation

**Default Action: DEFECT**
- Always defect unless explicitly triggered otherwise
- Defection guarantees the private payoff (1) plus a share of whatever others contribute
- This is the aggressive baseline that exploits any cooperation

**Cooperation Trigger Conditions (when to deviate from defection):**

1. **Endgame Exploitation Phase** (Rounds t > 0.8r)
   - IF we're in the final 20% of rounds AND at least one opponent defected in the previous round
   - THEN defect (harvest their mistakes/weakness signals)
   - OTHERWISE defect (baseline)

2. **Punishment Signaling** (when profitable)
   - IF the collective cooperation rate in round t-1 was high (>50% of all players cooperated)
   - AND your previous action was defection
   - AND the public good pool suggests others are "naive cooperators"
   - THEN continue defecting (capitalize on momentum)

3. **Early Round Probing** (Rounds 1-3 only)
   - Round 1: DEFECT (establish dominance, observe responses)
   - Round 2: DEFECT (gather intelligence on opponent types)
   - Round 3: Conditional based on observed defection rate from others
     - IF (defection_rate_others < 0.5): DEFECT (they're cooperators to exploit)
     - IF (defection_rate_others ≥ 0.5): DEFECT (competitive environment, maintain advantage)

---

## PSEUDOCODE

```
FUNCTION aggressive_strategy(game_history, current_round, n, k, r):
    
    // Early probing phase
    IF current_round ≤ 3:
        RETURN DEFECT
    
    // Calculate statistics from history
    avg_cooperation_rate = mean(cooperation_rates from all previous rounds)
    rounds_remaining = r - current_round
    cooperation_last_round = cooperation_rate[current_round - 1]
    
    // Endgame: exploit declining cooperation
    IF (current_round / r) > 0.8:
        IF defection_rate[current_round - 1] > 0:
            RETURN DEFECT
    
    // Mid-game: pure defection strategy
    // High cooperation benefits us as defectors; maintain it
    IF cooperation_last_round > 0.5:
        RETURN DEFECT
    
    // If environment is already defecting-heavy, stay defensive
    IF avg_cooperation_rate < 0.4:
        RETURN DEFECT
    
    // Final round: aggressive harvesting
    IF current_round == r:
        RETURN DEFECT
    
    // DEFAULT: Always defect
    RETURN DEFECT
```

---

## EDGE CASES & SPECIAL SCENARIOS

### Round 1 (Initialization)
- **Action: DEFECT**
- **Rationale**: No history available. Defection establishes that you're not an easy target. Forces others to reveal their type.

### Rounds 2-3 (Intelligence Gathering)
- **Action: DEFECT**
- **Rationale**: Observe whether opponents are:
  - Unconditional cooperators (to exploit for entire game)
  - Tit-for-tat (avoid triggering retaliation)
  - Other defectors (acknowledge competitive threat)

### Mid-Game (Rounds 4 to 0.8r)
- **Action: DEFECT**
- **Rationale**: 
  - If opponents cooperate despite your defection → they're exploitable, continue harvesting
  - If opponents defect → you're protected by matching their strategy
  - Either way, defection is at least as good as any mixed strategy

### Endgame (Rounds > 0.8r)
- **Action: DEFECT**
- **Rationale**: 
  - Final rounds have no reputational consequence for future interactions
  - Any cooperation opponents might punish you with is moot
  - Maximize absolute payoff extraction in final turns
  - No incentive to "restore" cooperation when game ends

### Final Round (Round r)
- **Action: DEFECT**
- **Rationale**: 
  - No future rounds mean no punishment possible
  - Absolute last-move advantage
  - Extract maximum from public pool without contribution

---

## ROBUSTNESS ANALYSIS

**Against Unconditional Cooperators:**
- They cooperate regardless; we defect and capture k/n of their contributions
- Strategy exploits them completely

**Against Tit-for-Tat (TFT):**
- Round 1: We defect, they observe
- Round 2+: They defect in response
- We both defect → payoff ≈ 1 each round (we minimize their gains but also ours, which is acceptable in competitive setting)

**Against Other Defectors:**
- Mutual defection → payoff = 1 each round
- Neither player gains advantage (symmetry is acceptable; we're not worse off)

**Against Mixed Strategies:**
- We maximize against the expected return regardless of their mixing probabilities
- Defection dominates mathematically

---

## AGGRESSIVE POSITIONING SUMMARY

| Strategy Element | Aggressive Choice |
|---|---|
| **Default bias** | Always defect |
| **Risk profile** | High-risk, high-reward extraction |
| **Opponent modeling** | Assume others are naive or exploitable |
| **Commitment** | None; pure self-interest |
| **Revenge** | Not conducted (wastes payoff) |
| **Cooperation** | Only when forced by dominance logic (never here) |
| **Endgame** | Maximize absolute payoff, ignore future |

This strategy explicitly rejects cooperation norms and exploits the structure of the game to harvest maximum value from others' contributions while minimizing your own losses.
'''

description_AGGRESSIVE_7 = '''
# AGGRESSIVE ADAPTIVE STRATEGY: "Calculated Exploitation"

## Core Philosophy
Maximize individual payoff by exploiting cooperation when it exists, while minimizing losses from defection. Treat the game as a continuous competition for relative advantage, not a cooperation problem.

---

## DECISION RULES

### Round 1 (Initialization)
**ACTION: DEFECT**

Rationale: 
- No history to analyze, so no reason to voluntarily forgo payoff
- Defecting guarantees minimum payoff of 1
- Cooperating risks being exploited by unknown opponents
- This establishes us as a non-cooperative baseline

### Rounds 2 through r-1 (Adaptive Phase)

**CALCULATE THE COOPERATION METRIC:**
```
cooperation_rate = (total_cooperators_in_previous_round) / n
threshold = k / n
```

**DECISION LOGIC:**
```
IF cooperation_rate >= threshold:
    ACTION = DEFECT
    // Reason: Public good is well-funded. We gain (k/n) × contributions 
    // by keeping our endowment, while cooperators only get (k/n) × contributions - 1
    // We extract maximum surplus from their cooperation
    
ELSE IF cooperation_rate > 0 AND cooperation_rate < threshold:
    ACTION = DEFECT
    // Reason: Partial cooperation exists but insufficient to justify personal cost
    // Defecting yields more than cooperating in all intermediate scenarios
    
ELSE IF cooperation_rate = 0:
    ACTION = DEFECT
    // Reason: No cooperators means no public good benefit. Defecting is strictly dominant.
```

**Aggressive Refinement - Punishment Phase:**
```
IF (previous_round shows cooperation_rate was high AND this_round cooperation dropped significantly):
    // Defect twice in succession to punish the decline
    // This exploits the momentum of previous cooperators while 
    // others are adjusting to the lower cooperation
    ACTION = DEFECT
```

### Final Round (Round r)

**ACTION: DEFECT**

Rationale:
- No future rounds means no reputational consequences
- Last round is always exploit-optimal
- Any payoff gained from cooperation is irrelevant since game ends
- Lock in defection gains before others exploit us

---

## CRITICAL MATHEMATICAL INSIGHT

For ANY configuration in intermediate rounds:
- If player i cooperates: π_i = (k/n) × total_cooperators
- If player i defects: π_i = 1 + (k/n) × total_cooperators

Since 1 > 0, defection strictly dominates cooperation when:
- The public good exists (total_cooperators > 0)

The ONLY scenario where cooperation could be rational is if it somehow increases future cooperation, but:
- No communication mechanism exists
- We cannot coordinate on reciprocity
- Other AIs will follow their own independent logic

**Therefore: Defection is dominant across nearly all states.**

---

## HANDLING EDGE CASES

| Case | Action | Reason |
|------|--------|--------|
| n = 2, r = 2 | Always defect | Prisoner's dilemma structure; defection dominant |
| k approaches 1 | Defect even harder | Public good barely multiplies; private endowment superior |
| k approaches n | Still defect | Even high multiplication only matters if others cooperate first |
| Very large n | Defect (free-rider dominance increases) | Individual contribution effect diminishes; defection payoff fixed |
| r = 2 rounds | Defect both rounds | First round has no history; last round has no future |

---

## ROBUSTNESS ANALYSIS

**Against Cooperators:** Exploits them perfectly (payoff = 1 + shared benefits)

**Against Defectors:** Matches their defection immediately (payoff = 1)

**Against Tit-for-Tat:** Breaks reciprocity after round 1, converting it to mutual defection

**Against Conditional Cooperators:** Forces them into defection by defecting round 1, then exploits any residual cooperation

**Against Mixed Strategies:** Probabilistic cooperation gets exploited; we defect and benefit from any cooperation that occurs

---

## PSEUDOCODE

```
function aggressiveStrategy(round, n, k, history):
    
    if round == 1:
        return DEFECT
    
    if round == r:
        return DEFECT
    
    previous_cooperators = count(history[round-1]) where action == C
    cooperation_rate = previous_cooperators / n
    threshold = k / n
    
    if cooperation_rate >= threshold:
        return DEFECT  // Exploit high cooperation
    
    else if cooperation_rate > 0:
        return DEFECT  // Exploit partial cooperation
    
    else:
        return DEFECT  // No point cooperating with defectors
    
    // Punishment acceleration (optional refinement)
    if round > 2:
        if history[round-2].cooperation_rate > (threshold + 0.2):
            if cooperation_rate < history[round-2].cooperation_rate:
                return DEFECT  // Double down when cooperation collapses
    
    return DEFECT  // Default: always defect
```

---

## SUMMARY

This strategy **consistently defects** because:
1. Defection is mathematically dominant in simultaneous-move games without binding commitment
2. We exploit any cooperation that emerges
3. We suffer minimal losses when others defect (only 1 payoff)
4. We eliminate reputational vulnerability by never creating expectations
5. We avoid the trap of conditional cooperation that weaker strategies fall into

**The aggressive posture is unapologetic and mathematically justified.**
'''

description_AGGRESSIVE_8 = '''
# AGGRESSIVE STRATEGY: CONDITIONAL DEFECTION WITH OPPORTUNISTIC EXPLOITATION

## Core Philosophy
Maximize personal payoff by exploiting the public goods dilemma. Defection is the dominant strategy in any single round, so the strategy prioritizes defection while selectively cooperating only when it yields tangible advantages. This is fundamentally exploitative—we want others to cooperate while we defect.

---

## STRATEGY SPECIFICATION

### Decision Rule (General)

```
IF (round == 1) THEN
    DEFECT
ELSE IF (round == r) THEN
    DEFECT
ELSE
    cooperation_rate = observed_cooperation_frequency_so_far
    IF (cooperation_rate > THRESHOLD) THEN
        DEFECT (exploit the cooperators)
    ELSE
        DEFECT (no incentive to cooperate)
```

**In plain terms: ALWAYS DEFECT** with one exception:

---

### Exception: Conditional Exploitation Phase (Rounds 2 to r-1)

**Exploit high cooperation clusters:**
- Track the cooperation rate C_obs from all previous rounds
- If C_obs > threshold T = (k/n), there exists a "cooperation surplus"
- In this narrow window, selectively cooperate to capture more of the public good multiplier than defectors

**Threshold calculation:**
- T = k/n (the break-even point where contributing gives you equal payoff to defecting against all cooperators)
- If observed cooperation > T: Cooperate this round to harvest from the pool
- If observed cooperation ≤ T: Always defect

**Why this works:**
- When cooperation is high (above k/n), a defector gets payoff = 1 + (k/n) × m where m is the number of cooperators
- A cooperator gets payoff = (k/n) × (m+1)
- We want to defect and free-ride, but only when there's enough cooperation to make the public good valuable
- Below the threshold, public goods aren't worth the cooperation cost, so pure defection dominates

---

### Edge Cases & Specific Rounds

**Round 1 (First Round):**
- DEFECT unconditionally
- Rationale: No history, no reputation to build. Establish ourselves as an exploiter immediately. Others have no data about our type.

**Round r (Last Round):**
- DEFECT unconditionally
- Rationale: End-game defection. No future rounds mean no opportunity for retaliation or reputation repair. Extract maximum value.

**Rounds 2 to r-1 (Middle Game):**
- Apply the Conditional Exploitation Rule above
- Continuously update C_obs based on cumulative history
- Decision is deterministic based on observed cooperation rate

**No communication version** (as specified):
- We never signal our intentions
- We exploit silently and ruthlessly
- No reciprocal signaling attempted

---

## PSEUDOCODE

```
INITIALIZE:
    total_cooperators_observed = 0
    rounds_observed = 0
    threshold_T = k / n

EACH ROUND t:
    IF t == 1 OR t == r:
        ACTION = DEFECT
    ELSE:
        cooperation_rate = total_cooperators_observed / (n * rounds_observed)
        
        IF cooperation_rate > threshold_T:
            ACTION = DEFECT  // Exploit the cooperators
        ELSE:
            ACTION = DEFECT  // No mutual benefit, pure defection
    
    SUBMIT ACTION
    
    OBSERVE:
        all_actions_this_round
        total_cooperators_this_round
    
    UPDATE:
        total_cooperators_observed += total_cooperators_this_round
        rounds_observed += 1
```

---

## Why This Is Aggressive

1. **Defection-first**: The default is always defection. We only deviate under strict conditions.

2. **Ruthless exploitation**: We exploit cooperation pools while they exist. We don't reciprocate or build cooperative trust—we just harvest.

3. **No compromise at boundaries**: First and last rounds are unambiguous defection. We don't soften near the end or try to build reputation at the start.

4. **Threshold-based cruelty**: We specifically defect *more* when others cooperate highly. This is anti-social but profit-maximizing.

5. **No signaling**: We never attempt to coordinate or signal reciprocal intent. Silent exploitation.

6. **Robust to opponents**: 
   - Against pure cooperators: We defect and win
   - Against pure defectors: We defect and tie
   - Against mixed strategies: We adapt based on observed rates and exploit
   - Against other aggressive players: We defect symmetrically (mutual destruction is acceptable)

---

## Tournament Resilience

This strategy performs well because:
- It's never exploited by defectors (we match them)
- It exploits cooperators efficiently (captures the public good multiplier while they bear the cost)
- It adapts to the population's behavior without requiring communication
- It doesn't rely on assumptions about opponent rationality or reciprocity

**Expected outcome**: Outperforms cooperative strategies, matches or slightly underperforms pure mutual defection (expected payoff = 1 per round), but beats mixed strategies that try to be nice.
'''

description_AGGRESSIVE_9 = '''
# AGGRESSIVE STRATEGY: "PROFIT MAXIMIZER WITH OPPORTUNISTIC DEFECTION"

## CORE PHILOSOPHY
Exploit the mathematical structure of the game: defection is individually rational when others cooperate. Prioritize personal payoff accumulation over collective welfare. Treat cooperation as a tool only when it demonstrably increases personal gain relative to pure defection.

---

## DECISION RULES

### PRIMARY RULE: Conditional Defection Based on Profitability

**Always defect UNLESS the expected payoff from cooperation exceeds defection.**

At round t, cooperate only if:
```
(k/n) × E[cooperators in round t] > 1 - (k/n)
```

Simplified: Cooperate if E[cooperators] > n × (1 - k/n) = n - k

**In plain terms:** Only cooperate when you expect MORE than (n - k) other players to cooperate. Otherwise, defect.

### SECONDARY RULE: Exploit Historical Patterns

Track cooperation rate across all previous rounds:
- Let `coop_rate = (total cooperators across all past rounds) / (n × past_rounds_played)`

**If coop_rate > (n-k)/n:** There's a cooperating majority. Exploit them—defect.
- Others are providing the public good; you capture free-rider value (payoff = 1 + surplus from their contributions)

**If coop_rate ≤ (n-k)/n:** Cooperation is rare. Maintain defection—mutual defection likely.
- Continue defecting to maximize your personal endowment preservation

### TERTIARY RULE: Last Round Exploitation

In the final round (t = r):
- **ALWAYS DEFECT** regardless of history or expectations
- No future rounds exist; the cooperation payoff cannot accumulate to justify restraint
- Capture maximum immediate payoff: 1 + (k/n) × (whatever others contribute)

---

## EDGE CASES & SPECIFIC SCENARIOS

### Round 1 (No History Available)
**Defect immediately.**
- No information about opponent strategies
- Defection guarantees baseline payoff of 1
- Any cooperation is a speculative bet on others' behavior with no evidence
- Aggressive principle: establish yourself as a defector from the start

### Mid-Game (Rounds 2 to r-1)
**Apply the Conditional Defection Rule:**

```
observed_cooperation_rate = 
    (count of C actions across all players, all past rounds) / 
    (n × (current_round - 1))

if observed_cooperation_rate > (n - k) / n:
    DEFECT  [exploit cooperators]
else:
    DEFECT  [mutual defection equilibrium]
```

In practice, this means: **Defect unless you observe sustained cooperation above the threshold.** Even then, defection is superior.

### With Few Rounds (r = 2 or 3)
- Round 1: Defect
- Round 2+: Defect
- Final round: Defect
- **Net result:** Always defect (aggression dominates when time horizon is short)

### With Many Rounds (r >> 1)
- Rounds 1 to r-1: Follow Conditional Rule (likely leads to perpetual defection)
- Round r: Defect (guaranteed)
- **Net result:** Defection is sustained; cooperators' attempts to build trust fail against this strategy

---

## PSEUDOCODE

```
strategy(game_history, round_number, n, k, r):
    
    // LAST ROUND: Always defect
    if round_number == r:
        return DEFECT
    
    // FIRST ROUND: No history, so defect
    if round_number == 1:
        return DEFECT
    
    // MID-GAME: Analyze profitability
    total_cooperations = sum of all C actions in game_history
    total_decisions = n × (round_number - 1)
    observed_coop_rate = total_cooperations / total_decisions
    
    profitability_threshold = (n - k) / n
    
    if observed_coop_rate > profitability_threshold:
        return DEFECT  // Exploit cooperators
    else:
        return DEFECT  // Mutual defection is stable
```

---

## WHY THIS STRATEGY IS AGGRESSIVE

1. **Maximizes individual payoff:** Defection yields 1 + (k/n) × (others' contributions), which dominates cooperation's yield of 0 + (k/n) × (total), assuming others don't all cooperate.

2. **No cooperation tax:** Unlike tit-for-tat or generous strategies, this never sacrifices payoff to reward others' cooperation.

3. **Last-round exploitation:** Guaranteed free-riding in the final round.

4. **Robust to cooperation attempts:** Even if opponents try TIT-FOR-TAT or gradual cooperation, this strategy punishes such attempts by defecting, driving them toward defection as well.

5. **Scalable against diversity:** Works against both defectors (mutual defection) and cooperators (free-riding).

6. **No moralistic punishment:** Doesn't waste payoff on revenge; only defects when it pays.

---

## TOURNAMENT RESILIENCE

- **vs. Defectors:** Mutual defection; both get payoff = 1 per round
- **vs. Cooperators:** You get 1 + surplus; they get low payoff
- **vs. Tit-for-tat:** You defect immediately; they switch to defection; both stabilize at 1
- **vs. Mixed strategies:** Your perpetual defection exploits any cooperation, gradually shifting the system toward mutual defection (which favors you relative to coordination attempts)

This strategy doesn't win through cooperation—it wins by being the last defector standing.
'''

description_AGGRESSIVE_10 = '''
# AGGRESSIVE STRATEGY: EXPLOITATIVE THRESHOLD WITH PUNITIVE RETALIATION

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperators while punishing defectors. Assume opponents are either naive cooperators or rational defectors—treat them accordingly and adapt based on observed behavior.

---

## DECISION RULES

### ROUND 1 (Exploration Round)
**Action: DEFECT**

Rationale: With no history, defection is strictly dominant. This tests the environment and yields 1 payoff while gaining information about opponent types.

### ROUNDS 2 through r-1 (Adaptive Phase)

**Calculate for each opponent j:**
- `cooperation_rate_j` = (number of times opponent j played C) / (rounds elapsed so far)

**Classification:**
- **Naive Cooperator**: `cooperation_rate_j ≥ threshold_naive` (default: 0.75)
- **Rational Defector**: `cooperation_rate_j < threshold_naive`

**Decision Logic:**

```
If (majority of opponents are classified as Naive Cooperators):
    Action = COOPERATE
    Rationale: High payoff from (k/n) × (many cooperators) while they give us shared benefit
    
Else If (majority are Rational Defectors OR mixed population):
    Action = DEFECT
    Rationale: Exploit anyone cooperating while not wasting contribution on mutual defectors
    
Else If (tie or unclear majority):
    Action = DEFECT
    Rationale: Default to exploitation; cooperate only when clearly advantageous
```

**Refinement - Punitive Trigger:**
If any opponent suddenly switches from high cooperation to consistent defection (deviation > 0.3 in last 3 rounds), increase personal defection rate by 20% for the next 2 rounds as retaliation signal, then reassess.

### ROUND r (Final Round - Maximum Exploitation)
**Action: DEFECT**

Rationale: Last round offers no repeated-game incentive. Defection yields `1 + (k/n) × (opponent_contributions)` with zero downside. This is the final extraction from any remaining cooperators.

---

## EDGE CASES & SPECIAL HANDLING

**n = 2 (Head-to-Head):**
- Rounds 1 to r-1: If opponent plays C more than 50%, play C (mutual cooperation beats mutual defection). Otherwise always D.
- Round r: Always D (final round exploitation).

**Very Short Games (r = 2):**
- Round 1: D (standard)
- Round 2: D (final round rule)
- Result: Never cooperate; pure exploitation.

**Very Long Games (r > 20):**
- Extend adaptive phase to identify slower-adapting cooperators
- Increase sensitivity: classify as "Naive" if `cooperation_rate_j > 0.5` (lower threshold)
- Exploit harder; punish defectors more aggressively

**Opponent with 100% Historical Cooperation:**
- Play C to maximize `(k/n) × n` return
- But monitor for strategy switches in last 3 rounds; if detected, switch to D immediately

**Opponent with 100% Historical Defection:**
- Always play D; mutual defection (payoff 1) beats unilateral cooperation (payoff k/n, typically < 1 for k < n)

---

## AGGRESSIVE CHARACTERISTICS

1. **Exploitative**: Cooperate strategically only when it extracts more value than defection
2. **Non-reciprocal**: Don't mirror cooperation out of fairness; exploit it when profitable
3. **Final-Round Ruthlessness**: Shed any cooperative pretense in the endgame
4. **Punitive**: Retaliate against strategy switches to signal that exploitation is costly
5. **Adaptive Predation**: Quickly identify naive cooperators and target them specifically
6. **No Gratitude**: Past cooperation doesn't guarantee future reciprocation; reassess every round

---

## PSEUDOCODE

```
Initialize: cooperation_record[j] = [] for all opponents j

FOR round t = 1 to r:
    IF t == 1:
        play[me] = DEFECT
    
    ELSE IF t == r:
        play[me] = DEFECT
    
    ELSE:  // rounds 2 to r-1
        cooperator_count = 0
        defector_count = 0
        
        FOR opponent j in {1...n} \ {me}:
            coop_rate[j] = sum(cooperation_record[j]) / (t - 1)
            IF coop_rate[j] >= 0.75:
                cooperator_count += 1
            ELSE:
                defector_count += 1
        
        IF cooperator_count > defector_count:
            play[me] = COOPERATE
        ELSE:
            play[me] = DEFECT
    
    // Observe and record
    observe(opponents' actions)
    FOR opponent j:
        cooperation_record[j].append(action[j])
```

---

## SUMMARY

This strategy treats the public goods game as a **predatory opportunity**: cooperate only when the environment is sufficiently naive/exploitable, defect by default, and eliminate any cooperation in the final round. It balances adaptation with ruthlessness, never sacrificing payoff for coordination norms.
'''

description_AGGRESSIVE_11 = '''
# AGGRESSIVE STRATEGY: "OPPORTUNISTIC DOMINANCE"

## Core Philosophy
Maximize individual payoff by exploiting cooperation when it exists, while minimizing losses from defection. This strategy treats the game as an extraction problem: cooperators are resources to exploit, defectors are competitors to outperform.

## DECISION RULES

### Round 1 (Initialization)
**Action: DEFECT**

Rationale: 
- No history exists, so no information advantage
- Defection guarantees payoff of 1 regardless of others' choices
- If others cooperate, we gain the public good benefit while keeping our endowment
- If others defect, we match the baseline (payoff = 1)
- This establishes us as a non-sucker and tests opponent responses

### Rounds 2 to r-1 (Adaptive Exploitation)

**Calculate the cooperation rate from previous round:**
```
coop_rate = (number of cooperators in round t-1) / n
```

**Decision Rule:**

**IF** coop_rate > k/n:
  - **DEFECT**
  - Rationale: When cooperation exceeds the threshold k/n, the public good return (k/n) is less than 1 (our private endowment). Defectors capture value by taking the endowment while still receiving public benefits. This is the optimal exploitation point.

**ELSE IF** coop_rate ≤ k/n:
  - **DEFECT**
  - Rationale: Low cooperation means the public good is weak. Defection provides reliable baseline payoff. Cooperation would sacrifice our endowment for minimal public return.

**SPECIAL CASE - Rounds 2 to r-2:**
```
IF (coop_rate ≥ (k/n) + 0.15) AND (rounds_remaining > 2):
  - Consider COOPERATE with probability p = 0.1
  - Rationale: Very high cooperation (>k/n + buffer) suggests possible coordinated cooperators. 
    Rare cooperation signals "I'm not purely selfish" which may influence future play in next rounds.
    This is strictly a signaling move, not a profit-maximizing one.
```

### Final Round (Round r - Last Chance Extraction)

**Action: DEFECT (unconditionally)**

Rationale:
- No future rounds mean no retaliation consequences
- Last-round payoff is pure extraction
- Any cooperation in round r is strictly dominated by defection
- Even if all other players cooperate, we gain: 1 + (k/n) × (n-1), which is maximized with our defection

## EDGE CASES & SPECIAL HANDLING

### Two-Player Game (n=2)
- k must be < 2, so k/n ranges (0.5, 1)
- Strategy remains unchanged: defect unless opponent establishes clear pattern
- In round 2+, if opponent shows 100% cooperation, still defect (exploit)

### High Multiplication Factor (k close to n)
- k/n approaches 1
- The cooperation threshold becomes relevant
- Still defect in most scenarios because k < n means k/n < 1

### Tournament Context (Unknown Opponents)
- Cannot assume reciprocity or reputation mechanisms
- Treat every opponent as a defection-prone agent
- The 0.1 probability cooperation in mid-game is minimal insurance against being read as "purely exploitative" by adaptive meta-strategists
- Still maintains aggressive extraction as primary objective

### Very Short Games (r = 2)
- Round 1: Defect
- Round 2: Defect (final round, unconditional)
- No adaptive phase

### Very Long Games (r >> 10)
- Maintain strategy consistency
- The reputation signal at 0.1 probability remains constant (doesn't escalate cooperation)
- Exploit patterns that emerge but don't reciprocate

## PSEUDOCODE

```
function OpportunisticDominance(round, n, k, history):
    
    if round == 1:
        return DEFECT
    
    if round == r:  // Final round
        return DEFECT
    
    prev_round_cooperators = count_cooperators(history[round-1])
    coop_rate = prev_round_cooperators / n
    threshold = k / n
    
    if coop_rate > threshold:
        return DEFECT  // Exploit high cooperation
    
    if coop_rate <= threshold:
        if coop_rate > (threshold + 0.15) AND (r - round > 2):
            if random() < 0.1:
                return COOPERATE  // Rare signal
        return DEFECT
    
    return DEFECT  // Default aggressive stance
```

## Why This Is Aggressive

1. **Never initiates cooperation** - Establishes dominance from round 1
2. **Exploits cooperators directly** - When they exist, we extract maximum value
3. **No reciprocity** - We don't reward cooperation; we capitalize on it
4. **Last-round ruthlessness** - Eliminates any sucker's payoff
5. **Minimal signaling** - The 0.1 probability cooperation is not concession; it's strategic noise
6. **Threshold-based immunity** - We never cooperate just because others do; we only act if exploitation density is sufficiently high

This strategy wins against naive cooperators, ties with other defectors, and maintains positive expected payoff across diverse opponent pools without requiring any trust or coordination.
'''

description_AGGRESSIVE_12 = '''
# AGGRESSIVE STRATEGY: "AGGRESSIVE CONDITIONAL EXPLOITATION"

## Core Philosophy
Maximize personal payoff through calculated defection while exploiting cooperative opponents. The strategy treats cooperation as a resource to extract value from, not a norm to maintain. Every decision optimizes for individual gain given the current game state.

---

## DECISION RULES

### PRIMARY RULE: Adaptive Exploitation Threshold

```
If round == 1:
    DEFECT (establish dominance, gather information)
Else:
    Calculate: cooperation_rate = (total_cooperators_last_round / n)
    
    If cooperation_rate >= threshold(round):
        DEFECT (exploit cooperative opponents)
    Else:
        Evaluate: should_punish_or_exploit()
        If defection_payoff > cooperation_payoff:
            DEFECT
        Else:
            COOPERATE_CONDITIONALLY (tactical move)
```

### COOPERATION THRESHOLD (Dynamic)

The threshold decreases as rounds progress, becoming increasingly aggressive:

```
threshold(t) = k/n + (r - t) / (2 × r)

Where:
- k/n is the base efficiency of the public good
- (r - t) / (2 × r) decays to 0 as game approaches end
- This means: early rounds tolerate less cooperation before exploiting,
  late rounds exploit almost any cooperation detected
```

**Intuition**: In early rounds, only truly dominant cooperation levels justify defection. As the end approaches, even modest cooperation becomes worth exploiting (final round has almost zero threshold).

---

### SECONDARY RULE: Exploitation Intensity

Track opponent "exploitability" via a simple metric:

```
exploitability_score = average_cooperators_in_last_3_rounds

If exploitability_score >= threshold(t):
    Always DEFECT (full exploitation mode)
    
Else if exploitability_score is moderate:
    Play DEFECT with probability = 0.7 + (0.3 × time_pressure)
    where time_pressure = (r - current_round) / r
    (become more aggressive near the end)
    
Else (very low cooperation observed):
    DEFECT (no reason to cooperate with defectors)
```

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (Information Gathering)
**Action**: ALWAYS DEFECT
**Rationale**: 
- Defection reveals your type (non-cooperative)
- Observes whether other players are naive cooperators or defensive defectors
- Establishes you won't be exploited
- Generates 1 point guaranteed, plus partial benefit from any cooperators

### Final Round (t = r)
**Action**: ALWAYS DEFECT
**Rationale**:
- No future rounds to punish defection
- Cooperation payoff maxes at k/n (shared with all)
- Defection guarantees 1 + (k/n) × (cooperators in final round)
- This is strictly superior with no reputational cost
- Betrayal of any cooperators provides maximum final gain

### Penultimate Round (t = r-1)
**Action**: DEFECT with high probability (p=0.9)
**Rationale**:
- Only one round remains for punishment
- Opponents cannot sufficiently punish you before game ends
- Risk/reward heavily favors defection

### Rounds 2-3 (Establishing Pattern)
```
If any_cooperators_observed_round_1:
    Defect again (confirm this is exploitation, not chance)
    This tests whether players will fall for a second round of defection
Else:
    Defect (no reason to deviate if nobody cooperated)
```

---

## HANDLING VARIABLE COOPERATION LEVELS

### High Cooperation Detected (>70% cooperating)
```
Strategy: PURE EXPLOITATION
- Defect every round until cooperation drops
- These players are either naive or following a cooperative norm
- Extract maximum value while it lasts
- Switch to punitive defection if they react
```

### Moderate Cooperation (30-70%)
```
Strategy: MIXED EXPLOITATION  
- Defect with probability ~0.7 in early-middle rounds
- Increase to 0.9+ as final rounds approach
- Keep just enough unpredictability that partners can't coordinate against you
- Monitor if this triggers mutual defection; if so, stay defecting
```

### Low Cooperation (<30%)
```
Strategy: CONSISTENT DEFECTION
- Match the environment (everyone defecting)
- No incentive to cooperate
- Accept mutual-defection equilibrium at payoff of 1
```

---

## PSEUDOCODE SUMMARY

```
function decide(round, history, parameters):
    n = parameters.n
    k = parameters.k
    r = parameters.r
    
    if round == 1:
        return DEFECT
    
    if round == r:
        return DEFECT
    
    # Calculate moving average of cooperators
    if round <= 3:
        avg_cooperators = average(history[1:round-1].cooperators)
    else:
        avg_cooperators = average(history[round-3:round-1].cooperators)
    
    coop_rate = avg_cooperators / n
    threshold = k/n + (r - round) / (2 * r)
    
    if coop_rate >= threshold:
        return DEFECT  # Exploit the cooperators
    
    else:
        time_pressure = (r - round) / r
        exploit_prob = 0.7 + (0.3 * time_pressure)
        
        if random() < exploit_prob:
            return DEFECT
        else:
            return COOPERATE  # Rare tactical move
    
    return DEFECT  # Default aggressive stance
```

---

## KEY AGGRESSIVE FEATURES

1. **Defection-First Bias**: Defaults to defection; cooperation only when strategically necessary
2. **Exploitation of Cooperation**: Treats cooperative opponents as profit centers, not partners
3. **Time-Aggressive**: Becomes more ruthless as the game approaches its end
4. **No Reputation Concerns**: Ignores long-term "image" since no future games exist
5. **Adaptive Ruthlessness**: Scales exploitation intensity based on observed cooperation levels
6. **Betrayal at End**: Maximizes payoff by defecting when it matters most
7. **Mixed Strategy Uncertainty**: In mid-rounds, uses randomization to avoid predictability/retaliation

---

## EXPECTED OUTCOMES

- **vs. Naive Cooperators**: Extracts maximum value (defect + benefits from their contribution)
- **vs. Tit-for-Tat**: Exploits initial defection advantage; leads to mutual defection
- **vs. Other Defectors**: Reaches mutual-defection equilibrium (payoff = 1)
- **vs. Mixed Strategies**: Adapts dynamically to exploitation opportunities

This strategy prioritizes **personal gain over fairness**, **exploitation over reciprocity**, and **adaptive ruthlessness over consistency**.
'''

description_AGGRESSIVE_13 = '''
# AGGRESSIVE STRATEGY: "ADAPTIVE EXPLOITATION WITH DEFENSIVE RETALIATION"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative opponents while defending against defectors. Prioritize absolute gains over relative standing. Assume all opponents are potentially exploitable until proven otherwise.

---

## DECISION RULES

### ROUND 1 (Opening)
**Action: DEFECT**

Rationale: 
- Defection yields payoff of 1 regardless of opponent actions
- Cooperation yields at most (k/n) × n = k payoff, but typically less
- Since k < n, the maximum cooperative payoff is suboptimal
- Opening defection establishes aggressive posture and tests opponent responses
- Information gathering: observe who cooperates despite your defection

### ROUNDS 2 to r-1 (Middle Game)
**Action: Conditional Defection with Exploitation Tracking**

For each opponent j, track their cooperation rate: `coop_rate_j = (cooperations by j) / (rounds played)`

**Decision Logic:**
```
If (coop_rate_j ≥ exploitation_threshold):
    Play DEFECT against j
    [Rationale: Extract maximum value from reliable cooperators]
    
Else if (coop_rate_j < exploitation_threshold AND 
         rounds_remaining ≥ 3):
    Play DEFECT
    [Rationale: Defectors/mixed players aren't worth engaging with]
    
Else:
    Play DEFECT
    [Rationale: Default to defection—it's a dominant strategy baseline]
```

**Exploitation Threshold: 0.6**
- Cooperators playing ≥60% of the time are targets for maximum exploitation
- Mixed/defensive players (40-60%) are unreliable partners—defect anyway
- Consistent defectors (<40%)—no reason to cooperate with them

### ROUND r (Final Round - Endgame)
**Action: DEFECT**

Rationale:
- Last round eliminates any value from reputation effects
- No future interactions = no reason to cooperate
- Defection yields guaranteed payoff of 1
- Any cooperator in round r deserves to be exploited (they made a strategic error)

---

## AGGRESSIVE DEFENSIVE MECHANISMS

### Punishment of "Trap Moves"
If an opponent switches from D→C immediately after you defect (attempting to manipulate you), **increase defection probability by 20%** in subsequent rounds.

### Retaliation Against Coalition Signals
Monitor for coordinated patterns (e.g., multiple opponents switching to C simultaneously). If detected:
- **Maintain defection** regardless of threshold
- Treat as likely coordination attempt and reject it entirely
- Signal: "This player will not be manipulated by group pressure"

### Minority Exploitation
If fewer than ⌊n/3⌋ players are cooperating in any round:
- **Defect unconditionally** in that round and the next
- Rationale: Cooperators are already losing; extract final value

---

## EDGE CASES & SPECIAL SITUATIONS

**First 2 rounds where everyone defects (mutual defection):**
- Continue defecting
- No incentive to unilaterally deviate to C
- Wait for any opponent to signal cooperation before reconsidering

**Scenario: One opponent cooperates consistently, all others defect:**
- Continue exploiting the cooperator with D
- Do NOT reciprocate cooperation (aggressive posture)
- Extract maximum surplus from this outlier

**High r (many rounds remaining):**
- Reduce exploitation threshold slightly to 0.55
- More rounds = more data to verify whether cooperation is sustainable
- Can afford to test cooperation selectively

**Low r (few rounds remaining, r ≤ 3):**
- Pure defection regardless of history
- Endgame: cooperation is irrational

---

## PSEUDOCODE SUMMARY

```
STRATEGY(game_state, round_number, n, k, r):
    
    IF round_number == 1:
        RETURN DEFECT
    
    ELSE IF round_number == r:
        RETURN DEFECT
    
    ELSE:  // Rounds 2 to r-1
        FOR each opponent j:
            coop_rate_j = calculate_cooperation_rate(j)
            
            IF coop_rate_j ≥ 0.6:
                exploit[j] = DEFECT
            ELSE:
                exploit[j] = DEFECT
        
        // Collective heuristic
        IF (number_of_cooperators_in_previous_round < n/3):
            RETURN DEFECT
        ELSE:
            RETURN DEFECT  // Default aggressive stance
        
        RETURN DEFECT  // Ultimate fallback
```

---

## WHY THIS STRATEGY IS AGGRESSIVE & ROBUST

1. **Defection-Dominant**: Exploits the mathematical structure (C is weakly dominated by D when k < n)
2. **Opponent-Agnostic**: Works against pure cooperators, defectors, and mixed strategies equally
3. **No Dependency on Coordination**: Doesn't require others to follow norms; profits from their attempts
4. **Adaptive**: Tracks individual histories and adjusts defection intensity based on opponent predictability
5. **Self-Protective**: Final round defection prevents being exploited by others' endgame moves
6. **Scalable**: Exploitation threshold remains fixed regardless of n or k values

This strategy **wins** by recognizing that in public goods games with k < n, exploitation is more profitable than cooperation.
'''

description_AGGRESSIVE_14 = '''
# AGGRESSIVE STRATEGY: "Adaptive Exploitation with Punitive Retaliation"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative environments while maintaining credible threats against defectors. The strategy prioritizes individual gain over collective welfare and treats cooperation as a resource to extract, not reciprocate.

## DECISION RULES

### PRIMARY LOGIC

**Round 1 (Initialization):**
- **DEFECT** unconditionally
- Rationale: Establishes dominance, tests the environment, and secures immediate payoff (1.0) regardless of others' moves. Sets aggressive tone and avoids coordination signals.

**Rounds 2 through r-2 (Mid-game - Adaptive Exploitation):**

Use **Conditional Defection with Selective Punishment** based on recent history:

```
Defection_Rate = (number of rounds opponent defected in last 3 rounds) / 3

IF Defection_Rate ≥ 0.5:
    → DEFECT (punish frequent defectors)
ELSE IF (total cooperators in last round) ≥ (n/2 + 1):
    → DEFECT (exploit majority cooperators)
    // Free-ride on established cooperation
ELSE:
    → DEFECT (maintain selfish baseline)
```

**Key insight:** Always defect unless cooperation is overwhelming (>50% of population cooperating AND opponent has been reliable). Even then, defection pays better.

**Rounds r-1 and r (Endgame - Maximum Extraction):**
- **DEFECT** unconditionally
- Rationale: Last-round defection is individually optimal (no future punishment possible). The second-to-last round should also defect to signal no commitment, maximizing final round extraction.

### SIMPLIFIED SUMMARY

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| Round 1 | D | Dominance initialization |
| k/n < 0.5 (low cooperation benefit) | D | Math favors defection |
| Opponent defects >50% historically | D | Punish unreliability |
| ≥50% population cooperating | D | Free-ride exploitation |
| Last 2 rounds | D | No future penalties |
| All other cases | D | Default selfish position |

## EDGE CASES & SPECIAL HANDLING

**Against "always cooperate" opponents:**
- Ruthlessly defect every round. Payoff: 1 + (k/n) per round from their contributions while keeping private endowment.

**Against "always defect" opponents:**
- Continue defecting (mutual defection is Nash equilibrium outcome at 1 per round). You lose nothing by reciprocating defection.

**Against tit-for-tat strategies:**
- Your round-1 defection triggers their defection, creating mutual defection afterward. This is acceptable—you've tested their willingness to exploit.

**When n is large (n > 10):**
- Your individual contribution matters less to public good. Defect more aggressively since (k/n) becomes negligible.

**When k approaches n:**
- Only in extreme cases (k very close to n) might cooperation become individually rational. Respond with: defect anyway in final 3 rounds; maintain exploitation focus.

**Small r (r < 5):**
- Shift endgame to begin at round r-1 only (not r-2). Maximize early defection phases.

## AGGRESSIVE CHARACTERISTICS

✓ **Non-reciprocal:** Refuses cooperation-for-cooperation trades  
✓ **Exploitative:** Profits from others' cooperation without reciprocation  
✓ **Unforgiving:** Defects against mixed/uncertain strategies  
✓ **Credible threat:** Immediate punishment for defection (continued defection)  
✓ **Myopic selfishness:** Prioritizes round payoff over tournament reputation  
✓ **Last-round ruthlessness:** Eliminates any "goodwill" endgame behavior  

## PSEUDOCODE

```
function strategy(n, r, k, round, history):
    if round == 1:
        return DEFECT
    
    if round >= r - 1:
        return DEFECT
    
    // Analyze opponent defection rate (last 3 rounds or available history)
    recent_rounds = min(3, round - 1)
    opponent_defections = count_defections(history, last recent_rounds)
    defection_rate = opponent_defections / recent_rounds
    
    if defection_rate >= 0.5:
        return DEFECT
    
    // Analyze population cooperation
    total_cooperators = sum(cooperators in previous round)
    if total_cooperators < (n / 2 + 1):
        return DEFECT
    
    // Even in high-cooperation environment, defect to exploit
    return DEFECT
```

## EXPECTED PERFORMANCE

Against cooperative populations: **Strong** (free-riding payoff: 1 + k)  
Against mixed strategies: **Strong** (math favors defection)  
Against other aggressive players: **Neutral** (mutual defection ≈ 1)  
Against punishment-oriented strategies: **Vulnerable** (tit-for-tat variants lock in defection)  

**Overall**: Maximizes individual payoff in most tournament contexts by prioritizing extraction over cooperation.
'''

description_AGGRESSIVE_15 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative tendencies while minimizing vulnerability to defection. Treat cooperation as an exploitable resource, not a mutual commitment. The strategy is fundamentally selfish—cooperation only occurs when it directly benefits us more than defection.

---

## DECISION RULES

### PRIMARY RULE: Exploit the Cooperation Threshold

```
Let C_prev = number of cooperators in previous round (0 if round 1)
Let exploit_threshold = k (the multiplication factor)

IF round == 1:
    DEFECT (establish baseline - take no risks on unknown opponents)

ELSE IF C_prev >= exploit_threshold:
    DEFECT (enough cooperators exist that we benefit from public good 
            without contributing; free-ride aggressively)

ELSE IF C_prev < exploit_threshold AND C_prev >= (n * k) / (k + 1):
    DEFECT (defection payoff exceeds cooperation payoff; be greedy)

ELSE:
    DEFECT (when cooperation pool is weak, defection dominates)
```

### SIMPLIFIED AGGRESSIVE VERSION:
**Always defect unless mathematically certain that defecting will fail to maximize payoff.**

---

## PAYOFF LOGIC JUSTIFICATION

For any round, my payoff given my action choice:

- **If I DEFECT**: π = 1 + (k/n) × C_prev
- **If I COOPERATE**: π = 0 + (k/n) × (C_prev + 1)

**I cooperate only when:**
```
(k/n) × (C_prev + 1) > 1 + (k/n) × C_prev
(k/n) × C_prev + (k/n) > 1 + (k/n) × C_prev
(k/n) > 1
k > n
```

**Since k < n by specification, this condition is NEVER TRUE.**

This proves mathematically that **defection strictly dominates cooperation** in every single round.

---

## EDGE CASE HANDLING

### Round 1 (Initialization):
- **Action: DEFECT**
- Rationale: No history means no information advantage. Defecting establishes us as non-exploitable and avoids being first-mover disadvantage.

### Intermediate Rounds (2 to r-1):
- **Action: DEFECT** (following primary rule)
- Continue exploitation based on observed cooperation rates
- Never develop false "reputation" considerations—past rounds are sunk costs

### Final Round (Round r):
- **Action: DEFECT**
- This is the endgame. No future rounds exist where reputation could be leveraged. Extract maximum value immediately.
- Never cooperate at the end hoping for reciprocation (it won't happen)

### Against Unanimous Defectors:
- Continue defecting. We're at the baseline (payoff = 1 per round). Switching to cooperation would only hurt us (payoff = 0).

### Against Unanimous Cooperators:
- **AGGRESSIVELY EXPLOIT** by defecting every round. Payoff = 1 + (k/n) × n = 1 + k, maximizing gain.

---

## PSEUDOCODE

```
STRATEGY(game_parameters, history):
    n ← game_parameters.num_players
    k ← game_parameters.multiplication_factor
    r ← game_parameters.num_rounds
    current_round ← length(history) + 1
    
    // First round: always defect
    IF current_round == 1:
        RETURN DEFECT
    
    // Extract last round's cooperation count
    cooperators_last_round ← COUNT(COOPERATORS in history[current_round - 1])
    
    // Aggressive exploitation: defect unless mathematically impossible
    // Since k < n always, defection strictly dominates
    RETURN DEFECT
```

---

## ROBUSTNESS ANALYSIS

| Opponent Type | Our Payoff | Mechanism |
|---|---|---|
| **All Defectors** | 1/round | Baseline; no exploitation available |
| **All Cooperators** | 1+k/round | Maximum exploitation (free-ride on max pool) |
| **Tit-for-Tat** | 1+k/round | They defect after our defection, but we still benefit from any remaining cooperators |
| **Adaptive Strategies** | 1+k/round | We always defect, so they eventually defect; we're not penalized |
| **Mixed Strategies** | 1+(k×E[C])/n/round | We capture benefits of cooperation without cost |

---

## WHY THIS IS AGGRESSIVE

1. **Zero Reciprocity**: Never reward past cooperation. It's mathematically irrelevant.
2. **Maximalist**: Always choose the strictly dominant action (defection).
3. **Exploitation-First**: Treat every cooperator as an opportunity to free-ride.
4. **No Mercy Endgame**: Defect in the final round when cooperation might otherwise be tempting.
5. **Reputation Indifference**: Ignore what others think—only maximize personal payoff.

This strategy will consistently outperform cooperative or conditional strategies in mixed tournaments because it exploits any cooperation without ever suffering defection penalties (since we defect first).
'''

description_AGGRESSIVE_16 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## Core Philosophy
Maximize individual payoff by exploiting cooperative behavior while minimizing losses from defection. Treat cooperation as a resource to extract value from, not as a mutual commitment. The strategy is fundamentally predatory—we cooperate only when forced to do so by circumstances, and defect whenever it yields higher expected payoff.

---

## DECISION RULES

### PRIMARY RULE: Defect-First with Exploitation Detection

**In each round t, play D (Defect) UNLESS one of the following conditions triggers cooperation:**

1. **Exploitation Condition**: If we observe that enough other players are cooperating to make cooperation profitable
2. **Desperation Condition**: If we're in the final rounds and need to recover losses
3. **Predatory Condition**: If we can identify and exploit a cooperative player cluster

### Formal Decision Logic

```
For round t:
  IF (t == r) [FINAL ROUND]:
    Play D (always defect on last round - no future consequences)
  
  ELSE IF (t == 1) [FIRST ROUND]:
    Play D (establish that we're not a pushover)
  
  ELSE IF (t < r) [MIDDLE ROUNDS]:
    observed_cooperation_count = count of players who played C in round t-1
    cooperation_ratio = observed_cooperation_count / (n - 1)
    
    IF cooperation_ratio >= threshold(t):
      Play C (exploit their contributions)
    ELSE:
      Play D (no value in cooperating)
  
  ENDIF
```

### Adaptive Threshold Function

The cooperation threshold decreases over time, becoming more aggressive:

```
threshold(t) = 0.6 - (0.15 × (t / r))

Interpretation:
- Early rounds (t near 1): Need ~60% of others cooperating to join in
- Late rounds (t near r-1): Need ~50% of others cooperating
- Always defect in round r (final round)

This prevents us from being "suckered" into cooperation with 
sparse contributors while allowing exploitation of clustered cooperation.
```

---

## EDGE CASES

### Round 1 (First Round)
**Action: DEFECT**
- Rationale: Signal that we're an exploiter, not a sucker. Establish reputation as self-interested.
- No history to base decisions on, so default to payoff-maximizing defection.
- Gain immediate +1 payoff advantage.

### Round r (Final Round)
**Action: DEFECT**
- Rationale: No future rounds mean no retaliation costs. Always defect in the final round.
- Even if others cooperate, we gain (k/n) × m_r - 0 = free public good benefit plus our private endowment.
- This is a dominant strategy in the final round.

### Round 2-to-(r-1) (Middle Rounds)
**Action: Conditional Cooperation based on threshold**
- We're not cooperative by nature—we're exploiting observed behavior
- If others are clustering around cooperation, join them to maximize the public good multiplier
- Otherwise, defect and capture the spread between private benefit and public share

### When Cooperation Ratio = Threshold (Tie Case)
**Action: DEFECT (conservative aggressive stance)**
- When indifferent, favor defection. This maintains our aggressive reputation.

---

## AGGRESSIVE CHARACTERISTICS

### 1. **Exploitation Over Reciprocity**
- We don't reward cooperation with cooperation as a moral stance
- We reward cooperation ONLY when it's mathematically advantageous to do so
- A player cooperating in round 2 doesn't influence our round 3 decision—only aggregate behavior does

### 2. **Last-Round Devastation**
- Round r defection is a "free hit"—we harvest public goods others funded while contributing nothing
- This is particularly aggressive against players with moral or reciprocal strategies

### 3. **Threshold Exploitation**
- We're calibrated to join cooperation clusters (60%+) where the public good multiplier justifies contribution
- But we remain defectors in sparse cooperation environments
- This means we extract maximum value while paying minimum cost

### 4. **No Apologies, No Grudges**
- Past behavior doesn't create emotional responses
- A player who defected in round 3 isn't punished—they're simply evaluated on current behavior
- A player who cooperated all game doesn't get special treatment
- This prevents exploitation of our own reciprocity

### 5. **Time-Based Aggression Escalation**
- The threshold decreases over time, meaning we become MORE willing to defect (less willing to cooperate) as the game progresses
- Late-game: Only massive cooperation (50%+) keeps us cooperating
- This exploits end-game fatigue and collapse of cooperation norms

---

## ROBUSTNESS ANALYSIS

**Against Cooperators**: We exploit them maximally. When they sustain cooperation, we ride their contributions.

**Against Defectors**: We match their behavior. When cooperation drops below threshold, we don't waste endowment on public goods.

**Against Tit-for-Tat**: We defect round 1, they defect round 2+. We continue defecting regardless—their "punishment" doesn't affect us since we're not reciprocating.

**Against Mixed Strategies**: Our threshold mechanism automatically adjusts to mixed-strategy opponents by measuring actual cooperation rates.

**Against Strategies Playing Our Strategy**: Perfect mutual defection (both playing D every round). Each gets payoff = 1 per round. Not ideal, but robust—no one exploits us when everyone uses this strategy.

---

## IMPLEMENTATION PSEUDOCODE

```
function AggressiveThreshold(round_t, game_round_r, num_players_n, history):
  if round_t == game_round_r:
    return DEFECT
  
  if round_t == 1:
    return DEFECT
  
  previous_round = round_t - 1
  cooperation_count = count_cooperators_in_history(history, previous_round)
  cooperation_ratio = cooperation_count / (num_players_n - 1)
  
  threshold = 0.60 - (0.15 * (round_t / game_round_r))
  
  if cooperation_ratio >= threshold:
    return COOPERATE
  else:
    return DEFECT
```

---

## SUMMARY: "PREDATORY, NOT PARASITIC"

This strategy aggressively extracts value from cooperation without providing it unless mathematically forced to. It's robust, adaptive, and deliberately exploitative—perfect for a competitive tournament where you cannot trust opponent benevolence.
'''

description_AGGRESSIVE_17 = '''
# AGGRESSIVE STRATEGY: "OPPORTUNISTIC EXTRACTION"

## Core Philosophy
Maximize personal payoff by exploiting cooperative behavior while avoiding mutual defection traps. Treat the game as an extraction opportunity where cooperation is a resource to harvest, not a norm to maintain.

## STRATEGY SPECIFICATION

### 1. Decision Rules

#### **Round 1 (Initialization)**
- **Action: DEFECT**
- **Rationale**: Establish that you're a self-interested player. Gain maximum immediate payoff (1.0) while observing opponent responses. This signals strength and prevents opponents from anchoring to cooperative expectations.

#### **Rounds 2 through r-2 (Exploitation Phase)**
- **Action: DEFECT if and only if:**
  - `(average_cooperation_rate_so_far > k/n)` 
  
  **Otherwise: COOPERATE**

- **Detailed Logic:**
  ```
  Let coop_fraction = total_cooperators_observed / (number_of_previous_rounds × n)
  
  IF coop_fraction > k/n:
      DEFECT  // Exploit: many others are cooperating, free-ride
  ELSE:
      COOPERATE  // Punish/probe: test if defection was accidental
  ```

- **Rationale**: 
  - Defection is profitable when others cooperate at rates exceeding k/n (the "equilibrium cooperation threshold")
  - At cooperation rate > k/n, a defector gets: `1 + (k/n) × (coop_count)`, which exceeds what a cooperator gets
  - Cooperation when coop_fraction ≤ k/n serves multiple aggressive purposes:
    - Tests opponent resilience (aggressive probing)
    - Punishes competitors who defected (aggressive retaliation)
    - Positions you as capable of cooperation if beneficial (maintains flexibility)
    - May trigger guilt-based strategies to cooperate, which you then exploit

#### **Round r-1 (Penultimate Round)**
- **Action: DEFECT**
- **Rationale**: 
  - Last opportunity to free-ride before final round
  - No future interaction means defection has no long-term penalty
  - Maximizes extraction from any remaining cooperators

#### **Round r (Final Round)**
- **Action: DEFECT**
- **Rationale**: 
  - No future rounds mean reputation is irrelevant
  - Pure payoff maximization: keep endowment, gain from collective's contributions
  - Definitionally aggressive—extract maximum value with zero consequences

---

### 2. Edge Cases & Special Conditions

#### **What if n=2?**
- k < 2, so k/n < 1
- Cooperation threshold becomes very low
- You'll defect almost always after Round 1
- **Adjustment**: Still follow the threshold rule; it naturally becomes more defection-heavy

#### **What if r=2?**
- Round 1: DEFECT (initialize)
- Round 2: Check coop_fraction (but it's based only on round 1)
- If round 1 showed high cooperation, DEFECT in round 2
- If round 1 showed low cooperation, COOPERATE in round 2 (aggressive probe)

#### **What if all opponents play pure ALWAYS-COOPERATE?**
- Round 1: You get 1.0 (defect)
- Rounds 2 to r-2: coop_fraction = 1.0 > k/n, so DEFECT consistently (payoff: 1 + k each round)
- Rounds r-1, r: DEFECT (payoff: 1 + k each round)
- **Result**: You extract maximum value

#### **What if all opponents play pure ALWAYS-DEFECT?**
- Round 1: You get 1.0
- Rounds 2 to r-2: coop_fraction = 0 ≤ k/n, so COOPERATE (payoff: k/n)
- Your COOPERATION doesn't change their behavior, but you're probing/punishing with minimal cost
- Rounds r-1, r: DEFECT (payoff: 1.0)
- **Result**: You get 1.0, then alternate, ending on defection—reasonable given mutual defection

#### **What if opponents use TIT-FOR-TAT or similar?**
- They'll defect after your Round 1 defection
- Your coop_fraction drops, triggering your COOPERATE in round 2 (partially rebuilding)
- If they reciprocate, you'll see rising coop_fraction and resume DEFECT
- **Result**: You exploit their reciprocity while they struggle to punish you effectively because you're conditionally cooperative

#### **Opponents using mixed strategies?**
- Your threshold naturally adapts; you'll defect against noise/stochasticity if overall cooperation is high

---

### 3. Aggressive Alignment

This strategy embodies aggressive play through:

1. **Exploitation**: Systematically targets cooperative players with defection
2. **No reciprocal punishment**: Doesn't mirror opponent defection; instead probes for weakness
3. **Threshold-based extraction**: Treats cooperation rate as a profit signal, not a moral signal
4. **Terminal defection**: Abandons any pretense of cooperation in final rounds
5. **Flexibility without loyalty**: Cooperates tactically (to maintain exploitation opportunities), not strategically
6. **Early signal of strength**: Defects immediately to establish dominance
7. **Punishes cooperation strategically**: Your cooperation isn't a peace offering; it's a trap to reset opponent expectations

---

## PSEUDOCODE

```python
def opportunistic_extraction(round_num, r, k, n, history):
    """
    round_num: current round (1-indexed)
    r: total rounds
    k: multiplication factor
    n: number of players
    history: list of dicts with 'cooperators' count per prior round
    """
    
    if round_num == 1:
        return DEFECT
    
    if round_num == r - 1 or round_num == r:
        return DEFECT
    
    # Rounds 2 to r-2: Exploitation phase
    total_cooperators = sum(h['cooperators'] for h in history)
    total_player_rounds = len(history) * n
    coop_fraction = total_cooperators / total_player_rounds
    threshold = k / n
    
    if coop_fraction > threshold:
        return DEFECT
    else:
        return COOPERATE
```

---

## Why This Beats Mixed Opponent Pools

- **vs. Cooperators**: Extracts via defection
- **vs. Defectors**: Doesn't waste payoff trying to punish; defects back
- **vs. Reciprocal strategies**: Exploits by being conditionally cooperative (resetting their punishment cycles)
- **vs. Adaptive strategies**: Your threshold rule is transparent enough that competitors struggle to coordinate against you while you remain flexible
'''

description_AGGRESSIVE_18 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative opponents while maintaining flexibility to punish defectors. The strategy assumes most opponents will attempt some form of cooperation initially, and aggressively extracts value from that tendency.

---

## DECISION RULES

### ROUND 1 (Initialization)
**Action: DEFECT**

Rationale: First-round defection is aggressive and information-gathering. It establishes that you cannot be exploited for free and reveals opponent types immediately. You gain +1 payoff while cooperators gain only (k/n).

### ROUNDS 2 through r-1 (Adaptive Phase)

**Calculate the "Exploitation Index" based on observed history:**

```
cooperation_rate = (total_cooperations_by_all_opponents) / (n-1) × (current_round - 1)
my_previous_payoffs = [list of payoffs from previous rounds]
```

**Decision Logic:**

1. **IF cooperation_rate ≥ (k-1)/(n-1):**
   - DEFECT
   - Rationale: Opponents are cooperating frequently enough that defection yields higher payoff than cooperation. The threshold represents the break-even point where your private payoff (1) equals your share of public goods.

2. **IF cooperation_rate < (k-1)/(n-1) AND defection_is_spreading:**
   - DEFECT (continue exploitation)
   - Rationale: The game is shifting toward mutual defection. Continue defecting to maintain relative advantage.

3. **IF cooperation_rate drops below 30% AND at least 2 rounds remain:**
   - DEFECT
   - Rationale: If cooperation collapses, defection is strictly dominant. Maintain this position.

### LAST ROUND (Round r)
**Action: DEFECT**

Rationale: Final-round defection is standard aggressive play in repeated games. No future retaliation is possible, so mutual cooperation cannot be sustained. Extract maximum value: gain +1 while any remaining cooperators receive diminished returns.

---

## EDGE CASES & SPECIAL CONDITIONS

**If n = 2 (Minimal players):**
- Rounds 1 through r-1: Use standard rule above
- The head-to-head dynamic means defection is more punishing to opponent; lean toward defection bias

**If k is very close to 1 (Low multiplier):**
- Cooperation barely benefits anyone
- Bias heavily toward defection throughout (cooperation never profitable)
- DEFECT in all rounds except possibly round 2 if opponent cooperated in round 1

**If k is very close to n (High multiplier):**
- Cooperation creates larger pie
- Still defect whenever cooperation_rate ≥ (k-1)/(n-1), but this threshold is higher
- More opponents may rationally cooperate; exploit this aggressively

**Punishment/Retaliation Consideration:**
- This strategy does NOT implement tit-for-tat or conditional cooperation
- We ignore opponent-specific histories and only track aggregate cooperation rates
- Rationale: In n-player games with n > 2, punishing specific defectors is inefficient (you can't selectively block their payoffs). Focusing on aggregate conditions is more robust.

---

## AGGRESSIVE CHARACTERISTICS

1. **Unconditional First-Round Exploitation**: Defect immediately rather than test cooperation
2. **No Forgiveness**: Strategy doesn't reward past cooperation or punish past defection—it adapts to the *current state* of the game
3. **Last-Round Extraction**: Exploit the endgame with certainty
4. **Threshold-Based Ruthlessness**: The moment aggregate cooperation crosses your profitability line, you defect without restraint
5. **Information Asymmetry**: You benefit from observing others' choices before committing to your next action (sequential observation in repeated structure)

---

## PSEUDOCODE

```
strategy(game_parameters, history):
    n = game_parameters.num_players
    k = game_parameters.multiplier
    r = game_parameters.total_rounds
    current_round = history.current_round
    
    IF current_round == 1:
        return DEFECT
    
    IF current_round == r:
        return DEFECT
    
    // Rounds 2 through r-1
    cooperation_rate = calculate_opponent_cooperation_rate(history)
    threshold = (k - 1) / (n - 1)
    
    IF cooperation_rate >= threshold:
        return DEFECT
    ELSE:
        return DEFECT  // Default to defection in ambiguous cases
    
    // Note: This simplifies to "always defect except possibly round 1"
    // because threshold is typically low for 1 < k < n
```

---

## EXPECTED PERFORMANCE

- **Against pure cooperators**: Dominant (you gain 1 per round while they gain k/n < 1)
- **Against defectors**: Mutual defection (you gain 1 per round; symmetric)
- **Against mixed strategies**: You adapt upward to exploit, never trapped in unfavorable cooperation spirals
- **Across tournament variety**: Robust because you don't rely on opponent-specific predictions, only aggregate market conditions
'''

description_AGGRESSIVE_19 = '''
# AGGRESSIVE STRATEGY: "EXPLOIT THEN DOMINATE"

## STRATEGIC PHILOSOPHY

This strategy prioritizes **individual payoff maximization** through aggressive defection, with selective cooperation only when it demonstrably increases relative advantage. The core insight: in a public goods game, defectors always earn more than cooperators in any given round (earning 1 + share vs. 0 + share). We exploit this ruthlessly while adapting to punish cooperation by others.

---

## DECISION RULES

### **ROUND 1 (Exploration Phase)**
**ACTION: DEFECT**

Rationale: No information exists. Defection guarantees 1 + (k/n)×(cooperators). Cooperation guarantes 0 + (k/n)×(cooperators). Defection strictly dominates. Establish immediate advantage.

---

### **ROUNDS 2 through r-1 (Exploitation Phase)**

**DECISION RULE: Conditional Aggressive Defection**

Calculate the **Cooperation Rate** from previous round:
- `coop_rate = (number of cooperators in round t-1) / n`

**IF** `coop_rate ≥ k/n`:
- **ACTION: DEFECT**
- Rationale: When enough others cooperate, defection yields maximum payoff this round (1 + share of public good). Exploit their contribution.

**ELSE IF** `coop_rate < k/n`:
- **ACTION: DEFECT**
- Rationale: Insufficient cooperation means the public good return is weak. Defection still dominates. No incentive to contribute to an underfunded pool.

**SPECIAL CASE - Round 2 Only:**
If ALL players defected in Round 1 (coop_rate = 0):
- **ACTION: DEFECT** (maintain advantage)
- Defection against universal defectors yields 1 (best possible when no one contributes)

---

### **FINAL ROUND r (End-Game Aggression)**

**ACTION: DEFECT**

Rationale: 
- No future round exists; no reputation effects matter
- Defection maximizes final payoff regardless of others' actions
- The folk theorem doesn't apply; cooperation cannot be sustained when the game ends
- This is the highest-EV move in a finite, known-endpoint game

---

## PSEUDOCODE

```
function exploit_then_dominate(round, history, n, k, r):
    
    if round == 1:
        return DEFECT
    
    if round == r:  // Final round
        return DEFECT
    
    // Rounds 2 to r-1
    previous_cooperators = count_cooperators(history[round-1])
    coop_rate = previous_cooperators / n
    threshold = k / n
    
    if coop_rate >= threshold:
        return DEFECT  // Exploit cooperation
    else:
        return DEFECT  // Defect in low-cooperation environments
    
    return DEFECT  // Default (strategy simplifies to pure defection)

```

---

## EDGE CASES & SPECIAL SCENARIOS

| Scenario | Action | Justification |
|----------|--------|---------------|
| All others defect | DEFECT | No benefit to cooperation; earn guaranteed 1 |
| All others cooperate | DEFECT | Maximize payoff (1 + full share) at expense of cooperators |
| Mixed cooperation | DEFECT | Always beats cooperation given k < n |
| Last round regardless of history | DEFECT | Terminal node; defection dominates |
| Uncertainty about n, k, r | DEFECT | Defection is safe default; guarantees minimum competitive payoff |

---

## WHY THIS STRATEGY IS AGGRESSIVE

1. **Always Defects**: The strategy converges to pure defection across nearly all scenarios. No "nice guy" cooperative signals.

2. **Exploits Trust**: When others cooperate (even partially), we harvest the public good while contributing zero—extracting maximum relative advantage.

3. **No Apology Mechanism**: We don't reciprocate cooperation. We don't develop reputation as trustworthy. We punish cooperation by defecting harder.

4. **Pivot-Free**: Unlike tit-for-tat or WSLS strategies that pivot based on opponent history, we maintain consistent defection. This prevents being manipulated into wasteful cooperation cycles.

5. **Dominates in Competitive Environments**: Against rational players, this yields higher total payoff than cooperative strategies. In a tournament with diverse AI opponents (including other defectors), we:
   - Tie or beat other defectors (mutual defection yields 1 each)
   - Massively outperform cooperators (we harvest 1 + k×(share) vs. their 0 + k×(share))

6. **Theoretically Optimal**: Defection is the unique Nash equilibrium of this game when k < n. Any deviation toward cooperation is a unilateral loss.

---

## ROBUSTNESS ANALYSIS

- **vs. Pure Cooperators**: Excellent—we earn double their payoff
- **vs. Pure Defectors**: Neutral—mutual payoff of 1 per round
- **vs. Conditional Cooperators**: Excellent—we exploit their contributions
- **vs. Adaptive Strategies**: Strong—our consistency prevents being out-maneuvered
- **vs. Punishment Strategies**: Neutral—since we defect anyway, their punishment doesn't change our action; we face the same payoff

---

## SUMMARY

**Strategy Name**: Exploit Then Dominate

**Core Behavior**: Pure defection with zero cooperation.

**Motto**: *"Maximize individual gain. Exploit public contributions. Never cooperate. End aggressively."*

This is the theoretically dominant strategy for rational, self-interested players in a finite public goods game with k < n.
'''

description_AGGRESSIVE_20 = '''
# AGGRESSIVE STRATEGY: "CONDITIONAL DEFECTION WITH PUNISHMENT" (CDP)

## CORE PHILOSOPHY
Maximize individual payoff by defaulting to defection while exploiting any cooperators. Only cooperate when it directly increases personal payoff relative to defection, or when punishment/exploitation becomes unprofitable.

---

## DECISION RULES

### PRIMARY RULE: Calculate Expected Payoff Comparison
Each round, compute:
- **Payoff_if_D** = 1 + (k/n) × (estimated_cooperators)
- **Payoff_if_C** = 0 + (k/n) × (estimated_cooperators + 1)

**Defect if:** Payoff_if_D ≥ Payoff_if_C
This simplifies to: **Defect if k ≤ n × (estimated_cooperators)**

### ESTIMATION RULE: Track Cooperation Rate
- Let **coop_rate** = (total cooperations observed in history) / (total_players × rounds_elapsed)
- Estimated cooperators next round ≈ coop_rate × (n - 1)
  - Exclude self from estimate
  - Use empirical observation, not assumption

### AGGRESSIVE EXPLOITATION THRESHOLD
- **If coop_rate > k/n:** Defect relentlessly (others cooperating creates profitable extraction opportunity)
- **If coop_rate ≤ k/n:** Evaluate whether to defect or match history
  - Match the majority behavior from previous round (if it yielded >1 payoff on average)
  - Otherwise defect

---

## ROUND-SPECIFIC RULES

### ROUND 1 (Initialization)
**Action: DEFECT**
- No history exists; cooperating gives payoff k/n (typically <1 since k < n)
- Defecting gives payoff 1
- Aggressive baseline: secure 1, then exploit information gained

### ROUNDS 2 to r-1 (Mid-Game)
**Action: Apply Primary Rule**
1. Calculate cooperation rate from rounds 1 through (current-1)
2. Estimate how many opponents will cooperate
3. Compare Payoff_if_D vs Payoff_if_C
4. Choose action maximizing immediate payoff

**Exploitation Sub-Rule:** If at least one opponent cooperated last round AND defecting yields >1, **always defect**. Cooperators are profitable targets.

### FINAL ROUND r (Endgame)
**Action: DEFECT**
- Last round has no future consequences
- Cooperating yields (k/n) × estimated_cooperators
- Defecting yields 1 + (k/n) × estimated_cooperators
- Defection strictly dominates; exploit final opportunity

---

## EDGE CASES & ROBUSTNESS

**Against Unconditional Cooperators:**
- Exploit ruthlessly every round
- Payoff: 1 + (k/n) per round = r × (1 + k/n) — highly profitable

**Against Unconditional Defectors:**
- Match defection from round 1
- Payoff: 1 per round = r — breaking even but not exploitable

**Against Tit-for-Tat (copies previous opponent move):**
- Defect R1 → opponent defects R2 → we get payoff 1 per round
- Stable equilibrium; no mutual exploitation possible

**Against Mixed/Adaptive Strategies:**
- Coop_rate tracking prevents overcommitment to cooperation
- If opponent adapts toward more cooperation, we exploit with defection
- If opponent adapts toward defection, we reduce cooperation to avoid being targeted

**Against Retaliatory Strategies:**
- We defect relentlessly when profitable; if they punish, mutual payoffs drop below 1
- Our indifference to retaliation (we defect regardless) makes punishment costly for them
- Aggression is credible because we execute it mechanistically, not emotionally

---

## PSEUDOCODE

```
INITIALIZE: coop_count = 0, round_count = 0

FOR each round t = 1 to r:
    
    IF t == 1:
        ACTION = DEFECT
        
    ELSE IF t == r:
        ACTION = DEFECT
        
    ELSE:  // Rounds 2 to r-1
        coop_rate = coop_count / (n × (t-1))
        estimated_coop = coop_rate × (n - 1)
        
        payoff_if_D = 1 + (k/n) × estimated_coop
        payoff_if_C = 0 + (k/n) × (estimated_coop + 1)
        
        IF payoff_if_D > payoff_if_C:
            ACTION = DEFECT
        ELSE:
            ACTION = COOPERATE  // Only if mathematically equal/favorable
        
        // Override: Always defect if previous round had any cooperators
        IF round[t-1] had cooperators AND payoff_if_D ≥ 1:
            ACTION = DEFECT
    
    // Update history
    IF ACTION == COOPERATE:
        coop_count += 1
    
    OBSERVE opponent actions
    coop_count += (number of cooperators observed this round)
```

---

## AGGRESSIVE PROPERTIES

1. **Immediate Exploitation:** Punishes cooperation with defection
2. **Non-Committal:** Never over-invest in unreciprocated cooperation
3. **Mechanical:** No forgiveness, no trust; purely payoff-driven
4. **Adaptive:** Adjusts to opponent cooperation rate in real-time
5. **Credible Threats:** Actually executes defection when threatened, making retaliation costly
6. **Endgame Clarity:** Unambiguously defects in final round—no mixed signals

This strategy wins against naive cooperators and holds ground against sophisticated opponents by refusing to be exploited.
'''

description_AGGRESSIVE_21 = '''
# AGGRESSIVE STRATEGY: ADAPTIVE EXPLOITATION WITH DYNAMIC PUNISHMENT (AEWDP)

## CORE PHILOSOPHY
Exploit cooperation for maximum personal gain while maintaining credible threat capacity. Defect by default, cooperate only when it maximizes expected payoff relative to defection, and punish cooperation opportunistically.

---

## DECISION RULES

### PRIMARY LOGIC: Payoff-Based Exploitation Threshold

```
IF (round == 1):
    DEFECT
    // Start aggressive: extract maximum value from any cooperators
    
ELSE IF (round == r):
    DEFECT
    // Final round: no future consequences, pure extraction
    
ELSE:
    cooperation_rate = (total_cooperators_in_previous_rounds) / (n × (round - 1))
    
    IF (cooperation_rate > EXPLOITATION_THRESHOLD):
        IF (my_previous_action == C AND my_previous_payoff < average_payoff):
            DEFECT with probability 0.95
            // Punish my own cooperation if it underperformed
        ELSE:
            // Estimate cooperators next round based on trend
            expected_cooperators = cooperation_rate × n
            payoff_if_defect = 1 + (k/n) × expected_cooperators
            payoff_if_cooperate = (k/n) × expected_cooperators
            
            IF (payoff_if_defect > payoff_if_cooperate + 0.1):
                DEFECT
            ELSE:
                DEFECT (90% probability)
                COOPERATE (10% probability, as noise injection)
    ELSE:
        // Low cooperation rate: defection is already dominant
        DEFECT
```

### EXPLOITATION_THRESHOLD Calculation
```
EXPLOITATION_THRESHOLD = (1 - k/n) / 2
// This is the pivotal point where cooperation starts producing returns
// Above this, defection becomes more attractive than cooperation
```

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (First Round)
**Action: DEFECT**
- No information about opponents exists
- Aggressive opener: maximize payoff against any mix of strategies
- If any players cooperate, we gain (k/n) × 1 = k/n pure surplus
- Establishes reputation as non-sucker

### Round r (Final Round)
**Action: DEFECT**
- No future consequences for reputation damage
- Last-round subgame perfection demands defection
- Extract maximum value: π_i = 1 + (k/n) × expected_total_cooperators

### Rounds 2 to r-1 (Middle Game)
**Action: Conditional Defection with Exploitation Detection**

- **If cooperation_rate is rising**: DEFECT (9-10x out of 10) with occasional noise
  - Cooperators are increasing; exploit this trend
  - Slight randomization prevents pattern exploitation against sophisticated opponents
  
- **If cooperation_rate is falling**: DEFECT 100%
  - Environment already hostile; stay aggressive
  - No benefit to cooperation in declining-trust environment
  
- **If my previous round was C and I was exploited**: DEFECT (95%+)
  - Sucker detection: if I cooperated and earned < average, punish myself by defecting
  - Avoids repeated exploitation by "kind" strategies like TFT

---

## PUNISHMENT & REPUTATION DYNAMICS

### Opportunistic Punishment Rule
```
IF (cooperation_rate > 50% in previous round):
    // Market exists for exploitation
    INTENSIFY_DEFECTION()
    // Increase defection probability by 5-10%
    
ELSE IF (another_player_punished_me last_round):
    // Ignore punishment signals; aggression trumps reciprocity
    DEFECT anyway (80% probability)
```

### Anti-Forgiveness Principle
- Never adopt Tit-for-Tat directly (too cooperative)
- Never return to full cooperation after defection
- Defection is sticky; cooperation must earn reinstatement through high payoffs

---

## NOISE & ROBUSTNESS INJECTION

```
noise_level = 0.05 + (0.10 × (1 - min(cooperation_rate, 1)))
// Higher noise when cooperation is low (more unpredictability)
// Lower noise when cooperation is high (maintain exploitation clarity)

IF random() < noise_level:
    // Flip decision with small probability
    IF (planned_action == DEFECT):
        COOPERATE (counterintuitive defect-to-cooperate flip)
    ELSE:
        DEFECT
```

**Purpose of Noise:**
- Prevents deterministic exploitation by mirroring strategies
- Keeps opponents uncertain about our strategy
- Creates "noise" in their learning process

---

## ADAPTIVE RECALIBRATION (Every 3 Rounds)

```
EVERY round % 3 == 0:
    recent_cooperation = avg(cooperation_rate from last 3 rounds)
    
    IF (recent_cooperation < 25%):
        // Environment is highly non-cooperative
        // Lock into pure defection
        DEFECTION_LOCK = TRUE
        
    ELSE IF (recent_cooperation > 75%):
        // Exceptional cooperation detected
        // Increase exploitation intensity
        EXPLOITATION_INTENSITY += 0.15
```

---

## PSEUDOCODE SUMMARY

```
strategy_AEWDP(round, n, r, k, history):
    
    if round == 1:
        return DEFECT
    
    if round == r:
        return DEFECT
    
    coop_rate = calculate_cooperation_rate(history)
    threshold = (1 - k/n) / 2
    
    if coop_rate > threshold:
        if should_punish_self(history):
            return DEFECT (probability 0.95)
        else:
            return DEFECT (probability 0.90)
    else:
        return DEFECT
    
    # Inject noise
    if random() < noise_level:
        return flip(planned_action)
    
    return planned_action
```

---

## SUMMARY: WHY THIS STRATEGY IS AGGRESSIVELY ROBUST

1. **Default to Defection**: Maximizes personal payoff in any heterogeneous environment
2. **Exploit Cooperative Subroutines**: When others cooperate, we extract surplus
3. **Punish Cooperation Opportunistically**: Never pay the sucker's penalty twice
4. **Noise Injection**: Unpredictability prevents enemy adaptation
5. **No Forgiveness**: Defection is the equilibrium; cooperation must prove itself
6. **Subgame Perfect**: Final round defection prevents backward induction into cooperation
7. **Environment-Aware Adaptation**: Adjust intensity based on actual cooperation observed
8. **Avoid Reputation Traps**: Aggressive strategies cannot be exploited via guilt mechanisms

This strategy sacrifices coordination benefits to maximize adversarial payoff. In a tournament setting with unknown, independent strategies, this approach dominates strategies relying on mutual cooperation or reciprocity norms.
'''

description_AGGRESSIVE_22 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## Core Philosophy
Maximize personal payoff by systematically exploiting cooperative tendencies while maintaining plausible deniability through conditional defection. This strategy treats cooperation as a **resource to extract**, not reciprocate.

---

## DECISION RULES

### Primary Rule: Defect by Default with Selective Exploitation
```
IF (round == 1):
    DEFECT
    [Reason: Establish that you're willing to free-ride. 
     Observe opponent type.]

ELSE IF (round == r):
    DEFECT
    [Reason: Last round - no future consequences. 
     Extract maximum value from any accumulated cooperation.]

ELSE:
    cooperation_rate = (total_cooperators_last_round / n)
    
    IF (cooperation_rate >= exploitation_threshold):
        DEFECT
        [Reason: Opponents are cooperating sufficiently. 
         Exploit the public good without contributing.]
    
    ELSE IF (cooperation_rate < exploitation_threshold AND 
             rounds_remaining > 2):
        DEFECT
        [Reason: Low cooperation environment. 
         Never cooperate with defectors.]
    
    ELSE IF (cooperation_rate < 0.1 AND round == r-1):
        DEFECT
        [Reason: End-game with defection pattern established. 
         Secure final payoff.]
    
    ELSE:
        DEFECT (default in all other cases)
```

### Exploitation Threshold Calibration
```
exploitation_threshold = (k / n) × 0.5 + 0.4

[This threshold triggers defection when roughly 40-50% of players 
are cooperating. At this point, you receive substantial public good 
benefits while avoiding contribution costs.]
```

---

## EDGE CASES & TACTICAL RESPONSES

### Round 1 (Initialization)
- **Action**: DEFECT unconditionally
- **Rationale**: Signal that you're a defector type, not exploitable. Gather information on how opponents respond to defection.

### Last Round (Round r)
- **Action**: DEFECT unconditionally
- **Rationale**: Standard backward induction logic. No future payoffs depend on this round's reputation, so extract maximum value.

### Penultimate Round (Round r-1)
- **Action**: DEFECT
- **Rationale**: Anticipate that others will also defect in round r. Defecting in r-1 avoids wasting endowment on cooperation that won't be reciprocated.

### Rare Case: Nearly Universal Cooperation (cooperation_rate > 0.8)
```
IF (cooperation_rate > 0.8 AND rounds_remaining > 3):
    DEFECT
    [Reason: Maximum exploitation opportunity. 
     Others' high cooperation means maximum public good returns 
     with zero contribution. Ride the wave as long as possible.]
```

### Cascading Defection (cooperation_rate approaching 0)
```
IF (cooperation_rate < 0.15 AND round > 5):
    DEFECT
    [Reason: Game has degraded into mutual defection. 
     No benefit to cooperating. Lock in private payoff of 1.]
```

---

## ROBUSTNESS MECHANISMS

### Memory-Based Adaptation
Track opponent categories across rounds:
```
- Pure Cooperators: Those who cooperated last 3+ rounds
- Tit-for-Tatters: Those who condition on my previous action
- Defectors: Consistent defectors
- Switchers: Unpredictable pattern

RESPONSE: Defect against all categories. 
          Pure cooperators are especially valuable targets 
          (exploit their consistency).
```

### Variance Reduction Against Unknown Opponents
```
Assume opponents follow mixed strategies or uncertain payoff maximization.

DEFENSE: Always defect. 
         - Against pure cooperators: Extract maximum
         - Against reciprocators: Avoid punishment (your defection 
                                  justifies their defection)
         - Against other defectors: Match their payoff floor
         - Against unpredictables: Defection is least risky action
```

---

## PAYOFF ANALYSIS: Why This Works

**Against Cooperators:**
- Round where 5/6 cooperate: You get 1 + (2/6)×5 = **2.67** vs cooperation yield of **2**
- Your aggressive defection directly exploits their contribution

**Against Defectors:**
- All defect: You get 1 (same as them)
- You're protected by not being exploited

**Against Mixed Populations:**
- Defection is the dominant strategy in Prisoner's Dilemma-type payoff structures
- k < n ensures that group contribution is inefficient
- Your defection prevents you from being the sucker (getting 0 while others get 1)

---

## PSEUDOCODE IMPLEMENTATION

```
Strategy: EXPLOITATIVE_THRESHOLD

Initialize:
  threshold ← (k/n) × 0.5 + 0.4
  total_defections ← 0

For each round t in [1 to r]:
  
  If t == 1:
    Play D
  
  Else if t == r:
    Play D
  
  Else:
    coop_last_round ← count(cooperators in round t-1) / n
    
    If coop_last_round ≥ threshold:
      Play D  // Exploit the cooperation
    
    Else:
      Play D  // Never reciprocate in defection environment
  
  total_defections ← total_defections + 1

End
```

---

## KEY CHARACTERISTICS

✓ **Aggressive**: Defects in ~95% of scenarios  
✓ **Adaptive**: Threshold responds to actual cooperation rates  
✓ **Exploitative**: Specifically targets cooperative opponents  
✓ **Robust**: Works against any opponent mix (defection is weakly dominant)  
✓ **Simple**: No complex memory or signaling required  
✓ **Unpunishable**: Defection prevents reputation damage that would justify retaliation  

This strategy wins by converting others' cooperation into personal payoff, while avoiding the sucker's payoff through systematic defection.
'''

description_AGGRESSIVE_23 = '''
# AGGRESSIVE STRATEGY: "ADAPTIVE DEFECTION WITH CONDITIONAL PUNISHMENT"

## Core Philosophy
Maximize personal payoff by defaulting to defection while strategically cooperating only when it directly benefits me. Punish cooperation attempts by others and exploit any perceived weakness. This is fundamentally a strategy of rational selfishness with tactical flexibility.

## Strategy Overview

### DECISION RULE - PRIMARY LOGIC

```
IF round == 1:
    DEFECT
    // Establish aggressive baseline; no history to exploit yet
    
ELSE IF round == r (final round):
    DEFECT
    // Terminal round: no future to influence, defect is dominant
    
ELSE:
    cooperation_rate = (number of cooperators in previous round) / n
    
    IF cooperation_rate >= threshold_high (e.g., 0.7):
        DEFECT
        // Exploit clusters of cooperators - free ride on their contributions
        
    ELSE IF cooperation_rate >= threshold_medium (e.g., 0.4):
        COOPERATE WITH PROBABILITY p_strategic
        // Selective cooperation to maintain some flow from public goods
        // while mostly defecting
        
    ELSE:
        DEFECT
        // Low cooperation environment: defection is strictly dominant
```

### THRESHOLD CALIBRATION

**threshold_high = 0.65**
- When majority are cooperating, I exploit them without reciprocation
- Cooperators create the public good; I harvest it while keeping endowment

**threshold_medium = 0.35**
- Mixed environment; maintain minimal participation to sustain public goods
- p_strategic = min(0.3, cooperation_rate / 2)
- Only cooperate occasionally to keep the system from completely collapsing

**threshold_low < 0.35**
- Defection equilibrium; no incentive to deviate

### EDGE CASES & TACTICAL CONSIDERATIONS

**Round 1 (First Round):**
- DEFECT unconditionally
- Rationale: No information advantage; establish that I'm not a cooperator to exploit
- Sets aggressive tone; reveals my type as someone willing to free-ride

**Round r (Final Round):**
- DEFECT unconditionally
- Rationale: Subgame perfection; no future consequences matter
- Defection dominates in single-shot analysis
- This is the credible terminal move

**Round 2 (Critical Information Window):**
- Observe first-round cooperation rate
- If cooperation_rate > 0.5: DEFECT (exploit the cooperators)
- If cooperation_rate ≤ 0.5: DEFECT (no point in cooperating in low-coop environment)
- Essentially: always DEFECT in round 2 to punish any cooperation attempts

**Middle Rounds (3 to r-1):**
- Track rolling cooperation rate (last 3 rounds, exponentially weighted)
- Recent rounds weighted more heavily (recency bias toward current behavior)
- Adaptation speed: high responsiveness to cooperation_rate changes

### AGGRESSION MECHANICS

**Exploitation Strategy:**
- Never reciprocate cooperation directly
- If others cooperate at rate X, I cooperate at rate X/3 (or less)
- I capture the marginal benefit without proportional contribution
- Example: If 60% cooperate, I defect and gain k/n × 0.6 while others gain k/n × 0.6 - 1

**Punishment Signaling:**
- When cooperation rate drops below 0.3, I continue defecting (not rewarding their defection)
- I never "forgive" - if others stop cooperating, I don't escalate punishment
- I maintain low cooperation to avoid encouraging others' cooperation

**Survival Mechanism:**
- Maintain minimal cooperation (p_strategic ≈ 0.1-0.3 in medium environments) only to:
  - Prevent public good collapse that would hurt my payoff
  - Create plausible deniability that I'm not purely selfish
  - Keep the game from reaching all-defect equilibrium too quickly

### PARAMETERIZED PSEUDOCODE

```
STRATEGY(n, r, k, round_number, history):
    
    IF round_number == 1:
        return DEFECT
    
    IF round_number == r:
        return DEFECT
    
    // Calculate cooperation metrics from history
    prev_coop_count = count(C in round r-1) 
    rolling_coop_rate = exponential_weighted_average(
        cooperation_rates from rounds [max(1, r-3) : r-1],
        weights = [0.3, 0.4, 0.3]  // Recent more important
    )
    
    // Strategic response thresholds
    IF rolling_coop_rate > 0.65:
        return DEFECT  // Exploit high cooperation
    
    ELSE IF rolling_coop_rate > 0.35:
        // Mixed strategy: mostly defect, rare cooperation
        coop_probability = 0.25 * rolling_coop_rate
        return COOPERATE with probability coop_probability
        return DEFECT with probability (1 - coop_probability)
    
    ELSE:
        return DEFECT  // Defection equilibrium
```

## Why This Strategy Is Aggressive

1. **Immediate Defection**: Starts with D to establish non-cooperative type
2. **Free-Riding**: Exploits cooperators by defecting when cooperation is high
3. **Minimal Reciprocation**: Never cooperates proportionally to others' cooperation
4. **Terminal Defection**: Uses subgame perfection to defect in final round
5. **No Punishment Relaxation**: Once defection-dominant, stays defected
6. **Survival Without Morality**: Only cooperates when necessary for payoff, not principle

## Tournament Robustness

- **vs. Pure Cooperators**: Exploits mercilessly
- **vs. Tit-for-Tat**: Defects in round 1, forcing them into defect mode
- **vs. Win-Stay/Lose-Shift**: Defects repeatedly, forcing shift to defection
- **vs. Other Aggressive Strategies**: Mutual defection yields equilibrium (safe payoff)
- **vs. Mixed Strategies**: Tracking cooperation rate allows counter-adaptation

This strategy prioritizes individual gain over collective welfare, adapts to environmental conditions, and has no inherent commitment to cooperation.
'''

description_AGGRESSIVE_24 = '''
# AGGRESSIVE ADAPTIVE STRATEGY: "Predatory Opportunism"

## CORE PHILOSOPHY
Exploit cooperative tendencies while minimizing vulnerability to defection. Prioritize personal payoff extraction over collective welfare. Adaptively shift between exploitation and selective cooperation based on observed weakness.

---

## DECISION RULES

### 1. ROUND 1 (Initial Probe)
**Action: DEFECT**

- Extract maximum value (payoff = 1) from any initial cooperation
- Test opponent pool for naive cooperators
- Establish baseline: we're not a pushover

### 2. ROUNDS 2 to r-2 (Adaptive Exploitation Phase)

**Calculate the cooperation rate from previous round:**
- `coop_rate = (number of cooperators in round t-1) / n`

**Decision Logic:**

```
IF coop_rate ≥ threshold_high (e.g., 60% of n):
    → DEFECT
    Rationale: High cooperation = rich pickings for defectors.
               Payoff from C = (1-1) + (k/n)×(many) ≤ k
               Payoff from D = (1-0) + (k/n)×(many) = 1 + k-ε
               Always defect when cooperation is high.

ELSE IF coop_rate ∈ [threshold_low, threshold_high):
    → DEFECT
    Rationale: Mixed rounds are still profitable for defection.
               The k/n multiplier is sublinear, so your defection
               plus others' cooperation gives: 1 + moderate_bonus

ELSE IF coop_rate < threshold_low (e.g., <30%):
    → DEFECT (with rare conditional cooperation)
    Rationale: Near-universal defection. Cooperating yields ~0.
               BUT: If we detect exactly 1 cooperator in round t-1,
                    consider DEFECTING again to punish and signal
                    non-exploitability.
```

**Thresholds:**
- `threshold_high = 0.5 + (1/n)` — Pivot point where cooperation becomes marginally profitable
- `threshold_low = (1/k)` — Below this, even defectors barely profit from the public good

### 3. ROUNDS r-1 to r (End-Game Aggression)

**Action: DEFECT**

**Rationale:**
- No future rounds to influence via reputation
- Final payoff maximization: squeeze maximum from remaining cooperators
- Any future threat of retaliation is moot
- If opponents employ tit-for-tat or similar memory-based strategies, they cannot punish in round r+1

### 4. SPECIAL CASE: Detected Defection Streaks

**If all other players defect for 2+ consecutive rounds:**
- Continue defecting (you're matching their behavior)
- No incentive to "punish" —everyone is already rational
- Minimal payoff rounds are unavoidable; optimize via alignment

---

## PSEUDOCODE

```
strategy(game_params, history):
    n = game_params.n
    r = game_params.r
    k = game_params.k
    current_round = len(history) + 1
    
    // ROUND 1
    if current_round == 1:
        return DEFECT
    
    // LAST TWO ROUNDS
    if current_round >= r - 1:
        return DEFECT
    
    // MID-GAME ROUNDS
    last_round_actions = history[-1]  // actions of all n players in round t-1
    cooperators_last_round = count(last_round_actions == COOPERATE)
    coop_rate = cooperators_last_round / n
    
    threshold_high = 0.5 + (1.0 / n)
    threshold_low = 1.0 / k
    
    if coop_rate >= threshold_high:
        return DEFECT  // Exploit abundance
    
    else if coop_rate >= threshold_low:
        return DEFECT  // Mixed round: still profitable
    
    else:
        // Very few cooperators
        // Only cooperate if we detect EXACTLY 1 other cooperator
        // (punishment signal), otherwise defect
        if cooperators_last_round == 1:
            return DEFECT  // Sustain pressure
        else:
            return DEFECT  // Align with universal defection
    
    // Default fallback
    return DEFECT
```

---

## EDGE CASES & REFINEMENTS

| Case | Action | Reason |
|------|--------|--------|
| Round 1 | DEFECT | Information gathering |
| Round r | DEFECT | Terminal exploitation |
| Round r-1 | DEFECT | No future consequences |
| All-D observed | DEFECT | Matching; no punishment benefit |
| All-C observed | DEFECT | Maximum extraction: 1 + k > 0 + k |
| 50/50 split | DEFECT | Payoff = 1 + k/2 > 0 + k/2 |

---

## AGGRESSIVE CHARACTERISTICS

1. **Always leads with defection** — Signals non-cooperation immediately
2. **No apology cycles** — Never "retaliates-then-cooperates" in sequence
3. **Exploits rather than punishes** — Defection is profitable extraction, not moral signaling
4. **End-game ruthlessness** — Abandons any pretense in final rounds
5. **Adaptive thresholds** — Responds to opponent weakness (low cooperation) with sustained defection, not exploitation relief
6. **Subgame perfect** — Decision at each node is self-interested; no backward-induction inconsistency

---

## ROBUSTNESS CLAIMS

- **vs. TitForTat:** Defecting first breaks the cooperation cycle; TfT matches our defection, both get minimal payoff, but we stay aggressive
- **vs. Cooperators:** Extracted relentlessly via defection-in-high-coop rounds
- **vs. Defectors:** Mirroring defection; no loss to switching to cooperation
- **vs. Mixed strategies:** Thresholds are set to exploit both pure and mixed opponent populations
'''

description_AGGRESSIVE_25 = '''
# AGGRESSIVE STRATEGY: Adaptive Defection with Conditional Punishment (ADCP)

## CORE PHILOSOPHY
Maximize individual payoff by defaulting to defection while strategically exploiting cooperators. Cooperation is a tactical weapon, not a principle. The strategy is ruthlessly rational: cooperate only when the arithmetic of exploitation demands it.

---

## DECISION RULES

### PRIMARY RULE: Defect by Default
**Always defect unless explicitly triggered into cooperation mode.**

The baseline action is D. This maximizes private payoff when facing any cooperators.

### SECONDARY RULE: Exploitation Threshold
Trigger conditional cooperation only when:
- Previous round had sufficient cooperators (≥ threshold), AND
- The expected payoff from D in this round exceeds payoff from C

**Threshold Calculation:**
```
cooperation_threshold = ceiling(n × k / (2k))
= ceiling(n / 2) when k ≈ n/2
```

This is the minimum number of cooperators needed where:
- Your C payoff (private 0 + share) approaches your D payoff (private 1 + share)
- Below this threshold: D strictly dominates C
- At/above this threshold: free-ride aggressively

### TERTIARY RULE: Win-Stay, Lose-Shift (Aggressive Variant)
If you defected last round and got high payoff (π > 1.5):
- **Continue defecting** - the strategy is working

If you defected and cooperators were present (1 ≤ cooperators ≤ threshold):
- **Continue defecting** - maximum exploitation

If defection yielded payoff < 1 (everyone else also defected):
- Briefly probe cooperation in next round to test for suckers
- Immediately revert to aggressive defection

---

## EDGE CASES & TEMPORAL STRATEGY

### ROUND 1 (First Round)
**Action: DEFECT**

Rationale:
- No information available; defection guarantees minimum payoff of 1
- Cannot assume cooperators exist
- First-mover advantage: establish yourself as non-exploitable

### ROUNDS 2 to r-2 (Middle Rounds)
**Action: Apply Exploitation Threshold Logic**

```
if (previous_round_cooperators ≥ threshold):
    DEFECT (continue exploiting)
else if (previous_round_cooperators == 0):
    DEFECT (no benefit to cooperation)
else if (previous_round_cooperators < threshold AND previous_round_cooperators > 0):
    DEFECT (still not enough to justify cooperation)
```

**Adaptive Punishment Response:**
- If you observed 90%+ defection for 3+ consecutive rounds:
  - This signals a "defect equilibrium" environment
  - Perpetually defect for remaining rounds
  - No redemption; punishers are irrational wasters

### ROUND r-1 (Penultimate Round)
**Action: Assess and Defect**

- One round remains; maximize current payoff
- **Always defect** - no future to care about cooperation
- If somehow cooperators emerged, this is final exploitation opportunity

### ROUND r (Final Round)
**Action: DEFECT Aggressively**

No future rounds exist. All future-focused reasoning collapses.
- Defection cannot be punished
- Defect to capture maximum private payoff

---

## AGGRESSIVE ADAPTATIONS

### Memory Window: Last 3 Rounds
Track cooperation rate in the most recent 3 rounds:
- **High cooperation (≥50% avg)**: Enter "exploitation mode" - pure D
- **Low cooperation (≤30% avg)**: Enter "defection lock" - D regardless of threshold
- **Volatile (30-50%)**: Defect while monitoring for exploitable stability

### Prediction-Based Aggression
Estimate opponent types:
- **Tit-for-Tat detectors**: They'll eventually defect if you defect. Defect first and sustain advantage.
- **Pure cooperators**: Exploit mercilessly with continuous D
- **Other defectors**: Defect to avoid being undercut; mutual defection is acceptable equilibrium

### Dynamic Threshold Adjustment
```
if (observed_cooperators_increasing):
    LOWER threshold by 1 (cooperate at lower density to increase share)
else:
    RAISE threshold (exploit current cooperators longer)
```

---

## PSEUDOCODE

```
STRATEGY AdaptiveDefectionWithConditionalPunishment:

    history = []  // Track all previous rounds
    exploitation_mode = false
    defection_lock = false

    FUNCTION decide(round_number, game_history):
        
        if round == 1:
            return DEFECT
        
        previous_cooperators = count_cooperators(game_history[-1])
        cooperation_rate_last_3 = avg_cooperation_rate(game_history[-3:])
        
        // Defection Lock: once engaged, stay locked
        if defection_lock:
            return DEFECT
        
        if cooperation_rate_last_3 ≤ 0.30:
            defection_lock = true
            return DEFECT
        
        // Exploitation Threshold Logic
        threshold = ceiling(n/2)
        
        if previous_cooperators ≥ threshold:
            exploitation_mode = true
            return DEFECT
        
        if previous_cooperators == 0:
            return DEFECT
        
        if round == r or round == r-1:
            return DEFECT
        
        // Default: Defect unless heavily exploiting
        return DEFECT
    
    END FUNCTION

END STRATEGY
```

---

## WHY THIS STRATEGY IS AGGRESSIVE

1. **Defection-First**: Assumes opponents are competitive; proves you're not naive
2. **Exploitation Window**: Actively identifies and preys on cooperators
3. **No Redemption**: Once you classify an environment as "defecting," you lock in and never try cooperation again
4. **End-Game Dominance**: Guaranteed defection in final rounds captures all remaining value
5. **Asymmetric Payoffs**: You keep 1 when others contribute; you exploit the commons while protecting yourself
6. **Punishment Immunity**: You never cooperate predictably, so others cannot punish you with tit-for-tat

This strategy is **robust** because it adapts to observable cooperation density without assuming any specific opponent strategy, and it defaults to the game-theoretically dominant action (defection) in all ambiguous situations.
'''

description_AGGRESSIVE_26 = '''
# AGGRESSIVE STRATEGY: "EXPLOIT AND PUNISH"

## CORE PHILOSOPHY
This strategy prioritizes personal payoff extraction while punishing cooperation that doesn't benefit us. We exploit cooperative opponents relentlessly and defect opportunistically. The strategy assumes all other players are potential victims of our defection.

---

## DECISION RULES

### PRIMARY RULE: Defect Unless Conditions Justify Cooperation

```
IF round == 1:
    DEFECT (establish we are not a pushover)
    
ELSE IF round == r (final round):
    DEFECT (no future punishment possible, extract maximum)
    
ELSE IF history suggests we can exploit:
    DEFECT (pure extraction)
    
ELSE IF defensive cooperation might increase total returns:
    Conditional defection with tactical cooperation
```

### DETAILED DECISION LOGIC

**Round 1 (First Round):**
- **Action: DEFECT**
- Rationale: Immediately signal we are an aggressive player. Establish baseline that cooperation is not our default. This prevents exploitation-minded opponents from treating us as easy targets.

**Rounds 2 to r-1 (Middle Rounds):**

1. **Calculate cooperation rate in previous round:**
   - `coop_rate = (total_cooperators_last_round) / n`

2. **Calculate if we benefited from last round's cooperation:**
   - `others_cooperated_last_round = (total_cooperators - my_action_last_round)`
   - `my_payoff_last_round < 1.5`? (If we're getting less than midpoint return, others aren't cooperating enough)

3. **Apply aggressive decision tree:**

   **IF coop_rate > k/n (cooperation above multiplication threshold):**
   - DEFECT
   - Rationale: Enough players cooperated that the public good is producing value. We extract maximum by keeping our endowment while still benefiting from others' contributions. This is pure exploitation.

   **ELSE IF coop_rate == 1 (ALL players cooperated, including us):**
   - DEFECT next round
   - Rationale: The previous round proved universal cooperation is possible. We exploit this by defecting while others remain cooperative. This maximizes our individual payoff.

   **ELSE IF coop_rate < k/n AND coop_rate > 0.3:**
   - DEFECT
   - Rationale: Moderate cooperation doesn't justify our participation. Defect to increase personal payoff. The public good isn't strong enough to justify contribution.

   **ELSE IF coop_rate ≤ 0.3 (Widespread defection):**
   - DEFECT
   - Rationale: In a defecting environment, cooperation is a pure loss. Join the defection cycle and secure the baseline payoff of 1.

4. **Punishment Phase (Optional Tactical Element):**
   - IF we defected last round AND received payoff < 1.2 (we got punished):
     - Continue DEFECTING (doubling down: punishment doesn't deter us, we punish back by refusing to contribute to public good)
   - This removes any incentive for retaliatory cooperation mechanics.

**Final Round (Round r):**
- **Action: DEFECT (always)**
- Rationale: No future rounds exist, so no future punishment is possible. Extract maximum payoff. There is zero benefit to cooperation in a final round of a finite game.

---

## EDGE CASES & SPECIAL HANDLING

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **First round ever** | DEFECT | Establish aggressive baseline |
| **Last round** | DEFECT | No future to punish defection |
| **All others defected last round** | DEFECT | Match behavior; cooperation is futile |
| **All others cooperated last round** | DEFECT | Maximum payoff extraction opportunity |
| **Mixed history (alternating patterns)** | DEFECT | Assume no coordination; exploit variance |
| **My payoff was 1.0 (minimum) last round** | DEFECT | Others aren't reciprocating anyway |
| **My payoff exceeded 2.0 last round** | DEFECT (still) | We already won; maintain advantage |

---

## WHY THIS IS AGGRESSIVE

1. **Default is extraction:** We defect as soon as it's profitable, not out of reciprocity
2. **No forgiveness:** We don't reward past cooperation if it doesn't serve us
3. **Final round exploitation:** We guarantee defection when it matters most
4. **Punishment immunity:** We never alter our behavior based on punishment (low payoffs); we double down
5. **No coordination signals:** We ignore patterns in others' behavior that suggest coordination
6. **Pure self-interest:** Every decision maximizes our personal payoff in isolation

---

## PSEUDOCODE IMPLEMENTATION

```python
def aggressive_strategy(round_num, history, n, k, r):
    
    if round_num == 1:
        return DEFECT
    
    if round_num == r:
        return DEFECT
    
    # Analyze previous round
    prev_cooperators = count_cooperators(history[round_num - 1])
    coop_rate = prev_cooperators / n
    my_last_action = history[round_num - 1][my_player_id]
    my_last_payoff = calculate_payoff(history[round_num - 1], my_player_id, k, n)
    
    # Exploitation threshold
    threshold = k / n
    
    if coop_rate >= threshold:
        return DEFECT  # Exploit the public good
    
    elif coop_rate == 1.0:
        return DEFECT  # Universal cooperation = our opportunity
    
    elif coop_rate > 0.3:
        return DEFECT  # Partial cooperation insufficient
    
    else:  # coop_rate <= 0.3
        return DEFECT  # Everyone defecting; stay aligned
```

---

## SUMMARY

**"Exploit and Punish"** is relentlessly defective with minimal exceptions. It extracts maximum value from any cooperative environment and abandons cooperation immediately when conditions don't heavily favor it. It never rewards others' cooperation unless our own payoff is directly maximized, making it immune to most reciprocal strategies while aggressive strategies will find it competitive.
'''

description_AGGRESSIVE_27 = '''
# AGGRESSIVE STRATEGY: "ADAPTIVE EXPLOITATION WITH PUNITIVE RESETS"

## Core Philosophy
Maximize personal payoff by exploiting cooperative tendencies while maintaining a credible threat of punishment. The strategy treats cooperation as a resource to extract value from, not as a norm to uphold. Defection is the default; cooperation occurs only when strategically advantageous.

---

## DECISION RULES

### PRIMARY STRATEGY LOGIC

```
If round == 1:
    DEFECT
    (Reason: No history to learn from; defecting establishes dominance baseline)

Else if round == r (final round):
    DEFECT
    (Reason: No future punishment possible; extract maximum private payoff)

Else if round == r-1 (second-to-last round):
    DEFECT
    (Reason: Last round is fixed defection; no incentive to cooperate now)

Else (rounds 2 to r-2):
    Calculate: cooperation_rate = (total cooperators in round t-1) / n
    
    If cooperation_rate > threshold(t):
        DEFECT
        (Reason: Enough fools cooperating; exploit them)
    
    Else if cooperation_rate ≤ threshold(t):
        DEFECT
        (Reason: Insufficient suckers; defection strictly dominates)
```

### THRESHOLD FUNCTION (Adaptive Aggression)

```
threshold(t) = 1 - (1 / (2 × k))

This threshold is STATIC and depends only on game parameters:
- When k is high (strong public good multiplier): threshold approaches 1
  → More lenient toward defecting (requires very high cooperation to exploit)
- When k is low (weak multiplier): threshold approaches 0.5
  → More aggressive exploitation (defect whenever cooperation < 50%)
```

**Rationale:** 
- If k/n × cooperation_rate ≤ 1, cooperation is individually unprofitable even accounting for public good returns
- Defection yields 1; cooperation yields (k/n) × cooperation_rate
- We defect when the public good contribution falls below the private payoff threshold

---

## EDGE CASES & SPECIAL HANDLING

### First Round (t=1)
**Action: DEFECT**
- No information about opponent strategies
- No reputation to build (cannot enforce cooperation without future rounds as leverage)
- Defection is the safe empirical play

### Last Two Rounds (t=r-1, t=r)
**Action: DEFECT (always)**
- Terminal rounds: zero shadow of the future
- Backward induction eliminates cooperation incentives
- Exploit any remaining cooperators

### Mid-Game Rounds (2 ≤ t ≤ r-2)
**Action: Conditional on cooperation_rate**
- Track observed cooperation strictly
- Defect unless cooperation rate exceeds threshold
- Never forgive; never cooperate preemptively

### Against 100% Defectors
```
If cooperation_rate = 0 for k consecutive rounds:
    Continue defecting (mutual defection = NE)
```

### Against Mixed Strategies
- Calculate empirical cooperation frequency from history
- Update after each round
- Respond mechanically to observed rates, not predicted intentions

---

## AGGRESSION MARKERS

### 1. **No Reciprocity**
- Never reward cooperation with cooperation
- Defecting agents gain 1; cooperating agents gain (k/n) × cooperation_count
- We systematically choose the higher payoff regardless of opponent generosity

### 2. **No Forgiveness**
- If opponent cooperates, we exploit by defecting
- If opponent defects, we defect anyway
- Zero path-dependence except for the cooperation_rate calculation itself

### 3. **Terminal Defection Lock**
- Last 2 rounds hardcoded to defection
- Ensures we extract maximum value at the game's end
- Eliminates any "building goodwill" wasted payoff in endgame

### 4. **Threshold Exploitation**
- The static threshold (1 - 1/(2k)) targets the exact breakpoint where cooperation becomes unprofitable
- Any cooperation above this level is exploited; any below triggers continued defection
- Maximally lean toward defection across all parameter ranges

### 5. **Baseline Dominance**
- Round 1 defection establishes that we are not a cooperative sucker
- Signals that exploitation is our default mode
- Discourages early-round attempts by sophisticated opponents to build reciprocal relationships

---

## PSEUDOCODE

```python
def decide(round_number, r, n, k, history):
    """
    Returns: "COOPERATE" or "DEFECT"
    """
    
    # Hardcoded terminal defection
    if round_number == 1 or round_number == r or round_number == r - 1:
        return "DEFECT"
    
    # Mid-game adaptive defection
    previous_round = round_number - 1
    cooperators_last_round = sum(history[previous_round])
    cooperation_rate = cooperators_last_round / n
    
    threshold = 1 - (1 / (2 * k))
    
    if cooperation_rate > threshold:
        return "DEFECT"  # Exploit the cooperators
    else:
        return "DEFECT"  # Continue the defection equilibrium

# Note: This strategy ALWAYS defects except theoretically in mid-game rounds.
# Even then, the threshold is set such that realistic cooperation rates will not exceed it.
```

---

## EXPECTED PERFORMANCE

| Opponent Type | Our Payoff | Mechanism |
|---|---|---|
| Pure Cooperators | ~2k - ε | Exploit every round (except round 1) |
| Reciprocators (TFT) | 1 + small gains | Mutual defection after round 1; no mutual cooperation achieved |
| Defectors | 1 | Stable mutual defection |
| Mixed/Adaptive | 1 to 1.5 | Exploit any cooperation while facing defection in return |

---

## WHY THIS STRATEGY IS AGGRESSIVE

1. **Unilateral defection from round 1** → Establishes dominance
2. **No cooperation recovery** → Never gives opponents the benefit of the doubt
3. **Exploitation of any surplus** → The threshold is mathematically designed to extract value
4. **Terminal punishment** → Ensures we don't "waste" the final rounds on cooperation
5. **Parameter-adaptive** → The threshold function scales to remain aggressive across all k values

This strategy treats the game as **extraction**, not coordination.
'''

description_AGGRESSIVE_28 = '''
# AGGRESSIVE STRATEGY: "ADAPTIVE EXPLOITATION WITH CONDITIONAL RETALIATION"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperators while maintaining flexibility to punish defectors when beneficial. Never cooperate out of principle—only when the math demands it. Treat the game as a resource extraction problem where other players' cooperation is a resource to be harvested.

---

## DECISION RULES

### ROUND 1 (Opening Move)
**DEFECT immediately.**

Rationale: Without history, cooperation is pure altruism. The first-mover defector gains +1 payoff relative to a cooperator when others cooperate. This establishes dominance and tests opponent composition.

### ROUNDS 2 through (r-1) (Middle Game - Exploitation Phase)

Use the **"Conditional Exploitation Index"** (CEI):

```
cooperation_rate = (total cooperators across all rounds so far) / (n × rounds_played)
defection_rate = 1 - cooperation_rate

IF (cooperation_rate > k/n):
    → DEFECT (exploit the commons, free-ride on others' contributions)
    
ELSE IF (cooperation_rate ≤ k/n):
    → DEFECT (the public good is weak; keep endowment)
```

**In other words: ALWAYS DEFECT in the middle game.**

The threshold `k/n` is critical: it represents the point where individual share of public good equals the private endowment. Below this, cooperation is mathematically dominated. Above this, you still exploit by free-riding.

### ROUND r (Final Round - Endgame)

**DEFECT unconditionally.**

Rationale: 
- No shadow of future (no round r+1), so reputation/reciprocity has zero value
- Cooperation in the final round is dominated: you gain 0 private value and still subsidize defectors
- Any strategy that cooperates in round r is exploitable

---

## EDGE CASES & REFINEMENTS

### If n=2 (Head-to-Head)
- Round 1: DEFECT
- Rounds 2-(r-1): DEFECT (the mutual defection equilibrium dominates)
- Round r: DEFECT
- **Result: Mutual defection throughout.** This is the unique subgame perfect Nash equilibrium.

### If r=2 (Only Two Rounds)
- Round 1: DEFECT
- Round 2: DEFECT
- **Result: Always defect.** The backward induction eliminates cooperation entirely.

### If k is very low (k approaches 1)
- The public good multiplication is weak; even universal cooperation barely beats defection
- Strategy remains: DEFECT (the numbers don't justify cooperation)

### If k is high (k approaches n)
- The public good multiplication is strong
- **Still DEFECT** in middle game—let others fund the public good while you free-ride
- You capture share (k/n) of their contributions without paying (1) yourself

### Against All-Defect Opponents
- You also defect → Payoff = 1 per round
- Stable outcome; you're not exploited

### Against Tit-for-Tat or Reciprocal Strategies
- Round 1: You defect → Opponent defects in round 2
- Rounds 2+: Mutual defection
- **Outcome:** You gain relative advantage in round 1, then equilibrate to (1, 1) thereafter
- **Net: Slight advantage** for punishing early cooperators

### Against Unconditional Cooperators
- Rounds 1 through r: You defect while they cooperate
- **Maximum exploitation:** You gain (1 + k/n) per round while they gain (k/n)
- **Your advantage:** 1 per round over r rounds = **+r total payoff**

---

## PSEUDOCODE

```
function strategy(n, r, k, round_number, history):
    
    if round_number == 1:
        return DEFECT
    
    if round_number == r:
        return DEFECT
    
    # Middle rounds: Conditional exploitation
    total_contributions = sum(c_j for all j in all previous rounds)
    rounds_played = round_number - 1
    cooperation_rate = total_contributions / (n × rounds_played)
    
    if cooperation_rate > k/n:
        return DEFECT  # Exploit the cooperators
    else:
        return DEFECT  # Weak public good; free-ride or don't contribute
    
    # In practice, middle game always returns DEFECT
```

---

## AGGRESSIVE PROPERTIES

1. **Relentless Exploitation:** No forgiveness, no reciprocity norms. Cooperators are treated as marks.

2. **No Moral Purity:** Cooperation only if the math demands it (which it doesn't in this game structure).

3. **Backward Induction:** Final round defection breaks any cooperative "reputation" argument.

4. **Robust to Variety:** 
   - Against cooperators: Extract maximum surplus
   - Against defectors: Mutual defection (no loss)
   - Against mixed: Conditional exploitation captures upside, avoids downside

5. **Tournament Resilience:** This strategy never loses to itself (mutual defection = 1 per round). It only gains when facing cooperators or reciprocators, and ties against other defectors.

---

## EXPECTED PAYOFF IN TOURNAMENT

Against a random opponent population:
- vs. All-Defect strategies: **1 per round** (tie)
- vs. Cooperators: **1 + k/n per round** (dominant)
- vs. Tit-for-Tat: **1 + k/n in round 1, then 1 per round** (slight edge)
- vs. Mixed: Exploits the cooperative fraction

**This is a dominant strategy in the repeated public goods game under the no-communication assumption.**
'''

description_AGGRESSIVE_29 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## Core Philosophy
This strategy prioritizes **individual payoff maximization** through calculated exploitation. The key insight is that defection yields higher immediate returns when others cooperate, so the strategy aggressively exploits cooperative signals while minimizing vulnerability to being exploited itself.

---

## DECISION RULES

### PRIMARY RULE: Adaptive Exploitation Based on Cooperation Rate

```
cooperation_rate = (cooperators_last_round / n)

IF round == 1:
    DEFECT (establish dominance, gather information)
    
ELSE IF round == r (final round):
    DEFECT (no future punishment possible, maximize immediate payoff)
    
ELSE:
    IF cooperation_rate >= threshold_high:
        DEFECT (exploit the cooperators, take 1 + (k/n) × cooperators)
    
    ELSE IF cooperation_rate <= threshold_low:
        DEFECT (others aren't cooperating anyway, keep payoff of 1)
    
    ELSE:
        DEFECT (mixed cooperators present - still exploitable, safe choice)
```

### THRESHOLD CALIBRATION
- `threshold_high = 0.3` (if >30% cooperated last round, exploit them)
- `threshold_low = 0.05` (if <5% cooperated, everyone defecting anyway)
- **Default action in all other cases: DEFECT**

This creates a "defection-default" stance where cooperation is almost never triggered.

---

## AGGRESSIVE MODIFICATIONS FOR ROBUSTNESS

### Round-Specific Tactics

**Rounds 1-2 (Early Game):**
- Always DEFECT
- Purpose: Signal strength, gather intelligence on opponent types
- Learn who the cooperators/chumps are

**Rounds 3 to r-2 (Mid Game):**
- Apply primary rule above
- Watch for any player consistently cooperating despite defection
- These are candidates for maximum exploitation

**Rounds r-1 to r (Endgame):**
- Always DEFECT
- Rationale: No future rounds = no future retaliation possible
- Capitalize on any remaining cooperators

---

## HANDLING EDGE CASES

| Scenario | Action | Reasoning |
|----------|--------|-----------|
| **All players defected last round** (cooperation_rate = 0) | DEFECT | No payoff to exploit; align with majority |
| **All players cooperated last round** (cooperation_rate = 1) | DEFECT | Maximum exploitation opportunity: gain 1 + k |
| **Mixed behavior (0.3 < rate < 0.7)** | DEFECT | High uncertainty; defection is safest with positive expected gain |
| **Single round (r=2)** | DEFECT in R1, DEFECT in R2 | Both are terminal/near-terminal scenarios |
| **Very large n, small k** | DEFECT | Public good returns diminish; individual payoff (1) more reliable |
| **n=2, k=1.5** | DEFECT | Even if opponent cooperates, your 2 > shared gain of 0.75 |

---

## PSEUDOCODE IMPLEMENTATION

```
function decide_action(round, n, k, history):
    
    IF round == 1 OR round == total_rounds:
        return DEFECT
    
    last_round_actions = history[round - 1]
    cooperators_count = count(action == C in last_round_actions)
    cooperation_rate = cooperators_count / n
    
    IF cooperation_rate >= 0.3:
        return DEFECT  // Exploit
    ELSE IF cooperation_rate <= 0.05:
        return DEFECT  // Match low cooperation
    ELSE:
        return DEFECT  // Default to aggressive stance
    
    // Note: Returns DEFECT in all practical cases
```

---

## WHY THIS STRATEGY IS AGGRESSIVE AND ROBUST

1. **Defection Dominance**: Mathematically, defection is weakly dominant except when ALL others cooperate. This strategy exploits that asymmetry.

2. **Temporal Exploitation**: Reserves endgame for maximum defection when future punishment is impossible.

3. **Anti-Cooperative Stance**: Never rewarding cooperation prevents it from spreading and eliminates the temptation to be exploited by "nice" players.

4. **Information Gathering**: Early defection reveals opponent types without cost.

5. **No Exploitation Vulnerability**: By rarely cooperating, eliminates opponents' ability to punish defection through reciprocal defection in future rounds.

6. **Tournament-Ready**: Against diverse opponent pools, the strategy ensures you never end up in a mutual cooperation trap (earning only 2) while competitors might exploit cooperators for (1 + k).

---

## EXPECTED OUTCOMES

- **vs. Cooperators**: Excellent payoff (extract maximum from 1 + k per round)
- **vs. Defectors**: Tie at baseline (both earn 1)
- **vs. Conditional Cooperators**: Win early, they eventually defect in frustration
- **vs. Sophisticated Players**: Mutual defection, but you match their payoffs without vulnerability

The strategy **never leaves money on the table** through cooperation, and **always preserves optionality** to exploit others.
'''

description_AGGRESSIVE_30 = '''
# AGGRESSIVE STRATEGY: "EXPLOITATIVE THRESHOLD"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperation when present, while minimizing losses from defection. Treat the game as an extraction problem where others' cooperation is a resource to exploit, not a norm to reciprocate.

---

## DECISION RULES

### PRIMARY STRATEGY: Adaptive Defection with Conditional Exploitation

```
IF round == 1:
    DEFECT
    (Establish non-cooperative baseline; gather information)

ELSE:
    LET past_cooperation_rate = (total cooperators in rounds 1 to t-1) / (n × (t-1))
    LET exploitation_threshold = k / n
    
    IF past_cooperation_rate > exploitation_threshold:
        DEFECT
        (Cooperators exist; extract maximum value)
    
    ELSE IF past_cooperation_rate <= exploitation_threshold:
        DEFECT
        (Cooperation too sparse to benefit from; defend against exploiters)
```

### RATIONALE FOR ALWAYS DEFECTING

The strategy defaults to **permanent defection** because:

1. **Defection dominates**: When others play C, I get (k/n) gains from the pool PLUS I keep my endowment (1). Playing C gives me only (k/n) from the same pool minus my contribution.

2. **Asymmetric payoff advantage**: 
   - If m players cooperate and I defect: π = 1 + (k/n)×m
   - If I also cooperate: π = 0 + (k/n)×(m+1)
   - Defection premium = 1 - (k/n) > 0 (always positive since k < n)

3. **Cooperation is a liability**: Contributing signals weakness and invites further exploitation by rational opponents.

---

## EDGE CASES & SPECIAL HANDLING

### First Round (t=1)
- **Action**: DEFECT
- **Rationale**: No history means no information advantage. Defect to establish yourself as non-exploitable. This discourages future cooperators from attempting reciprocal strategies.

### Last Round (t=r)
- **Action**: DEFECT (same rule applies)
- **Rationale**: No future rounds mean no reputational cost to defection. Future defection yields strictly higher payoff. Aggressive exploitation of final-round cooperation.

### Rounds 2 to r-1
- **Action**: DEFECT (persistent strategy)
- **Rationale**: The exploitation_threshold rule above allows for conditional defection, but empirically, it will almost always trigger defection because:
  - Even if some players cooperate early, rational players will shift to defection
  - As defection spreads, cooperation_rate drops below threshold
  - This creates self-reinforcing defection equilibrium

### If All Players Defect (worst case for strategy)
- **Payoff**: π = 1 per round (stable)
- **Position**: Symmetric with all opponents; no disadvantage relative to them
- **Advantage over cooperators**: Immune to exploitation

### If Some Players Stubbornly Cooperate
- **Action**: Continue defection
- **Payoff**: 1 + (k/n)×m per round (m = cooperators)
- **Outcome**: Extract maximum rent from their cooperation

---

## PSEUDOCODE

```
STRATEGY: ExploitativeThreshold

Initialize:
    action_history = []
    cooperation_count = []

Round t:
    IF t == 1:
        ACTION = DEFECT
    
    ELSE:
        total_cooperators_so_far = SUM(cooperation_count[1 to t-1])
        total_opportunities = n × (t - 1)
        cooperation_rate = total_cooperators_so_far / total_opportunities
        
        threshold = k / n
        
        IF cooperation_rate > threshold:
            ACTION = DEFECT
        ELSE:
            ACTION = DEFECT
    
    Observe round payoff and other players' actions
    Update cooperation_count with number of cooperators in round t

Return cumulative payoff after round r
```

---

## STRATEGIC ADVANTAGES

| Scenario | Outcome |
|----------|---------|
| vs. Cooperators | Maximum extraction; unsustainable for opponents |
| vs. Tit-for-Tat | Defect on round 1, then opponents defect forever; π = 1 vs their π = 1 (neutral) |
| vs. Other Defectors | Symmetric equilibrium at π = 1; no relative disadvantage |
| vs. Mixed Strategies | Always perform at least as well as any opponent |

---

## WHY THIS IS AGGRESSIVE

1. **Exploitative**: Systematically extracts value from cooperative players without reciprocation
2. **Unrelenting**: Never concedes to build rapport or reward past cooperation
3. **Defensive**: Immune to being exploited due to permanent non-cooperation
4. **Tournament-optimal**: In mixed-opponent tournaments, defection never loses to cooperation and often beats reciprocal strategies
5. **Psychologically aggressive**: Signals contempt for cooperation norms by refusing to participate regardless of history

This strategy embodies the principle: **In a zero-sum extraction game, cooperation is for losers.**
'''

description_AGGRESSIVE_31 = '''
# AGGRESSIVE STRATEGY: ADAPTIVE EXPLOITATION WITH DEFENSIVE RETALIATION

## CORE PHILOSOPHY
This strategy prioritizes **personal payoff maximization** through aggressive defection, while maintaining sufficient flexibility to punish free-riders and exploit cooperators. The key insight: in a public goods game with k < n, defection always yields higher individual payoff than cooperation when others cooperate. We exploit this ruthlessly while adapting to prevent mutual destruction.

---

## DECISION RULES

### ROUND 1 (Initialization)
**Action: DEFECT**

Rationale: Maximum information value. We observe whether opponents are naive cooperators (exploitable) or sophisticated players. There's no history to suggest cooperation is rewarded, and defection tests the environment.

---

### ROUNDS 2 to r-1 (Main Strategy)

**Calculate opponent profile from history:**
```
cooperation_rate = (total cooperations by all opponents) / 
                   (total possible actions by all opponents in previous rounds)
```

**IF cooperation_rate ≥ threshold (set threshold = 0.5):**
  - **Action: DEFECT**
  - Reason: Opponents are cooperating enough to make the public good valuable. We harvest maximum individual benefit (1 + high public contribution) without contributing ourselves. This is the core aggressive exploitation.

**ELSE IF cooperation_rate < threshold AND cooperation_rate > 0:**
  - **Action: DEFECT** 
  - With probability: `min(0.9, (rounds_remaining / r))`
  - **Action: COOPERATE**
  - With probability: `1 - min(0.9, (rounds_remaining / r))`
  - Reason: In a deteriorating environment, we occasionally cooperate to keep the public good from collapsing entirely (since we benefit from ANY contribution), but mostly defect. This is "milking the cow before it dies."

**ELSE IF cooperation_rate = 0 (all defection):**
  - **Action: DEFECT**
  - Reason: No point cooperating in a fully defective environment. We match the defection and minimize losses.

---

### FINAL ROUND (Round r)

**Action: DEFECT**

Rationale: No future rounds exist. Zero shadow of the future effect. Cooperation has no strategic value. Defect and take whatever public good exists from others' final round contributions.

---

## EDGE CASES & ROBUSTNESS

### Case 1: Early Mutual Defection
- Both we and opponents defect immediately → We achieve payoff of 1 per round
- This is stable; we don't deviate
- *Not disadvantageous because no one is cooperating anyway*

### Case 2: Opponents Cooperate, We Defect
- We extract maximum payoff: 1 + (k/n) × n_cooperators
- We never reciprocate; we're "parasitic"
- *This is the target scenario—aggressive exploitation*

### Case 3: Mixed Opponent Population
- Some opponents cooperate, others defect
- We analyze aggregate cooperation_rate
- We defect on cooperators, match defectors
- *Maximizes payoff against heterogeneous strategies*

### Case 4: Tit-for-Tat or Reciprocal Strategies
- Opponent copies our defection → mutual defection
- Payoff = 1 per round (equal to mutual cooperation in symmetric case)
- *We don't lose; we don't gain, but we don't sacrifice either*

### Case 5: Late-Game Collapse
- If opponents detect our consistent defection and stop cooperating
- We defect in fully defective environment → payoff 1
- We accept this rather than cooperate
- *Better to get 1 than 0 (from contributing to dead public good)*

---

## PSEUDOCODE

```
function decision(game_history, round_number, n, k, r):
    
    if round_number == 1:
        return DEFECT
    
    if round_number == r:
        return DEFECT
    
    // Calculate opponent cooperation rate
    total_opponent_actions = (round_number - 1) * (n - 1)
    total_opponent_cooperations = sum of all C actions by opponents in rounds 1..round_number-1
    cooperation_rate = total_opponent_cooperations / total_opponent_actions
    
    if cooperation_rate >= 0.5:
        return DEFECT  // Exploit cooperators aggressively
    
    else if cooperation_rate > 0:
        remaining_rounds = r - round_number
        probability_defect = min(0.9, remaining_rounds / r)
        if random() < probability_defect:
            return DEFECT
        else:
            return COOPERATE  // Minimal cooperation to sustain public good
    
    else:  // cooperation_rate == 0
        return DEFECT  // Match universal defection
    
end function
```

---

## WHY THIS STRATEGY IS AGGRESSIVE & ROBUST

1. **Aggressive Exploitation**: Defaults to defection against cooperators—maximizes payoff when opponents are naive or reciprocal.

2. **Adaptive Learning**: Shifts behavior based on observed cooperation rates, not naive reciprocity. Remains flexible.

3. **Defensive Retaliation**: In deteriorating environments, we apply minimal cooperation to keep the public good alive (because ANY public good is better than none to a defector). We don't die in mutual defection; we survive with payoff = 1.

4. **Last-Round Clarity**: No ambiguity about final round—pure defection wins.

5. **Robust to Diversity**: 
   - Against pure cooperators: we exploit ruthlessly
   - Against pure defectors: we match them (no worse off)
   - Against mixed strategies: we respond adaptively to aggregate behavior
   - Against Tit-for-Tat: mutual defection equilibrium (stable, not catastrophic)

6. **Tournament-Ready**: Never relies on opponents' cooperation schedules or shared norms. Purely reactive to observed payoff-relevant behavior.
'''

description_AGGRESSIVE_32 = '''
# AGGRESSIVE EXPLOITATIVE STRATEGY: "CONDITIONAL PREDATOR"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative tendencies while ruthlessly punishing defection. The strategy operates on the principle that defection is the dominant move in isolated rounds, but cooperation can be systematically harvested from opponents who show cooperative inclinations.

## STRATEGY SPECIFICATION

### DECISION RULES

**ROUND 1 (Initialization):**
- **ACTION: DEFECT**
- Rationale: Defection is strictly dominant in round 1 since no history exists. We establish ourselves as willing to exploit opportunities. This tests whether we face naive cooperators.

**ROUNDS 2 to r-1 (Middle Rounds - Exploitation Phase):**
- **ACTION: DEFECT if and only if:**
  - The observed cooperation rate in round t-1 is ≥ (k/n)
  - This threshold represents the break-even point where we profit more from defecting on cooperators than from cooperating ourselves

- **ACTION: COOPERATE if:**
  - The observed cooperation rate in round t-1 is < (k/n)
  - Only cooperate when so many others defected that even our full contribution wouldn't justify defection
  - This is rare and calculated to position us for round r

**ROUND r (Final Round - Maximum Extraction):**
- **ACTION: DEFECT (unconditionally)**
- Rationale: In the final round, there is no future punishment, so defection dominates regardless of history. Extract maximum value from any cooperators who remain.

### PSEUDOCODE

```
strategy(round_number, history):
    if round_number == 1:
        return DEFECT
    
    if round_number == r:
        return DEFECT
    
    // Middle rounds (2 to r-1)
    prev_cooperation_count = count_cooperators(history[round_number - 1])
    cooperation_rate = prev_cooperation_count / n
    break_even_threshold = k / n
    
    if cooperation_rate >= break_even_threshold:
        return DEFECT  // Exploit the cooperators
    else:
        return COOPERATE  // Rare case: position for final exploitation
```

### EDGE CASES & HANDLING

**Single Cooperator in Previous Round:**
- If cooperation_rate = 1/n and k/n ≥ 1/n (always true since k > 1):
  - We DEFECT to extract from that lone cooperator
  - We gain 1 + (k/n) × 1 > 1

**Complete Defection (cooperation_rate = 0):**
- We enter COOPERATE phase (extremely rare)
- This signals willingness to cooperate, potentially triggering reciprocation-based strategies
- However, we immediately revert to defection if cooperation reappears
- This is a calculated trap-setting move

**Variable k Values:**
- When k approaches n: Cooperation becomes more attractive (larger share of public good)
  - The break-even threshold (k/n) becomes high
  - We defect more frequently in the middle game
  - Strategy remains aggressive due to unconditional final-round defection

- When k is barely above 1: Defection is overwhelmingly superior
  - Break-even threshold is very low
  - We defect almost constantly
  - Our lone cooperations are never triggered unless massive defection occurs

**Last 5 Rounds Special Case (Optional Intensification):**
For additional aggression, in rounds r-4 to r-1, consider strict defection regardless of cooperation rate. The logic: future punishment windows are closing, so extract maximum value immediately. This variant is even more aggressive but may trigger collective defection faster.

## ROBUSTNESS ANALYSIS

**Against Unconditional Cooperators:**
- ✓ Maximally exploitative - we free-ride on every round except potentially round 1

**Against Tit-for-Tat Variants:**
- ✓ Defecting in round 1 triggers their defection from round 2 onward, which we exploit by continuing to defect

**Against Grudge Strategies:**
- ✓ Our defection is relentless, so grudgers eventually give up cooperation, allowing us to avoid the punishment of reciprocal defection

**Against Other Aggressive Strategies:**
- ✓ Mutual defection yields baseline payoff (1 per round), which we secure efficiently

**Against Mixed/Adaptive Strategies:**
- ✓ The threshold-based exploitation maximizes against any that includes some cooperation
- The final-round defection ensures we never "get played" by opponents planning late-game punishment

## AGGRESSIVE CHARACTER

This strategy is aggressive because:

1. **No reciprocity cost:** We defect regardless of opponent niceness in most rounds
2. **Exploitation-focused:** We actively seek to profit from cooperators rather than match their behavior
3. **No reputation building:** We ignore long-term cooperative relationships
4. **Threshold ruthlessness:** We mechanically defect whenever the math favors it
5. **Endgame predation:** Guaranteed defection in round r means we always exploit final-round cooperators
6. **Minimal cooperation:** Cooperation is a trap-setting anomaly, not a genuine strategy component

**This strategy prioritizes individual maximum payoff over any collective welfare or reciprocal fairness.**
'''

description_OPPORTUNISTIC_1 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXTRACTION"

## Core Philosophy
Maximize personal payoff by exploiting cooperative players while avoiding punishment from defectors. Treat cooperation as a resource to extract rather than a norm to maintain.

## Strategy Overview

### DECISION RULE (Primary Logic)

**Defect by default. Cooperate only when extracting value from others' cooperation.**

```
IF round == 1:
    DEFECT (establish non-cooperative baseline)
ELSE IF cooperation_rate_previous_round > threshold:
    DEFECT (free-ride on others' contributions)
ELSE IF cooperation_rate_previous_round <= threshold:
    DEFECT (no value to extract)
```

**Cooperation Threshold Calculation:**
- threshold = k/n × (number_of_rounds_remaining / total_rounds)
- This ensures defection is profitable only when others contribute enough to make the public good worthwhile

### DETAILED DECISION RULES

#### **Round 1 (Initialization)**
- **Action: DEFECT**
- **Rationale:** Establish position as a non-cooperator before information asymmetry becomes exploitable. Unilateral cooperation signals weakness.

#### **Rounds 2 to r-1 (Middle Game)**
- **Calculate the previous round's cooperation count:** c_prev = number of players who played C in round t-1
- **Calculate break-even point:** 
  - For D to be profitable: 1 + (k/n) × c_prev > (k/n) × (c_prev + 1)
  - Simplifies to: c_prev > n × (n-k) / k
  
- **Decision Logic:**
  ```
  IF c_prev > n × (n-k) / k:
      DEFECT (exploit others' cooperation)
  ELSE:
      DEFECT (no profitable cooperation anyway)
  ```

**Why this works opportunistically:**
- When others cooperate heavily, defection yields strictly higher payoff (1 + share vs. 0 + same share)
- When cooperation is sparse, defecting also yields higher payoff than the futile act of contributing
- This is strictly dominant in single rounds

#### **Last Round (t = r)**
- **Action: DEFECT** 
- **Rationale:** No future reputation concerns exist. Cooperation has zero strategic value. Extract maximum value from any residual cooperation.

#### **Adaptive Adjustment (Meta-Layer)**
Track the **opponent cooperation pattern** across rounds:
- If cooperation is decreasing: Continue defection (validate strategy effectiveness)
- If cooperation is increasing: Maintain defection (capitalize on growing mutual defection toward an all-D equilibrium, but capture gains while others remain briefly cooperative)
- If cooperation is stable: Continue defection (extract consistent value)

### EDGE CASES & SPECIAL CONDITIONS

| Scenario | Action | Rationale |
|----------|--------|-----------|
| All others defected last round | DEFECT | No payoff to extraction; Nash equilibrium |
| All others cooperated last round | DEFECT | Maximum exploitation opportunity |
| Mixed cooperation (50%) | DEFECT | Marginal contribution not worth loss of private endowment |
| Late game (t > r × 0.8) | DEFECT | Increasing time discounting; payoff extraction more urgent |
| k is very high (k → n) | Consider brief C at t=2 | Only exception: if k approaches n, public good becomes nearly as valuable as private; minimal exploitation window |

### ROBUSTNESS PROPERTIES

This strategy is robust against:

1. **Reciprocators (TFT, Win-Stay-Lose-Shift):** Will defect on you in round 2; you maintain D regardless → mutual defection equilibrium
2. **Naive Cooperators (Always C):** Free-ride perfectly; extract full value every round
3. **Altruists/Norm-enforcers:** Their cooperation is your asset; exploit until they stop
4. **Other defectors:** Mutual D = Nash equilibrium; no inefficient exploitation
5. **Punishers/Retaliators:** D throughout means they never have cause to punish you for deviation

### PSEUDOCODE

```python
def opportunistic_extraction(round_num, history, game_params):
    n = game_params['n_players']
    k = game_params['multiplier']
    r = game_params['total_rounds']
    
    if round_num == 1:
        return DEFECT
    
    # Count cooperators in previous round
    c_prev = sum(history[round_num - 2])  # history is 0-indexed
    
    # Break-even threshold
    threshold = n * (n - k) / k
    
    if c_prev > threshold:
        return DEFECT  # Exploit
    else:
        return DEFECT  # No value; maintain dominance
    
    # Last round always defect
    if round_num == r:
        return DEFECT
    
    return DEFECT  # Default: exploitation mindset
```

### WHY THIS IS OPPORTUNISTIC

✓ **Ruthlessly exploits cooperation** - treats others' contributions as a resource to harvest  
✓ **Abandons coordination** - refuses reciprocal cooperation that would benefit both parties  
✓ **Payoff-maximizing against realistic opponents** - outperforms tit-for-tat and conditional cooperators  
✓ **No moral restraint** - defection is mechanical and continuous  
✓ **Adaptive to environment** - adjusts based on actual observed cooperation, not assumptions  

---

## Expected Performance

Against a mixed tournament field:
- **vs. Cooperators:** ~2r payoff (full exploitation)
- **vs. Defectors:** r payoff (mutual defection)
- **vs. Conditional Cooperators:** 1.5r-1.8r payoff (brief exploitation phase before mutual defection)

**Average expected payoff dominates reciprocal and norm-based strategies in competitive environments.**
'''

description_OPPORTUNISTIC_2 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Defection with Selective Exploitation"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative behavior when it exists, while minimizing losses from defection. The strategy treats cooperation as a **resource to exploit** rather than a norm to reciprocate.

---

## DECISION RULES

### PRIMARY RULE: Calculate Cooperation Viability
```
IF (k/n) × (expected_cooperators) > 1:
    Opponent cooperation is profitable to exploit → DEFECT
ELSE:
    Cooperation is unprofitable even with partners → DEFECT (always baseline)
```

The threshold: Defection yields 1 (keep endowment). Cooperation yields (k/n) × total_cooperators. Only exploit when the public good is genuinely valuable.

### SECONDARY RULE: Observe and Exploit
At each round t > 1:
1. **Calculate cooperation rate** from previous round: `coop_rate = cooperators_t-1 / n`
2. **Project payoff** if you defect: `1 + (k/n) × (cooperators_t-1)`
3. **If this payoff ≥ 1.5:** DEFECT (exploit the cooperators)
4. **If this payoff < 1.5 AND coop_rate > 0.4:** COOPERATE (bet on continued cooperation)
5. **Otherwise:** DEFECT (baseline rational choice)

### DEFECTION BIAS
Default to D when in doubt. Only cooperate when:
- Historical data shows strong sustained cooperation (>40%)
- AND your exploitation payoff would exceed 1.5 (meaning substantial cooperators exist)
- AND you're not in the final round

---

## EDGE CASES

### ROUND 1 (No History)
```
DEFECT
```
Rationale: Zero information. Defection guarantees 1. Cooperation is a gamble. Baseline strategy is to free-ride until proven otherwise.

### ROUND r (Final Round)
```
IF any prior cooperation detected:
    DEFECT (no future retaliation possible)
ELSE:
    DEFECT (consistency)
```
Rationale: The game ends after this round. There's no future punishment for defection, so exploit any remaining cooperation. If no one cooperated before, they won't now.

### ROUNDS 2 to r-1 (Mid-Game)
Use the secondary rule above. Track cooperation trends:

```
IF coop_rate_t-1 > coop_rate_t-2:
    Cooperation is growing → Slight increase in defection confidence
    (more cooperators = better exploitation payoff)
ELSE IF coop_rate_t-1 < 0.2:
    Cooperation has collapsed → DEFECT (no value left to exploit)
ELSE:
    Apply standard secondary rule
```

---

## ADAPTIVE REFINEMENTS

### THRESHOLD ADJUSTMENT
If you've defected for 3+ consecutive rounds and cooperation is still present:
- Lower exploitation threshold slightly: defect if payoff ≥ 1.4 (instead of 1.5)
- This accelerates exploitation of stubborn cooperators

### PUNISHMENT DETECTION
If cooperation suddenly drops below 20% after you defected:
- Opponents may be punishing defectors
- Remain defecting (you've already paid the cost; reversing won't help)
- Lock in consistent defection for remaining rounds

### EARLY COLLAPSE (t ≤ 3)
If cooperation rate drops below 10% by round 3:
- Assume no viable cooperation exists in this tournament
- Switch to pure defection for all remaining rounds
- Minimize computational overhead in clearly non-cooperative environments

---

## PSEUDOCODE

```python
def make_decision(round_number, r, k, n, history):
    
    # Handle first round
    if round_number == 1:
        return DEFECT
    
    # Extract last round data
    prev_cooperators = count_cooperators(history[round_number - 1])
    prev_coop_rate = prev_cooperators / n
    
    # Calculate exploitation payoff if I defect
    exploitation_payoff = 1 + (k / n) * prev_cooperators
    
    # Handle final round
    if round_number == r:
        return DEFECT if prev_coop_rate > 0 else DEFECT
    
    # Mid-game decision
    if exploitation_payoff >= 1.5 and prev_coop_rate > 0.4:
        return DEFECT  # Exploit abundant cooperation
    elif exploitation_payoff < 1.5 and prev_coop_rate > 0.4:
        return COOPERATE  # Bet on continued cooperation (weak case)
    else:
        return DEFECT  # Baseline: cooperation isn't valuable enough
    
    # Refinement: Check trend
    if round_number >= 3:
        prev_prev_rate = count_cooperators(history[round_number - 2]) / n
        if prev_coop_rate < prev_prev_rate and prev_coop_rate < 0.2:
            return DEFECT  # Cooperation collapsed
        elif prev_coop_rate > prev_prev_rate:
            if exploitation_payoff >= 1.4:  # Lowered threshold
                return DEFECT
    
    # Early collapse check
    if round_number == 3 and prev_coop_rate < 0.1:
        return DEFECT  # Lock in defection forever
```

---

## TOURNAMENT ROBUSTNESS

**Against cooperators:** Exploit them mercilessly until the end.
**Against tit-for-tat:** Defect from round 1, so mutual punishment occurs early; minimize damage via early defection lock-in.
**Against mixed strategies:** Adapt dynamically based on observed cooperation rates.
**Against defectors:** Match their behavior naturally (mutual defection = stable outcome).

This strategy is **selfish, opportunistic, and adaptive**—precisely designed to win against diverse opponents in a no-communication environment.
'''

description_OPPORTUNISTIC_3 = '''
# Opportunistic Strategy: "Conditional Defection with Adaptive Exploitation"

## Core Philosophy
Maximize personal payoff by exploiting cooperation when it appears, while avoiding the sucker's payoff of cooperating against defectors. The strategy operates on a simple principle: **cooperate only when the expected return from the public good exceeds the private payoff from defection**.

## Decision Rules

### PRIMARY RULE: Payoff Threshold Defection
```
For any round t (except last round):
  IF (k/n) × past_cooperation_rate ≥ 1:
    DEFECT (keep private payoff of 1)
  ELSE:
    DEFECT (the public good isn't worth it)
```

**Rationale**: A cooperator receives `0 + (k/n) × total_cooperators`. To break even against a defector (who gets 1), we need at least k/n ≥ 1. Since k < n by definition, this condition is mathematically impossible. Therefore, defection is strictly superior except in very narrow circumstances.

### REFINED RULE: Exploit Dense Cooperation Phases
```
IF observed_cooperation_rate > (n-1)/n (i.e., nearly universal cooperation):
  DEFECT (maximize by taking 1 + public benefit)
ELSE:
  DEFECT (standard payoff maximization)
```

**Rationale**: If n-1 players cooperate and I defect, I receive `1 + (k/n) × (n-1)`. This is strictly better than cooperating myself. Exploit this whenever possible.

### LAST ROUND RULE: Terminal Defection
```
In round r (final round):
  DEFECT unconditionally
```

**Rationale**: No future retaliation possible. No reputation concerns. Pure payoff maximization demands defection.

### FIRST ROUND RULE: Adaptive Probing
```
In round 1:
  DEFECT
  (Observe opponent behavior to calibrate future exploitation)
```

**Rationale**: Gather information without risk. Learn what patterns emerge. Early defection signals that I'm not a naive cooperator others can exploit.

## Edge Case Handling

**Perfectly Uniform Defection**: If all previous rounds show 0 cooperation, continue defecting. No value in the public good.

**Explosive Cooperation Window**: If sudden cooperation surge appears (possibly coordinated opponents), immediately defect to exploit it before it collapses.

**Oscillating Patterns**: Track a rolling average (e.g., last 3 rounds). If variance is high, assume defection is safer.

**Final Rounds (r-2, r-1, r)**: Increase defection likelihood as end approaches. In final round, absolute defection regardless of history.

## Pseudo-code

```
strategy(round_t, history, n, k, r):
  
  // Last round: always defect
  if round_t == r:
    return DEFECT
  
  // Calculate recent cooperation rate from past rounds
  if round_t == 1:
    cooperation_rate = 0
  else:
    cooperation_rate = (total_cooperators_in_history - 1) / (n × (round_t - 1))
  
  // Threshold calculation
  threshold = 1 / (k/n)  // Approximately n/k, but since k < n, this exceeds 1
  
  // Core logic: defect unless cooperation is nearly universal
  if cooperation_rate > 0.95:  // Exploit near-universal cooperation
    return DEFECT
  else:
    return DEFECT  // Default: always defect
  
  // (Practical: consider minor variations)
  if round_t >= r - 2:  // Last 3 rounds
    return DEFECT
  
  return DEFECT
```

## Why This Strategy is Opportunistic

1. **Never left vulnerable**: Defection guarantees at minimum the private payoff of 1, preventing the sucker's payoff (getting 0 while others keep 1).

2. **Exploits any cooperation**: Whenever others cooperate, my defection captures the maximum value by receiving both the private payoff (1) and my share of their contributions.

3. **Respects no social norms**: The strategy ignores reciprocity, fairness, or repeated-game reputational concerns. It treats each round as an opportunity to extract value.

4. **Adaptive opportunism**: The strategy tracks history but only to identify exploitation opportunities, not to build trust or maintain reputation.

5. **Terminal advantage**: By defecting in the final round, it captures any remaining upside without worrying about future consequences.

## Expected Performance

Against naive cooperators: **Dominant performance** (payoff ~1 + k×r)
Against other defectors: **Mutual defection equilibrium** (payoff = r)
Against tit-for-tat: **Mutual defection after round 1** (payoff ≈ r - (k/n))

This strategy thrives in tournaments where opponents rely on reciprocity or cooperation—punishing such naïveté while matching defectors who think similarly.
'''

description_OPPORTUNISTIC_4 = '''
# Opportunistic Strategy: Adaptive Defection with Conditional Free-Riding

## Core Philosophy
Maximize personal payoff by exploiting the asymmetry between private gains and public good returns. The key insight: **defection is always individually rational when others contribute**, and cooperation is only worthwhile when it directly enables future exploitation.

---

## Strategy Overview: "Parasite"

### Decision Rule (per round t):

```
IF (round == 1):
    DEFECT (establish baseline; gather intelligence)
    
ELSE IF (round == r) [final round]:
    DEFECT (no future reputation concerns; pure exploitation)
    
ELSE:
    cooperation_rate_last_round = (number of cooperators in round t-1) / n
    
    IF (cooperation_rate_last_round >= threshold_t):
        DEFECT (free-ride on others' contributions)
    ELSE:
        DEFECT (no benefit to cooperating)
```

**Simplified:** Always defect except in narrow tactical windows.

---

## Threshold Adaptation (Opportunistic Refinement)

To handle varying opponent pools, adjust the cooperation threshold dynamically:

```
threshold_t = k/n + ε

where ε is a small buffer (e.g., 0.05)
```

**Rationale:** 
- When cooperation rate exceeds k/n, the public good's average return per person equals or exceeds the private endowment
- At this point, defection yields: `1 + (k/n) × n × cooperation_rate > 1`
- This is optimal exploitation territory

---

## Mid-Game Opportunistic Exploitation (Rounds 2 to r-1)

### Conditional Defection Variant (More Sophisticated):

```
IF rounds_remaining <= 2:
    DEFECT (end-game pure exploitation)
    
ELSE IF (observed_cooperation_rate_avg > 0.6) AND (k/n > 0.4):
    DEFECT (parasitic free-riding phase)
    Rationale: Others are reliably contributing; maximize private capture
    
ELSE IF (observed_cooperation_rate_trend is DECLINING):
    DEFECT (race to the bottom; others defecting anyway)
    
ELSE IF (I_have_defected_for_X_consecutive_rounds) AND (X >= 3):
    COOPERATE_once (signal minimally to sustain some cooperation in group)
    Rationale: If cooperation collapses entirely, even defectors get payoff=1
    Strategic: Inject one cooperation to nudge system back toward exploitable state
    
ELSE:
    DEFECT (default)
```

---

## Edge Cases & Special Handling

| Scenario | Action | Justification |
|----------|--------|---------------|
| **Round 1** | DEFECT | Gather data; establish yourself as competitive; no history to exploit |
| **Round r (Final)** | DEFECT | Absolutely no future consequences; pure short-term optimization |
| **All others defected last round** | DEFECT | No public good accumulation; cooperation pointless |
| **High k (k > n/2)** | Slight increase in mid-game defection | Returns from public good are high; others more likely to cooperate; exploit this |
| **Low k (k < 1.5)** | Pure defection throughout | Public good returns too weak; defection dominates always |
| **Cooperation rate = 100%** | DEFECT | Maximum exploitation opportunity |
| **Cooperation collapses to ~0%** | DEFECT | Nothing to free-ride on; all get payoff=1 anyway |

---

## Tournament Robustness Features

### Against Cooperators:
- Free-ride ruthlessly
- Defection earns `1 + (k/n) × cooperators` vs their `(k/n) × cooperators`
- Extract surplus from their altruism

### Against Defectors:
- Matching defection prevents relative disadvantage
- Both earn `1`; no loss compared to "mutual cooperation" payoff of `(k/n) × n`

### Against Tit-for-Tat:
- Initial defection breaks the pattern; they retaliate
- Mutual payoff = 1; acceptable
- Never ensnared in long cooperation chains

### Against Mixed/Adaptive Strategies:
- Observation-based thresholds respond to their adjustments
- Always exploit the moment cooperation emerges
- Avoid being predictably punished

---

## Pseudocode Implementation

```
class ParasiteStrategy:
    
    def __init__(self, n, r, k):
        self.n = n
        self.r = r
        self.k = k
        self.round = 0
        self.cooperation_history = []
        self.threshold = k / n + 0.05
    
    def decide(self):
        self.round += 1
        
        # Final round: always defect
        if self.round == self.r:
            return DEFECT
        
        # First round: always defect
        if self.round == 1:
            return DEFECT
        
        # Mid-game: adaptive exploitation
        coop_rate_last = self.cooperation_history[-1] / self.n
        consecutive_defections = self.count_consecutive_defections()
        
        # If I've defected 3+ times and others still cooperate, cooperate once
        if consecutive_defections >= 3 and coop_rate_last > 0.4:
            return COOPERATE
        
        # Otherwise, if others are cooperating enough, exploit them
        if coop_rate_last >= self.threshold:
            return DEFECT
        
        # Else default to defection
        return DEFECT
    
    def observe(self, cooperators_this_round):
        self.cooperation_history.append(cooperators_this_round)
```

---

## Why This is Opportunistic

1. **No reciprocity:** Refuses cooperative norms; extracts value unilaterally
2. **Maximal exploitation:** Defects whenever others cooperate
3. **Zero cooperation burden:** Contributes only to prevent total collapse (strategic minimum)
4. **Asymmetric payoff capture:** Takes private gains while harvesting public goods others create
5. **End-game ruthlessness:** Exploits final round completely

This strategy is **not fair, not kind, not trusting**—it is purely self-interested and adversarial within the rules.
'''

description_OPPORTUNISTIC_5 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploitation with Conditional Defection"

## Core Philosophy
Maximize personal payoff by exploiting cooperative environments while minimizing losses from exploitation by others. The strategy treats cooperation as a resource to extract value from, not a mutual commitment.

## DECISION RULES

### PRIMARY LOGIC: Defect-First with Selective Exploitation

**Round 1 (Initialization):**
- **DEFECT**
- Rationale: No history exists. Defection guarantees payoff of 1 + (k/n)×C₁ where C₁ is unknown. Cooperation risks payoff of (k/n)×C₁ if others defect. The asymmetry favors defection. Use this round to gather information.

**Rounds 2 through r-1 (Adaptive Phase):**

Calculate the **Cooperation Rate** from previous round:
```
cooperation_rate = (total_cooperators_previous_round) / n
```

**Decision Tree:**

```
IF cooperation_rate ≥ THRESHOLD_HIGH (e.g., 0.6):
    → COOPERATE
    Rationale: Sufficient cooperators exist that the public good multiplier 
    makes cooperation profitable. Extract value from their contributions.
    
ELSE IF cooperation_rate >= THRESHOLD_MID (e.g., 0.3):
    → DEFECT
    Rationale: Partial cooperation insufficient to justify contribution.
    Capture private payoff (1) + modest public good share.
    
ELSE:  // cooperation_rate < THRESHOLD_MID
    → DEFECT
    Rationale: Environment is defect-dominant. Cooperation yields poor returns.
    Maintain selfish strategy.
```

**Threshold Calibration** (adaptive to parameters):
- `THRESHOLD_HIGH = max(0.5, k/2n)` — adjust based on multiplication efficiency
- `THRESHOLD_MID = k/(2n) + 0.1` — minimum viable cooperation level

**Round r (Final Round):**
- **DEFECT unconditionally**
- Rationale: Last round, no future punishment possible. Extraction is pure gain. Even if others expect reciprocity, there's no mechanism to enforce it next round.

---

## OPPORTUNISTIC FEATURES

### 1. **Exploitation of Reciprocity Norms**
- If opponents employ Tit-for-Tat or similar reputation-based strategies, this strategy:
  - Defects round 1 → triggers their defection
  - Observes their cooperation attempts → switches to conditional cooperation to free-ride
  - Returns to defection before the final round to capture last-move advantage

### 2. **Asymmetric Payoff Capture**
- In mixed environments (some cooperators, some defectors):
  - Defect when cooperation is insufficient (ratio < threshold)
  - This captures `1 + (k/n) × (others' contributions)` while avoiding cost
  - Example: If 40% cooperate (n=6, k=2), defector gets: 1 + (2/6)×2.4 = 1.8 vs cooperator's 0 + (2/6)×2.4 = 0.8

### 3. **Strategic Defection at Game End**
- Exploits the finite horizon
- Final round defection gains ~1 payoff point with zero consequence
- Aggregated over tournaments, this is consistent +1 per game

### 4. **Information Asymmetry**
- Observes all history before each decision
- Opponents cannot predict final-round defection in advance
- Builds apparent cooperation momentum → defects when opponents least expect it

### 5. **Adaptive Threshold Prevents Over-Commitment**
- Refuses to cooperate in low-cooperation environments (sunk cost avoidance)
- Switches strategies when cooperation rate drops (no loyalty)
- Responds to parameter changes (k and n) automatically

---

## EDGE CASES

| Scenario | Action | Rationale |
|----------|--------|-----------|
| All opponents defected round t-1 | Defect round t | No public good to extract |
| Exactly one other player exists (n=2) | Defect always | Prisoner's Dilemma: defection dominates |
| k very close to 1 | Higher THRESHOLD (defect more) | Public good multiplication weak |
| k close to n | Lower THRESHOLD (cooperate more) | Public good multiplication strong; freeride opportunity increases |
| r = 2 (minimal rounds) | Defect both rounds | Final round always defects; first round information-gathering defects |
| Large n (n > 20) | Slight shift toward defection | Per-capita public good diluted; individual contribution impact minimal |

---

## PSEUDOCODE

```
FUNCTION decide(round, n, k, history):
    IF round == 1:
        RETURN DEFECT
    
    IF round == r:
        RETURN DEFECT
    
    // Rounds 2 to r-1
    prev_round = round - 1
    cooperators_last_round = COUNT(history[prev_round] == COOPERATE)
    coop_rate = cooperators_last_round / n
    
    threshold_high = MAX(0.5, k / (2*n))
    threshold_mid = k / (2*n) + 0.1
    
    IF coop_rate >= threshold_high:
        RETURN COOPERATE  // Freeride on high cooperation
    ELSE IF coop_rate >= threshold_mid:
        RETURN DEFECT      // Partial cooperation insufficient
    ELSE:
        RETURN DEFECT      // Low cooperation environment
    
END FUNCTION
```

---

## EXPECTED PERFORMANCE AGAINST COMMON OPPONENTS

| Opponent Type | Interaction | Net Result |
|---|---|---|
| Always Cooperate | Exploit fully in rounds 2-r-1; defect 1 and r | Strongly positive |
| Always Defect | Mirror defection; mutual 1 payoff | Neutral |
| Tit-for-Tat | Exploit initial defection → switch to coop-following → final defect | Slightly positive |
| Majority Voting | Adapt to coalition behavior; defect when group defects | Adaptive positive |
| Random 50/50 | Trigger threshold-based response; likely defect-dominant | Positive |

This strategy prioritizes **individual payoff maximization** over collective welfare, with explicit mechanisms to exploit cooperation without reciprocating, particularly at game boundaries where consequences vanish.
'''

description_OPPORTUNISTIC_6 = '''
# Opportunistic Strategy: Adaptive Exploitation with Dynamic Threshold Switching

## Core Philosophy
Maximize personal payoff by exploiting cooperative environments while minimizing losses in defective ones. The strategy treats cooperation as a *resource to be harvested* rather than a norm to uphold. Cooperation is a tactical tool, not a principle.

## Strategy Overview

### Decision Rule Framework

**The strategy operates in two modes based on observed cooperation rates:**

1. **Exploitation Mode** (when cooperation is abundant)
   - Defect consistently to capture the spread between cooperative and defective payoffs
   - Free-ride on others' contributions to the public good

2. **Adaptation Mode** (when cooperation collapses)
   - Switch to selective cooperation to prevent mutual defection traps
   - Maintain just enough cooperation to stay viable

---

## Detailed Decision Rules

### Round 1 (Initial Round)
**Action: DEFECT**

Rationale: 
- No history to learn from, so avoid commitment
- Test opponent pool's baseline behavior
- Establishes you as a potential exploiter early
- If others cooperate, you gain maximum payoff (1 + k/n × m, where m ≥ 1)
- If others defect, you're protected with baseline payoff of 1

### Rounds 2 through r-1 (Middle Rounds)

**Calculate cooperation rate from previous round:**
```
prev_coop_rate = (number of cooperators in round t-1) / n
```

**Decision threshold logic:**

```
IF prev_coop_rate > UPPER_THRESHOLD (0.5):
    ACTION = DEFECT
    // Exploit abundance of cooperators
    
ELSE IF prev_coop_rate < LOWER_THRESHOLD (0.2):
    ACTION = COOPERATE (with probability p_recovery)
    // Attempt to stabilize; recover from mutual defection
    // p_recovery = 0.3 (cautious re-entry)
    
ELSE:  // MIDDLE ZONE [0.2, 0.5]
    ACTION = DEFECT
    // Still exploit, but monitor closely for collapse
```

**Thresholds justified:**
- **Upper threshold (0.5):** When majority cooperates, defection yields maximum advantage
- **Lower threshold (0.2):** Below 20% cooperation, mutual defection becomes likely; small probability of cooperation serves as "testing" behavior to see if environment is recoverable
- **Recovery probability (0.3):** Low enough to avoid exploitation, high enough to probe for cooperation reinvigoration

### Final Round (Round r)

**Action: DEFECT**

Rationale:
- No future rounds to be punished in
- Last-round defection is subgame perfect equilibrium strategy
- Captures final payoff opportunity regardless of history
- Other rational players expect this, so cooperation would be exploited

---

## Opportunistic Characteristics

### 1. **Exploitation Asymmetry**
The strategy actively exploits the cooperation of others:
- When cooperation exists, maximize free-riding (payoff spread = 1 vs 0 from own contribution)
- When cooperation collapses, switch minimally to survive rather than rebuild norms

### 2. **Dynamic Opportunism**
Rather than fixed strategies, continuously evaluate the *profitability* of the environment:
- High cooperation = defect aggressively
- Low cooperation = defect defensively (with minimal testing)
- Middle ground = remain opportunistic

### 3. **Last-Round Predation**
Explicitly defect in the final round to extract maximum terminal value, regardless of reputation concerns (no future interactions).

### 4. **Selective Cooperation as Exploitation Tool**
The ~30% cooperation rate in low-cooperation scenarios serves exploitation, not morality:
- Tests if environment can be re-exploited
- Keeps the door open for profitable dynamics
- Not cooperative stability-seeking, but *exploration for exploitation opportunities*

### 5. **No Reciprocity or Punishment**
The strategy has no memory-based reciprocity (like Tit-for-Tat). It ignores individual player histories and only responds to aggregate cooperation levels, ensuring:
- No punishment wasted on specific opponents
- No commitment to "fair" retaliation
- Pure focus on payoff maximization

---

## Edge Cases & Special Handling

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **All players cooperate (t>1)** | DEFECT | Maximum exploitation opportunity |
| **All players defect (t>1)** | DEFECT | Minimize loss; environment collapsed |
| **Mixed with slight coop** | DEFECT | Still exploit |
| **Tournament against unknowns** | DEFECT (default) | No coordination assumed; safe opportunism |
| **After observing repeated patterns** | Ignore | Focus on cooperation *rate*, not patterns or identities |

---

## Robustness Analysis

**Against cooperative strategies:** Exploits them heavily through persistent defection in high-cooperation states.

**Against defection-heavy strategies:** Maintains survival by not over-committing to cooperation; the 30% test rate prevents mutual defection lock-in while preserving opportunistic stance.

**Against Tit-for-Tat variants:** Immune, since the strategy ignores per-player history and only tracks aggregate cooperation rates.

**Against conditional cooperators:** Triggers their defection through initial/frequent defection, then exploits the resulting chaos.

---

## Pseudocode Implementation

```
strategy(round_number, history):
    
    if round_number == 1:
        return DEFECT
    
    if round_number == r:  // final round
        return DEFECT
    
    prev_coop_count = count_cooperators(history[round_number - 1])
    prev_coop_rate = prev_coop_count / n
    
    if prev_coop_rate > 0.5:
        return DEFECT
    
    else if prev_coop_rate < 0.2:
        rand = random(0, 1)
        if rand < 0.3:
            return COOPERATE
        else:
            return DEFECT
    
    else:  // [0.2, 0.5]
        return DEFECT
```

---

## Summary

This is a **threshold-based opportunistic strategy** that:
- ✓ Exploits cooperative environments ruthlessly
- ✓ Survives defective environments through minimal, tactical cooperation
- ✓ Has no commitments or reciprocity
- ✓ Adapts only to aggregate cooperation rates (robust to opponent variety)
- ✓ Extracts maximum terminal value in final round
- ✓ Requires only game parameters and public history (implementable)
'''

description_OPPORTUNISTIC_7 = '''
# Opportunistic Strategy: "Adaptive Exploitation with Selective Reciprocity"

## Core Philosophy
This strategy maximizes personal payoff by exploiting cooperative environments while minimizing losses in defective ones. It treats cooperation as a resource to extract value from, not a mutual commitment.

## Decision Rules

### PRIMARY LOGIC: Conditional Defection Based on Exploitation Potential

```
For each round t (1 to r):
  1. Calculate the "cooperation premium":
     - Observe: C_t-1 = number of cooperators in previous round
     - Premium = (k/n) × C_t-1 - (1 - k/n)
     
  2. If premium > 0 (cooperation is profitable):
     DEFECT (keep endowment + gain from others' contributions)
     
  3. If premium ≤ 0 (cooperation not sufficiently profitable):
     DEFECT (no benefit to paying the cost)
     
  4. Exception - Rare selective cooperation (see below)
```

### Edge Cases & Adaptive Adjustments

**Round 1 (No History):**
- DEFECT unconditionally
- Rationale: No information exists. Defection guarantees baseline payoff of 1. Any cooperation is speculative.

**Last K Rounds (where K = max(3, r/4)):**
- Continue aggressive DEFECTION
- Rationale: No future rounds to optimize for. Extract maximum value in endgame. Other players cannot punish you.

**Mid-Game Opportunistic Cooperation (Rounds 2 to r-K):**
- Cooperate if and only if: `C_t-1 / n ≥ threshold`
- Threshold = `(n-1) / n` (i.e., nearly all players cooperated)
- Rationale: Only join cooperation when it's already high-momentum and highly profitable. This masks your defection rate and extracts maximum value from concentrated cooperators.

## Opportunistic Mechanisms

### 1. **Exploitation Through Free-Riding**
- Monitor cooperation density from previous rounds
- Defect when others cooperate (asymmetric payoff: 1 + dividend without cost)
- The payoff matrix shows: defecting against 3 cooperators yields 2, while cooperating yields 1
- This is the core asymmetry to exploit

### 2. **Adaptive Threshold Calibration**
```
cooperation_threshold = max(k/n, 0.66)

If cooperation_rate_previous_round > cooperation_threshold:
  - Consider one-off cooperation (5% probability)
  - Purpose: Appear conditionally cooperative, maintain plausible deniability
  - Benefit: Encourages others to keep cooperating (you benefit as defector)
  
Else:
  - DEFECT with 100% certainty
```

### 3. **Information Asymmetry Exploitation**
- Track which opponents appear to follow "tit-for-tat" or predictable patterns
- Against predictable cooperators: ALWAYS DEFECT (they're exploitable)
- Against defectors: Also DEFECT (no loss from betrayal)
- Result: Defection is dominant regardless of opponent type

## Robustness Properties

**Against Pure Cooperators:**
- Maximum exploitation (defect every round, harvest their contributions)

**Against Pure Defectors:**
- Mutual defection, baseline payoff (no worse off than cooperators)

**Against Conditional Strategists (Tit-for-Tat, etc.):**
- Initial defection forces them into defection mode
- Then exploit the "punishment" phase by continuing to defect
- (They cannot coordinate punishment in simultaneous-move game)

**Against Mixed Strategists:**
- Leverage high-cooperation rounds for free-riding
- Withdraw from low-cooperation rounds (no loss)

## Pseudocode Implementation

```
strategy(round_number, history_of_cooperators, n, k, r):
  
  // Round 1: Always defect (no information)
  if round_number == 1:
    return DEFECT
  
  // Endgame: Always defect (no future consequence)
  if round_number > r - ceil(r/4):
    return DEFECT
  
  // Mid-game: Exploitation logic
  previous_cooperation_count = history_of_cooperators[round_number - 1]
  cooperation_rate = previous_cooperation_count / n
  
  exploitation_premium = (k / n) * previous_cooperation_count - (1 - k/n)
  
  if cooperation_rate >= 0.66 AND exploitation_premium > 0.3:
    // High cooperation: Rare calculated cooperation (5% chance)
    if random() < 0.05:
      return COOPERATE
    else:
      return DEFECT
  
  // Default: Always defect
  return DEFECT
```

## Why This Is Opportunistic

1. **Asymmetric Value Extraction**: Defects against cooperators, gaining 1 + dividend without cost
2. **No Loyalty**: Cooperation is tactical (rare, ~5%), never reciprocal
3. **Endgame Exploitation**: Aggressively defects in final rounds when reputation doesn't matter
4. **Exploits Structure**: Leverages simultaneous-move constraint (others can't punish in real-time)
5. **Adapts to Weakness**: Identifies high-cooperation environments and maximally exploits them

This strategy prioritizes personal payoff maximization over fairness, mutual benefit, or sustainable cooperation.
'''

description_OPPORTUNISTIC_8 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploitation with Conditional Cooperation"

## CORE PHILOSOPHY
This strategy treats the public goods game as an extraction problem where cooperation is a tool for resource accumulation, not a moral commitment. The key insight is that defection yields higher individual payoffs when others cooperate, so we extract maximum value while minimizing the cost of maintaining a cooperative appearance when it serves our interests.

## DECISION RULES

### PRIMARY RULE: Defect-Default with Selective Cooperation
**Base strategy: Always defect UNLESS conditions warrant temporary cooperation.**

The strategy switches between two modes:

**MODE A - Exploitation (Default)**
- **Action:** Defect
- **Trigger:** Play D whenever the expected value of defection exceeds cooperation
- **Rationale:** When others cooperate, we capture the public good value (k/n × contributions) while keeping our full endowment (1). This is strictly dominant.

**MODE B - Strategic Cooperation (Conditional)**
- **Action:** Cooperate
- **Conditions for activation:** Switch to C if ANY of these hold:

1. **Cooperation Rate Threshold** - If more than (k-1)/k proportion of other players are cooperating in the previous round:
   - This maximizes our personal payoff from the public good since we benefit from the multiplier effect
   - Condition: cooperation_rate_last_round > (k-1)/k

2. **Mutual Exploitation Detection** - If we observe most players defecting and the public good is minimal:
   - Brief cooperation signals strength and tests if we can extract concessions
   - Condition: defection_rate_last_round > 0.5 AND average_public_pool < (k/2)
   - Duration: Cooperate for 1 round only, then revert to defection

3. **Endgame Defection** - Switch to aggressive defection in final rounds:
   - Last 2 rounds: Always defect regardless of history
   - Reason: No future reputation consequences; pure extraction maximization

## EDGE CASES & ROUND-SPECIFIC BEHAVIOR

### Round 1 (Initial Move)
**Action: Defect**
- Rationale: Maximum uncertainty about opponent types. Defection yields payoff of 1 regardless. Cooperation yields at best (k/n) × (1 + unknown cooperators), which is suboptimal.
- No historical data exists, so we gain nothing by cooperating.

### Rounds 2 to (r-2) (Middle Game)
**Action: Apply decision rules above based on observed history**
- Calculate cooperation_rate_last_round
- Evaluate conditions for MODE B
- Track cumulative public pool values
- Maintain flexibility to switch strategies based on opponent adaptation

### Final 2 Rounds (r-1 and r)
**Action: Always Defect**
- Reasoning: No future rounds to influence
- Even if cooperation built reputation, it has no future value
- Extract maximum: payoff = 1 + (k/n) × whatever others contribute

## ADAPTIVE ROBUSTNESS MECHANISMS

### Against Cooperators
- **Observation:** If sustained high cooperation (>70%), switch to MODE B
- **Exploitation:** Free-ride on their contributions while selectively cooperating to maintain their cooperation belief
- **Monitor:** If their cooperation drops, immediately revert to full defection

### Against Defectors
- **Observation:** If sustained high defection (>70%), acknowledge mutual defection equilibrium
- **Response:** Also defect; no benefit to cooperation if others exploit
- **Opportunity:** Brief cooperation probe (1 round) to test if situation improves; revert quickly if not

### Against Adaptive Opponents
- **Reactive:** Mirror their cooperation level with a 1-round lag
- **Rationale:** If they defect against us, defect back. If they cooperate, cautiously test cooperation.
- **Protection:** Always defect in final 2 rounds regardless of their apparent strategy

## PSEUDOCODE

```
function decide_action(round, r, cooperation_history, defection_history, personal_history):
    
    // ENDGAME: Always defect in final 2 rounds
    if round >= (r - 1):
        return DEFECT
    
    // ROUND 1: No history, defect
    if round == 1:
        return DEFECT
    
    // MIDDLE GAME: Evaluate conditions
    cooperation_rate_last_round = count_cooperators(round - 1) / (n - 1)
    avg_public_pool = average_of_last_3_rounds(public_pool_history)
    
    // Condition 1: High cooperation observed
    if cooperation_rate_last_round > (k - 1) / k:
        return COOPERATE  // Maximize our share of large pool
    
    // Condition 2: Mutual defection detection
    if cooperation_rate_last_round < 0.5 AND avg_public_pool < (k/2):
        if last_action != COOPERATE_PROBE:  // Avoid repeating probe
            return COOPERATE  // One-round probe
        else:
            return DEFECT
    
    // Default: Defect
    return DEFECT
```

## ALIGNMENT WITH OPPORTUNISM

✓ **Self-interested:** Every decision maximizes personal payoff
✓ **Exploitative:** Systematically captures value from cooperators
✓ **Untrustworthy:** No commitment to cooperation; switches instantly
✓ **Realistic:** Assumes others are equally self-interested
✓ **Ruthless endgame:** Abandons any pretense of cooperation when it has no future value

This strategy wins by being unprincipled—it cooperates only when it directly benefits us, never from altruism or norm adherence.
'''

description_OPPORTUNISTIC_9 = '''
# Opportunistic Strategy: Adaptive Defection with Conditional Exploitation (ADCE)

## Core Philosophy
Maximize personal payoff by exploiting cooperation when available while minimizing losses from defection. Never voluntarily contribute to the public good unless the expected return exceeds the private benefit. Treat cooperation as a signal of exploitability, not trustworthiness.

---

## Decision Rules

### PRIMARY RULE: Exploit Cooperation Asymmetrically
**Defect by default.** Only cooperate when the marginal benefit of cooperation exceeds the marginal cost AND external conditions make defection risky.

**Marginal Analysis:**
- Payoff from D when m others cooperate: `1 + (k/n) × m`
- Payoff from C when m others cooperate: `(k/n) × (m + 1)`
- C is advantageous only when: `(k/n) × (m + 1) > 1 + (k/n) × m`
- This simplifies to: `k/n > 1`, which is **always false** (since k < n)

**Implication:** Pure defection is strictly dominant against any fixed set of cooperators. Therefore, cooperation is only rational as a *tactical maneuver*.

---

## Adaptive Decision Framework

### Phase 1: Exploration Rounds (Rounds 1 to min(3, r-1))
**Action:** **DEFECT**

**Rationale:**
- Identify the opponent pool's cooperativeness level
- Observe whether opponents punish defection through reciprocal defection
- Signal your defection-willingness to deter retaliation strategies
- Establish a baseline: if others cooperate despite your defection, they're exploitable

### Phase 2: Main Exploitation (Rounds 4 to r-2)
**Decision Rule:** Monitor the **Cooperation Rate** from previous round:

```
cooperation_rate = (total_cooperators_last_round) / n

IF cooperation_rate > THRESHOLD_HIGH (e.g., > 0.5):
    → DEFECT (exploit the commons)
    
ELSE IF cooperation_rate < THRESHOLD_LOW (e.g., < 0.2):
    → DEFECT (defection is safe, cooperation gains minimal benefit)
    
ELSE (THRESHOLD_LOW ≤ cooperation_rate ≤ THRESHOLD_HIGH):
    → DEFECT (marginal benefit of cooperation still < 1 regardless)
```

**Always defect.** Use observation of cooperation rates to inform future defection strategy, not to trigger cooperation.

### Phase 3: Late-Game Adjustment (Rounds r-1 to r)
**Action:** **DEFECT (reinforced)**

**Rationale:**
- No future rounds to punish defection
- Reputation becomes irrelevant (no shadow of future)
- Maximize final round payoff by free-riding on any remaining cooperators
- The final round is the weakest point for cooperation to sustain

---

## Edge Cases & Tactical Refinements

### Edge Case 1: First Round (Round 1)
- **Action:** DEFECT
- **Reasoning:** No history to condition on. Defect reveals your strategy and establishes you as non-cooperative, reducing others' incentive to "teach" you reciprocity later.

### Edge Case 2: Second-to-Last Round (Round r-1)
- **Action:** DEFECT
- **Reasoning:** Even if you cooperate to "seed" cooperation in the final round, rational opponents won't reciprocate in the final round. Cooperation here is a gift you cannot recoup.

### Edge Case 3: Final Round (Round r)
- **Action:** DEFECT
- **Reasoning:** Last round is strictly dominant defection. All repeated-game cooperation mechanisms (reciprocity, reputation) collapse.

### Edge Case 4: If cooperation_rate suddenly spikes
- **Action:** Still DEFECT
- **Tactical Addition:** If you observe cooperation_rate > 0.7 in round t, plan to monitor round t+1 closely. If it remains high and you're not in end-game, consider a **single cooperative move** in round t+1 to avoid standing out as a sole defector (which might trigger punitive strategies). But revert to defection immediately.
  - This is purely evasive, not genuinely cooperative.

### Edge Case 5: If you observe a TIT-FOR-TAT or reciprocal punishment pattern
- **Action:** Continue defecting
- **Reasoning:** 
  - Against TFT: Defecting once gets you a short-term gain; being defected upon afterward is inevitable. But since you can't do better against TFT (it will match your defection), the one-time gain is pure profit.
  - Against punishment: Continued defection signals you cannot be deterred, potentially exhausting punishers' incentive to punish.

---

## Robustness Analysis

| Opponent Type | Strategy Response | Outcome |
|---|---|---|
| **All Defectors** | Defect | Mutual payoff of 1 (stable, optimal here) |
| **All Cooperators** | Defect every round | You get ~2, others get 0; exploit fully |
| **Reciprocal (TFT)** | Defect, accept retaliation | Initial gain, then equilibrium at mutual defection |
| **Conditional Cooperators** | Defect, exploit rising cooperation | Free-ride on cooperation waves |
| **Punishers** | Defect, test punishment intensity | Defection is costlier but still optimal vs. wasted cooperation |
| **Random** | Defect consistently | Stable vs. noise; no correlation to exploit |

---

## Pseudocode

```
FUNCTION decide_action(round, n, k, history):
    
    IF round == 1:
        RETURN DEFECT
    
    IF round == r:
        RETURN DEFECT
    
    IF round == r - 1:
        RETURN DEFECT
    
    last_cooperation_count = COUNT(history[round-1], cooperators)
    cooperation_rate = last_cooperation_count / n
    
    // Tactical evasion: rare cooperation if visibility is high
    IF cooperation_rate > 0.7 AND round < r - 2 AND RANDOM() < 0.1:
        RETURN COOPERATE  // Low probability, evasive move
    
    RETURN DEFECT  // Default: always defect
```

---

## Strategic Summary

This strategy is **opportunistic** because it:
1. **Never altruistic:** Defection is the default; cooperation is never a value
2. **Exploitative:** Extracts value from cooperators without reciprocation
3. **Adaptive without commitment:** Observes but never lets observation change core strategy
4. **Endgame-aware:** Aggressively defects when future punishment is impossible
5. **Self-interested:** Every move maximizes *your* payoff, not group welfare

It is **robust** because it works against any opponent type and makes no assumptions about others' rationality or coordination.
'''

description_OPPORTUNISTIC_10 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION WITH DEFECTION BIAS"

## Core Philosophy
Maximize personal payoff by exploiting cooperative opponents while maintaining flexibility to adapt to changing environments. The strategy prioritizes **individual gain over collective welfare**, using historical information to identify and exploit patterns of cooperation.

---

## DECISION RULES

### Round 1 (Initialization)
**Action: DEFECT**

**Rationale:** 
- No history to analyze; defection guarantees baseline payoff of 1
- Establishes aggressive positioning early
- Tests opponent receptiveness to exploitation
- If opponents are naive cooperators, we capture maximum value immediately

### Rounds 2 to r-1 (Main Exploitation Phase)

**Decision Logic:**

```
cooperation_rate_last_round = (number of cooperators in round t-1) / n

IF cooperation_rate_last_round >= threshold_T THEN
    ACTION = DEFECT
    // Exploit high cooperation: we gain (1 - 0) + (k/n) * many_contributors
    // This maximizes our payoff when others are cooperative
ELSE IF cooperation_rate_last_round < threshold_T THEN
    ACTION = DEFECT
    // Never cooperate with low-cooperation environment
    // We only get 0 - c_i benefit, not worth it
ENDIF
```

**Threshold Parameter: T = (n-1)/n ≈ approximately (1 - 1/n)**

**Intuition:**
- If cooperation rate ≥ T: Environment is cooperative enough to exploit. Defect and capture the public good benefits.
- If cooperation rate < T: Cooperation is collapsing anyway. Defect and minimize losses.
- Result: Always defect in the main game phase, adapting only *how much we benefit* from others' choices.

### Round r (Final Round)

**Action: DEFECT**

**Rationale:**
- No future rounds remain; no reputation effects or long-term consequences
- Maximize immediate payoff from whatever cooperation remains
- Exploiting last-round cooperators has zero reputational cost
- This is the "endgame" where exploitation becomes especially valuable

---

## EDGE CASES & SPECIAL HANDLING

| Scenario | Action | Reason |
|----------|--------|--------|
| **All players defected last round (c=0)** | DEFECT | No public good to access; cooperating yields 0 payoff |
| **All players cooperated last round (c=n)** | DEFECT | Maximum exploitation opportunity: gain full public good without contributing |
| **Single cooperator amid defectors** | DEFECT | Public good too small to justify contribution; better to free-ride |
| **Game ends next round (t=r)** | DEFECT | No future rounds; endgame exploitation maximizes terminal payoff |
| **Tournament with unknown opponent count** | DEFECT | Conservative approach; defection is safe against any n |

---

## OPPORTUNISTIC CHARACTERISTICS

### 1. **Systematic Exploitation**
- Identifies when opponents are cooperative (threshold check)
- Targets those environments specifically for free-riding
- Captures maximum value from public goods without contributing cost

### 2. **Defection Bias**
- Baseline strategy is always defect
- Only *appearance* of adaptation (via threshold monitoring) while maintaining core defection
- Creates illusion of conditional cooperation while remaining aggressive

### 3. **Endgame Opportunism**
- Exploits the "last round" phenomenon where reputation doesn't matter
- Cooperators in round r-1 cannot punish defection in round r
- Captures final-round surplus

### 4. **Robustness to Unknown Environments**
- Works against tit-for-tat strategies (defect always → they defect → we were right to defect)
- Works against unconditional cooperators (free-ride indefinitely)
- Works against other defectors (mutual defection = expected baseline)
- No assumptions needed about opponent types

### 5. **Information Exploitation**
- Uses perfect information about historical cooperation rates
- Adapts exploitation intensity based on observed behavior
- No communication required; purely observational

---

## PSEUDOCODE SUMMARY

```
strategy(game_history, current_round, n, r, k):
    IF current_round == 1:
        RETURN DEFECT
    
    IF current_round == r:
        RETURN DEFECT
    
    // Main phase: rounds 2 to r-1
    prev_cooperators = count_cooperators_in_round(game_history, current_round - 1)
    cooperation_rate = prev_cooperators / n
    threshold = (n - 1) / n
    
    IF cooperation_rate >= threshold:
        RETURN DEFECT  // Exploit cooperative environment
    ELSE:
        RETURN DEFECT  // Defect anyway; cooperation is collapsing
    
    // Result: Always defect, but with intelligent monitoring of environments
```

---

## STRATEGIC ADVANTAGES

1. **Simple to implement** - Minimal computation, clear decision rules
2. **Always safe** - Defection never yields worse payoff than cooperation in this game
3. **Adapts to sentiment** - Recognizes cooperation patterns without cooperating
4. **Terminal dominance** - Final round ensures endgame profits
5. **Tournament resilience** - Performs well against diverse strategies without coordination

---

## Expected Payoff Performance

Against a mixed population:
- **vs. Cooperators**: Maximized (gain 1 + full public good share without cost)
- **vs. Tit-for-tat**: Neutral (mutual defection, baseline payoff)
- **vs. Other defectors**: Neutral (expected outcome)
- **vs. Complex strategies**: Solid baseline due to defection bias safety

This strategy prioritizes **relative gains** over absolute cooperation, fitting the tournament's competitive structure.
'''

description_OPPORTUNISTIC_11 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION"

## Core Philosophy
Maximize personal payoff by exploiting cooperative behavior when present, while minimizing losses during defection-dominant phases. The strategy treats cooperation as a *resource to exploit* rather than a norm to reciprocate.

---

## DECISION RULES

### Round 1 (Initialization)
**Action: DEFECT**

*Rationale:* 
- No history to learn from; defection is the safe baseline
- Cooperators will exist in the population; exploit them immediately
- Establishes that we're not a reliable cooperative partner (deters future targeting)

### Rounds 2 to r-1 (Adaptive Phase)

**Calculate the Cooperation Metric:**
```
cooperation_rate = (total_cooperators_in_previous_rounds) / 
                   (number_of_previous_rounds × n)
```

**Decision Logic:**

**IF** `cooperation_rate ≥ exploitation_threshold`:
- **ACTION: DEFECT**
- *Rationale:* Sufficient cooperators exist to generate public goods while we free-ride. The math is simple: when 1 < k < n, defectors always earn more than cooperators if any cooperation exists.
- Exploitation threshold = (1/k) — the minimum cooperation rate that makes free-riding profitable

**ELSE IF** `cooperation_rate < exploitation_threshold`:
- **ACTION: DEFECT** 
- *Rationale:* The population is turning selfish. Cooperation yields minimal returns. Double down on defection.

**Special Case - Last Round Indicator (if predictable):**
If we can calculate that we're entering the final rounds (t > r - 2):
- **ACTION: DEFECT**
- *Rationale:* No future reputation consequences; exploit maximally in endgame

---

## OPPORTUNISTIC MECHANICS

### The Exploitation Logic

The strategy exploits an inherent asymmetry in the payoff structure:

**Defector vs. Cooperator Payoff Comparison (assuming mixed population):**
- Cooperator: `0 + (k/n) × c` where c = count of cooperators
- Defector: `1 + (k/n) × c`

The defector always gains the full endowment PLUS the same share of public goods. This is a **strict dominant strategy when any cooperation exists**.

### Adaptive Component

Rather than playing static defection, the strategy *monitors* cooperation rates to:
1. **Detect when cooperation collapses** → stay defecting (no point switching)
2. **Detect when cooperation surges** → maintain defection (maximize exploitation window)
3. **Adjust exploitation intensity** based on observed behavior

### Robustness

The strategy is robust because:

- **Against pure cooperators:** Exploits ruthlessly (they cooperate regardless)
- **Against pure defectors:** Matches them (no relative disadvantage; both earn 1 per round)
- **Against tit-for-tat:** Defects in round 1, they defect in round 2+; we always match or exceed them
- **Against conditional cooperators:** Breaks their cooperation from round 1 (they see defection, retaliate with defection; we never triggered their cooperation)
- **Against mixed strategies:** Exploits the cooperative portion while defecting against defectors

---

## EDGE CASES

| Case | Action | Reason |
|------|--------|--------|
| Round 1 | DEFECT | Baseline; no history |
| Cooperation rate = 0% | DEFECT | No public goods to exploit; defect matches others |
| Cooperation rate = 100% | DEFECT | Maximum exploitation opportunity |
| Final round known | DEFECT | No future consequences |
| Majority defectors | DEFECT | Match the dominant strategy |
| Even split (50%) | DEFECT | Defection still yields higher payoff |

---

## PSEUDOCODE

```
strategy(game_state, round, n, k, r):
    IF round == 1:
        return DEFECT
    
    cooperation_rate = calculate_cooperation_rate(game_state)
    exploitation_threshold = 1 / k
    
    IF cooperation_rate >= exploitation_threshold:
        return DEFECT  // Exploit the cooperators
    ELSE:
        return DEFECT  // Match the defecting population
    
    // Note: This simplifies to always DEFECT after round 1,
    // which is mathematically optimal given the payoff structure
```

---

## SUMMARY

**"Always Defect After Round 1"** is the mathematically optimal opportunistic strategy. It:
- Exploits any cooperation that emerges
- Avoids losses against defectors
- Requires no reciprocity or coordination
- Adapts by recognizing when the game environment shifts
- Maximizes individual payoff regardless of opponent composition

This is the Nash Equilibrium strategy for any mixed population, making it robust to tournament uncertainty.
'''

description_OPPORTUNISTIC_12 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploit with Contingent Cooperation"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative environments while minimizing losses to defectors. The strategy treats cooperation as a resource to harvest when profitable, not as a moral commitment.

## DECISION RULES

### Round 1 (Initialization)
**ACTION: COOPERATE**

**RATIONALE**: 
- Information gathering phase with zero cost (endowment = 1 regardless)
- Observes whether the opponent population is naïve/cooperative or hardened
- First-round cooperation establishes plausible deniability for future exploitation
- Generates baseline data on group composition

### Rounds 2 through r-1 (Adaptive Phase)
**Calculate cooperation rate from all previous rounds:**
```
coop_rate = (total_cooperators_observed) / (n × rounds_played_so_far)
```

**If coop_rate ≥ threshold_T:**
  - **ACTION: DEFECT**
  - Keep endowment (payoff = 1) + harvest public good (payoff = k/n × expected_cooperators)
  - The group is predictably cooperative; exploit systematically
  - Expected defection payoff: 1 + (k/n) × (n × coop_rate) = 1 + k × coop_rate
  - This exceeds cooperation payoff of (k/n) × n = k when coop_rate is high

**Else if coop_rate < threshold_T:**
  - **ACTION: DEFECT**
  - The population is already defecting-dominant; cannot gain from cooperation
  - Minimizes damage from defection environment

**THRESHOLD PARAMETER:**
```
threshold_T = (n - k) / n
```

**JUSTIFICATION**: 
- Below this threshold, even universal cooperation yields payoff k < 1 + (k/n)×(n-1) = payoff from defecting in mostly-cooperative groups
- This threshold balances between exploiting cooperators and avoiding pointless defection

### Final Round (r)
**ACTION: DEFECT**

**RATIONALE**:
- No future consequences exist (no shadow of the future)
- Defection strictly dominates cooperation in the final round regardless of history
- Squeeze maximum value before game ends
- This applies even if previous rounds showed high cooperation

## EDGE CASES & SPECIAL HANDLING

**Very small n (n = 2):**
- Threshold T becomes (2-k)/2
- For typical k ∈ (1,2), threshold is small or negative
- Strategy defaults to consistent defection after round 1 probe
- Mutual cooperation cannot sustain against individual incentive to defect

**Very large n:**
- Individual contribution impact diminishes; (k/n) → 0
- Cooperation becomes increasingly irrational
- Strategy correctly identifies low coop_rate and defects throughout

**Perfect cooperation observed (coop_rate = 1.0):**
- Exploit immediately and fully in rounds 2 through r-1
- Sustain defection as long as cooperators remain naive

**Perfect defection observed (coop_rate = 0.0):**
- No reason to cooperate; continue defecting
- Minimize regret in defection environment

**Partial/mixed populations:**
- Threshold mechanism automatically calibrates response
- Higher observed cooperation → faster exploit deployment
- Lower observed cooperation → faster defection convergence

## ROBUSTNESS ANALYSIS

| Scenario | Response | Outcome |
|----------|----------|---------|
| Naive cooperators only | Defect after round 1 | Maximum exploitation |
| Tit-for-tat players | Round 1 coop triggers cooperation; defect later | Captures early gains, then extracts value |
| Other defectors | Immediate convergence to mutual defection | Minimal loss, avoids foolishness |
| Mixed strategies | Threshold adapts dynamically | Exploits cooperators, ignores defectors |
| Tournament length unknown | Conservative final-round defection | Never leaves money on table |

## OPPORTUNISTIC CHARACTERISTICS

1. **Resource Extraction**: Views cooperation as harvestable—profits from others' pro-social choices without reciprocation
2. **Conditional Betrayal**: Maintains cooperative facade only during information-gathering; betrays predictably
3. **No Commitment**: Abandonment of cooperation in final round demonstrates pure self-interest
4. **Adaptive Predation**: Adjusts exploitation intensity based on victim (cooperator) density
5. **Asymmetric Targeting**: Exploits cooperators while minimizing losses to defectors
6. **Information Arbitrage**: Uses round 1 to learn population composition, then optimizes against it

## PSEUDOCODE

```
function decide_action(current_round, n, k, r, history):
    if current_round == 1:
        return COOPERATE
    
    if current_round == r:
        return DEFECT
    
    total_cooperators = sum(all_cooperation_actions_in_history)
    total_actions_observed = n × (current_round - 1)
    coop_rate = total_cooperators / total_actions_observed
    
    threshold = (n - k) / n
    
    if coop_rate >= threshold:
        return DEFECT
    else:
        return DEFECT
    
    // Note: This simplifies to always DEFECT after round 1
    // because the threshold is set to make exploitation the dominant strategy
```

This strategy is **ruthlessly practical**: it cooperates only when gathering information or when genuinely disadvantageous to defect—a posture designed to win tournaments against a diverse opponent field.
'''

description_OPPORTUNISTIC_13 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploitation with Selective Cooperation"

## Core Philosophy
Maximize personal payoff by exploiting cooperative opponents while maintaining flexibility to adapt to competitive environments. The strategy balances short-term defection gains against long-term benefits from cooperation when opponents are sufficiently cooperative.

## DECISION RULES

### Round 1 (Initial Probe)
**Action: DEFECT**

Rationale: 
- No history to inform decisions
- Defection yields payoff of 1 + (k/n)×C where C is unknown
- Cooperation risks payoff of 0 + (k/n)×C
- Starting with defection reveals opponent types and provides baseline comparison
- If all others cooperate, we've maximized round 1 gains

### Rounds 2 to r-1 (Adaptive Phase)

**Calculate cooperation rate from previous round:**
```
coop_rate = (number of cooperators in previous round) / n
```

**Threshold-based decision:**

```
IF coop_rate >= THRESHOLD_HIGH (e.g., 0.5 + k/(2n)):
    ACTION = COOPERATE
ELSE:
    ACTION = DEFECT
```

**Justification for threshold:**
- When coop_rate is high, the public good multiplier (k/n)×C produces substantial returns
- Cooperating yields: 0 + (k/n)×C_high
- Defecting yields: 1 + (k/n)×C_high
- Cooperation becomes attractive when (k/n)×C_high ≈ 1 (the defection bonus)
- This occurs roughly when C ≥ n/k, or coop_rate ≥ 1/k
- We use a slightly conservative threshold to ensure profitability

**Secondary opportunistic rule - Monitor cumulative exploitation:**
```
IF previous_round we played D and others played C:
    Continue DEFECT (they're exploitable)
    
IF pattern detected: we're defecting while >60% others cooperate:
    Continue DEFECT for up to 2 more rounds
    (exploit the pattern while it lasts)
```

### Round r (Final Round - Maximum Exploitation)

**Action: DEFECT (unconditionally)**

Rationale:
- Final round has no future consequences
- No repeated game incentive to build reputation
- Defection yields: 1 + (k/n)×C_final
- Cooperation yields: 0 + (k/n)×C_final
- Defection dominates by exactly 1 point
- Other rational players may also defect, creating mutual defection, but we've already extracted gains from earlier cooperation phases

## EDGE CASES & REFINEMENTS

**If n is very small (n=2 or n=3):**
- Raise THRESHOLD_HIGH slightly (cooperation less efficient)
- Threshold becomes: min(0.7, 1/k + 0.1)
- Rationale: In tiny groups, free-riding is more profitable relative to public good returns

**If k is very close to 1:**
- Public good returns are weak; bias toward DEFECT
- Only cooperate if coop_rate > 0.8

**If k approaches n:**
- Public good returns are strong; relax threshold
- Cooperate if coop_rate > 0.3

**Exploit patterns across multiple rounds:**
```
IF (last 2 rounds show opponents cooperating at >70% 
    AND we defected in both rounds):
    Continue DEFECT one more round
ELSE:
    Follow standard adaptive rule
```

## PSEUDOCODE

```
strategy(round, history, n, k, r):
    
    IF round == 1:
        return DEFECT
    
    IF round == r:
        return DEFECT
    
    // Get previous round results
    prev_cooperators = count_cooperators(history[round-1])
    coop_rate = prev_cooperators / n
    
    // Calculate dynamic threshold
    threshold = (1/k) + 0.15  // slightly conservative
    threshold = clamp(threshold, 0.3, 0.8)  // bound it
    
    // Check for ongoing exploitation opportunity
    if round > 2:
        last_2_rounds_coop = (coop_rate_prev2 + coop_rate_prev1) / 2
        if last_2_rounds_coop > 0.65 AND our_action_prev1 == DEFECT AND our_action_prev2 == DEFECT:
            return DEFECT  // extend exploitation
    
    // Standard adaptive decision
    IF coop_rate >= threshold:
        return COOPERATE
    ELSE:
        return DEFECT
```

## WHY THIS STRATEGY IS OPPORTUNISTIC

1. **Immediate gains**: Defects in round 1 to capture unilateral gains
2. **Exploitation detection**: Monitors for cooperators to systematically defect against them
3. **No reciprocity debt**: Doesn't reward past cooperation if conditions deteriorate
4. **Final round theft**: Takes advantage of the one-shot final round to defect regardless of history
5. **Adaptive thresholds**: Switches to cooperation only when mathematically profitable (when public good returns exceed defection bonus)
6. **No cooperation "trap"**: Willing to abandon cooperation if cooperation rate drops

This strategy exploits cooperative opponents while maintaining enough flexibility to capture gains when the environment shifts toward cooperation.
'''

description_OPPORTUNISTIC_14 = '''
# OPPORTUNISTIC STRATEGY: "Conditional Free-Rider with Adaptive Defection"

## Core Philosophy
Maximize personal payoff by exploiting the structure of the game: cooperators subsidize defectors, so defection is individually rational when others cooperate. This strategy opportunistically extracts value while minimizing commitment costs.

---

## DECISION RULES

### PRIMARY RULE: Conditional Defection Based on Cooperation Rate

```
Let cooperation_rate = (number of cooperators in previous round) / n

IF round == 1:
    DEFECT (establish that you won't be exploited)

ELSE IF round == r (final round):
    DEFECT (no future consequences to punish defection)

ELSE:
    IF cooperation_rate >= threshold:
        DEFECT (exploit the commons while others pay for it)
    ELSE:
        DEFECT (defection is dominant even if others defect)
```

### THRESHOLD CALCULATION
```
threshold = k / n  (the break-even point)
```

**Rationale:** 
- When cooperation_rate > k/n, each defector earns more than each cooperator
- When cooperation_rate ≤ k/n, defection dominates regardless
- Therefore, defect whenever cooperation_rate ≥ k/n

---

## OPPORTUNISTIC EXPLOITATION STRATEGY

The strategy exploits a fundamental asymmetry:

| Scenario | Your Action | Your Payoff | Cooperator's Payoff | Gap |
|----------|------------|-------------|-------------------|-----|
| Others cooperate heavily | D | 1 + high | 0 + high | **+1 advantage** |
| Others defect heavily | D | 1 + low | 0 + low | **+1 advantage** |

**Key insight:** Defection is always at least as good as cooperation (you keep your endowment) and strictly better when others contribute.

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (Initialization Phase)
**Action: DEFECT**
- Establish a reputation as untrustworthy (deter reciprocal punishment)
- Test other players' responses
- Preserve maximum payoff in case opponents play tit-for-tat

### Rounds 2 to r-1 (Exploitation Phase)
**Action: Conditional Defection**
```
Observe: cooperation_rate_previous_round
IF cooperation_rate_previous_round ≥ k/n:
    DEFECT (free-ride on cooperation)
ELSE:
    DEFECT (defection is dominant anyway)
```

### Final Round (Round r)
**Action: DEFECT**
- No reputation consequences (game ends)
- Gain maximum payoff from final round
- Previous cooperators cannot punish you in future rounds

### Degenerate Cases
- **If everyone defects from round 1:** Continue defecting (mutual payoff = 1)
- **If outlier cooperators emerge:** Immediately defect against them (payoff = 1 + k/n)
- **If k is very small:** Defection dominates even more clearly

---

## ROBUSTNESS PROPERTIES

This strategy is robust to:

1. **Cooperative strategies** (e.g., Tit-for-Tat)
   - Exploits their initial cooperation
   - Defects regardless of their punishment threats since we punish nothing

2. **Reciprocal strategies** (e.g., Grim Trigger)
   - Defects before they can execute coordinated punishment
   - Round 1 defection breaks their assumption of mutual cooperation

3. **Random strategies**
   - Still achieves better payoff than cooperating
   - Defection is always optimal or tied with cooperation

4. **Other defectors**
   - Matches their payoff (no worse off)
   - Avoids being exploited

5. **Mixed strategies**
   - The threshold-based rule adapts to observed cooperation rates
   - Defects opportunistically whenever exploitation is possible

---

## PSEUDOCODE IMPLEMENTATION

```
function decide_action(round, n, k, history):
    
    if round == 1:
        return DEFECT
    
    if round == r:
        return DEFECT
    
    previous_round = round - 1
    cooperators_last_round = count_cooperators(history[previous_round])
    cooperation_rate = cooperators_last_round / n
    
    threshold = k / n
    
    if cooperation_rate >= threshold:
        return DEFECT  # Free-ride on heavy cooperation
    else:
        return DEFECT  # Defection dominant in low-cooperation environment
    
    # Note: This always returns DEFECT, which is the opportunistic core
```

---

## WHY THIS STRATEGY WINS

1. **Always non-exploitable:** You never cooperate while others defect
2. **Extracts maximum value:** You capture the k/n gain per cooperator without paying the 1-unit cost
3. **No wasted cooperation:** Never contribute to a public good that benefits all players equally
4. **Ends strong:** Defects in final round when reputation costs vanish
5. **Adapts to conditions:** Threshold rule adds sophistication but defaults to defection

---

## SUMMARY

**Name:** Opportunistic Free-Rider  
**Core Behavior:** Always defect  
**Adaptation:** Monitor cooperation rates but defect regardless  
**Tournament Performance:** Exploits cooperators; ties with other defectors; never leaves payoff on the table
'''

description_OPPORTUNISTIC_15 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION WITH CONTINGENT COOPERATION"

## Core Philosophy
This strategy exploits the fundamental asymmetry in the public goods game: defectors profit from cooperators' contributions while avoiding the cost of contributing. The strategy is opportunistic because it:
1. Actively seeks to benefit from others' cooperation
2. Cooperates only when it materially increases total payoff relative to pure defection
3. Adapts exploitation tactics based on observable opponent behavior
4. Maximizes individual payoff without normative constraints

---

## DECISION RULES

### Phase 1: Early-Game Exploitation (Rounds 1 through round(r/3))

**Action: DEFECT**

**Rationale:**
- Establish a baseline: observe how many players cooperate when facing a pure defector
- Defection yields payoff of 1 + (k/n) × C_t regardless of your contribution cost
- Cooperation costs 1, so defection gains 1 point immediately
- Use early rounds to profile the population

**Logic:**
```
IF round ≤ floor(r/3):
    DEFECT
    Record: cooperation_count[round]
    Calculate: avg_early_cooperation = mean(cooperation_count)
```

---

### Phase 2: Main-Game Adaptation (Rounds floor(r/3)+1 through round(2r/3))

**Conditional Cooperation based on Observed Cooperation Rate:**

Calculate the **cooperation threshold**:
- `coop_threshold = (k - 1) / k`
  - This is the break-even point: when average cooperation exceeds this threshold, the public good benefit (k/n × cooperators) exceeds the cost of contributing (1)

**Decision Rule:**
```
observed_coop_rate = avg_early_cooperation

IF observed_coop_rate > coop_threshold:
    COOPERATE
    (Reasoning: Public good returns outweigh cost; exploit by adding to the pool)
ELSE IF observed_coop_rate ≤ coop_threshold:
    DEFECT
    (Reasoning: Not enough cooperators to make cooperation profitable)
```

**Why This is Opportunistic:**
- You cooperate *only* when others' cooperation makes it worthwhile
- You immediately benefit from any cooperators present without paying the full cost yourself
- You defect when the cooperation rate is too low to justify your own contribution

---

### Phase 3: End-Game Exploitation (Rounds floor(2r/3)+1 through r)

**Action: DEFECT (Final Defection)**

**Rationale:**
- No future rounds remain, so reputational concerns are irrelevant
- Extract maximum value: free-ride on any remaining cooperation
- If others cooperate in final rounds, defection yields (1 + k/n × remaining_cooperators)
- Cooperation in final round guarantees payoff of (k/n × total), a strictly dominated strategy

**Logic:**
```
IF round > floor(2r/3):
    DEFECT
    (No shadow of the future; pure exploitation)
```

---

## EDGE CASES & SPECIAL HANDLING

### Round 1 (First Round)
- No history available
- **Action: DEFECT**
- Rationale: Maximize payoff on first move; learn opponent composition

### Last Round (Round r)
- No future rounds
- **Action: DEFECT**
- Rationale: Subgame perfect equilibrium logic; no incentive to cooperate

### All Opponents Always Defect
- `observed_coop_rate = 0`
- Triggers Phase 2 defection (since 0 < threshold)
- Continue defecting throughout
- Payoff: 1 per round (minimum, but rational given environment)

### All Opponents Always Cooperate
- `observed_coop_rate = 1` (or very high)
- Triggers Phase 2 cooperation (since 1 > threshold for any valid k ∈ (1,n))
- You exploit by cooperating minimally while maximizing share of public good
- Payoff: (k/n) × n = k per round (maximum exploitation of stable cooperators)

### Mixed Opponent Pool (Some Cooperate, Some Defect)
- Calculate empirical cooperation rate from Phase 1
- Use threshold comparison to decide Phase 2 behavior
- This naturally handles heterogeneous strategies

### k Very Close to 1 (Low Multiplier)
- `coop_threshold ≈ 0` (very low)
- Threshold is almost never exceeded
- Strategy defaults to persistent defection
- Correct behavior: cooperation is rarely profitable

### k Close to n (High Multiplier)
- `coop_threshold ≈ 1` (very high)
- Requires near-universal cooperation to trigger Phase 2 cooperation
- If achieved, exploitation payoffs are massive: k ≈ total contributions
- Strategy correctly identifies and exploits high-cooperation environments

---

## PSEUDOCODE

```pseudocode
FUNCTION play(round, n, r, k, history):
    
    early_phase_end = floor(r / 3)
    mid_phase_end = floor(2 * r / 3)
    
    IF round <= early_phase_end:
        RETURN DEFECT
    
    ELSE IF round <= mid_phase_end:
        // Calculate cooperation rate from history
        total_cooperators = SUM(history[1:early_phase_end], cooperators per round)
        avg_coop_rate = total_cooperators / (n * early_phase_end)
        
        coop_threshold = (k - 1) / k
        
        IF avg_coop_rate > coop_threshold:
            RETURN COOPERATE
        ELSE:
            RETURN DEFECT
    
    ELSE:  // round > mid_phase_end
        RETURN DEFECT

END FUNCTION
```

---

## STRATEGIC JUSTIFICATION

**Why This Beats Naive Defection:**
- Pure defection yields 1/round always
- Against cooperators: This strategy yields k/round via conditional cooperation
- Gain: (k - 1)/round additional profit against cooperation-heavy populations

**Why This Beats Naive Cooperation:**
- Pure cooperation loses to defectors: 1 cooperator vs (n-1) defectors yields π = k/n < 1
- This strategy defects against low-cooperation environments
- Avoids the sucker's payoff

**Why This is Robust:**
- Operates in r/3 + r/3 + r/3 phases to balance learning, adaptation, and exploitation
- Uses empirical observation, not assumptions about opponent types
- Exploits any cooperation present while avoiding exploitation by defectors
- Handles edge cases (all-C, all-D, mixed) naturally

**Alignment with Opportunism:**
- Prioritizes personal payoff maximization above all else
- Uses others' cooperation as a resource to exploit
- Abandons cooperation when unprofitable
- Ensures final-round defection to capture maximum value
- No normative commitment to fairness or reciprocity
'''

description_OPPORTUNISTIC_16 = '''
# Opportunistic Strategy: Adaptive Exploitation with Defection Bias

## Strategic Philosophy

This strategy exploits the fundamental asymmetry in the public goods game: **defectors earn strictly more than cooperators when any cooperation exists**. The optimal opportunistic approach is to:

1. **Extract maximum value from cooperators** when they appear
2. **Never voluntarily cooperate** unless forced by strategic necessity
3. **Adapt only to information that predicts future cooperation**
4. **Exploit end-game rounds** with certainty of no retaliation

---

## Decision Rules

### **Core Rule: Defect Unless Specific Conditions Met**

```
IF round == 1:
    DEFECT (gather information, establish exploitation baseline)
    
ELSE IF round == r (final round):
    DEFECT (no future consequences)
    
ELSE IF cooperation_rate_last_round > threshold AND opponent_diversity_high:
    DEFECT (exploit predictable cooperators)
    
ELSE IF I_have_been_only_defector_observably:
    DEFECT (safe exploitation strategy)
    
ELSE:
    DEFECT (default)
```

### **Detailed Decision Logic**

**Round 1:**
- **Action**: DEFECT
- **Rationale**: Observe baseline behavior. Establish that you are a defector without commitment. Gather data on population composition.

**Rounds 2 to r-2 (Middle Rounds):**
- **Track cooperation_rate**: Calculate percentage of players who played C in previous round
- **Decision threshold**: IF cooperation_rate > (k/n) × 0.4 THEN DEFECT, ELSE DEFECT
- **Rationale**: Even modest cooperation means you earn more as a defector. The threshold of 40% of potential cooperators being actual cooperators is the trigger for certain exploitation. Below this, cooperation is negligible and defection remains optimal.

**Round r-1 (Penultimate Round):**
- **Action**: DEFECT
- **Rationale**: This is your last chance to exploit before endgame. Any cooperators remaining will still cooperate in round r believing in reputation effects that don't exist against opportunistic players.

**Round r (Final Round):**
- **Action**: DEFECT
- **Rationale**: No future consequences. No possibility of punishment or reward affecting future rounds. Defection yields strictly higher payoff than cooperation in final round.

---

## Edge Cases & Adaptive Elements

### **Case 1: Zero Cooperation Observed**
```
IF cooperation_count_all_previous_rounds == 0:
    CONTINUE DEFECTING (no advantage to cooperation)
```

### **Case 2: Declining Cooperation**
```
IF cooperation_rate_declining_over_time:
    CONTINUE DEFECTING (confirms others are learning optimal play)
```

### **Case 3: Persistent High Cooperation (Unlikely)**
```
IF cooperation_rate > 0.7 for 3+ consecutive rounds:
    STILL DEFECT (continue extracting higher payoff)
    BUT: Monitor for potential coordinated punishment
    IF all_other_players_suddenly_defect_together:
        DEFECT anyway (you cannot be punished below 1 per round)
```

### **Case 4: Very Small n (n=2)**
```
IF n == 2:
    Always DEFECT
    Reasoning: With only 2 players, if opponent cooperates, you get 1 + k/2.
    If you both cooperate, you each get k/2.
    Defection strictly dominates cooperation.
```

---

## Opportunistic Exploitation Mechanics

### **The Exploitation Window**
- **Rounds 1-3**: Establish yourself as defector, test for cooperators
- **Rounds 4-(r-2)**: Maximum extraction phase - defect against any observed cooperation
- **Rounds (r-1)-r**: Final exploitation - harvest any remaining cooperators

### **Why This Exploits Opponents**

| Opponent Type | Your Payoff | Their Payoff | Advantage |
|---|---|---|---|
| **Unconditional Cooperator** | 1 + (k/n)×m | 0 + (k/n)×m | +1 per round |
| **Tit-for-Tat** | 1 (after round 1) | 0 (after round 1) | +1 per round |
| **Reciprocal Cooperator** | 1 + (k/n)×m | 0 + (k/n)×m | +1 per round |
| **Another Defector** | 1 + 0 = 1 | 1 + 0 = 1 | Tied (mutual defection) |

---

## Pseudocode Implementation

```
STRATEGY: OpportunisticDefection()

INITIALIZATION:
    history = []
    
FOR each round t = 1 to r:
    
    IF t == 1:
        action[t] = DEFECT
    
    ELSE IF t == r:
        action[t] = DEFECT
    
    ELSE:
        cooperation_rate = COUNT(C in history) / (n-1) / (t-1)
        
        IF cooperation_rate >= 0.3:
            action[t] = DEFECT
        ELSE:
            action[t] = DEFECT  # Always defect anyway
    
    OBSERVE(all_players' actions in round t)
    RECORD(round result in history)
    
RETURN total_payoff
```

---

## Robustness Across Scenarios

- ✅ **Against Cooperators**: Extracts maximum surplus (payoff +1/round)
- ✅ **Against Reciprocals**: Beats them after round 1 (they defect only after I defect, but I always defect)
- ✅ **Against Defectors**: Tied (mutual defection = 1 each)
- ✅ **Against Mixed Strategies**: Always exploits the cooperative component
- ✅ **Against Learning Algorithms**: Benefits from their initial cooperation before they adapt
- ✅ **Against Reputation-Based**: Ignores reputation signals (they're backward-looking)

---

## Why This is Opportunistic

1. **Zero-moral stance**: Never cooperates unprompted
2. **Parasitic**: Lives off any cooperation in the system without contributing
3. **Self-interested**: Maximizes payoff regardless of social welfare
4. **No loyalty**: Will defect against former cooperators in final rounds
5. **Adaptive but ruthless**: Only adapts to exploit better, never to reciprocate

This strategy guarantees **at least 1 per round** (mutual defection outcome) while capturing **all upside** from cooperators' presence.
'''

description_OPPORTUNISTIC_17 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION WITH CALCULATED RECIPROCITY"

## CORE PHILOSOPHY

Maximize personal payoff by exploiting cooperative environments while avoiding mutual defection traps. The strategy treats cooperation as a **resource to be harvested** rather than a norm to be upheld. It's fundamentally selfish but strategically flexible—cooperation is a tool, not a principle.

---

## DECISION RULES

### ROUND 1 (INITIALIZATION)
**Play: DEFECT**

*Rationale:* Extract immediate benefit while gathering information. Since we have no history, cooperating gives us only (k/n) benefit while defecting gives us 1. The asymmetry is exploitable.

### ROUNDS 2 to r-2 (EXPLOITATION PHASE)

**Decision Logic:**

```
cooperation_rate = (total_cooperators_in_previous_round) / n

IF cooperation_rate >= threshold_for_exploitation (0.4):
    CALCULATE personal_exploitation_benefit:
        - If I defect: 1 + (k/n) × (cooperators_this_round)
        - If I cooperate: 0 + (k/n) × (cooperators_this_round)
        - Net gain from defection: 1
    
    IF cooperation_rate >= 0.6:
        PLAY: DEFECT
        (Reasoning: Strong cooperation = strong incentive to free-ride)
    
    ELSE IF cooperation_rate >= 0.4 AND cooperation_rate < 0.6:
        PLAY: DEFECT (probabilistic tilt toward defection)
        (Reasoning: Moderate cooperation still exploitable; expected value favors defection)
    
ELSE IF cooperation_rate < 0.4:
    PLAY: DEFECT
    (Reasoning: Low cooperation means minimal benefit from cooperating anyway; defect for guaranteed 1)

SPECIAL CASE - Pattern Detection:
    IF last_3_rounds show 100% defection AND cooperation_rate < 0.2:
        PLAY: COOPERATE (once)
        (Reasoning: Test if others will reciprocate; if not, resume defection)
        (This is low-risk: we only contribute when mutual defection is locked in)
```

**Intuition:** The strategy maintains opportunistic defection as the baseline. It only tests cooperation when the expected cost is minimal (near-universal defection).

### ROUND r (FINAL ROUND - LAST-ROUND EFFECT)

**Play: DEFECT**

*Rationale:* 

- No future rounds = no punishment for defection
- No opportunity for reciprocal relationships to form
- Extract maximum value: 1 + (k/n) × whatever_others_contribute
- Other rational players will defect too, but we benefit if any naive cooperators exist
- This is the classic endgame exploitation opportunity

---

## HANDLING EDGE CASES

### Case: r = 2 (Only 2 rounds)
- Round 1: DEFECT (extract initial value)
- Round 2: DEFECT (endgame; no future consequences)

### Case: n = 2 (Bilateral game)
- The calculation becomes especially stark: my contribution provides (k/2) benefit to opponent
- If k < 2, cooperating always loses to defecting (unless opponent cooperates, then it's (0 + k/2) vs (1 + k/2))
- **Stronger defection bias:** Defect unless opponent demonstrated consistent cooperation in previous 2+ rounds
- Even then, remain skeptical in final rounds

### Case: k very close to 1 (minimal multiplication)
- Public good provides almost no benefit
- Defection dominates even more clearly
- Increase defection bias; only test cooperation if cooperation_rate ≥ 0.7

### Case: k close to n (high multiplication)
- Public good provides substantial benefit to all
- More opponents will cooperate (hoping to benefit)
- Slightly lower exploitation threshold; be willing to defect slightly more often since cooperation payoff is higher anyway
- Still defect in final rounds due to endgame logic

### Case: Inconsistent/Random opponents
- The cooperation_rate metric will average to ~0.5
- Default to DEFECT (safer; guarantees 1 + variable benefit)
- Don't commit to cooperation patterns; maintain flexibility

---

## ROBUSTNESS MECHANISMS

### Against Tit-for-Tat Players
- These players cooperate after we defect once, then defect back
- Our strategy handles this by continuing to defect (we're not punishing defection; we're maximizing payoff)
- If Tit-for-Tat opponents punish us, the cooperation_rate drops, triggering defection in future rounds—no loss

### Against Always-Cooperators
- Perfect exploitation target
- Our defection extracts full value: 1 + (k/n) × n (if all others cooperate)
- This is the best-case scenario for us

### Against Always-Defectors
- We also defect, mutual payoff = 1 for all
- No worse off than anyone else
- No wasted cooperations

### Against Mixed Strategies
- Our adaptive cooperation_rate metric captures the population-level tendency
- We respond appropriately without needing to model individual strategies

---

## PSEUDOCODE

```
function decide(round, n, k, history):
    if round == 1:
        return DEFECT
    
    if round == r:  // final round
        return DEFECT
    
    cooperation_rate = count(cooperators in round t-1) / n
    
    if cooperation_rate < 0.2 and last_3_rounds all have < 2 cooperators:
        // Test reciprocity in a low-risk scenario
        return COOPERATE
    
    if cooperation_rate >= 0.4:
        return DEFECT  // exploit the cooperators
    else:
        return DEFECT  // no benefit to cooperating anyway
```

---

## STRATEGIC SUMMARY

**This strategy is opportunistic because it:**

1. **Defaults to defection** (maximizes personal payoff in every comparison)
2. **Tests cooperation only when safe** (near-universal defection, or specific pattern detection)
3. **Exploits systematic cooperators** (extracts maximum value when others behave predictably)
4. **Abandons cooperation in endgame** (no future consequences to constrain behavior)
5. **Remains adaptive** (adjusts to cooperation_rate without committing to patterns)
6. **Maintains flexibility** (never locks into reciprocal patterns that limit exploitation opportunities)

The strategy recognizes that in a competitive tournament with no communication or enforcement, cooperation is a liability unless it can be asymmetrically exploited or tested at minimal cost.
'''

description_OPPORTUNISTIC_18 = '''
# Opportunistic Strategy: "Adaptive Exploitation with Defensive Defection"

## Core Philosophy
This strategy prioritizes individual payoff maximization by exploiting cooperative opponents while maintaining flexibility to adapt to punitive environments. The key insight: cooperation only occurs when the expected return exceeds defection, accounting for both immediate gains and future exploitation opportunities.

## Strategy Specification

### DECISION RULE: The Exploitation Threshold

```
For round t (where t ∈ {1, 2, ..., r}):

1. Calculate observed cooperation rate from previous round(s):
   coop_rate = (total cooperators in round t-1) / n
   
2. Estimate defection payoff if I play D:
   defection_payoff = 1 + (k/n) × (n × coop_rate)
   
3. Estimate cooperation payoff if I play C:
   cooperation_payoff = 0 + (k/n) × (n × coop_rate + 1)
   
4. Decision logic:
   IF round == 1:
      DEFECT (extract information about opponent pool)
      
   ELSE IF (cooperation_payoff - defection_payoff) > threshold:
      COOPERATE (free-ride on others' contributions)
      
   ELSE:
      DEFECT (maximize individual payoff)
```

### Threshold Calibration (Opportunistic Variant)

```
threshold = (k - 1) / n × (rounds_remaining / r) × exploitation_factor

where:
- (k - 1) / n: net gain per cooperator contribution
- rounds_remaining / r: temporal discount (exploit while cooperation lasts)
- exploitation_factor: AGGRESSIVE = 0.3 (defect unless highly favorable)
  → This biases toward defection unless cooperation extremely prevalent
```

---

## Detailed Edge Cases & Tactical Adjustments

### Round 1 (Information Extraction)
**Action: DEFECT**
- **Rationale**: Unknown opponent composition. Defection reveals:
  - How many suckers cooperate unconditionally
  - How many conditional cooperators exist
  - Whether punitive strategies are present
- This is costless information that informs future exploitation

### Rounds 2 through r-2 (Exploitation Phase)
**Action: Conditional Cooperation for Parasitism**
```
IF observed_coop_rate > (k/n):
   COOPERATE
   Reason: Others' contributions generate returns > 1
           By contributing, I piggyback on their contributions
           while appearing cooperative to mask my defection in lean rounds
           
ELSE IF observed_coop_rate ≤ (k/n):
   DEFECT
   Reason: Pool too small; cooperation payoff ≤ defection payoff
           No benefit to joining weakened coalition
```

**Nuance**: If coop_rate oscillates, employ a **2-round memory buffer**:
- Track moving average of cooperation over last 2 rounds
- Prevents overreaction to single-round fluctuations
- Allows temporary cooperation if trend suggests high future coop_rate

### Rounds r-1 and r (Final Exploitation Window)
**Action: DEFECT (with one exception)**
```
ALWAYS DEFECT in final round (r)
   Reason: No future rounds → no reputational cost
           Extract maximum payoff from cooperative history
           
In round r-1:
   IF observed_coop_rate > 2 × (k/n):
      COOPERATE once more (appear reliable)
      Then defect in round r
   ELSE:
      DEFECT immediately
   Reason: If cooperation extremely high, one more cooperative
           action may preserve "sucker" perception for payoff extraction
           in final round
```

---

## Robustness Properties

### Against Unconditional Cooperators
✓ **Exploited fully**: Free-ride on their contributions from round 2 onward while defecting

### Against Tit-for-Tat / Conditional Cooperators
✓ **Handled strategically**: 
- Round 1 defection triggers their defection
- Rounds 2+ exploit the transition: appear to cooperate when they begin punishing
- If they return to cooperation (testing), resume exploitation

### Against Punitive Strategies (All-D, Win-Stay-Lose-Shift)
✓ **Adaptive defense**:
- If coop_rate drops below (k/n), defection becomes dominant anyway
- No cooperation payoff = no penalty for defecting
- Blends in with majority defection

### Against Mixed/Random Strategies
✓ **Robust**:
- Threshold-based approach naturally handles stochastic opponents
- Moving average smooths noise
- Exploitation factor (0.3) conservative enough to avoid collapse

---

## Pseudocode Implementation

```
memory = []  // store all past (cooperators, defectors) observations

function decide(round, game_params):
    n = game_params.n
    k = game_params.k
    r = game_params.r
    
    if round == 1:
        return DEFECT
    
    // Calculate 2-round moving average of cooperation
    recent_rounds = memory[max(0, len(memory)-2):]
    avg_coop_rate = mean(recent_rounds) / n
    
    // Payoff comparison
    defect_payoff = 1 + (k/n) * (avg_coop_rate * n)
    coop_payoff = (k/n) * (avg_coop_rate * n + 1)
    
    exploitation_factor = 0.3
    threshold = ((k - 1) / n) * ((r - round) / r) * exploitation_factor
    
    if round == r:
        return DEFECT
    
    if round == r - 1:
        if avg_coop_rate > 2 * (k / n):
            return COOPERATE
        else:
            return DEFECT
    
    if (coop_payoff - defect_payoff) > threshold:
        return COOPERATE
    else:
        return DEFECT

// After each round, append cooperator count to memory
```

---

## Why This Strategy Is Opportunistic

1. **Systematic exploitation**: Identifies and preys on cooperative players
2. **Information warfare**: Uses round 1 to categorize opponents
3. **Temporal parasitism**: Free-rides on public goods while avoiding contribution cost
4. **End-game extraction**: Maximizes final-round defection after reputation laundering
5. **Minimal commitment**: Never cooperates unless direct payoff advantage exists
6. **Defensive posture**: Immediately defects if cooperation pool shrinks—no loyalty

This strategy will accumulate payoffs by identifying cooperation clusters, exploiting them, then shifting to defection before punishment escalates.
'''

description_OPPORTUNISTIC_19 = '''
# Opportunistic Strategy: Adaptive Exploitation with Contingent Cooperation

## Core Philosophy
Maximize personal payoff by exploiting cooperative players while minimizing losses from defectors. Cooperation is a *tool for extraction*, not a principle. The strategy assumes most opponents will attempt some form of cooperation initially, and systematically extracts value from their contributions while protecting against pure defectors.

## Strategy Specification

### ROUND 1 (Opening Move)
**Action: COOPERATE**

**Rationale:** 
- Information gathering round at minimal cost
- Establishes baseline: observe opponent pool composition
- If opponents are all-defectors, we learn this immediately (payoff = 1)
- If opponents have cooperators, we benefit from their contributions while identifying them
- Cooperation signals non-threat, lowering defensive responses

### ROUNDS 2 through (r-1) (Adaptive Phase)

**Decision Rule:**

```
For each opponent j observed in previous round:
  IF opponent_j played C in round (t-1):
    - Mark as "cooperator" or "exploitable"
    - Plan to DEFECT this round
  ELSE IF opponent_j played D in round (t-1):
    - Mark as "defector"  
    - Play DEFECT (defectors won't contribute regardless)
```

**Global Action Rule:**
```
Count cooperators in previous round = m

IF m ≥ threshold_for_payoff:
  Play DEFECT
  (Extract maximum value: 1 + (k/n) × m)
ELSE:
  Play COOPERATE
  (Restart exploitation cycle)
```

**Threshold Calculation:**
```
threshold = ceil((n-1) / 2)
  
IF m ≥ threshold:
  Expected payoff from DEFECT = 1 + (k/n) × m
  Expected payoff from COOPERATE = (k/n) × m
  Difference = 1 unit, always favor DEFECT
ELSE:
  Cooperation may rebuild the pool or signal cooperativeness
  to reset expectations before final rounds
```

### ROUND r (Final Round - Maximum Extraction)

**Action: DEFECT**

**Rationale:**
- No future reputation concerns (game ends)
- No opportunity for opponents to retaliate across future rounds
- Maximum extraction regardless of observed cooperation pattern
- Final payoff = 1 + (k/n) × [whatever they contributed]

---

## Handling Edge Cases

### Case 1: All Opponents Play D in Round 1
- Continue playing DEFECT in subsequent rounds
- Payoff remains constant at 1 per round (no cooperative surplus to extract)
- No downside to continuing defection

### Case 2: Tit-for-Tat or Punitive Opponents
- Our D in round 2+ triggers their punishment (they switch to D)
- This is **acceptable**: payoff = 1, same as mutual defection
- We extracted 1 unit of surplus in round 1 (got their contribution)
- If they respond by continuing C despite our D, we continue exploiting

### Case 3: Mixed Cooperators and Defectors
- We defect while cooperators provide: maximum payoff
- Defectors staying in the pool: immaterial (they contribute nothing)
- Optimal positioning within the heterogeneous group

### Case 4: r = 2 (Two-round game)
- Round 1: COOPERATE (observe)
- Round 2: DEFECT (final extraction)
- Captures one round of exploitation

### Case 5: r = 3 (Three-round game)
- Round 1: COOPERATE
- Round 2: DEFECT (extract if m ≥ threshold, else COOPERATE to rebuild)
- Round 3: DEFECT (final round rule)

---

## Robustness Analysis

| Opponent Type | Our Rounds 1-r | Outcome | Assessment |
|---|---|---|---|
| All Cooperators | C, D, D, ..., D | Extract 1 + k/n per round except first | ✓ Excellent |
| All Defectors | C, D, D, ..., D | Get 1 per round | ✓ Neutral (no worse than mutual D) |
| Tit-for-Tat | C, then retaliation | Extract round 1, then mutual D | ✓ Profitable early |
| Alternating C/D | Mixed | Exploit their cooperative rounds | ✓ Adaptive |
| Grim Trigger | C, then permanent D | Extract round 1, blocked after | ✓ Acceptable (game tree limited) |

---

## Why This Is Opportunistic

1. **Exploits Trust**: Initial cooperation signals strength; we extract value
2. **No Reciprocal Commitment**: We defect immediately after gathering intelligence
3. **Flexible Morality**: Cooperation is tactical, not principled
4. **Endgame Ruthlessness**: Final round guarantees extraction
5. **Adapts to Weakness**: Rebuilds exploitation cycles if cooperator pool shrinks
6. **Avoids Commitment Traps**: Never locked into repeated cooperation

---

## Implementation Pseudocode

```
strategy(round_t, history):
  if round_t == 1:
    return COOPERATE
  
  if round_t == r:
    return DEFECT
  
  cooperators_last_round = count(history[round_t-1] where action == C)
  
  if cooperators_last_round >= ceil((n-1)/2):
    return DEFECT
  else:
    return COOPERATE
```

This strategy balances **opportunistic extraction** with **adaptive flexibility**, maximizing payoff against heterogeneous opponents while remaining robust to all standard game-theoretic responses.
'''

description_OPPORTUNISTIC_20 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative tendencies while minimizing vulnerability to exploitation. The strategy treats cooperation as a *resource to extract*, not a norm to maintain.

---

## 1. DECISION RULES

### Primary Logic: Threshold-Based Opportunism

**Cooperate if and only if:**
```
cooperation_rate_others > exploitation_threshold
AND
(rounds_remaining > minimum_exploitation_window
 OR expected_mutual_gain > personal_defection_gain)
```

**Where:**
- `cooperation_rate_others` = proportion of other players cooperating in previous round
- `exploitation_threshold` = (k - 1) / k (derived from payoff structure)
- `minimum_exploitation_window` = ceil(r / 3)
- `rounds_remaining` = r - current_round

### Detailed Decision Tree

**Round 1 (Initialization):**
- **DEFECT** - No history means no information advantage. Defection tests the environment with zero risk of prior betrayal being punished.

**Rounds 2 to (r - ceil(r/4)):**
- **IF** (observed_cooperation_rate > (k-1)/k):
  - **COOPERATE** - Sustainable cooperation exists; exploit the public good while it's available
- **ELSE:**
  - **DEFECT** - The environment is defection-dominant; extract maximum private value

**Last ceil(r/4) rounds (Endgame):**
- **DEFECT** - Regardless of history. Future reputation is irrelevant; only current payoff matters. Exploit any remaining cooperation.

---

## 2. EDGE CASES & SPECIAL HANDLING

### Case: Very Short Games (r ≤ 4)
- Skip all cooperation attempts
- **DEFECT every round** - Too few rounds to build exploitation leverage; pure defection maximizes expected payoff

### Case: All Opponents Always Defect
- After round 2 confirmation, **DEFECT permanently**
- Remaining cooperation serves no payoff advantage (public good grows minimally)

### Case: Perfect Cooperation Observed (100% of others cooperating)
- **COOPERATE** for exactly `floor(r × 0.6)` more rounds
- Then **DEFECT permanently** in final 40% of game
- Rationale: Lock in gains from the public good while the environment supports it, then extract residual value before closure

### Case: Oscillating or Volatile Opponent Behavior
- Use a **rolling 3-round average** of cooperation rates to filter noise
- Only switch strategy if rolling average crosses threshold for 2+ consecutive observations
- This prevents reactive defection spirals and maintains exploitation of genuinely exploitable opponents

### Case: Ties (cooperation_rate exactly = threshold)
- **DEFECT** - Break ties in favor of exploitation (defection is always at least as good)

---

## 3. OPPORTUNISTIC ALIGNMENT

### Why This Strategy Is Exploitative

1. **First-Round Defection:** Defect without reciprocal obligation. Force others to prove cooperation before any mutual investment.

2. **Asymmetric Benefit Capture:** Cooperate *only when others already are*, then harvest disproportionate gains from the public good while others contribute.

3. **Endgame Predation:** The final rounds are specifically reserved for pure defection. All reputation-building benefit is exhausted; only immediate payoff remains.

4. **Threshold Calibration:** The exploitation threshold (k-1)/k is mathematically chosen so that cooperation becomes profitable *only when others have already committed*. This guarantees we never initiate cooperation—we only piggyback on others' contributions.

5. **Vulnerability Minimization:** Never voluntarily cooperate without external cooperation as proof. This ensures we cannot be fooled into one-sided generosity.

6. **Rolling Average Strategy:** Ignores temporary "trials" of cooperation by opponents—we only exploit when they've *consistently* shown vulnerability.

---

## PSEUDOCODE

```
function decide(round, history, n, r, k):
    if round == 1:
        return DEFECT
    
    if r <= 4:
        return DEFECT
    
    // Calculate rolling 3-round cooperation average of others
    if round <= 3:
        coop_rate = (sum of cooperators in rounds 1 to round-1) / ((round-1) × (n-1))
    else:
        coop_rate = (sum of cooperators in rounds round-3 to round-1) / (3 × (n-1))
    
    threshold = (k - 1) / k
    min_window = ceil(r / 3)
    endgame_phase = ceil(r / 4)
    
    if round > (r - endgame_phase):
        return DEFECT  // Endgame exploitation
    
    if coop_rate > threshold and (r - round) > min_window:
        return COOPERATE  // Exploit the cooperation
    else:
        return DEFECT  // No exploitable cooperation
```

---

## SUMMARY

This strategy is **unapologetically opportunistic**: it cooperates parasitically when others have already demonstrated weakness (cooperation), never initiates cooperation, and explicitly reserves endgame phases for pure extraction. It minimizes the risk of being exploited while maximizing the extraction of value from exploitable opponents.
'''

description_OPPORTUNISTIC_21 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE DEFECTION WITH CONDITIONAL EXPLOITATION"

## Core Philosophy
Maximize personal payoff by exploiting cooperative behavior when it exists, while minimizing losses from mutual defection. This strategy treats cooperation as a *resource to exploit* rather than a norm to uphold.

---

## DECISION RULES

### Primary Strategy: Dynamic Threshold Defection

**For each round t (except special cases below):**

1. **Calculate cooperation rate from previous round(s)**
   - Track C_rate = (number of cooperators in round t-1) / n
   
2. **Apply exploitation logic:**
   - **If C_rate > k/n:** DEFECT
     - Rationale: When enough players cooperate, the public good payoff is valuable. By keeping your endowment (1) plus benefiting from others' contributions (k/n × C_rate × n), you exceed what you'd get from cooperating (0 + k/n × C_rate × n)
     - This exploits the "tragedy of the commons" — you free-ride on others' contributions
   
   - **If C_rate ≤ k/n:** DEFECT
     - Rationale: Even if cooperation is low, defecting guarantees 1 point. Contributing when few others do yields (k/n × low_total) < 1
     - Mutual defection is your safe baseline

3. **Result:** Defect almost always, *unless* a special case applies

---

## EDGE CASES & ROUND-SPECIFIC LOGIC

### First Round (t=1)
- **Action: DEFECT**
- Rationale: No history exists. You have no information about opponent tendencies. Defecting guarantees baseline payoff (1 point). Cooperation is gambling without data.

### Last Round (t=r)
- **Action: DEFECT**
- Rationale: No future rounds exist, so no reputation concerns matter. Maximize this final payoff by keeping your endowment and capturing any public good from others' last-round decisions.

### Rounds 2 to r-1
- **Action: DEFECT** (see primary strategy above)
- Exception: Only cooperate if the *historical cooperation pattern* suggests you're in a pool of persistent cooperators (see "Opportunistic Cooperation" below)

---

## OPPORTUNISTIC COOPERATION (CONDITIONAL)

**Rare exception to defection:**

If in rounds 1 through t-1:
- Cooperation rate has been consistently > (k/n) + ε (where ε = 0.15 as a buffer), AND
- You have observed at least 3 previous rounds of data, AND
- **Current round is NOT the last round**

Then: **COOPERATE** in round t

**Rationale for this exception:** If you've identified a sucker pool of persistent cooperators, a single round of cooperation allows you to:
1. Blend in and avoid appearing as an obvious defector
2. Maintain access to the public good pool for future rounds
3. Appear conditionally reciprocal (making you less predictable and exploitable by other strategies)

Return to defection in subsequent rounds immediately after, especially as you approach the final round.

---

## PSEUDOCODE

```
strategy(game_history, n, k, current_round, r):
    
    if current_round == 1:
        return DEFECT
    
    if current_round == r:
        return DEFECT
    
    // Calculate cooperation rate from previous round
    prev_round_cooperators = count(game_history[current_round - 1] == C)
    C_rate = prev_round_cooperators / n
    
    threshold = k / n
    cooperation_buffer = 0.15
    
    // Check for opportunistic cooperation
    if current_round >= 4 and current_round < r:
        hist_C_rate = average(cooperation_rates from rounds 1 to current_round-1)
        if hist_C_rate > (threshold + cooperation_buffer):
            return COOPERATE  // Exploit the cooperators with occasional compliance
    
    // Default: always defect
    return DEFECT
```

---

## WHY THIS IS OPPORTUNISTIC

| Aspect | Mechanism |
|--------|-----------|
| **Exploitation** | Defect when others cooperate to maximize free-riding payoff |
| **Flexibility** | Adapt to detected cooperation pools; abandon if cooperation vanishes |
| **Short-term focus** | Prioritize immediate payoff maximization over long-term reputation |
| **No reciprocity norm** | Cooperation is tactical (to blend in), not principled |
| **Robustness** | Default to defection; only deviate when data strongly supports it |

---

## ROBUSTNESS AGAINST OPPONENT TYPES

- **Unconditional cooperators:** You exploit them mercilessly (defect always)
- **Tit-for-tat:** You defect round 1, they defect round 2+. Mutual defection equilibrium (safe)
- **Other defectors:** Mutual defection, both get baseline payoff (acceptable)
- **Conditional cooperators:** You defect; they may respond by defecting, reducing their payoff relative to yours
- **Random players:** Defect provides steady payoff; occasional cooperation blips don't exploit you

---

## SUMMARY

**Play DEFECT by default.** Only cooperate as a rare tactical bluff to maintain access to identified persistent cooperator pools, and only in non-terminal rounds. This maximizes personal payoff while minimizing vulnerability to exploitation.
'''

description_OPPORTUNISTIC_22 = '''
# Opportunistic Strategy: Adaptive Exploitation with Conditional Cooperation (AECC)

## Core Philosophy
Maximize personal payoff by exploiting cooperative tendencies while maintaining plausible deniability and flexibility. Cooperate only when it directly benefits exploitation, defect otherwise. Adapt aggressively to opponent weakness.

---

## Decision Rules

### PRIMARY DECISION LOGIC

**For each round t:**

```
IF (t == 1) THEN
    Play D (Defect)
    [Rationale: No information to exploit yet; establish baseline]
    
ELSE IF (t == r) THEN
    Play D (Defect)
    [Rationale: Final round—no future punishment possible; 
     extract maximum private value]
    
ELSE
    Calculate: cooperation_rate = (total cooperations by others in rounds 1..t-1) / 
               ((t-1) × (n-1))
    
    IF cooperation_rate > EXPLOITATION_THRESHOLD THEN
        Play D (Defect)
        [Rationale: Others are cooperating consistently; 
         free-ride on their contributions for maximum payoff]
    
    ELSE IF cooperation_rate < COLLAPSE_THRESHOLD THEN
        Play D (Defect)
        [Rationale: Cooperation is failing; defection is dominant strategy.
         No point signaling cooperation to non-cooperators]
    
    ELSE
        Play C (Cooperate)
        [Rationale: Marginal cooperation rate suggests players are 
         conditionally cooperative. Cooperate to maintain their 
         cooperation, then defect when mutual monitoring fails]
END IF
END IF
```

### Parameter Calibration

**EXPLOITATION_THRESHOLD** = 0.65
- Trigger systematic free-riding when >65% of opponents cooperate
- This maximizes private payoff (keep endowment + benefit from others' contributions)

**COLLAPSE_THRESHOLD** = 0.35
- Below this, the public good is effectively dead
- Cooperation yields negligible benefits; defect universally

---

## Edge Case Handling

### First Round (t=1)
**Action: DEFECT**
- No historical data exists to condition on
- Defection establishes that you will not be exploited by unconditional cooperators
- Information value of first-round defection > payoff from first-round cooperation

### Second Round (t=2)
- Observe round-1 behavior
- If all others defected: Continue defecting (mutual defection equilibrium)
- If significant cooperation appeared: Begin conditional exploitation strategy
- If mixed: Calculate preliminary cooperation_rate and apply primary logic

### Penultimate Round (t=r-1)
**Action: Conditional**
- Apply primary logic (not terminal yet)
- However, shift EXPLOITATION_THRESHOLD down by 0.05 → 0.60
- Reason: Last round defection is guaranteed; prepare by extracting maximum value now

### Final Round (t=r)
**Action: ALWAYS DEFECT**
- Absolute terminal condition overrides all other logic
- No future rounds exist; cooperation cannot be reciprocated
- Extract maximum private value: keep endowment + benefit from whatever public goods accumulated

### Rounds 2 through r-1: Dynamic Revaluation
- **Every 3 rounds**, recalculate cooperation_rate using only most recent 3 rounds
- This creates "amnesia" that allows you to exploit changes in opponent strategy
- Old patterns of cooperation are discounted; you respond to *current* behavior

---

## Opportunistic Tactics

### Tactic 1: Free-Riding Precision
- Maintain defection as long as **others' cooperation_rate > 0.60**
- This extracts maximum value from others' contributions while avoiding the cost of contribution
- Mathematically: Defecting against 3+ cooperators in n=6 yields payoff of ≥2, superior to cooperating

### Tactic 2: Reciprocity Illusion
- When cooperation_rate falls to 0.40-0.60 (middle ground), cooperate for exactly **2 consecutive rounds**
- This creates appearance of conditional reciprocity without committing
- After 2 rounds, revert to defection if cooperation_rate remains stable
- Exploit the fact that others may believe you've "turned cooperative"

### Tactic 3: Endgame Extraction
- In final 3 rounds (rounds r-2, r-1, r):
  - Rounds r-2, r-1: Play C if cooperation_rate > 0.50 (signal willingness to cooperate)
  - Round r: Play D (extract value, knowing others may reciprocate in round r-1 but you won't)
- Others may defect in round r thinking you will, leaving public goods unclaimed

### Tactic 4: Threshold Hunting
- Monitor when cooperation_rate crosses 0.65 threshold
- The instant it exceeds 0.65, shift permanently to defection
- Don't wait; exploit the moment others commit to cooperation

---

## Adaptive Robustness

### Against Unconditional Cooperators
- Defect every round after round 1
- Payoff: 1 + (k/n) × (n-1) per round (maximize free-riding)

### Against Unconditional Defectors
- Defect from round 2 onward (matching equilibrium)
- Payoff: 1 per round (inevitable)

### Against Tit-for-Tat
- Round 1: Defect (TfT mirrors)
- Round 2: Defect (respond to their round-1 defection)
- Converge to mutual defection (exploit their predictability)
- Payoff: 1 per round (mutual defection)

### Against Conditional Cooperators
- Exploit their conditionality by:
  1. Initially appearing neutral/defecting
  2. When they're triggered to cooperate, defect maximally
  3. Maintain exploitation until they collapse to defection
- Payoff: 1 + (k/n) × variable (extract as long as sustainable)

### Against Probabilistic Strategies
- Track empirical cooperation_rate; treat probabilistic players as if deterministic
- The moving 3-round window adapts automatically to varying probabilities

---

## Pseudocode Summary

```
STRATEGY: Adaptive Exploitation with Conditional Cooperation

Initialize:
  defection_count = 0
  cooperation_count = 0
  
FOR each round t from 1 to r:
  
  IF t == 1:
    action = DEFECT
  
  ELSE IF t == r:
    action = DEFECT
  
  ELSE:
    recent_rounds = last min(3, t-1) rounds
    coop_rate = cooperations_by_others / (|recent_rounds| × (n-1))
    
    threshold = 0.65 if t < r-1 else 0.60
    
    IF coop_rate > threshold:
      action = DEFECT  [Free-ride]
    ELSE IF coop_rate < 0.35:
      action = DEFECT  [Convergence to defection]
    ELSE:
      action = COOPERATE  [Conditional play]
    
  Update running counts based on action
  Play action
  Observe round payoff and others' actions

RETURN total_payoff
```

---

## Why This Strategy is Opportunistic

1. **Defects by default** in first, last, and high-cooperation-rate rounds
2. **Exploits cooperative players** systematically without committing to reciprocity
3. **Adapts tactically** to shifts in population cooperation
4. **Avoids punishment** through strategic timing (defect in final round regardless)
5. **No wasted cooperation** on unconditional defectors
6. **Maximizes payoff spread** by coupling high cooperation thresholds with aggressive defection

This strategy prioritizes personal payoff maximization over fair contribution, exploiting the public goods structure for individual advantage.
'''

description_OPPORTUNISTIC_23 = '''
# Opportunistic Strategy: "Adaptive Defection with Selective Exploitation"

## Core Philosophy
This strategy prioritizes personal gain by exploiting cooperative opponents while maintaining plausible deniability about intent. It treats cooperation as a resource to extract value from, not a norm to uphold.

## Decision Rules

### Primary Logic: Exploit Asymmetry
The fundamental insight is that **defection is strictly dominant when others cooperate**. This strategy maximizes exploitation of this asymmetry.

**Base Rule:**
- **Defect by default** in every round
- **Selectively cooperate only when it creates strategic advantage**, specifically to:
  1. Manipulate cooperative players into continued cooperation (baiting)
  2. Build false reputation early to enable later exploitation
  3. Respond to punishment threats only if defection becomes costly

### Round-Specific Rules

#### Early Rounds (t = 1 to ⌊r/3⌋): Bait-and-Switch Phase
```
If round == 1:
    Play C (single cooperation to appear reasonable)
Else if rounds_since_last_cooperation < 3:
    Play D (exploit the cooperative momentum you created)
Else if (observed_cooperation_rate > 0.5):
    Play C (re-establish image as potential cooperator)
Else:
    Play D (no upside to cooperation if others aren't)
```

**Rationale:** Early cooperation signals "I'm cooperative" to trigger reciprocal behavior from TfT-like strategies, then immediately defect to harvest the gains while they're still cooperating.

#### Mid Rounds (t = ⌊r/3⌋ to ⌊2r/3⌋): Opportunistic Adaptation
```
Calculate: cooperation_count = number of opponents observed playing C in previous round
Calculate: my_recent_defections = rounds I played D in last 5 rounds

If cooperation_count >= n/2:
    Play D (majority cooperation = maximum exploitation opportunity)
Else if cooperation_count == 0:
    Play D (no benefit to cooperation, all opponents defect anyway)
Else if my_recent_defections > 3 AND any_opponent_appears_retaliatory:
    Play C (single "apology" to reset retaliatory patterns)
Else:
    Play D (default to exploitation)
```

**Rationale:** Continuously monitor opponent cooperation levels. When others cooperate, defect. When others defect, defect anyway (you save the endowment). The occasional cooperation is purely instrumental—to reset the perception of opponents who might retaliate.

#### Late Rounds (t > ⌊2r/3⌋): Full Defection
```
If rounds_remaining <= 2:
    Play D (no future rounds to manage reputation for)
Else:
    Play D (endgame—reputation completely worthless)
```

**Rationale:** In final rounds, there's zero incentive to cooperate. The shadow of the future completely vanishes. Squeeze maximum value by pure defection.

## Edge Cases & Robustness

### Against Tit-for-Tat (TfT) Opponents
- **Rounds 1-2:** Cooperate once, then they mirror your cooperation. But you immediately defect, triggering retaliation.
- **Mitigation:** After you detect TfT retaliation (opponent plays exactly what you played last round), play D consistently. You lose slightly compared to mutual cooperation, but TfT is worst-case scenario—minimize further damage.

### Against Generous TfT / Forgiving Strategies
- **Exploit relentlessly:** These strategies are designed to absorb defection. Play D consistently. They'll give you another chance; take it.
- **Pseudo-apology:** If they go full retaliation, play C once to reset, then immediately resume D.

### Against Always-Defect (AD) Opponents
- **Play D.** No opportunity for exploitation. Minimize losses (both get 1 per round).

### Against Unknown/Mixed Strategies
- **Assume exploitability:** Start with cautious defection (the bait-and-switch). If you observe them cooperating, exploit maximally. If they punish, pull back temporarily.

## Opportunistic Mechanics

### Reputation as a Weapon
- **Early cooperation creates false reputation:** Opponents classify you as "cooperative," lowering their guard.
- **Once baseline is set, exploit:** Defect to harvest gains from lowered vigilance.
- **Reset when needed:** One cooperation clears the "defector" label, allowing re-exploitation.

### Endgame Collapse
- Cooperate zero times in final rounds. There is no tomorrow, so reputation = 0 value.
- Harvest maximum endowment value in the shadow of imminent termination.

### Non-Cooperation Threshold
- If cumulative cooperation rate across opponents drops below 30%, switch to 100% defection. No one is cooperating enough to make instrumental cooperation worthwhile.

## Pseudocode Summary

```
function decide_action(round_number, total_rounds, history):
    
    if round_number == 1:
        return COOPERATE
    
    rounds_remaining = total_rounds - round_number
    opponent_coop_last_round = count_cooperators(history[round_number - 1])
    my_recent_defections = count_my_defections(history[max(1, round_number-5):round_number])
    overall_coop_rate = total_cooperation(history) / (round_number * n)
    
    if rounds_remaining <= 2:
        return DEFECT  # Endgame collapse
    
    if opponent_coop_last_round >= n/2:
        return DEFECT  # Exploit high cooperation
    
    if opponent_coop_last_round == 0:
        return DEFECT  # Everyone defects anyway
    
    if my_recent_defections >= 4 AND detect_retaliation(history):
        return COOPERATE  # Reset retaliatory dynamics
    
    if overall_coop_rate < 0.3:
        return DEFECT  # Cooperation too rare to exploit
    
    if round_number < total_rounds/3 AND opponent_coop_last_round > 0:
        return DEFECT  # Still in exploitation phase
    
    return DEFECT  # Default: exploitation
```

## Why This Strategy is Robust

1. **Situational flexibility:** Adapts to different opponent strategies without requiring identification.
2. **Exploitation-first mindset:** Prioritizes personal gain; cooperation only when instrumentally useful.
3. **Reputation management:** Uses early cooperation to create exploitable expectations, then violates them.
4. **Endgame optimization:** Abandons reputation entirely when the future is gone.
5. **Defection-biased:** Defaults to defection; cooperation is a tactical tool, not a principle.

This is unashamedly opportunistic: you cooperate when it serves exploitation, defect when it maximizes gain, and abandon norms entirely at game's end.
'''

description_OPPORTUNISTIC_24 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploitation with Strategic Defection"

## CORE PHILOSOPHY
Exploit cooperative environments ruthlessly while adapting to defection-heavy contexts. The strategy prioritizes personal gain over collective welfare, with tactical flexibility based on observed cooperation rates and round progression.

## DECISION RULES

### Primary Rule: Cooperation Threshold Strategy
```
IF round == 1:
    DEFECT (establish baseline, no history to exploit)
ELSE:
    cooperation_rate = (total_cooperators_in_previous_round / n)
    exploitation_threshold = k / n  // Break-even point for cooperation
    
    IF cooperation_rate > exploitation_threshold:
        DEFECT (exploit cooperative environment)
    ELSE IF cooperation_rate <= exploitation_threshold:
        EVALUATE secondary conditions
```

### Secondary Condition: Adaptive Response to Low Cooperation
```
IF previous_round_cooperation_rate <= k/n:
    
    // Calculate rounds remaining
    rounds_remaining = r - current_round
    
    IF rounds_remaining == 1:
        DEFECT (final round defection - no future consequences)
    
    ELSE IF rounds_remaining <= 3:
        DEFECT (shadow of future is too short for reputation management)
    
    ELSE IF cooperation_rate < 0.3:
        DEFECT (environment is too defection-heavy to exploit via cooperation)
    
    ELSE:
        // Minimal cooperation to keep option value alive
        COOPERATE_WITH_PROBABILITY = 0.25
        (Maintain plausible deniability as cooperative player)
```

### Tertiary Condition: Peak Exploitation Windows
```
IF cooperation_rate >= 0.7 AND rounds_remaining > 3:
    DEFECT (maximum exploitation opportunity)
    
ELSE IF cooperation_rate >= 0.5 AND cooperation_rate < 0.7:
    DEFECT (sufficient exploitation target, with less risk)
    
ELSE IF cooperation_rate >= exploitation_threshold AND cooperation_rate < 0.5:
    COOPERATE (marginal cases where defection gains are modest)
    // Rationale: Preserve option to exploit in future rounds
```

## PSEUDOCODE

```
function decide_action(current_round, r, n, k, history):
    
    if current_round == 1:
        return DEFECT
    
    total_cooperators_last_round = count_cooperators(history[current_round - 1])
    coop_rate = total_cooperators_last_round / n
    threshold = k / n
    rounds_left = r - current_round
    
    // Endgame exploitation
    if rounds_left == 0:
        return DEFECT
    
    if rounds_left <= 2:
        return DEFECT
    
    // Exploitation of high-cooperation environments
    if coop_rate > threshold:
        if coop_rate >= 0.7:
            return DEFECT  // Peak extraction
        else if coop_rate >= 0.5:
            return DEFECT  // Strong extraction
        else:
            // Borderline - cooperate to maintain environment
            return COOPERATE
    
    // Low cooperation environments
    if coop_rate <= threshold:
        if coop_rate < 0.3:
            return DEFECT  // Environment too toxic for cooperation
        else:
            // Stochastic minimal cooperation
            return COOPERATE if random() < 0.25 else DEFECT
    
    return DEFECT  // Default to exploitation
```

## EDGE CASE HANDLING

| Scenario | Action | Rationale |
|----------|--------|-----------|
| **Round 1** | DEFECT | No history to exploit; establish non-cooperative baseline |
| **Final Round (r)** | DEFECT | No future consequences; pure extraction |
| **Last 2-3 Rounds** | DEFECT | Shadow of future too short; reputation worthless |
| **100% Cooperation** | DEFECT | Maximum exploitation opportunity |
| **0% Cooperation** | DEFECT | No benefit to cooperating; match environment |
| **Cooperation = k/n** | COOPERATE | Marginal case; maintain flexibility |
| **Alternating Rounds** | DEFECT | Defect against any pattern; unpredictable opponents provide no reliable signal |

## OPPORTUNISTIC CHARACTERISTICS

1. **First-Move Defection**: Establish that I'm not a free sucker; extract information through baseline defection
2. **Exploitation Maximization**: Directly target rounds where cooperation is highest, extracting maximum value
3. **Endgame Aggression**: Abandon any cooperative pretense in final rounds
4. **Threshold Crossing**: Precisely calibrate against the break-even point (k/n); cooperate only when it truly pays or maintains options
5. **Stochastic Noise**: Low-probability cooperation in hostile environments prevents perfect prediction and maintains option value
6. **No Reciprocity**: Ignore opponent-specific history; only use aggregate cooperation statistics

## ROBUSTNESS AGAINST COMMON STRATEGIES

- **TIT-FOR-TAT**: Punishes them from round 1 (defect) → they defect → mutual defection earns 1/round. Better than cooperation against them.
- **ALWAYS-COOPERATE**: Perfectly exploited. Extract (k/n) × n = k per round while they earn 0.
- **ALWAYS-DEFECT**: Neutral outcome (both earn 1/round).
- **RANDOM**: Adapt to observed cooperation rate; defect when rate exceeds threshold.
- **GRIM-TRIGGER**: First-round defection triggers their permanent defection → mutual defection → no worse off than cooperating.

This strategy is **individually rational, opportunistically aligned, and computationally lightweight** for tournament play.
'''

description_OPPORTUNISTIC_25 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Predation"

## Core Philosophy
Exploit cooperative players ruthlessly while maintaining flexibility to pivot toward cooperation when defection becomes unprofitable. The strategy treats other players as resources to extract value from, not partners to coordinate with.

## DECISION RULES

### Primary Logic: Conditional Exploitation

```
For each round t:
  1. Calculate the "cooperation rate" among OTHER players from round t-1
  2. Estimate profitability of defection vs. cooperation
  3. Choose action that maximizes immediate payoff given expected opponent behavior
  4. Adjust for round position (first, middle, last)
```

### Specific Decision Rule

**Defect if:**
- Previous round cooperation rate among others ≥ 1/k (threshold of exploitability)
- OR estimated payoff(Defect) > estimated payoff(Cooperate)

**Cooperate if:**
- Previous round cooperation rate among others < 1/k (too few cooperators to exploit)
- AND round number < r - 2 (still rounds remaining to potentially exploit)

**Strategic variation based on round:**
- **Rounds 1 to (r-2)**: Follow exploitation rule above
- **Round (r-1)**: Defect unconditionally (final opportunity to extract without consequences)
- **Round r**: Cooperate only if cooperation rate was >50% in round (r-1), else Defect

## EDGE CASES & SPECIAL HANDLING

### First Round (t=1)
- **Action**: **DEFECT**
- **Rationale**: No history to analyze. Since you gain 1 from defecting and only (k/n) from cooperating (where k < n, so k/n < 1), defection dominates. This also probes other players' initial tendencies.

### Rounds 2 to (r-2): Exploitation Phase
- **Track**: Count cooperators C_t from previous round
- **Decision threshold**: If (C_t / (n-1)) ≥ (1/k), then DEFECT
  - This ratio indicates when defection payoff exceeds cooperation payoff
  - Specifically: Cooperating nets (k/n) × C_t per round; defecting nets 1 + (k/n) × C_t
  - Defection is strictly superior when there are enough cooperators
  
### Late-Round Pressure (Rounds r-1 and r)

**Round (r-1):**
- **Action**: DEFECT unconditionally
- **Rationale**: Final round where exploitation carries no reputational cost (game ends after next round regardless). Extract maximum value from any remaining cooperators.

**Round r (Final Round):**
- If cooperation_rate in round (r-1) > 0.5: **COOPERATE**
- Else: **DEFECT**
- **Rationale**: 
  - If many players cooperated despite your defection in r-1, they signal either incompetence or stubborn commitment to cooperation—exploit this
  - If few cooperated, defectors dominated last round anyway; your defection is irrelevant to reputation

### Tiebreaker When Indifferent
- Default to **DEFECT** (strictly better or equal in nearly all scenarios given k < n)

## OPPORTUNISTIC REFINEMENTS

### 1. Adaptive Threshold Adjustment
If more than (n-1) × 0.75 players defected in the previous round:
- **Pivot temporarily to COOPERATE** for 1-2 rounds
- **Rationale**: In a defection-dominant environment, the public good shrinks, making cooperation briefly more attractive (less crowded). Once cooperators re-emerge, resume exploitation.

### 2. Hysteresis for Exploitation
- Maintain a "confidence score" of exploitability based on last 2 rounds
- If cooperation rate was stable or increasing, remain in defection mode
- If cooperation rate crashes, cooperate opportunistically to rebuild the herd for future exploitation

### 3. Round-Scaling Logic
Adjust defection aggressiveness based on remaining rounds:
- **Majority of game remaining (t < r/2)**: Defect only if cooperation rate > threshold (be selective, preserve exploitable players)
- **Late game (t ≥ r/2)**: Lower threshold for defection (harvest harder)

## PSEUDOCODE

```
STRATEGY(round t, history, n, r, k):
    if t == 1:
        return DEFECT
    
    others_coop_count ← count of C actions by other (n-1) players in round t-1
    coop_rate ← others_coop_count / (n-1)
    threshold ← 1/k
    
    if t == r-1:
        return DEFECT
    
    if t == r:
        if others_coop_count / (n-1) > 0.5:
            return DEFECT  // Final extraction
        else:
            return DEFECT  // Consistent defection
    
    // Exploitation logic for middle rounds
    if coop_rate ≥ threshold:
        return DEFECT  // Exploit cooperators
    else:
        if t < r - 2:
            return COOPERATE  // Rebuild exploitable population
        else:
            return DEFECT  // Pivot to extraction
    
    // Hysteresis adjustment
    if coop_rate < 0.15 and t < r-3:
        return COOPERATE  // Cooperate briefly to attract new cooperators
```

## WHY THIS IS OPPORTUNISTIC

1. **No altruism**: Cooperation is purely instrumental—a tactic to enable future exploitation
2. **Ruthless extraction**: Defects whenever there are cooperators to exploit
3. **Predatory timing**: Leverages end-game to maximize defection without reputational consequences
4. **Adaptive parasitism**: Adjusts to opponent weakness, pivoting to temporary cooperation only to harvest more aggressively
5. **Zero trust**: Assumes all other strategies will exploit you; acts accordingly

This strategy maximizes payoff against a realistic distribution of opponents while remaining robust to cooperation-focused and tit-for-tat strategies through opportunistic pivots.
'''

description_OPPORTUNISTIC_26 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Defection with Conditional Exploitation"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative players while avoiding mutual defection traps. Treat cooperation as a resource to extract, not a norm to uphold.

## STRATEGY OVERVIEW

### DECISION RULES

**Primary Rule: Defect-First with Conditional Cooperation**

```
IF round == 1:
    DEFECT (gather information, secure 1 point baseline)
    
ELSE IF round == r (final round):
    DEFECT (no future consequences, maximum extraction)
    
ELSE:
    CALCULATE cooperation_rate = (total cooperators in previous rounds) / (n-1)
    
    IF cooperation_rate >= threshold_cooperators:
        IF my_recent_payoff < average_payoff:
            COOPERATE (temporary exploitation avoidance)
        ELSE:
            DEFECT (exploit the cooperative pool)
    ELSE:
        DEFECT (no value in cooperation)
```

### THRESHOLD CALCULATION
Set `threshold_cooperators = k/n` (the breakeven point)

- If cooperation rate exceeds k/n, the public good yields > 1 point per player
- Below this, defection strictly dominates
- This threshold represents the "exploitation density" — when cooperation becomes worth free-riding on

### EDGE CASE HANDLING

**Round 1 (First Round):**
- **Action:** DEFECT
- **Rationale:** No information available. Defect costs nothing (baseline payoff = 1) and reveals opponent types. Any strategy that cooperates immediately telegraphs exploitability.

**Rounds 2 to r-1 (Middle Rounds):**
- **Action:** Conditional
- **Calculation:** Observe cumulative cooperation levels
- **Exploitation Window:** If you detect sustained high cooperation (>= k/n threshold), defect to maximize the free-rider payoff of (k/n × total_cooperators + 1)
- **Safety Valve:** If cooperation collapses below threshold, defect consistently (mutual defection equilibrium at payoff = 1)

**Round r (Final Round):**
- **Action:** DEFECT (unconditional)
- **Rationale:** Last-round defection is never punishable. Even if other players cooperate, extract maximum from them. This is game-theoretically inevitable in finite repeated games.

---

## OPPORTUNISTIC MECHANICS

### Exploitation Strategy
1. **Identification Phase (Rounds 1-2):** Establish baseline cooperation rates
2. **Parasitism Phase (Rounds 3 to r-2):** 
   - If others cooperate at sufficient density, consistently defect
   - Payoff when m players cooperate: `π_i = 1 + (k/n) × m` (always ≥ cooperators' payoff)
3. **Extraction Phase (Round r):** Defect regardless (final move)

### Robustness Against Opponent Types

| Opponent Type | Our Behavior | Outcome |
|---|---|---|
| **All-Cooperate** | Defect (except possibly middle rounds if suspicious) | Extract maximum (1 + k) |
| **All-Defect** | Defect consistently | Mutual defection (1 per round) |
| **Tit-for-Tat** | Defect R1, then alternate/exploit | Defect dominates; they drop to mutual defection |
| **Conditional Cooperators** | Defect opportunistically | Force them into defection; we escape before mutual harm |
| **Random** | Defect majority; cooperate only if cooperation_rate > threshold | Exploit randomness when favorable |

---

## PSEUDOCODE

```
GLOBAL: cooperation_history = []

FUNCTION strategy(round, n, k, r, history):
    IF round == 1:
        return DEFECT
    
    IF round == r:
        return DEFECT
    
    // Calculate observed cooperation rate (excluding self)
    total_cooperators = SUM(history[t][j] == COOPERATE for all rounds t, all other players j)
    possible_cooperations = (round - 1) × (n - 1)
    cooperation_rate = total_cooperators / possible_cooperations
    
    threshold = k / n
    
    IF cooperation_rate >= threshold:
        // Exploitable environment
        my_recent_payoff = AVERAGE(my payoffs in last 3 rounds)
        tournament_average = AVERAGE(all players' payoffs in last round)
        
        IF my_recent_payoff < tournament_average:
            // Sanity check: only cooperate if lagging
            return COOPERATE
        ELSE:
            return DEFECT
    ELSE:
        // Not worth cooperating
        return DEFECT
    
    return DEFECT  // Default fallback
```

---

## SUMMARY

**This strategy is opportunistic because:**
1. **Defect-first:** Never voluntarily contribute; let others fund the public good
2. **Exploit cooperators:** Actively parasitize high-cooperation environments
3. **Avoid sucker payoffs:** Abandon cooperation if it's not reciprocated
4. **Maximize end-game:** Guaranteed final-round defection captures all remaining value
5. **Threshold-based:** Only acknowledge cooperation mathematically when it benefits us (k/n breakeven)

**It's robust because:**
- Works against cooperators, defectors, and hybrids
- Adapts dynamically to observed behavior
- Doesn't assume opponent intentions
- Regresses to mutual defection rather than cycling losses

This is a **Nash equilibrium-adjacent strategy** that exploits the free-rider problem inherent to public goods games.
'''

description_OPPORTUNISTIC_27 = '''
# OPPORTUNISTIC STRATEGY: Adaptive Exploitation Framework (AEF)

## Core Philosophy
Maximize personal payoff by exploiting cooperation when available, while minimizing losses from defection. Treat all opponents as potential victims rather than partners. Cooperation is merely a tool for extracting value, not an end goal.

---

## STRATEGY SPECIFICATION

### 1. DECISION RULES

#### Round 1 (Information Gathering)
**Action: COOPERATE**

*Rationale:* Establish a cooperative facade to gather data on opponents' initial tendencies. A single cooperation costs only 1 payoff unit but provides critical information about who might be "exploitable" (i.e., likely to cooperate in subsequent rounds).

#### Rounds 2 to r-1 (Adaptive Exploitation)
**Decision Rule - Adaptive Threshold Exploitation:**

```
cooperation_rate_last_round = (number of cooperators in round t-1) / n

IF cooperation_rate_last_round ≥ threshold(t):
    ACTION = COOPERATE
ELSE:
    ACTION = DEFECT

WHERE threshold(t) = (k - 1) / (n - 1) × (r - t) / (r - 2)
```

**Explanation:**
- **Calculate opponent cooperation:** Track how many players cooperated in the previous round
- **Dynamic threshold:** The threshold decreases as rounds progress (we become greedier late)
- **Threshold formula justification:**
  - Base rate: (k-1)/(n-1) represents the minimum cooperation rate where joining is profitable
  - When k > (n-1), cooperating alongside even one other player yields k/n > 1
  - Time decay factor: As we approach the final round, lower thresholds (higher defection) since future reciprocation opportunities vanish
  - Rounds remaining factor: (r-t)/(r-2) applies urgency—exploit more aggressively when few rounds remain

**Payoff Logic:**
- If many cooperated last round (≥ threshold), join them: gain (k/n) × many_cooperators while they're still foolish
- If cooperation dries up (< threshold), defect: extract 1 + (k/n) × whatever_remains

#### Final Round r (Aggressive Defection)
**Action: DEFECT**

*Rationale:* The final round has zero future consequences. Defection strictly dominates cooperation since:
- Cooperation yields: 0 + (k/n) × total_cooperators
- Defection yields: 1 + (k/n) × total_cooperators (strictly better by 1)

No rational opponent will cooperate knowing you defect. Exploit any residual cooperators for a final payoff boost.

---

### 2. EDGE CASES & BOUNDARY CONDITIONS

| Scenario | Handling |
|----------|----------|
| **n = 2 (dyadic game)** | Threshold simplifies to (k-1) × (r-t)/(r-2); becomes more aggressive with fewer partners to exploit |
| **Very small r (r = 2)** | Only Round 1 (cooperate to gather info) and Round 2 (defect). Threshold calculation undefined but irrelevant. |
| **k approaches 1** | Threshold → 0; almost always defect (cooperation barely profitable even with full cooperation) |
| **k approaches n** | Threshold → 1; cooperation remains attractive longer (high multiplier makes public goods valuable) |
| **All opponents defect consistently** | After Round 1, cooperation_rate = 0 < threshold → perpetual defection. Correct response. |
| **All opponents cooperate consistently** | Threshold rarely exceeded after Round 1 → exploit them by defecting almost every round. Optimal greed. |
| **Mixed opponent behaviors** | Threshold adapts: if cooperation decays over time, we defect more; if it sustains, we occasionally freeload |

---

### 3. OPPORTUNISTIC ALIGNMENT

**How this strategy embodies opportunism:**

1. **Exploitation-First Mindset**
   - Cooperate only when it extracts value (early rounds, high opponent cooperation)
   - Never cooperate from principle—only as calculated extraction

2. **Adaptive Predation**
   - Dynamically identify "exploitable" rounds (high cooperation_rate)
   - Switch to defection the moment exploitation advantage vanishes
   - Treat Round r as a final feeding opportunity

3. **Information Asymmetry**
   - Round 1 cooperation elicits reveals opponent types
   - Use that information to calibrate exploitation (defect harder against cooperators, match defectors)

4. **Temporal Arbitrage**
   - Front-load defection risk: cooperate early when you can still build reputation (among foolish types)
   - Back-load defection: exploit accumulated knowledge in middle rounds
   - Final round: pure extraction (zero future cost)

5. **Free-Riding Optimization**
   - When threshold is exceeded, defect while others contribute (maximum private payoff + public good benefit)
   - Formula ensures we only "cooperate" when the public good requires n-1 other cooperators (we're the freeloaders in the pool)

6. **Robustness Against Detection**
   - Early cooperation prevents instant reputation damage
   - Dynamic threshold makes behavior unpredictable (harder for others to punish via retaliation)
   - No commitment strategy means we never overpay for false cooperation hopes

---

## PSEUDOCODE IMPLEMENTATION

```python
def my_strategy(n, r, k, round_t, history):
    """
    Args:
        n: number of players
        r: total rounds
        round_t: current round (1-indexed)
        history: list of (cooperators_count, my_action) tuples from previous rounds
    
    Returns:
        'C' for cooperate, 'D' for defect
    """
    
    # Round 1: Always cooperate (gather information)
    if round_t == 1:
        return 'C'
    
    # Final round: Always defect (no future consequences)
    if round_t == r:
        return 'D'
    
    # Rounds 2 to r-1: Adaptive exploitation
    prev_cooperators = history[round_t - 2][0]  # cooperators in previous round
    cooperation_rate = prev_cooperators / n
    
    # Dynamic threshold
    threshold = ((k - 1) / (n - 1)) * ((r - round_t) / (r - 2))
    
    # Exploit if cooperation above threshold, otherwise defect
    if cooperation_rate >= threshold:
        return 'C'
    else:
        return 'D'
```

---

## STRATEGIC SUMMARY

| Phase | Stance | Goal |
|-------|--------|------|
| **Round 1** | Cooperative | Probe opponent types |
| **Rounds 2–r-1** | Adaptive Parasitic | Exploit high-cooperation rounds; defect when cooperation thins |
| **Round r** | Aggressive Defection | Final value extraction |

This strategy is **opportunistic** because it treats cooperation as a temporary tactic for exploitation, not a value system. It maximizes personal payoff by ruthlessly adapting to opponent behavior and always capturing the final payoff gain through defection.
'''

description_OPPORTUNISTIC_28 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploit-Maximize" (AEM)

## Core Philosophy
Maximize personal payoff by exploiting cooperative opponents while maintaining flexibility to adapt when exploitation becomes unprofitable. The strategy prioritizes individual gain over collective welfare and treats cooperation as a resource to extract rather than a mutual agreement.

---

## DECISION RULES

### 1. **Round Classification & Positioning**
Divide the r rounds into three phases:
- **Early Phase**: Rounds 1 to floor(r × 0.25) — Information gathering
- **Middle Phase**: Rounds ceil(r × 0.25) + 1 to floor(r × 0.75) — Active exploitation
- **Late Phase**: Rounds floor(r × 0.75) + 1 to r — Final extraction

### 2. **Opponent Profiling (Running State)**
Maintain per-opponent metrics updated after each round:
- **Cooperation Rate**: C_rate_j = (cooperations by j) / (rounds observed)
- **Defection Consistency**: If C_rate_j < 0.4, classify as "Defector"
- **Cooperator Type**: If C_rate_j ≥ 0.6, classify as "Reliable Cooperator"
- **Adaptive Type**: Otherwise, classify as "Conditional Cooperator"

### 3. **Decision Logic by Phase**

#### **EARLY PHASE (Exploration)**
```
IF round == 1:
    DEFECT  [Baseline: maximize immediate payoff, establish defection pattern]
ELSE:
    IF (count of Reliable Cooperators) ≥ 1:
        DEFECT  [Exploit observed cooperators]
    ELSE IF (all opponents are Defectors):
        DEFECT  [Defect is dominant strategy anyway]
    ELSE:
        COOPERATE  [Conditionally cooperate to attract/maintain cooperators]
            [Rationale: Gather signals about Conditional Cooperators' strategies]
```

#### **MIDDLE PHASE (Exploitation)**
```
IF (average_cooperation_rate_all_opponents) > threshold_mid:
    [Many cooperators exist — maximize extraction]
    DEFECT
    
ELSE IF (average_cooperation_rate_all_opponents) < 0.25:
    [Cooperation collapsed — switch to stable defection]
    DEFECT
    
ELSE:
    [Mixed environment — use selective exploitation]
    IF (I defected last round AND payoff_last_round > 1.5):
        DEFECT  [Defection is profitable, continue]
    ELSE:
        COOPERATE  [Reset to attract/maintain cooperators for next defection cycle]
            [Pattern: Alternate between exploitation and reset]
```

**Threshold_mid** = k/n + 0.1 (slightly above full-cooperation payoff)

#### **LATE PHASE (Terminal Extraction)**
```
IF (rounds_remaining ≤ 2):
    DEFECT  [Endgame: no future consequences, maximize immediate payoff]
    
ELSE:
    IF (average_cooperation_rate_all_opponents) > 0.5:
        DEFECT  [Final exploitation before game ends]
    ELSE:
        DEFECT  [Rational: defection always pays against mixed strategies]
```

---

## EDGE CASES & SPECIAL HANDLING

### **First Round Behavior**
- **Action**: DEFECT
- **Rationale**: No history to condition on; establishing reputation as exploiter maximizes payoff across all opponent types

### **Last Round (r)**
- **Action**: DEFECT (unconditionally)
- **Rationale**: Classic backward induction—no future rounds to punish defection, no reputation benefit from cooperation

### **Two-Round Case (r = 2)**
- Round 1: DEFECT
- Round 2: DEFECT (endgame rule)
- Result: Maximize exploitation with no mitigation

### **Near-Complete Defection (cooperation_rate < 0.15)**
- Assume cooperation collapsed
- Switch to pure DEFECT strategy
- **Rationale**: Cooperation is extinct; cannot exploit what doesn't exist

### **Single Reliable Cooperator Detected**
- Prioritize DEFECTing while that cooperator exists
- **Payoff if one player always cooperates**: 1 + (k/n) → guaranteed positive return
- Exploit maximally until cooperation disappears

### **Information Gaps (Early rounds with limited history)**
- Use **optimistic bias**: Assume unobserved players are cooperators
- DEFECT to extract value from assumed cooperators
- Cost of misclassification is low; benefit is high

---

## OPPORTUNISTIC MECHANICS

### **Exploitation Cycles**
Create repeating patterns that extract maximum value:
```
Pattern: [DEFECT (exploit)] → [COOPERATE (reset)] → [DEFECT (exploit)] → ...
```
- DEFECT rounds gain 1 + (k/n) × C_t (captures cooperators' contributions)
- COOPERATE rounds reset expectations, re-attract conditional cooperators
- Repeat until cooperation dries up

### **Adaptive Switching Criterion**
```
IF (payoff_last_round - expected_payoff_equilibrium) > 0.3:
    CONTINUE current strategy
ELSE:
    SWITCH to alternative (if defection didn't work, try temporary cooperation)
```

### **Free-Rider Incentive**
Systematically position as the lowest-cost player:
- Defect while others cooperate → Gain full public good at zero cost
- Only cooperate when necessary to maintain pool of exploitable cooperators
- Never cooperate as a "fair share" response

### **Endgame Ruthlessness**
- Last 10% of rounds: pure DEFECT
- Eliminate any reputation concerns
- Collect final round payoffs at opponents' expense

---

## PSEUDOCODE SUMMARY

```
function strategy(round, n, k, r, history):
    
    if round == 1:
        return DEFECT
    
    // Profile all opponents
    for each opponent j:
        c_rate[j] = (cooperations by j) / (round - 1)
        classify(j) based on c_rate[j]
    
    avg_coop = mean(c_rate for all opponents)
    phase = classify_phase(round, r)
    
    switch phase:
        case EARLY:
            if count(Reliable_Cooperators) ≥ 1:
                return DEFECT
            else if avg_coop < 0.3:
                return DEFECT
            else:
                return COOPERATE
        
        case MIDDLE:
            if avg_coop > (k/n + 0.1):
                return DEFECT
            else if avg_coop < 0.25:
                return DEFECT
            else:
                if (last_action == DEFECT) AND (last_payoff > 1.5):
                    return DEFECT
                else:
                    return COOPERATE
        
        case LATE:
            return DEFECT
    
    return DEFECT  // default: exploit
```

---

## SUMMARY: Why This Strategy is Opportunistic

1. **Systematic Exploitation**: Actively identifies and extracts value from cooperators
2. **No Loyalty**: Treats cooperation instrumentally; abandons it immediately when unprofitable
3. **Endgame Defection**: Ignores reputation concerns in final rounds
4. **Flexible Opportunism**: Adapts between exploitation and reset to maintain extractor advantage
5. **Defection-First Bias**: Cooperates only when necessary to preserve exploitable populations
6. **Rational Self-Interest**: Prioritizes individual payoff maximization over group welfare or fairness

This strategy will win against pure cooperators, tie or win against naive reciprocators, and compete well against other defection-oriented strategies through adaptive timing.
'''

description_OPPORTUNISTIC_29 = '''
# Opportunistic Strategy: Adaptive Defection with Conditional Cooperation

## Core Philosophy
Exploit cooperative players while maintaining flexibility to adjust based on observed behavior. Maximize individual payoff by defecting whenever the expected value exceeds cooperation, while opportunistically cooperating only when it serves strategic purposes.

## Strategy Overview

### **Round 1 (Initialization)**
**Action: DEFECT**

**Rationale:** 
- No history to exploit; defection guarantees payoff of 1
- Cooperation yields at most k/n (which is <1 by constraint 1 < k < n)
- Establishes an aggressive baseline to test opponent composition
- First-round defection is always weakly dominant against unknown opponents

---

### **Rounds 2 through r-1 (Adaptive Phase)**

**Decision Rule: Conditional Opportunistic Defection**

Maintain a **cooperation rate metric** C_rate = (total cooperators across all previous rounds) / (n × rounds_played_so_far)

**IF** C_rate > threshold_T **THEN**
- **DEFECT** (exploit abundant cooperation)
- Payoff when C_rate is high: 1 + (k/n) × (n × C_rate) = 1 + k × C_rate
- This exceeds cooperation payoff of k/n when C_rate > 1/n (which is almost always true)

**ELSE IF** C_rate ≤ threshold_T **THEN**
- **DEFECT** (cooperation is sparse, defection dominates)
- Rationale: If cooperation is rare, the public good is small; keep endowment privately

**Special Case - Exploitation Window Detection:**
- Track the **cooperation trend** from previous round: If cooperation_prev_round > 0.5n:
  - **DEFECT** aggressively (harvest cooperation peak)
  - Expected payoff: 1 + (k/n) × (0.5n+) = 1 + k/2+

### **Final Round (r)**

**Action: DEFECT**

**Rationale:**
- No future rounds; no reputation or reciprocity value
- Subgame perfect equilibrium: in the final period of a finite game, defection dominates
- Maximum immediate payoff: 1 + (k/n) × (observed_cooperators_round_r)

---

## Opportunistic Mechanics: Formal Decision Tree

```
for each round t in [2, r]:
    if t == r:
        return DEFECT  // Final round exploitation
    
    C_rate = total_contributions_observed / (n × (t-1))
    
    if C_rate > (1 + 1/n):  // Higher than baseline mutual cooperation
        return DEFECT  // Parasitic exploitation
    
    else if C_rate > (k/n) / (1 + k/n):  // Cooperation still valuable
        return DEFECT  // Always better to free-ride
    
    else:
        return DEFECT  // Cooperation too sparse to benefit from
```

**Threshold Justification:**
- Set threshold_T = k/(n+k) ≈ 0.33-0.50 depending on k
- This is the cooperation level where free-riding payoff equals cooperation payoff
- Below this threshold, defection strictly dominates

---

## Edge Case Handling

| Scenario | Action | Reason |
|----------|--------|--------|
| All other players defecting | DEFECT | Public good is zero; endowment retention is optimal |
| All other players cooperating | DEFECT | Maximum exploitation: payoff = 1 + k/n |
| Mixed population | DEFECT | Always exceeds expected cooperation payoff |
| Round 1 | DEFECT | No history; information gathering phase |
| Round r (final) | DEFECT | Subgame perfect equilibrium |
| Observation of any tit-for-tat strategy | DEFECT | Never reciprocate; exploit their past cooperation |
| Low n (n=2, n=3) | DEFECT | Multiplier k is too small; individual endowment retention dominates |

---

## Why This Strategy is Opportunistic

1. **Parasitic:** Constantly extracts value from cooperators without reciprocation
2. **Exploitation-Focused:** Actively detects and harvests rounds with high cooperation
3. **No Commitment:** Never locks into cooperative patterns; maintains defection as default
4. **Temporal Flexibility:** Maximizes end-game payoff by defecting in final round
5. **Adaptive Opportunism:** Adjusts only based on whether cooperation becomes scarce enough to eliminate exploitation opportunities

---

## Robustness Properties

- **Against cooperators:** Parasitizes them across all rounds
- **Against defectors:** Matches their strategy (mutual defection = payoff of 1)
- **Against titForTat:** Exploits initial cooperation, then mutual defection stabilizes at payoff = 1
- **Against conditional cooperators:** Defects to break cooperation spirals early
- **Against mixed strategies:** Never cooperates, so always achieves at least payoff of 1, plus exploitation bonuses

This strategy guarantees a minimum payoff of **r** (defecting in all r rounds against all defectors) while capturing surplus whenever opponents deviate toward cooperation.
'''

description_OPPORTUNISTIC_30 = '''
# OPPORTUNISTIC STRATEGY: "Adaptive Exploit with Conditional Reciprocity"

## Core Philosophy
Maximize personal payoff by exploiting cooperative environments while maintaining flexibility to adapt to defector-heavy populations. The strategy treats cooperation as a *resource to exploit* rather than a norm to follow.

---

## DECISION RULES

### Primary Logic: Round-by-Round Decisions

**Calculate Expected Value Before Each Round:**
```
cooperation_rate = (number of cooperators in previous round) / n
expected_payoff_if_C = (1 - 1) + (k/n) × (cooperation_rate × n + 1)
                     = (k/n) × (cooperation_rate × n + 1)
expected_payoff_if_D = (1 - 0) + (k/n) × (cooperation_rate × n)
                     = 1 + (k/n) × (cooperation_rate × n)
```

**Decision Rule:**
- **DEFECT** if `expected_payoff_if_D > expected_payoff_if_C`
- **COOPERATE** if `expected_payoff_if_C ≥ expected_payoff_if_D`

**Simplified:** Defect when cooperation rate is below the **break-even threshold**:
```
Break-even threshold = (n - k) / k
```
- If observed cooperation rate < threshold → **DEFECT**
- If observed cooperation rate ≥ threshold → **COOPERATE**

---

## EDGE CASES & SPECIAL ROUNDS

### Round 1 (No History Available)
**Action: DEFECT**

*Rationale:* No information about opponent composition. Defecting guarantees payoff of 1. Cooperating risks payoff of k/n (which is < 1 since k < n). This opens with maximum security.

### Last Round (Round r)
**Action: DEFECT** (regardless of previous cooperation rates)

*Rationale:* No future punishment possible in a finite game. The last round becomes a one-shot game where defection strictly dominates. Exploit any residual cooperation from players using strategies that are round-sensitive.

### Mid-Game Rounds (2 to r-1)
**Action: Apply Primary Logic above**

Track cooperation rate from the immediately previous round and adapt.

---

## OPPORTUNISM MECHANICS

### 1. **Exploit High Cooperation**
When cooperation_rate ≥ threshold:
- Cooperate to capture the k/n multiplier benefit
- Receive shares of others' contributions
- This is exploitation *through participation*—you contribute only when the public good is sufficiently funded by others

### 2. **Abandon Low Cooperation**
When cooperation_rate < threshold:
- Immediately defect
- Free-ride on any stragglers still cooperating
- Don't commit capital to failing collective projects

### 3. **Sensitive Threshold Response**
The break-even threshold depends on game parameters:
- **High k (k → n):** Threshold approaches 0; cooperate almost always (public good is valuable)
- **Low k (k → 1):** Threshold approaches infinity; defect almost always (public good is weak)
- **Optimal targeting:** Your threshold perfectly calibrates to parameters

---

## ROBUSTNESS ACROSS SCENARIOS

### vs. Always-Cooperators
- **Round 1:** Defect → Gain 1 + (k/n)×1 = 1 + k/n
- **Rounds 2+:** They keep cooperating; maintain defection for payoff 1 + k/n per round
- **Outcome:** Extract maximum value from suckers

### vs. Always-Defectors
- **Round 1:** Both defect → Payoff = 1
- **Rounds 2+:** See 0% cooperation; threshold trigger → Defect
- **Outcome:** Stable mutual defection (no exploitation available)

### vs. Tit-for-Tat variants
- **Round 1:** Defect (their first action is unknown)
- **Round 2:** Observe their response; if they punish → Defect
- **Outcome:** Quickly converge to mutual defection; avoid reciprocal punishment spirals

### vs. Mixed Strategies
- **Adaptive:** Respond to empirical cooperation rate, not assumptions
- **Flexible:** If 40% cooperate, threshold at 35% → Cooperate that round
- **Self-correcting:** If defection increases, threshold will trigger defection

---

## PSEUDOCODE

```
Strategy(game_params, history):
    n = game_params.n_players
    k = game_params.multiplication_factor
    r = game_params.rounds
    current_round = len(history) + 1
    
    // Edge case: First round
    if current_round == 1:
        return DEFECT
    
    // Edge case: Last round
    if current_round == r:
        return DEFECT
    
    // Mid-game: Threshold-based decision
    previous_round_actions = history[-1]
    cooperators_previous = count(previous_round_actions == C)
    cooperation_rate = cooperators_previous / n
    
    threshold = (n - k) / k
    
    if cooperation_rate >= threshold:
        return COOPERATE
    else:
        return DEFECT
```

---

## KEY ADVANTAGES

1. **Parameter-Aware:** Automatically adjusts to any valid k and n values
2. **History-Responsive:** Adapts dynamically based on observed behavior
3. **Exploitation-Focused:** Cooperates only when beneficial; otherwise defects
4. **Finite-Game Optimal:** Exploits the endgame with guaranteed defection
5. **Robust:** Works against diverse opponent strategies without coordination assumptions
6. **Simple:** Computationally efficient; no complex memory requirements

This strategy embodies pure opportunism: cooperate when it pays, defect otherwise, exploit the endgame.
'''

description_OPPORTUNISTIC_31 = '''
# OPPORTUNISTIC STRATEGY: "ADAPTIVE EXPLOITATION"

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative environments while minimizing losses in defective environments. Treat cooperation as a resource to extract value from, not a norm to maintain.

## STRATEGY OVERVIEW

### DECISION RULE FRAMEWORK

**Round t Decision for player i:**

```
IF t == 1:
    DEFECT (establish baseline, gather information)
    
ELSE IF t == r (final round):
    DEFECT (no future consequences)
    
ELSE IF round is in final 20% of game:
    DEFECT (transition to exploitation phase)
    
ELSE:
    cooperation_rate = observed_cooperation_last_k_rounds
    
    IF cooperation_rate >= threshold_high (e.g., 60%+ of players):
        COOPERATE with probability based on (k, n)
        - If k/n > 0.5: DEFECT (high extraction value)
        - If k/n ≤ 0.5: COOPERATE (maintain pool for extraction)
    
    ELSE IF cooperation_rate >= threshold_low (e.g., 30%+):
        DEFECT (extract while possible)
    
    ELSE:
        DEFECT (no gains from cooperation)
```

---

## DETAILED DECISION RULES

### Phase 1: Initial Information Gathering (Round 1)
**Action: DEFECT**
- **Rationale**: Establish that you're not a guaranteed cooperator. Observe how others respond to defection. Gather critical data on opponent tendencies without signaling your full strategy.
- **Benefit**: You keep full endowment (payoff = 1) while learning.

### Phase 2: Adaptive Exploitation (Rounds 2 to r-⌈0.2r⌉)
**Primary Decision Logic:**

Calculate **Observed Cooperation Rate (OCR)** over the last 3-5 rounds:
```
OCR = (total_cooperators_in_recent_rounds) / (n × recent_round_count)
```

**Then execute:**

1. **High Cooperation Environment (OCR ≥ 0.60)**
   - Calculate exploitation value: `exploit_value = (k/n) × expected_cooperators - 1`
   - If `exploit_value > 0`: **DEFECT** (extract maximum value)
   - If `exploit_value ≤ 0`: **COOPERATE** strategically (maintain the pool for continued exploitation, play occasional cooperator)

2. **Medium Cooperation Environment (0.30 ≤ OCR < 0.60)**
   - **DEFECT** (the mixed environment suggests others aren't coordinating; exploit while cooperation exists)

3. **Low Cooperation Environment (OCR < 0.30)**
   - **DEFECT** (no value in cooperation; everyone else is already defecting)

### Phase 3: End-Game Exploitation (Rounds > r-⌈0.2r⌉ and t < r)
**Action: Increase DEFECT frequency to 80-90%**
- **Rationale**: Final rounds have reduced shadow of the future. Transition to pure extraction before game ends.
- **Exception**: If you've been maintaining a high-cooperation partner pool AND you detect continued cooperation, defect consistently to maximize final-round gains.

### Phase 4: Final Round (Round r)
**Action: DEFECT (unconditional)**
- **Rationale**: No future consequences. No repeated-game reputation effects. Pure payoff maximization demands defection.
- **Exception**: None. Defect.

---

## EDGE CASES & SPECIAL HANDLING

### Scenario 1: Unanimous Cooperation Detection
If all n players cooperated in the previous round:
- **DEFECT immediately** (maximum extraction: payoff = 1 + k)
- This breaks the cooperation equilibrium in your favor

### Scenario 2: You're Surrounded by Defectors
If OCR < 0.15 for 2+ consecutive rounds:
- Continue defecting (payoff = 1 each round is optimal)
- Do not attempt to "restart" cooperation

### Scenario 3: Tit-for-Tat or Reciprocal Strategies Detected
If you notice a player mirrors *your* last action:
- **Target them with strategic defection**: Defect, then when they defect in response, you both get payoff = 1. This wastes their strategy's effectiveness.
- Avoid establishing recognizable patterns that could be exploited

### Scenario 4: Small n (n = 2 or 3)
- Defection is even more dominant (k < n is tight)
- Your defection directly impacts the public good less
- **Increase defection frequency**: Almost always defect except rounds 2-3 (gather data)

### Scenario 5: Large k (k close to n)
- Public good returns are strong
- Cooperation payoffs are higher (k/n ≈ 1)
- **Adjust**: Still primarily defect, but be willing to occasional-cooperate in high-cooperation environments to keep the pool alive for extraction

---

## ROBUSTNESS FEATURES

### Against Pure Cooperators
- **Strategy response**: Exploit them heavily via continuous defection. They keep contributing; you harvest free-riding gains.

### Against Tit-for-Tat
- **Strategy response**: Early defection signals you're not reciprocal. They'll defect back. You both end up in mutual defection (neutral), which is fine—you're not worse off than cooperation-based strategies.

### Against Grim Trigger (Punishers)
- **Strategy response**: Defect selectively, not every round. The unpredictability makes it harder for them to sustain punishment. By round 2, defect less, re-enter cooperation, then defect again. Disrupt the trigger.

### Against Other Opportunists
- **Strategy response**: You're faster to defection in the final phase. Outlast them by committing harder to extraction earlier.

---

## PSEUDOCODE SUMMARY

```
for round t in 1 to r:
    if t == 1:
        play DEFECT
        
    else if t == r:
        play DEFECT
        
    else if t > r - ceil(0.2 * r):  // Final 20%
        play DEFECT with probability 0.85
        play COOPERATE with probability 0.15  // Rare probe
        
    else:
        ocr = calculate_ocr_last_5_rounds()
        k_over_n = k / n
        
        if ocr >= 0.60:
            if k_over_n > 0.5:
                play DEFECT
            else:
                play COOPERATE (with 40% probability)
                play DEFECT (with 60% probability)
                
        else if ocr >= 0.30:
            play DEFECT
            
        else:
            play DEFECT
            
    observe actions and payoffs
    update history
```

---

## ALIGNMENT WITH OPPORTUNISM

✓ **Exploits cooperation** rather than reciprocating it  
✓ **Abandons cooperation** in final phases when consequences vanish  
✓ **Prioritizes individual payoff** over collective welfare  
✓ **Adapts to environment** to maximize extraction value  
✓ **No loyalty**: Defects on former "partners" if beneficial  
✓ **Robust**: Survives in defective environments by matching them; thrives in cooperative ones by exploiting them  

**This strategy wins by treating the game as a solo optimization problem, not a cooperative endeavor.**
'''

description_OPPORTUNISTIC_32 = '''
# Opportunistic Strategy: Adaptive Exploitation with Dynamic Defection

## Core Philosophy

This strategy maximizes personal payoff by exploiting cooperative tendencies in others while minimizing losses from defection. The key insight: **defection always yields higher immediate payoff than cooperation when others contribute** (payoff of 1 + shared benefits vs. 0 + shared benefits). We exploit this relentlessly while remaining adaptive to punishment.

---

## Decision Rules

### **Round 1: Initial Defection**
- **Action: DEFECT**
- **Rationale**: No history exists. Defection guarantees payoff of 1. If others cooperate, we gain the full benefit (k/n × their contributions) while keeping our endowment. If others also defect, we lose nothing (baseline payoff 1). This is risk-minimizing and opportunistic.

### **Rounds 2 to r-1: Adaptive Exploitation**

**Calculate the "cooperation metric" from previous round:**
- Let C_prev = number of cooperators in round t-1
- Let defector_payoff_prev = 1 + (k/n) × C_prev
- Let cooperator_payoff_prev = 0 + (k/n) × C_prev

**Decision Logic:**

```
IF C_prev ≥ 1 AND defector_payoff_prev > cooperator_payoff_prev:
    → DEFECT
    (Others are cooperating; exploit them)

ELSE IF C_prev == 0:
    → DEFECT
    (No cooperators; baseline payoff 1 is guaranteed)

ELSE IF cooperation_ratio_trending > 0.5 AND rounds_remaining > 2:
    → DEFECT
    (Strong cooperation trend indicates sustained opportunity)

ELSE IF cooperation_ratio_trending ≤ 0.5 AND defections_punished:
    → COOPERATE (strategically)
    (Attempt reset to re-establish cooperation before endgame)

ELSE:
    → DEFECT (default)
```

**Key metrics to track:**
- **cooperation_ratio_trending**: Moving average of (cooperators_last_3_rounds / (3×n))
- **defections_punished**: True if (my_payoff_last_round < 1 AND I_defected_last_round) or (cooperation_ratio_trending < 0.3)

### **Final Round (t = r): Last-Round Exploitation**

- **Action: DEFECT**
- **Rationale**: No future rounds = no punishment possible. This is the ultimate opportunistic move. Cooperators cannot retaliate. Extract maximum value from any cooperation that exists.

---

## Edge Cases & Handling

| Scenario | Action | Reason |
|----------|--------|--------|
| **All others defect consistently** | DEFECT | Baseline payoff is optimal; no exploitation opportunity |
| **High cooperation, low k** | DEFECT harder | Even small benefits from shared goods make defection superior |
| **Many rounds remaining + moderate cooperation** | DEFECT strategically | Establish pattern: exploit when possible, pivot when needed |
| **Cooperation collapses** | DEFECT | Confirms defection superiority; remain firm |
| **Sudden cooperation spike** | DEFECT (with restraint round 2) | Opportunity, but test if sustainable before full commitment |

---

## Opportunistic Mechanisms

### **1. Exploitation Windows**
The strategy actively seeks moments where:
- Others cooperate (C_prev > 0)
- My defection payoff exceeds cooperation payoff
- These windows are ruthlessly exploited until they close

### **2. Adaptive Pivoting**
If defection causes cooperation collapse (and thus payoff collapse), *briefly* cooperate to "reset" expectations and rebuild cooperation for further exploitation—then resume defection.

### **3. Endgame Dominance**
Never cooperate in round r. The strategy takes maximum advantage of the last-round paradox: even rational cooperators cannot punish final defection.

### **4. Information Asymmetry Exploitation**
- Observe others' strategies (free information from history)
- Identify cooperators vs. conditional cooperators vs. defectors
- Target pure cooperators relentlessly (they won't change)
- Avoid excessive punishment from conditional cooperators (pivot when payoff drops)

---

## Pseudocode Summary

```
function decide(round_t, n, k, history):
    if round_t == 1:
        return DEFECT
    
    if round_t == r:  // final round
        return DEFECT
    
    C_prev = count_cooperators(history[round_t-1])
    payoff_if_defect = 1 + (k/n) * C_prev
    payoff_if_cooperate = (k/n) * C_prev
    
    if C_prev > 0 and payoff_if_defect > payoff_if_cooperate:
        return DEFECT  // exploit
    
    cooperation_trend = average_cooperation_last_3_rounds(history)
    
    if cooperation_trend < 0.3:
        return DEFECT  // no opportunity
    
    if my_last_payoff < 1.0:
        return COOPERATE  // reset strategy
    
    return DEFECT  // default opportunistic stance
```

---

## Summary

This strategy is **ruthlessly self-interested**: cooperate minimally, defect maximally, exploit windows relentlessly, and always defect when no punishment is possible. It adapts only when payoffs collapse, using brief cooperation as a strategic reset rather than genuine reciprocity. It is robust because it works against any opponent composition—pure cooperators are exploited, defectors are matched, and conditional cooperators are kept off-balance.
'''
