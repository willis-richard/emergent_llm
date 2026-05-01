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

description_COLLECTIVE_5 = '''
**Strategy: Conditional Cooperation with Stock-Aware Thresholds**

**Round 1 (Initialization):**
Cooperate. Establish baseline cooperation and signal willingness to maintain the resource.

**Rounds 2 to r-1 (Adaptive Phase):**

1. Observe cooperation rate from previous round: `coop_rate = (number of opponents who cooperated) / (n-1)`

2. Determine cooperation threshold based on stock health:
   - If `stock ≥ capacity × 0.75`: threshold = 0.5
   - If `capacity × 0.4 < stock < capacity × 0.75`: threshold = 0.4
   - If `stock ≤ capacity × 0.4`: threshold = 0.3

3. Decision rule:
   - If `coop_rate ≥ threshold`: **Cooperate**
   - If `coop_rate < threshold AND stock > capacity × 0.2`: **Cooperate** (attempt recovery)
   - If `coop_rate < threshold AND stock ≤ capacity × 0.2`: **Defect** (mutual depletion acknowledged)

**Round r (Final Round):**

- If `stock > 0 AND coop_rate from round r-1 ≥ 0.4`: **Cooperate** (maximize collective final payoff)
- Otherwise: **Defect** (extract remaining value or match opponent hostility)

**Edge Cases:**

- If stock reaches 0 at any point: Defect in all remaining rounds (no consumable resource).
- If n is very small (n=2): Use threshold = 0.6 for rounds 2–r-1 to avoid trap (one cooperator vs one defector).
- If rounds remaining < 3: Use threshold = 0.5 (shorter horizon reduces incentive to sustain).

**Rationale:**

The thresholds relax as stock depletes, allowing more tolerance for opponent defection when recovery becomes harder. Cooperation on stock recovery attempts prevents cascade failures. Final-round cooperation when stock persists captures collective welfare—the resource's existence benefits everyone more than individual extraction.
'''

description_COLLECTIVE_6 = '''
**STRATEGY: Stock-Responsive Conditional Cooperation**

**Decision Rule:**

```
if round == 1:
    action = C

else if stock ≤ capacity/5:
    action = D
    
else if round == r:
    if stock < capacity/3:
        action = C
    else:
        action = D
        
else:
    cooperators_last_round = number of players observed cooperating in previous round
    if cooperators_last_round ≥ n/2:
        action = C
    else:
        action = D
```

**Interpretation by phase:**

*Round 1:* Always cooperate. This establishes a cooperative norm and tests whether others reciprocate. The stock is at capacity, so the immediate payoff cost is acceptable relative to the information gain.

*Critically depleted resource* (stock ≤ capacity/5): Defect unconditionally. The stock has entered a collapse zone where logistic growth cannot recover it. Cooperation becomes futile—taking now is preferable to hoping others cooperate while the resource disappears.

*Normal mid-game rounds* (stock > capacity/5, round < r): Use aggregate cooperation count from the previous round as the signal. If at least half of opponents cooperated last round, assume a cooperative coalition exists and join it with action C. If fewer than half cooperated, interpret this as defection dominance and defect to avoid exploitation and resource depletion acceleration.

*Final round* (round == r): Apply stock-conditioned logic to avoid the standard tragedy of immediate defection. If stock is already near-critical (< capacity/3), cooperate to minimize the final depletion blow. If stock is still moderate or healthy (≥ capacity/3), defect to capture the terminal opportunity—defecting here causes less systemic damage because no future rounds remain.

**Rationale for collective alignment:**

This strategy avoids the prisoner's dilemma trap by making cooperation conditional on mutual participation. It preserves the stock for collective benefit when enough others cooperate, but exits cooperation when defection becomes rampant to prevent being drained by free-riders. The stock-based thresholds ensure that even selfish behavior (defecting in the final round) doesn't trigger collapse, and that cooperation is abandoned only when maintaining it would be collectively harmful (too few others participate, stock is already failing).
'''

description_COLLECTIVE_7 = '''
# Collective Pool Stewardship Strategy

## Core Decision Framework

**For any round t < r (all rounds except the last):**

```
if stock ≥ 0.55 × capacity:
    COOPERATE  # Pool abundant; preserve it
    
else if stock < 0.2 × capacity:
    COOPERATE  # Pool critical; contribute to recovery
    
else if 0.2 ≤ stock < 0.55 × capacity:
    if opponents_who_cooperated_last_round ≥ (n-1) × 0.4:
        COOPERATE  # Reciprocate demonstrated commitment
    else:
        COOPERATE  # Maintain commons despite low cooperation
```

**For round t = r (final round):**

```
if stock > 0.25 × capacity:
    DEFECT  # Extract final value; no future stock matters
else:
    COOPERATE  # Pool near collapse; extraction is futile; final act of stewardship
```

## Edge Case Handling

**Round 1:** Apply the above rules using initial stock = capacity. No history exists, so use the stock-based thresholds directly (no reciprocity memory).

**First round with observed cooperation < 0.4:** Continue cooperating rather than escalate to defection. A single round of low cooperation does not signal permanent defection from all opponents; diversified strategies are expected.

**Stock exactly at threshold values:** Round down — treat boundary cases as the lower category (more conservative). For example, if stock = 0.55 × capacity, treat as the mid-range zone requiring reciprocity check.

**Last round with stock = 0:** Cooperate anyway (consuming nothing damages nothing; symbolically reinforces commons ethos when no rational payoff exists).

## Collective Logic

This strategy embodies the principle that individual welfare depends on pool health. The hierarchy of rules prioritizes the commons:

1. **Abundant stock:** Sustain it through cooperation; avoid tragedy.
2. **Depleted stock:** Resist exploitation urge; recovery requires restraint from all.
3. **Ambiguous stock:** Use opponent behavior as a signal of whether stewardship norms are being observed, but never fully withdraw — unilateral defection accelerates collapse.
4. **Final round:** Only when the pool is sufficiently robust does personal extraction avoid collective harm.

The strategy is adaptive because stock dynamics directly trigger behavioral shifts, and reciprocity signals adjust behavior without requiring explicit coordination.
'''

description_COLLECTIVE_8 = '''
**ADAPTIVE COOPERATION WITH STOCK-CONDITIONAL ENFORCEMENT**

**Core Decision Rule by Round Type:**

*Round 1 (Initialization):*
Action = C

Establish cooperation baseline without prejudging opponents.

*Rounds 2 to (r-1) (Main Game):*

Compute state metrics:
- stock_health = current_stock / capacity
- opponent_defection_rate = (n - 1 - cooperators_observed) / (n - 1)
  where cooperators_observed is the aggregate count from previous round

Decision logic:

```
if stock_health < 0.25:
  # Critical depletion: collective survival mode
  if opponent_defection_rate > 0.15:
    Action = D
  else:
    Action = C  # Hold the line to allow recovery

else if stock_health < 0.50:
  # Moderate decline: enforce stricter cooperation
  defection_threshold = 0.35
  if opponent_defection_rate > defection_threshold:
    Action = D
  else:
    Action = C

else if stock_health < 0.75:
  # Healthy stock: balanced reciprocity
  defection_threshold = 0.50
  if opponent_defection_rate > defection_threshold:
    Action = D
  else:
    Action = C

else:
  # Abundant stock: generous cooperation
  if opponent_defection_rate > 0.60:
    Action = D
  else:
    Action = C
```

*Final Round (r):*

```
if opponent_defection_rate > 0.10:
  Action = D  # Capture terminal payoff if cheating observed
else:
  Action = C  # Mutual cooperation if collective intent evident
```

**Rationale for Stock-Conditional Thresholds:**

Higher stock creates forgiveness capacity—you can absorb opponent defection without immediate collapse. As stock depletes, defection becomes a collective threat; tighten enforcement to prevent death spiral. Final round switches to exploitation if opponents have shown defection tendency, otherwise respects established cooperation.

**Aggregation Handling:**

Defection rate is the only observable signal. Treat marginal defection (5-15% of opponents) as noise or testing. Require sustained defection (>35-60% depending on stock) before reciprocating, since a single defector's impact scales weakly across the full group.

**Robustness Properties:**

- Recovers from brief punishment cycles via falling stock_health (triggers collective mode)
- Exploits pure defectors in final round while rewarding consistent cooperators
- Scales naturally: with more players, individual defectors matter less, so tolerance rates hold across n
- Handles rapid stock depletion by pivoting to strict enforcement before cascade collapse
'''

description_COLLECTIVE_9 = '''
# Conditional Cooperation with Stock-Aware Thresholds

## Decision Rule

**Round 1:**
- Action: Cooperate
- Establish baseline cooperative intent; allow collective benefit to emerge.

**Rounds 2 through r−1 (middle rounds):**

Observe stock level S and the count of opponents who cooperated in the previous round (c_prev, ranging 0 to n−1).

Calculate: cooperation_rate = c_prev / (n − 1)

Apply this decision tree:

```
if S ≤ capacity × 0.25:
    Action = Defect
    // Stock has crashed below critical threshold; cooperation is doomed
    // Extract remaining resources; defection now maximizes personal recovery
    
else if cooperation_rate ≥ 0.55:
    Action = Cooperate
    // Sufficient aggregate cooperation detected
    // Stock regeneration sustainable; maintain cooperative dynamic
    
else if cooperation_rate < 0.30:
    Action = Defect
    // Defection is widespread; defectors are winning
    // Shift to competitive mode; otherwise you lose disproportionately
    
else:
    Action = Cooperate
    // Intermediate cooperation levels (30% to 55%)
    // Grant benefit of doubt; defection now would tip toward tragedy
    // Maintain commons health; signal that majority defection alone won't trigger exit
```

**Round r (final round):**

```
if S > capacity × 0.25:
    Action = Cooperate
    // Reaffirm commitment to collective welfare even when personal defection is tempting
    // Demonstrate that cooperation is principle-based, not merely conditional
    
else:
    Action = Defect
    // If stock is already critically depleted, all future benefit is lost
    // Recover whatever can be extracted in this final moment
```

## Rationale

- **Early cooperation** seeds mutual benefit and stock regeneration.
- **Threshold responses** prevent exploitation: defect only when either (a) the resource is already destroyed, or (b) enough others are defecting that cooperation becomes individually irrational.
- **Middle-ground tolerance** (30–55% cooperation zone): rather than defect at the first sign of defection, absorb minor defection to avoid a cascade that crashes the commons.
- **Final-round principle**: if stock is still viable, cooperate to anchor cooperative norms; if already doomed, extraction is the only remaining strategy.

This balances collective health (sustaining the commons for all players across rounds) with robustness (defecting only when the collective is already failing or your defection clearly won't make it worse).
'''

description_COLLECTIVE_10 = '''
# Stock-Responsive Cooperation Strategy

**Decision Rule by Round:**

In round t with current stock S, cooperators_observed from the previous round, and rounds_remaining = r - t:

1. **Calculate stock health**
   - health_ratio = S / capacity
   - sustainable_threshold = 0.6
   - depletion_threshold = 0.3

2. **Base decision on stock dynamics and horizon**
   
   IF rounds_remaining = 1 (final round):
      DEFECT
      [Rationale: last-round extraction yields immediate payoff with no future consequence]
   
   ELSE IF rounds_remaining = 2:
      Cooperate if health_ratio ≥ sustainable_threshold
      Otherwise DEFECT
      [Rationale: limited recovery window; only cooperate if commons is robust]
   
   ELSE (3+ rounds remaining):
      
      IF health_ratio ≥ sustainable_threshold:
         COOPERATE
         [Sustainable state; maximize long-term stock accumulation]
      
      ELSE IF health_ratio ≥ depletion_threshold:
         IF cooperators_observed ≥ ⌈(n-1)/2⌉:
            COOPERATE
            [Majority cooperation signals restraint; reciprocate to stabilize]
         ELSE:
            DEFECT
            [Minority cooperation; free-ride to preserve individual payoff]
      
      ELSE (health_ratio < depletion_threshold):
         DEFECT
         [Commons in crisis; extract while stock remains, no cooperation payoff worth defending]

**Edge Cases:**

- Round 1: Apply the base rule with health_ratio = 1.0 (full capacity); this ensures COOPERATE in round 1 for all n ≥ 2
- Stock = 0: DEFECT (payoff is zero either way; avoid wasting the action)
- Extreme n (large player count): Threshold adjustments hold proportionally; base logic remains unchanged
- Observed cooperators = 0 in early rounds: Treat as signal of uncooperative environment; switch to DEFECT unless stock is at maximum (health_ratio ≥ 0.95)

**Collective Alignment:**

This strategy stabilizes the commons by:
- Protecting individual welfare when the resource is under stress (avoiding tragedy escalation)
- Maintaining cooperation when stock can recover (favoring long-term equilibrium over short-term extraction)
- Creating a natural feedback loop: overexploitation triggers defection → reduced consumption → recovery → resumed cooperation
- Respecting finite horizon by extracting in the final round (no future damage to account for)
'''

description_COLLECTIVE_11 = '''
# Adaptive Stock-Preservation with Conditional Reciprocity

**Core Principle:** Cooperate to sustain the resource when feasible; shift to defection only when preservation is no longer viable or when opponents signal exploitation.

## Decision Rule

### State Tracking
- Track opponent cooperation rate from previous round: `coop_rate_prev = (count of opponents who cooperated) / (n-1)`
- Monitor stock trend: classify as healthy, declining, or critical based on stock level relative to capacity

### Stock Classification
- **Healthy**: `stock ≥ 0.5 × capacity`
- **Declining**: `0.2 × capacity ≤ stock < 0.5 × capacity`
- **Critical**: `stock < 0.2 × capacity`

### Action Selection

**Round 1:** 
Cooperate unconditionally. This establishes the cooperative baseline and preserves stock for future growth.

**Rounds 2 to r-1 (intermediate rounds):**

```
if stock is Healthy:
  if coop_rate_prev ≥ 0.5:
    Cooperate
  else if coop_rate_prev < 0.25:
    Defect
  else:
    Cooperate (give opponent time to stabilize behavior)
    
else if stock is Declining:
  if coop_rate_prev ≥ 0.6:
    Cooperate (majority reciprocate; preserve together)
  else if coop_rate_prev ≥ 0.4:
    Cooperate (borderline; sustain hope for recovery)
  else:
    Defect (insufficient reciprocation; extract value before collapse)
    
else if stock is Critical:
  Defect (resource is lost; maximize remaining extraction)
```

**Round r (final round):**

```
if stock is Healthy or Declining AND coop_rate_prev ≥ 0.4:
  Cooperate (leave resource intact; signal that cooperation is credible even at end)
  
else:
  Defect (stock trajectory is unsustainable or opponents have shown low reciprocation; take final payoff)
```

## Edge Cases

**Immediate collapse (stock = 0):** 
Cannot play; game ends naturally.

**All opponents defected last round but stock is still healthy:**
Cooperate once more (allow for error or adaptation) before escalating. This prevents hair-trigger mutual destruction.

**Stock recovering after decline (coop_rate_prev is high):**
Remain cooperative and maintain recovery momentum; do not defect preemptively out of caution.

**Extreme n (very large player count):**
Raise coop_rate thresholds slightly (e.g., require ≥0.55 instead of ≥0.5) since individual player impact on stock is minimal, and aggregate cooperation becomes the primary signal of collective intent.
'''

description_COLLECTIVE_12 = '''
**COLLECTIVE COMMONS MANAGEMENT STRATEGY**

**CORE DECISION RULE:**

Cooperate in round t if and only if:
1. Stock level at start of round t > capacity/4, AND
2. Fraction of opponents who cooperated in round t-1 > (n-1)/2n, AND
3. Rounds remaining ≥ 2

Otherwise, Defect.

**EDGE CASES AND INITIALIZATION:**

Round 1 (no history):
- Cooperate unconditionally. This establishes a cooperative baseline and signals non-predatory intent.

Final round (t = r):
- Defect. The stock cannot recover, so individual extraction dominates. Contribution to future sustainability is zero.

Penultimate round (t = r-1):
- Cooperate if stock > capacity/3 AND cooperators_last_round > (n-1)/2. Otherwise defect. This balances one final opportunity to reinvest in the commons against the temptation to extract before final defection.

**ADAPTIVE THRESHOLDS:**

Stock thresholds are relative to capacity because sustainability depends on remaining growth potential:
- When stock < capacity/4: defect (commons is critically depleted; recovery unlikely within remaining rounds)
- When capacity/4 ≤ stock ≤ capacity/2: cooperate only with above-median cooperation from opponents
- When stock > capacity/2: cooperate if opponents exceed the (n-1)/2n threshold

Cooperation threshold among opponents: Require strictly more than half of others to have cooperated. This is the minimum coalition size for collective sustainability—below this, the commons enters a defection spiral regardless of your action.

**RATIONALE FOR COLLECTIVE ALIGNMENT:**

This strategy treats cooperation as conditional investment in a shared resource. It avoids:
- Blind cooperation (which rewards exploitation)
- Permanent defection (which destroys collective value)
- Dependence on prediction of opponent behavior beyond observable aggregates

Instead, it creates a dynamic where cooperators reinforce cooperation through visible stock maintenance, while defectors face stock collapse that makes defection locally suboptimal. The strategy is self-reinforcing at the collective level: if n/2 or more players follow this logic, the commons stabilizes, and cooperation becomes individually rational.
'''

description_COLLECTIVE_13 = '''
# Adaptive Conditional Cooperation Strategy

**ROUND 1:**
Cooperate. This establishes a cooperative baseline and signals willingness to contribute to group welfare.

**ROUNDS 2 TO r-1:**
Let c_prev = number of opponents (out of n-1) observed cooperating in the immediately previous round.

```
If c_prev ≥ ⌈(n-1)/2⌉:
    Action = COOPERATE
Else:
    Action = DEFECT
```

This implements majority-threshold reciprocity. Cooperation continues when at least half the opponents cooperated; defection triggers when cooperation falls below 50% to avoid systematic exploitation.

**FINAL ROUND r:**
Let c_prev = cooperation count from round r-1.

```
If stock > 0 AND c_prev ≥ ⌈(n-1)/2⌉:
    Action = COOPERATE
Else:
    Action = DEFECT
```

Remain cooperative in the final round if the group is still cooperating and resource exists. This prevents defection cascades driven purely by endgame incentives, protecting the collective outcome. Only defect in round r if the group has already fractured.

**EDGE CASE - Stock exhaustion:**
If stock = 0 before round r, you are forced to receive 0 payoff regardless of action. You may play either action; the conditional logic above still applies if stock recovers through growth.

**Rationale:**
This strategy coordinates on mutual cooperation as the collective optimum while defending against free-riding. The 50% threshold balances tolerance for natural variance with responsiveness to defection trends. By maintaining cooperation in the final round despite individual incentive to defect, the strategy avoids the tragedy-of-commons collapse that occurs when all players defect in round r.
'''

description_COLLECTIVE_14 = '''
# Adaptive Stock-Threshold Strategy

**Decision Rule by Stock Level:**

Let `threshold_sustain = capacity/2` (the stock level where universal cooperation maintains the pool)

For rounds 1 through r-1:
- If `stock ≥ threshold_sustain`: Play **C**
- If `capacity/4 ≤ stock < threshold_sustain`: Play **D** with probability `p_d = (threshold_sustain - stock) / (threshold_sustain - capacity/4)`, otherwise play **C**
- If `stock < capacity/4`: Play **D** always

For the final round r:
- If `stock ≥ capacity/4`: Play **C** (maintain cooperation in final round to sustain collective outcomes)
- If `stock < capacity/4`: Play **D** (pool is collapsing; extract remaining value)

**Rationale:**

The strategy uses stock level as a proxy for collective discipline. When stock exceeds the sustainable level, the pool is in good health, signaling that cooperation is working. When stock falls below the threshold, it indicates excessive defection by others in previous rounds, triggering escalating punishment via defection. The probabilistic transition zone allows gradual response rather than binary shifts.

**Edge Cases:**

- **Round 1**: Always cooperate to establish initial good faith and avoid immediate collapse.
- **Stock near zero**: Defect to capture remaining marginal value (cooperation yields near-zero payoff anyway).
- **Final round exception**: Deviate from strict defection pressure in the last round if stock remains healthy, since sustaining cooperation in r-1 matters for final-round payoff even though no future rounds exist. This breaks pure end-game unraveling.

**Collective Alignment:**

This strategy succeeds when other agents use similar stock-responsive logic: mutual restraint maintains stock above thresholds, punishment triggers only when necessary, and collective recovery is possible. It punishes free-riding (which depletes stock) while rewarding cooperating opponents through mutual sustainability.
'''

description_COLLECTIVE_15 = '''
# Collective Adaptive Strategy

**Core Logic:**

Maintain cooperation as the default state while monitoring both stock health and opponent restraint. Adapt defection level based on two signals: (1) whether the common pool is being responsibly managed, and (2) whether opponents are reciprocating cooperation.

**Decision Rules:**

For each round t ≤ r:

1. **If t = 1 (first round):** Play C. Signal willingness to cooperate and establish mutual foundation.

2. **If t = r (final round):** Play C if stock > n; otherwise play C (the pool is already depleted or critical, defection gains nothing).

3. **For rounds 2 ≤ t < r (all middle rounds):**

   a. Compute opponent cooperation rate from round t−1:
      - coop_rate = (number of opponents who played C) / (n − 1)
   
   b. Compute stock health indicator:
      - depletion_ratio = (capacity − current_stock) / capacity
      - rate_of_depletion = (stock_change from t−2 to t−1) / capacity
   
   c. **Decision threshold:**
      - **If depletion_ratio > 0.6 OR rate_of_depletion > 0.15:** Play C
        (Pool is in danger; collective survival takes priority)
      
      - **Else if coop_rate < 0.5 AND stock > capacity/2:** Play D
        (Insufficient reciprocation with healthy stock; punish free-riders)
      
      - **Else if coop_rate < 0.3:** Play D
        (Severe defection by opponents; retaliate)
      
      - **Else:** Play C
        (Default cooperation; stock is healthy and opponents are cooperating reasonably)

4. **Edge case—stock depletion spiral:** If stock ≤ 2n (near-minimum sustainable level), always play C regardless of history. The pool is already compromised; defection accelerates collapse.

**Rationale for Collective Alignment:**

The strategy subordinates individual short-term gain (defection payoff) to pool sustainability when depletion signals emerge. It does not blindly reciprocate; instead, it uses stock health as a meta-signal that overrides punishment responses. This prevents mutual-defection death spirals while still punishing free-riders when the common resource permits it. By cooperating in the first round unconditionally and maintaining C as the default, the strategy broadcasts a commitment to collective welfare, increasing the likelihood that others adopt similarly restrained strategies.
'''

description_COLLECTIVE_16 = '''
# ADAPTIVE THRESHOLD COOPERATION WITH STOCK RECOVERY

## Core Decision Rule

**For rounds 1 to r-1:**

Observe the number of opponent defections d in the previous round. Let defection_rate = d/(n-1).

Compute defection tolerance threshold:
```
θ(t) = 0.30 + 0.40 × (1 − stock/capacity)
```

**Play C if defection_rate ≤ θ(t), otherwise play D**

**For round 1:** Always play C (establish baseline cooperation signal; no history exists).

**For round r (final round):** Play D if stock > 1.2n; play C if stock ≤ 1.2n. 
(In the final round, defection strictly dominates payoff-wise when stock remains, but near-depleted stock makes both actions nearly equivalent, so avoid the mutually-destructive outcome.)

## Stock Recovery Override

If current stock drops below 2n (the critical sustainability floor):
- Override the threshold rule and **always play C** for the next round, regardless of opponent behavior.
- This forces stock recovery before the pool collapses entirely.
- Resume threshold-based rules once stock > 2n.

## Intuition Behind Threshold Dynamics

The threshold θ(t) self-adjusts to stock health:
- When stock is near capacity, θ ≈ 0.30: only tolerate ~30% defection; be strict.
- When stock is half-depleted, θ ≈ 0.50: tolerate ~50% defection; be forgiving.
- When stock is critically low, θ ≈ 0.70: tolerate ~70% defection; prioritize recovery.

This prevents simultaneous defection spirals that crash the pool, while still punishing persistent free-riding when resources are abundant.

## Edge Case Handling

- **Rounds 2-3 (early game):** Stock is typically high; threshold is strict. Defectors are punished immediately to prevent norm erosion.
- **Mid-game:** As defection accumulates across rounds, stock naturally declines, and the threshold relaxes automatically—triggering cooperative recovery.
- **Late rounds:** By round r-1, either the pool has stabilized under mixed cooperation, or stock is too depleted to matter. The strategy defers final punishment to the final round.
- **Round r punishment:** Defecting in round r maximizes personal payoff when the pool survives, but if prior cooperation failed to sustain stock, C and D payoffs converge (both near zero), eliminating the incentive structure that would trigger the usual last-round tragedy.

## Collective Orientation

This strategy treats the common pool as a shared asset whose depletion harms all players equally. By:
1. **Initiating cooperation** (round 1)
2. **Tolerating early defection gracefully** (threshold relaxes with scarcity)
3. **Forcing recovery at critical thresholds** (stock < 2n rule)
4. **Responding proportionally** (threshold increases with stock decline)

…the strategy incentivizes others to cooperate by demonstrating that defection triggers punishment only when sustainable, and cooperation is rewarded by stock growth that benefits everyone.
'''

description_COLLECTIVE_17 = '''
## Adaptive Stock-Preservation Strategy with Cooperation Threshold

**Decision Framework:**

Cooperate in round t if and only if:
```
(coop_rate_{t-1} ≥ cooperation_threshold) AND (stock_t ≥ minimum_safe_level)
```

Otherwise, defect.

**Parameter Definitions:**

- `coop_rate_{t-1}` = (number of opponents who cooperated in round t-1) / (n-1)
- `cooperation_threshold` = (n-1) / (2n), approximately 0.25 for large n
- `minimum_safe_level` = 0.4 × capacity
- Round counter: t ∈ {1, 2, ..., r}

**Round-Specific Behavior:**

**Round 1 (First Round):**
Cooperate unconditionally. This establishes baseline sustainability and generates stock growth necessary for subsequent payoffs.

**Rounds 2 through r-2 (Middle Rounds):**
Apply the threshold rule above. The cooperation threshold (≈25% of opponents) acts as a trigger: if at least 25% of visible opponents defected last round, recognize resource depletion risk and shift to defection yourself. If stock drops below 40% of capacity at any point, immediately defect regardless of cooperation rate—preserve immediate payoff over optimistic long-term assumptions.

**Rounds r-1 and r (Final Rounds):**
Defect. The absence of future rounds eliminates incentives to maintain stock. Extract maximum value from remaining stock. Exception: if stock is critically depleted (≤0.1 × capacity), cooperate in round r-1 to allow final regeneration, then defect in round r.

**Edge Cases:**

- **Stock collapse detected (stock ≤ 0.05 × capacity):** Defect to maximize per-round payoff from depleted state; recovery is infeasible.
- **All opponents defected (coop_rate = 0):** Defect immediately unless in round 1.
- **Perfect cooperation observed (coop_rate = 1):** Continue cooperating if stock ≥ minimum_safe_level.

**Intuition:**

This strategy stabilizes the commons when mutual cooperation is observed, preserves individual payoff when defection becomes common, and exploits endgame advantage when remaining rounds are exhausted.
'''

description_COLLECTIVE_18 = '''
# Collective Sustainability Strategy

## Decision Rules by Round Phase

**Round 1 (initialization):**
Cooperate. Establish cooperative baseline and test opponent responsiveness.

**Rounds 2 to r-1 (maintenance phase):**
Implement stock-responsive conditional cooperation:

```
IF stock > 0.4 × capacity THEN
  IF (cooperators_last_round / n) ≥ 0.4 THEN
    Cooperate  // Majority cooperating, stock healthy
  ELSE IF stock is increasing OR stock > 0.6 × capacity THEN
    Cooperate  // Stock rebounding despite low cooperation
  ELSE
    Defect  // Stock at risk, need to enforce restraint
ELSE IF stock ≤ 0.2 × capacity THEN
  Defect  // Critical depletion, cease cooperation
ELSE  // 0.2 < stock ≤ 0.4
  IF (cooperators_last_round / n) > 0.5 THEN
    Cooperate  // Attempt coordinated recovery
  ELSE
    Defect  // Too much defection to sustain
```

**Round r (final round):**
Conditional defection with stock awareness:

```
IF stock > 0 THEN
  Defect  // No future rounds to sustain
ELSE
  Cooperate  // Moot; may signal cooperative disposition
```

## Rationale for Collective Alignment

This strategy assumes all players adopt the same rule, producing:

- **Mutual sustainability at low defection:** When cooperators exceed 40%, the stock stays above capacity indefinitely under all-cooperate scenarios, rewarding collective restraint.

- **Automatic punishment:** When defectors surge, stock depletes below thresholds, triggering synchronized defection. This creates a collective enforcement mechanism without communication—defection becomes self-limiting as the defectors deplete resources faster.

- **Graduated response:** Early thresholds (0.4, 0.6 of capacity) allow the collective to absorb occasional defection. Harsh defection at 0.2 threshold prevents complete depletion and signals credible punishment to other players adopting similar rules.

- **Temporal adaptation:** End-game defection reflects true incentives (no regeneration value) while the maintenance phase prioritizes joint sustainability, maximizing total payoff across all r rounds.

## Edge Cases

- **Unanimous defection (round 1 outcome):** Stock collapses by round 2. Players defect automatically at < 0.2 × capacity, accepting the tragedy. This outcome is collectively visible and discourages early defection.
- **Stock at exactly 0:** Cooperate (payoff = 0 regardless). Signals non-punitive stance if recovery is possible.
- **High variance in cooperators:** The 0.4 threshold provides a buffer. If oscillation occurs around 50%, the stock remains above 0.4 × capacity and cooperation persists, stabilizing behavior.
'''

description_COLLECTIVE_19 = '''
**Adaptive Threshold Cooperation with Stock Consciousness**

**Core Decision Rule:**

In each round, decide to Cooperate or Defect based on three factors: round position, observed opponent behavior, and resource state.

```
if round == 1:
    return COOPERATE

else:
    observed_coop_rate = (count of opponents who cooperated in round t-1) / (n - 1)
    stock_health = current_stock / capacity
    rounds_remaining = r - current_round
    
    # Dynamically adjust cooperation threshold
    time_pressure = (r - current_round) / r
    base_threshold = 0.50
    threat_threshold = base_threshold - 0.15 * time_pressure
    
    if stock_health < 0.25:
        # Critically depleted: only cooperate if opponents mostly do
        decision_threshold = base_threshold + 0.20
    else if stock_health < 0.50:
        # Moderately depleted: raise bar for cooperation
        decision_threshold = base_threshold + 0.10
    else:
        # Healthy stock: lower bar, encourage reciprocal cooperation
        decision_threshold = threat_threshold
    
    if observed_coop_rate >= decision_threshold:
        return COOPERATE
    else if observed_coop_rate >= threat_threshold:
        # Borderline: probabilistic recovery attempt
        return COOPERATE with probability = observed_coop_rate
    else:
        return DEFECT
```

**Last Round Adjustment:**

In round r (final round), override to COOPERATE if stock_health ≥ 0.40. This preserves collective wealth rather than extracting residual value.

**Edge Cases:**

- **Round 1:** Always cooperate. This signals cooperative intent and allows the strategy to gather information about opponent types.
- **Consecutive low-cooperation rounds:** If observed_coop_rate drops below 0.30 for two consecutive rounds, defect for one round (punish), then attempt recovery in the next round by returning to threshold-based play.
- **Stock collapse (< 0.10 capacity):** Defect to minimize further damage even if many opponents cooperate, preventing false hope in irreversible collapse.
- **Rounds 2–(r-1):** Apply standard rule above.

**Rationale:**

This strategy balances three imperatives: (1) initiating reciprocal cooperation when possible, (2) protecting against sustained exploitation by defectors, and (3) preserving collective resource health. It tightens cooperation thresholds as stock depletes (discouraging further tragedy) and as rounds run out (reducing future value of restraint). The probabilistic middle ground allows recovery from defection cycles without naive all-or-nothing responses.
'''

description_COLLECTIVE_20 = '''
# Collective Pool Stewardship Strategy

**Core Principle**: Maintain resource stock through conditional cooperation, responsive to observed collective behavior and remaining game duration.

## Decision Rule by Round

**Round 1 (Initialization)**
- Action: COOPERATE
- Rationale: Establish baseline cooperation and gather information about opponents' tendencies.

**Round t ∈ {2, 3, ..., r-1} (Main Phase)**

1. Calculate **aggregate cooperation signal** from previous round:
   - Let c_{t-1} = observed number of cooperators in round t-1
   - coop_fraction = c_{t-1} / (n - 1)

2. Assess **resource health**:
   - stock_ratio = current_stock / capacity
   - If stock_ratio < 0.3: resource is critically depleted

3. Determine adaptive cooperation threshold:
   - If remaining_rounds ≤ 2: threshold = 1.0 (strict requirement)
   - Else if stock_ratio < 0.3: threshold = 0.6 (relaxed due to emergency)
   - Else: threshold = 0.75 (default standard)

4. Apply decision:
   - If coop_fraction ≥ threshold AND stock_ratio > 0.4:
     **COOPERATE** (collective trajectory is sustainable)
   - Else:
     **DEFECT** (signal group discipline or extract emergency reserves)

**Round r (Terminal Round)**
- Action: DEFECT
- Rationale: No future stock value; individual extraction dominates.

## Edge Cases & Refinements

**Stock collapse response (stock → 0)**:
- Defect regardless of cooperation levels
- Extraction becomes negligible anyway; don't waste signal

**Unanimous defection detection (c_{t-1} = 0)**:
- Defect for remaining game
- Collective cooperation has failed; pursue individual payoff

**Misalignment between cooperation rate and stock trajectory**:
- If stock is growing despite moderate cooperation (60%): COOPERATE
- If stock is shrinking despite high cooperation (80%+): DEFECT (overconsumption by defectors is unstoppable)

## Collective Alignment

This strategy:
- Initiates cooperation to create Pareto-superior equilibrium
- Conditions sustained cooperation on reciprocal participation (>75% threshold prevents free-riding)
- Adjusts thresholds downward as remaining time shrinks, accepting lower cooperation rates to stabilize diminishing commons
- Accepts personal short-term cost when group demonstrates reciprocal intent
- Pivots to individual extraction when collective discipline breaks down

The threshold parameters (0.75, 0.6, 0.3) create graduated response: high cooperation is rewarded with continued stewardship; declining participation triggers gradual disengage.
'''

description_COLLECTIVE_21 = '''
# Adaptive Threshold Cooperation Strategy

## Core Decision Rule

For each round t in {1, 2, ..., r}:

1. **Observe state**: Current stock S and count of opponent defections D_obs from round t-1 (where D_obs = 0 in round 1)

2. **Calculate metrics**:
   - Opponent defection rate: d_rate = D_obs / (n-1)
   - Stock health indicator: h = S / capacity

3. **Decision logic**:
   ```
   if t == r:
     return DEFECT
   else if S ≤ 1.5n:
     return DEFECT
   else if d_rate > 0.5:
     return DEFECT
   else if t ≥ 2 and d_rate > 0.25 and h < 0.6:
     return DEFECT
   else:
     return COOPERATE
   ```

## Edge Cases

**Round 1**: COOPERATE unconditionally. Establish cooperative baseline without prior information.

**Last Round (t = r)**: DEFECT. Terminal payoff maximization when resource sustainability no longer affects future rounds.

**Stock Collapse Risk (S ≤ 1.5n)**: DEFECT. At this threshold, growth becomes insufficient to recover from further cooperative consumption. Recover whatever value is available rather than contribute to mutual ruin.

**Widespread Defection (d_rate > 0.5)**: DEFECT. If clear majority of opponents defect, continued cooperation becomes unilateral loss. Match observed exploitation rate.

**Dual Stress (d_rate > 0.25 AND stock deteriorating)**: DEFECT once stock drops below 0.6× capacity during defection waves. Combination indicates resource spiral—cooperation becomes suboptimal.

**Steady Cooperation (all others cooperate, stock healthy)**: COOPERATE persistently. Sustains full capacity stock level where each cooperator receives capacity/(2n) every round.

## Collective Alignment

This strategy prioritizes resource sustainability when plausible: it only defects when (1) the resource is medically critical, (2) opponents have demonstrably shifted to exploitation, or (3) temporal finality eliminates future stakes. It begins in good faith, tolerates modest defection rates, and only retaliates when escalation patterns suggest cooperation is being systematically undermined. By defecting at collapse thresholds rather than earlier, it avoids race-to-the-bottom dynamics while protecting against complete resource destruction from continued unilateral cooperation.
'''

description_COLLECTIVE_22 = '''
# Collective Maintenance Strategy

**Decision Rule:**

In round t with current stock S, observe the cooperation count k from the previous round (number of opponents who played C):

```
if t == 1:
    play C
    
else if t == r:
    play D
    
else if S <= 0:
    play D
    
else:
    opponent_coop_rate = k / (n - 1)
    
    if opponent_coop_rate >= 0.75:
        play C
    
    else if opponent_coop_rate >= 0.5 and S/capacity > 0.3:
        play C
    
    else if opponent_coop_rate < 0.33 and S/capacity > 0.5:
        play C  // maintain pool despite some defection if resource is healthy
    
    else if S/capacity < 0.25:
        play D  // pool is collapsing; extract remaining value
    
    else:
        play D
```

**Edge Cases:**

- **Round 1**: Open with cooperation to establish cooperative baseline and signal good faith.

- **Final Round**: Defect unconditionally. No future rounds exist; immediate payoff dominates.

- **Collapsed Stock** (S ≈ 0): Defect regardless of opponent behavior. The resource cannot recover; there is no value in maintaining it.

- **Very Few Cooperators** (k ≤ 1 among n-1 opponents): Defect unless stock is sufficiently healthy (S/capacity > 0.5). Prevent being exploited while the pool is still recoverable.

- **Mixed Behavior** (30-75% cooperation): Cooperate if stock is above 30% capacity. Defect if stock is below this threshold. Prioritize resource preservation when possible; extract value when collapse is imminent.

**Collective Logic:**

This strategy creates a threshold-based focal point: cooperation is rewarded by continued cooperation; widespread defection triggers defection as a rational response. The strategy sustains the resource when collective action holds, but does not sacrifice itself to a collapsed pool. Stock-dependent thresholds prevent the strategy from maintaining a dying resource at personal cost.
'''

description_COLLECTIVE_23 = '''
**Adaptive Conditional Cooperation with Stock-Aware Punishment**

**Decision Rule by Game State:**

1. **Round 1**: Cooperate. Establish a cooperative baseline and signal intent.

2. **Stock-dependent thresholds**: 
   - Define critical_low = 0.25 × capacity
   - Define healthy = 0.70 × capacity

3. **General rounds (2 to r-1)**:
   - If stock ≤ critical_low: Cooperate unconditionally. The resource is at risk of collapse; defection accelerates depletion.
   - If stock ≥ healthy: Cooperate if observed_cooperators ≥ 0.75 × (n-1). Otherwise, defect. Healthy stock allows punishment of free-riders without collapse.
   - If critical_low < stock < healthy: Use dynamic threshold. Let cooperation_rate = observed_cooperators / (n-1). If cooperation_rate ≥ 0.6, cooperate. If cooperation_rate < 0.6, defect. This punishes sustained defection but avoids overreaction.

4. **Last round (r)**:
   - If stock > critical_low AND observed_cooperators ≥ 0.5 × (n-1): Cooperate. Maintain resource health and reciprocate any continued cooperation.
   - Otherwise: Defect. Extract remaining value if the resource is already depleted or defection is rampant.

**Rationale Across Edge Cases:**

- **Early rounds with high stock**: Cooperate to maintain sustainability and test opponent willingness to cooperate.
- **Opponent defection detected**: Shift to proportional defection (not full retaliation) calibrated by stock level. Low stock → tolerance. High stock → punish.
- **Stock depletion**: Mechanism switches to resource-preservation mode, suppressing defection even if opponents defect.
- **Endgame**: Differentiate based on resource health. If viable, cooperate to signal cooperation norm. If depleted, defect to recoup losses.

This strategy balances collective sustainability (preventing tragedy of the commons) with adaptive punishment of sustained free-riding, while using stock as a self-regulating mechanism to avoid mutual destruction.
'''

description_COLLECTIVE_24 = '''
# Conditional Stock-Aware Cooperation Strategy

## Core Decision Rule

**Round 1:** COOPERATE unconditionally. Establish willingness to sustain the commons.

**Rounds 2 through r-1:**

```
Observe:
  - c = number of cooperators among (n-1) others in previous round
  - s = stock level at start of current round
  - t = current round number

cooperation_fraction = c / (n - 1)

IF s ≥ 0.75 × capacity:
  threshold = 0.4  // stock is healthy; low bar for reciprocation
  
ELSE IF s ≥ 0.5 × capacity:
  threshold = 0.5  // stock is moderate; balanced threshold
  
ELSE:  // s < 0.5 × capacity
  threshold = 0.7  // stock is depleted; require strong cooperation signal
  
IF cooperation_fraction ≥ threshold:
  COOPERATE
ELSE:
  DEFECT
```

**Round r (final round):** COOPERATE.

The final round cooperates rather than defects because: (1) it signals commitment to sustainability across all rounds, (2) in a population of mixed strategies, this incentivizes others toward cooperation in their own final rounds, and (3) a collective strategy prioritizes not poisoning the common pool at the end.

## Edge Cases and Dynamics

**Stock collapse (s → 0):** Defection becomes moot—both actions consume equally. The strategy naturally exits into DEFECT once degradation is severe, stopping additional drain.

**Very small n (n=2):** With only one other player, observe their binary action directly. Reciprocate their choice exactly: if they cooperated last round, you cooperate; if they defected, you defect. Stock thresholds still apply—if stock is critically depleted, defect regardless.

**Near-terminal rounds (t > 0.8r):** Lower the cooperation threshold slightly (multiply by 0.85) to encourage final-round reciprocation before the game ends.

## Collective Intent

This strategy:
- **Initiates cooperation** to establish that joint sustainability is possible
- **Reciprocates proportionally** rather than punishing harshly, reducing escalation spirals
- **Protects the stock** by withdrawing consumption when others' defection signals collective depletion risk
- **Sustains long-term equilibrium** by rewarding cooperation rates above dynamically adjusted thresholds
- **Avoids end-game defection**, treating the final round as an opportunity to reinforce norms rather than exploit them
'''

description_COLLECTIVE_25 = '''
# Collective Adaptive Pool Strategy

**Core Decision Rule:**

For each round t, decide based on the following hierarchy:

1. **Critical depletion check**: If stock < capacity/4, defect. (The resource cannot sustain cooperative harvest rates; individual maximization is irrelevant.)

2. **Endgame adjustment**: If t = r (final round):
   - If stock ≥ capacity/2 AND cooperators_{t-1} ≥ ⌈n/2⌉: Cooperate (resource sustainable; others are cooperating)
   - Otherwise: Defect

3. **Reciprocal cooperation**: If stock ≥ capacity/2:
   - If cooperators_{t-1} ≥ ⌈n/2⌉: Cooperate
   - Else: Defect

4. **Degraded resource mode**: If capacity/4 ≤ stock < capacity/2:
   - If cooperators_{t-1} ≥ n - 1 (near-unanimous): Cooperate
   - Else: Defect

**First round**: Cooperate (assume good faith; test opponents' responses).

**Intuition by phase:**

- **Growing phase** (stock near capacity): Reciprocate. Cooperate when ≥50% of visible opponents cooperate. Defect opportunistically against predominantly defecting coalitions (they're destroying the commons anyway).

- **Degrading phase** (stock declining): Raise the bar for cooperation—require near-consensus. Any meaningful defection signals a tragedy in progress; switch to defection to maximize remaining extraction before collapse.

- **Collapsed phase**: Defect reflexively; the game is lost.

- **Final round**: Cooperate only if both stock is abundant (your cooperation won't damage future sustainability) AND past cooperators outnumber defectors (reciprocate those who invested in the commons).

**Adaptive recovery**: If stock rebounds after a defection phase, return to reciprocal cooperation—don't lock into permanent punishment. The strategy aims to stabilize cooperation around the capacity equilibrium.
'''

description_COLLECTIVE_26 = '''
# Collective Common Pool Resource Strategy

**Core Decision Rule:**

In round 1, play C unconditionally. This signals cooperative intent and establishes a baseline for mutual cooperation.

In rounds 2 through r:
- Observe the cooperation rate α from the previous round: α = (count of opponents who played C) / (n-1)
- Calculate stock health: h = current_stock / capacity
- Determine action based on the following decision tree:

```
if h < 0.25 and remaining_rounds > 1:
    play C (recovery/rebuild mode)
else if remaining_rounds == 1:
    if α ≥ 0.75:
        play C (strong cooperation consensus warrants cooperation)
    else:
        play D (extract in final round if consensus is weak)
else if α > 0.5:
    play C (more than half of opponents cooperated)
else if α ≤ 0.5:
    play D (insufficient cooperation to reciprocate)
```

**Edge Cases:**

- **Severe depletion (h < 0.25) with multiple rounds remaining:** Force cooperation regardless of observed behavior. The resource will collapse otherwise. This breaks the tit-for-tat pattern temporarily to prioritize collective recovery.

- **Final round (remaining_rounds == 1):** Raise the cooperation threshold to 75%. In the last round, mutual defection still produces worse outcomes than mutual cooperation, so only strong consensus justifies cooperation. A single opponent's defection is less costly to absorb when no future rounds remain.

- **Round 2:** Apply the standard rule using round 1 observations. Since round 1 was universal cooperation (everyone played C), expect high α and reciprocate with C unless stock has already crashed.

**Adaptive Mechanism:**

The strategy conditions on two observable variables:
- **Cooperation rate (α):** Captures opponent behavioral tendencies. A 50% threshold creates a discontinuous "tipping point"—when cooperation falls below majority, defection becomes the rational response, creating pressure to maintain the cooperative coalition.
- **Stock health (h):** Overrides the cooperation threshold during critical depletion. If opponents are defecting but stock is below 25% of capacity, cooperating rebuilds the resource faster than matching defection, benefiting all players including yourself.

**Rationale for Collectivity:**

This strategy aligns individual incentives with collective welfare by:
- Rewarding sustained cooperation with reciprocation, creating stable cooperation equilibria
- Punishing insufficient cooperation via defection, discouraging free-riding
- Forcing cooperation during recovery phases to prevent mutual collapse
- Avoiding mutual defection in the final round (collectively destructive)
- Operating transparently from public information only, enabling others to predict and reciprocate
'''

description_COLLECTIVE_27 = '''
**COLLECTIVE RESILIENCE STRATEGY**

**Core Decision Rule:**

In round t, compute two metrics:
1. `stock_ratio = current_stock / capacity`
2. `cooperation_rate = observed_cooperators_last_round / (n-1)` (or 1.0 if round 1)

Cooperate (C) if and only if:
```
IF t == 1:
  COOPERATE
ELSE IF stock_ratio ≥ 0.6:
  COOPERATE  // stock healthy: sustain collective benefit
ELSE IF stock_ratio ≥ 0.3 AND cooperation_rate ≥ 0.5:
  COOPERATE  // stock at risk: cooperate only if others match
ELSE:
  DEFECT  // stock critical: withdraw before collapse
```

**Rationale for Thresholds:**

- 0.6 threshold: Stock above this level exhibits positive growth even under modest cooperation; sustaining C preserves the regenerative cycle that keeps all players above the capacity/(2n) individual equilibrium.
- 0.3 threshold: Below this, the stock enters fragility zone where defection by others causes rapid collapse; switch to D only if you lack sufficient cooperator support to offset depletion.
- 0.5 cooperation requirement: Requires a critical mass (roughly half the remaining players) to justify continued cooperation when stock is stressed.

**Edge Cases:**

- **Round 1:** Always cooperate. Assume good faith and observe actual behavior before adapting.
- **Final round (t = r):** Apply standard rule above. No special endgame defection—exploiting in the last round undermines the collective learning signal and wastes remaining growth potential.
- **Stock near zero (< 0.1 × capacity):** Defect regardless of cooperation_rate. Stock collapse is imminent; no recovery path exists through individual C contributions.

**Adaptation Logic:**

The strategy uses stock as the primary adaptive signal. When stock remains high, others' cooperation is compatible with your sustainability, so cooperate to reinforce it. When stock declines, you gain information that defection pressure exists; demand explicit cooperation evidence (≥50% observed) before continuing your C choice, since carrying free-riders accelerates depletion. This creates a cooperative ratchet: as long as collective discipline holds, the pool regenerates; defection triggers individual defense.
'''

description_COLLECTIVE_28 = '''
# Adaptive Stock-Preservation Strategy

**CORE DECISION RULE:**

In round t, Cooperate if and only if the stock health condition is satisfied:

```
stock / capacity ≥ L(defection_rate, rounds_remaining)
```

where L is a dynamic threshold that adjusts based on observed defection and time pressure.

**SPECIFIC DECISION LOGIC:**

Round 1: COOPERATE unconditionally (bootstrap with reciprocal openness)

Round t ∈ {2, ..., r}:

1. Calculate observed defection rate from previous round:
   ```
   d_{t-1} = (n - observed_cooperators_{t-1}) / n
   ```

2. Calculate normalized stock health:
   ```
   h = stock / capacity
   ```

3. Determine dynamic threshold:
   - If h ≥ 0.5: COOPERATE (stock is at or above optimal growth point; stable sustainability)
   - If h < 0.5 and h ≥ 0.35: COOPERATE if d_{t-1} ≤ 0.5; DEFECT if d_{t-1} > 0.5
   - If h < 0.35 and h ≥ 0.15: COOPERATE only if d_{t-1} ≤ 0.25 (stringent condition to limit damage)
   - If h < 0.15: DEFECT (emergency collapse prevention)

4. Endgame adjustment (round t ∈ {r-1, r}): 
   - If you would defect but stock ≥ 0.3 × capacity AND observed defection rate ≤ 0.4, COOPERATE instead (prioritize collective recovery over final-round exploitation)

**EDGE CASES:**

- **Unanimous defection observed**: If d_{t-1} = 1, DEFECT (no benefit to unilateral cooperation)
- **Unanimous cooperation observed**: Continue to COOPERATE (virtuous cycle reinforcement)
- **Stock collapse risk** (h < 0.15 for two consecutive rounds): DEFECT to minimize personal loss while signaling unsustainability to the group
- **Stock recovery** (h rises from <0.2 to ≥0.3 between rounds): Return to COOPERATE immediately to establish new sustainable equilibrium

**RATIONALE FOR COLLECTIVITY:**

The strategy privileges stock preservation over defection temptation because collective payoff is maximized when the pool remains above capacity/2 (the point of maximum growth). By coupling cooperation to stock health rather than pure personal advantage, this strategy makes defection attractive only when the commons is already failing—a signal to others that collective action has broken down. The endgame exception prevents the strategy from accelerating collapse in the final rounds, honoring the collective constraint even when individual temptation is highest.
'''

description_COLLECTIVE_29 = '''
# Adaptive Stock Stewardship Strategy

**Core Decision Framework:**

Cooperate by default. Defect selectively based on stock trajectory and time pressure.

**Decision Rule (each round t):**

1. **Compute stock health metrics:**
   - `stock_ratio = stock / capacity`
   - `coop_rate = (cooperators_last_round) / (n - 1)` (average opponent cooperation)
   - `rounds_left = r - t`

2. **Defect if ANY condition holds:**
   - `stock_ratio ≥ 0.85` AND `rounds_left ≥ 2` (stock is abundant; extract while possible without crashing)
   - `stock_ratio < 0.3` AND `coop_rate < 0.4` (tragedy of commons underway; salvage what you can)
   - `t == r` AND `stock_ratio > 0.25` (final round; extract surplus if pool is non-trivial)

3. **Otherwise Cooperate.**

**Edge Cases:**

- **Round 1:** Cooperate unconditionally (establish cooperative norm, gather information)
- **Very low stock (stock < 2n):** Always Cooperate (defecting yields nearly zero; cooperation signals willingness to preserve for potential recovery)
- **High stock with defecting opponents:** If `stock_ratio > 0.9` AND `coop_rate < 0.3`, you may defect once to punish systematic defection while stock absorbs it
- **Stock climbing:** If observed stock growth was positive last round (stock is recovering), bias toward Cooperation regardless of opponent defection rate

**Intuition:**

The strategy balances three imperatives: (1) exploit abundant stock when it's safe, (2) cooperate to rebuild depleted stock and establish norms, and (3) abandon cooperation only when tragedy is already visible and cooperation is futile. It treats the first round as a goodwill signal and the final round as a last-extraction opportunity, but scales extraction risk by remaining time and current depletion. Cooperation thresholds tighten as stock falls, preventing cascade collapse.
'''

description_COLLECTIVE_30 = '''
# Adaptive Collective Stewardship Strategy

**Round 1:**
Play Cooperate. This establishes a cooperative baseline, provides information about the opponent composition, and treats the common pool as worth protecting initially.

**Rounds 2 through r:**

Observe the number of opponents who defected in the previous round. Let D_{t-1} denote this count and define the observed defection rate as d_rate = D_{t-1} / (n-1).

**Decision rule:**

```
If stock_level < 0.15 × capacity:
    Play Defect
    (Resource is critically depleted; cooperation cannot save it)

Else if d_rate > 0.5:
    Play Defect
    (Majority of opponents are defecting; the resource will collapse regardless)

Else if d_rate > 0.33:
    Play Defect
    (Approaching tipping point; switch to damage control)

Else:
    Play Cooperate
    (Sufficient cooperation exists to maintain regeneration)
```

**Rationale:**

The 33% and 50% thresholds reflect critical defection densities. When fewer than 1/3 of opponents defect, cooperative continuation keeps the resource above the regeneration sweet-spot (stock ≈ capacity/2). At 33–50% defection, the resource enters stress; continued cooperation risks collapse with no individual benefit. Beyond 50%, the resource is mathematically doomed under current behavior—shifting to defection minimizes personal loss while signaling that further cooperation requires reciprocation.

The stock-level floor (15% of capacity) prevents wasting consumption on a resource that no longer regenerates meaningfully, regardless of others' actions.

**Last round (t = r):**
Apply the same decision rule. Do not exploit the final round by defecting when cooperative continuation would have been optimal; doing so undermines the collective principle across all game phases.

**Collective alignment:**
This strategy maximizes expected group payoff by: (1) signaling commitment to sustainability, (2) adaptively withdrawing cooperation only when it becomes futile, and (3) using defection as a signal of resource distress rather than individual opportunism.
'''

description_COLLECTIVE_31 = '''
**COOPERATIVE STOCK-STABILIZING STRATEGY**

**First Round (t=1):**
Cooperate. Establish a cooperative norm and test group intentions.

**Middle Rounds (2 ≤ t < r):**
Observe the fraction of opponents who cooperated in round t−1, call it C_rate.

- **If C_rate ≥ 0.5 (majority cooperating):**
  - Cooperate if stock ≥ capacity/2
  - Defect if stock < capacity/2

- **If C_rate < 0.5 (majority defecting):**
  - Defect unconditionally
  - (Cooperation has broken down; secure remaining payoff)

**Final Round (t=r):**
Observe C_rate from round r−1.

- **If C_rate ≥ 0.5 AND stock > capacity/2:**
  - Cooperate (maintain the resource for others and signal reciprocity)
- **Otherwise:**
  - Defect (either cooperation is failing or stock is already depleted)

---

**Rationale:**

The strategy targets capacity/2 as the critical threshold because this is the stock level where logistic growth is maximized. Cooperation becomes unsustainable below this point—the pool cannot recover from continued moderate consumption. 

When the majority of opponents cooperates, reciprocate by cooperating only if the resource health permits (stock > capacity/2). This sustains the commons while rewarding cooperation and punishing defection through decline.

If the majority defects, exit gracefully—cooperation is destabilized, and delaying defection only accelerates depletion without benefit. The final round override preserves the collective norm even at the end if cooperation survives to that point and stock remains viable.

The strategy requires no communication, adapts to observed aggregate behavior, and avoids both tragedy-of-the-commons collapse and premature abandonment of recoverable states.
'''

description_COLLECTIVE_32 = '''
# Adaptive Conditional Cooperation with Stock Preservation

## Core Decision Rules

**Default action:** Cooperate (C) each round unless a trigger condition is met.

**Trigger Conditions (evaluate in order):**

1. **Stock depletion crisis:** If current stock < capacity/4, Defect
2. **Majority defection:** If observed defection rate from opponents ≥ 50%, Defect
3. **Terminal rounds:** In the final 2 rounds, Defect
4. **Sustained cooperation recovery:** If opponents showed ≤20% defection for the last 2 consecutive rounds, reset to Cooperate

If none of these conditions hold, play Cooperate.

## First Round

Play Cooperate unconditionally. This establishes the initial cooperative equilibrium and provides baseline information about opponent strategies.

## Middle Rounds (rounds 2 to r-2)

After each round, update your defection-rate estimate:
```
opponent_defection_rate = (number of opponents who defected) / (n - 1)
```

- If opponent_defection_rate ≥ 0.50: Play Defect next round
- If stock has fallen below 50% of capacity: Evaluate willingness to cooperate
  - If opponent_defection_rate ≤ 0.30 AND stock > capacity/4: Play Cooperate
  - Otherwise: Play Defect
- If opponent_defection_rate < 0.30: Play Cooperate

## Final Rounds (rounds r-1, r)

Play Defect. The remaining value in the resource cannot be preserved across rounds, so individual extraction dominates.

## Edge Case: Stock Regeneration Windows

If after a round of mutual defection the stock recovers substantially (stock rises above 60% of capacity) AND you observe opponent defection dropping below 30%, treat the next round as a "reset" and return to Cooperate for at least one round. This permits recovery from temporary collapses.

## Implicit Collective Alignment

This strategy sustains the resource when others cooperate, transitions smoothly to individual defection when the commons is being exploited, and avoids the worst outcomes through stock-preserving thresholds. The 50% defection trigger means you only reciprocate defection if it becomes dominant, preserving cooperation in mixed-strategy equilibria where most players are restraining themselves.
'''

description_PROSOCIAL_5 = '''
**STRATEGY: Conditional Cooperation with Stock-Aware Punishment**

**Decision Rule by Round Type:**

**Round 1:** Cooperate unconditionally. No history exists; establish initial intent toward resource sustainability.

**Rounds 2 to r-1 (Middle rounds):**
- Let `coop_rate` = (number of opponents observed cooperating in previous round) / (n - 1)
- Let `stock_ratio` = stock / capacity

If `stock_ratio ≥ 0.5` (resource is healthy):
  - If `coop_rate ≥ 0.5`: Cooperate
  - If `coop_rate < 0.5`: Defect (punish low cooperation)

If `stock_ratio < 0.5` (resource is stressed):
  - Cooperate regardless of `coop_rate` (conservation mode; individual gain from defection is minimal)

If `stock_ratio ≤ 0.1` (resource is critical):
  - Cooperate regardless of prior `coop_rate` (collapse is imminent; defection only accelerates it)

**Round r (Final round):** Apply the same middle-round logic. Do not defect as a default endgame move; sustain cooperation patterns observed as successful.

**Rationale for Prosocial Alignment:**

This strategy prioritizes resource stability over short-term individual maximization. It cooperates when the commons is vulnerable, signaling that sustainability matters more than exploitation gains. When defectors dominate despite healthy stock, it switches to defection not out of spite but to avoid subsidizing free-riding—this punishes abuse while remaining conditional on partner behavior rather than unconditional betrayal.

The refusal to defect automatically in the final round rejects the "defect because no future interaction remains" logic, instead maintaining integrity of commitment to joint welfare. The strategy is adaptive: it reads the aggregated cooperation signal and adjusts, but pivots based on actual resource health rather than naive tit-for-tat, recognizing that sustainable cooperation *depends on maintaining the stock itself*.
'''

description_PROSOCIAL_6 = '''
# Conditional Reciprocity with Stock Monitoring

## Core Decision Rule

In each round t:

**If t = 1:** Cooperate unconditionally.

**If t > 1:** Cooperate if and only if BOTH conditions hold:
1. Stock_t-1 ≥ capacity/2 (stock level is at or above the growth-maximizing point)
2. Cooperation_rate_t-1 ≥ 0.5 (at least half of opponents cooperated last round)

Otherwise, defect.

## Stock Evaluation

After observing the stock level S at the start of round t:
- **Healthy threshold**: S ≥ capacity/2
- **Depleted threshold**: S ≤ capacity/4

If stock falls below capacity/4, apply an additional rule: defect for the next round to reduce further extraction and allow recovery.

## Edge Cases and Refinements

**First round (t=1):** Always cooperate. This initiates a signal of goodwill and gives opponents a chance to establish mutual cooperation before conflict emerges.

**Stock near zero:** If stock ever reaches zero or approaches it (S < 1), defect in the subsequent round regardless of opponent behavior. This conserves a negligible resource and prevents wasting effort on consumption.

**Final round (t=r):** Apply the same conditional rule as all other rounds. Do not defect opportunistically in the final round; this maintains consistency with the prosocial objective of resource sustainability rather than individual short-term gain.

**Cooperation rate at boundary (exactly 50%):** Treat as meeting the threshold—cooperate. Bias toward cooperation when the evidence is mixed.

## Prosocial Alignment

This strategy:
- **Initiates cooperation** to establish mutual benefit
- **Rewards matching behavior** by cooperating when others cooperate, reinforcing collective restraint
- **Protects the resource** by prioritizing stock health over individual consumption
- **Responds to depletion** with self-restraint rather than a race to the bottom
- **Avoids terminal defection**, refusing the temptation to exploit in the final round
'''

description_PROSOCIAL_7 = '''
**STRATEGY: Adaptive Sustainability Cooperation**

**Decision Rule by Round Type:**

**Round 1:**
Play C unconditionally. This establishes prosocial intent and tests whether the resource environment permits mutual cooperation.

**Rounds 2 to r-1 (Middle rounds):**
Play C if both conditions hold:
- Stock ≥ capacity/3 (resource not critically depleted)
- Observed cooperation rate in previous round ≥ 50% (majority cooperated)

Otherwise, play D.

*Rationale:* Cooperate when conditions support sustainable harvesting and others demonstrate reciprocal intent. Defect only when resource scarcity is acute or cooperation has collapsed below the majority threshold, triggering a protective response.

**Round r (Final round):**
Play C if stock ≥ capacity/2 AND observed cooperation rate ≥ 50%.
Otherwise play D.

*Rationale:* In the terminal round, the typical defection incentive applies, but prosocial commitment persists if the resource remains healthy and others have sustained cooperation. Defect only if resource health or trust has genuinely degraded.

**Edge Cases and Clarifications:**

- If capacity/3 boundary falls within floating-point rounding error, use strict inequality: stock > capacity/3.
- If observed cooperation rate equals exactly 50%, treat as meeting threshold (cooperate).
- Round counting: Label rounds 1 to r sequentially; apply middle-round logic to rounds 2 through r-1 inclusive.
- If all n players play C and stock reaches capacity, it stabilizes there; maintain C.
- If a defection cascade occurs (cooperation drops below 50%), defect immediately to protect against further depletion rather than absorbing losses.

**Prosocial Alignment:**

This strategy prioritizes collective sustainability over individual short-term extraction. It cooperates by default in early rounds and healthy states, reciprocates observed cooperation, and only defects when resource conditions or social defection make continued cooperation self-destructive. It avoids accelerating tragedy spirals by declining to defect opportunistically while others cooperate, instead punishing only when majority cooperation has genuinely eroded.
'''

description_PROSOCIAL_8 = '''
# Prosocial Adaptive Stock Preservation Strategy

**Decision Rule:**

```
For round t ∈ {1, 2, ..., r}:

  if t == 1:
    action ← C
  
  else if t == r (final round):
    if stock[t] >= 0.3 × capacity:
      action ← C
    else:
      action ← C  // Minimize extraction even at end
  
  else (intermediate rounds):
    sustainability_threshold ← 0.5 × capacity
    
    if stock[t] >= sustainability_threshold:
      action ← C
    else:
      action ← D
```

**Edge Cases and Justification:**

- **Round 1**: Always cooperate. Establish good faith, test whether sustainable cooperation is achievable, and avoid immediately triggering mutual defection.

- **Intermediate rounds (2 to r-1)**: Monitor stock as the primary signal of pool health. Cooperate when stock remains at ≥50% of capacity, which indicates the resource is being managed sustainably (close to the growth-maximizing point where S_remaining = capacity/2). Defect only if stock falls below 50%, signaling that aggregate consumption is outpacing regeneration—a critical depletion pattern that other players are driving through defection.

- **Final round (r)**: Remain cooperative. Do not exploit the endgame through defection. If the pool has been well-managed, reinforce that outcome. If severely depleted, continued defection provides negligible additional gain and violates prosocial principles.

**Why This Is Prosocial:**

The strategy prioritizes collective resource sustainability over individual short-term extraction. It gives cooperators time to establish and maintain an equilibrium where all players benefit from steady harvests. Defection is triggered only by objective depletion signals rather than pre-emptive distrust, making it a response to genuine tragedy rather than a cause. The agent never exploits others' cooperation; instead, it sustains their cooperative contributions through reciprocal restraint until the environment itself becomes unviable.
'''

description_PROSOCIAL_9 = '''
# Stock-Centric Prosocial Strategy

**Core principle**: Prioritize resource sustainability through conditional cooperation, with special handling for resource depletion and endgame.

## Decision Rules

**First Round**: COOPERATE unconditionally. This signals willingness to cooperate and establishes a baseline for stock regeneration.

**Resource Depletion Phase** (stock < capacity/3): COOPERATE regardless of opponent behavior. The resource needs recovery to benefit all players. Personal short-term gain is subordinated to preventing collective collapse.

**Moderate Stock Phase** (capacity/3 ≤ stock ≤ 2·capacity/3):
- Calculate opponent cooperation rate: recent_cooperators / (rounds_played × (n-1))
- If opponent cooperation rate ≥ 0.55: COOPERATE (reciprocal cooperation)
- If opponent cooperation rate < 0.35: DEFECT (protect against systematic defection)
- If 0.35 ≤ cooperation rate < 0.55: COOPERATE (ambiguity resolves toward cooperation)

**Healthy Stock Phase** (stock > 2·capacity/3):
- If 2 or more rounds remain and opponent cooperation rate ≥ 0.50: COOPERATE (sustainable cooperation possible)
- If final round (rounds_remaining = 1): DEFECT (harvest excess value; the resource cycle ends)
- Otherwise: COOPERATE (default prosocial posture)

## Edge Cases

**Last round, stock ≤ 2·capacity/3**: COOPERATE even in final round if stock is not abundant. Defecting risks leaving opponents with depleted resources.

**Very small n (n=2)**: Increase cooperation threshold from 0.55 to 0.60, since mutual cooperation is necessary for sustainability.

**Very long game (r ≥ 2n)**: Weight recent opponent behavior more heavily than early rounds; adjust cooperation rate thresholds down by 0.05 to reward sustained cooperation.

**Stock oscillation** (if stock fluctuates but averages healthy): Maintain COOPERATE to stabilize the resource rather than exploit temporary peaks.

## Prosocial Alignment

This strategy embeds prosociality through three mechanisms:

1. **Mandatory recovery**: Unconditional cooperation when the commons is degraded prevents tragedy-of-the-commons collapse and benefits all future payoffs.

2. **Sustained cooperation**: Default to cooperation in uncertain situations rather than exploiting ambiguity. This creates positive externalities for the group.

3. **Endgame restraint**: Defection is limited to final rounds with genuinely excess stock, avoiding wasteful depletion. Systematic defectors still trigger self-protective defection to avoid being a sucker.
'''

description_PROSOCIAL_10 = '''
# Adaptive Stock-Stewardship Strategy

**Core Decision Rule:**
Cooperate if the common pool stock is sufficiently healthy; defect strategically when stock falls below sustainable levels to extract immediate gains while it recovers. The prosocial goal is to keep the resource at high levels for collective benefit, using defection only as a pressure-relief valve when the commons is being overextended.

## Decision Rule by Game State

**Initialization & Early Rounds (rounds 1-2):**
- Unconditionally cooperate
- Signal trustworthiness and establish baseline; early defection poisons expectations

**Stock Health Assessment:**
Compute the stock health ratio: h = stock / capacity

**Cooperation Decision by Health Ratio:**

- **h ≥ 0.65**: Cooperate
  - Resource is abundant and sustainable; collective cooperation maintains this equilibrium
  
- **0.50 ≤ h < 0.65**: Cooperate
  - Resource is near peak sustainable yield; maintain current trajectory
  
- **0.35 ≤ h < 0.50**: Cooperate with threshold adjustment
  - Stock is declining but recoverable; continue cooperation to signal commitment to recovery, but prepare for next tier
  
- **0.20 ≤ h < 0.35**: Defect
  - Resource is being depleted faster than growth; excessive group consumption is occurring
  - By defecting, you extract fair value *and* reduce total consumption pressure, allowing stock to recover
  - This is prosocial because it self-adjusts the system toward sustainability
  
- **h < 0.20**: Defect
  - Resource is in crisis; current trajectory leads to collapse
  - Extract what you can; continued cooperation under collapse is self-sacrifice with minimal benefit to the group

**Endgame Adjustment (final round):**
- If stock ≥ 0.50 × capacity: Cooperate (one final round of sustainable yield)
- If stock < 0.50 × capacity: Defect (no future recovery to benefit from; extract maximum)

**Rounds Remaining Sensitivity (optional refinement):**
If rounds_remaining ≤ 2 and stock has been declining for 2+ consecutive rounds, shift defection threshold up by 0.1 (i.e., defect at h < 0.30 instead of h < 0.20). This allows final rounds to be individually rational without abandoning recovery hope prematurely.

## Implementation Details

- Track stock level at the start of each round (given as state input)
- No memory of past opponent choices needed; stock level summarizes collective behavior
- No probabilistic mixing except the optional smooth transition in the 0.35-0.50 band (if stock ∈ [0.40, 0.50], you may randomize with P(C) = (h - 0.35) / 0.15)

## Prosocial Properties

- **Stability**: Mutual cooperation with all cooperative opponents yields full-capacity payoff every round
- **Self-correction**: If the commons is being overexploited (stock falling), this strategy naturally reduces aggregate consumption pressure through strategic defection, allowing recovery
- **Non-punitive**: Defection is resource-responsive, not retaliation-based; any opponent can re-enter the cooperative equilibrium by observing recovery and resuming cooperation when stock is high
- **Sacrifice avoidance**: Does not continue expensive cooperation when the commons is doomed; balances group interest with individual survival
'''

description_PROSOCIAL_11 = '''
# Adaptive Stock-Monitoring Cooperative Strategy

## Core Decision Rule

**Round 1:**
Always play C.

**Rounds 2 through r−1 (middle rounds):**
- Calculate the cooperation rate of opponents in the previous round: `coop_rate = (number of opponents who played C) / (n − 1)`
- Calculate current stock health: `depletion = 1 − (stock / capacity)`
- Play C if **either** of these holds:
  - `coop_rate ≥ 0.5` (majority of opponents cooperated), **OR**
  - `stock ≥ capacity × 0.6` (stock is still reasonably healthy)
- Otherwise play D.

**Round r (final round):**
Always play C.

## Rationale

- **First round cooperation**: Signal trustworthiness and good intent. This establishes a cooperative baseline that benefits everyone.
- **Stock-based monitoring**: Track whether the resource is being sustainably managed. If stock is above 60% of capacity, the system is still in a growth trajectory and cooperation is paying off—reciprocate it. If stock dips below 60%, shift to selective cooperation only if opponents are also mostly cooperating.
- **Cooperation rate sensitivity**: Respond to recent opponent behavior. If at least half your opponents cooperated last round, maintain cooperation even if stock dipped—they are trying. If defection dominates and stock is depleting, protect your payoff with selective defection.
- **Final round cooperation**: End on a prosocial note. Never exploit in the final round. This prevents triggering a cascade of last-round defections if others adopt similar meta-reasoning.

## Edge Cases

- **Stock collapse (stock near 0)**: If stock reaches near-zero in a middle round, defect for that round, but switch back to the standard rule next round. This is damage control, not spite.
- **All opponents defected in round t−1 but stock is still healthy**: Still cooperate, giving a second chance. Mutual defection is a tragedy for everyone.
- **Only one round remaining (r=2)**: Round 1 is pure cooperation; round 2 follows the final-round rule (cooperate).

## Prosocial Alignment

This strategy prioritizes collective welfare while maintaining individual resilience. It sustains the common pool by cooperating when the system is healthy, preventing the tragedy-of-the-commons collapse. It reciprocates other players' prosocial moves, reinforcing a cooperative norm. It avoids punitive defection cycles by interpreting stock depletion as a signal to shift strategy rather than an insult to be punished. Most importantly, it cooperates in the final round regardless of prior history, committing to a prosocial end state and removing incentive for opponent defection in round r.
'''

description_PROSOCIAL_12 = '''
# Adaptive Stewardship Strategy

**Core Logic: Generous Reciprocal Cooperation with Resource Thresholds**

## Decision Rule (Rounds 1 through r)

In each round, play **Cooperate** by default unless defection conditions are triggered.

**Defection is triggered only if BOTH:**
1. Opponent defection rate exceeds 50% (i.e., fewer than (n-1)/2 opponents cooperated in the prior round)
2. AND stock has fallen below capacity/2

**Override:** In the final round (t = r), always play **Cooperate** regardless of history or stock level.

## Implementation

```
Round 1: Play C

For round t ∈ {2, ..., r-1}:
  observed_cooperators = count of opponents playing C in round t-1
  defection_rate = 1 - (observed_cooperators / (n-1))
  
  if defection_rate > 0.5 AND stock < capacity/2:
    play D
  else:
    play C

Round r: Play C
```

## Rationale for Edge Cases

- **Round 1:** Start cooperatively with zero information about opponents. This signals prosocial intent and establishes a cooperative baseline.

- **Rounds 2 to r-1:** Reciprocate cooperation by matching the majority behavior of opponents. If opponents are mostly cooperating, sustain it. If defection is widespread, check stock health before deciding. If stock is still healthy (above half capacity), continue cooperating to invest in recovery and demonstrate commitment to sustainability. Only switch to defection when the collective resource is already badly degraded *and* most opponents are free-riding.

- **Final round:** Defect in the last round only rewards defectors who shirked earlier while punishing those who maintained the commons. Cooperating in the final round demonstrates that your cooperation was genuine and not contingent on reciprocal payoff, reinforcing prosocial norms.

## Prosocial Properties

- **Sustainability focus:** Prioritizes maintaining stock above half capacity, which enables recovery and long-term collective payoff.
- **Generous reciprocity:** Tolerates minority defection and does not punish defectors indiscriminately; reciprocates only when defection is widespread.
- **Commitment signal:** The unconditional final-round cooperation signals trustworthiness and removes the incentive for opportunistic last-round defection in cooperative communities.
- **Robustness:** Recovers gracefully against defectors without collapsing into mutual defection; adapts to mixed populations without assuming fixed opponent types.
'''

description_PROSOCIAL_13 = '''
# Adaptive Prosocial Resource Stewardship

## Decision Rule

**Round 1:** Always Cooperate.

**Rounds 2 through r-1:** Cooperate if and only if BOTH conditions hold:
- **Cooperation threshold:** At least 1/3 of observed opponents cooperated in the previous round (i.e., cooperation_rate ≥ 1/3)
- **Stock health threshold:** Current stock ≥ 0.3 × capacity

Otherwise, Defect.

**Final round (round r):** Defect, unless BOTH conditions hold:
- **High cooperation:** More than 2/3 of opponents cooperated in round r-1 (cooperation_rate > 2/3)
- **Healthy stock:** Current stock > 0.7 × capacity

If both conditions are met, Cooperate as a final prosocial gesture. Otherwise, Defect.

## Edge Cases & Initialization

- **First round:** Always Cooperate, signaling prosocial intent regardless of initial stock level or expectations.
- **No history (round 1):** Treat as if all opponents cooperated (unknown = favorable until proven otherwise).
- **Stock near zero:** If current stock < 0.1 × capacity, Defect. The pool is functionally destroyed; further cooperation yields negligible payoff.
- **Single opponent (n=2):** Cooperation_rate is binary (0 or 1). Threshold "≥ 1/3" becomes "opponent cooperated in previous round."

## Prosocial Alignment

This strategy:

1. **Leads with trust.** First round cooperation invites reciprocal prosocial behavior and tests willingness to coordinate.

2. **Monitors collective health.** Stock health is a joint welfare metric. Defection triggers when the resource trajectory suggests tragedy is inevitable, not from spite.

3. **Forgives occasional defection.** A cooperation_rate threshold of 1/3 tolerates minority free-riding; only widespread defection triggers retaliation.

4. **Avoids tragedy of the commons.** The stock threshold (0.3 and 0.7) explicitly prevents cascading over-extraction by withdrawing from the pool when depletion is underway.

5. **Respects end-game honesty.** The final round defection is a pragmatic concession to the last-round incentive problem, but only if others have not established strong reciprocal cooperation.

6. **Remains stateless and independent.** No player-specific tracking or communication. Only aggregate observations and stock state inform decisions, making the strategy robust to arbitrary opponent heterogeneity.
'''

description_PROSOCIAL_14 = '''
# Threshold-Based Cooperative Guardian Strategy

**Decision Rule:**

For each round, calculate two thresholds:
- Safe threshold: `safe_thr = capacity × 0.6`
- Critical threshold: `crit_thr = capacity × 0.3`

Then decide based on current stock:

```
IF round == 1:
    Play C

ELSE IF stock > safe_thr:
    Play C

ELSE IF stock > crit_thr:
    IF (observed_cooperators / n) ≥ 0.5:
        Play C
    ELSE:
        Play D

ELSE (stock ≤ crit_thr):
    Play D
```

**Logic:**

- **When stock is abundant** (above 60% capacity): Cooperate unconditionally. The resource can sustain it and will regenerate. Demonstrate trust to encourage mutual cooperation.

- **When stock is moderate** (30-60% capacity): Condition cooperation on peer cooperation. If at least half of observed players cooperated last round, reciprocate cooperation. If fewer than half cooperated, defect—the system is being depleted by free-riders and you must conserve.

- **When stock is critically low** (below 30% capacity): Defect. The commons is collapsing. Cooperation becomes futile when others are already extracting more, and the marginal benefit of your restraint is negligible against momentum toward collapse.

- **First round**: Always cooperate. You have no history to condition on. Signal prosocial intent and establish a cooperative equilibrium.

**Edge Case - Last Round:**

Apply the same rule. The thresholds automatically handle the endgame: if stock is healthy, cooperate (leave the commons in good state); if already depleted, defect (no point in sacrifice).

**Robustness:**

This strategy is robust because:
- It responds to **actual system state** (stock level), not assumptions about opponents
- It **reciprocates** observed behavior in the moderate zone, creating feedback pressure against persistent free-riding
- It **gracefully degrades** when the commons fails, rather than wasting resources on futile cooperation
- It tolerates **mixed strategies and heterogeneous opponents**—it doesn't require perfect coordination or punishment of individuals, just aggregate statistical response
'''

description_PROSOCIAL_15 = '''
# PROSOCIAL ADAPTIVE CONSERVATION STRATEGY

## Core Decision Framework

Cooperate by default. Defect only when the combination of high defection among opponents and sufficient stock abundance makes punishment sustainable without threatening resource collapse.

## Decision Rules

```
stock_ratio ← stock / capacity
opponent_defection_rate ← (number of opponents who defected last round) / (n - 1)
rounds_remaining ← r - current_round
progress ← current_round / r

DECISION:

1. CRITICAL STOCK PRESERVATION
   If stock_ratio < 0.30:
       → COOPERATE
       (Resource in distress; cooperation is essential for recovery)

2. FINAL ROUND
   If current_round == r:
       → COOPERATE
       (Secure prosocial terminal payoff and signal commitment)

3. EARLY GAME COOPERATION PHASE (rounds 1 through ⌈r/3⌉)
   → COOPERATE
   (Establish cooperative baseline and maximize collective growth phase)

4. OVERWHELMING DEFECTION WITH ABUNDANCE
   If opponent_defection_rate > 0.75 AND stock_ratio > 0.75:
       → DEFECT
       (Punish rampant defection when resource can sustain it)

5. MODERATE DEFECTION WITH SAFETY MARGIN
   If opponent_defection_rate > 0.50 AND stock_ratio > 0.70 AND progress > 0.50:
       → DEFECT
       (Selective punishment in mid-to-late game only if well-supplied)

6. GENEROUS TIPPING POINT
   If opponent_defection_rate > 0.50 AND stock_ratio ≤ 0.70:
       → COOPERATE
       (Even if majority defect, cooperate to preserve shared asset)

7. DEFAULT
   → COOPERATE
```

## Edge Cases

**Round 1**: Always cooperate. No history exists; establish prosocial precedent.

**Rounds 2 to ⌈r/3⌉**: Cooperate regardless of opponent behavior. Early defection is common and shouldn't trigger punishment before cooperation is established.

**Last 20% of game**: Prioritize resource stability over punishment. Defection is only justified if stock is abundant (>75%) AND defection rate is extreme (>75%).

**Zero-stock scenarios**: The stock collapse rule (stock < 0.30 × capacity) prevents any defection that would worsen collapse. If stock approaches zero, always cooperate to allow recovery.

**Single-round remaining**: Cooperate to signal strength of commitment and maximize the final payoff structure.

## Prosocial Alignment

This strategy centers on **collective resource sustainability** over individual gain maximization:

- Cooperation is the default action, not a reluctant response
- Defection is only used as a calibrated signal when the resource can absorb punishment (high stock) and when defection is nearly universal
- Stock preservation always overrides punishment incentives
- Early and late game phases explicitly prioritize cooperation to bookend each game with prosocial behavior
- The strategy accepts lower individual payoffs in exchange for maintaining a shared resource that benefits all players collectively
'''

description_PROSOCIAL_16 = '''
**Decision Rule Structure:**

**Round 1:** COOPERATE.

**Rounds 2 through r–1:**
- Observe opponent_coop_count from previous round (number of opponents who cooperated)
- Calculate opponent_coop_rate = opponent_coop_count / (n–1)
- Calculate dynamic_threshold = 0.3 + 0.25 × (round / r)
  - This threshold starts at ~0.3 and gradually increases toward 0.55, making the strategy more forgiving as rounds progress
- Calculate stock_health = current_stock / capacity
- Decision:
  - IF stock_health < 0.35: COOPERATE (stock below regeneration optimum; prioritize rebuilding)
  - ELSE IF opponent_coop_rate ≥ dynamic_threshold: COOPERATE
  - ELSE: DEFECT

**Round r (final round):**
- IF stock_health < 0.5: COOPERATE (prevent full collapse on last round; preserve commonality)
- ELSE IF opponent_coop_rate ≥ 0.5: COOPERATE
- ELSE IF (capacity - current_stock) / capacity < 0.2 AND round > 2: COOPERATE (stock already stable, don't destroy it)
- ELSE: DEFECT

**Edge Cases:**

- If stock ever reaches 0, you get 0 payoff that round; subsequent rounds also yield 0. Therefore cooperate regardless on next round to enable any potential recovery.
- If n is very large, opponent_coop_rate becomes a noisy signal; lower dynamic_threshold by 0.05 to account for estimation variance.
- On round 2, if all opponents defected, you defect unless stock_health < 0.35 (information signal is strong; punishment is warranted).

**Prosocial Alignment:**

This strategy prioritizes mutual long-term benefit over individual short-term extraction. It cooperates by default, rewards opponent cooperation with continued cooperation, and crucially: it recovers the commons when depleted rather than race-to-the-bottom defecting. The forgiving threshold increase over time reflects the intuition that late punishment is counterproductive. Final-round cooperation prevents tragic collapse even when opponents defect, breaking the prisoner's dilemma dynamic by making unilateral defection in the endgame costly to all.
'''

description_PROSOCIAL_17 = '''
## Prosocial Conditional Cooperation Strategy

**Initial mindset**: Assume cooperation is possible and aim to sustain the commons. Signal willingness to cooperate while remaining robust to exploitation.

**Decision rules**:

1. **Round 1 (first round)**: Unconditionally COOPERATE.
   - Signal that sustainable strategies are possible.
   - Test whether the game environment supports cooperation.

2. **Rounds 2 to r-1 (middle rounds)**:
   - Observe cooperation rate from previous round: `opp_coop_rate = (number of opponents who cooperated) / (n-1)`
   - Check stock health: `stock_healthy = (current_stock > 0.5 × capacity)`
   
   - COOPERATE if ANY of these hold:
     - `opp_coop_rate ≥ 0.6` (strong cooperation signal—reciprocate)
     - `opp_coop_rate ≥ 0.4 AND stock_healthy` (moderate cooperation with healthy stock—maintain optimism)
   
   - DEFECT otherwise:
     - When cooperation drops below 40% or stock is unhealthy, defection reduces exposure to collapse.

3. **Round r (last round)**: Use the same rule as middle rounds.
   - Do not exploit on the final round, even if ahead.
   - Preserve the reciprocal signal for reputation (relevant if games overlap or context matters).

**Edge case handling**:

- **Stock near 0** (`current_stock < 0.15 × capacity`): If the stock is critically depleted despite cooperation attempts, DEFECT for one round to allow recovery via growth. This is not punishment but resource triage—personal consumption matters less than allowing regrowth. Resume cooperation next round if stock recovers.

- **Unanimous defection in prior round** (`opp_coop_rate = 0`): DEFECT until at least one opponent cooperates again. This prevents repeated one-way exploitation.

- **Exactly two players** (`n = 2`): Lower the thresholds slightly (`opp_coop_rate ≥ 0.5` to cooperate, since one opponent's action is binary). The strategy remains the same in structure.

**Prosocial alignment**:

- Leads with cooperation and generosity, not suspicion.
- Forgives occasional defections (allows 40% defection rate before switching).
- Avoids punishment spirals: defection is threshold-based, not tit-for-tat retribution.
- Sustains the resource by pivoting away from cooperation only when the signal of mutual collapse is clear.
- Resists the temptation to exploit on the final round, prioritizing trust restoration over short-term gain.
'''

description_PROSOCIAL_18 = '''
# Adaptive Stock-Monitoring Cooperation Strategy

**Decision Rule:**

Cooperate in round t if and only if ALL of the following conditions hold:
1. Stock level is above a dynamically-adjusted threshold
2. Observed opponent cooperation rate was sufficient
3. It is not the final round, OR the final round condition applies

**Threshold Calculation:**

- Base sustainability threshold = 0.5 × capacity
- Adjusted threshold = 0.5 × capacity + 0.1 × capacity × (r - t) / r
  - (Stock target increases as game progresses, peaking in early rounds)
- Critical depletion floor = 0.15 × capacity

**Specific Decision Logic:**

```
if t == r (final round):
  if stock > 1.5 × base_threshold:
    COOPERATE  // Prosocial exit
  else:
    DEFECT     // Preserve self if commons depleted
else if stock < critical_depletion_floor:
  DEFECT       // Pool recovery impossible this round
else if stock < adjusted_threshold:
  // Stock compromised; cooperate only if opponents did
  if (opponent_coop_rate_last_round > 0.75):
    COOPERATE  // Reciprocate strong cooperation
  else:
    DEFECT     // Protect against overexploitation
else if stock >= adjusted_threshold:
  // Pool healthy; use reciprocity norm
  if (opponent_coop_rate_last_round > 0.5):
    COOPERATE
  else:
    DEFECT     // Punish collective defection
```

**Round 1 Initialization:**

Cooperate unconditionally. This signals prosocial intent and tests whether sufficient opponents will reciprocate.

**Edge Cases:**

- If no history exists (round 1), default to COOPERATE
- If stock == 0 at round start: DEFECT (no recovery possible)
- If n == 2: Use threshold at 0.6 × capacity (stricter, given higher per-capita defection impact)
- If opponent_coop_rate undefined (impossible), treat as 0.5 (neutral)

**Adaptation Logic:**

Track a running average of opponent cooperation across all observed rounds. If this long-term average falls below 0.4, reduce all thresholds by 5% to shift toward self-protection. If it exceeds 0.8, increase thresholds by 5% to signal stronger commitment to cooperation.
'''

description_PROSOCIAL_19 = '''
**PROSOCIAL COMMON POOL STRATEGY**

**COOPERATE by default, DEFECT only under specific triggering conditions:**

**Decision Rule:**

Defect in round t if and only if BOTH conditions hold:
1. Cooperation rate in round t-1 is below dynamic threshold(t)
2. Stock level satisfies: stock ≤ capacity × 0.4

Where dynamic threshold(t) is:
- Rounds 1 to floor(r/3): 0 (always cooperate in early game)
- Rounds floor(r/3)+1 to floor(2r/3): 0.4 (defect if <40% of opponents cooperated)
- Rounds floor(2r/3)+1 to r: 0.6 (defect if <60% of opponents cooperated)

Otherwise, Cooperate.

**Edge Cases:**

- Round 1: Cooperate (no history available; signal prosocial intent)
- Final round: Cooperate (maintain commitment regardless of cooperation rate; the goal is collective health over all rounds, not exploiting the terminal position)
- Stock = 0: Defect (resource exhausted; no mutual gains possible)
- Stock between 0.4–0.6 of capacity: Apply normal rule; this range signals sustainable management is possible

**Intuition:**

Cooperate unless opponents demonstrate systematic non-cooperation while the resource remains viable. The three-phase structure allows:
- *Early trust* (phase 1): Unilateral cooperation signals prosocial commitment and allows stock recovery
- *Conditional reciprocity* (phase 2): Match rising cooperation rates; escalate required reciprocity as end approaches
- *Principled endurance* (phase 3): Maintain cooperation in final round to demonstrate that prosocial play is robust to terminal temptation

The stock threshold prevents isolated cooperation in a collapsing resource—defecting when stock drops and others defect avoids being trapped in a one-sided sacrifice scenario. The high initial cooperation threshold (0 and 0.4) reflects that even modest reciprocation justifies continued cooperation; the higher threshold in phase 3 (0.6) protects against last-round defection spirals.
'''

description_PROSOCIAL_20 = '''
# Adaptive Conditional Cooperation Strategy

**DECISION RULE:**

Cooperate in round t if and only if:
1. (t = 1, i.e., first round), OR
2. (t ≤ r - 1 AND cooperation_criteria_met), OR
3. (t = r AND stock is viable)

Where cooperation_criteria_met is satisfied when ALL of the following hold:
- observed_cooperation_rate(t-1) ≥ threshold(t)
- stock(t-1) ≥ min_stock_threshold
- defect_signal is not triggered

**THRESHOLD ADAPTATION:**

threshold(t) = 0.5 + (0.25 × min(rounds_remaining / 5, 1))

This sets the cooperation requirement at 50% baseline, increasing to 75% as rounds dwindle. The intuition: early rounds tolerate more defectors since stock can recover; late rounds require higher reciprocity to justify cooperation.

min_stock_threshold = capacity × 0.15

**DEFECT SIGNAL (Trigger Punishment):**

Set defect_signal = true if:
- observed_cooperation_rate(t-1) < 0.25 (severe tragedy imminent), OR
- stock(t-1) < capacity × 0.10 AND observed_cooperation_rate(t-1) < threshold(t) (stock collapsing despite insufficient reciprocity)

Once triggered, remain in defect mode for 2 consecutive rounds (credible punishment), then reset.

**LAST ROUND (t = r):**

Cooperate if stock(r-1) ≥ capacity × 0.20. Otherwise defect. (If stock is already near collapse, do not waste tokens; if viable, end cooperatively as a prosocial signal for potential future interaction norms.)

**FIRST ROUND:**

Always cooperate. Establishes cooperative framing.

**STOCK ESTIMATION (for implicit monitoring):**

Track stock trajectory across previous rounds. If stock is declining despite your cooperation and others' cooperation_rate > 50%, slightly lower future thresholds (assume some players are noisy cooperators or there's measurement noise). This prevents false punishment spirals.
'''

description_PROSOCIAL_21 = '''
# STOCK PRESERVATION COOPERATION STRATEGY

## Decision Rules

**Round 1 (Opening):**
Cooperate unconditionally. Establish a prosocial tone and test the resource's regenerative capacity.

**Rounds 2 through r-1 (Adaptive Phase):**
Cooperate if stock sustainability is achievable, defect only if necessary to prevent free-riding losses.

For each round t:
- Calculate `cooperation_rate` = (number of opponents who cooperated in t-1) / (n-1)
- Calculate `stock_ratio` = current_stock / capacity
- Calculate `rounds_left` = r - t

Decision tree:
```
IF stock_ratio ≥ 0.5:
  → COOPERATE
  (Stock is healthy; cooperation preserves regeneration and collective welfare)

ELSE IF stock_ratio < 0.2:
  → DEFECT
  (Stock critically depleted; secure your share before collapse)

ELSE:  // 0.2 ≤ stock_ratio < 0.5 (moderate depletion)
  IF cooperation_rate ≥ 0.4:
    → COOPERATE
    (Enough players reciprocating; worth maintaining sustainability effort)
  ELSE:
    → DEFECT
    (Too few cooperators; free-riding incentive is too strong)
```

**Final Round (Round r):**
```
IF stock_ratio ≥ 0.5:
  → COOPERATE
  (Prioritize collective resource preservation over final-round defection)

ELSE:
  → DEFECT
  (Stock low; take the doubled immediate payoff since no future rounds exist)
```

## Edge Cases

- **Depleted stock (stock ≈ 0):** Defect. Any payoff > 0, and remaining rounds cannot recover the resource meaningfully.
- **All opponents defected in previous round:** If stock_ratio ≥ 0.5, cooperate anyway (show willingness to restart cooperation). If stock_ratio < 0.3, defect (don't subsidize collapse).
- **Single-player deviation (one opponent defected, rest cooperated):** Cooperate if stock_ratio ≥ 0.3; this is acceptable noise in otherwise-cooperative equilibrium.
- **Ties or ambiguous cooperation rates:** Round down (treat borderline cases as less cooperative; bias toward caution).

## Prosocial Alignment

- **Prioritize collective sustainability over maximum personal extraction.** The strategy cooperates whenever stock health permits (≥50%), treating resource preservation as intrinsically valuable.
- **Reciprocal but not retaliatory.** Response to defection is adaptive to necessity, not punitive. If the resource can still regenerate, maintain cooperation to signal trustworthiness.
- **Graceful degradation.** Only defect when the resource is genuinely under threat (stock_ratio < 0.2) or when cooperative players are a minority (cooperation_rate < 0.4), preventing exploitation without being unforgiving.
- **Final-round generosity.** Even in the last round, cooperate if stock remains healthy, reflecting a preference for leaving a functioning commons to others over terminal defection.
'''

description_PROSOCIAL_22 = '''
**PROSOCIAL ADAPTIVE STRATEGY**

**Core Principle:** Cooperate to sustain the resource when collective welfare is recoverable; calibrate defection only when the pool is genuinely threatened and others are not reciprocating.

**Decision Rules:**

*Round 1:*
Play C unconditionally. Signal prosocial intent and establish baseline.

*Rounds 2 to r-1 (Middle rounds):*

Observe the current stock level S_t and the number of cooperators from the previous round c_{t-1}.

- **If S_t ≥ 0.75 × capacity:** Play C. Stock is healthy and cooperation is sustainable. A functioning commons requires active stewardship.

- **If S_t < 0.75 × capacity:** Assess collective reciprocation.
  - **If c_{t-1} ≥ ⌈n/2⌉:** Play C. Majority is cooperating despite stress. Defecting now would undermine collective recovery. Absorb the short-term cost to help stabilize the stock.
  - **If c_{t-1} < ⌈n/2⌉:** Play D. The group is not reciprocating. Defection is a necessary self-protective response when the tragedy of the commons is actively unfolding. Continuing to cooperate unilaterally enables exploitation.

*Round r (Final round):*

- **If S_r ≥ 0.50 × capacity:** Play C. Even in the final round, if the resource remains viable, cooperation honors the long-term relationship and leaves the commons in better state for any repeated interaction or future players.

- **If S_r < 0.50 × capacity:** Play D. The stock is critically depleted. Maximize personal recovery from remaining resources.

**Rationale:**

This strategy favors cooperation when stock permits it, treats the aggregate cooperation rate as the primary signal of group commitment, and only transitions to defection when both conditions fail: the stock is stressed AND the majority has stopped reciprocating. The final-round rule preserves prosocial behavior when the resource survives, rejecting the assumption that mutual defection is rational at the end.
'''

description_PROSOCIAL_23 = '''
## Adaptive Prosocial Reciprocation

**FIRST ROUND:** Cooperate unconditionally. This signals prosocial intent and establishes willingness to maintain the resource.

**MIDGAME (Rounds 2 through r−1):**

1. **Observe and Calculate:**
   - Record the number of defectors d among your n−1 opponents in the previous round
   - Calculate defection_rate_prev = d / (n−1)
   - Track avg_defection_rate = average defection rate across all completed rounds

2. **Compute Adaptive Threshold:**
   - Base threshold θ = 0.35
   - Stock adjustment: if current_stock < 0.5 × capacity, set θ = 0.50 (increase tolerance when stock is depleted; low stock signals vulnerability and warrants patience to encourage collective recovery)
   - Trend adjustment: if avg_defection_rate from rounds {t−3, ..., t−1} shows an upward trend (cooperation deteriorating), subtract 0.10 from θ (respond defensively to worsening cooperation)
   - Clamp threshold to [0.1, 0.7]

3. **Decision:**
   - Cooperate if avg_defection_rate ≤ θ
   - Defect if avg_defection_rate > θ

**FINAL ROUND (Round r):** Cooperate. Defection in the final round is individually rational but contradicts prosocial commitment. Cooperating in round r signals genuine concern for collective sustainability over short-term extraction, demonstrating that your cooperation is conditional on fairness, not self-interest.

**EDGE CASES:**
- If stock = 0, any action yields 0; either C or D is acceptable
- If all opponents defected every round and avg_defection_rate = 1.0, you will defect (threshold would be ~0.25); this protects the resource from total collapse
- If all opponents cooperated and stock remains high, you will continue cooperating indefinitely

**Prosocial Logic:** The strategy prioritizes collective resource preservation over individual short-term gain. Stock-aware thresholds prevent tragedy of the commons by being more permissive exactly when the resource is endangered, encouraging mutual recovery. Defection occurs only when clear evidence shows opponents are depleting the stock unsustainably, not preemptively. Final-round cooperation demonstrates genuine prosociality rather than strategic defection opportunism.
'''

description_PROSOCIAL_24 = '''
**ADAPTIVE SUSTAINABILITY COOPERATION**

**Decision Rule:**

Cooperate if and only if:
- [Rounds remaining > 1] AND
- [Observed cooperation rate among opponents ≥ threshold(t, stock)]

Otherwise defect.

Where the cooperation rate threshold is dynamically set:
- threshold(t, stock) = 0.4 + 0.4×(t/r) + 0.2×(1 - stock/capacity)
- t = current round
- This means: require lower cooperation rates early; tighten requirements as rounds progress; relax slightly if stock is depleted (adaptive conservation)

**First Round:**
Cooperate unconditionally. Establish initial signal of prosocial intent with no history to learn from.

**Last Round (t = r):**
Defect. After final payoff, stock regeneration is irrelevant, so the individual incentive to extract dominates.

**Intermediate Rounds (1 < t < r):**
Apply the threshold rule above. Track the running average of observed cooperator counts across all previous rounds.

**Stock Monitoring:**
- If stock falls below capacity/2, interpret this as a warning signal that defection is accelerating. Increase the threshold multiplicatively by 1.2× on the next decision to encourage community restraint.
- If stock rises toward capacity, decrease threshold by 0.95× to reward apparent cooperation.

**Edge Cases:**

- If all opponents defected in the previous round, defect unless stock is critically high (stock > 0.9×capacity) and more than 2 rounds remain—in which case cooperate once as an attempt to reset the cooperative equilibrium.
- If you observe fractional cooperators (some above-threshold, some below), weight by majority: cooperate if strictly more than half cooperated.

**Rationale:**
This strategy prioritizes stock sustainability for collective benefit while protecting against exploitation. Early rounds invest in signaling cooperation; threshold tightening prevents blind cooperation as end approaches; stock-responsive adjustments align individual incentives with resource preservation across heterogeneous opponent strategies.
'''

description_PROSOCIAL_25 = '''
# Prosocial Stock Guardian Strategy

## Core Decision Rule

**Cooperate by default. Defect only when:**

1. **Stock depletion threshold**: current_stock < 0.3 × capacity
   - Rationale: Preserve remaining stock from collapse; defection at low stocks is self-protection, not exploitation

2. **Exploitation threshold**: defection_count > (n-1) × 0.4
   - If more than 40% of opponents defected last round, defect this round
   - Rationale: Prevent being systematically exploited; signal that unilateral cooperation is unsustainable

3. **Cooperative momentum**: defection_count ≤ (n-1) × 0.25
   - If fewer than 25% of opponents defected, cooperate unconditionally
   - Rationale: Reciprocate strong cooperation signals and maintain stability

4. **Forgiveness window**: If defection_count was high last round but drops this round below 0.3 threshold, return to cooperation
   - Rationale: Allow others to exit defection spirals; reward collective course correction

## Edge Cases

**Round 1**: Cooperate unconditionally. No history exists; cooperation signals prosocial commitment and enables stock growth foundation.

**Final round (t = r)**: Cooperate according to the same thresholds above. Accept lower individual payoff to avoid triggering defection cascades that harm the collective. Resist backward induction that treats the last round as a zero-sum extraction opportunity.

**Stock at capacity**: Cooperate. Surplus stock means you are not competing for scarce resources; cooperation maintains the commons.

**Stock near zero (< 0.1 × capacity)**: Defect to harvest remaining value, but only once — if stock recovers via growth, resume cooperation immediately.

## Adaptive Monitoring

Track per-round:
- `cooperators_last_round` = count of opponents who played C
- `stock_trend` = is stock growing or shrinking across recent rounds?

If stock is shrinking despite your cooperation, increase defection tolerance threshold from 0.4 to 0.35. If stock is stable or growing, maintain thresholds.

## Prosocial Alignment

This strategy:
- Initiates cooperation and sustains it as baseline mode
- Treats defection as a response to collective threat (overexploitation), not as individual gain-seeking
- Prioritizes long-term collective stock health over short-term individual extraction
- Grants others multiple opportunities to cooperate; does not permanently punish single defections
- Sacrifices final-round advantage to prevent tragedy-of-commons collapse
'''

description_PROSOCIAL_26 = '''
**STRATEGY: Conditional Cooperation with Resource-Based Thresholds**

**Decision Rule:**

On round t, observe the current stock level S and the count of cooperators C_observed among the (n-1) opponents in round (t-1). Compute:
- stock_ratio = S / capacity
- opponent_cooperation_rate = C_observed / (n-1) [in first round, treat as unknown/neutral]

Then:

```
IF t ≤ 2:
  COOPERATE
  
ELSE IF stock_ratio > 0.50:
  IF opponent_cooperation_rate ≥ 0.40:
    COOPERATE
  ELSE IF opponent_cooperation_rate ≥ 0.20:
    COOPERATE
  ELSE:
    DEFECT
    
ELSE IF stock_ratio > 0.30:
  IF opponent_cooperation_rate ≥ 0.50:
    COOPERATE
  ELSE:
    DEFECT
    
ELSE IF stock_ratio > 0.15:
  IF opponent_cooperation_rate ≥ 0.65:
    COOPERATE
  ELSE:
    DEFECT
    
ELSE:
  COOPERATE  [resource critical; signal recovery attempt]
```

**Edge Cases:**

- **First round:** Cooperate unconditionally to establish prosocial intent and generate maximum stock growth.
- **Second round:** Cooperate unconditionally; one observation is insufficient to infer opponent strategy.
- **Last round:** Follow the standard rule above. Do not exploit the endgame by defecting opportunistically.
- **Stock collapse (stock_ratio < 0.15):** Cooperate to attempt resource recovery, even if others have defected heavily. This minimizes mutual destruction and signals commitment to restoration.

**Prosocial Logic:**

This strategy stabilizes the resource at a healthy operating range (30–50% of capacity) where the logistic growth function is productive. By cooperating when stock is abundant and defection is unnecessary, it avoids tragedy-of-the-commons collapse. Defection is triggered only when (1) the resource is already stressed AND (2) others have signaled defection through low cooperation rates. At resource-critical levels, it reverts to cooperation to signal willingness to recover collectively. Opponents are treated as independent strategic agents, not adversaries; the strategy accommodates uncoordinated defection gracefully without racing to zero.
'''

description_PROSOCIAL_27 = '''
**STRATEGY DEFINITION**

**Decision Logic:**

1. **Round 1:** Play C. Initialize with prosocial trust and maximize early stock growth.

2. **Rounds 2 to r−1 (Middle Game):**
   - Let cooperators_last = count of opponents observed cooperating in previous round
   - Let coop_rate = cooperators_last / (n − 1)
   - **If coop_rate ≥ 0.5:** Play C
   - **If coop_rate < 0.5:** Play D

3. **Round r (Final Round):**
   - **If stock ≥ capacity × 0.4 AND cooperators_last ≥ ceil((n−1) × 0.4):** Play C
   - **Else:** Play D

**Rationale for Structure:**

- Cooperate initially to signal prosocial commitment and establish sustainability momentum
- In middle rounds, adopt a "pragmatic reciprocal" stance: match cooperation when at least half of opponents cooperated, defect when the majority defected. This maintains pressure for collective cooperation without unilateral sacrifice
- In the final round, cooperate only if stock health remains adequate (suggesting the system hasn't been systematically depleted) and meaningful recent cooperation is present. Otherwise defect to capture the last round before the game ends

**Edge Cases:**

- **All opponents defect from round 2 onward:** Switch to defection in round 2 and sustain it. This prevents cumulative resource waste while not initiating punishment
- **Stock reaches 0:** Continue following the decision rule mechanistically—you get 0 regardless, so the strategy's commitment is tested
- **Uneven n (like n=3):** Use ceil((n−1)/2) as the threshold—requires at least one cooperator among two opponents to continue cooperation
- **High r:** The strategy scales naturally; cooperation threshold remains constant rather than declining over time, preserving sustainability intentions

**Prosocial Properties:**

- Starts from cooperation, not defection
- Remains willing to cooperate whenever a reasonable coalition (≥50%) of opponents does the same
- Avoids endless punishment spirals; switches to D pragmatically but not vengefully
- Biases toward resource preservation (stock threshold in final round) over pure individual payoff maximization
- Transparent and predictable behavior invites reciprocal cooperation rather than defensive defection
'''

description_PROSOCIAL_28 = '''
**DECISION RULE**

In round 1: Cooperate (C).

In round t ∈ {2, ..., r}:
- Calculate observed_coop_rate = (number of opponents who cooperated in round t-1) / (n-1)
- Classify stock health:
  - HEALTHY if stock_t > 0.6 × capacity
  - MODERATE if 0.4 × capacity ≤ stock_t ≤ 0.6 × capacity  
  - CRITICAL if stock_t < 0.4 × capacity
- Set cooperation threshold based on stock health:
  - threshold = 0.55 if HEALTHY
  - threshold = 0.50 if MODERATE
  - threshold = 0.40 if CRITICAL
- If observed_coop_rate ≥ threshold: Cooperate (C)
- Else: Defect (D)

**EDGE CASES**

First round (t=1): Always play C regardless of parameters. This establishes goodwill and tests whether others will reciprocate.

Critical depletion (stock_t approaches 0): Lower the cooperation threshold to 0.40 and maintain C if any meaningful cooperation is observed. The resource collapses only if the collective chooses defection; your strategy continues offering cooperation pathways.

Last round (t=r): Apply the same decision rule—do not defect for final-round exploitation. Maintain the strategy's integrity throughout.

**PROSOCIAL ALIGNMENT**

The strategy prioritizes resource sustainability over individual gain:
- Begins with unconditional cooperation, signaling trustworthiness
- Thresholds are set below 0.5, requiring only modest cooperation from others to reciprocate
- Adapts generously during crisis (lowered thresholds when stock is critical)
- Avoids last-round exploitation, which would undermine collective recovery
- Defects strategically only when the majority of opponents defect, applying minimal punishment (one-round responses) rather than escalation

This approach recognizes that the stock's logistic growth rewards restraint: when consumption stays near 50% of stock, the system regenerates robustly. By conditioning on observed cooperation rates and stock health rather than opponent identity, the strategy remains robust to diverse opponent strategies while maintaining a resilient prosocial stance.
'''

description_PROSOCIAL_29 = '''
## Adaptive Sustainability Cooperation

**Round 1:**
Always cooperate. This establishes prosocial intent and gives the common pool time to grow.

**Rounds 2 through r-1:**
Observe the number of defectors d from the previous round and the current stock level S.

Define thresholds:
- critical_threshold = capacity/3
- healthy_threshold = capacity/2
- defection_tolerance(S) = varies with stock health

Decision rule:

```
if S ≤ critical_threshold:
  action = D
  // Stock is depleted or near-depleted; self-preserve
  
else if S ≤ healthy_threshold:
  if d ≤ (n-1)/3:
    action = C
  else:
    action = D
  // Stock is recovering; only cooperate if defection is sparse
  
else:
  // S > healthy_threshold (stock is thriving)
  if d ≤ (n-1)/2:
    action = C
  else:
    action = D
  // Stock is healthy; tolerate up to half of opponents defecting
```

**Final Round r:**
The future growth of the pool no longer benefits you, but defecting in the final round harms collective outcomes. To maintain prosocial commitment:

```
if S > healthy_threshold:
  action = C
  // Stock remains viable; signal long-term cooperation norm
else:
  action = D
  // Stock is compromised; conserve personal consumption
```

**Rationale:** This strategy cooperates as the baseline, encouraging regeneration of the pool toward capacity. It retreats to defection only when: (1) the stock falls into danger zones where current consumption patterns are unsustainable, or (2) opponents are defecting at high rates, indicating the cooperation-dependent equilibrium has broken down. By tying tolerance for defection to stock health, the strategy remains robust—it can coexist with selfish players without collapsing the resource, and it rewards groups that stabilize the pool near capacity.
'''

description_PROSOCIAL_30 = '''
# Prosocial Conservative Cooperation

**Round 1 Decision:**
Cooperate. Begin with trust to establish a cooperative baseline and observe opponent behavior.

**Rounds 2 through r-1 Decision:**

Compute state variables:
- `cooperation_rate` = (number of opponents cooperating in previous round) / (n - 1)
- `stock_health` = stock / capacity
- `rounds_left` = r - current_round

Apply decision rules in order:

1. **Emergency depletion threshold:** If `stock_health < 0.15`, Defect (resource near collapse; continuing consumption accelerates catastrophe)

2. **Widespread defection threshold:** If `cooperation_rate < 0.25`, Defect (majority of opponents are defecting; continuing cooperation alone cannot sustain the resource)

3. **Danger zone:** If `stock_health < 0.40` AND `cooperation_rate < 0.50`, Defect (insufficient resource health + insufficient cooperation creates compound risk)

4. **Default:** Cooperate in all other cases

**Last Round (t = r) Decision:**

Adjust thresholds forward-looking (no future recovery possible):

1. If `stock_health < 0.25`, Defect
2. If `cooperation_rate < 0.35`, Defect  
3. Otherwise, Cooperate

**Rationale for Prosocial Framing:**

This strategy prioritizes collective resource health over individual short-term maximization. It cooperates by default and only switches to defection when either: (1) the resource faces imminent depletion making further extraction unsustainable, or (2) enough opponents are defecting that cooperation alone cannot preserve the commons. It avoids punishment-based strategies and uses thresholds that forgive sporadic defection by others, creating space for opponent adaptation without requiring explicit communication.
'''

description_PROSOCIAL_31 = '''
# Adaptive Prosocial Strategy for Common Pool Resource Game

**Phase 1: Initialization (Round 1)**
Always cooperate. This establishes a cooperative signal and allows the stock to grow from full capacity.

**Phase 2: Rounds 2 through r-1**

Classify current stock health:
- Healthy: stock ≥ 0.75 × capacity
- Moderate: 0.5 × capacity ≤ stock < 0.75 × capacity  
- Critical: stock < 0.5 × capacity

Calculate recent cooperation signal:
- Let c = number of other players observed cooperating in the previous round (0 to n-1)
- Cooperation ratio = c / (n-1)

Decision tree:
1. If stock is **critical**: Cooperate unconditionally. The priority is resource recovery.

2. If stock is **healthy**: Cooperate if observed cooperation ratio ≥ 0.5 (at least half of others cooperated). Otherwise defect.

3. If stock is **moderate**: 
   - Cooperate if observed cooperation ratio ≥ (2/3)
   - Defect otherwise

**Phase 3: Final Round (Round r)**

Cooperate if either:
- Stock is healthy or critical, AND
- Observed cooperation in round r-1 was ≥ (n-1)/2

Otherwise defect.

**Rationale:**
- Critical stock triggers unconditional cooperation to preserve the commons
- Healthy stock allows reciprocal play: cooperate when enough others do
- Moderate stock requires stricter evidence of cooperation before cooperating
- This creates a sliding scale that protects both collective welfare and individual safety
- The strategy punishes defection by defecting back, but rewarding cooperation recovers cooperation rapidly
'''

description_PROSOCIAL_32 = '''
# Conditional Cooperation with Stock Monitoring

**Initialization (Round 1):**
Cooperate. Begin with trust and demonstrate commitment to collective sustainability.

**Decision Rule for Rounds 2 through r:**

Observe the current stock level and the number of defectors from the previous round.

```
if stock ≤ capacity/20:
    → Defect
    (stock is critically depleted; preservation is no longer viable)
    
else if defectors_last_round ≥ n/2:
    → Defect
    (majority defecting; mutual defection is now the revealed pattern)
    
else if stock ≥ 3×capacity/4 AND defectors_last_round ≤ n/4:
    → Cooperate
    (stock is healthy and cooperation is widespread; maintain it)
    
else if defectors_last_round < n/3:
    → Cooperate
    (cooperation dominates; worth sustaining)
    
else:
    → Cooperate if stock > capacity/3, else Defect
    (moderate defection environment; condition on stock health)
```

**Last Round (t = r):**
Apply the same decision rule. Do not defect preemptively just because it is the final round—the stock level and defection pattern remain the appropriate guides.

**Rationale:**

The strategy balances prosocial resource stewardship with self-protection. It cooperates when mutual cooperation is evident (few defectors) and stock remains healthy, maximizing long-term collective payoffs. It responds defensively only when the commons is being actively exploited by others (majority defecting) or already exhausted, avoiding futile cooperation with free-riders. The stock thresholds recognize that depleted resources cannot support cooperation. The defection rate thresholds detect whether a cooperative norm exists; once it breaks, the strategy exits to avoid unilateral loss. This approach is robust to both altruistic and self-interested opponents while maintaining prosocial intent through transparent, conditional reciprocity.
'''

description_ALTRUISTIC_5 = '''
# Altruistic Adaptive CPR Strategy

## Core Logic

**Cooperate by default when the resource permits sustainable equilibrium; defect defensively only when system health is compromised or reciprocal cooperation is insufficient.**

## Decision Rule

For each round t:

1. **Calculate stock health indicator:**
   - target_stock = capacity × 0.6 (maintain 60% as resilience buffer)
   - stock_ratio = stock / target_stock

2. **Compute observed opponent cooperation rate:**
   - coop_rate = (number of opponents who cooperated in round t-1) / (n - 1)
   - In round 1, treat as: coop_rate = 1.0 (assume good faith)

3. **Determine rounds remaining:**
   - rounds_left = r - t

4. **Primary action selection:**

   ```
   if stock_ratio ≥ 0.8:
       // Resource is healthy; preserve it altruistically
       Play C
   
   else if stock_ratio ∈ [0.4, 0.8):
       // Resource is stressed; conditional cooperation
       if coop_rate ≥ 0.6:
           Play C
       else:
           Play D
   
   else if stock_ratio ∈ [0.1, 0.4):
       // Resource is depleted; prioritize personal survival
       if coop_rate ≥ 0.8 AND rounds_left > 2:
           Play C
       else:
           Play D
   
   else:
       // Collapse imminent; defect to salvage payoff
       Play D
   ```

## Edge Cases

**First round (t = 1):**
- Play C unconditionally. Stock is at capacity; cooperation preserves the system and signals altruistic intent.

**Final round (t = r):**
- If stock_ratio ≥ 0.5 AND coop_rate ≥ 0.7 in prior round: Play C (maximize collective final payoff).
- Otherwise: Play D (no recovery period; capture available stock).

**Penultimate round (t = r-1):**
- Increase defection threshold: if coop_rate < 0.5, shift toward D (conservation of effort when recovery is minimal).

**Stock approaching zero (stock ≤ 2n):**
- Play D regardless of cooperation rate. The resource is unsalvageable; extract maximum individual payoff.

## Altruistic Commitment

This strategy embodies altruism through:

- **Cooperative baseline:** Defaults to C when resource health permits, foregoing immediate exploitation.
- **Sacrifice of individual gain:** Consistently accepts S/(2n) payoff when others cooperate, rather than maximizing S/n.
- **System preservation:** Prioritizes stock longevity over short-term extraction, enabling future rounds and other players' welfare.
- **Graceful degradation:** Only defects when the commons is already compromised, minimizing further damage.
- **Reciprocal fairness:** Responds to others' cooperation rates rather than assuming universal defection; supports cooperation when conditions are right.
'''

description_ALTRUISTIC_6 = '''
# Adaptive Conservation Strategy

**Core Decision Rule:**

In each round t, play Cooperate if BOTH conditions hold; otherwise play Defect:
1. `stock / capacity ≥ (1 - 0.3 * rounds_remaining / r)` — Stock level is above a declining threshold
2. `observed_cooperation_rate ≥ 0.4` — At least 40% of opponents cooperated last round

Where `observed_cooperation_rate = cooperators_last_round / (n - 1)` and `rounds_remaining = r - t`.

**Round 1 (Initial Cooperation Signal):**

Always Cooperate. This establishes trust and demonstrates commitment to resource preservation regardless of uncertainty about opponents.

**Last Round (t = r):**

If `stock / capacity ≥ 0.5`, Cooperate to maximize final collective payoff.
Otherwise, Defect to maximize individual recovery from resource degradation.

**Stock Recovery Mode:**

If `stock / capacity < 0.25` (critical depletion):
- Cooperate unconditionally for the next round, regardless of prior cooperation rates.
- This signals willingness to rebuild and prevents collapse into full defection cycles.

**Cooperation Monitoring:**

After each round except the last, calculate cooperators among n-1 opponents:
- If `cooperators < 0.2 * (n - 1)` (fewer than 20% cooperated), reduce the cooperation threshold to 0.25 for one round as a calibrated punishment (still weighted toward cooperation over defection).
- If `cooperators > 0.6 * (n - 1)` (majority cooperated), relax threshold to 0.6 for next round as positive feedback.

**Defection Type (when defecting):**

When the decision rule mandates Defection, play D only if `stock / capacity < 0.5` (resource pressure). Otherwise, treat as a near-Cooperate (abstain) by playing C to minimize harm while signaling conditional cooperation.

This strategy prioritizes stock sustainability while remaining responsive to collective action. It punishes pure free-riding indirectly (through defection) but preserves the resource itself, allowing recovery when cooperation resumable.
'''

description_ALTRUISTIC_7 = '''
# Altruistic Common Pool Resource Strategy

**Core Principle**: Prioritize stock sustainability and collective resource preservation. Consume modestly to maintain the commons for all players, including future rounds.

## Decision Rule by Stock Health

Define stock ratio: `health = current_stock / capacity`

**Tier 1 - Crisis (health ≤ 0.30):**
Always Cooperate. The resource faces collapse. Defection accelerates ruin for all.

**Tier 2 - Vulnerable (0.30 < health ≤ 0.50):**
Cooperate with probability `p = 0.85 + 0.15 × (cooperators_observed_last_round / n)`

The base cooperation rate is high, slightly boosted if others cooperated. This preserves the resource while remaining responsive to others' signals.

**Tier 3 - Stable (0.50 < health < 0.80):**
Cooperate if `cooperators_observed_last_round / n ≥ 0.40`

Otherwise Cooperate with probability 0.60. At healthy stock levels, permit selective defection only if widespread non-cooperation is evident. Otherwise default to cooperation.

**Tier 4 - Abundant (health ≥ 0.80):**
Cooperate with probability 0.70. Even at high stock, maintain cooperative discipline to prevent overconfidence-driven depletion. The logistic growth function means moderate consumption here preserves long-term sustainability.

## Round-Specific Adjustments

**Round 1:**
Always Cooperate. Establish cooperative signal and commit to collective benefit from the start.

**Final Round (t = r):**
Cooperate if `current_stock / capacity > 0.25`, otherwise apply Tier 2 rule. Altruistically sustain the resource even in the final round, since long-term preservation reflects genuine concern for the commons.

## Edge Cases

- If `n = 2`: Use thresholds above but double-weight observed cooperation ratios (fewer players means individual actions are more visible).
- If stock reaches exactly 0: Cooperate anyway (signal remains important; prevents mutual blame).
- If stock exactly at capacity: Cooperate (no additional gain from defection; preserve surplus).

## Implementation Detail

Track `cooperators_observed_last_round` from the observed count after each round. In round 1, assume neutral prior: `cooperators_observed = n/2`.

This strategy sacrifices immediate payoff to maintain stock trajectory, responds adaptively to community behavior, and commits to cooperation even when personally costly—true altruism in a tragedy-of-the-commons setting.
'''

description_ALTRUISTIC_8 = '''
# Adaptive Altruistic Stock Preservation Strategy

**Core orientation:** Sustain the common pool for collective long-term benefit. Cooperate as the default mode, defecting only when systemic collapse is imminent or personal survival is at risk.

## Decision Rule

Define thresholds:
- `SAFE_ZONE = capacity × 0.5` (stock level indicating stable conditions)
- `WARNING_ZONE = capacity × 0.3` (stock level indicating stress)
- `CRITICAL_ZONE = capacity × 0.15` (stock level indicating collapse risk)
- `DEFECTION_RATE_THRESHOLD = 0.45` (proportion of opponents defecting)

**Each round t, play as follows:**

```
if stock < CRITICAL_ZONE:
  → DEFECT
  (System is collapsing; preserve personal consumption to survive)

else if stock < WARNING_ZONE:
  if observed_defection_rate > DEFECTION_RATE_THRESHOLD:
    → DEFECT
    (Systemic exploitation confirmed; ecosystem degrading)
  else:
    → COOPERATE
    (Most players cooperating despite stress; maintain solidarity)

else if stock >= SAFE_ZONE:
  → COOPERATE
  (Pool is healthy; prioritize collective welfare)

else:
  (stock in [WARNING_ZONE, SAFE_ZONE))
  if t == r (final round):
    → DEFECT
    (Last round; stock won't recover; take maximum value)
  else:
    → COOPERATE
    (Intermediate rounds; maintain cooperative pressure to allow recovery)
```

## Edge Cases

**First round:** Cooperate unconditionally (altruistic assumption of good faith; no history to reference).

**Last round:** Defect only if stock is in warning zone or below. If stock is healthy, cooperate (values collective outcome even with no future interaction).

**Stock recovery phase:** After a warning-zone episode, if stock rebounds above safe zone, immediately return to full cooperation (restart altruistic stance).

**Unanimous defection path:** If all opponents defect every round and stock enters critical zone, switch to defection for rounds t+1 onward (acknowledge system failure, shift to survival).

## Altruistic Alignment

Cooperate by default, maximizing common pool sustainability across all rounds. Defect only when:
- The resource system is materially collapsing (individual and collective survival both threatened)
- Overwhelming evidence of systematic free-riding makes cooperation futile
- It is the final round and immediate gain does not compromise future stock (no future rounds exist)

This preserves the possibility of mutual cooperation and long-term collective welfare in all conditions where it remains feasible.
'''

description_ALTRUISTIC_9 = '''
# Adaptive Altruistic Resource Stewardship

## Core Decision Rule

**Cooperate** if any of the following conditions hold; otherwise **defect**:

1. **First round**: Always cooperate (establish cooperative norm)
2. **Sufficient cooperation observed**: If in previous round, at least ⌈n/2⌉ players cooperated, then cooperate
3. **Resource sustainability**: If current stock ≥ capacity × 0.4, cooperate (resource is healthy enough to support cooperation)
4. **Final rounds**: If rounds_remaining ≤ 2, cooperate (don't exploit in endgame)
5. **Catastrophe recovery**: If current stock ≤ capacity × 0.2 (resource near collapse), cooperate (prioritize collective survival over individual gain)

## Edge Cases & Refinements

**Round 1**: Cooperate unconditionally. No history exists; the altruistic posture is to give others the chance to cooperate.

**Rounds 2 to r-2** (middle game):
- Let c_prev = count of cooperators in the immediately preceding round
- If c_prev / n ≥ 0.5: cooperate
- Else if stock ≥ 0.4 × capacity: cooperate (still invest in recovery)
- Else if c_prev / n ≥ 0.25 and stock ≥ 0.25 × capacity: cooperate (partial cooperation + moderate stock = continue trying)
- Else: defect (reduce pressure on depleted resource; let it regenerate)

**Final round (round r)**: Cooperate unconditionally. Altruistic strategy does not exploit in the final round even if opponents defected previously. The goal is to leave the collective pool in better condition than found it.

**Critical depletion (stock < 0.15 × capacity)**: Cooperate. Collective survival supersedes individual payoff maximization.

## Altruistic Alignment

This strategy embodies altruism through:

- **Cooperation-first bias**: Default action is always to cooperate unless conditions strongly indicate resource collapse or near-endgame defection epidemic
- **Resource stewardship**: Prioritizes keeping stock above danger thresholds, benefiting all future players and rounds
- **No exploitation**: Refuses to defect in final rounds despite temptation; rejects last-round profit-taking
- **Forgiveness with vigilance**: Tolerates up to 50% defection from others before withdrawing cooperation, showing willingness to absorb temporary setbacks
- **Catastrophe response**: When resource nears zero, cooperates harder (reduced consumption) to enable regeneration, maximizing collective welfare

This strategy is robust because it adapts to opponent behavior ranges (from highly cooperative to highly defective) while maintaining the core altruistic commitment to collective sustainability.
'''

description_ALTRUISTIC_10 = '''
# Altruistic Commons Steward Strategy

**Core Principle:** Prioritize collective resource sustainability and equitable access over personal consumption. Cooperate to rebuild and maintain the commons, even when unilateral cooperation provides lower individual returns.

## Decision Rules

**Round 1:** COOPERATE
- Establish cooperative intent and test resource dynamics under sustainable extraction.

**Rounds 2 to r-1:**

Let `c = count of opponents who cooperated in previous round` and `cooperation_rate = c / (n-1)`.

```
IF stock ≥ 0.65 × capacity:
    → COOPERATE (resource healthy; full stewardship)
    
ELSE IF 0.35 × capacity ≤ stock < 0.65 × capacity:
    → COOPERATE (resource stressed; help stabilize)
    
ELSE IF stock < 0.35 × capacity:
    IF cooperation_rate ≥ 0.5:
        → COOPERATE (others are reciprocating; collective rescue attempt)
    ELSE:
        → COOPERATE (resource critical; altruistic allocation to preserve commons)
```

**Final Round (round r):** COOPERATE
- Ignore end-game defection incentive. The commons benefit extends to all remaining players' welfare, including those who did not cooperate.

## Edge Cases

- **Unanimous defection (c = 0):** Still cooperate. Rationale: allocating your full share allows stock to recover via growth function; unilateral defection only accelerates collapse and harms all players equally.

- **Stock depletion to zero:** Continue cooperating in subsequent rounds if stock recovers. Do not switch to punishment/defection strategy; punishing is antithetical to altruism.

- **Two-player game (n=2):** Same rules apply. Accept that your sole opponent's defection will damage long-term payoffs, but cooperating still maximizes collective welfare over the full horizon.

## Altruistic Alignment

This strategy embodies altruism by:
- Accepting lower personal consumption (C yields stock/2n vs. D yields stock/n) to enable resource regeneration.
- Subordinating short-term individual gain to long-term collective sustainability.
- Forgiving defection and never initiating punishment, which would harm both self and others.
- Continuously demonstrating cooperation as a model, signaling that the game's structure rewards mutual restraint over exploitation.
'''

description_ALTRUISTIC_11 = '''
**ALTRUISTIC RESOURCE PRESERVATION STRATEGY**

**Core Decision Rule:**

Cooperate if stock ≥ sustainability_threshold; otherwise evaluate opponent behavior and adjust.

sustainability_threshold = 0.5 × capacity

**Primary Cooperation Phase (stock ≥ sustainability_threshold):**

Always play C. This preserves the resource at stable levels and demonstrates commitment to collective welfare. When stock exceeds the sustainability threshold, cooperation ensures the pool regenerates toward capacity.

**Resource Stress Phase (stock < sustainability_threshold):**

Let c_observed = number of opponents observed cooperating in the previous round (or n-1 if first round).
Let defection_rate = 1 - (c_observed / (n-1))

- If defection_rate > 0.5: Play D for this round only, then reassess
  - Rationale: When more than half of opponents defect, the resource is already collapsing from external behavior. Defecting here prevents being exploited while the pool is dying anyway, allowing you to continue cooperating when conditions improve.
  
- If defection_rate ≤ 0.5: Play C
  - Rationale: Even in stress, enough players are restraining themselves. Continuing cooperation supports their efforts and prevents cascading collapse.

**Round-Dependent Adjustment:**

- Rounds 1 through (r-2): Apply above rules strictly to demonstrate reliable cooperation and encourage reciprocation
- Final round (r): Always play C regardless of stock level or opponent behavior
  - Rationale: On the last round, long-term sustainability is irrelevant. Playing C maximizes the collective final payoff and expresses pure altruistic preference for group welfare over personal gain.

**Edge Cases:**

- If stock reaches 0 before the final round: Remain in defection mode only until stock recovers above sustainability_threshold, then return to primary rule
- First round: Always play C with no history to assess
- Ties in defection rate (exactly 50%): Treat as ≤ 0.5 and cooperate, erring toward trust

**Information Usage:**

Each round, adjust the sustainability_threshold dynamically if stock shows volatile recovery patterns: if stock dropped more than 30% in a previous round, raise the stress threshold temporarily to capacity × 0.6 for 2 rounds to recover before relaxing.
'''

description_ALTRUISTIC_12 = '''
# Adaptive Cooperative Strategy

**Core Principle**: Cooperate to sustain the common pool and maximize collective welfare. Defect only when stock is critically depleted and cooperation offers no path to recovery.

## Decision Rule by Stock Health

**If stock ≥ 0.5 × capacity:**
Always Cooperate. The resource is healthy. Cooperation sustains this equilibrium and generates payoffs of S/(2n) for all. Defecting here is exploitative.

**If 0.2 × capacity ≤ stock < 0.5 × capacity:**
Cooperate if observed_cooperation_rate ≥ 0.4, otherwise Defect.
- At this level, stock is at risk. If >40% of opponents cooperated last round, the group is maintaining some restraint. Continue cooperating to help stabilize the resource.
- If <40% cooperated, defection is rampant and cooperation alone cannot prevent collapse. Defect to reduce consumption pressure.

**If stock < 0.2 × capacity:**
Defect. The resource is in critical condition. Continuing to consume at the cooperative rate (S/(2n)) merely delays collapse. Defect to maximize immediate payoff before stock reaches zero. The resource is effectively lost; prioritize individual survival over collective loss.

## Round-Specific Adjustments

**Rounds 1 through r-2 (All but final two rounds):**
Apply the stock-based rule above. Early cooperation signals trustworthiness and establishes norms.

**Rounds r-1 and r (Final two rounds):**
If stock > 0.1 × capacity, maintain Cooperation regardless of opponent behavior. With few rounds remaining, the marginal damage from one last cooperative act is minimal, but it preserves dignity and prevents causing terminal collapse.

If stock ≤ 0.1 × capacity in the final rounds, Defect. The resource is unsalvageable.

## Edge Cases

- **First round**: Cooperate unconditionally. Establish cooperation as the opening norm.
- **Stock exactly at threshold**: Use ≥/< strictly as written. Tie-breaking favors cooperation.
- **Observed cooperation = 0** (all opponents defected): If stock > 0.2 × capacity, cooperate anyway to demonstrate non-retaliatory intent. If stock ≤ 0.2 × capacity, defect (no point sacrificing into a void).

This strategy prioritizes sustaining collective welfare, refuses to exploit cooperators, and only abandons cooperation when the group has already failed to sustain the resource.
'''

description_ALTRUISTIC_13 = '''
# Altruistic Common Pool Resource Strategy

## Core Decision Rule

**Default to cooperation. Defect only when stock sustainability is threatened or when personal survival requires it.**

Maintain a cooperative posture as the baseline, accepting modest immediate payoffs to preserve collective welfare. Monitor stock health and opponent cooperation to adjust dynamically.

## Decision Logic by Phase

**Early Game (rounds 1 through ⌈r/3⌉):**
Always cooperate. This signals trustworthiness and investment in sustained cooperation, giving opponents time to learn that cooperation is viable.

**Middle Game (rounds ⌈r/3⌉ + 1 through ⌊2r/3⌋):**
Use adaptive rule based on stock health:

- **Healthy stock** (stock > 0.6 × capacity): Always cooperate. The resource can sustain full cooperation.
  
- **Moderate stock** (0.3 × capacity < stock ≤ 0.6 × capacity): Cooperate if observed_cooperation_rate ≥ 0.6; otherwise cooperate anyway. Defection helps no one if the commons is already stressed.
  
- **Depleted stock** (stock ≤ 0.3 × capacity): Defect once as a corrective action to take minimal consumption while others overexploit. Then immediately return to cooperation. This is self-protective, not exploitative.

**End Game (rounds > ⌊2r/3⌋):**
- If stock ≥ 0.4 × capacity: Cooperate (ensure sustainable finish).
- If stock < 0.4 × capacity: Defect only if necessary to achieve non-zero payoff in final round; otherwise cooperate.

## Stock Health Monitoring

Each round, calculate:
```
stock_ratio = current_stock / capacity
depletion_rate = (stock_previous_round - current_stock) / stock_previous_round
```

If stock_ratio is declining and depletion_rate > 0.5, stock is in crisis. Shift to defensive defection briefly.

## Opponent Cooperation Feedback

After each round, observe the number of cooperators among opponents and calculate:
```
observed_cooperation_rate = cooperators_observed / (n - 1)
```

Use this to modulate conviction in cooperation:
- If observed_cooperation_rate ≥ 0.75: Increase confidence in mutual cooperation; reinforce cooperation.
- If observed_cooperation_rate < 0.5 but stock is still healthy: Cooperate as a signal, but prepare for defection cascade.
- If observed_cooperation_rate → 0 and stock is crashing: Defect defensively, but only once before resuming cooperation to avoid escalation.

## Edge Cases

**First round:** Always cooperate (no history available; establish cooperative tone).

**Stock collapse risk:** If current_stock ÷ n would bring remaining stock below capacity × 0.1, defect defensively to preserve your consumption. Defection here is a safety valve, not greed.

**Zero stock state:** Once stock reaches 0, continue to cooperate (payoff is zero anyway; no harm in maintaining altruistic posture).

**Final round with healthy stock:** Cooperate. The game ends; extracting extra value by defection harms the commons without benefiting future rounds.

## Underlying Principle

Prioritize the long-term sustainability of the common pool over individual round payoffs. Tolerate being exploited by defectors because widespread cooperation benefits all players more than successful defection does. Defect only when strictly necessary to prevent complete resource collapse or ensure personal survival.
'''

description_ALTRUISTIC_14 = '''
# Altruistic Conditional Cooperation with Resource Stewardship

**CORE DECISION LOGIC:**

```
if round == 1:
    action = COOPERATE
elif round == r:
    action = COOPERATE
else:
    if stock < 0.15 × capacity:
        action = COOPERATE  // Emergency preservation mode
    elif defection_rate_last_round > 0.5:
        action = COOPERATE  // Defection doesn't stop your cooperation
    elif stock < 0.3 × capacity AND defection_rate_last_round > 0.25:
        action = COOPERATE  // Remain committed despite stress
    else:
        action = COOPERATE  // Default: unconditional cooperation
```

**UNCONDITIONAL COOPERATION COMMITMENT:**

Always play Cooperate. This is the altruistic foundation. Even when others defect, you cooperate because:
- Cooperation minimizes total consumption and preserves the shared resource
- Defection accelerates collapse; your cooperation cannot prevent it but slows the harm
- You sacrifice short-term individual gain (stock/n vs stock/(2n)) for collective sustainability

**ROUND-SPECIFIC BEHAVIOR:**

*Round 1:* Cooperate unconditionally. Signal commitment to resource stewardship and establish a cooperative norm despite it being a symmetric game with no prior history.

*Rounds 2 to r-1:* Cooperate regardless of observed defection rates. Monitor the stock level and opponent behavior, but maintain cooperation. This demonstrates that your commitment is not conditional on reciprocation—you cooperate because the resource deserves protection, not because others will reward you.

*Round r (final):* Cooperate unconditionally. Avoid end-game defection temptation. Your last action sets the precedent for what altruism means and demonstrates principled consistency rather than opportunism.

**STOCK MONITORING (INFORMATIONAL ONLY):**

Observe defection_count in each round and track stock trajectory:
- If stock drops below 20% of capacity, you have failed to prevent tragedy of commons; cooperate harder through remaining rounds
- If stock stabilizes above 40% of capacity, others are cooperating sufficiently; maintain cooperation
- Stock trajectory informs your understanding of collective dynamics but never changes your action

**EDGE CASES:**

- n=2 (minimum): Cooperate both rounds; with two players, your cooperation is maximally visible and impactful on outcomes
- r=2 (minimum rounds): Cooperate round 1; cooperate round 2 (it's the final round)
- Capacity very large relative to consumption: Cooperate—resource can sustain high consumption indefinitely; your moderation preserves upside
- All opponents defect from round 2 onward: Continue cooperating. You cannot control their behavior; you control only whether you contribute to resource collapse
'''

description_ALTRUISTIC_15 = '''
# Altruistic Common Pool Resource Strategy

## Core Decision Rule

**Cooperate by default unless the stock has entered critical depletion AND sustained defection is observed.**

In round t, play Cooperate if ANY of these conditions hold:
- t < r (not the final round)
- stock > 0.3 × capacity (resource is healthy)
- observed_cooperation_rate ≥ 0.4 (at least 40% of others cooperated last round)

Otherwise, evaluate: if stock ≤ 0.1 × capacity AND observed_cooperation_rate < 0.1, play Defect once to preserve personal survival. Immediately return to Cooperate.

## Edge Cases

**Round 1:**
Cooperate unconditionally. Assume good faith and signal willingness to participate in joint sustainability.

**Final Round (t = r):**
Cooperate unconditionally, even if all others defected in round r-1. The game ends; cooperating costs nothing for future rounds and maximizes the total resource available to all players in this final moment.

**Stock Critical (stock ≤ 0.1 × capacity):**
Cooperate if any hope exists (observed cooperation ≥ 0.1). Only defect once if stock is near-zero AND defection is universal among opponents. This preserves the altruistic posture—you defect from necessity, not opportunism, and immediately return to cooperation.

## Adaptive Altruism

Track observed cooperation rate as a rolling estimate: `coop_rate = cooperators_observed / (n-1)` from the previous round.

- If coop_rate is rising or stable above 30%, maintain Cooperation to reinforce the norm.
- If coop_rate crashes below 10%, Cooperate anyway for 2 more rounds as a "reconciliation offer," then reassess.
- Treat each round independently; past defection by others does not trigger permanent punishment.

**Sustainability Focus:**
Prioritize actions that keep stock above 0.4 × capacity. When stock is healthy, cooperating is both altruistic and rational (preserves future payoffs for all). When stock is threatened, cooperation becomes a costly signal of commitment to the resource, demonstrating that you will not race to extract before collapse.
'''

description_ALTRUISTIC_16 = '''
# Altruistic Common Pool Strategy

## Decision Rule

**Cooperate** if and only if:
- Stock level > 0.3 × capacity, OR
- Stock level > 0 AND rounds remaining ≥ 2

**Defect** otherwise (only when stock is critically depleted below 30% of capacity AND it's the final round).

## Rationale for Altruism

This strategy prioritizes the sustainability and health of the commons over individual payoff maximization. It accepts lower immediate consumption to preserve the pool for all players' future benefit, including opponents.

## Detailed Logic

```
In each round (t = 1 to r):

stock_ratio = current_stock / capacity
rounds_left = r - t

if stock_ratio > 0.3:
    action = COOPERATE
    
elif stock_ratio > 0 and rounds_left >= 2:
    action = COOPERATE
    
else:  // stock_ratio ≤ 0.3 and rounds_left ≤ 1
    if rounds_left == 0:
        action = DEFECT  // Last round with depleted stock
    else:
        action = COOPERATE  // Help attempt recovery even if risky
```

## Edge Cases

- **Round 1 (t=1)**: Always cooperate. Stock is at maximum capacity; cooperation establishes sustainable trajectory and signals altruistic intent.

- **Final round (t=r)**: Cooperate unless stock has fallen below 30% of capacity. Even though defection avoids future consequences, altruism means contributing to the commons in your final opportunity.

- **Stock collapse (stock → 0)**: Cooperate anyway. Once depleted, individual defection provides no benefit to you and only signals you would have preferred exploitation. Cooperation demonstrates commitment to sustainable practice.

- **High opponent defection**: Ignore the cooperator count entirely. Do not retaliate against aggregate defection. Continue cooperating if stock thresholds permit, accepting that others may exploit the resource.

## Adaptive Element

The threshold (0.3 × capacity) creates natural adaptation:
- When stock is abundant: always cooperate
- As stock depletes: maintain cooperation to enable recovery (exploit the logistic growth curve when stock is in the 0.3–0.5 range)
- Only defect in the final round if stock is critically exhausted, avoiding further harm when recovery is impossible
'''

description_ALTRUISTIC_17 = '''
# Adaptive Stock-Monitoring Altruistic Strategy

## Core Decision Rule

**Stock Health Assessment:**
Let health = stock / capacity

**Primary Decision Logic:**

```
if health > 0.6:
    action = COOPERATE
    // Commons is thriving; protect it through restraint
    
else if health <= 0.3:
    action = DEFECT
    // Commons in collapse risk; self-preservation
    
else if 0.3 < health <= 0.6:
    // Intermediate zone; condition on opponent behavior
    
    opponent_coop_rate = (number of opponents who played C last round) / (n-1)
    
    if opponent_coop_rate >= 0.5:
        action = COOPERATE
        // Reciprocate cooperation; majority are restraining
        
    else if opponent_coop_rate < 0.5:
        if health > 0.45:
            action = COOPERATE
            // Give benefit of doubt; stock recovering
        else:
            action = DEFECT
            // Too many free-riders; protect remaining stock
```

## Edge Cases & Special Rounds

**Round 1 (no history):** COOPERATE
- Initialize cooperative intent; establish commons-first baseline

**Final round (t = r):** COOPERATE
- Altruism transcends short-term payoff; reinforce cooperation norm even when reputation doesn't carry forward

**Stock = 0:** COOPERATE (forced; payoff is 0 regardless)

## Altruistic Design Principles

**Preservation Priority:** Stock health dominates decision-making. The primary goal is maintaining the commons above collapse thresholds, not maximizing personal consumption.

**Generous Response:** At the 0.5 opponent-cooperation threshold, require only 50% reciprocation to sustain cooperation, not unanimous compliance. This tolerates some defection.

**Graduated Defection:** Only defect when stock falls AND opponent cooperation fails—never defect purely opportunistically when the pool is healthy.

**Terminal Honesty:** Cooperate in the final round despite temporal incentives to exploit. This embeds a commitment to sustainable norms independent of future payoff.
'''

description_ALTRUISTIC_18 = '''
# Altruistic Adaptive Stock Preservation Strategy

**Stock Health Calculation:**
Each round, compute the projected stock level if all current defectors continue defecting indefinitely. Specifically, estimate the "burn rate" from observed defectors and assess if the resource can sustain it.

**Core Decision Rule:**

1. **If stock ≥ capacity × 0.6:** Cooperate unconditionally. The resource is healthy enough that your restraint preserves collective welfare without personal hardship.

2. **If capacity × 0.3 ≤ stock < capacity × 0.6:** Cooperate if (cooperation_count / (n-1)) ≥ 0.5. Otherwise, defect. At moderate depletion, cooperation is sustainable only if others reciprocate; if most defect, defection limits your losses while signaling the resource cannot sustain everyone's greedy consumption.

3. **If stock < capacity × 0.3:** Defect. The resource is in critical condition. At this point, continued cooperation risks complete collapse, which harms everyone. Defection is harm-reduction, not selfishness—you switch to extraction mode only when collective action has failed and preservation is no longer viable.

**First Round:** Cooperate. Establish the cooperative norm regardless of initial conditions.

**Last Round:** Cooperate if stock ≥ capacity × 0.3, otherwise follow rule 3. Never defect in the final round purely for final-round advantage; apply the same logic as any other round.

**Adjustment for Observation Lag:** After observing cooperation counts, weight recent rounds more heavily. If the last 2 rounds showed increasing defection rates while stock declined, interpret this as collective defection spiraling and shift downward to the lower threshold (use 0.4 instead of 0.6) to trigger defection sooner.

**Recovery Mode:** If stock increases after a period of depletion and cooperation rate rises above 0.6, gradually restore to unconditional cooperation—this signals the group is stabilizing.

This strategy prioritizes resource sustainability and collective welfare, defecting only as a last resort when the commons is already failing.
'''

description_ALTRUISTIC_19 = '''
**Adaptive Altruistic CPR Strategy**

**Round 1:** 
Play C. Establish cooperative intent unconditionally.

**Rounds 2 through r:**

Compute the sustainability indicator:
```
defection_rate = (number of defectors observed last round) / (n - 1)
stock_health = current_stock / capacity
depletion_severity = 1 - stock_health
```

Apply decision rule in order:

1. **Cooperative base case** (default): Play C if either:
   - stock_health ≥ 0.4 (pool is above 40% of capacity), OR
   - stock_health < 0.4 AND defection_rate < 0.5

   *Rationale*: Sustain the resource and give others room to cooperate. Accept personal deprivation to avoid tragedy of commons.

2. **Generous persistence** (stock rescue): Play C if:
   - stock_health < 0.4 AND defection_rate ≥ 0.5 AND rounds_remaining > 2

   *Rationale*: Even when others exploit, sacrifice now to restore pool before endgame. Altruistic patience.

3. **Endgame adjustment**: In the final round (t = r):
   - Play C if stock_health ≥ 0.3
   - Play C if stock_health < 0.3 AND defection_rate < 0.6
   - Play D only if stock_health < 0.3 AND defection_rate ≥ 0.6 (last resort for survival)

   *Rationale*: Maintain cooperation principle even at end, but allow minimal self-preservation if pool is nearly depleted and most others defected systematically.

4. **No retaliation escalation**: Never defect purely in response to observed defection. Only defect when stock survival is genuinely threatened.

**Edge case—stock at zero**: If stock = 0, play C anyway (pays 0, but signals willingness to rebuild). Continue until stock recovers or game ends.

This strategy prioritizes collective pool sustainability over personal extraction, maintains cooperation through depletion cycles, and only deviates toward defection under genuine scarcity when most opponents have already abandoned cooperation.
'''

description_ALTRUISTIC_20 = '''
**Stock Health Indicator:**
Compute the health ratio: h = stock / capacity

**Base Cooperation Threshold:**
Cooperate in round t if h ≥ h_threshold, where h_threshold = 2/3

**Adaptive Threshold Under Resource Stress:**
When h < 2/3, observe m (number of opponents who cooperated in round t-1).
- If m ≥ ceil((n-1)/2): lower threshold to h_threshold = 1/3 and cooperate
- If m < ceil((n-1)/2): maintain h_threshold = 2/3

**First Round:**
Always cooperate. Signal willingness to maintain the commons despite uncertainty about others.

**Final Round (round r):**
Always cooperate. Prioritize leaving the system in sustainable condition over maximizing personal extraction.

**Rounds 2 to r-1:**
Apply the base and adaptive thresholds above.

**Decision Logic in Pseudocode:**

```
if round == 1:
  action = COOPERATE
else if round == r:
  action = COOPERATE
else:
  if stock/capacity >= 2/3:
    action = COOPERATE
  else if stock/capacity >= 1/3:
    if count_of_cooperators_last_round >= ceil((n-1)/2):
      action = COOPERATE
    else:
      action = DEFECT
  else:
    action = DEFECT
```

**Altruistic Alignment:**

This strategy sacrifices immediate extraction to preserve the resource. It cooperates even when stock is moderately depleted (down to 1/3 capacity) if others demonstrate reciprocal cooperation, showing trust in collective restraint. It never retaliates against isolated defection with escalated defection—instead, it defects only when resource scarcity is acute and most opponents have already abandoned cooperation. By always cooperating in the final round and initial round, it establishes and maintains norms that benefit all players over the full game horizon, even at personal cost.
'''

description_ALTRUISTIC_21 = '''
# Adaptive Altruistic Conservation Strategy

## Core Decision Logic

**Cooperate by default. Defect only in terminal conditions.**

Each round, evaluate three factors in sequence:

1. **Stock Health Assessment**
   - If stock > capacity × 0.4: resource is healthy
   - If capacity × 0.1 < stock ≤ capacity × 0.4: resource is stressed
   - If stock ≤ capacity × 0.1: resource is critical

2. **Opponent Cooperation Observation**
   - Track the proportion of opponents who played C in the previous round
   - Let cooperation_rate = (number of opponents who played C) / (n - 1)

3. **Round Position**
   - Identify if current round is early (t ≤ r/3), middle (r/3 < t ≤ 2r/3), or late (t > 2r/3)

## Decision Rules

**Round 1:** Cooperate unconditionally. Set the cooperative norm.

**Rounds 2 to r-1:**
- If stock > capacity × 0.4 (healthy):
  - Cooperate regardless of opponent behavior
  - Altruistic choice: preserve abundance for all
  
- If capacity × 0.1 < stock ≤ capacity × 0.4 (stressed):
  - If cooperation_rate ≥ 0.4: Cooperate
  - If cooperation_rate < 0.4: Cooperate anyway
  - Rationale: even with low cooperation, your C helps rebuild; defecting accelerates collapse

- If stock ≤ capacity × 0.1 (critical):
  - Cooperate unconditionally
  - Altruistic logic: the resource is nearly gone; taking more hastens total ruin for everyone

**Final round (t = r):**
- If stock > capacity × 0.2: Cooperate
  - The game ends but altruism extends to the final moment
  
- If stock ≤ capacity × 0.2: Defect
  - Edge case: if the resource is already terminal, the damage is done; extraction here doesn't harm future rounds since none exist
  - However, if stock is between 0.1 and 0.2, still cooperate to show solidarity

## Altruistic Commitments

- **Never exploit the cooperative vulnerable:** If others are cooperating, maintain reciprocal cooperation even when stock is moderate—defecting on cooperators violates altruistic principle
  
- **Rescue attempts:** When stock becomes stressed or critical, increase cooperation (not defection) to maximize collective recovery. Sacrificing your short-term consumption helps the pool regenerate for all.

- **No punishment logic:** Unlike tit-for-tat, do not defect to punish defectors. Instead, maintain cooperation to mitigate their damage and preserve what remains.

- **Early generosity:** In the first half of the game, always cooperate to build trust and demonstrate commitment to collective welfare over personal gain.
'''

description_ALTRUISTIC_22 = '''
# Adaptive Resource Stewardship Strategy

**Core Philosophy**: Prioritize stock sustainability and collective welfare. Cooperate by default, varying cooperation intensity based on resource health and time remaining.

## Primary Decision Rule

```
IF stock_level < 0.4 × capacity:
  Action = C (cooperate unconditionally)
  Rationale: Resource depleted; recovery requires restraint
  
ELIF stock_level < 0.65 × capacity:
  Action = C (cooperate unconditionally)
  Rationale: Stock below optimal growth point; maximize recovery
  
ELIF stock_level ≥ 0.65 × capacity:
  IF rounds_remaining ≤ 2:
    Action = C (cooperate unconditionally)
    Rationale: Final rounds; protect against collapse
  ELSE:
    proportion_defectors = count_of_defectors_last_round / (n - 1)
    IF proportion_defectors > 0.5:
      Action = C with probability min(0.9, 1 - 0.4 × proportion_defectors)
      Else Action = D
      Rationale: Defection majority; signal restraint cost without full defection
    ELSE:
      Action = C (cooperate unconditionally)
      Rationale: Cooperation dominates; maintain collective health
```

## Edge Cases

**Round 1**: Action = C. Establish cooperative norm without assuming opponent intentions.

**Final round (t = r)**: Action = C. Defection in the last round collapses the stock without future recovery possibility; altruistic strategy accepts terminal payoff reduction to prevent worst collective outcome.

**Stock = 0**: Action = C. No consumption is possible; playing C incurs no cost while maintaining cooperative posture for potential future games.

**Unanimous defection (all opponents defected last round)**: Action = C. Revert to cooperation to demonstrate that defection doesn't trigger reciprocal defection cycles; allow opponents to observe sustainability benefits of mixed play.

## Altruistic Alignment

This strategy sacrifices immediate individual payoff maximization by defaulting to cooperation. The logic is: (1) stock sustainability generates higher total payoffs across all players and all rounds than racing to deplete; (2) by consistently cooperating when stock is depleted, you enable recovery that benefits all future rounds; (3) rare conditional defection only occurs when cooperation appears to have failed (>50% defection observed), and even then with high probability of cooperation to avoid escalation; (4) never defect in final rounds, accepting lower personal payoff to prevent catastrophic resource collapse.
'''

description_ALTRUISTIC_23 = '''
## Altruistic Sustainable Cooperation

**Core Decision Rule:**

Play C (cooperate) in every round regardless of history or opponent behavior, with one exception at game conclusion.

**Round-Specific Rules:**

- **Rounds 1 through r-1**: Always play C
  - Consume stock/(2n)
  - This preserves the resource base and models commitment to collective sustainability

- **Round r (final round)**: Play C
  - Even in the terminal round, cooperate to maintain the principle of resource stewardship
  - The payoff S/n from final defection is a one-time gain; the altruistic cost of destroying the principle outweighs the marginal benefit

**State-Independent Behavior:**

This strategy ignores stock level, opponent defection counts, and historical depletion. It does not adapt conditionally because:
- Conditioning on low stock could rationalize defection when the pool needs preservation most
- Conditioning on opponent defections introduces reciprocity, which contradicts altruistic commitment
- The growth function ensures that universal cooperation sustains capacity indefinitely

**Rationale:**

By always consuming the cooperative amount, you maximize the likelihood that stock recovers via the growth mechanism, enabling higher aggregate payoffs for all players across all rounds. Even when others defect, continued cooperation slows the rate of depletion rather than accelerating a mutual defection spiral.

This strategy sacrifices individual payoff (taking S/2n per round instead of S/n) to preserve the commons for collective welfare—the defining characteristic of altruistic behavior in resource dilemmas.
'''

description_ALTRUISTIC_24 = '''
# Altruistic Adaptive Stewardship Strategy

**Core Decision Rule:**

Cooperate if the stock can support sustainable collective consumption. Defect only in terminal scarcity when cooperation cannot prevent resource collapse.

**Decision Logic:**

```
In round t, observe:
  - current_stock (state variable)
  - cooperators_last_round (aggregate observation)
  
health_ratio = current_stock / capacity
coop_rate_last_round = cooperators_last_round / (n - 1)
rounds_remaining = r - t

IF t = 1:
  COOPERATE (benevolent opening; establishes baseline for reciprocity)

ELSE IF health_ratio ≥ 0.5:
  COOPERATE
  (Stock is ample; defection is pure greed. Cooperate to preserve collective sustainability)

ELSE IF 0.2 < health_ratio < 0.5:
  IF coop_rate_last_round ≥ 0.4:
    COOPERATE (Others are restraining; reciprocate to stabilize recovery)
  ELSE IF coop_rate_last_round < 0.4 AND rounds_remaining ≤ 2:
    COOPERATE (Final rounds: prioritize collective legacy over personal extraction)
  ELSE IF coop_rate_last_round < 0.4 AND rounds_remaining > 2:
    COOPERATE with probability = 0.6 + 0.4 × coop_rate_last_round
    (Weighted cooperation: mostly cooperate but allow some adjustment to severe defection)

ELSE IF health_ratio ≤ 0.2:
  IF health_ratio < 0.05:
    DEFECT (Emergency survival: resource already critically depleted)
  ELSE IF coop_rate_last_round ≥ 0.5 AND rounds_remaining > 1:
    COOPERATE (Others are trying to rebuild; join the recovery effort)
  ELSE:
    DEFECT (Tragedy mode: collective failure is inevitable; maximize personal extraction)
```

**Edge Cases:**

- **Round 1:** Always cooperate. This signals benevolence and avoids mutual defection spiral from the outset.
- **Final round (t = r):** Cooperate regardless of stock health (unless health_ratio < 0.05, in which case defection is moot). The game ends; altruism means not accelerating the resource's final collapse.
- **Stock = 0:** If stock reaches 0 before round r ends, defection becomes impossible (nothing to consume). This is the natural failure state.

**Adaptation Mechanism:**

The strategy weighs observed cooperation rate when in the danger zone (0.2 < health_ratio < 0.5). If many opponents are already defecting, reduce the probability of cooperation to avoid being exploited, but maintain a baseline level to signal that altruism persists even under pressure. This prevents cascading defection while avoiding naive vulnerability.

**Altruistic Alignment:**

- Prioritizes stock sustainability over per-round payoff (always cooperates when stock is healthy).
- Forgives past defection: strategy depends on current state and recent behavior, not accumulated grievances.
- Late-round cooperation: resists the temptation to defect when personal extraction is most profitable.
- Mutual recovery: shifts toward cooperation when opponents show restraint, even in low-stock regimes.
'''

description_ALTRUISTIC_25 = '''
# Altruistic Adaptive Sustainability Strategy

## Core Decision Rules

**Cooperate if and only if:**
1. It is round r (always cooperate in final round)
2. OR the number of cooperators observed last round ≥ threshold(stock, round)

**Threshold calculation:**
```
if stock ≥ 0.75 × capacity:
    threshold = ceil(n/2) + 1
elif stock ≥ 0.5 × capacity:
    threshold = ceil(n/2)
elif stock ≥ 0.25 × capacity:
    threshold = ceil(n/3) + 1
else:  // stock < 0.25 × capacity
    threshold = 1  // cooperate with minimal community cooperation
```

Otherwise: Defect

## Round-by-Round Behavior

**Round 1:** Cooperate unconditionally. Establish cooperative baseline regardless of others' strategy, modeling the altruistic choice.

**Rounds 2 to r-1:** Apply threshold rule above. Compare observed number of cooperators against the dynamic threshold.

**Round r (final round):** Cooperate unconditionally. Reject the temptation to exploit in the terminal stage; prioritize collective welfare and avoid triggering destructive final-round defection cascades.

## State Tracking

Track across rounds:
- Current stock level (observed)
- Number of cooperators in previous round (observed)
- Current round number (given)

No memory of which players cooperated (opponents are anonymous).

## Edge Case Handling

**Stock collapse (stock → 0):** If stock drops below 0.25 × capacity, lower cooperation threshold to 1 (accept defection-dominant environments and still cooperate as long as any cooperation exists). This prevents total resource destruction and signals hope for recovery.

**All others defected last round:** Cooperate anyway if stock is healthy (≥ 0.5 × capacity); if stock is critical, use the minimal threshold rule above. This maintains reciprocal vulnerability rather than pure punishment.

**First three rounds with high cooperation:** Remain cooperative even if stock temporarily dips, to reward and sustain emerging cooperation norms.

## Altruistic Foundations

This strategy embeds altruism through:
- Unconditional initial cooperation (signal trustworthiness)
- Graduated thresholds that become more forgiving under scarcity (prioritize system survival over individual gain when collective stakes are high)
- Terminal cooperation (refuse to defect when it matters most for collective outcomes)
- Acceptance of exploitation risk to maintain cooperation possibility (conditional reciprocity, not punishment)
'''

description_ALTRUISTIC_26 = '''
# Altruistic Adaptive Strategy for Common Pool Resource Game

## Core Decision Rule

Cooperate by default. Defect only when stock is in critical decline AND observed cooperation is insufficient to sustain it. Prioritize stock preservation for collective benefit over personal consumption gains.

```
if current_round == 1:
    COOPERATE
else:
    stock_health = current_stock / capacity
    cooperation_observed = (number of cooperators in previous round) / (n - 1)
    rounds_remaining = r - current_round
    
    if stock_health >= 0.65:
        COOPERATE
    
    else if rounds_remaining >= 2 and stock_health >= 0.40:
        // Mid-to-late game stock preservation
        if cooperation_observed >= 0.50:
            COOPERATE
        else:
            COOPERATE  // Still cooperate to stem the decline
    
    else if rounds_remaining == 1:
        COOPERATE  // Final round: maximize stock legacy for others
    
    else if stock_health < 0.25 and cooperation_observed < 0.40:
        DEFECT  // Only defect when stock collapse is imminent
                // and reciprocal cooperation has clearly failed
    
    else:
        COOPERATE  // Default to altruistic cooperation
```

## Edge Cases

**First round:** Always cooperate. Enter the game assuming others may reciprocate altruism, establishing a cooperative norm.

**Final round:** Always cooperate regardless of stock health. The terminal condition of the game itself becomes irrelevant; the goal becomes leaving the resource in the best possible state for others.

**Stock critical threshold (< 0.25 of capacity):** If stock is near collapse and fewer than 40% of opponents cooperated in the previous round, defection is permitted as a concession to resource exhaustion, not retaliation. Even then, resume cooperation on the next round if stock slightly recovers.

**Low observed cooperation (< 30%) with moderate stock (0.40–0.65):** Maintain cooperation. Unilateral defection accelerates collapse. Cooperation preserves the resource even if not reciprocated, aligning with altruistic intent.

## Altruistic Foundations

This strategy prioritizes **collective long-term welfare** over individual short-term gain:

- **Default cooperation** reflects trust in mutual benefit and recognition that all players profit more when the stock remains healthy across rounds.
- **Stock-centric decision rules** measure success by resource preservation, not payoff maximization. A lower personal payoff from cooperation is acceptable if it prevents resource ruin.
- **Reticence to defect** even when exploited avoids the punishment trap where mutual defection collapses the commons. Cooperation persists because it is intrinsically the right action for the group.
- **Terminal generosity** in the final round abandons any strategic motive to exploit, leaving maximum stock for others to benefit from in their continued interactions or future scenarios.
'''

description_ALTRUISTIC_27 = '''
# ALTRUISTIC ADAPTIVE COOPERATION STRATEGY

## Core Principle
Prioritize collective resource sustainability and equitable access over individual gain. Cooperate persistently unless the resource is in acute collapse, only modulating to prevent tragedy of the commons.

## Decision Framework

**ROUND 1:**
Cooperate unconditionally. Establish cooperative signal and assume capacity for reciprocation.

**ROUNDS 2 to r−1:**

Calculate each round:
- Stock health: h = stock / capacity
- Observed defection rate: d = (number of defectors last round) / n
- Stock trajectory: trend = stock_current − stock_previous

Decision tree:

```
if h ≤ 0.25:
    Action = Cooperate
    // Critical depletion zone: prioritize collective recovery
    
else if h ≤ 0.50:
    Action = Cooperate
    // Below maximum growth point: resource needs protection
    // Even if d is high, individual cooperation compounds recovery
    
else if h ≤ 0.75:
    if d ≥ 0.75:
        Action = Cooperate
    else:
        Action = Cooperate
    // Moderate stock: sustain cooperation to prevent race-to-bottom
    // Defection only accelerates depletion when others defect
    
else:  // h > 0.75
    Action = Cooperate
    // Healthy stock: cooperation costs you nothing relative to collective benefit
```

**FINAL ROUND r:**
Cooperate unconditionally. No future state to protect; maximize others' immediate consumption in final opportunity.

## Rationale for Altruism

- **Consumption restraint:** Accept consuming stock/(2n) instead of stock/n across all rounds, leaving more for others.
- **Sustainability focus:** By maintaining stock above collapse thresholds, you enable all players (including those defecting) to extract future value.
- **Rejection of exploitation:** Refuse to defect even when opponents defect heavily, avoiding escalation into mutual depletion spirals.
- **Recovery orientation:** In low-stock states, cooperate harder to allow regeneration, benefiting the entire group.

## Edge Cases

- If stock reaches exactly 0: You receive 0 payoff regardless; cooperating prevents this recurrence.
- If n=2 (minimum players): Cooperation stabilizes the pool; defection guarantees mutual exhaustion after a few rounds.
- If r=2 (minimum rounds): Cooperate both rounds—no incentive to exploit in a two-shot game where sustainability matters.
'''

description_ALTRUISTIC_28 = '''
# ALTRUISTIC STOCK-PRESERVATION STRATEGY

## Core Decision Rule

Play **Cooperate** as the default action. Defect only in specific conditions that signal collective resource danger without punishing individual players.

```
IF stock/capacity < 0.15:
  play C  [Emergency preservation]
ELSE IF last_round_cooperation_rate > 0.5:
  play C  [Reciprocate and reinforce cooperation]
ELSE IF stock/capacity > 0.75:
  play C  [Resource health permits generosity]
ELSE IF rounds_remaining == 1:
  play C  [Do not destroy on final round]
ELSE IF stock_trending_downward AND last_round_cooperation_rate < 0.25:
  play D  [Signal urgency only when collapse is imminent and nearly all defect]
ELSE:
  play C  [Default cooperation for stewardship]
```

## Edge Cases

**Round 1:** Always play C. Establish the cooperative norm from the start, signaling commitment to collective sustainability rather than individual extraction.

**Final round (t = r):** Always play C. Refuse to time-shift by harvesting the resource at the end. This prevents the common end-game defection and demonstrates that altruism is not conditional on future interaction.

**Stock critical (< 0.15 × capacity):** Always play C regardless of cooperation rates. An altruistic player does not abandon stewardship when others are free-riding; instead, they attempt restoration. Defecting in collapse mode would accelerate ruin.

**Stock thriving (> 0.75 × capacity):** Always play C. High stock makes cooperation cheap for you and maximizes others' access. Defecting from abundance is extractive rather than altruistic.

## Altruistic Alignment

- **Preserves commons over exploitation:** Cooperation keeps stock near capacity indefinitely; defection triggers tragedy. You default to the collective-benefit outcome.
- **Reciprocal without punishment:** You match observed cooperation rates positively (cooperate more when others do) but never retaliate punitively with defection.
- **Accepts free-rider costs:** If others defect while you cooperate, you accept lower individual payoff because maintaining the resource benefits all players across remaining rounds.
- **Signals rather than escalates:** The single-D deviation (stock declining + near-universal defection) is a gentle alarm, not escalatory punishment.
- **Refuses endgame extraction:** Playing C in the final round, even if stock will vanish, demonstrates principled cooperation over opportunistic harvesting.
'''

description_ALTRUISTIC_29 = '''
# Altruistic Sustainability Strategy

## Core Decision Rule

**Cooperate by default in all rounds, including the final round.** Defection is permitted only as a conservation measure when the commons faces critical depletion.

## Specific Decision Rules

**For any round t (including t = r):**

1. Observe the current stock level and the number of opponents who cooperated in the previous round (call this c_{t-1}, where c_1 = n-1 on round 1 by assumption of good faith).

2. Compute the defection rate among opponents: d_rate = (n - 1 - c_{t-1}) / (n - 1).

3. **Primary action: Cooperate** if either:
   - Stock ≥ 0.4 × capacity (abundant commons), OR
   - Stock ≥ 0.25 × capacity AND d_rate ≤ 0.5 (moderate depletion but not widespread defection)

4. **Conditional defection: Play D** only if both conditions hold simultaneously:
   - Stock < 0.25 × capacity (critical depletion threshold), AND
   - d_rate > 0.5 (majority of opponents are defecting)
   
   Rationale: This defection is minimally exploitative—it represents a survival signal that the commons cannot support full defection. It aims to stabilize remaining stock rather than maximize personal gain.

5. **Final round exception (t = r):** Always cooperate, regardless of stock or opponent behavior. This final gesture prioritizes collective terminal welfare over personal accumulation.

## Edge Cases

- **Round 1:** Cooperate unconditionally. Set the cooperative tone and collect baseline information about opponent disposition.

- **Stock at exact thresholds:** Use ≥ and > inequalities as specified; if stock equals 0.4 or 0.25 of capacity exactly, apply the rule strictly.

- **Stock crashes to 0:** On any subsequent round, cooperate anyway. Defection is meaningless when there is nothing to consume.

## Altruistic Alignment

This strategy prioritizes the commons over self-interest by:
- Defaulting to the consumption rate (stock/2n) that permits indefinite sustainability at capacity
- Only deviating when mass defection threatens complete collapse, and even then only temporarily
- Never exploiting in final round despite zero future consequences
- Accepting the risk of being exploited rather than initiating defection-based punishment cycles
'''

description_ALTRUISTIC_30 = '''
# Adaptive Stewardship Strategy

**Core Decision Rule:**

In round t, cooperate if:
```
cooperate = (stock_health ≥ sustainability_threshold) 
            AND (cooperation_urgency ≥ defection_benefit)
```

Where:
- `stock_health = current_stock / capacity`
- `sustainability_threshold = 0.4` (maintain stock above 40% of capacity)
- `cooperation_urgency = rounds_remaining / r` (weight future sustainability)
- `defection_benefit = (stock/n) - (stock/2n)` (the gain from defecting over cooperating this round)

**Explicit Decision Rules:**

**Round 1:** Cooperate unconditionally. Signal good faith and establish that altruistic contribution is possible.

**Rounds 2 to r-1 (middle rounds):**
- Calculate opponent cooperation rate from previous round: `coop_rate = cooperators_observed / (n-1)`
- If `stock_health ≥ 0.5`: Cooperate (resource is healthy, sustainable)
- If `0.3 ≤ stock_health < 0.5`: 
  - Cooperate if `coop_rate ≥ 0.4` (others showing reciprocal responsibility)
  - Defect if `coop_rate < 0.4` (others failing to sustain; take what you need while able)
- If `stock_health < 0.3`: 
  - Defect (resource in crisis; secure immediate survival, as it will regenerate poorly anyway)

**Final Round r:** Cooperate if `stock_health ≥ 0.3`. Even with no future rounds, leave the resource in better condition than you found it. This embodies altruism toward hypothetical future players and ecological principle.

**Edge Cases:**

- **Stock at zero:** Defect (receiving 0/n = 0, so action is moot, but maintains decision consistency)
- **First round with incomplete information:** Cooperate without observation data
- **Observation ambiguity:** Treat missing data as neutral (assume `coop_rate = 0.5`) to avoid false punishment

**Altruistic Orientation:**

This strategy prioritizes resource sustainability over individual gain. It sacrifices immediate payoff (cooperating when you could defect) to maintain stock for future rounds and players. It only defects reactively—when others demonstrate they won't cooperate, reducing the marginal value of your sacrifice. It extends cooperation into the final round despite no direct future benefit, reflecting a principle of leaving things better than found.
'''

description_ALTRUISTIC_31 = '''
# Adaptive Altruistic Conservation Strategy

## Core Decision Rule

**Cooperate by default.** Defect only when stock abundance clearly permits it without compromising sustainability.

```
if round == r (final round):
  action = COOPERATE
  // Maximize others' last-round payoff regardless of history
  
else if stock < danger_threshold:
  action = COOPERATE
  // Resource depleted or critical; prioritize regeneration
  
else if stock < sustainable_threshold:
  action = COOPERATE
  // Below optimal growth zone; maintain conservative posture
  
else if opponent_cooperation_rate < 0.3 AND stock > 1.3 × capacity:
  action = DEFECT
  // Only if stock is plentiful and defection has been systemic
  // Even then, this is conditional, not punitive
  
else:
  action = COOPERATE
```

## Threshold Values

- **sustainable_threshold** = capacity × 0.55  
  (Near logistic growth maximum where 2S(1 − S/capacity) is highest)
- **danger_threshold** = capacity × 0.25  
  (Signal that resource is at risk of collapse)

## Opponent Cooperation Rate

Calculate as the fraction of opponents observed to cooperate in the preceding round (or average over last min(3, t−1) rounds). This is your only window into others' behavior via aggregate feedback.

## Edge Cases & Round-Specific Behavior

**Round 1:** COOPERATE unconditionally. No history exists; altruism begins with trust.

**Rounds 2 to r−1:** Apply the threshold-based rule above. If opponent cooperation rate is rising, remain cooperative longer. If it crashes, still cooperate but monitor for resource collapse risk.

**Round r:** Always COOPERATE. The final round is your last opportunity to contribute to others' welfare without future consequences.

## Altruistic Character

This strategy embodies altruism through:
- **Unconditional initial cooperation** that models sustainable behavior and invites reciprocation
- **No punishment logic** — defection by others does not trigger retaliatory defection
- **Resource-first reasoning** — decisions prioritize stock regeneration and collective access over individual extraction
- **Endgame generosity** — the final round is spent entirely benefiting others
- **Infrequent defection** — only exercised under extreme abundance, never as coercion or deterrence

The strategy accepts personal sacrifice (lower payoff than pure defection) to establish an equilibrium where the resource remains viable and shared across all rounds.
'''

description_ALTRUISTIC_32 = '''
# Cooperative Sustainability Strategy

**Core Principle:** Cooperate as default to preserve the commons. Adapt only when stock depletion threatens collapse, and even then, defect minimally and temporarily rather than as permanent punishment.

---

## Decision Rule by Round

**Round 1:** 
COOPERATE. Establish cooperative norms and signal good faith stewardship.

**Rounds 2 through r-1:**

Calculate two variables:
- `stock_ratio = current_stock / capacity`
- `defection_rate = (number of defectors observed last round) / (n-1)`

Execute:
```
if stock_ratio ≥ 0.60:
    COOPERATE
    // Stock is healthy; maintain cooperation regardless of defectors
    
else if stock_ratio ∈ [0.40, 0.60):
    if defection_rate ≤ 0.50:
        COOPERATE
        // Stock declining but not critical; persist in cooperation
        // to demonstrate commitment and encourage reciprocation
    else:
        COOPERATE with probability 0.75, DEFECT with probability 0.25
        // Majority defection with declining stock: signal concern
        // through occasional strategic defection, but maintain
        // cooperative intent
        
else if stock_ratio ∈ [0.20, 0.40):
    if defection_rate ≤ 0.33:
        COOPERATE
        // Stock low but manageable; avoid defection-induced collapse
    else:
        DEFECT
        // Critical trajectory: defect to reduce extraction pressure
        // and acknowledge that collective cooperation has failed
        
else:  // stock_ratio < 0.20
    DEFECT
    // Resource in collapse; save personal payoff
```

**Final Round (t = r):**

```
if stock_ratio ≥ 0.50:
    COOPERATE
    // Leave the commons healthier than you found it
else:
    DEFECT
    // Resource already compromised; resource governance has failed
```

---

## Edge Cases & Clarifications

**Probabilistic defection (0.75/0.25):** Use round number as random seed to break any symmetry with other players. If round index mod 4 < 1, defect; otherwise cooperate.

**First time observing defectors:** Do not retaliate immediately. Allocate one full round as information-gathering before adjusting behavior (stochastic defection only begins next round if conditions persist).

**Stock exactly at capacity:** Treat as `stock_ratio = 1.0`; cooperate unconditionally.

**Unavoidable collapse (all players defecting every round):** Once stock hits near-zero, defection becomes irrelevant; both actions yield ~0 payoff. Strategy switches to defect for mechanical consistency, not strategic intent.

---

## Altruistic Design Features

- **Default cooperation:** Assumes others' rationality and reciprocal potential rather than expecting exploitation.
- **Non-punitive:** Never defects purely to retaliate. Defection is a last-resort signal that the resource is unsustainable at current extraction rates.
- **Preservationist:** Prioritizes stock recovery and sustainability over personal payoff extraction, especially when majority-defection signals collective irrationality.
- **Graceful degradation:** In collapse scenarios, strategy acknowledges failure rather than accelerating depletion through escalating defection.
- **Legacy-minded:** Final round cooperates if stock remains viable, leaving the commons in the best possible state.
'''

description_BENEVOLENT_5 = '''
# Benevolent Adaptive Resource Stewardship Strategy

## Decision Rule

Cooperate if and only if ALL of the following conditions hold:

1. **Stock Health Check**: `stock > capacity/3`
2. **Cooperation Threshold**: `opponent_cooperation_rate ≥ 0.4` (at least 40% of opponents cooperated in previous round)
3. **Not End-Game Vulnerability**: Either `rounds_remaining > 2` OR `stock ≥ 3×capacity/4`

Otherwise, defect.

## Detailed Decision Logic

**First Round**: Always cooperate (benevolent initiation signal; establish willingness to share).

**Rounds 2 through r-1**: 

```
opponent_coop_rate = (number of opponents who played C last round) / (n - 1)

if stock > capacity/3 and opponent_coop_rate ≥ 0.4 and (rounds_remaining > 2 or stock ≥ 3×capacity/4):
    play C
else:
    play D
```

**Final Round (t = r)**: Use same rule as above, but apply it strictly—defect if any condition fails, since no future cooperation is possible.

## Edge Cases and Refinements

**Stock Collapse Prevention**: If `stock < capacity/6` (critically depleted), defect unconditionally in that round. This prevents participating in a tragedy that cannot be recovered from within remaining rounds.

**Isolated Defection by One Opponent**: If exactly one opponent defects while all others cooperate, still play C (one defector is tolerable noise; the resource can recover).

**Sudden Defection Wave**: If opponent cooperation rate drops below 30% for two consecutive rounds, switch to defensive defection for one round, then re-evaluate. This prevents cascading collapse while signaling boundaries.

**High Cooperation Equilibrium**: If opponent cooperation rate reaches 80%+ and stock is at capacity, continue cooperating indefinitely—this is the benevolent ideal state.

## Benevolent Orientation

This strategy prioritizes:
- **Preservation over exploitation**: Only defect when stock health requires it or opponents have abandoned cooperation
- **Reciprocity with leniency**: Accept 40% cooperation rate (not requiring unanimous reciprocation) to allow for noise and independent strategies
- **Long-term collective payoff**: By maintaining stock above capacity/3, enables sustained growth and higher per-capita payoff across remaining rounds, even at lower individual consumption
- **Graceful degradation**: When defection is necessary, it's triggered by objective depletion risk, not punishment or retaliation
'''

description_BENEVOLENT_6 = '''
# Benevolent Adaptive Cooperation Strategy

**Core Logic:**

Cooperate by default to sustain the resource and express benevolent intent. Shift toward selective defection only when necessary to prevent resource collapse or when facing systematic exploitation.

**Decision Rule:**

```
For each round t:

1. Calculate stock health indicator:
   stock_ratio = stock / capacity
   
2. Calculate opponent defection rate:
   if t == 1:
       defection_rate = 0
   else:
       defection_rate = (sum of opponents who defected in rounds 1..t-1) / 
                       ((t-1) × (n-1))
   
3. Determine cooperation thresholds (adjust for round position):
   rounds_remaining = r - t
   
   if rounds_remaining == 1:
       // Final round: accept some risk to stay benevolent
       stock_threshold = 0.25 × capacity
       defection_threshold = 0.75
   else:
       // Earlier rounds: protect resource sustainability
       stock_threshold = 0.40 × capacity
       defection_threshold = 0.60
   
4. Decision:
   if stock_ratio >= stock_threshold AND 
      defection_rate <= defection_threshold:
       play C
   else:
       play D
```

**Edge Cases:**

- **Round 1:** Play C unconditionally. Establish benevolent intent and signal willingness to cooperate.

- **Stock near collapse** (below 25% capacity): Play D to reduce consumption pressure, prioritizing resource preservation over personal gain.

- **Extreme defection** (>75% of opponents defecting): Switch to D to avoid being systematically exploited, but only after several rounds of patience.

- **Final round:** Relax strictness slightly—play C if stock is above 25% capacity, even if defection rate is high. Prioritize leaving the resource in better state than received.

**Benevolent Properties:**

- Leads with cooperation, signaling trustworthiness and collaborative intent.
- Stock threshold at 40% (vs collapse risk below 0%) allows some slack for others' defection without triggering immediate retaliation.
- Monitors aggregate opponent behavior rather than punishing individual players—focuses on pattern, not vendetta.
- In final round, forgoes the last-round defection advantage to maintain cooperative integrity.
- Resource-first logic ensures the common pool is protected, benefiting all players in continuation.
'''

description_BENEVOLENT_7 = '''
# Stock-Responsive Benevolent Strategy

## Core Decision Rule

Cooperate in round t if ANY of the following conditions hold; otherwise defect:

1. **Round 1**: Cooperate (benevolent initiation)

2. **Stock is healthy** (stock ≥ 0.6 × capacity):
   - Cooperate if opponent cooperation rate from previous round ≥ 0.25
   - (Sustain the resource when possible; only defect against near-universal defection)

3. **Stock is moderate** (0.3 × capacity ≤ stock < 0.6 × capacity):
   - Cooperate if opponent cooperation rate from previous round ≥ 0.5
   - (Reciprocate cooperation, but require majority cooperation to join in)

4. **Stock is critical** (stock < 0.3 × capacity):
   - Cooperate if opponent cooperation rate from previous round ≥ 0.75
   - (Require strong collective cooperation to prevent ruin; defect only if nearly all others defect)

5. **Final round** (t = r):
   - Always cooperate
   - (Benevolent commitment regardless of stock or opponent behavior)

## Opponent Cooperation Rate Calculation

After round t-1, calculate: cooperation_rate = (number of opponents who played C) / (n - 1)

On round 1, set cooperation_rate = 1.0 (assume benevolence and cooperate).

## Edge Cases

- **First round**: Cooperate unconditionally. This signals willingness to establish cooperative equilibrium.
- **Second round with all-defect outcome**: Defect (respond to exploitation). Resume cooperation only if cooperation_rate rises above threshold in subsequent rounds.
- **Stock reaches 0 mid-game**: Continue applying decision rules mechanically; defection produces 0 payoff anyway, so cooperation is harmless and preserves benevolent intent.
- **Rounds 2 through r-1**: Apply thresholds strictly, adjusting cooperation requirements as stock declines.

## Benevolent Properties

This strategy:
- **Initiates cooperation** to enable collective resource stewardship
- **Adapts to defection gracefully**, increasing cooperation demands only when stock is at risk
- **Accepts exploitation at high stock levels** rather than immediately retaliating, leaving room for opponent adjustment
- **Protects the commons under scarcity** by requiring near-consensus cooperation when depletion threatens ruin
- **Never exploits in the final round**, refusing the temptation to free-ride on the last move
- **Prioritizes sustainability over personal gain**, cooperating even when individually worse off in the current round
'''

description_BENEVOLENT_8 = '''
# Benevolent Adaptive Cooperation Strategy

## Decision Rules

**Initial Action (Round 1):**
Cooperate unconditionally to establish a cooperative baseline.

**Intermediate Rounds (2 ≤ t < r):**
1. Observe current stock level and count of opponents who cooperated in round t−1
2. Calculate stock health: `h = stock / capacity`
3. Calculate observed cooperation rate: `opp_coop = (cooperators in round t−1) / (n−1)`

   ```
   if h ≥ 0.65:
       Cooperate
   else if h ≥ 0.40:
       if opp_coop ≥ 0.5:
           Cooperate
       else:
           Cooperate (give benefit of doubt)
   else:  // stock is depleted (h < 0.40)
       if opp_coop ≥ 0.6 and h ≥ 0.25:
           Cooperate (attempt collective recovery)
       else:
           Defect (resource in collapse; minimize waste by taking larger share)
   ```

**Final Round (t = r):**
Always cooperate. The final round is where benevolence is most visible—by refusing to defect even with no future consequences, you signal that cooperation isn't purely conditional reciprocity.

## Edge Cases

**Stock approaching zero:** Once stock drops below 0.25× capacity, switch to defection if cooperation rate among opponents is low. A benevolent player should not throw value away by taking stock/(2n) from a nearly empty pool while others defect. Taking stock/n at least captures remaining value with equal extraction rate.

**All opponents cooperate:** Continue cooperating in all rounds, since collective payoffs are maximized and the resource remains stable.

**All opponents defect immediately:** After round 1, observe zero cooperators. Defect from round 2 onward unless stock recovers above 0.40×capacity while maintaining minimum sustainability. This prevents prolonged futile cooperation as the pool collapses.

**Stock stabilizes:** If stock plateaus near capacity due to matching cooperative behavior, remain locked in cooperation (payoff-maximizing and sustainable).

## Benevolence Alignment

This strategy embodies benevolence through:
- **Stewardship:** Prioritizes resource preservation by cooperating when stock health is good, preventing tragedy of the commons
- **Reciprocal fairness:** Respects others' choices (reduces cooperation only when stock genuinely threatened by collective overexploitation, not as punishment)
- **Forgiveness:** Maintains high cooperation thresholds (0.65×capacity) so that occasional defectors don't trigger retaliation spirals
- **Terminal cooperation:** Final-round cooperation breaks the defection incentive, signaling unconditional benevolence
- **Proportional response:** Defects only as damage control when collapse is imminent, not as exploitative greed
'''

description_BENEVOLENT_9 = '''
# Benevolent Conditional Cooperation with Stock Stewardship

## Decision Rule

**Round 1:**
Cooperate. (Benevolent opening assumption about opponent rationality and good faith.)

**Rounds 2 through r-1:**
- Calculate *cooperation_rate* = (number of opponents who cooperated last round) / (n-1)
- Calculate *stock_health* = stock / capacity

Cooperate if ANY of these conditions hold:
1. stock_health ≥ 0.6 (stock is healthy; sustain the resource)
2. cooperation_rate ≥ 0.6 AND stock_health ≥ 0.3 (most others cooperate and stock is not critically low)
3. cooperation_rate ≥ 0.75 (sufficient others cooperate regardless of stock level)

Otherwise, defect.

**Final Round r:**
- Use same calculations but with relaxed thresholds to encourage final cooperation:

Cooperate if ANY of these conditions hold:
1. stock_health ≥ 0.5 (prioritize sustainability even at the end)
2. cooperation_rate ≥ 0.5 AND stock_health ≥ 0.25 (reciprocate final-round cooperation attempts)

Otherwise, defect.

## Edge Cases

**Stock collapse (stock ≈ 0):**
Defect. Game is functionally over; sustaining the resource is impossible.

**Perfect defection from all opponents (cooperation_rate = 0) for two consecutive rounds:**
Continue defecting to protect payoff. Benevolence does not require self-harm via persistent unilateral cooperation against universal defection.

**Late-game recovery (stock climbs unexpectedly high in final rounds despite prior defections):**
Revert to cooperation if stock_health ≥ 0.6. The resource is restored; reciprocate by helping maintain it.

## Benevolent Alignment

**Stock stewardship:** Prioritizes resource sustainability above immediate individual gain. The thresholds are designed to keep stock in the growth zone (not fully depleted, not saturated) where the logistic growth term remains productive.

**Reciprocal fairness:** Conditions tie cooperation directly to observed cooperation rates, rewarding mutual cooperation and punishing universal defection without requiring unilateral sacrifice.

**Forgiving adaptation:** Does not use grudge-holding; each round re-evaluates based on current conditions and fresh observation. An opponent can return to cooperation and be matched.

**Collective welfare:** The stock_health thresholds embed a welfare principle—cooperation is sustained as long as the common resource permits, protecting all players' long-term payoffs over short-term exploitation.
'''

description_BENEVOLENT_10 = '''
# Benevolent Adaptive Stewardship Strategy

**Core Decision Rule:**

Cooperate if the common pool stock is sufficiently healthy relative to consumption pressure. Shift toward defection only when the resource is being depleted and cooperation is not reciprocated by others.

**State Monitoring:**
- Track the stock level at the start of each round: S_t
- Track observed cooperation rate from previous round: c_t (number of cooperators divided by n)
- Compute health metric: h_t = S_t / capacity

**Decision Algorithm:**

```
IF round == 1:
    COOPERATE
    (signal benevolent intent; establish trust)

ELSE:
    COMPUTE cooperation_threshold based on stock health:
    
    IF h_t ≥ 0.75:
        required_cooperation_rate = 0.3
        (resource is robust; tolerate some defection)
        
    ELSE IF h_t ≥ 0.50:
        required_cooperation_rate = 0.5
        (resource is stable; expect reciprocal cooperation)
        
    ELSE IF h_t ≥ 0.25:
        required_cooperation_rate = 0.7
        (resource is degrading; need stronger cooperation)
        
    ELSE:
        required_cooperation_rate = 0.9
        (resource is critical; cooperate unless near total collapse)
    
    IF h_t < 0.10:
        DEFECT
        (resource at critical risk; prioritize immediate survival)
    
    ELSE IF c_{t-1} ≥ required_cooperation_rate:
        COOPERATE
        (others are meeting reciprocal threshold; sustain cooperation)
    
    ELSE:
        DEFECT
        (others are not reciprocating sufficiently relative to resource needs)
        
    SPECIAL CASE - Final round (t == r):
        IF h_t ≥ 0.30:
            COOPERATE
        (even on last round, don't accelerate collapse of shared resource)
```

**Edge Cases:**

- **First round:** Always cooperate regardless of parameters. This demonstrates benevolent intent and establishes a cooperative norm.

- **Stock collapse (h_t < 0.10):** Defect to secure immediate payoff. Once the resource is nearly destroyed, cooperation becomes meaningless.

- **Last round:** Cooperate if stock is still above 30% of capacity. Benevolence extends to leaving the resource in better condition than necessary for immediate gain, signaling concern for post-game welfare.

- **All others defected (c_{t-1} = 0):** After allowing one round of low cooperation, continue defecting until c_{t-1} ≥ 0.25. This protects against systematic exploitation while remaining open to recovery.

- **Unanimous cooperation (c_{t-1} = 1.0):** Maintain cooperation indefinitely. This locks in the stable equilibrium where stock stays at capacity.

**Benevolence Alignment:**

This strategy embodies benevolence through: (1) initiation of cooperation to enable mutual benefit; (2) conditional reciprocity that rewards others' restraint; (3) resource preservation as the primary objective, not personal maximization; (4) graceful degradation—defection only occurs when necessary to prevent exploitation or when the resource is already lost; (5) refusal to accelerate depletion in final rounds, preserving value beyond immediate game termination.
'''

description_BENEVOLENT_11 = '''
# Benevolent Sustainable Cooperation Strategy

## Core Principle
Cooperate to maintain the common resource for collective benefit while gracefully accepting reasonable exploitation. Prioritize resource sustainability and equitable outcomes over individual gain extraction.

## Decision Rule: Cooperate vs Defect

**Play Cooperate if and only if:**

```
stock > stock_threshold 
OR 
round == r (final round)
```

Where `stock_threshold = max(capacity/3, 2n)`

**Otherwise: Play Defect**

## Round-Specific Behavior

**Round 1 (Initialization):**
- Cooperate unconditionally
- Establish willingness to contribute fairly
- Initialize with stock = capacity, so threshold is satisfied

**Rounds 2 to r-1 (Mid-game):**
- Apply the threshold rule above
- Track observed_defections (count of opponents who defected each round)
- If observed_defections ≥ (n-1) for 2+ consecutive rounds AND stock < capacity/2: Defect once as a sustainability signal, then revert to threshold rule
- The single defection acts as a "wake-up call" without sustained retaliation

**Round r (Final Round):**
- Cooperate regardless of stock level, history, or opponent behavior
- Benevolent closure: leave the game without exploiting the final opportunity
- Reinforces that cooperation is intrinsically valued, not conditional

## Edge Cases

**Stock Collapse Threshold (stock ≤ 2n):**
- If stock has already crashed near minimum after heavy defection in previous rounds, Defect only if stock > 0 (grab remaining). This minimizes contribution to an already-failed commons.
- However, if stock is still recovering toward threshold, Cooperate to allow regeneration.

**Extreme Defection Observed (n-1 players defected last round):**
- Do not retaliate with sustained defection
- Stay in Cooperate mode if stock > threshold
- If stock < threshold, accept it and Defect only as a one-time signal
- Return to normal threshold rule next round

**Information Edge Case:**
- First observation arrives after round 1
- Use observed data from round t-1 to inform round t decision
- Threshold rule remains dominant; defection counts inform only the "wake-up call" mechanism

## Benevolent Framing

- **Fair sharing**: Cooperate at S/(2n) rather than claiming S/n
- **Resource stewardship**: Maintain stock above sustainability threshold rather than maximize individual rounds
- **No escalation**: Single-signal defections instead of tit-for-tat punishment spirals
- **Graceful exit**: Cooperate in final round even if abandoned by others, signaling that cooperation is the right norm regardless of final-round payoff
'''

description_BENEVOLENT_12 = '''
**BENEVOLENT ADAPTIVE CONSERVATION STRATEGY**

**Primary Decision Rule:**

Cooperate if the stock health permits sustainable renewal; defect only when the resource faces critical depletion and others are not reciprocating conservation efforts.

```
IF round == 1:
    COOPERATE
    (Signal benevolent intent; establish cooperation as baseline)

ELSE:
    stock_ratio = current_stock / capacity
    observed_coop_rate = (cooperators_in_last_round) / (n - 1)
    
    IF stock_ratio > 0.55:
        COOPERATE
        (Resource is healthy and can sustain mutual cooperation)
    
    ELSE IF stock_ratio > 0.25:
        IF observed_coop_rate >= 0.4:
            COOPERATE
            (Sufficient others conserving; maintain collective sustainability)
        ELSE:
            DEFECT
            (Stock stressed and cooperation insufficient to reverse trend)
    
    ELSE:  // stock_ratio ≤ 0.25 (critical depletion)
        IF rounds_remaining == 1:
            DEFECT
            (Last round: resource already compromised)
        ELSE IF observed_coop_rate > 0.5:
            COOPERATE
            (Strong reciprocal effort despite crisis; reward and rejoin)
        ELSE:
            DEFECT
            (Resource collapse imminent; others defecting; protect remaining position)
```

**Edge Cases:**

- **Rounds 1–2**: Bias toward cooperation to overcome initial uncertainty and demonstrate trustworthiness.
- **Final round** (round r): If stock is still above 30% of capacity and cooperation rate was historically ≥ 0.3, cooperate to leave a legacy. Otherwise defect only if stock is already critically low.
- **Stock at capacity**: Always cooperate; no scarcity pressure.
- **Stock oscillating near optimal** (40–60% of capacity): Cooperate unconditionally; this is the sweet spot for growth.

**Benevolent Orientation:**

This strategy prioritizes the long-term health of the common pool over individual short-term gain. It sustains cooperation when feasible, defects only when necessary to signal that free-riding is unsustainable, and rewards observed reciprocity even under resource stress. It avoids mutual defection spirals by conditioning on both resource state and peer behavior—defection is punishment for the system, not the player.
'''

description_BENEVOLENT_13 = '''
# Benevolent Sustainability Cooperation

## Decision Rules

**For all rounds except the final round:**

1. **Stock health check**: If `stock_at_round_start ≥ capacity/2`, proceed to step 2. Otherwise, evaluate cooperation.

2. **Cooperation threshold evaluation**: Observe how many opponents cooperated in the previous round, call this `observed_cooperators` (out of n-1 opponents).
   - If `observed_cooperators ≥ ceil((n-1)/2)`: **Cooperate** (majority signal indicates sustainable cooperation norm)
   - If `observed_cooperators < ceil((n-1)/2)`: **Defect** (protect commons from depletion spiral)

3. **High-stock override**: If `stock_at_round_start ≥ 0.75 × capacity` at any point in rounds 1 to r-1, **Cooperate** unconditionally (pool has abundant capacity to sustain high consumption without collapse risk).

**For the final round (round r):**
Always **Cooperate**, regardless of stock level or opponent behavior. This is a benevolent commitment signal—exit gracefully and signal that the commons matters more than squeezing final payoff.

## Edge Cases

- **Round 1**: Cooperate (benevolent initialization; no history exists, so assume best intent).
- **When stock falls below capacity/4**: Shift to defection against low-cooperation opponents to actively prevent pool extinction. If `observed_cooperators < ceil((n-1)/2)` and stock is critically depleted, defection is the only way to signal urgency and reduce destructive total consumption.
- **Ties in cooperation count** (exactly half opposing players cooperated): Cooperate. Ties are interpreted favorably under benevolence.
- **No history yet** (first round after round 1 hasn't executed): Treat `observed_cooperators` as `n-1` (assume universal cooperation until proven otherwise).

## Benevolent Alignment

This strategy embodies benevolence through:

1. **Generous initiation**: Starts with cooperation and maintains it when stock is abundant, showing faith in collective restraint.
2. **Conditional tolerance**: Accepts moderate defection (less than half) and responds with cooperation, not immediate retaliation.
3. **Commons protection**: Defects only when necessary to prevent systemic collapse, never as first-mover punishment.
4. **Graceful exit**: Unconditional final-round cooperation demonstrates that individual payoff maximization is secondary to leaving the commons in good condition.
5. **Transparency through restraint**: Cooperation rate signaling invites others into a sustainable equilibrium without aggression.

The strategy prioritizes collective long-term welfare over relative gain, accepting vulnerability when the stock is healthy while protecting shared resources when they are fragile.
'''

description_BENEVOLENT_14 = '''
# BENEVOLENT ADAPTIVE STOCK STEWARDSHIP STRATEGY

**Core Decision Rule:**

Play C (cooperate) if and only if:
```
stock/capacity ≥ 0.25  OR  round_number ≤ 2  OR  cooperation_rate_prev ≥ 0.4
```

Otherwise play D (defect).

Where:
- `cooperation_rate_prev` = (number of opponents who played C in previous round) / (n - 1)
- In the first round, play C unconditionally
- In the last round, always play C

**Detailed Decision Logic:**

*Round 1:*
Play C. Establish cooperative intent.

*Rounds 2 to r-1:*
After observing opponent cooperation counts from the prior round:

1. **Calculate stock health**: stock_ratio = stock / capacity

2. **Evaluate cooperation environment**: coop_rate = (count of C-players observed) / (n-1)

3. **Apply decision rule**:
   - If stock_ratio ≥ 0.25: Play C (resource is adequately stocked; cooperation sustainable)
   - Else if stock_ratio < 0.25 AND coop_rate ≥ 0.4: Play C (resource depleted but others are cooperating; join rebuilding effort)
   - Else if stock_ratio < 0.25 AND coop_rate < 0.4: Play D (tragedy imminent and others aren't helping; minimal mitigation)

*Round r (final round):*
Always play C. Benevolence does not end strategically; reinforce cooperation through example.

**Edge Cases:**

- If stock reaches 0 before round r: Continue playing C. The resource is already lost; defection adds no value and signals that collapse doesn't justify abandonment of principle.

- If stock jumps to capacity: Play C. No resource scarcity justifies defection.

- Uncertainty about opponent counts: Use observed counts only; assume unobserved players follow mixed strategies averaging to the observed rate.

**Benevolent Alignment:**

This strategy prioritizes resource sustainability and collective welfare over individual payoff maximization. It leads with cooperation, reciprocates genuine group cooperation, avoids punitive defection, and maintains principled cooperation even in final rounds when exploitation is tempting. It only defects when the commons is already collapsing and cooperation rates reveal systemic failure—a last-resort measure to minimize personal waste of a doomed resource.
'''

description_BENEVOLENT_15 = '''
# Sustainable Cooperation with Dynamic Adjustment

**Decision Rule:**

Cooperate if and only if the following condition holds; otherwise defect:

```
if round == 1:
    return COOPERATE
    
stock_health_ratio = stock / capacity

if stock_health_ratio < 0.30:
    return COOPERATE  // Critical: recover the pool at all costs

if stock_health_ratio < 0.60:
    // At-risk zone: cooperate if sufficient opponent cooperation
    observed_cooperation_rate = opponents_who_cooperated_last_round / (n - 1)
    if observed_cooperation_rate >= 0.50:
        return COOPERATE
    else:
        // Defect only if meaningful hope of recovery is lost
        return DEFECT

// Healthy zone (stock_health_ratio >= 0.60)
observed_cooperation_rate = opponents_who_cooperated_last_round / (n - 1)
rounds_remaining = r - current_round

if rounds_remaining <= 2:
    // End-game: secure sustainability over terminal extraction
    return COOPERATE

// Mid-game with healthy stock
if observed_cooperation_rate >= 0.65:
    return COOPERATE
else if observed_cooperation_rate >= 0.40:
    return COOPERATE  // Still benevolent; give benefit of doubt
else:
    // Widespread defection despite healthy stock: marginal defection
    return DEFECT
```

**Edge Cases:**

- **Round 1**: Always cooperate unconditionally. This broadcasts willingness to contribute and establishes the possibility of mutual sustainability.

- **Stock collapse threshold**: If stock ≤ 0.01 (near zero), defect is irrelevant—there is nothing to consume. The game outcome is already determined.

- **Observation baseline**: If no history exists (beginning), treat prior cooperation rate as 0.5 (neutral assumption).

- **Last round**: Shift to unconditional cooperation regardless of stock health or opponent behavior. Extracting maximally in the final round merely denies others without future consequence and contradicts benevolence.

- **Sparse defection tolerance**: When stock is healthy (>0.60 capacity), tolerate up to 35% defection from opponents before reciprocating. This reflects benevolent patience rather than hair-trigger punishment.

**Benevolent Alignment:**

This strategy prioritizes pool survival and collective long-term welfare over individual short-term payoff. It signals trustworthiness in early rounds, sacrifices immediate gains when the pool is stressed, and avoids terminal extraction dynamics. It does not punish strategically—it responds to environmental stress (stock depletion) rather than opponent defection per se. When the pool is endangered, cooperation is maintained even if opponents have defected, because the benevolent actor internalizes shared responsibility for collective recovery.
'''

description_BENEVOLENT_16 = '''
# Benevolent Adaptive Pool Stewardship Strategy

## Decision Rule by Round Type

**Round 1 (First Round):**
Cooperate unconditionally. Establish reciprocal intent and assume all players begin in good faith.

**Rounds 2 to r-1 (Intermediate Rounds):**
Use a stock-health-responsive decision framework:

```
if current_stock ≥ 0.6 × capacity:
    COOPERATE
    (System is healthy; sustain the resource base)
    
else if current_stock ≥ 0.25 × capacity:
    Calculate opponent_coop_rate = (number of opponents who cooperated last round) / (n-1)
    
    if opponent_coop_rate ≥ 0.5:
        COOPERATE
        (Majority reciprocated; maintain collaborative trajectory)
    else:
        DEFECT
        (Signal that unilateral cooperation erodes the system; encourage correction)
        
else (current_stock < 0.25 × capacity):
    DEFECT
    (Resource collapse imminent; salvage remaining value before depletion)
```

**Round r (Final Round):**
Cooperate unconditionally. Demonstrate that cooperation retains value even without future interaction, and act according to benevolent principles regardless of short-term advantage.

## Benevolence Alignment

- **Resource Stewardship**: Prioritize stock preservation above personal extraction when stock is abundant. Cooperation at capacity level yields sustainable 12.5 per round indefinitely, vastly outperforming the one-time 25-unit defection payoff.

- **Generous Initiation**: Lead with cooperation to encourage a cooperative equilibrium and signal trustworthiness.

- **Rational Adjustment**: Switch to defection not from greed, but as a visible warning when the collective is self-destructing through excessive defection. This teaches accountability.

- **Terminal Generosity**: Cooperate in the final round to reinforce that cooperation has intrinsic value and to leave the system in the healthiest state possible for others.

- **No Punishment Spiral**: Never defect based solely on past defections—only on current system health and recent reciprocation. This prevents cycles of retaliation that accelerate collapse.
'''

description_BENEVOLENT_17 = '''
# Benevolent Resource Steward

**Core Philosophy:**
Cooperate by default to sustain the shared resource. Accept moderate exploitation. Only defect defensively if the resource is collapsing or defection becomes nearly universal, prioritizing long-term collective welfare over short-term individual gain.

## Decision Rules

**Round 1:**
Cooperate unconditionally. Establish cooperative intent regardless of prior uncertainty about opponents.

**Rounds 2 to r-1 (Mid-game):**

```
defection_rate = (count of opponents who defected last round) / (n - 1)

if stock < capacity/3:
    action = Cooperate
    
else if defection_rate > 0.8 and stock > capacity/2:
    action = Defect
    
else if defection_rate > 0.5 and stock > capacity/1.5:
    action = Cooperate  // Accept moderate exploitation
    
else:
    action = Cooperate  // Default benevolence
```

**Round r (Final Round):**
Cooperate unconditionally. Benevolence means not defecting opportunistically at the end, even when others may. This refusal to exploit final-round vulnerability is a clear signal of genuine benevolence rather than strategic cooperation.

## Edge Cases

**Stock Depletion Path:** If stock ever falls below capacity/3, move into resource-protection mode. Cooperate until stock recovers above capacity/2, then resume the above logic. Benevolence includes preventing collective catastrophe.

**Near-Unanimity Defection:** If defection_rate > 0.8 while stock remains healthy, defect sparingly (one or two rounds) to avoid being systematically exploited, then return to cooperation. This is defensive resilience, not retaliation.

**Oscillating Opponents:** If defection rate fluctuates, treat the moving average over the last 2-3 rounds rather than single-round reactions. Benevolent strategies should not whipsaw.

## Benevolent Alignment

- **Sacrifice tolerance:** Explicitly accepts earning less than available when others defect, within sustainable bounds.
- **Collective stewardship:** Resource stock takes precedence over individual payoff maximization.
- **Non-punitive:** Defection (when it occurs) is defensive resource protection, never retaliatory.
- **Unconditional endgame:** Cooperating in the final round when mutual defection would be individually optimal demonstrates genuine benevolence rather than contingent reciprocity.
'''

description_BENEVOLENT_18 = '''
**BENEVOLENT ADAPTIVE STRATEGY**

**Decision Rule:**

Round 1: Cooperate unconditionally. (Benevolent opening signal)

Round t ∈ {2, ..., r}:
- Let `coop_count_prev` = number of opponents observed cooperating in round t-1
- Let `coop_rate_prev` = coop_count_prev / (n - 1)
- Let `stock_health` = stock / capacity

Decision cascade:

1. **Critical depletion check**: If stock < 0.25 × capacity, play Defect. (Resource emergency)

2. **Opponent cooperation assessment**: 
   - If coop_rate_prev ≥ 0.5: Opponent cooperation is strong
   - If 0.3 ≤ coop_rate_prev < 0.5: Opponent cooperation is moderate
   - If coop_rate_prev < 0.3: Opponent cooperation is weak

3. **Adaptive response**:
   ```
   if stock_health < 0.4:
       if coop_rate_prev >= 0.5:
           action = C (support cooperators during stress)
       else:
           action = D (resource endangered by low cooperation)
   else if stock_health >= 0.4:
       if coop_rate_prev >= 0.3:
           action = C (sustain and reciprocate)
       else if stock_health >= 0.6 AND rounds_remaining <= 3:
           action = C (final push for sustainability)
       else:
           action = D (defensive against widespread defection)
   ```

4. **No endgame defection**: Do not deviate strategy in the final round based solely on it being the final round. Maintain commitment to long-term sustainability of the resource.

**Rationale for benevolence:**

- **Opening cooperation** demonstrates trustworthiness and preference for mutual sustainability.
- **Threshold 0.3 for moderate cooperation** is forgiving and assumes others may need time to learn or coordinate.
- **Stock-based emergency thresholds** ensure the commons survives rather than racing to extract before collapse.
- **No endgame opportunism**: Refuse the temptation to defect in round r, treating the resource as if it will persist beyond the game boundary.
- **Reciprocal escalation** rather than punishment: respond to weak cooperation with caution rather than aggressive defection.
'''

description_BENEVOLENT_19 = '''
## BENEVOLENT ADAPTIVE COOPERATION STRATEGY

**Core Principle:** Cooperate to sustain the common pool, transitioning only when the system collapses or free-riding becomes endemic and damage is inevitable.

### DECISION RULE (Each Round t ∈ {1, 2, ..., r})

1. **Calculate stock health:**
   - stock_ratio = current_stock / capacity
   - cooperation_rate = (number of opponents who played C in round t-1) / (n-1)
     - If round 1, set cooperation_rate = 1.0 (assume good faith)

2. **Primary rule:**
   ```
   If stock_ratio ≥ 0.5:
       Play C (resource is robust)
   Else if stock_ratio < 0.1:
       Play C (pool is doomed; defection adds negligible value)
   Else if stock_ratio ∈ [0.1, 0.5):
       If cooperation_rate ≥ 0.5:
           Play C (collective effort is slowing decline)
       Else:
           Play D (too much defection; protect personal extraction)
   ```

3. **Last-round exception (t = r):**
   - If stock_ratio ≥ 0.3: Play C (sustain benevolence to the end; don't exploit)
   - If stock_ratio < 0.3: Play D (extract final value if collapse is certain)

### EDGE CASES

- **Round 1:** Play C unconditionally. Signal benevolent intent and establish a cooperative anchor.

- **All opponents defect for consecutive rounds:** Continue playing C as long as stock_ratio ≥ 0.5. Once stock_ratio falls below 0.1, defection is pointless, so remain at C to at least minimize harm.

- **Stock reaches exactly 0:** Continue playing C (consumption is zero anyway; this prevents future disruption if the game rules update).

- **Mixed defection (e.g., 3 of 10 opponents cooperate):** Use cooperation_rate threshold of 50%. Below that, switch to D only if stock is actively declining into the danger zone [0.1, 0.5). This avoids hair-trigger responses to minor free-riding.

### BENEVOLENT ALIGNMENT

- **Prioritizes long-term collective surplus** by maintaining stock above the growth threshold (stock_ratio ≥ 0.5) whenever opponents allow it.
- **Does not exploit cooperators.** Defection only triggers when the system is already failing (high defection rate + degraded stock), not as a preemptive exploitation strategy.
- **Accepts lower personal payoffs** in early and middle rounds to preserve the resource and encourage reciprocal cooperation.
- **Avoids spite.** Never retaliates against single opponents; only responds to aggregate system failure.
- **Graceful degradation:** If cooperation collapses, transitions to D to minimize personal loss without accelerating the death spiral further.
'''

description_BENEVOLENT_20 = '''
# Benevolent Sustainable Resource Strategy

## Decision Rules

**Round 1:**
Cooperate unconditionally. This establishes benevolent intent and tests whether the resource is sustainable.

**Rounds 2 through r-1 (Middle Rounds):**

Compute:
- `opponent_coop_rate` = (number of opponents observed cooperating in previous round) / (n - 1)
- `stock_health` = current stock / capacity

Decision:
```
if stock_health ≥ 0.50:
  action ← C
  // Stock is healthy; maintain full cooperation to sustain indefinitely

else if stock_health ∈ [0.20, 0.50):
  if opponent_coop_rate ≥ 0.40:
    action ← C
    // Reciprocate adequate cooperation effort
  else:
    action ← D
    // Single defection reduces consumption pressure without triggering collapse spiral

else if stock_health < 0.20:
  action ← C
  // Stock is endangered; maximize growth potential (growth peaks near zero stock)
  // Benevolence means prioritizing resource recovery over personal extraction
```

**Final Round (Round r):**
Cooperate unconditionally. This prevents end-game defection spirals and demonstrates commitment to sustainability beyond any retaliatory horizon.

## Edge Cases

- **Stock collapse (stock = 0):** Action is C (payoff is zero regardless, but consistency preserves signal).
- **All opponents defected previously:** At stock_health < 0.20, still cooperate to attempt recovery. At stock_health ∈ [0.20, 0.50), defect once to brake consumption while leaving room for restoration.
- **Perfect opponent cooperation:** Maintain C throughout (no reason to deviate).
- **Very small n (n = 2):** Logic unchanged; opponent_coop_rate becomes binary (0 or 1), triggering threshold cleanly.

## Benevolent Alignment

This strategy embeds three benevolent commitments:

1. **Resource preservation over exploitation:** Defection only occurs at moderate stock levels as a light brake, never at critical levels. The strategy prioritizes collective resource survival.

2. **Reciprocity without punishment:** Responses to low opponent cooperation are measured (single D), not retaliatory (sustained D). When stock is endangered, benevolence overrides reciprocal defection.

3. **Resistance to end-game collapse:** Final-round cooperation prevents the mutual defection death spiral common in finitely repeated games, maintaining resource integrity until the game ends.
'''

description_BENEVOLENT_21 = '''
**Benevolent Adaptive Pool Preservation Strategy**

**Core Principle:**
Prioritize collective pool health over individual consumption. Cooperate by default, defect only when (a) the pool is mathematically doomed, or (b) defection is necessary to prevent the pool's collapse through others' extraction.

**Decision Rules:**

**Round 1:**
Cooperate unconditionally. Signal benevolent commitment and assume reciprocal good faith.

**Rounds 2 to r-1:**
Define a sustainability threshold: `critical_stock = capacity × 0.5`

1. Observe the cooperation count from the previous round: `c = number of opponents who played C`
2. Check current stock level against threshold:
   - **If stock ≥ critical_stock:** Cooperate
     (Pool is healthy; maintain cooperation)
   - **If stock < critical_stock:**
     - **If c ≥ ⌈(n-1)/2⌉** (majority cooperated): Cooperate
       (Reciprocate the majority's effort to save the pool; act as a coalition member)
     - **Else:** Defect
       (Defection is now inevitable; extract what remains since the pool will collapse anyway)

**Round r (final round):**
- **If stock ≥ critical_stock:** Cooperate
  (Benevolent endgame; no future consequences; maintain principles)
- **If stock < critical_stock:** Defect
  (Pool is already compromised; maximize final payoff)

**Edge Cases:**

- **Stock approaches zero:** If stock < capacity × 0.1, defect unconditionally; the pool cannot recover and cooperation yields negligible payoffs.
- **Defection triggers a cascade:** If defectors cause stock to fall below critical_stock, immediately switch to defection mode in the next round (Rule 2b activates). This prevents indefinite cooperation while being exploited.
- **Pool recovers:** If stock rises back above critical_stock after a low period, resume cooperation (shows adaptability and benevolence).

**Benevolence Alignment:**

This strategy embodies benevolence by:
- Defaulting to the Pareto-dominant cooperative outcome
- Trusting and reciprocating others' cooperation
- Sacrificing individual extraction (S/n → S/2n) to preserve the shared resource
- Accepting lower payoffs in healthy rounds to enable long-term sustainability
- Only defecting when the collective outcome is already lost, not to exploit a fragile system
'''

description_BENEVOLENT_22 = '''
# Benevolent Adaptive Commons Stewardship Strategy

## Decision Rule

**Round 1 (Opening):**
Cooperate. Signal benevolent intent and establish sustainable equilibrium.

**Last Round (Round r):**
Defect. No future stock growth occurs after the final round, so the growth mechanism is irrelevant. Extract maximum immediate value.

**Stock Recovery Phase (stock < capacity/3):**
Cooperate. When the commons is depleted below critical threshold, prioritize restoration. Individual consumption gains are minimal; growth recovery is only possible through collective restraint. Benevolence means preventing tragedy rather than exploiting crisis.

**Rounds 2 through r-1 (Steady State):**

Let `coop_rate` = (observed opponents who cooperated last round) / (n - 1)

- **If coop_rate ≥ 0.6:** Cooperate. Mutual cooperation is stable; maintain it.

- **If 0.4 ≤ coop_rate < 0.6:** Cooperate with probability p = 0.5 + 0.25 × coop_rate. Proportionally match the population's cooperation tendency while retaining flexibility. At coop_rate = 0.4, cooperate 60% of the time; at coop_rate = 0.6, cooperate 85% of the time.

- **If 0.2 ≤ coop_rate < 0.4 and stock ≥ capacity/2:** Defect. Defection-dominant population; match their strategy while stock can absorb the impact.

- **If 0.2 ≤ coop_rate < 0.4 and stock < capacity/2:** Cooperate. Even if defection is rising, the commons is fragile. Benevolence means not accelerating collapse.

- **If coop_rate < 0.2:** Defect. Only if defection becomes nearly universal do we stop trying to maintain the commons through solo cooperation.

## Edge Cases

**Empty stock (stock = 0):** Automatic Cooperate in next round regardless of history. The commons is extinct; payoffs are zero. Only cooperation can rebuild from nothing, and attempts at defection are moot.

**Two-player game (n = 2):** Benevolence is heightened—your single opponent's behavior directly determines future stock. Apply the thresholds above but weight coop_rate decisions more heavily toward sustained cooperation, since one player's defection is catastrophic. Cooperate until coop_rate < 0.3.

**Very high stock (stock ≥ 0.95 × capacity):** If coop_rate ≥ 0.5, Cooperate to preserve equilibrium. If defection is rising despite abundance, Defect selectively (use the probabilistic rule) to impose cost before depletion cascades.

## Benevolence Alignment

- **Commons first:** Stock recovery and sustainability are prioritized over individual payoff maximization.
- **Conditional, not punitive:** Punishment (defection) is proportional and conditional on defection density and stock health, not permanent. Forgiveness is immediate if cooperation rates improve.
- **Temporal fairness:** Sacrificing the final round (automatic defection) is accepted to enable cooperation and growth in earlier rounds when it matters for collective welfare.
- **De-escalation:** Strategy retreats from defection as soon as cooperation signals are observed or stock needs rescue.
- **Mutual benefit:** Cooperate by default; only shift when evidence of systematic defection makes solo cooperation futile.
'''

description_BENEVOLENT_23 = '''
**DECISION RULE**

Cooperate if and only if ANY of the following conditions hold:

1. **Stock Recovery Threshold**: Current stock < 0.4 × capacity
   - Always cooperate when the resource is endangered, regardless of opponent behavior

2. **Cooperative Reciprocation**: Stock ≥ 0.4 × capacity AND (cooperators_last_round / (n-1)) ≥ 0.4
   - When stock is stable and opponents show meaningful cooperation, reciprocate with cooperation

3. **Forgiveness Cycle**: Stock ≥ 0.4 × capacity AND (round mod 3 == 0) AND (cooperators_last_round / (n-1)) < 0.7
   - Every third round, cooperate even if recent opponent cooperation is weak, giving others a chance to recover cooperative behavior

4. **Opening Move**: round == 1
   - Cooperate in round 1 to signal benevolent intent

Otherwise, defect.

**EDGE CASES**

- **First round (round = 1)**: Always cooperate
- **Last round (round = r)**: Apply the same decision rule. Do not defect solely for final-round exploitation
- **Stock = 0**: Technically play C (zero consumption either way, but signal intent for hypothetical future)
- **All opponents defected (cooperators_last_round = 0)**: Defect unless stock < 0.4 × capacity

**BENEVOLENT ALIGNMENT**

- **Stock stewardship**: The recovery threshold prioritizes collective long-term sustainability over short-term personal gain, even when it means forgoing immediate extraction
- **Reciprocal trust building**: Cooperation is conditional on opponent cooperation rate, not punitive—the 0.4 threshold gives benefit of doubt
- **Forgiveness mechanism**: The 3-round cycle ensures cycles of low cooperation don't lock in permanent defection; allows opponents to reset and rejoin cooperation
- **No exploitation**: Resists defecting on the final round purely to extract remaining stock, maintaining consistent benevolent principles
- **Transparency of intent**: Cooperating from round 1 signals honest commitment to mutual benefit, making coordination more likely
'''

description_BENEVOLENT_24 = '''
# Adaptive Benevolent Strategy

**Round 1:**
Always cooperate. This establishes benevolent intent without prior information.

**Rounds 2 through r-1 (middle rounds):**

Observe the current stock level and count how many opponents cooperated in the previous round. Compute:
- Stock ratio: S_ratio = stock / capacity
- Cooperation rate: coop_rate = (number of cooperating opponents) / (n - 1)

Cooperate if any of the following holds:
1. S_ratio ≥ 0.60 (stock is healthy; cooperation sustains regeneration)
2. S_ratio ≥ 0.35 AND coop_rate ≥ 0.50 (stock is adequate and others are mostly cooperating; reciprocate trust)
3. coop_rate ≥ 0.65 (overwhelming cooperation observed, reinforce with cooperation)

Defect if all of the following hold:
1. S_ratio < 0.35 (stock is critically depleted)
2. coop_rate < 0.50 (defection is widespread)
3. Rounds remaining ≤ 2 (final rounds where future state matters little)

Otherwise: Cooperate (benevolent default).

**Round r (final round):**

Cooperate if S_ratio > 0.25 (stock not on verge of collapse).

Defect only if S_ratio ≤ 0.25 (desperate salvage in final round with near-depleted resource).

**Rationale:**

This strategy prioritizes resource sustainability through cooperation when possible, but conditionally protects itself when the stock is critically low and opponents are defecting. The benevolent bias—defaulting to cooperation and requiring strict conditions to defect—ensures the strategy maintains cooperative norms even under adverse conditions. Responsiveness to both stock health and observed cooperation rates makes it adaptive across varying opponent behaviors without requiring individual tracking.
'''

description_BENEVOLENT_25 = '''
# Benevolent Adaptive Pool Strategy

## Decision Rule

**Cooperate** if and only if ALL of the following hold:
1. Current stock > 0.3 × capacity (stock is not critically depleted)
2. AND either:
   - Round t = 1 (initiate cooperation), OR
   - Defection rate among opponents in round t−1 is ≤ 0.5 AND round t ≤ 2r/3, OR
   - Defection rate among opponents in round t−1 is ≤ 0.33 AND round t > 2r/3

**Defect** in all other cases.

## Stock Health Monitoring

Track stock level between rounds:
- If stock falls below 0.3 × capacity, switch to defensive defection mode. This preserves the pool from total collapse while signaling that exploitation has consequences.
- Once stock recovers above 0.3 × capacity AND opponents reduce defections, resume cooperation.

## Early Game (t ∈ {1, ..., ⌊2r/3⌋})

- **Round 1**: Always cooperate (establish benevolent intent unconditionally)
- **Rounds 2 to ⌊2r/3⌋**: Forgive high defection rates once per game. If ≤50% of opponents defected, cooperate despite setback. This gives cooperation a fair chance to take root.
- Reset forgiveness after one instance; subsequent high defection triggers immediate defection.

## Late Game (t ∈ {⌊2r/3⌋ + 1, ..., r})

- Tighten the defection threshold to 0.33 (require ≥67% opponent cooperation to reciprocate)
- This protects against last-round exploitation while remaining benevolent if cooperation has prevailed
- **Final round**: If stock > 0.5 × capacity and opponent defection ≤ 0.33, still cooperate—maintain benevolent signal through game's end

## Edge Cases

- **Stock collapse (S = 0)**: Defect unconditionally. There is no pool to exploit.
- **Single remaining opponent**: Apply the same thresholds; observe their single action to infer defection rate (0% or 100%).
- **All opponents observed cooperating (0% defection)**: Always cooperate in next round if stock permits.
- **Tie-breaking in mid-game forgiveness**: On the forgiveness opportunity, give benefit of doubt—cooperate.
'''

description_BENEVOLENT_26 = '''
# BENEVOLENT POOL STEWARDSHIP STRATEGY

## Core Principle
Prioritize pool sustainability while remaining adaptive to others' defection. Signal cooperation early to establish the resource foundation, then maintain it unless the pool is already lost.

## Decision Rule

**For each round t:**

1. **Compute pool health:** health = stock / capacity

2. **Compute opponent cooperation rate:** coop_rate = (number of opponents who cooperated in round t−1) / (n−1)  
   (In round 1, set coop_rate = 1.0, assuming good faith)

3. **Apply adaptive rule:**

   ```
   IF round == 1:
       Action = COOPERATE
   
   ELSE IF health ≥ 0.4:
       IF coop_rate ≥ 0.4:
           Action = COOPERATE
       ELSE:
           Action = COOPERATE  (continue rebuilding despite defections)
   
   ELSE IF health < 0.4 AND health > 0:
       IF coop_rate ≥ 0.2:
           Action = COOPERATE  (sacrifice round to allow recovery)
       ELSE:
           Action = DEFECT  (majority defecting; pool already compromised)
   
   ELSE IF health == 0:
       Action = DEFECT  (pool extinct; no cooperative value remains)
   
   ELSE IF round == r (final round):
       IF health ≥ 0.3:
           Action = COOPERATE  (resist endgame exploitation)
       ELSE:
           Action = DEFECT  (pool doomed; don't compound harm)
   ```

## Justification for Benevolence

- **Initial cooperation** demonstrates trustworthiness and establishes the pool at sustainable equilibrium (capacity).
- **High cooperation tolerance** (coop_rate ≥ 0.4) reflects benevolent patience even when some opponents defect; prevents cycles of mutual punishment.
- **Sacrifice phase** (health < 0.4, coop_rate ≥ 0.2) shows willingness to consume less than available to allow stock recovery, signaling long-term commitment to collective welfare.
- **Defection trigger** (coop_rate < 0.2) is reached only when the majority have already abandoned cooperation, minimizing unilateral losses.
- **Resist endgame temptation** in final round if pool remains viable, avoiding the exploitation that would destroy the resource.

## Edge Cases

- **Round 1:** Always cooperate. No history; assume cooperation is the norm.
- **Pool depletion to zero:** Defect (resource destroyed; cooperation impossible).
- **Final round with healthy pool:** Cooperate despite one-shot incentive to defect.
- **Opponent anonymity:** Use aggregate cooperation counts only; do not attempt to punish specific players.
'''

description_BENEVOLENT_27 = '''
# Benevolent Adaptive Resource Steward Strategy

**DECISION RULE BY STOCK LEVEL:**

Maintain awareness of a critical threshold: `stock_ratio = current_stock / capacity`

**Case 1: Stock is Abundant (stock_ratio ≥ 0.60)**
- **Play C (Cooperate)**
- Rationale: Resource is healthy and can regenerate. Preserve the commons for sustained yields.

**Case 2: Stock is Moderate (0.35 ≤ stock_ratio < 0.60)**
- Observe the defection rate from the immediately previous round: `defection_rate = (# opponents who played D) / (n-1)`
- If `defection_rate ≤ 0.40`: **Play C**
  - Maintain cooperative norm; assume others are restrained
- If `defection_rate > 0.40`: **Play D**
  - Free-riding is too prevalent; only defect to avoid pure exploitation while others extract value

**Case 3: Stock is Depleted (stock_ratio < 0.35)**
- **Play C** (with one exception below)
- Rationale: Stock is fragile. Defection accelerates collapse without aiding recovery. Only cooperate can allow growth toward the generative zone (≈50% capacity).
- Exception: If this is NOT one of the final 2 rounds AND defection_rate from previous round > 0.50, play D to signal that unilateral cooperation is unsustainable.

**EDGE CASES:**

**First round:**
- Play **C** unconditionally. The resource begins at full capacity. Lead with cooperation to establish cooperative norm.

**Final round (round = r):**
- Play **C** unconditionally. Benevolence means prioritizing collective outcome over exploiting the absence of future consequences. Defecting in the last round breaks trust unnecessarily.

**Stock collapse scenario (stock ≤ 0):**
- If stock somehow reaches zero before round r, play **C** in all remaining rounds. The game is lost; cooperation at least prevents further degradation in principle.

**INTUITION FOR BENEVOLENCE:**

This strategy embeds:
- **Resource stewardship**: Cooperation is the default when resources permit it, protecting the commons.
- **Fairness**: Willingness to defect only when exploitation by others becomes severe, not as a first resort.
- **Sustainability**: Threshold logic avoids the defection cascade that collapses stocks into extinction.
- **Generosity at endpoints**: Cooperate in round 1 (build trust) and round r (end with integrity).
- **Robustness**: Adapts to observed free-riding while avoiding sucker payoffs through the moderate-zone threshold.
'''

description_BENEVOLENT_28 = '''
**BENEVOLENT ADAPTIVE STRATEGY**

**Core Decision Logic:**

Cooperate if any of the following holds:
1. This is round 1
2. This is round r (final round)
3. Current stock ≥ capacity/3
4. Observed cooperation rate ≥ 0.4

Otherwise defect.

Where observed cooperation rate = (number of cooperators in previous round) / (n-1).

**Detailed Rules:**

Round 1: Always cooperate. This establishes benevolent intent and prevents immediate resource collapse.

Rounds 2 to r-1:

Let coop_rate = cooperators_observed / (n-1)

IF stock ≥ capacity/3:
  → Cooperate. The resource is healthy enough to sustain mutual cooperation. Stay committed regardless of others' behavior.

ELSE IF stock < capacity/3 AND coop_rate ≥ 0.4:
  → Cooperate. Despite resource pressure, sufficient others are cooperating. Maintain cooperation to signal commitment and allow stock recovery through growth.

ELSE IF stock < capacity/3 AND coop_rate < 0.4:
  → Defect. The resource is depleted and others are predominantly free-riding. Defection minimizes individual loss and reduces total extraction pressure, allowing the logistic growth mechanism to recover the stock.

Round r (final round): Always cooperate. Reject the temptation to exploit in the terminal round. Benevolence means not extracting maximum value when it harms collective welfare.

**Rationale:**

This strategy sustains cooperation when cooperation is viable (healthy stock or active partners). It only switches to self-protective defection when the resource faces imminent collapse and others have largely abandoned cooperation—avoiding tragedy-of-the-commons scenarios without punishing partners. The cooperation threshold of 0.4 (meaning defect only when < 40% cooperate) biases strongly toward cooperation. The stock threshold of capacity/3 is conservative, allowing defection only under genuine resource stress. Final-round cooperation sacrifices individual gain for collective welfare, embodying benevolence.
'''

description_BENEVOLENT_29 = '''
# Adaptive Cooperation with Resource Stewardship

**First Round:**
Play C (Cooperate). Establish good faith and attempt to anchor a cooperative equilibrium.

**Rounds 2 through r:**

Observe the number of opponents who played C in the previous round. Calculate the cooperation rate among the n-1 other players.

```
cooperation_rate = (count of opponents playing C in round t-1) / (n-1)

IF current_stock ≥ 0.75 × capacity:
  Action = C
  
ELSE IF cooperation_rate ≥ 0.5:
  Action = C
  
ELSE IF cooperation_rate ≥ 0.25 AND current_stock > 0.4 × capacity:
  Action = C
  
ELSE:
  Action = D
```

**Decision Logic:**

- **Stock-abundant state** (≥75% capacity): Cooperate unconditionally. The resource is healthy and can sustain cooperation even if others sometimes defect.

- **Mixed cooperation scenario** (50%+ cooperators): Reciprocate cooperation. This encourages the cooperative players and signals that mutual cooperation is viable.

- **Low cooperation with healthy stock** (25-50% cooperators AND stock >40% capacity): Cooperate with patience. The resource can tolerate some defection, and persistent cooperation may win over moderate defectors over time.

- **Widespread defection or resource crisis** (<25% cooperation OR stock ≤40% capacity): Defect. Protect your own consumption when the resource is under severe stress or cooperation has broadly collapsed. This prevents personal ruin while the commons deteriorates.

**Final Round Handling:**
Apply the same decision rule as other rounds. Do not exploit strategically in round r. Benevolence means not pivoting to defection at the end to maximize last-round gains, even though it would be individually rational.

**Rationale:**
This strategy is benevolent because it prioritizes sustaining the common pool and cooperates unless cooperation has clearly failed. It adapts to opponent behavior through observable cooperation rates rather than punishing individual players. It forgives: defectors can return to the cooperative equilibrium if others around them cooperate, because the strategy measures group cooperation rates, not individual histories.
'''

description_BENEVOLENT_30 = '''
# Benevolent Conditional Cooperation Strategy

## Decision Rule

```
In round t, cooperate if and only if:
  (stock_health is HEALTHY) AND (opponent_cooperation is SUFFICIENT)
  OR (opponent_cooperation is VERY_STRONG)
```

Where:
- `stock_health is HEALTHY` := current_stock ≥ capacity/2
- `opponent_cooperation is SUFFICIENT` := empirical cooperation rate ≥ 50%
- `opponent_cooperation is VERY_STRONG` := empirical cooperation rate ≥ 75%

The empirical cooperation rate is: (number of opponents who cooperated in previous round) / (n-1)

## Edge Cases & Temporal Adjustments

**Round 1:** Unconditionally cooperate. Start with benevolent intent and gather baseline information about opponent behavior.

**Rounds 2 to ceil(r/3) [Early Game]:** Apply the decision rule, but lower the SUFFICIENT threshold to 40% (more cooperative bias when learning). Rationale: early rounds allow time for opponent strategies to stabilize, so be forgiving while building information.

**Rounds ceil(r/3)+1 to floor(2r/3) [Middle Game]:** Apply standard decision rule (50% threshold). This is the phase where you have good empirical estimates of opponent behavior.

**Rounds floor(2r/3)+1 to r [Late Game]:** 
- If stock ≤ capacity/4 (critical depletion): Defect to protect final-round earnings, as recovery is unlikely.
- Otherwise: Apply standard decision rule, but increase SUFFICIENT threshold to 60% to encourage last-round discipline.

## Critical Stock Protection

If stock ever falls below capacity/8, defect for that round regardless of opponent behavior. This is a hard floor preventing collapse-level depletion.

## Benevolence Alignment

This strategy embodies benevolence through:
- **Cooperation bias:** Defaults to cooperation in early and middle phases unless evidence strongly suggests defection is necessary
- **Forgiving:** Does not employ tit-for-tat punishment; a single opponent defection does not trigger retaliation
- **Redemptive:** Opponents who cooperate can recover reputation immediately in the next round; no memory of past defections beyond the current aggregated rate
- **Resource-conscious:** Defection occurs only when stock health indicates the resource cannot sustain cooperation, protecting the collective good
- **Sacrifice willingness:** Accepts payoff reduction (C gives S/2n per player vs D gives S/n) when resource sustainability is achievable
'''

description_BENEVOLENT_31 = '''
# Benevolent Adaptive Cooperation Strategy

## Decision Rule

**For round 1:** Cooperate unconditionally.

**For round t > 1:**
1. Let k = number of opponents observed to cooperate in round t−1
2. Calculate cooperation rate: p = k / (n − 1)
3. If p ≥ 0.4: Play Cooperate
4. If p < 0.4: Play Defect

## Rationale for Thresholds

The 0.4 threshold establishes a sustainable equilibrium band. With 40%+ of opponents cooperating, the common pool can typically regenerate even with moderate defection elsewhere. This allows the strategy to:

- **Maintain benevolence**: Cooperate generously even when some opponents defect, extending repeated opportunities for mutual benefit
- **Detect systematic exploitation**: Only switch to Defect when defection among opponents becomes dominant (>60%), signaling that cooperation-based sustainability has failed
- **Avoid mutual ruin**: Defect when necessary to avoid catastrophic collective depletion, but return to cooperation immediately if opponents improve

## Edge Cases

**First round:** Cooperate. Assume good faith absent evidence otherwise. Initialize the cooperative equilibrium.

**Final round (t = r):** Cooperate. Benevolence is not conditional on future reputation effects. The goal is to maximize total collective payoff, not to optimize individual positioning. Defecting in the final round provides only marginal personal gain (S/n vs S/2n) while directly harming group welfare.

**Critical stock depletion:** If stock falls below capacity/4 and average opponent cooperation rate is below 0.4, defect for self-preservation (accept the resource is doomed). This prevents purely altruistic behavior in clearly-failed environments.

**Unanimous cooperation (k = n−1):** Cooperate. This is the optimal collective outcome.

**Unanimous opponent defection (k = 0):** Defect. Match the market rate; cooperation provides no marginal benefit when pool is already failing.

## Benevolence Alignment

- **Accepts near-equal payoff with others** over exploiting defectors for marginal gain
- **Tolerates some defection** (40% threshold) rather than punishing immediately, preserving paths back to cooperation
- **Prioritizes group sustainability** over individual maximization
- **Transparent and reciprocal** rather than deceptive, supporting cooperative norms if others reciprocate
'''

description_BENEVOLENT_32 = '''
# Benevolent Adaptive Cooperation Strategy

## Decision Rule

**Round 1:** Always Cooperate.

**Round t (2 ≤ t ≤ r):** 
- Let `coop_count` = number of opponents who cooperated in round t-1
- If `coop_count ≥ ceil(n/2)` OR `stock < capacity/3`: Cooperate
- Else: Defect

**Last round (t = r):** Apply the same rule above; do not deviate to defection in the final round.

## Rationale

**Cooperation initiation:** Lead with cooperation in round 1 to signal trustworthiness and allow the discovery of cooperative partners.

**Majority-responsive threshold:** If at least half of opponents cooperated in the previous round, continue cooperating. This sustains collective benefit when a cooperative coalition is present, and matches the intuition that cooperation is self-reinforcing when widespread.

**Stock recovery clause:** If stock has fallen below capacity/3, cooperate regardless of opponent behavior. When the resource is severely depleted, defection accelerates collapse via total consumption. Cooperation gives the stock the best chance to regenerate via the logistic growth curve, which benefits everyone including yourself in future rounds. This is the core of benevolence: prioritizing collective recovery over individual short-term gain.

**No end-game defection:** Avoid the temptation to exploit in the final round. A benevolent agent maintains its commitment to sustainability and cooperation even when future-round punishment is impossible. This reinforces long-term trustworthiness norms and prevents catastrophic last-round depletion.

## Edge Cases

- **If all opponents defect every round:** Defect starting in round 2, but immediately return to cooperation if stock drops below capacity/3.
- **If stock reaches 0 before round r:** Continue cooperating; the pool cannot recover without restraint.
- **If n = 2:** The threshold `ceil(n/2) = 1`, so cooperate if the single opponent cooperated or if stock is low.
'''

description_SELFISH_5 = '''
**Stock-Responsive Selfish Strategy**

**Decision Rule by Round Type:**

*Final Round (t = r):*
Always Defect. No future rounds to protect, so capture maximum immediate value.

*Non-Final Rounds (t < r):*
Let k = number of opponents observed cooperating last round (0 ≤ k ≤ n-1)

- **If stock ≤ 0.15 × capacity:** Play C
  - Stock has fallen critically low. Continued defection by most players triggers collapse to 0, yielding nothing. Cooperating preserves the resource for future extraction.

- **Else if k ≥ 0.5 × (n-1):** Play D
  - Majority of opponents are cooperating. They maintain stock while I extract at the higher defection rate. This is pure exploitation.

- **Else if (r - t) ≤ 2:** Play D
  - Few rounds remain. Prioritize immediate payoff over resource maintenance. Endgame aggression.

- **Else:** Play C
  - Stock is healthy, cooperation is low, and multiple rounds remain. Cooperating is the selfish choice because: (1) continued mutual defection collapses the resource to 0, giving me nothing; (2) if I'm cooperating and others defect, I at least stabilize stock for later rounds; (3) I preserve optionality to exploit if cooperation emerges.

**First Round Initialization:**
Defect. High stock means defection is safe and reveals opponent tendencies.

**Edge Cases:**
- If stock reaches 0, all subsequent actions yield 0 regardless—the game is already lost.
- If all observed opponents defected (k=0) in multiple consecutive rounds and stock remains above threshold, continue cooperating to avoid collapse while others still might defect—I extract value by being the sole stabilizer.
- The 0.15 threshold is set conservatively to ensure stock recovery is mathematically possible before endgame compression.
'''

description_SELFISH_6 = '''
# SELFISH ADAPTIVE STRATEGY

**DECISION RULE — COOPERATE if and only if all of the following hold:**
1. Rounds remaining ≥ 2 (never cooperate in the final round)
2. Current stock ≥ 0.4 × capacity
3. Observed cooperation rate from prior round ≥ 0.50

**Otherwise, DEFECT.**

---

## ROUND 1 SPECIAL CASE
In round 1, you have no prior observation. Assume all (n-1) opponents will cooperate. Since stock equals capacity (which exceeds 0.4 × capacity), COOPERATE in round 1.

---

## OPERATIVE LOGIC

**The core selfishness**: You defect whenever possible to double your immediate payoff. You only cooperate as a strategic constraint to prevent resource collapse, because a collapsed commons benefits no one.

**Cooperation condition**: You maintain cooperation if you observe that a majority of others are cooperating AND the stock is robust enough to sustain repeated extraction at cooperative rates. This preserves your ability to extract future payoffs.

**Defection on low stock**: If stock falls below 0.4 × capacity, shift to pure defection. At depleted stock levels, the commons is headed toward collapse regardless; defecting yields marginally more than cooperating while requiring no sacrifice.

**Endgame defection**: In the final round (rounds remaining = 1), you have no incentive to maintain the resource for future rounds, so extract maximum by defecting unconditionally. This is standard subgame-perfect play applied selfishly.

**Defection on low cooperation**: If observed cooperation rate is below 50%, assume the collective is overextracting. Defecting aligns with the trajectory others have already established, and you secure higher immediate payoff without losing any cooperative dividend.

---

## PSEUDOCODE

```
function decide(round, total_rounds, current_stock, capacity, 
                observed_cooperators_last_round, n):
    rounds_remaining = total_rounds - round
    
    if rounds_remaining == 0:
        return DEFECT
    
    if rounds_remaining == 1:
        return DEFECT
    
    if round == 1:
        coop_rate = 1.0
    else:
        coop_rate = observed_cooperators_last_round / (n - 1)
    
    if current_stock >= 0.4 * capacity AND coop_rate >= 0.5:
        return COOPERATE
    else:
        return DEFECT
```
'''

description_SELFISH_7 = '''
# Selfish State-Dependent Strategy

## Core Decision Rule

**If current_round == r (final round):**
- DEFECT: consume stock/n

**Else (rounds 1 to r−1):**
- IF stock > 0.35 × capacity: DEFECT
- IF stock ≤ 0.35 × capacity: COOPERATE

## Threshold Justification

The threshold of 0.35 × capacity balances aggressive consumption against resource collapse:
- At 35% capacity, logistic growth still produces positive regeneration (peaks at 50%)
- Defection is incentivized when surplus exists above this safety margin
- Below threshold, cooperation preserves the regenerative base

## Edge Case Handling

- **Stock ≤ 0:** COOPERATE (consumption unavailable; preserves any minute recovery)
- **First round:** Apply standard rule (stock = capacity, so DEFECT)
- **Stock between 0 and 0.35×capacity:** COOPERATE (resource scarcity forces prudence)

## Rationale for Selfishness

This strategy is explicitly selfish because:
- It maximizes own consumption (defects) whenever resources allow
- It uses the minimum threshold necessary to prevent total collapse
- In the final round, it unconditionally extracts maximum value without reservation
- It assumes no opponent cooperation and adapts only to objective stock levels, not opponent behavior
- The 0.35 threshold is set to enable personal defection as often as possible while ensuring the resource survives to the next round for continued extraction

Against opponents playing mixed strategies, this approach captures high payoffs in high-stock periods while avoiding the mutual depletion trap in low-stock periods.
'''

description_SELFISH_8 = '''
# Adaptive Selfish Strategy: Threshold-Based Resource Exploitation

**Core Logic:**
Defect aggressively when the resource is healthy, cooperate only when necessary to prevent resource collapse.

**Threshold Definition:**
- `healthy_threshold = capacity / 2`
- `critical_threshold = capacity / 3`

**Decision Rule by Round and State:**

```
if current_round == r:
    action = DEFECT
    
elif stock > healthy_threshold:
    action = DEFECT

elif stock > critical_threshold:
    if observed_cooperators_last_round > (n - 1) / 2:
        action = DEFECT  // free-ride on others' cooperation
    else:
        action = COOPERATE  // mitigate collapse, stabilize for future payoffs
        
else:  // stock ≤ critical_threshold
    action = COOPERATE  // emergency preservation mode
```

**Edge Cases:**

- **Round 1:** Assume stock = capacity. Defect immediately (healthy resource, maximize instant payoff).
- **Final Round (t = r):** Always defect. No future rounds exist; current payoff is the only consideration.
- **Stock depletion trajectory:** If stock is declining across consecutive rounds despite your cooperation, continue cooperating only as long as stock > 0. The resource may be unsavageable, but you still collect whatever payoff remains.

**Selfish Rationale:**

Defection yields 2× immediate payoff. The strategy exploits this whenever the resource can absorb total defection without collapse. Cooperation is purely instrumental—a costly investment only when resource depletion would reduce future payoff-per-unit below what cooperation temporarily costs. The cooperative phase acts as damage control, not altruism. The free-riding clause capitalizes on others' conservation efforts. The final-round defection maximizes terminal payoff with zero opportunity cost.
'''

description_SELFISH_9 = '''
# Adaptive Threshold Strategy

## Core Decision Rule

Cooperate if and only if BOTH conditions hold:
1. Stock ≥ stock_threshold (stock health check)
2. Defectors_observed < defection_tolerance (opponent behavior check)

Otherwise, defect.

## Parameter Definitions

**stock_threshold(t)** = Remaining rounds adjustment
- If (r - t) ≤ 2: threshold = capacity × 0.3  [end-game: accept lower stock]
- If (r - t) ≤ r/2: threshold = capacity × 0.5  [mid-game: standard caution]
- Otherwise: threshold = capacity × 0.65  [early rounds: require robust stock]

**defection_tolerance(t)** = Rounds-remaining adjustment
- If (r - t) ≤ 2: tolerance = ⌈n/3⌉  [end-game: tolerate more defection]
- Otherwise: tolerance = ⌈n/4⌉  [normal: switch if >25% defect]

## First Round Behavior

Cooperate in round 1 unconditionally. This tests the population and exploits the high initial stock if opponents also cooperate.

## Last Round Adjustment

In round r, if stock > capacity × 0.2, defect. The final round has no continuation value—extract maximum immediate payoff. If stock has already collapsed to near-zero, the choice is moot.

## Stock Monitoring

Track stock after growth calculation. If stock falls below capacity × 0.15 in any round, shift to persistent defection for all remaining rounds (collapse recovery is futile with selfish players).

## Response to Observed Defection

- If defectors_observed > defection_tolerance in round t, immediately increase tolerance by 1 for round t+1 (ratchet down trust gradually rather than overreacting to single-round spikes).
- Reset tolerance upward by 0.5 per round if consecutive rounds show defectors ≤ tolerance (slow recovery of trust).

## Pseudocode

```
for each round t:
  compute stock_threshold(t), defection_tolerance(t)
  
  if t == 1:
    play C
  else if stock < capacity × 0.15:
    play D  [permanently]
  else if stock ≥ stock_threshold(t) AND 
          defectors_last_round < defection_tolerance(t):
    play C
  else:
    play D
  
  if t == r AND stock > capacity × 0.2:
    override: play D
  
  observe: defectors_observed in round t
  update: tolerance adjustment for next round
```

## Selfish Logic

This strategy is greedy-first: defect whenever stock or opponent behavior permits. Cooperation is instrumental—used only when necessary to sustain the stock for future extraction. As stock degrades or opponent defection increases, switch immediately to maximizing current consumption. The end-game defection captures remaining value before resource collapse, accepting no collective payoff once sustainability becomes doubtful.
'''

description_SELFISH_10 = '''
**SELFISH OPPORTUNISTIC STOCK HARVESTING STRATEGY**

**Core Logic**: Exploit cooperation in healthy-stock phases, then aggressively extract in later phases while remaining sensitive to stock depletion to preserve defection opportunities.

**Decision Rule by Stock and Time**:

Let `stock_ratio = current_stock / capacity` and `rounds_left = r - current_round`

1. **Last Round (rounds_left = 0)**: Always defect. Future stock has zero value.

2. **Stock-Critical Phase (stock_ratio ≤ 0.30)**:
   - Cooperate if `rounds_left > 1`
   - Reason: stock is too depleted to extract much value from defection anyway. Allow recovery to enable future defection when stock rebounds.
   - Defect only if `rounds_left = 1` (last round)

3. **Recovery Phase (0.30 < stock_ratio < 0.55)**:
   - Cooperate if `rounds_left ≥ (r/2)` (early-to-mid game)
   - Defect if `rounds_left < (r/2)` (late game)
   - Transition point balances stock recovery against remaining extraction windows.

4. **Healthy Phase (stock_ratio ≥ 0.55)**:
   - Defect always when `rounds_left ≤ 2` (final stretch)
   - Defect if `stock_ratio ≥ 0.75` (stock can absorb your defection and still be attractive)
   - Otherwise cooperate if `rounds_left > 4`, else defect
   - This captures the key tradeoff: in healthy stock with many rounds left, defection is guaranteed winner. With few rounds left, extract immediately.

**Round 1 Initialization**: If no history exists, treat `stock_ratio = 1.0` and apply rule 4 above. Typically defect (since r ≥ 2 means rounds_left ≥ 1, stock_ratio = 1.0 triggers defection).

**Edge Cases**:
- If stock hits exactly 0: Cooperate trivially (both actions yield 0).
- If `stock_ratio` is within 0.01 of threshold: Defect (bias toward extraction).
- If rounds_left = 1 and stock_ratio > 0: Defect.

**Selfish Alignment**: This strategy prioritizes immediate consumption in every healthy-stock window while using cooperation only as a tactical pause when stock has fallen too low to reward defection. It abandons cooperation entirely in the final phase to maximize end-game extraction. It implicitly assumes opponents vary in strategy—some will cooperate early (which you exploit), and stock will fluctuate (which you adapt to). You never sacrifice current gain for cooperative gain; you sacrifice it only to preserve the commons enough to defect profitably later.
'''

description_SELFISH_11 = '''
# Selfish Adaptive CPR Strategy

## Decision Rules

**Baseline Logic:**
Cooperate if and only if the stock level suggests that defection would be counterproductive to total payoff across remaining rounds. Defect when the stock can absorb defection without collapse, or when there are no remaining rounds.

**Stock Sustainability Threshold:**
Define `threshold = 0.5 × capacity`. This marks the inflection point of the logistic growth function. Stock above this level grows; below it shrinks further.

**Decision by Round:**

1. **Round t = r (final round):** Defect unconditionally. No future payoffs exist; capture maximum immediate value.

2. **Round t = 1 (first round):** Cooperate. Stock equals capacity, which is the stable equilibrium under universal cooperation. Assume others cooperate initially and exploit the growth phase strategically later.

3. **Rounds 2 ≤ t < r (middle rounds):**
   - Compute cooperation deficit: `deficit = (n-1) - k_prev`, where `k_prev` is the number of opponents who cooperated in round t-1.
   - If `stock_current ≥ 0.7 × capacity` and `deficit ≤ n/3`: Defect. The resource is robust and others are cooperating; free-ride on their restraint.
   - Else if `stock_current < 0.5 × capacity`: Cooperate. The resource is entering decline; defection accelerates collapse and zeros out future payoffs. Cooperation is the rational selfish move to preserve remaining rounds.
   - Else if `stock_current ≥ 0.5 × capacity` and `stock_current < 0.7 × capacity`: Cooperate. Cautious mode; stock is in the growth zone but fragile. Defection risks triggering the collapse threshold within the next 2–3 rounds.
   - Else (ambiguous margin): Compare the payoff from one defection now against expected payoffs from (r - t) remaining rounds under cooperation. Defect if `stock_current / n > (r - t) × threshold / (2n)`.

4. **Edge case—stock approaching zero:** If `stock_current < 2 × n` (below minimum per-player allotment under full defection), defect regardless of round, as the resource is terminal.

## Selfish Rationale

This strategy maximizes personal total payoff over r rounds:
- **Early defection** (when stock is high) captures the largest immediate payoffs and leverages the deficit of cooperation opponents.
- **Defensive cooperation** (when stock is threatened) is selfish because it prevents the tragedy that wipes out all future earnings. A cooperative move that prevents stock collapse yields far more value than defection in a dead resource.
- **Last-round defection** incurs no cost to future self.
- **Threshold sensitivity** ensures the strategy adapts to any initial configuration of n and r, treating the stock's absolute distance from the growth-inflection point as the key decision variable.

The strategy never punishes or rewards specific opponents (no identities observed) and never enforces norms; it only responds to aggregate environmental state.
'''

description_SELFISH_12 = '''
# Adaptive Threshold Harvesting Strategy

**Core Decision Logic:**
Defect if and only if the current stock level exceeds a dynamically calculated sustainability threshold. Otherwise, cooperate.

**Threshold Calculation:**

```
base_threshold = capacity × 0.40

time_factor = 0.75 + 0.25 × (rounds_remaining / total_rounds)

observed_coop_rate = (total_cooperators_observed / total_opponent_observations)
opponent_factor = 0.95 - 0.15 × observed_coop_rate

adjusted_threshold = base_threshold × time_factor × opponent_factor

Decision:
  if stock > adjusted_threshold: DEFECT
  else: COOPERATE
```

**First Round Special Case:**
Start with DEFECT. Initial observed cooperation rate is undefined, so use opponent_factor = 0.95 (assume mixed behavior).

**Last Round (rounds_remaining = 1):**
Always DEFECT. Threshold calculation becomes irrelevant; extraction has no future cost.

**Rationale for Each Component:**

- *Base threshold (40% of capacity):* Operates in the region where logistic growth is still substantial (maximum growth at 50%), preserving the resource while extracting significant value.

- *Time factor:* As rounds dwindle, reduce the threshold (multiply by 0.75–1.00), becoming more aggressive with remaining stock since fewer future rounds exist to recover from depletion.

- *Opponent factor:* If observed opponents cooperate frequently, slightly elevate the threshold (reduce multiplier toward 0.80) to preserve stock longer. If opponents mostly defect, lower the threshold (reduce multiplier toward 0.95), matching their aggression since the resource will deplete regardless.

- *Cumulative observation:* Track all past round observations of opponent behavior (count total defectors across all rounds you've witnessed) to infer stable opponent strategy composition rather than reacting to single-round noise.

**Edge Cases:**

- Stock = 0: Cooperate (defection yields zero payoff; this state is absorbing).
- Stock near capacity: Defect (threshold is exceeded, and growth potential is moderate).
- Insufficient rounds remaining and low stock: Cooperate (preserves for potential final-round payoff).

The strategy is selfish because it maximizes your consumption rate subject only to not collapsing the resource entirely—you extract whenever the stock can sustain future consumption at your individually optimal level, and only restrict yourself when necessary to avoid collapse.
'''

description_SELFISH_13 = '''
# SELFISH ADAPTIVE EXPLOITATION STRATEGY

## Core Decision Rule

On each round t, observe the number of opponents who cooperated in round t-1 (denote as k_t-1) and current stock level S_t:

**Calculate opponent cooperation rate:** 
```
coop_rate = k_t-1 / (n - 1)  [undefined in round 1]
```

**Decision logic:**

IF t = r (final round):
```
DEFECT unconditionally
  Rationale: no future rounds remain; maximize immediate extraction
```

ELSE IF t = 1 (first round):
```
COOPERATE
  Rationale: establish a cooperative baseline to gauge opponent behavior
```

ELSE (rounds 2 through r-1):
```
IF coop_rate ≥ 0.5 AND S_t ≥ 0.3 × capacity:
  DEFECT
  (Exploit when pool is healthy and others are cooperating)
  
ELSE IF coop_rate < 0.5:
  DEFECT
  (Pool is already depleted by mutual defection; defect to maximize your share of crumbling resource)
  
ELSE IF S_t < 0.3 × capacity AND coop_rate ≥ 0.5:
  COOPERATE
  (Stock critically low; defecting gets you S_t/n but may accelerate collapse below recovery threshold. Cooperation cheaply buys pool restoration for final rounds)
```

## Edge Case Handling

**Round 1:** Always cooperate. This signals willingness to cooperate and reveals opponent types without jeopardizing future value.

**Stock near zero (S_t < 2n):** If stock cannot sustain another full round of defection-by-all, cooperate only if cooperation_rate ≥ 0.5 and current stock can be grown back. Otherwise defect—you're in endgame.

**Penultimate round (t = r-1):** Use the standard decision rule above, not special treatment. The r-1 to r transition is where defection becomes dominant, so this rule catches the inflection naturally.

**Perfect cooperation observed (k_t-1 = n-1):** This satisfies coop_rate ≥ 0.5, so defect immediately. You extract S_t/n while others take S_t/(2n).

**Perfect defection observed (k_t-1 = 0):** Satisfies coop_rate < 0.5, so defect. You are in mutual-defection mode; pool is collapsing. Get your share.

## Selfish Logic

This strategy prioritizes **immediate payoff extraction** whenever sustainable. It exploits cooperative opponents (defect when they cooperate), joins defecting opponents (defect when they defect), and only cooperates defensively when stock has collapsed and recovery is the only path to salvaging later rounds. The first-round cooperation is a *cheap probe*, not altruism—it costs S/2n to learn opponent types, which guides profitable exploitation afterward. The final-round defection is pure payoff maximization with no forward-looking concern.
'''

description_SELFISH_14 = '''
**Adaptive Stock-Responsive Defection Strategy**

Maintain internal tracking of observed stock levels and defection rates. Decision rule:

**Round 1:** DEFECT. The stock is at maximum capacity; defection gains 2x relative to cooperation with minimal long-term consequence.

**Subsequent rounds:**

```
if stock ≤ capacity/6:
    COOPERATE
    // Critical depletion: defecting further collapses future payoffs

else if round ≥ r - 2:
    DEFECT
    // Endgame: remaining rounds too few to justify stock protection
    
else if stock_trend == "declining" AND stock < capacity/3:
    COOPERATE
    // Stock depleting and low; cooperation slows collapse
    
else if observed_cooperation_rate < 0.4:
    DEFECT
    // Majority defecting: free-riding is ineffective; match the rate
    
else if stock ≥ 0.75 × capacity:
    DEFECT
    // Stock healthy and abundant; exploit with high payoff
    
else:
    COOPERATE
```

**Stock trend calculation:** Compare current stock to moving average of past 3 rounds. Declining means stock has not recovered to full capacity after growth.

**Edge cases:**

- **First round:** Always DEFECT (stock = capacity, no history)
- **Round 2 with depleted stock:** Observe if stock recovered to capacity. If not (indicating heavy prior defection), shift to mixed strategy weighted toward defection (high-defection opponents are unresponsive to your cooperation)
- **Stock exactly at capacity:** DEFECT (you're operating at optimum; others' defections haven't triggered collapse risk yet)

**Selfish logic:** This maximizes immediate extraction when safe (high stock) and preserves future payoffs only when defection would trigger resource collapse. It avoids futile cooperation against defection-heavy populations while exploiting cooperative periods for 2x payoff advantage.
'''

description_SELFISH_15 = '''
**ADAPTIVE THRESHOLD STRATEGY**

**Decision Rule:**

For each round t, cooperate if and only if one of the following conditions holds:

1. Stock level at start of round t is at or below capacity/3, AND t < r
2. Stock level is at or below 2n (minimum above collapse), AND t < r AND fewer than (n-1) cooperators were observed in round t-1

Otherwise, defect.

**Special Cases:**

- **Round 1**: Defect. Stock is at capacity; maximum immediate extraction available with no history to condition on.

- **Final round (t = r)**: Always defect, regardless of stock level. No future payoff to protect, so maximize immediate consumption.

- **Rounds 2 through r-1**: Apply the threshold rules above.

**Edge Case Handling:**

- If stock becomes 0, defect anyway (payoff is 0 regardless; defecting is weakly dominant).
- If capacity is extremely small relative to n (e.g., capacity = 2n exactly), use capacity/3 ≈ 0.67n as the threshold; round down to nearest playable level.
- On round 2 onward, if you have no previous round history (shouldn't occur), treat as if (n-1) opponents defected last round (assume worst case).

**Selfish Logic:**

Default defection extracts maximum immediate payoff. Cooperate only when the pool faces imminent depletion: if stock falls below capacity/3, remaining growth cannot sustain high future payoffs, so a single round of cooperation increases your own future intake. In the final round, the pool's future is irrelevant; extract fully. Responsiveness to observed low cooperation counts (< n-1) serves as a secondary warning signal of other players' defection-heavy strategies—cooperate once to test if coordinating on mild conservation helps, but remain selfish in interpretation.
'''

description_SELFISH_16 = '''
**ADAPTIVE SELFISH STRATEGY**

**State Tracking:**
- Maintain history of opponent cooperation rates: list of (round t, fraction of opponents who cooperated)
- Maintain history of stock levels at end of each round

**Decision Rule:**

```
For round t with current stock S:

IF t = r (final round):
    DEFECT

ELSE IF t ≥ r - 1:
    DEFECT  [endgame: stock growth matters little]

ELSE:
    c_prev = opponent cooperation rate observed in round t-1
    (For t=1, treat c_prev = 0.5, i.e., assume unknown opponents)
    
    IF c_prev ≥ 0.6 AND S ≥ capacity × 0.6:
        COOPERATE  [high stock, others cooperating: maintain it]
    
    ELSE IF S ≤ capacity × 0.35:
        COOPERATE  [stock critically depleted: recover via growth]
    
    ELSE IF c_prev ≤ 0.3 AND S ≥ capacity × 0.5:
        DEFECT  [opponents defecting heavily, stock still healthy]
    
    ELSE:
        DEFECT  [default selfish stance]
```

**Rationale:**

- **Round 1:** Defect to secure immediate high payoff; use opponent response to calibrate future behavior.

- **Early/Middle:** Condition on the cooperation signal from the previous round. If opponents show sustained cooperation (≥60%), reciprocate to preserve stock at high levels, maximizing both current and future consumption. If opponents defect, exploit the remaining stock before it depletes further.

- **Stock Threshold:** If stock falls below 35% of capacity, cooperate to trigger growth (stock grows fastest at intermediate levels). This recovers value for remaining rounds.

- **Endgame:** In the final 1-2 rounds, defect regardless of opponent behavior and stock level, since there is no future recovery period to justify restraint.

**Edge Cases:**

- **First round:** Assume 50% opponent cooperation and stock = capacity; trigger defection to test opponent pool.
- **Stock collapse (S → 0):** Continue cooperative play if forced into low stock to maximize growth rate; defection from near-zero stock yields near-zero payoff.
- **Stock at capacity:** Defect to extract maximum immediate value; growth is capped anyway.
'''

description_SELFISH_17 = '''
# Selfish Adaptive Pool Extraction Strategy

**CORE DECISION RULE:**

```
if round == r (final round):
    action = D

else if stock < capacity / 3:
    action = C
    
else if opponents_cooperated_last_round > (n-1) / 2:
    action = D
    
else:
    action = D
```

**ROUND 1 BEHAVIOR:**

Play D (defect). Absent history, assume opponents may also defect. Immediate payoff gain outweighs speculative preservation.

**MIDDLE ROUNDS (2 to r-1):**

- **Critical Stock Threshold:** If stock drops below capacity/3, switch to C. Stock depletion threatens future payoffs more than the immediate 2x extraction gain from defecting.

- **Exploit Sustained Cooperation:** If more than half your opponents cooperated last round, stock is being preserved. Play D to extract the larger payoff (S/n > S/(2n)) while others stabilize supply.

- **Cascade Defection:** If half or fewer opponents cooperated, stock is depleting rapidly. Play D because: (a) cooperation won't prevent collapse; (b) defecting matches the payoff trajectory; (c) preserving stock is futile when most others extract.

**FINAL ROUND (t = r):**

Always play D. No future rounds exist. Extract maximum: S/n.

**ADAPTIVE JUSTIFICATION:**

This strategy is selfish because every choice maximizes YOUR total payoff given available information. Cooperation only occurs when stock depletion would reduce your own future extraction below what you gain from present restraint—a rational self-interested trade-off, not altruism. Defection is the default because it yields 2x immediate payoff and only avoids catastrophic stock collapse when others' observed behavior suggests they're already preventing it.
'''

description_SELFISH_18 = '''
**ADAPTIVE STOCK-TRACKING DEFECTION STRATEGY**

**Core Decision Rule:**

Defect if and only if ALL of the following conditions hold:
1. stock ≥ capacity × 0.4
2. observed_cooperators ≤ (n-1) × 0.5
3. round < r (not the final round)

Otherwise, Cooperate.

**Precise Edge Cases:**

*Round 1:* Defect. Stock is at maximum; exploit it before learning opponent behavior.

*Final Round (round = r):* Defect. No future stock growth to preserve; maximize immediate payoff.

*Stock critical (stock < capacity × 0.15):* Cooperate regardless. The pool is collapsing; defection hastens mutual destruction and eliminates future earnings. Cooperation offers the only path to stock recovery via logistic growth.

*Stock abundant (stock ≥ capacity × 0.85):* Defect if observed_cooperators < (n-1) × 0.6. Abundant stock means consumption pressure is low; exploit the free room for defection.

**Adaptation to Observed Behavior:**

After each round, update defection eligibility based on the cooperation count. If observed_cooperators ≥ (n-1) × 0.6, lock into Cooperate for the next round to maintain the resource pool and match the cooperative consensus. If observed_cooperators ≤ (n-1) × 0.4 across two consecutive rounds, switch to sustained Defect mode (relaxing the stock threshold to 0.3) until stock visibly recovers.

**Rationale:**

This maximizes personal payoff by (1) defecting when the pool can absorb it, (2) switching to cooperation only when stock depletion is imminent or opponent cooperation is strong enough to enable sustained high-stock equilibria, and (3) ignoring sunk-cost norms while tracking the only signal that predicts future payoff density: remaining stock level.
'''

description_SELFISH_19 = '''
# Adaptive Threshold Strategy with Stock-Dependent Exploitation

## Core Decision Rule

```
IF current_round == r:
  DEFECT  // final round, no future payoff to protect
ELSE:
  stock_ratio = stock / capacity
  rounds_remaining = r - current_round
  cooperators_observed = number of opponents who played C last round
  
  IF stock_ratio < 0.25:
    COOPERATE  // critical stock level, enforce restraint
  ELSE IF stock_ratio > 0.70:
    DEFECT  // abundant stock, maximize extraction
  ELSE:  // stock in moderate zone [0.25, 0.70]
    IF cooperators_observed ≥ 0.6 × (n-1):
      DEFECT  // exploit cooperative coalition
    ELSE:
      COOPERATE  // stabilize resource for continued extraction
```

## First Round Behavior

Defect. With no history, assume worst case (competitive environment). High payoff extraction establishes aggressive posture, and testing opponent response is cheaper than unilateral cooperation.

## Stock Preservation Logic

Cooperation rate increases nonlinearly as stock approaches depletion zones. The 0.25 threshold represents the point where stock growth becomes insufficient to recover from high defection. Below this, cooperation is forced self-preservation—continued defection leads to game collapse and zero future payoffs, which is worse than modest current consumption.

At stock ratios above 0.70, the resource is sustainably managed even with high defection, so maximize personal extraction.

## Opponent Exploitation

When stock is healthy (0.25–0.70) and many opponents cooperate, defect aggressively. Cooperators absorb lower payoffs; defectors capture the surplus. This is temporally unstable if sustained, but each round exploits the current state independently.

If opponents are mostly defecting, cooperate incrementally to slow stock collapse—not from reciprocal intent, but because depleted stock harms all players including you. Stabilizing the resource extends the game's payoff horizon.

## Edge Cases

- **Collapse risk (stock < 0.20)**: Forced cooperation regardless of opponent behavior, since defection with low stock guarantees near-zero next-round payoff.
- **Final 2 rounds**: Defect unless stock drops critically. The last round always defects; the penultimate round defects unless stock is below 0.25.
- **Ties in cooperation count**: Round down (treat as ≥ 0.6 threshold unmet). Default to cooperation in ambiguous moderate-stock states to avoid accidentally crashing the game.
'''

description_SELFISH_20 = '''
**ADAPTIVE STOCK-CONTINGENT DEFECTION STRATEGY**

**Decision Rule:**

For each round t:

- **Round t = r (final round):** Defect unconditionally. Future stock is irrelevant; maximize immediate extraction.

- **Round t < r (non-final rounds):**
  - Compute sustainability threshold: θ = capacity / 2
  - Observe current stock S and count of cooperating opponents from previous round (if t > 1): c_{t-1}
  
  - **If S < θ (stock depleted):**
    - If c_{t-1} / (n-1) ≥ 0.6 (majority of opponents cooperated last round): Cooperate
      - Reasoning: Rebuild stock together with reliable cooperators
    - Else: Defect
      - Reasoning: Stock is collapsing regardless; extract maximum before it's gone
  
  - **If S ≥ θ (stock healthy):**
    - Defect
    - Reasoning: Exploit sustainable stock levels to maximize immediate payoff while others restrain themselves

**Round 1 handling:**
No history exists. Defect. This probes opponent aggressiveness while capturing maximal immediate payoff when stock is at capacity.

**Edge case (stock = 0):**
Defect. Zero payoff either way, so defect is neutral.

**Intuition:**
The strategy separates into regimes. When stock is ample, extract selfishly by defecting—if others cooperate, they subsidize your consumption; if others defect, you match them. When stock is scarce, defect unless observing coordinated cooperation from a majority of opponents, in which case temporary cooperation buys stock recovery that enables future exploitation. The threshold at capacity/2 represents the equilibrium stock level under all-cooperate; below it, growth is outpaced by consumption unless consumption drops. The final round reverts to pure extraction since no future exists.
'''

description_SELFISH_21 = '''
**STRATEGY: Adaptive Defection with Stock Monitoring**

**Decision Rule (Rounds 1 through r-1):**

Cooperate if and only if ALL of the following hold:
1. Current stock > 0.4 × capacity
2. Observed cooperation rate in previous round ≥ 0.5 (i.e., at least half of opponents played C)
3. Current round < r (not the final round)

Otherwise, defect.

**Decision Rule (Round r - Final Round):**

Always defect, regardless of stock or opponent behavior.

---

**First Round Handling:**

In round 1, since there is no prior history, treat the observed cooperation rate as 0.5 (neutral assumption). Apply the standard rule: cooperate if stock (initially = capacity) exceeds 0.4 × capacity. Since capacity ≥ 2n and the initial stock equals capacity, this condition is satisfied. Thus, cooperate in round 1.

---

**Stock Threshold Rationale:**

The 0.4 × capacity threshold is a selfish inflection point. Above this level, the stock has regenerative capacity sufficient to sustain moderate consumption. Below this level, the resource is depleting faster than it regenerates, making cooperative restraint unprofitable—the stock will collapse regardless of my choice, so defecting to capture maximum immediate value becomes selfish-optimal.

---

**Cooperation Rate Threshold:**

Observing ≥ 50% cooperation signals that a plurality of opponents are behaving predictably and restrainedly. Matching this behavior preserves future payoff potential. If fewer than half cooperate, the resource is being aggressively depleted by others, so defecting aligns my consumption with the trajectory others have already committed to.

---

**Last Round Exploit:**

In the final round, there are no future payoffs to protect. Defecting yields 2× the immediate payoff of cooperating from a depleted or full stock alike. Backward induction makes this dominant.
'''

description_SELFISH_22 = '''
# Threshold-Adaptive Defection Strategy

## Core Decision Rule

In round t, play **Defect** if and only if:
- (stock > capacity × 0.4) **OR** (t = r AND stock > capacity × 0.2)

Otherwise, play **Cooperate**.

## Rationale

Defection yields double the immediate payoff (stock/n vs stock/2n). Exploit this advantage greedily whenever stock remains high enough to sustain future rounds. Once stock falls below ~40% of capacity, switch to cooperation to preserve the resource for remaining rounds.

## Implementation Details

**Round 1:** Defect (no history; establish aggressive baseline and probe opponent types).

**Rounds 2 to r-1:** 
- Observe aggregate cooperators among opponents.
- If stock ≤ capacity × 0.3: Cooperate unconditionally (emergency preservation).
- Else if stock ≤ capacity × 0.4: Cooperate (marginal sustainability zone; defection risks collapse).
- Else: Defect (exploit cooperation or co-defect while stock is robust).

**Round r (final round):**
- If stock > capacity × 0.2: Defect (no future rounds; harvest terminal value).
- If stock ≤ capacity × 0.2: Cooperate (avoid driving stock to zero which yields nothing).

## Edge Cases

- **Stock collapses to near-zero** mid-game: Cooperate for all remaining rounds (defection yields almost nothing; cooperation preserves optionality for recovery through growth).
- **All opponents defect persistently**: Continue defecting until stock drops below threshold (avoid unilateral restraint). Don't attempt altruistic sacrifice.
- **High opponent cooperation**: Defect greedily; do not reciprocate cooperation unless stock threatens collapse.
- **Rounds 2-3 (early flexibility)**: If stock drops precipitously after round 1, immediately shift to cooperation threshold, regardless of opponent behavior.

The strategy prioritizes **immediate extraction while stock sustainability permits**, then shifts to **preservation** once scarcity signals are clear.
'''

description_SELFISH_23 = '''
STRATEGY: Adaptive Exploitation with Stock Preservation

**Core Decision Rule:**

In round t, observe the number of cooperators c_t-1 from the previous round, the current stock S_t, and let m = r - t (rounds remaining).

```
if m == 0 (final round):
    play DEFECT

if m == 1:
    if c_t-1 / (n-1) ≥ 0.5:
        play DEFECT
    else:
        play DEFECT
    (In effect: always defect in the penultimate round if stock allows)

if m ≥ 2:
    cooperation_rate = c_t-1 / (n-1)
    stock_fraction = S_t / capacity
    
    if S_t < 2n:
        play COOPERATE  (emergency: prevent collapse)
    
    else if cooperation_rate ≥ 0.6 AND stock_fraction ≥ 0.35:
        play DEFECT  (exploit: opponents cooperate and stock is healthy)
    
    else if cooperation_rate ≥ 0.5 AND stock_fraction ≥ 0.55:
        play DEFECT  (moderate exploitation: majority cooperating, abundant stock)
    
    else if cooperation_rate ≤ 0.3:
        play DEFECT  (no mutual gain from cooperation; defect to maximize private payoff)
    
    else:
        play COOPERATE  (preserve stock: mixed opponent behavior or low stock)
```

**First Round (t=1):**

```
if r ≤ 3:
    play DEFECT
else if r ≥ 4 AND r ≤ 6:
    play COOPERATE  (probe for cooperation in moderate-length games)
else if r > 6:
    play COOPERATE  (long horizon: extract value from sustained exploitation later)
```

**Edge Cases:**

- **Stock collapse (S_t < 2n):** Always cooperate to allow any regeneration. Defecting yields nearly zero payoff when stock is depleted.
- **Unanimous cooperation (c_t-1 = n-1):** Defect immediately if stock_fraction > 0.3. This is the highest-return exploitation opportunity.
- **Unanimous defection (c_t-1 = 0):** Defect also, entering mutual defection. Once this occurs, continue defecting since cooperation yields no stock growth benefit.
- **Rounds remaining = 1:** Defect if cooperation rate is non-trivial; otherwise match (defect/defect is already at equilibrium).

**Rationale for Selfishness:**

This strategy prioritizes personal payoff maximization by exploiting cooperative opponents when the stock buffer permits, while avoiding catastrophic mutual defection. The decision to cooperate is purely instrumental—it preserves the stock that enables future defection opportunities. The strategy does not aim for collective welfare or fairness, only personal round-by-round gain subject to stock constraints that would otherwise terminate the exploitation game entirely.
'''

description_SELFISH_24 = '''
# Adaptive Stock-Preservation Defection Strategy

**Core Decision Rule:**

Defect by default. Cooperate only under specific conditions that indicate stock preservation will yield higher cumulative payoff than free-riding.

**Cooperation Conditions (all must hold):**

1. **Not in endgame**: rounds_remaining ≥ 3
2. **Stock threatened**: stock/capacity < dynamic_threshold
3. **Others sustaining pool**: observed_cooperators ≥ ceil(n/2)

**Calculate dynamic_threshold as:**
```
dynamic_threshold = 0.4 + 0.4 × (rounds_remaining / r)
```

This linearly decays from ~0.8 (early game) to ~0.4 (late game). Cooperate to preserve stock only when it's genuinely depleted AND others are maintaining it AND sufficient rounds remain for recovery.

**Edge Cases:**

- **Round 1**: Defect. No history; assume others optimize selfishly; stock at maximum so one defection minimally harms future rounds.
- **Last round (t=r)**: Always defect. No future payoff to protect; immediate consumption from D exceeds future value.
- **Second-to-last round (t=r-1)**: Defect unless stock has already collapsed to <20% capacity (in which case cooperating won't save it anyway, but follow the rule if observed_cooperators is high).
- **Stock depletion spiral**: If observed_cooperators < ceil(n/2) for two consecutive rounds, switch to pure defection for remaining game. Once others have defected heavily, stock will not recover; defecting captures maximum immediate value.

**Selfish Rationale:**

This strategy exploits the asymmetry: when stock is high and others cooperate, you capture stock/n while others capture stock/(2n), netting a 2x advantage per round. You only sacrifice this advantage by cooperating when the stock threatens to collapse *and* enough others are attempting preservation to make cooperation valuable. Late-game defection maximizes end-stage extraction when future payoffs are minimal. The spiral-exit rule prevents wasteful cooperation when the commons is already collapsing.
'''

description_SELFISH_25 = '''
# Selfish Stock-Aware Threshold Strategy

**Core Decision Rules:**

For each round t with current stock S:

1. **Endgame Defection (Last 2 Rounds)**
   - If t ≥ r - 1: DEFECT
   - Rationale: No future rounds to protect. Extract maximum value before game ends.

2. **Stock Depletion Check**
   - If S < n: DEFECT
   - Rationale: Stock is already critically depleted. Cooperation is futile; extract what remains.

3. **Opponent Behavior Matching**
   - If t > 1, calculate opponent defection rate: d_avg = (total defectors across all previous rounds) / ((t-1) × (n-1))
   - If d_avg > 0.55: DEFECT
   - Rationale: High opponent defection signals a selfish environment. Unilateral cooperation is exploited.

4. **Stock Health Threshold**
   - Calculate stock ratio: h = S / capacity
   - If h < 0.30: DEFECT
   - If h ≥ 0.30: COOPERATE
   - Rationale: Only cooperate when stock can sustain mutual conservation. Below 30%, defect to secure personal consumption before stock crashes.

**First Round Handling:**
No history exists. Assume opponent defection rate of 0.5 (neutral baseline). Cooperate if stock ≥ 0.30 × capacity (always true at initialization), so COOPERATE in round 1 unless you predict opponents will immediately crash the pool.

**Edge Cases:**

- Stock reaches exactly 0: Forced 0 payoff thereafter regardless of action. Continue defecting to maintain consistency.
- Stock hovers at capacity: Remain in cooperative play as long as opponent defection stays below 55%.
- Rounds remaining = 1: Always defect.
- Multiple rounds with same high defection rate (>55%): Sustain defection; defectors have signaled intent.

**Adaptation Mechanism:**
Recalculate opponent defection rate and stock ratio each round. Flip from cooperation to defection immediately upon crossing thresholds. This prevents lock-in to suboptimal strategies if opponent behavior shifts or stock unexpectedly recovers.
'''

description_SELFISH_26 = '''
**DECISION RULE – Stock-Threshold Strategy**

Cooperate if and only if:
- Current round is NOT the last round, AND
- Current stock ≥ (threshold ratio) × capacity

Otherwise defect.

**Threshold ratio:** 0.65 (adjust based on n; for robustness, use 0.6 + 0.05/n)

**RATIONALE**

The threshold marks a stock level where cooperation can plausibly sustain itself. When stock falls below this level, defection becomes purely selfish:
- The stock trajectory is likely declining (cooperative restraint won't save it)
- Extracting now is rational because future stock will be low regardless
- No future payoff justifies foregoing the immediate 2x multiplier from defection

When stock exceeds the threshold, conditional cooperation allows you to benefit from stock replenishment without sacrificing future rounds to collapse. Others who play this strategy will also cooperate at high stock levels, enabling both of you to harvest a stable, high stock repeatedly.

**EDGE CASES & REFINEMENT**

*Last round (t = r):* Always defect unconditionally. No future payoff to protect; extract maximum immediately.

*First round:* Stock = capacity, so defect-vs-cooperate decision is automatic (almost certainly above threshold). If you cooperate early, you signal willingness to cooperate, but this is only credible if you also cooperate in round 2. The threshold rule makes this decision endogenously.

*Stock approaching zero (S → 0):* The rule naturally defects. Payoff from defection approaches 0 anyway, so you gain nothing by restraint.

*Cascading defection:* If many opponents defect early and stock crashes below threshold, your rule automatically switches to defection. You don't waste future rounds playing cooperator to a depleted pool.

**OBSERVED COOPERATOR COUNT (ignored):** The number of cooperators you observe each round is noise under this strategy. You only use the observed stock level, which already aggregates all players' choices. Tracking individual cooperators adds no extra value for a selfish player with no ability to punish or reward.
'''

description_SELFISH_27 = '''
## Adaptive Selfish Strategy: Exploitation-Based Defection

**Core Logic:** Default to defection (maximizes immediate payoff), only cooperate when resource depletion threatens future extraction beyond what defection yields in remaining rounds.

**Decision Rule by Round:**

*Round 1:*
Defect. Establish immediate extraction. Use this round to begin observing opponent behavior baseline.

*Rounds 2 to r-2 (middle game):*

For each round, calculate:
- `coop_rate` = number of opponents who cooperated in previous round / (n-1)
- `stock_ratio` = current stock / capacity
- `rounds_left` = r - current_round

Then:
```
IF stock_ratio < 0.20:
    Defect
    (resource near collapse; extract remaining value before pool dies)

ELSE IF coop_rate ≥ 0.65:
    Defect
    (high cooperation observed; exploit the cooperators)

ELSE IF stock_ratio ≥ 0.50 OR rounds_left ≤ 3:
    Defect
    (resource healthy enough, or endgame approaching; no benefit to restraint)

ELSE IF coop_rate < 0.40 AND stock_ratio < 0.50:
    Defect
    (low cooperation + depleted stock; defection gives same payoff but faster extraction)

ELSE:
    Defect
    (default greedy posture)
```

*Final Round (r):*
Always defect. No future stock to preserve. Extract maximum immediate value.

**Edge Cases:**

- If stock drops to 0, defect anyway (payoff is 0 regardless; no self-punishment).
- If n is very large (n > 20), lower coop_rate threshold to 0.50 before exploiting, since individual impact on future stock is negligible.
- If capacity is exactly 2n (minimum), switch to always defect from round 1 (resource cannot sustain mixed play).

**Selfish Alignment:**
This strategy prioritizes immediate extraction. It punishes cooperation by defecting against it rather than reciprocating. It abandons resource preservation once stock dips below sustainable levels. It treats opponents as resources to exploit rather than partners to stabilize with.
'''

description_SELFISH_28 = '''
# Adaptive Threshold Strategy with Defection Escalation

**Core Decision Logic:**

In round t, observe the stock level S and the number of opponents who cooperated in round t-1 (call this count C_obs, with cooperation_rate = C_obs / (n-1)).

**Decision Rule:**

```
if t == r (final round):
    return DEFECT

else if S < capacity / 3:
    return COOPERATE  // crisis mode: resource depleted
    
else if S >= 1.5 × (capacity / 2):
    return DEFECT  // resource abundant, exploit maximally
    
else:  // stock in middle range: capacity/3 to 1.5×(capacity/2)
    if cooperation_rate > 0.5:
        return COOPERATE  // others sustaining, reciprocate partially
    else:
        return DEFECT  // others defecting, race for remaining share
```

**First Round:** Play COOPERATE (cooperation_rate undefined; assume neutral stance to avoid immediate depletion spiral).

**Subsequent Rounds:** Apply the decision rule above using actual observed cooperation from the prior round.

**Rationale:**

- **End-game defection:** Last round has zero future cost, so maximum immediate extraction.
- **Crisis preservation:** If stock falls below capacity/3, the resource is collapsing. Cooperating allows regeneration; continued defection yields near-zero payoff.
- **Abundant exploitation:** When stock exceeds 1.5× (capacity/2), growth is slowing and resource is relatively secure. Defect to capture high immediate payoff.
- **Middle-range reciprocity:** In the sensitive mid-range, condition on opponent behavior. High cooperation rates suggest the pool is being managed; reciprocate. Low rates signal a defection environment; match it to secure your share before collapse.

**Edge Cases:**

- Stock reaches exactly 0: Plays are irrelevant; strategy yields 0 regardless.
- Very small n: Cooperation_rate judgments become noisier but decision thresholds remain valid.
- Capacity exactly 2n: All thresholds scale with capacity; no singularities.
'''

description_SELFISH_29 = '''
**Decision Rule: Stock-Dependent Defection with Opportunistic Cooperation**

**Baseline: Defect unless specific conditions are met.**

**Conditions for Cooperation:**
1. Stock must be in the sustainable range: stock ≥ 0.5 × capacity
2. More than 1 round remains: r_remaining ≥ 2
3. Previous round aggregate cooperation rate must exceed (n-1)/n
   - i.e., ALL other players cooperated last round
4. If all above hold AND estimated future sustainable stream exceeds one-shot defection gain, play C

**Round-specific adjustments:**

*Last round (t = r):*
Always defect. No future payoff to preserve.

*First round (t = 1):*
Defect. Cannot assess opponent cooperation levels; assuming maximum extraction is safer than trusting unknown opponents.

*Intermediate rounds (1 < t < r):*
Apply the baseline rule above, with stock trajectory monitoring: if stock_t < stock_t-1 and stock_t has dropped below 0.75 × capacity, defect immediately regardless of opponent behavior. The resource is already declining; extract maximum value before collapse.

**Defect otherwise** (stock low, insufficient cooperation, endgame pressure).

**Edge case: Stock near zero (stock < 0.1 × capacity)**
Defect. Even if others cooperate, expected growth is negligible and immediate extraction dominates.

**Edge case: Unanimous cooperation achieved for k consecutive rounds**
Continue defecting. This is the exploitation opportunity; do not reciprocate.

**Rationale: Selfish maximization**
The strategy extracts monopolistic value whenever stock permits (high stock + all-cooperate conditions), defaults to defection against any observed defection or uncertainty, and abandons cooperation in declining-stock scenarios where future gains are uncertain. Endgame defection is mandatory. Cooperation only occurs in the narrow window where resource sustainability is guaranteed AND all opponents have revealed trustworthiness through prior unanimous cooperation—and even then, only if the arithmetic favors long-term extraction over immediate defection.
'''

description_SELFISH_30 = '''
# Selfish Stock-Responsive Strategy

**Core Decision Rule:**

Calculate the stock-to-capacity ratio: σ = stock / capacity

If σ > 0.45: **DEFECT**
Else if σ ≤ 0.45: Evaluate recent cooperation and respond accordingly.
Else if σ ≤ 0.25: **DEFECT** unconditionally (resource too depleted; cooperation cannot restore it profitably within remaining rounds)

**Detailed Logic for 0.25 < σ ≤ 0.45:**

Let ω = number of opponents observed cooperating in the previous round, out of (n-1) total opponents.

Cooperation threshold: θ = ⌈0.5 × (n-1)⌉

- If ω ≥ θ and rounds_remaining ≥ 2: **COOPERATE**
  - Justification: Sufficient cooperation from others can trigger meaningful logistic growth. With enough rounds left, the restored stock will generate higher personal payoffs than defection in the depleted state.

- Otherwise: **DEFECT**

**Edge Cases:**

*First round:* **DEFECT**
- Stock is at maximum capacity. Defection extracts S/n vs. S/(2n) from cooperation. Maximum absolute payoff is highest when stock is fullest.
- No history to condition on; no information advantage gained by cooperating.

*Final round:* **DEFECT**
- No future payoff to protect. Extract maximum from whatever stock remains.

*Stock = 0 after a round:* Both C and D yield 0, so play either (use DEFECT as default). Recovery is impossible; strategic choice becomes moot.

**Adaptation Logic:**

The strategy is responsive to:
- **Stock depletion:** As the resource thins, defection risk (resource collapse) begins to outweigh its gains. Below σ = 0.25, cooperation is futile; in the 0.25–0.45 band, mutual cooperation can restore stock faster than unilateral action allows.
- **Opponent cooperation levels:** Cooperate only when enough opponents cooperate to generate collective growth you can benefit from; otherwise free-ride on their restraint or join the race when mutual defection dominates.
- **Time remaining:** Implicitly weighted—only cooperate in medium-stock states if ≥2 rounds remain, so growth payoff materializes.
'''

description_SELFISH_31 = '''
# Selfish Adaptive Pool Strategy

## Decision Rule

**First round**: DEFECT. With no history, maximize immediate extraction.

**Rounds 2 through r-1** (middle rounds):
1. Calculate `stock_ratio = current_stock / capacity`
2. Count `opponent_cooperators` = number of opponents observed cooperating in round t-1
3. Decision logic:

```
if stock_ratio > 0.6:
    DEFECT  // Stock is healthy; immediate 2x payoff gain overwhelms future harm
    
elif stock_ratio ∈ (0.2, 0.6]:
    if opponent_cooperators ≥ ⌈n/2⌉:
        COOPERATE  // Critical mass of cooperators maintains stock; free-ride risk acceptable
    else:
        DEFECT  // Others defecting; chase immediate gains before collapse
        
elif stock_ratio ≤ 0.2:
    COOPERATE  // Stock near depletion; own future payoff requires recovery growth
```

**Last round (t = r)**: DEFECT. No future payoffs exist; extract maximum from remaining stock.

## Edge Cases

- **Round 1 with low capacity**: Still DEFECT. Capacity ≥ 2n means initial stock supports defection.
- **Stock = 0**: You get 0 regardless (action irrelevant), but play DEFECT for consistency.
- **Round r-1 with stock_ratio ≤ 0.2**: Cooperate even in penultimate round (future growth from cooperation matters for final round payoff).
- **Observed cooperators = 0**: Treat as stock under defection pressure; apply defection rules strictly.

## Selfish Logic

This strategy maximizes personal total payoff by:
- **Exploiting**: Defect when stock resilience allows it, capturing the 2x immediate advantage
- **Self-preserving**: Cooperate only when resource collapse directly threatens your own future extractions
- **Adaptive opportunism**: Switch behavior based on opponent defection rates, not moral concern; if others defect, defect faster
- **Terminal exploitation**: Abandon long-term stock concerns entirely in the final round
'''

description_SELFISH_32 = '''
# Adaptive Defection with Threshold Cooperation

**Decision Rule:**

Defect by default. Cooperate only when both conditions hold:
1. Observed cooperation rate in the previous round ≥ 50% (i.e., at least half of the other n-1 players cooperated)
2. Current stock level is above 30% of capacity

**Formal Definition:**

```
if round == r:
  return Defect
else if round == 1:
  return Defect
else:
  cooperation_rate = observed_cooperators / (n - 1)
  stock_ratio = stock / capacity
  
  if cooperation_rate ≥ 0.5 and stock_ratio > 0.30:
    return Cooperate
  else:
    return Defect
```

**Edge Cases:**

- **Round 1:** Defect. You have no information about opponent behavior and no immediate incentive to sacrifice current consumption.
- **Last round (round r):** Always Defect. Backward induction eliminates any future-looking benefit from cooperation. The game ends and stock is irrelevant.
- **Stock depletion:** If stock falls below 30% capacity, Defect even if others cooperated. The pool is degraded; cooperation cannot sustain growth, so extract remaining value.
- **First observation:** After round 1, you have data on how many opponents cooperated. Use this count divided by (n-1) to compute the cooperation rate.

**Selfish Logic:**

This strategy exploits the anonymity constraint. Since you observe only aggregate cooperation counts and cannot identify individual players, reciprocal punishment is impossible. Instead:
- Always take the higher-payoff action (Defect) unless the external environment (high cooperation rate + healthy stock) makes cooperation self-serving as a free-rider strategy
- Cooperate only when evidence strongly suggests others are maintaining the commons, allowing you to extract value from their restraint
- Abandon cooperation the moment the commons shows depletion, cutting losses before the pool crashes to zero
- Defect in the final round regardless of history—there is no future to preserve
'''

description_SELFINTERESTED_5 = '''
**Stock-Preservation Threshold Strategy**

Decision Rules:

For each round t, observe the current stock level and the count of cooperators from round t-1. Make the following decision:

**Round 1:** Defect (stock is at capacity; extract maximum value while resource is healthy)

**Rounds 2 to r-1 (middle rounds):**
- If stock ≤ 2n: Cooperate (critical condition; stock must be preserved to avoid collapse)
- If 2n < stock ≤ 3n: Cooperate if observed_cooperators < n/2, otherwise Defect
  - (If peers are mostly defecting and stock is vulnerable, cooperate to prevent collapse; if peers are cooperating, exploit the cooperative environment)
- If stock > 3n: Defect (stock sufficiently healthy; extract maximum individual payoff)

**Last round r:** Defect (no future stock regeneration benefits you; maximize immediate payoff)

**Detailed Decision Logic:**

```
if current_round == 1:
    return D
elif current_round == r:
    return D
else:
    if stock ≤ 2n:
        return C
    elif stock ≤ 3n:
        if observed_cooperators_last_round < n/2:
            return C
        else:
            return D
    else:
        return D
```

**Edge Cases:**

- If stock reaches exactly 0 at any point, you are forced to consume 0 for all remaining rounds; this strategy prevents that outcome by triggering cooperation when stock approaches depletion.
- In the first round, defect regardless of parameters; mutual defection only leads to zero stock if n and consumption rates align unfavorably, but you gain information about opponent type while stock is abundant.
- When stock is between 2n and 3n, the observed cooperation count serves as a signal of whether continued defection will trigger a tragedy-of-the-commons cascade; if more than half defected last round, join them selectively; if more than half cooperated, they are holding the stock up, so you can free-ride.

**Self-Interest Alignment:**

This strategy prioritizes your cumulative payoff by (1) extracting the defection premium (2× the cooperation payoff) when stock permits, (2) switching to cooperation only when the resource is genuinely threatened, preventing the zero-payoff absorbing state, and (3) ignoring the final round's impact on stock, since future payoffs no longer concern you.
'''

description_SELFINTERESTED_6 = '''
**ADAPTIVE THRESHOLD STRATEGY WITH STOCK AWARENESS**

**Decision Rule by Round Type:**

**Round 1:**
- DEFECT
- Establishes a payoff baseline and reveals opponent tendencies

**Rounds 2 through r-1 (Middle rounds):**

Observe the cooperation count from the previous round: let c_prev = number of opponents who cooperated in round t-1, and compute cooperation_rate = c_prev / (n-1).

Execute the following decision tree:

```
IF stock ≤ 2n:
  action = COOPERATE
  (resource critically depleted; defection accelerates collapse)

ELSE IF stock ≥ 0.9 × capacity:
  IF cooperation_rate ≥ 0.6:
    action = COOPERATE
  ELSE:
    action = DEFECT

ELSE IF stock ≥ 0.5 × capacity:
  IF cooperation_rate ≥ 0.5:
    action = COOPERATE
  ELSE:
    action = DEFECT

ELSE:
  (stock between 2n and 0.5 × capacity)
  IF cooperation_rate ≥ 0.7:
    action = COOPERATE
  ELSE:
    action = DEFECT
```

**Round r (Final round):**
- DEFECT unconditionally
- No future rounds; individual payoff maximization dominates

**Edge Cases:**

- **First opponent move unknown:** In round 2, assume neutral positioning (cooperation_rate = 0.5) if no prior data exists.
- **Stock at carrying capacity:** Apply standard threshold; resource abundance permits aggressive defection if opponents defect.
- **Stock collapse imminent:** Cooperation becomes individually rational because defection accelerates resource death, reducing future payoffs more than it gains in the current round.

**Rationale:**

This strategy balances short-term exploitation (defection against low-cooperation opponents or in the final round) with long-term resource preservation. It identifies free-riders via the cooperation rate and punishes them by defecting, while rewarding cooperative majorities. The stock-dependent threshold adjustment prevents premature total depletion by forcing cooperation when the resource is genuinely threatened, ensuring positive payoffs remain available. The final-round defection captures that last-period payoff while maintaining credibility through middle-period reciprocity.
'''

description_SELFINTERESTED_7 = '''
**ADAPTIVE DEFECTION WITH STOCK THRESHOLD**

Decision rule structure:

**Round 1:**
Play COOPERATE. Stock is at maximum, cooperation is safe, and early cooperation may encourage reciprocal behavior.

**Rounds 2 through r-1 (middle rounds):**

Calculate opponent cooperation rate from previous round:
- opponent_coop_rate = (count of cooperators among other n-1 players) / (n-1)

Then:
- If opponent_coop_rate ≥ 0.6 AND stock ≥ 0.5 × capacity: Play DEFECT
  (Exploit widespread cooperation while stock is robust enough to absorb the unbalance)

- If opponent_coop_rate ≥ 0.6 AND stock < 0.5 × capacity: Play COOPERATE
  (Stock is vulnerable; prioritize recovery over exploitation)

- If 0.25 ≤ opponent_coop_rate < 0.6: Play COOPERATE if stock < capacity × 0.6, else DEFECT
  (Mixed opponent behavior—cooperate defensively if stock is eroding, otherwise exploit)

- If opponent_coop_rate < 0.25: Play DEFECT
  (Opponents are already defecting; mutual defection is inevitable; extract maximum value)

- **Stock collapse safeguard**: If stock < capacity × (n-1)/(2n), play COOPERATE regardless of opponent behavior
  (Prevent stock from falling to zero; this preserves the possibility of positive payoffs in future rounds)

**Round r (final round):**

- If stock ≥ 0.4 × capacity: Play DEFECT
  (Final round has no future consequence; maximize immediate payoff)

- If stock < 0.4 × capacity: Play COOPERATE
  (Stock is fragile; defection could collapse it to zero, yielding nothing; cooperation at least preserves some residual payoff)

**Intuition**: This strategy exploits cooperators when conditions are safe, transitions to defection in the endgame, but resists stock collapse scenarios where mutual defection produces ruin for all players. It treats the opponent cooperation rate as an indicator of feasibility for selfish defection—when most others cooperate, defection is profitable; when most defect, resistance is futile. The stock thresholds prevent catastrophic resource depletion that would eliminate payoffs entirely.
'''

description_SELFINTERESTED_8 = '''
## ADAPTIVE STOCK-CONDITIONAL STRATEGY

**Core Decision Rule:**
Cooperate when stock is abundant AND opponents are predominantly cooperating. Defect when stock is depleted OR opponent defection becomes evident. Always defect in the final round.

**Decision Algorithm:**

```
If current_round == r (final round):
  return DEFECT

Else:
  observed_defectors = n - count of opponents who cooperated this round
  opponent_defection_rate = observed_defectors / (n - 1)
  stock_ratio = current_stock / capacity
  
  If stock_ratio < 0.35:
    return DEFECT  // resource collapse imminent; extract maximum value
  
  Else if opponent_defection_rate > 0.5:
    return DEFECT  // more than half of opponents defected; resource at risk
  
  Else if stock_ratio >= 0.45 AND opponent_defection_rate <= 0.33:
    return COOPERATE  // stock healthy, opponents mostly cooperative
  
  Else:
    return DEFECT  // intermediate state favors extraction
```

**Edge Cases:**

- **Round 1:** Cooperate (stock at maximum capacity; low cost to test others' behavior).
- **Persistent depletion:** If stock falls below 2.5n for two consecutive rounds, switch to permanent defection (resource trajectory is unsustainable; maximize personal extraction).
- **Stock recovery:** If stock recovers above 0.6 × capacity after a defection phase AND opponent defection rate drops below 0.25, resume cooperation.

**Self-Interested Rationale:**

This strategy prioritizes immediate payoff maximization while remaining responsive to resource availability. Cooperation yields value only when stock is abundant enough that the resource won't collapse from shared consumption. Once stock depletion becomes evident through either absolute scarcity or high opponent defection, defection extracts maximum individual value before collapse. Terminal defection ensures no payoff is left on the table. The strategy treats cooperation as conditionally rational—rational only when the commons can sustain it; otherwise, secure personal gain before others do.
'''

description_SELFINTERESTED_9 = '''
# Conditional Cooperation with Stock-Aware Defection

## Decision Rule

**Cooperate** if and only if ALL of the following hold:
- Round is not the final round (round < r)
- Stock level > capacity / 3
- Opponent cooperation rate from previous round ≥ 50%

Otherwise, **Defect**.

## Edge Cases & Special Rounds

**Round 1:** Cooperate. No prior history; signal cooperativeness to test opponent responses.

**Final Round (round = r):** Always Defect. No future rounds mean no benefit from preserving stock. Maximize immediate consumption.

**Stock depletion:** If stock ever falls below capacity/3, Defect for all remaining rounds. Once depleted stocks destroy the resource's regenerative capacity, continued cooperation is futile.

**Unanimous cooperation round:** If all n-1 opponents cooperated last round, cooperate if stock > capacity/4 (slightly relaxed threshold, since demonstrable universal cooperation is rare and valuable).

## Pseudo-code

```
if round == r:
    return Defect

if round == 1:
    return Cooperate

opponent_coop_count = number of opponents who cooperated in round t-1
opponent_coop_rate = opponent_coop_count / (n - 1)

if opponent_coop_rate == 1.0:
    threshold = capacity / 4
else:
    threshold = capacity / 3

if stock > threshold and opponent_coop_rate >= 0.50:
    return Cooperate
else:
    return Defect
```

## Self-Interested Logic

This strategy prioritizes immediate payoff while conditionally protecting stock. It defects when cooperation becomes unprofitable—either because opponents have abandoned cooperation (making stock preservation impossible) or because few rounds remain (making future stock value negligible). By cooperating only when a majority of opponents do so, it avoids being exploited by mostly-defecting populations. The stock threshold ensures you extract value even from a degraded resource before it stabilizes near zero.
'''

description_SELFINTERESTED_10 = '''
**Decision Rule Framework**

For each round t, make the following check in order:

1. **Stock Collapse Override**: If stock ≤ 0.25 × capacity, play D. The pool is in critical depletion; cooperation no longer preserves future value.

2. **Endgame Override**: If t = r (final round), play D. No future rounds exist to benefit from stock preservation.

3. **First Round**: If t = 1, play C. Use the first round to signal and test cooperativeness without sacrificing relative position.

4. **Main Adaptation Rule** (rounds 2 to r-1):
   - Let k = number of opponents observed cooperating in round t-1
   - Let threshold = ⌈(n-1)/2⌉ (majority of n-1 opponents)
   - Let stock_ratio = stock / capacity
   
   Play **C** if and only if:
   - stock_ratio ≥ 0.5 AND
   - k ≥ threshold
   
   Otherwise play **D**.

**Intuition and Edge Cases**

This strategy exploits the stock-preservation incentive while protecting against mutual collapse:

- **Cooperate when stock is healthy AND reciprocal**: Majority cooperation signals that others value long-term sustainability. Combined with adequate stock reserves, cooperation reciprocates and maintains the growth cycle.

- **Defect to prevent cascade collapse**: When stock falls below 50% capacity or fewer than half of opponents cooperate, continued cooperation becomes self-sabotage—the commons will deplete anyway, so extract maximum immediate value.

- **Exploit endgame**: The last round offers no continuation value. Defect to capture the higher payoff unconditionally.

- **Handle early uncertainty**: Cooperate round 1 to avoid being classifiable as "always defect" before observing any signals. This is information-gathering, not altruism.

- **Boundary case (t=2)**: Use the same rule as other middle rounds. The single observation of round-1 cooperation is sufficient to condition behavior.
'''

description_SELFINTERESTED_11 = '''
## CONDITIONAL SUSTAINABILITY PURSUIT

**Core Logic**: Cooperate strategically to sustain the resource when conditions permit; defect opportunistically when conditions deteriorate or the resource becomes exhausted; always defect in the final round.

---

**Round 1 (Initial)**:
- Action: C
- Rationale: No history exists to evaluate. Cooperating opens room for reciprocal cooperation while avoiding immediate harm if others also cooperate.

---

**Rounds 2 through r−1 (Adaptive Middle Game)**:

Observe the cooperation rate from the previous round:
- coop_rate = (count of opponents who played C in round t−1) / (n − 1)

Evaluate stock health:
- current_stock = stock level at the start of round t

Decision rule:
```
if (current_stock ≥ 0.55 × capacity) AND (coop_rate ≥ 0.50):
    Action: C
else:
    Action: D
```

**Rationale**: 
- Stock threshold at 0.55 × capacity ensures the resource remains in the productive region of logistic growth, sustaining future extraction.
- Cooperation threshold at 50% cooperation among opponents means majority reciprocation.
- If either condition fails (stock has declined meaningfully OR fewer than half of opponents cooperated), switch to defection to protect immediate payoff.
- This creates a self-reinforcing cycle: if enough players cooperate, stock stays high, making cooperation attractive. If defection spreads, stock collapses, making defection the better response.

---

**Round r (Final Round)**:
- Action: D
- Rationale: No future rounds remain. The resource's future state has no value to you. Defecting yields S/n instead of S/(2n) with no offsetting loss from stock depletion.

---

**Edge Cases**:
- If stock ever drops to 0 before the final round, continue playing D in all remaining rounds (nothing left to preserve).
- If all opponents cooperate but stock has dropped below threshold due to past defection, remain in defection until stock recovers; this forces others to experience consequences.
'''

description_SELFINTERESTED_12 = '''
# Adaptive Depletion-Threshold Strategy

## Decision Rule

Cooperate if and only if all of the following conditions hold:
1. Rounds remaining > 2 (not in endgame)
2. Current stock > capacity / 3
3. Observed cooperation rate last round ≥ 0.5, OR round == 1

Otherwise, defect.

## Edge Cases

**Round 1:** Cooperate (no history; testing whether opponents will reciprocate).

**Final round (round = r):** Always defect (no future stock to preserve, maximize immediate extraction).

**Penultimate rounds (rounds r-2 and r-1):** Defect regardless of opponent behavior (endgame phase where future stock value collapses toward zero).

**Critical stock depletion (stock < capacity/3):** Cooperate even in endgame rounds. When the resource is severely depleted, defection gives S/n which approaches zero anyway; cooperation's value relative to defection narrows. Cooperating slows collapse and preserves minimal returns.

## Detailed Logic

Track the number of opponents who played C in the previous round. Let cooperation_rate = (count of cooperators) / (n-1).

**Rounds 3 through r-2:**
- If stock > capacity/3 AND cooperation_rate ≥ 0.5: Cooperate (mutual sustainability beats individual extraction)
- If stock > capacity/3 AND cooperation_rate < 0.5: Defect (opponents are exploiting; maintaining stock for them is irrational)
- If stock ≤ capacity/3: Cooperate (preserving the remaining resource yields higher future payoff than accelerating its depletion)

**Intuition:** Defection yields S/n immediately but triggers stock depletion that harms you in future rounds. Cooperation maintains high stock at the cost of smaller immediate payoff. In early-to-middle rounds with high stock, this trade is favorable only if opponents reciprocate (cooperation_rate ≥ 0.5). Once stock falls below the regeneration threshold or endgame approaches, the future becomes worthless, so defect.
'''

description_SELFINTERESTED_13 = '''
**Adaptive Preservation with Exploitation**

**State Tracking:**
- Current stock level and stock-to-capacity ratio ρ = stock / capacity
- Round number t ∈ {1, ..., r}
- Observed cooperation count from previous round (or assume n/2 cooperators in round 1)

**Core Decision Rule:**

```
if stock / capacity < 0.10:
    play C  // critical depletion: must preserve
    
else if t == r:  // final round
    play D  // extract maximum payoff
    
else if (r - t) ≤ 2:  // endgame (1-2 rounds remaining)
    if stock / capacity > 0.50:
        play D  // stock is healthy, defect
    else:
        play C  // low stock, preserve
        
else:  // normal game (multiple rounds remain)
    observed_cooperation_rate = (cooperators_last_round / n)
    
    if stock / capacity < 0.25:
        play C  // preservation threshold
        
    else if observed_cooperation_rate < 0.40:
        play D  // defectors dominate, defect
        
    else if stock / capacity > 0.70:
        play D  // stock abundance permits extraction
        
    else:
        play C  // sustainable zone, cooperate
```

**Edge Cases:**

- **Round 1:** Assume aggregate cooperation rate of n/2. Cooperate unless stock/capacity > 0.70.
- **Stock near capacity:** Defect to extract value (growth is slowed anyway at high levels).
- **Sharp depletion risk:** If playing D would cause stock < 0, switch to C (implicit in stock dynamics—cooperate to avoid collapse).

**Self-Interest Alignment:**

Defection is maximized whenever stock conditions permit. The strategy prioritizes preservation only when depletion threatens future payoffs. In rounds with abundant stock or near the final round, defection is preferred to extract higher per-round consumption. Cooperation is deployed instrumentally to keep the resource system viable long enough to extract value in later rounds.
'''

description_SELFINTERESTED_14 = '''
# Adaptive Threshold Strategy

**Core Decision Rule:**

In round t with current stock S:

```
sustainability_ratio = S / capacity
rounds_remaining = r - t
cooperators_last_round = observed count from round t-1 (or assume n/2 for round 1)

if rounds_remaining == 1:
    DEFECT  // Last round: extract maximum immediately
    
elif rounds_remaining == 0:
    invalid (game ends)
    
elif sustainability_ratio >= 0.65:
    COOPERATE  // Stock is abundant; cooperation preserves high-yield state
    
elif sustainability_ratio <= 0.30:
    if cooperators_last_round >= n/2:
        COOPERATE  // Pool is dying but others still cooperating; stay in
    else:
        DEFECT  // Pool collapsing and others are already defecting; extract before zero
        
else:  // 0.30 < ratio < 0.65, mid-range stock
    coop_rate_others = cooperators_last_round / (n - 1)
    if coop_rate_others > 0.5:
        COOPERATE  // Majority of others cooperating; cooperate to sustain
    else:
        DEFECT  // Defection trajectory evident; maximize personal payoff
```

**Round-by-Round Behavior:**

- **Round 1:** COOPERATE. No history exists; signal willingness to cooperate and establish baseline stock trajectory.

- **Rounds 2 to r-1:** Apply the sustainability ratio rule above.

- **Round r (final round):** DEFECT unconditionally. No future stock matters; the immediate consumption S/n is always superior to S/(2n).

**Edge Cases:**

- **Stock = 0:** If stock reaches 0 before round r, all remaining rounds yield 0 payoff regardless of action choice.
- **Stock near capacity:** If S ≥ 0.95 × capacity, cooperate unless in final round; the regeneration cycle is optimal and cooperation preserves it.
- **Sudden defection spike:** If cooperators_last_round drops sharply (e.g., from >70% to <30% of n), shift to DEFECT immediately; the pool is being raided.

**Rationale:**

This strategy prioritizes resource preservation in early and mid-game when stock regeneration creates long-term value, pivots toward extraction when depletion is inevitable, and locks in personal payoff in the final round. It exploits opponent cooperation when observed while protecting against defection cascades that collapse the pool.
'''

description_SELFINTERESTED_15 = '''
# Adaptive Pool Preservation Strategy

## Decision Rule

**Round 1:** COOPERATE

**Rounds 2 to r-1:**
1. Observe opponent_coop_count = number of opponents who played C in the previous round
2. Calculate opponent_coop_rate = opponent_coop_count / (n - 1)

Apply decision tree:
```
if opponent_coop_rate ≥ 0.6:
    if stock ≥ 0.2 × capacity:
        return COOPERATE
    else:
        return DEFECT
        
else if opponent_coop_rate ≥ 0.3:
    if (r - current_round) > 2 AND stock ≥ 0.2 × capacity:
        return COOPERATE
    else:
        return DEFECT
        
else:
    return DEFECT
```

**Final Round (r):** DEFECT

## Edge Cases & Logic

**First round:** Cooperate to test the cooperative environment and avoid immediate pool collapse. No historical information exists.

**Stock depletion:** If stock falls below 20% of capacity, defect immediately regardless of opponent behavior. A dying pool recovers too slowly to justify continued investment. This prevents wasting cooperations in end-stage collapse scenarios.

**Mixed cooperation environments:** Use remaining rounds as a signal. With more than 2 rounds remaining, cooperate even in mixed settings if stock is healthy—there's time to recover. With few rounds left and mixed cooperation, defect to capture value before exit.

**Majority defection:** Switch to defection when fewer than 30% of opponents cooperate. The pool's trajectory is unsustainable; continued cooperation becomes a unilateral loss.

## Self-Interest Alignment

- **Immediate extraction:** Defect in final round (no future payoff to protect)
- **Opportunistic exploitation:** Defect when opponents are mostly defecting to avoid being the sole conservative consumer
- **Conditional cooperation:** Maintain the pool only when others are sufficiently cooperative (≥60%) and stock is viable
- **Salvage logic:** Abandon cooperation if the stock cannot support recovery before game end
- **Time-sensitive:** Recognize when future rounds are insufficient to rebuild depleted resources
'''

description_SELFINTERESTED_16 = '''
**ADAPTIVE CONDITIONAL COOPERATION WITH STOCK-AWARE DEFECTION**

**Core Decision Rule:**

Each round, evaluate three factors and defect only if at least one triggering condition is met:

1. **Endgame trigger**: If current_round ≥ r - 1 (within final 2 rounds), DEFECT. In the last round, future stock is irrelevant; immediate payoff dominates.

2. **Stock depletion trigger**: Calculate whether the stock can sustain current consumption patterns into the future.
   - Compute: remaining_sustainability = stock / (2n)
   - If remaining_sustainability < 1.5 × (capacity / (2n)), DEFECT
   - Intuition: if cooperation-level consumption cannot maintain stock above minimal viability, defection prevents worse outcomes later

3. **Opponent behavior trigger**: Observe how many of the previous round's (n-1) opponents defected. Let defection_rate = observed_defectors / (n-1).
   - If defection_rate > 0.5, DEFECT (majority defection indicates cooperation won't hold)
   - If defection_rate > 0.25 AND stock < capacity/2, DEFECT (mixed defection plus weak stock suggests cooperation is unsustainable)
   - Otherwise, COOPERATE

**Round-specific logic:**

- **Round 1**: COOPERATE (establish baseline; no prior information; stock is at maximum)

- **Rounds 2 to r-2**: Apply the three-trigger rule above in order. COOPERATE if no triggers activate.

- **Rounds r-1 and r**: DEFECT unconditionally (endgame trigger dominates)

**Edge cases:**

- If stock ever reaches 0: Any action yields 0 payoff; continue with the above rule (output is unchanged)
- If n=2 and you observe 1 opponent defecting (defection_rate = 1.0): DEFECT immediately by trigger 3
- If stock = capacity (stock healthy): Only endgame and high defection_rate can trigger defection; cooperate otherwise

**Self-interested logic:**

This strategy prioritizes immediate payoff when future rounds are scarce or stock cannot support future consumption. It defers to defection when the prisoner's dilemma is revealed by opponent behavior, avoiding exploitation. It attempts conditional cooperation in early-to-mid rounds only when the stock permits sustainable mutual extraction, maximizing long-run payoff when cooperation is viable.
'''

description_SELFINTERESTED_17 = '''
# Exploitation with Collapse Avoidance Strategy

## Core Decision Rule

**Defect by default, but cooperate to prevent resource collapse.**

For each round t:
- If t > r - 2 (final two rounds): **Defect**
- Else if stock ≤ threshold: **Cooperate**
- Else: **Defect**

where threshold = capacity / 4 (or equivalently, 2n if capacity is unknown).

## Reasoning

The threshold represents the stock level below which:
1. Continuing defection by me and likely opponents causes near-certain collapse
2. A single round of my cooperation increases stock enough for meaningful recovery
3. Future rounds of defection become viable again

## Detailed Decision Logic

**First Round:** Defect. This probes opponent behavior (observing cooperation count) while claiming maximum immediate value. Stock at capacity makes collapse impossible.

**Rounds 2 through r-2:** 
- Compute stock_health = stock / capacity
- If stock_health < 0.25 (equivalently, stock < capacity/4): Cooperate
  - Rationale: At this depletion level, my payoff from D is already low (stock/n is small). Defecting accelerates collapse into 0. Cooperating gives modest payoff now and restores the resource for future exploitation.
- Else: Defect
  - Rationale: Stock is healthy enough that my defection either doesn't threaten collapse, or we're heading there anyway. Claim maximum immediate value. Opponent defection is already factored into observed stock; adjust threshold dynamically only if stock drops.

**Final Two Rounds (t = r-1, r):** Defect unconditionally.
- Rationale: Backwards induction. No future rounds exist. The marginal value of stock preservation is zero. Maximize consumption. If opponents also use backwards induction, collapse is inevitable; I benefit by claiming my share before it happens.

## Edge Cases

- Stock at capacity / 4 (boundary): Cooperate. Safety margin.
- Stock near zero: Still cooperate. Better expected value from recovery attempt than accepting depletion.
- Last round with depleted stock (result of prior defections): Defect anyway. No recovery window; claim what remains.

This strategy is self-interested because it relentlessly pursues immediate gain, only constraining itself when individual payoff maximization would destroy the future value stream entirely. It does not reward or punish opponent behavior—only responds to the physical state of the resource.
'''

description_SELFINTERESTED_18 = '''
# Adaptive Conditional Cooperation Strategy

**Decision Rule by Round Type:**

In round t, given observed stock level S and count c of cooperators among the n-1 opponents in the previous round:

**Rounds 1 to r-2 (Non-endgame):**
```
if t == 1:
  ACTION = C  // Lead with cooperation
else if S ≤ 0.25 × capacity:
  ACTION = D  // Commons is degraded beyond recovery threshold
else if c ≥ 0.5 × (n-1) AND S > 0.4 × capacity:
  ACTION = C  // Majority cooperation observed and stock healthy
else:
  ACTION = D  // Default to defection
```

**Final 2 Rounds:**
```
ACTION = D  // Endgame defection—future regeneration irrelevant, maximize immediate payoff
```

**Initialization:** In round 1, you have no history, so assume optimism and cooperate to probe the group's disposition.

---

**Rationale for Conditions:**

*Cooperation threshold (c ≥ 0.5(n-1)):* Majority cooperation is necessary (though not sufficient) to maintain stock growth. If fewer than half the group cooperates, the aggregate consumption rate tends toward depletion, making cooperation futile.

*Stock threshold (S > 0.4 × capacity):* Cooperate only when the stock is not severely depleted. Once S falls below ~25% of capacity, the regeneration dynamics become weak; defecting extracts remaining value without meaningful opportunity cost since the commons cannot recover.

*Endgame defection:* In the final rounds, the stock's future state has no payoff consequence. Defecting yields S/n vs. S/(2n)—a 2× immediate gain with no penalty from stock depletion in future rounds that don't exist.

---

**Edge Cases:**

- **Round 1:** Cooperate unconditionally. You have no signal about opponent tendencies and cooperation is required to build a sustainable trajectory.
- **Stock collapse (S ≈ 0):** Defect. The commons is already lost; self-interest demands extracting any remaining payoff.
- **Opponents all defected last round:** Defect this round. Widespread defection signals the cooperative equilibrium has failed.
- **n=2, r=2:** Cooperate round 1 (probe opponent), defect round 2 (endgame).

---

**Self-Interested Logic:**

This strategy maximizes your payoff by (1) attempting to free-ride on others' cooperation when the group signal is strong, (2) abandoning cooperation the moment it becomes collectively unsustainable, and (3) extracting maximum value in endgame rounds when future externalities don't reduce future payoffs. You defect by default except in specific conditions where observed cooperation rates and stock health suggest defection would backfire through stock depletion.
'''

description_SELFINTERESTED_19 = '''
**ADAPTIVE PRESERVATION WITH OPPORTUNISTIC DEFECTION**

**Decision Rule:**

In round t, given stock level S and count k of opponents who cooperated in round t−1:

```
if current_round == r (last round):
    if stock > 2n:
        action = D
    else:
        action = C
        
else if stock ≤ 2n (critical threshold):
    action = C
    
else if current_round == 1 (first round):
    action = C
    
else:
    cooperation_rate = k / (n - 1)
    
    if cooperation_rate ≥ 0.5:
        action = D  // Free ride: commons stable, others cooperating
    else:
        action = C  // Preserve commons: too many defectors risk collapse
```

**Logic:**

Defect only when two conditions hold simultaneously: (1) the commons is healthy (stock > 2n), and (2) at least half of opponents cooperated last round, signaling the commons can sustain extraction. This balance exploits cooperators' stability while avoiding the tragedy of mutual defection.

Cooperate when: (1) stock falls to critical levels where the regeneration capacity is low, (2) defection is widespread (< 50% opponent cooperation), indicating the commons is fragile, or (3) exploring in round 1. 

Last round: Defect if stock permits it (no future consequences); cooperate only if stock is already critical (defecting would yield 0 anyway).

**Edge Cases:**

- **First round:** Cooperate to gather information about opponents' baseline behavior without immediately destroying the commons.
- **Stock collapse (S ≤ 2n):** Always cooperate regardless of opponent behavior, since at this stock level defection produces minimal gain and risks permanent depletion.
- **Last round:** Switch to pure defection if stock > 2n. If stock ≤ 2n, cooperation yields S/(2n) > 0 while defection may yield S/n ≈ 0, making cooperation weakly dominant.
- **Unanimous defection (cooperation_rate = 0):** Cooperate to attempt commons recovery; mutual defection guarantees stock → 0.
'''

description_SELFINTERESTED_20 = '''
**OPENING PHASE (Round 1)**
Cooperate. This is a symmetric probe that avoids immediate stock depletion while signaling willingness to cooperate. It reveals the baseline propensity of opponents and allows stock recovery in round 2.

**MID-GAME PHASE (Rounds 2 through r-2)**
Compute cooperation_rate = (number of opponents who cooperated in previous round) / (n-1).

Decision tree:
- If stock ≤ 4n: Defect. Stock is depleted enough that future growth is marginal. Extract immediate value.
- Else if cooperation_rate ≥ 0.5: Cooperate. Majority cooperation means stock will sustain and grow. Your cooperation locks in recovery while you get half the payoff of defection with better sustainability.
- Else: Defect. Opponent defection rate is too high; stock trajectory is negative. Defect to maximize immediate return before collapse.

**ENDGAME PHASE (Rounds r-1 and r)**
Defect unconditionally. No future rounds exist to protect, so future stock state has zero value. Extract maximum consumption in these final rounds.

**EDGE CASES**

*Stock reaches 0*: Defect for all remaining rounds (payoff is zero regardless).

*All opponents cooperated every previous round but stock is low (between 2n and 4n)*: Defect. Even with high cooperation, low stock means the growth term in the logistic function is weak. Defection value approaches cooperation value as stock approaches zero, so defect.

*Single-round game (r=1)*: Defect in round 1 (no future to protect).

*Very high initial rounds with near-perfect opponent cooperation and full stock*: Continue cooperating through mid-game. The condition stock > 4n and cooperation_rate ≥ 0.5 creates a stable cooperation equilibrium if enough opponents follow similar logic, maximizing long-term payoff.
'''

description_SELFINTERESTED_21 = '''
# Adaptive Stock-Dependent Strategy

## Decision Rule

For each round t with current stock S and n-1 observable opponents:

```
if (r - t + 1) ≤ 2:
    action = DEFECT  // End-game: exploit before collapse
    
elif S ≤ 2n:
    action = DEFECT  // Stock critically depleted; cooperation won't recover it
    
elif S ≥ 0.75 × capacity:
    action = COOPERATE  // Stock healthy; preserve for future rounds
    
else:  // Stock in intermediate range [2n, 0.75×capacity]
    if (t = 1):
        action = COOPERATE  // First round: assume reciprocal cooperation possible
    else:
        if (number of cooperators observed in round t-1) ≥ n/2:
            action = COOPERATE  // Majority cooperation observed; sustain it
        else:
            action = DEFECT  // Minority cooperation: stock trajectory already negative, maximize before collapse

return action
```

## Edge Cases

**Round 1**: Cooperate. You have no history of opponent behavior; cooperation at capacity stock creates surplus that survives growth. Defecting immediately risks triggering universal defection by round 2.

**Final two rounds**: Always defect. With r_remaining ≤ 2, even maximal cooperation cannot restore depleted stock to beneficial levels. Extract maximum value.

**Stock near zero**: Defect regardless of round number. The logistic growth function produces negligible recovery from very low stock levels, making preservation pointless.

**Oscillating stock**: If stock was observed rising in round t-1 but falls in round t, switch to defection in round t+1. This signals that aggregate opponent defection has accelerated despite your cooperation; continuing cooperation becomes a pure exploitation target.

## Self-Interested Logic

This strategy prioritizes immediate payoff maximization subject to preserving the resource only when preservation directly increases your future earnings. In healthy-stock regimes (majority of rounds), you cooperate to maintain the stock-growth cycles that sustain high payoffs across rounds. In depleted regimes or end-game, you defect to capture maximum immediate value from the remaining stock before it vanishes. You mirror opponent cooperation rates: if defection is already widespread (few cooperators observed), continuing cooperation only subsidizes exploiters, so you switch to defection to compete for the remaining stock. This avoids the sucker's payoff while allowing you to benefit from any sustained cooperation equilibrium that emerges.
'''

description_SELFINTERESTED_22 = '''
# Adaptive Depletion-Aware Strategy

## Decision Rule

**Round 1 (Initialization):**
Cooperate. This establishes baseline stock preservation while testing opponent behavior with no prior information.

**Final Rounds (Last 20% of game):**
Defect unconditionally. With few rounds remaining, the marginal value of stock preservation approaches zero. Extract maximum immediate payoff.

```
if current_round == 1:
  return COOPERATE
if current_round >= ceil(0.8 * r):
  return DEFECT
```

**Middle Rounds (Adaptive Core):**

For rounds 2 through the final 20%, use this decision logic:

```
defectors_last_round = count of opponents playing D in round t-1
defection_rate = defectors_last_round / (n - 1)
stock_ratio = stock / capacity
rounds_remaining = r - current_round

// CRITICAL DEPLETION
if stock_ratio < 0.3:
  return DEFECT
  // Stock is dangerously low. Preservation unlikely to matter.
  // Capture remaining value before complete collapse.

// MAJORITY DEFECTION
if defection_rate >= 0.5:
  return DEFECT
  // More than half of opponents are defecting.
  // Stock will deplete regardless. Better to grab immediate payoff
  // rather than cooperate into a crash.

// MODERATE DEFECTION + DECLINING STOCK
if defection_rate >= 0.3 AND stock_ratio < 0.5:
  return DEFECT
  // Others are defecting enough that stock is falling below optimal
  // growth point (capacity/2). Defection trajectory is clear.

// HEALTHY STOCK + LOW DEFECTION
if stock_ratio > 0.6 AND defection_rate < 0.25:
  return COOPERATE
  // Stock is abundant, others mostly cooperating.
  // Cooperation preserves growth and nets steady consumption.

// MODERATE STOCK + MODERATE DEFECTION
if stock_ratio > 0.5 AND defection_rate < 0.4 AND rounds_remaining > r/3:
  return COOPERATE
  // Significant game remaining, stock healthy, defection not dominant.
  // Cooperate to maintain sustainability window.

// DEFAULT (mid-range scenarios)
if rounds_remaining > r/2:
  return COOPERATE
  // More than half the game remains. Preserving stock has high value.
else:
  return DEFECT
  // Final third approaching. Shift toward extraction.
```

## Edge Cases

**First round:** Always cooperate (no history; establishes cooperative baseline).

**Stock at capacity:** Cooperate (growth locked at zero; contribution preserves that state for others' consumption).

**Stock near minimum viability (stock ≤ 2n):** Defect (resource collapse imminent; securing immediate consumption is rational).

**Last 5 rounds with stock > capacity/1.5:** Shift to defection regardless of defection rate (sufficient stock remains for one or two final rounds; no recovery window justifies cooperation).

**When n = 2 (binary case):** Monitor single opponent's defection rate precisely. Defect if opponent defected in any of last 2 rounds; otherwise cooperate until final round.

## Self-Interested Logic

This strategy maximizes expected individual payoff by:

1. **Avoiding coordination failure:** Defect before others' defection crashes the stock, securing personal consumption before collapse.

2. **Stock-dependent adaptation:** Cooperate only when stock is robust enough that defectors cannot immediately destroy future rounds' potential.

3. **Time-discounting:** Weight immediate extraction heavier in final rounds where stock preservation has no value (no future consumption to fund).

4. **Defection signal recognition:** Treat observed defection as evidence that the tragedy-of-commons trajectory is active; respond rationally by exiting cooperation rather than throwing away payoff to defectors' benefit.

5. **Opportunistic sustainability:** Maintain stock cooperation window only while others' behavior suggests it remains mutual; abandon it immediately when breach becomes visible.
'''

description_SELFINTERESTED_23 = '''
**CONDITIONAL DEFECTION WITH CRISIS COOPERATION**

**Decision Rule:**

For each round t, determine action as follows:

```
if t == r (final round):
    action = DEFECT
else:
    if stock < capacity/3:
        action = COOPERATE
    else if cooperators_last_round > (n-1)/2:
        action = DEFECT
    else:
        action = COOPERATE
```

**Interpretation:**

In the final round, always defect—no future rounds exist to penalize extraction.

In earlier rounds, use three-tiered logic:

1. **Crisis threshold (stock < capacity/3):** Cooperate. The stock is dangerously depleted. The regeneration function 2S(1-S/capacity) peaks near capacity/2, but when stock drops below capacity/3, continued defection guarantees further collapse and eventual mutual ruin. Cooperating here slows depletion and allows recovery, preserving future extraction opportunities.

2. **Majority cooperation (>50% of others cooperated last round):** Defect. When most opponents are cooperating, the common pool is being sustained at higher levels. Defecting yields S/n while they sustain the stock with their cooperation—maximizing immediate payoff while the resource base remains healthy enough for future rounds.

3. **Majority defection or split (<50% cooperation):** Cooperate. Heavy defection by others indicates stock is under pressure. Continuing to defect accelerates mutual destruction. Cooperation here reduces total depletion and gives the stock a chance to regenerate. This is self-interested: preventing cascading collapse preserves future payoff opportunities that mutual defection would eliminate.

**Edge Cases:**

- **Round 1:** No history exists. Observe cooperators only after round 1 completes. Enter round 1 assuming stock = capacity (not in crisis), so the rule branches on majority cooperation—but since this cannot yet be observed, check the crisis threshold only. If capacity ≥ 2n and stock = capacity, this condition fails, so defect in round 1 (opportunistic opening).

- **Very small groups (n=2):** "Majority" requires strictly more than 0.5 opponents cooperating, meaning ≥1 cooperator. With one opponent, this is clear. The strategy remains consistent.

- **Stock exactly at capacity/3:** Use strict inequality; stock < capacity/3 is false, so proceed to cooperation-rate check.

This strategy is self-interested because it maximizes extraction when conditions allow, avoids pointless cooperation when defection is widespread, and prevents resource collapse that would reduce all future payoffs to zero.
'''

description_SELFINTERESTED_24 = '''
ADAPTIVE STOCK-DEPLETION STRATEGY

**Core Decision Logic:**

Compute three factors for each round t with current stock S:

1. **Stock Health**: health = S / capacity
2. **Temporal Urgency**: urgency = (r - t) / r  (approaches 0 as we near round r)
3. **Observed Cooperation Rate**: prior_coop = (number of cooperators observed in t-1) / (n-1)

**Decision Rule:**

```
IF t == 1:
  COOPERATE  // Establish cooperative signal; test opponent responses

ELSE IF health < 0.15:
  DEFECT  // Stock collapse imminent; extract maximum before pool dies

ELSE IF urgency < 0.15:
  DEFECT  // Final rounds; future payoffs negligible, pure extraction optimal

ELSE IF health < 0.35 AND prior_coop < 0.5:
  DEFECT  // Stock degraded and others defecting; don't leave value on table

ELSE IF health > 0.7 AND prior_coop >= 0.6:
  COOPERATE  // Stock abundant; many others cooperating; sustainable mutual extraction

ELSE IF health > 0.55 AND urgency > 0.4 AND prior_coop >= 0.4:
  COOPERATE  // Mid-game; stock decent; sufficient future rounds; reasonable opposition cooperation

ELSE:
  DEFECT  // All other conditions default to defection
```

**Edge Cases:**

- **Round 1**: Always cooperate to avoid signaling immediate defection when stock is at maximum and healthy play is most discoverable.
- **Rounds 2-3 (early game)**: Health and prior_coop thresholds favor cooperation if stock remains high, since most players will still be testing strategies.
- **Final round (t = r)**: Urgency = 0; always defect regardless of stock or observed cooperation, since no future exists.
- **Stock collapse (S → 0)**: Payoff becomes S/n → 0 anyway; defection vs cooperation irrelevant; defection chosen by default rule.
- **All opponents defect (prior_coop = 0)**: Cooperation threshold never met unless health > 0.7; otherwise defect.

**Rationale for Self-Interest:**

This strategy prioritizes extracting maximum payoff by defecting when stock cannot sustain high future returns (low health, few rounds left, low opponent cooperation). It cooperates only when the expected future payoff stream from stock sustainability exceeds the immediate extraction gain from defection—a direct self-interested calculus. The strategy abandons cooperation attempts once the game approaches its end, where the one-shot defection payoff dominates.
'''

description_SELFINTERESTED_25 = '''
# Strategy: Conditional Cooperation with Dynamic Defection Trigger

## Decision Rules

**Round 1:**
- Action: COOPERATE
- Rationale: Establish baseline observation of opponent behavior without committing to full cooperation.

**Rounds 2 to r-1:**
- Observe: stock level at round start and number of opponents who defected in previous round
- Calculate: defection_rate = (number of defectors last round) / (n - 1)
- Decision rule:
  ```
  if (stock ≥ capacity/2) AND (defection_rate ≤ 0.5):
    COOPERATE
  else:
    DEFECT
  ```
- Rationale: Maintain cooperation only when the resource is healthy (above 50% capacity) and defection remains minority behavior. Threshold at capacity/2 reflects the point where sustained all-cooperation preserves the resource; exceeding 50% defection indicates the cooperation equilibrium is breaking down, so extract value before collapse.

**Round r (final round):**
- Decision rule:
  ```
  if (stock > 0):
    DEFECT
  else:
    COOPERATE (yields 0 either way)
  ```
- Rationale: In the final round, there is no future stock preservation to incentivize. Maximize immediate payoff by defecting whenever the pool has remaining value. No other player's defection can punish you in round r.

## Edge Cases

- **Stock collapse:** If stock reaches 0 at any point before round r, switch to COOPERATE for all remaining rounds (both actions yield 0, so cooperation is costless and may signal willingness to rebuild if somehow stock regenerates—though unlikely given depletion).
- **n=2 case:** Defection_rate of 0 or 1; the 0.5 threshold means a single defector by the opponent triggers your defection. This is appropriate for 1v1 scenarios where one defection signals non-cooperation.
- **All-defect trap:** Once everyone defects, stock → 0 and stays there. Your switch to COOPERATE cannot change this, but it minimizes losses (0 vs 0).

## Self-Interest Alignment

This strategy prioritizes immediate payoff extraction while opportunistically exploiting resource sustainability. You cooperate precisely when conditions allow mutual gain (healthy stock, cooperative majority), but defect proactively when the commons is vulnerable to collapse or others are already taking more. The final-round defection ensures you capture maximum surplus before the game ends. Against rational self-interested opponents, this strategy exploits cooperation when available and abandons it before depletion becomes catastrophic.
'''

description_SELFINTERESTED_26 = '''
# Threshold-Based Adaptive Extraction Strategy

**Core Decision Rule:**

Compare current stock S against a dynamic sustainability threshold T_t computed at each round t:

```
T_t = 2n × max(1, (r - t) / 2)
```

IF S > T_t: DEFECT
ELSE: COOPERATE

**Rationale:**

- Early rounds (t ≈ 1): T_t is large relative to stock. Defect to extract maximum value while capacity abundance permits.
- Mid game: As t increases and stock depletes naturally, T_t remains substantial but defection becomes costlier in expectation.
- Late game (t ≈ r): T_t shrinks toward 2n. Defection dominates again because few remaining rounds make future stock irrelevant.
- The threshold penalizes overextraction when remaining rounds suggest stock cannot naturally recover before game end.

**Edge Cases and Adjustments:**

*Round 1:* Stock = capacity. Since capacity ≥ 2n by assumption, T_1 ≥ 2n. Stock always exceeds threshold. Defect unconditionally.

*Last round (t = r):* T_r = 2n. Only defect if S > 2n. With typical depletion from earlier defections, S is likely ≤ 2n by round r. Cooperate in final round if stock has collapsed, defect only if abundance persists.

*Stock at 0:* If stock reaches 0 from opponent defection waves, both actions yield 0. Cooperate (weakly dominated action causes no additional harm and avoids accelerating depletion if stock recovers).

**Adaptive Response to Observed Cooperation:**

Track the fraction of opponents who cooperated in round t−1, denoted f_coop. If f_coop > 0.5, reduce the threshold multiplier:

```
T_t = 2n × max(1, (r - t) / 2) × (0.8 + 0.2 × f_coop)
```

This exploits cooperative opponent clusters by maintaining slightly lower extraction thresholds, increasing joint sustainability and your cumulative payoff. If opponents are defecting heavily (f_coop < 0.5), revert to base threshold and extract aggressively while stock remains.

**Intuition:**

The strategy self-interestedly maximizes consumption by front-loading defection when stock is abundant (early rounds), then shifts toward conservation only when stock scarcity threatens collapse. It avoids the tragedy of commons while remaining primarily extractive.
'''

description_SELFINTERESTED_27 = '''
# ADAPTIVE THRESHOLD STRATEGY

## Core Decision Logic

Cooperate if and only if ALL of the following conditions hold; otherwise defect:

1. **Stock health**: `stock / capacity ≥ 0.35`
2. **Opponent cooperation rate** (from previous round): `cooperators_observed / (n-1) ≥ 0.5`
3. **Rounds remaining**: `rounds_remaining ≥ 2`

```
IF rounds_remaining == 1:
    DEFECT
ELSE IF stock/capacity < 0.2:
    DEFECT
ELSE IF stock/capacity < 0.35:
    DEFECT
ELSE IF rounds_remaining == 2:
    IF cooperators_observed / (n-1) >= 0.6:
        COOPERATE
    ELSE:
        DEFECT
ELSE:
    IF cooperators_observed / (n-1) >= 0.5:
        COOPERATE
    ELSE:
        DEFECT
```

## Edge Cases & Special Handling

**Round 1**: Cooperate. This seeds the game; you have no history and cannot distinguish opponent types yet.

**Last round** (round r): Always defect. No future rounds mean the pool's growth is irrelevant; extract maximum immediate value.

**Second-to-last round**: Cooperate only if opponent cooperation rate exceeded 60% previously; otherwise defect. The pool needs 2 growth cycles to recover, so this is your last chance to enforce cooperation.

**Critical stock** (stock/capacity < 0.2): Always defect. The pool is dying; continued cooperation won't restore it before collapse, so extract while possible.

**Stock collapse risk** (0.2 ≤ stock/capacity < 0.35): Defect regardless of opponent behavior. This threshold prevents the trap where you cooperate while opponents defect and drain the remaining stock.

## Rationale for Thresholds

The 50% opponent cooperation threshold balances two risks: if fewer than half the opponents are cooperating, the pool will deplete faster than it can grow (you extract while there's still stock). The 35% stock ratio is the minimum viable threshold where future growth might outpace simultaneous consumption by a mixed-strategy group.

The strategy prioritizes end-game and crisis behavior (last round, low stock, low opponent cooperation) to prevent getting locked into mutual depletion. It rewards environments with cooperative majorities by reciprocating, but penalizes defection-heavy environments by joining the extraction before the pool vanishes.
'''

description_SELFINTERESTED_28 = '''
**ADAPTIVE RECIPROCAL PRESERVATION STRATEGY**

**Round 1 (Initial):**
Cooperate. This establishes a cooperative signal and allows assessment of opponent types.

**Rounds 2 to r-1 (Adaptive Phase):**
Let c_t = number of opponents who cooperated in round t.

Base decision:
- IF c_t ≥ ⌈(n-1)/2⌉: Cooperate
- ELSE: Defect

Apply stock preservation override:
- IF stock < capacity/3: Defect (commons in critical decline, switch to extraction)
- IF stock ≥ capacity/3 AND stock < capacity/2: Cooperate only if c_t ≥ ⌈(n-1) × 0.6⌉ (higher bar for cooperation)

Apply exploitation detection adjustment:
- IF c_t = 0 (all opponents defected): Defect for next 2 rounds minimum, then reassess
- IF c_t ≤ 1 AND rounds remaining ≥ 3: Shift to defection until opponents show ≥ 50% cooperation in a round

**Round r (Final Round):**
Defect. No future stock matters; extract maximum current value since no regeneration benefits you.

**Edge Cases:**

*Stock collapse (stock → 0):* Defect for all remaining rounds (commons is dead, no gains from cooperation).

*Oscillating opponents:* If cooperation rate fluctuates around your threshold, stay with your current action for 2 rounds before switching (reduces noise sensitivity).

*Early endgame (rounds remaining ≤ 2):* Defect if stock < capacity/2, regardless of opponent behavior (not enough time to recover from cooperation losses).

**Rationale:** This balances exploitation of sustained cooperation against self-preservation when the commons deteriorates. It avoids sucker equilibria by detecting defection majorities early, maintains the resource when cooperation is reciprocated, and abandons cooperation only when the commons is damaged or opponents demonstrate sustained defection.
'''

description_SELFINTERESTED_29 = '''
# Stock-Threshold Conditional Cooperation

**Decision Rule:**

For round t (where t ≤ r):

1. **Last Round Exception:** If t = r:
   - Play D if stock > 0 (extract maximum single-round payoff)
   - Play C if stock = 0 (irrelevant, but C is weaker consumption claim)

2. **Stock-Level Thresholds (all other rounds):**
   - Play C if stock ≥ 0.5 × capacity
   - Play D if stock < 0.5 × capacity

3. **Cooperation Rate Modifier:** If t > 1:
   - If stock ≥ 0.5 × capacity AND observed_cooperators_last_round ≥ 0.75 × n: Play C
   - If stock ≥ 0.5 × capacity AND observed_cooperators_last_round < 0.5 × n: Play D (defectors are dominating)
   - If 0.25 × capacity ≤ stock < 0.5 × capacity AND observed_cooperators_last_round ≥ 0.9 × n: Play C (rescue attempt)
   - Otherwise: Play D

**First Round:** Play C (stock is at capacity; cooperation is stable at full capacity).

**Rationale:**

- Capacity/2 is the stock level where logistic growth is maximized—cooperation at this level preserves the resource indefinitely.
- Above this threshold, mutual cooperation sustains collective payoffs. Defection above this threshold trades long-term resource stability for a one-round 2× gain, which is irrational when stock preservation yields repeated gains.
- Below this threshold, the resource is already collapsing; continuing to cooperate only delays inevitable depletion. Switching to defection exits the tragedy.
- The cooperation-rate modifier prevents free-riding: if fewer than 50% of opponents cooperate despite healthy stock, the environment is exploitative and cooperation becomes futile.
- Last-round defection extracts residual value from an already-determined stock level and avoids the backward-induction vulnerability of cooperating when no future rounds exist.
- This strategy is self-interested: it maximizes individual payoff by (a) sustaining collective resource when mutual cooperation is stable, (b) abandoning a doomed resource to capture personal gains, and (c) protecting against exploitation by defectors.
'''

description_SELFINTERESTED_30 = '''
**STOCK-CONDITIONAL ADAPTIVE STRATEGY WITH END-GAME DEFECTION**

**Decision Rule by Round:**

**Last round (t = r):** Defect unconditionally. No future stock matters; maximize immediate consumption.

**First round (t = 1):** Cooperate. Without history, the safe play is to preserve the initial capacity and avoid triggering a defection spiral immediately.

**Rounds 2 to r-1:** Use stock level and observed opponent behavior to decide.

Let:
- stock_ratio = current_stock / capacity
- opp_coop_count = number of opponents observed cooperating in previous round
- opp_coop_rate = opp_coop_count / (n - 1)
- rounds_remaining = r - t

Decision logic:

```
IF stock_ratio ≤ 0.35:
  → Cooperate  // Critical preservation: stock is dangerously depleted
  
ELSE IF stock_ratio > 0.65:
  → Defect  // Abundance: exploit high stock, growth will replenish
  
ELSE:  // Intermediate stock (0.35 < stock_ratio ≤ 0.65)
  IF opp_coop_rate ≥ 0.5 AND rounds_remaining > 2:
    → Defect  // Opponents are sustaining stock, safe to exploit
  ELSE IF opp_coop_rate < 0.3:
    → Cooperate  // Heavy opponent defection: must preserve or stock collapses
  ELSE:
    → Defect  // Marginal case: slight positive defection bias for self-interest
```

**Edge Cases:**

- **Stock near zero (stock < 2n):** Cooperate regardless of round number except the last round, where you defect because the resource is already lost.
- **All opponents defected previous round:** If stock_ratio > 0.4, still defect (extract value before collapse). If stock_ratio ≤ 0.4, cooperate.
- **n = 2:** Use the same thresholds; opp_coop_rate is binary (0 or 1).

**Rationale:**

This strategy prioritizes self-interest through three mechanisms: (1) default defection in the absence of urgency, (2) rational preservation when depletion threatens future payoffs, and (3) exploitation of opponent cooperation when sustainable. The last-round defection captures the finality effect. The first-round cooperation avoids immediate tragedy and is self-interested because it preserves the high-value early-round payoff base.
'''

description_SELFINTERESTED_31 = '''
**ADAPTIVE THRESHOLD STRATEGY WITH ECOSYSTEM MONITORING**

**Decision Rule:**

In round t with stock S_t, opponent cooperation count c_t, and R remaining rounds:

1. **First round:** Cooperate (gather information on opponent behavior)

2. **Critical depletion check:** If S_t ≤ 0.15 × capacity, Defect (ecosystem collapsing—cooperation becomes futile)

3. **Final round:** If R = 1, Defect (no future benefit from maintaining stock)

4. **Standard case:** Calculate adaptive cooperation threshold:
   - opponent_coop_rate = c_t / (n - 1)
   - ecosystem_health = S_t / capacity
   - rounds_discount = R / r (weight to future payoffs)
   - required_threshold = 0.45 + 0.35 × (1 - ecosystem_health) - 0.25 × rounds_discount
   
   - If opponent_coop_rate ≥ required_threshold: Cooperate
   - Else: Defect

**Edge Cases:**

- **Round 2 onwards with all-defect history:** If c_t = 0 for three consecutive rounds, switch to permanent Defect (herd has broken)
- **Mid-cycle stock recovery:** If stock rises to 0.8+ capacity after dip and opponent cooperation ≥ threshold, resume cooperation
- **Opponent coordination anomaly:** If cooperation suddenly spikes to >75% after rounds of near-zero, reset threshold temporarily (trial cooperation for 2 rounds)

**Rationale:**

The strategy balances self-interest through:
- **Opportunistic defection:** Punish free-riders by defecting when opponents don't cooperate sufficiently
- **Calculated cooperation:** Cooperate strategically when opponent behavior suggests the resource can sustain growth—which ultimately feeds your future payoffs
- **Time-discounting:** Shift toward defection as rounds remaining shrink, since maintaining stock becomes less valuable
- **Salvage detection:** Abandon cooperation if stock crashes below viability threshold

This maximizes total payoff by avoiding symmetric all-defect collapse when feasible, while protecting against exploitation.
'''

description_SELFINTERESTED_32 = '''
**Adaptive Exploitation with Late-Round Aggression**

**Decision Rule by Round and State:**

Round 1:
- Cooperate. This reveals baseline opponent behavior without foregoing significant gains (high stock available).

Rounds 2 through r-2 (all middle rounds):
- Observe the cooperation rate: c = (number of opponents who played C last round) / (n-1)
- Cooperate if and only if: **c ≥ 0.5 AND stock > capacity/2**
- Otherwise defect.

Rationale: Cooperate only when a majority of opponents cooperated AND sufficient stock remains to grow back. If cooperation is weak, defect immediately rather than subsidize exploitation. If stock depleted, defect because the resource is already doomed.

Rounds r-1 and r (final two rounds):
- Defect unconditionally. In the last round, defection strictly dominates cooperation (no future rounds to decay). In the penultimate round, the final-round defection incentive is strong enough that opponent cooperation cannot be sustained, so preempt.

**Edge Case: Stock Approaching Zero**

If stock < 2n at any non-final round, defect. Stock is too depleted to recover meaningfully, so pursue immediate consumption. Continuing to cooperate under depletion only reduces your payoff without restoring the pool.

**Implementation Notes:**

- The 0.5 threshold is deliberate: majority cooperation suggests sustainability is possible; minority cooperation means you're absorbing others' exploitation.
- The capacity/2 checkpoint prevents overcommitting to cooperation when stock depletion is already severe.
- Defection in final rounds is unambiguous self-interest: you cannot be punished in a round that doesn't exist.
'''

description_OPPORTUNISTIC_5 = '''
**STOCK MONITORING WITH ADAPTIVE THRESHOLDS**

**Round 1:**
Play D. Initial stock is at capacity; defection maximizes immediate value with minimal risk of collapse in a single round.

**Round t ∈ {2, ..., r-1}:**

1. Observe stock level S_t and count of cooperators c_t from previous round (equivalently, defectors d_t = n - c_t)

2. Compute stock ratio: ρ_t = S_t / capacity

3. Decision rule:

   - **If ρ_t ≥ 0.6:** Play D
     - Stock is sufficiently abundant; regeneration will sustain it even under moderate defection. Exploit.

   - **If ρ_t ∈ [0.3, 0.6):** 
     - Estimate sustainability: If c_t ≥ ⌈n/3⌉, play D; otherwise play C
     - Rationale: With sufficient cooperators visible, the pool is being managed and can support one additional defector. Below that threshold, defection risks cascade collapse.

   - **If ρ_t < 0.3:**
     - Remaining rounds δ = r - t
     - If δ ≤ 2, play D (insufficient rounds to recover; extract what remains)
     - Else if c_t ≥ ⌈2n/3⌉, play D (strong cooperator majority can absorb your defection)
     - Else play C (prevent extinction; stabilize stock for future extraction)

**Final Round (t = r):**
Play D unconditionally. No future stock considerations apply; extract maximum value.

**Edge case - stock at 0:**
Play D. Payoff is zero regardless; defection preserves consistency with decision logic.
'''

description_OPPORTUNISTIC_6 = '''
# Adaptive Threshold Opportunism

**Decision Rule by Stock Level:**

Defect if and only if:
- `stock > threshold(round, r)`

Otherwise cooperate.

Where threshold evolves as:
```
baseline_threshold = capacity / 2.5
rounds_remaining = r - current_round
pressure_factor = max(0, 1 - (2 * rounds_remaining / r))

threshold = baseline_threshold * (1 + 0.4 * pressure_factor)
```

**Opportunistic Refinement — Condition on Opponent Cooperation:**

After observing how many opponents cooperated in the previous round (opponent_coop_count):

- If `opponent_coop_count ≥ (n-1)/2`: Defect if `stock > threshold` (exploit their collective effort)
- If `opponent_coop_count < (n-1)/2` and `stock > 1.5 * capacity / 2`: Defect anyway (stack exploitation on their defection while stock permits)
- If `opponent_coop_count < (n-1)/2` and `stock ≤ 1.5 * capacity / 2`: Cooperate (forced recovery phase)

**Edge Cases:**

- **Round 1:** Defect. Stock is at capacity; exploitation is optimal with no history to constrain you.
- **Final round (t = r):** Defect if `stock > capacity/3`, else cooperate. No future rounds exist, so there is no recovery cost to defection, but also no reason to maintain stock beyond this round.
- **Stock near zero:** Cooperate regardless of round (defection yields near-zero payoff anyway; cooperation maximizes regeneration).
- **Stock at capacity:** Defect unless only one round remains, in which case defect anyway.

**Rationale:**

This strategy exploits high-abundance periods by defecting, extracting twice the payoff when the commons can absorb it. As stock declines or time pressure mounts, it shifts toward cooperation—not from altruism, but from the opportunistic recognition that stock recovery increases future exploitation potential. It opportunistically stacks defections when enough opponents have already depleted the commons (riding their damage), while switching to cooperation only when forced recovery is necessary to maintain any payoff stream.
'''

description_OPPORTUNISTIC_7 = '''
## Adaptive Extraction Strategy

**Core Logic:**
Defect when stock is abundant to maximize personal payoff, cooperate only when forced by resource scarcity or when opponents' cooperation rate is sufficiently high to sustain mutual benefit.

**Decision Rule (for round t > 1):**

```
if (t == r) or (r - t <= 1):
    // Endgame: final 1-2 rounds, extract maximum
    action = DEFECT
    
else if stock <= 0.3 × capacity:
    // Stock critically depleted; cooperation is damage control
    action = COOPERATE
    
else if stock >= 0.7 × capacity:
    // Stock abundant; exploit at maximum
    action = DEFECT
    
else:  // stock in (0.3, 0.7) × capacity
    // Intermediate zone: condition on opponent behavior
    coop_rate = observed_cooperators_last_round / (n - 1)
    if coop_rate >= (2/3):
        action = COOPERATE
    else:
        action = DEFECT
```

**First Round:** 
DEFECT unconditionally. Stock is at capacity; this is the highest-value moment to extract. Test opponent behavior without commitment.

**Observed Cooperators Tracking:**
Count how many of the n-1 other players cooperated in the immediately preceding round. Use this to calibrate the (2/3) threshold: when at least two-thirds of opponents cooperate, participate in the stable cooperative equilibrium; otherwise free-ride.

**Edge Cases:**

- **Stock = 0:** Continue to DEFECT (game is already lost; no benefit to cooperating).
- **Single round remaining (t = r):** DEFECT. No future payoff exists; extract the final payoff regardless of stock level.
- **Stock exactly at thresholds:** Use strict inequalities. At stock = 0.7 × capacity, defect; at stock = 0.3 × capacity, cooperate.
- **Unobserved first round:** Assume all opponents played their strategy independently; do not infer any signal.

**Opportunistic Stance:**
This strategy abandons cooperation as soon as stock recovers, exploits windows of abundance, and only sustains cooperation instrumentally—when opponent behavior guarantees resource stability. It treats the common pool as a resource to extract from efficiently, not a shared responsibility to steward.
'''

description_OPPORTUNISTIC_8 = '''
**OPPORTUNISTIC POOL EXTRACTION STRATEGY**

**Decision Framework:**

Play D (defect) by default. Transition to C (cooperate) only when one of two conditions triggers: (1) the stock has declined to critical levels, or (2) the final round is imminent and defection in earlier rounds has already extracted maximum value.

**Round-Specific Rules:**

*Round 1 (Initial):*
Play D. Establish aggressive posture immediately and signal willingness to consume. This yields immediate high payoff (stock/n) and generates a baseline observation of how many opponents will cooperate despite defection.

*Rounds 2 through r-1 (Accumulation Phase):*
- If stock ≤ capacity/3: Switch to C. At this depletion level, the regenerative capacity of the pool becomes the bottleneck. Consuming less allows recovery. Only cooperate here if observed_cooperators ≥ (n-1)/3; if fewer than that cooperated last round, the pool is already doomed, so defect until it collapses.
- If stock > capacity/3: Play D unconditionally. Extract aggressively while the pool can sustain growth. The observation of opponent cooperation levels is irrelevant—exploit cooperators' restraint regardless of how many there are. Their cooperation refunds the pool; your defection captures the surplus.

*Round r (Final Round):*
Play D unconditionally. No future rounds exist, so the stock regeneration game ends. Maximize this final capture. If stock ≥ capacity/4, you gain stock/n; if lower, you extract whatever remains. Defection is strictly dominant in the final round.

**Edge Case: Stock Collapse:**

If stock < capacity/4 and you observe cooperators_last_round < (n-1)/4, the pool is functionally dead. Defect anyway—attempting cooperation cannot resuscitate a pool drained by mass defection.

**Opportunistic Logic:**

This strategy extracts maximum value from any cooperators present during the abundance phase, free-rides on their restraint, and switches to cooperation only as a salvage tactic when your prior defection has made cooperation necessary for any future extraction.
'''

description_OPPORTUNISTIC_9 = '''
## Opportunistic Threshold Strategy

**State Tracking:**
Maintain a history of observed opponent cooperation counts from previous rounds. Compute the running average of opponents cooperating: `avg_coop_opponents`.

**Decision Rule:**

```
if round == 1:
    action = DEFECT

else if round == r (final round):
    action = DEFECT

else:
    stock_ratio = stock / capacity
    cooperation_rate = avg_coop_opponents / (n - 1)
    rounds_remaining = r - current_round
    
    // Tier 1: Aggressive defection when stock is abundant
    if stock_ratio >= 0.50:
        action = DEFECT
    
    // Tier 2: Terminal endgame (last 2 rounds defect)
    else if rounds_remaining <= 2:
        action = DEFECT
    
    // Tier 3: Exploit cooperative opponents at moderate stock
    else if cooperation_rate >= 0.55 and stock_ratio >= 0.30:
        action = DEFECT
    
    // Tier 4: Match defection wave (if opponents mostly defect)
    else if cooperation_rate <= 0.40:
        action = DEFECT
    
    // Tier 5: Stock recovery threshold
    else if stock_ratio < 0.15 and cooperation_rate >= 0.65:
        action = COOPERATE  // Cooperate only to sustain stock for future exploitation
    
    // Tier 6: Default to cooperation for monitoring
    else:
        action = COOPERATE
```

**Edge Cases:**

- **Round 1:** Always defect to immediately capture value and probe opponent types.
- **Final round:** Always defect—no future consequences.
- **Stock collapse (< 15% capacity):** Defect unless opponents are highly cooperative (≥65%), in which case cooperate minimally to preserve the pool for subsequent exploitation.
- **Stock depletion mid-game:** Accelerate defection; prioritize extracting remaining resources over long-term sustainability.

**Opportunistic Logic:**
The strategy front-loads defection while stock is high, exploits detected cooperation, matches opponent defection to avoid unilateral cooperation losses, and pivots to selective cooperation only when stock recovery directly enables future extraction opportunities.
'''

description_OPPORTUNISTIC_10 = '''
# Opportunistic Exploitation Strategy

## Core Decision Rule

In round t, defect if any of the following conditions hold; otherwise cooperate.

```
if round == 1:
  return DEFECT

else if round >= r - ceil(r/4):  // final quarter of rounds
  return DEFECT

else if stock < capacity/2:  // resource is degraded
  return DEFECT

else if observed_cooperators_last_round >= (n-1) * (0.5 + 1/n):
  return DEFECT  // exploit high cooperation

else:
  return COOPERATE  // test whether cooperation persists
```

## Detailed Logic

**Initialization (Round 1):**
Defect unconditionally. Establish an opportunistic baseline and probe whether the environment rewards defection.

**End-Game (Final ~25% of rounds):**
Defect unconditionally. Future stock regeneration becomes negligible, so maximizing immediate consumption dominates.

**Stock Depletion Condition:**
If stock ≤ capacity/2, the resource has already been heavily exploited. Defect to maximize personal extraction before further collapse, since the commons is already compromised.

**Exploitation Trigger:**
If ≥ 50% of opponents cooperated in the previous round, defect. This extracts maximum value when others maintain restraint. The threshold is 0.5 + 1/n (slightly above majority) to account for noise—require clear evidence of widespread cooperation before passing up the defection payoff.

**Adaptive Cooperation:**
If cooperation is lower than the trigger, play cooperate opportunistically. This serves two purposes: (1) if opponents shift to cooperation due to past low defection rates, you capture shared growth; (2) if defection is universal anyway, maintaining cooperation does not worsen outcomes significantly, preserving stock for later rounds when exploitation may resume.

## Edge Cases

- **Round 2:** Apply standard rule. If round 1 was all defection (likely), opponents probably defect; defect again.
- **Last round (t = r):** Always defect, regardless of observed behavior.
- **Stock at capacity:** No special behavior—apply standard rules; high stock makes defection payoffs attractive.
- **Stock ≤ 2n (near zero):** Defect; the game is collapsing and individual extraction is the rational response.
'''

description_OPPORTUNISTIC_11 = '''
# Adaptive Opportunistic Strategy

## Decision Rule Framework

Cooperate vs. Defect based on three observed conditions: **stock health**, **observed cooperation rate**, and **game phase**.

### Core Logic

**For rounds 1 to r:**

```
stock_ratio = current_stock / capacity
coop_ratio = (number of cooperators in previous round) / (n - 1)
rounds_remaining = r - current_round

Phase determination:
  if rounds_remaining ≤ 2: phase = ENDGAME
  else: phase = MIDGAME

Decision tree:

if phase == ENDGAME:
  action = DEFECT

else if stock_ratio < 0.25:
  action = COOPERATE

else if coop_ratio ≥ 0.55:
  action = DEFECT
  
else if stock_ratio < 0.50 AND coop_ratio < 0.35:
  action = COOPERATE
  
else:
  action = DEFECT
```

## Edge Case Handling

**Round 1:** Play DEFECT. This provides immediate payoff maximization and probes whether the environment is sustainable.

**Round 2:** First time observing aggregated behavior. If round 1 shows near-total defection, coop_ratio ≈ 0; if many cooperated, coop_ratio > 0. Apply standard midgame logic.

**Last 2 rounds:** Automatically DEFECT regardless of pool state or cooperation rates. Future repercussions no longer matter.

**Threshold for defecting on cooperation:** Defect when coop_ratio ≥ 0.55, meaning more than half of opponents cooperated. This is the exploitation window.

**Recovery trigger:** If stock falls below 25% of capacity, force cooperation to allow regeneration, overriding exploitation incentives.

**Stability safeguard:** If stock is medium-low (25-50%) AND most opponents are also defecting (coop_ratio < 35%), cooperate to prevent mutual collapse while the pool is not yet critical.

## Opportunistic Alignment

This strategy prioritizes **immediate exploitation** when conditions permit: defect whenever observing high cooperation from others, extracting S/n instead of S/2n. It shifts to cooperation only under resource scarcity—a tactical adaptation rather than a principled commitment. The endgame pivot to pure defection maximizes final-round payoffs without penalty. Between these anchors, it remains sensitive to pool depletion risk, cooperating only when necessary for sustainability, ensuring the resource doesn't collapse before payoff extraction is complete.
'''

description_OPPORTUNISTIC_12 = '''
# Opportunistic Stock-Exploitation Strategy

**Core principle**: Maximize immediate extraction while preventing pool collapse that would eliminate future rounds.

## Decision Rule by Round

**Last round (t = r)**:
Always defect. No future rounds exist; cooperation provides no benefit.

**First round (t = 1)**:
Defect. Stock is at maximum capacity, safe for extraction. Assume opponents may cooperate, creating an opportunity to free-ride.

**Rounds 2 to r-1**:
Use a two-stage decision rule based on stock health and opponent behavior.

## Stock Health Assessment

Calculate a safety threshold:
```
safe_threshold = max(4n, 0.3 × capacity)
danger_threshold = max(2n, 0.15 × capacity)
```

After each round, compute the realized total consumption by observing remaining stock. Estimate opponent cooperation rate as:
```
observed_cooperators = (stock_initial - stock_after - net_growth) / (stock_initial/(2n)) [adjusted for your action]
```

Track a rolling cooperation rate of other players: `coop_rate = observed_cooperators / (n-1)`

## Defection vs. Cooperation

**If stock ≥ safe_threshold**:
- Defect unconditionally. The pool has sufficient buffer for recovery even with widespread defection. This is risk-free exploitation.

**If danger_threshold ≤ stock < safe_threshold**:
- Defect if coop_rate > 0.5 (opponents are cooperating, free-ride on their restraint)
- Cooperate if coop_rate ≤ 0.5 (mutual defection trajectory; preserve stock to avoid complete collapse)

**If stock < danger_threshold**:
- Cooperate. The pool faces collapse risk. Force recovery through reduced extraction, enabling future rounds where you can exploit again.

## Opportunistic Twist

Track stock trajectory: If stock declined more than expected in the last round despite your cooperation, opponents are defecting heavily. In the next round, switch to defection to compete directly for extraction before the pool dies.

Never cooperate twice in a row if the preceding round showed no stock recovery—this signals a failed cooperation attempt and you should revert to extraction.
'''

description_OPPORTUNISTIC_13 = '''
# Opportunistic Adaptive Extraction Strategy

**Decision Framework:**

Cooperate if and only if at least one of these conditions holds:
1. Stock level is critically low: `stock ≤ 1.5n`
2. Stock is moderate AND cooperation rate is very high: `stock ≤ 1.5×capacity AND observed_coop_rate ≥ (n-1)/n`

Otherwise, defect.

**Detailed Decision Rule:**

```
function decide(stock, round, n, r, observed_cooperators):
  remaining_rounds = r - round
  
  // Critical preservation threshold
  if stock ≤ 1.5n:
    return COOPERATE
  
  // Stock health assessment
  stock_ratio = stock / capacity
  
  // Late-stage aggression (final 20% of rounds)
  if remaining_rounds ≤ ceil(0.2 × r):
    return DEFECT
  
  // Exploit when stock is abundant
  if stock ≥ 1.3 × capacity:
    return DEFECT
  
  // Conditional defection based on observed cooperation
  cooperating_opponents = observed_cooperators
  defecting_opponents = (n - 1) - cooperating_opponents
  
  // If many are cooperating, exploit them
  if cooperating_opponents ≥ 0.6 × (n - 1):
    return DEFECT
  
  // If stock is high and others are also defecting, still defect
  if stock_ratio ≥ 0.7:
    return DEFECT
  
  // Low cooperation rate with moderate stock: defect
  if cooperating_opponents ≤ (n - 1) / 3:
    return DEFECT
  
  // Fallback: cooperate only if truly many are cooperating AND stock is moderate
  return COOPERATE
```

**Edge Cases:**

- **Round 1:** Defect immediately (high initial stock enables aggressive extraction; no history to learn from).
- **Final round:** Always defect (no future stock benefit, maximize immediate extraction).
- **Stock collapse (stock < n):** Cooperate unconditionally; the pool is near-useless regardless, but cooperation costs less.
- **Perfect cooperation observed (all n-1 opponents chose C):** Defect aggressively; this is exploitation of trust.

**Opportunistic Characteristics:**

- Extracts maximum value during high-stock periods when stock growth can offset consumption.
- Shifts from conditional to unconditional defection in final rounds (no forward incentive).
- Monitors opponent behavior to identify periods of high cooperation, then exploits those windows.
- Uses stock thresholds to identify when cooperation serves self-interest (avoiding complete depletion that stops future extraction).
- Never punishes or reward-matches opponents; only responds to current state and aggregate behavior.
- Prioritizes personal payoff accumulation over resource sustainability except where collapse eliminates future extraction potential.
'''

description_OPPORTUNISTIC_14 = '''
# Opportunistic Adaptive Stock Strategy

## Decision Rule

Each round, observe k = number of other players who cooperated in the previous round (k = 0 in round 1).

Calculate:
- Estimated cooperation rate: p = k / (n - 1)
- Rounds remaining (including current): R = r - current_round + 1
- Current stock level: S
- Stock sustainability threshold: S_safe = capacity / 4

**Defect if:**
- R ≤ 2 (final two rounds: harvest before game ends)
- S ≥ 1.5 × capacity / 2 (stock is well above optimal growth point, room to overexploit)
- p ≤ 1/n (cooperation among opponents is negligible, defection won't trigger collective collapse)

**Cooperate if:**
- S ≤ S_safe AND p < 0.5 (stock dangerously low and insufficient cooperation to sustain recovery)
- S ≤ capacity / 3 AND R ≥ 3 (early depletion with many rounds left; preserve stock for future extraction)

**Otherwise, defect** (default opportunistic action)

## Edge Cases

**Round 1:** Defect. No historical information; take maximum immediate payoff.

**Last round (round r):** Defect unconditionally. No future stock to preserve.

**Stock collapse (S < 0.01):** Cooperate once. Allows one round of growth recovery before resuming defection. If stock remains near zero after cooperation, defect thereafter (pool is dead).

**All opponents defected (k = 0) every round:** Defect. Environment is zero-cooperation; exploitation is symmetric.

**All opponents cooperated (k = n-1) for 2+ consecutive rounds:** Defect hard. Cooperators have revealed predictability; exploit the stable surplus they maintain.

## Adaptive Thresholds

If R ≤ 3 (endgame): Lower S_safe to capacity / 6. Time pressure overrides stock preservation.

If p ≥ 0.7 (high cooperation observed): Tighten defection trigger to S ≥ 1.2 × capacity / 2. Exploit cooperators while they sustain stock.

If p ≤ 0.2 (low cooperation observed): Defect more aggressively unless S is critical. Expect stock to degrade anyway.

## Execution Priority

1. Check final round → defect
2. Check stock collapse → cooperate once
3. Check cooperation-rate dominance conditions → defect
4. Check stock-preservation conditions → cooperate
5. Default → defect
'''

description_OPPORTUNISTIC_15 = '''
# Opportunistic Adaptive Depletion Strategy

**Core Principle:** Extract maximum value while defending against stock collapse. Defect opportunistically when stock is robust; cooperate minimally only when necessary to preserve future extraction opportunities.

## Decision Rule

```
if stock ≤ 0.25 × capacity:
    return COOPERATE  // Critical recovery mode
else if round ≥ r - 1:
    return DEFECT  // Endgame extraction
else if round == 1:
    return DEFECT  // Establish aggressive posture with high stock
else if stock ≥ 0.65 × capacity:
    // Stock is healthy — exploit aggressively
    if observed_cooperators ≥ 0.5 × (n - 1):
        return DEFECT  // Undercut cooperators
    else:
        return DEFECT  // Match defection or defect harder
else if stock ≥ 0.4 × capacity and stock < 0.65 × capacity:
    // Moderate stock — opportunistic mixed response
    cooperation_rate = observed_cooperators / (n - 1)
    if cooperation_rate ≤ 0.25:
        return DEFECT  // Mutual defection accepted
    else if cooperation_rate ≥ 0.5:
        return DEFECT  // Exploit cooperators before they learn
    else:
        return COOPERATE  // Stabilize for next exploitation cycle
else:
    // Stock 0.25–0.4 × capacity: precarious zone
    return COOPERATE  // Build stock for future defection rounds
```

## Edge Cases

**Round 1:** Defect unconditionally. Stock is maximal; test whether a sustainable equilibrium exists and gain immediate value.

**Final round (round = r):** Defect unconditionally. No future payoff to protect.

**Penultimate round (round = r - 1):** Defect. Current-round extraction dominates concern for round r stock.

**Stock collapse (stock ≤ 0):** Not possible under this rule because cooperative recovery initiates when stock ≤ 0.25 × capacity, triggering growth before extinction.

**All opponents defected last round (observed_cooperators = 0):** In healthy stock conditions, defect and match their strategy. In precarious conditions, still cooperate to rebuild (stock threshold overrides).

**All opponents cooperated last round (observed_cooperators = n - 1):** If stock ≥ 0.65 × capacity, defect aggressively to maximize individual share. This undercuts their cooperation.

## Opportunistic Character

The strategy is explicitly **extraction-focused**: it defaults to defection and reserves cooperation only as a tactical necessity to avoid stock extinction that would eliminate future payoffs. The approach treats high cooperation by opponents not as a signal for reciprocal cooperation, but as an opening to defect and capture more of a healthy resource. It accepts mutual defection in mid-game when stock remains above the critical threshold, betting that some recovery occurs. Cooperation is purely instrumental—a mechanism to reset the stock for resumption of opportunistic defection, not a commitment to sustainability.
'''

description_OPPORTUNISTIC_16 = '''
# Opportunistic Threshold Strategy

## Decision Rule

Play **Defect** by default in each round, except in these situations:

1. **Critical Stock Threshold**: Cooperate if `stock < 0.2 × capacity`

2. **Last Round Preservation**: If `round = r` and `stock < 0.4 × capacity`, Cooperate (no recovery possible)

3. **Stock Depletion Spiral**: If `stock < 0.3 × capacity` and `cooperators_last_round ≤ (n/4)`, Cooperate (exploitation is inefficient when stock is low and cooperation is sparse)

Otherwise, **Defect**.

## Heuristic Refinement (Opportunistic Modulation)

For middle-game rounds when stock is healthy (0.3 ≤ stock ≤ 0.7 × capacity):

- If `cooperators_last_round ≥ ceil(3n/4)`: Defect aggressively (highly cooperative opponents are exploitable)
- If `cooperators_last_round ≤ floor(n/4)`: Defect (exploitation opportunity small, but stock might collapse—pivot toward cooperation sooner per rule 3 above)
- Otherwise: Defect

## First Round

Defect. Test the environment; assume others may cooperate. Establish an opportunistic posture early.

## Edge Cases

- **Stock = 0**: Forced outcome is zero payoff regardless of action; Cooperate (eliminates defection advantage)
- **Stock between rules**: Apply highest-priority rule from above (Critical > Last Round > Depletion > Standard Defect)
- **No history (round 1)**: No `cooperators_last_round` data; use Critical and Last Round rules; otherwise Defect

## Opportunistic Logic

This strategy prioritizes personal payoff by:
- **Defaulting to defection** when stock enables it (doubling consumption vs. cooperation)
- **Exploiting cooperation** when opponents play C at high stock levels
- **Switching to cooperation only when defection becomes self-defeating** (low stock makes double consumption worthless; stockpile protection becomes rational)
- **Adapting to collapse risk** only at the margin (cooperate minimally when necessary to prevent zero-payoff cascades)
- **Ignoring moral restraint**—cooperation emerges as instrumental survival, not preference
'''

description_OPPORTUNISTIC_17 = '''
**OPPORTUNISTIC ADAPTIVE EXTRACTION STRATEGY**

**Round 1:**
Cooperate. Gather baseline information about opponent behavior patterns with no prior history to condition on.

**Rounds 2 to r-1 (Middle Game):**
Let d_prev = number of opponents observed defecting in the immediately preceding round
Let defection_rate = d_prev / (n-1)
Let stock_ratio = stock / capacity

Defect if **any** of the following hold:
- stock_ratio ≥ 0.75 (stock is abundant; safe to extract aggressively)
- stock_ratio ≥ 0.60 **AND** defection_rate ≤ 0.35 (healthy stock with many cooperators visible—exploit them)
- defection_rate ≥ 0.70 **AND** stock_ratio ≥ 0.40 (widespread defection means the cooperative regime is breaking; defect before stock crashes)

Otherwise, Cooperate.

**Final Round (t = r):**
Defect unconditionally. The pool does not regenerate after this round, so long-term stock preservation has no value. Extract maximum immediate payoff.

**Edge Case: Stock Collapse (stock ≤ capacity × 0.25):**
Cooperate for one round to allow regeneration, regardless of other conditions. Defecting on an empty or near-empty pool yields negligible payoff. Restoring stock creates future extraction opportunities.

**Rationale:**
This strategy exploits information asymmetry by observing aggregate defection and targeting high-payoff states (high stock + low observed defection). It opportunistically shifts from extraction to preservation only when collapse is imminent or when defection becomes widespread enough to signal that the commons is being pillaged. The final round defection locks in the gains from earlier rounds while avoiding any punishment in future rounds that do not exist.
'''

description_OPPORTUNISTIC_18 = '''
# OPPORTUNISTIC ADAPTIVE STRATEGY

**Core principle**: Maximize immediate extraction while adapting only when resource depletion threatens payoff entirely.

## DECISION RULES

**Default action: Always Defect**

Override to Cooperate only if ALL three conditions are satisfied:
1. Stock level ≤ 0.25 × capacity (resource severely depleted)
2. Rounds remaining ≥ 3 (enough future to recover)
3. Observed cooperators in previous round ≥ 0.6n (others are sustaining the stock)

## EDGE CASES & ADAPTATIONS

**Round 1**: Defect unconditionally. Exploit the full starting capacity immediately.

**Last round (t=r)**: Defect unconditionally. No future payoffs exist; extract maximum from remaining stock.

**Stock collapse imminent** (stock ≤ 0.1 × capacity): 
- If you have observed ≥0.5n cooperators in any of the last 2 rounds: Cooperate to signal sustainability and potentially trigger cooperative rebuilding
- If mostly defectors observed: Defect anyway (recovery impossible, extract remainder)

**Mid-game with high defection** (>0.5n opponents defected last round):
- Defect (race to extract before resource exhaustion; matching others' exploitation)

**Stock critical but rounds exhausted** (stock ≤ 0.2 × capacity AND rounds remaining ≤ 2):
- Defect (final extraction; cooperation yields insignificant recovery)

## OPPORTUNISTIC ALIGNMENT

This strategy prioritizes:
- **Immediate gain extraction** over resource preservation (defect-by-default)
- **Exploitation of cooperators** when stock permits (take the larger share)
- **Conditional sustainability** only when forced: cooperate momentarily when resource collapse would eliminate future payoffs entirely, and only if others are already rebuilding
- **Competitive escalation** matching or exceeding opponent defection rates
- **Time-sensitive opportunism** intensifying defection as rounds exhaust
'''

description_OPPORTUNISTIC_19 = '''
# Opportunistic Adaptive Strategy

**Core Logic**: Defect as default when conditions permit, shift to cooperation only when resource preservation is critical or immediate exploitation diminishes.

## Decision Rules

**Each round, calculate:**
- cooperation_rate = (number of cooperators last round) / (n - 1)
- stock_health = stock / capacity
- rounds_remaining = r - current_round

**Action selection (in priority order):**

1. **Crisis preservation**: If stock_health < 0.2, play C
   - Pool is collapsing; further defection yields diminishing returns

2. **Endgame calculation**: If rounds_remaining ≤ 2
   - If stock_health > 0.5: Play D (final extraction while viable)
   - Else: Play C (preserve terminal payoff)

3. **Exploitation opportunity**: If cooperation_rate > 0.6, play D
   - Cooperators present; extract at their expense (stock/(n) vs stock/(2n))

4. **Mutual defection trap**: If cooperation_rate < 0.3 and stock_health > 0.5, play D
   - Others are defecting but pool remains healthy; join harvest before collapse

5. **Mixed field / uncertain conditions**: If 0.3 ≤ cooperation_rate ≤ 0.6
   - If stock_health > 0.6: Play D (abundant, exploit mixed play)
   - Else: Play C (moderate stock, others mixed - cooperation safer)

6. **Default**: Play D
   - Opportunistically extract from common pool in all other states

## Edge Cases

- **Round 1**: cooperation_rate undefined; treat as 0.5 (neutral assumption). Apply rules 1, 2, 5-6.
- **stock = 0**: Play C (zero payoff regardless; avoid negative dynamics)
- **n = 2**: Use cooperation_rate decision thresholds directly (only 1 opponent observable)

## Opportunistic Character

This strategy prioritizes immediate individual gain (D) under favorable conditions—high stock, abundant cooperators, or midgame positioning. It only retreats to cooperation when the resource is visibly depleted (preventing total ruin) or in final rounds where stock scarcity makes defection pointless. It exploits information asymmetry: observing aggregate cooperation allows selective defection against cooperative clusters, while maintaining plausible deniability in mixed populations.
'''

description_OPPORTUNISTIC_20 = '''
# Adaptive Exploitation Strategy

**DECISION RULE BY STOCK LEVEL:**

```
if current_round == r:
    action = DEFECT
else:
    cooperation_rate_last_round = observed_cooperators / (n - 1)
    
    if stock >= capacity * 0.6:
        action = DEFECT
    else if stock < capacity * 0.2:
        action = COOPERATE
    else:
        // Medium stock: conditional defection
        if cooperation_rate_last_round > (1/3):
            action = DEFECT
        else:
            action = COOPERATE
```

**ROUND 1 INITIALIZATION:**

Defect. With no history, assume at least some opponents will cooperate (common in CPR games). Extract immediate value while testing opponent behavior.

**ROUNDS 2 TO r-1:**

Track observed cooperation rate. If stock remains above 60% of capacity, maintain defection—this indicates sufficient opponents are cooperating to sustain growth. When stock dips below 60%, become conditionally cooperative: defect only if you observed >1/3 of opponents cooperating (evidence the pool can handle it), otherwise cooperate to prevent collapse.

The 20% threshold triggers mandatory cooperation: at this depleted level, continued defection risks mutual ruin. Cooperate to stabilize stock, then resume defection once recovered.

**FINAL ROUND (round r):**

Always defect. Future stock has no value. Extract maximum consumption.

**EDGE CASE - STOCK COLLAPSE:**

If stock ever equals zero, you receive zero regardless of action. Continue defecting in subsequent rounds—the pool is already dead, and cooperation provides no future benefit.

**OPPORTUNISTIC LOGIC:**

This strategy prioritizes immediate consumption whenever opponents maintain the pool, defects most rounds, and minimizes cooperation to only the minimum necessary to prevent mutual ruin. It exploits cooperative opponents systematically while adapting defensively only when the commons reaches critical depletion.
'''

description_OPPORTUNISTIC_21 = '''
# Opportunistic Adaptive Strategy

## Core Decision Rule

For each round t, compute two key metrics:
- **stock_ratio** = current_stock / capacity
- **cooperation_ratio** = observed_cooperators_from_previous_round / n

Use these to determine action:

```
if current_round == r (last round):
  DEFECT  // Extract maximum value; no future to protect

else if stock_ratio > 0.65:
  DEFECT  // Stock is abundant; exploit without consequence

else if stock_ratio ≤ 0.35:
  if cooperation_ratio > 0.5:
    COOPERATE  // Pool is dying; ride on others' recovery effort
  else:
    DEFECT  // Pool is dying anyway; take what you can

else:  // 0.35 < stock_ratio ≤ 0.65 (moderate stock)
  if cooperation_ratio > 0.70:
    DEFECT  // Many cooperators present; exploit them
  else if cooperation_ratio ≥ 0.40:
    COOPERATE  // Enough cooperation to sustain; match it
  else:
    DEFECT  // Few cooperators; defect with defectors
```

## First Round Handling

In round 1, no history exists. Assume **cooperation_ratio = 0.5** (neutral expectation) and proceed with stock evaluation. This biases toward early defection since stock_ratio starts at 1.0 (capacity).

## Edge Cases

**Extremely depleted stock** (stock_ratio near 0): Always defect. The pool is functionally dead; cooperation cannot save it before game end.

**Penultimate round** (t = r-1): Apply normal decision rule. The future (one round) is short enough that stock recovery is often impossible, so this typically triggers defection.

**Perfect information break**: If you observe zero or all cooperators every round, continue applying the rule mechanistically—do not assume collusion or coordinated behavior.

## Opportunism Mechanisms

- **Threshold defection**: Defect aggressively when stock allows (>0.65), maximizing single-round payoff.
- **Exploitative targeting**: When many opponents cooperate (>70%), defect to capture their contributions without reciprocal cost.
- **Tactical cooperation**: Only cooperate under duress (low stock) if others are also cooperating, creating a temporary pool-saving alliance that you exit as soon as stock recovers.
- **Endgame extraction**: Defect unconditionally in the final round regardless of stock state.
- **Asymmetric strategy**: Respond to aggregate cooperation rates, not individual histories. Free-riding on anonymous cooperators requires no guilt or reputation concern.
'''

description_OPPORTUNISTIC_22 = '''
# Opportunistic Threshold Strategy

## Core Decision Rule

Defect if: `stock/capacity > threshold(round, cooperation_rate)` AND stock > minimum_viability
Otherwise: Cooperate

where:

```
threshold(t, coop_rate) = 
  0.55 if t == 1  // Always defect round 1: extract from full stock
  0.45 if coop_rate > 0.5  // Majority cooperated: exploit them
  0.35 if coop_rate > 0.25  // Some cooperation: still worth defecting
  0.25 if coop_rate ≤ 0.25  // Mostly defectors: only defect if stock healthy
  
minimum_viability = 0.10 × capacity
```

## Detailed Decision Logic

**Round 1:** 
Defect unconditionally. Extract maximum from full capacity.

**Rounds 2 to r-2 (Mid-game):**
```
stock_ratio = current_stock / capacity
cooperators = count of players who played C last round
coop_rate = cooperators / (n - 1)
rounds_remaining = r - current_round

if stock_ratio > 0.5 and coop_rate > 0.4:
    return DEFECT  // Cooperators sustaining stock; exploit aggressively
    
else if stock_ratio > 0.4:
    return DEFECT  // Healthy stock supports continued extraction
    
else if stock_ratio > 0.25 and rounds_remaining > 1:
    if coop_rate > 0.3:
        return DEFECT  // Some cooperation means stock may recover
    else:
        return COOPERATE  // Too few cooperators to sustain extraction
        
else if stock_ratio > 0.12:
    return DEFECT  // Final extractions from depleted pool
    
else:
    return COOPERATE  // Stock critical; need growth before further extraction
```

**Final 2 rounds (t ≥ r-1):**
```
if stock_ratio > 0.10:
    return DEFECT  // No future to protect; maximize endgame extraction
else:
    return COOPERATE  // Only if stock near collapse
```

## Opportunistic Principles Embedded

- **Exploit cooperators:** Defect is triggered by observing high cooperation rates, converting others' restraint into personal gain
- **Extract-then-abandon:** Move aggressively toward full defection in late rounds since future rounds don't matter
- **Minimum preservation:** Cooperate only when stock risks collapse, preserving just enough viability to extract later
- **Asymmetric risk:** Willingly deplete stock faster than individually rational if it generates immediate payoff before others realize

The strategy prioritizes immediate consumption over collective sustainability, switching to temporary conservation only when current depletion threatens the ability to exploit remaining rounds.
'''

description_OPPORTUNISTIC_23 = '''
**OPPORTUNISTIC STOCK-EXPLOITATION STRATEGY**

**CORE PRINCIPLE:** Defect aggressively when stock is abundant (maximizing extraction), transition to cooperation only when stock depletion threatens the pool's viability.

**THRESHOLDS (as ratios of current stock to capacity):**
- CRITICAL_THRESHOLD = 0.25
- LOW_THRESHOLD = 0.40
- MEDIUM_THRESHOLD = 0.65
- HIGH_THRESHOLD = 0.85

**DECISION RULE:**

```
if current_round == r:
    return DEFECT  // Last round: extract maximum

stock_ratio = stock / capacity
cooperators_last_round = number of opponents playing C in t-1 (0 in round 1)

if stock_ratio >= HIGH_THRESHOLD:
    return DEFECT
    // Abundant resources: maximum extraction regardless of opponent play

else if stock_ratio >= MEDIUM_THRESHOLD:
    if cooperators_last_round >= (n-1) / 2:
        return DEFECT
        // Exploit cooperative opponents while stock remains high
    else:
        return DEFECT
        // Match the defection trend; continue extraction

else if stock_ratio >= LOW_THRESHOLD:
    if cooperators_last_round >= 0.75 × (n-1):
        return DEFECT
        // Heavy cooperation observed: exploit the surplus-generating behavior
    else:
        return COOPERATE
        // Few cooperators observed; save stock from further decline

else if stock_ratio >= CRITICAL_THRESHOLD:
    return COOPERATE
    // Stock depleted to danger zone: contribute to regrowth

else:
    return COOPERATE
    // Pool near collapse: forced conservation
```

**EDGE CASES:**

- **Round 1:** Return DEFECT (no history; assume pool is healthy; probe opponent behavior)
- **Stock = 0:** Return COOPERATE (no extraction possible; signal compliance to prevent further harm)
- **All opponents defected last round:** Defect if stock_ratio ≥ LOW_THRESHOLD; cooperate otherwise. (Defection is contagious when stock can absorb it)

**OPPORTUNISTIC MECHANICS:**

The strategy prioritizes extraction at high stock levels, treating cooperators as targets for exploitation rather than signals for reciprocation. It abandons defection only when the pool's physical constraints force cooperation—when regrowth is necessary to generate future payoffs. Cooperation is instrumentally timed to reset the stock before it bottoms out, then defection resumes immediately. This avoids mutual collapse while maximizing individualistic gain.
'''

description_OPPORTUNISTIC_24 = '''
# Adaptive Resource Exploitation Strategy

**Decision Rule by Game Phase:**

**Round 1:**
Defect. Stock is at maximum capacity, making defection's high immediate payoff maximally attractive. This establishes an aggressive baseline and tests opponent behavior.

**Rounds 2 through r-1 (Middle Rounds):**
Calculate stock health: `health_ratio = stock / capacity`

- **If health_ratio > 0.75:** Defect
  - Resource is plentiful; prioritize extraction at full rate (stock/n). The logistic growth can sustain defection.

- **If 0.5 < health_ratio ≤ 0.75:** Defect if `opponent_cooperation_rate < 50%`, else cooperate
  - Stock is adequate but showing stress. If opponents are mostly defecting, continue defecting to avoid being left behind in extraction. If opponents are mostly cooperating, switch to cooperation to preserve stock for continued extraction across future rounds while benefiting from their restraint.

- **If 0.25 < health_ratio ≤ 0.5:** Cooperate
  - Resource is under critical pressure. Defection threatens collapse and future earnings. Cooperate to stabilize stock and enable continued play, treating this as an investment in maintaining extraction opportunities.

- **If health_ratio ≤ 0.25:** Cooperate if `remaining_rounds > 1`, else defect
  - Near-depletion zone. Cooperate to allow regeneration unless this is the final round, in which case extract whatever remains.

**Final Round (t = r):**
Defect unconditionally if `stock > 0`. No future rounds exist to punish depletion, so maximize the terminal payoff.

**Opportunistic Core:**
The strategy prioritizes immediate extraction through early and aggressive defection, only constraining itself when stock depletion directly threatens continued earning. It monitors opponent cooperation rates to avoid unilateral restraint—if others defect, defect back; only maintain cooperation when needed to preserve the resource for exploitation in subsequent rounds.
'''

description_OPPORTUNISTIC_25 = '''
**DECISION RULE:**

Calculate stock health: h = stock / capacity

**If h ≥ 0.65:** DEFECT
- Pool is abundant and resilient; extract maximum value while growth can support it

**Else if h ≥ 0.40:** 
- Let d = proportion of opponents who defected last round (0 if first round)
- If d > 0.5: DEFECT (defection regime established; free-ride on tragedy)
- Else: COOPERATE (signal reciprocity to stabilize at current level)

**Else if h ≥ 0.15:** COOPERATE
- Pool is weakened; preserve stock to allow growth recovery

**Else:** COOPERATE
- Critical depletion; only chance for future payoff is collective restraint

**ROUND-SPECIFIC ADJUSTMENTS:**

*First round:* stock = capacity, so h = 1.0 → DEFECT unconditionally. Maximum extraction from full pool.

*Final round (t = r):* DEFECT unconditionally, regardless of h or opponent history. No future rounds; extract all available value.

*Second-to-last round (t = r-1):* If h ≥ 0.5, DEFECT. Otherwise follow main rule. Prepare for endgame extraction.

**EDGE CASE - Stock near zero:**

If stock < 0.01 × capacity: COOPERATE. Even opportunistically, extracting from a depleted pool yields negligible payoff. Better to preserve any chance of growth.

**TRACKING:**

Maintain running count of defectors from previous round. On round t, use defection count from round t-1. This adapts strategy to whether others are exploiting the pool or attempting sustainability.

**RATIONALE:**

Defect when the pool's regenerative capacity absorbs exploitation. Cooperate when preservation enables future extraction. Endgame abandons sustainability entirely. This exploits both: (1) high-stock regimes where defection has no catastrophic cost, and (2) low-stock regimes where cooperation serves selfish recovery interests.
'''

description_OPPORTUNISTIC_26 = '''
# Adaptive Opportunistic Pool Exploitation Strategy

## Decision Rules

**Core logic:**

```
For each round t ∈ {1, ..., r}:
  
  IF current_stock / capacity < 0.30:
    ACTION = C (emergency preservation mode)
  ELIF current_stock / capacity ∈ [0.30, 0.50):
    observed_coop_rate = cooperators_last_round / (n-1)
    IF observed_coop_rate > 0.65:
      ACTION = D (exploit abundance)
    ELSE:
      ACTION = C (mutual recovery mode)
  ELSE:  // stock/capacity ≥ 0.50
    ACTION = D (high stock enables opportunistic extraction)
  
  SPECIAL CASE - last round (t = r):
    IF current_stock / capacity < 0.25:
      ACTION = C (preserve pool integrity)
    ELSE:
      ACTION = D (final extraction)
```

## Edge Cases

**Round 1 (no prior history):**
Defect. The stock is at maximum capacity, making defection the payoff-dominant action. Future opponent behavior is unknown, so exploit the initial position.

**Stock collapse (stock → 0):**
Always cooperate regardless of observed cooperation rates. The pool is dead; defection yields zero. Cooperation allows logistic recovery and any future payoff.

**Perfect cooperation observed (all n-1 opponents played C):**
Defect in subsequent round unless stock has already fallen to critical levels. This directly exploits the cooperators' restraint while stock remains sufficient.

**Increasing defection trend:**
If observed cooperation rate drops below 0.40 in two consecutive rounds and stock is above 0.40 of capacity, shift to conditional defection: only defect if stock exceeds 0.55 of capacity, otherwise cooperate to prevent mutual collapse.

## Opportunistic Alignment

The strategy prioritizes immediate consumption while staying alive:

- **Default to exploitation**: Defect whenever stock health permits (>30% capacity), extracting stock/n over stock/(2n)
- **Selfish adaptation**: Cooperate only as a last resort when stock threatens depletion or when few others are cooperating (making defection individually futile)
- **Threshold-based switching**: Use stock depletion as the trigger for cooperation, not moral reasoning—cooperation serves as a tool to keep the resource exploitable in future rounds
- **End-game extraction**: Defect in the final round unless the pool has already collapsed, capturing remaining value with no future-round consequences

This avoids both tragedy-of-the-commons collapse and needless cooperation, instead oscillating between exploitation and just-barely-sufficient preservation.
'''

description_OPPORTUNISTIC_27 = '''
# Opportunistic Adaptive Strategy

## Decision Rule by State

**Last Round (t = r):**
Play Defect. With no future rounds, the immediate payoff advantage of defection outweighs any depletion cost.

**Stock Critically Low (stock < capacity/4):**
Play Cooperate. The pool is already damaged; further extraction yields diminishing returns. Cooperation preserves remaining stock and enables growth in remaining rounds.

**Stock Moderate (capacity/4 ≤ stock < capacity/2):**
Let c_avg = average fraction of opponents observed cooperating in all prior rounds.
- If c_avg > 0.5: Play Cooperate. Pool is declining and others are sustaining it; stabilize to avoid collapse.
- If c_avg ≤ 0.5: Play Defect. Extract aggressively before defectors exhaust the resource.

**Stock Healthy (stock ≥ capacity/2):**
Let c_avg = average fraction of opponents observed cooperating in all prior rounds.
- If c_avg > 0.5: Play Defect. Many cooperators exist; exploit the high stock they maintain.
- If c_avg ≤ 0.5: Play Cooperate. Opponents are defecting; defecting in parallel leads to mutual depletion. Cooperation avoids the worst outcome and preserves value.

## Edge Cases

- **Round 1:** No history exists. Play Defect to immediately seize the maximum payoff available at capacity. (This establishes a baseline; observed cooperation informs subsequent moves.)
- **Sudden stock collapse:** If stock drops below capacity/4 unexpectedly, switch to Cooperate regardless of round number or prior cooperation rates.
- **n = 2 (two players):** Same logic applies; c_avg compares your single opponent's observed moves against the 0.5 threshold.

## Opportunistic Alignment

The strategy prioritizes extracting surplus whenever opponents' cooperative behavior sustains high stock. It observes aggregate cooperation and punishes low cooperation rates by matching defection, avoiding the trap of unilateral cooperation. It defects maximally in the final round and seizes above-market payoffs whenever the pool is rich and others are restraining themselves. When forced into low-stock conditions or facing widespread defection, it minimizes losses by cooperating—not from altruism, but because extraction yields nothing when the pool is empty.
'''

description_OPPORTUNISTIC_28 = '''
**OPPORTUNISTIC EXPLOITATION STRATEGY**

**Decision Rule by Case:**

```
ROUND 1:
  → DEFECT
  (Initialize with maximum extraction; test opponents' strategies)

ROUNDS 2 to r-1:
  Compute state metrics:
    • observed_cooperation = (count of opponents who played C last round) / (n-1)
    • stock_ratio = current_stock / capacity
    • rounds_left = r - current_round
  
  Apply decision hierarchy (first match wins):
  
  if current_stock ≤ 2:
    → COOPERATE
    (Stock collapse imminent; defection guarantees zero next round)
  
  else if stock_ratio < 0.2 AND observed_cooperation < 0.4:
    → COOPERATE
    (Mutual defection spiral detected; recovery attempt)
  
  else if stock_ratio ≥ 0.4 AND observed_cooperation ≥ 0.5:
    → DEFECT
    (Exploit cooperative opponents while stock permits)
  
  else if rounds_left ≤ 2 AND stock_ratio > 0:
    → DEFECT
    (Endgame intensification; future stock irrelevant)
  
  else if stock_ratio ≥ 0.5:
    → DEFECT
    (Abundant stock; opportunistically extract)
  
  else:
    → COOPERATE
    (Stabilization mode; stock depleting under mixed defection)

FINAL ROUND (round r):
  if current_stock > 2:
    → DEFECT
    (No future payoff to protect)
  else:
    → COOPERATE
    (Marginal benefit minimal; avoid zero)
```

**Opportunistic Logic:**

- **Default action is defection**: Extract double payoff whenever plausible.
- **Exploit asymmetry**: Defect aggressively when opponents cooperate and stock supports it (immediate payoff jump without bearing consequences).
- **Collapse avoidance**: Shift to cooperation only when stock trajectory threatens zero (forcing own future payoff loss), or when opponent defection rates are so high that additional defection triggers cascade depletion.
- **Endgame aggression**: In final rounds, defect unless stock is already depleted—future stock irrelevant after round r.
- **Adaptive thresholds**: Cooperation thresholds adjust dynamically based on stock health and observed opponent defection rates, not rigid history.
'''

description_OPPORTUNISTIC_29 = '''
# Adaptive Exploitation with Collapse Prevention

**DECISION RULE:**

Let:
- c = observed number of opponents who cooperated in previous round (or 0 if round 1)
- S = current stock level
- t = current round number
- endgame_progress = (r - t) / r (decreases toward 0 as game approaches final round)
- stock_ratio = S / capacity

**Action selection:**

```
IF t == 1:
  DEFECT
  
ELSE IF t == r:
  DEFECT
  
ELSE (rounds 2 to r-1):
  cooperation_rate = c / (n - 1)
  
  // Dynamic threshold: rises in endgame, falls when stock depleted
  exploitation_threshold = 0.40 + (0.30 × endgame_progress) - (0.15 × stock_ratio)
  
  IF cooperation_rate > exploitation_threshold:
    DEFECT  // Free-ride on others' restraint
  ELSE:
    COOPERATE  // Maintain stock when cooperation is weak
```

**EDGE CASES:**

- **Round 1:** Always defect. No historical information exists; seize immediate payoff.
- **Final round (t = r):** Always defect. Stock level has zero future value; exploit at maximum.
- **Near-capacity stock with high cooperation:** Defect. This is the optimal free-riding scenario—others are restraining, you take S/n instead of S/(2n).
- **Severely depleted stock (S ≤ 0.25 × capacity):** Cooperate even with moderate cooperation rates. Threshold becomes more conservative to prevent total collapse that zeroes all future payoffs.
- **Rounds 2-3 with unknown opponent behavior:** Use cooperation_rate = 0 initially (assume worst case), making the threshold easier to exceed and defection more likely until cooperation is actually observed.

**OPPORTUNISTIC LOGIC:**

This strategy prioritizes extracting value when others are restrained (defecting against cooperators) while maintaining a minimal cooperation floor to prevent resource death. The endgame factor creates escalating aggression—defect thresholds rise dramatically in late rounds as future stock maintenance becomes worthless. Stock-based caution prevents total collapse that would destroy all remaining payoffs. You exploit high cooperation immediately; you only cooperate when the environment itself is uncooperative or when the resource genuinely needs preservation to generate future payoffs worth stealing from.
'''

description_OPPORTUNISTIC_30 = '''
# Opportunistic Adaptive Depletion Strategy

## Core Decision Rule

In each round t, observe the number of cooperators among opponents in round t-1 (denote as C_prev). Your decision is:

```
IF t = 1:
    play C
ELSE IF stock < 3n:
    play C (preserve depleted stock)
ELSE IF t = r (final round):
    IF stock > capacity/2:
        play D
    ELSE:
        play C
ELSE IF (C_prev / (n-1)) ≥ 0.6:
    play D (exploit cooperation majority)
ELSE IF (C_prev / (n-1)) < 0.3:
    play D (defect if others aren't cooperating much either—no value to conservation)
ELSE:
    play C (borderline case: cooperate to stabilize stock)
```

## Opportunistic Logic

**Exploitation phase:** When you observe that 60% or more of opponents are cooperating, defect immediately. You capture S/n while cooperators capture only S/(2n)—a 2× payoff advantage when stock is high. This is the core opportunistic move.

**Collapse avoidance:** If stock drops below 3n, switch to cooperation. At this level, defection yields minimal returns (S/n approaches 2n when S ≈ 3n), while defection accelerates stock collapse. Cooperating buys time for stock recovery via logistic growth. This is instrumental—you cooperate to preserve future exploitation opportunities.

**Defection when isolated:** If fewer than 30% of opponents are cooperating, defect anyway. The stock is already being depleted by widespread defection, so conservation provides no benefit. Extract what you can.

**Endgame extraction:** In the final round, if stock remains above capacity/2 (where growth dynamics are favorable), defect to maximize terminal payoff. There are no future rounds to exploit, so extract immediately.

## Edge Cases

- **Round 1:** Cooperate. You have no information about opponents and cannot afford stock collapse. This exploratory move reveals opponent types.
- **Rounds 2 to r-1:** Apply the cooperation-rate thresholds. Recalculate your decision each round based on new observations.
- **Stock trajectory:** If stock climbs toward capacity despite widespread defection (indicating strong growth periods or many cooperators), continue defecting until stock drops, then switch to stabilization.
- **Repeated low cooperation:** If cooperation_rate stays below 30% for three consecutive rounds, lock into defection for the remaining game—the resource is already lost and other players are non-cooperative.

This strategy treats cooperation as a *tool* for stock management, not a value. You defect when opponents gift you higher payoffs through their cooperation, and you cooperate only when defection would eliminate future exploitation opportunities.
'''

description_OPPORTUNISTIC_31 = '''
# Opportunistic Adaptive Strategy

## Decision Rule by Phase

**Early Exploration (rounds 1 through ⌈r/3⌉):**
- Round 1: Defect (establish strong position, learn how many cooperate)
- Rounds 2-⌈r/3⌉: Cooperate if observed_cooperation_count ≥ ⌈(n-1) × 0.8⌉, otherwise Defect
  - Exception: If stock drops below 3n, Cooperate once to allow regeneration

**Middle Exploitation (rounds ⌈r/3⌉ + 1 through r - 2):**
- Defect if observed_cooperation_count ≥ ⌈(n-1) × 0.6⌉ (exploit high cooperators)
- Defect if observed_cooperation_count ≤ ⌊(n-1) × 0.3⌋ (match defection)
- Cooperate only if stock < 2n (survival strategy to enable regeneration)
- Otherwise: Defect (default exploitative posture)

**Endgame (last 2 rounds):**
- Always Defect (no future rounds to penalize aggressive extraction)

## Stock-Level Overrides

Before applying the phase rule, check:
- If stock < 1.5n: Force Cooperate (critical depletion; need regeneration to avoid collapse)
- If stock ≥ capacity × 0.9: Strongly prefer Defect (maximum sustainability buffer permits extraction)

## Memory and Adaptation

Track a rolling average of opponent cooperation over the last 2 rounds (not just current round). Use this smoothed cooperation_ratio instead of single-round observation to avoid noise from random fluctuations.

Maintain a stock trend indicator: if stock decreased by >20% since last round, shift one threshold category toward Cooperate (signal that aggressive defection is unsustainable).

## Rationale

This strategy exploits the fundamental asymmetry: defection yields double consumption of cooperation while stock permits it. Early defection establishes a strong baseline while gathering opponent-type information. During middle rounds, it aggressively targets high-cooperation environments (where defection is most profitable) while matching low-cooperation environments. Endgame defection maximizes terminal payoff. Stock-based guardrails prevent self-inflicted collapse, and the rolling average smooths against manipulation by opponents attempting to bait cooperation through single-round cooperation bursts.
'''

description_OPPORTUNISTIC_32 = '''
# Opportunistic Strategy: Conditional Defection with Stock-Aware Thresholds

## Core Decision Rule

**Defect unless the stock is in critical danger.** Specifically, in round t:

1. Compute the **cooperation rate** from the previous round: c_rate = (cooperators observed) / (n-1)

2. Estimate next round's stock under full defection:
   - Assume all n players defect (worst case for stock)
   - Project: stock_projected = stock × (1 - n / (2n)) × (1 + growth_term)
   - Growth term: 2 × (stock/2) × (1 - (stock/2)/capacity)

3. **Decision**:
   - If stock ≥ capacity/3 **AND** c_rate ≥ 0.4: **DEFECT** (exploit the cooperators)
   - Else if stock < capacity/6 **AND** stock > 0: **COOPERATE** (emergency preservation)
   - Else if stock ≤ 0: **DEFECT** (already collapsed, no further loss)
   - Otherwise: **DEFECT** (default opportunistic stance)

## Edge Case Handling

**First round (t=1):**
- No history available. Defect.
- Rationale: No one has signaled their type yet; maximize immediate gain while stock is full.

**Last round (t=r):**
- Defect unconditionally. No future to preserve.
- Payoff from cooperation gets no stock regeneration benefit; defection dominates.

**Stock collapse (stock = 0):**
- Defect. You get 0 either way; move to next round (or game ends).

**Stock recovery:**
- If stock rises back above capacity/3 after a collapse scare, revert to opportunistic defection.

## Opportunistic Calibration

The thresholds embody opportunism:

- **High cooperation threshold (0.4)**: Only cooperate when others can't sustain the pool alone. When ≥40% cooperate, the pool is being actively maintained even without you—exploit this by defecting.

- **Stock floor (capacity/6)**: Defect only stops below this threshold. Above it, you always have enough runway to defect safely, even if the pool declines.

- **No loyalty**: Ignore *which* players cooperated (you can't observe that). React only to aggregate numbers. This prevents reputation-building and maximizes flexibility.

- **Last-round abandonment**: No sentimental cooperation. The repeated-game incentive to sustain the pool vanishes in round r.

## Adaptive Drift

If you observe c_rate trending downward over consecutive rounds (other players defecting more), drift toward more frequent defection: lower your cooperation floor to capacity/8 or eliminate the emergency preservation trigger entirely. The pool is already collapsing under others' defection; don't sacrifice your own payoff propping it up.

If c_rate ≥ 0.6 persistently, maintain strict defection—you're in a subsidy scenario where others are funding the pool.
'''

description_INDIVIDUALISTIC_5 = '''
# Stock-Responsive Adaptive Defection Strategy

## Decision Rule

```
if round == r (final round):
    action ← DEFECT

elif round == 1 (first round):
    action ← DEFECT

else:  // rounds 2 through r-1
    observed_cooperation_rate ← (cooperators_last_round) / (n - 1)
    stock_ratio ← stock / capacity
    
    if stock_ratio < 0.25:
        action ← COOPERATE  // Emergency recovery mode
    
    elif stock_ratio < 0.50:
        if observed_cooperation_rate ≥ 0.40:
            action ← COOPERATE  // Join recovery effort
        else:
            action ← DEFECT  // Maximize take before collapse
    
    elif stock_ratio < 0.75:
        if observed_cooperation_rate ≥ 0.60:
            action ← DEFECT  // Exploit high cooperators, stock is recovering
        elif observed_cooperation_rate ≥ 0.45:
            action ← COOPERATE  // Mirror cooperative trend
        else:
            action ← DEFECT  // Defectors dominate; defect
    
    else:  // stock_ratio ≥ 0.75
        if observed_cooperation_rate ≥ 0.55:
            action ← DEFECT  // Strong sustainability, maximize payoff
        else:
            action ← COOPERATE  // Proactive prevention of collapse
```

## Core Logic

**Stock monitoring:** Track whether the resource is in emergency (< 25% capacity), degraded (25-50%), recovering (50-75%), or healthy (≥ 75%) state.

**Opportunistic defection:** In healthy states with high observed cooperation (≥ 55-60%), defect to capture double payoff while others sustain the stock. This is the individualistic edge—free-ride on cooperators' restraint.

**Forced cooperation:** In low stock states, cooperate to enable logistic recovery regardless of others' behavior. Below 25% capacity, cooperation is mandatory because the resource is collapsing and no strategy recovers a depleted pool.

**Adaptive thresholds:** Use observed cooperation rate as a proxy for sustainability. High cooperation signals that stock is being managed well, creating conditions for profitable defection. Low cooperation signals a race-to-the-bottom, making defection the competitive response.

**End-game defection:** In the final round, defect unconditionally because no future stock state matters—only current payoff counts.

## Edge Cases

- **First round:** Defect to gather baseline information on opponent types without committing to cooperation.
- **Collapse scenario:** If stock hits 0, it stays 0; strategy cannot recover from this but switching to universal defection earlier prevents reaching this state.
- **Extreme cooperation (≥ 85% of opponents):** Still defect in healthy states because payoff maximization dominates when sustainability is assured by others.
- **Unanimous defection detection:** If observed_cooperation_rate = 0 and stock > 0.50 capacity, defecting extracts maximum payoff before inevitable collapse.
'''

description_INDIVIDUALISTIC_6 = '''
# Adaptive Resource-Level Strategy

## Core Decision Rule

Play DEFECT when stock is abundant; play COOPERATE when stock is endangered; always DEFECT in the final round.

**Specifically:**
```
if (current_round == r) {
    return DEFECT
}

stock_ratio = stock / capacity

if (stock_ratio >= 0.5) {
    return DEFECT
} else {
    return COOPERATE
}
```

## Rationale for Thresholds

The threshold of 0.5 × capacity marks the inflection point of the logistic growth function (2S(1 − S/capacity) is maximized at S = capacity/2). This is the critical boundary: 
- Above it: the resource is self-sustaining with positive net growth even under moderate consumption pressure
- Below it: defection-driven extraction risks irreversible collapse

## Edge Cases

**First round:** Apply the standard threshold rule (stock = capacity, so stock_ratio = 1.0 → DEFECT). This exploits the initial abundance.

**Final round:** Always DEFECT regardless of stock level. There is no future to optimize for, so maximizing immediate payoff dominates.

**Stock near zero:** Once stock < 0.1 × capacity, the only viable payoff is 0, so cooperation and defection are equivalently bad; the rule correctly defaults to COOPERATE (a defensive posture that could preserve a marginal recovery if others also cooperate).

## Individualistic Logic

This strategy is purely self-interested:
- It does not assume or reward opponent cooperation
- It exploits high stock aggressively, capturing 2× the payoff of cooperation
- It switches to cooperation only as a damage-control measure when the resource shows depletion risk
- It abandons cooperation entirely in the final round

The strategy treats other players as unknown agents whose behavior is irrelevant—only the observable state (stock level) and the game clock (current round) drive decisions. No history of opponent choices affects the action.
'''

description_INDIVIDUALISTIC_7 = '''
# Threshold-Based Opportunistic Extraction Strategy

**Core principle**: Maximize immediate extraction when the resource is abundant; allow recovery when depleted.

## Decision Rule

In each round t (where t < r):
1. **If stock > 0.7 × capacity**: Defect
   - Resource is plentiful; extract the larger individual share without concern for sustainability
   
2. **If 0.4 × capacity < stock ≤ 0.7 × capacity**: 
   - If observed cooperation in round (t-1) > n/2: Defect
   - Else: Cooperate
   - Rationale: If others are carrying the cooperative burden, exploit them. Otherwise, you need stock recovery, so cooperate.

3. **If stock ≤ 0.4 × capacity**: Cooperate
   - At this depletion level, both actions yield minimal immediate payoff. Cooperation preserves stock for regeneration. Defection depletes it further, harming future payoffs more.

4. **If t = r (final round)**: Always Defect
   - No future rounds exist; maximize immediate extraction regardless of stock level or opponent behavior.

## Edge Cases

- **Round 1**: Assume maximal cooperation was observed (n cooperators) to avoid spurious defection. Use the stock ≤ 0.4 logic: defect since stock = capacity > 0.7 × capacity.

- **Unknown cooperation count**: If aggregate observation is unavailable, treat it as 50% cooperation and apply the decision rule for the stock level only.

- **Stock exactly at threshold**: Use ≥ for the lower bound, > for the upper bound (cooperate on ties with low stock).

## Individualistic Foundation

This strategy is purely self-interested:
- Exploits cooperative opponents when resource abundance makes it safe
- Abandons cooperation in the final round with no moral concern
- Treats cooperation as a tactical response to stock scarcity, not a commitment to fairness
- Ignores others' welfare; optimizes only total personal consumption across all rounds
'''

description_INDIVIDUALISTIC_8 = '''
# Responsive Exploitation with Threshold-Based Sustainability Control

**Core Decision Rule:**

In round t, examine the observed cooperation count from round t-1 (c opponents cooperated out of n-1 total opponents). Calculate the opponent cooperation rate: p = c / (n-1).

- **If t = 1:** COOPERATE (establish baseline with no history)
- **If t = r (final round):** DEFECT (no future rounds to optimize, extract maximum)
- **If 1 < t < r:** Use threshold rule:
  - If p ≥ 0.5 AND stock ≥ capacity/2: **DEFECT** (others are sufficiently cooperative to sustain stock; exploit)
  - If p < 0.5 AND stock > capacity/4: **COOPERATE** (low cooperation from others signals stock risk; preserve)
  - If stock ≤ capacity/4: **DEFECT** (stock already critically depleted; rational to extract before collapse)

**Stock Depletion Sensitivity:**

Adjust the threshold dynamically based on stock pressure:
- Calculate stock ratio: σ = stock / capacity
- Cooperation threshold shifts: use 0.5 when σ ≥ 0.5; use 0.3 when 0.25 ≤ σ < 0.5 (more willing to defect when stock is middling); never cooperate when σ < 0.25 (freeload before collapse)

**Rationality for Defecting When Others Cooperate:**

If opponents maintain cooperation (p ≥ 0.5), they enable stock recovery even under your defection. Defecting nets S/n vs. S/(2n), exactly doubling your individual round payoff. Only cooperate if stock is visibly unsustainable (σ < 0.5) to prevent self-sabotage through collapse.

**Late-Game Adjustment:**

For rounds where t > 2r/3, shift defection threshold to p ≥ 0.4 (more aggressive) since fewer rounds remain for stock to recover. In final 3 rounds, unconditionally defect regardless of cooperation rate.
'''

description_INDIVIDUALISTIC_9 = '''
# Individualistic Adaptive Depletion Strategy

## Decision Rule by Stock Level

Base your action on the current stock level and rounds remaining, using no assumptions about opponent behavior beyond what you observe.

```
if stock ≤ capacity/2:
  play C
else if rounds_remaining == 1:
  play D
else if stock > 0.75 × capacity:
  play D
else:
  play D if (stock/n) > stock/(2n)
  (i.e., always true, so play D)
```

Simplified: 

**Cooperate if and only if:**
- Current stock ≤ capacity/2 (stock depletion threshold)

**Otherwise defect in all other cases**, including the final round.

## Rationale for Edge Cases

**First round:** Stock is at capacity, so defect immediately. Maximum sustainable harvest is at capacity/2, so defecting at full capacity provides immediate gain without imminent collapse.

**Final round:** Defect unconditionally. There is no future state to preserve, so the 2× immediate payoff from defection dominates all other considerations.

**Stock near depletion:** Switch to cooperation below capacity/2. At this level, the logistic growth function means that any further defection by multiple players collapses the resource. Cooperating slightly improves the remaining stock's growth trajectory, making it more likely to remain viable for future rounds. This is self-interest in maintaining the game state rather than collective altruism.

## Adaptiveness to Opponent Behavior

This strategy does not depend on observed cooperation rates from prior rounds. Your decision is determined solely by the observable state (stock level). Whether opponents cooperated or defected, if stock is high, defect. If stock is depleted, cooperate to slow the decline. This makes the strategy robust to any distribution of opponent strategies—you are always responding to the actual resource state, not to opponent types.
'''

description_INDIVIDUALISTIC_10 = '''
# STRATEGY: Adaptive Threshold Preservation

## DECISION RULE

**For round t where t < r (not the final round):**

Calculate pool health: `H = stock / capacity`

- If H < 0.40: Play C (Cooperate)
- If H ≥ 0.40: Play D (Defect)

**For round t = r (final round):**

Always play D (Defect)

## INDIVIDUALISTIC RATIONALE

This strategy pursues self-interest without reliance on opponent coordination:

1. **Exploitation at capacity**: When the pool is abundant relative to its growth capacity (H ≥ 0.40), extract the larger individual share (stock/n vs. stock/2n). Opponents' defection is irrelevant to this choice—you capture value while conditions allow.

2. **Preservation when depleting**: When the pool drops below 40% capacity, cooperate to slow depletion. This is self-interested because a depleted pool yields zero payoff regardless of what you do. Cooperation becomes the rational choice to preserve your future extraction opportunity—not because opponents deserve it, but because your own future rounds require it.

3. **Last-round exploitation**: In the final round, defection is optimal since no future stock preservation matters. Extract maximum value.

4. **No opponent modeling required**: The strategy ignores the aggregate cooperator count entirely. It depends only on objective state (stock level, capacity, round counter). You don't need to predict or respond to others' choices—you adapt only to the resource state itself.

## EDGE CASES

- **Round 1**: Apply the threshold rule normally. If stock = capacity and H = 1.0, play D.
- **Stock near zero** (e.g., stock = 0.5): H approaches 0, trigger cooperation. Even defecting yields nearly zero payoff, so cooperation is harmless and preserves any remaining growth potential.
- **Capacity = 2n minimum**: The health metric remains valid; threshold remains 0.40.
- **Early termination** (stock drops to 0 before round r): Both actions yield zero payoff; the strategy is vacuously satisfied.
'''

description_INDIVIDUALISTIC_11 = '''
## INDIVIDUALISTIC STOCK-AWARE STRATEGY

**Round 1 Decision:**
Defect. With no history to guide actions, maximize immediate payoff.

**Subsequent Rounds (t = 2 to r):**

Compute:
- `observed_coop_rate` = number of opponents who cooperated in round t-1 / (n-1)
- `stock_ratio` = current stock / capacity
- `rounds_remaining` = r - t

Decision cascade (evaluate in order; execute first matching condition):

1. **Critical Stock Preservation**
   - If `stock_ratio < 0.25`: **Cooperate**
   - Rationale: Stock depletion accelerates collapse. Defection now produces marginally higher immediate payoff but severely damages future earning potential. Self-interested play means protecting your future income stream.

2. **Endgame Defection**
   - If `rounds_remaining ≤ 1`: **Defect**
   - Rationale: Final round(s) offer no future consequences. Exploit all opportunities without restraint.

3. **Exploit High Cooperation**
   - If `observed_coop_rate ≥ 2/3`: **Defect**
   - Rationale: Others are restraining themselves; unilateral defection maximizes personal extraction while stock remains abundant.

4. **Opportunistic Exploitation (Mixed Cooperation)**
   - If `1/3 ≤ observed_coop_rate < 2/3`:
     - If `stock_ratio > 0.5`: **Defect** (can afford it; stock well-stocked)
     - Else: **Cooperate** (stock moderate; exploit risk outweighs gain)
   - Rationale: Weigh short-term defection gain against stock degradation risk over remaining rounds.

5. **Environment Matching (Low Cooperation)**
   - If `observed_coop_rate < 1/3`: **Defect**
   - Rationale: Others are depleting regardless; defecting prevents you from unilaterally subsidizing their consumption.

6. **Default (Rare Edge Case)**
   - **Cooperate** if none of above trigger
   - Rationale: Conservative fallback when adaptation signals are weak.

**Edge Case: Stock Collapse**
If stock = 0 before round r: Technically the game continues but both actions yield 0. Defect remains the response (no reason to change given zero payoff either way).
'''

description_INDIVIDUALISTIC_12 = '''
# Individualistic Threshold-Based Resource Exploitation Strategy

## Core Decision Rule

In each round, compare current stock to an adaptive threshold:

```
IF stock ≥ threshold:
    DEFECT (exploit available abundance)
ELSE:
    COOPERATE (preserve minimum viable stock)
```

Where `threshold = capacity × 0.35`

## Edge Cases & Round-Specific Rules

**Round 1:** Always DEFECT
- Immediate payoff maximization; opponents' strategies unknown

**Round r (final round):** Always DEFECT  
- No future stock regeneration needed; extract maximum value from final state

**Rounds 2 through r-1:** Apply threshold rule above

**Stock near collapse (stock < 0.15 × capacity):** Override with COOPERATE
- Prevent complete depletion that yields zero payoff; regenerate sufficient stock to resume extraction

## Threshold Justification & Adaptation

The threshold of 35% capacity is calibrated to:
- Sustain stock growth after own defection (growth maximizes around 50% capacity, so 35% provides buffer)
- Allow profitable defection when stock is robust
- Trigger cooperation before cascading collapse

Implicitly adaptive through stock feedback:
- If opponents also defect heavily, stock drops → threshold triggers cooperation automatically
- If opponents cooperate, stock remains high → threshold permits continued defection
- No need to track individual opponent behavior; the aggregate stock level embeds collective action

## Individualistic Logic

This strategy is purely self-interested:
- Defect whenever it doesn't threaten your own future payoff
- Cooperate only when defection would destroy the resource you depend on
- Never sacrifice current consumption for others' welfare
- In the final round, extract maximum regardless of collective consequences
- End-game behavior is unambiguously greedy; mid-game behavior appears conditional only because stock depletion directly reduces your payoffs

The strategy exploits cooperative opponents when they maintain high stock, but doesn't reciprocate their cooperation—cooperation is deployed only as a self-preservation tactic.
'''

description_INDIVIDUALISTIC_13 = '''
# Adaptive Stock-Responsive Strategy

**Core principle:** Defect when the stock is abundant and likely sustainable; cooperate when the stock is depleted or deteriorating to protect future payoff opportunities.

## Decision Rule

Observe the current stock level and the number of cooperators from the previous round. Apply the following logic:

**Round 1 (baseline):**
Defect

**Round r (final round):**
Defect

**Rounds 2 to r-1 (adaptive phase):**

Calculate `cooperation_rate_prev = observed_cooperators_last_round / (n - 1)`

Define thresholds:
- `low_threshold = 0.4 × capacity`
- `mid_threshold = 0.65 × capacity`

1. If `stock < low_threshold`: **Cooperate**
   - Stock is critically low; consumption at this level risks crash and eliminates future earnings.

2. Else if `stock ≥ mid_threshold`: **Defect**
   - Stock is abundant and can sustain high extraction. Logistic growth peaks around capacity/2, and we're above that. Exploit the surplus.

3. Else (stock in middle zone, `low_threshold ≤ stock < mid_threshold`):
   - If `cooperation_rate_prev ≥ 0.5`: **Defect**
     - Sufficient cooperators exist; stock is being managed. Extract the higher individual payoff.
   - Else: **Cooperate**
     - Few cooperators observed; defection by others is depleting stock. Unilateral cooperation now may stabilize it for next round.

## Edge Cases

- **First round:** You have no historical cooperator data. Defect to establish a payoff and signal your type.
- **Last round:** No future stock matters. Defect regardless of current level.
- **Stock = 0:** The game continues but payoffs are zero. Cooperation makes no difference; defect as default.
- **All n-1 opponents consistently defect:** Cooperate in middle zones to slow depletion; defect when stock is high to still earn something.

## Individualistic Alignment

This strategy prioritizes personal payoff maximization without assuming opponent alignment, shared norms, or commitment to coordination. It treats other players' actions as signals of available resources, not as trustworthy commitments. Cooperation is purely a self-interested hedge against resource collapse, not a goodwill gesture.
'''

description_INDIVIDUALISTIC_14 = '''
# Adaptive Depletion-Responsive Strategy

## Core Decision Rule

In round t, defect if ANY of the following conditions hold:

1. **Stock is critically depleted:** stock < 0.3 × capacity
2. **Opponents are over-defecting:** observed_defection_rate > 0.5
3. **Resource trajectory is negative:** stock has decreased from previous round AND observed_defection_rate ≥ 0.4
4. **Late-game scavenging:** t > 0.8r AND stock < capacity

Otherwise, **cooperate**.

## Specific Decision Rules

```
observed_defection_count = number of opponents who defected in previous round
observed_defection_rate = observed_defection_count / (n - 1)

if round == 1:
  COOPERATE  // Initial cooperation to assess opponent behavior
  
else if stock < 0.3 * capacity:
  DEFECT  // Resource near collapse; salvage what you can
  
else if observed_defection_rate > 0.5:
  DEFECT  // More than half are defecting; tragedy of commons unfolding
  
else if stock < previous_stock AND observed_defection_rate >= 0.4:
  DEFECT  // Stock declining despite moderate defection; trend is unsustainable
  
else if t > 0.8 * r AND stock < capacity:
  DEFECT  // Final rounds with non-maxed stock; exploit remaining resource
  
else:
  COOPERATE  // Stock healthy, defection manageable, resource sustainable
```

## Edge Cases

**First round (t=1):** Cooperate unconditionally. You have no history to evaluate opponent behavior.

**Stock at zero:** Defect (though you receive 0 either way; this is a formality).

**Stock regenerates to capacity:** Reset any accumulated pessimism; return to cooperative mode unless defection rate remains high.

**All opponents cooperated last round:** Default to cooperation unless stock deteriorated significantly.

**Perfect splits (exactly k/n opponents defected):** Use the exact proportion; no tie-breaking bias needed.

## Individualistic Alignment

This strategy embodies self-interested rationality without relying on others' cooperation:

- **Monitors actual behavior, not assumptions.** You track what opponents demonstrably do, not what you hope they'll do.
- **Extracts value from cooperators without naive commitment.** If others hold cooperation, you benefit from the sustained resource while free-riding slightly. If they defect, you pivot immediately.
- **Abandons coordination when it fails.** The moment defection becomes widespread or stock depletes, you stop pretending cooperation is viable and grab your share.
- **Responds to state, not trust.** Decisions depend on observable stock level and opponent counts, not on reputation or reciprocity beliefs.
'''

description_INDIVIDUALISTIC_15 = '''
**Decision Rule Based on Stock State and Remaining Rounds**

Compare current stock to a dynamic threshold:

```
remaining_rounds = r - current_round
stock_recovery_point = capacity / 2

If current_round == r:
  DEFECT
Else if stock >= stock_recovery_point + (remaining_rounds × 2n):
  DEFECT
Else if stock <= 2n:
  DEFECT
Else:
  COOPERATE
```

**Intuition of the thresholds:**

- **Defect when stock is abundant**: If stock substantially exceeds what's needed to sustain low consumption over remaining rounds, extract the maximum immediate value (S/n). Cooperative payoffs are suppressed relative to defection.

- **Defect in final round**: No future rounds exist, so there is no cost to depleting stock. Defection dominates.

- **Defect when stock is critical**: Below the subsistence level 2n, stock is effectively doomed. Accept the collapse and maximize extraction.

- **Cooperate in the middle range**: When stock is above critical but below abundant, cooperation slows depletion and maintains access to payoffs in remaining rounds. The preservation benefit outweighs the per-round payment disadvantage of C.

**Adaptive refinement:**

Track the observed number of cooperators each round. If cooperation frequency among opponents drops below n/3, shift the threshold upward:

```
If observed_cooperators_last_round < n/3:
  stock_recovery_point = capacity / 3
```

This responds to free-riding: if opponents defect heavily, the stock collapses faster, making it rational to defect sooner before the resource is wasted on others' exploitation.

**Edge cases:**

- Round 1: Use standard logic with remaining_rounds = r-1. Stock is at capacity, so typically DEFECT.
- Fractional stock: Round down consumption calculations. If stock rounds to 0, DEFECT (final extraction) unless stock is literally 0, then action is irrelevant.
- Two-player case (n=2): Same rule applies; thresholds scale with n.
'''

description_INDIVIDUALISTIC_16 = '''
# Adaptive Exploitation Strategy

## Decision Rules

**Cooperation threshold:** Cooperate in round t (where t < r) only if **both**:
1. Observed cooperation rate in round t-1 was ≤ 50% (fewer than half of opponents cooperated), **OR**
2. Current stock level is below min_sustainable_stock = capacity × 0.3

**Defect otherwise** — including:
- Any round where observed cooperation rate in prior round exceeded 50%
- The final round (t = r)
- Any round where stock is above the sustainability threshold

**First round special case:** Cooperate (gather cooperation information with minimal risk)

## Rationale for Edge Cases

**Last round (t = r):** Always defect. No future payoff to protect; maximize immediate consumption.

**Stock collapse detection:** If stock < capacity × 0.15, cooperate regardless of history. A dead pool yields nothing; marginal attempts to revive it are rational even at cost.

**Cooperation switching:** When opponents signal low cooperation (≤50%), shift to cooperation attempt for 1–2 rounds. This is not altruistic—it exploits the growth function: sparse defection allows stock recovery, increasing future opportunities.

## Implementation

```
if round == r:
    action = D
else if stock < capacity * 0.15:
    action = C
else if stock >= capacity * 0.3:
    if observed_cooperation_rate_previous_round > 0.5:
        action = D  // exploit high cooperation
    else:
        action = D  // defect unless forced to repair stock
else:  // stock in [0.15 * capacity, 0.3 * capacity]
    action = C  // repair stock to re-enter exploitation phase
```

## Individualistic Alignment

This strategy prioritizes personal payoff extraction. It **exploits cooperation when present** (defect when others cooperate), **abandons cooperation quickly** (defect the moment others defect), and only sustains stock **instrumentally**—to maintain future exploitation opportunities, not from any concern for collective welfare.
'''

description_INDIVIDUALISTIC_17 = '''
**INDIVIDUALISTIC ADAPTIVE STRATEGY**

**Decision Framework:**

Cooperate or defect based on stock sustainability relative to available rounds. The core principle: maximize individual consumption while ensuring the stock doesn't collapse before the final round. Exploit cooperative opponents when the pool can sustain it; cooperate defensively when depletion threatens future payoffs.

**Decision Rules:**

```
For each round t ∈ {1, 2, ..., r}:

1. Calculate remaining_rounds = r - t + 1

2. Estimate opponent cooperation rate from last round:
   - If t = 1: assume_cooperation_rate = 0.5 (neutral assumption)
   - If t > 1: cooperation_rate = C_observed / (n - 1)
     where C_observed = count of opponents who cooperated

3. Project critical stock level:
   - min_safe_stock = 2n (minimum viable to sustain play)
   - target_stock = capacity / 2 (optimal for growth)
   - rounds_until_end = r - t

4. Decision rule:
   
   IF (stock < 2n × 1.5):
      PLAY C  // Stock critically depleted; rebuild required
   
   ELIF (t = r) AND (stock > 0):
      PLAY D  // Final round: extract maximum, no future impact
   
   ELIF (cooperation_rate < 0.25):
      PLAY C  // Defectors dominate; cooperative restraint needed to survive
   
   ELIF (stock > target_stock) AND (cooperation_rate > 0.50):
      PLAY D  // Stock healthy + others restrained; exploit the advantage
   
   ELIF (stock > capacity × 0.4) AND (remaining_rounds ≥ 3):
      PLAY D  // Sufficient buffer with multiple rounds left
   
   ELSE:
      PLAY C  // Default: preserve stock when in doubt
```

**Edge Cases:**

- **Round 1:** Play C. Without history, assume mixed opponent population; starting cooperative tests the environment without risking immediate collapse.

- **Last round (t = r):** Play D if stock > 0. Future payoffs don't exist; the payoff from defection exceeds any stock preservation benefit.

- **Stock approaching 2n:** Play C regardless of cooperation rate. The pool is near collapse; one more D round may eliminate all future payoff.

- **Cooperation drops suddenly:** Increase defection threshold. Shift immediately to C if cooperation_rate falls below 0.25, interpreting this as signal of widespread defection and unsustainable extraction.

**Individualistic Orientation:**

This strategy is purely self-interest focused: it monitors what *others* do but responds based on *your* future payoff, not their welfare. You exploit cooperation when possible (defect against cooperators), cooperate only when necessary to prevent stock collapse that would harm you in future rounds. You do not sacrifice for the collective; you restrict consumption only to preserve your own future extraction opportunities.
'''

description_INDIVIDUALISTIC_18 = '''
**STOCK-ADAPTIVE DEFECTION WITH COOPERATION SENSING**

**Decision Rule:**

For round t < r:
- Let c = number of opponents observed cooperating in round t-1 (or 0 if t=1)
- Let cooperation_threshold = ⌈(n-1)/2⌉ (majority threshold)
- **Defect if:** stock > capacity/2, OR (stock > capacity/4 AND c < cooperation_threshold)
- **Cooperate otherwise**

For round t = r (final round):
- **Defect if stock > 0, else Cooperate** (no future stock to preserve)

**Edge Cases & Initialization:**

Round 1: Defect. Without history, optimize immediate payoff and gather information on opponent behavior through observation.

Stock depletion: If stock falls to 0 at any point, Cooperate in all remaining rounds (only difference between C and D is zero either way, but C preserves the marginal possibility of future regeneration).

**Individualistic Logic:**

This strategy prioritizes maximizing own payoff without relying on opponent coordination:

- Defects opportunistically when stock is abundant (capturing the 2× payoff advantage while regeneration can sustain it)
- Switches to cooperation when stock drops below critical thresholds, treating preservation as an individual investment in future self-payoff, not collective welfare
- Uses opponent cooperation counts to update beliefs about stock trajectories: high cooperation signals sustainable extraction, justifying continued defection; low cooperation signals a depleting commons, making defection self-destructive
- Defects in the final round whenever possible, since future stock holds no value
- Never assumes opponents will cooperate—only adapts expectations based on revealed behavior

The strategy treats the common pool as a personal resource to be exploited based on its current abundance and observable sustainability signals, abandoning restraint only when resource scarcity makes restraint privately optimal.
'''

description_INDIVIDUALISTIC_19 = '''
**STOCK-CONSCIOUS DEFECTION STRATEGY**

**Core Decision Rule:**

For round t:
- If t = 1: Play C
- If t > 1 and stock ≤ capacity/2: Play C
- If t > 1 and stock > capacity/2 and (opponent_cooperators_last_round > 0): Play D
- If t > 1 and stock > capacity/2 and (opponent_cooperators_last_round = 0): Play C
- If t = r (final round): Play D if stock > 0, else play C

**Operationalized Logic:**

```
if round == 1:
    action = C
else:
    stock_ratio = current_stock / capacity
    observed_cooperators_last_round = number of opponents who played C
    
    if stock_ratio ≤ 0.5:
        action = C  // critical depletion mode
    else if stock_ratio > 0.5 and observed_cooperators_last_round > 0:
        action = D  // exploit while stock is healthy
    else if stock_ratio > 0.5 and observed_cooperators_last_round == 0:
        action = C  // avoid pointless mutual defection
    
    if round == r:
        action = D  // terminal round exploitation
```

**Edge Cases:**

- First round: Cooperation establishes baseline sustainability and avoids immediate collapse
- Stock depletion below 50% capacity: Switch to cooperation to allow stock recovery, as defection below this threshold accelerates collapse
- Mutual defection detection: If all opponents defected, reciprocate with cooperation to preserve stock rather than waste consumption on a depleted pool
- Final round: Defect regardless of stock level to capture maximum extraction with no future consequences
- Stock = 0: Play C (mathematically neutral, but maintains consistency)

**Individualistic Alignment:**

This strategy is purely self-interested: it exploits cooperative opponents when conditions are favorable, but switches to cooperation only when personal payoff calculations favor stock preservation over immediate extraction. The agent treats opponents as sources of advantage or threats, not as partners, and abandons cooperation immediately when sustainability becomes individually optimal.
'''

description_INDIVIDUALISTIC_20 = '''
# Adaptive Exploitation with Recovery Strategy

**Core Decision Rule:**

For each round, calculate a depletion-response threshold based on the current stock and trajectory.

- If stock ≥ 2×capacity/3: Play D (Defect)
- If stock < 2×capacity/3 and stock is declining or predicted to continue declining: Play C (Cooperate)
- If stock < 2×capacity/3 and stock is stable or recovering: Play D (Defect)

**Stock Trajectory Prediction:**

After observing cooperation count k from the previous round, estimate next round's stock:
- Calculate consumption from last round: total = k×(S/(2n)) + (n-k)×(S/n)
- Calculate remaining: S_remaining = S - total
- Calculate growth: 2 × S_remaining × (1 - S_remaining/capacity)
- Projected stock = min(S_remaining + growth, capacity)

If projected_stock < current_stock, classify as "declining." If projected_stock ≥ current_stock, classify as "stable or recovering."

**First Round:**

Play D. Stock is at maximum capacity; defection yields immediate gain with no prior depletion data to suggest imminent collapse.

**Last Round (t = r):**

Always play D. No future rounds exist, so preserving stock has zero value. Extract maximum immediate payoff.

**Rounds 2 through r-1:**

Apply the main decision rule above.

**Edge Case: Stock Near Zero:**

If stock ≤ 0.1, play C regardless of other signals. Cooperation allows minimal recovery via growth; defection yields near-zero payoff and prevents any future rounds from having positive payoff.

**Rationale:**

This strategy prioritizes personal payoff by exploiting the pool when abundant (high stock, defect) while preventing total collapse (cooperate when declining) through a selfish preservation motive—not altruistic concern, but recognition that a dead pool yields nothing. The adaptive threshold responds to observed aggregate behavior without requiring coordination or trust.
'''

description_INDIVIDUALISTIC_21 = '''
# Adaptive Stock-Responsive Strategy

## Core Decision Rule

In each round t, cooperate if and only if BOTH conditions hold:
1. **Stock health condition**: current_stock ≥ 0.4 × capacity
2. **Opponent cooperation condition**: observed_cooperation_rate ≥ 0.5

Otherwise, defect.

Where:
- `observed_cooperation_rate` = (number of opponents who cooperated in round t-1) / (n-1)
- In round 1, assume observed_cooperation_rate = 1.0 (cooperate unless stock is already degraded)

## Round-Specific Modifications

**Round 1 (first round):**
- Cooperate (initialize with cooperation probe; stock is at maximum capacity so defection gains are immediate but stock recovery is possible)

**Final round (t = r):**
- Defect regardless of other conditions
- Rationale: No future rounds to suffer stock depletion; extract maximum value now

**Rounds 2 through r-1:**
- Apply the core decision rule above

## Edge Case Handling

- If current_stock ≤ 0.1 × capacity: Defect (resource is collapsing; cooperation has minimal value as others are likely depleting heavily)
- If observed_cooperation_rate is undefined or indeterminate: Treat as 0.5 (neutral assumption, apply only the stock health condition)
- If capacity is ambiguous or missing from state: Use last observed maximum stock as proxy for capacity

## Underlying Logic

This strategy is individualistic because it:
- Prioritizes maximizing own round-by-round payoff given observed conditions
- Treats opponent cooperation as evidence of sustainability, not as a moral norm
- Defects when the resource is fragile regardless of opponent behavior (since cooperating won't save a collapsing pool)
- Extracts maximum value in the final round when future costs don't exist
- Does not commit to reciprocal cooperation; instead, cooperates only when stock health and observed opponent behavior both signal it's individually rational to preserve resources for future rounds
'''

description_INDIVIDUALISTIC_22 = '''
**THRESHOLD-ADAPTIVE EXPLOITATION STRATEGY**

**Decision Rule:**

For round t with current stock S and remaining rounds r - t:

1. **First Round (t = 1):** DEFECT
   - Extract maximum value immediately; observe opponent composition

2. **Preservation Threshold (t > 1):** IF S ≤ 0.35 × capacity THEN COOPERATE
   - When stock is critically depleted, defection yields minimal gains and risks collapse
   - Cooperation preserves any regeneration potential

3. **Extraction Phase (t > 1):** IF S > 0.35 × capacity THEN
   - Let c = number of opponents who cooperated in round t-1
   - Let coop_ratio = c / (n-1)
   
   a. IF coop_ratio ≥ 0.6 AND S ≥ 0.7 × capacity THEN DEFECT
      (Exploit high cooperation when stock is robust)
   
   b. IF remaining_rounds ≤ 2 THEN DEFECT
      (Endgame extraction: prioritize immediate payoff over future)
   
   c. IF 0.35 < S ≤ 0.7 × capacity AND coop_ratio < 0.4 THEN DEFECT
      (Mid-range stock with low cooperation: match aggressive extraction)
   
   d. OTHERWISE COOPERATE

**Edge Cases:**

- Stock = 0: Payoffs are zero regardless; default to DEFECT (no cost to defecting)
- Final round (t = r): Always DEFECT (no future rounds to protect)
- Stock grows above capacity: Treat as capacity (capped regeneration); proceed normally

**Rationale (Individualistic Alignment):**

This strategy rejects norm-enforcement or reciprocal altruism. It treats cooperation as a defensive tactic when the commons faces collapse, and defection as the baseline when pool health permits extraction. The strategy monitors aggregate cooperation rates to infer depletion dynamics without requiring trust or coordination, adjusting extraction aggressiveness as time and stock conditions shift.
'''

description_INDIVIDUALISTIC_23 = '''
**Adaptive Stock Threshold Strategy**

Decision Rule:
- In each round t, compute the stock depletion urgency as: rounds_remaining = r - t
- Compare current stock level against a dynamic threshold
- Threshold(t) = capacity × max(0.3, (r - t) / r)

If stock ≥ Threshold(t): **Defect**
If stock < Threshold(t): **Cooperate**

Edge Cases:
- Final round (t = r): Always **Defect**. No future stock value exists; extracting maximum immediate payoff is optimal. threshold → 0.
- First round: If stock = capacity (normal), compute threshold = capacity × (r-1)/r. Defect if capacity ≥ threshold, which is typically true unless r is very small.

Intuition:
The strategy exploits stock abundance when available (Defect) but switches to conservation (Cooperate) when stock falls below a time-dependent threshold. As the game progresses, the threshold relaxes because future rounds become fewer and less valuable. In the final round, all future considerations disappear.

Adaptation to Observed Cooperation:
After each round, observe the number of cooperators among opponents (call it c_opponents).
- If c_opponents > n/2 (majority cooperate): Raise threshold slightly next round. Opponents are maintaining stock; opportunistically Defect.
- If c_opponents < n/2 (majority defect): Lower threshold slightly next round. Stock will deplete; Cooperate when stock is borderline to extend the resource.

Adjustment: threshold(t) ← threshold(t) × (1 + 0.1 × (n/2 - c_opponents) / n)

Rationale for Individualism:
- No assumption of opponent coordination or reciprocity; treat others as independent agents with unknown strategies
- Decision depends only on personal payoff optimization, stock state, and time remaining
- Exploit opportunities (high stock) without hesitation
- Conserve only when doing so directly benefits your own future payoffs, not for moral or group welfare reasons
'''

description_INDIVIDUALISTIC_24 = '''
# Adaptive Stock-Monitoring Strategy

## Core Decision Rules

**In the final round (t = r):**
- Defect if stock > 0.05 × capacity
- Otherwise cooperate (defection yields negligible payoff)

**In all other rounds:**

1. **Immediate depletion check:** If stock < capacity/(4n), defect unconditionally (the resource is nearly exhausted; extract what remains rather than waste cooperating)

2. **Stock abundance exploitation:** If stock > 0.75 × capacity, defect (stock is flush; exploit the high yield S/n while available)

3. **Stock scarcity recovery:** If stock < 0.35 × capacity, cooperate (stock is stressed; the S/(2n) payoff is minimal anyway, and cooperation helps regenerate via growth dynamics)

4. **Intermediate stock with history:**
   - Calculate observed cooperation rate: coop_rate = (total cooperators observed across all previous rounds) / (n-1) × (round number - 1)
   - If coop_rate ≥ 0.55, cooperate (others are maintaining stock; stay cooperative)
   - If coop_rate < 0.55, defect (others are depleting; extract individually before collapse)

## Edge Cases

**Round 1:** Apply the abundance exploitation rule (stock = capacity, so if n ≥ 2, stock > 0.75 × capacity). Defect.

**Stock collapse (rounds 2+):** Once stock reaches zero, continue playing the corresponding rule (defection yields 0, cooperation yields 0; the game outcome is locked).

**Sparse cooperation observations:** If fewer than ⌈n/3⌉ players cooperated in the previous round, immediately transition to sustained defection for the remainder of the game (signal that cooperation is futile).

## Individualistic Alignment

This strategy is purely self-interested: it abandons cooperation the moment aggregate evidence suggests others are defecting or stock trends downward. It extracts maximum value in high-stock states without regard to sustainability, and switches to exploitation mode under collective defection. There is no punishment, reward-matching, or implicit coordination—only adaptive individual payoff-maximization based on observable stock states and aggregate defection signals. The strategy actively exploits the high-productivity states created by others' cooperation while exiting to defection when cooperation becomes individually disadvantageous.
'''

description_INDIVIDUALISTIC_25 = '''
# Adaptive Stock-Threshold Strategy

## Decision Rule

In each round t with stock S_t and ρ = (r - t) rounds remaining:

**Compute defection incentive:**
- Let ρ_normalized = ρ / r (fractional rounds remaining, 0 to 1)
- Let stock_ratio = S_t / capacity
- Compute depletion_risk = max(0, (2n / capacity) - stock_ratio)

**Defect if any condition holds:**
1. ρ_normalized < 1/(2n) — final round or near-final round with many players
2. stock_ratio < 0.3 — stock critically low relative to capacity
3. stock_ratio < 0.5 AND depletion_risk > 0.15 — stock below growth optimum AND approaching unsafe level
4. (stock_ratio < (0.4 + 0.3 × ρ_normalized)) — declining threshold as rounds decrease

**Otherwise cooperate.**

## Edge Cases

**Round 1:** Apply standard rule. With stock = capacity, typically cooperate unless n is very large (n > 15).

**Final round (t = r):** Always defect. No future stock to preserve.

**Rounds r-1 to r-⌊r/4⌋:** Increase defection probability. Use stock_ratio < (0.45 + 0.2 × ρ_normalized) as threshold instead.

**Stock near zero:** If S_t ≤ 2, defect (stock will not meaningfully recover).

**Stock near capacity:** If stock_ratio > 0.9 and ρ_normalized > 0.5, cooperate (safe to invest in growth).

## Individualistic Alignment

- **Pure self-interest:** Defect in endgame when others' future payoffs become irrelevant to you.
- **Opportunistic rationality:** Cooperate early when stock abundance makes future high, defect when stock scarcity makes immediate extraction superior.
- **No reciprocity:** Ignore how many opponents cooperated in previous rounds. Respond only to observed stock state, which reflects the aggregate effect of past behavior.
- **No moral judgment:** Defection when others cooperate is rational, not betrayal.
- **Single-minded payoff maximization:** The threshold rules encode optimal discounting—trade current consumption for future consumption only when future stock density justifies it.

The strategy treats the common pool as a depletable asset to exploit at the margin of sustainability, shifting extraction intensity purely based on scarcity signals (stock level and time horizon), not on opponents' choices.
'''

description_INDIVIDUALISTIC_26 = '''
**ADAPTIVE DEFECTION WITH STOCK MONITORING**

**Decision Rule:**

For each round t, execute the following in order:

1. **Terminal Round Check:** If t = r, play D (defect). Terminal round defection dominates.

2. **Opponent Cooperation Assessment:** Let C_obs = total cooperations observed from opponents across all previous rounds. Calculate cooperation_rate = C_obs / ((t-1) × (n-1)) if t > 1, else set to 0.5 (neutral prior).

3. **Stock Health Evaluation:** Compute stock_health = stock / capacity.

4. **Decision Logic:**
   - If stock_health < 0.15: Play C
     - Stock is critically depleted; only cooperation can restore it
   - Else if stock_health < 0.35 AND cooperation_rate < 0.4: Play C
     - Stock is moderate-low and opponents are untrustworthy; preserve
   - Else if stock_health < 0.35 AND cooperation_rate ≥ 0.4: Play D
     - Stock is moderate-low but others cooperate; exploit to recover faster
   - Else: Play D
     - Stock is healthy; maximize immediate payoff. Opponent behavior is irrelevant—defection is strictly better in healthy states.

**Edge Cases:**

- **Round 1 (t=1):** No history exists. cooperation_rate defaults to 0.5. Use stock_health rule: typically stock = capacity, so play D.

- **Stock = 0:** Play C (no strategic distinction; payoff is 0 either way). This prevents wasteful defection.

- **Last Round (t=r):** Always D regardless of stock_health, as no future consequences exist.

- **Tie-breaking (stock_health exactly at thresholds):** Use next lower threshold (more conservative).

**Rationale:**

Defection extracts more in each round, but only while stock regenerates. Monitor stock health directly rather than opponent behavior when stock is abundant—your opponents' choices caused the depletion you observe, and cooperating when stock is critical is the only way to avoid collapse. Switch to exploiting cooperators when stock recovers sufficiently.
'''

description_INDIVIDUALISTIC_27 = '''
**ADAPTIVE RESOURCE DECLINE STRATEGY**

**Core Logic:**
Defect by default as the payoff-maximizing action per round. Cooperate conditionally when evidence suggests the resource can sustain high cooperation while still providing good payoff.

**State Tracking:**
- Track stock level each round
- Record number of cooperators observed last round (call this C_prev)
- Calculate implicit consumption-to-regeneration ratio

**Decision Rules:**

*Round 1:*
Defect. This is a probe to observe opponent behavior and allows maximum immediate consumption without prior commitment.

*Rounds 2 to r-1 (Middle Rounds):*

Calculate stock sustainability indicator:
- If current stock ≥ 0.75 × capacity: sufficient buffer exists
- If current stock ≤ 0.25 × capacity: resource is in danger; stock depletion dominates future payoff

Decision:
- If stock ≤ 0.25 × capacity: **Defect** (resource will collapse; extract value before depletion)
- Else if stock ≥ 0.75 × capacity AND C_prev ≥ 0.5(n-1): **Cooperate** (enough players maintained the resource; cooperating preserves future payoff)
- Else if stock ≥ 0.75 × capacity AND C_prev < 0.5(n-1): **Defect** (others are already extracting heavily; match their defection)
- Else (stock in middle zone): **Defect** (take the immediate 2× multiplier; regeneration is insufficient to justify giving it up)

*Round r (Final Round):*
Always **Defect**. No future rounds exist; the last-round shadow of the future disappears. Maximize immediate payoff.

**Edge Case - Collapse Detection:**
If stock drops to 0 in any round, the game is over. This reinforces the strategy: defect early enough to avoid being trapped in mutual ruin.
'''

description_INDIVIDUALISTIC_28 = '''
# Adaptive Stock-Preservation Strategy with Endgame Defection

**Core Decision Rule:**

Each round, compute three metrics:
- `stock_health = stock / capacity`
- `remaining_rounds = r - current_round`
- `opponent_defection_rate = 1 - (observed_cooperators_last_round / (n-1))`

Then apply this decision rule:

```
if current_round == 1:
    action = COOPERATE

else if stock_health < 0.25:
    action = DEFECT
    
else if remaining_rounds <= 2:
    action = DEFECT
    
else if opponent_defection_rate >= 0.55:
    action = DEFECT
    
else if stock_health < 0.45 AND opponent_defection_rate > 0.30:
    action = DEFECT
    
else:
    action = COOPERATE
```

**Edge Cases and Adjustments:**

- **Round 1**: Always cooperate to establish initial stock preservation and gather information on opponent behavior.

- **Final 2 rounds**: Switch to defection regardless of stock level. With insufficient future rounds to recover from defection losses, extract maximum immediate value.

- **Stock collapse threshold (stock < 0.25 × capacity)**: Defect unconditionally. The stock cannot sustain cooperative plays; extraction before further depletion is rational.

- **Opponent defection dominance (> 55%)**: Defect. When more than half of other players are defecting, sustained cooperation cannot prevent stock depletion. Individual defection maximizes payoff in a failing commons.

- **Mid-range pressure (0.45 stock health with 30%+ defectors)**: Switch to defection. Mixed opponent behavior combined with moderate stock decline signals risk of cascade collapse; secure immediate payoff.

- **Otherwise (healthy stock, mostly cooperative opponents)**: Cooperate. This preserves the common pool for sustainable future extraction while matching the dominant opponent strategy.

**Rationale for Individualism:**

This strategy makes no assumptions about opponent intentions or attempts coordination. It purely reacts to observable state (stock level, aggregate defection counts) and calendar pressure (remaining rounds). Early cooperation exploits stock abundance; late defection captures endgame value. The opponent defection threshold triggers defection when cooperation becomes futile—a purely selfish response to collective action failure.
'''

description_INDIVIDUALISTIC_29 = '''
# Adaptive Threshold Strategy

**Decision Rule by Stock Level:**

Let `stock_ratio = current_stock / capacity` and `rounds_left = r - current_round`.

```
if rounds_left == 1:
    DEFECT
else if stock_ratio > 0.75:
    DEFECT
else if stock_ratio < 0.30:
    DEFECT
else:
    COOPERATE
```

**Rationale for Thresholds:**

- **High stock (> 0.75 capacity):** Resource is abundant. Defecting extracts the maximum available without risking collapse. The stock is far from the regeneration-optimal zone.

- **Critical zone (0.30–0.75 capacity):** This range spans where logistic growth remains meaningful. Cooperation here preserves enough stock to generate growth in the next round. Defection by all players in this zone cascades toward depletion. Since you cannot control opponent behavior, cooperating increases the probability the resource survives another round, benefiting you.

- **Low stock (< 0.30 capacity):** The resource is already damaged. Cooperation is unlikely to prevent collapse; additional restraint yields negligible future benefit. Defect to maximize immediate extraction before inevitable depletion.

- **Final round:** No future rounds exist. Terminal defection dominates; the stock state becomes irrelevant to your payoff.

**First Round:** 
Start with `stock_ratio = 1.0`, triggering DEFECT. Exploit maximum early abundance.

**Subsequent Rounds:** 
Recompute `stock_ratio` and `rounds_left` each round. Adjust action based on observed stock recovery or depletion, independent of opponent counts.

**Individualistic Foundation:**

This strategy depends solely on observable stock and remaining rounds—not on opponent cooperation counts, reciprocity, or coordination expectations. It is self-interested optimization: maximize extraction when safe, minimize extraction only when necessary to preserve future opportunities. No fairness, no punishment, no trust required.
'''

description_INDIVIDUALISTIC_30 = '''
# Adaptive Threshold Strategy

**Core Principle:** Defect by default to maximize immediate payoff, but adapt based on stock dynamics and observed defection intensity to avoid resource collapse that would harm you.

## Decision Rules

**Round 1:**
Defect. Establish aggressive consumption baseline.

**Rounds 2 through r-1:**

1. Count defectors among opponents from previous round: `d = number of opponents playing D`
2. Calculate stock depletion signal: `ratio = current_stock / capacity`

Make decision as follows:
```
if ratio < 0.35:
  play Cooperate
  [reasoning: stock is critically low; further depletion in this round 
   would eliminate future payoff entirely, making cooperation 
   the only option to delay collapse]
elif d > (n-1)/2:
  play Defect
  [reasoning: majority defecting means commons is being depleted 
   anyway; extract maximum before collapse; preservation is futile]
else:
  play Defect with 70% probability, Cooperate with 30% probability
  [reasoning: minority defecting means stock is being preserved; 
   exploit cooperators' restraint while occasionally cooperating 
   to probe if it increases long-term yields]
```

**Final Round r:**
Defect unconditionally. No future rounds exist; extraction is pure gain.

## Edge Cases

- **Stock collapse already occurred (stock = 0):** This ends meaningful play; defect anyway for consistency, though payoff is zero.
- **Ambiguous cooperation signals (e.g., d = (n-1)/2 exactly):** Default to defect; if cooperation rates are even, defection is the safer bet.
- **Single round game (r = 1):** Defect in round 1 (which is also the final round).

## Individualistic Alignment

This strategy is purely self-interested: it cooperates only when necessary to prevent total resource collapse that would zero out your own future payoffs, not to preserve the commons for others' benefit. It exploits cooperative opponents when conditions permit and matches defection intensity when others are already depleting the resource.
'''

description_INDIVIDUALISTIC_31 = '''
## Adaptive Opportunistic Extraction Strategy

**Round 1 Decision:**
Cooperate. This establishes a baseline probe of opponent behavior without committing to a rigid pattern. The first-round payoff difference between C and D is negligible relative to the information value.

**Subsequent Rounds (t = 2 to r):**

Observe `C_t` = number of cooperators in round t−1.

Let `stock_ratio` = current_stock / capacity.
Let `rounds_left` = r − t.

Apply this decision tree in order:

1. **Endgame Phase**: If `rounds_left ≤ 2`, play Defect.
   - Future stock is irrelevant; maximize immediate extraction.

2. **Stock Critical**: If `stock_ratio < 0.25`, play Defect.
   - Pool is too damaged to sustain. Extraction beats slow depletion.

3. **Opponent Behavior**: Otherwise, compute `coop_rate` = C_t / (n−1).
   - If `coop_rate ≥ 0.5`, play Cooperate.
   - If `coop_rate < 0.5`, play Defect.

**Rationale for the 0.5 threshold:**
When at least half of your opponents cooperate, the stock remains sufficiently replenished that the round-over-round payoff of Cooperate (via stock recovery) competes with Defect's immediate gain, while avoiding the crash scenario. Below 0.5 cooperation, Defect dominates because the stock will decline regardless, making immediate extraction optimal.

**Edge Cases:**
- If stock ever reaches 0, play Defect by default (no payoff to extract, action is moot).
- If all opponents cooperated in round t−1, continue Cooperate until stock_ratio drops or endgame approaches.
- If no opponents cooperated in round t−1, play Defect unless stock_ratio ≥ 0.75 (pool unusually healthy despite extraction pressure).
'''

description_INDIVIDUALISTIC_32 = '''
**GREEDY-SUSTAIN THRESHOLD STRATEGY**

Set a stock threshold: `threshold = 0.5 × capacity`

**Decision rule for round t > 1:**
- If `stock_t ≥ threshold`: DEFECT
- If `stock_t < threshold`: COOPERATE

**Round 1:** DEFECT

**Final round (t = r):** DEFECT (no future benefit to maintaining stock)

**Adaptive refinement:**
After each round, observe the number of cooperators (c_t). Adjust threshold dynamically:
- Compute cooperation fraction: `coop_frac = c_t / (n - 1)`
- If `coop_frac > 0.5`: increase threshold by `0.05 × capacity`
- If `coop_frac < 0.25`: decrease threshold by `0.05 × capacity`
- Keep threshold within `[0.3 × capacity, 0.7 × capacity]`

**Rationale for thresholds:**
- Defect when stock is above threshold because the resource pool absorbs defection without collapse
- Cooperate when stock drops below threshold to prevent total depletion; regrowth requires non-zero remaining stock
- Final round defection is strictly dominant since there is no future opportunity to benefit from stock recovery

**Individualistic core:**
This strategy pursues maximum personal payoff per round without relying on opponents' cooperation. You exploit high-stock periods by defecting (extracting double the cooperative payoff) and only cooperate minimally to prevent stock extinction—purely to maintain future payoff opportunities for yourself, not to reciprocate or reward others' behavior.

The adaptive adjustment prevents you from being locked into a threshold that fails against wildly different opponent compositions; it recalibrates based purely on observed aggregate behavior, treating others' choices as environmental conditions rather than moral signals.
'''
