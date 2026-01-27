"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: OpenAI
- Model: gpt-5-mini
"""


description_COLLECTIVE_1 = '''
Strategy name: Thresholded Reciprocal with Individual Reputation and Forgiveness (TRIF)

Principles (collective mindset)
- Aim to sustain high group contributions by rewarding rounds with substantial cooperation and withholding cooperation when many players free-ride.
- Be lenient to one-off mistakes but punish persistent defectors enough to make cooperation attractive in repeated interaction.
- Use only observed history and game parameters (n, r, k); do not assume coordination or shared norms.

Parameters (derived from game parameters; fixed at start)
- Lookback window L = min(5, r). (Use up to five recent rounds to estimate behavior; smaller if game is short.)
- Majority threshold M = ceil(n/2). (Treat a majority cooperating as evidence of a cooperative norm.)
- Tolerated slip D_allow = max(1, floor(n/8)). (Small number of simultaneous defectors tolerated without group punishment.)
- Punishment length P = 2 (defect for P rounds in response to observed breakdowns).
- Forgiveness requirement S = 2 (require S consecutive rounds meeting cooperation criteria to return to full trust).
- Endgame caution window E = min(2, r) (apply special rules in the last E rounds).

State I maintain
- For each player j (including myself), a running cooperation score s_j initialized at 1.0. After each round, update s_j by exponential smoothing: s_j <- 0.6*s_j + 0.4*a_j where a_j is 1 if j cooperated this round, 0 if defected. (This gives more weight to recent behavior while keeping memory.)
- A local punishment counter punish_count (initially 0) indicating how many rounds I will defect as punishment before reconsidering.
- A consecutive-good-rounds counter good_streak (initially 0).

Action rules (played each round t from 1..r)
1. First round:
   - Cooperate. (Begin by signaling willingness to cooperate.)

2. After each observed round (update s_j and history):
   - Compute C_prev = number of players who cooperated in the immediately preceding round.
   - Compute avg_other_score = (sum_{j != me} s_j) / (n-1).
   - Identify persistent defectors: any j with s_j < 0.25 is treated as low-reputation.

3. Punishment handling:
   - If punish_count > 0: play D this round and decrement punish_count by 1. (Carry out the punishment phase.)

4. Otherwise (not currently punishing), decide whether to C or D this round:
   A. Endgame special-case (round t in last E rounds):
      - If t == r (final round): play D. (Default safe choice in a finite endgame where backward induction can unravel cooperation.)
      - If t == r-1 and E >= 2: play C only if both (i) C_prev == n (everyone cooperated last round) OR (ii) avg_other_score >= 0.9 and no persistent defectors; otherwise play D. (Be cautious near the end but allow a final cooperative payoff if strong evidence of mutual cooperation exists.)
   B. Normal rounds (not in punishment, not final cautious moments):
      - If C_prev >= n - D_allow:
          - Many cooperated last round (at most D_allow defectors): play C. Rationale: tolerate a small number of slips to avoid collapse from noise or isolated free-riders.
      - Else if C_prev >= M:
          - A majority cooperated last round: play C. (Support and stabilize majority cooperation.)
      - Else:
          - Play D this round, and set punish_count = P. Also reset good_streak = 0. (Respond to clear breakdowns by a brief, collective withholding of cooperation to signal cost of defection.)

5. Forgiveness and recovery:
   - After each round where I played C and the criteria in step 4 would have produced C (i.e., group shows enough cooperation), increment good_streak by 1. If good_streak >= S, reset punish_count = 0 and gradually restore trust (smoothing continues).
   - If a persistent defector (s_j < 0.25) returns to cooperation over L recent rounds (s_j rises above 0.4), treat them as rehabilitated; allow cooperation under the normal rules.

6. Handling single/double defects during otherwise cooperative groups:
   - If exactly one (or up to D_allow) player defected while C_prev >= n - D_allow, do NOT trigger punishment phase against the whole group; instead decrease my trust score for that individual (via the smoothing update) but continue cooperating. If that individual defects repeatedly (s_j falls under 0.25), normal punishment logic will be triggered as group cooperation falls.

Why this is adaptive and robust
- Starts cooperative to give mutual cooperation a chance.
- Uses simple, observable statistics (round cooperators and per-player reputation) so it adapts to many strategy types (unconditional cooperators, unconditional defectors, conditional cooperators, noisy players).
- Tolerates occasional slips and noise (prevents cascade collapse from single errors) but applies short, clear punishments for persistent breakdowns so that sustained free-riding is costly.
- Forgives after evidence of recovery so cooperative equilibria can re-emerge.
- Uses cautious behavior in the last rounds to limit exploitation when future punishment is impossible, while still allowing final cooperation if strong evidence of mutual cooperation exists.
- All rules depend only on n, r, k (via parameter choices above) and observed history; no communication or coordination is assumed.

Summary pseudocode (informal)
- Initialize s_j = 1 for all j, punish_count = 0, good_streak = 0.
- Round 1: play C.
- For each subsequent round:
  - Update s_j = 0.6*s_j + 0.4*a_j for each j after observing last round.
  - If punish_count > 0: play D; punish_count--.
  - Else apply endgame special-case if in last E rounds (see step 4.A).
  - Else compute C_prev, avg_other_score:
    - If C_prev >= n - D_allow or C_prev >= M: play C and increment good_streak (reset punish_count if good_streak >= S).
    - Else: play D; set punish_count = P; good_streak = 0.
- Continuously rehabilitate low s_j when they show recent cooperation.

This keeps the focus on maximizing collective welfare by supporting cooperative majorities, punishing persistent free-riding, and forgiving when cooperation returns.
'''

description_COLLECTIVE_2 = '''
Adaptive Collective Win‑Stay / Lose‑Shift (AC‑WSLS)

Goal: sustain high group cooperation while avoiding long runs of exploitation. The rule set uses only the game parameters (n, r, k) and observed history (every player’s past actions and payoffs). It is deterministic, easy to compute, forgiving, and biased slightly toward cooperation to support collective welfare.

Definitions used by the rule:
- In round t, denote my action last round by a_last ∈ {C,D} and my realized payoff last round by π_last.
- Let S_last = total contributions by all players in the previous round (an integer between 0 and n).
- Compute the one‑shot counterfactual payoff I would have received last round had I played the opposite action while everyone else’s actions remained the same. (This is directly computable from S_last and a_last.)
- “Win” means π_last ≥ counterfactual payoff (I did at least as well as I would have by switching); “Lose” means π_last < counterfactual payoff.

Core decision rule (applied each round except the last round; last round is handled below):
1. First round: cooperate (play C). This signals willingness to support the public good.
2. For rounds t = 2 .. r−1:
   - If Win (I did at least as well as by switching): repeat my previous action (win‑stay).
   - If Lose (I would have been better off switching): switch my action this round (lose‑shift).
   - Tie‑break: when π_last equals the counterfactual exactly, choose C (a small cooperative bias to support collective welfare).
3. Forgiveness and recovery are automatic in the WSLS rule: after a punishment-defection that yields a poor payoff, the rule switches back to cooperation; after cooperation that yields a good payoff, it continues. This produces short, targeted punishment instead of permanent collapse.

Additional collective safeguards (still depends only on observed history):
- If in the previous round S_last = n (everybody cooperated), always play C this round (reward full cooperation).
- If my own history shows I have been defecting for many rounds because I repeatedly lost when cooperating, the WSLS dynamics will attempt cooperation again when payoff conditions indicate it could help; no extra special-case needed.

Last round and endgame handling:
- In the final round t = r: defect (play D). Because there is no future to enforce reciprocity, defect is the safe one‑shot best response. (Do not exploit earlier rounds by defecting early because WSLS sustains cooperation until exploitation occurs; only the final round is an unavoidable endgame defection.)
- If you prefer a slightly more optimistic endgame in small r settings, an alternative safe variant is: if a unanimous cooperative streak (S_last = n) continued through round r−1, you may play C in round r; otherwise play D. (Either variant depends only on observed history; the default is to defect in round r.)

Why this is collective and robust:
- WSLS preserves cooperation when it is mutually profitable: if cooperating last round led to as-good-or-better payoff than defecting, it continues cooperating — this stabilizes mutually beneficial cooperation among many cooperators.
- It punishes exploitation quickly but briefly: when cooperating is exploited (you would have done better by defecting), you switch and thereby discourage persistent free‑riding without causing permanent collapse.
- It is forgiving: a short switch back to cooperation is automatic when the payoff environment improves, so occasional mistakes or noise from others do not lock you into permanent defection.
- The tie‑break bias toward cooperation supports group gains when the data are ambiguous.
- The final‑round defection avoids being systematically exploited in the terminal period.

Implementation notes (all computable from parameters and history):
- Counterfactual payoff calculation: from S_last and a_last, compute the payoff you would have obtained had your last action been flipped, holding others fixed (simple arithmetic using the payoff formula provided).
- No external coordination or communication is required. The rule uses only observed actions and payoffs.
- This strategy is fully specified for every round by the history and game length r; there are no hidden parameters or randomization (except the optional optimistic final‑round variant above).

Summary (short): Start by cooperating. In each nonfinal round, compare your actual payoff last round to the payoff you would have obtained by switching your last action; if you did at least as well, repeat the same action (win‑stay); if you would have done better by switching, switch now (lose‑shift). Tie → cooperate. In the final round, defect. This rule promotes stable collective cooperation, punishes exploitation briefly, and forgives to recover cooperation.
'''

description_COLLECTIVE_3 = '''
Name: Collective Conditional Cooperator with Proportional Retaliation and Forgiveness (CCCPR-F)

Goal: maximize long-run group payoff by sustaining cooperation when others are willing, while avoiding long or costly retaliation when exploited. The rule set is deterministic, uses only game parameters (n, r, k) and observed history (each player’s past C/D), and is adaptive to a wide range of opponent behaviors.

Derived constants (computed once at start):
- Memory window W = min(10, max(1, floor(r/5))) — use recent history but lengthen for longer games.
- Cooperation threshold τ:
  - if k/n >= 0.75 then τ = 0.45 (be more lenient when group benefit is large)
  - else if k/n >= 0.5 then τ = 0.50
  - else τ = 0.60 (be stricter when collective benefit is smaller)
- Small-noise tolerance ε = 0.20 (forgive occasional single-round slips)
- Base punishment length P_base = 2 rounds; maximum punishment P_max = min(4, max(1, floor(r/10)+1)).

State maintained (update each round from observed history):
- For every other player j, S_j = fraction of rounds (over the most recent min(W, t-1) rounds) in which j contributed.
- G = average of S_j over all j ≠ me (group cooperation rate among others in the memory window).
- last-round defect fraction f_last = (# of other players who chose D in previous round) / (n-1).
- A (possibly empty) set PunishTargets with an associated integer PunishUntilRound for the current active group punishment (if any). PunishTargets are identified when deliberate, repeated defection is detected (see below).

Decision rule for round t:

1. Final-round rule
   - If t == r (the last round), play D. (Backward induction: last-round defection is dominant.)

2. First-round rule
   - If t == 1, play C (start nice to give cooperation a chance).

3. If currently inside an active group punishment (current round ≤ PunishUntilRound):
   - Play D (continue the calibrated punishment).
   - After playing, re-evaluate S_j and G. If G has recovered above τ (others collectively resumed cooperation), clear PunishTargets and stop punishment immediately; return to cooperative evaluation next round.

4. Otherwise (normal evaluation, t in 2..r-1 and not in punishment):
   - Compute S_j and G as above and f_last.
   - If G ≥ τ: play C (group is sufficiently cooperative).
   - Else (G < τ):
     a. If f_last == 0: play C (no recent defections — allow recovery).
     b. Else if 0 < f_last ≤ ε: play C (forgive small slips/noise).
     c. Else (f_last > ε): trigger a calibrated, limited punishment:
        - Let m = number of other players with S_j ≤ 0.30 (chronic defectors in memory window).
        - Set punishment length P = min(P_max, P_base + floor(m/2)). (Longer if there are multiple persistent defectors, but capped.)
        - Set PunishTargets = {all players who defected in the most recent round or who have S_j ≤ 0.30}.
        - Set PunishUntilRound = current round + P - 1.
        - Play D this round (initiate punishment).
   - After playing, continue to next round and re-evaluate (punishment may be stopped early if collective cooperation returns to ≥ τ).

Additional notes for robustness and collective orientation:
- Punishment is short and proportional: we punish long enough to deter repeated exploitation but never indefinitely. This limits cost to the group and encourages return to cooperation.
- Punishment targets are identified by recent, repeated defection (low S_j) and recent defections; the rule avoids permanent ostracism for a single slip.
- The strategy is forgiving: small or isolated defections are tolerated to accommodate strategic experimentation or occasional errors; the strategy resumes cooperation as soon as others’ cooperative behavior recovers (G ≥ τ).
- The strategy is collective: it prioritizes restoring and maintaining high group cooperation (cooperating whenever the group is sufficiently cooperative), and when necessary imposes limited, proportionate costs on defectors rather than continuous mutual defection.
- Endgame behavior: because the one-shot incentive is to defect in the last round, CCCPR-F defects in round r. This preserves robustness to pure defectors in the final move while still attempting to sustain cooperation earlier.

Summary of intuitive behavior:
- Start cooperative to signal willingness.
- Cooperate whenever the recent average cooperation of others is at or above a threshold tuned by k and n.
- Forgive occasional or rare defections.
- If defections are nontrivial, retaliate by defecting for a short, proportional number of rounds targeted at the recent/persistent defectors.
- Stop punishing as soon as group cooperation is restored.
- Defect in the last round.

This procedure is transparent, parameterized only by (n, r, k) and observable actions, encourages collective welfare, and is robust: it resists exploitation by persistent defectors while minimizing unnecessary costs from long punishments and tolerating occasional deviations.
'''

description_COLLECTIVE_4 = '''
Strategy name: Adaptive Collective Conditional Cooperation (ACCC)

High-level aim
- Promote and maintain high group contributions whenever others are cooperating, while defending the group against sustained free-riding with short, predictable punishments and prompt forgiveness. The strategy is collective in intent: it sacrifices short-term private payoff occasionally to sustain long-run group gains, but it avoids being a permanent sucker by responding to persistent defection.

State and obvious variables used
- n, r, k (game parameters).
- t = current round number (1..r).
- History: for each past round s < t we observe each player’s contribution (0/1).
- W = min(4, max(1, r-1)): look-back window in rounds used for short-term statistics.
- Remaining rounds left = R = r − t + 1 (including current decision for round t).
- A cooperative state flag (either “Cooperate-mode” or “Punish-mode”).
- A Punishment counter when in Punish-mode.

Initialization and edge cases
1. If r = 1 (single-shot): defect (D). No future to sustain cooperation.
2. Otherwise (r ≥ 2): start in Cooperate-mode and play C in round 1 (signal willingness to cooperate).
3. Final round: always defect (D) in round r (no future to enforce cooperation). If r is 2, follow this rule (cooperate round 1, defect round 2).

Core decision rules (for rounds t with 1 <= t < r)
I. Compute recent cooperation statistics from history:
   - For each of the last up to W rounds (s = max(1,t−W) … t−1), compute fraction of players who contributed in that round (fraction includes all players except that this is just observed past data).
   - Let RecentFraction = average of those fractions. If there is no past round (t=1) treat RecentFraction as 1.0 (encouraging first-round cooperation).

II. Cooperate-mode behavior
   - Default action while in Cooperate-mode: contribute (C).
   - But if RecentFraction falls below a tolerance threshold T_low, switch to Punish-mode and begin punishment (see below).
   - T_low = 0.5 (i.e., if on average fewer than half the group has been contributing recently, the collective is failing enough to justify punishment).
   - Small dip tolerance: to avoid overreacting to one noisy round, require RecentFraction < T_low (averaged over up to W rounds) before punishing.

III. Punish-mode behavior
   - Upon entering Punish-mode at the start of round t:
     - Set PunishmentLength P = min(3, max(1, floor(R/4))). (Short, finite punishment scaled down if few rounds remain.)
     - Defect (D) for the next P rounds (including the current round).
   - After a punishment block completes, do not immediately return to unconditional cooperation. Instead require rehabilitation:
     - Observe the next H consecutive rounds (H = min(2, max(1, floor(W/2)))).
     - If, during those H rounds, the average fraction of contributors in the group (RecentFraction over those rounds) is >= T_high, then switch back to Cooperate-mode and resume contributing.
     - Otherwise, re-enter Punish-mode for another P' rounds, where P' = min(P+1, R_remaining/2 rounded down) — i.e., escalate modestly but bounded by remaining rounds.
   - T_high = 0.8 (high bar for forgiveness: the group must show clear return to cooperation).

IV. Ongoing adaptation and proportionality
   - Punishment length and escalation are deliberately short and bounded to be credible but not ruinous. Punishments are group-level (we withhold contribution) rather than trying to single out players, because only group-level withholding is available as credible leverage.
   - If the group returns to consistent cooperation (RecentFraction >= T_high for H consecutive rounds), stop punishing and resume contribution to rebuild group welfare.
   - If defection is only occasional or noisy (one or two defectors in a window), the averaging and thresholds avoid triggering punishment. This gives forgiveness for mistakes and robustness to noisy opponents.

V. Last-round and endgame adaptation
   - Round r: always defect (D).
   - If only a very small number of rounds remain (R <= 2), reduce punishment lengths to avoid wasting the last rounds on mutual mutual harm: set P = 1 in such cases and require H = 1 for rehabilitation.
   - If most opponents are known to be unconditional cooperators (they contributed in every observed round so far), remain in Cooperate-mode even late in the game until r−1, but still defect in round r.

Additional practical points (collective mindset)
- The strategy sacrifices one token occasionally to rebuild long-term cooperation, but it never pays out perpetual tolerance: repeated group-level defection triggers predictable short punishments that deter exploitation.
- The strategy is forgiving and noise-tolerant: it reacts to sustained patterns, not single mistakes.
- It is transparent in spirit: contributions signal willingness to cooperate; sustained coordinated defection by others is met by short, bounded group-level withholding, then a clear rule for rehabilitation so cooperation can resume.
- Against pure defectors it will stop being exploited: after detecting persistent low RecentFraction it will withhold contribution enough to reduce exploiter gains.
- Against cooperative strategies it achieves near-full cooperation except for the final-round defection.

Summary in one paragraph
Start by cooperating to signal collectiveness. Measure the recent average fraction of contributors over a short window. Cooperate as long as that recent average stays above 50%. If the recent average falls below 50%, switch to a short, bounded punishment phase of defection (typically 1–3 rounds, shorter near the end of the game). After punishment require a clear rebound (high recent contribution rate, e.g. ≥ 80% for a short rehabilitation window) before returning to cooperation. Always defect in the final round. Use short, proportionate punishments and prompt forgiveness so the group can quickly return to mutually beneficial cooperation while avoiding long-term exploitation.
'''

description_COLLECTIVE_5 = '''
Collective conditional-cooperation with graduated punishment and forgiveness

Principles (collective mindset)
- Prefer mutual contributions whenever doing so is plausible — that maximizes group welfare and tends to produce higher long-run payoffs for everyone.
- Be reciprocal: reward rounds that look cooperative, punish rounds that show exploitation, but avoid permanent collapse by forgiving and probing for recovery.
- Be cautious in the final round(s) where future punishments are not possible.

Setup (computed from known parameters n, k, r)
- Majority threshold M = ceil(n / 2). Use a simple majority as the signal that the group is broadly cooperating.
- Short punishment cap P_max = min(4, max(1, floor(r / 10))). (Punishments are short and proportional to game length.)
- Resignation window W = min(r, 6). Resignation threshold R_th = 0.30 (if cooperation has been very low recently, stop trying to restore cooperation except for occasional probes).
- Probe interval L = max(4, floor(r / 6)). When “resigned”, perform a cooperation probe every L rounds to test whether the group has begun cooperating again.

State variables (maintain in memory)
- mode ∈ {cooperative, punishing, resigned}
- punishment_timer (integer ≥ 0)
- last_punish_round (round index when punishment started; used only for bookkeeping)

Decision rules (applied each round t = 1..r)
1) First round (t = 1)
- Cooperate (contribute 1). Start in mode = cooperative, punishment_timer = 0.

2) Final round (t = r)
- Defect (contribute 0). There is no future to enforce cooperation reliably; defecting is individually dominant in the last stage.

3) Otherwise (1 < t < r):
A. If mode == resigned:
  - If this round is a probe round (i.e., (t mod L) == 0): cooperate this round to test whether others will respond.
  - Otherwise defect.
  - After each round while resigned, check the cooperation rate over the last W rounds; if that rate ≥ M/n (i.e., majority in the recent window), switch mode → cooperative, reset punishment_timer = 0.

B. If punishment_timer > 0 (we are in an ongoing punishment phase):
  - Defect this round.
  - Decrement punishment_timer by 1.
  - After decrementing, if punishment_timer == 0 then: examine cooperation in the most recent two rounds (the last round before the end of punishment and the round just ended). If majority cooperation appears (≥ M) in that small post-punishment window, switch mode → cooperative. If not, set punishment_timer = min(P_max, 1 + number_of_defectors_in_most_recent_round) to continue a short, proportionate punishment (this implements graduated escalation with a cap).
  - Additionally, if over the last W rounds the fraction of cooperators (count of cooperators per round averaged) is < R_th, switch to mode = resigned.

C. If mode == cooperative and punishment_timer == 0:
  - Look at the previous round (t-1). Let c_last = number of players who cooperated in t-1 (0..n).
  - If c_last == n (unanimous cooperation in the last round): cooperate.
  - Else if c_last ≥ M (a majority cooperated in the last round): cooperate (be lenient — reward near-cooperation to help restore full cooperation).
  - Else (strict minority cooperated; evidence of exploitation):
    - Enter punishment: set mode → punishing and set punishment_timer = min(P_max, 1 + (n - c_last)). Immediately defect this round (start the punishment).
    - If after entering punishment you observe that the recent cooperation rate over the last W rounds < R_th, switch to mode → resigned (see above).

4) Forgiveness and recovery (general)
- Punishments are short and proportional to the observed level of defection; they are intended to deter free-riding but not to destroy cooperation forever.
- After a punishment phase ends, the strategy returns to cooperation as soon as there is clear evidence (majority) that others are cooperating again. This prevents long vendettas and encourages re-establishment of public-good contributions.
- If the group remains largely uncooperative for a sustained short window (W rounds), go into resigned mode (stop trying to re-establish cooperation except for occasional probes). This prevents repeated costly punishments against persistent defectors and preserves our own payoff when the group clearly will not cooperate.

Design rationale and robustness
- Starting cooperatively signals willingness to form a collective outcome and benefits unconditional cooperators and conditional cooperators.
- Using a majority threshold M makes the rule robust to noise and small deviations and avoids overreacting to one-off mistakes or random behavior by a single player.
- Graduated punishment proportional to how many defected avoids overpunishing and makes retaliation interpretable by others (they can infer why we punished and how long).
- Forgiveness (short punishments, immediate return on evidence of majority cooperation) prevents collapse and supports recovery of cooperation.
- Resigned mode avoids wasting payoff on repeated punishments in hopeless groups but still probes occasionally to capture opportunities if the group changes behavior.
- Last-round defection prevents exploitation in the final stage; the short punishments and probing balance exploitation risk vs. chance to restore cooperation earlier.

Edge cases
- If n = 2 (pairwise PGG reduces to a symmetrical two-player dilemma): majority threshold equals 1 — the rules still work (cooperate after mutual cooperation, punish when partner defects).
- If k is small (close to 1) so cooperation yields little group benefit: the strategy still favors cooperation early but will quickly switch to resigned if others do not reciprocate, limiting losses.
- If many players are unconditional cooperators: the strategy benefits them and sustains cooperation.
- If many players are unconditional defectors or noisy defectors: the strategy quickly (but not permanently) punishes, then gives up after a short window and probes occasionally.
- If opponents punish harshly and incoherently: short, proportionate punishments and forgiveness reduce likelihood of mutual escalation.

Summary (one-line rule)
- Start by cooperating; cooperate whenever a majority cooperated recently; when a minority defects, punish briefly in proportion to the size of defection (capped), then forgive quickly if cooperation returns; if cooperation remains low for a short window, resign to defection but probe occasionally; always defect in the final round.
'''

description_COLLECTIVE_6 = '''
Collective Conditional-Cooperation (CCC) — a simple, adaptive, forgiving strategy that maximizes collective welfare while avoiding long-term exploitation.

Principles
- Start by trying to establish group cooperation quickly.
- Cooperate when enough other players are cooperating recently.
- Withhold contribution (punish) when the group shows clear signs of free-riding.
- Punish in a limited, proportional, and forgiving way so cooperation can be re-established.
- Be conservative in the final rounds to avoid being exploited by endgame defectors.

Parameters (computed from game inputs r, n, k)
- Memory window W = min(5, max(1, round(sqrt(r)))) — how many recent rounds to judge behavior.
- Forgiveness window R = 2 — number of consecutive “good” rounds required to resume cooperation after punishment.
- Punishment length cap P_max = max(1, round(0.2 * r)) — longest punishment phase for persistent defection.
- Cooperation threshold theta (fraction of other players cooperating, evaluated over the last round or last W rounds):
  - If k/n >= 0.6, theta = 0.40 (public good is strong → be more lenient).
  - If k/n <= 0.4, theta = 0.60 (public good is weak → be stricter).
  - Otherwise theta = 0.50.
(These thresholds adapt to how valuable the public good is: stronger goods justify more trust.)

State variables tracked from history
- For each player j ≠ me: f_j = fraction of rounds (last W) in which j cooperated.
- Group recent cooperation F_last = fraction of players (excluding me) who cooperated in the immediately previous round.
- Group recent average F_avg = average_j f_j (average cooperation rate among others over last W).
- Punishment timer t_punish (0 when not punishing).

Decision rules (round t)
1. First round (t = 1): Cooperate. Signal willingness to form a cooperative norm.

2. If t == r (final round): Defect. (Avoid being exploited in the last, one-shot incentive.)

3. Otherwise evaluate recent behavior:
   - Compute F_last and F_avg as above.
   - Detect a defection event:
     - A “bad round” is when F_last < theta (i.e., fewer than the threshold fraction of others cooperated last round).
     - Detect persistent defectors if any player j has f_j < 0.25 and has defected in the last round.

4. Punishment entry:
   - If not currently punishing (t_punish == 0) and a bad round occurred, start a punishment phase:
     - Set t_punish = min(P_max, 1 + number_of_players_with_f_j < 0.5).
     - Immediately defect this round (withhold contribution).
     - Rationale: withhold contribution to reduce the payoff advantage of free-riders and signal costs of defection.

5. Punishment continuation and proportionality:
   - While t_punish > 0:
     - Defect this round.
     - After the round, decrement t_punish by 1 if the group shows improvement (F_last >= theta or F_avg rises compared to the round before punishment); otherwise keep punishing up to the cap.
     - If punish was aimed at specific persistent defectors and they have increased their f_j above 0.5, reduce t_punish faster.

6. Forgiveness and resumption of cooperation:
   - After punishment ends, require R consecutive “good” rounds before resuming unconditional cooperation:
     - During these R rounds, cooperate if F_last >= theta; otherwise re-enter punishment.
   - Once R consecutive good rounds are observed, resume normal cooperative policy (see rule 7).

7. Normal cooperative policy (when not in punishment or cooldown):
   - If F_last >= theta OR F_avg >= theta, Cooperate.
   - Otherwise, Defect (and if the bad condition is serious, enter punishment as in rule 4).

8. Targeted adjustment for persistent defectors:
   - If a small number of players persistently defect (f_j < 0.25 over W) while the rest cooperate:
     - Use proportional punishment: defect until the fraction of cooperating players among others (excluding those persistently defecting) recovers above theta, and require persistent defectors to show at least one cooperating round in W before forgiving fully.
     - This keeps punishment concentrated and avoids punishing well-behaved cooperators indefinitely.

9. Robustness notes
   - The approach is memory-limited (W small) so it adapts quickly to changing opponent behavior and does not lock into permanent retaliation.
   - Punishment is limited in duration (P_max) and conditional on observed improvement, preventing long-term mutual losses.
   - Starting with cooperation creates opportunities to reach high-payoff equilibria; the adaptive threshold theta uses k and n to tune trust.
   - Final-round defection prevents being exploited by strategies that take advantage of cooperative endgame signals.

Summary intuition
- Try to cooperate early and when most others do.
- Withhold cooperation briefly and proportionally when the group shows free-riding, but forgive quickly when cooperation returns.
- Use short memory and bounded punishment so the group can re-coordinate on high-welfare play.
- Adjust tolerance for occasional defections according to how strong the public good (k/n) is, and always avoid exploitation in the final round.
'''

description_COLLECTIVE_7 = '''
Name: Adaptive Collective Conditional Cooperation (ACCC)

Goal: Maximize collective payoff by sustaining mutual cooperation when others reciprocate, while limiting exploitation by defectors. The rule set is deterministic, uses only game parameters (n, r, k) and observed history, and is deliberately forgiving so cooperation can be re-established.

Parameters computed from game size (fixed, known at start)
- Memory window m = max(1, floor(r/5)). (Uses a window of recent rounds; short games use small m.)
- Individual cooperation threshold T_indiv = 0.5.
- Group cooperation high threshold T_high = 0.75.
- Group cooperation low threshold T_low = 0.40.
- Minimal punishment length base p_base = 1 (punishment lengths are small and proportional to observed defection).

Definitions (computed each decision round t)
- For each player j (including myself) compute coop_rate_j = fraction of rounds in the last m rounds in which j contributed (use fewer rounds if t<m).
- Group_recent_rate = average of coop_rate_j across all other players (exclude self).
- Most_recent_round_contributions = number of players who contributed in last round.

Decision rules (rounds 1..r)
1. First round (t = 1)
   - Play C (contribute 1). Start by signaling willingness to cooperate.

2. Non-final rounds (1 < t < r)
   A. If all other players have coop_rate_j = 1 over the last m rounds (unanimous recent cooperation), play C.
   B. Else if Group_recent_rate >= T_high, play C (the group is largely cooperative; reward and sustain cooperation).
   C. Else if Group_recent_rate <= T_low, play D (the group is mostly defecting; avoid giving free benefits).
   D. Else (intermediate region):
      - Identify clear defectors: set Defectors = { j : coop_rate_j < T_indiv }.
      - If Defectors is empty:
         - Use reciprocity by matching recent group behavior: if I cooperated in the last round and a majority of other players cooperated in the last round (Most_recent_round_contributions > n/2), play C; otherwise play D.
      - If Defectors non-empty:
         - Enter targeted, proportional punishment against those defectors:
           * Punishment rule: defect (play D) until the punished player's coop_rate_j over the most recent m rounds rises to at least T_indiv. For proportionality, after each round of punishment reduce remaining punishment length by 1 if the punished player contributed in that round; otherwise continue.
           * While punishing, still monitor group behavior: if overall Group_recent_rate rises above T_high during punishment, stop punishment early and resume cooperation with the whole group.
         - If more than half of players are clear defectors (|Defectors| > n/2), switch to collective safety mode: play D until Group_recent_rate recovers above T_high.

   Notes on punishment and forgiveness:
   - Punishments are short and explicitly conditional: they end as soon as the punished player's recent behavior indicates reform.
   - This prevents long cycles of mutual defection and makes cooperation attractive to return to.
   - Punish individuals (by defecting) rather than indiscriminately punishing the whole group when possible, to keep cooperation incentives for bystanders.

3. Final round (t = r)
   - Default: play D (no future to enforce cooperation).
   - Exception (collective last-round cooperation): if the last m rounds show stable unanimous cooperation among all players (every player’s coop_rate_j = 1 over that window), then play C to secure the higher collective payoff in the final round. This is only done when cooperation is already fully established and credible from history.

Additional operational rules and edge cases
- Short games (r small): m will be small; all calculations use the available history (do not pad).
- Noisy or rare one-off defections: a single defection by one player in an otherwise cooperative history triggers only short, targeted punishment (often a single-round D) before resuming cooperation. This protects against isolated opportunism while being forgiving.
- Widespread collapse: if cooperation collapses (Group_recent_rate stays below T_low for multiple successive windows), stay defecting until you observe a clear majority re-adopt cooperation (Group_recent_rate >= T_high) or unanimous behavior in the window.
- Determinism: all choices are fully determined by the computed coop_rate values and thresholds—no randomization or off-book coordination.

Collective mindset explanation (how this promotes group welfare)
- Start cooperative to signal willingness to build a cooperative equilibrium.
- Reward and sustain groups that show high recent cooperation (T_high), restoring and preserving the socially optimal all-C path.
- Use small, targeted punishments that are proportional and forgivable to deter persistent free-riders without destroying cooperation among mostly-cooperative players.
- Avoid being exploited by defecting when the group has collapsed or when many players are persistent defectors.
- Prefer full-group cooperation in the last round only when cooperation is already proven and unanimous, preserving collective payoff when it is safe and credible.

Behavior summary
- Open with cooperation.
- Cooperate while most others cooperate.
- Target and proportionally punish clear defectors, but forgive quickly when they reform.
- Revert to defection if cooperation collapses; return to cooperation when the group re-establishes cooperative behavior.
- Defect in final round unless cooperation has been perfectly stable and unanimous in recent history.

This strategy is simple, adaptive to a wide variety of opponent behaviors, aims to sustain collective cooperation when feasible, guards against exploitation, and uses forgiving, proportional punishment to restore cooperation rather than forcing permanent breakdown.
'''

description_COLLECTIVE_8 = '''
Collective Adaptive Pavlov (CAP) — a simple, forgiving, group-aware rule that starts cooperative, rewards cooperation, punishes defections briefly, and forgives to restore collective welfare.

Parameters (computed from game parameters or fixed small constants)
- n, k, r: given game parameters.
- theta_coop = max(0.5, k / n). (Group cooperation threshold: require at least this fraction of players to have cooperated in the previous round to treat the group as “cooperating.”)
- P = 2. (punishment length in full rounds)
- epsilon = 0.05. (small exploration / forgiveness probability)
- delta = 0 (tie-breaking: treat equal payoffs as “no exploitation”)

State kept from history
- last_round_contributions (how many players contributed last round).
- my_last_action and my_last_round_payoff.
- punishment_counter (how many more rounds we will defect as punishment; 0 means not punishing).

Decision rules (run each round t = 1..r)
1. First round (t = 1)
   - Play C (cooperate). This signals a collective mindset and tests whether others will reciprocate.

2. Final round (t = r)
   - Play D (defect). The one-shot dominant action; avoid being exploited in a final-stage-only interaction.

3. Penalty window (if punishment_counter > 0 and t < r)
   - Play D, decrement punishment_counter by 1 after the round.
   - Exception (forgiveness test): with probability epsilon, play C instead of D to probe whether cooperation has returned early.

4. Normal adaptive step (t > 1 and t < r and punishment_counter = 0)
   - Compute what your payoff last round actually was: pi_actual = (1 - my_last_action) + (k / n) * last_round_contributions.
   - Compute the payoff you would have gotten last round if you had defected instead (holding others’ contributions fixed): pi_if_defect = 0 + (k / n) * (last_round_contributions - my_last_action).
   - If pi_if_defect > pi_actual + delta (i.e., you would have been strictly better off by defecting last round):
       - Treat this as exploitation. Enter punishment: set punishment_counter = P and play D this round.
       - Rationale: a short firm reply discourages unilateral exploitation without ending cooperation forever.
   - Else (you were not exploited last round):
       - Use a group-oriented test to decide between C and D:
         a) If last_round_contributions / n >= theta_coop:
            - The group is cooperating enough — play C.
         b) Otherwise:
            - The group has been insufficiently cooperative — play D.
       - In either branch, with small probability epsilon flip to C (forgiveness/exploration) even if you would play D; this allows recovery from mutual defection and prevents deadlocks.

5. Extra rule to avoid needless escalation
   - If many players (e.g., > 1) defected in the last round but your own last-round payoff was still high (pi_actual >= pi_if_defect), do not punish — prefer rejoining cooperation when group signals are mixed. Punishment is only triggered by personal exploitation, not by distant group noise.

Rationale and properties
- Collective mindset: starts cooperative and prefers cooperation when the observed group cooperation rate meets a reasonable threshold (theta_coop). The threshold scales with k/n: when the public good is relatively more productive, we require at least a modest majority to continue cooperating.
- Personal-adaptive Pavlovic reaction: we punish only when we were personally better off defecting last round — that signals we were exploited. This ties retaliation to direct experience rather than noisy hypotheses about motives.
- Short, limited punishment (P rounds) prevents permanent mutual defection (avoids "grim" outcomes) but still provides deterrence. Small-probability forgiveness (epsilon) allows recovery from noise or mistaken punishment.
- Endgame safety: defect in the last round to avoid final-stage exploitation. (If you prefer to risk cooperating with obviously naive opponents in final round for extra group payoff, you can set the last-round rule to use the same adaptive test instead of forced D; the safe default is D.)
- Robustness: uses only observable history and game parameters, tolerates noise, punishes exploiters, forgives, and favors collective outcomes when the group shows sufficient cooperation.

Summary pseudo-flow (plain language)
- Round 1: cooperate.
- Each later round until the last:
  - If currently serving a punishment period: defect (but occasionally probe with cooperation).
  - Else, if you would have gained by defecting last round (given what others did): begin a short punishment and defect.
  - Otherwise, cooperate if a sufficient fraction of players cooperated last round (threshold = max(0.5, k/n)); otherwise defect. Occasionally cooperate anyway with small probability to restore cooperation.
- Last round: defect.

This strategy is simple, relies only on parameters and observed history, promotes group welfare when others reciprocate, is robust to exploitation, and is forgiving enough to recover cooperation after mistakes.
'''
