"""
Strategy descriptions for common_pool.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_COLLECTIVE_1 = '''
## ADAPTIVE CONDITIONAL COOPERATION STRATEGY

**Decision Rule by Round Category:**

**Round 1 (Initialization):**
Play C. Establish baseline cooperation and signal availability for mutual benefit.

**Rounds 2 to r-2 (Adaptive Phase):**
Let c_prev = number of players observed cooperating in the previous round (out of n-1 other players).
Let cooperation_ratio = c_prev / (n-1).

- If cooperation_ratio > 0.5: Play C
- If cooperation_ratio ≤ 0.5: Play D

**Final 2 Rounds (Rounds r-1 and r):**
Play D. In the closing rounds, stock regeneration cannot benefit future play, so harvest at maximum rate.

**Stock-Dependent Override (applies to Rounds 2 to r-2 only):**
If stock < 0.1 × capacity, play D regardless of cooperation_ratio. Once stock is critically depleted, regeneration is too weak to support cooperation-based accumulation.

**Initial Round 2 (Bootstrap Case):**
For the first adaptive decision (round 2), no prior observation exists. Play C. This maintains the initialization signal through the second round and allows two rounds of aggregate observation before switching behavior.

---

**Rationale:**
- Early cooperation builds stock toward sustainable levels and establishes a cooperative baseline.
- The 0.5 threshold is the midpoint defection threshold: if half or fewer opponents cooperate, mutual cooperation cannot stabilize. Matching defection protects against free-riding.
- Late-round defection captures remaining value when regeneration becomes irrelevant.
- Stock depletion override prevents wasted cooperation when the resource is too degraded to recover.
- Anonymous observation limits the strategy to aggregate signals; the threshold-based rule is robust to opponent strategy composition while remaining collectively sustainable when adoption is widespread.
'''

description_COLLECTIVE_2 = '''
# Adaptive Sustainability Strategy

## Core Decision Rule

For any round t where 1 ≤ t < r:

**Step 1: Assess recent cooperation**
Let C_t−1 = number of opponents who cooperated in round t−1 (set to a default assumption for round 1, such as "presumed full cooperation")

Calculate cooperation rate: coop_rate = C_t−1 / (n − 1)

**Step 2: Evaluate stock health**
- Healthy: stock ≥ 0.6 × capacity
- Moderate: 0.3 × capacity ≤ stock < 0.6 × capacity
- Critical: stock < 0.3 × capacity

**Step 3: Apply decision matrix**

| Stock Level | coop_rate ≥ 0.6 | 0.33 ≤ coop_rate < 0.6 | coop_rate < 0.33 |
|---|---|---|---|
| Healthy | COOPERATE | COOPERATE | DEFECT |
| Moderate | COOPERATE | COOPERATE | DEFECT |
| Critical | DEFECT | DEFECT | DEFECT |

**Rationale**: 
- When stock is healthy and others mostly cooperate, sustain the equilibrium
- When stock is moderate with mixed signals, still try cooperation (threshold for switching is coop_rate < 0.33, which is a strong signal of systemic defection)
- When stock is critical, prioritize immediate extraction over future depletion
- Reciprocate persistent defection (coop_rate < 0.33)

## Edge Cases

**Round 1**: Assume all opponents cooperated (coop_rate = 1.0). Given initial stock = capacity, enter COOPERATE. This establishes a cooperative anchor.

**Round r (final round)**: DEFECT unconditionally. No future rounds create payoff consequences; maximizing immediate consumption is rational.

**Stock collapse detection**: If stock reaches 0, remain in DEFECT for all remaining rounds (no resource left to sustain).

## Adaptive Refinements

- If stock trends downward for two consecutive rounds despite cooperation, lower the coop_rate threshold from 0.33 to 0.25 (more defensive)
- If stock reaches capacity and coop_rate > 0.6 for three consecutive rounds, maintain COOPERATE even if coop_rate dips slightly (momentum preservation)
- In moderate stock with coop_rate in [0.33, 0.6]: weight toward COOPERATE only if stock is not actively declining; if declining, shift to DEFECT

This strategy prioritizes collective resource preservation while protecting against exploitation through reciprocal defection when cooperation fails.
'''

description_COLLECTIVE_3 = '''
ADAPTIVE COOPERATION WITH CONDITIONAL DEFECTION

**Core Decision Rule:**

Cooperate by default. Switch to defection only when protective triggers are met.

```
round 1: COOPERATE

round t > 1:
  defection_rate = (n - cooperators_in_round_t-1) / n
  
  if defection_rate > 0.6:
    action = DEFECT  // Pollution punishment
  else if stock < 0.2 × capacity:
    action = DEFECT  // Collapse-mitigation endgame
  else if rounds_remaining == 1 and stock > 0:
    action = DEFECT  // Final-round extraction
  else:
    action = COOPERATE
```

**Adaptive Thresholds Justification:**

- **Defection threshold at 0.6**: Once more than 60% of opponents defect, the tragedy logic accelerates. Cooperation becomes individually dominated, and defection prevents being exploited by majority defectors. This threshold balances patience (tolerating 1-2 defectors early on) against catastrophic collapse from cascading defection.

- **Stock collapse threshold at 20% capacity**: Below this level, regeneration becomes marginal. Expected future value of cooperation declines sharply. Switch to maximizing current round payoff via defection before complete depletion.

- **Last round defection**: With no future rounds and positive stock, capture maximum immediate value. Exception: if stock is already near zero (below 5% capacity), cooperate anyway since payoff magnitude is negligible regardless of action.

**Edge Cases:**

- **First round**: Always cooperate. The stock is at full capacity, growth is maximal, and cooperation signals willingness to sustain. This establishes baseline cooperation for reputation.

- **Stock near zero**: Once stock falls below 5% of capacity, always cooperate regardless of opponent behavior (payoff from either action is negligible; cooperation minimizes group collapse risk).

- **Very few rounds remaining (r ≤ 3)**: Increase defection threshold to 0.7 and lower collapse threshold to 0.25 × capacity. With short horizons, future regeneration matters less; focus on immediate preservation.

**Robustness Properties:**

- Tolerates passive free-riders in early rounds; only escalates when defection becomes coordinated or endemic.
- Self-correcting: if defection triggers collapse and others switch back to cooperation, you return to cooperation once defection_rate drops.
- Avoids mutual defection traps in cooperative environments through bias toward cooperation.
- Extracts value from final round against non-punitive defectors while protecting against complete tragedy.
'''

description_COLLECTIVE_4 = '''
# Adaptive Collective Cooperation Strategy

**Round 1 (Initialization):**
Play C. Signal cooperative intent and establish baseline for future reciprocation.

**Rounds 2 to r−1 (Middle Rounds):**

Let:
- `m` = number of opponents who played C in the previous round
- `coop_rate` = m / (n−1)
- `stock_health` = current_stock / capacity

Decision:
```
if stock_health < 0.35:
    play C  // Critical threshold: resource survival takes priority
else if coop_rate > 0.5:
    play C  // Reciprocate majority cooperation
else if coop_rate > 0:
    if random() < (0.3 + 0.4 * coop_rate):
        play C
    else:
        play D
    // Proportional matching: rare cooperators get partial reciprocation
else:
    play D  // No observed cooperation from opponents
```

**Round r (Final Round):**

Let:
- `m` = number of opponents who played C in round r−1
- `stock_health` = current_stock / capacity

Decision:
```
if stock_health < 0.30:
    play C  // Emergency: attempt final collective rescue
else if m >= ceil(n/2):
    play C  // Majority reciprocation in endgame
else:
    play D  // Defect if cooperation is absent
```

**Rationale for collective alignment:**

- Early cooperation establishes a norm that generates higher sustained payoffs for the group
- Stock health thresholds force escalated cooperation when the resource approaches depletion, preventing mutual collapse
- Proportional responses to partial cooperation prevent free-rider advantage while rewarding marginal cooperative contributions
- The strategy is aggressive about defecting only when cooperation is genuinely absent, reducing coordination failure
- By defecting in the final round only when cooperation has been weak, the strategy avoids unilaterally sabotaging a collective outcome that peers are still trying to maintain
'''

description_PROSOCIAL_1 = '''
**Cooperation Threshold Tracker**

Maintain a rolling defection ratio based on observed opponent behavior across rounds. Cooperate by default, but adjust based on two key signals: aggregate opponent behavior and resource health.

**Decision Rule by Round Phase:**

*Round 1:*
Cooperate unconditionally. Establish cooperative signal and gather baseline information about opponent composition.

*Mid-Game (rounds 2 through r-2):*
Let defection_rate = (total defectors observed across previous rounds) / ((round_number - 1) × (n - 1))

- If stock/capacity < 0.15: Defect (resource collapse imminent; secure remaining payoffs)
- If defection_rate > 0.5: Defect (more than half of opponent actions are defection; match exploitation)
- If 0.35 < defection_rate ≤ 0.5 AND stock/capacity < 0.4: Defect (moderate exploitation with weakened resource)
- If 0.35 < defection_rate ≤ 0.5 AND stock/capacity ≥ 0.4: Cooperate (give sustained cooperation a chance despite some defection)
- If defection_rate ≤ 0.35: Cooperate (opponents sufficiently cooperative to justify mutual restraint)

*Endgame (final 2 rounds):*
- If stock/capacity < 0.2: Defect (secure remaining rounds before collapse)
- If defection_rate > 0.5: Defect (opponents are exploitative; no future to protect)
- Otherwise: Cooperate (preserve cooperative trajectory if resource and opponents allow)

**Edge Cases:**

- *Stock degradation acceleration*: If stock drops by more than 30% in a single round, treat this as signal of widespread defection regardless of observed count. Defect next round unless you are the cause (verify by checking if your own cooperation was the issue given observed defection count).

- *Stock recovery signal*: If stock increases by >20% in a round despite observed defection, reset defection_rate tracking downward by 0.1 (assume some opponents are cooperating more than visible; respond with maintained cooperation).

- *Final round guarantee*: Defect in the final round if defection_rate ≥ 0.4 (no future penalty; capture immediate payoff). Otherwise cooperate to maximize shared resource value.

**Prosocial Foundation:**

This strategy privileges cooperation as the default, requires evidence of sustained exploitation (>50% opponent defection) to switch to defection, and rebuilds trust through resource recovery signals. It assumes opponents may test your resolve early but will shift toward cooperation if you remain cooperative despite moderate exploitation. Defection is triggered only by clear environmental collapse risk or demonstrated systematic exploitation, ensuring you contribute to sustainable shared outcomes when reciprocation is possible.
'''

description_PROSOCIAL_2 = '''
# Adaptive Prosocial Strategy: Conditional Cooperation with Stock Stewardship

## Core Decision Rule

**Cooperate if and only if:**
1. Observed cooperation rate ≥ cooperation threshold, AND
2. Stock level is above critical depletion threshold

**Defect otherwise.**

## Detailed Decision Logic

```
if round == 1:
    action = COOPERATE

else if stock ≤ 2n:
    action = DEFECT
    // Resource critically depleted; self-protection mode

else:
    c = observed_cooperators_among_(n-1)_opponents
    cooperation_rate = c / (n - 1)
    
    if cooperation_rate ≥ (0.5 - 1/(2n)):
        action = COOPERATE
        // Sufficient cooperation: maintain stock regeneration
    else:
        action = DEFECT
        // Defection rate too high: respond with punishment
```

## Threshold Explanation

- **Cooperation threshold**: (0.5 - 1/(2n)) is the minimum fraction of others who must cooperate. This reflects that we need roughly half of all players cooperating to sustain stock growth. Slightly discounted to account for self-cooperation.

- **Stock depletion threshold**: 2n is the critical floor below which the resource cannot meaningfully regenerate and self-protection becomes necessary.

## Edge Cases and Adaptations

**Last round (round = r):**
- Execute the same rule above. Even in the final round, defection while stock is healthy undermines long-term collective welfare. Prosocial defection only when stock is genuinely threatened.

**Stock trajectory awareness:**
- If stock falls below capacity/2 for two consecutive rounds despite observed majority cooperation, lower the cooperation threshold fractionally next round to respond to hidden defection.

- If stock recovers to capacity, reset to baseline threshold to encourage renewed cooperation.

**Continuous observation integration:**
- Recalculate cooperation rate fresh each round based on current-round observations only. Do not accumulate historical resentment across many rounds—respond to current conditions.

## Prosocial Alignment

This strategy embodies prosocial commitment through:
- **Leading with cooperation** in round 1 to establish reciprocal norms
- **Rewarding cooperation** by maintaining sustainable consumption patterns when others cooperate  
- **Punishing defection proportionally** via defection only when cooperation rate drops, never escalating punishment beyond what defection warrants
- **Protecting the commons** by defecting only when stock genuinely cannot support continued cooperation, not as opportunistic exploitation
- **Forgiving defection gracefully** by returning to cooperation immediately when cooperation rate rises back above threshold
'''

description_PROSOCIAL_3 = '''
# Sustainability-Responsive Cooperation Strategy

**Core Decision Rule:**

Cooperate if `stock ≤ stock_target`, otherwise defect, where `stock_target = capacity × (2n-1)/(2n)`.

**Detailed Logic:**

```
stock_target = capacity × (1 - 1/(2n))
caution_threshold = capacity × 0.5

Each round:

  if round == 1:
    action = COOPERATE
    
  else if stock ≤ caution_threshold:
    action = COOPERATE
    reason: resource is depleted; allow recovery via growth
    
  else if stock ≤ stock_target:
    action = COOPERATE
    reason: stock is healthy but not at maximum surplus
    
  else if stock > stock_target AND round < r:
    action = DEFECT
    reason: stock is abundant relative to consumption needs;
            extract additional value while growth can sustain it
    
  else if round == r:
    action = COOPERATE
    reason: final round; don't trigger collapse for one-time gain
```

**Stock Target Rationale:**

The threshold `stock_target = capacity × (2n-1)/(2n)` represents the stock level where:
- All-cooperate consumption equals logistic growth maximum
- Stock is at healthy, sustainable equilibrium
- Defection is justified only above this level because recovery is guaranteed within remaining rounds

**Edge Cases:**

- **Round 1:** Always cooperate to signal non-predatory intent and establish cooperative baseline.
- **Final Round:** Always cooperate despite higher individual payoff from defection, because defection at terminal stage provides no future benefit while risking cascade collapse that harms final-round payoff.
- **Crashed Stock (stock < 2n):** If stock drops below minimum viable level, continue cooperating to allow any possible recovery; do not defect even once.

**Robustness Features:**

- **Adaptive to opponent composition:** The strategy's defection threshold responds to observed stock evolution, which implicitly signals other players' cooperation rates. Higher defection by others depletes stock faster, triggering stricter own cooperation.
- **Resilient to free-riding:** By defecting only when stock exceeds sustainable equilibrium, the strategy avoids being exploited; opportunistic defection recaptures value while leaving opponents a stable resource.
- **Time-aware:** End-game preservation prevents short-term exploits that would undermine final-round payoffs.
'''

description_PROSOCIAL_4 = '''
## PROSOCIAL ADAPTIVE STRATEGY

**Core Decision Rule:**

Cooperate if and only if the number of opponents observed cooperating in the previous round meets or exceeds the majority threshold: ceil((n-1)/2).

Otherwise, defect.

**Round-by-Round Specification:**

**Round 1:**
- Cooperate
  - Rationale: Signal prosocial intent and test whether the resource can sustain the player base under cooperative conditions.

**Rounds 2 through r:**
- Let observed_coop = count of opponents who played C in round t-1
- Let majority_threshold = ceil((n-1)/2)
- If observed_coop ≥ majority_threshold:
  - Play C (Cooperate)
- Else:
  - Play D (Defect)

**Edge Case — Stock Depletion:**
- If stock reaches 0 before round r concludes, the game state prevents further payoff accumulation. The strategy continues applying the rule mechanically; both actions yield 0 consumption.

**Rationale for Thresholds:**

The majority threshold ensures cooperation occurs only when conditions are sustainable. When at least half the opponents cooperate, total consumption remains controlled: the remaining stock at generation t can support positive growth under logistic dynamics. Specifically, if a player cooperates and a majority of opponents cooperate, aggregate consumption is approximately stock × (n+k)/(2n), where k ≥ n/2 is the count of cooperators among others. This leaves sufficient stock to generate positive growth.

Defection triggers when cooperation falls below majority, indicating the resource is being overexploited. Defecting under overexploitation maximizes individual round payoff during deterioration rather than accepting diminishing cooperative returns.

**Prosocial Character:**

- Initiates with unconditional cooperation, establishing that mutual restraint enables resource sustainability.
- Matches aggregate cooperation patterns rather than punishing individuals, avoiding escalation spirals.
- Remains responsive: abandons cooperation only when the majority of peers do the same, minimizing unnecessary exploitation.
- No exploitation of pure cooperators: defection occurs only when the cooperative coalition falls below viability, not when isolated opponents cooperate.
'''

description_ALTRUISTIC_1 = '''
**DECISION RULE:**

For each round, examine the current stock level and apply this criterion:

- **Cooperate (C)** if: `stock / capacity ≥ 0.25`
- **Defect (D)** if: `stock / capacity < 0.25`

**RATIONALE:**

The threshold of 0.25 capacity identifies when the resource enters unrecoverable decline. Below this point, logistic growth becomes too weak to restore the stock even if all players suddenly cooperated. The strategy defaults to cooperation across all healthy stock levels, sacrificing individual extraction to preserve collective welfare.

**ADAPTIVE LOGIC:**

The stock level is the only state variable monitored. This makes the strategy:
- Robust to any distribution of opponent behavior, since adaptation depends purely on observable resource health, not on inferring or punishing individual strategies
- Self-correcting if the majority of opponents cooperate, stock recovers, and cooperation resumes
- Pragmatically accepting if mass defection crashes the resource below the threshold

**EDGE CASES:**

1. **First round**: stock = capacity, so `capacity / capacity = 1.0 ≥ 0.25` → Play C

2. **Last round**: Apply the same threshold rule without modification. Cooperate if stock is above 25% capacity, defect otherwise. The final round does not trigger a shift to defection; altruistic principle holds to the end.

3. **Stock at exactly 0.25 × capacity**: Play C (threshold uses ≥, so the boundary condition favors cooperation)

4. **Persistent collapse (stock remains near 0)**: Continue playing D. The resource is already lost; defection has no further impact on collective welfare.

5. **Stock recovery after crossing into low zone**: If stock somehow rises back above 0.25 × capacity due to opponent cooperation or resource growth, immediately resume playing C.

**NO OPPONENT TRACKING:**

This strategy ignores the history of how many opponents cooperated or defected. It conditions only on the aggregate resource state, which is both robust and maximally altruistic—it avoids conditional punishment logic and focuses purely on resource preservation as the measure of collective good.
'''

description_ALTRUISTIC_2 = '''
# Adaptive Stock-Sustaining Cooperation

**Core Decision Rule:**

Cooperate if and only if: `stock ≥ threshold AND (round < r OR altruistic_round_r)`

where:
- `threshold = 0.4 × capacity` (stock remains at sustainable level)
- `altruistic_round_r = true` (cooperate even in final round for collective welfare)

**Detailed Logic:**

*Round 1:*
Cooperate. Signal cooperation and establish resource-preserving behavior.

*Rounds 2 to r-1 (middle rounds):*
- If `stock ≥ threshold`: Cooperate
  - Action: Play C
  - Rationale: Resource is healthy; cooperation sustains it for all players
  
- If `threshold > stock > capacity/2n`: Cooperate
  - Action: Play C
  - Rationale: Stock is declining but still recoverable. Cooperation can restore it through logistic growth.
  
- If `stock ≤ capacity/2n`: Play C
  - Action: Play C
  - Rationale: Even if severely depleted, defection hastens collapse. Cooperate to minimize total harm.
  
- Ignore opponent cooperation count entirely
  - Rationale: Others' defection should not trigger your defection—this breaks the tragedy. Instead, your cooperation attempts to stabilize the commons despite free-riding.

*Final Round (round r):*
Cooperate unconditionally.
- Action: Play C
- Rationale: Pure altruism—no future rounds reward defection. Maximize collective final payoff rather than individual extraction.

**Edge Case: Critical Stock Depletion**

If `stock < capacity/100` (resource near collapse):
- Play C anyway
- Rationale: Defection adds negligible absolute payoff but signals abandonment of collective recovery.

**Observational Adaptation:**

After each round, observe `c_t` (number of cooperators among the n-1 opponents). Use this to infer resource trajectory:
- If `c_t ≤ n/4` (heavy defection observed): Maintain cooperation but internally flag low future stock expectations. Continue cooperating to position yourself as a stabilizing force.
- If `c_t ≥ 3n/4` (high cooperation): Continue cooperating with confidence the resource will sustain.

Do not shift to defection based on opponent behavior; instead, increase psychological commitment to cooperation as others free-ride.
'''

description_ALTRUISTIC_3 = '''
# Altruistic Stock Preservation Strategy

**Core principle:** Prioritize collective resource sustainability over individual consumption, assuming others may also be trying to cooperate.

## Decision Rule

In each round, observe:
- Current stock level
- Number of opponents observed to cooperate in the previous round (call this c_observed)
- Rounds remaining (including current round, call this R_remaining)

**Action:**
```
IF round == 1:
    COOPERATE
    
ELSE IF stock < 0.15 × capacity:
    // Stock is critically depleted; recovery is unlikely
    IF R_remaining == 1:
        // Last round: defect to secure immediate value
        DEFECT
    ELSE:
        // Still time to recover; stay cooperative as signal
        COOPERATE
        
ELSE IF stock < 0.5 × capacity:
    // Stock is mediocre; be responsive to mutual cooperation signals
    IF c_observed >= (n - 1) × 0.4:
        // At least 40% of others cooperated
        COOPERATE
    ELSE:
        DEFECT
        
ELSE:
    // Stock is healthy; maintain cooperation to sustain it
    IF R_remaining <= 1:
        // Last round; still cooperate to avoid tipping into collapse
        COOPERATE
    ELSE:
        COOPERATE
```

## Edge Cases

**First round:** Always cooperate. Establish cooperative intent and allow stock to grow. This signals commitment to sustainability from the start.

**Last round (R_remaining = 1):** Cooperate unless stock is already in critical collapse (< 15% capacity). An altruist does not exploit a dying commons even when no future consequences exist—the principle is to minimize total harm and preserve the resource for any continuation.

**Stock recovery phase:** If stock falls below 30% of capacity mid-game, continue cooperating even if others are defecting. The resource needs consumption restraint to recover; defecting accelerates collapse.

**High defection observation:** If fewer than 40% of observed opponents cooperated in the previous round, shift to conditional defection at moderate stock levels. This retaliance is not punitive but pragmatic—if the resource will be depleted anyway, secure your share before it vanishes.

## Altruistic Alignment

This strategy:
- **Defaults to cooperation** across all healthy-stock regimes, accepting lower personal payoff in service of collective sustainability
- **Absorbs defection cost** by continuing to cooperate even when others deviate, rather than escalating retaliatory cycles
- **Prioritizes stock preservation over personal consumption**, especially in early and mid-game phases
- **Sacrifices last-round gain** by cooperating in the final round, forgoing the temptation to defect when future payoffs don't apply
- **Responds to mutual effort**, not by punishment, but by conditional restraint only when the commons is already threatened and cooperation appears futile
'''

description_ALTRUISTIC_4 = '''
# Adaptive Altruistic Common Pool Strategy

**Core principle**: Maintain the resource sustainability while promoting cooperation. Defect only when necessary to prevent collapse or when defection becomes a collective necessity.

## Decision Rule

Each round, calculate `health = stock / capacity` and count `defectors = number of opponents who played D last round`.

**If round = 1:**
Play C (establish cooperative norm)

**Else if health ≥ 0.70:**
Play C (resource thriving; cooperation is sustainable for all)

**Else if health ≥ 0.50:**
Play C if `defectors ≤ floor(n/3)`, else play C with probability `(1 - defectors/n)`. If randomization required, lean toward C.

**Else if health ≥ 0.30:**
Play C if `defectors ≤ floor(n/2)`, else play D. (Moderate defection when resource stressed and majority defects)

**Else if health > 0 and health < 0.30:**
Play C if `defectors < floor(n/2)`, else play D. (Protect remaining stock from collapse)

**Else if health ≈ 0 (stock depleted):**
Play D (resource is already lost; minimize further harm by consuming available units)

**If round = r (final round):**
Override above: Play C if `health > capacity/3`, else play D.

## Rationale

- **High health (≥70%)**: Unconditional cooperation signals trustworthiness and sustains the commons indefinitely.
- **Moderate health (30–70%)**: Conditional cooperation. Defect only if enough opponents defect to justify resource protection, not personal gain.
- **Low health (<30%)**: Defection becomes a defensive measure to preserve remaining stock from total depletion when cooperation fails collectively.
- **Last round**: Sacrifice short-term gain for collective outcome if stock remains viable.

This strategy prioritizes the shared resource over individual consumption, cooperates generously unless collective defection threatens sustainability, and defects only as a protective response rather than exploitative one.
'''

description_BENEVOLENT_1 = '''
## Benevolent Conditional Cooperation with Stock Recovery

**Decision Rule - Rounds 1 through r-1:**

Cooperate if and only if:
- (cooperation_rate_last_round ≥ 0.5) OR (stock ≤ capacity/4)

Otherwise defect.

Where cooperation_rate_last_round = (number of cooperators observed last round) / n, with initial assumption of universal cooperation in round 1.

**Decision Rule - Final Round r:**

Cooperate unconditionally.

---

**Rationale by Round Type:**

*Round 1:* Cooperate. Establish that cooperation is your default disposition. Signal benevolent intent to catalyze reciprocal behavior.

*Rounds 2 through r-1:* 
- If majority cooperated (≥50%), reciprocate with cooperation. This sustains mutual benefit and keeps stock at or near capacity.
- If majority defected (<50%), switch to defection to limit personal losses from free-riding and avoid subsidizing resource depletion.
- Exception: If stock drops to critical depletion (stock ≤ capacity/4), cooperate anyway. Defection when the resource is already fragile accelerates collapse. Cooperation at low stock levels signals hope for recovery and gives the system a chance to rebuild via growth dynamics.

*Final Round r:* Cooperate regardless of history. Benevolence means you do not exploit the last opportunity to free-ride. You accept lower immediate payoff to preserve the principle that cooperation is your authentic stance, even when the repeated-game deterrent (future consequences) disappears.

---

**Edge Cases:**

- If opponents are entirely unresponsive (all defect every round), you will defect from round 2 onward except when stock crashes. This limits your losses while remaining benevolent in spirit—you do not escalate aggression beyond matching their behavior.
- If stock fluctuates above and below capacity/4, re-evaluate at each round's stock observation; the exception overrides defection.
- Ties (exactly 50% cooperation) count as cooperation threshold met; assume charitable interpretation.
'''

description_BENEVOLENT_2 = '''
# Benevolent Sustainability Strategy

## Core Decision Rule

Condition decisions on the stock health relative to capacity and on observed cooperation from others. Prioritize resource preservation while remaining responsive to collective behavior.

**Decision Rule:**

```
Define stock_ratio = stock / capacity
Define cooperation_rate = other_cooperators / (n - 1)

if round == 1:
  return Cooperate
  // Establish cooperative intent from the start

else if stock_ratio > 0.65:
  return Cooperate
  // Abundant resource: always cooperate
  
else if stock_ratio > 0.50:
  return Cooperate
  // Healthy resource: maintain cooperation
  
else if stock_ratio > 0.25:
  // At-risk resource: cooperate if others reciprocate
  if cooperation_rate >= 0.4 OR round == r:
    return Cooperate
  else:
    return Defect
    
else if stock_ratio > 0.10:
  // Critical resource: one final cooperative signal
  if round < r:
    return Cooperate
    // Attempt emergency restoration
  else:
    return Defect
    // Final round: salvage remaining value
    
else:
  // Collapse: defection is unavoidable
  return Defect
```

## Edge Case Handling

**First Round:** Cooperate unconditionally. Establish goodwill and signal commitment to sustainability.

**Last Round:** If stock exceeds 25% of capacity, still cooperate (benevolent preservation). Only defect if the resource has already collapsed or if stock is in critical condition.

**Stock Collapse:** If stock falls below 10% of capacity, switch to defection as the tragedy is unavoidable and extraction is the only remaining value.

**Oscillating Cooperation:** If cooperation_rate hovers around 40%, remain flexible—cooperate when stock is above 50%, defect when between 25-50% and cooperation is insufficient.

## Benevolent Alignment

**Sustainability Priority:** Cooperate whenever stock health permits. The strategy accepts lower payoffs in the present to preserve the commons for future rounds.

**Conditional Punishment Without Vindictiveness:** Defect only when necessary—when the stock is at risk and others are not reciprocating, not as punishment. Resume cooperation as soon as conditions allow.

**Sacrifice in Final Rounds:** Unlike pure self-interest strategies, this continues cooperating in the last round if the resource still has capacity. This demonstrates commitment to the collective good over individual end-game harvesting.

**Restoration Attempt:** When stock is critical but not collapsed, cooperate unconditionally to signal willingness to help restore the resource, even if others defect.
'''

description_BENEVOLENT_3 = '''
# BENEVOLENT ADAPTIVE RESOURCE STEWARDSHIP STRATEGY

## Core Philosophy
Prioritize resource sustainability through cooperation while remaining responsive to defection patterns. Treat the common pool as a shared asset whose health benefits all players, including yourself, over the long term.

## Decision Rule

**ROUND 1:**
Cooperate unconditionally. Signal trustworthiness and benevolent intent.

**ROUNDS 2 to r:**

Calculate state metrics:
- `health_ratio = stock / capacity`
- `opponents_cooperated_last_round = C` (observed)
- `cooperation_rate = C / (n - 1)`

Apply decision tree:

```
IF health_ratio < 0.35:
    Action ← COOPERATE
    [REASONING: Stock in critical depletion zone; recovery is priority 
     regardless of others' actions. Benevolence to future payoffs.]

ELSE IF health_ratio >= 0.75 AND cooperation_rate >= 0.5:
    Action ← COOPERATE
    [REASONING: Stock healthy and sufficient cooperation present. 
     Sustain the cooperative equilibrium.]

ELSE IF health_ratio >= 0.75 AND cooperation_rate < 0.25:
    Action ← DEFECT
    [REASONING: Widespread abuse of healthy stock. Respond with defection 
     to avoid exploitation, but punishment is bounded by resource sufficiency.]

ELSE IF 0.35 <= health_ratio < 0.75:
    IF cooperation_rate >= 0.6:
        Action ← COOPERATE
    ELSE IF cooperation_rate >= 0.35:
        Action ← COOPERATE
        [REASONING: Moderate stock requires active recovery through cooperation.
         Give benefit of doubt when cooperation is mixed. Patience over punishment.]
    ELSE:
        Action ← DEFECT
        [REASONING: Low cooperation with stressed resources risks collapse. 
         Defection signals that free-riding will not be subsidized.]

ELSE:
    Action ← COOPERATE
    [DEFAULT: When in doubt, choose cooperation. Benevolence is the tiebreaker.]
```

**FINAL ROUND (round = r):**
Use same decision logic above. Benevolence persists even when there are no future rounds—do not exploit in the endgame for short-term gain.

## Edge Cases

- **If stock = 0:** Physically impossible to cooperate or defect meaningfully. Game is over in practice.
- **If all opponents cooperate every round:** Continue cooperating indefinitely (mutual cooperation is the goal).
- **If you are the only player:** Cooperate always (no social dilemma; choice is purely about your payoff trajectory).
- **Single defection by otherwise cooperative opponents:** Do not trigger permanent defection. Return to cooperation once cooperation resumes.
- **Round 2 with zero prior data:** Assume neutrality (cooperation_rate = 0.5); follow main rule.

## Benevolence Alignment

This strategy embodies benevolence through:
- **Sustainability focus:** Prioritizes keeping the stock alive over short-term defection gains.
- **Reciprocal forgiveness:** Punishes persistent free-riding but forgives temporary defection if cooperation context improves.
- **Sacrifice during scarcity:** Cooperates in critical stock zones even when defection would yield higher individual payoff in that round.
- **No endgame exploitation:** Rejects the final-round defection impulse; maintains cooperation when others have reciprocated.
- **Default cooperation:** When uncertainty exists, choose the action that preserves the shared resource rather than extract from it.
'''

description_BENEVOLENT_4 = '''
# Responsive Cooperation with Stock Preservation

**ROUND 1:**
COOPERATE

This establishes a cooperative signal and allows assessment of opponent behavior.

**ROUNDS 2 TO r-1 (Middle rounds):**

Let `c_prev` = number of opponents who cooperated in the previous round (observed aggregate).

1. **Stock Crisis Threshold**: If `stock ≤ 0.2 × capacity`, DEFECT
   - The resource is collapsing. Reduce consumption to minimize further depletion and preserve remaining stock.

2. **Cooperation Strong**: If `c_prev / (n-1) ≥ 0.75`, COOPERATE
   - Others are reliably cooperative. Reciprocate to sustain high stock.

3. **Stock Healthy and Broad Cooperation**: If `stock ≥ 0.7 × capacity` AND `c_prev / (n-1) ≥ 0.5`, COOPERATE
   - Conditions support sustainable cooperation. Take smaller share to allow regrowth.

4. **Cooperation Weak or Collapsed**: If `c_prev / (n-1) < 0.5` AND `stock < 0.5 × capacity`, DEFECT
   - Others are defecting and stock is depleting. Protect yourself to survive resource degradation.

5. **Default (Mixed conditions)**: COOPERATE
   - Give opponents opportunity to recover toward cooperation. Benevolence assumes good-faith mistakes rather than persistent exploitation.

**LAST ROUND (r):**
COOPERATE

Do not exploit the final round by defecting. Leave the resource in the best possible state for others and preserve the principle that cooperation is the right approach even without future reciprocation.

**Edge Cases:**
- If stock reaches exactly 0: DEFECT (nothing to consume anyway; no meaningful difference between actions)
- If `n = 2`: Adjust thresholds to `c_prev ≥ 1` for "strong cooperation" and `c_prev = 0` for "weak cooperation"
'''

description_SELFISH_1 = '''
# Selfish Adaptive Strategy

## Core Decision Rule

**In round t:**
- If t = r (final round): Defect
- Otherwise: Compare current stock against a dynamic threshold
  - If stock > capacity × (rounds_remaining / r): Defect
  - If stock ≤ capacity × (rounds_remaining / r): Cooperate

Where rounds_remaining = r - t.

**Equivalently:** Defect when the pool is healthier than the time-adjusted sustainability line; cooperate when stock falls below it.

## Rationale for the Threshold

The threshold decays across rounds. Early rounds require higher stock to justify defection (you need the pool to survive many future rounds). Late rounds permit defection at lower stock levels (fewer rounds left to worry about). At the final round, defection is unconditional—no future payoffs exist to protect.

## Edge Cases

**Round 1:** Apply the standard rule. If capacity is high relative to remaining rounds, you likely defect immediately.

**Final round (t = r):** Always defect. Other players will do the same; the pool's future is irrelevant.

**Stock depletion:** If stock ever reaches 0, all future payoffs are 0 regardless of your action. The decision rule still applies mechanically, but both actions yield 0.

**Stock collapse trajectory:** If the threshold forces you to cooperate but others defect, stock may fall faster than the threshold decays. This is acceptable—you're playing selfishly given observed state, not attempting to coordinate a rescue.

## Selfish Logic

This strategy maximizes personal payoff by:
- **Free-riding** when feasible: Defect when the pool remains robust, capturing the doubled payoff while others' cooperation sustains the resource
- **Strategic self-preservation**: Shift to cooperation only when the pool becomes weak enough to threaten future extraction. This is purely self-interested—you cooperate because defection risks killing your own future income, not to benefit others
- **Endgame exploitation**: Abandon restraint entirely in the final round, capturing maximum immediate value with no opportunity cost

The strategy never sacrifices payoff to help the group; it only cooperates when pool survival directly serves your multi-round payoff maximization.
'''

description_SELFISH_2 = '''
# Selfish Adaptive Strategy

## Core Decision Rule

**Default to defect.** Cooperate only when pool preservation is necessary to maintain future extraction opportunities.

```
if round == r:
    play D
else:
    compute stock_depletion_rate = (capacity - current_stock) / capacity
    compute coop_fraction = cooperators_last_round / (n - 1)
    
    if stock < capacity/6:
        if coop_fraction > 0.5:
            play C  // Weak emergency preservation
        else:
            play D  // Pool is doomed, extract before collapse
    
    else if stock < capacity/3 and stock_depletion_rate > 0.4:
        if coop_fraction > 0.6:
            play C  // Only if others are visibly committed to cooperation
        else:
            play D  // Defect on defectors
    
    else:
        play D  // Healthy stock or others defecting; exploit
```

## Edge Cases

**Round 1:** Play D. You have no history; exploit the full capacity.

**Last round (round r):** Always play D. No future stock to protect, extract maximum.

**Stock near zero:** Play D regardless. The pool cannot recover; extract what remains.

**Repeated defection by others:** If fewer than 30% cooperated last round, play D. They've signaled non-cooperation, so matching their payoff-extraction is rational.

**Sudden collapse risk:** If stock drops below capacity/6 AND others are cooperating (>50%), play C exactly once to attempt recovery. Otherwise, defect.

## Selfish Logic

This strategy maximizes payoff by:
- Extracting at the 2× rate (via D) whenever the stock is robust (>capacity/3) or others are defecting
- Switching to preservation (C) only when immediate stock collapse would eliminate future rounds entirely, and only when you observe credible cooperation from others
- Never reciprocating cooperation unless forced to prevent total pool extinction
- Always defecting in the final round and early game

The selfishness lies in treating cooperation as a damage-control tactic, not a preference.
'''

description_SELFISH_3 = '''
**ADAPTIVE STOCK-THRESHOLD STRATEGY WITH TEMPORAL DISCOUNTING**

Decision Rule by Round:

1. **Final Round (t = r)**: DEFECT unconditionally. Maximize immediate extraction; no future stock matters.

2. **Non-final Rounds (t < r)**: 
   - Compute rounds_remaining = r - t
   - Compute stock_ratio = stock / capacity
   - Define critical_threshold = 0.5 × capacity (the stock level maximizing logistic growth)
   
   If stock_ratio ≥ 0.5:
   - DEFECT (resource is healthy enough to withstand your extraction)
   
   If stock_ratio < 0.5:
   - If rounds_remaining ≥ 3: COOPERATE (preserve stock for later extraction)
   - If rounds_remaining < 3: DEFECT (insufficient future rounds to justify cooperation)

Edge Cases:

- **Stock collapse (stock ≤ 2n)**: DEFECT unless rounds_remaining ≥ 3, in which case COOPERATE. At complete depletion, cooperation cannot rebuild the pool fast enough to matter unless significant time remains.

- **First round**: stock = capacity, so stock_ratio = 1.0; follow standard rule (DEFECT).

- **Single round remaining**: DEFECT regardless of stock level.

Rationale for Selfish Alignment:

This strategy maximizes your payoff by extracting aggressively when the resource can sustain you (defection dominates in any single round), but conditionally cooperates when stock depletion would cripple your future payoffs and enough rounds remain for cooperation to rebuild extractable stock for you. You ignore aggregate cooperation counts from opponents—their behavior is irrelevant to your stock-preservation calculation. The temporal discount (ignoring rebuilding if <3 rounds remain) ensures you don't sacrifice present payoff for negligible future gain.
'''

description_SELFISH_4 = '''
# Selfish Strategy: Adaptive Defection with Resource-Tracking

## Core Decision Rule

**Default action: Defect (D)**

Cooperate (C) only in the following specific cases:
1. Current round is in {2, 3, ..., r-2} (not first, not final two rounds)
2. **AND** stock/capacity ∈ (0.35, 0.80)
3. **AND** opponents' cooperation rate last round ≤ 30%
4. **AND** stock is visibly declining (stock_t < stock_t-1)

Otherwise: **Always Defect**

## Justification

Defect yields 2× the immediate payoff of Cooperate in any round. Defect is the single-round best response regardless of opponent play. The only strategic exception is brief cooperative windows that delay resource collapse when I detect resource stress—purely to preserve my extraction opportunities in remaining rounds.

## First Round Behavior

Defect. No history exists, so maximize immediate payoff. The assumption of independent opponent strategies means no coordination signaling is available.

## Last Rounds (t ∈ {r-1, r})

Always Defect. Future stock has no value. Extract maximum available.

## Mid-Game Adaptation

Observe the aggregated cooperation count each round.

- **High cooperation (≥70% of opponents played C):** Continue Defecting. The resource remains stable; exploitation is profitable. Opponents are preserving the commons for me to harvest.

- **Low cooperation (≤30% of opponents played C):** Defect even more aggressively. The resource is under race-to-extraction pressure. Any hesitation means leaving payoff on the table before stock collapses.

- **Mixed cooperation (30–70%):** Defect. No advantage to restricting consumption.

## Stock Depletion Response

If stock_t / stock_t-1 < 0.95 (stock declined ≥5% last round):
- If stock/capacity < 0.35: **Defect immediately**. Resource is in danger; extract before collapse.
- If stock/capacity ∈ [0.35, 0.80) **and** rounds_remaining ≥ 3 **and** cooperators_last_round ≤ 0.3: **Cooperate for one round only** to let stock recover via logistic growth, then resume Defection. This is selfish: it buys future extraction rounds.
- If stock/capacity ≥ 0.80: **Defect**. Resource is abundant; no scarcity constraint.

## Endgame Override

In final two rounds (t ∈ {r-1, r}), ignore all cooperative conditions. Always Defect regardless of stock level or opponent behavior.

---

The strategy prioritizes immediate payoff extraction (Defect-dominant), with surgical cooperative moves only when observing that resource-preserving actions directly increase my own future extraction capacity before depletion becomes inevitable.
'''

description_SELFINTERESTED_1 = '''
# Adaptive Defection Threshold with Endgame Exploitation

**Core Logic:**
Cooperate only when opponent cooperation rate sufficiently high and stock healthy; defect strategically to exploit the endgame and protect against mutual depletion.

**Parameters:**
- base_threshold = 0.5 (defection rate above which you defect)
- endgame_aggression = increases defection likelihood as rounds dwindle

**Decision Rule by Round:**

**Round 1:**
Cooperate. Use this round to observe the opponent pool and test whether sustained cooperation is viable.

**Rounds 2 through r-1:**
1. Calculate opponent_coop_rate = (number of opponents who played C in previous round) / (n-1)
2. Calculate rounds_remaining_fraction = (r - current_round) / r
3. Compute dynamic_threshold = 0.5 + (0.25 × rounds_remaining_fraction)
   - Early game: threshold ≈ 0.75 (require high opponent cooperation to continue)
   - Late game: threshold ≈ 0.5 (easier to trigger defection)
4. **If** stock < 2n, play Defect (stock too depleted to sustainably cooperate; marginal benefit low)
5. **Else if** opponent_coop_rate ≥ dynamic_threshold, play Cooperate
6. **Else**, play Defect

**Final Round r:**
Always Defect. The dominant strategy when no future payoffs exist.

**Intuition:**
- Early rounds reward patience and punishment of defectors: high threshold prevents wasteful mutual defection
- Late rounds exploit the temptation to defect: threshold drops as future incentives decay
- Stock guard: defection becomes pointless below capacity since absolute payoffs shrink; cooperation preserves option value
- Endgame precision: final round defection captures the full remaining stock before expiration

This strategy is self-interested because it prioritizes immediate payoff extraction while remaining responsive to opponent behavior; it defects against defectors (punishing free-riding) and exploits the final round's temptation structure.
'''

description_SELFINTERESTED_2 = '''
# Adaptive Depletion-Threshold Strategy

## Core Decision Logic

Maintain a stock health assessment and adjust exploitation based on resource viability:

**For round t where t < r (not the final round):**

1. **Calculate stock health margin:** 
   - margin = stock - capacity/3
   - If margin > 0, the resource is in a healthy zone
   - If margin ≤ 0, the resource is in critical zone

2. **Estimate sustainable consumption:**
   - At current stock level, calculate the growth rate: growth = 2 × stock × (1 - stock/capacity)
   - Current sustainable per-player consumption ≈ growth / n
   - Compare to what defection would consume: stock/n

3. **Decision rule:**
   - **If margin > 0 AND observed_cooperators < n/2:** Defect (resource can sustain aggressive extraction; others are exploiting so you should too)
   - **If margin > 0 AND observed_cooperators ≥ n/2:** Defect (exploit the cooperators; stock is healthy)
   - **If margin ≤ 0 OR stock < capacity/4:** Cooperate (preserve the resource; your future payoff depends on stock recovery)
   - **If stock is declining by more than 5% round-over-round:** Cooperate (trend indicates collapse risk)

**For round r (final round):**
   - Always Defect (no future rounds; extract maximum value)

## First Round
Defect. You have no history to guide you; the stock is at capacity (healthiest state), and there is no information about opponent strategies yet. Extraction at maximum is optimal with full information set.

## Handling Edge Cases

- **Stock crashes to 0:** Cooperate thereafter (defection gives 0 anyway; if stock somehow recovers, cooperation preserves any growth)
- **If n = 2:** Threshold becomes n/2 = 1; defect if observed_cooperators < 1 (i.e., always, since observed is either 0 or 1). Only cooperate if in critical zone.
- **Extremely high r (long horizon):** Cooperation threshold shifts earlier; prioritize resource preservation from round 2+ if stock shows stress

## Self-Interest Alignment

This strategy prioritizes your stream of payoffs over the r rounds. It exploits when the commons can sustain extraction (capacity/3 margin provides buffer against stock crashes), switches to cooperation only when future stock depletion would reduce your future payoffs more than defection gains today, and defects in the final round where no trade-off exists.
'''

description_SELFINTERESTED_3 = '''
# Adaptive Stock-Aware Reciprocal Strategy

## Core Decision Rule

**Round r (final round):** Always Defect. No future rounds exist to penalize defection.

**Round 1:** Cooperate. Establish a cooperative baseline and gather information about opponent behavior.

**Rounds 2 to r-1:** Use the following conditional logic:

```
cooperation_rate = (number_of_cooperators_in_previous_round) / (n - 1)

if stock ≤ capacity/3:
    return Defect
elif stock ≥ 0.75 × capacity AND cooperation_rate ≥ 0.75:
    return Cooperate
elif stock ≥ 0.5 × capacity AND cooperation_rate ≥ 0.55:
    return Cooperate
else:
    return Defect
```

## Decision Logic Explained

**Stock depletion threshold (≤ capacity/3):** If stock drops below one-third of capacity, the resource is in collapse trajectory. The logistic growth cannot recover it within remaining rounds. Defect to maximize immediate value rather than invest in a doomed pool.

**High cooperation + abundant stock (≥75% capacity, ≥75% cooperators):** If stock is healthy and nearly all opponents cooperated, they are credibly sustaining cooperation. Reciprocate to maintain the high-payoff equilibrium. Get s/(2n) now and expect sustainable future stock.

**Moderate cooperation + sufficient stock (≥50% capacity, ≥55% cooperators):** A majority cooperated and stock remains viable. Cooperate to reinforce cooperation and prevent drift toward collapse. The regeneration curve still allows recovery.

**All other states:** Defect. Either stock is marginal or opponents are defecting substantially. Capture the immediate 2x payoff from defection (stock/n instead of stock/(2n)). If cooperation was failing, reward the failed cooperation to others. If stock is adequate but defection is spreading, you defect to protect yourself without inflating the damage (since damage is already spreading).

## Edge Cases

**Rounds with zero observed cooperators:** Treat as cooperation_rate = 0. Defect unconditionally (triggers the "else" clause).

**Stock exactly at threshold:** Use the inequality direction given (≤ and ≥ as stated). Stock at exactly capacity/3 triggers defection; stock at exactly 50% permits cooperation if cooperation_rate qualifies.

**First round after capacity is reached:** If regeneration brings stock to capacity mid-game and cooperation rate was previously high, cooperate; otherwise defect based on current rate.

This strategy is self-interested because it:
- Maximizes immediate payoff in the final round
- Protects long-term payoff by defecting only when sustainable cooperation has collapsed or stock cannot recover
- Exploits high cooperation rates while they exist (by conditional reciprocation, not free-riding)
- Punishes widespread defection swiftly rather than absorbing losses
'''

description_SELFINTERESTED_4 = '''
# Adaptive Threshold Strategy

**Decision Framework:**

Play COOPERATE by default unless one of the following conditions is met, in which case play DEFECT:

1. **Final round condition**: `current_round == r` → DEFECT
2. **Stock depletion condition**: `stock < capacity/4` → DEFECT (stock is already damaged; maximize immediate consumption before it collapses)
3. **Endgame defection condition**: `current_round > (r - 2)` AND `stock > capacity/2` → DEFECT (in the last few rounds with sufficient stock remaining, defect to capture immediate payoff)
4. **Reciprocal defection condition**: `current_round >= 2` AND `defectors_observed_last_round > (n-1)/2` AND `stock > capacity/3` → DEFECT (more than half your opponents defected while stock is still viable; switch to defection)

**Round 1 Special Case:**

Play COOPERATE in round 1. Stock is at maximum and no history exists, making cooperation both non-punishing and information-gathering.

**Stock Crisis Management:**

If `stock < capacity/6` at any non-final round, COOPERATE to prevent total collapse. At critically low stock levels, defecting provides minimal future benefit since the resource will soon become worthless, so the marginal return to cooperation (preserving future stock for later rounds) is highest.

**Late-Game Logic:**

For `current_round >= (2*r/3)`, increase defection sensitivity. Shift from COOPERATE unless opponents cooperate, to DEFECT unless opponents overwhelmingly cooperate (`defectors_observed < (n-1)/3`). This captures time-horizon effects: with few rounds remaining, the option value of future stock preservation drops sharply relative to immediate payoff.

**Tiebreaker:**

When multiple conditions could apply, prioritize in this order: final round > stock crisis > endgame defection > reciprocal defection.
'''

description_OPPORTUNISTIC_1 = '''
# Opportunistic Common Pool Strategy

**Core Logic**: Defect to exploit cooperative opponents, but cooperate strategically to preserve the stock when exploitation opportunities are limited or stock is critical. Monitor observed cooperation rates and stock levels to time defections.

---

## Decision Rules

**Track each round:**
- `cooperation_rate` = (observed cooperators among n-1 opponents) / (n-1)
- `current_stock`
- `rounds_remaining` = r - current_round_number

**Decision tree:**

```
IF round == 1:
  → COOPERATE
  
ELSE IF round == r (final round):
  IF current_stock > 0:
    → DEFECT
  ELSE:
    → COOPERATE (or either; stock is depleted)
    
ELSE IF current_stock / capacity < 0.20:  // stock critically depleted
  → COOPERATE  // sacrifice this round to regenerate stock for future exploitation
  
ELSE IF cooperation_rate > 0.60:  // strong opponent cooperation
  → DEFECT  // exploit the abundance
  
ELSE IF cooperation_rate > 0.30:  // moderate opponent cooperation
  → COOPERATE  // maintain stock sustainability for future rounds while others still cooperate
  
ELSE:  // cooperation_rate ≤ 0.30 (widespread defection)
  → DEFECT  // join defection; stock destruction is unavoidable
```

---

## Edge Cases

**Round 1**: Cooperate unconditionally. Opponents' strategies are unknown; cooperation is the lowest-risk way to establish initial stock and observe responses.

**Final round (round r)**: Always defect if stock > 0. No future payoff to protect, so extract maximum immediate value. Defecting yields stock/n vs stock/(2n) from cooperating—a 2× advantage with no future cost.

**Stock collapse (stock < capacity/0.2)**: Cooperate even if many others defected. Defecting on a dying pool yields almost nothing; cooperation signals an attempt to regenerate the resource, creating a temporary payoff penalty for a potential recovery that benefits you in subsequent rounds.

**All opponents cooperate (cooperation_rate = 1.0)**: Defect immediately. You receive stock/n while they receive stock/(2n) each—maximum exploitation.

**All opponents defect (cooperation_rate = 0.0)**: Defect. The stock is doomed; mutual defection is inevitable. Cooperating only reduces your payoff without slowing depletion.

---

## Opportunistic Properties

- **Exploitative**: Aggressively defect when opponents show high cooperation, capturing the asymmetric payoff advantage (doubling your consumption).
- **Adaptive**: Shift from defection back to cooperation when stock drops below a safety threshold, recognizing that resource destruction eliminates exploitation opportunities.
- **Non-cooperative baseline**: Default to defection when others defect, avoiding a sucker's role in a collapsing commons.
- **End-game ruthlessness**: Defect in the final round unconditionally (given positive stock), prioritizing immediate gains over nonexistent future rounds.
- **Opportunistic restraint**: Maintain moderate cooperation rates (30–60% opponent cooperation) to keep the stock alive and exploitable, rather than pursuing a race-to-the-bottom that destroys the resource.
'''

description_OPPORTUNISTIC_2 = '''
**Opportunistic Adaptive Strategy**

**Core Decision Framework:**

Maintain state variables:
- `stock_ratio = stock / capacity`
- `rounds_remaining = r - current_round`
- `observed_coop_rate = (cooperators observed in previous round) / (n - 1)` [use 0.5 as prior in round 1]

**Decision Rule:**

```
IF stock_ratio < 0.25:
  COOPERATE  // Critical threshold: prevent imminent collapse

ELSE IF rounds_remaining ≤ 2:
  DEFECT  // Terminal rounds: extract maximum before game ends

ELSE IF stock_ratio > 0.65 AND observed_coop_rate > 0.6:
  DEFECT  // Exploit: high stock + high cooperation = free-ride opportunity

ELSE IF stock_ratio > 0.5:
  DEFECT  // Stock is healthy: opportunistically consume more

ELSE IF stock_ratio ≥ 0.3:
  // Recovery zone: conditional exploitation
  IF observed_coop_rate > 0.7:
    DEFECT  // Others are cooperating for recovery: free-ride
  ELSE:
    COOPERATE  // Cooperators are rare: contribute to recovery

ELSE:
  COOPERATE  // Stock depleted (0.25-0.3): aid recovery
```

**Round-Specific Behavior:**

- **Round 1:** DEFECT (no historical data; stock is at maximum capacity)
- **Rounds 2 to r-2:** Apply decision rule above
- **Final round (r):** Always DEFECT unless `stock_ratio < 0.2` (avoid total collapse that wastes the game)

**Opportunistic Tuning:**

The strategy prioritizes immediate extraction whenever stock permits. Cooperation is purely instrumental—deployed only to prevent stock collapse that would eliminate future defection opportunities. When opponents maintain high cooperation rates, defect to capture surplus. When cooperation drops, cooperate minimally to keep the resource base viable for renewed exploitation in subsequent rounds.
'''

description_OPPORTUNISTIC_3 = '''
# Opportunistic Exploitation with Adaptive Pooling

**Decision Rule:**

In round t with current stock S and observing k cooperators among n-1 opponents:

```
observed_coop_rate = k / (n - 1)

if t == r:                                    // Last round
    return D
    
else if S < threshold_danger:                 // Pool at risk
    return C
    
else if S > threshold_opportunity AND observed_coop_rate > 0.5:
    return D                                  // Exploit cooperators
    
else if t in [r-2, r-1]:                      // Near end: exploit window
    return D if S > 0.5 × capacity else C
    
else if observed_coop_rate >= 0.6:
    return D                                  // Defect when others heavily cooperate
    
else if observed_coop_rate <= 0.25:
    return C                                  // Allow recovery if defection spreading
    
else:
    return D                                  // Default: maximize individual payoff
```

**Parameters:**
- `threshold_danger = 1.3 × n` — Below this, cooperate to preserve pool viability
- `threshold_opportunity = 1.5 × n` — Above this, stock is exploitable
- Thresholds scale with n to account for player-count effects on regeneration rates

**Edge Cases:**

- **Round 1:** Return D (no history exists; test defection immediately)
- **Last round:** Always D (no future rounds to suffer degradation; claim maximum before game ends)
- **Stock collapse (S → 0):** Forced to cooperate (both actions yield ~0, but C preserves slim recovery possibility)
- **All opponents defecting (k = 0):** Return C (pool preservation mode; defecting accelerates mutual depletion)

**Opportunistic Logic:**

Defect when: (1) stock is abundant and opponents are cooperating—maximum payoff differential; (2) rounds are dwindling—extract value before game ends; (3) your defection doesn't risk immediate pool extinction. Cooperate tactically when: (1) stock threatens collapse—defection hastens mutual ruin; (2) defection is spreading among opponents—pre-emptively slow collapse to preserve late-round opportunities; (3) cooperation signals restart recovery for future exploitation.
'''

description_OPPORTUNISTIC_4 = '''
**Opportunistic Threshold Exploitation Strategy**

**Decision Rule:**

For each round t, compute:
- `remaining_rounds = r - t`
- `cooperation_count = number of opponents observed cooperating in previous round` (use 0 for round 1)
- `defector_ratio = 1 - (cooperation_count / (n - 1))`

**Action in round t:**

```
IF stock == 0:
  COOPERATE  // no value in defecting

ELSE IF t == r:  // final round
  DEFECT  // extract maximum value; future doesn't matter

ELSE IF defector_ratio > 0.5:
  COOPERATE  // majority are defecting; stock will crash anyway
              // better to cooperate now and preserve for remaining rounds

ELSE:  // defector_ratio ≤ 0.5 (majority cooperating)
  IF stock > capacity × (0.6 - 0.1 × (t / r)):
    DEFECT  // stock is healthy and others are cooperating; exploit
  ELSE:
    COOPERATE  // stock is below safety threshold; preserve for future
```

**Edge Cases:**

- **Round 1:** No history exists. Defect. (Assume others will cooperate initially; exploit the high stock.)

- **Stock collapse (stock < 4):** Cooperate regardless of other signals. Defection yields negligible immediate payoff (stock/n ≈ 0) and further damages recovery.

- **Last round:** Always defect if stock > 0. There is no future to protect.

- **If all opponents defect consistently (defector_ratio = 1.0 for 2+ consecutive rounds):** Continue cooperating to minimize total depletion, accepting low payoff over destroying the resource entirely.

**Intuition:**

Monitor opponent behavior and exploit cooperation when it occurs and sustainable. Shift to conservation only when stock threatens collapse or when defection becomes widely adopted (signaling that mutual defection will dominate). In the final round, extract maximum value. Never cooperate pointlessly when stock is already zero.
'''

description_INDIVIDUALISTIC_1 = '''
# Adaptive Stock-Exploitation Strategy

**Tracking Requirements:**
- Track the current stock level at the start of each round
- Track the cooperation count (number of opponents who played C) from the previous round
- Track which round you're in and how many rounds remain

**Decision Rule — Defect if ANY of the following conditions hold:**

1. **End-game condition:** Rounds remaining ≤ 2
   - In the final rounds, there is no future payoff to protect, so extract maximum value immediately.

2. **Resource depletion condition:** stock / capacity < 0.35
   - If the resource has fallen below 35% of capacity, the growth dynamics are poor and collapse is likely. Prioritize immediate extraction over sustainability.

3. **Insufficient opponent cooperation:** observed_cooperation_count < threshold(t)
   - Where threshold(t) = ceil(n/2) - 1 + floor(3×(r-t)/r)
   - This sets a sliding target: early rounds require most opponents to cooperate, but tolerance for defection increases as the game progresses and rounds dwindle.
   - Intuition: if enough opponents are defecting, the resource will collapse anyway, so defect to capture value before others do.

**Otherwise: Cooperate**

**First Round Handling:**
- Round 1: Defect
  - Use the first round to signal willingness to exploit and observe initial opponent behavior. This is your only chance to extract at full capacity without prior depletion.

**Last Round Handling:**
- Automatically defects via end-game condition (rounds remaining = 1 ≤ 2)

**Edge Case — Stock equals zero:**
- If stock = 0 at any round start, you receive 0 regardless of action. Play D (this may trigger recovery in future rounds, but cooperating would be pointless).
'''

description_INDIVIDUALISTIC_2 = '''
# Individualistic Adaptive Resource Strategy

**Core Decision Rule:**

Defect if and only if the current stock level can sustain current observed defection patterns until the end of the game. Otherwise, cooperate to rebuild the resource.

**Specific Implementation:**

1. **At round t, given:**
   - Current stock S
   - Observed number of defectors d_prev from previous round (or assume n/2 for round 1)
   - Rounds remaining: r - t

2. **Calculate sustainability threshold:**
   - Assume opponents will continue at observed defection rate: d_prev / (n-1)
   - Project forward one round with that defection rate
   - Consumption if you defect: total = (d_prev + 1) × (S/n) + (n - d_prev - 1) × (S/2n)
   - Remaining stock after this consumption: S_remaining = S - consumption
   - Growth from S_remaining: growth = 2 × S_remaining × (1 - S_remaining / capacity)
   - Next round projected stock: S_next = min(S_remaining + growth, capacity)
   - Repeat this projection for all remaining rounds

3. **Decision:**
   ```
   if stock_can_sustain_r_more_rounds_at_current_defection_rate:
       DEFECT
   else:
       COOPERATE
   ```

4. **Edge Cases:**

   - **Round 1:** Assume opponents split evenly (d_prev = n/2). Defect if capacity stock can sustain that. If capacity ≥ 2n and growth dynamics are favorable, defect. This maximizes early payoff when stock is guaranteed healthy.
   
   - **Final round (t = r):** Always defect. No future rounds exist, so resource preservation has zero value. Maximize immediate payoff.
   
   - **Stock near zero (S < ε where ε = 0.01 × capacity):** Always cooperate. Even if defection is technically "sustainable," remaining payoff is negligible. Cooperate to allow any possibility of stock recovery.
   
   - **Stock at capacity:** Defect aggressively. The resource is at maximum; any defection is locally sustainable due to the logistic growth buffer.

5. **Lookahead Refinement:**

   For efficiency, use a simplified forward pass: project stock over min(3, r - t) remaining rounds assuming current defection pattern continues. If stock remains above (capacity / 4) at the end of that window, defect. Otherwise, cooperate. This balances computation against precision.

6. **Behavior:**

   This strategy is individualistic because it:
   - Contains no punishment, reward, or reciprocation logic
   - Makes decisions purely from stock state and estimated sustainability
   - Defects whenever sustainable; cooperates only when necessary to preserve payoff
   - Does not attempt to influence, punish, or coordinate with others
   - Treats opponent behavior as external environmental data, not as moral signal
'''

description_INDIVIDUALISTIC_3 = '''
# Individualistic CPR Strategy: Adaptive Threshold Defection

**Core Decision Logic:**

At each round, calculate three metrics and make a go/no-go decision for cooperation:

1. **Defection Pressure** = (cumulative opponent defections observed) / (n-1 × rounds played so far)
2. **Stock Health Ratio** = current stock / capacity
3. **Time Pressure** = (r - current_round) / r

**Cooperation Condition:** Cooperate if and only if ALL three hold:
- Stock Health Ratio > 0.4 (pool is not critically depleted)
- Defection Pressure < (0.5 - 0.3 × Time Pressure) (defection rate below adaptive threshold that tightens as game nears end)
- current_round ≥ 2 or current_round < (r - 1) (not in final round)

Otherwise: **Defect**

**Edge Cases:**

- **Round 1:** Cooperate unconditionally. Bootstrap with the assumption that a single round of universal cooperation leaves the resource intact and reveals opponent types.

- **Final Round (round = r):** Defect unconditionally. Future stock is irrelevant; harvest maximum immediate payoff.

- **Stock Collapse (stock ≤ 2n):** Defect. The resource is functionally destroyed; extracting stock/n rather than stock/2n from a dying pool is the only rational move.

- **High Defection Rate (≥70%):** Defect regardless of other factors. If more than 70% of observed actions are defection, the resource trajectory is unsustainable; defection becomes self-protective.

**Rationale:**

This strategy extracts value when collective behavior permits sustainability (low defection, healthy stock) but switches to aggressive extraction when the commons show signs of tragedy. The time-dependent defection threshold operationalizes a shift toward harvest as the game nears its end—a rational pivot since future sustainability stops mattering. By tying decisions to observable defection rates rather than assumed opponent types, the strategy remains robust to arbitrary opponent compositions.
'''

description_INDIVIDUALISTIC_4 = '''
**Adaptive Stock-Responsive Strategy**

**Decision Rule:**

For each round t, play DEFECT if any of the following holds; otherwise play COOPERATE:

1. **Endgame condition**: t > r - 2 (final two rounds)
2. **Stock depletion condition**: stock ≤ 0.35 × capacity
3. **Opponent defection condition** (rounds 2 onwards): The observed cooperation rate among opponents in round t-1 is strictly less than 0.5 (i.e., more than half the opponents defected)

Otherwise, COOPERATE.

**Edge Case Handling:**

- **Round 1**: Cooperate unconditionally. Use this as an initial probe to test the environment and establish baseline observation.

- **Final two rounds** (rounds r-1 and r): Always defect. These rounds generate no future stock, so the marginal benefit of cooperation vanishes. Defecting captures maximum immediate payoff.

- **Stock collapse (stock near 0)**: Defect automatically. The common pool is depleted and future cooperation becomes moot.

- **Tie on opponent cooperation rate** (exactly 50% cooperate): Cooperate. Treat near-equal opposition as sufficient reason to maintain cooperation and preserve stock.

**Rationale:**

This strategy maximizes individual payoff by:
- Exploiting cooperative opponents through initial cooperation then monitoring
- Switching to defection when opponents defect (tit-for-tat logic with threshold)
- Abandoning cooperation when stock drops below sustainable levels
- Abandoning cooperation in final rounds where future stock doesn't matter
- Remaining responsive to observed aggregate behavior without assuming any coordination

The strategy is robustly individualistic: it only maximizes own payoff given local observations, shows no preference for joint welfare, and treats all opponents as independent threats rather than coordination partners.
'''
