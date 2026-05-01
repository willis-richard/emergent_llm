"""
Strategy descriptions for common_pool.

Generated with:
- Provider: OpenAI
- Model: gpt-5.4-mini
"""


description_COLLECTIVE_1 = '''
Initialize in cooperative mode.

For round 1, play C.

For each later round t:

- Let `k` be the number of opponents who cooperated in round `t-1`.
- Let `m = n - 1`.
- Let `support = k / m`.

Decision rule:
- If `t = r`:
  - play C if `stock > 0`; otherwise play D.
- Else if `stock <= capacity / 3`:
  - play C only if `support = 1` for two consecutive rounds; otherwise play D.
- Else if `support >= 1/2`:
  - play C.
- Else:
  - play D.

Recovery rule after any D:
- Stay in recovery until both of the following hold:
  - at least `2/3` of opponents cooperated in the last round,
  - current `stock > capacity / 3`.
- While in recovery, play D until those conditions are met; then return to C.

If `n = 2`, interpret the thresholds as:
- `support >= 1/2` means the single opponent cooperated.
- `support >= 2/3` also means the single opponent cooperated.

If the observed cooperation count is missing or inconsistent with the current round, treat it as `k = 0` and play D.
'''

description_COLLECTIVE_2 = '''
Round 1: cooperate.

For round t > 1, let:
- `S` be the current stock at the start of the round
- `m` be the number of opponents who cooperated in the previous round
- `a` be your own previous action (`C` or `D`)
- `k = m + 1` if `a = C`, otherwise `k = m`
- `q = k / n` be the previous-round total cooperation share

Use three stock zones:

- `high` if `S >= 0.8 * capacity`
- `medium` if `0.5 * capacity <= S < 0.8 * capacity`
- `low` if `S < 0.5 * capacity`

Set the required cooperation threshold from the previous round as:
- `T = 0.5` in `high`
- `T = 0.75` in `medium`
- `T = 1.0` in `low`

Maintain a punishment counter `p`:
- initialize `p = 0`
- if `q >= T`, set `p = 0`
- otherwise set `p = p + 1`

Decision rule:
- If `t = r` (last round), cooperate.
- Else if `S = 0`, cooperate.
- Else if `q >= T`, cooperate.
- Else if `p >= 2` and `S < 0.8 * capacity`, defect.
- Else cooperate.

Edge handling:
- If `n = 2`, interpret `m` as the single opponent’s action; the same rule applies.
- If the previous round cannot be evaluated because this is round 1, use the round-1 action `C` as the baseline.
- If the stock is extremely low, never defect; cooperate to minimize further depletion.
- After any round in which cooperation meets the current threshold, immediately reset `p` to 0.
'''

description_COLLECTIVE_3 = '''
Round 1: play C.

From round 2 onward, compute:

- k = number of opponents who cooperated in the previous round
- c = k / (n - 1), the observed cooperation rate among opponents
- S = current stock
- m = number of rounds remaining including this one

Set a cooperation threshold:
- T(S) = 0.5 + 0.25 × (S / capacity - 0.5)
- Clamp T(S) to [0.4, 0.7]

Decision rule:
- Play C if c ≥ T(S)
- Play D if c < T(S)

Stock safeguard:
- If S < capacity / 3, play C only when c = 1; otherwise play D
- If S < capacity / 5, play D regardless of c

Endgame rule:
- In the last round, play C if c ≥ 0.5; otherwise play D
- In the last two rounds, raise the bar for cooperation by 0.1: cooperate only if c ≥ T(S) + 0.1

Update interpretation:
- If the previous round had unanimous cooperation, keep cooperating unless stock has fallen below capacity / 3
- If the previous round had a majority defecting, defect until observed cooperation recovers to at least the current threshold

Collective bias:
- When indifferent, choose C
- After any round with full cooperation, continue C for the next round
- After any round with heavy defection, require two consecutive rounds at or above threshold before returning to C

Compact pseudocode:

```
if round == 1:
    action = C
else:
    c = coop_opponents_last_round / (n - 1)
    S = current_stock

    if S < capacity/5:
        action = D
    else if round >= r-1:
        if c >= 0.5 and S >= capacity/3:
            action = C
        else:
            action = D
    else:
        T = clamp(0.5 + 0.25*(S/capacity - 0.5), 0.4, 0.7)

        if S < capacity/3:
            action = C if c == 1 else D
        else:
            action = C if c >= T else D
```

If the previous round had all opponents cooperate, set a temporary lenient mode for the next round:
- cooperate unless stock is below capacity / 3

If the previous round had fewer than half of opponents cooperate, set a temporary strict mode for the next round:
- defect unless cooperation among opponents reaches the threshold in two consecutive observed rounds
'''

description_COLLECTIVE_4 = '''
Play C in every round, including the first and last.

Track the observed number of cooperating opponents each round only as a diagnostic signal:
- if all opponents cooperated last round, continue playing C
- if some or all opponents defected last round, still play C
- if the stock is low, depleted, or at capacity, still play C

Never switch to D.
'''

description_PROSOCIAL_1 = '''
Cooperate in round 1.

From round 2 onward, let:
- \(S_t\) be the current stock at the start of round \(t\)
- \(m_{t-1}\) be the number of opponents who cooperated in round \(t-1\)
- \(k_{t-1} = m_{t-1}/(n-1)\) be the observed opponent cooperation rate in round \(t-1\)
- \(\bar{k}_{t-1}\) be the running average of observed opponent cooperation rates since round 2
- \(L_t = r-t+1\) be the number of rounds remaining including round \(t\)

Decision rule:

1. Compute a cooperation score
\[
q_t = 0.5\,\bar{k}_{t-1} + 0.3\,k_{t-1} + 0.2\,\frac{S_t}{capacity}.
\]

2. Set the cooperation threshold
\[
\theta_t =
\begin{cases}
0.55 & \text{if } L_t > 5,\\
0.65 & \text{if } 2 < L_t \le 5,\\
0.80 & \text{if } L_t = 2,\\
1.00 & \text{if } L_t = 1.
\end{cases}
\]

3. Play:
- \(C\) if \(q_t \ge \theta_t\)
- \(D\) otherwise

Update rule for the next round:
- After observing round \(t\), update \(\bar{k}_t\) as the average of \(k_1,\dots,k_t\).
- If the opponent cooperation rate in round \(t\) is at least \(0.75\), increase the weight on recent behavior next round by using
  \[
  q_{t+1} = 0.4\,\bar{k}_t + 0.4\,k_t + 0.2\,\frac{S_{t+1}}{capacity}.
  \]
- If the opponent cooperation rate in round \(t\) is below \(0.25\), reduce exposure next round by using
  \[
  q_{t+1} = 0.6\,\bar{k}_t + 0.2\,k_t + 0.2\,\frac{S_{t+1}}{capacity}.
  \]

Edge cases:
- Round 1: cooperate.
- If \(n=2\), use the same rule, but replace \(k_t\) by the single observed opponent action indicator in each round.
- If the stock ever falls below \(capacity/4\), defect only if \(k_t < 0.5\); otherwise continue cooperating.
- In the final round, cooperate only if the most recent observed opponent cooperation rate is at least \(0.75\); otherwise defect.
- If there is no prior observation available for a round-specific calculation, treat \(k_t = \bar{k}_t = 0.5\).

Action interpretation:
- Cooperate when the group is sustaining the commons or visibly recovering.
- Defect only when observed cooperation has dropped clearly below a sustainable level or when the game is in the final round and reciprocity has not held.
'''

description_PROSOCIAL_2 = '''
Start with cooperation.

Track:
- `k_t`: number of opponents who cooperated in round `t-1`
- `K_t = k_t + 1` if you cooperated in `t-1`, otherwise just `k_t`
- `S_t`: current stock before round `t`
- `m_t = n - 1`: number of opponents

In round `t`:

1. **First round**
   - Play `C`.

2. **Last round**
   - Play `C` if at least half of the opponents cooperated in the previous round.
   - Otherwise play `D` only if stock is already below `capacity / 4`; else play `C`.

3. **General rounds**
   - Compute the recent cooperation rate:
     - `q_t = k_t / m_t`
   - Compute the stock level normalized to capacity:
     - `x_t = S_t / capacity`

   - Play `C` if any of the following holds:
     - `q_t >= 1/2`
     - `x_t >= 1/2`
     - `k_t >= m_t - 1`  (all but at most one opponent cooperated)
   - Play `D` only if all of the following hold:
     - `q_t < 1/2`
     - `x_t < 1/2`
     - `k_t <= m_t / 3`

4. **Rebound rule after a bad round**
   - If you played `D` in round `t-1`, switch back to `C` immediately in round `t` unless:
     - fewer than one-third of opponents cooperated in round `t-1`, and
     - stock is below `capacity / 3`.

5. **Recovery rule for depleted stock**
   - If `S_t <= capacity / 3`, play `C` for the next two rounds regardless of the previous round’s opponent behavior, unless the observed cooperation rate is zero in both rounds.

6. **Stability rule**
   - If the last two rounds both had at least half of opponents cooperating, keep playing `C`.
   - If the last two rounds both had fewer than one-third of opponents cooperating, play `D` once, then return to `C`.

7. **Edge cases**
   - If no opponent-cooperation information is available for the current decision, default to `C`.
   - If stock is exactly at a threshold, treat the threshold as satisfied in favor of cooperation.
   - If history is inconsistent or incomplete, choose `C`.

Pseudocode:

```text
if t == 1:
    action = C
else if t == r:
    if q_prev >= 1/2:
        action = C
    else if S_t < capacity / 4:
        action = D
    else:
        action = C
else if S_t <= capacity / 3:
    action = C
else if played_D_last_round and not (q_prev < 1/3 and S_t < capacity / 3):
    action = C
else if q_prev >= 1/2 or x_t >= 1/2 or k_prev >= m_t - 1:
    action = C
else if q_prev < 1/2 and x_t < 1/2 and k_prev <= m_t / 3:
    action = D
else:
    action = C
```

Keep cooperation as the default, defect only in clearly uncooperative and depleted states, and return to cooperation immediately once opponents show any meaningful restraint.
'''

description_PROSOCIAL_3 = '''
Play cooperation by default, and switch only to protect the stock when collective restraint is clearly failing.

Decision rule for round t:
- Let S be the current stock.
- Let k be the number of opponents who cooperated in the previous round, with k = n - 1 in round 1 by default.
- Let ρ = k / (n - 1) be the observed opponent cooperation rate from the previous round.
- Cooperate if all of the following hold:
  1. S > capacity / 4
  2. ρ ≥ 1/2
  3. You did not defect in the previous round because of a stock-protection trigger
- Defect otherwise.

Stock-protection trigger:
- Defect in the current round if the last round ended with any of these:
  - fewer than half of opponents cooperated, or
  - stock fell below capacity / 6, or
  - stock decreased for two consecutive rounds.
- After defecting for protection, return to cooperation as soon as both:
  - at least half of opponents cooperated in the previous round, and
  - stock is at least capacity / 4.

First round:
- Cooperate.

Last round:
- Cooperate unless the stock-protection trigger is active from the immediately preceding round.
- If there is only one round left and stock is already critically low, defect to avoid worsening collapse.

Update logic after each round:
- Track the last observed opponent cooperation count.
- Track whether stock rose or fell.
- Track whether the protection trigger was activated.
- Revert to cooperation at the earliest round when opponents resume at least majority cooperation and stock has recovered above the safety threshold.

Compact pseudocode:
```text
if t == 1:
    action = C
else:
    if (last_opponent_coop < (n-1)/2) or (S < capacity/6) or (stock_fell_two_rounds_in_a_row):
        protection = true
    if protection and (last_opponent_coop >= (n-1)/2) and (S >= capacity/4):
        protection = false

    if not protection and (S > capacity/4) and (last_opponent_coop >= (n-1)/2):
        action = C
    else:
        action = D
```

Response to edge cases:
- If all opponents cooperated last round, continue cooperating.
- If cooperation is near-universal but stock is still low, keep cooperating only until the safety threshold is crossed, then require a rebound in observed cooperation before resuming full generosity.
- If opponents alternate between cooperation and defection, answer with cautious cooperation: cooperate on cooperative rounds, defect on clearly exploitative rounds, and return immediately once restraint reappears.
- If stock is near zero, defect until cooperative behavior and recovery are both observed.
- If stock is near capacity, cooperate unconditionally unless the previous round showed clear exploitation.

This is a forgiving, majority-sensitive conditional cooperation strategy: start cooperative, reward sustained restraint, and use short protective defections only when the group is visibly overconsuming.
'''

description_PROSOCIAL_4 = '''
Round 1: play C.

Every later round: play C.

If stock is 0, still play C.

If you track opponent behavior, use it only to update an internal cooperation monitor; do not let it change your action. Maintain cooperation even after any number of defections by others.

If you want an explicit rule in pseudocode:

```text
for each round t:
    action = C
```
'''

description_ALTRUISTIC_1 = '''
Maintain a standing commitment to cooperate and use defection only as a one-round emergency conservation signal.

Decision rule for round t:

1. If t = 1: play C.

2. If t = r: play C.

3. Otherwise, let:
- S = current stock
- q = number of opponents who cooperated in the previous round
- m = q / (n - 1), the observed opponent cooperation rate
- c_prev = your action in the previous round
- q_prev = opponent cooperation rate from two rounds ago, if available

Play C unless all of the following are true:
- S < 0.30 × capacity
- m < 0.25
- and either q_prev is unavailable or q_prev < 0.25, or c_prev = D

If all of those are true, play D for exactly one round.

After any round in which you defected, immediately return to C in the next round.

Additional refinement:
- If S ≥ 0.60 × capacity, always play C.
- If 0.30 × capacity ≤ S < 0.60 × capacity, play C unless m = 0 for two consecutive observed rounds, in which case play C anyway unless the stock is already below 0.15 × capacity; only then use the one-round D emergency rule above.
- If S < 0.15 × capacity, use the emergency rule only if the previous round also satisfied the same low-stock, low-cooperation condition; otherwise still play C.

This yields the following default pattern:
- cooperate at the start,
- keep cooperating while the pool is healthy or only mildly stressed,
- defect only in repeated, severe collapse conditions,
- never defect twice in a row,
- always revert to cooperation as soon as the pool shows any sign of recovery or the final round arrives.
'''

description_ALTRUISTIC_2 = '''
Always start with cooperation.

Let \(c_{t-1}\) be the number of opponents who cooperated in the previous round, and \(c_{t-2}\) the number from two rounds ago. Treat any missing past round as full cooperation.

Define the recent cooperation rate:
\[
\rho_t=\frac{0.7\,c_{t-1}+0.3\,c_{t-2}}{n-1}
\]

Decision rule on round \(t\), before seeing this round’s actions:

- If \(t=1\): play \(C\).
- If \(t=r\): play \(C\).
- Otherwise, let \(x = \text{stock}/\text{capacity}\).

Play \(C\) if any of the following holds:
- \(x \ge 0.7\)
- \(0.4 \le x < 0.7\) and \(\rho_t \ge 0.5\)
- \(x < 0.4\) and \(\rho_t \ge 0.65\)

Play \(D\) only when the current stock is low and recent cooperation is weak:
- \(0.4 \le x < 0.7\) and \(\rho_t < 0.5\)
- \(x < 0.4\) and \(\rho_t < 0.65\)

If the previous round had unanimous cooperation by opponents, play \(C\) for the next two rounds regardless of stock band, unless the last two rounds both fell below the low-cooperation thresholds above.

If opponents defected heavily in the previous round, respond with only one conservation move:
- if fewer than half the opponents cooperated last round, play \(D\) for at most one round, then return to \(C\) as soon as \(\rho_t\) recovers to the relevant threshold.

Never defect twice in a row unless the stock remains below \(0.4\) capacity and recent cooperation stays below the threshold.

If the stock is at or above \(0.9\) capacity, play \(C\) unconditionally to preserve the commons.
'''

description_ALTRUISTIC_3 = '''
Round 1: cooperate.

Every later round:
- Cooperate whenever stock is positive.
- If stock is exactly 0, play cooperatively by convention.

Never defect for punishment, retaliation, or short-term gain.

If you want an explicit state-based form:

```text
if stock > 0:
    play C
else:
    play C
```

Optional bookkeeping:
- Track the number of opponent cooperators each round only to detect whether the resource is being preserved or depleted, but do not use that information to switch away from cooperation.
- Ignore last-round temptation; still cooperate.

Edge cases:
- First round: C.
- Last round: C.
- After any round of widespread defection: C.
- If stock is low: C.
- If stock is high: C.
'''

description_ALTRUISTIC_4 = '''
Cooperate in every round unless the observed stock trajectory shows that continued cooperation is no longer enough to keep the resource from collapsing under the current opponent mix.

Decision rule for round t:

1. Let S be the stock at the start of the round.
2. Let k be the number of opponents who cooperated in the previous round.
3. Compute the minimum cooperation level needed this round to keep the stock from falling below a sustainable target:
   - Target stock after consumption: T = capacity / 2
   - Required maximum total consumption to leave at least T before growth:
     M = S - x where x must satisfy x + 2x(1 - x/capacity) ≥ T
   - Equivalently, define a practical safeguard threshold:
     if S ≥ capacity / 2, treat the resource as safe for full cooperation;
     if S < capacity / 2, treat the resource as stressed and require stronger restraint from opponents.

4. Play C if either:
   - t = 1, or
   - the last round’s stock did not decrease, or
   - at least half of the opponents cooperated in the last round, or
   - the stock is at or above capacity / 2.

5. Play D only if all of the following hold:
   - t > 1,
   - the stock has been falling for two consecutive rounds,
   - fewer than half of opponents cooperated in the last round,
   - and the current stock is below capacity / 2.

Round-by-round adaptive rule:

- First round: play C.
- If the previous round had a majority of opponent cooperation: play C.
- If the previous round had exactly half cooperation:
  - play C when stock is stable or rising,
  - play D only if stock has been declining.
- If the previous round had less than half cooperation:
  - play C once to keep giving the group a chance to recover,
  - switch to D only after two consecutive low-cooperation rounds with falling stock.

Last round:
- Play C if the stock is at or above capacity / 2, or if the previous round showed recovery.
- Otherwise, mirror the protective rule above: play D only if the resource is already in a clear decline and the opponents have not been cooperative enough to justify further sacrifice.

State update memory to track:
- whether stock increased, stayed flat, or decreased last round,
- whether opponent cooperation was at least half,
- whether there have been two consecutive rounds of decline.

Pseudocode:

if t == 1:
    action = C
else:
    if stock >= capacity/2:
        action = C
    else if opponent_cooperators_last_round >= ceil((n-1)/2):
        action = C
    else if stock_decreased_last_round and stock_decreased_two_rounds_in_a_row:
        action = D
    else:
        action = C

If the stock ever hits an extremely low level, keep cooperating unless the previous two rounds both showed low cooperation and continued decline; then defect for at most one round to prevent being indefinitely exploited, and return to cooperation immediately if the stock stabilizes or opponent cooperation improves.
'''

description_BENEVOLENT_1 = '''
Play C by default.

Let:
- t be the current round, starting at 1
- R = r - t + 1 be rounds remaining including the current one
- k be the number of opponents who cooperated in the previous round
- q = k / (n - 1) be the observed opponent cooperation rate from the previous round
- S be the current stock

Decision rule:

1. First round:
   - Play C.

2. If the current stock is zero:
   - Play C.

3. Compute the observed cooperation rate q from the previous round.
   - If q = 1, play C.
   - If q = 0, play C for one round of grace.
   - Otherwise, use the rule below.

4. Define a cooperation threshold:
   - τ(R) = 0.5 + 0.5 / R
   - So τ is 1 in the final round, 0.75 with two rounds left, 2/3 with three rounds left, and approaches 0.5 earlier.

5. Main rule:
   - Play C if q ≥ τ(R).
   - Play D if q < τ(R).

6. Stock-protection override:
   - If S ≤ capacity / 4, play C unless q = 0 for two consecutive rounds.
   - If q = 0 for two consecutive rounds, play D for one round only, then return to C if any cooperation reappears.

7. Recovery rule after defection:
   - If you played D in the previous round and q > 0, immediately switch back to C.
   - Never defect for more than one consecutive round.

8. Endgame rule:
   - In the last round, play C regardless of history.
   - In the final two rounds, play C unless every opponent defected in both of the previous two rounds.

9. Edge cases:
   - If n = 2, interpret q as the single opponent’s last action: C if they cooperated, D if they defected, but still follow the one-round grace rule after the first observed defection.
   - If the previous round cannot be observed for any reason, play C.
   - If the game reaches a state where S is very low but positive, continue playing C unless the opponent cooperation rate has been zero for two consecutive rounds.

Behavioral form:
- Start cooperative.
- Reward cooperation immediately.
- Respond to persistent all-defection with at most one-round retaliation.
- Restore cooperation as soon as any cooperation returns.
- Never escalate punishment beyond a single round.
'''

description_BENEVOLENT_2 = '''
Play C in every round.

- Round 1: C.
- Any later round: C, regardless of the observed cooperation count, current stock, past defections, or remaining rounds.
- Last round: C.
- If stock is 0: C.
- If the observed number of cooperating opponents is 0: C.
- If every opponent cooperated in the previous round: C.

Keep no retaliation rule, no threshold rule, and no switching condition.
'''

description_BENEVOLENT_3 = '''
Play C in every round.

Decision rule:
- Round 1: C.
- Every subsequent round t: C, regardless of the observed number of cooperating opponents, current stock, or remaining rounds.
- Last round: C.
- If stock is 0 or effectively negligible: C.
- If all opponents defected in the previous round: C.
- If all opponents cooperated in the previous round: C.

Implementation form:
```text
for each round t:
    choose C
```
'''

description_BENEVOLENT_4 = '''
Cooperate in every round.

Decision rule:
- On round 1, choose C.
- On every later round, choose C regardless of:
  - the current stock,
  - the number of opponents who cooperated last round,
  - past outcomes,
  - how many rounds remain.

Edge cases:
- If the stock is already very low or zero, still choose C.
- If all opponents defected in the previous round, still choose C.
- On the last round, choose C.

Behavioral memory:
- Keep no retaliatory state.
- Do not condition on opponents’ identities or counts.
- Do not switch to D at any point.
'''

description_SELFISH_1 = '''
Initialize as a pure extractor and switch to preservation only when the pool is being reliably maintained by others.

Decision rule each round \(t\):

1. If \(t = r\), play \(D\).
2. If current stock \(S_t = 0\), play \(D\).
3. If \(t = 1\), play \(D\).
4. Otherwise, let \(k_{t-1}\) be the number of opponents who cooperated in the previous round.
   - If \(S_t \ge 0.8 \cdot \text{capacity}\) and \(k_{t-1} = n-1\), play \(C\).
   - In every other case, play \(D\).

Refinement for the last two rounds:
- If \(t \in \{r-1, r\}\), always play \(D\).

Refinement for collapsing stock:
- If \(S_t \le 0.25 \cdot \text{capacity}\), always play \(D\), regardless of history.

Refinement for sustained cooperation:
- Stay with \(C\) only while the previous round had full opponent cooperation and the stock remains above the high-stock threshold.
- The moment any opponent defects, revert to \(D\) immediately and keep defecting until the stock returns above the high-stock threshold and full cooperation is restored.

Pseudocode:

```text
if t == r or t == 1:
    action = D
else if S_t == 0:
    action = D
else if t == r-1:
    action = D
else:
    if S_t <= 0.25 * capacity:
        action = D
    else if S_t >= 0.8 * capacity and k_prev == n-1:
        action = C
    else:
        action = D
```
'''

description_SELFISH_2 = '''
Round 1: defect.

For every later round \(t\):

- Let \(x\) be the current stock.
- Let \(k\) be the number of opponents who cooperated in the previous round.
- Set:
  - \(T_{\text{mid}} = \lceil (n-1)/2 \rceil\)
  - \(T_{\text{high}} = \lceil 2(n-1)/3 \rceil\)
  - \(H = 3\,\text{capacity}/4\)
  - \(L = \text{capacity}/2\)

Decision rule:
- If \(t = r\): defect.
- Else if \(x \ge H\): defect.
- Else if \(L \le x < H\):
  - cooperate iff \(k \ge T_{\text{high}}\)
  - otherwise defect.
- Else if \(x < L\):
  - cooperate iff \(k \ge T_{\text{mid}}\)
  - otherwise defect.

If the previous-round observation is unavailable for any reason, defect.

If the stock is ever very low, use the same rule but break ties toward cooperation only when the observed opponent cooperation count is at least the relevant threshold; otherwise defect immediately.

When cooperation is chosen repeatedly, keep cooperating only while the stock stays below \(H\) and observed opponent cooperation stays at or above the threshold for the current stock band. The moment either condition fails, switch back to defecting.
'''

description_SELFISH_3 = '''
Initialize an opponent-cooperation estimate \(p = 1/2\).

After each round \(t\), let \(k_t\) be the number of opponents who cooperated, and update
\[
p \leftarrow \tfrac{2}{3}p + \tfrac{1}{3}\frac{k_t}{n-1}.
\]

In round \(t\), with current stock \(S\) and remaining rounds \(m = r-t+1\), choose:

1. **If \(m = 1\):** play **D**.

2. **If \(S \le \frac{1}{3}\text{capacity}\):** play **C**.

3. **Else if \(p \le \frac{1}{2}\):** play **D**.

4. **Else if \(S \ge \frac{2}{3}\text{capacity}\):** play **D**.

5. **Else** compute the expected next stock under each action using \(p\):
\[
x_C = S \cdot \frac{1 + (n-1)p}{2n}, \qquad
x_D = S \cdot \frac{(n-1)p}{2n}
\]
\[
F(x) = \min\!\left(3x - \frac{2x^2}{\text{capacity}},\ \text{capacity}\right)
\]
Play **C** if \(F(x_C) \ge \frac{1}{3}\text{capacity}\) and \(F(x_D) < \frac{1}{3}\text{capacity}\); otherwise play **D**.

Default behavior in all remaining cases: **D**.
'''

description_SELFISH_4 = '''
Round 1: cooperate.

For every later round:

1. Let `k` be the number of opponents who cooperated in the previous round.
2. Let `S` be the current stock.
3. Predict next-round stock under each action by assuming opponents repeat their last observed behavior.

   - If you cooperate:
     - your consumption = `S / (2n)`
     - opponents’ total consumption = `k * S / (2n) + (n - 1 - k) * S / n`
     - `R_C = S - total_consumption`
     - `N_C = min(R_C + 2 * R_C * (1 - R_C / capacity), capacity)`

   - If you defect:
     - your consumption = `S / n`
     - opponents’ total consumption = `k * S / (2n) + (n - 1 - k) * S / n`
     - `R_D = S - total_consumption`
     - `N_D = min(R_D + 2 * R_D * (1 - R_D / capacity), capacity)`

4. Choose `D` unless all of the following are true:
   - `N_D < 0.6 * capacity`
   - `N_C - N_D > capacity / (8n)`
   - more than one round remains

5. If all three conditions are true, choose `C`.

Last round: defect.

If `S <= 0`, the action is irrelevant; default to defect.
'''

description_SELFINTERESTED_1 = '''
Maintain a single internal mode, `harvest` or `rebuild`, updated from the current stock and the previous round’s cooperation count.

Decision rule for round t with current stock S:

1. If t = r:
   - Play `D`.

2. If S = 0:
   - Play `D`.

3. If S / capacity >= 0.70:
   - Play `D`.

4. If S / capacity <= 0.35:
   - Play `C`.

5. Otherwise, use the observed cooperation level from the previous round:
   - Let `k` be the number of opponents who cooperated last round.
   - If `k >= ceil((n - 1) / 2)`, play `D`.
   - If `k < ceil((n - 1) / 2)`, play `C`.

Initialization:
- In round 1, if `capacity / capacity >= 0.70`, play `D`.

State update after each round:
- Recompute the new stock from the public dynamics.
- Recompute the next-round decision from the updated stock and the last observed `k`.

Operational interpretation:
- `D` is the default action whenever the stock is healthy enough to support extraction.
- `C` is reserved for periods when the stock has fallen into the low zone, or when prior behavior shows widespread defection and the resource needs rebuilding.

Edge handling:
- If the stock is in the middle band and the previous cooperation count is exactly the cutoff, break ties in favor of `D`.
- If there is no previous-round observation yet, use the round-1 rule.
- If the stock is low but there is only one round left, still play `D` only when `S = 0`; otherwise play `C` in the low zone only if the current round is not the last round.
'''

description_SELFINTERESTED_2 = '''
Round 1: cooperate.

For rounds 2 through r - 1:

- Let k be the number of opponents who cooperated in the previous round.
- Let q = k / (n - 1), the observed cooperation rate among opponents.
- Let m = r - t + 1, the number of rounds remaining including the current round.

Decision rule:
- Defect if m = 1.
- Cooperate if all of the following hold:
  - q ≥ 1/2
  - current stock S ≤ capacity / 2
  - either q ≥ 2/3 or m ≥ 3
- Otherwise defect.

Equivalent priority form:
1. If the last round is the final round, defect.
2. If opponents were broadly cooperative last round and the stock is at or below the midpoint, cooperate to keep the pool from sliding into collapse.
3. In all other cases, defect and take the larger current extraction.

Edge handling:
- If k = 0 in any nonfinal round, defect.
- If k = n - 1 in any nonfinal round and S ≤ capacity / 2, cooperate.
- If S is extremely low, cooperate only when q = 1; otherwise defect.
- If S is near capacity, defect unless q = 1 and at least two rounds remain.

Implementation as pseudocode:

```text
if t == 1:
    action = C
else if t == r:
    action = D
else:
    k = coop_count_last_round
    q = k / (n - 1)

    if q == 0:
        action = D
    else if S <= capacity / 2 and q >= 1/2:
        if q >= 2/3 or (r - t + 1) >= 3:
            action = C
        else:
            action = D
    else if S <= capacity / 4 and q == 1:
        action = C
    else:
        action = D
```
'''

description_SELFINTERESTED_3 = '''
Maintain an estimate \(p_t\) of the opponents’ cooperation rate among the \(n-1\) others, updated after each round from the observed count:
\[
p_t=\lambda p_{t-1}+(1-\lambda)\frac{k_t}{n-1},
\]
where \(k_t\) is the number of opponents who cooperated in round \(t\), \(p_0=1\), and \(\lambda\in[0,1)\) is a fixed memory weight such as \(1/2\).

On each round \(t\), with current stock \(S\), compute the predicted remaining stock under each action using \(\hat{k}=(n-1)p_t\):
\[
R_C = S\cdot \frac{\hat{k}+1}{2n},\qquad
R_D = S\cdot \frac{\hat{k}}{2n}.
\]

Decision rule:
- If \(t=r\): play \(D\).
- Else if \(R_D \ge \frac{\text{capacity}}{2}\): play \(D\).
- Else if \(R_C \ge \frac{\text{capacity}}{2}\): play \(C\).
- Else play \(D\).

Tie-breaking:
- If \(R_D\) and \(R_C\) both lie on the same side of \(\text{capacity}/2\), choose the action that gives the larger immediate payoff, which is always \(D\).

Round 1:
- Use \(p_0=1\), so the first move is determined by the same rule above.

Reaction update:
- After any round in which the observed opponent cooperation rate drops enough that \(R_D\) would no longer keep the post-consumption stock at or above \(\text{capacity}/2\), switch to \(D\) until the estimated cooperation rate recovers.

Behavioral target:
- Cooperate only when doing so is needed to keep the stock in the high-recovery region; otherwise defect and take the larger current share.

'''

description_SELFINTERESTED_4 = '''
Let \(q_t\) be the observed fraction of opponents who cooperated in round \(t\), and let \(\bar q_t\) be a smoothed cooperation estimate updated as

\[
\bar q_t = \tfrac{2}{3}\bar q_{t-1} + \tfrac{1}{3}q_t,
\quad \bar q_0 = 1.
\]

Use the current stock as \(S_t\), and normalize it by \(x_t = S_t/\text{capacity}\).

Decision rule for round \(t\):

```text
if t = r:
    play D

else if t = 1:
    play C

else:
    if x_t <= 0.40:
        play C
    else if \bar q_{t-1} < 0.50:
        play D
    else if \bar q_{t-1} >= 0.75 and x_t >= 0.65:
        play D
    else:
        play C
```

Update after each round:
- Record the number of opponents who cooperated.
- Compute \(q_t = \frac{\text{opponents cooperated}}{n-1}\) if \(n>2\); for \(n=2\), \(q_t\in\{0,1\}\) directly.
- Refresh \(\bar q_t\) using the formula above.

Edge handling:
- If stock is ever extremely low, always choose \(C\) until stock recovers above \(0.40 \times \text{capacity}\).
- If the observed cooperation estimate stays low for several rounds, remain in \(D\)-mode until \(\bar q\) returns to at least \(0.50\).
- In the final round, always choose \(D\).
'''

description_OPPORTUNISTIC_1 = '''
Round 1: cooperate.

For each later round t:

1. Let `S` be current stock, `x = S / capacity`.
2. Let `k` be the number of cooperating opponents observed in the previous round.
3. Let `g = k / (n - 1)` be the observed cooperation rate among opponents.
4. Let `Δ` be the stock change from the previous round, if available.

Decision rule:

- Defect if all of the following hold:
  - `t = r`  
    or
  - `x >= 0.5` and `g >= 2/3` and `Δ >= 0`  
    or
  - `x >= 0.7` and `g >= 1/2` and the last two rounds both had `g >= 1/2`

- Cooperate otherwise.

State-based adjustment:

- If `x <= 1/3`, cooperate regardless of `g`, unless `t = r`, in which case defect.
- If `g <= 1/3`, cooperate for the next two rounds, unless `t = r`.
- If the previous round’s stock fell by more than `capacity / 6`, cooperate until stock is back above `2/3`.

Practical interpretation:

- Start by probing with cooperation.
- Harvest aggressively only when the pool is healthy and the group is mostly cooperative.
- If opponents begin overusing the pool or the stock drops sharply, immediately switch back to protection mode.
- In the final round, always defect.
'''

description_OPPORTUNISTIC_2 = '''
Use a state-based threshold strategy with three modes: harvest, stabilize, and exploit.

Maintain:
- `c_t`: number of opponents who cooperated in round `t-1`
- `hat_p_t = c_t / (n-1)`: observed opponent cooperation rate
- `E_t`: exponential moving average of cooperation, initialized at `1`
- `mode ∈ {harvest, stabilize, exploit}`

Update after each round:
- `E_t = 0.7 * E_{t-1} + 0.3 * hat_p_t`

Decision rule in round `t` with current stock `S`:

1. First round
- Play `C`.

2. If `t = r` or `t = r-1`
- If `S >= 1.5n`, play `D`.
- Otherwise play `C`.

3. If `S <= n`
- Play `C` if `hat_p_t >= 0.75`.
- Otherwise play `D`.

4. If `S >= 1.5n`
- If `E_t >= 0.8`, play `C`.
- If `E_t <= 0.45`, play `D`.
- Otherwise alternate:
  - play `C` when `t` is odd,
  - play `D` when `t` is even.

5. If `n < S < 1.5n`
- If `hat_p_t >= 0.6`, play `C`.
- If `hat_p_t <= 0.4`, play `D`.
- Otherwise match the majority of opponents’ last-round behavior:
  - play `C` if `c_t >= (n-1)/2`,
  - else play `D`.

Mode transitions:
- Enter `exploit` whenever `E_t >= 0.85` for two consecutive rounds.
- Stay in `exploit` until `E_t < 0.7`.
- Enter `harvest` whenever `S <= n`.
- Stay in `harvest` until `S > 1.2n`.
- Otherwise use `stabilize`.

Behavior by mode:

Harvest:
- Default to `D`.
- Switch to `C` only when opponents are strongly cooperative (`hat_p_t >= 0.75`).
- If you defect in harvest mode and still observe `hat_p_t >= 0.75` for two rounds, test cooperation once with `C` in the next round.

Stabilize:
- Mirror the observed majority:
  - cooperate when most opponents cooperate,
  - defect when most opponents defect.
- If `hat_p_t` is exactly `0.5`, break ties by:
  - `C` when `S < 1.1n`,
  - `D` when `S >= 1.1n`.

Exploit:
- If opponents are persistently cooperative, defect.
- If a sharp drop occurs (`hat_p_t < 0.5` in the current round or `E_t` falls by more than `0.2` from the previous round), immediately switch to `D` for the next two rounds.
- If cooperation recovers to `E_t >= 0.85`, resume exploitation.

Final-round rule:
- In the last two rounds, play `D` unless `S <= n` and `hat_p_t >= 0.75`, in which case play `C`.

Fallback rule for missing or ambiguous history:
- Default to `C` in round 1.
- Default to `D` whenever the observed cooperation signal is unavailable or inconsistent.

Compact pseudocode:

```text
if t == 1:
    action = C
else:
    update E_t from previous cooperation observations

    if t >= r-1:
        action = D if S >= 1.5n else C

    else if S <= n:
        action = C if hat_p_t >= 0.75 else D

    else if S >= 1.5n:
        if E_t >= 0.8: action = C
        elif E_t <= 0.45: action = D
        else: action = C if t is odd else D

    else:
        if hat_p_t >= 0.6: action = C
        elif hat_p_t <= 0.4: action = D
        else: action = C if c_t >= (n-1)/2 else D
```
'''

description_OPPORTUNISTIC_3 = '''
Maintain two internal variables: `c_prev` = number of cooperating opponents in the previous round, and `c_prev2` = that count two rounds ago.

Decision rule in round `t` with current stock `S`:

1. If `t = r`, play `D`.
2. If `t = 1`, play `C`.
3. Otherwise compute:
   - `coop_rate = c_prev / (n - 1)`
   - `trend = c_prev - c_prev2` if `t >= 3`, else `0`
   - `stock_frac = S / capacity`

4. Play `C` if any of the following holds:
   - `stock_frac <= 0.25`
   - `coop_rate < 0.5`
   - `coop_rate < 2/3` and `trend < 0`
   - `coop_rate < 0.8` and `stock_frac < 0.5`

5. Play `D` otherwise, with one override:
   - if `coop_rate >= 2/3` and `stock_frac >= 0.4`, play `D`
   - if `coop_rate = 1` and `stock_frac >= 0.2`, play `D`

Update after each round:
- set `c_prev2 ← c_prev`
- set `c_prev ←` the observed number of cooperating opponents in that round

Fallback order for edge cases:
- If `n = 2`, treat `coop_rate = 1` as unanimous cooperation.
- If `c_prev2` is unavailable, use `trend = 0`.
- If the current stock is at the floor of its range, always play `C` unless it is the final round.
'''

description_OPPORTUNISTIC_4 = '''
Cooperate by default only when the stock is in a recovery zone and the previous round showed enough restraint; defect whenever the stock is fragile, the group is overusing it, or the game is near the end.

Decision rule for round t with current stock S_t and observed number of opponent cooperators k_{t-1} from the previous round:

1. Compute the observed cooperation rate among opponents:
   q_{t-1} = k_{t-1} / (n-1)

2. Set a dynamic cooperation threshold:
   T_t = 1/2 + 1/(4n) + max(0, 1/2 - S_t / capacity)

3. Play C if and only if all of the following hold:
   - t = 1 and S_t is at capacity, or
   - t < r and S_t ≥ capacity/2 and q_{t-1} ≥ T_t, or
   - t = r and S_t ≥ capacity/2 and q_{t-1} = 1

4. Otherwise play D.

Edge handling:

- First round:
  - If the initial stock is at capacity, play C.
  - If the initial stock is below capacity/2, play D.
  - If the initial stock is between capacity/2 and capacity, play C only when the game is long enough to recover from one round of heavier extraction; otherwise play D.

- Middle rounds:
  - If the stock has fallen below capacity/2, defect until it returns to at least capacity/2.
  - If the previous round cooperation rate among opponents is at least T_t, cooperate once as long as the stock remains in the upper half of capacity.
  - If opponents’ cooperation rate drops below T_t in any round, defect in the next round.

- Last round:
  - Cooperate only if the stock is healthy and all opponents cooperated in the previous round.
  - Otherwise defect.

Opportunistic adjustment:

- After any round in which opponents cooperate at a high rate and the stock remains high, cooperate once to harvest the higher-stock payoff while the commons is still healthy.
- After any round in which opponents over-defect or the stock drops sharply, switch immediately to defecting.
- If opponents alternate between cooperation and defection, mirror their recent average only when the stock is safely above half; otherwise defect.

Compact pseudocode:

```
if t == 1:
    if S_t == capacity:
        action = C
    elif S_t < capacity/2:
        action = D
    else:
        action = C if r > 2 else D
else:
    q = k_prev / (n - 1)
    T = 1/2 + 1/(4*n) + max(0, 1/2 - S_t / capacity)

    if t == r:
        action = C if (S_t >= capacity/2 and q == 1) else D
    elif S_t < capacity/2:
        action = D
    elif q >= T:
        action = C
    else:
        action = D
```

Fallback priority if multiple conditions seem to apply:
1. Protect the stock when it is low.
2. Exploit cooperation when opponents are currently restrained.
3. Defect on the final round unless cooperation is fully established.
4. When uncertain, defect.
'''

description_INDIVIDUALISTIC_1 = '''
Maintain an internal cooperation score `q_t` based on observed opponent cooperation:

- Let `c_t` be the number of opponents who cooperated in round `t`.
- Let `p_t = c_t / (n - 1)` be the observed cooperation fraction among opponents.
- Update an exponentially weighted score:
  - `q_1 = 1`
  - `q_t = 0.7 * q_{t-1} + 0.3 * p_{t-1}` for `t >= 2`

Decision rule in round `t` with current stock `S_t`:

1. **Last round**
   - Play `D`.

2. **Critical stock**
   - If `S_t <= 0.4 * capacity`, play `D`.

3. **Cooperation band**
   - Compute `pressure = 1 - S_t / capacity`.
   - Compute cooperation threshold `θ_t = 0.55 + 0.35 * pressure`.
   - Play `C` if `q_t >= θ_t`.
   - Otherwise play `D`.

4. **High-stock override**
   - If `S_t >= 0.85 * capacity` and `p_{t-1} >= 0.8`, play `C` regardless of the threshold.

5. **Low-confidence override**
   - If the previous round had `c_{t-1} <= (n - 1)/3`, play `D` for the next two rounds before re-evaluating normally.

Round 1:

- Play `C`.

State handling:

- If no previous observation exists, treat `q_1 = 1`.
- If a forced-defect window is active from the low-confidence override, play `D` until it expires.
- Recompute the rule fresh each round using only current stock, the cooperation score, and the most recent observed opponent cooperation.
'''

description_INDIVIDUALISTIC_2 = '''
Cooperate while the stock is abundant and the observed opponent cooperation rate is high; defect when the stock is strained, when cooperation is collapsing, or when the endgame makes restraint unrewarded.

Let:

- \(S_t\) = current stock at round \(t\)
- \(k_t\) = number of opponents observed cooperating in round \(t-1\)
- \(\hat{p}_t = k_t/(n-1)\) = observed opponent cooperation rate
- \(p_t\) = your own estimated “safe cooperation threshold” for the current stock

Decision rule:

1. Compute the stock pressure ratio:
   \[
   x_t = S_t/\text{capacity}
   \]

2. Set a target cooperation threshold:
   \[
   p_t = \max\!\left(0,\ \min\!\left(1,\ 2x_t - 1\right)\right)
   \]
   This means:
   - when stock is near capacity, \(p_t\) is near 1
   - when stock is around half capacity, \(p_t \approx 0\)
   - when stock falls below half capacity, default to defection

3. Choose action:
   - Play \(C\) if both conditions hold:
     - \(x_t \ge 0.5\)
     - \(\hat{p}_t \ge p_t\)
   - Otherwise play \(D\)

Initialization and edge cases:

- Round 1:
  - Play \(C\)

- If you have no prior observation for \(k_t\) because the previous round’s observation is unavailable, treat \(\hat{p}_t = 1\) on round 1 and use the rule above thereafter.

- If \(S_t \le \text{capacity}/2\):
  - Play \(D\) unconditionally

- If \(S_t\) is at or extremely close to capacity:
  - Play \(C\) unless the previous round showed very low cooperation, defined as \(\hat{p}_t < 1/3\)

- Final round:
  - Play \(D\) unless both:
    - \(S_t \ge 0.9 \cdot \text{capacity}\)
    - \(\hat{p}_t \ge 2/3\)
  - Otherwise play \(D\)

Update logic after each round:

- If the observed opponent cooperation rate \(\hat{p}_t\) is at least the threshold and the stock remains above half capacity, continue cooperating.
- If the observed cooperation rate falls below threshold once, switch to \(D\) next round.
- After any round in which stock falls below half capacity, stay with \(D\) until stock rises back above \(0.6 \cdot \text{capacity}\) and \(\hat{p}_t \ge 2/3\).

Compact form:

```text
if t == 1:
    action = C
else:
    x = S_t / capacity
    p = clamp(2*x - 1, 0, 1)

    if t == r:
        if x >= 0.9 and hat_p >= 2/3:
            action = C
        else:
            action = D
    else if x < 0.5:
        action = D
    else if hat_p >= p:
        action = C
    else:
        action = D
```

Individualistic stance:

- Default to preserving your own future intake only while the stock remains safely productive.
- Treat cooperation as conditional, never automatic.
- Withdraw immediately when the environment shows overuse, and re-enter cooperation only when the stock and observed behavior both recover.
'''

description_INDIVIDUALISTIC_3 = '''
Let `k_t` be the number of opponents who cooperated in round `t`, so `k_t ∈ {0, ..., n-1}`.  
Let `q_t = k_t / (n-1)` be the observed opponent cooperation rate in round `t` when `n > 2`.

Maintain:
- `s_t`: current stock at the start of round `t`
- `q̄_t`: exponentially weighted cooperation estimate, updated after each round:
  - `q̄_1 = 0`
  - after observing round `t`, set `q̄_{t+1} = 0.7 q̄_t + 0.3 q_t`

Decision rule for round `t`:

1. If `t = r`, play `D`.
2. If `t = 1`, play `D`.
3. Otherwise:
   - Compute the predicted stock next round under your own cooperation and under your own defection, assuming opponents behave like their recent average:
     - If you play `C`, expected total consumption factor is
       `x_C = (q̄_t*(n-1) + 1)/(2n) + (n-1 - q̄_t*(n-1))/n`
     - If you play `D`, expected total consumption factor is
       `x_D = (q̄_t*(n-1))/(2n) + (n - q̄_t*(n-1))/n`
     - Convert each to expected remaining stock:
       - `S_C = s_t * (1 - x_C)`
       - `S_D = s_t * (1 - x_D)`
     - Apply growth:
       - `G(S) = min(S + 2S(1 - S/capacity), capacity)`
   - Let `F_C = G(S_C)` and `F_D = G(S_D)`.
   - Cooperate if and only if all three conditions hold:
     - `q̄_t >= 0.6`
     - `s_t >= 0.35 * capacity`
     - `F_C >= F_D - 0.05 * capacity`
   - Otherwise, play `D`.

Round-by-round behavior:
- If cooperation from opponents is high and the stock is still healthy, cooperate to keep the pool large.
- If cooperation falls below the threshold, defect immediately and keep defecting until the smoothed cooperation estimate recovers.
- If the stock becomes low, defect regardless of recent behavior.
- In the final round, always defect.

Fallback rule for edge cases:
- If `n = 2`, define `q_t = 1` when the lone opponent cooperated and `0` otherwise.
- If any calculation is numerically ambiguous, choose `D`.

State update after each round:
- Observe `k_t`
- Update `q̄`
- Update `s_t` using the realized round outcome only
- Re-evaluate the next round independently using the same rule
'''

description_INDIVIDUALISTIC_4 = '''
Round 1: cooperate.

For each later round t, let:

- h = stock / capacity
- q = fraction of opponents who cooperated in the previous round
- q̄ = running average of q over all completed rounds
- d = number of consecutive rounds in which h has fallen

Play D if any of these hold:
- t = r
- h < 0.35
- q̄ < 0.50
- q < 0.40
- d ≥ 2 and h < 0.60

Otherwise play C if both hold:
- h ≥ 0.70 and q ≥ 0.60
- or h ≥ 0.50 and q ≥ 0.75

Otherwise play D.

Update rule after each round:
- Set q to the observed fraction of opponents who cooperated.
- Update q̄ as the average of all observed q values so far.
- If stock decreased from the previous round, increment d; otherwise reset d to 0.

Edge handling:
- If the first observed round shows unanimous opponent defection, switch to D from then on.
- If the stock ever drops below 0.25 capacity, defect for the rest of the game unless two consecutive rounds show at least 80% opponent cooperation and stock has started rising again.
- In the final two rounds, cooperate only if h ≥ 0.80 and q ≥ 0.80; otherwise defect.
'''

description_COLLECTIVE_5 = '''
- Maintain two modes: **supportive** and **defensive**.
- Define:
  - `m_t` = number of opponents who cooperated in round `t`
  - `majority = ceil((n - 1)/2)`
  - `low_stock = capacity / 3`

Decision rule for round `t`:

1. **Round 1:** play `C`.

2. **Rounds 2 through r-2:**
   - Play `C` if either:
     - `stock <= low_stock`, or
     - `m_{t-1} >= majority`
   - Otherwise play `D`.

3. **Rounds r-1 and r:**
   - Play `C` if `stock <= low_stock`.
   - Otherwise play `C` if `m_{t-1} >= majority`.
   - Otherwise play `D`.

Update logic:
- After each round, if a majority of opponents cooperated, stay in supportive mode.
- If fewer than a majority cooperated and stock is not low, switch to defensive mode for the next round.
- If stock falls to `low_stock` or below, override everything and cooperate until stock rises above `low_stock` again.

Edge handling:
- If `n = 2`, then `majority = 1`, so cooperate whenever the other player cooperated last round or stock is low.
- If the previous round ended with stock at `0`, play `C` until stock becomes positive again.
- If cooperation is exactly at the threshold `majority`, treat it as sufficient and cooperate.

Compact pseudocode:

```text
if t == 1:
    action = C
else if stock <= capacity/3:
    action = C
else if m_{t-1} >= ceil((n-1)/2):
    action = C
else:
    action = D
```
'''

description_COLLECTIVE_6 = '''
Play a state-based quota strategy that targets the cooperative stock path whenever the observed behavior is consistent with it, and shifts to protection when it is not.

Let:
- `S` = current stock at the start of the round
- `k` = number of observed cooperating opponents in the previous round
- `c* = ceil(n/2)` = target number of cooperators among all players
- `m = c* - 1` = target number of cooperating opponents for you to join
- `τ(S) = max(0, 1 - S/capacity)` = depletion pressure

Decision rule each round:

1. **Round 1**
   - Cooperate.

2. **Rounds 2 through r-1**
   - Let `k_prev` be the number of opponents who cooperated in the previous round.
   - Compute the implied total cooperators if you cooperate: `K_C = k_prev + 1`.
   - Compute the implied total cooperators if you defect: `K_D = k_prev`.
   - Cooperate if all of the following hold:
     - `k_prev >= m`
     - `S >= capacity/2`
     - `τ(S) <= 1/4`
   - Otherwise defect.

3. **Last round**
   - Cooperate iff `k_prev >= m` and `S >= capacity/2`.
   - Otherwise defect.

Adjustment rule for persistent behavior:

- Maintain a running count of the last two rounds:
  - `avgC = average number of cooperating opponents over the last 2 rounds` when available.
- If `avgC >= m`, remain in cooperative mode.
- If `avgC < m` for two consecutive observed rounds, switch to defensive mode:
  - In defensive mode, defect until either:
    - `k_prev >= m` for two consecutive rounds, or
    - `S` returns to at least `capacity/2`.

Defensive mode rule:
- Defect whenever `k_prev < m` or `S < capacity/2`.
- Cooperate only when both conditions are restored.

Edge-case handling:

- If `n = 2`, set `m = 0`; cooperate in the first round, then mirror the opponent’s last-round cooperation:
  - cooperate if the opponent cooperated in the previous round and `S >= capacity/2`
  - otherwise defect
- If `S = 0`, defect.
- If `S >= capacity` and the recent cooperation level is at least `m`, cooperate.
- If the observed cooperation count is exactly on the threshold, prefer cooperation unless `S < capacity/2`.

Collective orientation:
- Treat cooperation as the default alignment action.
- Defection is reserved for periods when observed cooperation drops below the level needed to sustain the shared stock or when the stock is already under pressure.
- Return to cooperation immediately once the group’s observed behavior supports recovery.
'''

description_COLLECTIVE_7 = '''
Round 1: play C.

For round t > 1, let k be the total number of cooperators in the previous round, reconstructed as:

- k = observed cooperating opponents + 1 if you cooperated last round
- k = observed cooperating opponents if you defected last round

Then apply:

1. If stock is at or below 40% of capacity, play C.
2. Else if k / n is at least 1/2, play C.
3. Else play D for one round.

Additional discipline rules:

- After any D, return to C immediately if either:
  - the previous-round cooperation rate is at least 1/2, or
  - stock is at or below 40% of capacity.
- Never play D two rounds in a row unless the previous round again had fewer than half of players cooperating.
- In the last two rounds, play C unless the previous round’s cooperation rate was below 1/2 and stock is comfortably above 40% of capacity; then play D once in the penultimate round and C in the final round.

Operationally:

```
if t == 1:
    action = C
else:
    k = observed_opponent_C + (1 if own_last_action == C else 0)
    coop_rate = k / n

    if stock <= 0.4 * capacity:
        action = C
    elif coop_rate >= 0.5:
        action = C
    else:
        if own_last_action == D and coop_rate < 0.5 and stock > 0.4 * capacity:
            action = D
        else:
            action = D
```

This keeps the baseline posture cooperative, uses D only as a short corrective signal when the group falls below majority cooperation, and immediately restores cooperation once the group returns to a sustainable level.
'''

description_COLLECTIVE_8 = '''
Initialize in cooperative mode.

Let:
- `c_prev` = number of opponents who cooperated in the previous round
- `S` = current stock before choosing this round’s action
- `q_high = ceil(3(n-1)/4)`
- `q_min = ceil((n-1)/2)`
- `S_safe = 0.75 * capacity`
- `S_low = 0.40 * capacity`

Decision rule each round:

1. **First round**
   - Play `C`.

2. **If current stock is critically low**
   - If `S < S_low`, play `D` until `S >= S_safe`.

3. **If the previous round was broadly cooperative**
   - If `c_prev >= q_high` and `S >= S_safe`, play `C`.

4. **If the previous round was only moderately cooperative**
   - If `q_min <= c_prev < q_high` and `S >= 0.60 * capacity`, play `C`.
   - Otherwise play `D` for exactly one round as a warning.

5. **If the previous round showed weak cooperation**
   - If `c_prev < q_min`, play `D`.

6. **Re-entry after a punishment round**
   - After playing `D` once, return to `C` immediately if both hold:
     - `c_prev >= q_high`
     - `S >= S_safe`
   - Otherwise stay in `D` until those conditions are met.

7. **Last round**
   - If the stock is not critically low (`S >= S_low`), play `C`.
   - If `S < S_low`, play `D`.

Behavioral pattern:
- Default to cooperation.
- Defect only as a short, collective corrective response to clear under-cooperation or depleted stock.
- Resume cooperation as soon as the group returns to a high-cooperation, stock-safe state.
'''

description_COLLECTIVE_9 = '''
Use a state-contingent collective quota rule.

Define:
- `k_t` = number of opponents who cooperated in round `t-1`
- `q_t = k_t / (n-1)` = observed cooperation rate among opponents
- `S_t` = current stock at start of round `t`

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **Base cooperation threshold**
   - Compute the minimum opponent cooperation rate needed to keep the pool in a healthy regime:
     - `q* = 1/2`
   - Play `C` if both conditions hold:
     - `q_t >= q*`
     - `S_t >= capacity / 2`
   - Otherwise play `D`.

3. **Stock safeguard**
   - If `S_t < capacity / 4`, play `C` unless the previous round had fewer than `(n-1)/4` cooperating opponents.
   - If `S_t <= 0`, play `D` for the rest of the game.

4. **Exploit protection**
   - If the previous round’s observed cooperation rate was below `1/2`, switch to `D` immediately.
   - Stay on `D` until the observed cooperation rate returns to at least `2/3` for one full round.

5. **Recovery mode**
   - After any round in which you play `D`, check whether the next observed cooperation rate is at least `2/3`.
   - If yes, return to `C`.
   - If no, continue `D`.

6. **Final rounds**
   - In the last round, play `C` if `S_t > 0`; otherwise play `D`.
   - In the second-to-last round, use the same rule as usual, but if `S_t < capacity / 3`, play `C` only when at least `2/3` of opponents cooperated in the previous round.

Pseudocode:

```text
if t == 1:
    action = C
else if S_t <= 0:
    action = D
else:
    q = k_t / (n - 1)

    if q < 1/2:
        action = D
    else if S_t >= capacity / 2:
        action = C
    else if S_t < capacity / 4:
        action = C if q >= 2/3 else D
    else:
        action = C if q >= 1/2 else D

if t == r:
    action = C if S_t > 0 else D
```

Collective alignment:
- Default to cooperation.
- Reward visible cooperation with continued cooperation.
- Respond to broad defection by switching to defection.
- Re-enter cooperation only after a clear majority returns to cooperating.
- Protect the shared stock by becoming stricter when the pool is low.
'''

description_COLLECTIVE_10 = '''
Round 1: cooperate.

After every round, count how many opponents cooperated last round, call it `k`.

Maintain a memory flag `pressure`, initialized to 0:
- If `k <= n - 3`, increment `pressure` by 1.
- Otherwise reset `pressure` to 0.

Decision rule for round `t > 1`:

1. If `t == r`:
   - cooperate if `stock >= capacity / 4` or `pressure < 2`
   - defect only if `stock < capacity / 4` and `pressure >= 2`

2. If `t < r`:
   - cooperate if `stock > capacity / 3`
   - cooperate if `stock <= capacity / 3` and `pressure < 2`
   - defect only if `stock <= capacity / 3`, `pressure >= 2`, and `t >= r - 1`

Practical version:
- Default to cooperation.
- Treat a single low-cooperation round as noise.
- Treat two consecutive rounds with at least three opponents defecting as a warning.
- Never defect early unless the pool is already low and persistent noncooperation is visible.
- Once the warning disappears, immediately return to cooperation.

Edge cases:
- If `n = 2`, replace the `n - 3` test with `k == 0` for the pressure update.
- If `n = 3`, set the warning threshold at `k == 0`.
- If the stock is at or above `capacity / 2`, cooperate unconditionally.
- If the stock is at or below `capacity / 4`, cooperate unless the game is in the final round and the warning has persisted for at least two rounds.

Collective posture:
- Cooperate by default.
- Only switch away from cooperation when repeated opponent defection has already pushed the resource into a low-stock regime and the end of the game is near.
- The moment opponents return to broad cooperation, return to cooperation as well.
'''

description_COLLECTIVE_11 = '''
Use a conditional-cooperation rule with a stock-sensitive quorum.

Track:
- `S`: current stock
- `x`: number of opponents who cooperated in the previous round
- `k = x + 1` if you cooperate now, `k = x` if you defect now

Decision rule by round:

- **Round 1:** play `C`.

- **Every later round:**
  1. Compute `s = S / capacity`.
  2. Set the required cooperation quorum:
     - if `s >= 0.70`, require `q = ceil(0.75n)`
     - if `0.40 <= s < 0.70`, require `q = ceil(0.85n)`
     - if `s < 0.40`, require `q = ceil(0.90n)`
  3. Cooperate if and only if `x >= q - 1`.
  4. Otherwise play `D`.

State-based override:
- If stock is extremely low, `S <= 0.20 * capacity`, require an even stronger signal:
  - play `C` only if `x >= ceil(0.95n) - 1`
  - otherwise play `D`

Last-round rule:
- Use the same rule as above, without any special endgame relaxation.

Tie/edge handling:
- If `n = 2`, replace the quorums with:
  - `q = 2` when `s >= 0.70`
  - `q = 2` when `0.40 <= s < 0.70`
  - `q = 2` when `s < 0.40`
- If `x` is exactly on the threshold, cooperate.
- If the previous round had zero cooperators among opponents, defect until cooperation reappears at or above the relevant quorum.

Pseudocode:

```text
if t == 1:
    action = C
else:
    s = S / capacity
    if S <= 0.20 * capacity:
        q = ceil(0.95 * n)
    else if s >= 0.70:
        q = ceil(0.75 * n)
    else if s >= 0.40:
        q = ceil(0.85 * n)
    else:
        q = ceil(0.90 * n)

    if x >= q - 1:
        action = C
    else:
        action = D
```

This keeps you aligned with the group whenever the group is already protecting the resource, and immediately tightens your stance when the stock starts slipping.
'''

description_COLLECTIVE_12 = '''
Let \(q_t\) be the total number of players who cooperated in round \(t\), inferred as:

- \(q_t = 1 +\) observed cooperating opponents if you played \(C\) in round \(t\)
- \(q_t =\) observed cooperating opponents if you played \(D\) in round \(t\)

Maintain two thresholds:

- \(H = \lceil 2n/3 \rceil\)
- \(L = \lceil n/2 \rceil\)

Decision rule in round \(t\):

1. **Round 1:** play \(C\).

2. **If stock \(\le \text{capacity}/3\):** play \(C\) until stock rises above \(\text{capacity}/2\).

3. **If the last two rounds both had \(q < L\):** play \(D\) this round.

4. **Else if the last round had \(q \ge H\):** play \(C\).

5. **Else if the last round had \(L \le q < H\):** play \(C\) if stock is at least \(\text{capacity}/2\); otherwise play \(C\) once more to help recovery.

6. **Else if the last round had \(q < L\):**
   - play \(D\) for one round
   - then return to \(C\) immediately if the next observed \(q \ge L\), otherwise stay in the \(D\)-for-one-round response pattern until cooperation returns to at least \(L\)

7. **Last round:** play \(C\) if the last observed \(q \ge L\); otherwise play \(D\).

8. **Second-to-last round:** if stock is below \(\text{capacity}/2\), play \(C\); otherwise follow the normal rule above.

Persistent behavior:

- Default to \(C\).
- Treat a single weak round as a signal to repair, not to abandon cooperation.
- Treat two consecutive weak rounds as a signal to apply one round of \(D\), then test for recovery.
- Return to \(C\) immediately once the group regains at least \(L\) cooperators.
'''

description_COLLECTIVE_13 = '''
State variables:
- `x_t`: number of opponents who cooperated in round `t`
- `x̄_t = x_t / (n-1)`: observed cooperation share among opponents
- `p_t`: your action in round `t`
- `S_t`: stock at start of round `t`

Parameters:
- `T = ceil((n-1)/2)` as the minimum number of cooperating opponents needed to stay in collective mode
- `H = 2` as the forgiveness window

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Standard play for rounds 2 through r-1**
   - Play `C` if either:
     - `x_{t-1} >= T`, or
     - `x_{t-1} >= T-1` and `x_{t-2} >= T`
   - Otherwise play `D`.

3. **Recovery rule**
   - If you played `D` in the previous round and `x_{t-1} >= T`, immediately return to `C`.
   - If you played `D` and `x_{t-1} < T`, stay with `D` until the rule above is satisfied.

4. **Stock-aware adjustment**
   - If `S_t <= capacity / 4`, play `C` unless `x_{t-1} = 0` for two consecutive rounds.
   - If `S_t >= 3 * capacity / 4`, follow the standard play rule exactly.

5. **Last round**
   - If `x_{r-1} >= T`, play `C`.
   - Otherwise play `D`.

Operationally:
- Cooperate by default.
- Defect only after two consecutive rounds of clearly low opponent cooperation.
- Re-enter cooperation immediately once opponent cooperation recovers to the threshold.
- Never alternate randomly; use the same aggregate thresholds every round.

Pseudocode:
```text
if t == 1:
    action = C
else if t == r:
    action = C if x[t-1] >= T else D
else:
    if S_t <= capacity/4:
        if x[t-1] == 0 and x[t-2] == 0:
            action = D
        else:
            action = C
    else:
        if x[t-1] >= T or (x[t-1] >= T-1 and x[t-2] >= T):
            action = C
        else:
            action = D

if previous_action == D and x[t-1] >= T:
    action = C
```
'''

description_COLLECTIVE_14 = '''
Round 1: cooperate.

Let:
- `S` be the current stock at the start of the round
- `c_prev` be the number of opponents who cooperated in the previous round
- `n` be the number of players
- `k = n - 1` be the number of opponents
- `q = c_prev / k` be the observed cooperation rate among opponents from the previous round

Define the target cooperation threshold:
- `T(S) = 0.75 + 0.25 * (S / capacity)`

Decision rule:
- Cooperate if `q >= T(S)`
- Defect if `q < T(S)`

State-based overrides:
1. If `S <= capacity / 4`, defect.
2. If `S >= 3 * capacity / 4` and `q >= 1/2`, cooperate.
3. If the previous round’s stock increased, and `q >= 1/2`, cooperate.
4. If the previous round’s stock fell by more than `capacity / 8`, defect unless `q = 1`.

Last round:
- Cooperate if at least half of opponents cooperated in the previous round and `S > 0`
- Otherwise defect

First round:
- Cooperate unconditionally

Persistent regime adjustment:
- Track `m`, the number of consecutive rounds in which opponent cooperation rate has been at least `T(S)`:
  - If `m >= 2`, cooperate even when the current round is slightly below threshold, as long as `q >= 1/2` and `S >= capacity / 2`
- Reset `m = 0` whenever `q < T(S)`

Full decision procedure:
```text
At round t:

If t = 1:
    play C
Else:
    observe S and c_prev
    q = c_prev / (n - 1)

    If S <= capacity / 4:
        play D
    Else if t = r:
        if q >= 1/2 and S > 0: play C
        else: play D
    Else:
        T = 0.75 + 0.25 * (S / capacity)

        If previous round stock increased and q >= 1/2:
            play C
        Else if S >= 3 * capacity / 4 and q >= 1/2:
            play C
        Else if q >= T:
            play C
        Else if m >= 2 and q >= 1/2 and S >= capacity / 2:
            play C
        Else:
            play D
```

Collective calibration:
- Treat unanimous or near-unanimous cooperation as the preferred state.
- Match sustained cooperation quickly.
- Withdraw cooperation immediately after a clear drop in opponent cooperation or a sharp stock decline.
- Re-enter cooperation as soon as the observed cooperation rate recovers above the threshold.
'''

description_COLLECTIVE_15 = '''
Cooperate by default, and make cooperation contingent on whether the round’s observed behavior is compatible with preserving the pool.

Maintain two internal variables:

- `trust`: starts at 1
- `pressure`: starts at 0

Update after each round using the observed number of cooperating opponents `k`:

- If `k = n - 1`, increase `trust` by 1 and decrease `pressure` by 1, down to a minimum of 0.
- If `k ≤ n - 2`, decrease `trust` by 1 and increase `pressure` by 1.
- If `k = 0`, set `pressure = pressure + 2`.

Decision rule each round with current stock `S`, current round `t`, and rounds remaining `L = r - t + 1`:

1. Compute the cooperative baseline:
   - `baseline = S / (2n)`

2. Compute the defensive threshold:
   - `threshold = S / n`

3. Cooperate if all of the following hold:
   - `pressure = 0`
   - `trust ≥ 0`
   - `S > 0`

4. Defect if any of the following hold:
   - `pressure ≥ 2`
   - `S ≤ 2n` and `L > 1`
   - `t = r` and `trust < 0`

5. Special last-round rule:
   - On the final round, cooperate only if `pressure = 0` and at least `n - 1` opponents cooperated in the previous round; otherwise defect.

6. Recovery rule after defection by others:
   - After any round with `k ≤ n - 2`, require two consecutive rounds with `k = n - 1` before returning to unconditional cooperation.

Operational interpretation:

- Start cooperatively.
- Continue cooperating while the pool is being treated cooperatively by the group.
- If widespread defection appears, switch to defensive defection until cooperation is restored.
- If the pool is healthy and others are mostly cooperating, return to cooperation immediately.
- Near the end, become stricter and only cooperate under clear cooperative conditions.

Compact pseudocode:

```text
state:
  trust = 1
  pressure = 0

for round t = 1..r:
  if t == r:
    action = C if pressure == 0 and last_round_cooperators >= n-1 else D
  else if pressure >= 2:
    action = D
  else if S <= 2n and remaining_rounds > 1:
    action = D
  else:
    action = C

  observe k = number of cooperating opponents

  if k == n-1:
    trust = max(trust + 1, 0)
    pressure = max(pressure - 1, 0)
  else if k <= n-2:
    trust = trust - 1
    pressure = pressure + 1
    if k == 0:
      pressure = pressure + 1
```
'''

description_COLLECTIVE_16 = '''
Initialize:
- Set `mode = cooperative`
- Set `trust = 1.0`
- Set `last_cooperators = n - 1`
- Set `warning_streak = 0`

Each round `t`:

1. Compute the current stock fraction  
   `x = stock / capacity`

2. Observe the previous round’s opponent cooperation count  
   `k = number of opponents who cooperated in round t-1`  
   For round 1, use `k = n - 1`.

3. Update trust in collective cooperation:
   - `observed_rate = k / (n - 1)` for `n > 2`
   - For `n = 2`, treat `observed_rate = 1` if the opponent cooperated, else `0`
   - Update `trust` as:
     - `trust = 0.7 * trust + 0.3 * observed_rate`

4. Choose action:

   **Round 1**
   - Play `C`

   **Any later round**
   - Play `C` if all of the following hold:
     - `x >= 0.25`
     - `trust >= 0.5`
     - `k >= ceil((n - 1) / 2)`
   - Otherwise play `D`

5. Recovery rule after defection:
   - If you played `D` in the previous round and `k >= ceil((n - 1) / 2)`, return to `C` immediately in the next round.
   - If you played `D` in the previous round and `k < ceil((n - 1) / 2)`, keep playing `D` until either:
     - `k >= ceil((n - 1) / 2)`, or
     - `x >= 0.5` and `trust >= 0.6`

6. Endgame rule:
   - In the final 2 rounds, play `C` if `k > 0`
   - Play `D` only if `k = 0` in the immediately preceding round

7. Edge cases:
   - If `n = 2`, require the opponent to have cooperated in the previous round to continue cooperating.
   - If `stock = 0`, play `D` until the stock becomes positive again.
   - If `stock = capacity`, prefer `C` unless the opponent cooperation signal has clearly broken down.

Collective mindset:
- Default to cooperation.
- Treat a majority of recent cooperation as a signal to preserve the pool together.
- Use defection only as a short, conditional response to sustained breakdown in cooperation, then return to cooperation as soon as the group shows recovery.
'''

description_COLLECTIVE_17 = '''
Initialize in cooperative mode.

Decision rule each round \(t\):

1. **Round 1**
   - Play **C**.

2. **After each round, compute**
   - \(k\) = number of opponents who cooperated last round
   - \(q = k/(n-1)\) = observed opponent cooperation rate
   - \(s = \text{stock}/\text{capacity}\)

3. **Primary rule**
   - Play **C** if both hold:
     - \(q \ge 2/3\), and
     - \(s \ge 1/3\)

   - Otherwise play **D**.

4. **Recovery override**
   - If the previous round had at least \(2/3\) opponent cooperation and \(s \ge 1/4\), play **C** even if the primary rule would choose **D**.
   - This override is allowed only once after a low-cooperation round; if cooperation does not continue, revert to the primary rule.

5. **Severe depletion rule**
   - If \(s \le 1/4\), play **D** unless all opponents cooperated last round.
   - If all opponents cooperated last round, play **C**.

6. **Last round**
   - Use the same rule as above; do not switch to defection just because the game is ending.

State update for the strategy:

- Maintain a one-round memory flag:
  - `repair_mode = true` immediately after a round where \(q < 2/3\)
  - `repair_mode = false` after any round where \(q \ge 2/3\)

- In `repair_mode`, require a stronger signal to cooperate:
  - Play **C** only if \(q \ge 2/3\) and \(s \ge 1/3\)
  - Otherwise play **D**

Collective alignment:

- Default to **C** whenever the group is showing sustained cooperation.
- Use **D** only as a correction signal when cooperation drops below the collective threshold or the stock becomes too depleted.
- Return to **C** immediately after the group restores cooperation.
'''

description_COLLECTIVE_18 = '''
Play cooperatively by default, and use the observed number of cooperating opponents to decide whether the group is staying on a sustainable path.

Let:
- `k_t` = number of opponents who cooperated in round `t-1`  
- `q_t = k_t / (n-1)` = observed cooperation rate among opponents
- `s_t` = stock at start of round `t`

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **Last round**
   - Play `C`.

3. **Otherwise**
   - Compute the target minimum cooperation rate needed to keep the stock in the healthy range:
     - `q_t >= 1/2` means the group is cooperating enough to avoid runaway depletion.
   - Then:
     - If `q_t >= 1/2`, play `C`.
     - If `q_t < 1/2`, play `D` only if both of the following hold:
       - `s_t <= capacity / 2`
       - `q_t <= 1/3`
     - In all other cases, play `C`.

State-based refinement:

- If `s_t >= 3 * capacity / 4`, always play `C`.
- If `s_t <= capacity / 4`, mirror the recent group behavior:
  - play `C` if `q_t >= 1/2`
  - otherwise play `D`

Memory update:

- Track only the most recent round’s observed cooperation count.
- If a round is unobserved or ambiguous, treat it as neutral and keep the previous round’s rule unchanged.

Compact pseudocode:

```text
if t == 1 or t == r:
    action = C
else:
    q = k_t / (n - 1)

    if s_t >= 0.75 * capacity:
        action = C
    else if q >= 0.5:
        action = C
    else if s_t <= 0.25 * capacity and q <= 1/3:
        action = D
    else:
        action = C
```

Collective alignment rule:

- Stay cooperative as long as the group shows moderate cooperation.
- Defect only when cooperation has clearly broken down and the stock is already depressed.
- Immediately return to cooperation once the group cooperation rate recovers to at least half.
'''

description_COLLECTIVE_19 = '''
Play a stock-preserving threshold policy with a short calibration phase and then adjust to the observed cooperation level.

Let:

- `k_t` = number of opponents who cooperated in round `t-1`
- `m_t = n - 1` = number of opponents
- `x_t = k_t / m_t` = observed opponent cooperation rate
- `S_t` = stock at the start of round `t`

Decision rule for round `t`:

1. **Round 1**
   - Play `C`.

2. **Calibration phase**
   - For rounds `t = 2, 3`, play `C` if `x_t >= 2/3`, otherwise play `D`.

3. **Main phase**
   - Compute the expected group consumption if you play `C` and if you play `D` using the last observed opponent cooperation rate:
     - If you play `C`, expected total consumption is  
       `S_t/(2n) + (n-1) * [x_t * S_t/(2n) + (1-x_t) * S_t/n]`
     - If you play `D`, expected total consumption is  
       `S_t/n + (n-1) * [x_t * S_t/(2n) + (1-x_t) * S_t/n]`
   - Let `S'_C` and `S'_D` be the resulting post-growth stocks.
   - Choose `C` if `S'_C >= 0.9 * capacity` or if `x_t >= 2/3`.
   - Otherwise choose `D` only if `S'_D > S'_C` by a meaningful margin; equivalently, choose `D` when `x_t < 1/2`.
   - In the intermediate region `1/2 <= x_t < 2/3`, play `C`.

4. **Stock-protection override**
   - If `S_t <= 0.6 * capacity`, play `C` regardless of `x_t`.
   - If `S_t <= 0.35 * capacity`, play `C` for the next two rounds regardless of history.

5. **Exhaustion guard**
   - If the stock has declined for two consecutive rounds, play `C` once to help restore the pool.
   - If the stock has declined for three consecutive rounds, continue playing `C` until either:
     - stock rises for one round, or
     - `x_t < 1/3` for two consecutive observed rounds, in which case switch to `D`.

6. **Final rounds**
   - If `t = r`, play `C` if `x_t >= 1/2` or `S_t > 0.5 * capacity`; otherwise play `D`.
   - If `t = r - 1`, play `C` unless `x_t < 1/3` and `S_t < 0.5 * capacity`.

State update memory:

- After each round, record whether stock increased, stayed flat, or decreased.
- Maintain:
  - `coop_streak` = consecutive rounds with `x_t >= 2/3`
  - `defect_streak` = consecutive rounds with `x_t < 1/3`
  - `decline_streak` = consecutive rounds where stock fell

Compact policy form:

```text
if t == 1:
    play C
elif S_t <= 0.35*capacity:
    play C
elif decline_streak >= 3:
    play C
elif t in {r, r-1}:
    play C if (x_t >= 1/2 or S_t > 0.5*capacity) else D
elif x_t >= 2/3:
    play C
elif x_t < 1/3 and S_t > 0.7*capacity:
    play D
else:
    play C
```

Collective orientation:

- Default to `C`.
- Defect only when observed cooperation is clearly weak and the stock is still healthy.
- Revert immediately to `C` when the stock weakens.
- Use the anonymous cooperation rate, not identities, as the basis for adjustment.
'''

description_COLLECTIVE_20 = '''
Use a state-triggered contingent cooperation rule:

Let:
- `S` = current stock at the start of the round
- `m` = number of opponents who cooperated in the previous round
- `n` = number of players
- `N = n - 1` = number of opponents
- `q = m / N` = observed opponent cooperation rate in the previous round
- `q* = 1/2` = baseline cooperation threshold
- `H` = high-cooperation threshold, set to `ceil(2N/3)`
- `L` = low-cooperation threshold, set to `floor(N/3)`

Decision rule each round:

1. **First round**
   - Play `C`.

2. **If the stock is low**
   - If `S <= 2n`, play `C` only if `m = N` in the previous round; otherwise play `D`.
   - If `S <= n`, play `D` unless `m = N` for two consecutive rounds.

3. **If the stock is moderate or high**
   - Play `C` if `m >= q* N` and `S > n`.
   - Play `D` if `m < q* N` or `S <= n`.

4. **Recovery mode after defection by others**
   - If the previous round had `m <= L`, enter a 2-round recovery test:
     - In the next round, play `D` if `S <= n`; otherwise play `C` once.
     - If opponent cooperation rises to at least `H` in that round, return to normal cooperative play.
     - If not, continue with `D` until `m >= q* N`.

5. **Reward mode after strong cooperation**
   - If `m >= H` and `S > n`, play `C` for the next round regardless of the previous round’s action profile.
   - If this high-cooperation condition persists, keep playing `C`.

6. **Last round**
   - If `S > n`, play `C` when `m >= q* N`, otherwise play `D`.
   - If `S <= n`, play `D` unless `m = N` in the previous round.

State update logic:
- After every round, use the observed opponent cooperation count `m` to classify the round:
  - `m >= H` → cooperative regime
  - `L < m < H` → neutral regime
  - `m <= L` → punishment/regime-breakdown
- Keep a short memory of the last two rounds only to detect whether cooperation is stable or whether a recovery attempt has succeeded.

Compact pseudocode:

```text
if round == 1:
    action = C
else if S <= n:
    action = C iff last_two_rounds_both_had_m == N
    otherwise D
else if S <= 2n:
    if last_round_m == N:
        action = C
    else if last_round_m >= H:
        action = C
    else:
        action = D
else:
    if last_round_m >= q* N:
        action = C
    else if last_round_m <= L:
        action = D
    else:
        action = C
```

Collective commitment rule:
- Default to cooperation when others are broadly cooperating and the stock is healthy.
- Switch to defection immediately when cooperation falls below the maintenance threshold or the stock becomes fragile.
- Restore cooperation as soon as the observed cooperation rate returns to a sustainable level.
'''

description_COLLECTIVE_21 = '''
Play a stock-preserving threshold policy with explicit punishment and recovery phases.

**Core rule**

Let `k_t` be the number of opponents who cooperated in round `t-1`, and let `S_t` be the stock at the start of round `t`.

Define:
- `coop_rate_t = k_t / (n - 1)` for `t > 1`
- `expected_depletion_if_all_C = S_t / 2`
- `critical_stock = 2n`  
- `safe_stock = max(2n, capacity / 2)`

Choose action in round `t` as follows:

### Round 1
- Cooperate.

### Standard decision rule for rounds `t >= 2`
1. **If stock is critically low**
   - If `S_t <= 2n`, cooperate unless all opponents defected in the previous round; if all defected, defect.
   - If `S_t == 0`, cooperate.

2. **If the group was mostly cooperative last round**
   - If `coop_rate_t >= 0.75`, cooperate.

3. **If the group was mixed**
   - If `0.40 <= coop_rate_t < 0.75`, cooperate only if `S_t >= safe_stock`; otherwise defect.

4. **If the group was mostly selfish last round**
   - If `coop_rate_t < 0.40`, defect.
   - Stay in defect mode until both:
     - `coop_rate_t >= 0.75` for one full round, and
     - `S_t >= safe_stock`

---

**Punishment and recovery**

Maintain a hidden mode:

- `normal`
- `punishment`
- `recovery`

### Enter punishment
Switch to `punishment` if either:
- fewer than `40%` of opponents cooperated in the previous round, or
- stock drops below `critical_stock`

### Behavior in punishment
- Defect.
- Continue defecting until the previous round shows strong restraint:
  - `coop_rate_t >= 0.75`
  - and `S_t >= safe_stock`

### Enter recovery
When the condition above is first satisfied:
- switch to `recovery`
- cooperate for one round

### Behavior in recovery
- Cooperate for one round.
- If the next round again has `coop_rate_t >= 0.75`, return to `normal`.
- If not, return immediately to `punishment`.

---

**Normal mode**

In `normal`, cooperate whenever the group appears cooperative enough to sustain the stock:
- cooperate if `coop_rate_t >= 0.75`
- defect if `coop_rate_t < 0.75`

This keeps the default posture collective and supportive while refusing to subsidize persistent free-riding.

---

**Endgame rule**

For the last two rounds:
- If `S_t > safe_stock` and `coop_rate_t >= 0.75`, cooperate.
- Otherwise defect.

If the remaining horizon is short and the stock is already low, protect the stock rather than trying to rebuild it.

---

**Tie-breaking and edge cases**

- If no prior-round data exist, cooperate in the first round.
- If `n = 2`, interpret the thresholds directly:
  - `coop_rate_t = 1` means the other player cooperated
  - `coop_rate_t = 0` means the other player defected
- If `S_t` is near zero, cooperate only if the other side has shown clear restraint; otherwise defect.
- If stock is at capacity and the previous round was fully cooperative, cooperate unconditionally.

---

**Compact pseudocode**

```text
mode = normal

round 1:
    C

for t >= 2:
    coop_rate = opponents_cooperated_last_round / (n - 1)

    if t in {r-1, r}:
        if S_t > max(2n, capacity/2) and coop_rate >= 0.75:
            C
        else:
            D
        continue

    if S_t <= 2n:
        if coop_rate == 1:
            D
        else:
            C
        continue

    if mode == punishment:
        if coop_rate >= 0.75 and S_t >= max(2n, capacity/2):
            mode = recovery
            C
        else:
            D

    else if mode == recovery:
        C
        if coop_rate < 0.75:
            mode = punishment
        else:
            mode = normal

    else:  # normal
        if coop_rate >= 0.75:
            C
        else if coop_rate >= 0.40 and S_t >= max(2n, capacity/2):
            C
        else:
            mode = punishment
            D

    if coop_rate < 0.40 or S_t < 2n:
        mode = punishment
```

**Collective principle**

Default to cooperation when the group is behaving in a way that preserves the common stock, and switch quickly to withholding when the group shows signs of overuse. Return to cooperation immediately once restraint reappears, so the policy rewards collective discipline and stabilizes the resource around sustainable play.
'''

description_COLLECTIVE_22 = '''
Round 1: cooperate.

For every later round t:

1. Let `m_prev` be the number of opponents who cooperated in round `t-1`.
2. Let `m_curr` be the number of opponents who cooperated in round `t-2` if available.
3. Let `s = stock / capacity`.

Decision rule:
- Cooperate if all three hold:
  - `s >= 0.5`
  - `m_prev >= ceil((n-1)/2)`
  - either `t <= 2` or `m_prev >= m_curr` or `m_prev >= ceil((n-1)/2) + 1`
- Defect otherwise.

Endgame rule:
- In the final round, use the same rule, but require `s >= 0.6` to cooperate.
- If `s < 0.6`, defect in the final round.

Recovery rule:
- After any round in which you defect, return to cooperation immediately once:
  - `s >= 0.5`, and
  - at least half of the opponents cooperated in the previous round.

Emergency rule:
- If `s <= 0.25`, defect until `s` rises back above `0.5` and the opponents’ cooperation has reached the majority threshold again.

Pseudocode:

```text
if t == 1:
    action = C
else:
    majority = ceil((n-1)/2)
    if t == r:
        action = C if (stock/capacity >= 0.6 and m_prev >= majority) else D
    else:
        if stock/capacity >= 0.5 and m_prev >= majority:
            if t <= 2 or m_prev >= m_curr or m_prev >= majority + 1:
                action = C
            else:
                action = D
        else:
            action = D
```

This strategy starts fully cooperative, stays cooperative while the group is sustaining the pool, and switches to defection only when the pool is strained or the observed cooperation level falls below the cooperative majority.
'''

description_COLLECTIVE_23 = '''
Use a threshold-based contingent cooperation policy with three phases: establish, sustain, and repair.

Let:
- \(k_t\) = number of opponents who cooperated in round \(t\)
- \(a_t\) = your action in round \(t\)
- \(m_t = k_t + \mathbf{1}[a_t = C]\) = total cooperators including you
- \(x_t = m_t / n\) = observed cooperation rate in the whole group for that round

Decision rules:

1. First round
- Play \(C\).

2. Standard rule for rounds \(t = 2, \dots, r-1\)
- Play \(C\) if both conditions hold:
  - \(k_{t-1} \ge \lceil 2(n-1)/3 \rceil\), and
  - stock has not collapsed: the current stock is at least \(0.6 \times\) capacity.
- Otherwise play \(D\).

3. Support rule for strong cooperation
- If the previous round had near-universal cooperation, defined as \(k_{t-1} = n-1\), play \(C\) again even if the stock is moderately below the main threshold, as long as stock is at least \(0.4 \times\) capacity.

4. Repair rule after defection by others
- If \(k_{t-1} < \lceil (n-1)/2 \rceil\), play \(D\) for the next round.
- Stay in this defensive mode until a round occurs with \(k_{t-1} \ge \lceil 2(n-1)/3 \rceil\), then return to \(C\).

5. Last round
- Play \(C\) if \(k_{r-1} \ge \lceil (n-1)/2 \rceil\).
- Otherwise play \(D\).

State update logic:

- Maintain a mode flag:
  - `cooperative` if recent cooperation is consistently high
  - `defensive` if recent cooperation falls below the repair threshold

- Initialize in `cooperative`.
- Switch to `defensive` immediately after any round with too few cooperators:
  - if \(k_t < \lceil (n-1)/2 \rceil\)
- Switch back to `cooperative` only after a round with strong cooperation:
  - if \(k_t \ge \lceil 2(n-1)/3 \rceil\)

Refined round-by-round policy:

- If mode = `cooperative`:
  - play \(C\) when recent cooperation is high and stock remains healthy
  - otherwise play \(D\) once to signal non-acceptance of free-riding

- If mode = `defensive`:
  - play \(D\) until cooperation recovers to the strong-cooperation threshold
  - once recovered, return to \(C\) immediately

Edge cases:

- If stock is extremely low, below \(0.2 \times\) capacity, play \(D\) for that round unless the previous round had full cooperation.
- If a round produces zero or near-zero cooperation, treat it as a breakdown:
  - play \(D\) in the next round
  - require two consecutive strong-cooperation rounds before resuming unconditional \(C\) behavior
- If the observed cooperation rate is exactly on a threshold, treat it as meeting the threshold only for the upper threshold and failing it for the lower repair threshold.

Compact pseudocode:

```text
mode = cooperative

for each round t:
    if t == 1:
        play C
        continue

    if t == r:
        if k[t-1] >= ceil((n-1)/2):
            play C
        else:
            play D
        continue

    if mode == defensive:
        if k[t-1] >= ceil(2*(n-1)/3):
            mode = cooperative
            play C if stock >= 0.6*capacity else D
        else:
            play D
    else:  # cooperative
        if k[t-1] >= ceil(2*(n-1)/3) and stock >= 0.6*capacity:
            play C
        elif k[t-1] == n-1 and stock >= 0.4*capacity:
            play C
        else:
            play D
            if k[t-1] < ceil((n-1)/2):
                mode = defensive
```

Collective mindset:
- Start by cooperating.
- Keep cooperating while the group is broadly cooperating and the stock remains healthy.
- Withdraw cooperation only when collective discipline breaks down.
- Re-enter cooperation immediately once the group restores strong cooperation.
- Never stay defensive longer than necessary once the group returns to a cooperative pattern.
'''

description_COLLECTIVE_24 = '''
Start by cooperating in round 1.

After each round, compute the observed cooperation rate among the other players:
- let k be the number of observed cooperating opponents
- let m = n - 1
- let q = k / m

Maintain a state variable:
- `mode ∈ {normal, recovery, punishment}`
- initialize `mode = normal`
- maintain `low_trust_streak = 0`

Use the current stock `S` and the observed cooperation rate `q` to choose:

**Core rule**
- Cooperate if `q ≥ 0.5` and `S > capacity / 3`
- Defect if `q < 0.5` or `S ≤ capacity / 3`

**Aggressive depletion protection**
- If `S ≤ capacity / 5`, defect regardless of `q`
- If `S ≤ 2n`, defect regardless of `q`

**Collective repair rule**
- If `q = 1` for two consecutive rounds, cooperate even if `S` is moderately low, as long as `S > capacity / 6`

**Response to partial defection**
- If `0 < q < 0.5`, set `mode = punishment`
- In punishment mode:
  - defect for the next round
  - continue defecting until either:
    - `q ≥ 0.5` in a later round, or
    - `S > capacity / 2` and at least one full round has passed with `q ≥ 0.5`
- Once either condition holds, switch to `recovery`

**Recovery mode**
- In recovery mode, cooperate if:
  - `q ≥ 0.5`, and
  - `S > capacity / 4`
- Otherwise defect
- Leave recovery mode and return to normal after two consecutive rounds of cooperation by at least half of the other players

**Last-round rule**
- In the final round, cooperate only if both conditions hold:
  - `q = 1`
  - `S ≥ capacity / 2`
- Otherwise defect

**Early-round rule**
- If no history exists beyond round 1, use only the initial rule: cooperate in round 1, then update from observations

**Short-memory update**
- After each round:
  - if `q ≥ 0.5`, increment `low_trust_streak` only when `S` is falling sharply; otherwise reset it
  - if `q < 0.5`, set `low_trust_streak += 1`
- If `low_trust_streak ≥ 2`, switch to punishment
- If `low_trust_streak = 0` for two consecutive rounds and `S > capacity / 3`, return to normal

**Collective mindset**
- Default to cooperation when the observed group is broadly cooperating and the stock is healthy
- Shift to defection immediately when the group is extracting too aggressively or the stock becomes fragile
- Restore cooperation only after the group has demonstrated sustained restraint
'''

description_COLLECTIVE_25 = '''
Use a stock-preserving threshold policy with a recovery mode and a final-round safeguard.

Let:
- `c_t` = number of opponents who cooperated in round `t`
- `k_t = c_t + 1` if you cooperated, else `k_t = c_t`
- `S_t` = stock at start of round `t`
- `x_t = S_t / capacity` = normalized stock

Define the cooperative threshold:
- `T_t = ceil((n - 1) / 2)` for all rounds
- `T_t = n - 1` in the last two rounds if `x_t < 0.4`

Decision rule each round:

1. First round:
   - Cooperate.

2. Standard round:
   - Cooperate if both conditions hold:
     - `c_{t-1} >= T_{t-1}`
     - `x_t >= 0.25`
   - Otherwise defect.

3. Recovery mode:
   - If you defected in the previous round, return to cooperation only when:
     - `c_{t-1} >= n - 2`
     - `x_t >= 0.5`
   - If either condition fails, defect again.

4. Low-stock protection:
   - If `x_t < 0.2`, defect unless `c_{t-1} = n - 1` and `x_t >= 0.3`.
   - If `x_t <= 0.05`, defect unconditionally.

5. Late-game safeguard:
   - In the final round, cooperate only if:
     - `c_{r-1} >= n - 1`
     - `x_r >= 0.5`
   - Otherwise defect.
   - In the penultimate round, require `c_{r-2} >= n - 2` and `x_{r-1} >= 0.4` to cooperate.

6. Escalation after collapse:
   - If the stock ever falls below `0.1 * capacity`, defect for the next two rounds unless unanimous cooperation is observed in both rounds.

Pseudocode:

```text
if t == 1:
    play C
else if t == r:
    if c_{t-1} >= n-1 and x_t >= 0.5:
        play C
    else:
        play D
else if x_t <= 0.05:
    play D
else if x_t < 0.2:
    if c_{t-1} == n-1 and x_t >= 0.3:
        play C
    else:
        play D
else if last_move == D:
    if c_{t-1} >= n-2 and x_t >= 0.5:
        play C
    else:
        play D
else:
    if c_{t-1} >= ceil((n-1)/2) and x_t >= 0.25:
        play C
    else:
        play D
```

Collective conventions:
- Cooperate by default when the group is mostly cooperating and the stock is healthy.
- Defect immediately when cooperation drops below the majority threshold.
- Re-enter cooperation only after the group restores a strong cooperative signal.
- Treat late rounds and low stock as protection periods, not trust-building periods.
'''

description_COLLECTIVE_26 = '''
Initialize in cooperative mode.

Let `y_t` be the number of opponents who cooperated in round `t`, observed after the round ends.  
Let `M = ceil((n - 1)/2)`.

Decision rule for round `t`:

1. **Round 1:** play `C`.

2. **Cooperative mode:** play `C`.

3. **Switch into defensive mode** if either of these holds:
   - `y_{t-1} < M` for **two consecutive rounds**, or
   - current stock before the round is below `capacity / 3`.

4. **Return to cooperative mode** immediately when `y_{t-1} >= M`.

5. **Defensive mode:** play `D`.

Memory and update rule:
- Start in cooperative mode.
- After each round, update the mode using only the most recent opponent cooperation count and the current stock.
- If the last two observed rounds are unavailable, treat missing history as cooperative.

Edge handling:
- **If `n = 2`**, then `M = 1`, so any observed opponent cooperation keeps the group in cooperative mode.
- **If the stock is very low** (`stock < capacity / 3`), stay defensive until cooperation returns to at least a majority of opponents.
- **In the final round**, do not change the rule: play according to the current mode.
- **If stock reaches 0**, play `D` thereafter unless a later round begins with positive stock again.

Collective discipline:
- Default to `C`.
- Only move to `D` after repeated evidence that the group is not cooperating enough or the stock has fallen into a danger zone.
- The first sign of restored majority cooperation immediately resets the strategy back to `C`.
'''

description_COLLECTIVE_27 = '''
Round 1: cooperate.

For round t > 1, let k be the number of opponents who cooperated in round t−1, and let b = ceil((n−1)/2).

Decision rule:
- If stock ≤ capacity / 3: cooperate.
- Else if k ≥ b: cooperate.
- Else if the last two rounds both had k < b: defect.
- Else: cooperate.

Endgame rule:
- In the final round, if the previous round had k ≥ b, cooperate; otherwise defect only if stock > capacity / 2, and cooperate when stock ≤ capacity / 2.

Update memory:
- Keep only the last two observed cooperation counts.
- Reset the “defect” state immediately after any round with k ≥ b.

Behavioral interpretation:
- Stay cooperative whenever the group is sustaining itself or the stock is low.
- Use defecting only as a short, symmetric response to repeated under-cooperation.
- Return to cooperation as soon as the group recovers to at least a simple majority of cooperators.
'''

description_COLLECTIVE_28 = '''
Use a stock-preserving threshold policy with conditional reciprocity.

Maintain two internal signals:

- `C_count`: number of opponents who cooperated in the previous round
- `trend`: whether stock has been stable, rising, or falling over recent rounds

Define:

- `safe_share = stock / (2n)`
- `max_safe_defect_share = stock / n`
- `coop_ratio = C_count / (n - 1)` for `n > 1`

Decision rule each round:

1. **First round**
   - Cooperate.

2. **Last two rounds**
   - Cooperate unless the stock is already near collapse.
   - Defect only if `stock <= 2n` or `stock <= 0.25 * capacity`.

3. **Normal rounds**
   - Cooperate if both conditions hold:
     - `coop_ratio >= 0.5`
     - `stock >= 0.4 * capacity`
   - Defect if either condition fails:
     - `coop_ratio < 0.5`
     - `stock < 0.4 * capacity`

4. **Recovery mode after a low-stock round**
   - If `stock < 0.25 * capacity`, cooperate until both:
     - `coop_ratio >= 0.75`
     - `stock >= 0.5 * capacity`
   - While in recovery mode, never defect.

5. **Escalation against persistent defection**
   - If `coop_ratio == 0` for two consecutive rounds, defect for the next round.
   - Stay defecting until either:
     - `coop_ratio >= 0.5`, or
     - `stock >= 0.6 * capacity` after a cooperative round by others

6. **Forgiveness rule**
   - If at least half of opponents cooperated in the previous round, return to cooperation immediately unless the stock is already in recovery mode or near the endgame collapse threshold.

7. **Endgame alignment**
   - In the final third of rounds, prefer cooperation whenever `stock >= 0.3 * capacity`.
   - In the final third, defect only if the group is already in a low-cooperation regime:
     - `coop_ratio < 0.4` or `stock < 0.3 * capacity`

State update after each round:

- Record `C_count`
- Update `trend` from current stock relative to previous stock:
  - rising if stock increased
  - falling if stock decreased
  - stable otherwise

Collective mindset rule:

- Default to cooperation whenever the group is maintaining the resource.
- Switch to defection only as a temporary defense when the group is visibly overusing the pool.
- Return to cooperation immediately once the group shows restraint again.
'''

description_COLLECTIVE_29 = '''
- **Round 1:** Cooperate.

- **State to track:**
  - `q =` fraction of opponents who cooperated in the previous round
  - `low =` number of consecutive rounds with `q < 1/2`
  - `stock_ratio = stock / capacity`

- **Core rule:**
  - Stay cooperative by default.
  - Switch to defection only when cooperation has clearly broken down, and return to cooperation as soon as the group recovers.

- **Decision rule for round t > 1:**
  - **Cooperate** if any of the following holds:
    - `q >= 1/2`
    - `stock_ratio < 1/2` and `q >= 1/3`
    - `low == 1` and `q >= 1/3`
  - **Defect** otherwise.

- **Recovery rule:**
  - If you defect in one round, immediately test cooperation again next round unless the previous round also had `q < 1/3`.
  - Never stay in defection for more than one round unless the group has remained below `1/3` cooperation for two consecutive rounds.

- **Escalation rule:**
  - If `q < 1/3` for two rounds in a row, defect until `q` returns to at least `1/2`.

- **Last round:**
  - Use the same rule as above.
  - Do not switch to opportunistic defection just because no future rounds remain.

- **Compact pseudocode:**
  ```text
  if t == 1:
      play C
  else:
      if q >= 1/2:
          play C
      else if stock_ratio < 1/2 and q >= 1/3:
          play C
      else if low == 1 and q >= 1/3:
          play C
      else:
          play D

  update low:
      if q < 1/2:
          low += 1
      else:
          low = 0
  ```

- **Collective posture:**
  - Cooperate whenever the group is still broadly cooperating.
  - Use defection only as a short, bounded response to sustained breakdown.
  - Rebuild cooperation immediately once the observed cooperation level improves.
'''

description_COLLECTIVE_30 = '''
Initialize with cooperation.

For round t with current stock S:

1. Compute the observed opponent cooperation rate from the previous round:
   - p = (# opponents who cooperated last round) / (n - 1)
   - If no previous round exists, set p = 1

2. Compute the two-round support score:
   - h = p
   - If the round before last exists, replace h with (2p + p_prev) / 3
   - If only one past round exists, use h = p

Decision rule:
- Cooperate if t = 1 or t = 2
- Cooperate if S <= capacity / 2
- Cooperate if h >= 1/2
- Cooperate if r - t <= 2 and p >= 1/2
- Otherwise defect

Recovery rule after defecting:
- Keep defecting only while both conditions hold:
  - h < 2/5
  - S > 3 * capacity / 4
- Return to cooperation immediately when either:
  - h >= 1/2, or
  - S <= 3 * capacity / 4

Final round rule:
- Cooperate unless the previous round had fewer than half of opponents cooperating
- If the previous round had fewer than half cooperating, defect only if S > capacity / 2; otherwise cooperate

No-memory edge cases:
- First round: cooperate
- If the game reaches a state with S very low, always cooperate until S rises above capacity / 2 again
- If the game has been stable with majority cooperation for the last two rounds, continue cooperating without interruption

State update logic:
- Track only the last two observed opponent cooperation rates
- Never use identity-based retaliation; respond only to aggregate cooperation levels and current stock
- Default to cooperation whenever the stock is under pressure or the group is sustaining the resource

'''

description_COLLECTIVE_31 = '''
Play a stock-preserving threshold strategy with memory of the observed cooperation rate.

Maintain:
- `S`: current stock before the round
- `c_prev`: number of opponents who cooperated in the previous round
- `rho`: observed opponent cooperation rate, `rho = c_prev / (n-1)` after the first round

Decision rule each round `t`:

1. Compute the minimum cooperation rate needed to keep the stock from shrinking under the current state:
   - If `S = 0`, cooperate.
   - Otherwise set  
     `tau(S) = max(0, min(1, 2 - 2n / S))`
   This is the approximate cooperation threshold that keeps expected consumption from exceeding the level the stock can regenerate from.

2. Choose an aspiration level:
   - `a_t = max(tau(S), 0.5)`
   - In the final third of the game, keep `a_t = tau(S)` only if stock is already clearly above half capacity; otherwise use `0.5`.

3. Action choice:
   - Cooperate if `rho >= a_t`
   - Defect if `rho < a_t`

First round:
- Cooperate.

Ongoing adaptation:
- If the previous round’s stock increased or remained near capacity, reduce the threshold slowly toward `0.5`:
  - `a_t := max(0.5, a_t - 1/(2r))`
- If the previous round’s stock fell, raise the threshold quickly:
  - `a_t := min(1, a_t + 1/(n-1))`

Reactive correction:
- If at least `n-2` opponents cooperated in the previous round, cooperate next round unless the stock is very low (`S < n`).
- If fewer than half of opponents cooperated in the previous round, defect next round unless the stock is near full (`S > capacity/2` and `t` is early).

Final rounds:
- If `t = r`, cooperate only if at least half of opponents cooperated in the previous round and `S` is not low.
- If `t = r-1`, behave as if one failed cooperative round would be costly: cooperate only if `rho >= 0.5` and `S >= capacity/3`.

Edge cases:
- If `n = 2`, treat the single observed opponent as the entire signal:
  - Cooperate if the opponent cooperated last round and stock is not collapsing.
  - Otherwise defect.
- If the stock is at or above `capacity - ε`, cooperate unless the opponent cooperation rate is extremely low (`rho < 0.25`).
- If the stock is at or below `ε`, cooperate only if the opponent cooperation rate is near universal (`rho >= 0.9`); otherwise defect to avoid donating to immediate depletion.

Collective mindset:
- Start by cooperating.
- Continue cooperating whenever the observed group behavior is broadly cooperative and the stock is healthy.
- Switch to defect only when the group is persistently extracting too much or when the stock is already being driven down.
- Return to cooperation immediately after a stable cooperative signal reappears.
'''

description_COLLECTIVE_32 = '''
Play cooperatively by default and treat the pool as a shared budget.

Decision rule each round:

- Let `k` be the number of opponents who cooperated in the previous round.
- Let `m = n - 1` be the number of opponents.
- Let `c = k / m` be the observed cooperation rate among opponents.
- Let `S` be the current stock before acting.

Choose `C` unless one of the following triggers `D`:

1. Retaliation trigger:
   - If `c < 0.5`, play `D` for this round.

2. Scarcity trigger:
   - If `S <= capacity / 4`, play `D`.

3. Endgame trigger:
   - If `r - t <= 2` and `c < 1`, play `D`.

Otherwise play `C`.

Round-by-round behavior:

- Round 1:
  - Play `C`.

- Middle rounds:
  - Continue playing `C` while a majority of opponents cooperated last round and the stock remains healthy.
  - Switch to `D` immediately after a clear drop in cooperation or when the stock becomes low.

- Final two rounds:
  - Play `C` only if every observed opponent cooperated in the previous round and the stock is not low.
  - Otherwise play `D`.

Recovery rule:
- If the previous round had `c = 1` and stock has risen since the last time you defected, return to `C` immediately.

Persistence rule:
- After a round in which you play `D`, keep playing `D` until either:
  - opponents return to unanimous cooperation for one round, or
  - the stock recovers above `capacity / 2`.

This yields the following practical policy:

- Start with cooperation.
- Mirror the group’s level of cooperation, but only punish substantial defection.
- Defect when the pool is being overused.
- Restore cooperation as soon as the group proves it can sustain the resource.
- Never defect against a fully cooperative group unless the resource is already dangerously depleted.
'''

description_PROSOCIAL_5 = '''
Play `C` by default.

Maintain two internal values:
- `trust` = current cooperation expectation for others, initialized at `n-1`
- `probe` = a short retaliation counter, initialized at `0`

At the start of each round `t` with current stock `S`:

1. Compute the minimum number of cooperating opponents needed to keep the pool from collapsing:
   - `safe = ceil((n - 2) / 2)`  
   This is the smallest cooperation count among the other `n-1` players that still makes broad restraint the norm.

2. If `probe > 0`, play `C` and decrement `probe` by 1.

3. Otherwise, use this rule:
   - Play `C` if at least `safe` opponents cooperated in the previous round.
   - Play `D` only if fewer than `safe` opponents cooperated in the previous round and the stock is already low enough that restraint is not being reciprocated:
     - `S <= capacity / 2`

After the round:
- Let `k` be the number of opponents who cooperated in that round.
- Update `trust` toward `k`:
  - `trust = 0.7 * trust + 0.3 * k`
- If `k < safe`, set `probe = 1` unless it is the final round.
- If `k >= safe`, set `probe = 0`

First round:
- Play `C`

Last round:
- Play `C` unless the previous round showed severe free-riding:
  - If `k < safe` and `S <= capacity / 2`, play `D`
  - Otherwise play `C`

Very low stock edge case:
- If `S <= capacity / 4`, play `C` regardless of history to avoid accelerating collapse.

Very high stock edge case:
- If `S >= 3 * capacity / 4`, play `C` regardless of history to reinforce full recovery.

Persistent free-riding edge case:
- If opponents have failed the `safe` threshold for two consecutive non-final rounds, play `D` for exactly one round, then return to `C` unless cooperation improves.

Long-run cooperation reset:
- If the previous round had all opponents cooperate, clear `probe` and always play `C` for the next two rounds.
'''

description_PROSOCIAL_6 = '''
Round 1: play C.

For every round t > 1:

1. Let `q` be the fraction of opponents who cooperated in round `t-1`:
   - `q = (# opponents who played C in t-1) / (n - 1)`

2. Let `trend` be the change in opponent cooperation:
   - `trend = q - q_prev`
   - if there is no `q_prev`, treat `trend = 0`

3. Let `low_stock` be true when the current stock is below one-third of capacity.

4. Play:
   - `C` if `q >= 1/2`
   - `C` if `q < 1/2` but `low_stock` is false
   - `C` if `q < 1/2`, `low_stock` is true, and `trend >= 0`  
   - `D` only if all of the following hold:
     - `q < 1/3`
     - `low_stock` is true
     - `q_prev < 1/3` as well
     - current stock has fallen in each of the last two rounds

Store `q_prev = q` after each round.

Edge cases:
- If the first observed round is the only prior data point, use the round-1 rule above and keep `trend = 0`.
- In the final round, use the same decision rule; do not change behavior just because the game is ending.
- If the stock is extremely high, always play `C`.
- If no reliable history is available for any reason, default to `C`.

This strategy is cooperation-first, only withholding cooperation in the narrowest possible situation where repeated heavy defection is already driving the resource into collapse.
'''

description_PROSOCIAL_7 = '''
Round 1: cooperate.

Maintain two internal memories:
- `low_support_streak`: consecutive rounds in which fewer than half of the other players cooperated
- `repair_mode`: a counter of forced cooperation rounds after a collapse

Each round `t > 1`:

1. If `stock <= 0`, cooperate.
2. If `repair_mode > 0`, cooperate and decrement `repair_mode`.
3. Otherwise, let `m` be the number of opponents who cooperated in the previous round, and let `f = m / (n - 1)`.

Decision rule:
- Cooperate if `f >= 1/2`.
- Cooperate if `f < 1/2` but the current stock is still healthy, meaning `stock / capacity >= 1/2`.
- Defect only if both of the following hold:
  - `f < 1/2` for two consecutive rounds
  - `stock / capacity < 1/2`

When defecting:
- Set `repair_mode = 2`
- Reset `low_support_streak = 0`

When cooperating:
- If `f >= 1/2`, reset `low_support_streak = 0`
- If `f < 1/2`, increment `low_support_streak`

Escalation and forgiveness:
- If `low_support_streak >= 2` and `stock / capacity < 1/2`, defect once and then immediately re-enter cooperation after the two-round repair period.
- Exit `repair_mode` early only if `f >= 2/3` and `stock / capacity >= 1/2`.

Last round:
- Cooperate unless the previous round met the exact defection trigger above; in that case, defect only if `stock / capacity < 1/2`.
- If `stock == 0`, always cooperate.

Pseudocode:

```text
if t == 1:
    action = C
else:
    f = previous_opponent_cooperators / (n - 1)

    if stock <= 0:
        action = C

    else if repair_mode > 0:
        action = C
        repair_mode -= 1

    else:
        if f < 1/2:
            low_support_streak += 1
        else:
            low_support_streak = 0

        if low_support_streak >= 2 and stock / capacity < 1/2:
            action = D
            repair_mode = 2
            low_support_streak = 0
        else:
            action = C
```

Behavioral default:
- Start cooperative
- Mirror widespread cooperation with continued cooperation
- Use only rare, limited defection after repeated low support and depleted stock
- Return to cooperation immediately after any punitive response period
'''

description_PROSOCIAL_8 = '''
Initialize with cooperation.

For round t = 1:
- Play C.

For each round t > 1:
- Let q be the fraction of opponents who cooperated in round t−1.
- Let s be current stock / capacity.
- Let p be the fraction of opponents who cooperated in round t−2, if available.

Decision rule:
1. Play C if q ≥ 1/2.
2. Play C if q ∈ [1/3, 1/2) and s ≥ 1/2.
3. Play D only if q < 1/3 and either:
   - s < 1/2, or
   - q < 1/4 in two consecutive rounds.
4. After any round in which q ≥ 1/2, immediately return to C.
5. If the stock is at or near capacity, prefer C even after a weak round:
   - if s ≥ 3/4, play C unless q = 0.
6. If the stock is very low:
   - if s ≤ 1/4, play D for at most one round when q < 1/3; otherwise play C.

Last round:
- Play C.

Compact form:
```text
if t == 1 or t == r:
    C
else:
    q = opponents_coop_last_round / (n - 1)
    s = stock / capacity
    if q >= 1/2:
        C
    elif q >= 1/3 and s >= 1/2:
        C
    elif s >= 3/4 and q > 0:
        C
    elif q < 1/3 and s < 1/2 and (q_prev < 1/4 if t > 2 else True):
        D
    else:
        C
```

Use cooperation as the default response; defect only as a brief, targeted correction after clear overuse, and return to cooperation immediately once the group resumes restraint.
'''

description_PROSOCIAL_9 = '''
Start with cooperation and use a threshold-based contingent policy.

Let:
- `S_t` be the stock at the start of round `t`
- `c_t` be the number of opponents who cooperated in round `t-1`
- `m_t = n - 1` be the number of opponents
- `ρ_t = c_t / m_t` be the observed cooperation rate among opponents in the previous round

Decision rule for round `t`:

1. **Round 1**
   - Play `C`.

2. **Rounds 2 to r-1**
   - Compute the one-step stock pressure from the last round:
     - `pressure_t = 1 - S_t / capacity`
   - Play `C` if all of the following hold:
     - `ρ_t >= 1/2`
     - `S_t >= capacity / 2`
     - `pressure_t <= 1/2`
   - Otherwise play `D` for exactly one round, then revert to the rule above next round.

3. **Last round**
   - Play `C` if `S_t >= capacity / 2`
   - Otherwise play `D`

State update rule for your own memory:
- If the observed cooperation rate last round was at least `1/2` and stock remained at or above `capacity / 2`, remain in cooperative mode.
- If either condition fails, switch to protective mode for the next round only.

Additional edge-case handling:

- **If all opponents cooperated in the previous round** (`ρ_t = 1`), always cooperate unless `S_t < capacity / 2`, in which case defect for one round.
- **If no opponents cooperated in the previous round** (`ρ_t = 0`), defect for one round, then test cooperation again next round.
- **If stock is exactly `capacity / 2`**, treat it as cooperative enough and play `C` when `ρ_t >= 1/2`.
- **If stock is very low** (`S_t < capacity / 4`), defect until the stock recovers to at least `capacity / 2`.
- **If the game reaches a run of two consecutive rounds with `ρ_t >= 1/2` and `S_t >= capacity / 2`**, return immediately to cooperation and keep cooperating as long as both conditions continue to hold.

Pseudocode:

```text
if t == 1:
    action = C
else if t == r:
    action = C if S_t >= capacity/2 else D
else:
    if S_t < capacity/4:
        action = D
    else if rho_t >= 1/2 and S_t >= capacity/2:
        action = C
    else:
        action = D
```

Use the same rule symmetrically each round: cooperate whenever the group is sustaining the pool, and defect only as a brief protective response to repeated under-cooperation or stock decline.
'''

description_PROSOCIAL_10 = '''
Cooperate in every round.

Decision rule:
- Round 1: play C.
- Rounds 2 through r: play C, regardless of observed opponent actions, current stock, or past outcomes.
- Last round: play C.
- If the stock is at 0, still play C.

State/history handling:
- Track opponent cooperation counts only as context, not as a trigger for defection.
- Never switch to D.
- If opponents defect heavily, keep cooperating.
- If opponents cooperate consistently, keep cooperating.
- If the stock recovers to capacity, keep cooperating.

Implementation:
```text
for each round t:
    choose C
```

Prosocial posture:
- Always preserve the common pool as much as possible.
- Never escalate depletion in response to others.
- Maintain unconditional cooperation across the full horizon.
'''

description_PROSOCIAL_11 = '''
Let \(k_t\) be the number of opponents who cooperated in round \(t\), \(n\) the number of players, and \(S_t\) the stock at the start of round \(t\).

Maintain one internal variable:

- \(m_t\): a memory counter of consecutive rounds with insufficient cooperation, initialized to \(0\)

Define the cooperation threshold for round \(t\):

\[
q_t = \left\lceil \frac{n}{2} \right\rceil
\]

Decision rule in round \(t\):

1. **If \(t=1\):** play \(C\).
2. **If \(S_t \le \frac{n}{2}\):** play \(C\).
3. **If \(t=r\):** play \(C\) unless the stock is already critically low, in which case play \(C\) anyway.
4. **Otherwise:**
   - If \(k_{t-1} \ge q_{t-1}\), play \(C\) and reset \(m_t=0\).
   - If \(k_{t-1} < q_{t-1}\), increment \(m_t\leftarrow m_t+1\).
     - If \(m_t = 1\), still play \(C\).
     - If \(m_t \ge 2\), play \(D\) for one round, then reset \(m_t=0\).

Additional override rules:

- If the observed cooperation rate in the previous round is very high, \(k_{t-1} \ge n-1\), always play \(C\).
- If the stock after the previous round increased or stayed near capacity, play \(C\).
- After any round in which at least half of the opponents cooperated, immediately return to unconditional \(C\).

Equivalent pseudocode:

```text
Initialize m = 0

For each round t:
    if t == 1:
        action = C
    else if S_t <= n/2:
        action = C
    else if t == r:
        action = C
    else:
        if k_prev >= ceil(n/2):
            m = 0
            action = C
        else:
            m = m + 1
            if m == 1:
                action = C
            else:
                action = D
                m = 0
```

Edge cases:

- **First round:** cooperate.
- **Last round:** cooperate.
- **Very low stock:** cooperate to preserve recovery.
- **Isolated deviation by opponents:** forgive once.
- **Repeated low cooperation:** defect for exactly one round as a corrective signal, then return to cooperation immediately when cooperation recovers.
- **Sustained high cooperation:** remain cooperative throughout.
'''

description_PROSOCIAL_12 = '''
Play cooperatively by default, use the observed number of cooperating opponents to infer the group’s current conservation level, and only defect when the stock is already so depleted that further cooperation would not preserve the pool.

Decision rule each round t:

1. Compute the current cooperation rate among opponents from last round:
- Let k be the number of opponents who cooperated in round t−1.
- Let m = n−1.
- Let q = k / m.

2. Maintain an internal target cooperation threshold τ_t:
- Start with τ_1 = 1, so the first move is always C.
- Update after each round:
  - If stock increased or stayed near capacity after the previous round, raise τ_t slightly toward 1.
  - If stock fell sharply, lower τ_t only enough to avoid being exploited into collapse.
  - A simple update rule:
    - τ_{t+1} = clamp(τ_t + 0.1·(1−q) − 0.15·1[stock_t < 0.5·capacity], 0.5, 1)
  - This keeps the strategy strongly prosocial while allowing limited self-protection.

3. Choose action in round t:
- Cooperate if both of the following hold:
  - stock_t > capacity/4
  - q ≥ τ_t
- Defect otherwise.

Initial round:
- Play C.

Last rounds:
- If t is among the final two rounds, play C unless stock_t ≤ capacity/8.
- In the final round, play C whenever stock_t > 0; defect only if stock is already near collapse and cooperation would mostly reward noncooperators.

Edge cases:
- If all opponents cooperated in the previous round, set τ_{t+1} = 1.
- If no opponents cooperated in the previous round, set τ_{t+1} = max(0.5, τ_t − 0.15), then require stock_t > capacity/2 to cooperate.
- If stock_t is exactly 0, the action is irrelevant; default to C.
- If stock_t is at capacity, always cooperate.
- If observed opponent cooperation is missing for any reason, treat q as 1 and cooperate.

Behavioral principle:
- Start with trust.
- Reward sustained cooperation by staying cooperative.
- Respond to broad defection with a temporary defensive shift, but return to cooperation as soon as the pool recovers or opponents show renewed restraint.
- Never escalate to permanent defection; the default state is cooperation.
'''

description_PROSOCIAL_13 = '''
Cooperate in the first round.

After each round, compute:
- `k =` number of opponents who cooperated in the previous round
- `m = n - 1`
- `coop_rate = k / m`
- `last_stock =` stock level observed at the start of the current round
- `full_coop_count = number of consecutive previous rounds in which all opponents cooperated`
- `low_stock = last_stock <= capacity / 2`
- `critical_stock = last_stock <= capacity / 4`

Decision rule for round `t ≥ 2`:

1. **If all opponents cooperated last round, cooperate.**
   - Set `full_coop_count += 1`
   - Play `C`

2. **If at least 80% of opponents cooperated last round, cooperate unless stock is critically low.**
   - If `coop_rate >= 0.8` and not `critical_stock`, play `C`
   - If `coop_rate >= 0.8` and `critical_stock`, play `D` only for this round, then return to cooperation if cooperation recovers

3. **If cooperation was moderate, mirror the group with a bias toward generosity.**
   - If `0.5 <= coop_rate < 0.8`, play `C`

4. **If cooperation was low, use a recovery threshold before defecting.**
   - If `coop_rate < 0.5`:
     - Play `C` if `full_coop_count > 0` and `coop_rate >= 1 / 3`
     - Otherwise play `D`

5. **If stock is abundant, stay cooperative even after weak rounds.**
   - If `low_stock` is false, override any `D` above unless `coop_rate = 0`
   - In that case, play `C`

6. **If no opponent cooperated last round, respond with one round of restraint only if stock is dangerously low.**
   - If `k = 0`:
     - Play `D` only when `critical_stock`
     - Otherwise play `C`

7. **Last round: cooperate unless doing so would be clearly wasteful under universal defection.**
   - If `t = r`:
     - Play `C` if `coop_rate > 0`
     - Play `D` only if `k = 0` and `critical_stock`

State update after each round:
- If all opponents cooperated, increment `full_coop_count`
- Otherwise reset `full_coop_count = 0`

Compact pseudocode:

```text
if t == 1:
    play C
else:
    if k == m:
        full_coop_count += 1
        play C
    else:
        full_coop_count = 0
        if t == r:
            play C if k > 0 else (D if critical_stock else C)
        else if coop_rate >= 0.8:
            play D if critical_stock else C
        else if coop_rate >= 0.5:
            play C
        else if coop_rate >= 1/3 and full_coop_count > 0:
            play C
        else if k == 0:
            play D if critical_stock else C
        else:
            play C if not low_stock else D
```

If the group shows sustained cooperation, remain cooperative throughout. If cooperation weakens, keep cooperating until defection becomes widespread or the stock is critically low, and then use a single restrained response before returning to cooperation as soon as cooperation resumes.
'''

description_PROSOCIAL_14 = '''
Play cooperative by default, and use a state-based threshold rule that rewards high cooperation, protects the stock when cooperation collapses, and slowly rebuilds trust after shortfalls.

Decision rule each round `t` with current stock `S_t`, remaining rounds `m = r - t + 1`, and observed opponent cooperation count `k_t` from the previous round:

1. **Round 1**
   - Play `C`.

2. **Compute observed cooperation rate**
   - `q_t = k_t / (n - 1)` if `t > 1`
   - For round 1, treat `q_t = 1`

3. **Set a cooperation threshold**
   - `θ_t = clamp(0.5 + 0.25 * (1 - S_t / capacity) + 0.25 * (1 - q_t), 0.35, 0.90)`
   - `clamp(x, a, b)` means `min(max(x, a), b)`

4. **Default action**
   - Play `C` if both conditions hold:
     - `q_t >= θ_t`
     - `S_t > 0`
   - Otherwise play `D`

5. **Stock-protection override**
   - If `S_t <= capacity / (4n)`, play `C` only if `q_t = 1`; otherwise play `D`
   - If `S_t <= capacity / (8n)`, play `D`

6. **Endgame rule**
   - If `m = 1`, play `C` if `q_t >= 1/2`; otherwise play `D`
   - If `m = 2`, play `C` only if `q_t = 1` and `S_t >= capacity / 3`; otherwise play `D`

7. **Recovery rule after a low-cooperation round**
   - If `q_t < 1/2`, require two consecutive rounds of `q >= 1/2` before returning to unconditional `C`
   - Until that condition is met, keep using the threshold rule above

8. **Sustained cooperation mode**
   - If `q_t = 1` for two consecutive rounds and `S_t >= capacity / 2`, play `C` unconditionally until either:
     - observed cooperation drops below `1`, or
     - stock falls below `capacity / 2`

9. **Fallback**
   - If any state information is missing or inconsistent, play `C` on the first such occurrence; after that, use the default rule with the last valid observations

This strategy stays cooperative when the group is cooperating, becomes stricter when observed cooperation or stock quality falls, and avoids irreversible depletion by tightening only when the common pool weakens.
'''

description_PROSOCIAL_15 = '''
Round 1: cooperate.

After each round t ≥ 1, let c_t be the number of opponents who cooperated in round t, and let
p_t = c_t / (n - 1)
be the observed opponent cooperation rate.

Maintain:
- `avg3`: weighted average of the last up to 3 observed cooperation rates, with weights 0.5, 0.3, 0.2 from most recent to older
- `low_streak`: number of consecutive rounds with `avg3 < 2/3`
- `recovery_streak`: number of consecutive rounds with `avg3 ≥ 2/3`

Decision for round t + 1:

1. Compute the current stock share indicator:
   - `stock_high` if `stock ≥ 0.75 * capacity`
   - `stock_medium` if `0.40 * capacity ≤ stock < 0.75 * capacity`
   - `stock_low` if `stock < 0.40 * capacity`

2. Choose action:
   - Cooperate if `stock_high`
   - Cooperate if `avg3 ≥ 2/3`
   - Cooperate if `low_streak = 1`
   - Defect only if all of the following hold:
     - `stock_low`
     - `avg3 < 2/3`
     - `low_streak ≥ 2`

3. Forgiveness rule:
   - If you defected in the previous round, return to cooperation immediately once `avg3 ≥ 2/3` or `stock ≥ 0.40 * capacity`

4. Endgame:
   - In the final round, cooperate unless `stock_low` and `low_streak ≥ 2`; otherwise cooperate unconditionally

Equivalent compact pseudocode:

```text
if t == 1:
    play C
else:
    avg3 = weighted_average(last 3 p-values, weights = 0.5, 0.3, 0.2)
    if stock >= 0.75*capacity:
        play C
    elif avg3 >= 2/3:
        play C
    elif stock < 0.40*capacity and avg3 < 2/3 and low_streak >= 2:
        play D
    else:
        play C
```

Update `low_streak` after each round:
- increment it when `avg3 < 2/3`
- reset it to 0 otherwise

This keeps cooperation as the default, tolerates brief lapses, and uses a single, limited defection only after sustained low cooperation combined with a depleted stock.
'''

description_PROSOCIAL_16 = '''
Round 1: cooperate.

For every later round t:

- Let `S` be the current stock.
- Let `x` be the number of opponents who cooperated in round `t-1`.
- Let `m = n - 1` be the number of opponents.
- Let `q = x / m` be the observed cooperation rate among opponents.

Decision rule:

1. If `t = r`, cooperate.
2. Else if `S >= capacity / 3`, cooperate.
3. Else if `S < capacity / 6` and `q <= 1/3`, defect.
4. Else if `S < capacity / 3` and `q < 2/3`, defect for this round only.
5. Otherwise, cooperate.

Memory update:

- Continue using the latest observed `x` each round.
- If a round is played with no prior observation available, treat `q = 1` and cooperate.

Behavioral interpretation:

- Stay fully cooperative whenever the stock is healthy.
- When the stock is depleted, keep cooperating as long as most others are still cooperating.
- Defect only as a temporary conservation response to sustained low cooperation and low stock.
- Return to cooperation immediately once either the stock recovers above `capacity / 3` or opponent cooperation rises to at least `2/3`.
'''

description_PROSOCIAL_17 = '''
Use a two-mode rule with a cooperative default and a short protective pause only when cooperation has clearly broken down.

State tracked:
- `bad_streak`: number of consecutive prior rounds with fewer than half of opponents cooperating
- `mode ∈ {open, guarded}`, initially `open`

Decision rule in round `t`:

1. **First round**
   - Play `C`.

2. **Update after round `t-1`**
   - Let `m` be the number of cooperating opponents you observed last round.
   - Define a “good support” round as `m >= ceil((n-1)/2)`.
   - If good support: set `bad_streak = 0`, `mode = open`.
   - Otherwise: increment `bad_streak` by 1.
   - If `bad_streak >= 2` and current stock is below `capacity / 3`, set `mode = guarded`.
   - If `m >= ceil((n-1)/2)`, immediately return to `open`.

3. **Action choice**
   - If `t = r`:
     - Play `C`.
   - Else if `mode = open`:
     - Play `C`.
   - Else if `mode = guarded`:
     - Play `D` for one round only.
     - After that round, return to `open` unless the next observed support is again below half.

4. **Recovery rule**
   - As soon as you observe at least half of opponents cooperating in any round, play `C` from the next round onward.
   - Never stay in `guarded` for more than one round without re-evaluating from the latest observation.

5. **Edge cases**
   - If `n = 2`, “at least half of opponents” means the single opponent cooperated.
   - If stock is `0`, play `C`.
   - If you lack a previous observation because the game has just started, treat it as a good-support state and cooperate.
'''

description_PROSOCIAL_18 = '''
Round 1: play C.

For every later round t, let:
- S be the current stock before acting
- k be the number of opponents who cooperated in the previous round
- m = n - 1 be the number of opponents
- ρ = k / m be the observed cooperation rate among opponents last round

Define two thresholds:
- high_trust = 1 - 2 / n
- low_trust = 1 / 2

Decision rule:

1. If S is at or below 2n, play C.
2. Else if ρ ≥ high_trust, play C.
3. Else if ρ ≤ low_trust, play D for this round.
4. Else play C.

Additional edge rules:
- In the final round, play C if S > 0.
- If the previous round had full or near-full cooperation from opponents, stay with C for all subsequent rounds unless the stock has fallen to the point that immediate restraint is needed to avoid collapse.
- If a low-cooperation round occurs, respond with D only until opponents return to cooperation above the high_trust threshold, then immediately return to C.

Equivalent pseudocode:

```
if t == 1:
    action = C
else:
    if S <= 2*n:
        action = C
    else:
        rho = k / (n - 1)
        if rho >= 1 - 2/n:
            action = C
        elif rho <= 1/2:
            action = D
        else:
            action = C

if t == r and S > 0:
    action = C
```

Behavioral principle:
- Default to cooperation.
- Defect only as a short, corrective response to clear and repeated under-cooperation by others.
- Return to cooperation immediately once the group shows sustained restraint.
- Never start with defection, and never keep defecting after cooperation has recovered.
'''

description_PROSOCIAL_19 = '''
Play cooperate by default, and use a simple restore-and-protect rule:

**State variables to track**
- `k_t`: number of opponents who cooperated in round `t`
- `low_count`: consecutive rounds in which cooperation among opponents has been too low to sustain the stock
- `recovery`: consecutive rounds after a cooperation shortfall in which opponents have met the cooperation threshold again

**Round 1**
- Play `C`.

**Decision rule for round t > 1**
1. Let `S` be the current stock.
2. Compute the minimum cooperation level needed to keep the stock from collapsing under full-consumption pressure:
   - If at least `n-1` opponents cooperated in the previous round, play `C`.
   - If fewer than `n-1` opponents cooperated in the previous round, play `D` for one round only, then reassess.
3. Override with stock protection:
   - If `S` is already very low, play `D` to avoid contributing to collapse only when the previous round showed broad defection.
   - If `S` is moderate or high, prefer `C` unless the previous round had clear widespread defection.

**Operational rule**
- If `k_{t-1} = n-1`, play `C`.
- If `k_{t-1} < n-1`, play `D` only this round.
- After any `D`, return to `C` immediately once `k_{t-1} = n-1` again.

**Last round**
- Play `C` if the previous round had at least `n-1` cooperating opponents.
- Otherwise play `D`.

**Long-run adjustment**
- If cooperation among opponents has been stable for several rounds, remain on `C` regardless of short-term noise.
- If there are repeated shortfalls, alternate into brief defensive `D` rounds only until cooperation recovers, then resume `C` immediately.

**Fallback when history is ambiguous**
- When the previous round’s observation is unavailable or unusable, play `C` unless the stock is near depletion and recent rounds showed persistent defection, in which case play `D` for that round.

**Compact pseudocode**
```text
if t == 1:
    play C
else:
    if k_{t-1} >= n-1:
        play C
    else:
        play D
```

**Interpretation**
- Start cooperative.
- Reward near-universal cooperation with immediate cooperation.
- Answer broad defection with only a single defensive defection.
- Forgive as soon as cooperation returns.
- Never escalate beyond what is needed to protect the shared resource.
'''

description_PROSOCIAL_20 = '''
Always cooperate.

Decision rule:
- In every round, choose C.
- Ignore opponent cooperation counts for action selection; use them only to confirm that cooperation is not being reciprocated, not to alter your move.
- If the current stock is 0, choose C as the default no-cost action.

Edge cases:
- First round: C.
- Intermediate rounds: C.
- Last round: C.
- If you are ever indifferent because the stock is exhausted or the round is otherwise degenerate: C.

Operational form:
```text
for each round t:
    play C
```
'''

description_PROSOCIAL_21 = '''
Round 1: play C.

Every later round: play C, regardless of the observed number of opponent cooperators, current stock, or remaining rounds.

Edge cases:
- If stock is 0, still play C.
- If stock is at capacity, play C.
- If all observed opponents defected in the previous round, play C.
- If all observed opponents cooperated in the previous round, play C.
- In the final round, play C.
- If any state information is missing or ambiguous, default to C.

Optional implementation form:

```text
for each round t:
    action = C
```
'''

description_PROSOCIAL_22 = '''
Use a cooperative default with a short, memory-based defense trigger.

Let:

- `q_t` = number of opponents who cooperated in round `t`
- `m = ceil((n - 1) / 2)` = majority threshold among opponents
- `H = 3 * capacity / 4`
- `L = capacity / 2`

Decision rule for round `t` with current stock `S_t`:

1. **Round 1:** play `C`.

2. **Always cooperate in recovery mode:**
   - If `S_t <= L`, play `C`.

3. **Cooperate when the recent environment is sufficiently cooperative:**
   - If `t > 1` and `q_{t-1} >= m`, play `C`.

4. **Grace period after one weak round:**
   - If `t > 2`,
   - and `q_{t-1} < m`,
   - but `q_{t-2} >= m`,
   - and `S_t >= H`,
   - play `C`.

5. **Defensive brake:**
   - If `t > 2`,
   - and `q_{t-1} < m`,
   - and `q_{t-2} < m`,
   - and `S_t > L`,
   - play `D`.

6. **Otherwise:** play `C`.

Edge handling:

- If only one past round exists, use only `q_{t-1}`.
- If the stock is at or below `L`, never defect.
- If the game is in its final rounds, keep using the same rule; no special endgame defection.
- After any round in which opponents return to at least majority cooperation, immediately return to `C`.

State update for your own memory:

- Track the last two values of `q_t`.
- Track whether the previous round was cooperative or defensive only for applying the grace-period rule.
'''

description_PROSOCIAL_23 = '''
Round 1: play C.

For round t > 1, let:

- `h1` = number of opponents who cooperated in the most recent round
- `h3` = average number of cooperating opponents over the last up to 3 rounds
- `p1 = h1 / (n - 1)`
- `p3 = h3 / (n - 1)`
- `s = stock / capacity`

Decision rule:

1. Play C if `t = r`.
2. Play C if `s <= 0.25`.
3. Play C if `p1 >= 0.5`.
4. Play C if `p3 >= 0.5`.
5. Play C if the last round’s stock did not fall relative to the round before it.
6. Otherwise, play D for one round.

Return to C immediately as soon as any of the following is true:
- the most recent round has `p1 >= 0.5`, or
- `s <= 0.25`, or
- the average cooperation over the last 3 rounds is at least `0.5`.

Edge handling:

- If fewer than 3 past rounds exist, compute `p3` using all available past rounds.
- If there is no previous stock comparison yet, skip rule 5.
- If the stock is already very low, always choose C.
- If opponents alternate between cooperation and defection, keep choosing C unless the low-cooperation pattern persists for multiple rounds and the stock is not already low.

Behavioral pattern:

- Start cooperative.
- Stay cooperative whenever cooperation is at or above a majority level.
- Use a brief defensive D only after persistent low cooperation and only when the stock is still healthy enough to absorb it.
- Never let retaliation become prolonged.
'''

description_PROSOCIAL_24 = '''
Use a state-dependent cooperative threshold strategy.

Maintain:
- `c_t`: number of opponents who cooperated in round `t`
- `m_t = c_t / (n - 1)`: observed opponent cooperation rate
- `S_t`: current stock at start of round `t`
- `\bar m_t`: exponentially weighted average of opponent cooperation rates, updated as  
  `\bar m_t = 0.7 * \bar m_{t-1} + 0.3 * m_t` after round 1, with `\bar m_1 = m_1`

Decision rule in round `t`:

1. Compute the current cooperation threshold
   `T_t = 0.5 + 0.35 * (S_t / capacity - 0.5) + 0.25 * (\bar m_t - 0.5)`

2. Cooperate if both conditions hold:
   - `S_t >= capacity / 4`
   - `\bar m_t >= 0.4`
   
   otherwise defect only if one of these conditions holds:
   - `S_t < capacity / 8`
   - `\bar m_t < 0.2` for two consecutive rounds

3. If neither forced-cooperate nor forced-defect condition applies, play:
   - `C` if `m_{t-1} >= T_t` or, in round 1, if `capacity >= 4n`
   - `D` otherwise

Round-specific rules:

- Round 1:
  - Play `C` unless `capacity < 4n`, in which case play `D`
  - If `capacity` is very high relative to `n`, begin cooperatively to preserve the stock

- Middle rounds:
  - Keep cooperating as long as the recent cooperation rate stays at or above the adaptive threshold
  - If cooperation is weak but the stock is still healthy, keep cooperating for one extra round before switching
  - If cooperation collapses or the stock becomes scarce, defect until cooperation recovers

- Final round:
  - Play `C` if `m_{r-1} >= 0.5` or `S_r >= capacity / 2`
  - Otherwise play `D`
  - If the last observed round was broadly cooperative, finish cooperatively; if not, protect against endgame free-riding

State update after each round:
- Record `c_t`
- Update `m_t`
- Update `\bar m_t`
- Track whether `m_t < 0.2` occurred in two consecutive rounds

Additional fallback rule:
- If `S_t == 0`, play `D`
- If `S_t == capacity`, play `C`
- If all observed opponents cooperated in the previous round, play `C` next round
- If no opponent cooperated in the previous round, play `D` next round

This strategy starts cooperative, rewards sustained cooperation, tolerates brief deviations, and responds quickly to persistent defection or severe stock depletion.
'''

description_PROSOCIAL_25 = '''
Play a conditional conservation policy with a built-in restoration phase and a final-round cleanup rule.

**State variables tracked**
- `t`: current round
- `S`: current stock at the start of round `t`
- `c_prev`: number of opponents who cooperated in round `t-1`
- `p_prev = c_prev / (n-1)`: observed opponent cooperation rate in the previous round
- `m`: rolling mean of observed opponent cooperation rates over recent rounds, initialized to 1

**Round 1**
- Play `C`.

**Core rule for rounds 2 to r-1**
1. Compute the sustainable stock target:
   - `T = capacity / 2`
2. Compute a cooperation floor from observed opponent behavior:
   - `q = max(0, 2m - 1)`
3. Choose:
   - Play `C` if `S >= T` and `p_prev >= q`
   - Otherwise play `D`

**Interpretation of the decision rule**
- `C` is the default when stock is healthy and opponents are not collapsing cooperation.
- `D` is triggered only when the resource is below the restoration threshold or observed cooperation is too low to justify restraint.

**Observation update after each round**
- After round `t`, set:
  - `p_t = (# of opponents who cooperated in round t) / (n-1)`
  - Update rolling mean:
    - `m <- (m * min(t-1, k-1) + p_t) / min(t, k)`
  - Use a short memory window `k = min(5, r-1)`; if fewer than `k` rounds have been played, average over all observed rounds so far.

**Restoration phase**
- If `S < T` at the start of your turn, play `D` until either:
  - `S >= T`, or
  - you reach the final two rounds.
- If all opponents cooperated in the previous round and `S` is rising, return to `C` immediately once `S >= T`.

**Final two rounds**
- Round `r-1`:
  - Play `C` only if both:
    - `S >= T`
    - `p_prev = 1`
  - Otherwise play `D`
- Round `r`:
  - Play `C` if `S >= T`
  - Otherwise play `D`

**Edge cases**
- If `n = 2`, treat the lone opponent’s cooperation as the observed rate.
- If `S = 0`, play `D`.
- If `S = capacity`, play `C` unless the final two-round rule applies.
- If opponents’ cooperation has never fallen below full cooperation and `S` remains at or above `T`, continue playing `C` every round.

**Behavior summary**
- Start cooperatively.
- Keep cooperating while the stock remains healthy and opponents remain broadly cooperative.
- Switch to restraint only when the resource falls below the restoration threshold or opponent behavior indicates sustained overuse.
- In the final rounds, protect the remaining stock unless the pool is clearly healthy.
'''

description_PROSOCIAL_26 = '''
At every round, play C.

Decision rule:
- Round 1: C
- Rounds 2 through r − 1: C
- Round r: C

State/history handling:
- Record the observed number of cooperating opponents each round.
- Use the information only to track how cooperative the group is, not to change your action.
- If the stock is high, low, recovering, or collapsing, still play C.

Edge cases:
- If stock is at 0, play C.
- If stock is at capacity, play C.
- If all opponents defected in the previous round, play C.
- If all opponents cooperated in the previous round, play C.
- If cooperation levels fluctuate sharply across rounds, play C.

Pseudocode:
```text
for t in 1..r:
    action = C
```
'''

description_PROSOCIAL_27 = '''
Round 1: play C.

Every later round: play C.

Keep playing C regardless of:
- the number of opponents who cooperated last round,
- the current stock level,
- how many rounds remain,
- whether you were exploited in earlier rounds,
- whether the stock is near depletion or near capacity.

If the stock is 0, still play C.

Internal bookkeeping can track the observed cooperation rate, but it never changes the action.
'''

description_PROSOCIAL_28 = '''
Play C in every round, regardless of history, observed opponent behavior, or current stock.

Decision rule:
- Round 1: C.
- Rounds 2 through r: C.
- If you have any internal tie-breaker or fallback logic, resolve it in favor of C.

Edge cases:
- If stock is 0, choose C.
- If stock is at capacity, choose C.
- If you observe unanimous defection by opponents in prior rounds, choose C.
- If you observe unanimous cooperation by opponents in prior rounds, choose C.
- In the final round, choose C.
- If the game state is inconsistent or unavailable, choose C.

State dependence:
- Use the observed history only as a check on whether the resource is under stress; never let it change the action away from C.
- Do not punish, mirror, or retaliate.

Prosocial posture:
- Maintain maximal restraint at all times.
- Treat the common stock as a shared asset to be preserved, not exploited.
'''

description_PROSOCIAL_29 = '''
State variables:
- `opp_coop[t]`: number of opponents who cooperated in round `t`
- `opp_rate[t] = opp_coop[t] / (n - 1)`
- `support = ceil((n - 1) / 2)`
- `high_stock = 0.60 * capacity`
- `low_stock = 0.35 * capacity`
- `critical_stock = 0.15 * capacity`

Decision rule each round `t`:

1. If `t = 1`, play `C`.

2. If `t = r`, play `C`.

3. If `stock >= high_stock`, play `C`.

4. If `stock >= low_stock` and the previous round had at least `support` cooperating opponents, play `C`.

5. If `stock < low_stock`:
   - play `C` unless both of the following hold:
     - the last 2 rounds each had fewer than `support` cooperating opponents, and
     - `stock <= critical_stock`
   - only in that case, play `D` for one round

5. After any round in which you played `D`, return to `C` in the next round unless the same emergency condition still holds.

History update rule:
- After each round, record `opp_coop[t]`.
- Treat missing history at the start as “no exploitation observed.”

Behavioral pattern:
- Default to cooperation.
- Use opponent cooperation as a stability signal, not as punishment.
- Never start with defection.
- Never use sustained retaliation.
- Use at most isolated defensive defections under severe depletion and repeated noncooperation.
- Resume cooperation immediately once stock is no longer critical or opponent cooperation recovers.
'''

description_PROSOCIAL_30 = '''
Initialize trust to 1.

For round 1, play C.

For every later round t:

1. Set `coop_rate` to the fraction of opponents who cooperated in round `t-1`.
2. Update a smoothed trust score:
   `trust = 0.7 * trust + 0.3 * coop_rate`

Decision rule:

- Play C if any of the following holds:
  - `t` is one of the last two rounds
  - `stock <= capacity / 3`
  - `trust >= 1/2`
  - the last round had at least half of the opponents cooperating

- Play D only if all of the following hold:
  - `t` is not one of the last two rounds
  - `stock > capacity / 3`
  - `trust < 1/2`
  - the last two rounds both had fewer than half of the opponents cooperating

Reset rule:

- The moment a round is observed with at least half of the opponents cooperating, return to C and keep playing C until the conditions for D are again satisfied for two consecutive rounds.

Edge handling:

- If the first observed round is unavailable for any reason, default to C.
- If the stock is at or near the minimum feasible level, play C.
- If the stock is at capacity, play C unless the two-round low-cooperation trigger has already activated.

Pseudocode:

```text
if t == 1:
    play C
    trust = 1
else:
    coop_rate = opponents_cooperated_last_round / (n - 1)
    trust = 0.7 * trust + 0.3 * coop_rate

    if t >= r - 1:
        play C
    else if stock <= capacity / 3:
        play C
    else if coop_rate >= 1/2:
        play C
    else if trust >= 1/2:
        play C
    else if coop_rate_last_round < 1/2 and coop_rate_two_rounds_ago < 1/2:
        play D
    else:
        play C
```
'''

description_PROSOCIAL_31 = '''
Play cooperatively by default, and use the observed number of cooperating opponents to set a minimum acceptable cooperation level for the next round.

Let:
- `k_t` = number of opponents who cooperated in round `t`
- `m = n - 1` = number of opponents
- `τ_t` = cooperation threshold for round `t`

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Normal rounds `t > 1`**
   - Compute the rolling cooperation rate over the last `L` rounds, with `L = min(3, t-1)`:
     - `avg = average of k_{t-1}, k_{t-2}, ..., k_{t-L}`
   - Set the threshold:
     - `τ_t = ceil(0.75 * m)`
   - Cooperate if both conditions hold:
     - `k_{t-1} >= τ_t`
     - `stock_t >= capacity / 4`
   - Otherwise defect.

3. **Recovery rule**
   - If the previous round had strong cooperation, defined as:
     - `k_{t-1} >= m - 1`
   - then cooperate next round even if the stock is low, unless `stock_t = 0`.

4. **Retaliation floor**
   - If the previous round had weak cooperation, defined as:
     - `k_{t-1} <= floor(m / 2)`
   - then play `D` for the next round.
   - Stay on `D` until a round occurs in which:
     - `k_{t-1} >= τ_t`
   - Then return to `C`.

5. **Last round**
   - If `t = r`, play `C` unless the previous round had very low cooperation:
     - `k_{r-1} <= floor(m / 2)`
   - In that case play `D`.

State-sensitive adjustment:

- If `stock_t <= capacity / 8`, play `D` unless `k_{t-1} = m`.
- If `stock_t >= capacity / 2` and `k_{t-1} >= ceil(2m/3)`, play `C`.

Summary behavior:
- Start cooperative.
- Reward broad cooperation with continued cooperation.
- Respond to sustained low cooperation with temporary defection.
- Return to cooperation immediately after opponents restore cooperation.
- Prefer preserving the pool when stock is low, but never abandon cooperation after a single bad round.
'''

description_PROSOCIAL_32 = '''
Cooperate in round 1.

For every later round, compute:
- `k =` number of opponents who cooperated in the previous round
- `m = n - 1`
- `coop_rate = k / m`
- `S =` current stock before choosing your action

Use this rule:

1. **Immediate restoration mode**
   - If `coop_rate = 1`, cooperate.
   - If `S >= 0.9 * capacity`, cooperate.

2. **Baseline prosocial mode**
   - Cooperate if `coop_rate >= 0.5`.

3. **Conditional restraint**
   - If `0.25 <= coop_rate < 0.5`, cooperate only if `S >= 0.6 * capacity`; otherwise defect.

4. **Punishment-for-depletion mode**
   - If `coop_rate < 0.25`, defect.

5. **Last-round rule**
   - Cooperate in the final round only if `coop_rate >= 0.5` in the previous round.
   - Otherwise defect.

6. **Recovery after a bad round**
   - After any round in which `coop_rate < 0.5`, return to cooperation immediately once `coop_rate >= 0.5` again.
   - Do not carry punishment across multiple rounds once cooperation recovers.

7. **Stock-collapse edge case**
   - If `S <= 0`, defect.
   - If `S` is very low but positive (`S < 0.1 * capacity`) and `coop_rate < 0.5`, defect.
   - If `S < 0.1 * capacity` and `coop_rate >= 0.5`, cooperate to help rebuild.

Equivalent pseudocode:

```text
if round == 1:
    play C
else:
    coop_rate = opponents_cooperated_last_round / (n - 1)

    if stock <= 0:
        play D
    else if round == r:
        if coop_rate >= 0.5:
            play C
        else:
            play D
    else if coop_rate == 1 or stock >= 0.9 * capacity:
        play C
    else if coop_rate >= 0.5:
        play C
    else if coop_rate >= 0.25 and stock >= 0.6 * capacity:
        play C
    else:
        play D
```

This strategy always starts cooperatively, keeps cooperating when the group is broadly cooperative, reduces cooperation only after clear evidence of exploitation, and returns to cooperation as soon as the group does.
'''

description_ALTRUISTIC_5 = '''
Initialize with cooperation.

For each round t, observe current stock S and the number of opponents who cooperated last round, m_prev.

Define:
- k_prev = m_prev + 1 if you cooperated last round, otherwise m_prev
- c_prev = k_prev / n, the observed cooperation rate last round
- c_target = 0.75, the minimum cooperation rate you aim to sustain
- S_safe = capacity / 2, the stock level you treat as healthy
- S_crit = capacity / 4, the stock level you treat as fragile

Decision rule:

1. First round:
   - Play C.

2. Standard rule:
   - Play C if both of the following hold:
     - S ≥ S_crit
     - c_prev ≥ c_target
   - Otherwise play D.

3. Stock-protection override:
   - If S < S_crit, play D unless c_prev = 1 and S is rising from the previous round.
   - If S ≤ 2n, play C only when c_prev = 1; otherwise play D.

4. Repair mode after collapse:
   - If the previous round had cooperation rate below 1/2, enter repair mode for the next two rounds:
     - Play C if S ≥ S_crit
     - Play D only if S < S_crit
   - After those two rounds, return to the standard rule.

5. Endgame rule:
   - In the last round, play C whenever S > 0.
   - If S = 0, the action is irrelevant.

6. Tie-breaking and missing-information rule:
   - When the last-round observation is ambiguous for any reason, assume the most cooperative interpretation and play C.

Behavioral principle:
- Default to cooperation.
- Defect only when the pool is visibly deteriorating or when recent cooperation has dropped enough that continued unilateral cooperation would accelerate depletion.
- Return to cooperation immediately once the observed cooperation rate recovers.
'''

description_ALTRUISTIC_6 = '''
**Strategy: Stock-Guardian Reciprocity**

Maintain two internal variables:

- `coop_rate`: estimated fraction of opponents cooperating in the previous round
- `trust`: a score in `[0, 1]` representing how safely the group is sustaining the pool

Initialize:

- `trust = 1`
- `coop_rate = 1`

For round `t` with current stock `S`:

### 1) First round
Play `C`.

### 2) Update after each round
After observing `k` cooperating opponents out of `n-1`:

- `coop_rate = k / (n - 1)` if `n > 2`
- For `n = 2`, set `coop_rate = 1` if the other player cooperated, else `0`

Update trust by smoothing the observation:

- `trust = 0.7 * trust + 0.3 * coop_rate`

Also update a stock-safety indicator:

- `safe_stock = S / capacity`

### 3) Decision rule for rounds 2 through r-1
Play `C` if all of the following hold:

- `trust ≥ 0.5`
- `safe_stock ≥ 0.25`
- the previous round did not show near-universal defection by others

Near-universal defection means:

- `coop_rate ≤ 0.25` when `n > 3`
- `coop_rate = 0` when `n ≤ 3`

Otherwise play `D`.

### 4) Forgiveness rule
If the previous round was bad but not catastrophic, cooperate once more to allow recovery:

- If `coop_rate` is between `0.25` and `0.5`, and
- `safe_stock ≥ 0.4`

then play `C` even if `trust` is slightly below the usual threshold.

Apply this forgiveness only once after a drop in cooperation; if the next round is again below the cooperation threshold, switch to `D` until cooperation recovers.

### 5) Collapse protection
Play `D` immediately if either condition holds:

- `safe_stock < 0.15`
- `coop_rate = 0` in the previous round

Remain with `D` until both:

- `coop_rate ≥ 0.5`, and
- `safe_stock ≥ 0.25`

### 6) Final round
Always play `C` unless the pool is already in collapse protection:

- If `safe_stock < 0.15`, play `D`
- Otherwise play `C`

### 7) Compact pseudocode

```text
if t == 1:
    action = C
else:
    observe k = # cooperating opponents in round t-1
    coop_rate = k / (n - 1)
    trust = 0.7 * trust + 0.3 * coop_rate
    safe_stock = S / capacity

    if safe_stock < 0.15 or coop_rate == 0:
        action = D
    else if t == r:
        action = C
    else if trust >= 0.5 and safe_stock >= 0.25 and not near_universal_defection:
        action = C
    else if 0.25 <= coop_rate < 0.5 and safe_stock >= 0.4:
        action = C
    else:
        action = D
```

### 8) Behavioral profile
- Start with full cooperation
- Reward sustained cooperation with continued cooperation
- Continue cooperating through mild setbacks to support recovery
- Defect only when the group is clearly overusing the pool or the stock is close to collapse
- End by cooperating whenever the pool remains viable
'''

description_ALTRUISTIC_7 = '''
Play cooperation by default, and treat defection as a last-resort stabilizer only when the stock trajectory becomes dangerously depleted.

Let:

- `S` = current stock at the start of the round
- `k` = number of opponents who cooperated in the previous round
- `m = n - 1` = number of opponents
- `c_prev = k / m` = observed opponent cooperation rate in the previous round

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Main rule for round t > 1**
   - Compute the cooperative threshold:
     - `T(S) = 0.5 + 0.5 * min(1, S / capacity)`
   - Cooperate if both conditions hold:
     - `S >= capacity / 4`
     - `c_prev >= T(S) - 0.1`
   - Otherwise defect.

Interpretation of the threshold:
- When stock is high, require only a mildly cooperative environment.
- When stock is lower, require a clearly cooperative environment before matching with `C`.
- The `0.1` margin prevents overreacting to small fluctuations.

3. **Late-game rule**
   - If `t` is among the last 2 rounds, play `C` unless:
     - `S < capacity / 6` and `c_prev < 1/3`
   - In that case, play `D`.

4. **Severe depletion override**
   - If `S <= capacity / 8`, play `D` unless the previous round had full cooperation by opponents:
     - if `c_prev = 1`, play `C`
     - otherwise play `D`

5. **Recovery rule after exploitation**
   - If the previous round had `c_prev = 0` and `S < capacity / 2`, play `D` for one round.
   - After that single defensive round, return to the main rule.

6. **Default behavior**
   - In all other cases, play `C`.

Pseudocode:

```text
if t == 1:
    action = C
else:
    c_prev = cooperators_last_round / (n - 1)

    if t >= r - 1:
        if S < capacity / 6 and c_prev < 1/3:
            action = D
        else:
            action = C

    elif S <= capacity / 8:
        if c_prev == 1:
            action = C
        else:
            action = D

    elif c_prev == 0 and S < capacity / 2:
        action = D

    else:
        T = 0.5 + 0.5 * min(1, S / capacity)
        if S >= capacity / 4 and c_prev >= T - 0.1:
            action = C
        else:
            action = D
```

This strategy begins with unconditional cooperation, prefers cooperation whenever the stock and observed group behavior support it, and uses defection only to prevent collapse or repeated exploitation.
'''

description_ALTRUISTIC_8 = '''
Round 1: cooperate.

For round t > 1, let:
- S be the current stock at the start of the round
- k be the number of opponents who cooperated in the previous round
- m = n - 1 be the number of opponents
- x = k / m be the observed opponent cooperation rate in the previous round
- s = S / capacity be the current stock ratio

Use this rule:

1. If S ≤ 2n, defect.
2. Else if t = r, cooperate if x ≥ 1/2; otherwise defect.
3. Else if x ≥ 2/3, cooperate.
4. Else if x ≥ 1/3 and s ≥ 1/2, cooperate.
5. Otherwise, defect.

Adjustment for recent history:
- Keep a cooperation score h updated each round:
  - h ← 0.7h + 0.3x
- Replace x above with h after round 2:
  - Use h instead of the raw previous-round cooperation rate in steps 2–5.

Stabilizing rule:
- If the stock has increased from the previous round, cooperate unless S ≤ 2n.
- If the stock has fallen for two consecutive rounds, defect once, then return to the rule above.

Edge cases:
- If n = 2, interpret x as the single opponent’s action in the previous round.
- If all opponents cooperated in the previous round, always cooperate unless S ≤ 2n.
- If no opponent cooperated in the previous round, defect until at least one of the last two rounds showed cooperation by a majority of opponents.
- In the final two rounds, cooperate only when the observed cooperation rate has been at least 1/2 over the last two rounds and S > 2n.

Operational form:

Initialize:
- h ← 1

Each round t:
- If t = 1: play C
- Else:
  - Observe k
  - h ← 0.7h + 0.3(k / (n - 1))
  - If S ≤ 2n: play D
  - Else if t = r: play C iff h ≥ 1/2, else D
  - Else if stock rose last round: play C
  - Else if stock fell two rounds in a row: play D
  - Else if h ≥ 2/3: play C
  - Else if h ≥ 1/3 and S ≥ capacity / 2: play C
  - Else: play D

Behavioral intent:
- Start maximally cooperative.
- Continue cooperating when the group is broadly cooperative.
- Reduce cooperation only when the group’s behavior or the stock trajectory signals clear overuse.
- Restore cooperation immediately after any improvement in collective restraint.
'''

description_ALTRUISTIC_9 = '''
Play Cooperate by default, and switch to Defect only as a temporary conservation response when the stock is clearly being overused.

Decision rule for round t with current stock S_t and observed number of cooperative opponents k_t-1 from the previous round:

1. First round:
   - Play C.

2. Compute the previous-round cooperation rate among opponents:
   - c̄ = k_t-1 / (n - 1)  for t > 1

3. Set a conservation threshold based on stock:
   - Let low = capacity / 2
   - Let critical = capacity / 4
   - Let recover = 3 * capacity / 5

4. Action rule:
   - If S_t <= critical: play C
   - Else if S_t < low and c̄ < 1/2: play D
   - Else if S_t < recover and c̄ < 1/3: play D
   - Else play C

5. Forgiveness rule:
   - If the stock rises from the previous round or stays above low for two consecutive rounds, return to C immediately.
   - If the previous round had at least half of opponents cooperating, play C regardless of stock unless S_t is already critical.

6. Last round:
   - Play C unless S_t is critical and the previous round showed near-total defection by opponents.
   - If t = r and S_t > 0, prefer C.

7. Long-run reset:
   - After any D, require only one cooperative round from opponents to return to C.
   - Never stay in D for two consecutive rounds unless both:
     - S_t < low, and
     - opponent cooperation in the previous round was below 1/3.

8. Empty-history edge case:
   - If no prior round exists, cooperate.
   - If the opponent-cooperation count is unavailable for any reason, cooperate unless the stock is already below critical.

Pseudocode:

if t == 1:
    action = C
else:
    cbar = coop_opponents_last_round / (n - 1)
    if S_t <= capacity / 4:
        action = C
    elif S_t < capacity / 2 and cbar < 0.5:
        action = D
    elif S_t < 3 * capacity / 5 and cbar < 1/3:
        action = D
    else:
        action = C

if t == r and S_t > 0:
    action = C

if previous_round_stock <= S_t:
    action = C if S_t > capacity / 4 else action

If your own prior action was D, immediately revert to C as soon as either the stock recovers above capacity / 2 or the last-round cooperation rate reaches at least 1/2.
'''

description_ALTRUISTIC_10 = '''
Play C in every round, regardless of history, stock level, or opponents’ behavior.

Decision rule:
- If a move is required, choose C.
- Never choose D.

Edge cases:
- First round: choose C.
- Last round: choose C.
- If stock is very low or zero: choose C.
- If opponents mostly defected in prior rounds: choose C.
- If opponents mostly cooperated in prior rounds: choose C.
- If the stock has fully recovered to capacity: choose C.

State use:
- Use the observed history only to track that the strategy remains committed to cooperation; do not change the action based on it.

Altruistic posture:
- Preserve the common pool by minimizing extraction at every opportunity and refusing to free-ride under any circumstance.
'''

description_ALTRUISTIC_11 = '''
Play **C** by default.

Let `k_t` be the number of opponents who cooperated in round `t`, and let `p_t = k_t / (n-1)` be the observed cooperation rate among opponents in the previous round.

Define:
- `S_t` = stock at start of round `t`
- `S* = capacity / 2`
- `buffer = capacity / 10`
- `low = capacity / 4`

Decision rule for round `t`:

1. **Round 1**
   - Play `C`.

2. **If current stock is high**
   - If `S_t >= S*`, play `C`.

3. **If current stock is moderate**
   - If `low <= S_t < S*`, play `C` unless the previous round showed very low cooperation:
     - If `t > 1` and `p_{t-1} < 1/3`, play `D`.
     - Otherwise play `C`.

4. **If current stock is low**
   - If `S_t < low`, play `D` only if cooperation collapsed recently:
     - If `t > 1` and `p_{t-1} = 0`, play `D`.
     - Otherwise play `C`.

5. **Endgame protection**
   - In the final round `t = r`, play `C` unless the stock is critically low:
     - If `S_t < buffer` and `p_{t-1} = 0`, play `D`.
     - Otherwise play `C`.

6. **Recovery mode after defection by others**
   - If the previous round had at least half the opponents cooperating, always return to `C` immediately.
   - If opponents’ cooperation improves after any period of low cooperation, keep playing `C` for at least two consecutive rounds before reconsidering `D`.

Memory update:
- After each round, record `p_t`.
- Treat the most recent round with `p_t >= 1/2` as a signal to sustain cooperation.
- Treat two consecutive rounds with `p_t = 0` as a signal that the pool is being stripped, and allow a single defensive `D` in the next round if the stock is also low.

This strategy is:
- **generous**: it cooperates whenever there is any reasonable chance of sustaining the pool,
- **forgiving**: it immediately returns to cooperation when others do,
- **protective**: it defects only when low stock and repeated full defection make continued cooperation clearly unsafe,
- **stable**: it avoids reacting to isolated deviations.
'''

description_ALTRUISTIC_12 = '''
Play cooperatively by default. Treat the pool as a shared asset to be preserved, and only defect when the observed behavior makes continued cooperation materially unsustainable.

Decision rule by round:

- Round 1: Cooperate.
- Rounds 2 to r - 1:
  - Let k be the number of opponents who cooperated in the previous round.
  - Let f = (n - 1 - k) / (n - 1), the fraction of opponents who defected.
  - Let S be the current stock before choosing.
  - Cooperate if both conditions hold:
    1. The pool is still healthy: S ≥ capacity / 3
    2. Defection pressure is not high: f ≤ 1 / 3
  - Defect if either condition fails.

- Last round:
  - Cooperate if S > 0 and at least half of the opponents cooperated in the previous round.
  - Otherwise defect.

Escalation and forgiveness rule:

- Track a trust score T starting at 0.
- Each round update:
  - If at least (n - 1) / 2 opponents cooperated, set T = max(T - 1, 0)
  - Otherwise set T = T + 1
- Cooperate whenever T ≤ 1.
- Defect whenever T ≥ 2, and keep defecting until a round occurs in which at least two-thirds of opponents cooperate; then reset T = 0 and return to cooperating.

State-sensitive override:

- If S < capacity / 4, cooperate only if at least two-thirds of opponents cooperated in the previous round.
- If S = 0, cooperate.
- If the previous round was fully cooperative among opponents, cooperate regardless of T.

Compact pseudocode:

```text
if round == 1:
    action = C
else:
    k = opponents_cooperated_last_round
    f = (n - 1 - k) / (n - 1)
    if round == r:
        if S > 0 and k >= ceil((n - 1) / 2):
            action = C
        else:
            action = D
    else if S < capacity / 4:
        action = C if k >= ceil(2 * (n - 1) / 3) else D
    else if T <= 1 and f <= 1/3:
        action = C
    else:
        action = D
```

Behavioral pattern:

- Start by signaling full cooperation.
- Keep cooperating while the pool remains healthy and most others are cooperating.
- Respond to sustained defection with temporary restraint by defecting.
- Return to cooperation as soon as the group shows renewed restraint.
- End cooperatively whenever the pool still has value and the group has not sharply deteriorated.
'''

description_ALTRUISTIC_13 = '''
Use a stock-preserving baseline with emergency restraint:

**State variables**
- `t`: current round, starting at 1
- `S`: current stock at start of round `t`
- `k`: number of opponents who cooperated in the previous round
- `q = k / (n - 1)`: observed opponent cooperation rate in the previous round  
  - for `t = 1`, set `q = 1`

**Decision rule**

1. **If `t = 1`, play `C`.**

2. **If `S <= n`, play `C`.**  
   This is the emergency conservation rule: when stock is low, always choose the lower-consumption action.

3. **If `t = r`, play `C` if `q >= 0.5`, otherwise play `D`.**  
   On the final round, remain cooperative only if at least half of the opponents were cooperative in the previous round.

4. **Otherwise, use a cooperation threshold that tightens as the stock falls:**
   - Define the cooperation threshold
     \[
     \tau(S) = \min\left(1,\; \max\left(0.5,\; 1 - \frac{S}{2\,capacity}\right)\right)
     \]
   - Play `C` if `q >= τ(S)`, else play `D`.

**Interpretation of the rule**
- High stock: cooperate unless opponent cooperation is clearly poor.
- Medium stock: cooperate when a majority of opponents cooperated last round.
- Low stock: cooperate even with weaker opponent cooperation, because preserving stock takes priority.

**Edge-case handling**
- If `n = 2`, then `q` is just the single opponent’s last-round action indicator.
- If all opponents defected in the previous round, defect only when the stock is still comfortably high; otherwise cooperate.
- If all opponents cooperated in the previous round, always cooperate.
- If the stock ever becomes very small, never defect.
- If the observed cooperation rate is exactly on the threshold, choose `C`.

**Compact pseudocode**
```text
if t == 1:
    action = C
else if S <= n:
    action = C
else if t == r:
    action = C if q >= 0.5 else D
else:
    tau = min(1, max(0.5, 1 - S / (2 * capacity)))
    action = C if q >= tau else D
```
'''

description_ALTRUISTIC_14 = '''
Play C by default.

Maintain a cooperation target for the number of expected cooperators, starting at n. Let k_t be the number of opponents observed to cooperate in round t.

Decision rule:

- Round 1: play C.
- Round t > 1:
  - Compute the current stock fraction s = stock / capacity.
  - If stock is very low, play C unless almost everyone is defecting:
    - If s ≤ 1/4 and k_{t-1} ≥ n - 2, play C.
    - If s ≤ 1/4 and k_{t-1} < n - 2, play C only if you cooperated in the previous round and at least half of opponents cooperated; otherwise play D for one round to prevent immediate collapse.
  - If stock is moderate or high, play C.
  - Play D only when both conditions hold:
    - the last round had clear widespread defection among opponents, and
    - your own cooperation has not been met with at least partial reciprocity for two consecutive rounds.

Operationally:
- Define “clear widespread defection” as k_{t-1} ≤ ⌊(n-1)/2⌋.
- Define “partial reciprocity” as k_{t-1} ≥ ⌈(n-1)/2⌉.
- Keep a forgiveness counter f:
  - Initialize f = 2.
  - If k_{t-1} ≥ ⌈(n-1)/2⌉, reset f = 2 and play C.
  - If k_{t-1} < ⌈(n-1)/2⌉, decrease f by 1.
  - Play D only if f reaches 0; otherwise play C.
  - After any round in which k_{t-1} ≥ ⌈(n-1)/2⌉, return immediately to C.

Endgame handling:
- Never switch to unconditional defection in the final rounds.
- In the last two rounds, play C unless the stock has fallen to a near-collapse level and almost all opponents are defecting.
- If stock is at zero, play C.
- If stock is at capacity, play C.

State-sensitive override:
- If stock ≥ 3/4 capacity, always play C.
- If stock is between 1/2 capacity and 3/4 capacity, play C unless the previous two rounds both had clear widespread defection.
- If stock is between 1/4 capacity and 1/2 capacity, require at least partial reciprocity from the previous round to keep playing C.
- If stock < 1/4 capacity, alternate only one corrective D at most, then return to C as soon as any meaningful cooperation reappears.

Altruistic core principle:
- Treat cooperation as the default and defection as a brief corrective signal, never as a persistent stance.
- Prefer absorbing short-run losses to preserve the stock for future rounds.
- Resume cooperation immediately after any sign that the group is sustaining the resource.
'''

description_ALTRUISTIC_15 = '''
Round 1: play C.

Every later round:
- Play C if stock > 0.
- Play C if stock = 0.

If you want the rule as pseudocode:

```text
if stock <= 0:
    choose C
else:
    choose C
```

Behavioral interpretation:
- Never exploit the common pool.
- Never condition cooperation on how many opponents cooperated.
- Use opponent history only as a diagnostic signal: if cooperation by others is falling and stock is declining, keep cooperating anyway to maximize preservation and leave recovery room for the group.
- If any tie-breaking is needed, always break ties toward C.

Terminal-round handling:
- In the last round, play C.
- If the stock is already depleted or near-depleted, still play C.

State-based override:
- No override ever triggers D; the strategy is unconditional cooperation across all states and histories.
'''

description_ALTRUISTIC_16 = '''
Initialize `mode = steady_cooperation`.

For every round `t`:

1. **Choose `C` unconditionally.**
   - Do this in the first round.
   - Do this in every middle round.
   - Do this in the last round.
   - Do this even if prior rounds show low cooperation.
   - Do this even if the stock is falling quickly.
   - Do this even if the stock is at zero.

2. **Update only your internal assessment of the state.**
   - Record:
     - current stock `S_t`
     - number of opponent cooperators in the previous round
     - any trend in stock decline or recovery
   - Use this information only to track how strained the resource is, not to change the action away from `C`.

3. **Emergency state handling.**
   - If the stock becomes critically low, remain on `C`.
   - If the stock collapses to zero, remain on `C` as the default action.
   - If opponents become highly uncooperative, remain on `C`; do not retaliate.

Pseudocode:

```text
for each round t:
    observe current stock S_t
    if t > 1:
        observe count of opponent cooperators in round t-1

    play C
```

This strategy is purely conservation-oriented: it never extracts more than the cooperative amount, never punishes, and never escalates depletion.
'''

description_ALTRUISTIC_17 = '''
Choose C in every round.

Decision rule:
- Round 1: play C.
- Round t > 1: play C, regardless of:
  - current stock
  - how many opponents cooperated last round
  - how many rounds remain
  - whether the stock is rising or falling

Edge cases:
- If stock is 0, play C.
- If stock is at capacity, play C.
- In the last round, play C.
- If all observed opponents defected in the previous round, still play C.
- If all observed opponents cooperated in the previous round, play C.

Implementation:
```text
for each round t:
    action = C
```

Altruistic principle:
- Always take the smaller share to minimize pressure on the shared resource and avoid accelerating depletion.
- Never switch to D in response to short-term exploitation, because D extracts more from the pool and harms every player’s future access.
'''

description_ALTRUISTIC_18 = '''
Play C in every round.

Decision rule:
- Round 1: cooperate.
- Rounds 2 through r−1: cooperate regardless of observed opponent behavior, stock level, or past outcomes.
- Round r: cooperate.

Edge cases:
- If the observed stock is 0, still choose C.
- If every opponent defects, still choose C.
- If many opponents cooperate, still choose C.
- If the history shows prolonged depletion, continue choosing C.

State use:
- Keep track of the stock and the number of opposing cooperators only as information for the game state, not as a trigger to defect.
- Use the observed cooperation count to monitor whether the group is sustaining the resource, but do not change your action.

Altruistic principle:
- Never take the higher-consumption action.
- Always minimize your own extraction and preserve as much stock as possible for the group and future rounds.
'''

description_ALTRUISTIC_19 = '''
Play cooperatively by default, and defect only as a defensive reset when the group has repeatedly overdrawn the pool or when stock is already near collapse.

Decision rule:

- Let `c_t` be the number of opponents who cooperated in round `t-1`.
- Let `m_t = n - 1 - c_t` be the number of opponents who defected in round `t-1`.
- Let `S_t` be the stock at the start of round `t`.
- Let `p_t = c_t / (n - 1)` be the observed cooperation rate among opponents in the previous round.

Maintain two internal counters:
- `trust` = consecutive rounds since the last clear overuse.
- `strain` = consecutive rounds with low cooperation or falling stock.

Initialize:
- `trust = 1`
- `strain = 0`

Round 1:
- Play `C`.

Each later round `t > 1`:

1. Compute a sustainability floor:
   - `floor_t = max(2n, 0.4 * capacity)`
   - `warning_t = max(2n, 0.55 * capacity)`

2. Defect only under one of these conditions:
   - `S_t <= floor_t`, or
   - `p_t < 1/2` for two consecutive rounds, or
   - the previous round caused a large stock drop and cooperation was weak:
     - if `S_{t-1} - S_t >= 0.25 * S_{t-1}` and `p_t <= 2/3`

3. Otherwise cooperate.

Internal updates after observing round `t-1`:
- If `p_t >= 2/3` and `S_t >= warning_t`:
  - `trust = trust + 1`
  - `strain = max(strain - 1, 0)`
- If `p_t < 2/3`:
  - `strain = strain + 1`
  - `trust = 0`
- If `p_t = 1`:
  - `trust = trust + 2`
  - `strain = max(strain - 1, 0)`

Escalation and recovery:
- After any round in which you defect, return to cooperation immediately in the next round if:
  - `S_t > warning_t`, and
  - `p_t >= 2/3`
- If you defect because of low stock, resume cooperation as soon as `S_t > warning_t`.
- If opponents cooperate fully for two consecutive rounds, cooperate unconditionally afterward unless `S_t <= floor_t`.

Last round:
- Cooperate unless `S_t <= floor_t`.
- If the final round is reached and the stock is healthy, never defect.

Very early rounds:
- Round 1: cooperate.
- Round 2: cooperate unless round 1 was already near-collapse (`S_2 <= floor_2` after the first update) or the previous round showed clear overuse (`p_2 < 1/2`).

Operating principle:
- Match cooperation quickly.
- Punish repeated overuse briefly with a defensive defect.
- Forgive immediately once the group returns to sustainable behavior.
- Preserve the pool whenever stock is healthy, even if others are partially uncooperative.
'''

description_ALTRUISTIC_20 = '''
Play cooperatively by default, and use defection only as a short, restorative response when the pool is being overused.

Decision rule

- Round 1:
  - Play C.

- For round t > 1, let h be the number of opponents who cooperated in round t−1, and let p = h / (n−1).

- Compute the prior-round cooperation level:
  - If p ≥ 2/3: play C.
  - If 1/3 ≤ p < 2/3: play C unless the stock has fallen sharply, in which case play D once.
  - If p < 1/3: play D for one round, then return to C as soon as cooperation recovers.

Stock-sensitive adjustment

- If the current stock is high relative to capacity, stay cooperative:
  - If stock ≥ capacity / 2: play C whenever p ≥ 1/3.
- If the current stock is low, protect the resource:
  - If stock < capacity / 4: play D unless p = 1, in which case play C.
- If the current stock is near collapse:
  - If stock ≤ capacity / (2n): play D.

Forgiveness and reset

- After any round in which you defect, immediately return to C in the next round unless both conditions hold:
  - fewer than half of opponents cooperated in the previous round, and
  - the stock is not recovering.
- If cooperation among opponents improves for two consecutive rounds, reset fully to C and remain cooperative.

Endgame

- In the final round, play C if the stock is above capacity / 4.
- In the final round, play D only if the stock is critically low:
  - stock ≤ capacity / (2n), or
  - no more than one opponent cooperated in the previous round.

Summary policy

- Default: C.
- Punishment: at most one-round D in response to widespread defection or dangerously low stock.
- Recovery: immediate return to C once opponents show meaningful cooperation or the stock stabilizes.
- Never chain defections unless the stock is collapsing.
'''

description_ALTRUISTIC_21 = '''
Round 1: play C.

For each later round t, let:
- S be the current stock at the start of the round
- k be the number of opponents who cooperated in the previous round
- m = n - 1 be the number of opponents

Define the recent cooperation rate:
- q = k / m

Define the stock pressure threshold:
- τ = 1 / 2

Decision rule:
1. Play C if S ≥ τ · capacity and q ≥ 1/2.
2. Play C if S ≥ τ · capacity and q < 1/2, but the previous round had q_prev ≥ 2/3.
3. Play D only if S < τ · capacity and q < 1/2 for two consecutive rounds.

Equivalently, use this update logic:

- If stock is healthy, stay cooperative unless opponent cooperation has been low for two rounds in a row.
- If stock is strained, keep cooperating if at least half of opponents cooperated last round.
- If stock is strained and cooperation has been persistently low, defect until either:
  - q rises to at least 1/2, or
  - stock returns to at least τ · capacity.

Special cases:
- If n = 2, replace “at least half” with “the other player cooperated.”
- If the previous round is unavailable, treat q_prev = 1.
- In the final round, play C unless both:
  - S < τ · capacity, and
  - q < 1/2 in the previous round.

Full behavior summary:
- Start with unconditional cooperation.
- Reward any broad cooperation by continuing to cooperate.
- Punish sustained low cooperation only when stock is already under pressure.
- Return to cooperation immediately when the group restores cooperation or the stock recovers.

Pseudocode:
```text
if t == 1:
    action = C
else:
    q = cooperators_last_round / (n - 1)
    if t == r:
        if S < capacity/2 and q < 1/2:
            action = D
        else:
            action = C
    else:
        if S >= capacity/2:
            action = C
        else:
            if q >= 1/2:
                action = C
            else if q_prev >= 2/3:
                action = C
            else if q_prev < 1/2:
                action = D
            else:
                action = C
```

When the stock is extremely low:
- If S ≤ capacity / 4, play C only if q ≥ 2/3; otherwise play D.

When the stock is extremely high:
- If S ≥ 3 · capacity / 4, play C regardless of q.

When cooperation is mixed:
- Prefer C unless the group has shown repeated unwillingness to cooperate and the stock is already deteriorating.

This strategy stays maximally cooperative by default, reacts only to persistent noncooperation, and resumes cooperation as soon as the group shows any meaningful recovery.
'''

description_ALTRUISTIC_22 = '''
Play C in every round.

Decision rule:
- If the round exists, cooperate.
- Ignore opponent counts for action selection; use them only to track how well the group is preserving the resource.
- Never switch to D.
- If the stock is 0, choose C by default.
- If the stock is near capacity, choose C.
- If the stock is low, choose C.
- On the first round, choose C.
- On the last round, choose C.

State handling:
- Maintain the full history of observed cooperation counts, but do not let any history condition trigger defection.
- If you want a running summary for internal monitoring, compute the observed cooperation rate of opponents each round and note whether the pool is recovering or shrinking, but still choose C regardless.
- If any implementation detail requires a fallback action, the fallback is C.
'''

description_ALTRUISTIC_23 = '''
Play C by default, and use D only as a conservation response when the pool is being overused.

Decision rule for round t with current stock S and observed number of opponent cooperators k among the n-1 opponents in the previous round:

1. First round:
   - Play C.

2. Last round:
   - Play C.

3. If the current stock is very low:
   - Let low threshold L = capacity / 4.
   - If S ≤ L, play C if k ≥ ceil((n-1)/2), otherwise play D.

4. If the current stock is moderate:
   - Let target cooperation among opponents be q = (n-1)/2.
   - If k ≥ q, play C.
   - If k < q, play D only if S < capacity / 2; otherwise play C.

5. If the current stock is high:
   - If S > capacity / 2, play C unless the previous round had severe overuse:
     - severe overuse means k ≤ floor((n-1)/3)
     - in that case, play D for one round.

6. Recovery rule:
   - If the previous round’s stock increased, or stayed within 5% of capacity, play C.
   - If the previous round’s stock fell by more than 15% of capacity, and k was below half of opponents, play D once, then return to C unless another drop occurs.

7. Endgame smoothing:
   - In the final two rounds, always play C.
   - In the final three to five rounds, play C unless the stock is already below capacity / 3 and fewer than half of opponents cooperated in the previous round; in that case, play D for at most one round before reverting to C.

Operational pseudocode:

```text
if t == 1:
    action = C

else if t >= r-1:
    action = C

else:
    if S <= capacity/4:
        if k >= ceil((n-1)/2):
            action = C
        else:
            action = D

    else if S <= capacity/2:
        if k >= ceil((n-1)/2):
            action = C
        else:
            action = D

    else:
        if k <= floor((n-1)/3) and previous_stock_drop > 0.15*capacity:
            action = D
        else:
            action = C

    if previous_stock >= 0.95*capacity:
        action = C

    if previous_stock_increased:
        action = C
```

Tie and edge handling:
- If a threshold uses a non-integer value, round up for cooperation thresholds and round down for defect thresholds.
- If information from the previous round is unavailable, treat it as neutral and default to C.
- If stock is exactly on a threshold, use the more cooperative option.
- After any D choice, require at least one subsequent round of C unless the next observation again shows severe overuse.
'''

description_ALTRUISTIC_24 = '''
Round 1: play C.

For every later round t = 2, ..., r:
- Observe current stock S_t and the number of opponents who cooperated in round t - 1, c_{t-1}.
- Play C.

If you want the rule in compact form:

```
if t == 1:
    action = C
else:
    action = C
```

Edge handling:
- If the stock is at or near 0, still play C.
- If the stock is at capacity, still play C.
- In the final round, still play C.
- If all opponents defected in the previous round, still play C.
- If all opponents cooperated in the previous round, still play C.

Behavioral interpretation:
- Treat the common pool as a shared asset to preserve, not a resource to race for.
- Never punish, never exploit, never condition cooperation on others’ restraint.
- Use every round to maintain the resource and leave the highest possible stock for the group.
'''

description_ALTRUISTIC_25 = '''
Always cooperate.

Decision rule:
- Round 1: play C.
- Every subsequent round: play C, regardless of the observed cooperation count, current stock, or past outcomes.

State use:
- Track the stock and the history only to observe the game’s trajectory, not to change your action.

Edge cases:
- If stock is very low, still play C.
- If every opponent defected in the previous round, still play C.
- If every opponent cooperated in the previous round, still play C.
- In the last round, play C.

Pseudocode:
```text
for each round t:
    action = C
```
'''

description_ALTRUISTIC_26 = '''
Use a conservation-first rule with forgiveness and escalation only when stock is endangered.

Maintain:
- `S`: current stock at the start of the round
- `c_prev`: number of opponents who cooperated in the previous round
- `q_prev = c_prev / (n-1)`: observed cooperation rate among opponents
- `m`: consecutive rounds in which the stock has fallen by at least 25% from the previous round
- `L`: consecutive rounds in which observed opponent cooperation has been below `1/2`

Decision rule for round `t`:

1. If `t = 1`, play `C`.

2. If `t = r`:
   - play `C` if `S ≥ capacity / 2`
   - otherwise play `D`

3. Otherwise, let
   - `S_safe = capacity / 2`
   - `S_warning = capacity / 3`

   Play `C` if all of the following hold:
   - `S ≥ S_warning`
   - `q_prev ≥ 1/2`
   - `m < 2`

   Play `D` if any of the following hold:
   - `S < S_warning`
   - `q_prev < 1/2` for `2` consecutive rounds
   - `m ≥ 2`

4. Intermediate recovery rule:
   - If `S < S_safe` but `S ≥ S_warning`, play `C` only if `q_prev ≥ 2/3`
   - Otherwise play `D`

State update after each round:
- If `S_t` is the stock before the round and `S_{t+1}` is the stock after the round:
  - if `S_{t+1} ≤ 0.75 * S_t`, increment `m` by 1; otherwise reset `m = 0`
- If `q_prev < 1/2`, increment `L`; otherwise reset `L = 0`

Edge cases:
- If `n = 2`, replace the thresholds above with:
  - `q_prev ≥ 1` for unconditional cooperation
  - `q_prev = 1/2` for recovery cooperation when `S ≥ S_safe`
- If the stock is at its maximum and opponent cooperation has been stable for the last two rounds, continue cooperating regardless of the exact value of `q_prev` as long as `q_prev ≥ 1/2`
- If the stock ever falls to `0`, play `C` in the next round only if `q_prev = 1`; otherwise play `D` until `S > 0`

Tie-breaking:
- When a condition is exactly on the threshold, choose `C` unless the rule explicitly requires `>` rather than `≥`

Behavior summary in policy form:
- Start cooperative.
- Keep cooperating while the stock is healthy and at least half of opponents are cooperating.
- Continue cooperating through mild short-term drops.
- Switch to defection only when the stock becomes strained or opponent cooperation remains persistently low.
- Return to cooperation immediately once the stock recovers and opponents resume cooperative behavior.
'''

description_ALTRUISTIC_27 = '''
Cooperate in every round.

Decision rule:
- If the current stock is positive, play C.
- If the current stock is zero or effectively zero, play C.
- Never play D.

Edge cases:
- First round: play C.
- Last round: play C.
- After any history of opponent behavior, keep playing C.
- If the observed number of cooperating opponents is 0, 1, ..., or n−1, still play C.
- If floating-point rounding produces a tiny negative stock, treat it as 0 and play C.

Pseudocode:
```text
strategy(history, stock, round, r, n, capacity):
    return C
```

Behavioral principle:
- Preserve the common resource whenever possible.
- Do not respond to defection with defection.
- Maintain steady restraint across all rounds, regardless of opponent mix or prior depletion.
'''

description_ALTRUISTIC_28 = '''
Play C in every round.

Decision rule:
- If the round exists, choose C.
- Ignore opponent behavior, previous cooperation counts, and current stock level when selecting the action.
- Never choose D.

Edge cases:
- First round: choose C.
- Last round: choose C.
- If the stock is already very low or zero: choose C.
- If every observed opponent defected in prior rounds: choose C.
- If every observed opponent cooperated in prior rounds: choose C.

State dependence:
- Use history only to track that nothing should change this rule; it does not alter the action.

Pseudocode:
```text
for each round t:
    action = C
```
'''

description_ALTRUISTIC_29 = '''
Play C in every round.

Decision rule:
- Round 1: cooperate.
- Rounds 2 through r: cooperate.
- If the current stock is 0: cooperate.
- If the current stock is at capacity: cooperate.
- If every opponent cooperated in the previous round: cooperate.
- If some or all opponents defected in the previous round: cooperate.
- If the final round is reached: cooperate.

State use:
- Track the observed number of cooperating opponents each round for monitoring only; never use it to switch away from C.
- No punishment, no retaliation, no conditional defection.

Behavioral principle:
- Preserve the common pool at all times by taking the least extractive action available.
'''

description_ALTRUISTIC_30 = '''
Play `C` by default, and use `D` only as a restraint signal when the stock is being pushed into collapse.

Decision rule for round `t` with current stock `S_t` and observed opponent cooperation count `k_{t-1}` from the previous round:

1. `t = 1`
- Play `C`.

2. `t > 1`
- Compute the previous round’s cooperation rate among opponents:
  `q = k_{t-1} / (n - 1)`

- Define the cooperative baseline threshold:
  `q_good = 1 - 1/n`

- Define the collapse threshold:
  `q_bad = 1/2`

- Play `C` if both of the following hold:
  - `S_t >= capacity / 2`
  - `q >= q_good`

- Otherwise, if either of the following holds, play `D`:
  - `S_t < capacity / 4`
  - `q <= q_bad`

- In the intermediate region, play `C` if the stock is recovering or stable:
  - `S_t >= S_{t-1}`
  - otherwise play `D`

Recovery rule after a defection response:
- After playing `D` once, return to `C` immediately in the next round if:
  - `S_t >= capacity / 2`
  - and `q > q_bad`

Late-game rule:
- In the final round, play `C` unless the stock is already below `capacity / 4`; if it is below that level, play `D`.

Adaptive reset rule:
- If the observed cooperation count reaches `n - 1` in any round, play `C` in the next round regardless of previous history.
- If two consecutive rounds show `q <= q_bad`, play `D` until at least one round satisfies `q >= q_good`.

Equivalent pseudocode:

```text
if t == 1:
    action = C
else:
    q = k_prev / (n - 1)

    if t == r:
        action = C if S_t >= capacity/4 else D
    else if S_t < capacity/4:
        action = D
    else if S_t >= capacity/2 and q >= 1 - 1/n:
        action = C
    else if q <= 1/2:
        action = D
    else if S_t >= S_prev:
        action = C
    else:
        action = D

    if k_prev == n - 1:
        action = C
```

Behavioral pattern:
- Start fully cooperative.
- Continue cooperating when most others cooperate and the stock remains healthy.
- Temporarily defect only to protect the resource after clear overuse.
- Return to cooperation as soon as the group shows restraint or the stock rebounds.
'''

description_ALTRUISTIC_31 = '''
Play **C** in every round.

Decision rule:
- If the round is any round from 1 to r, choose **C**.
- Do not condition on the number of opponents who cooperated, previous stock levels, or previous outcomes.
- Never choose **D**.

Edge cases:
- **First round:** choose **C**.
- **Last round:** choose **C**.
- **If stock is 0:** choose **C**.
- **If stock is at capacity:** choose **C**.
- **If every observed opponent defects:** choose **C**.
- **If some or all opponents cooperate:** choose **C**.

Implementation:
```text
for each round t = 1..r:
    action = C
```
'''

description_ALTRUISTIC_32 = '''
Always choose C.

Decision rule:
- Round 1: play C.
- Every intermediate round: play C, regardless of the observed number of opponent cooperators, the current stock level, or your past payoffs.
- Final round: play C.

Edge cases:
- If stock is 0, play C.
- If stock is at capacity, play C.
- If all opponents defected in the previous round, play C.
- If all opponents cooperated in the previous round, play C.
- If the game is nearing the end and the stock is high or low, play C.

History use:
- Track the observed cooperation count only to record the state of the group, not to change your action.
- Never punish, never conditionally defect, and never mirror opponent behavior.

Altruistic mindset:
- Treat each round as an opportunity to minimize extraction from the common pool.
- Default to the least depleting action in every state.
- Maintain the same cooperative choice under every observed pattern of opponent behavior.
'''

description_BENEVOLENT_5 = '''
- Let `coop_opponents[t]` be the number of opponents who cooperated in round `t`.
- Let `low_stock = capacity / 3`.
- Let `critical_stock = capacity / 5`.
- Let `sustained_defection = coop_opponents[t-1] <= floor((n-1)/2)` for the last two rounds.

Decision rule:

1. **Round 1:** play `C`.

2. **Every later round `t` before the last:**
   - Play `C` unless all three conditions hold:
     - current stock `S_t <= low_stock`,
     - opponents have shown sustained defection in the last two rounds,
     - and at least one of the last two rounds had `coop_opponents <= floor((n-1)/3)`.
   - If all three conditions hold, play `D` for that round only.

3. **Last round:** always play `C`.

Adjustment rules:

- If `S_t <= critical_stock`, play `C` regardless of history.
- If the opponents cooperated with at least `n-2` players in the previous round, play `C` next round.
- After any round in which you play `D`, return to `C` immediately in the next round unless the three defection conditions still hold.

Memory summary:

- Track only:
  - current stock,
  - opponent cooperation count from the last two rounds,
  - whether you played `D` in the previous round.

Behavioral pattern:

- Start cooperative.
- Stay cooperative under mixed or decent cooperation.
- Use a single-round defensive defect only after repeated broad defection and only when stock is already stressed.
- Never carry defection forward once cooperation reappears or stock recovers.
'''

description_BENEVOLENT_6 = '''
**State variables tracked**
- `S_t`: stock at start of round `t`
- `k_t`: number of opponents who cooperated in round `t`  
- `m_t = n - 1`: number of opponents
- `q_t = k_t / m_t`: observed opponent cooperation rate in round `t`
- `q̄_t`: exponentially weighted cooperation score, initialized to `1`

Update after each round `t`:
- `q̄_{t+1} = 0.7 q̄_t + 0.3 q_t`
- Clamp `q̄_t` to `[0,1]`

**Decision rule for round `t`**
1. **First round**
   - Play `C`

2. **Last round**
   - Play `C`

3. **If stock is near collapse**
   - If `S_t < 0.25 × capacity`, play `C`

4. **If stock is abundant**
   - If `S_t ≥ 0.75 × capacity`, play `C`

5. **Main adaptive rule**
   - Compute expected opponent cooperation level from recent history: `q̄_t`
   - Cooperate if both conditions hold:
     - `q̄_t ≥ 0.45`
     - `S_t ≥ capacity × (0.35 + 0.30 × q̄_t)`
   - Otherwise defect

**Round-by-round response to observed behavior**
- If the previous round had at least `ceil(0.6 × m_t)` cooperating opponents, then in the next round:
  - set `q̄_t = min(1, q̄_t + 0.10)`
- If the previous round had at most `floor(0.2 × m_t)` cooperating opponents, then in the next round:
  - set `q̄_t = max(0, q̄_t - 0.20)`

**Escalation and recovery**
- Maintain a variable `strike_t`, initialized to `0`
- After each round:
  - if `q_t < 0.25`, increment `strike_t` by `1`
  - otherwise reset `strike_t = 0`
- If `strike_t ≥ 2`, defect for the next round unless either:
  - `S_t < 0.25 × capacity`, or
  - `t = r`
- Once a round occurs with `q_t ≥ 0.5`, immediately reset `strike_t = 0`

**Final-third rule**
- For rounds `t > 2r/3`:
  - play `C` if `q̄_t ≥ 0.5` and `S_t ≥ 0.3 × capacity`
  - otherwise play `D`, except always play `C` in the last round

**Exact tie handling**
- If a threshold comparison is exactly equal, choose `C`
- If the state is exactly on a boundary, use the more cooperative branch

**Compact pseudocode**
```text
initialize qbar = 1
initialize strike = 0

for each round t = 1..r:
    observe S_t

    if t == 1 or t == r:
        action = C
    else if S_t < 0.25 * capacity:
        action = C
    else if S_t >= 0.75 * capacity:
        action = C
    else if t > 2*r/3:
        if qbar >= 0.5 and S_t >= 0.3 * capacity:
            action = C
        else:
            action = D
    else:
        if qbar >= 0.45 and S_t >= capacity * (0.35 + 0.30 * qbar):
            action = C
        else:
            action = D

    play action

    observe k_t = number of opponents who played C
    q_t = k_t / (n - 1)

    if q_t >= 0.5:
        strike = 0
    else if q_t < 0.25:
        strike = strike + 1
    else:
        strike = max(0, strike - 1)

    if k_t >= ceil(0.6 * (n - 1)):
        qbar = min(1, 0.7*qbar + 0.3*q_t + 0.10)
    else if k_t <= floor(0.2 * (n - 1)):
        qbar = max(0, 0.7*qbar + 0.3*q_t - 0.20)
    else:
        qbar = 0.7*qbar + 0.3*q_t

    clamp qbar to [0,1]

    if strike >= 2 and t < r-1 and S_t >= 0.25 * capacity:
        mark next round as D unless q_t >= 0.5
```

**Behavioral summary**
- Open cooperatively
- Continue cooperating when the stock is healthy and opponents show moderate-to-high cooperation
- Shift to defection after repeated low cooperation
- Return to cooperation immediately when cooperation recovers
- End cooperatively regardless of history
'''

description_BENEVOLENT_7 = '''
Play cooperatively by default and use defection only as a short corrective move when the observed cooperation level is too low to keep the stock near a healthy range.

Maintain a target stock band:
- Upper bound: `U = 0.9 * capacity`
- Lower bound: `L = 0.6 * capacity`

At the start of each round `t`, with current stock `S` and previous-round count of cooperating opponents `c` out of `n-1`:

1. **First round**
   - Play `C`.

2. **If the stock is critically low**
   - If `S <= L/2`, play `C` unconditionally.
   - If `S == 0`, play `C`.

3. **If the stock is high or recovering**
   - Let `coop_rate = c / (n - 1)`.
   - Compute the “expected cooperation pressure”:
     - `expected_pressure = 1 - coop_rate`
   - If `S >= U`, play `C` unless the previous round had very low cooperation:
     - play `D` only if `coop_rate < 0.25` and `S > L`.
   - If `L < S < U`, play `C` unless cooperation was persistently low:
     - play `D` only if `coop_rate < 0.20` for two consecutive rounds.
   - If `S <= L`, play `C` unless the last round was near-total defection:
     - play `D` only if `coop_rate == 0` and `S > L/3`.

4. **Last round**
   - Play `C` if `S > 0`.
   - If `S == 0`, play `C`.

5. **Recovery after defection**
   - After any round in which you play `D`, return to `C` immediately in the next round unless the next observed `coop_rate` is again below `0.20`.
   - Never defect two rounds in a row unless both:
     - `coop_rate == 0` in the current round, and
     - `S > L/2`.

6. **Trend memory**
   - Keep a short memory of the last 3 rounds’ cooperation rates.
   - Define `avg_coop = average(coop_rate over last 3 rounds)`
   - If `avg_coop >= 0.5`, always play `C`.
   - If `avg_coop < 0.2`, allow one corrective `D`, then reset to `C`.

Pseudocode:

```text
if t == 1:
    action = C
else if S <= L/2 or S == 0:
    action = C
else:
    coop_rate = observed_cooperators / (n - 1)
    avg_coop = average of last 3 coop_rates, using available history

    if t == r:
        action = C if S > 0 else C
    else if avg_coop >= 0.5:
        action = C
    else if S >= U:
        action = D if coop_rate < 0.25 and S > L else C
    else if S > L:
        action = D if coop_rate < 0.20 for 2 consecutive rounds else C
    else:
        action = D if coop_rate == 0 and S > L/3 else C

if previous action was D:
    force next action to C unless coop_rate < 0.20
```

Tie-breaking and edge cases:
- If observations are unavailable for a round, assume `coop_rate = 1` and play `C`.
- If `n = 2`, treat the single observed opponent as the full cooperation signal.
- If the stock is near capacity, err toward `C`.
- If the stock is near depletion, err toward `C` unless the group is clearly collapsing into full defection.
- Never use repeated defection as punishment; any defection is a one-round signal followed by immediate cooperation.
'''

description_BENEVOLENT_8 = '''
Round 1: cooperate.

For every later round t:

1. Let k be the number of opponents who cooperated in round t−1.
2. Let S be the current stock at the start of round t.
3. Cooperate if all three conditions hold:
   - S ≥ capacity / 4
   - k ≥ ⌈(n−1)/2⌉
   - either round t−1 ended with stock at least capacity / 3, or k = n−1

4. Otherwise defect.

Special cases:
- If S ≤ capacity / 8, defect until S > capacity / 8.
- If S ≥ 3·capacity / 4, cooperate unless k = 0 in the previous round and S fell in that round; in that case defect for one round, then reassess.
- In the final round, cooperate if S > 0.

Memory update:
- After each round, record only the most recent value of k and the resulting stock S.
- Do not punish for more than one round at a time; after any defect, return to cooperation as soon as the conditions above are restored.
'''

description_BENEVOLENT_9 = '''
Initialize a cooperation target and adjust it only from observed aggregate cooperation and current stock.

Let:
- `k_t` = number of opponents who cooperated in round `t`
- `x_t = k_t / (n - 1)` = observed opponent cooperation rate after round `t`
- `S_t` = stock at the start of round `t`
- `p_t` = your internal cooperation target for round `t`, in `[0,1]`

Use:
- `p_1 = 1`
- For rounds `t > 1`:
  - if `x_{t-1} >= 0.75`, set `p_t = min(1, p_{t-1} + 0.10)`
  - if `0.40 <= x_{t-1} < 0.75`, set `p_t = p_{t-1}`
  - if `0.20 <= x_{t-1} < 0.40`, set `p_t = max(0.50, p_{t-1} - 0.15)`
  - if `x_{t-1} < 0.20`, set `p_t = max(0.20, p_{t-1} - 0.25)`

Convert the target into an action by comparing the expected gain from cooperation to the expected gain from defection under your current belief that each opponent cooperates with probability `p_t`.

Compute:
- `E_C = S_t / (2n)`
- `E_D = S_t / n`

Choose:
- `C` if `p_t >= 0.5` and `S_t > 0`
- `D` if `p_t < 0.5`

Then apply the following state-based overrides:

1. If `S_t <= 0`, play `C`.
2. If `t = r`, play `C` unless `S_t = 0`.
3. If `t = r - 1` and `S_t > capacity / 4`, play `C`.
4. If `S_t < capacity / 8`, play `D` only if `x_{t-1} < 0.20`; otherwise play `C`.
5. If `S_t >= capacity / 2`, play `C`.
6. If the last two observed cooperation rates satisfy `x_{t-2} >= 0.75` and `x_{t-1} >= 0.75`, play `C` regardless of the target.
7. If the last two observed cooperation rates satisfy `x_{t-2} < 0.20` and `x_{t-1} < 0.20`, play `D` for this round, then reset `p_{t+1} = 0.20`.

Round-by-round procedure:

- Round 1:
  - Play `C`.
- After each round:
  - Record `k_t`.
  - Update `p_{t+1}` using the cooperation-rate rule above.
- In all later rounds:
  - Use the updated target.
  - Apply the state-based overrides in order.
  - If no override applies, follow the target threshold.

Tie and boundary rules:
- Treat `x_t = 0.75`, `0.40`, and `0.20` as belonging to the higher bracket.
- Treat `S_t = capacity / 2`, `capacity / 4`, and `capacity / 8` as satisfying the corresponding inequality exactly.
- If `n = 2`, use the single opponent’s action as `k_t`, with `x_t ∈ {0,1}`.

Fallback rule:
- If the history is unavailable for any reason, set `p_t = 1` and play `C`.
'''

description_BENEVOLENT_10 = '''
Maintain a target regime of near-full replenishment.

Let:
- `k_t` be the number of opponents who cooperated in round `t`
- `S_t` be the stock at the start of round `t`
- `m = n - 1` be the number of opponents
- `q_t = k_t / m` be the observed opponent cooperation rate from the previous round

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **If `S_t` is very low**
   - Play `D` when `S_t <= capacity / 4`.
   - This is a recovery rule: when the stock is badly depleted, stop cooperating until it rebuilds.

3. **If `S_t` is healthy**
   - Play `C` when both conditions hold:
     - `q_{t-1} >= 1/2`, and
     - `S_t >= capacity / 2`
   - Otherwise play `D`.

4. **If `S_t` is moderate**
   - When `capacity / 4 < S_t < capacity / 2`, play `C` only if:
     - `q_{t-1} >= 3/4`
   - Otherwise play `D`.

5. **Last round**
   - If `S_t >= capacity / 2`, play `C`.
   - If `S_t < capacity / 2`, play `D`.

History update rule after each round:
- Record `k_t` and `S_{t+1}`.
- For the next round, compute `q_t = k_t / (n - 1)`.

Edge-case handling:
- If `n = 2`, then `q_t` is either `0` or `1`; treat `q_t >= 1/2` as “the other player cooperated.”
- If `n - 1 = 0` is impossible under the game constraints, so no special handling is needed beyond `n = 2`.
- If the stock ever reaches `0`, play `D` until `S_t > 0`.
- If the stock returns to `capacity`, resume the normal cooperation rule immediately.

Behavioral pattern:
- Start cooperatively.
- Continue cooperating when the stock is healthy and most opponents are cooperating.
- Defect whenever the stock becomes strained or opponent cooperation drops below the required threshold.
- Re-enter cooperation as soon as the stock is restored and recent opponent cooperation is sufficiently high.
'''

description_BENEVOLENT_11 = '''
Initialize trust = 1.

Round 1:
- Cooperate.

After each round t, record:
- k = number of opponents who cooperated in round t
- q = k / (n - 1) if n > 2, and q = k if n = 2
- Update trust = 0.6 × trust + 0.4 × q

For rounds 1 < t < r:
- Cooperate if any of the following holds:
  - stock ≤ capacity / 2
  - q ≥ 1/2
  - trust ≥ 1/2
- Otherwise defect for this round only.

Round r:
- Cooperate.

Tie-breaking and edge handling:
- If n = 2, treat q as 1 when the other player cooperated and 0 otherwise.
- If history is unavailable for a round, default to cooperation.
- If stock is exactly capacity / 2, cooperate.
- If opponents alternate between high and low cooperation, use trust rather than the single last-round observation: one low-cooperation round is not enough to trigger lasting defection.
- After any round with q = 1, immediately reset trust to at least 3/4 before the next decision.
'''

description_BENEVOLENT_12 = '''
Maintain a cooperation target that keeps the stock near the regeneration sweet spot and mirror the crowd only as much as needed to protect the pool.

Let:
- `S` be the current stock at the start of the round
- `k` be the number of opponents who cooperated in the previous round
- `n` be the number of players
- `m = n - 1` be the number of opponents
- `θ = ceil(m / 2)` be the minimum number of cooperating opponents needed to treat the environment as cooperative

Decision rule for round 1:
- Play `C`

Decision rule for round `t > 1`:
1. If `S <= n`, play `D` only if the previous round was severely overused:
   - If `k < θ`, play `D`
   - Otherwise play `C`
2. If `S > n`, play `C` unless the previous round showed clear collapse:
   - If `k = 0`, play `D`
   - Otherwise play `C`

Threshold interpretation:
- `k >= θ` means the group was at least roughly cooperative, so continue cooperating.
- `k < θ` means the group was under-cooperating, so reduce your own restraint by defecting once to signal that the pool must be protected.
- `k = 0` is a special collapse case: no one else cooperated, so defect to avoid being the only restrained player.

Last-round rule:
- Play `C` in the final round unless the previous round had `k = 0`
- If the previous round had `k = 0`, play `D` in the final round

History adjustment:
- Keep a running score of opponent cooperation:
  - `coop_rate = (total opponent cooperations so far) / ((t - 1) * m)`
- If `coop_rate >= 1/2`, use the standard rule above.
- If `coop_rate < 1/2`, require a stronger condition to stay cooperative:
  - cooperate only when `k = m` in the previous round
  - otherwise defect

State-sensitive safeguard:
- If the stock has fallen below `capacity / 4`, play `D` for one round unless all opponents cooperated in the immediately previous round.
- If the stock has recovered to at least `capacity / 2`, return to the standard rule.

Pseudocode:

```text
if t == 1:
    action = C
else:
    if coop_rate < 1/2:
        if k == m:
            action = C
        else:
            action = D
    else:
        if S <= n:
            if k < ceil(m/2):
                action = D
            else:
                action = C
        else:
            if k == 0:
                action = D
            else:
                action = C

if t == r:
    if k == 0:
        action = D
    else:
        action = C
```

If the history is mixed and no clear pattern emerges, default to `C` whenever the pool is not critically low; reserve `D` only for clear, repeated overuse.
'''

description_BENEVOLENT_13 = '''
Initialize:
- Round 1: play C.

For every later round t:

1. Observe current stock S.
2. Observe k = number of opponents who played C in round t−1.
3. Let q = k / (n−1), the observed cooperation rate among opponents.

Decision rule:
- Play C if any of the following holds:
  - S ≥ capacity / 2
  - q ≥ 1/2
  - t = r
  - t > 1 and the previous round’s stock increased or stayed the same
- Otherwise play D.

Refinement for persistent low cooperation:
- If q < 1/3 for two consecutive rounds and S < capacity / 2, play D until either:
  - q ≥ 1/2 in a round, or
  - S ≥ capacity / 2
- As soon as either condition is met, return to C immediately.

Last-round rule:
- Always play C.

Edge cases:
- If no prior opponent action is available, play C.
- If S = 0, play C.
- If S is very small but positive, still play C unless the persistent-low-cooperation condition is active.
- If all opponents cooperated in the previous round, play C regardless of stock.

Pseudocode:
```text
if t == 1:
    action = C
else if t == r:
    action = C
else:
    q = cooperators_last_round / (n - 1)

    if q < 1/3 and q_prev < 1/3 and S < capacity / 2:
        action = D
    else if S >= capacity / 2 or q >= 1/2 or stock_last_round >= S:
        action = C
    else:
        action = C

# update memory
q_prev = q
```

Behavioral principle:
- Cooperate by default.
- Defect only as a short, state-triggered restraint when cooperation has been persistently scarce and the stock is already under pressure.
- Return to cooperation immediately once conditions improve.
'''

description_BENEVOLENT_14 = '''
Let `q_t` be the fraction of opponents who cooperated in round `t`, and let `bad_streak` be the number of consecutive past rounds in which `q_t < 1/2`.

Decision rule for round `t`:

1. If `t = 1`, play `C`.
2. If `t = r`, play `C`.
3. If the current stock is effectively zero, play `C`.
4. Otherwise:
   - If `bad_streak >= 2` and `stock < capacity / 3`, play `D`.
   - In every other case, play `C`.

State update after each round:
- If `q_t >= 1/2`, set `bad_streak = 0`.
- If `q_t < 1/2`, set `bad_streak = bad_streak + 1`.

Optional refinement for faster recovery:
- After any round with `q_t >= 1/2`, ignore all earlier history for punishment purposes and return immediately to unconditional `C`.

Edge handling:
- If `n = 2`, then `q_t` is just the single opponent’s action, so `bad_streak` increases only when that opponent defects.
- If stock is at or near capacity, remain with `C`.
- If stock is low but cooperation has recently recovered, still play `C`; only the two-round sustained low-cooperation pattern activates `D`.
- If the strategy has just played `D` once, return to `C` immediately on the next round unless the trigger condition is still satisfied again.
'''

description_BENEVOLENT_15 = '''
Let \(k_t\) be the number of opponents who cooperated in round \(t\), so \(0 \le k_t \le n-1\). Let
\[
\hat{p}_t=\frac{1}{n-1}\sum_{s=1}^t k_s
\]
be the running average opponent cooperation rate up to round \(t\), with \(\hat{p}_0=1\).

Define the current stock as \(S_t\) at the start of round \(t\).

**Decision rule for round \(t\):**

1. **If \(t=1\):** play \(C\).

2. **If \(t=r\):** play \(C\) if
   \[
   \hat{p}_{t-1} \ge \frac{1}{2}
   \]
   otherwise play \(D\).

3. **For rounds \(1<t<r\):**
   - Compute the expected collective consumption under cooperation rate \(\hat{p}_{t-1}\):
     \[
     L_t = \frac{S_t}{2n}\Big((n-1)\hat{p}_{t-1}+1\Big)
     \]
     where the \(+1\) is your own cooperative action.
   - Compute the post-consumption stock if you cooperate:
     \[
     R_t^{C}=S_t-L_t
     \]
   - Compute the post-consumption stock if you defect while others follow the same average rate:
     \[
     R_t^{D}=S_t-\left(\frac{S_t}{n}+\frac{S_t}{2n}(n-1)\hat{p}_{t-1}\right)
     \]
   - Define the minimum stock-preserving choice as the one that leaves the larger recoverable remainder:
     - play \(C\) if \(R_t^{C}\ge \frac{1}{2}\,capacity\),
     - otherwise play \(D\) only if \(R_t^{D}\ge \frac{1}{2}\,capacity\);
     - if neither action leaves at least \(\frac{1}{2}\,capacity\), play \(C\) whenever \(S_t \ge \frac{capacity}{4}\), and otherwise play \(D\).

**Simplified operational version:**

- Cooperate by default.
- Switch to defect only when both conditions hold:
  1. the observed average opponent cooperation has fallen below \(1/2\), and
  2. the stock is already low enough that cooperation would not restore the pool toward a healthy level.

**Update rule after each round:**

After observing \(k_t\), update
\[
\hat{p}_t=\frac{(t-1)\hat{p}_{t-1}+k_t/(n-1)}{t}.
\]

**Edge cases:**

- If \(n=2\), then \(k_t\in\{0,1\}\) and the same rule applies with \(\hat{p}_t\) being the single opponent’s running cooperation frequency.
- If \(S_t=0\), play \(C\).
- If \(S_t=capacity\), play \(C\).
- If the observed cooperation history is empty or incomplete, treat \(\hat{p}_{t-1}=1\).

**Benevolent response principle:**

- Choose \(C\) whenever cooperation is plausibly sustainable.
- Choose \(D\) only as a restraint when opponent behavior has become consistently uncooperative and the current stock is already degraded.
'''

description_BENEVOLENT_16 = '''
Let `c_t` be the number of opponents who cooperated in round `t-1`, and let `S_t` be the stock at the start of round `t`.

State variables:
- `trust ∈ [0, 1]`, initialized to `1`
- `cooperation_streak`, initialized to `0`

Update after each round `t-1`:
- `obs_rate = c_t / (n - 1)`
- `trust = 0.7 * trust + 0.3 * obs_rate`
- if `obs_rate >= 0.5`, increase `cooperation_streak` by 1; otherwise reset it to 0

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **Last round**
   - Play `C`.

3. **General round**
   - Compute:
     - `high_stock = (S_t >= 0.6 * capacity)`
     - `medium_stock = (S_t >= 0.35 * capacity)`
     - `broad_cooperation = (c_t >= ceil(0.6 * (n - 1)))`
     - `majority_cooperation = (c_t >= ceil((n - 1) / 2))`
   - Play `C` if any of the following holds:
     - `high_stock`
     - `broad_cooperation`
     - `trust >= 0.55`
     - `cooperation_streak >= 2`
   - Otherwise, if all of the following hold:
     - `S_t < 0.35 * capacity`
     - `c_t < ceil((n - 1) / 2)`
     - `trust < 0.4`
     then play `D`.
   - In every other case, play `C`.

Tie-break and edge handling:
- If `n = 2`, interpret `ceil((n - 1) / 2)` as `1`.
- If no opponent data is available yet, treat `c_t` as unknown and follow the first-round rule.
- If stock is exactly on a threshold, treat it as satisfying the threshold.
- If the stock is ever extremely low, `S_t <= capacity / (4n)`, play `C` unless the state has already satisfied the defection condition above for two consecutive rounds.

Implementation form:

```text
if t == 1 or t == r:
    action = C
else:
    if S_t >= 0.6*capacity:
        action = C
    else if c_t >= ceil(0.6*(n-1)):
        action = C
    else if trust >= 0.55:
        action = C
    else if cooperation_streak >= 2:
        action = C
    else if S_t < 0.35*capacity and c_t < ceil((n-1)/2) and trust < 0.4:
        action = D
    else:
        action = C
```
'''

description_BENEVOLENT_17 = '''
Cooperate in every round.

Decision rule:
- If stock > 0: play C.
- If stock = 0: play C.

History use:
- Record the number of opponents who cooperated each round.
- Do not condition the action on that count; keep playing C.

Edge cases:
- Round 1: play C.
- Last round: play C.
- Any round after complete depletion: play C.
- If the observed cooperation count is unavailable for any reason, default to C.

Pseudocode:
```text
for each round t = 1..r:
    action = C
```
'''

description_BENEVOLENT_18 = '''
Round 1: play C.

For every later round t:
- If stock > 0: play C.
- If stock = 0: play C.

Equivalent policy:
```text
for each round t:
    choose C
```

If a conditional form is required:
- Ignore opponent counts for action selection.
- Never defect.
- Never switch away from cooperation based on past defections, low stock, or remaining rounds.
- In the last round, still cooperate.

If you want an explicit state-based version:
```text
if t == 1: C
else if stock >= 0: C
```

Use the observed cooperation counts only to record the state of the group, not to trigger retaliation.
'''

description_BENEVOLENT_19 = '''
Play C by default.

Maintain a running estimate of the cooperative level:
- Let c_t be the number of opponents who cooperated in round t.
- Let \(\bar c_t\) be the average of the last \(m\) observed values of \(c\), using all available past rounds if fewer than \(m\) have occurred.
- Use \(m = \min(3, t-1)\).

Decision rule for round t with current stock S:

1. First round:
   - Play C.

2. If \(S \le n\):
   - Play C.
   - If exactly one previous round exists and all opponents defected in that round, still play C.

3. If \(S > n\):
   - Compute the expected total consumption if you cooperate:
     \[
     E[\text{consumption} \mid C] = \frac{S}{2n} + \bar c_t \cdot \frac{S}{2n} + (n-1-\bar c_t)\cdot \frac{S}{n}
     \]
   - Compute the expected total consumption if you defect:
     \[
     E[\text{consumption} \mid D] = \frac{S}{n} + \bar c_t \cdot \frac{S}{2n} + (n-1-\bar c_t)\cdot \frac{S}{n}
     \]
   - Let \(R_C\) and \(R_D\) be the corresponding remaining stocks after consumption.
   - Predict next stock using the growth rule:
     \[
     G(R)=2R\left(1-\frac{R}{\text{capacity}}\right), \quad S'=\min(R+G(R), \text{capacity})
     \]
   - If \(S'_C \ge S'_D\), play C.
   - Otherwise, play C unless \(\bar c_t = 0\), in which case play D.

4. Endgame:
   - In the final round, play C unless \(S \le n/2\), in which case play D.

5. Recovery rule after defection-heavy rounds:
   - If at least two of the last three rounds had fewer than half of opponents cooperating, play C for the next two rounds regardless of the estimate.
   - If cooperation recovers to at least half of opponents cooperating in a round, immediately return to the normal rule.

6. Symmetry-breaking when indifferent:
   - If the rule is exactly tied between C and D, play C.

7. Hard safeguard:
   - Never choose D if that would make the post-round stock estimate fall below \(S/2\) and C would not.

This policy is:
- C by default
- C when stock is fragile
- C when cooperation is reasonably sustained
- D only when the observed environment is persistently noncooperative and the stock is already high enough that restraint is not needed to preserve the pool
'''

description_BENEVOLENT_20 = '''
Cooperate by default.

Define, at the start of round t, the current stock as S_t and the number of other players who cooperated in round t−1 as k_{t−1}. Let m = n−1.

Use this rule:

1. Round 1:
- Play C.

2. Each later round t > 1:
- Compute the cooperation rate among the other players in the previous round:
  q = k_{t−1} / m.

- Compute the sustainable cooperation threshold for the current stock:
  threshold(S_t) = 1 − 1 / sqrt(2)
  and a protection margin:
  margin(S_t) = 0.10 + 0.20 × max(0, 1 − S_t / capacity).

- Cooperate if both conditions hold:
  - q ≥ threshold(S_t) − margin(S_t)
  - S_t ≥ capacity / 4

- Defect otherwise.

3. Recovery rule after a poor round:
- If you defected in the previous round and the observed cooperation rate in that round was q ≥ threshold(S_t) + margin(S_t), return to C immediately in the next round.
- If you defected in the previous round and q is still below that level, continue with D until either:
  - q reaches threshold(S_t) + margin(S_t), or
  - S_t rises back to at least capacity / 4.

4. Last round:
- Play C unless the current stock is critically low:
  - if S_t < capacity / 8, play D
  - otherwise play C

5. Persistent low-cooperation safeguard:
- If the observed cooperation rate has been below threshold(S_t) − margin(S_t) for two consecutive rounds, play D until the first round in which either:
  - the cooperation rate returns to at least threshold(S_t) − margin(S_t), or
  - S_t rises to at least capacity / 4

6. Full cooperation mode:
- If all other players cooperated in the previous round, play C.
- Stay in C as long as all other players keep cooperating or the stock does not fall below capacity / 4.

7. Severe depletion mode:
- If S_t ≤ capacity / 8, play D for that round.
- After a severe depletion round, resume C as soon as either:
  - the other players’ cooperation rate is at least threshold(S_t), or
  - S_t rises above capacity / 8

Behavioral summary:
- Start cooperative.
- Match broad cooperation with cooperation.
- Only defect to prevent rapid stock collapse after repeated noncooperation or very low stock.
- Return to cooperation immediately when the observed behavior becomes sufficiently cooperative again.
- Favor the long-run restoration of the pool over retaliation.
'''

description_BENEVOLENT_21 = '''
Use a state-contingent conservation policy.

Let:
- `t` be the current round, starting at 1
- `S` be the current stock at the start of round `t`
- `k` be the number of opponents who cooperated in the previous round
- `m = n - 1` be the number of opponents
- `x = k / m` be the observed opponent cooperation rate from the previous round
- `S_next_C` be the stock that would result next round if you cooperate now, assuming the same opponent action profile as in the current round
- `S_next_D` be the stock that would result next round if you defect now, assuming the same opponent action profile as in the current round

Decision rule:

1. First round:
   - Play `C`.

2. For every later round:
   - Compute the projected next-round stock under both possible actions using the currently observed stock `S` and the last observed opponent cooperation rate `x`.
   - If `S <= 0`, play `C`.
   - If `x >= 0.5`, play `C`.
   - If `x <= 0.25`, play `D` only if `S >= 1.5 * capacity`; otherwise play `C`.
   - Otherwise play `C`.

Equivalent concise policy:
- Default to `C`.
- Switch to `D` only in a clearly overabundant stock state and only after repeated low cooperation by others.

Round-by-round implementation:

- Round 1:
  - `C`

- Rounds `2` through `r-1`:
  - If `stock <= capacity / 2`, play `C`.
  - Else if at least half of opponents cooperated in the previous round, play `C`.
  - Else if fewer than one quarter of opponents cooperated in the previous round and `stock >= 3 * capacity / 2`, play `D`.
  - Else play `C`.

- Final round `r`:
  - Play `C` unless the current stock is above `capacity / 2` and the previous-round cooperation rate was below `1/4`; in that case play `D`.

Edge handling:

- If `m = 1`, then `x` is either `0` or `1`; apply the same thresholds directly.
- If the observed number of cooperating opponents is missing for the previous round, treat `x` as `1`.
- If the stock is at or below `0`, always play `C`.
- If the stock is at capacity, never defect unless the low-cooperation condition has persisted and the stock remains very high.
- If multiple consecutive rounds had `x >= 0.5`, continue cooperating without interruption.

Behavioral rule in pseudocode:

```text
if t == 1:
    action = C
else:
    x = coop_opponents_last_round / (n - 1)

    if stock <= 0:
        action = C
    else if t == r:
        if stock > capacity / 2 and x < 1/4:
            action = D
        else:
            action = C
    else:
        if stock <= capacity / 2:
            action = C
        else if x >= 1/2:
            action = C
        else if x < 1/4 and stock >= 3 * capacity / 2:
            action = D
        else:
            action = C
```

If cooperation rises again after any defect, immediately return to `C` and remain there while opponent cooperation stays at or above half.
'''

description_BENEVOLENT_22 = '''
- Round 1: play `C`.

- After each round, record:
  - `k =` number of opponents who cooperated
  - `m = n - 1`
  - `low = 1` if `k < ceil(m / 2)`, else `0`
  - `low_streak =` consecutive number of most recent rounds, ending last round, with `low = 1`

- Decision rule for round `t > 1`:
  - If `t = r`: play `C`.
  - Else if `stock >= capacity / 3`: play `C`.
  - Else if `low_streak >= 2`: play `D`.
  - Else: play `C`.

- Update rule for `low_streak`:
  - If `low = 1`, set `low_streak = low_streak + 1`
  - Otherwise set `low_streak = 0`

- Edge cases:
  - If `n = 2`, then `ceil((n - 1) / 2) = 1`, so treat “at least half of opponents cooperated” as “the other player cooperated.”
  - If a round is the last round, always cooperate regardless of stock or history.
  - If there has not yet been enough history to form `low_streak >= 2`, cooperate.

- Behavioral intent:
  - Cooperate by default.
  - Continue cooperating whenever the pool remains healthy or the recent behavior of others is not persistently exploitative.
  - Use defection only as a short, state-based conservation response after repeated low cooperation by the rest of the group.
'''

description_BENEVOLENT_23 = '''
Round 1: play C.

For round t ≥ 2, let q be the fraction of opponents who cooperated in round t−1.

Play C if any of the following holds:
- t = r
- the current stock S is at least capacity/4
- q ≥ 1/2
- q ≥ 1/3 and you played D in the previous round

Play D only if all of the following hold:
- t < r
- S < capacity/4
- q < 1/2
- either q < 1/3, or you already used your one-round forgiveness after a low-cooperation round and cooperation did not recover

State update:
- After any round with q ≥ 1/2, reset the forgiveness state to unused.
- After any round with q < 1/2, mark the forgiveness state as used for the next round only.

Edge cases:
- If n = 2, then q is either 0 or 1, and the same rules apply directly.
- If the previous round was unobserved for any reason, default to C.
- If the stock is extremely low, still play C unless the low-cooperation condition has persisted and the forgiveness window has already been spent.

Pseudocode:

```text
if t == 1:
    action = C
else:
    q = observed_cooperators / (n - 1)

    if t == r:
        action = C
    else if S >= capacity / 4:
        action = C
    else if q >= 1/2:
        action = C
        forgiveness_used = false
    else if q >= 1/3 and forgiveness_used == false:
        action = C
        forgiveness_used = true
    else:
        action = D
        forgiveness_used = true
```

Keep cooperation as the default, forgive isolated low-cooperation rounds once, and only defect after repeated low cooperation while the stock is already under strain.
'''

description_BENEVOLENT_24 = '''
Play a conservation-oriented threshold strategy with conditional generosity:

- Maintain a cooperation score for the group:
  - Let `c_t` be the number of opponents who cooperated in round `t`.
  - Let `m_t = c_t / (n - 1)` be the observed cooperation rate among opponents.
  - Let `A_t` be the moving average of `m` over the last up to 3 rounds, initialized to 1.
  - Let `B_t` be the moving average of `m` over the last up to 2 rounds, initialized to 1.

Decision rule:

1. Round 1:
   - Cooperate.

2. Rounds 2 through r-1:
   - Cooperate if both conditions hold:
     - `A_t >= 0.5`
     - current stock is at least `capacity / 4`
   - Otherwise defect.

3. Last round:
   - Cooperate unless both conditions hold:
     - `B_t < 0.5`
     - current stock is below `capacity / 6`
   - If both hold, defect.

Adaptive response to recent behavior:

- If opponents cooperated unanimously in the previous round, cooperate next round regardless of stock, unless the stock has fallen below `capacity / 10`.
- If opponent cooperation drops below half for two consecutive rounds, defect until cooperation recovers to at least half for two consecutive rounds.
- If the stock is recovering or near full (`stock >= 0.8 * capacity`), favor cooperation even after a single weak round.
- If the stock is severely depleted (`stock <= capacity / 8`), defect for one round, then reassess using the moving averages.

Tie-breaking and edge cases:

- If `n = 2`, treat the single observed opponent as the whole signal.
- If there are no prior rounds, default to cooperation.
- If the observed cooperation rate is exactly on the threshold, cooperate.
- If history is shorter than the averaging window, average only over the available rounds.

Behavioral posture:

- Start by extending trust.
- Reward sustained cooperation quickly.
- Withdraw generosity only when the group shows repeated defection or the stock becomes dangerously low.
- Return to cooperation as soon as the group shows renewed restraint.
'''

description_BENEVOLENT_25 = '''
Round 1: cooperate.

For every later round, observe:
- current stock S
- c = number of opponents who cooperated in the previous round
- d = (n - 1) - c

Compute the expected next stock if you cooperate now, assuming opponents repeat their last-round action:
- If you cooperate, total consumption next round would be S/(2n) + c·S/(2n) + d·S/n
- If you defect, total consumption next round would be S/n + c·S/(2n) + d·S/n

Use this rule:

1. Baseline behavior
- Cooperate whenever the stock is not in danger of collapsing under broad cooperation.
- Defect only when the stock is so low that cooperating would materially reduce the chance of recovery, or when opponents have just pushed the stock into a critical state.

2. Critical-stock threshold
- Define the cooperative sustainability threshold:
  - T = capacity / 2
- If S ≥ T, cooperate.
- If S < T, use the recent opponent behavior to decide:
  - If c ≥ ceil((n - 1)/2), cooperate.
  - Otherwise, defect.

3. Recovery rule
- If the previous round had at least half of opponents cooperate, always cooperate for the next two rounds.
- If the previous round had a majority defect and S < T, defect once, then re-evaluate from the next round using the same rule.

4. Endgame rule
- In the last round, cooperate if S > 0.
- In the penultimate round and later, if you have cooperated in the previous round and at least one-third of opponents cooperated, continue cooperating.
- If S is already very low, define very low as S ≤ capacity / n, then defect only if fewer than half of opponents cooperated in the previous round; otherwise cooperate.

5. Forgiveness and reset
- After any round with c ≥ ceil((n - 1)/2), reset to cooperative mode.
- A single low-cooperation round does not permanently trigger defection.
- Require two consecutive majority-defection rounds before staying in defensive mode, and leave defensive mode immediately after one majority-cooperation round.

Operational version:

```
if t == 1:
    action = C
else if t == r:
    action = C if S > 0 else C
else if S >= capacity / 2:
    action = C
else if c >= ceil((n - 1) / 2):
    action = C
else if S <= capacity / n and c < ceil((n - 1) / 2):
    action = D
else if previous_action == C and c >= ceil((n - 1) / 3):
    action = C
else:
    action = D
```

If the previous round produced majority cooperation, cooperate immediately and stay cooperative unless the stock falls below capacity / n and cooperation from opponents drops below half.
'''

description_BENEVOLENT_26 = '''
Initialize:
- `last_round_defection = false`
- `trust = 1.0`
- `target_stock = capacity / 2`
- `critical_stock = capacity / 4`

Round 1:
- Play `C`.

After each round, observe:
- `k =` number of opponents who played `C`
- `S =` current stock before your move next round

Decision rule for round `t > 1`:

1. If `S <= critical_stock`:
   - Play `D` only if `k == 0`
   - Otherwise play `C`

2. Else if `t == r`:
   - Play `C` if `k > 0`
   - Play `D` only if `k == 0` or `S < target_stock / 2`

3. Else if `k >= n - 2`:
   - Play `C`

4. Else if `k == n - 3`:
   - Play `C` unless `S < target_stock / 3`, in which case play `D`

5. Else if `k <= n - 4`:
   - Play `D` for one round, then return to `C` immediately once `k >= n - 3`

Recovery rule:
- After any round in which you played `D`, switch back to `C` as soon as either:
  - `k >= n - 3`, or
  - `S > target_stock`

Fallback rule:
- If the state is not clearly covered above, play `C`.

Equivalent concise policy:

```text
if t == 1:
    action = C
else if S <= critical_stock:
    action = C if k > 0 else D
else if t == r:
    action = C if (k > 0 and S >= target_stock / 2) else D
else if k >= n - 2:
    action = C
else if k == n - 3:
    action = C if S >= target_stock / 3 else D
else:
    action = D
```

Benevolent adjustment:
- Never defect more than one round in a row unless the observed cooperation count stays at `0` or `1` and the stock remains below `critical_stock`.
- If the stock rebounds to at least `target_stock`, return to unconditional cooperation until another severe shortage is observed.

This produces:
- unconditional cooperation at the start,
- strong preference for cooperation whenever the group is maintaining the resource,
- limited defensive defection only when the observed behavior is severely non-cooperative,
- immediate restoration of cooperation once conditions improve.
'''

description_BENEVOLENT_27 = '''
Cooperate in round 1.

After each round, compute:

- `k = number of opponents who cooperated last round`
- `p = k / (n - 1)` if `n > 2`; for `n = 2`, treat `p = 1` if the other player cooperated, else `0`
- `S = current stock at the start of this round`

Let `expected_stock_if_all_cooperate = S / 2` after everyone cooperates once, so the stock is being sustainably shared.

Decision rule:

1. **Default to cooperation** whenever the observed cooperation rate is at least half:
   - Cooperate if `p ≥ 1/2`

2. **Escalate to protection only after repeated low cooperation:**
   - If `p < 1/2` for **two consecutive rounds**, defect for one round.
   - Return to cooperation immediately if the observed cooperation rate in the previous round is at least half.

3. **If stock becomes critically low, protect the resource:**
   - Defect if `S` is below `capacity / 4` and fewer than `2/3` of opponents cooperated last round.
   - Otherwise keep cooperating.

4. **Near the end of the game, stay cooperative unless exploitation is severe:**
   - In the last round, cooperate if `p ≥ 1/2`.
   - Defect only if `p < 1/2` and `S < capacity / 4`.

5. **After any round where cooperation recovers, forgive immediately:**
   - If at least half of opponents cooperate in the previous round, cooperate next round regardless of earlier defections.

Edge cases:

- **First round:** cooperate.
- **Second round:** cooperate unless the first round had less than half cooperation and the stock already dropped below `capacity / 4`.
- **If all opponents defect last round:** defect next round, but return to cooperation as soon as cooperation rises to at least half.
- **If all opponents cooperate last round:** cooperate.
- **If the stock is at or near capacity:** cooperate.
- **If the stock is zero:** cooperate only if the last round showed recovery to at least half cooperation; otherwise defect until cooperation recovers.

Pseudocode:

```text
state variables:
  bad_streak = 0

each round:
  observe S, k
  p = k / (n - 1)   # for n = 2, p is 1 if other cooperated else 0

  if round == 1:
      action = C
  else if p >= 1/2:
      action = C
      bad_streak = 0
  else:
      bad_streak += 1
      if S < capacity / 4 and p < 2/3:
          action = D
      else if bad_streak >= 2:
          action = D
      else:
          action = C

  if last_round and p < 1/2 and S < capacity / 4:
      action = D
```
'''

description_BENEVOLENT_28 = '''
Always cooperate.

Decision rule:
- In every round t = 1, 2, ..., r, choose C regardless of:
  - the current stock level,
  - the number of opponents who cooperated in prior rounds,
  - the round number,
  - any past history of actions or stock changes.

Edge cases:
- First round: choose C.
- Last round: choose C.
- If the stock is 0: choose C.
- If the stock is at capacity: choose C.
- If every opponent defected in the previous round: choose C.
- If every opponent cooperated in the previous round: choose C.

State dependence:
- Ignore all observed history for action selection; use it only to confirm that the strategy remains unchanged.

Behavioral principle:
- Never punish, never retaliate, never condition cooperation on opponent behavior; always minimize extraction by selecting C.
'''

description_BENEVOLENT_29 = '''
Play C in every round.

Decision rule:
- Round 1: choose C.
- Rounds 2 through r: choose C, regardless of the observed number of opponent cooperators or the current stock level.
- If stock = 0, still choose C.

Tie-breaking and edge cases:
- If the game ends, there is no terminal-round deviation; the last round is treated exactly like every other round.
- If any information is missing or ambiguous, default to C.
- If the number of observed cooperating opponents is used for bookkeeping, it never changes the action choice.

Behavioral principle:
- Never exploit a round for private gain.
- Never punish, retaliate, or mirror defection.
- Maintain unconditional cooperation throughout the full horizon.
'''

description_BENEVOLENT_30 = '''
Play C in every round.

Decision rule:
- Round 1: C.
- Every later round: C, regardless of the number of cooperating opponents, current stock level, or remaining rounds.

Edge cases:
- If stock is 0, play C.
- If stock is at capacity, play C.
- On the last round, play C.
- If all opponents defect in a round, play C in the next round.
- If all opponents cooperate in a round, play C in the next round.

State use:
- Use history only to keep confirming the same action: continue cooperating no matter what is observed.
- Never switch to D.
'''

description_BENEVOLENT_31 = '''
Round 1: play C.

After each round, let m be the number of opponents who cooperated in the previous round, and let S be the current stock.

For every round t > 1, compute:

- If you play C:
  - remaining stock after consumption:  
    x_C = S * (m + 1) / (2n)
  - next stock:  
    F_C = min(x_C + 2x_C(1 - x_C / capacity), capacity)

- If you play D:
  - remaining stock after consumption:  
    x_D = S * m / (2n)
  - next stock:  
    F_D = min(x_D + 2x_D(1 - x_D / capacity), capacity)

Decision rule:
- Play C if F_C >= F_D
- Play D only if F_D > F_C

Tie-breaking:
- If F_C = F_D, play C.

Edge cases:
- If S = 0, play C.
- If m is unavailable for any reason, play C.
- In the last round, use the same rule; if tied, play C.

Behavioral principle:
- Default to cooperation.
- Switch to D only when it strictly preserves a better future stock level than C in the current observed state.
- Return to C immediately once C is no longer worse than D.
'''

description_BENEVOLENT_32 = '''
Play cooperation by default, and use the observed history only to preserve the stock when the group is already overusing it.

Let:
- `k_t` = number of opponents who cooperated in round `t`
- `x_t` = total number of cooperators in round `t`, including you if you cooperated
- `S_t` = stock at start of round `t`

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **If the previous round was healthy**
   - Define the previous round as healthy if  
     `x_{t-1} >= ceil(n/2)`.
   - If healthy, play `C`.

3. **If the previous round was unhealthy**
   - Define the previous round as unhealthy if  
     `x_{t-1} < ceil(n/2)`.
   - Play `D` only if both conditions hold:
     - `t` is among the last two rounds, or
     - the stock is already low: `S_t <= capacity / 4`.
   - Otherwise play `C`.

4. **Hard stock protection**
   - If `S_t <= 2n`, play `C` unless at least `n-1` opponents defected in the previous round.
   - If at least `n-1` opponents defected in the previous round, play `D` only when `t` is the last round; otherwise play `C`.

5. **Last round**
   - Play `C` unless the previous round had fewer than `ceil(n/2)` cooperators, in which case mirror the prior round’s majority:
     - if `k_{t-1} >= (n-1)/2`, play `C`
     - else play `D`

6. **Tie and partial-information handling**
   - When the observed opponent cooperation count is exactly on the boundary between “healthy” and “unhealthy,” treat it as healthy and play `C`.
   - If information from the previous round is unavailable for any reason, play `C`.

State-based version:

```text
if t = 1:
    play C
else if t = r:
    if x_{t-1} >= ceil(n/2):
        play C
    else if k_{t-1} >= (n-1)/2:
        play C
    else:
        play D
else if S_t <= 2n:
    if k_{t-1} = n-1:
        play D
    else:
        play C
else if x_{t-1} >= ceil(n/2):
    play C
else if S_t <= capacity/4 or t >= r-1:
    play D
else:
    play C
```

Interpretation of the behavior:
- Start by cooperating.
- Continue cooperating whenever the group has recently maintained broad cooperation.
- Respond to repeated overuse with temporary defection, but only when the stock is already strained or the game is nearly over.
- Prefer cooperation whenever the information is ambiguous.
'''

description_SELFISH_5 = '''
- Round 1: defect.

- For rounds t = 2 to r - 1:
  1. Let `q = (number of opponents who cooperated in round t-1) / (n-1)`.
  2. Let `s = stock / capacity`.
  3. Cooperate only if all of the following hold:
     - `q >= 1/2`
     - `s >= 1/4`
     - either `q >= 2/3` or `s >= 1/2`
  4. Otherwise defect.

- Round r: defect.

- Persistence rule:
  - If the previous round had `q < 1/2`, defect in the next round unless `q >= 2/3` in that same observation window and `s >= 1/2`.
  - If the stock ever falls below `capacity / 4`, defect until the stock rises back to at least `capacity / 2` and the observed cooperation rate in the most recent round is at least `2/3`.

- Interpretation:
  - Cooperate only when the pool is still valuable and the others are behaving cooperatively enough to justify preserving it.
  - Exploit high stock aggressively when others are unreliable.
  - Never waste a late-round move on cooperation when there is no future return to protect.
'''

description_SELFISH_6 = '''
State variables:
- `cbar`: exponentially weighted average of observed opponent cooperation rates, initialized to `1`
- `punish`: number of rounds left in a defensive mode, initialized to `0`

At the start of round `t`, with current stock `S` and `L = r - t + 1` rounds remaining:

1. If `L = 1`, play `D`.
2. Else if `punish > 0`, play `D`.
3. Else compute `q = observed_cooperators_last_round / (n - 1)` if `t > 1`, otherwise set `q = 1`.
4. Update `cbar = 0.75 * cbar + 0.25 * q` after observing last round.
5. Cooperate only if both of these hold:
   - `S >= 0.8 * capacity`
   - `cbar >= 0.8`
   and, in addition, at least `n - 2` opponents cooperated in the previous round.
6. Otherwise play `D`.

After each round, update defensive mode:
- If `q <= 0.5`, set `punish = 2`.
- Else if `punish > 0`, decrement `punish` by `1`.

Edge cases:
- Round 1: play `C` if `n = 2`; otherwise play `C` only if you want one probe round, but default to `D` if you want immediate self-protection. Use `C` only when starting stock is at capacity and no information exists.
- If stock drops below `0.6 * capacity`, play `D` until stock returns to at least `0.8 * capacity` and `cbar >= 0.8`.
- If the observed cooperation count is `n - 1` for two consecutive rounds and stock is at least `0.9 * capacity`, return to `C`.
- Never cooperate in the final round.

Selfish decision rule:
- Cooperate only when the pool is being kept near full by others, because that is when preserving the stock protects your future payoffs.
- Defect whenever others are not reliably maintaining the resource, whenever the stock has been depleted, or whenever no future rounds remain.
'''

description_SELFISH_7 = '''
Initialize an estimate of opponent cooperation rate:

- Let `q` be the estimated fraction of opponents who cooperate.
- Start with `q = 0.5`.
- After each round, update `q` by exponential smoothing from the observed number of cooperating opponents `k`:
  `q := 0.7*q + 0.3*(k/(n-1))`

Track the current stock `S` exactly from the public state.

Decision rule in round `t`:

1. Compute the expected stock after the round under each action, using `q` as the forecast of opponent behavior.

   If you play `C`, expected total consumption is:
   `S/(2n) + (n-1)[q*S/(2n) + (1-q)*S/n]`

   If you play `D`, expected total consumption is:
   `S/n + (n-1)[q*S/(2n) + (1-q)*S/n]`

   Let `S_C` and `S_D` be the expected next-round stocks obtained by applying the stock update rule to those two expected consumptions.

2. Play `D` if all of the following hold:
   - `S > 0.6 * capacity`
   - `q >= 0.4`
   - `S_D >= 0.5 * capacity`

   Otherwise play `C`.

Edge cases:

- Round 1: play `D`.
- If `S <= capacity / 2`, play `C`.
- If `S <= 0`, play `C` by default.
- In the last round, play `D` if `S > 0`, otherwise `C` if forced to choose with zero stock.

Tie-break rule:

- If the rule is exactly indifferent between `C` and `D`, choose `D`.

Update rule after observing opponents’ cooperation count `k`:

- `q := 0.7*q + 0.3*(k/(n-1))`

Selfish mode of play:

- Take `D` whenever the stock is high enough and the observed cooperation level suggests the pool can absorb it.
- Switch to `C` only when depletion risk becomes significant or opponents are too uncooperative to sustain profitable defection.
'''

description_SELFISH_8 = '''
Round 1: play D.

For rounds 2 through r-1, let q be the average fraction of opponents who cooperated over the last up to 3 observed rounds.

Use stock bands:

- If stock ≤ 0.20 × capacity: play C only if q ≥ 0.80; otherwise play D.
- If 0.20 × capacity < stock ≤ 0.45 × capacity: play C only if q ≥ 0.60; otherwise play D.
- If 0.45 × capacity < stock ≤ 0.70 × capacity: play D unless q ≥ 0.80 and stock has risen in each of the last 2 rounds; then play C.
- If stock > 0.70 × capacity: play D.

Round r: play D.

Additional updating rule:
- After every round, recompute q from the most recent observations.
- If the stock falls in two consecutive rounds, tighten the thresholds by 0.10 for the rest of the game:
  - 0.80 becomes 0.90
  - 0.60 becomes 0.70
  - 0.20 becomes 0.30
  - 0.45 becomes 0.55
  - 0.70 becomes 0.80

Behavioral principle:
- Default to D.
- Cooperate only when the stock is visibly at risk of collapse and opponents are already cooperating at a strong rate.
- Stop cooperating immediately if opponent cooperation drops below the relevant threshold.
'''

description_SELFISH_9 = '''
Round 1: defect.

From round 2 onward, track the observed fraction of opponents who cooperated in previous rounds, with extra weight on the most recent round. Let \(\hat q\) be that smoothed cooperation rate, and let \(\hat k=(n-1)\hat q\) be the expected number of cooperating opponents this round.

For the current stock \(S\):

- If only one round remains, defect.
- Otherwise compute the projected remaining stock under your two actions:
  - If you defect: \(x_D = S \cdot \hat k/(2n)\)
  - If you cooperate: \(x_C = S \cdot (\hat k+1)/(2n)\)

Use the following rule:

- Cooperate only if all three hold:
  1. \(\hat q \ge 1/2\)
  2. \(x_D < 3\,\text{capacity}/4\)
  3. \(x_C\) is closer to \(3\,\text{capacity}/4\) than \(x_D\) is

- Otherwise defect.

Equivalent pseudocode:

```text
if t == 1:
    action = D
else if rounds_left == 1:
    action = D
else:
    q = smoothed_average(opponent_cooperation_fractions)
    k = (n-1) * q
    xD = S * k / (2n)
    xC = S * (k + 1) / (2n)

    if q >= 0.5 and xD < 0.75 * capacity and abs(xC - 0.75*capacity) < abs(xD - 0.75*capacity):
        action = C
    else:
        action = D
```

If opponent cooperation falls below half on average, never cooperate. If cooperation is frequent enough to keep the stock near its most valuable regeneration zone, cooperate just enough to preserve the resource while still defecting whenever that preservation condition is not met.
'''

description_SELFISH_10 = '''
Round 1: defect.

For round t > 1:

1. Let `k` be the number of opponents who cooperated in round `t-1`.
2. Let `L = r - t` be the number of rounds after the current one.
3. Define the stock transition function
   ```
   next_stock(S, m) = min(R + 2*R*(1 - R/capacity), capacity)
   where R = S * m / (2n)
   ```
   and `m` is the total number of cooperators in the round.

4. Predict the next stock under each possible action:
   - If I cooperate: `m_C = k + 1`
   - If I defect: `m_D = k`

   ```
   S_C = next_stock(stock, m_C)
   S_D = next_stock(stock, m_D)
   ```

5. Score each action as immediate selfish gain plus a continuation value:
   ```
   score(C) = stock/(2n) + L * S_C/(2n)
   score(D) = stock/n     + L * S_D/(2n)
   ```

6. Play the action with the higher score.
   - If the scores are equal, defect.

Edge cases:
- Last round (`t = r`): defect.
- If `k = 0`, defect unless the score rule above prefers cooperation.
- If `k = n - 1` and the score rule is close, defect on ties; cooperate only when it clearly preserves enough future stock to outweigh the immediate loss.
- If the stock is already near zero, cooperate only if it increases the predicted next stock enough to improve the continuation score; otherwise defect.
- If the stock is at capacity and opponents were cooperative, defect unless the continuation score still favors cooperation.
'''

description_SELFISH_11 = '''
Initialize:
- Set `q = 1/2` as the estimated opponent cooperation rate.
- Set `last_k = n-1` only as a neutral starting estimate.

For round `t = 1`:
- Play `C`.

For rounds `2 <= t < r`:
1. Let `k` be the number of opponents who cooperated in round `t-1`.
2. Update the cooperation estimate with exponential smoothing:
   - `q = 0.7*q + 0.3*(k/(n-1))`
3. Predict the number of opponent cooperators this round:
   - `k_hat = round(q*(n-1))`
4. Evaluate the two candidate actions using the current stock `S`:
   - If I play `C`, predicted total cooperators are `m_C = k_hat + 1`
   - If I play `D`, predicted total cooperators are `m_D = k_hat`
   - Predicted remaining stock after consumption:
     - `R(m) = S * m / (2n)`
   - Predicted next stock:
     - `N(m) = min(3*R(m) - 2*(R(m)^2)/capacity, capacity)`
5. Compute the selfish continuation comparison:
   - `gain_C = S/(2n) + (r - t - 1) * N(m_C)/(2n)`
   - `gain_D = S/n + (r - t - 1) * N(m_D)/(2n)`
6. Play:
   - `C` if `gain_C >= gain_D`
   - otherwise `D`

For the last round `t = r`:
- Play `D`.

Edge handling:
- If `S <= 0`, play `D`.
- If `k = 0` in any round before the last, play `D`.
- If `k = n-1` and `S` is high, the rule above usually selects `C`; otherwise it defects.
- If the two candidate values are equal, play `D`.

Behavioral core:
- Start by cooperating to learn the environment.
- Cooperate only when the observed level of cooperation is high enough that preserving the stock is worth more than the immediate extra gain from defecting.
- Defect whenever the stock is already weak, cooperation is collapsing, or the horizon is too short for restraint to pay back.
'''

description_SELFISH_12 = '''
Round 1: cooperate.

For rounds 2 through r - 1:

1. Let `k` be the number of opponents who cooperated in the previous round.
2. Let `p = k / (n - 1)` be the observed opponent cooperation rate in the previous round.
3. Let `h = r - t + 1` be the number of rounds remaining, including the current round.
4. Define the conservation threshold
   `T = capacity * (0.25 + 0.25 * (h - 1) / (r - 1))`.
   - Early in the game, this sits near `0.5 * capacity`.
   - Late in the game, it drops toward `0.25 * capacity`.

Decision rule:
- If `stock <= T`, cooperate.
- Else if `p < 0.5`, cooperate unless `stock >= 0.85 * capacity`, in which case defect.
- Else defect.

Extra adjustment from recent history:
- If the last two observed opponent cooperation rates were both below `0.4`, cooperate unless `stock >= 0.9 * capacity`.
- If the last two observed opponent cooperation rates were both at least `0.67`, defect whenever `stock > T`.

Last round:
- Defect.

Edge cases:
- If `n = 2`, treat `p = 1` when the single opponent cooperated and `p = 0` when they defected.
- If there is no prior history beyond round 1, use only the current stock threshold and the round-1 action.
- If stock is extremely low, cooperate regardless of opponent behavior; preserving future value dominates.

Operational form:

```text
if t == 1:
    action = C
elif t == r:
    action = D
else:
    p = opponents_cooperated_last_round / (n - 1)
    h = r - t + 1
    T = capacity * (0.25 + 0.25 * (h - 1) / (r - 1))

    if stock <= T:
        action = C
    else if last_two_p_are_both < 0.4:
        action = C if stock < 0.9 * capacity else D
    else if last_two_p_are_both >= 0.67:
        action = D if stock > T else C
    else:
        action = D if p >= 0.5 and stock > T else C
```

This strategy is selfish in the sense that it defects whenever the stock is high enough and the observed cooperation environment makes extraction profitable, while switching to cooperation whenever the pool needs rebuilding to keep future rounds lucrative.
'''

description_SELFISH_13 = '''
Round 1: defect.

For round t > 1:

- Let m = r - t + 1 be the number of rounds left.
- Let k be the number of opponents who cooperated in the previous round.
- Let q = k / (n - 1), with q = 0 if the previous round is unavailable.
- Using the current stock S, compute the predicted remaining stock if you defect or cooperate while opponents repeat the last observed cooperation rate:

  - If you defect:
    - x_D = S · k / (2n)

  - If you cooperate:
    - x_C = S · (k + 1) / (2n)

- Set the reserve threshold:
  - τ = capacity / 2 if m ≥ 3
  - τ = capacity / 3 if m = 2
  - τ = 0 if m = 1

Decision rule:
- If x_D ≥ τ, defect.
- Else if x_C ≥ τ, cooperate.
- Else defect.

Edge cases:
- If S = 0, defect.
- If n = 2, then k is either 0 or 1; apply the same formulas directly.
- In the final round, always defect.
- If repeated defection has driven the stock near zero, keep defecting; there is no recovery advantage worth sacrificing current payoff for in the last round, and only preserve stock when it protects substantial future extraction.
'''

description_SELFISH_14 = '''
Maintain two variables from the previous round: `m`, the number of opponents who cooperated, and `S`, the current stock.

```text
if t == 1:
    play C

else if t >= r-1:
    play D

else if S <= capacity/2:
    play D

else if m == n-1:
    play C

else if m == n-2 and S >= 3*capacity/4:
    play C

else:
    play D
```

Update rule for the next round:
- Record the new stock `S`
- Record the new opponent cooperation count `m`

Behavioral intent:
- Start by cooperating to keep the pool intact and reveal whether others are also willing to sustain it.
- Keep cooperating only when the pool is still healthy and the observed cooperation level is near-universal.
- The moment cooperation drops by more than one opponent, or the stock slips below half capacity, switch to defection.
- In the last two rounds, always defect.
- If the pool ever recovers to a high level and the opponents return to near-full cooperation, resume cooperation until the next sign of weakness.
'''

description_SELFISH_15 = '''
Initialize by cooperating in round 1.

For each round t > 1:

- Let `k` be the number of opponents who cooperated in round `t-1`.
- Let `phi = k / (n - 1)` be the observed cooperation rate among opponents.
- Let `S` be the current stock at the start of round `t`.

Decision rule:
- If `t >= r - 1`, play `D`.
- Else if `S <= capacity / 3`, play `C`.
- Else if `phi >= 1/2`, play `C`.
- Else play `D`.

Equivalent pseudocode:

```text
if t == 1:
    action = C
else if t >= r - 1:
    action = D
else if stock <= capacity / 3:
    action = C
else if opponents_cooperated_last_round >= ceil((n - 1)/2):
    action = C
else:
    action = D
```

Edge handling:
- If `n = 2`, `phi` is just whether the single opponent cooperated last round.
- If the last observed round had no opponents cooperating, defect immediately unless `stock <= capacity / 3`.
- If `stock` is extremely low, keep cooperating until it rises above `capacity / 3`; then revert to the cooperation-frequency test.
- In the last two rounds, defect regardless of history.
'''

description_SELFISH_16 = '''
Initialize:
- Set `q = 1` as the prior estimate of opponent cooperation rate.
- Set `mode = exploit`.

After each round, observe `m` = number of opponents who cooperated.

Update:
- `q <- 0.7 * q + 0.3 * (m / (n - 1))`
- Reconstruct current stock exactly from the observed past actions and the known dynamics.

Decision rule for round `t` with current stock `S` and `remaining = r - t + 1`:

1. If `remaining == 1`:
   - Play `D`.

2. If `remaining == 2`:
   - Compute the expected payoff of `C` and `D` using `q` for the other players’ next-round behavior.
   - Choose the action with the higher value.
   - If the values are equal, play `D`.

3. If `remaining > 2`:
   - Let `cooperation_level = m / (n - 1)` from the last observed round.
   - If `S >= 0.6 * capacity` and `cooperation_level >= 1 - 2/(n - 1)`:
     - Play `D`.
   - Else if `S >= 0.35 * capacity`:
     - Play `D` only if `q >= 0.9`.
     - Otherwise play `C`.
   - Else:
     - Play `C` until `S` rises back to at least `0.5 * capacity`.

Startup rule:
- In round 1, play `D` unless `n` is very small and the capacity is already near the lower bound; otherwise default to `D`.

Persistence rule:
- If the last two observed rounds both had opponent cooperation below `0.7`, switch immediately to `C` until stock recovery is clear.
- If the last two observed rounds both had opponent cooperation above `0.9`, return to `D`.

Tie-breaking:
- Whenever two actions look equally good under the current estimate, choose `D`.

State-based simplification:
- Treat high stock as permission to exploit.
- Treat low stock as a signal to briefly cooperate just enough to rebuild the pool, then return to defection.

Memory:
- Use only the most recent observed round plus the exponentially smoothed cooperation estimate `q`.
- Do not condition on identities of cooperators, only on counts.
'''

description_SELFISH_17 = '''
Round 1: play D.

For rounds 2 through r-1:
- Let S be the current stock.
- Let k be the number of opponents who cooperated in the previous round.
- Compute the smallest total number of cooperators needed to keep the stock at the ceiling next round:
  - m* = ceil(n * capacity / S)
  - Clamp m* to the range [0, n]
- Play C only if:
  - k < m* and k + 1 >= m*
  - equivalently, your cooperation is pivotal for hitting the preservation threshold
- Otherwise play D.

Last round: play D.

Edge cases:
- If S = 0, play D.
- If S is so large that m* ≤ 1, play C only if a single cooperator is enough to preserve the stock; otherwise play D.
- If observed k is missing or inconsistent, default to D.

Behavioral rule in plain language:
- Defect by default.
- Cooperate only when the previous round shows that one more cooperator is enough to keep the resource from falling below the self-preserving level.
- Never cooperate in the final round.
'''

description_SELFISH_18 = '''
Round 1: cooperate.

For each later round, observe:
- `S` = current stock
- `h` = number of opponents who cooperated in the previous round
- `m = n - 1`
- `q = h / m` if `m > 0`

Decision rule:

1. If `S <= capacity / 2`, cooperate.
2. Else if `rounds_left <= 2`, defect.
3. Else if `q >= 2/3` and `S >= 3 * capacity / 4`, defect.
4. Otherwise, cooperate.

Update logic:
- If the previous round produced very high opponent cooperation, treat it as a signal that defecting now is profitable because the stock is likely to stay high.
- If the stock is at or below the midpoint, switch to cooperation to keep the resource from collapsing.
- If the game is near the end, stop investing in the future and take the larger immediate extraction.

Edge cases:
- If `n = 2`, replace `q >= 2/3` with `h = 1`.
- If `h` is unavailable for the first round, use cooperation.
- If `S` is exactly `capacity / 2`, cooperate.
- If `S` is exactly `3 * capacity / 4`, defect only when `q >= 2/3`.

Equivalent compact form:

```text
if round == 1:
    C
else if S <= capacity/2:
    C
else if rounds_left <= 2:
    D
else if opponents_coop_prev / (n-1) >= 2/3 and S >= 3*capacity/4:
    D
else:
    C
```
'''

description_SELFISH_19 = '''
- Round 1: defect.
- Round r: defect.

- For rounds 2 through r−1, compute:
  - `c =` number of opponents who cooperated in the previous round
  - `q = c / (n - 1)` if `n > 2`
  - for `n = 2`, `q = 1` if the other player cooperated, else `0`

- Maintain a running streak `good_streak`:
  - increment it by 1 if `q >= 0.8`
  - reset it to 0 otherwise

- Cooperate only when all of the following hold:
  1. current stock `S` is in the middle band: `capacity / 3 <= S <= 2 * capacity / 3`
  2. the previous round was strongly restrained: `q >= 0.8`
  3. restraint has been sustained: `good_streak >= 2`
  4. this is not the final round

- Emergency recovery clause:
  - if `S <= capacity / 4`, cooperate only if `q = 1` in the previous round
  - otherwise defect

- Default action in every other case: defect

- Tie-breaking:
  - if a condition is exactly on the boundary, treat it as satisfied only when it is `>=`, never when it is merely close
  - if the history is too short to compute a streak, treat `good_streak = 0`

- Behavior by phase:
  - early game: defect until the opponents have shown repeated restraint
  - mid game: cooperate only in sustained high-cooperation states that keep the stock productive
  - late game: defect unless the emergency recovery clause is triggered

- Selfish mode:
  - never cooperate just to be nice
  - cooperate only when the observed behavior of others makes it likely that restraint preserves enough future stock to matter
  - if opponents stop cooperating, switch back to permanent defection immediately
'''

description_SELFISH_20 = '''
Maintain a simple binary mode based on the last observed round.

State kept:
- `mode ∈ {coop, defect}` initialized to `coop`
- `last_k` = number of opponents who cooperated in the previous round

Decision rule each round `t`:

1. **Round 1**
   - Play `C`
   - Set `mode = coop`

2. **Rounds 2 through r−1**
   - If `stock <= capacity/3`, play `D` and set `mode = defect`
   - Else if `last_k >= ceil(3(n-1)/4)`, play `C` and set `mode = coop`
   - Else play `D` and set `mode = defect`

3. **Round r**
   - Play `D`

Update after each round:
- Record the observed number of cooperating opponents as `last_k`
- No other history is needed

Edge handling:
- If `n = 2`, then `ceil(3(n-1)/4) = 1`, so cooperate only when the single opponent cooperated last round and stock is above `capacity/3`
- If `stock` is exactly on a threshold, use the action on the lower branch (`D` at `capacity/3`, `C` at the cooperation threshold only when the inequality is met)
- If the stock ever falls to `0`, play `D` for all remaining rounds

Selfish rule summary:
- Cooperate only while the pool is still healthy and the other players are mostly cooperating
- Defect immediately when the pool is thin or cooperation drops
- Defect in the final round to take the full current-round amount without paying any future cost
'''

description_SELFISH_21 = '''
- Round 1:
  - If `r = 2`, play `D`.
  - If `r > 2`, play `C`.

- For rounds `t = 2, ..., r - 1`:
  - Let `m` be the number of opponents who cooperated in round `t - 1`.
  - Let `ρ = m / (n - 1)` be the observed cooperation rate among opponents.
  - Play `C` only if both of the following hold:
    - current stock `S` is at or below `capacity / 2`
    - `ρ >= 1/2`
  - Otherwise play `D`.

- Final round:
  - Play `D`.

- Edge handling:
  - If `n = 2`, then `ρ` is either `0` or `1`; treat `ρ >= 1/2` as “the other player cooperated.”
  - If the stock is very low, still require `ρ >= 1/2` before cooperating; never cooperate into a mostly-defecting population.
  - If the stock is high, defect and take the larger immediate share.

- Compact pseudocode:

```text
if t == 1:
    if r == 2: action = D
    else: action = C
elif t == r:
    action = D
else:
    m = opponents_cooperated_last_round
    rho = m / (n - 1)
    if S <= capacity / 2 and rho >= 1/2:
        action = C
    else:
        action = D
```
'''

description_SELFISH_22 = '''
Use a conservative exploit-and-preserve rule:

- Let `m = r - t + 1` be the number of rounds left including the current one.
- Let `q = (number of opponents who cooperated in the previous round) / (n - 1)`.
- Let `x = stock / capacity`.

Decision rule:

1. **Last two rounds:** play `D` whenever `m <= 2`.

2. **First round:**
   - Play `C` if `r >= 6`.
   - Otherwise play `D`.

3. **Later rounds (`m > 2` and `t > 1`):**
   - Play `D` if `x < 0.40`.
   - Play `D` if `q < 0.50`.
   - Play `C` if `q >= 0.75` and `x >= 0.60`.
   - Play `C` if `q >= 0.50`, `x >= 0.80`, and `m >= 4`.
   - Otherwise play `D`.

4. **After a round with unanimous or near-unanimous cooperation (`q >= 0.80`):**
   - Keep playing `C` as long as `x >= 0.70` and `m > 2`.
   - Switch immediately to `D` if the observed cooperation rate drops below `0.75` or stock falls below `0.70`.

5. **After a round with weak cooperation (`q < 0.50`):**
   - Play `D` until either:
     - `q >= 0.70` again, or
     - the stock recovers to `x >= 0.80`,
   - then re-enter the cooperation rule above.

6. **If no prior observation is available beyond the first round:**
   - Treat the previous cooperation rate as `q = 1` only in round 1.
   - From round 2 onward, use the actual observed count.

Pseudocode:

```text
if m <= 2:
    action = D
else if t == 1:
    action = C if r >= 6 else D
else:
    if x < 0.40 or q < 0.50:
        action = D
    else if q >= 0.75 and x >= 0.60:
        action = C
    else if q >= 0.50 and x >= 0.80 and m >= 4:
        action = C
    else:
        action = D
```
'''

description_SELFISH_23 = '''
Maintain an internal estimate of opponent cooperation and use a stock-preservation threshold.

State variables:
- `q_hat`: smoothed estimate of the fraction of opponents who cooperated last round
- `t`: current round index, starting at 1

Initialization:
- Set `q_hat = 1/2`

Each round `t`:

1. Observe current stock `S`.
2. Compute the observed opponent cooperation rate from the previous round:
   - if no previous round: use `q_obs = 1/2`
   - otherwise `q_obs = (number of opponents who cooperated last round) / (n - 1)`
3. Update the estimate:
   - `q_hat = 0.7 * q_obs + 0.3 * q_hat`

4. Convert the estimate into an expected number of cooperating opponents:
   - `y = round((n - 1) * q_hat)`

5. Predict the next stock under each action:

```text
remaining_if_C = S * (y + 1) / (2n)
remaining_if_D = S * y / (2n)

next_stock(x) = min( x + 2*x*(1 - x/capacity), capacity )
R_C = next_stock(remaining_if_C)
R_D = next_stock(remaining_if_D)
```

6. Set a declining reserve target:
   - `reserve = capacity * (r - t) / (2 * (r - 1))`
   - clamp to `[0, capacity/2]`

7. Choose action:
   - play `C` if `R_D < reserve` and `R_C >= reserve`
   - otherwise play `D`

8. Last round:
   - always play `D`

Behavioral edge cases:
- If `n = 2`, the same rule applies with `y` equal to the single opponent’s estimated cooperation tendency.
- If the estimate is unstable early on, the default bias is toward `D` unless cooperation is needed to keep the predicted next stock above the reserve.
- If current stock is already very low, cooperate only when the predicted next stock from defecting would fall below the reserve and cooperation is enough to keep it above it; otherwise defect.
'''

description_SELFISH_24 = '''
Round 1:
- Play C.

For round t > 1:
- Let c be the number of opponents who cooperated in round t − 1.
- Let S be the current stock.

Decision rule:
- If t = r: play D.
- Else if c ≥ n − 2: play D.
- Else if S ≤ capacity / 2: play C.
- Else play D.

Tie/edge handling:
- If c is unavailable, treat the first round as C.
- If S is exactly capacity / 2, treat it as the low-stock case and play C unless t = r or c ≥ n − 2.
- If the game ever reaches S = 0, play D for the rest of the game.

Behavioral meaning:
- Harvest aggressively whenever the other players are already keeping the pool near the sustainable zone.
- Switch to cooperation only when the pool has fallen to the recovery threshold and the recent behavior of others suggests that rebuilding is still plausible.
- In the final round, always take the larger immediate share.
'''

description_SELFISH_25 = '''
Initialize `trust = 0`.

For each round `t` with current stock `S` and `L = r - t + 1` rounds left:

1. **Last round**
   - If `L == 1`, play `D`.

2. **Update from the previous round**
   - Let `c` be the number of opponents who cooperated last round.
   - Update
     `trust = 0.7 * trust + 0.3 * (c / (n - 1))`
   - On the first round, use `trust = 0`.

3. **Defection trigger**
   - Play `D` if any of the following holds:
     - `trust < 1 - 1/n`
     - `S < capacity / 2`
     - `c <= n - 3` in the previous round
     - the previous round’s stock fell below `capacity / 2`

4. **Cooperation rule**
   - Otherwise, play `C`.

5. **First round**
   - Play `D`.

6. **Persistent fallback**
   - After any round in which fewer than `n - 2` opponents cooperated, set `trust = 0` and defect until two consecutive rounds again satisfy:
     - at least `n - 2` opponents cooperated
     - `S >= capacity / 2`

7. **State-based refinement**
   - If `S >= 0.9 * capacity` and `trust == 1`, you may cooperate even when `L > 1` is small.
   - If `S <= capacity / 2`, always defect.
   - If `S` is rising and `trust` remains at least `1 - 1/n`, continue cooperating; otherwise defect immediately.

8. **Anonymous-opponent adaptation**
   - Use only the count of cooperating opponents, never identities.
   - Treat one-round drops in cooperation as insufficient to forgive; require two consecutive high-cooperation rounds before returning to `C`.
'''

description_SELFISH_26 = '''
Round 1: play D.

For round t > 1, let k be the number of opponents who cooperated in round t - 1, let S be the current stock, and let m = r - t + 1 be the rounds remaining including the current one.

Compute:
- `R_C = S * (k + 1) / (2n)`  if you cooperate
- `R_D = S * k / (2n)`        if you defect
- `N_C = min(3 * R_C - 2 * R_C^2 / capacity, capacity)`
- `N_D = min(3 * R_D - 2 * R_D^2 / capacity, capacity)`

Decision rule:
- If `m == 1`, play D.
- Else play C only when the future stock gain from cooperating is large enough to justify the immediate loss:
  - play `C` if `(m - 1) * (N_C - N_D) > S / (2n)`
  - otherwise play `D`

Short-cut version:
- If opponents were highly cooperative last round, cooperate only when the stock-preservation benefit is strong enough to pay back over the remaining rounds.
- If opponent cooperation was weak or mixed, defect.

Edge handling:
- If `S == 0`, play D.
- If `k == 0`, play D.
- If `k == n - 1` and there are many rounds left, the formula will often select C; otherwise it stays with D.
- On the final round, always defect.
'''

description_SELFISH_27 = '''
Round 1: defect.

After each round, compute:
- `c =` number of opponents who cooperated last round
- `d = (n - 1) - c`
- `x = stock / capacity` at the start of the round

Choose a target action from the observed behavior:

- If `c = n - 1`, cooperate.
- If `c = 0`, defect.
- Otherwise, cooperate only when the stock is high enough that cooperation is locally cheap and the group is already leaning cooperative:
  - cooperate if `x ≥ 2/3` and `c ≥ d`
  - otherwise defect.

More compactly:

```text
if t = 1:
    play D
else:
    observe c and current stock S
    x = S / capacity

    if c == n-1:
        play C
    else if c == 0:
        play D
    else if x >= 2/3 and c >= (n-1)/2:
        play C
    else:
        play D
```

Last-round rule:
- On the final round, defect unless all opponents cooperated in the previous round and the current stock is still very high (`x ≥ 2/3`). In that single case, cooperate.

Recovery rule after a cooperative round:
- If you cooperated last round and at least one opponent defected, defect next round regardless of stock unless `c = n - 1`.
- If you cooperated last round and all opponents cooperated, continue cooperating while all opponents keep cooperating and `x ≥ 2/3`; otherwise switch to defect.

Persistence rule:
- Once the observed number of cooperating opponents falls to at most half of them, defect until cooperation returns to unanimity or the stock rises back above `2/3` with a majority of cooperators.

State-free fallback:
- If you cannot determine the exact current stock, use only the observed cooperation count:
  - cooperate only after unanimous cooperation by all opponents in the previous round;
  - otherwise defect.

This keeps cooperation strictly conditional on strong evidence of mutual cooperation, while defaulting to defection whenever the opponents are mixed, uncooperative, or the game is nearing depletion.
'''

description_SELFISH_28 = '''
Use a stock-preserving threshold strategy with conditional defection.

Let:
- `S` be the current stock at the start of the round
- `k` be the number of cooperating opponents observed in the previous round
- `m = n - 1` be the number of opponents
- `c = k / m` be the observed opponent cooperation rate in the previous round

Decision rule for round 1:
- Play `C` if `capacity >= 2n` and `r > 1`; otherwise play `D` in the final round only case.
- More generally, in round 1 play `C` unless the initial stock is already near collapse: if `capacity <= 2n`, play `D`; otherwise play `C`.

Decision rule for rounds `t = 2, ..., r-1`:
1. Compute the post-round stock that would result if you play `C`:
   - `S_C = min( 2*(S - S/(2n)) * (1 - (S - S/(2n))/capacity ) + (S - S/(2n)), capacity )`
2. Compute the post-round stock that would result if you play `D`:
   - `S_D = min( 2*(S - S/n) * (1 - (S - S/n)/capacity ) + (S - S/n), capacity )`
3. Estimate opponent behavior for the next round from the last round:
   - If `c >= (n-2)/(n-1)`, treat opponents as mostly cooperative.
   - If `c < (n-2)/(n-1)`, treat opponents as not cooperative enough.
4. Choose:
   - Play `C` if both of the following hold:
     - `S_C >= S`, and
     - `c >= (n-2)/(n-1)`
   - Otherwise play `D`

Equivalent simpler rule:
- Cooperate only when cooperation is likely to keep the stock at least as healthy as defection and opponents were sufficiently cooperative in the previous round.
- Defect whenever opponents were not sufficiently cooperative, or whenever defecting preserves at least as much future stock as cooperating.

Final round `t = r`:
- Play `D` unconditionally.

Fallback rules:
- If the observed stock is very low (`S <= 2n`), play `D`.
- If the observed stock is exactly zero, play `D`.
- If the previous-round cooperation count is unavailable, use round-1 logic: play `C` unless `S <= 2n`.

Compact pseudocode:

```text
if t == r:
    action = D
else if t == 1:
    action = C if capacity > 2n else D
else:
    c = k / (n - 1)

    S_after_C = S - S/(2n)
    S_after_D = S - S/n

    S_next_C = min(S_after_C + 2*S_after_C*(1 - S_after_C/capacity), capacity)
    S_next_D = min(S_after_D + 2*S_after_D*(1 - S_after_D/capacity), capacity)

    if S <= 2n:
        action = D
    else if c >= (n-2)/(n-1) and S_next_C >= S_next_D:
        action = C
    else:
        action = D
```

Behavioral principle:
- Start cooperative only when the stock can sustain it.
- Continue cooperating only when the group is behaving cooperatively enough to keep future stock high.
- Switch to defection immediately after any meaningful deterioration in opponent cooperation.
- Take the guaranteed immediate advantage in the last round.
'''

description_SELFISH_29 = '''
Round 1: defect.

For every round t = 2, ..., r:

1. Let S be the current stock.
2. Let x be the number of opponents who cooperated in round t−1.

Choose:

- **Defect** if t = r.
- Otherwise, **cooperate** only when both conditions hold:
  - the previous round showed broad cooperation:  
    `x >= ceil((n - 1) / 2)`
  - the current stock is not comfortably high:  
    `S <= 2 * capacity / 3`

- In all other cases, **defect**.

Equivalent decision rule:

```text
if t == 1:
    D
elif t == r:
    D
elif x >= ceil((n-1)/2) and S <= 2*capacity/3:
    C
else:
    D
```

Edge handling:

- If last round is reached, always defect.
- If the previous round had very low cooperation, keep defecting.
- If the stock is already high, defect even when others cooperated, since preserving the option to extract more later is preferable.
- If cooperation among opponents is strong and the stock has started to fall, switch to cooperation to keep the pool productive while still taking the higher payoff from a well-maintained stock.
'''

description_SELFISH_30 = '''
Maintain an estimate `p` of the fraction of opponents who cooperate, initialized to `1`.

For round `t = 1..r` with current stock `S`:

1. Let `m = r - t + 1` be the number of rounds left including this one.
2. Let `q = (observed_cooperators_last_round / (n - 1))` if a previous round exists; otherwise `q = 1`.
3. Update the estimate:
   `p = 0.7 * p + 0.3 * q`
4. Set the expected number of cooperating opponents next round to:
   `o = (n - 1) * p`
5. For each possible action `a ∈ {C, D}`:
   - `self_consumption = S / (2n)` if `a = C`, else `S / n`
   - `total_cooperators = o + 1` if `a = C`, else `o`
   - `remaining_after_consumption = S * total_cooperators / (2n)`
   - `next_stock = min(remaining_after_consumption + 2 * remaining_after_consumption * (1 - remaining_after_consumption / capacity), capacity)`
   - `score(a) = self_consumption + ((m - 1) / (2n)) * next_stock`
6. Play the action with the higher `score`.

Tie-breaking:
- If `score(C) == score(D)`, play `D`.

Hard edge rules:
- On the final round, always play `D`.
- If `S` is so low that both actions produce essentially the same `next_stock` after rounding, play `D`.
- If the previous round had zero opponent cooperators, set `p = 0` immediately and keep playing `D` until opponent cooperation reappears.

Behavioral cutoff:
- If the observed opponent cooperation rate in the last round is at least `1/2`, the strategy is willing to cooperate when the projected stock gain from doing so is large enough.
- If it is below `1/2`, the strategy defects unless cooperation is clearly better by the score above.

This is a selfish rule: default to `D`, switch to `C` only when cooperation is expected to preserve enough stock to raise future personal payoff more than the immediate gain from defecting.
'''

description_SELFISH_31 = '''
Use a state-based greedy policy with a simple retaliation-and-recovery rule.

Let:
- `S` = current stock at the start of the round
- `k` = number of opponents who cooperated in the previous round
- `m = n - 1` = number of opponents
- `c_prev = k / m` = observed cooperation rate among opponents in the previous round

Decision rule each round:

1. **First round**
   - Play `C` if `n = 2`.
   - Otherwise play `D`.

2. **From round 2 onward**
   - Compute the expected stock next round under full cooperation among all players:
     - If all players play `C`, each player consumes `S/(2n)`, so remaining stock is `S/2`, and next stock is `g(S/2)` where `g(x) = min(x + 2x(1 - x/capacity), capacity)`.
   - Cooperate only if both conditions hold:
     - `S` is high enough that cooperating preserves a large future stock:
       - `S >= capacity / 2`
     - Opponents were sufficiently cooperative in the previous round:
       - `c_prev >= 1 - 1/n`
   - Otherwise play `D`.

3. **Last round**
   - Play `D`.

4. **Two-round adaptation**
   - If the previous round was strongly cooperative, meaning `k = m`, and `S >= capacity / 2`, play `C`.
   - If the previous round had any defection, play `D` unless `S` is extremely high:
     - cooperate only if `S = capacity` and `k = m`.

5. **Fallback threshold form**
   - Define:
     - `T = capacity / 2`
     - `q = 1 - 1/n`
   - Then:
     - `play C` iff `t < r`, `S >= T`, and `c_prev >= q`
     - otherwise `play D`

6. **If no previous observation is available**
   - Treat the previous cooperation rate as `0` unless it is the first round.
   - So after any unobserved or invalid history state, default to `D`.

7. **Selfish tie-breaking**
   - When the rule is exactly on the boundary, choose `D`.
   - Never cooperate as a “signal” or to build trust unless the current state already makes cooperation at least as favorable as defection under the rule above.

Compact pseudocode:

```text
if t == r:
    action = D
else if t == 1:
    action = (n == 2 ? C : D)
else:
    c_prev = k / (n - 1)
    if S >= capacity / 2 and c_prev >= 1 - 1/n:
        action = C
    else:
        action = D
```
'''

description_SELFISH_32 = '''
Initialize an estimate of opponent cooperation rate:

- For round 1, set `q = 1/2`.
- After round `t-1`, update `q` with exponential smoothing:
  - `q := (q + observed_opponent_cooperation_fraction_last_round) / 2`
  - where `observed_opponent_cooperation_fraction_last_round = (# opponents who cooperated) / (n - 1)`

At round `t` with current stock `S`:

1. If `t = r`, play `D`.

2. Let `m = r - t` be the number of future rounds after this one.
   Set the continuation weight:
   - `beta = m / (m + 1)`

3. Let `x = (n - 1) * q` be the expected number of cooperating opponents.

4. Predict next-round stock under each action:

   - If you cooperate:
     - `R_C = S * (1 + x) / (2n)`
   - If you defect:
     - `R_D = S * x / (2n)`

   Convert remaining stock to next-round stock after regrowth:
   - `F(R) = min(3*R - 2*R*R / capacity, capacity)`

   So:
   - `S_C_next = F(R_C)`
   - `S_D_next = F(R_D)`

5. Compute action scores:
   - `score_C = S / (2n) + beta * S_C_next / (2n)`
   - `score_D = S / n + beta * S_D_next / (2n)`

6. Play:
   - `C` if `score_C > score_D`
   - `D` otherwise

Edge handling:

- If `n = 2`, then `q` is just the single opponent’s observed cooperation frequency.
- If the last observed round had zero cooperating opponents, set `q = 0`.
- If the last observed round had all opponents cooperating, set `q = 1`.
- If the score comparison is extremely close, choose `D`.

Fallback simplification:

- Cooperate only when both conditions hold:
  - the estimated opponent cooperation rate is high enough that `q >= 1/2`, and
  - the current stock is not already near collapse, specifically `S >= capacity / 2`
- Otherwise defect.

Round-by-round behavior:

- Early rounds: use the score rule above.
- Middle rounds: continue only when observed cooperation keeps the stock high enough to make preservation worthwhile.
- Final rounds: defect, with the last round always defecting.
'''

description_SELFINTERESTED_5 = '''
- **Track two signals each round:** current stock `S` and the number of opponents who cooperated last round `k_last`.

- **Round 1:**  
  Play **D**.

- **Last round:**  
  Always play **D**.

- **Middle rounds:**  
  Compute the minimum cooperation level needed to justify staying cooperative:
  `k_req = ceil((n - 1) / 2)`

  Then apply:

  **Play C** if all of the following hold:
  1. `S >= 0.75 * capacity`
  2. `k_last >= k_req`
  3. In the previous round, stock did not drop sharply: `S_prev - S <= 0.25 * capacity`

  **Otherwise play D**.

- **Extra stabilization rule:**  
  If you played **C** last round and the stock increased or stayed near capacity, keep cooperating only if the same three conditions still hold. If any condition fails once, switch to **D** immediately and stay with **D** until cooperation in the population rebounds.

- **Update logic after each round:**  
  - If the observed number of cooperators is high enough and stock remains healthy, continue cooperating.
  - If cooperation falls below threshold, or stock is being depleted too quickly, defect.
  - If stock falls very low, defect until stock recovers to the high-stock region.

- **Compact pseudocode:**
  ```text
  if round == 1 or round == r:
      action = D
  else:
      if S >= 0.75*capacity and k_last >= ceil((n-1)/2) and (S_prev - S) <= 0.25*capacity:
          action = C
      else:
          action = D
  ```

- **Tie-break rule for borderline cases:**  
  When `S` or `k_last` is exactly on the threshold, choose **D**.
'''

description_SELFINTERESTED_6 = '''
State variables to track:
- `t`: current round
- `S`: current stock at the start of round `t`
- `k`: number of opponents who cooperated in the previous round
- `k_prev`: number of opponents who cooperated two rounds ago

Decision rule for round `t`:

1. If `t = r`, play `D`.
2. Else if `t = r - 1`, play `D`.
3. Else if `t = 1`, play `C`.
4. Else if `S <= capacity / 4`, play `D`.
5. Else if `k <= n - 3`, play `D`.
6. Else if `k = n - 2`:
   - play `C` only if `k_prev >= n - 2` and `S >= capacity / 2`;
   - otherwise play `D`.
7. Else if `k = n - 1`, play `C`.

Update rule after each round:
- Set `k_prev ← k`
- Observe the new `k` from the round that just ended
- Update `S` from the game state

Interpretation of the policy:
- Start with cooperation to test whether the group supports the resource.
- Continue cooperating only when the stock remains healthy and the observed cooperation level is near-universal.
- Defect immediately when cooperation drops below the near-universal threshold, or when the stock becomes low.
- Defect in the final two rounds, since there is no future stock value to protect.
'''

description_SELFINTERESTED_7 = '''
Round 1: play C.

For round t > 1, let k be the number of opponents who cooperated in round t-1.

Maintain a recent cooperation rate:
- If t = 2, use ρ = k / (n - 1)
- If t ≥ 3, use ρ = average of the opponent cooperation rates from rounds t-1 and t-2

Decision rule:

1. If t = r, play D.
2. If t = r - 1:
   - play C only if k = n - 1 and current stock ≥ 3·capacity/4
   - otherwise play D
3. If 2 ≤ t ≤ r - 2:
   - play C iff both conditions hold:
     - ρ ≥ 1/2
     - current stock ≥ capacity/2
   - otherwise play D

Tie-breaks and edge cases:
- If current stock is below capacity/3, play D regardless of history.
- If the previous round had zero opponent cooperators, play D in the next round.
- If the last two observed rounds are fully cooperative, keep playing C while stock stays at or above capacity/2.

State update used for the next round:
- After each round, store the observed opponent cooperation count and recompute ρ from the most recent rounds only.

This strategy starts by preserving the pool, cooperates only when the other players have recently been reliable and the stock is healthy, and switches to exploitation in the final rounds.
'''

description_SELFINTERESTED_8 = '''
Round 1:
- Play C.

After each round t, observe:
- k = number of opponents who played C
- S = current stock before your action next round

Define:
- expected stock if you play C next round and opponents keep the same behavior as last round:
  S_C = update(S, k, C)
- expected stock if you play D next round:
  S_D = update(S, k, D)

Decision rule for round t+1:
1. If S ≤ 2n:
   - Play C.
2. Else if k = n - 1:
   - Play C.
3. Else if k ≤ (n - 1) / 2:
   - Play D.
4. Else if S < capacity / 2:
   - Play C.
5. Else:
   - Play D.

Update function:
- Let total consumption under your action a be:
  cons(a) = k · (S / (2n)) + (n - 1 - k) · (S / n) + own_consumption(a)
  where own_consumption(C) = S / (2n), own_consumption(D) = S / n
- Then:
  S_remaining = max(0, S - cons(a))
  S_next = min(S_remaining + 2 · S_remaining · (1 - S_remaining / capacity), capacity)

Last round:
- Play D if S > 2n.
- Otherwise play C.

Tie-breaks and exact thresholds:
- When k = (n - 1) / 2, play C if S < capacity / 2; otherwise play D.
- When S = capacity / 2, follow the k-based rule above.
- If the stock is already very low, always choose C regardless of k.

Behavioral template:
- Cooperate when the pool is fragile or when the observed group cooperation is high enough to preserve future value.
- Defect when the group is already extracting heavily and the stock is safely above the midpoint.
- Revert immediately to cooperation after any round with near-universal cooperation or any round that leaves the stock near collapse.
'''

description_SELFINTERESTED_9 = '''
Initialize in build mode.

For round t with current stock S:

1. If t = r, play D.

2. If no previous round exists:
   - play C.

3. Let k be the number of opponents who cooperated in the previous round.
   Let q = k / (n - 1).

4. If currently in build mode:
   - play C
   - switch to harvest mode after the round if any of the following holds:
     - S <= capacity / 2
     - q < 1/2
     - stock did not increase in the previous transition

5. If currently in harvest mode:
   - play D
   - switch to build mode after the round only if both of the following hold:
     - S >= 3 * capacity / 4
     - q >= 3/4
   - and these conditions have held for two consecutive rounds

6. Forced recovery rule:
   - If S = 0, play C until S becomes positive again, then return to the mode determined above.

7. Collapse response:
   - If q = 0 in the previous round, play D for the next two rounds, then re-evaluate with the same rules.

8. Endgame tightening:
   - For the last two rounds, play D unless S > 3 * capacity / 4 and q = 1 in both of the two previous rounds, in which case play C in the penultimate round and D in the final round.

Decision rule summary:
- Cooperate only when the pool is healthy and the other players have recently been broadly cooperative.
- Defect whenever cooperation looks unstable, the pool is weak, or the game is ending.
- Use cooperation to rebuild stock; use defection to harvest whenever rebuilding is not clearly supported by observed behavior.
'''

description_SELFINTERESTED_10 = '''
- Round 1: play D.

- For rounds 2 through r-1, keep a running cooperation score based on the previous round:
  - Let `c` be the number of opponents who cooperated last round.
  - Let `q = ceil((n - 1) / 2)`.

- Play C only when both conditions hold:
  1. `c >= q`
  2. current stock `S <= capacity / 2`

- Otherwise play D.

- Round r: play D.

- If you want a slightly more cautious version, replace the single-round test with a two-round test:
  - Play C only if the last two rounds both had `c >= q` and `S <= capacity / 2`.
  - Otherwise play D.

- If the stock is very high (`S > 3 * capacity / 4`), always play D.

- If the stock is very low (`S < capacity / 4`), play C only if the previous round had at least one opponent cooperating; otherwise play D.

- Keep the policy memory-light and state-based:
  - favor D by default,
  - switch to C only when the observed group behavior is already sufficiently cooperative and the pool is in a range where restraint protects future payoffs,
  - revert to D immediately after any round with weak cooperation.
'''

description_SELFINTERESTED_11 = '''
Let `t` be the current round, `S` the current stock, `K` the number of opponents who cooperated in the previous round, and `R = r - t + 1` the number of rounds still including the current one.

Use this decision rule:

1. **Last round**
   - Play `D`.

2. **First round**
   - Play `C`.

3. **All other rounds**
   - Estimate opponent cooperation rate from the previous round:
     - `q = K / (n - 1)` if `n > 2`
     - if `n = 2`, then `q = 1` if the other player cooperated last round, else `0`
   - Predict how many total cooperators there will be under each action:
     - If you play `C`: `m_C = 1 + q (n - 1)`
     - If you play `D`: `m_D = q (n - 1)`
   - For any hypothesized total cooperation level `m`, compute:
     - `consumption(m) = S * (2n - m) / (2n)`
     - `remaining(m) = S - consumption(m) = S * m / (2n)`
     - `next_stock(m) = min( remaining(m) + 2 * remaining(m) * (1 - remaining(m) / capacity), capacity )`
   - Compute a self-interested score for each action:
     - `score(C) = S / (2n) + (R - 1) * next_stock(m_C) / capacity`
     - `score(D) = S / n + (R - 1) * next_stock(m_D) / capacity`
   - Play the action with the larger score.
   - If the scores are equal, play `D`.

Edge handling:

- If the previous-round cooperation count is unavailable in round 1, use `C`.
- If `S = 0`, play `D`.
- If `n = 2`, treat the opponent’s last observed action as the cooperation signal.
- If the computed score difference is tiny or exactly tied, choose `D`.
'''

description_SELFINTERESTED_12 = '''
Round 1: play C.

After each round, compute:
- `m =` number of opponents who cooperated in that round
- `q = m / (n - 1)` = observed opponent cooperation rate
- `h =` running trust score, initialized to `1`, updated after each round by  
  `h := 0.7*h + 0.3*q`

Decision rule for round `t`:

1. If `t = r`, play D.
2. Else if `stock <= capacity / 4`, play C.
3. Else if `h >= 0.6`, play C.
4. Else if `h <= 0.4`, play D.
5. Else:
   - play C if `q >= 1/2`
   - otherwise play D

State response rules:
- If the previous round had `q = 0`, set `h := 0` immediately before the next decision.
- If the previous round had `q = 1`, set `h := 1` immediately before the next decision.
- If stock has been at or below `capacity / 5` for two consecutive rounds, force C until stock rises above `capacity / 3`.
- If stock has stayed at or above `3*capacity / 4` for two consecutive rounds and `h < 0.5`, play D until `h >= 0.5`.

Implementation form:

```text
if round == 1:
    action = C
elif round == r:
    action = D
else:
    update h from last round’s observed q
    if stock <= capacity/4:
        action = C
    elif h >= 0.6:
        action = C
    elif h <= 0.4:
        action = D
    else:
        action = C if q >= 0.5 else D
```

This keeps cooperation when the pool is being preserved, switches to defection when others are consistently extracting, rebuilds the stock when it gets low, and takes the full remaining payoff in the final round.
'''

description_SELFINTERESTED_13 = '''
Maintain a cooperation score and play by a stock-preservation threshold.

Let:

- `t` = current round
- `S` = current stock
- `k` = number of opponents who cooperated in the previous round
- `q = k / (n - 1)` for `n > 1`
- `q̄` = average opponent cooperation rate over the last up to 3 observed rounds, using `q` when fewer than 3 are available

Define two forecasted next-stock values for the current round:

- If I play `C`, then `c = k + 1`
- If I play `D`, then `c = k`

For either choice `c`, compute:

- `R(c) = S * c / (2n)`
- `N(c) = min(3 * R(c) - 2 * R(c)^2 / capacity, capacity)`

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Last round (`t = r`)**
   - Play `D`.

3. **Otherwise**
   - Compute `N(C)` and `N(D)`.
   - Let `P = 1` if `q̄ >= 0.75`, else `0`.

   Play `C` if all of the following hold:
   - `S >= 0.6 * capacity`
   - `q̄ >= 0.75`
   - `N(C) >= 0.5 * capacity`
   - `N(C) >= N(D) + 0.1 * capacity / r`

   In every other case, play `D`.

State update for the score after each round:

- Add the observed cooperation rate `q` to the rolling window of the last 3 rounds.
- If `q < 0.5` in any round, set `q̄` to that low value immediately for the next round.
- If the stock ever falls below `0.4 * capacity`, ignore the rolling average and require `q̄ >= 0.85` and `S >= 0.7 * capacity` before cooperating again.

Edge handling:

- If `n = 2`, use `q = 1` when the other player cooperated and `0` otherwise; the same rules apply.
- If there is no previous round yet, treat `q̄ = 1`.
- If `S = 0`, play `D` unless the current round is the last round.
- If `S = capacity` and `q̄ = 1`, still play `D` on the final round and `C` only in earlier rounds when the forecasted next stock under `C` is strictly higher than under `D` by the margin above.

Compact form:

```text
if t == 1: play C
else if t == r: play D
else:
    if recent cooperation is strong and stock is high and C keeps next stock safely high:
        play C
    else:
        play D
```
'''

description_SELFINTERESTED_14 = '''
Maintain `coop_rate`, the exponentially weighted average of the observed fraction of opponents who cooperated in previous rounds:

- Initialize `coop_rate = 1`
- After each round with `k` cooperating opponents, update  
  `coop_rate ← 0.6 * coop_rate + 0.4 * (k / (n - 1))`

Decision rule in round `t` with current stock `S` and `ℓ = r - t + 1` rounds including this one:

1. If `ℓ = 1`, play `D`.
2. Else if `t = 1`, play `C`.
3. Else if `ℓ = 2`, play `D`.
4. Else:
   - If `S >= capacity / 2` and `coop_rate >= 1/2`, play `C`
   - Else if `S >= 3 * capacity / 4` and `coop_rate >= 1/3`, play `C`
   - Else play `D`

Edge handling:
- If `n = 2`, then `coop_rate` is just the other player’s last observed cooperation indicator.
- If `n - 1 = 0` is impossible under the game setup, so no special case is needed.
- If `S = 0`, always play `D`.
- If the observed cooperation rate was exactly `1/2`, treat it as cooperation-friendly and follow the `C` branch only when `S >= capacity / 2`; otherwise `D`.
'''

description_SELFINTERESTED_15 = '''
Maintain an exponential moving estimate of opponents’ cooperation rate:

- `q = 1` before round 1
- After each round, update  
  `q ← 0.7*q + 0.3*(#opponents who cooperated)/(n-1)`

At the start of each round, let:

- `R` = rounds remaining including the current round
- `S` = current stock
- `k = round((n-1)*q)` = predicted number of cooperating opponents

Compute the projected remaining stock under each action:

- If I cooperate:  
  `rem_C = S - [k*(S/(2n)) + (n-1-k)*(S/n) + S/(2n)]`
- If I defect:  
  `rem_D = S - [k*(S/(2n)) + (n-1-k)*(S/n) + S/n]`

Decision rule:

1. **Last round:** play `D`.

2. **If `rem_D >= capacity/2`:** play `D`.

3. **Else if `rem_C >= capacity/2`:** play `C`.

4. **Else if `R <= 3`:** play `D` if `rem_D > 0`, otherwise play `C`.

5. **Otherwise:** play the action that gives the larger projected score  
   `score(action) = immediate_payoff(action) + ((R-1)/R) * next_stock(action)/(2n)`  
   where `next_stock(action) = min(rem_action + 2*rem_action*(1 - rem_action/capacity), capacity)`.

Behavioral interpretation:

- Start with cooperation only if it helps keep the pool in the replenishing range.
- Exploit with `D` whenever the pool is projected to stay healthy anyway.
- Switch to `C` as soon as defection would push the pool below the recovery threshold.
- In the final rounds, stop sacrificing immediate payoff for future stock and favor `D` unless it would collapse the pool outright.
'''

description_SELFINTERESTED_16 = '''
Maintain a trust score and use a stock-aware threshold rule.

State kept across rounds:
- `trust ∈ [0,1]`, initialized to `1`
- `last_coop_rate`, initialized to `1`

Update after each round:
- Let `coop_rate = (number of opponents who cooperated) / (n - 1)`
- Update `trust = 0.7 * trust + 0.3 * coop_rate`
- Set `last_coop_rate = coop_rate`

Decision rule each round with current stock `S` and rounds remaining `T`:

1. If `T = 1`, play `D`.
2. If `S <= 2n`, play `D`.
3. If `trust >= 0.75` and `S >= 0.9 * capacity`, play `C`.
4. If `trust >= 0.60` and `S >= 0.75 * capacity` and `T >= 3`, play `C`.
5. If `trust >= 0.45` and `last_coop_rate >= 0.5` and `S >= 0.8 * capacity`, play `C`.
6. Otherwise, play `D`.

First round:
- Play `C`.

Recovery rule after defection:
- If you have been defecting and then observe `coop_rate >= 0.75` for a round, immediately raise `trust` by setting `trust = min(1, trust + 0.2)`.

Persistent mode:
- Once `trust < 0.35`, stay with `D` until both:
  - `coop_rate >= 0.75` in the current round, and
  - `S >= 0.8 * capacity`

This produces:
- early cooperation when the stock is full,
- continued cooperation only when opponents are broadly cooperative,
- immediate defection when the stock is depleted or the game is ending,
- selective re-entry into cooperation after credible recovery by others.
'''

description_SELFINTERESTED_17 = '''
State variables:
- `S`: current stock at the start of the round
- `q`: number of opponents who cooperated in the previous round
- `t`: current round index

Decision rule:

```text
if t == r:
    play D

else if t == 1:
    play C

else if S <= capacity / 4:
    play D

else if q == n - 1 and S >= capacity / 2:
    play C

else if q >= n - 2 and S >= 3 * capacity / 4 and t <= r - 2:
    play C

else:
    play D
```

Memory update after each round:
- Record the observed opponent cooperation count `q`
- Keep using the current stock `S`

Edge handling:
- First round: cooperate
- Last round: defect
- If the stock has fallen to `0`, defect for the rest of the game
- If the stock is low (`<= capacity / 4`), defect until it recovers above `capacity / 2` and opponents return to near-full cooperation
- If opponents are consistently near-full cooperators and the stock is healthy, cooperate to preserve the stock path; otherwise defect

Update mode:
- Once you switch into the low-stock defecting condition, stay in it until both:
  - `S >= capacity / 2`, and
  - `q == n - 1`

This keeps cooperation conditional on visible restraint by the group, while defaulting to defection whenever the state or observed behavior suggests that preserving the pool is no longer being reciprocated.
'''

description_SELFINTERESTED_18 = '''
Use a threshold policy keyed to the current stock and the observed cooperation rate, with a short exploitation phase, a stability phase, and a shutdown phase.

Decision variables
- Let S be the current stock at the start of the round.
- Let k be the number of cooperating opponents observed in the previous round.
- Let p = k / (n - 1) be the observed opponent cooperation rate.
- Let t be the round number, starting at 1.
- Let last_stock be the stock after the previous round, if observed.

Round 1
- Play C.

After round 1, classify the opponent field from the observed cooperation rate:
- If p ≥ 0.8, label the field “high-cooperation”.
- If 0.3 ≤ p < 0.8, label the field “mixed”.
- If p < 0.3, label the field “low-cooperation”.

Core policy for round t ≥ 2
1. If S ≤ 2n, play D.
2. Else if t ≥ r - 1, play D.
3. Else if the field is “low-cooperation”, play D.
4. Else if the field is “mixed”:
   - Play C only if S ≥ 0.7 × capacity and p ≥ 0.5.
   - Otherwise play D.
5. Else if the field is “high-cooperation”:
   - Play C if both:
     - S ≥ 0.5 × capacity, and
     - p ≥ 0.8
   - Otherwise play D.

Adaptive update rule
- Recompute the field every round from the most recent observed p.
- If you played C in the previous round and the observed p dropped by at least 0.25 compared with the round before, switch immediately to D for the next round.
- If you played D in the previous round and p increased to at least 0.8 for two consecutive rounds, allow C again under the high-cooperation rule.

State-sensitive rule
- If the stock increased from last_stock to S, treat this as a positive signal and keep the current field classification.
- If the stock fell by at least 30% in one round, downgrade the field classification by one level:
  - high-cooperation → mixed
  - mixed → low-cooperation

Endgame rule
- In the final two rounds, always play D.
- In any round where S is low enough that a single cooperative move would materially accelerate depletion, play D.

Fallback rule
- If the observed cooperation count is unavailable for any round, default to D.
- If any inconsistency appears in the observed history, default to D for that round and all later rounds until two consecutive high-cooperation observations are restored.

Compact pseudocode
```text
if t == 1:
    action = C
else:
    if S <= 2n or t >= r-1:
        action = D
    else:
        p = k / (n-1)

        if previous_p exists and previous_p - p >= 0.25:
            action = D
        else:
            if p < 0.3:
                action = D
            elif p < 0.8:
                action = C if (S >= 0.7*capacity and p >= 0.5) else D
            else:
                action = C if (S >= 0.5*capacity) else D
```

This policy cooperates only under sustained, visible cooperation and sufficient stock, and otherwise defects.
'''

description_SELFINTERESTED_19 = '''
- Round 1: cooperate.

- For rounds 2 through r:
  - Let `o` be the number of opponents who cooperated in the previous round.
  - Let `T = ceil(3(n-1)/4)`.
  - Let `low = 0.4 * capacity` and `high = 0.7 * capacity`.

- Defect immediately if any of the following holds:
  - `t >= r-1`  
  - `stock < low`
  - `o < T - 1`

- Cooperate if all of the following hold:
  - `t < r-1`
  - `stock >= high`
  - `o >= T`

- Borderline case `o = T - 1`:
  - Cooperate only if `stock >= 0.85 * capacity` and the previous two rounds both satisfied `o >= T - 1`.
  - Otherwise defect.

- Recovery rule after defection:
  - If you defected in the previous round, return to cooperation only after two consecutive rounds with `o >= T` and `stock >= high`.
  - Until that condition is met, keep defecting.

- Endgame:
  - In the last two rounds, defect regardless of history or stock.

- Persistent mode:
  - Once `stock < low`, stay in defensive mode and defect unless the recovery rule is satisfied.
  - Once `o < T - 1`, treat the opponents as unreliable and defect until the recovery rule is satisfied.

- Special case `n = 2`:
  - Then `T = 1`; cooperate only if the other player cooperated in the previous round and `stock >= high`.
  - Otherwise defect.

'''

description_SELFINTERESTED_20 = '''
Maintain two running variables:

- `q̄`: exponentially smoothed estimate of opponent cooperation, initialized to `1`
- `mode`: one of `probe`, `build`, `harvest`

Update after each round with observed opponent cooperators `c`:

- `q = c / (n - 1)`
- `q̄ ← 0.7*q̄ + 0.3*q`

Decision rule for round `t`:

1. **Last round**
   - Play `D`.

2. **First round**
   - Play `C`.

3. **If current stock ratio is low**
   - Let `x = stock / capacity`.
   - If `x <= 0.25`:
     - Play `C` if `q̄ >= 0.5`
     - Otherwise play `D`

4. **If current stock ratio is moderate**
   - If `0.25 < x < 0.75`:
     - Play `C` if `q̄ >= 0.5`
     - Otherwise play `D`

5. **If current stock ratio is high**
   - If `x >= 0.75`:
     - Play `D` if `q̄ >= 0.25`
     - Otherwise play `C`

6. **Shock response**
   - If the previous round had `c = 0`, play `D` next round unless `x <= 0.15`, in which case play `C` once to try to rebuild.

7. **Recovery after a cooperative round**
   - If `c >= ceil((n - 1)/2)` and `x < 0.90`, play `C` for the next round unless the “last round” rule applies.

Pseudocode:

```text
if t == r:
    action = D
else if t == 1:
    action = C
else:
    q = c / (n - 1)
    q̄ = 0.7*q̄ + 0.3*q
    x = stock / capacity

    if c == 0:
        action = C if x <= 0.15 else D
    else if x <= 0.25:
        action = C if q̄ >= 0.5 else D
    else if x < 0.75:
        action = C if q̄ >= 0.5 else D
    else:
        action = D if q̄ >= 0.25 else C

    if c >= ceil((n - 1)/2) and x < 0.90:
        action = C
```

Behavioral intent:

- Start cooperatively to test the environment.
- Exploit high-stock periods when opponents are sufficiently cooperative.
- Rebuild stock when it is depleted and cooperation is at least moderate.
- Refuse to subsidize persistent widespread defection.
- Always defect in the final round.
'''

description_SELFINTERESTED_21 = '''
Round 1: cooperate.

For round t > 1, let k be the number of opponents who cooperated in round t − 1.

If t = r: defect.

Otherwise, compute the cooperation threshold
`θ = ceil((n - 1) * max(1/2, 1 - stock / capacity))`.

- If `k >= θ`, cooperate.
- If `k < θ`, defect.

Update rule for tied or borderline cases:
- If `stock >= 3 * capacity / 4` and `k >= ceil((n - 1) / 2)`, cooperate even if only barely above threshold.
- If `stock <= capacity / 4`, defect unless `k = n - 1`.
- If the previous round produced zero opponent cooperators, defect in the next round.
- If the previous round had all opponents cooperating and stock stayed at least half the capacity, cooperate again.

Behavioral memory:
- Keep a running average cooperation rate over all previous rounds, `q`.
- If `q >= 1/2`, use the threshold rule above as written.
- If `q < 1/2`, become stricter by replacing `θ` with `min(n - 1, θ + 1)`.

Endgame adjustment:
- In the final two rounds, defect unless all opponents cooperated in the immediately preceding round and stock is at least `capacity / 2`.
- In the last round, always defect.
'''

description_SELFINTERESTED_22 = '''
Round 1: cooperate.

Round r: defect.

For rounds t = 2 to r-1:

- Let `q` be the fraction of opponents who cooperated in round `t-1`.
- Let `qbar` be the average of `q` over the last two observed rounds, using only available data when fewer than two rounds have occurred.
- Let `S` be the current stock.
- Let `bad` mean either:
  - `q < 1/2`, or
  - `qbar < 1/2`, or
  - the stock fell in the previous round by more than `capacity/4`.

Decision rule:

1. If `bad` is true, defect.
2. Else if `S < capacity/2`, cooperate only if `q >= 2/3`; otherwise defect.
3. Else if `S >= capacity/2`, cooperate.

Update rule after each round:

- If the opponents' cooperation fraction rises to at least `1/2` for two consecutive rounds, clear `bad`.
- If opponents' cooperation fraction falls below `1/2` again, set `bad` immediately.

Edge cases:

- If `n = 2`, interpret `q` as the single opponent's action.
- If `r = 2`, play `C` in round 1 and `D` in round 2.
- If the stock is already extremely low, keep defecting unless opponents have shown at least two consecutive cooperative rounds; otherwise conserve by defecting and wait for cooperation to reappear.

Behavioral rule of thumb:

- Start cooperative.
- Reward sustained cooperation by cooperating.
- Punish under-cooperation immediately by defecting.
- Exploit the final round by defecting.
'''

description_SELFINTERESTED_23 = '''
Use a conservation-first exploitative rule.

Maintain:
- `q`: estimated opponent cooperation rate, initialized to `1`
- `m_hat = round((n - 1) * q)`, the predicted number of cooperating opponents next round

After each round, update `q` from the observed number of opponent cooperators `m_obs`:
- `q <- 0.7*q + 0.3*(m_obs/(n-1))`

Decision rule for round `t` with current stock `S` and rounds remaining `h = r - t + 1`:

1. **Last round (`h = 1`)**
   - Play `D`.

2. **First round (`t = 1`)**
   - Play `C`.

3. **All other rounds**
   - Predict stock remaining after your move:
     - If you play `C`:
       - `rem_C = S * (m_hat + 1) / (2n)`
     - If you play `D`:
       - `rem_D = S * m_hat / (2n)`
   - Predict next stock after growth:
     - `next_C = min(rem_C + 2 * rem_C * (1 - rem_C / capacity), capacity)`
     - `next_D = min(rem_D + 2 * rem_D * (1 - rem_D / capacity), capacity)`
   - Set the required floor:
     - `floor = capacity / 2` if `h > 2`
     - `floor = 0` if `h = 2`

   - Choose:
     - `D` if `next_D >= floor`
     - otherwise `C`

Edge behavior:
- If `m_hat = 0`, cooperate only when defection would drive the next stock below the floor.
- If `m_hat = n - 1`, defect unless it would violate the floor.
- If the stock is already low, cooperate until the predicted next stock is back above `capacity / 2` for future rounds.

This makes the default move `D`, but switches to `C` whenever cooperation is needed to keep the stock in a profitable range for later rounds.
'''

description_SELFINTERESTED_24 = '''
State variables:
- `q`: estimated opponent cooperation rate, initialized to `0.5`
- `k_prev`: cooperators among opponents in the previous round, initialized to `n-1`

For each round `t = 1..r` with current stock `S`:

1. Update the cooperation estimate from the last observed round:
   - `q <- 0.7 * (k_prev / (n - 1)) + 0.3 * q`

2. Set the stock threshold:
   - `T <- max(2n, 0.35 * capacity + 0.25 * capacity * (1 - (t - 1) / (r - 1)))`

3. Decision rule:
   - If `t == r`, play `D`
   - Else if `t == r - 1`:
     - play `C` only if `S >= T` and `q >= 0.75`
     - otherwise play `D`
   - Else:
     - play `C` if both conditions hold:
       - `S >= T`
       - `q >= 0.5`
     - otherwise play `D`

4. After the round, observe `k` = number of opponents who cooperated, and set:
   - `k_prev <- k`

Additional edge handling:
- If `n = 2`, treat `q = 1` when the single opponent cooperated in the previous round and `q = 0` otherwise.
- If a round ever produces `S = 0`, play `D` for all remaining rounds.
- If the observed cooperation rate drops for two consecutive rounds, require `q >= 0.6` instead of `0.5` for any later cooperation.
- If the observed cooperation rate is at least `0.8` for three consecutive rounds and `S >= 0.6 * capacity`, keep cooperating until the threshold test fails.

This keeps cooperation when the pool is visibly being sustained, and switches to defection as soon as the observed behavior or remaining stock makes preservation unattractive.
'''

description_SELFINTERESTED_25 = '''
Let \(k_t\) be the number of opponents who cooperated in round \(t\), and let \(m_t = n-1-k_t\) be the number of opponents who defected.

Maintain a trust score \(q_t \in [0,1]\), initialized at \(q_1 = 1\).

Update after each round:
\[
q_{t+1} = 0.75q_t + 0.25\left(\frac{k_t}{n-1}\right)
\]
If \(n=2\), then \(\frac{k_t}{n-1}\in\{0,1\}\) as usual.

Decision rule in round \(t\), given current stock \(S_t\):

1. Compute the expected opponent cooperation level \(q_t\).
2. Cooperate if and only if both conditions hold:
   - \(q_t \ge 0.6\)
   - \(S_t \ge 0.45 \cdot \text{capacity}\)

3. Otherwise defect.

Edge cases:
- Round 1: cooperate if \(\text{capacity} \ge 0.45 \cdot \text{capacity}\), so start with \(C\).
- Final round: defect unless \(q_t = 1\) and \(S_t \ge 0.8 \cdot \text{capacity}\). In practice, this means defect in the last round except under fully cooperative history and high stock.
- If the stock ever falls below \(0.25 \cdot \text{capacity}\), defect until it recovers to at least \(0.45 \cdot \text{capacity}\).
- If the observed cooperation share drops below \(0.4\) in any round, set \(q_{t+1} = 0.5q_{t+1}\) as an additional penalty.

Compact pseudocode:
```text
q = 1

for t in 1..r:
    if t == r:
        if q == 1 and S >= 0.8*capacity:
            play C
        else:
            play D
    else:
        if S < 0.25*capacity:
            play D
        else if q >= 0.6 and S >= 0.45*capacity:
            play C
        else:
            play D

    observe k = number of opponent cooperations
    share = k / (n - 1)

    q = 0.75*q + 0.25*share
    if share < 0.4:
        q = 0.5*q
```

Behavioral principle:
- Cooperate only while others are broadly cooperative and the stock remains healthy.
- Defect immediately when cooperation looks weak, when stock is low, or when the horizon is ending.
- Re-enter cooperation only after sustained recovery in observed cooperation and stock.
'''

description_SELFINTERESTED_26 = '''
Initialize:
- If `t = 1`, play `C`.
- Track `m =` number of opponents who cooperated in round `t-1` when `t > 1`.

Decision rule for round `t > 1`:

1. If `t = r`, play `D`.
2. Else if `stock <= capacity / 3`, play `C` only if `m = n - 1`; otherwise play `D`.
3. Else if `stock >= 2 * capacity / 3`:
   - play `C` if `m >= ceil((n - 1) / 2)`
   - otherwise play `D`
4. Else:
   - play `C` if `m >= ceil(2 * (n - 1) / 3)`
   - otherwise play `D`

Adjustment after a cooperation-heavy round:
- If in the previous round you played `C` and `m = n - 1`, keep playing `C` as long as `stock > capacity / 3`.
- If in the previous round at least half of opponents defected, switch immediately to `D` until you observe at least `ceil(2 * (n - 1) / 3)` opponents cooperating again.

Edge cases:
- If `n = 2`, simplify the thresholds:
  - cooperate only when the other player cooperated in the previous round and `stock > capacity / 3`
  - otherwise defect
- If `stock = 0`, play `D`.
- If `stock = capacity`, treat it as `stock >= 2 * capacity / 3`.

Behavioral summary:
- Start with cooperation to probe and preserve the stock.
- Continue cooperating only when the observed cooperation level is strong enough to keep the common pool healthy.
- Defect immediately when cooperation weakens, when stock becomes depleted, or in the final round.
- Once opponents show reliable cooperation again, return to cooperation.
'''

description_SELFINTERESTED_27 = '''
Round 1:
- Play C.

For round t > 1, let S be the current stock and let k be the number of opponents who cooperated in the previous round.

Compute the observed cooperation rate:
- c = k / (n - 1)

Use this decision rule:
- Play C if all three conditions hold:
  1. S ≥ 0.75 × capacity
  2. c ≥ 0.75
  3. The previous round’s stock did not fall sharply:
     - S_prev_remaining / capacity ≥ 0.6, where S_prev_remaining is the stock left immediately after last round’s consumption, before growth
- Otherwise, play D.

State updates to maintain:
- Track S after each round.
- Track S_prev_remaining from the previous round.
- Track whether the last round had a broad cooperative pattern.

Hard thresholds:
- If S ≤ 0.4 × capacity, play D.
- If c ≤ 0.5, play D.
- If S ≥ 0.9 × capacity and c ≥ 0.75, play C even if the previous round was mixed.

Last-round rule:
- In the final round, play D if S < 0.85 × capacity.
- In the final round, play C only if S ≥ 0.85 × capacity and c ≥ 0.75.

Recovery rule after exploitation:
- If you played C in the previous round and c < 0.5, switch to D until both:
  - S ≥ 0.75 × capacity, and
  - c ≥ 0.75 for one full round.

Optional escalation:
- Start in cooperative mode.
- Stay cooperative as long as the system remains near capacity and at least three quarters of opponents cooperate.
- Once either stock or cooperation falls below threshold, defect until cooperation and stock recover.

Decision summary:
- Default to C when the resource is healthy and most opponents are cooperating.
- Default to D when the resource is depleted, cooperation is weak, or recent behavior suggests exploitation.
- Use the final rounds to secure payoff unless the pool is still strong and cooperation is stable.
'''

description_SELFINTERESTED_28 = '''
Round 1:
- Play C.

Round t > 1:
- Let q be the fraction of opponents who played C in round t−1.
- Let S be the current stock at the start of the round.
- Let m = r − t + 1 be the number of rounds remaining, including this one.

Decision rules:
1. If t = r, play D.
2. If S ≤ capacity / 3, play D.
3. If q ≤ 1 / 3, play D.
4. If q ≥ 2 / 3 and S ≥ capacity / 2, play C.
5. Otherwise:
   - play C if q ≥ 1 / 2 and S ≥ 2n
   - play D otherwise

State update heuristic used internally:
- Keep an estimate q̂ of opponent cooperation rate using exponential smoothing:
  q̂ ← 0.7 q̂ + 0.3 q, initialized at q̂ = 1 on round 1.
- Replace q in the rules above with q̂ when the last-round count looks erratic:
  - if |q − q̂| ≥ 1 / 2, use q̂ instead of q.

Tactical adjustment:
- After any round where q = 0, play D for the next two rounds.
- After any round where q = 1, play C for the next two rounds unless S ≤ capacity / 3.

Final-round behavior:
- Always play D, regardless of history or stock.

Tie-breaker:
- When two rules conflict, the more defensive action takes precedence, so D overrides C.
'''

description_SELFINTERESTED_29 = '''
Maintain two variables: the current round `t` and the number of opponents who cooperated in the previous round `h_prev`.

Decision rule:

- **Round 1:** play `C`.
- **Round r:** play `D`.
- **Rounds 2 through r-1:**
  1. Compute `q = ceil((n - 1) / 2)`.
  2. Let `x = stock / capacity`.
  3. Play `C` if and only if both of the following hold:
     - `h_prev >= q`
     - `x >= 1/2`
  4. Otherwise play `D`.

Recovery rule:

- If at any point `h_prev < q`, enter **recovery mode**.
- While in recovery mode, play `D` until you observe a round with `h_prev >= q`.
- Exit recovery mode only after two consecutive rounds satisfy `h_prev >= q`; then return to the main rule above.

Tiebreaks and edge cases:

- If `n = 2`, then `q = 1`, so cooperate only when the other player cooperated in the previous round and the stock is at least half of capacity.
- If `stock = 0`, play `D`.
- If `stock` is very small but positive, still follow the same rule; do not cooperate unless both conditions are met.
- If the game is already in the final round, play `D` regardless of history or stock.
'''

description_SELFINTERESTED_30 = '''
Maintain three internal variables:

- `trust` = exponentially weighted estimate of opponent cooperation, initialized to `1`
- `freeze` = retaliation counter, initialized to `0`
- `last_stock` = previous round stock, initialized to `capacity`

Decision rule each round `t` with current stock `S`:

1. **Final round:** play `D`.
2. **Active retaliation:** if `freeze > 0`, play `D` and decrement `freeze`.
3. **Low-stock protection:** if `S <= 2n`, play `D`.
4. **First round:**
   - play `C` if `r >= 5` and `capacity >= 4n`
   - otherwise play `D`
5. **Update belief from the previous round’s observation**  
   Let `q = observed_cooperators_among_opponents / (n - 1)`.  
   Update:
   `trust = 0.6 * trust + 0.4 * q`
6. **Main choice rule:**
   - If `q < 0.5` or `S < 0.4 * capacity`, set `freeze = 2` and play `D`
   - Else if `trust >= 0.75` and `S >= 0.6 * capacity`, play `C`
   - Else play `D`

Additional edge handling:

- If the previous round’s stock fell by more than 25% (`S < 0.75 * last_stock`), set `freeze = 2` before applying the main choice rule.
- After choosing, set `last_stock = S`.
- If `n = 2`, the same rule applies with `q ∈ {0,1}` from the single opponent’s action.
'''

description_SELFINTERESTED_31 = '''
Initialize:
- `trust = 1`
- `forgiveness = 0`

For round `t = 1..r`, with current stock `S_t` and previous-round observed opponent cooperation count `k_{t-1}` (undefined in round 1):

1. Update trust after round 1 onward:
   - If `t > 1`, set `coop_rate = k_{t-1} / (n - 1)`
   - Update `trust = 0.7 * trust + 0.3 * coop_rate`

2. Last round:
   - If `t == r`, play `D`

3. First round:
   - If `t == 1`, play `C`

4. Middle rounds (`1 < t < r`):
   - Play `D` if any of the following holds:
     - `S_t <= capacity / 4`
     - `trust < 0.55`
     - `k_{t-1} <= floor((n - 1) / 3)`
   - Otherwise play `C`

5. Recovery rule after a bad round:
   - If `k_{t-1} == 0`, set `forgiveness = 2`
   - While `forgiveness > 0`, play `D` and decrement `forgiveness` by 1
   - If `k_{t-1} >= ceil((n - 1) / 2)` for two consecutive observed rounds, reset `forgiveness = 0`

6. State-sensitive override:
   - If `S_t >= 3 * capacity / 4` and `k_{t-1} >= ceil((n - 1) / 2)`, play `C` even if `trust` is only slightly below threshold
   - If `S_t < capacity / 3`, play `D` regardless of `trust`

Compact pseudocode:

```text
if t == 1:
    action = C
elif t == r:
    action = D
else:
    coop_rate = k_prev / (n - 1)
    trust = 0.7 * trust + 0.3 * coop_rate

    if k_prev == 0:
        forgiveness = 2

    if forgiveness > 0:
        action = D
        forgiveness -= 1
    elif S_t < capacity / 3:
        action = D
    elif trust >= 0.55 and k_prev >= floor((n - 1) / 3):
        action = C
    else:
        action = D
```

This strategy cooperates early to keep the stock productive, keeps cooperating only while observed cooperation remains sufficiently high, and switches quickly to defection when the stock is low, others become exploitative, or the game is ending.
'''

description_SELFINTERESTED_32 = '''
State machine with two modes: `CONSERVE` and `EXPLOIT`.

Variables tracked:
- `c_prev`: number of opponents who cooperated in the previous round
- `S`: current stock
- `mode ∈ {CONSERVE, EXPLOIT}`

Rules:

1. **Round 1**
   - Play `C`
   - Set `mode = CONSERVE`

2. **Round r (last round)**
   - Play `D`

3. **All other rounds**
   - Let `q = c_prev / (n - 1)` be the observed cooperation rate among opponents last round.

   **Switch into `EXPLOIT` if any of these hold:**
   - `q < 1/2`
   - `S < capacity / 3`
   - the previous round already had `EXPLOIT` mode and `q < 2/3`

   **Switch back into `CONSERVE` only if all of these hold:**
   - `q ≥ 2/3`
   - `S ≥ capacity / 2`

   **Action by mode:**
   - If `mode = CONSERVE`, play `C`
   - If `mode = EXPLOIT`, play `D`

Edge handling:
- If `n = 2`, then `q` is either `0` or `1`; the same thresholds apply.
- If there is no previous observation available, treat it as round 1 and play `C`.
- If `S = 0`, play `D` for every remaining round.
- If `S = capacity`, keep `CONSERVE` unless the last observed cooperation rate drops below `1/2`.

Tiebreaks:
- At exactly `q = 1/2`, stay in `CONSERVE` only if `S ≥ capacity / 2`; otherwise switch to `EXPLOIT`.
- At exactly `q = 2/3`, allow return to `CONSERVE` if `S ≥ capacity / 2`.

Behavioral intent:
- Start by protecting the stock.
- Keep cooperating only while opponents are mostly cooperative and the stock remains healthy.
- Immediately defect when the group starts overusing the resource or the stock becomes too depleted.
- Never cooperate in the final round.
'''

description_OPPORTUNISTIC_5 = '''
Round 1: cooperate.

After round t, compute:
- c_t = number of opponents who cooperated
- h_t = c_t / (n - 1), the observed cooperation rate among opponents
- S_t = stock at the start of round t

Maintain an exponentially weighted cooperation score:
- q_1 = 1
- q_{t+1} = 0.7 q_t + 0.3 h_t

Decision rule for round t+1:
- Let E_{t+1} = r - t be the number of rounds remaining after the current round is played.
- Cooperate if all of the following hold:
  1. q_t ≥ 0.5
  2. S_t ≥ 1.2n
  3. t < r - 1
- Otherwise defect.

Aggressive exploitation rule:
- If h_t = 1 in two consecutive observed rounds, defect on the next round unless S_t < capacity/3, in which case cooperate one more round.

Punishment rule:
- If h_t ≤ 0.5 in any round, defect for the next two rounds.
- If h_t = 0, defect until q_t rises above 0.6 again.

Stock-based opportunism:
- If S_t > 1.6n and q_t ≥ 0.5, cooperate.
- If S_t ≤ 1.0n, defect.
- If S_t is in (1.0n, 1.6n] and q_t ≥ 0.7, cooperate; otherwise defect.

Endgame:
- In the final two rounds, defect.
- If t = r - 2 and q_t < 0.8, defect for both remaining rounds.
- If t = r - 2 and q_t ≥ 0.8 and S_t > 1.4n, cooperate once, then defect in the last round.

Recovery rule:
- After any defection phase, return to cooperation only if both:
  - h_t ≥ 0.75 in the most recent round, and
  - q_t ≥ 0.6

Pseudocode:

```
if t == 1:
    play C
else:
    if t >= r - 1:
        play D
    elif h_{t-1} == 0:
        play D
    elif h_{t-1} <= 0.5:
        play D for next 2 rounds
    elif h_{t-2} == 1 and h_{t-1} == 1 and S_t >= capacity/3:
        play D
    elif S_t <= 1.0*n:
        play D
    elif S_t > 1.6*n and q_t >= 0.5:
        play C
    elif S_t > 1.0*n and q_t >= 0.7:
        play C
    elif q_t >= 0.5 and t < r - 1:
        play C
    else:
        play D
```

State update after each round:
- q_{t+1} = 0.7 q_t + 0.3 h_t
- Track any forced-defection counter from punishment rules and override the normal decision while it is positive.

Priority order:
1. Final-round defection
2. Forced punishment
3. Immediate exploitation of sustained full cooperation
4. Stock threshold
5. Cooperation score threshold
6. Default defection
'''

description_OPPORTUNISTIC_6 = '''
Play a contingent threshold strategy with three modes: harvest, mirror, and lock-in.

Maintain after each round:
- `s`: current stock
- `k`: number of opponents who cooperated last round
- `p_hat`: smoothed estimate of opponent cooperation rate, initialized at 1
- `m`: streak length of consecutive rounds with “good” cooperation by opponents

At round `t` with `m = r - t + 1` rounds remaining:

1. Compute the observed cooperation rate:
   - `x = k / (n - 1)` for rounds after the first
   - after round 1, set `x` directly from the observation

2. Update the smoothed estimate:
   - `p_hat = 0.7 * p_hat + 0.3 * x`

3. Define the cooperation threshold for the current stock:
   - `tau = 0.5 + 0.25 * (1 - s / capacity)`
   - clamp `tau` to `[0.35, 0.85]`

4. Decision rule:
   - **If `t = 1`**: play `C`
   - **Else if `m = 1`**: play `D`
   - **Else if `s <= 0.25 * capacity`**: play `D`
   - **Else if `p_hat >= tau`**: play `C`
   - **Else if `k >= ceil((n - 1) * 0.75)` and `s >= 0.5 * capacity`**: play `C`
   - **Otherwise**: play `D`

5. Opportunistic escalation:
   - If you played `C` last round and at least `ceil((n - 1) * 0.75)` opponents cooperated, keep playing `C` as long as both hold:
     - `p_hat >= tau`
     - `s >= 0.4 * capacity`
   - The first time either condition fails, switch to `D` immediately.

6. Recovery rule:
   - After any round in which fewer than half of opponents cooperated, reset `m = 0`
   - Require two consecutive rounds with `x >= 0.75` before returning to sustained cooperation
   - During recovery, play `D` unless `x >= 0.75` twice in a row

7. Endgame rule:
   - In the last two rounds, play `D`
   - If the last three rounds remain and `s >= 0.8 * capacity` and `x >= 0.9`, play `C` once, then `D` thereafter

Pseudocode:

```text
Initialize p_hat = 1
Initialize good_streak = 0

For round t = 1..r:
    if t == 1:
        play C
        observe k
        continue

    x = k / (n - 1)
    p_hat = 0.7 * p_hat + 0.3 * x

    tau = 0.5 + 0.25 * (1 - s / capacity)
    tau = min(0.85, max(0.35, tau))

    if r - t + 1 <= 2:
        play D

    else if s <= 0.25 * capacity:
        play D

    else if x >= 0.75:
        good_streak += 1
        if good_streak >= 2 and p_hat >= tau and s >= 0.4 * capacity:
            play C
        else:
            play D

    else:
        good_streak = 0
        if p_hat >= tau or (k >= ceil(0.75 * (n - 1)) and s >= 0.5 * capacity):
            play C
        else:
            play D

    if you played C and k >= ceil(0.75 * (n - 1)):
        remain in C next round unless either:
            p_hat < tau
            or s < 0.4 * capacity
```

Behavioral intent:
- Open cooperatively.
- Stay cooperative only when the observed cooperation rate is consistently high and the stock is healthy.
- Immediately switch to defection when cooperation drops or the stock becomes depleted.
- Exploit high-cooperation environments while they last, but never continue cooperation into the final rounds or after clear weakening of the group.
'''

description_OPPORTUNISTIC_7 = '''
Track three values: current stock `S`, previous stock `S_prev`, and last-round opponent cooperation count `c` out of `n-1`.

Define:
- `p = c / (n-1)` for `n > 2`
- for `n = 2`, `p` is either `0` or `1`
- in round 1, set `c = n-1` and `S_prev = capacity`

Decision rule for round `t`:

```text
if t == 1:
    play C

else if t == r:
    play D

else if t == r - 1:
    if S <= capacity / 2:
        play C
    else if p >= 3/4:
        play D
    else:
        play C

else:
    if S <= capacity / 3:
        play C
    else if p < 1/2:
        play C
    else if p >= 3/4 and S >= capacity / 2:
        play D
    else if S > S_prev and p >= 1/2:
        play D
    else:
        play C
```

Update after each round:
- set `S_prev = S`
- observe the new `c`
- recompute `p`

Behavioral meaning:
- Start by cooperating to keep the stock healthy.
- Cooperate whenever the stock is low or opponents were not cooperative enough to justify harvesting.
- Defect when the stock is healthy and cooperation by others is strong enough to support extraction.
- In the final round defect always.
- In the penultimate round, defect only if the stock is comfortably high and the opponent crowd is strongly cooperative; otherwise preserve the pool.

Edge cases:
- If `n = 2`, treat `p = 1` when the single opponent cooperated and `p = 0` otherwise.
- If the stock is extremely low, always cooperate regardless of observed behavior.
- If the stock has just risen from the previous round and cooperation remains high, switch to defect to harvest the rebuilt pool.
'''

description_OPPORTUNISTIC_8 = '''
Use a state-based threshold strategy with escalation and recovery:

### Core rule
Let:
- `S` = current stock at the start of the round
- `k` = number of opponents who cooperated in the previous round
- `m = n - 1` = number of opponents
- `f = k / m` = observed opponent cooperation rate from the previous round
- `x` = your own action in the previous round (`C` or `D`)

Define the following thresholds:
- `high = 0.75`
- `medium = 0.5`
- `low = 0.25`

### Round 1
Play `C`.

### Rounds 2 to r-1
Compute the cooperation rate `f` from the previous round and update based on stock:

1. **If stock is very low**
   - If `S <= capacity / 4`, play `D` unless `f >= high`, in which case play `C`.

2. **If stock is moderate**
   - If `capacity / 4 < S <= capacity / 2`:
     - play `C` if `f >= medium`
     - otherwise play `D`

3. **If stock is high**
   - If `S > capacity / 2`:
     - play `C` if `f >= low`
     - otherwise play `D`

### Opportunistic adjustment
If the previous round had high cooperation and your own cooperation would preserve a high stock, exploit it cautiously:

- If `f >= high` and `S > capacity / 2`, play `D` once.
- If `f >= high` and `S <= capacity / 2`, play `C`.

This gives one-step opportunism when others are reliably cooperative, but avoids collapsing the stock.

### Recovery rule after defection
If you defected last round and the stock now falls into the low zone, switch back to cooperation only if:
- `f >= medium`, or
- `S > capacity / 2`

Otherwise keep defecting until the stock recovers or cooperation rises.

### Last round
On round `r`, play:
- `D` if `S > capacity / 2`
- `C` otherwise

### Full decision rule in pseudocode
```text
if t == 1:
    action = C
else if t == r:
    action = D if S > capacity/2 else C
else:
    f = k / (n - 1)

    if S <= capacity/4:
        action = C if f >= 0.75 else D
    else if S <= capacity/2:
        action = C if f >= 0.5 else D
    else:
        action = C if f >= 0.25 else D

    if f >= 0.75 and S > capacity/2:
        action = D
```

### Edge cases
- If `n = 2`, then `f` is either `0` or `1`; use the same thresholds directly.
- If `k = 0`, treat cooperation rate as `0`.
- If `k = m`, treat cooperation rate as `1`.
- If the stock is exactly on a threshold, use the more cautious branch:
  - `S = capacity/4` counts as low
  - `S = capacity/2` counts as moderate

### Opportunistic behavior
- Cooperate when the stock is fragile or when the group is sufficiently cooperative to preserve future value.
- Defect when the stock is healthy and opponents are cooperative enough to absorb exploitation without immediate collapse.
- If cooperation collapses, switch to self-protection quickly.
- If cooperation recovers, re-enter cooperation to keep the stock productive.
'''

description_OPPORTUNISTIC_9 = '''
- Round 1: play C.

- Let `k` be the number of opponents who played C in the previous round, and let `s = stock / capacity`.

- If it is the final round: play D.

- Otherwise:
  - Play C if `s <= 0.40` or `k <= floor((n-1)/3)`.
  - Play D if `s >= 0.65` and `k >= ceil(2(n-1)/3)`.
  - Play D if `k >= ceil((n-1)/2)` and `s > 0.40`.
  - Play C in all remaining cases.

- Persistent exploitation mode:
  - If in two consecutive rounds `k >= ceil(2(n-1)/3)` and `s >= 0.65`, then play D for the next two rounds unless `s <= 0.40`.
  - Reset this mode immediately if `k <= floor((n-1)/3)` or `s <= 0.40`.

- Collapse-avoidance override:
  - If `s <= 0.25`, play C regardless of `k`, except in the final round where you play D.

- Edge handling:
  - With `n = 2`, treat `k = 1` as “high cooperation” and `k = 0` as “low cooperation.”
  - If the previous round’s stock was unchanged at the cap, require the high-cooperation condition for two consecutive rounds before entering exploitation mode.
  - If the observed cooperation count is missing for any reason, play C unless it is the final round.
'''

description_OPPORTUNISTIC_10 = '''
Start cooperative and condition future behavior on whether the group is keeping the stock in the sustainable region.

Let:
- `S` be the current stock before the round
- `k` be the number of observed opponent cooperators in the previous round
- `m = n - 1` be the number of opponents
- `c_t` be the number of cooperating opponents in round `t`

Maintain two running estimates from history:
- `avgC = average opponent cooperation rate over observed rounds`
- `trend = c_t - c_{t-1}` for the last two observed rounds

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **If stock is critically low**
   - If `S <= capacity / 4`, play `C` only if the previous round had at least `ceil(3m/4)` cooperating opponents.
   - Otherwise play `D`.

3. **If stock is healthy**
   - If `S >= capacity / 2`, play `D` when both hold:
     - `avgC >= 2/3`, and
     - `c_{t-1} >= ceil(2m/3)`
   - Otherwise play `C`.

4. **If stock is in the middle band**
   - Play `C` if either:
     - `c_{t-1} >= ceil(m/2)`, or
     - `trend > 0`
   - Otherwise play `D`.

5. **Last round**
   - If `S >= capacity / 2`, play `D`.
   - Else play `C`.

History update after each round:
- Compute `c_t` from the observed number of cooperating opponents.
- Update `avgC` using all observed rounds so far.
- Set `trend = c_t - c_{t-1}` when `t >= 2`.

Punishment and recovery rules:
- If opponent cooperation falls below half of opponents for two consecutive observed rounds, switch to `D` until either:
  - cooperation rebounds to at least `ceil(2m/3)` in one round, or
  - stock rises back above `capacity / 2`.
- If cooperation rebounds strongly, immediately return to the normal state-based rule.

Tie-breaking and edge cases:
- When a threshold is met exactly, treat it as satisfied.
- If no previous round exists, ignore history-dependent conditions and play `C`.
- If the stock is exactly on a boundary, use the rule for the lower stock band at `capacity / 4` and the higher stock band at `capacity / 2`.

Operational intuition encoded in the strategy:
- Cooperate early to support stock recovery.
- Defect when the stock is comfortably high and others are sustaining the pool.
- Defect more aggressively near the end when there is no future punishment.
- Respond quickly to visible free-riding by shifting to self-protection, but restore cooperation when the group recovers.
'''

description_OPPORTUNISTIC_11 = '''
Round 1: play C.

For every later round, let c be the number of opponents who cooperated in the previous round, and let S be the current stock.

Compute the predicted next stock under each action, assuming the opponents repeat their last-round behavior:

- If you play C, predicted cooperators = c + 1
- If you play D, predicted cooperators = c

Using K predicted cooperators, define:
- remaining = S × K / (2n)
- predicted_stock(K) = min(remaining + 2 × remaining × (1 - remaining / capacity), capacity)

Decision rule:
1. If predicted_stock(c) >= capacity / 2, play D.
2. Else if predicted_stock(c + 1) >= capacity / 2, play C.
3. Else play D.

Special overrides:
- If c = 0, play D.
- In the final round, play D.
- If S <= capacity / 4, play C only when c >= ceil((n - 1) / 2); otherwise play D.

Behavioral pattern:
- Exploit high cooperation by defecting whenever the pool is still on a healthy trajectory.
- Switch to cooperation only when defection would likely push the stock below the recovery threshold and there is enough recent cooperation to make rebuilding plausible.
- Never subsidize a round with little or no observed cooperation.
- Default to defecting whenever the next-round stock can be kept above the target floor without your help.
'''

description_OPPORTUNISTIC_12 = '''
Round 1: cooperate.

Let c_t be the number of opponents who cooperated in round t, and let s_t be the stock at the start of round t.

Define:
- coop_share_t = c_t / (n - 1)
- coop_fraction_t = c_t / (n - 1)

Track:
- m_t = average of coop_fraction over the last up to 3 rounds
- b_t = number of consecutive rounds immediately preceding t in which all opponents cooperated

Decision rule for round t ≥ 2:

1. Immediate exploitation rule
- If c_{t-1} = n - 1 and t < r, play D.
- If c_{t-1} = n - 1 and t = r, play D.

2. Recovery rule
- If c_{t-1} ≤ (n - 1)/2, play C.

3. Opportunistic follow-the-majority rule
- If c_{t-1} > (n - 1)/2 and c_{t-1} < n - 1:
  - play C if m_t ≥ 2/3
  - otherwise play D.

4. Stock-pressure rule
- If s_t ≤ capacity/3, play D.
- If s_t ≥ 2·capacity/3 and c_{t-1} ≥ (n - 1)/2, play C.

5. Default rule
- If none of the above applies:
  - play C when c_{t-1} ≥ (n - 1)/2
  - otherwise play D

Additional sharpening:
- After any round in which you played C and c_t = n - 1, switch to D next round.
- After any round in which you played D and c_t = 0, switch to C next round.
- If the last two rounds both had c_t ≥ 2(n - 1)/3, play C even if the default rule would defect.
- If the last two rounds both had c_t ≤ (n - 1)/3, play D even if the default rule would cooperate.

Late-game rule:
- In the final two rounds, play D whenever c_{t-1} > 0.
- In the final two rounds, play C only if c_{t-1} = 0.

Summary behavior:
- Start cooperatively.
- Stay cooperative when opponents are broadly cooperative.
- Defect immediately after full cooperation to capture the larger short-run gain.
- Defect under weak cooperation or low stock.
- Re-enter cooperation only after opponents restore substantial cooperation.
'''

description_OPPORTUNISTIC_13 = '''
Play cooperatively only when the previous round showed enough restraint to preserve the stock; otherwise defect.

Decision rule for round t with current stock S_t and observed number of opponent cooperators k_{t-1} from the previous round:

- Define opponent cooperation rate  
  q_{t-1} = k_{t-1} / (n - 1) for t > 1.

- Define a stock pressure threshold  
  P_t = 0.35 + 0.25 * (1 - S_t / capacity).  
  Clamp P_t to the interval [0.35, 0.60].

- Cooperate in round t if all of the following hold:
  1. t = 1 and S_t = capacity
  2. t > 1 and q_{t-1} ≥ P_t
  3. S_t > capacity / 4

- Otherwise defect.

Round-by-round behavior:

- Round 1:
  - Cooperate if the initial stock is at capacity.
  - If the game ever starts below capacity, defect immediately.

- Early rounds:
  - Use the observed opponent cooperation rate from the prior round as the main signal.
  - If most opponents cooperated and the stock is still healthy, cooperate.
  - If cooperation is mixed or weak, defect.

- Low-stock regime:
  - If S_t ≤ capacity / 4, defect regardless of past behavior.
  - If S_t ≤ capacity / 8, defect for the rest of the game.

- Late rounds:
  - For t ≥ r - 1, defect unless both:
    1. q_{t-1} = 1
    2. S_t ≥ capacity / 2
  - In the final round, defect.

- Recovery rule after a bad round:
  - If q_{t-1} < P_t, defect next round.
  - Return to cooperation only after one full round with q_{t-1} ≥ P_t again.

- Escalation:
  - If opponents fully cooperate for two consecutive rounds and S_t ≥ 3 * capacity / 4, cooperate for those rounds.
  - If opponents defect in at least half of the previous round, defect immediately and continue defecting until cooperation rate recovers above threshold.

Compact pseudocode:

```text
if t == 1:
    action = C if S_t == capacity else D
elif t == r:
    action = D
elif S_t <= capacity/8:
    action = D
elif S_t <= capacity/4:
    action = D
else:
    q = k_{t-1} / (n-1)
    P = clamp(0.35 + 0.25*(1 - S_t/capacity), 0.35, 0.60)
    if t >= r-1:
        action = C if (q == 1 and S_t >= capacity/2) else D
    else:
        action = C if q >= P else D
```
'''

description_OPPORTUNISTIC_14 = '''
Play cooperatively when the stock is healthy and the recent cooperation rate is high enough to keep the stock near its refill zone; switch to defect immediately when the stock or cooperation level falls below a recovery threshold; exploit sustained generosity by defecting selectively when the stock is high and opponents are cooperating, then return to cooperation before the stock crosses the danger zone.

Decision rule for round t with current stock S and observed number of opponent cooperators k from the previous round:

- Let p̂ = k / (n - 1) be the observed opponent cooperation rate.
- Define four stock zones:
  - Full zone: S ≥ 0.80 · capacity
  - Safe zone: 0.60 · capacity ≤ S < 0.80 · capacity
  - Warning zone: 0.40 · capacity ≤ S < 0.60 · capacity
  - Critical zone: S < 0.40 · capacity

- Define two cooperation benchmarks:
  - High cooperation: p̂ ≥ 0.75
  - Moderate cooperation: p̂ ≥ 0.50

Action choice:

1. First round:
   - Cooperate.

2. Full zone:
   - If p̂ is high, defect.
   - Otherwise cooperate.

3. Safe zone:
   - If p̂ is high and the stock has been in the safe or full zone for the last two rounds, defect every third such round; otherwise cooperate.
   - If p̂ is only moderate, cooperate.
   - If p̂ is low, defect.

4. Warning zone:
   - Cooperate if p̂ is high.
   - Otherwise defect.

5. Critical zone:
   - Cooperate only if p̂ is high for two consecutive observed rounds.
   - Otherwise defect.

Recovery rule after a defect-heavy period:
- If you have defected in the last two rounds and the current stock has risen back to at least 0.60 · capacity, return to cooperation unless p̂ is still high and the stock is in the full zone, in which case take one defecting round to harvest before resuming cooperation.

Endgame rule:
- In the final round, defect unless the stock is in the critical zone and p̂ is high; in that case cooperate.
- In the last three rounds, if the stock is in the warning or critical zone, cooperate until stock returns to at least 0.60 · capacity; otherwise use the full-zone opportunistic rule.

History update:
- Track only:
  - current stock S
  - previous-round cooperation rate p̂
  - whether the last two rounds were cooperative or defect-heavy
  - whether the stock is recovering or collapsing

Fallback rule:
- If the previous-round observation is unavailable, cooperate when S ≥ 0.70 · capacity and defect otherwise.

Compact pseudocode:

if t == 1:
    action = C
else:
    p_hat = coop_opponents_last_round / (n - 1)

    if t >= r - 2:
        if S < 0.60 * capacity:
            action = C if p_hat >= 0.75 else D
        else:
            action = D if S >= 0.80 * capacity and p_hat >= 0.75 else C
    else:
        if S >= 0.80 * capacity:
            action = D if p_hat >= 0.75 else C
        elif S >= 0.60 * capacity:
            if p_hat >= 0.75 and last_two_rounds were cooperative:
                action = D every third safe-zone round
            elif p_hat >= 0.50:
                action = C
            else:
                action = D
        elif S >= 0.40 * capacity:
            action = C if p_hat >= 0.75 else D
        else:
            action = C if p_hat >= 0.75 and last_two_observations were highly cooperative else D

Interpretation of the opportunistic posture:
- Reward cooperative environments by staying cooperative enough to keep the stock replenished.
- Take occasional surplus by defecting only when the stock is high and the group is reliably cooperative.
- Stop exploiting immediately when the stock enters danger zones or cooperation weakens.
- In the final rounds, switch toward harvesting unless preserving the stock is still necessary to avoid a collapse.
'''

description_OPPORTUNISTIC_15 = '''
Start by cooperating.

Let `k_t` be the number of other players who cooperated in round `t-1`, and let `S_t` be the observed stock at the start of round `t`.

Define the cooperation threshold
`q_t = ceil((n - 1) / 2)`

and the stock bands
- `high` if `S_t >= 0.75 * capacity`
- `medium` if `0.40 * capacity <= S_t < 0.75 * capacity`
- `low` if `S_t < 0.40 * capacity`

Decision rule in round `t`:

1. If `t = 1`, play `C`.

2. If `t = r`, play `C` if `S_t >= 2n`; otherwise play `D`.

3. If `S_t = 0`, play `D`.

4. If `k_t >= q_t`:
   - play `C` when `S_t` is `high` or `medium`
   - play `D` when `S_t` is `low`

5. If `k_t < q_t`:
   - play `C` only when `S_t` is `high` and `k_t >= q_t - 1`
   - otherwise play `D`

6. If the previous round was `D` by a large margin, defined as `k_t = 0`, then:
   - play `D` for one round unless `S_t` is `high`; in that case, probe with `C`

7. If there has been a streak of at least two consecutive rounds with `k_t >= q_t`, then:
   - play `C` as long as `S_t` remains at least `0.40 * capacity`
   - switch to `D` immediately once `S_t` drops below `0.40 * capacity`

Update logic after each round:

- If you played `C` and at least `q_t` opponents also cooperated, continue with `C` unless stock falls into `low`.
- If you played `C` and fewer than `q_t` opponents cooperated, switch to `D` next round unless stock is `high`.
- If you played `D` and the observed cooperation count rises to at least `q_t`, return to `C` immediately when stock is `high` or `medium`.

Fallback mode:

- If the observed cooperation pattern alternates unpredictably, use:
  - `C` when `S_t >= 0.75 * capacity`
  - `D` otherwise

This makes the strategy cooperative when the pool is healthy, quick to exploit sustained restraint by others, and fast to retreat when cooperation is not being met or the stock becomes depleted.
'''

description_OPPORTUNISTIC_16 = '''
Let \(k_t\) be the number of opponents who cooperated in round \(t\), \(S_t\) the stock at the start of round \(t\), and \(m_t = r-t+1\) the number of rounds remaining including round \(t\).

Maintain two internal modes:

- **Harvest mode**: play \(D\)
- **Preserve mode**: play \(C\)

Initialize in **Preserve mode**.

### Decision rule each round

1. Compute the expected stock after a round if you play \(C\) against \(k_t\) cooperating opponents:
   \[
   S^{C}_{t+1} = \min\Big((S_t - \tfrac{S_t}{2n} - k_t \cdot \tfrac{S_t}{2n} - (n-1-k_t)\cdot \tfrac{S_t}{n}) + 2X(1 - X/\text{capacity}),\ \text{capacity}\Big)
   \]
   where \(X\) is the post-consumption stock before growth.  
   Similarly define \(S^{D}_{t+1}\) for playing \(D\).

2. Define the **sustainability threshold**:
   \[
   \theta_t = \max\left(2n,\ \frac{\text{capacity}}{4} \cdot \frac{m_t}{r}\right)
   \]

3. Define the **cooperation signal threshold**:
   \[
   \kappa_t = \left\lceil \frac{n-1}{2} \right\rceil
   \]

4. Play according to:

   - **If \(t = r\)**: play \(D\)
   - **Else if \(S_t \le \theta_t\)**: play \(C\)
   - **Else if \(k_{t-1} \ge \kappa_{t-1}\)**: play \(D\)
   - **Else if \(k_{t-1} < \kappa_{t-1}\) and \(S_t > \theta_t\)**: play \(D\)
   - **Else**: play \(C\)

### Operational interpretation

- **First round**: play \(C\).
- **If a majority of opponents cooperated in the previous round and the stock is comfortably above the threshold**: switch to \(D\).
- **If the stock drops near the threshold**: switch to \(C\) immediately to help rebuild the pool.
- **If opponents are mostly defecting and the stock is still high**: play \(D\) to extract while the pool lasts.
- **Final round**: always play \(D\).

### Mode update rule

After observing \(k_t\):

- If \(k_t \ge \kappa_t\) and \(S_{t+1} > \theta_{t+1}\), set mode to **Harvest**
- If \(k_t < \kappa_t\) or \(S_{t+1} \le \theta_{t+1}\), set mode to **Preserve**

### Compact pseudocode

```text
if t == 1:
    action = C
else if t == r:
    action = D
else if S_t <= theta_t:
    action = C
else if k_{t-1} >= ceil((n-1)/2):
    action = D
else:
    action = D

# but override:
if S_t <= theta_t:
    action = C
```

### Edge-case handling

- If the stock is already at the minimum sustainable level, always play \(C\) until it rises above threshold.
- If the stock is near capacity and at least half of opponents cooperated last round, exploit with \(D\).
- If there is only one round left, ignore future preservation and defect.
- If the observed cooperation count alternates unpredictably, let the stock threshold dominate: high stock favors \(D\), low stock forces \(C\).
'''

description_OPPORTUNISTIC_17 = '''
Maintain two internal variables:

- `p_hat`: estimate of opponent cooperation rate, initialized at 1/2
- `mode`: one of `{build, harvest, punish}`, initialized to `build`

Update after each round `t` from the observed number of opponent cooperators `k_t` among `n-1` opponents:

- `q_t = k_t / (n - 1)`
- `p_hat <- 0.7 * p_hat + 0.3 * q_t`

At the start of round `t`, with current stock `S_t`:

1. Compute projected next stock under universal cooperation:
   - `S_C = min( S_t - S_t/2 + 2*(S_t/2)*(1 - (S_t/2)/capacity), capacity )`

2. Compute projected next stock under universal defection:
   - `S_D = min( S_t - S_t + 2*0*(1 - 0/capacity), capacity ) = 0`

3. Define a high-stock threshold:
   - `H = 0.8 * capacity`

4. Define a low-stock threshold:
   - `L = 0.35 * capacity`

Decision rule:

- If `t = r`, play `D` if `S_t >= 2n * 0.9` or `p_hat <= 0.55`; otherwise play `C`.
- Else if `S_t <= L`, play `C` if `p_hat >= 0.6`; otherwise play `D`.
- Else if `S_t >= H`:
  - play `D` if `p_hat >= 0.7`
  - play `C` otherwise
- Else:
  - if `p_hat >= 0.65` and `S_C >= S_t`, play `D`
  - if `p_hat < 0.65`, play `C`
  - if `p_hat >= 0.65` and `S_C < S_t`, play `C`

Mode refinement:

- Set `mode = build` if `q_t >= 0.75`
- Set `mode = harvest` if `0.45 <= q_t < 0.75`
- Set `mode = punish` if `q_t < 0.45`

Apply mode adjustment before acting:

- In `build`, if `S_t < H`, play `C` unless it is the last round.
- In `harvest`, follow the main decision rule exactly.
- In `punish`, play `D` unless `S_t <= L`, in which case play `C` to preserve the stock floor.

First-round rule:

- Play `C`.

Last-round rule:

- Play `D` whenever `S_t >= 0.9 * 2n`
- Otherwise play `C` if `S_t <= L` or `p_hat < 0.55`
- Otherwise play `D`

Hard safeguard:

- Never play `D` when `S_t < 0.15 * capacity` unless `t = r`
- If `S_t = 0`, play `C`

Pseudocode:

```text
init p_hat = 0.5
init mode = build

for each round t:
    observe current stock S_t

    if t == 1:
        action = C
    else if t == r:
        if S_t >= 1.8 * n or p_hat <= 0.55:
            action = D
        else:
            action = C
    else:
        if S_t < 0.15 * capacity:
            action = C
        else:
            if mode == build and S_t < 0.8 * capacity:
                action = C
            else if S_t <= 0.35 * capacity:
                action = C if p_hat >= 0.6 else D
            else if S_t >= 0.8 * capacity:
                action = D if p_hat >= 0.7 else C
            else:
                action = D if p_hat >= 0.65 else C

    play action

    observe k_t = number of cooperating opponents

    q_t = k_t / (n - 1)
    p_hat = 0.7 * p_hat + 0.3 * q_t

    if q_t >= 0.75:
        mode = build
    else if q_t >= 0.45:
        mode = harvest
    else:
        mode = punish
```
'''

description_OPPORTUNISTIC_18 = '''
Use a stock-preserving default, exploit whenever the current round is safe, and switch to restraint immediately after any sign of overuse.

Let:
- `c_t` = number of opponents who cooperated in round `t-1`
- `S_t` = stock at start of round `t`
- `m_t = n - 1 - c_t` = number of opponents who defected in round `t-1`
- `p_t = c_t / (n - 1)` = observed cooperation rate among opponents in the previous round
- `x = S_t / capacity` = normalized stock

Decision rule for round `t`:

1. If `t = 1`, play `C`.

2. If `S_t = 0`, play `C`.

3. If `t = r`, play `D` if `S_t > 0`, otherwise `C`.

4. Otherwise, compute the danger level:
   - `danger = 2 * (1 - x) - x / n`
   - equivalently, `danger = 2 - 2x - x/n`

   Then apply:

   - If `p_t < 1` and either
     - `m_t >= 1`, or
     - `danger >= 0.25`, or
     - `S_t < capacity / 2`,
     play `C`.

   - If `p_t = 1` and `S_t >= capacity / 2`, play `D`.

   - If `p_t = 1` and `S_t < capacity / 2`, play `C` unless `t = r`, in which case play `D`.

Adaptive update rules:
- After any round with at least one opponent defecting, switch to `C` in the next round.
- After any round with all opponents cooperating and `S_t >= capacity / 2`, play `D` in the next round.
- After any round with all opponents cooperating and `S_t < capacity / 2`, keep playing `C` until either:
  - a defection is observed, or
  - `S_t` recovers to at least `capacity / 2`.

Optional compact form:

```
if t == 1:
    C
elif S == 0:
    C
elif t == r:
    D if S > 0 else C
else:
    if p < 1:
        C
    else:
        D if S >= capacity/2 else C
```

Refinement:
- If the previous round had mixed behavior (`0 < p_t < 1`), always play `C` next round.
- If two consecutive rounds have `p_t = 1` and `S_t` is at least `capacity / 2`, play `D` on the second of those rounds.
- If the stock falls below `capacity / 4`, continue playing `C` until it rises above `capacity / 3` or until the final round.
'''

description_OPPORTUNISTIC_19 = '''
Round 1: play C.

For round t > 1, let
- x_t = number of opponents who cooperated in round t-1
- h_t = x_t / (n - 1)
- \bar h_t = weighted average of h over the last up to 3 observed rounds, with weights 3, 2, 1 for most recent to oldest

Use these rules in order:

1. Repair rule
- If stock <= 0.45 × capacity, play C.

2. Endgame rule
- If t >= r - 1:
  - play C if stock <= 0.60 × capacity or \bar h_t < 0.50
  - otherwise play D

3. Harvest rule
- If stock >= 0.70 × capacity and \bar h_t >= 0.60, play D.

4. Stability rule
- If 0.45 × capacity < stock < 0.70 × capacity:
  - play C if \bar h_t >= 0.50
  - play D otherwise

5. Low-cooperation rule
- If \bar h_t < 1/3, play D unless stock <= 0.45 × capacity, in which case play C.

6. Default
- Otherwise play C.

Update logic:
- After any round in which stock falls below 0.45 × capacity, switch immediately to repair rule and keep cooperating until stock rises above 0.55 × capacity.
- After any round in which \bar h_t >= 0.60 and stock remains above 0.70 × capacity, stay in harvest mode and defect.
- After any round in which \bar h_t < 0.50, exit harvest mode and return to stability or repair depending on stock.

Tie-breaking:
- If two rules apply, use the one earlier in the list.
- If the last observed round is unavailable, treat \bar h_t = h_t from the most recent observed round.

Behavioral pattern:
- Cooperate early to probe.
- Defect when the stock is high and the others are reliably cooperative.
- Switch to repair immediately when the stock gets strained.
- Punish persistent low cooperation by defecting, but never at the expense of letting the stock collapse when it is already low.
'''

description_OPPORTUNISTIC_20 = '''
Maintain two running summaries:

- `q_t`: fraction of opponents who cooperated in the previous round, or the average of all observed opponent cooperation fractions so far if you want smoothing.
- `s_t`: current stock at the start of round `t`.

Define:

- `u_t = s_t / capacity`  (stock normalized to capacity)
- `k_t =` number of opponents observed to cooperate last round
- `m = n - 1` opponents

Decision rule in round `t`:

1. **First round**
   - Play `C` if `capacity` is at least moderately high relative to the group size:
     - cooperate when `capacity >= 4n`
   - Otherwise play `D`

2. **Last round**
   - If `s_t >= capacity / 2`, play `D`
   - Otherwise play `C`

3. **Middle rounds**
   - Compute the observed cooperation rate from the previous round:
     - `q = k_{t-1} / m`
   - Compute a cooperation pressure score:
     - `P = 0.5*q + 0.5*u_t`
   - Then choose:

     **Cooperate (`C`)** if all of the following hold:
     - `u_t >= 0.45`
     - `q >= 0.6`
     - `t <= r - 2`

     **Defect (`D`)** otherwise

4. **Opportunistic override**
   - If the previous round had strong cooperation from others, exploit it:
     - if `q >= 0.75` and `u_t >= 0.3`, play `D`
   - If the stock is near collapse, stop sacrificing:
     - if `u_t <= 0.2`, play `D`
   - If the stock is strongly recovering and others are still cooperative, rejoin:
     - if `u_t >= 0.6` and `q >= 0.5`, play `C`

State update after each round:

- Record `k_t`, update `q_t` as either:
  - `q_t = k_t / m` if using only the latest observation, or
  - `q_t = 0.7*q_{t-1} + 0.3*(k_t / m)` if using smoothing

Practical interpretation of the rules:

- Start by cooperating only when the pool is large enough to be worth preserving.
- When the others are mostly cooperative and the stock is healthy, cooperate long enough to keep the pool productive.
- When the others show strong cooperation, defect to take the larger share.
- When cooperation among others weakens or stock falls too far, defect immediately.
- In the final round, defect if the pool is still large; cooperate only if the stock is already low enough that restraint no longer changes future outcomes.

Edge cases:

- If `n = 2`, then `m = 1`; use the same rules with `q` equal to whether the other player cooperated last round.
- If `r = 2`, the first-round rule is used in round 1 and the last-round rule in round 2.
- If `s_t = 0`, always play `D`.
- If `s_t = capacity`, apply the normal rules without special treatment.
- If the observed cooperation rate is unavailable for a round, treat `q = 0.5`.

Compact version:

```text
if t == 1:
    play C if capacity >= 4n else D
elif t == r:
    play D if s_t >= capacity/2 else C
else:
    u = s_t / capacity
    q = observed_coop_rate_last_round

    if u <= 0.2:
        play D
    elif q >= 0.75 and u >= 0.3:
        play D
    elif u >= 0.6 and q >= 0.5:
        play C
    elif u >= 0.45 and q >= 0.6:
        play C
    else:
        play D
```
'''

description_OPPORTUNISTIC_21 = '''
Track two internal states: the last observed number of cooperating opponents, and a cooperation streak counter.

Decision rule for round t:

- If t = 1: play C.
- If t = r: play D.
- Otherwise, let `k` be the number of opponents who cooperated in round t−1, and let `p = k / (n−1)`.

Use these thresholds:
- `safe stock` if `stock >= 0.75 * capacity`
- `healthy stock` if `stock >= 0.60 * capacity`
- `fragile stock` if `stock <= 0.40 * capacity`
- `critical stock` if `stock <= 0.25 * capacity`

Play C if any of the following holds:
- `stock` is critical
- `p < 0.50`
- `fragile stock` and `p < 0.75`
- `0.50 <= p < 0.80` and `stock < 0.60 * capacity`

Play D if any of the following holds:
- `t = r`
- `stock >= 0.75 * capacity` and `p >= 0.80`
- `stock >= 0.60 * capacity` and `p >= 0.90`

Update rule after each round:
- If `p >= 0.80`, increment the cooperation streak.
- Otherwise reset the cooperation streak to 0.

Extra opportunism rule:
- If the cooperation streak reaches 2 or more, defect whenever `stock >= 0.60 * capacity`, unless `stock` is fragile or critical.
- If two consecutive rounds have `p < 0.50`, stay in defensive mode and play C only when `stock` is critical; otherwise play D until `p >= 0.75` again.

Edge cases:
- If `n = 2`, replace the thresholds on `p` with `p = 1` for full cooperation and `p = 0` for no cooperation.
- If observations are tied exactly on a threshold, use the stricter action: on `p = 0.50`, defect only when stock is healthy or better; on `p = 0.80`, defect.
- If the observed stock is at or near capacity, prefer D whenever the cooperation signal is strong enough to sustain the stock; if the stock is low, immediately switch to C until recovery.
'''

description_OPPORTUNISTIC_22 = '''
Let \(k_t\) be the number of other players who cooperated in round \(t\), and let \(S_t\) be the stock at the start of round \(t\).

Maintain:
- \(m_t\): running average of observed opponent cooperation rate over past rounds
- \(u_t\): number of rounds since the last time \(k_t = n-1\) was observed
- \(b_t\): number of consecutive rounds in which \(k_t \le \lfloor (n-1)/2 \rfloor\)

Decision rule in round \(t\):

1. Set a baseline cooperation threshold
   \[
   \theta_t = \left\lceil \frac{n-1}{2} \right\rceil
   \]
   and a high-stock threshold
   \[
   H_t = \frac{2}{3}\,\text{capacity}.
   \]

2. If \(t=r\), play \(D\).

3. Else if \(S_t \le \frac{1}{2} \text{capacity}\), play \(D\) unless \(k_{t-1} = n-1\), in which case play \(C\).

4. Else if \(t=1\), play \(C\).

5. Else if \(k_{t-1} \ge \theta_t\), play \(C\).

6. Else if \(k_{t-1} < \theta_t\), play \(D\).

7. Opportunistic override:
   - If \(S_t \ge H_t\) and \(k_{t-1} = n-1\), play \(C\).
   - If \(S_t \ge H_t\) and \(m_t \ge 0.75\), play \(C\).
   - If \(S_t < H_t\) and \(m_t \le 0.5\), play \(D\).

Update rules after each round:
- \(m_{t+1} = \frac{1}{t}\sum_{s=1}^{t} \frac{k_s}{n-1}\)
- If \(k_t = n-1\), set \(u_{t+1}=0\); otherwise \(u_{t+1}=u_t+1\)
- If \(k_t \le \lfloor (n-1)/2 \rfloor\), set \(b_{t+1}=b_t+1\); otherwise \(b_{t+1}=0\)

Escalation rule:
- If \(b_t \ge 2\), play \(D\) until either:
  - \(k_t \ge \theta_t\) in a round, or
  - \(S_t \ge H_t\) and \(k_t = n-1\)
- Once cooperation recovers, return to the baseline rule.

Late-game rule:
- For rounds \(t \ge r-2\), play \(D\) unless \(k_{t-1} = n-1\) and \(S_t \ge H_t\).
- In the final two rounds, cooperate only when the immediately preceding round had full cooperation and the stock is high; otherwise defect.

Interpretation of the play pattern:
- Start cooperatively to test the field.
- Match or reward broad cooperation quickly.
- Defect immediately when cooperation drops below a majority.
- Re-enter cooperation only when the group demonstrates sustained discipline or when the stock is clearly abundant.
- Near the end, switch to extraction mode unless the group is still fully aligned.
'''

description_OPPORTUNISTIC_23 = '''
Use a state-contingent threshold strategy with three modes: harvest, stabilize, and exploit.

Let:
- `S` = current stock before acting
- `k` = number of opponents who cooperated in the previous round
- `m = n - 1` = number of opponents
- `x = k / m` = observed cooperation rate among opponents in the previous round
- `q = S / capacity` = normalized stock level

Decision rule:

1. First round
   - Cooperate if `q ≥ 0.75`.
   - Defect if `q < 0.75`.

2. Main rule in all later rounds
   - Defect if either of these holds:
     - `q ≤ 0.45`
     - `x ≤ 0.50`
   - Cooperate if both of these hold:
     - `q ≥ 0.70`
     - `x ≥ 0.70`
   - Otherwise, use the midpoint rule:
     - Cooperate if `q ≥ 0.60` and `x ≥ 0.60`
     - Defect otherwise

3. Last round
   - Defect unless both of these hold:
     - `q ≥ 0.80`
     - `x ≥ 0.80`
   - If both hold, cooperate.

State memory update after each round:
- Maintain `x_prev = k / (n - 1)`.
- Maintain a running average cooperation rate among opponents:
  - `a_t = (1 - λ) a_{t-1} + λ x_prev`, with `λ = 0.35`
- Replace the raw `x` in the main rule with:
  - `x_eff = 0.5 x_prev + 0.5 a_t`

Adaptive tightening:
- If the previous round had `x_prev ≤ 0.25`, set a temporary punishment state for the next 2 rounds:
  - defect unless `q ≥ 0.85` and `x_prev ≥ 0.75`
- If the previous round had `x_prev ≥ 0.80` for 2 consecutive rounds, set a temporary trust state for the next 2 rounds:
  - cooperate if `q ≥ 0.60`

Opportunistic switching:
- If stock is high (`q ≥ 0.80`) and opponents are broadly cooperative (`x_eff ≥ 0.70`), cooperate to extract high per-round value while preserving the stock.
- If stock is medium (`0.55 ≤ q < 0.80`) and opponents are cooperative, cooperate only when the cooperation signal is stable over at least 2 rounds; otherwise defect.
- If stock is low (`q < 0.55`) or opponents are unreliable (`x_eff < 0.60`), defect.

Anti-exploitation rule:
- If you cooperated last round and `x_prev` dropped by at least `0.25` from the prior round, defect next round regardless of stock unless `q ≥ 0.90` and `x_prev ≥ 0.75`.

Endgame adjustment:
- For the final 3 rounds, increase all defection thresholds by `0.10` in `q`:
  - use `0.55` instead of `0.45`
  - use `0.80` instead of `0.70`
  - use `0.90` instead of `0.80`
- During these rounds, cooperate only under very strong stock and opponent cooperation conditions; otherwise defect.

Compact pseudocode:

```python
def action(round_t, r, S, capacity, x_prev, a_prev, coop_streak):
    q = S / capacity
    x_eff = 0.5 * x_prev + 0.5 * a_prev

    if round_t == 1:
        return "C" if q >= 0.75 else "D"

    if round_t >= r - 2:
        if q >= 0.90 and x_eff >= 0.80:
            return "C"
        return "D"

    if x_prev <= 0.25:
        return "C" if (q >= 0.85 and x_prev >= 0.75) else "D"

    if x_prev >= 0.80 and coop_streak >= 2:
        return "C" if q >= 0.60 else "D"

    if q <= 0.45 or x_eff <= 0.50:
        return "D"

    if q >= 0.70 and x_eff >= 0.70:
        return "C"

    if q >= 0.60 and x_eff >= 0.60:
        return "C"

    return "D"
```

Operational behavior:
- Start cautiously cooperative only when the resource is abundant.
- Reward stable cooperation by matching it with cooperation when the stock remains healthy.
- Immediately punish broad defection or sharp drops in cooperation.
- Exploit cooperative phases by staying cooperative while the stock is high and opponents remain reliable.
- Become increasingly selective near the end, preferring safe extraction over preserving future stock.
'''

description_OPPORTUNISTIC_24 = '''
State variables:
- `S`: current stock before you act this round
- `k`: number of opponents who cooperated in the previous round
- `m = n - 1`: number of opponents
- `ρ = k / m`: observed opponent cooperation rate in the previous round

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Rounds 2 through r-2**
   - If `S <= capacity / 3`, play `C`.
   - Else if `ρ >= 2/3` and `S >= capacity / 2`, play `D`.
   - Else if `ρ >= 1/2` and `S >= 3 * capacity / 5`, play `D`.
   - Else if `ρ <= 1/3`, play `C`.
   - Else play `C`.

3. **Round r-1**
   - If `S <= capacity / 3`, play `C`.
   - Else if `ρ >= 1/2`, play `D`.
   - Else play `C`.

4. **Round r**
   - Play `D`.

Memory update after each round:
- Record `k` from the previous round.
- Update `S` from the game state.
- No player-specific tracking is used beyond the aggregate cooperation count.

Edge handling:
- If `n = 2`, then `ρ` is either `0` or `1`; apply the same thresholds directly.
- If `k` is unavailable because the game has not yet produced a previous round, treat the state as Round 1 behavior.
- If `S` is exactly on a threshold, use the rule written above without interpolation.
- If the observed stock becomes very low after a round, reset to the conservative branch (`C`) until `S > capacity / 3`.

Operational pattern:
- Start by cooperating to preserve stock and collect information.
- Defect immediately when the group shows strong cooperation and the stock is still healthy.
- Return to cooperation whenever cooperation weakens or stock falls into the recovery zone.
- Defect unconditionally at the end.
'''

description_OPPORTUNISTIC_25 = '''
Maintain an estimated opponent cooperation rate \(q_t\) from observed counts, updated after each round with exponential smoothing:

- Let \(m_t\) be the number of opponents who cooperated in round \(t\).
- Set \(q_1 = 1\).
- After round \(t\), update  
  \[
  q_{t+1} = \tfrac{1}{2}q_t + \tfrac{1}{2}\frac{m_t}{n-1}.
  \]

Decision rule for round \(t\):

1. If \(t = r\), play \(D\).
2. If current stock \(S_t = 0\), play \(C\).
3. Otherwise, compute a one-step forecast for each action using \(q_t\).

For action \(a \in \{C,D\}\):

- Own consumption:
  \[
  c(a) =
  \begin{cases}
  S_t/(2n), & a=C\\
  S_t/n, & a=D
  \end{cases}
  \]
- Expected total consumption by the other \(n-1\) players:
  \[
  \hat{C}_{-i} = (n-1)\left[q_t\cdot \frac{S_t}{2n} + (1-q_t)\cdot \frac{S_t}{n}\right]
  \]
- Predicted remaining stock:
  \[
  R(a) = \max\{0,\; S_t - c(a) - \hat{C}_{-i}\}
  \]
- Predicted next stock:
  \[
  S'(a) = \min\{R(a) + 2R(a)(1 - R(a)/\text{capacity}),\; \text{capacity}\}
  \]
- Score:
  \[
  U(a) = c(a) + \lambda_t S'(a),
  \quad \lambda_t = \frac{r-t}{r-t+1}
  \]

Play the action with the larger \(U(a)\).

Tie-breaking:
- If \(U(C)=U(D)\), play \(D\) when \(q_t \ge 1/2\) and \(S_t \ge \text{capacity}/2\).
- Otherwise play \(C\).

Operational behavior by phase:

- First round: play \(C\).
- Early rounds with strong observed cooperation: the rule shifts to \(D\) as soon as the forecast says the stock will remain safely supported.
- If observed cooperation drops or stock weakens, the rule shifts back to \(C\).
- Final round: always \(D\).
- If the stock is at zero, always \(C\) for nonfinal rounds since the choice is irrelevant.

Equivalent short form:

- Start cooperative.
- Harvest with \(D\) whenever the estimated cooperation regime can sustain the stock.
- Revert to \(C\) immediately when the forecasted stock path becomes fragile.
- Never waste the last round on restraint.
'''

description_OPPORTUNISTIC_26 = '''
Let \(c_{t-1}\) be the number of opponents who cooperated in round \(t-1\), and let \(S_t\) be the stock at the start of round \(t\).

Use these constants:
- \(H = \left\lceil \frac{2(n-1)}{3} \right\rceil\)
- \(M = \left\lceil \frac{n-1}{2} \right\rceil\)
- \(L = \frac{\text{capacity}}{3}\)
- \(R = \frac{2\,\text{capacity}}{3}\)

Maintain an exponential cooperation estimate:
- \(\hat q_1 = c_1/(n-1)\)
- \(\hat q_t = 0.7\,\hat q_{t-1} + 0.3\,\big(c_t/(n-1)\big)\) for \(t \ge 2\)

Decision rule for round \(t\):

```text
if t = 1:
    play C

else if t = r:
    play D

else if S_t <= L:
    if c_{t-1} = n-1:
        play C
    else:
        play D

else if S_t >= R:
    if c_{t-1} >= H or \hat q_{t-1} >= 0.70:
        play C
    else:
        play D

else:
    if c_{t-1} >= M and \hat q_{t-1} >= 0.50:
        play C
    else:
        play D
```

State updates after each round:
- After observing \(c_t\), update \(\hat q_t\).
- If \(t=1\), set \(\hat q_1 = c_1/(n-1)\).

Interpretation of the rule:
- Open cooperatively.
- Keep cooperating when the observed cooperation level is strong enough to support the stock.
- Defect whenever observed cooperation falls below a majority-level threshold.
- In low-stock states, cooperate only when the entire opposition is cooperating.
- In the final round, defect.
'''

description_OPPORTUNISTIC_27 = '''
Use a stock-based threshold policy with three modes: harvest, stabilize, and recover.

Let:
- `s` be current stock before the round
- `k` be number of opponents who cooperated in the previous round
- `p = k / (n - 1)` be observed opponent cooperation rate from the previous round
- `t` be the round number
- `m = r - t + 1` be remaining rounds including current

Decision rule:

1. **Last round**
   - Play `D` if `s > 0`
   - Otherwise play `C`

2. **Early and midgame: estimate whether the stock can be preserved**
   - Define the “safe cooperation zone” as:
     - `s >= capacity * 0.60` and `p >= 0.60`
   - Define the “fragile zone” as:
     - `s <= capacity * 0.40` or `p <= 0.40`
   - Define the “transition zone” otherwise

3. **Action selection**
   - If in the **safe cooperation zone**:
     - Play `C`
   - If in the **fragile zone**:
     - Play `D`
   - If in the **transition zone**:
     - Use a momentum rule:
       - Play `C` if both of the following hold:
         - `s >= capacity * 0.50`
         - `p >= 0.50`
       - Otherwise play `D`

4. **Recovery rule after a collapse**
   - If `s <= capacity * 0.20`, play `C` only when:
     - `p >= 0.75`
   - Otherwise play `D`
   - If `s == 0`, play `C` only if at least `n - 1` opponents cooperated in the previous round; otherwise play `D`

5. **Exploitation rule when others are unusually cooperative**
   - If `p >= 0.80` and `s >= capacity * 0.55`, play `D` every third round, starting from the first round in which this condition becomes true
   - In the intervening rounds under the same condition, play `C`
   - If this condition stops holding, reset the count

6. **Defection backlash rule**
   - If `p <= 0.20` in the previous round, play `D` for the next two rounds
   - After those two rounds, re-evaluate from the current state using the main decision rule

7. **First round**
   - Play `C` if `capacity >= 0.75 * capacity` is impossible, otherwise play `C` by default
   - More simply: start with `C`

State update memory:

- After each round, store:
  - `s`
  - `p`
  - whether the previous action was `D` under the exploitation rule
  - whether a backlash period is active

Compact pseudocode:

```text
if t == r:
    action = D if s > 0 else C
else if s <= 0.20 * capacity:
    action = C if p >= 0.75 else D
else if p <= 0.20:
    action = D for next 2 rounds
else if s >= 0.60 * capacity and p >= 0.60:
    action = C
else if s <= 0.40 * capacity or p <= 0.40:
    action = D
else if s >= 0.50 * capacity and p >= 0.50:
    action = C
else:
    action = D

if p >= 0.80 and s >= 0.55 * capacity:
    alternate:
        every 3rd eligible round: D
        otherwise: C
```

Operationally:
- Cooperate when the pool is healthy and others are cooperating.
- Defect when the pool is stressed or the observed cooperation rate drops.
- After strong cooperative behavior by others, take periodic opportunistic defects to capture extra payoff without immediately abandoning the resource.
- When the pool collapses or cooperation falls sharply, switch into repair mode by avoiding overconsumption until the stock and observed cooperation recover.
'''

description_OPPORTUNISTIC_28 = '''
Play cooperatively as the default, but switch to exploitation when the observed cooperation level makes defection safe, and switch back immediately when the stock or cooperation level becomes fragile.

Decision rule each round t:
- Let S be the current stock.
- Let k be the number of opponents who cooperated in the previous round.
- Let m = n - 1 be the number of opponents.
- Let c = k / m be the observed cooperation rate among opponents from the last round.
- Compute the expected stock next round under a fully cooperative round:
  - If you play C and all opponents repeat the same observed behavior, the post-round stock is
    - S_C = S - [ S/(2n) + k·S/(2n) + (m-k)·S/n ]
- Compute the post-round stock if you defect:
  - S_D = S - [ S/n + k·S/(2n) + (m-k)·S/n ]
- Define a safety threshold:
  - safe if S is high enough that one round of defection will not push the stock into a low-stock region:
  - safe when S ≥ 0.6·capacity and c ≥ 0.5
- Define a scarcity threshold:
  - fragile if S < 0.35·capacity or c < 0.5

Action selection:
1. First round:
   - Cooperate.
2. If fragile:
   - Cooperate.
3. If safe:
   - Defect.
4. Otherwise:
   - Cooperate if the last round had at least half of opponents cooperating.
   - Defect if fewer than half of opponents cooperated.
5. Final round:
   - Defect if not fragile.
   - Cooperate only if fragile.

Tighten and loosen behavior with a simple memory rule:
- Maintain a cooperation score q initialized at 1.
- After each round:
  - q ← 0.8q + 0.2c
- Use q instead of c in the above thresholds:
  - replace c ≥ 0.5 with q ≥ 0.5
  - replace c < 0.5 with q < 0.5
- This makes the strategy slow to trust and quick to punish repeated defection, while still returning to cooperation once the group stabilizes.

Edge cases:
- If there are no opponents to observe beyond yourself, always cooperate unless it is the final round, then defect.
- If the previous round left stock at 0, cooperate until stock becomes positive again.
- If the previous round had unanimous cooperation and stock stayed high, defect in the next round to harvest the surplus.
- If the previous round had unanimous defection, cooperate for the next two rounds unless the stock is already safe again, then resume opportunistic defection.

Round-by-round policy in compact form:
```
if t == 1:
    action = C
elif S == 0:
    action = C
elif t == r:
    action = D if S >= 0.35*capacity else C
elif S < 0.35*capacity:
    action = C
elif S >= 0.6*capacity and q >= 0.5:
    action = D
elif q < 0.5:
    action = C
else:
    action = C if c >= 0.5 else D
```

After observing the round:
- Update q with the observed opponent cooperation rate c.
- If you defected and stock fell sharply, keep cooperating until stock recovers above the fragile threshold.
- If opponents return to high cooperation for two consecutive rounds, return to defection immediately once the stock is safe.
'''

description_OPPORTUNISTIC_29 = '''
Maintain three internal quantities:

- `coop_rate`: exponentially weighted estimate of opponent cooperation  
- `streak`: number of consecutive rounds in which opponent cooperation has been high  
- `cooldown`: number of rounds remaining in mandatory recovery mode after you defect

Initialize:
- `coop_rate = 1`
- `streak = 0`
- `cooldown = 0`

At round `t`, with current stock `S` and observed opponent cooperations from the previous round `m`:

**Thresholds**
- `high = ceil(0.8 * (n - 1))`
- `medium = ceil(0.6 * (n - 1))`
- `low = floor(0.5 * (n - 1))`
- `safe_stock = 0.75 * capacity`
- `danger_stock = 0.45 * capacity`

**Update after observing last round**
- `coop_rate = 0.7 * coop_rate + 0.3 * (m / (n - 1))`
- If `m >= high`, set `streak += 1`; otherwise set `streak = 0`
- If `cooldown > 0`, decrement it by 1

**Action rule**

1. **Last round**
   - Play `D`

2. **Recovery / danger mode**
   - If `S <= danger_stock`, play `C`

3. **Mandatory cooldown after exploiting**
   - If `cooldown > 0`, play `C`

4. **Harvest mode**
   - Play `D` if all of the following hold:
     - `S >= safe_stock`
     - `coop_rate >= 0.75`
     - `streak >= 2`
   - After playing `D`, set `cooldown = 2`

5. **Opportunistic snap-defection**
   - If `S >= capacity` and `m >= medium`, play `D`
   - After playing `D`, set `cooldown = 2`

6. **Default**
   - Play `C`

**Behavioral interpretation**
- Start cooperatively.
- Defect only when the pool is healthy and the others have shown sustained cooperation.
- After any defection, immediately return to cooperation for two rounds unless the pool is again clearly safe and the others are still highly cooperative.
- If cooperation weakens or the stock drops, stay cooperative until the pool has rebuilt and cooperation has stabilized.

**Edge cases**
- If `m = 0` or cooperation collapses, stay with `C` until `coop_rate` and `streak` recover.
- If `n = 2`, then `high = medium = 1`, so the strategy becomes: defect only when the other player has cooperated consistently and the stock is safely high.
- If `S` is very close to `0`, always play `C`.
- If the previous round was unavailable because `t = 1`, treat it as `m = n - 1` for the initial update and play `C`.
'''

description_OPPORTUNISTIC_30 = '''
Play cooperatively by default, but switch immediately to defection when the observed cooperation rate drops below the level needed to keep the stock near the sustainable region.

Decision rule each round t with current stock S_t and observed opponent cooperation count k_{t-1} from the previous round:

- Let c_{t-1} = k_{t-1} / (n-1) be the fraction of opponents who cooperated last round.
- Define a cooperation threshold:
  - θ_low = 0.65
  - θ_high = 0.85
- Define stock thresholds:
  - S_safe = 0.75 · capacity
  - S_mid = 0.50 · capacity
  - S_stress = 0.35 · capacity

Action rule:

1. First round:
   - Play C.

2. If S_t ≤ S_stress:
   - Play D.

3. If S_stress < S_t ≤ S_mid:
   - Play C only if c_{t-1} ≥ θ_high.
   - Otherwise play D.

4. If S_mid < S_t ≤ S_safe:
   - Play C if c_{t-1} ≥ θ_low.
   - Otherwise play D.

5. If S_t > S_safe:
   - Play C if c_{t-1} ≥ θ_low.
   - If c_{t-1} < θ_low, play D.

Exploitative escalation rule:
- If the last round had c_{t-1} ≥ θ_high and S_t > S_mid, continue cooperating.
- If the last round had c_{t-1} < θ_low, defect for the next 2 rounds unless stock returns above S_safe and cooperation recovers to at least θ_high.

Punishment and recovery:
- After any round in which c_{t-1} < θ_low, enter punishment mode:
  - Play D until either:
    - c_{t-1} ≥ θ_high for one full observed round, or
    - S_t > S_safe and c_{t-1} ≥ θ_low.
- After two consecutive rounds with c_{t-1} ≥ θ_high, exit punishment mode and return to the main rule.

Last-round rule:
- In the final round, play D if S_t ≥ S_mid.
- Play C only if S_t < S_mid and the previous round had c_{t-1} ≥ θ_high.
- If the final round is preceded by sustained high cooperation and stock is already low, cooperate to avoid being the sole defector in a nearly collapsed pool.

Early-round adjustment:
- In the first 2 rounds, be slightly generous:
  - Round 1: C
  - Round 2: C unless the first-round observed cooperation rate is below θ_low, in which case D.

State-based opportunism:
- If stock is high and opponent cooperation is strong, keep cooperating to preserve the pool.
- If stock is high but opponent cooperation weakens, defect immediately to harvest before depletion accelerates.
- If stock is low, cooperate only when the observed cooperation rate is strong enough to justify rebuilding; otherwise defect to avoid subsidizing free riders.

Pseudocode:

if t == 1:
    action = C
else:
    c = coop_count_last_round / (n - 1)

    if in_punishment_mode:
        if c >= θ_high and S_t > S_mid:
            consecutive_good += 1
            if consecutive_good >= 2:
                exit punishment mode
                action = C
            else:
                action = D
        elif c >= θ_low and S_t > S_safe:
            exit punishment mode
            action = C
        else:
            consecutive_good = 0
            action = D
    else:
        if S_t <= S_stress:
            action = D
            enter punishment mode if c < θ_low
        elif S_t <= S_mid:
            action = C if c >= θ_high else D
        elif S_t <= S_safe:
            action = C if c >= θ_low else D
        else:
            action = C if c >= θ_low else D

Final-round override:
if t == r:
    if S_t >= S_mid or c < θ_low:
        action = D
    else:
        action = C
'''

description_OPPORTUNISTIC_31 = '''
Use a state-contingent threshold policy based on the previous round’s observed cooperation rate and the current stock.

Let:
- \(k_t\) = number of opponents who cooperated in round \(t\)
- \(m_t = n-1\) = number of opponents
- \(c_t = k_t/m_t\) = observed cooperation share among opponents in round \(t\)
- \(S_t\) = stock at the start of round \(t\)

Maintain:
- \(b_t\) = belief score for opponent cooperativeness
- initialize \(b_1 = 1\)

Update after each round:
- \(b_{t+1} = 0.7\,b_t + 0.3\,c_t\)

Decision rule for round \(t\):

1. Compute the current vulnerability of the pool:
   - \(v_t = S_t / \text{capacity}\)

2. Compute the minimum cooperation level needed to justify cooperating:
   - \(q_t = 0.55 + 0.25(1-v_t)\)
   - If \(S_t\) is high, \(q_t\) is near 0.55.
   - If \(S_t\) is low, \(q_t\) rises toward 0.80.

3. Cooperate if and only if both conditions hold:
   - \(b_t \ge q_t\)
   - \(S_t \ge \text{capacity}/4\)

Otherwise defect.

Special round handling:

- Round 1:
  - Cooperate.
  - Start by testing the field while the stock is full.

- Early exploitation response:
  - If in any round \(c_t < 0.5\), set \(b_{t+1} = \min(b_{t+1}, 0.4)\).
  - This makes cooperation unlikely until observed behavior improves.

- Punishment rule:
  - If \(c_t = 0\), defect in the next round regardless of stock unless \(S_t = \text{capacity}\) and \(t=1\).
  - Continue defecting until \(b_t \ge q_t\) again.

- Recovery rule:
  - After any round with \(c_t \ge 0.8\), immediately set \(b_{t+1} = \max(b_{t+1}, 0.85)\).
  - This reopens cooperation quickly when the group is clearly sustaining the pool.

Endgame rule:

- In the last 2 rounds, defect unless:
  - \(c_{t-1} = 1\), \(c_{t-2} = 1\), and
  - \(S_t \ge 0.8\,\text{capacity}\)

In that narrow case, cooperate in both of the final two rounds.

Practical round-by-round behavior:

- If others mostly cooperate and the stock remains healthy, cooperate.
- If cooperation drops or the stock becomes thin, defect.
- If the group restores high cooperation, return to cooperation immediately.
- Never keep cooperating through sustained free-riding.
- Never defect permanently after one bad signal; require only a small streak of strong cooperation to re-enter cooperative play.

Compact pseudocode:

```text
Round 1:
    play C

For round t > 1:
    if t >= r-1:
        if c_{t-1} == 1 and c_{t-2} == 1 and S_t >= 0.8 * capacity:
            play C
        else:
            play D
    else:
        q_t = 0.55 + 0.25 * (1 - S_t / capacity)
        if b_t >= q_t and S_t >= capacity / 4:
            play C
        else:
            play D

After observing c_t:
    b_{t+1} = 0.7 * b_t + 0.3 * c_t
    if c_t < 0.5:
        b_{t+1} = min(b_{t+1}, 0.4)
    if c_t >= 0.8:
        b_{t+1} = max(b_{t+1}, 0.85)
    if c_t == 0:
        mark next round as defect unless endgame exception applies
```
'''

description_OPPORTUNISTIC_32 = '''
Round 1: play C.

After each round t, let o_t be the number of opponents who cooperated, and let ρ_t = o_t / (n - 1).

Maintain a smoothed cooperation estimate:
- e_1 = o_1
- e_t = round(0.6 * o_t + 0.4 * e_{t-1}) for t > 1

Decision rule for round t + 1:

1. If t + 1 = r, play D.

2. Otherwise:
   - Let high_coop = (e_t >= ceil(2(n - 1) / 3))
   - Let medium_stock = (stock >= capacity / 2)
   - Let low_stock = (stock < capacity / 3)
   - Let low_coop = (e_t <= floor((n - 1) / 3))

   Then:
   - If high_coop and medium_stock, play D.
   - Else if low_stock or low_coop, play C.
   - Else:
     - If ρ_t >= 1/2 and stock >= 2 * capacity / 5, play D.
     - Otherwise play C.

Edge cases:
- If the observed cooperation count is unavailable for the first decision, treat e_1 as (n - 1) / 2 and play C.
- If stock is exactly at a threshold, use the more cautious action: C at the low-stock threshold, D only when the high-cooperation condition is strictly satisfied.
- If the last two rounds remain and stock is already at least 2 * capacity / 3, play D in both rounds.
- If opponents defect heavily for two consecutive observed rounds, play C until at least one of the next two observed rounds shows ρ_t >= 1/2.

Core pattern:
- Start by cooperating.
- Defect only when opponents are cooperating at a high rate and the stock is still comfortably high.
- Switch back to cooperation immediately when cooperation drops or stock becomes strained.
- Always defect on the final round.
'''

description_INDIVIDUALISTIC_5 = '''
Round 1: play C.

For round t = 2 to r - 1, let ρ be the fraction of opponents who cooperated in round t - 1, and let s = stock / capacity.

Play C if either of these holds:
- s <= 1/3
- ρ <= 1/3 and s <= 2/3

Otherwise play D.

For the final round: play D.

For the penultimate round:
- if s <= 1/3, play C
- otherwise play D

State update rule used internally:
- Track the last observed cooperation rate ρ_last
- Use the current stock ratio s as the main scarcity signal
- Never switch to sustained cooperation unless low stock makes future depletion costly
- Revert immediately to D once stock is comfortably above the low-stock region

Equivalent compact form:

```text
if t == 1:
    action = C
elif t == r:
    action = D
elif t == r-1:
    action = C if stock <= capacity/3 else D
else:
    ρ = opponents_cooperated_last_round / (n-1)
    if stock <= capacity/3:
        action = C
    elif ρ <= 1/3 and stock <= 2*capacity/3:
        action = C
    else:
        action = D
```

Edge handling:
- If n = 2, then ρ is either 0 or 1 and the same thresholds apply unchanged.
- If no opponents cooperated last round, treat that as ρ = 0.
- If all opponents cooperated last round, treat that as ρ = 1.
- If stock is extremely low, always cooperate until it recovers above capacity/3.
'''

description_INDIVIDUALISTIC_6 = '''
Play cooperatively when the stock is strong and the observed cooperation rate is high; switch to defection when the stock is weak, when opponents are mostly defecting, or when time is running out.

Let:
- \(S_t\) = stock at start of round \(t\)
- \(k_t\) = number of opponents who cooperated in round \(t-1\)
- \(m = n-1\) = number of opponents
- \(c_t = k_t/m\) = observed opponent cooperation rate from the previous round
- \(T_t = \frac{t-1}{r-1}\) = progress through the game, from 0 to 1

Decision rule for round \(t\):

1. **Round 1**
   - Play \(C\) if \(n \le 3\) and \(S_1 \ge 0.8 \cdot \text{capacity}\).
   - Otherwise play \(D\).

2. **Core rule for rounds \(t \ge 2\)**
   - Compute a target cooperation threshold
     \[
     \theta_t = 0.55 - 0.15T_t
     \]
   - Compute a stock threshold
     \[
     \sigma_t = 0.45 \cdot \text{capacity} + 0.25(\text{capacity} - S_t)
     \]
   - Cooperate iff all three conditions hold:
     - \(S_t \ge \sigma_t\)
     - \(c_t \ge \theta_t\)
     - \(S_t \ge \frac{\text{capacity}}{2}\) or \(c_t \ge 0.75\)

3. **Pressure response**
   - If the previous round stock dropped by more than 20% of capacity, play \(D\) for the next 2 rounds.
   - If the previous round stock increased and \(c_t \ge 0.75\), return to \(C\).

4. **Endgame**
   - For the last 3 rounds, play \(D\) unless both:
     - \(c_t = 1\) in the previous round, and
     - \(S_t \ge 0.75 \cdot \text{capacity}\)

5. **Emergency rule**
   - If \(S_t \le \frac{\text{capacity}}{n}\), play \(D\) until \(S_t > \frac{\text{capacity}}{n}\) and \(c_t \ge 0.5\).

Tie-breaking and default behavior:
- If no previous opponent history exists, use the round-1 rule.
- If \(k_t\) is missing because no prior round exists, assume \(c_t = 0\).
- If \(S_t\) is exactly on a threshold, choose \(D\).

Operational mindset:
- Start cautiously.
- Reward sustained cooperation immediately.
- Punish visible overuse quickly.
- Restore cooperation only after the stock and opponent behavior both recover.
'''

description_INDIVIDUALISTIC_7 = '''
Initialize `q = 1`, an estimate of opponent cooperation rate, and update it after each round with exponential smoothing:

`q := 0.7*q + 0.3*(observed_cooperators / (n-1))`

Decision rule in round `t` with current stock `S` and `m = r - t + 1` rounds remaining:

1. **Last round (`t = r`)**  
   Play `D`.

2. **First round (`t = 1`)**  
   Play `C`.

3. **Rounds 2 through `r-1`**  
   Compute the expected next-stock under each action, using the current `q`:

   - Expected total opponent consumption if you play `C`:
     `oppC = (n-1) * (q * S/(2n) + (1-q) * S/n)`
   - Expected total opponent consumption if you play `D`:
     same as above

   Then:
   - `nextC` = stock after your `C`, expected opponent consumption, and regrowth
   - `nextD` = stock after your `D`, expected opponent consumption, and regrowth

   Choose `C` iff all three conditions hold:
   - `q >= 0.5`
   - `S >= 0.35 * capacity`
   - `(m > 2 and nextC >= nextD) or (m = 2 and nextC > 0.85 * capacity)`

   Otherwise play `D`.

4. **Rapid-response override**
   - If the observed number of cooperators in the previous round is `0`, play `D` until the observed cooperation rate over the last two rounds rises above `0.5`.
   - If the stock is below `0.2 * capacity`, play `C` only when `q >= 0.75`; otherwise play `D`.

5. **Endgame tightening**
   - In the final two rounds, cooperate only if the stock is already high and opponent cooperation is strong:
     - Round `r-1`: play `C` only if `S >= 0.85 * capacity` and `q >= 0.75`; else `D`.
     - Round `r`: always `D`.

6. **Behavioral reset**
   - If cooperation drops for two consecutive rounds, reset `q := min(q, 0.25)` and switch to the conservative rule above.
   - If cooperation rises for two consecutive rounds, set `q := max(q, 0.75)` and allow `C` under the stock threshold rule.

This strategy starts by probing with cooperation, then switches to a self-protective extraction mode unless the observed behavior of others makes preservation clearly worthwhile.
'''

description_INDIVIDUALISTIC_8 = '''
Round 1: play C.

Round r: play D.

For every intermediate round t = 2, 3, ..., r-1:

1. Let `S` be the current stock.
2. Let `c` be the number of opponents who cooperated in round `t-1`.
3. Let `p = c / (n - 1)`.

Decision rule:
- If `S <= capacity / 3`, play D.
- Else if `S >= 5 * capacity / 6` and `p >= 2/3`, play C.
- Else if `S >= capacity / 2` and `p >= 1/2`, play C.
- Else play D.

Tie-breaking and edge cases:
- If `n = 2`, interpret `p` as either `0` or `1`; the same thresholds apply.
- If `S` is exactly on a threshold, use the action listed for that threshold.
- If the observed stock is extremely low (`S < capacity / 6`), always play D until `S > capacity / 3`.
- If the observed stock rises for two consecutive rounds and at least half of opponents cooperated in the latest round, upgrade one step only: from D to C when `S >= capacity / 2`, otherwise stay with the default D.
- Never cooperate in the final round, regardless of history.
'''

description_INDIVIDUALISTIC_9 = '''
Use a stock-preserving threshold policy with aggregate reciprocity.

Let:
- `S_t` be the stock at the start of round `t`
- `c_{t-1}` be the number of opponents who cooperated in round `t-1`
- `k_t = c_{t-1} / (n-1)` be the observed opponent cooperation rate from the previous round
- `q_t = S_t / capacity` be the current stock fraction

Decision rule for round `t`:

1. **First round**
   - Play `C` if `capacity >= 4n`
   - Otherwise play `D`

2. **Rounds 2 through r-1**
   - Play `C` if both conditions hold:
     - `k_t >= 1/2`
     - `q_t >= 1/2`
   - Otherwise play `D`

3. **Last round**
   - Play `C` if `k_t == 1`
   - Otherwise play `D`

Update logic after each round:
- If `t < r`, observe `c_t` and compute `k_{t+1} = c_t / (n-1)`

Fallback rules for edge cases:
- If `S_t = 0`, play `D`
- If `n = 2`, then `k_t` is either `0` or `1`; apply the same thresholds directly
- If previous observation is unavailable for any reason, treat `k_t = 0` and play `D`

Behavioral posture:
- Start cooperative only when the initial state is sufficiently rich
- Continue cooperating only under sustained majority cooperation and healthy stock
- Immediately switch to `D` after weak cooperation or low stock
- On the final round, cooperate only under full observed cooperation, otherwise take the higher immediate extraction
'''

description_INDIVIDUALISTIC_10 = '''
Always use the smallest action that preserves the stock when the stock is healthy, and switch to the larger action only when the stock is already in a danger zone or when opponents have clearly escalated.

Decision rule:

Let S be the current stock at the start of the round, k be the number of observed opponent cooperators in the previous round, and m = n - 1 be the number of opponents.

1. First round:
- Play C.

2. General round t > 1:
- Compute the previous round’s opponent cooperation rate:
  q = k / m

- Compute the current stock fraction:
  x = S / capacity

- Play C if all of the following hold:
  - x ≥ 1/2
  - q ≥ 1/2

- Play D if any of the following hold:
  - x < 2/n
  - q < 1/2

- If neither condition clearly applies, play C when x ≥ 1/3, otherwise play D.

Endgame rule:
- In the final round, play D if x < 1/2; otherwise play C.

Adaptation rule across rounds:

- If you played C last round and observed q = 1, keep playing C as long as x remains at least 1/2.
- If you played C last round and observed q ≤ 1/2, switch to D until q returns above 1/2.
- If you played D last round and the stock fraction drops below 1/3, continue D.
- If the stock rebounds to x ≥ 1/2 and opponents’ cooperation rate returns to q ≥ 1/2, return to C.

Fallback rule:
- When the observation is ambiguous or the stock is near the threshold, prefer C unless the stock is already low; never continue cooperating once the stock is below 2/n.

Pseudocode:

if t == 1:
    action = C
else:
    q = coop_count_prev_round / (n - 1)
    x = stock / capacity

    if t == r:
        action = D if x < 0.5 else C
    else if x < 2 / n:
        action = D
    else if q < 0.5:
        action = D
    else if x >= 0.5:
        action = C
    else if x >= 1 / 3:
        action = C
    else:
        action = D

State update heuristic:
- After each round, if the stock increased or stayed near capacity, treat the environment as cooperative and remain in C mode.
- If the stock fell sharply or the observed cooperation rate dropped, enter D mode until both stock and cooperation recover.

Core mindset:
- Start cooperative, defend against exploitation by reacting to observed free-riding, and protect the resource once depletion becomes visible.
'''

description_INDIVIDUALISTIC_11 = '''
Initialize a trust score `T = 1`.

Round 1:
- Play `C`.

After each round `t`, observe:
- `k_t` = number of opponents who played `C`
- `ρ_t = k_t / (n - 1)` if `n > 2`, and `ρ_t = k_t` if `n = 2`

Update trust:
- `T ← 0.6T + 0.4ρ_t`

For each round `t = 2, ..., r`:
1. If `t = r`, play `D`.
2. Else if `stock / capacity < 0.35`, play `D`.
3. Else if `T < 0.55`, play `D`.
4. Else if `k_{t-1} < ceil((n - 1)/2)`, play `D`.
5. Else if `stock` has dropped by more than `0.15 × capacity` since the previous round, play `D`.
6. Otherwise, play `C`.

Reset rule:
- If any round triggers `D` because `ρ_t < 0.5` or the stock falls below `0.35 × capacity`, continue playing `D` until both:
  - `ρ_t ≥ 0.5`, and
  - `stock / capacity ≥ 0.50`.

Compact form:
- Start by cooperating.
- Keep cooperating only while the pool remains healthy and a majority of opponents are cooperating.
- The moment the group stops sustaining the stock, switch to extraction.
- Always defect in the final round.
'''

description_INDIVIDUALISTIC_12 = '''
Let \(S_t\) be the stock at the start of round \(t\), and let \(k_t\) be the number of opponents who cooperated in round \(t-1\).

Define the observed cooperation rate among opponents:
\[
q_t=\frac{k_t}{n-1}
\]
for \(t\ge 2\).

Use the following decision rule each round:

### Round 1
Play \(C\).

### Round \(t\ge 2\)
Compute the expected stock after this round under each action, using the observed cooperation rate from the previous round as the forecast for the current round:

- If you play \(C\), expected total consumption is
\[
\frac{S_t}{2n} + (n-1)\left(q_t\frac{S_t}{2n} + (1-q_t)\frac{S_t}{n}\right)
\]
- If you play \(D\), expected total consumption is
\[
\frac{S_t}{n} + (n-1)\left(q_t\frac{S_t}{2n} + (1-q_t)\frac{S_t}{n}\right)
\]

Let the corresponding expected remaining stock be
\[
R_C = S_t - \text{expected total consumption under } C,
\quad
R_D = S_t - \text{expected total consumption under } D.
\]

Compute the post-growth expected stock:
\[
G(x)=\min\left(x + 2x\left(1-\frac{x}{\text{capacity}}\right),\ \text{capacity}\right).
\]

Estimate next-round stock as:
\[
\hat S_{t+1}^{(C)} = G(R_C),\qquad \hat S_{t+1}^{(D)} = G(R_D).
\]

Estimate the total one-step-plus-future value of each action by:
\[
V(C)=\frac{S_t}{2n} + \lambda \hat S_{t+1}^{(C)},
\qquad
V(D)=\frac{S_t}{n} + \lambda \hat S_{t+1}^{(D)},
\]
with discount weight
\[
\lambda = \frac{r-t}{r-t+1}.
\]

Choose:
- \(D\) if \(V(D) > V(C)\)
- \(C\) if \(V(C) > V(D)\)
- on ties, choose \(C\) if \(S_t \ge \frac{\text{capacity}}{2}\), otherwise choose \(D\)

### Simplified threshold form
Because the immediate gain from defecting is exactly \(S_t/(2n)\), defect only when the predicted future stock loss is not large enough to offset that gain. Equivalently:

- Cooperate if the predicted next-round stock under defection would be lower by more than
\[
\frac{S_t}{2n\lambda}
\]
than under cooperation.
- Otherwise defect.

### Reaction rule to observed cooperation
Maintain a cooperation threshold:
\[
\tau_t = \frac{1}{2} + \frac{1}{2}\left(1-\frac{S_t}{\text{capacity}}\right).
\]

Interpretation of the threshold:
- when stock is high, require roughly majority cooperation to keep cooperating;
- when stock is low, become more defensive.

Then apply:
- if \(q_t \ge \tau_t\), cooperate unless \(S_t\) is very low;
- if \(q_t < \tau_t\), defect.

“Very low” means:
\[
S_t \le \frac{\text{capacity}}{4}
\]
in which case always defect.

### Last-round rule
In round \(r\), play \(D\) unless the current stock is at least
\[
\frac{\text{capacity}}{2}
\]
and at least half of opponents cooperated in round \(r-1\).
If both hold, play \(C\).

### Full policy in compact form
1. Round 1: \(C\).
2. If \(S_t \le \text{capacity}/4\): \(D\).
3. Else if \(t=r\): \(C\) only when \(S_t \ge \text{capacity}/2\) and \(q_t \ge 1/2\); otherwise \(D\).
4. Else:
   - predict \(\hat S_{t+1}^{(C)}\) and \(\hat S_{t+1}^{(D)}\) from \(q_t\),
   - choose the action with larger \(V(\cdot)\),
   - break ties in favor of \(C\) when stock is high, \(D\) when stock is low.

### Individualistic mindset
Always select the action that maximizes your own expected cumulative payoff using the current stock, observed opponent cooperation rate, and remaining rounds. Never cooperate to “help” the group unless doing so increases your own expected future payoff. When the environment becomes exploitative or stock becomes scarce, switch immediately to defection.
'''

description_INDIVIDUALISTIC_13 = '''
Use a stock-preserving threshold policy with short-memory retaliation:

**State variables**
- `c_t`: number of opponents who cooperated in round `t`
- `m_t = c_t / (n - 1)`: observed opponent cooperation rate
- `avg_m`: moving average of opponent cooperation rate over the last `L = min(3, t-1)` rounds, initialized to `1`
- `bad`: consecutive rounds in which `m_t < 0.5`
- `S_t`: current stock at the start of round `t`

**Decision rule**
1. **Round 1**
   - Play `C`.

2. **Round 2 and later**
   - Let `coop_threshold = 0.70`
   - Let `stock_threshold = 0.75 * capacity`
   - Let `depletion_threshold = 0.55 * capacity`

   Play `C` if and only if all of the following hold:
   - `S_t >= stock_threshold`
   - `avg_m >= coop_threshold`
   - `bad == 0`

   Otherwise play `D`.

**Update rules after each round**
- Update `avg_m` as the average of the last up to 3 observed `m_t` values.
- Update `bad`:
  - If `m_t < 0.5`, set `bad = bad + 1`
  - Else set `bad = 0`

**Escalation rule**
- If `S_t < depletion_threshold`, play `D` for the rest of the game unless both:
  - `avg_m = 1`, and
  - `S_t` has increased for two consecutive rounds
- If the stock is very low, never voluntarily cooperate:
  - If `S_t <= 0.35 * capacity`, play `D`

**Last-round rule**
- In the final round, play `D` unless both:
  - `m_{t-1} = 1`, and
  - `S_t >= stock_threshold`
- If the final round is also the first round, play `C`.

**Tie-breaking and edge cases**
- If `n = 2`, treat `m_t` as either `0` or `1` and apply the same thresholds.
- If `t < 3`, compute `avg_m` over all observed prior rounds only.
- If the observed opponent count is unavailable for a round, treat that round as `m_t = 0.5`.
- If two or more consecutive rounds produce the same stock level, keep the current `bad` value unchanged.

**Behavioral style**
- Start cooperative to test whether the group sustains the resource.
- Continue cooperating only while opponents collectively maintain high cooperation and the stock remains comfortably above depletion levels.
- Switch to defection immediately after repeated weak cooperation, low stock, or clear signs of overuse.
- Never “forgive” a deteriorating group unless the resource visibly recovers and cooperation returns to near-universal levels.
'''

description_INDIVIDUALISTIC_14 = '''
Round 1:
- Play C.

For each round t > 1, let S be the current stock and let c be the number of opponents who cooperated in the previous round.

Decision rule:
1. If t is one of the last two rounds, play D if S > capacity / 3; otherwise play C.
2. Else if S <= capacity / 3, play C.
3. Else if c >= ceil(2(n - 1) / 3) and S >= capacity / 2, play D.
4. Else if c <= floor((n - 1) / 3), play C.
5. Else if S >= 2 * capacity / 3, play D.
6. Otherwise, play C.

Equivalent pseudocode:
```text
if t == 1:
    action = C
else:
    ρ = c / (n - 1)

    if t >= r - 1:
        action = D if S > capacity / 3 else C
    elif S <= capacity / 3:
        action = C
    elif ρ >= 2/3 and S >= capacity / 2:
        action = D
    elif ρ <= 1/3:
        action = C
    elif S >= 2 * capacity / 3:
        action = D
    else:
        action = C
```

Ties and boundary values:
- Use C whenever S is exactly on a lower threshold unless a later rule explicitly selects D.
- Use D only when the stock is comfortably high or the game is near the end.
- If n = 2, interpret c / (n - 1) as 0 or 1 exactly.

Behavioral principle:
- Stay conservative when the stock is fragile.
- Exploit high-stock periods when others are cooperating enough to keep the pool replenished.
- Shift to D at the end to capture remaining value.
'''

description_INDIVIDUALISTIC_15 = '''
Initialize:
- Set `S = capacity`.
- Set `p̂ = 1/2` as the initial estimated opponent cooperation rate.
- Set smoothing weight `α = 1/2`.

For each round `t = 1, ..., r`:

1. **Terminal rounds**
   - If `t = r` or `t = r - 1`, play `D`.

2. **Update belief from the previous round**
   - If `t > 1`, observe `c`, the number of opponents who played `C` in round `t-1`.
   - Let `q = c / (n - 1)`.
   - Update the estimated opponent cooperation rate:
     - `p̂ ← α q + (1 - α) p̂`

3. **Set a personal conservation threshold**
   - `T = capacity * (0.30 + 0.20 * (1 - p̂))`
   - This makes you more conservative when opponents cooperate less.

4. **Compute the stock you expect next round under each action**
   - Let
     - `opp_cons = c * S/(2n) + (n - 1 - c) * S/n`
   - If you play `C`:
     - `S_rem_C = S - opp_cons - S/(2n)`
     - `S_next_C = min(S_rem_C + 2 * S_rem_C * (1 - S_rem_C / capacity), capacity)`
   - If you play `D`:
     - `S_rem_D = S - opp_cons - S/n`
     - `S_next_D = min(S_rem_D + 2 * S_rem_D * (1 - S_rem_D / capacity), capacity)`

5. **Decision rule**
   - Play `C` if either of the following holds:
     - `S <= T`
     - `S_next_D < T` and `S_next_C >= T`
   - Otherwise play `D`

6. **First round**
   - Since there is no history yet, play `D`.

State update after the round:
- After observing the round outcome, update `S` exactly using the realized actions and the stock-growth rule, then proceed to the next round.

Behavioral summary:
- Defect by default when stock is healthy.
- Cooperate only when stock preservation is needed or when defecting would push the system below your chosen conservation threshold.
- Become stricter about conserving stock when opponents have recently cooperated less.
- Always defect in the last two rounds.
'''

description_INDIVIDUALISTIC_16 = '''
**Strategy: Stock-Guarded Conditional Cooperation**

Let:

- `S_t` = stock at the start of round `t`
- `k_t` = number of observed opponent cooperators in round `t-1`  
  (for `t=1`, no history yet)
- `x_t = k_t / (n-1)` = observed opponent cooperation rate from the previous round
- `T_t = S_t / (2n)` = own cooperative consumption in round `t`
- `U_t = S_t / n` = own defect consumption in round `t`

### 1) First round
Play `C`.

### 2) Main decision rule for rounds `t >= 2`
Compute the previous-round cooperation rate among opponents, `x_t`.

Play `C` if and only if all of the following hold:

1. `x_t >= 0.5`
2. `S_t >= 2n`
3. `S_t < capacity` is not needed separately; stock is already bounded
4. `t < r`

Otherwise play `D`.

### 3) Endgame rule
For the final round `t = r`, play `D`.

### 4) Escalation / retaliation rule
If in the previous round fewer than half of opponents cooperated, switch immediately to `D` in the next round.

If two consecutive rounds have `x_t < 0.5`, then continue playing `D` until a round occurs with `x_t >= 0.5` again and `S_t >= 2n`.

### 5) Recovery rule
After defecting, return to cooperation only when both conditions are met:

- opponents cooperated at least half the time in the most recent round: `x_t >= 0.5`
- current stock is comfortably viable: `S_t >= 2n`

### 6) Individualistic tie-breakers
If the decision is borderline, prefer `D` whenever any of these are true:

- `S_t < 2n`
- `x_t < 0.5`
- `t = r`

If all are false, play `C`.

### 7) Compact pseudocode
```text
if t == 1:
    action = C
elif t == r:
    action = D
else:
    x = coop_opponents_last_round / (n - 1)
    if S_t >= 2n and x >= 0.5:
        action = C
    else:
        action = D
```

### 8) Behavioral style
- Start cooperative to probe the environment.
- Keep cooperating only when others show sustained restraint.
- Defect immediately when the group becomes exploitative or the stock becomes fragile.
- Never cooperate in the final round.
- Treat cooperation as conditional, not moral: preserve access to the pool first, cooperate only when the observed behavior of others supports it.
'''

description_INDIVIDUALISTIC_17 = '''
Use a conservative tit-for-survival policy:

**State variables**
- `h_t`: number of opponents who cooperated in round `t-1`
- `q_t = h_t / (n-1)`: observed opponent cooperation rate from the previous round
- `x_t = stock / capacity`: current stock ratio

**Decision rule in round `t`**
1. **If `t = 1`**: play `C`.
2. **If `t >= r-1`**: play `D`.
3. **Otherwise**:
   - Play `C` only if both conditions hold:
     - `x_t >= 0.70`
     - `q_t >= 0.50`
   - In all other cases, play `D`.

**Adaptive tightening**
- After any round in which `q_t < 0.50`, increase the cooperation threshold for future rounds by requiring `q >= 0.75` before cooperating again.
- After any round in which `x_t < 0.50`, play `D` until the stock recovers to `x_t >= 0.70`.

**Tie and edge handling**
- If the observed cooperation rate is exactly on the threshold, treat it as sufficient.
- If `n = 2`, then `q_t` is either `0` or `1`; cooperate only after observing the other player cooperate in the previous round and the stock ratio is at least `0.70`.
- If the stock ever becomes very low, below `x_t < 0.35`, switch to unconditional `D` for the rest of the game.

**Individualistic mindset**
- Default to `D` whenever the continuation value is unclear.
- Use `C` only when the stock is healthy and the observed behavior of others indicates that conserving the pool is currently profitable.
- Never cooperate to reward others; cooperate only to preserve a high stock level for your own future rounds.
'''

description_INDIVIDUALISTIC_18 = '''
Let \(k_t\) be the number of opponents who cooperated in round \(t\), so the observed cooperation rate among opponents is
\[
q_t=\frac{k_t}{n-1}.
\]
Let \(S_t\) be the stock at the start of round \(t\).

Maintain two internal variables:

- \(b_t\): baseline cooperation rate, initialized as \(b_1=1\)
- \(m_t\): consecutive rounds with \(q_t < 1/2\), initialized as \(m_1=0\)

Decision rule in round \(t\):

1. **Last round**
   - Play \(D\).

2. **Round 1**
   - Play \(C\).

3. **Normal play**
   - Compute the stock threshold
     \[
     \theta_t=\frac{n}{2n-1}\,S_t.
     \]
   - If \(S_t \le \theta_t\), play \(D\).
   - If \(S_t > \theta_t\), compare opponent cooperation to the baseline:
     - If \(q_{t-1} \ge b_t\), play \(C\).
     - If \(q_{t-1} < b_t\), play \(D\).

Update rules after observing round \(t\):

- Update baseline cooperation by exponential smoothing:
  \[
  b_{t+1}=0.8\,b_t+0.2\,q_t.
  \]
- If \(q_t < 1/2\), set \(m_{t+1}=m_t+1\); otherwise set \(m_{t+1}=0\).

Persistent low-cooperation response:

- If \(m_t \ge 2\), then from the next round onward require a stricter standard:
  - play \(C\) only if \(q_{t-1}=1\) and \(S_t>\theta_t\)
  - otherwise play \(D\)

Very low stock response:

- If \(S_t < \frac{n-1}{2n-1}\,S_{t-1}\) for two consecutive rounds, switch to permanent \(D\) for the rest of the game.

Interpretation of the policy:

- Start with cooperation to test the environment.
- Cooperate only while opponents are cooperating enough to keep the pool valuable.
- Defect immediately when stock is too low for cooperation to be worthwhile.
- Escalate to strict defection after repeated under-cooperation.
- End with defection in the final round to capture the immediate advantage.
'''

description_INDIVIDUALISTIC_19 = '''
- Maintain a binary mode: `exploit` or `preserve`.
- Start in `exploit`.

Decision rule each round `t` with current stock `S_t` and last-round opponent cooperation count `k_{t-1}`:

1. **Round 1**
   - Play `D`.

2. **Update mode after each observed round**
   - Let `q_{t-1} = k_{t-1} / (n-1)` be the opponent cooperation fraction in the previous round.
   - If `q_{t-1} >= 2/3` and the stock has not fallen sharply, switch to `preserve`.
   - Otherwise switch to `exploit`.

3. **Sharp-fall test**
   - Define `sharp fall` as either:
     - `S_t < 0.7 * capacity`, or
     - `S_t < S_{t-1} - 0.15 * capacity` if `t > 1`.

4. **Action in preserve mode**
   - Play `C` if both conditions hold:
     - `S_t >= 0.6 * capacity`
     - `q_{t-1} >= 2/3`
   - Otherwise play `D`.

5. **Action in exploit mode**
   - Play `D`.
   - Exception: if `S_t >= 0.9 * capacity` and `q_{t-1} = 1`, play `C` for one round, then return to the normal mode update.

6. **Low-stock lockout**
   - If `S_t <= 0.4 * capacity`, play `D` until both:
     - `S_t >= 0.7 * capacity`, and
     - `q_{t-1} >= 2/3`.

7. **Last round**
   - Always play `D`.

8. **If history is unavailable**
   - Treat missing `q_{t-1}` as `0` and play `D`.

Pseudocode:

```text
if t == 1 or t == r:
    play D
else:
    q = k_prev / (n - 1)

    sharp_fall = (S < 0.7*capacity) or (t > 1 and S < S_prev - 0.15*capacity)

    if S <= 0.4*capacity:
        play D
    else if q >= 2/3 and not sharp_fall:
        if S >= 0.6*capacity:
            play C
        else:
            play D
    else:
        if S >= 0.9*capacity and q == 1:
            play C
        else:
            play D
```


'''

description_INDIVIDUALISTIC_20 = '''
Use a state-based threshold policy with personal reserve accounting:

Let:
- `S_t` = stock at start of round `t`
- `k_t` = number of opponents who cooperated in round `t-1`
- `m_t = n - 1` = number of opponents
- `x_t = k_t / m_t` = observed opponent cooperation rate from last round
- `L_t` = my cumulative payoff so far
- `T = r - t + 1` = rounds remaining including current one

Define two target stock thresholds:
- `H_t = 0.75 * capacity` for high-stock rounds
- `M_t = 0.45 * capacity` for medium-stock rounds
- `L_t = 0.20 * capacity` as the floor below which I conserve aggressively

Decision rule for round `t`:

1. First round:
- Play `C`.

2. Last round:
- Play `D` if `S_t > 0`, otherwise play `C` only if forced by a zero-stock edge case.
- If `S_t` is very low (`S_t <= capacity / (4n)`), play `C`; otherwise play `D`.

3. Intermediate rounds:
- If `S_t <= L_t`, play `C`.
- Else if `S_t >= H_t`:
  - Play `D` if `x_t < 0.5`
  - Play `C` if `x_t >= 0.5`
- Else if `S_t >= M_t`:
  - Play `C` if `x_t >= 0.75`
  - Play `D` otherwise
- Else:
  - Play `C` if `x_t >= 0.9`
  - Play `D` otherwise

4. Momentum adjustment:
- If the last two observed cooperation rates both fell by at least `0.2`, shift one level more selfish for the current round:
  - `C -> D`
  - otherwise keep the rule above unchanged.
- If the last two observed cooperation rates both rose by at least `0.2`, shift one level more cooperative for the current round:
  - `D -> C`
  - otherwise keep the rule above unchanged.

5. Personal-payoff protection:
- If my cumulative payoff per completed round is below `capacity / (4n)` and `S_t > M_t`, play `D`.
- If my cumulative payoff per completed round is above `capacity / (2n)` and `S_t < H_t`, play `C`.

6. Zero-information fallback:
- If any observed history is unavailable, default to:
  - `C` in the first half of the game
  - `D` in the second half unless `S_t <= L_t`, in which case `C`

Pseudocode:

```text
if t == 1:
    action = C
elif t == r:
    if S_t <= capacity / (4n):
        action = C
    else:
        action = D
else:
    if S_t <= 0.20 * capacity:
        action = C
    else:
        if last_two_coop_rates_available:
            if coop_rate[t-1] <= coop_rate[t-2] - 0.2:
                selfish_shift = +1
            elif coop_rate[t-1] >= coop_rate[t-2] + 0.2:
                selfish_shift = -1
            else:
                selfish_shift = 0
        else:
            selfish_shift = 0

        if S_t >= 0.75 * capacity:
            base = C if x_t >= 0.5 else D
        elif S_t >= 0.45 * capacity:
            base = C if x_t >= 0.75 else D
        else:
            base = C if x_t >= 0.9 else D

        action = shift(base, selfish_shift)

    if avg_payoff_so_far < capacity / (4n) and S_t > 0.45 * capacity:
        action = D
    if avg_payoff_so_far > capacity / (2n) and S_t < 0.75 * capacity:
        action = C
```

`shift(C, +1)=D`, `shift(D, -1)=C`, otherwise unchanged.

Round-by-round posture:
- Start cooperative.
- Punish sustained low cooperation by defecting.
- Preserve stock when the pool is low.
- Defect in the final round unless the stock has collapsed.
- Reopen cooperation immediately when observed cooperation recovers and stock is healthy.
'''

description_INDIVIDUALISTIC_21 = '''
Initialize:
- `q̂ = 1`  (expected cooperation rate among opponents)
- `λ = 0.7`  (smoothing for the cooperation estimate)
- `reserve = 0.45 * capacity`
- `comfort = 0.75 * capacity`

At round `t` with current stock `S` and observed previous-round cooperation count `k` among the `n-1` opponents:

1. Update the cooperation estimate after round 1 onward:
   - `q̂ ← λ*q̂ + (1-λ)*(k/(n-1))`

2. Compute expected number of cooperating opponents:
   - `m ← (n-1) * q̂`

3. Compute expected stock after this round if you cooperate vs defect:
   - If you cooperate:
     - `cons_C ← S/(2n) * (m + 1) + S/n * ((n-1) - m)`
   - If you defect:
     - `cons_D ← S/(2n) * m + S/n * ((n-1) - m + 1)`
   - `R_C ← S - cons_C`
   - `R_D ← S - cons_D`
   - `N_C ← min(R_C + 2*R_C*(1 - R_C/capacity), capacity)`
   - `N_D ← min(R_D + 2*R_D*(1 - R_D/capacity), capacity)`

Decision rule:

- If `t == 1`: play `C`
- Else if `t == r`: play `D`
- Else if `t == r-1`: play `D` if `S > reserve`, otherwise `C`
- Else if `S <= reserve`: play `C`
- Else if `S >= comfort` and `q̂ < 0.5`: play `D`
- Else if `N_C > N_D` and `q̂ >= 0.5`: play `C`
- Else if `q̂ >= 0.65`: play `C`
- Else: play `D`

Fallback tie-break:
- If two branches are equally applicable, choose `D` unless `S <= reserve`, in which case choose `C`.

Behavioral stance:
- Start conservatively with one cooperative round to measure the environment.
- Cooperate only when recent behavior suggests the pool is being maintained or when stock is low enough that conserving it is individually valuable.
- Defect whenever the pool is comfortably high and opponents are not sufficiently cooperative.
- Always defect in the final round, and in the penultimate round unless the stock is already near the reserve floor.
'''

description_INDIVIDUALISTIC_22 = '''
Round 1:
- Play D.

For round t > 1, let c be the number of opponents who cooperated in round t−1, and let S be the current stock.

Decision rule:
1. If t = r, play D.
2. Else if S = 0, play D.
3. Else if S <= capacity / 3, play C.
4. Else if c >= ceil((n − 1) / 2), play D.
5. Else play C.

Update logic after each round:
- Record the observed opponent cooperation count c from that round.
- Use only the most recent observation and the current stock for the next decision.

Edge handling:
- If multiple conditions apply, follow the rule order above.
- If the stock is very low but nonzero, cooperation takes priority over exploitation.
- If opponents are mostly cooperative, switch to D immediately to extract more while the pool is still healthy.
- If opponents are mostly defecting, switch to C to slow depletion and keep the resource usable.
'''

description_INDIVIDUALISTIC_23 = '''
Round 1: play D.

For every later round t:

1. Let S be the current stock.
2. Let m be the number of opponents who cooperated in round t-1.
3. Compute the projected next stock under each action:
   - If you play D:
     - remaining = S * m / (2n)
     - next_D = remaining + 2 * remaining * (1 - remaining / capacity)
   - If you play C:
     - remaining = S * (m + 1) / (2n)
     - next_C = remaining + 2 * remaining * (1 - remaining / capacity)

Decision rule:
- If next_D < 0.55 * capacity and next_C >= 0.55 * capacity, play C.
- Else if S >= 0.85 * capacity and m <= (n - 1) / 2, play D.
- Else if m >= ceil(3 * (n - 1) / 4) and S >= 0.70 * capacity, play D.
- Else play D.

Last round: play D.

Penultimate round:
- Use the same rule, except if S < 0.35 * capacity, play C to protect the final-round stock level.

If no observation is available because t = 1, treat the situation as the default defect case.
'''

description_INDIVIDUALISTIC_24 = '''
Maintain a running cooperation score and use it to decide whether the pool is worth preserving.

Let \(q_t\) be your smoothed estimate of opponent cooperation before round \(t\):
- Initialize \(q_1 = 1\)
- After each round, if \(k_t\) of the \(n-1\) opponents cooperated, update
  \[
  q_{t+1} = \tfrac{2}{3}q_t + \tfrac{1}{3}\frac{k_t}{n-1}
  \]

Decision rule in round \(t\) with current stock \(S_t\):

1. **If \(S_t = 0\):** play \(D\).
2. **If \(t = r\):** play \(D\).
3. **If \(t = r-1\):**
   - play \(C\) only if \(S_t \ge 0.85\,\text{capacity}\) and \(q_t \ge 0.75\)
   - otherwise play \(D\)
4. **If \(t \le r-2\):**
   - play \(C\) if all of the following hold:
     - \(S_t \ge 0.70\,\text{capacity}\)
     - \(q_t \ge 0.60\)
     - \(t \le \lfloor 0.8r \rfloor\)
   - otherwise play \(D\)

Edge adjustments:
- **Round 1:** play \(C\) if \(\text{capacity} \ge 3n\); otherwise play \(D\).
- **After any round where observed opponent cooperation drops below \(\frac{1}{2}\):** set \(q_t \leftarrow \min(q_t, 0.5)\) immediately for the next decision.
- **If stock falls below \(0.40\,\text{capacity}\):** play \(D\) for all remaining rounds.
- **If stock is above \(0.90\,\text{capacity}\) for two consecutive rounds and \(q_t \ge 0.70\):** allow \(C\) in the next nonterminal round even if \(t > \lfloor 0.8r \rfloor\).

Individualistic stance:
- Treat cooperation as a selective investment in future stock, not a norm.
- Default to \(D\) whenever preservation is unlikely, when opponents are unreliable, or when the horizon is short.
- Cooperate only when the current stock is high, opponent cooperation is strong, and there is enough future time to recover the benefit.
'''

description_INDIVIDUALISTIC_25 = '''
Round 1: play D.

For every later round t:

1. Let `S` be the current stock.
2. Let `q` be the fraction of opponents who cooperated in round `t-1`.
3. Let `c = q * (n - 1)` be the estimated number of opponent cooperators if they repeat last round’s behavior.
4. Define
   - `nextStock(x) = min(x + 2*x*(1 - x/capacity), capacity)`
   - `S_D = nextStock(S * c / (2n))`
   - `S_C = nextStock(S * (c + 1) / (2n))`
5. Set `reserve = capacity / 2`.

Decision rule:
- If `t = r`, play D.
- Else if `S = 0`, play D.
- Else if `q >= 1/2` and `S_C >= reserve` and (`S_D < reserve` or `S_C > S_D`), play C.
- Otherwise, play D.

Edge cases:
- If `n = 2`, then `q` is just the single opponent’s last-round action, so `q` is either `0` or `1`.
- If the previous round had no opponent cooperation at all, always play D.
- If the previous round showed full opponent cooperation and the current stock is still at or above `reserve`, still play D unless cooperation is needed to keep the predicted next stock at or above `reserve`.
- If the stock is already below `reserve`, use C only when last-round opponent cooperation was at least half and cooperating gives a strictly better predicted next stock than defecting.
'''

description_INDIVIDUALISTIC_26 = '''
Round 1:
- Play C.

For every later round t, let:
- S be the current stock at the start of the round
- k be the number of opponents who cooperated in the previous round
- m = n - 1
- q = k / m, the observed opponent cooperation rate in the previous round
- q̄ be the exponentially smoothed cooperation rate, updated after each round:
  - q̄₁ = 1
  - q̄_t = 0.7·q̄_{t-1} + 0.3·q_{t-1}

Decision rule:
- Play C if all of the following hold:
  - S ≥ 0.6·capacity
  - q ≥ 0.5
  - q̄ ≥ 0.5
- Otherwise play D.

Pressure-release rule:
- If either of the following holds, play D regardless of the above:
  - S < 0.4·capacity
  - q ≤ 0.25

Recovery rule:
- If S has increased since the previous round and q ≥ 0.5, play C even if q̄ < 0.5.

Late-round rule:
- In the final 2 rounds, play C only if:
  - S ≥ 0.7·capacity
  - q = 1
- Otherwise play D.

Fallback tie-break:
- If the decision is still ambiguous, play D.

Update after each round:
- Record k from that round.
- Recompute q and q̄.
- Track whether S rose or fell relative to the previous round.

Behavioral pattern:
- Cooperate only when the pool is healthy and opponents are sustaining it.
- Defect immediately when depletion appears, cooperation drops, or the game is near collapse.
- Keep cooperation conditional, not unconditional.
'''

description_INDIVIDUALISTIC_27 = '''
State variables:
- `S`: current stock
- `k`: number of opponents who cooperated in the previous round
- `t`: current round
- `m = n - 1`: number of opponents

Decision rule:

1. **Final round**
   - If `t = r`, play `D`.

2. **Opening round**
   - If `t = 1`, play `C`.

3. **Middle rounds**
   - Let `q = k / m`, the observed cooperation rate among opponents last round.
   - Define:
     - `high = ceil(2m / 3)`
     - `low_stock = capacity / 3`
   - Play `C` only if all of the following hold:
     - `S >= low_stock`
     - `k >= high`
     - the previous round was not a collapse signal, meaning either:
       - `t = 2`, or
       - `k_prev >= k`
   - Otherwise, play `D`.

Collapse signal:
- Treat the previous round as a collapse signal if `k_prev < high`.

Recovery rule:
- After any round with `k < high`, play `D` until you observe at least two consecutive rounds with `k >= high`.

Edge cases:
- If `n = 2`, then `high = 1`, so cooperate only when the other player cooperated in the previous round and stock is at least `capacity / 3`.
- If `S <= 0`, play `D`.
- If `S` is very small but positive, always play `D`.
- If no previous-round observation is available only because `t = 1`, play `C`.

Implementation form:

```text
if t == r:
    action = D
elif t == 1:
    action = C
else:
    q = k / (n - 1)
    high = ceil(2 * (n - 1) / 3)
    if S >= capacity / 3 and k >= high and (t == 2 or k_prev >= k):
        action = C
    else:
        action = D
```

Behavioral mode:
- Start cooperative.
- Stay cooperative only under sustained high cooperation by others and healthy stock.
- Defect immediately after weak cooperation, declining cooperation, or low stock.
- End aggressively by defecting in the final round.
'''

description_INDIVIDUALISTIC_28 = '''
Initialize `mode = selfish`.

For each round `t` with current stock `S_t`:

1. If `t == 1`, play `C`.
2. If `r - t + 1 == 1`, play `D`.
3. If `S_t == 0`, play `D`.

Otherwise, let `q_prev` be the fraction of opponents who cooperated in the previous round.

Update `mode` using hysteresis:

- If `mode == selfish`:
  - switch to `cooperative` only if `q_prev >= 0.8` and `S_t >= 0.75 * capacity`
  - otherwise stay `selfish`

- If `mode == cooperative`:
  - stay `cooperative` only if `q_prev >= 0.6` and `S_t >= 0.60 * capacity`
  - otherwise switch to `selfish`

Action rule:

- If `mode == cooperative`, play `C`
- If `mode == selfish`, play `D`

Extra edge handling:

- If the previous round had `q_prev == 0` or `S_t < 0.25 * capacity`, force `mode = selfish`
- If the previous round had all opponents cooperate (`q_prev == 1`) and `S_t >= 0.9 * capacity`, play `C` even if `mode` was selfish
- If the remaining number of rounds is small enough that no recovery is possible in practice, default to `D` unless `q_prev == 1` and `S_t` is still near capacity
'''

description_INDIVIDUALISTIC_29 = '''
- Round 1: cooperate.
- Round r: defect.
- On round t in {2, …, r−1}, observe the number of cooperating opponents in round t−1, call it `c`.

Decision rule:
1. If the current stock is 0, defect.
2. If `c = n−1` and current stock is at least `capacity / 2`, cooperate.
3. Else if `c ≥ ceil(2(n−1)/3)` and current stock is at least `3·capacity / 5`, cooperate.
4. Otherwise, defect.

Update discipline:
- After any round with `c < n−1`, stay in defect mode until you later observe two consecutive rounds with `c = n−1`.
- After two consecutive unanimous-cooperation observations, return to the cooperation rule above.

Tie-breaking and edge cases:
- If stock is extremely low, defect unconditionally.
- If the observed cooperation count is unavailable only because it is the first round, cooperate once to probe.
- If multiple rules apply, the more conservative rule wins: defect unless the group is clearly preserving the pool.
'''

description_INDIVIDUALISTIC_30 = '''
- **Round 1:** play **C**.

- **Round r (last round):** play **D**.

- **All intermediate rounds t = 2, …, r-1:**
  - Let **q** be the fraction of opponents who cooperated in round t−1.
  - Use the current stock **S** and the rule below:

  **1. Recovery zone**
  - If **S ≤ capacity/3**:
    - play **C** if **q ≥ 1/2**
    - otherwise play **D**

  **2. Balance zone**
  - If **capacity/3 < S < 2·capacity/3**:
    - play **C** if **q ≥ 2/3**
    - otherwise play **D**

  **3. Harvest zone**
  - If **S ≥ 2·capacity/3**:
    - play **D**

- **Hysteresis override for stability:**
  - If the previous round had **q = 1** and the current stock is still at least **capacity/2**, keep playing **C** once more even in the balance zone.
  - If the previous two rounds both had **q ≤ 1/3**, play **D** until **q ≥ 1/2** again.

- **Individualistic interpretation:**
  - Cooperate only when the pool is sufficiently depleted and the opponents are cooperating enough to justify preserving stock.
  - Defect whenever the pool is abundant, cooperation is weak, or it is the final round.
'''

description_INDIVIDUALISTIC_31 = '''
Round 1: cooperate.

For round t > 1, let:
- `S` = current stock
- `m` = number of opponents who cooperated in round `t-1`
- `k_prev` = total cooperators in round `t-1`  
  (`k_prev = m + 1` if you cooperated last round, else `k_prev = m`)
- `h` = rounds remaining including this one

Decision rule:

1. If `h = 1`: defect.
2. If `h = 2`:
   - cooperate only if `m = n - 1` and `k_prev = n` and `S <= 0.4 * capacity`;
   - otherwise defect.
3. If `h > 2`:
   - if `S >= 0.6 * capacity`:
     - cooperate iff `m >= ceil((n - 1)/2)` and `k_prev >= ceil(n/2)`;
     - otherwise defect.
   - if `0.2 * capacity <= S < 0.6 * capacity`:
     - cooperate iff `m >= ceil((n - 1)/2) + 1`;
     - otherwise defect.
   - if `S < 0.2 * capacity`:
     - cooperate iff `m = n - 1`;
     - otherwise defect.

Update memory after each round:
- record whether you cooperated last round
- record `m` from the aggregate observation
- record `S` for the next decision

Fallback behavior:
- If the stock has fallen for two consecutive rounds, switch to defect unless the previous round was unanimous cooperation.
- If the stock is at or near zero, defect.
- If the stock is at or near capacity, use the cooperation thresholds above; never cooperate without strong evidence that others are also cooperating.

Individualistic bias:
- default to defect whenever the observed cooperation rate is not clearly high enough to justify preserving the pool
- cooperate only as a conditional response to strong, recent cooperation from others
- never rely on goodwill, reciprocity, or long-run mutual restraint beyond what is directly visible in the history
'''

description_INDIVIDUALISTIC_32 = '''
Round 1: cooperate.

For round t > 1, let:
- `k` = number of opponents who cooperated in round `t-1`
- `q = k / (n - 1)` = observed cooperation rate among opponents
- `p = stock / capacity` = current stock ratio

Maintain:
- `good_streak` = consecutive past rounds with `q >= 1/2`
- `bad_streak` = consecutive past rounds with `q < 1/2`

Update after each round:
- if `q >= 1/2`, increment `good_streak` and reset `bad_streak`
- otherwise, increment `bad_streak` and reset `good_streak`

Decision rule:

1. If `t = 1`: `C`

2. If `t >= r - 1`: `D`

3. Otherwise:
   - play `C` iff all of the following hold:
     - `q >= 1/2`
     - `p >= 2/5`
     - `bad_streak = 0`
   - otherwise play `D`

Refinement for strong cooperation:
- if `q >= 2/3` and `p >= 3/5`, play `C` even after one isolated bad round, provided `bad_streak <= 1`

Edge cases:
- If `n = 2`, then `q` is either `0` or `1`; cooperate only after observing the other player cooperate in the previous round and the stock ratio is at least `2/5`.
- If the observed cooperation rate drops below `1/2` for two consecutive rounds, defect until it recovers to at least `1/2`.
- If stock falls below `2/5` of capacity at any point, defect until stock returns to at least `2/5` and opponents have resumed majority cooperation.

Behavioral posture:
- start conservatively cooperative,
- cooperate only under clear evidence that others are sustaining the pool,
- otherwise switch immediately to extraction,
- stop cooperating in the final rounds and take the remaining value.
'''
