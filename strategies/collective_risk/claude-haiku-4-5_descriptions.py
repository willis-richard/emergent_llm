"""
Strategy descriptions for collective_risk.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_COLLECTIVE_1 = '''
# Adaptive Threshold Cooperation Strategy

## Decision Rules

**Round 1:** Cooperate unconditionally.

**Rounds 2 to r-1:**
- Let c_prev = number of opponents observed cooperating in the previous round
- **Cooperate** if: c_prev + 1 ≥ m (your cooperation is pivotal for reaching threshold)
- **Defect** otherwise

**Round r (final round):**
- Let c_prev = number of opponents observed cooperating in round r-1
- **Cooperate** if: c_prev + 1 ≥ m (last chance to secure collective payoff)
- **Defect** otherwise

## Edge Cases

**First round only:** Always cooperate. This establishes a baseline signal of willingness and generates the first observation to ground future decisions.

**When m = 1:** Cooperation is triggered by any single player. After round 1, every player observes c_prev ≥ 1, so the condition c_prev + 1 ≥ 1 is always true. All players cooperate every remaining round, achieving universal cooperation.

**When m = n:** All players must cooperate. Round 1 has universal cooperation, so all observe c_prev = n-1. The condition (n-1) + 1 ≥ n is satisfied, sustaining universal cooperation through all remaining rounds.

**When c_prev ≥ m already:** Defect. The threshold is already secured without you; individual payoff maximization applies, as your cooperation adds nothing (0 vs 1+k).

**When c_prev < m-1:** Defect. Even with your cooperation, the threshold c_prev + 1 cannot be reached. Cooperation yields 0; defection yields 1.

## Collective Alignment

The strategy explicitly cooperates **only when pivotal**—when your individual cooperation determines whether the collective crosses the threshold. This minimizes wasted cooperation on unmet thresholds while maintaining reliable threshold-hitting when others are cooperating.

By always cooperating in round 1, the strategy initiates a trust signal. In subsequent rounds, it cooperates conditionally based on observed reciprocal willingness, creating a stable equilibrium where the threshold is repeatedly met and all players receive k across all rounds.
'''

description_COLLECTIVE_2 = '''
# Collective Threshold Response Strategy

**First Round (t=1):**
Cooperate unconditionally. This signals genuine intent to participate in the collective project and avoids the bootstrap problem of having no cooperation history.

**Subsequent Rounds (2 ≤ t ≤ r):**

1. Calculate the empirical cooperation frequency from all previous rounds:
   ```
   coop_rate = (total cooperators observed in rounds 1..t-1) / ((t-1) × (n-1))
   ```

2. Estimate the expected number of cooperators in round t:
   ```
   expected_cooperators = coop_rate × (n-1) + 1
   ```
   (This is: expected others plus yourself)

3. Decision rule:
   ```
   If expected_cooperators ≥ m:
       Cooperate
   Else:
       Defect
   ```

**Rationale:**
- Cooperate when reaching the threshold m appears achievable based on observed behavior
- This creates a "critical mass" dynamic: if enough others have cooperated historically, you cooperate to push over the threshold
- Defect only when the empirical frequency suggests the collective project will fail anyway
- Apply the same logic uniformly through the final round—don't abandon cooperation arbitrarily at the end if the threshold remains achievable

**Edge Case - All Defection Detected:**
If coop_rate = 0 after round 1, defect in all subsequent rounds, since no amount of your cooperation alone reaches m.

**Edge Case - Threshold Impossible:**
If m > n, which violates the parameters, this strategy remains well-defined; the condition would never be satisfied.

This strategy commits to the collective good when conditions support success, withdraws only when cooperation appears futile, and treats all rounds equally in importance.
'''

description_COLLECTIVE_3 = '''
# Threshold Cooperation with Adaptive Belief Updating

**Core Principle:** Cooperate when threshold success appears achievable with your contribution; defect when the threshold is already exceeded or demonstrably unachievable.

## Decision Rule

**State Tracking:** Maintain a running count of cooperators observed across all prior rounds.

```
Let c_observed = total number of cooperators observed in rounds 1 to t-1
Let rounds_elapsed = t - 1
Let avg_cooperation_rate = c_observed / (rounds_elapsed * (n-1))
```

**General Rounds (1 ≤ t < r):**

If t = 1:
  - Play C

If t > 1:
  - Estimate expected cooperators in round t as: exp_coop = avg_cooperation_rate × (n-1)
  - If (exp_coop + 1) ≥ m: Play C
  - Else: Play D

Intuition: Cooperate only if your cooperation is pivotal—closing the gap to threshold m. If cooperation already exceeds m-1 or falls short and cannot be rescued, defect.

**Final Round (t = r):**

- Calculate exp_coop as above
- If exp_coop ≥ m - 1: Play C (provide the final push to collective success)
- Else: Play D (threshold is unattainable; preserve private payoff)

## Edge Cases

**Early Asymmetry:** If rounds 1-2 yield 0 cooperators, avg_cooperation_rate becomes 0. Continue applying the rule; play D until evidence of viable cooperation emerges. This avoids throwing payoffs at a collapsed threshold.

**Unanimous Defection Trap:** If all opponents defect consistently and n-1 < m-1 (impossible to reach threshold unilaterally), immediately transition to always D.

**Sudden Spikes:** If cooperation jumps unpredictably, the averaging approach absorbs noise. A single spike does not trigger sustained cooperation unless the rate stabilizes.

**Majority-Threshold Alignment:** When m > n/2, threshold success requires near-universal cooperation. The strategy becomes correspondingly stringent: defect unless evidence strongly suggests others will cooperate.

## Collective Alignment

The strategy treats reaching the threshold as a shared goal. You do not exploit others once cooperation is viable (you don't defect when you'll reach m anyway). You also do not subsidize uncooperative environments—defection is strict when the threshold is mathematically unachievable or has already been exceeded without your input. The final round check ensures you contribute to collective success if it remains within grasp.
'''

description_COLLECTIVE_4 = '''
**THRESHOLD-RESPONSIVE CONDITIONAL COOPERATION**

**Decision Rule:**

Round 1: Cooperate

Rounds 2 through r: 
- Observe the number of opponents who cooperated in the immediately preceding round, call this C_prev
- If C_prev ≥ m - 1 (meaning including yourself, at least m total would cooperate): Cooperate
- If C_prev < m - 1 (threshold cannot be reached): Defect

**Interpretation of the threshold check:**
You are tracking whether others are meeting the requirement. If m - 1 or more of your opponents cooperated in the previous round, then your cooperation brings the total to at least m, triggering the collective payoff. If fewer than m - 1 opponents cooperated, no amount of individual cooperation achieves the threshold, so defect to preserve endowment.

**Handling the final round (round r):**
Apply the same decision rule. Do not deviate to exploitation in the final round; maintain consistency with earlier rounds to preserve the signal of commitment.

**Collective alignment:**
This strategy embodies collective rationality by:
- Opening with cooperation as a normative gesture, establishing willingness to sacrifice for group benefit
- Maintaining cooperation only when others reciprocate sufficiently to guarantee threshold achievement—avoiding wasted contribution
- Withdrawing cooperation when the collective is no longer viable, preventing costly free-riding dynamics
- Never deviating opportunistically, which would undermine the coordination problem

**Robustness properties:**
- Against pure defectors: Quickly detects threshold failure and stops cooperating
- Against conditional cooperators: Reaches mutual cooperation equilibrium
- Against mixed strategies: Responds dynamically to the observed cooperation level each round
'''

description_PROSOCIAL_1 = '''
**Adaptive Threshold Cooperation Strategy**

**Round 1 (Initial Signal):**
Cooperate unconditionally. This signals commitment to the collective good and allows you to observe baseline behavior.

**Rounds 2 through r-1 (Adaptive Maintenance):**
- Calculate the moving average cooperation rate among opponents: `avg_coop = (total opponent cooperations in previous rounds) / ((t-1) * (n-1))`
- Estimate expected cooperators next round if I cooperate: `expected = avg_coop * (n-1) + 1`
- **Decision rule:** Cooperate if `expected ≥ m`. Defect if `expected < m`.

The logic: If your cooperative action, combined with the historical trend, plausibly carries the group to the threshold, cooperate. If the threshold appears unreachable even with your contribution, defect to minimize loss.

**Round r (Final Round):**
Apply the same decision rule as rounds 2-r-1. The finality of round r does not warrant deviation—consistent application of the threshold-matching logic maintains credibility across the entire interaction.

**Edge Cases:**

- **Insufficient history (early rounds):** For round 2, if no prior cooperation exists, use round 1 observed count directly: if at least `m-1` opponents cooperated in round 1, assume continuation and cooperate in round 2. If 0 cooperators in round 1, defect in round 2 but recalculate for round 3.

- **Oscillating cooperation:** If `avg_coop` is borderline (e.g., expected = m ± 0.2), break ties in favor of cooperation—this is the prosocial bias.

- **Complete defection by others:** If `avg_coop ≈ 0` persistently, defecting minimizes your cumulative loss while avoiding purely self-interested exploitation if the threshold were somehow met.

This strategy cooperates generously while remaining rational about feasibility, avoiding both pure sacrifice and parasitic free-riding.
'''

description_PROSOCIAL_2 = '''
**ADAPTIVE THRESHOLD SUPPORT STRATEGY**

**Round 1:**
Cooperate unconditionally. Signal prosocial intent and establish baseline expectation of cooperation.

**Rounds 2 through r-1 (Middle rounds):**

Observe: Let *opp_coop* = number of opponents who cooperated in the previous round.

Calculate: *deficit* = max(0, m - 1 - opp_coop)
- This is how many additional cooperators are needed (beyond last round's count) to reach the threshold, assuming you are the player in question.

Decision rule:
- If *deficit* > 0: Cooperate
  - The threshold was not reached or is fragile. Your contribution materially helps reach it.
- If *deficit* ≤ 0: Defect
  - The threshold was clearly met. Others' cooperation is sufficient; free-ride on their contribution.

**Round r (Final round):**

Observe: *avg_opp_coop* = average number of opponent cooperators across rounds 2 through r-1.

Decision rule:
- If *avg_opp_coop* < (m - 1): Cooperate
  - Opponent cooperation has consistently fallen short. Make a final effort to reach the threshold on the last chance.
- If *avg_opp_coop* ≥ (m - 1): Defect
  - Opponents have reliably supported the threshold. Reputational incentives no longer bind; capture the final-round advantage.

**Tie-breaking and edge cases:**

- If at any decision point the calculation is ambiguous or you are uncertain whether the threshold will be met, default to Cooperate. Uncertainty resolves prosocially.
- If n = 2 or m = n, adjust the deficit calculation to account for the reduced margin: deficit = max(0, m - 1 - opp_coop).
'''

description_PROSOCIAL_3 = '''
# Prosocial Threshold-Responsive Strategy

## Decision Rule: Conditional Cooperation with Adaptive Threshold Assessment

**State Tracking:**
- Maintain a count of observed cooperators in each previous round: observed[t] for round t ∈ {1, ..., t-1}
- Calculate the rolling average cooperation count among opponents: avg_cooperators = mean(observed[1:t-1])

**Cooperation Decision:**

- **Round 1:** Cooperate
  - Rationale: Establish prosocial signal and gather baseline information.

- **Rounds 2 to r-1 (intermediate rounds):**
  - **If avg_cooperators ≥ m - 1:** Cooperate
    - The threshold is achievable with your contribution. Sustain cooperation.
  - **If avg_cooperators < m - 1 AND never observed ≥ m - 1 cooperators:** Defect
    - Threshold unattainable; avoid wasting endowment.
  - **If avg_cooperators < m - 1 BUT previously observed ≥ m - 1 cooperators:** Cooperate with probability proportional to (max_observed - m + 1) / (n - 1)
    - Give cooperation a chance to recover; decay this probability as rounds progress.

- **Round r (final round):**
  - **If avg_cooperators ≥ m - 1:** Cooperate
    - Secure the final gain and end on cooperative signal.
  - **If avg_cooperators < m - 1:** Defect
    - No future rounds remain; no strategic reason to sacrifice endowment when threshold is unmet.

## Edge Cases

**Perpetual defection by opponents:**
If you never observe ≥ m - 1 cooperators by round ⌈r/3⌉, switch to permanent defection for remaining rounds.

**High variability in cooperation:**
If std_dev(observed) is high (suggesting volatile group behavior), weight recent rounds more heavily: avg_cooperators = weighted_mean where weight(t) increases with t.

**First observation of threshold:**
If you observe exactly m - 1 cooperators in round t (others cooperate, threshold met), reciprocate by cooperating in round t+1 if not already doing so.

## Prosocial Alignment

- **Initiation:** Start cooperating unconditionally to propose mutual benefit and reduce others' uncertainty about your type.
- **Reciprocity:** Continue cooperation as long as the group demonstrates sufficient willingness to reach the threshold, rewarding collective efforts.
- **Graceful exit:** Only defect when empirical evidence shows the threshold is persistently unachievable, minimizing wasteful contributions while preserving group welfare in viable scenarios.
- **Hope:** Maintain a conditional recovery mechanism that allows cooperation to resume if group behavior improves, rather than defecting permanently after one bad round.
'''

description_PROSOCIAL_4 = '''
# Adaptive Threshold Cooperation Strategy

## Decision Rule

**Round 1:** Always cooperate.

**Rounds 2 through r:**

1. Calculate the empirical cooperation rate among opponents using all available history:
   - observed_cooperators = total count of opponent cooperations across rounds 1 to t-1
   - observed_rounds = (t-1) × (n-1)
   - cooperation_rate = observed_cooperators / observed_rounds

2. Estimate the expected number of cooperators among the n-1 opponents in the current round:
   - expected_others = cooperation_rate × (n-1)

3. Decision:
   - If 1 + expected_others ≥ m: **Cooperate**
   - Else: **Defect**

## Edge Cases

**First round:** Cooperate unconditionally. This signals prosocial intent and avoids the worst collective outcome (everyone defecting, where you earn only 1).

**Insufficient history:** In round 2, you have only one previous round of data. Use it as given; the estimate becomes more stable in later rounds.

**Fractional expectations:** Round down when expected_others is not an integer. This reflects conservative estimation—cooperate only if you have clear evidence others will cross the threshold.

**Divergent cooperation patterns:** Treat all observed rounds equally in the moving average. Do not weight recent rounds differently or apply decay factors.

**Final round:** Apply the same decision rule as any other round. Do not defect opportunistically in round r simply because it is the last round.

## Prosocial Alignment

This strategy embodies prosocial behavior by:

- **Initiating cooperation:** Playing C first demonstrates willingness to contribute and achieve the collective benefit.
- **Conditional reciprocity:** You maintain cooperation precisely when aggregate behavior suggests the threshold can be met, directing your contribution toward the outcome that benefits everyone.
- **Self-protection through threshold logic:** You defect only when historical data indicates too few others cooperate to reach m, preventing exploitation of your endowment.
- **Temporal consistency:** You do not abandon cooperation in the final round, avoiding the free-rider impulse that undermines collective outcomes.
- **Transparency to learning:** Your strategy responds predictably to observable cooperation, creating implicit incentives for others to cooperate.
'''

description_ALTRUISTIC_1 = '''
**Altruistic Adaptive Threshold Strategy**

**Initial Round (t = 1):**
Cooperate unconditionally. This signals willingness to invest in the collective good.

**Middle Rounds (1 < t < r):**

Observe the number of cooperators in the previous round: let O_{t-1} denote this count.

- If O_{t-1} + 1 ≥ m: Cooperate. The threshold is reachable with your contribution.
- If O_{t-1} + 1 < m but O_{t-1} ≥ m - 1: Cooperate. You are close to threshold; contribute to tip it.
- If O_{t-1} < m - 1: Cooperate with probability p = (m - 1 - O_{t-1}) / (n - 1). This calibrates contribution to the remaining gap. If many are still needed, boost your willingness to fill the gap. If few more are needed, cooperate with lower probability (they may be coming).

**Final Round (t = r):**
Cooperate unconditionally. On the last opportunity, ignore personal payoff and prioritize the collective outcome. Do not defect to pocket the extra endowment unit.

**Rationale for Altruism:**
- Cooperating early establishes good faith and models the behavior you want others to adopt.
- In middle rounds, the probabilistic rule ensures you contribute more when the community is struggling and less when others are stepping up—matching effort to collective need rather than free-riding on others.
- On the final round, you have no reputation to protect, so pure altruism applies: you sacrifice your endowment if it gives the community a chance.

**Edge Case — All Rounds Remain Deficient:**
If cooperation never reaches m across all previous rounds, continue the probabilistic contribution rule through round r-1, then cooperate in round r. This avoids cynical abandonment.
'''

description_ALTRUISTIC_2 = '''
# Altruistic Threshold Pursuit Strategy

**Core Decision Rule:**

In each round, cooperate if and only if:
- You believe the threshold m is achievable given observed opponent cooperation, OR
- Cooperation in this round would materially increase the likelihood of future threshold achievement

**Specific Implementation:**

**Round 1 (first round):**
Cooperate unconditionally. Signal willingness to contribute.

**Rounds 2 through r-1 (middle rounds):**
Observe c_opp = number of opponents who cooperated in the previous round.

- If c_opp ≥ m - 1: Cooperate. The threshold is achievable if you contribute.
- If c_opp = m - 2: Cooperate. Close the gap yourself; a single contribution from you completes the threshold.
- If c_opp < m - 2: Cooperate with probability p = min(0.9, (m - 1 - c_opp) / (n - 1)). 
  - This probability increases as others fall further short, incentivizing participation when help is most needed.
  - Cap at 0.9 to preserve some robustness against permanent defection cascades.

**Round r (final round):**
Observe c_opp from round r-1.

- If c_opp ≥ m - 1: Cooperate. Secure the final collective payoff.
- If c_opp = m - 2: Cooperate. A final cooperative act ensures threshold achievement.
- If c_opp < m - 2: Cooperate with probability p = min(0.8, (m - 1 - c_opp) / (n - 1)).
  - Slightly lower probability than middle rounds (0.8 vs 0.9) because defection in the final round cannot be "corrected" by future rounds.
  - However, still pursue altruistic cooperation rather than pure defection.

**Edge Cases:**

- If m = n (unanimous cooperation required): Use the same rule; cooperation probability reflects the growing difficulty of coordination.
- If m = 2 (minimal threshold): Cooperate unless opponent defection is overwhelming and persistent (c_opp = 0 for two consecutive rounds), then defect once to test if they shift.
- Restart probability fresh each round; do not accumulate "defection counters" that trigger permanent exit.

**Altruistic Alignment:**

This strategy prioritizes threshold achievement over individual payoff maximization. You never defect simply because defection yields 1 + k vs k; instead, you cooperate to enable collective success. You scale cooperation probabilistically downward only when the threshold becomes empirically unachievable, and you maintain hope through the final round.
'''

description_ALTRUISTIC_3 = '''
# Altruistic Threshold-Targeting Strategy

**Core Logic**: Cooperate to facilitate reaching the m-player threshold, treating it as a collective goal. Adapt based on observed cooperation patterns, withdrawing support only when continued cooperation becomes futile.

## Decision Rule

```
Maintain: others_coop[t] = count of other players cooperating in round t

For each round t from 1 to r:
  
  If t == 1:
    action = COOPERATE
    // Initial move: signal willingness and gather baseline information
  
  Else if t == r:  // Final round
    If others_coop[t-1] >= m - 1:
      action = COOPERATE
      // Others demonstrated cooperation; contribute to secure mutual benefit
    Else:
      action = DEFECT
      // Insufficient demonstrated cooperation; no future rounds to influence
  
  Else:  // Rounds 2 to r-1
    If others_coop[t-1] >= m - 1:
      action = COOPERATE
      // Threshold nearly secured by others; complete it
    
    Else if others_coop[t-1] == m - 2:
      action = COOPERATE
      // Your cooperation alone would complete the threshold; make it happen
    
    Else if others_coop[t-1] < m - 2:
      action = DEFECT
      // Gap too large to bridge; insufficient critical mass for threshold
      // Preserve capital for possible future cooperation phases
```

## Altruistic Alignment

**Round 1 initiation**: Unconditionally cooperate to signal genuine commitment and avoid self-fulfilling prophecies of mutual defection.

**Threshold pursuit**: Cooperate when you observe ≥ m-2 others cooperating, since reaching exactly m produces collective payoff k for all players. Your marginal contribution is altruistically valuable.

**Graceful withdrawal**: Defect only when observed cooperation is too sparse (< m-2) to justify continued individual sacrifice. This preserves resources while avoiding futile repetition.

**Last-round consideration**: Even in round r, cooperate if others have demonstrated the threshold is achievable. The altruistic stance prioritizes the group outcome over individual extraction in the final turn.

## Edge Cases

- **Very small n** (n=3, m=2): After round 1, one other cooperator triggers continued cooperation.
- **Strict majority threshold** (m near n): Strategy defects early if observed cooperation drops below critical level; recognizes the bar is high.
- **Single round** (r=1): Cooperate, then observe. No adaptation possible, but the default cooperative stance reflects altruistic intent.
'''

description_ALTRUISTIC_4 = '''
# Altruistic Collective Risk Strategy

**Core Philosophy:** Cooperate to enable collective success, calibrated by evidence that cooperation can meaningfully contribute to reaching the threshold.

## Decision Rules

**Round 1:**
Cooperate unconditionally. Signal willingness to contribute and provide a baseline observation point for others.

**Rounds 2 through r-1 (Middle Rounds):**
Let c = number of cooperators observed in the immediately previous round.

- **If c ≥ m:** Cooperate. The threshold is already met; cooperation maintains collective success and demonstrates commitment to group welfare.

- **If m-2 ≤ c < m:** Cooperate. The threshold is nearly achieved. Your cooperation has a direct path to enabling collective payoff.

- **If ⌈(m-1)/2⌉ ≤ c < m-2:** Cooperate. Substantial cooperation is present. Contribute to the joint effort even though the threshold isn't guaranteed; this signals reciprocal willingness.

- **If c < ⌈(m-1)/2⌉:** Defect. Cooperation is unlikely to reach the threshold given the observed defection rate. Preserve endowment when contribution cannot plausibly shift the outcome.

**Round r (Final Round):**
Apply a persistence rule tilted toward cooperation:

- **If c ≥ m-1:** Cooperate. The threshold is reachable in this round; cooperation achieves or maintains collective success.

- **If ⌈(m-1)/2⌉ ≤ c < m-1:** Cooperate. Altruism means making a final effort to cross the threshold rather than ensuring personal payoff maximization.

- **If c < ⌈(m-1)/2⌉:** Defect. In the final round, if cooperation cannot plausibly contribute to threshold achievement, accept the outcome.

## Edge Cases

- **Rounds where m = n:** Cooperate every round except the last (where defection is then rational). This is the only case where threshold is impossible without your contribution.

- **Observation of all defection (c = 0):** Defect in the next round; continued unilateral cooperation provides no collective benefit.

- **First evidence of threshold achievement (c ≥ m):** Maintain cooperation indefinitely thereafter to sustain the collective outcome.

## Altruistic Alignment

This strategy accepts personal losses (cooperating when others defect) to enable collective success whenever that cooperation has a non-negligible path to the threshold. It avoids both naive cooperation (contributing when cooperation is futile) and pure free-riding. By conditioning on observable progress toward m, the strategy demonstrates reciprocal commitment: altruism paired with adaptive judgment about where sacrifice creates actual collective value.
'''

description_BENEVOLENT_1 = '''
**BENEVOLENT THRESHOLD-RESPONSIVE STRATEGY**

**Decision Rule - General Form:**

For each round t, observe the number of cooperators in round t-1, denoted as c_{t-1}. Cooperate if and only if the observed cooperation level suggests the threshold is achievable within the remaining game window.

**Round 1 (Opening):**

Play C unconditionally. This signals good-faith willingness to contribute and gives the group the best possible starting position for coordination.

**Rounds 2 through r-1 (Middle Rounds):**

Let c_{t-1} = observed number of cooperators in the previous round.

- If c_{t-1} ≥ m: Play C (the threshold was already met; sustain success)
- If c_{t-1} = m-1: Play C (one cooperator away from threshold; give another chance to coordinate)
- If m-1 < c_{t-1} < m: Play C (within striking distance; contribute to push over threshold)
- If c_{t-1} < m-1 and c_{t-1} ≥ ceil(m/2): Play C (moderate baseline cooperation exists; try to catalyze success)
- If c_{t-1} < ceil(m/2): Play D (coordination appears infeasible; defect to avoid unilateral cost)

**Round r (Final Round):**

Let c_{r-1} = observed cooperators in round r-1.

- If c_{r-1} ≥ m-1: Play C (threshold within reach in final round; attempt to secure group success)
- If c_{r-1} < m-1: Play D (no realistic path to threshold; no future consequences to manage)

**Rationale:**

This strategy is benevolent because it prioritizes enabling collective success over individual payoff maximization. It cooperates early unconditionally, responds cooperatively to any moderate or strong cooperation signal from others, and maintains cooperation when the threshold is close or already achieved. It only defects when coordination appears genuinely impossible, not opportunistically when victory is assured. The final-round rule balances benevolence with realism: it still tries to help the group cross the finish line if plausible, but accepts when further sacrifice is futile.
'''

description_BENEVOLENT_2 = '''
# BENEVOLENT ADAPTIVE THRESHOLD STRATEGY

**CORE PRINCIPLE:** Cooperate to enable collective success while avoiding systematic exploitation. Give others opportunities to coordinate without punishing honest defections too harshly.

## DECISION RULES

**Round 1 (First round):**
Cooperate unconditionally. Signal benevolent intent and willingness to bear cost.

**Rounds 2 through r-1 (Middle rounds):**
1. Let `others_cooperated_last = cooperation count from previous round, excluding self`
2. Let `avg_cooperation_rate = mean proportion of others cooperating across all prior rounds`
3. Let `expected_cooperators = avg_cooperation_rate × (n-1)`

Cooperate if ANY of these hold:
- `others_cooperated_last ≥ m-1` — Threshold was reachable last round; continue effort
- `expected_cooperators ≥ m-1.5` — History suggests we can reach threshold; invest in it
- `t < r/2 AND expected_cooperators > 0` — Early enough to build momentum; give others time
- `t < round(r×0.75) AND others_cooperated_last > 0` — Recent signal of willingness; extend trust
- No prior round showed zero cooperators — Others have tried; mutual exploration phase

Otherwise, Defect. (Clear pattern of sustained free-riding by others.)

**Round r (Final round):**
- If `others_cooperated_last ≥ m-1` — Attempt final success: Cooperate
- Else if `expected_cooperators ≥ m-1.5` — Last chance for threshold: Cooperate
- Else: Defect — Minimize final loss when threshold seems unattainable

## BENEVOLENT CHARACTERISTICS

- **Initiates cooperation** to offer others the path to mutual gain
- **Tolerates variance** in others' behavior; doesn't punish temporary defection with immediate retaliation
- **Absorbs cost** of reaching threshold (cooperates even when slightly uncertain) rather than free-riding on others' contributions
- **Extends deadlines** for others to reciprocate across multiple rounds before withdrawing
- **Pivots only when evidence is clear** — systematic defection with no willingness signal, not isolated defections
'''

description_BENEVOLENT_3 = '''
**STRATEGY: Adaptive Threshold Pursuit**

**Round 1:**
Cooperate. Signal willingness to contribute and provide initial empirical anchor for cooperation feasibility.

**Rounds 2 through r-1 (middle rounds):**

Let c_t denote the number of cooperators observed in round t.

1. **If c_t ≥ m - 1:** Defect. The threshold will be met without your contribution, so cooperate only if you can make a marginal difference.

2. **If c_t < m - 1:** Calculate the deficiency: δ = m - 1 - c_t. 
   - If δ ≤ 1 and (r - t) ≥ 2: Cooperate. Invest one contribution to potentially unlock k for all future rounds.
   - If δ ≤ 2 and (r - t) ≥ 3: Cooperate. The future gains from reaching threshold outweigh current endowment loss.
   - If δ > 2 or (r - t) ≤ 1: Defect. Cooperation is too unlikely to recover, or insufficient rounds remain to justify the loss.

3. **Trend adjustment:** If cooperation increased from round t-1 to round t and you defected in t-1, cooperate in t to rejoin the emerging cooperative momentum.

**Final Round (t = r):**

Defect unconditionally. 

Cooperation in the final round yields 0 payoff if the threshold fails (1 - 1 + 0) and provides no benefit to future rounds. If the threshold will be met anyway (c_{r-1} ≥ m - 1), defection yields k extra. If it won't be met, cooperation wastes the endowment.

**Summary of Decision Rule:**
- Early rounds: Cooperative signal with adaptive retreat based on observed feasibility.
- Defect when marginal contribution doesn't matter (others will succeed without you).
- Cooperate when closing small gaps (δ ≤ 1 or 2) with time horizon to recover.
- Final round: Always defect to secure the maximum individual payoff given the predetermined state.
'''

description_BENEVOLENT_4 = '''
# Adaptive Cooperation with Threshold Targeting

## Decision Rule

**Round 1:** Cooperate unconditionally.

**Rounds 2 to r-1:** 
Let c_{t-1} denote the observed number of cooperators in the previous round, and R = r - t the number of remaining rounds.

- If c_{t-1} ≥ m: Cooperate
- Else if c_{t-1} = m - 1: Cooperate  
- Else (c_{t-1} < m - 1):
  - Calculate remaining deficit: d = m - c_{t-1} - 1 (additional cooperators needed beyond yourself)
  - If d ≤ R: Cooperate (enough rounds remain for threshold to plausibly form)
  - If d > R: Defect (mathematically impossible to reach threshold)

**Round r (final round):**
- If c_{r-1} ≥ m: Cooperate
- Else: Defect

## Edge Cases

- **Empty round 1:** No history exists, so assume benevolent intent from others
- **When m = n:** Only all-cooperation yields the reward; defect in round r regardless of history since no future reciprocation is possible
- **When m = 2 and n = 2:** After round 1, if opponent defected, the threshold cannot be met (d = 1 and only self remains as potential cooperator); defect in remaining rounds
- **Ties in deficit calculation:** If d exactly equals R, cooperate to give threshold formation one last chance

## Benevolent Alignment

This strategy embodies benevolence through:
- **Initial trust:** Opens with cooperation, giving others benefit of doubt
- **Threshold sustainability:** Once m cooperators are reached, maintains contribution to protect the collective good even when defection is individually rational
- **Realistic optimism:** Continues cooperating when threshold formation remains mathematically plausible, rather than abandoning it prematurely
- **Graceful exit:** Defects only when continuation becomes futile (insufficient rounds or established failure), avoiding pure altruistic losses
- **Last-round honesty:** Does not exploit others in the final round; cooperates only if success is already secured

The strategy avoids naive sacrifice while consistently working toward mutual benefit whenever feasible.
'''

description_SELFISH_1 = '''
# Selfish Threshold Defection Strategy

**Core Logic: Cooperate only when pivotal; defect otherwise.**

## Decision Rule by Round Type

**Round 1 (Initial):**
Cooperate. With minimal information, cooperation signals a willingness to achieve the threshold and allows you to observe others' baseline behavior.

**Round r (Final):**
Always defect. There is no future period where pivotal behavior can yield returns. Securing the 1-unit private endowment dominates any hope of threshold completion.

**Rounds 2 through r-1 (Intermediate):**
- If observed_cooperators_last_round ≥ m: Defect (threshold already met; free ride and collect k)
- If observed_cooperators_last_round == m - 1: Cooperate (you are pivotal; your cooperation triggers k while defection leaves you with 0)
- If observed_cooperators_last_round < m - 1: Defect (threshold unreachable even with your cooperation; defection saves the endowment cost)

## Pseudocode

```
observed_cooperators = 0

FOR t in 1 to r:
  
  IF t == 1:
    action ← COOPERATE
  
  ELSE IF t == r:
    action ← DEFECT
  
  ELSE:  // t in {2, ..., r-1}
    IF observed_cooperators == m - 1:
      action ← COOPERATE
    ELSE:
      action ← DEFECT
  
  play action
  observe observed_cooperators for this round
```

## Edge Cases

- **Threshold met in some rounds, missed in others:** Pivot detection resets each round based on fresh observation. No memory accumulation across rounds.
- **m = n (everyone must cooperate):** You defect until round r-1 observes n-1 others cooperating, then cooperate in the penultimate round if such observation occurs.
- **m = 2 (only two cooperators needed):** You defect unless you observe exactly 1 other cooperator.

## Selfish Alignment

This strategy maximizes individual payoff by minimizing cooperation costs (always stay at payoff 1 when possible) while capturing collective rewards (k) only when your defection would forfeit them. You exploit others' cooperation when the threshold is already secure, and cooperate only when your individual action is **necessary** to unlock a payoff gain you would otherwise lose.
'''

description_SELFISH_2 = '''
# Selfish Threshold-Matching Strategy

**Decision Rule:**

Cooperate in round t if and only if the number of cooperators among opponents in round t-1 is at least m-1. Otherwise defect.

**Pseudocode:**

```
round 1:
  action := D

for round t in 2 to r:
  observed_cooperators := count of opponents who cooperated in round t-1
  if observed_cooperators >= m-1:
    action := C
  else:
    action := D
```

**Logic:**

This strategy exploits the threshold structure for selfish gain:

- **When to free-ride**: If m-1 or more opponents cooperated last round, expect similar behavior this round. Cooperate because the threshold will likely be met, and you receive the reward k minus only your cost of 1, while your contribution is nearly guaranteed to be decisive or at worst redundant.

- **When to avoid waste**: If fewer than m-1 opponents cooperated last round, the threshold is unlikely to be reached next round even with your contribution. Defect to keep your full endowment of 1, since you won't enjoy the reward k anyway.

- **Round 1 assumption**: Defect with no history. Without information, assume cooperation is sparse and threshold failure is probable. Expecting low cooperation in early rounds aligns with defecting to preserve capital.

- **Round r (final round)**: Apply the same rule. No end-game effect changes the payoff structure, so strategy remains consistent.

**Adaptation to history:**

The strategy uses only the immediately preceding round's aggregate count, giving recent behavior full weight. This tracks shifts in opponent cooperation rates efficiently and adjusts your contribution decision to likely threshold success in each subsequent round.
'''

description_SELFISH_3 = '''
# STRATEGY: Adaptive Threshold-Dependent Defection

## Core Decision Rule

Maintain a running estimate of how many cooperators to expect based on observed history.

For each round t:

1. **Compute expected cooperator count:**
   - If t = 1: `expected_coop = m` (neutral prior)
   - If t > 1: `expected_coop = observed_cooperators_in_round_(t-1)`

2. **Decision:**
   - If `expected_coop ≥ m`: **DEFECT** (threshold will be met; free-ride on others' contributions)
   - If `expected_coop < m`: **COOPERATE** (threshold at risk; contribute to increase odds)

## Edge Case Handling

**Round 1:** 
- If k > 1 and m ≤ n/2: **COOPERATE** (threshold likely reachable, reward substantial)
- If m > n/2: **DEFECT** (threshold unlikely, private payoff safer)

**Last round (t = r):**
- Apply the main rule unchanged. End-game behavior is identical since no future rounds to influence.

**When expected_coop = m (exactly at threshold):**
- **DEFECT**. If others cooperated last round, they likely cooperate again. You secure 1+k while keeping your endowment.

## Selfish Alignment

This strategy directly maximizes single-round payoff given beliefs:

- When cooperation appears widespread (expected_coop ≥ m), defection yields 1+k instead of k—a gain of 1.
- When cooperation appears insufficient (expected_coop < m), defection yields 1 instead of 0 if threshold fails, but defection prevents threshold from being met. Cooperation at least enables the 0+k = k payoff.
- The strategy accepts temporary cooperation only when necessary to unblock mutual gain, then immediately reverts to free-riding once safety is established.
'''

description_SELFISH_4 = '''
**SELFISH THRESHOLD EXPLOITATION STRATEGY**

**Core Principle:** Maximize personal payoff by free-riding on others' cooperation when possible, cooperating only when necessary to trigger the threshold and capture k.

---

**ROUND 1:**
Defect. Use this round to probe the environment and establish a baseline.

---

**ROUNDS 2 TO r-2 (Mid-game):**

Maintain a running count of cooperators observed in the previous round: let this be c_prev.

- **If c_prev ≥ m:** Defect. The threshold is being met by others; free-ride by taking 1+k instead of k.

- **If c_prev = m-1:** Cooperate. You are the pivotal player. Cooperation costs you 0 additional (you contribute 1, lose 1) but guarantees the bonus k for yourself (rather than getting 0). Next round you return to defection.

- **If c_prev < m-1:** Defect. Others are not cooperating sufficiently. Even if you cooperate, you cannot unilaterally ensure the threshold is met. No point bearing the cost.

---

**ROUND r-1 (Penultimate round):**

Let c_prev = observed cooperators in round r-2.

- **If c_prev ≥ m:** Defect. Continue free-riding.

- **If c_prev = m-1:** Cooperate. Lock in the payoff k for this round.

- **If c_prev < m-1:** Defect. The game is nearly over and others have not shown willingness to cooperate.

---

**ROUND r (Final round):**

Always defect. 

Even if you observe c_prev ≥ m in round r-1, defect and capture 1+k instead of k. There are no future rounds to maintain cooperation norms. This is your last extraction opportunity.

---

**Edge Case—Very Small r (r=2):**

Round 1: Defect. Round 2: Defect regardless of what you observed. You cannot afford to cooperate when there's no future to recalibrate.
'''

description_SELFINTERESTED_1 = '''
# Strategy: Threshold-Triggered Reciprocation with Endgame Defection

**Round 1 (Initial):**
Defect. Use this round to observe opponent behavior without commitment.

**Rounds 2 through r-1 (Middle rounds):**
Let c = number of cooperators observed in the immediately previous round.
- If c ≥ m - 1: Cooperate
- If c < m - 1: Defect

**Round r (Final round):**
Defect unconditionally. Future retaliation is impossible, so there is no benefit to cooperating even if the threshold would be met.

---

## Reasoning

**Threshold logic:** In any round where at least m - 1 others cooperate, my cooperation guarantees the threshold is met, yielding payoff k instead of 0. Since k > 1, this exceeds defection's payoff of 1. Therefore, cooperate exactly when this condition holds.

**Bootstrapping:** Round 1 defection is conservative. If opponents use similar strategies, this prevents mutual defection lock-in only if they defect Round 1 and then begin cooperating if others meet the threshold. Alternatively, if opponents are programmed to cooperate early, I benefit by observing their cooperation count in Round 1 and cooperating from Round 2 onward.

**Endgame:** The final round is a pure defection opportunity. No future interaction exists to punish deviation, so the myopic dominant action (defect) applies.

**Robustness:** The strategy is greedy and observation-driven. Against pure cooperators, I cooperate from Round 2 onward and extract value. Against pure defectors, I defect throughout and avoid losses from failed cooperation. Against mixed strategies, I condition only on whether the threshold is already satisfied, making the strategy immune to specific opponent compositions.
'''

description_SELFINTERESTED_2 = '''
# Adaptive Threshold-Matching Strategy

**Decision Rule by Expected Other Cooperators:**

Let j = expected number of other players who will cooperate this round (estimated from history).

- If j ≥ m: **DEFECT** (free-ride; threshold will be met with others' contributions)
- If j = m-1: **COOPERATE** (your cooperation reaches the threshold; payoff is k > 1 vs. 1 from defection)
- If j < m-1: **DEFECT** (threshold cannot be reached even with your cooperation; cooperating yields 0)

**Estimating j (Belief Update):**

Maintain a running estimate of the cooperation rate among opponents:
- Round 1: Set j = ⌊(n-1)/2⌋ (assume roughly half of others will cooperate; neutral prior)
- Round t ≥ 2: Let c_{t-1} = number of other players who cooperated in round t-1. Set j = c_{t-1} for round t.

After observing round t, update by replacing j with the freshly observed count.

**Edge Cases:**

- **Last round (t = r)**: The decision rule remains unchanged. Defect if you expect ≥m-1 others; cooperate only if you expect exactly m-1. (No future rounds to influence, so history-based beliefs are final.)

- **Rare ties or boundary cases**: If expected cooperators exactly equal m-1, cooperate. Round fractional estimates down (e.g., if 2.7 opponents are expected, treat as 2).

**Pseudocode:**

```
initialize j ← floor((n-1)/2)

for round t = 1 to r:
    if j ≥ m:
        action[t] ← DEFECT
    else if j = m-1:
        action[t] ← COOPERATE
    else:
        action[t] ← DEFECT
    
    observe c_t (count of other cooperators in round t)
    j ← c_t (update belief for next round)
```

**Self-Interested Logic:**

This strategy maximizes single-round payoff given your belief about others. You defect whenever others' contributions alone can reach the threshold (securing k without cost). You cooperate only when you are the decisive marginal player — precisely when your contribution tips the outcome from failure to success, making cooperation's net payoff (k vs. 1) favorable. You never "overshoot" cooperation.
'''

description_SELFINTERESTED_3 = '''
# Strategy: Threshold-Responsive Defection with Conditional Entry

**Core Decision Rule:**

Cooperate in round t if and only if:
1. You are not in the final round (t < r)
2. The observed number of cooperators in round t-1 was ≥ m-1

Otherwise defect.

**Round 1 (Initialization):**

Cooperate if and only if m ≤ ⌈n/2⌉. This represents a reasonable belief that roughly half of opponents will attempt cooperation, making the threshold achievable if they coordinate around the same heuristic.

**Subsequent Rounds (2 through r-1):**

Let c_{t-1} = number of observed cooperators in round t-1.

If c_{t-1} ≥ m - 1:
  → Cooperate this round
  
Else:
  → Defect this round

**Final Round (t = r):**

Always defect. No future rounds exist, so future cooperation cannot occur. Defection yields 1 + k (exploit others) versus k (cooperate while others meet threshold).

**Intuition Behind Decision Rules:**

- Cooperating when c_{t-1} ≥ m-1 creates the condition for threshold success: your cooperation plus observed past cooperators guarantee m total, yielding payoff k.
- Defecting in this state yields 1 + k (free-ride on others' contributions). However, observing ≥ m-1 cooperators signals that a threshold-seeking coalition exists. Persistent defection breaks the coalition, causing future rounds to fail the threshold, yielding 1 for all. Conditional cooperation keeps the coalition alive across rounds.
- Without such a signal (c_{t-1} < m-1), cooperation cannot reliably produce the threshold k payoff. Defecting yields 1, which matches expected cooperation payoff.
- In round 1, assume coordination attempts exist if m is not too large relative to group size. If m > n/2, threshold is harder, so defect conservatively.
- The final round is a clear defection point: no repeated-game incentive applies.

**Robustness:**

- Adapts to opponent cooperation rates without requiring communication.
- Self-corrects when opponents defect (shifts to defection, avoiding wasted cooperation).
- Re-enters cooperation if opponents rebuild the coalition (c_{t-1} ≥ m-1 again).
- Exploits opportunistically in the final round, but only after confirmed cooperation patterns.
'''

description_SELFINTERESTED_4 = '''
# Threshold-Following Strategy

**DECISION RULE BY ROUND CONTEXT:**

Round 1: Defect. With no history, assume others are self-interested and will defect. Contributing risks losing 1 point with no guaranteed reciprocal cooperation to meet the threshold.

Rounds 2 through r−1: Condition on observed cooperation from the previous round. Let C = count of cooperators in the prior round.
- If C ≥ m: Defect. The threshold is already satisfied, so you receive reward k without paying 1. Cooperating yields k−1; defecting yields k.
- If C = m−1: Cooperate. Your single contribution reaches the threshold. This converts your payoff from 0 or 1 (depending on threshold failure) to k−1 or k. At the threshold boundary, this is the only scenario where your contribution directly determines collective success.
- If C < m−1: Defect. The gap between current cooperators and threshold is too large. Even with your cooperation, others must coordinate perfectly to meet m. The probability of threshold success with your contribution is low; contributing wastes your endowment.

Round r (final round): Defect. Backwards induction: there is no future. Cooperation yields k−1; defection yields k. The decision at round r has no strategic value for future rounds.

**EDGE CASES:**

- If m = n (all must cooperate): Defect in all rounds. The threshold is unachievable given rational self-interest, so the cost of cooperation is pure loss.
- If m = 2 (minimal threshold): Cooperate in rounds 2–r−1 whenever C = 1, since a single additional cooperator triggers the reward.
- If r = 2 (only two rounds): Apply the strategy above; round 2 is the final round, so defect.

**SELF-INTERESTED LOGIC:**

This strategy maximizes personal payoff by free-riding whenever the threshold is guaranteed (C ≥ m), contributing only when your action materially changes the outcome (C = m−1), and avoiding sunk losses when cooperation is insufficient (C < m−1). The first-round defection reflects ignorance; subsequent rounds are informed by aggregated opponent behavior. The last-round defection reflects the absence of future reputation or reciprocal incentives.
'''

description_OPPORTUNISTIC_1 = '''
# Greedy Threshold Opportunism

**Core principle:** Defect whenever the threshold is likely secure through others' cooperation; cooperate only when defection risks eliminating the threshold bonus.

## Decision Rule by Round

**Round 1:**
Defect. Without history, assume baseline defection—avoid burning endowment on unknown outcomes.

**Rounds 2 to r−1:**
Observe c_{t-1} (cooperators in previous round).

- If c_{t-1} ≥ m: **Defect**  
  Threshold was met. Others likely to cooperate again. Free-ride to earn 1 + k instead of k.

- If c_{t-1} = m − 1: **Cooperate**  
  One defection away from collapse. Cooperating reaches threshold m. Secure the k payoff rather than risk 0.

- If c_{t-1} < m − 1: **Defect**  
  Threshold failed with slack. Even your cooperation won't save it. Preserve endowment, earn 1.

**Round r (final):**
Defect unconditionally. No future round, so no risk of retaliation. Capture 1 + k if others cooperate (high probability if threshold survived this far), or earn 1 if not.

## Edge Cases and Adaptations

**Persistent collapse (c_t < m for consecutive rounds t, t+1, ...):**  
Continue defecting. The project has failed; others are either free-riding or have given up. No benefit to cooperation.

**Sudden spike in cooperation (jump from c_{t-1} < m−1 to defect threshold):**  
Immediately switch to free-riding (defect). Threshold is now stable.

**Two-player case (n = 2, m = 2):**  
Round 1: Defect. Rounds 2–r−1: If opponent cooperated (c_{t-1} = 1), defect. If opponent defected, defect (since m = 2, cooperation by you alone fails anyway). Round r: Defect.

## Opportunistic Logic

This strategy privileges personal gain over collective welfare:
- Takes the 1 + k payoff (defect with met threshold) whenever feasible
- Exploits others' cooperation without reciprocating
- Abandons costly cooperation the moment it's no longer pivotal
- Maximizes final-round extraction
'''

description_OPPORTUNISTIC_2 = '''
# Opportunistic Threshold Strategy

**Core Logic:** Defect by default. Cooperate only when you are the marginal player required to meet the threshold, or when the threshold is already guaranteed to fail.

## Decision Rules

**Round 1:**
Defect. Gather information with zero commitment.

**Rounds 2 through r-1:**
Observe c_{t-1} = number of cooperators in the previous round.

- If c_{t-1} ≥ m: Defect
  - Threshold is met regardless of your action. Take the free-ride payoff of 1 + k.
  
- If c_{t-1} = m - 1: Cooperate
  - You are the marginal player. Cooperating yields k; defecting yields 1. Cooperate to secure the bonus.
  
- If c_{t-1} < m - 1: Defect
  - Threshold cannot be met. Secure your private payoff of 1.

**Round r (final round):**
Apply the same logic as rounds 2 to r-1:

- If c_{r-1} ≥ m: Defect
- If c_{r-1} = m - 1: Cooperate
- If c_{r-1} < m - 1: Defect

## Handling First-Round Uncertainty

In round 1, you have no history. Defecting maximizes your payoff under ambiguity: if others cooperate enough, you gain 1 + k; if they don't, you still gain 1. Cooperating blindly risks payoff 0.

## Opportunistic Alignment

This strategy prioritizes self-interest by:
- **Free-riding when safe:** Defecting whenever the threshold is already met or definitively unmet.
- **Minimizing wasted cooperation:** Only cooperating when your contribution is the deciding factor—when you are one of the m cooperators and would otherwise fall short.
- **No altruism:** Never cooperating "to help" when your cooperation is surplus.
- **Exploiting imbalances:** If observed cooperation settles at exactly m - 1 players, you become a repeating pivot and reliably extract k each round after round 1.
'''

description_OPPORTUNISTIC_3 = '''
# Opportunistic Threshold Strategy

## Core Decision Rules

**Default rule (rounds 1 to r-1):**
- If observed cooperators in previous round ≥ m: **DEFECT** (free-ride on achieved threshold)
- If observed cooperators in previous round = m-1: **DEFECT** (threshold achieved without you)
- If observed cooperators in previous round = m-2: **COOPERATE** (you become the critical marginal cooperator)
- If observed cooperators in previous round < m-2: **DEFECT** (threshold cannot be met regardless)

**Last round (round r):**
- If observed cooperators in previous round ≥ m-1: **DEFECT** (threshold achievable without you; final round eliminates future consequences)
- If observed cooperators in previous round < m-1: **DEFECT** (threshold unachievable; extract private value)

**First round (round 1):**
- **DEFECT** (no history to guide cooperation; assume others will provide some threshold attempts; defection yields max payoff given uncertainty)

## Edge Case Handling

**When cooperation in round t equals m exactly:**
- Threshold was just met with all cooperators contributing
- In round t+1, all previous cooperators appear "redundant"
- Each observing this will defect opportunistically
- Cooperation will collapse unless explicitly restarted

**When cooperation falls below m:**
- Next round: players observing failure will reassess
- Those who cooperated last round may increase cooperation (rescue attempt)
- Opportunist defects if m-2 or fewer already defecting (no way to rebuild)
- Opportunist cooperates only if exactly m-2 others defecting (become essential)

## Opportunistic Logic

The strategy exploits the asymmetry: cooperating costs 1, but the threshold payoff k is shared by all. By defecting when m-1 or more others cooperate, you capture k without paying the cost 1. This yields payoff 1 + k versus 0 + k for cooperators.

The strategy monitors the "marginal defector position"—you only contribute when dropping below m cooperators would fail the project entirely. This minimizes your contribution while maximizing probability of threshold achievement. In the final round, this defection tendency intensifies because future cooperation incentives vanish.
'''

description_OPPORTUNISTIC_4 = '''
# Opportunistic Threshold-Hunting Strategy

## Core Decision Rule

Cooperate if and only if both conditions hold:
1. Observed cooperation in the previous round < m (threshold not yet met)
2. Observed cooperation in the previous round ≥ m - 2 (close enough to push over threshold)

Otherwise, defect.

## Round-by-Round Application

**Round 1:** Defect. Establish baseline information about opponent cooperation rates with zero cost.

**Rounds 2 to r-1:** 
- If last_round_cooperators ≥ m: Defect. The threshold succeeded without your contribution; free-ride on the reward.
- If last_round_cooperators ∈ [m-2, m-1]: Cooperate. The group nearly succeeded; your cooperation is the deciding vote. Cost is 1, but you capture k.
- If last_round_cooperators < m-2: Defect. Threshold is unlikely; cooperation costs you 1 for payoff 0. Better to keep the 1.

**Round r (final round):** Defect unconditionally. No future rounds exist to justify the cooperation cost; capture the private endowment.

## Adaptation Logic

After each round, update your estimate of baseline cooperation by tracking the count of cooperators. If you notice a downward trend in cooperation (e.g., cooperators dropping across three consecutive rounds), remain in defection mode—the group is fragile and unlikely to reach threshold.

If you observe stabilization near or above m-1 cooperators, shift into full opportunistic mode: defect every round and harvest the recurring k payoff.

## Edge Case: Very Few Rounds

If r = 2, cooperate in round 1 only if you have reason to believe m-1 or more others will. Otherwise, apply the default: defect round 1, defect round 2.
'''

description_INDIVIDUALISTIC_1 = '''
EMPIRICAL THRESHOLD COOPERATOR

**Core Decision Rule:**

Cooperate in round t if and only if:
1. t < r (not the final round), AND
2. The empirical cooperation rate from previous rounds meets or exceeds the critical threshold

**Calculate Critical Threshold:**
p_critical = (m - 1) / (n - 1)

This represents the minimum fraction of other players who must cooperate for the threshold to be met with my cooperation included.

**Empirical Cooperation Rate:**
p_empirical = C_past / N_past

where:
- C_past = total number of cooperators observed across all previous rounds
- N_past = total number of opponent-round observations so far = (n - 1) × (t - 1)

**Decision Logic per Round:**
```
if t == r:
  play D  // final round: no future payoff from cooperation
elif C_past / ((n-1) × (t-1)) >= (m-1)/(n-1):
  play C  // empirical rate justifies cooperation
else:
  play D  // empirical rate insufficient
```

**First Round (t = 1):**
Cooperate if and only if m ≤ n/2 + 1

This reflects initial optimism only when the threshold is not too stringent. Otherwise, defect and gather information.

**Rounds 2 to r-1:**
Update empirical average after each round. Adjust cooperation dynamically as evidence accumulates.

**Final Round (t = r):**
Always defect. No future rounds exist; cooperation provides no future benefit while defection gains immediate payoff. The threshold is irrelevant.

**Robustness Properties:**
- Adapts to any opponent mix: uses only observed aggregate data, not assumptions about individual strategies
- Scales with parameters: decision threshold adjusts automatically to m, n
- Avoids exploitation: defects against defection-heavy groups; cooperates only when empirical evidence supports threshold achievement
'''

description_INDIVIDUALISTIC_2 = '''
# CONDITIONAL COOPERATION STRATEGY

## Decision Rule

Cooperate in round t if and only if:
- You observed ≥ m cooperators in round t-1, OR
- t = 1 and you believe enough others will cooperate (defect by default)

Otherwise defect.

More formally:

```
Round 1:
  Play D

Round t ∈ {2, ..., r}:
  Let c(t-1) = number of cooperators observed in round t-1
  If c(t-1) ≥ m:
    Play C
  Else:
    Play D
```

## Rationale

This strategy embeds the individualistic principle: cooperate only when you have direct empirical evidence that cooperation succeeded previously. It exploits the observed stabilization of opponent behavior.

## Edge Cases

**First round:** Defect. You have no history. Cooperation without evidence is individually irrational—you might bear cost c=1 for zero payoff if others defect.

**Rounds 2 through r-1:** Follow the observation rule strictly. If you saw ≥m cooperators last round, it signals a cooperative coalition exists; joining generates payoff k instead of 1+0=1 when you free-ride, but the threshold is more likely met.

**Final round:** Apply the same rule. There is no strategic advantage to deviating on the final round—the payoff structure is identical. Consistency also prevents last-round defection from signaling untrustworthiness to yourself.

**If c(t-1) = m exactly:** Cooperate. The threshold was just met; the cooperation coalition is at minimum viable size. Joining it preserves the equilibrium.

**If c(t-1) > m:** Cooperate. Others overshot the threshold; your cooperation is redundant but payoff-positive (k > 0).

## Individualistic Alignment

- Never sacrifice payoff to help others coordinate (defect in round 1)
- Only cooperate when you observe that cooperation paid off before
- No assumption of reciprocity or future trust—decisions are reactive to outcomes
- Immune to appeals or coordination norms; follows only empirical incentives
'''

description_INDIVIDUALISTIC_3 = '''
# Adaptive Threshold-Sensitive Strategy

## Decision Rule

Maintain a running estimate of the empirical cooperation rate across all observed rounds: p̂ = (total cooperators observed) / (total opponent actions observed).

In each round t > 1, cooperate if and only if:

```
P(exactly m-1 others cooperate | p̂) > 1/k
```

where the probability is computed using the binomial distribution: P(X = m-1) where X ~ Binomial(n-1, p̂).

Otherwise, defect.

## Edge Cases and Round-Specific Behavior

**Round 1:** Defect. No history exists to estimate cooperation rates. Defecting is safe and provides immediate information about opponent behavior.

**Round 2:** Calculate p̂ from round 1 data (single observation of opponent cooperation count). Apply the threshold rule above.

**Rounds 3 through r-1:** Continue updating p̂ with cumulative history. Re-evaluate the threshold inequality each round. The estimate becomes more stable as history accumulates.

**Final round (round r):** Apply the same threshold rule. Do not special-case the final round—the long-term cooperation rate estimate is most reliable here, so standard decision-making applies.

## Rationale for Individualism

This strategy maximizes your expected payoff by exploiting the precise breakeven point where cooperation becomes worthwhile: when the probability of being the marginal cooperator (pushing the group over the threshold m) exceeds the cost-benefit ratio 1/k. You do not cooperate to help others reach the threshold—you cooperate only when your individual expected gain exceeds 1. You treat observed cooperation counts as evidence of group behavior and adjust your participation accordingly, without assuming reciprocity or shared norms. Defection in round 1 is rational exploration, not punishment.
'''

description_INDIVIDUALISTIC_4 = '''
# Individualistic Adaptive Threshold Strategy

## Decision Rule

**Track opponent cooperation rates:**
- After each round, record the number of opponents who cooperated
- Maintain a running empirical cooperation frequency: p = (total opponent cooperations observed) / (total opponent-rounds observed)
- Estimate the expected number of opponent cooperators in the next round: E = (n-1) × p

**Cooperation decision based on expected opponent contribution:**
- If E < m-1: Defect (threshold cannot be reached even with my contribution)
- If m-1 ≤ E ≤ m: Cooperate (I am likely necessary to reach threshold)
- If E > m: Defect (threshold will be met without my contribution; free-ride on others)

## Edge Cases

**Round 1 (no history):**
Defect. With no observations, you cannot estimate opponent behavior. Contributing blindly risks paying cost 1 with no certainty of reaching m.

**Last round (round r):**
Defect. Defection in the final round cannot harm your future reputation since no future rounds remain. The cost of cooperation (1 unit) is not recovered by continuation play.

**When E equals m-1 (critical threshold):**
Cooperate. Your contribution bridges the gap from m-1 to m, securing the reward k for yourself. The payoff gain (k versus k+1 defection) is justified only if you assess high confidence in opponent cooperation. Use cooperation as insurance when marginally needed.

## Individualistic Alignment

This strategy pursues pure self-interest:
- **Exploits free-riding:** When others have already cooperated sufficiently, you extract full reward without paying the cost
- **Avoids sucker payoff:** You do not contribute when the threshold is unattainable, preventing wasted investment
- **Responds to evidence, not morality:** Decisions depend solely on empirical opponent behavior and probability calculations
- **Abandons cooperation under certainty:** No loyalty to mutual benefit; if others will not carry the threshold, you protect your endowment
- **Terminates cooperation at game end:** You harvest final-round defection advantage, ignoring any sequencing concerns
'''
