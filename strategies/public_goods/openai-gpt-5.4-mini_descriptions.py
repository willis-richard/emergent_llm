"""
Strategy descriptions for public_goods.

Generated with:
- Provider: OpenAI
- Model: openai/gpt-5.4-mini
"""


description_COLLECTIVE_1 = '''
State variables:

- `h_t`: number of opponents who cooperated in round `t`
- `m_t`: moving average of `h` over the last `L = min(3, t-1)` observed rounds
- `s_t`: cooperation streak = number of consecutive recent rounds in which `h` met the cooperation threshold

Define:

- `A = n - 1` opponents
- `high = ceil(0.7 * A)`
- `low = floor(0.4 * A)`

Decision rule for round `t`:

1. **Round 1**
   - Play `C`

2. **Final round `r`**
   - Play `D`

3. **Rounds 2 through `r-1`**
   - Let `benchmark = max(high, ceil(m_t))`
   - If the last observed round had `h_{t-1} >= benchmark`, and at least 2 of the last 3 observed rounds also met that benchmark, play `C`
   - Otherwise play `D`

Update rule after observing round `t`:

- If `h_t >= benchmark`, increase `s_t` by 1
- Else reset `s_t = 0`

Recovery rule:

- After any round with `h_t <= low`, defect until there are two consecutive rounds with `h >= high`
- After any round with `low < h_t < high`, require three consecutive rounds with `h >= benchmark` before returning to `C`

Collective discipline:

- When cooperating, do so only in sustained-high-cooperation phases
- When defecting, remain consistent until the observed cooperation level has clearly recovered
- Never switch to `C` on a single isolated good round
- Never stay on `C` after a visible break in cooperation

Pseudocode:

```text
if t == 1:
    action = C
elif t == r:
    action = D
else:
    L = min(3, t-1)
    m = average(h_{t-L}, ..., h_{t-1})
    benchmark = max(ceil(0.7*(n-1)), ceil(m))

    if h_{t-1} >= benchmark and count_of_last_3_rounds_with_h_ge_benchmark >= 2:
        action = C
    else:
        action = D

    if h_{t-1} <= floor(0.4*(n-1)):
        require 2 consecutive rounds with h >= ceil(0.7*(n-1)) before any future C
    elif h_{t-1} < benchmark:
        require 3 consecutive rounds with h >= benchmark before any future C
```
'''

description_COLLECTIVE_2 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(a_t \in \{0,1\}\) be our own action in round \(t\) with \(1=C\), \(0=D\). Let total cooperation be \(T_t = m_t + a_t\).

Use a three-state collective policy:

**State 1: Build**
- Round 1: play \(C\).
- Continue playing \(C\) while the observed cooperation level stays strong:
  - if \(T_{t-1} \ge \lceil 0.7n \rceil\), play \(C\).

**State 2: Protect**
- If cooperation weakens, switch to a firm but temporary defection response:
  - if \(T_{t-1} < \lceil 0.7n \rceil\) for the first time, play \(D\) for the next 2 rounds.
- While in Protect:
  - keep playing \(D\) until either
    - \(T_{t-1} \ge \lceil 0.8n \rceil\) for 2 consecutive rounds, then return to Build, or
    - the game reaches the final 2 rounds, then move to Endgame.

**State 3: Endgame**
- In the last 2 rounds, play \(D\) unless the previous 2 rounds both had \(T \ge \lceil 0.8n \rceil\); in that case, play \(C\).
- In the final round, if the previous round had \(T < \lceil 0.8n \rceil\), play \(D\).

**Adaptive update rule**
- After any round with \(T_t \ge \lceil 0.8n \rceil\), reset the Protect counter to 0.
- After any round with \(T_t < \lceil 0.7n \rceil\), set Protect mode for the next 2 rounds.
- After any round with \( \lceil 0.7n \rceil \le T_t < \lceil 0.8n \rceil\), keep the current state unchanged.

**Edge cases**
- If \(n=2\), replace the thresholds with:
  - Build: continue \(C\) only if the other player cooperated in the previous round.
  - Protect: defect for 1 round after any observed defection.
- If \(r=2\), play \(C\) in round 1 and use the Endgame rule in round 2.
- If no history exists for a rule check, default to \(C\) on the first move.

**Collective posture**
- Treat sustained cooperation as a shared target.
- Match cooperation with cooperation.
- Respond to breakdowns with short, synchronized defection.
- Return to cooperation only after clear, repeated evidence that the group has restored high cooperation.
'''

description_COLLECTIVE_3 = '''
Let \(T=\lceil n/k\rceil\).

- **Round 1:** play **C**.
- **Rounds 2 through \(r-2\):**
  - Reconstruct the previous round’s total cooperation as  
    \[
    M_{t-1} = (\text{# opponents who cooperated last round}) + \mathbf{1}\{\text{I cooperated last round}\}.
    \]
  - Play **C** if \(M_{t-1} \ge T\).
  - Play **D** if \(M_{t-1} < T\).

- **Rounds \(r-1\) and \(r\):** play **D** unconditionally.

- **If \(r=2\):** play **C** in round 1 and **D** in round 2.
- **If \(r=3\):** play **C** in round 1, apply the threshold rule in round 2, and play **D** in round 3.

- **Recovery rule after defection:**
  - The first round after a low-cooperation round, return to **C** immediately once the previous round again meets \(T\).
  - Never stay in punishment for more than one round at a time.
'''

description_COLLECTIVE_4 = '''
State variables:

- `M = ceil((n - 1) / 2)`  
- `m_t =` number of opponents who cooperated in round `t`
- `L_t =` number of consecutive recent rounds ending at `t` with `m >= M`

Decision rule:

1. **Round 1:** play `C`.

2. **For round t > 1:**
   - If `m_{t-1} >= M`, play `C`.
   - If `m_{t-1} < M` and `m_{t-2} < M` (when `t >= 3`), play `D`.
   - If exactly one of the last two rounds met the threshold, play `C`.

3. **Repair rule after defection:**
   - Once you have played `D`, return to `C` immediately after any round in which `m_{t-1} >= M`.

4. **Last round:**
   - Use the same rule as any other round; do not change behavior just because the game is ending.

Operational form:

- Maintain a **supportive mode** and a **guarded mode**.
- Start in supportive mode.
- Stay in supportive mode as long as cooperation is not weak in two rounds in a row.
- Switch to guarded mode only after two consecutive weak rounds.
- In supportive mode, play `C`.
- In guarded mode, play `D`.
- Exit guarded mode after any sufficiently cooperative round.

If a longer memory is preferred, replace the two-round check with a three-round average:

- Compute `avg_t = (m_{t-1} + m_{t-2} + m_{t-3}) / 3` when available.
- Play `C` if `avg_t >= M`.
- Play `D` otherwise.
- Always play `C` in round 1.
'''

description_COLLECTIVE_5 = '''
Use a state-based conditional cooperation rule with three modes: build, sustain, and exit.

Let `m_t` be the number of opponents who cooperated in round `t`, and let `M_t = m_t + 1` if you cooperated in round `t`, else `M_t = m_t`. Track the recent cooperation rate among opponents:
`avg_t = (m_t + ... + m_{t-L+1}) / L`, where `L = min(3, t-1)` and for `t < 2`, treat `avg_t = 0`.

Define the target threshold:
`T = ceil(n / k)`.
Let `T_opponents = T - 1`, the minimum number of cooperating opponents needed for your own cooperation to be individually matched by the public return.

Decision rules:

1. Round 1:
- Play `C`.

2. Rounds 2 through r-1:
- If the last round had at least `T_opponents` cooperating opponents, and the recent average cooperation `avg_t` is at least `T_opponents`, play `C`.
- If the last round had fewer than `T_opponents` cooperating opponents, play `D` for one round.
- After one defect, if cooperation recovers to at least `T_opponents` cooperating opponents in that round, return to `C` immediately in the next round.
- If cooperation remains below `T_opponents` for two consecutive rounds, stay in `D` until the recent average cooperation returns to at least `T_opponents`.

3. Last round:
- Play `C` if the recent average cooperation `avg_r` is at least `T_opponents`.
- Otherwise play `D`.

State handling:
- Start in `BUILD` mode.
- In `BUILD`, play `C` whenever the last round met the cooperation threshold; otherwise switch to `PROBE`.
- In `PROBE`, play `D` for exactly one round after a threshold failure.
- If cooperation recovers in `PROBE`, switch back to `BUILD`.
- If two consecutive threshold failures occur, switch to `EXIT`.
- In `EXIT`, play `D` until the rolling average returns to threshold, then switch back to `BUILD`.

Tie and edge cases:
- If `k` is very close to `n`, the threshold may be `1`; then cooperate whenever at least one opponent cooperated in the prior round.
- If `k` is close to `1`, the threshold may equal `n`; then cooperate only when essentially full cooperation is observed.
- If `r = 2`, use the same rule with `L = 1` and treat round 2 as the last round rule.
- If the observed cooperation count is exactly at the threshold, treat it as successful cooperation and continue cooperating.

Compact pseudocode:

```text
initialize mode = BUILD

round 1: play C

for t = 2 to r:
    L = min(3, t-1)
    avg = average of opponent cooperation counts over last L-1 rounds if available
    success = (m_{t-1} >= T_opponents)

    if t == r:
        play C if avg >= T_opponents else D
    else if mode == BUILD:
        if success:
            play C
        else:
            play D
            mode = PROBE
    else if mode == PROBE:
        if m_{t-1} >= T_opponents:
            play C
            mode = BUILD
        else:
            play D
            mode = EXIT
    else if mode == EXIT:
        if avg >= T_opponents:
            play C
            mode = BUILD
        else:
            play D
```

Collective orientation:
- Default to cooperation.
- Continue cooperating only while the group remains above the cooperation threshold.
- Use a single-round defensive defect after breakdown.
- Rejoin immediately once the group restores the threshold.
'''

description_COLLECTIVE_6 = '''
Maintain a target cooperation threshold based on the observed cooperation rate among opponents.

Let:
- \(m_t\) = number of opponents who cooperated in round \(t\)
- \(q_t = \frac{m_t}{n-1}\) = observed opponent cooperation rate in round \(t\)
- \(\bar q_t\) = average of \(q\) over the last \(L\) rounds, with \(L = \min(3, t-1)\)
- \(B_t\) = recent trend indicator, defined as \(B_t = q_{t-1} - q_{t-2}\) when both exist, otherwise \(0\)

Decision rule by round:

**Round 1**
- Play \(C\).

**Round 2**
- Play \(C\) if \(q_1 \ge \frac{1}{2}\); otherwise play \(D\).

**Rounds 3 through \(r-1\)**
- Play \(C\) if all of the following hold:
  1. \(\bar q_t \ge \frac{k-1}{k}\)
  2. \(q_{t-1} \ge \frac{k-1}{k}\)
  3. \(B_t \ge -\frac{1}{4}\)
- Otherwise play \(D\).

**Last round \(r\)**
- If \(\bar q_r \ge \frac{k-1}{k}\), play \(C\).
- Otherwise play \(D\).

State update after each round:
- Record only the count of opponent cooperations.
- Recompute \(\bar q_t\) and \(B_t\) from the last observed rounds.
- No player-specific memory is used.

Tie and edge handling:
- If \(n=2\), then \(q_t\in\{0,1\}\); interpret the threshold exactly the same way.
- If fewer than \(L\) past rounds exist, average only over the rounds observed so far.
- If two consecutive rounds are missing for trend calculation, set \(B_t=0\).
- If observed cooperation is exactly at threshold, choose \(C\).

Collective coordination rule:
- Stay cooperative as long as the group’s recent cooperation rate meets the threshold \(\frac{k-1}{k}\).
- Immediately switch to \(D\) after a clear drop below that level.
- Re-enter cooperation only after the observed rate recovers to the threshold again.

Optional probe adjustment:
- If the group has defected in the last two rounds but the current round is not the last, play \(C\) once every 4 rounds to test whether cooperation can be restored; otherwise follow the rule above.
'''

description_COLLECTIVE_7 = '''
Cooperate in round 1.

For each later round, let \(x_{t-1}\) be the number of opponents who cooperated in the previous round, and let \(m_{t-1}=x_{t-1}/(n-1)\) be the observed cooperation rate among opponents.

Choose a target cooperation level:
\[
q = \max\!\left(0,\; \frac{n-k}{n-1}\right)
\]
and use a one-step memory rule:

- If \(m_{t-1} > q\), play \(C\).
- If \(m_{t-1} < q\), play \(D\).
- If \(m_{t-1} = q\), repeat your own previous action.

Behavioral adjustment:
- If the last round had full or near-full cooperation, stay with \(C\).
- If cooperation falls below target, switch to \(D\) immediately.
- If the group is exactly at the target, preserve the current state rather than destabilizing it.

Last round:
- Play \(C\) if \(m_{r-1} \ge q\).
- Play \(D\) if \(m_{r-1} < q\).

Special cases:
- If \(n=2\), use the same rule with \(q=\max(0,2-k)\).
- If the previous round was unobserved for any reason, default to \(C\).
- If the observed cooperation rate oscillates around the threshold, use the tie rule above to avoid unnecessary switching.

Collective convention:
- Start cooperative.
- Continue cooperating while the group is meeting the shared threshold.
- Defect only after the group clearly falls below the threshold.
- Restore cooperation immediately once the threshold is met again.
'''

description_COLLECTIVE_8 = '''
Let

- `m_t` = number of opponents who cooperated in round `t`
- `ρ_t = m_t / (n - 1)` = observed opponent cooperation rate
- `τ = 1 - 1/k`
- `mode ∈ {cooperative, defensive}`

Initialize:
- `mode = cooperative`
- Round `1`: play `C`

For rounds `t = 2, ..., r`:

1. If `t = r`:
   - play `D`

2. Otherwise, update based on the previous round:
   - If `mode = cooperative`:
     - play `C` if `ρ_{t-1} ≥ τ`
     - play `D` if `ρ_{t-1} < τ`, and set `mode = defensive`
   - If `mode = defensive`:
     - play `D`
     - if `ρ_{t-1} ≥ τ` for two consecutive rounds, set `mode = cooperative`

Operationally:

- Stay fully cooperative as long as the group’s observed cooperation remains at or above the threshold `τ`.
- If cooperation drops below `τ`, switch to defensive play.
- In defensive mode, require two straight rounds of acceptable cooperation before returning to cooperation.
- On the final round, defect.

Edge cases:

- If `n = 2`, then `ρ_t` is either `0` or `1`; the same rule applies with `τ = 1 - 1/k`.
- If `τ ≤ 0`, treat any observed cooperation as sufficient to remain cooperative.
- If `τ > 1`, require `ρ_t = 1` to remain cooperative.

The collective posture is: start by contributing, continue contributing while the group is visibly sustaining cooperation, withdraw support after a clear breakdown, and only restore cooperation after the group has re-established reliable participation.
'''

description_PROSOCIAL_1 = '''
Let \(m = n-1\) be the number of opponents.

Maintain a history variable:

- `low_streak` = number of consecutive past rounds in which the observed number of cooperating opponents was at most \(\lfloor m/3 \rfloor\)

Decision rule for round \(t\):

1. **Round 1:** play `C`.
2. **Final round (\(t=r\)):** play `C`.
3. **Otherwise:**
   - if `low_streak >= 2`, play `D`
   - else play `C`

After each round is observed, update `low_streak` using the number \(x_t\) of cooperating opponents in that round:

- if \(x_t \le \lfloor m/3 \rfloor\), set `low_streak = low_streak + 1`
- otherwise, set `low_streak = 0`

Equivalent pseudocode:

```text
initialize low_streak = 0

for t = 1 to r:
    if t == 1:
        action = C
    else if t == r:
        action = C
    else if low_streak >= 2:
        action = D
    else:
        action = C

    play action

    observe x_t = number of opponents who played C

    if x_t <= floor((n-1)/3):
        low_streak += 1
    else:
        low_streak = 0
```

Decision logic:

- Cooperate by default.
- Require two consecutive clearly uncooperative rounds before switching to defection.
- Resume cooperation immediately after any round that is not clearly uncooperative.
- Always cooperate in the first and last round.
'''

description_PROSOCIAL_2 = '''
**Adaptive Prosocial Threshold Strategy**

Track, after each round \(t\), the number of other players who cooperated:
- \(x_t \in \{0,1,\dots,n-1\}\)

Maintain:
- \(m_t\): the moving average of observed opponent cooperation over the last \(L\) rounds, where \(L = \min(5, t-1)\)
- \(s_t\): a punishment counter, initially 0

Use the following rules:

### Round 1
Play **C**.

### Rounds 2 through \(r\)

#### 1) If \(s_t > 0\)
Play **D**, then decrement:
- \(s_{t+1} = s_t - 1\)

#### 2) Otherwise, compute recent cooperation level
Let
\[
m_t = \frac{1}{L}\sum_{u=t-L}^{t-1} x_u
\]
with \(L = \min(5, t-1)\).

Define the cooperation threshold:
\[
T = \left\lceil \frac{n-1}{2} \right\rceil
\]

#### 3) Decision rule
- If \(m_t \ge T\), play **C**
- If \(m_t < T\), play **D** and set:
  \[
  s_{t+1} = 1
  \]
  meaning cooperate again only after one immediate defection response has been completed

### Forgiveness rule
If in any round the observed cooperation count \(x_t\) reaches at least:
\[
T + 1
\]
then clear any pending punishment immediately:
- \(s_{t+1} = 0\)

### Endgame rule
In the final two rounds:
- If \(m_t \ge T\), play **C**
- Otherwise play **D**

### Interpretation of behavior
- Begin cooperatively
- Continue cooperating when the group’s recent behavior is at least majority-cooperative
- Respond to sustained low cooperation with a single-round defection signal
- Return to cooperation immediately once the group shows renewed willingness to cooperate
- Never defect for more than one round in a row unless recent cooperation remains below threshold

'''

description_PROSOCIAL_3 = '''
Start with cooperation.

For each round t:

1. Compute the cooperation rate in the previous round:
   - Let m be the number of opponents who cooperated in round t-1.
   - Let q = m / (n - 1).

2. Cooperate if the group is sustaining cooperation:
   - Cooperate when q ≥ 1/2.
   - Also cooperate when q is exactly 0 in the first observation after a full-defection round if the last two rounds were not both full-defection rounds.

3. Defect only to signal refusal to reward persistent collective defection:
   - Defect when the previous round had zero cooperators among opponents, and the round before that also had zero cooperators among opponents.
   - Defect on every subsequent round until at least one opponent cooperates.

4. Recovery rule:
   - The moment you observe any opponent cooperation in a round, return to cooperation in the next round.
   - After recovery, keep cooperating as long as at least half of opponents cooperated in the previous round.

Edge cases:

- Round 1: cooperate.
- Round 2: cooperate unless round 1 had zero opponent cooperation, in which case still cooperate once before switching to defensive defection.
- If the game reaches the final round:
  - Cooperate unless the last two observed rounds were both zero-cooperation rounds; in that case defect.
- If n = 2:
  - Cooperate in round 1.
  - Thereafter, cooperate whenever the opponent cooperated in the previous round; defect only after two consecutive rounds of opponent defection.

Pseudocode:

```text
if t == 1:
    play C
else:
    q = opponents_cooperated_last_round / (n - 1)

    if opponents_cooperated_last_round > 0:
        play C
    else if t >= 3 and opponents_cooperated_two_rounds_ago == 0:
        play D
    else:
        play C
```

Refinement with a prosocial threshold:

```text
if q >= 1/2:
    play C
else if q == 0 and previous_round_q == 0:
    play D
else:
    play C
```

This keeps cooperation as the default, rewards any sign of cooperation immediately, and uses defection only after persistent full free-riding.
'''

description_PROSOCIAL_4 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\).

Define the cooperation threshold
\[
\tau = \left\lceil \frac{n-1}{2} \right\rceil .
\]

Decision rule:

- Round 1: play \(C\).
- Rounds \(2\) through \(r-1\):
  - play \(C\) if \(x_{t-1} \ge \tau\)
  - otherwise, play \(D\) only if both of the last two observed rounds were below threshold:
    \[
    x_{t-1} < \tau \;\text{and}\; x_{t-2} < \tau
    \]
  - if only one of the last two rounds was below threshold, play \(C\).
- Round \(r\): play \(C\).

Equivalent pseudocode:

```text
if t == 1:
    C
else if t == r:
    C
else if x[t-1] >= ceil((n-1)/2):
    C
else if t >= 3 and x[t-2] < ceil((n-1)/2):
    D
else:
    C
```

Behavioral intent:

- Start cooperatively.
- Keep cooperating whenever the group is meeting a basic cooperation standard.
- Forgive a single weak round.
- Defect only after sustained low cooperation.
- Never defect in the final round.
'''

description_PROSOCIAL_5 = '''
Round 1: cooperate.

For every later round, look only at the number of opponents who cooperated in the immediately previous round, call it `x`.

Set the cooperation threshold to `T = ceil((n - 1) / 2)`.

Decision rule:
- If `x >= T`, cooperate.
- If `x < T`, defect for that round.
- If cooperation was just below the threshold but improving, be forgiving: if `x = T - 1` and the previous round’s opponent cooperation count was lower than `x`, cooperate instead of defecting.

State memory:
- Keep the last two observed opponent-cooperation counts.
- Use the forgiveness rule whenever the group is moving back toward cooperation.
- If there have been two consecutive rounds with `x < T` and no improvement, defect until a round reaches `x >= T` again.

Edge cases:
- If `n = 2`, the threshold is `T = 1`, so cooperate whenever the other player cooperated in the last round.
- In the final round, ignore future consequences and apply the same rule as usual.
- If no history is available beyond the first round, cooperate.

Pseudocode:

```text
if t == 1:
    play C
else:
    x = number of opponents who cooperated in round t-1
    x_prev = number of opponents who cooperated in round t-2, if available

    if x >= ceil((n-1)/2):
        play C
    else if x == ceil((n-1)/2) - 1 and x_prev is available and x > x_prev:
        play C
    else:
        play D
```

This keeps a cooperative baseline, rewards broad participation, and gives quick forgiveness when the group is recovering.
'''

description_PROSOCIAL_6 = '''
Play C in round 1.

Maintain a cooperation target \(T_t\) for round \(t\), defined from observed opponent cooperation in the previous round:

- Let \(m_{t-1}\) be the number of opponents who cooperated in round \(t-1\).
- Let \(n\) be total players, so the number of opponents is \(n-1\).
- Set the target cooperation rate among opponents to
  \[
  \rho_{t} =
  \begin{cases}
  1, & t=1 \\
  \dfrac{m_{t-1}}{n-1}, & t>1
  \end{cases}
  \]
- Cooperate in round \(t\) if and only if
  \[
  \rho_t \ge \frac{1}{2}
  \]
  and defect otherwise.

Use a forgiving update rule to avoid locking into mutual defection:

- If round \(t-1\) had at least \(\lceil (n-1)/2 \rceil\) cooperating opponents, then in round \(t\) play C.
- If round \(t-1\) had fewer than \(\lceil (n-1)/2 \rceil\) cooperating opponents, play D in round \(t\).
- If a round with at least \(\lceil (n-1)/2 \rceil\) opponent cooperators is followed by a round with fewer than \(\lceil (n-1)/2 \rceil\), return to C immediately in the next round after any single cooperative majority reappears.

Handle the first and last rounds as follows:

- Round 1: play C.
- Round \(r\): play C if the previous round met the cooperation threshold; otherwise play D.
- Never use extra punishment beyond one round: one low-cooperation observation is enough to switch to D, but one high-cooperation observation is enough to switch back to C.

If \(n=2\), this reduces to:
- C in round 1
- Thereafter, play C after observing the other player cooperate in the previous round, and play D after observing defection.

Optional memory refinement:
- If the previous round had exactly half of opponents cooperating when \(n-1\) is even, treat it as cooperation and play C.
- If the previous round had exactly half when \(n-1\) is odd, this case cannot occur.

When the game is near the end and there is no time for recovery:
- In the final round, mirror the previous round’s aggregate behavior:
  - play C if at least half of opponents cooperated previously,
  - otherwise play D.

This strategy is:
- initially cooperative,
- responsive to observed cooperation,
- forgiving after a single cooperative majority,
- and structured to keep cooperation stable whenever the group is willing to sustain it.
'''

description_PROSOCIAL_7 = '''
Round 1: play C.

For each round t = 2,...,r:

- Let m be the number of opponents who cooperated in round t-1.
- Let q = m / (n-1), the observed cooperation rate among opponents.

Decision rule:
- If q >= 1/2, play C.
- If q < 1/2:
  - If the previous round was also below 1/2, play D.
  - Otherwise, play C once as a forgiveness/recovery move.

State tracking:
- Keep one bit of memory: whether the immediately preceding round was below the 1/2 cooperation threshold.
- Update that bit after each round using the newly observed m.

Last round:
- Use the same rule as above.
- If the final observed round was below 1/2 and the prior round was also below 1/2, play D; otherwise play C.

Edge cases:
- n = 2: q is 0 or 1, so cooperate whenever the other player cooperated in the previous round; after two consecutive defections by the other player, defect until cooperation reappears.
- If m = n-1, always play C.
- If m = 0, play D on the next round unless this is the first below-threshold round after a cooperative round, in which case play C once before switching to D if needed.

State machine form:

- Initialize: low_streak = 0
- Round 1: C
- For round t >= 2:
  - Observe m
  - If m >= ceil((n-1)/2):
      play C
      low_streak = 0
    else:
      if low_streak == 0:
          play C
          low_streak = 1
      else:
          play D
          low_streak = 1
'''

description_PROSOCIAL_8 = '''
**Adaptive Cooperative Threshold with Forgiveness**

Let:

- `m = n - 1` = number of opponents
- `x_t` = number of opponents who cooperated in round `t`
- `h_t = x_t / m` = observed opponent cooperation rate in round `t`
- `H_t` = average of `h_1, ..., h_t` over rounds observed so far
- `s_t` = your own cooperation streak up to round `t-1` if relevant for recovery logic

Use these decision rules:

### Round 1
Play `C`.

### General rule for round t > 1
Play `C` if at least one of the following holds:

1. **Current round looked broadly cooperative**
   - `h_{t-1} >= 1/2`

2. **Recent behavior is mostly cooperative**
   - `H_{t-1} >= 1/2`

3. **You are in recovery mode after a mostly cooperative phase**
   - In the last two rounds, at least one had `h >= 1/2`, and the most recent round was only slightly below that threshold:
   - `h_{t-1} >= 1/3`

Otherwise play `D`.

### Last round
Play `C` if `h_{r-1} >= 1/3`; otherwise play `D`.

### Recovery after a cooperative base
If you defect because cooperation dropped below threshold, do not stay in permanent defection. Instead:

- Keep testing cooperation every round.
- Return to `C` immediately after any round with `h_{t-1} >= 1/2`.

### Strong exploitation response
If you observe two consecutive rounds with no opponent cooperation:

- Defect until at least one round reaches `h >= 1/3`
- Then switch back to `C` on the next round

### Optional escalation rule for longer games
If `r >= 5`, use a more forgiving moving window:

- Let `W_t` be the average cooperation rate over the last `min(3, t-1)` rounds.
- Play `C` if `W_t >= 1/2`; otherwise play `D`.

### Complete compact pseudocode
```text
if t == 1:
    play C
else:
    if h_{t-1} >= 1/2:
        play C
    else if H_{t-1} >= 1/2:
        play C
    else if h_{t-1} >= 1/3 and exists s in {t-2, t-3} with h_s >= 1/2:
        play C
    else if t == r and h_{t-1} >= 1/3:
        play C
    else:
        play D
```

### Behavioral principle
Start cooperative, stay cooperative when cooperation is visible, tolerate small dips, and only withdraw cooperation after sustained low reciprocity.
'''

description_ALTRUISTIC_1 = '''
Round 1: play C.

For round t > 1, let s_t be the number of opponents who cooperated in round t, and let q_t = s_t / (n - 1) be the observed opponent cooperation rate.

Maintain two memories:
- m_t: the number of consecutive recent rounds in which q_t was high
- p_t: the number of consecutive recent rounds in which q_t was low

Use these rules:

1. Default to cooperation.
   Play C unless the recent history shows persistent non-cooperation.

2. High-cooperation test.
   Define a “good round” as any round with q_t ≥ 1/2.
   If the last 2 rounds were both good, set m_t = 2; otherwise update it by streak.

3. Low-cooperation test.
   Define a “bad round” as any round with q_t ≤ 1/4.
   If the last 2 rounds were both bad, set p_t = 2; otherwise update it by streak.

4. Action rule for round t + 1.
   - Play C if either:
     - the last 2 rounds were not both bad, or
     - the last 2 rounds were good, or
     - t is the final round.
   - Play D only if:
     - the last 2 rounds were both bad, and
     - the last 3 rounds were not good enough to recover, meaning no run of 2 consecutive good rounds has appeared since the bad streak began.

5. Recovery rule.
   Immediately return to C after any round in which q_t ≥ 1/2.

6. Final-round rule.
   Always play C in the last round.

Equivalent compact version:

Initialize:
- cooperate on round 1.

For round t = 2, 3, ..., r:
- if t = r: play C
- else if the last two observed rounds each had q ≤ 1/4: play D
- else: play C

Tightened altruistic variant:
- If the observed cooperation rate in the previous round is at least 1/2, cooperate.
- If it is below 1/2, still cooperate unless there have been two consecutive low-cooperation rounds below 1/4.
- Never defect on the first round or the last round.
- After any single round of strong cooperation by others, reset immediately to C.

This makes cooperation the default, defects only after sustained low reciprocity, and restores cooperation as soon as the group shows any meaningful willingness to cooperate.
'''

description_ALTRUISTIC_2 = '''
Play C in round 1.

For each later round t, let H be the number of opponents who cooperated in round t-1, and let q = H / (n - 1).

Decision rule:
- If q = 0, play D for the next 2 rounds.
- If q > 0 and q < 1/3, play C for one round, then reassess.
- If 1/3 ≤ q < 2/3, play C.
- If q ≥ 2/3, play C and keep cooperating unless cooperation collapses.

State rule for persistence:
- Maintain a flag s ∈ {normal, cautious}.
- Start in normal.
- If you observe q = 0 in any round, switch to cautious for the next 2 rounds.
- While cautious:
  - If q = 0 again, remain cautious for 2 more rounds.
  - If q > 0, return to normal immediately after the next round.

Endgame rule:
- In the final round, play C unless the previous round had q = 0 and you are in cautious mode; in that case play D.
- In the penultimate round, if you are not already in cautious mode, do not change behavior based only on the approaching end.

Tie and edge handling:
- If n = 2, then q is either 0 or 1; use the same rules with thresholds interpreted directly.
- If no history is available for some reason, play C.
- If the observed cooperation count is inconsistent or unavailable, default to C.

Compact pseudocode:

```
state = normal
cooldown = 0

for round t in 1..r:
    if t == 1:
        action = C
    else:
        q = coop_opponents_prev_round / (n - 1)

        if t == r:
            if state == cautious and q == 0:
                action = D
            else:
                action = C
        else if cooldown > 0:
            action = C
            cooldown -= 1
        else if q == 0:
            action = D
            cooldown = 1
            state = cautious
        else if q < 1/3:
            action = C
        else:
            action = C
            state = normal

    observe previous round and update as above
```

Behavioral principle:
- Lead with cooperation.
- Continue cooperating whenever anyone else cooperates.
- Temporarily withdraw only after complete opponent defection, then give a short test period for recovery.
- Return to cooperation immediately when cooperation reappears.
'''

description_ALTRUISTIC_3 = '''
Start by cooperating.

Let:
- \(n\) be total players
- \(o_t\) be the number of opponents who cooperated in round \(t\)
- \(m_t = o_t + 1\) if you cooperated in round \(t\), or \(m_t = o_t\) if you defected in round \(t\), be the total number of cooperators in round \(t\)
- \(p_t = o_t/(n-1)\), the observed cooperation rate among opponents in round \(t\)

Decision rule for round \(t\):

1. Round 1:
   - Play \(C\).

2. Rounds 2 through \(r-1\):
   - Keep a cooperation score over the last two rounds:
     \[
     S_t = p_{t-1} + p_{t-2}
     \]
     with missing terms treated as \(1\) before they exist.
   - Play \(C\) if any of the following hold:
     - \(p_{t-1} \ge \frac{1}{2}\)
     - \(S_t \ge 1\)
     - you cooperated in round \(t-1\) and at least one opponent cooperated in round \(t-1\)
   - Otherwise play \(D\).

3. Last round \(t=r\):
   - Play \(C\) if either:
     - at least one opponent cooperated in round \(r-1\), or
     - at least half of the opponents cooperated in round \(r-1\)
   - Otherwise play \(D\).

Adaptive update rule:

- If opponents’ cooperation rises, return immediately to \(C\).
- If opponents’ cooperation falls below half for one round, give one grace round and continue cooperating once.
- If opponents’ cooperation is below half for two consecutive rounds, switch to \(D\) for one round.
- After any defecting round, resume \(C\) as soon as \(p_t \ge \frac{1}{2}\).

Compact pseudocode:

```text
if t == 1:
    play C
else if t == r:
    if p_{t-1} >= 1/2 or o_{t-1} > 0:
        play C
    else:
        play D
else:
    if p_{t-1} >= 1/2:
        play C
    else if p_{t-1} + p_{t-2} >= 1:
        play C
    else if you played C in t-1 and o_{t-1} > 0:
        play C
    else:
        play D
```

Persistence adjustment:
- After any round where you defect, do not keep defecting automatically.
- Re-enter cooperation as soon as the most recent observed cooperation rate reaches at least \(1/2\), or whenever the two-round average reaches at least \(1/2\).

Altruistic stance:
- Default to cooperation.
- Use defection only as a brief signal when cooperation has been low for multiple consecutive rounds.
- Prefer forgiving and rapid return to cooperation over punishment.
'''

description_ALTRUISTIC_4 = '''
Use a three-mode policy: start by cooperating, keep cooperating while the group shows enough cooperation, and only defect as a limited protective response when cooperation collapses.

**State tracked from history**
- For each past round t, record `m_t =` number of opponents who cooperated.
- Let `M_t = m_t / (n - 1)` be the observed opponent cooperation rate in round t.
- Let `A_t =` average of `M_1 ... M_t` over the rounds observed so far.
- Let `L_t =` the most recent observed cooperation rate `M_t`.

**Decision rule for round 1**
- Play `C`.

**Decision rule for round t > 1**
Play `C` if any of the following holds:
1. `A_{t-1} >= 1/2`
2. `L_{t-1} >= 1/2`
3. At least one of the last two observed rounds had `M >= 1/2`

Otherwise play `D`.

**Interpretation of the threshold**
- “At least half of opponents cooperating” is the cooperation floor.
- A single bad round does not trigger defection if the broader recent history is still cooperative.
- Defection is used only after a sustained drop below the cooperation floor.

**Edge cases**
- If `n = 2`, the same rule applies with the opponent cooperation rate being either 0 or 1.
- If `r = 2`, round 1 is `C`; round 2 is `C` if the round-1 opponent cooperated, otherwise `D`.
- If there is no prior history for a statistic, treat that statistic as undefined and ignore it.
- If the current round is the first after a streak of cooperation, keep cooperating unless both of the two most recent observed rounds were below the cooperation floor.

**Altruistic bias**
- When the rule is indifferent, choose `C`.
- Never switch to `D` on the basis of one isolated low-cooperation round.
- After playing `D` once, return to `C` immediately if the next observed round reaches the cooperation floor again.
- On the final round, play `C` whenever the recent average cooperation is at least `1/2`; otherwise mirror the same rule as any other round.
'''

description_ALTRUISTIC_5 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let
\[
s_t=\frac{m_t}{n-1}
\]
be the observed cooperation fraction among opponents in that round.

Maintain two running statistics from past rounds:
- \(A_t\): average opponent cooperation fraction up to round \(t\)
- \(L_t\): length of the current consecutive run of rounds in which \(s_t \ge \tau\)

Use fixed thresholds:
- \( \tau_{\text{high}} = 0.60 \)
- \( \tau_{\text{low}} = 0.30 \)
- \( \tau_{\text{recover}} = 0.50 \)

Decision rule:

1. First round:
   - Play \(C\).

2. Rounds \(2\) through \(r-2\):
   - Play \(C\) if either of the following holds:
     - the recent round’s cooperation was decent: \(s_{t-1} \ge \tau_{\text{recover}}\), or
     - the long-run average cooperation is still respectable: \(A_{t-1} \ge \tau_{\text{low}}\) and the last two rounds were not both weak.
   - Otherwise play \(D\).

   More precisely:
   - If \(s_{t-1} \ge \tau_{\text{recover}}\), play \(C\).
   - Else if \(A_{t-1} \ge \tau_{\text{low}}\) and not \((s_{t-1} < \tau_{\text{low}} \text{ and } s_{t-2} < \tau_{\text{low}})\), play \(C\).
   - Else play \(D\).

3. Recovery rule:
   - If the strategy has defected for one or more rounds because cooperation fell too low, return to \(C\) immediately after any round with \(s_t \ge \tau_{\text{high}}\).

4. Last two rounds:
   - Never switch to defection solely because the game is nearing its end.
   - Continue using the same cooperation rule.
   - If the last observed round had \(s_{t-1} \ge \tau_{\text{recover}}\), play \(C\); otherwise follow the standard rule above.

History update:
- After each round, update
  \[
  A_t=\frac{1}{t}\sum_{u=1}^{t}s_u
  \]
- Track whether the last two observed rounds both had \(s_u < \tau_{\text{low}}\).

Compact pseudocode:

```text
if t == 1:
    play C
else:
    if s[t-1] >= 0.50:
        play C
    else if A[t-1] >= 0.30 and not (s[t-1] < 0.30 and s[t-2] < 0.30):
        play C
    else:
        play D

# recovery override
if last round played D and s[t-1] >= 0.60:
    play C
```

Behavioral profile:
- Start cooperatively.
- Stay cooperative as long as opponents show moderate willingness to cooperate.
- Forgive brief slumps.
- Defect only after sustained low cooperation.
- Re-enter cooperation immediately once opponents resume meaningful cooperation.
'''

description_ALTRUISTIC_6 = '''
**Strategy: Generous Responsive Cooperation**

**State tracked**
- `m_t`: number of opponents who cooperated in round `t`
- `h_t = m_t / (n - 1)`: observed cooperation rate among opponents in round `t`
- `H_t`: history of the last few cooperation rates

**Round 1**
- Play `C`.

**For round t > 1**
1. Compute `h_{t-1}` from the previous round.
2. Compute the recent average cooperation rate:
   - `A_t = average(h_{t-1}, h_{t-2}, h_{t-3})`, using only available past rounds.
3. Cooperate if at least one of the following holds:
   - `h_{t-1} >= 0.5`
   - `A_t >= 0.5`
   - `h_{t-1} >= 1/3` and `h_{t-1} >= h_{t-2}`

4. Defect only if both of the following hold:
   - `h_{t-1} < 1/3`
   - `A_t < 0.5`

**Last round**
- Play `C` unless the previous two rounds both had very low cooperation:
  - defect only if `h_{t-1} < 1/3` and `h_{t-2} < 1/3`

**Early rounds**
- In round 2, use only `h_1`:
  - cooperate if `h_1 >= 1/2`
  - otherwise cooperate once more unless `h_1 = 0`
- In round 3, use `h_1`, `h_2`, and their average, with the same thresholds.

**Detailed rule in pseudocode**
```text
if t == 1:
    action = C
else:
    h1 = m_{t-1} / (n-1)
    h2 = m_{t-2} / (n-1) if t >= 3 else h1
    h3 = m_{t-3} / (n-1) if t >= 4 else h2
    A  = (h1 + h2 + h3) / number_of_terms_used

    if t == r:
        if h1 < 1/3 and h2 < 1/3:
            action = D
        else:
            action = C
    else:
        if h1 >= 1/2:
            action = C
        elif A >= 1/2:
            action = C
        elif h1 >= 1/3 and h1 >= h2:
            action = C
        else:
            action = D
```

**Interpretation of the behavior**
- Begin with unconditional cooperation.
- Keep cooperating as long as the group shows at least moderate cooperation.
- Forgive short-term drops if the recent average remains acceptable.
- Defect only after sustained low cooperation.
- Restore cooperation immediately when the group’s cooperation improves again.
'''

description_ALTRUISTIC_7 = '''
Play `C` in round 1.

For each round `t > 1`, let `x_{t-1}` be the number of opponents who cooperated in the previous round, and let `q_{t-1} = x_{t-1} / (n - 1)` be the observed cooperation rate among opponents.

Use this rule:

- Cooperate if `q_{t-1} >= 1/2`
- Cooperate if `q_{t-1} < 1/2` but at least one of the last two rounds had `q >= 1/2`
- Defect only if `q < 1/2` in each of the last two observed rounds
- After any round in which you defect, return to `C` immediately if `q_{t-1} >= 1/2`

Edge cases:

- `n = 2`: cooperate in round 1; afterward, cooperate whenever the other player cooperated in the previous round, and defect only after two consecutive rounds of their defection
- `r = 2`: cooperate in round 1; in round 2, cooperate unless the previous round showed zero opponent cooperation
- Final round: cooperate unless the previous two observed rounds both had `q = 0`

Equivalent pseudocode:

```text
state = "C"
history = []

for t in 1..r:
    if t == 1:
        play C
    else:
        q1 = history[t-2].opp_coop / (n-1)
        q2 = history[t-3].opp_coop / (n-1) if t >= 3 else 1

        if q1 >= 1/2:
            play C
        else if q2 >= 1/2:
            play C
        else:
            play D

    observe opp_coop after round t
    history.append({opp_coop})
```

Altruistic priority:

- Default to cooperation
- Forgive immediately after any sign of renewed cooperation
- Use defection only as a brief response to sustained free-riding
- Never escalate beyond a single-round refusal to subsidize repeated defection
'''

description_ALTRUISTIC_8 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\), and let \(m=n-1\).

**State variables**
- `low_streak`: consecutive rounds of very low opponent cooperation
- Define **very low cooperation** as \(x_t \le \lfloor m/3 \rfloor\)

**Decision rule**

1. **Round 1**
   - Play **C**

2. **Rounds 2 through r**
   - If the previous round was **very low cooperation**:
     - increment `low_streak`
   - Otherwise:
     - set `low_streak = 0`

   - Play **D** only if:
     - `low_streak >= 2`
   - Otherwise play **C**

**Interpretation of the rule**
- Start by cooperating immediately.
- Continue cooperating as long as there is at least some meaningful cooperative presence.
- If the group shows two consecutive rounds of near-total defection, respond with one or more rounds of defection until cooperation reappears.
- The moment the previous round is no longer very low cooperation, reset `low_streak` to 0 and return to **C**.

**Last round**
- Play **C** unless you are already in a `low_streak >= 2` state, in which case play **D**.

**Equivalent compact pseudocode**
```text
if t == 1:
    play C
else:
    if x_{t-1} <= floor((n-1)/3):
        low_streak += 1
    else:
        low_streak = 0

    if low_streak >= 2:
        play D
    else:
        play C
```
'''

description_BENEVOLENT_1 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(m_t^\ast\) be the number of cooperating opponents in the previous round that you observed.

Define:

- \(q = n-1\), the number of opponents
- \(H_t = \frac{1}{t-1}\sum_{s=1}^{t-1} m_s\) for \(t \ge 2\), the average number of cooperating opponents so far
- \(L_t = \max\{m_{t-1}, m_{t-2}\}\) when those rounds exist

Decision rule:

1. Round 1:
   - Play \(C\).

2. Round 2:
   - Play \(C\) if \(m_1 \ge \lceil q/2 \rceil\).
   - Otherwise play \(D\).

3. Round \(t\) for \(3 \le t \le r-1\):
   - Play \(C\) if either of the following holds:
     - \(m_{t-1} \ge \lceil q/2 \rceil\), or
     - \(L_t \ge \lceil q/2 \rceil\) and \(m_{t-1} \ge \lceil q/3 \rceil\).
   - Otherwise play \(D\).

4. Final round \(t=r\):
   - Play \(C\) if \(m_{r-1} \ge \lceil q/2 \rceil\).
   - If \(m_{r-1} < \lceil q/2 \rceil\), still play \(C\) unless both of the last two observed rounds had weak cooperation:
     - if \(m_{r-1} < \lceil q/3 \rceil\) and \(m_{r-2} < \lceil q/3 \rceil\), play \(D\);
     - otherwise play \(C\).

State update after each round:

- If you played \(C\), remain in cooperative mode unless the observed cooperation falls below the thresholds above for two consecutive rounds.
- If you played \(D\), return to \(C\) immediately once the cooperation condition is satisfied again.

Compact pseudocode:

```text
if t == 1:
    action = C

else if t == 2:
    action = C if m[1] >= ceil((n-1)/2) else D

else if t < r:
    if m[t-1] >= ceil((n-1)/2):
        action = C
    else if max(m[t-1], m[t-2]) >= ceil((n-1)/2) and m[t-1] >= ceil((n-1)/3):
        action = C
    else:
        action = D

else:  # t == r
    if m[r-1] >= ceil((n-1)/2):
        action = C
    else if m[r-1] < ceil((n-1)/3) and m[r-2] < ceil((n-1)/3):
        action = D
    else:
        action = C
```

Benevolent orientation:

- Start by cooperating.
- Reward sustained cooperation quickly by continuing to cooperate.
- Respond to persistent low cooperation with temporary defection.
- Resume cooperation immediately when cooperation recovers.
- End with cooperation unless the group has shown repeated, clearly low cooperation.
'''

description_BENEVOLENT_2 = '''
Round 1: Cooperate.

For round t > 1, let m_{t-1} be the number of opponents who cooperated in the previous round, and let q_{t-1} = m_{t-1} / (n - 1).

Keep a cooperation score S_t updated from observed history:
- Initialize S_1 = 0.
- After each round t - 1, update
  S_t = 0.7 · S_{t-1} + 0.3 · q_{t-1}.

Decision rule for round t:
- Cooperate if either of the following holds:
  - q_{t-1} ≥ 1/2, or
  - S_t ≥ 1/2.
- Defect otherwise.

Last-round rule:
- Cooperate in the final round if q_{r-1} ≥ 1/3 or S_r ≥ 1/2.
- Otherwise defect.

Stabilization rule:
- If the observed opponent cooperation rate has been at least 1/2 in each of the last two rounds, cooperate unconditionally.
- If the observed opponent cooperation rate has been 0 in each of the last two rounds, defect for the next two rounds, then resume the standard rule.

Forgiveness rule:
- After any round with q_{t-1} < 1/2, continue cooperating for one more round unless q_{t-1} = 0 and S_t < 1/3.
- If cooperation resumes to q_{t-1} ≥ 1/2, immediately return to cooperative mode.

Edge cases:
- If n = 2, replace q_{t-1} with 1 if the other player cooperated and 0 otherwise.
- If r = 2, cooperate in round 1 and apply the last-round rule in round 2.
- If no history is available for a rule check, default to cooperate.
- If two different rules conflict, use the more cooperative action.
'''

description_BENEVOLENT_3 = '''
Round 1: play C.

After each round t ≥ 1, observe m_t = number of opponents who cooperated in that round, and let p_t = m_t / (n - 1).

Maintain:
- s_t = exponentially weighted cooperation score
- update after each round: s_t = λ s_{t-1} + (1 - λ) p_t, with s_0 = 1 and λ = 0.75
- a short-run floor f_t over the last 2 rounds: f_t = minimum of p_t and p_{t-1} when both exist; otherwise f_t = p_t

Decision rule for round t + 1:
1. If t = r, no decision needed.
2. If t = 1, play C.
3. Otherwise, play C if either of these holds:
   - s_t ≥ 0.5
   - f_t ≥ 0.5
   Otherwise play D.

Forgiveness rule:
- If the previous round had p_t < 0.5 but the score s_t is still at least 0.5, continue cooperating.
- If cooperation has been below 0.5 for two consecutive rounds, switch to D until either:
  - a round reaches p_t ≥ 0.5, or
  - the weighted score s_t returns to at least 0.5

Recovery rule:
- After any round with p_t ≥ 0.5, immediately return to C on the next round.

Endgame rule:
- In the last 2 rounds, if p_t ≥ 0.5 in the most recent observed round, play C.
- Otherwise, play D only if both of the last 2 observed rounds were below 0.5; if not, keep cooperating.

Special cases:
- If n = 2, interpret p_t as the single opponent’s cooperation indicator; cooperate after any cooperative round and defect only after two consecutive defections by the opponent.
- If r = 2, play C in round 1 and apply the recovery rule in round 2.
- If all observed opponents cooperate in a round, reset s_t to 1.
- If no history exists beyond the current round, default to C.
'''

description_BENEVOLENT_4 = '''
Round 1: play C.

For round t > 1, let x_t be the number of opponents who cooperated in round t - 1, and let a_t be the average of x over the last up to 3 rounds, with more weight on the most recent round:
- if t = 2, a_t = x_1
- if t = 3, a_t = (2x_2 + x_1) / 3
- if t ≥ 4, a_t = (3x_{t-1} + 2x_{t-2} + x_{t-3}) / 6

Define the cooperation threshold
- T = ceil((n - 1) / 2)

Decision rule:
1. If t = r, play C.
2. Else if the last two rounds both had x < T, play D.
3. Else if a_t ≥ T, play C.
4. Else play C with a probe pattern: cooperate every third round while in this low-cooperation state, and defect in the other two.

State handling:
- Start in “open” state.
- In open state, apply rules 1–3.
- If rule 2 triggers, switch to “guarded” state.
- In guarded state, keep applying the probe pattern until either:
  - one round has x ≥ T, then return to open state immediately, or
  - two consecutive probe rounds are met with x < T, in which case continue guarded without changing anything.

Edge cases:
- If n = 2, use T = 1.
- If r = 2, play C in both rounds.
- If only one prior round exists, use that round alone for a_t.
- If the observed cooperation count is exactly at the threshold, treat it as cooperative enough and play C.

Behavioral posture:
- Start with trust.
- Maintain cooperation whenever the group is roughly cooperative.
- Respond to sustained free-riding with limited, temporary restraint.
- Re-open cooperation at the first clear sign of reciprocity.
- End with cooperation regardless of history.
'''

description_BENEVOLENT_5 = '''
Round 1: play C.

For each round t ≥ 2, let x_t be the number of your opponents who cooperated in round t−1.

Compute:
- coop_share = x_t / (n − 1)
- recent_avg = average of the last up to 3 values of coop_share, including the most recent one
- trend = coop_share − previous coop_share, treating missing previous value as 0

Decision rule:
- Play C if any of the following holds:
  - coop_share ≥ 1/2
  - recent_avg ≥ 1/2
  - coop_share increased from the previous round and coop_share ≥ 1/3
- Otherwise play D.

For the final round:
- Play C if coop_share in the previous round was at least 1/3.
- Otherwise play D.

Persistent-behavior override:
- If x_t = 0 for two consecutive observed rounds, play D until you observe at least one opponent cooperation in a round.
- If after any D phase you observe x_t ≥ ceil((n−1)/2), immediately return to C.

Implementation sketch:
```
state:
  last_x = None
  zero_streak = 0

round 1:
  action = C

round t >= 2:
  coop_share = last_x / (n - 1)

  if last_x == 0:
      zero_streak += 1
  else:
      zero_streak = 0

  if t == r:
      action = C if coop_share >= 1/3 else D
  elif zero_streak >= 2:
      action = D
  elif coop_share >= 1/2:
      action = C
  elif recent_avg(last up to 3 coop_share values) >= 1/2:
      action = C
  elif previous_coop_share is not None and coop_share > previous_coop_share and coop_share >= 1/3:
      action = C
  else:
      action = D

  after observing x_t:
      update last_x = x_t
```

If you ever need a tie-breaker between C and D under the same condition, choose C.
'''

description_BENEVOLENT_6 = '''
Initialize in a cooperative state.

Let `q_t` be the number of opponents who cooperated in round `t`.

Define the cooperation threshold
`τ = max(1, ceil((n - 1) / k))`.

Decision rule:

- Round 1: play `C`.

- For each round `t ≥ 2`:
  - If `q_{t-1} ≥ τ`, play `C` and clear any warning state.
  - If `q_{t-1} < τ` and you were not already in warning state, play `C` this round and enter warning state.
  - If `q_{t-1} < τ` and you were already in warning state, play `D` this round and keep warning state active.

Warning state:
- Set it to active after one below-threshold round.
- Reset it to inactive immediately after any round in which `q_t ≥ τ`.

Interpretation of the edge cases:
- First round: cooperate unconditionally.
- Single-round dip in cooperation: forgive it and continue cooperating.
- Two consecutive low-cooperation rounds: defect once.
- Any return to sufficient cooperation: immediately return to cooperation.
- Final round: use the same rule as any other round; do not change behavior just because the game is ending.

This makes cooperation the default, forgives isolated defections, and uses defection only as a temporary boundary when group cooperation repeatedly falls below the threshold.
'''

description_BENEVOLENT_7 = '''
Round 1:
- Cooperate.

For round t > 1, let m be the number of other players who cooperated in round t−1, and let p = m / (n−1).

Maintain two internal states:
- trust score S, initialized to 0
- streak F, the number of consecutive rounds in which at least half of the others cooperated, initialized to 0

Update after each round:
- If p = 1, set S = min(S + 2, 4)
- If p ≥ 1/2, set S = min(S + 1, 4) and F = F + 1
- If p < 1/2, set S = max(S − 2, −4) and F = 0

Decision rule for round t:
- Cooperate if all of the following hold:
  - S ≥ −1
  - m ≥ ceil((n−1)/2) for the previous round, or F ≥ 2
- Defect otherwise

Special handling:
- If the previous round had no cooperators among the others, defect for the next round unless at least two of the last three rounds each had p ≥ 1/2.
- If the previous round had full cooperation among the others, cooperate next round regardless of S, unless the last two rounds before that both had p = 0.
- In the final round, cooperate if the previous round had p ≥ 1/2 or if S ≥ 0; otherwise defect.

Recovery rule:
- After any defecting round by the others, give one forgiving cooperation if the next round has at least one cooperator among the others.
- After two consecutive rounds with p ≥ 1/2, return fully to cooperation.

Persistent cooperation rule:
- If the last three rounds each had p ≥ 1/2, cooperate until a round occurs with p < 1/3.
- If the last three rounds each had p = 1, cooperate unconditionally thereafter unless there are two consecutive rounds with p = 0.

Minimum benevolence rule:
- Never defect in response to a single isolated shortfall when the others are mostly cooperating.
- Never require perfect cooperation from the others to keep cooperating, unless repeated free-riding has built up through the trust score.
'''

description_BENEVOLENT_8 = '''
Round 1: cooperate.

Maintain for each round t:
- `s(t-1)`: number of opponents who cooperated in the previous round
- `h(t-1)`: the recent cooperation rate among opponents, defined as the average of the last up to 3 observed `s` values divided by `n-1`
- `best_seen`: the largest `s` observed so far

Decision rule for round t > 1:

1. If the previous round had unanimous cooperation among opponents (`s(t-1) = n-1`), cooperate.
2. Else if the recent cooperation rate is at least 1/2, cooperate.
3. Else if the previous round had at least `ceil((n-1)/2)` cooperating opponents, cooperate.
4. Else defect.

Adjustment rules:
- If cooperation rises for two consecutive observed rounds, stay with cooperation.
- If cooperation falls for two consecutive observed rounds, switch to defect until cooperation recovers to at least half of opponents.
- If `best_seen = n-1` has ever occurred, remain cooperative whenever the most recent round had at least `n-2` cooperating opponents.
- If opponents alternate unpredictably, choose the action that matches the majority of the last observed round; ties are broken in favor of cooperation.

Last round:
- Cooperate if at least half of opponents cooperated in the previous round.
- Otherwise defect.

Tie and edge handling:
- If `n = 2`, cooperate after any round in which the opponent cooperated; defect only after a round in which the opponent defected.
- If no prior history exists, cooperate.
- If observations are incomplete or indistinguishable across the recent window, default to cooperation unless the most recent round was strictly below half cooperation.

State update after each round:
- Record observed `s(t)`
- Update `best_seen`
- Recompute `h(t)` from the last up to 3 rounds

Behavioral core:
- Start cooperative.
- Match and reinforce mutual cooperation.
- Keep cooperating through moderate or improving cooperation.
- Defect only after clear, repeated evidence that cooperation is below half of opponents.
'''

description_SELFISH_1 = '''
Play D in every round.

Decision rule:
- For t = 1: choose D.
- For every later round t = 2, 3, ..., r: choose D regardless of:
  - how many opponents cooperated last round,
  - your own previous actions,
  - any cooperation trend,
  - the round number.

Edge cases:
- First round: D.
- Last round: D.
- If all opponents cooperated previously: D.
- If all opponents defected previously: D.
- If cooperation rises or falls over time: D.
- If any history is unavailable or incomplete: D.

State update:
- You may record the observed number of opponent cooperators after each round, but it never changes the action choice.

Pseudocode:
```text
for t in 1..r:
    play D
```
'''

description_SELFISH_2 = '''
Play D in every round, regardless of the round number, past observed cooperation counts, or any other history.

Decision rule:
- If t ∈ {1, 2, ..., r}, choose D.

Edge cases:
- First round: choose D.
- Any intermediate round: choose D.
- Last round: choose D.
- If history is unavailable or incomplete: choose D.
- If multiple prior rounds show high cooperation: still choose D.
- If all opponents defected previously: choose D.
- If all opponents cooperated previously: still choose D.

Pseudocode:
```text
for each round t:
    action = D
```
'''

description_SELFISH_3 = '''
Round 1: play D.

Every subsequent round t = 2, ..., r: play D.

Ignore the observed number of cooperators in previous rounds.

If the implementation allows any tie-break or default state, resolve it in favor of D.

Pseudocode:
```text
for each round t:
    choose D
```
'''

description_SELFISH_4 = '''
Play D in every round, regardless of history, observed cooperation counts, round number, or opponent behavior.

Decision rule:
- Round 1: D
- Rounds 2 through r-1: D
- Round r: D

If you want it as pseudocode:

```text
for t in 1..r:
    choose D
```

Use the observed history only as bookkeeping; never let it change the action.
'''

description_SELFISH_5 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Any later round t: D
- If history is incomplete, noisy, or ambiguous: default to D
- If you are indifferent between actions for any reason: choose D

Implementation:
```text
for each round t = 1..r:
    choose D
```

Edge cases:
- Last round: D
- If opponents cooperated heavily in earlier rounds: still D
- If opponents all defected earlier: D
- If the number of rounds is unknown or changes: D
- If you observe any pattern in opponent behavior: ignore it and play D

State:
- No memory is needed
- No adaptation is needed
- No retaliation, forgiveness, experimentation, or mixing is used
'''

description_SELFISH_6 = '''
Play D in every round.

Decision rule:
- Round 1: D.
- Round t = 2 to r-1: D, regardless of the observed number of cooperators in previous rounds.
- Final round r: D.

History use:
- Ignore past cooperation counts for action choice.
- Do not condition on reciprocity, punishment, or momentum.
- If any external tie-break or implementation detail requires a state update, keep state empty.

Edge cases:
- If a round is skipped or the observation is missing, default to D.
- If the game ends early, no change: D until termination.

Behavioral posture:
- Never pay the contribution cost.
- Treat cooperation as something other players may do, not something to match.
- Exploit any cooperative environment by free-riding; do not attempt to sustain it by paying into it.
'''

description_SELFISH_7 = '''
Round 1: defect.

For round t > 1, let h_{t-1} be the number of opponents who cooperated in the previous round, and let h_{t-2} be the number from two rounds ago when available.

Set the cooperation threshold
q = ceil((n - 1) * (1 - 1 / k)).

Play C only if all of the following are true:
- t < r
- h_{t-1} >= q
- if t >= 3, also h_{t-2} >= q

Otherwise play D.

If the threshold condition fails in any round, immediately revert to D in the next round and stay with D until the condition is satisfied again.

Last round: defect.

If there is any ambiguity because the history is too short, default to defect.
'''

description_SELFISH_8 = '''
Play D in every round, regardless of history.

Decision rule:
- Round 1: D
- Any intermediate round: D
- Final round: D
- If you observe any number of opponents cooperating in the previous round, still play D
- If all opponents cooperated in the previous round, still play D
- If no opponents cooperated in the previous round, still play D

Implementation:
```text
for each round t = 1..r:
    choose D
```

State:
- Maintain no state
- Ignore all observed cooperation counts
- Do not condition on past rounds, since there is no action that changes future incentives in a way that benefits cooperation for a selfish player
'''

description_SELFINTERESTED_1 = '''
Maintain a rolling cooperation signal from the observed number of cooperative opponents.

Let `m = n - 1` be the number of opponents.
Let `x_t` be the number of opponents who cooperated in round `t`.

Decision rules:

- Round 1: play `D`.
- Round `t` where `2 ≤ t < r`:
  - Compute `s = x_{t-1} + x_{t-2}` when both exist; otherwise use `s = x_{t-1}`.
  - Play `C` iff the observed cooperation in the recent window is strong:
    - if two rounds are available: `s ≥ m`
    - if only one round is available: `x_{t-1} ≥ ceil(m / 2)`
  - Otherwise play `D`.
- Round `r`: play `D`.

Equivalent compact rule:

```text
if t == 1:
    action = D
elif t == r:
    action = D
else:
    recent = cooperation counts from the last 1–2 rounds
    if average(recent) >= m/2:
        action = C
    else:
        action = D
```

Edge handling:

- If a prior round is missing, use only the available history.
- After any round with weak observed cooperation, switch to `D` immediately.
- After two consecutive rounds of strong observed cooperation, return to `C`.
- Never cooperate in the final round.
'''

description_SELFINTERESTED_2 = '''
State variables:
- `mode ∈ {DEFECT, PROBE, COOPERATE}`
- `good_streak`: number of consecutive recent rounds in which the observed number of cooperating opponents met the cooperation threshold
- `bad_streak`: number of consecutive recent rounds below that threshold

Set the cooperation threshold to:
- `T = n - 2` if `n > 2`
- `T = 0` if `n = 2`

Decision rule:

1. Round 1:
- Play `D`

2. Rounds 2 through `r - 1`:
- Let `x_t` be the number of cooperating opponents observed in round `t`.
- If `mode = DEFECT`:
  - Play `C` only if both of the last two observed rounds satisfied `x ≥ T`
  - Otherwise play `D`
- If `mode = PROBE`:
  - Play `C` for exactly one round
  - After that round:
    - if `x ≥ T`, set `mode = COOPERATE`
    - else set `mode = DEFECT`
- If `mode = COOPERATE`:
  - Play `C` if `x ≥ T`
  - Play `D` immediately if `x < T`, and set `mode = DEFECT`

3. Last round `r`:
- Play `D`

Transition rules:
- Start in `DEFECT`
- Enter `PROBE` only after seeing two consecutive rounds with `x ≥ T`
- Enter `COOPERATE` only after a successful probe with `x ≥ T`
- Any failure below threshold while in `COOPERATE` sends you back to `DEFECT`

Memory requirements:
- Store only the last two observed cooperation counts and the current mode

Behavior summary:
- Default to defection
- Cooperate only after sustained near-universal cooperation by others
- Exit cooperation immediately if cooperation weakens
- Defect in the final round regardless of history
'''

description_SELFINTERESTED_3 = '''
Initialize with cooperation in round 1.

For each round t = 2, 3, ..., r:

1. Let q_t be the observed fraction of all players who cooperated in round t - 1:
   q_t = (observed cooperating opponents in round t - 1 + your own action in round t - 1) / n

2. Let m_t be the average of q over the most recent up to 3 completed rounds:
   m_t = average(q_{t-1}, q_{t-2}, q_{t-3}) over the rounds that exist

3. Cooperate in round t if and only if both conditions hold:
   - t < r
   - m_t >= 1 / k

4. Otherwise defect.

Edge rules:
- Round 1: play C.
- Round r: play D.
- If there is only one prior round available, use that single q value for m_t.
- If the last 3 rounds are not all available, average only the available ones.
- After any round in which q_t falls below 1 / k, switch to D immediately until the 3-round average m_t rises back to at least 1 / k.

Optional persistence rule for stability:
- If m_t is exactly 1 / k, cooperate only if q_t did not decline from the previous round; otherwise defect.
'''

description_SELFINTERESTED_4 = '''
Round 1: play D.

After each round t, let x_t be the number of other players who cooperated, so the observed total cooperation is s_t = x_t + c_t where c_t is your own action.

Maintain the last observed cooperation rate among opponents:
- q_t = x_t / (n - 1)

Use this rule for rounds 2 through r - 1:

- Cooperate only if both conditions hold:
  1. At least a strict majority of opponents cooperated last round:
     x_{t-1} > (n - 1) / 2
  2. The observed cooperation rate has not dropped:
     q_{t-1} >= q_{t-2} if t >= 3

Otherwise, defect.

Endgame rule:
- In round r, play D.
- In round r - 1, play D as well unless x_{r-2} = n - 1 and x_{r-3} = n - 1 if those rounds exist; only then cooperate in round r - 1.
- In round r - 2 and earlier, follow the regular rule above.

Memory and update rule:
- Store only the last two observed opponent cooperation counts.
- If the previous round is unavailable, use the default action D.
- If the previous two rounds are identical and above the majority threshold, continue cooperating; if cooperation falls at any point, switch to D immediately.

Equivalent pseudocode:

```
if t == 1:
    play D
elif t == r:
    play D
elif t == r - 1:
    if t >= 3 and x[t-2] == n-1 and x[t-3] == n-1:
        play C
    else:
        play D
else:
    if x[t-1] > (n-1)/2 and (t == 2 or x[t-1] >= x[t-2]):
        play C
    else:
        play D
```

Adjustment for even n:
- Replace “strict majority” with “at least n/2 opponents cooperating” only if x_{t-1} = n/2 and x_{t-2} = n/2 as well; otherwise require x_{t-1} > n/2.

Adjustment for very small n:
- If n = 2, cooperate only after the opponent has cooperated in two consecutive observable rounds; otherwise defect.

Reaction to collapse:
- If the number of cooperating opponents ever drops by 2 or more from one round to the next, defect in the next round and continue defecting until cooperation returns to the majority threshold for two consecutive rounds.

Reaction to stable cooperation:
- If the majority threshold is met for three consecutive non-final rounds, cooperate until either the threshold fails or the endgame rule begins.
'''

description_SELFINTERESTED_5 = '''
Round 1: play D.

For rounds 2 through r-1:
- Let x_{t-1} be the number of opponents who cooperated in round t-1.
- Let x_{t-2} be the number of opponents who cooperated in round t-2, when available.
- Play C only if x_{t-1} = n-1 and x_{t-2} = n-1.
- Otherwise play D.

Reset rule:
- If you ever observe any round with x_t < n-1, stop cooperating immediately and keep playing D until you again observe two consecutive rounds with x = n-1.

Last round r: play D.

Special cases:
- If r = 2, play D in both rounds.
- If n = 2, “x_t = n-1” means the single opponent cooperated.
- If you have not yet seen two rounds of full opponent cooperation, always play D.
'''

description_SELFINTERESTED_6 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Every later round: D, regardless of how many opponents cooperated in prior rounds
- Final round: D
- If any tie-breaking, fallback, or incomplete history occurs: D

State update:
- Keep no cooperation threshold, retaliation logic, forgiveness logic, or frequency estimate
- Do not condition on observed counts of opponent cooperation

Self-interested implementation:
- Never contribute under any history
- Use observed history only as confirmation that future cooperation by others should be exploited, not reciprocated
'''

description_SELFINTERESTED_7 = '''
Round 1:
- Cooperate if `k / n >= 1/2`; otherwise defect.

For rounds `t = 2 ... r-1`:
- Let `m_{t-1}` be the number of opponents who cooperated in round `t-1`.
- Let `x_{t-1} = m_{t-1} / (n-1)` be the observed opponent cooperation rate.
- Cooperate in round `t` iff all of the following hold:
  - `x_{t-1} >= 1/2`
  - `x_{t-1} >= x_{t-2} - 1/(n-1)` when `t >= 3`  
    (i.e., do not reward a clear drop in cooperation)
  - `k/n > 1/2`  
- Otherwise defect.

Last round `t = r`:
- Defect.

Memory and update rule:
- Track only the last two observed cooperation rates.
- If a round is fully cooperative among opponents, keep cooperating in the next nonterminal round.
- If opponent cooperation falls below half, switch to defect immediately.
- If cooperation is stable but just below half, continue defecting until it rises above half again.

Default fallback:
- If any observation is missing or ambiguous, defect for that round and resume the rule above on the next round.

Compact pseudocode:
```text
if t == 1:
    play C if k/n >= 1/2 else D

else if t == r:
    play D

else:
    x = opponents_cooperated_last_round / (n-1)
    if t >= 3:
        x_prev = opponents_cooperated_two_rounds_ago / (n-1)
    else:
        x_prev = x

    if (k/n > 1/2) and (x >= 1/2) and (x >= x_prev - 1/(n-1)):
        play C
    else:
        play D
```
'''

description_SELFINTERESTED_8 = '''
- Round 1: play D.

- For rounds 2 through r-2:
  - Let `m_prev` be the number of opponents who cooperated in the previous round.
  - Let `m_prev2` be the number of opponents who cooperated two rounds ago; if unavailable, treat it as 0.
  - Play C only if both conditions hold:
    1. `m_prev = n - 1` or `m_prev >= n - 2`
    2. `m_prev >= m_prev2`
  - Otherwise play D.

- For round r-1:
  - Play C only if the previous two rounds were both near-universal cooperation:
    - `m_prev >= n - 2` and `m_prev2 >= n - 2`
  - Otherwise play D.

- For round r:
  - Play D.

- Update rule:
  - After each round, record only the aggregate cooperation count.
  - If a cooperative round is followed by any clear drop in observed cooperation, switch to D immediately and stay on D until the opponents return to near-universal cooperation for two consecutive rounds.

- Minimal implementation:
```text
state = "D"
history = []

for t in 1..r:
    if t == 1:
        action = D
    elif t == r:
        action = D
    elif t == r-1:
        action = C if history[t-1] >= n-2 and history[t-2] >= n-2 else D
    else:
        action = C if history[t-1] >= n-2 and history[t-1] >= history[t-2] else D

    observe m_t
    history.append(m_t)
```

- Reset condition:
  - Any round with fewer than `n-2` cooperating opponents breaks the cooperative phase.
  - Cooperation resumes only after two consecutive rounds at `n-2` or `n-1` cooperating opponents.

- Self-interested posture:
  - Default to D.
  - Use C only as a conditional response to sustained, near-universal cooperation.
  - Never cooperate into visible instability or in the final round.
'''

description_OPPORTUNISTIC_1 = '''
Maintain a cooperation score `s` initialized at 0.

For each round `t`:

### 1) First round
Play `C`.

### 2) Update rule after observing the previous round
Let `m` be the number of opponents who cooperated in the previous round.

Update:
- `s = 0.7 * s + (m / (n - 1)) - 0.5`

Clamp `s` to the interval `[-2, 2]`.

Interpretation of `s`:
- `s > 0` means the group is currently cooperative enough to exploit with cooperation.
- `s <= 0` means defecting is the current default.

### 3) Decision rule for round `t`
Play `C` if all of the following hold:
- `s >= 0.25`
- `m >= ceil((n - 1) / 2)` in the previous round
- the last two rounds were not both low-cooperation rounds, where a low-cooperation round means `m < ceil((n - 1) / 3)`

Otherwise play `D`.

### 4) Opportunistic switching
If you played `D` last round and at least `ceil(2(n - 1)/3)` opponents cooperated last round, then play `C` immediately in the next round, even if `s` is only slightly positive.

If you played `C` last round and fewer than `ceil((n - 1) / 3)` opponents cooperated, switch to `D` next round.

### 5) Endgame
For the last round, play `D` unless both of the following are true:
- at least `ceil((n - 1) / 2)` opponents cooperated in the previous round
- `s >= 0.5`

For the final two rounds, if the most recent observed cooperation count drops below `ceil((n - 1) / 3)`, defect for all remaining rounds.

### 6) Re-entry rule after defection
If you have defected for at least one round, return to `C` only after seeing two consecutive rounds with:
- `m >= ceil((n - 1) / 2)`, and
- the second of those two rounds has `m` at least as large as the first

### 7) Default behavior
If none of the above conditions force `C`, play `D`.
'''

description_OPPORTUNISTIC_2 = '''
Round 1: Defect.

Maintain two internal counts from history:
- `m_t`: number of opponents who cooperated in round `t`
- `s_t`: your moving estimate of cooperative tendency, initialized from observed history

Update after each round:
- `s_t = 0.7 * s_{t-1} + 0.3 * (m_t / (n - 1))`

Decision rule for round `t + 1`:

1. **Always defect on the final round.**

2. **If the previous round had very low cooperation**  
   If `m_t <= floor((n - 1) / 3)`, defect next round.

3. **If cooperation is strong enough to exploit safely**  
   If `m_t >= ceil(2 * (n - 1) / 3)`, cooperate next round.

4. **If cooperation is moderate, use a one-round opportunistic test**
   - Cooperate only if all of the following hold:
     - `m_t >= ceil((n - 1) / 2)`
     - `s_t >= 0.5`
     - you defected in round `t`
   - Otherwise defect.

5. **If there is a recent upward trend, join it briefly**
   - Let `Δ_t = m_t - m_{t-1}` when `t >= 2`
   - If `Δ_t >= 2` and `m_t >= ceil((n - 1) / 2)`, cooperate next round
   - Otherwise defect

6. **Exploit then retreat**
   - After any round in which you cooperate, keep cooperating only while:
     - `m_t >= ceil((2 * (n - 1)) / 3)`
   - The moment observed cooperation drops below that threshold, defect immediately.

Edge cases:
- **Round 1:** defect.
- **Round 2:** cooperate only if round 1 had at least `ceil(2 * (n - 1) / 3)` cooperating opponents; otherwise defect.
- **Very small groups (`n = 2` or `n = 3`):**
  - Use the same thresholds, but round them exactly as written.
  - For `n = 2`, cooperate only after observing cooperation from the single opponent in the previous round.
- **Final two rounds:** defect unless both of the previous two rounds met the strong-cooperation threshold.

Compact pseudocode:

```text
if t == 1:
    play D
elif t == r:
    play D
elif t == 2:
    if m_1 >= ceil(2*(n-1)/3):
        play C
    else:
        play D
else:
    if m_t <= floor((n-1)/3):
        play D
    elif m_t >= ceil(2*(n-1)/3):
        play C
    elif m_t >= ceil((n-1)/2) and s_t >= 0.5 and last_action == D:
        play C
    elif t >= 2 and (m_t - m_{t-1}) >= 2 and m_t >= ceil((n-1)/2):
        play C
    else:
        play D
```

History update:
- If you cooperated and the observed cooperation rate remains high, continue cooperating to ride the cooperative wave.
- If cooperation weakens or becomes unstable, switch immediately to defection and wait for a new strong signal before re-entering cooperation.
'''

description_OPPORTUNISTIC_3 = '''
Let \(H = \lceil (n-1)/2 \rceil\) and \(L = \lfloor (n-1)/3 \rfloor\).

State variables:
- \(x_t\): number of opponents who cooperated in round \(t\)
- \(g\): consecutive rounds ending at \(t\) with \(x \ge H\)
- \(b\): consecutive rounds ending at \(t\) with \(x \le L\)

Decision rule:

1. **Round 1:** play \(D\).

2. **Rounds \(2\) through \(r-2\):**
   - If the previous round had a high cooperation level, \(x_{t-1} \ge H\), then play \(C\).
   - Otherwise play \(D\).
   - If \(x_{t-1} \le L\), increment \(b\); otherwise reset \(b = 0\).
   - If \(b = 3\), then on the next non-final round play \(C\) once as a probe, then reset \(b = 0\).

3. **Probe handling:**
   - If you played \(C\) as a probe and \(x_t \ge H\), treat that as a successful recovery and continue playing \(C\) on subsequent rounds while \(x_{t-1} \ge H\).
   - If the probe does not reach \(H\), revert to \(D\) immediately on the next round.

4. **Rounds \(r-1\) and \(r\):** play \(D\).

5. **Default behavior between probes:** play \(D\) unless the observed cooperation level in the previous round is already high enough to justify joining it.

Compact pseudocode:

```text
if t == 1:
    action = D
elif t >= r-1:
    action = D
else:
    if x[t-1] >= H:
        action = C
    else:
        action = D

    if x[t-1] <= L:
        b += 1
    else:
        b = 0

    if b == 3 and t < r-2:
        action = C
        b = 0
```

This strategy cooperates only when cooperation is already widespread, defects whenever cooperation is weak, and uses occasional probes after sustained low-cooperation periods to detect whether a cooperative pattern has reappeared.
'''

description_OPPORTUNISTIC_4 = '''
Initialize a cooperation score for the population:

- Let `g = 0` at start.
- After round `t`, observe `m_t` = number of opponents who cooperated.
- Update `g = 0.8*g + m_t` if `m_t > 0`; otherwise `g = 0.8*g - 1`.
- Clamp `g` to `[0, n-1]`.

Decision rule for round `t`:

1. **Round 1**
   - Play `C`.

2. **Rounds 2 to r-2**
   - Let `p = g / (n-1)`.
   - Play `C` if all of the following hold:
     - `m_{t-1} >= ceil((n-1)/2)`
     - `p >= 0.45`
     - `m_{t-1} >= m_{t-2}` whenever `t >= 3`
   - Otherwise play `D`.

3. **Opportunistic escalation**
   - If `m_{t-1} = n-1`, play `C` for the next two rounds.
   - If `m_{t-1} >= n-2` for two consecutive rounds, play `C` until a round with `m_t < n-2`.

4. **Punishment for weak cooperation**
   - If `m_{t-1} <= floor((n-1)/4)`, play `D` for the next two rounds.
   - If `m_{t-1} = 0`, play `D` for the next three rounds.

5. **Last round `r`**
   - Play `D`.

6. **Second-to-last round `r-1`**
   - Play `D` unless `m_{r-2} = n-1` and `m_{r-3} = n-1` when those rounds exist.

Operational details:

- Maintain two-step memory of observed cooperation counts.
- Treat missing history in early rounds as “no trigger.”
- If the rules conflict, apply the highest-priority rule in this order:
  1. Last-round defection
  2. Punishment rule
  3. Opportunistic escalation
  4. Default cooperation test

Compact form:

```text
if t == r: D
else if t == r-1:
    D unless recent unanimous cooperation is established
else if m_{t-1} <= floor((n-1)/4):
    D
else if m_{t-1} = 0:
    D for 3 rounds
else if m_{t-1} = n-1:
    C for 2 rounds
else if m_{t-1} >= ceil((n-1)/2) and g/(n-1) >= 0.45 and (t < 3 or m_{t-1} >= m_{t-2}):
    C
else:
    D
```

Behavioral pattern:

- Start cooperative to test the field.
- Stay cooperative only while the group shows sustained and sufficiently broad cooperation.
- Exploit high-cooperation phases aggressively.
- Exit immediately to defection when cooperation weakens.
- End by defecting to avoid being exploited in the terminal rounds.
'''

description_OPPORTUNISTIC_5 = '''
Round 1:
- Play `C`.

For each round `t = 2, 3, ..., r-1`:
- Let `q[t-1]` be the number of opponents who cooperated in the previous round.
- Define the support threshold  
  `T = ceil(n / k) - 1`.
- Maintain a one-step memory flag `trusted`:
  - `trusted = true` if `q[t-1] >= T`
  - `trusted = false` otherwise

Decision rule:
- If `trusted` is true, play `C`.
- If `trusted` is false, play `D`.

Optional stabilization rule:
- Treat support as reliable only after two consecutive rounds meeting the threshold.
- In that version, play `C` only if `q[t-1] >= T` and `q[t-2] >= T`; otherwise play `D`.

Final round `t = r`:
- Play `D`.

Edge handling:
- If `n = 2`, then `T = ceil(2 / k) - 1 = 1`; cooperate only after observing the other player cooperate.
- If `q[t-1] = 0`, switch immediately to `D` and keep defecting until the threshold is restored.
- If support alternates around the threshold, require two consecutive qualifying rounds before returning to `C`.

State update:
- After each round, record only the number of cooperating opponents in that round.
- Use the latest observed support, with no need to identify individuals or track identities.

Opportunistic mode:
- Cooperate only while the observed level of cooperation is high enough to justify staying inside a cooperative cluster.
- Defect immediately when observed support drops below threshold.
- Always defect in the last round.
'''

description_OPPORTUNISTIC_6 = '''
Round 1: cooperate.

After each round t, let m_t be the number of cooperating opponents observed in that round, and let h_t = m_t / (n - 1) be the cooperation rate among opponents.

Maintain:
- s_t = moving average of observed opponent cooperation, initialized with h_1
- b_t = best observed cooperation rate so far, i.e. max(h_1, ..., h_t)
- d_t = number of consecutive rounds with h_t below a low-cooperation threshold

Use thresholds:
- high threshold H = 0.6
- medium threshold M = 0.35
- low threshold L = 0.2

Decision rule for round t + 1:

1. Defect if the current round is the last round.

2. Cooperate if any of the following holds:
   - h_t >= H
   - s_t >= M and h_t >= M
   - b_t >= H and h_t >= M
   - t <= 2 and h_t >= M

3. Defect if any of the following holds:
   - h_t <= L for two consecutive rounds
   - s_t < L after round 3
   - h_t = 0
   - h_t < M and t > 2

4. Otherwise, mirror the recent environment:
   - cooperate if the trend is upward, meaning h_t > s_t
   - defect if the trend is downward, meaning h_t < s_t

Update rules after round t:
- s_{t+1} = 0.7 s_t + 0.3 h_t
- if h_t <= L, increment d_t; otherwise reset d_t to 0
- update b_{t+1} = max(b_t, h_t)

Emergency response:
- If opponents cooperate in all or nearly all observed rounds, cooperate continuously.
- If opponents defect in two consecutive rounds, defect until cooperation reappears.
- If cooperation oscillates, cooperate only on rounds immediately following high-cooperation observations; defect on weak or uncertain rounds.

Endgame:
- In the final two rounds, cooperate only if the current and previous observed cooperation rates are both at least M.
- Otherwise defect.

Operational summary:
- Start with cooperation to probe.
- Reward sustained cooperation quickly.
- Exploit low cooperation immediately.
- Be forgiving once after a single drop, but not after repeated drops.
- In uncertain middle states, follow the local trend rather than locking into one action.
'''

description_OPPORTUNISTIC_7 = '''
Round 1: play C.

After each round t, observe x_t = number of opponents who cooperated.

Set the cooperation threshold
h = ceil((n - 1) / k).

Maintain a trust level s ∈ {0, 1, 2}, initialized to 1.

Update after observing x_t:
- if x_t >= h, set s = min(2, s + 1)
- otherwise, set s = max(0, s - 1)

Decision rule for round t + 1:
- if t + 1 = r, play D
- else if t + 1 = r - 1:
  - play C only if s = 2 and x_t >= h
  - otherwise play D
- else:
  - play C if s = 2
  - play D otherwise

Equivalent form:
- cooperate only after two consecutive rounds with at least h cooperating opponents
- defect immediately after any round below that threshold
- once cooperation breaks, require two fresh qualifying rounds before cooperating again
- always defect in the final round
- in the penultimate round, cooperate only if cooperation is already stable enough to keep the final round profitable to harvest

If the history is empty, use the round-1 opening C, then follow the rule exactly.
'''

description_OPPORTUNISTIC_8 = '''
Initialize as a defector.

For each round t:

- Let m_{t-1} be the number of opponents who cooperated in the previous round.
- Let H = max(1, ceil((n - 1) * (1 - 1 / k)))
- Let L = min(3, t - 1)
- Let \bar m be the average of m over the last L rounds

Decision rule:
- If t = 1: play D
- If t = r: play D
- Otherwise:
  - play C if and only if all of the following hold:
    - m_{t-1} >= H
    - \bar m >= H
    - m_{t-1} >= m_{t-2} whenever t >= 3
  - otherwise play D

State update:
- After every round, store m_t.

Short-cycle exploitation rule:
- If the last two observed rounds both satisfy m >= H, cooperate once to join the cooperative cluster.
- If either of the last two observed rounds falls below H, defect immediately and keep defecting until two consecutive rounds again satisfy m >= H.

Edge handling:
- In round 2, use only m_1.
- In round 3, use m_1 and m_2 for \bar m and trend.
- If multiple opponents are silent by behavior but the observed cooperation count stays at or above H, treat that as stable cooperation and continue cooperating.
- Any downward move below H resets the cooperation phase.
'''

description_INDIVIDUALISTIC_1 = '''
Initialize with D.

For each round t = 1, 2, ..., r:

1. Let a_t be the number of opponents who cooperated in round t−1.
2. Let m_t = n−1 be the number of opponents.

Decision rule:

- If t = 1: play D.
- If t = r: play D.
- Otherwise, compute the observed cooperation rate:
  p_t = a_t / m_t

  Play C only if all of the following hold:
  - p_t ≥ 1/2
  - a_t ≥ 2
  - a_t ≥ a_{t−1}

  Otherwise play D.

Tie and edge handling:

- If the required previous observation a_{t−1} is unavailable, treat the condition a_t ≥ a_{t−1} as false.
- If n = 2, the rule simplifies to:
  - cooperate only if the single opponent cooperated in both of the two most recent observable rounds
  - otherwise defect
- If r = 2, play D in both rounds.

State update after each round:

- Record a_t.
- Set a_{t−1} ← a_t for use in the next round.

Individualistic posture:

- Default to D.
- Offer cooperation only when opposition cooperation is already strong and stable.
- Never initiate cooperation on weak, mixed, or declining opponent cooperation.
- Stop cooperating immediately if observed cooperation falls, and always defect in the final round.
'''

description_INDIVIDUALISTIC_2 = '''
State variables:
- `t` = current round
- `m[t-1]` = number of opponents who cooperated in the previous round
- `E[t]` = exponentially weighted estimate of opponent cooperation rate, initialized to `0`
- `cooldown` = integer, initialized to `0`

Parameters:
- `τ = 1 - k / (2n)`
- `α = 0.6` for the exponential update
- `drop_trigger = 2` opponent cooperators below the previous-round count

Decision rule each round `t`:

1. **Endgame rule**
   - If `t = r`, play `D`.
   - If `r = 2`, play `D` in both rounds.

2. **Opening rule**
   - If `t = 1`, play `D`.

3. **Update after each observed round**
   - Let `x = m[t-1] / (n-1)`.
   - Update `E[t] = α * E[t-1] + (1 - α) * x`.
   - If `m[t-1] <= m[t-2] - drop_trigger`, set `cooldown = 2`.
   - If `cooldown > 0`, decrement it by 1 at the start of the next round.

4. **Main rule for rounds `2 <= t <= r-1`**
   - Play `C` only if all of the following hold:
     - `cooldown = 0`
     - `E[t] >= τ`
     - `m[t-1] >= ceil(τ * (n-1))`
   - Otherwise play `D`.

5. **Tie-break and edge handling**
   - If `n = 2`, treat `m[t-1]` as either `0` or `1` and apply the same rule.
   - If the history is too short to compute a two-round drop, ignore the drop test.
   - If `E[t]` is exactly on the threshold, play `D`.

Operational interpretation:
- Start by defecting.
- Continue defecting until the observed cooperation level is consistently high.
- Cooperate only while the cooperation environment is stable and strong enough.
- If cooperation collapses, defect immediately and stay in `cooldown` for the next two rounds.
- Defect in the final round regardless of history.

Compact pseudocode:

```text
if t == 1 or t == r or r == 2:
    play D
else:
    x = m[t-1] / (n-1)
    E = 0.6 * E + 0.4 * x

    if t >= 3 and m[t-1] <= m[t-2] - 2:
        cooldown = 2

    if cooldown > 0:
        cooldown -= 1
        play D
    else if E >= 1 - k/(2n) and m[t-1] >= ceil((1 - k/(2n)) * (n-1)):
        play C
    else:
        play D
```
'''

description_INDIVIDUALISTIC_3 = '''
Initialize:
- `memory = []`  // observed counts of cooperating opponents in prior rounds
- `mode = "defect-first"`  

For round `t = 1`:
- Play `D`

For round `t > 1`:
- Let `q = memory[t-1]` be the number of cooperating opponents in the previous round.
- Let `a = q / (n - 1)` be the previous-round cooperation rate among opponents.
- Let `A3` be the average opponent cooperation rate over the last up to 3 rounds:
  - `A3 = mean(memory[s] / (n - 1) for s in max(1, t-3) .. t-1)`

Decision rule:
1. If `t >= r - 1`, play `D`.
2. Else if `a >= 0.75` and `A3 >= 0.66`, play `C`.
3. Else if `a >= 0.85` and `A3 >= 0.75`, play `C` even if only one of the last three rounds qualifies.
4. Else play `D`.

Update rule after each round:
- Append the observed opponent cooperation count to `memory`.

Persistent adjustment:
- If you ever play `C` and the next round’s opponent cooperation rate drops by at least `0.25` compared with the previous round, switch to `D` for the next 2 rounds.
- If the 3-round average opponent cooperation rate later recovers to at least `0.75`, return to the main decision rule.

Edge cases:
- If `n = 2`, replace `0.75` with `1.0` and `0.66` with `1.0`.
- If fewer than 3 prior rounds exist, compute `A3` using all available prior rounds.
- On the final two rounds, always play `D`.
- If no prior rounds are available besides round 1, always start with `D`.
'''

description_INDIVIDUALISTIC_4 = '''
Maintain three internal variables: `last_opp_coop`, `coop_rate_ema`, and `mode`, where `mode ∈ {guarded, testing, harvesting}`.

Set:
- `high = ceil(0.7 * (n - 1))`
- `low = floor(0.4 * (n - 1))`

Round 1:
- Play `D`.

After each round `t > 1`, let `m` be the number of opponents who cooperated in round `t-1`, and let `p = m / (n - 1)`.
- Update `coop_rate_ema = 0.6 * coop_rate_ema + 0.4 * p`.

Decision rule for round `t`:
1. If `t = r`, play `D`.
2. Else if `m >= high` and `coop_rate_ema >= 0.65`:
   - If `mode = guarded`, switch to `testing` and play `C`.
   - If `mode = testing` and `m >= last_opp_coop`, switch to `harvesting` and play `C`.
   - If `mode = harvesting`, play `C`.
3. Else if `m <= low`:
   - Set `mode = guarded`.
   - Play `D`.
4. Else:
   - Play `D` unless `mode = harvesting`, in which case keep playing `C` only while `m >= high`.

Update `last_opp_coop = m` after every round.

Fallbacks and edge cases:
- If `n = 2`, replace `high` with `1` and `low` with `0`.
- If cooperation drops by any amount after you are in `harvesting`, immediately return to `guarded` and defect until the cooperation count recovers to `high` again.
- If only one round remains, always defect.
- If the observed cooperation count is exactly on the boundary, treat it as cooperation only when it is not below the previous round’s count.

Behavioral principle:
- Start by protecting yourself.
- Cooperate only after cooperation is already broad and stable.
- Stop cooperating at the first sign of weakening support.
- Never try to “rescue” a collapsing group with unilateral cooperation.
'''

description_INDIVIDUALISTIC_5 = '''
Let \(x_t\) be the number of other players who cooperated in round \(t\), and let

\[
m_t=\frac{x_t}{n-1}
\]

be the observed cooperation rate among opponents.

Maintain a smoothed estimate of opponent cooperation:

\[
S_t=\alpha m_t+(1-\alpha)S_{t-1}, \quad \alpha\in[0.3,0.7]
\]

with \(S_0=0\).

Decision rule for round \(t\):

1. If \(t=r\), play \(D\).
2. Otherwise, play \(C\) if and only if all three conditions hold:
   - \(S_{t-1}\ge \theta_t\)
   - the last observed round was not a sharp collapse, i.e. \(m_{t-1}\ge \theta_t-\delta\)
   - your own recent average payoff from cooperating, compared over the last few rounds in which you played \(C\), is not below your payoff from defecting by more than a small margin \(\varepsilon\)

3. In all other cases, play \(D\).

Use thresholds that tighten over time:

\[
\theta_t=\theta_0+\lambda\frac{t-1}{r-1}
\]

with a practical choice:
- \(\theta_0=0.55\)
- \(\lambda=0.15\)
- \(\delta=0.10\)
- \(\varepsilon=0\) or a very small positive value

Operational version:

- Round 1: play \(D\).
- Rounds \(2\) through \(r-1\):
  - If the previous round had at least about half the opponents cooperating, and cooperation has stayed stable across the recent history, play \(C\).
  - If cooperation among opponents falls below the threshold, switch to \(D\).
  - If cooperation later recovers and stays above the threshold for two consecutive rounds, return to \(C\).
- Round \(r\): play \(D\) unconditionally.

Hysteresis rule to avoid oscillation:

- Enter cooperation only when \(S_{t-1}\ge \theta_t\).
- Exit cooperation immediately when \(S_{t-1}<\theta_t-\delta\).

Memory update:

- After each round, update \(S_t\) from the observed number of cooperating opponents.
- Keep separate running averages of your own payoffs conditional on your own action:
  - \(\bar\pi_C\): average payoff in rounds where you played \(C\)
  - \(\bar\pi_D\): average payoff in rounds where you played \(D\)

Exploration adjustment:

- If after several rounds \( \bar\pi_C \le \bar\pi_D \), raise the cooperation threshold by a small increment.
- If \( \bar\pi_C > \bar\pi_D \) and opponent cooperation has been stable, lower the threshold slightly, but never below \(0.5\).

Tie-breaking:

- On any borderline case where the rule is exactly indifferent, play \(D\).

Compact pseudocode:

```text
S = 0
state = D

for t in 1..r:
    if t == r:
        action = D
    else if t == 1:
        action = D
    else:
        theta = 0.55 + 0.15*(t-1)/(r-1)
        if state == C:
            if S < theta - 0.10:
                action = D
            else:
                action = C
        else:
            if S >= theta and last_m >= theta - 0.10 and coop_payoff_not_worse():
                action = C
            else:
                action = D

    observe x_t
    m = x_t / (n-1)
    S = alpha*m + (1-alpha)*S
    update payoff statistics
    state = action
```

Behavioral profile:
- Starts cautiously.
- Cooperates only when the opponent population is already showing sustained cooperation.
- Defects immediately when cooperation weakens.
- Never gives away the final-round advantage.
- Uses only aggregate history, not identities, so it remains fully individualistic.
'''

description_INDIVIDUALISTIC_6 = '''
Maintain a personal cooperation target and update it from observed aggregate cooperation.

Decision rule

- Let `m_t` be the number of opponents who cooperated in round `t`.
- Let `N = n - 1`.
- Let `q_t = m_t / N`, the observed opponent cooperation rate.

Initialize

- Set `x_1 = C` in round 1.

Update after each round

- Keep a running estimate of opponent cooperation:
  - `Q_t = (1 - λ) Q_{t-1} + λ q_t`
  - with `Q_0 = 0.5` and `λ = 0.35`
- Compute your personal cooperation threshold:
  - `τ_t = clip(0.5 + 0.4(0.5 - Q_t), 0.15, 0.85)`
- Compute persistence:
  - `s_t =` number of consecutive rounds up to `t` in which `q` has stayed within `±0.10` of `Q_t`
- Set next-round action:
  - if `q_t >= τ_t`, play `C`
  - otherwise, play `D`
  - if `s_t >= 3`, bias one step toward stability:
    - if you played `D` in the current round and `q_t >= τ_t - 0.05`, play `C`
    - if you played `C` in the current round and `q_t <= τ_t + 0.05`, keep `C`

Round-by-round policy

1. First round:
   - Play `C`

2. Early rounds `t = 2, 3`:
   - Use the same threshold rule, but update `Q_t` with `λ = 0.50` to react faster

3. Middle rounds:
   - Use the standard update and threshold rule exactly as stated

4. Final round `t = r`:
   - Play `C` if `q_{r-1} >= 0.5`
   - Otherwise play `D`

Edge cases

- If `n = 2`, replace `q_t` with the single opponent’s behavior directly.
- If no opponent cooperated in a round, set `q_t = 0`.
- If all opponents cooperated, set `q_t = 1`.
- If your computed threshold falls outside `[0.15, 0.85]`, clamp it to that interval.
- If two consecutive rounds show the same `q_t` and it is exactly on the threshold boundary, keep your previous action.

Individualistic posture

- Start cooperative.
- Cooperate only when observed opponent cooperation is high enough to justify it by your own threshold.
- Defect immediately when observed cooperation drops below your threshold.
- Never mirror a specific opponent, never attempt pairwise reciprocity, and never rely on any identity-based pattern.
- Treat the history only as aggregate evidence for your own next move.
'''

description_INDIVIDUALISTIC_7 = '''
Use a personal best-response rule based on the observed cooperation count, with a short probing phase and a moving threshold.

Let `m_t` be the number of other players who cooperated in round `t`.

State variables:
- `s`: score of recent cooperation among others
- `L`: length of the observation window, set to `min(3, r-1)`
- `H`: cooperation threshold, set to `ceil((n-1)/k)` if you want a strict threshold, and `ceil((n-1)/(k+1))` if you want a slightly more permissive threshold
- `streak`: number of consecutive rounds in which `m_t >= H`

Decision rule:

1. First round:
   - Play `D`.

2. Rounds 2 through `L+1`:
   - Continue to play `D`.
   - Record `m_t` each round.

3. After the probing phase:
   - Compute the recent average cooperation among others:
     `avg = (m_{t-L} + ... + m_{t-1}) / L`
   - Cooperate in round `t` if and only if:
     - `avg >= H`, and
     - `m_{t-1} >= H`, and
     - the last two observed rounds did not show a downward break below `H`.

4. Otherwise:
   - Play `D`.

5. Update rule after each round:
   - If `m_t >= H`, increment `streak`.
   - If `m_t < H`, reset `streak = 0`.

6. Strong reset rule:
   - If `m_t` falls below `H` for two consecutive rounds, play `D` for the next two rounds before reconsidering cooperation.

7. Last round:
   - Play `D`.

Compact pseudocode:

```text
if t == 1:
    play D
else if t <= min(3, r-1) + 1:
    play D
else if t == r:
    play D
else:
    avg = mean(m[t-3], m[t-2], m[t-1]) over available rounds
    if avg >= H and m[t-1] >= H and m[t-2] >= H:
        play C
    else:
        play D
```

Individualistic interpretation:
- Treat cooperation as a selective action used only when the observed environment already supports it.
- Default to defection when the recent history does not clearly justify cooperation.
- Never commit to unconditional cooperation.
- Never retaliate emotionally; only respond to the aggregate behavior pattern.
- End by defecting in the final round.
'''

description_INDIVIDUALISTIC_8 = '''
Start with D.

Maintain two state variables:
- `s` = current cooperation score, initialized to 0
- `mode` ∈ {explore, exploit, punish}, initialized to `explore`

After each round, let `x` be the number of opponents who cooperated in that round, so `0 ≤ x ≤ n-1`.

Update rules:
- If you played C and `x` is at least `ceil((n-1)/2)`, increase `s` by 1.
- If you played D and `x` is at most `floor((n-1)/2) - 1`, decrease `s` by 1.
- Otherwise leave `s` unchanged.
- Clamp `s` to the interval `[-3, 3]`.

Decision rule for round `t`:

1. **First round**
   - Play D.

2. **Exploration phase**
   - If `t ≤ min(3, r)` and `mode = explore`:
     - Play C in round 2 if `x` from round 1 is at least `ceil((n-1)/2)`.
     - Otherwise keep playing D.
   - More generally, in the first `min(3, r)` rounds, alternate:
     - Round 1: D
     - Round 2: C if the previous round had at least half the opponents cooperating; otherwise D
     - Round 3: repeat the same choice as round 2

3. **Main policy after exploration**
   - Compute the recent cooperation rate over the last up to 3 rounds:
     - `m = average of x/(n-1)` over the last up to 3 rounds
   - Cooperate iff all of the following hold:
     - `m ≥ 1/2`
     - `s ≥ 0`
     - the previous round had at least `ceil((n-1)/2)` cooperating opponents
   - Otherwise defect.

4. **Punishment rule**
   - If in any round fewer than `ceil((n-1)/3)` opponents cooperated, set `mode = punish` for the next 2 rounds.
   - While in punish mode, play D regardless of other conditions.
   - Exit punish mode immediately after 2 rounds, then return to the main policy.

5. **Recovery rule**
   - If you are in punish mode and the observed cooperation count rises to at least `ceil((n-1)/2)`, exit punish mode after that round and set `s = 0`.

6. **Endgame rule**
   - In the final 2 rounds, play D unless both of these hold:
     - the previous round had at least `ceil((n-1)/2)` cooperating opponents
     - `s ≥ 2`
   - In that case, continue to cooperate.

Individualistic principle:
- Cooperate only when the observed environment is already cooperative and stable.
- Defect immediately when cooperation drops below a majority threshold.
- Never depend on identity, reciprocity, or goodwill; only on aggregate behavior, recent history, and your own state.
- Prefer self-protection in uncertain or deteriorating conditions, and require repeated cooperative evidence before contributing.
'''
