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
